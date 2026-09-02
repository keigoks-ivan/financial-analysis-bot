#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_read_triggers.py — 市況判讀自動觸發判定（stdlib-only）。

背景：`market-read-auto` 雲端 routine 每天固定時間喚醒，但寫一次判讀要花真的
token（冷讀 subagent＋修稿），所以喚醒本身必須幾乎零成本地決定「今天要不要真的
跑」。本檔就是那個零成本判定——純讀既有 JSON／JSONL，不呼叫任何 LLM。
設計稿：`notes/site-internal/root/_market_read_design_20260903.md` §5.1。

觸發條件（任一即 run_read=true）：
  ① 台北週一。
  ② `docs/monitor/data/score_history.json` 的壓力分數 s 較 5 個交易日前變動 ≥10。
  ③ `docs/detective/data/kill_watch.json` 的 `breached` 非空，或
     `docs/market/data/state.json` 的 `fuses[]` 任一 `dist_pct` ≤ 0。
  ④ VIX（`state.json.evidence.quotes["monitor:vix"].num`）≥ 25。
  ⑤ 判讀已過期：today − `read.json.as_of` > `read.json.valid_days`
    （`read.json` 完全不存在時，視同過期＝bootstrap，一併觸發）。
  ⑥ 上次判讀失敗：`docs/market/data/read_status.json` 存在且 status=="failed"
    （隔天由 routine 自然重試，本檔不另外比對日期）。

同一天不重跑（覆蓋以上全部）：若 `read.json.as_of` 等於「今天」，run_read=false，
reason=`already_read_today`。

缺檔／解析失敗一律降級為一則說明性 reason 字串，絕不 crash（唯一的硬性
exit(2) 是 --today 給了無法解析的日期字串，那是使用方式錯誤而非資料缺失）。

用法
----
  python scripts/check_read_triggers.py                 # 人類可讀輸出
  python scripts/check_read_triggers.py --json           # 印 JSON（routine 用）
  python scripts/check_read_triggers.py --today 2026-09-07   # 覆寫「今天」（測試／回放）

輸出（--json）：`{"run_read": bool, "reasons": [...], "as_of": "...", "taipei_date": "..."}`
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "docs" / "market" / "data" / "state.json"
SCORE_HISTORY_FILE = ROOT / "docs" / "monitor" / "data" / "score_history.json"
KILL_WATCH_FILE = ROOT / "docs" / "detective" / "data" / "kill_watch.json"
READ_FILE = ROOT / "docs" / "market" / "data" / "read.json"
READ_STATUS_FILE = ROOT / "docs" / "market" / "data" / "read_status.json"

TAIPEI = timezone(timedelta(hours=8))
STRESS_JUMP_THRESHOLD = 10.0
VIX_THRESHOLD = 25.0


def taipei_today() -> date:
    return datetime.now(TAIPEI).date()


def load_json(path: Path):
    """回傳 (data, error_str)；缺檔或壞檔回傳 (None, 說明字串)，絕不拋例外。"""
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"{path.relative_to(ROOT)} 不存在"
    except (json.JSONDecodeError, OSError) as e:
        return None, f"{path.relative_to(ROOT)} 無法解析：{e}"


def parse_date_loose(s):
    if not isinstance(s, str):
        return None
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        return None


# ═══════════════════════════════════════════════════════════════════════════
# 個別條件檢查：每個回傳 (triggered: bool, reason_or_None: str, notes: list[str])
# notes 是不影響 run_read 的說明性字串（缺檔／降級），一律併入輸出 reasons[]。
# ═══════════════════════════════════════════════════════════════════════════

def check_monday(today: date):
    if today.weekday() == 0:
        return True, f"monday_taipei（{today.isoformat()} 是台北週一）", []
    return False, None, []


def check_stress_jump(today: date):
    data, err = load_json(SCORE_HISTORY_FILE)
    if data is None:
        return False, None, [f"stress_jump_check_skipped：{err}"]
    series = data.get("series")
    if not isinstance(series, list) or not series:
        return False, None, ["stress_jump_check_skipped：score_history.series 為空"]
    rows = [r for r in series if isinstance(r, dict) and parse_date_loose(r.get("d")) and parse_date_loose(r.get("d")) <= today]
    if len(rows) < 6:
        return False, None, ["stress_jump_check_skipped：today 之前交易日不足 6 筆"]
    rows.sort(key=lambda r: r["d"])
    latest, five_back = rows[-1], rows[-6]
    s_latest, s_prior = latest.get("s"), five_back.get("s")
    if not isinstance(s_latest, (int, float)) or not isinstance(s_prior, (int, float)):
        return False, None, ["stress_jump_check_skipped：s 欄缺值"]
    delta = s_latest - s_prior
    if abs(delta) >= STRESS_JUMP_THRESHOLD:
        return True, (f"stress_score_jump（{five_back['d']}→{latest['d']}："
                       f"{s_prior}→{s_latest}，Δ{delta:+.1f}）"), []
    return False, None, []


def check_kill_watch_and_fuses():
    reasons = []
    notes = []
    kw_data, kw_err = load_json(KILL_WATCH_FILE)
    if kw_data is None:
        notes.append(f"kill_watch_check_skipped：{kw_err}")
    else:
        breached = kw_data.get("breached")
        if isinstance(breached, list) and breached:
            names = [b.get("theme") or b.get("id") or str(b) for b in breached][:5]
            reasons.append(f"kill_watch_breached（{len(breached)} 項：{names}）")

    state_data, state_err = load_json(STATE_FILE)
    if state_data is None:
        notes.append(f"fuse_check_skipped：{state_err}")
    else:
        fuses = state_data.get("fuses")
        if isinstance(fuses, list):
            hit = [f for f in fuses if isinstance(f.get("dist_pct"), (int, float)) and f["dist_pct"] <= 0]
            if hit:
                names = [f.get("theme") for f in hit]
                reasons.append(f"fuse_dist_pct_nonpositive（{names}）")
    return reasons, notes


def check_vix():
    data, err = load_json(STATE_FILE)
    if data is None:
        return False, None, [f"vix_check_skipped：{err}"]
    quote = ((data.get("evidence") or {}).get("quotes") or {}).get("monitor:vix")
    if not isinstance(quote, dict) or not isinstance(quote.get("num"), (int, float)):
        return False, None, ["vix_check_skipped：state.json 無 evidence.quotes['monitor:vix'].num"]
    vix = quote["num"]
    if vix >= VIX_THRESHOLD:
        return True, f"vix_ge_25（VIX={vix}）", []
    return False, None, []


def check_read_staleness_and_same_day(today: date):
    """回傳 (already_read_today: bool, stale_trigger: bool, reason_or_None, read_as_of, notes)。"""
    data, err = load_json(READ_FILE)
    if data is None:
        # read.json 完全不存在＝從未判讀過，視為 bootstrap，直接觸發。
        return False, True, f"read_json_missing（{err}，視同過期）", None, []

    as_of = parse_date_loose(data.get("as_of"))
    valid_days = data.get("valid_days")
    if not isinstance(valid_days, (int, float)):
        valid_days = 10
    if as_of is None:
        return False, True, "read_json_as_of_unparseable（視同過期）", data.get("as_of"), []

    if as_of == today:
        return True, False, None, as_of.isoformat(), []

    age = (today - as_of).days
    if age > valid_days:
        return False, True, f"read_stale（as_of={as_of.isoformat()}，已過 {age} 天 > valid_days {valid_days}）", as_of.isoformat(), []
    return False, False, None, as_of.isoformat(), []


def check_prior_failed():
    data, err = load_json(READ_STATUS_FILE)
    if data is None:
        return False, None, []
    if data.get("status") == "failed":
        stage = data.get("stage", "?")
        return True, f"prior_run_failed（stage={stage}，隔天重試）", []
    return False, None, []


def evaluate(today: date):
    reasons = []
    notes = []

    already_today, stale_trigger, stale_reason, read_as_of, stale_notes = check_read_staleness_and_same_day(today)
    notes.extend(stale_notes)

    if already_today:
        return {
            "run_read": False,
            "reasons": ["already_read_today"],
            "as_of": read_as_of,
            "taipei_date": today.isoformat(),
        }

    if stale_trigger:
        reasons.append(stale_reason)

    for check_fn in (check_monday,):
        triggered, reason, ns = check_fn(today)
        notes.extend(ns)
        if triggered:
            reasons.append(reason)

    triggered, reason, ns = check_stress_jump(today)
    notes.extend(ns)
    if triggered:
        reasons.append(reason)

    kw_reasons, kw_notes = check_kill_watch_and_fuses()
    reasons.extend(kw_reasons)
    notes.extend(kw_notes)

    triggered, reason, ns = check_vix()
    notes.extend(ns)
    if triggered:
        reasons.append(reason)

    triggered, reason, ns = check_prior_failed()
    notes.extend(ns)
    if triggered:
        reasons.append(reason)

    all_reasons = reasons + notes
    return {
        "run_read": bool(reasons),
        "reasons": all_reasons,
        "as_of": read_as_of,
        "taipei_date": today.isoformat(),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="輸出 JSON（routine 消費用）")
    ap.add_argument("--today", default=None, help="覆寫『今天』日期 YYYY-MM-DD（測試／回放用；預設台北現在日期）")
    args = ap.parse_args()

    if args.today:
        try:
            today = date.fromisoformat(args.today)
        except ValueError:
            print(f"[check-read-triggers][ERROR] --today 格式錯誤：{args.today!r}，需 YYYY-MM-DD", file=sys.stderr)
            sys.exit(2)
    else:
        today = taipei_today()

    result = evaluate(today)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"台北日期：{result['taipei_date']}　上次判讀 as_of：{result['as_of']}")
        print(f"run_read = {result['run_read']}")
        if result["reasons"]:
            print("reasons：")
            for r in result["reasons"]:
                print(f"  - {r}")
        else:
            print("reasons：（無）")

    sys.exit(0)


if __name__ == "__main__":
    main()
