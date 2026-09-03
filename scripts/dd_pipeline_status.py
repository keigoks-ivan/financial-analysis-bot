#!/usr/bin/env python3
"""dd_pipeline_status.py — v16 WP3: 一眼看 stock-analyst v16 鏈走到哪一步。

Zero-judgment status board for the v16 evidence->judgment->render chain
(see notes/site-internal/dd/_v16_design_spec_20260903.md §2). For each stage
artifact under .dd_build/{TICKER}_{DATE}.* (and the final assembled
docs/dd/DD_{TICKER}_{DATE}.html), reports exists/missing plus a one-line
summary from that artifact's own validator, run in --report mode. Never
validates anything itself, never raises on a missing artifact — only shells
out to existing validators (validate_evidence.py / validate_judgment.py /
qc.py / verify_dd_math.py / validate_dd_meta.py / dd_sections.py bytes).

Usage:
    python3 scripts/dd_pipeline_status.py TICKER DATE
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE_FILES = ["dashboard", "e2", "e12", "dd-meta", "appA-table"]
PROSE_IDS = [f"s{i}" for i in range(1, 15)] + ["decision", "appA", "revlog"]


def run(cmd):
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=60)
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:  # noqa: BLE001 — status board must never crash
        return 1, f"EXC: {e}"


def summarize(text, n=2):
    lines = [l for l in text.splitlines() if l.strip()]
    return " | ".join(lines[-n:]) if lines else "(no output)"


def check_file(path, label, validator=None):
    if not path.exists():
        return {"artifact": label, "status": "MISSING"}
    if validator is None:
        return {"artifact": label, "status": "present"}
    rc, out = run(validator(path))
    return {"artifact": label, "status": f"{'PASS' if rc == 0 else 'FAIL'} — {summarize(out)}"}


def check_dir(path, expected, label):
    if not path.exists():
        return {"artifact": label, "status": "MISSING"}
    have = {f.stem for f in path.glob("*.html")}
    missing = [e for e in expected if e not in have]
    tail = f", missing: {','.join(missing)}" if missing else " complete"
    return {"artifact": label, "status": f"{len(have)}/{len(expected)}{tail}"}


def decision_out_row(judgment_path):
    label = "Stage1 decision_out（judgment.json 內嵌）"
    if not judgment_path.exists():
        return {"artifact": label, "status": "MISSING（judgment.json 不存在）"}
    try:
        dout = json.loads(judgment_path.read_text()).get("decision_out") or {}
    except Exception as e:  # noqa: BLE001
        return {"artifact": label, "status": f"unreadable: {e}"}
    if not dout.get("verdict"):
        return {"artifact": label, "status": "empty（dd_decision.py run 尚未寫回）"}
    status = (f"verdict={dout.get('verdict')} role={dout.get('role')} "
              f"row_hit={dout.get('row_hit')} requires_critic={dout.get('requires_critic') or []}")
    return {"artifact": label, "status": status}


def docs_rows(ticker, date):
    docs = ROOT / "docs" / "dd" / f"DD_{ticker}_{date}.html"
    if not docs.exists():
        return [{"artifact": "最終組裝 docs/dd/DD_*.html", "status": "MISSING"}]
    checks = [
        ("qc", [sys.executable, "scripts/qc.py", str(docs)]),
        ("verify_math", [sys.executable, "scripts/verify_dd_math.py", str(docs)]),
        ("dd_meta", [sys.executable, "scripts/validate_dd_meta.py", str(docs), "--report"]),
    ]
    tags = [f"{name}={'PASS' if run(cmd)[0] == 0 else 'FAIL'}" for name, cmd in checks]
    _, by_out = run([sys.executable, "scripts/dd_sections.py", "bytes", str(docs)])
    return [
        {"artifact": "最終組裝 docs/dd/DD_*.html", "status": " ".join(tags)},
        {"artifact": "  └ bytes 預算 (dd_sections.py bytes)", "status": summarize(by_out, 3)},
    ]


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/dd_pipeline_status.py TICKER DATE")
        sys.exit(2)
    ticker, date = sys.argv[1].upper(), sys.argv[2]
    prefix = f"{ticker}_{date}"
    build = ROOT / ".dd_build"

    rows = [
        check_file(build / f"{prefix}.evidence.json", "Stage0 evidence.json",
                   validator=lambda p: [sys.executable, "scripts/validate_evidence.py", str(p), "--report"]),
        check_file(build / f"{prefix}.judgment.json", "Stage1 judgment.json",
                   validator=lambda p: [sys.executable, "scripts/validate_judgment.py", str(p), "--report"]),
        check_file(build / f"{prefix}.scenario.json", "Stage1 scenario.json"),
        decision_out_row(build / f"{prefix}.judgment.json"),
        check_dir(build / f"{prefix}.tables", TABLE_FILES, "Stage2 gen_dd_tables 輸出"),
        check_dir(build / f"{prefix}.prose", PROSE_IDS, "Stage2 prose/ 段落"),
    ]
    rows.extend(docs_rows(ticker, date))

    print(f"=== dd_pipeline_status: {ticker} {date} ===")
    width = max(len(r["artifact"]) for r in rows) + 1
    for r in rows:
        mark = "-- " if "MISSING" in str(r["status"]) else "OK "
        print(f"[{mark}] {r['artifact'].ljust(width)} {r['status']}")


if __name__ == "__main__":
    main()
