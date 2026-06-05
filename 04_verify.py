"""
Phase 1 / Step 1D : Cross-verification of the 317 hits.
Method (2 independent checks per stock):
  CHECK A - Event-adjusted return: re-fetch chart with events=div|split and recompute return
            from ADJUSTED close (the true split/bonus-adjusted price return).
  CHECK B - Independent current price: pull live quote from NSE (.NS) / BSE (.BO) quote APIs
            and compare to Yahoo price_today.
Flags:
  - corp_action  : |raw_return - adj_return| > 8 absolute pts  (bonus/split/dividend skew)
  - price_mismatch: |yahoo_today - live_today| / live_today > 5%
  - adj_below_25 : adjusted return < 25  (would fall out of universe on the verified metric)
Output: hits_verified.csv
"""
import time, threading, datetime as dt, requests, pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]
TODAY = dt.datetime.now(); TARGET = pd.Timestamp(TODAY - dt.timedelta(days=180))
P1 = int((TODAY - dt.timedelta(days=230)).timestamp()); P2 = int((TODAY + dt.timedelta(days=1)).timestamp())

_l = threading.local()
def sess():
    if not hasattr(_l, "s"):
        s = requests.Session(); s.headers.update({"User-Agent": UA}); _l.s = s
    return _l.s

def adj_return(tkr):
    for a in range(4):
        try:
            r = sess().get(f"https://{HOSTS[a%2]}/v8/finance/chart/{tkr}",
                           params={"period1": P1, "period2": P2, "interval": "1d",
                                   "events": "div,splits"}, timeout=25)
            if r.status_code in (429, 503, 999): time.sleep(1+a); continue
            res = r.json()["chart"]["result"][0]
            ts = res["timestamp"]; ind = res["indicators"]
            adj = ind.get("adjclose", [{}])[0].get("adjclose")
            close = ind["quote"][0]["close"]
            df = pd.DataFrame({"ts": ts, "adj": adj, "close": close}).dropna(subset=["close"])
            df["date"] = pd.to_datetime(df["ts"], unit="s"); df = df.sort_values("date")
            if adj is None: df["adj"] = df["close"]
            df = df.dropna(subset=["adj"])
            idx = (df["date"] - TARGET).abs().idxmin()
            a_now, a_past = float(df["adj"].iloc[-1]), float(df.loc[idx, "adj"])
            return round((a_now/a_past - 1)*100, 2) if a_past > 0 else float("nan")
        except Exception:
            time.sleep(0.5*(a+1))
    return float("nan")

def live_price(row):
    tkr, ex, sym = row["yahoo_ticker"], row["exchange"], str(row["symbol"])
    try:
        if ex == "NSE":
            s = sess()
            s.get("https://www.nseindia.com", timeout=10)
            j = s.get(f"https://www.nseindia.com/api/quote-equity?symbol={sym}",
                      headers={"Referer": "https://www.nseindia.com/", "Accept": "application/json"},
                      timeout=15).json()
            return float(j["priceInfo"]["lastPrice"])
        else:
            j = sess().get(f"https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w?scripcode={sym}&seriesid=",
                           headers={"Referer": "https://www.bseindia.com/"}, timeout=15).json()
            return float(j["CurrRate"]["LTP"])
    except Exception:
        return float("nan")

def work(row):
    out = dict(row)
    out["adj_return_pct"] = adj_return(row["yahoo_ticker"])
    out["live_today"] = live_price(row)
    return out

if __name__ == "__main__":
    hits = pd.read_csv("hits_enriched.csv", dtype={"symbol": str}).to_dict("records")
    print(f"Verifying {len(hits)} hits (adjusted return + live price)...")
    res = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(work, r) for r in hits]
        for i, f in enumerate(as_completed(futs), 1):
            res.append(f.result())
            if i % 50 == 0: print(f"  {i}/{len(hits)}")
    df = pd.DataFrame(res)
    df["raw_vs_adj_gap"] = (df["return_pct"] - df["adj_return_pct"]).abs().round(2)
    df["corp_action"] = df["raw_vs_adj_gap"] > 8
    df["price_mismatch_pct"] = ((df["price_today"] - df["live_today"]).abs() / df["live_today"] * 100).round(2)
    df["price_mismatch"] = df["price_mismatch_pct"] > 5
    df["adj_below_25"] = df["adj_return_pct"] < 25
    df = df.sort_values("return_pct", ascending=False).reset_index(drop=True)
    df.to_csv("hits_verified.csv", index=False)
    print("\n=== VERIFICATION SUMMARY ===")
    print(f"corp_action flagged (raw vs adj gap > 8pt): {df['corp_action'].sum()}")
    print(f"price_mismatch flagged (>5% vs live):       {df['price_mismatch'].sum()} (live price unavailable for {df['live_today'].isna().sum()})")
    print(f"adjusted return < 25% (fall out):           {df['adj_below_25'].sum()}")
    print("\nTop 15 (raw vs adjusted return, live price):")
    print(df[["symbol","name","exchange","price_today","live_today","return_pct","adj_return_pct","corp_action","price_mismatch"]].head(15).to_string(index=False))
