"""
Phase 1 / Step 1B-1C : Apply scan filters + enrich with market cap & sector.
Filters:
  - status ok
  - return_pct >= 25
  - liquidity: avg_daily_volume >= 50,000 shares  OR  avg_daily_value >= Rs 50 lakh (5e6)
  - penny flag: price_today < 10  -> FLAG (kept, per spec "flag but do not remove")
Enrichment (market cap in Rs cr + sector) via BSE master joined on ISIN -> covers NSE & BSE rows.
Output: hits_enriched.csv
"""
import requests, pandas as pd

HDR = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Referer": "https://www.bseindia.com/"}
LAKH = 100000

def bse_master():
    url = ("https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w"
           "?Group=&Scripcode=&industry=&segment=Equity&status=Active")
    df = pd.DataFrame(requests.get(url, headers=HDR, timeout=40).json())
    df["isin"] = df["ISIN_NUMBER"].astype(str).str.strip().str.upper()
    df["mktcap_cr"] = pd.to_numeric(df["Mktcap"], errors="coerce")
    df["sector"] = df["INDUSTRY"].astype(str).str.strip().replace({"None": "", "nan": ""})
    return df[["isin", "mktcap_cr", "sector"]].dropna(subset=["isin"]).query("isin.str.startswith('IN')") \
             .sort_values("mktcap_cr", ascending=False).drop_duplicates("isin")

if __name__ == "__main__":
    px = pd.read_csv("prices.csv", dtype={"symbol": str})
    ok = px[px["status"] == "ok"].copy()
    print(f"ok rows: {len(ok)}")

    hits = ok[ok["return_pct"] >= 25].copy()
    print(f">=25% return: {len(hits)}")

    liq = (hits["avg_daily_volume"] >= 50000) | (hits["avg_daily_value_rs"] >= 50 * LAKH)
    dropped_liq = (~liq).sum()
    hits = hits[liq].copy()
    print(f"after liquidity filter (>=50k sh OR >=Rs50L val): {len(hits)} (dropped {dropped_liq})")

    hits["penny_flag"] = hits["price_today"] < 10

    # Enrich market cap + sector via BSE master (ISIN join)
    hits["isin_norm"] = hits["isin"].astype(str).str.strip().str.upper()
    try:
        bm = bse_master()
        hits = hits.merge(bm, left_on="isin_norm", right_on="isin", how="left", suffixes=("", "_bse"))
        print(f"market cap matched: {hits['mktcap_cr'].notna().sum()}/{len(hits)}")
    except Exception as e:
        print("BSE enrich failed:", e); hits["mktcap_cr"] = pd.NA; hits["sector"] = ""

    def cap_bucket(cr):
        if pd.isna(cr): return "n/a"
        if cr >= 20000: return "Large"
        if cr >= 5000: return "Mid"
        if cr >= 500: return "Small"
        return "Micro"
    hits["cap_bucket"] = hits["mktcap_cr"].apply(cap_bucket)

    hits = hits.sort_values("return_pct", ascending=False).reset_index(drop=True)
    cols = ["symbol", "name", "exchange", "price_180d_ago", "past_date_used", "price_today",
            "return_pct", "mktcap_cr", "cap_bucket", "sector", "avg_daily_volume",
            "avg_daily_value_rs", "penny_flag", "isin_norm", "yahoo_ticker"]
    hits[cols].to_csv("hits_enriched.csv", index=False)
    print(f"\nFINAL HITS: {len(hits)} | penny-flagged: {hits['penny_flag'].sum()}")
    print("by exchange:", hits["exchange"].value_counts().to_dict())
    print("by cap:", hits["cap_bucket"].value_counts().to_dict())
    print("\nTop 15 by return%:")
    print(hits[["symbol","name","exchange","price_180d_ago","price_today","return_pct","cap_bucket"]].head(15).to_string(index=False))
