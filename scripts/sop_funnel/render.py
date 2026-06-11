#!/usr/bin/env python3
"""SOP 漏斗頁 server-render（沿用 dd-screener 家族頁面 CSS 慣例）。"""
from __future__ import annotations

import html


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
            f'<td>{_dd_link(e)}</td></tr>')
    return "".join(out)


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
            f'<td>{_e(s["current_state"])}</td><td>{s["current_fraction"] * 100:.0f}%</td>'
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
    label = {"A1": "A1 起漲型（主訊號）", "A2": "A2 續勢型（對照）", "B": "B 第二班車"}
    cards = []
    for k in ("A1", "A2", "B"):
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

    return f"""<!DOCTYPE html>
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
.imq-nav-root{{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:.7rem 20px;font-size:13px;position:sticky;top:0;z-index:1000}}
.imq-nav-inner{{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}}
.imq-logo{{font-weight:700;color:#fff;text-decoration:none;font-size:15px}}
.imq-logo span{{color:#3b82f6}}
.imq-menu{{display:flex;gap:.5rem}}
.imq-menu a{{color:rgba(255,255,255,.7);font-size:.8rem;padding:.4rem .7rem;border-radius:6px;text-decoration:none}}
.imq-menu a:hover{{color:#fff;background:rgba(255,255,255,.08)}}
.imq-menu a.active{{color:#fff;background:rgba(59,130,246,.22);font-weight:600}}
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
.grid3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}}
.grid3 h3,.score-card h3{{font-size:13px;font-weight:700;color:#0f2a45;margin-bottom:8px}}
.score-card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:14px 16px}}
.score-card.muted .score-grid strong{{color:#94a3b8}}
.score-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font-size:11px}}
.score-grid span{{color:#8aa5c0;display:block;font-size:10px}}
.score-grid strong{{font-size:14px;color:#0f2a45}}
.thin-flag{{font-size:10px;background:#f1f5f9;color:#64748b;padding:2px 8px;border-radius:4px;font-weight:600}}
.exceeded{{font-size:11px;color:#8aa5c0;margin-top:10px;line-height:1.7}}
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
<header class="imq-nav-root"><div class="imq-nav-inner">
<a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
<nav class="imq-menu"><a href="/">首頁</a><a href="/research/">個股 DD</a>
<a href="/dd-screener/">DD Screener</a><a href="/dd-screener/sop-funnel.html" class="active">🎯 SOP 漏斗</a></nav>
</div></header>

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
</div></div></div>

<div class="section"><div class="card">
<h2>§1 今日板機 🔫</h2>
<div class="desc">今天收盤觸發的進場訊號（執行 = 次一交易日收盤）。部位建議 = min(10%, 1.5% ÷ 停損距離)，分母 = 個股部淨值。</div>
<table><thead><tr><th class="left">ticker</th><th>型態</th><th>基期/錨</th><th>訊號收盤</th><th>停損距離</th><th>建議部位</th><th>報告</th></tr></thead>
<tbody>{_signal_rows(d["today_signals"])}</tbody></table>
{_veto_rows(d["today_vetoed"])}
</div></div>

<div class="section"><div class="card">
<h2>§2 待命區</h2>
<div class="desc">未扣板機的候選。A1 起漲待命 = 距 ATH ≤5% 且基期 ≥26 週；B 武裝 = A1 錨後 26 週內回踩中；築基中 = 距 ATH 5–25% 且 ATH 已站 ≥20 週（下一批 A1 孵化池）。</div>
<div class="grid3">
<div><h3>A1 起漲待命（{len(d["standby_a1"])}）</h3>{_standby_table(d["standby_a1"], a1_cols, "無起漲待命標的 — 等下一個長基期突破")}</div>
<div><h3>B 武裝中（{len([r for r in d["standby_b"] if not r["exceeded"]])}）</h3>{b_html}</div>
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

<div class="section"><div class="card">
<h2>§4 記分板</h2>
<div class="desc">漏斗累積成績（半年後裁決依據）。統計只算已平倉 trades；closed &lt; 20 顯示「樣本未熟」不給結論。A1 vs A2 對照驗證「起漲優於續勢」假設本身。</div>
<div class="grid3">{_score_cards(d["scoreboard"])}</div>
<h4>已平倉明細</h4>
<table><thead><tr><th class="left">ticker</th><th>型態</th><th>進場</th><th>出場</th><th>原因</th><th>報酬</th><th>R</th><th>α vs SPY</th><th>持有</th></tr></thead>
<tbody>{_closed_rows(d["closed_trades"])}</tbody></table>
<h4>5 年歷史回測參考（含態④減碼幅度 A/B，供 2026-09 季檢）</h4>
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
<li>財報靜默期（S-7 前 5 日禁建倉、gap 破線當日態⑤）未模擬 — 模擬以週收盤判態⑤，財報崩跌的出場時點與真實 SOP 有差</li>
<li>組合層規則（斷路器 10%、總曝險 100%、單檔 10% 互斥）未模擬 — 本頁為單筆訊號追蹤，非 NAV 回測</li>
<li>態①金字塔加碼未模擬 — 每 ticker 同時最多一筆 trade</li>
<li>價格為含息調整（auto_adjust，與全站一致）— TW 高息股的 ATH/52週線訊號可能比看盤圖表早觸發 ~1-2%/年</li>
<li>B 型「限突破後首次回測」實作為「每 A1 錨最多一次站回」；錨齡上限 26 週</li>
<li>回填段（{_e(d["params"].get("base_age_min_weeks"))}週基期規則上線前的歷史事件）五條件用當前值評估</li>
<li>報酬分母 = 累計投入資金（含態④回補）；R = 報酬 ÷ 進場時停損距離</li>
</ul>
</div>
</div></div>

<footer>InvestMQuest · Pure MA SOP 漏斗 v1.0 · 生成 {d["run_timestamp"]} · 模擬非投資建議</footer>
</body></html>
"""
