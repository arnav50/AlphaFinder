"""Classify the Phase-7 watchlist into EARLY STAGE (coiled below entry) vs
ALREADY MOVING (broken out, advancing to target) vs FAILED (below stop),
using fresh live prices. Read-only. Mechanical signals — not investment advice."""
import time, requests, pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"


def live_price(sym, s):
    for suf in (".NS", ".BO"):
        try:
            r = s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}{suf}",
                      params={"range": "5d", "interval": "1d"}, timeout=15)
            px = r.json()["chart"]["result"][0]["meta"].get("regularMarketPrice")
            if px:
                return float(px)
        except Exception:
            pass
    return None


wl = pd.read_csv("PHASE7_WATCHLIST.csv", dtype={"symbol": str})
s = requests.Session(); s.headers.update({"User-Agent": UA})
rows = []
for _, r in wl.iterrows():
    px = live_price(r["symbol"], s)
    entry, stop, tgt = float(r["pivot_entry"]), float(r["stop"]), float(r["target2"])
    move_total = (tgt / entry - 1) * 100          # full projected move from entry to target
    if px is None:
        stage = "NO DATA"; captured = to_entry = upside = None
    elif px <= stop:
        stage = "FAILED";   captured = to_entry = upside = None
    elif px >= entry:
        stage = "ALREADY MOVING"
        captured = (px - entry) / (tgt - entry) * 100      # % of entry->target path done
        upside = (tgt / px - 1) * 100                      # % left to target from here
        to_entry = 0.0
    else:
        stage = "EARLY STAGE"
        to_entry = (entry / px - 1) * 100                  # % rise needed just to trigger
        upside = (tgt / px - 1) * 100                      # total % to target from here
        captured = 0.0
    rows.append(dict(rank=r["rank"], symbol=r["symbol"], tier=r["tier"], live=round(px, 2) if px else None,
                     entry=round(entry, 2), stop=round(stop, 2), target=round(tgt, 2), move_total=round(move_total, 1),
                     stage=stage, to_entry=round(to_entry, 1) if to_entry is not None else None,
                     captured=round(captured, 1) if captured is not None else None,
                     upside_to_target=round(upside, 1) if upside is not None else None))
    time.sleep(0.2)

df = pd.DataFrame(rows)
df.to_csv("PHASE7_STAGE.csv", index=False)
pd.set_option("display.width", 200)

moving = df[df.stage == "ALREADY MOVING"].sort_values("captured", ascending=False)
early  = df[df.stage == "EARLY STAGE"].sort_values("to_entry")          # closest to trigger first
failed = df[df.stage == "FAILED"]

print("=" * 70)
print(f"ALREADY MOVING (broke out, advancing) — {len(moving)}")
print("  most progress toward target first")
if len(moving):
    print(moving[["rank","symbol","tier","live","entry","target","captured","upside_to_target"]].to_string(index=False))
print()
print("=" * 70)
print(f"EARLY STAGE (coiled below entry, not triggered) — {len(early)}")
print("  closest to triggering first | to_entry = % rise needed to fire")
if len(early):
    print(early[["rank","symbol","tier","live","entry","target","to_entry","upside_to_target"]].to_string(index=False))
print()
print("=" * 70)
print(f"FAILED (below stop, setup invalidated) — {len(failed)}")
if len(failed):
    print(failed[["rank","symbol","tier","live","entry","stop"]].to_string(index=False))
print(f"\nmove_total = full projected entry->target move (~25%+). Saved -> PHASE7_STAGE.csv")
print("Mechanical signals — not investment advice.")
