"""LIVE renderer for /backtest/index.html — full-expand classification directory.

This is the layout that actually builds the live page: _build_index.py's
main() calls render() here and writes docs/backtest/index.html.  Data
(GROUPS/RET/SCATTER/BH_ROWS/PERIOD_CAGR...) still lives in _build_index.py;
its legacy render()/TEMPLATE are DEAD code kept only as data helpers.

2026-08-29 — 全展開分類總表重構（取代 2026-07-17～2026-08-24 的六 tab 設計）
================================================================================
Owner feedback（逐字）:「首頁的設計不好啊 分類的不完全 重新設計整個」「要非常清楚現在有哪些
以及裡面有哪些回測 都要分類好」「要一目了然那種」。

問題診斷：舊版六個 tab＋<details> 收合把內容藏起來，落地只看得到一個 tab（預設 us）；且分類
清單本身漏頁——DIRECTORY["us"]「研究・因子」漏了 profitability／asset_growth／index_inclusion／
insider 四頁（_nav_common.RESEARCH_FACTOR_LINKS 早已補齊 8 頁，但這裡沒同步）；「研究・主動式
ETF」同時掛在 us 與 tw 兩個 tab（active_etf 專區頁重複出現）。

新設計：拿掉 JS tab 過濾與所有分類清單的 <details> 收合，改成單頁全展開——十三個分類 section
由上到下依序排列，捲動就能看到全部。結構：

  1. 頁首（h1 + 方法論工具列）
  2. 狀態總覽（4 張 stat 卡；研究／否決兩個數字改成從 SECTIONS 資料程式即時統計 _count_status()，
     不再寫死；實單 1／合格候補 6 維持寫死＋註解，因為那是人工判定，不是可從 pill 狀態字串推導
     的東西）
  3. 實單主系統卡＋合格候補小卡（%CARD%，內容不動）
  4. 錨點快跳列（13 個分類的 pill，純 <a href="#id">，無 JS 過濾；舊 hash #us/#tw/#multi/#lev/
     #macro/#scan 用一小段 JS 映射到新 section id，讓外部深連結不斷）
  5. 分類總表主體——兩區、十三個 section，全展開，見 SECTIONS 定義
  6. 數據對比區（原本塞在 us tab 尾端的排名表／完整比較表／scatter／逐年/分期 CAGR／
     US_RESEARCH／MULTI_RESEARCH link-card，內容與數字一個不動，搬到目錄之後）

分類修正（對照舊六 tab → 新十三 section）：
  * 個股因子（美股）section 直接從 _nav_common.RESEARCH_FACTOR_LINKS 取全部 8 頁（不再手抄
    4 頁的舊清單）——這是漏頁修復的關鍵。
  * 主動式ETF與基金 section 直接從 _nav_common.RESEARCH_ETF_LINKS 取（active_etf 專區 +
    us_active_etf + tw_active_etf + tw_mutual_fund，共 4 頁），全站只在這裡掛一次；US/TW
    波段 section 不再各自重複列一次。
  * 頻率／均線／崩盤防禦三個研究主題原本分散在 us/tw/multi 三個 tab 各登一次，現併入「方法研究」
    一個 section 的三個子列（直接取 _nav_common 對應的 RESEARCH_FREQ/MA/CRASH_LINKS），避免
    同一頁在多分類重複出現。
  * 台股選擇權／台股日內 section 直接取 _nav_common.OPTIONS_LINKS / INTRADAY_LINKS。
  * 美股波段系統／台股波段／多資產·經典複製／槓桿疊加／總經／國家掃描 沿用舊 DIRECTORY 手抄清單
    （_nav_common 對應清單頁數對不上，例如 MULTI_LINKS 6 頁 vs 這裡系統 9 頁含 gem/nonequity/
    reits），逐字保留。
  * 前瞻追蹤（美/台各 4 條）刻意在美股波段系統與台股波段兩個 section 都各自出現一次——同一顆
    實單系統本來就橫跨美台兩市場，這不是需要去重的重複，_count_status() 用 URL 做 set 去重，
    不會把它算成兩個不同頁面。

完整性守門：_build_index.py main() 新增 _completeness_check()，走訪 docs/backtest/*/index.html
的所有一層目錄，比對是否出現在 SECTIONS 的某個 url 裡；白名單（tw/multi/leverage/criteria/
glossary，逐項附一行理由）之外沒掛到就印 WARNING。

Run: python3 _build_index.py   (this module is imported, not run directly)
"""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _build_index as idx
import _nav_common as navc

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("system", "bt")
OUT = Path(__file__).parent / "index.html"

# 2026-08-24 視覺改版：換成全站奶油紙×深海軍藍×金 design token（/assets/imq-base.css）。
# 四檔語意色與全站一致：實單=金(GOLD) / 採用·候補=綠(GREEN=--pos) / 實驗·研究=藍(BLUE=--accent)
# / 否決·歸檔=紅(RED=--neg) / 基準=灰(GREY=--sec)。取代原本 --16a34a/--dc2626/--9ca3af 孤立色。
GREEN, RED, GREY = "#15803d", "#b91c1c", "#6b7a92"
BLUE, GOLD = "#0d2244", "#8f6d2c"

# 現役卡片改為「引導卡」（2026-08-24）：不再貼會過期的績效快照與執行層參數（曾寫「10pp 門檻＋
# 5% 取整」，已被 2026-07-22 升格的 20pp/10% 取整＋clamp 150% 取代而變成錯誤陳述）。單一事實
# 來源改為系統主控台 /long-track/#live，本頁只給一句定位＋連結，不再重複任何會漂移的數字。
LIVE_CARD = {
    "tag": "實單主系統",
    "name": "QQQ/SMH · W52 × 自適應波動率 cap 1.5",
    "sub": "實單即時淨值、曝險與執行層參數以系統主控台為準——本頁只做研究排名與分類目錄，不重貼會過期的快照數字。",
    "url": "/long-track/#live",
}


def _conv(links):
    """把 _nav_common 的 (url,label,key,status) 4-tuple 轉成本頁 pill 用的
    (url,text,status,current) 4-tuple，讀而不改 _nav_common.py。"""
    return [(u, lb, st, False) for (u, lb, _k, st) in links]


# ── 十三個分類 section（由上到下即為落地全展開順序）──────────────────────────
# region: "sys"=第一區「系統・可交易」／"research"=第二區「研究・非交易」
# cta: 可選 (url, label, sub) —— 該分類自己的總覽/專區入口頁（既有 .cta 版型，逐字沿用）
# rows: [ (row_label, [ (url, text, status_or_None, is_current[, emph]), ... ] ), ... ]
SECTIONS = [
    # ═══════════════ 第一區：系統・可交易 ═══════════════
    dict(id="us-swing", region="sys", emoji="🇺🇸", name="美股波段系統",
         sub="現役 W52×自適應波動率 150%（原 STX50/E3 降為對照）；其餘依風險調整排名分為"
             "採用／候補／實驗／否決，完整比較表與圖表見下方「數據對比」。",
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

# 舊六 tab hash → 新 section id（讓外部深連結不斷；section id 本身就是錨點，JS 只是保險）
LEGACY_HASH = {
    "us": "us-swing", "tw": "tw-swing", "multi": "multi-classic",
    "lev": "leverage", "macro": "macro", "scan": "scan",
}


def _section_count(sec) -> int:
    return sum(len(items) for _label, items in sec["rows"])


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
                if (status in ("否決", "失敗", "負貢獻", "未過")) or archived:
                    rej_urls.add(url)
                elif status and status != "實單":
                    exp_urls.add(url)
    return len(exp_urls), len(rej_urls)


def _badge(status):
    # 四檔語意色（2026-08-24 統一）：否決/失敗/負貢獻/未過 → 紅；實單 → 金；
    # 其餘（研究/專區/模擬中/觀察/追蹤中/即將，皆屬「實驗·研究」廣義）→ 藍。
    if not status:
        return ""
    if status in ("否決", "失敗", "負貢獻", "未過"):
        kind = "d"
    elif status == "實單":
        kind = "g"
    else:
        kind = "b"
    return f'<span class="b b-{kind}">{status}</span>'


def _pill(url, text, status=None, current=False, emph=False):
    # emph: macro-only "entry page" flag (5th tuple element) — reuses the
    # same navy-gradient look as the current-page ".on" state so the two
    # housing_gdp/ entry pages visually outrank the 14 country case pills
    # without introducing a new color. Other sections' 4-tuples default emph=False.
    classes = []
    if current:
        classes.append("on")
    if emph:
        classes.append("entry")
    cls = f' class="{" ".join(classes)}"' if classes else ""
    return f'<a href="{url}"{cls}>{text}{_badge(status)}</a>'


def _dir_rows_html(rows):
    body = ""
    for label, items in rows:
        pills = "".join(_pill(*p) for p in items)
        body += (f'<div class="dir-row"><div class="dir-lbl">{label}</div>'
                 f'<div class="dir-pills">{pills}</div></div>')
    return f'<div class="dir">{body}</div>'


def render_section(sec) -> str:
    n = _section_count(sec)
    cta_html = ""
    if sec["cta"]:
        url, label, sub = sec["cta"]
        cta_html = (f'<a class="cta" href="{url}"><span style="font-size:1.3rem">{sec["emoji"]}</span>'
                    f'<span>{label}<div class="cta-sub">{sub}</div></span><span class="arr">→</span></a>')
    return (f'<div class="section" id="{sec["id"]}">'
            f'<h2 class="section-title">{sec["emoji"]} {sec["name"]}<span class="sec-n">{n} 頁</span></h2>'
            f'<div class="section-sub">{sec["sub"]}</div>'
            f'{cta_html}{_dir_rows_html(sec["rows"])}</div>')


def anchor_jump() -> str:
    groups = {"sys": "", "research": ""}
    for sec in SECTIONS:
        n = _section_count(sec)
        groups[sec["region"]] += f'<a href="#{sec["id"]}">{sec["emoji"]} {sec["name"]}<span class="aj-n">{n}</span></a>'
    return (f'<div class="anchor-jump">'
            f'<div class="aj-group"><span class="aj-lbl">系統・可交易</span>{groups["sys"]}</div>'
            f'<div class="aj-group"><span class="aj-lbl">研究・非交易</span>{groups["research"]}</div>'
            f'</div>')


def sections_html() -> str:
    out, last_region = "", None
    for sec in SECTIONS:
        if sec["region"] != last_region:
            out += f'<h2 class="region-title">{REGION_TITLE[sec["region"]]}</h2>'
            last_region = sec["region"]
        out += render_section(sec)
    return out


# ── per-tab directory (legacy tab lookup kept for lane()/is_position() below) ──
def lane(title):
    # 檢查順序刻意：「否決」「實驗」先於「採用」判定，因為「🔬 實驗(未採用)」字面含
    # 「採用」子字串（未採用）——若採用判定先跑會誤判成綠色（舊版曾有此 bug，2026-08-24 修正）。
    if "否決" in title:
        return RED
    if "實驗" in title:
        return BLUE
    if "候補" in title or "採用" in title:
        return GREEN
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
    return (f'<tr><td colspan="6" style="background:var(--neutral-bg);border-left:3px solid {lc};'
            f'font-size:.74rem;font-weight:700;color:#475569;text-transform:uppercase;'
            f'letter-spacing:.04em">{title}</td></tr>')


# US research link-cards (verbatim) — only US-scoped notes belong to 美股 data section.
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

# Multi-asset / global research link-cards (verbatim) — 數據對比（多資產）小節用。
MULTI_RESEARCH = r"""<a class="link-card" href="/backtest/reits/" style="border-left:3px solid var(--grey)">
  <span style="font-size:1.3rem">🏢</span>
  <span><span class="lc-name">v4 REITs 三地延伸：美 IYR／日 1343.T／星 CLR.SI</span><br><span class="lc-sub">預註冊決策前研究(凍結 2026-07-24、cap 1.0)· 同引擎移植三地房地產信託 = <b>三地皆非候選</b> · IYR 判準3敗(與美股系統月相關 +0.340>0.3、2022升息年飆 +0.763)、Faber 簡單月線 Calmar 0.262 反勝主列 0.113(引擎移植首次不佔優)· 日/星相關夠低卻打不贏實盤系統(判準4)· 星洲樣本短且自身負報酬、結論標初步 · 同框架放行 GLD/擋下 REITs = 預註冊功能 · 匯率未建模</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/nonequity/" style="border-left:3px solid #d97706">
  <span style="font-size:1.3rem">🥇</span>
  <span><span class="lc-name">非股票 sleeve：商品／美債</span><br><span class="lc-sub">預註冊決策前研究(凍結 2026-07-23、cap 1.0 不上槓桿)· GLD/TLT/IEF/DBC 主列(W52×自適應+A2)四判準全過、與美股系統月相關 &lt;0.3、2022 升息債災主列 MDD −2.8% vs B&amp;H −39.8% · GEM 輪動 MDD −51% 且無 B&amp;H 基準 = 非候選 · DBC 判準4 邊際僅 +0.003(壓線)· 疊加 frictionless 已揭露</span></span>
  <span class="lc-arrow">→</span>
</a>
<a class="link-card" href="/backtest/multiasset_trend/" style="border-left:3px solid var(--grey)">
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
  <a class="ac-link" href="{c['url']}">前往系統主控台 →</a>
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
        f'<tr style="background:var(--neutral-bg);border-left:3px solid {GREY}"><td>{n}</td><td>{c}</td>'
        f'<td style="color:var(--muted)">{m}</td><td>{cl}</td><td>—</td><td>{idx.TAG["bh"]}</td></tr>'
        for n, c, m, s, cl in idx.BH_ROWS)

    period = "".join(
        f'<tr><td style="font-weight:600">{name}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>'
        for name, _color, a, b, c, d in idx.PERIOD_CAGR)

    # 完整比較表 — US groups only (🇹🇼 group has its own 台股波段 section)
    full_rows = ""
    for title, items in idx.GROUPS:
        if not is_position(title):
            continue
        full_rows += idx.group_header(title) + "".join(idx.sys_row(*r) for r in items)
    full_rows += idx.group_header("基準(Buy &amp; Hold)") + "".join(
        f'<tr style="background:var(--neutral-bg)"><td>{n}</td><td>{c}</td><td style="color:var(--muted)">{m}</td>'
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
            return "#9aa7b8"
        if "雙軌" in label or "做空" in label or "回歸" in label:
            return RED
        return GREY
    scatter = [dict(label=l, x=x, y=y, color=scat_color(l)) for l, x, y, _c in idx.SCATTER]

    # 狀態總覽（2026-08-29 改版）：研究／否決兩數字改為即時統計（見 _count_status），
    # 實單=1／合格候補=6 維持人工判定寫死——合格候補＝GROUPS「✓ 採用」+「合格候補」兩組
    # 共 6 個系統，屬人工分類判斷，不是能從 pill 狀態字串機械推導的東西。
    exp_n, rej_n = _count_status()
    status_overview = f"""<div class="stat-row">
  <a class="stat-card stat-live" href="/long-track/#live">
    <div class="stat-n">1</div><div class="stat-k">實單</div>
    <div class="stat-d">套 · 系統主控台 →</div>
  </a>
  <div class="stat-card stat-cand">
    <div class="stat-n">6</div><div class="stat-k">合格候補</div>
    <div class="stat-d">通過 L1 門檻，未上實倉</div>
  </div>
  <div class="stat-card stat-exp">
    <div class="stat-n">{exp_n}</div><div class="stat-k">實驗・研究</div>
    <div class="stat-d">探索性頁面，非實倉候選</div>
  </div>
  <div class="stat-card stat-rej">
    <div class="stat-n">{rej_n}</div><div class="stat-k">否決・歸檔</div>
    <div class="stat-d">已否決或降級為對照</div>
  </div>
</div>"""

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK, "%STATUS_OVERVIEW%": status_overview,
        "%ANCHOR_JUMP%": anchor_jump(), "%SECTIONS%": sections_html(),
        "%CARD%": card, "%MAIN_ROWS%": main_rows, "%TAIL_ROWS%": tail_rows, "%BH_ROWS%": bh,
        "%US_RESEARCH%": US_RESEARCH, "%MULTI_RESEARCH%": MULTI_RESEARCH,
        "%PERIOD_ROWS%": period,
        "%FULL_ROWS%": full_rows, "%YEARLY_HEAD%": yhead, "%YEARLY_ROWS%": yrows,
        "%JS_RET%": json.dumps(idx.RET), "%JS_SCATTER%": json.dumps(scatter),
        "%JS_YEARS%": json.dumps(idx.YEARS), "%JS_LEGACY_HASH%": json.dumps(LEGACY_HASH),
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
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<link rel="stylesheet" href="/assets/imq-base.css">
<style>
/* 2026-08-24 視覺改版：全站奶油紙×深海軍藍×金 design token（/assets/imq-base.css）取代原本
   灰白 generic 配色（--bg:#f7f8fa + 孤立 --green/--red）。以下 :root 只「別名」imq-base 既有
   token（--ink/--body/--sec/--paper/--line/--accent/--gold*/--pos/--neg/--warn），不重定義其值；
   保留 --red/--green/--muted/--bg/--border/--text 等舊名是因為 _build_index.py（GROUPS 資料層，
   不在本次改版範圍）的 Python 內嵌 inline style 仍寫死 var(--red)/var(--green)/var(--muted)，
   別名讓那些既有 inline style 不必逐一修改就能自動吃到新色，數字/文字內容全部不動。四檔語意色：
   實單=金(--gold*) / 採用·候補=綠(--pos 別名 --green) / 實驗·研究=藍(--accent) /
   否決·歸檔=紅(--neg 別名 --red) / 基準=灰(--sec 別名 --grey)。 */
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
.container{max-width:1080px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.5rem 0 1rem;background:var(--card);border-bottom:1px solid var(--border)}
.page-hdr h1{font-family:var(--serif);font-size:1.6rem;font-weight:700;letter-spacing:-.01em;color:var(--ink)}
.page-hdr .sub{color:var(--muted);font-size:.85rem;margin-top:.15rem}
.crumb{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}.crumb a{color:var(--muted)}
.methods{display:flex;align-items:center;flex-wrap:wrap;gap:.5rem;margin-top:.9rem;font-size:.8rem}
.methods .m-lbl{font-size:.66rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
.methods a{padding:.2rem .6rem;background:var(--accent-bg);border:1px solid var(--accent-border);border-radius:999px;color:var(--accent);font-weight:600}
/* 狀態總覽——頁首下方第一屏，四張狀態卡 */
.stat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem;margin-top:1rem}
.stat-card{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--grey);border-radius:10px;padding:.75rem .9rem;color:inherit}
.stat-card .stat-n{font-family:var(--mono);font-size:1.5rem;font-weight:700;color:var(--ink);line-height:1.1}
.stat-card .stat-k{font-size:.78rem;font-weight:700;color:var(--ink);margin-top:.2rem}
.stat-card .stat-d{font-size:.7rem;color:var(--muted);margin-top:.15rem}
.stat-live{border-left-color:var(--gold-deep)}
.stat-live .stat-n,.stat-live .stat-d{color:var(--gold-deep)}
.stat-live:hover{border-color:var(--gold-deep);text-decoration:none;box-shadow:var(--sh-1)}
.stat-cand{border-left-color:var(--green)}
.stat-exp{border-left-color:var(--accent)}
.stat-rej{border-left-color:var(--red)}
/* 錨點快跳列（2026-08-29）——13 個分類 pill，純 anchor，無 JS 過濾 */
.anchor-jump{margin-top:1rem;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.7rem .8rem}
.aj-group{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem}
.aj-group+.aj-group{margin-top:.5rem}
.aj-lbl{flex:0 0 auto;font-size:.66rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;margin-right:.3rem}
.anchor-jump a{display:inline-flex;align-items:center;gap:.28rem;padding:.28rem .62rem;background:var(--neutral-bg);color:var(--text);border-radius:999px;font-size:.76rem;font-weight:600;white-space:nowrap}
.anchor-jump a:hover{background:var(--line);text-decoration:none}
.aj-n{font-size:.68rem;font-weight:700;color:var(--muted)}
.region-title{font-family:var(--serif);font-size:1.3rem;font-weight:700;color:var(--ink);margin:2rem 0 .3rem;padding-top:1.3rem;border-top:2px solid var(--ink)}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.05rem;font-weight:700;color:var(--ink);margin-bottom:.85rem;padding-bottom:.4rem;border-bottom:1px solid var(--border);display:flex;align-items:baseline;gap:.5rem}
.sec-n{font-size:.72rem;font-weight:600;color:var(--muted)}
.section-sub{font-size:.82rem;color:var(--muted);margin:-.45rem 0 .9rem}
.dir{background:var(--card);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin:1.1rem 0}
.dir-row{display:flex;align-items:flex-start;gap:.55rem;padding:.34rem .6rem;border-top:1px solid var(--border)}
.dir-row:first-child{border-top:0}
.dir-lbl{flex:0 0 5em;font-size:.64rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;padding-top:.4rem}
.dir-pills{display:flex;flex-wrap:wrap;gap:.32rem;min-width:0}
.dir-pills a{display:inline-flex;align-items:center;gap:.3rem;padding:.28rem .62rem;background:var(--neutral-bg);color:var(--text);border-radius:999px;font-size:.76rem;font-weight:500;white-space:nowrap}
.dir-pills a:hover{background:var(--line);text-decoration:none}
.dir-pills a.on{background:linear-gradient(135deg,var(--accent-ink),var(--accent));color:#fff;font-weight:600}
.dir-pills a.entry{background:linear-gradient(135deg,var(--accent-ink),var(--accent));color:#fff;font-weight:700}
.dir-pills a.entry:hover{opacity:.92}
.b{font-size:.6rem;font-weight:700;padding:.03rem .32rem;border-radius:4px;line-height:1.5}
.b-d{background:var(--red-bg);color:var(--red)}
.b-b{background:var(--accent-bg);color:var(--accent)}
.b-g{background:var(--gold-bg);color:var(--gold-deep)}
.dir-pills a.on .b,.dir-pills a.entry .b{background:rgba(255,255,255,.22);color:#fff}
.cta{display:flex;align-items:center;gap:.7rem;background:var(--accent);color:#fff;border-radius:10px;padding:1rem 1.3rem;margin:1.1rem 0;font-weight:700}
.cta:hover{text-decoration:none;opacity:.94}
.cta .cta-sub{font-size:.76rem;font-weight:500;color:#cbd5e1;margin-top:.15rem}
.cta .arr{margin-left:auto;font-size:1.1rem}
.live-wrap{display:grid;grid-template-columns:1.3fr 1fr;gap:1rem;margin-top:1rem}
/* 引導卡——實單卡不再貼會過期的數字快照，只給定位＋連結 */
.acard{background:var(--card);border:1px solid var(--gold);border-radius:12px;padding:1.2rem 1.3rem;box-shadow:0 0 0 1px var(--gold) inset;display:flex;flex-direction:column}
.ac-tag{display:inline-block;font-size:.72rem;font-weight:700;padding:.2rem .6rem;border-radius:99px;margin-bottom:.5rem;background:var(--gold-deep);color:#fff;align-self:flex-start}
.ac-name{font-family:var(--serif);font-size:1.25rem;font-weight:700;letter-spacing:-.01em;color:var(--ink)}
.ac-sub{font-size:.84rem;color:var(--sec);margin:.4rem 0 1rem;line-height:1.7}
.ac-link{font-size:.86rem;font-weight:700;color:var(--gold-deep);margin-top:auto}
.acard-note{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.3rem}
.acn-title{font-size:.78rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:.6rem}
.acard-note ul{list-style:none;font-size:.84rem;line-height:1.9}
.acard-note li{padding-left:.9rem;position:relative}
.acard-note li::before{content:'·';position:absolute;left:0;color:var(--grey);font-weight:700}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.5rem;margin-bottom:1rem;overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.86rem}
th,td{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}
th{background:var(--neutral-bg);font-weight:600;font-size:.74rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
tbody tr:hover td{background:#fbf8f1}
.tag{display:inline-block;padding:.13rem .5rem;border-radius:4px;font-size:.7rem;font-weight:600;white-space:nowrap;background:var(--neutral-bg);color:var(--text);border:1px solid var(--border)}
.tag-best{background:var(--green-bg);color:var(--green);border:1px solid var(--green-border)}
.tag-fail{background:var(--red-bg);color:var(--red);border:1px solid var(--red-border)}
.tag-bh{background:var(--neutral-bg);color:var(--muted);border:1px solid var(--border)}
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
footer{background:var(--card);border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:820px){.live-wrap{grid-template-columns:1fr}.grid2{grid-template-columns:1fr}table{font-size:.76rem}th,td{padding:.4rem .45rem}
.dir-row{flex-direction:column;gap:.3rem}.dir-lbl{flex-basis:auto;padding-top:0}
.stat-row{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
%NAV%
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
  <h1>量化回測總覽</h1>
  <div class="sub">全展開分類總表——十三個分類、全部回測頁面，捲動即可看完，不需要點 tab。</div>
  <div class="methods">
    <span class="m-lbl">方法論（跨類通用）</span>
    <a href="/backtest/criteria/">評估標準</a>
    <a href="/backtest/glossary/">術語對照表</a>
    <a href="/backtest/free_lunch/">分散與免費午餐</a>
  </div>
  %STATUS_OVERVIEW%
</div></div>

<div class="container">

<div class="live-wrap">%CARD%</div>

%ANCHOR_JUMP%

%SECTIONS%

<!-- ══════════════ 數據對比 ══════════════ -->
<h2 class="region-title">數據對比</h2>

<div class="section">
<h2 class="section-title">數據對比（美股波段）</h2>
<div class="section-sub">左色帶：<span style="color:var(--green)">綠=採用</span> · 灰=候補/角色可用 · <span style="color:var(--red)">紅=否決</span>。支配性 = 對自然基準的 <a href="/backtest/criteria/">L2 判定</a>。實驗/否決收在下方。<br>(雙動能 GEM 的分類已歸「多資產·經典複製」；此表仍保留其為對美股 B&amp;H 的參照列。)</div>
<div class="card">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Calmar</th><th>支配性</th><th>狀態</th></tr></thead>
<tbody>%MAIN_ROWS%%BH_ROWS%</tbody></table>
</div>
<details><summary>實驗 / 已否決系統(收合)</summary><div class="d-body">
<table><thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Calmar</th><th>支配性</th><th>狀態</th></tr></thead>
<tbody>%TAIL_ROWS%</tbody></table></div></details>
</div>

<div class="section">
<h2 class="section-title">研究筆記（美股波段）</h2>
<div class="section-sub">探索性研究頁(分散結構 / 反例 / 文獻複驗),非實倉候選，刻意不列入上方比較表。跨資產 / 全球市場的研究見下方「數據對比（多資產）」。</div>
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

<div class="section">
<h2 class="section-title">數據對比（多資產）</h2>
<div class="section-sub">跨資產 / 全球市場的機制與穩健性研究 — 組合層互補缺口與弱基準假象的反例庫。資產池不同，僅供組合互補參照，不與上表直接比較。</div>
%MULTI_RESEARCH%
</div>

</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 量化回測總覽 · 真實 yfinance · 生成 %NOW%</div></footer>

<script>
var YEARS=%JS_YEARS%,RET=%JS_RET%,SCATTER=%JS_SCATTER%,LEGACY_HASH=%JS_LEGACY_HASH%;
function toNAV(r){var n=[],v=1;for(var i=0;i<r.length;i++){if(r[i]===null){n.push(null);continue}v*=1+r[i]/100;n.push(v)}return n}
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";Chart.defaults.font.size=11;
new Chart(document.getElementById('chart-nav'),{type:'line',
 data:{labels:YEARS.map(String),datasets:[
  {label:'SMH/QQQ STX50(舊實倉)',data:toNAV(RET.smh),borderColor:'#15803d',borderWidth:2.4,pointRadius:0,tension:.1},
  {label:'QQQ B&H',data:toNAV(RET.qqq),borderColor:'#9aa7b8',borderWidth:1.3,borderDash:[5,3],pointRadius:0,tension:.1},
  {label:'SPY B&H',data:toNAV(RET.spy),borderColor:'#c9bfa0',borderWidth:1.3,borderDash:[5,3],pointRadius:0,tension:.1}
 ]},
 options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
  plugins:{legend:{position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'line',padding:10,font:{size:10}}},
   tooltip:{callbacks:{label:function(c){return c.parsed.y===null?null:c.dataset.label+': $'+c.parsed.y.toFixed(2)+'M'}}}},
  scales:{x:{grid:{color:'rgba(12,21,33,.06)'},ticks:{font:{size:10}}},y:{type:'logarithmic',grid:{color:'rgba(12,21,33,.08)'},ticks:{callback:function(v){return '$'+v+'M'},font:{size:10}}}}}});
new Chart(document.getElementById('chart-scatter'),{type:'scatter',
 data:{datasets:SCATTER.map(function(p){return {label:p.label,data:[{x:p.x,y:p.y}],backgroundColor:p.color,pointRadius:6,pointHoverRadius:8}})},
 options:{responsive:true,maintainAspectRatio:false,
  plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return c.dataset.label+': MDD '+c.parsed.x+'% / CAGR '+c.parsed.y+'%'}}}},
  scales:{x:{title:{display:true,text:'Max Drawdown (%)'},grid:{color:'rgba(12,21,33,.07)'}},y:{title:{display:true,text:'CAGR (%)'},grid:{color:'rgba(12,21,33,.07)'}}}}});
(function(){
  // 舊六 tab hash(#us/#tw/#multi/#lev/#macro/#scan) 相容：映射到新 section id 並捲動過去。
  // 新 13 個 section 的 id 本身就是合法錨點，就算 JS 失敗，瀏覽器原生 #id 跳轉一樣能到位。
  function jump(){
    var h=(location.hash||'').slice(1);
    if(!h)return;
    var target=LEGACY_HASH[h]||h;
    var el=document.getElementById(target);
    if(el)el.scrollIntoView({block:'start'});
  }
  window.addEventListener('load',jump);
  window.addEventListener('hashchange',jump);
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
