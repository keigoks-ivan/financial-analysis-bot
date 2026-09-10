#!/usr/bin/env python3
"""
選股主控台名單變化警訊 — zero-LLM daily notifier.

WHAT THIS IS
------------
Not a judgment rule, a notifier: it takes今天 docs/engine/arena.json 的席位
（core_seats + sat_seats + core_bench，恰好就是 /cockpit/ 頁「陣容」表格 render
的同一份 ticker 集合——見 docs/cockpit/index.html renderRoster()，S.arena.core_seats
/sat_seats/core_bench，一字不差），跟上一次記錄的名單（docs/stages/data/
seat_stage_state.json）逐檔比對，主事件＝名單本身的變化：

  ＋ 新增：今天在席位裡、上次不在（含全新入列、或從追蹤外直接空降）
  − 移除：上次在席位裡、今天不在了
  ↔ 換區：兩邊都在，但 role 變了（核心／衛星／候補三組互換）

階段（S0 進出）與品質閘翻轉（見下）仍然照算，但降級為附屬區塊「階段與品質
變化」，跟名單變化共用同一封信、同一個檔案——不是刪掉，只是主從關係倒過來
（2026-09-10 之前，S0 進出才是唯一主事件；改版原因：使用者要看的是「主控台
名單本身」的異動，S0/品質只是名單裡既有 ticker 的體質變化）。

Stage labels are imported from scripts/build_stages.py's STAGE_NAMES (not
re-typed here), so a future stage added there shows up automatically.

STATE SCHEMA (v2, 2026-09-10 bump)
-----------------------------------
docs/stages/data/seat_stage_state.json = {
  "as_of": "YYYY-MM-DD",
  "seats": {TICKER: {"section": "核心"|"衛星"|"候補", "stage": "Sx"}},
  "quality": {TICKER: true|false|null}
}

v1 相容：v1 的 "seats" value 是純字串（stage code，沒有 section）。讀到字串
value 時視為「section 未知」，只補建 section（不補比較），不會因此噴出一批
假的換區事件——換句話說，schema 換版後第一次跑：
  - ticker 集合的新增／移除照常比對（v1 state 本來就有完整的 ticker key 集合，
    這件事沒有因為 schema 換版而變得不可信）
  - 換區事件不比（因為不知道 v1 時代每檔的 section 是什麼，只能先補建）
  - S0 進出／品質翻轉沿用原邏輯（v1 的 stage code 本來就在，可以正常比較）

FIRST RUN（完全沒有 state 檔）＝ baseline only，什麼事件都不觸發（沒有基準
可比）。

QUALITY-GATE FLIP（2026-09-09 加入，本次改版只是移到附屬區塊，邏輯不動）：
同一批 seat/bench ticker 拿 docs/engine/universe_board.json 每列的
quality.pass（ROIC/FCF 品質閘，見 build_arena.py `_universe_board_row`）跟
上次記錄的 state 比對，由過轉未過標「警訊」，由未過轉過標「解除」。品質閘
資料缺（ticker 不在 board 裡）比照階段缺資料的作法：沿用舊值不比較、不觸發。

--dry-run：印出今天各 section 的名單與將要送出的事件/信件內容，不寫
STATE_JSON、不寫 ALERT_TXT。

Zero LLM, exit 0 always — this must never fail the workflow it rides in.

Usage: python3 scripts/check_seat_stage_alerts.py [--dry-run]
"""
from __future__ import annotations

import argparse
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
COCKPIT_URL = "https://research.investmquest.com/cockpit/"

S0 = "S0"
ROLE_LABELS = (("核心", "core_seats"), ("衛星", "sat_seats"), ("候補", "core_bench"))


def _load_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def current_seats() -> dict:
    """ticker → {"role", "verdict"}，僅 core_seats/sat_seats/core_bench 三組
    （無 sat_bench 欄位，未坐席挑戰者不算）——這正是 /cockpit/ 頁「陣容」表格
    render 的同一份集合（docs/cockpit/index.html renderRoster()）。同一 ticker
    若同時出現在多組（理論上不會），先到者優先：核心 > 衛星 > 候補。"""
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


def _split_prev(value):
    """v2 value 是 {"section", "stage"}；v1 value 是純 stage code 字串（沒有
    section，視為未知，只補建不比較）；缺值回傳 (None, None)。"""
    if isinstance(value, dict):
        return value.get("section"), value.get("stage")
    if isinstance(value, str):
        return None, value
    return None, None


def _fmt_pct(v) -> str:
    return f"{v:+.1f}%" if isinstance(v, (int, float)) else "—"


def _fmt_plain_pct(v) -> str:
    return f"{v:.1f}%" if isinstance(v, (int, float)) else "—"


def _added_line(ticker: str, section: str, today_stage) -> str:
    stage = today_stage or "—"
    name = STAGE_NAMES.get(today_stage, "") if today_stage else ""
    return f"＋ 新增 {ticker}（{section}）· 今日階段 {stage} {name}".rstrip()


def _removed_line(ticker: str, prev_section, prev_stage) -> str:
    section = prev_section or "—"
    stage = prev_stage or "—"
    return f"− 移除 {ticker}（原 {section}）· 最後階段 {stage}"


def _switch_line(ticker: str, prev_section: str, today_section: str) -> str:
    return f"↔ {ticker}：{prev_section} → {today_section}"


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


def compute() -> dict:
    """算出今天的席位、事件與新 state；不寫任何檔案（供 --dry-run 與正式寫檔共用）。"""
    seats = current_seats()
    lamp_doc = _load_json(LAMP_JSON, {}) or {}
    lamp_map = lamp_doc.get("lamp") or {}
    as_of = lamp_doc.get("as_of") or "—"
    dist_map = dist_52w_high_map()
    quality_map = quality_pass_map()

    state = _load_json(STATE_JSON, None)
    first_run = state is None
    prev_seats_raw = (state or {}).get("seats") or {}
    prev_quality = (state or {}).get("quality") or {}
    prev_tickers = set(prev_seats_raw.keys())
    current_tickers = set(seats.keys())

    primary_events: list[str] = []
    secondary_events: list[str] = []
    new_state_seats: dict[str, dict] = {}
    new_state_quality: dict[str, bool | None] = {}

    if not first_run:
        for ticker in sorted(current_tickers - prev_tickers):
            info = seats[ticker]
            primary_events.append(_added_line(ticker, info["role"], lamp_map.get(ticker)))
        for ticker in sorted(prev_tickers - current_tickers):
            prev_section, prev_stage = _split_prev(prev_seats_raw.get(ticker))
            primary_events.append(_removed_line(ticker, prev_section, prev_stage))

    for ticker in sorted(seats):
        info = seats[ticker]
        today_stage = lamp_map.get(ticker)
        prev_section, prev_stage = _split_prev(prev_seats_raw.get(ticker))

        if today_stage is None:
            # 今日拿不到階段（母體外/資料缺）：沿用舊 stage（若有），section 仍用今天的
            if ticker in prev_seats_raw:
                new_state_seats[ticker] = {"section": info["role"], "stage": prev_stage}
        else:
            new_state_seats[ticker] = {"section": info["role"], "stage": today_stage}
            if not (first_run or prev_stage is None or prev_stage == today_stage):
                if prev_stage != S0 and today_stage == S0:
                    secondary_events.append(_event_line("警訊", ticker, info, prev_stage,
                                                          today_stage, dist_map.get(ticker)))
                elif prev_stage == S0 and today_stage != S0:
                    secondary_events.append(_event_line("解除", ticker, info, prev_stage,
                                                          today_stage, dist_map.get(ticker)))

        # 換區：兩邊都在、上次 section 已知（v2 state）、且變了
        if (not first_run and ticker in prev_tickers and prev_section is not None
                and prev_section != info["role"]):
            primary_events.append(_switch_line(ticker, prev_section, info["role"]))

        # 品質閘翻轉（見檔頭說明）——board 缺該 ticker（today_q 為 None）：
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
            secondary_events.append(_quality_event_line("警訊", ticker, info, prev_q, today_q,
                                                          qinfo.get("roic"), qinfo.get("fcf")))
        elif not prev_q and today_q:
            secondary_events.append(_quality_event_line("解除", ticker, info, prev_q, today_q,
                                                          qinfo.get("roic"), qinfo.get("fcf")))

    new_state = {"as_of": as_of, "seats": new_state_seats, "quality": new_state_quality}
    return {
        "seats": seats,
        "as_of": as_of,
        "first_run": first_run,
        "primary_events": primary_events,
        "secondary_events": secondary_events,
        "new_state": new_state,
    }


def build_alert_body(as_of: str, primary_events: list[str], secondary_events: list[str]) -> str | None:
    if not primary_events and not secondary_events:
        return None
    body_lines: list[str] = []
    if primary_events:
        body_lines.extend(primary_events)
    if secondary_events:
        if body_lines:
            body_lines.append("")
        body_lines.append("階段與品質變化")
        body_lines.extend(secondary_events)
    full = [f"🧭 選股主控台名單變化 {as_of}", ""] + body_lines + ["", f"詳見 {COCKPIT_URL}"]
    return "\n".join(full) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                         help="印出今天名單與將發生的事件，不寫 state／alert 檔")
    args = parser.parse_args(argv)

    result = compute()
    seats = result["seats"]
    as_of = result["as_of"]
    primary_events = result["primary_events"]
    secondary_events = result["secondary_events"]
    body = build_alert_body(as_of, primary_events, secondary_events)

    if args.dry_run:
        print(f"[dry-run] as_of={as_of}（first_run={result['first_run']}）")
        for role, _key in ROLE_LABELS:
            tickers = sorted(t for t, i in seats.items() if i["role"] == role)
            print(f"[dry-run] {role}（{len(tickers)}）：{'、'.join(tickers) if tickers else '（無）'}")
        if body:
            print(f"[dry-run] 將寫入 {len(primary_events)} 則名單事件、"
                  f"{len(secondary_events)} 則階段/品質事件 → {ALERT_TXT}")
            print("[dry-run] ---- alert body ----")
            print(body, end="")
            print("[dry-run] ---------------------")
        else:
            print(f"[dry-run] 無事件（as_of {as_of}）— 不會寫 alert 檔")
        print("[dry-run] state 檔未寫入（--dry-run 不落地任何變更）")
        return 0

    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATE_JSON.write_text(json.dumps(result["new_state"], ensure_ascii=False, indent=1),
                           encoding="utf-8")

    if body:
        ALERT_TXT.write_text(body, encoding="utf-8")
        print(f"seat_stage_alerts: {len(primary_events)} 則名單事件、"
              f"{len(secondary_events)} 則階段/品質事件（as_of {as_of}）→ {ALERT_TXT}")
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
