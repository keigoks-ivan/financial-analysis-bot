#!/usr/bin/env python3
"""dd2 run.py — DD 管線 v20 主流程（原型）。

    python3 scripts/dd2/run.py TICKER [--date YYYYMMDD] [--until STAGE] [--resume]
                               [--judgment-model fable|opus|sonnet] [--dry-run] [--no-push]

段：plan → stage0 → facts → judged → gated → brief → prose → finish
LLM 只在 stage0（sonnet，每軸一通）、judged（Fable，單輪無工具）、gated（opus，單輪無工具）、
prose（sonnet，只有 Write）四處出手；其餘全部零 LLM，沿用 scripts/ddreport.py 與 dd_*.py 的既有工具。
沒有修補輪：形狀錯先 `dd_project.py normalize` 一次，仍錯就 FAIL 停下。閘紅燈即 FAIL 停下。

契約見 scripts/dd2/README.md；設計稿 notes/site-internal/dd/_dd_v20_clean_design_20260916.md。
"""
import argparse
import datetime as _dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS_DIR = HERE.parent
REPO_ROOT = SCRIPTS_DIR.parent
for p in (str(SCRIPTS_DIR), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import ddreport  # noqa: E402  舊鏈：只 import helper，不改它
import dd_headless  # noqa: E402
from cards import CARDS_DIR  # noqa: E402
from facts_store import FactsStore  # noqa: E402
import bundle  # noqa: E402
import spawn as sp  # noqa: E402

STAGES = ["plan", "stage0", "facts", "judged", "gated", "brief", "prose", "finish"]

# 設計稿 §4 的通契約
COVERAGE_MAX_TURNS = 8
COVERAGE_MAX_TURNS_SEGMENTED = 12
COVERAGE_BUDGET = ddreport.BUDGET_CACHE_READ_COVERAGE
NUMBERS_MAX_TURNS = 14
NUMBERS_BUDGET = ddreport.BUDGET_CACHE_READ_NUMBERS
STAGE0_MAX_PARALLEL = int(os.environ.get("DD_MAX_PARALLEL", "8"))
JUDGE_THINKING_CAP = 32_000
JUDGE_BUDGET = ddreport.JUDGE_BUDGET_CACHE_READ
GATE_BUDGET = ddreport.GATE_BUDGET_CACHE_READ
PROSE_MAX_TURNS = 6
PROSE_BUDGET = ddreport.PROSE_BUDGET_CACHE_READ
DEFAULT_JUDGMENT_MODEL = ddreport.DEFAULT_JUDGMENT_MODEL
GATE_MODEL_FOR = ddreport.GATE_MODEL_FOR

_now = ddreport._now
_atomic_write_json = ddreport._atomic_write_json
_load_json = ddreport._load_json
_run_dir = ddreport._run_dir
_pick_python = ddreport._pick_python


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------

class Ctx:
    def __init__(self, ticker, date, args):
        self.ticker = ticker
        self.date = date
        self.args = args
        self.run_dir = _run_dir(ticker, date)
        self.manifest_path = self.run_dir / "manifest.json"
        self.manifest = {}
        self.judgment_model = args.judgment_model or DEFAULT_JUDGMENT_MODEL
        self.gate_model = GATE_MODEL_FOR.get(self.judgment_model, "opus")
        self.store = FactsStore(REPO_ROOT, ticker)
        self.run_id = "{0}_{1}".format(ticker, date)

    def load_manifest(self):
        if self.manifest_path.exists():
            self.manifest = _load_json(self.manifest_path)
        else:
            self.manifest = {"ticker": self.ticker, "date": self.date, "state": "planned",
                             "created": _now(), "stages": {}}
        self.manifest.setdefault("stages", {})
        self.manifest["pipeline"] = "dd2-v20"
        self.manifest["judgment_model"] = self.judgment_model
        return self.manifest

    def save(self):
        _atomic_write_json(self.manifest_path, self.manifest)

    def stage_begin(self, name):
        st = {"state": "RUNNING", "started": _now(), "agent_usage": []}
        self.manifest["stages"][name] = st
        self.manifest["state"] = "{0}_running".format(name)
        self.save()
        return st

    def stage_end(self, name, ok, note=None):
        st = self.manifest["stages"].setdefault(name, {})
        st["state"] = "PASS" if ok else "FAIL"
        st["ended"] = _now()
        if note:
            st["note"] = note[-2000:]
        self.manifest["state"] = "{0}_{1}".format(name, "pass" if ok else "fail")
        self.save()
        print("[{0}] {1}{2}".format(name, st["state"], ("  " + note.splitlines()[-1]) if note else ""))
        return ok

    def stage_passed(self, name):
        return (self.manifest.get("stages", {}).get(name) or {}).get("state") == "PASS"


def _usage_record(label, r, extra=None):
    rec = {"id": label, "ok": r.get("ok"), "num_turns": r.get("num_turns"),
           "output_tokens": r.get("output_tokens"), "cache_read": r.get("cache_read"),
           "cache_creation": r.get("cache_creation"), "cost_usd": r.get("cost_usd"),
           "duration_ms": r.get("duration_ms"), "over_budget": r.get("over_budget"),
           "thinking_tokens": r.get("thinking_tokens"), "haiku_input_tokens": r.get("haiku_input_tokens")}
    if extra:
        rec.update(extra)
    return rec


def _sub(cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, cwd=cwd)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _today_iso(date_yyyymmdd):
    return "{0}-{1}-{2}".format(date_yyyymmdd[:4], date_yyyymmdd[4:6], date_yyyymmdd[6:8])


# ---------------------------------------------------------------------------
# plan：零 LLM 準備，直接借舊鏈的 plan 子命令（evidence init／axes／prior／
# numbers_extra／Koyfin／a1_numbers prompt）。--reuse-days 0：跨 run 的沿用改由
# facts_store 按軸決定，不用舊鏈整包 30 天那套。
# ---------------------------------------------------------------------------

def do_plan(ctx):
    cmd = [_pick_python(), SCRIPTS_DIR / "ddreport.py", "plan", ctx.ticker, "--date", ctx.date,
           "--reuse-days", "0", "--axes-per-batch", "1"]
    if ctx.args.archetype:
        cmd += ["--archetype", ctx.args.archetype]
    if ctx.args.peers:
        cmd += ["--peers", ctx.args.peers]
    if ctx.args.offline:
        cmd.append("--offline")
    rc, out = _sub(cmd, cwd=REPO_ROOT)
    ctx.load_manifest()
    st = ctx.stage_begin("plan")
    st["cmd"] = " ".join(str(c) for c in cmd)
    ok = rc == 0 and (ctx.run_dir / "evidence.json").exists() and (ctx.run_dir / "axes.json").exists()
    return ctx.stage_end("plan", ok, out)


# ---------------------------------------------------------------------------
# stage0：查。過期軸每軸一通 sonnet；新鮮軸從證據庫注入；numbers 一通（有新鮮
# 值就跳過）。不重試；超輪數的軸寫成 status=none＋note 交給 finalize。
# ---------------------------------------------------------------------------

def _new_quarter(ctx, evidence):
    cur = ddreport._latest_transcript_date(evidence.get("transcripts") or {})
    prev = ctx.store.latest_transcript_date()
    if not cur:
        return False
    return (prev is None) or (str(cur) > str(prev))


def _price_move_pct(ctx, evidence):
    cur = (evidence.get("numbers") or {}).get("price_at_dd")
    prev = ctx.store.last_price()
    try:
        if cur and prev:
            return abs(float(cur) / float(prev) - 1.0) * 100.0
    except (TypeError, ValueError, ZeroDivisionError):
        pass
    return None


def do_stage0(ctx):
    st = ctx.stage_begin("stage0")
    run_dir = ctx.run_dir
    parts_dir = run_dir / "parts"
    prompts_dir = run_dir / "prompts"
    agents_dir = run_dir / "agents"
    for d in (parts_dir, prompts_dir, agents_dir):
        d.mkdir(parents=True, exist_ok=True)

    evidence = _load_json(run_dir / "evidence.json")
    axes = _load_json(run_dir / "axes.json")
    if isinstance(axes, dict):
        axes = axes.get("axes") or []
    axis_ids = [a.get("id") for a in axes if a.get("id")]

    new_q = _new_quarter(ctx, evidence)
    move = _price_move_pct(ctx, evidence)
    plan = ctx.store.plan_refresh(axis_ids, _today_iso(ctx.date), new_quarter=new_q, price_move_pct=move)
    stale_ids = list(plan.get("stale") or [])
    fresh = plan.get("fresh") or {}
    st["refresh_plan"] = {"stale": stale_ids, "fresh": sorted(fresh.keys()),
                          "new_quarter": new_q, "price_move_pct": move}
    if fresh:
        part = {"coverage": fresh}
        if "major_events" in fresh and ctx.store.get_events():
            part["events"] = ctx.store.get_events()
        _atomic_write_json(parts_dir / "reused_coverage.json", part)

    # 每軸一通
    specs = []
    by_id = {a.get("id"): a for a in axes}
    for k, axis_id in enumerate(stale_ids, start=1):
        axis = by_id.get(axis_id)
        if not axis:
            continue
        is_major = axis_id == "major_events"
        is_seg = (not is_major) and ddreport._is_segmented_axis(axis)
        part_rel = "parts/axes_{0}.json".format(k)
        mapping = {
            "TICKER": ctx.ticker,
            "N_AXES": "1",
            "AXES_BLOCK": ddreport._axis_block([axis]),
            "PART_PATH": str(run_dir / part_rel),
            "EVENTS_BLOCK": ddreport.EVENTS_ADDENDUM if is_major else "",
            "EVENTS_JSON_KEY": (',\n  "events": ' + ddreport.EVENTS_JSON_SAMPLE) if is_major else "",
        }
        text = ddreport._render_template(ddreport.PROMPTS_TMPL_DIR / "coverage.md.tmpl", mapping)
        prompt_rel = "prompts/a_{0}_{1}.md".format(k, axis_id)
        (run_dir / prompt_rel).write_text(text, encoding="utf-8")
        specs.append({"id": "a_{0}_{1}".format(k, axis_id), "axis_id": axis_id, "model": "sonnet",
                      "prompt": prompt_rel, "out": part_rel, "tools": ddreport.SPAWN_TOOLS_COVERAGE,
                      "max_turns": COVERAGE_MAX_TURNS_SEGMENTED if is_seg else COVERAGE_MAX_TURNS,
                      "budget_cache_read": COVERAGE_BUDGET, "run_dir": str(run_dir)})

    # numbers：一通，或沿用
    numbers_fresh = ctx.store.numbers_fresh(new_quarter=new_q)
    if numbers_fresh:
        _atomic_write_json(parts_dir / "numbers_collect.json",
                           {"numbers": {"latest_quarter_kpis": numbers_fresh.get("latest_quarter_kpis")}})
        st["numbers_reused"] = True
    elif (prompts_dir / "a1_numbers.md").exists():
        specs.append({"id": "a1_numbers", "model": "sonnet", "prompt": "prompts/a1_numbers.md",
                      "out": "parts/numbers_collect.json", "tools": ddreport.SPAWN_TOOLS_NUMBERS,
                      "max_turns": NUMBERS_MAX_TURNS, "budget_cache_read": NUMBERS_BUDGET,
                      "run_dir": str(run_dir)})
    st["spawn_list"] = [{k: v for k, v in s.items() if k != "run_dir"} for s in specs]
    ctx.save()

    if specs:
        # dd_headless.spawn_many 用 spec["out"] 當 raw JSON 落點；子 agent 自己 Write part。
        for s in specs:
            s["out"] = "agents/{0}.json".format(s["id"])
        results = dd_headless.spawn_many(specs, max_parallel=STAGE0_MAX_PARALLEL)
        for s, r in zip(specs, results):
            r = r or {"ok": False}
            st["agent_usage"].append(_usage_record(s["id"], r, {"axis_id": s.get("axis_id")}))
        ctx.save()

    # 驗 part；缺檔或不合格 → 寫成 none＋note，不重試
    py = _pick_python()
    incomplete = []
    for s in specs:
        if s["id"] == "a1_numbers":
            continue
        part = run_dir / [x for x in st["spawn_list"] if x["id"] == s["id"]][0]["out"]
        ok = part.exists()
        if ok:
            rc, out = _sub([py, SCRIPTS_DIR / "validate_evidence.py", "--part", part])
            ok = rc == 0
        if not ok:
            incomplete.append(s["axis_id"])
            _atomic_write_json(part, {"coverage": {s["axis_id"]: {
                "status": "none", "queries_run": ["(agent incomplete)"], "findings": [],
                "note": "dd2: 子 agent 未在輪數內交出合格 part，記為缺口"}}})
    st["incomplete_axes"] = incomplete

    rc, out, needs = ddreport._finalize_run_dir(run_dir)
    st["finalize_rc"] = rc
    if rc != 0:
        return ctx.stage_end("stage0", False, out)

    # 回存證據庫
    evidence = _load_json(run_dir / "evidence.json")
    cov = evidence.get("coverage") or {}
    fetched = _today_iso(ctx.date)
    for axis_id in stale_ids:
        if axis_id in cov and axis_id not in incomplete:
            ctx.store.put_axis(axis_id, cov[axis_id], fetched, ctx.run_id, axis_meta=by_id.get(axis_id),
                               events=(evidence.get("events") if axis_id == "major_events" else None))
    numbers = evidence.get("numbers") or {}
    if not numbers_fresh and numbers.get("latest_quarter_kpis"):
        ctx.store.put_numbers({"latest_quarter_kpis": numbers.get("latest_quarter_kpis"),
                               "price_at_dd": numbers.get("price_at_dd")},
                              fetched, ctx.run_id,
                              quarter=(numbers.get("latest_quarter_kpis") or {}).get("quarter"))
    ctx.store.put_transcripts(evidence.get("transcripts") or {}, fetched, ctx.run_id)
    return ctx.stage_end("stage0", True, "stale={0} fresh={1} incomplete={2}".format(
        len(stale_ids), len(fresh), len(incomplete)))


# ---------------------------------------------------------------------------
# facts：零 LLM 事實表
# ---------------------------------------------------------------------------

def do_facts(ctx):
    st = ctx.stage_begin("facts")
    py = _pick_python()
    out = ctx.run_dir / "facts.json"
    rc, o1 = _sub([py, SCRIPTS_DIR / "dd_facts.py", "extract", "--run-dir", ctx.run_dir,
                   "--date", _today_iso(ctx.date), "--out", out])
    if rc != 0 or not out.exists():
        return ctx.stage_end("facts", False, o1)
    rc2, o2 = _sub([py, SCRIPTS_DIR / "dd_facts.py", "check", out, "--report"])
    st["facts_bytes"] = out.stat().st_size
    return ctx.stage_end("facts", True, o1 + "\n" + o2)


# ---------------------------------------------------------------------------
# judged：Fable 單輪無工具；回覆即 JSON。形狀錯 normalize 一次，仍錯就停。
# ---------------------------------------------------------------------------

def _write_judgment(ctx, obj):
    meta = obj.setdefault("meta", {})
    meta.setdefault("ticker", ctx.ticker)
    meta.setdefault("date", _today_iso(ctx.date))
    meta["contract"] = "v19"
    # 兩個檔案指標是機械欄：判斷者不必猜路徑（TXN 2026-09-16 首跑 scenario_ref 沒填 → J2 略過、8 欄漂移對帳成 None）
    obj["facts_ref"] = str(ctx.run_dir / "facts.json")
    obj["scenario_ref"] = str(ctx.run_dir / "scenario.json")
    path = ctx.run_dir / "judgment.json"
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


def normalize_v20(obj):
    """dd2 自己的形狀修正，只做「指標字串→複製既有物件」，不補任何判斷值。
    TXN 2026-09-16 第三跑：`answers.q1_business.verdict_values.single_thing` 寫成
    「見 thesis.single_thing」字串，規格要物件；thesis.single_thing 本身是完整物件，
    複製過去即可。回傳 (obj, changes)。"""
    changes = []
    thesis_st = (obj.get("thesis") or {}).get("single_thing")
    q1 = ((obj.get("answers") or {}).get("q1_business") or {}).get("verdict_values")
    if isinstance(q1, dict) and isinstance(q1.get("single_thing"), str) and isinstance(thesis_st, dict):
        q1["single_thing"] = dict(thesis_st)
        changes.append("q1.verdict_values.single_thing: 指標字串 → 複製 thesis.single_thing")
    return obj, changes


def do_judged(ctx):
    prev_usage = list((ctx.manifest.get("stages", {}).get("judged") or {}).get("agent_usage") or [])
    st = ctx.stage_begin("judged")
    agents_dir = ctx.run_dir / "agents"
    agents_dir.mkdir(exist_ok=True)
    jpath = ctx.run_dir / "judgment.json"
    if ctx.args.reuse_judgment and jpath.exists():
        st["agent_usage"] = prev_usage
        st["reused_judgment"] = True
        obj = _load_json(jpath)
    else:
        b = bundle.build_judge(ctx.run_dir, cards_dir=CARDS_DIR)
        st["bundle_bytes"] = b.get("bytes")
        r = sp.oneshot(b["prompt_path"], ctx.judgment_model, agents_dir / "judge_1.json", ctx.run_dir,
                       thinking_cap=JUDGE_THINKING_CAP, budget_cache_read=JUDGE_BUDGET)
        st["agent_usage"].append(_usage_record("judge_1", r))
        ctx.save()
        if not r.get("ok") or not r.get("result_text"):
            return ctx.stage_end("judged", False, "judge spawn failed: {0}".format(r.get("error") or r.get("note")))
        obj, err = sp.strip_json(r["result_text"])
        if obj is None or not isinstance(obj, dict):
            (ctx.run_dir / "judge_raw.txt").write_text(r["result_text"], encoding="utf-8")
            return ctx.stage_end("judged", False, "judge 回覆不是 JSON 物件：{0}（原文存 judge_raw.txt）".format(err))
    obj, changes = normalize_v20(obj)
    if changes:
        st["normalize_v20"] = changes
    jpath = _write_judgment(ctx, obj)
    st["judgment_bytes"] = jpath.stat().st_size

    ok, report = ddreport._judge_check(ctx.ticker, ctx.date)
    if not ok:
        rc, out = _sub([_pick_python(), SCRIPTS_DIR / "dd_project.py", "normalize", jpath, "--write"])
        st["normalize_note"] = out[-1500:]
        ok, report = ddreport._judge_check(ctx.ticker, ctx.date)
    (ctx.run_dir / "judge_check.txt").write_text(report, encoding="utf-8")
    return ctx.stage_end("judged", ok, report)


# ---------------------------------------------------------------------------
# gated：opus 單輪無工具；JSON 陣列；任一 🔴 即停
# ---------------------------------------------------------------------------

def do_gated(ctx):
    st = ctx.stage_begin("gated")
    agents_dir = ctx.run_dir / "agents"
    b = bundle.build_gate(ctx.run_dir, cards_dir=CARDS_DIR)
    st["bundle_bytes"] = b.get("bytes")
    r = sp.oneshot(b["prompt_path"], ctx.gate_model, agents_dir / "gate_1.json", ctx.run_dir,
                   budget_cache_read=GATE_BUDGET)
    st["agent_usage"].append(_usage_record("gate_1", r))
    ctx.save()
    if not r.get("ok") or not r.get("result_text"):
        return ctx.stage_end("gated", False, "gate spawn failed")
    items, err = sp.strip_json(r["result_text"])
    if not isinstance(items, list):
        (ctx.run_dir / "gate_raw.txt").write_text(r["result_text"], encoding="utf-8")
        return ctx.stage_end("gated", False, "gate 回覆不是 JSON 陣列：{0}（原文存 gate_raw.txt）".format(err))
    clean = []
    for it in items:
        if not isinstance(it, dict):
            continue
        clean.append({"item": str(it.get("item", "")), "light": str(it.get("light", "")),
                      "judgment_path": str(it.get("judgment_path", "")), "reason": str(it.get("reason", ""))})
    reds = [x for x in clean if x["light"].startswith("🔴")]
    yellows = [x for x in clean if x["light"].startswith("🟡")]
    _atomic_write_json(ctx.run_dir / "gate_result.json",
                       {"model": ctx.gate_model, "items": clean, "red": len(reds), "yellow": len(yellows)})
    lines = ["# gate_audit（dd2 v20，{0}）".format(ctx.gate_model), "",
             "判斷級 🔴 = {0}，🟡 = {1}".format(len(reds), len(yellows)), ""]
    for x in clean:
        lines.append("- {0} {1} `{2}` {3}".format(x["light"], x["item"], x["judgment_path"], x["reason"]))
    (ctx.run_dir / "gate_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    st["red"] = len(reds)
    st["yellow"] = len(yellows)
    if reds:
        return ctx.stage_end("gated", False, "閘紅燈 {0} 項，停下交指揮者：\n".format(len(reds)) +
                             "\n".join("- {0} {1} {2}".format(x["item"], x["judgment_path"], x["reason"]) for x in reds))
    return ctx.stage_end("gated", True, "🔴 0 🟡 {0}".format(len(yellows)))


# ---------------------------------------------------------------------------
# brief：零 LLM 快速版（沿用舊鏈）
# ---------------------------------------------------------------------------

def do_brief(ctx):
    rc = ddreport._do_brief(ctx.ticker, ctx.date, True, ctx.manifest, dry_run=ctx.args.dry_run)
    ctx.load_manifest()  # _do_brief 自己寫了 manifest
    return rc == 0


# ---------------------------------------------------------------------------
# prose：sonnet，只有 Write，≤6 輪；split → gates；FAIL 即停，沒有補寫輪
# ---------------------------------------------------------------------------

def do_prose(ctx):
    st = ctx.stage_begin("prose")
    agents_dir = ctx.run_dir / "agents"
    rc = ddreport._do_prose_prepare(ctx.ticker, ctx.date)
    if rc != 0:
        return ctx.stage_end("prose", False, "prose prepare 失敗（gen_dd_tables／機械段）")
    for name in ("prose_A.html", "prose_B.html", "prose_fix.html"):
        p = ctx.run_dir / name
        if p.exists():
            p.unlink()
    b = bundle.build_prose(ctx.run_dir, cards_dir=CARDS_DIR)
    st["bundle_bytes"] = b.get("bytes")
    r = sp.agentic(b["prompt_path"], "sonnet", agents_dir / "prose_1.json", ctx.run_dir,
                   tools=["Write"], max_turns=PROSE_MAX_TURNS, budget_cache_read=PROSE_BUDGET)
    st["agent_usage"].append(_usage_record("prose_1", r))
    ctx.save()
    missing = [n for n in ("prose_A.html", "prose_B.html") if not (ctx.run_dir / n).exists()]
    if missing:
        return ctx.stage_end("prose", False, "散文 agent 未寫出 {0}".format("、".join(missing)))
    written, errors = ddreport._do_prose_split(ctx.ticker, ctx.date)
    st["sids"] = written
    ok, findings = ddreport._run_gates(ctx.run_dir, ctx.ticker, ctx.date)
    depth = ddreport._prose_depth_findings(ctx.run_dir, ctx.ticker, ctx.date)
    findings = list(findings) + list(depth)
    if errors or not ok or depth:
        note = "\n".join(["[split] " + e for e in errors] + ["- {0}：{1}".format(s, why) for s, why in findings])
        return ctx.stage_end("prose", False, note or "gates FAIL")
    out_path = (ctx.run_dir / "DD_full_preview.html") if ctx.args.dry_run \
        else (ddreport.DD_DIR / "DD_{0}_{1}.html".format(ctx.ticker, ctx.date))
    ok2, findings2 = ddreport._run_gates(ctx.run_dir, ctx.ticker, ctx.date, out_html=out_path,
                                         postprocess=not ctx.args.dry_run)
    st["out_path"] = str(out_path)
    if not ok2:
        return ctx.stage_end("prose", False, "\n".join("- {0}：{1}".format(s, w) for s, w in findings2))
    return ctx.stage_end("prose", True, "{0} ({1:,} bytes)".format(out_path, out_path.stat().st_size if out_path.exists() else 0))


# ---------------------------------------------------------------------------
# finish：沿用舊鏈（update_dd_index 同步、archive、commit、push）
# ---------------------------------------------------------------------------

def do_finish(ctx):
    cmd = [_pick_python(), SCRIPTS_DIR / "ddreport.py", "finish", ctx.ticker, ctx.date]
    if ctx.args.dry_run:
        cmd.append("--dry-run")
    if ctx.args.no_push:
        cmd.append("--no-push")
    rc, out = _sub(cmd, cwd=REPO_ROOT)
    ctx.load_manifest()
    st = ctx.manifest["stages"].setdefault("finish", {})
    st["rc"] = rc
    st["note"] = out[-2000:]
    st["state"] = "PASS" if rc == 0 else "FAIL"
    ctx.save()
    print("[finish] rc={0}".format(rc))
    print(out[-1500:])
    return rc


# ---------------------------------------------------------------------------
# 回報
# ---------------------------------------------------------------------------

def report(ctx):
    m = ctx.manifest
    stages = m.get("stages", {})
    tot_in = tot_out = tot_cr = 0
    cost = 0.0
    n_spawn = 0
    for name, st in stages.items():
        for a in st.get("agent_usage") or []:
            n_spawn += 1
            tot_out += a.get("output_tokens") or 0
            tot_cr += a.get("cache_read") or 0
            tot_in += a.get("cache_creation") or 0
            cost += a.get("cost_usd") or 0
    j = ctx.run_dir / "judgment.json"
    verdict = role = "?"
    if j.exists():
        try:
            jj = _load_json(j)
            do = jj.get("decision_out") or {}
            verdict = do.get("verdict") or "?"
            role = do.get("role") or "?"
        except Exception:
            pass
    sm = ctx.run_dir / "scenario_meta.json"
    nums = {}
    if sm.exists():
        try:
            nums = _load_json(sm)
        except Exception:
            nums = {}
    g = stages.get("gated") or {}
    print("\n===== dd2 v20 回報 {0} {1} =====".format(ctx.ticker, ctx.date))
    print("報告：", (stages.get("prose") or {}).get("out_path") or (stages.get("brief") or {}).get("out_path") or "-")
    print("裁決：{0}｜{1}".format(verdict, role))
    print("數字：5Y EV {0}｜IRR base {1}｜Max DD {2}".format(
        nums.get("ev5y_pct", "?"), nums.get("irr_base_pct", "?"), nums.get("max_dd_pct", "?")))
    print("帳：spawns {0}｜cache_write {1:,}｜output {2:,}｜cache_read {3:,}｜cost ${4:.2f}".format(
        n_spawn, tot_in, tot_out, tot_cr, cost))
    print("閘：🔴 {0} 🟡 {1}｜fallback 段數 0（v20 無修補輪）".format(g.get("red", "-"), g.get("yellow", "-")))
    print("manifest：", ctx.manifest_path)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("--date", default=None, help="YYYYMMDD；預設今天")
    ap.add_argument("--archetype", default=None)
    ap.add_argument("--peers", default=None)
    ap.add_argument("--judgment-model", default=None, choices=["fable", "opus", "sonnet"])
    ap.add_argument("--until", default=None, choices=STAGES, help="跑到這段就停（含）")
    ap.add_argument("--resume", action="store_true", help="manifest 已 PASS 的段跳過")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="產物留在 run 目錄，不寫 docs/、不 commit")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--reuse-judgment", action="store_true",
                    help="judged 段不 spawn，拿既有 judgment.json 走 normalize＋check（除錯／省錢用）")
    args = ap.parse_args(argv)

    ticker = args.ticker.strip().upper()
    date = args.date or time.strftime("%Y%m%d")
    ctx = Ctx(ticker, date, args)
    ctx.load_manifest()

    order = [
        ("plan", do_plan), ("stage0", do_stage0), ("facts", do_facts), ("judged", do_judged),
        ("gated", do_gated), ("brief", do_brief), ("prose", do_prose),
    ]
    t0 = time.time()
    for name, fn in order:
        if args.resume and ctx.stage_passed(name):
            print("[{0}] skip（已 PASS）".format(name))
        else:
            ok = fn(ctx)
            if not ok:
                report(ctx)
                print("\nFAIL 於 {0}。看 {1}".format(name, ctx.manifest_path), file=sys.stderr)
                return 1
        if args.until == name:
            report(ctx)
            return 0
    rc = 0
    if args.until in (None, "finish"):
        rc = do_finish(ctx)
    ctx.manifest["wall_seconds"] = int(time.time() - t0)
    ctx.save()
    report(ctx)
    return rc


if __name__ == "__main__":
    sys.exit(main())
