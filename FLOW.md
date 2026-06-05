# AlphaFinder — Code & Business Flow

> **One-page mental model for a new developer.**
> AlphaFinder is a **7-phase pipeline** that scans the *entire* NSE + BSE stock universe (~4,500 stocks),
> finds names that already ran up 25%+ in 180 days, studies *what their charts looked like*, distills that
> into a repeatable **"move-initiation fingerprint"**, then rescans the whole market for **fresh** stocks
> that match the fingerprint *before* they run — ending in a risk-defined **watchlist** and an interactive
> **HTML dashboard**.
>
> Each numbered script (`01`…`25`) is **one step**. A step **reads files** produced by earlier steps and
> **writes new files** for later steps. There is no hidden state — every hand-off is a CSV / pickle on disk.
> Run them in numeric order.

---

## 1. Business flow (plain English)

```mermaid
flowchart TD
    A["🌐 ALL NSE + BSE stocks<br/><b>~4,524</b>"]
    B["🚀 Already moved 25%+ in 180 days<br/>+ liquid enough to trade<br/><b>Phase 1 'winners'</b>"]
    C["🔬 Deep technical study of each winner<br/>Indicators · Candles · Smart-Money · VCP · Gann<br/><b>Phases 2–4</b>"]
    D["🧬 'What did they look like on Day-0?'<br/>Snapshot every winner at its breakout bar,<br/>aggregate into a FINGERPRINT<br/><b>Phase 5</b>"]
    E["🏆 Rank the winners 0–100 by confluence<br/>Tier 1 / 2 / 3 = the 'Alpha list'<br/><b>Phase 6</b>"]
    F["🎯 Rescan the WHOLE market for FRESH stocks<br/>that match the fingerprint NOW<br/>+ entry / stop / target / position size<br/><b>Phase 7 Watchlist</b>"]
    G["📊 Interactive dashboard<br/><b>alphafinder_dashboard.html</b>"]

    A -->|"return ≥ 25% & liquidity filter"| B
    B -->|"analyse the survivors"| C
    C --> D
    D -->|"fingerprint becomes the filter"| E
    E --> F
    D -.->|"≥6/9 confluence rule<br/>drives the rescan"| F
    F --> G
    E --> G

    style A fill:#1a2130,stroke:#3b82f6,color:#e6edf3
    style B fill:#0e2a16,stroke:#22c55e,color:#e6edf3
    style D fill:#241a33,stroke:#a78bfa,color:#e6edf3
    style F fill:#2a230c,stroke:#f59e0b,color:#e6edf3
    style G fill:#0e1f33,stroke:#22d3ee,color:#e6edf3
```

**The core idea (why it is built this way):**
Phases 1–6 are *backward-looking* — they study stocks that **already** won, to learn the recipe.
Phase 7 is *forward-looking* — it applies that recipe to the **whole market** to catch the **next** winners
early. The dashboard is just a viewer over the files those phases produce.

---

## 2. Code & data flow (what each script reads and writes)

> Read top-to-bottom. **Blue = code (a `.py` step)**, **grey = data file on disk**.
> External clouds = live internet sources fetched at runtime.

```mermaid
flowchart TD
    %% ---- external sources ----
    NSE(["☁️ NSE archives<br/>EQUITY_L.csv"])
    BSE(["☁️ BSE scrip-master API"])
    YH(["☁️ Yahoo Finance<br/>chart / quote API"])

    %% ============ PHASE 1 : DISCOVERY + VERIFICATION ============
    subgraph P1 ["PHASE 1 — Discover & verify the 25%+ universe"]
        direction TB
        s01["01_universe.py"] --> universe[(universe.csv<br/>~4,524)]
        universe --> s02["02_prices.py"] --> prices[(prices.csv<br/>180d return)]
        prices --> s03["03_filter_enrich.py"] --> hitsE[(hits_enriched.csv<br/>≥25% + liquid + cap/sector)]
        hitsE --> s04["04_verify.py"] --> hitsV[(hits_verified.csv<br/>adj-return + live-price check)]
        hitsE --> s05["05_finalize.py"] --> hitsF[(hits_final.csv<br/>robust median return)]
        hitsF --> s06["06_reconcile.py"] --> FINAL[(FINAL_universe_25pct.csv<br/>★ verified winners)]
        FINAL --> s07["07_sector.py"] -.->|enrich in place| FINAL
        FINAL --> s08["08_report.py"] --> rep1[(PHASE1_REPORT.md)]
    end

    NSE --> s01
    BSE --> s01 & s03 & s05 & s06
    YH --> s02 & s04 & s05

    %% ============ PHASE 2-4 : ANALYSE EACH WINNER ============
    subgraph DATA ["Price data for the winners"]
        FINAL --> s09["09_fetch_ohlc.py"] --> ohlc[(ohlc.pkl<br/>~500d OHLCV per stock)]
    end
    YH --> s09

    subgraph P2 ["PHASE 2 — Indicators · Candles · Scorecard"]
        ohlc --> s10["10_indicators.py"] --> indc[(indicators.csv)]
        ohlc --> s11["11_candles.py"] --> cand[(candles.csv +<br/>candles_summary.csv)]
        ohlc --> s12["12_patterns.py"] --> pat[(patterns.csv)]
        indc & cand & pat --> s13["13_scorecard.py"] --> P2SC[(PHASE2_SCORECARD.csv)]
        P2SC --> s14["14_reports.py"] --> RPT[/reports/&lt;SYMBOL&gt;.md/]
    end

    subgraph P3 ["PHASE 3 — Smart-Money Concepts"]
        ohlc --> s15["15_smc.py"] --> P3SMC[(PHASE3_SMC.csv)]
        P3SMC --> s16["16_phase3_reports.py"] -.->|append| RPT
    end

    subgraph P4 ["PHASE 4 — VCP + Gann"]
        ohlc --> s17["17_vcp_gann.py"] --> P4VG[(PHASE4_VCP_GANN.csv)]
        P4VG --> s18["18_phase4_reports.py"] -.->|append| RPT
    end

    %% ============ PHASE 5 : FINGERPRINT ============
    subgraph P5 ["PHASE 5 — Day-0 move-initiation fingerprint"]
        ohlc --> s19["19_day0.py"] --> P5D0[(PHASE5_DAY0.csv)]
        P5D0 --> s20["20_fingerprint.py"] --> P5FP[(PHASE5_FINGERPRINT.csv +<br/>PHASE5_SUMMARY.md)]
    end

    %% ============ PHASE 6 : RANK ============
    subgraph P6 ["PHASE 6 — Composite 0–100 confluence rank"]
        indc & P2SC & P3SMC & P4VG --> s21["21_phase6_score.py"] --> P6R[(PHASE6_RANKING.csv +<br/>ALPHA_LIST.csv)]
    end

    %% ============ PHASE 7 : FORWARD SCAN ============
    subgraph P7 ["PHASE 7 — Forward prime-filter rescan of the FULL market"]
        P5D0 --> s22
        universe --> s22["22_prime_scan.py"] --> PP[(prime_passers.csv +<br/>prime_passers.pkl)]
        PP --> s23["23_watchlist.py"] --> WL[(PHASE7_WATCHLIST.csv +<br/>PHASE7_ALL_PASSERS.csv)]
        WL --> s24["24_phase7_summary.py"] --> P7S[(PHASE7_SUMMARY.md)]
    end
    YH --> s22 & s23

    %% ============ FRONTEND ============
    FINAL & P2SC & P3SMC & P4VG & P6R & WL & P5FP --> s25["25_build_frontend.py"] --> DASH[["🖥️ alphafinder_dashboard.html"]]

    %% ---- styling ----
    classDef code fill:#0e1f33,stroke:#3b82f6,color:#e6edf3;
    classDef ext fill:#241a33,stroke:#a78bfa,color:#e6edf3;
    class s01,s02,s03,s04,s05,s06,s07,s08,s09,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25 code;
    class NSE,BSE,YH ext;
```

---

## 3. Shared helper libraries (no `__main__`, imported by the phase scripts)

| Library | What it provides | Used by |
|---|---|---|
| [ta_lib_local.py](ta_lib_local.py) | Pure-pandas indicator math — RSI, Stochastic, MACD, Bollinger, EMA, ADX, ATR, Supertrend, CCI, MFI, OBV, Williams %R, swing detection | `10`, `19`, `22`, `23` |
| [ta_smc.py](ta_smc.py) | Smart-Money Concepts — demand/supply zones, order blocks, fair-value gaps, BoS/CHoCH market structure, premium/discount | `15`, `22`, `23` |
| [ta_vcp_gann.py](ta_vcp_gann.py) | Volatility-Contraction-Pattern detection + Gann angles, Square-of-9 targets, time cycles, octaves | `17`, `22`, `23` |

---

## 4. Quick reference — one line per step

| # | Script | Reads | Writes | Business purpose |
|---|---|---|---|---|
| 01 | `01_universe.py` | NSE + BSE (live) | `universe.csv` | Build the full tradeable equity list (dedupe NSE/BSE by ISIN) |
| 02 | `02_prices.py` | `universe.csv`, Yahoo | `prices.csv` | 180-day return + liquidity per stock |
| 03 | `03_filter_enrich.py` | `prices.csv`, BSE | `hits_enriched.csv` | Keep ≥25% & liquid; add market-cap + sector |
| 04 | `04_verify.py` | `hits_enriched.csv`, Yahoo/NSE/BSE | `hits_verified.csv` | Cross-check: split-adjusted return + live price |
| 05 | `05_finalize.py` | `hits_enriched.csv`, Yahoo/NSE/BSE | `hits_final.csv` | Robust median return (immune to bad prints) |
| 06 | `06_reconcile.py` | `hits_final.csv`, BSE | **`FINAL_universe_25pct.csv`** | Canonical verified winner list |
| 07 | `07_sector.py` | `FINAL_universe_25pct.csv` | *(updates it)* | Fill/normalise sector labels |
| 08 | `08_report.py` | `FINAL_universe_25pct.csv` | `PHASE1_REPORT.md` | Human-readable Phase-1 report |
| 09 | `09_fetch_ohlc.py` | `FINAL_universe_25pct.csv`, Yahoo | **`ohlc.pkl`** | ~500d OHLCV per winner (analysis fuel) |
| 10 | `10_indicators.py` | `ohlc.pkl` | `indicators.csv` | All leading + lagging indicators |
| 11 | `11_candles.py` | `ohlc.pkl` | `candles*.csv` | Candlestick patterns |
| 12 | `12_patterns.py` | `ohlc.pkl` | `patterns.csv` | Chart patterns (H&S, flags, triangles…) |
| 13 | `13_scorecard.py` | `indicators`+`candles`+`patterns`+`FINAL` | `PHASE2_SCORECARD.csv` | Bullish/Neutral/Bearish verdict |
| 14 | `14_reports.py` | Phase-2 files | `reports/<SYM>.md` | Per-stock dossier (Phase 2 section) |
| 15 | `15_smc.py` | `ohlc.pkl` | `PHASE3_SMC.csv` | Smart-money zones & structure |
| 16 | `16_phase3_reports.py` | `PHASE3_SMC.csv` | *(appends reports)* | Add SMC to dossiers |
| 17 | `17_vcp_gann.py` | `ohlc.pkl` | `PHASE4_VCP_GANN.csv` | VCP + Gann setup detection |
| 18 | `18_phase4_reports.py` | `PHASE4_VCP_GANN.csv` | *(appends reports)* | Add VCP/Gann to dossiers |
| 19 | `19_day0.py` | `ohlc.pkl` | `PHASE5_DAY0.csv` | Snapshot each winner at its breakout bar |
| 20 | `20_fingerprint.py` | `PHASE5_DAY0.csv` | `PHASE5_FINGERPRINT.csv` | Aggregate Day-0 → the reusable fingerprint |
| 21 | `21_phase6_score.py` | Phases 2–4 files | `PHASE6_RANKING.csv`, `ALPHA_LIST.csv` | Composite 0–100 score → Tiers |
| 22 | `22_prime_scan.py` | `universe.csv`, `PHASE5_DAY0.csv`, Yahoo | `prime_passers.*` | **Rescan full market** through the fingerprint |
| 23 | `23_watchlist.py` | `prime_passers.pkl`, Yahoo | **`PHASE7_WATCHLIST.csv`** | Validate + add entry/stop/target/size |
| 24 | `24_phase7_summary.py` | `PHASE7_WATCHLIST.csv` | `PHASE7_SUMMARY.md` | Final watchlist write-up |
| 25 | `25_build_frontend.py` | the phase CSVs | **`alphafinder_dashboard.html`** | Self-contained interactive dashboard |

---

## 5. How to run

```powershell
# Full pipeline (fetches live data — slow, network-dependent). Run in order:
Get-ChildItem [0-2][0-9]_*.py | Sort-Object Name | ForEach-Object { python $_.Name }

# Or just rebuild the dashboard from the CSVs already on disk (fast, no network):
python 25_build_frontend.py

# Then open it:
start alphafinder_dashboard.html
```

**Key contract to remember:** every step is independent and communicates only through files.
To re-run from any phase, you only need the file(s) in its *Reads* column to already exist.

> ⚠️ Mechanical signals only — **not investment advice.** A few presentation values in
> `25_build_frontend.py` (the Nifty market-context banner, the scan date, and the "76.2%" recall figure)
> are hard-coded constants, not recomputed at build time; everything in the data tables is live-fetched.
