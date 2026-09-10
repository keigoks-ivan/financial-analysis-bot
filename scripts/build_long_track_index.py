#!/usr/bin/env python3
"""系統主控台 /long-track/ 產生器（fab）— 2026-08-23 系統群整併，2026-09-10 總覽儀表板化＋分頁重分組。

五分頁單一入口：
  #overview   總覽        — 頂部「今天」儀表板（讀 state.json／live_scoreboard.json，見
                            render_today_strip；今天曝險＋影子帳戶一覽，不重算任何數字）
                            ＋家族地圖（實單主系統大卡片／影子對照＋前瞻 OOS 候選一行式／
                            已退役凍結對照收進單一 details／沿革白話盒收進 details），inline
  #live       美股即時    — iframe 嵌入 /long-track-w52-adaptive/_body.html
  #scoreboard 記分板      — iframe 嵌入 /long-track/_scoreboard_body.html（2026-09-10 由
                            #live 拆出獨立分頁；#live 內保留一個跳轉連結）
  #positions  個股：持倉週掃 — iframe 嵌入 /pm/_body.html
  #record     個股：裁決實績 — iframe 嵌入 /track-record/_body.html

舊 3 個獨立 URL（/long-track-w52-adaptive/、/pm/、/track-record/）已改為
meta-refresh redirect stub，指回對應分頁錨點；三個來源頁的 builder
（update_long_track_w52_adaptive.py／build_pm_index.py／build_track_record.py）
改產 nav-less _body.html 片段。stub／片段皆已加入 scripts/site_nav.py 的
SKIP_FILES。/long-track-w52-adaptive/leverage.html 與 tw-semivol.html 維持
獨立完整頁，不在此整併範圍內。

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

# 每組＝(分類、色、突出、系統清單)；系統 dict：name／url／one／status／freq／email
GROUPS = [
    ("實單主系統", "live", True, [
        {"name": "W52 × 自適應波動率 cap 1.5（美 + 台）", "url": "/long-track-w52-adaptive/",
         "one": "兩市場各 70% 指數部＝W52 週線閘門 × 自適應波動率 × cap 1.5 ＋ A2 執行層。"
                "<b>2026-07-18 起接棒為實單主系統</b>。",
         "status": ("實單", "live"), "freq": "每交易日 × 2（台／美收盤後）", "email": "✅ 有"},
    ]),
    ("影子對照（同引擎、不上槓桿）", "shadow", False, [
        {"name": "W52 × 自適應波動率 cap 1.0 影子", "url": "/long-track-w52-adaptive/leverage.html",
         "one": "同引擎的 cap 1.0（不上槓桿）影子線，供槓桿 vs 不槓桿對照。",
         "status": ("影子對照", "shadow"), "freq": "每交易日 × 2", "email": "❌（併入主系統通知）"},
    ]),
    ("前瞻 OOS 候選（決策前研究通過、尚非實單）", "cand", False, [
        {"name": "🥇 GLD 金 sleeve", "url": "/long-track-gld/",
         "one": "非股票 sleeve 決策前研究通過後的前瞻紙上追蹤（單腿 GLD、cap 1.0、"
                "W52×自適應＋A2）。長樣本 1976-2026 含 20 年熊市壓力測試通過。<b>尚非實單</b>。",
         "status": ("前瞻 OOS・候選", "cand"), "freq": "每交易日（美股收盤後）", "email": "✅（可行動變化）"},
        {"name": "🐢 商品 Sleeve（80/20 組合）", "url": "/turtle-sleeve/",
         "one": "GLD/USO→期貨 商品 sleeve 疊上 STX50 的 80/20 組合曝險，OOS 並行追蹤。",
         "status": ("前瞻 OOS・候選", "cand"), "freq": "每交易日", "email": "—"},
        {"name": "🧩 F70：A 70%＋D1（TLT／GLD／DBC）30%", "url": "/backtest/f_comfort/",
         "one": "擁有者 2026-09-10 選定的 paper 候選；記分板 S-F70 影子帳戶每日追蹤，見 #scoreboard；"
                "D1 拿掉 SPY 因為 A 已是美股。",
         "status": ("前瞻 OOS・候選", "cand"), "freq": "每交易日（隨 W52 主系統更新）", "email": "—"},
    ]),
    ("已退役・凍結對照（被 W52×自適應取代）", "ret", False, [
        {"name": "STX50（SMH/QQQ 美股）", "url": "/long-track-smh/",
         "one": "2026-07-18 由 W52×自適應接棒、2026-07-23 停更（cron 已移除）。",
         "status": ("已凍結・2026-07-23 停更", "ret"), "freq": "已停更（僅手動）", "email": "—"},
        {"name": "E3（0050/2330 台股）", "url": "/long-track-tw/",
         "one": "2026-07-18 由 W52×自適應接棒、2026-07-23 停更（cron 已移除）。",
         "status": ("已凍結・2026-07-23 停更", "ret"), "freq": "已停更（僅手動）", "email": "—"},
        {"name": "0050 + 2330 固定 σ（歸檔）", "url": "/long-track-tw-vt/",
         "one": "固定 σ 版波動率目標，vt 家族早期研究線、已歸檔對照。",
         "status": ("凍結對照", "ret"), "freq": "歸檔", "email": "—"},
        {"name": "自適應美台總覽（歸檔）", "url": "/long-track-adaptive-vt/",
         "one": "自適應 σ 美台總覽，vt 家族研究線、已歸檔對照。",
         "status": ("凍結對照", "ret"), "freq": "歸檔", "email": "—"},
        {"name": "QQQ + SMH 長軌 × 套袖（歸檔）", "url": "/long-track-qs-vt/",
         "one": "週線長軌閘門 × 波動率套袖組合，vt 家族研究線、已歸檔對照。",
         "status": ("凍結對照", "ret"), "freq": "歸檔", "email": "—"},
        {"name": "六狀態機（SMH/QQQ）", "url": "/backtest/six_state/status/",
         "one": "早期六態機引擎，已退役、僅手動；被 W52×自適應取代。",
         "status": ("凍結對照", "ret"), "freq": "手動", "email": "—"},
    ]),
]

PLAIN = ('這個家族的沿革（白話）：早期實單主線用「六狀態機」與「STX50／E3」兩套引擎；'
         '<b>2026-07-18 起改由「W52 週線閘門 × 自適應波動率 × cap 1.5 ＋ A2 執行層」接棒為實單主系統</b>'
         '（美台兩市場各 70% 指數部），舊引擎降為凍結對照。'
         'GLD 金 sleeve、商品 sleeve 與 F70（A 70%＋D1 拿掉 SPY 30%）是決策前研究通過後的<b>前瞻候選</b>'
         '——還在紙上測、尚未進實單。')

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
.ov-retired{margin-top:1.6rem}
.ov-retired summary{cursor:pointer;font-weight:800;font-size:.78rem;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);
  padding-left:.6rem;border-left:4px solid var(--grey)}
.retired-list{margin-top:.6rem}
.retired-row{display:flex;justify-content:space-between;gap:.8rem;padding:.45rem .3rem;border-bottom:1px solid var(--border);
  font-size:.82rem;color:inherit}
.retired-row:hover{color:var(--brand)}
.retired-row .rr-meta{color:var(--muted);flex:0 0 auto;white-space:nowrap}

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
  var TABS = ['overview','live','scoreboard','positions','record'];
  // 2026-09-10 分頁重新分組：live（美股即時）與 scoreboard（記分板）各自獨立分頁
  // （先前 F1 修法把兩個 iframe 疊在同一個 live 分頁下，本次拆開，#live／#positions／
  // #record 舊錨點維持可用，新增 #scoreboard）。每個 tab 對應一個 id 陣列。
  var FRAME_ID = {live:['live-frame'], scoreboard:['scoreboard-frame'],
                  positions:['positions-frame'], record:['record-frame']};

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
    if(TABS.indexOf(tab) < 0) tab = 'overview';
    document.querySelectorAll('.console-tab-btn').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-ctab') === tab);
    });
    document.querySelectorAll('.console-tab-panel').forEach(function(p){
      p.classList.toggle('active', p.id === 'panel-' + tab);
    });
    if(frames[tab]) ensureLoaded(tab);
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


def render_overview_body() -> str:
    """總覽分頁本體（家族地圖）— 獨立於 page chrome，供 console 殼內嵌 Tab 1。
    2026-09-10 改版：頂部加「今天」儀表板（見 render_today_strip），實單主系統維持
    大卡片，影子對照／前瞻 OOS 候選改一行式，已退役／凍結對照收進單一 details，
    沿革白話盒移到底部 details。"""
    today_strip = render_today_strip()
    lede = ('<div class="ov-lede">看這三件事就好：上面「今天」區塊的<b>今天曝險</b>'
            '（目標／現持曝險與各腿在場／出場）、<b>最近一次變動</b>（哪一天、哪一腿調整了多少）、'
            '下面影子帳戶表的<b>影子帳戶怎麼說</b>（累計淨值差與 SPRT 判定是否已經足夠判斷現行規則比對照組好）。</div>')

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

    for title, cls, _, systems in GROUPS[1:3]:      # 影子對照、前瞻 OOS 候選 → 一行式
        rows = ""
        for s in systems:
            st_txt, st_cls = s["status"]
            rows += (
                f'<a class="sysrow" href="{s["url"]}">'
                f'<span class="sysrow-name">{s["name"]}</span>'
                f'<span class="pill {st_cls}">{st_txt}</span>'
                f'<span class="sysrow-one">{s["one"]}</span>'
                f'<span class="arr">→</span></a>')
        groups_html += f'<div class="grp {cls}"><div class="grp-h">{title}</div>{rows}</div>\n'

    ret_title, _, _, ret_systems = GROUPS[3]
    ret_rows = ""
    for s in ret_systems:
        st_txt, _ = s["status"]
        ret_rows += (f'<a class="retired-row" href="{s["url"]}">'
                     f'<span>{s["name"]}</span><span class="rr-meta">{st_txt}</span></a>')
    retired_html = (f'<details class="ov-retired"><summary>{ret_title.split("（")[0]}'
                    f'（{len(ret_systems)}）</summary><div class="retired-list">{ret_rows}</div></details>')

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
  <div class="sub">總覽 · 美股即時 · 記分板 · 個股：持倉週掃 · 個股：裁決實績 — 五分頁單一入口，一頁看清整個追蹤家族的定位、現況與紀律紀錄。</div>
</div></div>
<div class="container">
<div class="console-tabbar" role="tablist">
  <button type="button" class="console-tab-btn" data-ctab="overview" role="tab">總覽</button>
  <button type="button" class="console-tab-btn" data-ctab="live" role="tab">美股即時</button>
  <button type="button" class="console-tab-btn" data-ctab="scoreboard" role="tab">記分板</button>
  <button type="button" class="console-tab-btn" data-ctab="positions" role="tab">個股：持倉週掃</button>
  <button type="button" class="console-tab-btn" data-ctab="record" role="tab">個股：裁決實績</button>
</div>
<div class="console-tab-panel" id="panel-overview">{overview_body}</div>
<div class="console-tab-panel" id="panel-live">
  <p class="console-embed-note">W52 × 自適應波動率 cap 1.5（美＋台）· 2026-07-18 起實單主系統 · <a href="/long-track-w52-adaptive/">獨立頁</a> · <a href="/backtest/live_system_evidence/">這套系統的證據總覽（12 頁，白話）→</a> · <a href="#scoreboard">跳到記分板 →</a></p>
  <iframe class="console-embed-frame" id="live-frame" data-src="/long-track-w52-adaptive/_body.html" title="實單主系統" scrolling="no" loading="lazy"></iframe>
</div>
<div class="console-tab-panel" id="panel-scoreboard">
  <p class="console-embed-note">實單前瞻記分板（NAV／回撤／基準差／資料缺口，PREREG 2026-09-05） · <a href="/long-track/_scoreboard_body.html">獨立片段</a></p>
  <iframe class="console-embed-frame" id="scoreboard-frame" data-src="/long-track/_scoreboard_body.html" title="實單前瞻記分板" scrolling="no" loading="lazy"></iframe>
</div>
<div class="console-tab-panel" id="panel-positions">
  <p class="console-embed-note">逐一檢查每個持倉與近期研究 DD 的否證指標、催化劑時程、thesis 老化 · <a href="/pm/">獨立頁</a></p>
  <iframe class="console-embed-frame" id="positions-frame" data-src="/pm/_body.html" title="持倉週掃" scrolling="no" loading="lazy"></iframe>
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
