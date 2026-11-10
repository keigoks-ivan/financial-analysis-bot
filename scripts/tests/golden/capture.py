#!/usr/bin/env python3
"""黃金重播：抓價格快照。在受測 repo（預設＝本檔所在 repo）的程式上把每個場景跑一次，
所有網路邊界的回傳值（yfinance.download／yfinance.Ticker.history／證交所 requests.get）存進快照，只抓一次。

同時存：當下的 docs 輸入檔（state.json、w52／cap15 state、記分板 JSON 等）、生效日邊界那幾輪 CI 提交的
state.json 與它前一版（git show），以及 record 模式跑出的結果 results/record.json。

用法（venv：~/.venvs/v7bt/bin/python）：
  capture.py [--src <repo>] [--out <快照目錄>] [--now 2026-11-10T09:00:00+00:00]
             [--boundary-dates 2026-11-03,2026-11-04,...] [--no-boundary]
快照預設放 /Volumes/X10 Data/fab_golden/<台北日期>/（已存在就加時分秒），不放 repo、不提交。
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _golden as G  # noqa: E402
import replay as R  # noqa: E402

# 生效日邊界：11-04（Supertrend＋美股 70／30）、11-06（下軌接回）、11-10（台股正二）前後各一個交易日
DEFAULT_BOUNDARY = "2026-11-03,2026-11-04,2026-11-05,2026-11-06,2026-11-09,2026-11-10"
SETTLE = {"us": ("America/New_York", (16, 30)), "tw": ("Asia/Taipei", (14, 15))}


def git(repo: Path, *a) -> str:
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout


def find_boundary(repo: Path, dates: list[str]) -> list[dict]:
    """每個 (日期, 市場)：第一個「該市場最後一筆 history＝該日、且產生時間已過該市場定案時間」的 state.json 提交。"""
    since = (datetime.fromisoformat(min(dates)) - timedelta(days=10)).strftime("%Y-%m-%d")
    shas = git(repo, "log", "--reverse", f"--since={since}", "--format=%H", "--", G.STATE_REL).split()
    rows, prev = [], None
    for sha in shas:
        try:
            s = json.loads(git(repo, "show", f"{sha}:{G.STATE_REL}"))
        except Exception:  # noqa: BLE001
            prev = sha
            continue
        rows.append({"sha": sha, "prev": prev, "gen": s.get("generated_at"),
                     "us": (s.get("history_us") or [{}])[-1].get("date"),
                     "tw": (s.get("history_tw") or [{}])[-1].get("date")})
        prev = sha
    picked = {}
    for d in dates:
        for mk in ("us", "tw"):
            tz, (hh, mm) = SETTLE[mk]
            settle = datetime.fromisoformat(d).replace(hour=hh, minute=mm, tzinfo=ZoneInfo(tz))
            for r in rows:
                if r["prev"] and r[mk] == d and r["gen"] and \
                        datetime.fromisoformat(r["gen"].replace("Z", "+00:00")) >= settle:
                    picked.setdefault(r["sha"], {**r, "covers": []})["covers"].append(f"{mk} {d}")
                    break
    return sorted(picked.values(), key=lambda r: r["gen"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(G.REPO))
    ap.add_argument("--out")
    ap.add_argument("--now")
    ap.add_argument("--boundary-dates", default=DEFAULT_BOUNDARY)
    ap.add_argument("--no-boundary", action="store_true")
    ap.add_argument("--reuse-store", action="store_true", help="--out 已有快照時沿用其 store/（只補抓缺的），重寫 meta 與結果")
    args = ap.parse_args()

    src = Path(args.src).resolve()
    now = datetime.fromisoformat(args.now) if args.now else datetime.now(timezone.utc).replace(microsecond=0)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    now = now.astimezone(timezone.utc)
    now_iso = now.isoformat()
    out = Path(args.out) if args.out else G.GOLDEN_ROOT / now.astimezone(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d")
    if (out / "meta.json").exists() and not args.out:
        out = out.with_name(out.name + now.astimezone(ZoneInfo("Asia/Taipei")).strftime("_%H%M%S"))
    if (out / "meta.json").exists() and not args.reuse_store:
        sys.exit(f"{out} 已有快照，換一個 --out（或加 --reuse-store）")
    out.mkdir(parents=True, exist_ok=True)
    commit = git(src, "rev-parse", "HEAD").strip()
    dirty = [ln for ln in git(src, "status", "--porcelain", "--", "scripts", "docs/long-track-w52-adaptive").splitlines()
             if "scripts/tests/golden/" not in ln]
    print(f"[capture] 受測 {src} @ {commit[:10]}{'（有未提交改動：' + str(dirty[:5]) + '）' if dirty else ''}；凍結時間 {now_iso}")

    inputs = {}
    for rel in G.DOCS_INPUTS:
        p = src / rel
        if not p.exists():
            print(f"  （略過，不存在）{rel}")
            continue
        dst = out / "docs_inputs" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dst)
        inputs[rel] = str(Path("docs_inputs") / rel)

    scen = [{"name": "table", "kind": "table", "now": now_iso},
            {"name": "live", "kind": "main", "profile": "live", "now": now_iso},
            {"name": "w52", "kind": "main", "profile": "w52", "now": now_iso},
            {"name": "cap15", "kind": "main", "profile": "cap15", "now": now_iso},
            {"name": "scoreboard", "kind": "scoreboard", "now": now_iso},
            {"name": "console", "kind": "console", "now": now_iso}]
    boundary = []
    if not args.no_boundary:
        boundary = find_boundary(src, [d.strip() for d in args.boundary_dates.split(",") if d.strip()])
        for b in boundary:
            bd = out / "boundary" / b["sha"][:12]
            bd.mkdir(parents=True, exist_ok=True)
            (bd / "state.json").write_text(git(src, "show", f"{b['sha']}:{G.STATE_REL}"))
            (bd / "prev_state.json").write_text(git(src, "show", f"{b['prev']}:{G.STATE_REL}"))
            (bd / "info.json").write_text(json.dumps(b, ensure_ascii=False, indent=1))
            gen = datetime.fromisoformat(b["gen"].replace("Z", "+00:00")).isoformat()
            scen.append({"name": f"bnd_{b['sha'][:10]}", "kind": "main", "profile": "live", "now": gen,
                         "commit": b["sha"], "covers": b["covers"],
                         "inputs": {G.STATE_REL: str(Path("boundary") / b["sha"][:12] / "prev_state.json")}})
            print(f"  邊界 {b['sha'][:10]} {b['gen']} 涵蓋 {', '.join(b['covers'])}（前一版 {b['prev'][:10]}）")

    meta = {"now": now_iso, "source_repo": str(src), "source_commit": commit, "source_dirty": dirty,
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "inputs": inputs, "scenarios": scen}
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    R.run(out, src / "scripts", {"kind": "dir", "path": str(src), "commit": commit, "dirty_scripts": dirty},
          out / "results" / "record.json", {}, record=True)
    print(f"[capture] 快照：{out}")


if __name__ == "__main__":
    main()
