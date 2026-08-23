#!/usr/bin/env python3
"""Canonical site header (imq-nav) — single source of truth + idempotent injector.

The canonical nav is defined here once. Running this script over docs/ will:
  1. strip every known legacy/variant site header (imq-nav-root header blocks,
     dedicated nav <style> blocks, imq-dd toggle <script>s, legacy
     <nav class="imq-nav">, supply-chain <header class="site">, the old
     six-state plain header, the tools/ wordpress header)
  2. re-insert the canonical unit (style + header + script) right after <body>,
     with the active group/item derived from the file's path
  3. for /dd-screener/ pages, append the section sub-nav strip (sibling pages)
     below the site header — mirroring the /backtest/ pill-bar pattern

Idempotent: re-running produces identical output. New pages from any skill or
generator are picked up on the next run (update_dd_index.py calls this).

External generators (v7-backtest, morning-briefing, minervini-quality-backtest)
embed a copy of NAV_STYLE / NAV_HTML / NAV_SCRIPT — when changing the nav here,
re-sync those templates too (see .claude/notes/site-composition.md).

Usage:
    python3 scripts/site_nav.py            # apply to docs/
    python3 scripts/site_nav.py --check    # report variants, change nothing

Change log:
    2026-07-17：系統群 11→8，三波動率追蹤條整併為單一「波動率追蹤家族」入口。
    2026-07-17 晚：voltrack 入口改指現行主系統 W52 × 自適應波動率
        （/long-track-w52-adaptive/），label 簡化為「波動率追蹤」；舊三頁歸檔，
        PREFIX_ACTIVE 映射保留供歸檔頁高亮，並新增 long-track-w52-adaptive/ 映射。
    2026-07-19：復活兩張孤兒頁並掛 nav——(1) 頂層新增「投資流程」(/flow/) 連結，
        置於「使用指南」旁（howto 模式，group key "flow"）；(2) 系統群 tr 之後新增
        「持倉週掃」("pm", "/pm/")＝position-thesis-monitor 週掃報告索引。PREFIX_ACTIVE
        加 pm/ 與 flow/ 映射；pm/index.html 自 SKIP_FILES 移除（改為可注入 nav）。
        v7-backtest/site_nav_snippet.py 同步（build_nav flow_cls＋MENU system pm），
        full_nav_block 輸出對 canonical byte-identical。
    2026-07-23 Phase B：長線追蹤家族重整。系統群移除 ltsmh／lttw／sleeve 三條目，
        新增「追蹤總覽」("lthub", /long-track/)（排 voltrack 之後）；voltrack label
        由「波動率追蹤」改「實單主系統」（url 不變）。PREFIX_ACTIVE：long-track-smh／
        long-track-tw／turtle-sleeve／long-track-gld／long-track/ 全改 (system, lthub)；
        w52-adaptive 家族與三個 vt 頁維持 voltrack。★first-match：泛用 long-track/ 排在
        所有具體 long-track-*/ 之後★。退役 generator（smh/tw/turtle）＋GLD 追蹤頁＋總覽
        builder 的 full_nav_block 呼叫改 lthub；smh/tw cron 停更、加凍結 banner。
        v7-backtest/site_nav_snippet.py 同步、byte-identical 驗證。
    2026-08-20 intel 2.0 Phase C：市場群 13→7 收斂。移除 mon／det／rot／crowd／
        regime／cat 六條目（整併進 /intel/ 分頁殼：儀表＝monitor iframe、變化＝
        detective、週更＝crowding＋regime＋rotation、行事曆＝catalyst）；intel 升
        市場群首位。原頁全保留可直達、刻意不轉址（monitor 被 gauges.html iframe，
        其餘是 intel「完整互動頁」外連目的地）。雷達依持有人 2026-08-19 決定獨立
        保留。PREFIX_ACTIVE 六個舊前綴改 ("market", None)（群高亮、無選單項）。
        外部 repo snippet 同步待各 repo 自己的 commit（見 site-composition.md）。
    2026-08-20 選股入口整頓第二批：選股群收斂＋市場偵探回掛系統群。(1) 選股 ▾
        下拉移除 DD Screener／QGM 美股／QGM 台股／RS+VCP Screener／Momentum-5
        五條目——五者已收進 /cockpit/ 總覽分頁新增的「想法四路（發現層）」純
        連結區塊，不再需要獨立佔頂層下拉席位。移除後 MENU["pick"] 只剩「選股
        主控台」單一目的地，故整組下拉改頂層直連 <a href="/cockpit/">選股</a>
        （比照其他頂層項 2-4 字慣例，捨長版「選股主控台」）；PREFIX_ACTIVE 的
        pick 群映射不變，僅 build_nav() 渲染路徑改為 flat link。(2) 市場偵探
        （/detective/）於 8/20 Phase C 收斂時被移出市場群選單，但 how-to.html
        仍把它列為每日晨檢第一步的四磚之一——現改掛回系統群（"det" 排首位，
        緊接裁決實績／持倉週掃兩個既有監控類條目之前），PREFIX_ACTIVE 的
        detective/ 映射由 ("market", None) 改 ("system", "det")。
    2026-08-20 研究區整併第二階段（nav 瘦身，見 notes/site-internal/root/
        _consolidation_research_20260820.md §7）：研究 ▾ 下拉從 7 項收斂為
        3 項——「個股研究」(thub, /t/)／「產業研究」(id, /id/)／「Tier
        Matrix」(tier, /id/tier_matrix.html)；維持下拉形態，不降頂層直連
        （與同日選股群單一目的地改直連不同——研究群仍有 3 個真實目的地）。
        移除的 4 個舊條目（個股 DD／多股對比／期望落差綜合研判／供應鏈地圖）
        第一階段已收進 /t/ 或 /id/ 分頁，其實體頁面（stub／獨立頁／deep
        report）PREFIX_ACTIVE 映射同步改點到吸收方的 item，不再指向已消失
        的選單鍵：docs/research/（stub）、docs/dd/（個別 DD 報告）、
        docs/dca/、docs/report/、docs/comparisons/（stub＋MS_*.html 報告）、
        docs/research/synthesis/（stub＋{TICKER}_{date}.html 報告）一律改
        ("research","thub")（個股研究是這些「個股研究地圖三種切法」的收斂
        點）；docs/supply-chain/（獨立完整頁＋子地圖）改 ("research","id")
        （供應鏈地圖是 /id/ 的一個分頁，屬產業研究鏡頭）。效果：這些頁面
        瀏覽時「研究」下拉的對應項與群同時高亮，不再退化成純群高亮。
    2026-08-23 系統群 nav 瘦身（見 notes/site-internal/root/
        _consolidation_system_20260823.md）：MENU["system"] 8→4 項，只留
        「系統主控台」(lthub, /long-track/，label 由「追蹤總覽」改名)／
        「量化回測」(bt)／「期貨部位計算機」(tools)／「公開資料」(data)；
        市場偵探(det)／裁決實績(tr)／持倉週掃(pm)／實單主系統(voltrack) 四個
        item 鍵移除。PREFIX_ACTIVE：track-record/、pm/、long-track-w52-adaptive/
        與三個 vt 家族頁改掛 ("system","lthub")；detective/ 不進市場群選單
        （維持不轉址直達頁），改掛 ("market","intel")——比照 crowding/regime/
        rotation 的「同源完整互動頁」判定。順手清掉 2026-08-20 選股群收斂時
        遺留的 dangling PREFIX_ACTIVE 鍵：("pick","dds")／mom5／qus／qtw／scr
        五個已消失的下拉項鍵，統一改 ("pick", None)（群高亮、無選單項，
        與同批市場群六條目的處理方式一致）。build_nav() 不變——系統群仍是 4
        項，維持下拉形態，不觸發選股群式的單項 flat-link 特例。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs"

# ---------------------------------------------------------------- canonical

NAV_STYLE = """<style id="imq-nav-style">
.imq-nav-root{background:linear-gradient(135deg,#081832 0%,#173564 100%);padding:.7rem 20px;font-size:13px;box-shadow:0 1px 3px rgba(0,0,0,.12);position:sticky;top:0;z-index:1000;font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.imq-nav-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.imq-logo{font-weight:700;color:#fff !important;text-decoration:none !important;font-size:15px;letter-spacing:-.02em;flex-shrink:0;background:none !important;padding:0 !important}
.imq-logo:hover{color:#fff !important;text-decoration:none !important}
.imq-logo span{color:#d4b576}
.imq-menu{display:flex;align-items:center;gap:.15rem;flex-wrap:wrap;margin:0;padding:0;list-style:none}
.imq-menu > a,.imq-dd-btn{color:rgba(255,255,255,.7) !important;font-size:.8rem;font-weight:500;padding:.42rem .72rem;border-radius:6px;transition:all .15s;background:none;border:0;font-family:inherit;cursor:pointer;text-decoration:none !important;display:inline-flex;align-items:center;gap:.28rem;line-height:1.2;letter-spacing:0}
.imq-menu > a:hover,.imq-dd-btn:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-menu > a.active,.imq-dd.active > .imq-dd-btn{color:#fff !important;background:rgba(184,146,74,.26);font-weight:600}
.imq-dd{position:relative;display:inline-block}
.imq-dd-menu{display:none;position:absolute;top:100%;left:0;background:#0d2244;border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:.35rem 0;min-width:180px;box-shadow:0 10px 28px rgba(0,0,0,.3);z-index:1001}
.imq-dd:hover .imq-dd-menu,.imq-dd:focus-within .imq-dd-menu,.imq-dd.open .imq-dd-menu{display:block}
.imq-dd-menu a{display:block;padding:.55rem 1rem;color:rgba(255,255,255,.75) !important;font-size:.78rem;text-decoration:none !important;white-space:nowrap;transition:all .12s;font-weight:500}
.imq-dd-menu a:hover{color:#fff !important;background:rgba(184,146,74,.20)}
.imq-dd-menu a.active{color:#fff !important;background:rgba(184,146,74,.26);font-weight:600}
.imq-caret{font-size:.6rem;opacity:.7;margin-top:1px}
.imq-subnav{background:#081832;padding:.45rem 20px;font-family:'Inter','Noto Sans TC',-apple-system,sans-serif}
.imq-subnav-inner{max-width:1140px;margin:0 auto;display:flex;gap:.3rem;flex-wrap:wrap}
.imq-subnav a{color:rgba(255,255,255,.55) !important;font-size:.74rem;font-weight:500;padding:.28rem .6rem;border-radius:5px;text-decoration:none !important}
.imq-subnav a:hover{color:#fff !important;background:rgba(255,255,255,.08)}
.imq-subnav a.active{color:#fff !important;background:rgba(184,146,74,.30);font-weight:600}
@media(max-width:768px){
  .imq-nav-root{padding:.55rem 12px}
  .imq-nav-inner{gap:.4rem}
  .imq-menu{width:100%;justify-content:flex-start;gap:.1rem}
  .imq-menu > a,.imq-dd-btn{font-size:.74rem;padding:.32rem .5rem}
  .imq-dd-menu{position:static;display:none;min-width:auto;box-shadow:none;background:rgba(255,255,255,.04);border:none;padding:.1rem 0 .3rem 1rem;margin:.1rem 0}
  .imq-dd.open .imq-dd-menu{display:block}
}
</style>"""

NAV_SCRIPT = """<script>(function(){document.querySelectorAll('.imq-dd-btn').forEach(function(btn){btn.addEventListener('click',function(e){e.preventDefault();var dd=btn.closest('.imq-dd');document.querySelectorAll('.imq-dd.open').forEach(function(d){if(d!==dd)d.classList.remove('open')});dd.classList.toggle('open')})});document.addEventListener('click',function(e){if(!e.target.closest('.imq-dd'))document.querySelectorAll('.imq-dd.open').forEach(function(d){d.classList.remove('open')})});})();</script>"""

# (group, item, href, label) — groups: home / pick / research / market / system / mm / howto
# 2026-07-07 整站 IA v2（見 notes/site-internal/root/_proposal_site_ia_20260707.md）：
# 三群 catch-all（研究/市場/工具）改為四群意圖式（選股/研究/市場/系統）——
# 選股系統原散在研究+工具兩選單，收斂為單一「選股」群；跨資產三頁（描述器）
# 自研究移入市場；每日簡報已暫停自 nav 移除（/briefing/ 歸檔頁仍可直達）。
MENU = {
    # 2026-07-10 選股主控台整併（見 notes/site-internal/root/_consolidation_stock_console_20260710.md）：
    # 精選榜／流程板機／席位排序（＋原駕駛艙總覽）四頁已收斂進單一 /cockpit/ 四分頁，
    # 故下拉移除 picks／pipe／eng 三個舊條目，只留單一「選股主控台」入口。
    # 舊 URL 皆為活 redirect stub，外部書籤與外部 3 repo 舊 nav 仍可用。
    # 2026-08-20 選股入口整頓第二批：DD Screener／Momentum-5／QGM 美股／QGM 台股／
    # RS+VCP Screener 五條目移除——已收進 /cockpit/ 總覽分頁「想法四路（發現層）」
    # 純連結區塊，發現層職能不需要重複佔頂層下拉席位。移除後本組只剩「選股主控台」
    # 一項，build_nav() 因此不再對 "pick" 呼叫 dd()，改渲染成頂層直連連結；
    # 各頁 PREFIX_ACTIVE 仍映射 ("pick", ...) 供群高亮沿用，不受影響。
    "pick": [
        ("cockpit", "/cockpit/", "選股主控台"),
    ],
    # 2026-08-20 nav 瘦身第二階段（研究區整併第一階段的後續，見
    # notes/site-internal/root/_consolidation_research_20260820.md §7）：
    # 個股 DD／供應鏈地圖／多股對比／期望落差綜合研判四條目已在第一階段收進
    # /t/ 或 /id/ 分頁，故選單只留三個真實頂層目的地；下拉形態不變。
    "research": [
        ("thub", "/t/", "個股研究"),
        ("id", "/id/", "產業研究"),
        ("tier", "/id/tier_matrix.html", "Tier Matrix"),
    ],
    # 2026-08-20 intel 2.0 Phase C：市場群 13→7 收斂——monitor／detective／crowding／
    # regime／rotation（產業輪動）／catalyst 六個監看入口整併進情報監視器分頁殼
    # （儀表＝monitor iframe、變化＝detective、週更＝crowding＋regime＋rotation、
    # 行事曆＝catalyst）。原頁全數保留可直達、刻意「不轉址」：/monitor/ 被
    # /intel/gauges.html iframe，其餘是 intel 各分頁「完整互動頁」連結的目的地
    # （內容比 intel 分頁更全）。資產輪動雷達依持有人 2026-08-19 決定獨立保留。
    # PREFIX_ACTIVE 的六個舊前綴映射改 ("market", None)：頁面仍歸市場群高亮，
    # 但不再對應任何選單項目。
    "market": [
        ("intel", "/intel/", "情報監視器"),  # 2026-08-19 新增；2026-08-20 Phase C 升為市場群首位
        ("brief", "/briefing/", "每日簡報"),  # 2026-08-17 日報恢復（週一至週六 06:15），重新掛回頁首
        ("radar", "/rotation/radar.html", "資產輪動雷達"),
        ("macro", "/macro/", "總經深度報告"),
        ("earn", "/earnings/", "財報分析"),
        ("markets", "/markets.html", "Markets"),
        ("sectors", "/sectors.html", "Sectors"),
        # 2026-07-11 週報已停更，自頁首移除（/weekly/ 頁面保留可直達；
        # PREFIX_ACTIVE 的 weekly/ 映射保留，使其頁面仍歸市場群 active）
    ],
    # 2026-08-23 系統群瘦身（8→4，見 notes/site-internal/root/
    # _consolidation_system_20260823.md）：市場偵探／裁決實績／持倉週掃／實單
    # 主系統四條目移除——四者皆為「監控/裁決」類分頁，語意上收斂進 /long-track/
    # 總覽（該頁已是四分頁系統主控台，見 2026-08-20 Phase 1）。lthub 項標籤由
    # 「追蹤總覽」改「系統主控台」（URL 不變，仍 /long-track/）；市場偵探不落回
    # 市場群選單（維持不轉址、直達頁），改由 PREFIX_ACTIVE 群層映射處理。
    "system": [
        ("lthub", "/long-track/", "系統主控台"),
        ("bt", "/backtest/", "量化回測"),
        ("tools", "/tools/", "期貨部位計算機"),
        ("data", "/data.html", "公開資料"),
    ],
}
GROUP_LABELS = {"pick": "選股", "research": "研究", "market": "市場", "system": "系統"}


def build_nav(group=None, item=None):
    def dd(name):
        links = "\n".join(
            f'          <a href="{href}"{" class=\"active\"" if group == name and item == key else ""}>{label}</a>'
            for key, href, label in MENU[name]
        )
        act = " active" if group == name else ""
        return (
            f'      <div class="imq-dd{act}">\n'
            f'        <button type="button" class="imq-dd-btn">{GROUP_LABELS[name]}<span class="imq-caret">▾</span></button>\n'
            f'        <div class="imq-dd-menu">\n{links}\n        </div>\n'
            f"      </div>"
        )

    home_cls = ' class="active"' if group == "home" else ""
    # 2026-08-20 選股群收斂至單一目的地（/cockpit/）後改頂層直連，不再走 dd()。
    pick_cls = ' class="active"' if group == "pick" else ""
    mm_cls = ' class="active"' if group == "mm" else ""
    flow_cls = ' class="active"' if group == "flow" else ""
    howto_cls = ' class="active"' if group == "howto" else ""
    search_cls = ' class="active"' if group == "search" else ""
    return f"""<header class="imq-nav-root">
  <div class="imq-nav-inner">
    <a class="imq-logo" href="/">InvestMQuest<span>.</span> Research</a>
    <nav class="imq-menu">
      <a href="/"{home_cls}>首頁</a>
{dd("market")}
      <a href="/cockpit/"{pick_cls}>選股</a>
{dd("research")}
      <a href="/mental-models/"{mm_cls}>心智模型</a>
{dd("system")}
      <a href="/flow/"{flow_cls}>投資流程</a>
      <a href="/how-to.html"{howto_cls}>使用指南</a>
      <a href="/search.html"{search_cls}>搜尋</a>
    </nav>
  </div>
</header>"""


def full_nav_block(group=None, item=None, subnav=""):
    return NAV_STYLE + "\n" + build_nav(group, item) + subnav + "\n" + NAV_SCRIPT


# ------------------------------------------------------------- section subnav

# 2026-07-07 選股頁面整理：targets / bottom-out / breakout / 盈餘加速 /
# entry-state（含回測）/ alpha-rank / state-machine 已封存（noindex stub），
# 從子選單移除；見 notes/site-internal/root/_proposal_stock_pages_cleanup_20260707.md。
DD_SCREENER_SUBNAV = [
    ("/dd-screener/", "總覽"),
    ("/dd-screener/pipeline.html", "Pipeline"),
    ("/dd-screener/quality-entry.html", "Quality-Entry"),
    ("/dd-screener/cyclical-track.html", "衛星·循環軌"),
    ("/dd-screener/sop-funnel.html", "SOP Funnel"),
    ("/dd-screener/sop-funnel-backtest.html", "SOP 回測"),
]


ENGINE_SUBNAV = [
    ("/engine/", "總覽 · 方法論"),
    ("/engine/radar.html", "全市場雷達"),
    ("/engine/cards.html", "決策卡"),
    ("/engine/arena.html", "席位擂台"),
    ("/engine/scoreboard.html", "形狀記分板"),
]


def build_subnav(links, current):
    items = "".join(
        f'<a href="{href}"{" class=\"active\"" if href == current else ""}>{label}</a>'
        for href, label in links
    )
    return f'\n<div class="imq-subnav"><div class="imq-subnav-inner">{items}</div></div>'


# ----------------------------------------------------------- active mapping

PREFIX_ACTIVE = [
    # 選股群
    ("cockpit/", ("pick", "cockpit")),
    # picks/ · dd-screener/pipeline.html · engine/ 皆為 redirect stub / iframe 片段（全在 SKIP_FILES，
    # 不會被注入 nav）；保留前綴僅為「選股群高亮」的語意錨，不再對應下拉條目（item=None）。
    ("picks/", ("pick", None)),
    ("dd-screener/pipeline.html", ("pick", None)),
    # 2026-08-23 清 dangling keys：dds/mom5/qus/qtw/scr 五個 item 鍵已於
    # 2026-08-20 選股群收斂（8 項→單一 cockpit）時從 MENU["pick"] 移除，
    # 但 PREFIX_ACTIVE 當時漏改，殘留指向不存在的下拉項（active_for() 永遠
    # 比對不到，等同無聲退化成無高亮）。統一改 ("pick", None)：頁面仍歸
    # 選股群高亮，不再假裝有對應下拉項。
    ("dd-screener/", ("pick", None)),
    ("engine/", ("pick", None)),
    ("research/momentum-5/", ("pick", None)),
    ("qgm/", ("pick", None)),
    ("qgm-tw/", ("pick", None)),
    ("screeners.html", ("pick", None)),
    ("screener.html", ("pick", None)),
    ("screener-tw.html", ("pick", None)),
    ("screener-jp.html", ("pick", None)),
    ("screener-my.html", ("pick", None)),
    # 研究群
    # 2026-08-20 nav 瘦身第二階段：下拉只剩 thub/id/tier 三項，故舊 dd/cmp/syn/sc
    # 四個 item 鍵已從 MENU["research"] 移除。以下映射改點到吸收方的 item——
    # 個股 DD／多股對比／期望落差三頁是「個股研究地圖的三種切法」，改指
    # "thub"；供應鏈地圖是 /id/ 的一個分頁，改指 "id"。效果＝這些頁面瀏覽時
    # 對應下拉項與群一起高亮，不退化成純群高亮。
    ("t/", ("research", "thub")),  # 個股研究（2026-07-11 新增；2026-08-20 改名）
    ("research/synthesis/", ("research", "thub")),
    ("research/", ("research", "thub")),
    ("dd/", ("research", "thub")),
    ("dca/", ("research", "thub")),
    ("report/", ("research", "thub")),
    ("id/tier_matrix.html", ("research", "tier")),
    ("id/", ("research", "id")),
    ("ds/", ("research", "id")),
    ("comparisons/", ("research", "thub")),
    ("supply-chain/", ("research", "id")),
    # 市場群
    ("earnings/", ("market", "earn")),
    # 2026-08-20 Phase C：六個舊監看入口自選單移除後，其頁面映射改
    # ("market", None)——仍歸市場群高亮，但不再有對應選單項目。
    ("catalyst/", ("market", None)),
    ("monitor/", ("market", None)),  # 全資產市場監測（2026-07-10；Phase C 併入 intel 儀表分頁）
    ("intel/", ("market", "intel")),  # 情報監視器 Phase 1（2026-08-19 新增）
    ("markets.html", ("market", "markets")),
    ("sectors.html", ("market", "sectors")),
    ("crowding/", ("market", None)),
    # rotation/radar.html 是「資產輪動雷達」獨立項目；須排在 rotation/ 之前，
    # 否則會被 rotation/ 前綴吃掉。index.html 與 ROTATION_*.html 歸市場群（無選單項）。
    ("rotation/radar.html", ("market", "radar")),  # 資產輪動雷達（2026-07-11 新增）
    ("rotation/", ("market", None)),
    ("regime/", ("market", None)),
    ("macro/", ("market", "macro")),  # 總經深度報告（2026-07-09），nav 已掛項目
    ("weekly/", ("market", "week")),
    ("briefing/", ("market", "brief")),  # 2026-08-17 恢復更新，nav 項目已掛回
    # 市場偵探：2026-08-23 系統群瘦身時移出系統群——它是 /intel/ 變化分頁的
    # 同源完整互動頁，比照 crowding/regime/rotation 的不轉址判定，改掛市場群
    # intel 項；頁面本身不轉址，維持獨立可直達。
    ("detective/", ("market", "intel")),  # 市場偵探（2026-07-16 新增；2026-08-20 曾掛系統群；2026-08-23 改掛市場群 intel）
    # 系統群（2026-08-23 瘦身：det/tr/pm/voltrack 四個 item 鍵自 MENU["system"]
    # 移除，收斂進「系統主控台」單一入口，故以下前綴一律改掛 lthub）
    ("track-record/", ("system", "lthub")),  # 裁決實績（2026-07-11 新增；2026-08-23 併入系統主控台）
    ("pm/", ("system", "lthub")),  # 持倉週掃（2026-07-19 復活；2026-08-23 併入系統主控台）
    # 2026-08-23 voltrack 項移除，實單主系統與三個 vt 家族頁改掛 lthub。
    ("long-track-w52-adaptive/", ("system", "lthub")),
    ("long-track-qs-vt/", ("system", "lthub")),
    ("long-track-adaptive-vt/", ("system", "lthub")),
    ("long-track-tw-vt/", ("system", "lthub")),
    # 2026-07-23 Phase B：退役頁（STX50/E3）與前瞻候選頁（GLD／商品 sleeve）改歸
    # 「追蹤總覽」(lthub)。★first-match 陷阱★：泛用前綴 long-track/ 必須排在所有具體
    # long-track-*/ 前綴之後，否則會吃掉 long-track-w52-adaptive/ 等頁的高亮。
    ("long-track-smh/", ("system", "lthub")),
    ("long-track-tw/", ("system", "lthub")),
    ("long-track-gld/", ("system", "lthub")),
    ("turtle-sleeve/", ("system", "lthub")),
    ("long-track/", ("system", "lthub")),   # 泛用前綴：排在所有 long-track-*/ 之後
    ("backtest/", ("system", "bt")),
    ("tools/", ("system", "tools")),
    # 2026-07-17 cache/ 獨立條目移除（併入公開資料）；保留前綴映射避免
    # /cache/ 頁面失去群/項高亮 —— 判斷：cache 是全站資料層新鮮度儀表板
    # （4 個 cache JSON 通用狀態，非 backtest 專屬），與 /data.html（公開
    # 資料端點文件）同屬「資料層」語意，故映射到 data 而非 bt。
    ("cache/", ("system", "data")),
    ("data.html", ("system", "data")),  # 公開資料（2026-07-11 新增）
    # 頂層
    ("flow/", ("flow", None)),  # 投資流程（2026-07-19 復活孤兒頁；頂層連結，howto 模式）
    ("mental-models/", ("mm", None)),
    ("how-to.html", ("howto", None)),
    ("search.html", ("search", None)),  # 搜尋（2026-07-11 新增頂層連結）
    ("index.html", ("home", None)),
]

SKIP_DIRS = {"_archived", "private"}
# 外部三 repo（+ 其 cron）擁有的 docs/ 子樹（見 .claude/notes/site-composition.md）：
#   qgm / qgm-tw → minervini-quality-backtest；briefing / weekly → morning-briefing；
#   backtest → v7-backtest。這些頁面的 nav 由各自 repo 內嵌的 canonical literal 重生，
#   本 repo 的 re-inject sweep 必須跳過整棵樹（否則會在工作區改動 400+ 支外部檔，
#   且下次外部 cron push 會覆蓋）。改 nav 時：本 repo re-inject 只動自有頁面，
#   外部樹靠 step「re-sync 三個外部 repo 的 synced literal」重生 byte-identical。
EXTERNAL_TREES = {"qgm", "qgm-tw", "briefing", "weekly", "backtest"}
SKIP_FILES = {
    "jot.html",                                 # 私人餵腦框（noindex 獨立小頁，不掛站 nav）
    "six-state/index.html",                     # redirect stub -> /backtest/six_state/status/
    "backtest/six_state/status/index.html",     # live status sub-page, intentionally headerless
    # 2026-07-10 選股主控台整併：舊 4 頁折進 /cockpit/ 四分頁。
    # 這 3 個 redirect stub 與 3 個 nav-less iframe 片段一律不注入站 nav
    # （片段被灌 nav 會在 iframe 內冒出整條站選單；stub 應保持極簡）。
    "picks/index.html",                         # redirect stub -> /cockpit/#picks
    "dd-screener/pipeline.html",                # redirect stub -> /cockpit/#pipeline
    "engine/index.html",                        # redirect stub -> /cockpit/#seats
    "picks/_embed.html",                        # iframe 片段（精選榜分頁）
    "dd-screener/_pipeline_body.html",          # iframe 片段（流程板機分頁）
    "engine/_index_body.html",                  # iframe 片段（席位排序·席位總表子分頁）
    # 2026-07-10 engine 四子頁收編成 /cockpit/#seats 子分頁：
    # 舊 4 URL → redirect stub；builder 改產 nav-less _*_body 片段（供子分頁 iframe）。
    "engine/radar.html",                        # redirect stub -> /cockpit/#seats-radar
    "engine/arena.html",                        # redirect stub -> /cockpit/#seats-arena
    "engine/cards.html",                        # redirect stub -> /cockpit/#seats-cards
    "engine/scoreboard.html",                   # redirect stub -> /cockpit/#seats-scoreboard
    "engine/_radar_body.html",                  # iframe 片段（雷達子分頁）
    "engine/_arena_body.html",                  # iframe 片段（擂台子分頁·M5 對照組 PREREG 凍結）
    "engine/_cards_body.html",                  # iframe 片段（決策卡子分頁）
    "engine/_scoreboard_body.html",             # iframe 片段（記分板子分頁）
    # 2026-08-20 研究區整併第一階段：/研究/ 群 7 頁收斂成 /t/ + /id/ 兩個主控台。
    # 3 個 redirect stub 與 4 個 nav-less iframe 片段一律不注入站 nav（原因同上）。
    "research/index.html",                      # redirect stub -> /t/#dd
    "comparisons/index.html",                   # redirect stub -> /t/#compare
    "research/synthesis/index.html",            # redirect stub -> /t/#synthesis
    "research/_body.html",                      # iframe 片段（/t/ DD 清單分頁）
    "comparisons/_body.html",                   # iframe 片段（/t/ 多股對比分頁）
    "research/synthesis/_body.html",            # iframe 片段（/t/ 期望落差分頁）
    "supply-chain/_body.html",                  # iframe 片段（/id/ 供應鏈地圖分頁；
                                                 # supply-chain/index.html 本身維持獨立完整頁，不進此清單）
    # 2026-08-23 系統群整併第一批：/long-track/ 升級四分頁主控台，
    # 3 個舊獨立 URL 改 redirect stub、3 個 builder 改產 nav-less iframe 片段。
    # long-track-w52-adaptive/leverage.html／tw-semivol.html 不在此批範圍內，
    # 仍維持獨立完整頁、照常注入站 nav。
    "long-track-w52-adaptive/index.html",        # redirect stub -> /long-track/#live
    "long-track-w52-adaptive/_body.html",        # iframe 片段（實單主系統分頁）
    "pm/index.html",                             # redirect stub -> /long-track/#positions
    "pm/_body.html",                             # iframe 片段（持倉週掃分頁）
    "track-record/index.html",                   # redirect stub -> /long-track/#record
    "track-record/_body.html",                   # iframe 片段（裁決實績分頁）
}


def active_for(rel: str):
    for prefix, ga in PREFIX_ACTIVE:
        if rel == prefix or rel.startswith(prefix):
            return ga
    return (None, None)


# ------------------------------------------------------------ legacy removal

STRIP_PATTERNS = [
    # canonical + all imq-nav-root header variants
    re.compile(r'[ \t]*<header class="imq-nav-root"[^>]*>.*?</header>\n?', re.S),
    # dedicated nav style blocks (canonical id= form and bare legacy form)
    re.compile(r'[ \t]*<style id="imq-nav-style">.*?</style>\n?', re.S),
    re.compile(r"[ \t]*<style>\s*\.imq-nav-root\{.*?</style>\n?", re.S),
    # dropdown toggle scripts
    re.compile(r"[ \t]*<script>\(function\(\)\{document\.querySelectorAll\('\.imq-dd-btn'\).*?</script>\n?", re.S),
    # legacy hover-nav used by earnings dailies
    re.compile(r'[ \t]*<nav class="imq-nav">.*?</nav>\n?', re.S),
    # supply-chain hub/topic header
    re.compile(r'[ \t]*<header class="site">.*?</header>\n?', re.S),
    # old six-state plain header
    re.compile(r'[ \t]*<header>\s*<div class="container hdr-inner">.*?</header>\n?', re.S),
    # tools/ wordpress-site header
    re.compile(r'[ \t]*<header class="site-header">.*?</header>\n?', re.S),
    # injected sub-nav strip (re-runs)
    re.compile(r'[ \t]*<div class="imq-subnav">.*?</div></div>\n?', re.S),
]

BODY_RE = re.compile(r"<body[^>]*>")


def process(path: Path, check=False):
    rel = str(path.relative_to(ROOT))
    parts = path.relative_to(ROOT).parts
    if any(part in SKIP_DIRS for part in parts):
        return "skip"
    if parts and parts[0] in EXTERNAL_TREES:
        return "skip-external"
    if rel in SKIP_FILES:
        return "skip"
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "non-utf8"
    m = BODY_RE.search(text)
    if not m:
        return "no-body"

    stripped = text
    for pat in STRIP_PATTERNS:
        stripped = pat.sub("", stripped)

    group, item = active_for(rel)
    subnav = ""
    if rel.startswith("dd-screener/"):
        subnav = build_subnav(DD_SCREENER_SUBNAV, "/" + rel)
    elif rel.startswith("engine/"):
        cur = "/engine/" if rel == "engine/index.html" else "/" + rel
        subnav = build_subnav(ENGINE_SUBNAV, cur)
    block = full_nav_block(group, item, subnav)

    m = BODY_RE.search(stripped)
    new = stripped[: m.end()] + "\n" + block + stripped[m.end():]
    if new == text:
        return "unchanged"
    if not check:
        path.write_text(new, encoding="utf-8")
    return "updated"


def main():
    check = "--check" in sys.argv
    counts = {}
    issues = []
    for path in sorted(ROOT.rglob("*.html")):
        status = process(path, check=check)
        counts[status] = counts.get(status, 0) + 1
        if status in ("no-body", "non-utf8"):
            issues.append((status, str(path.relative_to(ROOT))))
    for k, v in sorted(counts.items()):
        print(f"{k:10s} {v}")
    for status, rel in issues:
        print(f"  ⚠️  {status}: {rel}")


if __name__ == "__main__":
    main()
