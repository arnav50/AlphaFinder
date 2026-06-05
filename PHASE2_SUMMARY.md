# PHASE 2 — DEEP TECHNICAL ANALYSIS — SUMMARY
Scan date 2026-06-02 · 311 stocks analysed (of 312 Phase-1 names; 1 dropped — KISSHT, <20 bars of history).

## ✓ VERIFICATION CHECKPOINT (Phase 2)
- ✅ All **leading** indicators (RSI, Stochastic, Bollinger, Ichimoku, CCI, Williams %R, OBV, MFI) scored for every stock
- ✅ All **lagging** indicators (MACD, EMA align, ADX, Supertrend, ATR, VWAP, Pivots) scored for every stock
- ✅ **Candlestick** patterns documented with date + context + confirmation (`candles.csv`, 9,285 patterns)
- ✅ **Price-action / chart** patterns with breakout levels + targets (`patterns.csv`)
- ✅ **Scorecard per stock** (Bullish/Neutral/Bearish via indicator confluence) — `reports/<symbol>.md` + `PHASE2_SCORECARD.csv`

## Scorecard distribution
| Verdict | Count |
|---|--:|
| BULLISH | 210 |
| MILD BULLISH | 34 |
| NEUTRAL | 37 |
| MILD BEARISH | 16 |
| BEARISH | 14 |

**Confluence confidence:** {'medium': 153, 'low': 101, 'high': 57}

Key insight: all 311 names gained ≥25% over 6m, but only **244** remain technically bullish; **30** are rolling over (momentum exhausted) and **37** are consolidating.

## Top 25 by confluence score (strongest technical setups)
| # | Symbol | Company | Score | Verdict | Conf | Supertrend | EMA | ADX | RSI | Trend |
|--:|---|---|--:|---|---|---|---|--:|--:|---|
| 1 | NDLVENTURE | NDL Ventures Limited | 17.2 | BULLISH | high | green_buy | bullish | 26.8 | 64.3 | Uptrend |
| 2 | SKYGOLD | SKY GOLD AND DIAMONDS LIMI | 16.5 | BULLISH | high | green_buy | bullish | 42.1 | 75.3 | Uptrend |
| 3 | KSHITIJPOL | Kshitij Polyline Limited | 16.2 | BULLISH | high | green_buy | bullish | 33.2 | 79.6 | Uptrend |
| 4 | BIRLACABLE | Birla Cable Limited | 16.2 | BULLISH | high | green_buy | bullish | 25.4 | 74.7 | Sideways / range-bound |
| 5 | E2E | E2E Networks Limited | 16.0 | BULLISH | high | green_buy | bullish | 37.4 | 79.3 | Uptrend |
| 6 | SKIPPER | Skipper Limited | 15.9 | BULLISH | high | green_buy | bullish | 38.2 | 78.3 | Uptrend |
| 7 | SYRMA | Syrma SGS Technology Limit | 15.7 | BULLISH | medium | green_buy | bullish | 40.3 | 74.8 | Uptrend |
| 8 | HFCL | HFCL Limited | 15.7 | BULLISH | high | green_buy | bullish | 61.9 | 84.9 | Uptrend |
| 9 | 526775 | Valiant Communications Ltd | 15.4 | BULLISH | high | green_buy | bullish | 35.4 | 73.2 | Uptrend |
| 10 | HINDALCO | Hindalco Industries Limite | 15.3 | BULLISH | high | green_buy | bullish | 30.7 | 65.6 | Uptrend |
| 11 | OMAXAUTO | Omax Autos Limited | 15.3 | BULLISH | high | green_buy | bullish | 54.3 | 68.2 | Uptrend |
| 12 | FCL | Fineotex Chemical Limited | 14.9 | BULLISH | high | green_buy | bullish | 47.2 | 80.5 | Uptrend |
| 13 | CGPOWER | CG Power and Industrial So | 14.8 | BULLISH | high | green_buy | bullish | 29.1 | 63.2 | Uptrend |
| 14 | STLTECH | Sterlite Technologies Limi | 14.7 | BULLISH | high | green_buy | bullish | 65.0 | 91.9 | Uptrend |
| 15 | GVPIL | GE Power India Limited | 14.7 | BULLISH | high | green_buy | bullish | 55.3 | 72.6 | Uptrend |
| 16 | GHCLTEXTIL | GHCL Textiles Limited | 14.5 | BULLISH | medium | green_buy | bullish | 26.0 | 59.6 | Uptrend |
| 17 | HIRECT | Hind Rectifiers Limited | 14.3 | BULLISH | medium | green_buy | bullish | 32.5 | 65.9 | Uptrend |
| 18 | 534755 | Trio Mercantile & Trading  | 14.2 | BULLISH | medium | green_buy | bullish | 59.2 | 83.5 | Uptrend |
| 19 | OFSS | Oracle Financial Services  | 14.0 | BULLISH | high | green_buy | bullish | 37.8 | 69.9 | Uptrend |
| 20 | MARKSANS | Marksans Pharma Limited | 14.0 | BULLISH | high | green_buy | bullish | 45.9 | 67.5 | Uptrend |
| 21 | DJML | DJ Mediaprint & Logistics  | 13.8 | BULLISH | high | green_buy | bullish | 21.1 | 70.7 | Uptrend |
| 22 | 539669 | RGF Capital Markets Ltd | 13.7 | BULLISH | medium | green_buy | bullish | 39.4 | 76.3 | Downtrend |
| 23 | YASHO | Yasho Industries Limited | 13.7 | BULLISH | high | green_buy | bullish | 38.4 | 69.5 | Uptrend |
| 24 | BALAMINES | Balaji Amines Limited | 13.5 | BULLISH | high | green_buy | bullish | 42.2 | 72.9 | Uptrend |
| 25 | CONFIPET | Confidence Petroleum India | 13.5 | BULLISH | high | green_buy | bullish | 43.3 | 66.6 | Uptrend |

## Bottom 15 (deteriorating — caution / avoid despite the 6m gain)
| # | Symbol | Company | Score | Verdict | Supertrend | Trend |
|--:|---|---|--:|---|---|---|
| 297 | CLEANMAX | Clean Max Enviro Energy So | -3.7 | MILD BEARISH | red_sell | Sideways / range-bound |
| 298 | GUJALKALI | Gujarat Alkalies and Chemi | -4.0 | BEARISH | red_sell | Downtrend |
| 299 | FINCABLES | Finolex Cables Limited | -4.0 | BEARISH | red_sell | Uptrend |
| 300 | ROLEXRINGS | Rolex Rings Limited | -4.0 | BEARISH | green_buy | Downtrend |
| 301 | EMPOWER | Empower India Limited | -4.7 | BEARISH | red_sell | Sideways / range-bound |
| 302 | GROWW | Billionbrains Garage Ventu | -4.7 | BEARISH | red_sell | Downtrend |
| 303 | GAUDIUMIVF | Gaudium IVF and Women Heal | -4.8 | BEARISH | green_buy | Downtrend |
| 304 | 544023 | Kalyani Cast-Tech Ltd | -5.0 | BEARISH | green_buy | Downtrend |
| 305 | 542046 | Vivid Mercantile Ltd | -5.3 | BEARISH | red_sell | Downtrend |
| 306 | VIVIMEDLAB | Vivimed Labs Limited | -5.8 | BEARISH | red_sell | Downtrend |
| 307 | AVANTIFEED | Avanti Feeds Limited | -6.4 | BEARISH | red_sell | Downtrend |
| 308 | QPOWER | Quality Power Electrical E | -7.0 | BEARISH | red_sell | Downtrend |
| 309 | 540492 | Starlineps Enterprises Ltd | -7.7 | BEARISH | red_sell | Downtrend |
| 310 | JINDALPOLY | Jindal Poly Films Limited | -7.9 | BEARISH | red_sell | Sideways / range-bound |
| 311 | KSR | KSR Footwear Limited | -8.3 | BEARISH | red_sell | Sideways / range-bound |

**Files:** `PHASE2_SCORECARD.csv` (full 40-column table) · `indicators.csv` · `candles.csv` · `patterns.csv` · `reports/` (311 per-stock scorecards).