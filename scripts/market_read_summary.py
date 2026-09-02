#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""market_read_summary.py — 把 `docs/market/data/read.json`（或失敗時的
`docs/market/data/read_status.json`）收斂成一封 email 摘要（HTML 版型＋純文字
備援）。

供 `.github/workflows/market-read-notify.yml` 消費：本檔第一行印主旨，
第二行空白，之後印純文字信文（stdout 合約不變）；`--html PATH` 額外寫出
美化版 HTML 信（設計稿 §5.7 版型標準：600px 單欄卡片、頂欄深藍、一分鐘版、
三顆數字磚、各節斑馬表、方向色票）；`--text PATH` 寫出純文字備援信文（與
stdout 的信文段落相同，供 `dawidd6/action-send-mail@v3` 的 `body:` 搭配
`html_body:` 組成 multipart 信）。設計稿：
`notes/site-internal/root/_market_read_design_20260903.md` §5.5（內容）／
§5.7（HTML 版型標準）。

判斷邏輯：先看 `--status-file`（預設 `docs/market/data/read_status.json`）；
若存在且 status=="failed"，印失敗摘要（不讀 read.json）。否則讀
`--file`（預設 `docs/market/data/read.json`）印成功摘要。任何檔案缺失／
欄位缺失一律降級印「（無資料）」等說明字串，絕不 crash；exit code 恆為 0
（email 一定要寄得出去，摘要腳本本身不應該擋 workflow）。HTML 產生失敗時
一律退化為與純文字摘要同義的失敗版型，不影響 stdout 合約。

用法
----
  python scripts/market_read_summary.py
  python scripts/market_read_summary.py --file docs/market/data/read.json \\
      --status-file docs/market/data/read_status.json \\
      --state docs/market/data/state.json \\
      --html /tmp/market_read_mail.html --text /tmp/market_read_mail.txt
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = ROOT / "docs" / "market" / "data" / "read.json"
DEFAULT_STATUS_FILE = ROOT / "docs" / "market" / "data" / "read_status.json"
DEFAULT_STATE_FILE = ROOT / "docs" / "market" / "data" / "state.json"
PAGE_URL = "https://research.investmquest.com/market/"


def load_json(path: Path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def fmt_pct(x):
    if not isinstance(x, (int, float)):
        return "—"
    return f"{x * 100:.0f}%" if abs(x) <= 1 else f"{x:.1f}%"


def fmt_pct1(x):
    if not isinstance(x, (int, float)):
        return "—"
    return f"{x * 100:.1f}%" if abs(x) <= 1 else f"{x:.1f}%"


# ═══════════════════════════════════════════════════════════════════════════
# 失敗摘要（純文字）
# ═══════════════════════════════════════════════════════════════════════════

def build_failure(status: dict):
    as_of = status.get("as_of", "?")
    stage = status.get("stage", "?")
    reasons = status.get("reasons") or []

    subject = f"市況判讀失敗 {as_of}｜{stage}"

    lines = []
    lines.append(f"本次市況判讀在「{stage}」關卡失敗，read.json 未變更、判讀未落帳。")
    lines.append("")
    if reasons:
        lines.append("失敗原因：")
        for r in reasons:
            lines.append(f"　－{r}")
    else:
        lines.append("失敗原因：（未提供）")
    lines.append("")
    lines.append("routine 明天會依觸發條件自動重試，或手動跑 market-read skill 補上。")
    lines.append("")
    lines.append(f"連結：{PAGE_URL}")
    body = "\n".join(lines)
    return subject, body


# ═══════════════════════════════════════════════════════════════════════════
# 成功摘要（純文字）
# ═══════════════════════════════════════════════════════════════════════════

def build_horizons_lines(horizons):
    lines = []
    if not isinstance(horizons, list):
        return ["　（無三框架資料）"]
    for h in horizons:
        label = h.get("label", h.get("key", "?"))
        p_up = fmt_pct(h.get("p_up"))
        p_clim_up = fmt_pct1(h.get("p_clim_up"))
        parts = [f"收高機率 {p_up}（基準 {p_clim_up}）"]
        p_dd = h.get("p_dd10") if h.get("p_dd10") is not None else h.get("p_dd20")
        if p_dd is not None:
            dd_label = "回撤 10%" if h.get("p_dd10") is not None else "回撤 20%"
            p_clim_dd = fmt_pct1(h.get("p_clim_dd"))
            parts.append(f"{dd_label} 機率 {fmt_pct(p_dd)}（基準 {p_clim_dd}）")
        lines.append(f"　－{label}：{'；'.join(parts)}")
    return lines or ["　（無三框架資料）"]


def build_forces_lines(forces):
    if not isinstance(forces, list) or not forces:
        return ["　（無三股力量資料）"]
    return [f"　－{f.get('title', '?')}" for f in forces]


def lookup_quote_value(state_data, ref, field="num"):
    if not isinstance(state_data, dict):
        return None
    quotes = ((state_data.get("evidence") or {}).get("quotes") or {})
    q = quotes.get(ref)
    if not isinstance(q, dict):
        return None
    return q.get(field)


def compute_distance_pct(current, threshold, op):
    if not isinstance(current, (int, float)) or not isinstance(threshold, (int, float)) or threshold == 0:
        return None
    if op in (">", ">="):
        return round((threshold - current) / abs(threshold) * 100, 1)
    return round((current - threshold) / abs(threshold) * 100, 1)


def build_falsifiers_lines(falsifiers, state_data):
    if not isinstance(falsifiers, list) or not falsifiers:
        return ["　（無證偽表資料）"]
    lines = []
    for f in falsifiers[:5]:
        label = f.get("label", "?")
        ref = f.get("ref")
        field = f.get("field", "num")
        threshold = f.get("threshold")
        unit = f.get("unit", "")
        op = f.get("op", "")
        current = lookup_quote_value(state_data, ref, field)
        if current is None:
            cur_str = "現值—"
        else:
            cur_str = f"現值 {current}{unit}"
        dist = compute_distance_pct(current, threshold, op)
        dist_str = f"，距離 {dist}%" if dist is not None else ""
        lines.append(f"　－[{f.get('direction', '?')}] {label}：{cur_str} → 門檻 {threshold}{unit}{dist_str}")
    return lines


def build_deviations_summary(deviations):
    if not isinstance(deviations, list) or not deviations:
        return "　（本次判讀與帳簿表格無申報分歧）"
    biggest = max(deviations, key=lambda d: abs((d.get("my_p") or 0) - (d.get("table_p") or 0)))
    diff = abs((biggest.get("my_p") or 0) - (biggest.get("table_p") or 0))
    return (f"　共 {len(deviations)} 條分歧；最大一條：{biggest.get('claim', '?')}"
            f"（表格 p={biggest.get('table_p')}，判讀 p={biggest.get('my_p')}，差 {diff:.2f}）")


def build_review_summary(review):
    if not isinstance(review, dict) or not review:
        return "　（本次判讀尚未經自動化冷讀 gate，或為 manual 模式產出）"
    model = review.get("model", "?")
    rnd = review.get("round", "?")
    verdict = review.get("verdict", "?")
    findings = review.get("findings") or []
    n_yellow = sum(1 for f in findings if isinstance(f, dict) and f.get("severity") == "🟡")
    return f"　冷讀模型 {model}／第 {rnd} 輪／verdict={verdict}／剩餘 🟡 {n_yellow} 條"


def build_success(data: dict, state_data):
    as_of = data.get("as_of", "?")
    thesis = data.get("thesis_zh", "") or ""
    subject = f"市況判讀 {as_of}｜{thesis[:28]}…"

    lines = []
    lines.append("【主張】")
    lines.append(thesis or "（無）")
    lines.append("")
    lines.append("【路徑】")
    lines.append(data.get("path_zh") or "（無）")
    lines.append("")
    lines.append("【三個時間框架】")
    lines.extend(build_horizons_lines(data.get("horizons")))
    lines.append("")
    lines.append("【三股力量】")
    lines.extend(build_forces_lines(data.get("forces")))
    lines.append("")
    lines.append("【證偽表（前 5 條）】")
    lines.extend(build_falsifiers_lines(data.get("falsifiers"), state_data))
    lines.append("")
    lines.append("【與帳簿表格的分歧】")
    lines.append(build_deviations_summary(data.get("deviations_from_tables")))
    lines.append("")
    lines.append("【冷讀結果】")
    lines.append(build_review_summary(data.get("review")))
    lines.append("")
    claim_ids = data.get("claim_ids") or []
    lines.append(f"【落帳編號】{claim_ids if claim_ids else '（無）'}")
    lines.append("")
    lines.append(f"連結：{PAGE_URL}")
    body = "\n".join(lines)
    return subject, body


# ═══════════════════════════════════════════════════════════════════════════
# HTML 版型（設計稿 §5.7）
# ═══════════════════════════════════════════════════════════════════════════

FONT_STACK = "-apple-system, 'PingFang TC', 'Noto Sans TC', 'Segoe UI', sans-serif"

COLOR_BG = "#f6f5f2"
COLOR_CARD = "#ffffff"
COLOR_BORDER = "#e6e2d8"
COLOR_NAVY = "#0f1f3d"
COLOR_NAVY_SUB = "#c9d2e3"
COLOR_DARK = "#1c1c1c"
COLOR_GRAY = "#6b6b6b"
COLOR_GOLD = "#8a6d1f"
COLOR_ZEBRA = "#faf9f6"
COLOR_HEAD_BG = "#f0eee9"

PILL_COLORS = {
    "green": ("#e8f3ea", "#1f6b3a"),
    "red": ("#fbe9e7", "#b3261e"),
    "gray": ("#f0eee9", "#5a5a5a"),
}


def esc(x) -> str:
    if x is None:
        return ""
    return html.escape(str(x), quote=True)


def pill_html(label: str, kind: str = "gray") -> str:
    bg, fg = PILL_COLORS.get(kind, PILL_COLORS["gray"])
    return (
        f'<span style="display:inline-block;background-color:{bg};color:{fg};'
        f'font-size:12px;font-weight:700;padding:2px 10px;border-radius:999px;'
        f'white-space:nowrap;">{esc(label)}</span>'
    )


def direction_pill_html(direction) -> str:
    d = (direction or "").strip().lower()
    if d == "bullish":
        return pill_html("轉多", "green")
    if d == "bearish":
        return pill_html("轉空", "red")
    return pill_html(direction or "中性", "gray")


def section_header_html(en: str, zh: str) -> str:
    return (
        f'<div style="margin:20px 0 8px 0;">'
        f'<div style="font-size:11px;letter-spacing:0.08em;color:{COLOR_GOLD};'
        f'font-weight:700;text-transform:uppercase;">{esc(en)}</div>'
        f'<div style="font-size:16px;color:{COLOR_DARK};font-weight:700;margin-top:2px;">{esc(zh)}</div>'
        f'</div>'
    )


def render_table_html(headers, rows, right_cols=None, min_width=None) -> str:
    right_cols = right_cols or set()
    thead = "".join(
        f'<th style="text-align:{"right" if i in right_cols else "left"};'
        f'background-color:{COLOR_HEAD_BG};color:{COLOR_GRAY};font-size:11px;font-weight:700;'
        f'padding:8px 8px;border-bottom:1px solid {COLOR_BORDER};white-space:nowrap;">{esc(h)}</th>'
        for i, h in enumerate(headers)
    )
    body_rows = []
    for ridx, row in enumerate(rows):
        bg = COLOR_ZEBRA if ridx % 2 == 1 else COLOR_CARD
        cells = "".join(
            f'<td style="text-align:{"right" if i in right_cols else "left"};padding:8px 8px;'
            f'font-size:12px;color:{COLOR_DARK};background-color:{bg};'
            f'border-bottom:1px solid {COLOR_BORDER};">{cell}</td>'
            for i, cell in enumerate(row)
        )
        body_rows.append(f"<tr>{cells}</tr>")
    style_extra = f"min-width:{min_width}px;" if min_width else ""
    table = (
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        f'style="width:100%;border-collapse:collapse;{style_extra}"><tr>{thead}</tr>{"".join(body_rows)}</table>'
    )
    if min_width:
        return (
            f'<div style="width:100%;max-width:100%;overflow-x:auto;'
            f'-webkit-overflow-scrolling:touch;">{table}</div>'
        )
    return table


def brief_zh(text, min_len=40, max_len=140) -> str:
    """取前 N 句直到累積長度達 min_len，超過 max_len 才截斷加刪節號。"""
    if not text:
        return "（無）"
    t = str(text).strip()
    parts = re.split(r"(?<=。)", t)
    out = ""
    for p in parts:
        if not out:
            out = p
        elif len(out) < min_len:
            out += p
        else:
            break
    out = out.strip() or t
    if len(out) > max_len:
        out = out[:max_len].rstrip("，,、") + "…"
    return out


def pick_watch_text(falsifiers, state_data) -> str:
    """挑距離門檻最近（最需要盯）的一條證偽訊號，供一分鐘版第三個要點使用。"""
    if not isinstance(falsifiers, list) or not falsifiers:
        return "（本期無可監測的轉向訊號）"
    best = None
    best_adist = None
    for f in falsifiers:
        current = lookup_quote_value(state_data, f.get("ref"), f.get("field", "num"))
        dist = compute_distance_pct(current, f.get("threshold"), f.get("op", ""))
        if dist is None:
            continue
        adist = abs(dist)
        if best_adist is None or adist < best_adist:
            best_adist = adist
            best = (f, current, dist)
    if best is None:
        f = falsifiers[0]
        return f"{f.get('label', '?')}（現值查無資料，距離未知）"
    f, current, dist = best
    unit = f.get("unit", "")
    cur_str = "—" if current is None else f"{current}{unit}"
    return f"{f.get('label', '?')}：現值 {cur_str}，距門檻 {f.get('threshold')}{unit} 還差 {abs(dist)}%"


def render_one_minute_html(data, state_data) -> str:
    thesis = brief_zh(data.get("thesis_zh"))
    path = brief_zh(data.get("path_zh"))
    watch = pick_watch_text(data.get("falsifiers"), state_data)
    items = [("主張", thesis), ("路徑", path), ("最需要盯的訊號", watch)]
    rows = "".join(
        f'<div style="margin-bottom:8px;font-size:15px;line-height:1.65;color:{COLOR_DARK};">'
        f'<b>{esc(k)}：</b>{esc(v)}</div>'
        for k, v in items
    )
    return (
        f'<div style="font-size:14px;font-weight:700;color:{COLOR_DARK};margin-bottom:8px;">一分鐘版</div>'
        f"{rows}"
    )


def render_tiles_html(horizons) -> str:
    by_key = {h.get("key"): h for h in (horizons or []) if isinstance(h, dict)}
    order = [("3m", "3 個月收高機率"), ("6m", "6 個月收高機率"), ("12m", "12 個月收高機率")]
    tiles = []
    present = [(k, label) for k, label in order if by_key.get(k)]
    for idx, (k, label) in enumerate(present):
        h = by_key[k]
        p_up = fmt_pct(h.get("p_up"))
        p_clim = fmt_pct1(h.get("p_clim_up"))
        mr = "3%" if idx < len(present) - 1 else "0"
        tiles.append(
            f'<div style="display:inline-block;width:31%;min-width:150px;max-width:190px;'
            f'vertical-align:top;margin:0 {mr} 10px 0;box-sizing:border-box;'
            f'background-color:{COLOR_ZEBRA};border:1px solid {COLOR_BORDER};border-radius:8px;'
            f'padding:14px 6px;text-align:center;">'
            f'<div style="font-size:11px;line-height:1.4;color:{COLOR_GRAY};">{esc(label)}</div>'
            f'<div style="font-size:26px;line-height:1.3;font-weight:700;color:{COLOR_DARK};margin-top:4px;">{esc(p_up)}</div>'
            f'<div style="font-size:11px;line-height:1.4;color:{COLOR_GRAY};margin-top:4px;">基準 {esc(p_clim)}</div>'
            f'</div>'
        )
    if not tiles:
        return f'<div style="font-size:13px;color:{COLOR_GRAY};">（無三框架資料）</div>'
    return f'<div style="font-size:0;">{"".join(tiles)}</div>'


def build_dd_caption_html(horizons) -> str:
    parts = []
    for h in horizons or []:
        if not isinstance(h, dict):
            continue
        label = str(h.get("label", "?")).split("（")[0]
        if h.get("p_dd10") is not None:
            parts.append(f"{label}看回撤 10%")
        elif h.get("p_dd20") is not None:
            parts.append(f"{label}看回撤 20%")
    if not parts:
        return ""
    return (
        f'<div style="font-size:11px;color:{COLOR_GRAY};margin-top:6px;">'
        f'回撤欄：{"；".join(parts)}；其餘顯示「—」代表本期未提供回撤資料。</div>'
    )


def render_horizons_table_html(horizons) -> str:
    if not isinstance(horizons, list) or not horizons:
        return f'<div style="font-size:13px;color:{COLOR_GRAY};">（無三框架資料）</div>'
    rows = []
    for h in horizons:
        label = str(h.get("label", h.get("key", "?"))).split("（")[0]
        p_up = fmt_pct(h.get("p_up"))
        p_clim_up = fmt_pct1(h.get("p_clim_up"))
        p_dd = h.get("p_dd10") if h.get("p_dd10") is not None else h.get("p_dd20")
        if p_dd is not None:
            dd_cell = f"{fmt_pct(p_dd)}（基準 {fmt_pct1(h.get('p_clim_dd'))}）"
        else:
            dd_cell = "—"
        rows.append([
            esc(label),
            esc(f"{p_up}（基準 {p_clim_up}）"),
            esc(dd_cell),
        ])
    # 5 個資料點（框架／收高p／基準／回撤p／基準）併成 3 欄，避免窄螢幕需要橫向捲動。
    table = render_table_html(["框架", "收高機率（基準）", "回撤機率（基準）"], rows, right_cols={1, 2})
    return table + build_dd_caption_html(horizons)


def render_forces_html(forces) -> str:
    if not isinstance(forces, list) or not forces:
        return f'<div style="font-size:13px;color:{COLOR_GRAY};">（無三股力量資料）</div>'
    blocks = []
    for f in forces[:3]:
        title = f.get("title", "?")
        mech = brief_zh(f.get("mechanism_zh", ""), min_len=20, max_len=110)
        blocks.append(
            f'<div style="margin-bottom:10px;">'
            f'<div style="font-size:14px;font-weight:700;color:{COLOR_DARK};">{esc(title)}</div>'
            f'<div style="font-size:13px;color:{COLOR_GRAY};margin-top:2px;line-height:1.55;">{esc(mech)}</div>'
            f'</div>'
        )
    return "".join(blocks)


def render_falsifiers_table_html(falsifiers, state_data) -> str:
    if not isinstance(falsifiers, list) or not falsifiers:
        return f'<div style="font-size:13px;color:{COLOR_GRAY};">（無可監測的轉向訊號）</div>'
    top = falsifiers[:5]
    rows = []
    for f in top:
        label = f.get("label", "?")
        threshold = f.get("threshold")
        unit = f.get("unit", "")
        current = lookup_quote_value(state_data, f.get("ref"), f.get("field", "num"))
        cur_str = "—" if current is None else f"{current}{unit}"
        dist = compute_distance_pct(current, threshold, f.get("op", ""))
        dist_str = "—" if dist is None else f"{abs(dist)}%"
        signal_cell = (
            f'<div>{direction_pill_html(f.get("direction"))}</div>'
            f'<div style="margin-top:4px;color:{COLOR_DARK};">{esc(label)}</div>'
        )
        # 現值／門檻／距離三個資料點併成一欄，避免窄螢幕需要橫向捲動。
        target_cell = esc(f"{cur_str} → {threshold}{unit}（距 {dist_str}）")
        rows.append([signal_cell, target_cell])
    table = render_table_html(["訊號", "現值→門檻（距離）"], rows, right_cols={1})
    extra = ""
    if len(falsifiers) > 5:
        extra = (
            f'<div style="font-size:12px;color:{COLOR_GRAY};margin-top:6px;">'
            f'其餘 {len(falsifiers) - 5} 條見網站。</div>'
        )
    return table + extra


def render_deviations_html(deviations) -> str:
    if not isinstance(deviations, list) or not deviations:
        return f'<div style="font-size:13px;color:{COLOR_DARK};line-height:1.6;">本次判讀與帳簿表格無申報分歧。</div>'
    biggest = max(deviations, key=lambda d: abs((d.get("my_p") or 0) - (d.get("table_p") or 0)))
    diff = abs((biggest.get("my_p") or 0) - (biggest.get("table_p") or 0))
    return (
        f'<div style="font-size:13px;color:{COLOR_DARK};line-height:1.65;">'
        f'共 <b>{len(deviations)}</b> 條分歧；最大一條：{esc(biggest.get("claim", "?"))}'
        f'（表格 p={esc(biggest.get("table_p"))}，判讀 p={esc(biggest.get("my_p"))}，差 {diff:.2f}）</div>'
    )


def render_review_html(review) -> str:
    if not isinstance(review, dict) or not review:
        return f'<div style="font-size:13px;color:{COLOR_GRAY};">本期為手動判讀，無冷讀紀錄。</div>'
    model = review.get("model", "?")
    rnd = review.get("round", "?")
    verdict = review.get("verdict", "?")
    findings = review.get("findings") or []
    n_yellow = sum(1 for f in findings if isinstance(f, dict) and f.get("severity") == "🟡")
    verdict_pill = pill_html("通過", "green") if verdict == "pass" else pill_html(str(verdict), "gray")
    return (
        f'<div style="font-size:13px;color:{COLOR_DARK};line-height:2;">'
        f'模型 {esc(model)}｜第 {esc(rnd)} 輪｜{verdict_pill}｜剩餘 🟡 {n_yellow} 條</div>'
    )


def render_claim_ids_html(claim_ids) -> str:
    if not claim_ids:
        return f'<div style="font-size:11px;color:{COLOR_GRAY};">（無）</div>'
    return f'<div style="font-size:11px;color:{COLOR_GRAY};word-break:break-all;">{esc("、".join(claim_ids))}</div>'


def render_email_shell_html(as_of: str, status_html: str, body_html: str) -> str:
    return f'''<meta charset="utf-8">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="width:100%;table-layout:fixed;background-color:{COLOR_BG};" bgcolor="{COLOR_BG}">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;table-layout:fixed;background-color:{COLOR_CARD};border:1px solid {COLOR_BORDER};border-radius:8px;font-family:{FONT_STACK};" bgcolor="{COLOR_CARD}">
<tr><td style="background-color:{COLOR_NAVY};padding:20px 24px;border-radius:8px 8px 0 0;" bgcolor="{COLOR_NAVY}">
<div style="color:#ffffff;font-size:18px;font-weight:700;font-family:{FONT_STACK};">市況判讀｜{esc(as_of)}</div>
{status_html}
</td></tr>
<tr><td style="padding:20px 24px 4px 24px;font-family:{FONT_STACK};">
{body_html}
</td></tr>
<tr><td style="padding:12px 24px 24px 24px;text-align:center;">
<a href="{PAGE_URL}" style="background-color:{COLOR_NAVY};color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 32px;border-radius:6px;display:inline-block;font-family:{FONT_STACK};">打開市況主控台</a>
</td></tr>
<tr><td style="padding:0 24px 24px 24px;">
<div style="font-size:11px;color:{COLOR_GRAY};line-height:1.6;border-top:1px solid {COLOR_BORDER};padding-top:12px;font-family:{FONT_STACK};">
本信為機械證據彙整與判讀者人工研判的摘要，屬描述器（只講機率與條件、不下買賣指令），非投資建議；完整證據與方法論請見網站原文。
</div>
</td></tr>
</table>
</td></tr>
</table>'''


def build_html_success(data: dict, state_data) -> str:
    as_of = data.get("as_of", "?")
    body_parts = [
        render_one_minute_html(data, state_data),
        render_tiles_html(data.get("horizons")),
        section_header_html("THREE HORIZONS", "三個時間框架"),
        render_horizons_table_html(data.get("horizons")),
        section_header_html("THREE FORCES", "三股力量"),
        render_forces_html(data.get("forces")),
        section_header_html("WHAT WOULD CHANGE THIS", "什麼會改變判讀"),
        render_falsifiers_table_html(data.get("falsifiers"), state_data),
        section_header_html("DEVIATION FROM THE LEDGER", "與帳簿的分歧"),
        render_deviations_html(data.get("deviations_from_tables")),
        section_header_html("COLD REVIEW", "冷讀結果"),
        render_review_html(data.get("review")),
        section_header_html("LEDGER CLAIM IDS", "落帳編號"),
        render_claim_ids_html(data.get("claim_ids")),
    ]
    return render_email_shell_html(as_of, "", "".join(body_parts))


def build_html_failure(as_of: str, stage: str, reasons) -> str:
    status_html = (
        f'<div style="margin-top:10px;">{pill_html("判讀失敗", "red")}'
        f'<span style="color:{COLOR_NAVY_SUB};font-size:12px;margin-left:8px;">關卡：{esc(stage)}</span></div>'
    )
    reasons = reasons or []
    if reasons:
        reasons_html = "".join(
            f'<div style="margin-bottom:6px;font-size:13px;color:{COLOR_DARK};">－{esc(r)}</div>'
            for r in reasons
        )
    else:
        reasons_html = f'<div style="font-size:13px;color:{COLOR_GRAY};">（未提供失敗原因）</div>'
    body_html = (
        f'<div style="font-size:15px;line-height:1.65;color:{COLOR_DARK};margin-bottom:8px;">'
        f'本次市況判讀在「{esc(stage)}」關卡失敗，read.json 未變更、判讀未落帳。</div>'
        + section_header_html("FAILURE REASONS", "失敗原因")
        + reasons_html
        + f'<div style="font-size:12px;color:{COLOR_GRAY};margin-top:16px;line-height:1.6;">'
          f'routine 明天會依觸發條件自動重試，或手動跑 market-read skill 補上。</div>'
    )
    return render_email_shell_html(as_of, status_html, body_html)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=str(DEFAULT_FILE), help="read.json 路徑（預設 %(default)s）")
    ap.add_argument("--status-file", default=str(DEFAULT_STATUS_FILE), help="read_status.json 路徑（預設 %(default)s）")
    ap.add_argument("--state", default=str(DEFAULT_STATE_FILE), help="state.json 路徑（供證偽表現值查詢，預設 %(default)s）")
    ap.add_argument("--html", default=None, help="額外寫出美化版 HTML 信到此路徑（設計稿 §5.7）")
    ap.add_argument("--text", default=None, help="額外寫出純文字備援信文到此路徑（內容與 stdout 信文段相同）")
    args = ap.parse_args()

    html_body = None
    try:
        status_data = load_json(Path(args.status_file))
        if isinstance(status_data, dict) and status_data.get("status") == "failed":
            subject, body = build_failure(status_data)
            html_body = build_html_failure(
                status_data.get("as_of", "?"), status_data.get("stage", "?"), status_data.get("reasons") or []
            )
        else:
            read_data = load_json(Path(args.file))
            if not isinstance(read_data, dict):
                subject = "市況判讀摘要產生失敗｜read.json 不可讀"
                body = f"找不到或無法解析 {args.file}，且 {args.status_file} 未標記失敗狀態。\n\n連結：{PAGE_URL}"
                html_body = build_html_failure(
                    "?", "read.json 無法讀取", [f"找不到或無法解析 {args.file}"]
                )
            else:
                state_data = load_json(Path(args.state))
                subject, body = build_success(read_data, state_data)
                html_body = build_html_success(read_data, state_data)
    except Exception as e:  # noqa: BLE001 — 摘要腳本絕不能讓 workflow 因未預期例外而卡住
        subject = "市況判讀摘要產生時發生未預期錯誤"
        body = f"market_read_summary.py 拋出例外：{e!r}\n\n連結：{PAGE_URL}"
        try:
            html_body = build_html_failure("?", "摘要腳本例外", [repr(e)])
        except Exception:  # noqa: BLE001 — HTML 版型本身出錯也不可讓腳本掛掉
            html_body = None

    if args.html:
        try:
            Path(args.html).write_text(html_body or "", encoding="utf-8")
        except OSError:
            pass
    if args.text:
        try:
            Path(args.text).write_text(body, encoding="utf-8")
        except OSError:
            pass

    print(subject)
    print()
    print(body)
    sys.exit(0)


if __name__ == "__main__":
    main()
