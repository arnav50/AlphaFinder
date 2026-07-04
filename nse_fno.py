"""Shared NSE F&O fetcher — gets past NSE's Akamai bot-wall.

NSE fingerprints the TLS handshake, so plain requests/curl get a 404 challenge page.
curl_cffi impersonates Chrome's TLS fingerprint; a homepage cookie warm-up then unlocks
the JSON API. Used by 28_option_chain.py (snapshot) and 29_fno_trade.py (trade finder).
    pip install curl_cffi
"""
import time, urllib.parse

HOME   = "https://www.nseindia.com/"
OCPAGE = "https://www.nseindia.com/option-chain"
APIHDR = {"accept": "application/json, text/plain, */*",
          "accept-language": "en-US,en;q=0.9", "referer": OCPAGE}
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def make_session():
    """Return (session, kind). Prefer curl_cffi (defeats Akamai); fall back to requests."""
    try:
        from curl_cffi import requests as creq
        s, kind = creq.Session(impersonate="chrome120"), "curl_cffi"
    except Exception:
        import requests
        s = requests.Session(); s.headers.update({"User-Agent": _UA})
        kind = "requests (curl_cffi not installed — NSE may block)"
    _warm(s, HOME); time.sleep(0.8)
    _warm(s, OCPAGE, headers={"referer": HOME}); time.sleep(0.8)
    return s, kind


def _warm(s, url, tries=5, **kw):
    """Warm-up GET with backoff — survives flaky DNS/connection hiccups."""
    for i in range(tries):
        try:
            return s.get(url, timeout=20, **kw)
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def get_json(s, url, tries=4):
    r = None
    for i in range(tries):
        r = s.get(url, headers=APIHDR, timeout=25)
        ctype = r.headers.get("content-type", "")
        if r.status_code == 200 and ctype.startswith("application/json") and len(r.content) > 5:
            return r.json()
        time.sleep(1.2 + i)            # let Akamai settle, then retry
    raise RuntimeError(f"NSE fetch failed ({getattr(r,'status_code','?')}, "
                       f"{len(r.content) if r is not None else 0}B) for {url[:80]}")


def contract_info(s, symbol="NIFTY"):
    """(expiry_dates, strike_prices) for the symbol."""
    j = get_json(s, f"https://www.nseindia.com/api/option-chain-contract-info?symbol={symbol}")
    return j.get("expiryDates", []), j.get("strikePrice", [])


def fetch_chain(s, symbol="NIFTY", expiry=None):
    """Full option chain for one expiry (nearest if expiry is None).
    Returns dict: spot, expiry, expiries[], timestamp, rows[ {strikePrice, CE{}, PE{}} ]."""
    expiries, _ = contract_info(s, symbol)
    if not expiries:
        raise RuntimeError("no expiry dates returned by NSE")
    exp = expiry or expiries[0]
    time.sleep(0.6)
    url = (f"https://www.nseindia.com/api/option-chain-v3?type=Indices&symbol={symbol}"
           f"&expiry=" + urllib.parse.quote(exp))
    rec = get_json(s, url)["records"]
    rows = [d for d in rec["data"] if "strikePrice" in d and ("CE" in d or "PE" in d)]
    return {"symbol": symbol, "spot": float(rec["underlyingValue"]), "expiry": exp,
            "expiries": expiries, "timestamp": rec.get("timestamp", ""), "rows": rows}
