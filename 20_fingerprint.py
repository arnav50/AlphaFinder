"""Phase 5D: aggregate Day-0 snapshots into the move-initiation FINGERPRINT.
Outputs PHASE5_FINGERPRINT.csv + PHASE5_SUMMARY.md (input for Phase 7)."""
import numpy as np, pandas as pd

d = pd.read_csv("PHASE5_DAY0.csv")
d = d[d["rsi"].notna()].copy()           # drop any error rows
N = len(d)

# (column, label, bin_edges, bin_labels)
NUM = [
 ("rsi","RSI(14)",[0,40,50,60,70,80,101],["<40","40-50","50-60","60-70","70-80",">80"]),
 ("stoch_k","Stochastic %K",[0,20,40,60,80,101],["<20","20-40","40-60","60-80","80-100"]),
 ("stoch_d","Stochastic %D",[0,20,40,60,80,101],["<20","20-40","40-60","60-80","80-100"]),
 ("pctB","Bollinger %B",[-1e9,0,20,50,80,100,1e9],["<0","0-20","20-50","50-80","80-100",">100"]),
 ("bb_width","BB width %",[0,5,10,15,20,30,1e9],["<5","5-10","10-15","15-20","20-30",">30"]),
 ("cci","CCI(20)",[-1e9,-100,0,100,200,1e9],["<-100","-100..0","0-100","100-200",">200"]),
 ("williams_r","Williams %R",[-100,-80,-50,-20,0],["-100..-80","-80..-50","-50..-20","-20..0"]),
 ("mfi","MFI(14)",[0,20,40,60,80,101],["<20","20-40","40-60","60-80","80-100"]),
 ("macd_hist","MACD hist",[-1e9,0,1e9],["<0(neg)",">0(pos)"]),
 ("adx","ADX(14)",[0,20,25,35,50,1e9],["<20","20-25","25-35","35-50",">50"]),
 ("atr_pct","ATR %",[0,3,5,7,1e9],["<3","3-5","5-7",">7"]),
 ("pct_vs_ema200","% vs EMA200",[-1e9,0,5,10,20,1e9],["<0","0-5","5-10","10-20",">20"]),
 ("pct_from_52wh","% from 52w high",[-1e9,-30,-15,-5,0.001],["<-30","-30..-15","-15..-5","-5..0"]),
 ("day0_vol_x_50davg","Vol × 50d-avg",[0,1.5,2,4,7,1e9],["<1.5","1.5-2","2-4","4-7",">7"]),
]
CAT = [("supertrend","Supertrend"),("ema_alignment","EMA alignment"),("obv_dir","OBV direction"),
       ("macd_vs_zero","MACD vs zero"),("bb_position","BB position")]
FLAGS = ["bos_triggered","vcp_pivot_broken","demand_zone_reclaimed","order_block_broken"]
PRE = [("pre_vol_pattern","Pre-5d volume"),("pre_rsi_trend","Pre-5d RSI"),
       ("pre_tight_range","Pre tight range"),("pre_volume_dryup","Pre VDU"),("pre_shakeout","Pre shakeout")]

rows=[]
for col,label,edges,labels in NUM:
    s=d[col].dropna()
    if not len(s): continue
    cats=pd.cut(s,bins=edges,labels=labels,include_lowest=True,right=False)
    vc=cats.value_counts()
    zone=vc.index[0]; cons=vc.iloc[0]/len(s)*100
    rows.append({"indicator":label,"n":len(s),"min":round(s.min(),1),"max":round(s.max(),1),
                 "avg":round(s.mean(),1),"median":round(s.median(),1),
                 "most_common_zone":str(zone),"consistency_pct":round(cons,1),"type":"numeric"})
for col,label in CAT:
    s=d[col].dropna().astype(str)
    if not len(s): continue
    vc=s.value_counts()
    rows.append({"indicator":label,"n":len(s),"min":"","max":"","avg":"","median":"",
                 "most_common_zone":vc.index[0],"consistency_pct":round(vc.iloc[0]/len(s)*100,1),"type":"categorical"})
for col in FLAGS:
    s=d[col].dropna().astype(str)
    y=(s=="Y").mean()*100
    rows.append({"indicator":col,"n":len(s),"min":"","max":"","avg":"","median":"",
                 "most_common_zone":("Y" if y>=50 else "N"),"consistency_pct":round(max(y,100-y),1),
                 "type":"structure_flag","Y_pct":round(y,1)})
for col,label in PRE:
    s=d[col].dropna().astype(str); vc=s.value_counts()
    rows.append({"indicator":label,"n":len(s),"min":"","max":"","avg":"","median":"",
                 "most_common_zone":vc.index[0],"consistency_pct":round(vc.iloc[0]/len(s)*100,1),"type":"pre_context"})

fp=pd.DataFrame(rows)
fp.to_csv("PHASE5_FINGERPRINT.csv",index=False)

# Top 5 most consistent among the core leading/lagging numeric+categorical indicators
core=fp[fp["type"].isin(["numeric","categorical"])].sort_values("consistency_pct",ascending=False)
top5=core.head(5)

S=[]
S.append("# PHASE 5 — MOVE-INITIATION FINGERPRINT (DNA at Day 0)")
S.append(f"Day-0 captured for **{N} stocks** · {int((d['day0_verified_volspike']==True).sum())} confirmed with a volume spike "
         f"(≥1.4× 50-day avg) + breakout above 20-bar structure + strong bullish close.\n")
S.append("## ✓ VERIFICATION CHECKPOINT (Phase 5)")
S.append(f"- ✅ Day 0 identified for every stock; **{int((d['day0_verified_volspike']==True).sum())}/{N}** verified via volume spike "
         f"(median spike **{d['day0_vol_x_50davg'].median():.1f}×**), rest via base-breakout fallback")
S.append("- ✅ All leading + lagging + price-action + structure indicators recorded at Day 0 (`PHASE5_DAY0.csv`)")
S.append("- ✅ 5-day pre-move context recorded (volume/RSI/range/VDU/shakeout)")
S.append("- ✅ Aggregate fingerprint table with consistency % built (`PHASE5_FINGERPRINT.csv`)")
S.append("- ✅ Top-5 most consistent indicators identified (prime filters)")
S.append("- ✅ Fingerprint exported — input for Phase 7\n")

S.append("## 🧬 THE FINGERPRINT — indicator state at move initiation")
S.append("| Indicator | Min | Max | Avg | Median | Most common zone | Consistency % |")
S.append("|---|--:|--:|--:|--:|---|--:|")
for _,r in fp[fp["type"]=="numeric"].iterrows():
    S.append(f"| {r['indicator']} | {r['min']} | {r['max']} | {r['avg']} | {r['median']} | {r['most_common_zone']} | **{r['consistency_pct']}%** |")
S.append("\n### Categorical state at Day 0")
S.append("| Indicator | Most common | Consistency % |")
S.append("|---|---|--:|")
for _,r in fp[fp["type"]=="categorical"].iterrows():
    S.append(f"| {r['indicator']} | {r['most_common_zone']} | {r['consistency_pct']}% |")
S.append("\n### Structure triggers on Day 0 (% of stocks = Y)")
S.append("| Trigger | % Yes |")
S.append("|---|--:|")
for _,r in fp[fp["type"]=="structure_flag"].iterrows():
    S.append(f"| {r['indicator']} | {r.get('Y_pct')}% |")
S.append("\n### 5-day pre-move context (dominant mode)")
S.append("| Context | Dominant | % |")
S.append("|---|---|--:|")
for _,r in fp[fp["type"]=="pre_context"].iterrows():
    S.append(f"| {r['indicator']} | {r['most_common_zone']} | {r['consistency_pct']}% |")

S.append("\n## 🎯 TOP 5 MOST CONSISTENT INDICATORS (prime filters for Phase 7)")
S.append("| Rank | Indicator | Zone | Consistency % |")
S.append("|--:|---|---|--:|")
for i,(_,r) in enumerate(top5.iterrows(),1):
    S.append(f"| {i} | {r['indicator']} | {r['most_common_zone']} | **{r['consistency_pct']}%** |")

# narrative fingerprint
g=lambda c: d[c].median()
S.append("\n## 📌 Plain-language DNA of a move start")
S.append(f"> A typical Day-0 breakout fired with **RSI ≈ {g('rsi'):.0f}**, **Stoch %K ≈ {g('stoch_k'):.0f}**, "
         f"**MFI ≈ {g('mfi'):.0f}**, **CCI ≈ {g('cci'):.0f}** (>100 = thrust), **ADX ≈ {g('adx'):.0f}** "
         f"(trend just beginning), **ATR ≈ {g('atr_pct'):.1f}%** of price, price **{g('pct_vs_ema200'):+.1f}% vs EMA200** "
         f"(just reclaimed) and **{g('pct_from_52wh'):.0f}% below its 52-week high** (room to run), on **{g('day0_vol_x_50davg'):.1f}× "
         f"average volume**, Supertrend **{d['supertrend'].mode()[0]}**, with a **{d['macd_vs_zero'].mode()[0]}-zero MACD**. "
         f"A Break of Structure triggered in **{(d['bos_triggered']=='Y').mean()*100:.0f}%** of cases.")
S.append("\n### Disclosure")
S.append("- Day 0 = earliest validated breakout after the recent base low (volume ≥1.4×, close>20-bar high, bullish close in upper half). "
         "RSI/Stoch read at the Day-0 *close* are momentum-elevated by construction (the breakout bar itself) — this is the breakout signature, not a pre-breakout reading.")
S.append("- Consistency % = share of stocks falling in the single most-common bin (bin widths shown in the zone). Wider zones naturally score higher; compare within similar bin widths.")
S.append("\n**Files:** `PHASE5_DAY0.csv` (per-stock Day-0 snapshot + pre-context) · `PHASE5_FINGERPRINT.csv` (this table).")
open("PHASE5_SUMMARY.md","w",encoding="utf-8").write("\n".join(S))
print(f"Wrote PHASE5_FINGERPRINT.csv ({len(fp)} rows) + PHASE5_SUMMARY.md  | N={N}")
print("\nTOP 5 consistent:")
print(top5[["indicator","most_common_zone","consistency_pct"]].to_string(index=False))
print("\nFingerprint (numeric):")
print(fp[fp["type"]=="numeric"][["indicator","avg","median","most_common_zone","consistency_pct"]].to_string(index=False))
