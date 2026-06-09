"""
STEP 4 — Prime Filter construction from the T=0 fingerprint.
4A: mean / std / Q1 / Q3 / sweet-spot (Q1-Q3) / extended (mean +/- 1 SD) per indicator.
4B: star rating by % of winners meeting a transparent bullish criterion per indicator.
Sector momentum: sectors with >=3 Phase-1 winners.
Reads T0_FINGERPRINT.csv + FINAL_universe_25pct.csv.
"""
import pandas as pd, numpy as np

fp = pd.read_csv("T0_FINGERPRINT.csv", dtype={"symbol": str})
fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})

NUM = ["rsi", "stochrsi_k", "adx", "plus_di", "minus_di", "cmf", "obv_accum_weeks", "atr_pct",
       "dist_ema9", "dist_ema21", "dist_ema50", "dist_ema200", "pctB",
       "days_in_base", "base_depth_pct", "breakout_vol_x20", "pct_below_52wh",
       "final_contraction_depth", "sq9_proximity_pct"]

print("=== STEP 4A — STATISTICAL ANALYSIS ===")
rows = []
for col in NUM:
    s = pd.to_numeric(fp[col], errors="coerce").dropna()
    if len(s) == 0: continue
    m, sd = s.mean(), s.std()
    rows.append({"indicator": col, "n": len(s), "mean": round(m, 2), "std": round(sd, 2),
                 "Q1": round(s.quantile(.25), 2), "Q3": round(s.quantile(.75), 2),
                 "sweet_Q1_Q3": f"{round(s.quantile(.25),2)} to {round(s.quantile(.75),2)}",
                 "ext_mean_pm_sd": f"{round(m-sd,2)} to {round(m+sd,2)}"})
A = pd.DataFrame(rows); A.to_csv("STEP4A_STATS.csv", index=False)
print(A.to_string(index=False))

print("\n=== STEP 4B — STAR WEIGHTING (% of winners meeting bullish criterion) ===")
def pct(mask): return round(100 * mask.mean(), 1)
crit = {
    "RSI in 50-80":            pct(fp["rsi"].between(50, 80)),
    "ADX > 20 (trending)":     pct(pd.to_numeric(fp["adx"], errors="coerce") > 20),
    "+DI > -DI":               pct(pd.to_numeric(fp["plus_di"], errors="coerce") > pd.to_numeric(fp["minus_di"], errors="coerce")),
    "CMF > 0":                 pct(pd.to_numeric(fp["cmf"], errors="coerce") > 0),
    "OBV trending up":         pct(fp["obv_up"].astype(bool)),
    "ATR% in 2-7":             pct(fp["atr_pct"].between(2, 7)),
    "Price > EMA9":            pct(fp["dist_ema9"] > 0),
    "Price > EMA21":           pct(fp["dist_ema21"] > 0),
    "Price > EMA50":           pct(fp["dist_ema50"] > 0),
    "Price > EMA200":          pct(fp["dist_ema200"] > 0),
    "%B > 80 (upper band)":    pct(pd.to_numeric(fp["pctB"], errors="coerce") > 80),
    "Breakout vol > 1.5x":     pct(pd.to_numeric(fp["breakout_vol_x20"], errors="coerce") > 1.5),
    "Base depth 10-40%":       pct(fp["base_depth_pct"].between(10, 40)),
    "Final contraction <15%":  pct(pd.to_numeric(fp["final_contraction_depth"], errors="coerce") < 15),
    "Liquidity sweep":         pct(fp["liquidity_sweep"].astype(bool)),
    "FVG unfilled below":      pct(fp["fvg_below_unfilled"].astype(bool)),
    "Above Gann 1x1":          pct(fp["above_gann_1x1"].astype(bool)),
    "Within Gann cycle":       pct(fp["within_gann_cycle"].astype(bool)),
}
def stars(p):
    if p >= 80: return "***** (>=80%)"
    if p >= 65: return "**** (65-80%)"
    if p >= 50: return "*** (50-65%)"
    return "DISCARD (<50%)"
B = pd.DataFrame([{"indicator": k, "appeared_%": v, "rating": stars(v)} for k, v in
                  sorted(crit.items(), key=lambda x: -x[1])])
B.to_csv("STEP4B_WEIGHTS.csv", index=False)
print(B.to_string(index=False))

print("\n=== SECTOR MOMENTUM (sectors with >=3 Phase-1 winners) ===")
sec = fin["sector"].fillna("n/a").value_counts()
hot = sec[sec >= 3]
print(hot.to_string())
hot.to_csv("STEP4_SECTORS.csv")
