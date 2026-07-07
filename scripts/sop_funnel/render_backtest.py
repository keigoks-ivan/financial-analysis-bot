#!/usr/bin/env python3
"""SOP 漏斗 2022 回測頁渲染 — 技術執行層 × 規則實驗室。

呈現層級（2026-06-11 用戶裁決後）：
- 現行配置 = gated × 無斷路器 × 財報窗標記不擋 → 主線
- charter 原版（含斷路器+靜默期禁令）→ 對照線（裁決前的樣子）
- 226 檔純價格（無閘門）→ 對照線
- 凍結名單偏誤 → 絕對數字仍降灰色參考；裁決依據與其證據等級全頁明標

用法：python3 scripts/sop_funnel/render_backtest.py
讀 docs/dd-screener/sop-funnel/backtest-full.json → 寫 docs/dd-screener/sop-funnel-backtest.html
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
IN_JSON = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel" / "backtest-full.json"
OUT_HTML = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel-backtest.html"

# Canonical site header (single source: scripts/site_nav.py)
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from site_nav import DD_SCREENER_SUBNAV, build_subnav, full_nav_block  # noqa: E402

# Canonical site header + dd-screener sub-nav for this page
NAV_BLOCK = full_nav_block(
    "pick", "dds",
    build_subnav(DD_SCREENER_SUBNAV, "/dd-screener/sop-funnel-backtest.html"),
)


# ── 顯示層圈數字替換（①-⑤ 小字級下不可讀；資料層內部表示不動）──
_CIRCLED = {"①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5"}


def _plain_states(html_text: str) -> str:
    for k, v in _CIRCLED.items():
        html_text = html_text.replace(k, v)
    return html_text


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
    """主線 = 現行配置（無斷路器+無靜默期）；對照 = charter 原版 / 226 純價格 / SPY / QQQ。"""
    t2 = d["tier2"]
    dates = [x[0] for x in t2["nav_series"]]
    series = [
        ("現行配置", [x[1] for x in d["tier2_no_silent"]["nav_series"]], "#059669", 2.4, ""),
        ("charter原版", [x[1] for x in t2["nav_series"]], "#dc2626", 1.8, ""),
        ("226純價格", [x[1] for x in d["tier2_ungated"]["nav_series"]], "#7c3aed", 1.4, ' stroke-dasharray="6,3"'),
        ("SPY", t2.get("spy_norm") or [], "#64748b", 1.2, ""),
        ("QQQ", t2.get("qqq_norm") or [], "#94a3b8", 1.2, ' stroke-dasharray="4,3"'),
    ]
    all_vals = [v for _, vals, *_ in series for v in vals if v is not None]
    lo, hi = min(all_vals) * 0.97, max(all_vals) * 1.03
    pad_l, pad_b = 46, 22
    iw, ih = w - pad_l - 8, h - pad_b - 8

    def xy(i, v):
        x = pad_l + i / (len(dates) - 1) * iw
        y = 8 + (1 - (v - lo) / (hi - lo)) * ih
        return f"{x:.1f},{y:.1f}"

    lines = []
    for name, vals, color, width, dash in series:
        pts = " ".join(xy(i, v) for i, v in enumerate(vals) if v is not None)
        if pts:
            lines.append(f'<polyline points="{pts}" fill="none" stroke="{color}" '
                         f'stroke-width="{width}"{dash}/>')
    for ep in t2.get("breaker_episodes", []):
        if ep["trigger"] in dates:
            i = dates.index(ep["trigger"])
            x = pad_l + i / (len(dates) - 1) * iw
            lines.append(f'<line x1="{x:.0f}" y1="8" x2="{x:.0f}" y2="{8 + ih}" '
                         f'stroke="#dc2626" stroke-width="1" stroke-dasharray="2,3" opacity=".6"/>'
                         f'<text x="{x + 4:.0f}" y="22" font-size="10" fill="#dc2626">原版斷路器死鎖 {ep["trigger"]}↓</text>')
    grid, seen = [], set()
    for i, dt in enumerate(dates):
        y4 = dt[:4]
        if y4 not in seen:
            seen.add(y4)
            x = pad_l + i / (len(dates) - 1) * iw
            grid.append(f'<line x1="{x:.0f}" y1="8" x2="{x:.0f}" y2="{8 + ih}" stroke="#eef3fa"/>'
                        f'<text x="{x + 3:.0f}" y="{h - 6}" font-size="10" fill="#8aa5c0">{y4}</text>')
    for lv in (100, 150, 200, 250):
        if lo < lv < hi:
            y = 8 + (1 - (lv - lo) / (hi - lo)) * ih
            grid.append(f'<line x1="{pad_l}" y1="{y:.0f}" x2="{w - 8}" y2="{y:.0f}" stroke="#eef3fa"/>'
                        f'<text x="4" y="{y + 3:.0f}" font-size="10" fill="#8aa5c0">{lv}</text>')
    legend = (f'<g font-size="11"><rect x="{pad_l + 8}" y="14" width="430" height="20" fill="#fff" opacity=".88"/>'
              f'<text x="{pad_l + 14}" y="28"><tspan fill="#059669" font-weight="bold">━ 現行配置</tspan>'
              f'<tspan fill="#dc2626" dx="10">━ charter原版</tspan>'
              f'<tspan fill="#7c3aed" dx="10">┅ 226純價格</tspan>'
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
    t1, t2 = d["tier1"], d["tier2"]
    nb, ns, ung = d["tier2_no_breaker"], d["tier2_no_silent"], d["tier2_ungated"]
    g, st, ug_s, gns = (t1["gated_charter"], t1["gated_staged"],
                        t1["ungated_all"], t1["gated_no_silent"])
    bt = t1["by_type"]
    spy_final = next((v for v in reversed(t2.get("spy_norm") or []) if v), None)
    qqq_final = next((v for v in reversed(t2.get("qqq_norm") or []) if v), None)
    silent_pct = round(g["n_silent_blocked"] / g["n_signals"] * 100) if g["n_signals"] else 0

    cf_rows = "".join(
        f'<tr><td class="left">{_e(c["ticker"])}</td><td>{_e(c["signal_date"])}</td>'
        f'<td class="{_cls(c["ret_pct"])}">{_pct(c["ret_pct"])}</td>'
        f'<td>{_e(c["exit_reason"])}</td></tr>'
        for c in sorted(d.get("silent_counterfactual", []),
                        key=lambda x: -(x["ret_pct"] or 0)))

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
                           f'<td colspan="6" class="left">財報窗內 — 原版被擋，現行配置放行（見發現②）</td></tr>')
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
.decided{{display:inline-block;padding:2px 9px;border-radius:5px;font-size:10.5px;font-weight:700;background:#dcfce7;color:#166534;margin-left:8px}}
.honesty{{background:#fef2f2;border:2px solid #fca5a5;border-radius:10px;padding:16px 20px;font-size:13px;color:#7f1d1d;line-height:1.8;margin-bottom:20px}}
.honesty strong{{display:block;font-size:14px;margin-bottom:6px}}
.honesty .ok-list{{color:#14532d;background:#f0fdf4;border-radius:6px;padding:8px 14px;margin-top:8px;font-size:12px}}
.finding{{border-left:4px solid #dc2626;background:#fff;border-radius:0 10px 10px 0;border-top:1px solid #dce8f5;border-right:1px solid #dce8f5;border-bottom:1px solid #dce8f5;padding:14px 18px;margin-bottom:14px}}
.finding h3{{font-size:14px;color:#0f2a45;margin-bottom:6px}}
.finding p{{font-size:12px;color:#475569;line-height:1.7}}
.finding .nums{{font-size:13px;font-weight:700;margin:6px 0;font-variant-numeric:tabular-nums}}
.finding table{{margin-top:8px;max-width:520px}}
.kpi{{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0}}
.kpi div{{background:#f0f5fb;border:1px solid #dce8f5;border-radius:6px;padding:7px 12px;font-size:11px;color:#5a7a9a}}
.kpi strong{{display:block;font-size:14px;color:#1e3a5f}}
.kpi .main strong{{color:#059669}}
.kpi .ghost strong{{color:#94a3b8}}
.caveat{{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:14px 18px;font-size:12px;color:#854d0e;line-height:1.7}}
.caveat ul{{margin-left:20px}}
h4{{font-size:12px;color:#0f2a45;margin:14px 0 6px}}
footer{{text-align:center;font-size:10.5px;color:#8aa5c0;padding:24px}}
.ghost-note{{font-size:10.5px;color:#94a3b8}}
</style>
</head>
<body>
{NAV_BLOCK}

<div class="hero"><div class="hero-inner">
<div class="hero-h1">SOP 漏斗 2022 回測 — 技術執行層 × 規則實驗室</div>
<div class="hero-sub">窗口 {d["window_start"]} → {d["window_end"]} · {d["price_basis"]} · 母體 = <strong>凍結 2026-06-11 的 {d["n_gated"]} 檔五條件過閘名單</strong>。本頁是規則對照實驗，不是選股能力證明。<strong>2026-06-11 裁決：拿掉斷路器、財報靜默期改「標記不擋」</strong>——現行配置（綠線）= 無斷路器 × 財報窗放行；裁決依據與其證據等級見 §1。</div>
</div></div>

<div class="section">
<div class="honesty">
<strong>⚠ 誠實邊界 — 先讀這個再看數字</strong>
五條件閘門用的是<u>今天</u>的分析師預估與護城河評級（歷史版本不存在），universe 是<u>今天</u>策展的 DD 名單——2022 年的漏斗會選出不一樣的股票。因此：<u>所有絕對報酬數字（CAGR、終值、α）一律視為灰色參考</u>，它們繼承了「拿今天的贏家回去考古」的樂觀偏誤。
<div class="ok-list">站得住的結論（同名單內部對照，偏誤兩邊抵銷）：① 斷路器死鎖 ② 靜默期影響 ③ 態④ A/B ④ 型態行為 ⑤ 閘門對照（殘留偏誤較大）。選股能力的無偏證據 = <a href="/dd-screener/sop-funnel.html">主頁 forward 帳本</a>。Phase 2（point-in-time 代理閘門）另議。</div>
</div>
</div>

<div class="section"><div class="card">
<h2>§1 發現與裁決</h2>
<div class="finding">
<h3>發現① 斷路器死鎖 <span class="decided">已裁決 2026-06-11：拿掉</span></h3>
<div class="nums">含斷路器終值 <span class="neg">{t2["final_nav"]:.0f}</span> vs 拿掉後 <span class="pos">{nb["final_nav"]:.0f}</span>（同訊號同名單，唯一變數 = 斷路器）</div>
<p>2024-07 曝險 ~83% 遇急跌，NAV -10.1% 觸發斷路器（{t2["breaker_episodes"][0]["trigger"] if t2["breaker_episodes"] else "—"}）→ 五狀態機把部位停損至滿手現金 → NAV 凍在回撤區<strong>永遠回不到 -5% 解除線</strong> → 後續 {t2["blocked_entries"]} 筆進場被擋到期末。解除條件假設「部位反彈收復回撤」，但觸發時部位已被砍光——條文與狀態機交互產生死鎖。<strong>裁決：拿掉斷路器</strong>。代價是失去帳戶層保險絲（whipsaw 市況的連續停損無人喊停），列入季檢覆議。</p>
</div>
<div class="finding" style="border-left-color:#d97706">
<h3>發現② 財報靜默期 — 擋下 {g["n_silent_blocked"]}/{g["n_signals"]} 筆（{silent_pct}%）<span class="decided">已裁決 2026-06-11：標記不擋</span></h3>
<div class="nums">有禁令：α {_pct(g["mean_alpha_pct"])} · R {g["mean_r"]} · NAV(無斷路器) {nb["final_nav"]:.0f}　vs　拿掉禁令：α {_pct(gns["mean_alpha_pct"])} · R {gns["mean_r"]} · NAV {ns["final_nav"]:.0f}</div>
<p>被擋 14 筆中實際成交的 {len(d.get("silent_counterfactual", []))} 筆放行後<strong>全數獲利</strong>（下表）。⚠ 但此證據含重度 survivorship 偏誤：凍結名單 = 今日贏家，其歷史財報多為利多，「衝著財報買」在贏家名單上只剩好的一面；且 FIX 一筆 +186% 扛走大半差距。<strong>裁決：forward 系統改「標記不擋」</strong>——財報窗內進場照進、標 ⚠，累積無偏數據供季檢複驗是否恢復禁令。</p>
<table><thead><tr><th class="left">ticker</th><th>訊號日</th><th>放行後報酬</th><th>下場</th></tr></thead><tbody>{cf_rows}</tbody></table>
</div>
<div class="finding" style="border-left-color:#2563eb">
<h3>發現③ 態④減碼幅度 A/B — 階梯小勝，不構成改規則的強證據</h3>
<div class="nums">charter 一次 50%：α {_pct(g["mean_alpha_pct"])} · R {g["mean_r"]}　vs　階梯 25%+25%：α {_pct(st["mean_alpha_pct"])} · R {st["mean_r"]}</div>
<p>與態④ trim-variants 舊研究（流程指標）合併讀，維持現行規則，供 2026-09 季檢。</p>
</div>
<div class="finding" style="border-left-color:#059669">
<h3>發現④ 型態行為 — A1 起漲樣本極稀但彈道不同</h3>
<div class="nums">A1：{bt["A1"]["n_entered"]} 筆 · 平均 {_pct(bt["A1"]["mean_ret_pct"])} · α {_pct(bt["A1"]["mean_alpha_pct"])}　|　A2：{bt["A2"]["n_entered"]} 筆 · 平均 {_pct(bt["A2"]["mean_ret_pct"])} · α {_pct(bt["A2"]["mean_alpha_pct"])}　|　B：{bt["B"]["n_entered"]} 筆 · 平均 {_pct(bt["B"]["mean_ret_pct"])} · α {_pct(bt["B"]["mean_alpha_pct"])}</div>
<p>4.4 年僅 {bt["A1"]["n_signals"]} 筆乾淨 A1（長基期突破本就稀有），樣本不足下結論——forward 帳本 A1 vs A2 預登記裁決（closed ≥20）才是正式裁判。</p>
</div>
<div class="finding" style="border-left-color:#7c3aed">
<h3>發現⑤ 226 檔純價格對照 — 閘門的價值主要在風險端</h3>
<div class="nums">現行配置（23 檔過閘）：NAV {ns["final_nav"]:.0f} · MDD {_pct(ns["mdd_pct"])} · Sharpe {ns["sharpe"]}　vs　226 檔純價格（無閘門）：NAV {ung["final_nav"]:.0f} · MDD {_pct(ung["mdd_pct"])} · Sharpe {ung["sharpe"]}</div>
<p>不看 ROIC/EPS/護城河、純價格規則跑全 universe：報酬相近（{ung["final_nav"]:.0f} vs {ns["final_nav"]:.0f}）但<strong>回撤深得多（{_pct(ung["mdd_pct"])} vs {_pct(ns["mdd_pct"])}）、曝險高得多（{ung["avg_exposure_pct"]:.0f}% vs {ns["avg_exposure_pct"]:.0f}%）</strong>——閘門在這份資料裡的作用不是挑出更會漲的票，是用更少的曝險、更淺的坑拿到相近報酬（風險調整後 Sharpe {ns["sharpe"]} vs {ung["sharpe"]}）。⚠ 仍含殘留偏誤：「今天過閘」與「過去表現好」相關；per-trade 口徑下無閘門組勝率僅 {_pct(ug_s["win_rate"], signed=False)}、中位 {_pct(ug_s["median_ret_pct"])}、α {_pct(ug_s["mean_alpha_pct"])}（vs 過閘組 {_pct(g["win_rate"], signed=False)} / {_pct(g["median_ret_pct"])} / {_pct(g["mean_alpha_pct"])}）。</p>
</div>
</div></div>

<div class="section"><div class="card">
<h2>§2 NAV 曲線（灰色參考 — 凍結名單偏誤未除）</h2>
<div class="desc">起始 100 · charter S-2 部位規則（min(10%, 1.5%÷停損)×NAV · 總曝險≤100% · 純現股）· 同日優先序 A1&gt;B&gt;A2。<strong>綠線 = 現行配置</strong>（裁決後：無斷路器 × 財報窗放行）；紅線 = charter 原版（含斷路器 → 2024-07 死鎖後曝險歸零）；紫線 = 226 檔純價格。</div>
{svg_chart(d)}
<div class="kpi">
<div class="main"><strong>{ns["final_nav"]:.0f}</strong>現行配置終值</div>
<div class="ghost"><strong>{t2["final_nav"]:.0f}</strong>charter 原版（死鎖）</div>
<div class="ghost"><strong>{ung["final_nav"]:.0f}</strong>226 純價格</div>
<div class="ghost"><strong>{_e(spy_final and round(spy_final))}</strong>SPY</div>
<div class="ghost"><strong>{_e(qqq_final and round(qqq_final))}</strong>QQQ</div>
<div><strong>{_pct(ns["mdd_pct"])}</strong>現行 MDD</div>
<div><strong>{_e(ns["sharpe"])}</strong>現行 Sharpe</div>
<div><strong>{ns["avg_exposure_pct"]:.0f}%</strong>平均曝險</div>
<div><strong>{ns["pct_days_flat"]:.0f}%</strong>空手日比</div>
</div>
<div class="ghost-note">絕對數字皆含凍結名單偏誤；本圖合法用途是各線之間的「形狀差」（規則影響）與曝險行為，不是與 SPY 比絕對高低。</div>
</div></div>

<div class="section"><div class="card">
<h2>§3 年度拆分（gated · charter 態④ · 含靜默期禁令版本）</h2>
<div class="desc">2022 全熊市：進場稀少且全敗但被停損框住 — 防禦行為符合設計；訊號集中在 2023 復甦與 2025。</div>
<table><thead><tr><th class="left">年</th><th>進場</th><th>財報窗</th><th>勝率</th><th>中位報酬</th><th>平均報酬</th></tr></thead>
<tbody>{yearly_rows}</tbody></table>
</div></div>

<div class="section"><div class="card">
<h2>§4 規則組合總表（per-trade 口徑）</h2>
<table><thead><tr><th class="left">組</th><th>訊號</th><th>進場</th><th>財報窗</th><th>勝率</th><th>中位報酬</th><th>平均報酬</th><th>α vs SPY</th><th>平均R</th><th>中位持有</th></tr></thead>
<tbody>
{stat_row(f'現行配置：過閘 {d["n_gated"]} 檔 · 財報窗放行', gns)}
{stat_row(f'原版：過閘 {d["n_gated"]} 檔 · 靜默期禁令', g)}
{stat_row('態④階梯變體（A/B）', st, muted=True)}
{stat_row(f'226 檔純價格（無閘門）', ug_s, muted=True)}
</tbody></table>
</div></div>

<div class="section"><div class="card">
<h2>§5 Trade 明細（原版口徑 · {g["n_entered"]} 筆進場 + {g["n_silent_blocked"]} 筆財報窗）</h2>
<table><thead><tr><th class="left">ticker</th><th>型態</th><th>訊號日</th><th>出場日</th><th>原因</th><th>報酬</th><th>R</th><th>α</th><th>持有</th></tr></thead>
<tbody>{trade_rows}</tbody></table>
</div></div>

<div class="section"><div class="card">
<h2>§6 方法論與已知偏誤</h2>
<div class="caveat"><ul>{caveat_lis}
<li>全動作 T+1 收盤執行；週線指標用已完成週凍結值（無部分週 look-ahead）</li>
<li>NAV 模擬：現金不計息、零交易成本；回補腿受現金約束、賣腿永遠執行</li>
<li>2026-06-11 裁決記錄：拿掉斷路器（死鎖發現）、靜默期改標記不擋（含偏證據，forward 標記複驗）— 兩項皆列季檢覆議</li>
<li>Phase 2（point-in-time 代理閘門：trailing 指標 + 季度資格窗 + 財報滯後）需 Koyfin 歷史財報匯出，另議</li>
</ul></div>
</div></div>

<footer class="imq-foot">
  <div>© 2026 InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</body></html>
"""
    OUT_HTML.write_text(_plain_states(page), encoding="utf-8")
    print(f"rendered → {OUT_HTML}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
