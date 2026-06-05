"""Phase 3: Supply/Demand + SMC for all stocks (daily primary, weekly structure/zones).
Output: PHASE3_SMC.csv"""
import pickle, pandas as pd, numpy as np
import ta_smc as S

def weekly(df):
    w = df.set_index("date").resample("W").agg({"open":"first","high":"max","low":"min",
        "close":"last","volume":"sum"}).dropna().reset_index()
    return w

def fmt_zone(z):
    if not z: return "none"
    return f"{z['zlo']}-{z['zhi']} ({z['quality']}, {'FRESH' if z['fresh'] else 'tested'}, {z['dist_pct']}% away)"

def analyze(sym, df):
    df = df.reset_index(drop=True)
    px = float(df["close"].iloc[-1])
    R = {"symbol": sym, "close": round(px,2)}
    # --- A: zones (daily) ---
    dz = S.demand_zone(df); sz = S.supply_zone(df)
    R["demand_zone_D"] = fmt_zone(dz)
    R["demand_fresh"] = dz["fresh"] if dz else None
    R["demand_quality"] = dz["quality"] if dz else "none"
    R["near_demand"] = bool(dz and -3 <= dz["dist_pct"] <= 8) if dz else False
    R["supply_zone_D"] = (f"{sz['zlo']}-{sz['zhi']} ({sz['quality']}, "
                          f"{'FRESH' if sz['fresh'] else 'tested'}, {sz['dist_pct']}% above)") if sz else "none"
    R["near_supply"] = bool(sz and 0 <= sz["dist_pct"] <= 6) if sz else False
    # weekly zones (structure-level)
    wk = weekly(df)
    if len(wk) >= 30:
        wdz = S.demand_zone(wk, lookback=80); wsz = S.supply_zone(wk, lookback=80)
        R["demand_zone_W"] = fmt_zone(wdz); R["supply_zone_W"] = fmt_zone(wsz) if wsz else "none"
    else:
        R["demand_zone_W"] = R["supply_zone_W"] = "n/a (short)"
    # --- B1/B2 BoS / ChoCh (daily) ---
    bos, choch, allev = S.bos_choch(df)
    R["last_BoS"] = f"{bos['dir']} @ {bos['level']} on {bos['date']}" if bos else "none"
    R["last_ChoCh"] = f"{choch['dir']} @ {choch['level']} on {choch['date']}" if choch else "none"
    R["bos_dir"] = bos["dir"] if bos else "none"
    # --- B3 Order blocks ---
    bob, beob = S.order_blocks(df)
    R["bull_OB"] = (f"{bob['low']}-{bob['high']} ({bob['date']}, "
                    f"{'mitigated' if bob['mitigated'] else 'UNMITIGATED'})") if bob else "none"
    R["bear_OB"] = (f"{beob['low']}-{beob['high']} ({beob['date']}, "
                    f"{'mitigated' if beob['mitigated'] else 'UNMITIGATED'})") if beob else "none"
    R["bull_OB_unmitigated"] = (not bob["mitigated"]) if bob else False
    # --- B4 FVG ---
    ubull, ubear, nb, na = S.fvgs(df)
    R["unfilled_bull_FVG"] = ubull; R["unfilled_bear_FVG"] = ubear
    R["nearest_bull_FVG_below"] = f"{nb['bot']}-{nb['top']} ({nb['date']})" if nb else "none"
    R["nearest_bear_FVG_above"] = f"{na['bot']}-{na['top']} ({na['date']})" if na else "none"
    # --- B5 Liquidity ---
    bsl, ssl, swept, neh, nel = S.liquidity(df)
    R["buyside_liq_above"] = bsl if bsl else "none"
    R["sellside_liq_below"] = ssl if ssl else "none"
    R["liquidity_swept"] = swept
    R["equal_highs"] = neh; R["equal_lows"] = nel
    # --- B6 Premium/Discount ---
    zone, pos, rhi, rlo = S.premium_discount(df)
    R["pd_zone"] = zone; R["range_pos_pct"] = pos
    R["range_high"] = rhi; R["range_low"] = rlo
    R["in_discount"] = zone == "Discount"
    # --- B7 Market structure ---
    R["structure_D"] = S.market_structure(df)
    R["structure_W"] = S.market_structure(wk) if len(wk) >= 12 else "n/a"
    R["structure_aligned"] = (R["structure_D"].split()[0] == str(R["structure_W"]).split()[0]) \
                             if R["structure_W"] != "n/a" else None
    return R

if __name__ == "__main__":
    data = pickle.load(open("ohlc.pkl","rb"))
    rows=[]
    for i,(sym,df) in enumerate(data.items(),1):
        try: rows.append(analyze(sym,df))
        except Exception as e: rows.append({"symbol":sym,"error":f"{type(e).__name__}:{e}"})
        if i%80==0: print(f"  {i}/{len(data)}")
    out=pd.DataFrame(rows); out.to_csv("PHASE3_SMC.csv",index=False)
    print(f"DONE {len(out)} stocks -> PHASE3_SMC.csv")
    if "error" in out: print("errors:", out["error"].notna().sum())
    print("\nstructure_D:", out["structure_D"].value_counts().to_dict())
    print("pd_zone:", out["pd_zone"].value_counts().to_dict())
    print("liquidity_swept:", out["liquidity_swept"].value_counts().to_dict())
    print("bos_dir:", out["bos_dir"].value_counts().to_dict())
    print("near_supply:", out["near_supply"].sum(), "| near_demand:", out["near_demand"].sum(),
          "| bull_OB_unmitigated:", out["bull_OB_unmitigated"].sum())
