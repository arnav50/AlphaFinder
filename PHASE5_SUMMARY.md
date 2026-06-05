# PHASE 5 — MOVE-INITIATION FINGERPRINT (DNA at Day 0)
Day-0 captured for **311 stocks** · 269 confirmed with a volume spike (≥1.4× 50-day avg) + breakout above 20-bar structure + strong bullish close.

## ✓ VERIFICATION CHECKPOINT (Phase 5)
- ✅ Day 0 identified for every stock; **269/311** verified via volume spike (median spike **3.3×**), rest via base-breakout fallback
- ✅ All leading + lagging + price-action + structure indicators recorded at Day 0 (`PHASE5_DAY0.csv`)
- ✅ 5-day pre-move context recorded (volume/RSI/range/VDU/shakeout)
- ✅ Aggregate fingerprint table with consistency % built (`PHASE5_FINGERPRINT.csv`)
- ✅ Top-5 most consistent indicators identified (prime filters)
- ✅ Fingerprint exported — input for Phase 7

## 🧬 THE FINGERPRINT — indicator state at move initiation
| Indicator | Min | Max | Avg | Median | Most common zone | Consistency % |
|---|--:|--:|--:|--:|---|--:|
| RSI(14) | 15.9 | 100.0 | 68.3 | 66.5 | 60-70 | **55.9%** |
| Stochastic %K | 9.6 | 100.0 | 76.8 | 82.2 | 80-100 | **55.1%** |
| Stochastic %D | 4.4 | 100.0 | 68.6 | 74.2 | 80-100 | **37.3%** |
| Bollinger %B | 22.3 | 159.0 | 112.6 | 113.6 | >100 | **83.8%** |
| BB width % | 3.6 | 312.9 | 21.9 | 18.8 | 20-30 | **30.7%** |
| CCI(20) | -70.5 | 1333.3 | 157.4 | 146.9 | 100-200 | **56.2%** |
| Williams %R | -81.7 | -0.0 | -10.9 | -8.0 | -20..0 | **79.2%** |
| MFI(14) | 27.5 | 99.6 | 73.8 | 74.8 | 60-80 | **50.3%** |
| MACD hist | -1.9 | 493.6 | 9.4 | 2.8 | >0(pos) | **95.8%** |
| ADX(14) | 10.8 | 99.5 | 24.5 | 21.7 | <20 | **39.2%** |
| ATR % | 1.1 | 10.0 | 4.5 | 4.3 | 3-5 | **56.0%** |
| % vs EMA200 | -78.9 | 415.0 | 5.3 | 3.4 | <0 | **33.0%** |
| % from 52w high | -96.6 | 0.0 | -18.4 | -16.5 | -30..-15 | **30.2%** |
| Vol × 50d-avg | 0.0 | 50.0 | 5.4 | 3.3 | 2-4 | **32.2%** |

### Categorical state at Day 0
| Indicator | Most common | Consistency % |
|---|---|--:|
| Supertrend | green | 90.4% |
| EMA alignment | bearish | 36.3% |
| OBV direction | already_rising | 93.2% |
| MACD vs zero | above | 68.2% |
| BB position | upper | 88.9% |

### Structure triggers on Day 0 (% of stocks = Y)
| Trigger | % Yes |
|---|--:|
| bos_triggered | 94.5% |
| vcp_pivot_broken | 49.8% |
| demand_zone_reclaimed | 65.0% |
| order_block_broken | 92.6% |

### 5-day pre-move context (dominant mode)
| Context | Dominant | % |
|---|---|--:|
| Pre-5d volume | rising | 59.5% |
| Pre-5d RSI | turning_up | 72.3% |
| Pre tight range | Y | 56.6% |
| Pre VDU | N | 64.0% |
| Pre shakeout | N | 57.6% |

## 🎯 TOP 5 MOST CONSISTENT INDICATORS (prime filters for Phase 7)
| Rank | Indicator | Zone | Consistency % |
|--:|---|---|--:|
| 1 | MACD hist | >0(pos) | **95.8%** |
| 2 | OBV direction | already_rising | **93.2%** |
| 3 | Supertrend | green | **90.4%** |
| 4 | BB position | upper | **88.9%** |
| 5 | Bollinger %B | >100 | **83.8%** |

## 📌 Plain-language DNA of a move start
> A typical Day-0 breakout fired with **RSI ≈ 66**, **Stoch %K ≈ 82**, **MFI ≈ 75**, **CCI ≈ 147** (>100 = thrust), **ADX ≈ 22** (trend just beginning), **ATR ≈ 4.3%** of price, price **+3.4% vs EMA200** (just reclaimed) and **-16% below its 52-week high** (room to run), on **3.3× average volume**, Supertrend **green**, with a **above-zero MACD**. A Break of Structure triggered in **95%** of cases.

### Disclosure
- Day 0 = earliest validated breakout after the recent base low (volume ≥1.4×, close>20-bar high, bullish close in upper half). RSI/Stoch read at the Day-0 *close* are momentum-elevated by construction (the breakout bar itself) — this is the breakout signature, not a pre-breakout reading.
- Consistency % = share of stocks falling in the single most-common bin (bin widths shown in the zone). Wider zones naturally score higher; compare within similar bin widths.

**Files:** `PHASE5_DAY0.csv` (per-stock Day-0 snapshot + pre-context) · `PHASE5_FINGERPRINT.csv` (this table).