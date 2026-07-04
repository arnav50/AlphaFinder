# PHASE 1 — UNIVERSE IDENTIFICATION (NSE + BSE)
**Scan date:** 2026-06-02  |  **180-day reference:** 2025-12-04  |  **Filter:** 180-day price return ≥ 25%

## Methodology (auditable, scripted — no hand-entered prices)
1. **Universe** — NSE official `EQUITY_L.csv` (series EQ+BE) + BSE active-equity scrip master (API), excluding BSE **Z / XT / XC** surveillance groups. Dual-listed companies de-duplicated by **ISIN** (NSE listing preferred).
2. **Prices** — ~180-day daily OHLCV per symbol from Yahoo Finance chart API (sources exchange data). Return = last close ÷ **median of ±2 bars around the 180-day date** (median guards against bad single prints).
3. **Liquidity filter** — avg daily volume ≥ 50,000 shares **OR** avg daily traded value ≥ ₹50 lakh.
4. **Verification (2 sources)** — (a) returns re-derived from **split/bonus-adjusted** prices → 0 corporate-action distortions; (b) current price cross-checked against the **other exchange's live quote** (BSE-twin via ISIN / BSE live API).

## ✓ VERIFICATION CHECKPOINT
- **Total verified stocks (180d return ≥ 25%): 399**
- Exchange split (after ISIN dedup, NSE preferred): {'NSE': 375, 'BSE': 24}
- Market-cap buckets: {'Small': 177, 'Mid': 106, 'Large': 70, 'Micro': 30}  *(Large ≥₹20k cr, Mid ≥₹5k cr, Small ≥₹500 cr, Micro <₹500 cr)*
- Penny stocks (price < ₹10): **0 flagged, none removed** (per spec)
- Cross-source current-price check: 383/399 have a 2nd exchange source; **383/383 agree within 5%** (median mismatch **0.08%**)
- Excluded categories (suspended / Z / XT / XC) removed at universe stage
- Sorted by Return% descending ✓

## OUTPUT — full ranked list
Columns: Symbol | Company | Exch | Price 180d ago | Price today | Return% | MktCap(₹cr) | Cap | Sector | AvgVol(sh) | AvgVal(₹)

| # | Symbol | Company | Exch | 180d Ago | Today | Return% | MktCap₹cr | Cap | Sector | AvgVol | AvgVal₹ |
|--:|---|---|---|--:|--:|--:|--:|---|---|--:|--:|
| 1 | ARIHANT | Arihant Foundations & Housing Limited | NSE | 39.65 | 791.30 | **1895.7** | 796 | Small | Real Estate | 7,007 | 5,835,540 |
| 2 | STLTECH | Sterlite Technologies Limited | NSE | 102.08 | 576.80 | **465.1** | 29,611 | Large | Technology | 5,330,530 | 1,240,805,149 |
| 3 | SANGINITA | Sanginita Chemicals Limited | NSE | 10.18 | 45.85 | **349.1** | n/a | nan | Basic Materials | 170,497 | 3,366,266 |
| 4 | DEEDEV | DEE Development Engineers Limited | NSE | 211.27 | 704.35 | **235.5** | 4,908 | Small | Industrials | 2,178,004 | 645,872,451 |
| 5 | UFBL | United Foodbrands Limited | NSE | 222.02 | 706.45 | **225.4** | 2,761 | Small | Consumer Cyclical | 255,791 | 98,276,411 |
| 6 | HFCL | HFCL Limited | NSE | 67.20 | 214.48 | **211.2** | 32,893 | Large | Technology | 35,130,827 | 4,086,219,124 |
| 7 | BLISSGVS | Bliss GVS Pharma Limited | NSE | 160.42 | 505.95 | **210.7** | 5,355 | Mid | Healthcare | 3,324,154 | 762,782,905 |
| 8 | 540492 | Starlineps Enterprises Ltd | BSE | 3.86 | 11.12 | **188.1** | 479 | Micro | nan | 1,158,921 | 9,202,813 |
| 9 | MTARTECH | Mtar Technologies Limited | NSE | 2473.90 | 7033.50 | **184.3** | 21,664 | Large | Industrials | 887,866 | 5,162,503,430 |
| 10 | SIGMAADV | SIGMA ADVANCED SYSTEMS LIMITED | NSE | 204.16 | 548.40 | **170.1** | 9,698 | Mid | Industrials | 246,768 | 78,116,714 |
| 11 | OMNI | Omnitech Engineering Limited | NSE | 204.93 | 508.65 | **166.8** | 6,300 | Mid | Industrials | 985,469 | 340,038,648 |
| 12 | GVPIL | GE Power India Limited | NSE | 341.10 | 873.75 | **157.1** | 5,890 | Mid | Industrials | 646,801 | 349,361,668 |
| 13 | CPPLUS | Aditya Infotech Limited | NSE | 1465.00 | 3588.40 | **144.9** | 42,328 | Large | Industrials | 277,062 | 624,917,268 |
| 14 | ONELIFECAP | Onelife Capital Advisors Limited | NSE | 16.01 | 38.60 | **140.3** | 145 | Micro | Financial Services | 142,989 | 2,448,909 |
| 15 | INDSWFTLAB | Ind-Swift Laboratories Limited | NSE | 90.34 | 214.16 | **136.7** | 1,861 | Small | Healthcare | 875,720 | 128,904,895 |
| 16 | KOVAI | Kovai Medical Center & Hospital Limited | NSE | 2576.65 | 6042.50 | **134.5** | 6,611 | Mid | Healthcare | 5,399 | 31,179,381 |
| 17 | CUPID | Cupid Limited | NSE | 78.01 | 198.84 | **131.8** | 26,745 | Large | Consumer Defensive | 30,396,404 | 2,939,456,642 |
| 18 | AEROFLEX | Aeroflex Industries Limited | NSE | 200.22 | 456.25 | **130.9** | 6,036 | Mid | Industrials | 2,519,036 | 743,138,662 |
| 19 | KSHINTL | KSH International Limited | NSE | 365.35 | 847.55 | **126.9** | 5,747 | Mid | Industrials | 456,706 | 255,115,854 |
| 20 | VENUSREM | Venus Remedies Limited | NSE | 763.00 | 1720.90 | **126.3** | 2,290 | Small | Healthcare | 75,111 | 79,651,518 |
| 21 | NGLFINE | NGL Fine-Chem Limited | NSE | 1424.70 | 3206.00 | **125.0** | 1,965 | Small | Healthcare | 10,626 | 26,772,137 |
| 22 | OMAXAUTO | Omax Autos Limited | NSE | 103.02 | 231.05 | **123.7** | 493 | Micro | Consumer Cyclical | 131,825 | 21,303,745 |
| 23 | BAJAJCON | Bajaj Consumer Care Limited | NSE | 280.10 | 616.20 | **122.7** | 8,073 | Mid | Consumer Defensive | 1,287,979 | 509,595,372 |
| 24 | NINSYS | NINtec Systems Limited | NSE | 390.35 | 876.60 | **120.5** | 1,636 | Small | Technology | 13,770 | 5,847,839 |
| 25 | BHAGYANGR | Bhagyanagar India Limited | NSE | 169.30 | 371.50 | **119.4** | 1,186 | Small | Basic Materials | 230,556 | 49,436,811 |
| 26 | NOVARTIND | Novartis India Limited | NSE | 672.25 | 1469.40 | **118.6** | 3,627 | Small | Healthcare | 28,697 | 37,521,043 |
| 27 | GRWRHITECH | Garware Hi-Tech Films Limited | NSE | 3131.00 | 6875.00 | **116.9** | 15,952 | Mid | Basic Materials | 86,955 | 395,684,140 |
| 28 | YASHO | Yasho Industries Limited | NSE | 1387.00 | 2972.90 | **114.3** | 3,578 | Small | Basic Materials | 29,773 | 54,266,770 |
| 29 | SHADOWFAX | Shadowfax Technologies Limited | NSE | 109.98 | 225.45 | **111.5** | 13,185 | Mid | Industrials | 2,825,779 | 438,080,064 |
| 30 | ACUTAAS | Acutaas Chemicals Limited | NSE | 1769.60 | 3694.80 | **110.2** | 30,215 | Large | Basic Materials | 429,556 | 1,026,429,769 |
| 31 | SAKAR | Sakar Healthcare Limited | NSE | 410.75 | 848.80 | **108.8** | n/a | nan | Healthcare | 119,489 | 75,196,776 |
| 32 | SCHNEIDER | Schneider Electric Infrastructure Limited | NSE | 702.45 | 1481.60 | **108.6** | 35,427 | Large | Industrials | 395,591 | 381,558,886 |
| 33 | EBGNG | GNG Electronics Limited | NSE | 309.25 | 641.15 | **107.0** | 7,312 | Mid | Technology | 405,885 | 176,336,299 |
| 34 | SPORTKING | Sportking India Limited | NSE | 86.65 | 179.34 | **106.0** | 2,282 | Small | Consumer Cyclical | 309,414 | 45,228,651 |
| 35 | JNKINDIA | JNK India Limited | NSE | 234.95 | 483.75 | **105.3** | 2,712 | Small | Industrials | 705,361 | 270,860,056 |
| 36 | CONFIPET | Confidence Petroleum India Limited | NSE | 36.76 | 74.17 | **104.4** | 2,459 | Small | Energy | 2,736,305 | 150,396,396 |
| 37 | ANTELOPUS | Antelopus Selan Energy Limited | NSE | 395.55 | 802.35 | **102.8** | 2,821 | Small | Energy | 402,382 | 226,955,817 |
| 38 | PAISALO | Paisalo Digital Limited | NSE | 35.48 | 71.87 | **101.9** | 6,539 | Mid | Financial Services | 8,506,584 | 406,272,342 |
| 39 | BALAMINES | Balaji Amines Limited | NSE | 1089.70 | 2194.20 | **101.4** | 7,137 | Mid | Basic Materials | 393,956 | 576,916,590 |
| 40 | RPTECH | Rashi Peripherals Limited | NSE | 379.95 | 757.95 | **99.5** | 4,994 | Small | Technology | 557,383 | 351,486,357 |
| 41 | SUVEN | Suven Life Sciences Limited | NSE | 161.92 | 327.60 | **98.8** | 8,647 | Mid | Healthcare | 926,819 | 221,534,063 |
| 42 | INDOTECH | Indo Tech Transformers Limited | NSE | 1592.60 | 3136.70 | **98.4** | 3,320 | Small | Industrials | 47,457 | 98,273,471 |
| 43 | VIDYAWIRES | Vidya Wires Limited | NSE | 49.67 | 99.02 | **98.1** | 2,105 | Small | Industrials | 5,575,379 | 399,077,556 |
| 44 | SEDEMAC | SEDEMAC Mechatronics Limited | NSE | 1451.10 | 2865.20 | **97.5** | 12,639 | Mid | Consumer Cyclical | 250,051 | 491,643,868 |
| 45 | PARKHOSPS | Park Medi World Limited | NSE | 150.00 | 294.80 | **96.9** | 12,712 | Mid | Healthcare | 1,445,413 | 274,468,137 |
| 46 | AVALON | Avalon Technologies Limited | NSE | 908.70 | 1788.30 | **96.8** | 11,931 | Mid | Technology | 327,396 | 406,126,856 |
| 47 | RUBICON | Rubicon Research Limited | NSE | 665.85 | 1307.00 | **96.3** | 21,545 | Large | Healthcare | 350,284 | 352,636,374 |
| 48 | SETL | Standard Engineering Technology Limited | NSE | 144.67 | 281.75 | **94.8** | 5,617 | Mid | Industrials | 495,257 | 89,537,047 |
| 49 | CEMPRO | Cemindia Projects Limited | NSE | 756.45 | 1449.00 | **91.5** | 24,888 | Large | Industrials | 767,201 | 678,166,282 |
| 50 | SHILPAMED | Shilpa Medicare Limited | NSE | 317.00 | 608.95 | **91.4** | 11,902 | Mid | Healthcare | 720,880 | 318,162,715 |
| 51 | ATLANTAELE | Atlanta Electricals Limited | NSE | 886.80 | 1688.40 | **90.2** | 12,999 | Mid | Industrials | 158,857 | 200,761,203 |
| 52 | EMMVEE | Emmvee Photovoltaic Power Limited | NSE | 184.91 | 358.95 | **90.1** | 24,834 | Large | Technology | 4,202,762 | 1,048,055,062 |
| 53 | BLUSPRING | Bluspring Enterprises Limited | NSE | 67.39 | 123.61 | **88.6** | 1,849 | Small | Industrials | 539,182 | 45,309,754 |
| 54 | E2E | E2E Networks Limited | NSE | 208.85 | 382.00 | **88.4** | 7,851 | Mid | Technology | 1,475,943 | 440,650,964 |
| 55 | IBULLSLTD | Indiabulls Limited | NSE | 15.65 | 29.30 | **87.2** | 6,826 | Mid | Real Estate | 7,485,733 | 123,010,046 |
| 56 | ASTRAMICRO | Astra Microwave Products Limited | NSE | 1000.00 | 1848.50 | **87.2** | 17,567 | Mid | Technology | 580,788 | 729,511,555 |
| 57 | PARAS | Paras Defence and Space Technologies Limited | NSE | 702.70 | 1294.00 | **86.9** | 10,432 | Mid | Industrials | 2,108,331 | 1,966,994,494 |
| 58 | MODISONLTD | MODISON LIMITED | NSE | 159.08 | 299.85 | **86.9** | 974 | Small | Industrials | 122,024 | 27,453,557 |
| 59 | NITTAGELA | Nitta Gelatin India Limited | NSE | 922.65 | 1727.40 | **86.7** | 1,568 | Small | Basic Materials | 18,404 | 27,061,765 |
| 60 | SBCL | Shivalik Bimetal Controls Limited | NSE | 422.25 | 794.05 | **86.2** | 4,567 | Small | Industrials | 303,647 | 185,869,812 |
| 61 | PARACABLES | Paramount Communications Limited | NSE | 38.32 | 71.12 | **84.8** | 2,163 | Small | Technology | 2,095,297 | 113,549,775 |
| 62 | THANGAMAYL | Thangamayil Jewellery Limited | NSE | 3337.00 | 6159.50 | **84.6** | 19,133 | Mid | Consumer Cyclical | 163,080 | 682,416,287 |
| 63 | SYRMA | Syrma SGS Technology Limited | NSE | 750.25 | 1376.00 | **83.6** | 26,551 | Large | Technology | 1,357,281 | 1,267,715,433 |
| 64 | VISL | Vedanta Iron and Steel Limited | NSE | 21.06 | 40.52 | **83.3** | 15,841 | Mid | Basic Materials | 96,933,702 | 3,016,038,126 |
| 65 | KERNEX | Kernex Microsystems (India) Limited | NSE | 1331.80 | 2378.80 | **83.3** | 3,998 | Small | Technology | 263,333 | 372,394,581 |
| 66 | KOTYARK | Kotyark Industries Limited | NSE | 21.34 | 38.88 | **82.2** | 434 | Micro | Basic Materials | 354,322 | 12,297,875 |
| 67 | AEGISLOG | Aegis Logistics Limited | NSE | 732.05 | 1325.40 | **81.0** | 46,530 | Large | Energy | 1,422,339 | 1,231,542,625 |
| 68 | GAYAPROJ | Gayatri Projects Limited | NSE | 12.10 | 21.89 | **80.9** | 414 | Micro | Industrials | 271,090 | 5,301,031 |
| 69 | WELCORP | Welspun Corp Limited | NSE | 802.70 | 1439.30 | **80.1** | 37,965 | Large | Basic Materials | 682,959 | 723,788,134 |
| 70 | BBOX | Black Box Limited | NSE | 553.50 | 994.95 | **79.8** | 17,652 | Mid | Technology | 659,037 | 479,938,471 |
| 71 | MAYURUNIQ | Mayur Uniquoters Ltd | NSE | 491.60 | 882.15 | **79.4** | 3,847 | Small | Consumer Cyclical | 153,721 | 102,782,941 |
| 72 | ARVIND | Arvind Limited | NSE | 317.75 | 569.05 | **79.1** | 14,935 | Mid | Consumer Cyclical | 720,226 | 304,738,015 |
| 73 | KIRLOSENG | Kirloskar Oil Engines Limited | NSE | 1254.30 | 2230.80 | **78.9** | 32,447 | Large | Industrials | 629,848 | 1,051,087,384 |
| 74 | CMPDI | Central Mine Planning & Design Institute Limited | NSE | 154.06 | 277.50 | **77.9** | 19,810 | Mid | Basic Materials | 5,646,107 | 1,263,654,298 |
| 75 | NITINSPIN | Nitin Spinners Limited | NSE | 317.00 | 563.55 | **77.2** | 3,174 | Small | Consumer Cyclical | 367,269 | 147,695,611 |
| 76 | SPARC | Sun Pharma Advanced Research Company Limited | NSE | 135.34 | 239.37 | **76.4** | 7,761 | Mid | Healthcare | 4,503,885 | 787,180,593 |
| 77 | TIRUPATIFL | Tirupati Forge Limited | NSE | 38.11 | 66.82 | **75.3** | n/a | nan | Industrials | 574,724 | 26,403,752 |
| 78 | SCPL | Sheetal Cool Products Limited | NSE | 319.45 | 561.35 | **75.0** | 590 | Small | Consumer Defensive | 27,662 | 9,887,502 |
| 79 | SATIN | Satin Creditcare Network Limited | NSE | 145.98 | 254.80 | **74.5** | 2,820 | Small | Financial Services | 523,504 | 109,276,141 |
| 80 | LOKESHMACH | Lokesh Machines Limited | NSE | 190.52 | 314.90 | **74.4** | 668 | Small | Industrials | 80,551 | 16,204,217 |
| 81 | IOLCP | IOL Chemicals and Pharmaceuticals Limited | NSE | 83.00 | 142.96 | **74.0** | 4,199 | Small | Healthcare | 2,121,385 | 231,369,251 |
| 82 | IDEAFORGE | Ideaforge Technology Limited | NSE | 485.00 | 821.60 | **73.8** | 3,568 | Small | Technology | 1,078,812 | 632,039,975 |
| 83 | KIRLPNU | Kirloskar Pneumatic Company Limited | NSE | 1046.80 | 1825.90 | **73.7** | 11,859 | Mid | Industrials | 147,032 | 217,449,546 |
| 84 | ZIMLAB | Zim Laboratories Limited | NSE | 70.33 | 122.01 | **73.5** | 659 | Small | Healthcare | 75,809 | 6,555,474 |
| 85 | APARINDS | Apar Industries Limited | NSE | 8172.50 | 14174.00 | **73.2** | 56,943 | Large | Industrials | 115,699 | 1,332,622,049 |
| 86 | DJML | DJ Mediaprint & Logistics Limited | NSE | 73.09 | 121.87 | **73.0** | 420 | Micro | Industrials | 205,443 | 18,734,066 |
| 87 | NEOGEN | Neogen Chemicals Limited | NSE | 1144.80 | 1968.30 | **71.9** | 5,385 | Mid | Basic Materials | 184,098 | 243,408,631 |
| 88 | 511523 | Veerhealth Care Ltd | BSE | 19.00 | 32.57 | **71.8** | 65 | Micro | nan | 99,845 | 2,243,725 |
| 89 | COCKERILL | John Cockerill India Limited | NSE | 5277.35 | 8947.50 | **71.6** | 4,418 | Small | Industrials | 24,164 | 207,421,043 |
| 90 | WHEELS | Wheels India Limited | NSE | 869.25 | 1491.60 | **69.8** | 3,642 | Small | Consumer Cyclical | 135,013 | 177,182,242 |
| 91 | SANSERA | Sansera Engineering Limited | NSE | 1933.00 | 3251.50 | **68.9** | 20,257 | Large | Consumer Cyclical | 245,443 | 580,297,794 |
| 92 | 539730 | Fredun Pharmaceuticals Ltd | BSE | 1567.90 | 2588.80 | **68.5** | 1,417 | Small | nan | 12,169 | 23,960,476 |
| 93 | AEQUS | Aequs Limited | NSE | 141.00 | 236.54 | **68.3** | 15,898 | Mid | Industrials | 5,618,339 | 964,644,809 |
| 94 | DATAPATTNS | Data Patterns (India) Limited | NSE | 2731.30 | 4507.00 | **68.3** | 25,242 | Large | Industrials | 954,930 | 3,413,823,164 |
| 95 | APOLLO | Apollo Micro Systems Limited | NSE | 267.75 | 450.05 | **68.1** | 16,075 | Mid | Industrials | 11,183,323 | 3,789,630,050 |
| 96 | SKMEGGPROD | SKM Egg Products Export (India) Limited | NSE | 184.98 | 314.60 | **67.8** | 1,656 | Small | Consumer Defensive | 560,228 | 120,117,017 |
| 97 | JAYBARMARU | Jay Bharat Maruti Limited | NSE | 104.31 | 171.55 | **67.6** | 1,854 | Small | Consumer Cyclical | 805,069 | 97,420,876 |
| 98 | SKYGOLD | SKY GOLD AND DIAMONDS LIMITED | NSE | 335.75 | 560.00 | **67.6** | 8,674 | Mid | Consumer Cyclical | 1,072,536 | 452,197,488 |
| 99 | DIVGIITTS | Divgi Torqtransfer Systems Limited | NSE | 617.70 | 1021.50 | **66.5** | 3,127 | Small | Consumer Cyclical | 99,265 | 89,215,635 |
| 100 | GRANDOAK | Grand Oak Canyons Distillery Limited | NSE | 28.90 | 48.01 | **66.1** | 2,486 | Small | nan | 59,291 | 2,206,260 |
| 101 | 532380 | Baba Arts Ltd-$ | BSE | 9.55 | 15.08 | **65.7** | 79 | Micro | nan | 71,060 | 939,365 |
| 102 | INOXINDIA | INOX India Limited | NSE | 1123.30 | 1871.00 | **65.5** | 16,989 | Mid | Industrials | 212,259 | 330,574,593 |
| 103 | POWERINDIA | Hitachi Energy India Limited | NSE | 19004.00 | 31040.00 | **64.7** | 138,259 | Large | Industrials | 159,726 | 4,187,724,815 |
| 104 | APOLLOPIPE | Apollo Pipes Limited | NSE | 283.10 | 479.40 | **63.3** | 2,106 | Small | Industrials | 925,158 | 377,880,280 |
| 105 | KRN | KRN Heat Exchanger and Refrigeration Limited | NSE | 758.35 | 1214.80 | **63.3** | 7,937 | Mid | Technology | 863,758 | 843,321,738 |
| 106 | KPL | Kwality Pharmaceuticals Limited | NSE | 1662.60 | 2678.70 | **63.2** | 2,777 | Small | nan | 44,267 | 97,638,664 |
| 107 | 544023 | Kalyani Cast-Tech Ltd | BSE | 464.65 | 757.55 | **63.0** | 544 | Small | nan | 11,183 | 6,344,528 |
| 108 | SENORES | Senores Pharmaceuticals Limited | NSE | 847.80 | 1381.90 | **63.0** | 6,356 | Mid | Healthcare | 322,979 | 308,629,298 |
| 109 | NRL | Nupur Recyclers Limited | NSE | 56.82 | 92.57 | **62.9** | n/a | nan | Industrials | 75,533 | 4,767,568 |
| 110 | ATHERENERG | Ather Energy Limited | NSE | 684.90 | 1130.00 | **62.7** | 43,300 | Large | Consumer Cyclical | 3,307,043 | 2,812,537,746 |
| 111 | DECNGOLD | Deccan Gold Mines Limited | NSE | 120.20 | 195.46 | **62.6** | 3,888 | Small | nan | 2,643,742 | 470,386,831 |
| 112 | PREMIERPOL | Premier Polyfilm Limited | NSE | 42.35 | 68.30 | **62.5** | 718 | Small | Basic Materials | 208,321 | 11,155,278 |
| 113 | WABAG | VA Tech Wabag Limited | NSE | 1284.20 | 2080.90 | **62.0** | 13,000 | Mid | Industrials | 435,272 | 655,818,832 |
| 114 | SGFIN | SG Finserve Limited | NSE | 411.05 | 673.80 | **61.8** | 3,761 | Small | Financial Services | 279,416 | 139,131,408 |
| 115 | UNIVPHOTO | Universus Photo Imagings Limited | NSE | 224.14 | 357.95 | **61.4** | 400 | Micro | Healthcare | 15,567 | 6,635,147 |
| 116 | ELPROINTL | Elpro International Limited | NSE | 105.35 | 173.51 | **61.4** | 2,940 | Small | nan | 172,276 | 25,776,237 |
| 117 | ACMESOLAR | Acme Solar Holdings Limited | NSE | 238.63 | 383.25 | **61.1** | 27,087 | Large | Utilities | 1,634,773 | 466,804,088 |
| 118 | CENTUM | Centum Electronics Limited | NSE | 2236.50 | 3627.00 | **61.0** | 5,361 | Mid | Technology | 72,554 | 203,784,689 |
| 119 | FCL | Fineotex Chemical Limited | NSE | 24.36 | 39.12 | **60.6** | 4,557 | Small | Basic Materials | 10,000,850 | 341,616,371 |
| 120 | J&KBANK | The Jammu & Kashmir Bank Limited | NSE | 103.49 | 165.20 | **59.6** | 18,192 | Mid | Financial Services | 4,586,454 | 567,989,381 |
| 121 | SPAL | S. P. Apparels Limited | NSE | 700.45 | 1118.60 | **59.6** | 2,817 | Small | Consumer Cyclical | 139,293 | 124,948,353 |
| 122 | RISHABH | Rishabh Instruments Limited | NSE | 407.00 | 649.45 | **59.6** | 2,514 | Small | Technology | 136,253 | 67,713,451 |
| 123 | XPROINDIA | Xpro India Limited | NSE | 938.30 | 1495.00 | **59.3** | 3,512 | Small | Basic Materials | 55,910 | 62,728,423 |
| 124 | SGMART | SG Mart Limited | NSE | 378.00 | 600.95 | **59.0** | 7,589 | Mid | Industrials | 280,863 | 132,647,018 |
| 125 | TDPOWERSYS | TD Power Systems Limited | NSE | 694.30 | 1091.80 | **58.6** | 16,993 | Mid | Industrials | 1,123,541 | 1,109,022,985 |
| 126 | MEGASTAR | Megastar Foods Limited | NSE | 232.02 | 366.70 | **58.4** | 416 | Micro | Consumer Defensive | 26,283 | 7,936,508 |
| 127 | AFIL | Akme Fintrade (India) Limited | NSE | 6.37 | 10.07 | **58.1** | 431 | Micro | Financial Services | 1,637,090 | 12,854,398 |
| 128 | PRECWIRE | Precision Wires India Limited | NSE | 253.92 | 400.75 | **57.8** | 7,303 | Mid | Industrials | 969,975 | 304,267,276 |
| 129 | HONASA | Honasa Consumer Limited | NSE | 292.50 | 461.75 | **57.7** | 15,044 | Mid | Consumer Defensive | 1,789,057 | 629,542,832 |
| 130 | ADFFOODS | ADF Foods Limited | NSE | 204.06 | 320.40 | **57.0** | 3,522 | Small | Consumer Defensive | 347,558 | 91,551,799 |
| 131 | ADVAIT | Advait Energy Transitions Limited | NSE | 1391.80 | 2188.20 | **56.6** | 2,392 | Small | Industrials | 58,651 | 113,953,999 |
| 132 | ROSSTECH | Rossell Techsys Limited | NSE | 629.25 | 981.10 | **56.5** | 3,688 | Small | Industrials | 211,973 | 172,616,247 |
| 133 | SPECTRUM | Spectrum Electrical Industries Limited | NSE | 1189.60 | 1853.20 | **55.8** | 2,930 | Small | Industrials | 12,768 | 18,916,574 |
| 134 | NRBBEARING | NRB Bearing Limited | NSE | 268.50 | 423.15 | **55.6** | 4,103 | Small | Consumer Cyclical | 545,015 | 196,496,005 |
| 135 | AYMSYNTEX | AYM Syntex Limited | NSE | 166.67 | 262.64 | **55.2** | 1,545 | Small | Consumer Cyclical | 33,169 | 6,789,330 |
| 136 | EXICOM | Exicom Tele-Systems Limited | NSE | 115.41 | 178.01 | **54.2** | 2,481 | Small | Industrials | 2,664,345 | 394,866,722 |
| 137 | 524520 | KMC Speciality Hospitals (India) Ltd | BSE | 86.76 | 133.65 | **54.0** | 2,180 | Small | nan | 133,183 | 13,509,202 |
| 138 | GALAPREC | Gala Precision Engineering Limited | NSE | 768.20 | 1183.40 | **53.9** | 1,518 | Small | Industrials | 40,267 | 38,203,671 |
| 139 | NARMADA | Narmada Agrobase Limited | NSE | 23.62 | 36.34 | **53.9** | 138 | Micro | Basic Materials | 503,476 | 18,501,504 |
| 140 | 543787 | Macfos Ltd | BSE | 718.86 | 1128.55 | **53.8** | 1,169 | Small | nan | 9,223 | 8,787,153 |
| 141 | UTLSOLAR | Fujiyama Power Systems Limited | NSE | 225.00 | 342.75 | **53.4** | 10,507 | Mid | Technology | 683,088 | 164,291,486 |
| 142 | TIMEX | Timex Group India Limited | NSE | 344.55 | 524.45 | **53.4** | 5,302 | Mid | Consumer Cyclical | 583,838 | 258,338,990 |
| 143 | ICIL | Indo Count Industries Limited | NSE | 278.35 | 426.50 | **53.2** | 8,497 | Mid | Consumer Cyclical | 776,117 | 254,541,654 |
| 144 | VTL | Vardhman Textiles Limited | NSE | 435.15 | 666.25 | **53.1** | 19,315 | Mid | Consumer Cyclical | 514,902 | 275,559,853 |
| 145 | JINDALSAW | Jindal Saw Limited | NSE | 172.69 | 260.95 | **53.0** | 16,678 | Mid | Basic Materials | 5,244,047 | 1,038,540,128 |
| 146 | RUBYMILLS | The Ruby Mills Limited | NSE | 220.06 | 339.65 | **52.9** | 1,133 | Small | Consumer Cyclical | 60,804 | 15,571,399 |
| 147 | RRKABEL | R R Kabel Limited | NSE | 1536.70 | 2343.30 | **52.5** | 26,480 | Large | Industrials | 409,760 | 747,599,481 |
| 148 | FAZE3Q | Faze Three Limited | NSE | 403.65 | 614.25 | **52.2** | 1,494 | Small | Consumer Cyclical | 73,170 | 35,344,831 |
| 149 | SAIPARENT | Sai Parenterals Limited | NSE | 405.70 | 618.60 | **52.1** | 2,738 | Small | Healthcare | 347,047 | 180,392,538 |
| 150 | VENUSPIPES | Venus Pipes & Tubes Limited | NSE | 1179.30 | 1783.20 | **52.0** | 3,697 | Small | Basic Materials | 78,790 | 104,144,820 |
| 151 | ADANIGREEN | Adani Green Energy Limited | NSE | 1030.50 | 1556.20 | **51.7** | 256,408 | Large | Utilities | 3,427,289 | 3,817,004,797 |
| 152 | AEROENTER | Aeroflex Enterprises Limited | NSE | 86.76 | 130.65 | **50.6** | 1,480 | Small | Basic Materials | 587,468 | 63,591,589 |
| 153 | 543828 | Sudarshan Pharma Industries Ltd | BSE | 26.24 | 39.49 | **50.5** | 950 | Small | nan | 203,380 | 5,666,725 |
| 154 | TALBROAUTO | Talbros Automotive Components Limited | NSE | 273.90 | 412.10 | **50.5** | 2,543 | Small | Consumer Cyclical | 208,455 | 68,071,088 |
| 155 | ADANIPOWER | Adani Power Limited | NSE | 146.20 | 221.79 | **50.3** | 427,638 | Large | Utilities | 29,701,252 | 5,594,966,322 |
| 156 | ADANIENSOL | Adani Energy Solutions Limited | NSE | 1044.90 | 1568.80 | **50.1** | 188,511 | Large | Utilities | 2,235,359 | 2,741,040,091 |
| 157 | THERMAX | Thermax Limited | NSE | 3070.60 | 4607.50 | **50.1** | 54,962 | Large | Industrials | 208,983 | 836,190,567 |
| 158 | LLOYDSENGG | LLOYDS ENGINEERING WORKS LIMITED | NSE | 56.75 | 83.94 | **49.5** | 12,272 | Mid | Industrials | 8,847,278 | 597,660,775 |
| 159 | KISSHT | OnEMI Technology Solutions Limited | NSE | 208.63 | 311.60 | **49.4** | 5,241 | Mid | Financial Services | 5,789,091 | 1,404,315,920 |
| 160 | 543920 | CFF Fluid Control Ltd | BSE | 599.45 | 879.40 | **49.2** | 1,844 | Small | nan | 29,366 | 19,802,570 |
| 161 | MANINDS | Man Industries (India) Limited | NSE | 394.45 | 582.55 | **48.7** | 4,373 | Small | Basic Materials | 848,389 | 392,214,501 |
| 162 | AMANTA | Amanta Healthcare Limited | NSE | 110.45 | 163.09 | **48.6** | 641 | Small | Healthcare | 165,151 | 21,304,844 |
| 163 | MANCREDIT | Mangal Credit and Fincorp Limited | NSE | 164.68 | 245.33 | **48.0** | 518 | Small | Financial Services | 113,721 | 22,972,965 |
| 164 | RAMCOSYS | Ramco Systems Limited | NSE | 540.40 | 799.60 | **48.0** | 3,007 | Small | Technology | 847,524 | 577,880,306 |
| 165 | RML | Rane (Madras) Limited | NSE | 831.40 | 1206.80 | **47.7** | 3,325 | Small | Consumer Cyclical | 44,811 | 44,170,217 |
| 166 | STEELCAS | Steelcast Limited | NSE | 209.45 | 310.55 | **47.7** | 3,139 | Small | Basic Materials | 126,537 | 34,260,578 |
| 167 | HIRECT | Hind Rectifiers Limited | NSE | 743.10 | 1092.20 | **47.0** | 3,757 | Small | Industrials | 141,096 | 124,481,005 |
| 168 | ANGELONE | Angel One Limited | NSE | 240.20 | 352.25 | **46.6** | 32,150 | Large | Financial Services | 8,956,938 | 2,510,681,269 |
| 169 | CLEANMAX | Clean Max Enviro Energy Solutions Limited | NSE | 867.50 | 1256.70 | **46.5** | 14,727 | Mid | Utilities | 433,210 | 465,239,154 |
| 170 | SBC | SBC Exports Limited | NSE | 28.75 | 42.14 | **46.5** | 2,008 | Small | Industrials | 12,317,032 | 400,387,307 |
| 171 | INDOBORAX | Indo Borax & Chemicals Limited | NSE | 267.95 | 392.25 | **46.4** | 1,262 | Small | Basic Materials | 124,645 | 38,962,360 |
| 172 | OFSS | Oracle Financial Services Software Limited | NSE | 7677.00 | 11248.00 | **46.3** | 97,922 | Large | Technology | 219,041 | 1,891,495,589 |
| 173 | STYLAMIND | Stylam Industries Limited | NSE | 2188.50 | 3230.00 | **46.3** | 5,470 | Mid | Consumer Cyclical | 59,221 | 138,541,606 |
| 174 | VINDHYATEL | Vindhya Telelinks Limited | NSE | 1392.70 | 2032.90 | **46.0** | 2,410 | Small | Industrials | 53,196 | 93,065,128 |
| 175 | PANACEABIO | Panacea Biotec Limited | NSE | 369.90 | 551.20 | **46.0** | 3,366 | Small | Healthcare | 767,074 | 350,632,777 |
| 176 | AMAGI | Amagi Media Labs Limited | NSE | 348.25 | 532.60 | **45.7** | 11,505 | Mid | Technology | 753,906 | 296,814,653 |
| 177 | SWANDEF | Swan Defence and Heavy Industries Limited | NSE | 1606.90 | 2339.80 | **45.6** | 12,337 | Mid | Industrials | 14,527 | 27,443,456 |
| 178 | PRADPME | Pradeep Metals Limited | NSE | 370.60 | 547.45 | **45.5** | 944 | Small | nan | 29,832 | 14,185,628 |
| 179 | TMB | Tamilnad Mercantile Bank Limited | NSE | 535.10 | 778.65 | **45.5** | 12,311 | Mid | Financial Services | 372,139 | 245,140,316 |
| 180 | SUDEEPPHRM | Sudeep Pharma Limited | NSE | 597.50 | 868.05 | **45.5** | 9,786 | Mid | Healthcare | 637,881 | 465,186,555 |
| 181 | SOLARINDS | Solar Industries India Limited | NSE | 12731.00 | 18514.00 | **45.4** | 167,605 | Large | Basic Materials | 161,523 | 2,394,489,760 |
| 182 | KRISHANA | Krishana Phoschem Limited | NSE | 104.71 | 151.85 | **45.3** | n/a | nan | Basic Materials | 938,419 | 116,670,296 |
| 183 | MARKSANS | Marksans Pharma Limited | NSE | 182.02 | 264.45 | **45.3** | 11,964 | Mid | Healthcare | 1,571,290 | 346,384,137 |
| 184 | KRISHNADEF | Krishna Defence And Allied Industries Limited | NSE | 862.60 | 1253.20 | **45.3** | n/a | nan | Industrials | 148,194 | 157,773,148 |
| 185 | NDLVENTURE | NDL Ventures Limited | NSE | 91.89 | 133.37 | **45.1** | 448 | Micro | Communication Services | 44,744 | 5,238,987 |
| 186 | GAUDIUMIVF | Gaudium IVF and Women Health Limited | NSE | 80.26 | 116.90 | **44.7** | 852 | Small | Healthcare | 925,239 | 90,002,594 |
| 187 | BHARATFORG | Bharat Forge Limited | NSE | 1482.30 | 2136.70 | **44.6** | 102,220 | Large | Consumer Cyclical | 1,291,620 | 2,279,428,028 |
| 188 | MBAPL | Madhya Bharat Agro Products Limited | NSE | 86.73 | 125.15 | **44.3** | n/a | nan | Basic Materials | 1,067,791 | 104,748,175 |
| 189 | PREMEXPLN | Premier Explosives Limited | NSE | 543.70 | 782.05 | **44.2** | 4,203 | Small | Basic Materials | 588,912 | 375,527,743 |
| 190 | GCSL | Gretex Corporate Services Limited | NSE | 335.25 | 490.45 | **44.2** | 1,189 | Small | Financial Services | 184,277 | 75,012,494 |
| 191 | GLAND | Gland Pharma Limited | NSE | 1698.20 | 2462.30 | **44.1** | 40,588 | Large | Healthcare | 327,204 | 683,773,651 |
| 192 | BTTL | Bhilwara Technical Textiles Limited | NSE | 34.70 | 49.88 | **43.8** | 291 | Micro | Consumer Cyclical | 57,589 | 2,617,172 |
| 193 | POWERICA | Powerica Limited | NSE | 390.00 | 567.30 | **43.6** | 7,197 | Mid | Industrials | 531,591 | 267,532,766 |
| 194 | AETHER | Aether Industries Limited | NSE | 946.70 | 1359.60 | **43.6** | 18,060 | Mid | Basic Materials | 339,927 | 369,985,913 |
| 195 | APCOTEXIND | Apcotex Industries Limited | NSE | 372.85 | 525.55 | **43.6** | 2,724 | Small | Basic Materials | 64,140 | 30,499,726 |
| 196 | MOREPENLAB | Morepen Laboratories Limited | NSE | 41.26 | 59.07 | **43.2** | 3,232 | Small | Healthcare | 6,117,854 | 287,068,439 |
| 197 | IFCI | IFCI Limited | NSE | 53.11 | 75.91 | **43.0** | 20,458 | Large | Financial Services | 39,151,370 | 2,727,417,891 |
| 198 | SUYOG | Suyog Telematics Limited | NSE | 617.20 | 876.85 | **42.9** | 1,027 | Small | Communication Services | 35,656 | 24,942,266 |
| 199 | CALSOFT | California Software Company Limited | NSE | 15.10 | 22.29 | **42.8** | 79 | Micro | Technology | 116,595 | 2,244,396 |
| 200 | GHCLTEXTIL | GHCL Textiles Limited | NSE | 76.80 | 106.75 | **42.8** | 1,020 | Small | Consumer Cyclical | 341,967 | 29,911,068 |
| 201 | BSE | BSE Limited | NSE | 2673.90 | 3816.60 | **42.7** | n/a | nan | Financial Services | 4,191,758 | 13,343,907,410 |
| 202 | RAYMOND | Raymond Limited | NSE | 430.15 | 607.90 | **42.7** | 4,042 | Small | Industrials | 590,632 | 277,170,154 |
| 203 | GVT&D | GE Vernova T&D India Limited | NSE | 3077.20 | 4401.50 | **42.3** | 112,508 | Large | Industrials | 893,970 | 3,389,521,909 |
| 204 | BIRLACABLE | Birla Cable Limited | NSE | 137.18 | 192.35 | **41.8** | 576 | Small | Technology | 75,429 | 12,434,686 |
| 205 | MACPOWER | Macpower CNC Machines Limited | NSE | 1003.40 | 1422.20 | **41.7** | n/a | nan | Industrials | 33,664 | 35,600,407 |
| 206 | PANAMAPET | Panama Petrochem Limited | NSE | 299.35 | 425.55 | **41.3** | 2,579 | Small | Energy | 314,326 | 124,370,110 |
| 207 | ADANIENT | Adani Enterprises Limited | NSE | 2279.50 | 3212.10 | **41.2** | 417,877 | Large | Energy | 1,947,073 | 4,655,626,357 |
| 208 | CORONA | CORONA Remedies Limited | NSE | 1467.10 | 2037.90 | **41.2** | 12,453 | Mid | Healthcare | 190,669 | 281,479,361 |
| 209 | VIYASH | Viyash Scientific Limited | NSE | 206.94 | 294.15 | **41.2** | 12,853 | Mid | Healthcare | 1,554,585 | 368,168,411 |
| 210 | FINCABLES | Finolex Cables Limited | NSE | 781.95 | 1100.10 | **40.6** | 16,826 | Mid | Industrials | 459,377 | 437,780,549 |
| 211 | DBOL | Dhampur Bio Organics Limited | NSE | 79.81 | 111.92 | **40.2** | 748 | Small | Consumer Defensive | 179,220 | 18,676,377 |
| 212 | HSCL | Himadri Speciality Chemical Limited | NSE | 489.70 | 680.65 | **40.2** | 34,359 | Large | Basic Materials | 5,629,554 | 3,353,026,956 |
| 213 | SOTL | Savita Oil Technologies Limited | NSE | 380.10 | 532.65 | **40.1** | 3,627 | Small | Basic Materials | 199,356 | 102,739,577 |
| 214 | AKUMS | Akums Drugs and Pharmaceuticals Limited | NSE | 447.35 | 626.80 | **40.1** | 9,856 | Mid | Healthcare | 250,661 | 127,161,932 |
| 215 | NEPHROPLUS | Nephrocare Health Services Limited | NSE | 479.90 | 671.95 | **40.0** | 6,745 | Mid | Healthcare | 357,395 | 189,492,336 |
| 216 | CGPOWER | CG Power and Industrial Solutions Limited | NSE | 645.25 | 892.55 | **39.9** | 140,661 | Large | Industrials | 3,680,259 | 2,767,630,460 |
| 217 | GOCLCORP | GOCL Corporation Limited | NSE | 288.20 | 403.50 | **39.9** | 1,998 | Small | Basic Materials | 201,439 | 61,547,235 |
| 218 | ONIDA | Onida Electronics Limited | NSE | 31.71 | 44.36 | **39.9** | 1,641 | Small | Consumer Cyclical | 1,590,305 | 56,736,673 |
| 219 | JTLIND | JTL INDUSTRIES LIMITED | NSE | 58.87 | 82.29 | **39.8** | 3,237 | Small | Basic Materials | 5,026,884 | 344,690,098 |
| 220 | LIKHITHA | Likhitha Infrastructure Limited | NSE | 187.56 | 262.30 | **39.7** | 1,034 | Small | Energy | 102,172 | 19,642,460 |
| 221 | STEELXIND | STEEL EXCHANGE INDIA LIMITED | NSE | 9.12 | 12.74 | **39.7** | 1,625 | Small | Basic Materials | 2,621,904 | 27,967,090 |
| 222 | DIACABS | Diamond Power Infrastructure Limited | NSE | 143.13 | 198.89 | **39.6** | 10,463 | Mid | Industrials | 2,931,275 | 510,059,520 |
| 223 | AMBIKCO | Ambika Cotton Mills Limited | NSE | 1246.80 | 1735.60 | **39.5** | 994 | Small | Consumer Cyclical | 11,792 | 17,562,143 |
| 224 | QUADFUTURE | Quadrant Future Tek Limited | NSE | 343.00 | 469.80 | **39.4** | 1,880 | Small | Industrials | 1,279,824 | 429,731,113 |
| 225 | HARDWYN | Hardwyn India Limited | NSE | 17.33 | 24.75 | **39.4** | 1,207 | Small | Industrials | 2,760,643 | 61,401,088 |
| 226 | QPOWER | Quality Power Electrical Equipments Limited | NSE | 834.65 | 1132.10 | **39.3** | 8,719 | Mid | Industrials | 891,485 | 829,164,468 |
| 227 | SASKEN | Sasken Technologies Limited | NSE | 1503.10 | 2094.00 | **39.3** | 3,180 | Small | Technology | 113,984 | 200,644,854 |
| 228 | BOROSCI | Borosil Scientific Limited | NSE | 118.68 | 166.45 | **39.2** | 1,478 | Small | Consumer Cyclical | 158,051 | 22,268,119 |
| 229 | AVADHSUGAR | Avadh Sugar & Energy Limited | NSE | 372.50 | 511.90 | **39.1** | 1,022 | Small | Consumer Defensive | 72,624 | 30,420,270 |
| 230 | LAURUSLABS | Laurus Labs Limited | NSE | 1103.20 | 1542.30 | **38.9** | 83,293 | Large | Healthcare | 1,910,536 | 2,209,057,808 |
| 231 | MENONBE | Menon Bearings Limited | NSE | 114.42 | 158.77 | **38.8** | 890 | Small | Consumer Cyclical | 124,247 | 18,336,000 |
| 232 | SINDHUTRAD | Sindhu Trade Links Limited | NSE | 20.02 | 27.66 | **38.7** | 4,288 | Small | Industrials | 2,123,330 | 51,358,603 |
| 233 | GOODLUCK | Goodluck India Limited | NSE | 1100.30 | 1490.20 | **38.7** | 4,952 | Small | Basic Materials | 135,732 | 171,536,642 |
| 234 | ABSLAMC | Aditya Birla Sun Life AMC Limited | NSE | 853.65 | 1178.40 | **38.6** | 34,077 | Large | Financial Services | 440,713 | 421,589,353 |
| 235 | SONACOMS | Sona BLW Precision Forgings Limited | NSE | 481.40 | 660.10 | **38.5** | 41,060 | Large | Consumer Cyclical | 2,028,338 | 1,098,819,192 |
| 236 | MAHABANK | Bank of Maharashtra | NSE | 64.03 | 88.53 | **38.5** | 68,101 | Large | Financial Services | 21,438,424 | 1,508,538,704 |
| 237 | 544141 | Pune E - Stock Broking Ltd | BSE | 204.00 | 284.00 | **38.4** | 447 | Micro | nan | 23,594 | 5,615,159 |
| 238 | BHARATSE | Bharat Seats Limited | NSE | 173.96 | 239.73 | **38.3** | 1,506 | Small | Consumer Cyclical | 669,799 | 141,015,201 |
| 239 | SHREEJISPG | Shreeji Shipping Global Limited | NSE | 375.25 | 520.80 | **38.1** | 8,486 | Mid | Industrials | 1,146,788 | 441,153,844 |
| 240 | REFEX | Refex Industries Limited | NSE | 259.70 | 358.40 | **38.0** | 4,919 | Small | Energy | 1,848,364 | 534,493,226 |
| 241 | HEXAGON | Hexagon Nutrition Limited | NSE | 50.66 | 73.39 | **38.0** | 905 | Small | Consumer Defensive | 4,005,206 | 245,689,532 |
| 242 | HESTERBIO | Hester Biosciences Limited | NSE | 1592.60 | 2198.40 | **37.9** | 1,879 | Small | Healthcare | 8,059 | 14,478,550 |
| 243 | CHENNPETRO | Chennai Petroleum Corporation Limited | NSE | 813.60 | 1125.80 | **37.8** | 16,758 | Mid | Energy | 1,830,397 | 1,821,226,725 |
| 244 | MSTCLTD | Mstc Limited | NSE | 529.70 | 715.70 | **37.7** | 5,039 | Mid | Industrials | 600,548 | 346,684,829 |
| 245 | ASHIANA | Ashiana Housing Limited | NSE | 282.70 | 389.90 | **37.6** | 3,902 | Small | Real Estate | 139,454 | 46,983,420 |
| 246 | CAPLIPOINT | Caplin Point Laboratories Limited | NSE | 1845.30 | 2538.10 | **37.5** | 19,272 | Mid | Healthcare | 114,663 | 228,484,216 |
| 247 | NELCAST | Nelcast Limited | NSE | 104.92 | 142.78 | **37.4** | 1,244 | Small | Industrials | 207,761 | 27,195,146 |
| 248 | SIGNPOST | Signpost India Limited | NSE | 218.34 | 299.70 | **37.3** | 1,596 | Small | Communication Services | 261,112 | 73,290,410 |
| 249 | NAHARSPING | Nahar Spinning Mills Limited | NSE | 194.61 | 265.85 | **37.0** | 967 | Small | Consumer Cyclical | 27,915 | 5,741,371 |
| 250 | NAM-INDIA | Nippon Life India Asset Management Limited | NSE | 899.65 | 1218.20 | **36.5** | 77,812 | Large | Financial Services | 959,324 | 928,631,911 |
| 251 | EMIL | Electronics Mart India Limited | NSE | 103.10 | 140.68 | **36.5** | 5,410 | Mid | Consumer Cyclical | 1,201,305 | 136,212,736 |
| 252 | BLSE | BLS E-Services Limited | NSE | 193.97 | 265.11 | **36.3** | 2,407 | Small | Industrials | 490,179 | 96,914,355 |
| 253 | BANDHANBNK | Bandhan Bank Limited | NSE | 147.19 | 200.60 | **36.3** | 32,310 | Large | Financial Services | 10,272,014 | 1,801,599,339 |
| 254 | WELSPLSOL | Welspun Specialty Solutions Limited | NSE | 38.05 | 52.94 | **36.3** | 3,511 | Small | nan | 1,666,597 | 87,448,514 |
| 255 | GRANULES | Granules India Limited | NSE | 605.25 | 833.80 | **36.2** | 20,645 | Large | Healthcare | 1,136,195 | 747,566,430 |
| 256 | BLACKROSE | Black Rose Inds. Limited | NSE | 83.25 | 113.38 | **36.1** | 572 | Small | nan | 75,811 | 8,570,079 |
| 257 | AYE | Aye Finance Limited | NSE | 128.91 | 176.06 | **35.8** | 4,345 | Small | Financial Services | 1,854,761 | 255,805,536 |
| 258 | SAREGAMA | Saregama India Limited | NSE | 370.40 | 485.75 | **35.7** | 9,364 | Mid | Communication Services | 1,816,201 | 733,407,929 |
| 259 | ONMOBILE | OnMobile Global Limited | NSE | 58.68 | 80.03 | **35.7** | 850 | Small | Communication Services | 554,721 | 33,717,834 |
| 260 | RATEGAIN | Rategain Travel Technologies Limited | NSE | 697.90 | 941.05 | **35.6** | 11,143 | Mid | Technology | 486,041 | 321,633,451 |
| 261 | 540786 | Sharika Enterprises Ltd | BSE | 13.97 | 18.88 | **35.4** | 82 | Micro | nan | 74,417 | 1,085,842 |
| 262 | KDDL | KDDL Limited | NSE | 2349.20 | 3244.00 | **35.3** | 3,991 | Small | Consumer Cyclical | 29,903 | 79,259,195 |
| 263 | QUESS | Quess Corp Limited | NSE | 213.03 | 290.85 | **35.2** | 4,343 | Small | Industrials | 664,696 | 149,013,997 |
| 264 | KIMS | Krishna Institute of Medical Sciences Limited | NSE | 653.60 | 850.65 | **35.2** | 35,732 | Large | Healthcare | 472,849 | 333,121,837 |
| 265 | MWL | Mangalam Worldwide Limited | NSE | 271.40 | 376.00 | **35.2** | 1,117 | Small | Basic Materials | 83,199 | 24,468,866 |
| 266 | NETWEB | Netweb Technologies India Limited | NSE | 3274.60 | 4427.40 | **35.2** | 25,198 | Large | Technology | 1,719,096 | 6,525,824,191 |
| 267 | GNA | GNA Axles Limited | NSE | 344.80 | 466.00 | **35.1** | 2,009 | Small | Consumer Cyclical | 197,053 | 79,133,318 |
| 268 | FUSION | Fusion Finance Limited | NSE | 169.93 | 229.40 | **35.0** | 3,724 | Small | Financial Services | 532,733 | 98,226,636 |
| 269 | 526873 | Rajasthan Securities Ltd | BSE | 39.09 | 52.70 | **34.8** | 405 | Micro | nan | 108,818 | 4,636,516 |
| 270 | SILVERTUC | Silver Touch Technologies Limited | NSE | 135.16 | 182.15 | **34.8** | 2,310 | Small | Technology | 791,487 | 148,049,158 |
| 271 | AGIIL | Agi Infra Limited | NSE | 259.10 | 354.05 | **34.8** | 4,427 | Small | Real Estate | 2,012,299 | 666,554,591 |
| 272 | HALDYNGL | Haldyn Glass Limited | NSE | 89.05 | 118.92 | **34.7** | 645 | Small | nan | 119,144 | 13,734,370 |
| 273 | APEX | Apex Frozen Foods Limited | NSE | 310.45 | 403.95 | **34.6** | 1,261 | Small | Consumer Defensive | 1,284,871 | 483,432,252 |
| 274 | PRIVISCL | Privi Speciality Chemicals Limited | NSE | 2735.30 | 3694.90 | **34.3** | 14,434 | Mid | Basic Materials | 141,461 | 421,385,199 |
| 275 | 540252 | Viram Suvarn Ltd | BSE | 7.80 | 10.70 | **34.2** | 121 | Micro | nan | 435,630 | 4,716,694 |
| 276 | 539469 | Panorama Studios International Ltd | BSE | 37.09 | 51.92 | **34.2** | 1,353 | Small | nan | 163,891 | 7,334,892 |
| 277 | RPEL | Raghav Productivity Enhancers Limited | NSE | 940.20 | 1261.50 | **34.2** | 5,799 | Mid | Basic Materials | 91,204 | 81,444,700 |
| 278 | STOVEKRAFT | Stove Kraft Limited | NSE | 589.35 | 781.85 | **33.9** | 2,584 | Small | Consumer Cyclical | 239,619 | 131,736,165 |
| 279 | ABB | ABB India Limited | NSE | 5168.50 | 6950.50 | **33.5** | 147,270 | Large | Industrials | 359,525 | 2,255,945,836 |
| 280 | WOCKPHARMA | Wockhardt Limited | NSE | 1452.40 | 1938.50 | **33.5** | 31,496 | Large | Healthcare | 1,523,042 | 2,505,540,937 |
| 281 | AUROPHARMA | Aurobindo Pharma Limited | NSE | 1207.40 | 1620.50 | **33.3** | 93,217 | Large | Healthcare | 1,395,726 | 1,835,198,348 |
| 282 | SANGHVIMOV | Sanghvi Movers Limited | NSE | 350.00 | 463.25 | **33.3** | 4,014 | Small | Industrials | 374,245 | 125,298,890 |
| 283 | NIBE | NIBE Limited | NSE | 1296.80 | 1648.00 | **33.2** | 2,459 | Small | Industrials | 127,786 | 169,807,169 |
| 284 | VIPULLTD | Vipul Limited | NSE | 11.52 | 15.34 | **33.2** | 216 | Micro | Real Estate | 574,641 | 6,752,196 |
| 285 | SKIPPER | Skipper Limited | NSE | 435.00 | 574.95 | **33.1** | 6,491 | Mid | Industrials | 573,258 | 266,389,518 |
| 286 | TAALTECH | Taal Tech Limited | NSE | 2986.00 | 3991.60 | **33.0** | 1,240 | Small | nan | 2,102 | 7,392,397 |
| 287 | SOMANYCERA | Somany Ceramics Limited | NSE | 405.65 | 537.20 | **33.0** | 2,204 | Small | Industrials | 102,601 | 48,044,967 |
| 288 | CEIGALL | Ceigall India Limited | NSE | 274.15 | 364.10 | **33.0** | 6,337 | Mid | Industrials | 464,128 | 148,654,760 |
| 289 | GROWW | Billionbrains Garage Ventures Limited | NSE | 155.53 | 206.50 | **33.0** | 129,550 | Large | Financial Services | 51,948,965 | 9,292,489,781 |
| 290 | PREMIERENE | Premier Energies Limited | NSE | 787.75 | 1046.80 | **32.9** | 47,481 | Large | Technology | 1,927,491 | 1,698,915,925 |
| 291 | LLOYDSME | Lloyds Metals And Energy Limited | NSE | 1336.20 | 1777.00 | **32.9** | 100,010 | Large | Basic Materials | 592,702 | 852,171,323 |
| 292 | CARBORUNIV | Carborundum Universal Limited | NSE | 858.60 | 1139.60 | **32.7** | 21,716 | Large | Industrials | 286,444 | 272,054,570 |
| 293 | DEEPAKFERT | Deepak Fertilizers and Petrochemicals Corporation Limited | NSE | 1252.20 | 1649.30 | **32.6** | 20,841 | Large | Basic Materials | 432,927 | 523,435,871 |
| 294 | GRINDWELL | Grindwell Norton Limited | NSE | 1581.50 | 2088.50 | **32.5** | 23,008 | Large | Industrials | 63,612 | 109,427,496 |
| 295 | 539479 | GTV Engineering Ltd | BSE | 59.28 | 75.20 | **32.2** | 352 | Micro | nan | 83,992 | 5,438,239 |
| 296 | TEJASNET | Tejas Networks Limited | NSE | 449.55 | 593.60 | **32.0** | 10,566 | Mid | Technology | 8,522,778 | 4,046,525,595 |
| 297 | ANANDRATHI | Anand Rathi Wealth Limited | NSE | 1561.80 | 2061.70 | **32.0** | 34,219 | Large | Financial Services | 560,762 | 927,340,524 |
| 298 | PIXTRANS | Pix Transmissions Limited | NSE | 1372.50 | 1810.60 | **31.9** | 2,474 | Small | Industrials | 44,160 | 75,380,200 |
| 299 | GOLDIAM | Goldiam International Limited | NSE | 356.40 | 480.40 | **31.8** | 5,427 | Mid | Consumer Cyclical | 808,627 | 316,754,975 |
| 300 | SCI | Shipping Corporation Of India Limited | NSE | 228.98 | 301.75 | **31.8** | 14,058 | Mid | Industrials | 7,145,968 | 2,034,424,759 |
| 301 | UNIPARTS | Uniparts India Limited | NSE | 497.10 | 652.45 | **31.8** | 2,943 | Small | Industrials | 137,978 | 75,977,247 |
| 302 | SUNFLAG | Sunflag Iron And Steel Company Limited | NSE | 268.40 | 353.35 | **31.6** | 6,343 | Mid | Basic Materials | 431,041 | 146,455,712 |
| 303 | SAILIFE | Sai Life Sciences Limited | NSE | 955.25 | 1257.30 | **31.6** | 26,663 | Large | Healthcare | 553,303 | 559,937,148 |
| 304 | RSWM | RSWM Limited | NSE | 148.01 | 194.76 | **31.6** | 916 | Small | Consumer Cyclical | 91,737 | 16,510,451 |
| 305 | TPLPLASTEH | TPL Plastech Limited | NSE | 66.21 | 87.16 | **31.5** | 678 | Small | Consumer Cyclical | 132,961 | 9,106,391 |
| 306 | 542669 | BMW Industries Ltd | BSE | 43.22 | 55.65 | **31.3** | 1,253 | Small | nan | 267,790 | 13,040,787 |
| 307 | COMSYN | Commercial Syn Bags Limited | NSE | 153.84 | 200.31 | **31.2** | 813 | Small | Consumer Cyclical | 138,828 | 24,051,642 |
| 308 | CARYSIL | CARYSIL LIMITED | NSE | 885.55 | 1162.10 | **31.2** | 3,303 | Small | Consumer Cyclical | 115,188 | 113,686,559 |
| 309 | MARINE | Marine Electricals (India) Limited | NSE | 217.66 | 280.30 | **31.2** | n/a | nan | Industrials | 532,060 | 121,434,738 |
| 310 | 535916 | Alacrity Securities Ltd | BSE | 52.63 | 67.73 | **31.1** | 316 | Micro | nan | 55,765 | 3,442,652 |
| 311 | SALSTEEL | S.A.L. Steel Limited | NSE | 43.12 | 56.50 | **31.0** | 621 | Small | Basic Materials | 132,041 | 6,454,935 |
| 312 | DSSL | Dynacons Systems & Solutions Limited | NSE | 974.40 | 1316.90 | **31.0** | 1,678 | Small | Technology | 178,200 | 206,197,233 |
| 313 | INNOVACAP | Innova Captab Limited | NSE | 733.20 | 957.85 | **30.9** | 5,474 | Mid | Healthcare | 76,324 | 57,384,117 |
| 314 | KTKBANK | The Karnataka Bank Limited | NSE | 201.25 | 263.40 | **30.9** | 9,952 | Mid | Financial Services | 4,505,138 | 991,127,387 |
| 315 | VADILALIND | Vadilal Industries Limited | NSE | 4897.60 | 6361.50 | **30.9** | 4,566 | Small | Consumer Defensive | 18,134 | 91,388,695 |
| 316 | 530249 | Bridge Securities Ltd | BSE | 12.47 | 16.39 | **30.7** | 64 | Micro | nan | 70,120 | 934,095 |
| 317 | BHAGCHEM | Bhagiradha Chemicals & Industries Limited | NSE | 216.98 | 283.40 | **30.6** | 3,662 | Small | Basic Materials | 185,050 | 43,597,378 |
| 318 | MMWL | Media Matrix Worldwide Limited | NSE | 10.35 | 13.44 | **30.5** | 1,499 | Small | Communication Services | 128,960 | 1,845,378 |
| 319 | SUPRIYA | Supriya Lifescience Limited | NSE | 744.75 | 978.90 | **30.4** | 7,884 | Mid | Healthcare | 293,619 | 245,526,880 |
| 320 | SEAMECLTD | Seamec Limited | NSE | 1103.70 | 1431.70 | **30.4** | 3,643 | Small | Industrials | 81,906 | 111,818,527 |
| 321 | ELECTHERM | Electrotherm (India) Limited | NSE | 930.75 | 1200.30 | **30.4** | 1,530 | Small | Basic Materials | 65,475 | 61,127,687 |
| 322 | RAYMONDREL | Raymond Realty Limited | NSE | 518.60 | 676.00 | **30.4** | 4,505 | Small | Real Estate | 673,447 | 377,648,825 |
| 323 | AVL | Aditya Vision Limited | NSE | 490.65 | 638.55 | **30.3** | 8,256 | Mid | Consumer Cyclical | 207,652 | 110,734,667 |
| 324 | SFL | Sheela Foam Limited | NSE | 588.35 | 766.55 | **30.3** | 8,362 | Mid | Consumer Cyclical | 229,518 | 139,601,620 |
| 325 | KPRMILL | K.P.R. Mill Limited | NSE | 903.05 | 1184.50 | **30.2** | 40,543 | Large | Consumer Cyclical | 594,819 | 599,990,341 |
| 326 | VIJAYA | Vijaya Diagnostic Centre Limited | NSE | 1055.90 | 1365.20 | **30.2** | 14,043 | Mid | Healthcare | 242,977 | 278,447,820 |
| 327 | AZAD | Azad Engineering Limited | NSE | 1689.40 | 2149.10 | **30.2** | 13,873 | Mid | Industrials | 312,244 | 593,455,633 |
| 328 | GULPOLY | Gulshan Polyols Limited | NSE | 149.45 | 191.78 | **30.1** | 1,195 | Small | Basic Materials | 259,096 | 47,217,335 |
| 329 | WALCHANNAG | Walchandnagar Industries Limited | NSE | 187.24 | 243.55 | **30.1** | 1,652 | Small | Industrials | 2,077,787 | 446,038,506 |
| 330 | JETFREIGHT | Jet Freight Logistics Limited | NSE | 16.90 | 21.83 | **30.0** | 101 | Micro | Industrials | 191,075 | 3,734,816 |
| 331 | AARTIIND | Aarti Industries Limited | NSE | 372.70 | 487.70 | **29.8** | 17,685 | Mid | Basic Materials | 1,123,797 | 497,253,063 |
| 332 | WELSPUNLIV | Welspun Living Limited | NSE | 131.72 | 170.93 | **29.8** | 16,363 | Mid | Consumer Cyclical | 3,605,563 | 509,044,928 |
| 333 | HCC | Hindustan Construction Company Limited | NSE | 19.80 | 24.83 | **29.5** | 6,512 | Mid | Industrials | 37,117,196 | 773,916,261 |
| 334 | DHANBANK | Dhanlaxmi Bank Limited | NSE | 26.50 | 34.09 | **29.4** | 1,342 | Small | Financial Services | 1,328,407 | 39,500,348 |
| 335 | GESHIP | The Great Eastern Shipping Company Limited | NSE | 1125.90 | 1440.40 | **29.3** | 21,169 | Large | Industrials | 768,034 | 1,124,593,706 |
| 336 | JINDALPOLY | Jindal Poly Films Limited | NSE | 476.85 | 620.45 | **29.3** | 2,720 | Small | Consumer Cyclical | 228,369 | 151,926,132 |
| 337 | NELCO | NELCO Limited | NSE | 719.10 | 929.55 | **29.3** | 2,121 | Small | Technology | 245,404 | 194,899,153 |
| 338 | SERVOTECH | Servotech Renewable Power System Limited | NSE | 78.50 | 101.37 | **29.1** | n/a | nan | Industrials | 1,325,813 | 117,905,790 |
| 339 | ASTERDM | Aster DM Healthcare Limited | NSE | 615.25 | 793.20 | **28.9** | 41,071 | Large | Healthcare | 779,533 | 527,268,375 |
| 340 | UNIVASTU | Univastu India Limited | NSE | 68.61 | 88.41 | **28.9** | n/a | nan | Industrials | 109,034 | 8,170,405 |
| 341 | ZENTEC | Zen Technologies Limited | NSE | 1369.70 | 1746.70 | **28.8** | 15,786 | Mid | Industrials | 652,559 | 1,021,170,168 |
| 342 | BALRAMCHIN | Balrampur Chini Mills Limited | NSE | 440.45 | 562.45 | **28.3** | 11,902 | Mid | Consumer Defensive | 642,546 | 319,682,040 |
| 343 | SEIL | Shanti Educational Initiatives Limited | NSE | 181.00 | 234.08 | **28.3** | 3,764 | Small | nan | 541,446 | 111,166,643 |
| 344 | KIRLOSIND | Kirloskar Industries Limited | NSE | 3203.30 | 4099.90 | **28.3** | 4,333 | Small | Industrials | 15,469 | 56,802,678 |
| 345 | 526775 | Valiant Communications Ltd-$ | BSE | 841.80 | 1080.45 | **28.2** | 1,263 | Small | nan | 15,328 | 14,893,747 |
| 346 | ORIENTHOT | Oriental Hotels Limited | NSE | 108.54 | 139.26 | **28.2** | 2,490 | Small | Consumer Cyclical | 551,580 | 67,135,547 |
| 347 | BHEL | Bharat Heavy Electricals Limited | NSE | 300.05 | 383.60 | **28.1** | 133,537 | Large | Industrials | 14,177,000 | 4,505,375,407 |
| 348 | HAPPYFORGE | Happy Forgings Limited | NSE | 1170.50 | 1499.10 | **28.1** | 14,135 | Mid | Industrials | 76,713 | 101,371,109 |
| 349 | ENRIN | Siemens Energy India Limited | NSE | 2564.50 | 3281.50 | **28.0** | 117,030 | Large | Utilities | 679,496 | 2,071,374,410 |
| 350 | SONAMLTD | SONAM LIMITED | NSE | 41.95 | 53.67 | **27.9** | n/a | nan | Consumer Cyclical | 63,920 | 3,164,775 |
| 351 | NAVINFLUOR | Navin Fluorine International Limited | NSE | 5937.50 | 7552.50 | **27.9** | 38,788 | Large | Basic Materials | 195,751 | 1,266,804,862 |
| 352 | 539682 | Mobavenue AI Tech Ltd | BSE | 238.84 | 305.15 | **27.9** | 2,359 | Small | nan | 50,873 | 13,035,800 |
| 353 | INVPRECQ | Investment & Precision Castings Limited | NSE | 672.10 | 859.80 | **27.9** | 860 | Small | nan | 7,703 | 5,364,765 |
| 354 | GINNIFILA | Ginni Filaments Limited | NSE | 43.10 | 54.65 | **27.9** | 470 | Micro | Consumer Cyclical | 128,656 | 5,418,166 |
| 355 | RAIN | Rain Industries Limited | NSE | 146.81 | 187.74 | **27.9** | 6,312 | Mid | Basic Materials | 4,949,834 | 762,484,479 |
| 356 | JBCHEPHARM | JB Chemicals & Pharmaceuticals Limited | NSE | 1840.20 | 2364.60 | **27.8** | 37,944 | Large | Healthcare | 264,715 | 539,171,425 |
| 357 | SHAILY | Shaily Engineering Plastics Limited | NSE | 2309.20 | 2901.60 | **27.7** | 13,347 | Mid | Basic Materials | 346,231 | 825,861,453 |
| 358 | DCMSIL | DCM Shriram International Limited | NSE | 52.21 | 70.00 | **27.7** | 622 | Small | Industrials | 142,099 | 11,052,954 |
| 359 | NUVAMA | Nuvama Wealth Management Limited | NSE | 1492.90 | 1887.50 | **27.7** | 34,440 | Large | Financial Services | 515,633 | 748,060,450 |
| 360 | GOLDTECH | AION-TECH SOLUTIONS LIMITED | NSE | 50.43 | 64.47 | **27.6** | 335 | Micro | Technology | 81,093 | 4,048,151 |
| 361 | LINCOLN | Lincoln Pharmaceuticals Limited | NSE | 490.55 | 620.20 | **27.6** | 1,242 | Small | Healthcare | 88,949 | 56,556,477 |
| 362 | RAMRAT | Ram Ratna Wires Limited | NSE | 305.90 | 395.60 | **27.6** | 3,691 | Small | Industrials | 173,169 | 67,292,479 |
| 363 | ESAFSFB | ESAF Small Finance Bank Limited | NSE | 27.02 | 34.15 | **27.6** | 1,755 | Small | Financial Services | 936,679 | 27,614,175 |
| 364 | ALIVUS | Alivus Life Sciences Limited | NSE | 898.60 | 1157.70 | **27.6** | 14,200 | Mid | Healthcare | 93,444 | 91,941,328 |
| 365 | DENORA | De Nora India Limited | NSE | 690.90 | 879.05 | **27.5** | 464 | Micro | Industrials | 8,276 | 6,270,487 |
| 366 | UNIMECH | Unimech Aerospace and Manufacturing Limited | NSE | 906.55 | 1155.40 | **27.3** | 5,877 | Mid | Industrials | 100,946 | 97,922,416 |
| 367 | WSTCSTPAPR | West Coast Paper Mills Limited | NSE | 413.10 | 529.40 | **27.3** | 3,494 | Small | Basic Materials | 98,078 | 46,429,493 |
| 368 | MENNPIS | Menon Pistons Limited | NSE | 57.00 | 73.45 | **27.3** | 373 | Micro | nan | 69,684 | 4,650,595 |
| 369 | BETA | Beta Drugs Limited | NSE | 1644.50 | 2090.50 | **27.2** | n/a | nan | Healthcare | 16,898 | 26,145,941 |
| 370 | ADOR | Ador Welding Limited | NSE | 1028.10 | 1317.80 | **27.1** | 2,287 | Small | Industrials | 24,940 | 26,338,086 |
| 371 | CUMMINSIND | Cummins India Limited | NSE | 4309.80 | 5478.00 | **27.1** | 151,656 | Large | Industrials | 616,052 | 2,951,467,167 |
| 372 | KOPRAN | Kopran Limited | NSE | 147.74 | 193.31 | **27.1** | 939 | Small | Healthcare | 502,886 | 81,247,870 |
| 373 | ELGIRUBCO | Elgi Rubber Company Limited | NSE | 43.51 | 55.29 | **27.1** | n/a | nan | Consumer Cyclical | 63,723 | 3,013,898 |
| 374 | NACLIND | NACL Industries Limited | NSE | 171.50 | 218.40 | **27.0** | 5,123 | Mid | Basic Materials | 705,295 | 129,141,416 |
| 375 | MCX | Multi Commodity Exchange of India Limited | NSE | 2199.00 | 2814.00 | **27.0** | 71,762 | Large | Financial Services | 3,332,041 | 8,589,829,512 |
| 376 | GANESHBE | Ganesh Benzoplast Limited | NSE | 81.36 | 103.32 | **27.0** | 743 | Small | Basic Materials | 260,498 | 24,995,927 |
| 377 | CCL | CCL Products (India) Limited | NSE | 933.65 | 1173.00 | **26.9** | 15,666 | Mid | Consumer Defensive | 333,440 | 358,312,818 |
| 378 | 544037 | Amic Forging Ltd | BSE | 1446.70 | 1832.20 | **26.6** | 1,969 | Small | nan | 46,690 | 74,358,203 |
| 379 | 526433 | ASM Technologies Ltd | BSE | 3184.60 | 4031.55 | **26.6** | 5,881 | Mid | nan | 23,428 | 72,556,401 |
| 380 | KAPSTON | Kapston Services Limited | NSE | 298.70 | 379.95 | **26.5** | n/a | nan | Industrials | 22,573 | 7,729,476 |
| 381 | ADANIPORTS | Adani Ports and Special Economic Zone Limited | NSE | 1493.00 | 1874.20 | **26.5** | 431,808 | Large | Industrials | 2,516,424 | 3,950,551,069 |
| 382 | SURYODAY | Suryoday Small Finance Bank Limited | NSE | 142.70 | 182.15 | **26.5** | 1,936 | Small | Financial Services | 401,266 | 61,541,858 |
| 383 | STARHEALTH | Star Health and Allied Insurance Company Limited | NSE | 458.80 | 580.30 | **26.5** | 34,146 | Large | Financial Services | 638,379 | 317,481,283 |
| 384 | WANBURY | Wanbury Limited | NSE | 226.58 | 286.45 | **26.4** | 1,003 | Small | Healthcare | 101,015 | 25,094,344 |
| 385 | GKSL | Gujarat Kidney And Super Speciality Limited | NSE | 102.40 | 129.83 | **26.4** | 1,024 | Small | Healthcare | 950,124 | 106,146,295 |
| 386 | DIFFNKG | Diffusion Engineers Limited | NSE | 329.60 | 416.35 | **26.3** | 1,557 | Small | Industrials | 128,967 | 40,787,128 |
| 387 | PASUPTAC | Pasupati Acrylon Limited | NSE | 49.54 | 63.71 | **26.1** | 572 | Small | Consumer Cyclical | 277,367 | 16,666,617 |
| 388 | SANSTAR | Sanstar Limited | NSE | 94.22 | 118.70 | **26.0** | 2,161 | Small | Basic Materials | 565,852 | 62,341,924 |
| 389 | SIS | SIS LIMITED | NSE | 338.30 | 425.75 | **26.0** | 6,018 | Mid | Industrials | 195,507 | 75,291,643 |
| 390 | IPCALAB | IPCA Laboratories Limited | NSE | 1413.00 | 1778.90 | **25.9** | 45,174 | Large | Healthcare | 247,522 | 378,044,470 |
| 391 | NEULANDLAB | Neuland Laboratories Limited | NSE | 15040.00 | 18944.00 | **25.8** | 24,270 | Large | Healthcare | 52,492 | 814,231,398 |
| 392 | TIPSMUSIC | Tips Music Limited | NSE | 545.45 | 684.65 | **25.7** | 8,741 | Mid | Communication Services | 352,129 | 208,654,871 |
| 393 | AAREYDRUGS | Aarey Drugs & Pharmaceuticals Limited | NSE | 67.62 | 84.87 | **25.6** | 244 | Micro | Healthcare | 172,979 | 12,750,590 |
| 394 | SMSPHARMA | SMS Pharmaceuticals Limited | NSE | 335.70 | 421.45 | **25.5** | 3,948 | Small | Healthcare | 511,290 | 183,988,912 |
| 395 | INGERRAND | Ingersoll Rand (India) Limited | NSE | 3459.50 | 4343.00 | **25.5** | 13,711 | Mid | Industrials | 18,728 | 74,099,877 |
| 396 | 539598 | Credent Global Finance Ltd | BSE | 30.30 | 37.99 | **25.4** | 233 | Micro | nan | 136,290 | 4,112,930 |
| 397 | 543916 | Hemant Surgical Industries Ltd | BSE | 289.35 | 364.75 | **25.2** | 530 | Small | nan | 27,300 | 9,011,689 |
| 398 | ATGL | Adani Total Gas Limited | NSE | 577.05 | 721.75 | **25.1** | 79,379 | Large | Utilities | 4,191,920 | 2,714,013,311 |
| 399 | KAMDHENU | Kamdhenu Limited | NSE | 24.99 | 31.25 | **25.1** | 885 | Small | Basic Materials | 1,695,129 | 40,418,225 |

🟡 = penny stock (price < ₹10), flagged not removed.

**Machine-readable file:** `FINAL_universe_25pct.csv` (399 rows).

### Known limitations (full disclosure)
- 464 universe symbols (of 4,524) returned no Yahoo history (recently renamed post-corporate-action e.g. demerged Tata Motors, thinly-traded, or delisted-from-Yahoo) — excluded from the scan, not from reality. These are predominantly illiquid BSE micro-caps.
- 11 NSE-only names have no BSE twin, so their current price rests on Yahoo alone (still passes the adjusted-return integrity check).
- Sector unavailable for 37 BSE-only micro-caps (shown as n/a).