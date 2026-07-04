#!/usr/bin/env python3
"""SOP 漏斗頁 server-render（沿用 dd-screener 家族頁面 CSS 慣例）。"""
from __future__ import annotations

import html
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Canonical site header (single source: scripts/site_nav.py)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from site_nav import DD_SCREENER_SUBNAV, build_subnav, full_nav_block  # noqa: E402

# Canonical site header + dd-screener sub-nav for this page
NAV_BLOCK = full_nav_block(
    "quant", "dds", build_subnav(DD_SCREENER_SUBNAV, "/dd-screener/sop-funnel.html")
)


_TAIPEI = timezone(timedelta(hours=8))


def _updated_taipei(run_ts: str) -> str:
    """UTC ISO run_timestamp → 台北時間 'YYYY-MM-DD HH:MM'（含幾點幾分）。"""
    try:
        dt = datetime.strptime(run_ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return dt.astimezone(_TAIPEI).strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return run_ts


# ── 顯示層圈數字替換（①-⑤ 小字級下不可讀；資料層內部表示不動）──
_CIRCLED = {"①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5"}


def _plain_states(html_text: str) -> str:
    for k, v in _CIRCLED.items():
        html_text = html_text.replace(k, v)
    return html_text


def _e(v) -> str:
    return html.escape(str(v)) if v is not None else "—"


def _pct(v, signed=True) -> str:
    if v is None:
        return "—"
    return f"{v:+.1f}%" if signed else f"{v:.1f}%"


def _cls(v) -> str:
    if v is None:
        return ""
    return "pos" if v > 0 else ("neg" if v < 0 else "")


def _dd_link(ev) -> str:
    p = ev.get("dd_path")
    return f'<a href="/{_e(p)}" target="_blank">DD</a>' if p else "—"


_ST_COLOR = {"1": "#059669", "2": "#ca8a04", "3": "#ea580c", "4": "#b45309", "5": "#dc2626"}


def _state_badge(st) -> str:
    d = _CIRCLED.get(st, st)
    if d in _ST_COLOR:
        return (f'<span style="font-weight:800;font-size:13px;color:{_ST_COLOR[d]}">'
                f'態{d}</span>')
    return _e(st)


def _signal_rows(evs) -> str:
    if not evs:
        return '<tr><td colspan="8" class="empty">今日無訊號 — 系統在等，不是壞了</td></tr>'
    out = []
    for e in evs:
        star = " ⭐" if e.get("base_star") else ""
        base = f'{e["base_age_weeks"]:.0f}w' if e.get("base_age_weeks") else \
            (f'錨 {e["anchor_a1_date"]}' if e.get("anchor_a1_date") else "—")
        out.append(
            f'<tr><td class="left"><strong>{_e(e["ticker"])}</strong> {_e(e.get("name") or "")}</td>'
            f'<td><span class="tag tag-{e["entry_type"].lower()}">{e["entry_type"]}{star}</span></td>'
            f'<td>{base}</td><td>{e["signal_close"]:,.1f}</td>'
            f'<td>{_pct(-(e["stop_dist_pct"] or 0)) if e.get("stop_dist_pct") else "—"}</td>'
            f'<td>{_e(e.get("suggested_position_pct"))}%</td>'
            f'<td>{_warn_tags(e)}</td>'
            f'<td>{_dd_link(e)}</td></tr>')
    return "".join(out)


def _warn_tags(e) -> str:
    tags = []
    if e.get("moat_review_due"):
        tags.append('<span class="warn-tag">護城河待複檢</span>')
    if e.get("earnings_check") == "silent":
        tags.append('<span class="warn-tag">財報窗內</span>')
    if e.get("earnings_check") == "unverified":
        tags.append('<span class="warn-tag">財報日未驗</span>')
    return "".join(tags) or "—"


def _veto_rows(evs) -> str:
    if not evs:
        return ""
    rows = "".join(
        f'<tr><td class="left">{_e(e["ticker"])}</td>'
        f'<td><span class="tag tag-{e["entry_type"].lower()}">{e["entry_type"]}</span></td>'
        f'<td>{e["signal_close"]:,.1f}</td>'
        f'<td class="left veto">{_e("；".join(e["vetoes"]))}</td></tr>'
        for e in evs)
    return (f'<details class="veto-box"><summary>今日否決 {len(evs)} 筆（創新高/站回但被五問擋下）</summary>'
            f'<table><thead><tr><th class="left">ticker</th><th>型態</th><th>訊號價</th>'
            f'<th class="left">否決原因</th></tr></thead><tbody>{rows}</tbody></table></details>')


def _veto_distribution_block(vd) -> str:
    """否決原因分布小統計區塊（帳本累計 + 近 30 日）。"""
    if not vd or not vd.get("by_reason"):
        return ""
    mentions = sum(x["count"] for x in vd["by_reason"]) or 1
    recent_map = {x["reason"]: x["count"] for x in vd.get("recent_by_reason", [])}
    palette = ["#b45309", "#0369a1", "#7c3aed", "#0f766e", "#be185d"]
    bars = ""
    for i, x in enumerate(vd["by_reason"]):
        pct = x["count"] / mentions * 100
        rec = recent_map.get(x["reason"], 0)
        bars += (
            f'<div class="vd-row"><div class="vd-label">{_e(x["reason"])}</div>'
            f'<div class="vd-track"><div class="vd-fill" '
            f'style="width:{pct:.0f}%;background:{palette[i % len(palette)]}"></div></div>'
            f'<div class="vd-val">{x["count"]} 筆 · {pct:.0f}%'
            f'<span class="vd-rec">近30日 {rec}</span></div></div>')
    return (
        f'<details class="vd-box" open><summary>否決原因分布 — 帳本累計 {vd["total"]} 筆'
        f'（近 {vd["recent_window_days"]} 日 {vd["recent_total"]} 筆）</summary>'
        f'<div class="vd-wrap">{bars}</div>'
        f'<div class="vd-note">否決＝五條件已過、技術型態觸發，但進場當下被態勢守則擋下。'
        f'態2過熱＝價格離均線過遠，不追高、等回踩；價≤52週線／排列不正＝尚未進入健康多頭。</div>'
        f'</details>')


def _performance_block(p) -> str:
    """6/1 起策略淨值 vs SPY — 內嵌 SVG 折線圖 + 摘要 + 持倉貢獻。"""
    if not p or not p.get("series") or len(p["series"]) < 2:
        return ""
    s, cap = p["series"], float(p["capital"])
    navs = [r["nav"] for r in s]
    spys = [r["spy"] for r in s]
    lo, hi = min(min(navs), min(spys)), max(max(navs), max(spys))
    if hi == lo:
        hi = lo + 1
    span = (hi - lo) * 0.14
    lo, hi = lo - span, hi + span
    W, H, pl, pr, pt, pb = 760, 280, 56, 16, 16, 30
    n = len(s)
    fx = lambda i: pl + (W - pl - pr) * (i / (n - 1))
    fy = lambda v: pt + (H - pt - pb) * (1 - (v - lo) / (hi - lo))
    nav_pts = " ".join(f"{fx(i):.1f},{fy(r['nav']):.1f}" for i, r in enumerate(s))
    spy_pts = " ".join(f"{fx(i):.1f},{fy(r['spy']):.1f}" for i, r in enumerate(s))
    grid = ""
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        y = fy(v)
        grid += (f'<line x1="{pl}" y1="{y:.1f}" x2="{W - pr}" y2="{y:.1f}" class="pf-grid"/>'
                 f'<text x="{pl - 7}" y="{y + 3:.1f}" class="pf-ytick">{(v / cap - 1) * 100:+.1f}%</text>')
    yb = fy(cap)
    base = f'<line x1="{pl}" y1="{yb:.1f}" x2="{W - pr}" y2="{yb:.1f}" class="pf-base"/>'
    xticks = (f'<text x="{fx(0):.1f}" y="{H - 9}" class="pf-xtick" text-anchor="start">{_e(s[0]["date"][5:])}</text>'
              f'<text x="{fx(n - 1):.1f}" y="{H - 9}" class="pf-xtick" text-anchor="end">{_e(s[-1]["date"][5:])}</text>')
    svg = (f'<svg viewBox="0 0 {W} {H}" class="pf-svg" preserveAspectRatio="none" role="img" '
           f'aria-label="策略淨值 vs SPY">{grid}{base}'
           f'<polyline points="{spy_pts}" class="pf-spy"/>'
           f'<polyline points="{nav_pts}" class="pf-nav"/>{xticks}</svg>')

    sm = p["summary"]
    cr = p.get("cash_rate") or {}
    apr = sm.get("cash_apr_pct", 0)
    rate_src = (f'{cr["bm_ticker"]} {cr["bm"]:.2f}%−{cr.get("spread_pct", 0.5):g}%'
                if cr.get("bm") is not None else "IBKR 公告")
    win = sm["excess_pp"] >= 0
    cap_m = f'${cap / 1e6:.0f}M'
    stat = (
        f'<div class="pf-stats">'
        f'<div class="pf-stat"><span>策略淨值</span><strong>${sm["strategy_value"]:,.0f}</strong>'
        f'<em class="{"pos" if sm["strategy_ret_pct"] >= 0 else "neg"}">{sm["strategy_ret_pct"]:+.2f}%</em></div>'
        f'<div class="pf-stat"><span>SPY 基準</span><strong>${sm["spy_value"]:,.0f}</strong>'
        f'<em class="{"pos" if sm["spy_ret_pct"] >= 0 else "neg"}">{sm["spy_ret_pct"]:+.2f}%</em></div>'
        f'<div class="pf-stat"><span>超額 (vs SPY)</span><strong class="{"pos" if win else "neg"}">{sm["excess_pp"]:+.2f}pp</strong>'
        f'<em>投入 {sm["invested_pct"]:.1f}% · 現金 {sm["cash_pct"]:.1f}%</em></div>'
        f'<div class="pf-stat"><span>現金利息（IBKR {apr:.2f}% p.a.）</span>'
        f'<strong class="pos">+${sm.get("interest_usd", 0):,.0f}</strong>'
        f'<em>{_e(rate_src)} · 閒置 USD &gt;$10k</em></div>'
        f'</div>')
    prows = "".join(
        f'<tr><td class="left"><strong>{_e(pp["ticker"])}</strong> '
        f'<span class="tag tag-{pp["entry_type"].lower()}">{pp["entry_type"]}</span></td>'
        f'<td>{_e(pp["entry_date"][5:])}</td><td>{pp["weight_pct"]:.2f}%</td>'
        f'<td>${pp["alloc_usd"]:,.0f}</td>'
        f'<td class="{"pos" if (pp["ret_pct"] or 0) >= 0 else "neg"}">{(pp["ret_pct"] or 0):+.1f}%</td>'
        f'<td class="{"pos" if pp["pnl_usd"] >= 0 else "neg"}">{pp["pnl_usd"]:+,.0f}</td>'
        f'<td>{_e(pp.get("state") or "—")}</td></tr>'
        for pp in p["positions"])
    ptable = (f'<table class="pf-pos"><thead><tr><th class="left">ticker</th><th>進場</th>'
              f'<th>部位%</th><th>配置$</th><th>報酬</th><th>損益$</th><th>態</th></tr></thead>'
              f'<tbody>{prows}</tbody></table>') if p["positions"] else ""
    return (
        f'<div class="section"><div class="card">'
        f'<h2>📈 6/1 起策略淨值 vs SPY（起始資金 {cap_m}）</h2>'
        f'<div class="desc">起始 {cap_m} 個股部，照 SOP 全交易設定（T+1 進場 · 部位 = min(10%, 1.5%÷停損) · '
        f'態③減1/3 · 態④減碼+回補 · 態⑤全出）逐日 mark-to-market；未投入現金照 IBKR 閒置資金利率 '
        f'{p.get("cash_apr_pct", 0):.2f}% p.a.（{_e(rate_src)}，自動跟基準）計息（USD、&gt;$10k、Actual/360）。'
        f'基準 SPY 同起始資金、{_e(p["start"])} 為基期。日序列由 sim legs 重建，與 §3/§4 一致。</div>'
        f'<div class="pf-legend"><span class="pf-lg-nav">策略 NAV</span>'
        f'<span class="pf-lg-spy">SPY</span><span class="pf-lg-base">基期 {cap_m}</span></div>'
        f'{svg}{stat}{ptable}'
        f'<div class="pf-note">截至 {_e(p["as_of"])}（x 軸取 SPY 交易日，兩端對齊）。'
        f'現金部位主導 → 空頭時抗跌，多頭時跟不上；樣本小，僅追蹤非結論。</div>'
        f'</div></div>')


def _standby_table(rows, cols, empty_msg) -> str:
    if not rows:
        return f'<div class="empty">{empty_msg}</div>'
    head = "".join(f'<th class="{c[2]}">{c[0]}</th>' for c in cols)
    body = "".join(
        "<tr>" + "".join(f'<td class="{c[2]}">{c[1](r)}</td>' for c in cols) + "</tr>"
        for r in rows)
    return f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def _open_rows(evs) -> str:
    if not evs:
        return '<tr><td colspan="9" class="empty">尚無模擬持倉</td></tr>'
    out = []
    for e in sorted(evs, key=lambda x: x["entry_date"], reverse=True):
        s = e["sim"]
        legs = "；".join(f'{l["reason"]}@{l["price"]:,.0f}' for l in s["legs"]) or "—"
        flo = (s["last_price"] / s["entry_close"] - 1) * 100 if s.get("last_price") else None
        out.append(
            f'<tr><td class="left"><strong>{_e(e["ticker"])}</strong></td>'
            f'<td><span class="tag tag-{e["entry_type"].lower()}">{e["entry_type"]}</span></td>'
            f'<td>{_e(e["entry_date"])}</td><td>{s["entry_close"]:,.1f}</td>'
            f'<td>{_state_badge(s["current_state"])}'
            + (f'<span class="pending-tag">{_e(s["pending_action"])}·明日收盤執行</span>'
               if s.get("pending_action") else '')
            + f'</td><td>{s["current_fraction"] * 100:.0f}%</td>'
            f'<td class="{_cls(flo)}">{_pct(flo)}</td>'
            f'<td class="{_cls(s.get("alpha_pct"))}">{_pct(s.get("alpha_pct"))}</td>'
            f'<td class="left legs">{legs}</td></tr>')
    return "".join(out)


def _closed_rows(evs) -> str:
    if not evs:
        return '<tr><td colspan="9" class="empty">尚無已平倉 trade</td></tr>'
    out = []
    for e in sorted(evs, key=lambda x: x["sim"]["exit_date"] or "", reverse=True):
        s = e["sim"]
        out.append(
            f'<tr><td class="left"><strong>{_e(e["ticker"])}</strong></td>'
            f'<td><span class="tag tag-{e["entry_type"].lower()}">{e["entry_type"]}</span></td>'
            f'<td>{_e(e["entry_date"])}</td><td>{_e(s["exit_date"])}</td>'
            f'<td>{_e(s["exit_reason"])}</td>'
            f'<td class="{_cls(s["ret_pct"])}">{_pct(s["ret_pct"])}</td>'
            f'<td>{_e(s["r_multiple"])}</td>'
            f'<td class="{_cls(s.get("alpha_pct"))}">{_pct(s.get("alpha_pct"))}</td>'
            f'<td>{s["holding_days"]}d</td></tr>')
    return "".join(out)


def _score_cards(sb) -> str:
    label = {"A1": "A1 起漲型（主訊號）", "A2": "A2 續勢型（對照）", "B": "B 第二班車",
             "C": "C 冷卻再武裝（觀察期）"}
    cards = []
    for k in ("A1", "A2", "B", "C"):
        if k not in sb:
            continue
        a = sb[k]
        conv = (a["entered"] / a["signals"] * 100) if a["signals"] else None
        thin = '<span class="thin-flag">樣本未熟（closed&lt;20）</span>' if a["thin"] else ""
        stat_cls = "muted" if a["thin"] else ""
        cards.append(f"""<div class="score-card {stat_cls}">
<h3>{label[k]} {thin}</h3>
<div class="score-grid">
<div><span>訊號</span><strong>{a["signals"]}</strong></div>
<div><span>否決</span><strong>{a["vetoed"]}</strong></div>
<div><span>進場(轉換)</span><strong>{a["entered"]}{f' ({conv:.0f}%)' if conv is not None else ''}</strong></div>
<div><span>持有中</span><strong>{a["open"]}</strong></div>
<div><span>已平倉</span><strong>{a["closed"]}</strong></div>
<div><span>勝率</span><strong>{_pct(a["win_rate"], signed=False)}</strong></div>
<div><span>中位報酬</span><strong>{_pct(a["median_ret_pct"])}</strong></div>
<div><span>α vs SPY</span><strong>{_pct(a["mean_alpha_pct"])}</strong></div>
<div><span>平均 R</span><strong>{_e(a["mean_r"])}</strong></div>
</div></div>""")
    return "".join(cards)


def _backtest_block(bt) -> str:
    if not bt:
        return ('<div class="empty">5 年歷史回測尚未產出 — 跑 '
                '<code>python3 scripts/sop_funnel/backtest.py</code></div>')
    rows = []
    for variant, m in bt.get("variants", {}).items():
        rows.append(
            f'<tr><td class="left">{_e(m.get("label", variant))}</td>'
            f'<td>{m["n_trades"]}</td><td>{_pct(m["win_rate"], signed=False)}</td>'
            f'<td class="{_cls(m["median_ret_pct"])}">{_pct(m["median_ret_pct"])}</td>'
            f'<td class="{_cls(m["mean_ret_pct"])}">{_pct(m["mean_ret_pct"])}</td>'
            f'<td class="{_cls(m.get("mean_alpha_pct"))}">{_pct(m.get("mean_alpha_pct"))}</td>'
            f'<td>{_e(m.get("mean_r"))}</td><td>{_e(m.get("median_holding_days"))}d</td></tr>')
    per_type = ""
    if bt.get("by_type"):
        tr = "".join(
            f'<tr><td class="left">{k}</td><td>{v["n_trades"]}</td>'
            f'<td>{_pct(v["win_rate"], signed=False)}</td>'
            f'<td class="{_cls(v["median_ret_pct"])}">{_pct(v["median_ret_pct"])}</td>'
            f'<td class="{_cls(v.get("mean_alpha_pct"))}">{_pct(v.get("mean_alpha_pct"))}</td></tr>'
            for k, v in bt["by_type"].items())
        per_type = (f'<h4>訊號型態拆分（現行規則）</h4><table><thead><tr><th class="left">型態</th>'
                    f'<th>trades</th><th>勝率</th><th>中位報酬</th><th>α vs SPY</th></tr></thead>'
                    f'<tbody>{tr}</tbody></table>')
    return (f'<p class="bt-meta">窗口 {_e(bt.get("window_start"))} → {_e(bt.get("window_end"))} · '
            f'universe {bt.get("n_tickers")} 檔 · ⚠ 質量閘門凍結今日值（survivorship 偏誤，僅供參考）</p>'
            f'<table><thead><tr><th class="left">態④變體</th><th>trades</th><th>勝率</th>'
            f'<th>中位報酬</th><th>平均報酬</th><th>α vs SPY</th><th>平均R</th><th>中位持有</th>'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table>{per_type}')


def _grade_badge(g, trend) -> str:
    color = {"S": "#7c2d12", "A": "#166534", "B": "#1e40af"}.get(g, "#64748b")
    tcolor = {"↑": "#059669", "↓": "#dc2626"}.get(trend, "#94a3b8")
    return (f'<span style="font-weight:700;color:{color}">{_e(g)}</span>'
            f'<span style="color:{tcolor};margin-left:3px">{_e(trend)}</span>')


def _population_block(pop, excluded) -> str:
    if not pop:
        return '<div class="empty">母體為空</div>'
    rows = []
    for r in pop:
        st = "態① ✓" if r["state1"] else "✗" + "、".join(r["state1_fails"])
        st_cls = "pos" if r["state1"] else ""
        rows.append(
            f'<tr><td class="left"><strong>{_e(r["ticker"])}</strong> {_e(r.get("name") or "")}'
            + ('<span class="warn-tag">待複檢</span>' if r.get("moat_review_due") else '')
            + f'</td>'
            f'<td>{_grade_badge(r["moat_grade"], r["moat_trend"])} <span style="color:#94a3b8">{_e(r["moat_score"])}</span></td>'
            f'<td>{_e(r.get("signal"))}</td>'
            f'<td>{_e(round(r["cagr"], 0)) if r.get("cagr") is not None else "—"}</td>'
            f'<td>{_e(round(r["roic"], 0)) if r.get("roic") is not None else "—"}</td>'
            f'<td>{_e(round(r["fcf"], 1)) if r.get("fcf") is not None else "—"}</td>'
            f'<td>{_e(round(r["peg"], 2)) if r.get("peg") is not None else "—"}</td>'
            f'<td>{_pct(r["dist_ath_pct"])}</td>'
            f'<td class="left {st_cls}" style="font-size:10.5px">{_e(st)}</td>'
            f'<td>{_dd_link(r)}</td></tr>')
    recon = ""
    if excluded:
        items = "、".join(
            f'{_e(e["ticker"])}（{_grade_badge(e["moat_grade"], e["moat_trend"])}'
            f'，{_e("、".join(e["moat_cut"]))}）' for e in excluded)
        recon = (f'<div class="exceeded">四質量條件通過、被護城河 gate 擋下 {len(excluded)} 檔'
                 f'（{len(pop)}＋{len(excluded)} = 四條件母體）：{items}</div>')
    return (f'<table><thead><tr><th class="left">ticker</th><th>護城河</th><th>訊號</th>'
            f'<th>CAGR</th><th>ROIC</th><th>FCFm</th><th>PEG</th><th>距ATH</th>'
            f'<th class="left">週線態勢</th><th>報告</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>{recon}')


def render_page(d: dict) -> str:
    a1_cols = [
        ("ticker", lambda r: f'<strong>{_e(r["ticker"])}</strong> {_e(r.get("name") or "")}', "left"),
        ("距ATH", lambda r: _pct(r["dist_ath_pct"]), ""),
        ("基期", lambda r: f'{r["ath_age_weeks"]:.0f}w' + (" ⭐" if r["ath_age_weeks"] >= 52 else ""), ""),
        ("DD", _dd_link, ""),
    ]
    b_cols = [
        ("ticker", lambda r: f'<strong>{_e(r["ticker"])}</strong>', "left"),
        ("錨(A1)", lambda r: _e(r["anchor_date"]), ""),
        ("錨齡", lambda r: f'{r["weeks_since_anchor"]:.0f}w' + ("（已超窗）" if r["exceeded"] else ""), ""),
        ("回踩深度", lambda r: _pct(r["pullback_pct"]), ""),
        ("距60MA", lambda r: _pct(r.get("dist_60ma_pct")), ""),
    ]
    bb_cols = [
        ("ticker", lambda r: f'<strong>{_e(r["ticker"])}</strong> {_e(r.get("name") or "")}', "left"),
        ("距ATH", lambda r: _pct(r["dist_ath_pct"]), ""),
        ("已築基", lambda r: f'{r["ath_age_weeks"]:.0f}w', ""),
        ("DD", _dd_link, ""),
    ]
    c_cols = [
        ("ticker", lambda r: f'<strong>{_e(r["ticker"])}</strong>', "left"),
        ("原訊號", lambda r: f'{_e(r["armed_type"])} @ {_e(r["armed_date"])}', ""),
        ("武裝週數", lambda r: f'{r["weeks_since_armed"]:.0f}w', ""),
        ("距+2σ帶", lambda r: _pct(r.get("dist_bb2_pct")), ""),
        ("DD", _dd_link, ""),
    ]
    standby_b_rows = [r for r in d["standby_b"]]
    b_html = _standby_table(
        [r for r in standby_b_rows if not r["exceeded"]], b_cols, "無 B 武裝中標的")
    b_exceeded = [r for r in standby_b_rows if r["exceeded"]]
    if b_exceeded:
        b_html += ('<div class="exceeded">已超窗（看得見、不給訊號）：'
                   + "、".join(f'{r["ticker"]}（錨齡 {r["weeks_since_anchor"]:.0f}w，'
                               f'回踩 {_pct(r["pullback_pct"])}）' for r in b_exceeded)
                   + "</div>")
    a2_block = ""
    if d["standby_a2"]:
        a2_rows = "、".join(f'{r["ticker"]}（距ATH {_pct(r["dist_ath_pct"])}，基期 '
                            f'{r["ath_age_weeks"]:.0f}w）' for r in d["standby_a2"])
        a2_block = (f'<details class="a2-box"><summary>A2 續勢待命 {len(d["standby_a2"])} 檔'
                    f'（距ATH ≤5% 但基期 &lt;26 週 — 趨勢中段，非起漲）</summary>'
                    f'<div class="a2-list">{a2_rows}</div></details>')
    insuf = ""
    if d["insufficient_history"]:
        insuf = ('<div class="exceeded">歷史不足（&lt;200 週，無法判定週線排列）：'
                 + "、".join(r["ticker"] for r in d["insufficient_history"]) + "</div>")

    return _plain_states(f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pure MA SOP 漏斗 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:#f0f5fb;color:#1e3a5f;line-height:1.5}}
.hero{{background:#fff;border-bottom:1px solid #dce8f5;padding:24px 32px 18px}}
.hero-inner{{max-width:min(1400px,96vw);margin:0 auto}}
.hero-h1{{font-size:22px;font-weight:600;color:#0f2a45;margin-bottom:6px}}
.hero-sub{{font-size:12px;color:#5a7a9a;line-height:1.6;max-width:980px}}
.hero-stats{{display:flex;gap:14px;margin-top:12px;flex-wrap:wrap}}
.hero-stat{{background:#f0f5fb;border:1px solid #dce8f5;border-radius:6px;padding:7px 11px;font-size:11px;color:#5a7a9a}}
.hero-stat strong{{color:#1e3a5f;font-size:13px;display:block}}
.section{{max-width:min(1400px,96vw);margin:0 auto;padding:20px 32px 4px}}
.card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:16px 18px;margin-bottom:20px}}
.card h2{{font-size:16px;font-weight:700;margin-bottom:4px;color:#0f2a45}}
.card .desc{{font-size:12px;color:#5a7a9a;margin-bottom:12px;line-height:1.6}}
table{{width:100%;border-collapse:collapse;font-size:11.5px}}
th{{background:#f0f6ff;color:#5a7a9a;font-weight:700;padding:7px 8px;text-align:right;border-bottom:2px solid #dce8f5;font-size:10px;white-space:nowrap}}
th.left{{text-align:left}}
td{{padding:7px 8px;text-align:right;border-bottom:1px solid #f0f5fb;font-variant-numeric:tabular-nums}}
td.left{{text-align:left;font-weight:500}}
td.legs{{font-size:10.5px;color:#5a7a9a}}
td.veto{{color:#b45309;font-size:11px}}
.pos{{color:#059669;font-weight:600}}.neg{{color:#dc2626;font-weight:600}}
.empty{{color:#8aa5c0;font-size:12px;text-align:center;padding:14px}}
.tag{{display:inline-block;padding:1px 8px;border-radius:4px;font-size:10.5px;font-weight:700}}
.tag-a1{{background:#dcfce7;color:#166534}}
.tag-a2{{background:#e0e7ff;color:#3730a3}}
.tag-b{{background:#fef3c7;color:#92400e}}
.tag-c{{background:#ede9fe;color:#5b21b6}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}}
.grid3 h3,.score-card h3{{font-size:13px;font-weight:700;color:#0f2a45;margin-bottom:8px}}
.score-card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:14px 16px}}
.score-card.muted .score-grid strong{{color:#94a3b8}}
.score-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font-size:11px}}
.score-grid span{{color:#8aa5c0;display:block;font-size:10px}}
.score-grid strong{{font-size:14px;color:#0f2a45}}
.thin-flag{{font-size:10px;background:#f1f5f9;color:#64748b;padding:2px 8px;border-radius:4px;font-weight:600}}
.exceeded{{font-size:11px;color:#8aa5c0;margin-top:10px;line-height:1.7}}
.warn-tag{{display:inline-block;margin-left:6px;padding:1px 6px;border-radius:4px;font-size:9.5px;font-weight:700;background:#fef3c7;color:#92400e}}
.pending-tag{{display:block;font-size:9.5px;color:#b45309;font-weight:600}}
.prereg{{background:#f0f9ff;border:1px solid #bae6fd;border-radius:8px;padding:10px 14px;font-size:11.5px;color:#0c4a6e;line-height:1.7;margin-bottom:14px}}
.prereg strong{{display:inline;margin-right:6px}}
.vd-box{{margin-top:14px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:10px 14px}}
.vd-box>summary{{color:#92400e;font-weight:700;font-size:12px}}
.vd-wrap{{margin-top:11px;display:flex;flex-direction:column;gap:7px;max-width:580px}}
.vd-row{{display:grid;grid-template-columns:92px 1fr auto;align-items:center;gap:10px;font-size:11px}}
.vd-label{{color:#78350f;font-weight:600;text-align:right;white-space:nowrap}}
.vd-track{{background:#fef3c7;border-radius:5px;height:14px;overflow:hidden}}
.vd-fill{{height:100%;border-radius:5px;min-width:2px}}
.vd-val{{color:#92400e;white-space:nowrap;font-variant-numeric:tabular-nums}}
.vd-rec{{color:#b9893f;margin-left:8px}}
.vd-note{{font-size:10.5px;color:#a16207;margin-top:10px;line-height:1.6;max-width:700px}}
.pf-legend{{display:flex;gap:16px;font-size:11px;color:#5a7a9a;margin-bottom:8px;flex-wrap:wrap}}
.pf-legend span{{display:inline-flex;align-items:center}}
.pf-legend span::before{{content:"";width:14px;height:0;border-top:2.5px solid;margin-right:5px}}
.pf-lg-nav::before{{border-color:#0369a1}}
.pf-lg-spy::before{{border-color:#94a3b8}}
.pf-lg-base::before{{border-top-style:dashed!important;border-color:#cbd5e1}}
.pf-svg{{width:100%;height:280px;display:block;background:#fcfdff;border:1px solid #eef3f9;border-radius:8px}}
.pf-grid{{stroke:#eef3f9;stroke-width:1}}
.pf-base{{stroke:#cbd5e1;stroke-width:1;stroke-dasharray:4 3}}
.pf-nav{{fill:none;stroke:#0369a1;stroke-width:2.2;stroke-linejoin:round}}
.pf-spy{{fill:none;stroke:#94a3b8;stroke-width:1.8;stroke-linejoin:round}}
.pf-ytick{{fill:#94a3b8;font-size:9.5px;text-anchor:end}}
.pf-xtick{{fill:#94a3b8;font-size:9.5px}}
.pf-stats{{display:flex;gap:14px;flex-wrap:wrap;margin:13px 0 4px}}
.pf-stat{{background:#f8fbff;border:1px solid #e6eef8;border-radius:8px;padding:9px 14px;min-width:150px}}
.pf-stat span{{display:block;font-size:10px;color:#8aa5c0}}
.pf-stat strong{{font-size:16px;color:#0f2a45;display:block;margin:1px 0;font-variant-numeric:tabular-nums}}
.pf-stat em{{font-style:normal;font-size:11px;color:#5a7a9a;font-variant-numeric:tabular-nums}}
.pf-pos{{margin-top:12px}}
.pf-note{{font-size:10.5px;color:#8aa5c0;margin-top:10px;line-height:1.6}}
details{{margin-top:12px;font-size:12px}}
summary{{cursor:pointer;color:#5a7a9a;font-weight:600}}
.a2-list{{padding:10px 4px;color:#5a7a9a;line-height:1.9;font-size:11.5px}}
.caveat{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:14px 18px;font-size:12px;color:#854d0e;line-height:1.7}}
.caveat strong{{color:#78350f;display:block;margin-bottom:6px}}
.caveat ul{{margin-left:20px}}
.bt-meta{{font-size:11px;color:#b45309;margin-bottom:10px}}
.sop-table{{font-size:11px;color:#5a7a9a;line-height:1.8}}
h4{{font-size:12px;color:#0f2a45;margin:14px 0 6px}}
code{{background:#f1f5f9;padding:1px 5px;border-radius:4px;font-size:11px}}
footer{{text-align:center;font-size:10.5px;color:#8aa5c0;padding:24px}}
</style>
</head>
<body>
{NAV_BLOCK}

<div class="hero"><div class="hero-inner">
<div class="hero-h1">Pure MA SOP 漏斗 — 起漲點雷達 × 自動記分板</div>
<div class="hero-sub">個股部 Pure MA SOP v2.1 機器版（總守則 v2.0）。五條件閘門（FY1→FY3 CAGR&gt;15 · ROIC&gt;15 · FCFm&gt;10 · PEG&lt;2 · 護城河≥B 且趨勢非↓）→ 態①健康多頭 → <strong>A1 起漲型</strong>（突破站立 ≥26 週的 ATH）/ <strong>B 第二班車</strong>（A1 後 26 週內首次回踩站回 60MA）。所有動作 T+1 收盤執行；進場後五狀態機自動模擬、出場自動記分。</div>
<div class="hero-stats">
<div class="hero-stat"><strong>{d["as_of"]}</strong>as of</div>
<div class="hero-stat"><strong>{d["universe_total"]}</strong>universe</div>
<div class="hero-stat"><strong>{d["quality_pass"]}</strong>五條件過閘</div>
<div class="hero-stat"><strong>{d["state1_count"]}</strong>態①健康多頭</div>
<div class="hero-stat"><strong>{len(d["open_trades"])}</strong>模擬持倉</div>
<div class="hero-stat"><strong>{len(d["closed_trades"])}</strong>已平倉</div>
{'<div class="hero-stat"><strong>⚠</strong>SPY 基準滯後</div>' if d.get("spy_benchmark_stale") else ''}
<div class="hero-stat"><strong>{_updated_taipei(d["run_timestamp"])}</strong>更新時間（台北）</div>
</div></div></div>

<div class="section"><div class="card">
<h2>§1 今日板機 🔫</h2>
<div class="desc">今天收盤觸發的進場訊號（執行 = 次一交易日收盤）。部位建議 = min(10%, 1.5% ÷ 停損距離)，分母 = 個股部淨值。</div>
<table><thead><tr><th class="left">ticker</th><th>型態</th><th>基期/錨</th><th>訊號收盤</th><th>停損距離</th><th>建議部位</th><th>旗標</th><th>報告</th></tr></thead>
<tbody>{_signal_rows(d["today_signals"])}</tbody></table>
{_veto_rows(d["today_vetoed"])}
{_veto_distribution_block(d.get("veto_distribution"))}
</div></div>

<div class="section"><div class="card">
<h2>§2 待命區</h2>
<div class="desc">未扣板機的候選。A1 起漲待命 = 距 ATH ≤5% 且基期 ≥26 週；B 武裝 = A1 錨後 26 週內回踩中；C 冷卻武裝 = 純態②否決後等「完成週收盤跌回 +2σ 帶內且守住 52週線」（2026-07-04 gate change，PREREG 觀察期）；築基中 = 距 ATH 5–25% 且 ATH 已站 ≥20 週（下一批 A1 孵化池）。</div>
<div class="grid3">
<div><h3>A1 起漲待命（{len(d["standby_a1"])}）</h3>{_standby_table(d["standby_a1"], a1_cols, "無起漲待命標的 — 等下一個長基期突破")}</div>
<div><h3>B 武裝中（{len([r for r in d["standby_b"] if not r["exceeded"]])}）</h3>{b_html}</div>
<div><h3>C 冷卻武裝中（{len(d.get("standby_c") or [])}）</h3>{_standby_table(d.get("standby_c") or [], c_cols, "無冷卻武裝中標的")}</div>
<div><h3>築基中（{len(d["base_building"])}）</h3>{_standby_table(d["base_building"], bb_cols, "無築基中標的")}</div>
</div>
{a2_block}{insuf}
</div></div>

<div class="section"><div class="card">
<h2>§3 模擬持倉</h2>
<div class="desc">帳本中 open 的訊號，每日按五狀態機演進（態③觸3σ減1/3 · 態④破60MA×0.97/連3日減至核心50%+站回回補 · 態⑤週收盤破52週線全出）。</div>
<table><thead><tr><th class="left">ticker</th><th>型態</th><th>進場日</th><th>進場價</th><th>目前態</th><th>部位</th><th>浮動報酬</th><th>α</th><th class="left">出場腿</th></tr></thead>
<tbody>{_open_rows(d["open_trades"])}</tbody></table>
</div></div>

{_performance_block(d.get("performance"))}

<div class="section"><div class="card">
<h2>§4 記分板</h2>
<div class="desc">漏斗累積成績（半年後裁決依據）。統計只算已平倉 trades；closed &lt; 20 顯示「樣本未熟」不給結論。A1 vs A2 對照驗證「起漲優於續勢」假設本身。</div>
<div class="prereg">🔒 <strong>預登記裁決（跑前鎖定）</strong>{_e(d["prereg"]["a2_adjudication"])}</div>
<div class="grid3">{_score_cards(d["scoreboard"])}</div>
<h4>已平倉明細</h4>
<table><thead><tr><th class="left">ticker</th><th>型態</th><th>進場</th><th>出場</th><th>原因</th><th>報酬</th><th>R</th><th>α vs SPY</th><th>持有</th></tr></thead>
<tbody>{_closed_rows(d["closed_trades"])}</tbody></table>
<h4>5 年歷史回測參考（含態④減碼幅度 A/B，供 2026-09 季檢）　·　<a href="/dd-screener/sop-funnel-backtest.html">🧪 完整 2022 回測：斷路器死鎖發現 + NAV 曲線 + 規則實驗室 →</a></h4>
{_backtest_block(d.get("backtest"))}
</div></div>

<div class="section"><div class="card">
<h2>§5 規則對照與 Caveats</h2>
<div class="sop-table">
<strong>S-4 五問機器化程度</strong>：Q1 五條件 ✓自動（四質量 + 護城河≥B 非↓，dd-screener 資料庫）· Q2 進場型態 ✓自動（A1/A2/B）· Q3 態①健康多頭 ✓自動（凍結週線）· Q4 部位公式 ✓建議值 · Q5 財報靜默期＋斷路器＋總曝險 ✗<strong>人工自查</strong>
</div>
<div class="caveat" style="margin-top:12px">
<strong>v1 已知簡化（誠實清單）</strong>
<ul>
<li>財報靜默期：<strong>2026-06-11 用戶裁決拿掉禁令</strong>（2022 回測：被擋 14 筆放行後全獲利，惟證據含凍結名單偏誤）。forward 訊號改為「標記不擋」——財報窗內進場標 ⚠ 供季檢以無偏數據複查。S-7 gap 破線當日態⑤未模擬</li>
<li>態⑤ 執行 = 週收盤確認後的次一交易日<strong>收盤</strong>（資料層只有日收盤、無開盤價）— 真實操作建議週一開盤即出，模擬與實盤在生死線上差約一個交易日</li>
<li>組合層規則（斷路器 10%、總曝險 100%、單檔 10% 互斥）未模擬 — 本頁為單筆訊號追蹤，非 NAV 回測</li>
<li>態①金字塔加碼未模擬 — 每 ticker 同時最多一筆 trade</li>
<li>價格為含息調整（auto_adjust，與全站一致）— TW 高息股的 ATH/52週線訊號可能比看盤圖表早觸發 ~1-2%/年</li>
<li>B 型「限突破後首次回測」實作為「每 A1 錨最多一次站回」；錨齡上限 26 週</li>
<li>回填段（{_e(d["params"].get("base_age_min_weeks"))}週基期規則上線前的歷史事件）五條件用當前值評估</li>
<li>報酬分母 = 累計投入資金（含態④回補）；R = 報酬 ÷ 進場時停損距離</li>
<li>護城河評級來自 DD 報告（人工輸入會過期）：dd 評級逾 {_e(183)} 天未更新 → 訊號照發但標「護城河待複檢」</li>
</ul>
</div>
<div class="sop-table" style="margin-top:12px">
<strong>季檢待議（2026-09，預登記）</strong>：{"　·　".join(_e(x) for x in d["prereg"]["quarterly_review_items"])}
</div>
</div></div>

<div class="section"><div class="card">
<h2>§6 漏斗母體 — 五條件全過清單（{len(d["population"])} 檔）</h2>
<div class="desc">這是任何時點的「射程內」標的：四質量條件（CAGR&gt;15 · ROIC&gt;15 · FCFm&gt;10 · PEG&lt;2）＋護城河（≥B 且趨勢非↓）全過。技術面（態①/起漲板機）只決定「何時」對這份名單動手，不影響入列。按護城河等級排序。</div>
{_population_block(d["population"], d.get("moat_excluded", []))}
</div></div>

<footer>InvestMQuest · Pure MA SOP 漏斗 v1.0 · 更新 {_updated_taipei(d["run_timestamp"])}（台北）· 模擬非投資建議</footer>
</body></html>
""")
