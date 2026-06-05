"""Fetch LIVE current price for each Phase-7 watchlist stock and compare to
scan-time close + planned entry/stop. Read-only helper — does not touch pipeline files."""
import time, requests, pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
S = requests.Session(); S.headers.update({"User-Agent": UA})

def live_price(sym):
    """Return (price, prev_close) from Yahoo chart meta, or (None, None)."""
    for suf in (".NS", ".BO"):
        try:
            r = S.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}{suf}",
                      params={"range": "5d", "interval": "1d"}, timeout=20)
            m = r.json()["chart"]["result"][0]["meta"]
            px = m.get("regularMarketPrice")
            pc = m.get("chartPreviousClose") or m.get("previousClose")
            if px:
                return float(px), (float(pc) if pc else None)
        except Exception:
            pass
    return None, None

wl = pd.read_csv("PHASE7_WATCHLIST.csv")
rows = []
for _, r in wl.iterrows():
    px, pc = live_price(r["symbol"])
    chg = ((px / pc - 1) * 100) if (px and pc) else None
    # is the live price at/above the planned breakout entry?
    status = ""
    if px is not None:
        if px >= r["pivot_entry"]:
            status = "ABOVE ENTRY"
        elif px <= r["stop"]:
            status = "BELOW STOP"
        else:
            to_entry = (r["pivot_entry"] / px - 1) * 100
            status = f"{to_entry:+.1f}% to entry"
    rows.append({
        "rank": r["rank"], "symbol": r["symbol"], "tier": r["tier"],
        "scan_close": r["close"], "live": round(px, 2) if px else None,
        "day_chg%": round(chg, 2) if chg is not None else None,
        "entry": r["pivot_entry"], "stop": r["stop"], "status": status,
    })
    time.sleep(0.25)

out = pd.DataFrame(rows)
pd.set_option("display.max_rows", None, "display.width", 200)
print(out.to_string(index=False))
out.to_csv("PHASE7_WATCHLIST_LIVE.csv", index=False)
print("\nSaved -> PHASE7_WATCHLIST_LIVE.csv")
