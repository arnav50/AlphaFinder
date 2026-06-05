"""Self-contained technical-analysis library (exact standard formulas, numpy/pandas only).
Every function guards on minimum bars and returns NaN where history is insufficient."""
import numpy as np, pandas as pd

def wilder(s, n):                      # Wilder's smoothing (RMA)
    return s.ewm(alpha=1/n, adjust=False, min_periods=n).mean()

def ema(s, n):
    return s.ewm(span=n, adjust=False, min_periods=n).mean()

def rsi(close, n=14):
    d = close.diff()
    up = wilder(d.clip(lower=0), n)
    dn = wilder(-d.clip(upper=0), n)
    rs = up / dn.replace(0, np.nan)
    return (100 - 100/(1+rs)).fillna(100)

def stoch(h, l, c, k=14, d=3, smooth=3):
    ll = l.rolling(k).min(); hh = h.rolling(k).max()
    raw = 100*(c-ll)/(hh-ll).replace(0, np.nan)
    pk = raw.rolling(smooth).mean()
    pd_ = pk.rolling(d).mean()
    return pk, pd_

def bollinger(c, n=20, k=2):
    mid = c.rolling(n).mean(); sd = c.rolling(n).std(ddof=0)
    up, lo = mid + k*sd, mid - k*sd
    width = (up-lo)/mid*100
    return mid, up, lo, width

def cci(h, l, c, n=20):
    tp = (h+l+c)/3
    sma = tp.rolling(n).mean()
    md = (tp - sma).abs().rolling(n).mean()
    return (tp-sma)/(0.015*md.replace(0, np.nan))

def williams_r(h, l, c, n=14):
    hh = h.rolling(n).max(); ll = l.rolling(n).min()
    return -100*(hh-c)/(hh-ll).replace(0, np.nan)

def obv(c, v):
    return (np.sign(c.diff().fillna(0))*v).cumsum()

def mfi(h, l, c, v, n=14):
    tp = (h+l+c)/3; rmf = tp*v
    pos = rmf.where(tp > tp.shift(1), 0.0)
    neg = rmf.where(tp < tp.shift(1), 0.0)
    pr = pos.rolling(n).sum(); nr = neg.rolling(n).sum()
    return 100 - 100/(1 + pr/nr.replace(0, np.nan))

def macd(c, f=12, s=26, sig=9):
    line = ema(c, f) - ema(c, s)
    signal = line.ewm(span=sig, adjust=False, min_periods=sig).mean()
    return line, signal, line-signal

def atr(h, l, c, n=14):
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return wilder(tr, n)

def adx(h, l, c, n=14):
    up = h.diff(); dn = -l.diff()
    plus = ((up > dn) & (up > 0)) * up
    minus = ((dn > up) & (dn > 0)) * dn
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    atr_ = wilder(tr, n)
    pdi = 100*wilder(plus, n)/atr_
    mdi = 100*wilder(minus, n)/atr_
    dx = 100*(pdi-mdi).abs()/(pdi+mdi).replace(0, np.nan)
    return wilder(dx, n), pdi, mdi

def supertrend(h, l, c, period=7, mult=3.0):
    a = atr(h, l, c, period).values
    hl2 = ((h+l)/2).values; cv = c.values
    ub = hl2 + mult*a; lb = hl2 - mult*a
    nlen = len(cv)
    fub = np.full(nlen, np.nan); flb = np.full(nlen, np.nan)
    st = np.full(nlen, np.nan); dir_ = np.full(nlen, np.nan)
    started = False
    for i in range(nlen):
        if np.isnan(a[i]):
            continue
        if not started:                       # seed at first valid ATR bar
            fub[i], flb[i] = ub[i], lb[i]
            st[i] = lb[i] if cv[i] >= lb[i] else ub[i]
            dir_[i] = 1 if cv[i] > st[i] else -1
            started = True; continue
        fub[i] = ub[i] if (ub[i] < fub[i-1] or cv[i-1] > fub[i-1]) else fub[i-1]
        flb[i] = lb[i] if (lb[i] > flb[i-1] or cv[i-1] < flb[i-1]) else flb[i-1]
        if st[i-1] == fub[i-1]:
            st[i] = fub[i] if cv[i] <= fub[i] else flb[i]
        else:
            st[i] = flb[i] if cv[i] >= flb[i] else fub[i]
        dir_[i] = 1 if cv[i] > st[i] else -1
    return pd.Series(st, index=c.index), pd.Series(dir_, index=c.index)

def ichimoku(h, l, c):
    tenkan = (h.rolling(9).max()+l.rolling(9).min())/2
    kijun = (h.rolling(26).max()+l.rolling(26).min())/2
    spanA = ((tenkan+kijun)/2).shift(26)
    spanB = ((h.rolling(52).max()+l.rolling(52).min())/2).shift(26)
    chikou = c.shift(-26)
    # future cloud (for kumo-twist detection): spanA/B without the forward shift
    fA = (tenkan+kijun)/2
    fB = (h.rolling(52).max()+l.rolling(52).min())/2
    return tenkan, kijun, spanA, spanB, chikou, fA, fB

def vwap_rolling(h, l, c, v, n=20):
    tp = (h+l+c)/3
    return (tp*v).rolling(n).sum()/v.rolling(n).sum()

def pivots(h, l, c):                   # classic floor pivots from a completed period
    p = (h+l+c)/3
    return {"P": p, "R1": 2*p-l, "S1": 2*p-h, "R2": p+(h-l), "S2": p-(h-l)}

def swings(s, w=3):
    """indices of local maxima/minima with window w on each side."""
    hi, lo = [], []
    a = s.values
    for i in range(w, len(a)-w):
        seg = a[i-w:i+w+1]
        if a[i] == seg.max() and (seg.argmax() == w): hi.append(i)
        if a[i] == seg.min() and (seg.argmin() == w): lo.append(i)
    return hi, lo

def last_cross(fast, slow, lookback=5):
    """returns 'bull'/'bear'/'' if fast crossed slow within lookback bars."""
    d = (fast - slow)
    sgn = np.sign(d)
    for k in range(1, min(lookback, len(d)-1)+1):
        if sgn.iloc[-k] > 0 and sgn.iloc[-k-1] <= 0: return "bull"
        if sgn.iloc[-k] < 0 and sgn.iloc[-k-1] >= 0: return "bear"
    return ""
