#!/usr/bin/env bash
# Render cron job: rebuild the dashboard from fresh market data, then commit &
# push so Vercel (connected to the same GitHub repo) auto-redeploys the frontend.
set -euo pipefail

: "${GITHUB_TOKEN:?set GITHUB_TOKEN in Render env}"
: "${GITHUB_REPO:?set GITHUB_REPO (owner/name) in Render env}"

git config user.email "${GIT_USER_EMAIL:-bot@alphafinder.local}"
git config user.name  "AlphaFinder Bot"
git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git"

git fetch origin main
git checkout main
git pull --rebase --autostash origin main

echo ">>> running pipeline ($(python --version))"
python run_pipeline.py

git add -A
if git diff --cached --quiet; then
  echo ">>> no changes to commit"
else
  git commit -m "chore: scheduled data refresh"
  git push origin main
  echo ">>> pushed refresh — Vercel will redeploy the dashboard"
fi
