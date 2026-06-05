"""PHASE 7 — Prime Filter Scanner (forward-looking).
Filter constants DERIVED FROM PHASE 5 Day-0 fingerprint (see PRIME dict).
Stage 1: scan full NSE+BSE universe (fetch 1y OHLC, compute indicators, apply prime filter).
Stage 2: secondary validation (VCP/SMC/Gann/candles) + entry/stop/targets on passers.
Outputs: PHASE7_WATCHLIST.csv, prime_backtest.txt"""
import pickle, time, threading, datetime as dt, numpy as np, pandas as pd, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import ta_lib_local as T, ta_smc as S, ta_vcp_gann as VG
import importlib.util
spec=importlib.util.spec_from_file_location("c11","11_candles.py"); c11=importlib.util.module_from_spec(spec)
exec(open("11_candles.py").read().split('if __name__')[0], c11.__dict__)

# ===== PRIME FILTER (from Phase 5 fingerprint; breakout-initiation profile) =====
PRIME = dict(RSI_MIN=55, RSI_MAX=75, ADX_MIN=18, ADX_MAX=30,
             VOL_SPIKE=1.5,          # max vol last 5d / 50d-sma  (Phase5 Day0 median 3.3x, Q25 1.9x)
             EMA200_MAX_EXT=1.20,    # price not >20% above EMA200 (Phase5 median +3.4%)
             DIST_52WH_LO=-0.35, DIST_52WH_HI=-0.03,   # Phase5 Q25..Q75 ~ -28%..-4.5%
             MIN_ADV_VALUE=2e7,      # >= Rs 2 cr/day traded value (liquidity for a tradeable list)
             MIN_PRICE=10)

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
HOSTS=["query1.finance.yahoo.com","query2.finance.yahoo.com"]
_l=threading.local()
def sess():
    if not hasattr(_l,"s"): _l.s=requests.Session(); _l.s.headers.update({"User-Agent":UA})
    return _l.s

def fetch(tkr):
    for a in range(3):
        try:
            r=sess().get(f"https://{HOSTS[a%2]}/v8/finance/chart/{tkr}",params={"range":"1y","interval":"1d"},timeout=25)
            if r.status_code!=200: time.sleep(0.8+a); continue
            res=r.json()["chart"]["result"][0]; q=res["indicators"]["quote"][0]
            df=pd.DataFrame({"date":pd.to_datetime(res["timestamp"],unit="s"),"open":q["open"],
                "high":q["high"],"low":q["low"],"close":q["close"],"volume":q["volume"]}).dropna(subset=["close"]).sort_values("date").reset_index(drop=True)
            return df
        except Exception: time.sleep(0.5*(a+1))
    return None

def prime_pass(df):
    if df is None or len(df)<60: return None
    o,h,l,c,v=(df[x] for x in ["open","high","low","close","volume"])
    px=float(c.iloc[-1])
    if px<PRIME["MIN_PRICE"]: return None
    adv=float((c*v).tail(50).mean())
    if adv<PRIME["MIN_ADV_VALUE"]: return None
    rsi=T.rsi(c).iloc[-1]
    ml,ms,hist=T.macd(c)
    adxv,pdi,mdi=T.adx(h,l,c); adx=adxv.iloc[-1]
    e20=T.ema(c,20).iloc[-1]; e50=T.ema(c,50).iloc[-1]; e200=T.ema(c,200).iloc[-1]
    st,sd=T.supertrend(h,l,c)
    obv=T.obv(c,v); obv_up=np.polyfit(range(10),obv.tail(10).values,1)[0]>0
    sma50v=v.tail(50).mean(); volspike=float(v.tail(5).max()/sma50v) if sma50v>0 else 0
    hi52=float(h.tail(252).max()); dist52=(px/hi52-1)
    checks=dict(
        rsi=PRIME["RSI_MIN"]<=rsi<=PRIME["RSI_MAX"],
        macd=(hist.iloc[-1]>0) and (ml.iloc[-1]>ms.iloc[-1]),
        adx=pd.notna(adx) and PRIME["ADX_MIN"]<=adx<=PRIME["ADX_MAX"],
        vol=volspike>=PRIME["VOL_SPIKE"],
        st=sd.iloc[-1]==1,
        obv=bool(obv_up),
        ema20_50=pd.notna(e50) and e20>e50,
        px_ema200=pd.notna(e200) and px>e200,
        dist52=PRIME["DIST_52WH_LO"]<=dist52<=PRIME["DIST_52WH_HI"],
    )
    prime_score=int(sum(checks.values()))
    not_extended=pd.notna(e200) and px<=e200*PRIME["EMA200_MAX_EXT"]
    return dict(close=round(px,2),rsi=round(float(rsi),1),adx=round(float(adx),1),
                macd_hist=round(float(hist.iloc[-1]),3),vol_spike=round(volspike,2),
                dist_52wh_pct=round(dist52*100,2),adv_value_cr=round(adv/1e7,2),
                atr_pct=round(float(T.atr(h,l,c).iloc[-1]/px*100),2),
                prime_score=prime_score, not_extended=bool(not_extended),
                checks="".join("1" if checks[k] else "0" for k in
                       ["rsi","macd","adx","vol","st","obv","ema20_50","px_ema200","dist52"]))

THRESHOLD=6   # confluence-count threshold (76% recall on known winners; balances recall/precision)
def worker(row):
    df=fetch(row["yahoo_ticker"])
    m=prime_pass(df)
    if m is None or m["prime_score"]<THRESHOLD: return None
    return {"symbol":str(row["symbol"]),"name":row["name"],"exchange":row["exchange"],
            "yahoo_ticker":row["yahoo_ticker"], **m, "_df":df}

# ---------- in-sample backtest: apply prime filter to known winners at their Day-0 ----------
def backtest():
    d=pd.read_csv("PHASE5_DAY0.csv"); d=d[d["rsi"].notna()].copy()
    score=( d["rsi"].between(PRIME["RSI_MIN"],PRIME["RSI_MAX"]).astype(int)
          + ((d["macd_hist"]>0)&(d["macd"]>d["macd_signal"])).astype(int)
          + d["adx"].between(PRIME["ADX_MIN"],PRIME["ADX_MAX"]).astype(int)
          + (d["day0_vol_x_50davg"]>=PRIME["VOL_SPIKE"]).astype(int)
          + (d["supertrend"]=="green").astype(int)
          + d["obv_dir"].isin(["already_rising","turning_up"]).astype(int)
          + (d["ema20"]>d["ema50"]).astype(int)
          + (d["pct_vs_ema200"]>0).astype(int)
          + d["pct_from_52wh"].between(PRIME["DIST_52WH_LO"]*100,PRIME["DIST_52WH_HI"]*100).astype(int) )
    return (score>=THRESHOLD).mean()*100, len(d), int((score>=THRESHOLD).sum())

if __name__=="__main__":
    rec,ntot,npass=backtest()
    bt=(f"PRIME FILTER constants (from Phase 5): {PRIME}\n"
        f"Confluence threshold: prime_score >= {THRESHOLD} of 9 criteria.\n"
        f"In-sample backtest: applied prime filter to {ntot} known 25%+ winners AT their Day-0 bar.\n"
        f"  -> {npass}/{ntot} ({rec:.1f}%) would have been flagged at initiation (RECALL).\n"
        f"  (In-sample: bands derived from these same Day-0s; this is recall/consistency, not out-of-sample.)\n")
    open("prime_backtest.txt","w").write(bt); print(bt)

    uni=pd.read_csv("universe.csv",dtype={"symbol":str})
    rows=uni.to_dict("records")
    print(f"Scanning {len(rows)} NSE+BSE tickers with the prime filter...")
    passers=[]
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs=[ex.submit(worker,r) for r in rows]
        done=0
        for f in as_completed(futs):
            done+=1
            r=f.result()
            if r: passers.append(r)
            if done%400==0: print(f"  {done}/{len(rows)} | passers so far: {len(passers)}")
    print(f"\nStage-1 prime-filter passers: {len(passers)}")
    pickle.dump(passers, open("prime_passers.pkl","wb"))
    # quick dump without _df
    pd.DataFrame([{k:v for k,v in p.items() if k!='_df'} for p in passers]).to_csv("prime_passers.csv",index=False)
    print("saved prime_passers.pkl / .csv")
