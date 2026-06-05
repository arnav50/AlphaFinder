"""Phase 4: VCP + Gann for all stocks. Output PHASE4_VCP_GANN.csv"""
import pickle, pandas as pd
import ta_vcp_gann as VG

def analyze(sym, df):
    df = df.reset_index(drop=True)
    R = {"symbol": sym, "close": round(float(df["close"].iloc[-1]),2), "bars": len(df)}
    R.update(VG.detect_vcp(df))
    g = VG.gann_angles(df); R.update({f"gann_{k}":v for k,v in g.items()})
    R.update({f"sq9_{k}":v for k,v in VG.gann_square9(R["close"]).items()})
    R.update(VG.gann_time_cycles(g["days_since_low"]))
    R.update(VG.gann_octave(df))
    R.update(VG.gann_cardinal(R["close"]))
    return R

if __name__ == "__main__":
    import sys
    data = pickle.load(open("ohlc.pkl","rb"))
    if len(sys.argv)>1 and sys.argv[1]=="sample":
        for s in ["MARKSANS","STLTECH","CUMMINSIND","540492","GALAPREC"]:
            r=analyze(s,data[s])
            print(f"\n=== {s} px={r['close']} ===")
            for k in ["prior_uptrend","pct_above_52w_low","num_contractions","contractions","depths_decreasing",
                      "vdu_confirmed","vdu_ratio","near_52w_high","pivot","pct_from_pivot","breakout_vol_ratio",
                      "vcp_status","vcp_quality","entry_zone","gann_days_since_low","gann_above_1x1","gann_g1x1",
                      "sq9_T1_+0.25","sq9_T2_+0.5","sq9_T3_+1.0","next_gann_cycle_days","near_gann_cycle",
                      "octave","near_cardinal","nearest_cardinal_sq"]:
                print(f"  {k}: {r.get(k)}")
        sys.exit()
    rows=[]
    for i,(sym,df) in enumerate(data.items(),1):
        try: rows.append(analyze(sym,df))
        except Exception as e: rows.append({"symbol":sym,"error":f"{type(e).__name__}:{e}"})
        if i%80==0: print(f"  {i}/{len(data)}")
    out=pd.DataFrame(rows); out.to_csv("PHASE4_VCP_GANN.csv",index=False)
    print(f"DONE {len(out)} -> PHASE4_VCP_GANN.csv")
    if "error" in out: print("errors:",out["error"].notna().sum())
    print("vcp_quality:",out["vcp_quality"].value_counts().to_dict())
    print("vcp_status:",out["vcp_status"].value_counts().to_dict())
    print("octave:",out["octave"].value_counts().to_dict())
    print("above_1x1:",out["gann_above_1x1"].value_counts().to_dict())
    print("near_gann_cycle:",out["near_gann_cycle"].sum(),"| near_cardinal:",out["near_cardinal"].sum())
