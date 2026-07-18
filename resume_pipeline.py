"""Resume the AlphaFinder pipeline from a given step number (inclusive).

Same contract as run_pipeline.py (stops on first failure, builds the frontend
25 last) but skips already-completed early steps whose outputs are on disk.
Usage: python resume_pipeline.py 7   # run steps 07..31, dashboard last
"""
import glob, os, subprocess, sys, time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
FRONTEND = "25_build_frontend.py"
scripts = sorted(s for s in glob.glob("[0-9][0-9]_*.py") if int(s[:2]) >= start)
if FRONTEND in scripts:                      # always build the dashboard last
    scripts = [s for s in scripts if s != FRONTEND] + [FRONTEND]
print(f"=== RESUME FROM {start:02d}: {len(scripts)} scripts ===", flush=True)
for s in scripts:
    print(f"=== START {s} {time.strftime('%H:%M:%S')} ===", flush=True)
    rc = subprocess.call([sys.executable, "-u", s])
    if rc != 0:
        print(f"=== FAILED {s} (exit {rc}) ===", flush=True)
        sys.exit(rc)
    print(f"=== DONE {s} {time.strftime('%H:%M:%S')} ===", flush=True)
print("=== PIPELINE COMPLETE ===", flush=True)
