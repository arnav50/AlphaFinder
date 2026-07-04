"""Phase 9 — F&O TRADE FINDER: the 7-phase Watchlist methodology applied to the
Nifty 50 option chain to surface an actionable options trade.

Mirrors the equity pipeline phase-for-phase, but on options:
  P1 Discovery   : live chain + DTE, lot size, OI-based support/resistance
  P2 Technicals  : EMA20/50/200, RSI, ADX, MACD, Supertrend, ATR on Nifty 50 -> price bias
  P3 Structure   : max-PE-OI support, max-CE-OI resistance, ChgOI writing, PCR, max-pain -> OI bias
  P4 Volatility  : ATM IV regime + implied expected move (ATM straddle) -> buy vs spread
  P5 Fingerprint : price-bias AND OI-bias AND IV alignment template -> direction + confidence
  P6 Ranking     : score CE / PE / debit-spread candidates 0-100 -> rank, tier
  P7 Trade plan  : option entry / stop / target / R:R / lots + GO/WATCH/AVOID verdict

Picks the nearest weekly expiry with >=2 days left (skips an expiring contract).
Outputs FNO_TRADES.csv (ranked candidates) + FNO_PLAN.csv (headline + per-phase reads).
Read at build time by 25_build_frontend.py. Mechanical signals only — NOT advice.
"""
import datetime, numpy as np, pandas as pd, requests
import ta_lib_local as T
import ta_vcp_gann as VG
import nse_fno

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
SYMBOL   = "NIFTY"
LOT      = 75            # NSE Nifty lot size
CAPITAL  = 1_000_000     # Rs 10L reference book
RISK_PCT = 0.01          # 1% risk per trade
DELTA    = {"ITM": 0.65, "ATM": 0.50, "OTM": 0.32}   # rough |delta| by moneyness for buyers


# ---------- Nifty 50 daily technicals (Phase 2) ----------
def nifty_daily():
    r = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI",
                     params={"range": "1y", "interval": "1d"},
                     headers={"User-Agent": UA}, timeout=25)
    res = r.json()["chart"]["result"][0]; q = res["indicators"]["quote"][0]
    df = pd.DataFrame({"open": q["open"], "close": q["close"], "high": q["high"],
                       "low": q["low"], "volume": q["volume"]}).dropna().reset_index(drop=True)
    return df


def price_bias(df):
    c, h, l = df["close"], df["high"], df["low"]
    px = float(c.iloc[-1])
    e20, e50, e200 = float(T.ema(c, 20).iloc[-1]), float(T.ema(c, 50).iloc[-1]), float(T.ema(c, 200).iloc[-1])
    rsi = float(T.rsi(c).iloc[-1]); adx = float(T.adx(h, l, c)[0].iloc[-1])
    macd_line, sig, hist = T.macd(c); mh = float(hist.iloc[-1])
    _st_line, st_dirs = T.supertrend(h, l, c); stv = st_dirs.iloc[-1]
    st_dir = "up" if stv == 1 else "down" if stv == -1 else ""
    atr = float(T.atr(h, l, c).iloc[-1])
    sig_list = []
    score = 0
    if px > e20: score += 1; sig_list.append("px>EMA20")
    else: score -= 1; sig_list.append("px<EMA20")
    if e20 > e50: score += 1; sig_list.append("EMA20>50")
    else: score -= 1; sig_list.append("EMA20<50")
    if e50 > e200: score += 1; sig_list.append("EMA50>200")
    else: score -= 1; sig_list.append("EMA50<200")
    if rsi >= 55: score += 1; sig_list.append(f"RSI {rsi:.0f}>55")
    elif rsi <= 45: score -= 1; sig_list.append(f"RSI {rsi:.0f}<45")
    if mh > 0: score += 1; sig_list.append("MACD+")
    else: score -= 1; sig_list.append("MACD-")
    if st_dir in ("up", "green", "1", "buy"): score += 1; sig_list.append("Supertrend up")
    elif st_dir: score -= 1; sig_list.append("Supertrend down")
    trend = "UPTREND" if px > e50 > e200 else "DOWNTREND" if px < e50 < e200 else "MIXED/RANGE"
    return dict(px=round(px, 2), e20=round(e20), e50=round(e50), e200=round(e200),
                rsi=round(rsi, 1), adx=round(adx, 1), macd_hist=round(mh, 1), st_dir=st_dir,
                atr=round(atr, 1), trend=trend, score=score, signals=", ".join(sig_list))


# ---------- option-chain structure (Phase 3) ----------
def oi_structure(rows, spot, atm):
    by = {int(d["strikePrice"]): d for d in rows}
    strikes = sorted(by)
    win = [k for k in strikes if abs(k - atm) <= 15 * 50]   # ATM +/-15 strikes, skip far illiquid
    def oi(k, side): return float((by[k].get(side) or {}).get("openInterest") or 0)
    def chgoi(k, side): return float((by[k].get(side) or {}).get("changeinOpenInterest") or 0)
    above = [k for k in win if k > spot] or win
    below = [k for k in win if k < spot] or win
    resistance = max(above, key=lambda k: oi(k, "CE"))      # heaviest call OI above spot = resistance
    support    = max(below, key=lambda k: oi(k, "PE"))      # heaviest put OI below spot = support
    near = [k for k in strikes if abs(k - atm) <= 3 * 50]
    ce_chg = sum(chgoi(k, "CE") for k in near); pe_chg = sum(chgoi(k, "PE") for k in near)
    ce_oi_tot = sum(oi(k, "CE") for k in strikes); pe_oi_tot = sum(oi(k, "PE") for k in strikes)
    pcr = round(pe_oi_tot / ce_oi_tot, 2) if ce_oi_tot else None
    def pain(at): return sum(oi(k, "CE") * max(0, at - k) + oi(k, "PE") * max(0, k - at) for k in strikes)
    max_pain = min(strikes, key=pain)
    score = 0; sig = []
    if pcr is not None and pcr >= 1.05: score += 1; sig.append(f"PCR {pcr}>1 (put-heavy/bullish)")
    elif pcr is not None and pcr <= 0.85: score -= 1; sig.append(f"PCR {pcr}<0.85 (call-heavy/bearish)")
    if pe_chg > ce_chg: score += 1; sig.append("fresh put writing (bullish)")
    elif ce_chg > pe_chg: score -= 1; sig.append("fresh call writing (bearish)")
    if max_pain > spot: score += 1; sig.append(f"max-pain {max_pain}>spot (pull up)")
    elif max_pain < spot: score -= 1; sig.append(f"max-pain {max_pain}<spot (pull down)")
    return dict(support=support, resistance=resistance, pcr=pcr, max_pain=max_pain,
                ce_chg_oi=round(ce_chg), pe_chg_oi=round(pe_chg),
                ce_oi_total=round(ce_oi_tot), pe_oi_total=round(pe_oi_tot),
                score=score, signals="; ".join(sig) or "balanced", by=by, strikes=strikes)


def leg(by, k, side):
    d = (by.get(k, {}).get(side) or {})
    return dict(ltp=float(d.get("lastPrice") or 0), iv=float(d.get("impliedVolatility") or 0),
                oi=float(d.get("openInterest") or 0))


def main():
    today = datetime.date.today()
    s, kind = nse_fno.make_session(); print(f"session: {kind}")
    expiries, _ = nse_fno.contract_info(s, SYMBOL)

    # P1: pick nearest expiry with >=2 days left (don't trade an expiring contract)
    def dte(e): return (datetime.datetime.strptime(e, "%d-%b-%Y").date() - today).days
    expiry = next((e for e in expiries if dte(e) >= 2), expiries[0])
    ch = nse_fno.fetch_chain(s, SYMBOL, expiry)
    spot, rows, nse_ts = ch["spot"], ch["rows"], ch["timestamp"]
    days = max(dte(expiry), 0)
    by = {int(d["strikePrice"]): d for d in rows}
    strikes = sorted(by); atm = min(strikes, key=lambda k: abs(k - spot))
    step = int(np.median(np.diff(strikes))) if len(strikes) > 1 else 50

    # P2: price bias (+ VCP 3-leg breakout on the underlying)
    ndf = nifty_daily()
    pb = price_bias(ndf)
    vcp = VG.detect_vcp(ndf)
    # P3: OI structure
    oc = oi_structure(rows, spot, atm)

    # P4: volatility / expected move
    atm_ce, atm_pe = leg(by, atm, "CE"), leg(by, atm, "PE")
    atm_iv = round((atm_ce["iv"] + atm_pe["iv"]) / 2, 1) if (atm_ce["iv"] and atm_pe["iv"]) else round(atm_ce["iv"] or atm_pe["iv"], 1)
    straddle = round(atm_ce["ltp"] + atm_pe["ltp"], 1)          # market-implied move to expiry
    exp_move = straddle
    iv_regime = "low" if atm_iv and atm_iv < 12 else "high" if atm_iv and atm_iv > 18 else "normal"

    # P5: alignment -> direction + confidence
    combined = pb["score"] + 1.5 * oc["score"]                  # price + OI (OI weighted)
    if combined >= 2 and pb["score"] >= 1: direction, dirn = "BULLISH", +1
    elif combined <= -2 and pb["score"] <= -1: direction, dirn = "BEARISH", -1
    else: direction, dirn = "NEUTRAL", 0
    agree = (pb["score"] > 0 and oc["score"] > 0) or (pb["score"] < 0 and oc["score"] < 0)
    adx_ok = pb["adx"] >= 18
    confidence = "high" if (agree and adx_ok and direction != "NEUTRAL") else \
                 "low" if (direction == "NEUTRAL" or not adx_ok) else "medium"

    # ---- P6/P7: build + score candidate trades ----
    def build(side, strike, moneyness, kind_label, sell_strike=None):
        L = leg(by, strike, side); entry = round(L["ltp"], 2)
        if entry <= 0: return None
        dlt = DELTA[moneyness]; atr = pb["atr"]
        if side == "CE":                                        # bullish: target above, stop below spot
            tgt_lvl  = max(spot + 1, min(oc["resistance"], spot + exp_move))
            stop_lvl = min(spot - 1, max(oc["support"], spot - 0.6 * atr))
            tgt_move = tgt_lvl - spot; stop_move = spot - stop_lvl
        else:                                                   # bearish: target below, stop above spot
            tgt_lvl  = min(spot - 1, max(oc["support"], spot - exp_move))
            stop_lvl = max(spot + 1, min(oc["resistance"], spot + 0.6 * atr))
            tgt_move = spot - tgt_lvl; stop_move = stop_lvl - spot
        # option stop = bounded 30-50% of premium (options decay fast); target from the underlying move
        frac = min(0.50, max(0.30, (dlt * stop_move) / entry))
        tgt_prem = round(entry + dlt * tgt_move, 2)
        stop_prem = round(entry * (1 - frac), 2)
        net_entry, net_tgt, net_stop = entry, tgt_prem, stop_prem
        legs = f"BUY {SYMBOL} {expiry} {strike} {side} @ {entry}"
        if sell_strike:                                          # debit spread: sell further OTM
            S2 = leg(by, sell_strike, side); credit = round(S2["ltp"], 2)
            net_entry = round(entry - credit, 2)
            if net_entry <= 0: return None
            width = abs(sell_strike - strike)
            net_tgt = round(min(tgt_prem - credit, width), 2)             # capped by spread width
            net_stop = round(net_entry * (1 - frac), 2)
            legs = f"BUY {strike} {side} / SELL {sell_strike} {side} @ net {net_entry}"
        risk = round(net_entry - net_stop, 2); reward = round(net_tgt - net_entry, 2)
        rr = round(reward / risk, 2) if risk > 0 else np.nan
        risk_lot = risk * LOT; qty_lots = int((RISK_PCT * CAPITAL) // risk_lot) if risk_lot > 0 else 0
        return dict(strategy=kind_label, side=side, strike=strike, sell_strike=sell_strike or "",
                    moneyness=moneyness, instrument=legs, entry=net_entry, stop=net_stop, target=net_tgt,
                    rr=rr, delta=dlt, target_level=round(tgt_lvl), stop_level=round(stop_lvl),
                    iv=round(L["iv"], 1), oi=round(L["oi"]), lots=qty_lots,
                    risk_per_lot=round(risk * LOT), qty=qty_lots * LOT)

    cands = []
    if dirn > 0:
        cands.append(build("CE", atm - step, "ITM", "Long Call (ITM)"))
        cands.append(build("CE", atm, "ATM", "Long Call (ATM)"))
        cands.append(build("CE", atm, "ATM", "Bull Call Spread", sell_strike=oc["resistance"]))
    elif dirn < 0:
        cands.append(build("PE", atm + step, "ITM", "Long Put (ITM)"))
        cands.append(build("PE", atm, "ATM", "Long Put (ATM)"))
        cands.append(build("PE", atm, "ATM", "Bear Put Spread", sell_strike=oc["support"]))
    cands = [c for c in cands if c]

    def score_trade(c):
        sc = 0
        sc += min(30, max(0, (abs(pb["score"]) / 6) * 30))      # trend alignment
        sc += 25 if agree else 8                                # OI agrees with price
        sc += min(20, (pb["adx"] / 40) * 20)                    # momentum/strength
        rr = c["rr"] if c["rr"] == c["rr"] else 0
        sc += min(15, rr / 3 * 15)                              # R:R quality
        sc += 10 if iv_regime == "low" else 6 if iv_regime == "normal" else 2   # cheaper premium better
        if "Spread" in c["strategy"] and iv_regime == "high": sc += 4           # spreads suit high IV
        return round(min(100, sc))
    for c in cands: c["score"] = score_trade(c)
    cands.sort(key=lambda c: (c["score"], c["rr"] if c["rr"] == c["rr"] else 0), reverse=True)

    # P7 verdict on the top candidate
    if cands:
        top = cands[0]; rr = top["rr"] if top["rr"] == top["rr"] else 0
        if direction != "NEUTRAL" and confidence == "high" and rr >= 1.5 and days >= 2:
            verdict = "GO"
        elif direction != "NEUTRAL" and rr >= 1.0:
            verdict = "WATCH"
        else:
            verdict = "AVOID"
        for c in cands:
            c["tier"] = "TIER 1" if c["score"] >= 70 else "TIER 2" if c["score"] >= 55 else "TIER 3" if c["score"] >= 40 else "EXCLUDE"
        headline = f"{verdict}: {top['strategy']} — {top['instrument']} | stop {top['stop']} target {top['target']} | R:R {top['rr']} | {top['lots']} lot(s)"
    else:
        verdict = "AVOID"; top = {}
        headline = "AVOID: no high-confluence directional trade — price & OI not aligned. Stay flat / wait."

    plan = {
        "symbol": SYMBOL, "fetched_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "nse_timestamp": nse_ts, "expiry": expiry, "dte": days, "lot_size": LOT,
        "spot": round(spot, 2), "atm": atm, "direction": direction, "confidence": confidence,
        "verdict": verdict, "score": top.get("score", 0), "tier": top.get("tier", "—"),
        "headline": headline, "atm_iv": atm_iv, "iv_regime": iv_regime,
        "exp_move": exp_move, "straddle": straddle,
        "support": oc["support"], "resistance": oc["resistance"], "pcr": oc["pcr"], "max_pain": oc["max_pain"],
        "vcp_quality": vcp["vcp_quality"], "vcp_status": vcp["vcp_status"],
        "vcp_contractions": vcp["contractions"], "vcp_num": vcp["num_contractions"],
        "vcp_pivot": vcp["pivot"], "vcp_pct_from_pivot": vcp["pct_from_pivot"],
        "vcp_bo_vol": vcp["breakout_vol_ratio"], "vcp_entry_zone": vcp["entry_zone"],
        "vcp_decreasing": bool(vcp["depths_decreasing"]),
        "p1": f"Chain {SYMBOL} exp {expiry} (DTE {days}), spot {spot:.0f}, ATM {atm}, lot {LOT}. "
              f"OI support {oc['support']} / resistance {oc['resistance']}.",
        "p2": f"{pb['trend']} | px {pb['px']} vs EMA20 {pb['e20']}/50 {pb['e50']}/200 {pb['e200']} | "
              f"RSI {pb['rsi']} ADX {pb['adx']} MACDh {pb['macd_hist']} | price-score {pb['score']:+d} ({pb['signals']}).",
        "p3": f"PCR {oc['pcr']} | max-pain {oc['max_pain']} | nearby ChgOI CE {oc['ce_chg_oi']} / PE {oc['pe_chg_oi']} | "
              f"OI-score {oc['score']:+d} ({oc['signals']}).",
        "p4": f"ATM IV {atm_iv} ({iv_regime}) | implied expected move to expiry ~+/-{exp_move:.0f} pts (ATM straddle {straddle}).",
        "p5": f"Direction {direction} (price{pb['score']:+d} + OI{oc['score']:+d}); price/OI {'AGREE' if agree else 'DISAGREE'}; "
              f"ADX {'ok' if adx_ok else 'weak'} -> confidence {confidence}.",
        "p6": (f"Top: {top.get('strategy','none')} score {top.get('score',0)}/100 "
               f"(of {len(cands)} candidates)." if cands else "No directional candidates."),
        "p7": headline,
    }

    cols = ["strategy", "instrument", "side", "strike", "sell_strike", "moneyness",
            "entry", "stop", "target", "rr", "lots", "qty", "risk_per_lot",
            "target_level", "stop_level", "delta", "iv", "oi", "score", "tier"]
    tdf = pd.DataFrame(cands)
    (tdf[cols] if len(tdf) else pd.DataFrame(columns=cols)).to_csv("FNO_TRADES.csv", index=False)
    pd.DataFrame([plan]).to_csv("FNO_PLAN.csv", index=False)
    print(f"Wrote FNO_TRADES.csv ({len(cands)} candidates) + FNO_PLAN.csv")
    print(f"  {direction} / {confidence} -> {verdict}")
    print(f"  {headline}")


if __name__ == "__main__":
    main()
