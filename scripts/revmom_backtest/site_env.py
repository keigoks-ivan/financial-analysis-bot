"""What differs between running in v7-backtest (local) and in the financial-analysis-bot copy (GitHub Actions).

The cloud copy lives at financial-analysis-bot/scripts/revmom_backtest/ (sync steps in that folder's README.md),
so ROOT is the site repo there: data/, results/ and docs/ resolve inside it. Locally ROOT is v7-backtest and pages go to the sibling
financial-analysis-bot checkout (override with REVMOM_SITE_ROOT).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CLOUD = (ROOT / "docs" / "backtest").is_dir()          # running inside the site repo
SITE = Path(os.environ.get("REVMOM_SITE_ROOT", str(ROOT if CLOUD else Path.home() / "financial-analysis-bot")))
LEDGER_SNAPSHOT = ROOT / "data" / "revmom" / "ledger_revmom.json"


def full_nav_block(group=None, item=None):
    try:
        sys.path.insert(0, str(ROOT))
        from site_nav_snippet import full_nav_block as f        # v7-backtest root (synced copy of the canonical nav)
    except ImportError:
        sys.path.insert(0, str(SITE / "scripts"))
        from site_nav import full_nav_block as f                # the canonical nav in the site repo
    return f(group, item)


def make_toggle(key):
    sys.path.insert(0, str(SITE / "docs" / "backtest"))
    from _nav_common import make_toggle as f
    return f(key)


def site_kit():
    sys.path.insert(0, str(ROOT / "src"))                       # v7-backtest/src/site_kit.py
    sys.path.insert(0, str(HERE))                               # cloud: copied next to this file
    import site_kit
    return site_kit


def ledger(family="REVMOM"):
    """(family_report, {exp_id: trial}). Locally read the experiment ledger and refresh the snapshot the cloud uses;
    in the cloud read that snapshot (the ledger is append-only and only written locally)."""
    try:
        sys.path.insert(0, str(ROOT))
        from src.experiment_ledger import _read, family_report
        rep = family_report(family)
        trials = {r["exp_id"]: r for r in _read() if r.get("family") == family and r.get("kind") == "trial"}
        LEDGER_SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_SNAPSHOT.write_text(json.dumps({"report": rep, "trials": trials}, ensure_ascii=False, indent=1))
    except ImportError:
        snap = json.loads(LEDGER_SNAPSHOT.read_text())
        rep, trials = snap["report"], snap["trials"]
    return rep, trials
