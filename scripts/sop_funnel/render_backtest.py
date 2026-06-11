#!/usr/bin/env python3
"""SOP 漏斗 2022 回測頁渲染 — 方式二定位：技術執行層回測 + 規則 A/B 實驗室。

定位（用戶 2026-06-11 拍板）：凍結名單下絕對報酬不可信 → 降為灰色參考；
主角 = 同名單內部對照的四大相對發現（斷路器死鎖 / 態④ A/B / 靜默期 / 型態行為）。
選股能力的無偏證據 = forward 帳本（主頁）；Phase 2 point-in-time 代理閘門另議。

用法：python3 scripts/sop_funnel/render_backtest.py
讀 docs/dd-screener/sop-funnel/backtest-full.json → 寫 docs/dd-screener/sop-funnel-backtest.html
"""
from __future__ import annotations

import html
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IN_JSON = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel" / "backtest-full.json"
OUT_HTML = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel-backtest.html"


def _e(v):
    return html.escape(str(v)) if v is not None else "—"


def _pct(v, signed=True):
    if v is None:
        return "—"
    return f"{v:+.1f}%" if signed else f"{v:.1f}%"


def _cls(v):
    if v is None:
        return ""
    return "pos" if v > 0 else ("neg" if v < 0 else "")


def svg_chart(d: dict, w=1080, h=340) -> str:
    """NAV(charter) / NAV(無斷路器) / SPY / QQQ 四線 + 斷路器觸發標記。"""
    t2, nb = d["tier2"], d["tier2_no_breaker"]
    dates = [x[0] for x in t2["nav_series"]]
    series = {
        "charter": ([x[1] for x in t2["nav_series"]], "#dc2626"),
        "no_breaker": ([x[1] for x in nb["nav_series"]], "#059669"),
        "SPY": (t2.get("spy_norm") or [], "#64748b"),
        "QQQ": (t2.get("qqq_norm") or [], "#94a3b8"),
    }
    all_vals = [v for vals, _ in series.values() for v in vals if v is not None]
    lo, hi = min(all_vals) * 0.97, max(all_vals) * 1.03
    pad_l, pad_b = 46, 22
    iw, ih = w - pad_l - 8, h - pad_b - 8

    def xy(i, v):
        x = pad_l + i / (len(dates) - 1) * iw
        y = 8 + (1 - (v - lo) / (hi - lo)) * ih
        return f"{x:.1f},{y:.1f}"

    lines = []
    for name, (vals, color) in series.items():
        pts = " ".join(xy(i, v) for i, v in enumerate(vals) if v is not None)
        if pts:
            width = 2.2 if name in ("charter", "no_breaker") else 1.3
            dash = ' stroke-dasharray="4,3"' if name == "QQQ" else ""
            lines.append(f'<polyline points="{pts}" fill="none" stroke="{color}" '
                         f'stroke-width="{width}"{dash}/>')
    # 斷路器觸發豎線
    for ep in t2.get("breaker_episodes", []):
        if ep["trigger"] in dates:
            i = dates.index(ep["trigger"])
            x = pad_l + i / (len(dates) - 1) * iw
            lines.append(f'<line x1="{x:.0f}" y1="8" x2="{x:.0f}" y2="{8 + ih}" '
                         f'stroke="#dc2626" stroke-width="1" stroke-dasharray="2,3" opacity=".6"/>'
                         f'<text x="{x + 4:.0f}" y="22" font-size="10" fill="#dc2626">斷路器 {ep["trigger"]}'
                         + ("（未解除→死鎖）" if not ep.get("release") else "") + "</text>")
    # 年度刻度 + 水平格線
    grid = []
    seen = set()
    for i, dt in enumerate(dates):
        y4 = dt[:4]
        if y4 not in seen:
            seen.add(y4)
            x = pad_l + i / (len(dates) - 1) * iw
            grid.append(f'<line x1="{x:.0f}" y1="8" x2="{x:.0f}" y2="{8 + ih}" stroke="#eef3fa"/>'
                        f'<text x="{x + 3:.0f}" y="{h - 6}" font-size="10" fill="#8aa5c0">{y4}</text>')
    for lv in (100, 150, 200):
        if lo < lv < hi:
            y = 8 + (1 - (lv - lo) / (hi - lo)) * ih
            grid.append(f'<line x1="{pad_l}" y1="{y:.0f}" x2="{w - 8}" y2="{y:.0f}" stroke="#eef3fa"/>'
                        f'<text x="4" y="{y + 3:.0f}" font-size="10" fill="#8aa5c0">{lv}</text>')
    legend = (f'<g font-size="11"><rect x="{pad_l + 8}" y="14" width="270" height="20" fill="#fff" opacity=".85"/>'
              f'<text x="{pad_l + 14}" y="28"><tspan fill="#dc2626">━ charter</tspan>'
              f'<tspan fill="#059669" dx="10">━ 無斷路器</tspan>'
              f'<tspan fill="#64748b" dx="10">━ SPY</tspan>'
              f'<tspan fill="#94a3b8" dx="10">┄ QQQ</tspan></text></g>')
    return (f'<svg viewBox="0 0 {w} {h}" style="width:100%;background:#fff;'
            f'border:1px solid #dce8f5;border-radius:8px">{"".join(grid)}{"".join(lines)}{legend}</svg>')


def stat_row(label, m, muted=False):
    cls = ' class="muted-row"' if muted else ""
    return (f'<tr{cls}><td class="left">{label}</td><td>{m["n_signals"]}</td>'
            f'<td>{m["n_entered"]}</td><td>{m.get("n_silent_blocked", "—")}</td>'
            f'<td>{_pct(m["win_rate"], signed=False)}</td>'
            f'<td class="{_cls(m["median_ret_pct"])}">{_pct(m["median_ret_pct"])}</td>'
            f'<td class="{_cls(m["mean_ret_pct"])}">{_pct(m["mean_ret_pct"])}</td>'
            f'<td class="{_cls(m["mean_alpha_pct"])}">{_pct(m["mean_alpha_pct"])}</td>'
            f'<td>{_e(m["mean_r"])}</td><td>{_e(m["median_holding_days"])}d</td></tr>')


def main() -> int:
    d = json.loads(IN_JSON.read_text(encoding="utf-8"))
    t1, t2, nb = d["tier1"], d["tier2"], d["tier2_no_breaker"]
    g, st, ug = t1["gated_charter"], t1["gated_staged"], t1["ungated_all"]
    bt = t1["by_type"]
    spy_final = next((v for v in reversed(t2.get("spy_norm") or []) if v), None)
    qqq_final = next((v for v in reversed(t2.get("qqq_norm") or []) if v), None)
    silent_pct = round(g["n_silent_blocked"] / g["n_signals"] * 100) if g["n_signals"] else 0

    yearly_rows = ""
    for y, m in t1["yearly"].items():
        yearly_rows += (f'<tr><td class="left">{y}</td><td>{m["n_entered"]}</td>'
                        f'<td>{m["n_silent_blocked"]}</td>'
                        f'<td>{_pct(m["win_rate"], signed=False)}</td>'
                        f'<td class="{_cls(m["median_ret_pct"])}">{_pct(m["median_ret_pct"])}</td>'
                        f'<td class="{_cls(m["mean_ret_pct"])}">{_pct(m["mean_ret_pct"])}</td></tr>')

    trade_rows = ""
    for t in d["trades"]:
        if t.get("earnings_check") == "silent":
            trade_rows += (f'<tr class="muted-row"><td class="left">{_e(t["ticker"])}</td>'
                           f'<td>{_e(t["type"])}</td><td>{_e(t["signal_date"])}</td>'
                           f'<td colspan="6" class="left">🛡 財報靜默期擋下（未進場）</td></tr>')
            continue
        nb_tag = f'<span class="warn-tag">{_e(t.get("nav_blocked"))}</span>' if t.get("nav_blocked") else ""
        trade_rows += (f'<tr><td class="left"><strong>{_e(t["ticker"])}</strong>{nb_tag}</td>'
                       f'<td>{_e(t["type"])}</td><td>{_e(t["signal_date"])}</td>'
                       f'<td>{_e(t.get("exit_date"))}</td><td>{_e(t.get("exit_reason") or ("持有中" if t.get("status") == "open" else "—"))}</td>'
                       f'<td class="{_cls(t.get("ret_pct"))}">{_pct(t.get("ret_pct"))}</td>'
                       f'<td>{_e(t.get("r"))}</td>'
                       f'<td class="{_cls(t.get("alpha_pct"))}">{_pct(t.get("alpha_pct"))}</td>'
                       f'<td>{_e(t.get("holding_days"))}d</td></tr>')

    caveat_lis = "".join(f"<li>{_e(c)}</li>" for c in d["caveats"])

    page = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SOP 漏斗 2022 回測 — 技術執行層 × 規則實驗室 | InvestMQuest</title>
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
.hero-inner{{max-width:min(1320px,96vw);margin:0 auto}}
.hero-h1{{font-size:22px;font-weight:600;color:#0f2a45;margin-bottom:6px}}
.hero-sub{{font-size:12px;color:#5a7a9a;line-height:1.6;max-width:980px}}
.section{{max-width:min(1320px,96vw);margin:0 auto;padding:20px 32px 4px}}
.card{{background:#fff;border:1px solid #dce8f5;border-radius:10px;padding:16px 18px;margin-bottom:20px}}
.card h2{{font-size:16px;font-weight:700;margin-bottom:4px;color:#0f2a45}}
.card .desc{{font-size:12px;color:#5a7a9a;margin-bottom:12px;line-height:1.6}}
table{{width:100%;border-collapse:collapse;font-size:11.5px}}
th{{background:#f0f6ff;color:#5a7a9a;font-weight:700;padding:7px 8px;text-align:right;border-bottom:2px solid #dce8f5;font-size:10px;white-space:nowrap}}
th.left{{text-align:left}}
td{{padding:7px 8px;text-align:right;border-bottom:1px solid #f0f5fb;font-variant-numeric:tabular-nums}}
td.left{{text-align:left;font-weight:500}}
.pos{{color:#059669;font-weight:600}}.neg{{color:#dc2626;font-weight:600}}
.muted-row td{{color:#94a3b8}}
.warn-tag{{display:inline-block;margin-left:6px;padding:1px 6px;border-radius:4px;font-size:9.5px;font-weight:700;background:#fef3c7;color:#92400e}}
.honesty{{background:#fef2f2;border:2px solid #fca5a5;border-radius:10px;padding:16px 20px;font-size:13px;color:#7f1d1d;line-height:1.8;margin-bottom:20px}}
.honesty strong{{display:block;font-size:14px;margin-bottom:6px}}
.honesty .ok-list{{color:#14532d;background:#f0fdf4;border-radius:6px;padding:8px 14px;margin-top:8px;font-size:12px}}
.finding{{border-left:4px solid #dc2626;background:#fff;border-radius:0 10px 10px 0;border-top:1px solid #dce8f5;border-right:1px solid #dce8f5;border-bottom:1px solid #dce8f5;padding:14px 18px;margin-bottom:14px}}
.finding h3{{font-size:14px;color:#0f2a45;margin-bottom:6px}}
.finding p{{font-size:12px;color:#475569;line-height:1.7}}
.finding .nums{{font-size:13px;font-weight:700;margin:6px 0;font-variant-numeric:tabular-nums}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:14px}}
.kpi{{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0}}
.kpi div{{background:#f0f5fb;border:1px solid #dce8f5;border-radius:6px;padding:7px 12px;font-size:11px;color:#5a7a9a}}
.kpi strong{{display:block;font-size:14px;color:#1e3a5f}}
.kpi .ghost strong{{color:#94a3b8}}
.caveat{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:14px 18px;font-size:12px;color:#854d0e;line-height:1.7}}
.caveat ul{{margin-left:20px}}
h4{{font-size:12px;color:#0f2a45;margin:14px 0 6px}}
footer{{text-align:center;font-size:10.5px;color:#8aa5c0;padding:24px}}
.ghost-note{{font-size:10.5px;color:#94a3b8}}
</style>
</head>
<body>
<header class="imq-nav-root"><div class="imq-nav-inner">
<a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
<nav class="imq-menu"><a href="/">首頁</a><a href="/dd-screener/">DD Screener</a>
<a href="/dd-screener/sop-funnel.html">🎯 SOP 漏斗</a>
<a href="/dd-screener/sop-funnel-backtest.html" class="active">🧪 2022 回測</a></nav>
</div></header>

<div class="hero"><div class="hero-inner">
<div class="hero-h1">SOP 漏斗 2022 回測 — 技術執行層 × 規則實驗室</div>
<div class="hero-sub">窗口 {d["window_start"]} → {d["window_end"]} · {d["price_basis"]} · 母體 = <strong>凍結 2026-06-11 的 {d["n_gated"]} 檔五條件過閘名單</strong>。本頁不是選股能力證明（見下方誠實邊界）——它是同一份名單上的<strong>規則對照實驗</strong>：斷路器條文、態④減碼幅度、財報靜默期、訊號型態，這些「兩邊共享同樣偏誤」的相對結論才是主角。</div>
</div></div>

<div class="section">
<div class="honesty">
<strong>⚠ 誠實邊界 — 先讀這個再看數字</strong>
五條件閘門用的是<u>今天</u>的分析師預估與護城河評級（歷史版本不存在），universe 是<u>今天</u>策展的 DD 名單——2022 年的漏斗會選出不一樣的股票。因此：<u>所有絕對報酬數字（CAGR、終值、α）一律視為灰色參考</u>，它們繼承了「拿今天的贏家回去考古」的樂觀偏誤。
<div class="ok-list">✅ 仍然站得住的結論（同名單內部對照，偏誤兩邊抵銷）：① 斷路器死鎖 ② 態④減碼 A/B ③ 財報靜默期影響 ④ A1/A2/B 型態行為差 ⑤ 2022 熊市防禦行為。選股能力的無偏證據只有一種：<a href="/dd-screener/sop-funnel.html">主頁 forward 帳本</a>（今天選、明天驗）。Phase 2（point-in-time 代理閘門）另議。</div>
</div>
</div>

<div class="section"><div class="card">
<h2>§1 四大發現（規則實驗室 — 本頁主角）</h2>
<div class="finding">
<h3>發現① 斷路器死鎖 — charter 條文照字面執行會永久停機</h3>
<div class="nums">含斷路器終值 <span class="neg">{t2["final_nav"]:.0f}</span> vs 無斷路器 <span class="pos">{nb["final_nav"]:.0f}</span>（同訊號、同名單，唯一變數 = 斷路器條文）</div>
<p>2024-07 系統曝險 ~83% 遇上 7-8 月急跌，NAV 自高點 -10.1% 觸發斷路器（{t2["breaker_episodes"][0]["trigger"] if t2["breaker_episodes"] else "—"}）。隨後五狀態機把部位陸續停損 → 滿手現金 → NAV 凍在回撤區 → <strong>永遠回不到「-5% 以內」的解除線 → 之後 {t2["blocked_entries"]} 筆進場（含 2025 全部贏家）被擋到期末</strong>。Charter 的解除條件隱含「部位會反彈收復回撤」，但斷路器觸發時部位往往已被狀態機砍光——條文與五狀態機的交互作用產生死鎖。<strong>季檢建議</strong>：解除條件加一條「現金比 &gt;90% 且經過 N 日 → 自動解除」或改時間解除。</p>
</div>
<div class="finding" style="border-left-color:#2563eb">
<h3>發現② 態④減碼幅度 A/B — 階梯式小勝，與舊研究方向一致</h3>
<div class="nums">charter 一次 50%：勝率 {_pct(g["win_rate"], signed=False)} · 中位 {_pct(g["median_ret_pct"])} · α {_pct(g["mean_alpha_pct"])} · R {g["mean_r"]}　vs　階梯 25%+25%：勝率 {_pct(st["win_rate"], signed=False)} · 中位 {_pct(st["median_ret_pct"])} · α {_pct(st["mean_alpha_pct"])} · R {st["mean_r"]}</div>
<p>本窗口階梯式各項略優但差距小（α +{round((st["mean_alpha_pct"] or 0) - (g["mean_alpha_pct"] or 0), 1)}pp）。與態④ trim-variants 舊研究（流程指標）合併讀：不構成改規則的強證據，供 2026-09 季檢。</p>
</div>
<div class="finding" style="border-left-color:#d97706">
<h3>發現③ 財報靜默期 — 擋下 {g["n_silent_blocked"]}/{g["n_signals"]} 筆訊號（{silent_pct}%）</h3>
<p>四年間近四分之一的進場訊號落在財報前 7 曆日內。真實 SOP 會躲掉這些，無守衛的模擬會吃下它們——這就是 forward 帳本必須有靜默期守衛的量化理由（已上線）。被擋訊號在明細表以灰色顯示。</p>
</div>
<div class="finding" style="border-left-color:#059669">
<h3>發現④ 型態行為 — A1 起漲樣本極稀但彈道不同</h3>
<div class="nums">A1：{bt["A1"]["n_entered"]} 筆 · 平均 {_pct(bt["A1"]["mean_ret_pct"])} · α {_pct(bt["A1"]["mean_alpha_pct"])}　|　A2：{bt["A2"]["n_entered"]} 筆 · 平均 {_pct(bt["A2"]["mean_ret_pct"])} · α {_pct(bt["A2"]["mean_alpha_pct"])}　|　B：{bt["B"]["n_entered"]} 筆 · 平均 {_pct(bt["B"]["mean_ret_pct"])} · α {_pct(bt["B"]["mean_alpha_pct"])}</div>
<p>4.4 年只出現 {bt["A1"]["n_signals"]} 筆乾淨 A1（長基期突破本來就稀有），均值被大贏家拉高、樣本遠不足下結論——這正是 forward 帳本 A1 vs A2 預登記裁決存在的理由。B 第二班車 {bt["B"]["n_entered"]} 筆，行為介於兩者之間。</p>
</div>
</div></div>

<div class="section"><div class="card">
<h2>§2 NAV 曲線（灰色參考 — 凍結名單偏誤未除）</h2>
<div class="desc">起始 100 · charter S-2 部位規則（min(10%, 1.5%÷停損)×NAV · 總曝險≤100% · 純現股）· 同日優先序 A1&gt;B&gt;A2。紅線 = charter 含斷路器（死鎖後曝險歸零）；綠線 = 無斷路器對照。</div>
{svg_chart(d)}
<div class="kpi">
<div class="ghost"><strong>{t2["final_nav"]:.0f}</strong>charter 終值</div>
<div class="ghost"><strong>{nb["final_nav"]:.0f}</strong>無斷路器終值</div>
<div class="ghost"><strong>{_e(spy_final and round(spy_final))}</strong>SPY 同期</div>
<div class="ghost"><strong>{_e(qqq_final and round(qqq_final))}</strong>QQQ 同期</div>
<div><strong>{_pct(t2["mdd_pct"])} / {_pct(nb["mdd_pct"])}</strong>MDD charter / 無斷路器</div>
<div><strong>{_e(t2["sharpe"])} / {_e(nb["sharpe"])}</strong>Sharpe</div>
<div><strong>{nb["avg_exposure_pct"]:.0f}%</strong>平均曝險（無斷路器）</div>
<div><strong>{nb["pct_days_flat"]:.0f}%</strong>空手日比</div>
</div>
<div class="ghost-note">絕對數字皆含凍結名單偏誤；本圖的合法用途是紅綠兩線的「形狀差」（死鎖成本）與曝險行為，不是與 SPY 比絕對高低。</div>
</div></div>

<div class="section"><div class="card">
<h2>§3 年度拆分（gated · charter 態④）</h2>
<div class="desc">2022 全熊市：進場稀少且全敗但被停損框住 — 防禦行為符合設計；訊號集中在 2023 復甦與 2025。</div>
<table><thead><tr><th class="left">年</th><th>進場</th><th>靜默擋</th><th>勝率</th><th>中位報酬</th><th>平均報酬</th></tr></thead>
<tbody>{yearly_rows}</tbody></table>
</div></div>

<div class="section"><div class="card">
<h2>§4 閘門對照（殘留偏誤警示）</h2>
<div class="desc">⚠ 此對照<strong>不是</strong>乾淨實驗：「今天過閘」與「過去四年表現好」相關，gated 組天然占便宜。僅供方向參考，權重低於 §1 四大發現。ungated 組未套靜默期守衛。</div>
<table><thead><tr><th class="left">組</th><th>訊號</th><th>進場</th><th>靜默擋</th><th>勝率</th><th>中位報酬</th><th>平均報酬</th><th>α vs SPY</th><th>平均R</th><th>中位持有</th></tr></thead>
<tbody>
{stat_row(f'五條件過閘 {d["n_gated"]} 檔（charter）', g)}
{stat_row(f'無閘門全 universe {d["n_universe"]} 檔', ug, muted=True)}
</tbody></table>
</div></div>

<div class="section"><div class="card">
<h2>§5 Trade 明細（gated · charter · {g["n_entered"]} 筆進場 + {g["n_silent_blocked"]} 筆靜默擋）</h2>
<table><thead><tr><th class="left">ticker</th><th>型態</th><th>訊號日</th><th>出場日</th><th>原因</th><th>報酬</th><th>R</th><th>α</th><th>持有</th></tr></thead>
<tbody>{trade_rows}</tbody></table>
</div></div>

<div class="section"><div class="card">
<h2>§6 方法論與已知偏誤</h2>
<div class="caveat"><ul>{caveat_lis}
<li>全動作 T+1 收盤執行；週線指標用已完成週凍結值（無部分週 look-ahead）</li>
<li>NAV 模擬：現金不計息、零交易成本；回補腿受斷路器與現金約束、賣腿永遠執行</li>
<li>Phase 2（point-in-time 代理閘門：trailing 指標 + 季度資格窗 + 財報滯後）需 Koyfin 歷史財報匯出，另議</li>
</ul></div>
</div></div>

<footer>InvestMQuest · SOP 漏斗 2022 回測 v1.0 · 生成 {d["run_timestamp"]} · 模擬非投資建議</footer>
</body></html>
"""
    OUT_HTML.write_text(page, encoding="utf-8")
    print(f"rendered → {OUT_HTML}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
