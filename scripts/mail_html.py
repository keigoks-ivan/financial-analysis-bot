#!/usr/bin/env python3
"""共用 email HTML 版型渲染器（純 stdlib，py3.9+）。

實作 `notes/site-internal/root/_market_read_design_20260903.md` §5.7 的
email 版型標準 — 600px 單欄、外底色 #f6f5f2、白卡、系統字型（含 PingFang TC／
Noto Sans TC）、頂欄深藍 #0f1f3d、金色小標 #8a6d1f、斑馬列表格、三色狀態
pill、深藍站內連結按鈕、一行免責。全部 inline style，無外部 CSS／字型／
JS／圖片依賴（Gmail 網頁版安全）。

供六支 alert 產生器共用（sop_funnel/alert.py、update_turtle_sleeve.py、
build_earnings_reaction.py、update_long_track_w52_adaptive.py、
update_long_track_gld.py），讓外觀完全一致。已手工刻出的 weekly-engine 信
（`scripts/engine/build_weekly_mail.py`）與市況判讀信（`scripts/market_read_summary.py`）
是這套版型的原型／先例，兩者現況不動——之後可再refactor 移到本模組上。

用法（每支 builder 各自組 body_html 後呼叫 frame() 產生完整信件字串）：

    from mail_html import frame, one_minute, tiles, section, table, pill, esc

    body = one_minute(["..."]) + tiles([...]) + section("EN LABEL", "中文標題", table(...))
    html = frame("信件標題", "2026-09-02", body,
                 button_label="前往頁面 →", button_url="https://...",
                 disclaimer="本信為系統訊號通知，非投資建議。")
"""
from __future__ import annotations

from html import escape as _escape
from typing import Iterable, Sequence

# ── 版型 tokens（§5.7，與 build_weekly_mail.py 一致）───────────────────────
BG_PAGE = "#f6f5f2"
CARD_BORDER = "#e6e2d8"
NAVY = "#0f1f3d"
GOLD = "#8a6d1f"
ZEBRA = "#faf9f6"
TEXT_DARK = "#1c1c1c"
TEXT_GRAY = "#6b6b6b"
FONT_STACK = ("-apple-system,BlinkMacSystemFont,'PingFang TC','Noto Sans TC',"
              "'Segoe UI',sans-serif")

PILL_COLORS = {
    "green": ("#e8f3ea", "#1f6b3a"),
    "red": ("#fbe9e7", "#b3261e"),
    "gray": ("#f0eee9", "#5a5a5a"),
}

ACCENT_COLORS = {"navy": NAVY, "red": "#b3261e"}


def esc(v) -> str:
    """html.escape 包裝；None 一律轉空字串。"""
    if v is None:
        return ""
    return _escape(str(v))


def pill(text: str, tone: str = "gray") -> str:
    """狀態色票：綠(green)／紅(red)／灰(gray)，圓角 999，字 12px。"""
    bg, fg = PILL_COLORS.get(tone, PILL_COLORS["gray"])
    return (f'<span style="display:inline-block;background:{bg};color:{fg};'
            f'font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;'
            f'white-space:nowrap;">{esc(text)}</span>')


def one_minute(bullets: Sequence[str]) -> str:
    """「一分鐘版」bullet 區塊。少於 2 條時不渲染（單點事件不需要摘要重複）。

    bullets 內容視為已是 HTML-safe（呼叫端可用 <strong> 等標記粗體開頭字）。
    """
    items = [b for b in bullets if b]
    if len(items) < 2:
        return ""
    lis = "".join(f'<li style="margin:0 0 8px;">{b}</li>' for b in items)
    return (f'<div style="background:#fbf8f1;border:1px solid {CARD_BORDER};border-radius:6px;'
            f'padding:14px 18px;margin:18px 0;">'
            f'<div style="font-size:11px;letter-spacing:.08em;text-transform:uppercase;'
            f'color:{GOLD};font-weight:700;margin-bottom:6px;">ONE-MINUTE VERSION</div>'
            f'<div style="font-size:14px;font-weight:700;color:{TEXT_DARK};margin-bottom:6px;">'
            f'一分鐘版</div>'
            f'<ul style="margin:0;padding-left:18px;font-size:13.5px;line-height:1.65;'
            f'color:#333333;">{lis}</ul></div>')


def tiles(items: Sequence[tuple]) -> str:
    """三顆（或以上）大數字磚。items: [(label, value, sub)]，sub 可省略/None。

    用 <table><tr><td width="33%"> 排版；窄視窗（375px）下每格仍固定寬度，
    數字/標籤字級已縮小以避免擠壓（見驗收截圖）。
    """
    if not items:
        return ""
    n = len(items)
    width_pct = max(100 // n, 25)
    cells = []
    for it in items:
        label, value, sub = (list(it) + [None, None, None])[:3]
        sub_html = (f'<div style="font-size:10.5px;color:{TEXT_GRAY};margin-top:2px;">'
                    f'{esc(sub)}</div>') if sub else ""
        cells.append(
            f'<td width="{width_pct}%" style="padding:4px;vertical-align:top;">'
            f'<div style="background:#ffffff;border:1px solid {CARD_BORDER};border-radius:8px;'
            f'padding:14px 6px;text-align:center;">'
            f'<div style="font-size:21px;font-weight:700;color:{NAVY};">{esc(value)}</div>'
            f'<div style="font-size:11px;color:{TEXT_GRAY};margin-top:4px;">{esc(label)}</div>'
            f'{sub_html}</div></td>')
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="margin:0 0 4px;"><tr>{"".join(cells)}</tr></table>')


def section(label_en: str, title_zh: str, inner_html: str = "") -> str:
    """小字金色全大寫英文副標 ＋ 中文主標，接著渲染 inner_html。"""
    header = (f'<div style="margin:26px 0 10px;">'
              f'<div style="font-size:11px;letter-spacing:.08em;text-transform:uppercase;'
              f'color:{GOLD};font-weight:700;">{esc(label_en)}</div>'
              f'<div style="font-size:16px;font-weight:700;color:{TEXT_DARK};'
              f'margin-top:2px;">{esc(title_zh)}</div></div>')
    return header + inner_html


def _th(label: str, right: bool) -> str:
    al = "text-align:right;" if right else "text-align:left;"
    return (f'<th style="background:#eeece4;color:#4a4a42;font-size:11px;'
            f'text-transform:uppercase;letter-spacing:.02em;padding:8px 9px;{al}'
            f'border-bottom:1px solid {CARD_BORDER};">{esc(label)}</th>')


def _td(html_val: str, zebra: bool, right: bool) -> str:
    bg = ZEBRA if zebra else "#ffffff"
    al = "text-align:right;" if right else "text-align:left;"
    return (f'<td style="padding:7px 9px;border-bottom:1px solid #f0eee6;font-size:12.5px;'
            f'color:{TEXT_DARK};background:{bg};{al}">{html_val}</td>')


def table(headers: Sequence[str], rows: Sequence[Sequence[str]],
          numeric_cols: Iterable[int] = ()) -> str:
    """斑馬列表格。headers/rows 的字串視為已 HTML-safe（呼叫端自行 esc()）。

    numeric_cols：需靠右對齊的欄位 index（0-based）。
    """
    if not rows:
        return (f'<div style="font-size:13px;color:{TEXT_GRAY};padding:8px 2px;">'
                f'（無資料）</div>')
    nset = set(numeric_cols)
    head = "".join(_th(h, i in nset) for i, h in enumerate(headers))
    body_rows = []
    for i, row in enumerate(rows):
        zebra = i % 2 == 1
        cells = "".join(_td(v, zebra, j in nset) for j, v in enumerate(row))
        body_rows.append(f"<tr>{cells}</tr>")
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            f'style="border-collapse:collapse;margin:0 0 16px;background:#ffffff;'
            f'border:1px solid {CARD_BORDER};border-radius:6px;overflow:hidden;">'
            f'<tr>{head}</tr>' + "".join(body_rows) + '</table>')


def note(text_html: str) -> str:
    """單行淡灰提示（如「其餘見網站」「本次無事件」）。"""
    return (f'<div style="font-size:12.5px;color:{TEXT_GRAY};margin:0 0 14px;">'
            f'{text_html}</div>')


def frame(title: str, date: str, body_html: str, button_label: str, button_url: str,
          accent: str = "navy", disclaimer: str = "") -> str:
    """完整信件外殼：頂欄 → 內容 → 站內按鈕 → 一行免責。

    accent："navy"（預設，一般系統通知）或 "red"（提高留意的事件，於頂欄
    日期旁加一個小色標；頂欄底色與按鈕底色固定深藍——這是 §5.7 明訂的視覺
    錨點，不隨 accent 變動）。
    """
    accent_color = ACCENT_COLORS.get(accent, NAVY)
    tag_html = ""
    if accent == "red":
        tag_html = (f'<span style="display:inline-block;margin-left:8px;background:#3a1416;'
                    f'color:#ffb4ab;font-size:10.5px;font-weight:700;padding:1px 8px;'
                    f'border-radius:999px;vertical-align:middle;">留意</span>')
    top_bar = (f'<div style="background:{NAVY};padding:20px 24px;border-radius:8px 8px 0 0;'
              f'border-top:3px solid {accent_color};">'
              f'<div style="font-size:19px;font-weight:700;color:#ffffff;">'
              f'{esc(title)}{tag_html}</div>'
              f'<div style="font-size:12.5px;color:#c9d4e8;margin-top:4px;">'
              f'{esc(date)}（台北時間）</div></div>')
    button_html = ""
    if button_label and button_url:
        button_html = (f'<a href="{esc(button_url)}" style="display:inline-block;'
                       f'background:{NAVY};color:#ffffff;text-decoration:none;'
                       f'font-size:13.5px;font-weight:700;padding:10px 18px;'
                       f'border-radius:6px;margin:6px 0 14px;">{esc(button_label)}</a>')
    disclaimer_html = ""
    if disclaimer:
        disclaimer_html = (f'<div style="font-size:11.5px;color:{TEXT_GRAY};line-height:1.8;'
                           f'margin-top:2px;">{esc(disclaimer)}</div>')
    return f"""<div style="background:{BG_PAGE};padding:24px 12px;">
<div style="max-width:600px;margin:0 auto;background:#ffffff;border:1px solid {CARD_BORDER};
border-radius:8px;font-family:{FONT_STACK};font-size:15px;line-height:1.65;color:{TEXT_DARK};">
{top_bar}
<div style="padding:18px 22px 4px;">
{body_html}
</div>
<div style="padding:0 22px 20px;">
{button_html}
{disclaimer_html}
</div>
</div>
</div>"""
