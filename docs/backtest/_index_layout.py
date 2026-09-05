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

2026-08-31 — 移除「數據對比」區
================================================================================
Owner 指示：首頁只留「整個回測系列有哪些東西」的分類目錄，上方結構第 6 項數據對比區（排名表／
完整比較表／scatter／逐年·分期 CAGR／US_RESEARCH／MULTI_RESEARCH link-card）整段拿掉，首頁到
第 5 項分類總表為止。連帶清掉只服務該區塊的死碼：本檔局部 lane()/is_position()/slim_row()/
section_header()（非 idx.group_header）/render() 內的 scat_color()、US_RESEARCH／
MULTI_RESEARCH 常數、GREEN/RED/GREY/BLUE/GOLD 色碼常數、`import _build_index as idx`（無其他
引用）、Chart.js CDN 與 chart-nav/chart-scatter 兩張圖、%MAIN_ROWS%/%TAIL_ROWS%/%BH_ROWS%/
%US_RESEARCH%/%MULTI_RESEARCH%/%PERIOD_ROWS%/%FULL_ROWS%/%YEARLY_HEAD%/%YEARLY_ROWS%/
%JS_RET%/%JS_SCATTER%/%JS_YEARS% 等 placeholder 與其填充邏輯。_build_index.py 本身不動——
GROUPS/RET/BH_ROWS/PERIOD_CAGR/YEARLY_COLS/SCATTER/group_header/sys_row/yearly_cell 仍被
_build_10y.py／_build_tw.py／_build_leverage.py／_build_multi.py 等子頁 builder 引用，只是
首頁不再消費。

2026-08-31 — 首頁改多欄卡片牆（masonry card wall）
================================================================================
Owner 從四份 mockup（variant_a/b/c/d）中拍板 A：多欄卡片牆。SECTIONS 資料常數一筆不動，只改
render 邏輯：

  * 十三個分類 section 從整行式 .section/.dir 改成緊湊 .card，桌機 3 欄 CSS columns masonry
    （.masonry{column-count:3}）、平板 2 欄、手機 1 欄，卡片 break-inside:avoid 避免跨欄斷裂；
    兩大區標題（系統・可交易／研究・非交易）維持 masonry 區塊前的 region-title。
  * section sub（分類說明文字）不再渲染——資料留在 SECTIONS，render_section() 不輸出
    section-sub div 了。
  * 錨點快跳列整段拿掉（anchor_jump() 函式與 %ANCHOR_JUMP% placeholder 一併移除）——頁面縮
    到卡片牆後已冗餘；但每個 section 的 id 仍原樣留在對應 .card 上，頁尾 LEGACY_HASH（舊六
    tab hash → 新 section id）的 scrollIntoView script 不動，外部深連結（如 #us-swing／#us）
    仍能捲到正確卡片。
  * 有 CTA 專區入口的三個分類（tw-swing／multi-classic／leverage）原本佔滿版寬的 .cta banner
    改為卡片頂部一顆 .card-cta pill（「{label} →」），入口不丟但不再佔整條卡片高度。
  * _dir_rows_html() 更名 _card_body_html()，輸出從 .dir/.dir-row/.dir-lbl/.dir-pills 改成
    .grp/.grp-lbl/.pills（沿用 mockup 命名並重寫對應 CSS）；卡內仍依 dir-lbl 子群分組（如總經
    卡的 主線/亞洲/英語系/歐陸/新興 照舊），pill 樣式改緊湊版，狀態 badge（.b/.b-d/.b-b/.b-g）
    色語意不變。舊 .section/.section-title/.sec-n/.section-sub/.dir*/.cta*/.anchor-jump CSS，
    以及早已死碼的 .card{overflow-x:auto}（本檔內 0 處引用的表格卡殘留）一併移除，避免跟新
    .card 選擇器衝突。

2026-08-31 — pill 樣式一致化
================================================================================
Owner 看了卡片牆截圖後指示「都要用成一致的」：台股波段／多資產·經典複製／槓桿疊加三張卡的
`.card-cta` 全寬深藍按鈕，與 us-swing 卡「20 年總覽」的 `.on` 深色填滿樣式，跟其他 pill 視覺
不同級。改法：三個 hub 連結在 render_section() 動態併入該卡第一個子群的 pills（帶「專區」小標
沿用既有 badge 體系，SECTIONS 資料不動——cta 併入純屬 render 層邏輯）；`.on` 拉平成一般 pill 底
色＋細邊框＋粗體辨識，不再是深色填滿按鈕。清掉死碼 `.card-cta`/`.card-cta:hover` CSS 與
render_section() 內的 cta_html 分支。

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

NAV_BLOCK = full_nav_block("system", "bt")
OUT = Path(__file__).parent / "index.html"

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
    dict(id="oos-validation", region="research", emoji="🧪", name="跨標的證偽",
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


def _card_body_html(rows):
    body = ""
    for label, items in rows:
        pills = "".join(_pill(*p) for p in items)
        body += (f'<div class="grp"><div class="grp-lbl">{label}</div>'
                 f'<div class="pills">{pills}</div></div>')
    return body


def render_section(sec) -> str:
    """Render one分類 as a compact masonry card. sec['sub'] (section 副標) is
    intentionally not emitted here (2026-08-31) — the data stays in SECTIONS,
    the card wall just doesn't render it.

    sec['cta'] (hub 專區入口，2026-08-31 起不再是全寬 .card-cta 按鈕) is spliced
    into the first row group as an ordinary leading pill tagged with a "專區"
    status badge — SECTIONS itself is not mutated, this is render-layer only."""
    n = _section_count(sec)
    rows = sec["rows"]
    if sec["cta"]:
        url, label, _sub = sec["cta"]
        hub_pill = (url, label, "專區", False)
        first_label, first_items = rows[0]
        rows = [(first_label, (hub_pill,) + tuple(first_items))] + list(rows[1:])
    return (f'<div class="card" id="{sec["id"]}">'
            f'<h3>{sec["emoji"]} {sec["name"]}<span class="n">{n} 頁</span></h3>'
            f'{_card_body_html(rows)}</div>')


def sections_html() -> str:
    out, last_region = "", None
    for sec in SECTIONS:
        if sec["region"] != last_region:
            if last_region is not None:
                out += "</div>"
            out += f'<h2 class="region-title">{REGION_TITLE[sec["region"]]}</h2><div class="masonry">'
            last_region = sec["region"]
        out += render_section(sec)
    out += "</div>"
    return out


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
        "%SECTIONS%": sections_html(),
        "%CARD%": card,
        "%JS_LEGACY_HASH%": json.dumps(LEGACY_HASH),
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
.region-title{font-family:var(--serif);font-size:1.3rem;font-weight:700;color:var(--ink);margin:2rem 0 .3rem;padding-top:1.3rem;border-top:2px solid var(--ink)}
/* 多欄卡片牆（2026-08-31）——CSS columns masonry：桌機 3 欄／平板 2 欄／手機 1 欄 */
.masonry{column-count:3;column-gap:1rem}
@media(max-width:1100px){.masonry{column-count:2}}
@media(max-width:680px){.masonry{column-count:1}}
.card{break-inside:avoid;background:var(--card);border:1px solid var(--border);border-radius:10px;box-shadow:var(--sh-1);padding:.9rem 1rem;margin:0 0 1rem}
.card h3{font-size:.94rem;font-weight:700;color:var(--ink);display:flex;align-items:baseline;gap:.4rem;padding-bottom:.45rem;border-bottom:1px solid var(--border);margin-bottom:.55rem}
.card h3 .n{margin-left:auto;font-size:.66rem;font-weight:600;color:var(--muted);font-family:var(--mono)}
.grp{margin-bottom:.5rem}
.grp:last-child{margin-bottom:0}
.grp-lbl{font-size:.6rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:.28rem}
.pills{display:flex;flex-wrap:wrap;gap:.26rem}
.pills a{display:inline-flex;align-items:center;gap:.24rem;padding:.18rem .48rem;background:var(--neutral-bg);color:var(--text);border-radius:999px;font-size:.68rem;font-weight:500;white-space:nowrap;line-height:1.4}
.pills a:hover{background:var(--line);text-decoration:none}
.pills a.on{background:var(--neutral-bg);color:var(--text);font-weight:700;border:1px solid var(--accent)}
.pills a.entry{background:linear-gradient(135deg,var(--accent-ink),var(--accent));color:#fff;font-weight:700}
.pills a.entry:hover{opacity:.92}
.b{font-size:.6rem;font-weight:700;padding:.03rem .32rem;border-radius:4px;line-height:1.5}
.b-d{background:var(--red-bg);color:var(--red)}
.b-b{background:var(--accent-bg);color:var(--accent)}
.b-g{background:var(--gold-bg);color:var(--gold-deep)}
.pills a.entry .b{background:rgba(255,255,255,.22);color:#fff}
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

%SECTIONS%

</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 量化回測總覽 · 真實 yfinance · 生成 %NOW%</div></footer>

<script>
var LEGACY_HASH=%JS_LEGACY_HASH%;
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
