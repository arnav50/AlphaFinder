"""PHASE 7 Stage 2: secondary validation + final risk-defined watchlist.
Outputs PHASE7_WATCHLIST.csv (final shortlist) + PHASE7_ALL_PASSERS.csv + PHASE7_SUMMARY.md"""
import pickle, time, requests, numpy as np, pandas as pd
import ta_lib_local as T, ta_smc as S, ta_vcp_gann as VG
import importlib.util
spec=importlib.util.spec_from_file_location("c11","11_candles.py"); c11=importlib.util.module_from_spec(spec)
exec(open("11_candles.py").read().split('if __name__')[0], c11.__dict__)

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
BEAR_CANDLES={"Shooting Star","Bearish Engulfing","Evening Star","Gravestone Doji","Dark Cloud Cover",
              "Bearish Pin Bar","Hanging Man","Tweezer Top","Three Black Crows","Bearish Marubozu"}
CAP=1_000_000   # example capital Rs 10,00,000 for position sizing illustration
RISK_PCT=0.01   # 1% risk per trade

def market_context():
    try:
        r=requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI",
                       params={"range":"1y","interval":"1d"},headers={"User-Agent":UA},timeout=25)
        res=r.json()["chart"]["result"][0]; c=pd.Series(res["indicators"]["quote"][0]["close"]).dropna()
        e50=T.ema(c,50).iloc[-1]; e200=T.ema(c,200).iloc[-1]; px=c.iloc[-1]
        trend="UPTREND" if px>e50>e200 else "DOWNTREND" if px<e50<e200 else "MIXED/RANGE"
        return f"Nifty 50 = {px:.0f} | EMA50 {e50:.0f} EMA200 {e200:.0f} -> {trend}", trend
    except Exception as e:
        return f"Nifty context unavailable ({e})","UNKNOWN"

def secondary(p):
    df=p["_df"].reset_index(drop=True); c=df["close"]; px=float(c.iloc[-1])
    o,h,l=df["open"],df["high"],df["low"]
    atr=float(T.atr(h,l,c).iloc[-1])
    # VCP
    vcp=VG.detect_vcp(df)
    # SMC
    struct=S.market_structure(df); zone,pos,rhi,rlo=S.premium_discount(df)
    dz=S.demand_zone(df); near_demand=bool(dz and -3<=dz["dist_pct"]<=8)
    bos,choch,_=S.bos_choch(df); bull_bos = bos and bos["dir"]=="bull"
    bob,beob=S.order_blocks(df); ob_support=bool(bob and not bob["mitigated"])
    # Gann
    g=VG.gann_angles(df); sq9=VG.gann_square9(px); above1x1=bool(g.get("above_1x1"))
    # candles last 2 bars
    last_pats=set(c11.detect_at(df,len(df)-1))|set(c11.detect_at(df,len(df)-2))
    bearish_candle=bool(last_pats & BEAR_CANDLES)
    # entry/stop/targets
    pivot=float(h.iloc[-21:-1].max())            # 20-bar prior high = breakout pivot
    entry=round(max(px,pivot),2)
    stop=round(entry-1.8*atr,2)                   # primary stop = 1.8x ATR (spec ATR option)
    base_low=round(float(l.tail(20).min()),2)     # structural stop reference (VCP base / demand low)
    risk=entry-stop
    tg1=round((np.sqrt(entry)+0.5)**2,2)         # Gann sq9 T1
    tg2=round((np.sqrt(entry)+1.0)**2,2)         # Gann sq9 T2
    obj25=round(entry*1.25,2)                     # system 25% objective
    target2=max(tg2,obj25)
    rr=round((target2-entry)/risk,2) if risk>0 else np.nan
    qty=int((RISK_PCT*CAP)/risk) if risk>0 else 0
    # secondary score (bonuses on top of prime)
    sec=0
    if vcp["vcp_quality"]!="No VCP": sec+=1
    if vcp["vcp_status"] in ("AT PIVOT (actionable)","BROKEN OUT (fresh)"): sec+=2
    if zone=="Discount" or near_demand: sec+=1
    if bull_bos: sec+=1
    if ob_support: sec+=1
    if above1x1: sec+=1
    if p.get("not_extended"): sec+=1
    phase7=p["prime_score"]+sec-(3 if bearish_candle else 0)
    return dict(vcp_quality=vcp["vcp_quality"],vcp_status=vcp["vcp_status"],
                struct=struct,pd_zone=zone,range_pos=pos,near_demand=near_demand,
                bull_bos=bool(bull_bos),ob_support=ob_support,gann_above_1x1=above1x1,
                bearish_candle=bearish_candle,last_candles=";".join(sorted(last_pats))[:60] or "none",
                atr=round(atr,2),pivot_entry=entry,stop=stop,struct_stop_ref=base_low,
                stop_pct=round((entry-stop)/entry*100,2),
                gann_T1=tg1,gann_T2=tg2,target2=target2,rr=rr,qty_per_10L=qty,
                sec_bonus=sec,phase7_score=phase7)

def get_crumb(sessn):
    for a in range(6):
        try:
            sessn.get("https://fc.yahoo.com",timeout=10)
            cr=sessn.get("https://query1.finance.yahoo.com/v1/test/getcrumb",timeout=10).text.strip()
            if cr and "Too Many" not in cr and len(cr)<20: return cr
        except Exception: pass
        time.sleep(8+4*a)   # back off until rate-limit clears
    return None

def fetch_sector(tkr,sessn,crumb):
    for a in range(3):
        try:
            r=sessn.get(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{tkr}",
                        params={"modules":"assetProfile","crumb":crumb},timeout=15)
            ap=r.json()["quoteSummary"]["result"][0].get("assetProfile",{})
            return ap.get("sector") or ap.get("industry") or "n/a"
        except Exception: time.sleep(1.5+a)
    return "n/a"

if __name__=="__main__":
    passers=pickle.load(open("prime_passers.pkl","rb"))
    ctx,trend=market_context(); print(ctx)
    rows=[]
    for p in passers:
        base={k:v for k,v in p.items() if k!="_df"}
        try: rows.append({**base, **secondary(p)})
        except Exception as e: rows.append({**base,"error":f"{type(e).__name__}:{e}"})
    allp=pd.DataFrame(rows)
    allp=allp[allp.get("phase7_score").notna()] if "phase7_score" in allp else allp
    allp=allp.sort_values(["phase7_score","rr"],ascending=[False,False]).reset_index(drop=True)
    allp.to_csv("PHASE7_ALL_PASSERS.csv",index=False)

    # FINAL watchlist gates: no bearish candle, RR>=3, valid trade levels
    wl=allp[(allp["bearish_candle"]==False)&(allp["rr"]>=3)&(allp["stop"]>0)].copy()
    wl=wl.sort_values(["phase7_score","rr"],ascending=[False,False]).head(30).reset_index(drop=True)
    # tier from phase7_score (prime 0-9 + sec 0-7 => max 16)
    wl["tier"]=np.where(wl["phase7_score"]>=13,"TIER 1",np.where(wl["phase7_score"]>=10,"TIER 2","TIER 3"))
    # sectors for the final shortlist
    sx=requests.Session(); sx.headers.update({"User-Agent":UA})
    crumb=get_crumb(sx); print("crumb ok:",bool(crumb))
    secs=[]
    for _,r in wl.iterrows():
        secs.append(fetch_sector(r["yahoo_ticker"],sx,crumb) if crumb else "n/a"); time.sleep(0.3)
    wl["sector"]=secs
    wl.insert(0,"rank",wl.index+1)
    cols=["rank","symbol","name","exchange","sector","close","vcp_status","rsi","adx","macd_hist",
          "vol_spike","pd_zone","gann_above_1x1","pivot_entry","stop","struct_stop_ref","stop_pct",
          "gann_T1","target2","rr","qty_per_10L","prime_score","sec_bonus","phase7_score","tier","last_candles"]
    wl[cols].to_csv("PHASE7_WATCHLIST.csv",index=False)
    print(f"\nStage-2 validated: {len(allp)} | FINAL watchlist (no bearish candle, RR>=3): {len(wl)}")
    print("sector breadth in watchlist:", wl["sector"].value_counts().to_dict())
    print(wl[["rank","symbol","name","close","vcp_status","rr","phase7_score","tier","sector"]].head(30).to_string(index=False))
