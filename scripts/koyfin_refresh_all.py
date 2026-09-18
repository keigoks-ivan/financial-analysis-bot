#!/usr/bin/env python3
"""Koyfin monthly refresh orchestrator — one command in place of driving
Chrome by hand through .claude/skills/refresh-eps-screener-web/SKILL.md for
all three watchlists (dd_screener / dd_smallcap / dd_largecap).

Run with python3.12 (this repo's convention for build/test tooling). It never
imports scripts/koyfin_xlsx_from_raw.py directly (that module does
`from openpyxl import Workbook` at import time, and openpyxl is only
installed for python3 in this environment — see facts in the task brief) —
it always shells out to `python3` for that step, exactly mirroring how the
manual skill invokes it (SKILL.md Step 6: "python3 scripts/koyfin_xlsx_from_raw.py").

Pipeline per family (screener / smallcap / largecap, see scripts/koyfin_families.py):
  1. (optional) --scrape: subprocess `python3 scripts/koyfin_scrape.py --all`
  2. locate the raw txt for --date (data/eps-estimates/raw/koyfin_<family>_raw_<date>.txt)
  3. verify its djb2 fingerprint (recompute in this process; cross-check a
     .fingerprint.json sidecar if koyfin_scrape.py wrote one)
  4. Step 5 gate (SKILL.md "分割 / 異常 gate", the one judgment step in the
     skill): flag tickers whose FY1 EPS moved >=35% or flipped sign vs. the
     previous xlsx of the same family. This script only does the MECHANICAL
     screen (candidate list) — the skill's decision tree (stock split vs. bad
     Koyfin data vs. real analyst revision) requires WebSearch + judgment and
     is NOT automated. Any flagged ticker is a hard stop (exit 6): no xlsx is
     built, no downstream command runs, until a human resolves it (see the
     note file this task also produces for the recovery procedure).
  5. build the xlsx via `python3 scripts/koyfin_xlsx_from_raw.py`
Then, once every requested family is done: the four downstream commands in
the order the task brief gives them (note the last one uses `python3`, not
python3.12 — copied verbatim, not a typo):
  python3.12 scripts/build_dd_screener.py --include-non-dd
  python3.12 scripts/build_dd_screener.py --universe smallcap
  python3.12 scripts/build_tenbagger.py
  python3 scripts/engine/build_arena.py
Then a final summary (universe sizes, largecap rows, arena core/waiting/buyable line).

--commit stages the built xlsx + the docs/ outputs the downstream commands
just wrote (never data/eps-estimates/raw/*.txt) with a message listing
universe counts per family; never pushes unless --push is also given.
Default: no commit (report and stop, matching every other skill's git-flow
convention in this repo).

Exit codes: 0 ok; 2 usage error; 3 missing raw file for a requested family;
6 Step-5 anomaly gate tripped (hard stop, see above); nonzero from a failed
subprocess is passed through.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from koyfin_families import FAMILIES, FAMILY_ORDER, raw_txt_name, fingerprint_sidecar_name  # noqa: E402
import load_eps_estimates_xlsx as leex  # noqa: E402  (stdlib-only reader, python3.12-safe)

RAW_DIR = ROOT / "data" / "eps-estimates"
DATA_DIR = ROOT / "data" / "eps-estimates"
DOCS_DIR = ROOT / "docs"

FY1_GATE_PCT = 35.0  # skill Step 5: "|FY1 移動| ≥ 35% 或翻號"


# ---------------------------------------------------------------------------
# Fingerprint (Step 4 recompute — same djb2 algorithm as the skill / koyfin_scraper.js)
# ---------------------------------------------------------------------------

def compute_fingerprint(raw_path: Path) -> dict:
    s = raw_path.read_text(encoding="utf-8").rstrip("\n")
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    rows = len(s.split("\n")) if s else 0
    return {"rows": rows, "bytes": len(s), "djb2": h}


def find_raw_file(data_dir: Path, family_key: str, date_str: str) -> Path:
    p = data_dir / "raw" / raw_txt_name(family_key, date_str)
    if not p.exists():
        raise FileNotFoundError(
            f"missing raw file for family={family_key!r} date={date_str!r}: {p} "
            f"(run with --scrape, or place the raw txt at this path manually — "
            f"see .claude/skills/refresh-eps-screener-web/SKILL.md Step 1-4 for the manual fallback)"
        )
    return p


def verify_fingerprint(raw_path: Path, family_key: str, date_str: str, data_dir: Path) -> dict:
    fp = compute_fingerprint(raw_path)
    sidecar = data_dir / "raw" / fingerprint_sidecar_name(family_key, date_str)
    if sidecar.exists():
        recorded = json.loads(sidecar.read_text(encoding="utf-8"))
        mismatches = {
            k: (recorded.get(k), fp[k]) for k in ("rows", "bytes", "djb2") if recorded.get(k) != fp[k]
        }
        if mismatches:
            raise ValueError(
                f"fingerprint mismatch for {raw_path.name} vs. its sidecar {sidecar.name}: {mismatches} "
                f"— raw file may have been edited since it was scraped. Do not proceed; re-scrape."
            )
        fp["verified_against"] = "sidecar"
    else:
        fp["verified_against"] = "none (no .fingerprint.json — pre-automation/manual raw file; nothing to cross-check)"
    return fp


# ---------------------------------------------------------------------------
# Step 5 gate — mechanical part only (see module docstring)
# ---------------------------------------------------------------------------

def _blank(v: str) -> bool:
    return v.strip() in ("", "-", "—", "N/A")


def parse_fy1_from_raw(raw_path: Path) -> dict:
    """FY1 EPS is raw-txt field index 1 (f[0]=ticker, f[1]="EPS Norm - Est Avg
    (FY1E)") — see scripts/koyfin_xlsx_from_raw.py build_row(). Reimplemented
    here (not imported) because koyfin_xlsx_from_raw.py pulls in openpyxl at
    import time, which python3.12 doesn't have in this environment."""
    out: dict[str, float | None] = {}
    for line in raw_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        f = line.split("|")
        if len(f) < 2:
            continue
        ticker = f[0]
        val = f[1].strip()
        if _blank(val):
            out[ticker] = None
            continue
        try:
            out[ticker] = float(val.replace(",", ""))
        except ValueError:
            out[ticker] = None
    return out


def find_previous_snapshot(data_dir: Path, xlsx_family: str, exclude_date: str) -> Path | None:
    """Latest existing xlsx of this family strictly excluding `exclude_date`
    (the date we're about to build) — find_latest_excel() alone would just
    return today's own file once it exists (e.g. largecap's only snapshot is
    2026-09-18 itself), which would make the gate compare a file against
    itself. Returns None when there is no earlier snapshot (e.g. a family's
    first-ever run — the skill explicitly says Step 5 does not apply then)."""
    pat = re.compile(re.escape(xlsx_family) + r"(\d{8})\.xlsx$")
    candidates = []
    if not data_dir.exists():
        return None
    for p in data_dir.glob(f"{xlsx_family}*.xlsx"):
        m = pat.search(p.name)
        if m and m.group(1) != exclude_date:
            candidates.append((m.group(1), p))
    if not candidates:
        return None
    candidates.sort(key=lambda t: t[0], reverse=True)
    return candidates[0][1]


def run_anomaly_gate(new_fy1: dict, prev_snapshot) -> dict:
    """Mechanical screen only: |FY1 change%| >= 35% or sign flip vs. the
    previous snapshot of the same family. `prev_snapshot` is an
    load_eps_estimates_xlsx.ExcelSnapshot (or None when there is no prior
    snapshot — see find_previous_snapshot()). The judgment step (split vs.
    bad data vs. real revision — SKILL.md Step 5's decision tree) is NOT
    automated; a non-empty "flagged" list means the caller must stop and a
    human must walk that decision tree before anything downstream runs."""
    if prev_snapshot is None:
        return {"flagged": [], "checked": 0, "skipped_no_prev": True}
    flagged = []
    checked = 0
    for ticker, new_v in new_fy1.items():
        if new_v is None:
            continue
        prev_rec = prev_snapshot.get(ticker)
        if not prev_rec:
            continue
        prev_v = prev_rec.get("fy1")
        if prev_v is None:
            continue
        checked += 1
        sign_flip = (prev_v > 0 and new_v < 0) or (prev_v < 0 and new_v > 0)
        pct_move = None if prev_v == 0 else abs(new_v - prev_v) / abs(prev_v) * 100
        if sign_flip or (pct_move is not None and pct_move >= FY1_GATE_PCT):
            flagged.append(
                {
                    "ticker": ticker,
                    "prev_fy1": prev_v,
                    "new_fy1": new_v,
                    "pct_move": pct_move,
                    "sign_flip": sign_flip,
                }
            )
    flagged.sort(key=lambda r: r["ticker"])
    return {"flagged": flagged, "checked": checked, "skipped_no_prev": False}


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------

def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True, **kw)


def build_xlsx(family_key: str, raw_path: Path, out_path: Path, snapshot_date: str) -> tuple[int, int]:
    """Returns (returncode, rows_built)."""
    fam = FAMILIES[family_key]
    cmd = [
        "python3", str(SCRIPTS_DIR / "koyfin_xlsx_from_raw.py"),
        "--raw", str(raw_path),
        "--out", str(out_path),
        "--snapshot-date", snapshot_date,
    ]
    if fam["universe_note"]:
        cmd += ["--universe-note", fam["universe_note"]]
    proc = run(cmd)
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode, 0
    m = re.search(r"rows (\d+) cols", proc.stdout)
    return 0, (int(m.group(1)) if m else 0)


DOWNSTREAM_CMDS = [
    ["{PY312}", "scripts/build_dd_screener.py", "--include-non-dd"],
    ["{PY312}", "scripts/build_dd_screener.py", "--universe", "smallcap"],
    ["{PY312}", "scripts/build_tenbagger.py"],
    ["python3", "scripts/engine/build_arena.py"],
]


def run_downstream() -> tuple[bool, str]:
    """Runs the four downstream commands in order. Stops at the first
    failure. Returns (all_ok, arena_summary_line)."""
    arena_line = ""
    for tpl in DOWNSTREAM_CMDS:
        cmd = [sys.executable if c == "{PY312}" else c for c in tpl]
        cmd = [str(ROOT / c) if c.startswith("scripts/") else c for c in cmd]
        proc = run(cmd)
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        if proc.returncode != 0:
            print(f"downstream command failed (exit {proc.returncode}): {cmd}", file=sys.stderr)
            return False, arena_line
        if "build_arena.py" in cmd[-1]:
            for line in proc.stdout.splitlines():
                if line.startswith("arena:"):
                    arena_line = line
    return True, arena_line


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_family(family_key: str, date_str: str, dry_run: bool, scratch_dir: Path | None) -> tuple[int, dict]:
    fam = FAMILIES[family_key]
    snapshot_date = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"

    raw_path = find_raw_file(DATA_DIR, family_key, date_str)
    fp = verify_fingerprint(raw_path, family_key, date_str, DATA_DIR)
    print(f"[{family_key}] fingerprint OK: rows={fp['rows']} bytes={fp['bytes']} djb2={fp['djb2']} "
          f"(verified_against={fp['verified_against']})")

    new_fy1 = parse_fy1_from_raw(raw_path)
    prev_path = find_previous_snapshot(DATA_DIR, fam["xlsx_family"], date_str)
    prev_snapshot = leex.load_excel(prev_path) if prev_path else None
    gate = run_anomaly_gate(new_fy1, prev_snapshot)

    if gate["skipped_no_prev"]:
        print(f"[{family_key}] Step 5 gate: no previous {fam['xlsx_family']}*.xlsx snapshot to compare "
              f"against — gate not applicable (first run for this family), per skill.")
    else:
        print(f"[{family_key}] Step 5 gate: checked {gate['checked']} tickers vs. {prev_path.name}, "
              f"{len(gate['flagged'])} flagged (|FY1 move| >= {FY1_GATE_PCT}% or sign flip).")

    if gate["flagged"]:
        print(f"\n[{family_key}] STOP — Step 5 anomaly gate tripped. Mechanical screen only; a human must "
              f"walk the skill's decision tree (stock split vs. bad Koyfin data vs. real analyst revision — "
              f"SKILL.md Step 5) for each ticker below before any xlsx is built or any downstream command runs.\n")
        for r in gate["flagged"]:
            move = f"{r['pct_move']:.1f}%" if r["pct_move"] is not None else "n/a"
            print(f"    {r['ticker']}: prev_fy1={r['prev_fy1']} new_fy1={r['new_fy1']} "
                  f"move={move} sign_flip={r['sign_flip']}")
        return 6, {"family": family_key, "gate": gate}

    out_dir = scratch_dir if dry_run and scratch_dir else DATA_DIR
    out_path = out_dir / f"{fam['xlsx_family']}{date_str}.xlsx"
    rc, rows = build_xlsx(family_key, raw_path, out_path, snapshot_date)
    if rc != 0:
        return rc, {"family": family_key}

    return 0, {"family": family_key, "rows": rows, "xlsx": out_path, "fingerprint": fp, "gate": gate}


def git_commit(built: list[dict], push: bool) -> int:
    xlsx_paths = [str(b["xlsx"].relative_to(ROOT)) for b in built if "xlsx" in b]
    doc_paths = [
        "docs/dd-screener/latest.json", "docs/dd-screener/index.html",
        "docs/dd-screener/smallcap/latest.json",
        "docs/engine/arena.json", "docs/engine/board.txt", "docs/engine/_arena_body.html",
    ]
    doc_paths = [p for p in doc_paths if (ROOT / p).exists()]
    add_paths = xlsx_paths + doc_paths
    if not add_paths:
        print("[commit] nothing to add (dry-run or no families built) — skipping.")
        return 0

    counts = ", ".join(f"{b['family']}={b.get('rows', '?')}" for b in built if "rows" in b)
    msg = f"koyfin refresh {datetime.now().strftime('%Y-%m-%d')}: {counts}"

    proc = run(["git", "add"] + add_paths)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode
    proc = run(["git", "commit", "-m", msg])
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return proc.returncode
    if push:
        proc = run(["git", "pull", "--rebase"])
        print(proc.stdout)
        if proc.returncode != 0:
            print(proc.stderr, file=sys.stderr)
            return proc.returncode
        proc = run(["git", "push", "origin", "main"])
        print(proc.stdout)
        if proc.returncode != 0:
            print(proc.stderr, file=sys.stderr)
            return proc.returncode
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    scrape_group = ap.add_mutually_exclusive_group(required=True)
    scrape_group.add_argument("--scrape", action="store_true",
                               help="Run koyfin_scrape.py --all via python3 first.")
    scrape_group.add_argument("--no-scrape", action="store_true",
                               help="Use raw files already in data/eps-estimates/raw/ for --date.")
    ap.add_argument("--date", default=None,
                     help="YYYYMMDD. Required with --no-scrape; defaults to today with --scrape.")
    ap.add_argument("--only", choices=FAMILY_ORDER, default=None,
                     help="Restrict to a single family (testing).")
    ap.add_argument("--dry-run", action="store_true",
                     help="Build xlsx to --scratch-dir instead of data/eps-estimates/, skip downstream builds and commit.")
    ap.add_argument("--scratch-dir", type=Path, default=None,
                     help="Output dir for --dry-run xlsx (default: a tempfile.mkdtemp()).")
    ap.add_argument("--commit", action="store_true", help="Commit built xlsx + docs outputs. Default: no commit.")
    ap.add_argument("--push", action="store_true", help="Also push (requires --commit).")
    args = ap.parse_args()

    if args.no_scrape and not args.date:
        ap.error("--no-scrape requires --date YYYYMMDD")
    if args.push and not args.commit:
        ap.error("--push requires --commit")

    date_str = args.date or datetime.now().strftime("%Y%m%d")

    if args.scrape:
        cmd = ["python3", str(SCRIPTS_DIR / "koyfin_scrape.py"), "--all"]
        proc = subprocess.run(cmd, cwd=str(ROOT))
        if proc.returncode != 0:
            print(f"koyfin_scrape.py --all failed (exit {proc.returncode})", file=sys.stderr)
            return proc.returncode

    families = [args.only] if args.only else FAMILY_ORDER

    scratch_dir = args.scratch_dir
    if args.dry_run and scratch_dir is None:
        import tempfile
        scratch_dir = Path(tempfile.mkdtemp(prefix="koyfin_refresh_dryrun_"))
    if scratch_dir:
        scratch_dir.mkdir(parents=True, exist_ok=True)

    built = []
    for family_key in families:
        rc, info = process_family(family_key, date_str, args.dry_run, scratch_dir)
        if rc != 0:
            return rc
        built.append(info)

    if args.dry_run:
        print(f"\n[dry-run] built {len(built)} xlsx under {scratch_dir}, skipping downstream builds and commit.")
        for b in built:
            print(f"  {b['family']}: rows={b.get('rows')} -> {b.get('xlsx')}")
        return 0

    ok, arena_line = run_downstream()
    if not ok:
        return 1

    print("\n=== summary ===")
    for b in built:
        print(f"  {b['family']}: {b.get('rows')} rows scraped -> {b.get('xlsx')}")
    latest = DOCS_DIR / "dd-screener" / "latest.json"
    if latest.exists():
        d = json.loads(latest.read_text(encoding="utf-8"))
        print(f"  dd-screener universe_size: {d.get('universe_size')}")
    smallcap_latest = DOCS_DIR / "dd-screener" / "smallcap" / "latest.json"
    if smallcap_latest.exists():
        d = json.loads(smallcap_latest.read_text(encoding="utf-8"))
        print(f"  dd-screener smallcap universe_size: {d.get('universe_size')}")
    if arena_line:
        print(f"  {arena_line}")

    if args.commit:
        return git_commit(built, args.push)

    print("\n(no --commit given — nothing staged, matching every other skill's default-stop-for-review git flow)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
