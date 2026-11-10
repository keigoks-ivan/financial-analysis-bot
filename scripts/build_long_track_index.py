#!/usr/bin/env python3
"""系統主控台 /long-track/ 產生器（fab）。2026-11-08 整頁改版（持有人拍板）：美股、台股各一個分頁，內容順序相同：
每個標的應持有多少 %（分母是該市場總資金）與跟上週的變化、個股席位（只有美股）、下週會動的價位、實盤紀錄、系統績效、
一年水位變化與 K 棒軌跡（收起）、規則與揭露（收起）。第三個分頁放對照與歸檔。

資料都讀現成檔案，本檔不算訊號：state.json（指數部）、arena-ledger.json（美股席位）、
data/system_profile.json（體檢摘要）。實盤紀錄切自 _scoreboard_body.html，圖表與規則切自 long-track-w52-adaptive/_body.html，
樣式加前綴後直接放進頁面，不用內嵌框。切不到就顯示連結，不讓整頁壞掉。
舊錨點：#overview／#live／#scoreboard 落到美股分頁；#record 轉到 /track-record/；#evidence／#archive 落到對照與歸檔。

用法：python3 scripts/build_long_track_index.py
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from site_nav import full_nav_block  # noqa: E402
import live_rules as _lr  # noqa: E402  實盤規則正本 knowledge/live_rules.toml（資金換算 [params.capital]）

NAV_BLOCK = full_nav_block("system", "lthub")

# 實盤證據清單的資料來源：回測區頁面資料（docs/backtest/_page_meta.py，首頁第①區同一份）
sys.path.insert(0, str(HERE.parent / "docs" / "backtest"))
import _page_meta as _PM  # noqa: E402
from archive_banner import ARCHIVE_DATE, ARCHIVE_TEXT  # noqa: E402  (歸檔區每條線的一句結論)
OUT = HERE.parent / "docs" / "long-track" / "index.html"

STATE_JSON = HERE.parent / "docs" / "long-track-w52-adaptive" / "state.json"

TESTING = [
    {"q": "Supertrend 週線＋月線比 W52 × 自適應波動率好嗎？",
     "start": "2026-11-04",
     "due": "不設績效退回，2027-11-04 回顧只記錄、不改（規則帳本 2026-11-04）",
     "now": "2026-11-04 起累積中",
     "name": "W52 對照線", "url": "/long-track-w52-adaptive/w52.html"},
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
     "2026-07-18 由新系統接棒，2026-07-23 停更。", "2026-07-23 停更"),
    ("SMH 槓桿疊加", "/long-track-smh/leverage/",
     ARCHIVE_TEXT["smh_leverage"], f"{ARCHIVE_DATE} 歸檔"),
    ("E3（台股 0050／2330）", "/long-track-tw/",
     "2026-07-18 由新系統接棒，2026-07-23 停更。", "2026-07-23 停更"),
    ("0050＋2330 固定 σ", "/long-track-tw-vt/",
     "固定 σ 版波動率目標，早期研究線，已歸檔對照。", "凍結對照"),
    ("自適應美台總覽", "/long-track-adaptive-vt/",
     "自適應 σ 美台總覽，早期研究線，已歸檔對照。", "凍結對照"),
    ("QQQ＋SMH 套袖", "/long-track-qs-vt/",
     "週線長軌閘門 × 波動率套袖組合，早期研究線，已歸檔對照。", "凍結對照"),
    ("六狀態機（SMH／QQQ）", "/backtest/six_state/status/",
     "早期六狀態機引擎，已退役、僅手動；已由現行系統取代。", "凍結對照"),
]

PLAIN = ('這個家族的沿革（白話）：早期實單主線用「六狀態機」與「STX50／E3」兩套引擎，現已降為凍結對照；'
         '現行實單主系統是 Supertrend 週線＋月線（美股債金版、台股不借錢版）。'
         f'<b>{ARCHIVE_DATE} 整理影子線</b>：不借錢版、債金版、舊規則版、台股下跌半變異、黃金單腿、商品組合、F70 '
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
@media(max-width:640px){.console-tab-btn{padding:.55rem .65rem;font-size:.82rem}}
:root{--lt-muted:#5f6b7a}
@media(max-width:640px){.lt-sec .lt-lsb .lsb-tiles{display:grid;grid-template-columns:1fr 1fr;gap:.4rem}
  .lt-sec .lt-lsb table th,.lt-sec .lt-lsb table td{white-space:nowrap}
  .lt-sec .lt-lsb table{display:block;overflow-x:auto}}
.lt-next{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.8rem 1rem;margin:.4rem 0 .9rem}
.lt-next-h{font-size:.78rem;font-weight:800;color:var(--lt-muted);margin-bottom:.3rem}
.lt-next-row{display:flex;flex-wrap:wrap;gap:.15rem .6rem;align-items:baseline;padding:.15rem 0}
.lt-next-row b{min-width:2.4rem}
.lt-next-row small{color:var(--lt-muted);font-size:.76rem}
.lt-cap{font-size:.78rem;color:var(--lt-muted);margin:.1rem 0 .65rem;max-width:80ch}
.lt-panel.lt-hidden{display:none}
.lt-sec{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.95rem 1.1rem;margin-bottom:.9rem}
.lt-sec h2{font-size:1.02rem;font-weight:800;margin-bottom:.3rem}
.lt-h3{font-size:.86rem;font-weight:700;margin:.9rem 0 .35rem}
.lt-scroll{overflow-x:auto}
.lt-tbl{width:100%;border-collapse:collapse;font-size:.9rem}
.lt-tbl th{font-size:.76rem;color:var(--lt-muted);font-weight:600;text-align:left;border-bottom:1px solid var(--border);padding:.3rem .4rem;white-space:nowrap}
.lt-tbl td{border-bottom:1px solid var(--border);padding:.45rem .4rem;vertical-align:top}
.lt-tbl .num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.lt-nowrap td,.lt-nowrap th{white-space:nowrap}
.lt-sub{display:block;font-size:.74rem;color:var(--lt-muted)}
.lt-target{font-weight:800}
.lt-buy{color:var(--green-text);font-weight:800}
.lt-sell{color:var(--red-text,#b91c1c);font-weight:800}
.lt-hold,.lt-muted{color:var(--lt-muted)}
.lt-total td{font-weight:700;border-bottom:0;background:var(--bg)}
.lt-stale{background:var(--red-bg,#fbeceb);color:var(--red-text,#b91c1c);border-radius:6px;padding:.45rem .65rem;font-size:.84rem;margin-bottom:.6rem}
.lt-fold>summary{cursor:pointer;font-weight:700;font-size:.92rem}
.lt-fold[open]>summary{margin-bottom:.7rem}
.lt-links{list-style:none;display:flex;flex-direction:column;gap:.3rem;font-size:.9rem}
"""

CONSOLE_JS = """
<script>
(function(){
  "use strict";
  var TABS = ['us','tw','ref'];
  var ALIAS = {overview:'us', live:'us', scoreboard:'us', evidence:'ref', archive:'ref'};
  // 站頭會黏在畫面上方，分頁列要停在它下面
  var nav = document.querySelector('.imq-nav-root'), bar = document.querySelector('.console-tabbar');
  if(nav && bar && getComputedStyle(nav).position !== 'static'){ bar.style.top = nav.offsetHeight + 'px'; }
  // 圖表要在看得見的時候才量得到寬度，建好才收起來、切分頁
  document.querySelectorAll('details[data-lt-close]').forEach(function(d){ d.open = false; });
  function activate(raw){
    if(raw === 'record'){ location.replace('/track-record/'); return; }
    var tab = TABS.indexOf(raw) >= 0 ? raw : (ALIAS[raw] || 'us');
    document.querySelectorAll('.console-tab-btn').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-ctab') === tab);
    });
    document.querySelectorAll('.lt-panel').forEach(function(p){
      p.classList.toggle('lt-hidden', p.id !== 'panel-' + tab);
    });
    if(raw === 'evidence' || raw === 'archive'){
      var el = document.getElementById(raw);
      if(el){ if(el.tagName === 'DETAILS') el.open = true; el.scrollIntoView(); }
    }
  }
  document.querySelectorAll('.console-tab-btn').forEach(function(b){
    b.addEventListener('click', function(){
      var t = b.getAttribute('data-ctab');
      if(('#' + t) !== location.hash){ location.hash = t; } else { activate(t); }
    });
  });
  window.addEventListener('hashchange', function(){ activate((location.hash || '#us').replace('#','')); });
  activate((location.hash || '#us').replace('#',''));

  // 看頁面當下檢查：最新一個該收完的交易日，資料有沒有到（只看平日，休市日可能多提醒一次）
  function wall(tz){
    var o = {};
    new Intl.DateTimeFormat('en-CA', {timeZone: tz, year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit', hour12:false})
      .formatToParts(new Date()).forEach(function(x){ o[x.type] = x.value; });
    return o;
  }
  function expected(h, m, tz){
    var n = wall(tz);
    var d = new Date(Date.UTC(+n.year, +n.month - 1, +n.day));
    if((+n.hour % 24) * 60 + (+n.minute) < h * 60 + m) d.setUTCDate(d.getUTCDate() - 1);
    while(d.getUTCDay() === 0 || d.getUTCDay() === 6) d.setUTCDate(d.getUTCDate() - 1);
    return d.toISOString().slice(0, 10);
  }
  document.querySelectorAll('[data-asof]').forEach(function(el){
    var c = el.getAttribute('data-close').split(',');
    var exp = expected(+c[0], +c[1], c[2]), asof = el.getAttribute('data-asof');
    if(asof && asof < exp){
      el.hidden = false;
      el.textContent = '資料只到 ' + asof + '，' + exp + ' 的收盤還沒算進來，下面的動作可能還是舊的。' + exp + ' 休市的話可以忽略。';
    }
  });
})();
</script>
"""


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


DOCS = HERE.parent / "docs"
SCOREBOARD_JSON = DOCS / "market" / "data" / "live_scoreboard.json"
BODY_HTML = DOCS / "long-track-w52-adaptive" / "_body.html"
SCOREBOARD_HTML = DOCS / "long-track" / "_scoreboard_body.html"
PROFILE_JSON = DOCS / "long-track" / "data" / "system_profile.json"
ARENA_JSON = DOCS / "engine" / "arena.json"
ARENA_LEDGER = DOCS / "engine" / "arena-ledger.json"

_CAP = _lr.param("params.capital")
SEAT_PCT = _CAP["us_seat_pct"]     # 美股個股 30% 分 5 席，每席 6%
WD = "一二三四五六日"
MKT = {
    "us": {"name": "美股", "legs": ["QQQ", "SMH"], "hist": "history_us", "close": [23, 0, "America/New_York"],
           "idx_share": _CAP["us_index_share"], "seat_link": ("/cockpit/", "美股看板")},
    "tw": {"name": "台股", "legs": ["0050", "2330"], "hist": "history_tw", "close": [23, 30, "Asia/Taipei"],
           "idx_share": _CAP["tw_index_share"]},  # 持有人 2026-11-08：台股不預設持有個股（2330 在指數部），台股資金全部照水位配
}


def _num(x) -> str:
    return f"{x:.1f}".rstrip("0").rstrip(".") if isinstance(x, (int, float)) else "—"


def _px(x) -> str:
    return f"{x:,.2f}" if isinstance(x, (int, float)) else "—"


def _next_session(ds: str) -> str:
    """資料日的下一個平日（不查休市日）。"""
    d = date.fromisoformat(ds) + timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d.isoformat()


def _md(ds: str) -> str:
    d = date.fromisoformat(ds)
    return f"{d.month:02d}-{d.day:02d}（週{WD[d.weekday()]}）"


def _change(before: float, target: float) -> tuple[str, str]:
    """離散比較在整數空間（千分位）做，避免浮點誤差。"""
    b, t = round(before * 10), round(target * 10)
    if t == b:
        return "不變", "hold"
    return (f"+{_num(abs(t - b) / 10)}", "buy") if t > b else (f"−{_num(abs(t - b) / 10)}", "sell")


def _last_week_ref(hist: list[dict]) -> dict:
    """上週收盤時該持有的那一筆。訊號下一個交易日才成交，所以取該週最後一個交易日的前一筆；
    週五資料一進來，該週就算收完，之後一整週的基準都不變。"""
    if len(hist) < 2:
        return hist[-1] if hist else {}
    last = date.fromisoformat(hist[-1]["date"])
    if last.weekday() == 4:
        end = len(hist) - 1
    else:
        monday = last - timedelta(days=last.weekday())
        end = max((i for i, r in enumerate(hist) if date.fromisoformat(r["date"]) < monday), default=0)
    return hist[max(end - 1, 0)]


def _share(pct_of_index: float, key: str) -> float:
    return round(float(pct_of_index) * MKT[key]["idx_share"], 1)


def _signal_txt(st: dict) -> str:
    txt = f'週{"多" if st.get("w") else "空"}月{"多" if st.get("m") else "空"}'
    return txt + "・下軌接回中" if st.get("tb_info") else txt


def _index_rows(state: dict, key: str) -> list[dict]:
    """指數部每個標的：下單前、上週、應持有（占該市場資金）。"""
    cfg, rows = MKT[key], []
    ref = _last_week_ref(state.get(cfg["hist"]) or [])
    for t in cfg["legs"]:
        k = state.get("tickers", {}).get(t)
        if not k:
            continue
        st = k.get("st") or {}
        target_idx = float(k["executed_pct"])
        before_idx = float(k.get("held_before_pct", target_idx))
        note = f'{_signal_txt(st)}｜水位 {st.get("level_pct", "—")}%'
        if key == "us":
            note += f'｜占指數部 {_num(target_idx)}%'
        last_idx = float(((ref.get("tickers") or {}).get(t) or {}).get("final_pct", before_idx))
        rows.append({"t": t, "before": _share(before_idx, key), "last_week": _share(last_idx, key),
                     "target": _share(target_idx, key), "note": note})
    if key == "us":
        hist = state.get("history_us") or []
        cur = (hist[-1].get("overlay") or {}) if hist else {}
        prev = (hist[-2].get("overlay") or {}) if len(hist) > 1 else cur
        ov = state.get("overlay") or {}
        for t, k, nm in (("IEF", "ief", "公債"), ("GLD", "gld", "黃金")):
            target_idx = float(cur.get(f"{k}_target_pct") or 0.0)
            before_idx = float(prev.get(f"{k}_target_pct") or 0.0)
            o = ov.get(k) or {}
            last_idx = float((ref.get("overlay") or {}).get(f"{k}_target_pct") or 0.0)
            rows.append({"t": t, "before": _share(before_idx, key), "last_week": _share(last_idx, key), "target": _share(target_idx, key),
                         "note": f'{nm}｜週{"多" if o.get("w") else "空"}月{"多" if o.get("m") else "空"}｜占指數部 {_num(target_idx)}%'})
    l2 = state.get("tw_l2") or {}
    if key == "tw" and l2.get("applied"):      # 正二：只看 0050 週線，占指數部最多 20%；今天／昨天／上週的目標都讀 history 的 l2 欄（生效前沒有這欄＝0）
        hist = state.get("history_tw") or []
        cur = (hist[-1].get("l2") or {}) if hist else {}
        prev = (hist[-2].get("l2") or {}) if len(hist) > 1 else {}
        target_idx = float(cur.get("target_pct", l2.get("target_pct") or 0.0))
        rows.append({"t": "00631L", "before": _share(float(prev.get("target_pct") or 0.0), key),
                     "last_week": _share(float((ref.get("l2") or {}).get("target_pct") or 0.0), key), "target": _share(target_idx, key),
                     "note": f'正二｜0050 週{"多" if l2.get("w") else "空"}{"・下軌接回中" if l2.get("tb") else ""}｜水位 {l2.get("level_pct")}%'})
    return rows


def _seat_rows(key: str) -> tuple[list[dict], str, str]:
    """個股席位：回傳 (每列 {t, target, act, note}, 決策日, 補充說明)。台股不預設持有個股，回空列。"""
    rows: list[dict] = []
    if key == "us":
        snap = (_load_json(ARENA_LEDGER).get("snapshots") or [{}])[-1]
        size = {c.get("ticker"): (c.get("lamp") or {}).get("size", 1.0) for c in _load_json(ARENA_JSON).get("core_seats") or []}
        add, out = [], []
        for c in snap.get("changes") or []:
            if c.get("track") == "core":
                add += c.get("in") or []
                out += c.get("out") or []
        rows += [{"t": t, "target": 0.0, "act": "移出", "cls": "sell", "note": ""} for t in out]
        for t in snap.get("core") or []:
            pct = round(SEAT_PCT * float(size.get(t) or 1.0), 1)
            rows.append({"t": t, "target": pct, "act": "新進" if t in add else "不變", "cls": "buy" if t in add else "hold", "note": ""})
        return rows, snap.get("date") or "", ""
    return rows, "", ""


def _next_steps(index_rows: list[dict], seat_rows: list[dict]) -> str:
    parts = [f'{r["t"]} 調到 {_num(r["target"])}%' for r in index_rows if _change(r["before"], r["target"])[1] != "hold"]
    sell = [r["t"].split(" ")[0] for r in seat_rows if r["cls"] == "sell"]
    buy = [r["t"].split(" ")[0] for r in seat_rows if r["cls"] == "buy"]
    seat = "、".join(x for x in (f'賣 {"、".join(sell)}' if sell else "", f'買 {"、".join(buy)}' if buy else "") if x)
    txt = "、".join(parts)
    if seat:
        txt = f"{txt}；個股 {seat}" if txt else f"個股 {seat}"
    return txt or "不用動作"


def _sec(title: str, body: str, cap: str = "") -> str:
    cap_html = f'<p class="lt-cap">{cap}</p>' if cap else ""
    return f'<section class="lt-sec"><h2>{title}</h2>{cap_html}{body}</section>'


def _action_table(key: str, rows: list[dict]) -> str:
    name = MKT[key]["name"]
    head = (f'<thead><tr><th>標的</th><th class="num">應持有</th><th class="num">跟上週</th></tr></thead>')
    body = ""
    for r in rows:
        txt, cls = _change(r["last_week"], r["target"])
        body += (f'<tr><td><b>{r["t"]}</b><span class="lt-sub">{r["note"]}</span></td>'
                 f'<td class="num lt-target">{_num(r["target"])}%</td><td class="num lt-{cls}">{txt}</td></tr>')
    stock = [r for r in rows if r["t"] not in ("IEF", "GLD")]
    b, t = sum(r["last_week"] for r in stock), sum(r["target"] for r in stock)
    txt, cls = _change(b, t)
    total_label = "指數部股票合計" if key == "us" else "股票合計"
    body += (f'<tr class="lt-total"><td>{total_label}</td><td class="num lt-target">{_num(t)}%</td><td class="num lt-{cls}">{txt}</td></tr>')
    if key == "tw":
        txt, cls = _change(100 - b, 100 - t)
        body += (f'<tr class="lt-total"><td>未投入（現金）</td><td class="num lt-target">{_num(round(100 - t, 1))}%</td><td class="num lt-{cls}">{txt}</td></tr>')
    return f'<div class="lt-scroll"><table class="lt-tbl" aria-label="{name}指數部目標持股">{head}<tbody>{body}</tbody></table></div>'


def _seat_table(key: str, rows: list[dict], decided: str, extra: str, index_rows: list[dict]) -> str:
    url, label = MKT[key]["seat_link"]
    body = ""
    idx_target = {r["t"]: r["target"] for r in index_rows}
    for r in rows:
        code = r["t"].split(" ")[0]
        txt = r["note"]
        if code in idx_target:
            both = f'指數部另持有，上表應持有 {_num(idx_target[code])}%，這裡只算席位這一塊'
            txt = f"{txt}。{both}" if txt else both
        note = f'<span class="lt-sub">{html.escape(txt, quote=False)}</span>' if txt else ""
        body += f'<tr><td><b>{html.escape(r["t"], quote=False)}</b>{note}</td><td class="num lt-target">{_num(r["target"])}%</td><td class="num lt-{r["cls"]}">{r["act"]}</td></tr>'
    if not rows:
        body = '<tr><td colspan="3" class="lt-muted">本週沒有持股，也沒有進出。</td></tr>'
    total = sum(r["target"] for r in rows) + sum(r["target"] for r in index_rows)
    # 上週現金＝100－上週指數部各檔－上一期席位。帳本 core_meta 的 size 從 2026-10-31 那筆起才有，缺就留空。
    snaps = _load_json(ARENA_LEDGER).get("snapshots") or []
    prev = (snaps[-2].get("core_meta") or []) if len(snaps) >= 2 else []
    txt, cls = "", "hold"
    if prev and all("size" in m for m in prev):
        before = 100 - sum(r["last_week"] for r in index_rows) - sum(SEAT_PCT * float(m["size"]) for m in prev)
        txt, cls = _change(before, 100 - total)
    body += f'<tr class="lt-total"><td>未投入（現金）</td><td class="num lt-target">{_num(round(100 - total, 1))}%</td><td class="num lt-{cls}">{txt}</td></tr>'
    cap = f'{decided} 週六決策的名單，占{MKT[key]["name"]}資金，每席 {_num(SEAT_PCT)}%。{extra}<a href="{url}">看{label} →</a>'
    return _sec("個股席位", f'<div class="lt-scroll"><table class="lt-tbl"><thead><tr><th>標的</th><th class="num">應持有</th><th class="num">跟上週</th></tr></thead><tbody>{body}</tbody></table></div>', cap)


def _level_rows(t: str, st: dict, overlay: bool = False) -> str:
    w, m = int(st.get("w") or 0), int(st.get("m") or 0)
    # 公債、黃金最多占指數部 20%，水位 100／70／30／0 對應 20／14／6／0
    lv = (lambda a, b: f"占指數部 {14 * a + 6 * b}%") if overlay else (lambda a, b: f"水位 {70 * a + 30 * b}%")
    approx = lambda k: "" if st.get(f"{k}_exact") else "約 "
    conds = [f'週五收盤{"跌破" if w else "站上"} {approx("w")}{_px(st.get("w_thr"))} → {lv(1 - w, m)}',
             f'月底收盤{"跌破" if m else "站上"} {approx("m")}{_px(st.get("m_thr"))} → {lv(w, 1 - m)}']
    tb = st.get("tb_info")
    if tb and isinstance(tb.get("ma"), (int, float)):
        conds.insert(1, f'週五收盤回到 20 週均線 約 {_px(tb["ma"])} → 水位 30%')
    return f'<tr><td><b>{t}</b></td><td>{"<br>".join(conds)}</td></tr>'


def _l2_level_row(l2: dict) -> str:
    thr = f'{"" if l2.get("w_exact") else "約 "}{_px(l2["w_thr"])}'
    if l2.get("w"):
        conds = [f"週五收盤跌破 {thr} → 水位 0%"]
    else:
        conds = [f"週五收盤站上 {thr} → 水位 100%"]
        if l2.get("tb"):
            conds.append(f'週五收盤回到 20 週均線 約 {_px(l2["ma"])} → 水位 0%')
        elif l2.get("lower") is not None:
            conds.append(f'週五收盤跌破 20 週下軌 約 {_px(l2["lower"])} → 水位 30%')
    tag = "" if l2.get("applied") else f'<span class="lt-sub">{l2.get("active_from")} 收盤起生效</span>'
    return f'<tr><td><b>00631L</b>{tag}</td><td>{"<br>".join(conds)}</td></tr>'


def _levels_table(state: dict, key: str) -> str:
    rows = ""
    for t in MKT[key]["legs"]:
        k = state.get("tickers", {}).get(t) or {}
        if k.get("st"):
            rows += _level_rows(t, k["st"])
    if key == "us":
        ov = state.get("overlay") or {}
        for t, k in (("IEF", "ief"), ("GLD", "gld")):
            if ov.get(k):
                rows += _level_rows(t, {**ov[k], "tb_info": None, "w_exact": ov[k].get("w_exact", True), "m_exact": ov[k].get("m_exact", True)}, overlay=True)
    cap = "每項只列下一個會改變水位的條件，先到的為準。週線門檻每週會小幅移動，以週五收盤為準。水位 30 時週收盤跌破 2.5 個標準差下軌，改為 50。"
    l2 = state.get("tw_l2") or {}
    if key == "tw" and l2.get("w_thr") is not None:
        rows += _l2_level_row(l2)
        cap += "00631L 只看 0050 週線，價位都是 0050 的價格，門檻是 0050 週線，不看月線。"
    return _sec("下週會動的價位", f'<div class="lt-scroll"><table class="lt-tbl"><thead><tr><th>標的</th><th>條件與新水位</th></tr></thead><tbody>{rows}</tbody></table></div>', cap)


def _balance(frag: str) -> str:
    """切出來的片段補齊或去掉多餘的 div 收尾。"""
    opened = len(re.findall(r"<div\b", frag))
    closed = len(re.findall(r"</div>", frag))
    if closed > opened:
        for _ in range(closed - opened):
            k = frag.rfind("</div>")
            frag = frag[:k] + frag[k + 6:]
    return frag + "</div>" * max(0, opened - closed)


def _scope_css(css: str, scope: str) -> tuple[str, str]:
    """把樣式表加上範圍前綴。回傳 (全域的 :root 變數, 加了前綴的其餘規則)。"""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    tokens, rules, i = [], [], 0
    while True:
        j = css.find("{", i)
        if j < 0:
            break
        head, depth, k = css[i:j].strip(), 1, j + 1
        while k < len(css) and depth:
            depth += (css[k] == "{") - (css[k] == "}")
            k += 1
        block = css[j + 1:k - 1]
        i = k
        if head.startswith("@media (prefers-color-scheme"):
            continue  # 頁面只有淺色，跟著系統深色的規則不帶進來
        if head.startswith(("@media", "@supports")):
            t, r = _scope_css(block, scope)
            if t:
                tokens.append(f"{head}{{{t}}}")
            if r:
                rules.append(f"{head}{{{r}}}")
        elif head.startswith("@"):
            rules.append(f"{head}{{{block}}}")
        else:
            root, scoped = [], []
            for sel in (x.strip() for x in head.split(",")):
                m = re.match(r"^(:root|html)(\[[^\]]*\])?(?:\s+(.*))?$", sel)
                if sel == "body":
                    scoped.append(scope)
                elif sel.startswith("body "):
                    scoped.append(f"{scope} {sel[5:]}")
                elif m and not m.group(3):
                    root.append(sel)
                elif m:
                    scoped.append(f'{m.group(1)}{m.group(2) or ""} {scope} {m.group(3)}')
                else:
                    scoped.append(f"{scope} {sel}")
            if root:
                tokens.append(f'{",".join(root)}{{{block}}}')
            if scoped:
                rules.append(f'{",".join(scoped)}{{{block}}}')
    return "".join(tokens), "".join(rules)


def _detail_parts() -> dict:
    """從實單明細頁切出兩市場的圖表區塊、規則區塊、樣式與圖表程式。切不到回傳空字串。"""
    empty = {"us": "", "tw": "", "rules": "", "tokens": "", "css": "", "js": ""}
    try:
        s = BODY_HTML.read_text(encoding="utf-8")
    except OSError:
        return empty
    us, tw, rule = s.find('<div class="mkt-section" id="mkt-us"'), s.find('<div class="mkt-section" id="mkt-tw"'), s.find("規則說明（點開看")
    src = s.find("<script src=")
    if not (0 <= us < tw < rule < src):
        return empty
    rule = s.rfind('<div class="card">', 0, rule)
    end = s.find("<footer", rule)      # 規則區塊到頁尾為止，頁尾和外層容器不要帶進來
    end = end if 0 <= end < src else src
    # 換掉 class：明細頁的 switchMarket 只切 .mkt-section，這裡兩市場分放在各自分頁，不讓它動
    fix = lambda f: _balance(f).replace('class="mkt-section"', 'class="lt-mkt-section"')
    style = re.search(r"<style[^>]*>(.*?)</style>", s, flags=re.S)
    tokens, css = _scope_css(style.group(1), ".lt-detail") if style else ("", "")
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", s[src:], flags=re.S)
    js = max(scripts, key=len) if scripts else ""
    lib = re.search(r'<script src="([^"]+lightweight-charts[^"]+)"', s[src:])
    return {"us": fix(s[us:tw]), "tw": fix(s[tw:rule]), "rules": _balance(s[rule:end]), "tokens": tokens, "css": css,
            "js": f'<script src="{lib.group(1)}"></script>\n<script>{js}</script>' if lib and js else ""}


LIVE_NOTE = ("同風險基準是同標的一直抱著、只放一部分資金、其餘放現金，讓回撤跟系統相近再比；同報酬基準是放到報酬跟系統相近。"
             "每個月比一次，滿 20 筆才判定，判定只供檢討，不觸發買賣。")


def _plain_scoreboard(f: str) -> str:
    """記分板片段的欄名換白話，只動顯示文字。"""
    for a, b in (("系統 vs B-mdd（同風險稀釋基準，主判準）", "對同風險基準（主要判準）"),
                 ("系統 vs B-cagr（同報酬稀釋基準，並列）", "對同報酬基準"),
                 ("累積差 vs B-mdd", "領先同風險基準（百分點）"), ("累積差 vs B-cagr", "領先同報酬基準（百分點）"),
                 ("B-mdd 基準報酬", "同風險基準報酬"), ("執行層變化（水位）", "水位變化"),
                 ("<th>日期</th><th>檔</th>", "<th>下單日</th><th>檔</th>"),
                 ("S-60（固定 60% B&amp;H） vs 系統", "六成一直抱著對系統"), ("S-60（固定 60% B&amp;H）", "六成一直抱著"),
                 (r'"S-60\uff08\u56fa\u5b9a 60% B&H\uff09"', '"六成一直抱著"')):
        f = f.replace(a, b)
    f = f.replace("'B-mdd（k=稀釋）'", "'同風險基準'").replace("'B-cagr（稀釋）'", "'同報酬基準'")
    f = re.sub(r"<p class='lsb-note'>兩市場合併.*?</p>", "", f, flags=re.S)
    # 手機上照寬高比只剩 81px 高，圖建立之前先把畫布比例改高
    f = re.sub(r'(<canvas id="lsb-[^"]+" height="90"></canvas>)',
               r"\1<script>if(innerWidth<640)document.currentScript.previousElementSibling.height=200;</script>", f)
    f = re.sub(r'(class="lsb-v">-?\d+\.\d{2})\d{2}<', r"\1<", f)
    return re.sub(r"(-?\d+\.\d)\d{3}%", r"\1%", f)


def _live_summary(key: str) -> str:
    """上線以來報酬、回撤，跟同期一直抱著比。缺資料回空字串。"""
    m = (_load_json(SCOREBOARD_JSON).get("markets") or {}).get(key) or {}
    def stats(k):
        nav = [x["nav"] for x in m.get(k) or []]
        if len(nav) < 2:
            return None
        peak, worst = nav[0], 0.0
        for v in nav:
            peak = max(peak, v)
            worst = min(worst, v / peak - 1)
        return (nav[-1] / nav[0] - 1) * 100, worst * 100
    a, b = stats("nav_sys"), stats("nav_raw_bh")
    if not a or not b:
        return ""
    return (f'{m.get("inception", "")} 起累計 {a[0]:+.1f}%，最大回撤 {a[1]:.1f}%。'
            f'同期一直抱著 {b[0]:+.1f}%，最大回撤 {b[1]:.1f}%。')


def _scoreboard_parts() -> dict:
    """從記分板片段切出美股、台股實盤紀錄與兩市場影子帳戶。"""
    empty = {"us": "", "tw": "", "us_shadow": "", "tw_shadow": "", "plain": "", "prereg": "", "css": ""}
    try:
        s = SCOREBOARD_HTML.read_text(encoding="utf-8")
    except OSError:
        return empty
    marks = [m.start() for m in re.finditer(r'<div class="lsb-market">', s)]
    h2, det = s.find('<h2 style="margin:1.4rem'), s.find("<details")
    if len(marks) != 4 or not (marks[1] < h2 < marks[2]) or det < marks[3]:
        return empty
    style = re.search(r"<style[^>]*>(.*?)</style>", s, flags=re.S)
    tokens, css = _scope_css(style.group(1), ".lt-lsb") if style else ("", "")
    first = re.search(r'<div class="lsb-plain">(.*?)</div>', s, flags=re.S)
    end = s.find("</body>")
    return {"us": _plain_scoreboard(_balance(s[marks[0]:marks[1]])), "tw": _plain_scoreboard(_balance(s[marks[1]:h2])),
            "us_shadow": _plain_scoreboard(_balance(s[marks[2]:marks[3]])), "tw_shadow": _plain_scoreboard(_balance(s[marks[3]:det])), "plain": first.group(1) if first else "", "prereg": _balance(s[det:end]), "css": tokens + css}


def _perf_block(key: str) -> str:
    d = _load_json(PROFILE_JSON)
    m = d.get(key)
    link = '<a href="/long-track/live-system-profile.html">看完整回測報告 →</a>'
    if not isinstance(m, dict):
        return _sec("系統績效", f"<p>{link}</p>")
    def v(k, unit=""):
        x = m.get(k)
        return f"{x:.2f}{unit}" if isinstance(x, (int, float)) else "—"
    rows = "".join(f'<tr><td>{n}</td><td class="num lt-target">{v(k, u)}</td><td class="num">{v("bh_" + k, u)}</td></tr>'
                   for n, k, u in (("年化報酬", "cagr", "%"), ("最大回撤", "mdd", "%"), ("夏普值（每承受一單位波動多賺多少）", "sharpe", ""),
                                   ("年化報酬除以最大回撤（Calmar）", "calmar", "")))
    t1 = f'<div class="lt-scroll"><table class="lt-tbl"><thead><tr><th></th><th class="num">系統</th><th class="num">一直抱著</th></tr></thead><tbody>{rows}</tbody></table></div>'
    lay = ""
    for k, n in (("week", "週線那塊"), ("month", "月線那塊"), ("takeback", "下軌接回")):
        x = (m.get("layers") or {}).get(k) or {}
        g = lambda f, dec=2, u="": f"{x[f]:.{dec}f}{u}" if isinstance(x.get(f), (int, float)) else "—"
        lay += (f'<tr><td>{n}</td><td class="num">{g("n", 0)}</td><td class="num">{g("win_rate", 0, "%")}</td><td class="num">{g("payoff")}</td>'
                f'<td class="num">{g("avg_hold_days", 0)}</td><td class="num">{g("max_lose_streak", 0)}</td></tr>')
    t2 = (f'<h3 class="lt-h3">逐筆交易（只算做完的，筆數少的那塊只當描述）</h3><div class="lt-scroll"><table class="lt-tbl lt-nowrap"><thead><tr><th></th><th class="num">筆數</th><th class="num">勝率</th>'
          f'<th class="num">賺賠比</th><th class="num">平均持有（天）</th><th class="num">最長連虧</th></tr></thead><tbody>{lay}</tbody></table></div>')
    alt = m.get("alt") or {}
    alt_txt = ""
    if alt:
        alt_txt = (f'不含 2008 年（{alt["start"]} 起）：系統年化 {alt["cagr"]:.2f}%、最大回撤 {alt["mdd"]:.1f}%、夏普值 {alt["sharpe"]:.2f}，'
                   f'一直抱著 {alt["bh_cagr"]:.2f}%、{alt["bh_mdd"]:.1f}%、{alt["bh_sharpe"]:.2f}。')
    cap = (f'{m.get("start", "")} 起到 {d.get("asof", "")}，訊號用{(d.get("signal_basis") or {}).get(key, "")} K 線。'
           f'平均持股 {m.get("avg_exposure", 0):.0f}%{"（股票曝險，正二按 2 倍算）" if key == "tw" else ""}，一年下單 {m.get("adj_days_per_yr", 0):.1f} 天，成本每年 {m.get("cost_per_yr", 0):.2f} 個百分點。{alt_txt}'
           f'現行規則套回整段歷史算出來的，參數與接回都是看過結果才定，當成上限看。{link}')
    return _sec("系統績效", t1 + t2, cap)


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
    intro = (f'<div class="ev-intro">這些檢驗大多做在 2026-11-04 以前的 W52 規則上，共 {len(urls)} 頁，先看第一頁的總覽。現行 Supertrend 的回測看<a href="/long-track/live-system-profile.html">完整回測報告</a>。'
             f'每頁的結論和判斷依據都寫在頁內；網址在回測區，狀態標籤與回測區首頁一致。</div>')
    return (f'<div class="grp live" id="evidence"><div class="grp-h">實盤證據</div>{intro}{body}{dead_html}</div>\n')


LAST_WEEK_NOTE = "「跟上週」是應持有減上週收盤時的應持有，單位是百分點。"


def render_market_panel(key: str, state: dict, idx: list, seats: tuple, dp: dict, sb: dict) -> str:
    cfg = MKT[key]
    hist = state.get(cfg["hist"]) or []
    asof = hist[-1]["date"] if hist else ""
    h, m, tz = cfg["close"]
    stale = f'<div class="lt-stale" hidden data-asof="{asof}" data-close="{h},{m},{tz}"></div>'
    when = f'資料到 {_md(asof)}。下單日 {_md(_next_session(asof))}（遇休市順延），一次調到「應持有」。' if asof else ""
    if key == "us":
        cap = f'{when}百分比都是占美股總資金：指數部 70%、個股 30%。{LAST_WEEK_NOTE}'
    else:
        cap = f'{when}百分比都是占台股總資金。{LAST_WEEK_NOTE}台股照水位持有 00631L 20%、0050 40%、2330 40%（2026-11-10 收盤的訊號起，之前 0050、2330 各半），其餘放現金。00631L 是 2 倍產品，這裡的百分比是占資金的比例，不是曝險。<a href="/cockpit-tw/">台股席位</a>只當研究名單，不算預設持股。'
    rows, decided, extra = seats
    parts = [_sec("每個標的應持有", stale + _action_table(key, idx), cap)]
    if key == "us":
        parts.append(_seat_table(key, rows, decided, extra, idx))
    parts.append(_levels_table(state, key))
    if sb.get(key):
        parts.append(_sec("實盤紀錄", f'<div class="lt-lsb">{sb[key]}</div>', f'{_live_summary(key)}{sb.get("plain", "")}{LIVE_NOTE}'))
    else:
        parts.append(_sec("實盤紀錄", '<p><a href="/long-track/_scoreboard_body.html">看記分板 →</a></p>'))
    parts.append(_perf_block(key))
    if dp.get(key):
        parts.append(f'<details class="lt-sec lt-fold" open data-lt-close><summary>一年水位變化、K 棒軌跡</summary><div class="lt-detail">{dp[key]}</div></details>')
    else:
        parts.append(_sec("一年水位變化、K 棒軌跡", '<p><a href="/long-track-w52-adaptive/_body.html">看明細頁 →</a></p>'))
    if dp.get("rules"):
        parts.append(f'<div class="lt-detail">{dp["rules"]}</div>')
    return f'<div class="lt-panel" id="panel-{key}">{"".join(parts)}</div>'


def render_ref_panel(sb: dict) -> str:
    parts = []
    if sb.get("us_shadow"):
        parts.append(_sec("影子帳戶", f'<div class="lt-lsb">{sb["us_shadow"]}{sb["tw_shadow"]}</div>',
                          "同標的各半一直抱著、只放六成、其餘放現金的帳戶，每月調回六成。用來看系統有沒有輸給這種最簡單的做法，只是參考，不觸發動作。"))
    parts.append(f'<div class="grp shadow"><div class="grp-h">還在測的</div>{render_testing_table(TESTING)}</div>')
    parts.append(render_evidence())
    parts.append(render_archive())
    parts.append(f'<details class="ov-history"><summary>沿革</summary><div class="plain-box" style="margin-top:.6rem">'
                 f'<span class="pb-tag">💬 白話</span><span class="pb-body">{PLAIN}</span></div></details>')
    if sb.get("prereg"):
        parts.append(f'<div class="lt-lsb" style="margin-top:.9rem">{sb["prereg"]}</div>')
    links = ('<ul class="lt-links"><li><a href="/long-track/live-system-profile.html">實單主系統回測報告</a></li>'
             '<li><a href="/backtest/supertrend_vs_live/">Supertrend 對 W52 的比較</a></li>'
             '<li><a href="/long-track/why-qqq70-smh30.html">為什麼改 QQQ 70／SMH 30</a></li>'
             '<li><a href="/long-track-w52-adaptive/w52.html">舊規則 W52 對照線</a></li>'
             '<li><a href="/track-record/">個股裁決實績</a></li></ul>')
    parts.append(f'<div style="margin-top:.9rem">{_sec("相關頁面", links)}</div>')
    return f'<div class="lt-panel" id="panel-ref">{"".join(parts)}</div>'


def render() -> str:
    state = _load_json(STATE_JSON)
    dp, sb = _detail_parts(), _scoreboard_parts()
    data = {k: (_index_rows(state, k), _seat_rows(k)) for k in MKT}
    next_rows = ""
    for k, (idx, seats) in data.items():
        hist = state.get(MKT[k]["hist"]) or []
        day = f'<small>下單日 {_md(_next_session(hist[-1]["date"]))}</small>' if hist else ""
        next_rows += f'<div class="lt-next-row"><b>{MKT[k]["name"]}</b><span>{_next_steps(idx, seats[0])}</span>{day}</div>'
    panels = "".join(render_market_panel(k, state, data[k][0], data[k][1], dp, sb) for k in MKT) + render_ref_panel(sb)
    extra_css = dp["tokens"] + dp["css"] + sb["css"]
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>系統主控台 | InvestMQuest Research</title>
<link rel="stylesheet" href="/assets/imq-base.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
<style>{CSS}{extra_css}</style>
</head>
<body>
{NAV_BLOCK}
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / 系統主控台</div>
  <h1>系統主控台</h1>
  <div class="sub">實單主系統：每個標的下一個交易日該持有多少，美股、台股分開看。</div>
</div></div>
<div class="container">
<div class="lt-next"><div class="lt-next-h">下一步（占該市場總資金）</div>{next_rows}</div>
<div class="console-tabbar" role="tablist">
  <button type="button" class="console-tab-btn" data-ctab="us" role="tab">美股</button>
  <button type="button" class="console-tab-btn" data-ctab="tw" role="tab">台股</button>
  <button type="button" class="console-tab-btn" data-ctab="ref" role="tab">對照與歸檔</button>
</div>
{panels}
</div>
<footer><div class="container">&copy; 2026 InvestMQuest Research · 系統主控台 · 僅供研究參考</div></footer>
{dp["js"]}
{CONSOLE_JS}
</body>
</html>"""


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Written {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
