"""
Smart-Money-Concepts + Supply/Demand mapping for the Phase-1 universe, anchored to the
BASE that preceded each 25%+ move. Reuses ta_smc.py primitives on pre-move slices.

'Move start' = base low = lowest close in trailing ~180 trading days (same proxy as the
other passes). Zones/OB are detected on df[:start+impulse] so the 'most recent' structure
is the base of THIS move; FVG on the impulse window; BOS/CHoCH on df[:start+30].

Per stock:
  DEMAND ZONE : high/low, fresh vs tested, quality, DBR vs RBR classification
  ORDER BLOCK : bullish OB (last bearish candle before the impulse) high/low, mitigated?
  FVG         : bullish 3-candle imbalance created during the initial impulse (levels)
  BOS / CHoCH : breakout level + date; was there a bullish CHoCH before the BOS?
  LIQUIDITY   : stop-hunt below a prior low before the move? (Y/N)
  PREMIUM/DISC: was the entry in discount (<50% of prior range)?
  SMC Score (1-10) via a transparent additive rubric.

Outputs: SMC_ANALYSIS.csv (full) + SMC_SCORECARD.csv (requested 7-col table)
"""
import pickle, numpy as np, pandas as pd
import ta_smc as S

def dbr_or_rbr(df, start, base_lo, base_hi):
    """classify demand base: Drop-Base-Rally vs Rally-Base-Rally by the leg INTO the base."""
    pre = df["close"].iloc[max(0, start - 8):max(1, start - 1)]
    if len(pre) < 3:
        return "n/a"
    return "Drop-Base-Rally (DBR)" if pre.iloc[0] > pre.iloc[-1] else "Rally-Base-Rally (RBR)"

def analyze(sym, df):
    df = df.reset_index(drop=True)
    c = df["close"]; n = len(df); px = float(c.iloc[-1])
    R = {"symbol": sym, "CMP": round(px, 2), "bars_daily": n}
    W = min(n, 180)
    start = int(c.tail(W).idxmin())
    R["move_start_date"] = df["date"].iloc[start].date().isoformat()
    imp_end = min(n, start + 12)
    pre_slice = df.iloc[:imp_end].reset_index(drop=True)        # base + first impulse

    # ---- DEMAND ZONE (the base before the move) ----
    dz = S.demand_zone(pre_slice)
    if dz:
        R.update({"demand_low": dz["zlo"], "demand_high": dz["zhi"], "demand_fresh": dz["fresh"],
                  "demand_tested": dz["tested"], "demand_quality": dz["quality"], "demand_date": dz["date"]})
        R["demand_pattern"] = dbr_or_rbr(df, start, dz["zlo"], dz["zhi"])
    else:
        R.update({"demand_low": np.nan, "demand_high": np.nan, "demand_fresh": None,
                  "demand_tested": None, "demand_quality": "none", "demand_date": "", "demand_pattern": "n/a"})

    # ---- ORDER BLOCK (last bearish candle before the explosive bullish impulse) ----
    bull_ob, _ = S.order_blocks(pre_slice)
    if bull_ob:
        R.update({"ob_low": bull_ob["low"], "ob_high": bull_ob["high"],
                  "ob_mitigated": bull_ob["mitigated"], "ob_date": bull_ob["date"]})
    else:
        R.update({"ob_low": np.nan, "ob_high": np.nan, "ob_mitigated": None, "ob_date": ""})

    # ---- FVG during the initial impulse ----
    imp = df.iloc[max(0, start - 2):imp_end + 3].reset_index(drop=True)
    nub, nbe, near_below, _ = S.fvgs(imp, look=len(imp))
    R["impulse_bull_fvgs"] = nub
    if near_below:
        R["fvg_low"] = near_below["bot"]; R["fvg_high"] = near_below["top"]; R["fvg_date"] = near_below["date"]
    else:
        R["fvg_low"] = np.nan; R["fvg_high"] = np.nan; R["fvg_date"] = ""

    # ---- BOS / CHoCH around the move start ----
    bo_slice = df.iloc[:min(n, start + 30)].reset_index(drop=True)
    _, _, clean = S.bos_choch(bo_slice)
    bull_bos = next((e for e in clean if e["dir"] == "bull" and e["i"] >= start), None)
    if bull_bos is None:
        bull_bos = next((e for e in reversed(clean) if e["dir"] == "bull"), None)
    R["bos_level"] = bull_bos["level"] if bull_bos else np.nan
    R["bos_date"] = bull_bos["date"] if bull_bos else ""
    # CHoCH = a bear->bull flip at/before the BOS
    choch = False
    if bull_bos:
        for k in range(1, len(clean)):
            if clean[k]["dir"] == "bull" and clean[k-1]["dir"] == "bear" and clean[k]["i"] <= bull_bos["i"]:
                choch = True; break
    R["choch_before_bos"] = choch

    # ---- LIQUIDITY sweep (stop-hunt below a prior low) before the move ----
    liq_slice = df.iloc[:min(n, start + 4)].reset_index(drop=True)
    _, _, swept, _, _ = S.liquidity(liq_slice)
    R["liquidity_swept_desc"] = swept
    # direct fallback: low broke prior swing low then closed back above, in [start-8, start+2]
    direct = False
    if start >= 20:
        prior_low = float(df["low"].iloc[start-20:start-5].min())
        for i in range(max(0, start-8), min(n, start+3)):
            if df["low"].iloc[i] < prior_low and df["close"].iloc[i] > prior_low:
                direct = True; break
    R["liquidity_sweep"] = bool("sell-side" in swept or direct)

    # ---- PREMIUM / DISCOUNT of the entry (vs prior range) ----
    rng_slice = df.iloc[max(0, start-120):start+1]
    hi = float(rng_slice["high"].max()); lo = float(rng_slice["low"].min())
    pos = (float(c.iloc[start]) - lo) / (hi - lo) * 100 if hi > lo else 50.0
    R["entry_range_pos_pct"] = round(pos, 1)
    R["entry_in_discount"] = bool(pos < 50)

    # ---- SMC Score (1-10) ----
    raw, mx = 0.0, 0.0
    def add(cond, w):
        nonlocal raw, mx; mx += w; raw += (w if cond else 0)
    add(dz is not None, 2.0)
    add(dz is not None and dz.get("fresh"), 1.0)
    add(dz is not None and dz.get("quality") in ("Strong", "Moderate"), 0.5)
    add(bull_ob is not None, 1.0)
    add(bull_ob is not None and not bull_ob.get("mitigated"), 0.5)
    add(nub > 0, 1.0)
    add(bull_bos is not None, 1.5)
    add(choch, 1.0)
    add(R["liquidity_sweep"], 1.0)
    add(R["entry_in_discount"], 0.5)
    R["smc_score_10"] = int(np.clip(round(raw / mx * 10), 1, 10)) if mx else 1
    return R

if __name__ == "__main__":
    fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
    meta = fin.set_index("symbol")[["name", "exchange"]].to_dict("index")
    data = pickle.load(open("ohlc.pkl", "rb"))
    rows = []
    for i, sym in enumerate(fin["symbol"], 1):
        df = data.get(sym)
        if df is None or len(df) < 40:
            rows.append({"symbol": sym, "note": "insufficient OHLC"}); continue
        try:
            r = analyze(sym, df)
            r["name"] = meta.get(sym, {}).get("name", ""); r["exchange"] = meta.get(sym, {}).get("exchange", "")
            rows.append(r)
        except Exception as e:
            rows.append({"symbol": sym, "note": f"{type(e).__name__}:{e}"})
        if i % 80 == 0: print(f"  {i}/{len(fin)}")

    out = pd.DataFrame(rows).sort_values("smc_score_10", ascending=False, na_position="last").reset_index(drop=True)
    full_cols = ["symbol", "name", "exchange", "CMP", "move_start_date",
                 "demand_low", "demand_high", "demand_fresh", "demand_tested", "demand_quality",
                 "demand_pattern", "demand_date",
                 "ob_low", "ob_high", "ob_mitigated", "ob_date",
                 "impulse_bull_fvgs", "fvg_low", "fvg_high", "fvg_date",
                 "bos_level", "bos_date", "choch_before_bos",
                 "liquidity_sweep", "liquidity_swept_desc", "entry_range_pos_pct", "entry_in_discount",
                 "bars_daily", "smc_score_10"]
    full_cols = [c for c in full_cols if c in out.columns]
    out[full_cols].to_csv("SMC_ANALYSIS.csv", index=False)

    def lvl(a, b):
        if pd.isna(a) or pd.isna(b): return "n/a"
        return f"{a}-{b}"
    summ = pd.DataFrame({
        "Stock": out["symbol"],
        "Demand Zone Levels": out.apply(lambda r: lvl(r.get("demand_low"), r.get("demand_high")), axis=1),
        "OB Level": out.apply(lambda r: lvl(r.get("ob_low"), r.get("ob_high")), axis=1),
        "FVG Level": out.apply(lambda r: lvl(r.get("fvg_low"), r.get("fvg_high")), axis=1),
        "BOS Level": out["bos_level"],
        "Liquidity Sweep (Y/N)": out["liquidity_sweep"].map({True: "Y", False: "N"}),
        "SMC Score (1-10)": out["smc_score_10"],
    })
    summ.to_csv("SMC_SCORECARD.csv", index=False)

    nn = int(out["smc_score_10"].notna().sum())
    print(f"\nDONE. analysed {nn} stocks -> SMC_ANALYSIS.csv + SMC_SCORECARD.csv")
    print(f"demand zone found: {int(out['demand_high'].notna().sum())} | bull OB: {int(out['ob_high'].notna().sum())} | "
          f"BOS: {int(out['bos_level'].notna().sum())} | CHoCH: {int(out['choch_before_bos'].sum())} | "
          f"liq sweep: {int(out['liquidity_sweep'].sum())} | discount entry: {int(out['entry_in_discount'].sum())}")
    print("\n=== TOP 20 (by SMC score) ===")
    print(summ.head(20).to_string(index=False))
