#!/usr/bin/env bash
# scripts/koyfin_refresh_worktree.sh — unattended-run wrapper for
# scripts/koyfin_refresh_all.py. Introduced 2026-09-23 because the shared
# working copy (~/financial-analysis-bot) routinely has other Claude
# sessions' uncommitted work sitting in it; running the monthly refresh
# there and letting git_commit() autostash around that was unsafe (autostash
# can mangle someone else's uncommitted work, a plain `git commit` in that
# directory can sweep in whatever another session had staged, and the shared
# copy may not even be on main at the time). See
# notes/site-internal/root/_koyfin_refresh_automation_20260918.md for the
# full writeup.
#
# What this does: fetches origin/main, resets a dedicated git worktree
# (outside the shared copy) to a clean detached HEAD at origin/main, runs
# koyfin_refresh_all.py entirely inside that worktree (scrape/build/commit/
# push all happen there — the shared copy is never touched), then copies the
# freshly scraped raw txt + fingerprint sidecars back into the shared copy's
# data/eps-estimates/raw/ so the owner can still find them in the familiar
# place (that directory is intentionally untracked by git either way — see
# koyfin_refresh_all.py's module docstring — so this is a plain file copy,
# not a git operation).
#
# launchd (com.investmquest.koyfin-refresh) invokes this script instead of
# calling koyfin_refresh_all.py directly. Manual/interactive runs should
# keep using koyfin_refresh_all.py directly from the shared copy, as before
# — this wrapper is only for the unattended path.
#
# Usage: koyfin_refresh_worktree.sh [args passed through to koyfin_refresh_all.py]
#   e.g. koyfin_refresh_worktree.sh --scrape --commit --push   (the launchd case)
#        koyfin_refresh_worktree.sh --no-scrape --date 20260919 --dry-run   (manual test)

set -euo pipefail

SHARED_REPO="${KOYFIN_SHARED_REPO:-$HOME/financial-analysis-bot}"
WORKTREE="${KOYFIN_WORKTREE:-$HOME/.koyfin-refresh-worktree}"
PY312="${KOYFIN_PY312:-/opt/homebrew/bin/python3.12}"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

if [ ! -d "$SHARED_REPO/.git" ]; then
  echo "ERROR: $SHARED_REPO is not a git repo (expected the shared financial-analysis-bot checkout)" >&2
  exit 1
fi

log "fetching origin/main into shared repo ($SHARED_REPO) — read-only, does not touch its working tree"
git -C "$SHARED_REPO" fetch origin main

if git -C "$SHARED_REPO" worktree list --porcelain | grep -qxF "worktree $WORKTREE"; then
  log "resetting existing worktree $WORKTREE to freshly fetched origin/main (clean, detached)"
  git -C "$WORKTREE" fetch origin main
  git -C "$WORKTREE" checkout --force --detach origin/main
  git -C "$WORKTREE" clean -fdx
else
  if [ -e "$WORKTREE" ]; then
    echo "ERROR: $WORKTREE exists but is not a registered git worktree of $SHARED_REPO — refusing to" >&2
    echo "       touch it automatically. Remove it (or 'git -C $SHARED_REPO worktree prune') and rerun." >&2
    exit 1
  fi
  log "creating dedicated worktree $WORKTREE (detached HEAD at origin/main)"
  git -C "$SHARED_REPO" worktree add --detach "$WORKTREE" origin/main
fi

log "running koyfin_refresh_all.py inside $WORKTREE (args: $*)"
set +e
(cd "$WORKTREE" && "$PY312" "$WORKTREE/scripts/koyfin_refresh_all.py" "$@")
RC=$?
set -e

log "copying any scraped raw txt / fingerprint sidecars back to $SHARED_REPO/data/eps-estimates/raw/ (reference copy; neither copy is git-tracked)"
mkdir -p "$SHARED_REPO/data/eps-estimates/raw"
if compgen -G "$WORKTREE/data/eps-estimates/raw/*" > /dev/null; then
  cp -p "$WORKTREE"/data/eps-estimates/raw/* "$SHARED_REPO/data/eps-estimates/raw/"
fi

log "done, exit=$RC"
exit "$RC"
