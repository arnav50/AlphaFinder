# PHASE 3 — SUPPLY/DEMAND + SMC — SUMMARY
Scan date 2026-06-02 · 543 stocks · daily primary, weekly structure overlay.

## ✓ VERIFICATION CHECKPOINT (Phase 3)
- ✅ Demand & supply zones mapped on **daily and weekly** (`demand_zone_D/W`, `supply_zone_D/W`)
- ✅ **Order blocks** identified with **mitigation status** (`bull_OB`, `bear_OB`)
- ✅ **FVGs** listed with filled/unfilled counts + nearest unfilled (`unfilled_bull/bear_FVG`)
- ✅ **Liquidity pools** above/below + sweep detection (`buyside/sellside_liq`, `liquidity_swept`)
- ✅ **Market structure** daily+weekly (`structure_D/W`, alignment)
- ✅ **Premium/Discount** classification for every stock (`pd_zone`, `range_pos_pct`)

## Structural landscape
- **Market structure (daily):** {'bullish (HH/HL)': 276, 'ranging': 179, 'bearish (LH/LL)': 88}
- **Premium/Discount:** {'Premium': 511, 'Equilibrium': 25, 'Discount': 7}
- **Last BoS direction:** {'bull': 375, 'bear': 168}
- **Liquidity swept recently:** {'none': 455, 'buy-side swept (bearish stop-hunt)': 63, 'sell-side swept (bullish stop-hunt)': 25}
- **Unmitigated bullish order blocks (pullback support):** 255
- **Price near a demand zone:** 174 · **approaching overhead supply (long risk):** 20

> **Key institutional read:** 511/543 names sit in **Premium** (expensive, extended) — smart-money playbook is to wait for a retracement into discount / an unmitigated demand OB rather than chase. Only 7 are currently in a discount zone.

## Stocks currently in DISCOUNT (institutional buy zone)
| Symbol | Company | Range pos% | Structure(D) | Last BoS | Scorecard |
|---|---|--:|---|---|---|
| JINDALPOLY | Jindal Poly Films Limited | 44.4 | bearish (LH/LL) | bear @ 630.0 on 2026-06-30 | NEUTRAL |
| SETCO | Setco Automotive Limited | 37.8 | ranging | bear @ 15.93 on 2026-07-06 | MILD BULLISH |
| AXISCADES | AXISCADES Technologies Limited | 40.2 | bearish (LH/LL) | bear @ 1636.2 on 2026-07-06 | BEARISH |
| AVANTIFEED | Avanti Feeds Limited | 32.5 | bearish (LH/LL) | bull @ 971.85 on 2026-07-15 | MILD BULLISH |
| JYOTISTRUC | Jyoti Structures Limited | 43.6 | bearish (LH/LL) | bear @ 11.25 on 2026-07-17 | BEARISH |
| GUJALKALI | Gujarat Alkalies and Chemicals Limited | 43.6 | bearish (LH/LL) | bear @ 601.0 on 2026-07-07 | BEARISH |
| DSSL | Dynacons Systems & Solutions Limited | 37.9 | bullish (HH/HL) | bear @ 1261.1 on 2026-07-15 | BEARISH |

## High-conviction confluence: bullish structure + unmitigated demand OB + not in extreme premium
**62 stocks** meet bullish-structure + unmitigated-bull-OB + range_pos<85%:
| Symbol | Company | pos% | Bull OB | Demand zone | Scorecard |
|---|---|--:|---|---|---|
| ROLEXRINGS | Rolex Rings Limited | 72.5 | 140.0-143.82 (2026-07-10, UNMITIGATED) | 138.1-147.44 (Moderate, FRESH, 7.09% away) | BULLISH |
| JITFINFRA | JITF Infralogistics Limi | 69.0 | 294.0-299.8 (2026-07-09, UNMITIGATED) | 290.0-325.1 (Moderate, FRESH, 13.1% away) | BULLISH |
| J&KBANK | The Jammu & Kashmir Bank | 81.5 | 162.2-166.9 (2026-07-07, UNMITIGATED) | 162.2-171.0 (Moderate, FRESH, 6.84% away) | BULLISH |
| BLUESTONE | BlueStone Jewellery and  | 82.9 | 466.1-478.0 (2026-05-27, UNMITIGATED) | 421.0-465.5 (Moderate, tested, 28.69% away) | BULLISH |
| UNICHEMLAB | Unichem Laboratories Lim | 76.0 | 457.75-478.45 (2026-07-06, UNMITIGATED) | 454.05-486.0 (Moderate, FRESH, 21.2% away) | BULLISH |
| OMAXE | Omaxe Limited | 79.7 | 83.82-90.49 (2026-07-08, UNMITIGATED) | 78.0-88.9 (Moderate, tested, 5.17% away) | BULLISH |
| PPAP | PPAP Automotive Limited | 59.2 | 244.21-260.18 (2026-07-06, UNMITIGATED) | 243.31-331.95 (Moderate, tested, -10.67% away) | BULLISH |
| GODREJIND | Godrej Industries Limite | 84.5 | 1195.6-1234.0 (2026-07-07, UNMITIGATED) | 1195.6-1254.7 (Moderate, FRESH, 6.38% away) | BULLISH |
| PLASTIBLEN | Plastiblends India Limit | 81.4 | 168.1-179.91 (2026-07-08, UNMITIGATED) | 168.1-184.0 (Moderate, FRESH, 7.92% away) | BULLISH |
| FUSION | Fusion Finance Limited | 83.9 | 185.11-195.0 (2026-06-29, UNMITIGATED) | 182.0-197.96 (Moderate, FRESH, 14.11% away) | BULLISH |
| PIXTRANS | Pix Transmissions Limite | 79.1 | 1598.2-1626.0 (2026-06-24, UNMITIGATED) | 1598.2-1659.0 (Moderate, FRESH, 8.38% away) | BULLISH |
| DYCL | Dynamic Cables Limited | 79.2 | 360.1-367.25 (2026-07-10, UNMITIGATED) | 308.2-332.55 (Moderate, FRESH, 16.22% away) | BULLISH |
| GRINDWELL | Grindwell Norton Limited | 67.3 | 1971.0-2034.1 (2026-07-14, UNMITIGATED) | 1971.0-2083.9 (Moderate, tested, 0.13% away) | BULLISH |
| DALMIASUG | Dalmia Bharat Sugar and  | 66.3 | 331.75-341.6 (2026-07-02, UNMITIGATED) | 322.4-349.05 (Moderate, FRESH, 5.26% away) | BULLISH |
| UTLSOLAR | Fujiyama Power Systems L | 83.8 | 331.5-348.05 (2026-07-07, UNMITIGATED) | 194.55-204.0 (Moderate, FRESH, 79.0% away) | BULLISH |
| DIACABS | Diamond Power Infrastruc | 78.4 | 168.3-176.0 (2026-05-12, UNMITIGATED) | 168.06-184.75 (Moderate, tested, 20.37% away) | BULLISH |
| SKMEGGPROD | SKM Egg Products Export  | 76.8 | 291.8-310.0 (2026-07-08, UNMITIGATED) | 291.8-325.05 (Moderate, tested, -1.88% away) | BULLISH |
| IVALUE | Ivalue Infosolutions Lim | 81.3 | 226.98-234.9 (2026-06-11, UNMITIGATED) | none | BULLISH |
| VIPULLTD | Vipul Limited | 70.5 | 14.67-15.6 (2026-07-06, UNMITIGATED) | 8.61-9.41 (Moderate, tested, 66.21% away) | BULLISH |
| FERMENTA | Fermenta Biotech Limited | 79.7 | 348.15-383.05 (2026-07-08, UNMITIGATED) | 336.8-369.0 (Moderate, tested, 17.25% away) | BULLISH |
| MOREPENLAB | Morepen Laboratories Lim | 82.0 | 51.41-53.24 (2026-06-24, UNMITIGATED) | 42.5-46.42 (Moderate, FRESH, 26.88% away) | BULLISH |
| KIMS | Krishna Institute of Med | 80.5 | 735.3-752.25 (2026-06-03, UNMITIGATED) | 669.6-721.2 (Moderate, tested, 11.34% away) | BULLISH |
| TARSONS | Tarsons Products Limited | 75.9 | 260.0-273.1 (2026-07-01, UNMITIGATED) | 199.41-244.9 (Moderate, FRESH, 17.37% away) | BULLISH |
| SCANSTL | Scan Steels Limited | 82.1 | 39.47-43.0 (2026-07-08, UNMITIGATED) | 37.1-43.2 (Moderate, FRESH, 11.81% away) | BULLISH |
| NITCO | Nitco Limited | 84.6 | 103.58-106.52 (2026-07-14, UNMITIGATED) | 102.63-109.5 (Moderate, tested, 1.24% away) | BULLISH |

**Files:** `PHASE3_SMC.csv` (full table) · per-stock SMC appended to `reports/<symbol>.md`.