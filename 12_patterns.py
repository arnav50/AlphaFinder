"""Phase 2 Section D: trend structure + chart patterns (algorithmic, with honest confidence).
Output: patterns.csv -> symbol | trend_structure | pattern | breakout_level | volume_confirm | target | confidence"""
import pickle, numpy as np, pandas as pd
import ta_lib_local as T

def fractals(df, w=3):
    hi, lo = T.swings(df["close"], w)
    return hi, lo

def trend_structure(df):
    hi, lo = fractals(df, 4)
    c = df["close"]
    hh = [c.iloc[i] for i in hi][-3:]; ll = [c.iloc[i] for i in lo][-3:]
    up = len(hh) >= 2 and len(ll) >= 2 and hh[-1] > hh[-2] and ll[-1] > ll[-2]
    dn = len(hh) >= 2 and len(ll) >= 2 and hh[-1] < hh[-2] and ll[-1] < ll[-2]
    if up: return "Uptrend (HH/HL)"
    if dn: return "Downtrend (LH/LL)"
    return "Sideways / range-bound"

def line(idxs, vals):
    if len(idxs) < 2: return 0.0, np.mean(vals) if len(vals) else 0.0
    m, b = np.polyfit(idxs, vals, 1)
    return m, b

def vol_confirm(df, lvl):
    """recent breakout bar volume vs 20d avg."""
    v = df["volume"]; avg = v.tail(20).mean()
    last = v.iloc[-1]
    return "yes" if last > 1.5*avg else "weak" if last > avg else "no"

def detect_chart(df):
    """returns (pattern, breakout_level, target, confidence) for a recent window."""
    win = df.tail(90).reset_index(drop=True)
    if len(win) < 30: return ("insufficient history", np.nan, np.nan, "low")
    c, h, l = win["close"], win["high"], win["low"]
    hi, lo = T.swings(c, 3)
    px = c.iloc[-1]
    out = []

    # --- Double Top / Bottom ---
    if len(hi) >= 2:
        a, b = hi[-2], hi[-1]
        if abs(c.iloc[a]-c.iloc[b])/c.iloc[a] < 0.04:
            trough = c.iloc[a:b+1].min()
            out.append(("Double Top", round(trough,2), round(trough-(c.iloc[a]-trough),2), "medium"))
    if len(lo) >= 2:
        a, b = lo[-2], lo[-1]
        if abs(c.iloc[a]-c.iloc[b])/c.iloc[a] < 0.04:
            peak = c.iloc[a:b+1].max()
            out.append(("Double Bottom", round(peak,2), round(peak+(peak-c.iloc[a]),2), "medium"))
    # --- Head & Shoulders / Inverse ---
    if len(hi) >= 3:
        x,y,z = hi[-3],hi[-2],hi[-1]
        if c.iloc[y] > c.iloc[x] and c.iloc[y] > c.iloc[z] and abs(c.iloc[x]-c.iloc[z])/c.iloc[x] < 0.06:
            neck = min(c.iloc[x:y+1].min(), c.iloc[y:z+1].min())
            out.append(("Head & Shoulders", round(neck,2), round(neck-(c.iloc[y]-neck),2), "medium"))
    if len(lo) >= 3:
        x,y,z = lo[-3],lo[-2],lo[-1]
        if c.iloc[y] < c.iloc[x] and c.iloc[y] < c.iloc[z] and abs(c.iloc[x]-c.iloc[z])/c.iloc[x] < 0.06:
            neck = max(c.iloc[x:y+1].max(), c.iloc[y:z+1].max())
            out.append(("Inverse Head & Shoulders", round(neck,2), round(neck+(neck-c.iloc[y]),2), "medium"))
    # --- Triangles / Wedges / Rectangle via trendline slopes on swings ---
    if len(hi) >= 2 and len(lo) >= 2:
        mh, bh = line(hi[-3:], [c.iloc[i] for i in hi[-3:]])
        ml, bl = line(lo[-3:], [c.iloc[i] for i in lo[-3:]])
        rngh = np.ptp([c.iloc[i] for i in hi[-3:]]) if len(hi)>=2 else 0
        rngl = np.ptp([c.iloc[i] for i in lo[-3:]]) if len(lo)>=2 else 0
        flat_h = abs(mh) < 0.0008*px; flat_l = abs(ml) < 0.0008*px
        upper = mh*(len(c)-1)+bh
        if flat_h and ml > 0:   out.append(("Ascending Triangle", round(upper,2), round(upper*1.1,2), "medium"))
        elif flat_l and mh < 0: out.append(("Descending Triangle", round(ml*(len(c)-1)+bl,2), np.nan, "medium"))
        elif mh < 0 and ml > 0: out.append(("Symmetrical Triangle", round(upper,2), np.nan, "low"))
        elif mh > 0 and ml > 0 and mh < ml: out.append(("Rising Wedge (bearish)", round(ml*(len(c)-1)+bl,2), np.nan, "low"))
        elif mh < 0 and ml < 0 and ml < mh: out.append(("Falling Wedge (bullish)", round(upper,2), np.nan, "low"))
        elif flat_h and flat_l:  out.append(("Rectangle consolidation", round(upper,2), np.nan, "low"))
    # --- Flag / Pennant: strong pole then tight consolidation ---
    pole = (c.iloc[-20] if len(c)>20 else c.iloc[0])
    run = (c.iloc[-6]/c.iloc[-26]-1)*100 if len(c) > 26 else 0
    recent_range = (c.tail(6).max()-c.tail(6).min())/c.tail(6).mean()*100
    if run > 20 and recent_range < 8:
        out.append(("Bull Flag / Pennant", round(c.tail(6).max(),2), round(c.tail(6).max()*(1+run/100),2), "medium"))
    # --- Rounding bottom (saucer): U-shape fit ---
    if len(c) >= 40:
        x = np.arange(len(c)); coef = np.polyfit(x, c.values, 2)
        if coef[0] > 0 and c.iloc[-1] > c.iloc[len(c)//2]:
            out.append(("Rounding Bottom (saucer)", round(c.max(),2), np.nan, "low"))

    if not out:
        return ("No clean pattern", np.nan, np.nan, "n/a")
    # prefer medium-confidence / most actionable
    out.sort(key=lambda t: 0 if t[3]=="medium" else 1)
    return out[0]

if __name__ == "__main__":
    data = pickle.load(open("ohlc.pkl","rb"))
    rows = []
    for sym, df in data.items():
        df = df.reset_index(drop=True)
        ts = trend_structure(df)
        pat, lvl, tgt, conf = detect_chart(df)
        rows.append({"symbol":sym,"trend_structure":ts,"chart_pattern":pat,
                     "breakout_level":lvl,"volume_confirm":vol_confirm(df,lvl) if pd.notna(lvl) else "n/a",
                     "target":tgt,"pattern_confidence":conf})
    out = pd.DataFrame(rows); out.to_csv("patterns.csv", index=False)
    print(f"DONE. patterns for {len(out)} stocks")
    print("trend_structure:", out["trend_structure"].value_counts().to_dict())
    print("\nchart patterns:")
    print(out["chart_pattern"].value_counts().to_string())
