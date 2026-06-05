"""Fetch sector/industry for the 312 final hits (Yahoo quoteSummary assetProfile, crumb auth)
   and write the final, output-format CSV + markdown."""
import time, requests, pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
s = requests.Session(); s.headers.update({"User-Agent": UA})
s.get("https://fc.yahoo.com", timeout=10)
CRUMB = s.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10).text

def profile(tkr):
    for a in range(3):
        try:
            r = s.get(f"https://query{1+a%2}.finance.yahoo.com/v10/finance/quoteSummary/{tkr}",
                      params={"modules": "assetProfile", "crumb": CRUMB}, timeout=20)
            if r.status_code in (429, 503): time.sleep(1+a); continue
            ap = r.json()["quoteSummary"]["result"][0].get("assetProfile", {})
            return ap.get("sector") or "", ap.get("industry") or ""
        except Exception:
            time.sleep(0.4*(a+1))
    return "", ""

f = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
f["yahoo_ticker"] = f.apply(lambda r: f"{r['symbol']}.NS" if r["exchange"] == "NSE" else f"{r['symbol']}.BO", axis=1)
secs, inds = [], []
for i, r in f.iterrows():
    se, ind = profile(r["yahoo_ticker"])
    secs.append(se); inds.append(ind)
    time.sleep(0.05)
    if (i+1) % 60 == 0: print(f"  {i+1}/{len(f)}")
f["sector"] = secs
f["industry"] = inds
# BSE-only fallback note where blank
f["sector"] = f["sector"].replace("", "n/a")
f.to_csv("FINAL_universe_25pct.csv", index=False)
print("sector coverage:", (f["sector"] != "n/a").sum(), "/", len(f))
print(f["sector"].value_counts().head(15).to_string())
