# PHASE 5 — MOVE-INITIATION FINGERPRINT (DNA at Day 0)
Day-0 captured for **543 stocks** · 483 confirmed with a volume spike (≥1.4× 50-day avg) + breakout above 20-bar structure + strong bullish close.

## ✓ VERIFICATION CHECKPOINT (Phase 5)
- ✅ Day 0 identified for every stock; **483/543** verified via volume spike (median spike **3.2×**), rest via base-breakout fallback
- ✅ All leading + lagging + price-action + structure indicators recorded at Day 0 (`PHASE5_DAY0.csv`)
- ✅ 5-day pre-move context recorded (volume/RSI/range/VDU/shakeout)
- ✅ Aggregate fingerprint table with consistency % built (`PHASE5_FINGERPRINT.csv`)
- ✅ Top-5 most consistent indicators identified (prime filters)
- ✅ Fingerprint exported — input for Phase 7

## 🧬 THE FINGERPRINT — indicator state at move initiation
| Indicator | Min | Max | Avg | Median | Most common zone | Consistency % |
|---|--:|--:|--:|--:|---|--:|
| RSI(14) | 15.9 | 100.0 | 66.9 | 66.5 | 60-70 | **58.7%** |
| Stochastic %K | 9.6 | 100.0 | 76.2 | 81.5 | 80-100 | **52.6%** |
| Stochastic %D | 4.4 | 100.0 | 68.3 | 73.4 | 60-80 | **36.0%** |
| Bollinger %B | 19.4 | 156.4 | 111.1 | 112.9 | >100 | **82.2%** |
| BB width % | 3.6 | 109.0 | 20.6 | 18.8 | 20-30 | **31.8%** |
| CCI(20) | -127.1 | 442.5 | 141.6 | 134.7 | 100-200 | **57.9%** |
| Williams %R | -81.7 | -0.0 | -11.2 | -8.1 | -20..0 | **78.3%** |
| MFI(14) | 0.9 | 99.6 | 72.7 | 74.4 | 60-80 | **45.5%** |
| MACD hist | -19.6 | 493.6 | 10.2 | 3.6 | >0(pos) | **95.6%** |
| ADX(14) | 9.9 | 100.0 | 23.3 | 21.4 | <20 | **41.8%** |
| ATR % | 1.3 | 11.1 | 4.5 | 4.4 | 3-5 | **64.8%** |
| % vs EMA200 | -70.0 | 60.6 | 3.0 | 3.2 | <0 | **37.7%** |
| % from 52w high | -90.9 | 0.0 | -21.2 | -19.8 | -30..-15 | **34.4%** |
| Vol × 50d-avg | 0.1 | 41.5 | 5.7 | 3.2 | 2-4 | **31.5%** |

### Categorical state at Day 0
| Indicator | Most common | Consistency % |
|---|---|--:|
| Supertrend | green | 88.0% |
| EMA alignment | bearish | 44.0% |
| OBV direction | already_rising | 89.9% |
| MACD vs zero | above | 68.1% |
| BB position | upper | 87.9% |

### Structure triggers on Day 0 (% of stocks = Y)
| Trigger | % Yes |
|---|--:|
| bos_triggered | 94.1% |
| vcp_pivot_broken | 49.9% |
| demand_zone_reclaimed | 71.5% |
| order_block_broken | 94.8% |

### 5-day pre-move context (dominant mode)
| Context | Dominant | % |
|---|---|--:|
| Pre-5d volume | rising | 54.5% |
| Pre-5d RSI | turning_up | 72.2% |
| Pre tight range | Y | 57.5% |
| Pre VDU | N | 61.1% |
| Pre shakeout | N | 55.6% |

## 🎯 TOP 5 MOST CONSISTENT INDICATORS (prime filters for Phase 7)
| Rank | Indicator | Zone | Consistency % |
|--:|---|---|--:|
| 1 | MACD hist | >0(pos) | **95.6%** |
| 2 | OBV direction | already_rising | **89.9%** |
| 3 | Supertrend | green | **88.0%** |
| 4 | BB position | upper | **87.9%** |
| 5 | Bollinger %B | >100 | **82.2%** |

## 📌 Plain-language DNA of a move start
> A typical Day-0 breakout fired with **RSI ≈ 66**, **Stoch %K ≈ 82**, **MFI ≈ 74**, **CCI ≈ 135** (>100 = thrust), **ADX ≈ 21** (trend just beginning), **ATR ≈ 4.4%** of price, price **+3.2% vs EMA200** (just reclaimed) and **-20% below its 52-week high** (room to run), on **3.2× average volume**, Supertrend **green**, with a **above-zero MACD**. A Break of Structure triggered in **94%** of cases.

### Disclosure
- Day 0 = earliest validated breakout after the recent base low (volume ≥1.4×, close>20-bar high, bullish close in upper half). RSI/Stoch read at the Day-0 *close* are momentum-elevated by construction (the breakout bar itself) — this is the breakout signature, not a pre-breakout reading.
- Consistency % = share of stocks falling in the single most-common bin (bin widths shown in the zone). Wider zones naturally score higher; compare within similar bin widths.

**Files:** `PHASE5_DAY0.csv` (per-stock Day-0 snapshot + pre-context) · `PHASE5_FINGERPRINT.csv` (this table).