"""Validate the Phase-7 watchlist against FRESH market data and emit a GO / WATCH / DROP
verdict per stock based on objective (Layer-1) checks only.

Layer-1 checks (all mechanical, price/volume — NOT fundamental):
  alive       live price still above the planned stop (plan not yet invalidated)
  liquid      20-day median traded value >= MIN_ADV_VALUE (can actually trade it)
  triggered   price has broken the planned breakout entry (it's a trade, not a wish)
  vol_ok      breakout backed by volume >= 1.5x the 50-day average (fingerprint's #1 trait)
  not_ext     not chasing — live price <= ~5% above entry
  rs_ok       relative strength: 3-month return beats the Nifty over the same window

Verdict:
  DROP   below stop, or too illiquid to trade
  GO     alive + liquid + triggered + vol_ok + not_ext + rs_ok  (act-on in this regime)
  WATCH  alive + liquid but not yet a clean trigger (staging / partial confirmation)

Outputs PHASE7_VALIDATION.csv + a console table.  Mechanical signals — NOT investment advice.
Layer-2 checks (GSM/ASM surveillance, promoter pledge, earnings dates, governance) are NOT
covered here and must be checked manually before buying.
"""
import time, requests, numpy as np, pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
MIN_ADV_VALUE = 20_000_000   # Rs 2 crore/day median traded value (matches prime filter)
VOL_SPIKE     = 1.5          # breakout volume vs 50d avg
MAX_EXT_PCT   = 5.0          # don't chase more than 5% above entry
RS_WINDOW     = 63           # ~3 trading months for relative strength


def fetch_ohlc(ticker, session, suffixes=(".NS", ".BO")):
    """Return (DataFrame[close,high,low,volume], live_price) from Yahoo daily 1y, or (None,None)."""
    for suf in suffixes:
        try:
            r = session.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}{suf}",
                            params={"range": "1y", "interval": "1d"}, timeout=20)
            res = r.json()["chart"]["result"][0]
            q = res["indicators"]["quote"][0]
            df = pd.DataFrame({"close": q["close"], "high": q["high"],
                               "low": q["low"], "volume": q["volume"]}).dropna().reset_index(drop=True)
            if len(df) > 60:
                meta = res["meta"]
                live = meta.get("regularMarketPrice") or float(df["close"].iloc[-1])
                return df, float(live)
        except Exception:
            pass
    return None, None


def pct_return(series, n):
    n = min(n, len(series) - 1)
    return (series.iloc[-1] / series.iloc[-1 - n] - 1) * 100 if n > 0 else np.nan


def main():
    wl = pd.read_csv("PHASE7_WATCHLIST.csv", dtype={"symbol": str})
    sx = requests.Session(); sx.headers.update({"User-Agent": UA})

    # Nifty benchmark return for relative strength
    try:
        ndf, _ = fetch_ohlc("%5ENSEI", sx, suffixes=("",))
        nifty_ret = pct_return(ndf["close"], RS_WINDOW)
    except Exception:
        nifty_ret = 0.0
    print(f"Nifty {RS_WINDOW}d return baseline: {nifty_ret:+.1f}%\n")

    rows = []
    for _, r in wl.iterrows():
        sym, entry, stop = r["symbol"], float(r["pivot_entry"]), float(r["stop"])
        df, live = fetch_ohlc(sym, sx)
        if df is None:
            rows.append(dict(rank=r["rank"], symbol=sym, tier=r["tier"], live=None,
                             verdict="NO DATA", passed=0, checks="fetch failed",
                             phase7_score=r["phase7_score"]))
            time.sleep(0.2); continue

        c, v, h = df["close"], df["volume"], df["high"]
        sma50_vol = v.iloc[-50:].mean()
        recent_vol = v.iloc[-5:].max()                       # breakout-window volume
        vol_ratio = recent_vol / sma50_vol if sma50_vol else 0
        adv_value = float((c * v).iloc[-20:].median())        # 20d median traded value
        ext_pct = (live / entry - 1) * 100
        stock_ret = pct_return(c, RS_WINDOW)
        rs = stock_ret - nifty_ret

        chk = {
            "alive":     live > stop,
            "liquid":    adv_value >= MIN_ADV_VALUE,
            "triggered": live >= entry,                       # price currently AT/above the breakout pivot
            "vol_ok":    vol_ratio >= VOL_SPIKE,
            "not_ext":   ext_pct <= MAX_EXT_PCT,
            "rs_ok":     rs > 0,
        }
        passed = sum(chk.values())

        if not chk["alive"]:
            verdict = "DROP (below stop)"
        elif not chk["liquid"]:
            verdict = "DROP (illiquid)"
        elif all([chk["triggered"], chk["vol_ok"], chk["not_ext"], chk["rs_ok"]]):
            verdict = "GO"
        elif chk["triggered"] and not chk["not_ext"]:
            verdict = "WATCH (extended)"
        elif not chk["triggered"]:
            verdict = "WATCH (staging)"
        else:
            verdict = "WATCH (weak confirm)"

        fails = ",".join(k for k, ok in chk.items() if not ok) or "all pass"
        rows.append(dict(
            rank=r["rank"], symbol=sym, tier=r["tier"],
            live=round(live, 2), entry=round(entry, 2), stop=round(stop, 2),
            ext_pct=round(ext_pct, 1), vol_x=round(vol_ratio, 1),
            adv_cr=round(adv_value / 1e7, 2), rs_vs_nifty=round(rs, 1),
            verdict=verdict, passed=passed, fails=fails,
            phase7_score=r["phase7_score"],
        ))
        time.sleep(0.2)

    out = pd.DataFrame(rows)
    order = {"GO": 0, "WATCH (staging)": 1, "WATCH (weak confirm)": 1, "WATCH (extended)": 2,
             "DROP (below stop)": 3, "DROP (illiquid)": 3, "NO DATA": 4}
    out["_o"] = out["verdict"].map(lambda x: order.get(x, 5))
    out = out.sort_values(["_o", "passed", "phase7_score"], ascending=[True, False, False]).drop(columns="_o")

    pd.set_option("display.max_rows", None, "display.width", 220)
    cols = ["rank", "symbol", "tier", "live", "entry", "stop", "ext_pct", "vol_x",
            "adv_cr", "rs_vs_nifty", "passed", "verdict", "fails"]
    print(out[cols].to_string(index=False))
    out.to_csv("PHASE7_VALIDATION.csv", index=False)

    vc = out["verdict"].apply(lambda x: x.split()[0]).value_counts()
    print(f"\nSummary: " + " | ".join(f"{k}={v}" for k, v in vc.items()))
    print("Saved -> PHASE7_VALIDATION.csv")
    print("\nNOTE: Layer-1 (mechanical) only. Before buying, manually check GSM/ASM surveillance,")
    print("promoter pledge, upcoming earnings/events, and the chart. Not investment advice.")


if __name__ == "__main__":
    main()
