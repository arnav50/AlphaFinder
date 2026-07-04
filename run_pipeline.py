"""Run the AlphaFinder pipeline in order. Stops on first failure.

The frontend builder (25) is forced to run LAST: it embeds every upstream CSV,
including SWING_TRADES.csv from 26_swing.py, so it must build after 26.
"""
import glob, os, re, subprocess, sys, time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FRONTEND = "25_build_frontend.py"
scripts = sorted(s for s in glob.glob("[0-9][0-9]_*.py"))
if FRONTEND in scripts:                      # always build the dashboard last
    scripts = [s for s in scripts if s != FRONTEND] + [FRONTEND]
print(f"=== PIPELINE START: {len(scripts)} scripts ===", flush=True)
for s in scripts:
    ts = time.strftime("%H:%M:%S")
    print(f"=== START {s} {ts} ===", flush=True)
    rc = subprocess.call([sys.executable, "-u", s])
    if rc != 0:
        print(f"=== FAILED {s} (exit {rc}) ===", flush=True)
        sys.exit(rc)
    print(f"=== DONE {s} {time.strftime('%H:%M:%S')} ===", flush=True)
print("=== PIPELINE COMPLETE ===", flush=True)
