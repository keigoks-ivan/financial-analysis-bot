"""LIVE renderer for /backtest/index.html — decision-first overview (v4, 2026-09-06).

This is the layout that actually builds the live page: _build_index.py's
main() calls render() here and writes docs/backtest/index.html.  Data
(GROUPS/RET/SCATTER/BH_ROWS/PERIOD_CAGR...) still lives in _build_index.py;
its legacy render()/TEMPLATE are DEAD code kept only as data helpers.
SECTIONS is defined in this module (derived from BLOCKS below) and is read
only by _build_index._completeness_check(), which needs every
docs/backtest/*/index.html directory's url to appear in some row.

2026-09-09 — 改回藥丸表，美股／台股／多資產分區
================================================================================
Owner: the 2026-09-06 card-wall redesign (stat chips + search + top3 cards +
scoreboard + accordion directory with auto-extracted one-line verdicts) was
判定「超級混亂」— too many moving parts, and 美股/台股/多資產 got blended
together inside the same accordion themes. Replaced with ONE plain layout:
five blocks (🇺🇸 美股 / 🇹🇼 台股 / 🧩 多資產 / 🏠 房價與所得 / 🌏 總經・跨國), each
its own pill table styled after `_nav_common.make_toggle()`'s sub-nav bar
(label column + wrapped pill row, small red/gold/blue status badges).
Removed: stat cards, search box, top3 cards, scoreboard table, accordion
directory, their JS, `_extract_verdict()` / VERDICT_OVERRIDES / THEMES /
LEGACY_HASH.

2026-09-10 — housing_gdp 獨立分區，全部 50 頁列出
================================================================================
Supersedes the line above: housing_gdp's ~47 country/case pages no longer
stay off this page. New 🏠 房價與所得 block covers all 50
docs/backtest/housing_gdp/ pages (hub + 9 series + 6 主線／假說 pages + 35
country/case pages, one row per region/status). The old 🌏 總經・跨國「房價×GDP」
row (hub + regression.html) is removed — those two links moved into 🏠; 🌏
now carries 國家掃描 only.

Run: python3 _build_index.py   (this module is imported, not run directly)
"""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import _nav_common as navc

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("system", "bt")
OUT = Path(__file__).parent / "index.html"

LIVE_LINE_URL = "/long-track/#live"
LIVE_LINE_TEXT = "實單主系統：QQQ/SMH 與 0050/2330・W52×自適應波動率 cap 1.5 → 系統主控台"


def _conv(links):
    """把 _nav_common 的 (url,label,key,status) 4-tuple 轉成本頁 pill 用的
    (url,text,status,current) 4-tuple，讀而不改 _nav_common.py。"""
    return [(u, lb, st, False) for (u, lb, _k, st) in links]


# ── 五大分區（美股／台股／多資產／房價與所得／總經・跨國）───────────────────
# rows: [ (row_label, row_id_or_None, [ (url, text, status_or_None, is_current), ... ] ), ... ]
BLOCKS = [
    dict(id="us", emoji="🇺🇸", title="美股", rows=[
        ("總覽", None, [
            ("/backtest/", "20 年", None, True),
            ("/backtest/10y/", "10 年", None, False),
            ("/backtest/criteria/", "評估標準", None, False),
            ("/backtest/glossary/", "術語對照表", None, False),
            ("/backtest/ma_sensitivity/", "MA 敏感度", None, False),
            ("/backtest/free_lunch/", "分散與免費午餐", None, False),
        ]),
        ("個別系統", None, [
            ("/backtest/long_track/", "SPY/QQQ 長軌", None, False),
            ("/backtest/long_track_qqq/", "QQQ 長軌純攻", None, False),
            ("/backtest/long_track_ensemble/", "SPY/QQQ 集成", None, False),
            ("/backtest/long_track_smh/", "SMH/QQQ 進攻", None, False),
            ("/backtest/six_state/", "QQQ＋SMH 六狀態", None, False),
            ("/backtest/six_state_v1r1/", "QQQ 六狀態實盤", None, False),
            ("/backtest/gem/", "SPY/ACWX 雙動能", None, False),
            ("/backtest/slope_filter/", "SPY/AGG 斜率", None, False),
            ("/backtest/rsi2_mr/", "SPY/QQQ 均值回歸", None, False),
            ("/backtest/supertrend/", "週線 Supertrend", None, False),
            ("/backtest/minervini/", "Minervini RS+VCP", None, False),
            ("/backtest/mom_volscaling/", "動能·波動縮放", None, False),
            ("/backtest/dual_track_study/", "雙軌分散研究", None, False),
            ("/backtest/vol_targeting/", "波動目標倉位", "研究", False),
            ("/backtest/vol_targeting/adaptive.html", "波動率變體實驗室", "研究", False),
            ("/backtest/dual_track/", "SPY/QQQ 雙軌多空", "否決", False),
            ("/backtest/exit_switch/", "出場法切換", "否決", False),
            ("/backtest/short_system/", "指數做空", "失敗", False),
        ]),
        ("槓桿疊加", None, [
            ("/backtest/leverage/", "槓桿疊加總覽", None, False),
            ("/backtest/leverage_voltarget/", "期貨槓桿疊加", None, False),
            ("/backtest/vol_targeting/leverage.html", "W52×自適應 150% 槓桿", "研究", False),
        ]),
        ("選擇權", None, [
            ("/backtest/cndr/", "Iron Condor", "失敗", False),
            ("/backtest/covered_call/", "Covered Call", "負貢獻", False),
            ("/backtest/put_timing/", "SPY/QQQ 買 put 避險", "負貢獻", False),
        ]),
        ("實單追蹤", None, [
            ("/long-track-w52-adaptive/", "W52 × 自適應波動率 150%（實單主系統）", "實單", False),
            ("/long-track-qs-vt/", "QQQ+SMH 固定 σ（歸檔）", None, False),
            ("/long-track-qs-vt/adaptive.html", "QQQ+SMH 自適應（歸檔）", None, False),
            ("/long-track-adaptive-vt/", "自適應美台總覽（歸檔）", None, False),
        ]),
        ("實單證據", None, _conv(navc.RESEARCH_OOS_LINKS)),
        ("研究・因子", None, _conv(navc.RESEARCH_FACTOR_LINKS)),
        ("研究・主動式ETF", None, [
            ("/backtest/us_active_etf/", "美股主動式ETF", "研究", False),
        ]),
        ("研究・方法", None, [
            ("/backtest/daily_vs_weekly/", "日/週線", None, False),
            ("/backtest/daily_vs_weekly_deep/", "日/週·深掘", None, False),
            ("/backtest/ma_cross/", "MA 交叉", None, False),
            ("/backtest/ma_deviation/", "MA 乖離", None, False),
            ("/backtest/ma_dynband/", "MA 動態帶", None, False),
            ("/backtest/ma_squeeze/", "MA 擠壓", None, False),
            ("/backtest/smh_vcrash/", "SMH V崩", None, False),
        ]),
    ]),
    dict(id="tw", emoji="🇹🇼", title="台股", rows=[
        ("總覽", None, [
            ("/backtest/tw/", "台股總覽", None, False),
        ]),
        ("波段", None, [
            ("/backtest/tw_0050_compare/", "0050 總覽·台美差異", None, False),
            ("/backtest/tw_0050/", "0050 進攻趨勢", None, False),
            ("/backtest/tw_0050_lt/", "0050 長軌趨勢", None, False),
            ("/backtest/long_track_tw/", "2330/0050 E3 長軌", None, False),
            ("/backtest/vol_targeting/tw.html", "0050+2330 波動率變體", "研究", False),
            ("/backtest/tw_0050_six/", "0050 六狀態機", None, False),
            ("/backtest/tw_0050_dual/", "0050 雙軌多空", "否決", False),
        ]),
        ("選擇權", None, _conv(navc.OPTIONS_LINKS)),
        ("日內", None, _conv(navc.INTRADAY_LINKS)),
        ("可轉債", None, _conv(navc.TW_CB_LINKS)),
        ("實單追蹤", None, [
            ("/long-track-w52-adaptive/", "W52 × 自適應波動率 150%（實單主系統）", "實單", False),
            ("/long-track-tw-vt/", "0050+2330 固定 σ（歸檔）", None, False),
            ("/long-track-tw-vt/adaptive.html", "0050+2330 自適應（歸檔）", None, False),
            ("/long-track-adaptive-vt/", "自適應美台總覽（歸檔）", None, False),
        ]),
        ("研究・主動式ETF", None, [
            ("/backtest/active_etf/", "主動式ETF總結", "專區", False),
            ("/backtest/tw_active_etf/", "台股主動式ETF", "研究", False),
            ("/backtest/tw_mutual_fund/", "台股共同基金", "研究", False),
        ]),
        ("研究・方法", None, [
            ("/backtest/daily_vs_weekly_tw/", "日/週·台股", None, False),
            ("/backtest/tw_vcrash/", "台股 V崩防禦", None, False),
            ("/backtest/tw_crash/", "台股含崩盤驗證", None, False),
        ]),
    ]),
    dict(id="multi", emoji="🧩", title="多資產", rows=[
        ("總覽", None, [
            ("/backtest/multi/", "多資產總覽", None, False),
        ]),
        ("系統", None, [
            ("/backtest/turtle/", "唐奇安突破", None, False),
            ("/backtest/clenow/", "跨資產趨勢", None, False),
            ("/backtest/multiasset_trend/", "SG Trend 複製", None, False),
            ("/backtest/turtle_adopt/", "組合採用 Sleeve", None, False),
            ("/backtest/slope_filter_global/", "全球斜率穩健性", None, False),
            ("/backtest/crossasset_defense/", "跨資產防守", None, False),
            ("/backtest/nonequity/", "非股票 sleeve", "研究", False),
            ("/backtest/reits/", "REITs 三地延伸", "研究", False),
        ]),
        ("研究・方法", None, [
            ("/backtest/daily_vs_weekly_global/", "日/週·全球", None, False),
        ]),
    ]),
    dict(id="housing", emoji="🏠", title="房價與所得・43 經濟體", rows=[
        ("總覽", None, [
            ("/backtest/housing_gdp/", "研究總覽：短中期看信貸，所得只在同一國 3～7 年有用", "研究", False),
        ]),
        ("九個系列", None, [
            ("/backtest/housing_gdp/gdppc_level.html", "人均 GDP 實際金額", "研究", False),
            ("/backtest/housing_gdp/income_affordability.html", "所得與房價所得比", "研究", False),
            ("/backtest/housing_gdp/income_horizon.html", "所得×房價：時間尺度", "研究", False),
            ("/backtest/housing_gdp/catchup.html", "追趕假說", "研究", False),
            ("/backtest/housing_gdp/mortgage_burden.html", "房貸負擔", "研究", False),
            ("/backtest/housing_gdp/house_price_drawdown.html", "房價回撤", "研究", False),
            ("/backtest/housing_gdp/credit_lead.html", "信貸預警", "研究", False),
            ("/backtest/housing_gdp/price_to_rent.html", "房價租金比", "研究", False),
            ("/backtest/housing_gdp/household_debt.html", "家庭負債空間", "研究", False),
        ]),
        ("主線與假說", None, [
            ("/backtest/housing_gdp/regression.html", "主線迴歸", "研究", False),
            ("/backtest/housing_gdp/catchup.html", "追趕假說（重測版）", "研究", False),
            ("/backtest/housing_gdp/catchup_v1.html", "追趕假說（舊版，已凍結）", "研究", False),
            ("/backtest/housing_gdp/divergence.html", "三型分流", "研究", False),
            ("/backtest/housing_gdp/gdp_band.html", "GDP 帶假說", "研究", False),
            ("/backtest/housing_gdp/city_catchup.html", "補漲假說：城市版", "研究", False),
        ]),
        ("個案・已重寫", None, [
            ("/backtest/housing_gdp/taiwan.html", "台灣：貴、熱、還沒跌", "研究", False),
            ("/backtest/housing_gdp/malaysia.html", "馬來西亞：變便宜、去槓桿、原地踏步", "研究", False),
            ("/backtest/housing_gdp/japan.html", "日本：崩過、沒回來、租金比偏貴", "研究", False),
            ("/backtest/housing_gdp/usa.html", "美國（重寫中）", "研究", False),
        ]),
        ("個案・亞太", None, [
            ("/backtest/housing_gdp/australia.html", "澳洲", "研究", False),
            ("/backtest/housing_gdp/china.html", "中國", "研究", False),
            ("/backtest/housing_gdp/hongkong.html", "香港", "研究", False),
            ("/backtest/housing_gdp/india.html", "印度", "研究", False),
            ("/backtest/housing_gdp/indonesia.html", "印尼", "研究", False),
            ("/backtest/housing_gdp/korea.html", "南韓", "研究", False),
            ("/backtest/housing_gdp/newzealand.html", "紐西蘭", "研究", False),
            ("/backtest/housing_gdp/singapore.html", "新加坡", "研究", False),
            ("/backtest/housing_gdp/thailand.html", "泰國", "研究", False),
        ]),
        ("個案・歐洲", None, [
            ("/backtest/housing_gdp/austria.html", "奧地利", "研究", False),
            ("/backtest/housing_gdp/czechia.html", "捷克", "研究", False),
            ("/backtest/housing_gdp/denmark.html", "丹麥", "研究", False),
            ("/backtest/housing_gdp/france.html", "法國", "研究", False),
            ("/backtest/housing_gdp/germany.html", "德國", "研究", False),
            ("/backtest/housing_gdp/greece.html", "希臘", "研究", False),
            ("/backtest/housing_gdp/ireland.html", "愛爾蘭", "研究", False),
            ("/backtest/housing_gdp/italy.html", "義大利", "研究", False),
            ("/backtest/housing_gdp/netherlands.html", "荷蘭", "研究", False),
            ("/backtest/housing_gdp/norway.html", "挪威", "研究", False),
            ("/backtest/housing_gdp/poland.html", "波蘭", "研究", False),
            ("/backtest/housing_gdp/portugal.html", "葡萄牙", "研究", False),
            ("/backtest/housing_gdp/spain.html", "西班牙", "研究", False),
            ("/backtest/housing_gdp/sweden.html", "瑞典", "研究", False),
            ("/backtest/housing_gdp/switzerland.html", "瑞士", "研究", False),
            ("/backtest/housing_gdp/uk.html", "英國", "研究", False),
        ]),
        ("個案・美洲與其他", None, [
            ("/backtest/housing_gdp/brazil.html", "巴西", "研究", False),
            ("/backtest/housing_gdp/canada.html", "加拿大", "研究", False),
            ("/backtest/housing_gdp/israel.html", "以色列", "研究", False),
            ("/backtest/housing_gdp/mexico.html", "墨西哥", "研究", False),
            ("/backtest/housing_gdp/southafrica.html", "南非", "研究", False),
            ("/backtest/housing_gdp/turkey.html", "土耳其", "研究", False),
        ]),
    ]),
    dict(id="macro", emoji="🌏", title="總經・跨國", rows=[
        ("國家掃描", "scan", [
            ("/backtest/country_scan/us.html", "美國：市場結構與九個投資鏡頭", "研究", False),
            ("/backtest/country_scan/taiwan.html", "台灣：市場結構與八個投資鏡頭", "研究", False),
            ("/backtest/country_scan/japan.html", "日本：市場結構與七個投資鏡頭", "研究", False),
            ("/backtest/country_scan/malaysia.html", "馬來西亞：市場結構與四個投資鏡頭", "研究", False),
        ]),
    ]),
]

# _build_index._completeness_check() only needs sec["rows"] = [(label, items), ...]
# with item[0] a url; region/emoji/name/cta/id/sub aren't read by it.
SECTIONS = [dict(rows=[(label, items) for (label, _rid, items) in b["rows"]])
            for b in BLOCKS]

_REJECTED_STATUS = ("否決", "失敗", "負貢獻", "未過")


def _tag_kind(status: str) -> str:
    if status in _REJECTED_STATUS:
        return "red"
    if status == "實單":
        return "gold"
    return "blue"  # 研究/專區/模擬中/觀察/追蹤中 等


def _pill(url: str, text: str, status: str | None, is_current: bool) -> str:
    cls = ["ov-current"] if is_current else []
    tag = f'<span class="ov-tag ov-tag-{_tag_kind(status)}">{status}</span>' if status else ""
    cls_attr = f' class="{" ".join(cls)}"' if cls else ""
    return f'<a href="{url}"{cls_attr}>{text}{tag}</a>'


def _row_html(label: str, row_id: str | None, items: list) -> str:
    pills = "".join(_pill(u, t, s, c) for (u, t, s, c) in items)
    id_attr = f' id="{row_id}"' if row_id else ""
    return (f'<div class="ov-row"{id_attr}><div class="ov-row-lbl">{label}</div>'
            f'<div class="ov-row-pills">{pills}</div></div>')


def _block_html(block: dict) -> str:
    rows = "".join(_row_html(label, row_id, items) for (label, row_id, items) in block["rows"])
    return (f'<section class="ov-block" id="{block["id"]}">'
            f'<h2 class="ov-block-hd">{block["emoji"]} {block["title"]}</h2>'
            f'<div class="ov-table">{rows}</div></section>')


def blocks_html() -> str:
    return "".join(_block_html(b) for b in BLOCKS)


def _total_page_count() -> int:
    return sum(len(items) for b in BLOCKS for (_label, _rid, items) in b["rows"])


def render():
    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%LIVE_LINE_URL%": LIVE_LINE_URL,
        "%LIVE_LINE_TEXT%": LIVE_LINE_TEXT,
        "%BLOCKS%": blocks_html(),
        "%PAGE_COUNT%": str(_total_page_count()),
        "%NOW%": datetime.now().strftime("%Y-%m-%d"),
    }.items():
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>量化回測總覽 | InvestMQuest Research</title>
<link rel="stylesheet" href="/assets/imq-base.css">
<style>
/* imq-base 沒有的少數 token 別名 —— 只補這頁實際會用到的。 */
:root{--red-bg:#fbeceb;--accent-bg:#eef1f6}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--paper);color:var(--body);line-height:1.6;font-size:15px}
a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1100px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.5rem 0 1rem;background:var(--card);border-bottom:1px solid var(--line)}
.page-hdr h1{font-family:var(--serif);font-size:1.6rem;font-weight:700;letter-spacing:-.01em;color:var(--ink)}
.page-hdr .sub{color:var(--sec);font-size:.88rem;margin-top:.3rem;max-width:70ch;line-height:1.7}
.crumb{font-size:.8rem;color:var(--sec);margin-bottom:.35rem}.crumb a{color:var(--sec)}
.ov-live-line{margin-top:1rem;padding:.65rem 1rem;background:var(--card);border:1px solid var(--gold);border-radius:8px;font-size:.86rem}
.ov-live-line a{color:var(--gold-deep);font-weight:700}
/* 分區藥丸表（樣式仿 _nav_common.make_toggle）*/
.ov-block{margin-top:2.2rem}
.ov-block:first-child{margin-top:1.6rem}
.ov-block-hd{font-family:var(--serif);font-size:1.3rem;font-weight:700;color:var(--ink);padding-top:1rem;border-top:2px solid var(--ink);margin-bottom:.7rem}
.ov-table{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--card)}
.ov-row{display:flex;align-items:flex-start;gap:.6rem;padding:.42rem .7rem;border-top:1px solid var(--line)}
.ov-row:first-child{border-top:0}
.ov-row-lbl{flex:0 0 7rem;font-size:.72rem;font-weight:700;color:var(--sec);text-transform:uppercase;letter-spacing:.03em;padding-top:.4rem}
.ov-row-pills{display:flex;flex-wrap:wrap;gap:.35rem;min-width:0}
.ov-row-pills a{display:inline-flex;align-items:center;gap:.3rem;padding:.3rem .7rem;background:var(--line-soft);color:var(--body);border-radius:999px;text-decoration:none;font-weight:500;font-size:.82rem;white-space:nowrap}
.ov-row-pills a:hover{background:var(--line);text-decoration:none}
.ov-row-pills a.ov-current{background:linear-gradient(135deg,#081832,#173564);color:#fff;font-weight:600}
.ov-row-pills a.ov-current:hover{background:linear-gradient(135deg,#081832,#173564)}
.ov-tag{font-size:.62rem;font-weight:700;padding:.03rem .32rem;border-radius:4px;line-height:1.5}
.ov-tag-red{background:var(--red-bg);color:var(--neg)}
.ov-tag-gold{background:var(--gold-bg);color:var(--gold-deep)}
.ov-tag-blue{background:var(--accent-bg);color:var(--accent)}
.ov-row-pills a.ov-current .ov-tag{background:rgba(255,255,255,.22);color:#fff}
footer{background:var(--card);border-top:1px solid var(--line);color:var(--sec);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2.2rem}
@media(max-width:640px){
  .ov-row{flex-direction:column;gap:.3rem}
  .ov-row-lbl{flex-basis:auto;padding-top:0}
}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>量化回測</h1>
  <div class="sub">全部回測頁的目錄，依美股／台股／多資產／房價與所得／總經・跨國五大分區列出，每列一個系統或研究主題。</div>
  <div class="ov-live-line"><a href="%LIVE_LINE_URL%">%LIVE_LINE_TEXT%</a></div>
</div></div>

<div class="container">

%BLOCKS%

</div>
<footer><div class="container">
  &copy; 2026 InvestMQuest Research · 量化回測總覽 · 共 %PAGE_COUNT% 頁 ·
  <a href="/backtest/glossary/">術語對照表</a> · 生成 %NOW%
</div></footer>
</body></html>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
