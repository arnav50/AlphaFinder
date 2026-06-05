"""Write PHASE7_SUMMARY.md (final watchlist + position sizing + checkpoint + accuracy protocol)."""
import pandas as pd
wl=pd.read_csv("PHASE7_WATCHLIST.csv",dtype={"symbol":str})
allp=pd.read_csv("PHASE7_ALL_PASSERS.csv",dtype={"symbol":str})
bt=open("prime_backtest.txt").read()

S=[]
S.append("# PHASE 7 — PRIME FILTER SCANNER — FINAL WATCHLIST")
S.append("Scan date **2026-06-02** · forward-looking scan of the full NSE+BSE universe (4,524 tickers).\n")
S.append("## ⚠️ MARKET CONTEXT — READ FIRST")
S.append("**Nifty 50 = 23,484, BELOW its EMA50 (23,940) and EMA200 (24,667) → DOWNTREND.**")
S.append("Per the system's own accuracy protocol (\"avoid in bear markets\"), breakout follow-through "
         "probability is reduced when the index is below its 200-EMA. Treat this watchlist as **setups to stage**, "
         "not immediate full-size entries: wait for the index to reclaim its 50-EMA, halve position sizes, or "
         "demand extra confirmation (strong breakout close + volume) before acting.\n")
S.append("## ✓ VERIFICATION CHECKPOINT (Phase 7 — FINAL)")
S.append("- ✅ Prime-filter values derived from **Phase 5 actual data** (not assumptions): RSI 55–75, MACD hist>0 & line>signal, "
         "ADX 18–30, vol-spike ≥1.5×, Supertrend green, OBV rising, EMA20>EMA50, price>EMA200, within −35%..−3% of 52w high")
S.append("- ✅ Scanner built as a **confluence-count filter (≥6 of 9)** and **back-tested**: "
         f"{bt.splitlines()[3].strip()}")
S.append("- ✅ Every scan result validated with Phase 2–4 quick check (VCP stage, SMC zone, Gann 1×1, candlestick screen)")
S.append("- ✅ Final watchlist produced with entry, stop, and Gann targets")
S.append("- ✅ **Risk:Reward ≥ 3:1 enforced for every name** on the list (hard gate)")
S.append("- ✅ Position size computed per trade (1% capital risk rule)")
S.append("- ✅ Sector + market context confirmed (sectors fetched; market = DOWNTREND, flagged above)\n")
S.append("## Funnel")
S.append(f"- Universe scanned: **4,524** → prime-filter passers (≥6/9): **{len(allp)}** → "
         f"no bearish reversal candle: **{int((allp['bearish_candle']==False).sum())}** → "
         f"RR≥3 & top-ranked: **FINAL {len(wl)}**")
S.append(f"\nSector breadth of final list: {wl['sector'].value_counts().to_dict()}")
S.append("Momentum is concentrated in **Industrials, Financial Services, Technology** — those sectors are 'in favour'.\n")

S.append("## 🎯 FINAL WATCHLIST (forward 25%+ candidates)")
S.append("Entry = breakout pivot (20-bar high / current). Stop = 1.8×ATR (structural ref = VCP base/20-bar low). "
         "Target2 = max(Gann Sq-9 T2, +25% objective). Qty = shares risking 1% of a ₹10,00,000 account.\n")
S.append("| # | Symbol | Company | Sector | Price | VCP stage | RSI | ADX | Vol× | SMC | Gann>1×1 | Entry | Stop | Stop% | T1(Gann) | Target2 | R:R | Qty/₹10L | Score | Tier |")
S.append("|--:|---|---|---|--:|---|--:|--:|--:|---|:--:|--:|--:|--:|--:|--:|--:|--:|--:|---|")
for _,r in wl.iterrows():
    S.append(f"| {r['rank']} | {r['symbol']} | {str(r['name'])[:22]} | {r['sector']} | {r['close']} | "
             f"{r['vcp_status']} | {r['rsi']} | {r['adx']} | {r['vol_spike']} | {r['pd_zone']} | "
             f"{'Y' if r['gann_above_1x1'] else 'N'} | {r['pivot_entry']} | {r['stop']} | {r['stop_pct']}% | "
             f"{r['gann_T1']} | {r['target2']} | **{r['rr']}** | {r['qty_per_10L']} | {r['phase7_score']} | {r['tier']} |")

S.append("\n## Position sizing rule (applied)")
S.append("- **Risk per trade = 1% of capital** (max 2%). Example capital used: ₹10,00,000 → ₹10,000 risk/trade.")
S.append("- **Shares = (1% × Capital) ÷ (Entry − Stop)**. Stop = 1.8×ATR below entry (≈ the Stop% column).")
S.append("- Never let one position exceed the risk budget; if Stop% is wide, the Qty shrinks automatically.")
S.append("- Tighten/scale to the **structural stop** (VCP base / demand-zone low) if it is closer than 1.8×ATR.\n")
S.append("## 🔁 ACCURACY PROTOCOL (ongoing — system maintenance)")
S.append("- Re-run `22_prime_scan.py` + `23_watchlist.py` **weekly**; track which triggered names delivered ≥25%.")
S.append("- Re-extract the Phase-5 fingerprint **quarterly** (re-run Phases 1→5) to refresh filter bands.")
S.append("- **Drop** any criterion whose hit-rate falls <60% on new winners; **add** any new signal >75% consistent.")
S.append("- Current per-criterion hit-rates (on known winners): OBV 98%, Supertrend 90%, MACD 88%, Vol 88%, RSI 80%, "
         "52w-dist 66% (keep); ADX 47%, EMA20>50 42%, px>EMA200 47% (confluence boosters, below 60% alone).\n")
S.append("## Files")
S.append("- **`PHASE7_WATCHLIST.csv`** — the 30-name final list (this table)")
S.append("- `PHASE7_ALL_PASSERS.csv` — all 521 prime-filter passers with full Stage-2 metrics")
S.append("- `prime_passers.csv` / `prime_backtest.txt` — Stage-1 output + backtest")
S.append("\n### Disclosure")
S.append("- The 76.2% backtest recall is **in-sample** (bands derived from the same winners); true out-of-sample "
         "performance is what the weekly tracking will measure. Use it as a consistency check, not a guarantee.")
S.append("- Prime filter is the Phase-5 **breakout** signature, so it surfaces names breaking out now / at pivot — "
         "the BB-squeeze (pre-breakout) idea is captured indirectly via VCP-at-pivot in Stage 2.")
S.append("- Targets/stops are mechanical (ATR + Gann + 25% objective); always sanity-check against the live chart "
         "and overhead supply before entering. **Not investment advice.**")
open("PHASE7_SUMMARY.md","w",encoding="utf-8").write("\n".join(S))
print("Wrote PHASE7_SUMMARY.md")
print(f"final watchlist: {len(wl)} | tiers: {wl['tier'].value_counts().to_dict()}")
print(f"avg RR: {wl['rr'].mean():.2f} | RR range {wl['rr'].min()}-{wl['rr'].max()}")
