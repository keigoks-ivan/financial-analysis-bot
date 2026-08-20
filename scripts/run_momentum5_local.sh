#!/bin/bash
# Momentum-5 weekly data updater — runs from the isolated ~/automation/momentum5-runner
# clone (NOT the main working repo). GitHub Actions can no longer refresh
# eps_trend (Yahoo blocks the CI IP range since 2026-08), so this replaces the
# weekly build with a local launchd job on this Mac. The CI workflow
# .github/workflows/weekly-market-update.yml is left untouched.
#
# Exit codes:
#   0 = gate skipped (not due yet) OR build+commit+push succeeded
#   1 = build ran but produced no data.json change (fail-safe likely tripped,
#       or push failed after retries) — launchd log should surface this
set -euo pipefail

PY=/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
REPO_DIR="$HOME/automation/momentum5-runner"
LOG="$HOME/Library/Logs/momentum5-weekly.log"
DATA_JSON="docs/research/momentum-5/data.json"

mkdir -p "$(dirname "$LOG")"

# ── all stdout/stderr from here on gets a timestamp prefix and goes to LOG ──
exec 1> >(while IFS= read -r line; do printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S %z')" "$line"; done >> "$LOG")
exec 2>&1

echo "===== run_momentum5_local.sh start (FORCE=${FORCE:-0}) ====="

cd "$REPO_DIR"

echo "syncing runner clone to origin/main..."
git fetch origin main
git reset --hard origin/main

if [ ! -f "$DATA_JSON" ]; then
  echo "ERROR: $DATA_JSON not found after reset — aborting."
  exit 1
fi

# ── gate: only run on Saturday (unless as_of already today), or if as_of is
#    stale by >= 8 days. FORCE=1 bypasses this entirely. ──
if [ "${FORCE:-0}" != "1" ]; then
  AS_OF=$("$PY" -c "import json; print(json.load(open('$DATA_JSON'))['as_of'])")
  TODAY=$(date '+%Y-%m-%d')
  DOW=$(date '+%u')  # 1=Mon ... 6=Sat, 7=Sun

  AS_OF_EPOCH=$(date -j -f '%Y-%m-%d' "$AS_OF" '+%s')
  TODAY_EPOCH=$(date -j -f '%Y-%m-%d' "$TODAY" '+%s')
  AGE_DAYS=$(( (TODAY_EPOCH - AS_OF_EPOCH) / 86400 ))

  echo "gate check: today=$TODAY dow=$DOW as_of=$AS_OF age_days=$AGE_DAYS"

  SHOULD_RUN=0
  if [ "$DOW" = "6" ] && [ "$AS_OF" != "$TODAY" ]; then
    SHOULD_RUN=1
  fi
  if [ "$AGE_DAYS" -ge 8 ]; then
    SHOULD_RUN=1
  fi

  if [ "$SHOULD_RUN" != "1" ]; then
    echo "fresh, skip"
    exit 0
  fi
else
  echo "FORCE=1 set — bypassing gate"
fi

echo "running build_momentum5.py..."
"$PY" scripts/build_momentum5.py

if git status --porcelain "$DATA_JSON" | grep -q .; then
  echo "data.json changed — committing"
  TODAY=$(date '+%Y-%m-%d')
  git add "$DATA_JSON"
  git commit -m "data: momentum-5 weekly update ${TODAY}（本地跑點）"

  PUSHED=0
  for i in 1 2 3 4 5; do
    if git push origin main; then
      PUSHED=1
      break
    fi
    echo "push attempt $i failed — rebasing onto origin/main and retrying"
    git pull --rebase --autostash origin main
  done

  if [ "$PUSHED" != "1" ]; then
    echo "ERROR: push failed after 5 attempts"
    exit 1
  fi

  echo "push succeeded: $(git rev-parse --short HEAD)"
else
  echo "build produced no change (fail-safe?)"
  exit 1
fi

echo "===== run_momentum5_local.sh done ====="
