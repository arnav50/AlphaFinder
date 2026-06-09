"""
Entry-pattern / price-action analysis: find the candle/pattern that INITIATED each
25%+ move, scanning from the BASE (before the move). Reuses 11_candles.py detectors.

'Move start' = base low = lowest close in trailing ~180 trading days (same proxy used in
leading_analysis.py). Base window = a few bars around that low.

Per stock:
  ENTRY (reversal at base) : strongest bullish reversal pattern in the base window
  CONFIRMATION (during move): first strong momentum/continuation candle after the base
  PRICE ACTION             : HH+HL sequence, support respected, breakout volume >=1.5x,
                             false-breakdown (bull-trap) reversal
  WEEKLY                   : strong bullish close at base, weekly support rejection
  Pattern Quality Score (1-10) via a transparent additive rubric.

Outputs: ENTRY_PATTERN_ANALYSIS.csv (full) + ENTRY_PATTERN_SCORECARD.csv (requested 5-col)
"""
import pickle, importlib.util, numpy as np, pandas as pd

# --- load 11_candles.py (digit-leading filename -> load by path) for its detectors ---
_spec = importlib.util.spec_from_file_location("candles_mod", "11_candles.py")
CN = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(CN)

# reversal patterns ranked strongest -> weakest (for picking the entry candle)
ENTRY_RANK = ["Three White Soldiers", "Bullish Engulfing", "Morning Star", "Piercing Line",
              "Hammer", "Inverted Hammer", "Dragonfly Doji", "Bullish Harami",
              "Tweezer Bottom", "Bullish Pin Bar", "Bullish Marubozu"]
ENTRY_STRONG = {"Three White Soldiers", "Bullish Engulfing", "Morning Star", "Piercing Line", "Hammer"}

def weekly(df):
    return (df.set_index("date").resample("W")
              .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
              .dropna().reset_index())

def best_entry(df, lo, hi):
    """strongest ranked bullish reversal pattern in bar window [lo,hi]; returns (name,date)."""
    found = {}
    for i in range(max(0, lo), min(len(df), hi)):
        for p in CN.detect_at(df, i):
            if p in CN.BULL and p not in found:
                found[p] = df["date"].iloc[i].date().isoformat()
    for p in ENTRY_RANK:
        if p in found:
            return p, found[p]
    return "none", ""

def first_continuation(df, lo, hi):
    o, h, l, c, v = (df[x] for x in ["open", "high", "low", "close", "volume"])
    for i in range(max(1, lo), min(len(df), hi)):
        O, H, L, C = o.iloc[i], h.iloc[i], l.iloc[i], c.iloc[i]
        rng = H - L if H > L else 1e-9; body = abs(C - O); green = C > O
        gain = (C / c.iloc[i-1] - 1) * 100
        if green and body >= 0.9 * rng:
            return "Bullish Marubozu", df["date"].iloc[i].date().isoformat()
        if green and O > h.iloc[i-1] and gain > 2:
            return "Gap-Up Continuation", df["date"].iloc[i].date().isoformat()
        if green and body >= 0.7 * rng and gain >= 5:
            return "Strong Momentum Candle", df["date"].iloc[i].date().isoformat()
        pats = CN.detect_at(df, i)
        if "Three White Soldiers" in pats:
            return "Three White Soldiers", df["date"].iloc[i].date().isoformat()
    return "none", ""

def analyze(sym, df):
    df = df.reset_index(drop=True)
    o, h, l, c, v = (df[x] for x in ["open", "high", "low", "close", "volume"])
    n = len(df); R = {"symbol": sym, "CMP": round(float(c.iloc[-1]), 2), "bars_daily": n}
    W = min(n, 180)
    start = int(c.tail(W).idxmin())
    R["move_start_date"] = df["date"].iloc[start].date().isoformat()
    base_low = float(c.iloc[start])

    # ENTRY at base
    ename, edate = best_entry(df, start - 2, start + 5)
    R["entry_candle"] = ename; R["entry_date"] = edate

    # CONFIRMATION during move
    cname, cdate = first_continuation(df, start + 1, start + 25)
    R["confirmation_candle"] = cname; R["confirmation_date"] = cdate

    # --- PA: HH + HL after start ---
    seg = df.iloc[start:].reset_index(drop=True)
    hh = hl = False
    if len(seg) >= 12:
        hi_idx, lo_idx = CN.T.swings(seg["close"], 3)
        if len(hi_idx) >= 2: hh = seg["high"].iloc[hi_idx[-1]] > seg["high"].iloc[hi_idx[-2]]
        if len(lo_idx) >= 2: hl = seg["low"].iloc[lo_idx[-1]] > seg["low"].iloc[lo_idx[-2]]
    R["HH_HL_sequence"] = bool(hh and hl)

    # --- breakout candle + volume confirmation (>=1.5x trailing 20d avg) ---
    base_ceiling = float(h.iloc[max(0, start-20):start+1].max())
    vol20 = v.rolling(20).mean()
    bo_ratio = np.nan; bo_date = ""
    for i in range(start, min(n, start + 30)):
        if c.iloc[i] > base_ceiling:
            va = vol20.iloc[i]
            bo_ratio = round(float(v.iloc[i] / va), 2) if pd.notna(va) and va else np.nan
            bo_date = df["date"].iloc[i].date().isoformat(); break
    R["breakout_date"] = bo_date; R["breakout_vol_x"] = bo_ratio
    R["breakout_vol_confirmed"] = bool(pd.notna(bo_ratio) and bo_ratio >= 1.5)

    # --- support respected: closes held above base low until breakout ---
    if bo_date:
        bo_pos = df.index[df["date"].dt.date.astype(str) == bo_date][0]
        held = (c.iloc[start:bo_pos+1].min() >= base_low * 0.97) if bo_pos > start else True
    else:
        held = c.iloc[start:].min() >= base_low * 0.97
    R["support_respected"] = bool(held)

    # --- false breakdown / bull trap before move (wick below prior support, close recovers) ---
    trap = False
    if start >= 30:
        prior_sup = float(l.iloc[start-30:start-5].min())
        for i in range(max(0, start-12), start+1):
            if l.iloc[i] < prior_sup and c.iloc[i] > prior_sup:
                trap = True; break
    R["false_breakdown_reversal"] = trap

    # --- WEEKLY structure at base ---
    wk = weekly(df); R["weekly_bars"] = len(wk)
    R["weekly_strong_bull_base"] = False; R["weekly_support_rejection"] = False
    if len(wk) >= 6:
        sd = pd.to_datetime(R["move_start_date"])
        wpos = (wk["date"] - sd).abs().idxmin()
        for j in (wpos, min(wpos + 1, len(wk) - 1)):
            W_ = wk.iloc[j]; rng = W_["high"] - W_["low"]
            if rng > 0 and W_["close"] > W_["open"] and (W_["close"] - W_["low"]) / rng >= 0.65:
                R["weekly_strong_bull_base"] = True
            # support rejection: long lower wick (>=40% of range) with green/neutral close
            if rng > 0 and (min(W_["open"], W_["close"]) - W_["low"]) / rng >= 0.40 and W_["close"] >= W_["open"]:
                R["weekly_support_rejection"] = True

    # --- Pattern Quality Score (1-10) ---
    raw, mx = 0.0, 0.0
    def add(cond, w):
        nonlocal raw, mx; mx += w; raw += (w if cond else 0)
    add(ename != "none", 2.0)
    add(ename in ENTRY_STRONG, 1.0)
    add(R["breakout_vol_confirmed"], 1.5)
    add(R["HH_HL_sequence"], 1.0)
    add(R["support_respected"], 1.0)
    add(cname != "none", 1.0)
    add(R["false_breakdown_reversal"], 1.0)
    add(R["weekly_strong_bull_base"], 1.0)
    add(R["weekly_support_rejection"], 0.5)
    R["pattern_quality_10"] = int(np.clip(round(raw / mx * 10), 1, 10)) if mx else 1
    return R

if __name__ == "__main__":
    fin = pd.read_csv("FINAL_universe_25pct.csv", dtype={"symbol": str})
    meta = fin.set_index("symbol")[["name", "exchange"]].to_dict("index")
    data = pickle.load(open("ohlc.pkl", "rb"))
    rows = []
    for i, sym in enumerate(fin["symbol"], 1):
        df = data.get(sym)
        if df is None or len(df) < 40:
            rows.append({"symbol": sym, "note": "insufficient OHLC"}); continue
        try:
            r = analyze(sym, df)
            r["name"] = meta.get(sym, {}).get("name", ""); r["exchange"] = meta.get(sym, {}).get("exchange", "")
            rows.append(r)
        except Exception as e:
            rows.append({"symbol": sym, "note": f"{type(e).__name__}:{e}"})
        if i % 80 == 0: print(f"  {i}/{len(fin)}")

    out = pd.DataFrame(rows).sort_values("pattern_quality_10", ascending=False, na_position="last").reset_index(drop=True)
    full_cols = ["symbol", "name", "exchange", "CMP", "move_start_date",
                 "entry_candle", "entry_date", "confirmation_candle", "confirmation_date",
                 "HH_HL_sequence", "support_respected", "breakout_date", "breakout_vol_x", "breakout_vol_confirmed",
                 "false_breakdown_reversal", "weekly_strong_bull_base", "weekly_support_rejection",
                 "weekly_bars", "bars_daily", "pattern_quality_10"]
    full_cols = [c for c in full_cols if c in out.columns]
    out[full_cols].to_csv("ENTRY_PATTERN_ANALYSIS.csv", index=False)

    def pa_struct(r):
        bits = []
        if r.get("HH_HL_sequence"): bits.append("HH+HL")
        if r.get("support_respected"): bits.append("supp-held")
        if r.get("breakout_vol_confirmed"): bits.append(f"BO {r.get('breakout_vol_x')}x")
        if r.get("false_breakdown_reversal"): bits.append("bull-trap")
        return ", ".join(bits) if bits else "weak"
    summ = pd.DataFrame({
        "Stock": out["symbol"],
        "Entry Candle Type": out["entry_candle"],
        "Confirmation Candle": out["confirmation_candle"],
        "PA Structure": out.apply(pa_struct, axis=1),
        "Pattern Quality Score (1-10)": out["pattern_quality_10"],
    })
    summ.to_csv("ENTRY_PATTERN_SCORECARD.csv", index=False)

    nn = int(out["pattern_quality_10"].notna().sum())
    print(f"\nDONE. analysed {nn} stocks -> ENTRY_PATTERN_ANALYSIS.csv + ENTRY_PATTERN_SCORECARD.csv")
    print("entry candle distribution:", out["entry_candle"].value_counts().to_dict())
    print(f"breakout vol >=1.5x: {int(out['breakout_vol_confirmed'].sum())} | HH+HL: {int(out['HH_HL_sequence'].sum())} | "
          f"bull-trap: {int(out['false_breakdown_reversal'].sum())} | weekly strong base: {int(out['weekly_strong_bull_base'].sum())}")
    print("\n=== TOP 20 (by pattern quality) ===")
    print(summ.head(20).to_string(index=False))
