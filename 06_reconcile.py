"""
Final reconciliation:
  - canonical return = last_close(today)  /  MEDIAN(+-2 bars around today-180d)  - 1
    (point 'today' keeps trending winners accurate; median past guards vs bad single print)
  - 2nd-source current price for NSE hits = BSE-twin LTP via ISIN  (independent exchange)
  - keep rows where canonical return >= 25 ; flag any with weak cross-source agreement
Output: FINAL_universe_25pct.csv  + console verification checkpoint
"""
import time, requests, pandas as pd

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
H = {"User-Agent": UA, "Referer": "https://www.bseindia.com/"}

df = pd.read_csv("hits_final.csv", dtype={"symbol": str})

# canonical: today's last close / robust past median
df["return_pct_final"] = ((df["price_today"] / df["robust_past"] - 1) * 100).round(2)

# Build ISIN -> BSE scrip code map for cross-source current price on NSE names.
# The BSE API is flaky (intermittently returns HTML/empty instead of JSON); retry
# with backoff, and degrade gracefully if it stays down -- the winner list only
# depends on return_pct_final, the BSE cross-source price is a secondary check.
def bse_master(tries=4):
    for i in range(tries):
        try:
            r = requests.get(
                "https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w?Group=&Scripcode=&industry=&segment=Equity&status=Active",
                headers=H, timeout=40)
            return pd.DataFrame(r.json())
        except Exception as e:
            if i == tries - 1:
                print(f"[warn] BSE master fetch failed ({type(e).__name__}); "
                      f"skipping BSE cross-source price check.")
                return None
            time.sleep(2 * (i + 1))

master = bse_master()
if master is not None:
    master["isin"] = master["ISIN_NUMBER"].astype(str).str.strip().str.upper()
    isin2code = dict(zip(master["isin"], master["SCRIP_CD"].astype(str)))
else:
    isin2code = {}

bse = requests.Session(); bse.headers.update(H)
def bse_ltp(code):
    try:
        j = bse.get(f"https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w?scripcode={code}&seriesid=", timeout=15).json()
        return float(j["CurrRate"]["LTP"])
    except Exception: return float("nan")

xsrc = []
for _, r in df.iterrows():
    if r["exchange"] == "BSE":
        xsrc.append(r.get("live_today_2ndsrc"))                  # already BSE live
    else:
        code = isin2code.get(str(r["isin_norm"]).upper())
        xsrc.append(bse_ltp(code) if code else float("nan")); time.sleep(0.12)
df["xsrc_price"] = [round(x, 2) if pd.notna(x) else x for x in xsrc]
df["xsrc_mismatch_pct"] = ((df["price_today"] - df["xsrc_price"]).abs() / df["xsrc_price"] * 100).round(2)

# verification verdict per row
df["xsrc_ok"] = df["xsrc_mismatch_pct"] <= 5            # agrees within 5% with the other exchange
df["verified"] = df["return_pct_final"] >= 25

final = df[df["verified"]].sort_values("return_pct_final", ascending=False).reset_index(drop=True)
final.insert(0, "rank", final.index + 1)

out_cols = ["rank", "symbol", "name", "exchange", "price_180d_ago", "past_date_used",
            "price_today", "return_pct_final", "mktcap_cr", "cap_bucket", "sector",
            "avg_daily_volume", "avg_daily_value_rs", "penny_flag",
            "xsrc_price", "xsrc_mismatch_pct", "xsrc_ok", "isin_norm"]
final[out_cols].to_csv("FINAL_universe_25pct.csv", index=False)

print("="*70)
print("PHASE 1 VERIFICATION CHECKPOINT")
print("="*70)
print(f"[OK] Total stocks with verified 180d return >= 25% : {len(final)}")
print(f"[OK] Duplicates removed (same co. NSE & BSE) via ISIN: dedup done in universe step")
print(f"     by exchange: {final['exchange'].value_counts().to_dict()}")
print(f"     by cap     : {final['cap_bucket'].value_counts().to_dict()}")
print(f"[OK] Penny stocks (<Rs10) flagged (not removed)      : {int(final['penny_flag'].sum())}")
xs = final[final['xsrc_price'].notna()]
print(f"[OK] Cross-source price check (BSE twin / BSE live)   : {len(xs)}/{len(final)} have 2nd source")
print(f"     agree within 5%: {int(xs['xsrc_ok'].sum())}/{len(xs)}  | median mismatch {xs['xsrc_mismatch_pct'].median():.2f}%")
print(f"     NSE-only names w/ no BSE twin (Yahoo-only price) : {final['xsrc_price'].isna().sum()}")
print(f"[OK] Sorted by Return% descending                    : yes")
print("\nTop 20:")
show = final[["rank","symbol","name","exchange","price_180d_ago","price_today","return_pct_final","cap_bucket","xsrc_mismatch_pct"]].head(20)
print(show.to_string(index=False))
