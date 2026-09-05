"""LIVE renderer for /backtest/index.html — decision-first overview (v4, 2026-09-06).

This is the layout that actually builds the live page: _build_index.py's
main() calls render() here and writes docs/backtest/index.html.  Data
(GROUPS/RET/SCATTER/BH_ROWS/PERIOD_CAGR...) still lives in _build_index.py;
its legacy render()/TEMPLATE are DEAD code kept only as data helpers.
SECTIONS (13 分類清單，完整性守門用) is defined in this module and unchanged
by this redesign — only how it's *rendered* changed.

2026-09-06 — 目錄頁重設計（取代 2026-08-29～2026-08-31 的全展開卡片牆）
================================================================================
Owner-approved plan（見對話紀錄）。舊版問題：13 張卡片牆一次全展開，找「現在該看
哪個」要靠肉眼掃 13 張卡；證據總覽入口埋在卡片深處；無篩選/搜尋。

新結構（由上到下）：
  A. 頁首 — 標題 + 一句話定位 + 四格狀態統計改成可點篩選 chips + 即時搜尋框
     （純前端 JS，零依賴，過濾下面的系統記分表與研究目錄兩個清單）。
  B. 「先看這三個」— 三張等寬卡：實單主系統(→系統主控台) / 證據總覽(→
     live_system_evidence + 9 個子證據 pill) / 方法論(評估標準/術語/分散)。
  C. 系統記分表 — 單一表格，只收「實單」與「合格候補」（GROUPS[0]+GROUPS[1]，
     人工判定 6+1=7 個系統，同舊版狀態統計的判定依據不變），欄位：系統/市場/
     狀態徽章/一句結論/連結；一句結論來自 VERDICT_OVERRIDES 或抽取器。
  D. 研究目錄 — 手風琴 <details>，13 個原分類重分組為 7 個主題（不遺漏任何
     連結，原分類名稱保留為子標題），第一個主題預設展開。每列改成「標題 [狀態
     徽章] — 一句結論」的 row（非 pill）。
  E. 頁尾 — 生成戳記 + 頁數 + 術語對照表連結。

一句結論抽取器 `_extract_verdict()`：讀對應 docs/backtest/<dir>/index.html，
優先 <meta name="description">，其次抓 class/id 含 hero/verdict/conclusion/
lede/summary 的區塊文字，再退而求其次抓第一個 <h1> 之後的第一個 <p>；抓不到
或太短(<12 字)或像 HTML/JS 殘渣就留空。VERDICT_OVERRIDES 只人工覆寫 11 項證據
頁與 7 個實單/候補系統（讀原頁面 hero/meta 得出，未杜撰）。

SECTIONS 的 13 個分類、每個分類內的子群標籤、pill 版狀態徽章色語意（.b/.b-d/
.b-b/.b-g）、完整性守門 (`_build_index._completeness_check`) 均原樣保留 —
本次改版只動「呈現層」。舊 masonry 卡片牆 render 邏輯
(render_section/_card_body_html/_pill/sections_html/featured_evidence_html/
REGION_TITLE) 與其死碼一併移除。

Run: python3 _build_index.py   (this module is imported, not run directly)
"""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _nav_common as navc

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

# late-safe: _index_layout is only ever imported from inside
# _build_index.main() (after GROUPS etc. are already defined at module
# load time), so this import finds an already-populated sys.modules entry
# instead of re-running _build_index.py from the top.
import _build_index as bidx

NAV_BLOCK = full_nav_block("system", "bt")
OUT = Path(__file__).parent / "index.html"
BASE_DIR = Path(__file__).parent

# 現役卡片改為「引導卡」（2026-08-24）：不再貼會過期的績效快照與執行層參數。
# 一句結論取自 /long-track/ 系統主控台頁 .sys-one 原文（未杜撰）。
LIVE_CARD = {
    "tag": "實單主系統",
    "name": "QQQ/SMH · W52 × 自適應波動率 cap 1.5",
    "sub": "兩市場各 70% 指數部＝W52 週線閘門 × 自適應波動率 × cap 1.5 ＋ A2 執行層。"
           "即時淨值、曝險與執行層參數以系統主控台為準。",
    "url": "/long-track/#live",
}


def _conv(links):
    """把 _nav_common 的 (url,label,key,status) 4-tuple 轉成本頁 pill 用的
    (url,text,status,current) 4-tuple，讀而不改 _nav_common.py。"""
    return [(u, lb, st, False) for (u, lb, _k, st) in links]


# ── 十三個分類 section（規類資料本身不變，見 2026-08-29 設計註記）──────────────
# region: "sys"=第一區「系統・可交易」／"research"=第二區「研究・非交易」
# cta: 可選 (url, label, sub) —— 該分類自己的總覽/專區入口頁（既有 .cta 版型，逐字沿用）
# rows: [ (row_label, [ (url, text, status_or_None, is_current[, emph]), ... ] ), ... ]
SECTIONS = [
    # ═══════════════ 第一區：系統・可交易 ═══════════════
    dict(id="us-swing", region="sys", emoji="🇺🇸", name="美股波段系統",
         sub="現役 W52×自適應波動率 150%（原 STX50/E3 降為對照）；其餘依風險調整排名分為"
             "採用／候補／實驗／否決。",
         cta=None,
         rows=[
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
            ("前瞻追蹤", [
                ("/long-track-w52-adaptive/", "W52 × 自適應波動率 150%（實單主系統）", "實單", False),
                ("/long-track-qs-vt/", "QQQ+SMH 固定 σ（歸檔）", None, False),
                ("/long-track-qs-vt/adaptive.html", "QQQ+SMH 自適應（歸檔）", None, False),
                ("/long-track-adaptive-vt/", "自適應美台總覽（歸檔）", None, False),
            ]),
         ]),
    dict(id="us-options", region="sys", emoji="🇺🇸", name="美股選擇權",
         sub="Iron Condor／Covered Call／買 put 避險三個選擇權研究，結果全部失敗或負貢獻。",
         cta=None,
         rows=[
            ("選擇權研究", [
                ("/backtest/cndr/", "Iron Condor", "失敗", False),
                ("/backtest/covered_call/", "Covered Call", "負貢獻", False),
                ("/backtest/put_timing/", "SPY/QQQ 買 put 避險", "負貢獻", False),
            ]),
         ]),
    dict(id="tw-swing", region="sys", emoji="🇹🇼", name="台股波段",
         sub="0050+2330 現役 W52×自適應波動率（實單）；前代 E3 對照；0050 四系統含崩盤驗證。",
         cta=("/backtest/tw/", "台股總覽",
              "0050+2330 W52×自適應波動率(實單)· 前代 E3 對照 · 0050 四系統 · 含崩盤驗證 · 完整比較表與圖表"),
         rows=[
            ("波段", [
                ("/backtest/tw_0050_compare/", "0050 總覽·台美差異", None, False),
                ("/backtest/tw_0050/", "0050 進攻趨勢", None, False),
                ("/backtest/tw_0050_lt/", "0050 長軌趨勢", None, False),
                ("/backtest/long_track_tw/", "2330/0050 E3 長軌", None, False),
                ("/backtest/vol_targeting/tw.html", "0050+2330 波動率變體", "研究", False),
                ("/backtest/tw_0050_six/", "0050 六狀態機", None, False),
                ("/backtest/tw_0050_dual/", "0050 雙軌多空", "否決", False),
            ]),
            ("前瞻追蹤", [
                ("/long-track-w52-adaptive/", "W52 × 自適應波動率 150%（實單主系統）", "實單", False),
                ("/long-track-tw-vt/", "0050+2330 固定 σ（歸檔）", None, False),
                ("/long-track-tw-vt/adaptive.html", "0050+2330 自適應（歸檔）", None, False),
                ("/long-track-adaptive-vt/", "自適應美台總覽（歸檔）", None, False),
            ]),
         ]),
    dict(id="tw-options", region="sys", emoji="🇹🇼", name="台股選擇權",
         sub="台指選擇權賣方／雙賣／避險策略群，共用 TAIEX/TWVIX/TXO 資料層與 Black-76 引擎。",
         cta=None,
         rows=[("選擇權", _conv(navc.OPTIONS_LINKS))]),
    dict(id="tw-intraday", region="sys", emoji="🇹🇼", name="台股日內",
         sub="台指期與個股期日內訊號普查，四條線目前皆未通過門檻或已否決。",
         cta=None,
         rows=[("日內", _conv(navc.INTRADAY_LINKS))]),
    dict(id="multi-classic", region="sys", emoji="🧩", name="多資產·經典複製",
         sub="唐奇安突破／Clenow／SG Trend／跨資產防守等經典系統複製，資產池與現役系統不同，"
             "僅供組合互補參照。",
         cta=("/backtest/multi/", "多資產總覽",
              "唐奇安 / Clenow / SG Trend / 跨資產防守 · 資產池不同，僅供組合互補參照"),
         rows=[
            ("系統", [
                ("/backtest/turtle/", "唐奇安突破", None, False),
                ("/backtest/clenow/", "跨資產趨勢", None, False),
                ("/backtest/multiasset_trend/", "SG Trend 複製", None, False),
                ("/backtest/turtle_adopt/", "組合採用 Sleeve", None, False),
                ("/backtest/slope_filter_global/", "全球斜率穩健性", None, False),
                ("/backtest/crossasset_defense/", "跨資產防守", None, False),
                ("/backtest/gem/", "SPY/ACWX 雙動能", None, False),
                ("/backtest/nonequity/", "非股票 sleeve", "研究", False),
                ("/backtest/reits/", "REITs 三地延伸", "研究", False),
            ]),
         ]),
    dict(id="leverage", region="sys", emoji="🔧", name="槓桿疊加",
         sub="在現役趨勢引擎上疊加期貨槓桿／波動目標，屬換軸互補研究，尚未採用。",
         cta=("/backtest/leverage/", "槓桿疊加總覽",
              "在現役趨勢引擎上疊加期貨槓桿 / 波動目標 · 換軸互補研究(未採用)"),
         rows=[
            ("系統", [
                ("/backtest/leverage_voltarget/", "期貨槓桿疊加", None, False),
                ("/backtest/vol_targeting/leverage.html", "W52×自適應 150% 槓桿", "研究", False),
            ]),
         ]),
    # ═══════════════ 第二區：研究・非交易 ═══════════════
    dict(id="factor", region="research", emoji="🧬", name="個股因子（美股）",
         sub="S&P500+NDX100 point-in-time SEC EDGAR 個股層級因子研究——獲利能力／資產成長／"
             "指數納入／內部人買賣等八個題目，皆非可交易系統。",
         cta=None,
         rows=[("研究", _conv(navc.RESEARCH_FACTOR_LINKS))]),
    dict(id="oos-validation", region="research", emoji="🧪", name="實單系統證據（明細）",
         sub="用已上線規則對域外標的做跨標的證偽，只報聚合過尺率與信賴區間，不挑單一標的講故事。",
         cta=None,
         rows=[("研究", _conv(navc.RESEARCH_OOS_LINKS))]),
    dict(id="active-fund", region="research", emoji="📊", name="主動式ETF與基金",
         sub="台美主動式 ETF 與共同基金能否創造 alpha 的因子分析總結。",
         cta=None,
         rows=[("研究", _conv(navc.RESEARCH_ETF_LINKS))]),
    dict(id="tw-cb", region="research", emoji="💵", name="台股可轉債",
         sub="台股可轉債折價／賣回保底／收斂等策略研究專區。",
         cta=None,
         rows=[("研究", _conv(navc.TW_CB_LINKS))]),
    dict(id="method", region="research", emoji="📐", name="方法研究",
         sub="日/週頻率、均線進場方法、V 崩防禦等跨系統機制研究——答的是「這個機制有沒有 edge」，"
             "不是「這個系統能不能上實單」。",
         cta=None,
         rows=[
            ("頻率", _conv(navc.RESEARCH_FREQ_LINKS)),
            ("均線", _conv(navc.RESEARCH_MA_LINKS)),
            ("崩盤防禦", _conv(navc.RESEARCH_CRASH_LINKS)),
         ]),
    dict(id="macro", region="research", emoji="🌏", name="總經・房價×GDP",
         sub="本類非可交易系統（無 CAGR／MDD／Sharpe），是跨國總經機制研究。主線問題：人均所得"
             "成長能否解釋房價走勢——因子矩陣做跨國比較、補漲假說檢驗所得與房價的領先落後關係；"
             "下方個案頁依地區分組，逐一拆解各國房價史的高點、崩盤與復甦路徑。",
         cta=None,
         rows=[
            ("研究・主線", [
                ("/backtest/housing_gdp/", "人均 GDP 與房價（42 國因子矩陣）", "研究", False, True),
                ("/backtest/housing_gdp/catchup.html", "補漲假說：所得領先、房價落後", "研究", False, True),
                ("/backtest/housing_gdp/city_catchup.html", "補漲假說：換成城市層級，訊號還在嗎？", "研究", False, True),
                ("/backtest/housing_gdp/gdp_band.html", "GDP 帶假說：3,000→10,000 美元最快？", "研究", False, True),
            ]),
            ("個案・亞洲", [
                ("/backtest/housing_gdp/taiwan.html", "台灣：二十五年房價史", "研究", False),
                ("/backtest/housing_gdp/japan.html", "日本：七十年房價史", "研究", False),
                ("/backtest/housing_gdp/korea.html", "南韓：與日本同年見頂", "研究", False),
                ("/backtest/housing_gdp/hongkong.html", "香港：撤辣之後仍在跌", "研究", False),
                ("/backtest/housing_gdp/malaysia.html", "馬來西亞：所得跑贏房價", "研究", False),
                ("/backtest/housing_gdp/thailand.html", "泰國：失落的十三年", "研究", False),
                ("/backtest/housing_gdp/china.html", "中國：官方指數換過口徑，分級城市差很大", "研究", False),
                ("/backtest/housing_gdp/singapore.html", "新加坡：政府自己蓋，所得贏了房價", "研究", False),
                ("/backtest/housing_gdp/indonesia.html", "印尼：22 年跌勢未收復", "研究", False),
                ("/backtest/housing_gdp/india.html", "印度：跨過 3,000 美元門檻，房價卻沒漲", "研究", False),
            ]),
            ("個案・英語系", [
                ("/backtest/housing_gdp/usa.html", "美國：崩盤與收復", "研究", False),
                ("/backtest/housing_gdp/canada.html", "加拿大：從未崩過的市場正在崩", "研究", False),
                ("/backtest/housing_gdp/uk.html", "英國：最深崩盤是通膨", "研究", False),
                ("/backtest/housing_gdp/ireland.html", "愛爾蘭：42 國最深崩盤", "研究", False),
                ("/backtest/housing_gdp/australia.html", "澳洲：從未真正崩過", "研究", False),
                ("/backtest/housing_gdp/newzealand.html", "紐西蘭：政策工具全試過一輪", "研究", False),
            ]),
            ("個案・歐陸", [
                ("/backtest/housing_gdp/germany.html", "德國：沒有泡沫的 25 年凍結", "研究", False),
                ("/backtest/housing_gdp/spain.html", "西班牙：人口驅動的兩次泡沫", "研究", False),
                ("/backtest/housing_gdp/greece.html", "希臘：失落的十年，19 年未收復", "研究", False),
                ("/backtest/housing_gdp/italy.html", "義大利：18 年未收復 2007 高點", "研究", False),
                ("/backtest/housing_gdp/portugal.html", "葡萄牙：谷底比紓困期早 4 年", "研究", False),
                ("/backtest/housing_gdp/netherlands.html", "荷蘭：供給彈性倒數第 2", "研究", False),
                ("/backtest/housing_gdp/denmark.html", "丹麥：房貸債券吸收利率衝擊", "研究", False),
                ("/backtest/housing_gdp/norway.html", "挪威：石油而非人口外移", "研究", False),
                ("/backtest/housing_gdp/austria.html", "奧地利：實質利率係數 37 國最正", "研究", False),
                ("/backtest/housing_gdp/poland.html", "波蘭：負實質利率卻刻意降息", "研究", False),
                ("/backtest/housing_gdp/france.html", "法國：所得解釋不了房價的異數", "研究", False),
                ("/backtest/housing_gdp/switzerland.html", "瑞士：升息循環中紋風不動的房價", "研究", False),
                ("/backtest/housing_gdp/sweden.html", "瑞典：銀行危機與負債爭議兩張臉", "研究", False),
                ("/backtest/housing_gdp/czechia.html", "捷克：看不見的修正，不磁吸資金的首都", "研究", False),
            ]),
            ("個案・其他新興市場", [
                ("/backtest/housing_gdp/turkey.html", "土耳其：通膨 80% 仍降息", "研究", False),
                ("/backtest/housing_gdp/brazil.html", "巴西：同期相關拉滿，長期方向消失", "研究", False),
                ("/backtest/housing_gdp/southafrica.html", "南非：被遺忘的 1983 年崩盤", "研究", False),
                ("/backtest/housing_gdp/israel.html", "以色列：房市抗議運動打輸的那一場", "研究", False),
                ("/backtest/housing_gdp/mexico.html", "墨西哥：升息打不下去的 20 年", "研究", False),
            ]),
         ]),
    dict(id="scan", region="research", emoji="🔍", name="國家掃描",
         sub="對單一國家股市的第一輪系統性掃描：複利機器篩選×出口群深查×估值現況。掃描是研究記錄"
             "不是選股名單，個股裁決一律走 DD。",
         cta=None,
         rows=[
            ("市場初掃", [
                ("/backtest/country_scan/us.html", "美國：市場結構與九個投資鏡頭", "研究", False),
                ("/backtest/country_scan/taiwan.html", "台灣：市場結構與八個投資鏡頭", "研究", False),
                ("/backtest/country_scan/japan.html", "日本：市場結構與七個投資鏡頭", "研究", False),
                ("/backtest/country_scan/malaysia.html", "馬來西亞：市場結構與四個投資鏡頭", "研究", False),
            ]),
         ]),
]

REGION_TITLE = {"sys": "系統・可交易", "research": "研究・非交易"}

# 舊六 tab hash → 新 section id（部分沿用自 2026-08-29 masonry 版；section id 本身
# 仍以 <h4 id="…"> 的形式保留在手風琴子標題上，深連結一樣能命中並展開該手風琴）。
LEGACY_HASH = {
    "us": "us-swing", "tw": "tw-swing", "multi": "multi-classic",
    "lev": "leverage", "macro": "macro", "scan": "scan",
}

# ── 7 大研究目錄主題（regroup，不遺漏任何連結；原 13 分類名稱保留為子標題）────
THEMES = [
    ("趨勢與波段", ["us-swing", "tw-swing", "multi-classic", "leverage"]),
    ("選擇權與衍生品", ["us-options", "tw-options", "tw-intraday", "tw-cb"]),
    ("因子與基金", ["factor", "active-fund"]),
    ("方法研究", ["method"]),
    ("總經・房價×GDP", ["macro"]),
    ("國家掃描", ["scan"]),
    ("實單系統證據（明細）", ["oos-validation"]),
]

_SECTION_BY_ID = {sec["id"]: sec for sec in SECTIONS}

# ── 一句結論人工覆寫：只覆寫 11 個證據頁（RESEARCH_OOS_LINKS 全部 10 條，含 hub）
# 與 7 個實單/候補系統（GROUPS[0] 1 個 + GROUPS[1] 5 個 + 真正實單 1 個）。文字
# 逐字取自各頁 <meta name="description"> 或 hero 區塊，僅做截字，未杜撰新內容。
VERDICT_OVERRIDES = {
    # 實單主系統的系統主控台入口（系統記分表用；文字取自 /long-track/ .sys-one）
    "/long-track/#live": "兩市場各 70% 指數部＝W52 週線閘門 × 自適應波動率 × cap 1.5 ＋ A2 執行層。",
    "/long-track-w52-adaptive/": "兩市場各 70% 指數部＝W52 週線閘門 × 自適應波動率 × cap 1.5 ＋ A2 執行層。",
    # 7 個實單/候補系統（GROUPS[0]+GROUPS[1]，文字取自各頁 hero-top）
    "/backtest/long_track_smh/": "半倉掛上 ATR 通道出場閘門，塌陷時比均線更快離場，且打敗同 CAGR 的現金稀釋對照。",
    "/backtest/long_track_ensemble/": "集成治得了盤整病，治不了 gap risk——MDD 換了形狀，系統擁有者接受這個交換。",
    "/backtest/slope_filter/": "用嚴格進場換更小回撤：CAGR 比 Faber 略低，Sharpe／Calmar／MDD 全面更好。",
    "/backtest/long_track/": "保險費付在盤整、保障兌現在崩盤——修正 warmup 後 CAGR +9.75%。",
    "/backtest/long_track_qqq/": "回撤保護全來自 W52 出場線——修正 warmup 後 CAGR +10.83%、MDD -25.37%。",
    "/backtest/gem/": "發表後(2014~2026)優勢消失——全樣本風險調整優勢整包來自 2008 單一事件。",
    # 11 個證據頁（RESEARCH_OOS_LINKS，文字取自各頁 <meta name="description">）
    "/backtest/live_system_evidence/": "十一項證據總覽：跨標的證偽、保險價格、兩種洗牌測試、慢熊 base rate、"
                                       "美台合併帳戶等，一頁看完整體證據強度。",
    "/backtest/w52_adaptive_oos/": "實單規則鏈丟到規則選擇時從未看過的約 30 檔標的做前瞻證偽：過尺率 20.6%"
                                    "（95% CI [10.3%, 36.8%]），判定：kill 訊號。",
    "/backtest/insurance_premium/": "把三種下檔保險（均線閘門、跨資產分散、倉位稀釋）放在同一把尺上，"
                                     "量出每一種的保費與理賠。",
    "/backtest/adopted_bootstrap/": "用價格路徑與報酬流兩種 bootstrap，量出系統勝過買進持有的統計強度 p_B，"
                                     "回答「這個裁決有多少是運氣」。",
    "/backtest/regime_bootstrap/": "用真實牛熊段（非固定長度 block）當重抽單位，回答固定 block bootstrap "
                                    "是否對趨勢規則不公平。",
    "/backtest/combined_account/": "把美股與台股兩套實單合成一個帳戶，量合併後的 CAGR／MDD／Calmar 與"
                                    "回撤同步性、匯率分解。",
    "/backtest/slow_bear_base_rate/": "量化慢熊多久來一次：合併池每十年約 0.87 次。判定：慢熊約十年一遇，"
                                       "保費要用十年攤。",
    "/backtest/slow_bear_onset/": "116 個起點事件的可分辨性檢定，判定：有跡象但樣本不夠，只記錄。",
    "/backtest/f_portfolio/": "F＝0.5×均線閘門實單A＋0.5×跨資產分散D1，問「疊兩種保險」是結構性優勢還是"
                               "歷史巧合。",
    "/backtest/cross_sectional_trend/": "把「每腿各自看均線」改成「持有相對最強的幾腿」，判定：形式不是關鍵。",
}

# _extract_verdict() 抓取用關鍵字（class 或 id 命中其一即視為候選區塊）
_VERDICT_KEYWORDS = ("hero", "verdict", "conclusion", "lede", "summary")
_verdict_cache: dict[str, tuple[str, str]] = {}
_verdict_stats = {"auto": 0, "override": 0, "blank": 0}


def _clean_text(raw: str) -> str:
    t = re.sub(r"<[^>]+>", " ", raw)
    t = t.replace("&amp;", "&").replace("&nbsp;", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _trim(text: str) -> str:
    cut = text.find("。")
    if cut != -1 and cut < 70:
        return text[: cut + 1]
    if len(text) > 70:
        return text[:70] + "…"
    return text


def _extract_verdict(url: str) -> tuple[str, str]:
    """回傳 (一句結論, 來源) — 來源 ∈ {override, auto, blank}。逐 url 記憶化。"""
    if url in _verdict_cache:
        return _verdict_cache[url]

    override = VERDICT_OVERRIDES.get(url)
    if override:
        result = (override, "override")
        _verdict_cache[url] = result
        _verdict_stats["override"] += 1
        return result

    m = re.match(r"^/backtest/([^/#]+)/", url)
    path = BASE_DIR / m.group(1) / "index.html" if m else None
    html = None
    if path and path.exists():
        try:
            html = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            html = None

    text = None
    if html:
        md = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
            html, re.I)
        if md:
            text = _clean_text(md.group(1))
        if not text:
            kw = "|".join(_VERDICT_KEYWORDS)
            km = re.search(rf'(?:class|id)="[^"]*(?:{kw})[^"]*"[^>]*>', html, re.I)
            if km:
                chunk = html[km.end(): km.end() + 800]
                candidate = _clean_text(chunk)
                if len(candidate) >= 12:
                    text = candidate
        if not text:
            h1m = re.search(r"<h1[^>]*>.*?</h1>", html, re.I | re.S)
            if h1m:
                pm = re.search(r"<p[^>]*>(.*?)</p>",
                                html[h1m.end(): h1m.end() + 2000], re.I | re.S)
                if pm:
                    text = _clean_text(pm.group(1))

    if not text or len(text) < 12 or re.match(r"^[{<]|^function\b|^var\b", text):
        result = ("", "blank")
        _verdict_stats["blank"] += 1
    else:
        result = (_trim(text), "auto")
        _verdict_stats["auto"] += 1
    _verdict_cache[url] = result
    return result


# ── 資料層分類：實單 / 合格候補 兩組系統的 url 集合（人工判定，來自 GROUPS）───
_CANDIDATE_ROWS = bidx.GROUPS[0][1] + bidx.GROUPS[1][1]  # ✓ 採用(1) + 合格候補(5)
_CANDIDATE_URLS = {row[1] for row in _CANDIDATE_ROWS}
_LIVE_URLS = {"/long-track/#live", "/long-track-w52-adaptive/"}
_REJECTED_STATUS = ("否決", "失敗", "負貢獻", "未過")


def _row_cat(url: str, status: str | None, text: str) -> str:
    """篩選 chip 用的分類：live / candidate / research / rejected / ''（無狀態）。"""
    if url in _LIVE_URLS or status == "實單":
        return "live"
    if url in _CANDIDATE_URLS:
        return "candidate"
    if (status in _REJECTED_STATUS) or ("（歸檔）" in text):
        return "rejected"
    if status:
        return "research"
    return ""


def _badge(status):
    # 四檔語意色（2026-08-24 統一）：否決/失敗/負貢獻/未過 → 紅；實單 → 金；
    # 其餘（研究/專區/模擬中/觀察/追蹤中/即將，皆屬「實驗·研究」廣義）→ 藍。
    if not status:
        return ""
    if status in _REJECTED_STATUS:
        kind = "d"
    elif status == "實單":
        kind = "g"
    else:
        kind = "b"
    return f'<span class="b b-{kind}">{status}</span>'


# ══════════════════════ B. 先看這三個 ══════════════════════
def top3_html() -> str:
    evidence_pills = "".join(
        f'<a href="{u}" data-cat="research">{lb}</a>'
        for (u, lb, _k, _st) in navc.RESEARCH_OOS_LINKS if _k != "evidence_hub")
    return f"""<div class="top3">
  <a class="t3-card t3-live" href="{LIVE_CARD['url']}" data-cat="live">
    <div class="t3-tag">① 實單主系統</div>
    <div class="t3-name">QQQ/SMH 與 0050/2330・W52×自適應波動率 cap 1.5</div>
    <div class="t3-sub">{LIVE_CARD['sub']}</div>
    <span class="t3-arrow">前往系統主控台 →</span>
  </a>
  <div class="t3-card">
    <div class="t3-tag">② 實單系統的證據總覽</div>
    <div class="t3-name"><a href="/backtest/live_system_evidence/">先看這頁</a></div>
    <div class="t3-sub">十一項預註冊測試白話串講：規則普不普遍、保費多少、慢熊多久來一次、
      贏了多少是運氣、美台是不是同一注。</div>
    <div class="t3-pills">{evidence_pills}</div>
  </div>
  <div class="t3-card">
    <div class="t3-tag">③ 方法論</div>
    <div class="t3-name">跨分類通用</div>
    <div class="t3-sub">判定框架、名詞定義與「為什麼分散/免費午餐不是萬能」三頁。</div>
    <div class="t3-pills">
      <a href="/backtest/criteria/">評估標準</a>
      <a href="/backtest/glossary/">術語對照表</a>
      <a href="/backtest/free_lunch/">分散與免費午餐</a>
    </div>
  </div>
</div>"""


# ══════════════════════ C. 系統記分表 ══════════════════════
def scoreboard_html() -> str:
    rows = []
    live_verdict, _ = _extract_verdict(LIVE_CARD["url"])
    rows.append(("QQQ/SMH · 0050/2330 · W52×自適應波動率 cap 1.5", LIVE_CARD["url"],
                 "美股+台股", "實單", live_verdict))
    for (name, url, _sub, *_rest) in _CANDIDATE_ROWS:
        verdict, _src = _extract_verdict(url)
        market = "台股" if ("2330" in name or "0050" in name) else "美股"
        rows.append((name, url, market, "候補", verdict))

    # sort: 實單 first, then 候補 (stable — preserves GROUPS order within each)
    rows.sort(key=lambda r: 0 if r[3] == "實單" else 1)

    body = ""
    for name, url, market, status, verdict in rows:
        cat = "live" if status == "實單" else "candidate"
        badge = _badge(status)
        body += (f'<tr data-cat="{cat}"><td><a href="{url}">{name}</a></td>'
                  f'<td>{market}</td><td>{badge}</td>'
                  f'<td class="sb-verdict">{verdict}</td>'
                  f'<td><a href="{url}">看詳頁 →</a></td></tr>')

    return f"""<div class="section-block">
  <h2 class="section-h">系統記分表</h2>
  <div class="section-note">已上實單或通過 L1 門檻的候補系統——{len(rows)} 個。</div>
  <div class="sb-wrap"><table class="scoreboard">
    <thead><tr><th>系統</th><th>市場</th><th>狀態</th><th>一句結論</th><th></th></tr></thead>
    <tbody>{body}</tbody>
  </table></div>
  <div class="sb-footnote">數字見 <a href="/backtest/criteria/">評估標準</a> 頁與
    <a href="/long-track/#live">系統主控台</a>。</div>
</div>"""


# ══════════════════════ D. 研究目錄（手風琴） ══════════════════════
def _theme_row_html(item) -> str:
    url, text, status = item[0], item[1], item[2]
    verdict, _src = _extract_verdict(url)
    cat = _row_cat(url, status, text)
    badge = _badge(status)
    verdict_html = f'<span class="d-verdict">{verdict}</span>' if verdict else ""
    cat_attr = f' data-cat="{cat}"' if cat else ' data-cat=""'
    return (f'<div class="d-row"{cat_attr}>'
            f'<a href="{url}">{text}</a>{badge}{verdict_html}</div>')


def _theme_html(theme_name: str, sec_ids: list[str], is_first: bool) -> str:
    body = ""
    page_count = 0
    tally: dict[str, int] = {}
    for sid in sec_ids:
        sec = _SECTION_BY_ID[sid]
        cta_row = ""
        if sec["cta"]:
            url, label, _sub = sec["cta"]
            cta_row = _theme_row_html((url, f"{label}（專區入口）", "專區"))
        body += f'<h4 class="d-subhead" id="{sid}">{sec["emoji"]} {sec["name"]}</h4>{cta_row}'
        for label, items in sec["rows"]:
            if label:
                body += f'<div class="d-grouplbl">{label}</div>'
            for item in items:
                page_count += 1
                status = item[2] or "—"
                tally[status] = tally.get(status, 0) + 1
                body += _theme_row_html(item)
    tally_str = " · ".join(f"{k}×{v}" for k, v in
                            sorted(tally.items(), key=lambda kv: -kv[1]))
    open_attr = " open" if is_first else ""
    return f"""<details class="d-theme"{open_attr}>
  <summary>{theme_name}<span class="d-n">{page_count} 頁</span><span class="d-tally">{tally_str}</span></summary>
  <div class="d-body">{body}</div>
</details>"""


def directory_html() -> str:
    body = "".join(_theme_html(name, ids, i == 0) for i, (name, ids) in enumerate(THEMES))
    return f"""<div class="section-block">
  <h2 class="section-h">研究目錄</h2>
  <div class="section-note">十三個分類重分組成七個主題，展開看完整清單；點標題可收合。</div>
  {body}
</div>"""


def _total_page_count() -> int:
    return sum(len(items) for sec in SECTIONS for _label, items in sec["rows"])


def _count_status():
    """研究／否決兩個總覽數字：從 SECTIONS 即時統計不重複頁面（用 URL 當 key 去重——
    前瞻追蹤同一顆實單系統會同時出現在美股波段系統與台股波段兩個 section，不應重複計數）。
    否決·歸檔 = 狀態∈{否決,失敗,負貢獻,未過} 或連結文字含「（歸檔）」；
    實驗·研究 = 其餘任何非空狀態（研究/專區/模擬中/觀察/追蹤中/即將），但排除「實單」本身。"""
    exp_urls, rej_urls = set(), set()
    for sec in SECTIONS:
        for _label, items in sec["rows"]:
            for item in items:
                url, text, status = item[0], item[1], item[2]
                archived = "（歸檔）" in text
                if (status in _REJECTED_STATUS) or archived:
                    rej_urls.add(url)
                elif status and status != "實單":
                    exp_urls.add(url)
    return len(exp_urls), len(rej_urls)


def render():
    exp_n, rej_n = _count_status()
    n_candidate = len(_CANDIDATE_ROWS)

    header_stats = f"""<div class="stat-row">
  <div class="stat-card stat-live" data-filter="live">
    <div class="stat-n">1</div><div class="stat-k">實單</div>
    <div class="stat-d">套 · <a href="/long-track/#live" onclick="event.stopPropagation()">系統主控台 →</a></div>
  </div>
  <div class="stat-card stat-cand" data-filter="candidate">
    <div class="stat-n">{n_candidate}</div><div class="stat-k">合格候補</div>
    <div class="stat-d">通過 L1 門檻，未上實倉</div>
  </div>
  <div class="stat-card stat-exp" data-filter="research">
    <div class="stat-n">{exp_n}</div><div class="stat-k">實驗・研究</div>
    <div class="stat-d">探索性頁面，非實倉候選</div>
  </div>
  <div class="stat-card stat-rej" data-filter="rejected">
    <div class="stat-n">{rej_n}</div><div class="stat-k">否決・歸檔</div>
    <div class="stat-d">已否決或降級為對照</div>
  </div>
</div>
<div class="filter-bar">
  <input id="bt-search" type="search" placeholder="搜尋系統名稱或一句結論…" aria-label="搜尋">
  <button id="bt-filter-reset" type="button">全部</button>
</div>"""

    # verdict extraction 統計（放在 build console，非頁面內容）——覆蓋 top3/scoreboard/
    # directory 三處全部呼叫過 _extract_verdict 之後才印，統計以 url 記憶化去重。
    top3 = top3_html()
    scoreboard = scoreboard_html()
    directory = directory_html()
    print(f"Verdict extraction — override: {_verdict_stats['override']}, "
          f"auto: {_verdict_stats['auto']}, blank: {_verdict_stats['blank']} "
          f"(unique urls: {len(_verdict_cache)})")

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%HEADER_STATS%": header_stats,
        "%TOP3%": top3,
        "%SCOREBOARD%": scoreboard,
        "%DIRECTORY%": directory,
        "%JS_LEGACY_HASH%": json.dumps(LEGACY_HASH),
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
/* 別名 imq-base token，數字/文字內容全部不動（沿用 2026-08-24 版規則）。 */
:root{
  --text:var(--body); --muted:var(--sec); --border:var(--line); --bg:var(--paper);
  --green:var(--pos); --green-bg:#eafaef; --green-border:#bfe0c8;
  --red:var(--neg); --red-bg:#fbeceb; --red-border:#f1c9c6;
  --grey:var(--sec);
  --accent-bg:#eef1f6; --accent-border:#ccd3de;
  --gold-border:#e8d6a8;
  --warn-bg:#fbf3df; --warn-border:#e8d6a8;
  --neutral-bg:var(--line-soft);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;font-size:15px}
a{color:var(--ink);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1100px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.5rem 0 1rem;background:var(--card);border-bottom:1px solid var(--border)}
.page-hdr h1{font-family:var(--serif);font-size:1.6rem;font-weight:700;letter-spacing:-.01em;color:var(--ink)}
.page-hdr .sub{color:var(--muted);font-size:.88rem;margin-top:.3rem;max-width:70ch;line-height:1.7}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}.crumb a{color:var(--muted)}
/* 狀態總覽——現在是可點篩選 chip */
.stat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem;margin-top:1rem}
.stat-card{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--grey);border-radius:10px;padding:.75rem .9rem;color:inherit;cursor:pointer;user-select:none;transition:box-shadow .12s,border-color .12s}
.stat-card:hover{box-shadow:var(--sh-1)}
.stat-card.chip-active{border-color:var(--ink);box-shadow:0 0 0 2px var(--ink) inset}
.stat-card .stat-n{font-family:var(--mono);font-size:1.5rem;font-weight:700;color:var(--ink);line-height:1.1}
.stat-card .stat-k{font-size:.78rem;font-weight:700;color:var(--ink);margin-top:.2rem}
.stat-card .stat-d{font-size:.7rem;color:var(--muted);margin-top:.15rem}
.stat-card .stat-d a{color:inherit;font-weight:600}
.stat-live{border-left-color:var(--gold-deep)}
.stat-live .stat-n{color:var(--gold-deep)}
.stat-cand{border-left-color:var(--green)}
.stat-exp{border-left-color:var(--accent)}
.stat-rej{border-left-color:var(--red)}
.filter-bar{display:flex;gap:.5rem;margin-top:.7rem}
.filter-bar #bt-search{flex:1;padding:.5rem .8rem;border:1px solid var(--border);border-radius:8px;font-size:.85rem;background:var(--card);color:var(--text)}
.filter-bar #bt-search:focus{outline:2px solid var(--accent);outline-offset:1px}
.filter-bar button{padding:.5rem 1rem;border:1px solid var(--border);border-radius:8px;background:var(--card);color:var(--muted);font-size:.8rem;font-weight:600;cursor:pointer}
.filter-bar button:hover{color:var(--ink);border-color:var(--ink)}
/* B. 先看這三個 */
.top3{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1.4rem}
.t3-card{display:block;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.2rem;color:inherit;display:flex;flex-direction:column}
.t3-live{border:1px solid var(--gold);box-shadow:0 0 0 1px var(--gold) inset}
.t3-tag{font-size:.7rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:.4rem}
.t3-live .t3-tag{color:var(--gold-deep)}
.t3-name{font-family:var(--serif);font-size:1.02rem;font-weight:700;color:var(--ink);margin-bottom:.4rem}
.t3-sub{font-size:.82rem;color:var(--sec);line-height:1.65;flex:1}
.t3-arrow{margin-top:.7rem;font-size:.84rem;font-weight:700;color:var(--gold-deep)}
.t3-pills{display:flex;flex-wrap:wrap;gap:.28rem;margin-top:.7rem}
.t3-pills a{display:inline-flex;padding:.16rem .5rem;background:var(--neutral-bg);color:var(--text);border-radius:999px;font-size:.68rem;font-weight:500;white-space:nowrap}
.t3-pills a:hover{background:var(--line);text-decoration:none}
@media(max-width:820px){.top3{grid-template-columns:1fr}}
/* C. 系統記分表 */
.section-block{margin-top:2.2rem}
.section-h{font-family:var(--serif);font-size:1.25rem;font-weight:700;color:var(--ink);padding-top:1rem;border-top:2px solid var(--ink)}
.section-note{font-size:.8rem;color:var(--muted);margin:.35rem 0 .9rem}
.sb-wrap{overflow-x:auto;background:var(--card);border:1px solid var(--border);border-radius:10px}
table.scoreboard{width:100%;border-collapse:collapse;font-size:.86rem}
table.scoreboard th,table.scoreboard td{text-align:left;padding:.6rem .8rem;border-bottom:1px solid var(--border);vertical-align:top}
table.scoreboard th{background:var(--neutral-bg);font-weight:600;font-size:.72rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}
table.scoreboard tbody tr:last-child td{border-bottom:0}
table.scoreboard tbody tr:hover td{background:#fbf8f1}
.sb-verdict{color:var(--sec);font-size:.82rem;line-height:1.55}
.sb-footnote{font-size:.76rem;color:var(--muted);margin-top:.6rem}
/* D. 研究目錄（手風琴） */
details.d-theme{background:var(--card);border:1px solid var(--border);border-radius:10px;margin-bottom:.7rem}
details.d-theme summary{padding:.85rem 1.1rem;font-weight:700;font-size:.95rem;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.6rem;color:var(--ink);font-family:var(--serif)}
details.d-theme summary::before{content:'▸';color:var(--grey);transition:transform .15s;font-family:sans-serif}
details.d-theme[open] summary::before{transform:rotate(90deg)}
.d-n{font-size:.66rem;font-weight:600;color:var(--muted);font-family:var(--mono)}
.d-tally{font-size:.68rem;font-weight:500;color:var(--muted);margin-left:auto;text-align:right}
.d-body{padding:.2rem 1.1rem 1rem}
.d-subhead{font-size:.82rem;font-weight:700;color:var(--ink);margin:1rem 0 .3rem;padding-top:.7rem;border-top:1px solid var(--border)}
.d-subhead:first-child{margin-top:.2rem;padding-top:0;border-top:0}
.d-grouplbl{font-size:.62rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin:.5rem 0 .15rem}
.d-row{display:flex;align-items:baseline;flex-wrap:wrap;gap:.4rem;padding:.28rem 0;font-size:.84rem;border-bottom:1px dotted var(--border)}
.d-row:last-child{border-bottom:0}
.d-row a{font-weight:600;color:var(--ink)}
.d-verdict{color:var(--sec);font-size:.78rem;flex-basis:100%;line-height:1.5}
@media(min-width:720px){.d-verdict{flex-basis:auto;margin-left:.3rem}}
.b{font-size:.6rem;font-weight:700;padding:.03rem .32rem;border-radius:4px;line-height:1.5}
.b-d{background:var(--red-bg);color:var(--red)}
.b-b{background:var(--accent-bg);color:var(--accent)}
.b-g{background:var(--gold-bg);color:var(--gold-deep)}
footer{background:var(--card);border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){
  .stat-row{grid-template-columns:repeat(2,1fr)}
  table.scoreboard{font-size:.76rem}
  table.scoreboard th,table.scoreboard td{padding:.45rem .5rem}
  table.scoreboard thead{display:none}
  table.scoreboard tbody tr{display:block;padding:.6rem .5rem;border-bottom:1px solid var(--border)}
  table.scoreboard tbody td{display:block;border-bottom:0;padding:.15rem 0}
}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>量化回測</h1>
  <div class="sub">全部回測頁的目錄：先看實單系統與它的證據，再看系統記分表，最後是研究目錄。</div>
  %HEADER_STATS%
</div></div>

<div class="container">

%TOP3%

%SCOREBOARD%

%DIRECTORY%

</div>
<footer><div class="container">
  &copy; 2026 InvestMQuest Research · 量化回測總覽 · 共 %PAGE_COUNT% 頁 ·
  <a href="/backtest/glossary/">術語對照表</a> · 生成 %NOW%
</div></footer>

<script>
var LEGACY_HASH=%JS_LEGACY_HASH%;
(function(){
  function jump(){
    var h=(location.hash||'').slice(1);
    if(!h)return;
    var target=LEGACY_HASH[h]||h;
    var el=document.getElementById(target);
    if(el){
      var det=el.closest('details');
      if(det)det.open=true;
      el.scrollIntoView({block:'start'});
    }
  }
  window.addEventListener('load',jump);
  window.addEventListener('hashchange',jump);
})();
(function(){
  // 篩選 chips + 即時搜尋，純前端、零依賴。
  var chips=Array.prototype.slice.call(document.querySelectorAll('.stat-card[data-filter]'));
  var resetBtn=document.getElementById('bt-filter-reset');
  var searchBox=document.getElementById('bt-search');
  var rows=Array.prototype.slice.call(document.querySelectorAll('[data-cat]'));
  var themes=Array.prototype.slice.call(document.querySelectorAll('details.d-theme'));
  var active=null;

  function apply(){
    var q=(searchBox.value||'').trim().toLowerCase();
    rows.forEach(function(el){
      var cat=el.getAttribute('data-cat');
      var catOk=!active||cat===active;
      var textOk=!q||el.textContent.toLowerCase().indexOf(q)!==-1;
      el.style.display=(catOk&&textOk)?'':'none';
    });
    themes.forEach(function(det){
      var anyVisible=false;
      det.querySelectorAll('[data-cat]').forEach(function(el){
        if(el.style.display!=='none')anyVisible=true;
      });
      det.style.display=anyVisible?'':'none';
      if(anyVisible&&(active||q))det.open=true;
    });
    chips.forEach(function(c){
      c.classList.toggle('chip-active',c.getAttribute('data-filter')===active);
    });
  }
  chips.forEach(function(c){
    c.addEventListener('click',function(e){
      if(e.target.tagName==='A')return; // let inner links (系統主控台 →) navigate normally
      var f=c.getAttribute('data-filter');
      active=(active===f)?null:f;
      apply();
    });
  });
  if(resetBtn)resetBtn.addEventListener('click',function(){active=null;searchBox.value='';apply();});
  if(searchBox)searchBox.addEventListener('input',apply);
})();
</script>
</body></html>
"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
