"""
T=0 (move-start) fingerprint for the Phase-1 universe.
T=0 = first decisive breakout / strong-impulse candle after the base low, located by
reusing 19_day0.find_day0() (volume >=1.4x 50d, forward gain >=15%, with fallback).

For every Phase-1 stock, snapshot the full requested field set AS OF T=0 (indicators read
at the breakout bar; VCP/SMC/Gann computed on df[:t0+1] = info available at breakout).
Then aggregate across all stocks: MIN/MAX/MEAN/MEDIAN + the 70% common range (P15-P85,
which by construction contains the central 70% of stocks) = the PRIME FILTER values.

Outputs: T0_FINGERPRINT.csv (per-stock) + T0_PRIME_FILTER.csv (aggregate + prime ranges)
"""
import pickle, re, importlib.util, numpy as np, pandas as pd
import ta_lib_local as T
import ta_smc as S
import ta_vcp_gann as VG

# reuse the breakout/Day-0 locator + candlestick detector
_d0 = importlib.util.spec_from_file_location("day0mod", "19_day0.py")
D0 = importlib.util.module_from_spec(_d0); _d0.loader.exec_module(D0)
_c11 = importlib.util.spec_from_file_location("cand", "11_candles.py")
CN = importlib.util.module_from_spec(_c11); _c11.loader.exec_module(CN)

def stochrsi(close, n=14, k=3, d=3):
    r = T.rsi(close, n); ll = r.rolling(n).min(); hh = r.rolling(n).max()
    sr = 100 * (r - ll) / (hh - ll).replace(0, np.nan)
    K = sr.rolling(k).mean(); return K, K.rolling(d).mean()

def cmf(h, l, c, v, n=20):
    mfm = (((c - l) - (h - c)) / (h - l).replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0)
    return (mfm * v).rolling(n, min_periods=10).sum() / v.rolling(n, min_periods=10).sum().replace(0, np.nan)

def parse_last_depth(s):
    d = re.findall(r"C\d+:-([\d.]+)%", s); return float(d[-1]) if d else np.nan

def at(series, i, r=2):
    x = series.iloc[i]; return round(float(x), r) if pd.notna(x) else np.nan

def snap(sym, df):
    df = df.reset_index(drop=True)
    o, h, l, c, v = (df[x] for x in ["open", "high", "low", "close", "volume"])
    n = len(df)
    i, verified, volmult = D0.find_day0(df)            # T=0 = breakout bar
    R = {"symbol": sym, "t0_date": str(df["date"].iloc[i].date()),
         "t0_verified_breakout": verified, "bars_after_t0": n - 1 - i}

    rsi = T.rsi(c); K, _ = stochrsi(c); adxv, pdi, mdi = T.adx(h, l, c)
    cm = cmf(h, l, c, v); atr = T.atr(h, l, c); obv = T.obv(c, v)
    macd, sig, hist = T.macd(c)
    e9, e21, e50, e200 = T.ema(c, 9), T.ema(c, 21), T.ema(c, 50), T.ema(c, 200)
    mid, ub, lb, _ = T.bollinger(c)

    # ---- LEADING @ T=0 ----
    R["rsi"] = at(rsi, i, 1); R["stochrsi_k"] = at(K, i, 1)
    R["adx"] = at(adxv, i, 1); R["plus_di"] = at(pdi, i, 1); R["minus_di"] = at(mdi, i, 1)
    R["cmf"] = at(cm, i, 3)
    obv_seg = obv.iloc[max(0, i-60):i+1].reset_index(drop=True)
    R["obv_up"] = bool(D0.slope(obv, i, 10) > 0)
    R["obv_accum_weeks"] = round(((len(obv_seg) - 1) - int(obv_seg.idxmin())) / 5, 1) if len(obv_seg) >= 5 else np.nan
    R["atr"] = at(atr, i, 2)
    R["atr_pct"] = round(float(atr.iloc[i] / c.iloc[i] * 100), 2) if pd.notna(atr.iloc[i]) else np.nan

    # ---- LAGGING @ T=0 ----
    def distpct(ema):
        return round(float((c.iloc[i] / ema.iloc[i] - 1) * 100), 2) if pd.notna(ema.iloc[i]) else np.nan
    R["dist_ema9"] = distpct(e9); R["dist_ema21"] = distpct(e21)
    R["dist_ema50"] = distpct(e50); R["dist_ema200"] = distpct(e200)
    R["macd"] = at(macd, i, 3); R["macd_signal"] = at(sig, i, 3); R["macd_hist"] = at(hist, i, 3)
    if pd.notna(ub.iloc[i]) and ub.iloc[i] > lb.iloc[i]:
        R["pctB"] = round(float((c.iloc[i] - lb.iloc[i]) / (ub.iloc[i] - lb.iloc[i]) * 100), 1)
        R["bb_position"] = ("upper" if c.iloc[i] >= ub.iloc[i] * 0.99 else
                            "lower" if c.iloc[i] <= lb.iloc[i] * 1.01 else
                            "above_mid" if c.iloc[i] > mid.iloc[i] else "below_mid")
    else:
        R["pctB"] = np.nan; R["bb_position"] = "n/a"

    # ---- PRICE STRUCTURE @ T=0 ----
    win0 = max(0, n - 200)
    base_low_idx = int(c.iloc[win0:i].idxmin()) if i > win0 + 2 else win0
    ph_lo = max(0, base_low_idx - 40)
    prior_high = float(h.iloc[ph_lo:base_low_idx].max()) if base_low_idx > ph_lo else float(h.iloc[base_low_idx])
    R["days_in_base"] = int(i - base_low_idx)
    R["weeks_in_base"] = round((i - base_low_idx) / 5, 1)
    R["base_depth_pct"] = round((prior_high - float(l.iloc[base_low_idx])) / prior_high * 100, 1) if prior_high > 0 else np.nan
    v20 = v.iloc[max(0, i-20):i].mean()
    R["breakout_vol_x20"] = round(float(v.iloc[i] / v20), 2) if pd.notna(v20) and v20 > 0 else np.nan
    pats = [p for p in CN.detect_at(df, i) if p in CN.BULL]
    if pats:
        R["breakout_candle"] = pats[0]
    else:
        rng = h.iloc[i] - l.iloc[i]; body = abs(c.iloc[i] - o.iloc[i])
        R["breakout_candle"] = ("Strong Green" if c.iloc[i] > o.iloc[i] and rng > 0 and body >= 0.6 * rng
                                else "Green" if c.iloc[i] > o.iloc[i] else "Red/Doji")
    hi52 = float(h.iloc[max(0, i-252):i+1].max())
    R["close_at_breakout"] = round(float(c.iloc[i]), 2); R["high_52w_at_t0"] = round(hi52, 2)
    R["pct_below_52wh"] = round((hi52 - c.iloc[i]) / hi52 * 100, 2) if hi52 > 0 else np.nan
    vcp = VG.detect_vcp(df.iloc[:i+1].reset_index(drop=True))
    R["vcp_contractions"] = vcp["num_contractions"]
    R["final_contraction_depth"] = parse_last_depth(vcp["contractions"])

    # ---- SMC @ T=0 ----
    pre = df.iloc[:i+1].reset_index(drop=True)
    sweep = False
    if base_low_idx >= 20:
        prior_low = float(l.iloc[base_low_idx-15:base_low_idx-2].min())
        for j in range(max(0, base_low_idx-8), min(n, i+1)):
            if l.iloc[j] < prior_low and c.iloc[j] > prior_low:
                sweep = True; break
    R["liquidity_sweep"] = sweep
    _, _, clean = S.bos_choch(pre)
    choch_idx = None
    for kk in range(1, len(clean)):
        if clean[kk]["dir"] == "bull" and clean[kk-1]["dir"] == "bear":
            choch_idx = clean[kk]["i"]
    R["choch_distance_candles"] = int(i - choch_idx) if choch_idx is not None and choch_idx <= i else np.nan
    _, _, nb, _ = S.fvgs(pre)
    R["fvg_below_unfilled"] = bool(nb is not None)

    # ---- GANN @ T=0 ----
    g = VG.gann_angles(pre)
    R["above_gann_1x1"] = bool(g.get("above_1x1")) if g.get("above_1x1") is not None else None
    sq9 = VG.gann_square9(float(c.iloc[i]))
    R["sq9_proximity_pct"] = round(min(abs(c.iloc[i] - lvl) / c.iloc[i] * 100 for lvl in sq9.values()), 2)
    R["within_gann_cycle"] = bool(VG.gann_time_cycles(g.get("days_since_low", 0))["near_gann_cycle"])
    return R

NUMERIC = ["rsi", "stochrsi_k", "adx", "plus_di", "minus_di", "cmf", "obv_accum_weeks", "atr_pct",
           "dist_ema9", "dist_ema21", "dist_ema50", "dist_ema200", "macd_hist", "pctB",
           "days_in_base", "base_depth_pct", "breakout_vol_x20", "pct_below_52wh",
           "vcp_contractions", "final_contraction_depth", "choch_distance_candles", "sq9_proximity_pct"]
BOOL = ["obv_up", "liquidity_sweep", "fvg_below_unfilled", "above_gann_1x1", "within_gann_cycle",
        "t0_verified_breakout"]

if __name__ == "__main__":
    fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
    meta = fin.set_index("symbol")[["name", "exchange"]].to_dict("index")
    data = pickle.load(open("ohlc.pkl", "rb"))
    rows = []
    for ix, sym in enumerate(fin["symbol"], 1):
        df = data.get(sym)
        if df is None or len(df) < 60:
            rows.append({"symbol": sym, "note": "insufficient OHLC"}); continue
        try:
            r = snap(sym, df); r["name"] = meta.get(sym, {}).get("name", "")
            r["exchange"] = meta.get(sym, {}).get("exchange", ""); rows.append(r)
        except Exception as e:
            rows.append({"symbol": sym, "note": f"{type(e).__name__}:{e}"})
        if ix % 80 == 0: print(f"  {ix}/{len(fin)}")

    out = pd.DataFrame(rows)
    front = ["symbol", "name", "exchange", "t0_date", "t0_verified_breakout"]
    cols = front + [c for c in (NUMERIC + [b for b in BOOL if b != "t0_verified_breakout"]
                                + ["breakout_candle", "bb_position", "close_at_breakout", "high_52w_at_t0"])
                    if c in out.columns]
    out[[c for c in cols if c in out.columns]].to_csv("T0_FINGERPRINT.csv", index=False)

    valid = out[out.get("rsi").notna()] if "rsi" in out else out
    agg = []
    for col in NUMERIC:
        if col not in valid.columns: continue
        s = pd.to_numeric(valid[col], errors="coerce").dropna()
        if len(s) == 0: continue
        agg.append({"indicator": col, "n": len(s), "min": round(s.min(), 2), "max": round(s.max(), 2),
                    "mean": round(s.mean(), 2), "median": round(s.median(), 2),
                    "prime_low_P15": round(s.quantile(0.15), 2), "prime_high_P85": round(s.quantile(0.85), 2)})
    for col in BOOL:
        if col not in valid.columns: continue
        s = valid[col].dropna()
        if len(s) == 0: continue
        pct = round(100 * s.astype(bool).mean(), 1)
        agg.append({"indicator": col, "n": len(s), "min": "", "max": "", "mean": f"{pct}% Yes",
                    "median": "", "prime_low_P15": "TRUE in 70%+" if pct >= 70 else "", "prime_high_P85": ""})
    A = pd.DataFrame(agg)
    A.to_csv("T0_PRIME_FILTER.csv", index=False)

    print(f"\nDONE. T=0 snapshot for {len(valid)} stocks -> T0_FINGERPRINT.csv")
    print(f"verified breakout (vol>=1.4x): {int(valid['t0_verified_breakout'].sum())}/{len(valid)}")
    print("\n=== PRIME FILTER (70% common range = P15-P85) ===")
    print(A.to_string(index=False))
