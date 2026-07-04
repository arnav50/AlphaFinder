"""Phase 8c — F&O ALERT ENGINE.

Evaluate rules against the F&O data (FNO_PLAN / FNO_VCP / FNO_VPROFILE / OPTION_CHAIN_META)
and fire alerts in multiple forms. New triggers only (dedup via .fno_alerts_state.json, reset
daily), so you are not spammed with the same condition every cycle.

USAGE
  py -3.10 31_fno_alerts.py               # one-shot: evaluate the current CSVs, fire new alerts
  py -3.10 31_fno_alerts.py --watch 5     # LIVE: refresh (28,29,30) + evaluate every 5 minutes
  py -3.10 31_fno_alerts.py --reset       # clear today's dedup state (re-fire everything)

DELIVERY (all optional via env vars; console + FNO_ALERTS.csv are always on)
  FNO_ALERT_BEAP=0            disable the Windows beep (default on)
  FNO_ALERT_TOAST=1          Windows toast via BurntToast module if installed (default off)
  FNO_ALERT_WEBHOOK=<url>    HTTP POST {"text": ...} (Slack / Discord / Teams / your server)
  TELEGRAM_TOKEN=<t> TELEGRAM_CHAT=<id>   Telegram message

ADD YOUR OWN CONDITION: append a function to RULES (see the examples). Each rule receives the
loaded data and yields (level, code, message) tuples. `code` must be stable+unique per trigger.
"""
import os, sys, json, time, subprocess, datetime, urllib.request, urllib.parse
import pandas as pd

try:                       # Windows consoles default to cp1252 — emojis/₹/→ in messages need UTF-8
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STATE = ".fno_alerts_state.json"
LOG   = "FNO_ALERTS.csv"
REFRESH_SCRIPTS = ["28_option_chain.py", "29_fno_trade.py", "30_fno_vcp.py"]


# ----------------------------- data -----------------------------
def _csv(f):
    try:
        return pd.read_csv(f)
    except Exception:
        return pd.DataFrame()


def load_data():
    plan_df = _csv("FNO_PLAN.csv")
    return {"plan": (plan_df.iloc[0].to_dict() if len(plan_df) else None),
            "vcp": _csv("FNO_VCP.csv"), "vprofile": _csv("FNO_VPROFILE.csv"),
            "ocmeta": _csv("OPTION_CHAIN_META.csv"), "chain": _csv("OPTION_CHAIN.csv")}


# ----------------------------- RULES -----------------------------
# Each rule: def(data) -> iterable of (level, code, message). Edit / add freely.
def r_trade_verdict(d):
    p = d["plan"]
    if p and str(p.get("verdict")) == "GO":
        yield ("HIGH", f"verdict-go:{p.get('expiry')}", f"Trade setup GO — {p.get('headline', '')}")
    if p and str(p.get("verdict")) == "WATCH" and str(p.get("confidence")) == "high":
        yield ("MED", f"verdict-watch:{p.get('expiry')}", f"Trade setup WATCH (high conf) — {p.get('headline', '')}")


def r_vcp_breakout(d, tf="5m"):
    v = d["vcp"]
    if not len(v): return
    for _, r in v[(v["tf"] == tf) & (v["status"] == "Breakout")].iterrows():
        yield ("HIGH", f"vcpbrk:{r['expiry']}:{r['strike']}:{r['side']}:{tf}",
               f"VCP breakout — {r['strike']} {r['side']} ({r['expiry']}) @{tf}")
    for _, r in v[(v["tf"] == tf) & (v["status"] == "VCP forming") & (v["tightening"] == True)].iterrows():
        yield ("MED", f"vcpform:{r['expiry']}:{r['strike']}:{r['side']}:{tf}",
               f"VCP forming (tightening) — {r['strike']} {r['side']} ({r['expiry']}) @{tf}")


def r_ema_cross(d, tf="5m"):
    v = d["vcp"]
    if not len(v): return
    for _, r in v[(v["tf"] == tf) & (v["ema_cross"] == "golden")].iterrows():
        yield ("MED", f"golden:{r['expiry']}:{r['strike']}:{r['side']}:{tf}",
               f"EMA 10/20 GOLDEN cross — {r['strike']} {r['side']} ({r['expiry']}) @{tf}")
    for _, r in v[(v["tf"] == tf) & (v["ema_cross"] == "death")].iterrows():
        yield ("LOW", f"death:{r['expiry']}:{r['strike']}:{r['side']}:{tf}",
               f"EMA 10/20 DEATH cross — {r['strike']} {r['side']} ({r['expiry']}) @{tf}")


def r_liquidity(d, tf="5m"):
    v = d["vcp"]
    if not len(v): return
    m = (v["tf"] == tf) & (v["smc_liq"].astype(str).str.contains("swept"))
    for _, r in v[m].iterrows():
        yield ("MED", f"liq:{r['expiry']}:{r['strike']}:{r['side']}:{tf}",
               f"Liquidity sweep — {r['strike']} {r['side']} ({r['expiry']}) @{tf}: {r['smc_liq']}")


def r_vprofile(d):
    v = d["vprofile"]
    if not len(v): return
    for _, r in v[v["vp_bias"].astype(str).str.contains("momentum")].iterrows():
        yield ("MED", f"vpmom:{r['expiry']}:{r['strike']}:{r['side']}",
               f"VP momentum long — {r['strike']} {r['side']} ({r['expiry']}): entry {r['vp_entry']} SL {r['vp_sl']} tgt {r['vp_target']} R:R {r['vp_rr']}")


def r_pcr(d, hi=1.30, lo=0.70):
    for _, m in d["ocmeta"].iterrows():
        pcr = m.get("pcr")
        if pd.isna(pcr): continue
        if pcr >= hi:
            yield ("LOW", f"pcrhi:{m['expiry']}", f"PCR {pcr} ≥ {hi} (put-heavy / bullish) — {m['expiry']}")
        elif pcr <= lo:
            yield ("LOW", f"pcrlo:{m['expiry']}", f"PCR {pcr} ≤ {lo} (call-heavy / bearish) — {m['expiry']}")


# ---- manual per-strike conditions from ALERTS_CONFIG.csv (user-entered) ----
CHAIN_FIELD = {"ltp": "ltp", "oi": "oi", "iv": "iv", "vol": "vol", "chg_oi": "chg_oi", "chg": "chg"}
INTRA_FIELD = {"vcp": "status", "ema": "ema_sig", "vwap": "vwap_pos", "structure": "smc_struct",
               "zone": "smc_zone", "liq": "smc_liq", "trend": "smc_trend"}


def _cmp(a, op, b):
    try:
        af, bf = float(a), float(b)
        return {">": af > bf, "<": af < bf, ">=": af >= bf, "<=": af <= bf,
                "==": af == bf, "!=": af != bf}.get(op, False)
    except (TypeError, ValueError):
        a, b = str(a), str(b)
        if op == "contains": return b.lower() in a.lower()
        if op == "==": return a.lower() == b.lower()
        if op == "!=": return a.lower() != b.lower()
        return False


def _clean(v):
    return "" if (v is None or (isinstance(v, float) and pd.isna(v))) else str(v).strip()


def r_manual(d):
    try:
        cfg = pd.read_csv("ALERTS_CONFIG.csv", comment="#", skipinitialspace=True)
    except Exception:
        cfg = pd.DataFrame()
    if not len(cfg): return
    chain, vcp = d["chain"], d["vcp"]
    for idx, c in cfg.iterrows():
        metric, op, val = _clean(c.get("metric")).lower(), _clean(c.get("op")), _clean(c.get("value"))
        exp, strk, side = _clean(c.get("expiry")), _clean(c.get("strike")), _clean(c.get("side")).upper()
        tf, note = _clean(c.get("tf")), _clean(c.get("note"))
        if not metric or not op or val == "":
            continue
        if metric in INTRA_FIELD and len(vcp):
            col = INTRA_FIELD[metric]; m = pd.Series(True, index=vcp.index)
            if exp and exp != "*": m &= vcp["expiry"].astype(str) == exp
            if strk and strk != "*": m &= vcp["strike"].astype(str) == strk
            if side and side != "*": m &= vcp["side"].astype(str) == side
            if tf: m &= vcp["tf"].astype(str) == tf
            for _, r in vcp[m].iterrows():
                if _cmp(r.get(col), op, val):
                    yield ("HIGH", f"man:{r['expiry']}:{r['strike']}:{r['side']}:{metric}:{op}:{val}:{tf}",
                           f"[manual] {r['strike']} {r['side']} ({r['expiry']}) {metric}{'@'+tf if tf else ''} {op} {val} — now {r.get(col)}" + (f" · {note}" if note else ""))
        elif metric in CHAIN_FIELD and len(chain):
            m = pd.Series(True, index=chain.index)
            if exp and exp != "*": m &= chain["expiry"].astype(str) == exp
            if strk and strk != "*": m &= chain["strike"].astype(str) == strk
            for _, r in chain[m].iterrows():
                for sd in (["CE", "PE"] if side in ("", "*") else [side]):
                    col = ("ce_" if sd == "CE" else "pe_") + CHAIN_FIELD[metric]
                    if col in r and _cmp(r.get(col), op, val):
                        yield ("HIGH", f"man:{r['expiry']}:{r['strike']}:{sd}:{metric}:{op}:{val}",
                               f"[manual] {r['strike']} {sd} ({r['expiry']}) {metric} {op} {val} — now {r.get(col)}" + (f" · {note}" if note else ""))


RULES = [r_manual, r_trade_verdict, r_vcp_breakout, r_ema_cross, r_liquidity, r_vprofile, r_pcr]


# --------------------------- delivery ---------------------------
def _beep():
    if os.environ.get("FNO_ALERT_BEAP", "1") != "1": return
    try:
        import winsound; winsound.Beep(880, 200)
    except Exception:
        sys.stdout.write("\a"); sys.stdout.flush()


def _toast(title, msg):
    if os.environ.get("FNO_ALERT_TOAST", "0") != "1": return
    safe = msg.replace("'", "").replace('"', "")
    try:
        subprocess.Popen(["powershell", "-NoProfile", "-Command",
                          f"$ErrorActionPreference='SilentlyContinue';"
                          f"if(Get-Module -ListAvailable BurntToast){{Import-Module BurntToast;"
                          f"New-BurntToastNotification -Text '{title}','{safe}'}}"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def _webhook(text):
    url = os.environ.get("FNO_ALERT_WEBHOOK")
    if not url: return
    try:
        req = urllib.request.Request(url, data=json.dumps({"text": text}).encode(),
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass


def _telegram(text):
    tk, ch = os.environ.get("TELEGRAM_TOKEN"), os.environ.get("TELEGRAM_CHAT")
    if not (tk and ch): return
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{tk}/sendMessage?chat_id={ch}"
                               f"&text=" + urllib.parse.quote(text), timeout=10)
    except Exception:
        pass


_C = {"HIGH": "\033[91m", "MED": "\033[93m", "LOW": "\033[90m"}


def deliver(level, code, msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{level}] {msg}"
    print(f"{_C.get(level, '')}🔔 {ts}  {line}\033[0m", flush=True)
    pd.DataFrame([{"time": ts, "level": level, "code": code, "message": msg}]).to_csv(
        LOG, mode="a", header=not os.path.exists(LOG), index=False)
    _beep(); _toast("AlphaFinder F&O", msg); _webhook(line); _telegram(line)


# ----------------------------- state ----------------------------
def load_state():
    today = datetime.date.today().isoformat()
    try:
        st = json.load(open(STATE))
        if st.get("date") == today:
            return set(st.get("codes", []))
    except Exception:
        pass
    return set()


def save_state(codes):
    json.dump({"date": datetime.date.today().isoformat(), "codes": sorted(codes)}, open(STATE, "w"))


def evaluate_once():
    data = load_data()
    fired = load_state()
    n = 0
    for rule in RULES:
        try:
            for level, code, msg in rule(data):
                if code in fired:
                    continue
                fired.add(code); deliver(level, code, msg); n += 1
        except Exception as e:
            print(f"  (rule {rule.__name__} error: {e})", flush=True)
    save_state(fired)
    if n == 0:
        print(f"  {datetime.datetime.now():%H:%M:%S} — no new alerts", flush=True)
    return n


def refresh():
    for s in REFRESH_SCRIPTS:
        subprocess.call([sys.executable, "-u", s])


def main():
    args = sys.argv[1:]
    if "--reset" in args:
        try: os.remove(STATE)
        except OSError: pass
        print("alert state cleared."); return
    watch = 0
    if "--watch" in args:
        i = args.index("--watch")
        watch = int(args[i + 1]) if i + 1 < len(args) else 5
    print(f"F&O alert engine — {'WATCH every %dm' % watch if watch else 'one-shot'} | rules: {len(RULES)}", flush=True)
    while True:
        if watch:
            refresh()
        evaluate_once()
        if not watch:
            break
        time.sleep(watch * 60)


if __name__ == "__main__":
    main()
