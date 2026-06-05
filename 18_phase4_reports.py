"""Append Phase-4 VCP+Gann to reports/<symbol>.md and write PHASE4_SUMMARY.md."""
import os, pandas as pd

v = pd.read_csv("PHASE4_VCP_GANN.csv", dtype={"symbol": str})
sc = pd.read_csv("PHASE2_SCORECARD.csv", dtype={"symbol": str})[["symbol","name","scorecard","total_score","return_pct_final"]]
smc = pd.read_csv("PHASE3_SMC.csv", dtype={"symbol": str})[["symbol","pd_zone","structure_D","bull_OB_unmitigated","near_demand"]]
m = v.merge(sc, on="symbol", how="left").merge(smc, on="symbol", how="left")

def g(r,k,d="n/a"):
    val=r.get(k); return d if pd.isna(val) else val

for _, r in m.iterrows():
    path=f"reports/{r['symbol']}.md"
    if not os.path.exists(path): continue
    L=["\n\n---\n## PHASE 4 — VCP + Gann"]
    L.append("### A. Volatility Contraction Pattern (Minervini)")
    L.append(f"- **Prior uptrend:** {g(r,'prior_uptrend')} ({g(r,'pct_above_52w_low')}% above 52w low, above EMA200: {g(r,'above_ema200')})")
    L.append(f"- **Contractions ({g(r,'num_contractions')}):** {g(r,'contractions')}")
    L.append(f"- **Depths decreasing:** {g(r,'depths_decreasing')} | **Duration decreasing:** {g(r,'dur_decreasing')} | "
             f"**Volume dry-up (VDU):** {g(r,'vdu_confirmed')} (vol ratio {g(r,'vdu_ratio')})")
    L.append(f"- **Near 52w high:** {g(r,'near_52w_high')} | **Pivot:** {g(r,'pivot')} | **% from pivot:** {g(r,'pct_from_pivot')}%")
    L.append(f"- **Breakout vol ratio (today/50d):** {g(r,'breakout_vol_ratio')} | **close pos in range:** {g(r,'breakout_close_pos')}")
    L.append(f"- **🏆 VCP QUALITY: {g(r,'vcp_quality')}** | **3rd-leg status: {g(r,'vcp_status')}** | entry zone {g(r,'entry_zone')}")
    L.append("### B. Gann Theory")
    L.append(f"- **Angles (auto-scaled from swing low {g(r,'gann_low_price')} on {g(r,'gann_low_date')}):** "
             f"1x1={g(r,'gann_g1x1')} 2x1={g(r,'gann_g2x1')} 1x2={g(r,'gann_g1x2')} → **{g(r,'gann_gann_trend')}** (above 1x1: {g(r,'gann_above_1x1')})")
    L.append(f"- **Square-of-9 targets:** T1 {g(r,'sq9_T1_+0.25')} · T2 {g(r,'sq9_T2_+0.5')} · T3 {g(r,'sq9_T3_+1.0')} "
             f"(support S1 {g(r,'sq9_S1_-0.25')}, S2 {g(r,'sq9_S2_-0.5')})")
    L.append(f"- **Time cycles:** {g(r,'gann_days_since_low')} days since swing low → next Gann cycle at {g(r,'next_gann_cycle_days')}d "
             f"({g(r,'days_to_next_cycle')}d away); near cycle: {g(r,'near_gann_cycle')}")
    L.append(f"- **Octave position:** {g(r,'octave')} | levels {g(r,'octave_levels')}")
    L.append(f"- **Cardinal square:** nearest perfect-square {g(r,'nearest_cardinal_sq')} ({g(r,'cardinal_dist_pct')}% away); near: {g(r,'near_cardinal')}")
    with open(path,"a",encoding="utf-8") as f: f.write("\n".join(L))

# ---- priority shortlist + summary ----
gt="gann_gann_trend"
pivot_vcp = m[(m["vcp_status"]=="AT PIVOT (actionable)") & (m["vcp_quality"]!="No VCP")] \
              .sort_values(["vcp_quality","total_score"], ascending=[True,False])
fresh = m[(m["vcp_status"]=="BROKEN OUT (fresh)") & (m["vcp_quality"]!="No VCP")].sort_values("total_score",ascending=False)
strong = m[m["vcp_quality"]=="Strong VCP"].sort_values("total_score",ascending=False)

S=[]
S.append("# PHASE 4 — VCP + GANN — SUMMARY")
S.append(f"Scan date 2026-06-02 · {len(m)} stocks analysed.\n")
S.append("## ✓ VERIFICATION CHECKPOINT (Phase 4)")
S.append("- ✅ VCP contraction pattern validated per stock (legs with depth%/duration, decreasing test)")
S.append("- ✅ 3rd-leg breakout status: broken-out / at-pivot / extended / forming")
S.append("- ✅ Volume dry-up (VDU) confirmed in final contraction (`vdu_confirmed`, `vdu_ratio`)")
S.append("- ✅ Gann angles mapped from swing low (auto-scaled 1x1/2x1/1x2)")
S.append("- ✅ Gann Square-of-9 targets T1/T2/T3 computed")
S.append("- ✅ Gann time cycles checked (days since low → next cycle)")
S.append("- ✅ Gann octave position noted (1/8 … 8/8)")
S.append("- ✅ Cardinal-square (perfect-square) proximity flagged")
S.append("- ✅ Shortlist of VCP at 3rd-leg pivot (highest priority) below\n")
S.append("## Distributions")
S.append(f"- **VCP quality:** {m['vcp_quality'].value_counts().to_dict()}")
S.append(f"- **3rd-leg status:** {m['vcp_status'].value_counts().to_dict()}")
S.append(f"- **Gann octave:** {m['octave'].value_counts().to_dict()}")
S.append(f"- **Above Gann 1x1 (strong trend):** {int(m['gann_above_1x1'].sum())}/{len(m)}")
S.append(f"- **Near a Gann time cycle (±5d):** {int(m['near_gann_cycle'].sum())} | **near cardinal square:** {int(m['near_cardinal'].sum())}\n")

S.append(f"## ⭐ HIGHEST PRIORITY — VCP at 3rd-leg PIVOT (actionable), {len(pivot_vcp)} names")
S.append("Tightest part of the base, within ~5% of pivot. Entry on breakout above pivot with volume ≥1.4× 50d-avg.\n")
S.append("| Symbol | Company | VCP | Contractions (C1→C3) | VDU | %from pivot | Entry zone | T1 (Gann) | Scorecard | Octave |")
S.append("|---|---|---|---|---|--:|---|--:|---|---|")
for _, r in pivot_vcp.iterrows():
    S.append(f"| {r['symbol']} | {str(g(r,'name'))[:24]} | {r['vcp_quality'].split()[0]} | {g(r,'contractions')} | "
             f"{'Y' if r['vdu_confirmed']==True else 'N'} | {g(r,'pct_from_pivot')} | {g(r,'entry_zone')} | "
             f"{g(r,'sq9_T1_+0.25')} | {g(r,'scorecard')} | {g(r,'octave')} |")

S.append(f"\n## 🔵 STRONG VCP (any status), {len(strong)} names")
S.append("| Symbol | Company | Status | Contractions | %from pivot | Scorecard |")
S.append("|---|---|---|---|--:|---|")
for _, r in strong.iterrows():
    S.append(f"| {r['symbol']} | {str(g(r,'name'))[:26]} | {g(r,'vcp_status')} | {g(r,'contractions')} | {g(r,'pct_from_pivot')} | {g(r,'scorecard')} |")

S.append(f"\n## 🟢 Fresh VCP breakouts (broken out ≤8% past pivot), {len(fresh)} names")
S.append("| Symbol | Company | %past pivot | Breakout vol× | Scorecard |")
S.append("|---|---|--:|--:|---|")
for _, r in fresh.head(20).iterrows():
    S.append(f"| {r['symbol']} | {str(g(r,'name'))[:26]} | {g(r,'pct_from_pivot')} | {g(r,'breakout_vol_ratio')} | {g(r,'scorecard')} |")

S.append("\n**Files:** `PHASE4_VCP_GANN.csv` (full table) · per-stock VCP+Gann appended to `reports/<symbol>.md`.")
S.append("\n### Method notes (disclosure)")
S.append("- VCP legs detected via fractal swing highs/lows over the last ~90 bars; 'decreasing depth' is strict, so most names score 'No VCP' — consistent with how few clean VCPs exist at any time.")
S.append("- Gann **angles auto-scaled**: 1×1 = traverse the 52-week range over 252 bars (scale-invariant across price levels), since a literal points/time scale is chart-software-specific.")
S.append("- Square-of-9 uses √price ± {0.25,0.5,1.0}; octaves use 52-week low→high eighths.")
open("PHASE4_SUMMARY.md","w",encoding="utf-8").write("\n".join(S))
print(f"Appended Phase-4 to reports + wrote PHASE4_SUMMARY.md")
print(f"VCP at pivot: {len(pivot_vcp)} | Strong VCP: {len(strong)} | Fresh breakouts: {len(fresh)}")
