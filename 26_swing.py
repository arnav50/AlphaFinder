"""Phase 7b — Short-term SWING trade plans for the Phase-7 watchlist.

Pure daily-bar swing screen (no intraday). For each of the 30 watchlist names this:
  • fetches ~1y of DAILY bars from Yahoo,
  • measures the daily picture — EMA20/50/200 trend stack, RSI(14), ATR(14),
    the 20-day breakout level and the recent swing low,
  • classifies the swing setup — BREAKOUT / PULLBACK / BASE / EXTENDED / WEAK,
  • builds a swing plan: entry (breakout pivot or EMA20 reclaim), stop (recent
    swing low or 2×ATR, whichever is tighter but valid), target = the daily
    structural swing target from the watchlist,
  • emits a GO / WATCH / AVOID verdict + R:R, size and an expected hold horizon.

Output: SWING_TRADES.csv  (consumed by 25_build_frontend.py → "Short Term Trade" tab)

Mechanical signals only — not investment advice. Swing horizon ~1-3 weeks.
"""
import time, datetime, requests, numpy as np, pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
CAPITAL_REF = 1_000_000      # ₹10L reference book (qty scales linearly with your capital)
RISK_PCT    = 0.01           # 1% risk per swing trade
RISK_RS     = CAPITAL_REF * RISK_PCT
ATR_N = RSI_N = 14
BREAKOUT_LOOKBACK = 20       # 20-day high defines the breakout pivot
SWINGLOW_LOOKBACK = 10       # recent swing low for the structural stop

def fetch_daily(ticker, session, suffixes=(".NS", ".BO")):
    """Return (DataFrame[close,high,low,volume], live, prev_close) of daily 1y bars."""
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

def analyze(row, df, live, prev):
    """Daily swing read blended with the watchlist's structural target."""
    d_entry = float(row["pivot_entry"]); d_stop = float(row["stop"]); tgt = float(row["target2"])
    e20, e50, e200 = ema(df["close"], 20), ema(df["close"], 50), ema(df["close"], 200)
    datr = atr(df); drsi = rsi(df["close"])
    bo_level = float(df["high"].iloc[-BREAKOUT_LOOKBACK:].max())
    swing_low = float(df["low"].iloc[-SWINGLOW_LOOKBACK:].min())
    dist20 = (live / e20 - 1) * 100
    uptrend = e20 > e50 and live > e50
    strong_up = uptrend and e50 > e200
    chg = round((live / prev - 1) * 100, 2) if prev else None

    # --- trend label ---
    if strong_up:   trend = "strong up"
    elif uptrend:   trend = "up"
    elif live > e200: trend = "neutral"
    else:           trend = "down"

    # --- setup classification (daily) ---
    near_bo = live >= bo_level * 0.99
    if not uptrend:
        setup = "WEAK"
    elif dist20 > 8:
        setup = "EXTENDED"
    elif near_bo:
        setup = "BREAKOUT"
    elif -3 <= dist20 <= 4 and 40 <= drsi <= 60:
        setup = "PULLBACK"
    else:
        setup = "BASE"

    # --- swing plan: entry timed off the setup, target = daily structural target ---
    if setup == "BREAKOUT":
        entry = round(max(bo_level, d_entry), 2)
        horizon = "1-3 weeks"
    elif setup == "PULLBACK":
        entry = round(max(live, e20), 2)              # reclaim of the 20-EMA
        horizon = "1-2 weeks"
    else:                                              # BASE / EXTENDED / WEAK → use the structural pivot
        entry = round(d_entry, 2)
        horizon = "2-4 weeks" if setup == "BASE" else "wait"
    # stop = tightest valid level below entry (recent swing low / 2×ATR / structural stop)
    cands = [swing_low, entry - 2 * datr, d_stop]
    below = [c for c in cands if c < entry]
    stop = round(max(below), 2) if below else round(d_stop, 2)
    risk = entry - stop
    rr = round((tgt - entry) / risk, 2) if risk > 0 else None
    qty = int(RISK_RS / risk) if risk > 0 else None
    stop_pct = round(risk / entry * 100, 2) if entry else None

    # --- verdict ---
    if setup == "WEAK":
        verdict, reason = "AVOID", "below 50-EMA — trend not supportive"
    elif setup == "EXTENDED":
        verdict, reason = "WATCH", "extended above 20-EMA — wait for a pullback"
    elif setup in ("BREAKOUT", "PULLBACK") and 45 <= drsi <= 72:
        verdict, reason = "GO", f"{setup.lower()} in an uptrend"
    else:
        verdict, reason = "WATCH", "basing — needs a trigger"
    return {
        "live": round(live, 2), "chg_pct": chg,
        "ema20": round(e20, 2), "ema50": round(e50, 2), "ema200": round(e200, 2),
        "trend": trend, "d_rsi": round(drsi, 1), "d_atr": round(datr, 2),
        "dist_ema20": round(dist20, 2), "bo_level": round(bo_level, 2),
        "setup": setup, "swing_entry": entry, "swing_stop": stop, "stop_pct": stop_pct,
        "swing_target": round(tgt, 2), "rr": rr, "qty_per_10L": qty,
        "horizon": horizon, "verdict": verdict, "reason": reason,
    }

def main():
    wl = pd.read_csv("PHASE7_WATCHLIST.csv", dtype={"symbol": str})
    sx = requests.Session(); sx.headers.update({"User-Agent": UA})
    rows = []
    for _, r in wl.iterrows():
        df, live, prev = fetch_daily(r["symbol"], sx)
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
    out["st_order"] = out["verdict"].map(order).fillna(3).astype(int)
    out = out.sort_values(["st_order", "rr"], ascending=[True, False]).reset_index(drop=True)
    out.to_csv("SWING_TRADES.csv", index=False)
    vc = out["verdict"].value_counts().to_dict()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"Wrote SWING_TRADES.csv | {len(out)} names @ {ts} | "
          + " ".join(f"{k}={v}" for k, v in vc.items()))

if __name__ == "__main__":
    main()
