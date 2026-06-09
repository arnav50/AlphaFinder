"""Run the AlphaFinder pipeline 01..25 in order. Stops on first failure."""
import glob, os, re, subprocess, sys, time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
scripts = sorted(s for s in glob.glob("[0-9][0-9]_*.py"))
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
