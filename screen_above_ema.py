"""
Ad-hoc screen on top of the verified Phase-1 universe.

FILTERS (all must pass):
  1. 6M return >= 25%                 (return_pct_final, already verified in FINAL)
  2. Market cap >= 500 Cr             (mktcap_cr)
  3. 20-day avg volume >= 2,00,000    (computed live from ohlc.pkl trailing 20 bars)
  4. Trading ABOVE 200-EMA            (indicators.csv px_vs_e200 == 'above')
  5. Trading ABOVE 50-EMA             (indicators.csv px_vs_e50  == 'above')
Plus inherited exclusions: CMP >= Rs10 (pennies already dropped from FINAL),
  avg vol < 1 lakh (subsumed by >=2 lakh gate), corp-action distorted names.

Inputs : FINAL_universe_25pct.csv, indicators.csv, hits_verified.csv, ohlc.pkl
Outputs: SCREEN_above_ema.csv         (all caps >=500Cr, sorted by 6M return desc)
         SCREEN_above_ema_smallcap.csv (Small-cap subset, listed separately)
"""
import pickle, pandas as pd

MIN_RET   = 25
MIN_MCAP  = 500          # Rs crore
MIN_VOL20 = 200_000      # shares

fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
ind = pd.read_csv("indicators.csv", dtype={"symbol": str})[["symbol", "px_vs_e50", "px_vs_e200", "ema50", "ema200"]]
hv  = pd.read_csv("hits_verified.csv", dtype={"symbol": str})
ohlc = pickle.load(open("ohlc.pkl", "rb"))

# --- true trailing 20-bar average volume from daily OHLCV ---
def vol20(sym):
    df = ohlc.get(sym)
    if df is None or "volume" not in df or len(df) < 20:
        return float("nan")
    return float(df["volume"].dropna().tail(20).mean())

fin["avg_vol_20d"] = fin["symbol"].map(vol20)

# --- corp-action distorted names to remove (raw vs split/bonus-adjusted gap > 8pts) ---
corp = set(hv[hv.get("corp_action", False) == True]["symbol"]) if "corp_action" in hv.columns else set()

# --- join EMA position flags ---
df = fin.merge(ind, on="symbol", how="left")

n0 = len(df)
df = df[df["return_pct_final"] >= MIN_RET]
n1 = len(df)
df = df[df["mktcap_cr"] >= MIN_MCAP]
n2 = len(df)
df = df[df["avg_vol_20d"] >= MIN_VOL20]
n3 = len(df)
df = df[df["px_vs_e200"] == "above"]
n4 = len(df)
df = df[df["px_vs_e50"] == "above"]
n5 = len(df)
df = df[~df["symbol"].isin(corp)]
n6 = len(df)

df = df.drop(columns=["rank"], errors="ignore").sort_values("return_pct_final", ascending=False).reset_index(drop=True)
df.insert(0, "rank", df.index + 1)

out_cols = ["rank", "name", "symbol", "exchange", "price_today", "return_pct_final",
            "mktcap_cr", "cap_bucket", "sector", "avg_vol_20d", "px_vs_e50", "px_vs_e200",
            "ema50", "ema200", "past_date_used", "xsrc_mismatch_pct"]
out = df[out_cols].rename(columns={
    "name": "Stock Name", "symbol": "Symbol", "exchange": "Exchange",
    "price_today": "CMP", "return_pct_final": "6M Return%", "mktcap_cr": "Market Cap (Cr)",
    "cap_bucket": "Cap", "sector": "Sector", "avg_vol_20d": "Avg Vol (20D)"})
out["Avg Vol (20D)"] = out["Avg Vol (20D)"].round(0).astype("Int64")
out.to_csv("SCREEN_above_ema.csv", index=False)

small = out[out["Cap"] == "Small"].copy()
small.to_csv("SCREEN_above_ema_smallcap.csv", index=False)

print("=== FUNNEL (each filter applied in order) ===")
print(f"  start (FINAL verified, >=Rs10, penny-free) : {n0}")
print(f"  1. 6M return >= 25%                         : {n1}")
print(f"  2. market cap >= 500 Cr                     : {n2}  (dropped {n1-n2})")
print(f"  3. 20D avg vol >= 2,00,000 shares           : {n3}  (dropped {n2-n3})")
print(f"  4. above 200-EMA                            : {n4}  (dropped {n3-n4})")
print(f"  5. above 50-EMA                             : {n5}  (dropped {n4-n5})")
print(f"  6. remove corp-action distorted             : {n6}  (dropped {n5-n6})")
print(f"\nFINAL PASSERS: {len(out)}  ->  SCREEN_above_ema.csv")
print(f"  by exchange: {df['exchange'].value_counts().to_dict()}")
print(f"  by cap     : {df['cap_bucket'].value_counts().to_dict()}")
print(f"  small-cap (listed separately): {len(small)}  ->  SCREEN_above_ema_smallcap.csv")
print(f"\nData vintage: EOD {ohlc[list(ohlc)[0]]['date'].iloc[-1].date()} (NOT real-time)")
print("\n=== TOP 15 ===")
show = out.head(15)[["rank", "Symbol", "Exchange", "CMP", "6M Return%", "Market Cap (Cr)", "Cap", "Avg Vol (20D)"]]
print(show.to_string(index=False))
