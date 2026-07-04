# PHASE 5 — MOVE-INITIATION FINGERPRINT (DNA at Day 0)
Day-0 captured for **355 stocks** · 333 confirmed with a volume spike (≥1.4× 50-day avg) + breakout above 20-bar structure + strong bullish close.

## ✓ VERIFICATION CHECKPOINT (Phase 5)
- ✅ Day 0 identified for every stock; **333/355** verified via volume spike (median spike **3.3×**), rest via base-breakout fallback
- ✅ All leading + lagging + price-action + structure indicators recorded at Day 0 (`PHASE5_DAY0.csv`)
- ✅ 5-day pre-move context recorded (volume/RSI/range/VDU/shakeout)
- ✅ Aggregate fingerprint table with consistency % built (`PHASE5_FINGERPRINT.csv`)
- ✅ Top-5 most consistent indicators identified (prime filters)
- ✅ Fingerprint exported — input for Phase 7

## 🧬 THE FINGERPRINT — indicator state at move initiation
| Indicator | Min | Max | Avg | Median | Most common zone | Consistency % |
|---|--:|--:|--:|--:|---|--:|
| RSI(14) | 15.9 | 100.0 | 67.5 | 66.6 | 60-70 | **60.6%** |
| Stochastic %K | 9.6 | 100.0 | 78.1 | 83.2 | 80-100 | **57.0%** |
| Stochastic %D | 4.4 | 100.0 | 70.5 | 75.3 | 80-100 | **39.9%** |
| Bollinger %B | 24.0 | 156.4 | 113.5 | 113.3 | >100 | **85.9%** |
| BB width % | 3.3 | 109.0 | 20.2 | 17.8 | 20-30 | **29.3%** |
| CCI(20) | -85.9 | 430.4 | 154.0 | 146.3 | 100-200 | **59.9%** |
| Williams %R | -81.7 | -0.0 | -10.2 | -7.8 | -20..0 | **81.4%** |
| MFI(14) | 0.9 | 97.7 | 73.7 | 75.1 | 60-80 | **47.8%** |
| MACD hist | -3.8 | 493.6 | 10.3 | 3.9 | >0(pos) | **97.4%** |
| ADX(14) | 10.2 | 100.0 | 22.9 | 21.0 | <20 | **44.8%** |
| ATR % | 1.6 | 10.2 | 4.4 | 4.3 | 3-5 | **64.8%** |
| % vs EMA200 | -63.1 | 60.2 | 4.6 | 3.9 | <0 | **32.5%** |
| % from 52w high | -86.3 | 0.0 | -19.3 | -18.0 | -30..-15 | **33.8%** |
| Vol × 50d-avg | 0.3 | 39.9 | 5.3 | 3.3 | 2-4 | **32.4%** |

### Categorical state at Day 0
| Indicator | Most common | Consistency % |
|---|---|--:|
| Supertrend | green | 92.7% |
| EMA alignment | bearish | 39.4% |
| OBV direction | already_rising | 92.1% |
| MACD vs zero | above | 72.7% |
| BB position | upper | 92.5% |

### Structure triggers on Day 0 (% of stocks = Y)
| Trigger | % Yes |
|---|--:|
| bos_triggered | 97.5% |
| vcp_pivot_broken | 52.7% |
| demand_zone_reclaimed | 72.7% |
| order_block_broken | 94.9% |

### 5-day pre-move context (dominant mode)
| Context | Dominant | % |
|---|---|--:|
| Pre-5d volume | rising | 55.2% |
| Pre-5d RSI | turning_up | 74.9% |
| Pre tight range | Y | 58.9% |
| Pre VDU | N | 62.3% |
| Pre shakeout | N | 55.8% |

## 🎯 TOP 5 MOST CONSISTENT INDICATORS (prime filters for Phase 7)
| Rank | Indicator | Zone | Consistency % |
|--:|---|---|--:|
| 1 | MACD hist | >0(pos) | **97.4%** |
| 2 | Supertrend | green | **92.7%** |
| 3 | BB position | upper | **92.5%** |
| 4 | OBV direction | already_rising | **92.1%** |
| 5 | Bollinger %B | >100 | **85.9%** |

## 📌 Plain-language DNA of a move start
> A typical Day-0 breakout fired with **RSI ≈ 67**, **Stoch %K ≈ 83**, **MFI ≈ 75**, **CCI ≈ 146** (>100 = thrust), **ADX ≈ 21** (trend just beginning), **ATR ≈ 4.3%** of price, price **+3.9% vs EMA200** (just reclaimed) and **-18% below its 52-week high** (room to run), on **3.3× average volume**, Supertrend **green**, with a **above-zero MACD**. A Break of Structure triggered in **97%** of cases.

### Disclosure
- Day 0 = earliest validated breakout after the recent base low (volume ≥1.4×, close>20-bar high, bullish close in upper half). RSI/Stoch read at the Day-0 *close* are momentum-elevated by construction (the breakout bar itself) — this is the breakout signature, not a pre-breakout reading.
- Consistency % = share of stocks falling in the single most-common bin (bin widths shown in the zone). Wider zones naturally score higher; compare within similar bin widths.

**Files:** `PHASE5_DAY0.csv` (per-stock Day-0 snapshot + pre-context) · `PHASE5_FINGERPRINT.csv` (this table).