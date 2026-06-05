"""Phase 2 Section C: candlestick pattern scan over the last 20 DAILY candles.
Output: candles.csv  -> symbol | pattern | date | direction | context | confirmation
        candles_summary.csv -> per-stock counts of bullish/bearish candle signals (last 20)."""
import pickle, numpy as np, pandas as pd
import ta_lib_local as T

BULL = {"Hammer","Inverted Hammer","Bullish Engulfing","Bullish Harami","Piercing Line",
        "Morning Star","Three White Soldiers","Bullish Marubozu","Tweezer Bottom","Dragonfly Doji",
        "Bullish Pin Bar"}
BEAR = {"Hanging Man","Shooting Star","Bearish Engulfing","Bearish Harami","Dark Cloud Cover",
        "Evening Star","Three Black Crows","Bearish Marubozu","Tweezer Top","Gravestone Doji",
        "Bearish Pin Bar"}

def sr_levels(df):
    hi, lo = T.swings(df["close"], 5)
    res = sorted({round(df["high"].iloc[i], 2) for i in hi})
    sup = sorted({round(df["low"].iloc[i], 2) for i in lo})
    return sup, res

def context(price, sup, res, tol=0.025):
    near_s = any(abs(price-s)/price <= tol for s in sup)
    near_r = any(abs(price-r)/price <= tol for r in res)
    if near_s and not near_r: return "at support"
    if near_r and not near_s: return "at resistance"
    if near_s and near_r: return "at S/R confluence"
    return "midair"

def trend_before(c, i, look=10):
    if i-look < 0: return "flat"
    seg = c.iloc[max(0,i-look):i]
    if len(seg) < 4: return "flat"
    sl = np.polyfit(range(len(seg)), seg.values, 1)[0]
    return "up" if sl > 0 else "down" if sl < 0 else "flat"

def detect_at(df, i):
    """return list of pattern names ending at index i."""
    o,h,l,c = (df[x] for x in ["open","high","low","close"])
    out = []
    O,H,L,C = o.iloc[i],h.iloc[i],l.iloc[i],c.iloc[i]
    body = abs(C-O); rng = H-L if H>L else 1e-9
    upsh = H-max(O,C); dnsh = min(O,C)-L
    green = C>O; red = C<O
    tr = trend_before(c, i)
    # --- single-candle ---
    if body <= 0.1*rng:
        if dnsh > 0.6*rng and upsh < 0.1*rng: out.append("Dragonfly Doji")
        elif upsh > 0.6*rng and dnsh < 0.1*rng: out.append("Gravestone Doji")
        elif upsh > 0.3*rng and dnsh > 0.3*rng: out.append("Long-legged Doji")
        else: out.append("Doji")
    if body >= 0.9*rng:
        out.append("Bullish Marubozu" if green else "Bearish Marubozu")
    # hammer family: small body, one long shadow
    if body <= 0.35*rng and dnsh >= 2*body and upsh <= 0.25*rng and body>0:
        out.append("Hammer" if tr=="down" else "Hanging Man" if tr=="up" else "Hammer")
    if body <= 0.35*rng and upsh >= 2*body and dnsh <= 0.25*rng and body>0:
        out.append("Inverted Hammer" if tr=="down" else "Shooting Star" if tr=="up" else "Shooting Star")
    # pin bar (rejection) — long single shadow >=66% range
    if dnsh >= 0.66*rng and body <= 0.3*rng: out.append("Bullish Pin Bar")
    if upsh >= 0.66*rng and body <= 0.3*rng: out.append("Bearish Pin Bar")
    # --- two-candle ---
    if i>=1:
        O1,C1,H1,L1 = o.iloc[i-1],c.iloc[i-1],h.iloc[i-1],l.iloc[i-1]
        b1 = abs(C1-O1)
        if C1<O1 and green and C>=O1 and O<=C1 and body>b1: out.append("Bullish Engulfing")
        if C1>O1 and red and O>=C1 and C<=O1 and body>b1: out.append("Bearish Engulfing")
        if C1<O1 and green and O>C1 and C<O1 and body<b1 and O>=L1: out.append("Bullish Harami")
        if C1>O1 and red and O<C1 and C>O1 and body<b1: out.append("Bearish Harami")
        if C1<O1 and green and O<L1 and C>(O1+C1)/2 and C<O1: out.append("Piercing Line")
        if C1>O1 and red and O>H1 and C<(O1+C1)/2 and C>O1: out.append("Dark Cloud Cover")
        if abs(H-H1)/max(H,1e-9) < 0.003 and tr=="up": out.append("Tweezer Top")
        if abs(L-L1)/max(L,1e-9) < 0.003 and tr=="down": out.append("Tweezer Bottom")
        if H<H1 and L>L1: out.append("Inside Bar")
        if H>H1 and L<L1: out.append("Outside Bar")
    # --- NR7 / NR4 ---
    if i>=6 and rng == min((h.iloc[i-6:i+1]-l.iloc[i-6:i+1]).values): out.append("NR7")
    elif i>=3 and rng == min((h.iloc[i-3:i+1]-l.iloc[i-3:i+1]).values): out.append("NR4")
    # --- three-candle ---
    if i>=2:
        O2,C2 = o.iloc[i-2],c.iloc[i-2]; b2=abs(C2-O2)
        O1,C1 = o.iloc[i-1],c.iloc[i-1]; b1=abs(C1-O1)
        # morning star
        if C2<O2 and b1<0.5*b2 and green and C>(O2+C2)/2: out.append("Morning Star")
        if C2>O2 and b1<0.5*b2 and red and C<(O2+C2)/2: out.append("Evening Star")
        # three soldiers / crows
        if (c.iloc[i]>c.iloc[i-1]>c.iloc[i-2]) and all(c.iloc[j]>o.iloc[j] for j in (i,i-1,i-2)):
            out.append("Three White Soldiers")
        if (c.iloc[i]<c.iloc[i-1]<c.iloc[i-2]) and all(c.iloc[j]<o.iloc[j] for j in (i,i-1,i-2)):
            out.append("Three Black Crows")
    return out

def confirm(df, i, name):
    if i >= len(df)-1: return "pending (last bar)"
    nxt = df["close"].iloc[i+1]; cur = df["close"].iloc[i]
    if name in BULL: return "confirmed" if nxt > cur else "failed"
    if name in BEAR: return "confirmed" if nxt < cur else "failed"
    return "neutral"

if __name__ == "__main__":
    data = pickle.load(open("ohlc.pkl","rb"))
    rows, summ = [], []
    for sym, df in data.items():
        df = df.reset_index(drop=True)
        sup, res = sr_levels(df)
        nb = 0; bull=bear=0
        start = max(0, len(df)-20)
        for i in range(start, len(df)):
            pats = detect_at(df, i)
            for p in pats:
                ctx = context(df["close"].iloc[i], sup, res)
                conf = confirm(df, i, p)
                rows.append({"symbol":sym,"pattern":p,"date":df["date"].iloc[i].date().isoformat(),
                             "timeframe":"1D","direction":"bullish" if p in BULL else "bearish" if p in BEAR else "neutral",
                             "context":ctx,"confirmation":conf})
                nb += 1
                if p in BULL: bull+=1
                elif p in BEAR: bear+=1
        summ.append({"symbol":sym,"candle_signals_20d":nb,"bullish_candles":bull,"bearish_candles":bear,
                     "candle_bias":"bullish" if bull>bear else "bearish" if bear>bull else "neutral"})
    pd.DataFrame(rows).to_csv("candles.csv", index=False)
    s = pd.DataFrame(summ); s.to_csv("candles_summary.csv", index=False)
    print(f"DONE. {len(rows)} candle patterns across {len(data)} stocks")
    print("candle_bias:", s["candle_bias"].value_counts().to_dict())
    allp = pd.DataFrame(rows)
    print("\nmost common patterns:")
    print(allp["pattern"].value_counts().head(15).to_string())
