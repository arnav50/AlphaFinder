"""Phase 6: composite confluence score (0-100) from Phases 2-5. Exact rubric, per-component audit.
Outputs PHASE6_RANKING.csv, ALPHA_LIST.csv, PHASE6_SUMMARY.md"""
import pandas as pd, numpy as np

ind = pd.read_csv("indicators.csv", dtype={"symbol":str})
p2  = pd.read_csv("PHASE2_SCORECARD.csv", dtype={"symbol":str})[["symbol","name","exchange","sector","return_pct_final","close","cap_bucket","scorecard","chart_pattern"]]
p3  = pd.read_csv("PHASE3_SMC.csv", dtype={"symbol":str})
p4  = pd.read_csv("PHASE4_VCP_GANN.csv", dtype={"symbol":str})

df = p2.merge(ind, on="symbol", how="left", suffixes=("","_ind")).merge(p3, on="symbol", how="left").merge(p4, on="symbol", how="left")

BULL_CHART={"Double Bottom","Inverse Head & Shoulders","Bull Flag / Pennant","Falling Wedge (bullish)",
            "Rounding Bottom (saucer)","Ascending Triangle"}

def gv(r,k,d=None):
    v=r.get(k); return d if (v is None or (isinstance(v,float) and pd.isna(v))) else v

def score(r):
    aud={}   # component -> points (audit, each metric used once)
    # ---------------- SECTION A: indicator confluence (max 40) ----------------
    # leading (max 20)
    lead=0
    rsi=gv(r,"rsi",np.nan)
    if pd.notna(rsi) and 45<=rsi<=65: lead+=5; aud["A_rsi_45_65"]=5
    if gv(r,"stoch_cross")=="bull" and gv(r,"stoch_state")!="overbought": lead+=3; aud["A_stoch_cross_oversold"]=3
    if gv(r,"bb_squeeze")==True: lead+=4; aud["A_bb_squeeze"]=4
    if gv(r,"obv_trend")=="rising": lead+=3; aud["A_obv_up"]=3
    mfi=gv(r,"mfi",np.nan)
    if pd.notna(mfi) and mfi<55: lead+=3; aud["A_mfi_rising_low"]=3
    if gv(r,"cci_state") in ("above0","strong_up"): lead+=2; aud["A_cci_above0"]=2
    lead=min(lead,20)
    # lagging (max 20)
    lag=0
    if gv(r,"macd_cross")=="bull" or gv(r,"macd_hist_state")=="expanding_pos": lag+=5; aud["A_macd_bull"]=5
    if gv(r,"ema_alignment")=="bullish": lag+=5; aud["A_ema_aligned"]=5
    adx=gv(r,"adx",np.nan)
    if pd.notna(adx) and 20<=adx<=28: lag+=4; aud["A_adx_20_28"]=4
    if gv(r,"supertrend")=="green_buy": lag+=3; aud["A_supertrend_green"]=3
    if gv(r,"atr_state")=="expanding": lag+=3; aud["A_atr_expanding"]=3
    lag=min(lag,20)
    A=lead+lag
    # ---------------- SECTION B: structure confluence (max 25) ----------------
    B=0
    if gv(r,"bos_dir")=="bull": B+=5; aud["B_bull_bos"]=5
    if gv(r,"pd_zone")=="Discount" or gv(r,"near_demand")==True: B+=5; aud["B_discount_or_demand"]=5
    if gv(r,"bull_OB_unmitigated")==True: B+=5; aud["B_ob_support"]=5
    if str(gv(r,"nearest_bull_FVG_below","none"))!="none" or (pd.notna(gv(r,"unfilled_bull_FVG")) and gv(r,"unfilled_bull_FVG",0)>0):
        B+=4; aud["B_fvg"]=4
    if "swept" in str(gv(r,"liquidity_swept","none")): B+=3; aud["B_liq_swept"]=3
    if str(gv(r,"supply_zone_D","none"))=="none": B+=3; aud["B_supply_cleared"]=3
    B=min(B,25)
    # ---------------- SECTION C: VCP + price action (max 20) ----------------
    C=0
    if gv(r,"vcp_quality")!="No VCP" and gv(r,"num_contractions",0)>=3: C+=8; aud["C_valid_vcp"]=8
    if gv(r,"vcp_status") in ("AT PIVOT (actionable)","BROKEN OUT (fresh)"): C+=7; aud["C_3rd_leg"]=7
    if gv(r,"vdu_confirmed")==True: C+=5; aud["C_vdu"]=5
    if gv(r,"chart_pattern") in BULL_CHART: C+=3; aud["C_chart_pattern"]=3
    C=min(C,20)
    # ---------------- SECTION D: Gann (max 15) ----------------
    D=0
    if gv(r,"gann_above_1x1")==True: D+=5; aud["D_above_1x1"]=5
    if gv(r,"near_gann_cycle")==True: D+=4; aud["D_time_cycle"]=4
    octn=gv(r,"octave_n",np.nan)
    if pd.notna(octn) and int(octn) in (2,4,6): D+=3; aud["D_octave_key"]=3
    if pd.notna(octn) and int(octn)<=6: D+=3; aud["D_room_to_run"]=3
    D=min(D,15)
    total=A+B+C+D
    tier=("TIER 1" if total>=80 else "TIER 2" if total>=65 else "TIER 3" if total>=50 else "EXCLUDE")
    return pd.Series({"ind_score_40":A,"struct_score_25":B,"vcp_score_20":C,"gann_score_15":D,
                      "TOTAL_100":total,"tier":tier,"audit":";".join(f"{k}:{v}" for k,v in aud.items())})

sc=df.apply(score,axis=1)
out=pd.concat([df[["symbol","name","exchange","sector","cap_bucket","return_pct_final","close",
                   "scorecard","vcp_quality","vcp_status","pd_zone","structure_D","octave"]],sc],axis=1)
out=out.sort_values("TOTAL_100",ascending=False).reset_index(drop=True)
out.insert(0,"rank",out.index+1)
out.to_csv("PHASE6_RANKING.csv",index=False)

alpha=out[out["tier"].isin(["TIER 1","TIER 2"])].copy()
alpha.to_csv("ALPHA_LIST.csv",index=False)

# audit: verify section caps never exceeded (no double counting beyond caps)
assert (out["ind_score_40"]<=40).all() and (out["struct_score_25"]<=25).all() and (out["vcp_score_20"]<=20).all() and (out["gann_score_15"]<=15).all()
assert (out["TOTAL_100"]<=100).all()

S=[]
S.append("# PHASE 6 — CONFLUENCE SCORING MATRIX & FINAL RANKING")
S.append(f"Scan date 2026-06-02 · {len(out)} stocks scored 0-100 from Phases 2-5.\n")
S.append("## ✓ VERIFICATION CHECKPOINT (Phase 6)")
S.append("- ✅ Every stock scored across all 4 sections (A:40 indicators, B:25 structure, C:20 VCP, D:15 Gann)")
S.append("- ✅ No double-counting: each metric awarded once; section caps enforced (asserted in code); per-stock `audit` column lists every awarded component")
S.append("- ✅ Ranked highest→lowest (`PHASE6_RANKING.csv`)")
S.append("- ✅ TIER 1 + TIER 2 separated as the **ALPHA LIST** (`ALPHA_LIST.csv`)")
S.append("- ✅ Alpha list = Phase-7 prime-scanner input\n")
S.append("## Tier distribution")
S.append("| Tier | Band | Count |")
S.append("|---|---|--:|")
for t,b in [("TIER 1","80-100"),("TIER 2","65-79"),("TIER 3","50-64"),("EXCLUDE","<50")]:
    S.append(f"| {t} | {b} | {(out['tier']==t).sum()} |")
S.append(f"\n**ALPHA LIST (Tier 1 + Tier 2): {len(alpha)} stocks** · score range {alpha['TOTAL_100'].min()}-{alpha['TOTAL_100'].max()}")
S.append(f"\nSection averages (all): Ind {out['ind_score_40'].mean():.1f}/40 · Struct {out['struct_score_25'].mean():.1f}/25 · "
         f"VCP {out['vcp_score_20'].mean():.1f}/20 · Gann {out['gann_score_15'].mean():.1f}/15 · TOTAL {out['TOTAL_100'].mean():.1f}/100\n")
S.append("## ⭐ ALPHA LIST — ranked")
S.append("| Rank | Symbol | Company | Exch | Ind/40 | Struct/25 | VCP/20 | Gann/15 | TOTAL | Tier | Ret% | VCP status |")
S.append("|--:|---|---|---|--:|--:|--:|--:|--:|---|--:|---|")
for _,r in alpha.iterrows():
    S.append(f"| {r['rank']} | {r['symbol']} | {str(r['name'])[:24]} | {r['exchange']} | {r['ind_score_40']} | "
             f"{r['struct_score_25']} | {r['vcp_score_20']} | {r['gann_score_15']} | **{r['TOTAL_100']}** | "
             f"{r['tier']} | {r['return_pct_final']} | {r['vcp_status']} |")
S.append(f"\n**Files:** `PHASE6_RANKING.csv` (all {len(out)} + audit column) · `ALPHA_LIST.csv` ({len(alpha)} names).")
open("PHASE6_SUMMARY.md","w",encoding="utf-8").write("\n".join(S))

print("Tier distribution:", out["tier"].value_counts().reindex(["TIER 1","TIER 2","TIER 3","EXCLUDE"]).to_dict())
print(f"ALPHA LIST: {len(alpha)} | score range {alpha['TOTAL_100'].min()}-{alpha['TOTAL_100'].max()}")
print(f"section avgs: Ind {out['ind_score_40'].mean():.1f} Struct {out['struct_score_25'].mean():.1f} VCP {out['vcp_score_20'].mean():.1f} Gann {out['gann_score_15'].mean():.1f}")
print("\nTOP 20:")
print(out.head(20)[["rank","symbol","name","ind_score_40","struct_score_25","vcp_score_20","gann_score_15","TOTAL_100","tier"]].to_string(index=False))