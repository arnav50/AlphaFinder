"""
Phase 1 / Step 1A-1B : Build the NSE + BSE equity universe.
Outputs: universe.csv  (columns: symbol, name, exchange, yahoo_ticker, series_or_group, isin)
"""
import io, json, requests, pandas as pd

HDR = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
S = requests.Session(); S.headers.update(HDR)


def nse_universe():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(io.StringIO(S.get(url, timeout=30).text))
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={
        "SYMBOL": "symbol", "NAME OF COMPANY": "name",
        "SERIES": "series", " ISIN NUMBER": "isin", "ISIN NUMBER": "isin"})
    # Keep equity series only: EQ (normal) + BE (trade-for-trade). Drop BZ/SM/ST surveillance series.
    df = df[df["series"].str.strip().isin(["EQ", "BE"])].copy()
    df["exchange"] = "NSE"
    df["yahoo_ticker"] = df["symbol"].str.strip() + ".NS"
    df["series_or_group"] = df["series"].str.strip()
    return df[["symbol", "name", "exchange", "yahoo_ticker", "series_or_group", "isin"]]


def bse_universe():
    # BSE scrip master via official API. Group filters out Z (suspended) / T (T2T flagged separately).
    url = ("https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w"
           "?Group=&Scripcode=&industry=&segment=Equity&status=Active")
    r = S.get(url, headers={**HDR, "Referer": "https://www.bseindia.com/"}, timeout=40)
    df = pd.DataFrame(r.json())  # keys: SCRIP_CD, Scrip_Name, Status, GROUP, ISIN_NUMBER, INDUSTRY, Mktcap ...
    out = pd.DataFrame({
        "symbol": df["SCRIP_CD"].astype(str).str.strip(),
        "name": df["Scrip_Name"].astype(str).str.strip(),
        "isin": df["ISIN_NUMBER"].astype(str).str.strip(),
        "series_or_group": df["GROUP"].astype(str).str.strip(),
        "bse_sector": df["INDUSTRY"].astype(str).str.strip(),
        "bse_mktcap_cr": pd.to_numeric(df["Mktcap"], errors="coerce"),  # in Rs crore
    })
    # Exclude Z-group (suspended/non-compliant) and XT/XC/X surveillance groups per spec.
    out = out[~out["series_or_group"].str.upper().isin(["Z", "XT", "XC", "ZP", "ZY"])].copy()
    out["exchange"] = "BSE"
    out["yahoo_ticker"] = out["symbol"] + ".BO"   # Yahoo uses numeric BSE scrip code + .BO
    return out


if __name__ == "__main__":
    nse = nse_universe()
    print(f"NSE equity (EQ+BE): {len(nse)}")
    try:
        bse = bse_universe()
        print(f"BSE equity (active, ex Z/XT): {len(bse)}")
    except Exception as e:
        print(f"BSE fetch failed ({type(e).__name__}: {e}) -- continuing NSE-only, will retry separately")
        bse = pd.DataFrame(columns=nse.columns)

    uni = pd.concat([nse, bse], ignore_index=True)
    # Dedup by ISIN across exchanges: prefer NSE listing (more liquid/standard) when both exist.
    uni["isin_norm"] = uni["isin"].astype(str).str.strip().str.upper()
    uni["_pref"] = (uni["exchange"] == "NSE").astype(int)
    has_isin = uni[uni["isin_norm"].str.startswith("IN")]
    no_isin = uni[~uni["isin_norm"].str.startswith("IN")]
    has_isin = (has_isin.sort_values("_pref", ascending=False)
                        .drop_duplicates("isin_norm", keep="first"))
    uni = pd.concat([has_isin, no_isin], ignore_index=True).drop(columns=["_pref"])
    uni.to_csv("universe.csv", index=False)
    print(f"TOTAL universe after ISIN dedup (NSE preferred): {len(uni)}")
    print(uni["exchange"].value_counts().to_dict())
