"""Phase 8 — Nifty 50 LIVE option chain → OPTION_CHAIN.csv + OPTION_CHAIN_META.csv.

Fetches the real NSE option chain for the CURRENT expiry plus every upcoming expiry in
the current calendar month (month of the nearest expiry), and for each one keeps 5 strikes
centred on ATM (ATM +/- 2). Results are stacked with an `expiry` column so the dashboard
can show a separate table per expiry.

NSE/Akamai fetch lives in nse_fno.py (curl_cffi TLS impersonation). Read at build time
by 25_build_frontend.py.
"""
import datetime
import pandas as pd
import nse_fno

SYMBOL    = "NIFTY"
N_STRIKES = 2           # ATM + this many strikes each side => 5 strikes total


def f(x, nd=2):
    try:
        return round(float(x), nd)
    except (TypeError, ValueError):
        return None


def build_rows(ch, expiry, dte):
    """5-strike (ATM +/-2) rows + a meta dict for one expiry's chain."""
    spot, rows = ch["spot"], ch["rows"]
    by_strike = {int(d["strikePrice"]): d for d in rows}
    strikes = sorted(by_strike)
    atm = min(strikes, key=lambda k: abs(k - spot))
    ai = strikes.index(atm)
    window = strikes[max(0, ai - N_STRIKES): ai + N_STRIKES + 1]

    out = []
    for k in window:
        d = by_strike.get(k, {})
        ce, pe = d.get("CE", {}) or {}, d.get("PE", {}) or {}
        out.append({
            "expiry": expiry, "dte": dte, "strike": k, "atm": k == atm,
            "ce_itm": k < spot, "pe_itm": k > spot,
            "ce_oi": f(ce.get("openInterest"), 0), "ce_chg_oi": f(ce.get("changeinOpenInterest"), 0),
            "ce_vol": f(ce.get("totalTradedVolume"), 0), "ce_iv": f(ce.get("impliedVolatility")),
            "ce_ltp": f(ce.get("lastPrice")), "ce_chg": f(ce.get("change")),
            "pe_ltp": f(pe.get("lastPrice")), "pe_chg": f(pe.get("change")),
            "pe_iv": f(pe.get("impliedVolatility")), "pe_vol": f(pe.get("totalTradedVolume"), 0),
            "pe_chg_oi": f(pe.get("changeinOpenInterest"), 0), "pe_oi": f(pe.get("openInterest"), 0),
        })

    ce_oi_tot = sum(f((by_strike[k].get("CE") or {}).get("openInterest"), 0) or 0 for k in strikes)
    pe_oi_tot = sum(f((by_strike[k].get("PE") or {}).get("openInterest"), 0) or 0 for k in strikes)
    pcr = round(pe_oi_tot / ce_oi_tot, 2) if ce_oi_tot else None

    def pain(at):
        return sum((f((by_strike[k].get("CE") or {}).get("openInterest"), 0) or 0) * max(0, at - k) +
                   (f((by_strike[k].get("PE") or {}).get("openInterest"), 0) or 0) * max(0, k - at)
                   for k in strikes)
    max_pain = min(strikes, key=pain) if strikes else None

    meta = {"symbol": SYMBOL, "expiry": expiry, "dte": dte, "spot": round(spot, 2),
            "atm": atm, "nse_timestamp": ch["timestamp"],
            "fetched_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "pcr": pcr, "ce_oi_total": round(ce_oi_tot, 0), "pe_oi_total": round(pe_oi_tot, 0),
            "max_pain": max_pain, "n_strikes": len(out)}
    return out, meta


def main():
    today = datetime.date.today()
    s, kind = nse_fno.make_session(); print(f"session: {kind}")
    expiries, _ = nse_fno.contract_info(s, SYMBOL)

    def dparse(e): return datetime.datetime.strptime(e, "%d-%b-%Y").date()
    upcoming = [e for e in expiries if dparse(e) >= today]
    if not upcoming:
        upcoming = expiries[:1]
    ym = (dparse(upcoming[0]).year, dparse(upcoming[0]).month)      # month of the nearest expiry
    selected = [e for e in upcoming if (dparse(e).year, dparse(e).month) == ym]
    print(f"current month expiries: {selected}")

    all_rows, metas = [], []
    for e in selected:
        dte = (dparse(e) - today).days
        ch = nse_fno.fetch_chain(s, SYMBOL, e)
        rows, meta = build_rows(ch, e, dte)
        all_rows += rows; metas.append(meta)
        print(f"  {e} (DTE {dte}): ATM {meta['atm']} spot {meta['spot']} PCR {meta['pcr']} max_pain {meta['max_pain']}")

    pd.DataFrame(all_rows).to_csv("OPTION_CHAIN.csv", index=False)
    pd.DataFrame(metas).to_csv("OPTION_CHAIN_META.csv", index=False)
    print(f"Wrote OPTION_CHAIN.csv ({len(selected)} expiries x {2*N_STRIKES+1} strikes) + OPTION_CHAIN_META.csv")


if __name__ == "__main__":
    main()
