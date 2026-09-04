#!/usr/bin/env python3
"""決策引擎 L3 — 席位擂台（seat vs challenger）＋ regime 撥盤.

擂台規則（v1，2026-07-04 鎖定）：
  席位 = 現行漏斗同口徑（裁決＝進場＋核心角色，無條件優先，EV5y×確定性排序，核心 5 席；
         衛星 = 進場＋衛星角色，上限 5 席，空缺明示）。
  挑戰者 = 同「形狀」的未坐席候選（裁決 ∈ {進場, 觀望}），按 EV5y×確定性排序。
  ⚔ 擂台警報 = 挑戰者分數 > 席位分數 → 進人工複審清單（每月擂台裁決是人做的，
  本頁只把對戰表擺好——引擎不自動換席）。

Regime 撥盤（v1 規則鎖定；資訊性，不接倉位系統）：
  進攻 1.0 = SPY confirmed_uptrend 且 25 日 distribution ≤ 3
  中性 0.5 = under_pressure 或 distribution 4–7
  防守 0.25 = correction 或跌破 200DMA 或 distribution ≥ 8
  形狀敏感度：突破帶/動能重估 對 regime 最敏感；循環轉折次之；規則詳頁尾。

輸出：docs/engine/arena.json + arena.html。
Usage: python3 scripts/engine/build_arena.py
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.common import OUT_DIR, ROOT, page_embed_shell, pct  # noqa: E402
from engine.build_scoreboard import _bars, classify_shape  # noqa: E402
from engine.grp import (  # noqa: E402
    DD_FRESH_DAYS, MKTCAP_MIN, P_LABEL_HTML, R_VETO_FY1, cap_ok, fetch_caps, grp_route, grp_score,
    market_ok,
)

WEEKLY_CACHE_UNIVERSE = ROOT / "data" / "weekly_cache_universe"   # 非 DD 池週線 fallback（見 build_radar.py 檔頭 docstring）
QGM_US = ROOT / "docs" / "qgm" / "latest.json"
QGM_TW = ROOT / "docs" / "qgm-tw" / "latest.json"
BOARD_TXT = OUT_DIR / "board.txt"
BOARD_HTML = OUT_DIR / "_board_body.html"   # 2026-09-02：HTML 版看板（表格＋燈號），raw fragment 供 cockpit innerHTML 與 _arena_body.html 內嵌共用
TWD_PER_USD = 32.0          # QGM-TW 市值（新台幣十億）換算門檻用，近似值
OVERHEAT_R26_PCT = 80.0     # 時機燈：26 週漲幅 >+80% ＝ 過熱（不進席位，只列擁有層）
LISTING_ALIAS = {"2330.TW": "TSM"}   # 本地掛牌 → ADR（同公司只留一席）
HYST_NEW_RUNS = 2           # 遲滯：新席需連 2 次週跑過閘
HYST_INCUMBENT_FAILS = 4    # 遲滯：現任席連 4 次不過閘才下席（硬 veto 除外）
# B4② 降權版（2026-09-04 持有人拍板）：DD 180 天內裁決＝觀望的現任席，遲滯保護降權
# 4→2 次不過閘即下席（新席遲滯與硬 veto 不變）。依據：席位層回溯考卷只命中 FIX 一檔；
# DD 池全體 miss 組（觀望但後續漲）8 檔中位 +39% vs save 組（觀望且後續跌）112 檔中位 −10.5%，
# miss 尾巴太肥故不硬擋、只降權。詳 knowledge/rule_ledger.md。
HYST_INCUMBENT_FAILS_WATCH = 2

DD_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
MARKET_STATE = ROOT / "docs" / "screener" / "market_state.json"
UNIVERSE = ROOT / "data" / "engine" / "universe.json"
CARDS_JSON = OUT_DIR / "cards.json"
LEDGER_JSON = OUT_DIR / "arena-ledger.json"   # 席位變動帳本（append-only）
ARENA_JSON = OUT_DIR / "arena.json"
# 2026-07-10 席位分頁整併：輸出 nav-less 片段供 /cockpit/#seats-arena 子分頁 iframe 嵌入；
# /engine/arena.html 已改為 redirect stub（見 site_nav SKIP_FILES）。內容為 M5 對照組 PREREG 凍結，只換殼不改文。
ARENA_HTML = OUT_DIR / "_arena_body.html"

CORE_SLOTS = 5
SAT_SLOTS = 5
SHAPE_LABELS = {"breakout_base": "🟩 突破帶", "cyclical_turn": "🟧 循環轉折",
                "momentum_rerate": "🟪 動能重估", "other": "⬜ 其他"}


def regime_dial() -> dict:
    try:
        ms = json.loads(MARKET_STATE.read_text(encoding="utf-8"))
        spy = ms["indices"]["SPY"]
    except (OSError, json.JSONDecodeError, KeyError):
        return {"level": None, "label": "market_state 不可用", "detail": ""}
    state = spy.get("state")
    dist = (spy.get("distribution_days") or {}).get("count_25d") or 0
    below_200 = (spy.get("vs_200dma_pct") or 0) < 0
    if state == "correction" or below_200 or dist >= 8:
        level, label = 0.25, "🛡 防守"
    elif state == "under_pressure" or dist >= 4:
        level, label = 0.5, "⚖ 中性"
    else:
        level, label = 1.0, "🚀 進攻"
    return {"level": level, "label": label,
            "detail": f"SPY {state}（{spy.get('state_since', '—')} 起）· 25 日 distribution {dist} · "
                      f"vs 200DMA {spy.get('vs_200dma_pct', '—')}%",
            "as_of": ms.get("data_date")}


def shape_of(ticker: str) -> str:
    bars = _bars(ticker)
    if not bars:
        return "other"
    return classify_shape(bars, bars[-1][0])


def _universe_bars(t, _c={}):
    """Fallback 週線讀取：data/weekly_cache_universe/<TICKER>.json（build_radar.py Stage 1
    為不在 DD 池的 engine universe 名字〔如 QGM〕另存的 cache，見該檔 docstring）。與
    build_scoreboard._bars() 讀的 data/weekly_cache/ 是刻意分離的兩個目錄——後者是
    p_clim 基準率母體，不可混入非 DD 池名字，故這裡另開一份獨立、同格式的讀取＋記憶體 cache。"""
    if t not in _c:
        p = WEEKLY_CACHE_UNIVERSE / f"{t}.json"
        if p.exists():
            try:
                raw = json.loads(p.read_text(encoding="utf-8")).get("weekly_bars") or []
                _c[t] = [(b["week_end"], b["close"]) for b in raw if b.get("close")]
            except (json.JSONDecodeError, KeyError, OSError):
                _c[t] = None
        else:
            _c[t] = None
    return _c[t]


def weekly_structure(ticker: str) -> dict:
    """週線 cache → 26 週漲幅／52 週線／距 52 週高（時機層用，不依賴 DD）。
    DD 池（data/weekly_cache/）沒有時 fall back 到 data/weekly_cache_universe/——
    讓池外名字（如 QGM）也有 52 週線 / 距高 / 26 週報酬，不再一律顯示「缺」。"""
    bars = _bars(ticker) or _universe_bars(ticker)
    if not bars or len(bars) < 30:
        return {}
    closes = [c for _, c in bars]
    last = closes[-1]
    r26 = (last / closes[-27] - 1) * 100 if len(closes) > 27 else None
    r52 = (last / closes[-53] - 1) * 100 if len(closes) > 53 else None
    w52 = sum(closes[-52:]) / min(52, len(closes))
    hi52 = max(closes[-52:])
    return {"px": last, "r26": r26, "r52": r52, "above_w52": last > w52,
            "dist_hi52": (last / hi52 - 1) * 100}


def load_qgm_rows(stocks_map: dict, exclude: set | None = None) -> list[dict]:
    """QGM（姊妹 repo 品質池，US＋TW）→ 無 DD 名字的擁有層列（v2：DD 選配）。
    欄位對齊 latest.json 口徑：roic／fcf／成長（FY1→FY2 單年，QGM 的 cagr2y 以 FY0 為基期會膨脹）
    ／live_fpe_est＝fy1_per／時機取週線 cache，缺則用 QGM trend template 條件 1＋3。"""
    rows = []
    seen = set(exclude or ())
    for path, src, fx in ((QGM_US, "qgm-us", 1.0), (QGM_TW, "qgm-tw", TWD_PER_USD)):
        if src == "qgm-tw" and not market_ok("0000.TW"):
            # 2026-09-02 持有人拍板：v2 先只做美股，台股另建——不讀 QGM-TW 供母體列
            #（探測值用 market_ok 而非硬寫死排除，未來拍板改變時這裡自動跟著恢復）。
            # qgm_cap_map() 仍讀 QGM_TW 當市值 fallback，無害（不產生 universe row）。
            continue
        try:
            q = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for key in ("candidates", "watch_list", "quality_pool"):
            for x in q.get(key) or []:
                tk = x.get("ticker")
                if not tk or tk in stocks_map or tk in seen:
                    continue
                seen.add(tk)
                h = x.get("hard_filter_details") or {}
                def hv(k):
                    v = (h.get(k) or {}).get("value")
                    return None if v is None else float(v)
                fy1, fy2 = x.get("fy1_eps"), x.get("fy2_eps")
                g1 = ((fy2 / fy1 - 1) * 100) if fy1 and fy2 and fy1 > 0 else None
                per1 = x.get("fy1_per")
                st = weekly_structure(tk)
                conds = (x.get("trend_template") or {}).get("conditions") or {}
                c1 = (conds.get("condition_1") or {}).get("pass")
                c3 = (conds.get("condition_3") or {}).get("pass")
                qb = x.get("quality_breakdown") or {}
                durable = (qb.get("roic_5y_stability") or {}).get("pct_above")
                roic = hv("roic"); fcf = hv("fcf_margin")
                rows.append({
                    "ticker": tk, "name": tk, "sector": "", "_src": "qgm", "_qgm_pool": src,
                    "_durable_5y": durable, "_g_method": "FY1→FY2 單年",
                    "roic": roic * 100 if roic is not None else None,
                    "fcf": fcf * 100 if fcf is not None else None,
                    "de": hv("debt_to_equity"),
                    "eps_fy1_fy3_cagr_pct": g1, "eps_fy_next": fy2, "eps_fy_curr": fy1,
                    "live_fpe_est": per1, "live_peg": (per1 / g1) if per1 and g1 and g1 > 0 else None,
                    "eps_fy_next_revision_pct": None, "eps2y_revision_pp": None,
                    "ma": {"above_w52": st.get("above_w52") if st else bool(c1 and c3),
                           "price": st.get("px") or x.get("price")},
                    "timing": {"dist_52w_high_pct": st.get("dist_hi52") if st else None,
                               "timing_source": "weekly_cache" if st else "qgm-tt"},
                    "_r26": st.get("r26") if st else None, "_r52": st.get("r52") if st else None,
                    "_mktcap": (x.get("market_cap_b") or 0) * 1e9 / fx,
                    "moat_grade": None, "moat_trend": None,
                    "dca_verdict": None, "dca_role": None, "dd_path": None, "dd_age_days": None,
                })
    return rows


def qgm_cap_map() -> dict:
    """QGM 市值（含 DD 池重疊名字）當 mktcap.json／yfinance 缺漏時的 fallback（TW 以近似匯率換算）。"""
    out = {}
    for path, fx in ((QGM_US, 1.0), (QGM_TW, TWD_PER_USD)):
        try:
            q = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for key in ("candidates", "watch_list", "quality_pool"):
            for x in q.get(key) or []:
                if x.get("ticker") and x.get("market_cap_b"):
                    out.setdefault(x["ticker"], x["market_cap_b"] * 1e9 / fx)
    return out


def _yf_rev_map() -> dict:
    """雷達 stage2 的 yfinance 30 天修正（第二源，覆蓋主榜候選 ~250 檔）。"""
    try:
        radar = json.loads((OUT_DIR / "radar.json").read_text(encoding="utf-8"))
        return {t: v.get("fy1_rev_30d_pct") for t, v in (radar.get("stage2") or {}).items()}
    except (OSError, json.JSONDecodeError):
        return {}


def cross_check_r(r: dict, yf_rev) -> dict:
    """兩源一致性防線（2026-07-04）：主源規則＝DD 池認 Koyfin、池外認 yfinance，計分不混用；
    但「重下修 ≤-2% 一票否決」採**任一源觸發即否決**（保守聯集——源吵架時聽壞消息），
    兩源方向相反（一正一負）標 ⚠ 源分歧供人工判讀。"""
    if yf_rev is None:
        return r
    r["r_alt_yf30d"] = yf_rev
    g = r["grp"]
    koy = g.get("r_fy1")
    if koy is not None and ((koy > 0) != (yf_rev > 0)) and abs(koy - yf_rev) > 2:
        r["r_conflict"] = True
    if yf_rev <= R_VETO_FY1 and not g.get("veto"):   # v2：否決線與主源同步（−10%）
        r["grp"] = g = dict(g)
        g["veto"] = True
        g["pass"] = False
        g["why"] = [f"上修閘保守否決：yfinance 30 天預估重下修 {yf_rev:+.1f}%（Koyfin 正向不足以豁免）"] \
                   + list(g["why"])
    return r


def dd_tag(s: dict) -> str:
    v = s.get("dca_verdict"); age = s.get("dd_age_days")
    if not v:
        return "DD 舊版無裁決" if s.get("dd_path") else "無 DD"
    tag = f"DD {v}" + (f"·{s.get('dca_role')}" if s.get("dca_role") else "")
    if age is not None:
        tag += f"（{int(age)}d）"
        if age > DD_FRESH_DAYS:
            tag += "⚠過期"
    return tag


def row_dict(s: dict) -> dict:
    if "_r26" not in s:
        st = weekly_structure(s["ticker"])
        s["_r26"] = st.get("r26") if st else None
        s["_r52"] = st.get("r52") if st else None
    g = grp_score(s)
    # 時機燈：過熱（26 週 >+80%）——不進席位，擁有層照列
    if g["p_label"] and s.get("_r26") is not None and s["_r26"] > OVERHEAT_R26_PCT:
        g = dict(g); g["p_label"] = "overheated"; g["pass"] = False
        g["why"] = [f"位置閘：過熱（26 週 {s['_r26']:+.0f}%）"] + list(g["why"])
    route, route_why = grp_route(s)
    role = s.get("dca_role") or ""
    age = s.get("dd_age_days")
    fresh = bool(s.get("dca_verdict")) and (age is None or age <= DD_FRESH_DAYS)
    mismatch = fresh and ((route == "satellite" and "核心" in role) or (route == "core" and "衛星" in role))
    if s.get("dca_verdict") == "迴避":
        g = dict(g); g["pass"] = False; g["why"] = ["DD 迴避（veto）"] + list(g["why"])
    return {"ticker": s["ticker"], "verdict": s.get("dca_verdict"),
            "role": role, "route": route, "route_why": route_why,
            "role_mismatch": mismatch, "dd_tag": dd_tag(s), "dd_age_days": age, "dd_fresh": fresh,
            "src": s.get("_src") or "dd-pool", "g_method": s.get("_g_method") or "FY1→FY3 CAGR",
            "grp": g, "score": g["score"],
            "roic": g["quality"].get("roic"), "fcf": g["quality"].get("fcf"),
            "peg": (s.get("live_peg") if s.get("live_peg") is not None else s.get("peg")),
            "r26": s.get("_r26"), "r52": s.get("_r52"),
            "moat": f'{s.get("moat_grade") or "?"}{s.get("moat_trend") or ""}' if s.get("moat_grade") else "—",
            "shape": shape_of(s["ticker"]),
            "dd_path": s.get("dd_path")}


def render_seat_changes(changes: list[dict]) -> str:
    if not changes:
        return '<div class="empty">尚無席位變動記錄（首個 snapshot 已建檔，之後的變動會逐筆列出）。</div>'
    track_txt = {"core": "🎯 核心", "sat": "🛰 衛星"}
    rows = []
    for c in reversed(changes[-10:]):
        rows.append(f'<tr><td>{escape(c["to"])}</td><td class="left">{track_txt.get(c["track"], c["track"])}</td>'
                    f'<td class="left">{escape("、".join(c["in"]) or "—")}</td>'
                    f'<td class="left">{escape("、".join(c["out"]) or "—")}</td></tr>')
    return ('<table><thead><tr><th>日期</th><th class="left">軌</th>'
            '<th class="left">上席</th><th class="left">下席</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table>")


def load_light_rows(stocks_map: dict) -> list[dict]:
    """快審卡（qual_tier=light）→ 衛星席第二資格來源（2026-07-04 拍板）。
    光卡只給衛星資格（核心席必須完整 DD）。優先序：dd-meta 有裁決的名字光卡讓位；
    池內「待補 DD」名字光卡可用（GRP 用 latest.json 全口徑）；池外用雷達主榜口徑
    （G＝FY+1 隱含成長、R＝30 天修正），頁面標 🪶。"""
    cards_dir = OUT_DIR / "cards" / "data"
    try:
        radar = json.loads((OUT_DIR / "radar.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        radar = {}
    board = {r["ticker"]: r for r in radar.get("grp_board") or []}
    stage2 = radar.get("stage2") or {}
    verdict_tickers = {t for t, s in stocks_map.items() if s.get("dca_verdict")}
    rows = []
    for p in sorted(cards_dir.glob("*.json")):
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if c.get("qual_tier") != "light" or c["ticker"] in verdict_tickers:
            continue   # dd-meta 裁決優先，光卡不重複
        if not market_ok(c["ticker"]):
            continue   # 2026-09-02 持有人拍板：台股另建，快審卡母體亦排除 .TW
        t = c["ticker"]
        if t in stocks_map:
            grp = grp_score(stocks_map[t])   # 池內待補 DD：全口徑
        else:
            b = board.get(t) or {}
            s2 = stage2.get(t) or {}
            g = b.get("g_fy1_pct", s2.get("g_fy1_pct"))
            rev = b.get("fy1_rev_30d_pct", s2.get("fy1_rev_30d_pct"))
            p_label = b.get("p_label")
            veto = rev is not None and rev <= -2.0
            ok = (g is not None and g >= 15.0 and rev is not None and rev > 0
                  and not veto and p_label is not None)
            grp = {"pass": ok, "veto": veto, "g": g, "r_fy1": rev, "r_2y": None,
                   "r_strength": rev or 0.0, "p_label": p_label,
                   "dist_hi": b.get("dist_ath"), "price": b.get("price"),
                   "score": round((rev or 0) + (g or 0) / 100.0, 3),
                   "why": [] if ok else ["雷達三閘資料不足或未過（隨主榜週更再驗）"]}
        rows.append({"ticker": t, "verdict": c.get("verdict"),
                     "role": c.get("role") or "衛星持倉",
                     "route": "satellite", "route_why": "快審卡（衛星限定）",
                     "role_mismatch": False, "qual": "light",
                     "grp": grp, "score": grp["score"],
                     "moat": f'{c.get("moat_grade") or "?"}{c.get("moat_trend") or ""}',
                     "shape": "other", "dd_path": None})
    return rows


def _n(v, w=5, d=1):
    if v is None:
        return "-".rjust(w)   # ASCII 連字號（非 CJK 全形或 em dash）——欄位須 ASCII-only，見規則 A
    try:
        return f"{float(v):{w}.{d}f}"
    except (TypeError, ValueError):
        return str(v)[:w].rjust(w)


# ── 顯示寬度感知補白（規則 B）：f-string 的 {x:w} 只算 code point，CJK/emoji 在瀏覽器
#    fallback 字型下常不是精準 2×等寬格寬，故看板主表改走規則 A（欄位全 ASCII，見下）；
#    _pad() 是終端機顯示層的再一道防呆，用 unicodedata.east_asian_width 抓 W/F 全形字元
#    ＋常見 emoji/符號區塊（≥U+1F300、Misc Symbols U+2600-27BF／U+2B00-2BFF）算 2 格。
def _char_width(ch: str) -> int:
    o = ord(ch)
    if o >= 0x1F300 or 0x2600 <= o <= 0x27BF or 0x2B00 <= o <= 0x2BFF:
        return 2
    return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1


def _display_width(s: str) -> int:
    return sum(_char_width(c) for c in s)


def _pad(s, w: int, right: bool = False) -> str:
    s = str(s)
    fill = " " * max(0, w - _display_width(s))
    return (fill + s) if right else (s + fill)


# ── 規則 A：等寬看板 note 欄以左一律 ASCII 代碼（timing/seat/dd/moat），保證任何
#    字型都對齊；中文只留在 note（最後一欄，無需再對齊）與圖例行（表頭上方 prose）。
TIMING_CODE = {"breakout": "BRK", "pullback": "PB", "in_trend": "TR",
               "overheated": "HOT", None: "DN"}
TIMING_TXT = {"breakout": "🟢 突破帶", "pullback": "🟢 回踩", "in_trend": "🟡 趨勢內",
              "overheated": "🟠 過熱", None: "🔴 52 週線下／缺"}   # HTML 表格（seat_tr 等）另用 P_LABEL_HTML，此表僅供未來 board 之外的中文呈現備用

_ROLE_CODE = {"核心": "core", "核心持倉": "core", "條件式核心持倉": "core",
              "衛星": "sat", "衛星持倉": "sat", "追蹤": "trk", "追蹤池": "trk", "不持有": ""}
_ARROW_ASCII = {"↑": "+", "→": "=", "↓": "-", "": ""}

# 等寬看板欄寬（header 與資料列共用同一組常數，保證 note 欄起始 index 對齊）
W_IDX, W_TICKER, W_SCORE, W_GROW = 2, 9, 5, 6
W_EY, W_ROIC, W_FCF, W_PEG, W_REV = 5, 5, 5, 5, 6
W_TIMING, W_SEAT, W_DD, W_MOAT = 6, 4, 19, 4


def _role_code(role) -> str:
    role = role or ""
    if role in _ROLE_CODE:
        return _ROLE_CODE[role]
    if "核心" in role:
        return "core"
    if "衛星" in role or "投機" in role:
        return "sat"
    if "追蹤" in role or "候選" in role:
        return "trk"
    return ""


def dd_ascii(r: dict) -> str:
    """等寬看板專用 ASCII 版 dd_tag——從列的 verdict/role/dd_age_days 直接映射，不 parse
    中文 dd_tag 字串。IN/WATCH/AVOID(/role) Nd；legacy＝舊版無裁決；none＝無 DD；
    >180 天（同 DD_FRESH_DAYS 門檻）附加 !old。"""
    verdict = r.get("verdict")
    if not verdict:
        return "legacy" if r.get("dd_path") else "none"
    if verdict.startswith("進場"):
        code = "IN"
    elif verdict == "觀望":
        code = "WATCH"
    elif verdict == "迴避":
        code = "AVOID"
    else:
        code = "?"
    rc = _role_code(r.get("role"))
    tag = f"{code}/{rc}" if rc else code
    age = r.get("dd_age_days")
    if age is not None:
        tag += f" {int(age)}d"
        if age > DD_FRESH_DAYS:
            tag += "!old"
    return tag


def moat_ascii(m) -> str:
    """護城河欄 ASCII 化：箭頭→ +/=/-（升/平/降），缺值→ -。"""
    if not m or m == "—":
        return "-"
    grade, arrow = m[0], m[1:]
    return f"{grade}{_ARROW_ASCII.get(arrow, '')}"


def render_board_text(as_of, rows, core_seats, sat_seats, prev_snap, entered) -> str:
    """附錄 B 式等寬看板（持有人 2026-09-02 指定形式；2026-09-02 對齊修正）：擁有層排序表
    ＋席位對照＋DD 進場 vs 機械資格＋無 DD 過閘候選。純文字，同時寫 docs/engine/board.txt
    與 <pre> 嵌頁（docs/engine/_arena_body.html、docs/cockpit/index.html 皆讀同一份文字）。

    對齊規則：瀏覽器對 CJK 常用 fallback 字型，其字寬不保證是等寬字型 cell 的精準 2 倍，
    f-string {x:w} 補白也只算 code point 不算顯示寬度——兩者都會讓含中文/emoji 的欄位
    在瀏覽器 <pre> 裡跑版。故主表 note 欄以左（#/ticker/score/grow/EY/ROIC/FCF/PEG/
    rev1m/timing/seat/dd/moat）一律 ASCII 代碼，任何字型都保證對齊；中文只留在最後的
    note 欄（不需要再對齊）與表頭上方的圖例行（純 prose，非欄位）。"""
    seat_of = {r["ticker"]: "核心席" for r in core_seats}
    seat_of.update({r["ticker"]: "衛星席" for r in sat_seats})
    seat_code = {r["ticker"]: f"C{j}" for j, r in enumerate(core_seats, 1)}
    seat_code.update({r["ticker"]: f"S{j}" for j, r in enumerate(sat_seats, 1)})
    prev_seats = {t: "核心席" for t in prev_snap.get("core", [])}
    prev_seats.update({t: "衛星席" for t in prev_snap.get("sat", [])})
    track_code = {"核心席": "C", "衛星席": "S"}

    def tk(t) -> str:
        return _pad(str(t)[:W_TICKER], W_TICKER)

    L = []
    L.append(f"選股看板 v2｜as_of {as_of}｜母體 {len(rows)}（DD 池＋QGM 無 DD＋快審卡）"
             "｜母體＝美股含 ADR；台股另建（.TW 不在本看板）")
    L.append("甲 擁有層｜資格：品質閘 ROIC≥15∧FCF≥10（或 ROIC≥25∧FCF≥0）× 成長閘 ≥15 × 市值 ≥$20B"
             "｜排序＝min(成長，30)＋FY1 盈餘殖利率（ROIC≥30 +2；PEG>2 −5）｜時機燈獨立、不進排序")
    L.append("欄位說明：score＝擁有層分、grow＝FY1→FY3 成長%、EY＝FY1 盈餘殖利率%、rev1m＝FY+1 單月修正%、"
             "timing＝時機燈、seat＝席位、dd＝DD 標籤、moat＝護城河；note＝註記")
    L.append("timing 代碼：BRK＝突破帶、PB＝回踩、TR＝趨勢內、HOT＝過熱、DN＝52 週線下或缺"
             "｜seat：C1-C5＝核心席次、S1-S5＝衛星席次｜moat：字母＝評級，+/=/-＝護城河趨勢升/平/降"
             "｜dd：IN/WATCH/AVOID/legacy/none，core/sat/trk＝角色，Nd＝天數，!old＝逾 180 天過期")
    hdr = (f"{'#':>{W_IDX}} {'ticker':<{W_TICKER}} {'score':>{W_SCORE}} {'grow':>{W_GROW}} "
           f"{'EY':>{W_EY}} {'ROIC':>{W_ROIC}} {'FCF':>{W_FCF}} {'PEG':>{W_PEG}} {'rev1m':>{W_REV}} "
           f"{'timing':<{W_TIMING}} {'seat':<{W_SEAT}} {'dd':<{W_DD}} {'moat':<{W_MOAT}} note")
    L.append(hdr)
    own = [r for r in rows if (r["grp"].get("quality") or {}).get("pass") and (r["score"] or 0) > 0]
    for i, r in enumerate(own[:40], 1):
        g = r["grp"]; o = g.get("own") or {}
        note = "；".join(list(g.get("why") or [])[:2])
        if r.get("g_method") == "FY1→FY2 單年":
            note = ("成長=FY1→FY2 單年；" + note) if note else "成長=FY1→FY2 單年"
        if r.get("hyst") and "候補" in r["hyst"]:
            note = (r["hyst"] + "；" + note) if note else r["hyst"]
        L.append(
            f"{i:>{W_IDX}} {tk(r['ticker'])} {_n(r['score'], W_SCORE)} {_n(g.get('g'), W_GROW)} "
            f"{_n(o.get('ey'), W_EY)} {_n(r.get('roic'), W_ROIC)} {_n(r.get('fcf'), W_FCF)} "
            f"{_n(r.get('peg'), W_PEG, 2)} {_n(g.get('r_fy1'), W_REV)} "
            f"{_pad(TIMING_CODE.get(g.get('p_label'), 'DN'), W_TIMING)} "
            f"{_pad(seat_code.get(r['ticker'], ''), W_SEAT)} "
            f"{_pad(dd_ascii(r)[:W_DD], W_DD)} {_pad(moat_ascii(r.get('moat')), W_MOAT)} {note}"
        )
    L.append("")
    L.append("== 席位（核心 5／衛星 5）與上期對照")
    for track, seats in (("核心席", core_seats), ("衛星席", sat_seats)):
        for j, r in enumerate(seats, 1):
            if prev_seats.get(r["ticker"]) == track:
                chg = ""
            elif r["ticker"] not in prev_seats:
                chg = "NEW"
            else:
                chg = f"FROM:{track_code.get(prev_seats[r['ticker']], '?')}"
            L.append(
                f"  {track_code[track]}{j} {tk(r['ticker'])} {_n(r['score'], W_SCORE)} "
                f"{_pad(TIMING_CODE.get(r['grp'].get('p_label'), 'DN'), W_TIMING)} "
                f"{_pad(dd_ascii(r)[:W_DD], W_DD)} {_pad(chg, 6)} {r.get('hyst') or ''}"
            )
    gone = [t for t in prev_seats if t not in seat_of]
    if gone:
        why = {r["ticker"]: r for r in rows}
        for t in gone:
            r = why.get(t)
            why_txt = "；".join((((r or {}).get("grp") or {}).get("why") or [])[:2]) or ("擁有層分數被擠下" if r else "不在母體")
            L.append(f"  DOWN {tk(t)} {(r or {}).get('hyst') or ''}：{why_txt}")
    L.append("")
    L.append("== DD 裁決進場 vs 機械資格")
    ok = [r for r in entered if r["grp"]["pass"]]; ng = [r for r in entered if not r["grp"]["pass"]]
    L.append(f"  進場 {len(entered)}：過閘 {len(ok)}／未過 {len(ng)}")
    for r in ng:
        L.append(
            f"   X {tk(r['ticker'])} {_pad(TIMING_CODE.get(r['grp'].get('p_label'), 'DN'), W_TIMING)} "
            f"{'；'.join((r['grp'].get('why') or [])[:3])}"
        )
    L.append("")
    L.append("== 無 DD 而機械過閘（DD 選配層的候選；有興趣才跑 DD）")
    for r in own:
        if r.get("src") == "qgm" and r["grp"]["pass"]:
            L.append(
                f"   {tk(r['ticker'])} score {_n(r['score'], W_SCORE)} grow {_n(r['grp'].get('g'), W_GROW)} "
                f"ROIC {_n(r.get('roic'), W_ROIC)} PEG {_n(r.get('peg'), W_PEG, 2)} "
                f"{_pad(TIMING_CODE.get(r['grp'].get('p_label'), 'DN'), W_TIMING)} {r.get('hyst') or ''}"
            )
    return "\n".join(L) + "\n"


# ── HTML 版看板（2026-09-02，持有人否決 ASCII <pre>：燈號不見、欄位對不齊）─────────────
# board.txt（render_board_text，above）保留給終端機／郵件；瀏覽器一律走這裡的 HTML TABLE
# ——對齊交給瀏覽器排版引擎，欄位不再需要手動補白，顏色燈號也能回來。輸出是「裸片段」
# （單一 <div class="board-wrap">…</div>，樣式自帶 scoped <style>），不含 html/head/body，
# 可直接：① innerHTML 塞進 cockpit #roster-mount；② 原樣接進 page_embed_shell() 產的
# _arena_body.html body（後者另有 common.py PAGE_CSS，兩邊 class 名不衝突，token 共用
# /assets/imq-base.css，故顏色與字體在兩處視覺一致）。

_TIMING_HTML = {   # p_label -> (dot, 中文, 色系)；色系對應 bw-pill-{cls}
    "breakout": ("🟢", "突破帶", "up"),
    "pullback": ("🟢", "回踩", "up"),
    "in_trend": ("🟡", "趨勢內", "neu"),
    "overheated": ("🟠", "過熱", "warn"),
}

# note 欄 chip 化：why[] 裡固定句型 -> (短 chip 文字, 原句當 title)。順序即比對順序，
# 不影響輸出順序（輸出仍照 why[] 原順序，此表只負責「認出這句要不要變 chip」）。
_CHIP_PATTERNS = [
    (re.compile(r"^市值資料缺漏"), lambda w, m: "市值待補"),
    (re.compile(r"^市值 (\d+)B 低於門檻 (\d+)B"), lambda w, m: f"市值 <{m.group(2)}B"),
    (re.compile(r"^位置閘：過熱（26 週 ([+-]?\d+)%）"), lambda w, m: f"過熱 {m.group(1)}%"),
    (re.compile(r"^位置閘未過"), lambda w, m: "線下"),
    (re.compile(r"^品質閘 ROIC (\S+)"), lambda w, m: f"品質閘 ROIC {m.group(1)}"),
    (re.compile(r"^品質閘 FCF (\S+)"), lambda w, m: f"品質閘 FCF {m.group(1)}"),
    (re.compile(r"^成長閘用 2 年成長率代替"), lambda w, m: "2Y 代替"),
    (re.compile(r"^成長閘未過"), lambda w, m: "成長閘"),
    (re.compile(r"^上修閘保守否決"), lambda w, m: "上修否決"),
    (re.compile(r"^上修閘否決"), lambda w, m: "上修否決"),
    (re.compile(r"^DD 迴避"), lambda w, m: "DD 迴避"),
    (re.compile(r"^硬 veto 下席"), lambda w, m: "硬 veto"),
]


def _match_chip(w: str):
    for pat, fn in _CHIP_PATTERNS:
        m = pat.match(w)
        if m:
            return fn(w, m), w
    return None


def _chip_html(short: str, title: str) -> str:
    return f'<span class="bw-chip" title="{escape(title)}">{escape(short)}</span>'


def _chips_html(chips: list, cap: int = 3) -> str:
    if not chips:
        return '<span class="bw-muted">—</span>'
    vis, extra = chips[:cap], chips[cap:]
    out = "".join(_chip_html(s, t) for s, t in vis)
    if extra:
        more_title = "；".join(f"{s}：{t}" for s, t in extra)
        out += _chip_html(f"+{len(extra)}", more_title)
    return out


def _note_chips(r: dict) -> list:
    """單列的完整 chip 清單（未截斷）：why[] 逐句比對 ＋ g_method（QGM 單年代替）
    ＋ hyst（候補／觀察中）。輸出順序＝why 原順序（否決/市值/過熱等最先），其後補兩類狀態 chip。"""
    chips, seen = [], set()
    def add(short, title):
        if short in seen:
            return
        seen.add(short); chips.append((short, title))
    for w in ((r.get("grp") or {}).get("why") or []):
        c = _match_chip(w)
        if c:
            add(*c)
    if r.get("g_method") == "FY1→FY2 單年":
        add("成長=單年", "QGM 品質池：以 FY1→FY2 單年成長率代替 FY1→FY3 CAGR（缺 FY3 預估）")
    hy = r.get("hyst") or ""
    if "候補" in hy:
        m = re.search(r"(\d+)/(\d+)", hy)
        add(f"候補 {m.group(1)}/{m.group(2)}" if m else "候補", hy)
    elif "觀察中" in hy:
        add("觀察中", hy)
    return chips


def _chips_from_why(why_list, limit: int = 3) -> list:
    """通用版（不含 g_method／hyst）：給 DD-vs-機械資格、下席原因等只有 why[] 可用的表格。"""
    out = []
    for w in (why_list or [])[:limit]:
        c = _match_chip(w)
        out.append(c if c else (w[:14] + ("…" if len(w) > 14 else ""), w))
    return out


def _num(v, d: int = 1) -> str:
    if v is None:
        return '<span class="bw-muted">—</span>'
    try:
        return f"{float(v):.{d}f}"
    except (TypeError, ValueError):
        return '<span class="bw-muted">—</span>'


def _timing_pill(p_label, r26, dist_hi) -> str:
    dot, label, cls = _TIMING_HTML.get(p_label, ("🔴", "線下", "dn"))
    bits = []
    if r26 is not None:
        bits.append(f"26 週漲幅 {r26:+.1f}%")
    if dist_hi is not None:
        bits.append(f"距 52 週高 {dist_hi:+.1f}%")
    title = "；".join(bits) or "時機資料缺"
    return f'<span class="bw-pill bw-pill-{cls}" title="{escape(title)}">{dot} {escape(label)}</span>'


def _rev_pill(r_fy1) -> str:
    if r_fy1 is None:
        return '<span class="bw-pill bw-pill-mut">—</span>'
    if r_fy1 >= 5:
        return f'<span class="bw-pill bw-pill-up">🟢 {r_fy1:+.1f}%</span>'
    if r_fy1 <= -10:
        return f'<span class="bw-pill bw-pill-dn">🔴 否決 {r_fy1:+.1f}%</span>'
    return f'<span class="bw-pill bw-pill-neu">⚪ {r_fy1:+.1f}%</span>'


def _dd_pill(tag) -> str:
    if not tag:
        return '<span class="bw-pill bw-pill-mut">—</span>'
    if "進場" in tag:
        cls = "up"
    elif "觀望" in tag:
        cls = "neu"
    elif "迴避" in tag:
        cls = "dn"
    else:
        cls = "mut"
    return f'<span class="bw-pill bw-pill-{cls}">{escape(tag)}</span>'


def _tk_link(r: dict) -> str:
    tk = escape(r["ticker"])
    return f'<a href="{escape(r["dd_path"])}#decision">{tk}</a>' if r.get("dd_path") else tk


_BOARD_CSS = """<style>
.board-wrap{font-family:var(--sans,-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans TC",sans-serif);
  color:var(--ink,var(--text,#1a1a1a));font-size:13px;line-height:1.55}
.board-wrap .bw-head{font-size:14.5px;font-weight:700;color:var(--ink,var(--text,#1a1a1a))}
.board-wrap .bw-rule{font-size:11.5px;color:var(--sec,var(--text-sec,#666));margin:2px 0 10px}
.board-wrap h3.bw-sec{font-family:var(--serif,'Playfair Display','Noto Serif TC',Georgia,serif);
  font-size:15px;font-weight:700;color:var(--ink,var(--text,#1a1a1a));margin:20px 0 3px}
.board-wrap .bw-sub{font-size:11.5px;color:var(--sec,var(--text-sec,#666));margin:0 0 8px}
.board-wrap .bw-scroll{overflow-x:auto;border:1px solid var(--line,var(--border,#ddd));
  border-radius:var(--r,8px);background:var(--card,#fff)}
.board-wrap table{width:100%;border-collapse:collapse;font-size:12.5px}
.board-wrap th{font-family:var(--mono,'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace);
  font-size:10.5px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;
  color:var(--sec,var(--text-sec,#666));text-align:right;padding:6px 8px;
  border-bottom:1px solid var(--line,var(--border,#ddd));white-space:nowrap;cursor:help}
.board-wrap th.bw-l,.board-wrap td.bw-l{text-align:left}
.board-wrap td{padding:5px 8px;text-align:right;border-bottom:1px solid var(--line-soft,var(--border,#eee));
  white-space:nowrap;font-family:var(--mono,'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace);
  font-variant-numeric:tabular-nums}
.board-wrap td.bw-note{white-space:normal;text-align:left;font-family:var(--sans,inherit);min-width:160px}
.board-wrap tr.bw-seated td{background:var(--paper,rgba(0,0,0,.025))}
.board-wrap tbody tr:hover td{background:var(--line-soft,rgba(0,0,0,.03))}
.board-wrap .bw-muted{color:var(--muted,#999)}
.board-wrap a{color:var(--accent,#0d2244);font-weight:650;text-decoration:none}
.board-wrap a:hover{text-decoration:underline}
.board-wrap .bw-pill{display:inline-block;font-family:var(--mono,'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace);
  font-size:10.5px;font-weight:600;border-radius:5px;padding:1px 6px;white-space:nowrap}
.board-wrap .bw-pill-up{background:#eafaef;color:var(--pos,#15803d)}
.board-wrap .bw-pill-dn{background:#fbeceb;color:var(--neg,#b91c1c)}
.board-wrap .bw-pill-neu{background:#fbf3df;color:var(--warn,#a16207)}
.board-wrap .bw-pill-warn{background:#fdeedb;color:#c2610a}
.board-wrap .bw-pill-mut{background:var(--line-soft,#eee);color:var(--muted,#999)}
.board-wrap .bw-chip{display:inline-block;font-size:10.5px;font-family:var(--sans,inherit);
  color:var(--sec,var(--text-sec,#666));background:var(--line-soft,rgba(0,0,0,.045));
  border-radius:4px;padding:1px 6px;margin:0 3px 3px 0;cursor:help}
.board-wrap .bw-chip-more{color:var(--muted,#999)}
.board-wrap .bw-note-line{font-size:12px;color:var(--sec,var(--text-sec,#666));margin-top:8px;line-height:1.75}
.board-wrap .bw-note-line b{color:var(--ink,var(--text,#1a1a1a))}
@media(max-width:760px){.board-wrap table{font-size:11.5px}.board-wrap th,.board-wrap td{padding:4px 6px}}
</style>"""


def render_board_html(as_of, rows, core_seats, sat_seats, prev_snap, entered) -> str:
    """HTML TABLE 版看板（2026-09-02，取代 <pre> ASCII——持有人否決理由：對齊靠瀏覽器排版
    引擎解決，燈號用顏色不用代碼）。回傳裸片段（無 html/head/body），可直接 innerHTML 或
    接進另一頁 <body>。內容與 render_board_text 同源同排序，只是呈現層換成表格＋燈號＋chip。"""
    seat_label = {}
    for i, r in enumerate(core_seats, 1):
        seat_label[r["ticker"]] = f"核心 {i}"
    for i, r in enumerate(sat_seats, 1):
        seat_label[r["ticker"]] = f"衛星 {i}"

    own = [r for r in rows if (r["grp"].get("quality") or {}).get("pass") and (r["score"] or 0) > 0][:40]

    thead = ("<tr>"
             '<th title="排序名次">#</th>'
             '<th class="bw-l" title="點擊連到該股 DD #decision 錨點（若有 v13+ DD）">Ticker</th>'
             '<th title="擁有層分＝min(成長,30)＋FY1 盈餘殖利率（ROIC≥30 持續期 +2；PEG>2 罰 −5）——排序鍵">擁有層分</th>'
             '<th title="FY1→FY3 EPS CAGR（缺 FY3 用 2 年成長率代替）">成長%</th>'
             '<th title="FY1 盈餘殖利率＝100 ÷ FY1 P/E">EY%</th>'
             '<th title="投入資本回報率 ROIC">ROIC%</th>'
             '<th title="自由現金流利潤率">FCF%</th>'
             '<th title="PEG＝FY1 P/E ÷ 成長%">PEG</th>'
             '<th title="FY+1 單月 EPS 修正——燈號不參與排序；≤−10% 為資格否決線">上修燈</th>'
             '<th title="52 週位置與熱度燈號——不參與排序，見各燈 title">時機燈</th>'
             '<th class="bw-l" title="目前坐核心／衛星席次；空白＝未坐席">席</th>'
             '<th class="bw-l" title="DD 裁決標籤——只做 veto（迴避）與角色標籤，不參與排序；⚠過期＝逾 180 天">DD</th>'
             '<th class="bw-l" title="護城河評級與趨勢：字母＝評級，↑升 →平 ↓降">護城河</th>'
             '<th class="bw-l" title="資格閘未過／狀態摘要，完整原因見各 chip title">註記</th>'
             "</tr>")

    body_rows = []
    for i, r in enumerate(own, 1):
        g = r["grp"]; o = g.get("own") or {}
        tk = r["ticker"]
        seated = tk in seat_label
        seat_cell = escape(seat_label[tk]) if seated else '<span class="bw-muted">—</span>'
        moat = r.get("moat") or "—"
        moat_cell = escape(moat) if moat != "—" else '<span class="bw-muted">—</span>'
        body_rows.append(
            f'<tr{" class=\"bw-seated\"" if seated else ""}>'
            f"<td>{i}</td>"
            f'<td class="bw-l"><strong>{_tk_link(r)}</strong></td>'
            f"<td>{_num(r.get('score'), 1)}</td>"
            f"<td>{_num(g.get('g'), 1)}</td>"
            f"<td>{_num(o.get('ey'), 1)}</td>"
            f"<td>{_num(r.get('roic'), 1)}</td>"
            f"<td>{_num(r.get('fcf'), 1)}</td>"
            f"<td>{_num(r.get('peg'), 2)}</td>"
            f"<td>{_rev_pill(g.get('r_fy1'))}</td>"
            f"<td>{_timing_pill(g.get('p_label'), r.get('r26'), g.get('dist_hi'))}</td>"
            f'<td class="bw-l">{seat_cell}</td>'
            f'<td class="bw-l">{_dd_pill(r.get("dd_tag"))}</td>'
            f'<td class="bw-l">{moat_cell}</td>'
            f'<td class="bw-note">{_chips_html(_note_chips(r))}</td>'
            "</tr>")

    main_tbl = ('<div class="bw-scroll"><table><thead>' + thead + "</thead><tbody>"
                + "".join(body_rows) + "</tbody></table></div>")

    # ── 席位對照 ──
    prev_seats = {t: "核心席" for t in prev_snap.get("core", [])}
    prev_seats.update({t: "衛星席" for t in prev_snap.get("sat", [])})
    track_code = {"核心席": "C", "衛星席": "S"}
    seat_thead = ("<tr><th class=\"bw-l\">席</th><th class=\"bw-l\">Ticker</th>"
                  "<th>擁有層分</th><th class=\"bw-l\">時機燈</th>"
                  "<th class=\"bw-l\">DD</th><th class=\"bw-l\">遲滯</th></tr>")
    seat_rows = []
    for track_label, seats, code_letter in (("核心席", core_seats, "C"), ("衛星席", sat_seats, "S")):
        for j, r in enumerate(seats, 1):
            g = r["grp"]
            if prev_seats.get(r["ticker"]) == track_label:
                chg = ""
            elif r["ticker"] not in prev_seats:
                chg = "NEW"
            else:
                chg = f'FROM:{track_code.get(prev_seats[r["ticker"]], "?")}'
            hyst_txt = (f'<span class="bw-chip" title="本期新換入或跨軌轉入">{escape(chg)}</span> ' if chg else "") \
                       + escape(r.get("hyst") or "—")
            seat_rows.append(
                f'<tr><td class="bw-l">{code_letter}{j}</td>'
                f'<td class="bw-l"><strong>{_tk_link(r)}</strong></td>'
                f"<td>{_num(r.get('score'), 1)}</td>"
                f'<td class="bw-l">{_timing_pill(g.get("p_label"), r.get("r26"), g.get("dist_hi"))}</td>'
                f'<td class="bw-l">{_dd_pill(r.get("dd_tag"))}</td>'
                f'<td class="bw-l">{hyst_txt}</td></tr>')
    seat_tbl = ('<div class="bw-scroll"><table><thead>' + seat_thead + "</thead><tbody>"
                + "".join(seat_rows) + "</tbody></table></div>")

    gone = [t for t in prev_seats if t not in seat_label]
    if gone:
        why_map = {r["ticker"]: r for r in rows}
        lines = []
        for t in gone:
            r = why_map.get(t)
            why = (((r or {}).get("grp") or {}).get("why") or [])
            chips = _chips_from_why(why, limit=2) if why else []
            reason = _chips_html(chips) if chips else '<span class="bw-muted">擁有層分數被擠下／不在母體</span>'
            lines.append(f'<div class="bw-note-line">🔻 DOWN <b>{escape(t)}</b>'
                         f'（{escape((r or {}).get("hyst") or "—")}）：{reason}</div>')
        changes_html = "".join(lines)
    else:
        changes_html = '<div class="bw-note-line">本期無下席變動。</div>'

    # ── DD 進場 vs 機械資格 ──
    ok_n = sum(1 for r in entered if r["grp"]["pass"])
    ng = [r for r in entered if not r["grp"]["pass"]]
    dd_gate_sub = f"進場 {len(entered)}：過閘 {ok_n}／未過 {len(ng)}"
    if ng:
        ng_thead = '<tr><th class="bw-l">Ticker</th><th class="bw-l">時機燈</th><th class="bw-l">原因</th></tr>'
        ng_rows = []
        for r in ng:
            g = r["grp"]
            ng_rows.append(
                f'<tr><td class="bw-l"><strong>{_tk_link(r)}</strong></td>'
                f'<td class="bw-l">{_timing_pill(g.get("p_label"), r.get("r26"), g.get("dist_hi"))}</td>'
                f'<td class="bw-note">{_chips_html(_chips_from_why(g.get("why")))}</td></tr>')
        ng_tbl = ('<div class="bw-scroll"><table><thead>' + ng_thead + "</thead><tbody>"
                  + "".join(ng_rows) + "</tbody></table></div>")
    else:
        ng_tbl = '<div class="bw-note-line">進場票全數過機械三閘，無需人工複審。</div>'

    # ── 無 DD 而機械過閘（DD 選配層候選） ──
    qgm_cands = [r for r in own if r.get("src") == "qgm" and r["grp"]["pass"]]
    if qgm_cands:
        q_thead = ('<tr><th class="bw-l">Ticker</th><th>分</th><th>成長%</th><th>ROIC%</th>'
                   '<th>PEG</th><th class="bw-l">時機燈</th><th class="bw-l">遲滯</th></tr>')
        q_rows = []
        for r in qgm_cands:
            g = r["grp"]
            q_rows.append(
                f'<tr><td class="bw-l"><strong>{_tk_link(r)}</strong></td>'
                f"<td>{_num(r.get('score'), 1)}</td><td>{_num(g.get('g'), 1)}</td>"
                f"<td>{_num(r.get('roic'), 1)}</td><td>{_num(r.get('peg'), 2)}</td>"
                f'<td class="bw-l">{_timing_pill(g.get("p_label"), r.get("r26"), g.get("dist_hi"))}</td>'
                f'<td class="bw-l">{escape(r.get("hyst") or "—")}</td></tr>')
        qgm_tbl = ('<div class="bw-scroll"><table><thead>' + q_thead + "</thead><tbody>"
                   + "".join(q_rows) + "</tbody></table></div>")
    else:
        qgm_tbl = '<div class="bw-note-line">目前無候選（QGM 品質池名字皆已有 DD 或未過機械三閘）。</div>'

    head_line = f"選股看板 v2 · as_of {as_of} · 母體 {len(rows)}（美股含 ADR；台股另建）"
    rule_line = ("排序＝擁有層分（min(成長，30)＋FY1 盈餘殖利率；ROIC≥30 +2；PEG>2 −5）"
                 "· 資格＝品質閘×成長閘×市值 · 時機燈不進排序 · DD 只 veto／角色")

    return (
        '<div class="board-wrap">' + _BOARD_CSS
        + f'<div class="bw-head">{escape(head_line)}</div>'
        + f'<div class="bw-rule">{escape(rule_line)}</div>'
        + main_tbl
        + '<h3 class="bw-sec">席位對照</h3>'
        + '<div class="bw-sub">C1–C5＝核心席次、S1–S5＝衛星席次；NEW＝本期新換入、FROM:X＝跨軌轉入。</div>'
        + seat_tbl + changes_html
        + '<h3 class="bw-sec">DD 進場 vs 機械資格</h3>'
        + f'<div class="bw-sub">{escape(dd_gate_sub)}——過閘者已在席位或候補中，這裡只列未過者供人工複審。</div>'
        + ng_tbl
        + '<h3 class="bw-sec">無 DD 而機械過閘（DD 選配層候選）</h3>'
        + '<div class="bw-sub">QGM 品質池名字，機械三閘全過但尚無 DD 裁決——有興趣才跑 DD。</div>'
        + qgm_tbl
        + '<div class="bw-note-line">同內容另存純文字版 <a href="/engine/board.txt">board.txt</a>（終端機／郵件用）。</div>'
        + "</div>"
    )


def main() -> int:
    stocks = json.loads(DD_LATEST.read_text(encoding="utf-8"))["stocks"]
    # latest.json 若以 --include-non-dd 產出，無 DD 列（dd_status="none"）改由 load_qgm_rows 供給
    #（帶 _src／_durable_5y／_mktcap），這裡先排除以免搶走 QGM 列的身份標記
    stocks = [s for s in stocks if s.get("dd_status") != "none"]
    # 2026-09-02 持有人拍板：v2 先只做美股（含 ADR），台股另建獨立系統——母體排除 .TW
    stocks = [s for s in stocks if market_ok(s["ticker"])]
    try:
        sectors = {r["ticker"]: r["sector"]
                   for r in json.loads(UNIVERSE.read_text(encoding="utf-8"))["tickers"]}
    except (OSError, json.JSONDecodeError, KeyError):
        sectors = {}
    try:
        card_stats = json.loads(CARDS_JSON.read_text(encoding="utf-8")).get("by_ticker", {})
    except (OSError, json.JSONDecodeError):
        card_stats = {}

    # ── v2 席位資格（2026-09-02）：擁有層 ∩ 時機層，DD 只做 veto／角色標籤 ──
    #   母體＝DD 池（全部裁決，迴避者 veto）∪ QGM 品質池無 DD 名字（US＋TW）∪ 快審卡
    #   資格＝品質閘（ROIC/FCF）∩ G 成長閘 ∩ 市值 ∩ P 位置閘（未過熱）∩ 無重下修否決
    #   排序＝own_score（擁有層），R 上修只作燈號；遲滯：新席連 2 次過、現任連 4 次不過才下
    #   （DD 180 天內觀望之現任席降權為連 2 次不過即下，B4② 2026-09-04）
    stocks_map = {s["ticker"]: s for s in stocks}
    # 同一家公司的 ADR／本地掛牌只留一個（席位不得重複曝險）：本地掛牌讓位給 ADR
    aliased = set()
    for local, adr in LISTING_ALIAS.items():
        if adr in stocks_map:
            stocks_map.pop(local, None); aliased.add(local)
    stocks = [s for s in stocks if s["ticker"] in stocks_map]
    qgm_rows = load_qgm_rows(stocks_map, exclude=aliased)
    universe_rows = [row_dict(s) for s in stocks] + [row_dict(s) for s in qgm_rows]
    light = load_light_rows(stocks_map)
    universe_rows += [r for r in light if r["verdict"] in ("進場", "觀望", None)]

    # 兩源一致性防線：任一源重下修即否決＋方向矛盾標記
    yf_map = _yf_rev_map()
    universe_rows = [cross_check_r(r, yf_map.get(r["ticker"])) for r in universe_rows]

    # 市值門檻（持有人拍板 ≥$200 億）：席位/挑戰者資格層——未達或未知者降板凳並列原因
    qgm_caps = {s["ticker"]: s.get("_mktcap") for s in qgm_rows}
    caps = fetch_caps(sorted({r["ticker"] for r in universe_rows if r["ticker"] not in qgm_caps}))
    for k, v in qgm_cap_map().items():          # fallback：yfinance 缺漏時用 QGM 市值
        if v and not caps.get(k):
            caps[k] = v
    caps.update({k: v for k, v in qgm_caps.items() if v})
    def apply_cap(r):
        r["mktcap"] = caps.get(r["ticker"])
        ok = cap_ok(r["mktcap"])
        r["cap_ok"] = bool(ok)
        if not ok:
            r["grp"] = dict(r["grp"])
            r["grp"]["pass"] = False
            r["grp"]["why"] = (["市值資料缺漏，資格從嚴不予通過"] if ok is None
                               else [f"市值 {r['mktcap']/1e9:.0f}B 低於門檻 {MKTCAP_MIN/1e9:.0f}B"]) \
                              + list(r["grp"]["why"])
        return r
    universe_rows = [apply_cap(r) for r in universe_rows]
    universe_rows.sort(key=lambda r: -(r["score"] or 0))

    # ── 遲滯（arena-ledger gate_history，append-only）──
    try:
        ledger0 = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        ledger0 = {"schema_version": "1.0", "snapshots": []}
    bootstrap = not ledger0.get("gate_history")   # 首跑：無歷史，新席只需本次過閘
    hist = ledger0.setdefault("gate_history", {})
    prev = ledger0["snapshots"][-1] if ledger0.get("snapshots") else {"core": [], "sat": []}
    incumbents = set(prev.get("core", [])) | set(prev.get("sat", []))
    try:
        as_of = json.loads(DD_LATEST.read_text(encoding="utf-8")).get("as_of", "—")
    except (OSError, json.JSONDecodeError):
        as_of = "—"
    for r in universe_rows:
        h = hist.setdefault(r["ticker"], [])
        if h and h[-1][0] == as_of:
            h[-1] = [as_of, bool(r["grp"]["pass"])]
        else:
            h.append([as_of, bool(r["grp"]["pass"])])
        del h[:-8]
    def hard_veto(r):
        return r["grp"].get("veto") or r["verdict"] == "迴避" or not r.get("cap_ok")
    def eligible(r):
        h = hist.get(r["ticker"], [])
        if r["ticker"] in incumbents:
            if hard_veto(r):
                r["hyst"] = "硬 veto 下席"; return False
            # B4② 降權版：DD 新鮮且裁決＝觀望的現任席，下席門檻用 2 次而非 4 次
            watch = bool(r.get("dd_fresh")) and r.get("verdict") == "觀望"
            fails_n = HYST_INCUMBENT_FAILS_WATCH if watch else HYST_INCUMBENT_FAILS
            tag = "（DD 觀望）" if watch else ""
            recent = [x[1] for x in h[-fails_n:]]
            if r["grp"]["pass"]:
                r["hyst"] = "現任"; return True
            if len(recent) >= fails_n and not any(recent):
                r["hyst"] = f"連 {fails_n} 次不過閘下席{tag}"; return False
            r["hyst"] = f"現任·觀察中 {len(recent)}/{fails_n}{tag}"; return True
        recent = [x[1] for x in h[-HYST_NEW_RUNS:]]
        if r["grp"]["pass"] and bootstrap:
            r["hyst"] = "新席（首跑免遲滯）"; return True
        if r["grp"]["pass"] and len(recent) >= HYST_NEW_RUNS and all(recent):
            r["hyst"] = "新席（連 2 次過閘）"; return True
        if r["grp"]["pass"]:
            r["hyst"] = f"候補·待第 2 次過閘（{len(recent)}/{HYST_NEW_RUNS}）"
        return False
    passed = [r for r in universe_rows if eligible(r)]
    passed.sort(key=lambda r: (0 if r["grp"]["pass"] else 1, -(r["score"] or 0)))   # 過閘者優先，觀察中現任其後
    failed = [r for r in universe_rows if r not in passed]
    core_pass = [r for r in passed if r["route"] == "core"]
    sat_pass = [r for r in passed if r["route"] == "satellite"]
    core_seats = core_pass[:CORE_SLOTS]
    sat_seats = sat_pass[:SAT_SLOTS]
    core_bench = core_pass[CORE_SLOTS:] + [r for r in failed if r["route"] == "core" and r["grp"]["pass"]]
    sat_bench = sat_pass[SAT_SLOTS:] + [r for r in failed if r["route"] == "satellite" and r["grp"]["pass"]]
    entered = [r for r in universe_rows if r["verdict"] == "進場"]

    seated = {r["ticker"] for r in core_seats + sat_seats}
    challengers = [r for r in universe_rows if r["grp"]["pass"] and r["ticker"] not in seated]
    challengers.sort(key=lambda r: -r["score"])

    # 擂台配對（v2）：軌別配對——核心席 vs 核心向挑戰者、衛星席 vs 衛星向挑戰者
    # （形狀降為資訊欄；moat 耐久性同級的才有資格互換）
    duels = []
    for seat in core_seats + sat_seats:
        rivals = [c for c in challengers if c["route"] == seat["route"]]
        top = rivals[0] if rivals else None
        duels.append({"seat": seat, "challenger": top,
                      "alert": bool(top and top["score"] > seat["score"])})

    # 席位產業集中度
    conc: dict[str, int] = {}
    for r in core_seats + sat_seats:
        sec = sectors.get(r["ticker"]) or "（未分類）"
        conc[sec] = conc.get(sec, 0) + 1
    n_seated = len(core_seats + sat_seats)
    conc_rows = sorted(conc.items(), key=lambda kv: -kv[1])
    max_share = (conc_rows[0][1] / n_seated * 100) if n_seated else 0

    # ── 席位變動帳本（append-only）：席位組成變了才記一筆，換席決策從此可結算 ──
    ledger = ledger0
    snap = {"date": as_of,
            "core": [r["ticker"] for r in core_seats],
            "sat": [r["ticker"] for r in sat_seats]}
    changes = []
    prev_snap = ledger["snapshots"][-1] if ledger["snapshots"] else None
    if prev_snap is None or (set(prev_snap["core"]) != set(snap["core"])
                             or set(prev_snap["sat"]) != set(snap["sat"])):
        if prev_snap:
            for track in ("core", "sat"):
                up = sorted(set(snap[track]) - set(prev_snap[track]))
                down = sorted(set(prev_snap[track]) - set(snap[track]))
                if up or down:
                    changes.append({"track": track, "in": up, "out": down,
                                    "from": prev_snap["date"], "to": snap["date"]})
            snap["changes"] = changes
        if prev_snap is None or prev_snap["date"] != snap["date"]:
            ledger["snapshots"].append(snap)
        else:
            ledger["snapshots"][-1] = snap   # 同日重跑覆蓋（冪等）
    LEDGER_JSON.parent.mkdir(parents=True, exist_ok=True)   # gate_history 每跑必寫（遲滯狀態）
    LEDGER_JSON.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    recent_changes = [c for s in ledger["snapshots"][-6:] for c in (s.get("changes") or [])]

    dial = regime_dial()
    def compact(r):
        g = r["grp"]
        return {"ticker": r["ticker"], "score": r["score"], "g": g.get("g"), "g_method": r.get("g_method"),
                "ey": (g.get("own") or {}).get("ey"), "roic": r.get("roic"), "fcf": r.get("fcf"),
                "peg": r.get("peg"), "r_fy1": g.get("r_fy1"), "p_label": g.get("p_label"),
                "r26": r.get("r26"), "pass": g.get("pass"), "why": g.get("why"),
                "route": r["route"], "dd_tag": r.get("dd_tag"), "verdict": r.get("verdict"),
                "moat": r.get("moat"), "src": r.get("src"), "hyst": r.get("hyst"), "dd_path": r.get("dd_path")}
    own_board = [compact(r) for r in universe_rows
                 if (r["grp"].get("quality") or {}).get("pass") and (r["score"] or 0) > 0][:60]
    board_text = render_board_text(as_of, universe_rows, core_seats, sat_seats, prev, entered)
    BOARD_TXT.write_text(board_text, encoding="utf-8")
    board_html = render_board_html(as_of, universe_rows, core_seats, sat_seats, prev, entered)
    BOARD_HTML.write_text(board_html, encoding="utf-8")
    payload = {
        "schema_version": "2.0",
        "method": "v2 擁有層×時機層分離（2026-09-02）：排序＝own_score；R 為燈號；DD 只 veto／角色；遲滯 2/4（DD 180 天內觀望之現任席 2，B4② 降權版 2026-09-04）",
        "universe_n": len(universe_rows),
        "seats_without_card": sorted(r["ticker"] for r in core_seats + sat_seats if r["ticker"] not in card_stats),
        "own_board": own_board,
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regime": dial,
        "core_seats": core_seats, "core_bench": core_bench[:8],
        "sat_seats": sat_seats, "sat_vacant": SAT_SLOTS - len(sat_seats),
        "duels": duels, "challengers_top": challengers[:15],
        "concentration": [{"sector": k, "n": v} for k, v in conc_rows],
        "max_sector_share_pct": round(max_share),
    }

    # ── render ──
    def card_cell(t: str) -> str:
        cs = card_stats.get(t)
        if not cs:
            return '<span class="tag tag-blind">無卡 → 抽</span>'
        bits = [f'{cs["n_claims"]} 宣稱']
        if cs["n_breach"]:
            bits.append(f'❌{cs["n_breach"]}')
        if cs["n_due"]:
            bits.append(f'⏰{cs["n_due"]}')
        if cs.get("next_deadline"):
            bits.append(f'下個到期 {cs["next_deadline"]}')
        cls = "tag-dn" if cs["n_breach"] else ("tag-blind" if cs["n_due"] else "tag-pool")
        return f'<a href="/engine/cards.html#{escape(t)}"><span class="tag {cls}">🗂 {"·".join(bits)}</span></a>'

    def _rev_html(g, r=None):
        bits = []
        if g["r_fy1"] is not None:
            bits.append(f'FY+1 {pct(g["r_fy1"])}')
        if g["r_2y"] is not None:
            bits.append(f'2Y {g["r_2y"]:+.1f}pp')
        if r is not None and r.get("r_alt_yf30d") is not None:
            bits.append(f'<span class="muted">yf30d {r["r_alt_yf30d"]:+.1f}%</span>')
        out = "　".join(bits) or '<span class="muted">—</span>'
        if r is not None and r.get("r_conflict"):
            out += ' <span class="tag tag-blind" title="Koyfin 與 yfinance 修正方向相反">⚠ 源分歧</span>'
        return out

    def seat_tr(r, seat_no=None):
        g = r["grp"]
        link = f'<a href="{escape(r["dd_path"])}#decision">{escape(r["ticker"])}</a>' if r.get("dd_path") else escape(r["ticker"])
        if r.get("qual") == "light":
            link += f'<a href="/engine/cards.html#{escape(r["ticker"])}"><span class="tag tag-pool">🪶 快審</span></a>'
        if r.get("role_mismatch"):
            link += f'<span class="tag tag-blind" title="DD 角色：{escape(r["role"])}">⚠ DD 角色異</span>'
        dist = f'（距高 {g["dist_hi"]:+.0f}%）' if g["dist_hi"] is not None else ""
        return (f'<tr><td class="left">{f"{seat_no}." if seat_no else ""} <strong>{link}</strong></td>'
                f'<td class="left">{SHAPE_LABELS.get(r["shape"], r["shape"])}</td>'
                f'<td class="left">{_rev_html(g, r)}</td>'
                f'<td>{pct(g["g"], 0, False) if g["g"] is not None else "—"}</td>'
                f'<td class="left">{P_LABEL_HTML.get(g["p_label"])}{dist}</td>'
                f'<td class="left">{escape(r["moat"])}</td>'
                f'<td class="left">{card_cell(r["ticker"])}</td></tr>')

    def duel_tr(d):
        s, c = d["seat"], d["challenger"]
        if not c:
            rhs = '<span class="muted">同形狀無挑戰者</span>'
        else:
            link = f'<a href="{escape(c["dd_path"])}#decision">{escape(c["ticker"])}</a>' if c.get("dd_path") else escape(c["ticker"])
            rhs = (f'{link}（{c["verdict"]}，上修排序分 {c["score"]:.1f}）')
        flag = '<span class="tag tag-dn">⚔ 警報</span>' if d["alert"] else '<span class="tag tag-up">守住</span>'
        return (f'<tr><td class="left"><strong>{escape(s["ticker"])}</strong>（上修排序分 {s["score"]:.1f}）</td>'
                f'<td class="left">{SHAPE_LABELS.get(s["shape"], s["shape"])}</td>'
                f'<td class="left">{rhs}</td><td>{flag}</td></tr>')

    head = ('<table><thead><tr><th class="left">席位</th><th class="left">形狀</th>'
            '<th class="left">上修閘</th><th>成長閘</th><th class="left">位置閘</th>'
            '<th class="left">護城河</th><th class="left">決策卡</th></tr></thead><tbody>')
    core_tbl = head + "".join(seat_tr(r, i) for i, r in enumerate(core_seats, 1)) + "</tbody></table>"
    for i in range(CORE_SLOTS - len(core_seats)):
        core_tbl = core_tbl.replace("</tbody>", (
            f'<tr><td class="left">{len(core_seats)+i+1}. <span class="muted">（空缺）</span></td>'
            f'<td class="left muted" colspan="6">進場核心票中無三閘全過者遞補 — 寧缺勿濫</td></tr></tbody>'), 1)
    sat_body = "".join(seat_tr(r, i) for i, r in enumerate(sat_seats, 1))
    for i in range(payload["sat_vacant"]):
        sat_body += (f'<tr><td class="left">{len(sat_seats)+i+1}. <span class="muted">（空缺）</span></td>'
                     f'<td class="left muted" colspan="6">等衛星候選同時拿到進場裁決＋三閘全過</td></tr>')
    sat_tbl = head + sat_body + "</tbody></table>"

    def bench_line(rows):
        parts = []
        for r in rows[:10]:
            g = r["grp"]
            tag = "" if g["pass"] else f'（{("；".join(g["why"][:1])) or "三閘未過"}）'
            parts.append(f'{r["ticker"]}{tag}')
        return escape("、".join(parts) or "—")
    duel_tbl = ('<table><thead><tr><th class="left">席位（分數）</th><th class="left">形狀</th>'
                '<th class="left">同形狀最強挑戰者</th><th>裁定</th></tr></thead><tbody>'
                + "".join(duel_tr(d) for d in duels) + "</tbody></table>")
    conc_html = "、".join(f'{escape(k["sector"])} ×{k["n"]}' for k in payload["concentration"])
    conc_warn = (f'<div class="note warn">⚠ 單一產業占席 {payload["max_sector_share_pct"]}%'
                 f'（>50% 集中度警戒）——擂台換人時優先考慮異產業挑戰者。</div>'
                 if payload["max_sector_share_pct"] > 50 else "")

    body = f"""<div class="hero">
<h1>席位擂台 · 組合層</h1>
<div class="hero-sub">組合才是產品：核心 {CORE_SLOTS} 席＋衛星 {SAT_SLOTS} 席，每席對決「同形狀最強挑戰者」。
⚔ 警報＝挑戰者分數超過席位 → 進<b>每月擂台的人工複審清單</b>。引擎不自動換席——換人是人的裁決。
席位資格（<b>v2 擁有層×時機層</b>，2026-09-02 持有人拍板）＝<b>品質閘</b>（ROIC ≥15 ∧ FCF ≥10；capex 週期豁免 ROIC ≥25 ∧ FCF ≥0）×
<b>成長閘</b>（FY1→FY3 EPS CAGR ≥15%）× <b>位置閘</b>（站上 52 週線且 26 週漲幅 ≤+80%）× 無重下修否決（FY+1 單月 ≤−10%）。
排序＝<b>擁有層分數</b>＝min(成長，30)＋FY1 盈餘殖利率（ROIC ≥30 +2；PEG &gt;2 −5）；上修幅度降為燈號。
<b>DD 只做 veto（迴避）與角色標籤</b>（≤180 天有效）；無 DD 名字（QGM 品質池）同場排序、標「待 DD」。
<b>遲滯</b>：新席連 2 次週跑過閘、現任連 4 次不過才下席（硬 veto 除外；DD 180 天內裁決＝觀望的現任席降權為連 2 次不過即下，B4② 2026-09-04）。
<b>軌別路由</b>：DD 角色優先；無 DD 走護城河 S/A 非↓（QGM 5 年 ROIC 穩定 ≥75% 亦可核心）；其餘衛星。
<b>市值門檻 ≥ ${MKTCAP_MIN/1e9:.0f}B</b>（持有人 2026-07-04 拍板：席位與主榜資格層；雷達發現層照掃全宇宙）。
<b>母體＝美股含 ADR；台股另建（.TW 不在本看板，2026-09-02 持有人拍板）</b>。
<b>兩級資格</b>：核心席必須完整 v14 DD；衛星席另接受 🪶 快審卡（週期位置＋陷阱＋護城河快評）。
DD 角色與機械軌別衝突標 ⚠ 供人裁。三閘未過的進場票落板凳、寧缺勿濫。</div>
<div class="asof">資料源 dd-screener latest.json ＋ QGM 品質池（US／TW）＋週線 cache ｜ v2 擁有層×時機層 ｜ 週更</div>
</div>
<div class="block"><h2>選股看板 v2</h2>
<div class="block-sub">擁有層排序（值不值得擁有）與時機燈（現在能不能動）分開讀；DD 只做 veto 與角色標籤。</div>
{board_html}</div>
<div class="stat-row">
<div class="stat"><strong>{dial['label'] if dial['level'] else '—'}</strong><span>Regime 撥盤（{dial['level'] if dial['level'] else '—'}×）</span></div>
<div class="stat"><strong>{sum(1 for d in duels if d['alert'])}</strong><span>⚔ 擂台警報</span></div>
<div class="stat"><strong>{len(core_seats)}/{CORE_SLOTS} · {len(sat_seats)}/{SAT_SLOTS}</strong><span>核心 · 衛星席位</span></div>
<div class="stat"><strong>{payload['max_sector_share_pct']}%</strong><span>最大單一產業占席</span></div>
</div>
<div class="note">Regime：{escape(dial.get('detail') or '')}（as of {escape(str(dial.get('as_of') or '—'))}）。
撥盤規則 v1 鎖定：進攻 1.0＝confirmed_uptrend 且 distribution ≤3；中性 0.5＝under_pressure 或 4–7；
防守 0.25＝correction／跌破 200DMA／≥8。<b>資訊性，不接倉位系統</b>——新倉節奏由人按撥盤自裁。
形狀敏感度：突破帶/動能重估最敏感（防守時停新倉）、循環轉折次之（防守時只留回踩單）。</div>
<div class="block"><h2>核心席位（{len(core_seats)}/{CORE_SLOTS}）</h2>{core_tbl}</div>
<div class="block"><h2>衛星席位（{len(sat_seats)}/{SAT_SLOTS}）</h2>{sat_tbl}</div>
<div class="block"><h2>擂台對戰表</h2>
<div class="block-sub">軌別配對：核心席 vs 核心向挑戰者、衛星席 vs 衛星向挑戰者（moat 耐久性同級才有資格互換；
挑戰者資格＝裁決 ∈ {{進場、觀望}} ∩ 三閘全過）。觀望挑戰者勝出＝先觸發它的複審，不是直接換。</div>
{duel_tbl}</div>
<div class="block"><h2>席位變動帳本</h2>
<div class="block-sub">append-only——席位組成變動才記一筆；有帳本，換席決策才能被結算（誰換對了、誰換錯了，91 天後對答案）。</div>
{render_seat_changes(recent_changes)}</div>
<div class="block"><h2>席位產業分布</h2><div class="block-sub">{conc_html}</div>{conc_warn}</div>
<div class="note">核心板凳（進場但未坐席）：{bench_line(core_bench)}。
衛星板凳：{bench_line(sat_bench)}。
挑戰者池 top（三閘全過）：{escape('、'.join(r['ticker'] for r in payload['challengers_top'][:10]) or '—')}。</div>"""

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ARENA_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    ARENA_HTML.write_text(
        page_embed_shell("席位擂台 · 席位排序", body,
                         "核心 5＋衛星 5 席位 vs 同形狀挑戰者的每月擂台 — regime 撥盤與集中度警戒"),
        encoding="utf-8")
    print(f"arena: regime={dial['label']} 警報={sum(1 for d in duels if d['alert'])} "
          f"核心={[r['ticker'] for r in core_seats]} 衛星={[r['ticker'] for r in sat_seats]} "
          f"集中度={payload['max_sector_share_pct']}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
