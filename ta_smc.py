"""Smart-Money-Concepts + Supply/Demand primitives (algorithmic, OHLCV only)."""
import numpy as np, pandas as pd

def swing_points(df, w=3):
    """Return chronological list of dicts {i, price, type} using fractal highs/lows."""
    H, L = df["high"].values, df["low"].values
    pts = []
    for i in range(w, len(df)-w):
        if H[i] == H[i-w:i+w+1].max() and H[i] > H[i-1] and H[i] >= H[i+1]:
            pts.append({"i": i, "price": float(H[i]), "type": "H"})
        if L[i] == L[i-w:i+w+1].min() and L[i] < L[i-1] and L[i] <= L[i+1]:
            pts.append({"i": i, "price": float(L[i]), "type": "L"})
    pts.sort(key=lambda p: p["i"])
    return pts

def bos_choch(df, w=3):
    """Walk price vs most-recent swing high/low to log BoS events; flip = ChoCh."""
    pts = swing_points(df, w)
    C = df["close"].values; dts = df["date"].dt.date.values
    SH = [p for p in pts if p["type"]=="H"]
    SL = [p for p in pts if p["type"]=="L"]
    events = []
    for i in range(len(df)):
        # most-recent swing high / low strictly before bar i
        sh = next((p for p in reversed(SH) if p["i"] < i), None)
        sl = next((p for p in reversed(SL) if p["i"] < i), None)
        if sh and C[i] > sh["price"]:
            if not (events and events[-1]["dir"]=="bull" and events[-1]["level"]==round(sh["price"],2)):
                events.append({"i": i, "date": str(dts[i]), "dir": "bull", "level": round(sh["price"],2)})
        if sl and C[i] < sl["price"]:
            if not (events and events[-1]["dir"]=="bear" and events[-1]["level"]==round(sl["price"],2)):
                events.append({"i": i, "date": str(dts[i]), "dir": "bear", "level": round(sl["price"],2)})
    # dedup consecutive same-direction same-level
    clean = []
    for e in events:
        if clean and clean[-1]["dir"]==e["dir"] and clean[-1]["level"]==e["level"]:
            continue
        clean.append(e)
    last_bos = clean[-1] if clean else None
    # ChoCh = most recent direction change
    choch = None
    for k in range(len(clean)-1, 0, -1):
        if clean[k]["dir"] != clean[k-1]["dir"]:
            choch = clean[k]; break
    return last_bos, choch, clean

def market_structure(df, w=4):
    pts = swing_points(df, w)
    Hs = [p for p in pts if p["type"]=="H"][-3:]
    Ls = [p for p in pts if p["type"]=="L"][-3:]
    if len(Hs)>=2 and len(Ls)>=2:
        if Hs[-1]["price"]>Hs[-2]["price"] and Ls[-1]["price"]>Ls[-2]["price"]: return "bullish (HH/HL)"
        if Hs[-1]["price"]<Hs[-2]["price"] and Ls[-1]["price"]<Ls[-2]["price"]: return "bearish (LH/LL)"
    return "ranging"

def demand_zone(df, impulse_atr=1.5, base_max=4, lookback=180):
    """Most recent demand zone: tight base then strong up impulse. Returns dict or None."""
    sub = df.tail(lookback).reset_index(drop=True)
    o,h,l,c = sub["open"],sub["high"],sub["low"],sub["close"]
    tr = pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    px=float(c.iloc[-1]); best = None
    for i in range(len(sub)-2, 14, -1):
        # impulse up at i: strong bullish bar leaving the area
        if pd.isna(atr.iloc[i]): continue
        if (c.iloc[i]-o.iloc[i]) > impulse_atr*atr.iloc[i] and c.iloc[i] > h.iloc[i-1]:
            # base = preceding up-to base_max small bars
            bs = max(0, i-base_max)
            base = sub.iloc[bs:i]
            zlo, zhi = float(base["low"].min()), float(base["high"].max())
            if zlo > px*1.02: continue           # demand zone must be at/below price (support)
            departure = (c.iloc[-1]-zhi)/zhi*100
            # tested? any later low re-enters [zlo,zhi]
            later = sub.iloc[i+1:]
            tested = bool((later["low"] <= zhi).any())
            volr = sub["volume"].iloc[bs:i].mean()/sub["volume"].iloc[:i].mean() if i>5 else 1
            base_bars = i-bs
            qual = "Strong" if (c.iloc[i]-o.iloc[i])>2*atr.iloc[i] and base_bars<=3 else "Moderate" if base_bars<=base_max else "Weak"
            best = {"zlo":round(zlo,2),"zhi":round(zhi,2),"date":str(sub["date"].iloc[bs].date()),
                    "fresh": not tested,"tested":tested,"quality":qual,
                    "vol_ratio":round(float(volr),2),"dist_pct":round(float((c.iloc[-1]-zhi)/zhi*100),2)}
            break
    return best

def supply_zone(df, impulse_atr=1.5, base_max=4, lookback=180):
    sub = df.tail(lookback).reset_index(drop=True)
    o,h,l,c = sub["open"],sub["high"],sub["low"],sub["close"]
    tr = pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    px=float(c.iloc[-1]); best=None
    for i in range(len(sub)-2, 14, -1):
        if pd.isna(atr.iloc[i]): continue
        if (o.iloc[i]-c.iloc[i]) > impulse_atr*atr.iloc[i] and c.iloc[i] < l.iloc[i-1]:
            bs=max(0,i-base_max); base=sub.iloc[bs:i]
            zlo,zhi=float(base["low"].min()),float(base["high"].max())
            if zhi < px*0.98: continue          # only OVERHEAD supply is a relevant resistance for longs
            later=sub.iloc[i+1:]; tested=bool((later["high"]>=zlo).any())
            base_bars=i-bs
            qual="Strong" if (o.iloc[i]-c.iloc[i])>2*atr.iloc[i] and base_bars<=3 else "Moderate" if base_bars<=base_max else "Weak"
            best={"zlo":round(zlo,2),"zhi":round(zhi,2),"date":str(sub["date"].iloc[bs].date()),
                  "fresh":not tested,"tested":tested,"quality":qual,
                  "dist_pct":round(float((zlo-px)/px*100),2)}
            break
    return best

def order_blocks(df, atr_mult=1.0, look=120):
    sub=df.tail(look).reset_index(drop=True)
    o,h,l,c=sub["open"],sub["high"],sub["low"],sub["close"]
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr=tr.rolling(14).mean()
    bull_ob=bear_ob=None
    px=float(c.iloc[-1])
    for i in range(len(sub)-2,14,-1):
        if pd.isna(atr.iloc[i]): continue
        # bullish impulse -> bullish OB = last bearish candle before i
        if bull_ob is None and (c.iloc[i]-o.iloc[i])>atr_mult*atr.iloc[i] and c.iloc[i]>h.iloc[i-1]:
            for j in range(i-1,max(0,i-6),-1):
                if c.iloc[j]<o.iloc[j]:
                    obl,obh=float(l.iloc[j]),float(h.iloc[j])
                    mitig=bool((sub["low"].iloc[i+1:]<=obh).any())
                    bull_ob={"low":round(obl,2),"high":round(obh,2),"date":str(sub["date"].iloc[j].date()),
                             "mitigated":mitig,"returned":mitig,"dist_pct":round((px-obh)/obh*100,2)}
                    break
        if bear_ob is None and (o.iloc[i]-c.iloc[i])>atr_mult*atr.iloc[i] and c.iloc[i]<l.iloc[i-1]:
            for j in range(i-1,max(0,i-6),-1):
                if c.iloc[j]>o.iloc[j]:
                    obl,obh=float(l.iloc[j]),float(h.iloc[j])
                    mitig=bool((sub["high"].iloc[i+1:]>=obl).any())
                    bear_ob={"low":round(obl,2),"high":round(obh,2),"date":str(sub["date"].iloc[j].date()),
                             "mitigated":mitig,"returned":mitig,"dist_pct":round((obl-px)/px*100,2)}
                    break
        if bull_ob and bear_ob: break
    return bull_ob,bear_ob

def fvgs(df, look=80):
    sub=df.tail(look).reset_index(drop=True)
    h,l=sub["high"].values,sub["low"].values
    px=float(sub["close"].iloc[-1])
    bull=[]; bear=[]
    for i in range(2,len(sub)):
        # bullish FVG: candle1.high < candle3.low
        if h[i-2] < l[i]:
            top,bot=l[i],h[i-2]
            filled=bool((l[i+1:]<=bot).any()) if i+1<len(sub) else False
            bull.append({"i":i,"top":round(top,2),"bot":round(bot,2),"date":str(sub["date"].iloc[i].date()),"filled":filled})
        # bearish FVG: candle1.low > candle3.high
        if l[i-2] > h[i]:
            top,bot=l[i-2],h[i]
            filled=bool((h[i+1:]>=top).any()) if i+1<len(sub) else False
            bear.append({"i":i,"top":round(top,2),"bot":round(bot,2),"date":str(sub["date"].iloc[i].date()),"filled":filled})
    unfilled_bull=[g for g in bull if not g["filled"]]
    unfilled_bear=[g for g in bear if not g["filled"]]
    # nearest unfilled below (bullish, magnet) and above (bearish)
    below=[g for g in unfilled_bull if g["bot"]<px]
    above=[g for g in unfilled_bear if g["top"]>px]
    near_below=max(below,key=lambda g:g["bot"]) if below else None
    near_above=min(above,key=lambda g:g["top"]) if above else None
    return len(unfilled_bull),len(unfilled_bear),near_below,near_above

def liquidity(df, w=3, tol=0.005, look=150):
    sub=df.tail(look).reset_index(drop=True)
    pts=swing_points(sub,w)
    px=float(sub["close"].iloc[-1])
    Hs=[p["price"] for p in pts if p["type"]=="H"]
    Ls=[p["price"] for p in pts if p["type"]=="L"]
    def clusters(vals):
        cl=[]
        for v in sorted(vals):
            if cl and abs(v-cl[-1][-1])/cl[-1][-1]<=tol: cl[-1].append(v)
            else: cl.append([v])
        return [round(np.mean(c),2) for c in cl if len(c)>=2]
    eq_highs=clusters(Hs); eq_lows=clusters(Ls)
    bsl=[x for x in eq_highs if x>px]      # buy-side liquidity above
    ssl=[x for x in eq_lows if x<px]       # sell-side liquidity below
    # sweep: last 6 bars poked above an eq-high then closed back below (or below eq-low then back up)
    recent=sub.tail(6)
    swept=""
    for x in eq_highs:
        if (recent["high"]>x*1.001).any() and sub["close"].iloc[-1]<x: swept="buy-side swept (bearish stop-hunt)"
    for x in eq_lows:
        if (recent["low"]<x*0.999).any() and sub["close"].iloc[-1]>x: swept="sell-side swept (bullish stop-hunt)"
    return (min(bsl) if bsl else None, max(ssl) if ssl else None, swept or "none",
            len(eq_highs), len(eq_lows))

def premium_discount(df, look=120):
    sub=df.tail(look)
    hi=float(sub["high"].max()); lo=float(sub["low"].min()); px=float(sub["close"].iloc[-1])
    if hi==lo: return "n/a",50.0,hi,lo
    pos=(px-lo)/(hi-lo)*100
    zone="Premium" if pos>55 else "Discount" if pos<45 else "Equilibrium"
    return zone,round(pos,1),round(hi,2),round(lo,2)
