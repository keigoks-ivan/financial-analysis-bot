#!/bin/sh
# Install local git hooks for this repo by pointing core.hooksPath at scripts/hooks/.
# Run once after clone (or after pulling new hooks): bash scripts/install_hooks.sh
#
# Why this exists: .git/hooks/ is not tracked, so hooks don't follow the repo
# across machines. Tracking them in scripts/hooks/ + setting core.hooksPath
# means any clone gets the same enforcement once this script runs.
#
# To uninstall: git config --unset core.hooksPath
# To bypass once: git commit --no-verify

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

if [ ! -d scripts/hooks ]; then
  echo "❌ scripts/hooks/ not found. Run from repo root or ensure repo is up to date."
  exit 1
fi

# Ensure all hook scripts are executable
chmod +x scripts/hooks/* 2>/dev/null || true

# Point git at our tracked hooks directory
git config core.hooksPath scripts/hooks

echo "✅ Git hooks installed (core.hooksPath = scripts/hooks)"
echo ""
echo "Active hooks:"
ls scripts/hooks/ | sed 's/^/  /'
echo ""
echo "Test it: stage a broken ID file and try to commit — should be blocked."
echo "Bypass once: git commit --no-verify"
echo "Uninstall: git config --unset core.hooksPath"
