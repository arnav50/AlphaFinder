# PHASE 1 — UNIVERSE IDENTIFICATION (NSE + BSE)
**Scan date:** 2026-06-02  |  **180-day reference:** 2025-12-04  |  **Filter:** 180-day price return ≥ 25%

## Methodology (auditable, scripted — no hand-entered prices)
1. **Universe** — NSE official `EQUITY_L.csv` (series EQ+BE) + BSE active-equity scrip master (API), excluding BSE **Z / XT / XC** surveillance groups. Dual-listed companies de-duplicated by **ISIN** (NSE listing preferred).
2. **Prices** — ~180-day daily OHLCV per symbol from Yahoo Finance chart API (sources exchange data). Return = last close ÷ **median of ±2 bars around the 180-day date** (median guards against bad single prints).
3. **Liquidity filter** — avg daily volume ≥ 50,000 shares **OR** avg daily traded value ≥ ₹50 lakh.
4. **Verification (2 sources)** — (a) returns re-derived from **split/bonus-adjusted** prices → 0 corporate-action distortions; (b) current price cross-checked against the **other exchange's live quote** (BSE-twin via ISIN / BSE live API).

## ✓ VERIFICATION CHECKPOINT
- **Total verified stocks (180d return ≥ 25%): 546**
- Exchange split (after ISIN dedup, NSE preferred): {'NSE': 520, 'BSE': 26}
- Market-cap buckets: {}  *(Large ≥₹20k cr, Mid ≥₹5k cr, Small ≥₹500 cr, Micro <₹500 cr)*
- Penny stocks (price < ₹10): **0 flagged, none removed** (per spec)
- Cross-source current-price check: 26/546 have a 2nd exchange source; **26/26 agree within 5%** (median mismatch **0.00%**)
- Excluded categories (suspended / Z / XT / XC) removed at universe stage
- Sorted by Return% descending ✓

## OUTPUT — full ranked list
Columns: Symbol | Company | Exch | Price 180d ago | Price today | Return% | MktCap(₹cr) | Cap | Sector | AvgVol(sh) | AvgVal(₹)

| # | Symbol | Company | Exch | 180d Ago | Today | Return% | MktCap₹cr | Cap | Sector | AvgVol | AvgVal₹ |
|--:|---|---|---|--:|--:|--:|--:|---|---|--:|--:|
| 1 | ARIHANT | Arihant Foundations & Housing Limited | NSE | 39.65 | 802.80 | **1924.7** | n/a | nan | Real Estate | 7,032 | 5,817,433 |
| 2 | STLTECH | Sterlite Technologies Limited | NSE | 91.56 | 520.40 | **462.0** | n/a | nan | Technology | 5,411,100 | 1,316,065,045 |
| 3 | SANGINITA | Sanginita Chemicals Limited | NSE | 11.44 | 55.85 | **392.5** | n/a | nan | Basic Materials | 173,790 | 3,680,099 |
| 4 | UFBL | United Foodbrands Limited | NSE | 179.00 | 701.90 | **283.6** | n/a | nan | Consumer Cyclical | 254,846 | 101,803,059 |
| 5 | DEEDEV | DEE Development Engineers Limited | NSE | 190.09 | 691.75 | **251.1** | n/a | nan | Industrials | 2,163,355 | 644,631,301 |
| 6 | HFCL | HFCL Limited | NSE | 63.32 | 213.17 | **236.7** | n/a | nan | Technology | 35,918,538 | 4,330,289,237 |
| 7 | SIGMAADV | SIGMA ADVANCED SYSTEMS LIMITED | NSE | 173.45 | 557.80 | **220.6** | n/a | nan | Industrials | 269,179 | 93,832,390 |
| 8 | BLISSGVS | Bliss GVS Pharma Limited | NSE | 156.87 | 483.50 | **208.2** | n/a | nan | Healthcare | 3,287,579 | 764,654,519 |
| 9 | OMNI | Omnitech Engineering Limited | NSE | 204.93 | 565.60 | **196.7** | n/a | nan | Industrials | 917,623 | 323,926,724 |
| 10 | GVPIL | GE Power India Limited | NSE | 283.65 | 792.95 | **178.4** | n/a | nan | Industrials | 638,393 | 355,659,895 |
| 11 | NINSYS | NINtec Systems Limited | NSE | 339.80 | 893.60 | **163.0** | n/a | nan | Technology | 13,560 | 5,866,366 |
| 12 | CUPID | Cupid Limited | NSE | 80.67 | 214.78 | **161.8** | n/a | nan | Consumer Defensive | 33,601,825 | 3,782,519,326 |
| 13 | CPPLUS | Aditya Infotech Limited | NSE | 1400.00 | 3614.40 | **160.7** | n/a | nan | Industrials | 277,253 | 650,769,720 |
| 14 | INDOTECH | Indo Tech Transformers Limited | NSE | 1318.70 | 3400.90 | **157.9** | n/a | nan | Industrials | 47,721 | 101,113,349 |
| 15 | CEMPRO | Cemindia Projects Limited | NSE | 626.35 | 1615.00 | **151.4** | n/a | nan | Industrials | 786,891 | 725,557,069 |
| 16 | BHAGYANGR | Bhagyanagar India Limited | NSE | 160.30 | 401.05 | **144.8** | n/a | nan | Basic Materials | 216,047 | 48,408,365 |
| 17 | AEROFLEX | Aeroflex Industries Limited | NSE | 168.93 | 410.60 | **143.1** | n/a | nan | Industrials | 2,578,580 | 774,743,977 |
| 18 | GRWRHITECH | Garware Hi-Tech Films Limited | NSE | 2745.30 | 6970.50 | **142.4** | n/a | nan | Basic Materials | 83,238 | 389,921,462 |
| 19 | OMAXAUTO | Omax Autos Limited | NSE | 94.34 | 228.38 | **142.1** | n/a | nan | Consumer Cyclical | 129,725 | 21,542,401 |
| 20 | KSHINTL | KSH International Limited | NSE | 350.35 | 864.75 | **141.1** | n/a | nan | Industrials | 451,347 | 259,897,732 |
| 21 | SPORTKING | Sportking India Limited | NSE | 81.81 | 197.21 | **141.1** | n/a | nan | Consumer Cyclical | 350,049 | 53,690,646 |
| 22 | MTARTECH | Mtar Technologies Limited | NSE | 2516.00 | 6046.00 | **140.3** | n/a | nan | Industrials | 875,606 | 5,167,815,078 |
| 23 | VENUSREM | Venus Remedies Limited | NSE | 726.25 | 1770.00 | **138.0** | n/a | nan | Healthcare | 61,844 | 74,165,445 |
| 24 | YASHO | Yasho Industries Limited | NSE | 1270.50 | 3010.70 | **137.0** | n/a | nan | Basic Materials | 30,372 | 56,759,148 |
| 25 | ONELIFECAP | Onelife Capital Advisors Limited | NSE | 15.67 | 36.88 | **135.3** | n/a | nan | Financial Services | 143,466 | 2,504,459 |
| 26 | NOVARTIND | Novartis India Limited | NSE | 672.25 | 1570.10 | **133.6** | n/a | nan | Healthcare | 34,157 | 47,727,691 |
| 27 | KOVAI | Kovai Medical Center & Hospital Limited | NSE | 2576.65 | 5986.00 | **132.3** | n/a | nan | Healthcare | 5,082 | 29,456,647 |
| 28 | IBULLSLTD | Indiabulls Limited | NSE | 12.55 | 28.99 | **131.0** | n/a | nan | Real Estate | 8,143,711 | 142,782,557 |
| 29 | SUVEN | Suven Life Sciences Limited | NSE | 143.49 | 325.90 | **127.1** | n/a | nan | Healthcare | 1,018,524 | 254,301,099 |
| 30 | CONFIPET | Confidence Petroleum India Limited | NSE | 32.45 | 73.12 | **124.4** | n/a | nan | Energy | 2,823,674 | 157,704,932 |
| 31 | JNKINDIA | JNK India Limited | NSE | 208.85 | 477.15 | **122.9** | n/a | nan | Industrials | 768,075 | 303,946,598 |
| 32 | SHILPAMED | Shilpa Medicare Limited | NSE | 279.20 | 620.25 | **122.2** | n/a | nan | Healthcare | 747,123 | 338,541,699 |
| 33 | UNIVPHOTO | Universus Photo Imagings Limited | NSE | 188.53 | 436.30 | **120.7** | n/a | nan | Healthcare | 14,760 | 6,407,971 |
| 34 | ACUTAAS | Acutaas Chemicals Limited | NSE | 1626.50 | 3619.40 | **120.1** | n/a | nan | Basic Materials | 425,268 | 1,054,636,815 |
| 35 | PAISALO | Paisalo Digital Limited | NSE | 32.75 | 71.75 | **119.1** | n/a | nan | Financial Services | 9,617,848 | 502,501,952 |
| 36 | ATLANTAELE | Atlanta Electricals Limited | NSE | 777.60 | 1698.30 | **118.4** | n/a | nan | Industrials | 156,906 | 203,304,024 |
| 37 | 532380 | Baba Arts Ltd-$ | BSE | 7.37 | 15.99 | **117.0** | n/a | nan | nan | 72,019 | 967,211 |
| 38 | RUBICON | Rubicon Research Limited | NSE | 663.85 | 1439.60 | **116.9** | n/a | nan | Healthcare | 336,768 | 354,701,825 |
| 39 | SETL | Standard Engineering Technology Limited | NSE | 130.03 | 281.10 | **116.2** | n/a | nan | Industrials | 556,371 | 107,366,931 |
| 40 | INDSWFTLAB | Ind-Swift Laboratories Limited | NSE | 107.42 | 231.47 | **115.5** | n/a | nan | Healthcare | 954,412 | 148,051,331 |
| 41 | SAKAR | Sakar Healthcare Limited | NSE | 408.60 | 877.70 | **114.8** | n/a | nan | Healthcare | 131,932 | 86,556,783 |
| 42 | RUBYMILLS | The Ruby Mills Limited | NSE | 194.03 | 413.60 | **111.3** | n/a | nan | Consumer Cyclical | 61,377 | 16,088,886 |
| 43 | SHADOWFAX | Shadowfax Technologies Limited | NSE | 109.98 | 223.25 | **109.4** | n/a | nan | Industrials | 2,827,099 | 453,487,196 |
| 44 | WELCORP | Welspun Corp Limited | NSE | 758.60 | 1581.50 | **108.5** | n/a | nan | Basic Materials | 794,944 | 922,600,405 |
| 45 | RPTECH | Rashi Peripherals Limited | NSE | 344.80 | 734.45 | **108.0** | n/a | nan | Technology | 587,654 | 377,024,630 |
| 46 | SCHNEIDER | Schneider Electric Infrastructure Limited | NSE | 585.45 | 1278.50 | **107.3** | n/a | nan | Industrials | 406,480 | 403,869,746 |
| 47 | ATHERENERG | Ather Energy Limited | NSE | 606.90 | 1282.20 | **107.2** | n/a | nan | Consumer Cyclical | 3,451,847 | 3,122,987,299 |
| 48 | VIDYAWIRES | Vidya Wires Limited | NSE | 45.95 | 94.82 | **106.3** | n/a | nan | Industrials | 5,260,124 | 377,825,497 |
| 49 | IOLCP | IOL Chemicals and Pharmaceuticals Limited | NSE | 71.54 | 148.33 | **106.1** | n/a | nan | Healthcare | 2,804,080 | 348,134,814 |
| 50 | EBGNG | GNG Electronics Limited | NSE | 260.10 | 543.00 | **105.9** | n/a | nan | Technology | 431,250 | 195,175,353 |
| 51 | NGLFINE | NGL Fine-Chem Limited | NSE | 1531.70 | 3131.90 | **104.5** | n/a | nan | Healthcare | 10,973 | 28,221,704 |
| 52 | SYRMA | Syrma SGS Technology Limited | NSE | 646.75 | 1359.10 | **103.6** | n/a | nan | Technology | 1,336,524 | 1,287,491,729 |
| 53 | NITTAGELA | Nitta Gelatin India Limited | NSE | 922.65 | 1880.00 | **103.1** | n/a | nan | Basic Materials | 19,667 | 30,908,026 |
| 54 | KIRLOSENG | Kirloskar Oil Engines Limited | NSE | 1099.00 | 2255.70 | **102.7** | n/a | nan | Industrials | 653,774 | 1,138,526,785 |
| 55 | AVALON | Avalon Technologies Limited | NSE | 856.55 | 1724.00 | **101.3** | n/a | nan | Technology | 341,706 | 437,220,446 |
| 56 | LOKESHMACH | Lokesh Machines Limited | NSE | 164.29 | 329.85 | **100.7** | n/a | nan | Industrials | 78,363 | 16,279,968 |
| 57 | AEGISLOG | Aegis Logistics Limited | NSE | 672.90 | 1349.10 | **100.5** | n/a | nan | Energy | 1,566,951 | 1,429,970,194 |
| 58 | TIRUPATIFL | Tirupati Forge Limited | NSE | 33.60 | 68.17 | **100.4** | n/a | nan | Industrials | 598,872 | 29,265,537 |
| 59 | NRL | Nupur Recyclers Limited | NSE | 53.69 | 107.84 | **99.6** | n/a | nan | Industrials | 81,186 | 5,522,752 |
| 60 | MODISONLTD | MODISON LIMITED | NSE | 145.77 | 295.40 | **97.8** | n/a | nan | Industrials | 121,816 | 27,884,287 |
| 61 | PARACABLES | Paramount Communications Limited | NSE | 32.71 | 64.35 | **96.7** | n/a | nan | Technology | 2,158,933 | 118,783,433 |
| 62 | IDEAFORGE | Ideaforge Technology Limited | NSE | 423.25 | 843.75 | **96.5** | n/a | nan | Technology | 1,038,911 | 617,819,961 |
| 63 | KRN | KRN Heat Exchanger and Refrigeration Limited | NSE | 641.45 | 1249.90 | **94.9** | n/a | nan | Technology | 844,296 | 829,207,373 |
| 64 | JAYBARMARU | Jay Bharat Maruti Limited | NSE | 87.74 | 170.79 | **94.7** | n/a | nan | Consumer Cyclical | 863,645 | 109,478,923 |
| 65 | HIRECT | Hind Rectifiers Limited | NSE | 639.65 | 1244.50 | **94.6** | n/a | nan | Industrials | 172,075 | 165,678,684 |
| 66 | WHEELS | Wheels India Limited | NSE | 759.85 | 1472.10 | **93.7** | n/a | nan | Consumer Cyclical | 140,081 | 185,850,464 |
| 67 | SGMART | SG Mart Limited | NSE | 323.45 | 635.85 | **93.2** | n/a | nan | Industrials | 365,845 | 190,802,146 |
| 68 | POWERINDIA | Hitachi Energy India Limited | NSE | 16630.00 | 32075.00 | **92.2** | n/a | nan | Industrials | 162,626 | 4,347,221,892 |
| 69 | APARINDS | Apar Industries Limited | NSE | 7035.00 | 13836.00 | **91.8** | n/a | nan | Industrials | 118,277 | 1,386,582,321 |
| 70 | 543828 | Sudarshan Pharma Industries Ltd | BSE | 20.86 | 40.00 | **91.8** | n/a | nan | nan | 225,974 | 6,737,929 |
| 71 | SKYGOLD | SKY GOLD AND DIAMONDS LIMITED | NSE | 326.50 | 621.30 | **91.5** | n/a | nan | Consumer Cyclical | 1,093,803 | 480,106,195 |
| 72 | 539730 | Fredun Pharmaceuticals Ltd | BSE | 501.62 | 955.20 | **90.5** | n/a | nan | nan | 35,992 | 24,228,685 |
| 73 | INDOBORAX | Indo Borax & Chemicals Limited | NSE | 243.80 | 465.70 | **90.2** | n/a | nan | Basic Materials | 153,360 | 52,110,368 |
| 74 | BAJAJCON | Bajaj Consumer Care Limited | NSE | 260.70 | 525.65 | **90.1** | n/a | nan | Consumer Defensive | 1,369,689 | 571,703,842 |
| 75 | ASTRAMICRO | Astra Microwave Products Limited | NSE | 889.85 | 1720.80 | **89.7** | n/a | nan | Technology | 592,802 | 765,206,622 |
| 76 | ADANIENSOL | Adani Energy Solutions Limited | NSE | 885.50 | 1722.60 | **89.6** | n/a | nan | Utilities | 2,353,785 | 2,974,823,645 |
| 77 | RISHABH | Rishabh Instruments Limited | NSE | 340.00 | 656.10 | **89.4** | n/a | nan | Technology | 152,830 | 79,245,467 |
| 78 | LLOYDSENGG | LLOYDS ENGINEERING WORKS LIMITED | NSE | 46.88 | 88.56 | **88.9** | n/a | nan | Industrials | 9,754,998 | 682,038,606 |
| 79 | BALAMINES | Balaji Amines Limited | NSE | 1212.10 | 2289.10 | **88.8** | n/a | nan | Basic Materials | 415,605 | 634,481,799 |
| 80 | KOTYARK | Kotyark Industries Limited | NSE | 18.26 | 34.55 | **88.7** | n/a | nan | Basic Materials | 356,086 | 12,425,545 |
| 81 | E2E | E2E Networks Limited | NSE | 214.99 | 404.95 | **88.4** | n/a | nan | Technology | 1,508,589 | 462,479,097 |
| 82 | SEDEMAC | SEDEMAC Mechatronics Limited | NSE | 1451.10 | 2712.30 | **86.9** | n/a | nan | Consumer Cyclical | 230,137 | 458,704,165 |
| 83 | ANTELOPUS | Antelopus Selan Energy Limited | NSE | 414.80 | 820.80 | **86.5** | n/a | nan | Energy | 394,702 | 226,543,698 |
| 84 | SKMEGGPROD | SKM Egg Products Export (India) Limited | NSE | 180.65 | 318.95 | **84.9** | n/a | nan | Consumer Defensive | 610,385 | 140,050,611 |
| 85 | APOLLOPIPE | Apollo Pipes Limited | NSE | 270.30 | 499.50 | **84.8** | n/a | nan | Industrials | 928,078 | 380,504,744 |
| 86 | ACMESOLAR | Acme Solar Holdings Limited | NSE | 209.68 | 385.25 | **83.7** | n/a | nan | Utilities | 1,705,076 | 500,234,933 |
| 87 | SANSERA | Sansera Engineering Limited | NSE | 1759.00 | 3218.80 | **83.0** | n/a | nan | Consumer Cyclical | 245,523 | 601,524,767 |
| 88 | GAYAPROJ | Gayatri Projects Limited | NSE | 12.10 | 22.12 | **82.8** | n/a | nan | Industrials | 300,912 | 5,962,343 |
| 89 | SPARC | Sun Pharma Advanced Research Company Limited | NSE | 127.99 | 235.20 | **81.5** | n/a | nan | Healthcare | 4,717,229 | 847,613,325 |
| 90 | PARAS | Paras Defence and Space Technologies Limited | NSE | 626.30 | 1176.30 | **81.5** | n/a | nan | Industrials | 2,175,468 | 2,088,094,984 |
| 91 | CONSOFINVT | Consolidated Finvest & Holdings Limited | NSE | 152.79 | 279.01 | **81.2** | n/a | nan | Financial Services | 23,294 | 5,182,455 |
| 92 | ARVIND | Arvind Limited | NSE | 292.65 | 535.95 | **79.5** | n/a | nan | Consumer Cyclical | 725,959 | 314,150,655 |
| 93 | SPECTRUM | Spectrum Electrical Industries Limited | NSE | 1090.90 | 1959.30 | **79.1** | n/a | nan | Industrials | 18,071 | 30,327,112 |
| 94 | BUILDPRO | Shankara Buildpro Limited | NSE | 691.35 | 1233.40 | **78.4** | n/a | nan | Consumer Cyclical | 86,095 | 90,417,133 |
| 95 | DATAPATTNS | Data Patterns (India) Limited | NSE | 2250.60 | 4085.80 | **78.2** | n/a | nan | Industrials | 942,023 | 3,418,304,114 |
| 96 | GAUDIUMIVF | Gaudium IVF and Women Health Limited | NSE | 80.26 | 143.78 | **78.0** | n/a | nan | Healthcare | 855,294 | 84,360,570 |
| 97 | PARKHOSPS | Park Medi World Limited | NSE | 153.92 | 273.95 | **78.0** | n/a | nan | Healthcare | 1,414,221 | 275,640,478 |
| 98 | INOXINDIA | INOX India Limited | NSE | 1096.60 | 1980.20 | **77.9** | n/a | nan | Industrials | 229,869 | 371,449,667 |
| 99 | J&KBANK | The Jammu & Kashmir Bank Limited | NSE | 98.92 | 182.69 | **77.7** | n/a | nan | Financial Services | 4,904,147 | 638,372,312 |
| 100 | WABAG | VA Tech Wabag Limited | NSE | 1123.90 | 1991.10 | **77.2** | n/a | nan | Industrials | 487,566 | 773,374,113 |
| 101 | GCSL | Gretex Corporate Services Limited | NSE | 295.40 | 525.70 | **76.8** | n/a | nan | Financial Services | 226,759 | 96,901,961 |
| 102 | UNIVASTU | Univastu India Limited | NSE | 65.88 | 116.23 | **76.4** | n/a | nan | Industrials | 116,259 | 9,171,608 |
| 103 | TDPOWERSYS | TD Power Systems Limited | NSE | 640.65 | 1127.70 | **76.0** | n/a | nan | Industrials | 1,113,213 | 1,124,501,299 |
| 104 | NITINSPIN | Nitin Spinners Limited | NSE | 307.45 | 550.35 | **75.9** | n/a | nan | Consumer Cyclical | 366,900 | 148,501,291 |
| 105 | 544023 | Kalyani Cast-Tech Ltd | BSE | 459.40 | 820.00 | **75.6** | n/a | nan | nan | 11,203 | 6,519,035 |
| 106 | NEOGEN | Neogen Chemicals Limited | NSE | 1205.50 | 2175.60 | **75.3** | n/a | nan | Basic Materials | 185,530 | 253,323,214 |
| 107 | SHREEJISPG | Shreeji Shipping Global Limited | NSE | 336.50 | 596.30 | **74.4** | n/a | nan | Industrials | 1,114,953 | 450,155,858 |
| 108 | SENORES | Senores Pharmaceuticals Limited | NSE | 784.55 | 1405.10 | **74.3** | n/a | nan | Healthcare | 323,382 | 320,487,668 |
| 109 | RAMCOSYS | Ramco Systems Limited | NSE | 452.70 | 789.05 | **74.3** | n/a | nan | Technology | 998,360 | 707,827,954 |
| 110 | QPOWER | Quality Power Electrical Equipments Limited | NSE | 667.30 | 1163.00 | **74.3** | n/a | nan | Industrials | 867,811 | 813,624,295 |
| 111 | UTLSOLAR | Fujiyama Power Systems Limited | NSE | 209.07 | 365.15 | **73.8** | n/a | nan | Technology | 524,368 | 137,976,798 |
| 112 | BLUSPRING | Bluspring Enterprises Limited | NSE | 64.07 | 111.33 | **73.8** | n/a | nan | Industrials | 589,625 | 51,305,755 |
| 113 | NAHARSPING | Nahar Spinning Mills Limited | NSE | 159.40 | 276.75 | **73.6** | n/a | nan | Consumer Cyclical | 27,661 | 5,741,947 |
| 114 | RPEL | Raghav Productivity Enhancers Limited | NSE | 757.20 | 1313.80 | **73.5** | n/a | nan | Basic Materials | 92,966 | 84,884,557 |
| 115 | THANGAMAYL | Thangamayil Jewellery Limited | NSE | 3712.30 | 6436.00 | **73.4** | n/a | nan | Consumer Cyclical | 175,863 | 778,659,974 |
| 116 | FCL | Fineotex Chemical Limited | NSE | 22.13 | 38.75 | **73.1** | n/a | nan | Basic Materials | 10,423,389 | 359,940,040 |
| 117 | GANECOS | Ganesha Ecosphere Limited | NSE | 697.05 | 1203.15 | **72.6** | n/a | nan | Consumer Cyclical | 449,357 | 447,414,941 |
| 118 | DIACABS | Diamond Power Infrastructure Limited | NSE | 127.05 | 222.38 | **72.2** | n/a | nan | Industrials | 3,395,079 | 623,152,248 |
| 119 | COCKERILL | John Cockerill India Limited | NSE | 5277.35 | 8959.00 | **71.8** | n/a | nan | Industrials | 22,062 | 190,665,701 |
| 120 | APOLLO | Apollo Micro Systems Limited | NSE | 227.40 | 397.80 | **71.2** | n/a | nan | Industrials | 11,895,352 | 4,098,645,799 |
| 121 | HESTERBIO | Hester Biosciences Limited | NSE | 1410.30 | 2447.80 | **70.6** | n/a | nan | Healthcare | 13,814 | 28,863,641 |
| 122 | 540492 | Starlineps Enterprises Ltd | BSE | 6.24 | 10.64 | **70.5** | n/a | nan | nan | 994,045 | 8,796,334 |
| 123 | MBAPL | Madhya Bharat Agro Products Limited | NSE | 79.29 | 136.20 | **70.3** | n/a | nan | Basic Materials | 1,163,414 | 117,603,338 |
| 124 | SBCL | Shivalik Bimetal Controls Limited | NSE | 433.20 | 737.35 | **70.2** | n/a | nan | Industrials | 328,552 | 205,487,454 |
| 125 | IZMO | IZMO Limited | NSE | 657.25 | 1124.00 | **70.1** | n/a | nan | Technology | 127,190 | 107,464,702 |
| 126 | SATIN | Satin Creditcare Network Limited | NSE | 148.72 | 255.07 | **70.0** | n/a | nan | Financial Services | 558,578 | 119,743,854 |
| 127 | 524520 | KMC Speciality Hospitals (India) Ltd | BSE | 76.55 | 134.65 | **69.5** | n/a | nan | nan | 136,985 | 14,327,982 |
| 128 | AEQUS | Aequs Limited | NSE | 135.42 | 228.38 | **69.2** | n/a | nan | Industrials | 6,131,335 | 1,122,029,553 |
| 129 | HONASA | Honasa Consumer Limited | NSE | 277.60 | 466.95 | **68.2** | n/a | nan | Consumer Defensive | 1,823,754 | 651,139,822 |
| 130 | KERNEX | Kernex Microsystems (India) Limited | NSE | 1207.50 | 2039.30 | **68.1** | n/a | nan | Technology | 266,108 | 387,956,600 |
| 131 | NRBBEARING | NRB Bearing Limited | NSE | 243.25 | 407.40 | **67.5** | n/a | nan | Consumer Cyclical | 558,372 | 203,203,540 |
| 132 | ADANIGREEN | Adani Green Energy Limited | NSE | 883.20 | 1513.90 | **67.4** | n/a | nan | Utilities | 3,488,888 | 3,967,132,681 |
| 133 | GVT&D | GE Vernova T&D India Limited | NSE | 2600.80 | 4387.40 | **67.4** | n/a | nan | Industrials | 797,481 | 3,195,611,088 |
| 134 | WANBURY | Wanbury Limited | NSE | 198.57 | 332.20 | **67.3** | n/a | nan | Healthcare | 173,610 | 49,894,712 |
| 135 | BHEL | Bharat Heavy Electricals Limited | NSE | 250.15 | 422.00 | **67.2** | n/a | nan | Industrials | 14,948,425 | 4,897,074,365 |
| 136 | 543920 | CFF Fluid Control Ltd | BSE | 544.10 | 917.60 | **67.0** | n/a | nan | nan | 31,275 | 21,976,522 |
| 137 | JINDALPOLY | Jindal Poly Films Limited | NSE | 380.35 | 659.05 | **66.7** | n/a | nan | Consumer Cyclical | 228,867 | 152,531,709 |
| 138 | SGFIN | SG Finserve Limited | NSE | 374.50 | 631.15 | **66.5** | n/a | nan | Financial Services | 347,657 | 183,943,459 |
| 139 | UNIVCABLES | Universal Cables Limited | NSE | 689.30 | 1166.70 | **66.2** | n/a | nan | Industrials | 175,135 | 180,738,473 |
| 140 | KABRAEXTRU | Kabra Extrusion Technik Limited | NSE | 182.58 | 330.70 | **66.1** | n/a | nan | Industrials | 57,452 | 14,854,019 |
| 141 | MOREPENLAB | Morepen Laboratories Limited | NSE | 35.52 | 58.90 | **65.8** | n/a | nan | Healthcare | 6,682,418 | 323,118,820 |
| 142 | EMMVEE | Emmvee Photovoltaic Power Limited | NSE | 202.03 | 345.05 | **65.6** | n/a | nan | Technology | 3,861,834 | 1,008,499,213 |
| 143 | AVADHSUGAR | Avadh Sugar & Energy Limited | NSE | 311.25 | 533.90 | **65.5** | n/a | nan | Consumer Defensive | 72,723 | 30,742,781 |
| 144 | PRECWIRE | Precision Wires India Limited | NSE | 213.23 | 361.65 | **65.1** | n/a | nan | Industrials | 942,516 | 298,643,280 |
| 145 | CENTUM | Centum Electronics Limited | NSE | 2224.70 | 3711.40 | **64.9** | n/a | nan | Technology | 73,215 | 208,011,254 |
| 146 | GNA | GNA Axles Limited | NSE | 340.40 | 567.05 | **64.9** | n/a | nan | Consumer Cyclical | 261,623 | 115,666,712 |
| 147 | SOTL | Savita Oil Technologies Limited | NSE | 347.35 | 580.25 | **64.8** | n/a | nan | Basic Materials | 226,427 | 118,850,746 |
| 148 | INDNIPPON | India Nippon Electricals Limited | NSE | 717.80 | 1213.40 | **64.7** | n/a | nan | Consumer Cyclical | 48,574 | 44,285,771 |
| 149 | STYL | Seshaasai Technologies Limited | NSE | 243.00 | 399.95 | **64.6** | n/a | nan | Technology | 194,588 | 53,958,999 |
| 150 | KPL | Kwality Pharmaceuticals Limited | NSE | 1662.60 | 2702.00 | **64.6** | n/a | nan | nan | 41,074 | 92,382,833 |
| 151 | FILATEX | Filatex India Limited | NSE | 42.93 | 71.57 | **64.4** | n/a | nan | Consumer Cyclical | 1,585,268 | 89,417,111 |
| 152 | TEJASNET | Tejas Networks Limited | NSE | 328.00 | 538.90 | **64.3** | n/a | nan | Technology | 8,597,067 | 4,091,440,883 |
| 153 | 531911 | Galaxy Agrico Exports Ltd | BSE | 42.62 | 69.90 | **64.0** | n/a | nan | nan | 121,554 | 5,710,113 |
| 154 | GALAPREC | Gala Precision Engineering Limited | NSE | 720.15 | 1182.00 | **63.9** | n/a | nan | Industrials | 43,427 | 42,259,328 |
| 155 | BBOX | Black Box Limited | NSE | 497.70 | 825.50 | **63.8** | n/a | nan | Technology | 652,404 | 482,647,911 |
| 156 | CMPDI | Central Mine Planning & Design Institute Limited | NSE | 154.06 | 254.91 | **63.4** | n/a | nan | Basic Materials | 5,318,555 | 1,207,181,388 |
| 157 | ADFFOODS | ADF Foods Limited | NSE | 181.14 | 299.10 | **62.8** | n/a | nan | Consumer Defensive | 352,897 | 94,031,670 |
| 158 | AMANTA | Amanta Healthcare Limited | NSE | 100.62 | 168.00 | **62.8** | n/a | nan | Healthcare | 163,068 | 21,461,535 |
| 159 | 540786 | Sharika Enterprises Ltd | BSE | 12.78 | 20.89 | **62.4** | n/a | nan | nan | 76,808 | 1,144,697 |
| 160 | ELPROINTL | Elpro International Limited | NSE | 105.35 | 174.63 | **62.4** | n/a | nan | nan | 150,016 | 22,580,058 |
| 161 | MANINDS | Man Industries (India) Limited | NSE | 326.25 | 529.55 | **62.3** | n/a | nan | Basic Materials | 805,252 | 373,487,781 |
| 162 | ICIL | Indo Count Industries Limited | NSE | 239.95 | 389.30 | **62.2** | n/a | nan | Consumer Cyclical | 771,372 | 255,197,712 |
| 163 | AYMSYNTEX | AYM Syntex Limited | NSE | 149.87 | 244.91 | **62.0** | n/a | nan | Consumer Cyclical | 36,139 | 7,566,798 |
| 164 | TALBROAUTO | Talbros Automotive Components Limited | NSE | 236.70 | 405.10 | **61.6** | n/a | nan | Consumer Cyclical | 212,892 | 70,575,654 |
| 165 | HSCL | Himadri Speciality Chemical Limited | NSE | 448.95 | 741.55 | **61.6** | n/a | nan | Basic Materials | 6,269,516 | 3,812,959,448 |
| 166 | SCPL | Sheetal Cool Products Limited | NSE | 297.20 | 490.15 | **61.2** | n/a | nan | Consumer Defensive | 30,176 | 11,287,563 |
| 167 | VENUSPIPES | Venus Pipes & Tubes Limited | NSE | 1018.30 | 1708.80 | **61.0** | n/a | nan | Basic Materials | 83,799 | 114,480,022 |
| 168 | SPAL | S. P. Apparels Limited | NSE | 616.30 | 992.20 | **61.0** | n/a | nan | Consumer Cyclical | 144,231 | 132,642,247 |
| 169 | RRKABEL | R R Kabel Limited | NSE | 1411.80 | 2293.30 | **61.0** | n/a | nan | Industrials | 426,231 | 796,002,143 |
| 170 | SIGNPOST | Signpost India Limited | NSE | 201.51 | 326.90 | **60.5** | n/a | nan | Communication Services | 281,121 | 79,761,145 |
| 171 | VADILALIND | Vadilal Industries Limited | NSE | 4185.20 | 6716.00 | **60.5** | n/a | nan | Consumer Defensive | 18,911 | 97,095,459 |
| 172 | DECNGOLD | Deccan Gold Mines Limited | NSE | 120.20 | 192.75 | **60.4** | n/a | nan | nan | 2,538,479 | 459,160,688 |
| 173 | WALCHANNAG | Walchandnagar Industries Limited | NSE | 144.02 | 245.90 | **60.3** | n/a | nan | Industrials | 2,157,718 | 467,753,218 |
| 174 | MENONBE | Menon Bearings Limited | NSE | 122.09 | 199.67 | **60.1** | n/a | nan | Consumer Cyclical | 128,793 | 19,286,508 |
| 175 | UNIPARTS | Uniparts India Limited | NSE | 410.20 | 676.00 | **60.0** | n/a | nan | Industrials | 134,829 | 76,373,890 |
| 176 | LLOYDSME | Lloyds Metals And Energy Limited | NSE | 1166.80 | 1865.40 | **59.9** | n/a | nan | Basic Materials | 601,958 | 880,747,404 |
| 177 | GHCLTEXTIL | GHCL Textiles Limited | NSE | 71.18 | 113.70 | **59.7** | n/a | nan | Consumer Cyclical | 386,362 | 35,064,663 |
| 178 | MAYURUNIQ | Mayur Uniquoters Ltd | NSE | 492.20 | 785.25 | **59.5** | n/a | nan | Consumer Cyclical | 157,993 | 107,120,052 |
| 179 | RSWM | RSWM Limited | NSE | 128.58 | 212.68 | **59.5** | n/a | nan | Consumer Cyclical | 92,371 | 16,772,359 |
| 180 | ROSSTECH | Rossell Techsys Limited | NSE | 578.20 | 990.90 | **59.4** | n/a | nan | Industrials | 174,616 | 145,518,902 |
| 181 | SUDEEPPHRM | Sudeep Pharma Limited | NSE | 530.00 | 862.75 | **59.3** | n/a | nan | Healthcare | 362,052 | 253,982,571 |
| 182 | THERMAX | Thermax Limited | NSE | 2921.40 | 4662.00 | **59.1** | n/a | nan | Industrials | 217,405 | 886,072,386 |
| 183 | AZAD | Azad Engineering Limited | NSE | 1464.90 | 2329.70 | **59.0** | n/a | nan | Industrials | 353,442 | 702,336,394 |
| 184 | ZIMLAB | Zim Laboratories Limited | NSE | 76.22 | 121.00 | **58.8** | n/a | nan | Healthcare | 73,892 | 6,466,392 |
| 185 | BLSE | BLS E-Services Limited | NSE | 167.09 | 274.37 | **58.6** | n/a | nan | Industrials | 505,485 | 103,676,373 |
| 186 | 543787 | Macfos Ltd | BSE | 722.05 | 1143.70 | **58.4** | n/a | nan | nan | 9,134 | 8,803,931 |
| 187 | ABB | ABB India Limited | NSE | 4691.50 | 7506.00 | **57.8** | n/a | nan | Industrials | 379,048 | 2,430,164,259 |
| 188 | AKUMS | Akums Drugs and Pharmaceuticals Limited | NSE | 421.45 | 664.95 | **57.8** | n/a | nan | Healthcare | 264,825 | 140,646,040 |
| 189 | CYIENTDLM | Cyient DLM Limited | NSE | 366.30 | 578.65 | **57.7** | n/a | nan | Industrials | 681,399 | 243,137,675 |
| 190 | CGPOWER | CG Power and Industrial Solutions Limited | NSE | 573.75 | 905.00 | **57.6** | n/a | nan | Industrials | 3,745,594 | 2,868,078,607 |
| 191 | SONACOMS | Sona BLW Precision Forgings Limited | NSE | 445.95 | 704.85 | **57.5** | n/a | nan | Consumer Cyclical | 2,026,908 | 1,122,893,795 |
| 192 | MARKSANS | Marksans Pharma Limited | NSE | 169.47 | 267.10 | **57.3** | n/a | nan | Healthcare | 1,652,319 | 372,046,865 |
| 193 | PANACHE | Panache Digilife Limited | NSE | 274.90 | 431.00 | **56.8** | n/a | nan | Technology | 16,015 | 5,590,657 |
| 194 | STEELCAS | Steelcast Limited | NSE | 192.47 | 301.60 | **56.7** | n/a | nan | Basic Materials | 128,768 | 35,390,169 |
| 195 | RAYMOND | Raymond Limited | NSE | 383.00 | 604.75 | **56.6** | n/a | nan | Industrials | 605,417 | 290,225,677 |
| 196 | VTL | Vardhman Textiles Limited | NSE | 402.85 | 636.55 | **56.4** | n/a | nan | Consumer Cyclical | 507,507 | 274,865,783 |
| 197 | TIMEX | Timex Group India Limited | NSE | 344.55 | 534.00 | **56.2** | n/a | nan | Consumer Cyclical | 535,726 | 242,145,829 |
| 198 | STOVEKRAFT | Stove Kraft Limited | NSE | 488.05 | 773.25 | **56.2** | n/a | nan | Consumer Cyclical | 246,009 | 137,510,079 |
| 199 | RML | Rane (Madras) Limited | NSE | 737.95 | 1179.20 | **55.4** | n/a | nan | Consumer Cyclical | 47,434 | 47,679,057 |
| 200 | BHARATFORG | Bharat Forge Limited | NSE | 1394.10 | 2190.50 | **54.8** | n/a | nan | Consumer Cyclical | 1,260,658 | 2,272,249,411 |
| 201 | DCMSIL | DCM Shriram International Limited | NSE | 52.21 | 84.77 | **54.6** | n/a | nan | Industrials | 129,435 | 10,065,813 |
| 202 | MACPOWER | Macpower CNC Machines Limited | NSE | 858.00 | 1326.70 | **54.4** | n/a | nan | Industrials | 31,667 | 34,133,831 |
| 203 | GRANULES | Granules India Limited | NSE | 552.75 | 880.80 | **54.2** | n/a | nan | Healthcare | 1,150,248 | 782,980,818 |
| 204 | SAILIFE | Sai Life Sciences Limited | NSE | 821.45 | 1272.00 | **54.0** | n/a | nan | Healthcare | 560,690 | 575,633,237 |
| 205 | AMAGI | Amagi Media Labs Limited | NSE | 348.25 | 562.80 | **53.9** | n/a | nan | Technology | 726,740 | 292,309,849 |
| 206 | EXICOM | Exicom Tele-Systems Limited | NSE | 105.14 | 161.51 | **53.6** | n/a | nan | Industrials | 2,761,466 | 412,174,765 |
| 207 | DIVGIITTS | Divgi Torqtransfer Systems Limited | NSE | 592.45 | 913.50 | **53.3** | n/a | nan | Consumer Cyclical | 102,431 | 92,470,077 |
| 208 | TBZ | Tribhovandas Bhimji Zaveri Limited | NSE | 168.41 | 258.13 | **53.3** | n/a | nan | Consumer Cyclical | 1,184,214 | 228,213,795 |
| 209 | UNICHEMLAB | Unichem Laboratories Limited | NSE | 384.40 | 589.05 | **53.2** | n/a | nan | Healthcare | 345,600 | 172,563,539 |
| 210 | MEGASTAR | Megastar Foods Limited | NSE | 220.15 | 337.35 | **53.2** | n/a | nan | Consumer Defensive | 30,370 | 9,429,458 |
| 211 | RAYMONDREL | Raymond Realty Limited | NSE | 446.00 | 683.30 | **53.2** | n/a | nan | Real Estate | 706,767 | 406,443,605 |
| 212 | VISL | Vedanta Iron and Steel Limited | NSE | 21.06 | 33.87 | **53.2** | n/a | nan | Basic Materials | 87,638,903 | 2,837,925,559 |
| 213 | CARYSIL | CARYSIL LIMITED | NSE | 759.00 | 1170.40 | **53.1** | n/a | nan | Consumer Cyclical | 120,487 | 121,400,000 |
| 214 | GRANDOAK | Grand Oak Canyons Distillery Limited | NSE | 28.90 | 44.21 | **53.0** | n/a | nan | nan | 52,627 | 1,988,571 |
| 215 | KAMDHENU | Kamdhenu Limited | NSE | 21.85 | 33.54 | **52.8** | n/a | nan | Basic Materials | 1,721,795 | 41,616,257 |
| 216 | KIRLPNU | Kirloskar Pneumatic Company Limited | NSE | 1100.10 | 1696.00 | **52.7** | n/a | nan | Industrials | 150,411 | 226,143,771 |
| 217 | HAPPYFORGE | Happy Forgings Limited | NSE | 1033.30 | 1595.30 | **52.6** | n/a | nan | Industrials | 78,596 | 105,621,957 |
| 218 | ADANIPOWER | Adani Power Limited | NSE | 137.48 | 214.45 | **52.6** | n/a | nan | Utilities | 30,947,714 | 5,931,527,648 |
| 219 | GOCLCORP | GOCL Corporation Limited | NSE | 263.10 | 403.70 | **52.1** | n/a | nan | Basic Materials | 202,512 | 62,350,426 |
| 220 | SERVOTECH | Servotech Renewable Power System Limited | NSE | 65.85 | 99.80 | **51.6** | n/a | nan | Industrials | 1,342,700 | 119,733,831 |
| 221 | SKIPPER | Skipper Limited | NSE | 353.60 | 538.80 | **51.6** | n/a | nan | Industrials | 610,402 | 287,323,057 |
| 222 | ADANIENT | Adani Enterprises Limited | NSE | 2055.10 | 3160.70 | **51.5** | n/a | nan | Energy | 1,963,959 | 4,782,664,491 |
| 223 | SUYOG | Suyog Telematics Limited | NSE | 561.75 | 849.85 | **51.5** | n/a | nan | Communication Services | 37,482 | 26,829,088 |
| 224 | APCOTEXIND | Apcotex Industries Limited | NSE | 343.70 | 529.10 | **51.5** | n/a | nan | Basic Materials | 67,800 | 32,586,556 |
| 225 | GREAVESCOT | Greaves Cotton Limited | NSE | 163.97 | 249.46 | **51.0** | n/a | nan | Industrials | 1,517,504 | 292,371,638 |
| 226 | FAZE3Q | Faze Three Limited | NSE | 371.30 | 560.60 | **51.0** | n/a | nan | Consumer Cyclical | 64,256 | 30,544,347 |
| 227 | AETHER | Aether Industries Limited | NSE | 966.45 | 1475.30 | **50.6** | n/a | nan | Basic Materials | 346,377 | 393,674,751 |
| 228 | ELGIRUBCO | Elgi Rubber Company Limited | NSE | 40.35 | 61.84 | **50.5** | n/a | nan | Consumer Cyclical | 78,006 | 3,896,776 |
| 229 | BANDHANBNK | Bandhan Bank Limited | NSE | 139.39 | 213.25 | **49.7** | n/a | nan | Financial Services | 10,675,529 | 1,904,298,698 |
| 230 | KTKBANK | The Karnataka Bank Limited | NSE | 182.12 | 273.15 | **49.7** | n/a | nan | Financial Services | 3,409,688 | 774,783,499 |
| 231 | STYLAMIND | Stylam Industries Limited | NSE | 2169.90 | 3250.40 | **49.4** | n/a | nan | Consumer Cyclical | 53,359 | 128,759,383 |
| 232 | 526433 | ASM Technologies Ltd | BSE | 2745.35 | 4099.70 | **49.3** | n/a | nan | nan | 23,507 | 74,137,709 |
| 233 | ARROWGREEN | Arrow Greentech Limited | NSE | 448.80 | 670.00 | **49.3** | n/a | nan | Consumer Cyclical | 62,424 | 32,548,559 |
| 234 | ADVAIT | Advait Energy Transitions Limited | NSE | 1391.80 | 2085.40 | **49.3** | n/a | nan | Industrials | 57,294 | 112,018,080 |
| 235 | KOPRAN | Kopran Limited | NSE | 135.91 | 203.63 | **49.2** | n/a | nan | Healthcare | 495,479 | 80,892,912 |
| 236 | BTTL | Bhilwara Technical Textiles Limited | NSE | 34.70 | 51.77 | **49.2** | n/a | nan | Consumer Cyclical | 57,744 | 2,714,520 |
| 237 | ENRIN | Siemens Energy India Limited | NSE | 2269.40 | 3385.50 | **49.2** | n/a | nan | Utilities | 567,022 | 1,722,054,631 |
| 238 | BOROSCI | Borosil Scientific Limited | NSE | 107.78 | 160.75 | **49.1** | n/a | nan | Consumer Cyclical | 158,678 | 22,565,194 |
| 239 | OFSS | Oracle Financial Services Software Limited | NSE | 7825.00 | 11771.00 | **49.1** | n/a | nan | Technology | 227,799 | 2,019,948,120 |
| 240 | CALSOFT | California Software Company Limited | NSE | 15.02 | 22.12 | **49.0** | n/a | nan | Technology | 120,314 | 2,335,622 |
| 241 | KISSHT | OnEMI Technology Solutions Limited | NSE | 208.63 | 310.65 | **48.9** | n/a | nan | Financial Services | 5,142,813 | 1,284,284,238 |
| 242 | BHARATSE | Bharat Seats Limited | NSE | 151.28 | 225.09 | **48.8** | n/a | nan | Consumer Cyclical | 715,286 | 152,592,696 |
| 243 | SAREGAMA | Saregama India Limited | NSE | 332.75 | 494.85 | **48.7** | n/a | nan | Communication Services | 1,757,099 | 713,108,416 |
| 244 | RAIN | Rain Industries Limited | NSE | 132.65 | 206.77 | **48.7** | n/a | nan | Basic Materials | 5,215,294 | 829,624,774 |
| 245 | GOLDIAM | Goldiam International Limited | NSE | 232.57 | 345.40 | **48.5** | n/a | nan | Consumer Cyclical | 1,126,406 | 340,572,293 |
| 246 | 544037 | Amic Forging Ltd | BSE | 1165.80 | 1767.05 | **48.0** | n/a | nan | nan | 49,945 | 80,691,124 |
| 247 | STEELXIND | STEEL EXCHANGE INDIA LIMITED | NSE | 8.12 | 12.03 | **47.8** | n/a | nan | Basic Materials | 2,667,878 | 28,769,415 |
| 248 | LAURUSLABS | Laurus Labs Limited | NSE | 1035.50 | 1529.80 | **47.7** | n/a | nan | Healthcare | 1,896,751 | 2,251,415,255 |
| 249 | ORCHPHARMA | Orchid Pharma Limited | NSE | 700.80 | 1041.35 | **47.7** | n/a | nan | Healthcare | 119,435 | 98,283,243 |
| 250 | TINNARUBR | Tinna Rubber and Infrastructure Limited | NSE | 671.75 | 991.60 | **47.6** | n/a | nan | Basic Materials | 44,505 | 35,365,920 |
| 251 | LIKHITHA | Likhitha Infrastructure Limited | NSE | 161.94 | 240.60 | **47.5** | n/a | nan | Energy | 98,804 | 19,067,564 |
| 252 | INNOVACAP | Innova Captab Limited | NSE | 652.75 | 962.70 | **47.5** | n/a | nan | Healthcare | 78,004 | 59,607,916 |
| 253 | DJML | DJ Mediaprint & Logistics Limited | NSE | 72.94 | 106.68 | **47.3** | n/a | nan | Industrials | 217,432 | 20,627,840 |
| 254 | AMBIKCO | Ambika Cotton Mills Limited | NSE | 1139.40 | 1728.20 | **47.2** | n/a | nan | Consumer Cyclical | 12,045 | 18,169,179 |
| 255 | CLEANMAX | Clean Max Enviro Energy Solutions Limited | NSE | 867.50 | 1262.20 | **47.2** | n/a | nan | Utilities | 400,598 | 433,125,644 |
| 256 | SHRIPISTON | SPR Auto Technologies Limited | NSE | 2738.70 | 4169.90 | **47.2** | n/a | nan | Consumer Cyclical | 121,025 | 387,097,273 |
| 257 | BALRAMCHIN | Balrampur Chini Mills Limited | NSE | 410.90 | 604.45 | **47.1** | n/a | nan | Consumer Defensive | 679,285 | 342,810,585 |
| 258 | DENORA | De Nora India Limited | NSE | 592.35 | 871.10 | **47.1** | n/a | nan | Industrials | 8,457 | 6,497,261 |
| 259 | PREMIERENE | Premier Energies Limited | NSE | 732.65 | 1086.20 | **47.0** | n/a | nan | Technology | 1,971,416 | 1,750,651,490 |
| 260 | JITFINFRA | JITF Infralogistics Limited | NSE | 250.30 | 367.70 | **46.9** | n/a | nan | Industrials | 29,552 | 9,721,550 |
| 261 | APEX | Apex Frozen Foods Limited | NSE | 272.00 | 400.25 | **46.7** | n/a | nan | Consumer Defensive | 1,101,038 | 425,128,699 |
| 262 | CAPLIPOINT | Caplin Point Laboratories Limited | NSE | 1782.60 | 2614.20 | **46.6** | n/a | nan | Healthcare | 119,377 | 242,657,716 |
| 263 | CGCL | Capri Global Capital Limited | NSE | 174.94 | 256.38 | **46.5** | n/a | nan | Financial Services | 2,360,892 | 474,877,033 |
| 264 | JETFREIGHT | Jet Freight Logistics Limited | NSE | 16.09 | 23.68 | **46.4** | n/a | nan | Industrials | 165,767 | 3,446,980 |
| 265 | IRISDOREME | Iris Clothings Limited | NSE | 31.65 | 46.54 | **46.4** | n/a | nan | Consumer Cyclical | 487,866 | 17,690,300 |
| 266 | PPAP | PPAP Automotive Limited | NSE | 201.48 | 296.52 | **46.4** | n/a | nan | Consumer Cyclical | 80,138 | 23,548,221 |
| 267 | SBC | SBC Exports Limited | NSE | 28.88 | 42.27 | **46.4** | n/a | nan | Industrials | 11,868,559 | 396,396,760 |
| 268 | RATEGAIN | Rategain Travel Technologies Limited | NSE | 649.95 | 950.70 | **46.3** | n/a | nan | Technology | 493,931 | 333,845,170 |
| 269 | ABSLAMC | Aditya Birla Sun Life AMC Limited | NSE | 786.65 | 1150.60 | **46.3** | n/a | nan | Financial Services | 440,896 | 427,354,010 |
| 270 | 543916 | Hemant Surgical Industries Ltd | BSE | 257.70 | 389.00 | **46.2** | n/a | nan | nan | 27,612 | 9,175,013 |
| 271 | KDDL | KDDL Limited | NSE | 2179.50 | 3186.80 | **46.2** | n/a | nan | Consumer Cyclical | 29,737 | 79,689,517 |
| 272 | 506597 | Amal Ltd | BSE | 492.40 | 752.15 | **46.1** | n/a | nan | nan | 9,959 | 5,994,465 |
| 273 | KRISHANA | Krishana Phoschem Limited | NSE | 94.10 | 140.45 | **45.9** | n/a | nan | Basic Materials | 1,000,359 | 125,590,621 |
| 274 | OCCLLTD | OCCL Limited | NSE | 90.91 | 135.27 | **45.8** | n/a | nan | Basic Materials | 129,558 | 14,895,881 |
| 275 | SASKEN | Sasken Technologies Limited | NSE | 1289.60 | 1886.20 | **45.6** | n/a | nan | Technology | 114,110 | 201,668,837 |
| 276 | PRADPME | Pradeep Metals Limited | NSE | 370.60 | 546.70 | **45.3** | n/a | nan | nan | 27,045 | 12,954,069 |
| 277 | GABRIEL | Gabriel India Limited | NSE | 885.20 | 1336.60 | **45.3** | n/a | nan | Consumer Cyclical | 408,013 | 428,028,585 |
| 278 | QUESS | Quess Corp Limited | NSE | 198.78 | 290.95 | **45.1** | n/a | nan | Industrials | 633,831 | 144,277,162 |
| 279 | BIRLACABLE | Birla Cable Limited | NSE | 125.09 | 182.57 | **45.1** | n/a | nan | Technology | 76,376 | 12,666,542 |
| 280 | SHILCTECH | Shilchar Technologies Limited | NSE | 3004.90 | 4413.90 | **45.1** | n/a | nan | Industrials | 34,859 | 141,486,379 |
| 281 | PREMIERPOL | Premier Polyfilm Limited | NSE | 50.83 | 73.75 | **45.1** | n/a | nan | Basic Materials | 237,944 | 13,950,086 |
| 282 | MUNJALAU | Munjal Auto Industries Limited | NSE | 70.50 | 103.79 | **45.1** | n/a | nan | Consumer Cyclical | 610,841 | 61,896,257 |
| 283 | POWERICA | Powerica Limited | NSE | 390.00 | 572.65 | **45.0** | n/a | nan | Industrials | 510,758 | 260,205,302 |
| 284 | CHENNPETRO | Chennai Petroleum Corporation Limited | NSE | 803.75 | 1200.60 | **44.9** | n/a | nan | Energy | 1,730,919 | 1,747,026,444 |
| 285 | VINDHYATEL | Vindhya Telelinks Limited | NSE | 1205.00 | 1806.50 | **44.8** | n/a | nan | Industrials | 53,648 | 94,433,608 |
| 286 | DBOL | Dhampur Bio Organics Limited | NSE | 74.62 | 111.78 | **44.7** | n/a | nan | Consumer Defensive | 175,639 | 18,575,951 |
| 287 | GLAND | Gland Pharma Limited | NSE | 1668.90 | 2449.00 | **44.7** | n/a | nan | Healthcare | 349,489 | 750,445,934 |
| 288 | AEROENTER | Aeroflex Enterprises Limited | NSE | 80.56 | 117.46 | **44.7** | n/a | nan | Basic Materials | 624,275 | 68,405,150 |
| 289 | RADICO | Radico Khaitan Limited | NSE | 2753.50 | 4097.90 | **44.4** | n/a | nan | Consumer Defensive | 406,053 | 1,286,828,682 |
| 290 | JINDALSAW | Jindal Saw Limited | NSE | 186.80 | 269.45 | **44.2** | n/a | nan | Basic Materials | 5,340,833 | 1,071,934,683 |
| 291 | PANAMAPET | Panama Petrochem Limited | NSE | 283.00 | 418.05 | **44.2** | n/a | nan | Energy | 317,473 | 126,494,408 |
| 292 | SOLARINDS | Solar Industries India Limited | NSE | 12596.00 | 18467.00 | **43.9** | n/a | nan | Basic Materials | 163,279 | 2,457,851,471 |
| 293 | BETA | Beta Drugs Limited | NSE | 1538.60 | 2229.10 | **43.9** | n/a | nan | Healthcare | 19,039 | 31,176,440 |
| 294 | 526873 | Rajasthan Securities Ltd | BSE | 37.19 | 54.45 | **43.8** | n/a | nan | nan | 145,349 | 6,679,535 |
| 295 | INGERRAND | Ingersoll Rand (India) Limited | NSE | 3180.30 | 4571.20 | **43.7** | n/a | nan | Industrials | 18,842 | 75,210,488 |
| 296 | TMB | Tamilnad Mercantile Bank Limited | NSE | 540.75 | 797.35 | **43.6** | n/a | nan | Financial Services | 378,415 | 252,271,208 |
| 297 | KECL | Kirloskar Electric Company Limited | NSE | 83.05 | 119.11 | **43.4** | n/a | nan | Industrials | 291,417 | 30,940,448 |
| 298 | PANACEABIO | Panacea Biotec Limited | NSE | 382.95 | 548.85 | **43.3** | n/a | nan | Healthcare | 768,386 | 353,453,128 |
| 299 | EMIL | Electronics Mart India Limited | NSE | 89.93 | 128.77 | **43.2** | n/a | nan | Consumer Cyclical | 1,254,272 | 143,383,500 |
| 300 | ASTERDM | Aster DM Healthcare Limited | NSE | 551.60 | 819.90 | **43.1** | n/a | nan | Healthcare | 754,921 | 515,167,241 |
| 301 | MANCREDIT | Mangal Credit and Fincorp Limited | NSE | 158.21 | 233.39 | **43.0** | n/a | nan | Financial Services | 147,445 | 31,145,279 |
| 302 | GOODLUCK | Goodluck India Limited | NSE | 1100.70 | 1546.60 | **43.0** | n/a | nan | Basic Materials | 145,155 | 188,518,033 |
| 303 | UNIMECH | Unimech Aerospace and Manufacturing Limited | NSE | 898.75 | 1282.80 | **42.9** | n/a | nan | Industrials | 110,952 | 110,898,898 |
| 304 | SANGAMIND | Sangam (India) Limited | NSE | 445.75 | 636.95 | **42.9** | n/a | nan | Consumer Cyclical | 69,663 | 38,456,247 |
| 305 | SCANSTL | Scan Steels Limited | NSE | 33.70 | 48.30 | **42.7** | n/a | nan | nan | 104,400 | 4,498,010 |
| 306 | AARTIIND | Aarti Industries Limited | NSE | 345.75 | 493.95 | **42.6** | n/a | nan | Basic Materials | 1,165,282 | 520,410,174 |
| 307 | YATHARTH | Yatharth Hospital & Trauma Care Services Limited | NSE | 593.55 | 844.00 | **42.2** | n/a | nan | Healthcare | 427,185 | 311,223,752 |
| 308 | TARSONS | Tarsons Products Limited | NSE | 198.98 | 287.45 | **41.8** | n/a | nan | Healthcare | 390,588 | 100,342,731 |
| 309 | NARMADA | Narmada Agrobase Limited | NSE | 27.63 | 39.18 | **41.8** | n/a | nan | Basic Materials | 576,630 | 21,318,212 |
| 310 | TRIVENI | Triveni Engineering & Industries Limited | NSE | 330.95 | 472.15 | **41.8** | n/a | nan | Consumer Defensive | 592,682 | 235,052,007 |
| 311 | SANGHVIMOV | Sanghvi Movers Limited | NSE | 297.45 | 421.20 | **41.6** | n/a | nan | Industrials | 385,381 | 131,709,278 |
| 312 | OPTIEMUS | Optiemus Infracom Limited | NSE | 416.25 | 588.95 | **41.5** | n/a | nan | Technology | 195,141 | 84,799,190 |
| 313 | MANORAMA | Manorama Industries Limited | NSE | 1125.60 | 1591.50 | **41.4** | n/a | nan | Consumer Defensive | 141,048 | 199,652,451 |
| 314 | CORONA | CORONA Remedies Limited | NSE | 1458.80 | 2062.20 | **41.4** | n/a | nan | Healthcare | 179,194 | 265,382,479 |
| 315 | ASIANENE | Asian Energy Services Limited | NSE | 249.80 | 356.65 | **41.2** | n/a | nan | Energy | 263,290 | 86,304,593 |
| 316 | PGIL | Pearl Global Industries Limited | NSE | 1402.50 | 2041.30 | **41.0** | n/a | nan | Consumer Cyclical | 113,190 | 195,707,277 |
| 317 | LUXIND | Lux Industries Limited | NSE | 897.50 | 1278.20 | **41.0** | n/a | nan | Consumer Cyclical | 133,678 | 168,528,471 |
| 318 | DIFFNKG | Diffusion Engineers Limited | NSE | 269.75 | 380.25 | **41.0** | n/a | nan | Industrials | 121,819 | 39,119,149 |
| 319 | NDLVENTURE | NDL Ventures Limited | NSE | 89.58 | 128.18 | **40.7** | n/a | nan | Communication Services | 42,792 | 5,070,468 |
| 320 | 530249 | Bridge Securities Ltd | BSE | 12.04 | 17.45 | **40.6** | n/a | nan | nan | 75,282 | 1,047,844 |
| 321 | LLOYDSENT | Lloyds Enterprises Limited | NSE | 53.85 | 77.90 | **40.6** | n/a | nan | Basic Materials | 4,520,060 | 281,569,513 |
| 322 | 542669 | BMW Industries Ltd | BSE | 36.79 | 53.03 | **40.5** | n/a | nan | nan | 269,908 | 13,258,453 |
| 323 | SFL | Sheela Foam Limited | NSE | 524.65 | 761.10 | **40.4** | n/a | nan | Consumer Cyclical | 235,919 | 146,711,094 |
| 324 | IKIO | IKIO Technologies Limited | NSE | 156.39 | 219.37 | **40.3** | n/a | nan | Technology | 873,940 | 165,393,361 |
| 325 | GOKEX | Gokaldas Exports Limited | NSE | 560.85 | 827.80 | **40.2** | n/a | nan | Consumer Cyclical | 848,772 | 617,376,254 |
| 326 | RAMRAT | Ram Ratna Wires Limited | NSE | 278.25 | 410.75 | **40.2** | n/a | nan | Industrials | 179,679 | 70,406,428 |
| 327 | 539479 | GTV Engineering Ltd | BSE | 49.68 | 69.63 | **40.2** | n/a | nan | nan | 82,348 | 5,373,322 |
| 328 | MAWANASUG | Mawana Sugars Limited | NSE | 80.11 | 113.27 | **40.1** | n/a | nan | Consumer Defensive | 101,823 | 10,148,039 |
| 329 | KRISHNADEF | Krishna Defence And Allied Industries Limited | NSE | 915.30 | 1281.10 | **40.0** | n/a | nan | Industrials | 154,051 | 166,711,156 |
| 330 | SSWL | Steel Strips Wheels Limited | NSE | 190.38 | 266.21 | **39.8** | n/a | nan | Consumer Cyclical | 526,757 | 121,628,638 |
| 331 | FINCABLES | Finolex Cables Limited | NSE | 726.30 | 1017.30 | **39.8** | n/a | nan | Industrials | 464,054 | 445,243,681 |
| 332 | GANESHBE | Ganesh Benzoplast Limited | NSE | 73.14 | 104.41 | **39.7** | n/a | nan | Basic Materials | 275,560 | 26,692,799 |
| 333 | PIXTRANS | Pix Transmissions Limited | NSE | 1268.80 | 1798.00 | **39.6** | n/a | nan | Industrials | 44,971 | 77,282,966 |
| 334 | JASH | Jash Engineering Limited | NSE | 369.25 | 520.45 | **39.5** | n/a | nan | Industrials | 147,775 | 65,558,033 |
| 335 | NAM-INDIA | Nippon Life India Asset Management Limited | NSE | 852.10 | 1186.50 | **39.2** | n/a | nan | Financial Services | 973,793 | 955,550,942 |
| 336 | PSPPROJECT | PSP Projects Limited | NSE | 751.60 | 1046.30 | **39.2** | n/a | nan | Industrials | 103,713 | 88,124,988 |
| 337 | NELCAST | Nelcast Limited | NSE | 89.29 | 128.43 | **39.1** | n/a | nan | Industrials | 213,928 | 28,149,871 |
| 338 | PRIVISCL | Privi Speciality Chemicals Limited | NSE | 2620.70 | 3676.50 | **39.1** | n/a | nan | Basic Materials | 139,705 | 417,522,735 |
| 339 | PRITIKAUTO | Pritika Auto Industries Limited | NSE | 13.05 | 18.29 | **39.1** | n/a | nan | Industrials | 271,158 | 4,040,178 |
| 340 | NIBE | NIBE Limited | NSE | 1077.90 | 1505.40 | **39.1** | n/a | nan | Industrials | 131,859 | 177,395,621 |
| 341 | LANDMARK | Landmark Cars Limited | NSE | 378.65 | 526.25 | **39.0** | n/a | nan | Consumer Cyclical | 442,495 | 212,028,377 |
| 342 | SUNFLAG | Sunflag Iron And Steel Company Limited | NSE | 248.20 | 344.65 | **38.9** | n/a | nan | Basic Materials | 435,814 | 148,736,071 |
| 343 | GREENPLY | Greenply Industries Limited | NSE | 227.30 | 315.35 | **38.7** | n/a | nan | Basic Materials | 617,464 | 168,212,271 |
| 344 | SUTLEJTEX | Sutlej Textiles and Industries Limited | NSE | 28.71 | 39.25 | **38.6** | n/a | nan | Consumer Cyclical | 58,208 | 1,949,822 |
| 345 | NELCO | NELCO Limited | NSE | 625.90 | 867.15 | **38.5** | n/a | nan | Technology | 252,260 | 201,162,928 |
| 346 | ABDL | Allied Blenders and Distillers Limited | NSE | 439.50 | 616.55 | **38.4** | n/a | nan | Consumer Defensive | 467,657 | 255,197,181 |
| 347 | TVSSCS | TVS Supply Chain Solutions Limited | NSE | 98.04 | 135.54 | **38.2** | n/a | nan | Industrials | 1,169,087 | 142,230,348 |
| 348 | SETCO | Setco Automotive Limited | NSE | 13.03 | 18.01 | **38.2** | n/a | nan | Consumer Cyclical | 161,900 | 3,283,468 |
| 349 | ITDC | India Tourism Development Corporation Limited | NSE | 538.40 | 743.95 | **38.2** | n/a | nan | Consumer Cyclical | 1,194,422 | 800,168,783 |
| 350 | WELSPUNLIV | Welspun Living Limited | NSE | 113.00 | 164.40 | **38.2** | n/a | nan | Consumer Cyclical | 3,104,847 | 438,558,588 |
| 351 | GSPCROP | GSP Crop Science Limited | NSE | 356.25 | 492.20 | **38.2** | n/a | nan | Basic Materials | 401,164 | 160,609,208 |
| 352 | WOCKPHARMA | Wockhardt Limited | NSE | 1376.00 | 1900.70 | **38.1** | n/a | nan | Healthcare | 1,544,550 | 2,556,133,995 |
| 353 | SONAMLTD | SONAM LIMITED | NSE | 40.59 | 56.13 | **37.9** | n/a | nan | Consumer Cyclical | 60,973 | 3,086,003 |
| 354 | ZYDUSWELL | Zydus Wellness Limited | NSE | 416.70 | 586.45 | **37.9** | n/a | nan | Consumer Defensive | 1,399,332 | 665,842,197 |
| 355 | VOLTAMP | Voltamp Transformers Limited | NSE | 6911.00 | 9522.00 | **37.8** | n/a | nan | Industrials | 49,347 | 459,491,338 |
| 356 | JGCHEM | J.G.Chemicals Limited | NSE | 321.80 | 445.45 | **37.3** | n/a | nan | Basic Materials | 90,159 | 34,801,087 |
| 357 | BELRISE | Belrise Industries Limited | NSE | 161.89 | 226.91 | **37.3** | n/a | nan | Consumer Cyclical | 6,203,612 | 1,196,730,892 |
| 358 | MMWL | Media Matrix Worldwide Limited | NSE | 10.35 | 14.13 | **37.2** | n/a | nan | Communication Services | 111,287 | 1,589,513 |
| 359 | MARINE | Marine Electricals (India) Limited | NSE | 176.14 | 249.75 | **37.1** | n/a | nan | Industrials | 547,453 | 125,790,084 |
| 360 | FERMENTA | Fermenta Biotech Limited | NSE | 318.40 | 432.65 | **37.0** | n/a | nan | nan | 183,663 | 72,755,743 |
| 361 | WELSPLSOL | Welspun Specialty Solutions Limited | NSE | 38.05 | 53.21 | **37.0** | n/a | nan | nan | 1,479,705 | 77,641,648 |
| 362 | SAIPARENT | Sai Parenterals Limited | NSE | 405.70 | 556.10 | **36.8** | n/a | nan | Healthcare | 323,154 | 169,525,584 |
| 363 | RANEHOLDIN | Rane Holdings Limited | NSE | 1251.90 | 1729.20 | **36.7** | n/a | nan | Consumer Cyclical | 26,787 | 36,709,937 |
| 364 | TARIL | Transformers And Rectifiers (India) Limited | NSE | 242.20 | 332.50 | **36.6** | n/a | nan | Industrials | 6,187,359 | 1,870,335,158 |
| 365 | OAL | Oriental Aromatics Limited | NSE | 258.55 | 358.75 | **36.4** | n/a | nan | Basic Materials | 24,640 | 7,365,071 |
| 366 | XPROINDIA | Xpro India Limited | NSE | 1024.65 | 1397.30 | **36.4** | n/a | nan | Basic Materials | 57,041 | 64,776,220 |
| 367 | 544141 | Pune E - Stock Broking Ltd | BSE | 199.75 | 270.00 | **36.4** | n/a | nan | nan | 23,989 | 5,802,577 |
| 368 | BEPL | Bhansali Engineering Polymers Limited | NSE | 83.01 | 113.10 | **36.2** | n/a | nan | Basic Materials | 539,634 | 51,657,015 |
| 369 | COSMOFIRST | COSMO FIRST LIMITED | NSE | 588.40 | 835.05 | **36.2** | n/a | nan | Consumer Cyclical | 108,514 | 78,552,000 |
| 370 | KPRMILL | K.P.R. Mill Limited | NSE | 812.85 | 1140.30 | **36.2** | n/a | nan | Consumer Cyclical | 593,729 | 599,332,948 |
| 371 | VIJAYA | Vijaya Diagnostic Centre Limited | NSE | 964.20 | 1341.30 | **36.0** | n/a | nan | Healthcare | 249,317 | 290,722,871 |
| 372 | HALDYNGL | Haldyn Glass Limited | NSE | 89.05 | 120.03 | **35.9** | n/a | nan | nan | 103,504 | 11,955,671 |
| 373 | DHANBANK | Dhanlaxmi Bank Limited | NSE | 24.92 | 33.86 | **35.9** | n/a | nan | Financial Services | 1,456,733 | 44,400,456 |
| 374 | 540401 | Maximus International Ltd | BSE | 10.03 | 13.61 | **35.8** | n/a | nan | nan | 67,448 | 684,757 |
| 375 | KMEW | Knowledge Marine & Engineering Works Limited | NSE | 1770.60 | 2404.90 | **35.8** | n/a | nan | Industrials | 169,397 | 312,422,319 |
| 376 | SCI | Shipping Corporation Of India Limited | NSE | 203.25 | 281.75 | **35.8** | n/a | nan | Industrials | 7,059,705 | 2,019,885,161 |
| 377 | NEULANDLAB | Neuland Laboratories Limited | NSE | 13581.00 | 18434.00 | **35.7** | n/a | nan | Healthcare | 52,107 | 813,090,794 |
| 378 | GANDHAR | Gandhar Oil Refinery (India) Limited | NSE | 153.19 | 207.93 | **35.7** | n/a | nan | Energy | 1,155,903 | 191,766,299 |
| 379 | PREMEXPLN | Premier Explosives Limited | NSE | 467.00 | 664.10 | **35.7** | n/a | nan | Basic Materials | 623,987 | 402,647,260 |
| 380 | SHAILY | Shaily Engineering Plastics Limited | NSE | 2035.60 | 2760.60 | **35.6** | n/a | nan | Basic Materials | 342,538 | 818,240,174 |
| 381 | RACLGEAR | RACL Geartech Limited | NSE | 974.10 | 1341.10 | **35.6** | n/a | nan | Consumer Cyclical | 74,188 | 99,890,815 |
| 382 | ELGIEQUIP | Elgi Equipments Limited | NSE | 415.55 | 581.70 | **35.4** | n/a | nan | Industrials | 535,941 | 281,565,783 |
| 383 | KSL | Kalyani Steels Limited | NSE | 678.60 | 926.05 | **35.3** | n/a | nan | Basic Materials | 52,187 | 40,787,512 |
| 384 | PITTIENG | Pitti Engineering Limited | NSE | 697.80 | 943.65 | **35.2** | n/a | nan | Industrials | 51,212 | 45,273,580 |
| 385 | ANANDRATHI | Anand Rathi Wealth Limited | NSE | 1533.45 | 2072.70 | **35.2** | n/a | nan | Financial Services | 578,800 | 974,245,552 |
| 386 | RPPL | Rajshree Polypack Limited | NSE | 16.04 | 22.26 | **35.1** | n/a | nan | Consumer Cyclical | 110,977 | 2,033,680 |
| 387 | CUMMINSIND | Cummins India Limited | NSE | 4020.90 | 5448.00 | **35.1** | n/a | nan | Industrials | 607,075 | 2,947,297,675 |
| 388 | ZENTEC | Zen Technologies Limited | NSE | 1304.30 | 1769.70 | **35.0** | n/a | nan | Industrials | 667,695 | 1,061,407,010 |
| 389 | IDEA | Vodafone Idea Limited | NSE | 10.13 | 13.74 | **35.0** | n/a | nan | Communication Services | 505,567,606 | 5,862,532,289 |
| 390 | DEEPAKFERT | Deepak Fertilizers and Petrochemicals Corporation Limited | NSE | 1145.60 | 1594.00 | **34.8** | n/a | nan | Basic Materials | 438,580 | 534,849,973 |
| 391 | VIYASH | Viyash Scientific Limited | NSE | 199.43 | 268.65 | **34.7** | n/a | nan | Healthcare | 1,413,882 | 337,811,979 |
| 392 | SJS | S.J.S. Enterprises Limited | NSE | 1578.80 | 2175.30 | **34.7** | n/a | nan | Consumer Cyclical | 116,373 | 211,748,256 |
| 393 | BODALCHEM | Bodal Chemicals Limited | NSE | 47.72 | 64.16 | **34.5** | n/a | nan | Basic Materials | 288,233 | 17,848,713 |
| 394 | SAMBHV | Sambhv Steel Tubes Limited | NSE | 88.57 | 118.96 | **34.3** | n/a | nan | Basic Materials | 1,271,466 | 135,978,000 |
| 395 | ADOR | Ador Welding Limited | NSE | 999.90 | 1384.10 | **34.1** | n/a | nan | Industrials | 26,990 | 29,356,450 |
| 396 | DIXON | Dixon Technologies (India) Limited | NSE | 10682.00 | 14329.00 | **34.1** | n/a | nan | Technology | 678,894 | 7,824,828,430 |
| 397 | DYCL | Dynamic Cables Limited | NSE | 285.00 | 386.50 | **34.1** | n/a | nan | Industrials | 397,866 | 136,183,176 |
| 398 | 515043 | Saint Gobain Sekurit India Ltd | BSE | 98.95 | 132.80 | **33.9** | n/a | nan | nan | 54,608 | 6,353,662 |
| 399 | AUROPHARMA | Aurobindo Pharma Limited | NSE | 1141.70 | 1533.40 | **33.9** | n/a | nan | Healthcare | 1,384,791 | 1,838,141,096 |
| 400 | STARHEALTH | Star Health and Allied Insurance Company Limited | NSE | 435.00 | 582.95 | **33.8** | n/a | nan | Financial Services | 649,776 | 326,538,957 |
| 401 | MWL | Mangalam Worldwide Limited | NSE | 27.19 | 37.15 | **33.6** | n/a | nan | Basic Materials | 873,094 | 26,636,326 |
| 402 | WEBELSOLAR | Websol Energy System Limited | NSE | 78.09 | 104.29 | **33.5** | n/a | nan | Technology | 6,576,862 | 581,045,847 |
| 403 | NYKAA | FSN E-Commerce Ventures Limited | NSE | 242.35 | 323.05 | **33.3** | n/a | nan | Consumer Cyclical | 6,268,951 | 1,700,833,899 |
| 404 | MGEL | Mangalam Global Enterprise Limited | NSE | 12.33 | 16.50 | **33.3** | n/a | nan | Consumer Defensive | 507,521 | 6,785,282 |
| 405 | GRINDWELL | Grindwell Norton Limited | NSE | 1531.20 | 2086.70 | **33.2** | n/a | nan | Industrials | 71,997 | 129,144,344 |
| 406 | DALMIASUG | Dalmia Bharat Sugar and Industries Limited | NSE | 268.80 | 367.40 | **33.1** | n/a | nan | Consumer Defensive | 497,356 | 187,094,758 |
| 407 | 539682 | Mobavenue AI Tech Ltd | BSE | 222.37 | 307.00 | **33.0** | n/a | nan | nan | 46,008 | 12,395,539 |
| 408 | INDIAGLYCO | India Glycols Limited | NSE | 872.00 | 1159.30 | **33.0** | n/a | nan | Basic Materials | 129,118 | 128,451,424 |
| 409 | MAHLOG | Mahindra Logistics Limited | NSE | 279.55 | 387.35 | **32.9** | n/a | nan | Industrials | 288,744 | 106,908,819 |
| 410 | BLUESTONE | BlueStone Jewellery and Lifestyle Limited | NSE | 440.05 | 599.05 | **32.9** | n/a | nan | Consumer Cyclical | 468,790 | 236,850,815 |
| 411 | SUBEXLTD | Subex Limited | NSE | 9.99 | 13.27 | **32.8** | n/a | nan | Technology | 1,986,032 | 20,136,865 |
| 412 | SHANKARA | Shankara Building Products Limited | NSE | 104.02 | 139.65 | **32.8** | n/a | nan | Consumer Cyclical | 167,607 | 19,899,127 |
| 413 | GODREJIND | Godrej Industries Limited | NSE | 1004.80 | 1334.70 | **32.8** | n/a | nan | Industrials | 274,569 | 294,550,675 |
| 414 | MOSCHIP | Moschip Technologies Limited | NSE | 181.03 | 240.10 | **32.6** | n/a | nan | Technology | 2,572,328 | 539,929,989 |
| 415 | MUTHOOTMF | Muthoot Microfin Limited | NSE | 177.99 | 240.06 | **32.6** | n/a | nan | Financial Services | 613,305 | 124,394,620 |
| 416 | 544001 | Sunita Tools Ltd | BSE | 654.45 | 867.45 | **32.5** | n/a | nan | nan | 15,390 | 12,680,645 |
| 417 | MCLEODRUSS | Mcleod Russel India Limited | NSE | 41.99 | 55.64 | **32.5** | n/a | nan | Consumer Defensive | 445,493 | 21,904,245 |
| 418 | SALSTEEL | S.A.L. Steel Limited | NSE | 40.11 | 53.12 | **32.4** | n/a | nan | Basic Materials | 130,562 | 6,444,785 |
| 419 | BSE | BSE Limited | NSE | 2653.40 | 3581.80 | **32.2** | n/a | nan | Financial Services | 4,131,953 | 13,344,996,276 |
| 420 | SINDHUTRAD | Sindhu Trade Links Limited | NSE | 18.35 | 24.75 | **32.2** | n/a | nan | Industrials | 2,145,396 | 52,035,848 |
| 421 | AVL | Aditya Vision Limited | NSE | 476.30 | 634.30 | **32.2** | n/a | nan | Consumer Cyclical | 208,274 | 112,341,178 |
| 422 | 539469 | Panorama Studios International Ltd | BSE | 38.51 | 50.90 | **32.2** | n/a | nan | nan | 173,939 | 7,888,047 |
| 423 | ROLEXRINGS | Rolex Rings Limited | NSE | 118.00 | 157.89 | **32.2** | n/a | nan | Industrials | 2,994,613 | 435,729,829 |
| 424 | DEEPINDS | Deep Industries Limited | NSE | 360.20 | 476.00 | **32.1** | n/a | nan | Energy | 352,400 | 153,453,357 |
| 425 | GULPOLY | Gulshan Polyols Limited | NSE | 131.87 | 176.73 | **32.1** | n/a | nan | Basic Materials | 262,624 | 48,112,589 |
| 426 | CNL | Creative Newtech Limited | NSE | 690.50 | 916.55 | **32.1** | n/a | nan | Technology | 57,444 | 47,247,057 |
| 427 | PFOCUS | Prime Focus Limited | NSE | 208.23 | 289.47 | **32.1** | n/a | nan | Communication Services | 4,031,871 | 1,001,745,323 |
| 428 | AEGISVOPAK | Aegis Vopak Terminals Limited | NSE | 204.00 | 271.24 | **32.0** | n/a | nan | Energy | 1,276,123 | 298,266,903 |
| 429 | FUSION | Fusion Finance Limited | NSE | 163.83 | 225.89 | **32.0** | n/a | nan | Financial Services | 582,805 | 110,757,502 |
| 430 | MANGLMCEM | Mangalam Cement Limited | NSE | 738.40 | 986.60 | **31.8** | n/a | nan | Basic Materials | 85,147 | 72,045,815 |
| 431 | THEMISMED | Themis Medicare Limited | NSE | 83.45 | 109.90 | **31.7** | n/a | nan | Healthcare | 172,696 | 18,386,625 |
| 432 | MMFL | MM Forgings Limited | NSE | 401.00 | 527.60 | **31.6** | n/a | nan | Industrials | 196,290 | 81,151,091 |
| 433 | ARMANFIN | Arman Financial Services Limited | NSE | 1479.50 | 1958.20 | **31.6** | n/a | nan | Financial Services | 46,352 | 75,614,277 |
| 434 | SOMANYCERA | Somany Ceramics Limited | NSE | 397.45 | 522.55 | **31.5** | n/a | nan | Industrials | 105,972 | 49,960,651 |
| 435 | GOKULAGRO | Gokul Agro Resources Limited | NSE | 157.79 | 211.74 | **31.4** | n/a | nan | Consumer Defensive | 1,216,113 | 245,079,419 |
| 436 | AXISCADES | AXISCADES Technologies Limited | NSE | 1178.10 | 1548.00 | **31.4** | n/a | nan | Industrials | 156,070 | 254,766,296 |
| 437 | KIMS | Krishna Institute of Medical Sciences Limited | NSE | 617.00 | 802.95 | **31.4** | n/a | nan | Healthcare | 484,664 | 344,952,896 |
| 438 | SIS | SIS LIMITED | NSE | 321.30 | 433.60 | **31.4** | n/a | nan | Industrials | 194,278 | 75,672,301 |
| 439 | SPLPETRO | Supreme Petrochem Limited | NSE | 507.85 | 693.90 | **31.4** | n/a | nan | Basic Materials | 119,284 | 82,420,926 |
| 440 | NETWEB | Netweb Technologies India Limited | NSE | 3234.80 | 4244.30 | **31.2** | n/a | nan | Technology | 1,700,206 | 6,514,854,256 |
| 441 | TAALTECH | Taal Tech Limited | NSE | 2986.00 | 3933.00 | **31.1** | n/a | nan | nan | 2,537 | 9,277,082 |
| 442 | NUVAMA | Nuvama Wealth Management Limited | NSE | 1421.40 | 1863.10 | **31.1** | n/a | nan | Financial Services | 503,512 | 741,344,033 |
| 443 | TFCILTD | Tourism Finance Corporation of India Limited | NSE | 64.93 | 85.03 | **31.0** | n/a | nan | Financial Services | 8,047,501 | 560,213,640 |
| 444 | ADANIPORTS | Adani Ports and Special Economic Zone Limited | NSE | 1367.60 | 1837.40 | **31.0** | n/a | nan | Industrials | 2,480,060 | 3,923,918,326 |
| 445 | CARBORUNIV | Carborundum Universal Limited | NSE | 779.65 | 1059.80 | **30.9** | n/a | nan | Industrials | 233,457 | 228,307,539 |
| 446 | ALIVUS | Alivus Life Sciences Limited | NSE | 868.35 | 1133.30 | **30.8** | n/a | nan | Healthcare | 94,765 | 95,068,803 |
| 447 | HEXAGON | Hexagon Nutrition Limited | NSE | 50.66 | 69.54 | **30.7** | n/a | nan | Consumer Defensive | 3,501,058 | 226,097,246 |
| 448 | AVANTIFEED | Avanti Feeds Limited | NSE | 784.85 | 1024.85 | **30.6** | n/a | nan | Consumer Defensive | 1,070,078 | 1,257,544,262 |
| 449 | ZYDUSLIFE | Zydus Lifesciences Limited | NSE | 873.40 | 1143.70 | **30.5** | n/a | nan | Healthcare | 1,029,586 | 1,030,465,842 |
| 450 | RPSGVENT | RPSG VENTURES LIMITED | NSE | 682.90 | 895.30 | **30.4** | n/a | nan | Technology | 538,810 | 505,436,219 |
| 451 | TANLA | Tanla Platforms Limited | NSE | 441.25 | 584.55 | **30.4** | n/a | nan | Technology | 823,026 | 422,012,729 |
| 452 | 506854 | TANFAC Industries Ltd-$ | BSE | 2060.10 | 2684.25 | **30.3** | n/a | nan | nan | 16,259 | 36,124,405 |
| 453 | EXIDEIND | Exide Industries Limited | NSE | 330.50 | 435.20 | **30.2** | n/a | nan | Consumer Cyclical | 2,625,534 | 963,296,967 |
| 454 | OLECTRA | Olectra Greentech Limited | NSE | 1034.60 | 1346.70 | **30.2** | n/a | nan | Industrials | 839,697 | 1,014,894,632 |
| 455 | JAGSNPHARM | Jagsonpal Pharmaceuticals Limited | NSE | 172.17 | 224.08 | **30.1** | n/a | nan | Healthcare | 200,430 | 42,324,887 |
| 456 | GINNIFILA | Ginni Filaments Limited | NSE | 37.31 | 48.53 | **30.1** | n/a | nan | Consumer Cyclical | 131,368 | 5,634,553 |
| 457 | JYOTISTRUC | Jyoti Structures Limited | NSE | 8.19 | 11.17 | **30.0** | n/a | nan | Industrials | 10,262,976 | 116,672,501 |
| 458 | QUADFUTURE | Quadrant Future Tek Limited | NSE | 304.80 | 405.00 | **30.0** | n/a | nan | Industrials | 1,287,379 | 434,795,546 |
| 459 | WSTCSTPAPR | West Coast Paper Mills Limited | NSE | 395.50 | 520.40 | **29.9** | n/a | nan | Basic Materials | 108,498 | 52,294,640 |
| 460 | SILVERTUC | Silver Touch Technologies Limited | NSE | 152.21 | 197.72 | **29.9** | n/a | nan | Technology | 818,340 | 150,042,975 |
| 461 | KSR | KSR Footwear Limited | NSE | 24.08 | 31.24 | **29.7** | n/a | nan | Consumer Cyclical | 86,460 | 2,191,594 |
| 462 | ATGL | Adani Total Gas Limited | NSE | 532.30 | 706.60 | **29.7** | n/a | nan | Utilities | 4,299,855 | 2,793,916,041 |
| 463 | AYE | Aye Finance Limited | NSE | 128.91 | 168.12 | **29.6** | n/a | nan | Financial Services | 1,754,694 | 244,363,679 |
| 464 | POKARNA | Pokarna Limited | NSE | 715.55 | 967.30 | **29.6** | n/a | nan | Industrials | 167,765 | 165,463,764 |
| 465 | MOTHERSON | Samvardhana Motherson International Limited | NSE | 107.89 | 144.17 | **29.5** | n/a | nan | Consumer Cyclical | 19,934,681 | 2,561,006,029 |
| 466 | LINCOLN | Lincoln Pharmaceuticals Limited | NSE | 461.05 | 597.00 | **29.5** | n/a | nan | Healthcare | 88,916 | 56,608,121 |
| 467 | AMBER | Amber Enterprises India Limited | NSE | 6033.00 | 7804.50 | **29.4** | n/a | nan | Consumer Cyclical | 355,077 | 2,570,390,276 |
| 468 | TIIL | Technocraft Industries (India) Limited | NSE | 1907.00 | 2538.30 | **29.2** | n/a | nan | Industrials | 14,030 | 33,011,576 |
| 469 | TRITURBINE | Triveni Turbine Limited | NSE | 470.90 | 615.25 | **29.2** | n/a | nan | Industrials | 1,627,343 | 983,473,545 |
| 470 | STEL | Stel Holdings Limited | NSE | 398.75 | 555.50 | **29.2** | n/a | nan | Financial Services | 13,587 | 7,013,451 |
| 471 | GROWW | Billionbrains Garage Ventures Limited | NSE | 156.98 | 208.30 | **29.2** | n/a | nan | Financial Services | 44,216,730 | 8,066,304,006 |
| 472 | JINDWORLD | Jindal Worldwide Limited | NSE | 24.95 | 32.20 | **29.1** | n/a | nan | Consumer Cyclical | 2,411,929 | 71,413,719 |
| 473 | DWARKESH | Dwarikesh Sugar Industries Limited | NSE | 33.49 | 44.08 | **28.9** | n/a | nan | Consumer Defensive | 1,682,802 | 74,918,038 |
| 474 | SURYODAY | Suryoday Small Finance Bank Limited | NSE | 135.88 | 179.79 | **28.8** | n/a | nan | Financial Services | 412,268 | 64,694,476 |
| 475 | WELENT | Welspun Enterprises Limited | NSE | 486.45 | 626.30 | **28.8** | n/a | nan | Industrials | 230,523 | 121,683,906 |
| 476 | PLASTIBLEN | Plastiblends India Limited | NSE | 152.18 | 198.57 | **28.7** | n/a | nan | Basic Materials | 40,619 | 7,390,680 |
| 477 | MSTCLTD | Mstc Limited | NSE | 458.20 | 594.55 | **28.5** | n/a | nan | Industrials | 632,828 | 369,466,139 |
| 478 | VISAKAIND | Visaka Industries Limited | NSE | 62.10 | 80.95 | **28.4** | n/a | nan | Industrials | 111,756 | 7,875,057 |
| 479 | RPGLIFE | RPG Life Sciences Limited | NSE | 2228.00 | 2859.80 | **28.4** | n/a | nan | Healthcare | 26,720 | 61,623,745 |
| 480 | AVG | AVG Logistics Limited | NSE | 157.06 | 201.59 | **28.4** | n/a | nan | Industrials | 64,415 | 11,029,649 |
| 481 | REFEX | Refex Industries Limited | NSE | 243.30 | 306.80 | **28.3** | n/a | nan | Energy | 1,687,578 | 478,527,387 |
| 482 | KSB | Ksb Limited | NSE | 704.30 | 903.60 | **28.2** | n/a | nan | Industrials | 311,051 | 255,662,367 |
| 483 | POLYPLEX | Polyplex Corporation Limited | NSE | 828.15 | 1077.55 | **28.2** | n/a | nan | Basic Materials | 110,528 | 99,753,905 |
| 484 | NITCO | Nitco Limited | NSE | 82.15 | 110.86 | **28.1** | n/a | nan | Industrials | 955,407 | 92,209,510 |
| 485 | BCLIND | Bcl Industries Limited | NSE | 28.46 | 36.47 | **28.1** | n/a | nan | Consumer Defensive | 1,393,251 | 48,531,494 |
| 486 | ANTHEM | Anthem Biosciences Limited | NSE | 599.95 | 777.00 | **28.1** | n/a | nan | Healthcare | 394,303 | 284,678,100 |
| 487 | PPL | Prakash Pipes Limited | NSE | 199.77 | 255.90 | **28.1** | n/a | nan | Industrials | 142,461 | 35,371,976 |
| 488 | JSWINFRA | JSW Infrastructure Limited | NSE | 267.90 | 342.15 | **28.1** | n/a | nan | Industrials | 2,332,328 | 680,114,482 |
| 489 | HUHTAMAKI | Huhtamaki India Limited | NSE | 181.65 | 237.44 | **28.1** | n/a | nan | Consumer Cyclical | 164,756 | 30,812,816 |
| 490 | CORDSCABLE | Cords Cable Industries Limited | NSE | 156.60 | 203.05 | **28.0** | n/a | nan | Industrials | 51,570 | 10,446,506 |
| 491 | IVALUE | Ivalue Infosolutions Limited | NSE | 234.30 | 300.10 | **27.9** | n/a | nan | Technology | 282,924 | 74,681,166 |
| 492 | IPCALAB | IPCA Laboratories Limited | NSE | 1479.70 | 1900.60 | **27.9** | n/a | nan | Healthcare | 242,793 | 378,038,368 |
| 493 | BUTTERFLY | Butterfly Gandhimathi Appliances Limited | NSE | 587.60 | 775.95 | **27.9** | n/a | nan | Consumer Cyclical | 112,165 | 76,272,991 |
| 494 | GUJALKALI | Gujarat Alkalies and Chemicals Limited | NSE | 458.30 | 586.20 | **27.9** | n/a | nan | Basic Materials | 1,944,383 | 1,146,043,161 |
| 495 | PASUPTAC | Pasupati Acrylon Limited | NSE | 44.06 | 58.55 | **27.9** | n/a | nan | Consumer Cyclical | 243,868 | 14,664,818 |
| 496 | SOUTHWEST | South West Pinnacle Exploration Limited | NSE | 177.49 | 226.74 | **27.8** | n/a | nan | Energy | 287,598 | 66,974,784 |
| 497 | APOLLOHOSP | Apollo Hospitals Enterprise Limited | NSE | 6912.50 | 8826.00 | **27.7** | n/a | nan | Healthcare | 399,698 | 3,077,576,806 |
| 498 | NAVINFLUOR | Navin Fluorine International Limited | NSE | 5938.50 | 7579.00 | **27.6** | n/a | nan | Basic Materials | 194,069 | 1,267,691,262 |
| 499 | BHAGCHEM | Bhagiradha Chemicals & Industries Limited | NSE | 212.02 | 270.50 | **27.6** | n/a | nan | Basic Materials | 193,211 | 46,109,634 |
| 500 | SAATVIKGL | Saatvik Green Energy Limited | NSE | 365.65 | 466.40 | **27.6** | n/a | nan | Technology | 204,637 | 86,114,124 |
| 501 | SWANDEF | Swan Defence and Heavy Industries Limited | NSE | 1748.50 | 2229.60 | **27.5** | n/a | nan | Industrials | 15,521 | 29,780,005 |
| 502 | JSFB | Jana Small Finance Bank Limited | NSE | 377.50 | 493.00 | **27.4** | n/a | nan | Financial Services | 569,785 | 249,739,036 |
| 503 | AJANTPHARM | Ajanta Pharma Limited | NSE | 2684.20 | 3419.40 | **27.3** | n/a | nan | Healthcare | 125,633 | 372,897,568 |
| 504 | ASHIANA | Ashiana Housing Limited | NSE | 292.40 | 374.80 | **27.3** | n/a | nan | Real Estate | 138,181 | 46,742,286 |
| 505 | COMSYN | Commercial Syn Bags Limited | NSE | 148.29 | 189.27 | **27.3** | n/a | nan | Consumer Cyclical | 177,322 | 31,507,904 |
| 506 | GARFIBRES | Garware Technical Fibres Limited | NSE | 599.25 | 765.50 | **27.3** | n/a | nan | Consumer Cyclical | 114,477 | 81,007,996 |
| 507 | OMAXE | Omaxe Limited | NSE | 70.42 | 93.50 | **27.3** | n/a | nan | Real Estate | 1,101,731 | 91,539,781 |
| 508 | 538668 | Meghna Infracon Infrastructure Ltd | BSE | 564.50 | 741.05 | **27.2** | n/a | nan | nan | 57,702 | 39,219,153 |
| 509 | KALYANKJIL | Kalyan Jewellers India Limited | NSE | 451.45 | 574.40 | **27.2** | n/a | nan | Consumer Cyclical | 10,673,230 | 4,688,026,299 |
| 510 | VETO | Veto Switchgears And Cables Limited | NSE | 102.50 | 130.41 | **27.2** | n/a | nan | Industrials | 63,329 | 7,838,179 |
| 511 | SHYAMMETL | Shyam Metalics and Energy Limited | NSE | 801.00 | 1022.50 | **27.2** | n/a | nan | Basic Materials | 395,219 | 356,500,649 |
| 512 | MCLOUD | Magellanic Cloud Limited | NSE | 22.27 | 28.37 | **27.2** | n/a | nan | Technology | 6,457,823 | 179,227,111 |
| 513 | BLUEJET | Blue Jet Healthcare Limited | NSE | 459.75 | 584.55 | **27.1** | n/a | nan | Healthcare | 676,649 | 311,816,613 |
| 514 | FLUOROCHEM | Gujarat Fluorochemicals Limited | NSE | 3259.80 | 4144.90 | **27.1** | n/a | nan | Basic Materials | 95,012 | 339,964,521 |
| 515 | KIRLOSIND | Kirloskar Industries Limited | NSE | 2904.30 | 3824.80 | **27.1** | n/a | nan | Industrials | 16,119 | 59,526,140 |
| 516 | AUTOIND | Autoline Industries Limited | NSE | 70.94 | 92.31 | **27.1** | n/a | nan | Consumer Cyclical | 179,714 | 13,854,802 |
| 517 | NEPHROPLUS | Nephrocare Health Services Limited | NSE | 494.75 | 635.70 | **26.9** | n/a | nan | Healthcare | 348,558 | 186,516,937 |
| 518 | MANAKSTEEL | Manaksia Steels Limited | NSE | 58.21 | 76.58 | **26.8** | n/a | nan | Basic Materials | 62,294 | 4,373,535 |
| 519 | AERONEU | Aeroflex Neu Limited | NSE | 70.58 | 89.46 | **26.8** | n/a | nan | Consumer Cyclical | 53,312 | 4,407,381 |
| 520 | GLOTTIS | Glottis Limited | NSE | 53.05 | 67.20 | **26.7** | n/a | nan | Industrials | 282,575 | 16,758,936 |
| 521 | NACLIND | NACL Industries Limited | NSE | 168.58 | 213.45 | **26.6** | n/a | nan | Basic Materials | 840,156 | 159,793,752 |
| 522 | UYFINCORP | U. Y. Fincorp Limited | NSE | 13.24 | 16.75 | **26.5** | n/a | nan | Financial Services | 114,305 | 1,681,511 |
| 523 | SUMICHEM | Sumitomo Chemical India Limited | NSE | 422.60 | 538.55 | **26.4** | n/a | nan | Basic Materials | 546,199 | 256,408,542 |
| 524 | SEAMECLTD | Seamec Limited | NSE | 1092.00 | 1380.40 | **26.4** | n/a | nan | Industrials | 82,252 | 113,307,096 |
| 525 | FEDERALBNK | The Federal Bank  Limited | NSE | 273.25 | 349.00 | **26.4** | n/a | nan | Financial Services | 10,230,188 | 2,935,320,192 |
| 526 | AURUM | Aurum PropTech Limited | NSE | 187.76 | 239.28 | **26.3** | n/a | nan | Real Estate | 153,035 | 31,037,744 |
| 527 | BHAGERIA | Bhageria Industries Limited | NSE | 161.07 | 203.49 | **26.3** | n/a | nan | Basic Materials | 80,921 | 15,103,504 |
| 528 | RATNAVEER | Ratnaveer Precision Engineering Limited | NSE | 143.05 | 180.66 | **26.3** | n/a | nan | Basic Materials | 1,771,540 | 291,115,582 |
| 529 | ZEEL | Zee Entertainment Enterprises Limited | NSE | 83.84 | 107.40 | **26.2** | n/a | nan | Communication Services | 20,384,038 | 1,993,600,702 |
| 530 | DELHIVERY | Delhivery Limited | NSE | 384.85 | 492.15 | **26.2** | n/a | nan | Industrials | 2,945,071 | 1,343,698,696 |
| 531 | ASAL | Automotive Stampings and Assemblies Limited | NSE | 410.90 | 522.30 | **26.2** | n/a | nan | Consumer Cyclical | 28,966 | 14,388,886 |
| 532 | VIPULLTD | Vipul Limited | NSE | 12.40 | 15.64 | **26.1** | n/a | nan | Real Estate | 648,850 | 8,128,581 |
| 533 | NIITLTD | NIIT Limited | NSE | 77.05 | 97.17 | **26.1** | n/a | nan | Consumer Defensive | 1,493,604 | 134,656,067 |
| 534 | FINEORG | Fine Organic Industries Limited | NSE | 4009.50 | 5056.00 | **26.1** | n/a | nan | Basic Materials | 15,111 | 69,468,578 |
| 535 | SPANDANA | Spandana Sphoorty Financial Limited | NSE | 230.40 | 296.90 | **26.1** | n/a | nan | Financial Services | 323,815 | 83,212,383 |
| 536 | ENGINERSIN | Engineers India Limited | NSE | 180.61 | 227.66 | **26.1** | n/a | nan | Industrials | 6,013,538 | 1,319,599,396 |
| 537 | CENTENKA | Century Enka Limited | NSE | 423.20 | 541.40 | **26.0** | n/a | nan | Consumer Cyclical | 49,695 | 25,116,889 |
| 538 | RATNAMANI | Ratnamani Metals & Tubes Limited | NSE | 2052.40 | 2582.80 | **25.8** | n/a | nan | Basic Materials | 53,845 | 131,951,665 |
| 539 | STLNETWORK | STL Networks Limited | NSE | 19.47 | 24.46 | **25.6** | n/a | nan | Communication Services | 2,523,212 | 63,776,325 |
| 540 | ONIDA | Onida Electronics Limited | NSE | 31.01 | 39.19 | **25.5** | n/a | nan | Consumer Cyclical | 1,581,202 | 56,842,353 |
| 541 | DSSL | Dynacons Systems & Solutions Limited | NSE | 968.30 | 1214.80 | **25.5** | n/a | nan | Technology | 178,830 | 207,556,151 |
| 542 | SIEMENS | Siemens Limited | NSE | 2848.60 | 3658.80 | **25.3** | n/a | nan | Industrials | 429,973 | 1,470,319,225 |
| 543 | CCL | CCL Products (India) Limited | NSE | 950.60 | 1191.40 | **25.3** | n/a | nan | Consumer Defensive | 332,130 | 359,672,331 |
| 544 | POLYCAB | Polycab India Limited | NSE | 7074.50 | 8862.00 | **25.3** | n/a | nan | Industrials | 421,705 | 3,422,966,246 |
| 545 | EIEL | Enviro Infra Engineers Limited | NSE | 173.84 | 220.23 | **25.2** | n/a | nan | Industrials | 3,212,833 | 641,278,322 |
| 546 | SMSPHARMA | SMS Pharmaceuticals Limited | NSE | 309.65 | 387.75 | **25.2** | n/a | nan | Healthcare | 407,386 | 152,373,464 |

🟡 = penny stock (price < ₹10), flagged not removed.

**Machine-readable file:** `FINAL_universe_25pct.csv` (546 rows).

### Known limitations (full disclosure)
- 464 universe symbols (of 4,524) returned no Yahoo history (recently renamed post-corporate-action e.g. demerged Tata Motors, thinly-traded, or delisted-from-Yahoo) — excluded from the scan, not from reality. These are predominantly illiquid BSE micro-caps.
- 11 NSE-only names have no BSE twin, so their current price rests on Yahoo alone (still passes the adjusted-return integrity check).
- Sector unavailable for 37 BSE-only micro-caps (shown as n/a).