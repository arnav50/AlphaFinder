"""
Leading-indicator + volume + ATR deep dive for the Phase-1 universe — WEEKLY + DAILY.
Reads FINAL_universe_25pct.csv (Phase-1 list) + ohlc.pkl (daily OHLCV).

'Start of the move' = base low = the lowest-close bar within the trailing ~180 trading days.
Initial RSI / ADX / ATR are read at that bar (documented, reproducible proxy for Day-0).

Computes per stock (daily; weekly mirror where noted):
  RSI(14)            : current, initial (at move start), >50-at-start?, bullish base divergence, RSI-HH-with-price
  Stochastic RSI(14,3,3): current %K/%D + cross; crossing-up-from-oversold near move start
  ADX(14)            : current, +DI vs -DI, ADX at move start
  Volume             : OBV trend, volume>20d-avg-on-up-days, CMF(20) sign, price vs (rolling) VWAP
  ATR(14)            : current (for stops), ATR at move start (expansion signal)
  Leading Score (1-10) via a transparent additive rubric.

Outputs: LEADING_ANALYSIS.csv (full detail) + LEADING_SCORECARD.csv (requested 6-col table)
"""
import pickle, numpy as np, pandas as pd
import ta_lib_local as T

def stochrsi(close, n=14, k=3, d=3):
    r = T.rsi(close, n)
    ll = r.rolling(n).min(); hh = r.rolling(n).max()
    sr = 100 * (r - ll) / (hh - ll).replace(0, np.nan)
    K = sr.rolling(k).mean(); D = K.rolling(d).mean()
    return K, D

def cmf(h, l, c, v, n=20):
    # zero-range bars (upper/lower circuit: high==low) -> money-flow multiplier = 0, not NaN
    mfm = (((c - l) - (h - c)) / (h - l).replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0)
    mfv = mfm * v
    return mfv.rolling(n, min_periods=10).sum() / v.rolling(n, min_periods=10).sum().replace(0, np.nan)

def weekly(df):
    return (df.set_index("date").resample("W")
              .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
              .dropna().reset_index())

def reg_div(price, ind, kind="bull", w=3, recent=60):
    p = price.tail(recent).reset_index(drop=True); q = ind.tail(recent).reset_index(drop=True)
    hi, lo = T.swings(p, w)
    pts = lo if kind == "bull" else hi
    if len(pts) < 2: return False
    a, b = pts[-2], pts[-1]
    return (p[b] < p[a] and q[b] > q[a]) if kind == "bull" else (p[b] > p[a] and q[b] < q[a])

def rsi_hh_with_price(c, rsi, w=3, recent=80):
    p = c.tail(recent).reset_index(drop=True); q = rsi.tail(recent).reset_index(drop=True)
    hi, _ = T.swings(p, w)
    if len(hi) < 2: return False
    a, b = hi[-2], hi[-1]
    return bool(p[b] > p[a] and q[b] > q[a])

def analyze(sym, df):
    df = df.reset_index(drop=True)
    o, h, l, c, v = df["open"], df["high"], df["low"], df["close"], df["volume"]
    px = float(c.iloc[-1]); n = len(df)
    R = {"symbol": sym, "CMP": round(px, 2), "bars_daily": n}

    rsi = T.rsi(c); adxv, pdi, mdi = T.adx(h, l, c); atr = T.atr(h, l, c)
    K, D = stochrsi(c); ob = T.obv(c, v); cm = cmf(h, l, c, v)
    vw = T.vwap_rolling(h, l, c, v)

    # ----- move start = base low (lowest close in trailing ~180 trading days) -----
    W = min(n, 180)
    start_pos = int(c.tail(W).idxmin())
    R["move_start_date"] = df["date"].iloc[start_pos].date().isoformat()

    # ----- RSI -----
    R["rsi"] = round(rsi.iloc[-1], 1)
    R["rsi_state"] = "overbought" if rsi.iloc[-1] > 70 else "oversold" if rsi.iloc[-1] < 30 else "neutral"
    R["rsi_initial"] = round(float(rsi.iloc[start_pos]), 1) if pd.notna(rsi.iloc[start_pos]) else np.nan
    R["rsi_above50_at_start"] = bool(pd.notna(rsi.iloc[start_pos]) and rsi.iloc[start_pos] >= 50)
    R["rsi_bull_div_base"] = bool(reg_div(c, rsi, "bull"))
    R["rsi_hh_with_price"] = rsi_hh_with_price(c, rsi)

    # ----- Stochastic RSI -----
    R["stochrsi_k"] = round(float(K.iloc[-1]), 1) if pd.notna(K.iloc[-1]) else np.nan
    R["stochrsi_d"] = round(float(D.iloc[-1]), 1) if pd.notna(D.iloc[-1]) else np.nan
    R["stochrsi_cross"] = T.last_cross(K, D, 3) or "none"
    R["stochrsi_state"] = ("overbought" if pd.notna(K.iloc[-1]) and K.iloc[-1] > 80
                           else "oversold" if pd.notna(K.iloc[-1]) and K.iloc[-1] < 20 else "neutral")
    # crossing up from oversold within +/-5 bars of move start
    lo_w = slice(max(0, start_pos - 2), min(n, start_pos + 6))
    seg_k, seg_d = K.iloc[lo_w], D.iloc[lo_w]
    cross_up_start = False
    if len(seg_k) >= 2:
        diff = (seg_k - seg_d)
        for i in range(1, len(diff)):
            if pd.notna(diff.iloc[i]) and pd.notna(diff.iloc[i-1]) and diff.iloc[i] > 0 >= diff.iloc[i-1] \
               and pd.notna(seg_k.iloc[i-1]) and seg_k.iloc[i-1] < 30:
                cross_up_start = True; break
    R["stochrsi_crossup_from_os_at_start"] = cross_up_start

    # ----- ADX -----
    R["adx"] = round(float(adxv.iloc[-1]), 1) if pd.notna(adxv.iloc[-1]) else np.nan
    R["adx_strength"] = ("very_strong" if adxv.iloc[-1] > 40 else "strong" if adxv.iloc[-1] > 25
                         else "weak") if pd.notna(adxv.iloc[-1]) else "n/a"
    R["di"] = "+DI>-DI" if pdi.iloc[-1] > mdi.iloc[-1] else "-DI>+DI"
    R["adx_initial"] = round(float(adxv.iloc[start_pos]), 1) if pd.notna(adxv.iloc[start_pos]) else np.nan

    # ----- Volume -----
    def trend10(s):
        x = s.dropna().tail(10)
        if len(x) < 4: return "n/a"
        sl = np.polyfit(range(len(x)), x.values, 1)[0]
        rng = x.max() - x.min()
        if rng == 0 or abs(sl) * len(x) < 0.15 * rng: return "flat"
        return "rising" if sl > 0 else "falling"
    R["obv_trend"] = trend10(ob)
    vol20 = v.rolling(20).mean()
    last = df.tail(20)
    up_mask = last["close"].diff() > 0
    up_vol_hi = (last["volume"][up_mask] > vol20.tail(20)[up_mask]).mean() if up_mask.any() else np.nan
    R["vol_gt20avg_on_updays"] = ("yes" if pd.notna(up_vol_hi) and up_vol_hi >= 0.5
                                  else "no" if pd.notna(up_vol_hi) else "n/a")
    R["cmf"] = round(float(cm.iloc[-1]), 3) if pd.notna(cm.iloc[-1]) else np.nan
    R["cmf_sign"] = ("positive" if pd.notna(cm.iloc[-1]) and cm.iloc[-1] > 0
                     else "negative" if pd.notna(cm.iloc[-1]) else "n/a")
    R["vwap20"] = round(float(vw.iloc[-1]), 2) if pd.notna(vw.iloc[-1]) else np.nan
    R["px_vs_vwap"] = "above" if pd.notna(vw.iloc[-1]) and px > vw.iloc[-1] else "below" if pd.notna(vw.iloc[-1]) else "n/a"

    # ----- ATR -----
    R["atr"] = round(float(atr.iloc[-1]), 2) if pd.notna(atr.iloc[-1]) else np.nan
    R["atr_pct"] = round(float(atr.iloc[-1]) / px * 100, 2) if pd.notna(atr.iloc[-1]) else np.nan
    R["atr_initial"] = round(float(atr.iloc[start_pos]), 2) if pd.notna(atr.iloc[start_pos]) else np.nan
    R["atr_expansion_x"] = (round(float(atr.iloc[-1]) / float(atr.iloc[start_pos]), 2)
                            if pd.notna(atr.iloc[start_pos]) and atr.iloc[start_pos] else np.nan)

    # ----- weekly RSI / ADX mirror -----
    wk = weekly(df); R["weekly_bars"] = len(wk)
    if len(wk) >= 20:
        wr = T.rsi(wk["close"]).iloc[-1]
        R["wk_rsi"] = round(float(wr), 1) if pd.notna(wr) else np.nan
    else:
        R["wk_rsi"] = np.nan
    if len(wk) >= 30:
        wadx, wp, wm = T.adx(wk["high"], wk["low"], wk["close"])
        R["wk_adx"] = round(float(wadx.iloc[-1]), 1) if pd.notna(wadx.iloc[-1]) else np.nan
        R["wk_di"] = "+DI>-DI" if wp.iloc[-1] > wm.iloc[-1] else "-DI>+DI"
    else:
        R["wk_adx"] = np.nan; R["wk_di"] = "n/a"

    # ----- Leading Score (1-10) -----
    raw, mx = 0.0, 0.0
    def add(cond, w):
        nonlocal raw, mx; mx += w; raw += (w if cond else 0)
    add(rsi.iloc[-1] > 50, 1.0)
    add(50 <= rsi.iloc[-1] <= 70, 0.5)                         # healthy, not overbought
    add(R["rsi_above50_at_start"], 1.0)
    add(R["rsi_bull_div_base"], 1.0)
    add(R["rsi_hh_with_price"], 1.0)
    add(R["stochrsi_cross"] == "bull" and R["stochrsi_state"] != "overbought", 1.0)
    add(pd.notna(adxv.iloc[-1]) and adxv.iloc[-1] > 25 and R["di"] == "+DI>-DI", 1.5)
    add(pd.notna(adxv.iloc[-1]) and adxv.iloc[-1] > 40 and R["di"] == "+DI>-DI", 0.5)
    add(R["obv_trend"] == "rising", 1.0)
    add(R["vol_gt20avg_on_updays"] == "yes", 0.5)
    add(R["cmf_sign"] == "positive", 1.0)
    add(R["px_vs_vwap"] == "above", 0.5)
    R["leading_score_10"] = int(np.clip(round(raw / mx * 10), 1, 10)) if mx else 1
    return R

if __name__ == "__main__":
    fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
    meta = fin.set_index("symbol")[["name", "exchange"]].to_dict("index")
    data = pickle.load(open("ohlc.pkl", "rb"))
    rows = []
    for i, sym in enumerate(fin["symbol"], 1):
        df = data.get(sym)
        if df is None or len(df) < 40:
            rows.append({"symbol": sym, "note": "insufficient OHLC"}); continue
        try:
            r = analyze(sym, df)
            r["name"] = meta.get(sym, {}).get("name", ""); r["exchange"] = meta.get(sym, {}).get("exchange", "")
            rows.append(r)
        except Exception as e:
            rows.append({"symbol": sym, "note": f"{type(e).__name__}:{e}"})
        if i % 80 == 0: print(f"  {i}/{len(fin)}")

    out = pd.DataFrame(rows).sort_values("leading_score_10", ascending=False, na_position="last").reset_index(drop=True)
    full_cols = ["symbol", "name", "exchange", "CMP", "move_start_date",
                 "rsi", "rsi_state", "rsi_initial", "rsi_above50_at_start", "rsi_bull_div_base", "rsi_hh_with_price",
                 "stochrsi_k", "stochrsi_d", "stochrsi_cross", "stochrsi_state", "stochrsi_crossup_from_os_at_start",
                 "adx", "adx_strength", "di", "adx_initial",
                 "obv_trend", "vol_gt20avg_on_updays", "cmf", "cmf_sign", "vwap20", "px_vs_vwap",
                 "atr", "atr_pct", "atr_initial", "atr_expansion_x",
                 "wk_rsi", "wk_adx", "wk_di", "weekly_bars", "bars_daily", "leading_score_10"]
    full_cols = [c for c in full_cols if c in out.columns]
    out[full_cols].to_csv("LEADING_ANALYSIS.csv", index=False)

    summ = pd.DataFrame({
        "Stock": out["symbol"],
        "RSI": out["rsi"],
        "ADX": out["adx"],
        "OBV Trend": out["obv_trend"],
        "CMF": out["cmf_sign"],
        "ATR": out["atr"],
        "Leading Score (1-10)": out["leading_score_10"],
    })
    summ.to_csv("LEADING_SCORECARD.csv", index=False)

    nn = int(out["leading_score_10"].notna().sum())
    print(f"\nDONE. analysed {nn} stocks -> LEADING_ANALYSIS.csv + LEADING_SCORECARD.csv")
    print(f"RSI>50 at start: {int(out['rsi_above50_at_start'].sum())} | bull base div: {int(out['rsi_bull_div_base'].sum())} | "
          f"ADX>25 +DI lead: {int(((out['adx']>25)&(out['di']=='+DI>-DI')).sum())} | CMF+: {int((out['cmf_sign']=='positive').sum())}")
    print("\n=== TOP 20 (by leading score) ===")
    print(summ.head(20).to_string(index=False))
