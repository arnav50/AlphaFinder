# PHASE 2 — DEEP TECHNICAL ANALYSIS — SUMMARY
Scan date 2026-06-02 · 355 stocks analysed (of 312 Phase-1 names; 1 dropped — KISSHT, <20 bars of history).

## ✓ VERIFICATION CHECKPOINT (Phase 2)
- ✅ All **leading** indicators (RSI, Stochastic, Bollinger, Ichimoku, CCI, Williams %R, OBV, MFI) scored for every stock
- ✅ All **lagging** indicators (MACD, EMA align, ADX, Supertrend, ATR, VWAP, Pivots) scored for every stock
- ✅ **Candlestick** patterns documented with date + context + confirmation (`candles.csv`, 9,285 patterns)
- ✅ **Price-action / chart** patterns with breakout levels + targets (`patterns.csv`)
- ✅ **Scorecard per stock** (Bullish/Neutral/Bearish via indicator confluence) — `reports/<symbol>.md` + `PHASE2_SCORECARD.csv`

## Scorecard distribution
| Verdict | Count |
|---|--:|
| BULLISH | 271 |
| MILD BULLISH | 36 |
| NEUTRAL | 26 |
| MILD BEARISH | 11 |
| BEARISH | 11 |

**Confluence confidence:** {'medium': 183, 'low': 108, 'high': 64}

Key insight: all 311 names gained ≥25% over 6m, but only **307** remain technically bullish; **22** are rolling over (momentum exhausted) and **26** are consolidating.

## Top 25 by confluence score (strongest technical setups)
| # | Symbol | Company | Score | Verdict | Conf | Supertrend | EMA | ADX | RSI | Trend |
|--:|---|---|--:|---|---|---|---|--:|--:|---|
| 1 | ACUTAAS | Acutaas Chemicals Limited | 15.9 | BULLISH | high | green_buy | bullish | 48.6 | 75.6 | Uptrend |
| 2 | KRISHANA | Krishana Phoschem Limited | 15.3 | BULLISH | high | green_buy | bullish | 25.3 | 57.7 | Sideways / range-bound |
| 3 | OFSS | Oracle Financial Services  | 15.2 | BULLISH | high | green_buy | bullish | 26.6 | 71.7 | Uptrend |
| 4 | RATEGAIN | Rategain Travel Technologi | 15.2 | BULLISH | high | green_buy | bullish | 56.4 | 76.0 | Uptrend |
| 5 | FUSION | Fusion Finance Limited | 14.9 | BULLISH | high | green_buy | bullish | 23.0 | 72.4 | Uptrend |
| 6 | PGIL | Pearl Global Industries Li | 14.9 | BULLISH | high | green_buy | bullish | 52.1 | 73.3 | Uptrend |
| 7 | PRIVISCL | Privi Speciality Chemicals | 14.7 | BULLISH | high | green_buy | bullish | 28.6 | 69.9 | Sideways / range-bound |
| 8 | IBULLSLTD | Indiabulls Limited | 14.7 | BULLISH | high | green_buy | bullish | 39.8 | 72.8 | Uptrend |
| 9 | RML | Rane (Madras) Limited | 14.7 | BULLISH | high | green_buy | bullish | 46.0 | 75.2 | Uptrend |
| 10 | SANGHVIMOV | Sanghvi Movers Limited | 14.5 | BULLISH | high | green_buy | bullish | 45.7 | 69.4 | Uptrend |
| 11 | 511523 | Veerhealth Care Ltd | 14.4 | BULLISH | high | green_buy | bullish | 45.9 | 95.5 | Uptrend |
| 12 | XPROINDIA | Xpro India Limited | 14.4 | BULLISH | medium | green_buy | bullish | 47.1 | 77.2 | Uptrend |
| 13 | SANSERA | Sansera Engineering Limite | 14.4 | BULLISH | high | green_buy | bullish | 30.8 | 70.6 | Uptrend |
| 14 | SATIN | Satin Creditcare Network L | 14.4 | BULLISH | medium | green_buy | bullish | 31.3 | 69.4 | Uptrend |
| 15 | ONELIFECAP | Onelife Capital Advisors L | 14.4 | BULLISH | high | green_buy | bullish | 55.5 | 81.6 | Sideways / range-bound |
| 16 | NINSYS | NINtec Systems Limited | 14.2 | BULLISH | high | green_buy | bullish | 60.4 | 85.3 | Uptrend |
| 17 | DIFFNKG | Diffusion Engineers Limite | 14.2 | BULLISH | high | green_buy | bullish | 47.5 | 78.8 | Uptrend |
| 18 | WABAG | VA Tech Wabag Limited | 14.0 | BULLISH | high | green_buy | bullish | 43.9 | 70.3 | Uptrend |
| 19 | GHCLTEXTIL | GHCL Textiles Limited | 14.0 | BULLISH | high | green_buy | bullish | 20.3 | 63.1 | Uptrend |
| 20 | SURYODAY | Suryoday Small Finance Ban | 14.0 | BULLISH | high | green_buy | bullish | 36.3 | 68.6 | Uptrend |
| 21 | 526433 | ASM Technologies Ltd | 13.9 | BULLISH | high | green_buy | bullish | 38.4 | 72.5 | Uptrend |
| 22 | SETL | Standard Engineering Techn | 13.9 | BULLISH | high | green_buy | bullish | 54.5 | 90.9 | Uptrend |
| 23 | SKMEGGPROD | SKM Egg Products Export (I | 13.9 | BULLISH | medium | green_buy | bullish | 64.9 | 78.0 | Uptrend |
| 24 | STOVEKRAFT | Stove Kraft Limited | 13.8 | BULLISH | high | green_buy | bullish | 58.0 | 74.4 | Sideways / range-bound |
| 25 | RISHABH | Rishabh Instruments Limite | 13.7 | BULLISH | high | green_buy | bullish | 30.8 | 72.5 | Uptrend |

## Bottom 15 (deteriorating — caution / avoid despite the 6m gain)
| # | Symbol | Company | Score | Verdict | Supertrend | Trend |
|--:|---|---|--:|---|---|---|
| 341 | GESHIP | The Great Eastern Shipping | -2.3 | MILD BEARISH | red_sell | Downtrend |
| 342 | ADANIPOWER | Adani Power Limited | -2.8 | MILD BEARISH | red_sell | Sideways / range-bound |
| 343 | ADVAIT | Advait Energy Transitions  | -3.0 | MILD BEARISH | green_buy | Uptrend |
| 344 | VIDYAWIRES | Vidya Wires Limited | -3.2 | MILD BEARISH | green_buy | Downtrend |
| 345 | BSE | BSE Limited | -4.2 | BEARISH | red_sell | Sideways / range-bound |
| 346 | UNIVPHOTO | Universus Photo Imagings L | -4.8 | BEARISH | red_sell | Sideways / range-bound |
| 347 | 540252 | Viram Suvarn Ltd | -4.8 | BEARISH | red_sell | Downtrend |
| 348 | AGIIL | Agi Infra Limited | -5.0 | BEARISH | green_buy | Downtrend |
| 349 | JINDALPOLY | Jindal Poly Films Limited | -5.4 | BEARISH | red_sell | Sideways / range-bound |
| 350 | SEAMECLTD | Seamec Limited | -5.8 | BEARISH | red_sell | Downtrend |
| 351 | HARDWYN | Hardwyn India Limited | -5.8 | BEARISH | red_sell | Sideways / range-bound |
| 352 | NARMADA | Narmada Agrobase Limited | -6.0 | BEARISH | red_sell | Downtrend |
| 353 | KSR | KSR Footwear Limited | -6.3 | BEARISH | red_sell | Downtrend |
| 354 | APEX | Apex Frozen Foods Limited | -7.3 | BEARISH | red_sell | Downtrend |
| 355 | ATLANTAELE | Atlanta Electricals Limite | -7.7 | BEARISH | red_sell | Sideways / range-bound |

**Files:** `PHASE2_SCORECARD.csv` (full 40-column table) · `indicators.csv` · `candles.csv` · `patterns.csv` · `reports/` (311 per-stock scorecards).