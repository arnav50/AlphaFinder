"""Phase 5A-5C: locate Day 0 (move start) per stock and snapshot ALL indicators there + pre-context.
Output: PHASE5_DAY0.csv"""
import pickle, numpy as np, pandas as pd
import ta_lib_local as T
import importlib.util
# import candlestick detector
spec = importlib.util.spec_from_file_location("c11","11_candles.py"); c11=importlib.util.module_from_spec(spec)
src=open("11_candles.py").read().split('if __name__')[0]; exec(src, c11.__dict__)

def series(df):
    o,h,l,c,v=(df[x] for x in ["open","high","low","close","volume"])
    rsi=T.rsi(c); k,d=T.stoch(h,l,c); mid,ub,lb,bw=T.bollinger(c)
    pctB=(c-lb)/(ub-lb)*100
    macd,sig,hist=T.macd(c); e20,e50,e200=T.ema(c,20),T.ema(c,50),T.ema(c,200)
    adxv,pdi,mdi=T.adx(h,l,c); a=T.atr(h,l,c); st,sd=T.supertrend(h,l,c)
    return dict(rsi=rsi,k=k,d=d,bw=bw,pctB=pctB,cci=T.cci(h,l,c),wr=T.williams_r(h,l,c),
                mfi=T.mfi(h,l,c,v),obv=T.obv(c,v),macd=macd,sig=sig,hist=hist,
                e20=e20,e50=e50,e200=e200,adx=adxv,atr=a,st=sd)

def slope(s, i, look=5):
    seg=s.iloc[max(0,i-look):i+1].dropna()
    if len(seg)<3: return 0.0
    return float(np.polyfit(range(len(seg)),seg.values,1)[0])

def find_day0(df):
    o,h,l,c,v=(df[x] for x in ["open","high","low","close","volume"])
    n=len(df); v50=v.rolling(50,min_periods=10).mean()
    prior20=h.rolling(20).max().shift(1)
    # anchor on the base low of the RECENT move window (~last 200 bars) -> Day0 is the
    # FIRST decisive breakout after that low (move initiation, not a later acceleration leg)
    win0=max(0, n-200)
    base_low_idx=int(c.iloc[win0:n-10].idxmin()) if n>15 else win0
    cands=[]
    for i in range(max(base_low_idx, 25), n-5):
        if pd.isna(prior20.iloc[i]) or pd.isna(v50.iloc[i]): continue
        rng=h.iloc[i]-l.iloc[i]; cpos=(c.iloc[i]-l.iloc[i])/rng if rng>0 else 0.5
        volmult=v.iloc[i]/v50.iloc[i] if v50.iloc[i]>0 else 0
        if c.iloc[i]>prior20.iloc[i] and volmult>=1.4 and c.iloc[i]>o.iloc[i] and cpos>=0.5:
            fwd=c.iloc[i+1:i+60].max() if i+1<n else c.iloc[i]
            gain=(fwd/c.iloc[i]-1) if c.iloc[i]>0 else 0
            if gain>=0.15:
                cands.append((i,gain,volmult))
    if cands:
        i,gain,volmult=min(cands,key=lambda x:x[0])    # EARLIEST validated breakout = move initiation
        return i,True,round(volmult,2)
    # fallback: base low then first +8% close, no volume spike required
    iL=base_low_idx
    for i in range(iL+1,n):
        if c.iloc[i]>=c.iloc[iL]*1.08:
            vm=v.iloc[i]/v50.iloc[i] if pd.notna(v50.iloc[i]) and v50.iloc[i]>0 else np.nan
            return i,False,round(float(vm),2) if pd.notna(vm) else np.nan
    return n-1,False,np.nan

def snap(sym, df):
    df=df.reset_index(drop=True); S=series(df)
    o,h,l,c,v=(df[x] for x in ["open","high","low","close","volume"])
    i,verified,volmult=find_day0(df)
    R={"symbol":sym,"day0_date":str(df["date"].iloc[i].date()),"day0_idx_from_end":len(df)-1-i,
       "day0_open":round(float(o.iloc[i]),2),"day0_close":round(float(c.iloc[i]),2),
       "day0_volume":int(v.iloc[i]),"day0_verified_volspike":verified,"day0_vol_x_50davg":volmult}
    def val(key,r=1):
        x=S[key].iloc[i]; return round(float(x),r) if pd.notna(x) else np.nan
    # leading
    R["rsi"]=val("rsi"); R["stoch_k"]=val("k"); R["stoch_d"]=val("d")
    R["bb_width"]=val("bw",2); R["pctB"]=val("pctB",1); R["cci"]=val("cci"); R["williams_r"]=val("wr")
    R["mfi"]=val("mfi")
    osl=slope(S["obv"],i,10)
    R["obv_dir"]=("already_rising" if osl>0 and slope(S["obv"],i,3)>0 else "turning_up" if osl<=0 and slope(S["obv"],i,3)>0 else "flat/down")
    # lagging
    R["macd"]=val("macd",3); R["macd_signal"]=val("sig",3); R["macd_hist"]=val("hist",3)
    R["macd_vs_zero"]="above" if pd.notna(S["macd"].iloc[i]) and S["macd"].iloc[i]>0 else "below"
    R["ema20"]=val("e20",2); R["ema20_slope"]="up" if slope(S["e20"],i)>0 else "down/flat"
    R["ema50"]=val("e50",2); R["ema50_slope"]="up" if slope(S["e50"],i)>0 else "down/flat"
    e20i,e50i,e200i=S["e20"].iloc[i],S["e50"].iloc[i],S["e200"].iloc[i]
    if pd.notna(e200i):
        R["ema_alignment"]=("20>50>200" if e20i>e50i>e200i else "bearish" if e20i<e50i<e200i else "crossing/mixed")
    else: R["ema_alignment"]="n/a(short)"
    R["adx"]=val("adx"); R["atr"]=val("atr",2)
    R["atr_pct"]=round(float(S["atr"].iloc[i]/c.iloc[i]*100),2) if pd.notna(S["atr"].iloc[i]) else np.nan
    sd=S["st"]
    R["supertrend"]="green" if sd.iloc[i]==1 else "red"
    flip=""
    for kk in range(0,5):
        if i-kk-1>=0 and sd.iloc[i-kk]!=sd.iloc[i-kk-1]:
            flip="just_flipped_green" if sd.iloc[i-kk]==1 else "just_flipped_red"; break
    R["supertrend_flip"]=flip or "none_recent"
    # price action
    pats=c11.detect_at(df,i)
    R["day0_candle"]=";".join(pats) if pats else "none"
    hi52=float(h.iloc[max(0,i-252):i+1].max())
    R["pct_from_52wh"]=round((c.iloc[i]/hi52-1)*100,2)
    R["pct_vs_ema200"]=round(float((c.iloc[i]/e200i-1)*100),2) if pd.notna(e200i) else np.nan
    bwmid,bub,blb,_=T.bollinger(c)
    R["bb_position"]=("upper" if c.iloc[i]>bwmid.iloc[i] and c.iloc[i]>=bub.iloc[i]*0.99 else
                      "midband" if abs(c.iloc[i]-bwmid.iloc[i])/bwmid.iloc[i]<0.02 else
                      "above_mid" if c.iloc[i]>bwmid.iloc[i] else "lower") if pd.notna(bwmid.iloc[i]) else "n/a"
    # structure flags on Day0
    p10=float(h.iloc[max(0,i-10):i].max()) if i>0 else c.iloc[i]
    p20=float(h.iloc[max(0,i-20):i].max()) if i>0 else c.iloc[i]
    tight=(h.iloc[max(0,i-10):i].max()-l.iloc[max(0,i-10):i].min())/c.iloc[i]<0.13 if i>10 else False
    R["bos_triggered"]= "Y" if c.iloc[i]>p10 else "N"
    R["vcp_pivot_broken"]= "Y" if (c.iloc[i]>p20 and tight) else "N"
    hl = (l.iloc[max(0,i-5):i].min() > l.iloc[max(0,i-15):i-5].min()) if i>15 else False
    R["demand_zone_reclaimed"]= "Y" if (hl and c.iloc[i]>p10) else "N"
    last_bear=None
    for j in range(i-1,max(0,i-6),-1):
        if c.iloc[j]<o.iloc[j]: last_bear=j; break
    R["order_block_broken"]= "Y" if (last_bear is not None and c.iloc[i]>h.iloc[last_bear]) else "N"
    # 5D pre-context (days -5..-1)
    pv=v.iloc[max(0,i-5):i]; pr=S["rsi"].iloc[max(0,i-5):i]
    R["pre_vol_pattern"]=("rising" if slope(v,i-1,4)>0 else "declining" if slope(v,i-1,4)<0 else "flat")
    rs=slope(S["rsi"],i-1,4)
    R["pre_rsi_trend"]=("turning_up" if rs>0.5 else "rising_slowly" if rs>0 else "flat/down")
    pre_rng=(h.iloc[max(0,i-5):i].max()-l.iloc[max(0,i-5):i].min())/c.iloc[i]*100 if i>5 else np.nan
    R["pre_range_pct"]=round(float(pre_rng),2) if pd.notna(pre_rng) else np.nan
    R["pre_tight_range"]= "Y" if (pd.notna(pre_rng) and pre_rng<10) else "N"
    v50i=v.rolling(50,min_periods=10).mean().iloc[i]
    R["pre_volume_dryup"]= "Y" if (pd.notna(v50i) and pv.mean()<0.8*v50i) else "N"
    # shakeout in 10 days before: a low breaking prior-10 support then closing back above
    shake="N"
    if i>20:
        supp=float(l.iloc[i-20:i-10].min())
        for j in range(i-10,i):
            if l.iloc[j]<supp and c.iloc[j]>supp: shake="Y"; break
    R["pre_shakeout"]=shake
    R["bars_available"]=len(df)
    return R

if __name__=="__main__":
    data=pickle.load(open("ohlc.pkl","rb"))
    rows=[]
    for ix,(sym,df) in enumerate(data.items(),1):
        try: rows.append(snap(sym,df))
        except Exception as e: rows.append({"symbol":sym,"error":f"{type(e).__name__}:{e}"})
        if ix%80==0: print(f"  {ix}/{len(data)}")
    out=pd.DataFrame(rows); out.to_csv("PHASE5_DAY0.csv",index=False)
    print(f"DONE {len(out)} -> PHASE5_DAY0.csv")
    if "error" in out: print("errors:",out["error"].notna().sum(), out[out['error'].notna()]['symbol'].tolist()[:10])
    ok=out[out.get("rsi").notna()] if "rsi" in out else out
    print(f"verified vol-spike Day0: {out['day0_verified_volspike'].sum()}/{len(out)}")
    print("\nDay0 RSI: avg=%.1f min=%.1f max=%.1f"%(ok['rsi'].mean(),ok['rsi'].min(),ok['rsi'].max()))
    print("Day0 ADX: avg=%.1f"%ok['adx'].mean(),"| Day0 vol x50d avg=%.2f"%out['day0_vol_x_50davg'].dropna().mean())
    print("supertrend@day0:",out['supertrend'].value_counts().to_dict())
    print("ema_alignment@day0:",out['ema_alignment'].value_counts().to_dict())
