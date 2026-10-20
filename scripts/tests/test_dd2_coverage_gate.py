"""閘 ⑤ 覆蓋面改程式規則＋不適用軸（2026-10-20 持有人核准）：核心軸／不適用軸標記、coverage_gate 燈號、
閘階段覆寫與「核心軸缺證據」直接停下、stage0 不適用軸不派 agent。fixture 全在 tmp_path，不碰 docs/。"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dd2"))
import dd_evidence as de  # noqa: E402
import validate_evidence as ve  # noqa: E402
import run  # noqa: E402

MATRIX = de.load_matrix()
DEFAULT_ARCH = "品質複利成長"


def _cov(archetype=DEFAULT_ARCH, **override):
    """全 found 的 coverage（依 archetype 展開），override＝{axis_id: status}。"""
    cov = {}
    for a in de.resolve_axes(MATRIX, archetype):
        cov[a["id"]] = {"status": "found", "findings": [{"claim": "c"}], "queries_run": ["q"], "note": ""}
    for k, v in override.items():
        cov[k] = {"status": v, "findings": [], "queries_run": ["q"], "note": "n"}
    return cov


# ---- 標記：axes 子命令帶 core／not_applicable_reason ----

def test_axes_flag_core_and_na():
    axes = {a["id"]: a for a in de.resolve_axes(MATRIX, "金融")}
    assert axes["customer_second_source"]["not_applicable_reason"]
    assert not axes["customer_second_source"].get("core")
    assert axes["customer_concentration_credit"].get("core") and axes["customer_concentration_credit"]["not_applicable_reason"]
    assert axes["financial_capital_credit_cycle"].get("core")
    assert not axes["financial_regulatory_capital_rules"].get("core")
    assert not axes["regulatory_antitrust"].get("core") and "not_applicable_reason" not in axes["regulatory_antitrust"]


def test_default_archetype_has_no_na_axes():
    axes = de.resolve_axes(MATRIX, DEFAULT_ARCH)
    assert not [a for a in axes if a.get("not_applicable_reason")]
    assert sorted(a["id"] for a in axes if a.get("core")) == [
        "competitive_share_entrants", "customer_concentration_credit", "end_markets", "supply_demand_durability"]


def test_core_ids_cover_every_archetype_and_exist():
    all_ids = set(a["id"] for a in MATRIX["common"]) | set(a["id"] for v in MATRIX["by_archetype"].values() for a in v)
    for arch in MATRIX["by_archetype"]:
        assert arch in MATRIX["core_axes"]["by_archetype"] and arch in MATRIX["not_applicable_by_archetype"]
        assert de.core_axis_ids(MATRIX, arch) <= all_ids
        assert set(de.na_axis_reasons(MATRIX, arch)) <= all_ids
        # 各 archetype 的核心加項必須是該 archetype 自己的軸
        own = set(a["id"] for a in MATRIX["by_archetype"][arch]) | set(a["id"] for a in MATRIX["common"])
        assert de.core_axis_ids(MATRIX, arch) <= own


def test_segment_expansion_keeps_core_flag():
    axes = de.resolve_axes(MATRIX, DEFAULT_ARCH, segments=["資料中心", "車用"])
    seg = [a for a in axes if a["id"].startswith("end_markets__")]
    assert len(seg) == 2 and all(a.get("core") for a in seg)


# ---- validate_evidence：not_applicable 的 na_allowed ----

def test_na_validation_follows_na_allowed():
    ok, _ = ve.check_axis("customer_second_source", {"status": "not_applicable", "note": "銀行沒有這件事"}, MATRIX)
    assert ok == []
    bad, _ = ve.check_axis("competitive_share_entrants", {"status": "not_applicable", "note": "x"}, MATRIX)
    assert bad and "na_allowed=false" in bad[0]
    empty, _ = ve.check_axis("customer_concentration_credit", {"status": "not_applicable", "note": ""}, MATRIX)
    assert empty  # 沒寫理由仍擋


def test_program_na_part_passes_validation_and_is_selected(tmp_path):
    parts = tmp_path / "parts"
    parts.mkdir()
    na = {a["id"]: {"status": "not_applicable", "queries_run": [], "findings": [], "note": a["not_applicable_reason"],
                    "na_source": "archetype"} for a in de.resolve_axes(MATRIX, "金融") if a.get("not_applicable_reason")}
    (parts / "na_coverage.json").write_text(json.dumps({"coverage": na}, ensure_ascii=False), encoding="utf-8")
    assert parts / "na_coverage.json" in de._select_parts(parts)
    for axis_id, obj in na.items():
        assert ve.check_axis(axis_id, obj, MATRIX)[0] == []


# ---- coverage_gate 燈號 ----

def test_gate_green_when_all_found_or_na():
    g = de.coverage_gate(_cov(customer_second_source="not_applicable"), MATRIX, DEFAULT_ARCH)
    assert g["light"] == "🟢" and not g["core_none"] and not g["noncore_none"]


def test_gate_yellow_when_only_noncore_none():
    g = de.coverage_gate(_cov(regulatory_antitrust="none", major_events="none", channel_business_model_shift="none"),
                         MATRIX, DEFAULT_ARCH)
    assert g["light"] == "🟡" and g["core_none"] == []
    assert g["noncore_none"] == ["channel_business_model_shift", "major_events", "regulatory_antitrust"]


def test_gate_red_when_any_core_none():
    for axis in ("competitive_share_entrants", "supply_demand_durability", "end_markets", "customer_concentration_credit"):
        g = de.coverage_gate(_cov(**{axis: "none"}), MATRIX, DEFAULT_ARCH)
        assert g["light"] == "🔴" and g["core_none"] == [axis], axis
    assert "核心軸缺證據" in g["reason"]


def test_gate_pending_or_missing_core_counts_as_none():
    assert de.coverage_gate(_cov(competitive_share_entrants="pending"), MATRIX, DEFAULT_ARCH)["light"] == "🔴"
    cov = _cov()
    del cov["supply_demand_durability"]
    g = de.coverage_gate(cov, MATRIX, DEFAULT_ARCH)
    assert g["light"] == "🔴" and g["core_none"] == ["supply_demand_durability"]


def test_gate_archetype_core_additions():
    cov = _cov("循環/商品", cyclical_inventory_price_position="none")
    assert de.coverage_gate(cov, MATRIX, "循環/商品")["light"] == "🔴"
    # 歷史類比軸非核心：只標黃
    cov = _cov("循環/商品", cyclical_prior_downcycle_behavior="none")
    assert de.coverage_gate(cov, MATRIX, "循環/商品")["light"] == "🟡"
    # EMS：稼動率核心、同業 ROIC 排名非核心
    assert de.coverage_gate(_cov("EMS/ODM", ems_utilization_capex_cycle="none"), MATRIX, "EMS/ODM")["light"] == "🔴"
    assert de.coverage_gate(_cov("EMS/ODM", ems_roic_asset_turnover_benchmark="none"), MATRIX, "EMS/ODM")["light"] == "🟡"


def test_gate_segmented_axis_groups_by_base_id():
    cov = _cov()
    del cov["end_markets"]
    cov["end_markets__a"] = {"status": "found"}
    cov["end_markets__b"] = {"status": "none"}
    g = de.coverage_gate(cov, MATRIX, DEFAULT_ARCH)
    assert g["light"] == "🟡" and g["partial"] == ["end_markets"]  # 部分分段空：不紅
    cov["end_markets__a"] = {"status": "none"}
    assert de.coverage_gate(cov, MATRIX, DEFAULT_ARCH)["light"] == "🔴"  # 整組全空


def test_gate_agent_claimed_na_on_core_is_listed_but_green():
    cov = _cov(customer_concentration_credit="not_applicable")  # 沒有 na_source＝採證 agent 自報
    g = de.coverage_gate(cov, MATRIX, DEFAULT_ARCH)
    assert g["light"] == "🟢" and g["agent_na_core"] == ["customer_concentration_credit"]
    cov["customer_concentration_credit"]["na_source"] = "archetype"  # 程式標的不列
    assert de.coverage_gate(cov, MATRIX, DEFAULT_ARCH)["agent_na_core"] == []


def test_gate_red_reason_also_mentions_noncore():
    g = de.coverage_gate(_cov(end_markets="none", major_events="none"), MATRIX, DEFAULT_ARCH)
    assert g["light"] == "🔴" and "major_events" in g["reason"]


# ---- run.py：閘階段覆寫與直接停下 ----

def _items(five_light="🟢", extra_light=None):
    items = [{"item": c, "light": "🟢", "judgment_path": "$.x", "reason": "r"}
             for c in ("①", "②", "③", "④", "⑥", "⑦", "⑧")]
    items.insert(4, {"item": "⑤", "light": five_light, "judgment_path": "$.y", "reason": "查詢切題"})
    if extra_light:
        items[0]["light"] = extra_light
    return items


def _gated_env(tmp_path, monkeypatch, coverage, reply_items, judged_archetype=None):
    (tmp_path / "agents").mkdir()
    (tmp_path / "prompts").mkdir()
    ev = {"ticker": "T", "date": "20261020", "archetype_hint": DEFAULT_ARCH, "coverage": coverage}
    (tmp_path / "evidence.json").write_text(json.dumps(ev, ensure_ascii=False), encoding="utf-8")
    j = {"answers": {"q1_business": {"verdict_values": {"archetype": {"primary": judged_archetype}}}}} if judged_archetype else {}
    (tmp_path / "judgment.json").write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(run, "_run_dir", lambda t, d: tmp_path)
    monkeypatch.setattr(run.ddreport, "_gate_input_signature", lambda d: "sig")
    spawns, hints = [], []

    def fake_build(run_dir, cards_dir=None, extra_section=None):
        hints.append(extra_section)
        (tmp_path / "prompts" / "gate.md").write_text("P", encoding="utf-8")
        return {"prompt_path": tmp_path / "prompts" / "gate.md", "bytes": 1}

    def fake_oneshot(prompt_path, model, out, cwd, **kw):
        spawns.append(model)
        return {"ok": True, "result_text": json.dumps(reply_items, ensure_ascii=False)}

    def no_patch(*a, **k):
        raise AssertionError("⑤ 紅燈不該跑 patch")

    monkeypatch.setattr(run.bundle, "build_gate", fake_build)
    monkeypatch.setattr(run.sp, "oneshot_stream", fake_oneshot)
    monkeypatch.setattr(run, "_gate_patch", no_patch)
    args = argparse.Namespace(judgment_model=None, mechanical_gate=False, no_gate_patch=False, judge_effort=None)
    ctx = run.Ctx("T", "20261020", args)
    ctx.load_manifest()
    return ctx, spawns, hints


def test_do_gated_core_none_stops_without_patch_and_overrides_agent(tmp_path, monkeypatch, capsys):
    ctx, spawns, hints = _gated_env(tmp_path, monkeypatch, _cov(competitive_share_entrants="none"), _items("🟢"))
    assert run.do_gated(ctx) is False
    assert spawns == ["sonnet"]  # 只閘一次，沒有 patch／再閘
    out = capsys.readouterr().out
    assert "核心軸缺證據：competitive_share_entrants" in out
    st = ctx.manifest["stages"]["gated"]
    assert st["state"] == "FAIL" and st["red"] == 1
    assert st["coverage_gate"]["light"] == "🔴"
    assert {"path": "$.gate_result.⑤.light", "judge": "🟢", "program": "🔴"} in ctx.manifest["mechanical_overrides"]
    five = [x for x in json.loads((tmp_path / "gate_result.json").read_text(encoding="utf-8"))["items"] if x["item"] == "⑤"][0]
    assert five["light"] == "🔴" and "閘評論：查詢切題" in five["reason"]
    assert "程式判定" in hints[0] and "競爭份額" in hints[0]


def test_do_gated_noncore_none_overrides_agent_red_to_yellow_and_passes(tmp_path, monkeypatch):
    ctx, spawns, _ = _gated_env(tmp_path, monkeypatch, _cov(regulatory_antitrust="none"), _items("🔴"))
    assert run.do_gated(ctx) is True
    st = ctx.manifest["stages"]["gated"]
    assert st["state"] == "PASS" and st["red"] == 0 and st["yellow"] == 1
    assert {"path": "$.gate_result.⑤.light", "judge": "🔴", "program": "🟡"} in ctx.manifest["mechanical_overrides"]


def test_do_gated_all_found_green_no_override_record(tmp_path, monkeypatch):
    ctx, _, _ = _gated_env(tmp_path, monkeypatch, _cov(), _items("🟢"))
    assert run.do_gated(ctx) is True
    assert not ctx.manifest.get("mechanical_overrides")


def test_do_gated_missing_five_item_is_inserted(tmp_path, monkeypatch):
    items = [x for x in _items("🟢") if x["item"] != "⑤"]
    ctx, _, _ = _gated_env(tmp_path, monkeypatch, _cov(regulatory_antitrust="none"), items)
    assert run.do_gated(ctx) is True
    got = json.loads((tmp_path / "gate_result.json").read_text(encoding="utf-8"))["items"]
    assert [x for x in got if x["item"] == "⑤"][0]["light"] == "🟡" and len(got) == 8


def test_do_gated_other_items_red_still_listed_when_five_red(tmp_path, monkeypatch, capsys):
    ctx, spawns, _ = _gated_env(tmp_path, monkeypatch, _cov(end_markets="none"), _items("🟢", extra_light="🔴"))
    assert run.do_gated(ctx) is False
    note = ctx.manifest["stages"]["gated"]["note"]
    assert "閘紅燈 2 項" in note and "- ① " in note and note.splitlines()[-1].startswith("核心軸缺證據：end_markets")


def test_archetype_mismatch_noted_but_not_scored(tmp_path, monkeypatch):
    # plan 時走預設，判斷者歸「循環/商品」：專屬核心軸沒採證，只在 reason 註明，燈號仍 🟢
    ctx, _, _ = _gated_env(tmp_path, monkeypatch, _cov(), _items("🟢"), judged_archetype="循環/商品")
    assert run.do_gated(ctx) is True
    cg = ctx.manifest["stages"]["gated"]["coverage_gate"]
    assert cg["light"] == "🟢"
    assert cg["archetype_mismatch"]["core_not_gathered"] == [
        "cyclical_inventory_price_position", "cyclical_supply_discipline_capacity"]
    assert "未採證" in cg["reason"]


def test_core_none_from_dropped_undated_is_flagged(tmp_path, monkeypatch):
    ctx, _, _ = _gated_env(tmp_path, monkeypatch, _cov(competitive_share_entrants="none"), _items("🟢"))
    ctx.manifest["stages"]["stage0"] = {"dropped_undated": {"competitive_share_entrants": 4, "major_events": 2}}
    assert run.do_gated(ctx) is False
    cg = ctx.manifest["stages"]["gated"]["coverage_gate"]
    assert cg["core_none_dropped_undated"] == {"competitive_share_entrants": 4}  # 非核心軸的不列
    assert "無 as_of" in cg["reason"] and "4 條" in cg["reason"]


def test_missing_evidence_falls_back_to_agent_light(tmp_path, monkeypatch):
    ctx, _, _ = _gated_env(tmp_path, monkeypatch, _cov(), _items("🟡"))
    (tmp_path / "evidence.json").unlink()
    assert run.do_gated(ctx) is True
    st = ctx.manifest["stages"]["gated"]
    assert "coverage_gate_error" in st and "coverage_gate" not in st


# ---- stage0：不適用軸不派 agent ----

def test_stage0_writes_na_part_and_skips_agents(tmp_path, monkeypatch):
    axes = de.resolve_axes(MATRIX, "金融")
    run_dir = tmp_path
    (run_dir / "evidence.json").write_text(json.dumps({"ticker": "T", "coverage": {}}), encoding="utf-8")
    (run_dir / "axes.json").write_text(json.dumps(axes, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(run, "_run_dir", lambda t, d: run_dir)
    monkeypatch.setattr(run, "_new_quarter", lambda c, e: False)
    monkeypatch.setattr(run, "_price_move_pct", lambda c, e: None)
    monkeypatch.setattr(run, "_digest_targets", lambda e: [])
    seen = {}

    def fake_plan(axis_ids, today, new_quarter=False, price_move_pct=None):
        seen["axis_ids"] = list(axis_ids)
        return {"stale": [], "fresh": {}}  # 不派任何 agent

    args = argparse.Namespace(judgment_model=None, resume=False)
    ctx = run.Ctx("T", "20261020", args)
    ctx.load_manifest()
    monkeypatch.setattr(ctx.store, "plan_refresh", fake_plan)
    monkeypatch.setattr(ctx.store, "numbers_fresh", lambda new_quarter=False: {"latest_quarter_kpis": {"items": []}})
    monkeypatch.setattr(run.ddreport, "_finalize_run_dir", lambda d: (0, "", []))
    for name in ("put_axis", "put_numbers", "put_transcripts"):  # 證據庫回存不能寫進 repo 的 facts/
        monkeypatch.setattr(ctx.store, name, lambda *a, **k: None)
    run.do_stage0(ctx)
    assert "customer_second_source" not in seen["axis_ids"] and "customer_concentration_credit" not in seen["axis_ids"]
    assert "competitive_share_entrants" in seen["axis_ids"]
    part = json.loads((run_dir / "parts" / "na_coverage.json").read_text(encoding="utf-8"))["coverage"]
    assert sorted(part) == ["customer_concentration_credit", "customer_second_source"]
    assert part["customer_second_source"]["status"] == "not_applicable" and part["customer_second_source"]["note"]
    assert ctx.manifest["stages"]["stage0"]["not_applicable_axes"] == ["customer_concentration_credit", "customer_second_source"]
    # 非金融（沒有不適用軸）重跑：舊的 na_coverage.json 要清掉
    (run_dir / "axes.json").write_text(json.dumps(de.resolve_axes(MATRIX, DEFAULT_ARCH), ensure_ascii=False), encoding="utf-8")
    run.do_stage0(ctx)
    assert not (run_dir / "parts" / "na_coverage.json").exists()


# ---- facts 段尾判 ⑤：紅就停在 facts，不跑 judged ----

def _facts_env(tmp_path, monkeypatch, coverage, args_extra=None):
    ev = {"ticker": "T", "date": "20261020", "archetype_hint": DEFAULT_ARCH, "coverage": coverage}
    (tmp_path / "evidence.json").write_text(json.dumps(ev, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(run, "_run_dir", lambda t, d: tmp_path)

    def fake_sub(cmd, cwd=None):
        if "extract" in [str(c) for c in cmd]:
            (tmp_path / "facts.json").write_text("{}", encoding="utf-8")
        return 0, "ok"

    monkeypatch.setattr(run, "_sub", fake_sub)
    monkeypatch.setattr(run, "_inject_ma_facts", lambda ctx, out: ("🟢", {}))
    monkeypatch.setattr(run, "decide_valuation_basis", lambda ctx: "eps_pe")
    ns = dict(judgment_model=None, force_gate=False, dry_run=False)
    ns.update(args_extra or {})
    ctx = run.Ctx("T", "20261020", argparse.Namespace(**ns))
    ctx.load_manifest()
    return ctx


def test_do_facts_core_none_stops_before_judged(tmp_path, monkeypatch, capsys):
    ctx = _facts_env(tmp_path, monkeypatch, _cov(competitive_share_entrants="none", major_events="none"))
    assert run.do_facts(ctx) is False
    st = ctx.manifest["stages"]["facts"]
    assert st["state"] == "FAIL" and ctx.manifest["state"] == "facts_fail"
    assert st["coverage_gate"]["light"] == "🔴" and st["coverage_gate"]["core_none"] == ["competitive_share_entrants"]
    assert st["note"].splitlines()[-1].startswith("核心軸缺證據：competitive_share_entrants")
    assert "停在 facts" in st["note"]
    assert "核心軸缺證據：competitive_share_entrants" in capsys.readouterr().out  # stage_end 印最後一行


def test_do_facts_noncore_none_passes_and_records_gate(tmp_path, monkeypatch):
    ctx = _facts_env(tmp_path, monkeypatch, _cov(regulatory_antitrust="none"))
    assert run.do_facts(ctx) is True
    st = ctx.manifest["stages"]["facts"]
    assert st["state"] == "PASS" and st["coverage_gate"]["light"] == "🟡"


def test_do_facts_ignores_stale_judgment_archetype(tmp_path, monkeypatch):
    # facts 段尾 judged 還沒跑，上一輪留下的 judgment.json 不能拿來做 archetype 對照
    ctx = _facts_env(tmp_path, monkeypatch, _cov())
    j = {"answers": {"q1_business": {"verdict_values": {"archetype": {"primary": "循環/商品"}}}}}
    (tmp_path / "judgment.json").write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    assert run.do_facts(ctx) is True
    assert "archetype_mismatch" not in ctx.manifest["stages"]["facts"]["coverage_gate"]


def test_do_facts_force_gate_dry_run_continues(tmp_path, monkeypatch, capsys):
    ctx = _facts_env(tmp_path, monkeypatch, _cov(end_markets="none"), {"force_gate": True, "dry_run": True})
    assert run.do_facts(ctx) is True
    assert ctx.manifest["stages"]["facts"]["coverage_gate"]["light"] == "🔴"  # 仍記紅，閘段會擋
    assert "--force-gate" in capsys.readouterr().out
    # 只有 force_gate 沒有 dry_run：不放行
    ctx2 = _facts_env(tmp_path, monkeypatch, _cov(end_markets="none"), {"force_gate": True, "dry_run": False})
    assert run.do_facts(ctx2) is False


def test_do_facts_missing_evidence_does_not_block(tmp_path, monkeypatch):
    ctx = _facts_env(tmp_path, monkeypatch, _cov())
    (tmp_path / "evidence.json").unlink()
    assert run.do_facts(ctx) is True
    assert "coverage_gate_error" in ctx.manifest["stages"]["facts"]


def _main_env(tmp_path, monkeypatch, coverage):
    ctx0 = _facts_env(tmp_path, monkeypatch, coverage)  # 寫 evidence、掛 monkeypatch
    calls = []

    def fake_stage(name):
        def fn(ctx):
            calls.append(name)
            ctx.stage_begin(name)
            return ctx.stage_end(name, True)
        return fn

    real_facts = run.do_facts

    def counting_facts(ctx):
        calls.append("facts")
        return real_facts(ctx)

    monkeypatch.setattr(run, "do_plan", fake_stage("plan"))
    monkeypatch.setattr(run, "do_stage0", fake_stage("stage0"))
    monkeypatch.setattr(run, "do_facts", counting_facts)
    monkeypatch.setattr(run, "do_judged", lambda ctx: (_ for _ in ()).throw(AssertionError("⑤ 紅不該跑 judged")))
    return calls


def _set_cov(tmp_path, coverage):
    ev = json.loads((tmp_path / "evidence.json").read_text(encoding="utf-8"))
    ev["coverage"] = coverage
    (tmp_path / "evidence.json").write_text(json.dumps(ev, ensure_ascii=False), encoding="utf-8")


def test_main_until_facts_red_returns_1_and_resume_reruns_facts_only(tmp_path, monkeypatch):
    calls = _main_env(tmp_path, monkeypatch, _cov(supply_demand_durability="none"))
    base = ["T", "--date", "20261020", "--until", "facts"]
    assert run.main(base) == 1  # facts 紅：停，judged 不跑（跑了 do_judged 會 AssertionError）
    assert calls == ["plan", "stage0", "facts"]
    m = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert m["stages"]["facts"]["state"] == "FAIL"
    # 補證後 --resume：plan／stage0 已 PASS 跳過，只重跑 facts
    _set_cov(tmp_path, _cov())
    assert run.main(base + ["--resume"]) == 0
    assert calls == ["plan", "stage0", "facts", "facts"]
    # facts 已 PASS：--resume 跳過；--redo facts 才重跑
    assert run.main(base + ["--resume"]) == 0
    assert calls == ["plan", "stage0", "facts", "facts"]
    assert run.main(base + ["--resume", "--redo", "facts"]) == 0
    assert calls == ["plan", "stage0", "facts", "facts", "facts"]


def test_main_until_facts_green_returns_0(tmp_path, monkeypatch):
    calls = _main_env(tmp_path, monkeypatch, _cov(regulatory_antitrust="none"))
    assert run.main(["T", "--date", "20261020", "--until", "facts"]) == 0
    assert calls == ["plan", "stage0", "facts"]


def test_resume_past_facts_pass_still_stops_at_gate(tmp_path, monkeypatch, capsys):
    # facts 當時 PASS（例如舊版程式跑的）、之後證據變紅：--resume 跳過 facts，閘段仍要擋住
    ctx, spawns, _ = _gated_env(tmp_path, monkeypatch, _cov(competitive_share_entrants="none"), _items("🟢"))
    ctx.stage_begin("facts")
    ctx.stage_end("facts", True)
    assert run.do_gated(ctx) is False
    assert "核心軸缺證據：competitive_share_entrants" in capsys.readouterr().out
