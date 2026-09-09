#!/usr/bin/env python3
"""
席位持股階段變化警訊 — zero-LLM daily notifier.

WHAT THIS IS
------------
Not a judgment rule, a notifier: it takes today's docs/engine/arena.json
seats (core_seats + sat_seats + core_bench tickers) and today's
docs/stages/data/lamp.json stage lamp, diffs against the last run's
recorded stage per seat ticker (docs/stages/data/seat_stage_state.json),
and writes a plain-text alert only when a seat ticker's stage crosses the
S0（弱勢）boundary:
  - 進入 S0（任何較高階段 → S0）             → 「警訊」
  - 離開 S0（S0 → 任何較高階段，含 S9 過渡）  → 「解除」
No other stage transition is reported — this only watches the floor.

Stage labels are imported from scripts/build_stages.py's STAGE_NAMES (not
re-typed here), so a future stage added there (e.g. a S5 高檔整理) shows up
automatically instead of silently falling back to the raw code.

STATE: docs/stages/data/seat_stage_state.json = {"as_of", "seats": {TICKER:
stage_code}, "quality": {TICKER: true|false|null}}. First run (no state file)
just writes the baseline — no alert, since there is nothing to compare
against yet. A ticker seen for the first time in the seats set (new seat
since last run) is treated the same way — baseline only, no event — because
there is no genuine "yesterday" for it.

QUALITY-GATE FLIP (2026-09-09, additive — 同一份 ALERT_TXT／同一封信，只是多
幾行)：除了 S0 進出，同一批 seat/bench ticker 也拿 docs/engine/universe_board.json
每列的 quality.pass（ROIC/FCF 品質閘，見 build_arena.py `_universe_board_row`）
跟上次記錄的 state 比對——由過轉未過標「警訊」，由未過轉過標「解除」，跟 S0
事件共用同一套 kind 詞彙、同一個檔案。品質閘資料缺（ticker 不在 board 裡）
比照階段缺資料的作法：沿用舊值不比較、不觸發。

Zero LLM, exit 0 always — this must never fail the workflow it rides in.

Usage: python3 scripts/check_seat_stage_alerts.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_stages import STAGE_NAMES  # noqa: E402 — 階段代碼→白話標籤，不在本檔重複定義

ROOT = Path(__file__).resolve().parent.parent
ARENA_JSON = ROOT / "docs" / "engine" / "arena.json"
LAMP_JSON = ROOT / "docs" / "stages" / "data" / "lamp.json"
STAGES_LATEST_JSON = ROOT / "docs" / "stages" / "data" / "latest.json"
UNIVERSE_BOARD_JSON = ROOT / "docs" / "engine" / "universe_board.json"
STATE_JSON = ROOT / "docs" / "stages" / "data" / "seat_stage_state.json"
ALERT_TXT = ROOT / "docs" / "stages" / "data" / "seat_stage_alert.txt"

S0 = "S0"
ROLE_LABELS = (("核心", "core_seats"), ("衛星", "sat_seats"), ("候補", "core_bench"))


def _load_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def current_seats() -> dict:
    """ticker → {"role", "verdict"}，僅 core_seats/sat_seats/core_bench 三組
    （無 sat_bench 欄位，未坐席挑戰者不算）。同一 ticker 若同時出現在多組
    （理論上不會），先到者優先：核心 > 衛星 > 候補。"""
    arena = _load_json(ARENA_JSON, {}) or {}
    seats: dict[str, dict] = {}
    for role, key in ROLE_LABELS:
        for r in arena.get(key) or []:
            t = r.get("ticker")
            if t and t not in seats:
                seats[t] = {"role": role, "verdict": r.get("verdict")}
    return seats


def dist_52w_high_map() -> dict:
    """ticker → dist_52w_high_pct，來自 stages latest.json 的 rows（該檔只收
    S1-S4，S0/S9 不在列——這正是我們最在意的「剛跌入 S0」事件常拿不到這欄的
    原因，取不到就顯示「—」，不是 bug。"""
    latest = _load_json(STAGES_LATEST_JSON, {}) or {}
    return {r["ticker"]: r.get("dist_52w_high_pct") for r in (latest.get("rows") or [])}


def quality_pass_map() -> dict:
    """ticker → quality.pass（true/false/null），來自 docs/engine/universe_board.json
    每列的 quality 欄（build_arena.py `_universe_board_row` 直接複用 grp.quality，
    見該函式 docstring）——ROIC/FCF 品質閘的當日結果，不重算。"""
    board = _load_json(UNIVERSE_BOARD_JSON, {}) or {}
    out = {}
    for r in board.get("rows") or []:
        t = r.get("ticker")
        if not t:
            continue
        q = r.get("quality") or {}
        out[t] = {"pass": q.get("pass"), "roic": q.get("roic"), "fcf": q.get("fcf")}
    return out


def _fmt_pct(v) -> str:
    return f"{v:+.1f}%" if isinstance(v, (int, float)) else "—"


def _fmt_plain_pct(v) -> str:
    return f"{v:.1f}%" if isinstance(v, (int, float)) else "—"


def _event_line(kind: str, ticker: str, info: dict, prev_stage: str, today_stage: str,
                 dist_pct) -> str:
    prev_name = STAGE_NAMES.get(prev_stage, prev_stage)
    today_name = STAGE_NAMES.get(today_stage, today_stage)
    verdict = info.get("verdict") or "—"
    return (f"{kind}　{ticker}、席位：{info['role']}、{prev_name}→{today_name}、"
            f"距52週高：{_fmt_pct(dist_pct)}、DD裁決：{verdict}")


def _quality_event_line(kind: str, ticker: str, info: dict, prev_pass: bool, today_pass: bool,
                         roic, fcf) -> str:
    verdict = info.get("verdict") or "—"
    trans = "過→未過" if (prev_pass and not today_pass) else "未過→過"
    return (f"{kind}　{ticker}、席位：{info['role']}、品質閘：{trans}、"
            f"ROIC：{_fmt_plain_pct(roic)}、FCF率：{_fmt_plain_pct(fcf)}、DD裁決：{verdict}")


def main() -> int:
    seats = current_seats()
    lamp_doc = _load_json(LAMP_JSON, {}) or {}
    lamp_map = lamp_doc.get("lamp") or {}
    as_of = lamp_doc.get("as_of") or "—"
    dist_map = dist_52w_high_map()
    quality_map = quality_pass_map()

    state = _load_json(STATE_JSON, None)
    first_run = state is None
    prev_seats = (state or {}).get("seats") or {}
    prev_quality = (state or {}).get("quality") or {}

    events: list[str] = []
    new_state_seats: dict[str, str] = {}
    new_state_quality: dict[str, bool | None] = {}
    for ticker in sorted(seats):
        info = seats[ticker]
        today_stage = lamp_map.get(ticker)
        if today_stage is None:
            # 今日拿不到階段（母體外/資料缺）：沿用舊值（若有），不比較不觸發
            if ticker in prev_seats:
                new_state_seats[ticker] = prev_seats[ticker]
        else:
            new_state_seats[ticker] = today_stage
            prev_stage = prev_seats.get(ticker)
            if not (first_run or prev_stage is None or prev_stage == today_stage):
                if prev_stage != S0 and today_stage == S0:
                    events.append(_event_line("警訊", ticker, info, prev_stage, today_stage,
                                               dist_map.get(ticker)))
                elif prev_stage == S0 and today_stage != S0:
                    events.append(_event_line("解除", ticker, info, prev_stage, today_stage,
                                               dist_map.get(ticker)))

        # 品質閘翻轉（2026-09-09，加成，不取代上面的階段事件）——同一批
        # seat/bench ticker，比對 docs/engine/universe_board.json 的
        # quality.pass 跟上次記錄值。board 缺該 ticker（today_q 為 None）：
        # 沿用舊值不比較不觸發，跟階段缺資料同一套處理方式。
        today_q = (quality_map.get(ticker) or {}).get("pass")
        if today_q is None:
            if ticker in prev_quality:
                new_state_quality[ticker] = prev_quality[ticker]
            continue
        new_state_quality[ticker] = today_q
        prev_q = prev_quality.get(ticker)
        if first_run or prev_q is None or prev_q == today_q:
            continue   # 首跑／新入席只建基準；品質閘未變無事件
        qinfo = quality_map.get(ticker) or {}
        if prev_q and not today_q:
            events.append(_quality_event_line("警訊", ticker, info, prev_q, today_q,
                                               qinfo.get("roic"), qinfo.get("fcf")))
        elif not prev_q and today_q:
            events.append(_quality_event_line("解除", ticker, info, prev_q, today_q,
                                               qinfo.get("roic"), qinfo.get("fcf")))

    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATE_JSON.write_text(
        json.dumps({"as_of": as_of, "seats": new_state_seats, "quality": new_state_quality},
                   ensure_ascii=False, indent=1),
        encoding="utf-8")

    if events:
        ALERT_TXT.write_text("\n".join(events) + "\n", encoding="utf-8")
        print(f"seat_stage_alerts: {len(events)} 則事件（as_of {as_of}）→ {ALERT_TXT}")
    else:
        if ALERT_TXT.exists():
            ALERT_TXT.unlink()
        print(f"seat_stage_alerts: 無事件（as_of {as_of}）")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 — 通知器不可擋排程，任何未預期錯誤照樣 exit 0
        print(f"seat_stage_alerts: unexpected error, skipping ({exc!r})")
        sys.exit(0)
