"""
Master composite conviction sheet — merges all five framework passes + the screen flag
into one ranked table. Composite /100 = sum(sub_score/10 * weight), weights below.

Inputs : FINAL_universe_25pct.csv + the 5 *_ANALYSIS.csv + SCREEN_above_ema.csv
Output : MASTER_SCORECARD.csv
"""
import pandas as pd, numpy as np

# ---- weights (equal weight, sum=100) ----
W = {"lagging": 20, "leading": 20, "entry": 20, "smc": 20, "vcp": 20}

fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
ctx = fin[["symbol", "name", "exchange", "sector", "cap_bucket", "mktcap_cr",
           "price_today", "return_pct_final"]].rename(columns={
           "price_today": "CMP", "return_pct_final": "ret_6m_pct", "mktcap_cr": "mktcap_cr"})

def load(path, col, newname):
    d = pd.read_csv(path, dtype={"symbol": str})
    return d[["symbol", col]].rename(columns={col: newname}) if col in d.columns else \
           pd.DataFrame({"symbol": d["symbol"], newname: np.nan})

m = ctx \
    .merge(load("LAGGING_ANALYSIS.csv", "lagging_score_10", "lagging"), on="symbol", how="left") \
    .merge(load("LEADING_ANALYSIS.csv", "leading_score_10", "leading"), on="symbol", how="left") \
    .merge(load("ENTRY_PATTERN_ANALYSIS.csv", "pattern_quality_10", "entry"), on="symbol", how="left") \
    .merge(load("SMC_ANALYSIS.csv", "smc_score_10", "smc"), on="symbol", how="left") \
    .merge(load("VCP_ANALYSIS.csv", "vcp_leg_score_10", "vcp"), on="symbol", how="left")

_scr = pd.read_csv("SCREEN_above_ema.csv", dtype=str)
screen_pass = set(_scr["Symbol"] if "Symbol" in _scr.columns else _scr["symbol"])
m["screen_pass"] = m["symbol"].isin(screen_pass).map({True: "Y", False: "N"})

subs = ["lagging", "leading", "entry", "smc", "vcp"]
m["passes_available"] = m[subs].notna().sum(axis=1)

def composite(r):
    if r["passes_available"] == 0:
        return np.nan
    # rescale weights over available sub-scores so partial coverage isn't penalised to 0
    wsum = sum(W[s] for s in subs if pd.notna(r[s]))
    got = sum((r[s] / 10) * W[s] for s in subs if pd.notna(r[s]))
    return round(got / wsum * 100, 1)

m["composite_100"] = m.apply(composite, axis=1)

def tier(x):
    if pd.isna(x): return "n/a"
    if x >= 80: return "TIER 1"
    if x >= 65: return "TIER 2"
    if x >= 50: return "TIER 3"
    return "WATCH"
m["tier"] = m["composite_100"].apply(tier)

m = m.sort_values(["composite_100", "ret_6m_pct"], ascending=[False, False], na_position="last").reset_index(drop=True)
m.insert(0, "rank", m.index + 1)

cols = ["rank", "symbol", "name", "exchange", "sector", "cap_bucket", "CMP", "ret_6m_pct", "mktcap_cr",
        "lagging", "leading", "entry", "smc", "vcp", "passes_available",
        "composite_100", "tier", "screen_pass"]
m[cols].to_csv("MASTER_SCORECARD.csv", index=False)

print(f"weights: {W}  (sum={sum(W.values())})")
print(f"stocks ranked: {m['composite_100'].notna().sum()} | incomplete (<5 passes): {int((m['passes_available']<5).sum())}")
print("tier distribution:", m["tier"].value_counts().reindex(["TIER 1","TIER 2","TIER 3","WATCH"]).dropna().to_dict())
print(f"composite: min={m['composite_100'].min()} median={m['composite_100'].median()} max={m['composite_100'].max()}")
print(f"screen-passers in TIER 1/2: {int(((m['tier'].isin(['TIER 1','TIER 2']))&(m['screen_pass']=='Y')).sum())}")
print("\n=== TOP 25 (composite /100) ===")
show = m.head(25)[["rank","symbol","exchange","cap_bucket","ret_6m_pct","lagging","leading","entry","smc","vcp","composite_100","tier","screen_pass"]]
print(show.to_string(index=False))
