"""
Phase 1 / Step 1B : Fetch ~180-day daily OHLCV for every universe ticker via Yahoo chart API.
For each ticker compute:
  price_today, price_180d_ago, return_pct, avg_daily_volume(shares), avg_daily_value(Rs)
Outputs: prices.csv   (one row per ticker that returned usable data)
Robust: threaded, retries w/ backoff, host rotation, incremental checkpoint.
"""
import time, math, random, threading, datetime as dt
import requests, pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

HDR = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]

TODAY = dt.datetime.now()
TARGET_PAST = TODAY - dt.timedelta(days=180)           # rolling 180 calendar days
P1 = int((TODAY - dt.timedelta(days=230)).timestamp()) # pull a bit extra for slack
P2 = int((TODAY + dt.timedelta(days=1)).timestamp())

_local = threading.local()
def sess():
    if not hasattr(_local, "s"):
        _local.s = requests.Session(); _local.s.headers.update(HDR)
    return _local.s


def fetch_one(row):
    tkr = row["yahoo_ticker"]
    last_err = ""
    for attempt in range(4):
        host = HOSTS[attempt % len(HOSTS)]
        url = f"https://{host}/v8/finance/chart/{tkr}"
        try:
            r = sess().get(url, params={"period1": P1, "period2": P2, "interval": "1d"}, timeout=25)
            if r.status_code in (429, 999, 503):
                time.sleep(1.2 * (attempt + 1) + random.random()); last_err = f"HTTP{r.status_code}"; continue
            j = r.json()
            res = j.get("chart", {}).get("result")
            if not res:
                return {**base(row), "status": "no_data"}
            res = res[0]
            ts = res.get("timestamp")
            q = res["indicators"]["quote"][0]
            closes = q.get("close")
            vols = q.get("volume")
            if not ts or not closes:
                return {**base(row), "status": "no_data"}
            df = pd.DataFrame({"ts": ts, "close": closes, "vol": vols}).dropna(subset=["close"])
            if len(df) < 5:
                return {**base(row), "status": "too_few_bars"}
            df["date"] = pd.to_datetime(df["ts"], unit="s")
            df = df.sort_values("date")
            price_today = float(df["close"].iloc[-1])
            # bar closest to (today - 180 calendar days):
            tgt = pd.Timestamp(TARGET_PAST)
            idx = (df["date"] - tgt).abs().idxmin()
            price_past = float(df.loc[idx, "close"])
            past_date = df.loc[idx, "date"].date().isoformat()
            ret = (price_today / price_past - 1.0) * 100 if price_past > 0 else float("nan")
            df["val"] = df["close"] * df["vol"].fillna(0)
            avg_vol = float(df["vol"].fillna(0).mean())
            avg_val = float(df["val"].mean())
            return {**base(row),
                    "price_180d_ago": round(price_past, 2),
                    "past_date_used": past_date,
                    "price_today": round(price_today, 2),
                    "return_pct": round(ret, 2),
                    "avg_daily_volume": int(avg_vol),
                    "avg_daily_value_rs": int(avg_val),
                    "bars": len(df),
                    "status": "ok"}
        except Exception as e:
            last_err = f"{type(e).__name__}"
            time.sleep(0.6 * (attempt + 1))
    return {**base(row), "status": f"err:{last_err}"}


def base(row):
    return {"symbol": row["symbol"], "name": row["name"], "exchange": row["exchange"],
            "yahoo_ticker": row["yahoo_ticker"], "isin": row.get("isin", "")}


if __name__ == "__main__":
    uni = pd.read_csv("universe.csv", dtype={"symbol": str})
    rows = uni.to_dict("records")
    print(f"Fetching {len(rows)} tickers | today={TODAY.date()} | 180d target={TARGET_PAST.date()}")
    out, done = [], 0
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = {ex.submit(fetch_one, r): r for r in rows}
        for f in as_completed(futs):
            out.append(f.result()); done += 1
            if done % 250 == 0:
                ok = sum(1 for o in out if o["status"] == "ok")
                print(f"  {done}/{len(rows)} done | ok={ok}")
    res = pd.DataFrame(out)
    res.to_csv("prices.csv", index=False)
    vc = res["status"].value_counts().to_dict()
    print("DONE. status counts:", vc)
    print("rows with ok:", (res["status"] == "ok").sum())
