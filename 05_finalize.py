"""
Phase 1 / Step 1D (final hardening) for the 317 hits:
  1. ROBUST return: re-fetch full series, compute return using a 5-bar MEDIAN window
     centered on 'today' and on 'today-180d' -> immune to isolated bad prints.
  2. INDEPENDENT current price: warmed sequential NSE quote API + BSE quote API
     as a 2nd source vs Yahoo; compute mismatch%.
Output: hits_final.csv  (sorted by robust return desc)
"""
import time, datetime as dt, requests, pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
TODAY = dt.datetime.now(); TARGET = pd.Timestamp(TODAY - dt.timedelta(days=180))
P1 = int((TODAY - dt.timedelta(days=230)).timestamp()); P2 = int((TODAY + dt.timedelta(days=1)).timestamp())

ysess = requests.Session(); ysess.headers.update({"User-Agent": UA})

def robust_return(tkr):
    for a in range(4):
        try:
            r = ysess.get(f"https://query{1+a%2}.finance.yahoo.com/v8/finance/chart/{tkr}",
                          params={"period1": P1, "period2": P2, "interval": "1d"}, timeout=25)
            if r.status_code in (429, 503, 999): time.sleep(1+a); continue
            res = r.json()["chart"]["result"][0]
            df = pd.DataFrame({"d": pd.to_datetime(res["timestamp"], unit="s"),
                               "c": res["indicators"]["quote"][0]["close"]}).dropna().sort_values("d").reset_index(drop=True)
            if len(df) < 5: return (float("nan"),)*3
            now_med = float(df["c"].tail(5).median())                       # last 5 bars
            tpos = (df["d"] - TARGET).abs().idxmin()
            lo, hi = max(0, tpos-2), min(len(df), tpos+3)
            past_med = float(df["c"].iloc[lo:hi].median())                  # +-2 bars around target
            ret = (now_med/past_med - 1)*100 if past_med > 0 else float("nan")
            return round(ret, 2), round(now_med, 2), round(past_med, 2)
        except Exception:
            time.sleep(0.5*(a+1))
    return (float("nan"),)*3

# warmed sequential live-price 2nd source
nse = requests.Session(); nse.headers.update({"User-Agent": UA, "Accept": "application/json",
        "Referer": "https://www.nseindia.com/get-quotes/equity", "Accept-Language": "en-US,en;q=0.9"})
def warm_nse():
    try:
        nse.get("https://www.nseindia.com/", timeout=12)
        nse.get("https://www.nseindia.com/get-quotes/equity?symbol=RELIANCE", timeout=12)
    except Exception: pass
def nse_live(sym):
    try:
        j = nse.get(f"https://www.nseindia.com/api/quote-equity?symbol={sym}", timeout=15).json()
        return float(j["priceInfo"]["lastPrice"])
    except Exception: return float("nan")
bse = requests.Session(); bse.headers.update({"User-Agent": UA, "Referer": "https://www.bseindia.com/"})
def bse_live(code):
    try:
        j = bse.get(f"https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w?scripcode={code}&seriesid=", timeout=15).json()
        return float(j["CurrRate"]["LTP"])
    except Exception: return float("nan")

if __name__ == "__main__":
    hits = pd.read_csv("hits_enriched.csv", dtype={"symbol": str})
    warm_nse(); time.sleep(1)
    rob, rnow, rpast, live = [], [], [], []
    for i, row in hits.iterrows():
        rr, nn, pp = robust_return(row["yahoo_ticker"])
        rob.append(rr); rnow.append(nn); rpast.append(pp)
        if row["exchange"] == "NSE":
            lv = nse_live(str(row["symbol"])); time.sleep(0.25)
        else:
            lv = bse_live(str(row["symbol"]))
        live.append(lv)
        if (i+1) % 40 == 0: print(f"  {i+1}/{len(hits)} | last {row['symbol']} live={lv}")
    hits["robust_return_pct"] = rob
    hits["robust_now"] = rnow
    hits["robust_past"] = rpast
    hits["live_today_2ndsrc"] = live
    hits["price_mismatch_pct"] = ((hits["price_today"] - hits["live_today_2ndsrc"]).abs() /
                                  hits["live_today_2ndsrc"] * 100).round(2)
    hits["return_delta_raw_vs_robust"] = (hits["return_pct"] - hits["robust_return_pct"]).abs().round(2)
    hits["robust_below_25"] = hits["robust_return_pct"] < 25
    hits = hits.sort_values("robust_return_pct", ascending=False).reset_index(drop=True)
    hits.to_csv("hits_final.csv", index=False)
    print("\n=== FINAL HARDENING SUMMARY ===")
    print(f"total hits: {len(hits)}")
    print(f"robust return < 25% (drop): {hits['robust_below_25'].sum()}")
    print(f"raw-vs-robust gap > 5pt:    {(hits['return_delta_raw_vs_robust']>5).sum()}")
    print(f"live 2nd-source price available: {hits['live_today_2ndsrc'].notna().sum()}/{len(hits)}")
    avail = hits[hits['live_today_2ndsrc'].notna()]
    print(f"  of those, price mismatch >5%: {(avail['price_mismatch_pct']>5).sum()}  | median mismatch {avail['price_mismatch_pct'].median():.2f}%")
