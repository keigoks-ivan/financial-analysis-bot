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
import re
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
# 2026-09-16：採證 agent 拿掉自我驗證（Bash）與重寫輪，只留搜尋／讀網頁／寫檔——
# 舊模板每軸 7–10 輪裡有 2–4 輪在跑 validate_evidence.py 自驗，v20 由 run.py 驗。
COVERAGE_TOOLS = ["WebSearch", "WebFetch", "Write"]
COVERAGE_MAX_TURNS = 6
COVERAGE_MAX_TURNS_SEGMENTED = 10
COVERAGE_TMPL = HERE / "prompts" / "coverage.md.tmpl"
COVERAGE_BUDGET = ddreport.BUDGET_CACHE_READ_COVERAGE
NUMBERS_MAX_TURNS = 14
NUMBERS_BUDGET = ddreport.BUDGET_CACHE_READ_NUMBERS
# 12 軸一波開完：牆鐘時間＝最慢那軸，不是兩波相加；token 逐 agent 算、與並行度無關。撞 rate limit 再降。
STAGE0_MAX_PARALLEL = int(os.environ.get("DD_MAX_PARALLEL", "12"))
# Koyfin 下載逾時寫死 300 秒（session 過期會等滿才退回磁碟）；磁碟逐字稿在這天數內就把逾時壓到 15 秒。
KOYFIN_DISK_FRESH_DAYS = 100
KOYFIN_FAST_TIMEOUT = 15
JUDGE_THINKING_CAP = 32_000
JUDGE_BUDGET = ddreport.JUDGE_BUDGET_CACHE_READ
GATE_BUDGET = ddreport.GATE_BUDGET_CACHE_READ
PROSE_MAX_TURNS = 6
PROSE_MAX_TURNS_HALF = 4  # 前後半各一通
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


def _enrich_from_raw(r, out_json):
    """spawn_many 走 dd_headless.spawn，不會算 thinking／haiku；從落地的 raw JSON 補。"""
    try:
        raw = _load_json(Path(out_json))
    except Exception:
        return r
    mu = raw.get("modelUsage") or {}
    r = dict(r or {})
    r["thinking_tokens"] = sum((v.get("thinkingTokens") or 0) for v in mu.values() if isinstance(v, dict))
    r["haiku_input_tokens"] = sum((v.get("inputTokens") or 0) for k, v in mu.items() if "haiku" in k and isinstance(v, dict))
    return r


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

def _disk_transcript_age_days(ticker, date_yyyymmdd):
    """Drive 資料夾裡最新逐字稿（檔名尾 _YYYYMMDD.md）距 run 日幾天；找不到回 None。"""
    folder = ddreport._find_koyfin_drive_folder(ticker)
    if not folder:
        return None
    dates = []
    for f in folder.glob("*.md"):
        m = re.search(r"_(\d{8})\.md$", f.name)
        if m:
            dates.append(m.group(1))
    if not dates:
        return None
    latest = max(dates)
    d0 = _dt.date(int(latest[:4]), int(latest[4:6]), int(latest[6:8]))
    d1 = _dt.date(int(date_yyyymmdd[:4]), int(date_yyyymmdd[4:6]), int(date_yyyymmdd[6:8]))
    return (d1 - d0).days


def do_plan(ctx):
    ns = argparse.Namespace(
        ticker=ctx.ticker, date=ctx.date, archetype=ctx.args.archetype, peers=ctx.args.peers,
        segments=None, axes_per_batch=1, offline=ctx.args.offline, reuse_days=0,
    )
    age = _disk_transcript_age_days(ctx.ticker, ctx.date)
    fast = ctx.args.skip_koyfin or (age is not None and age <= KOYFIN_DISK_FRESH_DAYS)
    prev_timeout = ddreport.KOYFIN_DOWNLOAD_TIMEOUT
    if fast:
        ddreport.KOYFIN_DOWNLOAD_TIMEOUT = KOYFIN_FAST_TIMEOUT
    t0 = time.time()
    try:
        rc = ddreport.cmd_plan(ns)
    finally:
        ddreport.KOYFIN_DOWNLOAD_TIMEOUT = prev_timeout
    ctx.load_manifest()
    st = ctx.stage_begin("plan")
    st["koyfin_fast_path"] = bool(fast)
    st["disk_transcript_age_days"] = age
    st["seconds"] = int(time.time() - t0)
    ok = rc == 0 and (ctx.run_dir / "evidence.json").exists() and (ctx.run_dir / "axes.json").exists()
    return ctx.stage_end("plan", ok, "rc={0} koyfin_fast={1} disk_age={2}d {3}s".format(rc, fast, age, st["seconds"]))


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
        # 搜尋上限照題目數：重大事件五類各一次、分段軸（終端市場逐段）6 次、其餘 3 次。
        # 2026-09-16 TSM 實測固定 3 次時，重大事件把 3 次都用在證券詐欺類，漏掉亞利桑那廠集體訴訟；終端市場 12 條掉到 5 條。
        n_q = len(axis.get("queries") or [])
        max_search = 5 if is_major else (6 if is_seg else max(3, min(n_q, 4)))
        mapping = {
            "TICKER": ctx.ticker,
            "N_AXES": "1",
            "MAX_SEARCH": str(max_search),
            "AXES_BLOCK": ddreport._axis_block([axis]),
            "PART_PATH": str(run_dir / part_rel),
            "EVENTS_BLOCK": ddreport.EVENTS_ADDENDUM if is_major else "",
            "EVENTS_JSON_KEY": (',\n  "events": ' + ddreport.EVENTS_JSON_SAMPLE) if is_major else "",
        }
        text = ddreport._render_template(COVERAGE_TMPL, mapping)
        prompt_rel = "prompts/a_{0}_{1}.md".format(k, axis_id)
        (run_dir / prompt_rel).write_text(text, encoding="utf-8")
        specs.append({"id": "a_{0}_{1}".format(k, axis_id), "axis_id": axis_id, "model": "sonnet",
                      "prompt": prompt_rel, "out": part_rel, "tools": COVERAGE_TOOLS,
                      "max_turns": COVERAGE_MAX_TURNS_SEGMENTED if (is_seg or is_major) else COVERAGE_MAX_TURNS,
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
            r = _enrich_from_raw(r or {"ok": False}, run_dir / s["out"])
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

# ---------------------------------------------------------------------------
# 週線均線六態（timing-appendix §F）：純機械，判斷者不得自判。
# 2026-09-16：TXN 判斷者無資料硬填 ✅（閘抓）、TSM 填「-」（矩陣自動降衛星）——兩檔同一個洞。
# 借 dd_screener_ma.compute_ma_snapshot（yfinance 週線＋快取）與 build_quality_entry 的六態映射。
# ---------------------------------------------------------------------------

def _ma_state(ticker):
    import dd_screener_ma
    import build_quality_entry
    snap = dd_screener_ma.compute_ma_snapshot(ticker, use_cache=True)
    label, _score = build_quality_entry.ma_state_label_and_score(snap or {})
    if label == "—":
        label = "-"
    return snap or {}, label


def _inject_ma_facts(ctx, facts_path):
    """把六態與四個均線數字加進 facts.json 的 q5_valuation.facts；回 (label, snapshot)。"""
    snap, label = _ma_state(ctx.ticker)
    _atomic_write_json(ctx.run_dir / "ma_snapshot.json", {"label": label, "snapshot": snap})
    facts = _load_json(facts_path)
    q5 = facts.setdefault("questions", {}).setdefault("q5_valuation", {})
    arr = q5.setdefault("facts", [])
    arr[:] = [f for f in arr if not str(f.get("id", "")).startswith("f_ma_")]
    as_of = _today_iso(ctx.date)
    src = {"type": "manual", "ref": "ma_snapshot.json", "as_of": as_of,
           "citation": "程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）"}
    basis = "timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%"
    arr.append({"id": "f_ma_state", "label": "週線均線六態（decision_inputs.ma 必須等於此值）", "value": label,
                "period": as_of, "unit": None, "basis": basis, "kind": "realized", "source": src,
                "quote": "price {0} / W52 {1} / W104 {2} / W250 {3} / W250 13週斜率 {4}%".format(
                    snap.get("price"), snap.get("w52"), snap.get("w104"), snap.get("w250"), snap.get("slope_w250_pct"))})
    for key, lab in (("w52", "52 週均線"), ("w104", "104 週均線"), ("w250", "250 週均線"), ("slope_w250_pct", "W250 13 週斜率")):
        if snap.get(key) is not None:
            arr.append({"id": "f_ma_" + key, "label": lab, "value": snap.get(key), "period": as_of,
                        "unit": "%" if key.endswith("pct") else "USD", "basis": "週線收盤 SMA（yfinance auto_adjust）",
                        "kind": "realized", "source": src})
    _atomic_write_json(facts_path, facts)
    return label, snap


def do_facts(ctx):
    st = ctx.stage_begin("facts")
    py = _pick_python()
    out = ctx.run_dir / "facts.json"
    rc, o1 = _sub([py, SCRIPTS_DIR / "dd_facts.py", "extract", "--run-dir", ctx.run_dir,
                   "--date", _today_iso(ctx.date), "--out", out])
    if rc != 0 or not out.exists():
        return ctx.stage_end("facts", False, o1)
    try:
        label, snap = _inject_ma_facts(ctx, out)
        st["ma_state"] = label
        st["ma_snapshot"] = {k: snap.get(k) for k in ("price", "w52", "w104", "w250", "slope_w250_pct")}
    except Exception as exc:  # 均線抓不到不擋事實表，記下來讓判斷者填「-」
        st["ma_state_error"] = str(exc)[:300]
    rc2, o2 = _sub([py, SCRIPTS_DIR / "dd_facts.py", "check", out, "--report"])
    st["facts_bytes"] = out.stat().st_size
    if re.search(r"^\[FAIL\]", o2, re.M):
        return ctx.stage_end("facts", False, o1 + "\n" + o2)
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
    # 機械覆寫：decision_inputs.ma ＝ 事實表 f_ma_state（程式算的週線六態），判斷者填什麼都不算
    ma_path = ctx.run_dir / "ma_snapshot.json"
    if ma_path.exists():
        label = (_load_json(ma_path) or {}).get("label")
        if label:
            di = obj.setdefault("decision_inputs", {})
            if di.get("ma") != label:
                ctx.manifest.setdefault("mechanical_overrides", []).append(
                    {"path": "$.decision_inputs.ma", "judge": di.get("ma"), "program": label})
                di["ma"] = label
    obj, drift_log = program_drift_entries(ctx, obj, decision_out=None)
    st = ctx.manifest.get("stages", {}).get("judged")
    if isinstance(st, dict):
        st["program_drift"] = drift_log
        st["oneliner_role_words"] = _oneliner_role_warn(obj)
    path = ctx.run_dir / "judgment.json"
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# 程式欄位漂移歸因（2026-09-16 TSM 閘紅燈 ⑧）：ma 由程式算、price_at_dd 由事實表來，
# 因 ma 變動導致矩陣改列的裁決／角色變動也是機械結果。這幾欄的 contradictions 條目由程式
# 生成，判斷者只歸因基本面欄位；判斷者條目裡誤掛這幾欄（尤其掛在「價格變動」下）一律拆掉。
# ---------------------------------------------------------------------------

PROGRAM_DRIFT_FIELDS_MA = ("ma",)
PROGRAM_DRIFT_FIELDS_PRICE = ("price_at_dd",)
DECISION_FIELDS = ("dca_verdict", "dca_role")
_PROGRAM_TAG = "[程式歸因]"


def _prior_meta(ctx):
    pp = ctx.run_dir / "parts" / "prior.json"
    if not pp.exists():
        return {}
    pd_ = (_load_json(pp) or {}).get("prior_dd") or {}
    pm = dict(pd_.get("prior_meta") or {})
    for k in ("dca_verdict", "dca_role", "price_at_dd"):
        if pm.get(k) is None and pd_.get(k) is not None:
            pm[k] = pd_.get(k)
    return pm


def _current_price(ctx):
    ev = ctx.run_dir / "evidence.json"
    if ev.exists():
        return ((_load_json(ev) or {}).get("numbers") or {}).get("price_at_dd")
    return None


def _ma_label(ctx):
    mp = ctx.run_dir / "ma_snapshot.json"
    return ((_load_json(mp) or {}).get("label") if mp.exists() else None)


def _mk_entry(cause, fields, axis, side_a, side_b, ruling):
    return {"axis": _PROGRAM_TAG + axis, "cause": cause, "prior_field": list(fields),
            "side_a": side_a, "side_b": side_b, "ruling": ruling,
            "evidence_level": "程式計算", "settle_metric": "—", "if_then": [], "evidence_refs": []}


def program_drift_entries(ctx, obj, decision_out=None):
    """回 (obj, log)。把程式欄位從判斷者條目拆掉，前插程式條目。decision_out 有值時（judge check 之後）
    才把裁決／角色變動併進 ma 那條。可重複呼叫（先移除舊的程式條目再重建）。"""
    log = []
    pm = _prior_meta(ctx)
    decision_out = decision_out or obj.get("decision_out") or None
    ce = obj.setdefault("counter_evidence", {})
    entries = [e for e in (ce.get("contradictions") or []) if isinstance(e, dict)]
    entries = [e for e in entries if not str(e.get("axis", "")).startswith(_PROGRAM_TAG)]
    ma_now, ma_prev = _ma_label(ctx), pm.get("ma")
    price_now, price_prev = _current_price(ctx), pm.get("price_at_dd")
    ma_changed = bool(ma_now) and ma_prev is not None and ma_now != ma_prev
    program_fields = set(PROGRAM_DRIFT_FIELDS_MA) | set(PROGRAM_DRIFT_FIELDS_PRICE)

    # 1. 拆判斷者條目裡的程式欄；掛在「價格變動」下的裁決／角色也拆
    for e in entries:
        pf = e.get("prior_field")
        if isinstance(pf, str):
            pf = [pf]
        if not isinstance(pf, list):
            continue
        keep = []
        for f in pf:
            if f in program_fields:
                log.append("拆掉判斷者條目 prior_field '{0}'（程式欄）".format(f))
                continue
            # 裁決／角色掛在「價格變動」下：只有程式會接手歸因（ma 變動）時才拆，否則留給閘審
            # （MU 2026-09-17：ma 沒變卻拆掉，變成沒人歸因 → 驗證 FAIL）
            if f in DECISION_FIELDS and e.get("cause") == "價格變動" and ma_changed:
                log.append("拆掉判斷者條目 prior_field '{0}'（裁決變更不得併入價格原因，改由程式歸因於 ma）".format(f))
                continue
            keep.append(f)
        e["prior_field"] = keep

    # 2. 程式條目
    new_entries = []
    if ma_now is not None:
        fields = list(PROGRAM_DRIFT_FIELDS_MA)
        axis = "週線均線六態由程式算（timing-appendix §F）：前份 {0} → 本次 {1}".format(ma_prev, ma_now)
        ruling = "均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；" + (
            "此欄變動屬方法變動，不是基本面新證據。" if ma_changed else "與前份相同。")
        if ma_changed and not decision_out:
            # 裁決還沒算：先預留兩欄，讓 validate 的漂移對帳過得了；phase 2 再依實際裁決改寫
            fields += list(DECISION_FIELDS)
            axis += "；裁決／角色若因此被矩陣改列，直接原因為本欄（待 dd_decision.py 算出後補實際值）"
        if decision_out and ma_changed:
            v_prev, r_prev = pm.get("dca_verdict"), pm.get("dca_role")
            v_now, r_now = decision_out.get("verdict"), decision_out.get("role")
            moved = []
            if v_prev is not None and v_now and v_now != v_prev:
                moved.append("dca_verdict")
            if r_prev is not None and r_now and r_now != r_prev:
                moved.append("dca_role")
            if moved:
                fields += moved
                parts = []
                if "dca_verdict" in moved:
                    parts.append("裁決 {0}→{1}".format(v_prev, v_now))
                if "dca_role" in moved:
                    parts.append("角色 {0}→{1}".format(r_prev, r_now))
                axis += "；矩陣落第 {0} 列，{1} 隨之改變".format(decision_out.get("row_hit"), "、".join(parts))
                ruling += " 裁決與角色由 dd_decision.py 依 decision_inputs 機械路由，本次變動的直接原因是 ma 這一欄（{0}→{1}）；基本面欄位的變動另見判斷者條目。".format(ma_prev, ma_now)
        new_entries.append(_mk_entry("方法變動", fields, axis,
                                     "前份 ma={0}".format(ma_prev), "本次 ma={0}".format(ma_now), ruling))
        log.append("程式條目：ma（方法變動）" + ("＋" + "/".join(fields[1:]) if len(fields) > 1 else ""))
    if price_now is not None:
        try:
            chg = (float(price_now) / float(price_prev) - 1.0) * 100.0 if price_prev else None
        except (TypeError, ValueError, ZeroDivisionError):
            chg = None
        new_entries.append(_mk_entry("價格變動", list(PROGRAM_DRIFT_FIELDS_PRICE),
                                     "判斷日現價由事實表帶入：前份 {0} → 本次 {1}{2}".format(
                                         price_prev, price_now, "（{0:+.1f}%）".format(chg) if chg is not None else ""),
                                     "前份 price_at_dd={0}".format(price_prev), "本次 price_at_dd={0}".format(price_now),
                                     "現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。"))
        log.append("程式條目：price_at_dd（價格變動）")
    ce["contradictions"] = new_entries + entries
    return obj, log


def _oneliner_role_warn(obj):
    ol = str(obj.get("oneliner") or "")
    hits = [w for w in ("核心倉", "衛星倉", "核心持有", "追蹤池", "不持有") if w in ol]
    return hits


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
    # TSM 2026-09-16：q4 quality 的 buyback／lumpiness 留 null，schema 要 object（無必填子欄）。
    # 空物件＝「判斷者沒填」，不補任何值；渲染端把空物件當未展開。
    q4 = ((obj.get("answers") or {}).get("q4_capital") or {}).get("verdict_values") or {}
    quality = q4.get("quality")
    if isinstance(quality, dict):
        for k in ("buyback", "lumpiness"):
            if k in quality and quality[k] is None:
                quality[k] = {}
                changes.append("q4.verdict_values.quality.{0}: null → {{}}（空物件，未補值）".format(k))
    # TSM 2026-09-16 第二跑：governance.sbc 寫成一句話，schema 要 object（無必填子欄）。
    # 字串原文包進 {"note": …}，內容一字不動。
    gov = q4.get("governance")
    if isinstance(gov, dict):
        for k in ("sbc", "capital_returns"):
            if isinstance(gov.get(k), str):
                gov[k] = {"note": gov[k]}
                changes.append("q4.verdict_values.governance.{0}: 字串 → {{\"note\": 原文}}".format(k))
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
        # 優先從原始回覆重建（judgment.json 可能已被上一輪的 normalize／程式歸因／patch 改過，
        # 不是乾淨起點；MU 2026-09-17 就是拆過的欄位被寫回磁碟導致重用時找不到）
        obj = None
        raw_path = agents_dir / "judge_1.json"
        if raw_path.exists():
            raw = _load_json(raw_path) or {}
            text = raw.get("stitched_text") or raw.get("result") or ""
            if text:
                cand, err = sp.strip_json(text)
                if isinstance(cand, dict):
                    obj = cand
                    st["reused_from"] = "agents/judge_1.json"
        if obj is None:
            obj = _load_json(jpath)
            st["reused_from"] = "judgment.json"
    else:
        b = bundle.build_judge(ctx.run_dir, cards_dir=CARDS_DIR)
        st["bundle_bytes"] = b.get("bytes")
        extra = ["--effort", ctx.args.judge_effort] if ctx.args.judge_effort else None
        r = sp.oneshot_stream(b["prompt_path"], ctx.judgment_model, agents_dir / "judge_1.json", ctx.run_dir,
                              thinking_cap=JUDGE_THINKING_CAP, budget_cache_read=JUDGE_BUDGET, extra_args=extra)
        st["judge_effort"] = ctx.args.judge_effort
        st["stitched_parts"] = r.get("stitched_parts")
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
    if ok:
        # phase 2：decision_out 已由 dd_decision.py 寫回 judgment.json，把因 ma 變動導致的裁決／角色變動併進程式條目
        cur = _load_json(jpath)
        cur, drift_log2 = program_drift_entries(ctx, cur, decision_out=cur.get("decision_out") or {})
        jpath.write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding="utf-8")
        st["program_drift"] = drift_log2
        ok, report = ddreport._judge_check(ctx.ticker, ctx.date)
    (ctx.run_dir / "judge_check.txt").write_text(report, encoding="utf-8")
    return ctx.stage_end("judged", ok, report)


# ---------------------------------------------------------------------------
# gated：opus 單輪無工具；JSON 陣列；任一 🔴 即停
# ---------------------------------------------------------------------------

GATE_PATCH_MAX = 1  # 2026-09-16 持有人拍板：閘紅燈後允許一通 patch map，再閘一次，仍紅就停


def _gate_once(ctx, st, idx):
    """跑一次閘。回 (ok_spawn, clean_items, reds, yellows)。"""
    agents_dir = ctx.run_dir / "agents"
    b = bundle.build_gate(ctx.run_dir, cards_dir=CARDS_DIR)
    st.setdefault("bundle_bytes", []).append(b.get("bytes"))
    r = sp.oneshot_stream(b["prompt_path"], ctx.gate_model, agents_dir / "gate_{0}.json".format(idx), ctx.run_dir,
                          budget_cache_read=GATE_BUDGET)
    st["agent_usage"].append(_usage_record("gate_{0}".format(idx), r))
    ctx.save()
    if not r.get("ok") or not r.get("result_text"):
        return False, [], [], []
    items, err = sp.strip_json(r["result_text"])
    if not isinstance(items, list):
        (ctx.run_dir / "gate_raw_{0}.txt".format(idx)).write_text(r["result_text"], encoding="utf-8")
        st["gate_parse_error"] = "gate 回覆不是 JSON 陣列：{0}".format(err)
        return False, [], [], []
    clean = []
    for it in items:
        if not isinstance(it, dict):
            continue
        clean.append({"item": str(it.get("item", "")), "light": str(it.get("light", "")),
                      "judgment_path": str(it.get("judgment_path", "")), "reason": str(it.get("reason", ""))})
    reds = [x for x in clean if x["light"].startswith("🔴")]
    yellows = [x for x in clean if x["light"].startswith("🟡")]
    _atomic_write_json(ctx.run_dir / "gate_result.json",
                       {"model": ctx.gate_model, "round": idx, "items": clean, "red": len(reds), "yellow": len(yellows)})
    lines = ["# gate_audit（dd2 v20，{0}，第 {1} 輪）".format(ctx.gate_model, idx), "",
             "判斷級 🔴 = {0}，🟡 = {1}".format(len(reds), len(yellows)), ""]
    for x in clean:
        lines.append("- {0} {1} `{2}` {3}".format(x["light"], x["item"], x["judgment_path"], x["reason"]))
    audit_path = ctx.run_dir / "gate_audit.md"
    audit_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # 舊鏈 finish 的 _gate_audit_is_current 要這兩個欄（審核綁定輸入內容）
    import hashlib as _hl
    st["audit_sha256"] = _hl.sha256(audit_path.read_bytes()).hexdigest()
    st["input_signature"] = ddreport._gate_input_signature(ctx.run_dir)
    ctx.save()
    return True, clean, reds, yellows


def _gate_patch(ctx, st, clean, idx):
    """閘紅燈後的一通定點修補：Fable 單輪回 patch map，程式用舊鏈的候選目錄驗證後套用。回 (ok, note)。"""
    agents_dir = ctx.run_dir / "agents"
    jpath = ctx.run_dir / "judgment.json"
    raw = _load_json(jpath)
    prior = _load_json(ctx.run_dir / "parts" / "prior.json") if (ctx.run_dir / "parts" / "prior.json").exists() else {}
    items = [x for x in clean if x["light"].startswith(("🔴", "🟡"))]
    gate_items = "\n".join("- {0} {1} `{2}` {3}".format(x["light"], x["item"], x["judgment_path"], x["reason"]) for x in items)
    tmpl = (HERE / "prompts" / "gate_patch.md.tmpl").read_text(encoding="utf-8")
    text = tmpl.format(
        ticker=ctx.ticker, date=ctx.date, gate_items=gate_items,
        judgment_compact=json.dumps(raw, ensure_ascii=False, separators=(",", ":")),
        prior_compact=bundle.prior_summary(prior),
    )
    ppath = ctx.run_dir / "prompts" / "gate_patch_{0}.md".format(idx)
    ppath.write_text(text, encoding="utf-8")
    r = sp.oneshot_stream(ppath, ctx.judgment_model, agents_dir / "gate_patch_{0}.json".format(idx), ctx.run_dir,
                          thinking_cap=JUDGE_THINKING_CAP, budget_cache_read=JUDGE_BUDGET,
                          extra_args=(["--effort", ctx.args.judge_effort] if ctx.args.judge_effort else None))
    st["agent_usage"].append(_usage_record("gate_patch_{0}".format(idx), r))
    ctx.save()
    if not r.get("ok") or not r.get("result_text"):
        return False, "patch spawn failed"
    patches = ddreport._parse_patch_map(r["result_text"])
    if not patches:
        (ctx.run_dir / "gate_patch_raw_{0}.txt".format(idx)).write_text(r["result_text"], encoding="utf-8")
        return False, "patch 回覆解析不到 json:patch 區塊"
    applied, errors = ddreport._apply_patch_map(ctx.run_dir, patches)
    st.setdefault("patches", []).append({"round": idx, "requested": len(patches.get("judgment") or {}),
                                         "applied": applied, "errors": errors[:20]})
    ctx.save()
    if errors:
        return False, "patch 驗證未過（原檔未動）：\n" + "\n".join(str(e)[:200] for e in errors[:10])
    ok, report = ddreport._judge_check(ctx.ticker, ctx.date)
    (ctx.run_dir / "judge_check.txt").write_text(report, encoding="utf-8")
    return ok, "patch 套用 {0} 筆，judge check {1}".format(applied, "PASS" if ok else "FAIL")


def do_gated(ctx):
    st = ctx.stage_begin("gated")
    (ctx.run_dir / "agents").mkdir(exist_ok=True)
    max_rounds = 1 + (0 if ctx.args.no_gate_patch else GATE_PATCH_MAX)
    for idx in range(1, max_rounds + 1):
        ok_spawn, clean, reds, yellows = _gate_once(ctx, st, idx)
        if not ok_spawn:
            return ctx.stage_end("gated", False, st.get("gate_parse_error") or "gate spawn failed")
        st["red"] = len(reds)
        st["yellow"] = len(yellows)
        st["rounds"] = idx
        if not reds:
            return ctx.stage_end("gated", True, "🔴 0 🟡 {0}（第 {1} 輪）".format(len(yellows), idx))
        if idx >= max_rounds:
            break
        ok, note = _gate_patch(ctx, st, clean, idx)
        st["patch_note"] = note
        if not ok:
            return ctx.stage_end("gated", False, "閘紅燈 {0} 項，修補失敗：{1}".format(len(reds), note))
    return ctx.stage_end("gated", False, "閘紅燈 {0} 項（{1} 輪後仍紅），停下交指揮者：\n".format(len(reds), st["rounds"]) +
                         "\n".join("- {0} {1} {2}".format(x["item"], x["judgment_path"], x["reason"]) for x in reds))


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

# ---------------------------------------------------------------------------
# v20 散文閘：沿用舊鏈六支機械檢查（組頁／數字白名單／機器語言／標點／驗算），
# 但不接 2026-09-11 未完成的 validate_report_v19（要求條列附 f_* id、要求抽取器
# 尚未實作的 e9b 財務表非空），改用自己的篇幅下限與中文寫作掃描。
# ---------------------------------------------------------------------------

PROSE_TOTAL_FLOOR = ddreport.DD_FULL_FLOOR_BYTES   # 70,000，與 pre-commit 同值
# 2026-09-16 校準：v19 版面把約 74KB 內容放進機械表格（TXN 預覽 96KB 含 22KB 散文），
# 散文本體下限不能照舊版面的 46KB 訂。先取 20KB／s5 3KB，等三檔對照再調。
PROSE_TEXT_FLOOR = 20_000                            # 散文本體（不含表格）下限
PROSE_SECTION_FLOOR = {"s3": 1500, "s4": 1500, "s5": 3000, "s6": 1500, "s7": 1200, "s10": 1200, "s12": 1500}
PROSE_THINKING_CAP = 8_000                            # sonnet 散文通思考上限（實測 95K 太浪費）
_MECH_TABLE_SIDS = ("appB", "appC", "revlog", "s14", "appA")  # v19 機械表的機器語言命中降為 WARN

_ZH_PATTERNS = [
    ("——", r"——"), ("；", r"；"),
    ("不是A是B", r"不是[^。]{1,30}(?:而是|，是)"),
    ("這就是", r"這就是"), ("自我說明", r"值得(?:注意|點出|一提)|本頁不"),
    ("比喻", r"吹出|煞車|柱子|震央|癒合|扛著|甩開|雪崩|閘門|藥方|天平|鏡像|同一張牌|拆柱"),
    ("半形逗號接中文", r"[\u4e00-\u9fff],"),
]


def _zh_scan(prose_dir):
    """zh-analyst-prose §一 的機械掃描，回 [(sid, 問題, 次數)]。只掃散文段（不掃機械表）。"""
    import html as _html
    out = []
    for f in sorted(Path(prose_dir).glob("*.html")):
        sid = f.stem
        if sid in _MECH_TABLE_SIDS:
            continue
        plain = _html.unescape(re.sub(r"<[^>]+>", " ", f.read_text(encoding="utf-8")))
        for label, pat in _ZH_PATTERNS:
            n = len(re.findall(pat, plain))
            if n:
                out.append((sid, label, n))
    return out


def _gates_v20(ctx, out_html=None, postprocess=False):
    """回 (ok, findings, warns)。findings 擋，warns 只印。"""
    import dd_sections
    run_dir = ctx.run_dir
    py = _pick_python()
    prose_dir, tables_dir = run_dir / "prose", run_dir / "tables"
    judgment_path, evidence_path = run_dir / "judgment.json", run_dir / "evidence.json"
    out_path = Path(out_html) if out_html else run_dir / "DD_preview.html"
    findings, warns = [], []

    cmd = [py, SCRIPTS_DIR / "render_dd.py", "--assemble", prose_dir, "--tables", tables_dir,
           "--judgment", judgment_path, "-o", out_path, "--layout", "v19"]
    if not postprocess:
        cmd.append("--no-postprocess")
    rc, out = _sub(cmd)
    if rc != 0:
        return False, [("_assemble", out.strip()[-500:])], warns

    vp = [py, SCRIPTS_DIR / "validate_prose.py", prose_dir, "--judgment", judgment_path, "--json"]
    if evidence_path.exists():
        vp += ["--evidence", evidence_path]
    r = subprocess.run([str(c) for c in vp], capture_output=True, text=True)
    try:
        vj = json.loads(r.stdout) if r.stdout.strip() else None
    except (json.JSONDecodeError, ValueError):
        vj = None
    if vj is None:
        findings.append(("_validate_prose", (r.stdout + r.stderr).strip()[-500:]))
    else:
        for sid, misses in (vj.get("by_section") or {}).items():
            sample = "、".join("{0}（{1}）".format(m.get("raw"), m.get("context")) for m in misses[:3])
            findings.append((sid, "validate_prose：{0} 個未覆蓋數字：{1}".format(len(misses), sample)))

    html_text = out_path.read_text(encoding="utf-8")
    markers = dd_sections.split_sections(html_text)
    for lineno, word, ctxt in dd_sections.leak_hits(html_text):
        sid = ddreport._sid_for_line(html_text, lineno, markers) or "_global"
        (warns if sid in _MECH_TABLE_SIDS else findings).append((sid, "leaks：{0}（…{1}…）".format(word, ctxt)))

    rc, out = _sub([py, SCRIPTS_DIR / "qc.py", "--escalate", out_path])
    if rc != 0:
        findings.append(("_qc", out.strip()[-500:]))
    rc, out = _sub([py, SCRIPTS_DIR / "verify_dd_math.py", out_path])
    if rc != 0:
        findings.append(("_math", out.strip()[-500:]))

    total = out_path.stat().st_size
    text_total = sum(f.stat().st_size for f in prose_dir.glob("*.html") if f.stem not in _MECH_TABLE_SIDS)
    if total < PROSE_TOTAL_FLOOR:
        findings.append(("_depth", "整檔 {0:,}B < 下限 {1:,}B".format(total, PROSE_TOTAL_FLOOR)))
    if text_total < PROSE_TEXT_FLOOR:
        findings.append(("_depth", "散文本體 {0:,}B < 下限 {1:,}B".format(text_total, PROSE_TEXT_FLOOR)))
    for sid, floor in PROSE_SECTION_FLOOR.items():
        f = prose_dir / (sid + ".html")
        if f.exists() and f.stat().st_size < floor:
            findings.append((sid, "篇幅 {0:,}B < 下限 {1:,}B".format(f.stat().st_size, floor)))
    for sid, label, n in _zh_scan(prose_dir):
        warns.append((sid, "zh：{0} ×{1}".format(label, n)))
    return not findings, findings, warns


def _prose_prepare_v20(ctx):
    """v20 的散文準備：只跑 gen_dd_tables（v19 分支同時產 v19-s14／appA／revlog 機械段），
    不呼叫舊鏈 `_do_prose_prepare`——它在 v19 判斷檔上會改走「判斷者直接寫給讀者」的
    research_sections 路徑，要求 financial_note 等散文欄，v20 那些由 sonnet 寫。回 (ok, note)。"""
    run_dir = ctx.run_dir
    judgment_path = run_dir / "judgment.json"
    scenario_meta_path = run_dir / "scenario_meta.json"
    tables_dir = run_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "prose").mkdir(parents=True, exist_ok=True)
    cmd = [_pick_python(), SCRIPTS_DIR / "gen_dd_tables.py", judgment_path, "--out", tables_dir,
           "--scenario-html", tables_dir / "e11.html"]
    if scenario_meta_path.exists():
        cmd += ["--scenario-meta", scenario_meta_path]
    rc, out = _sub(cmd)
    return rc == 0, out[-1200:]


def do_prose(ctx):
    prev_usage_all = list((ctx.manifest.get("stages", {}).get("prose") or {}).get("agent_usage") or [])
    st = ctx.stage_begin("prose")
    st["agent_usage"] = prev_usage_all if ctx.args.reuse_prose else []
    agents_dir = ctx.run_dir / "agents"
    ok0, note0 = _prose_prepare_v20(ctx)
    if not ok0:
        return ctx.stage_end("prose", False, "prose prepare 失敗（gen_dd_tables）：" + note0)
    if ctx.args.reuse_prose and (ctx.run_dir / "prose_A.html").exists():
        st["reused_prose"] = True
    else:
        for name in ("prose_A.html", "prose_B.html", "prose_fix.html"):
            p = ctx.run_dir / name
            if p.exists():
                p.unlink()
        # 2026-09-16：前後半兩通同時寫（牆鐘減半，token 不變）；每通只列大綱不預演全文
        specs = []
        for part in ("A", "B"):
            b = bundle.build_prose(ctx.run_dir, cards_dir=CARDS_DIR, part=part)
            st.setdefault("bundle_bytes", {})[part] = b.get("bytes")
            specs.append({"id": "prose_{0}".format(part), "model": "sonnet",
                          "prompt": str(b["prompt_path"]), "out": str(agents_dir / "prose_{0}.json".format(part)),
                          "tools": ["Write"], "max_turns": PROSE_MAX_TURNS_HALF,
                          "budget_cache_read": PROSE_BUDGET, "run_dir": str(ctx.run_dir)})
        results = dd_headless.spawn_many(specs, max_parallel=2)
        for spec, r in zip(specs, results):
            st["agent_usage"].append(_usage_record(spec["id"], _enrich_from_raw(r or {"ok": False}, spec["out"])))
        ctx.save()
    missing = [n for n in ("prose_A.html", "prose_B.html") if not (ctx.run_dir / n).exists()]
    if missing:
        return ctx.stage_end("prose", False, "散文 agent 未寫出 {0}".format("、".join(missing)))
    written, errors = ddreport._do_prose_split(ctx.ticker, ctx.date)
    st["sids"] = written
    ok, findings, warns = _gates_v20(ctx)
    st["zh_warns"] = ["{0}：{1}".format(a, b) for a, b in warns]
    for a, b in warns:
        print("  [warn] {0}：{1}".format(a, b))
    if errors or not ok:
        note = "\n".join(["[split] " + e for e in errors] + ["- {0}：{1}".format(s, why) for s, why in findings])
        return ctx.stage_end("prose", False, note or "gates FAIL")
    out_path = (ctx.run_dir / "DD_full_preview.html") if ctx.args.dry_run \
        else (ddreport.DD_DIR / "DD_{0}_{1}.html".format(ctx.ticker, ctx.date))
    ok2, findings2, _ = _gates_v20(ctx, out_html=out_path, postprocess=not ctx.args.dry_run)
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
    ap.add_argument("--judge-effort", default=None, choices=["low", "medium", "high"],
                    help="判斷／修補通的 --effort（實測 Fable 小題 low/medium 思考歸零；預設不帶＝完整思考）")
    ap.add_argument("--until", default=None, choices=STAGES, help="跑到這段就停（含）")
    ap.add_argument("--resume", action="store_true", help="manifest 已 PASS 的段跳過")
    ap.add_argument("--redo", default=None, help="逗號分隔的段名，即使已 PASS 也重跑（配 --resume）")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="產物留在 run 目錄，不寫 docs/、不 commit")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--skip-koyfin", action="store_true", help="不等 Koyfin 下載（逾時壓到 15 秒），直接用磁碟逐字稿")
    ap.add_argument("--no-gate-patch", action="store_true", help="閘紅燈後不做 patch map，直接停")
    ap.add_argument("--force-gate", action="store_true",
                    help="閘紅燈仍往下做 brief／prose 預覽（只在 --dry-run 有效；manifest 記 FAIL，finish 拒絕）")
    ap.add_argument("--reuse-prose", action="store_true",
                    help="prose 段不 spawn，拿既有 prose_A/B.html 走 split＋gates（除錯／省錢用）")
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
    redo = set(x.strip() for x in (args.redo or "").split(",") if x.strip())
    for name, fn in order:
        if args.resume and ctx.stage_passed(name) and name not in redo:
            print("[{0}] skip（已 PASS）".format(name))
        elif args.resume and name == "gated" and args.force_gate and args.dry_run \
                and (ctx.manifest.get("stages", {}).get("gated") or {}).get("rounds"):
            # 已跑過閘且紅燈未清，--force-gate（只限 dry-run）跳過重跑，往下做預覽；manifest 仍記 FAIL，finish 會拒絕
            print("[gated] skip（FAIL，--force-gate 強行往下，僅供預覽）")
        else:
            ok = fn(ctx)
            if not ok and not (name == "gated" and args.force_gate and args.dry_run):
                report(ctx)
                print("\nFAIL 於 {0}。看 {1}".format(name, ctx.manifest_path), file=sys.stderr)
                return 1
            if not ok:
                print("[gated] FAIL 但 --force-gate（dry-run）強行往下，僅供預覽，不得發布")
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
