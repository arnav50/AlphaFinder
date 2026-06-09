"""
Lagging-indicator deep dive for the Phase-1 universe — WEEKLY + DAILY.
Reads FINAL_universe_25pct.csv (the Phase-1 list) + ohlc.pkl (daily OHLCV).

Computes per stock:
  MOVING AVERAGES
    - Daily EMA 9, 21, 50, 100, 200 (+ price distance % from each)
    - Weekly SMA 50, 200 (200 = N/A unless >=200 weekly bars exist)
    - price_above_all_emas (Y/N)
    - perfect_bull_stack: EMA9>EMA21>EMA50>EMA100>EMA200 (Y/N)
  MACD (12,26,9) daily + weekly
    - line vs signal (above/below), histogram expanding/contracting, regular divergence
    - exact macd / signal / histogram values
  BOLLINGER (20,2) daily
    - walking upper band?, width expanding/squeezing, exact upper/mid/lower
  Overall Lagging Score (1-10) via a transparent additive rubric.

Outputs:
  LAGGING_ANALYSIS.csv   (full detail: every exact value)
  LAGGING_SCORECARD.csv  (the requested 5-col table)
"""
import pickle, numpy as np, pandas as pd
import ta_lib_local as T

def weekly(df):
    return (df.set_index("date").resample("W")
              .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
              .dropna().reset_index())

def reg_div(price, ind, kind, w=3, recent=60):
    """regular divergence over the last `recent` bars."""
    p = price.tail(recent).reset_index(drop=True); q = ind.tail(recent).reset_index(drop=True)
    hi, lo = T.swings(p, w)
    pts = lo if kind == "bull" else hi
    if len(pts) < 2: return False
    a, b = pts[-2], pts[-1]
    return (p[b] < p[a] and q[b] > q[a]) if kind == "bull" else (p[b] > p[a] and q[b] < q[a])

def dist(px, ema_val):
    return round((px / ema_val - 1) * 100, 2) if pd.notna(ema_val) and ema_val else np.nan

def analyze(sym, df):
    df = df.reset_index(drop=True)
    c, h, l, v = df["close"], df["high"], df["low"], df["volume"]
    px = float(c.iloc[-1])
    R = {"symbol": sym, "CMP": round(px, 2), "bars_daily": len(df)}

    # ---------------- MOVING AVERAGES (Daily EMAs) ----------------
    emas = {n: T.ema(c, n).iloc[-1] for n in (9, 21, 50, 100, 200)}
    for n in (9, 21, 50, 100, 200):
        R[f"ema{n}"] = round(emas[n], 2) if pd.notna(emas[n]) else np.nan
        R[f"dist_ema{n}_pct"] = dist(px, emas[n])
    valid = [emas[n] for n in (9, 21, 50, 100, 200) if pd.notna(emas[n])]
    R["price_above_all_emas"] = bool(len(valid) == 5 and all(px > e for e in valid))
    if all(pd.notna(emas[n]) for n in (9, 21, 50, 100, 200)):
        R["perfect_bull_stack"] = bool(emas[9] > emas[21] > emas[50] > emas[100] > emas[200])
    else:
        R["perfect_bull_stack"] = False
    # user's exact 9>21>50>200 (100 omitted) reported separately
    R["stack_9_21_50_200"] = bool(all(pd.notna(emas[n]) for n in (9, 21, 50, 200))
                                  and emas[9] > emas[21] > emas[50] > emas[200])

    # ---------------- Weekly SMA 50/200 ----------------
    wk = weekly(df); wc = wk["close"]
    R["weekly_bars"] = len(wk)
    sma50w = wc.rolling(50).mean().iloc[-1] if len(wk) >= 50 else np.nan
    sma200w = wc.rolling(200).mean().iloc[-1] if len(wk) >= 200 else np.nan
    R["wk_sma50"] = round(sma50w, 2) if pd.notna(sma50w) else "N/A"
    R["wk_sma200"] = round(sma200w, 2) if pd.notna(sma200w) else "N/A (need ~4y hist)"
    R["px_vs_wk_sma50"] = ("above" if pd.notna(sma50w) and px > sma50w
                           else "below" if pd.notna(sma50w) else "n/a")
    R["px_vs_wk_sma200"] = ("above" if pd.notna(sma200w) and px > sma200w
                            else "below" if pd.notna(sma200w) else "n/a")

    # ---------------- MACD (12,26,9) Daily ----------------
    ml, ms, hist = T.macd(c)
    R["macd"] = round(ml.iloc[-1], 3); R["macd_signal"] = round(ms.iloc[-1], 3)
    R["macd_hist"] = round(hist.iloc[-1], 3)
    R["macd_vs_signal"] = "above" if ml.iloc[-1] > ms.iloc[-1] else "below"
    hh = hist.tail(2).values
    pos = hh[-1] > 0
    R["macd_hist_state"] = (("expanding_pos" if hh[-1] > hh[-2] else "contracting_pos") if pos
                            else ("expanding_neg" if hh[-1] < hh[-2] else "contracting_neg"))
    R["macd_above_zero"] = bool(ml.iloc[-1] > 0)
    R["macd_div"] = ("bullish" if reg_div(c, ml, "bull") else
                     "bearish" if reg_div(c, ml, "bear") else "none")
    # weekly MACD position (bonus)
    if len(wk) >= 35:
        wml, wms, _ = T.macd(wc)
        R["wk_macd_vs_signal"] = "above" if wml.iloc[-1] > wms.iloc[-1] else "below"
    else:
        R["wk_macd_vs_signal"] = "n/a"

    # ---------------- BOLLINGER (20,2) Daily ----------------
    mid, ub, lb, bw = T.bollinger(c)
    um, mm, lm = ub.iloc[-1], mid.iloc[-1], lb.iloc[-1]
    R["bb_upper"] = round(um, 2) if pd.notna(um) else np.nan
    R["bb_mid"] = round(mm, 2) if pd.notna(mm) else np.nan
    R["bb_lower"] = round(lm, 2) if pd.notna(lm) else np.nan
    R["bb_width_pct"] = round(bw.iloc[-1], 2) if pd.notna(bw.iloc[-1]) else np.nan
    # walking upper band: >=3 of last 5 closes in the top 20% of the band
    if pd.notna(um):
        thresh = mm + 0.6 * (um - mm)                       # upper 40% line, conservative
        last5 = c.tail(5).values
        ups = sum(1 for x in last5 if x >= mm + 0.6 * (um - mm))
        walking = ups >= 3 and px >= 0.97 * um
        if walking: R["bb_position"] = "Walking Upper"
        elif px > um: R["bb_position"] = "Above Upper"
        elif px >= thresh: R["bb_position"] = "Upper Band"
        elif px >= mm: R["bb_position"] = "Upper Half"
        elif px >= lm: R["bb_position"] = "Lower Half"
        else: R["bb_position"] = "Below Lower"
    else:
        R["bb_position"] = "n/a"
    # width trend: now vs mean of prior 10 and 60
    if pd.notna(bw.iloc[-1]):
        w10 = bw.tail(11).head(10).mean(); w60 = bw.tail(63).mean()
        if bw.iloc[-1] > w10 and bw.iloc[-1] > w60: R["bb_width_state"] = "Expanding"
        elif bw.iloc[-1] < w60 * 0.85: R["bb_width_state"] = "Squeezing"
        else: R["bb_width_state"] = "Neutral"
    else:
        R["bb_width_state"] = "n/a"

    # ---------------- Overall Lagging Score (1-10) ----------------
    raw, mx = 0.0, 0.0
    def add(cond, w):
        nonlocal raw, mx; mx += w; raw += (w if cond else 0)
    add(R["price_above_all_emas"], 2.0)
    add(R["perfect_bull_stack"], 2.0)
    add(px > emas[200] if pd.notna(emas[200]) else False, 1.0)
    add(R["macd_vs_signal"] == "above", 1.5)
    add(R["macd_hist_state"] == "expanding_pos", 1.0)
    add(R["macd_above_zero"], 0.5)
    add(R["bb_position"] in ("Walking Upper", "Above Upper"), 1.0)
    add(R["bb_width_state"] == "Expanding" and px >= mm if pd.notna(mm) else False, 0.5)
    add(R["px_vs_wk_sma50"] == "above", 1.0)
    add(R["wk_macd_vs_signal"] == "above", 0.5)
    R["lagging_score_10"] = int(np.clip(round(raw / mx * 10), 1, 10)) if mx else 1
    return R

if __name__ == "__main__":
    fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
    meta = fin.set_index("symbol")[["name", "exchange"]].to_dict("index")
    data = pickle.load(open("ohlc.pkl", "rb"))
    rows = []
    for i, sym in enumerate(fin["symbol"], 1):
        df = data.get(sym)
        if df is None or len(df) < 30:
            rows.append({"symbol": sym, "note": "insufficient OHLC"}); continue
        try:
            r = analyze(sym, df)
            r["name"] = meta.get(sym, {}).get("name", "")
            r["exchange"] = meta.get(sym, {}).get("exchange", "")
            rows.append(r)
        except Exception as e:
            rows.append({"symbol": sym, "note": f"{type(e).__name__}:{e}"})
        if i % 80 == 0: print(f"  {i}/{len(fin)}")

    out = pd.DataFrame(rows)
    out = out.sort_values("lagging_score_10", ascending=False, na_position="last").reset_index(drop=True)
    full_cols = ["symbol", "name", "exchange", "CMP",
                 "ema9", "ema21", "ema50", "ema100", "ema200",
                 "dist_ema9_pct", "dist_ema21_pct", "dist_ema50_pct", "dist_ema100_pct", "dist_ema200_pct",
                 "price_above_all_emas", "perfect_bull_stack", "stack_9_21_50_200",
                 "wk_sma50", "wk_sma200", "px_vs_wk_sma50", "px_vs_wk_sma200",
                 "macd", "macd_signal", "macd_hist", "macd_vs_signal", "macd_hist_state",
                 "macd_above_zero", "macd_div", "wk_macd_vs_signal",
                 "bb_upper", "bb_mid", "bb_lower", "bb_width_pct", "bb_position", "bb_width_state",
                 "weekly_bars", "bars_daily", "lagging_score_10"]
    full_cols = [c for c in full_cols if c in out.columns]
    out[full_cols].to_csv("LAGGING_ANALYSIS.csv", index=False)

    # requested 5-col summary table
    def macd_status(r):
        if pd.isna(r.get("macd_vs_signal")): return "n/a"
        s = "MACD>Signal" if r["macd_vs_signal"] == "above" else "MACD<Signal"
        hs = {"expanding_pos": "Hist+ exp", "contracting_pos": "Hist+ contr",
              "expanding_neg": "Hist- exp", "contracting_neg": "Hist- contr"}.get(r.get("macd_hist_state"), "")
        return f"{s}, {hs}"
    summ = pd.DataFrame({
        "Stock": out["symbol"],
        "EMA Stack (Y/N)": out["perfect_bull_stack"].map({True: "Y", False: "N"}),
        "MACD Status": out.apply(macd_status, axis=1),
        "BB Position": out["bb_position"],
        "Overall Lagging Score (1-10)": out["lagging_score_10"],
    })
    summ.to_csv("LAGGING_SCORECARD.csv", index=False)

    n = out["lagging_score_10"].notna().sum()
    print(f"\nDONE. analysed {int(n)} stocks -> LAGGING_ANALYSIS.csv + LAGGING_SCORECARD.csv")
    print(f"price_above_all_emas: {int(out['price_above_all_emas'].sum())} | "
          f"perfect_bull_stack: {int(out['perfect_bull_stack'].sum())}")
    print(f"weekly SMA200 available: {int((out['wk_sma200'].astype(str).str.replace('.','',regex=False).str.replace('-','').str.isnumeric()).sum())}/{int(n)}")
    print("\n=== TOP 20 (by lagging score) ===")
    print(summ.head(20).to_string(index=False))
