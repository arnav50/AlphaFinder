"""Phase 7c — INTRADAY trade plans for the Phase-7 watchlist.

Same step-by-step method as 26_swing.py, but read on INTRADAY (15-minute) bars
instead of daily bars. For each of the 30 watchlist names this:
  • fetches ~1 month of 15-MINUTE bars from Yahoo (with timestamps),
  • measures the intraday picture — EMA9/20/50 trend stack, RSI(14), ATR(14) on
    15m bars, the session VWAP (volume-weighted, reset each day), the opening-range
    (first 30 min) high/low and the running day high/low,
  • classifies the intraday setup — ORB / MOMENTUM / VWAP_RECLAIM / PULLBACK /
    EXTENDED / WEAK,
  • builds an intraday plan: entry (opening-range break, VWAP reclaim or join),
    stop (tightest valid of session VWAP / day low / 1.5×ATR), target = 2R,
  • emits a GO / WATCH / AVOID verdict + R:R, size (0.5% risk) and same-session hold.

Output: INTRADAY_TRADES.csv  (consumed by 25_build_frontend.py → "Intraday" tab)

Mechanical signals only — not investment advice. Intraday horizon = same session.
"""
import time, datetime, requests, numpy as np, pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
CAPITAL_REF = 1_000_000      # ₹10L reference book (qty scales linearly with your capital)
RISK_PCT    = 0.005          # 0.5% risk per intraday trade (tighter than swing)
RISK_RS     = CAPITAL_REF * RISK_PCT
ATR_N = RSI_N = 14
OPENING_RANGE_BARS = 2       # first 2×15m bars = 30-min opening range
R_MULT = 2.0                 # intraday target = entry + 2R

def fetch_intraday(ticker, session, suffixes=(".NS", ".BO")):
    """Return (DataFrame[ts,close,high,low,volume], live, prev_close) of 15m bars (~1mo)."""
    for suf in suffixes:
        try:
            r = session.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}{suf}",
                            params={"range": "1mo", "interval": "15m"}, timeout=20)
            res = r.json()["chart"]["result"][0]; q = res["indicators"]["quote"][0]
            df = pd.DataFrame({"ts": res["timestamp"], "close": q["close"], "high": q["high"],
                               "low": q["low"], "volume": q["volume"]}).dropna().reset_index(drop=True)
            if len(df) > 50:
                meta = res["meta"]
                live = meta.get("regularMarketPrice") or float(df["close"].iloc[-1])
                prev = meta.get("previousClose") or meta.get("chartPreviousClose")
                return df, float(live), (float(prev) if prev else None)
        except Exception:
            pass
    return None, None, None

def ema(s, n): return float(s.ewm(span=n, adjust=False).mean().iloc[-1])

def rsi(close, n=RSI_N):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return float((100 - 100/(1+rs)).iloc[-1])

def atr(df, n=ATR_N):
    pc = df["close"].shift()
    tr = pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)
    return float(tr.ewm(alpha=1/n, adjust=False).mean().iloc[-1])

def session_slice(df):
    """Bars belonging to the most recent trading day (by the UTC date of each timestamp)."""
    days = pd.to_datetime(df["ts"], unit="s").dt.date
    last_day = days.iloc[-1]
    return df[days.values == last_day]

def vwap(sess):
    typ = (sess["high"] + sess["low"] + sess["close"]) / 3
    vol = sess["volume"]
    tot = float(vol.sum())
    return float((typ * vol).sum() / tot) if tot > 0 else float(sess["close"].iloc[-1])

def analyze(row, df, live, prev):
    """Intraday read on 15m bars blended with the watchlist's structural levels."""
    d_entry = float(row["pivot_entry"]); d_stop = float(row["stop"])
    e9, e20, e50 = ema(df["close"], 9), ema(df["close"], 20), ema(df["close"], 50)
    iatr = atr(df); irsi = rsi(df["close"])
    sess = session_slice(df)
    ivwap = vwap(sess)
    orb_high = float(sess["high"].iloc[:OPENING_RANGE_BARS].max())
    orb_low = float(sess["low"].iloc[:OPENING_RANGE_BARS].min())
    day_high = float(sess["high"].max()); day_low = float(sess["low"].min())
    dist_vwap = (live / ivwap - 1) * 100
    chg = round((live / prev - 1) * 100, 2) if prev else None

    above_vwap = live > ivwap
    ema_up = e9 > e20 and live > e20
    near_orb = live >= orb_high * 0.999

    # --- intraday trend label ---
    if above_vwap and e9 > e20 > e50: itrend = "strong up"
    elif above_vwap and ema_up:       itrend = "up"
    elif above_vwap:                  itrend = "neutral"
    else:                             itrend = "down"

    # --- setup classification (intraday, current session) ---
    if not above_vwap and live < e20:
        setup = "WEAK"
    elif dist_vwap > 4:
        setup = "EXTENDED"
    elif near_orb and above_vwap:
        setup = "ORB"
    elif above_vwap and -1.0 <= dist_vwap <= 1.0 and ema_up:
        setup = "VWAP_RECLAIM"
    elif above_vwap and ema_up:
        setup = "MOMENTUM"
    elif above_vwap:
        setup = "PULLBACK"
    else:
        setup = "WEAK"

    # --- intraday plan: entry timed off the setup, target = 2R ---
    if setup == "ORB":
        entry = round(max(orb_high, live), 2)
    elif setup == "MOMENTUM":
        entry = round(live, 2)                         # join the move
    elif setup in ("VWAP_RECLAIM", "PULLBACK"):
        entry = round(max(live, ivwap), 2)             # buy the VWAP reclaim
    else:                                              # EXTENDED / WEAK → wait for the ORB trigger
        entry = round(orb_high, 2)
    # stop = tightest valid level below entry (session VWAP / day low / 1.5×ATR / structural stop)
    cands = [ivwap, day_low, entry - 1.5 * iatr, d_stop]
    below = [c for c in cands if c < entry]
    stop = round(max(below), 2) if below else round(entry - 1.5 * iatr, 2)
    risk = entry - stop
    target = round(entry + R_MULT * risk, 2) if risk > 0 else None
    rr = round((target - entry) / risk, 2) if (risk > 0 and target) else None
    qty = int(RISK_RS / risk) if risk > 0 else None
    stop_pct = round(risk / entry * 100, 2) if entry else None

    # --- verdict ---
    if setup == "WEAK":
        verdict, reason = "AVOID", "below VWAP — intraday trend not supportive"
    elif setup == "EXTENDED":
        verdict, reason = "WATCH", "extended above VWAP — wait for a pullback"
    elif setup in ("ORB", "MOMENTUM", "VWAP_RECLAIM") and 45 <= irsi <= 78:
        verdict, reason = "GO", f"{setup.replace('_', ' ').lower()} above VWAP"
    elif setup == "PULLBACK":
        verdict, reason = "WATCH", "holding VWAP — needs a momentum trigger"
    else:
        verdict, reason = "WATCH", "above VWAP — await confirmation"
    return {
        "live": round(live, 2), "chg_pct": chg,
        "ivwap": round(ivwap, 2), "ema9": round(e9, 2), "ema20": round(e20, 2), "ema50": round(e50, 2),
        "itrend": itrend, "i_rsi": round(irsi, 1), "i_atr": round(iatr, 2),
        "dist_vwap": round(dist_vwap, 2), "orb_high": round(orb_high, 2), "orb_low": round(orb_low, 2),
        "day_high": round(day_high, 2), "day_low": round(day_low, 2),
        "setup": setup, "intraday_entry": entry, "intraday_stop": stop, "stop_pct": stop_pct,
        "intraday_target": target, "rr": rr, "qty_per_10L": qty,
        "horizon": "same session", "verdict": verdict, "reason": reason,
    }

def main():
    wl = pd.read_csv("PHASE7_WATCHLIST.csv", dtype={"symbol": str})
    sx = requests.Session(); sx.headers.update({"User-Agent": UA})
    rows = []
    for _, r in wl.iterrows():
        df, live, prev = fetch_intraday(r["symbol"], sx)
        base = {"rank": r["rank"], "symbol": r["symbol"], "name": r["name"],
                "sector": r.get("sector"), "close": r["close"], "tier": r["tier"],
                "vcp_status": r["vcp_status"], "phase7_score": r["phase7_score"]}
        if df is None:
            base["verdict"] = "NO DATA"
            rows.append(base)
        else:
            base.update(analyze(r, df, live, prev)); rows.append(base)
        time.sleep(0.2)
    out = pd.DataFrame(rows)
    order = {"GO": 0, "WATCH": 1, "AVOID": 2, "NO DATA": 3}
    out["it_order"] = out["verdict"].map(order).fillna(3).astype(int)
    out = out.sort_values(["it_order", "rr"], ascending=[True, False]).reset_index(drop=True)
    out.to_csv("INTRADAY_TRADES.csv", index=False)
    vc = out["verdict"].value_counts().to_dict()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"Wrote INTRADAY_TRADES.csv | {len(out)} names @ {ts} | "
          + " ".join(f"{k}={v}" for k, v in vc.items()))

if __name__ == "__main__":
    main()
