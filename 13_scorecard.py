"""Phase 2 scorecard: confluence scoring -> Bullish / Neutral / Bearish per stock.
Transparent additive model with component sub-scores. Outputs PHASE2_SCORECARD.csv."""
import pandas as pd, numpy as np

ind = pd.read_csv("indicators.csv", dtype={"symbol": str})
cnd = pd.read_csv("candles_summary.csv", dtype={"symbol": str})
pat = pd.read_csv("patterns.csv", dtype={"symbol": str})
p1  = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})

df = ind.merge(cnd, on="symbol", how="left").merge(pat, on="symbol", how="left") \
        .merge(p1[["symbol","name","exchange","return_pct_final","mktcap_cr","cap_bucket","sector"]],
               on="symbol", how="left")

BULL_CHART = {"Double Bottom","Inverse Head & Shoulders","Bull Flag / Pennant","Falling Wedge (bullish)",
              "Rounding Bottom (saucer)","Ascending Triangle"}
BEAR_CHART = {"Double Top","Head & Shoulders","Rising Wedge (bearish)","Descending Triangle"}

def score_row(r):
    L = 0.0   # leading
    # RSI
    rs = r.get("rsi_state"); rt = r.get("rsi_trend")
    L += {"overbought":-0.5,"oversold":0.5,"neutral":0.0}.get(rs,0)
    L += {"rising":0.5,"falling":-0.5,"flat":0.0,"n/a":0}.get(rt,0)
    L += {"bullish":1,"bearish":-1}.get(r.get("rsi_div"),0)
    # Stoch
    L += {"bull":0.5,"bear":-0.5}.get(r.get("stoch_cross"),0)
    L += {"overbought":-0.3,"oversold":0.3}.get(r.get("stoch_state"),0)
    L += {"bullish":0.5,"bearish":-0.5}.get(r.get("stoch_div"),0)
    # Bollinger
    L += {"above_upper":0.3,"above_mid":0.3,"below_mid":-0.3,"below_lower":-0.5}.get(r.get("bb_pos"),0)
    # Ichimoku
    L += {"above":1,"below":-1,"inside":0,"n/a":0}.get(r.get("ichi_price_cloud"),0)
    L += {"bullish":0.5,"bearish":-0.5}.get(r.get("ichi_tk"),0)
    L += {"above":0.5,"below":-0.5}.get(r.get("ichi_chikou"),0)
    # CCI
    L += {"strong_up":1,"above0":0.5,"below0":-0.5,"strong_down":-1}.get(r.get("cci_state"),0)
    # Williams
    L += {"overbought":-0.3,"oversold":0.3,"neutral":0}.get(r.get("wr_state"),0)
    # OBV
    L += {"rising":1,"falling":-1,"flat":0,"n/a":0}.get(r.get("obv_trend"),0)
    L += {"bullish":1,"bearish":-1}.get(r.get("obv_div"),0)
    # MFI
    L += {"overbought":-0.3,"oversold":0.3,"neutral":0}.get(r.get("mfi_state"),0)

    G = 0.0   # lagging
    G += {"above_signal":1,"below_signal":-1}.get(r.get("macd_pos"),0)
    G += {"expanding_pos":0.5,"contracting_pos":0.0,"expanding_neg":-0.5,"contracting_neg":0.0}.get(r.get("macd_hist_state"),0)
    G += {"bull":0.5,"bear":-0.5}.get(r.get("macd_cross"),0)
    G += {"above":0.5,"below":-0.5}.get(r.get("macd_zero"),0)
    G += {"bullish":2,"bearish":-2,"mixed":0}.get(str(r.get("ema_alignment")).split()[0] if pd.notna(r.get("ema_alignment")) else "",{}) if False else \
         {"bullish":2,"bearish":-2}.get(r.get("ema_alignment"),0)
    G += {"above":1,"below":-1,"n/a":0}.get(r.get("px_vs_e200"),0)
    G += {"rising":0.5,"falling":-0.5,"flat":0,"n/a":0}.get(r.get("ema200_slope"),0)
    if r.get("adx_regime")=="trending":
        G += 1 if r.get("di")=="+DI>-DI" else -1
    G += {"green_buy":1,"red_sell":-1}.get(r.get("supertrend"),0)
    G += {"buy_flip":0.5,"sell_flip":-0.5}.get(r.get("supertrend_flip"),0)
    G += {"above":0.5,"below":-0.5,"n/a":0}.get(r.get("px_vs_vwap"),0)
    G += {"above_R2":0.5,"above_R1":0.3,"below_S1":-0.5,"mid_range":0,"n/a":0}.get(r.get("px_vs_wpivot"),0)

    C = {"bullish":1,"bearish":-1,"neutral":0}.get(r.get("candle_bias"),0)   # candles

    P = 0.0   # price action
    ts = str(r.get("trend_structure"))
    if ts.startswith("Uptrend"): P += 1.5
    elif ts.startswith("Downtrend"): P -= 1.5
    cp = r.get("chart_pattern")
    if cp in BULL_CHART: P += 1
    elif cp in BEAR_CHART: P -= 1

    total = round(L+G+C+P, 2)
    return pd.Series({"leading_score":round(L,2),"lagging_score":round(G,2),
                      "candle_score":C,"price_action_score":round(P,2),"total_score":total})

sc = df.apply(score_row, axis=1)
df = pd.concat([df, sc], axis=1)

def verdict(t):
    if t >= 4: return "BULLISH"
    if t >= 1.5: return "MILD BULLISH"
    if t > -1.5: return "NEUTRAL"
    if t > -4: return "MILD BEARISH"
    return "BEARISH"
df["scorecard"] = df["total_score"].apply(verdict)

# confidence = how aligned the 4 components are (all same sign = high)
def conf(r):
    comps = [r["leading_score"], r["lagging_score"], r["candle_score"], r["price_action_score"]]
    pos = sum(1 for x in comps if x > 0.3); neg = sum(1 for x in comps if x < -0.3)
    if max(pos,neg) >= 4: return "high"
    if max(pos,neg) == 3: return "medium"
    return "low"
df["confluence_confidence"] = df.apply(conf, axis=1)

cols = ["symbol","name","exchange","sector","return_pct_final","close","cap_bucket","bars",
        "leading_score","lagging_score","candle_score","price_action_score","total_score",
        "scorecard","confluence_confidence",
        "rsi","rsi_state","stoch_k","stoch_d","macd_pos","ema_alignment","px_vs_e200","ema200_slope",
        "adx","adx_regime","di","supertrend","supertrend_flip","ichi_price_cloud","cci","mfi",
        "candle_bias","bullish_candles","bearish_candles","trend_structure","chart_pattern",
        "breakout_level","target","volume_confirm","bb_squeeze","atr_pct"]
df = df.sort_values("total_score", ascending=False).reset_index(drop=True)
df.insert(0,"ta_rank",df.index+1)
df[["ta_rank"]+cols].to_csv("PHASE2_SCORECARD.csv", index=False)

print("=== SCORECARD DISTRIBUTION ===")
print(df["scorecard"].value_counts().reindex(["BULLISH","MILD BULLISH","NEUTRAL","MILD BEARISH","BEARISH"]).to_string())
print("\nconfidence:", df["confluence_confidence"].value_counts().to_dict())
print(f"total_score: min={df['total_score'].min()} median={df['total_score'].median()} max={df['total_score'].max()}")
print("\n=== TOP 15 by confluence score ===")
print(df[["ta_rank","symbol","name","total_score","scorecard","confluence_confidence","supertrend","ema_alignment","adx"]].head(15).to_string(index=False))
print("\n=== BOTTOM 10 (weakest) ===")
print(df[["ta_rank","symbol","name","total_score","scorecard","supertrend","trend_structure"]].tail(10).to_string(index=False))
