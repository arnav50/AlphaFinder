"""Tiny local helper so the dashboard's alert builder can APPEND rows to ALERTS_CONFIG.csv.

Run it:   py -3.10 alert_server.py
Then either:
  • open  http://localhost:8777/alphafinder_dashboard.html   (same-origin, cleanest), or
  • keep using the file:// dashboard — it POSTs here (CORS + private-network headers set).

Endpoints:  POST /add-alert  {expiry,strike,side,metric,op,value,tf,note}  -> appends one row.
The alert engine (31_fno_alerts.py) then picks the new condition up on its next evaluation.
"""
import http.server, socketserver, json, os, csv, subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = int(os.environ.get("PORT", "8777"))          # Render injects $PORT
HOST = os.environ.get("HOST", "127.0.0.1")          # set 0.0.0.0 on Render
CFG  = os.environ.get("ALERTS_CONFIG_PATH", "ALERTS_CONFIG.csv")
GIT_PUSH = os.environ.get("ALERTS_GIT_PUSH", "0") == "1"   # commit+push each new alert
COLS = ["expiry", "strike", "side", "metric", "op", "value", "tf", "note"]


def _git_push_alert(line):
    """Commit the appended alert so the scheduled pipeline (which reads the
    git-tracked ALERTS_CONFIG.csv) picks it up. No-op unless ALERTS_GIT_PUSH=1
    and git auth is configured on the host."""
    if not GIT_PUSH:
        return
    try:
        subprocess.run(["git", "add", CFG], check=True)
        subprocess.run(["git", "commit", "-m", f"chore: alert via dashboard [{line}]"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("  git: pushed new alert", flush=True)
    except Exception as e:
        print(f"  git push failed (alert saved locally): {e}", flush=True)


def append_row(d):
    row = [str(d.get(c, "")).replace(",", " ").replace("\n", " ").strip() for c in COLS]
    if not row[3] or not row[4] or row[5] == "":          # metric / op / value required
        raise ValueError("metric, op and value are required")
    new = not os.path.exists(CFG)
    if not new and os.path.getsize(CFG) > 0:               # ensure a trailing newline before append
        with open(CFG, "rb") as f:
            f.seek(-1, 2); last = f.read(1)
        if last not in (b"\n", b"\r"):
            with open(CFG, "a", encoding="utf-8") as f:
                f.write("\n")
    with open(CFG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(COLS)
        w.writerow(row)
    return ",".join(row)


class H(http.server.SimpleHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")   # Chrome PNA (file:// -> localhost)

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def _json(self, code, obj):
        self.send_response(code); self._cors()
        self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps(obj).encode())

    def do_POST(self):
        if self.path.split("?")[0] != "/add-alert":
            return self._json(404, {"ok": False, "error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n) or b"{}")
            line = append_row(d)
            print(f"  + appended: {line}", flush=True)
            _git_push_alert(line)
            self._json(200, {"ok": True, "line": line})
        except Exception as e:
            self._json(400, {"ok": False, "error": str(e)})

    def end_headers(self):                                  # add CORS to static GETs too
        if self.command == "GET":
            self._cors()
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), H) as httpd:
        print(f"Alert helper running on http://{HOST}:{PORT}")
        print(f"  auto-append target: {CFG}  (git push: {'on' if GIT_PUSH else 'off'})")
        print(f"  same-origin dashboard: http://{HOST}:{PORT}/alphafinder_dashboard.html")
        print("  Ctrl+C to stop.")
        httpd.serve_forever()
