"""Phase 8b — Intraday VCP scan of the Nifty option strikes → FNO_VCP.csv.

For every strike in OPTION_CHAIN.csv (ATM +/-2, all current-month expiries), fetch the
option's intraday chart from NSE (chart-databyindex), resample the tick/price series to
1m / 3m / 5m / 15m / 1h OHLC, and run a Volatility-Contraction-Pattern scan on each.

Data is price-only (no volume) and single-session (today), so 1m-5m have ample bars,
15m is usable, and 1h is usually too few bars (flagged "insufficient"). Read at build
time by 25_build_frontend.py for the F&O VCP dropdown. Mechanical only — not advice.
"""
import time, urllib.parse
import numpy as np, pandas as pd
import ta_lib_local as T
import ta_smc as S
import nse_fno

SYMBOL = "NIFTY"
N_STRIKES = 2                                   # ATM +/-2 (match 28_option_chain.py)
TFS = [("1m", "1min"), ("3m", "3min"), ("5m", "5min"), ("15m", "15min"), ("1h", "60min")]
MIN_BARS = 12                                   # fewer bars than this -> can't judge a VCP


def intraday_series(s, identifier):
    """Return a price Series indexed by datetime for one contract's intraday chart, or None."""
    url = f"https://www.nseindia.com/api/chart-databyindex?index={urllib.parse.quote(identifier)}&indices=false"
    try:
        j = nse_fno.get_json(s, url)
    except Exception:
        return None
    gd = j.get("grapthData") or j.get("graphData") or []     # NSE's field is misspelt "grapthData"
    if len(gd) < 30:
        return None
    df = pd.DataFrame(gd, columns=["ts", "price"]).dropna()
    df["dt"] = pd.to_datetime(df["ts"], unit="ms")
    return df.set_index("dt")["price"].sort_index()


def scan_vcp(ohlc):
    """Price-based VCP scan on a resampled OHLC frame (no volume). Returns a verdict dict."""
    if ohlc is None or len(ohlc) < MIN_BARS:
        return {"status": "insufficient data", "legs": 0, "tightening": False,
                "pivot": None, "pct": None, "bars": 0 if ohlc is None else len(ohlc), "depths": ""}
    h = ohlc["high"].reset_index(drop=True); l = ohlc["low"].reset_index(drop=True); c = ohlc["close"].reset_index(drop=True)
    sh, sl = T.swings(c, 3)
    ev = sorted([(i, "H", float(h.iloc[i])) for i in sh] + [(i, "L", float(l.iloc[i])) for i in sl], key=lambda x: x[0])
    contr, last_peak = [], None
    for i, t, p in ev:
        if t == "H":
            last_peak = (i, p)
        elif t == "L" and last_peak is not None:
            depth = (last_peak[1] - p) / last_peak[1] * 100
            if depth >= 1:
                contr.append(round(depth, 1))
            last_peak = None
    last3 = contr[-3:]
    tightening = len(last3) >= 2 and all(last3[i] > last3[i + 1] for i in range(len(last3) - 1))
    pivot = float(h.iloc[sh[-1]]) if len(sh) else float(h.max())
    px = float(c.iloc[-1]); pct = (px - pivot) / pivot * 100 if pivot else None
    if pivot and px > pivot * 1.001:
        status = "Breakout"
    elif pct is not None and -1.5 <= pct <= 0.3:
        status = "At pivot"
    elif len(last3) >= 2 and tightening:
        status = "VCP forming"
    elif len(last3) >= 3:
        status = "Contracting"
    else:
        status = "No VCP"
    return {"status": status, "legs": len(last3), "tightening": bool(tightening),
            "pivot": round(pivot, 2), "pct": round(pct, 2) if pct is not None else None,
            "bars": len(ohlc), "depths": " / ".join(f"-{d}%" for d in last3)}


def price_signals(ohlc):
    """VWAP position + EMA 10/20 crossover on a resampled OHLC frame (price-only, no volume)."""
    if ohlc is None or len(ohlc) < 5:
        return {"vwap_pos": "—", "vwap": None, "ema_sig": "—", "ema_cross": ""}
    c = ohlc["close"]; tp = (ohlc["high"] + ohlc["low"] + ohlc["close"]) / 3
    vwap = float(tp.expanding().mean().iloc[-1])            # anchored session mean (no volume weighting)
    res = {"vwap_pos": "above" if float(c.iloc[-1]) > vwap else "below", "vwap": round(vwap, 2)}
    if len(ohlc) >= 20:
        e10 = c.ewm(span=10, adjust=False).mean(); e20 = c.ewm(span=20, adjust=False).mean()
        sgn = np.sign(e10 - e20)
        res["ema_sig"] = "bull" if sgn.iloc[-1] > 0 else "bear"
        tail = sgn.tail(4).values
        res["ema_cross"] = "golden" if (tail[0] <= 0 and tail[-1] > 0) else "death" if (tail[0] >= 0 and tail[-1] < 0) else ""
    else:
        res["ema_sig"], res["ema_cross"] = "—", ""
    return res


def volume_profile(ser, bins=40):
    """Tick/time-based profile from the intraday price series (no exchange volume available).
    Returns POC + Value Area (VAH/VAL) and a long-the-option entry/SL/target plan."""
    if ser is None or len(ser) < 30:
        return None
    p = ser.values.astype(float)
    lo, hi = float(p.min()), float(p.max())
    if hi <= lo:
        return None
    counts, edges = np.histogram(p, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    poc_i = int(counts.argmax()); poc = float(centers[poc_i])
    total = counts.sum(); target = 0.70 * total
    lo_i = hi_i = poc_i; acc = int(counts[poc_i])
    while acc < target:
        up = int(counts[hi_i + 1]) if hi_i + 1 < len(counts) else -1
        dn = int(counts[lo_i - 1]) if lo_i - 1 >= 0 else -1
        if up < 0 and dn < 0:
            break
        if up >= dn:
            hi_i += 1; acc += int(counts[hi_i])
        else:
            lo_i -= 1; acc += int(counts[lo_i])
    val = float(edges[lo_i]); vah = float(edges[hi_i + 1]); last = float(p[-1]); width = vah - val
    if last > vah:
        bias, entry, sl, tgt = "Above value — momentum long", round(vah, 2), round(val, 2), round(vah + 2 * width, 2)
    elif last < val:
        bias, entry, sl, tgt = "Below value — avoid long (weak)", None, None, None
    else:
        bias, entry, sl, tgt = "In value — long from VAL", round(val, 2), round(val - 0.5 * width, 2), round(vah, 2)
    rr = round((tgt - entry) / (entry - sl), 2) if (entry and sl and tgt and entry > sl) else None
    return {"poc": round(poc, 2), "vah": round(vah, 2), "val": round(val, 2), "last": round(last, 2),
            "vp_bias": bias, "vp_entry": entry, "vp_sl": sl, "vp_target": tgt, "vp_rr": rr}


def trendline_liq(o):
    """Trendline-liquidity proxy: break of the line through the last 2 swing lows (SSL grab)
    or last 2 swing highs (BSL grab)."""
    try:
        pts = S.swing_points(o.reset_index(drop=True))
    except Exception:
        return "—"
    n = len(o)
    lows = [(p["i"], p["price"]) for p in pts if p["type"] == "L"]
    highs = [(p["i"], p["price"]) for p in pts if p["type"] == "H"]
    lastlow, lasthigh = float(o["low"].iloc[-1]), float(o["high"].iloc[-1])
    if len(lows) >= 2:
        (i1, p1), (i2, p2) = lows[-2], lows[-1]
        if p2 > p1 and i2 > i1:                                   # rising support line
            proj = p2 + (p2 - p1) / (i2 - i1) * ((n - 1) - i2)
            if lastlow < proj * 0.999:
                return "uptrend line swept (SSL)"
    if len(highs) >= 2:
        (i1, p1), (i2, p2) = highs[-2], highs[-1]
        if p2 < p1 and i2 > i1:                                   # falling resistance line
            proj = p2 + (p2 - p1) / (i2 - i1) * ((n - 1) - i2)
            if lasthigh > proj * 1.001:
                return "downtrend line broken (BSL)"
    return "—"


def smc_signals(ohlc):
    """Core SMC read on a resampled OHLC frame: structure, premium/discount, supply/demand,
    liquidity sweeps + trendline liquidity."""
    blank = {"smc_struct": "—", "smc_zone": "—", "smc_sd": "—", "smc_liq": "—", "smc_trend": "—"}
    if ohlc is None or len(ohlc) < 15:
        return blank
    d = ohlc.reset_index()
    d = d.rename(columns={d.columns[0]: "date"}); d["volume"] = 1.0
    try:
        struct = S.market_structure(d)
    except Exception:
        struct = "ranging"
    struct_s = "bull" if "bull" in struct else "bear" if "bear" in struct else "range"
    try:
        zone = S.premium_discount(d)[0]
    except Exception:
        zone = "—"
    try:
        _bsl, _ssl, swept, _neh, _nel = S.liquidity(d)
    except Exception:
        _bsl = _ssl = None; swept = "none"
    liq = swept if swept and swept != "none" else ("BSL above" if _bsl else "SSL below" if _ssl else "—")
    try:
        dz = S.demand_zone(d)
    except Exception:
        dz = None
    try:
        sz = S.supply_zone(d)
    except Exception:
        sz = None
    sd = "—"
    if dz and dz.get("dist_pct") is not None and 0 <= dz["dist_pct"] <= 2:
        sd = "at demand"
    elif sz and sz.get("dist_pct") is not None and 0 <= sz["dist_pct"] <= 2:
        sd = "at supply"
    elif dz and (dz.get("dist_pct") if dz.get("dist_pct") is not None else 99) <= 6:
        sd = "demand below"
    elif sz and (sz.get("dist_pct") if sz.get("dist_pct") is not None else 99) <= 6:
        sd = "supply above"
    return {"smc_struct": struct_s, "smc_zone": zone, "smc_sd": sd,
            "smc_liq": liq, "smc_trend": trendline_liq(ohlc)}


def main():
    chain = pd.read_csv("OPTION_CHAIN.csv")
    expiries = list(dict.fromkeys(chain["expiry"].tolist()))
    s, kind = nse_fno.make_session(); print(f"session: {kind}")

    rows, vp_rows, n_ok = [], [], 0
    for exp in expiries:
        ch = nse_fno.fetch_chain(s, SYMBOL, exp)
        by = {int(d["strikePrice"]): d for d in ch["rows"]}
        strikes = sorted(set(chain[chain["expiry"] == exp]["strike"].astype(int)))
        for k in strikes:
            for side in ("CE", "PE"):
                ident = (by.get(k, {}).get(side) or {}).get("identifier")
                ser = intraday_series(s, ident) if ident else None
                vp = volume_profile(ser)                      # session profile (once per contract)
                if vp:
                    vp_rows.append({"expiry": exp, "strike": k, "side": side, **vp})
                for tflabel, rule in TFS:
                    o = ser.resample(rule).ohlc().dropna() if ser is not None else None
                    v = scan_vcp(o); sig = price_signals(o); smc = smc_signals(o)
                    rows.append({"expiry": exp, "strike": k, "side": side, "tf": tflabel, **v, **sig, **smc})
                if ser is not None:
                    n_ok += 1
                time.sleep(0.2)
        print(f"  {exp}: scanned {len(strikes)} strikes x CE/PE")

    pd.DataFrame(rows).to_csv("FNO_VCP.csv", index=False)
    pd.DataFrame(vp_rows).to_csv("FNO_VPROFILE.csv", index=False)
    print(f"Wrote FNO_VCP.csv ({len(rows)} rows) + FNO_VPROFILE.csv ({len(vp_rows)} contracts) "
          f"| contracts with intraday data: {n_ok}")


if __name__ == "__main__":
    main()
