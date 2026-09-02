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
import sys
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
TWD_PER_USD = 32.0          # QGM-TW 市值（新台幣十億）換算門檻用，近似值
OVERHEAT_R26_PCT = 80.0     # 時機燈：26 週漲幅 >+80% ＝ 過熱（不進席位，只列擁有層）
LISTING_ALIAS = {"2330.TW": "TSM"}   # 本地掛牌 → ADR（同公司只留一席）
HYST_NEW_RUNS = 2           # 遲滯：新席需連 2 次週跑過閘
HYST_INCUMBENT_FAILS = 4    # 遲滯：現任席連 4 次不過閘才下席（硬 veto 除外）

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
            "role_mismatch": mismatch, "dd_tag": dd_tag(s), "dd_fresh": fresh,
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
        return "—".rjust(w)
    try:
        return f"{float(v):{w}.{d}f}"
    except (TypeError, ValueError):
        return str(v)[:w].rjust(w)


TIMING_TXT = {"breakout": "🟢 突破帶", "pullback": "🟢 回踩", "in_trend": "🟡 趨勢內",
              "overheated": "🟠 過熱", None: "🔴 52 週線下／缺"}


def render_board_text(as_of, rows, core_seats, sat_seats, prev_snap, entered) -> str:
    """附錄 B 式等寬看板（持有人 2026-09-02 指定形式）：擁有層排序表＋席位對照＋
    DD 進場 vs 機械資格＋無 DD 過閘候選。純文字，同時寫 docs/engine/board.txt 與 <pre> 嵌頁。"""
    seat_of = {r["ticker"]: "核心席" for r in core_seats}
    seat_of.update({r["ticker"]: "衛星席" for r in sat_seats})
    prev_seats = {t: "核心席" for t in prev_snap.get("core", [])}
    prev_seats.update({t: "衛星席" for t in prev_snap.get("sat", [])})
    L = []
    L.append(f"選股看板 v2｜as_of {as_of}｜母體 {len(rows)}（DD 池＋QGM 無 DD＋快審卡）"
             "｜母體＝美股含 ADR；台股另建（.TW 不在本看板）")
    L.append("甲 擁有層｜資格：品質閘 ROIC≥15∧FCF≥10（或 ROIC≥25∧FCF≥0）× 成長閘 ≥15 × 市值 ≥$20B"
             "｜排序＝min(成長，30)＋FY1 盈餘殖利率（ROIC≥30 +2；PEG>2 −5）｜時機燈獨立、不進排序")
    hdr = f"{'#':>2} {'ticker':9} {'分':>5} {'成長':>6} {'EY':>5} {'ROIC':>5} {'FCF':>5} {'PEG':>5} {'1M修':>6} {'時機':10} {'席位':6} {'DD':26} {'moat':5} 註記"
    L.append(hdr)
    own = [r for r in rows if (r["grp"].get("quality") or {}).get("pass") and (r["score"] or 0) > 0]
    for i, r in enumerate(own[:40], 1):
        g = r["grp"]; o = g.get("own") or {}
        note = "；".join(list(g.get("why") or [])[:2])
        if r.get("g_method") == "FY1→FY2 單年":
            note = ("成長=FY1→FY2 單年；" + note) if note else "成長=FY1→FY2 單年"
        if r.get("hyst") and "候補" in r["hyst"]:
            note = (r["hyst"] + "；" + note) if note else r["hyst"]
        L.append(f"{i:>2} {r['ticker']:9} {_n(r['score'])} {_n(g.get('g'),6)} {_n(o.get('ey'))} {_n(r.get('roic'))} "
                 f"{_n(r.get('fcf'))} {_n(r.get('peg'),5,2)} {_n(g.get('r_fy1'),6)} "
                 f"{TIMING_TXT.get(g.get('p_label'), '—'):10} {seat_of.get(r['ticker'], ''):6} "
                 f"{(r.get('dd_tag') or '—')[:26]:26} {(r.get('moat') or '—'):5} {note}")
    L.append("")
    L.append("== 席位（核心 5／衛星 5）與上期對照")
    for track, seats in (("核心席", core_seats), ("衛星席", sat_seats)):
        for j, r in enumerate(seats, 1):
            chg = "" if prev_seats.get(r["ticker"]) == track else ("↑新席" if r["ticker"] not in prev_seats else f"↔自{prev_seats[r['ticker']]}")
            L.append(f"  {track} {j}. {r['ticker']:8} 分 {_n(r['score'])} {TIMING_TXT.get(r['grp'].get('p_label'), '—'):8} "
                     f"{r.get('dd_tag') or '—'}  {r.get('hyst') or ''} {chg}")
    gone = [t for t in prev_seats if t not in seat_of]
    if gone:
        why = {r["ticker"]: r for r in rows}
        for tk in gone:
            r = why.get(tk)
            why_txt = "；".join((((r or {}).get("grp") or {}).get("why") or [])[:2]) or ("擁有層分數被擠下" if r else "不在母體")
            L.append(f"  ↓下席 {tk:8} {(r or {}).get('hyst') or ''}：{why_txt}")
    L.append("")
    L.append("== DD 裁決進場 vs 機械資格")
    ok = [r for r in entered if r["grp"]["pass"]]; ng = [r for r in entered if not r["grp"]["pass"]]
    L.append(f"  進場 {len(entered)}：過閘 {len(ok)}／未過 {len(ng)}")
    for r in ng:
        L.append(f"   ✗ {r['ticker']:8} {'；'.join((r['grp'].get('why') or [])[:3])}  時機 {TIMING_TXT.get(r['grp'].get('p_label'), '—')}")
    L.append("")
    L.append("== 無 DD 而機械過閘（DD 選配層的候選；有興趣才跑 DD）")
    for r in own:
        if r.get("src") == "qgm" and r["grp"]["pass"]:
            L.append(f"   {r['ticker']:8} 分 {_n(r['score'])} 成長 {_n(r['grp'].get('g'))} ROIC {_n(r.get('roic'))} "
                     f"PEG {_n(r.get('peg'),5,2)} 時機 {TIMING_TXT.get(r['grp'].get('p_label'), '—')} {r.get('hyst') or ''}")
    return "\n".join(L) + "\n"


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
            recent = [x[1] for x in h[-HYST_INCUMBENT_FAILS:]]
            if r["grp"]["pass"]:
                r["hyst"] = "現任"; return True
            if len(recent) >= HYST_INCUMBENT_FAILS and not any(recent):
                r["hyst"] = f"連 {HYST_INCUMBENT_FAILS} 次不過閘下席"; return False
            r["hyst"] = f"現任·觀察中（近 {len(recent)} 次 {sum(recent)} 過）"; return True
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
    payload = {
        "schema_version": "2.0",
        "method": "v2 擁有層×時機層分離（2026-09-02）：排序＝own_score；R 為燈號；DD 只 veto／角色；遲滯 2/4",
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
<b>遲滯</b>：新席連 2 次週跑過閘、現任連 4 次不過才下席（硬 veto 除外）。
<b>軌別路由</b>：DD 角色優先；無 DD 走護城河 S/A 非↓（QGM 5 年 ROIC 穩定 ≥75% 亦可核心）；其餘衛星。
<b>市值門檻 ≥ ${MKTCAP_MIN/1e9:.0f}B</b>（持有人 2026-07-04 拍板：席位與主榜資格層；雷達發現層照掃全宇宙）。
<b>母體＝美股含 ADR；台股另建（.TW 不在本看板，2026-09-02 持有人拍板）</b>。
<b>兩級資格</b>：核心席必須完整 v14 DD；衛星席另接受 🪶 快審卡（週期位置＋陷阱＋護城河快評）。
DD 角色與機械軌別衝突標 ⚠ 供人裁。三閘未過的進場票落板凳、寧缺勿濫。</div>
<div class="asof">資料源 dd-screener latest.json ＋ QGM 品質池（US／TW）＋週線 cache ｜ v2 擁有層×時機層 ｜ 週更</div>
</div>
<div class="block"><h2>選股看板 v2（等寬版）</h2>
<div class="block-sub">擁有層排序（值不值得擁有）與時機燈（現在能不能動）分開讀；DD 只做 veto 與角色標籤。同內容另存 <a href="/engine/board.txt">board.txt</a>。</div>
<pre class="board" style="font-family:var(--mono);font-size:11.5px;line-height:1.45;overflow-x:auto;white-space:pre;background:var(--paper);border:1px solid var(--line);padding:12px">{escape(board_text)}</pre></div>
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
