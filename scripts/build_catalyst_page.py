#!/usr/bin/env python3
"""前瞻催化劑日曆 — 頁面渲染器（Phase 2＋3）.

讀 docs/catalyst/calendar.json ＋ archive.json ＋ variance.json（Phase 3 承保差異），
輸出 docs/catalyst/index.html。

版面（沿用 build_pipeline_page.py 慣例：site_nav import、STYLE 常數、--dry-run）：
  · 標題 ＋ 一句話導言
  · 「本週／未來 14 天」highlight block
  · 完整前瞻表：日期｜Ticker｜事件｜類型｜影響｜我們的立場｜來源
    （s15_static 列視覺標記「可能過期」）
  · 保質期警示 block（dd_expiry 事件）
  · 承保差異 variance section（現共識 EPS vs DD base_eps_path，漂移%＋旗標）
  · 已過事件／archive：最近 10 筆，含 outcome 欄（未回填顯示「待複盤」）
  · Coverage footer：universe_count、skipped / errors 計數（誠實顯示）
  · noindex,nofollow

Usage:
  python3 scripts/build_catalyst_page.py
  python3 scripts/build_catalyst_page.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import full_nav_block  # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
CAT_DIR = ROOT / "docs" / "catalyst"
CALENDAR_JSON = CAT_DIR / "calendar.json"
ARCHIVE_JSON = CAT_DIR / "archive.json"
VARIANCE_JSON = CAT_DIR / "variance.json"        # Phase 3（尚未存在）
HTML_OUT = CAT_DIR / "index.html"

TAIPEI = timezone(timedelta(hours=8))
HIGHLIGHT_DAYS = 14
ARCHIVE_SHOW = 10

NAV_BLOCK = full_nav_block("market", "cat")

TYPE_LABEL = {
    "earnings": "財報", "dd_expiry": "保質期", "product": "產品",
    "regulatory": "法規", "capacity": "產能", "guidance": "財測",
    "macro": "總經", "other": "其他",
}
SOURCE_LABEL = {
    "yfinance": "yfinance", "dd-meta": "dd-meta", "s15_static": "§15 靜態",
}


# ── utils ─────────────────────────────────────────────────────────────────────
def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI).isoformat(timespec="seconds")


def _fmt_stamp(iso: Optional[str]) -> str:
    if not iso or "T" not in iso:
        return iso or "—"
    d, t = iso.split("T", 1)
    return f"{d} {t[:5]}"


def _load(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _type_badge(t: str) -> str:
    label = TYPE_LABEL.get(t, t or "其他")
    return f'<span class="typ typ-{escape(t or "other")}">{escape(label)}</span>'


def _impact_badge(imp: str) -> str:
    cls = {"高": "imp-hi", "中": "imp-mid", "低": "imp-lo"}.get(imp, "imp-mid")
    return f'<span class="imp {cls}">{escape(imp or "—")}</span>'


def _verdict_badge(v: Optional[str]) -> str:
    if not v:
        return '<span class="verdict v-none">待補</span>'
    cls = {"進場": "v-in", "觀望": "v-watch", "迴避": "v-avoid"}.get(v, "v-none")
    return f'<span class="verdict {cls}">{escape(v)}</span>'


def _positioning_cell(e: dict) -> str:
    p = e.get("positioning") or {}
    role = p.get("dca_role") or ""
    role_html = f'<span class="role">{escape(role)}</span>' if role else ""
    return f'{_verdict_badge(p.get("dca_verdict"))} {role_html}'


def _source_cell(e: dict) -> str:
    src = e.get("source", "")
    label = SOURCE_LABEL.get(src, src)
    stale_flag = ""
    if src == "s15_static":
        stale_flag = ' <span class="stale-flag" title="來自 DD §15 靜態日期，非即時查詢，可能已過期">可能過期</span>'
    return f'<span class="src src-{escape(src)}">{escape(label)}</span>{stale_flag}'


def _ticker_link(e: dict) -> str:
    t = escape(e["ticker"])
    dd = e.get("dd_file")
    if dd:
        return f'<a href="{escape(dd)}#decision">{t}</a>'
    return t


def _watch_html(e: dict) -> str:
    w = e.get("watch") or ""
    return f'<div class="watch">{escape(w)}</div>' if w else ""


def _date_cell(e: dict) -> str:
    dp = e.get("date_precision")
    approx = "~" if dp in ("month", "quarter") else ""
    hint = f' <span class="dp" title="日期精度：{escape(dp)}">≈</span>' if dp in ("month", "quarter") else ""
    return f'{approx}{escape(e["date"])}{hint}'


# ── sections ──────────────────────────────────────────────────────────────────
def render_highlight(events: list, today: date) -> str:
    horizon = (today + timedelta(days=HIGHLIGHT_DAYS)).isoformat()
    soon = [e for e in events if today.isoformat() <= e["date"] <= horizon]
    if not soon:
        body = '<div class="empty">未來 14 天內無登錄事件。</div>'
    else:
        cards = "\n".join(
            f'''<div class="hl-card">
      <div class="hl-date">{_date_cell(e)}</div>
      <div class="hl-main">{_ticker_link(e)} {_type_badge(e["type"])} {_impact_badge(e.get("impact",""))}</div>
      <div class="hl-event">{escape(e["event"])}</div>
      <div class="hl-pos">{_positioning_cell(e)}</div>
    </div>'''
            for e in soon
        )
        body = f'<div class="hl-grid">{cards}</div>'
    return f"""<section class="block">
  <h2 class="block-h"><span class="dot"></span>本週／未來 14 天</h2>
  <div class="block-sub">距今 {HIGHLIGHT_DAYS} 天內的財報與結構化催化劑，共 {len(soon)} 筆。財報前 5 個交易日為靜默期，禁新建倉。</div>
  {body}
</section>"""


def _preview_link(e: dict) -> str:
    """財報事件的 T-minus 狀態徽章：已有 preview HTML → 📋 前瞻連結；
    只有凍結快照（cron 自動凍結）→ 🔒 錨已凍結（提示可觸發 preview skill）。"""
    if e.get("type") != "earnings":
        return ""
    ymd = e["date"].replace("-", "")
    fname = f"preview_{e['ticker'].replace('.', '')}_{ymd}.html"
    fname_dot = f"preview_{e['ticker']}_{ymd}.html"
    for f in (fname_dot, fname):
        if (ROOT / "docs" / "earnings" / f).exists():
            return f' <a class="pv-link" href="/earnings/{f}">📋 前瞻</a>'
    for f in (f"preview_{e['ticker'].upper()}_{ymd}.json",
              f"preview_{e['ticker'].upper().replace('.', '')}_{ymd}.json"):
        if (ROOT / "docs" / "catalyst" / "snapshots" / f).exists():
            return (f' <span class="pv-frozen" title="賽前共識已自動凍結（{f}）；'
                    f'敘事層 preview 以「{e["ticker"]} 財報前瞻」觸發">🔒 錨已凍結</span>')
    return ""


def _fwd_row(e: dict) -> str:
    return f"""<tr>
  <td class="left nowrap">{_date_cell(e)}</td>
  <td class="left tk">{_ticker_link(e)}</td>
  <td class="left ev">{escape(e["event"])}{_preview_link(e)}{_watch_html(e)}</td>
  <td>{_type_badge(e["type"])}</td>
  <td>{_impact_badge(e.get("impact",""))}</td>
  <td class="left">{_positioning_cell(e)}</td>
  <td class="left">{_source_cell(e)}</td>
</tr>"""


def render_forward_table(events: list) -> str:
    rows = [e for e in events if e["type"] != "dd_expiry"]
    if not rows:
        body = '<tr><td colspan="7" class="empty">目前無前瞻事件。</td></tr>'
    else:
        body = "\n".join(_fwd_row(e) for e in rows)
    return f"""<section class="block">
  <h2 class="block-h"><span class="dot"></span>前瞻事件全表 <span class="cnt">{len(rows)} 筆</span></h2>
  <div class="block-sub">
    依日期排序。<b>來源</b>三類：<span class="src src-yfinance">yfinance</span> 即時財報日、
    <span class="src src-dd-meta">dd-meta</span> DD 內結構化催化劑、
    <span class="src src-s15_static">§15 靜態</span>（yfinance 失敗時備援，<span class="stale-flag">可能過期</span>）。
    Ticker 連該檔 DD 的 <code>#decision</code> 錨點。
  </div>
  <div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">日期</th><th class="left">Ticker</th><th class="left">事件</th>
  <th>類型</th><th>影響</th><th class="left">我們的立場</th><th class="left">來源</th>
</tr></thead>
<tbody>
{body}
</tbody></table></div>
</section>"""


def render_expiry(events: list) -> str:
    exp = [e for e in events if e["type"] == "dd_expiry"]
    if not exp:
        body = '<div class="empty">目前無 30 天內屆滿的 DD 保質期。</div>'
    else:
        rows = "\n".join(
            f"""<tr>
  <td class="left nowrap">{escape(e["date"])}</td>
  <td class="left tk">{_ticker_link(e)}</td>
  <td class="left">{_positioning_cell(e)}</td>
  <td class="left">{escape(e.get("watch") or "")}</td>
</tr>""" for e in exp)
        body = f"""<div class="tbl-wrap"><table>
<thead><tr><th class="left">保質期</th><th class="left">Ticker</th><th class="left">現裁決</th><th class="left">動作</th></tr></thead>
<tbody>
{rows}
</tbody></table></div>"""
    return f"""<section class="block warn-block">
  <h2 class="block-h"><span class="dot dot-warn"></span>保質期警示 <span class="cnt">{len(exp)} 檔</span></h2>
  <div class="block-sub">DD §15 保質期在 30 天內屆滿或已過的名字——保質期後 §14 裁決可能失效，需重跑 stock-analyst 複審。</div>
  {body}
</section>"""


def _flag_cell(flag: str) -> str:
    cls = {"🔴": "vf-red", "🟡": "vf-amber", "🟢": "vf-green", "🟢↑": "vf-up",
           "⚪": "vf-cur"}.get(flag, "vf-green")
    return f'<span class="vflag {cls}">{escape(flag)}</span>'


def _drift_cell(d, muted: bool = False) -> str:
    try:
        v = float(d)
    except (TypeError, ValueError):
        return "—"
    if muted:            # ⚪ 幣別待確認：數字存疑，不上紅綠色
        cls = "dr-muted"
    else:
        cls = "dr-neg" if v < -5 else ("dr-pos" if v > 5 else "dr-flat")
    sign = "+" if v > 0 else ""
    return f'<span class="drift {cls}">{sign}{v:.1f}%</span>'


def _eps_cell(v) -> str:
    if v is None:
        return '<span class="na">—</span>'
    try:
        return f"{float(v):,.2f}"
    except (TypeError, ValueError):
        return escape(str(v))


def _var_row(r: dict) -> str:
    tk = escape(r.get("ticker", ""))
    dd = r.get("dd_file")
    tk_html = f'<a href="{escape(dd)}#decision">{tk}</a>' if dd else tk
    fy = escape(str(r.get("fy_label", "")))
    fy_end = escape(str(r.get("fy_end", "")))
    cur = (r.get("currency") or "").upper()
    cur_note = f' <span class="cur">{escape(cur)}</span>' if cur and cur != "USD" else ""
    mm = ' <sup class="bmark" title="口徑為 GAAP，yfinance 共識通常為 adjusted，比較僅供方向參考">†</sup>' if r.get("basis_mismatch") else ""
    basis_html = escape(str(r.get("eps_basis", "")))
    if r.get("currency_suspect"):
        fc = escape((r.get("financial_currency") or "?").upper())
        basis_html += (f'<div class="cur-suspect">疑似幣別錯配（yfinance 共識疑為 {fc}），人工確認</div>')
    return f"""<tr>
  <td class="left tk">{tk_html}</td>
  <td class="left nowrap">{fy}<span class="fye">（{fy_end}）</span></td>
  <td class="num">{_eps_cell(r.get("base_eps"))}{cur_note}</td>
  <td class="num">{_eps_cell(r.get("consensus_eps"))}{mm}</td>
  <td class="num">{_eps_cell(r.get("actual_eps_ttd"))}</td>
  <td class="num">{_drift_cell(r.get("drift_pct"), muted=bool(r.get("currency_suspect")))}</td>
  <td>{_flag_cell(r.get("flag", ""))}</td>
  <td class="left basis">{basis_html}</td>
</tr>"""


def render_variance(variance: Optional[dict]) -> str:
    if not variance:
        inner = ('<div class="placeholder">承保差異對照（現共識 EPS vs DD 承保 Base 路徑）尚無資料。'
                 '本區塊已預留版位，<code>variance.json</code> 產出後自動填入。</div>')
        return f"""<section class="block ph-block">
  <h2 class="block-h"><span class="dot dot-ph"></span>承保差異（Variance vs Underwriting）</h2>
  {inner}
</section>"""

    rows = list(variance.get("rows", []) or [])
    cov = variance.get("coverage", {}) or {}
    with_bp = cov.get("with_base_path", 0)
    n_rows = cov.get("rows", len(rows))
    # worst drift first（build_variance_tracker 已排序，仍防禦式再排一次）
    rows.sort(key=lambda r: (r.get("drift_pct") if isinstance(r.get("drift_pct"), (int, float)) else 0))
    has_mismatch = any(r.get("basis_mismatch") for r in rows)

    if not rows:
        body = '<tr><td colspan="8" class="empty">目前無可比對之 FY 列。</td></tr>'
    else:
        body = "\n".join(_var_row(r) for r in rows)

    mismatch_note = ('<span class="bmark">†</span> 該列 DD 口徑為 GAAP；yfinance 共識通常為 adjusted，'
                     '漂移方向仍算但幅度僅供參考。') if has_mismatch else ""

    return f"""<section class="block var-block">
  <h2 class="block-h"><span class="dot dot-var"></span>承保差異（Variance vs Underwriting） <span class="cnt">{n_rows} 列</span></h2>
  <div class="block-sub">
    以財年<b>截止日對齊</b>，把 DD dd-meta 承保的 <code>base_eps_path</code>（我們進場時對未來 EPS 的估計）
    對照<b>當下分析師共識</b>（yfinance）。<b>漂移% = 現共識 vs DD 承保 Base</b>，向下＝共識在下修、
    thesis 開始承壓，向上＝正向修正。
    <br><b>旗標</b>：
    <span class="vflag vf-green">🟢</span> |漂移| ≤ 5%（貼合承保）·
    <span class="vflag vf-up">🟢↑</span> 漂移 &gt; +5%（共識上修，不示警）·
    <span class="vflag vf-amber">🟡</span> −15% ≤ 漂移 &lt; −5%（下修留意）·
    <span class="vflag vf-red">🔴</span> 漂移 &lt; −15%（大幅下修）·
    <span class="vflag vf-cur">⚪</span> 幣別待確認（yfinance financialCurrency 與 DD 口徑幣別不合且 |漂移| &gt; 10%，
    疑為幣別假訊號，排除於 🔴/🟡 語義、交人工確認）。
    <br>覆蓋率：追蹤宇宙 <code>{with_bp}</code> 檔有 <code>base_eps_path</code>，<code>{n_rows}</code> 列可比對
    （超出 yfinance 0y/+1y 視野的 FY+2 及缺共識者記入 <code>variance.json</code> skipped[]）。
    {mismatch_note}
  </div>
  <div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">Ticker</th><th class="left">FY（截止）</th>
  <th>DD Base EPS</th><th>現共識 EPS</th><th>已報 EPS 累計</th>
  <th>漂移%</th><th>旗標</th><th class="left">口徑註記</th>
</tr></thead>
<tbody>
{body}
</tbody></table></div>
</section>"""


def _outcome_cell(e: dict) -> str:
    o = e.get("outcome")
    if not o:
        return '<span class="oc oc-pending">待複盤</span>'
    note = e.get("outcome_note") or ""
    note_html = f'<div class="watch">{escape(note)}</div>' if note else ""
    return f'<span class="oc oc-done">{escape(str(o))}</span>{note_html}'


def render_archive(archive: Optional[dict]) -> str:
    events = (archive or {}).get("events", []) or []
    # 最近 10 筆（日期最新在前）
    recent = sorted(events, key=lambda e: e.get("date", ""), reverse=True)[:ARCHIVE_SHOW]
    total = len(events)
    if not recent:
        body = '<tr><td colspan="6" class="empty">尚無已過事件。</td></tr>'
    else:
        body = "\n".join(
            f"""<tr>
  <td class="left nowrap">{escape(e["date"])}</td>
  <td class="left tk">{_ticker_link(e)}</td>
  <td class="left ev">{escape(e.get("event",""))}</td>
  <td>{_type_badge(e.get("type","other"))}</td>
  <td class="left">{_source_cell(e)}</td>
  <td class="left">{_outcome_cell(e)}</td>
</tr>""" for e in recent)
    return f"""<section class="block">
  <h2 class="block-h"><span class="dot dot-arch"></span>已過事件 · 複盤佇列 <span class="cnt">最近 {len(recent)} / 共 {total}</span></h2>
  <div class="block-sub">日期已過的事件滾入此處等待人工回填 outcome（結果 / 註記 / 知識帳本連結）。<b>outcome 欄為人工所有，週更 cron 永不覆寫</b>；未回填顯示「待複盤」。</div>
  <div class="tbl-wrap"><table>
<thead><tr>
  <th class="left">日期</th><th class="left">Ticker</th><th class="left">事件</th>
  <th>類型</th><th class="left">來源</th><th class="left">結果 outcome</th>
</tr></thead>
<tbody>
{body}
</tbody></table></div>
</section>"""


# ── style ─────────────────────────────────────────────────────────────────────
STYLE = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,'Noto Sans TC',sans-serif;background:#f0f5fb;color:#1e3a5f;line-height:1.5}
.hero{background:#fff;border-bottom:1px solid #dce8f5;padding:24px 32px 18px}
.hero-inner{max-width:min(1240px,96vw);margin:0 auto}
.hero-h1{font-size:22px;font-weight:600;color:#0f2a45;margin-bottom:6px}
.hero-sub{font-size:12.5px;color:#5a7a9a;line-height:1.7;max-width:940px}
.hero-stats{display:flex;gap:12px;margin-top:12px;flex-wrap:wrap}
.hero-stat{background:#f0f5fb;border:1px solid #dce8f5;border-radius:6px;padding:7px 11px;font-size:11px;color:#5a7a9a}
.hero-stat strong{color:#1e3a5f;font-size:13px;display:block;margin-bottom:1px}
.stale-banner{background:#fef2f2;border:1px solid #fecaca;color:#991b1b;border-radius:8px;padding:10px 14px;margin-top:12px;font-size:12.5px}
.wrap{max-width:min(1240px,96vw);margin:0 auto;padding:18px 32px 0}
.block{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:18px 20px;margin-bottom:18px}
.block-h{font-size:16px;font-weight:700;color:#0f2a45;margin-bottom:6px;display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.block-h .dot{width:10px;height:10px;border-radius:50%;background:#2563eb;flex-shrink:0}
.block-h .dot-warn{background:#d97706}.block-h .dot-arch{background:#64748b}.block-h .dot-ph{background:#a855f7}.block-h .dot-var{background:#0891b2}
.block-h .cnt{font-size:11px;font-weight:600;color:#94a3b8}
.block-sub{font-size:12px;color:#5a7a9a;line-height:1.7;margin-bottom:12px}
code{background:#f0f5fb;padding:1px 5px;border-radius:3px;font-size:11px;color:#1e3a5f}
.warn-block{border-color:#fde3c2;background:#fffcf7}
.ph-block{border-style:dashed;border-color:#e2d6f5;background:#fbf8ff}
.placeholder{font-size:12.5px;color:#8b6fb0;line-height:1.7;padding:6px 0}
.var-block{border-color:#c7e9f1;background:#f6fdff}
.var-block .dot-var{background:#0891b2}
td.num{text-align:right;font-variant-numeric:tabular-nums;color:#334e68;font-weight:600;white-space:nowrap}
.fye{color:#94a3b8;font-size:10.5px;font-weight:400}
.cur{font-size:9.5px;font-weight:700;color:#0e7490;background:#cffafe;border-radius:4px;padding:0 4px}
.na{color:#cbd5e1}
.basis{font-size:10.5px;color:#64748b}
.vflag{font-size:12px;white-space:nowrap}
.drift{font-weight:700;font-size:11.5px;font-variant-numeric:tabular-nums}
.dr-neg{color:#b91c1c}.dr-pos{color:#15803d}.dr-flat{color:#64748b}.dr-muted{color:#cbd5e1}
.vf-cur{filter:grayscale(1);opacity:.85}
.cur-suspect{font-size:10px;color:#b45309;line-height:1.5;margin-top:2px}
.bmark{color:#b45309;font-weight:700;cursor:help}
sup.bmark{font-size:9px}
/* highlight grid */
.hl-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.hl-card{border:1px solid #dce8f5;border-left:3px solid #2563eb;border-radius:8px;padding:10px 12px;background:#f9fcff}
.hl-date{font-size:11px;color:#64748b;font-variant-numeric:tabular-nums;font-weight:700}
.hl-main{margin:4px 0;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.hl-main a{color:#0f2a45;font-weight:700;text-decoration:none}
.hl-main a:hover{color:#2563eb;text-decoration:underline}
.hl-event{font-size:11.5px;color:#475569;line-height:1.5;margin-bottom:6px}
.hl-pos{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
/* tables */
.tbl-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:12px;margin-top:4px}
th{background:#f0f6ff;color:#5a7a9a;font-weight:700;padding:7px 9px;text-align:center;border-bottom:2px solid #dce8f5;font-size:10.5px;letter-spacing:.02em;white-space:nowrap}
th.left{text-align:left}
td{padding:8px 9px;text-align:center;border-bottom:1px solid #f0f5fb;vertical-align:top}
td.left{text-align:left}
td.nowrap{white-space:nowrap;font-variant-numeric:tabular-nums;color:#334e68;font-weight:600}
td.tk a{color:#2563eb;text-decoration:none;font-weight:700}
td.tk a:hover{text-decoration:underline}
td.ev{color:#334e68;line-height:1.55;max-width:420px}
.watch{font-size:10.5px;color:#94a3b8;line-height:1.5;margin-top:3px}
.role{font-size:10px;color:#64748b}
/* badges */
.typ{font-size:10px;font-weight:700;padding:1px 7px;border-radius:99px;white-space:nowrap;background:#eef2f7;color:#475569}
.typ-earnings{background:#dbeafe;color:#1e40af}
.typ-dd_expiry{background:#fef3c7;color:#92400e}
.typ-regulatory{background:#fee2e2;color:#991b1b}
.typ-product{background:#dcfce7;color:#166534}
.typ-macro{background:#f3e8ff;color:#6b21a8}
.typ-capacity{background:#cffafe;color:#0e7490}
.typ-guidance{background:#ffe4e6;color:#9f1239}
.imp{font-size:10.5px;font-weight:700;padding:1px 7px;border-radius:4px;white-space:nowrap}
.imp-hi{background:#fee2e2;color:#b91c1c}.imp-mid{background:#fef3c7;color:#a16207}.imp-lo{background:#f1f5f9;color:#64748b}
.verdict{padding:1px 8px;border-radius:99px;font-size:10.5px;font-weight:700;white-space:nowrap}
.v-in{background:#dcfce7;color:#166534}.v-watch{background:#fef3c7;color:#92400e}
.v-avoid{background:#fee2e2;color:#991b1b}.v-none{background:#f1f5f9;color:#94a3b8;font-weight:600}
.src{font-size:10.5px;font-weight:600;padding:1px 6px;border-radius:4px;white-space:nowrap}
.src-yfinance{background:#e0edff;color:#1d4ed8}.src-dd-meta{background:#e6f4ea;color:#15803d}
.src-s15_static{background:#f1f5f9;color:#64748b}
.stale-flag{font-size:9.5px;font-weight:700;color:#b45309;background:#fef3c7;border-radius:4px;padding:0 5px;white-space:nowrap;cursor:help}
.pv-link{font-size:10.5px;font-weight:700;color:#1e40af;background:#dbeafe;border-radius:4px;padding:1px 6px;white-space:nowrap;text-decoration:none}
.pv-link:hover{background:#bfdbfe;text-decoration:none}
.pv-frozen{font-size:10.5px;font-weight:700;color:#475569;background:#e2e8f0;border-radius:4px;padding:1px 6px;white-space:nowrap;cursor:help}
.dp{color:#94a3b8;cursor:help}
.oc{font-size:11px;font-weight:700;padding:1px 7px;border-radius:4px;white-space:nowrap}
.oc-pending{background:#f1f5f9;color:#94a3b8}.oc-done{background:#dcfce7;color:#166534}
.empty{padding:14px;text-align:center;color:#94a3b8;font-size:12px;font-style:italic}
.footer{padding:24px 32px;font-size:11px;color:#94a3b8;line-height:1.7;max-width:min(1240px,96vw);margin:0 auto}
.footer code{background:#eef4fb;padding:1px 5px;border-radius:3px;font-size:10px}
.footer .err{color:#b91c1c}
@media(max-width:760px){.wrap,.hero,.footer{padding-left:14px;padding-right:14px}}
"""


def build(dry_run: bool = False) -> int:
    print(f"=== Catalyst-page build · {_now_taipei_iso()} ===\n")
    calendar = _load(CALENDAR_JSON)
    if not calendar:
        print(f"  ERR: {CALENDAR_JSON} missing — 先跑 build_catalyst_calendar.py", file=sys.stderr)
        return 2
    archive = _load(ARCHIVE_JSON)
    variance = _load(VARIANCE_JSON)

    events = calendar.get("events", []) or []
    skipped = calendar.get("skipped", []) or []
    errors = calendar.get("errors", []) or []
    universe_count = calendar.get("universe_count", 0)
    stale = bool(calendar.get("stale"))
    today = date.today()

    n_earn = sum(1 for e in events if e["type"] == "earnings")
    n_cat = sum(1 for e in events if e["source"] == "dd-meta")
    n_exp = sum(1 for e in events if e["type"] == "dd_expiry")
    print(f"  forward={len(events)} (earnings={n_earn} dd-meta={n_cat} expiry={n_exp}) "
          f"universe={universe_count} skipped={len(skipped)} errors={len(errors)} stale={stale}")

    stale_banner = ""
    if stale:
        stale_banner = ('<div class="stale-banner">⚠ <b>資料標記為 stale</b>：本次更新所有 yfinance '
                        '財報日查詢皆失敗，以下前瞻財報日沿用上一版（非本次即時抓取），dd-meta 催化劑與保質期不受影響。</div>')

    highlight_html = render_highlight(events, today)
    forward_html = render_forward_table(events)
    expiry_html = render_expiry(events)
    variance_html = render_variance(variance)
    archive_html = render_archive(archive)

    gen = calendar.get("generated_at")
    err_line = ""
    if errors:
        tks = "、".join(escape(e.get("ticker", "?")) for e in errors)
        err_line = f'<p class="err">yfinance 未取得財報日（{len(errors)}）：{tks} — 已退回 §15 靜態備援或略過，不捏造日期。</p>'
    skip_line = ""
    if skipped:
        skip_line = f'<p>catalysts 格式問題略過 {len(skipped)} 筆（skipped[] 記錄於 calendar.json）。</p>'

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>前瞻催化劑日曆 — 財報日 × DD 結構化催化劑 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<style>{STYLE}</style>
</head>
<body>
{NAV_BLOCK}

<div class="hero">
  <div class="hero-inner">
    <div class="hero-h1">📅 前瞻催化劑日曆</div>
    <div class="hero-sub">
      前瞻事件日曆：財報日與 DD 內結構化催化劑，週更。彙整 yfinance 即時財報日、dd-meta 結構化催化劑、
      DD §15 保質期三來源，收斂成一張「未來哪天、哪檔、什麼事、我們現在的立場」的時間表。
    </div>
    {stale_banner}
    <div class="hero-stats">
      <div class="hero-stat"><strong>{_fmt_stamp(gen)}</strong>最後更新（台北）</div>
      <div class="hero-stat"><strong>{universe_count}</strong>追蹤宇宙</div>
      <div class="hero-stat"><strong>{len(events)}</strong>前瞻事件</div>
      <div class="hero-stat"><strong>{n_earn}</strong>財報日</div>
      <div class="hero-stat"><strong>{n_exp}</strong>保質期警示</div>
    </div>
  </div>
</div>

<div class="wrap">
{highlight_html}
{forward_html}
{expiry_html}
{variance_html}
{archive_html}
</div>

<div class="footer">
  <p><b>覆蓋率</b>：追蹤宇宙 <code>{universe_count}</code> 檔（v13/v14 latest 且 DD ≤90 天或裁決＝進場）·
  前瞻事件 <code>{len(events)}</code> 筆 · skipped <code>{len(skipped)}</code> · errors <code>{len(errors)}</code>。</p>
  {err_line}
  {skip_line}
  <p style="margin-top:8px"><b>資料來源</b>：<code>docs/catalyst/calendar.json</code>（前瞻）·
  <code>archive.json</code>（已過＋人工 outcome）· <code>earnings_cache.json</code>（yfinance 7 天 TTL）。
  財報日 ≠ 買賣訊號；財報前 5 個交易日靜默期禁新倉。</p>
  <p style="margin-top:10px;color:#cbd5e1">Generated by <code>scripts/build_catalyst_page.py</code></p>
</div>
</body>
</html>
"""

    if dry_run:
        print(f"\n  (dry-run) would write {HTML_OUT} ({len(html):,} bytes)")
        return 0

    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"\n  ✓ Wrote {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="不寫檔")
    args = p.parse_args()
    return build(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
