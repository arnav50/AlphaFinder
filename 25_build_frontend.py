"""Generate a self-contained HTML dashboard (alphafinder_dashboard.html) from the phase CSVs.
Data is embedded as JSON so the file opens by double-click (no server needed)."""
import json, time, datetime, requests, pandas as pd, numpy as np

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

def load(f, cols=None):
    d = pd.read_csv(f, dtype={"symbol": str})
    if cols: d = d[[c for c in cols if c in d.columns]]
    return d

# Layer-1 validation thresholds (see validate_watchlist.py)
MIN_ADV_VALUE = 20_000_000   # Rs 2 crore/day median traded value
VOL_SPIKE     = 1.5          # breakout volume vs 50d avg
MAX_EXT_PCT   = 5.0          # don't chase >5% above entry
RS_WINDOW     = 63           # ~3 trading months for relative strength

def fetch_ohlc(ticker, session, suffixes=(".NS", ".BO")):
    """Return (DataFrame[close,high,low,volume], live_price, prev_close) from Yahoo daily 1y."""
    for suf in suffixes:
        try:
            r = session.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}{suf}",
                            params={"range": "1y", "interval": "1d"}, timeout=20)
            res = r.json()["chart"]["result"][0]; q = res["indicators"]["quote"][0]
            df = pd.DataFrame({"close": q["close"], "high": q["high"],
                               "low": q["low"], "volume": q["volume"]}).dropna().reset_index(drop=True)
            if len(df) > 60:
                meta = res["meta"]
                live = meta.get("regularMarketPrice") or float(df["close"].iloc[-1])
                prev = meta.get("previousClose") or meta.get("chartPreviousClose")
                return df, float(live), (float(prev) if prev else None)
        except Exception:
            pass
    return None, None, None

def pct_return(series, n):
    n = min(n, len(series) - 1)
    return float((series.iloc[-1] / series.iloc[-1 - n] - 1) * 100) if n > 0 else None

def enrich_watchlist(df):
    """Add live-price + Layer-1 GO/WATCH/DROP validation columns from one fresh fetch each."""
    sx = requests.Session(); sx.headers.update({"User-Agent": UA})
    try:
        ndf, _, _ = fetch_ohlc("%5ENSEI", sx, suffixes=("",))
        nifty_ret = pct_return(ndf["close"], RS_WINDOW) or 0.0
    except Exception:
        nifty_ret = 0.0
    keys = ["live", "live_chg", "live_state", "live_to_entry", "vol_x", "ext_pct",
            "adv_cr", "rs", "verdict", "vreason", "vpassed", "vfails",
            "stage", "stage_pct", "upside_tgt"]
    out = {k: [] for k in keys}
    def push(**kw):
        for k in keys: out[k].append(kw.get(k))
    for _, r in df.iterrows():
        entry, stop = float(r["pivot_entry"]), float(r["stop"])
        ohlc, live, prev = fetch_ohlc(r["symbol"], sx)
        if ohlc is None:
            push(verdict="NO DATA"); time.sleep(0.2); continue
        c, v = ohlc["close"], ohlc["volume"]
        sma50 = v.iloc[-50:].mean()
        vol_x = float(v.iloc[-5:].max() / sma50) if sma50 else 0.0
        adv = float((c * v).iloc[-20:].median())
        ext = (live / entry - 1) * 100
        rs = (pct_return(c, RS_WINDOW) or 0.0) - nifty_ret
        chk = {"alive": live > stop, "liquid": adv >= MIN_ADV_VALUE, "triggered": live >= entry,
               "vol_ok": vol_x >= VOL_SPIKE, "not_ext": ext <= MAX_EXT_PCT, "rs_ok": rs > 0}
        if not chk["alive"]:        verdict, reason = "DROP", "below stop"
        elif not chk["liquid"]:     verdict, reason = "DROP", "illiquid"
        elif all([chk["triggered"], chk["vol_ok"], chk["not_ext"], chk["rs_ok"]]):
            verdict, reason = "GO", "all checks pass"
        elif chk["triggered"] and not chk["not_ext"]:
            verdict, reason = "WATCH", "extended (chasing)"
        elif not chk["triggered"]:  verdict, reason = "WATCH", "staging (not triggered)"
        else:                       verdict, reason = "WATCH", "weak confirmation"
        if live >= entry:   state, to_entry = "above", 0.0
        elif live <= stop:  state, to_entry = "stop", None
        else:               state, to_entry = "pending", round((entry / live - 1) * 100, 2)
        # stage: EARLY (coiled below entry) / MOVING (broke out, advancing) / FAILED (below stop)
        tgt = float(r["target2"])
        if live <= stop:
            stage, stage_pct, upside_tgt = "FAILED", None, None
        elif live >= entry:
            stage = "MOVING"
            stage_pct = round((live - entry) / (tgt - entry) * 100, 1) if tgt > entry else None  # % of move done
            upside_tgt = round((tgt / live - 1) * 100, 1)
        else:
            stage = "EARLY"
            stage_pct = round((entry / live - 1) * 100, 1)                                        # % rise to trigger
            upside_tgt = round((tgt / live - 1) * 100, 1)
        push(live=round(live, 2), stage=stage, stage_pct=stage_pct, upside_tgt=upside_tgt,
             live_chg=round((live / prev - 1) * 100, 2) if prev else None,
             live_state=state, live_to_entry=to_entry,
             vol_x=round(vol_x, 1), ext_pct=round(ext, 1), adv_cr=round(adv / 1e7, 2),
             rs=round(rs, 1), verdict=verdict, vreason=reason,
             vpassed=int(sum(chk.values())),
             vfails=",".join(k for k, ok in chk.items() if not ok) or "none")
        time.sleep(0.2)
    df = df.copy()
    for k in keys: df[k] = out[k]
    return df, nifty_ret

p1 = load("FINAL_universe_25pct.csv")
p2 = load("PHASE2_SCORECARD.csv")
p3 = load("PHASE3_SMC.csv")
p4 = load("PHASE4_VCP_GANN.csv")
p6 = load("PHASE6_RANKING.csv")
wl = load("PHASE7_WATCHLIST.csv")
fp = load("PHASE5_FINGERPRINT.csv")

# ---------- live prices + Layer-1 validation for the watchlist (fetched fresh at build time) ----------
nifty_ret = None
try:
    wl, nifty_ret = enrich_watchlist(wl)
    live_ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    vc = wl["verdict"].value_counts().to_dict()
    print(f"Live + validation: {int(wl['live'].notna().sum())}/{len(wl)} fetched @ {live_ts} | "
          + " ".join(f"{k}={v}" for k, v in vc.items()))
except Exception as e:
    live_ts = None
    for k in ["live","live_chg","live_state","live_to_entry","vol_x","ext_pct","adv_cr","rs","verdict","vreason","vpassed","vfails"]:
        if k not in wl.columns: wl[k] = None
    print(f"Live/validation fetch skipped ({e}) — dashboard will show scan-time close only")

# ---------- master: one row per Phase-1 stock, fields from all phases ----------
m = p6.merge(p1[["symbol","price_180d_ago","price_today","avg_daily_volume","penny_flag"]], on="symbol", how="left")
m = m.merge(p2[["symbol","rsi","adx","macd_pos","ema_alignment","supertrend","candle_bias","trend_structure"]], on="symbol", how="left")
m = m.merge(p3[["symbol","pd_zone","range_pos_pct","last_BoS","bull_OB","unfilled_bull_FVG","liquidity_swept","structure_W"]], on="symbol", how="left")
m = m.merge(p4[["symbol","vcp_quality","vcp_status","contractions","pivot","pct_from_pivot","gann_gann_trend","octave","sq9_T1_+0.25","sq9_T2_+0.5"]], on="symbol", how="left")

def recs(df):
    return json.loads(df.where(pd.notna(df), None).to_json(orient="records"))

DATA = {
 "master": recs(m),
 "watchlist": recs(wl),
 "fingerprint": recs(fp),
 "agg": {
   "universe_total": 4524,
   "phase1": int(len(p1)),
   "analyzed": int(len(p2)),
   "alpha": int((p6["tier"].isin(["TIER 1","TIER 2"])).sum()),
   "prime_passers": int(len(load("PHASE7_ALL_PASSERS.csv"))) if True else 0,
   "watchlist": int(len(wl)),
   "tiers6": p6["tier"].value_counts().to_dict(),
   "scorecards": p2["scorecard"].value_counts().to_dict(),
   "sectors_wl": wl["sector"].value_counts().to_dict() if "sector" in wl else {},
   "vcp_quality": p4["vcp_quality"].value_counts().to_dict(),
   "pd_zone": p3["pd_zone"].value_counts().to_dict(),
 },
 "market": {"nifty": 23484, "ema50": 23940, "ema200": 24667, "trend": "DOWNTREND"},
 "scan_date": "2026-06-02",
 "live_fetched_at": live_ts,
 "nifty_3m": round(nifty_ret, 1) if nifty_ret is not None else None,
}

HTML = r"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AlphaFinder — Systematic Equity Scanner</title>
<style>
:root{
 --bg:#0b0e14; --bg2:#121722; --bg3:#1a2130; --line:#243044; --txt:#e6edf3; --mut:#8b97a8;
 --accent:#3b82f6; --green:#22c55e; --red:#ef4444; --amber:#f59e0b; --cyan:#22d3ee; --violet:#a78bfa;
}
*{box-sizing:border-box} html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
header{padding:20px 28px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,#10151f,#0b0e14)}
.brand{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.logo{width:38px;height:38px;border-radius:9px;background:linear-gradient(135deg,var(--accent),var(--violet));display:grid;place-items:center;font-weight:800;font-size:18px}
h1{font-size:20px;margin:0;letter-spacing:.3px} .sub{color:var(--mut);font-size:12.5px;margin-top:2px}
.banner{margin:14px 28px 0;padding:10px 14px;border-radius:9px;border:1px solid #5b3b18;background:#2a1d0c;color:#ffce8a;font-size:13px;display:flex;gap:10px;align-items:center}
.banner.down{border-color:#5e2230;background:#2a1117;color:#ff9aa6}
nav{display:flex;gap:4px;padding:14px 24px 0;flex-wrap:wrap;border-bottom:1px solid var(--line);background:var(--bg)}
nav button{background:none;border:none;color:var(--mut);padding:10px 14px;border-radius:8px 8px 0 0;cursor:pointer;font-size:13.5px;font-weight:600;border-bottom:2px solid transparent}
nav button:hover{color:var(--txt);background:var(--bg2)}
nav button.active{color:var(--txt);border-bottom-color:var(--accent)}
main{padding:24px 28px;max-width:1500px}
section{display:none} section.active{display:block;animation:fade .25s}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1}}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-bottom:22px}
.card{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:16px}
.card .k{color:var(--mut);font-size:12px;text-transform:uppercase;letter-spacing:.5px}
.card .v{font-size:28px;font-weight:800;margin-top:6px} .card .v small{font-size:13px;color:var(--mut);font-weight:500}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:22px} @media(max-width:900px){.grid2{grid-template-columns:1fr}}
.panel{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:18px;margin-bottom:22px}
.panel h3{margin:0 0 14px;font-size:14px;letter-spacing:.3px}
.funnel{display:flex;flex-direction:column;gap:8px}
.fbar{display:flex;align-items:center;gap:12px}
.fbar .lbl{width:230px;color:var(--mut);font-size:13px}
.fbar .bar{height:26px;border-radius:6px;background:linear-gradient(90deg,var(--accent),var(--violet));display:flex;align-items:center;justify-content:flex-end;padding:0 8px;color:#fff;font-weight:700;font-size:12px;min-width:42px}
.bars .row{display:flex;align-items:center;gap:10px;margin-bottom:7px}
.bars .row .nm{width:130px;font-size:12.5px;color:var(--mut)}
.bars .row .tk{flex:1;height:18px;background:var(--bg3);border-radius:5px;overflow:hidden}
.bars .row .tk i{display:block;height:100%;border-radius:5px}
.bars .row .ct{width:42px;text-align:right;font-weight:700;font-size:12.5px}
.toolbar{display:flex;gap:10px;align-items:center;margin-bottom:12px;flex-wrap:wrap}
input.search{background:var(--bg2);border:1px solid var(--line);color:var(--txt);padding:9px 12px;border-radius:8px;width:280px;font-size:13px}
.pill{font-size:11px;padding:2px 8px;border-radius:20px;font-weight:700;white-space:nowrap}
.t1{background:#0e2a16;color:#5ef08a;border:1px solid #1c5a30}
.t2{background:#0e1f33;color:#7db8ff;border:1px solid #1d426e}
.t3{background:#2a230c;color:#ffce6a;border:1px solid #5b4a18}
.ex{background:#2a1117;color:#ff8c99;border:1px solid #5e2230}
.bull{color:var(--green);font-weight:700}.bear{color:var(--red);font-weight:700}.neu{color:var(--mut)}
.tablewrap{overflow:auto;border:1px solid var(--line);border-radius:12px;max-height:72vh}
table{border-collapse:collapse;width:100%;font-size:12.8px;white-space:nowrap}
thead th{position:sticky;top:0;background:var(--bg3);color:var(--mut);text-align:right;padding:10px 12px;font-weight:700;cursor:pointer;border-bottom:1px solid var(--line);user-select:none}
thead th:first-child,tbody td:first-child{text-align:left}
thead th.l,tbody td.l{text-align:left}
thead th:hover{color:var(--txt)}
tbody td{padding:9px 12px;text-align:right;border-bottom:1px solid #161d2a}
tbody tr:hover{background:var(--bg3);cursor:pointer}
.sym{font-weight:700;color:var(--cyan)}
.pos{color:var(--green)}.neg{color:var(--red)}
.muted{color:var(--mut)}
.modal{position:fixed;inset:0;background:rgba(3,6,12,.7);display:none;place-items:center;z-index:50;padding:20px}
.modal.open{display:grid}
.sheet{background:var(--bg2);border:1px solid var(--line);border-radius:16px;max-width:760px;width:100%;max-height:88vh;overflow:auto;padding:24px}
.sheet h2{margin:0 0 2px;font-size:20px}.sheet .x{float:right;cursor:pointer;color:var(--mut);font-size:22px;line-height:1}
.kv{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;margin-top:16px}
.kv .i{background:var(--bg3);border:1px solid var(--line);border-radius:9px;padding:10px 12px}
.kv .i .kk{color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.4px}
.kv .i .vv{font-size:14px;font-weight:600;margin-top:3px}
.sech{margin:18px 0 6px;color:var(--violet);font-size:12px;text-transform:uppercase;letter-spacing:.6px;font-weight:700}
.foot{color:var(--mut);font-size:11.5px;padding:24px 28px;border-top:1px solid var(--line);margin-top:20px}
.legend{display:flex;gap:14px;flex-wrap:wrap;color:var(--mut);font-size:12px;margin-top:8px}
</style></head><body>
<header>
 <div class="brand">
   <div class="logo">α</div>
   <div><h1>AlphaFinder <span class="muted" style="font-weight:500">· Systematic Equity Scanner (NSE + BSE)</span></h1>
   <div class="sub">7-phase pipeline · live exchange data · scan date <b id="sd"></b></div></div>
 </div>
 <div class="banner down" id="mkt"></div>
</header>
<nav id="nav"></nav>
<main>
 <section id="overview" class="active">
   <div class="cards" id="cards"></div>
   <div class="grid2">
     <div class="panel"><h3>Discovery funnel</h3><div class="funnel" id="funnel"></div></div>
     <div class="panel"><h3>Phase 6 tier distribution</h3><div class="bars" id="tiers"></div>
        <h3 style="margin-top:18px">Phase 2 scorecards</h3><div class="bars" id="scards"></div></div>
   </div>
   <div class="grid2">
     <div class="panel"><h3>VCP quality (Phase 4)</h3><div class="bars" id="vcpq"></div></div>
     <div class="panel"><h3>Watchlist sector breadth (Phase 7)</h3><div class="bars" id="wsec"></div></div>
   </div>
 </section>

 <section id="watchlist">
   <div class="panel" style="margin-bottom:18px"><h3>🎯 Phase 7 — Forward 25%+ Watchlist</h3>
     <div class="muted">Fresh candidates from the full universe matching the Phase-5 move-initiation fingerprint (≥6/9 confluence) + secondary validation. Every name R:R ≥ 3:1. Entry=breakout pivot, Stop=1.8×ATR. <b>Market is in a downtrend — stage, don't chase.</b></div>
     <div class="muted" id="wl_live_ts" style="margin-top:6px"></div></div>
   <div class="toolbar"><input class="search" id="s_wl" placeholder="Filter watchlist… (symbol / sector / stage)"></div>
   <div class="tablewrap"><table id="t_wl"></table></div>
 </section>

 <section id="ranking">
   <div class="toolbar"><input class="search" id="s_m" placeholder="Filter 311 ranked stocks… (symbol / sector / tier)">
     <span class="muted" id="m_count"></span></div>
   <div class="tablewrap"><table id="t_m"></table></div>
   <div class="legend"><span>Click any row for the full multi-phase dossier.</span></div>
 </section>

 <section id="fingerprint">
   <div class="panel" style="margin-bottom:18px"><h3>🧬 Phase 5 — Move-Initiation Fingerprint (Day-0 DNA)</h3>
     <div class="muted">Indicator state captured at the exact breakout bar of all 311 winners, then aggregated. Higher consistency % = more reliable filter. Backtest recall of the ≥6/9 filter on known winners: <b>76.2%</b>.</div></div>
   <div class="tablewrap"><table id="t_fp"></table></div>
 </section>
</main>
<div class="modal" id="modal"><div class="sheet" id="sheet"></div></div>
<div class="foot">Generated from live NSE/BSE + Yahoo Finance data via the AlphaFinder pipeline. Mechanical signals — sanity-check against live charts and overhead supply. <b>Not investment advice.</b></div>
<script>
const DATA = __DATA__;
const $=s=>document.querySelector(s), el=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
$("#sd").textContent=DATA.scan_date;
const mk=DATA.market;$("#mkt").innerHTML=`⚠️ <b>Market context:</b> Nifty 50 = ${mk.nifty} &nbsp;|&nbsp; EMA50 ${mk.ema50} &nbsp;|&nbsp; EMA200 ${mk.ema200} &nbsp;→&nbsp; <b>${mk.trend}</b> &nbsp;·&nbsp; reduce size / await 50-EMA reclaim before acting.`;
if(DATA.live_fetched_at)$("#wl_live_ts").innerHTML=`🟢 <b>Live</b> prices + <b>validation</b> fetched <b>${DATA.live_fetched_at}</b> (Yahoo). <b>Check</b> = Layer-1 mechanical verdict: <span class="pill t1">✓ GO</span> alive+triggered+volume+RS+not-extended · <span class="pill t3">… WATCH</span> alive but not a clean trigger · <span class="pill ex">✕ DROP</span> below stop / illiquid.${DATA.nifty_3m!=null?` Nifty 3-mo: <b>${DATA.nifty_3m>0?'+':''}${DATA.nifty_3m}%</b> (RS baseline).`:''} <b>Stage:</b> <span class="pill t2">● early</span> coiled below entry (% = rise needed to trigger) · <span class="pill t1">▲ moving</span> broke out, advancing (% = move done) · <span class="pill ex">✕ failed</span> below stop. <i>Mechanical only — still check surveillance/earnings/chart.</i>`;

const TABS=[["overview","Overview"],["watchlist","🎯 Watchlist"],["ranking","Ranked 311"],["fingerprint","🧬 Fingerprint"]];
const nav=$("#nav");
TABS.forEach(([id,lb],i)=>{const b=el("button",i==0?"active":"",lb);b.onclick=()=>{document.querySelectorAll("nav button").forEach(x=>x.classList.remove("active"));b.classList.add("active");document.querySelectorAll("section").forEach(s=>s.classList.remove("active"));$("#"+id).classList.add("active")};nav.appendChild(b)});

// ---- overview ----
const A=DATA.agg;
const cards=[["Universe scanned",A.universe_total,""],["Phase 1: 25%+ movers",A.phase1,"verified"],["Fully analysed",A.analyzed,"stocks"],["Alpha list (T1+T2)",A.alpha,"Phase 6"],["Prime-filter passers",A.prime_passers,"of 4,524"],["Final watchlist",A.watchlist,"R:R≥3"]];
cards.forEach(([k,v,s])=>{const c=el("div","card");c.innerHTML=`<div class="k">${k}</div><div class="v">${v} <small>${s}</small></div>`;$("#cards").appendChild(c)});
const funnel=[["NSE+BSE universe",A.universe_total],["Phase 1 — 25%+ in 180d",A.phase1],["Phases 2-4 analysed",A.analyzed],["Phase 6 Alpha (T1+T2)",A.alpha],["Phase 7 prime passers",A.prime_passers],["Final watchlist",A.watchlist]];
const fmax=A.universe_total;
funnel.forEach(([l,v])=>{const r=el("div","fbar");r.innerHTML=`<div class="lbl">${l}</div><div class="bar" style="width:${Math.max(4,v/fmax*100)}%">${v}</div>`;$("#funnel").appendChild(r)});
function bars(host,obj,order,colors){const max=Math.max(...Object.values(obj));const keys=order||Object.keys(obj);keys.forEach(k=>{if(obj[k]==null)return;const r=el("div","row");r.innerHTML=`<div class="nm">${k}</div><div class="tk"><i style="width:${obj[k]/max*100}%;background:${(colors&&colors[k])||'var(--accent)'}"></i></div><div class="ct">${obj[k]}</div>`;host.appendChild(r)})}
bars($("#tiers"),A.tiers6,["TIER 1","TIER 2","TIER 3","EXCLUDE"],{"TIER 1":"var(--green)","TIER 2":"var(--cyan)","TIER 3":"var(--amber)","EXCLUDE":"var(--red)"});
bars($("#scards"),A.scorecards,["BULLISH","MILD BULLISH","NEUTRAL","MILD BEARISH","BEARISH"],{"BULLISH":"var(--green)","MILD BULLISH":"#6fcf97","NEUTRAL":"var(--mut)","MILD BEARISH":"#f0a35e","BEARISH":"var(--red)"});
bars($("#vcpq"),A.vcp_quality,["Strong VCP","Moderate VCP","No VCP"],{"Strong VCP":"var(--green)","Moderate VCP":"var(--cyan)","No VCP":"var(--mut)"});
bars($("#wsec"),A.sectors_wl,null,{});

// ---- table builder ----
function buildTable(tbl, rows, cols, opts){
 opts=opts||{}; tbl.innerHTML="";
 const thead=el("thead"),tr=el("tr");
 cols.forEach(c=>{const th=el("th",c.l?"l":"",c.h);th.onclick=()=>sortBy(c.k);tr.appendChild(th)});
 thead.appendChild(tr);tbl.appendChild(thead);
 const tb=el("tbody");tbl.appendChild(tb);
 let sortKey=opts.sort||cols[0].k, asc=false;
 function render(list){tb.innerHTML="";list.forEach(r=>{const trr=el("tr");cols.forEach(c=>{const td=el("td",c.l?"l":"");td.innerHTML=c.f?c.f(r[c.k],r):fmt(r[c.k]);trr.appendChild(td)});if(opts.onclick)trr.onclick=()=>opts.onclick(r);tb.appendChild(trr)})}
 function sortBy(k){asc=(k===sortKey)?!asc:false;sortKey=k;const s=[...(tbl._data)].sort((a,b)=>{let x=a[k],y=b[k];if(x==null)return 1;if(y==null)return -1;if(typeof x==="number"&&typeof y==="number")return asc?x-y:y-x;return asc?(""+x).localeCompare(""+y):(""+y).localeCompare(""+x)});render(s)}
 tbl._data=rows; tbl._render=render; tbl._sort=sortBy;
 sortBy(sortKey);
}
function fmt(v){if(v==null)return '<span class="muted">—</span>';if(typeof v==="number")return Number.isInteger(v)?v.toLocaleString():v;return v}
function tierPill(t){const m={"TIER 1":"t1","TIER 2":"t2","TIER 3":"t3","EXCLUDE":"ex"};return `<span class="pill ${m[t]||''}">${t}</span>`}
function sgn(v){if(v==null)return fmt(v);const c=v>=0?"pos":"neg";return `<span class="${c}">${v>0?'+':''}${v}%</span>`}
function vcpCell(v){if(!v||v=="No VCP")return '<span class="muted">—</span>';return v.includes("Strong")?`<span class="bull">${v}</span>`:`<span style="color:var(--cyan)">${v}</span>`}
function scCell(v){if(!v)return '—';if(v.includes("BULL"))return `<span class="bull">${v}</span>`;if(v.includes("BEAR"))return `<span class="bear">${v}</span>`;return `<span class="neu">${v}</span>`}
function liveCell(v,r){if(v==null)return '<span class="muted">—</span>';const c=r.live_chg==null?'':(r.live_chg>=0?'pos':'neg');const ch=r.live_chg==null?'':` <small class="${c}">${r.live_chg>0?'+':''}${r.live_chg}%</small>`;return `<b>${v}</b>${ch}`}
function liveStatus(r){if(r.live==null)return '<span class="muted">—</span>';if(r.live_state=='above')return '<span class="pill t1">▲ above entry</span>';if(r.live_state=='stop')return '<span class="pill ex">▼ below stop</span>';return `<span class="muted">+${r.live_to_entry}% to entry</span>`}
function valCell(r){const v=r.verdict;if(!v||v=='NO DATA')return '<span class="muted">—</span>';const m={GO:'t1',WATCH:'t3',DROP:'ex'},ic={GO:'✓',WATCH:'…',DROP:'✕'};const tip=`${r.vreason} · ${r.vpassed}/6 checks pass · fails: ${r.vfails} · vol ${r.vol_x}× · ext ${r.ext_pct}% · ₹${r.adv_cr}cr/d · RS ${r.rs>0?'+':''}${r.rs}%`;return `<span class="pill ${m[v]}" title="${tip}">${ic[v]} ${v}</span>`}
function stageCell(r){const s=r.stage;if(!s||s=='NO DATA')return '<span class="muted">—</span>';if(s=='MOVING')return `<span class="pill t1" title="${r.stage_pct}% of the entry→target move already done">▲ moving <small>${r.stage_pct}%</small></span>`;if(s=='FAILED')return '<span class="pill ex" title="below stop — setup invalidated">✕ failed</span>';return `<span class="pill t2" title="coiled — needs +${r.stage_pct}% to trigger the breakout entry">● early <small>+${r.stage_pct}%</small></span>`}

// ---- watchlist table ----
buildTable($("#t_wl"), DATA.watchlist, [
 {k:"rank",h:"#"},{k:"symbol",h:"Symbol",l:1,f:v=>`<span class="sym">${v}</span>`},
 {k:"verdict",h:"Check",l:1,f:(v,r)=>valCell(r)},
 {k:"name",h:"Company",l:1,f:v=>`<span class="muted">${(v||'').slice(0,22)}</span>`},
 {k:"sector",h:"Sector",l:1},{k:"close",h:"Scan px"},
 {k:"live",h:"Live",f:liveCell},{k:"live_to_entry",h:"vs Plan",l:1,f:(v,r)=>liveStatus(r)},
 {k:"stage",h:"Stage",l:1,f:(v,r)=>stageCell(r)},{k:"upside_tgt",h:"Upside→T",f:v=>v==null?'<span class="muted">—</span>':`<span class="pos">+${v}%</span>`},
 {k:"vcp_status",h:"VCP stage",l:1,f:v=>v&&v.includes("PIVOT")?`<span style="color:var(--cyan)">at pivot</span>`:v&&v.includes("BROKEN")?`<span class="bull">fresh BO</span>`:`<span class="muted">${v}</span>`},
 {k:"rsi",h:"RSI"},{k:"adx",h:"ADX"},{k:"pivot_entry",h:"Entry"},{k:"stop",h:"Stop"},
 {k:"stop_pct",h:"Stop%",f:v=>`${v}%`},{k:"target2",h:"Target"},
 {k:"rr",h:"R:R",f:v=>`<b style="color:${v>=4?'var(--green)':'var(--cyan)'}">${v}</b>`},
 {k:"qty_per_10L",h:"Qty/₹10L"},{k:"phase7_score",h:"Score"},{k:"tier",h:"Tier",f:tierPill}
], {sort:"rank", onclick:r=>showDetail(r,true)});

// ---- master ranking table ----
const M=DATA.master;
buildTable($("#t_m"), M, [
 {k:"rank",h:"#"},{k:"symbol",h:"Symbol",l:1,f:v=>`<span class="sym">${v}</span>`},
 {k:"name",h:"Company",l:1,f:v=>`<span class="muted">${(v||'').slice(0,24)}</span>`},
 {k:"exchange",h:"Exch",l:1},{k:"sector",h:"Sector",l:1},
 {k:"return_pct_final",h:"6m Ret",f:sgn},{k:"close",h:"Price"},
 {k:"scorecard",h:"P2 Verdict",l:1,f:scCell},
 {k:"TOTAL_100",h:"P6 /100",f:v=>`<b>${v}</b>`},{k:"tier",h:"Tier",f:tierPill},
 {k:"vcp_quality",h:"VCP",l:1,f:vcpCell},{k:"pd_zone",h:"P/D",l:1},
 {k:"rsi",h:"RSI"},{k:"adx",h:"ADX"},{k:"supertrend",h:"S/T",l:1,f:v=>v&&v.includes("green")?'<span class="bull">green</span>':'<span class="bear">red</span>'}
], {sort:"rank", onclick:r=>showDetail(r,false)});
$("#m_count").textContent=M.length+" stocks";

// ---- fingerprint table ----
buildTable($("#t_fp"), DATA.fingerprint, [
 {k:"indicator",h:"Indicator",l:1,f:v=>`<b>${v}</b>`},{k:"type",h:"Type",l:1,f:v=>`<span class="muted">${v}</span>`},
 {k:"min",h:"Min"},{k:"max",h:"Max"},{k:"avg",h:"Avg"},{k:"median",h:"Median"},
 {k:"most_common_zone",h:"Most-common zone",l:1,f:v=>`<span style="color:var(--cyan)">${v}</span>`},
 {k:"consistency_pct",h:"Consistency",f:v=>{const c=v>=80?'var(--green)':v>=60?'var(--amber)':'var(--mut)';return `<b style="color:${c}">${v}%</b>`}}
], {sort:"consistency_pct"});

// ---- search wiring ----
function wire(inp,tbl){$(inp).addEventListener("input",e=>{const q=e.target.value.toLowerCase();const f=tbl._data.filter(r=>Object.values(r).some(v=>v!=null&&(""+v).toLowerCase().includes(q)));tbl._render(f)})}
wire("#s_wl",$("#t_wl")); wire("#s_m",$("#t_m"));

// ---- detail modal ----
function row(k,v){return `<div class="i"><div class="kk">${k}</div><div class="vv">${v==null||v===""?'—':v}</div></div>`}
function showDetail(r,isWl){
 const s=$("#sheet");
 const title=`${r.symbol} — ${r.name||''}`;
 let h=`<span class="x" onclick="document.getElementById('modal').classList.remove('open')">&times;</span><h2>${title}</h2>`;
 h+=`<div class="muted">${r.exchange||''} ${r.sector?'· '+r.sector:''} ${r.cap_bucket?'· '+r.cap_bucket+' cap':''} ${r.tier?'· ':''}${r.tier?tierPill(r.tier):''}</div>`;
 if(isWl){
   h+='<div class="sech">Phase 7 — Trade plan</div><div class="kv">';
   const liveTxt=r.live==null?'—':`${r.live}${r.live_chg==null?'':' ('+(r.live_chg>0?'+':'')+r.live_chg+'%)'} `+(r.live_state=='above'?'▲ above entry':r.live_state=='stop'?'▼ below stop':'+'+r.live_to_entry+'% to entry');
   const valTxt=r.verdict&&r.verdict!='NO DATA'?`${r.verdict} — ${r.vreason} (${r.vpassed}/6: vol ${r.vol_x}×, ext ${r.ext_pct}%, ₹${r.adv_cr}cr/d, RS ${r.rs>0?'+':''}${r.rs}%)`:'—';
   const stgTxt=r.stage=='MOVING'?`MOVING — ${r.stage_pct}% of move done, +${r.upside_tgt}% left to target`:r.stage=='EARLY'?`EARLY (coiled) — needs +${r.stage_pct}% to trigger, +${r.upside_tgt}% to target`:r.stage=='FAILED'?'FAILED — below stop':'—';
   h+=row("Stage",stgTxt)+row("Validation (Layer-1)",valTxt)+row("Scan-time close",r.close)+row("Live price",liveTxt)+row("VCP stage",r.vcp_status)+row("Entry (pivot)",r.pivot_entry)+row("Stop (1.8×ATR)",r.stop)+row("Stop %",r.stop_pct+"%")+row("Gann T1",r.gann_T1)+row("Target",r.target2)+row("Risk:Reward",r.rr)+row("Qty / ₹10L (1% risk)",r.qty_per_10L)+row("RSI",r.rsi)+row("ADX",r.adx)+row("Vol spike",r.vol_spike+"×")+row("SMC zone",r.pd_zone)+row("Gann > 1×1",r.gann_above_1x1)+row("Confluence score",r.phase7_score)+"</div>";
   h+=`<div class="sech">Recent candles</div><div class="muted">${r.last_candles||'—'}</div>`;
 } else {
   h+='<div class="sech">Phase 1 — Performance</div><div class="kv">';
   h+=row("6-month return", (r.return_pct_final>0?'+':'')+r.return_pct_final+"%")+row("Price 180d ago",r.price_180d_ago)+row("Price now",r.price_today)+row("Avg daily vol",r.avg_daily_volume)+"</div>";
   h+='<div class="sech">Phase 2 — Technicals</div><div class="kv">';
   h+=row("Scorecard",r.scorecard)+row("RSI",r.rsi)+row("ADX",r.adx)+row("MACD",r.macd_pos)+row("EMA align",r.ema_alignment)+row("Supertrend",r.supertrend)+row("Candle bias",r.candle_bias)+row("Trend structure",r.trend_structure)+"</div>";
   h+='<div class="sech">Phase 3 — Smart Money</div><div class="kv">';
   h+=row("Premium/Discount",r.pd_zone)+row("Range position",r.range_pos_pct+"%")+row("Weekly structure",r.structure_W)+row("Last BoS",r.last_BoS)+row("Bullish OB",r.bull_OB)+row("Unfilled bull FVGs",r.unfilled_bull_FVG)+row("Liquidity swept",r.liquidity_swept)+"</div>";
   h+='<div class="sech">Phase 4 — VCP + Gann</div><div class="kv">';
   h+=row("VCP quality",r.vcp_quality)+row("VCP status",r.vcp_status)+row("Contractions",r.contractions)+row("Pivot",r.pivot)+row("% from pivot",r.pct_from_pivot+"%")+row("Gann trend",r.gann_gann_trend)+row("Octave",r.octave)+row("Gann T1",r["sq9_T1_+0.25"])+row("Gann T2",r["sq9_T2_+0.5"])+"</div>";
   h+='<div class="sech">Phase 6 — Confluence score</div><div class="kv">';
   h+=row("Indicators /40",r.ind_score_40)+row("Structure /25",r.struct_score_25)+row("VCP /20",r.vcp_score_20)+row("Gann /15",r.gann_score_15)+row("TOTAL /100",r.TOTAL_100)+"</div>";
 }
 s.innerHTML=h; $("#modal").classList.add("open");
}
$("#modal").onclick=e=>{if(e.target.id=="modal")$("#modal").classList.remove("open")};
</script></body></html>"""

out = HTML.replace("__DATA__", json.dumps(DATA, separators=(",",":")))
open("alphafinder_dashboard.html","w",encoding="utf-8").write(out)
print(f"Wrote alphafinder_dashboard.html ({len(out)//1024} KB) | master={len(DATA['master'])} watchlist={len(DATA['watchlist'])} fingerprint={len(DATA['fingerprint'])}")
