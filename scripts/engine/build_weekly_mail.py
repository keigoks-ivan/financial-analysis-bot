#!/usr/bin/env python3
"""每週選股結果 email — 席位擂台前後週對比＋換席原因＋候補／爆發榜／十倍榜／帳簿記分／看板節錄
（供 weekly-engine.yml 寄信用；2026-09 起由「席位擂台週報」擴充為完整版週報，同一寄信步驟）。

跑在 weekly-engine.yml 的「Commit and push if changed」步驟**之前**（此時 HEAD 仍是
上週版本），所以前後週對比不靠 arena-ledger.json 是否剛好記了這期，而是自己算：

  本週陣容 = docs/engine/arena.json（working tree，本次 build 已跑完）
  上週陣容 = `git show HEAD:docs/engine/arena.json`（commit 前 HEAD 仍是上週版本）
             或 PREV_ARENA_JSON=<path> 環境變數覆寫（本地測試用）

換出原因是機械推導、不是 LLM 生成：對每個換出 ticker 在本週 arena 找下落——
  1. 還在 core_bench[] / challengers_top[]（衛星向 bench 沒有獨立輸出，併在
     challengers_top 裡）且 grp.pass=false → 引其 grp.why[] 第一條白話轉寫
  2. 還在合格池（grp.pass=true 且 verdict=進場）但名次被擠出前五 → 分數對照末席門檻
  3. verdict 不再是「進場」 → DD 裁決轉向，失去席位資格
  4. 全站找不到（含 dd-screener latest.json 查無紀錄）→ 跌出資格池
查無明確原因時誠實寫「機械層未留下具體原因」，不捏造。

本週選股結果其餘各段（候補／無 DD 機械過閘／爆發正式榜／十倍榜／帳簿記分／看板節錄）
全部讀既有機械輸出檔，不重新判斷、不捏造數字；來源檔缺失時該段落寫「本週無資料」，
不中止整封信（僅 docs/engine/arena.json 缺失才視為無法組信，exit 非零）。

Email 版型依 notes/site-internal/root/_market_read_design_20260903.md §5.7 的共用信件
版型標準（600px 置中白卡、頂欄深藍、一分鐘版、數字磚、金色小標題、斑馬表、狀態色票）。

輸出：engine_weekly_mail.html（repo 根目錄）＋ engine_weekly_mail_subject.txt（一行主旨）。
任何輸入缺失導致無法組信 → exit 非零（workflow 據此跳過寄信步驟）。
Usage: python3 scripts/engine/build_weekly_mail.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ARENA_JSON = ROOT / "docs" / "engine" / "arena.json"
LEDGER_JSON = ROOT / "docs" / "engine" / "arena-ledger.json"
BOARD_TXT = ROOT / "docs" / "engine" / "board.txt"
DD_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
CANDIDATES_JSON = ROOT / "docs" / "picks" / "candidates.json"
TENBAGGER_JSON = ROOT / "docs" / "picks" / "tenbagger.json"
SOP_FUNNEL_JSON = ROOT / "docs" / "dd-screener" / "sop-funnel" / "latest.json"
SCORECARD_JSON = ROOT / "docs" / "flowmap" / "data" / "scorecard.json"
OUT_HTML = ROOT / "engine_weekly_mail.html"
OUT_SUBJECT = ROOT / "engine_weekly_mail_subject.txt"

TRACK_LABEL = {"core": "核心", "sat": "衛星"}
P_LABEL_TXT = {"breakout": "突破帶", "pullback": "回踩", "in_trend": "趨勢內",
               "overheated": "過熱"}
P_LABEL_DOT = {"breakout": "🟢", "pullback": "🟢", "in_trend": "🟡", "overheated": "🟠"}
LEDGER_SOURCES = [("grp-seat", "三閘評分（GRP）席位"), ("own-board", "擁有層全榜"),
                  ("picks-baofa", "爆發候選"), ("picks-late", "爆發晚段候選"),
                  ("mech-nodd", "無 DD 機械過閘"), ("sop-funnel", "機械板機（狀態機）")]

# ── 版型 tokens（notes/site-internal/root/_market_read_design_20260903.md §5.7）──
BG_PAGE = "#f6f5f2"
CARD_BORDER = "#e6e2d8"
NAVY = "#0f1f3d"
GOLD = "#8a6d1f"
ZEBRA = "#faf9f6"
TEXT_DARK = "#1c1c1c"
TEXT_GRAY = "#6b6b6b"
FONT_STACK = ("-apple-system,BlinkMacSystemFont,'PingFang TC','Noto Sans TC',"
              "'Segoe UI',sans-serif")
SERIF_STACK = "Georgia,'Noto Serif TC',serif"
PILL_COLORS = {"green": ("#e8f3ea", "#1f6b3a"), "red": ("#fbe9e7", "#b3261e"),
               "gray": ("#f0eee9", "#5a5a5a")}


# ── 資料載入 ────────────────────────────────────────────────────────────
def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def load_prev_arena() -> dict | None:
    override = os.environ.get("PREV_ARENA_JSON")
    if override:
        return load_json(Path(override))
    try:
        out = subprocess.run(["git", "show", "HEAD:docs/engine/arena.json"],
                             cwd=ROOT, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return None


# ── 換出原因（機械推導）────────────────────────────────────────────────
def humanize_why(raw: str | None) -> str:
    if not raw:
        return "機械層未留下具體原因"
    if raw.startswith("市值資料缺漏"):
        return raw
    if raw.startswith("市值"):
        return f"市值不足（{raw}）"
    if raw.startswith("上修閘否決") or raw.startswith("上修閘保守否決"):
        return raw
    if raw.startswith("上修閘未過"):
        return f"EPS 預估上修未達標（{raw}）"
    if raw.startswith("成長閘未過"):
        return f"成長動能未達標（{raw}）"
    return raw


def build_pool(arena: dict) -> dict[str, dict]:
    """本週 arena.json 全部找得到的列（席位＋板凳＋挑戰者），ticker → row。"""
    pool: dict[str, dict] = {}
    for key in ("core_seats", "sat_seats", "core_bench", "challengers_top"):
        for row in arena.get(key) or []:
            t = row.get("ticker")
            if t and t not in pool:
                pool[t] = row
    return pool


def dd_screener_verdict(ticker: str) -> str | None:
    data = load_json(DD_LATEST)
    if not data:
        return None
    for s in data.get("stocks") or []:
        if s.get("ticker") == ticker:
            return s.get("dca_verdict")
    return None


def seat_threshold(arena: dict, track: str) -> tuple[float | None, str | None]:
    seats = arena.get("core_seats" if track == "core" else "sat_seats") or []
    if not seats:
        return None, None
    last = seats[-1]
    return last.get("score"), last.get("ticker")


def exit_reason(ticker: str, track: str, arena: dict) -> str:
    pool = build_pool(arena)
    row = pool.get(ticker)
    if row is not None:
        grp = row.get("grp") or {}
        if grp.get("pass") is False:
            why0 = (grp.get("why") or [None])[0]
            return humanize_why(why0)
        verdict = row.get("verdict")
        if verdict and verdict != "進場":
            return f"DD 裁決轉{verdict}，失去席位資格"
        # grp.pass=true 且 verdict=進場，但未坐席 → 分數被擠下
        thresh, thresh_ticker = seat_threshold(arena, track)
        score = row.get("score")
        if thresh is not None and score is not None:
            extra = f"（現末席 {thresh_ticker}）" if thresh_ticker else ""
            return f"分數被擠下——現 {score:.2f} 分，末席門檻 {thresh:.2f} 分{extra}"
        return "機械層未留下具體原因"
    # 本週 arena.json 全站找不到 → 查 dd-screener latest.json 的裁決
    verdict = dd_screener_verdict(ticker)
    if verdict is None:
        return "跌出資格池（本週雷達／dd-screener 無此檔合格紀錄）"
    if verdict != "進場":
        return f"DD 裁決轉{verdict}，失去席位資格"
    return ("機械層未留下具體原因（DD 裁決仍為進場，但明確名次未收錄於本週擂台"
            "候選前 15 名內，機械層截斷）")


# ── 擁有層四值：core_seats/sat_seats/core_bench/challengers_top 巢狀 grp，
#    own_board 扁平欄位，兩種 schema 統一擷取 ─────────────────────────────
def own_layer(row: dict) -> dict:
    grp = row.get("grp")
    if isinstance(grp, dict):
        own = grp.get("own") or {}
        return {"g": grp.get("g"), "ey": own.get("ey"), "roic": row.get("roic"),
                "p_label": grp.get("p_label"), "pass": grp.get("pass"),
                "score": row.get("score")}
    return {"g": row.get("g"), "ey": row.get("ey"), "roic": row.get("roic"),
            "p_label": row.get("p_label"), "pass": row.get("pass"),
            "score": row.get("score")}


def timing_txt(p_label) -> str:
    return f"{P_LABEL_DOT.get(p_label, '🔴')}{P_LABEL_TXT.get(p_label, '52 週線下或缺')}"


# ── 換入 / 全陣容 入選原因 ─────────────────────────────────────────────
def entry_reason(row: dict, seat_no: int) -> str:
    ol = own_layer(row)
    g_txt = f"{ol['g']:.1f}%" if isinstance(ol['g'], (int, float)) else "—"
    grp = row.get("grp") or {}
    r = grp.get("r_fy1")
    r_txt = f"{r:+.1f}%" if isinstance(r, (int, float)) else "—"
    p_label = P_LABEL_TXT.get(ol["p_label"], "52 週線下或缺")
    score_txt = f"{ol['score']:.2f}" if isinstance(ol['score'], (int, float)) else "—"
    return (f"DD 裁決進場，{row.get('route_why') or '護城河資料缺'}。"
            f"三閘：成長 {g_txt}／預估上修 {r_txt}／位置 {p_label}。"
            f"本週第 {seat_no} 名，分數 {score_txt}。")


# ── 前後週差異 ──────────────────────────────────────────────────────────
def diff_track(prev_tickers: list[str], cur_tickers: list[str]) -> tuple[list[str], list[str]]:
    prev_set, cur_set = set(prev_tickers), set(cur_tickers)
    ins = [t for t in cur_tickers if t in cur_set - prev_set]
    outs = [t for t in prev_tickers if t in prev_set - cur_set]
    return ins, outs


def duel_alerts(arena: dict) -> list[tuple[str, str, float, float]]:
    out = []
    for d in arena.get("duels") or []:
        if not d.get("alert"):
            continue
        seat, chal = d.get("seat") or {}, d.get("challenger") or {}
        out.append((seat.get("ticker"), chal.get("ticker"), chal.get("score"), seat.get("score")))
    return out


# ── 小工具：格式化 ──────────────────────────────────────────────────────
def fmt1(v) -> str:
    return f"{v:.1f}" if isinstance(v, (int, float)) else "—"


def fmt_pct1(v) -> str:
    return f"{v:.1f}%" if isinstance(v, (int, float)) else "—"


def fmt_signed_pct1(v) -> str:
    return f"{v:+.1f}%" if isinstance(v, (int, float)) else "—"


def fmt2(v) -> str:
    return f"{v:.2f}" if isinstance(v, (int, float)) else "—"


# ── HTML 渲染組件（inline CSS，Gmail 相容；市況判讀共用信件版型 §5.7）────
def pill(text: str, kind: str) -> str:
    bg, fg = PILL_COLORS.get(kind, PILL_COLORS["gray"])
    # 短字（新進／留任／離席／通過…）才鎖 nowrap；長字（帳簿記分的 status_label 這類
    # 「🟡 證據累積中（n_eff=0／20，LLR=0）」）任其換行，否則會把窄螢幕表格撐爆。
    nowrap = "white-space:nowrap;" if len(text) <= 8 else ""
    return (f'<span style="display:inline-block;background:{bg};color:{fg};'
            f'font-size:11.5px;font-weight:700;padding:2px 9px;border-radius:999px;'
            f'{nowrap}">{escape(text)}</span>')


def hyst_text(hyst: str | None) -> str:
    """遲滯狀態原始文字可能偏長（如「候補·待第 2 次過閘（1/2）」），不套 nowrap 的
    色票 pill（會撐開窄螢幕表格），改用可換行的小字灰字呈現。"""
    return f'<span style="color:{TEXT_GRAY};font-size:11px;">{escape(hyst or "—")}</span>'


def section_header(eng: str, zh: str) -> str:
    return (f'<div style="margin:28px 0 10px;">'
            f'<div style="font-size:11px;letter-spacing:.08em;text-transform:uppercase;'
            f'color:{GOLD};font-weight:700;">{escape(eng)}</div>'
            f'<div style="font-size:16.5px;font-weight:700;color:{TEXT_DARK};'
            f'font-family:{SERIF_STACK};margin-top:2px;">{escape(zh)}</div></div>')


TH_STYLE = (f"background:#eeece4;color:#4a4a42;font-size:11px;text-transform:uppercase;"
            f"letter-spacing:.02em;padding:8px 9px;text-align:left;border-bottom:1px solid {CARD_BORDER};")


def _th(label: str, align: str = "left") -> str:
    al = "text-align:right;" if align == "right" else ""
    return f'<th style="{TH_STYLE}{al}">{escape(label)}</th>'


def _td(html_val: str, zebra: bool, align: str = "left") -> str:
    bg = ZEBRA if zebra else "#ffffff"
    al = "text-align:right;" if align == "right" else ""
    return (f'<td style="padding:7px 9px;border-bottom:1px solid #f0eee6;font-size:12.5px;'
            f'color:{TEXT_DARK};background:{bg};{al}">{html_val}</td>')


def render_table(headers: list[tuple[str, str]], rows: list[list[str]]) -> str:
    """headers: [(label, align)]；rows: 每列已是 HTML-safe 字串（呼叫端自行 escape）。"""
    head = "".join(_th(h, a) for h, a in headers)
    body = []
    for i, row in enumerate(rows):
        zebra = i % 2 == 1
        cells = "".join(_td(v, zebra, a) for (_, a), v in zip(headers, row))
        body.append(f"<tr>{cells}</tr>")
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="border-collapse:collapse;margin:0 0 18px;background:#ffffff;'
            f'border:1px solid {CARD_BORDER};border-radius:6px;overflow:hidden;">'
            f'<tr>{head}</tr>' + "".join(body) + "</table>")


def render_top_bar(report_date: str) -> str:
    return (f'<div style="background:{NAVY};padding:20px 24px;border-radius:8px 8px 0 0;">'
            f'<div style="font-family:{SERIF_STACK};font-size:19px;font-weight:700;'
            f'color:#ffffff;">📋 每週選股結果</div>'
            f'<div style="font-size:12.5px;color:#c9d4e8;margin-top:4px;">'
            f'{escape(report_date)}（台北時間）</div></div>')


def render_one_minute(bullets: list[str]) -> str:
    items = "".join(f'<li style="margin:0 0 8px;">{b}</li>' for b in bullets)
    return (f'<div style="background:#fbf8f1;border:1px solid {CARD_BORDER};border-radius:6px;'
            f'padding:14px 18px;margin:18px 0;">'
            f'<div style="font-size:11px;letter-spacing:.08em;text-transform:uppercase;'
            f'color:{GOLD};font-weight:700;margin-bottom:6px;">ONE-MINUTE VERSION</div>'
            f'<div style="font-size:14px;font-weight:700;color:{TEXT_DARK};margin-bottom:6px;">'
            f'一分鐘版</div>'
            f'<ul style="margin:0;padding-left:18px;font-size:13.5px;line-height:1.65;'
            f'color:#333;">{items}</ul></div>')


def render_tiles(tiles: list[tuple[str, str]]) -> str:
    cells = "".join(
        f'<td width="33%" style="padding:4px;">'
        f'<div style="background:#ffffff;border:1px solid {CARD_BORDER};border-radius:8px;'
        f'padding:14px 6px;text-align:center;">'
        f'<div style="font-size:22px;font-weight:700;color:{NAVY};font-family:{SERIF_STACK};">'
        f'{escape(v)}</div>'
        f'<div style="font-size:11px;color:{TEXT_GRAY};margin-top:4px;">{escape(l)}</div>'
        f'</div></td>' for v, l in tiles)
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:0 0 4px;"><tr>{cells}</tr></table>')


def render_alert_box(kind: str, tag: str, html_body: str) -> str:
    styles = {
        "in": ("#f4faf5", "#1f6b3a", "green"),
        "out": ("#fdf6f5", "#b3261e", "red"),
        "neutral": ("#f7f5ef", "#8a8578", "gray"),
    }
    bg, border, pk = styles[kind]
    return (f'<div style="background:{bg};border-left:3px solid {border};padding:10px 14px;'
            f'margin:0 0 10px;font-size:13px;color:#333;line-height:1.7;">'
            f'{pill(tag, pk)} {html_body}</div>')


# ── §3 席位表 ────────────────────────────────────────────────────────────
def week_status_pill(t: str, prev_rank: dict, cur_rank: int, degrade: bool) -> str:
    if degrade:
        return pill("首週", "gray") + '<div style="color:#9a968a;font-size:11px;margin-top:3px;">無前週資料</div>'
    pr = prev_rank.get(t)
    if pr is None:
        return pill("新進", "green")
    if pr == cur_rank:
        return pill("留任", "gray")
    arrow = "↑" if pr > cur_rank else "↓"
    return (pill("留任", "gray")
            + f'<div style="color:#9a968a;font-size:11px;margin-top:3px;">{arrow} 第{pr}→{cur_rank}名</div>')


def render_seat_table(cur_rows: list[dict], vacant_n: int, track_label: str,
                       prev_tickers: list[str], out_tickers: list[str],
                       degrade: bool, arena: dict, track: str) -> str:
    # 窄螢幕（375px）友善：5 欄，數字/DD/遲滯疊行顯示，避免橫向溢出。
    headers = [("Ticker", "left"), ("擁有層分", "right"), ("時機燈", "left"),
               ("DD 標籤／遲滯狀態", "left"), ("與上週對照", "left")]
    prev_rank = {t: i + 1 for i, t in enumerate(prev_tickers)}
    rows = []
    for i, row in enumerate(cur_rows, 1):
        ol = own_layer(row)
        grp3 = f"成長 {fmt1(ol['g'])}／殖利率 {fmt1(ol['ey'])}／ROIC {fmt1(ol['roic'])}"
        ticker_cell = (f'<div style="color:{TEXT_GRAY};font-size:10.5px;">{escape(track_label)}{i}</div>'
                       f'<strong>{escape(row["ticker"])}</strong>')
        score_cell = (f'<div style="font-weight:700;">{fmt2(ol["score"])}</div>'
                      f'<div style="color:{TEXT_GRAY};font-size:10.5px;">{escape(grp3)}</div>')
        dd_cell = (f'<div style="font-size:12px;">{escape(row.get("dd_tag") or "—")}</div>'
                   f'<div style="margin-top:2px;">{hyst_text(row.get("hyst"))}</div>')
        rows.append([ticker_cell, score_cell, escape(timing_txt(ol["p_label"])), dd_cell,
                     week_status_pill(row["ticker"], prev_rank, i, degrade)])
    for v in range(1, vacant_n + 1):
        vacant_cell = (f'<div style="color:{TEXT_GRAY};font-size:10.5px;">'
                       f'{escape(track_label)}{len(cur_rows) + v}</div>（空位）')
        rows.append([vacant_cell, "—", "—", "—", pill("空位", "gray")])
    if not degrade:
        for t in out_tickers:
            out_cell = (f'<strong style="text-decoration:line-through;color:#b3261e;">'
                        f'{escape(t)}</strong>')
            rows.append([out_cell, "—", "—", "—", pill("離席", "red")])
    return render_table(headers, rows)


# ── 主流程 ──────────────────────────────────────────────────────────────
def main() -> int:
    arena = load_json(ARENA_JSON)
    if not arena or not isinstance(arena.get("core_seats"), list) \
            or not isinstance(arena.get("sat_seats"), list):
        print("::error:: 無法讀取本週 docs/engine/arena.json（缺檔或格式不符），無法組信。",
              file=sys.stderr)
        return 1

    core_cur = arena.get("core_seats") or []
    sat_cur = arena.get("sat_seats") or []
    cur_core_tickers = [r["ticker"] for r in core_cur]
    cur_sat_tickers = [r["ticker"] for r in sat_cur]
    sat_vacant = arena.get("sat_vacant") or 0
    universe_n = arena.get("universe_n")

    prev_arena = load_prev_arena()
    degrade = prev_arena is None or prev_arena == arena

    core_in: list[str] = []
    core_out: list[str] = []
    sat_in: list[str] = []
    sat_out: list[str] = []
    prev_core_tickers: list[str] = []
    prev_sat_tickers: list[str] = []
    if not degrade:
        prev_core_tickers = [r["ticker"] for r in (prev_arena.get("core_seats") or [])]
        prev_sat_tickers = [r["ticker"] for r in (prev_arena.get("sat_seats") or [])]
        core_in, core_out = diff_track(prev_core_tickers, cur_core_tickers)
        sat_in, sat_out = diff_track(prev_sat_tickers, cur_sat_tickers)

    has_changes = bool(core_in or core_out or sat_in or sat_out)
    changed_tickers = set(core_in) | set(core_out) | set(sat_in) | set(sat_out)

    # ── 日期 ──
    taipei_now = datetime.now(timezone.utc) + timedelta(hours=8)
    report_date = taipei_now.strftime("%Y-%m-%d")
    ledger = load_json(LEDGER_JSON)
    data_as_of = None
    if ledger and ledger.get("snapshots"):
        data_as_of = ledger["snapshots"][-1].get("date")
    if not data_as_of:
        data_as_of = (arena.get("regime") or {}).get("as_of") \
            or (arena.get("run_timestamp") or "—")[:10]

    # ── 讀取其餘資料源（缺檔不致命，段落各自降級）──
    candidates = load_json(CANDIDATES_JSON)
    tenbagger = load_json(TENBAGGER_JSON)
    sop_funnel = load_json(SOP_FUNNEL_JSON)
    scorecard = load_json(SCORECARD_JSON)
    board_lines: list[str] = []
    try:
        board_lines = BOARD_TXT.read_text(encoding="utf-8").splitlines()
    except OSError:
        board_lines = []

    official_baofa = (candidates or {}).get("official_baofa") or []
    baofa_pool = (candidates or {}).get("baofa") or []
    late_cycle = [r for r in baofa_pool if r.get("late_cycle")]
    tenbagger_official = (tenbagger or {}).get("official") or []
    tenbagger_as_of = (tenbagger or {}).get("as_of")

    own_board = arena.get("own_board") or []
    mech_nodd = [r for r in own_board if r.get("src") != "dd-pool" and r.get("pass")]

    today_signals = (sop_funnel or {}).get("today_signals") if sop_funnel is not None else None

    # ── §subject 用數字 ──
    n_core, n_sat = len(core_cur), len(sat_cur)
    n_baofa = len(official_baofa)
    n_tenbagger = len(tenbagger_official)
    k_change = len(changed_tickers)
    change_txt = "首週" if degrade else str(k_change)

    subject = (f"📋 每週選股結果 {report_date}｜核心 {n_core}/5 · 衛星 {n_sat}/5 · "
               f"爆發 {n_baofa} · 十倍 {n_tenbagger}｜換席 {change_txt}")

    # ── 一分鐘版三句 ──
    sent1 = ("本週核心與衛星席位由「三閘評分」（GRP：成長閘×上修閘×位置閘）換算出的"
             "<strong>擁有層分</strong>排序決定——看成長速度與盈餘殖利率，ROIC 高有加分、"
             "本益成長比過高會扣分；<strong>時機燈</strong>（突破帶／回踩／趨勢內／過熱／"
             "52 週線下）只做標示、不參與排序；DD 報告只負責否決不合格公司，或標示"
             "核心／衛星角色。")
    if degrade:
        sent2 = "本週<strong>無前週資料可比</strong>，暫無法判定換席（HEAD 上無可對照的上週擂台紀錄）。"
    elif has_changes:
        bits = []
        if core_in or core_out:
            bits.append(f'核心入 {"、".join(core_in) or "—"}／出 {"、".join(core_out) or "—"}')
        if sat_in or sat_out:
            bits.append(f'衛星入 {"、".join(sat_in) or "—"}／出 {"、".join(sat_out) or "—"}')
        sent2 = f'本週<strong>換席 {k_change} 檔</strong>——' + "；".join(bits) + "，原因見下段機械推導。"
    else:
        sent2 = "本週<strong>無換席</strong>，陣容與上週相同。"
    sent3 = (f"本週母體 <strong>{universe_n if universe_n is not None else '—'} 檔</strong>"
             f"（美股含 ADR，不含 .TW 台股另建名單）。")

    # ── 三顆數字磚 ──
    tiles = render_tiles([
        (f"{n_core}/5", "核心席滿員數"),
        (change_txt if degrade else f"{k_change} 檔", "本週換席"),
        (str(n_baofa), "爆發正式榜"),
    ])

    # ── §SEAT ROSTER ──
    core_section = (f'<div style="font-size:13px;color:{TEXT_GRAY};margin:0 0 6px;">'
                     f'核心席（{n_core}/5）</div>'
                     + render_seat_table(core_cur, 0, "核心", prev_core_tickers, core_out,
                                          degrade, arena, "core"))
    sat_section = (f'<div style="font-size:13px;color:{TEXT_GRAY};margin:0 0 6px;">'
                    f'衛星席（{n_sat}/5，空缺 {sat_vacant}）</div>'
                    + render_seat_table(sat_cur, sat_vacant, "衛星", prev_sat_tickers, sat_out,
                                         degrade, arena, "sat"))
    section_roster = (section_header("SEAT ROSTER", "核心席／衛星席")
                       + core_section + sat_section)

    # ── §SEAT CHANGES ──
    if degrade or not has_changes:
        alerts = duel_alerts(arena)
        extra = ""
        if alerts and not degrade:
            alert_lines = "；".join(f'{c} 挑戰者分數已超車在席者 {s}（{cs:.2f} vs {ss:.2f}）'
                                    for s, c, cs, ss in alerts if s and c
                                    and cs is not None and ss is not None)
            if alert_lines:
                extra = f'但 {alert_lines}，下週留意。'
        msg = "本週無前週資料可比，暫無法判定換席。" if degrade else "本週無換席，陣容與上週相同。"
        section_changes = render_alert_box("neutral", "首週" if degrade else "無換席",
                                            escape(msg) + extra)
    else:
        core_in_rows = [(row, i + 1) for i, row in enumerate(core_cur) if row["ticker"] in core_in]
        sat_in_rows = [(row, i + 1) for i, row in enumerate(sat_cur) if row["ticker"] in sat_in]
        parts = []
        for label, in_rows, outs, track in (("核心", core_in_rows, core_out, "core"),
                                             ("衛星", sat_in_rows, sat_out, "sat")):
            for row, seat_no in in_rows:
                parts.append(render_alert_box(
                    "in", "新進",
                    f'<strong>{escape(row["ticker"])}</strong>（{escape(label)}）入選：'
                    f'{escape(entry_reason(row, seat_no))}'))
            for t in outs:
                parts.append(render_alert_box(
                    "out", "離席",
                    f'<strong>{escape(t)}</strong>（{escape(label)}）換出：'
                    f'{escape(exit_reason(t, track, arena))}'))
        section_changes = "".join(parts)
    section_changes_full = section_header("SEAT CHANGES", "換席原因") + section_changes

    # ── §CHALLENGERS（窄螢幕友善：4 欄，DD 標籤／遲滯狀態疊行）──
    chal_headers = [("Ticker", "left"), ("擁有層分", "right"), ("三閘通過", "left"),
                    ("DD 標籤／遲滯狀態", "left")]
    chal_rows = []
    for i, row in enumerate((arena.get("challengers_top") or [])[:5], 1):
        ol = own_layer(row)
        ticker_cell = (f'<div style="color:{TEXT_GRAY};font-size:10.5px;">候補{i}</div>'
                       f'<strong>{escape(row["ticker"])}</strong>')
        dd_cell = (f'<div style="font-size:12px;">{escape(row.get("dd_tag") or "—")}</div>'
                   f'<div style="margin-top:2px;">{hyst_text(row.get("hyst"))}</div>')
        chal_rows.append([ticker_cell, fmt2(ol["score"]),
                           pill("通過", "green") if ol["pass"] else pill("未通過", "red"),
                           dd_cell])
    section_challengers = section_header("CHALLENGERS", "候補前 5 與無 DD 機械過閘")
    if chal_rows:
        section_challengers += render_table(chal_headers, chal_rows)
    else:
        section_challengers += render_alert_box("neutral", "無資料", "本週無候補名單資料。")

    section_challengers += (f'<div style="font-size:13px;color:{TEXT_GRAY};margin:4px 0 8px;">'
                             f'「無 DD 而機械過閘」＝擁有層全榜中不是來自 DD 資料池、'
                             f'但仍通過三閘資格的股票：</div>')
    if mech_nodd:
        mech_headers = [("Ticker", "left"), ("擁有層分", "right"), ("成長（%）", "right"),
                        ("殖利率（%）", "right")]
        mech_rows = [[f"<strong>{escape(r['ticker'])}</strong>", fmt2(r.get('score')),
                      fmt1(r.get('g')), fmt1(r.get('ey'))] for r in mech_nodd[:8]]
        section_challengers += render_table(mech_headers, mech_rows)
        if len(mech_nodd) > 8:
            section_challengers += (f'<div style="font-size:12px;color:{TEXT_GRAY};">'
                                     f'其餘 {len(mech_nodd) - 8} 檔見網站。</div>')
    else:
        section_challengers += render_alert_box("neutral", "本週 0 檔",
                                                  "本週無「無 DD 機械過閘」名單成員。")
    if isinstance(today_signals, list):
        n_sig = len(today_signals)
        sig_txt = "、".join(s.get("ticker", "—") for s in today_signals[:8]) if n_sig else ""
        section_challengers += (f'<div style="font-size:12.5px;color:{TEXT_GRAY};margin-top:6px;">'
                                 f'另外，機械板機（狀態機訊號）本週觸發 {n_sig} 檔進場訊號'
                                 f'{("：" + escape(sig_txt)) if sig_txt else "（本週無新板機）"}。</div>')

    # ── §BREAKOUT PICKS（爆發正式榜＋晚段守門）──
    section_breakout = section_header("BREAKOUT PICKS", "爆發正式榜與晚段守門")
    if official_baofa:
        bo_headers = [("#", "left"), ("Ticker", "left"), ("上修幅度（FY+1）", "right"),
                      ("位置", "left"), ("退出條件", "left")]
        bo_rows = []
        for i, r in enumerate(official_baofa[:5], 1):
            bo_rows.append([str(i), f"<strong>{escape(r['ticker'])}</strong>",
                            fmt_signed_pct1(r.get("eps_fy_next_revision_pct")),
                            f'<span style="font-size:12px;">{escape(r.get("position") or "—")}</span>',
                            f'<span style="font-size:12px;">{escape(r.get("exit") or "—")}</span>'])
        section_breakout += render_table(bo_headers, bo_rows)
    else:
        section_breakout += render_alert_box("neutral", "無資料", "本週無爆發正式榜資料。")
    if late_cycle:
        late_headers = [("Ticker", "left"), ("被擋原因", "left")]
        late_rows = [[pill("晚段被擋", "red") + " " + f"<strong>{escape(r['ticker'])}</strong>",
                      f'<span style="font-size:12px;">{escape(r.get("late_reason") or "—")}</span>']
                     for r in late_cycle[:8]]
        section_breakout += render_table(late_headers, late_rows)
        if len(late_cycle) > 8:
            section_breakout += (f'<div style="font-size:12px;color:{TEXT_GRAY};">'
                                  f'其餘 {len(late_cycle) - 8} 檔見網站。</div>')
        section_breakout += (f'<div style="font-size:12.5px;color:{TEXT_GRAY};margin-top:4px;">'
                              f'守門邏輯：漲幅已在循環<strong>峰頂</strong>附近（追高風險），或未來兩年'
                              f'共識獲利成長路徑轉為<strong>下彎</strong>，才會被擋在候選、不列入正式榜。'
                              f'</div>')
    elif official_baofa:
        section_breakout += render_alert_box("neutral", "本週 0 檔", "本週無被守門擋下的晚段候選。")

    # ── §TENBAGGER WATCH（十倍榜）──
    section_tenbagger = section_header("TENBAGGER WATCH", "十倍榜")
    if tenbagger_official:
        stale_note = ""
        if tenbagger_as_of and tenbagger_as_of != data_as_of:
            stale_note = (f'<div style="font-size:12px;color:{TEXT_GRAY};margin-bottom:6px;">'
                          f'十倍榜資料 as_of {escape(str(tenbagger_as_of))}，'
                          f'早於本期擂台資料 {escape(str(data_as_of))}，較舊。</div>')
        tb_headers = [("#", "left"), ("Ticker", "left"), ("一句風險標示", "left")]
        tb_rows = []
        for i, r in enumerate(tenbagger_official[:5], 1):
            if r.get("above_w52") is False:
                risk = "已跌破年線（52 週）——訊號降溫，非停損理由"
            elif isinstance(r.get("dilution_cagr_pct"), (int, float)) and r["dilution_cagr_pct"] > 3:
                risk = f"稀釋 CAGR {r['dilution_cagr_pct']:+.1f}%，超過退出門檻 3%/年"
            elif isinstance(r.get("ret_12m_pct"), (int, float)) and r["ret_12m_pct"] < 0:
                risk = f"近 12 個月報酬 {r['ret_12m_pct']:+.1f}%，動能轉弱"
            else:
                exit_txt = (r.get("exit") or "").split("；")[0]
                risk = exit_txt or "無明顯風險標記"
            tb_rows.append([str(i), f"<strong>{escape(r['ticker'])}</strong>",
                            f'<span style="font-size:12px;">{escape(risk)}</span>'])
        section_tenbagger += stale_note + render_table(tb_headers, tb_rows)
    else:
        section_tenbagger += render_alert_box("neutral", "無資料", "本週無十倍榜資料。")

    # ── §LEDGER SCORECARD（帳簿記分）──
    section_scorecard = ""
    if scorecard is not None:
        ls = scorecard.get("ledger_sources") or {}
        sc_headers = [("名單", "left"), ("狀態", "left"), ("有效樣本（n_eff）", "right"),
                      ("技巧分（BSS）", "right")]
        sc_rows = []
        for key, label in LEDGER_SOURCES:
            entry = ls.get(key)
            if not entry:
                sc_rows.append([label, pill("尚無記分", "gray"), "—", "—"])
                continue
            status = entry.get("status")
            kind = {"green": "green", "red": "red"}.get(status, "gray")
            status_label = entry.get("status_label") or "—"
            sc_rows.append([label, pill(status_label, kind), fmt1(entry.get("n_eff")),
                            fmt2(entry.get("bss")) if entry.get("bss") is not None else "—"])
        section_scorecard = (section_header("LEDGER SCORECARD", "帳簿記分")
                              + render_table(sc_headers, sc_rows)
                              + f'<div style="font-size:12.5px;color:{TEXT_GRAY};">'
                                f'各名單層是否有實績，由預測帳簿同一把尺打分——不是所有名單都'
                                f'已經有結算樣本，「尚無記分」不代表名單無效，只代表還沒累積夠。'
                                f'</div>')

    # ── §BOARD EXCERPT（看板節錄）──
    section_board = section_header("BOARD EXCERPT", "看板節錄")
    if len(board_lines) >= 6:
        excerpt = board_lines[2:5] + board_lines[5:25]
        pre_txt = escape("\n".join(excerpt))
        section_board += (f'<div style="font-size:12px;color:{TEXT_GRAY};margin-bottom:6px;">'
                           f'等寬看板節錄；完整看板在 /cockpit/。</div>'
                           f'<pre style="background:#1f1b16;color:#e8e4da;font-size:10.5px;'
                           f'line-height:1.5;padding:12px 14px;border-radius:6px;overflow-x:auto;'
                           f'white-space:pre;font-family:Menlo,Consolas,monospace;margin:0 0 16px;">'
                           f'{pre_txt}</pre>')
    else:
        section_board += render_alert_box("neutral", "無資料", "本週無看板資料。")

    # ── 組信 ──
    body = f"""<div style="background:{BG_PAGE};padding:24px 12px;">
<div style="max-width:600px;margin:0 auto;background:#ffffff;border:1px solid {CARD_BORDER};
border-radius:8px;font-family:{FONT_STACK};font-size:15px;line-height:1.65;color:{TEXT_DARK};">
{render_top_bar(report_date)}
<div style="padding:18px 22px 4px;">
{render_one_minute([sent1, sent2, sent3])}
{tiles}
{section_roster}
{section_changes_full}
{section_challengers}
{section_breakout}
{section_tenbagger}
{section_scorecard}
{section_board}
</div>
<div style="padding:0 22px 20px;">
<a href="https://research.investmquest.com/cockpit/#overview" style="display:inline-block;
background:{NAVY};color:#ffffff;text-decoration:none;font-size:13.5px;font-weight:700;
padding:10px 18px;border-radius:6px;margin:6px 0 14px;">前往選股主控台 →</a>
<div style="font-size:11.5px;color:{TEXT_GRAY};line-height:1.8;">
連結：<a href="https://research.investmquest.com/cockpit/#overview" style="color:{GOLD};">選股主控台</a>
・<a href="https://research.investmquest.com/picks/" style="color:{GOLD};">精選榜</a>
・<a href="https://research.investmquest.com/engine/arena.html" style="color:{GOLD};">席位擂台頁</a><br>
資料 as-of：{escape(str(data_as_of))}<br>
席位與名單＝研究層產出，非帳戶持倉。本信純資訊性，不構成買賣建議。
</div>
</div>
</div>
</div>"""

    OUT_HTML.write_text(body, encoding="utf-8")
    OUT_SUBJECT.write_text(subject + "\n", encoding="utf-8")

    print(f"weekly_mail: {subject}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
