"""Canonical /backtest/ sub-navigation (pill bar) — single source of truth.

Every backtest page header renders the same rows via make_toggle(active):
one row per zone of the /backtest/ index (2026-10 reorganisation), in the same order:
    ① 實盤證據 | ② 槓桿與保險 | ③ 趨勢規則 | ④ 台指期與短線 | ⑤ 選股與因子
    ⑥ 分散資產 | ⑦ 總經與房市 | 方法與術語
Which page sits in which row, its short label and its status come from _page_meta.py
(PAGES). Pages that were folded into another page's chapter are not in the bar;
the pages that still exist but belong to a chapter (_page_meta.MEMBERS) highlight
their main page's pill (aliases).

Design (2026-07-11 redesign, kept):
  * Colour discipline — every pill is neutral (grey fill, dark-grey text); the
    ONE current page is highlighted with the site brand deep-blue gradient
    (imq-nav #081832→#173564).
  * No emoji in labels.
  * Status (實盤/候選/已否決/已退役) is a small suffix TAG inside the pill; 筆記 has no tag.
    已否決/已退役 pills sort to the end of their row and recede.
  * Compact layout — fixed-width left label column, pills flow to the right,
    one row per zone.  No JS; wraps (never horizontally overflows) on mobile.

Each link entry is (url, label, key, status) where status is one of the keys of
_page_meta.STATUS.

Used by:
  * docs/backtest/_build_*.py, scripts/build_*.py and the v7-backtest page generators
    (they sys.path this directory and import make_toggle);
  * _inject_subnav.py — surgically refreshes the bar in every existing page.

When adding a page: add one entry to _page_meta.PAGES, then run _inject_subnav.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _page_meta as PM  # noqa: E402

# status → (css-class, is-dead)  — dead sorts last within a row; 筆記 shows no tag
_STATUS = {
    "live": ("live", False),
    "cand": ("watch", False),
    "note": (None, False),
    "rej": ("dead", True),
    "ret": ("dead", True),
}

ROW_LABELS = {1: "① 實盤證據", 2: "② 槓桿與保險", 3: "③ 趨勢規則", 4: "④ 台指期與短線",
              5: "⑤ 選股與因子", 6: "⑥ 分散資產", 7: "⑦ 總經與房市", 8: "方法與術語"}

# 向後相容：舊的 pill 群名稱改為依區組成
ZONE_LINKS = {
    z: [(u, PM.PAGES[u]["short"], PM.PAGES[u]["key"], PM.PAGES[u]["status"]) for u in PM.ZONE_ORDER[z]]
    for z in PM.ZONES
}
ALIASES = PM.aliases()

# One <style> block per page (make_toggle is embedded once). Scoped under
# .bt-subnav so it can never collide with page CSS.
_STYLE = (
    '<style id="bt-subnav-style">'
    '.bt-subnav{margin-top:.75rem;border:1px solid var(--border,#e5e7eb);border-radius:8px;'
    'overflow:hidden;font-size:.78rem;line-height:1.3}'
    '.bt-subnav-row{display:flex;align-items:flex-start;gap:.55rem;padding:.32rem .55rem;'
    'border-top:1px solid var(--border,#e5e7eb)}'
    '.bt-subnav-row:first-child{border-top:0}'
    '.bt-subnav-lbl{flex:0 0 5.4em;font-size:.64rem;font-weight:700;color:var(--muted,#6b7280);'
    'text-transform:uppercase;letter-spacing:.04em;padding-top:.34rem}'
    '.bt-subnav-pills{display:flex;flex-wrap:wrap;gap:.3rem;min-width:0}'
    '.bt-subnav-pills a{display:inline-flex;align-items:center;gap:.28rem;padding:.26rem .6rem;'
    'background:#eef1f4;color:#374151;border-radius:999px;text-decoration:none;font-weight:500;'
    'white-space:nowrap;transition:background .12s}'
    '.bt-subnav-pills a:hover{background:#e1e6ea}'
    '.bt-subnav-pills a.bt-dead{color:#7a828d;background:#f2f3f5}'
    '.bt-subnav-pills a.bt-on{background:linear-gradient(135deg,#081832,#173564);color:#fff;'
    'font-weight:600}'
    '.bt-subnav-pills a.bt-on:hover{background:linear-gradient(135deg,#081832,#173564)}'
    '.bt-tag{font-size:.6rem;font-weight:600;padding:.02rem .3rem;border-radius:4px;line-height:1.4}'
    '.bt-tag-dead{background:rgba(220,38,38,.12);color:#b42318}'
    '.bt-tag-watch{background:rgba(180,118,20,.15);color:#986a12}'
    '.bt-tag-live{background:rgba(184,146,74,.2);color:#7a5a1a}'
    '.bt-on .bt-tag-dead{background:rgba(255,255,255,.22);color:#fff}'
    '.bt-on .bt-tag-watch{background:rgba(255,255,255,.22);color:#fff}'
    '.bt-on .bt-tag-live{background:rgba(255,255,255,.22);color:#fff}'
    '@media(max-width:640px){'
    '.bt-subnav-row{flex-direction:column;gap:.28rem;padding:.4rem .55rem}'
    '.bt-subnav-lbl{flex-basis:auto;padding-top:0}}'
    '</style>'
)


def _pill(url: str, label: str, key: str, status: str | None, active: str) -> str:
    cls = ["bt-on"] if key == active else []
    tag = ""
    if status:
        kind, is_dead = _STATUS[status]
        if is_dead and key != active:
            cls.append("bt-dead")
        if kind:
            tag = f'<span class="bt-tag bt-tag-{kind}">{PM.STATUS[status]}</span>'
    cls_attr = f' class="{" ".join(cls)}"' if cls else ""
    return f'<a href="{url}"{cls_attr}>{label}{tag}</a>'


def _sorted(links: list) -> list:
    """已否決／已退役 pills sort to the end; otherwise stable order."""
    def rank(entry):
        status = entry[3]
        return 1 if (status and _STATUS[status][1]) else 0
    return sorted(links, key=rank)


def _row(title: str, links: list, active: str) -> str:
    pills = "".join(_pill(u, lb, k, s, active) for u, lb, k, s in _sorted(links))
    return (f'<div class="bt-subnav-row"><div class="bt-subnav-lbl">{title}</div>'
            f'<div class="bt-subnav-pills">{pills}</div></div>')


def make_toggle(active: str) -> str:
    """Render the pill bar. `active` = key of the current page (member keys are aliased)."""
    active = ALIASES.get(active, active)
    return (_STYLE + '<nav class="bt-subnav" aria-label="回測子導航">'
            + "".join(_row(ROW_LABELS[z], ZONE_LINKS[z], active) for z in sorted(ZONE_LINKS))
            + '</nav>')
