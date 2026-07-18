"""Run AlphaFinder 02..31 (skip 01 — NSE archive is IP-blocked; reuse existing universe.csv).
Continue-on-failure so one blocked/network step doesn't abort the rest. 25 forced last.
Prints a per-step status summary at the end.
"""
import glob, os, subprocess, sys, time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FRONTEND = "25_build_frontend.py"
scripts = sorted(s for s in glob.glob("[0-9][0-9]_*.py"))
scripts = [s for s in scripts if not s.startswith("01_")]      # skip NSE universe refresh
if FRONTEND in scripts:                                        # always build dashboard last
    scripts = [s for s in scripts if s != FRONTEND] + [FRONTEND]

print(f"=== PIPELINE START (no-01): {len(scripts)} scripts ===", flush=True)
results = []
for s in scripts:
    ts = time.strftime("%H:%M:%S")
    print(f"=== START {s} {ts} ===", flush=True)
    t0 = time.time()
    rc = subprocess.call([sys.executable, "-u", s])
    dt = time.time() - t0
    tag = "OK" if rc == 0 else f"FAIL(exit {rc})"
    results.append((s, tag, round(dt, 1)))
    print(f"=== {tag} {s} in {dt:.1f}s ({time.strftime('%H:%M:%S')}) ===", flush=True)

print("\n=== PIPELINE SUMMARY ===", flush=True)
for s, tag, dt in results:
    print(f"  {tag:14s} {dt:8.1f}s  {s}", flush=True)
nfail = sum(1 for _, t, _ in results if t != "OK")
print(f"=== COMPLETE: {len(results)-nfail} ok, {nfail} failed ===", flush=True)
