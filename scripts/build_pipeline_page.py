#!/usr/bin/env python3
"""Pipeline 漏斗總覽頁 — 個股部 25% 投資流程的活數字單頁.

設計 source-of-truth: docs/_handoff_stock_sleeve_pipeline_20260703.md（Task 4）

一頁呈現整條漏斗：發現 → 資格閘 → 三軌射擊名單（＋觀望複審隊列）→ 板機（＋態②否決對照組）
→ 回看鏡（發現力稽核）→ 隱私線。
資料**全部來自既有 JSON**，不新增採集：
  - docs/dd-screener/latest.json         （宇宙 / 資格閘 / 核心軌 / 結構軌）
  - docs/dd-screener/cyclical-track.json （衛星·循環軌，Task 2 輸出）
  - docs/dd-screener/sop-funnel/latest.json（板機現況）
  - docs/dd-screener/sop-funnel/ledger.json（態②否決計數）
  - docs/dd-screener/pre_id_scan.json    （六燈盲區 coverage）
  - data/weekly_cache/{T}.json           （回看鏡 12M/24M 週線報酬）

**資格閘自算口徑**（不依賴 latest.json 的 pass_count，Task 1 並行改動中該欄口徑可能新舊不一）：
  fail_criteria 去掉 'de' 後為空  且  moat_grade∈{S,A,B}  且  moat_trend≠↓
  D/E>0.7 顯示 ⚠ badge（advisory，不擋）。

Usage:
  python3 scripts/build_pipeline_page.py
  python3 scripts/build_pipeline_page.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import DD_SCREENER_SUBNAV, build_subnav, full_nav_block  # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DDS = ROOT / "docs" / "dd-screener"
LATEST_JSON = DDS / "latest.json"
CYCLICAL_JSON = DDS / "cyclical-track.json"
SOP_LATEST = DDS / "sop-funnel" / "latest.json"
SOP_LEDGER = DDS / "sop-funnel" / "ledger.json"
PRE_ID_SCAN = DDS / "pre_id_scan.json"
WEEKLY_CACHE_DIR = ROOT / "data" / "weekly_cache"
HTML_OUT = DDS / "pipeline.html"

NAV_BLOCK = full_nav_block(
    "pick", "pipe", build_subnav(DD_SCREENER_SUBNAV, "/dd-screener/pipeline.html")
)

TAIPEI_TZ = timezone(timedelta(hours=8))

# ── 常數（口徑，與 build_cyclical_track / handoff 對齊）────────────────────────
QUALITY_MOAT_GRADES = {"S", "A", "B"}
DE_WARN_THRESHOLD = 0.7          # D/E 警示線（advisory，不擋）
DD_STALE_DAYS = 90               # DD>90 天視為過舊（回看鏡盲區判定）
LOOKBACK_TOP_N = 30              # 回看鏡 top N
LEADERBOARD_TOP_N = 25           # 全宇宙潛力榜 top N
HEUR_EV5Y_ARTIFACT_CAP = 60.0    # heur 來源 EV5y 超過此值＝artifact，抽出排行單列人工檢視
STRUCT_BULL_MULT = 15.0          # 結構軌排序：bull 倍數權重
CORE_CAP_PCT = 10.0              # 核心單檔上限（個股部淨值）
SATELLITE_CAP_PCT = 5.0          # 衛星單檔上限
CORE_SLOTS = 5                   # 核心席位硬上限（章程 core ≤5）；超出落板凳

# ── 觀望複審隊列（裁決保鮮迴路，2026-07-04）──────────────────────────────────
# 門檻全部沿用既有拍板值，不引入新調參：miss＝結算警報線（knowledge/ --calibration 同口徑）、
# EPS 上修＝循環軌資格口徑（handoff Task 2）。命中＝裁決回爐複審，不是買進訊號。
REREVIEW_MISS_PCT = 30.0         # 錯過成本：裁決後現價漲逾此值
REREVIEW_EPS_FY1_PCT = 5.0       # FY+1 EPS 單月上修門檻
REREVIEW_EPS2Y_PP = 3.0          # eps2y 修正 pp 門檻


def is_core_role(s: dict) -> bool:
    """核心角色＝角色欄含「核心持倉」（涵蓋無條件核心持倉與條件式核心持倉）。"""
    return "核心持倉" in (s.get("dca_role") or "")


def _is_unconditional_core(s: dict) -> bool:
    return (s.get("dca_role") or "") == "核心持倉"
CYCLICAL_CAP_PCT = 3.0           # 循環衛星單檔上限


def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def _fmt_stamp(iso_str: Optional[str]) -> str:
    if not iso_str or "T" not in iso_str:
        return iso_str or "—"
    date, time = iso_str.split("T", 1)
    return f"{date} {time[:5]}"


def _safe_float(x) -> Optional[float]:
    if x is None:
        return None
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    return None if f != f else f


def _load(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


# ── weekly return ─────────────────────────────────────────────────────────────
def _weekly_return(ticker: str, n: int) -> Optional[float]:
    """報酬 = close[-1]/close[-n]-1（附錄計算慣例；12M→n=53，24M→n=105）."""
    p = WEEKLY_CACHE_DIR / f"{ticker}.json"
    if not p.exists():
        return None
    try:
        bars = json.loads(p.read_text(encoding="utf-8")).get("weekly_bars", []) or []
    except (json.JSONDecodeError, OSError):
        return None
    if len(bars) < n:
        return None
    a = _safe_float(bars[-1].get("close"))
    b = _safe_float(bars[-n].get("close"))
    if not a or not b:
        return None
    return a / b - 1.0


def _weekly_bars(ticker: str) -> Optional[list]:
    """weekly_cache 的 (week_end, close) 序列；無檔或壞檔回 None。"""
    p = WEEKLY_CACHE_DIR / f"{ticker}.json"
    if not p.exists():
        return None
    try:
        raw = json.loads(p.read_text(encoding="utf-8")).get("weekly_bars", []) or []
    except (json.JSONDecodeError, OSError):
        return None
    out = [(b.get("week_end"), _safe_float(b.get("close"))) for b in raw]
    return [(d, c) for d, c in out if d and c] or None


def veto_control_stats(ledger: Optional[dict]) -> Optional[dict]:
    """態②否決對照組 — 每檔取「首次」否決，用 weekly_cache 結算否決之後的走勢：
    to-date 報酬、最深回撤（等回踩到底等不等得到）。閘的年度複檢（91 天）看這組數字。"""
    if not ledger:
        return None
    first: dict = {}
    for e in sorted(ledger.get("events", []) or [], key=lambda e: e.get("signal_date") or ""):
        if e.get("status") == "vetoed" and "態②過熱" in (e.get("vetoes") or []):
            first.setdefault(e.get("ticker"), e)
    rows = []
    for t, e in first.items():
        bars = _weekly_bars(t)
        d0 = e.get("signal_date")
        if not (bars and d0):
            continue
        p0 = None
        for d, c in bars:
            if d <= d0:
                p0 = c
            else:
                break
        after = [c for d, c in bars if d > d0]
        if not (p0 and after):
            continue
        rows.append({"todate": after[-1] / p0 * 100 - 100,
                     "maxdd": min(after) / p0 * 100 - 100})
    if not rows:
        return None
    med = lambda xs: sorted(xs)[len(xs) // 2]  # noqa: E731
    return {
        "n": len(rows),
        "med_todate": med([r["todate"] for r in rows]),
        "med_maxdd": med([r["maxdd"] for r in rows]),
        "pullback10_pct": sum(1 for r in rows if r["maxdd"] < -10) / len(rows) * 100,
    }


# ── 資格閘（自算，不依賴 pass_count）─────────────────────────────────────────
def passes_gate(s: dict) -> bool:
    fail = set(s.get("fail_criteria") or []) - {"de"}
    return (len(fail) == 0
            and s.get("moat_grade") in QUALITY_MOAT_GRADES
            and s.get("moat_trend") != "↓")


def _ev5y(s: dict) -> float:
    v = _safe_float(s.get("live_ev5y_pct"))
    if v is None:
        v = _safe_float(s.get("ev5y_pct"))
    return v or 0.0


def _certainty(s: dict) -> float:
    """確定性 = (moat_score + quality_score) / 20 ∈ [0,1]."""
    return ((_safe_float(s.get("moat_score")) or 0.0)
            + (_safe_float(s.get("quality_score")) or 0.0)) / 20.0


def _ev5y_raw(s: dict):
    """EV5y 原值（None 表無資料，不 fallback 0）。live 優先、缺則報告靜態值。"""
    v = _safe_float(s.get("live_ev5y_pct"))
    if v is None:
        v = _safe_float(s.get("ev5y_pct"))
    return v


def _has_scenario(s: dict) -> bool:
    """EV5y 是否來自 §11.5 機率加權情境（有 bull/bear 價＋機率）＝🟢 嚴謹；否則 heur。"""
    return all(_safe_float(s.get(k)) is not None
               for k in ("bull_5y_price", "bear_5y_price", "p_bull_pct", "p_bear_pct"))


def _bull_mult(s: dict) -> Optional[float]:
    b = _safe_float(s.get("bull_5y_price"))
    p = _safe_float(s.get("price_at_dd"))
    if b and p:
        return b / p
    return None


# ── HTML helpers ──────────────────────────────────────────────────────────────
def _dd_link(s: dict, anchor: bool = True) -> str:
    t = escape(s["ticker"])
    dd = s.get("dd_path")
    if dd:
        href = dd if ("#" in dd or not anchor) else f"{dd}#decision"
        return f'<a href="{escape(href)}">{t}</a>'
    return t


def _verdict_badge(v: Optional[str]) -> str:
    if not v:
        return '<span class="verdict v-none">待補 DD</span>'
    cls = {"進場": "v-in", "觀望": "v-watch", "迴避": "v-avoid"}.get(v, "v-none")
    return f'<span class="verdict {cls}">{escape(v)}</span>'


def _de_badge(s: dict) -> str:
    de = _safe_float(s.get("de"))
    if de is not None and de > DE_WARN_THRESHOLD:
        return f' <span class="de-warn" title="D/E {de:.2f} &gt; {DE_WARN_THRESHOLD} — advisory，不計分不擋">⚠ D/E {de:.1f}</span>'
    return ""


def _pct(v: Optional[float], decimals: int = 1, signed: bool = True) -> str:
    if v is None:
        return "—"
    sign = "+" if (signed and v >= 0) else ""
    return f"{sign}{v:.{decimals}f}%"


DISCOVERY_DETAIL_HTML = '\n<section class="block">\n  <h2 class="block-h"><span class="step">1b</span> 發現層明細 · 多倍候選池 × 形狀掃描</h2>\n  <div class="block-sub">2026-07-07 自 DD Screener 總覽移駐——發現層明細統一住在漏斗頁。兩塊皆為瀏覽器端即時讀取，資料檔未產出時自動隱藏。</div>\n  <!-- ══ Discovery Pool：ID 已標 🔴 核心受益、尚未建 DD ══════════════════════\n       資料源 discovery_pool.json（scripts/list_breakout_candidates.py --write，\n       build_dd_screener.py 每次 build 後自動刷新）。本表 universe 與主表互斥：\n       主表 = 已建 DD 的 242 檔；本池 = ID 層發現但還沒進 DD 漏斗的名字。\n  ═══════════════════════════════════════════════════════════════════════════ -->\n  <div id="discovery-pool" style="display:none;margin:18px 0 0">\n    <details style="background:#fbf3df;border:1px solid var(--line);border-radius:10px;padding:12px 18px">\n      <summary style="cursor:pointer;font-size:13px;font-weight:700;color:var(--warn);letter-spacing:.02em">\n        多倍候選池 — ID 已標 🔴 核心受益、尚未建 DD（<span id="dp-count">0</span> 檔）\n      </summary>\n      <p style="font-size:11.5px;line-height:1.7;color:var(--warn);margin:10px 0 8px">\n        產業報告（ID）§9 標為 <strong>🔴 核心受益</strong>但還沒做個股 DD 的名單 — 這些 ticker 不在上方主表 universe 內（主表只收已建 DD 者）。\n        排序鍵：市值級距（mid/small 優先）→ 純度% → 5Y 需求倍數 → 被標 🔴 的 ID 數。\n        「待補」＝來源 ID 為 v2.4 前的 legacy 報告，重跑後自動補齊；欄位定義見 industry-analyst v2.4（<code>purity_pct</code> / <code>mcap_bucket</code> / <code>demand_5y_multiple</code>）。\n        對池內名字跑 <code>ddreport {ticker}</code> 產 DD 後，該 ticker 自動移入主表。\n      </p>\n      <div id="dp-table" style="overflow-x:auto"></div>\n    </details>\n    <!-- 形狀掃描（爆發形狀 × 覆蓋標籤，橫切研究狀態的雷達）。資料 pre_id_scan.json\n         （scripts/scan_pre_id.py，手動/週更），檔案不存在時整塊隱藏。 -->\n    <details id="pre-id-scan" style="display:none;margin-top:10px;background:#e8eef5;border:1px solid var(--line);border-radius:10px;padding:12px 18px">\n      <summary style="cursor:pointer;font-size:13px;font-weight:700;color:var(--accent-ink)">\n        形狀掃描 — 正在噴的多倍形狀 × 前瞻確認 × 覆蓋標籤（<span id="ps-count">0</span> 檔，<span id="ps-asof">—</span>）\n      </summary>\n      <p style="font-size:11.5px;line-height:1.7;color:var(--accent-ink);margin:10px 0 8px">\n        <strong>橫切研究狀態的雷達</strong>：用「形狀」過濾（不用覆蓋、也不用市值過濾）——掃 RS 領導（510 股日更）∪ <strong>自訂全市場 screen</strong>（美股主板 × 市值 ≥ $0.3B × 營收 YoY ≥ +20%，系統性條件掃描、不是當日漲幅榜碰運氣），過爆發形狀閘（<strong>市值 ≥ $0.3B 無上限</strong>、季營收 YoY ≥ +20%、52 週位置 ≥ 0.6 或 RS ≥ 80、GM ≥ 25%、金融/REIT 剔除）。命中後<strong>三層標籤</strong>而非剔除：\n        <br>• <strong>前瞻</strong>：trailing 只證明過去，多倍股是「市場還沒 price in 的持續成長」——DD universe 內用 Koyfin FY1→FY3 EPS CAGR（與下方主表<strong>同源</strong>，附修正動能），universe 外用 yfinance 分析師 FY+1 營收預估。<span style="background:#eafaef;color:var(--pos);padding:0 6px;border-radius:99px">🟢 續強 ≥+15%</span> <span style="background:var(--line-soft);color:var(--sec);padding:0 6px;border-radius:99px">➖ 放緩 0~15%</span> <span style="background:#fbeceb;color:var(--neg);padding:0 6px;border-radius:99px">🔴 反轉 &lt;0</span>（trailing 是基期效應/週期頂）<span style="background:var(--line-soft);color:var(--sec);padding:0 6px;border-radius:99px">⚪ 無預估</span>（零分析師＝真沒被發現，是訊號不是剔除理由）。<strong>排序＝min(trailing, 前瞻) 保守取小</strong>——trailing +104% 但前瞻 −24% 的週期頂自動沉底。\n        <br>• <strong>加速</strong>：📈 預估下季 YoY 明顯高於已報告 YoY（營運槓桿點火中）／📉 明顯放緩／➖ 平穩。加速 × 🟢 前瞻 × ✅有DD 三者疊加＝本漏斗最強候選訊號。\n        <br>• <strong>覆蓋 + 市值級距</strong>：<span style="background:#e8eef5;color:var(--accent-ink);padding:0 6px;border-radius:99px">🔭 盲區</span>零覆蓋 → <strong>立 ID</strong>｜<span style="background:#fbf3df;color:var(--warn);padding:0 6px;border-radius:99px">🟡 有 ID 無 DD</span> → 形狀轉強＝加速訊號，<strong>建 DD</strong>｜<span style="background:#eafaef;color:var(--pos);padding:0 6px;border-radius:99px">✅ 有 DD</span> → 懂它且剛突破＝最強訊號，<strong>回頭重看 DD</strong>（AR Live 只抓回檔、抓不到突破，這裡補上）。大型股照樣翻倍（NVDA $300B→$3T），小/中型看「沒被發現」、大型/mega 看週期/重定價。\n        <br>• <strong>週數</strong>：連續在榜週數（🆕＝本次新進榜）。形狀撐過 3 週比一日遊強得多；歷史同時累積成日後回測這條漏斗命中率的資料。\n        <br><strong>用途：告訴你注意力放哪</strong>——不是買入清單，估值與獲利品質刻意不在此把關（多倍股早期永遠看起來貴），那是管線②（DD 裁決層）的事。最終進場由個股 DD §14 裁決 + 時機決定。\n      </p>\n      <div id="ps-table" style="overflow-x:auto"></div>\n    </details>\n  </div>\n</section>\n<script>\n// ── Discovery pool（ID 🔴 未建 DD 候選池）─────────────────────────────────\n// 獨立 fetch，404 / parse 失敗時整個區塊保持隱藏，不影響主表。\nfetch(\'./discovery_pool.json\')\n  .then(function(r) { if (!r.ok) throw new Error(\'HTTP \' + r.status); return r.json(); })\n  .then(function(pool) {\n    var rows = pool.rows || [];\n    if (!rows.length) return;\n    var esc = function(s) {\n      return String(s == null ? \'\' : s).replace(/&/g, \'&amp;\').replace(/</g, \'&lt;\').replace(/>/g, \'&gt;\');\n    };\n    var pending = \'<span style="color:var(--warn);opacity:.55">待補</span>\';\n    var html = \'<table style="width:100%;border-collapse:collapse;font-size:11.5px;background:var(--card);border-radius:6px">\' +\n      \'<thead><tr style="background:#fbf3df;color:var(--warn);text-align:left">\' +\n      \'<th style="padding:6px 10px">Ticker</th><th style="padding:6px 8px">市值</th>\' +\n      \'<th style="padding:6px 8px">純度%</th><th style="padding:6px 8px">需求5Y×</th>\' +\n      \'<th style="padding:6px 8px">🔴 ID 數</th><th style="padding:6px 10px">主題</th>\' +\n      \'</tr></thead><tbody>\';\n    rows.forEach(function(r, i) {\n      var themes = (r.themes || []).join(\'；\');\n      html += \'<tr style="border-top:1px solid var(--line)\' + (i % 2 ? \';background:var(--paper)\' : \'\') + \'">\' +\n        \'<td style="padding:5px 10px;font-weight:700;color:var(--ink)">\' + esc(r.ticker) + \'</td>\' +\n        \'<td style="padding:5px 8px">\' + (r.mcap_bucket ? esc(r.mcap_bucket) : pending) + \'</td>\' +\n        \'<td style="padding:5px 8px">\' + (r.purity_pct != null ? esc(r.purity_pct) : pending) + \'</td>\' +\n        \'<td style="padding:5px 8px">\' + (r.best_demand_mult != null ? esc(r.best_demand_mult) : pending) + \'</td>\' +\n        \'<td style="padding:5px 8px">\' + esc(r.core_count) + \'</td>\' +\n        \'<td style="padding:5px 10px;color:var(--sec);max-width:420px">\' + esc(themes) + \'</td>\' +\n        \'</tr>\';\n    });\n    html += \'</tbody></table>\' +\n      \'<p style="font-size:10.5px;color:var(--warn);margin:8px 0 2px">as of \' + esc(pool.as_of || \'—\') +\n      \'｜掃描 \' + esc(pool.id_files_scanned) + \' 份 ID｜v2.4 排序欄位就緒 \' + esc(pool.v24_ranked) + \'/\' + esc(pool.total) + \' 檔</p>\';\n    document.getElementById(\'dp-table\').innerHTML = html;\n    document.getElementById(\'dp-count\').textContent = rows.length;\n    document.getElementById(\'discovery-pool\').style.display = \'\';\n  })\n  .catch(function() { /* pool 未產出：區塊保持隱藏 */ });\n\n// ── 形狀掃描（爆發形狀 × 覆蓋標籤，橫切研究狀態的雷達）─────────────────\nfetch(\'./pre_id_scan.json\')\n  .then(function(r) { if (!r.ok) throw new Error(\'HTTP \' + r.status); return r.json(); })\n  .then(function(scan) {\n    var rows = scan.rows || [];\n    if (!rows.length) return;\n    var esc = function(s) {\n      return String(s == null ? \'\' : s).replace(/&/g, \'&amp;\').replace(/</g, \'&lt;\').replace(/>/g, \'&gt;\');\n    };\n    var COV = {\n      dd:  {t: \'✅ 有 DD\',       bg: \'#eafaef\', fg: \'var(--pos)\'},\n      id:  {t: \'🟡 有 ID 無 DD\', bg: \'#fbf3df\', fg: \'var(--warn)\'},\n      \'\':  {t: \'🔭 盲區\',        bg: \'#e8eef5\', fg: \'var(--accent-ink)\'}\n    };\n    var FWD = {\n      strong:  {t: \'🟢\', bg: \'#eafaef\', fg: \'var(--pos)\'},\n      slow:    {t: \'➖\', bg: \'var(--line-soft)\', fg: \'var(--sec)\'},\n      reverse: {t: \'🔴\', bg: \'#fbeceb\', fg: \'var(--neg)\'},\n      none:    {t: \'⚪\', bg: \'var(--line-soft)\', fg: \'var(--muted)\'}\n    };\n    var ACCEL = {up: \'📈\', down: \'📉\', flat: \'➖\'};\n    var html = \'<table style="width:100%;border-collapse:collapse;font-size:11.5px;background:var(--card);border-radius:6px">\' +\n      \'<thead><tr style="background:#e8eef5;color:var(--accent-ink);text-align:left">\' +\n      \'<th style="padding:6px 10px">Ticker</th><th style="padding:6px 8px">覆蓋</th><th style="padding:6px 8px">市值</th>\' +\n      \'<th style="padding:6px 8px">營收YoY</th>\' +\n      \'<th style="padding:6px 8px" title="DD universe 內＝Koyfin FY1→FY3 EPS CAGR（與主表同源）；外＝yfinance 分析師 FY+1 營收預估。🟢≥+15% ➖0~15% 🔴<0 ⚪無預估">前瞻</th>\' +\n      \'<th style="padding:6px 8px" title="預估下季 YoY vs 已報告 YoY：📈 加速（≥1.15×）📉 放緩（≤0.7× 或轉負）➖ 平穩">加速</th>\' +\n      \'<th style="padding:6px 8px" title="連續在榜週數；🆕＝本次新進榜">週</th>\' +\n      \'<th style="padding:6px 8px">GM</th>\' +\n      \'<th style="padding:6px 8px">52w位置</th><th style="padding:6px 8px">RS</th>\' +\n      \'<th style="padding:6px 10px">Industry</th></tr></thead><tbody>\';\n    rows.forEach(function(r, i) {\n      var c = COV[r.coverage || \'\'] || COV[\'\'];\n      var f = FWD[r.fwd_tag || \'none\'] || FWD.none;\n      var fwdTxt = r.fwd_growth_pct != null\n        ? f.t + \' \' + (r.fwd_growth_pct > 0 ? \'+\' : \'\') + Math.round(r.fwd_growth_pct) + \'%\'\n        : f.t + \' —\';\n      var fwdTip = r.fwd_src === \'koyfin\'\n        ? \'Koyfin FY1→FY3 EPS CAGR（與主表同源）\' + (r.eps_revision_pct != null ? \'｜修正 \' + (r.eps_revision_pct > 0 ? \'+\' : \'\') + r.eps_revision_pct + \'pp\' : \'\')\n        : (r.fwd_src === \'yf\' ? \'yfinance 分析師 FY+1 營收預估\' : \'無分析師預估（零覆蓋＝真沒被發現）\');\n      var wk = r.weeks_on_list || 1;\n      var isNew = r.first_seen && scan.as_of && r.first_seen === scan.as_of;\n      // ✅有DD 的覆蓋標籤連到該 DD §14 裁決錨點（雷達↔裁決一鍵；「懂它且剛轉強→直接看裁決」）\n      var covInner = \'<span style="background:\' + c.bg + \';color:\' + c.fg + \';padding:1px 7px;border-radius:99px;font-size:10.5px;white-space:nowrap">\' + c.t + \'</span>\';\n      var covCell = (r.coverage === \'dd\' && r.dd_path)\n        ? \'<a href="\' + r.dd_path + \'" target="_blank" style="text-decoration:none" title="跳該 DD §14 統一裁決">\' + covInner + \'</a>\'\n        : covInner;\n      html += \'<tr style="border-top:1px solid var(--line)\' + (i % 2 ? \';background:var(--paper)\' : \'\') + \'">\' +\n        \'<td style="padding:5px 10px;font-weight:700;color:var(--ink)">\' + esc(r.ticker) +\n        (r.name ? \' <span style="font-weight:400;color:var(--sec);font-size:10.5px">\' + esc(r.name) + \'</span>\' : \'\') + \'</td>\' +\n        \'<td style="padding:5px 8px">\' + covCell + \'</td>\' +\n        \'<td style="padding:5px 8px">$\' + (r.mcap_usd / 1e9).toFixed(1) + \'B <span style="color:var(--muted);font-size:10px">\' + esc(r.mcap_bucket || \'\') + \'</span></td>\' +\n        \'<td style="padding:5px 8px;color:var(--pos);font-weight:700">+\' + Math.round(r.rev_growth * 100) + \'%</td>\' +\n        \'<td style="padding:5px 8px" title="\' + esc(fwdTip) + \'"><span style="background:\' + f.bg + \';color:\' + f.fg + \';padding:1px 7px;border-radius:99px;font-size:10.5px;white-space:nowrap;font-weight:600">\' + fwdTxt + \'</span></td>\' +\n        \'<td style="padding:5px 8px;text-align:center">\' + (ACCEL[r.accel] || \'—\') + \'</td>\' +\n        \'<td style="padding:5px 8px;white-space:nowrap">\' + (isNew ? \'<span style="background:#e8eef5;color:var(--accent-ink);padding:0 5px;border-radius:99px;font-size:10px;font-weight:700">🆕</span>\' : esc(wk) + \'週\') + \'</td>\' +\n        \'<td style="padding:5px 8px">\' + (r.gross_margin != null ? Math.round(r.gross_margin * 100) + \'%\' : \'—\') + \'</td>\' +\n        \'<td style="padding:5px 8px">\' + (r.range_pos != null ? esc(r.range_pos) : \'—\') + \'</td>\' +\n        \'<td style="padding:5px 8px">\' + (r.rs_score != null ? esc(r.rs_score) : \'—\') + \'</td>\' +\n        \'<td style="padding:5px 10px;color:var(--sec)">\' + esc(r.industry || \'\') + \'</td></tr>\';\n    });\n    var cc = scan.coverage_counts || {};\n    var fc = scan.fwd_counts || {};\n    html += \'</tbody></table>\' +\n      \'<p style="font-size:10.5px;color:var(--accent-ink);margin:8px 0 2px">as of \' + esc(scan.as_of) +\n      \'｜掃描候選 \' + esc(scan.candidates_scanned) + \'｜命中 \' + esc(scan.hits) +\n      (scan.hits > rows.length ? \'（顯示排序前 \' + rows.length + \'）\' : \'\') +\n      \'（🔭 盲區 \' + esc(cc.blind != null ? cc.blind : \'—\') + \'｜🟡 有 ID \' + esc(cc.id != null ? cc.id : \'—\') + \'｜✅ 有 DD \' + esc(cc.dd != null ? cc.dd : \'—\') + \'）\' +\n      (scan.fwd_counts ? \'｜前瞻：🟢 \' + esc(fc.strong) + \'／➖ \' + esc(fc.slow) + \'／🔴 \' + esc(fc.reverse) + \'／⚪ \' + esc(fc.none) : \'\') +\n      \'｜排序＝min(trailing, 前瞻) 保守取小</p>\';\n    document.getElementById(\'ps-table\').innerHTML = html;\n    document.getElementById(\'ps-count\').textContent = rows.length;\n    document.getElementById(\'ps-asof\').textContent = scan.as_of || \'—\';\n    document.getElementById(\'pre-id-scan\').style.display = \'\';\n  })\n  .catch(function() { /* 掃描未產出：區塊保持隱藏 */ });\n</script>\n'


# ── section renderers ─────────────────────────────────────────────────────────
def render_universe(latest: dict, pre_id: Optional[dict], momentum_blind: list) -> str:
    universe = latest.get("universe_size", len(latest.get("stocks", [])))
    shape_blind = 0
    if pre_id:
        cc = pre_id.get("coverage_counts") or {}
        shape_blind = cc.get("blind", 0)
    mom_blind = len(momentum_blind)
    return f"""<section class="block">
  <h2 class="block-h"><span class="step">1</span> 宇宙 · 待研究隊列</h2>
  <div class="block-sub">DD 宇宙規模與兩條「還沒被研究的候選」入口——形狀掃描的覆蓋盲區（六燈全滅＝零方法覆蓋），與下方回看鏡的動能盲區（高報酬卻無／舊 DD）。</div>
  <div class="stat-row">
    <div class="stat"><strong>{universe}</strong>DD 宇宙（latest.json）</div>
    <div class="stat"><strong>{shape_blind}</strong>形狀掃描盲區</div>
    <div class="stat"><strong>{mom_blind}</strong>動能盲區 <a href="#lookback" class="mini">→ 回看鏡</a></div>
  </div>
</section>"""


def render_gate(gated: list) -> str:
    de_warn_n = sum(1 for s in gated if (_safe_float(s.get("de")) or 0) > DE_WARN_THRESHOLD)
    # sort by certainty desc for a stable display
    gsorted = sorted(gated, key=lambda s: (-_certainty(s), s["ticker"]))
    tags = "".join(
        f'<span class="gtag">{_dd_link(s)}<span class="gm">{escape(s.get("moat_grade") or "?")}{escape(s.get("moat_trend") or "")}</span>{_de_badge(s)}</span>'
        for s in gsorted
    )
    return f"""<section class="block">
  <h2 class="block-h"><span class="step">2</span> 資格閘 · 通過 {len(gated)} 檔</h2>
  <div class="block-sub">
    自算口徑（<b>不依賴 pass_count</b>）：<code>fail_criteria −{{de}} 為空</code> 且 <code>moat_grade∈{{S,A,B}}</code> 且 <code>moat_trend≠↓</code>。
    D/E 為 advisory——<code>&gt;{DE_WARN_THRESHOLD}</code> 標 ⚠ 但<b>不計分、不擋</b>（持有人 2026-06-11 拍板的五條件無 D/E；本頁已把 de 退出閘）。
    本閘通過 {len(gated)} 檔，其中 <b>{de_warn_n}</b> 檔帶 D/E ⚠。
  </div>
  <div class="gate-grid">{tags}</div>
</section>"""


def _core_row(s: dict) -> str:
    return f"""<tr>
  <td class="left">{_dd_link(s)}{_de_badge(s)}</td>
  <td>{_verdict_badge(s.get("dca_verdict"))}</td>
  <td>{escape(s.get("dca_role") or "—")}</td>
  <td class="num"><strong>{s["_score"]:.2f}</strong></td>
  <td class="num">{_pct(_ev5y(s), signed=False)}</td>
  <td class="num">{_certainty(s):.2f}</td>
  <td class="meta">{escape(s.get("moat_grade") or "?")}{escape(s.get("moat_trend") or "")} · {escape(s.get("runway_post_y5") or "—")}</td>
</tr>"""


def _core_table(rows: list, empty: str) -> str:
    if not rows:
        return f'<div class="empty">{empty}</div>'
    body = "\n".join(_core_row(s) for s in rows)
    return f"""<table>
<thead><tr>
  <th class="left">Ticker</th><th>裁決</th><th>角色</th>
  <th class="num">EV5y×確定性</th><th class="num">EV5y</th><th class="num">確定性</th>
  <th class="left">護城河 · runway</th>
</tr></thead>
<tbody>
{body}
</tbody></table>"""


def render_core(core_sorted: list) -> str:
    exe_all = [s for s in core_sorted if s.get("dca_verdict") == "進場"]
    # 核心席位只認「進場＋核心角色」；角色優先＝無條件核心先佔位，再依潛力分補足 5 席
    exe_core = [s for s in exe_all if is_core_role(s)]
    exe_core.sort(key=lambda s: (0 if _is_unconditional_core(s) else 1, -s["_score"], s["ticker"]))
    sleeve = exe_core[:CORE_SLOTS]
    bench_core = exe_core[CORE_SLOTS:]
    exe_noncore = [s for s in exe_all if not is_core_role(s)]   # 進場但角色非核心 → 歸衛星軌
    watch = [s for s in core_sorted if s.get("dca_verdict") == "觀望"]
    nodd = [s for s in core_sorted if s.get("dca_verdict") not in ("進場", "觀望", "迴避")]
    noncore_note = ""
    if exe_noncore:
        names = "、".join(escape(s["ticker"]) for s in exe_noncore)
        noncore_note = (f'<div class="seg-note">↪ 另有 {len(exe_noncore)} 檔進場但 DD 角色為衛星'
                        f'（{names}）→ 走衛星倉上限 {SATELLITE_CAP_PCT:.0f}%，不佔核心席位。</div>')
    return f"""<div class="track-card track-core">
  <h3>核心軌 <span class="cnt">席位 {len(sleeve)}/{CORE_SLOTS}</span></h3>
  <div class="track-desc">
    軌別＝<b>DD 裁決＝進場 且 角色含「核心持倉」</b>；<b>席位硬上限 {CORE_SLOTS} 檔</b>（章程 core ≤5）。
    選席＝<b>角色優先</b>：無條件核心持倉先佔位，餘席依 <b>EV5y × 確定性</b> 由條件式核心補足；超出落板凳。
    EV5y 取 <code>live_ev5y_pct</code> 優先、缺則 <code>ev5y_pct</code>。單檔上限 {CORE_CAP_PCT:.0f}%（個股部淨值）。
  </div>
  <div class="seg-h seg-in">核心席位（最終 {CORE_SLOTS}）· {len(sleeve)} 檔</div>
  {_core_table(sleeve, "目前無可執行核心進場票。")}
  {noncore_note}
  <div class="seg-h seg-watch">核心板凳（進場核心·超出席位，等席位開遞補）· {len(bench_core)} 檔</div>
  {_core_table(bench_core, "無溢出板凳名字。")}
  <div class="seg-h seg-watch">⏸ 觀望板凳（裁決＝觀望）· {len(watch)} 檔</div>
  {_core_table(watch, "板凳無觀望名字。")}
  <div class="seg-h seg-none">無裁決 · 待補 DD · {len(nodd)} 檔</div>
  {_core_table(nodd, "過閘者皆有站上裁決。")}
</div>"""


def _struct_row(s: dict) -> str:
    bm = _bull_mult(s)
    return f"""<tr>
  <td class="left">{_dd_link(s)}{_de_badge(s)}</td>
  <td>{_verdict_badge(s.get("dca_verdict"))}</td>
  <td class="num"><strong>{s["_sscore"]:.1f}</strong></td>
  <td class="num">{_pct(_ev5y(s), signed=False)}</td>
  <td class="num">{('×%.2f' % bm) if bm else '—'}</td>
  <td class="meta">{escape(s.get("moat_grade") or "?")}{escape(s.get("moat_trend") or "")} · runway {escape(s.get("runway_post_y5") or "—")}</td>
</tr>"""


def render_struct(struct_sorted: list) -> str:
    if not struct_sorted:
        body = '<div class="empty">目前無符合結構軌條件的名字。</div>'
    else:
        rows = "\n".join(_struct_row(s) for s in struct_sorted)
        body = f"""<table>
<thead><tr>
  <th class="left">Ticker</th><th>裁決</th>
  <th class="num">EV5y+bull×</th><th class="num">EV5y</th><th class="num">bull 倍數</th>
  <th class="left">護城河 · runway</th>
</tr></thead>
<tbody>
{rows}
</tbody></table>"""
    return f"""<div class="track-card track-struct">
  <h3>衛星·結構軌 <span class="cnt">{len(struct_sorted)} 檔</span></h3>
  <div class="track-desc">
    軌別＝<b>runway_post_y5＝🟢</b> ＋ <code>eps2y</code>／<code>peg</code> 不 fail ＋ 護城河過（∈{{S,A,B}}、trend≠↓）＋ <b>非核心角色</b>（一檔一軌）。
    排序＝<b>EV5y ＋ bull 倍數 ×{STRUCT_BULL_MULT:.0f}</b>（bull 倍數＝bull_5y_price/price_at_dd）。單檔上限 {SATELLITE_CAP_PCT:.0f}%。
  </div>
  {body}
</div>"""


def _cyc_row(r: dict) -> str:
    dd = r.get("dd_path")
    t = escape(r["ticker"])
    link = f'<a href="{escape(dd)}#decision">{t}</a>' if dd else t
    ret = r.get("ret_12m_pct")
    ret_str = f"{'+' if (ret or 0) >= 0 else ''}{ret:.0f}%" if ret is not None else "—"
    v = r.get("dca_verdict")
    return f"""<tr>
  <td class="left">{link}</td>
  <td class="num"><strong>{(r.get("revision_rank_score") or 0):.1f}</strong></td>
  <td class="num">{_pct(_safe_float(r.get("eps2y_revision_pp")))}</td>
  <td class="num">{_pct(_safe_float(r.get("eps_fy_next_revision_pct")))}</td>
  <td class="num {'ret-hot' if r.get('hot') else ''}">{ret_str}</td>
  <td class="meta">{escape(r.get("moat_grade") or "?")}{escape(r.get("moat_trend") or "")}</td>
  <td>{_verdict_badge(v)}</td>
</tr>"""


def _cyc_table(rows: list, empty: str) -> str:
    if not rows:
        return f'<div class="empty">{empty}</div>'
    body = "\n".join(_cyc_row(r) for r in rows)
    return f"""<table>
<thead><tr>
  <th class="left">Ticker</th><th class="num">排序分</th><th class="num">2Y修正pp</th>
  <th class="num">FY+1修正%</th><th class="num">12M報酬</th><th class="left">護城河</th><th>裁決</th>
</tr></thead>
<tbody>
{body}
</tbody></table>"""


def render_cyclical(cyc: Optional[dict]) -> str:
    if not cyc:
        return """<div class="track-card track-cyc">
  <h3>衛星·循環軌</h3>
  <div class="empty">cyclical-track.json 尚未產生 — 先跑 <code>scripts/build_cyclical_track.py</code>。</div>
</div>"""
    low = cyc.get("low_heat", [])
    hot = cyc.get("hot", [])
    return f"""<div class="track-card track-cyc">
  <h3>衛星·循環軌 <span class="cnt">{cyc.get('qualified_total', 0)} 檔（低熱 {len(low)} / 🔥 {len(hot)}）</span></h3>
  <div class="track-desc warn-inline">
    <b>研究提名清單，非進場清單</b>——循環底部（FCF／ROIC 未過）× 分析師上修的候選池，交 DD（QC-42 循環鏡頭附錄 B）＋ 板機接手。
    單檔上限 <b>{CYCLICAL_CAP_PCT:.0f}%</b>；🔥 標記者 12M 報酬 &gt; +250%，<b>明文不可追高</b>，等回踩。
    詳見 <a href="/dd-screener/cyclical-track.html">循環軌全頁</a>。
  </div>
  <div class="seg-h seg-in">🟢 低熱可研究 · {len(low)} 檔</div>
  {_cyc_table(low, "目前無低熱循環候選。")}
  <div class="seg-h seg-hot">🔥 已熱等回踩（不可追）· {len(hot)} 檔</div>
  {_cyc_table(hot, "目前無 🔥 已熱候選。")}
</div>"""


def compute_rereview(stocks: list) -> list:
    """觀望複審隊列 — 裁決保鮮迴路。觀望/迴避不是終局：錯過成本或上修動能命中門檻，
    裁決強制回爐複審（stock-analyst）。複審≠改判，維持原判也是合法產出；不複審才是缺陷。"""
    rows = []
    for s in stocks:
        if s.get("dca_verdict") not in ("觀望", "迴避"):
            continue
        reasons = []
        p0 = _safe_float(s.get("price_at_dd"))
        px = _safe_float((s.get("ma") or {}).get("price"))
        miss = (px / p0 - 1) * 100 if (p0 and px) else None
        if miss is not None and miss >= REREVIEW_MISS_PCT:
            reasons.append(f"錯過成本 {miss:+.0f}%")
        fy1 = _safe_float(s.get("eps_fy_next_revision_pct"))
        if fy1 is not None and fy1 >= REREVIEW_EPS_FY1_PCT:
            reasons.append(f"FY+1 上修 {fy1:+.1f}%")
        pp = _safe_float(s.get("eps2y_revision_pp"))
        if pp is not None and pp >= REREVIEW_EPS2Y_PP:
            reasons.append(f"2Y CAGR 上修 {pp:+.1f}pp")
        if reasons:
            rows.append({"s": s, "miss": miss, "reasons": reasons})
    rows.sort(key=lambda r: (-(r["miss"] if r["miss"] is not None else -999.0), r["s"]["ticker"]))
    return rows


def _rereview_row(r: dict) -> str:
    s = r["s"]
    age = s.get("dd_age_days")
    return f"""<tr>
  <td class="left">{_dd_link(s)}{_de_badge(s)}</td>
  <td>{_verdict_badge(s.get("dca_verdict"))}</td>
  <td class="left">{escape("；".join(r["reasons"]))}</td>
  <td class="num">{f"{age:.0f}d" if age is not None else "—"}</td>
</tr>"""


def render_rereview(rows: list) -> str:
    if not rows:
        body = '<div class="empty">目前無觸發複審的觀望/迴避裁決。</div>'
    else:
        body = f"""<table>
<thead><tr>
  <th class="left">Ticker</th><th>現裁決</th><th class="left">觸發原因</th><th class="num">DD 齡</th>
</tr></thead>
<tbody>
{"".join(_rereview_row(r) for r in rows)}
</tbody></table>"""
    return f"""<div class="track-card track-rereview">
  <h3>⏰ 觀望複審隊列 <span class="cnt">{len(rows)} 檔</span></h3>
  <div class="track-desc">
    <b>裁決保鮮迴路</b>——觀望/迴避不是終局。命中任一門檻＝裁決回爐複審（跑 stock-analyst 複審，非重寫）：
    ① 錯過成本 ≥ +{REREVIEW_MISS_PCT:.0f}%（裁決日價 → 現價）
    ② FY+1 EPS 單月上修 ≥ +{REREVIEW_EPS_FY1_PCT:.0f}%
    ③ 2Y CAGR 修正 ≥ +{REREVIEW_EPS2Y_PP:.0f}pp（②③＝循環軌同口徑）。
    <b>複審≠追高</b>——維持原判也是合法產出；不複審才是缺陷（MU 型錯過的直接解）。
  </div>
  {body}
</div>"""


def render_tracks(core_sorted: list, struct_sorted: list, cyc: Optional[dict],
                  rereview_rows: list) -> str:
    return f"""<section class="block">
  <h2 class="block-h"><span class="step">3</span> 三軌射擊名單</h2>
  <div class="block-sub">過閘後依角色分三軌，一檔一軌。每檔 Ticker 連站上 DD 的 <code>#decision</code> 錨點；無裁決者標「待補 DD」＝研究隊列。</div>
  {render_core(core_sorted)}
  {render_struct(struct_sorted)}
  {render_cyclical(cyc)}
  {render_rereview(rereview_rows)}
</section>"""


def render_trigger(sop: Optional[dict], veto_by_reason: dict,
                   veto_ctrl: Optional[dict] = None) -> str:
    if not sop:
        return """<section class="block">
  <h2 class="block-h"><span class="step">4</span> 板機現況</h2>
  <div class="empty">sop-funnel/latest.json 尚未產生。</div>
</section>"""
    today = sop.get("today_signals", []) or []
    opens = sop.get("open_trades", []) or []
    a1 = sop.get("standby_a1", []) or []
    a2 = sop.get("standby_a2", []) or []
    b = sop.get("standby_b", []) or []
    c = sop.get("standby_c", []) or []
    base = sop.get("base_building", []) or []
    veto2 = veto_by_reason.get("態②過熱", 0)
    as_of = sop.get("as_of", "—")

    def _names(lst):
        return "、".join(escape(x.get("ticker", "?")) for x in lst) or "—"

    def _open_names(lst):
        parts = []
        for x in lst:
            t = escape(x.get("ticker", "?"))
            st = x.get("sim", {}).get("current_state") if isinstance(x.get("sim"), dict) else None
            parts.append(f"{t}<span class='st'>{escape(st or x.get('entry_type',''))}</span>")
        return "、".join(parts) or "—"

    return f"""<section class="block">
  <h2 class="block-h"><span class="step">4</span> 板機現況 <span class="asof">sop-funnel as of {as_of}</span></h2>
  <div class="block-sub">SOP 漏斗 T+1 執行層的當日燈號。態②過熱否決＝反動能硬閘擋下的訊號累計（ledger append-only 統計）。</div>
  <div class="stat-row">
    <div class="stat"><strong>{len(today)}</strong>今日訊號</div>
    <div class="stat"><strong>{len(opens)}</strong>持倉中 open</div>
    <div class="stat"><strong>{len(a1)}/{len(a2)}/{len(b)}/{len(c)}</strong>待命 A1/A2/B/C</div>
    <div class="stat"><strong>{len(base)}</strong>築底中</div>
    <div class="stat warn"><strong>{veto2}</strong>態②過熱否決（累計）</div>
  </div>
  <div class="trigger-detail">
    <div><span class="lbl">持倉中</span>{_open_names(opens)}</div>
    <div><span class="lbl">待命 A2</span>{_names(a2)} <span class="sep">·</span> <span class="lbl">待命 B</span>{_names(b)} <span class="sep">·</span> <span class="lbl">待命 C·冷卻</span>{_names(c)}</div>
    <div><span class="lbl">築底中</span>{_names(base)}</div>
  </div>
  {_veto_ctrl_html(veto_ctrl)}
  <div class="block-foot"><a href="/dd-screener/sop-funnel.html">→ SOP Funnel 全頁</a></div>
</section>"""


def _veto_ctrl_html(vc: Optional[dict]) -> str:
    """態②否決對照組一行 — 閘的成本/收益活數字（每檔首否決口徑，weekly_cache 結算）。"""
    if not vc:
        return ""
    return (f'<div class="veto-ctrl">否決對照組（每檔首否決，n={vc["n"]}）：'
            f'否決後 to-date 中位 <b>{vc["med_todate"]:+.1f}%</b> · '
            f'最深回撤中位 <b>{vc["med_maxdd"]:+.1f}%</b> · '
            f'曾回撤&gt;10% 比例 <b>{vc["pullback10_pct"]:.0f}%</b>'
            f'　＝閘擋下的名字後來給不給回踩機會，91 天複檢閾值時看這行。</div>')


def _lookback_row(entry: dict) -> str:
    t = escape(entry["ticker"])
    dd = entry.get("dd_path")
    link = f'<a href="{escape(dd)}#decision">{t}</a>' if dd else t
    cov = entry["cov"]
    cov_html = {
        "covered": '<span class="cov cov-ok">✅ 已覆蓋</span>',
        "stale": f'<span class="cov cov-stale">⚠ DD {entry.get("dd_age_days")}天</span>',
        "blind": '<span class="cov cov-blind">🔭 盲區·無 DD</span>',
    }[cov]
    return f"""<tr class="{'lb-queue' if cov != 'covered' else ''}">
  <td class="num rk">{entry['rank']}</td>
  <td class="left">{link}</td>
  <td class="num big">{'+' if entry['ret'] >= 0 else ''}{entry['ret']*100:.0f}%</td>
  <td>{cov_html}</td>
</tr>"""


def render_lookback(lb12: list, lb24: list, queue12: list, queue24: list) -> str:
    def _tbl(rows):
        body = "\n".join(_lookback_row(r) for r in rows)
        return f"""<table>
<thead><tr><th class="num">#</th><th class="left">Ticker</th><th class="num">報酬</th><th>覆蓋</th></tr></thead>
<tbody>
{body}
</tbody></table>"""

    q12 = "、".join(escape(r["ticker"]) for r in queue12) or "—（top30 皆已覆蓋）"
    q24 = "、".join(escape(r["ticker"]) for r in queue24) or "—（top30 皆已覆蓋）"
    return f"""<section class="block" id="lookback">
  <h2 class="block-h"><span class="step">5</span> 回看鏡 · 發現力稽核</h2>
  <div class="block-sub">
    週線報酬 top {LOOKBACK_TOP_N}（<code>close[-1]/close[-53]</code>＝12M、<code>[-105]</code>＝24M），標覆蓋狀態＝「這些大漲的名字我抓到了嗎」的誠實稽核。
    <b>盲區＋DD&gt;{DD_STALE_DAYS} 天</b>者＝<b>動能盲區研究隊列</b>（表中反白列）。SNDK／AXTI／BE 等 mandate-gap 循環贏家已回補新 DD＝已覆蓋，正是循環鏡頭補上的證據。
  </div>
  <div class="queue-note">
    <b>12M 動能盲區隊列</b>（{len(queue12)}）：{q12}<br>
    <b>24M 動能盲區隊列</b>（{len(queue24)}）：{q24}
  </div>
  <div class="lb-grid">
    <div class="lb-col"><h4>12M 報酬 top {LOOKBACK_TOP_N}</h4>{_tbl(lb12)}</div>
    <div class="lb-col"><h4>24M 報酬 top {LOOKBACK_TOP_N}</h4>{_tbl(lb24)}</div>
  </div>
</section>"""


def _prov_badge(prov: str) -> str:
    if prov == "rigorous":
        return '<span class="prov prov-rig">🟢 §11.5</span>'
    return '<span class="prov prov-heur">🟡 heur</span>'


def _eps_incomplete(s: dict) -> bool:
    """Koyfin 無 FY3 EPS 預估 → 過閘 eps2y／heur EV5y 可能失真（多為小型股無分析師覆蓋）。"""
    return _safe_float(s.get("eps_fy3")) is None


def _eps_flag(s: dict) -> str:
    return ('<span class="eps-flag" title="Koyfin 無 FY3 EPS 預估：過閘 eps2y 與 heur EV5y 可能失真；'
            '§11.5 情境不受影響">⚠ EPS 不全</span>') if _eps_incomplete(s) else ""


def _lb_score_row(u: dict, rank: int) -> str:
    s = u["s"]
    fill = ""
    if u["prov"] == "heur" and not s.get("dca_verdict"):
        fill = '<span class="lb-fill">→ 補 DD</span>'
    verd = _verdict_badge(s.get("dca_verdict"))
    age = s.get("dd_age_days")
    age_s = f"{age}d" if age is not None else "—"
    return f"""<tr>
  <td class="num">{rank}</td>
  <td class="left">{_dd_link(s)}{_de_badge(s)}</td>
  <td class="num"><strong>{u['score']:.1f}</strong></td>
  <td class="num">{_pct(u['raw_ev'], signed=True)}</td>
  <td>{_prov_badge(u['prov'])}{_eps_flag(s)}</td>
  <td class="num">{u['cert']:.2f}</td>
  <td>{verd}</td>
  <td class="num">{age_s}</td>
  <td class="meta">{escape(s.get("moat_grade") or "?")}{escape(s.get("moat_trend") or "")}</td>
  <td>{fill}</td>
</tr>"""


def render_leaderboard(univ: list, artifacts: list, n_total: int) -> str:
    top = univ[:LEADERBOARD_TOP_N]
    body = "\n".join(_lb_score_row(u, i) for i, u in enumerate(top, 1)) or \
        '<tr><td colspan="10" class="empty">無可排名的名字。</td></tr>'
    fill_cnt = sum(1 for u in top if u["prov"] == "heur" and not u["s"].get("dca_verdict"))
    art_note = ""
    if artifacts:
        items = "、".join(
            f'{escape(u["s"]["ticker"])}（EV5y {_pct(u["raw_ev"], signed=True)}）' for u in artifacts)
        art_note = (f'<div class="queue-note" style="border-color:var(--warn)">'
                    f'<b>⚠ EV5y 異常 · 抽出排行待人工檢視（{len(artifacts)}）</b>：{items}<br>'
                    f'　來源＝heur 啟發式（無 §11.5 情境）且 EV5y &gt; {HEUR_EV5Y_ARTIFACT_CAP:.0f}%，'
                    f'數值不可信（多為舊 DD 無 bull/bear 情境）→ 補 v14 DD 才有嚴謹 EV5y。</div>')
    return f"""<section class="block" id="leaderboard">
  <h2 class="block-h"><span class="step">6</span> 全宇宙潛力榜 · 補 DD 導航</h2>
  <div class="block-sub">
    把核心軌的<b>潛力分（EV5y × 確定性）</b>套到全宇宙 {n_total} 檔——<b>不是買入排行，是研究優先序</b>。
    <b>確定性</b>（moat+quality/20）全宇宙皆有；<b>EV5y</b> 出處分兩級：
    <span class="prov prov-rig">🟢 §11.5</span> 機率加權情境（嚴謹、有反偏差防線）vs
    <span class="prov prov-heur">🟡 heur</span> 啟發式估計（僅方向性）。
    <b>用途</b>：🟡 高分票＝「看起來有潛力但 EV5y 未經 §11.5 嚴謹化」＝<b>下一個該補 v14 DD 的候選</b>（補了就把 🟡 轉 🟢）。
    <br><span class="eps-flag">⚠ EPS 不全</span>＝Koyfin 無 FY3 EPS 預估（多為小型股無分析師覆蓋），此時<b>過閘 eps2y 與 heur EV5y 雙重不可信</b>——補 DD 用 §11.5 bottom-up 自建情境即可繞過（如 WLDN）。
  </div>
  {art_note}
  <div class="tbl-wrap"><table class="lb-score">
<thead><tr>
  <th class="num">#</th><th class="left">Ticker</th><th class="num">潛力分</th><th class="num">EV5y</th>
  <th>出處</th><th class="num">確定性</th><th>裁決</th><th class="num">DD齡</th><th>moat</th><th></th>
</tr></thead>
<tbody>
{body}
</tbody></table></div>
  <div class="block-foot">榜上 top {LEADERBOARD_TOP_N} 中 <b>{fill_cnt} 檔標「→ 補 DD」</b>＝🟡 且無裁決，優先補齊到潛力序前段皆 🟢，核心/衛星席位才是在可信名單裡競爭。</div>
</section>"""


def render_howto() -> str:
    rules = [
        ("這頁只排序，不下單", "潛力分決定「先研究／先考慮誰」，<b>不是買進訊號</b>。要買，等 sop-funnel 板機亮燈：A1 起漲／B 回踩／<b>C 冷卻完成</b>（態②過熱否決後，完成週收盤跌回 +2σ 帶內且守住 52 週線 — 2026-07-04 起，過熱不再是終局）。"),
        ("裁決是唯一權威", "能不能進候選，看 DD §14＝<b>進場／觀望／迴避</b>。沒裁決（待補 DD）＝還沒資格，不是可買。"),
        ("席位鎖死：核心 5 ＋ 衛星 5", "核心軌固定 5 席（角色優先），衛星／循環另計。滿了要進，得<b>打贏現有最弱的</b>才換，不加席位。"),
        ("三軌各有任務，別混", "核心＝耐久複利（上限 10%）；衛星結構＝runway🟢 數倍股（5%）；衛星循環＝底部×上修（3%，先等回踩）。"),
        ("潛力榜是補 DD 導航，不是買入排行", "🟢 §11.5 才可信，<b>🟡 heur 只有方向性</b>。標「→ 補 DD」＝下一個該研究的名字，不是叫你買。"),
        ("由左到右讀", "發現 → 資格閘 → 三軌裁決 → 板機 → 回看鏡 → 潛力榜。每一站只回答一個問題，別跳著看。"),
        ("這頁不含實際持倉", "只呈現研究層。買了什麼、多少倉位，不在站上。"),
        ("觀望不是終局", "觀望/迴避後錯過成本 ≥+30% 或 EPS 上修過門檻 → 進「⏰ 複審隊列」，裁決<b>必須回爐</b>。複審≠追高，維持原判也合法；不複審才是缺陷。"),
    ]
    items = "\n".join(
        f'<li><b>{i}. {t}</b>　{d}</li>' for i, (t, d) in enumerate(rules, 1))
    return f"""<section class="block howto">
  <h2 class="block-h">使用守則 · 30 秒讀懂這頁</h2>
  <ol class="howto-list">
{items}
  </ol>
</section>"""


def render_privacy() -> str:
    return f"""<section class="block privacy">
  <h2 class="block-h"><span class="step">7</span> 隱私線</h2>
  <div class="privacy-body">
    本頁只呈現<b>研究層</b>：宇宙、資格閘、三軌候選、板機燈號、發現力稽核。
    <b>實際持倉與權重不上站</b>（與 <code>/pm/</code> 封存同一原則）。射擊名單≠買入指令——每檔進場仍須
    (a) 站上 DD 統一裁決＝進場、(b) sop-funnel 板機亮燈、(c) 部位在個股部上限內
    （核心 ≤{CORE_CAP_PCT:.0f}%／衛星 ≤{SATELLITE_CAP_PCT:.0f}%／循環 ≤{CYCLICAL_CAP_PCT:.0f}%，分母＝個股部淨值）。
  </div>
</section>"""


# ── page assembly ─────────────────────────────────────────────────────────────
STYLE = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--sans);background:var(--paper);color:var(--body);line-height:1.5}
.hero{background:var(--card);border-bottom:1px solid var(--line);padding:24px 32px 18px}
.hero-inner{max-width:min(1400px,96vw);margin:0 auto}
.hero-h1{font-family:var(--serif);font-size:1.6rem;font-weight:700;letter-spacing:-.01em;color:var(--ink);margin-bottom:6px}
.hero-sub{font-size:12px;color:var(--sec);line-height:1.6;max-width:1000px}
.hero-stats{display:flex;gap:12px;margin-top:12px;flex-wrap:wrap}
.hero-stat{background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:7px 11px;font-size:11px;color:var(--sec)}
.hero-stat strong{color:var(--ink);font-size:13px;display:block;margin-bottom:1px}
.wrap{max-width:min(1400px,96vw);margin:0 auto;padding:18px 32px 0}
.block{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh-1);padding:18px 20px;margin-bottom:18px}
.block-h{font-family:var(--serif);font-size:1.25rem;font-weight:700;color:var(--ink);margin-bottom:6px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.block-h .step{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:5px;background:var(--accent);color:#fff;font-size:13px;font-weight:700}
.block-h .asof{font-size:11px;font-weight:400;color:var(--muted)}
.block-sub{font-size:12px;color:var(--sec);line-height:1.7;margin-bottom:12px}
.block-foot{margin-top:10px;font-size:12px}
.block-foot a,.block-sub a,.queue-note a,.track-desc a{color:var(--accent);text-decoration:none}
.block-foot a:hover{text-decoration:underline}
code{background:var(--paper);padding:1px 5px;border-radius:5px;font-size:11px;color:var(--body)}
.stat-row{display:flex;gap:12px;flex-wrap:wrap}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:10px 14px;font-size:11px;color:var(--sec);min-width:110px}
.stat strong{color:var(--ink);font-size:20px;display:block;margin-bottom:2px;font-variant-numeric:tabular-nums}
.stat.warn{background:#fbf3df;border-color:var(--line)}
.stat.warn strong{color:var(--warn)}
.stat .mini{display:inline-block;margin-top:3px;font-size:10px}
/* gate grid */
.gate-grid{display:flex;flex-wrap:wrap;gap:6px}
.gtag{display:inline-flex;align-items:center;gap:5px;background:var(--paper);border:1px solid var(--line);border-radius:5px;padding:4px 8px;font-size:12px}
.gtag a{color:var(--ink);text-decoration:none;font-weight:700}
.gtag a:hover{color:var(--accent);text-decoration:underline}
.gtag .gm{font-size:10px;color:var(--sec);font-weight:600}
.de-warn{font-size:9.5px;color:var(--warn);background:#fbf3df;border-radius:5px;padding:0 4px}
/* tracks */
.track-card{border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh-1);padding:14px 16px;margin-top:14px;background:var(--card)}
.veto-ctrl{margin-top:10px;font-size:12px;color:var(--sec);background:var(--paper);border:1px solid var(--line);border-radius:5px;padding:8px 10px}
.track-card h3{font-family:var(--sans);font-size:1rem;font-weight:700;color:var(--ink);margin-bottom:4px;display:flex;align-items:center;gap:8px}
.track-card h3 .cnt{font-size:11px;font-weight:600;color:var(--muted)}
.track-desc{font-size:11.5px;color:var(--sec);line-height:1.7;margin-bottom:10px}
.track-desc.warn-inline{background:#fbf3df;border:1px solid var(--line);border-radius:5px;padding:8px 10px;color:var(--warn)}
.seg-h{font-size:11.5px;font-weight:700;padding:6px 0 4px;margin-top:8px;border-top:1px dashed var(--line)}
.seg-note{font-size:11px;color:var(--sec);padding:4px 0 2px;line-height:1.6}
.prov{font-size:10.5px;font-weight:700;padding:1px 6px;border-radius:5px;white-space:nowrap}
.prov-rig{background:#eafaef;color:var(--pos)}
.prov-heur{background:#fbf3df;color:var(--warn)}
.lb-fill{font-size:10.5px;font-weight:700;color:var(--accent);white-space:nowrap}
.eps-flag{display:inline-block;font-size:10px;font-weight:700;color:var(--warn);background:#fbf3df;border-radius:5px;padding:1px 5px;margin-left:4px;white-space:nowrap;cursor:help}
table.lb-score td,table.lb-score th{padding:5px 8px}
.howto{background:var(--paper);border-color:var(--line)}
.howto-list{margin:6px 0 0;padding-left:0;list-style:none}
.howto-list li{font-size:12.5px;color:var(--body);line-height:1.7;padding:5px 0;border-top:1px solid var(--line)}
.howto-list li:first-child{border-top:none}
.howto-list li b{color:var(--ink)}
.seg-in{color:var(--pos)}.seg-watch{color:var(--warn)}.seg-none{color:var(--muted)}.seg-hot{color:var(--warn)}
table{width:100%;border-collapse:collapse;font-size:12px;margin-top:4px}
th{background:var(--paper);color:var(--sec);font-weight:700;padding:7px 9px;text-align:right;border-bottom:2px solid var(--line);font-size:10px;letter-spacing:.03em}
th.left{text-align:left}
td{padding:7px 9px;text-align:right;border-bottom:1px solid var(--line-soft);font-variant-numeric:tabular-nums}
td.left{text-align:left;color:var(--ink);font-weight:500}
td.num{text-align:right}
td a{color:var(--accent);text-decoration:none;font-weight:700}
td a:hover{text-decoration:underline}
td.meta{font-size:10.5px;color:var(--sec);text-align:left}
tbody tr:hover td{background:#fbf8f1}
.ret-hot{color:var(--warn);font-weight:700}
.verdict{padding:1px 8px;border-radius:5px;font-size:10.5px;font-weight:700;white-space:nowrap}
.v-in{background:#eafaef;color:var(--pos)}.v-watch{background:#fbf3df;color:var(--warn)}
.v-avoid{background:#fbeceb;color:var(--neg)}.v-none{background:var(--line-soft);color:var(--muted);font-weight:600}
.empty{padding:12px;text-align:center;color:var(--muted);font-size:12px;font-style:italic}
/* trigger */
.trigger-detail{margin-top:12px;font-size:12px;color:var(--body);line-height:2}
.trigger-detail .lbl{display:inline-block;min-width:64px;color:var(--muted);font-size:11px;font-weight:700}
.trigger-detail .st{font-size:9.5px;color:var(--muted);margin-left:2px}
.trigger-detail .sep{color:var(--muted);margin:0 6px}
/* lookback */
.queue-note{background:#fbf3df;border:1px solid var(--line);border-radius:5px;padding:10px 12px;font-size:11.5px;color:var(--warn);line-height:1.9;margin-bottom:12px}
.lb-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.lb-col h4{font-size:12px;color:var(--sec);margin-bottom:4px;font-weight:700}
tr.lb-queue{background:#fbf6ea}
tr.lb-queue td{border-bottom-color:var(--line)}
td.rk{color:var(--muted);font-size:10px}
td.big{font-weight:700;color:var(--pos)}
.cov{font-size:10px;font-weight:700;padding:1px 6px;border-radius:5px;white-space:nowrap}
.cov-ok{background:#eafaef;color:var(--pos)}.cov-stale{background:#fbf3df;color:var(--warn)}.cov-blind{background:var(--line-soft);color:var(--sec)}
/* privacy */
.privacy{border-color:var(--line);background:var(--paper)}
.privacy-body{font-size:12.5px;color:var(--body);line-height:1.9}
.meta-note{padding:16px 20px 4px;font-size:11px;color:var(--muted);line-height:1.7}
.meta-note code{background:var(--paper);padding:1px 5px;border-radius:5px;font-size:10px}
@media(max-width:760px){.lb-grid{grid-template-columns:1fr}}
"""


def build(dry_run: bool = False) -> int:
    print(f"=== Pipeline-page build · {_now_taipei_iso()} ===\n")
    latest = _load(LATEST_JSON)
    if not latest:
        print(f"  ERR: {LATEST_JSON} missing — run build_dd_screener.py first", file=sys.stderr)
        return 2
    stocks = latest.get("stocks", []) or []
    by_ticker = {s["ticker"]: s for s in stocks}
    cyc = _load(CYCLICAL_JSON)
    sop = _load(SOP_LATEST)
    ledger = _load(SOP_LEDGER)
    pre_id = _load(PRE_ID_SCAN)

    # ── 資格閘 ──
    gated = [s for s in stocks if passes_gate(s)]
    gated_set = {s["ticker"] for s in gated}

    # ── 核心軌 ── = 過閘池 ∪（裁決∈{進場,觀望} 且 角色含核心持倉）
    # 條件式核心（如 COHR）即使未過數字閘也算核心角色，納入核心軌、不漏進衛星軌
    core = {}
    for s in stocks:
        v = s.get("dca_verdict")
        if s["ticker"] in gated_set or (v in ("進場", "觀望") and is_core_role(s)):
            core[s["ticker"]] = s
    for s in core.values():
        s["_score"] = _ev5y(s) * _certainty(s)
    core_sorted = sorted(core.values(), key=lambda s: (-s["_score"], s["ticker"]))

    # ── 衛星·結構軌 ── runway🟢 + eps2y/peg 不 fail + moat 過 + 非核心角色
    # 一檔一軌：循環軌成員（trailing fcf/roic fail 形狀）優先歸循環軌，不重複列入結構軌
    cyc_tickers = set()
    if cyc:
        for grp in ("low_heat", "hot"):
            for r in (cyc.get(grp) or []):
                cyc_tickers.add(r.get("ticker"))
    struct = []
    for s in stocks:
        if s["ticker"] in core or s["ticker"] in cyc_tickers or is_core_role(s):
            continue
        if s.get("runway_post_y5") != "🟢":
            continue
        fail = set(s.get("fail_criteria") or [])
        if "eps2y" in fail or "peg" in fail:
            continue
        if s.get("moat_grade") not in QUALITY_MOAT_GRADES or s.get("moat_trend") == "↓":
            continue
        bm = _bull_mult(s)
        s["_sscore"] = _ev5y(s) + (bm * STRUCT_BULL_MULT if bm else 0.0)
        struct.append(s)
    struct_sorted = sorted(struct, key=lambda s: (-s["_sscore"], s["ticker"]))

    # ── 態②否決計數 + 對照組結算 ──
    veto_by_reason: dict = {}
    if ledger:
        for e in ledger.get("events", []) or []:
            if e.get("status") == "vetoed":
                for v in (e.get("vetoes") or []):
                    veto_by_reason[v] = veto_by_reason.get(v, 0) + 1
    veto_ctrl = veto_control_stats(ledger)

    # ── 觀望複審隊列（裁決保鮮迴路）──
    rereview_rows = compute_rereview(stocks)

    # ── 回看鏡 ──
    def _cov(ticker: str):
        s = by_ticker.get(ticker)
        if s is None or not s.get("dd_path"):
            return "blind", None, None
        age = s.get("dd_age_days")
        cov = "stale" if (age is not None and age > DD_STALE_DAYS) else "covered"
        return cov, s.get("dd_path"), age

    def _top(n_bars: int):
        rows = []
        for p in WEEKLY_CACHE_DIR.glob("*.json"):
            r = _weekly_return(p.stem, n_bars)
            if r is not None:
                rows.append((p.stem, r))
        rows.sort(key=lambda x: -x[1])
        out = []
        for i, (t, r) in enumerate(rows[:LOOKBACK_TOP_N], 1):
            cov, dd, age = _cov(t)
            out.append({"rank": i, "ticker": t, "ret": r, "cov": cov,
                        "dd_path": dd, "dd_age_days": age})
        return out

    lb12 = _top(53)
    lb24 = _top(105)
    queue12 = [r for r in lb12 if r["cov"] != "covered"]
    queue24 = [r for r in lb24 if r["cov"] != "covered"]

    # momentum blind (for universe section) = union of the two queues
    momentum_blind = {r["ticker"] for r in queue12} | {r["ticker"] for r in queue24}

    # ── 全宇宙潛力榜 ── 潛力分 = EV5y × 確定性；heur 來源且 EV5y>cap 抽出當 artifact
    univ, artifacts = [], []
    for s in stocks:
        raw = _ev5y_raw(s)
        if raw is None:
            continue
        rigorous = _has_scenario(s)
        u = {"s": s, "raw_ev": raw, "cert": _certainty(s),
             "prov": "rigorous" if rigorous else "heur",
             "score": raw * _certainty(s)}
        if (not rigorous) and raw > HEUR_EV5Y_ARTIFACT_CAP:
            artifacts.append(u)
        else:
            univ.append(u)
    univ.sort(key=lambda u: (-u["score"], u["s"]["ticker"]))
    artifacts.sort(key=lambda u: -u["raw_ev"])
    n_scored = len(univ) + len(artifacts)

    # ── console summary ──
    print(f"  universe={latest.get('universe_size')} 過閘={len(gated)} "
          f"(D/E⚠={sum(1 for s in gated if (_safe_float(s.get('de')) or 0)>DE_WARN_THRESHOLD)})")
    print(f"  核心軌={len(core_sorted)} "
          f"(進場={sum(1 for s in core_sorted if s.get('dca_verdict')=='進場')} "
          f"觀望={sum(1 for s in core_sorted if s.get('dca_verdict')=='觀望')} "
          f"待補={sum(1 for s in core_sorted if s.get('dca_verdict') not in ('進場','觀望','迴避'))})")
    print(f"    可執行: {[s['ticker'] for s in core_sorted if s.get('dca_verdict')=='進場']}")
    print(f"  結構軌={len(struct_sorted)}: {[s['ticker'] for s in struct_sorted]}")
    if cyc:
        print(f"  循環軌={cyc.get('qualified_total')} (低熱 {len(cyc.get('low_heat',[]))} / 🔥 {len(cyc.get('hot',[]))})")
    print(f"  板機: today={len(sop.get('today_signals',[])) if sop else '?'} "
          f"open={len(sop.get('open_trades',[])) if sop else '?'} 態②否決={veto_by_reason.get('態②過熱',0)}")
    print(f"  複審隊列={len(rereview_rows)}: "
          f"{[(r['s']['ticker'], r['reasons']) for r in rereview_rows]}")
    if veto_ctrl:
        print(f"  態②對照組: n={veto_ctrl['n']} to-date中位={veto_ctrl['med_todate']:+.1f}% "
              f"最深回撤中位={veto_ctrl['med_maxdd']:+.1f}% 回撤>10%={veto_ctrl['pullback10_pct']:.0f}%")
    print(f"  回看鏡動能盲區: 12M={[r['ticker'] for r in queue12]} 24M={[r['ticker'] for r in queue24]}")
    print(f"  潛力榜: 可排 {len(univ)}/{n_scored} "
          f"(🟢{sum(1 for u in univ if u['prov']=='rigorous')} 🟡{sum(1 for u in univ if u['prov']=='heur')}) "
          f"artifact 抽出 {len(artifacts)}={[u['s']['ticker'] for u in artifacts]}")
    print(f"    top5: {[(u['s']['ticker'], round(u['score'],1), u['prov']) for u in univ[:5]]}")

    # ── assemble HTML ──
    universe_html = render_universe(latest, pre_id, list(momentum_blind))
    gate_html = render_gate(gated)
    tracks_html = render_tracks(core_sorted, struct_sorted, cyc, rereview_rows)
    trigger_html = render_trigger(sop, veto_by_reason, veto_ctrl)
    howto_html = render_howto()
    lookback_html = render_lookback(lb12, lb24, queue12, queue24)
    leaderboard_html = render_leaderboard(univ, artifacts, n_scored)
    privacy_html = render_privacy()

    as_of = latest.get("as_of", "—")
    run_ts = _now_taipei_iso()
    # 核心席位＝進場＋核心角色，硬上限 CORE_SLOTS（與 render_core 同口徑）
    n_sleeve = min(CORE_SLOTS, sum(1 for s in core_sorted
                                   if s.get("dca_verdict") == "進場" and is_core_role(s)))

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>個股部漏斗總覽 Pipeline — 發現 → 資格閘 → 三軌 → 板機 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<link rel="stylesheet" href="/assets/imq-base.css">
<style>{STYLE}</style>
</head>
<body>
{NAV_BLOCK}

<div class="hero">
  <div class="hero-inner">
    <div class="hero-h1">個股部漏斗總覽 · Pipeline</div>
    <div class="hero-sub">
      個股部（總資產 25%，5～10 檔最有上漲潛力的組合）整條投資流程的活數字：
      <b>發現 → 資格閘 → 三軌射擊名單 → 板機 → 監控 → 回看鏡</b>。所有數字來自既有 JSON，每週隨基本面刷新自動更新。
      本頁只呈現<b>研究層</b>，實際持倉與權重不上站。
      <b>分工</b>：本頁管<b>流程與板機</b>；排序與席位見 <a href="/engine/">決策引擎</a>，對外正式榜見 <a href="/picks/">精選清單</a>。
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>{_fmt_stamp(run_ts)}</strong>最後更新（台北）</div>
      <div class="hero-stat"><strong>{as_of}</strong>資料 as of</div>
      <div class="hero-stat"><strong>{latest.get('universe_size')}</strong>DD 宇宙</div>
      <div class="hero-stat"><strong>{len(gated)}</strong>過閘</div>
      <div class="hero-stat"><strong>{n_sleeve}/{CORE_SLOTS}</strong>核心席位</div>
      <div class="hero-stat"><strong>{cyc.get('qualified_total',0) if cyc else 0}</strong>循環候選</div>
    </div>
  </div>
</div>

<div class="wrap">
{howto_html}
{universe_html}
{DISCOVERY_DETAIL_HTML}
{gate_html}
{tracks_html}
{trigger_html}
{lookback_html}
{leaderboard_html}
{privacy_html}

<div class="meta-note">
  <p><b>數據來源</b>：<code>latest.json</code>（宇宙／資格閘／核心軌／結構軌）·
  <code>cyclical-track.json</code>（循環軌）· <code>sop-funnel/latest.json</code>＋<code>ledger.json</code>（板機／否決）·
  <code>pre_id_scan.json</code>（形狀盲區）· <code>data/weekly_cache/</code>（回看鏡週線報酬）。</p>
  <p style="margin-top:8px">資格閘為<b>自算口徑</b>（fail−de 為空 ∧ moat∈{{S,A,B}} ∧ trend≠↓），不依賴 latest.json 的 pass_count。
  射擊名單≠買入指令，見「隱私線」三重前提。</p>
</div>
</div>

<footer class="imq-foot">
  <div>© 2026 InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</body>
</html>
"""

    if dry_run:
        print(f"\n  (dry-run) would write {HTML_OUT} ({len(html):,} bytes)")
        return 0

    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"\n  ✓ Wrote {HTML_OUT} ({HTML_OUT.stat().st_size:,} bytes)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Don't write files")
    args = p.parse_args()
    return build(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
