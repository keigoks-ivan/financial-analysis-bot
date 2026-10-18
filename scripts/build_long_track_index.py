#!/usr/bin/env python3
"""系統主控台 /long-track/ 產生器（fab）— 2026-08-23 系統群整併，2026-09-10 總覽儀表板化＋分頁重分組，
2026-09-10 移除「個股：持倉週掃」分頁。

四分頁單一入口：
  #overview   總覽        — 頂部「今天」儀表板（讀 state.json／live_scoreboard.json，見
                            render_today_strip；今天曝險＋影子帳戶一覽，不重算任何數字）
                            ＋家族地圖三區（2026-10-18 整理）：實單主系統大卡片／還在測的
                            （一張小表，每列一個還沒答案的問題）／歸檔（預設收起的 details，
                            每條一句結論，文字來自 scripts/archive_banner.py）；沿革白話盒
                            收進 details，inline
  #live       美股即時    — iframe 嵌入 /long-track-w52-adaptive/_body.html
  #scoreboard 記分板      — iframe 嵌入 /long-track/_scoreboard_body.html（2026-09-10 由
                            #live 拆出獨立分頁；#live 內保留一個跳轉連結）
  #record     個股：裁決實績 — iframe 嵌入 /track-record/_body.html

「個股：持倉週掃」（#positions，原本 iframe 嵌 /pm/_body.html）已於 2026-09-10 移除——
它是一份人工個股研究報告（最後更新 2026-08-24），不屬於本系統主控台的機械化追蹤
範圍。docs/pm/ 本身未動、仍可獨立造訪；本檔的 console-tabbar／CONSOLE_JS 已不再嵌入它。
console-tabbar／CONSOLE_JS 的 TABS 白名單機制原本就會把未知 hash 落回 #overview，
所以舊的 /long-track/#positions 連結會自動 fallback 到總覽分頁，不會出錯。

舊獨立 URL（/long-track-w52-adaptive/、/track-record/）已改為
meta-refresh redirect stub，指回對應分頁錨點；來源頁的 builder
（update_long_track_w52_adaptive.py／build_track_record.py）
改產 nav-less _body.html 片段，已加入 scripts/site_nav.py 的 SKIP_FILES。
/long-track-w52-adaptive/leverage.html 與 tw-semivol.html 維持獨立完整頁，
不在此整併範圍內。

nav 用 full_nav_block("system","lthub")（追蹤總覽，MENU 條目本身未改動——
nav 瘦身留待下一批）。設計沿用本頁既有 token 體系（--brand:#1a56db 等），
未套用 /assets/imq-base.css 的 --line/--paper/--accent 等 token（本頁未載入
該檔），tabbar 樣式改用本頁既有配色以避免未定義變數。

用法：python3 scripts/build_long_track_index.py
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from site_nav import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "lthub")

# 實盤證據清單的資料來源：回測區頁面資料（docs/backtest/_page_meta.py，首頁第①區同一份）
sys.path.insert(0, str(HERE.parent / "docs" / "backtest"))
import _page_meta as _PM  # noqa: E402
from archive_banner import ARCHIVE_DATE, ARCHIVE_TEXT  # noqa: E402  (歸檔區每條線的一句結論)
OUT = HERE.parent / "docs" / "long-track" / "index.html"

# 2026-09-10 總覽儀表板化：讀既有兩份 JSON 產生「今天」區塊，本檔不重新計算任何數字——
# 缺欄位一律顯示「—」，絕不捏造。
STATE_JSON = HERE.parent / "docs" / "long-track-w52-adaptive" / "state.json"
SCOREBOARD_JSON = HERE.parent / "docs" / "market" / "data" / "live_scoreboard.json"

SPRT_MEANING = {          # 見 build_live_scoreboard.py 的 green/yellow/red 定義
    "green": ("綠", "影子勝過系統"),
    "red": ("紅", "系統勝過影子"),
    "yellow": ("黃", "樣本不足，尚未能判定"),
}

# 三區（2026-10-18 影子／對照線整理，持有人拍板）：實單主系統／還在測的／歸檔。
# 實單主系統：每組＝(分類、色、突出、系統清單)；系統 dict：name／url／one／status／freq／email
GROUPS = [
    ("實單主系統", "live", True, [
        {"name": "W52 × 自適應波動率（美股債金版・台股不借錢版）", "url": "/long-track-w52-adaptive/",
         "one": "兩市場各 70% 指數部＝W52 週線閘門 × 自適應波動率 ＋ A2 執行層。"
                "<b>2026-10-19 起：美股股票部分上限 100% 不借錢，另加公債（IEF）與黃金（GLD）各最多 20% 的週線疊加；台股上限 100%、不借錢。</b>"
                "此前（2026-07-18 至 10-16）用 cap 1.5 ＋日線均線確認，現降為對照線，每日更新、不寄信。",
         "status": ("實單", "live"), "freq": "每交易日 × 2（台／美收盤後）", "email": "✅ 有"},
    ]),
]

# 還在測的：每列一個還沒答案的問題。q／start／due／now／name／url（url 為 None 表示頁面還沒建）。
TESTING = [
    {"q": "新規則（2026-10-19 起：美股債金版、台股不借錢版）比舊規則（股票上限 150%，加日線均線確認）好嗎？",
     "start": "2026-10-19",
     "due": "上線滿 60 個交易日，或組合首次出現 10% 以上回撤時回顧（草案，持有人未確認）",
     "now": "2026-10-19 起累積中",
     "name": "舊規則對照線", "url": "/long-track-w52-adaptive/cap15.html"},
    {"q": "NFCI 紅燈時持股減半，能不能讓回撤變淺？",
     "start": "2026-10-19",
     "due": "2029-10-19 起（兩個市場都至少 3 次股災才判，最晚 2031-10-19）",
     "now": None, "key": "nfci",      # now 由 nfci_forward_now_html 讀影子線狀態檔組出
     "name": None, "url": None},
]

# 歸檔：先 2026-10-18 歸檔的七條（一句結論來自 archive_banner.ARCHIVE_TEXT，與各頁頂端橫幅同字），
# 再接原本已退役的六條。每列（名稱、網址、一句結論、右側狀態字）。
ARCHIVED_NEW = [
    ("不借錢版", "/long-track-w52-adaptive/leverage.html", ARCHIVE_TEXT["leverage"]),
    ("債金版", "/long-track-w52-adaptive/c1-shadow.html", ARCHIVE_TEXT["c1"]),
    ("舊規則版（沒有均線條件）", "/long-track-w52-adaptive/noma.html", ARCHIVE_TEXT["noma"]),
    ("台股下跌半變異", "/long-track-w52-adaptive/tw-semivol.html", ARCHIVE_TEXT["tw_semivol"]),
    ("黃金單腿（GLD）", "/long-track-gld/", ARCHIVE_TEXT["gld"]),
    ("商品組合", "/turtle-sleeve/", ARCHIVE_TEXT["turtle"]),
    ("F70：股票 70% 加三資產 30%", "/backtest/f_comfort/", ARCHIVE_TEXT["f70"]),
]
ARCHIVED_OLD = [
    ("STX50（美股 SMH／QQQ）", "/long-track-smh/",
     "2026-07-18 由 W52 × 自適應波動率接棒，2026-07-23 停更。", "2026-07-23 停更"),
    ("E3（台股 0050／2330）", "/long-track-tw/",
     "2026-07-18 由 W52 × 自適應波動率接棒，2026-07-23 停更。", "2026-07-23 停更"),
    ("0050＋2330 固定 σ", "/long-track-tw-vt/",
     "固定 σ 版波動率目標，早期研究線，已歸檔對照。", "凍結對照"),
    ("自適應美台總覽", "/long-track-adaptive-vt/",
     "自適應 σ 美台總覽，早期研究線，已歸檔對照。", "凍結對照"),
    ("QQQ＋SMH 套袖", "/long-track-qs-vt/",
     "週線長軌閘門 × 波動率套袖組合，早期研究線，已歸檔對照。", "凍結對照"),
    ("六狀態機（SMH／QQQ）", "/backtest/six_state/status/",
     "早期六狀態機引擎，已退役、僅手動；被 W52 × 自適應波動率取代。", "凍結對照"),
]

PLAIN = ('這個家族的沿革（白話）：早期實單主線用「六狀態機」與「STX50／E3」兩套引擎；'
         '<b>2026-07-18 起改由「W52 週線閘門 × 自適應波動率 × cap 1.5 ＋ A2 執行層」接棒為實單主系統</b>'
         '（美台兩市場各 70% 指數部），舊引擎降為凍結對照；'
         '<b>2026-10-19 起再改為美股債金版、台股不借錢版</b>（股票部分上限 100%，美股另加公債與黃金），cap 1.5 規則降為對照線。'
         f'<b>{ARCHIVE_DATE} 整理影子線</b>：不借錢版、債金版（已成為實單）、舊規則版、台股下跌半變異、黃金單腿、商品組合、F70 '
         '七條停止更新並歸檔，頁面凍結保留；還沒有答案的問題只剩下「還在測的」那張小表。')

CSS = """
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;--text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e;--grey:#9ca3af}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1080px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.6rem 0 1.1rem;background:linear-gradient(180deg,#eff6ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.5rem;font-weight:700;letter-spacing:-.03em}
.page-hdr .sub{color:var(--muted);font-size:.88rem;margin-top:.25rem;max-width:76ch}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}.crumb a{color:var(--muted)}
.plain-box{display:flex;gap:.6rem;background:#f0f7ff;border:1px solid #cfe3fb;border-left:4px solid #3b82f6;border-radius:8px;padding:.8rem 1rem;margin:1.1rem 0 .3rem;font-size:.88rem;line-height:1.7}
.pb-tag{flex:0 0 auto;font-size:.72rem;font-weight:700;color:#1e40af;background:#dbeafe;border-radius:6px;padding:.15rem .45rem;height:fit-content;white-space:nowrap}
.pb-body{color:#1e3a5f}.pb-body b{color:#1e40af}
.grp{margin-top:1.6rem}
.grp-h{font-size:.78rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin-bottom:.6rem;padding-left:.6rem;border-left:4px solid var(--grey)}
.grp.live .grp-h{border-left-color:var(--green);color:var(--green-text)}
.grp.cand .grp-h{border-left-color:var(--amber);color:var(--amber-text)}
.grp.shadow .grp-h{border-left-color:#6366f1}
.sys{display:block;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.95rem 1.15rem;margin-bottom:.7rem;color:inherit}
.sys:hover{border-color:var(--brand);text-decoration:none;box-shadow:0 1px 4px rgba(0,0,0,.06)}
.grp.live .sys{border-width:2px;border-color:var(--green)}
.sys-top{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-bottom:.35rem}
.sys-name{font-size:1.02rem;font-weight:700;color:var(--text)}
.grp.live .sys-name{color:var(--green-text)}
.pill{font-size:.68rem;font-weight:700;padding:.12rem .55rem;border-radius:99px;white-space:nowrap}
.pill.live{background:var(--green);color:#fff}
.pill.shadow{background:#eef2ff;color:#4338ca;border:1px solid #c7d2fe}
.pill.cand{background:var(--amber-bg);color:var(--amber-text);border:1px solid var(--amber-border)}
.pill.ret{background:#f3f4f6;color:var(--muted);border:1px solid var(--border)}
.pill.rej{background:#fbeceb;color:#b42318;border:1px solid #f0c4c0}
.ev-intro{font-size:.84rem;color:var(--muted);margin:.1rem 0 .7rem;line-height:1.65}
.sys-one{font-size:.86rem;color:#374151;line-height:1.6}
.sys-meta{display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:.5rem;font-size:.76rem;color:var(--muted)}
.sys-meta b{color:#374151;font-weight:600}
.arr{margin-left:auto;color:var(--brand);font-weight:700}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.2rem 0;font-size:.78rem;margin-top:2rem}

/* ── 總覽「今天」儀表板（2026-09-10）── */
.tstrip{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1rem 1.15rem;margin:1rem 0 1.3rem}
.tstrip-hdr{font-size:.78rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--brand);margin-bottom:.7rem}
.tstrip-grid{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}
.tstrip-mkt{border:1px solid var(--border);border-radius:8px;padding:.75rem .9rem}
.tstrip-mkt-h{font-weight:700;font-size:.92rem;margin-bottom:.35rem}
.tstrip-exp{font-size:.86rem;color:#374151;margin-bottom:.45rem}
.tstrip-exp b{color:var(--text)}
.tstrip-legs{display:flex;flex-wrap:wrap;gap:.5rem 1rem;font-size:.78rem;color:var(--muted)}
.tstrip-legs .leg b{color:var(--text)}
.tstrip-change{font-size:.84rem;margin:.9rem 0 .3rem;padding:.5rem .7rem;background:var(--brand-light);border-radius:6px}
.tstrip-note{font-size:.76rem;color:var(--muted);margin:.5rem 0 .7rem;line-height:1.6}
.tstrip-shadow-wrap{overflow-x:auto}
.tstrip-shadow{width:100%;border-collapse:collapse;font-size:.8rem}
.tstrip-shadow th{text-align:left;padding:.4rem .55rem;border-bottom:1px solid var(--border);font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.tstrip-shadow td{padding:.45rem .55rem;border-bottom:1px solid var(--border);vertical-align:top}
.tstrip-shadow td.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.tstrip-shadow .ts-def{color:#374151;max-width:34ch}
.tstrip-src{font-size:.72rem;color:var(--muted);margin-top:.6rem;font-family:ui-monospace,Menlo,monospace}
.sprt-pill{display:inline-block;width:1.1em;height:1.1em;border-radius:50%;text-align:center;font-size:.68rem;line-height:1.1em;color:#fff}
.sprt-green{background:var(--green)}.sprt-yellow{background:var(--amber)}.sprt-red{background:#dc2626}.sprt-na{background:var(--grey)}
.ov-lede{font-size:.88rem;color:#374151;line-height:1.75;margin-bottom:1rem}
.ov-history{margin-top:1.6rem;padding-top:.2rem}
.ov-history summary{cursor:pointer;font-weight:700;font-size:.85rem;color:var(--muted)}
@media(max-width:640px){.tstrip-grid{grid-template-columns:1fr}}

/* ── 卡片瘦身：影子對照／前瞻 OOS 候選改一行式、已退役收進 details（2026-09-10）── */
.sysrow{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;background:var(--card);border:1px solid var(--border);
  border-radius:8px;padding:.6rem .85rem;margin-bottom:.5rem;color:inherit}
.sysrow:hover{border-color:var(--brand);text-decoration:none}
.sysrow-name{font-weight:700;font-size:.88rem;color:var(--text)}
.sysrow-one{font-size:.8rem;color:var(--muted);flex:1 1 260px}
.shtbl-wrap{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.2rem .9rem .5rem}
.shtbl{width:100%;border-collapse:collapse;font-size:.84rem}
.shtbl th{text-align:left;padding:.55rem .5rem;border-bottom:1px solid var(--border);font-size:.72rem;color:var(--muted);font-weight:700}
.shtbl td{padding:.65rem .5rem;border-bottom:1px solid var(--border);vertical-align:top;color:#374151;line-height:1.6}
.shtbl tr:last-child td{border-bottom:0}
.shtbl td.sh-name a{font-weight:700;color:var(--text)}
.shtbl td.sh-name a:hover{color:var(--brand)}
.shtbl .sh-pill{display:inline-block;margin-top:.25rem;font-size:.68rem;font-weight:700;padding:.1rem .5rem;border-radius:99px;background:var(--amber-bg);color:var(--amber-text);border:1px solid var(--amber-border)}
.shtbl .sh-ret b{color:var(--text);font-variant-numeric:tabular-nums}
.shtbl .sh-since{display:block;font-size:.72rem;color:var(--muted)}
.shtbl .sh-na{color:var(--muted)}
.sh-foot{font-size:.74rem;color:var(--muted);margin:.4rem .1rem 0;line-height:1.6}
@media(max-width:640px){
  .shtbl thead{display:none}
  .shtbl,.shtbl tbody,.shtbl tr,.shtbl td{display:block;width:100%}
  .shtbl tr{padding:.5rem 0;border-bottom:1px solid var(--border)}
  .shtbl tr:last-child{border-bottom:0}
  .shtbl td{border-bottom:0;padding:.2rem .3rem}
  .shtbl td[data-label]::before{content:attr(data-label);display:block;font-size:.7rem;font-weight:700;color:var(--muted)}
  .shtbl td.sh-name::before{display:none}
}
.ov-retired{margin-top:1.6rem}
.ov-retired summary{cursor:pointer;font-weight:800;font-size:.78rem;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);
  padding-left:.6rem;border-left:4px solid var(--grey)}
.retired-list{margin-top:.6rem}
.retired-row{display:flex;justify-content:space-between;gap:.8rem;padding:.45rem .3rem;border-bottom:1px solid var(--border);
  font-size:.82rem;color:inherit}
.retired-row:hover{color:var(--brand)}
.retired-row .rr-meta{color:var(--muted);flex:0 0 auto;white-space:nowrap}
.arch-row{display:flex;gap:.3rem .9rem;flex-wrap:wrap;align-items:baseline;padding:.55rem .3rem;border-bottom:1px solid var(--border);font-size:.82rem;color:inherit}
.arch-row:hover{color:var(--brand);text-decoration:none}
.arch-row .ar-name{font-weight:700;flex:0 0 13em;color:var(--text)}
.arch-row .ar-one{flex:1 1 22em;color:#4b5563;line-height:1.6}
.arch-row .ar-meta{color:var(--muted);flex:0 0 auto;white-space:nowrap;font-size:.76rem}
.arch-sub{font-size:.74rem;font-weight:700;color:var(--muted);margin:.8rem 0 .1rem .3rem}
.tsttbl-note{font-size:.76rem;color:var(--muted);margin:.4rem .1rem 0;line-height:1.6}

/* ── 系統主控台 tabbar（2026-08-23，比照 /cockpit/ 與 /t/ 殼；沿用本頁既有 token）── */
.console-tabbar{display:flex;gap:.25rem;flex-wrap:wrap;border-bottom:1px solid var(--border);margin:.2rem 0 1.3rem;position:sticky;top:0;background:var(--bg);z-index:5}
.console-tab-btn{appearance:none;background:none;border:0;font-family:inherit;cursor:pointer;
  font-size:.94rem;font-weight:600;color:var(--muted);padding:.7rem 1.05rem;
  border-bottom:2px solid transparent;margin-bottom:-1px;letter-spacing:.01em}
.console-tab-btn:hover{color:var(--text)}
.console-tab-btn.active{color:var(--brand);border-bottom-color:var(--brand)}
.console-tab-panel{display:none}
.console-tab-panel.active{display:block}
.console-embed-frame{width:100%;border:0;display:block;min-height:70vh;background:transparent}
.console-embed-note{font-size:.72rem;color:var(--muted);margin:.9rem 0 .6rem;font-family:ui-monospace,Menlo,monospace}
.console-embed-note a{color:var(--brand)}
@media(max-width:640px){.console-tab-btn{padding:.55rem .65rem;font-size:.82rem}}
"""

CONSOLE_JS = """
<script>
(function(){
  "use strict";
  var TABS = ['overview','live','scoreboard','record'];
  // 2026-09-10 分頁重新分組：live（美股即時）與 scoreboard（記分板）各自獨立分頁
  // （先前 F1 修法把兩個 iframe 疊在同一個 live 分頁下，本次拆開，#live／
  // #record 舊錨點維持可用，新增 #scoreboard）。「個股：持倉週掃」（#positions）
  // 已於同日移除（人工報告、非本系統機械化追蹤範圍）——不在 TABS 白名單內的
  // hash 一律落回 #overview，故舊的 #positions 連結不會出錯。每個 tab 對應一個
  // id 陣列。
  var FRAME_ID = {live:['live-frame'], scoreboard:['scoreboard-frame'],
                  record:['record-frame']};

  function sizeFrame(fr){
    try{
      var d = fr.contentDocument || fr.contentWindow.document;
      if(!d) return;
      var h = Math.max(d.documentElement ? d.documentElement.scrollHeight : 0,
                       d.body ? d.body.scrollHeight : 0);
      if(h > 0) fr.style.height = (h + 24) + 'px';
    }catch(e){}
  }
  function wireSize(fr){
    fr.addEventListener('load', function(){
      sizeFrame(fr);
      var n = 0, iv = setInterval(function(){ sizeFrame(fr); if(++n > 16) clearInterval(iv); }, 400);
    });
  }
  var frames = {};
  Object.keys(FRAME_ID).forEach(function(k){
    var arr = [];
    FRAME_ID[k].forEach(function(id){
      var fr = document.getElementById(id);
      if(fr){ arr.push(fr); wireSize(fr); }
    });
    if(arr.length) frames[k] = arr;
  });

  function ensureLoaded(k){
    var arr = frames[k];
    if(!arr) return;
    arr.forEach(function(fr){
      var src = fr.getAttribute('data-src');
      if(fr._loadedSrc === src){ sizeFrame(fr); return; }
      fr._loadedSrc = src;
      fr.src = src;
    });
  }

  function activate(tab){
    var anchor = null;
    if(tab === 'evidence' || tab === 'archive'){ anchor = tab; tab = 'overview'; }
    if(TABS.indexOf(tab) < 0) tab = 'overview';
    document.querySelectorAll('.console-tab-btn').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-ctab') === tab);
    });
    document.querySelectorAll('.console-tab-panel').forEach(function(p){
      p.classList.toggle('active', p.id === 'panel-' + tab);
    });
    if(frames[tab]) ensureLoaded(tab);
    if(anchor){ var el = document.getElementById(anchor); if(el){ if(el.tagName === 'DETAILS') el.open = true; el.scrollIntoView(); } }
  }

  document.querySelectorAll('.console-tab-btn').forEach(function(b){
    b.addEventListener('click', function(){
      var t = b.getAttribute('data-ctab');
      if(('#' + t) !== location.hash){ location.hash = t; }
      else { activate(t); }
    });
  });
  window.addEventListener('hashchange', function(){
    activate((location.hash || '#overview').replace('#',''));
  });

  var initial = (location.hash || '#overview').replace('#','');
  activate(initial);
})();
</script>
"""


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def render_today_strip() -> str:
    """總覽最上方「今天」區塊：美股／台股各自的目標曝險（訊號）／現持曝險（執行層）
    ／每腿閘門在場出場／最近一次執行層變動，讀 long-track-w52-adaptive/state.json；
    下方影子帳戶一覽讀 market/data/live_scoreboard.json。本函式不計算任何新數字，
    缺欄位一律顯示「—」。"""
    state = _load_json(STATE_JSON)
    scoreboard = _load_json(SCOREBOARD_JSON)

    tickers = state.get("tickers", {})
    data_date = state.get("data_date", "—")
    last_change_date = state.get("last_change_date") or "—"
    last_change_desc = html.escape(state.get("last_change_desc") or "尚無紀錄", quote=False)

    def leg_span(t):
        tk = tickers.get(t)
        if not tk:
            return f'<span class="leg"><b>{t}</b>：—</span>'
        gate = "在場" if tk.get("gate") else "出場"
        final = tk.get("final_weight_pct", "—")
        exe = tk.get("executed_pct", "—")
        return (f'<span class="leg"><b>{t}</b> {gate}｜目標 {final}%｜現持 {exe}%</span>')

    def mkt_block(name, legs, exp_key):
        exp = state.get(exp_key, "—")
        vals = [tickers[t]["executed_pct"] for t in legs if isinstance(tickers.get(t), dict) and "executed_pct" in tickers[t]]
        exec_sum = round(sum(vals), 1) if len(vals) == len(legs) and legs else "—"
        rows = "".join(leg_span(t) for t in legs)
        return (f'<div class="tstrip-mkt"><div class="tstrip-mkt-h">{name}</div>'
                f'<div class="tstrip-exp">目標曝險（訊號，週線閘門 × 自適應套袖算出的理論持股率）<b>{exp}%</b>'
                f' ／ 現持曝險（執行層，實際已調整到的持股率——A2 規則要求目標與現持差達 20 個百分點才調整，故常與目標有差）<b>{exec_sum}%</b></div>'
                f'<div class="tstrip-legs">{rows}</div></div>')

    us_block = mkt_block("美股 QQQ + SMH", ["QQQ", "SMH"], "combined_exposure_us_pct")
    tw_block = mkt_block("台股 0050 + 2330", ["0050", "2330"], "combined_exposure_tw_pct")
    change_line = f'最近一次執行層變動：<b>{last_change_date}</b>｜{last_change_desc}'
    ov = state.get("overlay") or {}
    if all(k in ov for k in ("ief", "gld")):
        def _ov(k, nm):
            o = ov[k]
            return f'{nm} <b>{o.get("n", "—")}／3</b> 條成立，目標 <b>{o.get("target_pct", "—")}%</b>'
        ov_state = "已生效" if ov.get("active") else f'{ov.get("active_from", "2026-10-19")} 起生效，目前為預覽'
        change_line += (f'<br>美股債金疊加（占指數部淨值，各最多 20%，{ov_state}）：'
                        f'{_ov("ief", "公債（IEF）")}；{_ov("gld", "黃金（GLD）")}')

    shadow_entries = [   # (顯示名, market key, shadow key)
        ("S-60（美）", "us", "s60"), ("S-F（美）", "us", "sf"),
        ("S-A10（美）", "us", "sa10"), ("S-F70（美）", "us", "sf70"),
        ("S-60（台）", "tw", "s60"), ("S-A10（台）", "tw", "sa10"),
    ]
    shadows = scoreboard.get("shadows", {})
    shadow_rows = ""
    for label, mkey, skey in shadow_entries:
        sh = shadows.get(mkey, {}).get(skey) if isinstance(shadows.get(mkey), dict) else None
        if not sh:
            continue
        defi = html.escape(sh.get("definition", "—"), quote=False)
        diff = sh.get("cum_diff_vs_sys")
        diff_txt = f"{diff:+.2f} pp" if isinstance(diff, (int, float)) else "—"
        months = sh.get("n_closed_months", "—")
        status = (sh.get("sprt") or {}).get("status")
        col, meaning = SPRT_MEANING.get(status, ("—", "—"))
        shadow_rows += (f'<tr><td>{label}</td><td class="ts-def">{defi}</td>'
                        f'<td class="num">{diff_txt}</td><td class="num">{months}</td>'
                        f'<td><span class="sprt-pill sprt-{status or "na"}">{col}</span> {meaning}</td></tr>')
    if not shadow_rows:
        shadow_rows = '<tr><td colspan="5" style="color:var(--muted)">影子帳戶資料未就緒</td></tr>'
    as_of = scoreboard.get("as_of", "—")

    return f"""<div class="tstrip">
  <div class="tstrip-hdr">今天</div>
  <div class="tstrip-grid">{us_block}{tw_block}</div>
  <div class="tstrip-change">{change_line}</div>
  <div class="tstrip-note">影子帳戶＝同一套實單系統的訊號，換一種資金配置或槓桿規則跑出的對照組合（例如固定持股不動、加一塊分散資產、不加槓桿）——用來檢驗「現行規則真的比較好」這個問題本身，不是另一套建議操作。SPRT＝一種一邊累積樣本、一邊持續檢定的統計方法，樣本不夠前會停在「黃」。</div>
  <div class="tstrip-shadow-wrap"><table class="tstrip-shadow">
  <thead><tr><th>影子帳戶</th><th>定義</th><th class="num">累計淨值差（pp）</th><th class="num">已收月數</th><th>SPRT 判定</th></tr></thead>
  <tbody>{shadow_rows}</tbody></table></div>
  <div class="tstrip-src">數字讀自 state.json（數據截至 {data_date}）與 live_scoreboard.json（as of {as_of}），本頁不重新計算。</div>
</div>"""


NFCI_FORWARD_JSON = HERE.parent / "docs" / "long-track" / "data" / "nfci_forward_state.json"
NFCI_PENDING = "2026-10-19 起累積中"


def _nfci_pp(bp) -> str:
    """整數基點 → 百分點，一位小數（只在顯示時換算）。"""
    return f"{bp / 100:+.1f}"


def nfci_forward_now_html(state) -> str:
    """「還在測的」NFCI 那一列的目前結果：讀 update_nfci_forward.py 寫的狀態檔，不重算。
    檔案不存在或還沒有影子資料時寫「2026-10-19 起累積中」。判定日之前只放累積中的數字，不提前判。"""
    if not state or not state.get("markets"):
        return NFCI_PENDING
    cur = (state.get("nfci") or {}).get("current") or {}
    color = {"red": "紅燈", "green": "綠燈"}.get(cur.get("color"), "—")
    parts = [f"目前燈號：{color}（{cur.get('release_date', '—')} 公布的版本）"]
    for key, label in (("us", "美股"), ("tw", "台股")):
        m = state["markets"].get(key)
        if not m:
            parts.append(f"{label}：{NFCI_PENDING}")
            continue
        cr = m["crashes"]
        if cr["count"]:
            eps = "、".join(_nfci_pp(e["benefit_bp"]) + ("（進行中）" if not e["recovered"] else "")
                           for e in cr["episodes"])
            crash = f"股災 {cr['count']} 次，每次影子線少跌（個百分點，負數代表跌得更深）：{eps}"
        else:
            crash = "股災 0 次"
        cal = m["calmar"]
        if cal.get("shadow") is not None and cal.get("live") is not None:
            calmar = f"整段 Calmar（年化報酬 ÷ 最大回撤）影子線 {cal['shadow']:.2f}／實單 {cal['live']:.2f}"
        else:
            calmar = "整段 Calmar（年化報酬 ÷ 最大回撤）滿一年後才算"
        adj = m["adjustments"]
        ratio = f"{adj['ratio']:.2f} 倍" if adj.get("ratio") is not None else "—"
        parts.append(f"{label}：{crash}；{calmar}；調整次數比 {ratio}（影子線 {adj['shadow']} 次／實單 {adj['live']} 次）")
    if state.get("status") not in (None, "累積中"):
        word = {True: "過", False: "沒過", None: "算不出來"}
        crit = state.get("criteria") or {}
        for key, label in (("us", "美股"), ("tw", "台股")):
            c = crit.get(key)
            if c:
                parts.append(f"已到判定日（{state['status']}）{label}：股災 {word[c['crash_rule']]}、"
                             f"整段報酬回撤比 {word[c['calmar_rule']]}、調整次數 {word[c['trade_rule']]}"
                             f"{'' if c['crashes_enough'] else '（股災不滿 3 次）'}")
        if not crit:
            parts.append(f"已到判定日：{state['status']}")
    return "<br>".join(parts)


def _load_nfci_forward():
    try:
        return json.loads(NFCI_FORWARD_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def render_testing_table(rows) -> str:
    """還在測的：一張小表，每列一個還沒答案的問題。欄位＝問題、開始日、判定日、目前結果、頁面連結。
    「目前結果」沒有自動來源就寫文字，不編數字。"""
    body = ""
    for r in rows:
        link = (f'<a href="{r["url"]}">{r["name"]}</a>' if r.get("url") else '<span class="sh-na">—</span>')
        body += (f'<tr><td class="sh-name" data-label="問題">{r["q"]}</td>'
                 f'<td data-label="開始日">{r["start"]}</td>'
                 f'<td data-label="判定日">{r["due"]}</td>'
                 f'<td data-label="目前結果">{nfci_forward_now_html(_load_nfci_forward()) if r.get("key") == "nfci" else r["now"]}</td>'
                 f'<td data-label="頁面">{link}</td></tr>')
    return (f'<div class="shtbl-wrap"><table class="shtbl"><thead><tr><th>問題</th><th>開始日</th>'
            f'<th>判定日</th><th>目前結果</th><th>頁面</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>'
            f'<div class="tsttbl-note">只列還沒有答案的問題。判定日是回顧的時點，不是自動切換規則的日子；'
            f'第一列的判定日是草案，等持有人確認。</div>')


def render_archive() -> str:
    """歸檔區：預設收起。先 2026-10-18 歸檔的七條，再接原本已退役的六條；每條一句結論。"""
    new_rows = "".join(
        f'<a class="arch-row" href="{u}"><span class="ar-name">{n}</span><span class="ar-one">{one}</span>'
        f'<span class="ar-meta">{ARCHIVE_DATE} 歸檔</span></a>'
        for n, u, one in ARCHIVED_NEW)
    old_rows = "".join(
        f'<a class="arch-row" href="{u}"><span class="ar-name">{n}</span><span class="ar-one">{one}</span>'
        f'<span class="ar-meta">{st}</span></a>'
        for n, u, one, st in ARCHIVED_OLD)
    total = len(ARCHIVED_NEW) + len(ARCHIVED_OLD)
    return (f'<details class="ov-retired" id="archive"><summary>歸檔（{total}）</summary>'
            f'<div class="retired-list">'
            f'<div class="arch-sub">{ARCHIVE_DATE} 歸檔：停止更新，頁面凍結保留（{len(ARCHIVED_NEW)}）</div>{new_rows}'
            f'<div class="arch-sub">更早已退役（{len(ARCHIVED_OLD)}）</div>{old_rows}'
            f'</div></details>')


def render_evidence() -> str:
    """「實盤證據」一節：支撐實單配置的檢驗頁（資料來自 docs/backtest/_page_meta.py 第①區）。
    實盤與候選直接列出，已否決的收在摺疊區。頁面網址維持 /backtest/…，不搬家。"""
    import html as _H
    urls = _PM.ZONE_ORDER[1]
    pill_cls = {"live": "live", "cand": "cand", "rej": "rej", "ret": "ret", "note": "ret"}

    def row(u):
        p = _PM.PAGES[u]
        return (f'<a class="sysrow" href="{u}"><span class="sysrow-name">{_H.escape(p["title"], quote=False)}</span>'
                f'<span class="pill {pill_cls[p["status"]]}">{_PM.STATUS[p["status"]]}</span>'
                f'<span class="sysrow-one">{_H.escape(p["desc"], quote=False)}</span><span class="arr">→</span></a>')

    shown = [u for u in urls if _PM.PAGES[u]["status"] in ("live", "cand", "note")]
    dead = [u for u in urls if _PM.PAGES[u]["status"] in ("rej", "ret")]
    body = "".join(row(u) for u in shown)
    dead_html = ""
    if dead:
        dead_html = (f'<details class="ov-retired" style="margin-top:.8rem"><summary>已否決與已退役（{len(dead)}）</summary>'
                     f'<div class="retired-list">{"".join(row(u) for u in dead)}</div></details>')
    intro = (f'<div class="ev-intro">支撐實單配置的檢驗，共 {len(urls)} 頁，先看第一頁的總覽。'
             f'每頁的結論和判斷依據都寫在頁內；網址在回測區，狀態標籤與回測區首頁一致。</div>')
    return (f'<div class="grp live" id="evidence"><div class="grp-h">實盤證據</div>{intro}{body}{dead_html}</div>\n')


def render_overview_body() -> str:
    """總覽分頁本體（家族地圖）— 獨立於 page chrome，供 console 殼內嵌 Tab 1。
    2026-09-10 改版：頂部加「今天」儀表板（見 render_today_strip），實單主系統維持
    大卡片，沿革白話盒移到底部 details。
    2026-10-18 整理成三區：實單主系統／還在測的（一張小表）／歸檔（預設收起，含七條新歸檔
    與六條早已退役）。實盤證據清單（render_evidence）維持在還在測的之後。"""
    today_strip = render_today_strip()
    lede = ('<div class="ov-lede">看這三件事就好：上面「今天」區塊的<b>今天曝險</b>'
            '（目標／現持曝險與各腿在場／出場）、<b>最近一次變動</b>（哪一天、哪一腿調整了多少）、'
            '區塊底部影子帳戶表的<b>影子帳戶怎麼說</b>（累計淨值差與 SPRT 判定是否已經足夠判斷現行規則比對照組好）。'
            '還沒有答案的問題，看下面「還在測的」。</div>')

    live_title, live_cls, _, live_systems = GROUPS[0]
    live_rows = ""
    for s in live_systems:
        st_txt, st_cls = s["status"]
        live_rows += (
            f'<a class="sys" href="{s["url"]}">'
            f'<div class="sys-top"><span class="sys-name">{s["name"]}</span>'
            f'<span class="pill {st_cls}">{st_txt}</span><span class="arr">→</span></div>'
            f'<div class="sys-one">{s["one"]}</div>'
            f'<div class="sys-meta"><span>更新頻率：<b>{s["freq"]}</b></span>'
            f'<span>Email 通知：<b>{s["email"]}</b></span></div></a>')
    groups_html = f'<div class="grp {live_cls}"><div class="grp-h">{live_title}</div>{live_rows}</div>\n'

    groups_html += (f'<div class="grp shadow"><div class="grp-h">還在測的</div>'
                    f'{render_testing_table(TESTING)}</div>\n')

    groups_html += render_evidence()

    retired_html = render_archive()

    history_html = (f'<details class="ov-history"><summary>沿革</summary>'
                    f'<div class="plain-box" style="margin-top:.6rem">'
                    f'<span class="pb-tag">💬 白話</span><span class="pb-body">{PLAIN}</span></div></details>')

    return f'{today_strip}{lede}{groups_html}{retired_html}{history_html}'


def render() -> str:
    overview_body = render_overview_body()
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>系統主控台 | InvestMQuest Research</title>
<style>{CSS}</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 系統主控台</div>
  <h1>系統主控台</h1>
  <div class="sub">總覽 · 美股即時 · 記分板 · 個股：裁決實績 — 四分頁單一入口，一頁看清整個追蹤家族的定位、現況與紀律紀錄。</div>
</div></div>
<div class="container">
<div class="console-tabbar" role="tablist">
  <button type="button" class="console-tab-btn" data-ctab="overview" role="tab">總覽</button>
  <button type="button" class="console-tab-btn" data-ctab="live" role="tab">美股即時</button>
  <button type="button" class="console-tab-btn" data-ctab="scoreboard" role="tab">記分板</button>
  <button type="button" class="console-tab-btn" data-ctab="record" role="tab">個股：裁決實績</button>
</div>
<div class="console-tab-panel" id="panel-overview">{overview_body}</div>
<div class="console-tab-panel" id="panel-live">
  <p class="console-embed-note">W52 × 自適應波動率（美股債金版・台股不借錢版）· 2026-10-19 起新規則實單主系統 · <a href="/long-track-w52-adaptive/">獨立頁</a> · <a href="/backtest/live_system_evidence/">這套系統的證據總覽（12 頁，白話）→</a> · <a href="#scoreboard">跳到記分板 →</a></p>
  <iframe class="console-embed-frame" id="live-frame" data-src="/long-track-w52-adaptive/_body.html" title="實單主系統" scrolling="no" loading="lazy"></iframe>
</div>
<div class="console-tab-panel" id="panel-scoreboard">
  <p class="console-embed-note">實單前瞻記分板（NAV／回撤／基準差／資料缺口，PREREG 2026-09-05） · <a href="/long-track/_scoreboard_body.html">獨立片段</a></p>
  <iframe class="console-embed-frame" id="scoreboard-frame" data-src="/long-track/_scoreboard_body.html" title="實單前瞻記分板" scrolling="no" loading="lazy"></iframe>
</div>
<div class="console-tab-panel" id="panel-record">
  <p class="console-embed-note">本站個股 DD 裁決的回顧性前瞻報酬統計，描述器語言、非績效宣傳 · <a href="/track-record/">獨立頁</a></p>
  <iframe class="console-embed-frame" id="record-frame" data-src="/track-record/_body.html" title="裁決實績" scrolling="no" loading="lazy"></iframe>
</div>
</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 系統主控台 · 僅供研究參考</div></footer>
{CONSOLE_JS}
</body>
</html>"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
