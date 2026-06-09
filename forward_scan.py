"""
FORWARD SCAN — apply the mode-B prime filter to the full NSE+BSE universe.
Reuses 22-style 1y OHLC fetch. Pre-filters on prices.csv (fresh, full universe) for
price/volume, joins BSE-master market cap, then fetches OHLC only for survivors and
computes every mandatory + confirmation + Gann check from the user's spec.

Prime ranges (Phase-3): RSI sweet 63-70 (V1 literal) / 45-62 (V2 coherent base);
ADX 18-28; CMF>0; base 2-7 wk, depth 13-32%; 20-40% below 52w high.

Outputs: FORWARD_SCAN_METRICS.csv (all candidates) + FORWARD_SCAN_V1.csv + FORWARD_SCAN_V2.csv
"""
import pickle, time, threading, numpy as np, pandas as pd, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import ta_lib_local as T, ta_smc as S, ta_vcp_gann as VG

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]
HOT_SECTORS = {"Industrials", "Basic Materials", "Consumer Cyclical"}   # top-3 by Phase-1 winner count
_l = threading.local()
def sess():
    if not hasattr(_l, "s"): _l.s = requests.Session(); _l.s.headers.update({"User-Agent": UA})
    return _l.s

def fetch(tkr):
    for a in range(3):
        try:
            r = sess().get(f"https://{HOSTS[a%2]}/v8/finance/chart/{tkr}",
                           params={"range": "1y", "interval": "1d"}, timeout=25)
            if r.status_code != 200: time.sleep(0.8 + a); continue
            res = r.json()["chart"]["result"][0]; q = res["indicators"]["quote"][0]
            return pd.DataFrame({"date": pd.to_datetime(res["timestamp"], unit="s"), "open": q["open"],
                "high": q["high"], "low": q["low"], "close": q["close"], "volume": q["volume"]}) \
                .dropna(subset=["close"]).sort_values("date").reset_index(drop=True)
        except Exception: time.sleep(0.5 * (a + 1))
    return None

def metrics(row):
    df = fetch(row["yahoo_ticker"])
    if df is None or len(df) < 200: return None
    o, h, l, c, v = (df[x] for x in ["open", "high", "low", "close", "volume"])
    px = float(c.iloc[-1])
    if px < 10: return None
    rsi = T.rsi(c).iloc[-1]
    adxv, pdi, mdi = T.adx(h, l, c); adx = adxv.iloc[-1]
    ml, ms, hist = T.macd(c)
    e200 = T.ema(c, 200).iloc[-1]; e50 = T.ema(c, 50).iloc[-1]
    obv = T.obv(c, v)
    mfm = (((c - l) - (h - c)) / (h - l).replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0)
    cmf = ((mfm * v).rolling(20, min_periods=10).sum() / v.rolling(20, min_periods=10).sum().replace(0, np.nan)).iloc[-1]
    hi52 = float(h.tail(252).max()); dist52 = (hi52 - px) / hi52 * 100 if hi52 > 0 else np.nan
    v20 = v.tail(20).mean(); v50 = v.tail(50).mean()
    spike10 = bool((v.tail(10) > 2 * v50).any()) if v50 > 0 else False
    drying = bool(v20 <= v50 * 1.05)
    # base over last 40 bars
    base_hi = float(h.tail(40).max()); base_lo = float(l.tail(40).min())
    base_depth = (base_hi - base_lo) / base_hi * 100 if base_hi > 0 else np.nan
    bars_since_high = len(c) - 1 - int(h.tail(40).reset_index(drop=True).idxmax()) + (len(c) - 40 if len(c) > 40 else 0)
    weeks_base = round(bars_since_high / 5, 1)
    # confirmations
    A = bool(hist.iloc[-1] < 0 and hist.iloc[-1] > hist.iloc[-6])                  # MACD neg but improving
    B = bool(pd.notna(cmf) and cmf > 0)                                           # CMF > 0
    C = bool(obv.iloc[-1] > obv.iloc[-20] and px <= float(c.iloc[-20]) * 1.03)    # OBV up, price flat/down
    vcp = VG.detect_vcp(df)
    E = bool(vcp["num_contractions"] >= 2 and (vcp["vdu_confirmed"] or vcp["depths_decreasing"]))
    sz = S.supply_zone(df)
    F = bool(sz is None or sz.get("dist_pct", 99) > 10)                           # no supply within 10% above
    # gann bonus
    sq9 = VG.gann_square9(px); g = VG.gann_angles(df)
    G = bool(min(abs(px - lvl) / px * 100 for lvl in sq9.values()) <= 5)
    H = bool(VG.gann_time_cycles(g.get("days_since_low", 0))["near_gann_cycle"])
    # next resistance = nearest swing high above px, else 52w high
    shi, _ = T.swings(c, 3)
    overhead = [float(h.iloc[i]) for i in shi if h.iloc[i] > px * 1.005]
    next_res = round(min(overhead), 2) if overhead else round(hi52, 2)
    return {"symbol": str(row["symbol"]), "name": row["name"], "exchange": row["exchange"],
            "CMP": round(px, 2), "dist_52wh_pct": round(dist52, 2), "rsi": round(float(rsi), 1),
            "adx": round(float(adx), 1) if pd.notna(adx) else np.nan,
            "above_ema200": bool(pd.notna(e200) and px > e200), "above_ema50": bool(pd.notna(e50) and px > e50),
            "vol_drying": drying, "vol_spike10": spike10, "base_depth_pct": round(base_depth, 1),
            "weeks_base": weeks_base, "cmf": round(float(cmf), 3) if pd.notna(cmf) else np.nan,
            "macd_hist": round(float(hist.iloc[-1]), 3),
            "confA_macd": A, "confB_cmf": B, "confC_obv": C, "confE_vcp": E, "confF_no_supply": F,
            "gannG_sq9": G, "gannH_cycle": H, "next_resistance": next_res,
            "vcp_contractions": vcp["num_contractions"]}

def sector_for(row):
    try:
        s = sess()
        cr = s.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=10).text
        j = s.get(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{row['yahoo_ticker']}",
                  params={"modules": "assetProfile", "crumb": cr}, timeout=15).json()
        return j["quoteSummary"]["result"][0].get("assetProfile", {}).get("sector", "") or "n/a"
    except Exception:
        return "n/a"

if __name__ == "__main__":
    uni = pd.read_csv("universe.csv", dtype={"symbol": str})
    px = pd.read_csv("prices.csv", dtype={"symbol": str})
    px = px[px["status"] == "ok"]
    liquid = px[(px["price_today"] >= 10) & (px["avg_daily_volume"] >= 100000)]["symbol"]
    cand = uni[uni["symbol"].isin(set(liquid))].copy()
    # market cap via BSE master (ISIN join)
    try:
        H = {"User-Agent": UA, "Referer": "https://www.bseindia.com/"}
        bm = pd.DataFrame(requests.get("https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w"
              "?Group=&Scripcode=&industry=&segment=Equity&status=Active", headers=H, timeout=40).json())
        bm["isin"] = bm["ISIN_NUMBER"].astype(str).str.strip().str.upper()
        bm["mcap"] = pd.to_numeric(bm["Mktcap"], errors="coerce")
        cap = bm.dropna(subset=["isin"]).sort_values("mcap", ascending=False).drop_duplicates("isin").set_index("isin")["mcap"]
        cand["isin_n"] = cand["isin"].astype(str).str.strip().str.upper()
        cand["mcap_cr"] = cand["isin_n"].map(cap)
    except Exception as e:
        print("mcap join failed:", e); cand["mcap_cr"] = np.nan
    before = len(cand)
    cand = cand[(cand["mcap_cr"] >= 500) | (cand["mcap_cr"].isna())]   # keep >=500cr or unknown (flagged)
    print(f"universe {len(uni)} -> liquid (>=Rs10 & >=1L vol) {len(set(liquid))} -> mcap>=500/unknown {len(cand)} (from {before})")

    rows = cand.to_dict("records")
    out = []
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = [ex.submit(metrics, r) for r in rows]
        done = 0
        for f in as_completed(futs):
            done += 1; r = f.result()
            if r: out.append(r)
            if done % 300 == 0: print(f"  fetched {done}/{len(rows)} | computed {len(out)}")
    m = cand[["symbol", "mcap_cr", "yahoo_ticker"]].merge(pd.DataFrame(out), on="symbol", how="right")
    m.to_csv("FORWARD_SCAN_METRICS.csv", index=False)
    print(f"\nmetrics computed for {len(m)} stocks -> FORWARD_SCAN_METRICS.csv")

    def mandatory(d, rsi_lo, rsi_hi):
        return (d["dist_52wh_pct"].between(20, 40) & d["above_ema200"] &
                d["rsi"].between(rsi_lo, rsi_hi) & d["adx"].between(18, 28) &
                d["vol_drying"] & d["vol_spike10"] &
                d["weeks_base"].ge(2) & d["base_depth_pct"].between(13, 32))
    conf_ohlc = m[["confA_macd", "confB_cmf", "confC_obv", "confE_vcp", "confF_no_supply"]].sum(axis=1)

    for tag, lo, hi in [("V1", 63, 70), ("V2", 45, 62)]:
        prov = m[mandatory(m, lo, hi) & (conf_ohlc >= 3)].copy()
        # fetch sector (D) only for provisional passers
        prov["sector"] = [sector_for({"yahoo_ticker": yt}) for yt in prov["yahoo_ticker"]]
        prov["confD_sector"] = prov["sector"].isin(HOT_SECTORS)
        prov["num_confirmations"] = (prov[["confA_macd","confB_cmf","confC_obv","confE_vcp","confF_no_supply"]].sum(axis=1)
                                     + prov["confD_sector"].astype(int))
        passers = prov[prov["num_confirmations"] >= 4].sort_values(
            ["num_confirmations", "dist_52wh_pct"], ascending=[False, True]).reset_index(drop=True)
        passers.insert(0, "rank", passers.index + 1)
        cols = ["rank", "symbol", "name", "exchange", "sector", "CMP", "dist_52wh_pct", "rsi", "adx",
                "mcap_cr", "weeks_base", "base_depth_pct", "num_confirmations",
                "confA_macd", "confB_cmf", "confC_obv", "confD_sector", "confE_vcp", "confF_no_supply",
                "gannG_sq9", "gannH_cycle", "next_resistance"]
        passers[[c for c in cols if c in passers.columns]].to_csv(f"FORWARD_SCAN_{tag}.csv", index=False)
        print(f"\n=== {tag} (RSI {lo}-{hi}) : {len(passers)} passers (mandatory ALL + >=4 confirmations) ===")
        if len(passers):
            print(passers.head(20)[["rank","symbol","exchange","CMP","dist_52wh_pct","rsi","adx","num_confirmations","next_resistance"]].to_string(index=False))
