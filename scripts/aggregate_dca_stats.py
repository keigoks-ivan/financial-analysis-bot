#!/usr/bin/env python3
"""Aggregate DCA role/verdict across all DCA_*.html into a stats panel HTML.

Outputs a self-contained HTML block to be injected into docs/research/index.html
between <!-- DCA_AUTO_STATS_START --> and <!-- DCA_AUTO_STATS_END --> markers.

Stats included:
  - §7a 角色分布 (stacked bar)
  - DCA 裁決分布 (進場 / 觀望 / 迴避 pills)
  - 核心持倉 list
  - 條件式（核心+衛星）list
  - 不持有/迴避 list
  - 角色 × 裁決 cross-tab

Stdlib only (no yfinance — pure local aggregation, fast).
Python 3.9 compat: use Optional[X] from typing, not X | None.
"""
import json
import re
import sys
from collections import Counter
from datetime import date as _date
from html import escape
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent.parent
DCA_DIR = ROOT / "docs" / "dca"
DD_DIR = ROOT / "docs" / "dd"

# Regex: handle both <th> and <td> label elements (DCA reports use <th>)
_ROLE_RE = re.compile(
    r'在投資組合中的角色</t[dh]>\s*<td[^>]*>(.*?)</td>',
    re.DOTALL,
)
_VERDICT_RE = re.compile(r'<!--\s*dca-verdict:\s*(進場|觀望|迴避)\s*-->')
_FILE_RE = re.compile(r'^DCA_(.+)_(\d{8})\.html$')
# v13 merged reports carry the decision layer (dca_role/dca_verdict) in dd-meta.
_DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)


def _norm(t: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", t or "").upper()

# v14.5 conditional-entry verdicts (§14 row 8b). Bucketed together and shown
# right after 進場 in the distribution pill row + cross-tab. Rendered only when
# ≥1 record carries one — zero churn for the current 進場/觀望/迴避-only corpus.
ENTER_CONDITIONAL = ("進場·條件式（循環衛星）", "進場·條件式（爆發候選）")
COND_VERDICT_LABEL = "進場·條件式"


# Category order for display
# v14.12 四值稅制（2026-07-10 持有人拍板「大道至簡」）：核心/衛星/追蹤/不持有。
# legacy dd-meta 的 條件式*/投機部位/候選·追蹤池/不持有·迴避 由 _categorize 映射歸一，檔案不動。
CATEGORY_ORDER = [
    "核心",
    "衛星",
    "追蹤",
    "不持有",
    "缺資料",
]

# Bar segment colours (CSS inline — reuse sig-pill palette hues)
_CAT_COLORS = {
    "核心":   "#1e40af",   # deep blue
    "衛星":   "#15803d",   # green
    "追蹤":   "#d97706",   # amber
    "不持有": "#6b7280",   # grey
    "缺資料": "#e2e8f0",   # very light (won't crowd)
}


def _strip_tags(s: str) -> str:
    return re.sub(r'<[^>]+>', '', s).strip()


def _categorize(role: str) -> str:
    """四值歸一：核心 / 衛星 / 追蹤 / 不持有（v14.12 canonical；legacy 值映射）。"""
    r = role.strip()
    if not r:
        return '缺資料'
    # v14.12 canonical（新報告直接命中）
    if r in ('核心', '衛星', '追蹤', '不持有'):
        return r
    # legacy 映射（85 份既有 dd-meta，檔案凍結不改）
    if '候選' in r or '追蹤池' in r or r == '追蹤池':
        return '追蹤'
    if r.startswith('不持有') or r.startswith('暫不持有') or r.startswith('迴避'):
        return '不持有'
    if '核心' in r:
        return '核心'
    if (
        '衛星' in r
        or '投機' in r
        or r.lower().startswith('satellite')
    ):
        return '衛星'
    return '缺資料'


def load_dca_records() -> dict:
    """Glob docs/dca/DCA_*.html, group by ticker, take latest date.

    Returns {ticker: {"date": "YYYY-MM-DD", "path": "DCA_X_YYYYMMDD.html",
                      "role_raw": str, "role_category": str,
                      "verdict": "進場|觀望|迴避|—"}}.
    """
    records: dict = {}
    for p in sorted(DCA_DIR.glob("DCA_*.html")):
        m = _FILE_RE.match(p.name)
        if not m:
            continue
        ticker, datestr = m.group(1), m.group(2)
        date_fmt = f"{datestr[:4]}-{datestr[4:6]}-{datestr[6:8]}"
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue

        # Verdict from head marker (first 2000 chars)
        head = text[:2000]
        vm = _VERDICT_RE.search(head)
        verdict = vm.group(1) if vm else "—"

        # Role text from §7a table row
        rm = _ROLE_RE.search(text)
        role_raw = _strip_tags(rm.group(1)) if rm else ""
        role_category = _categorize(role_raw)

        if ticker not in records or datestr > records[ticker]["_datestr"]:
            records[ticker] = {
                "date": date_fmt,
                "_datestr": datestr,
                "path": p.name,
                "role_raw": role_raw,
                "role_category": role_category,
                "verdict": verdict,
            }

    # v13 merged reports: dca_role/dca_verdict live in dd-meta. Overlay over the
    # legacy DCA records, newest date wins (a v13 DD supersedes a stale stand-
    # alone DCA for the same ticker). No-op for the current all-v12 corpus.
    if DD_DIR.exists():
        for p in sorted(DD_DIR.glob("DD_*.html")):
            try:
                text = p.read_text(encoding="utf-8")
            except Exception:
                continue
            mm = _DD_META_RE.search(text)
            if not mm:
                continue
            try:
                meta = json.loads(mm.group(1).strip())
            except Exception:
                continue
            if not str(meta.get("schema", "")).startswith(("v13", "v14")):
                continue
            ticker = _norm(meta.get("ticker", ""))
            datestr = (meta.get("date") or "").replace("-", "")
            if not ticker or len(datestr) != 8:
                continue
            role_raw = meta.get("dca_role", "") or ""
            verdict = meta.get("dca_verdict", "") or "—"
            if ticker not in records or datestr > records[ticker]["_datestr"]:
                records[ticker] = {
                    "date": f"{datestr[:4]}-{datestr[4:6]}-{datestr[6:8]}",
                    "_datestr": datestr,
                    "path": p.name,  # DD_* → _ticker_link routes to /dd/...#decision
                    "role_raw": role_raw,
                    "role_category": _categorize(role_raw),
                    "verdict": verdict,
                }
    return records


def _ticker_link(ticker: str, path: str) -> str:
    if path:
        # v13 records store the DD filename (DD_*) → link to its #decision anchor;
        # legacy records store the DCA filename (DCA_*) → link to /dca/.
        if path.startswith("DD_"):
            href = f"/dd/{escape(path)}#decision"
        else:
            href = f"/dca/{escape(path)}"
        return (
            f'<a href="{href}" target="_blank" rel="noopener">'
            f'{escape(ticker)}</a>'
        )
    return escape(ticker)


def _role_bar(records: dict) -> str:
    """Render horizontal stacked bar for role distribution."""
    total = len(records)
    if total == 0:
        return ""
    cat_counts: Counter = Counter(d["role_category"] for d in records.values())
    # omit 缺資料 from bar if 0, but keep others
    segments = []
    for cat in CATEGORY_ORDER:
        count = cat_counts.get(cat, 0)
        if count == 0:
            continue
        pct = count / total * 100
        color = _CAT_COLORS.get(cat, "#94A3B8")
        label = escape(cat)
        title = f"{cat}: {count} ({pct:.0f}%)"
        segments.append(
            f'<span title="{escape(title)}" style="'
            f'display:inline-block;width:{pct:.1f}%;background:{color};'
            f'height:18px;vertical-align:middle;'
            f'border-right:1px solid rgba(255,255,255,.3)" ></span>'
        )
    bar_html = "".join(segments)

    legend_items = []
    for cat in CATEGORY_ORDER:
        count = cat_counts.get(cat, 0)
        if count == 0:
            continue
        color = _CAT_COLORS.get(cat, "#94A3B8")
        legend_items.append(
            f'<span style="display:inline-flex;align-items:center;gap:3px;margin-right:8px;'
            f'font-size:11px;color:#475569">'
            f'<span style="width:10px;height:10px;background:{color};'
            f'display:inline-block;border-radius:2px"></span>'
            f'{escape(cat)} {count}'
            f'</span>'
        )
    legend_html = "".join(legend_items)

    return (
        f'<div style="width:100%;border-radius:4px;overflow:hidden;'
        f'background:#e2e8f0;margin-bottom:8px">{bar_html}</div>'
        f'<div style="margin-top:4px;line-height:1.8">{legend_html}</div>'
    )


def _verdict_pills(records: dict) -> str:
    counts: Counter = Counter(d["verdict"] for d in records.values())
    n_enter = counts.get("進場", 0)
    n_cond = sum(counts.get(v, 0) for v in ENTER_CONDITIONAL)
    n_watch = counts.get("觀望", 0)
    n_avoid = counts.get("迴避", 0)
    # Conditional-entry pill only when present (kept in the 進場 family colour).
    cond_pill = (
        f'<span class="sig-pill sig-enter">{COND_VERDICT_LABEL} · {n_cond}</span>'
        if n_cond else ""
    )
    return (
        f'<div class="signal-bar">'
        f'<span class="sig-pill sig-enter">進場 · {n_enter}</span>'
        f'{cond_pill}'
        f'<span class="sig-pill sig-watch">觀望 · {n_watch}</span>'
        f'<span class="sig-pill sig-avoid">迴避 · {n_avoid}</span>'
        f'</div>'
    )


def _ticker_list(items: list) -> str:
    """items = list of (ticker, path, optional_note)"""
    if not items:
        return '<li style="color:#94A3B8;font-style:italic;list-style:none">—</li>'
    lis = ""
    for ticker, path, note in items:
        link = _ticker_link(ticker, path)
        note_html = (
            f' <span class="meta" style="font-size:10.5px;color:#94A3B8">{escape(note)}</span>'
            if note else ""
        )
        lis += f'<li><span class="lead">{link}</span>{note_html}</li>'
    return lis


def _cross_tab(records: dict) -> str:
    """Small role × verdict cross-tab table."""
    cats = [c for c in CATEGORY_ORDER if c != "缺資料"]
    # Insert 進場·條件式 column after 進場 only when a conditional-entry record
    # exists; conditional verdicts are bucketed into that column so row totals
    # stay consistent (no silent drop).
    has_cond = any(d["verdict"] in ENTER_CONDITIONAL for d in records.values())
    verdicts = (
        ["進場"] + ([COND_VERDICT_LABEL] if has_cond else []) + ["觀望", "迴避", "—"]
    )

    def _bucket(v: str) -> str:
        return COND_VERDICT_LABEL if v in ENTER_CONDITIONAL else v

    # build matrix
    matrix: dict = {cat: Counter() for cat in CATEGORY_ORDER}
    for d in records.values():
        matrix[d["role_category"]][_bucket(d["verdict"])] += 1

    rows_html = ""
    for cat in CATEGORY_ORDER:
        row_total = sum(matrix[cat].values())
        if row_total == 0:
            continue
        cells = "".join(
            f'<td style="text-align:center;padding:2px 6px;font-size:11px">'
            f'{matrix[cat].get(v, 0) or "·"}</td>'
            for v in verdicts
        )
        rows_html += (
            f'<tr>'
            f'<td style="font-size:11px;padding:2px 6px;white-space:nowrap">'
            f'{escape(cat)}</td>'
            f'{cells}'
            f'<td style="text-align:center;font-weight:600;font-size:11px;'
            f'padding:2px 6px">{row_total}</td>'
            f'</tr>'
        )

    header_cells = "".join(
        f'<th style="font-size:11px;padding:2px 6px;font-weight:600;color:#475569">{v}</th>'
        for v in verdicts
    )
    return (
        f'<table style="border-collapse:collapse;width:100%">'
        f'<thead><tr>'
        f'<th style="font-size:11px;padding:2px 6px;font-weight:600;color:#475569">角色</th>'
        f'{header_cells}'
        f'<th style="font-size:11px;padding:2px 6px;font-weight:600;color:#475569">小計</th>'
        f'</tr></thead>'
        f'<tbody>{rows_html}</tbody>'
        f'</table>'
    )


def render(records: dict) -> str:
    """Return HTML matching auto-stats style for injection."""
    total = len(records)
    latest_date = max(
        (d["date"] for d in records.values()),
        default="—",
    )
    today = _date(2026, 5, 14)

    # Cell 1: 角色分布
    role_bar_html = _role_bar(records)

    # Cell 2: 裁決分布
    verdict_html = _verdict_pills(records)

    # Cell 3: 核心持倉
    core_items = sorted(
        [
            (t, d["path"], d["verdict"])
            for t, d in records.items()
            if d["role_category"] == "核心持倉"
        ],
        key=lambda x: x[0],
    )
    core_lis = _ticker_list(core_items)

    # Cell 4: 條件式（核心+衛星）
    cond_items = sorted(
        [
            (t, d["path"], d["role_category"].replace("條件式", ""))
            for t, d in records.items()
            if d["role_category"] in ("條件式核心持倉", "條件式衛星持倉")
        ],
        key=lambda x: (x[2], x[0]),
    )
    cond_lis = _ticker_list(cond_items)

    # Cell 5: 不持有/迴避
    avoid_items = sorted(
        [
            (t, d["path"], d["verdict"])
            for t, d in records.items()
            if d["role_category"] == "不持有/迴避"
        ],
        key=lambda x: x[0],
    )
    avoid_lis = _ticker_list(avoid_items)

    # Cell 6: cross-tab
    cross_tab_html = _cross_tab(records)

    return f'''<div class="auto-stats">
  <h3>
    📋 DCA 組合快照
    <span class="auto-tag">FULL-AUTO</span>
    <span class="ts">最近更新：{escape(latest_date)} ｜ {total} 檔 unique tickers</span>
  </h3>

  <div class="stats-grid">

    <div class="stats-cell">
      <div class="stats-label">📊 §7a 角色分布</div>
      {role_bar_html}
    </div>

    <div class="stats-cell">
      <div class="stats-label">DCA 裁決分布</div>
      {verdict_html}
      <div style="margin-top:10px;font-size:11.5px;color:#64748B">
        {total} unique tickers ｜ 最新報告：{escape(latest_date)}
      </div>
    </div>

    <div class="stats-cell stats-cell-stacked">
      <div class="stats-label">🛡️ 核心持倉</div>
      <ul>{core_lis}</ul>
    </div>

    <div class="stats-cell stats-cell-stacked">
      <div class="stats-label">⚡ 條件式持倉（待觸發）</div>
      <ul>{cond_lis}</ul>
    </div>

    <div class="stats-cell stats-cell-stacked">
      <div class="stats-label">🚫 不持有 / 迴避</div>
      <ul>{avoid_lis}</ul>
    </div>

    <div class="stats-cell">
      <div class="stats-label">📐 角色 × 裁決 cross-tab</div>
      {cross_tab_html}
    </div>

  </div>
</div>'''


def main() -> None:
    records = load_dca_records()
    print(render(records))


if __name__ == "__main__":
    main()
