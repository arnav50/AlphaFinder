"""VCP (Minervini) + Gann theory primitives — OHLCV only, deterministic."""
import numpy as np, pandas as pd
import ta_lib_local as T

# ----------------------- VCP -----------------------
def detect_vcp(df, window=90):
    o,h,l,c,v = (df[x] for x in ["open","high","low","close","volume"])
    px = float(c.iloc[-1]); n = len(df)
    low52 = float(l.tail(252).min()); high52 = float(h.tail(252).max())
    ema200 = T.ema(c,200).iloc[-1]
    above_52low_pct = (px/low52-1)*100 if low52>0 else np.nan
    prior_uptrend = (above_52low_pct >= 30) and (pd.notna(ema200) and px > ema200)

    sub = df.tail(window).reset_index(drop=True)
    sh, sl = T.swings(sub["close"], 3)
    # build alternating peak/trough events
    ev = sorted([(i,"H",float(sub["high"].iloc[i])) for i in sh] +
                [(i,"L",float(sub["low"].iloc[i])) for i in sl], key=lambda x:x[0])
    # contractions: each peak followed by a trough
    contractions = []
    last_peak = None
    for i,t,p in ev:
        if t=="H":
            last_peak = (i,p)
        elif t=="L" and last_peak is not None:
            depth = (last_peak[1]-p)/last_peak[1]*100
            dur = i-last_peak[0]
            if depth >= 2:   # ignore noise
                contractions.append({"peak_i":last_peak[0],"peak":round(last_peak[1],2),
                                     "trough_i":i,"trough":round(p,2),
                                     "depth_pct":round(depth,1),"dur_bars":int(dur)})
            last_peak = None
    last3 = contractions[-3:] if len(contractions)>=3 else contractions[-len(contractions):]
    nC = len(last3)
    depths = [x["depth_pct"] for x in last3]
    decreasing = all(depths[i] > depths[i+1] for i in range(len(depths)-1)) if nC>=2 else False
    durs = [x["dur_bars"] for x in last3]
    dur_decreasing = all(durs[i] >= durs[i+1] for i in range(len(durs)-1)) if nC>=2 else False

    # pivot = most recent swing high in window (consolidation ceiling)
    pivot = float(sub["high"].iloc[sh[-1]]) if sh else high52
    # volume dry-up: last-5d avg vol vs 50d avg, and vs min 5d-avg over last 60
    v50 = v.tail(50).mean(); v5 = v.tail(5).mean()
    vdu_ratio = v5/v50 if v50>0 else np.nan
    roll5 = v.tail(60).rolling(5).mean()
    vdu = bool(pd.notna(vdu_ratio) and vdu_ratio < 0.85) or bool(v5 <= roll5.min()*1.15)

    near_high = px >= 0.92*high52
    # breakout state
    recent = c.tail(4).values
    above_pivot = px > pivot*1.001
    broke_recently = any(recent[k] <= pivot and px > pivot for k in range(len(recent)))
    pct_from_pivot = (px-pivot)/pivot*100
    # breakout-day volume (today vs 50d avg)
    bo_vol_ratio = v.iloc[-1]/v50 if v50>0 else np.nan
    rng = h.iloc[-1]-l.iloc[-1]
    close_pos = (c.iloc[-1]-l.iloc[-1])/rng if rng>0 else 0.5

    if above_pivot and pct_from_pivot <= 8:
        status = "BROKEN OUT (fresh)"
    elif above_pivot and pct_from_pivot > 8:
        status = "extended past pivot"
    elif -5 <= pct_from_pivot <= 1:
        status = "AT PIVOT (actionable)"
    else:
        status = "forming / still basing"

    # quality
    if prior_uptrend and nC>=3 and decreasing and vdu and near_high:
        quality = "Strong VCP"
    elif prior_uptrend and nC>=2 and (decreasing or vdu) and near_high:
        quality = "Moderate VCP"
    else:
        quality = "No VCP"

    return {
        "prior_uptrend": prior_uptrend, "pct_above_52w_low": round(above_52low_pct,1),
        "above_ema200": bool(pd.notna(ema200) and px>ema200),
        "num_contractions": nC,
        "contractions": " | ".join(f"C{j+1}:-{x['depth_pct']}%/{x['dur_bars']}b" for j,x in enumerate(last3)) or "none",
        "depths_decreasing": decreasing, "dur_decreasing": dur_decreasing,
        "vdu_confirmed": vdu, "vdu_ratio": round(float(vdu_ratio),2) if pd.notna(vdu_ratio) else np.nan,
        "near_52w_high": near_high, "pivot": round(pivot,2), "pct_from_pivot": round(pct_from_pivot,2),
        "breakout_vol_ratio": round(float(bo_vol_ratio),2) if pd.notna(bo_vol_ratio) else np.nan,
        "breakout_close_pos": round(close_pos,2),
        "vcp_status": status, "vcp_quality": quality,
        "entry_zone": f"{round(pivot*1.00,2)}-{round(pivot*1.05,2)}" if quality!="No VCP" else "n/a",
    }

# ----------------------- GANN -----------------------
def swing_low_ref(df, lookback=180):
    sub = df.tail(lookback)
    i = sub["low"].idxmin()
    return int(i), float(df["low"].loc[i]), df["date"].loc[i]

def gann_square9(price):
    r = np.sqrt(price)
    def up(inc): return round((r+inc)**2, 2)
    def dn(inc): return round((r-inc)**2, 2)
    return {"T1_+0.25": up(0.25), "T2_+0.5": up(0.5), "T3_+1.0": up(1.0),
            "S1_-0.25": dn(0.25), "S2_-0.5": dn(0.5)}

def gann_angles(df):
    """Gann angles from last major swing low, auto-scaled: 1x1 = traverse the
    52-week price range over 252 bars (1 'natural unit' = range/252 price-pts per bar).
    Scale-invariant across price levels. Price above 1x1 => stronger-than-balanced trend."""
    i, lowp, lowdate = swing_low_ref(df)
    bars = (len(df)-1) - i
    px = float(df["close"].iloc[-1])
    lo52 = float(df["low"].tail(252).min()); hi52 = float(df["high"].tail(252).max())
    unit = (hi52-lo52)/252 if hi52>lo52 else np.nan
    if bars <= 0 or pd.isna(unit) or unit==0:
        return {"days_since_low": bars, "above_1x1": None, "g1x1": np.nan, "g2x1": np.nan,
                "g1x2": np.nan, "low_price": round(lowp,2), "low_date": str(lowdate.date())}
    g1x1 = lowp + 1*unit*bars
    g2x1 = lowp + 2*unit*bars
    g1x2 = lowp + 0.5*unit*bars
    return {"days_since_low": int(bars), "low_price": round(lowp,2), "low_date": str(lowdate.date()),
            "gann_unit_per_bar": round(unit,3),
            "g1x1": round(g1x1,2), "g2x1": round(g2x1,2), "g1x2": round(g1x2,2),
            "above_1x1": bool(px>g1x1), "above_2x1": bool(px>g2x1),
            "gann_trend": "very strong (>2x1)" if px>g2x1 else "strong (>1x1)" if px>g1x1
                          else "moderate (>1x2)" if px>g1x2 else "weak (<1x2)"}

def gann_time_cycles(days):
    cycles = [30,45,60,90,120,144,180,270,360]
    nxt = next((x for x in cycles if x > days), None)
    near = any(abs(days-x) <= 5 for x in cycles)
    return {"next_gann_cycle_days": nxt, "days_to_next_cycle": (nxt-days) if nxt else None,
            "near_gann_cycle": near}

def gann_octave(df):
    lo = float(df["low"].tail(252).min()); hi = float(df["high"].tail(252).max())
    px = float(df["close"].iloc[-1])
    if hi==lo: return {"octave": "n/a", "octave_n": np.nan}
    frac = (px-lo)/(hi-lo)
    n = min(8, int(frac*8)+1)
    labels={1:"1/8",2:"2/8 (25%)",3:"3/8",4:"4/8 (50%)",5:"5/8",6:"6/8 (75%)",7:"7/8 (exhaustion)",8:"8/8 (52w high)"}
    return {"octave": labels[n], "octave_n": n, "octave_levels":
            f"4/8={round(lo+(hi-lo)*0.5,2)} 6/8={round(lo+(hi-lo)*0.75,2)} 7/8={round(lo+(hi-lo)*0.875,2)}"}

def gann_cardinal(price):
    r = np.sqrt(price)
    below = int(np.floor(r))**2; above = int(np.ceil(r))**2
    nearest = below if abs(price-below)<abs(price-above) else above
    dist = abs(price-nearest)/price*100
    return {"nearest_cardinal_sq": nearest, "cardinal_dist_pct": round(dist,2),
            "near_cardinal": dist<=2.0, "cardinal_below": below, "cardinal_above": above}
