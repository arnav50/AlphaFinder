"""
VCP (Minervini) + 3rd-leg breakout analysis for the Phase-1 universe.
Reuses ta_vcp_gann.detect_vcp for the contraction/volume/pivot core; adds the
leg-structure (Leg1.Base1.Leg2.Base2.Leg3), Fibonacci extension, highest-pivot,
volume-expansion, and time-contraction layer on top.

'Move start' = base low = lowest close in trailing ~180 trading days (same proxy as the
other passes); leg structure is read from move_start -> now.

Per stock:
  VCP    : contractions C1/C2/C3 (depth%), depths decreasing?, VDU (volume dry-up),
           pivot, breakout volume >40% above avg?, final-contraction tightness (<10-15%)
  3rd LEG: leg count, leg-3 volume expansion vs prior legs, leg-3 = highest pivot?,
           Leg3/Leg1 Fib ratio (~1.272 / ~1.618), 52w-high clearance, time contraction
  VCP+Leg Score (1-10) via a transparent additive rubric.

Outputs: VCP_ANALYSIS.csv (full) + VCP_SCORECARD.csv (requested 6-col table)
"""
import pickle, re, numpy as np, pandas as pd
import ta_vcp_gann as VG
import ta_lib_local as T

def alt_pivots(seg):
    """alternating L/H pivots starting from the base low at index 0."""
    c = seg["close"]
    hi, lo = T.swings(c, 3)
    raw = [(0, "L", float(seg["low"].iloc[0]))]
    raw += sorted([(i, "H", float(seg["high"].iloc[i])) for i in hi if i > 3]
                  + [(i, "L", float(seg["low"].iloc[i])) for i in lo if i > 3], key=lambda x: x[0])
    # add the current bar as a terminal high (the breakout being analysed)
    last = len(seg) - 1
    raw.append((last, "H", float(seg["high"].iloc[last])))
    # reduce to strict alternation: keep most-extreme of consecutive same-type
    out = []
    for p in raw:
        if out and out[-1][1] == p[1]:
            if (p[1] == "H" and p[2] > out[-1][2]) or (p[1] == "L" and p[2] < out[-1][2]):
                out[-1] = p
        else:
            out.append(p)
    return out

def extract_legs(seg):
    piv = alt_pivots(seg)
    legs, bases = [], []
    k = 0
    while k + 1 < len(piv):
        a, b = piv[k], piv[k + 1]
        if a[1] == "L" and b[1] == "H" and b[2] > a[2]:
            vol = float(seg["volume"].iloc[a[0]:b[0] + 1].mean()) if b[0] > a[0] else float(seg["volume"].iloc[a[0]])
            legs.append({"t_i": a[0], "t_p": a[2], "p_i": b[0], "p_p": b[2],
                         "range": b[2] - a[2], "gain_pct": (b[2] / a[2] - 1) * 100, "vol": vol})
            # base after this peak = peak -> next trough
            if k + 2 < len(piv) and piv[k + 2][1] == "L":
                bases.append({"dur": piv[k + 2][0] - b[0]})
            k += 1
        else:
            k += 1
    return legs, bases

def parse_depths(contr_str):
    return [float(x) for x in re.findall(r"C\d+:-([\d.]+)%", contr_str)]

def analyze(sym, df):
    df = df.reset_index(drop=True)
    n = len(df); px = float(df["close"].iloc[-1])
    R = {"symbol": sym, "CMP": round(px, 2), "bars_daily": n}
    vcp = VG.detect_vcp(df)
    R.update({k: vcp[k] for k in ["num_contractions", "contractions", "depths_decreasing",
              "dur_decreasing", "vdu_confirmed", "vdu_ratio", "pivot", "pct_from_pivot",
              "breakout_vol_ratio", "near_52w_high", "vcp_status", "vcp_quality", "pct_above_52w_low"]})
    depths = parse_depths(vcp["contractions"])
    R["C1_pct"] = depths[0] if len(depths) >= 1 else np.nan
    R["C2_pct"] = depths[1] if len(depths) >= 2 else np.nan
    R["C3_pct"] = depths[2] if len(depths) >= 3 else np.nan
    R["final_contraction_tight"] = bool(depths and depths[-1] <= 15)
    R["breakout_vol_gt40pct"] = bool(pd.notna(vcp["breakout_vol_ratio"]) and vcp["breakout_vol_ratio"] >= 1.4)

    # ---- 3rd-leg structure ----
    W = min(n, 180)
    start = int(df["close"].tail(W).idxmin())
    R["move_start_date"] = df["date"].iloc[start].date().isoformat()
    seg = df.iloc[start:].reset_index(drop=True)
    legs, bases = extract_legs(seg)
    R["num_legs"] = len(legs)
    R["leg_gains_pct"] = " | ".join(f"L{j+1}:+{lg['gain_pct']:.0f}%" for j, lg in enumerate(legs[:3])) or "none"

    fib_ratio = np.nan; fib_label = "n/a"; highest_pivot = False; vol_expand = False; time_contract = False
    if len(legs) >= 3:
        l1, l2, l3 = legs[0], legs[1], legs[2]
        if l1["range"] > 0:
            fib_ratio = l3["range"] / l1["range"]
            if abs(fib_ratio - 1.272) <= 0.13: fib_label = "~1.272x"
            elif abs(fib_ratio - 1.618) <= 0.13: fib_label = "~1.618x"
            else: fib_label = f"{fib_ratio:.2f}x"
        peaks = [lg["p_p"] for lg in legs]
        highest_pivot = l3["p_p"] >= max(peaks) - 1e-9
        vol_expand = l3["vol"] > l1["vol"] and l3["vol"] > l2["vol"]
        if len(bases) >= 2:
            time_contract = bases[1]["dur"] <= bases[0]["dur"]
    R["fib_ratio_L3_L1"] = round(float(fib_ratio), 2) if pd.notna(fib_ratio) else np.nan
    R["fib_extension"] = fib_label
    R["leg3_highest_pivot"] = highest_pivot
    R["leg3_vol_expansion"] = vol_expand
    R["time_contraction"] = time_contract
    R["cleared_52w_high"] = bool(px >= float(df["high"].tail(252).max()) * 0.999)

    R["third_leg_confirmed"] = bool(len(legs) >= 3 and highest_pivot and vol_expand)

    # ---- VCP+Leg Score (1-10) ----
    raw, mx = 0.0, 0.0
    def add(cond, w):
        nonlocal raw, mx; mx += w; raw += (w if cond else 0)
    add(R["num_contractions"] >= 3, 1.5)
    add(R["num_contractions"] == 2, 0.75)
    add(R["depths_decreasing"], 1.0)
    add(R["vdu_confirmed"], 1.0)
    add(R["final_contraction_tight"], 1.0)
    add(R["breakout_vol_gt40pct"], 1.0)
    add(R["near_52w_high"], 0.5)
    add(len(legs) >= 3, 1.0)
    add(R["leg3_highest_pivot"], 1.0)
    add(R["leg3_vol_expansion"], 1.0)
    add(fib_label in ("~1.272x", "~1.618x"), 0.5)
    add(R["time_contraction"], 0.5)
    R["vcp_leg_score_10"] = int(np.clip(round(raw / mx * 10), 1, 10)) if mx else 1
    return R

if __name__ == "__main__":
    fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
    meta = fin.set_index("symbol")[["name", "exchange"]].to_dict("index")
    data = pickle.load(open("ohlc.pkl", "rb"))
    rows = []
    for i, sym in enumerate(fin["symbol"], 1):
        df = data.get(sym)
        if df is None or len(df) < 60:
            rows.append({"symbol": sym, "note": "insufficient OHLC"}); continue
        try:
            r = analyze(sym, df)
            r["name"] = meta.get(sym, {}).get("name", ""); r["exchange"] = meta.get(sym, {}).get("exchange", "")
            rows.append(r)
        except Exception as e:
            rows.append({"symbol": sym, "note": f"{type(e).__name__}:{e}"})
        if i % 80 == 0: print(f"  {i}/{len(fin)}")

    out = pd.DataFrame(rows).sort_values("vcp_leg_score_10", ascending=False, na_position="last").reset_index(drop=True)
    full_cols = ["symbol", "name", "exchange", "CMP", "move_start_date", "vcp_quality", "vcp_status",
                 "num_contractions", "contractions", "C1_pct", "C2_pct", "C3_pct",
                 "depths_decreasing", "final_contraction_tight", "vdu_confirmed", "vdu_ratio",
                 "pivot", "pct_from_pivot", "breakout_vol_ratio", "breakout_vol_gt40pct", "near_52w_high",
                 "num_legs", "leg_gains_pct", "leg3_highest_pivot", "leg3_vol_expansion",
                 "fib_ratio_L3_L1", "fib_extension", "cleared_52w_high", "time_contraction",
                 "third_leg_confirmed", "bars_daily", "vcp_leg_score_10"]
    full_cols = [c for c in full_cols if c in out.columns]
    out[full_cols].to_csv("VCP_ANALYSIS.csv", index=False)

    summ = pd.DataFrame({
        "Stock": out["symbol"],
        "VCP Contractions": out["contractions"],
        "Pivot Price": out["pivot"],
        "3rd Leg confirmed (Y/N)": out["third_leg_confirmed"].map({True: "Y", False: "N"}),
        "Fib Extension Level": out["fib_extension"],
        "VCP+Leg Score (1-10)": out["vcp_leg_score_10"],
    })
    summ.to_csv("VCP_SCORECARD.csv", index=False)

    nn = int(out["vcp_leg_score_10"].notna().sum())
    print(f"\nDONE. analysed {nn} stocks -> VCP_ANALYSIS.csv + VCP_SCORECARD.csv")
    print("vcp_quality:", out["vcp_quality"].value_counts().to_dict())
    print(f"3rd-leg confirmed: {int(out['third_leg_confirmed'].sum())} | breakout vol >40%: {int(out['breakout_vol_gt40pct'].sum())} | "
          f">=3 contractions: {int((out['num_contractions']>=3).sum())} | fib ~1.27/1.62: {int(out['fib_extension'].isin(['~1.272x','~1.618x']).sum())}")
    print("\n=== TOP 20 (by VCP+Leg score) ===")
    print(summ.head(20).to_string(index=False))
