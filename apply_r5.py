"""
Materialise the R5 forward-scan watchlist from cached FORWARD_SCAN_METRICS.csv (no re-fetch).
R5 mandatory: 20-40% below 52wH, above 50-EMA (trend intact, pulled back), RSI 45-62,
ADX 15-32, (volume drying OR >2x spike day), base >=2wk & depth 13-32%.
Confirmations: >=3 of the 5 OHLC checks (A MACD, B CMF, C OBV, E VCP, F no-supply);
sector (D) fetched for passers and added as a 6th -> num_confirmations out of 6.
Output: FORWARD_SCAN_WATCHLIST.csv
"""
import time, requests, pandas as pd
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
HOT = {"Industrials", "Basic Materials", "Consumer Cyclical"}

m = pd.read_csv("FORWARD_SCAN_METRICS.csv", dtype={"symbol": str})
conf = m[["confA_macd", "confB_cmf", "confC_obv", "confE_vcp", "confF_no_supply"]].sum(axis=1)
mand = (m["dist_52wh_pct"].between(20, 40) & m["above_ema50"] & m["rsi"].between(45, 62)
        & m["adx"].between(15, 32) & (m["vol_drying"] | m["vol_spike10"])
        & m["weeks_base"].ge(2) & m["base_depth_pct"].between(13, 32))
p = m[mand & (conf >= 3)].copy()

s = requests.Session(); s.headers.update({"User-Agent": UA})
try:
    s.get("https://fc.yahoo.com", timeout=10)                       # cookie warmup (required for valid crumb)
    crumb = s.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10).text
except Exception: crumb = ""
def sector(yt):
    for _ in range(2):
        try:
            j = s.get(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{yt}",
                      params={"modules": "assetProfile", "crumb": crumb}, timeout=15).json()
            return j["quoteSummary"]["result"][0].get("assetProfile", {}).get("sector", "") or "n/a"
        except Exception: time.sleep(0.4)
    return "n/a"
p["sector"] = [sector(yt) for yt in p["yahoo_ticker"]]; time.sleep(0)
p["confD_sector"] = p["sector"].isin(HOT)
p["num_confirmations"] = (p[["confA_macd", "confB_cmf", "confC_obv", "confE_vcp", "confF_no_supply"]].sum(axis=1)
                          + p["confD_sector"].astype(int))
p = p.sort_values(["num_confirmations", "dist_52wh_pct"], ascending=[False, True]).reset_index(drop=True)
p.insert(0, "rank", p.index + 1)

p = p.rename(columns={"CMP": "CMP", "dist_52wh_pct": "pct_below_52wH", "rsi": "RSI", "adx": "ADX",
                      "mcap_cr": "MktCap_Cr", "next_resistance": "Next_Resistance"})
cols = ["rank", "symbol", "name", "exchange", "sector", "MktCap_Cr", "CMP", "pct_below_52wH",
        "RSI", "ADX", "weeks_base", "base_depth_pct", "num_confirmations",
        "confA_macd", "confB_cmf", "confC_obv", "confD_sector", "confE_vcp", "confF_no_supply",
        "gannG_sq9", "gannH_cycle", "Next_Resistance"]
p[[c for c in cols if c in p.columns]].to_csv("FORWARD_SCAN_WATCHLIST.csv", index=False)

print(f"R5 watchlist: {len(p)} stocks -> FORWARD_SCAN_WATCHLIST.csv")
print("confirmations distribution:", p["num_confirmations"].value_counts().sort_index(ascending=False).to_dict())
print("sector mix:", p["sector"].value_counts().to_dict())
print("\n=== R5 WATCHLIST (ranked) ===")
show = p[["rank", "symbol", "exchange", "sector", "CMP", "pct_below_52wH", "RSI", "ADX",
          "num_confirmations", "Next_Resistance"]]
print(show.to_string(index=False))
