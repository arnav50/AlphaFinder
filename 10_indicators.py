"""Phase 2 Sections A & B: compute all leading + lagging indicators per stock.
Output: indicators.csv (one row per stock, values + categorical states)."""
import pickle, numpy as np, pandas as pd
import ta_lib_local as T

def regular_divergence(price, ind, kind, w=3, recent=60):
    """kind='bull' uses swing lows (price LL + ind HL); 'bear' uses swing highs."""
    p = price.tail(recent).reset_index(drop=True); q = ind.tail(recent).reset_index(drop=True)
    hi, lo = T.swings(p, w)
    pts = lo if kind == "bull" else hi
    if len(pts) < 2: return False
    a, b = pts[-2], pts[-1]
    if kind == "bull":   # price lower low, indicator higher low
        return p[b] < p[a] and q[b] > q[a]
    else:                # price higher high, indicator lower high
        return p[b] > p[a] and q[b] < q[a]

def trend10(s):
    x = s.dropna().tail(10)
    if len(x) < 4: return "n/a"
    sl = np.polyfit(range(len(x)), x.values, 1)[0]
    rng = x.max()-x.min()
    if rng == 0 or abs(sl)*len(x) < 0.15*rng: return "flat"
    return "rising" if sl > 0 else "falling"

def analyze(sym, df):
    o, h, l, c, v = df["open"], df["high"], df["low"], df["close"], df["volume"]
    n = len(df); px = float(c.iloc[-1]); R = {"symbol": sym, "bars": n, "close": round(px, 2)}

    # ---------- A1 RSI ----------
    rsi = T.rsi(c); rv = rsi.iloc[-1]
    R["rsi"] = round(rv, 1)
    R["rsi_state"] = "overbought" if rv > 70 else "oversold" if rv < 30 else "neutral"
    R["rsi_trend"] = trend10(rsi)
    R["rsi_div"] = ("bullish" if regular_divergence(c, rsi, "bull") else
                    "bearish" if regular_divergence(c, rsi, "bear") else "none")
    # ---------- A2 Stochastic ----------
    k, d = T.stoch(h, l, c)
    R["stoch_k"] = round(k.iloc[-1], 1); R["stoch_d"] = round(d.iloc[-1], 1)
    R["stoch_cross"] = T.last_cross(k, d, 3) or "none"
    R["stoch_state"] = "overbought" if k.iloc[-1] > 80 else "oversold" if k.iloc[-1] < 20 else "neutral"
    R["stoch_div"] = ("bullish" if regular_divergence(c, k, "bull") else
                      "bearish" if regular_divergence(c, k, "bear") else "none")
    # ---------- A3 Bollinger ----------
    mid, ub, lb, bw = T.bollinger(c)
    R["bb_pos"] = ("above_upper" if px > ub.iloc[-1] else "below_lower" if px < lb.iloc[-1]
                   else "above_mid" if px > mid.iloc[-1] else "below_mid")
    R["bb_width_pct"] = round(bw.iloc[-1], 2) if pd.notna(bw.iloc[-1]) else np.nan
    bw3 = bw.tail(63).mean()
    R["bb_squeeze"] = bool(pd.notna(bw.iloc[-1]) and pd.notna(bw3) and bw.iloc[-1] < bw3)
    R["bb_state"] = "expanding" if (pd.notna(bw.iloc[-1]) and bw.iloc[-1] > bw.tail(10).mean()) else "contracting"
    # ---------- A4 Ichimoku ----------
    if n >= 78:
        ten, kij, sA, sB, chi, fA, fB = T.ichimoku(h, l, c)
        top = max(sA.iloc[-1], sB.iloc[-1]); bot = min(sA.iloc[-1], sB.iloc[-1])
        R["ichi_price_cloud"] = "above" if px > top else "below" if px < bot else "inside"
        R["ichi_tk"] = "bullish" if ten.iloc[-1] > kij.iloc[-1] else "bearish"
        # chikou vs price 26 bars ago
        R["ichi_chikou"] = ("above" if c.iloc[-1] > c.iloc[-27] else "below") if n > 27 else "n/a"
        twist = T.last_cross(fA, fB, 26)  # future span cross ahead
        R["ichi_twist_ahead"] = twist or "none"
    else:
        R.update({"ichi_price_cloud": "n/a", "ichi_tk": "n/a", "ichi_chikou": "n/a", "ichi_twist_ahead": "n/a"})
    # ---------- A5 CCI ----------
    cci = T.cci(h, l, c); cv = cci.iloc[-1]
    R["cci"] = round(cv, 1) if pd.notna(cv) else np.nan
    R["cci_state"] = "strong_up" if cv > 100 else "strong_down" if cv < -100 else "above0" if cv > 0 else "below0"
    # ---------- A6 Williams %R ----------
    wr = T.williams_r(h, l, c).iloc[-1]
    R["williams_r"] = round(wr, 1) if pd.notna(wr) else np.nan
    R["wr_state"] = "overbought" if wr > -20 else "oversold" if wr < -80 else "neutral"
    # ---------- A7 OBV ----------
    ob = T.obv(c, v)
    R["obv_trend"] = trend10(ob)
    R["obv_div"] = ("bullish" if regular_divergence(c, ob, "bull") else
                    "bearish" if regular_divergence(c, ob, "bear") else "none")
    # ---------- A8 MFI ----------
    mf = T.mfi(h, l, c, v).iloc[-1]
    R["mfi"] = round(mf, 1) if pd.notna(mf) else np.nan
    R["mfi_state"] = "overbought" if mf > 80 else "oversold" if mf < 20 else "neutral"

    # ---------- B1 MACD ----------
    ml, ms, hist = T.macd(c)
    R["macd"] = round(ml.iloc[-1], 3); R["macd_signal"] = round(ms.iloc[-1], 3)
    R["macd_hist"] = round(hist.iloc[-1], 3)
    R["macd_pos"] = "above_signal" if ml.iloc[-1] > ms.iloc[-1] else "below_signal"
    h2 = hist.tail(2).values
    R["macd_hist_state"] = ("expanding_pos" if h2[-1] > 0 and h2[-1] > h2[-2] else
                            "contracting_pos" if h2[-1] > 0 else
                            "expanding_neg" if h2[-1] < h2[-2] else "contracting_neg")
    R["macd_cross"] = T.last_cross(ml, ms, 5) or "none"
    R["macd_zero"] = "above" if ml.iloc[-1] > 0 else "below"
    # ---------- B2 EMA alignment ----------
    e20, e50, e200 = T.ema(c, 20), T.ema(c, 50), T.ema(c, 200)
    R["ema20"] = round(e20.iloc[-1], 2) if pd.notna(e20.iloc[-1]) else np.nan
    R["ema50"] = round(e50.iloc[-1], 2) if pd.notna(e50.iloc[-1]) else np.nan
    R["ema200"] = round(e200.iloc[-1], 2) if pd.notna(e200.iloc[-1]) else np.nan
    if pd.notna(e200.iloc[-1]):
        R["ema_alignment"] = "bullish" if e20.iloc[-1] > e50.iloc[-1] > e200.iloc[-1] else \
                             "bearish" if e20.iloc[-1] < e50.iloc[-1] < e200.iloc[-1] else "mixed"
        sl = np.polyfit(range(20), e200.tail(20).values, 1)[0]
        R["ema200_slope"] = "rising" if sl > 0 else "falling" if sl < 0 else "flat"
    else:
        R["ema_alignment"] = "n/a (short)"; R["ema200_slope"] = "n/a"
    R["px_vs_e20"] = "above" if pd.notna(e20.iloc[-1]) and px > e20.iloc[-1] else "below" if pd.notna(e20.iloc[-1]) else "n/a"
    R["px_vs_e50"] = "above" if pd.notna(e50.iloc[-1]) and px > e50.iloc[-1] else "below" if pd.notna(e50.iloc[-1]) else "n/a"
    R["px_vs_e200"] = "above" if pd.notna(e200.iloc[-1]) and px > e200.iloc[-1] else "below" if pd.notna(e200.iloc[-1]) else "n/a"
    # ---------- B3 ADX ----------
    adxv, pdi, mdi = T.adx(h, l, c)
    R["adx"] = round(adxv.iloc[-1], 1) if pd.notna(adxv.iloc[-1]) else np.nan
    R["adx_regime"] = "trending" if adxv.iloc[-1] > 25 else "choppy" if adxv.iloc[-1] < 20 else "transitional"
    R["di"] = "+DI>-DI" if pdi.iloc[-1] > mdi.iloc[-1] else "-DI>+DI"
    R["adx_dir"] = "rising" if adxv.iloc[-1] > adxv.iloc[-6] else "falling"
    # ---------- B4 Supertrend ----------
    st, sd = T.supertrend(h, l, c)
    R["supertrend"] = "green_buy" if sd.iloc[-1] == 1 else "red_sell"
    flip = ""
    for kk in range(1, 6):
        if len(sd) > kk and sd.iloc[-kk] != sd.iloc[-kk-1]:
            flip = "buy_flip" if sd.iloc[-kk] == 1 else "sell_flip"; break
    R["supertrend_flip"] = flip or "none"
    # ---------- B5 ATR ----------
    a = T.atr(h, l, c)
    R["atr"] = round(a.iloc[-1], 2) if pd.notna(a.iloc[-1]) else np.nan
    R["atr_pct"] = round(a.iloc[-1]/px*100, 2) if pd.notna(a.iloc[-1]) else np.nan
    R["atr_state"] = "expanding" if pd.notna(a.iloc[-1]) and a.iloc[-1] > a.tail(10).mean() else "contracting"
    # ---------- B6 VWAP (rolling 20d) ----------
    vw = T.vwap_rolling(h, l, c, v).iloc[-1]
    R["vwap20"] = round(vw, 2) if pd.notna(vw) else np.nan
    R["px_vs_vwap"] = "above" if pd.notna(vw) and px > vw else "below" if pd.notna(vw) else "n/a"
    R["vwap_dist_pct"] = round((px-vw)/vw*100, 2) if pd.notna(vw) else np.nan
    # ---------- B7 Pivots (daily from last bar, weekly from last week) ----------
    dp = T.pivots(h.iloc[-1], l.iloc[-1], c.iloc[-1])
    R["pivot_P"] = round(dp["P"], 2); R["pivot_R1"] = round(dp["R1"], 2)
    R["pivot_S1"] = round(dp["S1"], 2)
    wk = df.set_index("date").resample("W").agg({"high": "max", "low": "min", "close": "last"}).dropna()
    if len(wk) >= 2:
        wp = T.pivots(wk["high"].iloc[-2], wk["low"].iloc[-2], wk["close"].iloc[-2])
        R["wpivot_R1"] = round(wp["R1"], 2); R["wpivot_S1"] = round(wp["S1"], 2)
        R["px_vs_wpivot"] = ("above_R2" if px > wp["R2"] else "above_R1" if px > wp["R1"]
                             else "below_S1" if px < wp["S1"] else "mid_range")
    else:
        R["wpivot_R1"] = R["wpivot_S1"] = np.nan; R["px_vs_wpivot"] = "n/a"
    return R

if __name__ == "__main__":
    data = pickle.load(open("ohlc.pkl", "rb"))
    rows = []
    for i, (sym, df) in enumerate(data.items(), 1):
        try:
            rows.append(analyze(sym, df))
        except Exception as e:
            rows.append({"symbol": sym, "bars": len(df), "error": f"{type(e).__name__}:{e}"})
        if i % 80 == 0: print(f"  {i}/{len(data)}")
    out = pd.DataFrame(rows)
    out.to_csv("indicators.csv", index=False)
    print(f"DONE. indicators for {len(out)} stocks -> indicators.csv")
    print("errors:", out["error"].notna().sum() if "error" in out else 0)
    print(out[["symbol","close","rsi","rsi_state","macd_pos","ema_alignment","adx","adx_regime","supertrend"]].head(12).to_string(index=False))
