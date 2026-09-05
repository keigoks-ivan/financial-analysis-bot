#!/usr/bin/env python3
"""scripts/ddreport.py — v17 WP1a：per-run 目錄、manifest、`plan`、`status`。

只動 `.dd_build/runs/{TICKER}_{DATE}/` 這個新的 per-run 慣例，不改任何既有腳本的
行為或路徑。`plan` 呼叫既有零 LLM 工具（`dd_prior.py`／`dd_evidence.py`／
`dd_numbers_extra.py`，皆原樣呼叫、不改語意）取得證據骨架與軸清單，再依軸分批寫出
子 agent 派工用的 prompt 檔＋`spawn_list.json`。`status` 印 manifest 與各產物存在／
大小，供人工或 orchestrator 檢視進度。

3.9 相容（`from __future__ import annotations`，不用 3.10+ 語法）。

用法：
    python3 scripts/ddreport.py plan TICKER [--date YYYYMMDD] [--archetype X]
        [--peers a,b] [--segments a,b] [--axes-per-batch 2] [--offline]
    python3 scripts/ddreport.py status TICKER DATE

見 notes/site-internal/dd/_wp_spec_v17_20260905.md「共同約定」與「WP1a」段。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
BUILD_DIR = REPO_ROOT / ".dd_build"
RUNS_DIR = BUILD_DIR / "runs"
PROMPTS_TMPL_DIR = SCRIPTS_DIR / "dd_prompts"

# 最後手段的預設 archetype：coverage-axes.md 裡 by_archetype 附加軸數為 0 的
# 那一類（即「只查 common 軸」的基準情境），在 --archetype 未給、且前份 DD
# 是不含 archetype 欄位的 legacy schema（v14.x 以前）時使用。此為刻意的工程
# 折衷，非隨意猜測——見 notes/site-internal/dd/_wp_spec_v17_20260905.md 驗收
# 段對此邊界案例（CRDO 20260904，prior 為 v14.2、無 archetype 欄）的討論。
DEFAULT_ARCHETYPE = "品質複利成長"

AXES_PER_BATCH_DEFAULT = 2

SPAWN_TOOLS_COVERAGE = ["WebSearch", "WebFetch", "Read", "Write", "Bash"]
SPAWN_TOOLS_NUMBERS = ["WebSearch", "WebFetch", "Read", "Write", "Bash"]
SPAWN_TOOLS_DIGEST = ["Read", "Write", "Bash"]
SPAWN_TOOLS_KOYFIN = ["Bash", "Read", "Write"]

BUDGET_CACHE_READ_DEFAULT = 700000


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def _pick_python():
    """優先 /tmp/ddvenv/bin/python（若存在且 import yfinance 成功），否則 python3。"""
    venv_py = Path("/tmp/ddvenv/bin/python")
    if venv_py.exists():
        try:
            r = subprocess.run(
                [str(venv_py), "-c", "import yfinance"],
                capture_output=True, timeout=15,
            )
            if r.returncode == 0:
                return str(venv_py)
        except Exception:
            pass
    return "python3"


def _run_dir(ticker, date):
    return RUNS_DIR / "{0}_{1}".format(ticker, date)


def _atomic_write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _render_template(tmpl_path, mapping):
    text = Path(tmpl_path).read_text(encoding="utf-8")
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def _axis_block(axes):
    lines = []
    for a in axes:
        lines.append("[{0}] {1}".format(a.get("id"), a.get("name", "")))
        lines.append("Q: {0}".format(a.get("question", "")))
        for q in a.get("queries", []) or []:
            lines.append("  - {0}".format(q))
        if a.get("na_allowed"):
            lines.append("  (na_allowed=true)")
        lines.append("")
    text = "\n".join(lines).rstrip()
    return text + "\n" if text else ""


EVENTS_ADDENDUM = """## major_events 軸另交頂層 events 五組（QC-19）
`validate_evidence.py` 的 strict 檢查讀的是 evidence.json **頂層** `events` 物件，
不是 `coverage.major_events`——這兩個是分開的鍵，只填前者會漏掉後者。

你除了（a）對 `major_events` 這一軸本身作答（寫進 `coverage.major_events`），
**還要**（b）把同一批查證結果拆成下列五組，寫進回傳 JSON 的**頂層** `events` 鍵：
`ma_merger`（併購）／`lawsuit_class_action`（訴訟／集體訴訟）／`clinical_fda`
（臨床／FDA，非藥品器材業務可用 not_applicable）／`product_recall_warning`
（產品召回／警告）／`sec_investigation_restatement`（SEC 調查／重編財報）。

每組欄位規則與 `coverage.<axis>` 相同：found 需 ≥1 條帶 source／as_of／
direction／affects 的 finding；none 需 ≥2 條 queries_run；不適用（如非藥品業務
的 `clinical_fda`）用 `status:"none"`＋queries_run 說明「非藥品/器材業務，已查
證無相關監管動作」，**不得省略該組鍵**。
"""

EVENTS_JSON_SAMPLE = """{
    "ma_merger": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "lawsuit_class_action": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "clinical_fda": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "product_recall_warning": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "sec_investigation_restatement": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""}
  }"""


def _resolve_archetype(cli_archetype, prior):
    """回傳 (archetype, source)。source 只供 log／回報用途。"""
    if cli_archetype:
        return cli_archetype, "cli"
    if isinstance(prior, dict):
        try:
            a = (prior.get("prior_dd") or {}).get("prior_meta", {}).get("archetype")
            if a:
                return a, "prior.prior_dd.prior_meta.archetype"
        except Exception:
            pass
        a = prior.get("archetype_hint")
        if a:
            return a, "prior.archetype_hint"
    return None, None


def _run_subprocess(cmd, manifest, step_name, cwd=None):
    r = subprocess.run(
        [str(c) for c in cmd], cwd=str(cwd or REPO_ROOT),
        capture_output=True, text=True,
    )
    manifest["steps"].append({
        "step": step_name,
        "cmd": " ".join(str(c) for c in cmd),
        "returncode": r.returncode,
    })
    return r


# ---------------------------------------------------------------------------
# plan
# ---------------------------------------------------------------------------

def cmd_plan(args):
    ticker = args.ticker.strip().upper()
    date = args.date or time.strftime("%Y%m%d")
    run_dir = _run_dir(ticker, date)
    parts_dir = run_dir / "parts"
    prompts_dir = run_dir / "prompts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    py = _pick_python()

    manifest = {
        "ticker": ticker,
        "date": date,
        "state": "planning",
        "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "steps": [],
        "agents": [],
    }

    # 1. dd_prior.py（零 LLM，前份 DD／q.py 帳本／canonical ID／逐字稿路徑）
    prior_out = parts_dir / "prior.json"
    r = _run_subprocess(
        [py, SCRIPTS_DIR / "dd_prior.py", ticker, "--date", date, "--out", prior_out],
        manifest, "dd_prior",
    )
    prior = {}
    if r.returncode != 0:
        print("[warn] dd_prior.py 失敗（exit {0}）：{1}".format(
            r.returncode, r.stderr.strip()[-500:]), file=sys.stderr)
    elif prior_out.exists():
        try:
            prior = _load_json(prior_out)
        except Exception as e:
            print("[warn] prior.json 解析失敗：{0}".format(e), file=sys.stderr)

    # 2. archetype 解析
    archetype, src = _resolve_archetype(args.archetype, prior)
    if not archetype:
        archetype = DEFAULT_ARCHETYPE
        src = "default_fallback"
        print(
            "[warn] 未給 --archetype 且 prior.json 無可用 archetype_hint（前份 DD "
            "可能是不含 archetype 欄位的 legacy schema），退回基準 archetype={0!r}"
            "（coverage-axes.md by_archetype 附加軸數=0，即僅 common 軸）".format(archetype),
            file=sys.stderr,
        )
    print("archetype={0!r}（來源：{1}）".format(archetype, src))
    manifest["archetype"] = archetype
    manifest["archetype_source"] = src

    # 3. dd_evidence.py init（既有腳本固定寫到 .dd_build/{T}_{D}.evidence.json，
    #    搬一份進 run 目錄；不改該腳本行為）
    init_cmd = [
        "python3", SCRIPTS_DIR / "dd_evidence.py", "init", ticker, date,
        "--archetype", archetype,
    ]
    if args.segments:
        init_cmd += ["--segments", args.segments]
    r = _run_subprocess(init_cmd, manifest, "dd_evidence_init")
    if r.returncode != 0:
        print("[error] dd_evidence.py init 失敗：{0}".format(r.stderr.strip()), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    evidence_flat = BUILD_DIR / "{0}_{1}.evidence.json".format(ticker, date)
    evidence_dest = run_dir / "evidence.json"
    if evidence_flat.exists():
        evidence_dest.write_text(evidence_flat.read_text(encoding="utf-8"), encoding="utf-8")

    # 4. dd_evidence.py axes --json
    axes_cmd = [
        "python3", SCRIPTS_DIR / "dd_evidence.py", "axes",
        "--archetype", archetype, "--json", "--ticker", ticker,
    ]
    if args.segments:
        axes_cmd += ["--segments", args.segments]
    r = _run_subprocess(axes_cmd, manifest, "dd_evidence_axes")
    if r.returncode != 0:
        print("[error] dd_evidence.py axes 失敗：{0}".format(r.stderr.strip()), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    try:
        axes = json.loads(r.stdout)
    except Exception as e:
        print("[error] axes --json 輸出不是合法 JSON：{0}".format(e), file=sys.stderr)
        _atomic_write_json(run_dir / "manifest.json", manifest)
        return 1
    _atomic_write_json(run_dir / "axes.json", axes)

    # 5. numbers_extra（--offline 時跳過；失敗只 warn 不 abort）
    if args.offline:
        manifest["steps"].append({"step": "dd_numbers_extra", "skipped": "offline"})
    else:
        numbers_extra_out = parts_dir / "numbers_extra.json"
        ne_cmd = [py, SCRIPTS_DIR / "dd_numbers_extra.py", ticker, date, "--out", numbers_extra_out]
        if args.peers:
            ne_cmd += ["--peers", args.peers]
        if evidence_dest.exists():
            ne_cmd += ["--evidence", evidence_dest]
        r = _run_subprocess(ne_cmd, manifest, "dd_numbers_extra")
        if r.returncode != 0:
            print("[warn] dd_numbers_extra.py 失敗（不 abort）：{0}".format(
                r.stderr.strip()[-500:]), file=sys.stderr)

    # 6. 軸分批：major_events 單獨一批，其餘每 --axes-per-batch 軸一批
    axis_list = axes if isinstance(axes, list) else []
    major = [a for a in axis_list if a.get("id") == "major_events"]
    rest = [a for a in axis_list if a.get("id") != "major_events"]
    batches = []
    if major:
        batches.append(major)
    step = max(1, args.axes_per_batch)
    for i in range(0, len(rest), step):
        batches.append(rest[i:i + step])

    spawn_list = []
    for k, batch in enumerate(batches, start=1):
        is_major = any(a.get("id") == "major_events" for a in batch)
        part_rel = "parts/axes_{0}.json".format(k)
        part_path = run_dir / part_rel
        mapping = {
            "TICKER": ticker,
            "N_AXES": str(len(batch)),
            "AXES_BLOCK": _axis_block(batch),
            "PART_PATH": str(part_path),
            "EVENTS_BLOCK": EVENTS_ADDENDUM if is_major else "",
            "EVENTS_JSON_KEY": (',\n  "events": ' + EVENTS_JSON_SAMPLE) if is_major else "",
        }
        prompt_text = _render_template(PROMPTS_TMPL_DIR / "coverage.md.tmpl", mapping)
        prompt_rel = "prompts/a_{0}.md".format(k)
        (run_dir / prompt_rel).write_text(prompt_text, encoding="utf-8")
        spawn_list.append({
            "id": "a_{0}".format(k),
            "model": "sonnet",
            "prompt": prompt_rel,
            "out": part_rel,
            "tools": SPAWN_TOOLS_COVERAGE,
            "max_turns": 12,
            "budget_cache_read": BUDGET_CACHE_READ_DEFAULT,
        })

    # a1_numbers
    numbers_mapping = {
        "TICKER": ticker,
        "DATE": date,
        "PART_PATH": str(parts_dir / "numbers_collect.json"),
        "NUMBERS_EXTRA_PATH": str(parts_dir / "numbers_extra.json"),
    }
    (prompts_dir / "a1_numbers.md").write_text(
        _render_template(PROMPTS_TMPL_DIR / "numbers.md.tmpl", numbers_mapping), encoding="utf-8")
    spawn_list.append({
        "id": "a1_numbers", "model": "sonnet", "prompt": "prompts/a1_numbers.md",
        "out": "parts/numbers_collect.json", "tools": SPAWN_TOOLS_NUMBERS,
        "max_turns": 15, "budget_cache_read": BUDGET_CACHE_READ_DEFAULT,
    })

    # a2_digest
    digest_mapping = {
        "TICKER": ticker,
        "DATE": date,
        "DIGEST_PATH": str(run_dir / "digest.json"),
        "EVIDENCE_PATH": str(evidence_dest),
    }
    (prompts_dir / "a2_digest.md").write_text(
        _render_template(PROMPTS_TMPL_DIR / "digest.md.tmpl", digest_mapping), encoding="utf-8")
    spawn_list.append({
        "id": "a2_digest", "model": "sonnet", "prompt": "prompts/a2_digest.md",
        "out": "digest.json", "tools": SPAWN_TOOLS_DIGEST,
        "max_turns": 10, "budget_cache_read": BUDGET_CACHE_READ_DEFAULT,
    })

    # k_koyfin
    koyfin_mapping = {
        "TICKER": ticker,
        "DATE": date,
        "PART_PATH": str(parts_dir / "transcripts.json"),
        "EVIDENCE_PATH": str(evidence_dest),
    }
    (prompts_dir / "k_koyfin.md").write_text(
        _render_template(PROMPTS_TMPL_DIR / "koyfin.md.tmpl", koyfin_mapping), encoding="utf-8")
    spawn_list.append({
        "id": "k_koyfin", "model": "sonnet", "prompt": "prompts/k_koyfin.md",
        "out": "parts/transcripts.json", "tools": SPAWN_TOOLS_KOYFIN,
        "max_turns": 10, "budget_cache_read": BUDGET_CACHE_READ_DEFAULT,
    })

    _atomic_write_json(run_dir / "spawn_list.json", spawn_list)

    manifest["state"] = "planned"
    manifest["agents"] = [s["id"] for s in spawn_list]
    _atomic_write_json(run_dir / "manifest.json", manifest)

    print("\n{0:14s} {1:8s} {2:10s} {3}".format("id", "model", "max_turns", "out"))
    for s in spawn_list:
        print("{0:14s} {1:8s} {2:<10d} {3}".format(s["id"], s["model"], s["max_turns"], s["out"]))
    print("\n共 {0} 個 spawn，寫入 {1}".format(len(spawn_list), run_dir))
    return 0


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

_TOP_LEVEL_FILES = [
    "evidence.json", "axes.json", "spawn_list.json", "digest.json",
    "judgment.json", "scenario.json", "scenario_meta.json",
]
_SUBDIRS = ["parts", "prompts", "agents", "tables", "prose", "bundles"]


def cmd_status(args):
    ticker = args.ticker.strip().upper()
    date = args.date
    run_dir = _run_dir(ticker, date)
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        print("[error] 找不到 run 目錄或 manifest：{0}".format(manifest_path), file=sys.stderr)
        return 1
    manifest = _load_json(manifest_path)
    print("ticker={0} date={1} state={2} created={3}".format(
        manifest.get("ticker"), manifest.get("date"), manifest.get("state"), manifest.get("created")))
    print("archetype={0!r}（來源：{1}）".format(manifest.get("archetype"), manifest.get("archetype_source")))
    print("steps={0} agents={1}".format(len(manifest.get("steps", [])), len(manifest.get("agents", []))))

    print()
    for name in _TOP_LEVEL_FILES:
        p = run_dir / name
        if p.exists():
            print("[ok      ] {0:24s} {1:>10d} bytes".format(name, p.stat().st_size))
        else:
            print("[missing ] {0:24s} —".format(name))

    for sub in _SUBDIRS:
        d = run_dir / sub
        if d.exists():
            files = sorted(f for f in d.iterdir() if f.is_file())
            print("\n{0}/ （{1} 檔）".format(sub, len(files)))
            for f in files:
                print("  {0:30s} {1:>10d} bytes".format(f.name, f.stat().st_size))
        else:
            print("\n{0}/  missing".format(sub))
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(prog="ddreport.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("plan")
    pl.add_argument("ticker")
    pl.add_argument("--date", default=None, help="YYYYMMDD；預設今天")
    pl.add_argument("--archetype", default=None)
    pl.add_argument("--peers", default=None)
    pl.add_argument("--segments", default=None)
    pl.add_argument("--axes-per-batch", type=int, default=AXES_PER_BATCH_DEFAULT)
    pl.add_argument("--offline", action="store_true")
    pl.set_defaults(func=cmd_plan)

    st = sub.add_parser("status")
    st.add_argument("ticker")
    st.add_argument("date")
    st.set_defaults(func=cmd_status)

    return p


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
