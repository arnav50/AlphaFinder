# PHASE 1 — UNIVERSE IDENTIFICATION (NSE + BSE)
**Scan date:** 2026-06-02  |  **180-day reference:** 2025-12-04  |  **Filter:** 180-day price return ≥ 25%

## Methodology (auditable, scripted — no hand-entered prices)
1. **Universe** — NSE official `EQUITY_L.csv` (series EQ+BE) + BSE active-equity scrip master (API), excluding BSE **Z / XT / XC** surveillance groups. Dual-listed companies de-duplicated by **ISIN** (NSE listing preferred).
2. **Prices** — ~180-day daily OHLCV per symbol from Yahoo Finance chart API (sources exchange data). Return = last close ÷ **median of ±2 bars around the 180-day date** (median guards against bad single prints).
3. **Liquidity filter** — avg daily volume ≥ 50,000 shares **OR** avg daily traded value ≥ ₹50 lakh.
4. **Verification (2 sources)** — (a) returns re-derived from **split/bonus-adjusted** prices → 0 corporate-action distortions; (b) current price cross-checked against the **other exchange's live quote** (BSE-twin via ISIN / BSE live API).

## ✓ VERIFICATION CHECKPOINT
- **Total verified stocks (180d return ≥ 25%): 375**
- Exchange split (after ISIN dedup, NSE preferred): {'NSE': 359, 'BSE': 16}
- Market-cap buckets: {'Small': 156, 'Mid': 108, 'Large': 70, 'Micro': 27}  *(Large ≥₹20k cr, Mid ≥₹5k cr, Small ≥₹500 cr, Micro <₹500 cr)*
- Penny stocks (price < ₹10): **0 flagged, none removed** (per spec)
- Cross-source current-price check: 361/375 have a 2nd exchange source; **361/361 agree within 5%** (median mismatch **0.26%**)
- Excluded categories (suspended / Z / XT / XC) removed at universe stage
- Sorted by Return% descending ✓

## OUTPUT — full ranked list
Columns: Symbol | Company | Exch | Price 180d ago | Price today | Return% | MktCap(₹cr) | Cap | Sector | AvgVol(sh) | AvgVal(₹)

| # | Symbol | Company | Exch | 180d Ago | Today | Return% | MktCap₹cr | Cap | Sector | AvgVol | AvgVal₹ |
|--:|---|---|---|--:|--:|--:|--:|---|---|--:|--:|
| 1 | ARIHANT | Arihant Foundations & Housing Limited | NSE | 39.65 | 788.70 | **1889.2** | 787 | Small | Real Estate | 6,993 | 5,829,818 |
| 2 | STLTECH | Sterlite Technologies Limited | NSE | 103.64 | 561.25 | **447.6** | 27,403 | Large | Technology | 5,304,184 | 1,221,080,736 |
| 3 | SANGINITA | Sanginita Chemicals Limited | NSE | 10.21 | 44.96 | **340.4** | n/a | nan | Basic Materials | 170,248 | 3,348,350 |
| 4 | DEEDEV | DEE Development Engineers Limited | NSE | 214.90 | 709.30 | **237.9** | 4,942 | Small | Industrials | 2,176,762 | 644,833,374 |
| 5 | BLISSGVS | Bliss GVS Pharma Limited | NSE | 162.82 | 527.65 | **224.1** | 5,584 | Mid | Healthcare | 3,324,155 | 761,105,894 |
| 6 | UFBL | United Foodbrands Limited | NSE | 216.11 | 672.95 | **210.2** | 2,632 | Small | Consumer Cyclical | 256,541 | 97,979,975 |
| 7 | 540492 | Starlineps Enterprises Ltd | BSE | 3.68 | 11.36 | **208.7** | 483 | Micro | nan | 1,190,366 | 9,271,602 |
| 8 | MTARTECH | Mtar Technologies Limited | NSE | 2372.20 | 7417.00 | **206.9** | 22,817 | Large | Industrials | 888,719 | 5,155,718,695 |
| 9 | HFCL | HFCL Limited | NSE | 67.73 | 202.12 | **198.2** | 30,956 | Large | Technology | 34,962,613 | 4,044,927,330 |
| 10 | OMNI | Omnitech Engineering Limited | NSE | 204.93 | 545.35 | **186.1** | 6,740 | Mid | Industrials | 997,137 | 341,971,587 |
| 11 | SIGMAADV | SIGMA ADVANCED SYSTEMS LIMITED | NSE | 207.23 | 562.80 | **177.2** | 9,809 | Mid | Industrials | 245,027 | 76,868,838 |
| 12 | GVPIL | GE Power India Limited | NSE | 340.00 | 930.00 | **173.7** | 6,266 | Mid | Industrials | 670,484 | 355,920,630 |
| 13 | AEROFLEX | Aeroflex Industries Limited | NSE | 197.57 | 478.05 | **143.8** | 6,350 | Mid | Industrials | 2,508,763 | 737,508,340 |
| 14 | BHAGYANGR | Bhagyanagar India Limited | NSE | 161.24 | 389.80 | **141.8** | 1,246 | Small | Basic Materials | 236,658 | 50,056,858 |
| 15 | CPPLUS | Aditya Infotech Limited | NSE | 1501.40 | 3546.00 | **137.9** | 41,654 | Large | Industrials | 279,682 | 626,339,124 |
| 16 | KOVAI | Kovai Medical Center & Hospital Limited | NSE | 2576.65 | 6050.00 | **134.8** | 6,621 | Mid | Healthcare | 5,336 | 30,769,026 |
| 17 | KSHINTL | KSH International Limited | NSE | 373.55 | 855.00 | **134.0** | 5,798 | Mid | Industrials | 453,730 | 251,596,275 |
| 18 | VENUSREM | Venus Remedies Limited | NSE | 779.60 | 1770.00 | **132.0** | 2,360 | Small | Healthcare | 75,549 | 79,532,378 |
| 19 | BAJAJCON | Bajaj Consumer Care Limited | NSE | 267.35 | 618.35 | **131.3** | 8,113 | Mid | Consumer Defensive | 1,296,200 | 511,653,632 |
| 20 | ONELIFECAP | Onelife Capital Advisors Limited | NSE | 15.99 | 37.00 | **130.4** | 141 | Micro | Financial Services | 142,591 | 2,429,904 |
| 21 | INDSWFTLAB | Ind-Swift Laboratories Limited | NSE | 91.55 | 204.86 | **126.8** | 1,784 | Small | Healthcare | 864,455 | 126,468,590 |
| 22 | OMAXAUTO | Omax Autos Limited | NSE | 107.79 | 232.80 | **126.0** | 493 | Micro | Consumer Cyclical | 131,403 | 21,179,327 |
| 23 | CUPID | Cupid Limited | NSE | 83.99 | 193.39 | **125.4** | 26,006 | Large | Consumer Defensive | 30,462,273 | 2,911,962,905 |
| 24 | RPTECH | Rashi Peripherals Limited | NSE | 360.80 | 806.35 | **123.5** | 5,312 | Mid | Technology | 555,387 | 348,833,589 |
| 25 | GRWRHITECH | Garware Hi-Tech Films Limited | NSE | 3170.40 | 6971.00 | **122.6** | 16,232 | Mid | Basic Materials | 87,603 | 396,493,720 |
| 26 | NOVARTIND | Novartis India Limited | NSE | 672.25 | 1475.50 | **119.5** | 3,640 | Small | Healthcare | 28,782 | 37,572,255 |
| 27 | SHADOWFAX | Shadowfax Technologies Limited | NSE | 109.98 | 233.49 | **119.0** | 13,653 | Mid | Industrials | 2,833,255 | 437,896,469 |
| 28 | YASHO | Yasho Industries Limited | NSE | 1439.10 | 3108.00 | **118.7** | 3,746 | Small | Basic Materials | 29,533 | 53,445,871 |
| 29 | EBGNG | GNG Electronics Limited | NSE | 310.70 | 676.00 | **118.3** | 7,715 | Mid | Technology | 400,374 | 172,319,756 |
| 30 | NINSYS | NINtec Systems Limited | NSE | 398.50 | 855.00 | **115.0** | 1,581 | Small | Technology | 13,719 | 5,792,167 |
| 31 | CONFIPET | Confidence Petroleum India Limited | NSE | 37.25 | 78.01 | **113.4** | 2,586 | Small | Energy | 2,702,832 | 147,843,169 |
| 32 | ACUTAAS | Acutaas Chemicals Limited | NSE | 1749.30 | 3663.70 | **109.3** | 29,899 | Large | Basic Materials | 427,698 | 1,017,740,440 |
| 33 | NGLFINE | NGL Fine-Chem Limited | NSE | 1408.10 | 2942.90 | **109.0** | 1,815 | Small | Healthcare | 10,494 | 26,308,161 |
| 34 | RUBICON | Rubicon Research Limited | NSE | 661.40 | 1383.70 | **107.8** | 22,973 | Large | Healthcare | 380,353 | 372,562,123 |
| 35 | SAKAR | Sakar Healthcare Limited | NSE | 406.55 | 833.45 | **104.8** | n/a | nan | Healthcare | 117,440 | 73,418,765 |
| 36 | JNKINDIA | JNK India Limited | NSE | 235.95 | 481.05 | **103.9** | 2,685 | Small | Industrials | 705,711 | 270,460,838 |
| 37 | VIDYAWIRES | Vidya Wires Limited | NSE | 50.13 | 101.36 | **103.6** | 2,156 | Small | Industrials | 5,643,251 | 403,604,682 |
| 38 | INDOTECH | Indo Tech Transformers Limited | NSE | 1601.60 | 3202.00 | **103.3** | 3,398 | Small | Industrials | 48,798 | 100,288,763 |
| 39 | SPORTKING | Sportking India Limited | NSE | 87.06 | 175.83 | **102.0** | 2,228 | Small | Consumer Cyclical | 307,455 | 44,848,403 |
| 40 | AVALON | Avalon Technologies Limited | NSE | 893.75 | 1803.10 | **101.8** | 12,023 | Mid | Technology | 325,601 | 402,235,713 |
| 41 | BALAMINES | Balaji Amines Limited | NSE | 1110.00 | 2220.90 | **100.1** | 7,174 | Mid | Basic Materials | 392,164 | 572,551,197 |
| 42 | PAISALO | Paisalo Digital Limited | NSE | 36.30 | 72.40 | **99.6** | 6,575 | Mid | Financial Services | 8,314,511 | 391,272,553 |
| 43 | ATLANTAELE | Atlanta Electricals Limited | NSE | 907.35 | 1771.00 | **99.5** | 13,618 | Mid | Industrials | 159,159 | 200,281,504 |
| 44 | SETL | Standard Engineering Technology Limited | NSE | 149.83 | 296.55 | **97.9** | 5,912 | Mid | Industrials | 482,579 | 85,854,331 |
| 45 | SCHNEIDER | Schneider Electric Infrastructure Limited | NSE | 717.30 | 1411.20 | **97.2** | 33,695 | Large | Industrials | 388,255 | 370,188,784 |
| 46 | SEDEMAC | SEDEMAC Mechatronics Limited | NSE | 1451.10 | 2841.40 | **95.8** | 12,520 | Mid | Consumer Cyclical | 250,957 | 491,386,006 |
| 47 | ANTELOPUS | Antelopus Selan Energy Limited | NSE | 406.40 | 795.55 | **95.8** | 2,796 | Small | Energy | 401,483 | 226,192,722 |
| 48 | MODISONLTD | MODISON LIMITED | NSE | 160.41 | 308.15 | **93.7** | 999 | Small | Industrials | 122,046 | 27,315,558 |
| 49 | PARKHOSPS | Park Medi World Limited | NSE | 149.73 | 289.90 | **93.6** | 12,522 | Mid | Healthcare | 1,438,476 | 271,335,782 |
| 50 | PARAS | Paras Defence and Space Technologies Limited | NSE | 683.75 | 1322.40 | **93.2** | 10,646 | Mid | Industrials | 2,131,364 | 1,970,755,494 |
| 51 | VISL | Vedanta Iron and Steel Limited | NSE | 21.06 | 42.65 | **92.9** | 16,674 | Mid | Basic Materials | 83,172,054 | 2,392,679,894 |
| 52 | TIRUPATIFL | Tirupati Forge Limited | NSE | 36.27 | 69.95 | **92.9** | n/a | nan | Industrials | 553,831 | 24,883,016 |
| 53 | E2E | E2E Networks Limited | NSE | 202.75 | 388.00 | **91.4** | 7,976 | Mid | Technology | 1,471,411 | 437,733,252 |
| 54 | EMMVEE | Emmvee Photovoltaic Power Limited | NSE | 187.75 | 360.35 | **90.8** | 25,146 | Large | Technology | 4,199,557 | 1,043,876,089 |
| 55 | NITTAGELA | Nitta Gelatin India Limited | NSE | 922.65 | 1742.10 | **88.2** | 1,592 | Small | Basic Materials | 18,559 | 27,237,709 |
| 56 | SYRMA | Syrma SGS Technology Limited | NSE | 741.90 | 1394.60 | **88.0** | 26,835 | Large | Technology | 1,358,104 | 1,263,244,131 |
| 57 | KIRLOSENG | Kirloskar Oil Engines Limited | NSE | 1261.10 | 2339.10 | **87.6** | 33,992 | Large | Industrials | 631,658 | 1,047,747,222 |
| 58 | THANGAMAYL | Thangamayil Jewellery Limited | NSE | 3229.50 | 6091.50 | **86.9** | 18,916 | Mid | Consumer Cyclical | 160,031 | 661,745,677 |
| 59 | WHEELS | Wheels India Limited | NSE | 884.70 | 1623.50 | **86.8** | 3,968 | Small | Consumer Cyclical | 132,137 | 172,766,588 |
| 60 | KERNEX | Kernex Microsystems (India) Limited | NSE | 1250.80 | 2329.50 | **86.2** | 3,901 | Small | Technology | 265,405 | 371,772,215 |
| 61 | GAYAPROJ | Gayatri Projects Limited | NSE | 11.53 | 21.43 | **85.9** | 403 | Micro | Industrials | 265,781 | 5,183,807 |
| 62 | CEMPRO | Cemindia Projects Limited | NSE | 774.65 | 1431.40 | **85.8** | 24,583 | Large | Industrials | 762,702 | 671,064,310 |
| 63 | SHILPAMED | Shilpa Medicare Limited | NSE | 319.80 | 588.70 | **85.0** | 11,511 | Mid | Healthcare | 708,991 | 310,448,856 |
| 64 | WELCORP | Welspun Corp Limited | NSE | 806.35 | 1482.30 | **84.7** | 39,059 | Large | Basic Materials | 676,794 | 713,967,000 |
| 65 | IDEAFORGE | Ideaforge Technology Limited | NSE | 469.10 | 861.85 | **83.7** | 3,736 | Small | Technology | 1,080,382 | 632,270,904 |
| 66 | PARACABLES | Paramount Communications Limited | NSE | 39.40 | 71.76 | **83.2** | 2,175 | Small | Technology | 2,094,373 | 112,926,137 |
| 67 | KIRLPNU | Kirloskar Pneumatic Company Limited | NSE | 1058.60 | 1914.10 | **82.0** | 12,430 | Mid | Industrials | 145,015 | 213,558,502 |
| 68 | POWERINDIA | Hitachi Energy India Limited | NSE | 18803.00 | 34010.00 | **80.9** | 151,724 | Large | Industrials | 155,559 | 4,054,120,869 |
| 69 | SATIN | Satin Creditcare Network Limited | NSE | 144.64 | 260.88 | **80.4** | 2,872 | Small | Financial Services | 517,463 | 107,662,601 |
| 70 | APARINDS | Apar Industries Limited | NSE | 8264.50 | 14905.00 | **80.3** | 59,860 | Large | Industrials | 114,533 | 1,310,936,043 |
| 71 | ASTRAMICRO | Astra Microwave Products Limited | NSE | 963.35 | 1764.70 | **79.5** | 16,767 | Mid | Technology | 573,428 | 714,185,958 |
| 72 | IOLCP | IOL Chemicals and Pharmaceuticals Limited | NSE | 84.03 | 147.42 | **79.2** | 4,328 | Small | Healthcare | 2,089,852 | 226,376,652 |
| 73 | DATAPATTNS | Data Patterns (India) Limited | NSE | 2621.70 | 4687.00 | **78.4** | 26,226 | Large | Industrials | 964,721 | 3,436,289,143 |
| 74 | BBOX | Black Box Limited | NSE | 557.40 | 982.15 | **78.3** | 17,428 | Mid | Technology | 655,660 | 475,856,326 |
| 75 | MAYURUNIQ | Mayur Uniquoters Ltd | NSE | 514.20 | 881.95 | **78.1** | 3,829 | Small | Consumer Cyclical | 152,225 | 101,366,550 |
| 76 | AEGISLOG | Aegis Logistics Limited | NSE | 726.15 | 1292.00 | **77.9** | 45,430 | Large | Energy | 1,383,309 | 1,177,900,865 |
| 77 | SUVEN | Suven Life Sciences Limited | NSE | 164.81 | 292.95 | **77.8** | 7,701 | Mid | Healthcare | 857,106 | 198,242,892 |
| 78 | SBCL | Shivalik Bimetal Controls Limited | NSE | 433.50 | 755.75 | **77.2** | 4,361 | Small | Industrials | 294,780 | 178,558,739 |
| 79 | SPARC | Sun Pharma Advanced Research Company Limited | NSE | 135.72 | 238.47 | **76.2** | 7,740 | Mid | Healthcare | 4,524,981 | 790,225,572 |
| 80 | ARVIND | Arvind Limited | NSE | 318.35 | 559.40 | **76.0** | 14,650 | Mid | Consumer Cyclical | 716,112 | 301,903,901 |
| 81 | LOKESHMACH | Lokesh Machines Limited | NSE | 169.35 | 299.95 | **76.0** | 637 | Small | Industrials | 80,479 | 16,170,266 |
| 82 | COCKERILL | John Cockerill India Limited | NSE | 5277.35 | 9141.00 | **75.3** | 4,506 | Small | Industrials | 24,453 | 209,836,758 |
| 83 | NITINSPIN | Nitin Spinners Limited | NSE | 320.15 | 556.70 | **75.1** | 3,143 | Small | Consumer Cyclical | 366,744 | 147,359,736 |
| 84 | KOTYARK | Kotyark Industries Limited | NSE | 21.34 | 37.05 | **73.6** | 419 | Micro | Basic Materials | 356,026 | 12,333,628 |
| 85 | TDPOWERSYS | TD Power Systems Limited | NSE | 684.75 | 1189.00 | **72.7** | 18,602 | Mid | Industrials | 1,118,888 | 1,101,309,680 |
| 86 | JAYBARMARU | Jay Bharat Maruti Limited | NSE | 100.42 | 172.86 | **72.1** | 1,877 | Small | Consumer Cyclical | 798,137 | 96,178,318 |
| 87 | NEOGEN | Neogen Chemicals Limited | NSE | 1154.30 | 1978.70 | **71.4** | 5,424 | Mid | Basic Materials | 183,964 | 242,933,747 |
| 88 | SANSERA | Sansera Engineering Limited | NSE | 1871.00 | 3204.00 | **71.2** | 19,952 | Mid | Consumer Cyclical | 244,052 | 575,102,317 |
| 89 | BLUSPRING | Bluspring Enterprises Limited | NSE | 65.97 | 112.93 | **71.2** | 1,684 | Small | Industrials | 506,716 | 41,085,337 |
| 90 | 511523 | Veerhealth Care Ltd | BSE | 18.86 | 32.48 | **71.0** | 65 | Micro | nan | 99,076 | 2,211,759 |
| 91 | ZIMLAB | Zim Laboratories Limited | NSE | 70.43 | 120.05 | **70.6** | 656 | Small | Healthcare | 77,414 | 6,658,838 |
| 92 | SCPL | Sheetal Cool Products Limited | NSE | 319.75 | 545.10 | **70.5** | 573 | Small | Consumer Defensive | 25,976 | 8,925,447 |
| 93 | SKYGOLD | SKY GOLD AND DIAMONDS LIMITED | NSE | 332.65 | 568.50 | **70.4** | 8,764 | Mid | Consumer Cyclical | 1,062,811 | 445,554,456 |
| 94 | IBULLSLTD | Indiabulls Limited | NSE | 16.47 | 28.05 | **70.3** | 6,569 | Mid | Real Estate | 7,361,565 | 119,386,488 |
| 95 | CMPDI | Central Mine Planning & Design Institute Limited | NSE | 154.06 | 265.60 | **70.3** | 18,964 | Mid | Basic Materials | 5,550,669 | 1,232,857,614 |
| 96 | AEQUS | Aequs Limited | NSE | 137.37 | 234.75 | **69.9** | 15,727 | Mid | Industrials | 5,563,301 | 949,266,871 |
| 97 | INOXINDIA | INOX India Limited | NSE | 1130.80 | 1870.30 | **65.4** | 16,973 | Mid | Industrials | 209,305 | 324,909,577 |
| 98 | KRN | KRN Heat Exchanger and Refrigeration Limited | NSE | 770.15 | 1230.00 | **65.4** | 7,962 | Mid | Technology | 865,588 | 844,657,133 |
| 99 | DJML | DJ Mediaprint & Logistics Limited | NSE | 70.46 | 116.26 | **65.0** | 400 | Micro | Industrials | 199,499 | 17,987,077 |
| 100 | APOLLOPIPE | Apollo Pipes Limited | NSE | 289.75 | 483.95 | **64.9** | 2,131 | Small | Industrials | 925,104 | 377,734,539 |
| 101 | 532380 | Baba Arts Ltd-$ | BSE | 9.10 | 14.99 | **64.7** | 78 | Micro | nan | 70,509 | 929,493 |
| 102 | SGFIN | SG Finserve Limited | NSE | 416.45 | 679.00 | **64.5** | 3,788 | Small | Financial Services | 277,392 | 137,678,656 |
| 103 | 524520 | KMC Speciality Hospitals (India) Ltd | BSE | 85.48 | 140.65 | **64.5** | 2,217 | Small | nan | 131,191 | 13,192,495 |
| 104 | ACMESOLAR | Acme Solar Holdings Limited | NSE | 240.47 | 390.00 | **64.0** | 27,497 | Large | Utilities | 1,627,095 | 463,350,325 |
| 105 | AFIL | Akme Fintrade (India) Limited | NSE | 6.42 | 10.44 | **63.9** | 442 | Micro | Financial Services | 1,643,105 | 12,885,039 |
| 106 | 543787 | Macfos Ltd | BSE | 737.86 | 1188.50 | **63.4** | 1,237 | Small | nan | 9,283 | 8,814,835 |
| 107 | PRECWIRE | Precision Wires India Limited | NSE | 247.48 | 406.05 | **63.4** | 7,426 | Mid | Industrials | 987,927 | 308,838,854 |
| 108 | KPL | Kwality Pharmaceuticals Limited | NSE | 1662.60 | 2672.20 | **62.8** | 2,778 | Small | nan | 44,391 | 97,536,579 |
| 109 | ADVAIT | Advait Energy Transitions Limited | NSE | 1391.80 | 2273.80 | **62.8** | 2,485 | Small | Industrials | 59,164 | 114,811,160 |
| 110 | PREMIERPOL | Premier Polyfilm Limited | NSE | 41.91 | 68.05 | **62.4** | 712 | Small | Basic Materials | 207,668 | 11,100,800 |
| 111 | CENTUM | Centum Electronics Limited | NSE | 2266.80 | 3669.30 | **61.9** | 5,420 | Mid | Technology | 72,419 | 203,155,433 |
| 112 | SGMART | SG Mart Limited | NSE | 386.20 | 611.05 | **61.6** | 7,676 | Mid | Industrials | 281,413 | 132,566,411 |
| 113 | NRBBEARING | NRB Bearing Limited | NSE | 269.05 | 433.75 | **61.2** | 4,206 | Small | Consumer Cyclical | 540,907 | 194,562,904 |
| 114 | HONASA | Honasa Consumer Limited | NSE | 292.75 | 469.70 | **60.6** | 15,323 | Mid | Consumer Defensive | 1,798,135 | 630,893,585 |
| 115 | ELPROINTL | Elpro International Limited | NSE | 105.35 | 172.60 | **60.5** | 2,923 | Small | nan | 172,739 | 25,776,195 |
| 116 | AEROENTER | Aeroflex Enterprises Limited | NSE | 87.91 | 138.83 | **60.0** | 1,572 | Small | Basic Materials | 579,449 | 62,475,634 |
| 117 | ROSSTECH | Rossell Techsys Limited | NSE | 629.85 | 1005.25 | **59.8** | 3,773 | Small | Industrials | 211,757 | 171,938,796 |
| 118 | APOLLO | Apollo Micro Systems Limited | NSE | 271.90 | 434.00 | **59.6** | 15,505 | Mid | Industrials | 10,936,058 | 3,674,874,053 |
| 119 | THERMAX | Thermax Limited | NSE | 3025.90 | 4880.50 | **59.3** | 58,202 | Large | Industrials | 207,153 | 826,688,713 |
| 120 | MEGASTAR | Megastar Foods Limited | NSE | 233.31 | 368.00 | **59.0** | 417 | Micro | Consumer Defensive | 25,794 | 7,719,694 |
| 121 | DIVGIITTS | Divgi Torqtransfer Systems Limited | NSE | 613.50 | 973.70 | **58.7** | 2,983 | Small | Consumer Cyclical | 97,080 | 86,971,006 |
| 122 | WABAG | VA Tech Wabag Limited | NSE | 1291.60 | 2048.70 | **58.6** | 12,770 | Mid | Industrials | 423,068 | 628,974,956 |
| 123 | GRANDOAK | Grand Oak Canyons Distillery Limited | NSE | 28.90 | 45.73 | **58.2** | 2,366 | Small | nan | 60,040 | 2,229,859 |
| 124 | ADFFOODS | ADF Foods Limited | NSE | 204.09 | 322.40 | **58.0** | 3,548 | Small | Consumer Defensive | 320,495 | 83,289,782 |
| 125 | SPAL | S. P. Apparels Limited | NSE | 709.75 | 1109.50 | **58.0** | 2,786 | Small | Consumer Cyclical | 138,156 | 123,253,761 |
| 126 | J&KBANK | The Jammu & Kashmir Bank Limited | NSE | 102.36 | 161.62 | **57.9** | 17,784 | Mid | Financial Services | 4,553,825 | 561,762,663 |
| 127 | XPROINDIA | Xpro India Limited | NSE | 980.05 | 1502.40 | **57.9** | 3,522 | Small | Basic Materials | 55,256 | 61,649,354 |
| 128 | SKMEGGPROD | SKM Egg Products Export (India) Limited | NSE | 204.27 | 317.65 | **57.2** | 1,677 | Small | Consumer Defensive | 554,717 | 118,273,244 |
| 129 | RISHABH | Rishabh Instruments Limited | NSE | 434.20 | 637.00 | **56.5** | 2,450 | Small | Technology | 130,066 | 63,592,427 |
| 130 | GVT&D | GE Vernova T&D India Limited | NSE | 3093.70 | 4837.50 | **56.4** | 123,542 | Large | Industrials | 869,435 | 3,277,419,467 |
| 131 | RRKABEL | R R Kabel Limited | NSE | 1510.50 | 2361.00 | **56.3** | 26,682 | Large | Industrials | 406,875 | 740,179,092 |
| 132 | ICIL | Indo Count Industries Limited | NSE | 280.10 | 436.55 | **55.9** | 8,636 | Mid | Consumer Cyclical | 768,045 | 250,901,633 |
| 133 | DECNGOLD | Deccan Gold Mines Limited | NSE | 120.20 | 187.28 | **55.8** | 3,725 | Small | nan | 2,598,996 | 461,195,616 |
| 134 | SPECTRUM | Spectrum Electrical Industries Limited | NSE | 1218.80 | 1898.00 | **55.7** | 3,014 | Small | Industrials | 12,734 | 18,824,978 |
| 135 | CLEANMAX | Clean Max Enviro Energy Solutions Limited | NSE | 867.50 | 1334.30 | **55.6** | 15,649 | Mid | Utilities | 434,454 | 465,767,471 |
| 136 | SENORES | Senores Pharmaceuticals Limited | NSE | 865.30 | 1314.20 | **55.5** | 6,058 | Mid | Healthcare | 319,663 | 303,347,827 |
| 137 | UNIVPHOTO | Universus Photo Imagings Limited | NSE | 223.97 | 348.20 | **55.5** | 379 | Micro | Healthcare | 15,575 | 6,636,248 |
| 138 | NARMADA | Narmada Agrobase Limited | NSE | 22.50 | 34.95 | **55.3** | 133 | Micro | Basic Materials | 490,394 | 18,018,165 |
| 139 | TALBROAUTO | Talbros Automotive Components Limited | NSE | 276.30 | 426.90 | **55.3** | 2,614 | Small | Consumer Cyclical | 205,908 | 66,898,152 |
| 140 | HIRECT | Hind Rectifiers Limited | NSE | 748.20 | 1158.80 | **54.9** | 3,983 | Small | Industrials | 140,986 | 124,027,366 |
| 141 | VENUSPIPES | Venus Pipes & Tubes Limited | NSE | 1206.80 | 1797.00 | **54.8** | 3,730 | Small | Basic Materials | 78,395 | 103,376,812 |
| 142 | UTLSOLAR | Fujiyama Power Systems Limited | NSE | 224.71 | 345.60 | **54.7** | 10,565 | Mid | Technology | 685,291 | 164,099,636 |
| 143 | AYMSYNTEX | AYM Syntex Limited | NSE | 170.22 | 263.21 | **54.6** | 1,549 | Small | Consumer Cyclical | 31,315 | 6,277,903 |
| 144 | SWANDEF | Swan Defence and Heavy Industries Limited | NSE | 1530.40 | 2362.70 | **54.4** | 12,486 | Mid | Industrials | 14,263 | 26,827,769 |
| 145 | FCL | Fineotex Chemical Limited | NSE | 24.48 | 37.73 | **54.1** | 4,379 | Small | Basic Materials | 9,907,162 | 337,593,938 |
| 146 | TIMEX | Timex Group India Limited | NSE | 344.55 | 525.35 | **53.7** | 5,300 | Mid | Consumer Cyclical | 582,485 | 256,646,591 |
| 147 | SAIPARENT | Sai Parenterals Limited | NSE | 405.70 | 622.00 | **53.0** | 2,781 | Small | Healthcare | 344,209 | 177,411,003 |
| 148 | ATHERENERG | Ather Energy Limited | NSE | 741.65 | 1125.50 | **52.4** | 43,063 | Large | Consumer Cyclical | 3,316,517 | 2,806,401,464 |
| 149 | DIACABS | Diamond Power Infrastructure Limited | NSE | 137.01 | 210.30 | **52.3** | 11,074 | Mid | Industrials | 2,915,509 | 506,218,491 |
| 150 | ADANIPOWER | Adani Power Limited | NSE | 148.17 | 224.72 | **52.3** | 432,941 | Large | Utilities | 29,698,927 | 5,582,810,810 |
| 151 | JINDALSAW | Jindal Saw Limited | NSE | 170.58 | 259.55 | **52.2** | 16,634 | Mid | Basic Materials | 5,238,202 | 1,036,178,102 |
| 152 | PRADPME | Pradeep Metals Limited | NSE | 370.60 | 568.95 | **51.3** | 972 | Small | nan | 30,188 | 14,338,442 |
| 153 | KISSHT | OnEMI Technology Solutions Limited | NSE | 208.63 | 315.30 | **51.1** | 5,301 | Mid | Financial Services | 5,669,493 | 1,355,714,019 |
| 154 | VTL | Vardhman Textiles Limited | NSE | 436.10 | 657.85 | **51.1** | 19,017 | Mid | Consumer Cyclical | 515,360 | 275,180,373 |
| 155 | KRISHNADEF | Krishna Defence And Allied Industries Limited | NSE | 812.65 | 1227.40 | **51.0** | n/a | nan | Industrials | 147,401 | 156,409,288 |
| 156 | ONIDA | Onida Electronics Limited | NSE | 28.83 | 43.45 | **50.7** | 1,614 | Small | Consumer Cyclical | 1,587,550 | 56,578,411 |
| 157 | POWERICA | Powerica Limited | NSE | 390.00 | 594.50 | **50.5** | 7,524 | Mid | Industrials | 537,938 | 269,947,840 |
| 158 | ADANIGREEN | Adani Green Energy Limited | NSE | 1038.80 | 1543.50 | **50.5** | 254,538 | Large | Utilities | 3,430,059 | 3,810,205,531 |
| 159 | SOLARINDS | Solar Industries India Limited | NSE | 12336.00 | 18530.00 | **50.2** | 168,074 | Large | Basic Materials | 161,130 | 2,384,179,188 |
| 160 | FAZE3Q | Faze Three Limited | NSE | 409.25 | 614.00 | **50.0** | 1,503 | Small | Consumer Cyclical | 73,834 | 35,668,761 |
| 161 | AMAGI | Amagi Media Labs Limited | NSE | 348.25 | 548.10 | **49.9** | 11,854 | Mid | Technology | 758,232 | 298,192,744 |
| 162 | CGPOWER | CG Power and Industrial Solutions Limited | NSE | 649.10 | 964.20 | **49.4** | 151,379 | Large | Industrials | 3,520,421 | 2,622,605,003 |
| 163 | SASKEN | Sasken Technologies Limited | NSE | 1545.40 | 2273.90 | **49.4** | 3,447 | Small | Technology | 113,414 | 199,446,594 |
| 164 | NRL | Nupur Recyclers Limited | NSE | 56.80 | 84.60 | **48.9** | n/a | nan | Industrials | 73,745 | 4,597,013 |
| 165 | MARKSANS | Marksans Pharma Limited | NSE | 182.19 | 268.50 | **48.9** | 12,149 | Mid | Healthcare | 1,572,514 | 345,815,978 |
| 166 | MANINDS | Man Industries (India) Limited | NSE | 396.45 | 582.15 | **48.6** | 4,366 | Small | Basic Materials | 897,376 | 412,703,394 |
| 167 | ADANIENSOL | Adani Energy Solutions Limited | NSE | 1057.90 | 1550.50 | **48.4** | 186,055 | Large | Utilities | 2,226,402 | 2,719,416,000 |
| 168 | EXICOM | Exicom Tele-Systems Limited | NSE | 119.26 | 172.30 | **48.4** | 2,393 | Small | Industrials | 2,623,258 | 387,555,464 |
| 169 | LLOYDSENGG | LLOYDS ENGINEERING WORKS LIMITED | NSE | 56.14 | 83.14 | **48.1** | 12,110 | Mid | Industrials | 8,797,071 | 593,197,932 |
| 170 | RML | Rane (Madras) Limited | NSE | 844.20 | 1209.90 | **48.1** | 3,327 | Small | Consumer Cyclical | 44,521 | 43,754,910 |
| 171 | 543920 | CFF Fluid Control Ltd | BSE | 589.30 | 872.30 | **48.0** | 1,833 | Small | nan | 29,838 | 20,044,609 |
| 172 | QPOWER | Quality Power Electrical Equipments Limited | NSE | 831.05 | 1199.90 | **47.7** | 9,278 | Mid | Industrials | 900,769 | 836,861,913 |
| 173 | VINDHYATEL | Vindhya Telelinks Limited | NSE | 1417.60 | 2063.30 | **47.1** | 2,443 | Small | Industrials | 53,680 | 93,701,009 |
| 174 | GALAPREC | Gala Precision Engineering Limited | NSE | 785.80 | 1141.70 | **47.0** | 1,461 | Small | Industrials | 39,278 | 36,986,255 |
| 175 | NDLVENTURE | NDL Ventures Limited | NSE | 89.89 | 132.11 | **47.0** | 448 | Micro | Communication Services | 44,637 | 5,224,296 |
| 176 | SBC | SBC Exports Limited | NSE | 28.47 | 42.20 | **46.8** | 2,008 | Small | Industrials | 12,267,325 | 397,371,226 |
| 177 | GNA | GNA Axles Limited | NSE | 317.70 | 466.05 | **46.7** | 2,001 | Small | Consumer Cyclical | 193,182 | 77,298,312 |
| 178 | BSE | BSE Limited | NSE | 2666.50 | 3905.80 | **46.5** | n/a | nan | Financial Services | 4,194,465 | 13,318,246,332 |
| 179 | FINCABLES | Finolex Cables Limited | NSE | 784.45 | 1139.30 | **45.7** | 17,443 | Mid | Industrials | 460,165 | 437,825,828 |
| 180 | MOREPENLAB | Morepen Laboratories Limited | NSE | 42.03 | 59.87 | **45.6** | 3,260 | Small | Healthcare | 6,040,059 | 282,237,464 |
| 181 | STYLAMIND | Stylam Industries Limited | NSE | 2207.80 | 3213.80 | **45.6** | 5,438 | Mid | Consumer Cyclical | 59,602 | 139,111,546 |
| 182 | GAUDIUMIVF | Gaudium IVF and Women Health Limited | NSE | 80.26 | 117.49 | **45.4** | 855 | Small | Healthcare | 934,469 | 90,864,785 |
| 183 | IFCI | IFCI Limited | NSE | 53.62 | 77.11 | **45.3** | 20,762 | Large | Financial Services | 38,996,642 | 2,715,262,450 |
| 184 | MENONBE | Menon Bearings Limited | NSE | 111.97 | 162.40 | **45.0** | 916 | Small | Consumer Cyclical | 124,023 | 18,290,209 |
| 185 | PREMEXPLN | Premier Explosives Limited | NSE | 542.20 | 773.00 | **45.0** | 4,171 | Small | Basic Materials | 586,453 | 371,989,061 |
| 186 | RUBYMILLS | The Ruby Mills Limited | NSE | 223.04 | 321.35 | **44.7** | 1,098 | Small | Consumer Cyclical | 60,814 | 15,563,369 |
| 187 | BHARATFORG | Bharat Forge Limited | NSE | 1477.20 | 2133.50 | **44.7** | 102,058 | Large | Consumer Cyclical | 1,293,732 | 2,278,062,002 |
| 188 | AETHER | Aether Industries Limited | NSE | 944.10 | 1364.80 | **44.6** | 18,131 | Mid | Basic Materials | 363,612 | 387,977,588 |
| 189 | OFSS | Oracle Financial Services Software Limited | NSE | 7731.50 | 11096.00 | **44.4** | 96,659 | Large | Technology | 216,924 | 1,866,661,826 |
| 190 | PANACEABIO | Panacea Biotec Limited | NSE | 379.85 | 543.00 | **44.3** | 3,331 | Small | Healthcare | 765,876 | 349,913,751 |
| 191 | BIRLACABLE | Birla Cable Limited | NSE | 136.54 | 197.00 | **44.3** | 599 | Small | Technology | 75,541 | 12,433,345 |
| 192 | CALSOFT | California Software Company Limited | NSE | 15.73 | 22.67 | **44.1** | 80 | Micro | Technology | 116,200 | 2,234,702 |
| 193 | STEELCAS | Steelcast Limited | NSE | 210.31 | 301.60 | **43.5** | 3,045 | Small | Basic Materials | 126,787 | 34,283,355 |
| 194 | 544023 | Kalyani Cast-Tech Ltd | BSE | 489.50 | 691.50 | **43.2** | 521 | Small | nan | 11,071 | 6,235,911 |
| 195 | NELCAST | Nelcast Limited | NSE | 105.66 | 148.87 | **43.1** | 1,281 | Small | Industrials | 187,795 | 24,236,778 |
| 196 | GLAND | Gland Pharma Limited | NSE | 1715.80 | 2453.20 | **43.0** | 40,446 | Large | Healthcare | 323,247 | 673,788,006 |
| 197 | ANGELONE | Angel One Limited | NSE | 238.79 | 341.15 | **42.9** | 31,154 | Large | Financial Services | 8,907,611 | 2,490,765,478 |
| 198 | MANCREDIT | Mangal Credit and Fincorp Limited | NSE | 164.80 | 236.65 | **42.7** | 500 | Small | Financial Services | 105,473 | 20,922,113 |
| 199 | MAHABANK | Bank of Maharashtra | NSE | 63.93 | 91.14 | **42.6** | 69,962 | Large | Financial Services | 21,400,308 | 1,502,489,275 |
| 200 | NETWEB | Netweb Technologies India Limited | NSE | 3024.10 | 4431.00 | **42.4** | 25,230 | Large | Technology | 1,718,619 | 6,517,265,225 |
| 201 | PANAMAPET | Panama Petrochem Limited | NSE | 311.55 | 428.60 | **42.4** | 2,583 | Small | Energy | 313,620 | 123,977,468 |
| 202 | 543828 | Sudarshan Pharma Industries Ltd | BSE | 27.04 | 38.39 | **42.0** | 896 | Small | nan | 200,753 | 5,544,388 |
| 203 | CEIGALL | Ceigall India Limited | NSE | 274.45 | 388.65 | **42.0** | 6,774 | Mid | Industrials | 461,321 | 147,566,777 |
| 204 | AMBIKCO | Ambika Cotton Mills Limited | NSE | 1247.20 | 1763.90 | **41.9** | 1,008 | Small | Consumer Cyclical | 11,759 | 17,491,930 |
| 205 | TMB | Tamilnad Mercantile Bank Limited | NSE | 527.80 | 748.30 | **41.8** | 11,803 | Mid | Financial Services | 366,106 | 240,332,817 |
| 206 | NEPHROPLUS | Nephrocare Health Services Limited | NSE | 474.40 | 671.90 | **41.6** | 6,745 | Mid | Healthcare | 359,228 | 190,344,604 |
| 207 | DBOL | Dhampur Bio Organics Limited | NSE | 80.26 | 113.00 | **41.6** | 752 | Small | Consumer Defensive | 179,600 | 18,691,666 |
| 208 | AKUMS | Akums Drugs and Pharmaceuticals Limited | NSE | 451.85 | 632.85 | **41.5** | 9,961 | Mid | Healthcare | 254,534 | 128,529,889 |
| 209 | AMANTA | Amanta Healthcare Limited | NSE | 109.74 | 155.00 | **41.4** | 598 | Small | Healthcare | 163,866 | 21,080,939 |
| 210 | VIYASH | Viyash Scientific Limited | NSE | 210.49 | 294.25 | **41.2** | 12,881 | Mid | Healthcare | 1,554,094 | 367,038,326 |
| 211 | BANDHANBNK | Bandhan Bank Limited | NSE | 144.46 | 205.70 | **41.1** | 33,180 | Large | Financial Services | 10,253,124 | 1,796,566,899 |
| 212 | SUDEEPPHRM | Sudeep Pharma Limited | NSE | 596.80 | 841.55 | **40.9** | 9,514 | Mid | Healthcare | 639,165 | 465,703,301 |
| 213 | REFEX | Refex Industries Limited | NSE | 262.30 | 365.75 | **40.7** | 5,009 | Mid | Energy | 1,843,292 | 532,664,582 |
| 214 | SUYOG | Suyog Telematics Limited | NSE | 617.05 | 864.90 | **40.7** | 1,013 | Small | Communication Services | 35,168 | 24,446,458 |
| 215 | MBAPL | Madhya Bharat Agro Products Limited | NSE | 429.80 | 604.50 | **40.6** | n/a | nan | Basic Materials | 213,059 | 104,213,052 |
| 216 | ADANIENT | Adani Enterprises Limited | NSE | 2279.80 | 3165.00 | **40.0** | 411,997 | Large | Energy | 1,952,634 | 4,650,827,964 |
| 217 | INDOBORAX | Indo Borax & Chemicals Limited | NSE | 268.20 | 375.05 | **39.8** | 1,202 | Small | Basic Materials | 123,842 | 38,621,804 |
| 218 | HARDWYN | Hardwyn India Limited | NSE | 17.76 | 24.23 | **39.8** | 1,187 | Small | Industrials | 2,681,708 | 59,377,097 |
| 219 | 544141 | Pune E - Stock Broking Ltd | BSE | 206.00 | 287.00 | **39.8** | 449 | Micro | nan | 23,752 | 5,649,418 |
| 220 | BOROSCI | Borosil Scientific Limited | NSE | 119.58 | 167.00 | **39.7** | 1,490 | Small | Consumer Cyclical | 158,500 | 22,289,619 |
| 221 | APCOTEXIND | Apcotex Industries Limited | NSE | 370.85 | 517.80 | **39.6** | 2,679 | Small | Basic Materials | 63,772 | 30,295,503 |
| 222 | CORONA | CORONA Remedies Limited | NSE | 1443.50 | 1995.00 | **39.5** | 12,178 | Mid | Healthcare | 192,941 | 284,524,769 |
| 223 | AYE | Aye Finance Limited | NSE | 128.91 | 180.50 | **39.2** | 4,456 | Small | Financial Services | 1,858,772 | 255,671,590 |
| 224 | ABSLAMC | Aditya Birla Sun Life AMC Limited | NSE | 833.60 | 1172.70 | **39.0** | 33,922 | Large | Financial Services | 439,030 | 419,085,487 |
| 225 | BLACKROSE | Black Rose Inds. Limited | NSE | 83.25 | 115.57 | **38.7** | 587 | Small | nan | 76,793 | 8,680,902 |
| 226 | BHARATSE | Bharat Seats Limited | NSE | 177.60 | 240.37 | **38.6** | 1,510 | Small | Consumer Cyclical | 599,013 | 123,903,107 |
| 227 | SAREGAMA | Saregama India Limited | NSE | 357.95 | 490.20 | **38.6** | 9,464 | Mid | Communication Services | 1,817,971 | 733,880,525 |
| 228 | WELSPLSOL | Welspun Specialty Solutions Limited | NSE | 38.05 | 53.81 | **38.5** | 3,567 | Small | nan | 1,644,861 | 86,296,226 |
| 229 | JTLIND | JTL INDUSTRIES LIMITED | NSE | 59.82 | 81.40 | **37.9** | 3,200 | Small | Basic Materials | 5,011,651 | 342,715,099 |
| 230 | GOCLCORP | GOCL Corporation Limited | NSE | 292.65 | 401.05 | **37.8** | 1,989 | Small | Basic Materials | 201,258 | 61,453,717 |
| 231 | SALSTEEL | S.A.L. Steel Limited | NSE | 44.00 | 59.77 | **37.8** | 646 | Small | Basic Materials | 132,333 | 6,445,717 |
| 232 | ENRIN | Siemens Energy India Limited | NSE | 2546.70 | 3526.00 | **37.7** | 125,509 | Large | Utilities | 668,245 | 2,033,990,789 |
| 233 | GRINDWELL | Grindwell Norton Limited | NSE | 1557.90 | 2152.50 | **37.6** | 23,828 | Large | Industrials | 62,942 | 107,941,498 |
| 234 | CAPLIPOINT | Caplin Point Laboratories Limited | NSE | 1848.80 | 2528.00 | **37.5** | 19,216 | Mid | Healthcare | 113,993 | 226,544,615 |
| 235 | CHENNPETRO | Chennai Petroleum Corporation Limited | NSE | 827.20 | 1137.60 | **37.5** | 16,940 | Mid | Energy | 1,835,878 | 1,826,595,810 |
| 236 | RAYMOND | Raymond Limited | NSE | 436.50 | 587.45 | **37.5** | 3,916 | Small | Industrials | 588,147 | 275,482,046 |
| 237 | NAM-INDIA | Nippon Life India Asset Management Limited | NSE | 892.30 | 1221.60 | **37.2** | 77,850 | Large | Financial Services | 957,760 | 925,745,673 |
| 238 | APEX | Apex Frozen Foods Limited | NSE | 295.95 | 405.40 | **37.0** | 1,275 | Small | Consumer Defensive | 1,286,286 | 483,769,489 |
| 239 | MSTCLTD | Mstc Limited | NSE | 528.30 | 716.00 | **36.9** | 5,041 | Mid | Industrials | 593,260 | 341,480,052 |
| 240 | SIGNPOST | Signpost India Limited | NSE | 223.70 | 301.65 | **36.9** | 1,609 | Small | Communication Services | 254,250 | 71,285,766 |
| 241 | LIKHITHA | Likhitha Infrastructure Limited | NSE | 193.41 | 261.20 | **36.7** | 1,038 | Small | Energy | 101,912 | 19,562,438 |
| 242 | LLOYDSME | Lloyds Metals And Energy Limited | NSE | 1348.80 | 1825.00 | **36.6** | 102,793 | Large | Basic Materials | 591,447 | 848,782,723 |
| 243 | ASHIANA | Ashiana Housing Limited | NSE | 286.00 | 387.00 | **36.6** | 3,897 | Small | Real Estate | 139,135 | 46,829,717 |
| 244 | GHCLTEXTIL | GHCL Textiles Limited | NSE | 76.77 | 102.07 | **36.5** | 979 | Small | Consumer Cyclical | 326,291 | 28,222,227 |
| 245 | LAURUSLABS | Laurus Labs Limited | NSE | 1106.50 | 1512.00 | **36.5** | 81,705 | Large | Healthcare | 1,892,482 | 2,175,044,063 |
| 246 | GOODLUCK | Goodluck India Limited | NSE | 1074.50 | 1481.00 | **36.2** | 4,926 | Small | Basic Materials | 134,125 | 169,042,430 |
| 247 | SONACOMS | Sona BLW Precision Forgings Limited | NSE | 486.35 | 652.20 | **36.0** | 40,485 | Large | Consumer Cyclical | 1,996,139 | 1,076,250,058 |
| 248 | AGIIL | Agi Infra Limited | NSE | 273.35 | 357.20 | **36.0** | 4,475 | Small | Real Estate | 2,020,182 | 668,957,781 |
| 249 | RAMCOSYS | Ramco Systems Limited | NSE | 573.55 | 771.55 | **36.0** | 2,895 | Small | Technology | 796,245 | 536,524,801 |
| 250 | RATEGAIN | Rategain Travel Technologies Limited | NSE | 693.85 | 943.00 | **35.9** | 11,173 | Mid | Technology | 483,650 | 318,668,328 |
| 251 | HESTERBIO | Hester Biosciences Limited | NSE | 1604.20 | 2165.40 | **35.8** | 1,844 | Small | Healthcare | 8,052 | 14,428,332 |
| 252 | MACPOWER | Macpower CNC Machines Limited | NSE | 1019.40 | 1383.10 | **35.7** | n/a | nan | Industrials | 33,393 | 35,157,995 |
| 253 | MWL | Mangalam Worldwide Limited | NSE | 272.55 | 375.50 | **35.7** | 1,117 | Small | Basic Materials | 82,963 | 24,365,383 |
| 254 | KRISHANA | Krishana Phoschem Limited | NSE | 527.90 | 710.00 | **35.6** | n/a | nan | Basic Materials | 185,060 | 114,684,255 |
| 255 | TEJASNET | Tejas Networks Limited | NSE | 453.25 | 609.25 | **35.5** | 10,829 | Mid | Technology | 8,511,249 | 4,039,295,670 |
| 256 | BHEL | Bharat Heavy Electricals Limited | NSE | 299.50 | 402.35 | **35.5** | 139,996 | Large | Industrials | 14,030,766 | 4,441,074,529 |
| 257 | MARINE | Marine Electricals (India) Limited | NSE | 213.63 | 289.30 | **35.4** | n/a | nan | Industrials | 532,945 | 121,395,180 |
| 258 | KDDL | KDDL Limited | NSE | 2410.00 | 3263.10 | **35.4** | 4,010 | Small | Consumer Cyclical | 29,825 | 78,929,227 |
| 259 | SHREEJISPG | Shreeji Shipping Global Limited | NSE | 370.00 | 508.00 | **35.4** | 8,276 | Mid | Industrials | 1,141,356 | 437,474,343 |
| 260 | 540786 | Sharika Enterprises Ltd | BSE | 13.94 | 18.81 | **34.9** | 85 | Micro | nan | 72,834 | 1,052,439 |
| 261 | RPEL | Raghav Productivity Enhancers Limited | NSE | 953.05 | 1281.20 | **34.7** | 5,874 | Mid | Basic Materials | 91,572 | 81,533,660 |
| 262 | MCX | Multi Commodity Exchange of India Limited | NSE | 2216.00 | 2981.70 | **34.5** | 75,874 | Large | Financial Services | 3,313,286 | 8,524,603,264 |
| 263 | SAILIFE | Sai Life Sciences Limited | NSE | 921.70 | 1240.10 | **34.5** | 26,319 | Large | Healthcare | 553,198 | 558,849,351 |
| 264 | SOTL | Savita Oil Technologies Limited | NSE | 382.05 | 513.60 | **34.5** | 3,529 | Small | Basic Materials | 198,501 | 102,272,102 |
| 265 | 540252 | Viram Suvarn Ltd | BSE | 7.97 | 10.52 | **34.5** | 121 | Micro | nan | 434,465 | 4,703,581 |
| 266 | WOCKPHARMA | Wockhardt Limited | NSE | 1406.20 | 1945.50 | **34.5** | 31,615 | Large | Healthcare | 1,516,498 | 2,491,640,651 |
| 267 | QUESS | Quess Corp Limited | NSE | 215.04 | 286.40 | **34.4** | 4,265 | Small | Industrials | 658,451 | 147,087,529 |
| 268 | GRANULES | Granules India Limited | NSE | 615.35 | 821.45 | **34.2** | 20,394 | Large | Healthcare | 1,130,472 | 740,631,239 |
| 269 | HCC | Hindustan Construction Company Limited | NSE | 19.39 | 25.72 | **34.1** | 6,732 | Mid | Industrials | 36,962,445 | 770,079,329 |
| 270 | NIBE | NIBE Limited | NSE | 1236.80 | 1657.20 | **34.0** | 2,471 | Small | Industrials | 127,375 | 168,857,043 |
| 271 | PRIVISCL | Privi Speciality Chemicals Limited | NSE | 2780.90 | 3723.40 | **33.9** | 14,513 | Mid | Basic Materials | 141,366 | 420,854,092 |
| 272 | 539479 | GTV Engineering Ltd | BSE | 55.23 | 76.05 | **33.7** | 351 | Micro | nan | 84,320 | 5,455,550 |
| 273 | JETFREIGHT | Jet Freight Logistics Limited | NSE | 16.88 | 22.44 | **33.6** | 105 | Micro | Industrials | 191,498 | 3,734,728 |
| 274 | 526873 | Rajasthan Securities Ltd | BSE | 40.01 | 52.30 | **33.6** | 404 | Micro | nan | 109,332 | 4,655,760 |
| 275 | KIMS | Krishna Institute of Medical Sciences Limited | NSE | 632.25 | 840.25 | **33.6** | 35,281 | Large | Healthcare | 469,944 | 330,282,727 |
| 276 | DHANBANK | Dhanlaxmi Bank Limited | NSE | 24.96 | 33.38 | **33.6** | 1,321 | Small | Financial Services | 1,317,786 | 39,056,273 |
| 277 | QUADFUTURE | Quadrant Future Tek Limited | NSE | 336.95 | 450.70 | **33.5** | 1,806 | Small | Industrials | 1,274,742 | 427,195,478 |
| 278 | KTKBANK | The Karnataka Bank Limited | NSE | 200.00 | 268.85 | **33.4** | 10,191 | Mid | Financial Services | 4,499,424 | 988,921,647 |
| 279 | AVL | Aditya Vision Limited | NSE | 483.55 | 649.80 | **33.1** | 8,385 | Mid | Consumer Cyclical | 205,950 | 109,536,320 |
| 280 | DSSL | Dynacons Systems & Solutions Limited | NSE | 1005.00 | 1337.80 | **33.1** | 1,706 | Small | Technology | 178,033 | 205,908,416 |
| 281 | INNOVACAP | Innova Captab Limited | NSE | 725.15 | 972.40 | **33.0** | 5,581 | Mid | Healthcare | 76,182 | 57,213,042 |
| 282 | SOMANYCERA | Somany Ceramics Limited | NSE | 403.85 | 536.80 | **33.0** | 2,200 | Small | Industrials | 101,199 | 47,285,146 |
| 283 | UNIPARTS | Uniparts India Limited | NSE | 497.05 | 658.35 | **33.0** | 2,979 | Small | Industrials | 136,795 | 75,118,578 |
| 284 | GROWW | Billionbrains Garage Ventures Limited | NSE | 155.19 | 206.20 | **32.8** | 129,362 | Large | Financial Services | 53,405,279 | 9,501,472,610 |
| 285 | SILVERTUC | Silver Touch Technologies Limited | NSE | 124.85 | 179.35 | **32.7** | 2,286 | Small | Technology | 788,347 | 147,742,608 |
| 286 | GULPOLY | Gulshan Polyols Limited | NSE | 143.40 | 190.26 | **32.7** | 1,192 | Small | Basic Materials | 258,182 | 47,013,918 |
| 287 | GOLDTECH | AION-TECH SOLUTIONS LIMITED | NSE | 50.52 | 66.97 | **32.6** | 353 | Micro | Technology | 80,180 | 3,986,285 |
| 288 | BTTL | Bhilwara Technical Textiles Limited | NSE | 34.70 | 46.00 | **32.6** | 274 | Micro | Consumer Cyclical | 55,512 | 2,509,484 |
| 289 | BETA | Beta Drugs Limited | NSE | 1629.40 | 2159.70 | **32.5** | n/a | nan | Healthcare | 16,666 | 25,651,356 |
| 290 | VIJAYA | Vijaya Diagnostic Centre Limited | NSE | 1059.20 | 1399.10 | **32.5** | 14,385 | Mid | Healthcare | 242,169 | 277,034,174 |
| 291 | HEXAGON | Hexagon Nutrition Limited | NSE | 50.66 | 70.46 | **32.5** | 850 | Small | Consumer Defensive | 3,548,858 | 208,317,008 |
| 292 | ABB | ABB India Limited | NSE | 5205.50 | 6850.50 | **32.3** | 145,178 | Large | Industrials | 357,532 | 2,240,611,198 |
| 293 | NAHARSPING | Nahar Spinning Mills Limited | NSE | 194.57 | 257.45 | **32.3** | 923 | Small | Consumer Cyclical | 27,935 | 5,739,000 |
| 294 | HSCL | Himadri Speciality Chemical Limited | NSE | 494.00 | 645.50 | **32.3** | 32,596 | Large | Basic Materials | 5,555,674 | 3,302,325,252 |
| 295 | ZENTEC | Zen Technologies Limited | NSE | 1362.40 | 1802.00 | **32.3** | 16,270 | Mid | Industrials | 658,620 | 1,028,491,391 |
| 296 | AVADHSUGAR | Avadh Sugar & Energy Limited | NSE | 373.60 | 489.00 | **32.2** | 999 | Small | Consumer Defensive | 72,301 | 30,233,048 |
| 297 | CARBORUNIV | Carborundum Universal Limited | NSE | 859.55 | 1134.50 | **32.1** | 21,637 | Large | Industrials | 287,515 | 272,861,766 |
| 298 | STEELXIND | STEEL EXCHANGE INDIA LIMITED | NSE | 9.37 | 12.38 | **32.1** | 1,583 | Small | Basic Materials | 2,622,372 | 27,918,860 |
| 299 | STOVEKRAFT | Stove Kraft Limited | NSE | 592.90 | 763.35 | **32.0** | 2,531 | Small | Consumer Cyclical | 239,892 | 131,550,254 |
| 300 | SCI | Shipping Corporation Of India Limited | NSE | 235.08 | 302.65 | **31.9** | 14,118 | Mid | Industrials | 7,156,949 | 2,036,641,534 |
| 301 | RAMRAT | Ram Ratna Wires Limited | NSE | 311.35 | 407.00 | **31.8** | 3,805 | Small | Industrials | 173,023 | 67,170,259 |
| 302 | BHAGCHEM | Bhagiradha Chemicals & Industries Limited | NSE | 200.62 | 285.80 | **31.7** | 3,696 | Small | Basic Materials | 185,515 | 43,666,828 |
| 303 | SUPRIYA | Supriya Lifescience Limited | NSE | 750.55 | 988.50 | **31.7** | 7,953 | Mid | Healthcare | 293,493 | 245,065,743 |
| 304 | CARYSIL | CARYSIL LIMITED | NSE | 918.00 | 1183.50 | **31.7** | 3,344 | Small | Consumer Cyclical | 114,984 | 113,373,070 |
| 305 | MMWL | Media Matrix Worldwide Limited | NSE | 10.35 | 13.55 | **31.6** | 1,529 | Small | Communication Services | 130,105 | 1,862,929 |
| 306 | HAPPYFORGE | Happy Forgings Limited | NSE | 1185.80 | 1538.00 | **31.4** | 14,509 | Mid | Industrials | 76,769 | 101,256,791 |
| 307 | HALDYNGL | Haldyn Glass Limited | NSE | 89.05 | 115.77 | **31.1** | 617 | Small | nan | 121,063 | 13,954,062 |
| 308 | UNIVCABLES | Universal Cables Limited | NSE | 956.90 | 1230.00 | **30.8** | 4,261 | Small | Industrials | 202,841 | 204,113,954 |
| 309 | UNIMECH | Unimech Aerospace and Manufacturing Limited | NSE | 911.05 | 1187.80 | **30.8** | 6,029 | Mid | Industrials | 100,065 | 96,865,496 |
| 310 | FUSION | Fusion Finance Limited | NSE | 161.95 | 211.72 | **30.7** | 3,429 | Small | Financial Services | 504,497 | 91,761,594 |
| 311 | RSWM | RSWM Limited | NSE | 149.86 | 194.00 | **30.7** | 923 | Small | Consumer Cyclical | 91,756 | 16,509,433 |
| 312 | VIPULLTD | Vipul Limited | NSE | 11.77 | 15.38 | **30.7** | 215 | Micro | Real Estate | 503,304 | 5,650,234 |
| 313 | PIXTRANS | Pix Transmissions Limited | NSE | 1404.30 | 1828.90 | **30.5** | 2,478 | Small | Industrials | 43,894 | 74,843,589 |
| 314 | WALCHANNAG | Walchandnagar Industries Limited | NSE | 187.96 | 245.30 | **30.5** | 1,671 | Small | Industrials | 2,069,742 | 443,929,144 |
| 315 | SHRIPISTON | SPR Auto Technologies Limited | NSE | 3297.20 | 4300.00 | **30.4** | 18,941 | Mid | Consumer Cyclical | 121,255 | 384,114,400 |
| 316 | SKIPPER | Skipper Limited | NSE | 452.85 | 566.90 | **30.3** | 6,406 | Mid | Industrials | 574,409 | 266,361,930 |
| 317 | GCSL | Gretex Corporate Services Limited | NSE | 340.05 | 442.55 | **30.1** | 1,070 | Small | Financial Services | 168,325 | 67,114,502 |
| 318 | UNIVASTU | Univastu India Limited | NSE | 69.10 | 89.23 | **29.9** | n/a | nan | Industrials | 108,704 | 8,136,433 |
| 319 | ORIENTHOT | Oriental Hotels Limited | NSE | 107.93 | 140.91 | **29.8** | 2,517 | Small | Consumer Cyclical | 549,542 | 66,822,078 |
| 320 | KSR | KSR Footwear Limited | NSE | 23.83 | 30.90 | **29.7** | 56 | Micro | Consumer Cyclical | 91,144 | 2,305,065 |
| 321 | DCMSIL | DCM Shriram International Limited | NSE | 52.21 | 71.06 | **29.6** | 611 | Small | Industrials | 143,544 | 11,166,239 |
| 322 | SFL | Sheela Foam Limited | NSE | 593.35 | 762.20 | **29.6** | 8,299 | Mid | Consumer Cyclical | 231,919 | 140,971,030 |
| 323 | JINDALPOLY | Jindal Poly Films Limited | NSE | 479.95 | 621.00 | **29.4** | 2,718 | Small | Consumer Cyclical | 228,198 | 151,816,433 |
| 324 | SINDHUTRAD | Sindhu Trade Links Limited | NSE | 20.11 | 25.79 | **29.3** | 3,986 | Small | Industrials | 2,076,683 | 50,015,317 |
| 325 | LINCOLN | Lincoln Pharmaceuticals Limited | NSE | 497.15 | 625.25 | **29.2** | 1,251 | Small | Healthcare | 89,030 | 56,578,078 |
| 326 | DEEPAKFERT | Deepak Fertilizers and Petrochemicals Corporation Limited | NSE | 1261.80 | 1617.00 | **29.1** | 20,451 | Large | Basic Materials | 430,478 | 519,139,713 |
| 327 | WSTCSTPAPR | West Coast Paper Mills Limited | NSE | 419.90 | 533.30 | **29.1** | 3,526 | Small | Basic Materials | 97,520 | 46,121,435 |
| 328 | NELCO | NELCO Limited | NSE | 729.60 | 931.60 | **29.0** | 2,124 | Small | Technology | 244,043 | 193,617,720 |
| 329 | SONAMLTD | SONAM LIMITED | NSE | 41.99 | 54.16 | **29.0** | n/a | nan | Consumer Cyclical | 64,124 | 3,172,141 |
| 330 | KPRMILL | K.P.R. Mill Limited | NSE | 909.75 | 1173.40 | **29.0** | 40,156 | Large | Consumer Cyclical | 597,550 | 602,334,121 |
| 331 | RAIN | Rain Industries Limited | NSE | 146.42 | 189.19 | **28.9** | 6,362 | Mid | Basic Materials | 4,951,166 | 761,210,693 |
| 332 | AUROPHARMA | Aurobindo Pharma Limited | NSE | 1215.40 | 1556.80 | **28.9** | 89,523 | Large | Healthcare | 1,392,580 | 1,825,017,963 |
| 333 | 526433 | ASM Technologies Ltd | BSE | 3185.45 | 4103.75 | **28.8** | 6,032 | Mid | nan | 23,411 | 72,318,817 |
| 334 | ASTERDM | Aster DM Healthcare Limited | NSE | 613.90 | 792.05 | **28.7** | 41,009 | Large | Healthcare | 776,968 | 525,119,075 |
| 335 | ALIVUS | Alivus Life Sciences Limited | NSE | 913.00 | 1168.30 | **28.7** | 14,311 | Mid | Healthcare | 92,860 | 91,220,080 |
| 336 | 543916 | Hemant Surgical Industries Ltd | BSE | 291.40 | 375.00 | **28.7** | 535 | Small | nan | 27,348 | 9,022,398 |
| 337 | STARHEALTH | Star Health and Allied Insurance Company Limited | NSE | 459.75 | 589.90 | **28.6** | 34,658 | Large | Financial Services | 652,068 | 324,404,062 |
| 338 | SHAILY | Shaily Engineering Plastics Limited | NSE | 2239.90 | 2907.50 | **28.6** | 13,431 | Mid | Basic Materials | 345,508 | 823,247,419 |
| 339 | SERVOTECH | Servotech Renewable Power System Limited | NSE | 79.98 | 101.00 | **28.6** | n/a | nan | Industrials | 1,322,601 | 117,579,126 |
| 340 | EMCURE | Emcure Pharmaceuticals Limited | NSE | 1430.90 | 1838.90 | **28.5** | 34,929 | Large | Healthcare | 251,760 | 394,476,851 |
| 341 | SMSPHARMA | SMS Pharmaceuticals Limited | NSE | 326.25 | 419.10 | **28.5** | 3,914 | Small | Healthcare | 510,180 | 183,425,485 |
| 342 | AARTIIND | Aarti Industries Limited | NSE | 376.95 | 481.80 | **28.5** | 17,454 | Mid | Basic Materials | 1,120,837 | 495,607,852 |
| 343 | BLSE | BLS E-Services Limited | NSE | 199.35 | 256.02 | **28.4** | 2,323 | Small | Industrials | 435,032 | 81,986,624 |
| 344 | SURYODAY | Suryoday Small Finance Bank Limited | NSE | 143.96 | 183.12 | **28.3** | 1,954 | Small | Financial Services | 395,766 | 60,481,458 |
| 345 | GESHIP | The Great Eastern Shipping Company Limited | NSE | 1114.00 | 1429.50 | **28.2** | 20,954 | Large | Industrials | 766,289 | 1,121,826,021 |
| 346 | SANGHVIMOV | Sanghvi Movers Limited | NSE | 349.95 | 445.70 | **28.2** | 3,855 | Small | Industrials | 372,537 | 124,274,836 |
| 347 | INGERRAND | Ingersoll Rand (India) Limited | NSE | 3507.20 | 4469.00 | **28.2** | 14,149 | Mid | Industrials | 18,897 | 74,726,573 |
| 348 | AAREYDRUGS | Aarey Drugs & Pharmaceuticals Limited | NSE | 66.34 | 86.60 | **28.2** | 254 | Micro | Healthcare | 173,180 | 12,770,324 |
| 349 | BALRAMCHIN | Balrampur Chini Mills Limited | NSE | 438.55 | 561.85 | **28.1** | 11,869 | Mid | Consumer Defensive | 647,010 | 321,427,037 |
| 350 | SEAMECLTD | Seamec Limited | NSE | 1088.10 | 1405.50 | **28.0** | 3,581 | Small | Industrials | 81,966 | 111,737,907 |
| 351 | ATGL | Adani Total Gas Limited | NSE | 587.60 | 738.80 | **28.0** | 81,243 | Large | Utilities | 4,186,235 | 2,709,339,949 |
| 352 | BELRISE | Belrise Industries Limited | NSE | 185.05 | 236.04 | **27.8** | 20,966 | Large | Consumer Cyclical | 6,215,197 | 1,167,341,584 |
| 353 | PGIL | Pearl Global Industries Limited | NSE | 1653.70 | 2074.50 | **27.8** | 9,599 | Mid | Consumer Cyclical | 125,620 | 215,587,474 |
| 354 | GKSL | Gujarat Kidney And Super Speciality Limited | NSE | 102.71 | 131.19 | **27.7** | 1,033 | Small | Healthcare | 964,164 | 107,695,523 |
| 355 | CCL | CCL Products (India) Limited | NSE | 915.70 | 1179.80 | **27.7** | 15,765 | Mid | Consumer Defensive | 338,537 | 363,539,158 |
| 356 | 530249 | Bridge Securities Ltd | BSE | 12.60 | 15.98 | **27.5** | 65 | Micro | nan | 69,904 | 926,028 |
| 357 | ANANDRATHI | Anand Rathi Wealth Limited | NSE | 1539.70 | 1981.20 | **27.3** | 32,884 | Large | Financial Services | 556,562 | 918,073,886 |
| 358 | ICICIAMC | ICICI Prudential Asset Management Company Limited | NSE | 2662.20 | 3388.80 | **27.3** | 167,670 | Large | Financial Services | 791,383 | 2,292,280,925 |
| 359 | NAVINFLUOR | Navin Fluorine International Limited | NSE | 5903.00 | 7535.00 | **27.3** | 38,613 | Large | Basic Materials | 194,382 | 1,255,448,112 |
| 360 | INVPRECQ | Investment & Precision Castings Limited | NSE | 672.10 | 855.15 | **27.2** | 851 | Small | nan | 7,419 | 5,097,327 |
| 361 | SUNFLAG | Sunflag Iron And Steel Company Limited | NSE | 273.45 | 345.05 | **27.0** | 6,227 | Mid | Basic Materials | 431,299 | 146,400,000 |
| 362 | PIRAMALFIN | Piramal Finance Limited | NSE | 1712.50 | 2174.90 | **27.0** | 49,325 | Large | Financial Services | 403,702 | 749,062,897 |
| 363 | ESAFSFB | ESAF Small Finance Bank Limited | NSE | 26.77 | 33.85 | **26.4** | 1,752 | Small | Financial Services | 928,795 | 27,342,732 |
| 364 | RADICO | Radico Khaitan Limited | NSE | 3094.20 | 3954.20 | **26.4** | 52,965 | Large | Consumer Defensive | 440,266 | 1,380,381,564 |
| 365 | GANESHBE | Ganesh Benzoplast Limited | NSE | 81.69 | 102.80 | **26.4** | 740 | Small | Basic Materials | 259,954 | 24,911,565 |
| 366 | ADANIPORTS | Adani Ports and Special Economic Zone Limited | NSE | 1489.50 | 1870.80 | **26.3** | 431,290 | Large | Industrials | 2,514,137 | 3,940,678,546 |
| 367 | DIFFNKG | Diffusion Engineers Limited | NSE | 336.25 | 422.50 | **26.2** | 1,589 | Small | Industrials | 128,944 | 40,680,116 |
| 368 | SIS | SIS LIMITED | NSE | 339.30 | 425.85 | **26.0** | 6,010 | Mid | Industrials | 195,270 | 75,156,964 |
| 369 | JBCHEPHARM | JB Chemicals & Pharmaceuticals Limited | NSE | 1850.40 | 2313.00 | **25.7** | 37,097 | Large | Healthcare | 264,164 | 537,664,676 |
| 370 | DELHIVERY | Delhivery Limited | NSE | 404.50 | 508.00 | **25.6** | 38,045 | Large | Industrials | 2,656,614 | 1,182,116,960 |
| 371 | VADILALIND | Vadilal Industries Limited | NSE | 4861.70 | 6151.00 | **25.6** | 4,452 | Small | Consumer Defensive | 18,061 | 90,896,524 |
| 372 | NACLIND | NACL Industries Limited | NSE | 167.94 | 215.31 | **25.6** | 5,027 | Mid | Basic Materials | 690,863 | 125,981,635 |
| 373 | AZAD | Azad Engineering Limited | NSE | 1652.80 | 2075.00 | **25.5** | 13,368 | Mid | Industrials | 305,870 | 579,598,820 |
| 374 | KSB | Ksb Limited | NSE | 753.05 | 945.20 | **25.5** | 16,463 | Mid | Industrials | 324,533 | 264,879,985 |
| 375 | AERONEU | Aeroflex Neu Limited | NSE | 74.95 | 94.00 | **25.5** | 244 | Micro | Consumer Cyclical | 51,636 | 4,233,541 |

🟡 = penny stock (price < ₹10), flagged not removed.

**Machine-readable file:** `FINAL_universe_25pct.csv` (375 rows).

### Known limitations (full disclosure)
- 464 universe symbols (of 4,524) returned no Yahoo history (recently renamed post-corporate-action e.g. demerged Tata Motors, thinly-traded, or delisted-from-Yahoo) — excluded from the scan, not from reality. These are predominantly illiquid BSE micro-caps.
- 11 NSE-only names have no BSE twin, so their current price rests on Yahoo alone (still passes the adjusted-return integrity check).
- Sector unavailable for 37 BSE-only micro-caps (shown as n/a).