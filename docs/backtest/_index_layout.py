"""LIVE renderer for /backtest/index.html — four-tab categorised directory.

This is the layout that actually builds the live page: _build_index.py's
main() calls render() here and writes docs/backtest/index.html.  Data
(GROUPS/RET/SCATTER/BH_ROWS/PERIOD_CAGR...) still lives in _build_index.py;
its legacy render()/TEMPLATE are DEAD code kept only as data helpers.

2026-07-17 redesign — four-tab true filtering
=============================================
Owner feedback: the four top tabs (美股/台股/多資產/槓桿疊加) used to be plain
page-links while the shared make_toggle pill bar dumped ALL seven groups
(多資產/台股波段/台股選擇權/日內…) onto every page — so the 美股 page showed
台股/多資產/日內 rows.  Now the index is a single page whose four tabs are
pure front-end JS filters over a per-tab directory:

  * Every navigable entry (pill / link) lives in EXACTLY ONE tab.  The only
    cross-tab links are the always-visible 方法論 utilities (評估標準/術語表)
    and /long-track-adaptive-vt/ (自適應美台總覽 — legitimately US+TW).
  * Tabs switch client-side (showTab); the standalone /backtest/{tw,multi,
    leverage}/ overview pages still exist and are reached via each tab's CTA.
  * Classification (2026-07): GEM(SPY/ACWX 雙動能) → 多資產 (global-rotation
    nature); 全球/18-市場 日週研究(dvw_global/dvw_deep) → 多資產; SG Trend /
    全球斜率 → 多資產; all TXO + 台指日內 → 台股.  The US-overview comparison
    ANALYTICS (波段 ranking, 完整比較表, scatter, 逐年/分期 CAGR) are left
    exactly as the pinned data defines them — GEM stays there only as a
    benchmarked 參照 row/column, its NAV pill lives under 多資產.  完整比較表
    is filtered to US groups (🇹🇼 group belongs to the 台股 tab/page).

No sub-page generator is re-run; only index.html is regenerated.
Run: python3 _build_index.py   (this module is imported, not run directly)
"""
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _build_index as idx

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("quant", "bt")
OUT = Path(__file__).parent / "index.html"

GREEN, RED, GREY = "#16a34a", "#dc2626", "#9ca3af"

# the single live card
LIVE_CARD = {
    "name": "SMH/QQQ · STX50", "tag": "舊實倉（2026-07-18 前）",
    "sub": "50/50 SMH/QQQ · E3 三訊號 + 週線 ST(10,3) 半倉出場閘門 · 舊進攻位（實單已改用 W52 × 自適應波動率 150%）",
    "cagr": "+13.84%", "mdd": "-21.87%", "sharpe": "0.90", "calmar": "0.63",
    "url": "/backtest/long_track_smh/",
}

# ── per-tab directory ────────────────────────────────────────────────────
# tab -> [ (row_label, [ (url, text, status_or_None, is_current), ... ]) ]
# status ∈ 否決/失敗/負貢獻 (red) · 未過/觀察/研究/模擬中/專區 (amber) · 追蹤中/即將 (blue)
DIRECTORY = {
    "us": [
        ("總覽・工具", [
            ("/backtest/", "20 年總覽", None, True),
            ("/backtest/10y/", "10 年對比", None, False),
            ("/backtest/ma_sensitivity/", "MA 敏感度", None, False),
            ("/backtest/free_lunch/", "分散與免費午餐", None, False),
        ]),
        ("個別系統", [
            ("/backtest/long_track_smh/", "SMH/QQQ 進攻", None, False),
            ("/backtest/long_track_ensemble/", "SPY/QQQ 集成", None, False),
            ("/backtest/slope_filter/", "SPY/AGG 斜率", None, False),
            ("/backtest/long_track/", "SPY/QQQ 長軌", None, False),
            ("/backtest/long_track_qqq/", "QQQ 長軌純攻", None, False),
            ("/backtest/six_state/", "QQQ＋SMH 六狀態", None, False),
            ("/backtest/six_state_v1r1/", "QQQ 六狀態實盤", None, False),
            ("/backtest/supertrend/", "週線 Supertrend", None, False),
            ("/backtest/minervini/", "Minervini RS+VCP", None, False),
            ("/backtest/mom_volscaling/", "動能·波動縮放", None, False),
            ("/backtest/dual_track_study/", "雙軌分散研究", None, False),
            ("/backtest/vol_targeting/", "波動目標倉位", "研究", False),
            ("/backtest/vol_targeting/adaptive.html", "波動率變體實驗室", "研究", False),
            ("/backtest/rsi2_mr/", "SPY/QQQ 均值回歸", None, False),
            ("/backtest/dual_track/", "SPY/QQQ 雙軌多空", "否決", False),
            ("/backtest/exit_switch/", "出場法切換", "否決", False),
            ("/backtest/short_system/", "指數做空", "失敗", False),
        ]),
        ("選擇權研究", [
            ("/backtest/cndr/", "Iron Condor", "失敗", False),
            ("/backtest/covered_call/", "Covered Call", "負貢獻", False),
            ("/backtest/put_timing/", "SPY/QQQ 買 put 避險", "負貢獻", False),
        ]),
        ("研究・主動式ETF", [
            ("/backtest/active_etf/", "主動式 ETF 研究總結（台美）", "專區", False),
            ("/backtest/us_active_etf/", "美股主動式 ETF 因子分析", "研究", False),
        ]),
        ("研究・頻率", [
            ("/backtest/daily_vs_weekly/", "日/週線", None, False),
        ]),
        ("研究・均線", [
            ("/backtest/ma_cross/", "MA 交叉", None, False),
            ("/backtest/ma_deviation/", "MA 乖離", None, False),
            ("/backtest/ma_dynband/", "MA 動態帶", None, False),
            ("/backtest/ma_squeeze/", "MA 擠壓", None, False),
        ]),
        ("研究・崩盤", [
            ("/backtest/smh_vcrash/", "SMH V崩", None, False),
        ]),
        ("前瞻追蹤", [
            ("/long-track-w52-adaptive/", "W52 × 自適應波動率 150%（實單主系統）", "實單", False),
            ("/long-track-qs-vt/", "QQQ+SMH 固定 σ（歸檔）", None, False),
            ("/long-track-qs-vt/adaptive.html", "QQQ+SMH 自適應（歸檔）", None, False),
            ("/long-track-adaptive-vt/", "自適應美台總覽（歸檔）", None, False),
        ]),
    ],
    "tw": [
        ("波段", [
            ("/backtest/tw_0050_compare/", "0050 總覽·台美差異", None, False),
            ("/backtest/tw_0050/", "0050 進攻趨勢", None, False),
            ("/backtest/tw_0050_lt/", "0050 長軌趨勢", None, False),
            ("/backtest/long_track_tw/", "2330/0050 E3 長軌", None, False),
            ("/backtest/vol_targeting/tw.html", "0050+2330 波動率變體", "研究", False),
            ("/backtest/tw_0050_six/", "0050 六狀態機", None, False),
            ("/backtest/tw_0050_dual/", "0050 雙軌多空", "否決", False),
        ]),
        ("選擇權", [
            ("/backtest/tw_options/", "台股選擇權專區", "專區", False),
            ("/backtest/txo_vol_seller/", "台指選擇權賣方", "模擬中", False),
            ("/backtest/txo_put_seller/", "台指賣方下檔", "研究", False),
            ("/backtest/txo_iron_condor/", "台指雙賣", "研究", False),
            ("/backtest/txo_covered_call_0050/", "台指 Covered Call", "研究", False),
            ("/backtest/txo_tail_hedge/", "台指尾端避險", "研究", False),
        ]),
        ("日內交易", [
            ("/backtest/txf_intraday/", "台指當沖", "未過", False),
            ("/backtest/txf_chips/", "籌碼偏向", "觀察", False),
            ("/backtest/ssf_xsec/", "個股期橫斷面", "未過", False),
            ("/backtest/txf_basis/", "基差偏向", "否決", False),
        ]),
        ("研究・主動式ETF", [
            ("/backtest/active_etf/", "主動式 ETF 研究總結（台美）", "專區", False),
            ("/backtest/tw_active_etf/", "台股主動式 ETF 因子分析", "研究", False),
        ]),
        ("研究・頻率", [
            ("/backtest/daily_vs_weekly_tw/", "日/週·台股", None, False),
        ]),
        ("研究・崩盤", [
            ("/backtest/tw_vcrash/", "台股 V崩防禦", None, False),
            ("/backtest/tw_crash/", "台股含崩盤驗證", None, False),
        ]),
        ("前瞻追蹤", [
            ("/long-track-w52-adaptive/", "W52 × 自適應波動率 150%（實單主系統）", "實單", False),
            ("/long-track-tw-vt/", "0050+2330 固定 σ（歸檔）", None, False),
            ("/long-track-tw-vt/adaptive.html", "0050+2330 自適應（歸檔）", None, False),
            ("/long-track-adaptive-vt/", "自適應美台總覽（歸檔）", None, False),
        ]),
    ],
    "multi": [
        ("系統", [
            ("/backtest/turtle/", "唐奇安突破", None, False),
            ("/backtest/clenow/", "跨資產趨勢", None, False),
            ("/backtest/multiasset_trend/", "SG Trend 複製", None, False),
            ("/backtest/turtle_adopt/", "組合採用 Sleeve", None, False),
            ("/backtest/slope_filter_global/", "全球斜率穩健性", None, False),
            ("/backtest/crossasset_defense/", "跨資產防守", None, False),
            ("/backtest/gem/", "SPY/ACWX 雙動能", None, False),
        ]),
        ("研究・頻率", [
            ("/backtest/daily_vs_weekly_global/", "日/週·全球", None, False),
            ("/backtest/daily_vs_weekly_deep/", "日/週·深掘（18 市場）", None, False),
        ]),
    ],
    "lev": [
        ("系統", [
            ("/backtest/leverage_voltarget/", "期貨槓桿疊加", None, False),
            ("/backtest/vol_targeting/leverage.html", "W52×自適應 150% 槓桿", "研究", False),
        ]),
    ],
}


def _badge(status):
    if not status:
        return ""
    if status in ("否決", "失敗", "負貢獻"):
        kind = "d"
    elif status in ("追蹤中", "即將"):
        kind = "t"
    else:
        kind = "w"
    return f'<span class="b b-{kind}">{status}</span>'


def _pill(url, text, status=None, current=False):
    cls = ' class="on"' if current else ""
    return f'<a href="{url}"{cls}>{text}{_badge(status)}</a>'


def _dir(tab):
    rows = ""
    for label, items in DIRECTORY[tab]:
        pills = "".join(_pill(*p) for p in items)
        rows += (f'<div class="dir-row"><div class="dir-lbl">{label}</div>'
                 f'<div class="dir-pills">{pills}</div></div>')
    return f'<div class="dir">{rows}</div>'


def lane(title):
    if "採用" in title:
        return GREEN
    if "否決" in title:
        return RED
    return GREY


def is_position(title):   # US 波段 (exclude multi-asset + TW group)
    return "🇹🇼" not in title and "多資產" not in title


def slim_row(name, url, sub, cagr, mdd, sharpe, calmar, dom_key, final, tag, lc):
    cagr_h = (f'<td style="font-weight:700;color:var(--green)">{cagr}</td>' if cagr != "—" else "<td>—</td>")
    mdd_h = f'<td style="color:var(--muted)">{mdd}</td>' if mdd != "—" else "<td>—</td>"
    return (f'<tr style="border-left:3px solid {lc}"><td><a href="{url}" style="font-weight:600">{name}</a>'
            f'<div style="font-size:.72rem;color:var(--muted);margin-top:.15rem">{sub}</div></td>'
            f'{cagr_h}{mdd_h}<td>{calmar}</td><td>{idx.DOM[dom_key]}</td><td>{tag}</td></tr>')


def section_header(title, lc):
    return (f'<tr><td colspan="6" style="background:#f8fafc;border-left:3px solid {lc};'
            f'font-size:.74rem;font-weight:700;color:#475569;text-transform:uppercase;'
            f'letter-spacing:.04em">{title}</td></tr>')


# US research link-cards (verbatim) — only US-scoped notes belong to 美股 tab.
US_RESEARCH = r"""<a class="link-card" href="/backtest/mom_volscaling/" style="border-left:3px solid var(--grey)">
  <span style="font-size:1.3rem">🌀</span>
  <span><span class="lc-name">美股動能・波動率縮放 · Barroso & Santa-Clara (2015) 複驗</span><br><span class="lc-sub">複驗 · WML 動能用已實現波動事前削平崩盤 · 真 OOS 2014-2026 Sharpe 0.26→0.52、MDD −77.6%→−27.2%,bootstrap 95% CI [+0.04,+0.45] 不含 0(顯著)· 只答機制存活性、不答可交易性(無成本)· 2020-03 反彈期削獲利是雙面刃</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/dual_track_study/" style="border-left:3px solid var(--green)">
  <span style="font-size:1.3rem">🧪</span>
  <span><span class="lc-name">雙軌分散研究 · 短MR + 長趨勢 on SMH/QQQ</span><br><span class="lc-sub">過尺 · 真實引擎(E3 長軌 + RSI2 短軌)· Calmar 0.65→0.70、MDD −27%→−18% · 兩條軸(時間架構/驅動)收斂到雙軌 = v7 Ch12 設計</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/minervini/" style="border-left:3px solid var(--red)">
  <span style="font-size:1.3rem">🔬</span>
  <span><span class="lc-name">Minervini RS+VCP 機械回測 ·《超級績效》</span><br><span class="lc-sub">否決 · 存活者偏誤樂觀上界，非忠實回測 · 即使偏誤灌水 CAGR 仍輸大盤；三槓桿(出場/進場/部位)皆推不開報酬↔回撤前緣 → alpha 在裁量、不可機械化</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/smh_vcrash/" style="border-left:3px solid #d97706">
  <span style="font-size:1.3rem">🛡️</span>
  <span><span class="lc-name">突發 V 崩防禦 · SMH/QQQ STX50</span><br><span class="lc-sub">同台股研究套到美股 · 唯一過尺仍是分散腿，但 2022 股債雙殺讓債券危機腿反向(TLT 只 10% 過、上不去)· 跨 regime 穩健只剩黃金(過尺 10–40%);純對沖股票(put/加速出場/vol-target)全失敗</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/daily_vs_weekly/" style="border-left:3px solid #1a56db">
  <span style="font-size:1.3rem">⏱️</span>
  <span><span class="lc-name">日線 vs 週線長軌 · SPY/QQQ/SMH</span><br><span class="lc-sub">長軌規則搬到日線 D60/120/200,加遍出場確認/盤整閘門(ER·R²·ADX·CHOP)/多空/200日方向/MA組合 · 0/72 真過尺，週線 long-only 是最優；盤整閘門只是重建週線、空單任何濾網都救不活</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/ma_deviation/" style="border-left:3px solid #1a56db">
  <span style="font-size:1.3rem">📐</span>
  <span><span class="lc-name">乖離率擇時 · 微笑曲線 (QQQ/SMH/SPY/0050)</span><br><span class="lc-sub">價對均線偏離當買賣訊 · 買側是微笑曲線(兩端深超賣/強噴出有 edge、中段最沒用),最強格深超賣 in 上升趨勢 +22%/60d 但稀有；乖離當賣訊是反指標(高乖離續漲、低乖離反彈),出場 overlay 疊週線全是幻象/有害</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/ma_cross/" style="border-left:3px solid #1a56db">
  <span style="font-size:1.3rem">✕</span>
  <span><span class="lc-name">黃金/死亡交叉 · 慢晚回吐大 (QQQ/SMH/SPY/0050)</span><br><span class="lc-sub">快×慢均線交叉當進出訊 · 0/20 過尺 · CAGR 不輸週線但交叉出場太晚、MDD 一律更深(SMH 10/30 −44%);交叉事件前瞻邊際近零，死叉甚至不是乾淨賣訊(50/200 死叉後 120日 +2.5%);「站上家族」最後一塊，仍敗給週線</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/ma_squeeze/" style="border-left:3px solid #1a56db">
  <span style="font-size:1.3rem">🪢</span>
  <span><span class="lc-name">均線糾結→發散 · 糾結不加值 (QQQ/SMH/SPY/0050)</span><br><span class="lc-sub">多均線收斂後發散點火進場 · 點火 60日超額 −2.1%、比「無糾結純突破」對照(−0.8%)更差 = 糾結減值；系統 3/8 過尺但無糾結對照過得一樣好(QQQ 純突破 0.63≥糾結)→ 是底層突破持有+200日出場在做工，且全擠在弱週線市(QQQ/SPY)= 弱基準假象</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/ma_dynband/" style="border-left:3px solid #1a56db">
  <span style="font-size:1.3rem">📊</span>
  <span><span class="lc-name">ATR/σ 動態乖離帶 · 解決稀有沒解決可交易 (QQQ/SMH/SPY/0050)</span><br><span class="lc-sub">把固定% 乖離門檻換波動標準化(布林/肯特納) · 深超賣訊號 n 1-2→70-110 變密 ✓,但揭穿固定−15%「深超賣神格」是門檻錯覺(σ 單位下極端反轉負、甜蜜點移到中度−1~−2σ);跨標的仍不一致、曝險僅 8-33%,系統 1/32 過尺幻象 — MA 進場方法系列收尾</span></span>
  <span class="lc-arrow">→</span>
</a>"""

# Multi-asset / global research link-cards (verbatim) — moved to 多資產 tab.
MULTI_RESEARCH = r"""<a class="link-card" href="/backtest/multiasset_trend/" style="border-left:3px solid var(--grey)">
  <span style="font-size:1.3rem">📈</span>
  <span><span class="lc-name">多資產期貨・趨勢追蹤 · SG Trend Index 複製</span><br><span class="lc-sub">複驗(非發明)· 10 檔期貨/ETF 代理零參數搜索 · 對 SG 官方月報酬相關 0.647、2022 +21.92% ✓,驗收 2/3 過 · CAGR 2.79% 遠不及 SG(第3條深回撤不過 = universe 廣度不足非 bug)· 複製的是風格不是報酬水準；CL=F/SI=F 幻影拼接已審計剔除</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/slope_filter_global/" style="border-left:3px solid #1a56db">
  <span style="font-size:1.3rem">🌍</span>
  <span><span class="lc-name">W52 斜率濾網 · 全球 15 國 ETF 穩健性</span><br><span class="lc-sub">穩健性地圖 · 同規則套 15 國指數 ETF · MDD 控制 15/15 普世(平均淺 +25.7pp)、CAGR 0/15 全輸 B&amp;H、Sharpe 9/15 只在乾淨週期市 · 換倉↔折損 corr −0.79(澳洲 41 次極端)、慢熊到處有效/急殺月度太慢</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/daily_vs_weekly_global/" style="border-left:3px solid #d97706">
  <span style="font-size:1.3rem">🌐</span>
  <span><span class="lc-name">日線 vs 週線長軌 · 全球 14 國 ETF</span><br><span class="lc-sub">同調查推廣到 14 個國家股票 ETF · 長軌 edge 集中在強趨勢市場(美/0050),多數國家週線 Calmar 僅 0.05–0.30;日線「過尺」全擠在週線最弱的市場 = 弱基準假象，非日線 alpha</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/daily_vs_weekly_deep/" style="border-left:3px solid #059669">
  <span style="font-size:1.3rem">🔬</span>
  <span><span class="lc-name">深掘：長軌 edge 在哪、為什麼、能否輪動 · 18 市場</span><br><span class="lc-sub">市場趨勢度(週線ER)以 r=+0.88 預測長軌 Calmar(事前可算);弱市場=趨勢不持久(在場僅36-42%+被洗);但動態跨市場輪動全失敗(輸「只用美國」0.46 vs 0.09-0.16、追高加深MDD)→ 結構關係只能靜態選市場吃、不能輪動</span></span>
  <span class="lc-arrow">→</span>
</a>"""


def render():
    c = LIVE_CARD
    card = f"""<div class="acard">
  <div class="ac-tag">{c['tag']}</div>
  <div class="ac-name">{c['name']}</div>
  <div class="ac-sub">{c['sub']}</div>
  <div class="ac-metrics">
    <div><span>CAGR</span><b style="color:var(--green)">{c['cagr']}</b></div>
    <div><span>MDD</span><b>{c['mdd']}</b></div>
    <div><span>Sharpe</span><b>{c['sharpe']}</b></div>
    <div><span>Calmar</span><b>{c['calmar']}</b></div>
  </div>
  <a class="ac-link" href="{c['url']}">詳細頁 →</a>
</div>
<div class="acard-note">
  <div class="acn-title">其餘已採用 / 候補(未上實倉)</div>
  <ul>
    <li><a href="/backtest/long_track_ensemble/">SPY/QQQ E3 集成</a> — 合格候補(原列採用，未上實倉)· 核心防守</li>
    <li><a href="/backtest/slope_filter/">SPY/AGG 斜率</a> — 合格候補 · 勝 B&amp;H 風險調整(SPY 特定；2026-06 審計改還原日線 MDD −22.13% 後，「近支配」已撤回)</li>
  </ul>
</div>"""

    # 波段 table (US position systems; experimental/rejected collapsed)
    main_rows, tail_rows = "", ""
    for title, items in idx.GROUPS:
        if not is_position(title):
            continue
        lc = lane(title)
        hdr = section_header(title, lc)
        body = "".join(slim_row(*r, lc) for r in items)
        if "實驗" in title or "否決" in title:
            tail_rows += hdr + body
        else:
            main_rows += hdr + body
    bh = "".join(
        f'<tr style="background:#fafbfc;border-left:3px solid {GREY}"><td>{n}</td><td>{c}</td>'
        f'<td style="color:var(--muted)">{m}</td><td>{cl}</td><td>—</td><td>{idx.TAG["bh"]}</td></tr>'
        for n, c, m, s, cl in idx.BH_ROWS)

    period = "".join(
        f'<tr><td style="font-weight:600">{name}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>'
        for name, _color, a, b, c, d in idx.PERIOD_CAGR)

    # 完整比較表 — US groups only (🇹🇼 group has its own 台股 tab/page)
    full_rows = ""
    for title, items in idx.GROUPS:
        if not is_position(title):
            continue
        full_rows += idx.group_header(title) + "".join(idx.sys_row(*r) for r in items)
    full_rows += idx.group_header("基準(Buy &amp; Hold)") + "".join(
        f'<tr style="background:#fafbfc"><td>{n}</td><td>{c}</td><td style="color:var(--muted)">{m}</td>'
        f'<td>{s}</td><td>{cl}</td><td>—</td><td>—</td><td>{idx.TAG["bh"]}</td></tr>'
        for n, c, m, s, cl in idx.BH_ROWS)

    yhead = "".join(f'<th>{h}</th>' for _, h, _c in idx.YEARLY_COLS)
    yrows = ""
    for i, y in enumerate(idx.YEARS):
        yrows += f"<tr><td>{y}</td>" + "".join(idx.yearly_cell(idx.RET[k][i]) for k, _, _ in idx.YEARLY_COLS) + "</tr>\n"

    # scatter recoloured by category (green adopted / grey bench&others / red rejected)
    def scat_color(label):
        if "進攻" in label or "集成" in label:
            return GREEN
        if "B&H" in label:
            return "#94a3b8"
        if "雙軌" in label or "做空" in label or "回歸" in label:
            return RED
        return "#64748b"
    scatter = [dict(label=l, x=x, y=y, color=scat_color(l)) for l, x, y, _c in idx.SCATTER]

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%US_DIR%": _dir("us"), "%TW_DIR%": _dir("tw"),
        "%MULTI_DIR%": _dir("multi"), "%LEV_DIR%": _dir("lev"),
        "%CARD%": card, "%MAIN_ROWS%": main_rows, "%TAIL_ROWS%": tail_rows, "%BH_ROWS%": bh,
        "%US_RESEARCH%": US_RESEARCH, "%MULTI_RESEARCH%": MULTI_RESEARCH,
        "%PERIOD_ROWS%": period,
        "%FULL_ROWS%": full_rows, "%YEARLY_HEAD%": yhead, "%YEARLY_ROWS%": yrows,
        "%JS_RET%": json.dumps(idx.RET), "%JS_SCATTER%": json.dumps(scatter),
        "%JS_YEARS%": json.dumps(idx.YEARS), "%NOW%": datetime.now().strftime("%Y-%m-%d"),
    }.items():
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>量化回測總覽 | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--ink:#1f2937;--text:#374151;--muted:#6b7280;--border:#e5e7eb;--bg:#f7f8fa;--card:#fff;
      --green:#16a34a;--green-bg:#f0fdf4;--green-border:#bbf7d0;--red:#dc2626;--grey:#9ca3af}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;font-size:15px}
a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1080px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.5rem 0 1rem;background:#fff;border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.45rem;font-weight:800;letter-spacing:-.03em;color:var(--ink)}
.page-hdr .sub{color:var(--muted);font-size:.85rem;margin-top:.15rem}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}.crumb a{color:var(--muted)}
.tabs{display:flex;gap:.4rem;margin-top:.9rem;flex-wrap:wrap}
.tabs a{font-size:.86rem;font-weight:600;padding:.4rem .9rem;border:1px solid var(--border);border-radius:7px;color:var(--muted);background:#fff;cursor:pointer}
.tabs a:hover{text-decoration:none;border-color:var(--ink)}
.tabs a.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.methods{display:flex;align-items:center;flex-wrap:wrap;gap:.5rem;margin-top:.6rem;font-size:.8rem}
.methods .m-lbl{font-size:.66rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
.methods a{padding:.2rem .6rem;background:#eef2ff;border:1px solid #c7d2fe;border-radius:999px;color:#3730a3;font-weight:600}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.05rem;font-weight:700;color:var(--ink);margin-bottom:.85rem;padding-bottom:.4rem;border-bottom:1px solid var(--border)}
.section-sub{font-size:.82rem;color:var(--muted);margin:-.45rem 0 .9rem}
.dir{background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin:1.1rem 0}
.dir-row{display:flex;align-items:flex-start;gap:.55rem;padding:.34rem .6rem;border-top:1px solid var(--border)}
.dir-row:first-child{border-top:0}
.dir-lbl{flex:0 0 5em;font-size:.64rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;padding-top:.4rem}
.dir-pills{display:flex;flex-wrap:wrap;gap:.32rem;min-width:0}
.dir-pills a{display:inline-flex;align-items:center;gap:.3rem;padding:.28rem .62rem;background:#eef1f4;color:#374151;border-radius:999px;font-size:.76rem;font-weight:500;white-space:nowrap}
.dir-pills a:hover{background:#e1e6ea;text-decoration:none}
.dir-pills a.on{background:linear-gradient(135deg,#081832,#173564);color:#fff;font-weight:600}
.b{font-size:.6rem;font-weight:700;padding:.03rem .32rem;border-radius:4px;line-height:1.5}
.b-d{background:rgba(220,38,38,.12);color:#b42318}
.b-w{background:rgba(180,118,20,.15);color:#986a12}
.b-t{background:rgba(37,99,235,.14);color:#1d4ed8}
.dir-pills a.on .b{background:rgba(255,255,255,.22);color:#fff}
.cta{display:flex;align-items:center;gap:.7rem;background:var(--ink);color:#fff;border-radius:10px;padding:1rem 1.3rem;margin:1.1rem 0;font-weight:700}
.cta:hover{text-decoration:none;opacity:.94}
.cta .cta-sub{font-size:.76rem;font-weight:500;color:#cbd5e1;margin-top:.15rem}
.cta .arr{margin-left:auto;font-size:1.1rem}
.live-wrap{display:grid;grid-template-columns:1.3fr 1fr;gap:1rem;margin-top:1rem}
.acard{background:var(--card);border:1px solid var(--green);border-radius:12px;padding:1.2rem 1.3rem;box-shadow:0 0 0 1px var(--green) inset}
.ac-tag{display:inline-block;font-size:.72rem;font-weight:700;padding:.2rem .6rem;border-radius:99px;margin-bottom:.5rem;background:var(--green);color:#fff}
.ac-name{font-size:1.3rem;font-weight:800;letter-spacing:-.02em;color:var(--ink)}
.ac-sub{font-size:.8rem;color:var(--muted);margin:.25rem 0 .9rem}
.ac-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin-bottom:.8rem}
.ac-metrics > div{text-align:center;background:#fafbfc;border:1px solid var(--border);border-radius:8px;padding:.5rem .3rem}
.ac-metrics span{display:block;font-size:.64rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.ac-metrics b{font-size:1.05rem;font-weight:800;color:var(--ink)}
.ac-link{font-size:.82rem;font-weight:600;color:var(--green)}
.acard-note{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.3rem}
.acn-title{font-size:.78rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:.6rem}
.acard-note ul{list-style:none;font-size:.84rem;line-height:1.9}
.acard-note li{padding-left:.9rem;position:relative}
.acard-note li::before{content:'·';position:absolute;left:0;color:var(--grey);font-weight:700}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.5rem;margin-bottom:1rem;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.86rem}
th,td{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}
th{background:#fafbfc;font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
tbody tr:hover td{background:#f6f8fb}
.tag{display:inline-block;padding:.13rem .5rem;border-radius:4px;font-size:.7rem;font-weight:600;white-space:nowrap;background:#f3f4f6;color:#475569;border:1px solid var(--border)}
.tag-best{background:var(--green-bg);color:#166534;border:1px solid var(--green-border)}
.tag-fail{background:#fef2f2;color:#991b1b;border:1px solid #fecaca}
.tag-bh{background:#f3f4f6;color:#6b7280;border:1px solid var(--border)}
.link-card{display:flex;align-items:center;gap:.75rem;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem;color:var(--ink)}
.link-card:hover{border-color:var(--ink);text-decoration:none}
.link-card .lc-name{font-weight:700;font-size:1rem}.link-card .lc-sub{font-size:.78rem;color:var(--muted)}.link-card .lc-arrow{margin-left:auto;color:var(--ink);font-weight:700}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem;margin-bottom:1rem}
.chart-card h3{font-size:.92rem;font-weight:600;color:var(--ink);margin-bottom:.4rem}
.chart-sub{font-size:.76rem;color:var(--muted);margin-bottom:.5rem}
.chart-wrap{position:relative;width:100%;height:330px}
.grid2{display:grid;grid-template-columns:3fr 2fr;gap:1rem}
details{background:var(--card);border:1px solid var(--border);border-radius:10px;margin-bottom:.75rem}
details summary{padding:.85rem 1.2rem;font-weight:600;font-size:.9rem;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.5rem;color:var(--ink)}
details summary::before{content:'▸';color:var(--grey);transition:transform .15s}
details[open] summary::before{transform:rotate(90deg)}
details .d-body{padding:0 1.2rem 1.2rem;overflow-x:auto}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:820px){.live-wrap{grid-template-columns:1fr}.grid2{grid-template-columns:1fr}table{font-size:.76rem}th,td{padding:.4rem .45rem}
.dir-row{flex-direction:column;gap:.3rem}.dir-lbl{flex-basis:auto;padding-top:0}}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>量化回測總覽</h1>
  <div class="sub">20 年全週期(2006~,含 2008/2020/2022 三熊)· 真實 yfinance · 起始 $1M · 依市場/資產類別分四類，點 tab 切換</div>
  <div class="tabs">
    <a data-tabkey="us" href="#us" onclick="return showTab('us')">🇺🇸 美股</a>
    <a data-tabkey="tw" href="#tw" onclick="return showTab('tw')">🇹🇼 台股</a>
    <a data-tabkey="multi" href="#multi" onclick="return showTab('multi')">🧩 多資產</a>
    <a data-tabkey="lev" href="#lev" onclick="return showTab('lev')">🔧 槓桿疊加</a>
  </div>
  <div class="methods">
    <span class="m-lbl">方法論（跨類通用）</span>
    <a href="/backtest/criteria/">評估標準</a>
    <a href="/backtest/glossary/">術語對照表</a>
    <a href="/backtest/free_lunch/">分散與免費午餐</a>
  </div>
</div></div>

<div class="container">

<!-- ══════════════ 🇺🇸 美股 ══════════════ -->
<div class="tabpane" data-tab="us">
%US_DIR%

<div class="section">
<h2 class="section-title">現役系統</h2>
<div class="section-sub">實單攻擊位 2026-07-18 起改為 <a href="/long-track-w52-adaptive/">W52 × 自適應波動率 150%</a>；本表 STX50／E3 為其前身（舊實倉・對照）。其餘採用 / 候補列在右側，未上實倉。</div>
<div class="live-wrap">%CARD%</div>
</div>

<div class="section">
<h2 class="section-title">波段系統 · 風險調整排名</h2>
<div class="section-sub">左色帶：<span style="color:var(--green)">綠=採用</span> · 灰=候補/角色可用 · <span style="color:var(--red)">紅=否決</span>。支配性 = 對自然基準的 <a href="/backtest/criteria/">L2 判定</a>。實驗/否決收在下方。<br>(雙動能 GEM 的導覽已歸「多資產」tab；此表仍保留其為對美股 B&amp;H 的參照列。)</div>
<div class="card">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Calmar</th><th>支配性</th><th>狀態</th></tr></thead>
<tbody>%MAIN_ROWS%%BH_ROWS%</tbody></table>
</div>
<details><summary>實驗 / 已否決系統(收合)</summary><div class="d-body">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Calmar</th><th>支配性</th><th>狀態</th></tr></thead>
<tbody>%TAIL_ROWS%</tbody></table></div></details>
</div>

<div class="section">
<h2 class="section-title">研究筆記</h2>
<div class="section-sub">探索性研究頁(分散結構 / 反例 / 文獻複驗),非實倉候選，刻意不列入上方比較表。跨資產 / 全球市場的研究已歸「多資產」tab。</div>
%US_RESEARCH%
</div>

<div class="section">
<h2 class="section-title">淨值與風險</h2>
<div class="grid2">
  <div class="chart-card"><h3>Growth of $1M</h3><div class="chart-sub">年頻 · 對數座標 · 實倉系統 + B&amp;H</div><div class="chart-wrap"><canvas id="chart-nav"></canvas></div></div>
  <div class="chart-card"><h3>Risk vs Return</h3><div class="chart-sub">X=MDD · Y=CAGR · 左上最佳</div><div class="chart-wrap"><canvas id="chart-scatter"></canvas></div></div>
</div>
<div class="card" style="padding:1.1rem">
<h3 style="font-size:.92rem;margin-bottom:.6rem;color:var(--ink)">分期間 CAGR</h3>
<table><thead><tr><th>系統</th><th>全期</th><th>近 15 年</th><th>近 10 年</th><th>近 5 年</th></tr></thead><tbody>%PERIOD_ROWS%</tbody></table>
</div>
</div>

<div class="section">
<h2 class="section-title">明細</h2>
<details><summary>完整比較表(美股全系統 · 8 欄)</summary><div class="d-body">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar</th><th>支配性</th><th>期末</th><th>狀態</th></tr></thead>
<tbody>%FULL_ROWS%</tbody></table></div></details>
<details><summary>逐年報酬表(2006–2026)</summary><div class="d-body">
<table><thead><tr><th>Year</th>%YEARLY_HEAD%</tr></thead><tbody>%YEARLY_ROWS%</tbody></table></div></details>
</div>
</div>

<!-- ══════════════ 🇹🇼 台股 ══════════════ -->
<div class="tabpane" data-tab="tw" style="display:none">
<a class="cta" href="/backtest/tw/">
  <span style="font-size:1.3rem">🇹🇼</span>
  <span>台股總覽<div class="cta-sub">0050+2330 W52×自適應波動率(實單)· 前代 E3 對照 · 0050 四系統 · 含崩盤驗證 · 完整比較表與圖表</div></span>
  <span class="arr">→</span>
</a>
%TW_DIR%
<div class="section">
<div class="section-sub">2330/0050 E3 為<b>舊實倉</b>台股攻擊位(NT$，自 2010，不與美股同尺；實單已改用 W52 × 自適應波動率 150%)。波段 / 選擇權 / 日內三線各自獨立追蹤；完整數字見上方「台股總覽」。</div>
</div>
</div>

<!-- ══════════════ 🧩 多資產 ══════════════ -->
<div class="tabpane" data-tab="multi" style="display:none">
<a class="cta" href="/backtest/multi/">
  <span style="font-size:1.3rem">🧩</span>
  <span>多資產總覽<div class="cta-sub">唐奇安 / Clenow / SG Trend / 跨資產防守 · 資產池不同，僅供組合互補參照</div></span>
  <span class="arr">→</span>
</a>
%MULTI_DIR%
<div class="section">
<h2 class="section-title">研究筆記</h2>
<div class="section-sub">跨資產 / 全球市場的機制與穩健性研究 — 組合層互補缺口與弱基準假象的反例庫。</div>
%MULTI_RESEARCH%
</div>
</div>

<!-- ══════════════ 🔧 槓桿疊加 ══════════════ -->
<div class="tabpane" data-tab="lev" style="display:none">
<a class="cta" href="/backtest/leverage/">
  <span style="font-size:1.3rem">🔧</span>
  <span>槓桿疊加總覽<div class="cta-sub">在現役趨勢引擎上疊加期貨槓桿 / 波動目標 · 換軸互補研究(未採用)</div></span>
  <span class="arr">→</span>
</a>
%LEV_DIR%
<div class="section">
<div class="section-sub">槓桿疊加皆為研究線(非實盤)：擇時家族全否決，換軸 +ZN+GC 的 E3 閘門 overlay 三窗全勝但仍待 L4 決策。完整數字見上方「槓桿疊加總覽」。</div>
</div>
</div>

</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 量化回測總覽 · 真實 yfinance · 生成 %NOW%</div></footer>

<script>
var YEARS=%JS_YEARS%,RET=%JS_RET%,SCATTER=%JS_SCATTER%;
function showTab(t){
  var panes=document.querySelectorAll('.tabpane');
  for(var i=0;i<panes.length;i++){panes[i].style.display=(panes[i].getAttribute('data-tab')===t)?'':'none';}
  var tabs=document.querySelectorAll('.tabs a');
  for(var j=0;j<tabs.length;j++){tabs[j].classList.toggle('on',tabs[j].getAttribute('data-tabkey')===t);}
  if(window.history&&history.replaceState)history.replaceState(null,'','#'+t);
  if(t==='us')window.dispatchEvent(new Event('resize'));
  return false;
}
function toNAV(r){var n=[],v=1;for(var i=0;i<r.length;i++){if(r[i]===null){n.push(null);continue}v*=1+r[i]/100;n.push(v)}return n}
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";Chart.defaults.font.size=11;
new Chart(document.getElementById('chart-nav'),{type:'line',
 data:{labels:YEARS.map(String),datasets:[
  {label:'SMH/QQQ STX50(舊實倉)',data:toNAV(RET.smh),borderColor:'#16a34a',borderWidth:2.4,pointRadius:0,tension:.1},
  {label:'QQQ B&H',data:toNAV(RET.qqq),borderColor:'#94a3b8',borderWidth:1.3,borderDash:[5,3],pointRadius:0,tension:.1},
  {label:'SPY B&H',data:toNAV(RET.spy),borderColor:'#cbd5e1',borderWidth:1.3,borderDash:[5,3],pointRadius:0,tension:.1}
 ]},
 options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
  plugins:{legend:{position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'line',padding:10,font:{size:10}}},
   tooltip:{callbacks:{label:function(c){return c.parsed.y===null?null:c.dataset.label+': $'+c.parsed.y.toFixed(2)+'M'}}}},
  scales:{x:{grid:{color:'rgba(0,0,0,.04)'},ticks:{font:{size:10}}},y:{type:'logarithmic',grid:{color:'rgba(0,0,0,.06)'},ticks:{callback:function(v){return '$'+v+'M'},font:{size:10}}}}}});
new Chart(document.getElementById('chart-scatter'),{type:'scatter',
 data:{datasets:SCATTER.map(function(p){return {label:p.label,data:[{x:p.x,y:p.y}],backgroundColor:p.color,pointRadius:6,pointHoverRadius:8}})},
 options:{responsive:true,maintainAspectRatio:false,
  plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.dataset.label+': MDD '+c.parsed.x+'% / CAGR '+c.parsed.y+'%'}}}},
  scales:{x:{title:{display:true,text:'Max Drawdown (%)'},grid:{color:'rgba(0,0,0,.05)'}},y:{title:{display:true,text:'CAGR (%)'},grid:{color:'rgba(0,0,0,.05)'}}}}});
(function(){var h=(location.hash||'#us').slice(1);if(!/^(us|tw|multi|lev)$/.test(h))h='us';showTab(h);})();
</script>
</body></html>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
