"""Generate a self-contained HTML dashboard (alphafinder_dashboard.html) from the phase CSVs.
Data is embedded as JSON so the file opens by double-click (no server needed)."""
import os, json, time, datetime, requests, pandas as pd, numpy as np

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

def load(f, cols=None):
    d = pd.read_csv(f, dtype={"symbol": str})
    if cols: d = d[[c for c in cols if c in d.columns]]
    return d

# Layer-1 validation thresholds (see validate_watchlist.py)
MIN_ADV_VALUE = 20_000_000   # Rs 2 crore/day median traded value
VOL_SPIKE     = 1.5          # breakout volume vs 50d avg
MAX_EXT_PCT   = 5.0          # don't chase >5% above entry
RS_WINDOW     = 63           # ~3 trading months for relative strength

def fetch_ohlc(ticker, session, suffixes=(".NS", ".BO")):
    """Return (DataFrame[close,high,low,volume], live_price, prev_close) from Yahoo daily 1y."""
    for suf in suffixes:
        try:
            r = session.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}{suf}",
                            params={"range": "1y", "interval": "1d"}, timeout=20)
            res = r.json()["chart"]["result"][0]; q = res["indicators"]["quote"][0]
            df = pd.DataFrame({"close": q["close"], "high": q["high"],
                               "low": q["low"], "volume": q["volume"]}).dropna().reset_index(drop=True)
            if len(df) > 60:
                meta = res["meta"]
                live = meta.get("regularMarketPrice") or float(df["close"].iloc[-1])
                prev = meta.get("previousClose") or meta.get("chartPreviousClose")
                return df, float(live), (float(prev) if prev else None)
        except Exception:
            pass
    return None, None, None

def pct_return(series, n):
    n = min(n, len(series) - 1)
    return float((series.iloc[-1] / series.iloc[-1 - n] - 1) * 100) if n > 0 else None

def enrich_watchlist(df):
    """Add live-price + Layer-1 GO/WATCH/DROP validation columns from one fresh fetch each."""
    sx = requests.Session(); sx.headers.update({"User-Agent": UA})
    market = None
    try:
        ndf, nlive, _ = fetch_ohlc("%5ENSEI", sx, suffixes=("",))
        nifty_ret = pct_return(ndf["close"], RS_WINDOW) or 0.0
        nc = ndf["close"]
        spot = float(nlive) if nlive else float(nc.iloc[-1])
        ema50 = float(nc.ewm(span=50, adjust=False).mean().iloc[-1])
        ema200 = float(nc.ewm(span=200, adjust=False).mean().iloc[-1])
        if spot >= ema50 >= ema200:   trend = "UPTREND"
        elif spot <= ema50 <= ema200: trend = "DOWNTREND"
        else:                         trend = "SIDEWAYS"
        market = {"nifty": round(spot), "ema50": round(ema50), "ema200": round(ema200), "trend": trend}
    except Exception:
        nifty_ret = 0.0
    keys = ["live", "live_chg", "live_state", "live_to_entry", "vol_x", "ext_pct",
            "adv_cr", "rs", "verdict", "vreason", "vpassed", "vfails",
            "stage", "stage_pct", "upside_tgt"]
    out = {k: [] for k in keys}
    def push(**kw):
        for k in keys: out[k].append(kw.get(k))
    for _, r in df.iterrows():
        entry, stop = float(r["pivot_entry"]), float(r["stop"])
        ohlc, live, prev = fetch_ohlc(r["symbol"], sx)
        if ohlc is None:
            push(verdict="NO DATA"); time.sleep(0.2); continue
        c, v = ohlc["close"], ohlc["volume"]
        sma50 = v.iloc[-50:].mean()
        vol_x = float(v.iloc[-5:].max() / sma50) if sma50 else 0.0
        adv = float((c * v).iloc[-20:].median())
        ext = (live / entry - 1) * 100
        rs = (pct_return(c, RS_WINDOW) or 0.0) - nifty_ret
        chk = {"alive": live > stop, "liquid": adv >= MIN_ADV_VALUE, "triggered": live >= entry,
               "vol_ok": vol_x >= VOL_SPIKE, "not_ext": ext <= MAX_EXT_PCT, "rs_ok": rs > 0}
        if not chk["alive"]:        verdict, reason = "DROP", "below stop"
        elif not chk["liquid"]:     verdict, reason = "DROP", "illiquid"
        elif all([chk["triggered"], chk["vol_ok"], chk["not_ext"], chk["rs_ok"]]):
            verdict, reason = "GO", "all checks pass"
        elif chk["triggered"] and not chk["not_ext"]:
            verdict, reason = "WATCH", "extended (chasing)"
        elif not chk["triggered"]:  verdict, reason = "WATCH", "staging (not triggered)"
        else:                       verdict, reason = "WATCH", "weak confirmation"
        if live >= entry:   state, to_entry = "above", 0.0
        elif live <= stop:  state, to_entry = "stop", None
        else:               state, to_entry = "pending", round((entry / live - 1) * 100, 2)
        # stage: EARLY (coiled below entry) / MOVING (broke out, advancing) / FAILED (below stop)
        tgt = float(r["target2"])
        if live <= stop:
            stage, stage_pct, upside_tgt = "FAILED", None, None
        elif live >= entry:
            stage = "MOVING"
            stage_pct = round((live - entry) / (tgt - entry) * 100, 1) if tgt > entry else None  # % of move done
            upside_tgt = round((tgt / live - 1) * 100, 1)
        else:
            stage = "EARLY"
            stage_pct = round((entry / live - 1) * 100, 1)                                        # % rise to trigger
            upside_tgt = round((tgt / live - 1) * 100, 1)
        push(live=round(live, 2), stage=stage, stage_pct=stage_pct, upside_tgt=upside_tgt,
             live_chg=round((live / prev - 1) * 100, 2) if prev else None,
             live_state=state, live_to_entry=to_entry,
             vol_x=round(vol_x, 1), ext_pct=round(ext, 1), adv_cr=round(adv / 1e7, 2),
             rs=round(rs, 1), verdict=verdict, vreason=reason,
             vpassed=int(sum(chk.values())),
             vfails=",".join(k for k, ok in chk.items() if not ok) or "none")
        time.sleep(0.2)
    df = df.copy()
    for k in keys: df[k] = out[k]
    return df, nifty_ret, market

p1 = load("FINAL_universe_25pct.csv")
p2 = load("PHASE2_SCORECARD.csv")
p3 = load("PHASE3_SMC.csv")
p4 = load("PHASE4_VCP_GANN.csv")
p6 = load("PHASE6_RANKING.csv")
wl = load("PHASE7_WATCHLIST.csv")
fp = load("PHASE5_FINGERPRINT.csv")
try:                                        # Phase 7b — short-term swing plans (26_swing.py)
    sw = load("SWING_TRADES.csv")
except Exception:
    sw = pd.DataFrame()
try:                                        # Phase 7c — intraday plans (27_intraday.py)
    iz = load("INTRADAY_TRADES.csv")
except Exception:
    iz = pd.DataFrame()
try:                                        # Phase 8 — live Nifty option chain (28_option_chain.py)
    oc = pd.read_csv("OPTION_CHAIN.csv")
    oc_meta = json.loads(pd.read_csv("OPTION_CHAIN_META.csv").to_json(orient="records"))  # one row per expiry
except Exception:
    oc, oc_meta = pd.DataFrame(), []
try:                                        # Phase 9 — F&O trade finder (29_fno_trade.py)
    fno_plan_df = pd.read_csv("FNO_PLAN.csv")
    fno_trades_df = pd.read_csv("FNO_TRADES.csv")
except Exception:
    fno_plan_df, fno_trades_df = pd.DataFrame(), pd.DataFrame()
try:                                        # Phase 8b — intraday per-strike VCP scan (30_fno_vcp.py)
    fno_vcp_df = pd.read_csv("FNO_VCP.csv")
except Exception:
    fno_vcp_df = pd.DataFrame()
try:                                        # volume-profile entry/SL plan (30_fno_vcp.py)
    fno_vprofile_df = pd.read_csv("FNO_VPROFILE.csv")
except Exception:
    fno_vprofile_df = pd.DataFrame()
try:                                        # fired alerts log (31_fno_alerts.py) — newest first
    fno_alerts_df = pd.read_csv("FNO_ALERTS.csv").tail(40).iloc[::-1]
except Exception:
    fno_alerts_df = pd.DataFrame()

# ---------- live prices + Layer-1 validation for the watchlist (fetched fresh at build time) ----------
nifty_ret = None
market = None
try:
    wl, nifty_ret, market = enrich_watchlist(wl)
    live_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    vc = wl["verdict"].value_counts().to_dict()
    print(f"Live + validation: {int(wl['live'].notna().sum())}/{len(wl)} fetched @ {live_ts} | "
          + " ".join(f"{k}={v}" for k, v in vc.items()))
except Exception as e:
    live_ts = None
    for k in ["live","live_chg","live_state","live_to_entry","vol_x","ext_pct","adv_cr","rs","verdict","vreason","vpassed","vfails"]:
        if k not in wl.columns: wl[k] = None
    print(f"Live/validation fetch skipped ({e}) — dashboard will show scan-time close only")

# ---------- qualify filter: show only stocks that still qualify (GO / WATCH) ----------
# Drop the disqualified names (DROP = below stop / illiquid / failed; AVOID = below 50-EMA).
# Count is dynamic — fewer or more depending on how many pass verification on the day.
# Fallback: if live validation was skipped, verdict is None → nothing is hidden.
wl_total = len(wl)
if "verdict" in wl.columns:
    wl = wl[wl["verdict"].fillna("") != "DROP"].reset_index(drop=True)
wl_hidden = wl_total - len(wl)

sw_total = len(sw)
if len(sw) and "verdict" in sw.columns:
    sw = sw[sw["verdict"].fillna("") != "AVOID"].reset_index(drop=True)
sw_hidden = sw_total - len(sw)

iz_total = len(iz)
if len(iz) and "verdict" in iz.columns:
    iz = iz[iz["verdict"].fillna("") != "AVOID"].reset_index(drop=True)
iz_hidden = iz_total - len(iz)
print(f"Qualify filter: watchlist {len(wl)}/{wl_total} shown ({wl_hidden} DROP hidden) | "
      f"swing {len(sw)}/{sw_total} shown ({sw_hidden} AVOID hidden) | "
      f"intraday {len(iz)}/{iz_total} shown ({iz_hidden} AVOID hidden)")

# ---------- master: one row per Phase-1 stock, fields from all phases ----------
m = p6.merge(p1[["symbol","price_180d_ago","price_today","avg_daily_volume","penny_flag"]], on="symbol", how="left")
m = m.merge(p2[["symbol","rsi","adx","macd_pos","ema_alignment","supertrend","candle_bias","trend_structure"]], on="symbol", how="left")
m = m.merge(p3[["symbol","pd_zone","range_pos_pct","last_BoS","bull_OB","unfilled_bull_FVG","liquidity_swept","structure_W"]], on="symbol", how="left")
m = m.merge(p4[["symbol","vcp_quality","vcp_status","contractions","pivot","pct_from_pivot","gann_gann_trend","octave","sq9_T1_+0.25","sq9_T2_+0.5"]], on="symbol", how="left")

def recs(df):
    return json.loads(df.where(pd.notna(df), None).to_json(orient="records"))

DATA = {
 "master": recs(m),
 "watchlist": recs(wl),
 "swing": recs(sw),
 "intraday": recs(iz),
 "fingerprint": recs(fp),
 "option_chain": recs(oc),
 "oc_meta": oc_meta,
 "fno_plan": (json.loads(fno_plan_df.to_json(orient="records"))[0] if len(fno_plan_df) else None),
 "fno_trades": recs(fno_trades_df),
 "fno_vcp": recs(fno_vcp_df),
 "fno_vprofile": recs(fno_vprofile_df),
 "fno_alerts": recs(fno_alerts_df),
 "agg": {
   "universe_total": 4524,
   "phase1": int(len(p1)),
   "analyzed": int(len(p2)),
   "alpha": int((p6["tier"].isin(["TIER 1","TIER 2"])).sum()),
   "prime_passers": int(len(load("PHASE7_ALL_PASSERS.csv"))) if True else 0,
   "watchlist": int(len(wl)),
   "wl_hidden": int(wl_hidden),
   "sw_hidden": int(sw_hidden),
   "iz_hidden": int(iz_hidden),
   "tiers6": p6["tier"].value_counts().to_dict(),
   "scorecards": p2["scorecard"].value_counts().to_dict(),
   "sectors_wl": wl["sector"].value_counts().to_dict() if "sector" in wl else {},
   "vcp_quality": p4["vcp_quality"].value_counts().to_dict(),
   "pd_zone": p3["pd_zone"].value_counts().to_dict(),
 },
 "market": market or {"nifty": "—", "ema50": "—", "ema200": "—", "trend": "UNKNOWN"},
 "scan_date": datetime.date.today().strftime("%Y-%m-%d"),
 "live_fetched_at": live_ts,
 "nifty_3m": round(nifty_ret, 1) if nifty_ret is not None else None,
}

HTML = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AlphaFinder — Systematic Equity Scanner</title>
<style>
:root{
 --bg:#0b0e14; --bg2:#121722; --bg3:#1a2130; --line:#243044; --txt:#e6edf3; --mut:#8b97a8;
 --accent:#3b82f6; --green:#22c55e; --red:#ef4444; --amber:#f59e0b; --cyan:#22d3ee; --violet:#a78bfa;
}
*{box-sizing:border-box} html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
header{padding:20px 28px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,#10151f,#0b0e14)}
.brand{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.logo{width:38px;height:38px;border-radius:9px;background:linear-gradient(135deg,var(--accent),var(--violet));display:grid;place-items:center;font-weight:800;font-size:18px}
h1{font-size:20px;margin:0;letter-spacing:.3px} .sub{color:var(--mut);font-size:12.5px;margin-top:2px}
.banner{margin:14px 28px 0;padding:10px 14px;border-radius:9px;border:1px solid #5b3b18;background:#2a1d0c;color:#ffce8a;font-size:13px;display:flex;gap:10px;align-items:center}
.banner.down{border-color:#5e2230;background:#2a1117;color:#ff9aa6}
nav{display:flex;gap:4px;padding:14px 24px 0;flex-wrap:wrap;border-bottom:1px solid var(--line);background:var(--bg)}
nav button{background:none;border:none;color:var(--mut);padding:10px 14px;border-radius:8px 8px 0 0;cursor:pointer;font-size:13.5px;font-weight:600;border-bottom:2px solid transparent}
nav button:hover{color:var(--txt);background:var(--bg2)}
nav button.active{color:var(--txt);border-bottom-color:var(--accent)}
main{padding:24px 28px;max-width:1500px}
section{display:none} section.active{display:block;animation:fade .25s}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1}}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-bottom:22px}
.card{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:16px}
.card .k{color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.5px}
.card .v{font-size:28px;font-weight:800;margin-top:6px} .card .v small{font-size:13px;color:var(--mut);font-weight:500}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:22px} @media(max-width:900px){.grid2{grid-template-columns:1fr}}
.panel{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:18px;margin-bottom:22px}
.panel h3{margin:0 0 14px;font-size:14px;letter-spacing:.3px}
.funnel{display:flex;flex-direction:column;gap:8px}
.fbar{display:flex;align-items:center;gap:12px}
.fbar .lbl{width:230px;color:var(--mut);font-size:13px}
.fbar .bar{height:26px;border-radius:6px;background:linear-gradient(90deg,var(--accent),var(--violet));display:flex;align-items:center;justify-content:flex-end;padding:0 8px;color:#fff;font-weight:700;font-size:12px;min-width:42px}
.bars .row{display:flex;align-items:center;gap:10px;margin-bottom:7px}
.bars .row .nm{width:130px;font-size:12.5px;color:var(--mut)}
.bars .row .tk{flex:1;height:18px;background:var(--bg3);border-radius:5px;overflow:hidden}
.bars .row .tk i{display:block;height:100%;border-radius:5px}
.bars .row .ct{width:42px;text-align:right;font-weight:700;font-size:12.5px}
.toolbar{display:flex;gap:10px;align-items:center;margin-bottom:12px;flex-wrap:wrap}
input.search{background:var(--bg2);border:1px solid var(--line);color:var(--txt);padding:9px 12px;border-radius:8px;width:280px;font-size:13px}
.pill{font-size:11px;padding:2px 8px;border-radius:20px;font-weight:700;white-space:nowrap}
.t1{background:#0e2a16;color:#5ef08a;border:1px solid #1c5a30}
.t2{background:#0e1f33;color:#7db8ff;border:1px solid #1d426e}
.t3{background:#2a230c;color:#ffce6a;border:1px solid #5b4a18}
.ex{background:#2a1117;color:#ff8c99;border:1px solid #5e2230}
.bull{color:var(--green);font-weight:700}.bear{color:var(--red);font-weight:700}.neu{color:var(--mut)}
.tablewrap{overflow:auto;border:1px solid var(--line);border-radius:12px;max-height:72vh}
table{border-collapse:collapse;width:100%;font-size:12.8px;white-space:nowrap}
thead th{position:sticky;top:0;background:var(--bg3);color:var(--mut);text-align:right;padding:10px 12px;font-weight:700;cursor:pointer;border-bottom:1px solid var(--line);user-select:none}
thead th:first-child,tbody td:first-child{text-align:left}
thead th.l,tbody td.l{text-align:left}
thead th:hover{color:var(--txt)}
tbody td{padding:9px 12px;text-align:right;border-bottom:1px solid #161d2a}
tbody tr:hover{background:var(--bg3);cursor:pointer}
.sym{font-weight:700;color:var(--cyan)}
.pos{color:var(--green)}.neg{color:var(--red)}
.muted{color:var(--mut)}
.modal{position:fixed;inset:0;background:rgba(3,6,12,.7);display:none;place-items:center;z-index:50;padding:20px}
.modal.open{display:grid}
.sheet{background:var(--bg2);border:1px solid var(--line);border-radius:16px;max-width:760px;width:100%;max-height:88vh;overflow:auto;padding:24px}
.sheet h2{margin:0 0 2px;font-size:20px}.sheet .x{float:right;cursor:pointer;color:var(--mut);font-size:22px;line-height:1}
.kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin-top:16px}
.kv .i{background:var(--bg3);border:1px solid var(--line);border-radius:9px;padding:10px 12px}
.kv .i .kk{color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.4px}
.kv .i .vv{font-size:14px;font-weight:600;margin-top:3px}
.sech{margin:18px 0 6px;color:var(--violet);font-size:12px;text-transform:uppercase;letter-spacing:.6px;font-weight:700}
.foot{color:var(--mut);font-size:11.5px;padding:24px 28px;border-top:1px solid var(--line);margin-top:20px}
.legend{display:flex;gap:14px;flex-wrap:wrap;color:var(--mut);font-size:12px;margin-top:8px}
</style></head><body>
<header>
 <div class="brand">
   <div class="logo">α</div>
   <div><h1>AlphaFinder <span class="muted" style="font-weight:500">· Systematic Equity Scanner (NSE + BSE)</span></h1>
   <div class="sub">7-phase pipeline · live exchange data · scan date <b id="sd"></b></div></div>
 </div>
 <div class="banner down" id="mkt"></div>
</header>
<nav id="nav"></nav>
<main>
 <section id="overview" class="active">
   <div class="cards" id="cards"></div>
   <div class="grid2">
     <div class="panel"><h3>Discovery funnel</h3><div class="funnel" id="funnel"></div></div>
     <div class="panel"><h3>Phase 6 tier distribution</h3><div class="bars" id="tiers"></div>
        <h3 style="margin-top:18px">Phase 2 scorecards</h3><div class="bars" id="scards"></div></div>
   </div>
   <div class="grid2">
     <div class="panel"><h3>VCP quality (Phase 4)</h3><div class="bars" id="vcpq"></div></div>
     <div class="panel"><h3>Watchlist sector breadth (Phase 7)</h3><div class="bars" id="wsec"></div></div>
   </div>
 </section>

 <section id="watchlist">
   <div class="panel" style="margin-bottom:18px"><h3>🎯 Phase 7 — Forward 25%+ Watchlist</h3>
     <div class="muted">Fresh candidates from the full universe matching the Phase-5 move-initiation fingerprint (≥6/9 confluence) + secondary validation. Every name R:R ≥ 3:1. Entry=breakout pivot, Stop=1.8×ATR. <b>Market is in a downtrend — stage, don't chase.</b></div>
     <div class="muted" id="wl_live_ts" style="margin-top:6px"></div></div>
   <div class="toolbar"><input class="search" id="s_wl" placeholder="Filter watchlist… (symbol / sector / stage)"></div>
   <div class="tablewrap"><table id="t_wl"></table></div>
 </section>

 <section id="fno">
   <div class="panel" style="margin-bottom:18px"><h3>🔔 Alerts <span class="muted" style="font-weight:500;font-size:13px">— triggered F&amp;O conditions · run <code>py 31_fno_alerts.py --watch 5</code> for live (console · beep · CSV · webhook/Telegram)</span></h3>
     <div id="fno_alerts_box"></div>
     <div class="sech" style="margin-top:16px">➕ Add a manual per-strike alert</div>
     <div class="muted">Build a condition and click <b>Add alert</b> — it appends to <code>ALERTS_CONFIG.csv</code> automatically when the helper is running (<code>py alert_server.py</code>); otherwise it hands you the line to paste. Use <b>*</b> for every strike / expiry / side.</div>
     <div class="toolbar" style="margin-top:8px" id="ab_row"></div>
     <div id="ab_out" style="margin-top:8px"></div></div>

   <div class="panel" style="margin-bottom:18px"><h3>🎯 F&amp;O Trade Setup — the 7-phase Watchlist method applied to the Nifty chain</h3>
     <div id="fno_headline" class="muted">Run <code>py 29_fno_trade.py</code> to generate the setup.</div>
     <div class="cards" id="fno_cards" style="margin-top:14px"></div>
     <div class="sech" style="margin-top:18px">Phase-by-phase read</div>
     <div id="fno_phases"></div></div>

   <div class="panel" style="margin-bottom:18px"><h3>📋 Candidate trades (ranked by confluence)</h3>
     <div class="muted">Built mechanically from the phases above. Entry = option LTP · stop = bounded 30–50% of premium · target mapped from the underlying move to the OI level via approx delta · size = 1% risk on ₹10L (lot 75). <b>Mechanical signals — not investment advice.</b></div>
     <div class="tablewrap" style="margin-top:10px"><table id="t_ft"></table></div></div>

   <div class="panel" style="margin-bottom:14px"><h3>🔮 Nifty 50 — Option Chain · 5 strikes (ATM ±2) per expiry</h3>
     <div class="muted" id="oc_sub">Live NSE option chain — current + upcoming expiries this month.</div>
     <div class="legend" style="margin-top:8px"><span><b style="color:var(--cyan)">◄ATM</b> = at-the-money</span><span style="color:var(--green)">● green LTP = in-the-money</span><span>Calls ITM below spot · Puts ITM above spot</span><span><b>Mechanical NSE data — not investment advice.</b></span></div></div>
   <div class="panel" style="margin-bottom:18px"><h3>🔬 Per-strike indicator analysis</h3>
     <div class="muted">Pick one indicator to analyse every strike individually, per expiry. Bars scale to the largest value within each expiry; ATM marked ◄.</div>
     <div class="toolbar" style="margin-top:10px"><label class="muted" for="oc_ind">Indicator:</label>
       <select id="oc_ind" style="background:var(--bg2);border:1px solid var(--line);color:var(--txt);padding:8px 10px;border-radius:8px;font-size:13px"></select></div>
     <div class="muted" id="oc_ind_note" style="margin-top:2px"></div>
     <div id="oc_analysis" style="margin-top:12px"></div></div>
   <div id="oc_expiries"></div>
 </section>

 <section id="swing">
   <div class="panel" style="margin-bottom:18px"><h3>⚡ Short Term Trade — swing setups on the watchlist</h3>
     <div class="muted">The Phase-7 watchlist read on <b>daily</b> bars (no intraday). Each name is classified by its <b>EMA20/50/200 trend</b> and swing <b>setup</b> — <b>breakout</b> (20-day high), <b>pullback</b> (20-EMA reclaim), <b>base</b>, <b>extended</b> or <b>weak</b>. <b>Entry</b> = breakout pivot or 20-EMA reclaim · <b>Stop</b> = tightest valid of recent swing-low / 2×ATR / structural stop · <b>Target</b> = the daily structural swing target. Typical hold <b>~1–3 weeks</b>.</div>
     <div class="muted" id="sw_ts" style="margin-top:6px"></div></div>
   <div class="toolbar"><input class="search" id="s_sw" placeholder="Filter… (symbol / sector / setup / signal)"></div>
   <div class="tablewrap"><table id="t_sw"></table></div>
 </section>

 <section id="intraday">
   <div class="panel" style="margin-bottom:18px"><h3>⏱️ Intraday — same-session setups on the watchlist</h3>
     <div class="muted">The Phase-7 watchlist read on <b>15-minute</b> bars. Each name is classified by its intraday <b>EMA9/20/50</b> stack vs <b>session VWAP</b> and its <b>setup</b> — <b>ORB</b> (30-min opening-range break), <b>momentum</b> (trending above VWAP), <b>VWAP reclaim</b>, <b>pullback</b>, <b>extended</b> or <b>weak</b>. <b>Entry</b> = opening-range break / VWAP reclaim / join · <b>Stop</b> = tightest valid of session VWAP / day-low / 1.5×ATR · <b>Target</b> = 2R · <b>Risk</b> 0.5% · hold <b>same session</b>.</div>
     <div class="muted" id="iz_ts" style="margin-top:6px"></div></div>
   <div class="toolbar"><input class="search" id="s_iz" placeholder="Filter… (symbol / sector / setup / signal)"></div>
   <div class="tablewrap"><table id="t_iz"></table></div>
 </section>

 <section id="ranking">
   <div class="toolbar"><input class="search" id="s_m" placeholder="Filter 311 ranked stocks… (symbol / sector / tier)">
     <span class="muted" id="m_count"></span></div>
   <div class="tablewrap"><table id="t_m"></table></div>
   <div class="legend"><span>Click any row for the full multi-phase dossier.</span></div>
 </section>

 <section id="fingerprint">
   <div class="panel" style="margin-bottom:18px"><h3>🧬 Phase 5 — Move-Initiation Fingerprint (Day-0 DNA)</h3>
     <div class="muted">Indicator state captured at the exact breakout bar of all 311 winners, then aggregated. Higher consistency % = more reliable filter. Backtest recall of the ≥6/9 filter on known winners: <b>76.2%</b>.</div></div>
   <div class="tablewrap"><table id="t_fp"></table></div>
 </section>
</main>
<div class="modal" id="modal"><div class="sheet" id="sheet"></div></div>
<div class="foot">Generated from live NSE/BSE + Yahoo Finance data via the AlphaFinder pipeline. Mechanical signals — sanity-check against live charts and overhead supply. <b>Not investment advice.</b></div>
<script>
const DATA = __DATA__;
const $=s=>document.querySelector(s), el=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
$("#sd").textContent=DATA.scan_date;
const mk=DATA.market;$("#mkt").innerHTML=`⚠️ <b>Market context:</b> Nifty 50 = ${mk.nifty} &nbsp;|&nbsp; EMA50 ${mk.ema50} &nbsp;|&nbsp; EMA200 ${mk.ema200} &nbsp;→&nbsp; <b>${mk.trend}</b> &nbsp;·&nbsp; reduce size / await 50-EMA reclaim before acting.`;
if(DATA.live_fetched_at)$("#wl_live_ts").innerHTML=`🟢 <b>Live</b> prices + <b>validation</b> fetched <b>${DATA.live_fetched_at}</b> (Yahoo). <b>Check</b> = Layer-1 mechanical verdict: <span class="pill t1">✓ GO</span> alive+triggered+volume+RS+not-extended · <span class="pill t3">… WATCH</span> alive but not a clean trigger · <span class="pill ex">✕ DROP</span> below stop / illiquid.${DATA.nifty_3m!=null?` Nifty 3-mo: <b>${DATA.nifty_3m>0?'+':''}${DATA.nifty_3m}%</b> (RS baseline).`:''} <b>Stage:</b> <span class="pill t2">● early</span> coiled below entry (% = rise needed to trigger) · <span class="pill t1">▲ moving</span> broke out, advancing (% = move done) · <span class="pill ex">✕ failed</span> below stop. <i>Mechanical only — still check surveillance/earnings/chart.</i>${DATA.agg.wl_hidden?` <br><b>Showing ${DATA.watchlist.length} qualifying</b> (GO/WATCH) · <b>${DATA.agg.wl_hidden}</b> disqualified (DROP — below stop / illiquid) hidden.`:''}`;

const TABS=[["overview","Overview"],["watchlist","🎯 Watchlist"],["fno","🔮 F&O Chain"],["swing","⚡ Short Term Trade"],["intraday","⏱️ Intraday"],["ranking","Ranked 311"],["fingerprint","🧬 Fingerprint"]];
const nav=$("#nav");
TABS.forEach(([id,lb],i)=>{const b=el("button",i==0?"active":"",lb);b.onclick=()=>{document.querySelectorAll("nav button").forEach(x=>x.classList.remove("active"));b.classList.add("active");document.querySelectorAll("section").forEach(s=>s.classList.remove("active"));$("#"+id).classList.add("active")};nav.appendChild(b)});

// ---- overview ----
const A=DATA.agg;
const cards=[["Universe scanned",A.universe_total,""],["Phase 1: 25%+ movers",A.phase1,"verified"],["Fully analysed",A.analyzed,"stocks"],["Alpha list (T1+T2)",A.alpha,"Phase 6"],["Prime-filter passers",A.prime_passers,"of 4,524"],["Final watchlist",A.watchlist,"R:R≥3"]];
cards.forEach(([k,v,s])=>{const c=el("div","card");c.innerHTML=`<div class="k">${k}</div><div class="v">${v} <small>${s}</small></div>`;$("#cards").appendChild(c)});
const funnel=[["NSE+BSE universe",A.universe_total],["Phase 1 — 25%+ in 180d",A.phase1],["Phases 2-4 analysed",A.analyzed],["Phase 6 Alpha (T1+T2)",A.alpha],["Phase 7 prime passers",A.prime_passers],["Final watchlist",A.watchlist]];
const fmax=A.universe_total;
funnel.forEach(([l,v])=>{const r=el("div","fbar");r.innerHTML=`<div class="lbl">${l}</div><div class="bar" style="width:${Math.max(4,v/fmax*100)}%">${v}</div>`;$("#funnel").appendChild(r)});
function bars(host,obj,order,colors){const max=Math.max(...Object.values(obj));const keys=order||Object.keys(obj);keys.forEach(k=>{if(obj[k]==null)return;const r=el("div","row");r.innerHTML=`<div class="nm">${k}</div><div class="tk"><i style="width:${obj[k]/max*100}%;background:${(colors&&colors[k])||'var(--accent)'}"></i></div><div class="ct">${obj[k]}</div>`;host.appendChild(r)})}
bars($("#tiers"),A.tiers6,["TIER 1","TIER 2","TIER 3","EXCLUDE"],{"TIER 1":"var(--green)","TIER 2":"var(--cyan)","TIER 3":"var(--amber)","EXCLUDE":"var(--red)"});
bars($("#scards"),A.scorecards,["BULLISH","MILD BULLISH","NEUTRAL","MILD BEARISH","BEARISH"],{"BULLISH":"var(--green)","MILD BULLISH":"#6fcf97","NEUTRAL":"var(--mut)","MILD BEARISH":"#f0a35e","BEARISH":"var(--red)"});
bars($("#vcpq"),A.vcp_quality,["Strong VCP","Moderate VCP","No VCP"],{"Strong VCP":"var(--green)","Moderate VCP":"var(--cyan)","No VCP":"var(--mut)"});
bars($("#wsec"),A.sectors_wl,null,{});

// ---- table builder ----
function buildTable(tbl, rows, cols, opts){
 opts=opts||{}; tbl.innerHTML="";
 const thead=el("thead"),tr=el("tr");
 cols.forEach(c=>{const th=el("th",c.l?"l":"",c.h);th.onclick=()=>sortBy(c.k);tr.appendChild(th)});
 thead.appendChild(tr);tbl.appendChild(thead);
 const tb=el("tbody");tbl.appendChild(tb);
 let sortKey=opts.sort||cols[0].k, asc=false;
 function render(list){tb.innerHTML="";list.forEach(r=>{const trr=el("tr");cols.forEach(c=>{const td=el("td",c.l?"l":"");td.innerHTML=c.f?c.f(r[c.k],r):fmt(r[c.k]);trr.appendChild(td)});if(opts.onclick)trr.onclick=()=>opts.onclick(r);tb.appendChild(trr)})}
 function sortBy(k){asc=(k===sortKey)?!asc:false;sortKey=k;const s=[...(tbl._data)].sort((a,b)=>{let x=a[k],y=b[k];if(x==null)return 1;if(y==null)return -1;if(typeof x==="number"&&typeof y==="number")return asc?x-y:y-x;return asc?(""+x).localeCompare(""+y):(""+y).localeCompare(""+x)});render(s)}
 tbl._data=rows; tbl._render=render; tbl._sort=sortBy;
 sortBy(sortKey);
}
function fmt(v){if(v==null)return '<span class="muted">—</span>';if(typeof v==="number")return Number.isInteger(v)?v.toLocaleString():v;return v}
function tierPill(t){const m={"TIER 1":"t1","TIER 2":"t2","TIER 3":"t3","EXCLUDE":"ex"};return `<span class="pill ${m[t]||''}">${t}</span>`}
function sgn(v){if(v==null)return fmt(v);const c=v>=0?"pos":"neg";return `<span class="${c}">${v>0?'+':''}${v}%</span>`}
function vcpCell(v){if(!v||v=="No VCP")return '<span class="muted">—</span>';return v.includes("Strong")?`<span class="bull">${v}</span>`:`<span style="color:var(--cyan)">${v}</span>`}
function scCell(v){if(!v)return '—';if(v.includes("BULL"))return `<span class="bull">${v}</span>`;if(v.includes("BEAR"))return `<span class="bear">${v}</span>`;return `<span class="neu">${v}</span>`}
function liveCell(v,r){if(v==null)return '<span class="muted">—</span>';const c=r.live_chg==null?'':(r.live_chg>=0?'pos':'neg');const ch=r.live_chg==null?'':` <small class="${c}">${r.live_chg>0?'+':''}${r.live_chg}%</small>`;return `<b>${v}</b>${ch}`}
function liveStatus(r){if(r.live==null)return '<span class="muted">—</span>';if(r.live_state=='above')return '<span class="pill t1">▲ above entry</span>';if(r.live_state=='stop')return '<span class="pill ex">▼ below stop</span>';return `<span class="muted">+${r.live_to_entry}% to entry</span>`}
function valCell(r){const v=r.verdict;if(!v||v=='NO DATA')return '<span class="muted">—</span>';const m={GO:'t1',WATCH:'t3',DROP:'ex'},ic={GO:'✓',WATCH:'…',DROP:'✕'};const tip=`${r.vreason} · ${r.vpassed}/6 checks pass · fails: ${r.vfails} · vol ${r.vol_x}× · ext ${r.ext_pct}% · ₹${r.adv_cr}cr/d · RS ${r.rs>0?'+':''}${r.rs}%`;return `<span class="pill ${m[v]}" title="${tip}">${ic[v]} ${v}</span>`}
function stageCell(r){const s=r.stage;if(!s||s=='NO DATA')return '<span class="muted">—</span>';if(s=='MOVING')return `<span class="pill t1" title="${r.stage_pct}% of the entry→target move already done">▲ moving <small>${r.stage_pct}%</small></span>`;if(s=='FAILED')return '<span class="pill ex" title="below stop — setup invalidated">✕ failed</span>';return `<span class="pill t2" title="coiled — needs +${r.stage_pct}% to trigger the breakout entry">● early <small>+${r.stage_pct}%</small></span>`}

// ---- watchlist table ----
buildTable($("#t_wl"), DATA.watchlist, [
 {k:"rank",h:"#"},{k:"symbol",h:"Symbol",l:1,f:v=>`<span class="sym">${v}</span>`},
 {k:"verdict",h:"Check",l:1,f:(v,r)=>valCell(r)},
 {k:"name",h:"Company",l:1,f:v=>`<span class="muted">${(v||'').slice(0,22)}</span>`},
 {k:"sector",h:"Sector",l:1},{k:"close",h:"Scan px"},
 {k:"live",h:"Live",f:liveCell},{k:"live_to_entry",h:"vs Plan",l:1,f:(v,r)=>liveStatus(r)},
 {k:"stage",h:"Stage",l:1,f:(v,r)=>stageCell(r)},{k:"upside_tgt",h:"Upside→T",f:v=>v==null?'<span class="muted">—</span>':`<span class="pos">+${v}%</span>`},
 {k:"vcp_status",h:"VCP stage",l:1,f:v=>v&&v.includes("PIVOT")?`<span style="color:var(--cyan)">at pivot</span>`:v&&v.includes("BROKEN")?`<span class="bull">fresh BO</span>`:`<span class="muted">${v}</span>`},
 {k:"rsi",h:"RSI"},{k:"adx",h:"ADX"},{k:"pivot_entry",h:"Entry"},{k:"stop",h:"Stop"},
 {k:"stop_pct",h:"Stop%",f:v=>`${v}%`},{k:"target2",h:"Target"},
 {k:"rr",h:"R:R",f:v=>`<b style="color:${v>=4?'var(--green)':'var(--cyan)'}">${v}</b>`},
 {k:"qty_per_10L",h:"Qty/₹10L"},{k:"phase7_score",h:"Score"},{k:"tier",h:"Tier",f:tierPill}
], {sort:"rank", onclick:r=>showDetail(r,true)});

// ---- short-term swing table ----
function swVerdict(r){const v=r.verdict;if(!v||v=='NO DATA')return '<span class="muted">—</span>';const m={GO:'t1',WATCH:'t3',AVOID:'ex'},ic={GO:'✓',WATCH:'…',AVOID:'✕'};return `<span class="pill ${m[v]||''}" title="${r.reason||''}">${ic[v]||''} ${v}</span>`}
function setupCell(v){if(!v)return '—';if(v=='BREAKOUT')return '<span class="bull">breakout</span>';if(v=='PULLBACK')return '<span style="color:var(--cyan)">pullback</span>';if(v=='EXTENDED')return '<span class="bear">extended</span>';if(v=='WEAK')return '<span class="bear">weak</span>';return `<span class="neu">${(v||'').toLowerCase()}</span>`}
function trendCell(v){if(!v)return '—';if(v.indexOf('up')>=0)return `<span class="bull">${v}</span>`;if(v=='down')return '<span class="bear">down</span>';return `<span class="neu">${v}</span>`}
function swLive(v,r){if(v==null)return '<span class="muted">—</span>';const c=r.chg_pct==null?'':(r.chg_pct>=0?'pos':'neg');const ch=r.chg_pct==null?'':` <small class="${c}">${r.chg_pct>0?'+':''}${r.chg_pct}%</small>`;return `<b>${v}</b>${ch}`}
const SW=DATA.swing||[];
if(SW.length){
 buildTable($("#t_sw"), SW, [
  {k:"symbol",h:"Symbol",l:1,f:v=>`<span class="sym">${v}</span>`},
  {k:"verdict",h:"Signal",l:1,f:(v,r)=>swVerdict(r)},
  {k:"name",h:"Company",l:1,f:v=>`<span class="muted">${(v||'').slice(0,20)}</span>`},
  {k:"sector",h:"Sector",l:1},
  {k:"live",h:"Live",f:swLive},{k:"trend",h:"Trend",l:1,f:trendCell},
  {k:"setup",h:"Setup",l:1,f:setupCell},{k:"d_rsi",h:"RSI"},
  {k:"ema20",h:"20-EMA"},{k:"dist_ema20",h:"vs 20E",f:sgn},
  {k:"swing_entry",h:"Entry"},{k:"swing_stop",h:"Stop"},
  {k:"stop_pct",h:"Stop%",f:v=>v==null?'<span class="muted">—</span>':`${v}%`},
  {k:"swing_target",h:"Target"},
  {k:"rr",h:"R:R",f:v=>v==null?'<span class="muted">—</span>':`<b style="color:${v>=4?'var(--green)':'var(--cyan)'}">${v}</b>`},
  {k:"qty_per_10L",h:"Qty/₹10L"},{k:"horizon",h:"Hold",l:1},
  {k:"phase7_score",h:"Score"},{k:"tier",h:"Tier",f:tierPill}
 ], {sort:"st_order", onclick:r=>showSwing(r)});
 const swc=SW.reduce((a,r)=>{a[r.verdict]=(a[r.verdict]||0)+1;return a},{});
 $("#sw_ts").innerHTML=`⚡ <b>Swing read</b> on daily bars · <span class="pill t1">✓ GO</span> breakout/pullback in an uptrend · <span class="pill t3">… WATCH</span> basing / extended, await a trigger. <b>Showing ${SW.length} qualifying — GO ${swc.GO||0} · WATCH ${swc.WATCH||0}</b>${DATA.agg.sw_hidden?` · <b>${DATA.agg.sw_hidden}</b> AVOID (below 50-EMA) hidden`:''}. <i>Mechanical — sanity-check the chart and overhead supply.</i>`;
} else {
 $("#t_sw").innerHTML='<tbody><tr><td style="padding:18px" class="muted">No SWING_TRADES.csv — run <b>python 26_swing.py</b> first.</td></tr></tbody>';
}
function showSwing(r){
 const s=$("#sheet");
 let h=`<span class="x" onclick="document.getElementById('modal').classList.remove('open')">&times;</span><h2>${r.symbol} — ${r.name||''}</h2>`;
 h+=`<div class="muted">${r.sector||''} ${r.tier?'· ':''}${r.tier?tierPill(r.tier):''} · ${swVerdict(r)}</div>`;
 h+='<div class="sech">Daily swing read</div><div class="kv">';
 h+=row("Live",r.live==null?'—':`${r.live}${r.chg_pct==null?'':' ('+(r.chg_pct>0?'+':'')+r.chg_pct+'%)'}`)+row("Trend",r.trend)+row("Setup",(r.setup||'').toLowerCase())+row("RSI(14)",r.d_rsi)+row("ATR(14)",r.d_atr)+row("EMA 20 / 50 / 200",`${r.ema20} / ${r.ema50} / ${r.ema200}`)+row("vs 20-EMA",r.dist_ema20==null?'—':(r.dist_ema20>0?'+':'')+r.dist_ema20+'%')+row("20-day high",r.bo_level)+"</div>";
 h+='<div class="sech">Swing plan (daily structure)</div><div class="kv">';
 h+=row("Entry",r.swing_entry)+row("Stop",r.swing_stop)+row("Stop %",r.stop_pct==null?'—':r.stop_pct+'%')+row("Target",r.swing_target)+row("Risk:Reward",r.rr)+row("Qty / ₹10L (1% risk)",r.qty_per_10L)+row("Hold horizon",r.horizon)+row("Confluence score",r.phase7_score)+"</div>";
 h+=`<div class="muted" style="margin-top:14px">${r.reason||''}</div>`;
 s.innerHTML=h; $("#modal").classList.add("open");
}

// ---- intraday table ----
function izSetupCell(v){if(!v)return '—';if(v=='ORB')return '<span class="bull">ORB break</span>';if(v=='MOMENTUM')return '<span class="bull">momentum</span>';if(v=='VWAP_RECLAIM')return '<span style="color:var(--cyan)">VWAP reclaim</span>';if(v=='PULLBACK')return '<span style="color:var(--cyan)">pullback</span>';if(v=='EXTENDED')return '<span class="bear">extended</span>';if(v=='WEAK')return '<span class="bear">weak</span>';return `<span class="neu">${(v||'').toLowerCase()}</span>`}
const IZ=DATA.intraday||[];
if(IZ.length){
 buildTable($("#t_iz"), IZ, [
  {k:"symbol",h:"Symbol",l:1,f:v=>`<span class="sym">${v}</span>`},
  {k:"verdict",h:"Signal",l:1,f:(v,r)=>swVerdict(r)},
  {k:"name",h:"Company",l:1,f:v=>`<span class="muted">${(v||'').slice(0,20)}</span>`},
  {k:"sector",h:"Sector",l:1},
  {k:"live",h:"Live",f:swLive},{k:"itrend",h:"Trend",l:1,f:trendCell},
  {k:"setup",h:"Setup",l:1,f:izSetupCell},{k:"i_rsi",h:"RSI"},
  {k:"ivwap",h:"VWAP"},{k:"dist_vwap",h:"vs VWAP",f:sgn},
  {k:"intraday_entry",h:"Entry"},{k:"intraday_stop",h:"Stop"},
  {k:"stop_pct",h:"Stop%",f:v=>v==null?'<span class="muted">—</span>':`${v}%`},
  {k:"intraday_target",h:"Target"},
  {k:"rr",h:"R:R",f:v=>v==null?'<span class="muted">—</span>':`<b style="color:${v>=2?'var(--green)':'var(--cyan)'}">${v}</b>`},
  {k:"qty_per_10L",h:"Qty/₹10L"},{k:"horizon",h:"Hold",l:1},
  {k:"phase7_score",h:"Score"},{k:"tier",h:"Tier",f:tierPill}
 ], {sort:"it_order", onclick:r=>showIntraday(r)});
 const izc=IZ.reduce((a,r)=>{a[r.verdict]=(a[r.verdict]||0)+1;return a},{});
 $("#iz_ts").innerHTML=`⏱️ <b>Intraday read</b> on 15-min bars · <span class="pill t1">✓ GO</span> ORB/momentum/VWAP-reclaim above VWAP · <span class="pill t3">… WATCH</span> holding/extended, await a trigger. <b>Showing ${IZ.length} qualifying — GO ${izc.GO||0} · WATCH ${izc.WATCH||0}</b>${DATA.agg.iz_hidden?` · <b>${DATA.agg.iz_hidden}</b> AVOID (below VWAP) hidden`:''}. <i>Mechanical — uses the last session's bars; sanity-check live before the open.</i>`;
} else {
 $("#t_iz").innerHTML='<tbody><tr><td style="padding:18px" class="muted">No INTRADAY_TRADES.csv — run <b>python 27_intraday.py</b> first.</td></tr></tbody>';
}
function showIntraday(r){
 const s=$("#sheet");
 let h=`<span class="x" onclick="document.getElementById('modal').classList.remove('open')">&times;</span><h2>${r.symbol} — ${r.name||''}</h2>`;
 h+=`<div class="muted">${r.sector||''} ${r.tier?'· ':''}${r.tier?tierPill(r.tier):''} · ${swVerdict(r)}</div>`;
 h+='<div class="sech">Intraday read (15-min bars)</div><div class="kv">';
 h+=row("Live",r.live==null?'—':`${r.live}${r.chg_pct==null?'':' ('+(r.chg_pct>0?'+':'')+r.chg_pct+'%)'}`)+row("Trend",r.itrend)+row("Setup",(r.setup||'').replace('_',' ').toLowerCase())+row("RSI(14)",r.i_rsi)+row("ATR(14)",r.i_atr)+row("Session VWAP",r.ivwap)+row("vs VWAP",r.dist_vwap==null?'—':(r.dist_vwap>0?'+':'')+r.dist_vwap+'%')+row("EMA 9 / 20 / 50",`${r.ema9} / ${r.ema20} / ${r.ema50}`)+row("Opening range (H/L)",r.orb_high==null?'—':`${r.orb_high} / ${r.orb_low}`)+row("Day high / low",r.day_high==null?'—':`${r.day_high} / ${r.day_low}`)+"</div>";
 h+='<div class="sech">Intraday plan (2R, 0.5% risk)</div><div class="kv">';
 h+=row("Entry",r.intraday_entry)+row("Stop",r.intraday_stop)+row("Stop %",r.stop_pct==null?'—':r.stop_pct+'%')+row("Target (2R)",r.intraday_target)+row("Risk:Reward",r.rr)+row("Qty / ₹10L (0.5% risk)",r.qty_per_10L)+row("Hold horizon",r.horizon)+row("Confluence score",r.phase7_score)+"</div>";
 h+=`<div class="muted" style="margin-top:14px">${r.reason||''}</div>`;
 s.innerHTML=h; $("#modal").classList.add("open");
}

// ---- master ranking table ----
const M=DATA.master;
buildTable($("#t_m"), M, [
 {k:"rank",h:"#"},{k:"symbol",h:"Symbol",l:1,f:v=>`<span class="sym">${v}</span>`},
 {k:"name",h:"Company",l:1,f:v=>`<span class="muted">${(v||'').slice(0,24)}</span>`},
 {k:"exchange",h:"Exch",l:1},{k:"sector",h:"Sector",l:1},
 {k:"return_pct_final",h:"6m Ret",f:sgn},{k:"close",h:"Price"},
 {k:"scorecard",h:"P2 Verdict",l:1,f:scCell},
 {k:"TOTAL_100",h:"P6 /100",f:v=>`<b>${v}</b>`},{k:"tier",h:"Tier",f:tierPill},
 {k:"vcp_quality",h:"VCP",l:1,f:vcpCell},{k:"pd_zone",h:"P/D",l:1},
 {k:"rsi",h:"RSI"},{k:"adx",h:"ADX"},{k:"supertrend",h:"S/T",l:1,f:v=>v&&v.includes("green")?'<span class="bull">green</span>':'<span class="bear">red</span>'}
], {sort:"rank", onclick:r=>showDetail(r,false)});
$("#m_count").textContent=M.length+" stocks";

// ---- fingerprint table ----
buildTable($("#t_fp"), DATA.fingerprint, [
 {k:"indicator",h:"Indicator",l:1,f:v=>`<b>${v}</b>`},{k:"type",h:"Type",l:1,f:v=>`<span class="muted">${v}</span>`},
 {k:"min",h:"Min"},{k:"max",h:"Max"},{k:"avg",h:"Avg"},{k:"median",h:"Median"},
 {k:"most_common_zone",h:"Most-common zone",l:1,f:v=>`<span style="color:var(--cyan)">${v}</span>`},
 {k:"consistency_pct",h:"Consistency",f:v=>{const c=v>=80?'var(--green)':v>=60?'var(--amber)':'var(--mut)';return `<b style="color:${c}">${v}%</b>`}}
], {sort:"consistency_pct"});

// ---- F&O trade setup + phases (Phase 9) ----
(function(){
 const P=DATA.fno_plan, FT=DATA.fno_trades||[];
 if(!P){return;}
 const vc={GO:'t1',WATCH:'t3',AVOID:'ex'}[P.verdict]||'';
 $("#fno_headline").innerHTML=`<span class="pill ${vc}" style="font-size:13px">${P.verdict}</span> <b>${P.direction}</b> bias · confidence <b>${P.confidence}</b> · ${P.expiry} (DTE ${P.dte}) · <span class="muted">spot ${P.spot} · as of NSE ${P.nse_timestamp}</span><div style="margin-top:10px;font-size:15px;font-weight:600">${P.headline}</div>`;
 const cards=[["Direction",P.direction,P.tier!=='—'?P.tier:''],["Verdict",P.verdict,"score "+P.score],["Confidence",P.confidence,""],["ATM IV",P.atm_iv,P.iv_regime],["Expected move",'±'+Math.round(P.exp_move),"pts to expiry"],["PCR · Max-pain",P.pcr+' · '+P.max_pain,"S "+P.support+" / R "+P.resistance]];
 cards.forEach(([k,v,s])=>{const c=el("div","card");c.innerHTML=`<div class="k">${k}</div><div class="v">${v} <small>${s}</small></div>`;$("#fno_cards").appendChild(c)});
 const PH=[["1 · Discovery",P.p1],["2 · Technicals — price bias",P.p2],["3 · OI structure",P.p3],["4 · Volatility / expected move",P.p4],["5 · Alignment → direction",P.p5],["6 · Confluence ranking",P.p6],["7 · Trade plan",P.p7]];
 const ph=$("#fno_phases");
 PH.forEach(([k,v])=>{const d=el("div");d.style.cssText="padding:9px 0;border-bottom:1px solid #161d2a";d.innerHTML=`<b style="color:var(--violet)">Phase ${k}</b><div class="muted" style="margin-top:3px">${v||'—'}</div>`;ph.appendChild(d)});
 if(FT.length){
   const rrCell=v=>v==null?'—':`<b style="color:${v>=1.5?'var(--green)':v>=1?'var(--amber)':'var(--red)'}">${v}</b>`;
   buildTable($("#t_ft"), FT, [
    {k:"strategy",h:"Strategy",l:1,f:v=>`<b>${v}</b>`},{k:"instrument",h:"Instrument",l:1,f:v=>`<span class="muted">${v}</span>`},
    {k:"entry",h:"Entry ₹"},{k:"stop",h:"Stop ₹"},{k:"target",h:"Target ₹"},{k:"rr",h:"R:R",f:rrCell},
    {k:"lots",h:"Lots"},{k:"qty",h:"Qty"},{k:"score",h:"Score",f:v=>`<b>${v}</b>`},{k:"tier",h:"Tier",l:1,f:tierPill}
   ], {sort:"score"});
 } else { $("#t_ft").innerHTML='<tbody><tr><td class="muted" style="padding:14px">No directional candidates — price &amp; OI not aligned (stay flat).</td></tr></tbody>'; }
})();

// ---- F&O alerts log + manual alert builder (Phase 8c) ----
(function(){
 const box=$("#fno_alerts_box"); if(!box) return;
 const A=DATA.fno_alerts||[], col={HIGH:'var(--red)',MED:'var(--amber)',LOW:'var(--mut)'};
 box.innerHTML = A.length ? A.map(a=>`<div style="display:flex;gap:10px;padding:6px 0;border-bottom:1px solid #161d2a;font-size:12.8px"><span class="muted" style="width:150px;flex:none">${a.time||''}</span><span style="width:52px;flex:none;font-weight:700;color:${col[a.level]||'var(--mut)'}">${a.level||''}</span><span>${a.message||''}</span></div>`).join('')
   : '<div class="muted">No alerts logged yet. Run <code>py 31_fno_alerts.py</code> (or <code>--watch 5</code> for live).</div>';
 const row=$("#ab_row"); if(!row) return;
 const OC=DATA.option_chain||[], MS=DATA.oc_meta||[];
 const ss="background:var(--bg2);border:1px solid var(--line);color:var(--txt);padding:7px 9px;border-radius:8px;font-size:12.5px";
 const mksel=(id,opts)=>`<select id="${id}" style="${ss}">${opts.map(o=>`<option value="${o[0]}">${o[1]}</option>`).join('')}</select>`;
 row.innerHTML=
   `<label class="muted">Expiry</label>${mksel("ab_exp",[["*","* any"]].concat(MS.map(m=>[m.expiry,m.expiry])))}`+
   `<label class="muted">Strike</label>${mksel("ab_strike",[["*","* any"]])}`+
   `<label class="muted">Side</label>${mksel("ab_side",[["*","*"],["CE","CE"],["PE","PE"]])}`+
   `<label class="muted">Metric</label>${mksel("ab_metric",[["ltp","LTP"],["oi","OI"],["iv","IV"],["vol","Volume"],["chg_oi","Chg OI"],["chg","Chg"],["vcp","VCP status"],["ema","EMA sig"],["vwap","VWAP pos"],["structure","Structure"],["zone","P/D zone"],["liq","Liquidity"],["trend","Trendline"]])}`+
   `<label class="muted">Op</label>${mksel("ab_op",[[">",">"],["<","<"],[">=",">="],["<=","<="],["==","=="],["!=","!="],["contains","contains"]])}`+
   `<input id="ab_val" class="search" style="width:110px" placeholder="value (e.g. 200 or Breakout)">`+
   `<label class="muted">TF</label>${mksel("ab_tf",[["","—"],["1m","1m"],["3m","3m"],["5m","5m"],["15m","15m"],["1h","1h"]])}`+
   `<input id="ab_note" class="search" style="width:150px" placeholder="note (optional)">`+
   `<button id="ab_gen" style="${ss};cursor:pointer;font-weight:700">➕ Add alert</button>`;
 function fillStrikes(){const exp=$("#ab_exp").value;const ks=[...new Set(OC.filter(r=>exp==='*'||r.expiry===exp).map(r=>r.strike))].sort((a,b)=>a-b);$("#ab_strike").innerHTML='<option value="*">* any</option>'+ks.map(k=>`<option value="${k}">${k}</option>`).join('');}
 $("#ab_exp").onchange=fillStrikes; fillStrikes();
 $("#ab_gen").onclick=()=>{
  const g=id=>($(id).value||'').trim();
  const rec={expiry:g("#ab_exp"),strike:g("#ab_strike"),side:g("#ab_side"),metric:g("#ab_metric"),op:g("#ab_op"),value:g("#ab_val"),tf:g("#ab_tf"),note:g("#ab_note")};
  const line=[rec.expiry,rec.strike,rec.side,rec.metric,rec.op,rec.value,rec.tf,rec.note].join(",");
  const out=$("#ab_out"); out.innerHTML='<span class="muted">Adding…</span>';
  const host=("__ALPHA_BACKEND__"||(location.protocol==='http:'?'':'http://localhost:8777'));   // build-time backend URL, else same-origin / local helper
  fetch(host+"/add-alert",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(rec)})
   .then(r=>r.json()).then(j=>{
     out.innerHTML = j.ok
       ? `<span style="color:var(--green)">✓ Appended to ALERTS_CONFIG.csv:</span> <code>${line}</code>`
       : `<span style="color:var(--red)">✕ ${j.error||'rejected'}</span> — metric, op and value are required.`;
   })
   .catch(()=>{ out.innerHTML=`<div class="muted" style="margin-bottom:4px">Auto-append helper not running (start <code>py alert_server.py</code>). Meanwhile, copy this line into <code>ALERTS_CONFIG.csv</code>:</div><input class="search" style="width:100%;font-family:monospace" readonly value="${line.replace(/"/g,'&quot;')}" onclick="this.select()">`; });
 };
})();

// ---- option chain per expiry (Phase 8) ----
(function(){
 const OC=DATA.option_chain||[], MS=DATA.oc_meta||[], host=$("#oc_expiries");
 if(!MS.length||!OC.length){$("#oc_sub").innerHTML='Option chain unavailable — run <code>py 28_option_chain.py</code> first (fetches live NSE data).';return;}
 $("#oc_sub").innerHTML=`<b>NIFTY</b> · ${MS.length} expiry(ies) this month · spot <b>${MS[0].spot}</b> · as of NSE <b>${MS[0].nse_timestamp}</b> · fetched ${MS[0].fetched_at}. 5 strikes (ATM ±2) per expiry. <i>Snapshot — rerun 28_option_chain.py to refresh.</i>`;
 const num=(v,nd)=>v==null?'—':Number(v).toLocaleString('en-IN',{maximumFractionDigits:nd==null?0:nd,minimumFractionDigits:nd==null?0:nd});
 const chg=v=>{if(v==null)return '—';const c=v>0?'pos':v<0?'neg':'muted';return `<span class="${c}">${v>0?'+':''}${num(v)}</span>`};
 const ce=(v,r)=>`<b style="color:${r.ce_itm?'var(--green)':'var(--mut)'}">${num(v,2)}</b>`;
 const pe=(v,r)=>`<b style="color:${r.pe_itm?'var(--green)':'var(--mut)'}">${num(v,2)}</b>`;
 MS.forEach(M=>{
   const rows=OC.filter(r=>r.expiry===M.expiry);
   const pcrTag=M.pcr==null?'':(M.pcr>=1?'put-heavy (bullish)':'call-heavy (bearish)');
   const panel=el("div","panel"); panel.style.marginBottom="18px";
   panel.innerHTML=`<h3>🗓️ ${M.expiry} <span class="muted" style="font-weight:500;font-size:13px">· DTE ${M.dte} · ATM ${M.atm} · PCR ${M.pcr}${pcrTag?' ('+pcrTag+')':''} · max-pain ${M.max_pain}</span></h3>`;
   const wrap=el("div","tablewrap"); wrap.style.marginTop="10px"; const tbl=el("table"); wrap.appendChild(tbl); panel.appendChild(wrap);
   host.appendChild(panel);
   buildTable(tbl, rows, [
    {k:"ce_oi",h:"OI",f:v=>num(v)},{k:"ce_chg_oi",h:"Chg OI",f:chg},{k:"ce_vol",h:"Volume",f:v=>num(v)},
    {k:"ce_iv",h:"IV",f:v=>num(v,2)},{k:"ce_ltp",h:"CALL LTP",f:ce},
    {k:"strike",h:"STRIKE",l:1,f:(v,r)=>`<b style="color:${r.atm?'var(--green)':'var(--cyan)'}">${v}${r.atm?' ◄ATM':''}</b>`},
    {k:"pe_ltp",h:"PUT LTP",f:pe},{k:"pe_iv",h:"IV",f:v=>num(v,2)},{k:"pe_vol",h:"Volume",f:v=>num(v)},
    {k:"pe_chg_oi",h:"Chg OI",f:chg},{k:"pe_oi",h:"OI",f:v=>num(v)}
   ], {sort:"strike"});
   tbl._sort("strike");   // ascending strike (low -> high)
 });

 // ---- per-strike single-indicator analysis (dropdown) ----
 const IND=[
  {k:"oi",lbl:"Open Interest (OI)",ce:"ce_oi",pe:"pe_oi",nd:0,note:"Total open contracts per strike. Highest CE OI = resistance; highest PE OI = support."},
  {k:"chgoi",lbl:"Change in OI",ce:"ce_chg_oi",pe:"pe_chg_oi",nd:0,signed:true,note:"OI added (coloured) or shed (red) today. Rising CE OI = call writing (resistance); rising PE OI = put writing (support)."},
  {k:"vol",lbl:"Volume (contracts)",ce:"ce_vol",pe:"pe_vol",nd:0,note:"Contracts traded today — activity & liquidity per strike."},
  {k:"iv",lbl:"Implied Volatility (IV %)",ce:"ce_iv",pe:"pe_iv",nd:2,note:"Option-implied volatility per strike (the volatility smile)."},
  {k:"ltp",lbl:"Last Price (LTP ₹)",ce:"ce_ltp",pe:"pe_ltp",nd:2,note:"Option premium per strike."},
  {k:"pcr",lbl:"PCR at strike (PE OI ÷ CE OI)",single:true,note:"Put/Call OI ratio at each strike. >1 (green) = put-heavy / support; <1 (red) = call-heavy / resistance."},
  {k:"buildup",lbl:"OI Buildup signal",buildup:true,note:"Price move + OI move → Long Buildup (bullish), Short Buildup (bearish), Short Covering (bullish), Long Unwinding (bearish)."},
  {k:"vcp",lbl:"Intraday per-strike scan: VCP · VWAP · EMA · SMC",vcp:true,note:"Per-strike intraday scan of <b>each option's own chart</b> — pick a timeframe (1m/3m/5m/15m/1h) and a lens. <b>Momentum</b>: VCP (tightening legs→pivot→breakout), VWAP position, EMA 10/20 crossover. <b>SMC</b>: market structure, premium/discount, supply/demand zones, liquidity sweeps + trendline liquidity. Today's session only; VWAP price-anchored (no volume in feed); higher TFs may have too few bars."},
  {k:"vprofile",lbl:"Volume Profile — POC / Value Area + entry-SL plan (per strike)",vprofile:true,note:"Per-strike <b>Volume Profile</b> from the intraday session — <b>POC</b> (point of control) + <b>Value Area</b> (VAH/VAL). Gives a long-the-option plan: <b>entry</b> at value, <b>SL</b> below value, <b>target</b> VAH/extension, with R:R. <i>Intraday feed has no exchange volume, so the profile is tick/time-weighted (a TPO-style proxy).</i>"}
 ];
 const sel=$("#oc_ind");
 IND.forEach(i=>{const o=document.createElement("option");o.value=i.k;o.textContent=i.lbl;sel.appendChild(o)});
 const fmtv=(v,nd)=>v==null?'—':Number(v).toLocaleString('en-IN',{maximumFractionDigits:nd,minimumFractionDigits:nd});
 const bar=(w,color)=>`<div style="height:14px;width:${w}%;background:${color};border-radius:3px;min-width:2px"></div>`;
 const strikeCell=r=>`<div style="width:96px;text-align:center;font-weight:700;color:${r.atm?'var(--green)':'var(--txt)'}">${r.strike}${r.atm?' ◄':''}</div>`;
 function buildupTag(cp,co){if(co==null||cp==null)return['—','var(--mut)'];if(co>0&&cp>0)return['Long Buildup','var(--green)'];if(co>0&&cp<0)return['Short Buildup','var(--red)'];if(co<0&&cp>0)return['Short Covering','var(--green)'];if(co<0&&cp<0)return['Long Unwinding','var(--red)'];return['Neutral','var(--mut)']}
 function hdr(l,c,r){const d=el("div");d.style.cssText="display:flex;align-items:center;gap:8px;margin:6px 0 2px;font-size:11px;text-transform:uppercase;letter-spacing:.4px;color:var(--mut)";d.innerHTML=`<div style="flex:1;text-align:right">${l}</div><div style="width:96px;text-align:center">${c}</div><div style="flex:1">${r}</div>`;return d}
 function mkRow(html){const row=el("div");row.style.cssText="display:flex;align-items:center;gap:8px;margin:3px 0;font-size:12.5px";row.innerHTML=html;return row}
 function vcpCell(r){
  if(!r) return '<span class="muted">—</span>';
  if(r.status==="insufficient data") return `<span class="muted">insuf ${r.bars}b</span>`;
  const col={"Breakout":"var(--green)","At pivot":"var(--cyan)","VCP forming":"var(--cyan)","Contracting":"var(--amber)","No VCP":"var(--mut)"}[r.status]||"var(--mut)";
  return `<span style="color:${col};font-weight:600">${r.status}</span>${r.legs?` <small class="muted">${r.legs}L${r.tightening?'✓':''}</small>`:''}`;
 }
 function vwapCell(r){ if(!r||!r.vwap_pos||r.vwap_pos==="—") return '<span class="muted">—</span>'; return r.vwap_pos==="above"?'<span style="color:var(--green)">▲ above</span>':'<span style="color:var(--red)">▼ below</span>'; }
 function emaCell(r){ if(!r||!r.ema_sig||r.ema_sig==="—") return '<span class="muted">—</span>'; if(r.ema_sig==="bull") return `<span style="color:var(--green)">10&gt;20${r.ema_cross==="golden"?' ⤴':''}</span>`; return `<span style="color:var(--red)">10&lt;20${r.ema_cross==="death"?' ⤵':''}</span>`; }
 function smcCell(r){
  if(!r) return '<span class="muted">—</span>';
  const t=[];
  const sc={bull:'var(--green)',bear:'var(--red)',range:'var(--mut)'}[r.smc_struct];
  if(sc) t.push(`<span style="color:${sc}">${r.smc_struct}</span>`);
  if(r.smc_zone&&r.smc_zone!=="—"){const zc=r.smc_zone==="Discount"?'var(--green)':r.smc_zone==="Premium"?'var(--red)':'var(--mut)';t.push(`<span style="color:${zc}">${r.smc_zone}</span>`);}
  if(r.smc_sd&&r.smc_sd!=="—"){const dc=/demand/.test(r.smc_sd)?'var(--green)':'var(--red)';t.push(`<span style="color:${dc}">${r.smc_sd}</span>`);}
  if(r.smc_liq&&r.smc_liq!=="—"){const lc=/bullish|sell-side/.test(r.smc_liq)?'var(--green)':/bearish|buy-side/.test(r.smc_liq)?'var(--red)':'var(--mut)';t.push(`<span style="color:${lc}">${r.smc_liq}</span>`);}
  if(r.smc_trend&&r.smc_trend!=="—") t.push(`<span style="color:var(--amber)">${r.smc_trend}</span>`);
  return t.length?t.join(' <span class="muted">·</span> '):'<span class="muted">—</span>';
 }
 function renderVCP(host){
  const V=DATA.fno_vcp||[];
  if(!V.length){host.innerHTML='<div class="muted">Intraday scan unavailable — run <code>py 30_fno_vcp.py</code> (fetches each strike\'s intraday chart from NSE).</div>';return;}
  const TFS=["1m","3m","5m","15m","1h"]; let curTf="5m", lens="mom";
  host.innerHTML='<div class="toolbar" style="margin:2px 0 10px"><span class="muted">Timeframe:</span><span id="vcp_tfs"></span><span class="muted" style="margin-left:14px">Lens:</span><span id="vcp_lens"></span></div><div id="vcp_body"></div>';
  const tfWrap=host.querySelector("#vcp_tfs"), lensWrap=host.querySelector("#vcp_lens"), body=host.querySelector("#vcp_body");
  const tbtn=(wrap,label,active,fn)=>{const b=el("button");b.textContent=label;b.style.cssText=`background:var(--bg2);border:1px solid ${active?'var(--accent)':'var(--line)'};color:var(--txt);padding:5px 12px;margin-right:6px;border-radius:8px;font-size:12.5px;cursor:pointer`;b.onclick=fn;wrap.appendChild(b)};
  function draw(){
   tfWrap.innerHTML=""; TFS.forEach(tf=>tbtn(tfWrap,tf,tf===curTf,()=>{curTf=tf;draw()}));
   lensWrap.innerHTML=""; [["mom","Momentum"],["smc","SMC"]].forEach(([k,l])=>tbtn(lensWrap,l,lens===k,()=>{lens=k;draw()}));
   body.innerHTML="";
   [...new Set(V.map(r=>r.expiry))].forEach(exp=>{
    const rows=V.filter(r=>r.expiry===exp&&r.tf===curTf); if(!rows.length)return;
    const atm=((DATA.oc_meta||[]).find(m=>m.expiry===exp)||{}).atm;
    const strikes=[...new Set(rows.map(r=>r.strike))].sort((a,b)=>a-b);
    const sk=k=>`<td class="l"><b style="color:${k===atm?'var(--green)':'var(--cyan)'}">${k}${k===atm?' ◄':''}</b></td>`;
    let h=`<div class="sech" style="margin:10px 0 2px">🗓️ ${exp} <span class="muted" style="font-weight:500">· intraday @ ${curTf}</span></div><div class="tablewrap"><table>`;
    if(lens==="mom"){
     h+='<thead><tr><th class="l">Strike</th><th class="l">Call VCP</th><th class="l">VWAP</th><th class="l">EMA10/20</th><th class="l">Put VCP</th><th class="l">VWAP</th><th class="l">EMA10/20</th></tr></thead><tbody>';
     strikes.forEach(k=>{const ce=rows.find(r=>r.strike===k&&r.side==="CE"),pe=rows.find(r=>r.strike===k&&r.side==="PE");
      h+=`<tr>${sk(k)}<td class="l">${vcpCell(ce)}</td><td class="l">${vwapCell(ce)}</td><td class="l">${emaCell(ce)}</td><td class="l">${vcpCell(pe)}</td><td class="l">${vwapCell(pe)}</td><td class="l">${emaCell(pe)}</td></tr>`;});
    } else {
     h+='<thead><tr><th class="l">Strike</th><th class="l">Call SMC — structure · P/D · supply-demand · liquidity · trendline</th><th class="l">Put SMC</th></tr></thead><tbody>';
     strikes.forEach(k=>{const ce=rows.find(r=>r.strike===k&&r.side==="CE"),pe=rows.find(r=>r.strike===k&&r.side==="PE");
      h+=`<tr>${sk(k)}<td class="l">${smcCell(ce)}</td><td class="l">${smcCell(pe)}</td></tr>`;});
    }
    h+='</tbody></table></div>';
    const box=el("div"); box.style.marginBottom="16px"; box.innerHTML=h; body.appendChild(box);
   });
  }
  draw();
 }
 function renderVProfile(host){
  const VP=DATA.fno_vprofile||[];
  if(!VP.length){host.innerHTML='<div class="muted">Volume-profile plan unavailable — run <code>py 30_fno_vcp.py</code>.</div>';return;}
  const nv=(v)=>v==null?'—':Number(v).toLocaleString('en-IN',{maximumFractionDigits:2,minimumFractionDigits:2});
  let out="";
  [...new Set(VP.map(r=>r.expiry))].forEach(exp=>{
   const rows=VP.filter(r=>r.expiry===exp); if(!rows.length)return;
   const atm=((DATA.oc_meta||[]).find(m=>m.expiry===exp)||{}).atm;
   let h=`<div class="sech" style="margin:10px 0 2px">🗓️ ${exp} <span class="muted" style="font-weight:500">· session volume profile</span></div><div class="tablewrap"><table><thead><tr><th class="l">Strike</th><th class="l">Side</th><th>POC</th><th>VAH</th><th>VAL</th><th>LTP</th><th class="l">Setup</th><th>Entry</th><th>SL</th><th>Target</th><th>R:R</th></tr></thead><tbody>`;
   rows.slice().sort((a,b)=>a.strike-b.strike||(a.side<b.side?-1:1)).forEach(r=>{
    const bc=/avoid|below/i.test(r.vp_bias)?'var(--mut)':/momentum/i.test(r.vp_bias)?'var(--green)':'var(--cyan)';
    const rrc=r.vp_rr==null?'var(--mut)':r.vp_rr>=2?'var(--green)':r.vp_rr>=1?'var(--amber)':'var(--red)';
    h+=`<tr><td class="l"><b style="color:${r.strike===atm?'var(--green)':'var(--cyan)'}">${r.strike}${r.strike===atm?' ◄':''}</b></td><td class="l">${r.side}</td><td>${nv(r.poc)}</td><td>${nv(r.vah)}</td><td>${nv(r.val)}</td><td>${nv(r.last)}</td><td class="l" style="color:${bc}">${r.vp_bias}</td><td>${nv(r.vp_entry)}</td><td style="color:var(--red)">${nv(r.vp_sl)}</td><td style="color:var(--green)">${nv(r.vp_target)}</td><td style="color:${rrc};font-weight:700">${r.vp_rr==null?'—':r.vp_rr}</td></tr>`;
   });
   h+='</tbody></table></div>';
   out+=`<div style="margin-bottom:16px">${h}</div>`;
  });
  host.innerHTML=out;
 }
 function renderAnalysis(){
  const cfg=IND.find(x=>x.k===sel.value)||IND[0];
  $("#oc_ind_note").innerHTML=cfg.note;
  const wrapAll=$("#oc_analysis"); wrapAll.innerHTML="";
  if(cfg.vcp){ renderVCP(wrapAll); return; }
  if(cfg.vprofile){ renderVProfile(wrapAll); return; }
  MS.forEach(M=>{
   const rows=OC.filter(r=>r.expiry===M.expiry).slice().sort((a,b)=>a.strike-b.strike);
   const box=el("div"); box.style.cssText="margin-bottom:16px";
   box.innerHTML=`<div class="sech" style="margin:8px 0 2px">🗓️ ${M.expiry} <span class="muted" style="font-weight:500">· ATM ${M.atm} · DTE ${M.dte}</span></div>`;
   if(cfg.single){
     box.appendChild(hdr("","STRIKE","PE OI ÷ CE OI"));
     const vals=rows.map(r=>r.ce_oi?r.pe_oi/r.ce_oi:null); const mx=Math.max(1,...vals.filter(v=>v!=null));
     rows.forEach((r,i)=>{const v=vals[i],w=(v||0)/mx*100,col=v==null?'var(--mut)':(v>=1?'var(--green)':'var(--red)');
       box.appendChild(mkRow(`<div style="flex:1"></div>${strikeCell(r)}<div style="flex:1;display:flex;align-items:center;gap:6px">${bar(w,col)}<span style="color:${col};font-weight:700">${v==null?'—':v.toFixed(2)}</span></div>`))});
   } else if(cfg.buildup){
     box.appendChild(hdr("CALL","STRIKE","PUT"));
     rows.forEach(r=>{const[ct,cc]=buildupTag(r.ce_chg,r.ce_chg_oi),[pt,pc]=buildupTag(r.pe_chg,r.pe_chg_oi);
       box.appendChild(mkRow(`<div style="flex:1;text-align:right;color:${cc};font-weight:600">${ct}</div>${strikeCell(r)}<div style="flex:1;color:${pc};font-weight:600">${pt}</div>`))});
   } else {
     box.appendChild(hdr("CALL","STRIKE","PUT"));
     const cev=rows.map(r=>Math.abs(r[cfg.ce]||0)),pev=rows.map(r=>Math.abs(r[cfg.pe]||0)),mx=Math.max(1,...cev,...pev);
     rows.forEach(r=>{const cv=r[cfg.ce],pv=r[cfg.pe],cw=Math.abs(cv||0)/mx*100,pw=Math.abs(pv||0)/mx*100;
       const cbg=cfg.signed&&cv<0?'var(--red)':'var(--cyan)',pbg=cfg.signed&&pv<0?'var(--red)':'var(--violet)';
       box.appendChild(mkRow(`<div style="flex:1;display:flex;align-items:center;justify-content:flex-end;gap:6px"><span style="color:var(--mut)">${fmtv(cv,cfg.nd)}</span>${bar(cw,cbg)}</div>${strikeCell(r)}<div style="flex:1;display:flex;align-items:center;gap:6px">${bar(pw,pbg)}<span style="color:var(--mut)">${fmtv(pv,cfg.nd)}</span></div>`))});
   }
   wrapAll.appendChild(box);
  });
 }
 sel.onchange=renderAnalysis; renderAnalysis();
})();

// ---- search wiring ----
function wire(inp,tbl){$(inp).addEventListener("input",e=>{const q=e.target.value.toLowerCase();const f=tbl._data.filter(r=>Object.values(r).some(v=>v!=null&&(""+v).toLowerCase().includes(q)));tbl._render(f)})}
wire("#s_wl",$("#t_wl")); wire("#s_m",$("#t_m")); if(SW.length)wire("#s_sw",$("#t_sw")); if(IZ.length)wire("#s_iz",$("#t_iz"));

// ---- detail modal ----
function row(k,v){return `<div class="i"><div class="kk">${k}</div><div class="vv">${v==null||v===""?'—':v}</div></div>`}
function showDetail(r,isWl){
 const s=$("#sheet");
 const title=`${r.symbol} — ${r.name||''}`;
 let h=`<span class="x" onclick="document.getElementById('modal').classList.remove('open')">&times;</span><h2>${title}</h2>`;
 h+=`<div class="muted">${r.exchange||''} ${r.sector?'· '+r.sector:''} ${r.cap_bucket?'· '+r.cap_bucket+' cap':''} ${r.tier?'· ':''}${r.tier?tierPill(r.tier):''}</div>`;
 if(isWl){
   h+='<div class="sech">Phase 7 — Trade plan</div><div class="kv">';
   const liveTxt=r.live==null?'—':`${r.live}${r.live_chg==null?'':' ('+(r.live_chg>0?'+':'')+r.live_chg+'%)'} `+(r.live_state=='above'?'▲ above entry':r.live_state=='stop'?'▼ below stop':'+'+r.live_to_entry+'% to entry');
   const valTxt=r.verdict&&r.verdict!='NO DATA'?`${r.verdict} — ${r.vreason} (${r.vpassed}/6: vol ${r.vol_x}×, ext ${r.ext_pct}%, ₹${r.adv_cr}cr/d, RS ${r.rs>0?'+':''}${r.rs}%)`:'—';
   const stgTxt=r.stage=='MOVING'?`MOVING — ${r.stage_pct}% of move done, +${r.upside_tgt}% left to target`:r.stage=='EARLY'?`EARLY (coiled) — needs +${r.stage_pct}% to trigger, +${r.upside_tgt}% to target`:r.stage=='FAILED'?'FAILED — below stop':'—';
   h+=row("Stage",stgTxt)+row("Validation (Layer-1)",valTxt)+row("Scan-time close",r.close)+row("Live price",liveTxt)+row("VCP stage",r.vcp_status)+row("Entry (pivot)",r.pivot_entry)+row("Stop (1.8×ATR)",r.stop)+row("Stop %",r.stop_pct+"%")+row("Gann T1",r.gann_T1)+row("Target",r.target2)+row("Risk:Reward",r.rr)+row("Qty / ₹10L (1% risk)",r.qty_per_10L)+row("RSI",r.rsi)+row("ADX",r.adx)+row("Vol spike",r.vol_spike+"×")+row("SMC zone",r.pd_zone)+row("Gann > 1×1",r.gann_above_1x1)+row("Confluence score",r.phase7_score)+"</div>";
   h+=`<div class="sech">Recent candles</div><div class="muted">${r.last_candles||'—'}</div>`;
 } else {
   h+='<div class="sech">Phase 1 — Performance</div><div class="kv">';
   h+=row("6-month return", (r.return_pct_final>0?'+':'')+r.return_pct_final+"%")+row("Price 180d ago",r.price_180d_ago)+row("Price now",r.price_today)+row("Avg daily vol",r.avg_daily_volume)+"</div>";
   h+='<div class="sech">Phase 2 — Technicals</div><div class="kv">';
   h+=row("Scorecard",r.scorecard)+row("RSI",r.rsi)+row("ADX",r.adx)+row("MACD",r.macd_pos)+row("EMA align",r.ema_alignment)+row("Supertrend",r.supertrend)+row("Candle bias",r.candle_bias)+row("Trend structure",r.trend_structure)+"</div>";
   h+='<div class="sech">Phase 3 — Smart Money</div><div class="kv">';
   h+=row("Premium/Discount",r.pd_zone)+row("Range position",r.range_pos_pct+"%")+row("Weekly structure",r.structure_W)+row("Last BoS",r.last_BoS)+row("Bullish OB",r.bull_OB)+row("Unfilled bull FVGs",r.unfilled_bull_FVG)+row("Liquidity swept",r.liquidity_swept)+"</div>";
   h+='<div class="sech">Phase 4 — VCP + Gann</div><div class="kv">';
   h+=row("VCP quality",r.vcp_quality)+row("VCP status",r.vcp_status)+row("Contractions",r.contractions)+row("Pivot",r.pivot)+row("% from pivot",r.pct_from_pivot+"%")+row("Gann trend",r.gann_gann_trend)+row("Octave",r.octave)+row("Gann T1",r["sq9_T1_+0.25"])+row("Gann T2",r["sq9_T2_+0.5"])+"</div>";
   h+='<div class="sech">Phase 6 — Confluence score</div><div class="kv">';
   h+=row("Indicators /40",r.ind_score_40)+row("Structure /25",r.struct_score_25)+row("VCP /20",r.vcp_score_20)+row("Gann /15",r.gann_score_15)+row("TOTAL /100",r.TOTAL_100)+"</div>";
 }
 s.innerHTML=h; $("#modal").classList.add("open");
}
$("#modal").onclick=e=>{if(e.target.id=="modal")$("#modal").classList.remove("open")};
</script></body></html>"""

out = HTML.replace("__DATA__", json.dumps(DATA, separators=(",",":")))
# Inject the deployed backend base URL (Render) at build time. Defaults to the
# live Render web service so the deployed "Add alert" button works without setting
# any env var; override with ALPHAFINDER_BACKEND_URL if the service is renamed.
_DEFAULT_BACKEND = "https://alphafinder-mrye.onrender.com"
out = out.replace("__ALPHA_BACKEND__", os.environ.get("ALPHAFINDER_BACKEND_URL", _DEFAULT_BACKEND).rstrip("/"))
open("alphafinder_dashboard.html","w",encoding="utf-8").write(out)
print(f"Wrote alphafinder_dashboard.html ({len(out)//1024} KB) | master={len(DATA['master'])} watchlist={len(DATA['watchlist'])} fingerprint={len(DATA['fingerprint'])}")
