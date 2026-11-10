#!/usr/bin/env python3
"""黃金重播：讀價格快照，在拋棄式副本上跑受測程式的每個場景，寫出一份結果 JSON（給 compare.py 比）。

用法（venv：~/.venvs/v7bt/bin/python）：
  replay.py --snapshot <快照目錄> --src <repo 或含 scripts/ 的目錄> [--out <結果.json>]
  replay.py --snapshot <快照目錄> --commit <sha> [--repo <repo>]       # 用 git archive 取該 commit 的 scripts/
選項：--env K=V（可重複；例：W52_TW_L2_CUTOVER_DATE=2026-11-13）、--only 場景名（可重複）、--jobs N、--keep（留工作目錄）。
受測 repo 本身不會被寫：每個場景把 scripts/ 複製到工作目錄、docs/ 只放快照輸入檔，主程式寫的檔都落在副本裡。
子行程的環境變數從零組起（不帶任何通知用的金鑰），TZ=UTC、PYTHONHASHSEED=0。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _golden as G  # noqa: E402

BASE_ENV_KEYS = ("HOME", "TMPDIR", "USER", "LOGNAME")


def worker_env(overrides: dict) -> dict:
    env = {k: os.environ[k] for k in BASE_ENV_KEYS if k in os.environ}
    env.update({"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8",
                "TZ": "UTC", "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"})
    env.update(overrides)
    return env


def resolve_scripts(args, work: Path) -> tuple[Path, dict]:
    """回傳 (受測 scripts 目錄, 來源描述)。"""
    if args.commit:
        repo = Path(args.repo or G.REPO)
        sha = subprocess.run(["git", "-C", str(repo), "rev-parse", args.commit], capture_output=True, text=True,
                             check=True).stdout.strip()
        dst = work / "_src"
        dst.mkdir(parents=True)
        arc = subprocess.run(["git", "-C", str(repo), "archive", sha, "scripts"], capture_output=True, check=True)
        subprocess.run(["tar", "-x", "-C", str(dst)], input=arc.stdout, check=True)
        if subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{sha}:{G.RULES_REL}"],
                          capture_output=True).returncode == 0:      # P1 起的 commit 才有規則正本
            arc = subprocess.run(["git", "-C", str(repo), "archive", sha, G.RULES_REL], capture_output=True, check=True)
            subprocess.run(["tar", "-x", "-C", str(dst)], input=arc.stdout, check=True)
        return dst / "scripts", {"kind": "commit", "repo": str(repo), "commit": sha}
    src = Path(args.src).resolve()
    scripts = src / "scripts" if (src / "scripts").is_dir() else src
    desc = {"kind": "dir", "path": str(src)}
    r = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True)
    if r.returncode == 0:
        desc["commit"] = r.stdout.strip()
        st = subprocess.run(["git", "-C", str(src), "status", "--porcelain", "--", "scripts", G.RULES_REL],
                            capture_output=True, text=True)
        desc["dirty_scripts"] = [ln for ln in st.stdout.splitlines() if "scripts/tests/golden/" not in ln]
    return scripts, desc


def run(snapshot: Path, scripts: Path, src_desc: dict, out: Path, env_over: dict, only=None, jobs=4,
        record=False, keep=False) -> dict:
    meta = json.loads((snapshot / "meta.json").read_text())
    scens = [s for s in meta["scenarios"] if not only or s["name"] in only]
    work = G.GOLDEN_ROOT / "_work" / f"{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"
    work.mkdir(parents=True, exist_ok=True)
    base_inputs = {rel: snapshot / p for rel, p in meta["inputs"].items()}
    env = worker_env(env_over)
    mode = "record" if record else "offline"

    def one(s):
        root = work / s["name"]
        inputs = dict(base_inputs)
        inputs.update({rel: snapshot / p for rel, p in (s.get("inputs") or {}).items()})
        G.prepare_root(scripts, root, inputs)
        spec = {"root": str(root), "scenario": s, "store": str(snapshot / "store"), "mode": mode,
                "out": str(root / "_result.json")}
        (root / "_spec.json").write_text(json.dumps(spec, ensure_ascii=False))
        t0 = time.time()
        p = subprocess.run([G.PY, str(G.HERE / "_golden.py"), "worker", str(root / "_spec.json")],
                           env=env, cwd=str(root), capture_output=True, text=True)
        rp = root / "_result.json"
        if rp.exists():
            res = json.loads(rp.read_text())
        else:
            res = {"kind": s["kind"], "now": s["now"], "outputs": {"error": f"worker 沒有產出結果（exit {p.returncode}）",
                                                                   "asof": s["now"][:10]},
                   "written": [], "misses": [], "log_tail": (p.stdout + p.stderr).splitlines()[-40:]}
        res["wall_s"] = round(time.time() - t0, 1)
        o = res.get("outputs") or {}
        print(f"  {s['name']:<22} {res['wall_s']:>6.1f}s  error={'有' if o.get('error') else '無'}  "
              f"misses={len(res.get('misses') or [])}  fetched={len(res.get('fetched') or [])}  "
              f"written={len(res.get('written') or [])}", flush=True)
        return s["name"], res

    t0 = time.time()
    print(f"[replay] {mode}：{len(scens)} 個場景，受測 {src_desc}，env 覆寫 {env_over or '無'}", flush=True)
    if record or jobs <= 1:
        results = dict(one(s) for s in scens)
    else:
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            results = dict(ex.map(one, scens))
    total = round(time.time() - t0, 1)
    import pandas as pd
    import numpy as np
    result = {"meta": {"snapshot": str(snapshot), "snapshot_now": meta["now"], "source": src_desc, "mode": mode,
                       "env_overrides": env_over, "python": sys.version.split()[0], "pandas": pd.__version__,
                       "numpy": np.__version__, "wall_s": total,
                       "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
              "scenarios": {k: results[k] for k in sorted(results)}}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, allow_nan=False))
    print(f"[replay] 完成 {total}s → {out}", flush=True)
    for k, r in result["scenarios"].items():
        o = r.get("outputs") or {}
        if o.get("error"):
            print(f"  ! {k} error: {str(o['error']).splitlines()[0]}")
        if r.get("misses"):
            print(f"  ! {k} 快照缺 {len(r['misses'])} 筆，例：{r['misses'][0]}")
        if r.get("reads_outside"):
            print(f"  ! {k} 讀了副本外的檔：{r['reads_outside'][:5]}")
        if o.get("path_inconsistent"):
            print(f"  ! {k} 實單路徑與向量化路徑不一致 {len(o['path_inconsistent'])} 格，例：{o['path_inconsistent'][:3]}")
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    else:
        print(f"[replay] 工作目錄保留：{work}")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--snapshot", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--src")
    g.add_argument("--commit")
    ap.add_argument("--repo")
    ap.add_argument("--out")
    ap.add_argument("--env", action="append", default=[])
    ap.add_argument("--only", action="append")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()
    snapshot = Path(args.snapshot)
    env_over = dict(e.split("=", 1) for e in args.env)
    work = G.GOLDEN_ROOT / "_work" / f"src-{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"
    work.mkdir(parents=True, exist_ok=True)
    try:
        scripts, desc = resolve_scripts(args, work)
        label = (desc.get("commit") or "src")[:10]
        out = Path(args.out) if args.out else snapshot / "results" / f"replay_{label}_{time.strftime('%H%M%S')}.json"
        run(snapshot, scripts, desc, out, env_over, only=args.only, jobs=args.jobs, keep=args.keep)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
