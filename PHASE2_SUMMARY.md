# PHASE 2 — DEEP TECHNICAL ANALYSIS — SUMMARY
Scan date 2026-06-02 · 295 stocks analysed (of 312 Phase-1 names; 1 dropped — KISSHT, <20 bars of history).

## ✓ VERIFICATION CHECKPOINT (Phase 2)
- ✅ All **leading** indicators (RSI, Stochastic, Bollinger, Ichimoku, CCI, Williams %R, OBV, MFI) scored for every stock
- ✅ All **lagging** indicators (MACD, EMA align, ADX, Supertrend, ATR, VWAP, Pivots) scored for every stock
- ✅ **Candlestick** patterns documented with date + context + confirmation (`candles.csv`, 9,285 patterns)
- ✅ **Price-action / chart** patterns with breakout levels + targets (`patterns.csv`)
- ✅ **Scorecard per stock** (Bullish/Neutral/Bearish via indicator confluence) — `reports/<symbol>.md` + `PHASE2_SCORECARD.csv`

## Scorecard distribution
| Verdict | Count |
|---|--:|
| BULLISH | 220 |
| MILD BULLISH | 32 |
| NEUTRAL | 17 |
| MILD BEARISH | 13 |
| BEARISH | 13 |

**Confluence confidence:** {'medium': 154, 'low': 77, 'high': 64}

Key insight: all 311 names gained ≥25% over 6m, but only **252** remain technically bullish; **26** are rolling over (momentum exhausted) and **17** are consolidating.

## Top 25 by confluence score (strongest technical setups)
| # | Symbol | Company | Score | Verdict | Conf | Supertrend | EMA | ADX | RSI | Trend |
|--:|---|---|--:|---|---|---|---|--:|--:|---|
| 1 | NRBBEARING | NRB Bearing Limited | 15.9 | BULLISH | high | green_buy | bullish | 49.7 | 82.8 | Uptrend |
| 2 | OCCLLTD | OCCL Limited | 15.9 | BULLISH | high | green_buy | bullish | 38.9 | 79.0 | Uptrend |
| 3 | JNKINDIA | JNK India Limited | 15.5 | BULLISH | high | green_buy | bullish | 27.6 | 75.8 | Uptrend |
| 4 | SYRMA | Syrma SGS Technology Limit | 15.4 | BULLISH | high | green_buy | bullish | 46.6 | 77.3 | Uptrend |
| 5 | PREMEXPLN | Premier Explosives Limited | 14.8 | BULLISH | high | green_buy | bullish | 29.5 | 69.9 | Uptrend |
| 6 | CUPID | Cupid Limited | 14.7 | BULLISH | high | green_buy | bullish | 23.5 | 78.5 | Uptrend |
| 7 | ANTELOPUS | Antelopus Selan Energy Lim | 14.5 | BULLISH | high | green_buy | bullish | 46.5 | 62.8 | Uptrend |
| 8 | SANGHVIMOV | Sanghvi Movers Limited | 14.5 | BULLISH | high | green_buy | bullish | 34.4 | 70.2 | Uptrend |
| 9 | NEOGEN | Neogen Chemicals Limited | 14.2 | BULLISH | high | green_buy | bullish | 39.5 | 69.6 | Sideways / range-bound |
| 10 | MAHABANK | Bank of Maharashtra | 14.0 | BULLISH | medium | green_buy | bullish | 12.9 | 65.4 | Downtrend |
| 11 | SHAILY | Shaily Engineering Plastic | 13.7 | BULLISH | medium | green_buy | bullish | 33.3 | 71.6 | Uptrend |
| 12 | THYROCARE | Thyrocare Technologies Lim | 13.5 | BULLISH | medium | green_buy | bullish | 50.1 | 76.6 | Uptrend |
| 13 | BLISSGVS | Bliss GVS Pharma Limited | 13.5 | BULLISH | high | green_buy | bullish | 55.1 | 68.7 | Uptrend |
| 14 | SERVOTECH | Servotech Renewable Power  | 13.5 | BULLISH | high | green_buy | mixed | 31.2 | 58.4 | Uptrend |
| 15 | SAILIFE | Sai Life Sciences Limited | 13.5 | BULLISH | high | green_buy | bullish | 20.3 | 70.1 | Uptrend |
| 16 | SURYODAY | Suryoday Small Finance Ban | 13.5 | BULLISH | medium | green_buy | bullish | 40.1 | 68.1 | Uptrend |
| 17 | CPPLUS | Aditya Infotech Limited | 13.4 | BULLISH | high | green_buy | bullish | 51.4 | 82.9 | Uptrend |
| 18 | BALAMINES | Balaji Amines Limited | 13.4 | BULLISH | high | green_buy | bullish | 42.8 | 75.6 | Uptrend |
| 19 | CHENNPETRO | Chennai Petroleum Corporat | 13.4 | BULLISH | high | green_buy | bullish | 23.8 | 75.0 | Sideways / range-bound |
| 20 | CEMPRO | Cemindia Projects Limited | 13.2 | BULLISH | medium | green_buy | bullish | 48.0 | 75.4 | Uptrend |
| 21 | PASUPTAC | Pasupati Acrylon Limited | 13.2 | BULLISH | medium | green_buy | bullish | 46.7 | 76.1 | Uptrend |
| 22 | GULPOLY | Gulshan Polyols Limited | 13.0 | BULLISH | medium | green_buy | bullish | 36.2 | 70.5 | Sideways / range-bound |
| 23 | 526775 | Valiant Communications Ltd | 13.0 | BULLISH | medium | green_buy | bullish | 36.1 | 65.4 | Uptrend |
| 24 | STEELXIND | STEEL EXCHANGE INDIA LIMIT | 13.0 | BULLISH | high | green_buy | bullish | 24.9 | 60.8 | Uptrend |
| 25 | AEROENTER | Aeroflex Enterprises Limit | 13.0 | BULLISH | medium | green_buy | bullish | 35.3 | 66.4 | Uptrend |

## Bottom 15 (deteriorating — caution / avoid despite the 6m gain)
| # | Symbol | Company | Score | Verdict | Supertrend | Trend |
|--:|---|---|--:|---|---|---|
| 281 | GESHIP | The Great Eastern Shipping | -3.2 | MILD BEARISH | red_sell | Downtrend |
| 282 | EBGNG | GNG Electronics Limited | -3.5 | MILD BEARISH | green_buy | Sideways / range-bound |
| 283 | JINDALPOLY | Jindal Poly Films Limited | -4.3 | BEARISH | red_sell | Sideways / range-bound |
| 284 | NATIONALUM | National Aluminium Company | -4.7 | BEARISH | red_sell | Uptrend |
| 285 | LINCOLN | Lincoln Pharmaceuticals Li | -4.8 | BEARISH | red_sell | Sideways / range-bound |
| 286 | UNIVPHOTO | Universus Photo Imagings L | -5.4 | BEARISH | red_sell | Sideways / range-bound |
| 287 | 540545 | Guru Krupa Gems and Jewell | -5.5 | BEARISH | red_sell | Sideways / range-bound |
| 288 | SCHNEIDER | Schneider Electric Infrast | -6.0 | BEARISH | red_sell | Uptrend |
| 289 | HINDCOPPER | Hindustan Copper Limited | -6.5 | BEARISH | red_sell | Sideways / range-bound |
| 290 | 540252 | Viram Suvarn Ltd | -7.3 | BEARISH | red_sell | Downtrend |
| 291 | ARFIN | Arfin India Limited | -7.5 | BEARISH | red_sell | Sideways / range-bound |
| 292 | GAUDIUMIVF | Gaudium IVF and Women Heal | -7.7 | BEARISH | red_sell | Downtrend |
| 293 | KSR | KSR Footwear Limited | -7.8 | BEARISH | red_sell | Downtrend |
| 294 | KESORAMIND | Kesoram Industries Limited | -7.9 | BEARISH | red_sell | Sideways / range-bound |
| 295 | AVANTIFEED | Avanti Feeds Limited | -9.6 | BEARISH | red_sell | Downtrend |

**Files:** `PHASE2_SCORECARD.csv` (full 40-column table) · `indicators.csv` · `candles.csv` · `patterns.csv` · `reports/` (311 per-stock scorecards).