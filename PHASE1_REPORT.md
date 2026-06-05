# PHASE 1 — UNIVERSE IDENTIFICATION (NSE + BSE)
**Scan date:** 2026-06-02  |  **180-day reference:** 2025-12-04  |  **Filter:** 180-day price return ≥ 25%

## Methodology (auditable, scripted — no hand-entered prices)
1. **Universe** — NSE official `EQUITY_L.csv` (series EQ+BE) + BSE active-equity scrip master (API), excluding BSE **Z / XT / XC** surveillance groups. Dual-listed companies de-duplicated by **ISIN** (NSE listing preferred).
2. **Prices** — ~180-day daily OHLCV per symbol from Yahoo Finance chart API (sources exchange data). Return = last close ÷ **median of ±2 bars around the 180-day date** (median guards against bad single prints).
3. **Liquidity filter** — avg daily volume ≥ 50,000 shares **OR** avg daily traded value ≥ ₹50 lakh.
4. **Verification (2 sources)** — (a) returns re-derived from **split/bonus-adjusted** prices → 0 corporate-action distortions; (b) current price cross-checked against the **other exchange's live quote** (BSE-twin via ISIN / BSE live API).

## ✓ VERIFICATION CHECKPOINT
- **Total verified stocks (180d return ≥ 25%): 312**
- Exchange split (after ISIN dedup, NSE preferred): {'NSE': 280, 'BSE': 32}
- Market-cap buckets: {'Small': 124, 'Mid': 78, 'Large': 62, 'Micro': 37}  *(Large ≥₹20k cr, Mid ≥₹5k cr, Small ≥₹500 cr, Micro <₹500 cr)*
- Penny stocks (price < ₹10): **12 flagged, none removed** (per spec)
- Cross-source current-price check: 301/312 have a 2nd exchange source; **298/301 agree within 5%** (median mismatch **0.11%**)
- Excluded categories (suspended / Z / XT / XC) removed at universe stage
- Sorted by Return% descending ✓

### ⚠ Price-discrepancy flags (NSE-vs-BSE > 5% — review before trading; all still >25%)
- `534755` Trio Mercantile & Trading Ltd (BSE): Yahoo ₹1.81 vs other-exchange ₹1.99 (9.1%)
- `UNIVPHOTO` Universus Photo Imagings Limited (NSE): Yahoo ₹403.95 vs other-exchange ₹457.70 (11.7%)
- `526570` Midwest Gold Ltd (BSE): Yahoo ₹4616.90 vs other-exchange ₹4386.10 (5.3%)

## OUTPUT — full ranked list
Columns: Symbol | Company | Exch | Price 180d ago | Price today | Return% | MktCap(₹cr) | Cap | Sector | AvgVol(sh) | AvgVal(₹)

| # | Symbol | Company | Exch | 180d Ago | Today | Return% | MktCap₹cr | Cap | Sector | AvgVol | AvgVal₹ |
|--:|---|---|---|--:|--:|--:|--:|---|---|--:|--:|
| 1 | STLTECH | Sterlite Technologies Limited | NSE | 98.96 | 591.05 | **497.3** | 28,868 | Large | Technology | 5,171,316 | 1,020,738,202 |
| 2 | DEEDEV | DEE Development Engineers Limited | NSE | 209.40 | 654.20 | **218.3** | 4,542 | Small | Industrials | 2,198,565 | 641,314,939 |
| 3 | 540492 | Starlineps Enterprises Ltd | BSE | 3.50 | 10.72 | **206.3** | 378 | Micro | nan | 1,522,324 | 9,556,235 |
| 4 | MTARTECH | Mtar Technologies Limited | NSE | 2383.90 | 7216.00 | **202.7** | 22,185 | Large | Industrials | 765,988 | 3,648,960,518 |
| 5 | SANGINITA | Sanginita Chemicals Limited | NSE | 9.72 | 29.77 | **201.9** | n/a | nan | Basic Materials | 169,348 | 2,775,086 |
| 6 | HFCL | HFCL Limited | NSE | 69.03 | 189.94 | **176.1** | 29,143 | Large | Technology | 32,771,741 | 3,377,526,611 |
| 7 | OMAXAUTO | Omax Autos Limited | NSE | 88.50 | 244.30 | **176.1** | 525 | Small | Consumer Cyclical | 140,984 | 21,365,252 |
| 8 | UFBL | United Foodbrands Limited | NSE | 180.54 | 487.20 | **170.0** | 1,916 | Small | Consumer Cyclical | 231,800 | 78,230,543 |
| 9 | BLISSGVS | Bliss GVS Pharma Limited | NSE | 171.23 | 434.45 | **167.9** | 4,599 | Small | Healthcare | 3,516,006 | 742,738,922 |
| 10 | OMNI | Omnitech Engineering Limited | NSE | 204.93 | 504.15 | **164.5** | 6,241 | Mid | Industrials | 1,164,065 | 368,908,482 |
| 11 | GVPIL | GE Power India Limited | NSE | 330.85 | 858.95 | **159.6** | 5,782 | Mid | Industrials | 631,469 | 307,094,862 |
| 12 | 534755 | Trio Mercantile & Trading Ltd | BSE | 0.69 | 1.81 🟡 | **158.6** | 14 | Micro | nan | 111,264 | 106,381 |
| 13 | BHAGYANGR | Bhagyanagar India Limited | NSE | 132.42 | 323.20 | **147.6** | 1,030 | Small | Basic Materials | 311,777 | 55,570,842 |
| 14 | AEROFLEX | Aeroflex Industries Limited | NSE | 176.75 | 419.45 | **137.3** | 5,549 | Mid | Industrials | 2,332,849 | 624,838,132 |
| 15 | KSHINTL | KSH International Limited | NSE | 355.00 | 814.75 | **137.3** | 5,522 | Mid | Industrials | 466,511 | 236,602,995 |
| 16 | SCPL | Sheetal Cool Products Limited | NSE | 199.66 | 456.20 | **128.5** | 479 | Micro | Consumer Defensive | 23,087 | 7,025,137 |
| 17 | KSHITIJPOL | Kshitij Polyline Limited | NSE | 2.28 | 5.19 🟡 | **127.6** | n/a | nan | Industrials | 435,675 | 1,576,685 |
| 18 | 539669 | RGF Capital Markets Ltd | BSE | 0.66 | 1.54 🟡 | **126.5** | 24 | Micro | nan | 469,720 | 408,587 |
| 19 | ANTELOPUS | Antelopus Selan Energy Limited | NSE | 380.40 | 854.20 | **124.5** | 3,004 | Small | Energy | 391,453 | 215,505,754 |
| 20 | ATLANTAELE | Atlanta Electricals Limited | NSE | 871.25 | 1952.50 | **124.1** | 15,031 | Mid | Industrials | 202,411 | 236,124,625 |
| 21 | 532380 | Baba Arts Ltd | BSE | 6.30 | 13.98 | **119.5** | 72 | Micro | nan | 56,956 | 712,114 |
| 22 | NOVARTIND | Novartis India Limited | NSE | 672.25 | 1465.50 | **118.0** | 3,617 | Small | Healthcare | 34,355 | 43,535,633 |
| 23 | SAKAR | Sakar Healthcare Limited | NSE | 375.90 | 834.60 | **116.5** | n/a | nan | Healthcare | 107,262 | 62,579,338 |
| 24 | SIGMAADV | SIGMA ADVANCED SYSTEMS LIMITED | NSE | 197.80 | 416.10 | **113.5** | 7,334 | Mid | Industrials | 250,310 | 61,443,438 |
| 25 | CPPLUS | Aditya Infotech Limited | NSE | 1511.90 | 3213.70 | **112.6** | 37,857 | Large | Industrials | 278,738 | 534,878,508 |
| 26 | BAJAJCON | Bajaj Consumer Care Limited | NSE | 268.95 | 571.65 | **112.5** | 7,491 | Mid | Consumer Defensive | 1,356,837 | 499,980,318 |
| 27 | SPORTKING | Sportking India Limited | NSE | 89.73 | 190.64 | **112.5** | 2,425 | Small | Consumer Cyclical | 289,619 | 39,793,235 |
| 28 | KOVAI | Kovai Medical Center & Hospital Limited | NSE | 2576.65 | 5342.00 | **107.3** | 5,840 | Mid | Healthcare | 3,677 | 20,242,759 |
| 29 | MODISONLTD | MODISON LIMITED | NSE | 152.38 | 313.70 | **107.2** | 1,019 | Small | Industrials | 106,152 | 21,320,213 |
| 30 | VIDYAWIRES | Vidya Wires Limited | NSE | 53.17 | 109.16 | **106.5** | 2,322 | Small | Industrials | 6,140,145 | 425,284,204 |
| 31 | RUBICON | Rubicon Research Limited | NSE | 635.80 | 1302.60 | **106.5** | 21,700 | Large | Healthcare | 553,544 | 428,164,074 |
| 32 | NGLFINE | NGL Fine-Chem Limited | NSE | 1299.50 | 2654.50 | **104.3** | 1,645 | Small | Healthcare | 7,752 | 17,670,585 |
| 33 | E2E | E2E Networks Limited | NSE | 2123.80 | 4324.40 | **101.8** | n/a | nan | Technology | 133,078 | 365,389,283 |
| 34 | BBOX | Black Box Limited | NSE | 528.50 | 1031.80 | **95.2** | 18,168 | Mid | Technology | 658,350 | 440,871,579 |
| 35 | CONFIPET | Confidence Petroleum India Limited | NSE | 36.03 | 69.81 | **93.8** | 2,323 | Small | Energy | 2,240,758 | 110,981,798 |
| 36 | RAIN | Rain Industries Limited | NSE | 104.68 | 197.90 | **89.0** | 6,658 | Mid | Basic Materials | 4,476,922 | 654,707,209 |
| 37 | SASKEN | Sasken Technologies Limited | NSE | 1259.90 | 2338.50 | **86.5** | 3,556 | Small | Technology | 106,517 | 180,258,472 |
| 38 | 526775 | Valiant Communications Ltd | BSE | 658.25 | 1264.60 | **86.5** | 1,411 | Small | nan | 14,119 | 13,155,854 |
| 39 | IDEAFORGE | Ideaforge Technology Limited | NSE | 445.35 | 828.90 | **86.1** | 3,591 | Small | Technology | 1,083,002 | 617,081,602 |
| 40 | ONELIFECAP | Onelife Capital Advisors Limited | NSE | 14.85 | 27.53 | **85.4** | 103 | Micro | Financial Services | 143,361 | 2,343,211 |
| 41 | VENUSREM | Venus Remedies Limited | NSE | 745.05 | 1411.30 | **85.0** | 1,890 | Small | Healthcare | 67,923 | 53,423,363 |
| 42 | WHEELS | Wheels India Limited | NSE | 828.35 | 1517.90 | **83.2** | 3,709 | Small | Consumer Cyclical | 115,858 | 138,430,485 |
| 43 | KESORAMIND | Kesoram Industries Limited | NSE | 6.54 | 11.98 | **83.2** | 374 | Micro | Basic Materials | 2,456,177 | 23,097,623 |
| 44 | PARKHOSPS | Park Medi World Limited | NSE | 147.95 | 282.65 | **82.5** | 12,217 | Mid | Healthcare | 1,553,656 | 279,244,829 |
| 45 | PARACABLES | Paramount Communications Limited | NSE | 36.26 | 65.90 | **81.7** | 2,005 | Small | Technology | 1,683,636 | 82,408,876 |
| 46 | POWERINDIA | Hitachi Energy India Limited | NSE | 19305.00 | 35105.00 | **80.0** | 156,460 | Large | Industrials | 159,463 | 3,816,591,454 |
| 47 | PRECWIRE | Precision Wires India Limited | NSE | 238.35 | 428.45 | **79.8** | 7,834 | Mid | Industrials | 1,221,498 | 357,770,592 |
| 48 | NINSYS | NINtec Systems Limited | NSE | 402.75 | 721.35 | **79.8** | 1,335 | Small | Technology | 13,387 | 5,346,596 |
| 49 | SHADOWFAX | Shadowfax Technologies Limited | NSE | 109.98 | 191.03 | **79.2** | 11,189 | Mid | Industrials | 3,057,431 | 440,901,339 |
| 50 | DJML | DJ Mediaprint & Logistics Limited | NSE | 59.53 | 104.14 | **78.9** | 359 | Micro | Industrials | 144,967 | 11,670,622 |
| 51 | GAYAPROJ | Gayatri Projects Limited | NSE | 11.53 | 20.61 | **78.8** | 382 | Micro | Industrials | 187,424 | 3,362,664 |
| 52 | SWANDEF | Swan Defence and Heavy Industries Limited | NSE | 1142.20 | 2038.30 | **78.5** | 10,773 | Mid | Industrials | 12,164 | 22,230,836 |
| 53 | NEOGEN | Neogen Chemicals Limited | NSE | 1054.70 | 1876.90 | **78.0** | 5,137 | Mid | Basic Materials | 175,464 | 219,638,322 |
| 54 | ACUTAAS | Acutaas Chemicals Limited | NSE | 1707.60 | 3037.60 | **77.9** | 24,906 | Large | Basic Materials | 437,874 | 938,168,414 |
| 55 | BALAMINES | Balaji Amines Limited | NSE | 1126.20 | 2016.10 | **77.9** | 6,536 | Mid | Basic Materials | 342,002 | 459,063,890 |
| 56 | NITTAGELA | Nitta Gelatin India Limited | NSE | 922.65 | 1642.00 | **77.4** | 1,490 | Small | Basic Materials | 16,466 | 21,953,230 |
| 57 | TDPOWERSYS | TD Power Systems Limited | NSE | 696.70 | 1235.00 | **77.3** | 19,300 | Mid | Industrials | 1,286,644 | 1,164,292,450 |
| 58 | SALSTEEL | S.A.L. Steel Limited | NSE | 36.63 | 61.67 | **76.4** | 665 | Small | Basic Materials | 137,644 | 6,300,905 |
| 59 | SANSERA | Sansera Engineering Limited | NSE | 1657.10 | 2953.30 | **75.6** | 18,394 | Mid | Consumer Cyclical | 220,483 | 481,770,721 |
| 60 | THERMAX | Thermax Limited | NSE | 2845.70 | 4969.70 | **74.6** | 59,191 | Large | Industrials | 191,692 | 723,235,302 |
| 61 | MIRCELECTR | MIRC Electronics Limited | NSE | 23.53 | 41.04 | **74.4** | 1,510 | Small | Consumer Cyclical | 1,589,952 | 56,168,512 |
| 62 | INDSWFTLAB | Ind-Swift Laboratories Limited | NSE | 95.90 | 162.10 | **74.0** | 1,408 | Small | Healthcare | 701,828 | 95,944,627 |
| 63 | KERNEX | Kernex Microsystems (India) Limited | NSE | 1007.50 | 1804.70 | **73.8** | 3,036 | Small | Technology | 257,605 | 336,091,441 |
| 64 | CUPID | Cupid Limited | NSE | 73.02 | 128.35 | **71.7** | 17,259 | Mid | Consumer Defensive | 29,649,432 | 2,523,688,213 |
| 65 | INDOTECH | Indo Tech Transformers Limited | NSE | 1592.50 | 2722.80 | **71.0** | 2,879 | Small | Industrials | 47,112 | 91,376,747 |
| 66 | GVT&D | GE Vernova T&D India Limited | NSE | 2768.80 | 4781.00 | **70.4** | 122,471 | Large | Industrials | 819,274 | 2,869,865,812 |
| 67 | ROLLT | Rollatainers Limited | NSE | 1.37 | 2.14 🟡 | **69.8** | 53 | Micro | Real Estate | 399,431 | 647,161 |
| 68 | FCL | Fineotex Chemical Limited | NSE | 25.41 | 42.36 | **69.8** | 4,929 | Small | Basic Materials | 9,043,569 | 285,716,274 |
| 69 | RPTECH | Rashi Peripherals Limited | NSE | 325.00 | 554.20 | **69.4** | 3,654 | Small | Technology | 162,930 | 66,754,046 |
| 70 | AVALON | Avalon Technologies Limited | NSE | 862.45 | 1511.90 | **68.8** | 10,083 | Mid | Technology | 307,391 | 353,783,103 |
| 71 | SGMART | SG Mart Limited | NSE | 343.55 | 578.20 | **68.3** | 6,863 | Mid | Industrials | 315,854 | 140,431,158 |
| 72 | WELCORP | Welspun Corp Limited | NSE | 826.60 | 1386.80 | **67.8** | 36,572 | Large | Basic Materials | 753,239 | 736,121,110 |
| 73 | DSSL | Dynacons Systems & Solutions Limited | NSE | 895.90 | 1502.90 | **67.8** | 1,912 | Small | Technology | 167,332 | 189,948,514 |
| 74 | LOKESHMACH | Lokesh Machines Limited | NSE | 148.76 | 248.95 | **67.3** | 497 | Micro | Industrials | 85,245 | 16,784,298 |
| 75 | SBCL | Shivalik Bimetal Controls Limited | NSE | 436.05 | 734.55 | **67.2** | 4,227 | Small | Industrials | 254,543 | 144,524,795 |
| 76 | APOLLO | Apollo Micro Systems Limited | NSE | 261.90 | 437.00 | **66.9** | 15,599 | Mid | Industrials | 8,990,866 | 2,785,261,673 |
| 77 | SKYGOLD | SKY GOLD AND DIAMONDS LIMITED | NSE | 336.50 | 559.70 | **66.8** | 8,660 | Mid | Consumer Cyclical | 1,051,487 | 412,557,444 |
| 78 | UNIVPHOTO | Universus Photo Imagings Limited | NSE | 262.50 | 403.95 | **65.9** | 501 | Small | Healthcare | 16,716 | 6,969,568 |
| 79 | SEAMECLTD | Seamec Limited | NSE | 1011.30 | 1643.30 | **65.5** | 4,186 | Small | Industrials | 78,861 | 102,556,467 |
| 80 | APEX | Apex Frozen Foods Limited | NSE | 266.85 | 441.20 | **65.3** | 1,382 | Small | Consumer Defensive | 1,312,291 | 486,922,407 |
| 81 | ADANIPOWER | Adani Power Limited | NSE | 143.78 | 235.93 | **65.3** | 454,926 | Large | Utilities | 32,978,854 | 5,861,357,150 |
| 82 | KIRLOSENG | Kirloskar Oil Engines Limited | NSE | 1130.80 | 1856.90 | **65.3** | 27,051 | Large | Industrials | 603,370 | 787,323,242 |
| 83 | KOTYARK | Kotyark Industries Limited | NSE | 267.70 | 420.45 | **64.4** | 431 | Micro | Basic Materials | 29,031 | 10,769,169 |
| 84 | APOLLOPIPE | Apollo Pipes Limited | NSE | 292.40 | 478.85 | **63.8** | 2,115 | Small | Industrials | 949,146 | 383,841,409 |
| 85 | MCLEODRUSS | Mcleod Russel India Limited | NSE | 46.25 | 75.32 | **62.9** | 785 | Small | Consumer Defensive | 511,278 | 25,743,547 |
| 86 | NATIONALUM | National Aluminium Company Limited | NSE | 273.15 | 434.40 | **61.9** | 79,792 | Large | Basic Materials | 13,951,217 | 4,883,558,398 |
| 87 | SUVEN | Suven Life Sciences Limited | NSE | 170.18 | 275.20 | **61.7** | 7,272 | Mid | Healthcare | 638,575 | 138,713,818 |
| 88 | JNKINDIA | JNK India Limited | NSE | 220.54 | 361.40 | **61.4** | 2,025 | Small | Industrials | 354,233 | 98,079,929 |
| 89 | NARMADA | Narmada Agrobase Limited | NSE | 22.72 | 36.54 | **60.8** | 139 | Micro | Basic Materials | 213,283 | 6,892,874 |
| 90 | CENTUM | Centum Electronics Limited | NSE | 2210.90 | 3600.00 | **60.6** | 5,297 | Mid | Technology | 68,176 | 184,770,949 |
| 91 | SEDEMAC | SEDEMAC Mechatronics Limited | NSE | 1451.10 | 2326.00 | **60.3** | 10,318 | Mid | Consumer Cyclical | 271,618 | 469,516,081 |
| 92 | SATIN | Satin Creditcare Network Limited | NSE | 144.21 | 231.12 | **60.3** | 2,556 | Small | Financial Services | 463,830 | 92,437,459 |
| 93 | GRWRHITECH | Garware Hi-Tech Films Limited | NSE | 3704.70 | 5894.50 | **59.7** | 13,656 | Mid | Basic Materials | 92,484 | 385,652,390 |
| 94 | NITINSPIN | Nitin Spinners Limited | NSE | 319.95 | 507.30 | **58.6** | 2,852 | Small | Consumer Cyclical | 368,615 | 143,722,363 |
| 95 | ADANIENSOL | Adani Energy Solutions Limited | NSE | 978.85 | 1530.60 | **57.5** | 183,910 | Large | Utilities | 2,122,950 | 2,423,403,464 |
| 96 | UTLSOLAR | Fujiyama Power Systems Limited | NSE | 204.28 | 319.80 | **57.1** | 9,819 | Mid | Technology | 728,867 | 169,077,687 |
| 97 | SCHNEIDER | Schneider Electric Infrastructure Limited | NSE | 753.45 | 1181.30 | **56.8** | 28,263 | Large | Industrials | 310,628 | 263,348,751 |
| 98 | 543787 | Macfos Ltd | BSE | 736.18 | 1150.00 | **56.2** | 1,210 | Small | nan | 9,874 | 8,448,770 |
| 99 | SAIL | Steel Authority of India Limited | NSE | 132.54 | 205.85 | **56.0** | 84,977 | Large | Basic Materials | 23,818,901 | 3,792,434,661 |
| 100 | ELPROINTL | Elpro International Limited | NSE | 105.35 | 167.65 | **55.9** | 2,840 | Small | nan | 281,224 | 41,274,100 |
| 101 | IOLCP | IOL Chemicals and Pharmaceuticals Limited | NSE | 84.40 | 131.42 | **55.7** | 3,858 | Small | Healthcare | 1,982,482 | 198,243,085 |
| 102 | 521113 | Suditi Industries Ltd | BSE | 59.56 | 91.01 | **55.6** | 436 | Micro | nan | 70,588 | 5,219,994 |
| 103 | SHILPAMED | Shilpa Medicare Limited | NSE | 331.65 | 517.35 | **55.1** | 10,123 | Mid | Healthcare | 565,995 | 221,330,996 |
| 104 | KRISHNADEF | Krishna Defence And Allied Industries Limited | NSE | 741.70 | 1148.80 | **54.9** | n/a | nan | Industrials | 122,053 | 123,324,597 |
| 105 | BIRLACABLE | Birla Cable Limited | NSE | 138.38 | 213.78 | **54.5** | 644 | Small | Technology | 67,483 | 10,370,071 |
| 106 | ACMESOLAR | Acme Solar Holdings Limited | NSE | 212.64 | 334.75 | **54.1** | 20,249 | Large | Utilities | 1,447,928 | 387,119,778 |
| 107 | SYRMA | Syrma SGS Technology Limited | NSE | 743.25 | 1166.80 | **54.1** | 22,491 | Large | Technology | 1,593,114 | 1,369,097,618 |
| 108 | VIJIFIN | Viji Finance Limited | NSE | 2.50 | 3.83 🟡 | **53.8** | 55 | Micro | Financial Services | 373,680 | 1,066,654 |
| 109 | NIBE | NIBE Limited | NSE | 998.50 | 1541.00 | **53.6** | 2,300 | Small | Industrials | 102,273 | 124,887,000 |
| 110 | 524520 | KMC Speciality Hospitals (India) Ltd | BSE | 74.96 | 115.00 | **53.4** | 1,939 | Small | nan | 100,627 | 8,685,223 |
| 111 | 544191 | Purple Finance Ltd | BSE | 42.60 | 66.18 | **53.1** | 391 | Micro | nan | 86,450 | 4,832,781 |
| 112 | NETWEB | Netweb Technologies India Limited | NSE | 3081.60 | 4782.80 | **52.9** | 27,194 | Large | Technology | 1,731,744 | 6,287,426,276 |
| 113 | APARINDS | Apar Industries Limited | NSE | 8899.00 | 13270.00 | **51.1** | 53,250 | Large | Industrials | 108,912 | 1,101,231,987 |
| 114 | CMPDI | Central Mine Planning & Design Institute Limited | NSE | 154.06 | 235.55 | **51.0** | 16,829 | Mid | Basic Materials | 5,917,477 | 1,246,906,624 |
| 115 | ARVIND | Arvind Limited | NSE | 331.80 | 500.65 | **50.9** | 13,129 | Mid | Consumer Cyclical | 649,058 | 249,466,056 |
| 116 | ROSSTECH | Rossell Techsys Limited | NSE | 717.15 | 1080.50 | **50.7** | 4,067 | Small | Industrials | 195,866 | 150,955,468 |
| 117 | KIRLPNU | Kirloskar Pneumatic Company Limited | NSE | 1033.30 | 1578.50 | **50.6** | 10,252 | Mid | Industrials | 116,975 | 149,979,643 |
| 118 | HINDCOPPER | Hindustan Copper Limited | NSE | 371.85 | 546.20 | **50.3** | 52,833 | Large | Basic Materials | 19,898,546 | 10,414,438,207 |
| 119 | ARFIN | Arfin India Limited | NSE | 60.77 | 90.85 | **49.5** | 1,537 | Small | Basic Materials | 1,120,121 | 94,347,128 |
| 120 | LLOYDSME | Lloyds Metals And Energy Limited | NSE | 1220.30 | 1821.70 | **49.4** | 99,337 | Large | Basic Materials | 578,448 | 804,830,722 |
| 121 | CEIGALL | Ceigall India Limited | NSE | 232.91 | 347.80 | **49.3** | 6,057 | Mid | Industrials | 388,225 | 117,298,617 |
| 122 | JAYBARMARU | Jay Bharat Maruti Limited | NSE | 84.46 | 126.14 | **49.3** | 1,368 | Small | Consumer Cyclical | 584,910 | 62,670,182 |
| 123 | WALCHANNAG | Walchandnagar Industries Limited | NSE | 158.50 | 238.75 | **49.2** | 1,620 | Small | Industrials | 1,713,614 | 341,305,219 |
| 124 | JINDALSAW | Jindal Saw Limited | NSE | 161.60 | 241.12 | **49.2** | 15,419 | Mid | Basic Materials | 5,395,182 | 1,041,536,454 |
| 125 | MAYURUNIQ | Mayur Uniquoters Ltd | NSE | 499.95 | 745.25 | **49.1** | 3,238 | Small | Consumer Cyclical | 129,934 | 80,928,248 |
| 126 | HIRECT | Hind Rectifiers Limited | NSE | 756.70 | 1109.50 | **49.0** | 3,824 | Small | Industrials | 136,090 | 115,315,935 |
| 127 | HARDWYN | Hardwyn India Limited | NSE | 17.90 | 25.44 | **49.0** | 1,244 | Small | Industrials | 2,463,631 | 50,822,401 |
| 128 | EXICOM | Exicom Tele-Systems Limited | NSE | 107.33 | 159.72 | **48.8** | 2,224 | Small | Industrials | 1,138,433 | 152,573,650 |
| 129 | SUNFLAG | Sunflag Iron And Steel Company Limited | NSE | 254.00 | 375.85 | **48.8** | 6,787 | Mid | Basic Materials | 402,607 | 133,921,589 |
| 130 | BUILDPRO | Shankara Buildpro Limited | NSE | 812.55 | 1146.30 | **48.5** | 2,775 | Small | Consumer Cyclical | 80,372 | 79,712,540 |
| 131 | BHEL | Bharat Heavy Electricals Limited | NSE | 277.75 | 410.75 | **48.3** | 143,095 | Large | Industrials | 14,219,092 | 4,257,508,843 |
| 132 | HONASA | Honasa Consumer Limited | NSE | 274.95 | 407.05 | **48.0** | 13,221 | Mid | Consumer Defensive | 1,648,646 | 543,091,737 |
| 133 | EMPOWER | Empower India Limited | NSE | 1.40 | 2.22 🟡 | **48.0** | 261 | Micro | nan | 3,438,298 | 8,400,803 |
| 134 | WOCKPHARMA | Wockhardt Limited | NSE | 1360.00 | 1966.20 | **47.6** | 31,988 | Large | Healthcare | 1,356,621 | 2,119,258,309 |
| 135 | MANAKALUCO | Manaksia Aluminium Company Limited | NSE | 24.54 | 35.42 | **47.2** | 232 | Micro | Basic Materials | 289,331 | 12,346,734 |
| 136 | ASTRAMICRO | Astra Microwave Products Limited | NSE | 908.35 | 1323.80 | **47.1** | 12,565 | Mid | Technology | 454,285 | 506,019,787 |
| 137 | DBOL | Dhampur Bio Organics Limited | NSE | 77.56 | 112.72 | **46.4** | 747 | Small | Consumer Defensive | 183,060 | 18,790,207 |
| 138 | ZIMLAB | Zim Laboratories Limited | NSE | 71.41 | 103.91 | **46.4** | 545 | Small | Healthcare | 123,906 | 9,644,192 |
| 139 | BANDHANBNK | Bandhan Bank Limited | NSE | 140.08 | 206.33 | **46.3** | 33,235 | Large | Financial Services | 10,603,016 | 1,797,907,679 |
| 140 | EMMVEE | Emmvee Photovoltaic Power Limited | NSE | 212.66 | 310.75 | **46.1** | 21,535 | Large | Technology | 4,364,247 | 1,038,996,845 |
| 141 | RRKABEL | R R Kabel Limited | NSE | 1368.20 | 2023.80 | **46.1** | 22,934 | Large | Industrials | 382,725 | 613,548,841 |
| 142 | MWL | Mangalam Worldwide Limited | NSE | 260.41 | 380.50 | **46.1** | 1,132 | Small | Basic Materials | 80,111 | 22,959,736 |
| 143 | NLCINDIA | NLC India Limited | NSE | 239.40 | 349.10 | **45.9** | 48,380 | Large | Utilities | 3,326,962 | 1,013,943,402 |
| 144 | 538668 | Meghna Infracon Infrastructure Ltd | BSE | 530.55 | 774.10 | **45.9** | 1,661 | Small | nan | 53,388 | 34,318,778 |
| 145 | COCKERILL | John Cockerill India Limited | NSE | 5277.35 | 7593.50 | **45.6** | 3,750 | Small | Industrials | 11,548 | 74,360,919 |
| 146 | DATAPATTNS | Data Patterns (India) Limited | NSE | 2766.30 | 4025.20 | **45.5** | 22,489 | Large | Industrials | 867,566 | 2,864,670,421 |
| 147 | IFCI | IFCI Limited | NSE | 49.38 | 71.64 | **45.1** | 19,316 | Mid | Financial Services | 23,743,607 | 1,414,728,354 |
| 148 | QPOWER | Quality Power Electrical Equipments Limited | NSE | 717.20 | 1040.50 | **45.1** | 8,032 | Mid | Industrials | 944,045 | 870,305,188 |
| 149 | KOPRAN | Kopran Limited | NSE | 135.42 | 195.92 | **44.7** | 942 | Small | Healthcare | 514,291 | 82,497,495 |
| 150 | 542669 | BMW Industries Ltd | BSE | 37.89 | 54.63 | **44.7** | 1,213 | Small | nan | 209,922 | 9,260,395 |
| 151 | JAYNECOIND | Jayaswal Neco Industries Limited | NSE | 66.28 | 99.52 | **44.1** | 9,647 | Mid | Basic Materials | 6,724,334 | 567,731,315 |
| 152 | VINDHYATEL | Vindhya Telelinks Limited | NSE | 1471.30 | 2117.90 | **44.0** | 2,508 | Small | Industrials | 45,347 | 72,522,246 |
| 153 | AYMSYNTEX | AYM Syntex Limited | NSE | 155.16 | 223.99 | **43.6** | 1,318 | Small | Consumer Cyclical | 29,914 | 5,734,024 |
| 154 | SOLARINDS | Solar Industries India Limited | NSE | 12819.00 | 18386.00 | **43.4** | 166,404 | Large | Basic Materials | 153,780 | 2,197,742,937 |
| 155 | 539519 | Sattva Sukun Lifecare Ltd | BSE | 0.56 | 0.76 🟡 | **43.4** | 29 | Micro | nan | 2,432,521 | 1,628,609 |
| 156 | SGFIN | SG Finserve Limited | NSE | 396.70 | 567.90 | **43.2** | 3,178 | Small | Financial Services | 272,272 | 125,301,291 |
| 157 | ADANIGREEN | Adani Green Energy Limited | NSE | 1017.70 | 1449.40 | **43.1** | 238,766 | Large | Utilities | 3,653,106 | 3,887,980,298 |
| 158 | KSR | KSR Footwear Limited | NSE | 23.70 | 33.91 | **43.1** | 62 | Micro | Consumer Cyclical | 104,804 | 2,634,057 |
| 159 | NEPHROPLUS | Nephrocare Health Services Limited | NSE | 471.25 | 660.45 | **43.0** | 6,614 | Mid | Healthcare | 388,507 | 198,749,537 |
| 160 | AFIL | Akme Fintrade (India) Limited | NSE | 7.05 | 10.04 | **42.4** | 427 | Micro | Financial Services | 1,653,831 | 12,455,820 |
| 161 | ATHERENERG | Ather Energy Limited | NSE | 675.20 | 960.60 | **42.3** | 36,755 | Large | Consumer Cyclical | 3,532,907 | 2,732,550,305 |
| 162 | BSE | BSE Limited | NSE | 2815.90 | 3931.90 | **42.2** | n/a | nan | Financial Services | 4,489,526 | 13,458,612,958 |
| 163 | KRN | KRN Heat Exchanger and Refrigeration Limited | NSE | 783.05 | 1104.60 | **42.1** | 6,846 | Mid | Technology | 896,932 | 864,543,772 |
| 164 | PAISALO | Paisalo Digital Limited | NSE | 37.08 | 52.69 | **42.1** | 4,774 | Small | Financial Services | 7,372,265 | 302,843,161 |
| 165 | VTL | Vardhman Textiles Limited | NSE | 432.65 | 613.85 | **42.1** | 17,773 | Mid | Consumer Cyclical | 594,440 | 299,414,481 |
| 166 | THANGAMAYL | Thangamayil Jewellery Limited | NSE | 3223.30 | 4590.70 | **41.6** | 14,266 | Mid | Consumer Cyclical | 166,767 | 586,276,283 |
| 167 | AVANTIFEED | Avanti Feeds Limited | NSE | 819.60 | 1158.60 | **41.6** | 15,785 | Mid | Consumer Defensive | 1,165,067 | 1,313,454,681 |
| 168 | STEELXIND | STEEL EXCHANGE INDIA LIMITED | NSE | 8.63 | 12.14 | **41.5** | 1,510 | Small | Basic Materials | 2,076,630 | 20,488,258 |
| 169 | 542046 | Vivid Mercantile Ltd | BSE | 4.94 | 7.07 🟡 | **41.4** | 70 | Micro | nan | 464,724 | 3,236,744 |
| 170 | ABSLAMC | Aditya Birla Sun Life AMC Limited | NSE | 726.50 | 1027.20 | **41.4** | 29,609 | Large | Financial Services | 404,581 | 369,654,192 |
| 171 | MCX | Multi Commodity Exchange of India Limited | NSE | 2068.60 | 2878.70 | **41.4** | 73,444 | Large | Financial Services | 3,289,824 | 8,076,801,580 |
| 172 | ADVAIT | Advait Energy Transitions Limited | NSE | 1391.80 | 1972.40 | **41.2** | 2,157 | Small | Industrials | 54,825 | 100,096,301 |
| 173 | LLOYDSENGG | LLOYDS ENGINEERING WORKS LIMITED | NSE | 52.64 | 72.13 | **41.1** | 10,570 | Mid | Industrials | 5,547,353 | 312,426,526 |
| 174 | AGIIL | Agi Infra Limited | NSE | 276.75 | 381.60 | **41.0** | 4,774 | Small | Real Estate | 1,877,497 | 604,661,065 |
| 175 | NDLVENTURE | NDL Ventures Limited | NSE | 96.68 | 133.54 | **40.7** | 447 | Micro | Communication Services | 43,952 | 5,053,039 |
| 176 | HINDALCO | Hindalco Industries Limited | NSE | 823.25 | 1146.30 | **40.4** | 257,555 | Large | Basic Materials | 6,120,977 | 5,659,203,337 |
| 177 | EBGNG | GNG Electronics Limited | NSE | 315.20 | 441.40 | **40.0** | 5,020 | Mid | Technology | 297,348 | 111,122,771 |
| 178 | KPL | Kwality Pharmaceuticals Limited | NSE | 1662.60 | 2298.80 | **40.0** | 2,380 | Small | nan | 46,665 | 93,165,731 |
| 179 | ABB | ABB India Limited | NSE | 5173.50 | 7146.00 | **39.6** | 151,453 | Large | Industrials | 355,712 | 2,161,522,484 |
| 180 | INDOBORAX | Indo Borax & Chemicals Limited | NSE | 251.69 | 345.90 | **39.6** | 1,109 | Small | Basic Materials | 94,235 | 26,332,560 |
| 181 | SHREEJISPG | Shreeji Shipping Global Limited | NSE | 329.70 | 465.65 | **39.4** | 7,593 | Mid | Industrials | 1,118,487 | 401,062,662 |
| 182 | STYLAMIND | Stylam Industries Limited | NSE | 2147.50 | 2957.90 | **39.4** | 5,017 | Mid | Consumer Cyclical | 65,437 | 145,906,971 |
| 183 | GAUDIUMIVF | Gaudium IVF and Women Health Limited | NSE | 80.26 | 112.39 | **39.1** | 814 | Small | Healthcare | 1,238,651 | 120,160,587 |
| 184 | BODALCHEM | Bodal Chemicals Limited | NSE | 52.02 | 72.37 | **39.1** | 924 | Small | Basic Materials | 304,318 | 18,659,456 |
| 185 | GESHIP | The Great Eastern Shipping Company Limited | NSE | 1091.00 | 1517.20 | **39.1** | 22,292 | Large | Industrials | 753,082 | 1,080,453,249 |
| 186 | DREDGECORP | Dredging Corporation of India Limited | NSE | 880.55 | 1223.30 | **38.9** | 3,431 | Small | Industrials | 624,090 | 619,106,763 |
| 187 | GRANULES | Granules India Limited | NSE | 560.85 | 777.55 | **38.6** | 19,250 | Mid | Healthcare | 1,089,235 | 686,610,063 |
| 188 | MAHABANK | Bank of Maharashtra | NSE | 56.98 | 78.91 | **38.6** | 60,763 | Large | Financial Services | 22,319,234 | 1,488,969,935 |
| 189 | TMB | Tamilnad Mercantile Bank Limited | NSE | 534.25 | 739.75 | **38.5** | 11,690 | Mid | Financial Services | 370,313 | 234,509,629 |
| 190 | KRISHANA | Krishana Phoschem Limited | NSE | 497.30 | 686.45 | **38.4** | n/a | nan | Basic Materials | 167,885 | 98,876,095 |
| 191 | NAHARSPING | Nahar Spinning Mills Limited | NSE | 199.36 | 275.00 | **38.1** | 979 | Small | Consumer Cyclical | 28,857 | 5,838,988 |
| 192 | 540252 | Viram Suvarn Ltd | BSE | 8.78 | 11.88 | **38.0** | 132 | Micro | nan | 397,414 | 4,281,650 |
| 193 | DECNGOLD | Deccan Gold Mines Limited | NSE | 120.20 | 165.80 | **37.9** | 3,297 | Small | nan | 1,729,583 | 256,218,802 |
| 194 | 543542 | Kesar India Ltd | BSE | 900.00 | 1240.20 | **37.8** | 3,538 | Small | nan | 9,649 | 11,416,911 |
| 195 | POWERICA | Powerica Limited | NSE | 390.00 | 543.75 | **37.7** | 6,900 | Mid | Industrials | 520,560 | 242,444,608 |
| 196 | 535916 | Alacrity Securities Ltd | BSE | 52.30 | 69.91 | **37.6** | 336 | Micro | nan | 53,146 | 3,162,805 |
| 197 | J&KBANK | The Jammu & Kashmir Bank Limited | NSE | 103.15 | 141.92 | **37.6** | 15,620 | Mid | Financial Services | 4,437,763 | 521,600,543 |
| 198 | AMBIKCO | Ambika Cotton Mills Limited | NSE | 1237.20 | 1697.60 | **37.5** | 972 | Small | Consumer Cyclical | 10,179 | 14,424,835 |
| 199 | YASHO | Yasho Industries Limited | NSE | 1578.60 | 2168.00 | **37.3** | 2,612 | Small | Basic Materials | 25,060 | 38,929,130 |
| 200 | TIRUPATIFL | Tirupati Forge Limited | NSE | 32.87 | 45.05 | **37.1** | n/a | nan | Industrials | 462,084 | 18,197,860 |
| 201 | CGPOWER | CG Power and Industrial Solutions Limited | NSE | 661.35 | 907.70 | **37.0** | 142,920 | Large | Industrials | 3,333,942 | 2,376,459,429 |
| 202 | UNIVCABLES | Universal Cables Limited | NSE | 907.25 | 1239.20 | **36.6** | 4,306 | Small | Industrials | 178,517 | 167,694,382 |
| 203 | GOCLCORP | GOCL Corporation Limited | NSE | 292.90 | 400.80 | **36.6** | 1,982 | Small | Basic Materials | 182,138 | 52,816,288 |
| 204 | BHARATFORG | Bharat Forge Limited | NSE | 1406.00 | 1902.90 | **36.5** | 90,911 | Large | Consumer Cyclical | 1,257,721 | 2,089,276,251 |
| 205 | 500449 | Hindustan Organic Chemicals Ltd | BSE | 30.55 | 41.26 | **36.4** | 271 | Micro | nan | 72,500 | 2,398,620 |
| 206 | FINCABLES | Finolex Cables Limited | NSE | 736.55 | 1002.10 | **36.0** | 15,331 | Mid | Industrials | 434,751 | 396,190,268 |
| 207 | LAURUSLABS | Laurus Labs Limited | NSE | 1026.10 | 1382.60 | **36.0** | 74,673 | Large | Healthcare | 1,884,183 | 2,008,157,412 |
| 208 | KINGFA | Kingfa Science & Technology (India) Limited | NSE | 3927.20 | 5340.00 | **36.0** | 7,248 | Mid | Basic Materials | 6,147 | 28,347,801 |
| 209 | DIACABS | Diamond Power Infrastructure Limited | NSE | 144.32 | 194.65 | **35.9** | 10,273 | Mid | Industrials | 2,458,372 | 401,369,833 |
| 210 | SBC | SBC Exports Limited | NSE | 27.50 | 36.81 | **35.8** | 1,755 | Small | Industrials | 11,848,893 | 357,019,102 |
| 211 | HAPPYFORGE | Happy Forgings Limited | NSE | 1038.80 | 1409.00 | **35.6** | 13,296 | Mid | Industrials | 69,727 | 85,336,133 |
| 212 | 526570 | Midwest Gold Ltd | BSE | 3240.65 | 4616.90 | **35.4** | 5,284 | Mid | nan | 5,715 | 23,826,028 |
| 213 | BELRISE | Belrise Industries Limited | NSE | 160.97 | 217.89 | **35.3** | 19,399 | Mid | Consumer Cyclical | 6,332,717 | 1,134,754,522 |
| 214 | SPARC | Sun Pharma Advanced Research Company Limited | NSE | 152.94 | 204.24 | **34.8** | 6,622 | Mid | Healthcare | 4,229,222 | 715,338,341 |
| 215 | CALSOFT | California Software Company Limited | NSE | 16.70 | 22.12 | **34.7** | 53 | Micro | Technology | 107,328 | 1,969,930 |
| 216 | MBAPL | Madhya Bharat Agro Products Limited | NSE | 407.00 | 543.25 | **34.7** | n/a | nan | Basic Materials | 207,633 | 98,228,839 |
| 217 | MCL | Madhav Copper Limited | NSE | 45.82 | 61.59 | **34.4** | n/a | nan | Basic Materials | 133,912 | 9,012,153 |
| 218 | ADFFOODS | ADF Foods Limited | NSE | 201.50 | 273.15 | **34.1** | 3,000 | Small | Consumer Defensive | 229,534 | 52,795,383 |
| 219 | ADANIENT | Adani Enterprises Limited | NSE | 2265.40 | 2968.10 | **33.8** | 383,427 | Large | Energy | 1,866,739 | 4,275,678,964 |
| 220 | MENONBE | Menon Bearings Limited | NSE | 106.54 | 142.28 | **33.4** | 801 | Small | Consumer Cyclical | 74,207 | 9,652,434 |
| 221 | GRAPHITE | Graphite India Limited | NSE | 537.50 | 721.35 | **33.4** | 14,093 | Mid | Industrials | 1,629,787 | 1,073,683,403 |
| 222 | SOUTHWEST | South West Pinnacle Exploration Limited | NSE | 204.28 | 265.00 | **33.2** | 786 | Small | Energy | 270,589 | 57,797,659 |
| 223 | NAM-INDIA | Nippon Life India Asset Management Limited | NSE | 814.00 | 1089.90 | **33.1** | 69,579 | Large | Financial Services | 967,058 | 901,500,142 |
| 224 | GHCLTEXTIL | GHCL Textiles Limited | NSE | 73.12 | 97.17 | **33.1** | 929 | Small | Consumer Cyclical | 279,875 | 23,435,264 |
| 225 | SENORES | Senores Pharmaceuticals Limited | NSE | 776.75 | 1033.50 | **33.0** | 4,774 | Small | Healthcare | 322,491 | 283,226,030 |
| 226 | 519477 | CIAN Agro Industries & Infrastructure Ltd | BSE | 1119.45 | 1492.55 | **33.0** | 4,386 | Small | nan | 79,443 | 106,047,072 |
| 227 | IDEA | Vodafone Idea Limited | NSE | 10.80 | 14.16 | **32.6** | 153,414 | Large | Communication Services | 511,512,159 | 5,487,755,669 |
| 228 | SCI | Shipping Corporation Of India Limited | NSE | 232.26 | 302.70 | **32.5** | 14,102 | Mid | Industrials | 8,209,022 | 2,276,113,028 |
| 229 | 543916 | Hemant Surgical Industries Ltd | BSE | 294.60 | 386.60 | **32.5** | 503 | Small | nan | 26,392 | 8,533,191 |
| 230 | DHANBANK | Dhanlaxmi Bank Limited | NSE | 25.52 | 33.72 | **32.1** | 1,330 | Small | Financial Services | 1,244,824 | 35,691,732 |
| 231 | SIGNPOST | Signpost India Limited | NSE | 205.94 | 275.00 | **32.1** | 1,469 | Small | Communication Services | 66,339 | 16,390,133 |
| 232 | KISSHT | OnEMI Technology Solutions Limited | NSE | 208.63 | 275.55 | **32.1** | 4,666 | Small | Financial Services | 9,225,440 | 2,063,798,114 |
| 233 | 531911 | Galaxy Agrico Exports Ltd | BSE | 47.37 | 61.87 | **31.9** | 96 | Micro | nan | 110,988 | 4,973,995 |
| 234 | POLYCAB | Polycab India Limited | NSE | 7257.00 | 9531.50 | **31.9** | 143,519 | Large | Industrials | 403,254 | 3,137,912,135 |
| 235 | GAEL | Gujarat Ambuja Exports Limited | NSE | 115.32 | 155.62 | **31.8** | 7,125 | Mid | Consumer Defensive | 988,533 | 134,416,099 |
| 236 | MIDHANI | Mishra Dhatu Nigam Limited | NSE | 311.95 | 410.75 | **31.7** | 7,696 | Mid | Basic Materials | 1,155,677 | 416,641,818 |
| 237 | DIVGIITTS | Divgi Torqtransfer Systems Limited | NSE | 600.75 | 789.45 | **31.4** | 2,414 | Small | Consumer Cyclical | 32,966 | 24,062,823 |
| 238 | HSCL | Himadri Speciality Chemical Limited | NSE | 476.75 | 607.10 | **31.3** | 30,706 | Large | Basic Materials | 3,657,898 | 1,997,088,010 |
| 239 | GULPOLY | Gulshan Polyols Limited | NSE | 139.76 | 183.03 | **31.3** | 1,145 | Small | Basic Materials | 214,403 | 36,241,655 |
| 240 | GLAND | Gland Pharma Limited | NSE | 1751.60 | 2277.00 | **31.2** | 37,486 | Large | Healthcare | 236,179 | 465,278,022 |
| 241 | CLEANMAX | Clean Max Enviro Energy Solutions Limited | NSE | 867.50 | 1123.80 | **31.1** | 13,164 | Mid | Utilities | 425,527 | 408,396,174 |
| 242 | 539132 | Wardwizard Foods and Beverages Ltd | BSE | 8.99 | 11.80 | **31.0** | 309 | Micro | nan | 522,861 | 5,335,884 |
| 243 | MMWL | Media Matrix Worldwide Limited | NSE | 10.35 | 13.49 | **31.0** | 1,535 | Small | Communication Services | 205,875 | 2,970,969 |
| 244 | ANGELONE | Angel One Limited | NSE | 264.17 | 342.65 | **30.5** | 31,250 | Large | Financial Services | 9,444,410 | 2,557,173,717 |
| 245 | SANSTAR | Sanstar Limited | NSE | 88.66 | 115.77 | **30.4** | 2,114 | Small | Basic Materials | 369,196 | 36,312,464 |
| 246 | 543828 | Sudarshan Pharma Industries Ltd | BSE | 26.43 | 34.35 | **30.4** | 820 | Small | nan | 223,605 | 5,817,994 |
| 247 | VIVIMEDLAB | Vivimed Labs Limited | NSE | 4.95 | 6.45 🟡 | **30.3** | 54 | Micro | Healthcare | 197,986 | 1,617,667 |
| 248 | RUBYMILLS | The Ruby Mills Limited | NSE | 214.39 | 279.05 | **30.2** | 934 | Small | Consumer Cyclical | 49,388 | 11,591,124 |
| 249 | GMDCLTD | Gujarat Mineral Development Corporation Limited | NSE | 514.40 | 668.40 | **29.9** | 21,258 | Large | Energy | 4,856,840 | 2,941,378,301 |
| 250 | RAMRAT | Ram Ratna Wires Limited | NSE | 305.00 | 395.90 | **29.8** | 3,706 | Small | Industrials | 172,171 | 65,241,868 |
| 251 | GKSL | Gujarat Kidney And Super Speciality Limited | NSE | 104.54 | 134.25 | **29.8** | 1,058 | Small | Healthcare | 1,109,747 | 123,149,909 |
| 252 | NELCAST | Nelcast Limited | NSE | 107.35 | 139.87 | **29.6** | 1,212 | Small | Industrials | 188,276 | 23,844,050 |
| 253 | SONAMLTD | SONAM LIMITED | NSE | 44.27 | 57.08 | **29.6** | n/a | nan | Consumer Cyclical | 65,110 | 3,102,375 |
| 254 | SPECTRUM | Spectrum Electrical Industries Limited | NSE | 1135.20 | 1473.70 | **29.6** | 2,323 | Small | Industrials | 8,251 | 11,024,955 |
| 255 | STLNETWORK | STL Networks Limited | NSE | 22.06 | 28.58 | **29.6** | 1,395 | Small | Communication Services | 2,723,950 | 68,523,107 |
| 256 | VIJAYA | Vijaya Diagnostic Centre Limited | NSE | 1017.35 | 1317.00 | **29.4** | 13,529 | Mid | Healthcare | 207,666 | 225,806,560 |
| 257 | SAILIFE | Sai Life Sciences Limited | NSE | 875.90 | 1128.30 | **29.4** | 23,929 | Large | Healthcare | 545,305 | 532,187,509 |
| 258 | AARTIIND | Aarti Industries Limited | NSE | 363.05 | 469.75 | **29.4** | 17,022 | Mid | Basic Materials | 1,096,665 | 464,940,185 |
| 259 | AETHER | Aether Industries Limited | NSE | 847.50 | 1098.70 | **29.4** | 14,560 | Mid | Basic Materials | 332,404 | 335,763,664 |
| 260 | 540693 | Shish Industries Ltd | BSE | 9.65 | 12.45 | **29.0** | 521 | Small | nan | 1,785,547 | 25,147,612 |
| 261 | ROLEXRINGS | Rolex Rings Limited | NSE | 109.15 | 140.58 | **28.8** | 3,830 | Small | Industrials | 2,878,541 | 414,362,636 |
| 262 | APCOTEXIND | Apcotex Industries Limited | NSE | 383.90 | 494.10 | **28.7** | 2,561 | Small | Basic Materials | 47,947 | 21,182,934 |
| 263 | GUJALKALI | Gujarat Alkalies and Chemicals Limited | NSE | 516.80 | 664.85 | **28.6** | 4,885 | Small | Basic Materials | 1,964,119 | 1,157,024,847 |
| 264 | JINDALPOLY | Jindal Poly Films Limited | NSE | 509.60 | 655.15 | **28.6** | 2,869 | Small | Consumer Cyclical | 228,585 | 151,580,031 |
| 265 | MARKSANS | Marksans Pharma Limited | NSE | 183.97 | 241.19 | **28.4** | 10,917 | Mid | Healthcare | 1,378,083 | 285,523,955 |
| 266 | LENSKART | Lenskart Solutions Limited | NSE | 417.20 | 524.20 | **28.3** | 90,997 | Large | Healthcare | 5,456,033 | 2,529,363,663 |
| 267 | 513502 | Baroda Extrusion Ltd | BSE | 7.24 | 9.23 🟡 | **28.2** | 173 | Micro | nan | 273,341 | 2,747,796 |
| 268 | OFSS | Oracle Financial Services Software Limited | NSE | 8219.00 | 10344.50 | **28.1** | 90,036 | Large | Technology | 193,806 | 1,600,792,853 |
| 269 | JSWENERGY | JSW Energy Limited | NSE | 461.95 | 588.55 | **28.0** | 107,937 | Large | Utilities | 3,364,552 | 1,708,501,709 |
| 270 | 539730 | Fredun Pharmaceuticals Ltd | BSE | 1874.10 | 2396.35 | **27.9** | 1,300 | Small | nan | 11,889 | 21,703,406 |
| 271 | TARIL | Transformers And Rectifiers (India) Limited | NSE | 236.90 | 312.35 | **27.8** | 9,371 | Mid | Industrials | 6,101,180 | 1,816,086,385 |
| 272 | NSLNISP | NMDC Steel Limited | NSE | 41.13 | 52.55 | **27.8** | 15,392 | Mid | Basic Materials | 6,266,042 | 274,181,906 |
| 273 | CUMMINSIND | Cummins India Limited | NSE | 4468.90 | 5708.00 | **27.7** | 158,233 | Large | Industrials | 633,467 | 2,937,891,140 |
| 274 | 544141 | Pune E - Stock Broking Ltd | BSE | 216.40 | 276.40 | **27.7** | 446 | Micro | nan | 26,015 | 5,968,793 |
| 275 | 544023 | Kalyani Cast-Tech Ltd | BSE | 474.05 | 605.20 | **27.7** | 420 | Micro | nan | 10,000 | 5,530,917 |
| 276 | AVADHSUGAR | Avadh Sugar & Energy Limited | NSE | 358.10 | 456.45 | **27.5** | 915 | Small | Consumer Defensive | 74,846 | 31,171,486 |
| 277 | TIMEX | Timex Group India Limited | NSE | 344.55 | 435.60 | **27.4** | 4,395 | Small | Consumer Cyclical | 589,996 | 239,828,516 |
| 278 | ADVENZYMES | Advanced Enzyme Technologies Limited | NSE | 305.90 | 392.10 | **27.4** | 4,382 | Small | Basic Materials | 262,873 | 87,886,747 |
| 279 | 531626 | Orosil Smiths India Ltd | BSE | 4.61 | 5.87 🟡 | **27.3** | 25 | Micro | nan | 57,281 | 301,005 |
| 280 | ICICIAMC | ICICI Prudential Asset Management Company Limited | NSE | 2585.90 | 3322.10 | **27.3** | 164,052 | Large | Financial Services | 821,225 | 2,324,164,339 |
| 281 | CRAFTSMAN | Craftsman Automation Limited | NSE | 7102.50 | 8979.00 | **27.3** | 21,397 | Large | Consumer Cyclical | 80,855 | 644,934,910 |
| 282 | PIRAMALFIN | Piramal Finance Limited | NSE | 1484.60 | 1908.30 | **27.1** | 43,176 | Large | Financial Services | 424,724 | 762,825,992 |
| 283 | CEMPRO | Cemindia Projects Limited | NSE | 820.85 | 1041.70 | **26.9** | 17,889 | Mid | Industrials | 723,142 | 601,795,440 |
| 284 | SKIPPER | Skipper Limited | NSE | 451.55 | 572.40 | **26.8** | 6,456 | Mid | Industrials | 512,114 | 229,332,329 |
| 285 | NRBBEARING | NRB Bearing Limited | NSE | 281.20 | 356.45 | **26.8** | 3,458 | Small | Consumer Cyclical | 332,349 | 100,504,630 |
| 286 | STEELCAS | Steelcast Limited | NSE | 216.84 | 273.50 | **26.6** | 2,758 | Small | Basic Materials | 87,397 | 20,563,380 |
| 287 | WSTCSTPAPR | West Coast Paper Mills Limited | NSE | 411.45 | 520.75 | **26.6** | 3,441 | Small | Basic Materials | 85,862 | 39,457,493 |
| 288 | RHETAN | Rhetan TMT Limited | NSE | 24.01 | 30.34 | **26.5** | 2,417 | Small | Basic Materials | 3,419,052 | 88,146,186 |
| 289 | BHARATWIRE | Bharat Wire Ropes Limited | NSE | 171.78 | 217.23 | **26.5** | 1,492 | Small | Basic Materials | 706,050 | 149,201,039 |
| 290 | AYE | Aye Finance Limited | NSE | 128.91 | 163.98 | **26.4** | 4,058 | Small | Financial Services | 2,033,070 | 270,153,517 |
| 291 | KEI | KEI Industries Limited | NSE | 4163.50 | 5261.50 | **26.4** | 50,313 | Large | Industrials | 346,858 | 1,566,620,997 |
| 292 | HALDYNGL | Haldyn Glass Limited | NSE | 89.05 | 111.62 | **26.4** | 599 | Small | nan | 99,994 | 10,739,410 |
| 293 | AKUMS | Akums Drugs and Pharmaceuticals Limited | NSE | 420.00 | 531.25 | **26.4** | 8,344 | Mid | Healthcare | 220,720 | 105,322,449 |
| 294 | TRITURBINE | Triveni Turbine Limited | NSE | 545.40 | 689.25 | **26.4** | 21,906 | Large | Industrials | 1,535,016 | 905,960,309 |
| 295 | AZAD | Azad Engineering Limited | NSE | 1626.80 | 2066.10 | **26.4** | 13,333 | Mid | Industrials | 266,378 | 485,291,049 |
| 296 | TATASTEEL | Tata Steel Limited | NSE | 167.11 | 210.60 | **26.3** | 262,964 | Large | Basic Materials | 29,239,770 | 5,649,651,683 |
| 297 | RISHABH | Rishabh Instruments Limited | NSE | 409.40 | 516.80 | **26.2** | 1,999 | Small | Technology | 112,290 | 52,419,876 |
| 298 | GROWW | Billionbrains Garage Ventures Limited | NSE | 151.18 | 190.81 | **26.2** | 119,700 | Large | Financial Services | 63,094,546 | 10,771,662,021 |
| 299 | VISHNU | Vishnu Chemicals Limited | NSE | 497.00 | 626.70 | **26.1** | 4,219 | Small | Basic Materials | 112,958 | 61,368,338 |
| 300 | 540545 | Guru Krupa Gems and Jewellery Ltd | BSE | 28.96 | 36.50 | **25.9** | 57 | Micro | nan | 130,541 | 4,633,110 |
| 301 | TIPSMUSIC | Tips Music Limited | NSE | 525.70 | 672.30 | **25.9** | 8,602 | Mid | Communication Services | 383,287 | 219,962,613 |
| 302 | HINDZINC | Hindustan Zinc Limited | NSE | 498.10 | 625.10 | **25.8** | 264,125 | Large | Basic Materials | 9,323,398 | 5,629,402,724 |
| 303 | INOXINDIA | INOX India Limited | NSE | 1137.80 | 1452.20 | **25.8** | 13,187 | Mid | Industrials | 132,801 | 176,950,511 |
| 304 | 530145 | Kisan Mouldings Ltd | BSE | 27.65 | 34.77 | **25.8** | 406 | Micro | nan | 157,682 | 4,866,973 |
| 305 | MMFL | MM Forgings Limited | NSE | 351.45 | 442.55 | **25.7** | 2,140 | Small | Industrials | 180,941 | 71,944,402 |
| 306 | ELECTHERM | Electrotherm (India) Limited | NSE | 813.85 | 1028.30 | **25.6** | 1,321 | Small | Basic Materials | 47,361 | 39,912,160 |
| 307 | GALAPREC | Gala Precision Engineering Limited | NSE | 721.00 | 904.90 | **25.5** | 1,154 | Small | Industrials | 19,156 | 15,203,313 |
| 308 | 530883 | Super Crop Safe Ltd | BSE | 7.92 | 9.94 🟡 | **25.5** | 40 | Micro | nan | 60,269 | 542,491 |
| 309 | SIS | SIS LIMITED | NSE | 329.05 | 412.50 | **25.4** | 5,857 | Mid | Industrials | 124,871 | 43,007,231 |
| 310 | PREMIERPOL | Premier Polyfilm Limited | NSE | 44.57 | 55.85 | **25.3** | 585 | Small | Basic Materials | 200,854 | 10,549,545 |
| 311 | PANACEABIO | Panacea Biotec Limited | NSE | 344.15 | 430.60 | **25.1** | 2,635 | Small | Healthcare | 525,998 | 211,120,320 |
| 312 | GANDHAR | Gandhar Oil Refinery (India) Limited | NSE | 124.60 | 155.79 | **25.0** | 1,529 | Small | Energy | 958,712 | 153,996,591 |

🟡 = penny stock (price < ₹10), flagged not removed.

**Machine-readable file:** `FINAL_universe_25pct.csv` (312 rows).

### Known limitations (full disclosure)
- 464 universe symbols (of 4,524) returned no Yahoo history (recently renamed post-corporate-action e.g. demerged Tata Motors, thinly-traded, or delisted-from-Yahoo) — excluded from the scan, not from reality. These are predominantly illiquid BSE micro-caps.
- 11 NSE-only names have no BSE twin, so their current price rests on Yahoo alone (still passes the adjusted-return integrity check).
- Sector unavailable for 37 BSE-only micro-caps (shown as n/a).