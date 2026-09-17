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
Usage: python3 scripts/engine/build_arena.py [--ledger] [--lamp-only]

--ledger：帳本（arena-ledger.json：last_rotation_month／roster／w52_fail_streak／
snapshots）預設唯讀——不帶旗標時，用「既有帳本」算席位並照常寫 arena.json／board.txt／
fragments，但不推進月頻輪動時鐘、不追加 snapshot。只有 `.github/workflows/weekly-engine.yml`
的排程跑次帶 `--ledger` 真正寫帳本，避免手動/ad-hoc 執行提早觸發輪動或誤記週跌破 52 週線
次數（沿用 2026-09-08 VRTX/INCY 教訓的精神：跑次不能當週次算）。

--lamp-only（2026-09-17 持有人拍板，見 knowledge/rule_ledger.md「時機燈日更、席位月更」
列）：唯讀模式，只重算既有席位＋候補的時機燈／倉位（timing.*／ma.above_w52 與
mom_12_1_pct／docs/stages/data/lamp.json 階段／overheated），不重跑選股或月頻輪動、
不寫 arena-ledger.json、不動任何列的 score／rank／own/g/pass/veto。席位名單優先讀
arena-ledger.json 的 roster，缺則退回 arena.json 現有 core_seats／sat_seats；兩者皆缺
→ 印 warning、exit 0（不擋排程）。只改 arena.json 的席位列本身＋lamp_as_of／
lamp_source／lamp_last_rotation_date 三個戳記，board.txt／_board_body.html 只原地
替換「目前席位」區塊，全母體表／DD 對照／候選佇列維持上次週跑（`--ledger`）內容不變
——那些欄位的排序鍵是跨檔百分位，only weekly-engine.yml 的 `--ledger` 跑次能動。
見 `scripts/engine/run_lamp_only()`、`.github/workflows/daily-taipei-morning.yml`。
時機燈原料（dd-screener timing.*/ma.*）本來就每日跟著 build_dd_screener.py 更新，
只是過去只有週跑的 build_arena.py --ledger 會讀進來算 lamp——這支旗標把「讀」的
頻率補成跟「寫」一樣，不動「值不值得擁有」（own_score／席位）這條月頻時鐘。

v4 席位引擎（2026-09-17 持有人拍板，見 knowledge/rule_ledger.md「v4 席位引擎」列）：
月頻輪動取代週遲滯——每月第一次 --ledger 跑整批重選一次；期間只有硬否決（DD 迴避／體質
拒絕／衰退 ⛔／三月上修 ≤−5％／市值不足／連兩週跌破 52 週線）能換人，空位由下一名遞補。
own_score 排序改五個百分位（三月上修／12-1 月動能／成長封頂 30／品質／盈餘殖利率）在
ELIGIBLE 集合內互相比較，見 scripts/engine/grp.py 檔頭 v4 段與 own_score_v4()。

v4.1（2026-09-17 持有人拍板，見 knowledge/rule_ledger.md「v4.1 融券比 >10% 只能衛星」與
「v4.1 基期效應＋循環股守門」兩列；實作全在 scripts/engine/grp.py，本檔只多讀
grp["high_short_interest"]/["base_effect"]/own["cyclical"]/["cycle_guard"] 三組欄位
決定 core_candidate 與備註 badge）：融券占流通股比 >10% 比照過熱待遇——只排除
core_candidate（衛星照樣能坐），不進 own_score 排序、不是資格閘；內部人買賣
（insider_signal）全程只是備註 badge。成長遇基期效應改用 FY2→FY3 成長率；循環股
PEG 過低觸發循環守門時成長／盈餘殖利率分位封頂 50。設計稿：notes/site-internal/
root/_seat_engine_v4_20260917.md「v4.1 追加」段。

財報錨定上修（2026-09-17 持有人拍板，見 knowledge/rule_ledger.md「上修改為財報後
錨定」列）：own_score 的上修排序輸入與上修否決改讀 grp["rev_used_pct"]（build_
dd_screener._compute_eps_rev_since_earnings() 算好、以每檔自己最近一次財報日為
錨的 FY 加權上修；缺財報錨定時退回舊的 ~90 天日曆 baseline，即 eps_rev_3m_pct，
見 grp._revision_anchor()），取代固定 ~90 天日曆窗——後者對報告日期分散的母體不
公平（早報者的上修一個月後就因日曆理由過期出窗，晚報者反而卡在接近零）。本檔的
下游顯示（seat table「財報後上修%」欄＋tooltip、board.txt legend、arena.json
method 字串）同步改標，grp["eps_rev_3m_pct"] 欄位本身不變、仍保留供對照。新增
「下次財報」欄（grp["days_to_next_earnings"]）標示距下次財報天數 ≤7 天的名字，
提醒讀者該分數是財報前快照。
"""
from __future__ import annotations

import argparse
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
    DD_FRESH_DAYS, G_MIN_CAGR, G_MIN_CAGR_DURABLE, LAMP_ACTION, MKTCAP_MIN, MOM_12_1_OVERHEAT,
    P_LABEL_HTML, PEAK_ROIC_X, Q_FCF_MIN, Q_ROIC_MIN, R26_OVERHEAT_FALLBACK, R_VETO_FY1,
    cap_ok, fetch_caps, grp_route, grp_score, market_ok, own_score_v4, timing_lamp,
)
from dd_screener_quality import load_qgm_durability_index  # noqa: E402

WEEKLY_CACHE_UNIVERSE = ROOT / "data" / "weekly_cache_universe"   # 非 DD 池週線 fallback（見 build_radar.py 檔頭 docstring）
QGM_US = ROOT / "docs" / "qgm" / "latest.json"
QGM_TW = ROOT / "docs" / "qgm-tw" / "latest.json"
BOARD_TXT = OUT_DIR / "board.txt"
BOARD_HTML = OUT_DIR / "_board_body.html"   # 2026-09-02：HTML 版看板（表格＋燈號），raw fragment 供 cockpit innerHTML 與 _arena_body.html 內嵌共用
TWD_PER_USD = 32.0          # QGM-TW 市值（新台幣十億）換算門檻用，近似值
LISTING_ALIAS = {"2330.TW": "TSM"}   # 本地掛牌 → ADR（同公司只留一席）
# v4 席位引擎（2026-09-17 持有人拍板，見 knowledge/rule_ledger.md「v4 席位引擎」列）：
# 週遲滯（新席連 2 次過閘／現任連 4 次不過才下席）整批換成月頻輪動——10 週對照顯示
# 週遲滯在保護雜訊（23 檔坐過 10 席，核心 −3.8%／核心＋衛星 −8.4% vs SPY +1.2%）。
# 舊 HYST_* 常數與 DD_VERDICT_INFLUENCE 旗標已隨此改版移除（生產路徑不再讀）；
# DD 迴避否決改為無條件（見 grp.grp_score 的 veto_dd_avoid），不再靠環境變數開關。
W52_FAIL_STREAK_VETO = 2   # 硬否決之一：現任席連續此數目週跑站不上 52 週線 → 立即下席

DD_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
MARKET_STATE = ROOT / "docs" / "screener" / "market_state.json"
UNIVERSE = ROOT / "data" / "engine" / "universe.json"
# 2026-09-08：個股階段雷達「時機」欄（生命週期階段，與既有「時機燈」的 52 週位置／
# 過熱燈號是兩套獨立機制——只加欄、不改 own_score／排序／遲滯／席位任何邏輯，見
# notes/site-internal/root/_stages_radar_design_20260908.md §7b）。
LAMP_JSON = ROOT / "docs" / "stages" / "data" / "lamp.json"
STAGE_LABEL = {"S0": "弱勢", "S1": "轉強", "S2": "築底", "S5": "高檔整理", "S3": "收縮完成", "S4": "領先", "S9": "過渡"}
# pos=領先/收縮完成、accent=轉強、sec=築底、accent-muted=高檔整理、neg=弱勢、muted=過渡
# （design spec §7b 色票；S5 2026-09-09 owner decision，色階介於 sec 與 pos 之間，見
# notes/site-internal/root/_stages_radar_design_20260908.md）；up/dn/mut 沿用既有
# bw-pill 色系，accent/sec/accent-muted 是本節新增的三個 pill 色系。
STAGE_PILL_CLS = {"S0": "dn", "S1": "accent", "S2": "sec", "S5": "accent-muted",
                  "S3": "up", "S4": "up", "S9": "mut"}
STAGE_CODE_ASCII = {"S0": "WEAK", "S1": "TURN", "S2": "BASE", "S5": "HIGH",
                    "S3": "CONT", "S4": "LEAD", "S9": "TRAN"}
W_STAGE = 4
CARDS_JSON = OUT_DIR / "cards.json"
LEDGER_JSON = OUT_DIR / "arena-ledger.json"   # 席位變動帳本（append-only）
ARENA_JSON = OUT_DIR / "arena.json"
# 2026-07-10 席位分頁整併：輸出 nav-less 片段供 /cockpit/#seats-arena 子分頁 iframe 嵌入；
# /engine/arena.html 已改為 redirect stub（見 site_nav SKIP_FILES）。內容為 M5 對照組 PREREG 凍結，只換殼不改文。
ARENA_HTML = OUT_DIR / "_arena_body.html"
# 2026-09-09：研究母體（品質×時機矩陣「研究母體」欄，own_board 60 名以外的全 ~276 檔）——
# design spec notes/site-internal/root/_quality_timing_matrix_design_20260908.md。純攤平
# universe_rows 已算好的 grp.quality／verdict／route，不新增排序或資格邏輯。
UNIVERSE_BOARD_JSON = OUT_DIR / "universe_board.json"

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


def load_qgm_rows(stocks_map: dict, exclude: set | None = None,
                  latest_none: dict | None = None) -> list[dict]:
    """QGM（姊妹 repo 品質池，US＋TW）→ 無 DD 名字的擁有層列（v2：DD 選配）。
    latest_none＝dd-screener latest.json 裡 dd_status="none" 的列（--include-non-dd 產出），
    2026-09-16 起用它帶的 Koyfin FY1／FY3 補三年 CAGR——在此之前這些列被 main() 整批丟掉，
    QGM 名字永遠只有單年成長、g_three_year 恆為 False、永遠進不了席位（v3「DD 選配」名存實亡）。
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
                # 2026-09-16：優先用 dd-screener 供給列的 Koyfin 三年 CAGR；欄位空（Koyfin 匯出
                # 常留白 CAGR 欄）就用同列的 FY1／FY3 自算，公式同 build_dd_screener 的 fallback。
                ln = (latest_none or {}).get(tk) or {}
                g3 = ln.get("eps_fy1_fy3_cagr_pct")
                if g3 is None and ln.get("eps_source") == "xlsx":
                    lf1, lf3 = ln.get("eps_fy_curr"), ln.get("eps_fy3")
                    if lf1 and lf3 and lf1 > 0 and lf3 > 0:
                        g3 = ((lf3 / lf1) ** 0.5 - 1) * 100
                if g3 is not None:
                    g1 = g3
                g_method = "FY1→FY3 CAGR" if g3 is not None else "FY1→FY2 單年"
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
                    "_durable_5y": durable, "_g_method": g_method,
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


_QGM_DURABLE_INDEX_CACHE: dict | None = None


def _qgm_durable_index() -> dict:
    """懶載入＋記憶體快取 load_qgm_durability_index()（純本地讀 docs/qgm*/latest.json，
    零網路），供 _apply_durable_fallback() 在 dd-screener latest.json 尚未帶
    durable_5y 時當即時 fallback 用（見該函式 docstring）。"""
    global _QGM_DURABLE_INDEX_CACHE
    if _QGM_DURABLE_INDEX_CACHE is None:
        _QGM_DURABLE_INDEX_CACHE = load_qgm_durability_index()
    return _QGM_DURABLE_INDEX_CACHE


def _apply_durable_fallback(s: dict) -> None:
    """v3 席位資格（2026-09-09）：確保 s["durable_5y"]/s["durable_source"] 存在，
    就地補值，優先序：
      1. dd-screener enrich_ticker() 已算好的權威值（s["durable_5y"] 非 None）——
         --include-non-dd 上排程、latest.json 重建過後，任何 ticker（含 QGM 供給列）
         都會帶這個欄位，直接採用。
      2. build_arena 自己 load_qgm_rows() 供給列的原始 QGM 值（s["_durable_5y"]，
         0-1 的 pct_above，只有 QGM 供給列會有這個 key）。
      3. 本函式自己查 _qgm_durable_index()（本地讀 QGM JSON，零網路）——涵蓋
         latest.json 尚未重建、但該 ticker 本身也在 QGM 品質池內的過渡期情形
         （多數 DD 池大型股同時也在 QGM 池，見 commit 訊息的覆蓋率量測）。
      4. 皆缺 → None（grp_route 落款「耐久資料不足，只能衛星」）。
    """
    if s.get("durable_5y") is not None:
        # v4：權威值已就緒時，QGM 供給列可能仍缺 qgm_roic_5y_stability_pct（耐久欄
        # hover 用）——若 s["_durable_5y"]（0-1 分數）在場就順手補上，不覆寫既有值。
        if s.get("qgm_roic_5y_stability_pct") is None and s.get("_durable_5y") is not None:
            s["qgm_roic_5y_stability_pct"] = round(s["_durable_5y"] * 100, 1)
        return
    raw = s.get("_durable_5y")
    if raw is not None:
        s["durable_5y"] = raw >= 0.75
        s["durable_source"] = "qgm"
        s["qgm_roic_5y_stability_pct"] = round(raw * 100, 1)
        return
    hit = _qgm_durable_index().get(s.get("ticker"))
    if hit is not None:
        s["durable_5y"] = hit >= 0.75
        s["durable_source"] = "qgm"
        s["qgm_roic_5y_stability_pct"] = round(hit * 100, 1)
        return
    s.setdefault("durable_5y", None)
    s.setdefault("durable_source", None)


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
    _apply_durable_fallback(s)   # v4：durable_5y 就緒供成長閘門檻（10%/15%）與 grp_route 讀
    g = grp_score(s)             # v4：過熱／頂點／新硬否決／上修否決（財報後錨定，缺值退回三月）皆已在 grp_score 內算好
    route, route_why = grp_route(s)
    # v4 核心候選資格＝耐久達標 AND 不過熱（見 grp.py 檔頭 v4 段第 3 點；頂點不排除，
    # 只留顯示註記 g["peak"]）——build_arena.main() 用這個欄位挑核心 5 席。
    # v4.1（2026-09-17，見 knowledge/rule_ledger.md「v4.1 融券比 >10% 只能衛星」列）：
    # 融券高比照過熱的待遇——不進排序、不是資格閘，只排除核心候選資格（衛星照樣能坐）。
    core_candidate = route == "core" and not g["overheated"] and not g["high_short_interest"]
    role = s.get("dca_role") or ""
    age = s.get("dd_age_days")
    fresh = bool(s.get("dca_verdict")) and (age is None or age <= DD_FRESH_DAYS)
    # role_mismatch 現在比對的是「DD 自己講的角色」vs「耐久判定出的軌別」（v3 起
    # grp_route 已不讀 DD 角色）——分歧代表 DD 判斷的可長抱程度跟耐久數字對不上，
    # 值得人工複審，語意與 v2 時代相同、只是比對基準換了。
    mismatch = fresh and ((route == "satellite" and "核心" in role) or (route == "core" and "衛星" in role))
    g_method = ({True: "FY1→FY3 CAGR", False: "FY1→FY2 單年"}.get(g.get("g_three_year")))
    # v4 時機燈（grp.timing_lamp，pure）：s["_stage_code"] 由呼叫端（main()）注入，
    # s["_overheated"] 用本列剛算好的 g["overheated"]（同一份判定，不重算）。
    s["_overheated"] = g["overheated"]
    lamp = timing_lamp(s)
    return {"ticker": s["ticker"], "verdict": s.get("dca_verdict"),
            "role": role, "route": route, "route_why": route_why, "core_candidate": core_candidate,
            "role_mismatch": mismatch, "dd_tag": dd_tag(s), "dd_age_days": age, "dd_fresh": fresh,
            "src": s.get("_src") or "dd-pool", "g_method": g_method,
            "durable_5y": s.get("durable_5y"), "durable_source": s.get("durable_source"),
            "durable_roic_5y_avg_pct": s.get("roic_5y_avg_pct"),
            "durable_qgm_pct": s.get("qgm_roic_5y_stability_pct"),
            "grp": g, "score": g["score"],
            "lamp": lamp, "action": LAMP_ACTION.get(lamp["code"], "—"),
            "roic": g["quality"].get("roic"), "fcf": g["quality"].get("fcf"),
            "peg": (s.get("live_peg") if s.get("live_peg") is not None else s.get("peg")),
            "r26": s.get("_r26"), "r52": s.get("_r52"),
            # 2026-09-17（籌碼面備註 badge，見 knowledge/rule_ledger.md「v4.1 融券比
            # >10% 只能衛星」列）：insider 全程只是備註，不進資格與排序；SI 的排除
            # 核心候選判定已在 g["high_short_interest"]／core_candidate 算好，這裡
            # 只多帶原始 % 與內部人訊號供席位表 hover 顯示用。
            "insider_signal": s.get("insider_signal"), "insider_net_buy_3m": s.get("insider_net_buy_3m"),
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


def load_light_rows(stocks_map: dict, exclude: set | None = None) -> list[dict]:
    """快審卡（qual_tier=light）→ 衛星席第二資格來源（2026-07-04 拍板）。
    光卡只給衛星資格（核心席必須完整 DD）。優先序：dd-meta 有裁決的名字光卡讓位；
    池內「待補 DD」名字光卡可用（GRP 用 latest.json 全口徑）；池外用雷達主榜口徑
    （G＝FY+1 隱含成長、R＝30 天修正），頁面標 🪶。
    `exclude`（2026-09-09 dedupe 修復）＝已被更高優先序來源收走的 ticker（目前是
    load_qgm_rows 輸出）——first source wins: dd-pool > qgm > light，本函式原本只
    對 stocks_map（dd-pool）去重，沒對過 qgm_rows，INCY 這類名字若同時出現在 QGM
    品質池與快審卡就會在 universe_rows 裡重複兩列（見 build_arena.py main() 呼叫端）。"""
    cards_dir = OUT_DIR / "cards" / "data"
    try:
        radar = json.loads((OUT_DIR / "radar.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        radar = {}
    board = {r["ticker"]: r for r in radar.get("grp_board") or []}
    stage2 = radar.get("stage2") or {}
    verdict_tickers = {t for t, s in stocks_map.items() if s.get("dca_verdict")}
    exclude = exclude or set()
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
        if t in exclude:
            print(f"  [dedupe] 快審卡 {t} 已由 QGM 品質池供給，光卡讓位"
                  "（first source wins: dd-pool > qgm > light）")
            continue
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

# v4 席位表（board.txt「目前席位」區塊，見 render_board_text）欄寬與 ASCII 代碼——
# 時機燈／倉位另立一套代碼（GRN/YLW/HOT/RED/OUT、FULL/HALF/ZERO/-），與上面舊 P_LABEL
# 系（BRK/PB/TR/HOT/DN，全母體表沿用）刻意分開，語意不同不能共用一張表。
LAMP_CODE_ASCII = {"green": "GRN", "yellow": "YLW", "hot": "HOT", "red": "RED", "out": "OUT"}
ACTION_CODE_ASCII = {"green": "FULL", "yellow": "HALF", "hot": "HALF", "red": "ZERO", "out": "-"}
W_SEATCODE, W_RANK, W_REV3M, W_MOM12, W_DUR, W_LAMPCODE, W_ACTCODE = 4, 5, 6, 6, 3, 4, 4
# 財報錨定上修（2026-09-17）：「下次財報」欄寬——board.txt 席位表新增欄，見
# _seat_section_lines()／knowledge/rule_ledger.md「上修改為財報後錨定」列。
W_NEXTEARN = 6


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


def _ticker_col(t) -> str:
    return _pad(str(t)[:W_TICKER], W_TICKER)


def _seat_section_lines(core_seats, sat_seats, bench_seats, prev_snap, rows,
                        lamp_as_of=None, last_rotation_date=None) -> list[str]:
    """『目前席位：核心 5＋衛星 5＋候補 5』區塊（board.txt 用，含 DOWN 異動列）——獨立
    成函式供 render_board_text() 全量重建與 run_lamp_only() 唯讀刷新共用同一份格式
    （見檔頭 --lamp-only 段）：後者只重算列內時機欄位（lamp／action／grp 的 P 閘與
    overheated），原樣呼叫本函式重繪這段；全母體表／DD 對照／候選佇列需要全母體
    `rows` 才能重建，唯讀模式不動、維持上次 `--ledger` 跑次內容（`rows` 在該路徑
    傳空清單，DOWN 列的原因只會退化成「不在母體」，是刻意的降級，見呼叫端）。"""
    seat_of = {r["ticker"]: "核心席" for r in core_seats}
    seat_of.update({r["ticker"]: "衛星席" for r in sat_seats})
    prev_seats = {t: "核心席" for t in prev_snap.get("core", [])}
    prev_seats.update({t: "衛星席" for t in prev_snap.get("sat", [])})

    L = ["== 目前席位：核心 5 ＋ 衛星 5 ＋ 候補 5"]
    if lamp_as_of or last_rotation_date:
        L.append(f"時機更新：{lamp_as_of or '—'}（每日）／席位更新：{last_rotation_date or '—'}（每月換席）")
    hdr2 = (f"{'seat':<{W_SEATCODE}} {'ticker':<{W_TICKER}} {'rank':>{W_RANK}} {'rev':>{W_REV3M}} "
            f"{'nextE':>{W_NEXTEARN}} {'mom12':>{W_MOM12}} {'dur':<{W_DUR}} {'lamp':<{W_LAMPCODE}} "
            f"{'act':<{W_ACTCODE}} {'dd':<{W_DD}} note")
    L.append(hdr2)
    for track_label, seats, prefix in (("核心席", core_seats, "C"), ("衛星席", sat_seats, "S"),
                                       ("候補", bench_seats, "B")):
        for j, r in enumerate(seats, 1):
            g = r["grp"]
            raw = (g.get("own") or {}).get("raw") or {}
            lamp = r.get("lamp") or {}
            if prefix != "B" and prev_seats.get(r["ticker"]) == track_label:
                chg = ""
            elif prefix != "B" and r["ticker"] not in prev_seats:
                chg = "NEW"
            elif prefix != "B":
                chg = f"FROM:{'C' if prev_seats[r['ticker']] == '核心席' else 'S'}"
            else:
                chg = ""
            note_bits = []
            if g.get("peak"):
                note_bits.append("頂點")
            if g.get("overheated"):
                note_bits.append("過熱")
            if g.get("high_short_interest"):
                note_bits.append("融券高")
            if g.get("base_effect"):
                note_bits.append("基期")
            own_raw_ = ((g.get("own") or {}).get("raw")) or {}
            if own_raw_.get("cycle_guard"):
                note_bits.append("循環守門")
            elif own_raw_.get("cyclical"):
                note_bits.append("循環")
            if r.get("insider_signal") == "買":
                note_bits.append("內部人買")
            elif r.get("insider_signal") == "賣":
                note_bits.append("內部人賣")
            days_ne = g.get("days_to_next_earnings")
            # 財報錨定上修（2026-09-17）：距下次財報 <=7 天者標記——提醒讀者這個
            # 分數是財報前快照（財報後上修分位可能一週內就變動）。
            if days_ne is not None and 0 <= days_ne <= 7:
                note_bits.append("財報前")
            if chg:
                note_bits.append(chg)
            if r.get("seat_note"):
                note_bits.append(r["seat_note"])
            if r.get("route_why"):
                note_bits.append(r["route_why"])
            next_earn_cell = f"{int(days_ne)}d" if days_ne is not None else "-"
            L.append(
                f"{_pad(f'{prefix}{j}', W_SEATCODE)} {_ticker_col(r['ticker'])} {_n(r['score'], W_RANK)} "
                f"{_n(g.get('rev_used_pct'), W_REV3M)} {_pad(next_earn_cell, W_NEXTEARN, right=True)} "
                f"{_n(raw.get('mom'), W_MOM12)} "
                f"{_pad('Y' if r.get('durable_5y') else '-', W_DUR)} "
                f"{_pad(LAMP_CODE_ASCII.get(lamp.get('code'), '-'), W_LAMPCODE)} "
                f"{_pad(ACTION_CODE_ASCII.get(lamp.get('code'), '-'), W_ACTCODE)} "
                f"{_pad(dd_ascii(r)[:W_DD], W_DD)} {'；'.join(note_bits)}"
            )
    gone = [t for t in prev_seats if t not in seat_of]
    if gone:
        why = {r["ticker"]: r for r in rows}
        for t in gone:
            r = why.get(t)
            why_txt = "；".join((((r or {}).get("grp") or {}).get("why") or [])[:2]) or ("排名分被擠下" if r else "不在母體")
            L.append(f"  DOWN {_ticker_col(t)}：{why_txt}")
    L.append("")
    return L


def render_board_text(as_of, rows, core_seats, sat_seats, bench_seats, prev_snap, entered, lamp_map,
                      lamp_as_of=None, last_rotation_date=None) -> str:
    """附錄 B 式等寬看板（持有人 2026-09-02 指定形式；2026-09-17 v4 改版——目前席位
    區塊改新欄序 席/代號/排名分/財報後上修/下次財報/12M動能/耐久/時機/倉位/DD/備註，見
    knowledge/rule_ledger.md「v4 席位引擎」「上修改為財報後錨定」兩列）：目前席位＋擁有層排序表＋DD 進場 vs
    機械資格＋無 DD 過閘候選。純文字，同時寫 docs/engine/board.txt 與 <pre> 嵌頁
    （docs/engine/_arena_body.html、docs/cockpit/index.html 皆讀同一份文字）。

    對齊規則：瀏覽器對 CJK 常用 fallback 字型，其字寬不保證是等寬字型 cell 的精準 2 倍，
    f-string {x:w} 補白也只算 code point 不算顯示寬度——兩者都會讓含中文/emoji 的欄位
    在瀏覽器 <pre> 裡跑版。故主表 note 欄以左一律 ASCII 代碼，任何字型都保證對齊；
    中文只留在最後的 note 欄（不需要再對齊）與表頭上方的圖例行（純 prose，非欄位）。

    `lamp_as_of`／`last_rotation_date`（2026-09-17，見 --lamp-only 段）：「目前席位」
    區塊的兩行新鮮度戳記，由 run_lamp_only() 與本函式共用的 _seat_section_lines()
    渲染；main() 全量重建時同樣傳入（lamp_as_of=as_of），保持兩條路徑輸出格式一致。"""
    seat_code = {r["ticker"]: f"C{j}" for j, r in enumerate(core_seats, 1)}
    seat_code.update({r["ticker"]: f"S{j}" for j, r in enumerate(sat_seats, 1)})

    L = []
    L.append(f"選股看板 v4｜as_of {as_of}｜母體 {len(rows)}（DD 池＋QGM 無 DD＋快審卡）"
             "｜母體＝美股含 ADR；台股另建（.TW 不在本看板）")
    L.append("這是研究層陣容——值不值得擁有，月頻換人，不是帳戶持倉。")
    L.append("排名分＝財報後上修（缺財報錨定退回三個月）、12M 動能、成長（封頂 30）、品質"
             "（FCF/淨利與稀釋率百分位平均；增量 ROIC>=15% 免計 FCF/淨利）、盈餘殖利率，"
             "五個排名百分位在合格集合內平均。成長遇基期效應（FY1->FY2 因低基期跳增、"
             "FY2->FY3 <20%）改用 FY2->FY3 成長率。循環股（毛利跨距>20pp 或 capex 佔營收"
             ">15%）若 PEG<0.3 觸發循環守門，成長/盈餘殖利率分位封頂 50。")
    L.append("欄位說明：rank=排名分、rev=財報後上修%（已排除匯率；以該股自己最近一次財報日"
             "前最新月度 snapshot 為基準，缺財報錨定退回三個月）、nextE=距下次財報天數、"
             "mom12=12減1個月動能%、dur=耐久（Y=核心資格達標：五年 ROIC 平均或 QGM 五年"
             "穩定度）、lamp=時機燈、act=倉位（跟 lamp 一對一）、dd=DD 標籤（僅供顯示）；"
             "note=備註（財報前=距下次財報 <=7 天，分數為財報前快照）")
    L.append("lamp/act 代碼：GRN/FULL=可進·正常倉、YLW/HALF=半倉、HOT/HALF=過熱·半倉、"
             "RED/ZERO=等板機·零倉、OUT/-=不合格·未站上 52 週線")
    L.append("seat：C1-C5=核心席次、S1-S5=衛星席次、B1-B5=候補（未坐席）"
             "｜dd：IN/WATCH/AVOID/legacy/none，core/sat/trk=角色，Nd=天數，!old=逾 180 天過期")
    L.append("資格門檻：市值 200 億以上、品質閘、三年成長 15%（耐久者 10%）、站上 52 週線、"
             "財報後上修達 5% 否決（缺財報錨定退回三月上修）、體質拒絕/衰退⛔/DD迴避同樣否決。"
             "過熱／融券高（SI>10%）與頂點不擋資格，只排除核心候選（過熱、融券高）或純顯示"
             "（頂點）；核心候選另需耐久且不過熱且非融券高；無產業集中度上限；內部人買賣僅"
             "備註，不進資格與排序。")
    L.append("換人規則：每月第一次排程換一次席；期間只有硬否決（迴避/拒絕/⛔/財報後上修"
             "達5%（缺財報錨定退回三月上修）/市值不足/連兩週跌破 52 週線）能換人，空位由"
             "下一名遞補。")
    L.append("怎麼用：席位+時機綠燈=正常倉可以買；席位+時機紅燈=先別動，等板機。")
    L.append("")
    L.extend(_seat_section_lines(core_seats, sat_seats, bench_seats, prev_snap, rows,
                                 lamp_as_of, last_rotation_date))
    hdr = (f"{'#':>{W_IDX}} {'ticker':<{W_TICKER}} {'score':>{W_SCORE}} {'grow':>{W_GROW}} "
           f"{'EY':>{W_EY}} {'ROIC':>{W_ROIC}} {'FCF':>{W_FCF}} {'PEG':>{W_PEG}} {'rev1m':>{W_REV}} "
           f"{'timing':<{W_TIMING}} {'stage':<{W_STAGE}} {'seat':<{W_SEAT}} {'dd':<{W_DD}} {'moat':<{W_MOAT}} note")
    L.append(hdr)
    # v4：全母體看板改用真正 ELIGIBLE 名次（own_score_v4）——只有過全部資格閘的名字
    # 才有有效排名分，見 apply_own_score_v4()／grp.own_score_v4()。
    own = sorted((r for r in rows if r["grp"].get("pass")), key=lambda r: -(r["score"] or 0))
    for i, r in enumerate(own[:40], 1):
        g = r["grp"]; o = g.get("own") or {}
        note = "；".join(list(g.get("why") or [])[:2])
        if r.get("g_method") == "FY1→FY2 單年":
            note = ("成長=FY1→FY2 單年；" + note) if note else "成長=FY1→FY2 單年"
        L.append(
            f"{i:>{W_IDX}} {_ticker_col(r['ticker'])} {_n(r['score'], W_SCORE)} {_n(g.get('g'), W_GROW)} "
            f"{_n((o.get('raw') or {}).get('ey'), W_EY)} {_n(r.get('roic'), W_ROIC)} {_n(r.get('fcf'), W_FCF)} "
            f"{_n(r.get('peg'), W_PEG, 2)} {_n(g.get('r_fy1'), W_REV)} "
            f"{_pad(TIMING_CODE.get(g.get('p_label'), 'DN'), W_TIMING)} "
            f"{_pad(STAGE_CODE_ASCII.get(lamp_map.get(r['ticker']), '-'), W_STAGE)} "
            f"{_pad(seat_code.get(r['ticker'], ''), W_SEAT)} "
            f"{_pad(dd_ascii(r)[:W_DD], W_DD)} {_pad(moat_ascii(r.get('moat')), W_MOAT)} {note}"
        )
    L.append("")
    L.append("== DD 裁決進場 vs 機械資格")
    ok = [r for r in entered if r["grp"]["pass"]]; ng = [r for r in entered if not r["grp"]["pass"]]
    L.append(f"  進場 {len(entered)}：過閘 {len(ok)}／未過 {len(ng)}")
    for r in ng:
        L.append(
            f"   X {_ticker_col(r['ticker'])} {_pad(TIMING_CODE.get(r['grp'].get('p_label'), 'DN'), W_TIMING)} "
            f"{'；'.join((r['grp'].get('why') or [])[:3])}"
        )
    L.append("")
    L.append("== 可選但先不入席：缺三年成長預估（加進 Koyfin 名單即可）")
    L.append("這些名字其餘資格都過，但成長只有單年預估（yfinance FY1→FY2，非 Koyfin FY1→FY3 CAGR），"
             "v4 起三年期是成長閘硬性必備，所以只列隊、不佔席、不計輪動。加進 Koyfin watchlist "
             "補上三年成長率，下次 build 就會脫隊、以三年成長率重新競爭席位（不需要先有 DD）。")
    # v4：g_three_year 直接併入成長閘 pass/fail，這類名字的 grp.pass 恆為 False，
    # 故改掃全母體 `rows`（而非只含 pass=True 的 own），依成長率（單年）降冪排列。
    queue_rows = sorted(
        (r for r in rows if r.get("qual") != "light" and not r["grp"].get("g_three_year")
         and r["grp"].get("g") is not None and r["grp"]["g"] >= 15
         and (r["grp"].get("quality") or {}).get("pass") and not r["grp"].get("veto")
         and r["grp"].get("above_w52")),
        key=lambda r: -(r["grp"].get("g") or 0))
    for r in queue_rows[:20]:
        g = r["grp"]
        L.append(
            f"   {_ticker_col(r['ticker'])} grow(單年) {_n(g.get('g'), W_GROW)} "
            f"ROIC {_n(r.get('roic'), W_ROIC)} FCF {_n(r.get('fcf'), W_FCF)} "
            f"distHi {_n(g.get('dist_hi'), 6)} "
            f"{_pad(TIMING_CODE.get(g.get('p_label'), 'DN'), W_TIMING)}"
        )
    return "\n".join(L) + "\n"


# ── HTML 版看板（2026-09-02，持有人否決 ASCII <pre>：燈號不見、欄位對不齊）─────────────
# board.txt（render_board_text，above）保留給終端機／郵件；瀏覽器一律走這裡的 HTML TABLE
# ——對齊交給瀏覽器排版引擎，欄位不再需要手動補白，顏色燈號也能回來。輸出是「裸片段」
# （單一 <div class="board-wrap">…</div>，樣式自帶 scoped <style>），不含 html/head/body，
# 可直接：① innerHTML 塞進 cockpit #roster-mount；② 原樣接進 page_embed_shell() 產的
# _arena_body.html body（後者另有 common.py PAGE_CSS，兩邊 class 名不衝突，token 共用
# /assets/imq-base.css，故顏色與字體在兩處視覺一致）。

_TIMING_HTML = {   # p_label -> (中文一詞, 色系)；色系對應 bw-pill-{cls}
    # 2026-09-08：欄名「時機燈」改叫「位置」（與 stages 的「時機」欄改叫「階段」
    # 區分開）——值改成一詞白話（不再用色點 emoji 當主要視覺，顏色交給 bw-pill-{cls}）。
    "breakout": ("突破", "up"),
    "pullback": ("回踩", "up"),
    "in_trend": ("趨勢", "neu"),
    "overheated": ("過熱", "warn"),
}

# note 欄 chip 化：why[] 裡固定句型 -> (短 chip 文字, 原句當 title)。順序即比對順序，
# 不影響輸出順序（輸出仍照 why[] 原順序，此表只負責「認出這句要不要變 chip」）。
# 2026-09-09（owner 走查回饋）：短 chip 一律白話＋帶數字/差距，不留代號；未收錄的句子
# 一律原文入 chip、不砍字看不全（見下 _chips_from_why 的 fallback，CSS 交給 .bw-note 換行）。
_CHIP_PATTERNS = [
    (re.compile(r"^市值資料缺漏"), lambda w, m: "市值缺資料"),
    (re.compile(r"^市值 \d+B 低於門檻 (\d+)B"), lambda w, m: f"市值不足 {int(m.group(1)) * 10} 億美元"),
    (re.compile(r"^位置閘：過熱（26 週 ([+-]?\d+)%）"), lambda w, m: f"過熱 {m.group(1)}%"),
    (re.compile(r"^位置閘未過"), lambda w, m: "52 週線下"),
    (re.compile(r"^品質閘 ROIC 缺"), lambda w, m: "ROIC 缺資料"),
    (re.compile(r"^品質閘 ROIC ([+-]?[\d.]+)"),
     lambda w, m: f"ROIC {float(m.group(1)):.1f}%，未達 {Q_ROIC_MIN:.0f}%"),
    (re.compile(r"^品質閘 FCF 缺"), lambda w, m: "FCF 率缺資料"),
    (re.compile(r"^品質閘 FCF ([+-]?[\d.]+)"),
     lambda w, m: f"FCF 率 {float(m.group(1)):.1f}%，未達 {Q_FCF_MIN:.0f}%"),
    (re.compile(r"^品質欄缺"), lambda w, m: "品質未判定（金融股另軌）"),
    (re.compile(r"^成長閘用 2 年成長率代替"), lambda w, m: "成長用兩年數代替"),
    (re.compile(r"^成長閘未過"), lambda w, m: f"成長未達 {G_MIN_CAGR:.0f}%"),
    (re.compile(r"^上修閘保守否決"), lambda w, m: "上修否決"),
    (re.compile(r"^上修閘否決"), lambda w, m: "上修否決"),
    (re.compile(r"^DD 迴避"), lambda w, m: "DD 迴避"),
    (re.compile(r"^硬 veto 下席"), lambda w, m: "硬 veto"),
    (re.compile(r"^雷達三閘資料不足或未過"), lambda w, m: "資格資料不足或未過（隨主榜週更再驗）"),
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
    """通用版（不含 g_method／hyst）：給 DD-vs-機械資格、下席原因等只有 why[] 可用的表格。
    未收錄進 _CHIP_PATTERNS 的句子原文入 chip、不截斷（2026-09-09：舊版 w[:14]+… 會把長句
    砍到看不全，owner 走查回饋——長句交給 .bw-note 的 white-space:normal 自然換行）。"""
    out = []
    for w in (why_list or [])[:limit]:
        c = _match_chip(w)
        out.append(c if c else (w, w))
    return out


def _num(v, d: int = 1) -> str:
    if v is None:
        return '<span class="bw-muted">—</span>'
    try:
        return f"{float(v):.{d}f}"
    except (TypeError, ValueError):
        return '<span class="bw-muted">—</span>'


def load_lamp() -> dict:
    """docs/stages/data/lamp.json → {ticker: 階段碼}；缺檔或壞檔回傳空字典——
    「時機」欄整欄呈現「—」，不擋 build（stages 是每日 21:45 UTC 收盤帶最後一步，
    engine 是週更，兩者不保證同一次 run 都成功）。頁面 JS 之後會 fetch 這份檔案
    覆寫成當天最新值，見 docs/cockpit/index.html／docs/engine/arena.html。"""
    try:
        return json.loads(LAMP_JSON.read_text(encoding="utf-8")).get("lamp") or {}
    except (OSError, json.JSONDecodeError):
        return {}


def _stage_pill(ticker: str, lamp_map: dict) -> str:
    code = lamp_map.get(ticker)
    label = STAGE_LABEL.get(code, "無資料")   # 海外雙掛牌等無階段資料的名字（2026-09-09 owner 走查回饋）
    cls = STAGE_PILL_CLS.get(code, "mut")
    return (f'<span class="bw-pill bw-pill-{cls}" data-lamp-ticker="{escape(ticker)}">'
            f"{escape(label)}</span>")


def _timing_pill(p_label, r26, dist_hi) -> str:
    label, cls = _TIMING_HTML.get(p_label, ("線下", "dn"))
    bits = []
    if r26 is not None:
        bits.append(f"26 週漲幅 {r26:+.1f}%")
    if dist_hi is not None:
        bits.append(f"距 52 週高 {dist_hi:+.1f}%")
    title = "；".join(bits) or "位置資料缺"
    return f'<span class="bw-pill bw-pill-{cls}" title="{escape(title)}">{escape(label)}</span>'


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
.board-wrap tr.bw-muted-row td{opacity:.6}
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
.board-wrap .bw-pill-accent{background:#fdf4e3;color:var(--accent,#b8924a)}
.board-wrap .bw-pill-sec{background:var(--line-soft,#eee);color:var(--sec,#666)}
.board-wrap .bw-pill-accent-muted{background:#eaf3ee;color:#3f7d63}
.board-wrap .bw-chip{display:inline-block;font-size:10.5px;font-family:var(--sans,inherit);
  color:var(--sec,var(--text-sec,#666));background:var(--line-soft,rgba(0,0,0,.045));
  border-radius:4px;padding:1px 6px;margin:0 3px 3px 0;cursor:help}
.board-wrap .bw-chip-more{color:var(--muted,#999)}
.board-wrap .bw-note-line{font-size:12px;color:var(--sec,var(--text-sec,#666));margin-top:8px;line-height:1.75}
.board-wrap .bw-note-line b{color:var(--ink,var(--text,#1a1a1a))}
.board-wrap details.bw-fold{margin-top:4px}
.board-wrap details.bw-fold>summary{cursor:pointer;font-size:12.5px;font-weight:650;
  color:var(--ink,var(--text,#1a1a1a));padding:6px 2px;list-style:revert}
.board-wrap details.bw-fold[open]>summary{margin-bottom:6px}
@media(max-width:760px){.board-wrap table{font-size:11.5px}.board-wrap th,.board-wrap td{padding:4px 6px}}
</style>"""

# 「時機」欄每日刷新（2026-09-08，design spec §7b）：board_html 裡的 data-lamp-ticker
# cell 是 engine 建置當時（週更）的階段值；stages 是每日排程，所以頁面載入時再 fetch
# 一次 /stages/data/lamp.json 覆寫成當天最新——404／格式錯就靜默保留建置期值，不擋頁面。
# 一般字串（非 f-string）：JS 花括號在此不需跳脫；由呼叫端以單一 {變數} 插入 f-string body。
_STAGE_LAMP_SCRIPT = """<script>(function(){
function refreshStageLamp(){
  fetch('/stages/data/lamp.json',{cache:'no-store'}).then(function(r){
    if(!r.ok) throw new Error(String(r.status));
    return r.json();
  }).then(function(d){
    var lamp=(d&&d.lamp)||{};
    var LABEL={S0:'弱勢',S1:'轉強',S2:'築底',S5:'高檔整理',S3:'收縮完成',S4:'領先',S9:'過渡'};
    var CLS={S0:'dn',S1:'accent',S2:'sec',S5:'accent-muted',S3:'up',S4:'up',S9:'mut'};
    document.querySelectorAll('[data-lamp-ticker]').forEach(function(el){
      var code=lamp[el.getAttribute('data-lamp-ticker')];
      el.className='bw-pill bw-pill-'+(CLS[code]||'mut');
      el.textContent=LABEL[code]||'無資料';
    });
    if(d&&d.as_of){
      document.querySelectorAll('.stage-lamp-asof').forEach(function(el){
        el.textContent='（階段資料日 '+d.as_of+'）';
      });
    }
  }).catch(function(){ /* 缺檔或壞檔：保留看板片段建置期的值 */ });
}
if(document.readyState!=='loading') refreshStageLamp();
else document.addEventListener('DOMContentLoaded', refreshStageLamp);
})();</script>"""


def _seat_remark(r: dict) -> str:
    g = r["grp"]; bits = []
    if g.get("peak"):
        bits.append(_chip_html("⚠ 頂點", "ROIC 高於五年平均 1.3 倍以上——只能衛星，非下市訊號"))
    if g.get("overheated"):
        bits.append(_chip_html("🟠 過熱", "12-1 個月動能 >150%（或 fallback 26 週漲幅 >80%）——只能衛星"))
    if g.get("high_short_interest"):
        si = g.get("short_interest_pct_float")
        siT = f"{si:.1f}%" if isinstance(si, (int, float)) else "—"
        bits.append(_chip_html("🔴 融券高", f"融券占流通股比 {siT}（>10%）——只能衛星，非資格閘、不進排序"))
    if g.get("base_effect"):
        d = g.get("base_effect_detail") or {}
        bits.append(_chip_html("基期", f'FY1→FY2 跳 +{d.get("fy1_fy2_pct", "—")}%，'
                                      f'FY2→FY3 只 +{d.get("fy2_fy3_pct", "—")}%，成長改用 FY2→FY3'))
    own_raw_ = ((g.get("own") or {}).get("raw")) or {}
    if own_raw_.get("cycle_guard"):
        cd = own_raw_.get("cycle_guard_detail") or {}
        bits.append(_chip_html("循環守門", f'毛利跨距 {cd.get("gm_swing_pp", "—")}pp／資本支出佔營收 '
                                         f'{cd.get("capex_pct_rev", "—")}%／PEG {cd.get("peg", "—")}'
                                         '——成長與盈餘殖利率分位封頂 50'))
    elif own_raw_.get("cyclical"):
        bits.append(_chip_html("循環", "毛利率跨距 >20pp 或資本支出佔營收 >15%——純顯示，未觸發守門"))
    if r.get("insider_signal") == "買":
        insT = r.get("insider_net_buy_3m")
        insT = f"{insT:+,.0f} 股" if isinstance(insT, (int, float)) else "—"
        bits.append(_chip_html("內部人買", f"近 3 個月內部人淨買超 {insT}——僅供備註，不進資格與排序"))
    elif r.get("insider_signal") == "賣":
        insT = r.get("insider_net_buy_3m")
        insT = f"{insT:+,.0f} 股" if isinstance(insT, (int, float)) else "—"
        bits.append(_chip_html("內部人賣", f"近 3 個月內部人淨賣超 {insT}——僅供備註，不進資格與排序"))
    if r.get("seat_note"):
        bits.append(escape(r["seat_note"]))
    if r.get("route_why"):
        bits.append(f'<span class="bw-muted">{escape(r["route_why"])}</span>')
    return "".join(bits) or '<span class="bw-muted">—</span>'


def _seat_tr(r: dict, code: str, lamp_map: dict, muted: bool = False) -> str:
    g = r["grp"]; o = g.get("own") or {}; raw = o.get("raw") or {}
    rank_title = (f"財報後上修分位 {_num(o.get('p_rev'), 1)}／12M 動能分位 {_num(o.get('p_mom'), 1)}／"
                  f"成長分位 {_num(o.get('p_g'), 1)}／品質分位 {_num(o.get('p_q'), 1)}／"
                  f"盈餘殖利率分位 {_num(o.get('p_ey'), 1)}｜原始值：上修 {_num(raw.get('rev'), 1)}%、"
                  f"動能 {_num(raw.get('mom'), 1)}%、成長 {_num(raw.get('g'), 1)}%、EY {_num(raw.get('ey'), 1)}%")
    durable_bits = []
    if r.get("durable_roic_5y_avg_pct") is not None:
        durable_bits.append(f"五年 ROIC 平均 {r['durable_roic_5y_avg_pct']:.1f}%")
    if r.get("durable_qgm_pct") is not None:
        durable_bits.append(f"QGM 五年穩定度 {r['durable_qgm_pct']:.1f}%")
    durable_cell = (f'<span title="{escape("；".join(durable_bits) or "耐久資料不足")}">'
                    f'{"✓" if r.get("durable_5y") else "—"}</span>')
    # 財報錨定上修（2026-09-17）：上修欄 tooltip 標基準快照日＋錨定方式（財報／日曆）；
    # 「下次財報」欄天數 <=7 者用 warn pill 標示——分數是財報前快照。
    rev_anchor_txt = {"earnings": "財報後", "calendar_3m": "日曆三個月（缺財報錨定）"}.get(
        g.get("rev_anchor"), "—")
    rev_title = f"錨定：{rev_anchor_txt}｜基準快照 {g.get('rev_baseline_date') or '—'}"
    days_ne = g.get("days_to_next_earnings")
    if days_ne is None:
        next_earn_cell = '<span class="bw-muted">—</span>'
    elif 0 <= days_ne <= 7:
        next_earn_cell = (f'<span class="bw-pill bw-pill-warn" '
                          f'title="距下次財報 {int(days_ne)} 天——分數為財報前快照">{int(days_ne)} 天</span>')
    else:
        next_earn_cell = f"{int(days_ne)} 天"
    lamp = r.get("lamp") or {}
    p_txt = {"breakout": "突破帶", "pullback": "回踩", "in_trend": "趨勢內"}.get(g.get("p_label"), "52 週線下")
    stage_txt = STAGE_LABEL.get(lamp_map.get(r["ticker"]), "無資料")
    lamp_title = (f'{lamp.get("why", "")}｜位置：{p_txt}｜階段：{stage_txt}'
                 + (f'｜板機：{lamp["trigger"]}' if lamp.get("trigger") else ""))
    lamp_cell = f'<span class="bw-pill" title="{escape(lamp_title)}">{escape(lamp.get("label", "—"))}</span>'
    cls = ' class="bw-muted-row"' if muted else ""
    return (f'<tr{cls}><td class="bw-l">{escape(code)}</td>'
            f'<td class="bw-l"><strong>{_tk_link(r)}</strong></td>'
            f'<td title="{escape(rank_title)}">{_num(r.get("score"), 1)}</td>'
            f'<td title="{escape(rev_title)}">{_num(g.get("rev_used_pct"), 1)}</td>'
            f'<td class="bw-l">{next_earn_cell}</td>'
            f'<td>{_num(raw.get("mom"), 1)}</td>'
            f'<td class="bw-l">{durable_cell}</td>'
            f'<td class="bw-l">{lamp_cell}</td>'
            f'<td class="bw-l">{escape(r.get("action") or "—")}</td>'
            f'<td class="bw-l">{_dd_pill(r.get("dd_tag"))}</td>'
            f'<td class="bw-note">{_seat_remark(r)}</td></tr>')


def _seat_section_html(core_seats, sat_seats, bench_seats, prev_snap, rows, lamp_map,
                       lamp_as_of=None, last_rotation_date=None) -> str:
    """『目前席位：核心 5＋衛星 5＋候補 5』HTML 區塊（h3＋sub＋表＋legend＋變動列）——
    獨立成函式供 render_board_html() 全量重建與 run_lamp_only() 唯讀刷新共用同一份
    格式（見檔頭 --lamp-only 段）：後者只重算列內時機欄位，原樣呼叫本函式重繪這段；
    全母體表／DD 對照／候選佇列需要全母體 `rows` 才能重建，唯讀模式不動、維持上次
    `--ledger` 跑次內容（`rows` 在該路徑傳空清單，DOWN 列的原因只會退化成
    「排名分被擠下／不在母體」，是刻意的降級，見呼叫端）。"""
    seat_label = {}
    for i, r in enumerate(core_seats, 1):
        seat_label[r["ticker"]] = f"核心 {i}"
    for i, r in enumerate(sat_seats, 1):
        seat_label[r["ticker"]] = f"衛星 {i}"
    prev_seats = {t: "核心席" for t in prev_snap.get("core", [])}
    prev_seats.update({t: "衛星席" for t in prev_snap.get("sat", [])})
    seat_thead = ("<tr><th class=\"bw-l\">席</th><th class=\"bw-l\">代號</th>"
                  "<th title=\"own_score v4：財報後上修／12M 動能／成長封頂 30／品質／盈餘殖利率"
                  "五個排名百分位平均，見下方說明\">排名分</th>"
                  "<th title=\"以該股自己最近一次財報日前最新月度 snapshot 為基準的 FY 加權 EPS "
                  "上修（已排除匯率）；缺財報錨定時退回近三個月，詳見各列 hover\">財報後上修%</th>"
                  "<th class=\"bw-l\" title=\"距下次財報天數；<=7 天標記——分數為財報前快照\">下次財報</th>"
                  "<th title=\"12 減 1 個月價格動能\">12M 動能%</th>"
                  "<th class=\"bw-l\" title=\"核心資格：五年 ROIC 平均或 QGM 五年穩定度達標\">耐久</th>"
                  "<th class=\"bw-l\">時機</th><th class=\"bw-l\">倉位</th>"
                  "<th class=\"bw-l\">DD</th><th class=\"bw-l\">備註</th></tr>")

    seat_rows = ([_seat_tr(r, f"C{j}", lamp_map) for j, r in enumerate(core_seats, 1)]
                + [_seat_tr(r, f"S{j}", lamp_map) for j, r in enumerate(sat_seats, 1)]
                + [_seat_tr(r, f"B{j}", lamp_map, muted=True) for j, r in enumerate(bench_seats, 1)])
    seat_tbl = ('<div class="bw-scroll"><table><thead>' + seat_thead + "</thead><tbody>"
                + "".join(seat_rows) + "</tbody></table></div>")

    seat_legend = f"""<details class="bw-fold" open><summary>怎麼讀這張表</summary>
<div class="bw-note-line">這是研究層陣容——值不值得擁有，月頻換人，不是帳戶持倉。</div>
<div class="bw-note-line"><b>排名分</b>：財報後上修、12M 動能、成長（封頂 30）、品質（FCF÷淨利與稀釋率百分位平均；
增量 ROIC ≥15%＝投資有回報者免計 FCF÷淨利）、盈餘殖利率——五個排名百分位平均。</div>
<div class="bw-note-line"><b>財報後上修</b>：以該股自己最近一次財報日前最新月度 snapshot 為基準的 FY 加權
EPS 上修幅度（已排除匯率影響）——每檔錨定自己的財報日，不是全母體共用一個日曆窗（見頁尾規則
登記「上修改為財報後錨定」）；缺財報錨定（尚未查到最近一次財報日，或查到的財報日之前沒有更早的
月度 snapshot 可比）時退回舊制的近三個月日曆 baseline，個別列 hover 會標基準快照日與錨定方式。
<b>下次財報</b>：距下次財報天數，≤7 天標橘色——提醒這個分數是財報前快照，財報後上修分位可能一週
內就變動。<b>12M 動能</b>：12 減 1 個月價格動能（略過最近一個月）。</div>
<div class="bw-note-line"><b>耐久</b>：核心資格——五年 ROIC 平均達標或 QGM 五年穩定度達標，兩者有一個成立就算。</div>
<div class="bw-note-line"><b>時機</b>：🟢 可進（多頭排列）／🟡 半倉（站上 52 週線但未達綠燈）／
🟠 過熱（12 個月動能過熱）／🔴 等板機（跌破 200 日線、RS 太弱、離高點太遠或階段弱勢）／
⚫ 不合格（未站上 52 週線）。<b>倉位</b>跟時機一對一：正常倉／半倉／零倉．等板機／—。</div>
<div class="bw-note-line"><b>DD</b>：個股報告的裁決標籤，僅供顯示，不影響席位。
<b>備註</b>：⚠ 頂點＝ROIC 高於五年平均 1.3 倍（只能衛星，非下市訊號）；
🟠 過熱＝12 個月動能超過 150%（只能衛星）；🔴 融券高＝融券占流通股比 &gt;10%（只能衛星，
非資格閘、不進 own_score 排序，依據見頁尾規則登記）；<b>基期</b>＝三年 CAGR 因 FY1→FY2
低基期跳增而改用 FY2→FY3 成長率取代；<b>循環守門</b>＝循環股（毛利率跨距大或資本支出
佔營收高）且 PEG 低到可疑，成長與盈餘殖利率分位封頂 50；<b>循環</b>＝循環股但未觸發守門，
純顯示；<b>財報前</b>＝距下次財報 ≤7 天；<b>內部人買／內部人賣</b>＝近 3 個月內部人淨買賣方向，
僅供備註，不進資格與排序；新席／現任／遞補＝本期席位異動狀態。</div>
<div class="bw-note-line">資格門檻：市值 200 億以上、品質閘、三年成長 15%（耐久者 10%）、站上 52 週線、
財報後上修達 5%（缺財報錨定退回三個月）否決、體質拒絕／衰退 ⛔／DD 迴避同樣否決。無產業集中度上限。</div>
<div class="bw-note-line">換人規則：每月第一次排程換一次席；期間只有硬否決能把人換掉，空位由下一名遞補。</div>
<div class="bw-note-line">怎麼用：席位在＋時機綠燈＝正常倉可以買；席位在＋時機紅燈＝先別動，等板機。</div>
</details>"""

    gone = [t for t in prev_seats if t not in seat_label]
    if gone:
        why_map = {r["ticker"]: r for r in rows}
        lines = []
        for t in gone:
            r = why_map.get(t)
            why = (((r or {}).get("grp") or {}).get("why") or [])
            chips = _chips_from_why(why, limit=2) if why else []
            reason = _chips_html(chips) if chips else '<span class="bw-muted">排名分被擠下／不在母體</span>'
            lines.append(f'<div class="bw-note-line">🔻 DOWN <b>{escape(t)}</b>：{reason}</div>')
        changes_html = "".join(lines)
    else:
        changes_html = '<div class="bw-note-line">本期無下席變動。</div>'

    freshness = (f'<div class="bw-note-line">時機更新：{escape(lamp_as_of or "—")}（每日）／'
                f'席位更新：{escape(last_rotation_date or "—")}（每月換席）</div>'
                if (lamp_as_of or last_rotation_date) else "")

    return ('<h3 class="bw-sec">目前席位：核心 5 ＋ 衛星 5 ＋ 候補 5</h3>'
           + '<div class="bw-sub">這就是本月的陣容。C1–C5＝核心席次、S1–S5＝衛星席次、B1–B5＝候補（未坐席，muted）。</div>'
           + freshness
           + seat_tbl + seat_legend + changes_html)


def render_board_html(as_of, rows, core_seats, sat_seats, bench_seats, prev_snap, entered, lamp_map,
                      lamp_as_of=None, last_rotation_date=None) -> str:
    """HTML TABLE 版看板（2026-09-02，取代 <pre> ASCII；2026-09-17 v4 席位表改版——新欄序
    席/代號/排名分/財報後上修/下次財報/12M動能/耐久/時機/倉位/DD/備註，見
    knowledge/rule_ledger.md「v4 席位引擎」「上修改為財報後錨定」兩列）。回傳裸片段
    （無 html/head/body），可直接 innerHTML 或接進另一頁
    <body>。內容與 render_board_text 同源同排序，只是呈現層換成表格＋燈號＋chip。

    `lamp_as_of`／`last_rotation_date`（2026-09-17，見 --lamp-only 段）：轉交
    _seat_section_html() 渲染成「目前席位」區塊的兩行新鮮度戳記。"""
    seat_label = {}
    for i, r in enumerate(core_seats, 1):
        seat_label[r["ticker"]] = f"核心 {i}"
    for i, r in enumerate(sat_seats, 1):
        seat_label[r["ticker"]] = f"衛星 {i}"

    # v4：全母體看板改直接用已排序的 ELIGIBLE 名次（own_score_v4）——只有真的過全部
    # 資格閘的名字才有有效排名分，見 apply_own_score_v4()／grp.own_score_v4()。`rows`
    # 即 main() 的 universe_rows，已被 apply_own_score_v4() 就地回填 score／grp.own，
    # 這裡重新依 pass＋score 排序等同重建一份 ranked，不需要另外傳參數。
    rows_ranked = sorted((r for r in rows if r["grp"].get("pass")), key=lambda r: -(r["score"] or 0))
    own = rows_ranked[:40]

    thead = ("<tr>"
             '<th title="排序名次">#</th>'
             '<th class="bw-l" title="點擊連到該股 DD #decision 錨點（若有 v13+ DD）">Ticker</th>'
             '<th title="own_score v4：財報後上修（缺財報錨定退回三個月）／12M 動能／成長封頂 30／品質／盈餘殖利率五個排名百分位平均——排序鍵">排名分</th>'
             '<th title="FY1→FY3 EPS CAGR（缺 FY3 用 2 年成長率代替）">成長%</th>'
             '<th title="FY1 盈餘殖利率＝100 ÷ FY1 P/E">EY%</th>'
             '<th title="投入資本回報率 ROIC">ROIC%</th>'
             '<th title="自由現金流利潤率">FCF%</th>'
             '<th title="PEG＝FY1 P/E ÷ 成長%">PEG</th>'
             '<th title="FY+1 單月 EPS 修正（燈號，非主否決線；v4 主否決看財報後上修 ≤−5%，缺財報錨定退回三個月，見排名分 hover）">上修燈</th>'
             '<th>位置</th>'
             '<th class="bw-l">階段</th>'
             '<th class="bw-l" title="目前坐核心／衛星席次；空白＝未坐席">席</th>'
             '<th class="bw-l" title="DD 裁決標籤——僅供顯示（2026-09-16 起不否決、不降權）；⚠過期＝逾 180 天">DD</th>'
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
            f'<td class="bw-l">{_stage_pill(tk, lamp_map)}</td>'
            f'<td class="bw-l">{seat_cell}</td>'
            f'<td class="bw-l">{_dd_pill(r.get("dd_tag"))}</td>'
            f'<td class="bw-l">{moat_cell}</td>'
            f'<td class="bw-note">{_chips_html(_note_chips(r))}</td>'
            "</tr>")

    main_tbl = ('<div class="bw-scroll"><table><thead>' + thead + "</thead><tbody>"
                + "".join(body_rows) + "</tbody></table></div>")

    seat_section = _seat_section_html(core_seats, sat_seats, bench_seats, prev_snap, rows, lamp_map,
                                      lamp_as_of, last_rotation_date)

    # ── DD 進場 vs 機械資格 ──
    ok_n = sum(1 for r in entered if r["grp"]["pass"])
    ng = [r for r in entered if not r["grp"]["pass"]]
    dd_gate_sub = f"進場 {len(entered)}：過閘 {ok_n}／未過 {len(ng)}"
    if ng:
        ng_thead = '<tr><th class="bw-l">Ticker</th><th class="bw-l">位置</th><th class="bw-l">原因</th></tr>'
        ng_rows = []
        for r in ng:
            g = r["grp"]
            ng_rows.append(
                f'<tr><td class="bw-l"><strong>{_tk_link(r)}</strong></td>'
                f'<td class="bw-l">{_timing_pill(g.get("p_label"), r.get("r26"), g.get("dist_hi"))}</td>'
                f'<td class="bw-note">{_chips_html(_chips_from_why(g.get("why")))}</td></tr>')
        ng_tbl = (
            '<details class="bw-fold"><summary>DD 進場但機械資格未過：' + str(len(ng)) + ' 檔（點開複審）</summary>'
            '<div class="bw-scroll"><table><thead>' + ng_thead + "</thead><tbody>"
            + "".join(ng_rows) + "</tbody></table></div></details>")
    else:
        ng_tbl = '<div class="bw-note-line">進場票全數過機械三閘，無需人工複審。</div>'

    # ── 可選但先不入席：缺三年成長預估（v3 席位資格 2026-09-09；v4 起 g_three_year
    # 直接併入成長閘 pass/fail——這類名字的 grp.pass 恆為 False，故改從全母體 `rows`
    # 找「其餘資格都過、只差三年成長」的名字，依成長率（單年）降冪排列，不再能沿用
    # `own`（v4 的 own 只含真正 ELIGIBLE 名字）。DD 池名字若也只有 FY1→FY2 單年
    # fallback（缺 FY3 預估）一樣進這條隊。──
    queue_rows = sorted(
        (r for r in rows if r.get("qual") != "light" and not r["grp"].get("g_three_year")
         and r["grp"].get("g") is not None and r["grp"]["g"] >= 15
         and (r["grp"].get("quality") or {}).get("pass") and not r["grp"].get("veto")
         and r["grp"].get("above_w52")),
        key=lambda r: -(r["grp"].get("g") or 0))[:20]
    if queue_rows:
        q_thead = ('<tr><th class="bw-l">Ticker</th><th>擁有層分</th>'
                   '<th title="FY1→FY2 單年成長率（yfinance）——非三年期 Koyfin FY1→FY3 CAGR，兩把尺不等長">成長%（單年）</th>'
                   '<th>ROIC%</th><th>FCF%</th><th>距高%</th><th class="bw-l">位置</th></tr>')
        q_rows = []
        for r in queue_rows:
            g = r["grp"]
            q_rows.append(
                f'<tr><td class="bw-l"><strong>{_tk_link(r)}</strong></td>'
                f"<td>{_num(r.get('score'), 1)}</td><td>{_num(g.get('g'), 1)}</td>"
                f"<td>{_num(r.get('roic'), 1)}</td><td>{_num(r.get('fcf'), 1)}</td>"
                f"<td>{_num(g.get('dist_hi'), 1)}</td>"
                f'<td class="bw-l">{_timing_pill(g.get("p_label"), r.get("r26"), g.get("dist_hi"))}</td></tr>')
        qgm_tbl = ('<div class="bw-scroll"><table><thead>' + q_thead + "</thead><tbody>"
                   + "".join(q_rows) + "</tbody></table></div>")
    else:
        qgm_tbl = '<div class="bw-note-line">目前無候選（都已有三年成長預估或未過機械三閘）。</div>'

    head_line = f"選股看板 v4 · as_of {as_of} · 母體 {len(rows)}（美股含 ADR；台股另建）"
    rule_line = ("排序＝own_score v4：財報後上修（缺財報錨定退回三個月）、12M 動能、成長（封頂 30）、"
                 "品質、盈餘殖利率五個排名百分位在合格集合內平均（成長遇基期效應改用 FY2→FY3 成長率；"
                 "循環股 PEG 過低時觸發循環守門，成長／盈餘殖利率分位封頂 50）。資格要過品質、三年"
                 "成長預估（durable 者 10%、否則 15%）、市值、站上 52 週線、財報後上修達 5%（缺財報"
                 "錨定退回三個月）否決、體質拒絕／衰退 ⛔／DD 迴避同樣否決。核心候選另需耐久（五年 "
                 "ROIC 平均或 QGM 五年穩定度）且不過熱、融券占流通股比不超過 10%；無產業集中度上限。"
                 "內部人買賣僅備註，不進資格與排序。")
    timing_note = ("過熱／融券高（>10%）與頂點不擋資格，只排除核心候選（過熱、融券高）或純顯示"
                   "（頂點）；時機燈是另一層週頻判斷，不進排序。")

    return (
        '<div class="board-wrap">' + _BOARD_CSS
        + f'<div class="bw-head">{escape(head_line)}</div>'
        + f'<div class="bw-rule">{escape(rule_line)}</div>'
        + f'<div class="bw-rule">{escape(timing_note)}</div>'
        + seat_section
        + '<h3 class="bw-sec">全母體看板（擁有層排序）</h3>'
        + '<div class="bw-sub">席位是從這張表由上往下挑出來的<span class="stage-lamp-asof"></span>。</div>'
        + main_tbl
        + '<h3 class="bw-sec">DD 進場 vs 機械資格</h3>'
        + f'<div class="bw-sub">{escape(dd_gate_sub)}——過閘者已在席位或候補中，這裡只列未過者供人工複審。</div>'
        + ng_tbl
        + '<h3 class="bw-sec">可選但先不入席：缺三年成長預估（加進 Koyfin 名單即可）</h3>'
        + '<div class="bw-sub">這些名字三閘都過，但成長只有單年預估（yfinance FY1→FY2，非 Koyfin FY1→FY3 CAGR），'
          '所以只列隊、不佔席、不計遲滯。加進 Koyfin watchlist 補上三年成長率，下次 build 就會脫隊、'
          '以三年成長率重新競爭席位（不需要先有 DD）。</div>'
        + qgm_tbl
        + '<div class="bw-note-line">同內容另存純文字版 <a href="/engine/board.txt">board.txt</a>（終端機／郵件用）。</div>'
        + "</div>"
    )


def _universe_board_row(r: dict, seat_map: dict) -> dict:
    """universe_board.json 單列——直接複用該列已算好的 grp.quality，不重算。"""
    g = r.get("grp") or {}
    q = g.get("quality") or {}
    quality = {"pass": q.get("pass"), "why": q.get("why") or [],
               "roic": q.get("roic"), "fcf": q.get("fcf"), "exempt": bool(q.get("exempt"))}
    return {"ticker": r["ticker"], "src": r.get("src") or "dd-pool", "score": r.get("score"),
            "quality": quality, "g": g.get("g"), "g_method": r.get("g_method"),
            "verdict": r.get("verdict"), "dd_tag": r.get("dd_tag"), "dd_path": r.get("dd_path"),
            "route": r.get("route"), "seat": seat_map.get(r["ticker"])}


def build_universe_board(universe_rows, core_seats, sat_seats, core_bench, sat_bench, as_of) -> dict:
    """docs/engine/universe_board.json：研究母體（DD 池美股 ∪ QGM 品質池 ∪ 可選但先不入席
    候選，即 universe_n 計數的同一份 ~276 檔全母體）——供 cockpit 品質×時機矩陣「研究母體」
    欄；不影響 own_board／席位／遲滯任何既有邏輯。決定性排序：依 ticker 字母序。"""
    seat_map = {}
    for r in core_seats:
        seat_map[r["ticker"]] = "C"
    for r in sat_seats:
        seat_map[r["ticker"]] = "S"
    for r in core_bench + sat_bench:
        seat_map.setdefault(r["ticker"], "B")
    rows = sorted((_universe_board_row(r, seat_map) for r in universe_rows), key=lambda x: x["ticker"])
    return {"schema": "engine-universe-board-v1", "as_of": as_of, "n": len(rows), "rows": rows}


def _last_snapshot_before(snapshots: list[dict], as_of: str) -> dict | None:
    """最近一筆日期嚴格早於 as_of 的 snapshot——同日重跑時跳過「今天自己已寫入」的那筆，
    避免拿今天跟今天比較（self-referential，見 2026-09-09 修復）。"""
    earlier = [s for s in snapshots if s.get("date") and s["date"] < as_of]
    return earlier[-1] if earlier else None


# ── v4 席位引擎：own_score 跨檔百分位 ＋ 月頻輪動（純函式，見 knowledge/rule_ledger.md
#    「v4 席位引擎（2026-09-17）」列）───────────────────────────────────────────

def apply_own_score_v4(universe_rows: list) -> list:
    """v4：在 ELIGIBLE 集合（r["grp"]["pass"] 為真）內算跨檔 own_score_v4 百分位，
    就地回填每列的 r["grp"]["own"]／r["score"]（universe_rows 內的列物件身分不變，
    後續顯示邏輯直接看得到更新；grp 子物件仍照現有慣例換新 dict 避免共享 mutation）。
    回傳「有效名次」清單——只含分數非 None 者（<4/5 百分位缺值不參與排名，仍留在
    universe_rows 供顯示，語意同 sim_seats.py 的 `elig=[r for r in elig if r['comp'] is not None]`），
    依分數降冪排序。"""
    elig = [r for r in universe_rows if r["grp"].get("pass")]
    # load_light_rows() 供給列的 grp 是自己拼的 ad hoc dict（不經 grp_score()），
    # 沒有 "own" key——缺 raw 就當全空（own_score_v4 對缺值一律 None，天然算不出
    # 排名分而落榜，不需要另外特判快審卡）。
    raws = [(r["grp"].get("own") or {}).get("raw") or {} for r in elig]
    results = own_score_v4(raws)
    ranked = []
    for r, res in zip(elig, results):
        r["grp"] = dict(r["grp"])
        r["grp"]["own"] = res
        r["score"] = res["score"] if res["score"] is not None else 0.0
        if res["score"] is not None:
            ranked.append(r)
    ranked.sort(key=lambda r: -r["score"])
    return ranked


def rotation_month(as_of: str) -> str:
    """as_of（'YYYY-MM-DD'）→ 'YYYY-MM'，月頻輪動比較粒度。"""
    return (as_of or "")[:7]


def select_fresh_roster(ranked: list, core_slots: int = CORE_SLOTS, sat_slots: int = SAT_SLOTS) -> dict:
    """v4 整批重選（pure）：`ranked` 為 apply_own_score_v4() 的輸出（已按分數降冪
    排序、只含有效名次者）。核心＝core_candidate（耐久且不過熱，見 row_dict()）中
    前 core_slots 名；衛星＝母體中所有未坐核心席者（含過熱／頂點／非耐久——衛星
    公開競爭，v3 沿用至今的設計）前 sat_slots 名。無產業/主題集中度上限（2026-09-17
    持有人拍板）。回傳 {"core":[ticker,...], "sat":[ticker,...]}。"""
    core = [r for r in ranked if r.get("core_candidate")][:core_slots]
    core_t = {r["ticker"] for r in core}
    sat = [r for r in ranked if r["ticker"] not in core_t][:sat_slots]
    return {"core": [r["ticker"] for r in core], "sat": [r["ticker"] for r in sat]}


def hard_veto_v4(r: dict, w52_fail_streak: int = 0) -> str | None:
    """v4 硬否決判定（pure）——回傳觸發理由，或 None（未觸發）。六個條件之一：
    DD 迴避／體質拒絕／衰退 ⛔／上修達 5%（財報後錨定，缺值退回三個月；皆已在
    grp_score 算成 grp["veto_*"] 細項）、市值不足（r["cap_ok"]，apply_cap() 算好）、
    連續 `w52_fail_streak` 次週跑站不上 52 週線（跨次跑狀態，呼叫端從 ledger 讀，
    見 W52_FAIL_STREAK_VETO）。只用在「月中沿用現任席」的路徑——整批重選
    （select_fresh_roster）不需要這個。"""
    g = r.get("grp") or {}
    if g.get("veto_dd_avoid"):
        return "DD 迴避"
    if g.get("veto_quality_reject"):
        return "體質拒絕"
    if g.get("veto_decline"):
        return "衰退 ⛔"
    if g.get("veto_revision"):
        return "財報後上修 ≤ −5" if g.get("rev_anchor") == "earnings" else "三月上修 ≤ −5"
    if not r.get("cap_ok", True):
        return "市值不足"
    if w52_fail_streak >= W52_FAIL_STREAK_VETO:
        return "連續兩週跌破 52 週線"
    return None


def rotate_roster(current_month: str, last_rotation_month, prev_roster, ranked: list,
                  w52_fail_streaks: dict | None = None,
                  core_slots: int = CORE_SLOTS, sat_slots: int = SAT_SLOTS,
                  all_by_ticker: dict | None = None) -> dict:
    """v4 月頻輪動主體（pure）。
      - 本月第一次跑（last_rotation_month != current_month，或無 prev_roster）→
        整批重選（select_fresh_roster），rotated=True。
      - 同月內的後續跑 → 沿用 prev_roster；任何現任席命中 hard_veto_v4() 立即移除，
        空位由 ranked 中尚未入席的下一名遞補（核心缺只從 core_candidate 池找、
        衛星缺對全母體公開競爭，與整批重選同一套資格邏輯）；找不到人可補則留空。

    重要：現任席的沿用檢查查的是 `all_by_ticker`（全母體，含資格閘未過者），不是
    `ranked`（只含 ELIGIBLE、已排名者）——月中軟性資格失守（成長掉出門檻、品質閘
    未過等）不該立刻下席，只有 hard_veto_v4() 認定的六個硬否決才下席，這正是月頻
    輪動要給的「不因單週雜訊洗掉席位」的容忍度。`all_by_ticker` 未提供時 fallback
    用 `ranked` 建索引（相容舊呼叫，但退化成「掉出 ELIGIBLE 即視同跌出母體」，
    僅供測試用；正式呼叫請務必傳全母體）。
    回傳 {"core":[...], "sat":[...], "rotated": bool, "removed":[(ticker,why),...],
    "filled":[(track,ticker),...]}（ticker 清單，不是列物件）。"""
    w52_fail_streaks = w52_fail_streaks or {}
    universe_by_ticker = all_by_ticker if all_by_ticker is not None else {r["ticker"]: r for r in ranked}

    if prev_roster is None or last_rotation_month != current_month:
        fresh = select_fresh_roster(ranked, core_slots, sat_slots)
        return {"core": fresh["core"], "sat": fresh["sat"], "rotated": True,
                "removed": [], "filled": []}

    removed: list = []

    def _carry(track: str) -> list:
        kept = []
        for t in prev_roster.get(track, []) or []:
            r = universe_by_ticker.get(t)
            if r is None:
                removed.append((t, "跌出母體（下市或資料消失）"))
                continue
            why = hard_veto_v4(r, w52_fail_streaks.get(t, 0))
            if why:
                removed.append((t, why))
                continue
            kept.append(t)   # 沿用——即便本次未過全部資格閘，非硬否決不下席
        return kept

    core_kept = _carry("core")
    sat_kept = _carry("sat")
    removed_tickers = {t for t, _why in removed}
    filled: list = []

    def _fill(kept: list, slots: int, pool: list, track: str) -> list:
        # 剛被硬否決下席的名字本回合不得遞補回自己的空位——即便它仍在 ranked／
        # core_pool 裡（例如 w52 連續兩週否決，資格本身其餘條件都還過），見
        # test_rotate_roster_w52_streak_evicts_after_two_consecutive_runs。
        seated = set(core_kept) | set(sat_kept) | removed_tickers
        for r in pool:
            if len(kept) >= slots:
                break
            if r["ticker"] in seated:
                continue
            kept.append(r["ticker"])
            seated.add(r["ticker"])
            filled.append((track, r["ticker"]))
        return kept

    core_pool = [r for r in ranked if r.get("core_candidate")]
    core_kept = _fill(core_kept, core_slots, core_pool, "core")
    sat_kept = _fill(sat_kept, sat_slots, ranked, "sat")   # 衛星公開競爭：全母體皆可遞補

    return {"core": core_kept, "sat": sat_kept, "rotated": False,
            "removed": removed, "filled": filled}


# ── --lamp-only（2026-09-17 持有人拍板，見檔頭 --lamp-only 段／knowledge/rule_ledger.md
#    「時機燈日更、席位月更」列）：唯讀時機燈日更，見 run_lamp_only() ────────────────

def _find_last_rotation_date(snapshots: list[dict]) -> str | None:
    """帳本 snapshots 中最近一筆 rotated=True 的日期——供席位表『席位更新：』顯示用
    （main() 與 run_lamp_only() 皆呼叫）。"""
    return next((sn.get("date") for sn in reversed(snapshots or []) if sn.get("rotated")), None)


def _load_stock_sources() -> tuple[dict, dict]:
    """--lamp-only 用的輕量來源查表：DD 池（dd-screener latest.json）＋ QGM 品質池
    （US／TW），只為了給既有席位/候補 ticker 補最新 ma／timing 欄位，不做母體重建
    （不含快審卡、不算 latest_none 的三年 CAGR fallback——那些只影響 own_score，
    --lamp-only 不碰，見 run_lamp_only() docstring）。"""
    try:
        stocks = json.loads(DD_LATEST.read_text(encoding="utf-8"))["stocks"]
    except (OSError, json.JSONDecodeError, KeyError):
        stocks = []
    stocks = [s for s in stocks if s.get("dd_status") != "none" and market_ok(s["ticker"])]
    stocks_map = {s["ticker"]: s for s in stocks}
    for local, adr in LISTING_ALIAS.items():
        if adr in stocks_map:
            stocks_map.pop(local, None)
    qgm_map = {r["ticker"]: r for r in load_qgm_rows(stocks_map)}
    return stocks_map, qgm_map


def _refresh_row_timing(row: dict, s: dict, lamp_map: dict) -> None:
    """--lamp-only 唯讀刷新：就地更新單一席位/候補列的時機欄位（above_w52／p_label／
    dist_hi／price／overheated／lamp／action／r26／r52）。借用 grp_score() 算 P 閘與
    overheated（own／score／pass／veto／g／r 等擁有層欄位一律丟棄不採用）——不重新
    發明公式，只借同一份既有邏輯；row 其餘既有欄位（score／rank／route／core_candidate／
    seat_note／durable_5y…）原樣保留，見檔頭 --lamp-only 段：唯讀模式不得動席位/分數/
    排名。"""
    st = weekly_structure(s["ticker"])
    s["_r26"] = st.get("r26") if st else None
    s["_r52"] = st.get("r52") if st else None
    fresh = grp_score(s)
    g = dict(row["grp"])
    for k in ("above_w52", "p_label", "dist_hi", "price", "overheated"):
        g[k] = fresh[k]
    row["grp"] = g
    s["_stage_code"] = lamp_map.get(s["ticker"])
    s["_overheated"] = g["overheated"]
    lamp = timing_lamp(s)
    row["lamp"] = lamp
    row["action"] = LAMP_ACTION.get(lamp["code"], "—")
    row["r26"] = s.get("_r26")
    row["r52"] = s.get("_r52")


def _patch_seat_section_in_text(old_text: str, new_lines: list[str]) -> str | None:
    """在既有 board.txt 內容裡原地替換『== 目前席位…』區塊（run_lamp_only() 用）；
    找不到起訖 marker（格式意外改變）回傳 None，呼叫端原樣保留舊檔不覆寫，不擋排程。"""
    lines = old_text.split("\n")
    start_marker = "== 目前席位：核心 5 ＋ 衛星 5 ＋ 候補 5"
    end_marker = (f"{'#':>{W_IDX}} {'ticker':<{W_TICKER}} {'score':>{W_SCORE}} {'grow':>{W_GROW}} "
                 f"{'EY':>{W_EY}} {'ROIC':>{W_ROIC}} {'FCF':>{W_FCF}} {'PEG':>{W_PEG}} {'rev1m':>{W_REV}} "
                 f"{'timing':<{W_TIMING}} {'stage':<{W_STAGE}} {'seat':<{W_SEAT}} {'dd':<{W_DD}} {'moat':<{W_MOAT}} note")
    try:
        start_idx = lines.index(start_marker)
        end_idx = lines.index(end_marker, start_idx + 1)
    except ValueError:
        return None
    return "\n".join(lines[:start_idx] + new_lines + lines[end_idx:])


def _patch_seat_section_in_html(old_html: str, new_section_html: str) -> str | None:
    """同上，_board_body.html 版（字串子字串替換，見 run_lamp_only()）。"""
    start_marker = '<h3 class="bw-sec">目前席位：核心 5 ＋ 衛星 5 ＋ 候補 5</h3>'
    end_marker = '<h3 class="bw-sec">全母體看板（擁有層排序）</h3>'
    start_idx = old_html.find(start_marker)
    end_idx = old_html.find(end_marker, start_idx + 1) if start_idx >= 0 else -1
    if start_idx < 0 or end_idx < 0:
        return None
    return old_html[:start_idx] + new_section_html + old_html[end_idx:]


def run_lamp_only() -> int:
    """--lamp-only（唯讀）：daily-taipei-morning.yml 每日跑，只重算既有席位／候補的
    時機燈＋倉位，不重跑選股／輪動、不寫 arena-ledger.json。依據（2026-09-17 持有人
    拍板，見 knowledge/rule_ledger.md「時機燈日更、席位月更」列）：時機燈原料
    （dd-screener timing.*/ma.*、docs/stages/data/lamp.json）本來就每日更新，但過去
    只有 weekly-engine.yml 的 --ledger 跑次會讀進來算 lamp，導致席位表的燈號最多
    落後 6 天。這支旗標只把「讀」的頻率補成跟「寫」一樣，不動「值不值得擁有」
    （own_score／席位／排名）這條月頻時鐘——見檔頭 --lamp-only 段。

    席位名單優先讀 arena-ledger.json 的 roster，缺則退回 arena.json 現有
    core_seats／sat_seats；兩者皆缺（或 arena.json 本身缺檔/壞檔）→ 印 warning、
    exit 0，不擋排程。只改 arena.json 的席位列本身＋lamp_as_of／lamp_source／
    lamp_last_rotation_date 三個戳記；board.txt／_board_body.html 只原地替換
    『目前席位』區塊（_seat_section_lines()／_seat_section_html()，與 main() 全量
    重建共用同一份格式），全母體表／DD 對照／候選佇列維持上次 `--ledger` 跑次內容
    不變——那些欄位的排序鍵是跨檔百分位，只有 weekly-engine.yml 的 `--ledger` 跑次
    能動。"""
    try:
        payload = json.loads(ARENA_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("::warning::--lamp-only：docs/engine/arena.json 不存在或壞檔，無法刷新時機燈，略過")
        return 0

    try:
        ledger = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        ledger = {}

    row_by_ticker = {r["ticker"]: r for r in
                     (payload.get("core_seats") or []) + (payload.get("sat_seats") or [])
                     + (payload.get("bench_seats") or [])}
    roster = ledger.get("roster") or {}
    core_tickers = roster.get("core") or [r["ticker"] for r in payload.get("core_seats") or []]
    sat_tickers = roster.get("sat") or [r["ticker"] for r in payload.get("sat_seats") or []]
    core_seats = [row_by_ticker[t] for t in core_tickers if t in row_by_ticker]
    sat_seats = [row_by_ticker[t] for t in sat_tickers if t in row_by_ticker]
    bench_seats = payload.get("bench_seats") or []
    if not core_seats and not sat_seats and not bench_seats:
        print("::warning::--lamp-only：arena-ledger.json／arena.json 皆無可用席位，略過")
        return 0

    stocks_map, qgm_map = _load_stock_sources()
    lamp_map = load_lamp()
    missing = []
    for row in core_seats + sat_seats + bench_seats:
        t = row["ticker"]
        s = stocks_map.get(t) or qgm_map.get(t)
        if s is None:
            missing.append(t)
            continue
        _refresh_row_timing(row, s, lamp_map)
    if missing:
        print(f"  [lamp-only] 找不到來源資料，時機燈維持前次值：{missing}")

    try:
        lamp_as_of = json.loads(DD_LATEST.read_text(encoding="utf-8")).get("as_of", "—")
    except (OSError, json.JSONDecodeError):
        lamp_as_of = "—"
    last_rotation_date = _find_last_rotation_date(ledger.get("snapshots") or [])

    payload["core_seats"] = core_seats
    payload["sat_seats"] = sat_seats
    payload["bench_seats"] = bench_seats
    payload["lamp_as_of"] = lamp_as_of
    payload["lamp_source"] = "daily"
    payload["lamp_last_rotation_date"] = last_rotation_date
    ARENA_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    prev_snap = _last_snapshot_before(ledger.get("snapshots") or [], lamp_as_of) or {"core": [], "sat": []}
    new_seat_lines = _seat_section_lines(core_seats, sat_seats, bench_seats, prev_snap, [],
                                         lamp_as_of, last_rotation_date)
    if BOARD_TXT.exists():
        patched = _patch_seat_section_in_text(BOARD_TXT.read_text(encoding="utf-8"), new_seat_lines)
        if patched is None:
            print("::warning::--lamp-only：board.txt 找不到『目前席位』區塊 marker，略過該檔刷新")
        else:
            BOARD_TXT.write_text(patched, encoding="utf-8")
    else:
        print("::warning::--lamp-only：docs/engine/board.txt 不存在，略過該檔刷新")

    new_seat_html = _seat_section_html(core_seats, sat_seats, bench_seats, prev_snap, [], lamp_map,
                                       lamp_as_of, last_rotation_date)
    if BOARD_HTML.exists():
        patched_html = _patch_seat_section_in_html(BOARD_HTML.read_text(encoding="utf-8"), new_seat_html)
        if patched_html is None:
            print("::warning::--lamp-only：_board_body.html 找不到『目前席位』區塊 marker，略過該檔刷新")
        else:
            BOARD_HTML.write_text(patched_html, encoding="utf-8")
    else:
        print("::warning::--lamp-only：docs/engine/_board_body.html 不存在，略過該檔刷新")

    print(f"lamp-only: 刷新 core={len(core_seats)} sat={len(sat_seats)} bench={len(bench_seats)}｜"
          f"lamp_as_of={lamp_as_of}｜席位更新={last_rotation_date}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", action="store_true",
                         help="寫入 arena-ledger.json（last_rotation_month／roster／snapshots，"
                              "月頻輪動時鐘前進）；僅 weekly-engine.yml 排程使用，手動跑不帶此旗標＝帳本唯讀")
    parser.add_argument("--lamp-only", action="store_true",
                         help="唯讀模式，只重算既有席位／候補的時機燈與倉位（daily-taipei-morning.yml 用）；"
                              "不重跑選股／輪動、不寫 arena-ledger.json，見檔頭 --lamp-only 段")
    args = parser.parse_args()
    if args.lamp_only:
        return run_lamp_only()
    stocks = json.loads(DD_LATEST.read_text(encoding="utf-8"))["stocks"]
    # latest.json 若以 --include-non-dd 產出，無 DD 列（dd_status="none"）改由 load_qgm_rows 供給
    #（帶 _src／_durable_5y／_mktcap），這裡先排除以免搶走 QGM 列的身份標記
    # 2026-09-16：丟掉前先留一份給 load_qgm_rows 補三年 CAGR（見該函式 docstring）
    latest_none = {s["ticker"]: s for s in stocks if s.get("dd_status") == "none"}
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

    # ── v4 席位引擎（2026-09-17 持有人拍板，見 knowledge/rule_ledger.md「v4 席位引擎」列）──
    #   母體＝DD 池（全部裁決）∪ QGM 品質池（US＋TW）∪ 快審卡（不變）
    #   資格＝品質閘（ROIC/FCF，不變）∩ 三年成長預估必備（Koyfin FY1→FY3 CAGR，durable_5y
    #        者 10% 否則 15%）∩ 市值 ∩ 位置閘（站上 52 週線）∩ 上修否決（財報後錨定 ≤−5%，
    #        缺財報錨定退回三個月日曆窗，FY+1 單月 ≤−10% 僅兩者皆缺值時 fallback；2026-09-17
    #        見 rule_ledger「上修改為財報後錨定」列）∩ 新硬否決（體質拒絕／衰退 ⛔／DD 迴避
    #        180 天內）。過熱（12-1 月動能 >150%）與頂點（roic_vs_5y_x ≥1.3）不是資格閘，
    #        只排除核心候選（過熱）或純顯示（頂點）——見 grp.grp_score()。
    #   核心候選＝route=="core"（耐久，grp.grp_route）AND 不過熱；核心＝候選前 5 名。
    #   衛星＝母體中所有未坐核心席的合格名字（含過熱／頂點／非耐久）前 5 名，公開競爭、
    #   無產業/主題集中度上限。
    #   排序＝own_score v4：財報後上修（缺財報錨定退回三個月）／12-1 月動能／成長封頂 30／
    #   品質／盈餘殖利率五個百分位在 ELIGIBLE 集合內互相比較後平均（見 grp.own_score_v4()）。
    #   輪動＝月頻：每月第一次 --ledger 跑重新整批選一次，期間只有硬否決（迴避／拒絕／
    #   ⛔／財報後上修達 5%（缺財報錨定退回三個月）／市值不足／連兩週跌破 52 週線）能換人，
    #   空位由下一名遞補（見 rotate_roster()）。
    #   DD 不再是入席前提：只做迴避否決，觀望／進場僅供角色標籤參考（role_mismatch 顯示用）。
    stocks_map = {s["ticker"]: s for s in stocks}
    # 同一家公司的 ADR／本地掛牌只留一個（席位不得重複曝險）：本地掛牌讓位給 ADR
    aliased = set()
    for local, adr in LISTING_ALIAS.items():
        if adr in stocks_map:
            stocks_map.pop(local, None); aliased.add(local)
    stocks = [s for s in stocks if s["ticker"] in stocks_map]
    qgm_rows = load_qgm_rows(stocks_map, exclude=aliased, latest_none=latest_none)
    qgm_tickers = {r["ticker"] for r in qgm_rows}
    # v4 時機燈（grp.timing_lamp，pure）需要階段代碼——lamp_map 提前載入（原本在
    # render 前才讀），注入每檔 s["_stage_code"]，讓 row_dict() 能在算完 grp_score()
    # 的 overheated 之後一次把燈號算好、掛在列上（見下 row_dict() 呼叫端改法）。
    lamp_map = load_lamp()
    for s in stocks + qgm_rows:
        s["_stage_code"] = lamp_map.get(s["ticker"])
    universe_rows = [row_dict(s) for s in stocks] + [row_dict(s) for s in qgm_rows]
    # dedupe 修復（2026-09-09）：load_qgm_rows／load_light_rows 過去只各自對
    # stocks_map（dd-pool）去重，沒對過彼此——INCY 這類同時在 QGM 品質池與快審卡
    # 出現的名字會在 universe_rows 進兩列。first source wins: dd-pool > qgm > light。
    light = load_light_rows(stocks_map, exclude=qgm_tickers)
    universe_rows += [r for r in light if r["verdict"] in ("進場", "觀望", None)]

    # 防線：universe_rows 不得有重複 ticker（席位不得重複曝險）。
    _ticker_seq = [r["ticker"] for r in universe_rows]
    _dupes = sorted({t for t in _ticker_seq if _ticker_seq.count(t) > 1})
    if _dupes:
        print(f"  [dedupe] ⚠ universe_rows 仍有重複 ticker（不應發生）：{_dupes}")
    assert not _dupes, f"universe_rows 出現重複 ticker，席位會重複曝險：{_dupes}"

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

    # ── v4 own_score 跨檔百分位（見 grp.own_score_v4()）：只在 ELIGIBLE 集合內比較 ──
    ranked = apply_own_score_v4(universe_rows)   # 已依 score 降冪排序、只含有效名次者
    for i, r in enumerate(ranked, 1):
        r["rank"] = i
    ranked_by_ticker = {r["ticker"]: r for r in ranked}

    # ── 月頻輪動（arena-ledger.json，見 knowledge/rule_ledger.md「v4 席位引擎」列）──
    try:
        ledger0 = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        ledger0 = {"schema_version": "4.0", "snapshots": []}
    try:
        as_of = json.loads(DD_LATEST.read_text(encoding="utf-8")).get("as_of", "—")
    except (OSError, json.JSONDecodeError):
        as_of = "—"
    current_month = rotation_month(as_of)
    last_rotation_month = ledger0.get("last_rotation_month")
    prev_roster = ledger0.get("roster")            # {"core":[...], "sat":[...]}——月度持久化
    w52_fail_streaks = ledger0.get("w52_fail_streak") or {}
    # prev＝上一筆「日期嚴格早於今天」的 snapshot，只給「席位變動帳本」的 up/down 對照用
    # （沿用既有 render_seat_changes／render_board_text 的 NEW/FROM 標記邏輯，與月頻輪動
    # 本身的 carry-forward 狀態〔prev_roster〕是兩件事：後者決定「這個月坐誰」，前者只是
    # 「跟上一筆記錄比誰上誰下」的顯示層對照）。
    prev = _last_snapshot_before(ledger0.get("snapshots", []), as_of) or {"core": [], "sat": []}

    all_by_ticker = {r["ticker"]: r for r in universe_rows}
    rotation = rotate_roster(current_month, last_rotation_month, prev_roster, ranked, w52_fail_streaks,
                             all_by_ticker=all_by_ticker)
    # 沿用的現任席可能本次未過全部資格閘（非硬否決不下席，見 rotate_roster()）——
    # 這種列不在 ranked（ELIGIBLE-only）裡，改查全母體 all_by_ticker 才能顯示。
    core_seats = [ranked_by_ticker.get(t) or all_by_ticker.get(t) for t in rotation["core"]]
    core_seats = [r for r in core_seats if r is not None]
    sat_seats = [ranked_by_ticker.get(t) or all_by_ticker.get(t) for t in rotation["sat"]]
    sat_seats = [r for r in sat_seats if r is not None]
    core_seated = {r["ticker"] for r in core_seats}
    sat_seated = {r["ticker"] for r in sat_seats}
    seated_all = core_seated | sat_seated

    # 備註欄用：新席／現任／遞補（Step 3 備註欄），並把移除理由掛回去顯示。
    prior_tickers = set((prev_roster or {}).get("core", []) or []) | set((prev_roster or {}).get("sat", []) or [])
    filled_tickers = {t for _, t in rotation["filled"]}
    removed_map = dict(rotation["removed"])
    for r in core_seats + sat_seats:
        t = r["ticker"]
        if rotation["rotated"]:
            r["seat_note"] = "現任" if t in prior_tickers else "新席"
        else:
            r["seat_note"] = "遞補" if t in filled_tickers else "現任"

    # 候補（Step 3：候補 1–5，合併單一清單，不分核心/衛星）——核心板凳／衛星板凳仍各自
    # 保留供 arena.html「M5 對照組」既有的擂台/板凳文案與 universe_board 沿用。
    core_bench = [r for r in ranked if r.get("core_candidate") and r["ticker"] not in seated_all][:8]
    sat_bench = [r for r in ranked if r["ticker"] not in seated_all and r["ticker"]
                not in {x["ticker"] for x in core_bench}][:8]
    bench_seats = sorted(core_bench + sat_bench, key=lambda r: -(r["score"] or 0))[:5]
    entered = [r for r in universe_rows if r["verdict"] == "進場"]

    challengers = [r for r in ranked if r["ticker"] not in seated_all]

    # 擂台配對（v2 起沿用）：軌別配對——核心席 vs 核心向挑戰者、衛星席 vs 衛星向挑戰者
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
    # 帳本寫入只在 --ledger（weekly-engine.yml 排程）才發生；手動/ad-hoc 跑只讀既有帳本
    # 算席位、照常寫 arena.json 等輸出，不推進月頻輪動時鐘、不追加 snapshot（見檔頭
    # docstring 與 knowledge/rule_ledger.md「v4 席位引擎」列）。
    ledger = ledger0

    def _seat_meta(r: dict) -> dict:
        """v3 稽核用列（2026-09-09）：無 DD 席位 vs 有 DD 席位 12 週報酬比較的 kill
        condition 需要知道每個 snapshot 當下每個席位的屬性，光有 ticker 清單對不了帳。"""
        return {
            "ticker": r["ticker"],
            "score": r.get("score"),
            "has_dd": bool(r.get("dd_path")),
            "verdict": r.get("verdict"),
            "durable_5y": r.get("durable_5y"),
            "route": r.get("route"),
            "price": (r.get("grp") or {}).get("price"),
        }

    snap = {"date": as_of,
            "core": [r["ticker"] for r in core_seats],
            "sat": [r["ticker"] for r in sat_seats],
            "core_meta": [_seat_meta(r) for r in core_seats],
            "sat_meta": [_seat_meta(r) for r in sat_seats],
            "rotated": rotation["rotated"],
            "removed": [{"ticker": t, "why": w} for t, w in rotation["removed"]],
            "rule_version": "v4"}
    changes = []
    # 比較基準＝嚴格早於今天的最後一筆——同日重跑不可拿「今天已寫入的自己」當基準
    # （self-referential bug：會把「今天跟今天比較」的假差異當成真變動，見檔頭說明）。
    prev_snap = _last_snapshot_before(ledger["snapshots"], as_of)
    today_entry_exists = bool(ledger["snapshots"]) and ledger["snapshots"][-1]["date"] == as_of
    if args.ledger:
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
            if today_entry_exists:
                ledger["snapshots"][-1] = snap   # 同日重跑覆蓋（冪等）——不再依附自我比較
            else:
                ledger["snapshots"].append(snap)
        # v4 月頻輪動狀態（見 rotate_roster() docstring）——只在 --ledger 排程跑時前進：
        #   last_rotation_month／roster：下次跑靠這兩個值判斷「這個月是否已經選過」；
        #   w52_fail_streak：above_w52 為 False 逐次 +1、True 歸零（清掉不再追蹤的
        #   ticker，避免帳本無限增長）、None（資料缺）維持原值不動。
        new_streak = dict(w52_fail_streaks)
        for r in universe_rows:
            above = r["grp"].get("above_w52")
            if above is False:
                new_streak[r["ticker"]] = new_streak.get(r["ticker"], 0) + 1
            elif above is True:
                new_streak.pop(r["ticker"], None)
        ledger["w52_fail_streak"] = new_streak
        ledger["last_rotation_month"] = current_month
        ledger["roster"] = {"core": [r["ticker"] for r in core_seats],
                            "sat": [r["ticker"] for r in sat_seats]}
        LEDGER_JSON.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_JSON.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                               encoding="utf-8")
    else:
        print("帳本唯讀（未帶 --ledger）：last_rotation_month／roster／snapshots 未寫入，輪動時鐘未前進。")
    recent_changes = [c for s in ledger["snapshots"][-6:] for c in (s.get("changes") or [])]

    dial = regime_dial()
    def compact(r):
        g = r["grp"]; o = g.get("own") or {}
        return {"ticker": r["ticker"], "score": r["score"], "rank": r.get("rank"),
                "g": g.get("g"), "g_method": r.get("g_method"),
                "ey": (o.get("raw") or {}).get("ey"), "roic": r.get("roic"), "fcf": r.get("fcf"),
                "peg": r.get("peg"), "eps_rev_3m_pct": g.get("eps_rev_3m_pct"), "p_label": g.get("p_label"),
                # 財報錨定上修（2026-09-17）：實際用於排序/否決的值＋錨定方式/基準快照日/
                # 距下次財報天數，見 grp._revision_anchor()。
                "rev_used_pct": g.get("rev_used_pct"), "rev_anchor": g.get("rev_anchor"),
                "rev_baseline_date": g.get("rev_baseline_date"),
                "days_to_next_earnings": g.get("days_to_next_earnings"),
                "p_rev": o.get("p_rev"), "p_mom": o.get("p_mom"), "p_g": o.get("p_g"),
                "p_q": o.get("p_q"), "p_ey": o.get("p_ey"),
                "overheated": g.get("overheated"), "peak": g.get("peak"),
                "high_short_interest": g.get("high_short_interest"),
                "short_interest_pct_float": g.get("short_interest_pct_float"),
                "base_effect": g.get("base_effect"),
                "cyclical": o.get("cyclical"), "cycle_guard": o.get("cycle_guard"),
                "insider_signal": r.get("insider_signal"), "insider_net_buy_3m": r.get("insider_net_buy_3m"),
                "durable_5y": r.get("durable_5y"), "durable_source": r.get("durable_source"),
                "lamp": r.get("lamp"), "action": r.get("action"),
                "r26": r.get("r26"), "pass": g.get("pass"), "why": g.get("why"),
                "route": r["route"], "route_why": r.get("route_why"),
                "dd_tag": r.get("dd_tag"), "verdict": r.get("verdict"),
                "moat": r.get("moat"), "src": r.get("src"), "seat_note": r.get("seat_note"),
                "dd_path": r.get("dd_path")}
    own_board = [compact(r) for r in universe_rows
                 if (r["grp"].get("quality") or {}).get("pass") and (r["score"] or 0) > 0][:60]
    # 時機燈新鮮度戳記（2026-09-17，見 --lamp-only 段）：全量重建時 lamp 一定是這一跑
    # 剛算好的（as_of＝今天），席位更新日＝今天（若本跑真的輪動）否則沿用帳本最近一次
    # rotated=True 的 snapshot 日期——run_lamp_only() 唯讀刷新時共用同一份格式函式。
    last_rotation_date = as_of if rotation["rotated"] else _find_last_rotation_date(ledger.get("snapshots") or [])
    board_text = render_board_text(as_of, universe_rows, core_seats, sat_seats, bench_seats, prev, entered, lamp_map,
                                   lamp_as_of=as_of, last_rotation_date=last_rotation_date)
    BOARD_TXT.write_text(board_text, encoding="utf-8")
    board_html = render_board_html(as_of, universe_rows, core_seats, sat_seats, bench_seats, prev, entered, lamp_map,
                                   lamp_as_of=as_of, last_rotation_date=last_rotation_date)
    BOARD_HTML.write_text(board_html, encoding="utf-8")
    payload = {
        "schema_version": "4.0",
        "lamp_as_of": as_of, "lamp_source": "weekly", "lamp_last_rotation_date": last_rotation_date,
        "method": ("v4.1 席位引擎（2026-09-17，同日再改：上修改為財報後錨定）：核心候選＝耐久（五年 ROIC 平均 "
                  "≥15% 或 QGM 五年穩定度 ≥75%）且不過熱（12-1 月動能 ≤150%）且融券占流通股比不超過 "
                  "10%（融券高比照過熱，只排除核心候選、不進排序、不是資格閘）；排序＝own_score v4，"
                  "財報後上修（以該股自己最近一次財報日前最新月度 snapshot 為基準，缺財報錨定退回舊制"
                  "近三個月日曆窗）／12-1 月動能／成長封頂 30（遇基期效應改用 FY2→FY3 成長率；循環股 "
                  "PEG 過低觸發循環守門、成長與盈餘殖利率分位封頂 50）／品質（FCF∶淨利＋稀釋率，投資"
                  "有回報者免計 FCF∶淨利）／盈餘殖利率五個百分位在合格集合內平均；財報後上修達 5%"
                  "（缺財報錨定退回三個月）否決（FY+1 單月 ≤−10% 僅兩者皆缺值時 fallback）；無產業"
                  "集中度上限；內部人買賣僅備註，不進資格與排序；每月第一次排程重選，期間只有硬否決"
                  "能換人、空位遞補"),
        "universe_n": len(universe_rows),
        "seats_without_card": sorted(r["ticker"] for r in core_seats + sat_seats if r["ticker"] not in card_stats),
        "own_board": own_board,
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regime": dial,
        "rotation": {"rotated": rotation["rotated"], "current_month": current_month,
                    "removed": [{"ticker": t, "why": w} for t, w in rotation["removed"]],
                    "filled": [{"track": tr, "ticker": t} for tr, t in rotation["filled"]]},
        "core_seats": core_seats, "core_bench": core_bench[:8],
        "sat_seats": sat_seats, "sat_vacant": SAT_SLOTS - len(sat_seats),
        "bench_seats": bench_seats,
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
席位資格（<b>v4 擁有層×時機層</b>，2026-09-17 持有人拍板）＝<b>品質閘</b>（ROIC ≥15 ∧ FCF ≥10；capex 週期豁免 ROIC ≥25 ∧ FCF ≥0）×
<b>成長閘</b>（FY1→FY3 EPS CAGR ≥15%，耐久者放寬至 10%；且成長必須是三年期 Koyfin 數字——只有 FY1→FY2 單年 fallback 的名字不入席，改列「可選但先不入席」隊列）× <b>位置閘</b>（站上 52 週線）× <b>財報後上修否決</b>（≤−5%，以該股自己最近一次財報日前最新月度 snapshot 為基準，缺財報錨定退回舊制近三個月日曆窗；FY+1 單月 ≤−10% 僅兩者皆缺值時 fallback；2026-09-17 見規則登記「上修改為財報後錨定」）× 新硬否決（體質拒絕／衰退 ⛔／DD 迴避 180 天內）。
排序＝<b>own_score v4</b>：財報後上修（缺財報錨定退回三個月）、12-1 月動能、成長（封頂 30）、品質（FCF÷淨利與稀釋率百分位平均；投資有回報者〔增量 ROIC ≥15%〕免計 FCF÷淨利）、盈餘殖利率，五個排名百分位在合格集合內互相比較後平均。成長遇<b>基期效應</b>（FY1→FY2 因低基期跳增 &gt;1.6x 且 FY2→FY3 成長 &lt;20%）改用 FY2→FY3 成長率取代；<b>循環股守門</b>（毛利率跨距 &gt;20pp 或資本支出佔營收 &gt;15%，且 PEG &lt;0.3）觸發時成長／盈餘殖利率分位封頂 50。
<b>過熱／融券高／頂點不是資格閘</b>：12-1 月動能 &gt;150%（缺值 fallback 26 週漲幅 &gt;80%）＝過熱、融券占流通股比 &gt;10%＝融券高，兩者皆排除核心候選（只能衛星，不進排序，依據見頁尾規則登記）；roic_vs_5y_x ≥1.3＝頂點，純顯示註記（⚠），不影響核心候選資格。<b>內部人買賣</b>（近 3 個月淨股數）僅供備註，不進資格與排序。
<b>DD 選配</b>：不是入席前提，只做迴避否決（180 天內），觀望／進場僅供角色標籤參考（僅供顯示）。
<b>月頻輪動</b>：每月第一次排程整批重選一次；期間只有硬否決（迴避／拒絕／⛔／財報後上修達 5%（缺財報錨定退回三個月）／市值不足／連兩週跌破 52 週線）能換人，空位由下一名遞補。
<b>軌別路由</b>：核心候選另需耐久——五年 ROIC 平均 ≥15%（Koyfin）或 QGM 五年穩定度 ≥75%（兩者有一成立即可）→ 核心；未達標或無耐久資料 → 衛星。DD 角色不影響軌別，只當顯示標籤（與軌別衝突時標 ⚠ 供人裁）。<b>耐久＋不過熱＋融券不高＝核心候選，不等於保證核心席</b>：沒卡進核心前 5 名的核心候選會回頭跟其餘合格名字一起搶衛星 5 席（純比 own_score），此時席位表仍標示其軌別為「核心」（代表可長抱），另加註「耐久・暫居衛星」。
<b>市值門檻 ≥ ${MKTCAP_MIN/1e9:.0f}B</b>（持有人 2026-07-04 拍板：席位與主榜資格層；雷達發現層照掃全宇宙）。
<b>母體＝美股含 ADR；台股另建（.TW 不在本看板，2026-09-02 持有人拍板）</b>。無產業/主題集中度上限（2026-09-17 持有人拍板）。
<b>快審卡</b>：衛星席另接受 🪶 快審卡（週期位置＋陷阱＋護城河快評），與三年成長閘、DD 皆無關。
資格未過的進場票落板凳、寧缺勿濫。</div>
<div class="asof">資料源 dd-screener latest.json ＋ QGM 品質池（US／TW）＋週線 cache ｜ v4 擁有層×時機層 ｜ 月頻輪動</div>
</div>
<div class="block"><h2>選股看板 v4</h2>
<div class="block-sub">own_score 排序（值不值得擁有）與時機燈（現在能不能買）分開讀；DD 只做迴避否決與角色標籤。</div>
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
挑戰者池 top（三閘全過）：{escape('、'.join(r['ticker'] for r in payload['challengers_top'][:10]) or '—')}。</div>
{_STAGE_LAMP_SCRIPT}"""

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    universe_board = build_universe_board(universe_rows, core_seats, sat_seats, core_bench, sat_bench, as_of)
    UNIVERSE_BOARD_JSON.write_text(json.dumps(universe_board, ensure_ascii=False, indent=1), encoding="utf-8")
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
