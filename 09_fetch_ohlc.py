"""Phase 2 data: fetch ~500 calendar days of daily OHLCV for each Phase-1 stock.
Saves ohlc.pkl  ->  {symbol: DataFrame[date,open,high,low,close,volume]}  (enough bars for EMA200/Ichimoku52)."""
import time, threading, pickle, datetime as dt
import requests, pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]
NOW = dt.datetime.now()
P1 = int((NOW - dt.timedelta(days=520)).timestamp())
P2 = int((NOW + dt.timedelta(days=1)).timestamp())

_l = threading.local()
def sess():
    if not hasattr(_l, "s"):
        _l.s = requests.Session(); _l.s.headers.update({"User-Agent": UA})
    return _l.s

def fetch(row):
    sym, tkr = row["symbol"], row["yahoo_ticker"]
    for a in range(4):
        try:
            r = sess().get(f"https://{HOSTS[a%2]}/v8/finance/chart/{tkr}",
                           params={"period1": P1, "period2": P2, "interval": "1d"}, timeout=30)
            if r.status_code in (429, 503, 999): time.sleep(1+a); continue
            res = r.json()["chart"]["result"][0]
            q = res["indicators"]["quote"][0]
            df = pd.DataFrame({"date": pd.to_datetime(res["timestamp"], unit="s"),
                               "open": q["open"], "high": q["high"], "low": q["low"],
                               "close": q["close"], "volume": q["volume"]}).dropna(subset=["close"])
            df = df.sort_values("date").reset_index(drop=True)
            return sym, df
        except Exception:
            time.sleep(0.5*(a+1))
    return sym, None

if __name__ == "__main__":
    f = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
    f["yahoo_ticker"] = f.apply(lambda r: f"{r['symbol']}.NS" if r["exchange"]=="NSE" else f"{r['symbol']}.BO", axis=1)
    rows = f.to_dict("records")
    data, done, fail = {}, 0, []
    with ThreadPoolExecutor(max_workers=20) as ex:
        futs = [ex.submit(fetch, r) for r in rows]
        for fu in as_completed(futs):
            sym, df = fu.result(); done += 1
            if df is not None and len(df) >= 60: data[sym] = df
            else: fail.append(sym)
            if done % 80 == 0: print(f"  {done}/{len(rows)} | ok={len(data)}")
    pickle.dump(data, open("ohlc.pkl", "wb"))
    bars = pd.Series({k: len(v) for k, v in data.items()})
    print(f"DONE. stocks with usable OHLC: {len(data)} | failed/short: {len(fail)}")
    print(f"bars per stock: min={bars.min()} median={int(bars.median())} max={bars.max()}")
    if fail: print("short/failed:", fail[:20])
