# PHASE 1 — UNIVERSE IDENTIFICATION (NSE + BSE)
**Scan date:** 2026-06-02  |  **180-day reference:** 2025-12-04  |  **Filter:** 180-day price return ≥ 25%

## Methodology (auditable, scripted — no hand-entered prices)
1. **Universe** — NSE official `EQUITY_L.csv` (series EQ+BE) + BSE active-equity scrip master (API), excluding BSE **Z / XT / XC** surveillance groups. Dual-listed companies de-duplicated by **ISIN** (NSE listing preferred).
2. **Prices** — ~180-day daily OHLCV per symbol from Yahoo Finance chart API (sources exchange data). Return = last close ÷ **median of ±2 bars around the 180-day date** (median guards against bad single prints).
3. **Liquidity filter** — avg daily volume ≥ 50,000 shares **OR** avg daily traded value ≥ ₹50 lakh.
4. **Verification (2 sources)** — (a) returns re-derived from **split/bonus-adjusted** prices → 0 corporate-action distortions; (b) current price cross-checked against the **other exchange's live quote** (BSE-twin via ISIN / BSE live API).

## ✓ VERIFICATION CHECKPOINT
- **Total verified stocks (180d return ≥ 25%): 309**
- Exchange split (after ISIN dedup, NSE preferred): {'NSE': 286, 'BSE': 23}
- Market-cap buckets: {'Small': 131, 'Mid': 81, 'Large': 58, 'Micro': 28}  *(Large ≥₹20k cr, Mid ≥₹5k cr, Small ≥₹500 cr, Micro <₹500 cr)*
- Penny stocks (price < ₹10): **0 flagged, none removed** (per spec)
- Cross-source current-price check: 298/309 have a 2nd exchange source; **295/298 agree within 5%** (median mismatch **0.10%**)
- Excluded categories (suspended / Z / XT / XC) removed at universe stage
- Sorted by Return% descending ✓

### ⚠ Price-discrepancy flags (NSE-vs-BSE > 5% — review before trading; all still >25%)
- `UNIVPHOTO` Universus Photo Imagings Limited (NSE): Yahoo ₹365.20 vs other-exchange ₹457.70 (20.2%)
- `540252` Viram Suvarn Ltd (BSE): Yahoo ₹11.05 vs other-exchange ₹10.29 (7.4%)
- `535916` Alacrity Securities Ltd (BSE): Yahoo ₹73.11 vs other-exchange ₹67.87 (7.7%)

## OUTPUT — full ranked list
Columns: Symbol | Company | Exch | Price 180d ago | Price today | Return% | MktCap(₹cr) | Cap | Sector | AvgVol(sh) | AvgVal(₹)

| # | Symbol | Company | Exch | 180d Ago | Today | Return% | MktCap₹cr | Cap | Sector | AvgVol | AvgVal₹ |
|--:|---|---|---|--:|--:|--:|--:|---|---|--:|--:|
| 1 | STLTECH | Sterlite Technologies Limited | NSE | 100.61 | 613.00 | **529.0** | 29,932 | Large | Technology | 5,305,658 | 1,119,926,309 |
| 2 | 540492 | Starlineps Enterprises Ltd | BSE | 3.24 | 11.44 | **250.9** | 401 | Micro | nan | 1,523,943 | 9,679,695 |
| 3 | SANGINITA | Sanginita Chemicals Limited | NSE | 9.71 | 32.84 | **233.1** | n/a | nan | Basic Materials | 170,586 | 2,896,618 |
| 4 | MTARTECH | Mtar Technologies Limited | NSE | 2345.50 | 7458.00 | **218.0** | 22,930 | Large | Industrials | 773,462 | 3,886,267,392 |
| 5 | DEEDEV | DEE Development Engineers Limited | NSE | 217.51 | 688.70 | **215.7** | 4,777 | Small | Industrials | 2,192,412 | 643,197,960 |
| 6 | UFBL | United Foodbrands Limited | NSE | 182.28 | 549.95 | **201.7** | 2,144 | Small | Consumer Cyclical | 242,685 | 84,894,894 |
| 7 | BLISSGVS | Bliss GVS Pharma Limited | NSE | 144.37 | 421.60 | **192.0** | 4,449 | Small | Healthcare | 3,531,370 | 757,050,571 |
| 8 | GVPIL | GE Power India Limited | NSE | 312.55 | 905.50 | **188.3** | 6,093 | Mid | Industrials | 647,189 | 322,410,193 |
| 9 | HFCL | HFCL Limited | NSE | 66.56 | 178.01 | **169.6** | 27,268 | Large | Technology | 33,985,147 | 3,659,900,391 |
| 10 | OMNI | Omnitech Engineering Limited | NSE | 204.93 | 494.45 | **159.4** | 6,112 | Mid | Industrials | 1,106,033 | 356,427,988 |
| 11 | AEROFLEX | Aeroflex Industries Limited | NSE | 176.13 | 425.70 | **141.7** | 5,630 | Mid | Industrials | 2,395,112 | 653,290,657 |
| 12 | SIGMAADV | SIGMA ADVANCED SYSTEMS LIMITED | NSE | 183.74 | 437.45 | **140.7** | 7,677 | Mid | Industrials | 257,082 | 67,022,169 |
| 13 | KSHINTL | KSH International Limited | NSE | 355.00 | 819.90 | **138.8** | 5,560 | Mid | Industrials | 474,555 | 249,177,871 |
| 14 | MODISONLTD | MODISON LIMITED | NSE | 140.65 | 327.40 | **135.0** | 1,061 | Small | Industrials | 110,027 | 22,847,735 |
| 15 | BHAGYANGR | Bhagyanagar India Limited | NSE | 132.62 | 307.80 | **132.1** | 981 | Small | Basic Materials | 314,108 | 56,825,046 |
| 16 | BAJAJCON | Bajaj Consumer Care Limited | NSE | 254.05 | 582.20 | **127.7** | 7,611 | Mid | Consumer Defensive | 1,352,824 | 507,549,931 |
| 17 | IDEAFORGE | Ideaforge Technology Limited | NSE | 425.40 | 964.90 | **127.4** | 4,181 | Small | Technology | 1,095,475 | 630,512,514 |
| 18 | CPPLUS | Aditya Infotech Limited | NSE | 1554.90 | 3482.20 | **126.8** | 41,127 | Large | Industrials | 293,278 | 595,179,359 |
| 19 | KOVAI | Kovai Medical Center & Hospital Limited | NSE | 2576.65 | 5746.00 | **123.0** | 6,290 | Mid | Healthcare | 3,925 | 21,682,956 |
| 20 | CONFIPET | Confidence Petroleum India Limited | NSE | 34.04 | 75.50 | **121.8** | 2,515 | Small | Energy | 2,406,054 | 124,398,308 |
| 21 | OMAXAUTO | Omax Autos Limited | NSE | 99.29 | 216.79 | **119.9** | 463 | Micro | Consumer Cyclical | 141,742 | 21,650,372 |
| 22 | ANTELOPUS | Antelopus Selan Energy Limited | NSE | 396.65 | 853.85 | **115.3** | 2,998 | Small | Energy | 396,180 | 219,928,454 |
| 23 | NGLFINE | NGL Fine-Chem Limited | NSE | 1326.70 | 2820.70 | **112.6** | 1,740 | Small | Healthcare | 8,346 | 19,405,829 |
| 24 | JNKINDIA | JNK India Limited | NSE | 234.65 | 484.05 | **110.6** | 2,713 | Small | Industrials | 519,367 | 176,682,526 |
| 25 | ATLANTAELE | Atlanta Electricals Limited | NSE | 925.05 | 1890.70 | **109.8** | 14,497 | Mid | Industrials | 188,391 | 224,311,358 |
| 26 | 532380 | Baba Arts Ltd-$ | BSE | 6.54 | 13.50 | **106.4** | 70 | Micro | nan | 57,679 | 723,732 |
| 27 | SHADOWFAX | Shadowfax Technologies Limited | NSE | 109.98 | 216.90 | **103.4** | 12,698 | Mid | Industrials | 3,033,565 | 446,553,923 |
| 28 | VENUSREM | Venus Remedies Limited | NSE | 825.40 | 1610.70 | **102.4** | 2,142 | Small | Healthcare | 75,494 | 66,645,111 |
| 29 | SPORTKING | Sportking India Limited | NSE | 89.75 | 177.84 | **100.3** | 2,257 | Small | Consumer Cyclical | 297,872 | 41,490,042 |
| 30 | BALAMINES | Balaji Amines Limited | NSE | 1120.60 | 2242.10 | **99.1** | 7,266 | Mid | Basic Materials | 376,815 | 533,876,683 |
| 31 | NOVARTIND | Novartis India Limited | NSE | 672.25 | 1331.40 | **98.0** | 3,288 | Small | Healthcare | 32,616 | 41,611,485 |
| 32 | E2E | E2E Networks Limited | NSE | 210.48 | 408.80 | **94.4** | n/a | nan | Technology | 1,382,101 | 389,734,917 |
| 33 | SAKAR | Sakar Healthcare Limited | NSE | 422.35 | 813.60 | **93.8** | n/a | nan | Healthcare | 109,594 | 64,887,931 |
| 34 | ACUTAAS | Acutaas Chemicals Limited | NSE | 1664.00 | 3198.70 | **92.2** | 26,189 | Large | Basic Materials | 422,630 | 940,445,080 |
| 35 | SASKEN | Sasken Technologies Limited | NSE | 1228.70 | 2314.40 | **91.1** | 3,545 | Small | Technology | 108,060 | 184,220,017 |
| 36 | RAIN | Rain Industries Limited | NSE | 106.86 | 203.97 | **90.9** | 6,855 | Mid | Basic Materials | 4,673,039 | 695,649,943 |
| 37 | AVALON | Avalon Technologies Limited | NSE | 870.75 | 1639.50 | **89.6** | 10,963 | Mid | Technology | 314,189 | 367,693,530 |
| 38 | COCKERILL | John Cockerill India Limited | NSE | 5277.35 | 9883.50 | **89.6** | 4,869 | Small | Industrials | 25,526 | 208,201,776 |
| 39 | PARKHOSPS | Park Medi World Limited | NSE | 147.95 | 292.50 | **88.8** | 12,628 | Mid | Healthcare | 1,510,623 | 273,933,746 |
| 40 | BBOX | Black Box Limited | NSE | 516.55 | 970.10 | **87.9** | 17,194 | Mid | Technology | 674,959 | 462,278,012 |
| 41 | TCIFINANCE | TCI Finance Limited | NSE | 11.33 | 20.91 | **87.4** | 27 | Micro | Financial Services | 65,820 | 1,222,319 |
| 42 | KERNEX | Kernex Microsystems (India) Limited | NSE | 1026.40 | 1889.90 | **86.6** | 3,171 | Small | Technology | 259,037 | 343,724,925 |
| 43 | SGMART | SG Mart Limited | NSE | 334.15 | 619.40 | **85.4** | 7,383 | Mid | Industrials | 314,605 | 141,393,027 |
| 44 | GAYAPROJ | Gayatri Projects Limited | NSE | 11.53 | 21.33 | **85.0** | 398 | Micro | Industrials | 206,874 | 3,773,090 |
| 45 | CUPID | Cupid Limited | NSE | 78.80 | 145.86 | **84.9** | 19,612 | Mid | Consumer Defensive | 29,943,039 | 2,584,916,833 |
| 46 | RUBICON | Rubicon Research Limited | NSE | 636.35 | 1170.50 | **83.9** | 19,310 | Mid | Healthcare | 392,846 | 343,470,605 |
| 47 | KSR | KSR Footwear Limited | NSE | 17.33 | 32.63 | **83.4** | 62 | Micro | Consumer Cyclical | 100,712 | 2,536,651 |
| 48 | VIDYAWIRES | Vidya Wires Limited | NSE | 51.59 | 94.00 | **82.2** | 1,999 | Small | Industrials | 6,089,879 | 427,242,647 |
| 49 | PARACABLES | Paramount Communications Limited | NSE | 36.95 | 66.75 | **81.7** | 2,035 | Small | Technology | 1,832,394 | 92,780,415 |
| 50 | SEDEMAC | SEDEMAC Mechatronics Limited | NSE | 1451.10 | 2624.90 | **80.9** | 11,596 | Mid | Consumer Cyclical | 261,956 | 466,127,207 |
| 51 | TDPOWERSYS | TD Power Systems Limited | NSE | 687.10 | 1231.00 | **79.2** | 19,228 | Mid | Industrials | 1,292,061 | 1,188,514,555 |
| 52 | POWERINDIA | Hitachi Energy India Limited | NSE | 19535.00 | 34610.00 | **79.1** | 154,218 | Large | Industrials | 163,196 | 3,991,969,128 |
| 53 | WHEELS | Wheels India Limited | NSE | 842.10 | 1507.60 | **79.0** | 3,687 | Small | Consumer Cyclical | 116,374 | 140,490,059 |
| 54 | DJML | DJ Mediaprint & Logistics Limited | NSE | 59.96 | 107.25 | **78.9** | 369 | Micro | Industrials | 157,300 | 13,037,098 |
| 55 | APOLLO | Apollo Micro Systems Limited | NSE | 236.00 | 413.05 | **78.7** | 14,762 | Mid | Industrials | 9,816,948 | 3,144,690,351 |
| 56 | NARMADA | Narmada Agrobase Limited | NSE | 20.52 | 37.77 | **78.0** | 144 | Micro | Basic Materials | 218,567 | 7,135,314 |
| 57 | NEOGEN | Neogen Chemicals Limited | NSE | 1089.70 | 1938.80 | **77.9** | 5,302 | Mid | Basic Materials | 176,887 | 223,355,600 |
| 58 | WELCORP | Welspun Corp Limited | NSE | 793.30 | 1411.60 | **77.4** | 37,274 | Large | Basic Materials | 768,598 | 763,952,212 |
| 59 | NINSYS | NINtec Systems Limited | NSE | 409.15 | 718.90 | **76.5** | 1,340 | Small | Technology | 13,387 | 5,424,869 |
| 60 | SANSERA | Sansera Engineering Limited | NSE | 1699.20 | 2961.40 | **76.2** | 18,437 | Mid | Consumer Cyclical | 225,265 | 499,332,413 |
| 61 | DATAPATTNS | Data Patterns (India) Limited | NSE | 2594.20 | 4558.50 | **75.7** | 25,497 | Large | Industrials | 905,828 | 3,051,690,814 |
| 62 | PRECWIRE | Precision Wires India Limited | NSE | 235.90 | 410.85 | **74.2** | 7,502 | Mid | Industrials | 1,217,156 | 359,318,808 |
| 63 | SHILPAMED | Shilpa Medicare Limited | NSE | 331.15 | 569.15 | **73.8** | 11,089 | Mid | Healthcare | 610,207 | 246,532,873 |
| 64 | EMMVEE | Emmvee Photovoltaic Power Limited | NSE | 193.72 | 335.20 | **73.0** | 23,214 | Large | Technology | 4,386,624 | 1,060,980,057 |
| 65 | PANACEABIO | Panacea Biotec Limited | NSE | 363.25 | 607.75 | **73.0** | 3,727 | Small | Healthcare | 720,624 | 323,604,282 |
| 66 | NITINSPIN | Nitin Spinners Limited | NSE | 317.65 | 539.00 | **71.8** | 3,026 | Small | Consumer Cyclical | 371,465 | 146,089,020 |
| 67 | SYRMA | Syrma SGS Technology Limited | NSE | 738.80 | 1256.80 | **71.3** | 24,204 | Large | Technology | 1,611,107 | 1,400,900,884 |
| 68 | GRWRHITECH | Garware Hi-Tech Films Limited | NSE | 3689.60 | 6225.00 | **71.2** | 14,438 | Mid | Basic Materials | 92,898 | 393,813,395 |
| 69 | KRISHNADEF | Krishna Defence And Allied Industries Limited | NSE | 745.00 | 1240.80 | **71.1** | n/a | nan | Industrials | 125,560 | 127,919,282 |
| 70 | 543787 | Macfos Ltd | BSE | 727.86 | 1231.35 | **70.8** | 1,301 | Small | nan | 10,014 | 8,755,020 |
| 71 | THANGAMAYL | Thangamayil Jewellery Limited | NSE | 3196.60 | 5469.50 | **70.3** | 17,030 | Mid | Consumer Cyclical | 184,668 | 685,063,456 |
| 72 | SATIN | Satin Creditcare Network Limited | NSE | 143.49 | 242.10 | **69.7** | 2,678 | Small | Financial Services | 494,353 | 100,003,781 |
| 73 | INDSWFTLAB | Ind-Swift Laboratories Limited | NSE | 97.91 | 161.87 | **69.0** | 1,403 | Small | Healthcare | 736,273 | 101,538,210 |
| 74 | SALSTEEL | S.A.L. Steel Limited | NSE | 35.30 | 59.52 | **68.6** | 658 | Small | Basic Materials | 137,236 | 6,409,254 |
| 75 | ADVAIT | Advait Energy Transitions Limited | NSE | 1391.80 | 2346.20 | **68.0** | 2,570 | Small | Industrials | 59,953 | 112,661,972 |
| 76 | APOLLOPIPE | Apollo Pipes Limited | NSE | 300.30 | 501.75 | **67.1** | 2,212 | Small | Industrials | 948,277 | 384,199,968 |
| 77 | SWANDEF | Swan Defence and Heavy Industries Limited | NSE | 1199.30 | 1996.80 | **66.5** | 10,505 | Mid | Industrials | 12,343 | 22,642,049 |
| 78 | MANAKALUCO | Manaksia Aluminium Company Limited | NSE | 24.29 | 40.12 | **66.1** | 265 | Micro | Basic Materials | 291,480 | 12,425,705 |
| 79 | THERMAX | Thermax Limited | NSE | 2870.40 | 4739.90 | **65.1** | 56,509 | Large | Industrials | 195,533 | 747,651,858 |
| 80 | 542669 | BMW Industries Ltd | BSE | 36.96 | 61.19 | **65.0** | 1,425 | Small | nan | 246,726 | 11,537,513 |
| 81 | MAYURUNIQ | Mayur Uniquoters Ltd | NSE | 487.25 | 798.85 | **64.0** | 3,468 | Small | Consumer Cyclical | 139,913 | 88,968,152 |
| 82 | GVT&D | GE Vernova T&D India Limited | NSE | 3050.90 | 4931.00 | **63.7** | 126,217 | Large | Industrials | 842,384 | 3,002,547,048 |
| 83 | FCL | Fineotex Chemical Limited | NSE | 24.44 | 39.86 | **63.1** | 4,648 | Small | Basic Materials | 9,728,144 | 314,629,248 |
| 84 | KIRLOSENG | Kirloskar Oil Engines Limited | NSE | 1144.60 | 1851.30 | **63.0** | 26,918 | Large | Industrials | 608,627 | 801,028,768 |
| 85 | SBCL | Shivalik Bimetal Controls Limited | NSE | 451.60 | 731.30 | **62.8** | 4,208 | Small | Industrials | 262,994 | 151,615,008 |
| 86 | JAYBARMARU | Jay Bharat Maruti Limited | NSE | 88.51 | 138.82 | **62.6** | 1,506 | Small | Consumer Cyclical | 662,352 | 73,191,180 |
| 87 | QPOWER | Quality Power Electrical Equipments Limited | NSE | 701.60 | 1133.70 | **62.6** | 8,834 | Mid | Industrials | 933,423 | 861,081,432 |
| 88 | INDOTECH | Indo Tech Transformers Limited | NSE | 1598.30 | 2595.50 | **62.4** | 2,757 | Small | Industrials | 47,276 | 92,366,318 |
| 89 | YASHO | Yasho Industries Limited | NSE | 1574.40 | 2543.60 | **61.6** | 3,068 | Small | Basic Materials | 26,175 | 41,917,796 |
| 90 | KRN | KRN Heat Exchanger and Refrigeration Limited | NSE | 775.25 | 1232.00 | **61.5** | 8,031 | Mid | Technology | 893,329 | 863,079,768 |
| 91 | ASTRAMICRO | Astra Microwave Products Limited | NSE | 907.05 | 1457.70 | **61.2** | 13,851 | Mid | Technology | 481,811 | 549,889,677 |
| 92 | IOLCP | IOL Chemicals and Pharmaceuticals Limited | NSE | 83.08 | 132.84 | **61.1** | 3,901 | Small | Healthcare | 2,018,025 | 204,515,823 |
| 93 | RPTECH | Rashi Peripherals Limited | NSE | 344.75 | 552.65 | **60.3** | 3,681 | Small | Technology | 165,481 | 68,796,902 |
| 94 | IFCI | IFCI Limited | NSE | 48.70 | 77.07 | **60.1** | 20,754 | Large | Financial Services | 28,064,841 | 1,763,758,263 |
| 95 | LOKESHMACH | Lokesh Machines Limited | NSE | 173.61 | 265.15 | **59.8** | 524 | Small | Industrials | 82,809 | 16,371,006 |
| 96 | ATHERENERG | Ather Energy Limited | NSE | 645.10 | 1032.80 | **59.8** | 39,590 | Large | Consumer Cyclical | 3,516,458 | 2,790,173,615 |
| 97 | MENONBE | Menon Bearings Limited | NSE | 106.03 | 169.81 | **59.7** | 953 | Small | Consumer Cyclical | 93,723 | 12,961,569 |
| 98 | PAISALO | Paisalo Digital Limited | NSE | 37.81 | 60.18 | **59.5** | 5,478 | Mid | Financial Services | 7,634,073 | 323,347,021 |
| 99 | NITTAGELA | Nitta Gelatin India Limited | NSE | 922.65 | 1471.00 | **59.0** | 1,341 | Small | Basic Materials | 20,623 | 29,575,759 |
| 100 | HONASA | Honasa Consumer Limited | NSE | 261.45 | 407.95 | **58.6** | 13,291 | Mid | Consumer Defensive | 1,684,503 | 558,639,819 |
| 101 | RUBYMILLS | The Ruby Mills Limited | NSE | 217.57 | 344.70 | **58.4** | 1,157 | Small | Consumer Cyclical | 60,260 | 15,250,951 |
| 102 | CEIGALL | Ceigall India Limited | NSE | 234.71 | 366.40 | **58.3** | 6,376 | Mid | Industrials | 401,748 | 123,192,542 |
| 103 | SKYGOLD | SKY GOLD AND DIAMONDS LIMITED | NSE | 323.05 | 513.05 | **58.2** | 7,948 | Mid | Consumer Cyclical | 1,081,275 | 435,421,964 |
| 104 | ONELIFECAP | Onelife Capital Advisors Limited | NSE | 16.94 | 26.49 | **58.0** | 101 | Micro | Financial Services | 144,177 | 2,378,887 |
| 105 | ADANIENSOL | Adani Energy Solutions Limited | NSE | 1011.30 | 1579.20 | **58.0** | 189,568 | Large | Utilities | 2,206,410 | 2,588,339,942 |
| 106 | APEX | Apex Frozen Foods Limited | NSE | 266.40 | 409.80 | **57.9** | 1,280 | Small | Consumer Defensive | 1,322,632 | 491,456,232 |
| 107 | KIRLPNU | Kirloskar Pneumatic Company Limited | NSE | 1042.40 | 1645.00 | **57.8** | 10,687 | Mid | Industrials | 119,284 | 154,306,769 |
| 108 | GULPOLY | Gulshan Polyols Limited | NSE | 136.11 | 214.95 | **57.8** | 1,344 | Small | Basic Materials | 259,894 | 45,906,667 |
| 109 | SEAMECLTD | Seamec Limited | NSE | 1027.20 | 1612.80 | **57.5** | 4,101 | Small | Industrials | 80,256 | 105,237,900 |
| 110 | PARAS | Paras Defence and Space Technologies Limited | NSE | 667.45 | 1039.15 | **57.5** | 8,376 | Mid | Industrials | 1,558,359 | 1,198,948,732 |
| 111 | 526775 | Valiant Communications Ltd-$ | BSE | 801.05 | 1259.25 | **57.2** | 1,423 | Small | nan | 14,458 | 13,677,098 |
| 112 | MIRCELECTR | MIRC Electronics Limited | NSE | 24.88 | 38.09 | **57.1** | 1,404 | Small | Consumer Cyclical | 1,579,787 | 55,970,438 |
| 113 | SCPL | Sheetal Cool Products Limited | NSE | 283.83 | 445.55 | **57.0** | 475 | Micro | Consumer Defensive | 23,099 | 7,109,383 |
| 114 | KOTYARK | Kotyark Industries Limited | NSE | 263.15 | 407.20 | **56.6** | 417 | Micro | Basic Materials | 29,089 | 10,812,376 |
| 115 | ADANIPOWER | Adani Power Limited | NSE | 144.49 | 226.14 | **56.6** | 435,931 | Large | Utilities | 30,782,016 | 5,558,356,583 |
| 116 | CMPDI | Central Mine Planning & Design Institute Limited | NSE | 154.06 | 244.18 | **56.5** | 17,429 | Mid | Basic Materials | 5,676,634 | 1,205,963,080 |
| 117 | SGFIN | SG Finserve Limited | NSE | 384.95 | 606.15 | **56.4** | 3,387 | Small | Financial Services | 261,667 | 122,306,862 |
| 118 | J&KBANK | The Jammu & Kashmir Bank Limited | NSE | 102.53 | 156.98 | **55.9** | 17,272 | Mid | Financial Services | 4,535,057 | 541,555,672 |
| 119 | ROSSTECH | Rossell Techsys Limited | NSE | 673.70 | 1050.30 | **55.7** | 3,959 | Small | Industrials | 196,054 | 151,994,880 |
| 120 | ARVIND | Arvind Limited | NSE | 318.15 | 500.10 | **55.3** | 13,104 | Mid | Consumer Cyclical | 661,617 | 257,330,567 |
| 121 | ELPROINTL | Elpro International Limited | NSE | 105.35 | 166.77 | **55.1** | 2,829 | Small | nan | 238,088 | 35,076,970 |
| 122 | SUVEN | Suven Life Sciences Limited | NSE | 170.79 | 264.45 | **54.8** | 6,983 | Mid | Healthcare | 714,158 | 158,379,828 |
| 123 | NRBBEARING | NRB Bearing Limited | NSE | 284.65 | 438.95 | **54.2** | 4,254 | Small | Consumer Cyclical | 492,485 | 169,296,420 |
| 124 | ZIMLAB | Zim Laboratories Limited | NSE | 73.35 | 113.05 | **54.1** | 582 | Small | Healthcare | 123,835 | 9,705,157 |
| 125 | SOTL | Savita Oil Technologies Limited | NSE | 372.75 | 568.05 | **53.9** | 3,896 | Small | Basic Materials | 171,828 | 86,571,480 |
| 126 | TMB | Tamilnad Mercantile Bank Limited | NSE | 507.10 | 780.55 | **53.7** | 12,366 | Mid | Financial Services | 377,226 | 241,070,654 |
| 127 | NEPHROPLUS | Nephrocare Health Services Limited | NSE | 471.25 | 709.25 | **53.6** | 7,084 | Mid | Healthcare | 383,256 | 197,959,204 |
| 128 | SCHNEIDER | Schneider Electric Infrastructure Limited | NSE | 717.40 | 1097.80 | **53.6** | 26,263 | Large | Industrials | 340,807 | 298,315,486 |
| 129 | UTLSOLAR | Fujiyama Power Systems Limited | NSE | 204.78 | 314.25 | **53.5** | 9,649 | Mid | Technology | 731,640 | 172,389,931 |
| 130 | 521113 | Suditi Industries Ltd | BSE | 60.77 | 90.55 | **53.2** | 428 | Micro | nan | 70,877 | 5,263,206 |
| 131 | RRKABEL | R R Kabel Limited | NSE | 1424.00 | 2177.00 | **52.9** | 24,625 | Large | Industrials | 405,813 | 665,956,837 |
| 132 | SPARC | Sun Pharma Advanced Research Company Limited | NSE | 136.84 | 209.19 | **52.9** | 6,792 | Mid | Healthcare | 4,334,402 | 737,799,095 |
| 133 | ACMESOLAR | Acme Solar Holdings Limited | NSE | 228.32 | 348.70 | **52.7** | 24,634 | Large | Utilities | 1,551,580 | 424,904,801 |
| 134 | WALCHANNAG | Walchandnagar Industries Limited | NSE | 175.53 | 254.70 | **52.7** | 1,726 | Small | Industrials | 1,773,947 | 356,756,038 |
| 135 | WELSPLSOL | Welspun Specialty Solutions Limited | NSE | 38.05 | 59.25 | **52.5** | 3,938 | Small | nan | 1,445,411 | 71,944,092 |
| 136 | BIRLACABLE | Birla Cable Limited | NSE | 133.68 | 203.70 | **52.2** | 610 | Small | Technology | 73,100 | 11,674,980 |
| 137 | UNIVPHOTO | Universus Photo Imagings Limited | NSE | 240.25 | 365.20 | **51.7** | 501 | Small | Healthcare | 16,334 | 6,850,121 |
| 138 | APARINDS | Apar Industries Limited | NSE | 9023.50 | 13609.00 | **51.4** | 54,642 | Large | Industrials | 109,979 | 1,132,023,619 |
| 139 | HIRECT | Hind Rectifiers Limited | NSE | 742.05 | 1098.20 | **51.0** | 3,776 | Small | Industrials | 140,042 | 120,037,629 |
| 140 | BSE | BSE Limited | NSE | 2735.00 | 3996.30 | **50.9** | n/a | nan | Financial Services | 4,511,325 | 13,729,926,645 |
| 141 | MIDHANI | Mishra Dhatu Nigam Limited | NSE | 300.55 | 450.35 | **50.8** | 8,432 | Mid | Basic Materials | 1,233,098 | 451,520,414 |
| 142 | VINDHYATEL | Vindhya Telelinks Limited | NSE | 1417.10 | 2134.70 | **50.5** | 2,528 | Small | Industrials | 50,285 | 83,087,723 |
| 143 | 524520 | KMC Speciality Hospitals (India) Ltd | BSE | 75.25 | 112.55 | **49.6** | 1,856 | Small | nan | 109,638 | 9,845,386 |
| 144 | ADANIGREEN | Adani Green Energy Limited | NSE | 1040.20 | 1534.50 | **49.2** | 252,800 | Large | Utilities | 3,762,336 | 4,071,763,749 |
| 145 | AXISCADES | AXISCADES Technologies Limited | NSE | 1297.90 | 1935.50 | **49.1** | 8,236 | Mid | Industrials | 123,122 | 196,370,456 |
| 146 | JINDALSAW | Jindal Saw Limited | NSE | 161.20 | 239.81 | **48.8** | 15,335 | Mid | Basic Materials | 5,421,714 | 1,054,618,839 |
| 147 | SOLARINDS | Solar Industries India Limited | NSE | 12304.00 | 18267.00 | **48.5** | 165,181 | Large | Basic Materials | 156,700 | 2,259,085,720 |
| 148 | INOXINDIA | INOX India Limited | NSE | 1141.00 | 1686.70 | **47.8** | 15,299 | Mid | Industrials | 147,291 | 201,820,585 |
| 149 | OCCLLTD | OCCL Limited | NSE | 94.98 | 139.92 | **47.3** | 697 | Small | Basic Materials | 144,006 | 16,401,018 |
| 150 | MAHABANK | Bank of Maharashtra | NSE | 57.03 | 83.97 | **47.2** | 64,617 | Large | Financial Services | 21,474,920 | 1,451,806,772 |
| 151 | BELRISE | Belrise Industries Limited | NSE | 159.90 | 234.73 | **47.0** | 20,881 | Large | Consumer Cyclical | 6,551,946 | 1,191,875,816 |
| 152 | CENTUM | Centum Electronics Limited | NSE | 2302.80 | 3355.20 | **46.7** | 4,957 | Small | Technology | 69,313 | 189,318,911 |
| 153 | STEELXIND | STEEL EXCHANGE INDIA LIMITED | NSE | 8.17 | 11.96 | **46.4** | 1,488 | Small | Basic Materials | 2,174,810 | 21,777,285 |
| 154 | CEMPRO | Cemindia Projects Limited | NSE | 830.45 | 1203.80 | **46.1** | 20,678 | Large | Industrials | 750,330 | 635,381,486 |
| 155 | HSCL | Himadri Speciality Chemical Limited | NSE | 465.55 | 679.50 | **46.0** | 34,271 | Large | Basic Materials | 4,224,523 | 2,382,126,728 |
| 156 | HARDWYN | Hardwyn India Limited | NSE | 17.90 | 24.73 | **45.8** | 1,210 | Small | Industrials | 2,536,133 | 53,116,965 |
| 157 | NDLVENTURE | NDL Ventures Limited | NSE | 89.93 | 130.03 | **45.0** | 438 | Micro | Communication Services | 43,885 | 5,067,387 |
| 158 | APCOTEXIND | Apcotex Industries Limited | NSE | 371.60 | 539.00 | **44.9** | 2,796 | Small | Basic Materials | 55,650 | 25,378,925 |
| 159 | DIACABS | Diamond Power Infrastructure Limited | NSE | 140.68 | 202.47 | **44.8** | 10,674 | Mid | Industrials | 2,586,821 | 429,240,590 |
| 160 | PREMEXPLN | Premier Explosives Limited | NSE | 502.30 | 721.95 | **44.6** | 3,889 | Small | Basic Materials | 525,454 | 314,115,796 |
| 161 | SPECTRUM | Spectrum Electrical Industries Limited | NSE | 1214.20 | 1683.30 | **44.4** | 2,660 | Small | Industrials | 11,362 | 16,223,250 |
| 162 | AFIL | Akme Fintrade (India) Limited | NSE | 7.07 | 10.01 | **44.0** | 427 | Micro | Financial Services | 1,637,892 | 12,438,444 |
| 163 | MCLEODRUSS | Mcleod Russel India Limited | NSE | 48.67 | 68.11 | **43.9** | 710 | Small | Consumer Defensive | 492,539 | 24,752,427 |
| 164 | CLEANMAX | Clean Max Enviro Energy Solutions Limited | NSE | 867.50 | 1232.40 | **43.7** | 14,452 | Mid | Utilities | 403,505 | 391,273,747 |
| 165 | SAIL | Steel Authority of India Limited | NSE | 131.90 | 185.99 | **43.4** | 76,778 | Large | Basic Materials | 24,220,377 | 3,889,499,268 |
| 166 | EBGNG | GNG Electronics Limited | NSE | 279.05 | 411.10 | **42.7** | 4,682 | Small | Technology | 300,665 | 113,313,673 |
| 167 | KPL | Kwality Pharmaceuticals Limited | NSE | 1662.60 | 2338.60 | **42.4** | 2,424 | Small | nan | 43,051 | 87,004,356 |
| 168 | BHEL | Bharat Heavy Electricals Limited | NSE | 285.15 | 396.55 | **42.0** | 138,012 | Large | Industrials | 14,551,635 | 4,405,006,130 |
| 169 | ABSLAMC | Aditya Birla Sun Life AMC Limited | NSE | 751.95 | 1062.40 | **41.9** | 30,731 | Large | Financial Services | 410,833 | 377,524,593 |
| 170 | KOPRAN | Kopran Limited | NSE | 130.85 | 183.65 | **40.9** | 886 | Small | Healthcare | 516,895 | 83,018,713 |
| 171 | RSWM | RSWM Limited | NSE | 153.62 | 213.40 | **40.8** | 1,003 | Small | Consumer Cyclical | 83,918 | 14,690,099 |
| 172 | BUILDPRO | Shankara Buildpro Limited | NSE | 812.55 | 1086.70 | **40.8** | 2,635 | Small | Consumer Cyclical | 77,120 | 76,682,472 |
| 173 | WOCKPHARMA | Wockhardt Limited | NSE | 1341.20 | 1887.60 | **40.8** | 30,662 | Large | Healthcare | 1,472,027 | 2,356,435,066 |
| 174 | LAURUSLABS | Laurus Labs Limited | NSE | 1012.30 | 1424.40 | **40.7** | 76,900 | Large | Healthcare | 1,894,795 | 2,046,589,417 |
| 175 | HINDCOPPER | Hindustan Copper Limited | NSE | 382.30 | 519.60 | **40.7** | 50,295 | Large | Basic Materials | 19,795,587 | 10,397,232,030 |
| 176 | STYLAMIND | Stylam Industries Limited | NSE | 2227.60 | 3103.50 | **40.6** | 5,245 | Mid | Consumer Cyclical | 65,532 | 148,162,841 |
| 177 | AGIIL | Agi Infra Limited | NSE | 263.95 | 373.30 | **40.5** | 4,678 | Small | Real Estate | 1,870,075 | 609,373,225 |
| 178 | PASUPTAC | Pasupati Acrylon Limited | NSE | 52.25 | 73.37 | **40.4** | 654 | Small | Consumer Cyclical | 302,952 | 17,864,483 |
| 179 | HALDYNGL | Haldyn Glass Limited | NSE | 89.05 | 123.89 | **40.3** | 665 | Small | nan | 130,164 | 14,587,738 |
| 180 | NIBE | NIBE Limited | NSE | 1099.50 | 1541.30 | **40.2** | 2,301 | Small | Industrials | 110,306 | 137,348,879 |
| 181 | MWL | Mangalam Worldwide Limited | NSE | 269.76 | 377.50 | **39.9** | 1,112 | Small | Basic Materials | 80,403 | 23,211,930 |
| 182 | AZAD | Azad Engineering Limited | NSE | 1607.90 | 2230.00 | **39.5** | 14,456 | Mid | Industrials | 277,759 | 512,684,179 |
| 183 | FINCABLES | Finolex Cables Limited | NSE | 740.15 | 1032.10 | **39.4** | 15,789 | Mid | Industrials | 445,249 | 408,259,579 |
| 184 | SENORES | Senores Pharmaceuticals Limited | NSE | 786.10 | 1094.50 | **39.2** | 5,037 | Mid | Healthcare | 323,636 | 286,996,406 |
| 185 | VTL | Vardhman Textiles Limited | NSE | 446.30 | 620.85 | **39.1** | 17,956 | Mid | Consumer Cyclical | 596,350 | 301,885,394 |
| 186 | 543828 | Sudarshan Pharma Industries Ltd | BSE | 24.12 | 34.40 | **39.0** | 842 | Small | nan | 222,640 | 5,811,638 |
| 187 | MCX | Multi Commodity Exchange of India Limited | NSE | 2032.40 | 2824.80 | **39.0** | 72,028 | Large | Financial Services | 3,316,547 | 8,245,339,251 |
| 188 | GANESHBE | Ganesh Benzoplast Limited | NSE | 79.23 | 110.61 | **38.8** | 796 | Small | Basic Materials | 237,040 | 22,326,490 |
| 189 | SHREEJISPG | Shreeji Shipping Global Limited | NSE | 332.05 | 461.90 | **38.8** | 7,541 | Mid | Industrials | 1,151,787 | 417,291,854 |
| 190 | DECNGOLD | Deccan Gold Mines Limited | NSE | 120.20 | 166.75 | **38.7** | 3,317 | Small | nan | 1,808,022 | 275,139,716 |
| 191 | NATIONALUM | National Aluminium Company Limited | NSE | 278.15 | 383.90 | **38.7** | 70,527 | Large | Basic Materials | 14,093,920 | 4,979,097,564 |
| 192 | SUNFLAG | Sunflag Iron And Steel Company Limited | NSE | 251.85 | 357.10 | **38.6** | 6,434 | Mid | Basic Materials | 431,598 | 145,213,033 |
| 193 | BANDHANBNK | Bandhan Bank Limited | NSE | 149.57 | 206.94 | **38.4** | 33,380 | Large | Financial Services | 10,626,912 | 1,811,500,158 |
| 194 | 544141 | Pune E - Stock Broking Ltd | BSE | 205.65 | 283.90 | **38.4** | 441 | Micro | nan | 26,065 | 6,027,014 |
| 195 | 539730 | Fredun Pharmaceuticals Ltd | BSE | 1581.35 | 2297.80 | **38.4** | 1,265 | Small | nan | 12,193 | 22,681,445 |
| 196 | NETWEB | Netweb Technologies India Limited | NSE | 3200.80 | 4428.20 | **38.4** | 25,212 | Large | Technology | 1,772,253 | 6,505,479,351 |
| 197 | DBOL | Dhampur Bio Organics Limited | NSE | 79.88 | 109.72 | **38.1** | 737 | Small | Consumer Defensive | 181,413 | 18,667,897 |
| 198 | LLOYDSENGG | LLOYDS ENGINEERING WORKS LIMITED | NSE | 52.09 | 71.78 | **37.8** | 10,530 | Mid | Industrials | 5,752,057 | 327,592,768 |
| 199 | SAIPARENT | Sai Parenterals Limited | NSE | 405.70 | 560.05 | **37.7** | 2,478 | Small | Healthcare | 320,387 | 153,061,494 |
| 200 | 544191 | Purple Finance Ltd | BSE | 47.34 | 65.19 | **37.7** | 394 | Micro | nan | 85,681 | 4,869,800 |
| 201 | STEELCAS | Steelcast Limited | NSE | 211.66 | 288.60 | **37.5** | 2,916 | Small | Basic Materials | 86,732 | 20,521,516 |
| 202 | 538668 | Meghna Infracon Infrastructure Ltd | BSE | 589.55 | 783.90 | **37.2** | 1,684 | Small | nan | 54,898 | 35,796,148 |
| 203 | SAILIFE | Sai Life Sciences Limited | NSE | 899.40 | 1229.70 | **36.7** | 26,076 | Large | Healthcare | 555,696 | 546,675,107 |
| 204 | CGPOWER | CG Power and Industrial Solutions Limited | NSE | 665.90 | 911.20 | **36.7** | 143,447 | Large | Industrials | 3,438,089 | 2,481,665,093 |
| 205 | VETO | Veto Switchgears And Cables Limited | NSE | 108.62 | 148.45 | **36.7** | 285 | Micro | Industrials | 59,165 | 7,115,694 |
| 206 | UNIVCABLES | Universal Cables Limited | NSE | 895.25 | 1223.40 | **36.5** | 4,249 | Small | Industrials | 191,112 | 183,265,153 |
| 207 | GAEL | Gujarat Ambuja Exports Limited | NSE | 117.52 | 160.27 | **36.4** | 7,336 | Mid | Consumer Defensive | 983,424 | 134,990,139 |
| 208 | GLAND | Gland Pharma Limited | NSE | 1678.60 | 2288.50 | **36.3** | 37,695 | Large | Healthcare | 246,906 | 490,140,135 |
| 209 | NLCINDIA | NLC India Limited | NSE | 243.90 | 327.75 | **36.3** | 45,461 | Large | Utilities | 3,532,314 | 1,084,227,216 |
| 210 | NAHARSPING | Nahar Spinning Mills Limited | NSE | 199.47 | 269.90 | **36.2** | 998 | Small | Consumer Cyclical | 28,570 | 5,809,119 |
| 211 | MBAPL | Madhya Bharat Agro Products Limited | NSE | 408.60 | 553.90 | **36.2** | n/a | nan | Basic Materials | 206,735 | 98,471,760 |
| 212 | KISSHT | OnEMI Technology Solutions Limited | NSE | 208.63 | 284.10 | **36.2** | 4,797 | Small | Financial Services | 8,115,819 | 1,859,662,081 |
| 213 | BHARATFORG | Bharat Forge Limited | NSE | 1426.60 | 1925.40 | **36.2** | 92,058 | Large | Consumer Cyclical | 1,261,075 | 2,110,673,968 |
| 214 | ASIANENE | Asian Energy Services Limited | NSE | 296.70 | 383.80 | **36.0** | 1,726 | Small | Energy | 237,639 | 76,518,745 |
| 215 | ADFFOODS | ADF Foods Limited | NSE | 210.78 | 286.45 | **35.9** | 3,150 | Small | Consumer Defensive | 238,085 | 55,573,892 |
| 216 | SOUTHWEST | South West Pinnacle Exploration Limited | NSE | 195.53 | 260.15 | **35.8** | 775 | Small | Energy | 282,371 | 61,015,572 |
| 217 | JINDALPOLY | Jindal Poly Films Limited | NSE | 494.55 | 669.90 | **35.6** | 2,932 | Small | Consumer Cyclical | 226,986 | 150,634,999 |
| 218 | TIRUPATIFL | Tirupati Forge Limited | NSE | 32.81 | 43.99 | **34.9** | n/a | nan | Industrials | 464,096 | 18,318,390 |
| 219 | KINGFA | Kingfa Science & Technology (India) Limited | NSE | 3853.30 | 5196.00 | **34.9** | 7,043 | Mid | Basic Materials | 6,154 | 28,471,205 |
| 220 | TIMEX | Timex Group India Limited | NSE | 344.55 | 460.30 | **34.6** | 4,646 | Small | Consumer Cyclical | 594,427 | 245,042,487 |
| 221 | GROWW | Billionbrains Garage Ventures Limited | NSE | 145.13 | 195.25 | **34.2** | 122,492 | Large | Financial Services | 62,110,762 | 10,631,222,854 |
| 222 | 543542 | Kesar India Ltd | BSE | 925.00 | 1233.25 | **34.0** | 3,504 | Small | nan | 10,028 | 11,904,881 |
| 223 | AYMSYNTEX | AYM Syntex Limited | NSE | 161.31 | 218.49 | **34.0** | 1,281 | Small | Consumer Cyclical | 29,943 | 5,759,256 |
| 224 | GRANULES | Granules India Limited | NSE | 574.50 | 765.05 | **33.8** | 18,955 | Mid | Healthcare | 1,083,939 | 687,741,379 |
| 225 | KTKBANK | The Karnataka Bank Limited | NSE | 202.20 | 270.60 | **33.8** | 10,238 | Mid | Financial Services | 4,651,476 | 1,001,200,106 |
| 226 | DSSL | Dynacons Systems & Solutions Limited | NSE | 978.80 | 1309.30 | **33.8** | 1,666 | Small | Technology | 173,179 | 197,864,169 |
| 227 | SCI | Shipping Corporation Of India Limited | NSE | 225.42 | 297.15 | **33.4** | 13,832 | Mid | Industrials | 8,399,646 | 2,337,744,647 |
| 228 | LLOYDSME | Lloyds Metals And Energy Limited | NSE | 1288.30 | 1717.20 | **33.3** | 93,586 | Large | Basic Materials | 579,515 | 811,446,618 |
| 229 | DIVGIITTS | Divgi Torqtransfer Systems Limited | NSE | 593.50 | 788.75 | **32.9** | 2,391 | Small | Consumer Cyclical | 33,895 | 24,830,995 |
| 230 | CHENNPETRO | Chennai Petroleum Corporation Limited | NSE | 927.40 | 1226.40 | **32.7** | 18,267 | Mid | Energy | 2,670,148 | 2,573,450,339 |
| 231 | ARFIN | Arfin India Limited | NSE | 64.88 | 85.71 | **32.6** | 1,443 | Small | Basic Materials | 1,184,713 | 100,196,326 |
| 232 | EXICOM | Exicom Tele-Systems Limited | NSE | 111.22 | 147.37 | **32.5** | 2,051 | Small | Industrials | 1,770,037 | 247,013,160 |
| 233 | 540252 | Viram Suvarn Ltd | BSE | 8.34 | 11.05 | **32.5** | 117 | Micro | nan | 407,587 | 4,401,164 |
| 234 | KESORAMIND | Kesoram Industries Limited | NSE | 8.19 | 10.85 | **32.5** | 342 | Micro | Basic Materials | 2,445,819 | 23,178,531 |
| 235 | SBC | SBC Exports Limited | NSE | 27.96 | 37.04 | **32.5** | 1,768 | Small | Industrials | 11,984,484 | 365,710,353 |
| 236 | INDOBORAX | Indo Borax & Chemicals Limited | NSE | 274.67 | 359.10 | **32.4** | 1,152 | Small | Basic Materials | 98,536 | 27,942,852 |
| 237 | LINCOLN | Lincoln Pharmaceuticals Limited | NSE | 472.85 | 637.80 | **32.3** | 1,277 | Small | Healthcare | 86,095 | 54,454,332 |
| 238 | IBULLSLTD | Indiabulls Limited | NSE | 18.94 | 24.47 | **32.3** | 5,685 | Mid | Real Estate | 6,941,636 | 107,400,939 |
| 239 | BLUSPRING | Bluspring Enterprises Limited | NSE | 68.14 | 90.01 | **32.2** | 1,342 | Small | Industrials | 357,349 | 24,185,700 |
| 240 | ABB | ABB India Limited | NSE | 5278.00 | 6931.00 | **32.2** | 146,752 | Large | Industrials | 357,490 | 2,187,109,969 |
| 241 | MARKSANS | Marksans Pharma Limited | NSE | 193.86 | 252.75 | **32.2** | 11,447 | Mid | Healthcare | 1,453,644 | 305,607,244 |
| 242 | POLYCAB | Polycab India Limited | NSE | 7276.50 | 9615.50 | **32.1** | 144,832 | Large | Industrials | 394,920 | 3,089,434,447 |
| 243 | NELCAST | Nelcast Limited | NSE | 109.44 | 143.63 | **32.1** | 1,248 | Small | Industrials | 185,294 | 23,601,186 |
| 244 | PREMIERPOL | Premier Polyfilm Limited | NSE | 42.67 | 55.51 | **32.0** | 585 | Small | Basic Materials | 200,807 | 10,566,634 |
| 245 | GOCLCORP | GOCL Corporation Limited | NSE | 302.50 | 398.85 | **31.9** | 1,980 | Small | Basic Materials | 187,646 | 55,165,843 |
| 246 | DHANBANK | Dhanlaxmi Bank Limited | NSE | 25.28 | 33.08 | **31.6** | 1,302 | Small | Financial Services | 1,256,577 | 36,365,981 |
| 247 | RISHABH | Rishabh Instruments Limited | NSE | 400.65 | 525.20 | **31.4** | 2,026 | Small | Technology | 114,930 | 53,888,706 |
| 248 | GHCLTEXTIL | GHCL Textiles Limited | NSE | 72.27 | 96.88 | **31.3** | 924 | Small | Consumer Cyclical | 291,363 | 24,617,316 |
| 249 | SUPRIYA | Supriya Lifescience Limited | NSE | 744.45 | 962.90 | **31.3** | 7,744 | Mid | Healthcare | 302,181 | 243,891,994 |
| 250 | AETHER | Aether Industries Limited | NSE | 864.80 | 1135.00 | **31.2** | 15,068 | Mid | Basic Materials | 343,755 | 349,473,073 |
| 251 | 535916 | Alacrity Securities Ltd | BSE | 56.59 | 73.11 | **31.2** | 317 | Micro | nan | 53,407 | 3,190,658 |
| 252 | 511523 | Veerhealth Care Ltd | BSE | 18.15 | 24.25 | **31.2** | 49 | Micro | nan | 80,259 | 1,627,359 |
| 253 | AEROENTER | Aeroflex Enterprises Limited | NSE | 80.15 | 105.05 | **31.1** | 1,188 | Small | Basic Materials | 344,212 | 29,925,483 |
| 254 | 531911 | Galaxy Agrico Exports Ltd | BSE | 48.99 | 64.20 | **31.1** | 106 | Micro | nan | 112,689 | 5,097,218 |
| 255 | ANGELONE | Angel One Limited | NSE | 259.53 | 337.55 | **31.0** | 30,821 | Large | Financial Services | 9,222,151 | 2,520,734,105 |
| 256 | GAUDIUMIVF | Gaudium IVF and Women Health Limited | NSE | 80.26 | 105.75 | **30.9** | 766 | Small | Healthcare | 1,135,383 | 110,200,714 |
| 257 | VIJAYA | Vijaya Diagnostic Centre Limited | NSE | 990.45 | 1296.20 | **30.9** | 13,346 | Mid | Healthcare | 214,822 | 236,843,847 |
| 258 | PIRAMALFIN | Piramal Finance Limited | NSE | 1520.40 | 1993.70 | **30.9** | 45,194 | Large | Financial Services | 416,541 | 749,725,712 |
| 259 | UNIPARTS | Uniparts India Limited | NSE | 489.40 | 640.30 | **30.8** | 2,891 | Small | Industrials | 152,695 | 80,212,084 |
| 260 | ADANIENT | Adani Enterprises Limited | NSE | 2282.40 | 2979.90 | **30.8** | 384,758 | Large | Energy | 1,923,603 | 4,456,107,813 |
| 261 | TRUALT | TruAlt Bioenergy Limited | NSE | 407.15 | 531.95 | **30.6** | 4,563 | Small | Energy | 345,305 | 155,713,650 |
| 262 | KDDL | KDDL Limited | NSE | 2307.10 | 3014.10 | **30.6** | 3,718 | Small | Consumer Cyclical | 26,723 | 68,191,064 |
| 263 | BODALCHEM | Bodal Chemicals Limited | NSE | 52.43 | 68.45 | **30.6** | 872 | Small | Basic Materials | 301,404 | 18,512,611 |
| 264 | HCC | Hindustan Construction Company Limited | NSE | 17.94 | 23.42 | **30.6** | 6,137 | Mid | Industrials | 32,679,267 | 657,101,141 |
| 265 | GESHIP | The Great Eastern Shipping Company Limited | NSE | 1109.40 | 1442.20 | **30.5** | 21,187 | Large | Industrials | 764,128 | 1,098,676,601 |
| 266 | ZENTEC | Zen Technologies Limited | NSE | 1389.10 | 1782.50 | **30.2** | 16,087 | Mid | Industrials | 619,427 | 932,578,372 |
| 267 | AMANTA | Amanta Healthcare Limited | NSE | 105.60 | 135.46 | **30.2** | 524 | Small | Healthcare | 113,858 | 13,292,363 |
| 268 | NRL | Nupur Recyclers Limited | NSE | 60.37 | 76.19 | **30.1** | n/a | nan | Industrials | 67,402 | 4,009,539 |
| 269 | SONAMLTD | SONAM LIMITED | NSE | 43.48 | 56.49 | **30.0** | n/a | nan | Consumer Cyclical | 64,395 | 3,126,172 |
| 270 | KEI | KEI Industries Limited | NSE | 4067.10 | 5281.00 | **29.9** | 50,512 | Large | Industrials | 326,806 | 1,489,327,074 |
| 271 | CRAFTSMAN | Craftsman Automation Limited | NSE | 7016.00 | 9126.50 | **29.8** | 21,777 | Large | Consumer Cyclical | 80,415 | 646,929,611 |
| 272 | AKUMS | Akums Drugs and Pharmaceuticals Limited | NSE | 423.05 | 548.25 | **29.6** | 8,635 | Mid | Healthcare | 223,494 | 107,170,599 |
| 273 | HMVL | Hindustan Media Ventures Limited | NSE | 66.23 | 84.86 | **29.5** | 618 | Small | Communication Services | 64,746 | 4,597,236 |
| 274 | OLAELEC | Ola Electric Mobility Limited | NSE | 36.69 | 47.34 | **29.1** | 21,902 | Large | Consumer Cyclical | 98,556,854 | 3,555,963,326 |
| 275 | 543920 | CFF Fluid Control Ltd | BSE | 565.40 | 729.25 | **29.0** | 1,485 | Small | nan | 29,358 | 19,069,905 |
| 276 | SURYODAY | Suryoday Small Finance Bank Limited | NSE | 137.08 | 174.97 | **28.9** | 1,860 | Small | Financial Services | 396,670 | 59,280,805 |
| 277 | SIS | SIS LIMITED | NSE | 324.85 | 421.20 | **28.8** | 5,950 | Mid | Industrials | 132,816 | 46,453,645 |
| 278 | KRISHANA | Krishana Phoschem Limited | NSE | 526.40 | 677.65 | **28.7** | n/a | nan | Basic Materials | 166,074 | 98,363,039 |
| 279 | QUADFUTURE | Quadrant Future Tek Limited | NSE | 267.70 | 343.05 | **28.7** | 1,370 | Small | Industrials | 1,308,718 | 426,467,321 |
| 280 | HINDALCO | Hindalco Industries Limited | NSE | 852.10 | 1076.70 | **28.6** | 242,150 | Large | Basic Materials | 6,156,951 | 5,736,666,058 |
| 281 | SANDHAR | Sandhar Technologies Limited | NSE | 561.10 | 708.90 | **28.5** | 4,269 | Small | Consumer Cyclical | 349,686 | 207,422,308 |
| 282 | SHAILY | Shaily Engineering Plastics Limited | NSE | 2447.20 | 3132.60 | **28.0** | 14,443 | Mid | Basic Materials | 345,163 | 806,066,607 |
| 283 | MMWL | Media Matrix Worldwide Limited | NSE | 10.35 | 13.18 | **28.0** | 1,502 | Small | Communication Services | 172,913 | 2,492,905 |
| 284 | SANGHVIMOV | Sanghvi Movers Limited | NSE | 306.15 | 391.70 | **27.9** | 3,392 | Small | Industrials | 363,124 | 118,099,319 |
| 285 | ASTERDM | Aster DM Healthcare Limited | NSE | 620.35 | 790.35 | **27.9** | 40,945 | Large | Healthcare | 758,383 | 504,311,557 |
| 286 | GANDHAR | Gandhar Oil Refinery (India) Limited | NSE | 124.64 | 159.34 | **27.8** | 1,558 | Small | Energy | 971,454 | 156,098,699 |
| 287 | 500449 | Hindustan Organic Chemicals Ltd | BSE | 30.29 | 38.71 | **27.8** | 260 | Micro | nan | 72,614 | 2,417,483 |
| 288 | TALBROAUTO | Talbros Automotive Components Limited | NSE | 280.75 | 360.05 | **27.8** | 2,232 | Small | Consumer Cyclical | 168,694 | 51,185,332 |
| 289 | ATGL | Adani Total Gas Limited | NSE | 593.70 | 752.15 | **27.7** | 82,728 | Large | Utilities | 4,037,277 | 2,586,931,497 |
| 290 | 530145 | Kisan Mouldings Ltd-$ | BSE | 27.71 | 35.37 | **27.6** | 407 | Micro | nan | 158,263 | 4,892,567 |
| 291 | 539479 | GTV Engineering Ltd | BSE | 57.96 | 73.92 | **27.5** | 360 | Micro | nan | 78,741 | 4,979,590 |
| 292 | 543619 | Concord Control Systems Ltd | BSE | 2286.60 | 2938.05 | **27.5** | 2,986 | Small | nan | 10,364 | 25,000,656 |
| 293 | HAPPYFORGE | Happy Forgings Limited | NSE | 1072.10 | 1363.00 | **27.2** | 12,846 | Mid | Industrials | 68,124 | 84,625,878 |
| 294 | PFC | Power Finance Corporation Limited | NSE | 344.20 | 435.60 | **27.2** | 143,703 | Large | Financial Services | 7,502,473 | 3,031,308,000 |
| 295 | INNOVACAP | Innova Captab Limited | NSE | 721.40 | 914.70 | **26.8** | 5,254 | Mid | Healthcare | 70,397 | 51,173,666 |
| 296 | CALSOFT | California Software Company Limited | NSE | 15.94 | 20.36 | **26.8** | 49 | Micro | Technology | 110,417 | 2,044,473 |
| 297 | AMBIKCO | Ambika Cotton Mills Limited | NSE | 1274.60 | 1611.80 | **26.7** | 929 | Small | Consumer Cyclical | 10,358 | 14,767,599 |
| 298 | WABAG | VA Tech Wabag Limited | NSE | 1245.80 | 1586.30 | **26.6** | 9,900 | Mid | Industrials | 328,771 | 435,094,703 |
| 299 | EQUITASBNK | Equitas Small Finance Bank Limited | NSE | 58.70 | 74.98 | **26.6** | 8,550 | Mid | Financial Services | 3,900,987 | 253,944,859 |
| 300 | AVANTIFEED | Avanti Feeds Limited | NSE | 807.10 | 1027.00 | **26.5** | 13,994 | Mid | Consumer Defensive | 1,171,994 | 1,324,645,131 |
| 301 | PANAMAPET | Panama Petrochem Limited | NSE | 276.50 | 351.85 | **26.5** | 2,130 | Small | Energy | 116,822 | 35,588,782 |
| 302 | TRITURBINE | Triveni Turbine Limited | NSE | 532.90 | 673.20 | **26.3** | 21,393 | Large | Industrials | 1,550,617 | 917,918,079 |
| 303 | 540545 | Guru Krupa Gems and Jewellery Ltd | BSE | 28.43 | 36.05 | **26.3** | 55 | Micro | nan | 128,223 | 4,579,396 |
| 304 | THYROCARE | Thyrocare Technologies Limited | NSE | 435.75 | 547.95 | **26.1** | 8,721 | Mid | Healthcare | 749,997 | 338,643,290 |
| 305 | MMFL | MM Forgings Limited | NSE | 359.40 | 451.90 | **25.7** | 2,178 | Small | Industrials | 180,632 | 72,132,205 |
| 306 | RML | Rane (Madras) Limited | NSE | 741.05 | 927.50 | **25.7** | 2,562 | Small | Consumer Cyclical | 23,524 | 19,917,723 |
| 307 | DCMSIL | DCM Shriram International Limited | NSE | 52.21 | 68.83 | **25.6** | 596 | Small | Industrials | 170,641 | 13,303,966 |
| 308 | AEQUS | Aequs Limited | NSE | 147.05 | 184.11 | **25.2** | 12,370 | Mid | Industrials | 5,119,050 | 817,205,233 |
| 309 | SERVOTECH | Servotech Renewable Power System Limited | NSE | 82.75 | 103.51 | **25.1** | n/a | nan | Industrials | 1,286,300 | 114,287,490 |

🟡 = penny stock (price < ₹10), flagged not removed.

**Machine-readable file:** `FINAL_universe_25pct.csv` (309 rows).

### Known limitations (full disclosure)
- 464 universe symbols (of 4,524) returned no Yahoo history (recently renamed post-corporate-action e.g. demerged Tata Motors, thinly-traded, or delisted-from-Yahoo) — excluded from the scan, not from reality. These are predominantly illiquid BSE micro-caps.
- 11 NSE-only names have no BSE twin, so their current price rests on Yahoo alone (still passes the adjusted-return integrity check).
- Sector unavailable for 37 BSE-only micro-caps (shown as n/a).