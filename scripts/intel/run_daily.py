#!/usr/bin/env python3
"""scripts/intel/run_daily.py — Phase 1 orchestrator: fetch (optional) →
classify (haiku) → summarize (sonnet, incl. story-thread assignment) →
threads.merge_daily (thread counts/heat/cooling) → deepread (sonnet, ≤12
articles) → digest (sonnet brief_zh) → write docs/intel/data/{date}.json →
render (if scripts/intel/render.py exists yet).

2026-08-19「加料」：新增 deepread.py（重要卡讀全文）與 threads.py（故事串連），
見 notes/site-internal/intel/DESIGN.md 2026-08-19 晚間段落。兩者都掛在
llm_available 分支裡——`--no-llm` 路徑（見下）完全不跑，deep read 需要 sonnet，
threads 的機械路徑理論上零 LLM 也能跑，但因為 `--no-llm` 路徑本來就不呼叫
classify/summarize（只處理 kind=="data" 卡），沒有 news 卡可供指派，故一併
跳過，只讀現有 threads 狀態供 status 頁參考。

對應 notes/site-internal/intel/DESIGN.md §10（每天怎麼跑）。這支是 GHA
`.github/workflows/intel-daily.yml` 唯一直接呼叫的入口。

失敗策略：只有「連 JSON 都寫不出來」才回非 0（讓 workflow 標紅）；LLM 任何一步
失敗都走 classify.py/summarize.py 內建的保守 fallback（零 LLM 的 data 卡片
永遠會在、市場層仍能上頁），這是 DESIGN §6 rule 3「寧可漏不爆額度」的延伸。
若 CLAUDE_CODE_OAUTH_TOKEN 沒設，直接跳過兩段 LLM 呼叫（不必讓 llm.py 每個
batch 都失敗重試三次才知道結果），只保留 data 卡片＋日曆，`"llm":"unavailable"`。

CLI:
    python3 scripts/intel/run_daily.py --date 2026-08-19
    python3 scripts/intel/run_daily.py --date 2026-08-19 --skip-fetch
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

from classify import classify
from common import (
    ROOT,
    daily_output_path,
    iso,
    load_json,
    load_source_name_map,
    load_source_short_map,
    now_utc,
    pending_path,
)
from deepread import run_deepread
from llm import Ledger
from summarize import (
    build_calendar,
    build_digest,
    build_flags,
    build_gauges,
    finalize_card,
    passthrough_card,
    summarize_cards,
    summarize_data_card,
)
from classify import classify_data_card
import threads as threads_mod

INTEL_DIR = ROOT / "scripts" / "intel"
NEXT_RUN_LABEL = "06:00 TPE"


def _today_tpe() -> str:
    return datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")


def _llm_available() -> bool:
    return bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") or os.environ.get("CLAUDE_CODE_USE_LOCAL_AUTH"))


def run_fetch(date: str) -> bool:
    cmd = [sys.executable, str(INTEL_DIR / "fetch.py"), "--date", date]
    print(f"[intel/run_daily] fetch: {' '.join(cmd)}")
    proc = subprocess.run(cmd)
    return proc.returncode == 0


def run_render(date: str) -> None:
    render_py = INTEL_DIR / "render.py"
    if not render_py.exists():
        print("[intel/run_daily] scripts/intel/render.py not found yet — skipping render step "
              "(built by a parallel workstream).", file=sys.stderr)
        return
    cmd = [sys.executable, str(render_py), "--date", date]
    print(f"[intel/run_daily] render: {' '.join(cmd)}")
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        print(f"[intel/run_daily] WARNING: render.py exited {proc.returncode}", file=sys.stderr)


def build_output(date: str, pending: dict, llm_available: bool) -> dict:
    meta = pending.get("meta", {})
    all_cards = pending.get("cards", [])
    ledger = Ledger()
    name_map = load_source_name_map()
    short_map = load_source_short_map()

    # calendar 純 Python、跟 LLM 開關無關，先算好——gauges 的 cb 欄在沒有今日
    # 央行卡片時要退而求其次找日曆裡最近的 FOMC 條目。
    calendar = build_calendar(date)

    threads_output: list = []
    deep_log: dict = {}

    if not llm_available:
        print("[intel/run_daily] CLAUDE_CODE_OAUTH_TOKEN not set — LLM steps skipped, "
              "data-only mode.", file=sys.stderr)
        data_cards = [c for c in all_cards if c.get("kind") == "data"]
        for c in data_cards:
            classify_data_card(c)
            summarize_data_card(c)
        finalized = [finalize_card(c, name_map, short_map) for c in data_cards]
        gauges = build_gauges(data_cards, calendar)
        flags = build_flags(data_cards)
        brief_zh = []
        classified_count = len(data_cards)
        summarized_count = len(data_cards)
        llm_tag = "unavailable"
        threads_state = threads_mod.load_state()  # --no-llm 路徑不寫回，只讀現況給 status 頁看
    else:
        result = classify(pending, ledger)
        selected = result["selected"]
        selected_ids = {c["id"] for c in selected}

        # 故事串連（threads.py）：sonnet 摘要那通呼叫順便帶「目前活躍故事線」
        # 清單給模型判斷歸屬（零額外呼叫）；title-only 卡片用機械路徑比對。
        threads_state = threads_mod.load_state()
        active_threads = threads_mod.active_thread_list(threads_state)
        summarized = summarize_cards(selected, ledger, active_threads=active_threads)
        # 2026-08-19：relevant 但沒擠進 stage 2（sonnet 每日額度／per-source cap）
        # 的卡片不再整批消失——走 passthrough_card()（title-only，
        # summarized:false），一樣進最終輸出。「回應內容有點空虛」的另一半
        # 成因就是這裡：舊版只有進了 sonnet 的卡才會出現在頁面上。
        passthrough = [
            passthrough_card(c) for c in result["all"]
            if c.get("relevant") and c["id"] not in selected_ids
        ]
        raw_cards = summarized["cards"] + passthrough
        threads_mod.assign_mechanical(passthrough, threads_state)
        threads_output = threads_mod.merge_daily(date, raw_cards, threads_state)
        threads_mod.save_state(threads_state)

        finalized = [finalize_card(c, name_map, short_map) for c in raw_cards]

        # 重要卡讀全文（deepread.py）：在 finalize 之後、digest 之前跑，這樣
        # digest 的早報寫手能用上 card["deep"]["takeaway_zh"]（見
        # summarize.build_digest 的 deep_takeaway 欄位）。
        deep_log = run_deepread(finalized, ledger)

        digest = build_digest(result["all"], finalized, ledger, name_map, short_map)
        gauges = build_gauges(result["all"], calendar)
        flags = build_flags(result["all"])
        brief_zh = digest["brief_zh"]
        classified_count = sum(1 for c in result["all"] if c.get("relevant"))
        summarized_count = summarized["log"]["summarized"]
        llm_tag = "ok"

    deep_counts = {"ok": 0, "paywall": 0, "fail": 0, "skipped": 0}
    for c in finalized:
        ds = c.get("deep_status")
        if ds in deep_counts:
            deep_counts[ds] += 1

    status = {
        "sources_ok": meta.get("sources_ok", 0),
        "sources_fail": meta.get("sources_fail", 0),
        "fetched": meta.get("counts", {}).get("fetched", 0),
        "kept": meta.get("counts", {}).get("kept", len(all_cards)),
        "classified": classified_count,
        "summarized": summarized_count,
        "tokens": ledger.tokens_summary(),
        "next_run": NEXT_RUN_LABEL,
        "deep_read": deep_counts,
        "threads_active": len(threads_output),
        "threads_total": len(threads_state.get("threads", [])),
    }
    status.update({"cards_used": ledger.cards_used, "capped": ledger.capped})

    return {
        "schema": "intel-daily-v1",
        "date": date,
        "generated_at": iso(now_utc()),
        "llm": llm_tag,
        "gauges": gauges,
        "brief_zh": brief_zh,
        "flags": flags,
        "cards": finalized,
        "threads": threads_output,
        "calendar": calendar,
        "status": status,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="YYYY-MM-DD, default = today TPE")
    ap.add_argument("--skip-fetch", action="store_true")
    ap.add_argument("--out", default=None, help="override output path (default docs/intel/data/{date}.json)")
    ap.add_argument(
        "--no-llm", action="store_true",
        help="force data-only mode (fetch + deterministic gauges/flags/calendar, "
             "llm:\"unavailable\") even if CLAUDE_CODE_OAUTH_TOKEN is set — for "
             "testing the pipeline without spending sonnet/haiku tokens.",
    )
    args = ap.parse_args()

    date = args.date or _today_tpe()

    if not args.skip_fetch:
        ok = run_fetch(date)
        if not ok:
            print("[intel/run_daily] fetch.py reported failures (see above) — "
                  "continuing with whatever pending JSON it wrote.", file=sys.stderr)

    pending = load_json(pending_path(date))
    if pending is None:
        print(f"[intel/run_daily] FATAL: no pending JSON for {date} at {pending_path(date)} "
              "and could not produce one — cannot build daily JSON.", file=sys.stderr)
        return 1

    llm_available = False if args.no_llm else _llm_available()
    try:
        output = build_output(date, pending, llm_available)
    except Exception as e:  # noqa: BLE001 — even a hard crash in classify/summarize
        # must not stop us from writing *something*, per the "exit 0 unless the
        # JSON truly cannot be produced" contract.
        print(f"[intel/run_daily] ERROR during classify/summarize: {e!r} — "
              "falling back to data-only output.", file=sys.stderr)
        try:
            output = build_output(date, pending, llm_available=False)
            output["llm"] = "error"
        except Exception as e2:  # noqa: BLE001
            print(f"[intel/run_daily] FATAL: even the data-only fallback failed: {e2!r}", file=sys.stderr)
            return 1

    out_path = args.out or str(daily_output_path(date))
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except OSError as e:
        print(f"[intel/run_daily] FATAL: could not write {out_path}: {e!r}", file=sys.stderr)
        return 1

    print(f"[intel/run_daily] wrote {out_path}")
    run_render(date)

    s = output["status"]
    print(
        f"[intel/run_daily] date={date} llm={output['llm']} "
        f"sources_ok={s['sources_ok']}/{s['sources_ok'] + s['sources_fail']} "
        f"fetched={s['fetched']} kept={s['kept']} classified={s['classified']} "
        f"summarized={s['summarized']} tokens(haiku)={s['tokens'].get('haiku', 0)} "
        f"tokens(sonnet)={s['tokens'].get('sonnet', 0)} "
        f"tokens(deepread)={s['tokens'].get('deepread', 0)} cards={len(output['cards'])} "
        f"gauges={len(output['gauges'])} flags={len(output['flags'])} "
        f"calendar={len(output['calendar'])} "
        f"deep_read={s.get('deep_read')} threads_active={s.get('threads_active')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
