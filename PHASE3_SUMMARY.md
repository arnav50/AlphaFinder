# PHASE 3 — SUPPLY/DEMAND + SMC — SUMMARY
Scan date 2026-06-02 · 376 stocks · daily primary, weekly structure overlay.

## ✓ VERIFICATION CHECKPOINT (Phase 3)
- ✅ Demand & supply zones mapped on **daily and weekly** (`demand_zone_D/W`, `supply_zone_D/W`)
- ✅ **Order blocks** identified with **mitigation status** (`bull_OB`, `bear_OB`)
- ✅ **FVGs** listed with filled/unfilled counts + nearest unfilled (`unfilled_bull/bear_FVG`)
- ✅ **Liquidity pools** above/below + sweep detection (`buyside/sellside_liq`, `liquidity_swept`)
- ✅ **Market structure** daily+weekly (`structure_D/W`, alignment)
- ✅ **Premium/Discount** classification for every stock (`pd_zone`, `range_pos_pct`)

## Structural landscape
- **Market structure (daily):** {'bullish (HH/HL)': 214, 'ranging': 126, 'bearish (LH/LL)': 36}
- **Premium/Discount:** {'Premium': 368, 'Equilibrium': 6, 'Discount': 2}
- **Last BoS direction:** {'bull': 303, 'bear': 73}
- **Liquidity swept recently:** {'none': 341, 'sell-side swept (bullish stop-hunt)': 19, 'buy-side swept (bearish stop-hunt)': 16}
- **Unmitigated bullish order blocks (pullback support):** 193
- **Price near a demand zone:** 86 · **approaching overhead supply (long risk):** 11

> **Key institutional read:** 368/376 names sit in **Premium** (expensive, extended) — smart-money playbook is to wait for a retracement into discount / an unmitigated demand OB rather than chase. Only 2 are currently in a discount zone.

## Stocks currently in DISCOUNT (institutional buy zone)
| Symbol | Company | Range pos% | Structure(D) | Last BoS | Scorecard |
|---|---|--:|---|---|---|
| JINDALPOLY | Jindal Poly Films Limited | 38.6 | ranging | bear @ 630.0 on 2026-06-30 | BEARISH |
| DCMSIL | DCM Shriram International Limited | 36.8 | ranging | bull @ 69.39 on 2026-06-24 | BULLISH |

## High-conviction confluence: bullish structure + unmitigated demand OB + not in extreme premium
**28 stocks** meet bullish-structure + unmitigated-bull-OB + range_pos<85%:
| Symbol | Company | pos% | Bull OB | Demand zone | Scorecard |
|---|---|--:|---|---|---|
| PIXTRANS | Pix Transmissions Limite | 82.4 | 1598.2-1626.0 (2026-06-24, UNMITIGATED) | 1598.2-1659.0 (Moderate, FRESH, 9.14% away) | BULLISH |
| ICIL | Indo Count Industries Li | 84.9 | 386.3-401.0 (2026-06-22, UNMITIGATED) | 343.1-410.5 (Moderate, tested, 3.9% away) | BULLISH |
| MANCREDIT | Mangal Credit and Fincor | 82.6 | 165.7-169.9 (2026-05-22, UNMITIGATED) | 165.7-174.0 (Moderate, FRESH, 40.99% away) | BULLISH |
| 539730 | Fredun Pharmaceuticals L | 80.2 | 2270.0-2364.85 (2026-06-15, UNMITIGATED) | 2226.0-2375.0 (Moderate, FRESH, 9.0% away) | BULLISH |
| BOROSCI | Borosil Scientific Limit | 82.9 | 154.0-157.99 (2026-06-25, UNMITIGATED) | 153.05-162.01 (Moderate, FRESH, 2.74% away) | BULLISH |
| HAPPYFORGE | Happy Forgings Limited | 84.4 | 1422.1-1462.9 (2026-06-18, UNMITIGATED) | 1323.2-1384.0 (Moderate, FRESH, 8.32% away) | BULLISH |
| KIRLOSENG | Kirloskar Oil Engines Li | 70.6 | 1972.2-2052.7 (2026-06-18, UNMITIGATED) | 1910.0-2052.7 (Moderate, FRESH, 8.68% away) | BULLISH |
| PANAMAPET | Panama Petrochem Limited | 69.4 | 371.95-387.0 (2026-06-17, UNMITIGATED) | 371.95-418.95 (Moderate, tested, 1.58% away) | BULLISH |
| CARBORUNIV | Carborundum Universal Li | 70.7 | 1051.8-1073.7 (2026-06-16, UNMITIGATED) | 993.2-1082.5 (Moderate, FRESH, 5.27% away) | BULLISH |
| SAIPARENT | Sai Parenterals Limited | 71.4 | 492.0-505.0 (2026-06-03, UNMITIGATED) | 474.0-543.2 (Moderate, tested, 13.88% away) | BULLISH |
| CARYSIL | CARYSIL LIMITED | 83.4 | 1051.6-1123.0 (2026-06-08, UNMITIGATED) | 882.6-942.0 (Moderate, FRESH, 23.37% away) | BULLISH |
| INDOBORAX | Indo Borax & Chemicals L | 83.7 | 271.6-277.95 (2026-05-20, UNMITIGATED) | 268.7-284.45 (Moderate, FRESH, 37.9% away) | BULLISH |
| PANACEABIO | Panacea Biotec Limited | 73.0 | 395.0-443.9 (2026-06-01, UNMITIGATED) | 391.0-443.9 (Moderate, FRESH, 24.17% away) | BULLISH |
| SOTL | Savita Oil Technologies  | 73.0 | 411.65-445.0 (2026-06-01, UNMITIGATED) | 411.65-450.35 (Moderate, FRESH, 18.27% away) | BULLISH |
| UNIVASTU | Univastu India Limited | 83.1 | 80.5-83.49 (2026-06-15, UNMITIGATED) | 77.11-83.52 (Moderate, FRESH, 5.85% away) | BULLISH |
| ZENTEC | Zen Technologies Limited | 65.4 | 1607.1-1676.9 (2026-06-01, UNMITIGATED) | 1582.3-1714.4 (Moderate, tested, 1.88% away) | BULLISH |
| RRKABEL | R R Kabel Limited | 83.8 | 1964.3-2039.0 (2026-06-02, UNMITIGATED) | 1951.0-2130.0 (Moderate, tested, 10.01% away) | BULLISH |
| NIBE | NIBE Limited | 80.7 | 1413.0-1494.0 (2026-06-11, UNMITIGATED) | 1002.6-1409.5 (Moderate, tested, 16.92% away) | BULLISH |
| CALSOFT | California Software Comp | 67.3 | 19.8-20.53 (2026-06-11, UNMITIGATED) | 13.54-15.54 (Moderate, tested, 43.44% away) | BULLISH |
| DIACABS | Diamond Power Infrastruc | 80.6 | 168.3-176.0 (2026-05-12, UNMITIGATED) | 168.06-184.75 (Moderate, tested, 7.65% away) | BULLISH |
| FCL | Fineotex Chemical Limite | 71.3 | 30.64-34.12 (2026-05-21, UNMITIGATED) | 30.55-35.8 (Moderate, FRESH, 9.27% away) | BULLISH |
| IFCI | IFCI Limited | 59.7 | 70.01-73.27 (2026-06-11, UNMITIGATED) | 70.01-79.06 (Moderate, tested, -3.98% away) | MILD BULLISH |
| INOXINDIA | INOX India Limited | 77.9 | 1433.3-1510.0 (2026-06-01, UNMITIGATED) | 1469.1-1753.0 (Moderate, FRESH, 6.73% away) | MILD BULLISH |
| 535916 | Alacrity Securities Ltd | 67.2 | 58.99-60.0 (2026-04-29, UNMITIGATED) | 54.0-61.0 (Moderate, FRESH, 11.03% away) | MILD BULLISH |
| NETWEB | Netweb Technologies Indi | 63.5 | 3792.9-3908.6 (2026-05-25, UNMITIGATED) | 3792.9-4097.7 (Moderate, tested, 8.05% away) | NEUTRAL |

**Files:** `PHASE3_SMC.csv` (full table) · per-stock SMC appended to `reports/<symbol>.md`.