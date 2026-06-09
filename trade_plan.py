"""
Trade plans for the R5 forward-scan watchlist (FORWARD_SCAN_WATCHLIST.csv).
Re-fetches 1y OHLC per stock, computes entries / stops / targets / sizing / management
exactly per the user's spec. CAPITAL + risk are parameters (sizing scales linearly).

Outputs: TRADE_PLANS.csv (+ printed plans for the top tier)
"""
import time, threading, math, numpy as np, pandas as pd, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import ta_lib_local as T, ta_smc as S, ta_vcp_gann as VG

CAPITAL = 1_000_000        # Rs 10,00,000 (10 lakh) — change to your capital; shares scale linearly
RISK_PCT = 0.01            # 1% risk per trade (hard cap 2%)
RISK_RS = CAPITAL * RISK_PCT

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]
_l = threading.local()
def sess():
    if not hasattr(_l, "s"): _l.s = requests.Session(); _l.s.headers.update({"User-Agent": UA})
    return _l.s
def fetch(tkr):
    for a in range(3):
        try:
            r = sess().get(f"https://{HOSTS[a%2]}/v8/finance/chart/{tkr}",
                           params={"range": "1y", "interval": "1d"}, timeout=25)
            if r.status_code != 200: time.sleep(0.7 + a); continue
            res = r.json()["chart"]["result"][0]; q = res["indicators"]["quote"][0]
            return pd.DataFrame({"date": pd.to_datetime(res["timestamp"], unit="s"), "open": q["open"],
                "high": q["high"], "low": q["low"], "close": q["close"], "volume": q["volume"]}) \
                .dropna(subset=["close"]).sort_values("date").reset_index(drop=True)
        except Exception: time.sleep(0.5 * (a + 1))
    return None

def plan(row):
    tkr = f"{row['symbol']}.NS" if row["exchange"] == "NSE" else f"{row['symbol']}.BO"
    df = fetch(tkr)
    if df is None or len(df) < 200: return None
    o, h, l, c, v = (df[x] for x in ["open", "high", "low", "close", "volume"])
    px = float(c.iloc[-1])
    atr = float(T.atr(h, l, c).iloc[-1])
    e9 = float(T.ema(c, 9).iloc[-1]); e21 = float(T.ema(c, 21).iloc[-1])
    vcp = VG.detect_vcp(df); pivot = float(vcp["pivot"])
    bull_ob, _ = S.order_blocks(df); dz = S.demand_zone(df); sz = S.supply_zone(df)

    # ---- ENTRIES ----
    entry_aggr = round(px, 2)                                   # buy now if confirmations + close>pivot
    entry_consv = round(pivot * 1.002, 2)                       # breakout trigger above VCP pivot
    entry_pull = round(max(e9, dz["zhi"]) if dz else e9, 2)     # pullback to 9EMA / demand zone top

    # ---- STOP-LOSS candidates ----
    vcp_low = round(float(l.tail(15).min()), 2)                 # final-contraction low (recent tight base)
    ob_low = round(float(bull_ob["low"]), 2) if bull_ob else np.nan
    sl_ema21 = round(e21 * 0.99, 2)
    dz_low = round(float(dz["zlo"]), 2) if dz else np.nan
    cand = {"VCP_base_low": vcp_low, "OB_low": ob_low, "EMA21": sl_ema21, "Demand_low": dz_low}
    # choose tightest-but-logical: highest SL that is 1.5%-12% below entry
    valid = {k: s for k, s in cand.items() if pd.notna(s) and px * 0.88 <= s <= px * 0.985}
    if valid:
        sl_rule = max(valid, key=valid.get); SL = valid[sl_rule]
    else:
        SL = round(px - 1.5 * atr, 2); sl_rule = "1.5xATR (fallback)"
    risk_ps = round(entry_aggr - SL, 2)

    # ---- TARGETS ----
    t1 = round(entry_aggr + 3 * atr, 2)                         # 1x ATR x3
    shi, _ = T.swings(c, 3)
    overhead = [float(h.iloc[i]) for i in shi if h.iloc[i] > px * 1.005]
    t2 = round(min(overhead), 2) if overhead else round(float(h.tail(252).max()), 2)  # next resistance
    sq9_up = [lvl for k, lvl in VG.gann_square9(px).items() if "+" in k and lvl > px]
    t3 = round(min(sq9_up), 2) if sq9_up else np.nan            # Gann Sq9 next resistance
    base_low_mm = float(l.tail(40).min())
    t4 = round(pivot + (pivot - base_low_mm), 2)               # measured move = base height projected

    rr_t1 = round((t1 - entry_aggr) / risk_ps, 2) if risk_ps > 0 else np.nan
    # ---- SIZING (1% risk; cap position at full capital = no leverage; risk cap 2%) ----
    shares = int(RISK_RS / risk_ps) if risk_ps > 0 else 0
    pos_val = shares * entry_aggr
    if pos_val > CAPITAL:                                       # cap to no-leverage
        shares = int(CAPITAL / entry_aggr); pos_val = shares * entry_aggr
    actual_risk = round(shares * risk_ps, 0); actual_risk_pct = round(100 * actual_risk / CAPITAL, 2)
    be_trigger = round(entry_aggr + 1.5 * atr, 2)               # trail to breakeven here

    return {"rank": row["rank"], "symbol": row["symbol"], "sector": row["sector"],
            "num_conf": row["num_confirmations"], "CMP": entry_aggr,
            "entry_aggressive": entry_aggr, "entry_conservative": entry_consv, "entry_pullback": entry_pull,
            "SL_chosen": SL, "SL_rule": sl_rule, "SL_VCP_low": vcp_low, "SL_OB_low": ob_low,
            "SL_EMA21": sl_ema21, "SL_Demand_low": dz_low, "risk_per_share": risk_ps,
            "ATR": round(atr, 2), "T1_atrx3": t1, "T2_resistance": t2, "T3_gann_sq9": t3,
            "T4_measured_move": t4, "RR_at_T1": rr_t1,
            "shares_10L_1pct": shares, "position_value": round(pos_val, 0),
            "actual_risk_rs": actual_risk, "actual_risk_pct": actual_risk_pct,
            "BE_trail_at": be_trigger, "weekly_exit": "close < 21EMA (weekly)"}

if __name__ == "__main__":
    wl = pd.read_csv("FORWARD_SCAN_WATCHLIST.csv", dtype={"symbol": str})
    rows = wl.to_dict("records")
    out = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(plan, r) for r in rows]
        for f in as_completed(futs):
            r = f.result()
            if r: out.append(r)
    P = pd.DataFrame(out).sort_values("rank").reset_index(drop=True)
    P.to_csv("TRADE_PLANS.csv", index=False)
    print(f"trade plans built for {len(P)}/{len(wl)} stocks (capital=Rs{CAPITAL:,}, risk={RISK_PCT*100:.0f}%/trade) -> TRADE_PLANS.csv")
    print(f"R:R at T1 -> min {P['RR_at_T1'].min()} median {P['RR_at_T1'].median()} max {P['RR_at_T1'].max()}")
    print(f"trades meeting >=1:3 R:R at T1: {int((P['RR_at_T1']>=3).sum())}/{len(P)}")
    print("\n=== TRADE PLANS — top tier (5-confirmation) ===")
    for _, r in P[P["num_conf"] >= 5].iterrows():
        print(f"\n[{r['symbol']}] {r['sector']} | conf {r['num_conf']}/6 | CMP {r['CMP']}")
        print(f"  ENTRY  aggr {r['entry_aggressive']} | consv>{r['entry_conservative']} (breakout+vol) | pullback {r['entry_pullback']} (9EMA/DZ)")
        print(f"  STOP   {r['SL_chosen']} via {r['SL_rule']}  (risk/sh {r['risk_per_share']})  [VCP {r['SL_VCP_low']} OB {r['SL_OB_low']} 21EMA {r['SL_EMA21']} DZ {r['SL_Demand_low']}]")
        print(f"  TGTS   T1 {r['T1_atrx3']} (ATRx3, R:R {r['RR_at_T1']}) | T2 {r['T2_resistance']} (resist) | T3 {r['T3_gann_sq9']} (Gann) | T4 {r['T4_measured_move']} (measured)")
        print(f"  SIZE   {r['shares_10L_1pct']} sh = Rs{r['position_value']:,.0f} | risk Rs{r['actual_risk_rs']:,.0f} ({r['actual_risk_pct']}%) | BE-trail at {r['BE_trail_at']}")
