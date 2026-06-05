# PHASE 3 — SUPPLY/DEMAND + SMC — SUMMARY
Scan date 2026-06-02 · 311 stocks · daily primary, weekly structure overlay.

## ✓ VERIFICATION CHECKPOINT (Phase 3)
- ✅ Demand & supply zones mapped on **daily and weekly** (`demand_zone_D/W`, `supply_zone_D/W`)
- ✅ **Order blocks** identified with **mitigation status** (`bull_OB`, `bear_OB`)
- ✅ **FVGs** listed with filled/unfilled counts + nearest unfilled (`unfilled_bull/bear_FVG`)
- ✅ **Liquidity pools** above/below + sweep detection (`buyside/sellside_liq`, `liquidity_swept`)
- ✅ **Market structure** daily+weekly (`structure_D/W`, alignment)
- ✅ **Premium/Discount** classification for every stock (`pd_zone`, `range_pos_pct`)

## Structural landscape
- **Market structure (daily):** {'bullish (HH/HL)': 146, 'ranging': 123, 'bearish (LH/LL)': 42}
- **Premium/Discount:** {'Premium': 297, 'Equilibrium': 7, 'Discount': 7}
- **Last BoS direction:** {'bull': 239, 'bear': 70, 'none': 2}
- **Liquidity swept recently:** {'none': 284, 'buy-side swept (bearish stop-hunt)': 20, 'sell-side swept (bullish stop-hunt)': 7}
- **Unmitigated bullish order blocks (pullback support):** 149
- **Price near a demand zone:** 55 · **approaching overhead supply (long risk):** 9

> **Key institutional read:** 297/311 names sit in **Premium** (expensive, extended) — smart-money playbook is to wait for a retracement into discount / an unmitigated demand OB rather than chase. Only 7 are currently in a discount zone.

## Stocks currently in DISCOUNT (institutional buy zone)
| Symbol | Company | Range pos% | Structure(D) | Last BoS | Scorecard |
|---|---|--:|---|---|---|
| MANAKALUCO | Manaksia Aluminium Company Limited | 29.5 | bearish (LH/LL) | bear @ 34.41 on 2026-05-12 | NEUTRAL |
| MCL | Madhav Copper Limited | 35.6 | ranging | bull @ 64.31 on 2026-05-15 | MILD BEARISH |
| VIVIMEDLAB | Vivimed Labs Limited | 6.1 | bearish (LH/LL) | bear @ 6.46 on 2026-05-12 | BEARISH |
| 540693 | Shish Industries Ltd | 39.9 | bearish (LH/LL) | bear @ 12.49 on 2026-05-13 | MILD BULLISH |
| 513502 | Baroda Extrusion Ltd | 32.5 | bullish (HH/HL) | bull @ 9.54 on 2026-04-29 | BULLISH |
| JINDALPOLY | Jindal Poly Films Limited | 43.9 | ranging | bear @ 675.8 on 2026-06-01 | BEARISH |
| 540545 | Guru Krupa Gems and Jewellery Ltd | 41.7 | bullish (HH/HL) | bear @ 40.28 on 2026-05-22 | NEUTRAL |

## High-conviction confluence: bullish structure + unmitigated demand OB + not in extreme premium
**28 stocks** meet bullish-structure + unmitigated-bull-OB + range_pos<85%:
| Symbol | Company | pos% | Bull OB | Demand zone | Scorecard |
|---|---|--:|---|---|---|
| MARKSANS | Marksans Pharma Limited | 78.8 | 210.02-218.02 (2026-05-22, UNMITIGATED) | 210.02-223.76 (Moderate, FRESH, 7.79% away) | BULLISH |
| CUMMINSIND | Cummins India Limited | 82.3 | 5337.5-5419.5 (2026-05-25, UNMITIGATED) | 5335.5-5454.0 (Moderate, FRESH, 4.66% away) | BULLISH |
| WOCKPHARMA | Wockhardt Limited | 65.9 | 1569.0-1614.7 (2026-05-22, UNMITIGATED) | 1382.0-1603.9 (Moderate, tested, 22.59% away) | BULLISH |
| STEELXIND | STEEL EXCHANGE INDIA LIM | 80.4 | 9.91-10.75 (2026-05-25, UNMITIGATED) | 9.79-10.13 (Moderate, tested, 19.84% away) | BULLISH |
| MAYURUNIQ | Mayur Uniquoters Ltd | 81.9 | 600.75-631.5 (2026-05-18, UNMITIGATED) | 594.45-631.5 (Moderate, FRESH, 18.01% away) | BULLISH |
| GALAPREC | Gala Precision Engineeri | 76.5 | 825.95-844.05 (2026-05-20, UNMITIGATED) | 735.15-759.1 (Moderate, tested, 19.21% away) | BULLISH |
| SPARC | Sun Pharma Advanced Rese | 68.4 | 179.2-189.29 (2026-05-21, UNMITIGATED) | 158.21-189.45 (Moderate, FRESH, 7.81% away) | BULLISH |
| 526570 | Midwest Gold Ltd | 53.5 | 4050.0-4339.95 (2026-05-20, UNMITIGATED) | 2194.95-2396.55 (Moderate, tested, 92.65% away) | BULLISH |
| 500449 | Hindustan Organic Chemic | 79.1 | 35.16-36.59 (2026-05-22, UNMITIGATED) | 35.16-40.52 (Moderate, FRESH, 1.83% away) | BULLISH |
| ZIMLAB | Zim Laboratories Limited | 80.1 | 84.63-87.5 (2026-04-29, UNMITIGATED) | 65.52-71.0 (Moderate, tested, 46.35% away) | BULLISH |
| MIRCELECTR | MIRC Electronics Limited | 70.5 | 32.5-34.3 (2026-05-05, UNMITIGATED) | 32.2-34.89 (Moderate, FRESH, 17.63% away) | BULLISH |
| GANDHAR | Gandhar Oil Refinery (In | 63.8 | 139.51-142.71 (2026-05-13, UNMITIGATED) | 136.25-141.8 (Moderate, tested, 9.87% away) | BULLISH |
| POWERINDIA | Hitachi Energy India Lim | 83.8 | 31645.0-32660.0 (2026-05-13, UNMITIGATED) | 31195.0-33730.0 (Moderate, FRESH, 4.08% away) | BULLISH |
| 543916 | Hemant Surgical Industri | 74.3 | 298.0-329.95 (2026-05-08, UNMITIGATED) | 288.0-329.95 (Moderate, FRESH, 17.17% away) | BULLISH |
| TRITURBINE | Triveni Turbine Limited | 72.6 | 590.0-612.4 (2026-05-18, UNMITIGATED) | 557.2-612.9 (Moderate, FRESH, 12.46% away) | BULLISH |
| CRAFTSMAN | Craftsman Automation Lim | 76.9 | 7691.0-7843.5 (2026-05-06, UNMITIGATED) | 7611.0-7880.0 (Moderate, FRESH, 13.95% away) | BULLISH |
| 535916 | Alacrity Securities Ltd | 73.8 | 58.99-60.0 (2026-04-29, UNMITIGATED) | 54.0-61.0 (Moderate, FRESH, 14.61% away) | BULLISH |
| KOTYARK | Kotyark Industries Limit | 84.0 | 359.0-375.0 (2026-04-22, UNMITIGATED) | 271.0-338.0 (Moderate, tested, 24.39% away) | BULLISH |
| MENONBE | Menon Bearings Limited | 69.8 | 125.21-127.79 (2026-05-05, UNMITIGATED) | 112.2-124.61 (Moderate, tested, 14.18% away) | MILD BULLISH |
| DIACABS | Diamond Power Infrastruc | 82.7 | 168.3-176.0 (2026-05-12, UNMITIGATED) | 168.06-184.75 (Moderate, tested, 5.36% away) | MILD BULLISH |
| SHADOWFAX | Shadowfax Technologies L | 81.7 | 139.0-145.32 (2026-04-17, UNMITIGATED) | 117.01-136.4 (Moderate, tested, 40.05% away) | MILD BULLISH |
| KIRLPNU | Kirloskar Pneumatic Comp | 82.3 | 1325.0-1360.0 (2026-04-23, UNMITIGATED) | 1320.0-1374.3 (Moderate, FRESH, 14.86% away) | MILD BULLISH |
| 539132 | Wardwizard Foods and Bev | 75.9 | 8.84-9.85 (2026-04-24, UNMITIGATED) | 8.88-9.8 (Moderate, tested, 20.41% away) | MILD BULLISH |
| GKSL | Gujarat Kidney And Super | 71.8 | 120.01-129.9 (2026-05-05, UNMITIGATED) | 120.01-134.0 (Moderate, tested, 0.19% away) | NEUTRAL |
| POWERICA | Powerica Limited | 80.8 | 441.45-456.15 (2026-04-24, UNMITIGATED) | none | NEUTRAL |

**Files:** `PHASE3_SMC.csv` (full table) · per-stock SMC appended to `reports/<symbol>.md`.