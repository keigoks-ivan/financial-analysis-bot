#!/bin/bash
# Publish new DD reports: update research page index + commit + push
cd "$(dirname "$0")/.."
python3 scripts/update_dd_index.py
git add docs/dd/ docs/research/index.html
git diff --staged --quiet && echo "No changes to publish." && exit 0
git commit -m "Add/update DD reports: $(date -u '+%Y-%m-%d')"
git push origin main
