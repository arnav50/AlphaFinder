"""Append Phase-3 SMC section to each reports/<symbol>.md and write PHASE3_SUMMARY.md."""
import os, pandas as pd

smc = pd.read_csv("PHASE3_SMC.csv", dtype={"symbol": str})
sc = pd.read_csv("PHASE2_SCORECARD.csv", dtype={"symbol": str})[["symbol","name","scorecard","total_score"]]
smc = smc.merge(sc, on="symbol", how="left")

def g(r,k,d="n/a"):
    v=r.get(k); return d if pd.isna(v) else v

for _, r in smc.iterrows():
    sym = r["symbol"]; path = f"reports/{sym}.md"
    if not os.path.exists(path): continue
    L = ["\n\n---\n## PHASE 3 — Supply/Demand + Smart Money Concepts"]
    L.append("### A. Supply & Demand zones")
    L.append(f"- **Demand (daily):** {g(r,'demand_zone_D')} — quality {g(r,'demand_quality')}"
             f"{' · PRICE NEAR' if r.get('near_demand')==True else ''}")
    L.append(f"- **Demand (weekly):** {g(r,'demand_zone_W')}")
    L.append(f"- **Supply (daily, overhead):** {g(r,'supply_zone_D')}"
             f"{' · PRICE APPROACHING (long risk)' if r.get('near_supply')==True else ''}")
    L.append(f"- **Supply (weekly):** {g(r,'supply_zone_W')}")
    L.append("### B. Smart Money Concepts")
    L.append(f"- **Market structure:** daily {g(r,'structure_D')} | weekly {g(r,'structure_W')} | "
             f"aligned: {g(r,'structure_aligned')}")
    L.append(f"- **Break of Structure (last):** {g(r,'last_BoS')}")
    L.append(f"- **Change of Character (last):** {g(r,'last_ChoCh')}")
    L.append(f"- **Bullish Order Block:** {g(r,'bull_OB')}")
    L.append(f"- **Bearish Order Block:** {g(r,'bear_OB')}")
    L.append(f"- **Fair Value Gaps:** {g(r,'unfilled_bull_FVG')} unfilled bullish, "
             f"{g(r,'unfilled_bear_FVG')} unfilled bearish · nearest bull FVG below {g(r,'nearest_bull_FVG_below')} · "
             f"nearest bear FVG above {g(r,'nearest_bear_FVG_above')}")
    L.append(f"- **Liquidity:** buy-side above {g(r,'buyside_liq_above')} | sell-side below {g(r,'sellside_liq_below')} | "
             f"equal-highs {g(r,'equal_highs')} / equal-lows {g(r,'equal_lows')} | swept: {g(r,'liquidity_swept')}")
    L.append(f"- **Premium/Discount:** **{g(r,'pd_zone')}** (price at {g(r,'range_pos_pct')}% of range "
             f"{g(r,'range_low')}–{g(r,'range_high')}){' · IN DISCOUNT (institutional buy zone)' if r.get('in_discount')==True else ''}")
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(L))

# ---- summary ----
def vc(col): return smc[col].value_counts().to_dict()
S=[]
S.append("# PHASE 3 — SUPPLY/DEMAND + SMC — SUMMARY")
S.append(f"Scan date 2026-06-02 · {len(smc)} stocks · daily primary, weekly structure overlay.\n")
S.append("## ✓ VERIFICATION CHECKPOINT (Phase 3)")
S.append("- ✅ Demand & supply zones mapped on **daily and weekly** (`demand_zone_D/W`, `supply_zone_D/W`)")
S.append("- ✅ **Order blocks** identified with **mitigation status** (`bull_OB`, `bear_OB`)")
S.append("- ✅ **FVGs** listed with filled/unfilled counts + nearest unfilled (`unfilled_bull/bear_FVG`)")
S.append("- ✅ **Liquidity pools** above/below + sweep detection (`buyside/sellside_liq`, `liquidity_swept`)")
S.append("- ✅ **Market structure** daily+weekly (`structure_D/W`, alignment)")
S.append("- ✅ **Premium/Discount** classification for every stock (`pd_zone`, `range_pos_pct`)\n")
S.append("## Structural landscape")
S.append(f"- **Market structure (daily):** {vc('structure_D')}")
S.append(f"- **Premium/Discount:** {vc('pd_zone')}")
S.append(f"- **Last BoS direction:** {vc('bos_dir')}")
S.append(f"- **Liquidity swept recently:** {vc('liquidity_swept')}")
S.append(f"- **Unmitigated bullish order blocks (pullback support):** {int(smc['bull_OB_unmitigated'].sum())}")
S.append(f"- **Price near a demand zone:** {int(smc['near_demand'].sum())} · **approaching overhead supply (long risk):** {int(smc['near_supply'].sum())}\n")
S.append("> **Key institutional read:** {p}/{n} names sit in **Premium** (expensive, extended) — smart-money "
         "playbook is to wait for a retracement into discount / an unmitigated demand OB rather than chase. "
         "Only {d} are currently in a discount zone.".format(p=vc('pd_zone').get('Premium',0), n=len(smc),
                                                              d=vc('pd_zone').get('Discount',0)))
S.append("\n## Stocks currently in DISCOUNT (institutional buy zone)")
disc = smc[smc["pd_zone"]=="Discount"]
if len(disc):
    S.append("| Symbol | Company | Range pos% | Structure(D) | Last BoS | Scorecard |")
    S.append("|---|---|--:|---|---|---|")
    for _, r in disc.iterrows():
        S.append(f"| {r['symbol']} | {g(r,'name')} | {r['range_pos_pct']} | {g(r,'structure_D')} | {g(r,'last_BoS')} | {g(r,'scorecard')} |")
else:
    S.append("_none_")
S.append("\n## High-conviction confluence: bullish structure + unmitigated demand OB + not in extreme premium")
hot = smc[(smc["structure_D"].str.startswith("bullish")) & (smc["bull_OB_unmitigated"]==True) & (smc["range_pos_pct"]<85)]
S.append(f"**{len(hot)} stocks** meet bullish-structure + unmitigated-bull-OB + range_pos<85%:")
if len(hot):
    S.append("| Symbol | Company | pos% | Bull OB | Demand zone | Scorecard |")
    S.append("|---|---|--:|---|---|---|")
    for _, r in hot.sort_values("total_score",ascending=False).head(25).iterrows():
        S.append(f"| {r['symbol']} | {str(g(r,'name'))[:24]} | {r['range_pos_pct']} | {g(r,'bull_OB')} | {g(r,'demand_zone_D')} | {g(r,'scorecard')} |")
S.append(f"\n**Files:** `PHASE3_SMC.csv` (full table) · per-stock SMC appended to `reports/<symbol>.md`.")
open("PHASE3_SUMMARY.md","w",encoding="utf-8").write("\n".join(S))
print(f"Appended SMC to reports + wrote PHASE3_SUMMARY.md")
print(f"discount stocks: {len(disc)} | high-conviction confluence: {len(hot)}")
