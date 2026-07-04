# PHASE 5 — MOVE-INITIATION FINGERPRINT (DNA at Day 0)
Day-0 captured for **376 stocks** · 354 confirmed with a volume spike (≥1.4× 50-day avg) + breakout above 20-bar structure + strong bullish close.

## ✓ VERIFICATION CHECKPOINT (Phase 5)
- ✅ Day 0 identified for every stock; **354/376** verified via volume spike (median spike **3.2×**), rest via base-breakout fallback
- ✅ All leading + lagging + price-action + structure indicators recorded at Day 0 (`PHASE5_DAY0.csv`)
- ✅ 5-day pre-move context recorded (volume/RSI/range/VDU/shakeout)
- ✅ Aggregate fingerprint table with consistency % built (`PHASE5_FINGERPRINT.csv`)
- ✅ Top-5 most consistent indicators identified (prime filters)
- ✅ Fingerprint exported — input for Phase 7

## 🧬 THE FINGERPRINT — indicator state at move initiation
| Indicator | Min | Max | Avg | Median | Most common zone | Consistency % |
|---|--:|--:|--:|--:|---|--:|
| RSI(14) | 15.9 | 100.0 | 67.3 | 66.8 | 60-70 | **59.3%** |
| Stochastic %K | 9.6 | 100.0 | 77.9 | 83.2 | 80-100 | **56.9%** |
| Stochastic %D | 4.4 | 100.0 | 70.6 | 75.1 | 80-100 | **40.5%** |
| Bollinger %B | 19.4 | 156.4 | 112.9 | 113.2 | >100 | **85.7%** |
| BB width % | 3.3 | 109.0 | 20.3 | 18.2 | 20-30 | **30.3%** |
| CCI(20) | -116.2 | 430.4 | 150.8 | 145.2 | 100-200 | **58.7%** |
| Williams %R | -81.7 | -0.0 | -10.5 | -7.6 | -20..0 | **80.9%** |
| MFI(14) | 0.9 | 97.7 | 73.1 | 74.7 | 60-80 | **49.1%** |
| MACD hist | -3.8 | 493.6 | 10.4 | 3.8 | >0(pos) | **96.7%** |
| ADX(14) | 10.2 | 100.0 | 22.9 | 21.0 | <20 | **44.6%** |
| ATR % | 1.6 | 11.1 | 4.4 | 4.3 | 3-5 | **64.7%** |
| % vs EMA200 | -63.1 | 59.9 | 4.1 | 3.4 | <0 | **35.8%** |
| % from 52w high | -86.3 | 0.0 | -19.7 | -18.5 | -30..-15 | **34.0%** |
| Vol × 50d-avg | 0.3 | 32.8 | 5.1 | 3.2 | 2-4 | **33.4%** |

### Categorical state at Day 0
| Indicator | Most common | Consistency % |
|---|---|--:|
| Supertrend | green | 92.8% |
| EMA alignment | bearish | 40.7% |
| OBV direction | already_rising | 91.2% |
| MACD vs zero | above | 73.1% |
| BB position | upper | 91.6% |

### Structure triggers on Day 0 (% of stocks = Y)
| Trigger | % Yes |
|---|--:|
| bos_triggered | 96.8% |
| vcp_pivot_broken | 53.5% |
| demand_zone_reclaimed | 73.7% |
| order_block_broken | 94.9% |

### 5-day pre-move context (dominant mode)
| Context | Dominant | % |
|---|---|--:|
| Pre-5d volume | rising | 54.8% |
| Pre-5d RSI | turning_up | 74.2% |
| Pre tight range | Y | 58.8% |
| Pre VDU | N | 62.5% |
| Pre shakeout | N | 56.1% |

## 🎯 TOP 5 MOST CONSISTENT INDICATORS (prime filters for Phase 7)
| Rank | Indicator | Zone | Consistency % |
|--:|---|---|--:|
| 1 | MACD hist | >0(pos) | **96.7%** |
| 2 | Supertrend | green | **92.8%** |
| 3 | BB position | upper | **91.6%** |
| 4 | OBV direction | already_rising | **91.2%** |
| 5 | Bollinger %B | >100 | **85.7%** |

## 📌 Plain-language DNA of a move start
> A typical Day-0 breakout fired with **RSI ≈ 67**, **Stoch %K ≈ 83**, **MFI ≈ 75**, **CCI ≈ 145** (>100 = thrust), **ADX ≈ 21** (trend just beginning), **ATR ≈ 4.3%** of price, price **+3.5% vs EMA200** (just reclaimed) and **-19% below its 52-week high** (room to run), on **3.2× average volume**, Supertrend **green**, with a **above-zero MACD**. A Break of Structure triggered in **97%** of cases.

### Disclosure
- Day 0 = earliest validated breakout after the recent base low (volume ≥1.4×, close>20-bar high, bullish close in upper half). RSI/Stoch read at the Day-0 *close* are momentum-elevated by construction (the breakout bar itself) — this is the breakout signature, not a pre-breakout reading.
- Consistency % = share of stocks falling in the single most-common bin (bin widths shown in the zone). Wider zones naturally score higher; compare within similar bin widths.

**Files:** `PHASE5_DAY0.csv` (per-stock Day-0 snapshot + pre-context) · `PHASE5_FINGERPRINT.csv` (this table).