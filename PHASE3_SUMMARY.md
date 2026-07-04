# PHASE 3 — SUPPLY/DEMAND + SMC — SUMMARY
Scan date 2026-06-02 · 355 stocks · daily primary, weekly structure overlay.

## ✓ VERIFICATION CHECKPOINT (Phase 3)
- ✅ Demand & supply zones mapped on **daily and weekly** (`demand_zone_D/W`, `supply_zone_D/W`)
- ✅ **Order blocks** identified with **mitigation status** (`bull_OB`, `bear_OB`)
- ✅ **FVGs** listed with filled/unfilled counts + nearest unfilled (`unfilled_bull/bear_FVG`)
- ✅ **Liquidity pools** above/below + sweep detection (`buyside/sellside_liq`, `liquidity_swept`)
- ✅ **Market structure** daily+weekly (`structure_D/W`, alignment)
- ✅ **Premium/Discount** classification for every stock (`pd_zone`, `range_pos_pct`)

## Structural landscape
- **Market structure (daily):** {'bullish (HH/HL)': 194, 'ranging': 124, 'bearish (LH/LL)': 37}
- **Premium/Discount:** {'Premium': 347, 'Equilibrium': 6, 'Discount': 2}
- **Last BoS direction:** {'bull': 298, 'bear': 57}
- **Liquidity swept recently:** {'none': 320, 'buy-side swept (bearish stop-hunt)': 18, 'sell-side swept (bullish stop-hunt)': 17}
- **Unmitigated bullish order blocks (pullback support):** 184
- **Price near a demand zone:** 84 · **approaching overhead supply (long risk):** 11

> **Key institutional read:** 347/355 names sit in **Premium** (expensive, extended) — smart-money playbook is to wait for a retracement into discount / an unmitigated demand OB rather than chase. Only 2 are currently in a discount zone.

## Stocks currently in DISCOUNT (institutional buy zone)
| Symbol | Company | Range pos% | Structure(D) | Last BoS | Scorecard |
|---|---|--:|---|---|---|
| DCMSIL | DCM Shriram International Limited | 38.7 | ranging | bull @ 69.39 on 2026-06-24 | BULLISH |
| JINDALPOLY | Jindal Poly Films Limited | 39.1 | ranging | bear @ 630.0 on 2026-06-30 | BEARISH |

## High-conviction confluence: bullish structure + unmitigated demand OB + not in extreme premium
**22 stocks** meet bullish-structure + unmitigated-bull-OB + range_pos<85%:
| Symbol | Company | pos% | Bull OB | Demand zone | Scorecard |
|---|---|--:|---|---|---|
| 532380 | Baba Arts Ltd-$ | 81.2 | 14.02-14.52 (2026-06-25, UNMITIGATED) | 13.12-15.37 (Moderate, tested, -2.47% away) | BULLISH |
| KIRLOSENG | Kirloskar Oil Engines Li | 76.2 | 1972.2-2052.7 (2026-06-18, UNMITIGATED) | 1910.0-2052.7 (Moderate, FRESH, 13.26% away) | BULLISH |
| MANCREDIT | Mangal Credit and Fincor | 82.2 | 165.7-169.9 (2026-05-22, UNMITIGATED) | 165.7-174.0 (Moderate, FRESH, 36.25% away) | BULLISH |
| BOROSCI | Borosil Scientific Limit | 84.0 | 154.0-157.99 (2026-06-25, UNMITIGATED) | 153.05-162.01 (Moderate, FRESH, 3.3% away) | BULLISH |
| DIVGIITTS | Divgi Torqtransfer Syste | 81.0 | 823.0-873.8 (2026-06-23, UNMITIGATED) | 825.0-881.0 (Moderate, FRESH, 10.35% away) | BULLISH |
| PANAMAPET | Panama Petrochem Limited | 70.3 | 371.95-387.0 (2026-06-17, UNMITIGATED) | 371.95-418.95 (Moderate, tested, 2.14% away) | BULLISH |
| RAMCOSYS | Ramco Systems Limited | 81.3 | 553.0-568.0 (2026-06-22, UNMITIGATED) | 550.5-732.0 (Moderate, FRESH, 5.2% away) | BULLISH |
| SAIPARENT | Sai Parenterals Limited | 73.8 | 492.0-505.0 (2026-06-03, UNMITIGATED) | 474.0-543.2 (Moderate, tested, 15.23% away) | BULLISH |
| PANACEABIO | Panacea Biotec Limited | 70.4 | 395.0-443.9 (2026-06-01, UNMITIGATED) | 391.0-443.9 (Moderate, FRESH, 22.08% away) | BULLISH |
| ZENTEC | Zen Technologies Limited | 70.5 | 1607.1-1676.9 (2026-06-01, UNMITIGATED) | 1582.3-1714.4 (Moderate, tested, 4.29% away) | BULLISH |
| INOXINDIA | INOX India Limited | 78.1 | 1433.3-1510.0 (2026-06-01, UNMITIGATED) | 1469.1-1753.0 (Moderate, FRESH, 6.88% away) | BULLISH |
| CALSOFT | California Software Comp | 69.8 | 19.8-20.53 (2026-06-11, UNMITIGATED) | 13.54-15.54 (Moderate, tested, 46.14% away) | BULLISH |
| NIBE | NIBE Limited | 81.2 | 1413.0-1494.0 (2026-06-11, UNMITIGATED) | 1002.6-1409.5 (Moderate, tested, 17.26% away) | BULLISH |
| INDOBORAX | Indo Borax & Chemicals L | 77.2 | 271.6-277.95 (2026-05-20, UNMITIGATED) | 268.7-284.45 (Moderate, FRESH, 33.59% away) | BULLISH |
| SOTL | Savita Oil Technologies  | 67.3 | 411.65-445.0 (2026-06-01, UNMITIGATED) | 411.65-450.35 (Moderate, FRESH, 14.03% away) | BULLISH |
| UNIVASTU | Univastu India Limited | 84.6 | 80.5-83.49 (2026-06-15, UNMITIGATED) | 77.11-83.52 (Moderate, FRESH, 6.56% away) | BULLISH |
| VENUSREM | Venus Remedies Limited | 81.5 | 1004.35-1055.0 (2026-05-21, UNMITIGATED) | 664.1-800.0 (Moderate, FRESH, 122.74% away) | MILD BULLISH |
| IFCI | IFCI Limited | 61.4 | 70.01-73.27 (2026-06-11, UNMITIGATED) | 70.01-79.06 (Moderate, tested, -2.95% away) | MILD BULLISH |
| TMB | Tamilnad Mercantile Bank | 78.6 | 676.1-693.85 (2026-05-27, UNMITIGATED) | 637.5-676.05 (Moderate, tested, 9.68% away) | MILD BULLISH |
| FCL | Fineotex Chemical Limite | 66.0 | 30.64-34.12 (2026-05-21, UNMITIGATED) | 30.55-35.8 (Moderate, FRESH, 5.11% away) | NEUTRAL |
| NETWEB | Netweb Technologies Indi | 63.0 | 3792.9-3908.6 (2026-05-25, UNMITIGATED) | 3792.9-4097.7 (Moderate, tested, 7.77% away) | NEUTRAL |
| HSCL | Himadri Speciality Chemi | 75.7 | 580.9-614.7 (2026-06-03, UNMITIGATED) | none | NEUTRAL |

**Files:** `PHASE3_SMC.csv` (full table) · per-stock SMC appended to `reports/<symbol>.md`.