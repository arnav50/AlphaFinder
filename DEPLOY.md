# Deploying AlphaFinder — Vercel (frontend) + Render (backend)

## The big idea (why the ~500-file churn doesn't matter)

`alphafinder_dashboard.html` is **fully self-contained** — `25_build_frontend.py`
embeds every CSV into it. So:

- **Vercel serves only that one HTML file.** All the `PHASE*.csv`, `reports/*.md`,
  `*.pkl`, logs, etc. are pipeline *build artifacts* Vercel never needs
  (`.vercelignore` keeps the deploy to just the dashboard).
- The "500 changes per run" is only *git noise*, and here it's actually the
  **deploy trigger**: the Render cron rebuilds the dashboard, commits, and pushes;
  Vercel redeploys on that push.

**Chosen setup: local-only refresh** — the deployed dashboard always equals your
local run. You run the pipeline locally (where NSE/Yahoo aren't IP-blocked), then
commit & push the rebuilt HTML; Vercel serves it verbatim. Render runs only the
alert web service. No cron.

```
Local:  python run_pipeline.py ──rebuild HTML──git push──▶ GitHub
                                                              │
                                                   Vercel auto-redeploy (exact local data)
Deployed "Add alert" ──POST /add-alert──▶ Render web service (alert_server.py)
```

## Files added for deployment

| File | Purpose |
|---|---|
| `requirements.txt` | Python deps for Render (pandas/numpy/requests/curl_cffi, pinned) |
| `vercel.json` | Static config: `/` → `alphafinder_dashboard.html` |
| `.vercelignore` | Deploy only the dashboard, nothing else |
| `render.yaml` | Blueprint: `web` (alerts) only — cron removed for local-only refresh |
| `render_web.sh` | Web start command |
| `render_refresh.sh` | *(unused in local-only setup; kept for optional cloud cron)* |
| `.gitattributes` | Force LF on `*.sh` (Windows→Linux safety) |

Code changes: `alert_server.py` now honors `PORT`/`HOST`/`ALERTS_CONFIG_PATH`
(+ optional git push); `25_build_frontend.py` bakes `ALPHAFINDER_BACKEND_URL`
into the dashboard's Add-alert button.

---

## Part 1 — Frontend on Vercel

1. Push this repo to GitHub (see Part 3 for commit).
2. vercel.com → **Add New… → Project** → import this repo.
3. Framework preset: **Other**. Build command: *(leave empty)*. Output dir: *(leave empty)*.
4. **Deploy.** Your dashboard is live at `https://<project>.vercel.app`.

Every future `git push` to `main` (including the Render cron's refresh commits)
auto-redeploys the latest dashboard.

## Part 2 — Backend on Render (alert web service only)

1. render.com → **New → Blueprint** → connect this repo. Render reads `render.yaml`
   and proposes a single **web** service (`alphafinder-alerts`). No secrets needed.
2. **Apply.** The service comes up at `https://alphafinder-mrye.onrender.com`.
   - This exact URL is already baked into the deployed dashboard's "Add alert"
     button. **If you rename the service, rebuild the dashboard with the new URL**
     (see the refresh command below) so the button keeps working.
3. That's it — no cron, no GitHub token. Data refreshes come from your local push
   (Part 3 / the refresh command), not from Render.

> Free web services **spin down when idle**; the first "Add alert" click after a
> quiet period wakes it (a few seconds) — fine for a personal tool.

---

## Refreshing the deployed data (local-only)

Whenever you want the live site to show new data, run this locally and push. It
rebuilds the self-contained dashboard **with the Render backend URL baked in**, so
the deployed "Add alert" button keeps working:

```powershell
# PowerShell (Windows)
$env:ALPHAFINDER_BACKEND_URL = "https://alphafinder-mrye.onrender.com"
python run_pipeline.py
git add -A
git commit -m "chore: data refresh"
git push          # Vercel auto-redeploys the exact dashboard you just built
```

Because the HTML embeds every CSV, **what you see at `localhost` is byte-for-byte
what Vercel serves.** If step 22/28–31 fail on NSE blocks locally too, re-run just
those later — the pushed dashboard only updates when the pipeline completes.

---

## Where dashboard-added alerts go (local-only setup)

Alerts you add from the **deployed** dashboard POST to the Render web service and
persist on its **1 GB disk** (`ALERTS_CONFIG_PATH=/var/data/...`,
`ALERTS_GIT_PUSH=0`). They are **not** fed back into the pipeline — which you run
locally against the repo's own `ALERTS_CONFIG.csv`.

> Optional (only if you later want deployed alerts to reach your local pipeline):
> set `ALERTS_CONFIG_PATH=ALERTS_CONFIG.csv` + `ALERTS_GIT_PUSH=1` on the web
> service and add a `GITHUB_TOKEN` (fine-grained PAT, *Contents: read/write*),
> `GITHUB_REPO`, `GIT_USER_EMAIL`. Each alert then commits & pushes to git, which
> your next local `git pull` picks up.

---

## Known caveats / things to watch

- **NSE may block non-Indian datacenter IPs — this is exactly why we refresh
  locally.** The pipeline hits live NSE/Yahoo/BSE endpoints; from Render's
  datacenter these can 503 or return empty. Running the pipeline on your own
  machine sidesteps that entirely, and the push is what updates Vercel.
- **Free web service sleeps when idle.** First "Add alert" click after a quiet
  period wakes it (a few seconds) — fine for a personal tool.
- **Python version** is pinned to 3.10.0 on Render to match local (3.10.0).

## Run locally

```powershell
# rebuild everything (bake the Render URL so the deployed button works), then push
$env:ALPHAFINDER_BACKEND_URL = "https://alphafinder-mrye.onrender.com"
python run_pipeline.py
python alert_server.py          # http://localhost:8777/alphafinder_dashboard.html
```
