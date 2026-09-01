#!/usr/bin/env python3
"""決策引擎週報 email — 席位擂台前後週對比 + 換席原因（供 weekly-engine.yml 寄信用）.

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
DD_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
OUT_HTML = ROOT / "engine_weekly_mail.html"
OUT_SUBJECT = ROOT / "engine_weekly_mail_subject.txt"

TRACK_LABEL = {"core": "核心", "sat": "衛星"}
P_LABEL_TXT = {"breakout": "突破帶", "pullback": "回踩中", "in_trend": "趨勢帶內"}


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
    if raw.startswith("市值"):
        return f"市值不足（{raw}）"
    if raw.startswith("R 否決") or raw.startswith("R 保守否決"):
        return raw
    if raw.startswith("R fail"):
        return f"EPS 預估上修未達標（{raw}）"
    if raw.startswith("G fail"):
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


# ── 換入 / 全陣容 入選原因 ─────────────────────────────────────────────
def entry_reason(row: dict, seat_no: int) -> str:
    grp = row.get("grp") or {}
    g = grp.get("g")
    r = grp.get("r_fy1")
    p_label = P_LABEL_TXT.get(grp.get("p_label"), "—")
    g_txt = f"{g:.1f}%" if isinstance(g, (int, float)) else "—"
    r_txt = f"{r:+.1f}%" if isinstance(r, (int, float)) else "—"
    score = row.get("score")
    score_txt = f"{score:.2f}" if isinstance(score, (int, float)) else "—"
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


# ── HTML 渲染（全 inline CSS，Gmail 相容）───────────────────────────────
TH_STYLE = ("background:#2c2c2c;color:#f5f2ea;font-size:11.5px;text-transform:uppercase;"
            "letter-spacing:.04em;padding:8px 10px;text-align:left;")
TD_STYLE = "padding:7px 10px;border-bottom:1px solid #e5e0d5;font-size:13px;color:#222;"


def _table_open() -> str:
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            'style="border-collapse:collapse;margin:10px 0 22px;background:#ffffff;">')


def render_track_compare(track_label: str, cur_rows: list[dict],
                          prev_tickers: list[str], out_tickers: list[str]) -> str:
    prev_rank = {t: i + 1 for i, t in enumerate(prev_tickers)}
    rows = [(f'<tr><th style="{TH_STYLE}">席次</th><th style="{TH_STYLE}">本週</th>'
              f'<th style="{TH_STYLE}">上週</th><th style="{TH_STYLE}">狀態</th></tr>')]
    for i, row in enumerate(cur_rows, 1):
        t = row["ticker"]
        prev_r = prev_rank.get(t)
        if prev_r is None:
            status = ('<span style="background:#e8f5e9;color:#2e7d32;padding:2px 8px;'
                      'border-radius:4px;font-weight:600;">🆕 新任</span>')
            prev_txt = "（無）"
        elif prev_r == i:
            status = ('<span style="background:#f0f0ec;color:#666;padding:2px 8px;'
                      'border-radius:4px;">續任</span>')
            prev_txt = t
        elif prev_r > i:
            status = f'<span style="color:#2e7d32;font-weight:600;">↑ 續任（第{prev_r}→{i}名）</span>'
            prev_txt = t
        else:
            status = f'<span style="color:#c17a00;font-weight:600;">↓ 續任（第{prev_r}→{i}名）</span>'
            prev_txt = t
        rows.append(f'<tr><td style="{TD_STYLE}">{escape(track_label)} {i}</td>'
                    f'<td style="{TD_STYLE}"><strong>{escape(t)}</strong></td>'
                    f'<td style="{TD_STYLE}">{escape(prev_txt)}</td>'
                    f'<td style="{TD_STYLE}">{status}</td></tr>')
    red = TD_STYLE + "color:#c62828;"
    for t in out_tickers:
        rows.append(f'<tr style="background:#fdecea;"><td style="{red}">—</td>'
                    f'<td style="{red}">（無）</td>'
                    f'<td style="{red}text-decoration:line-through;"><strong>{escape(t)}</strong></td>'
                    f'<td style="{red}">❌ 換出</td></tr>')
    return _table_open() + "".join(rows) + "</table>"


def render_single_week_track(track_label: str, cur_rows: list[dict]) -> str:
    rows = [(f'<tr><th style="{TH_STYLE}">席次</th><th style="{TH_STYLE}">Ticker</th>'
              f'<th style="{TH_STYLE}">DD 裁決</th><th style="{TH_STYLE}">護城河</th>'
              f'<th style="{TH_STYLE}">分數</th></tr>')]
    for i, row in enumerate(cur_rows, 1):
        score = row.get("score")
        score_txt = f"{score:.2f}" if isinstance(score, (int, float)) else "—"
        rows.append(f'<tr><td style="{TD_STYLE}">{escape(track_label)} {i}</td>'
                    f'<td style="{TD_STYLE}"><strong>{escape(row["ticker"])}</strong></td>'
                    f'<td style="{TD_STYLE}">{escape(row.get("verdict") or "—")}</td>'
                    f'<td style="{TD_STYLE}">{escape(row.get("moat") or "—")}</td>'
                    f'<td style="{TD_STYLE}">{score_txt}</td></tr>')
    return _table_open() + "".join(rows) + "</table>"


def render_full_roster(core_rows: list[dict], sat_rows: list[dict]) -> str:
    rows = [(f'<tr><th style="{TH_STYLE}">席次</th><th style="{TH_STYLE}">Ticker</th>'
              f'<th style="{TH_STYLE}">DD 裁決</th><th style="{TH_STYLE}">護城河</th>'
              f'<th style="{TH_STYLE}">分數</th><th style="{TH_STYLE}">入選原因</th></tr>')]
    small = TD_STYLE + "font-size:12px;color:#555;"
    for label, track_rows in (("核心", core_rows), ("衛星", sat_rows)):
        for i, row in enumerate(track_rows, 1):
            score = row.get("score")
            score_txt = f"{score:.2f}" if isinstance(score, (int, float)) else "—"
            rows.append(f'<tr><td style="{TD_STYLE}">{escape(label)} {i}</td>'
                        f'<td style="{TD_STYLE}"><strong>{escape(row["ticker"])}</strong></td>'
                        f'<td style="{TD_STYLE}">{escape(row.get("verdict") or "—")}</td>'
                        f'<td style="{TD_STYLE}">{escape(row.get("moat") or "—")}</td>'
                        f'<td style="{TD_STYLE}">{score_txt}</td>'
                        f'<td style="{small}">{escape(entry_reason(row, i))}</td></tr>')
    return _table_open() + "".join(rows) + "</table>"


def render_change_paragraphs(track_label: str, ins: list[dict], outs: list[str],
                             track: str, arena: dict) -> str:
    parts = []
    box_in = ("background:#f4faf5;border-left:3px solid #2e7d32;padding:10px 14px;"
              "margin:0 0 10px;font-size:13px;color:#333;line-height:1.7;")
    box_out = ("background:#fdf6f5;border-left:3px solid #c62828;padding:10px 14px;"
               "margin:0 0 10px;font-size:13px;color:#333;line-height:1.7;")
    for row, seat_no in ins:
        parts.append(f'<div style="{box_in}">🆕 <strong>{escape(row["ticker"])}</strong>'
                     f'（{escape(track_label)}）入選：{escape(entry_reason(row, seat_no))}</div>')
    for t in outs:
        parts.append(f'<div style="{box_out}">❌ <strong>{escape(t)}</strong>'
                     f'（{escape(track_label)}）換出：{escape(exit_reason(t, track, arena))}</div>')
    return "".join(parts)


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

    prev_arena = load_prev_arena()
    degrade = prev_arena is None or prev_arena == arena

    core_in: list[str] = []
    core_out: list[str] = []
    sat_in: list[str] = []
    sat_out: list[str] = []
    if not degrade:
        prev_core_tickers = [r["ticker"] for r in (prev_arena.get("core_seats") or [])]
        prev_sat_tickers = [r["ticker"] for r in (prev_arena.get("sat_seats") or [])]
        core_in, core_out = diff_track(prev_core_tickers, cur_core_tickers)
        sat_in, sat_out = diff_track(prev_sat_tickers, cur_sat_tickers)
    else:
        prev_core_tickers, prev_sat_tickers = [], []

    has_changes = bool(core_in or core_out or sat_in or sat_out)

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

    # ── 標題一句話結論 ──
    if degrade:
        headline = "本週無前週資料可比，僅列本週陣容（HEAD 上無可對照的上週 arena.json）。"
    elif has_changes:
        bits = []
        if core_in or core_out:
            bits.append(f'核心：入 {"、".join(core_in) or "—"} ／出 {"、".join(core_out) or "—"}')
        if sat_in or sat_out:
            bits.append(f'衛星：入 {"、".join(sat_in) or "—"} ／出 {"、".join(sat_out) or "—"}')
        headline = "本週換席——" + "；".join(bits)
    else:
        headline = "本週無換席，陣容與上週相同。"

    # ── §1 前後週陣容對照 ──
    if degrade:
        section1 = (f'<h3 style="font-family:Georgia,\'Noto Serif TC\',serif;font-size:15px;'
                    f'color:#1a1a1a;margin:22px 0 4px;">核心席位（{len(core_cur)}/5）</h3>'
                    + render_single_week_track("核心", core_cur)
                    + f'<h3 style="font-family:Georgia,\'Noto Serif TC\',serif;font-size:15px;'
                      f'color:#1a1a1a;margin:22px 0 4px;">衛星席位（{len(sat_cur)}/5）</h3>'
                    + render_single_week_track("衛星", sat_cur))
    else:
        section1 = (f'<h3 style="font-family:Georgia,\'Noto Serif TC\',serif;font-size:15px;'
                    f'color:#1a1a1a;margin:22px 0 4px;">核心席位（{len(core_cur)}/5）</h3>'
                    + render_track_compare("核心", core_cur, prev_core_tickers, core_out)
                    + f'<h3 style="font-family:Georgia,\'Noto Serif TC\',serif;font-size:15px;'
                      f'color:#1a1a1a;margin:22px 0 4px;">衛星席位（{len(sat_cur)}/5）</h3>'
                    + render_track_compare("衛星", sat_cur, prev_sat_tickers, sat_out))

    # ── §2 換席原因 ──
    if degrade or not has_changes:
        alerts = duel_alerts(arena)
        extra = ""
        if alerts and not degrade:
            alert_lines = "；".join(f'{c} 挑戰者分數已超車在席者 {s}（{cs:.2f} vs {ss:.2f}）'
                                    for s, c, cs, ss in alerts if s and c
                                    and cs is not None and ss is not None)
            if alert_lines:
                extra = f'但 {alert_lines}，下週留意。'
        msg = "本週無前週資料可比，暫無法判定換席。" if degrade else "本週無換席。"
        section2 = (f'<div style="background:#f7f5ef;border-left:3px solid #999;padding:10px 14px;'
                    f'font-size:13px;color:#333;line-height:1.7;">{msg}{extra}</div>')
    else:
        core_in_rows = [(row, i + 1) for i, row in enumerate(core_cur) if row["ticker"] in core_in]
        sat_in_rows = [(row, i + 1) for i, row in enumerate(sat_cur) if row["ticker"] in sat_in]
        section2 = (render_change_paragraphs("核心", core_in_rows, core_out, "core", arena)
                    + render_change_paragraphs("衛星", sat_in_rows, sat_out, "sat", arena))

    # ── §3 本週全陣容細表 ──
    section3 = render_full_roster(core_cur, sat_cur)

    accent = "#8a5a2b"
    body = f"""<div style="max-width:680px;margin:0 auto;background:#ffffff;
font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang TC','Noto Sans TC',sans-serif;">
<div style="background:#1f1b16;padding:22px 24px;">
<div style="font-family:Georgia,'Noto Serif TC',serif;font-size:20px;font-weight:700;color:#f5f2ea;">
⚔ 席位擂台週報</div>
<div style="font-size:12.5px;color:#c9bfae;margin-top:4px;">{escape(report_date)}</div>
</div>
<div style="padding:18px 24px 4px;">
<div style="background:#fbf8f1;border:1px solid #e5e0d5;border-radius:6px;padding:12px 16px;
font-size:13.5px;color:#333;line-height:1.7;">{escape(headline)}</div>
</div>
<div style="padding:0 24px;">
<h2 style="font-family:Georgia,'Noto Serif TC',serif;font-size:17px;color:{accent};
margin:20px 0 2px;border-bottom:2px solid {accent};padding-bottom:4px;">§1 前後週陣容對照</h2>
{section1}
<h2 style="font-family:Georgia,'Noto Serif TC',serif;font-size:17px;color:{accent};
margin:8px 0 10px;border-bottom:2px solid {accent};padding-bottom:4px;">§2 換席原因</h2>
{section2}
<h2 style="font-family:Georgia,'Noto Serif TC',serif;font-size:17px;color:{accent};
margin:22px 0 2px;border-bottom:2px solid {accent};padding-bottom:4px;">§3 本週全陣容細表</h2>
{section3}
</div>
<div style="padding:14px 24px 24px;border-top:1px solid #e5e0d5;margin-top:8px;
font-size:11.5px;color:#888;line-height:1.9;">
連結：<a href="https://research.investmquest.com/cockpit/#overview" style="color:{accent};">組合駕駛艙</a>
<a href="https://research.investmquest.com/engine/arena.html" style="color:{accent};">席位擂台頁</a><br>
資料 as-of：{escape(str(data_as_of))}<br>
席位＝研究層陣容，非帳戶持倉。本信純資訊性，不構成買賣建議。
</div>
</div>"""

    OUT_HTML.write_text(body, encoding="utf-8")

    if degrade or not has_changes:
        tail = "本週無前週資料可比" if degrade else "本週無換席"
    else:
        ins = []
        for t in core_in + sat_in:
            if t not in ins:
                ins.append(t)
        outs = []
        for t in core_out + sat_out:
            if t not in outs:
                outs.append(t)
        change_bits = []
        if ins:
            change_bits.append("換入 " + "、".join(ins))
        if outs:
            change_bits.append("換出 " + "、".join(outs))
        tail = "／".join(change_bits) if change_bits else "本週無換席"
    subject = f"⚔️ 席位擂台週報 {report_date}｜{tail}"
    OUT_SUBJECT.write_text(subject + "\n", encoding="utf-8")

    print(f"weekly_mail: {subject}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
