#!/usr/bin/env bash
# Start command for the Render web service (alert_server.py).
set -euo pipefail

# Strategy A: seed the persistent-disk config from the repo baseline on first boot.
if [ -n "${ALERTS_CONFIG_PATH:-}" ] && [ "$ALERTS_CONFIG_PATH" != "ALERTS_CONFIG.csv" ]; then
  if [ ! -f "$ALERTS_CONFIG_PATH" ] && [ -f ALERTS_CONFIG.csv ]; then
    mkdir -p "$(dirname "$ALERTS_CONFIG_PATH")"
    cp ALERTS_CONFIG.csv "$ALERTS_CONFIG_PATH"
  fi
fi

# Strategy B: if pushing dashboard-added alerts back to git, configure auth once.
if [ "${ALERTS_GIT_PUSH:-0}" = "1" ] && [ -n "${GITHUB_TOKEN:-}" ] && [ -n "${GITHUB_REPO:-}" ]; then
  git config user.email "${GIT_USER_EMAIL:-bot@alphafinder.local}"
  git config user.name  "AlphaFinder Bot"
  git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git"
fi

exec python alert_server.py
