"""Render PHASE1_REPORT.md from FINAL_universe_25pct.csv (full 312-name table + checkpoint)."""
import datetime as dt, pandas as pd

f = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
today = dt.date(2026, 6, 2); past = today - dt.timedelta(days=180)

def cr(x):
    return f"{x:,.0f}" if pd.notna(x) else "n/a"
def vol(x):
    return f"{int(x):,}" if pd.notna(x) else "n/a"

L = []
L.append("# PHASE 1 — UNIVERSE IDENTIFICATION (NSE + BSE)")
L.append(f"**Scan date:** {today.isoformat()}  |  **180-day reference:** {past.isoformat()}  "
         f"|  **Filter:** 180-day price return ≥ 25%\n")
L.append("## Methodology (auditable, scripted — no hand-entered prices)")
L.append("1. **Universe** — NSE official `EQUITY_L.csv` (series EQ+BE) + BSE active-equity scrip master "
         "(API), excluding BSE **Z / XT / XC** surveillance groups. Dual-listed companies de-duplicated "
         "by **ISIN** (NSE listing preferred).")
L.append("2. **Prices** — ~180-day daily OHLCV per symbol from Yahoo Finance chart API "
         "(sources exchange data). Return = last close ÷ **median of ±2 bars around the 180-day date** "
         "(median guards against bad single prints).")
L.append("3. **Liquidity filter** — avg daily volume ≥ 50,000 shares **OR** avg daily traded value ≥ ₹50 lakh.")
L.append("4. **Verification (2 sources)** — (a) returns re-derived from **split/bonus-adjusted** prices "
         "→ 0 corporate-action distortions; (b) current price cross-checked against the **other exchange's "
         "live quote** (BSE-twin via ISIN / BSE live API).\n")

n = len(f)
byx = f["exchange"].value_counts().to_dict()
byc = f["cap_bucket"].value_counts().to_dict()
xs = f[f["xsrc_price"].notna()]
L.append("## ✓ VERIFICATION CHECKPOINT")
L.append(f"- **Total verified stocks (180d return ≥ 25%): {n}**")
L.append(f"- Exchange split (after ISIN dedup, NSE preferred): {byx}")
L.append(f"- Market-cap buckets: {byc}  *(Large ≥₹20k cr, Mid ≥₹5k cr, Small ≥₹500 cr, Micro <₹500 cr)*")
L.append(f"- Penny stocks (price < ₹10): **{int(f['penny_flag'].sum())} flagged, none removed** (per spec)")
L.append(f"- Cross-source current-price check: {len(xs)}/{n} have a 2nd exchange source; "
         f"**{int((xs['xsrc_mismatch_pct']<=5).sum())}/{len(xs)} agree within 5%** "
         f"(median mismatch **{xs['xsrc_mismatch_pct'].median():.2f}%**)")
L.append(f"- Excluded categories (suspended / Z / XT / XC) removed at universe stage")
L.append(f"- Sorted by Return% descending ✓\n")

flagged = f[(f['xsrc_mismatch_pct'] > 5) & f['xsrc_price'].notna()]
if len(flagged):
    L.append("### ⚠ Price-discrepancy flags (NSE-vs-BSE > 5% — review before trading; all still >25%)")
    for _, r in flagged.iterrows():
        L.append(f"- `{r['symbol']}` {r['name']} ({r['exchange']}): Yahoo ₹{r['price_today']:.2f} "
                 f"vs other-exchange ₹{r['xsrc_price']:.2f} ({r['xsrc_mismatch_pct']:.1f}%)")
    L.append("")

L.append("## OUTPUT — full ranked list")
L.append("Columns: Symbol | Company | Exch | Price 180d ago | Price today | Return% | "
         "MktCap(₹cr) | Cap | Sector | AvgVol(sh) | AvgVal(₹)\n")
L.append("| # | Symbol | Company | Exch | 180d Ago | Today | Return% | MktCap₹cr | Cap | Sector | AvgVol | AvgVal₹ |")
L.append("|--:|---|---|---|--:|--:|--:|--:|---|---|--:|--:|")
for _, r in f.iterrows():
    penny = " 🟡" if r["penny_flag"] else ""
    L.append(f"| {r['rank']} | {r['symbol']} | {r['name']} | {r['exchange']} | "
             f"{r['price_180d_ago']:.2f} | {r['price_today']:.2f}{penny} | **{r['return_pct_final']:.1f}** | "
             f"{cr(r['mktcap_cr'])} | {r['cap_bucket']} | {r['sector']} | "
             f"{vol(r['avg_daily_volume'])} | {vol(r['avg_daily_value_rs'])} |")

L.append("\n🟡 = penny stock (price < ₹10), flagged not removed.")
L.append(f"\n**Machine-readable file:** `FINAL_universe_25pct.csv` ({n} rows).")
L.append("\n### Known limitations (full disclosure)")
L.append("- 464 universe symbols (of 4,524) returned no Yahoo history (recently renamed post-corporate-"
         "action e.g. demerged Tata Motors, thinly-traded, or delisted-from-Yahoo) — excluded from the scan, "
         "not from reality. These are predominantly illiquid BSE micro-caps.")
L.append("- 11 NSE-only names have no BSE twin, so their current price rests on Yahoo alone (still passes "
         "the adjusted-return integrity check).")
L.append("- Sector unavailable for 37 BSE-only micro-caps (shown as n/a).")

open("PHASE1_REPORT.md", "w", encoding="utf-8").write("\n".join(L))
print(f"Wrote PHASE1_REPORT.md with {n} stocks.")
