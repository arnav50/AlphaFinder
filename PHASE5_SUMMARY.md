# PHASE 5 — MOVE-INITIATION FINGERPRINT (DNA at Day 0)
Day-0 captured for **295 stocks** · 270 confirmed with a volume spike (≥1.4× 50-day avg) + breakout above 20-bar structure + strong bullish close.

## ✓ VERIFICATION CHECKPOINT (Phase 5)
- ✅ Day 0 identified for every stock; **270/295** verified via volume spike (median spike **3.3×**), rest via base-breakout fallback
- ✅ All leading + lagging + price-action + structure indicators recorded at Day 0 (`PHASE5_DAY0.csv`)
- ✅ 5-day pre-move context recorded (volume/RSI/range/VDU/shakeout)
- ✅ Aggregate fingerprint table with consistency % built (`PHASE5_FINGERPRINT.csv`)
- ✅ Top-5 most consistent indicators identified (prime filters)
- ✅ Fingerprint exported — input for Phase 7

## 🧬 THE FINGERPRINT — indicator state at move initiation
| Indicator | Min | Max | Avg | Median | Most common zone | Consistency % |
|---|--:|--:|--:|--:|---|--:|
| RSI(14) | 15.9 | 100.0 | 67.1 | 66.4 | 60-70 | **63.1%** |
| Stochastic %K | 9.6 | 100.0 | 77.3 | 82.6 | 80-100 | **56.2%** |
| Stochastic %D | 4.4 | 100.0 | 69.5 | 75.4 | 80-100 | **38.8%** |
| Bollinger %B | 24.0 | 156.4 | 112.5 | 113.8 | >100 | **84.8%** |
| BB width % | 3.6 | 109.0 | 20.7 | 18.8 | 20-30 | **31.1%** |
| CCI(20) | -123.1 | 430.4 | 148.5 | 141.0 | 100-200 | **58.3%** |
| Williams %R | -81.7 | -0.0 | -10.4 | -7.7 | -20..0 | **82.1%** |
| MFI(14) | 22.8 | 97.5 | 72.9 | 74.4 | 60-80 | **48.4%** |
| MACD hist | -6.1 | 493.6 | 9.4 | 2.9 | >0(pos) | **96.1%** |
| ADX(14) | 11.2 | 99.3 | 24.0 | 21.5 | <20 | **39.7%** |
| ATR % | 1.2 | 10.0 | 4.4 | 4.3 | 3-5 | **59.1%** |
| % vs EMA200 | -79.0 | 61.1 | 3.6 | 3.1 | <0 | **35.1%** |
| % from 52w high | -96.6 | 0.0 | -19.2 | -18.0 | -30..-15 | **32.9%** |
| Vol × 50d-avg | 0.4 | 34.9 | 5.1 | 3.3 | 2-4 | **34.0%** |

### Categorical state at Day 0
| Indicator | Most common | Consistency % |
|---|---|--:|
| Supertrend | green | 92.2% |
| EMA alignment | bearish | 39.3% |
| OBV direction | already_rising | 92.2% |
| MACD vs zero | above | 70.8% |
| BB position | upper | 90.3% |

### Structure triggers on Day 0 (% of stocks = Y)
| Trigger | % Yes |
|---|--:|
| bos_triggered | 95.6% |
| vcp_pivot_broken | 50.8% |
| demand_zone_reclaimed | 69.8% |
| order_block_broken | 95.6% |

### 5-day pre-move context (dominant mode)
| Context | Dominant | % |
|---|---|--:|
| Pre-5d volume | rising | 57.6% |
| Pre-5d RSI | turning_up | 73.2% |
| Pre tight range | Y | 57.3% |
| Pre VDU | N | 67.5% |
| Pre shakeout | N | 55.9% |

## 🎯 TOP 5 MOST CONSISTENT INDICATORS (prime filters for Phase 7)
| Rank | Indicator | Zone | Consistency % |
|--:|---|---|--:|
| 1 | MACD hist | >0(pos) | **96.1%** |
| 2 | OBV direction | already_rising | **92.2%** |
| 3 | Supertrend | green | **92.2%** |
| 4 | BB position | upper | **90.3%** |
| 5 | Bollinger %B | >100 | **84.8%** |

## 📌 Plain-language DNA of a move start
> A typical Day-0 breakout fired with **RSI ≈ 66**, **Stoch %K ≈ 83**, **MFI ≈ 74**, **CCI ≈ 141** (>100 = thrust), **ADX ≈ 22** (trend just beginning), **ATR ≈ 4.3%** of price, price **+3.1% vs EMA200** (just reclaimed) and **-18% below its 52-week high** (room to run), on **3.3× average volume**, Supertrend **green**, with a **above-zero MACD**. A Break of Structure triggered in **96%** of cases.

### Disclosure
- Day 0 = earliest validated breakout after the recent base low (volume ≥1.4×, close>20-bar high, bullish close in upper half). RSI/Stoch read at the Day-0 *close* are momentum-elevated by construction (the breakout bar itself) — this is the breakout signature, not a pre-breakout reading.
- Consistency % = share of stocks falling in the single most-common bin (bin widths shown in the zone). Wider zones naturally score higher; compare within similar bin widths.

**Files:** `PHASE5_DAY0.csv` (per-stock Day-0 snapshot + pre-context) · `PHASE5_FINGERPRINT.csv` (this table).