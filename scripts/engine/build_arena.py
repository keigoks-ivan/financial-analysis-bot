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
Usage: python3 scripts/engine/build_arena.py [--ledger] [--daily | --lamp-only]

--ledger：帳本（arena-ledger.json：last_rotation_month／roster.core／w52_fail_streak／
snapshots）預設唯讀——不帶旗標時，用「既有帳本」算核心席並照常寫 arena.json／board.txt／
fragments，但不推進月頻輪動時鐘、不追加 snapshot。只有 `.github/workflows/weekly-engine.yml`
的排程跑次帶 `--ledger` 真正寫帳本，避免手動/ad-hoc 執行提早觸發輪動或誤記週跌破 52 週線
次數（沿用 2026-09-08 VRTX/INCY 教訓的精神：跑次不能當週次算）。

--daily（2026-09-17 持有人拍板，v5 席位引擎起取代 v4「--lamp-only 只刷時機燈」的窄流程，
見 knowledge/rule_ledger.md「v5 席位引擎」列／grp.py 檔頭 v5 段第 5 點）：全量重跑資格／
池／排序／時機燈／距歷史新高，帳本唯讀（不寫 arena-ledger.json）——這其實就是不帶
`--ledger` 的預設路徑本身（本來就是「全量重算、只讀不寫帳本」），`--daily` 只是給
workflow 檔一個明講意圖的旗標名，不觸發額外分支。核心席名單仍從 arena-ledger.json 的
`roster.core` 讀（月頻輪動時鐘不因 `--daily` 前進）；若現任核心席本次命中硬否決
（hard_veto_v5()），本次輸出會立即顯示替換（空位由池遞補），但要等下一次
`weekly-engine.yml` 的 `--ledger` 排程跑次才會真正把這次替換寫回帳本、前進月頻時鐘。
`--lamp-only` 是 v4 舊名，向下相容別名，語意等同 `--daily`——v5 起沒有「窄流程只刷時機
燈」這回事，因為資格/池/排序本身已經便宜到可以每天全量重算（見 grp.py 檔頭 v5 段：
上修排序鍵只在新的 Koyfin xlsx 匯入時才變，但距歷史新高／時機燈／倉位每天都變，
`--daily` 一次重算兩者，頁首同時標 `rev_data_as_of`／`price_as_of` 兩個日期供讀者
分辨資料新鮮度）。掛在 `.github/workflows/daily-taipei-morning.yml`（與
`daily-non-fundamental-refresh.yml` 手動 dispatch 同步）Step 1 之後，取代舊有的
`--lamp-only` 呼叫。

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

v5 席位引擎（2026-09-17 持有人拍板「品質派 ∩ 獲利上修 ∩ 突破還原權息歷史新高」；
完整判斷規則見 scripts/engine/grp.py 檔頭 v5 段／knowledge/rule_ledger.md「v5 席位
引擎」列／notes/site-internal/root/_seat_engine_v5_20260917.md）——本檔改動：
  1. 母體/資格/池：不變的是母體組成（DD 池∪QGM 品質池∪快審卡）；grp_score() 已把
     耐久（durable_5y）與融券高升級為資格閘本體，本檔只需在 ELIGIBLE 集合
     （r["grp"]["pass"]）上再疊加「上修 ≥5%」這道池門檻（grp.in_pool()），見
     main() 的 `pool_rows`／`not_in_pool_rows`。
  2. 排序：`pool_rows` 依 grp.pool_sort_key()（上修降冪、tie-break implied_growth_pct、
     再 tie-break EY）排序，取代 v4 的 own_score_v4 百分位排序；後者（`ranked`／
     `apply_own_score_v4()`）保留一輪只做「v4 對照」tooltip 與全母體對照表。
  3. 席位：核心＝ `select_fresh_roster_v5()`/`rotate_roster()` 對 `pool_rows` 取前
     5（月頻輪動機制不變，只是候選池換成 pool_rows）；衛星軌取消，`waiting_pool`
     （池扣掉核心）依時機燈拆成 `buyable`（綠/橘燈）與 `waiting_rest`（其餘）兩段
     顯示。`sat_seats`（arena.json）保留 key 向下相容，內容改成整個 `waiting_pool`
     （每列帶 `track:"pool"` 標記）；`sat_vacant` 恆為 0（池無固定席次概念）。
  4. 時機燈：grp.timing_lamp() 全面改讀 `ma.dist_ath_pct`（見 build_dd_screener.
     compute_ath_highs()，還原權息全歷史 ATH，快取 data/ath_cache.json），本檔
     row_dict() 只多把 `dist_ath_pct`/`ath_adj_price`/`ath_adj_date`/`ath_source`
     從 `s["ma"]` 帶進顯示列（見 _row_cells()／_shared_thead_cells() 欄位改版）。
  5. `--daily`（見上）取代 v4 `--lamp-only` 窄流程；run_lamp_only() 與其專用的
     `_refresh_row_timing`/`_fresh_timing_bundle`/`_patch_*_in_*` 系列輔助函式已
     移除（連同 v4 的 `select_fresh_roster`/`hard_veto_v4`/舊版 `rotate_roster`
     ——v5 版同名函式見上方 select_fresh_roster_v5()/hard_veto_v5()/rotate_roster()）。
  6. M5 對照組（`_arena_body.html`，PREREG 凍結，只換殼不改文）：其「衛星席位」
     沿用固定 5 席快照概念，資料源改接 `waiting_pool[:SAT_SLOTS]`（見 main() 內
     `sat_seats_m5` 變數），與 payload 真正的 v5 `sat_seats`（全量等待池）是兩件
     事，故獨立變數不共用，避免污染 M5 頁面既有的擂台/板凳文案。
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
    P_LABEL_HTML, PEAK_ROIC_X, POOL_REV_MIN, Q_FCF_MIN, Q_ROIC_MIN, R26_OVERHEAT_FALLBACK,
    R_VETO_FY1, VAL_PEG_MAX, VAL_PE_VS_5Y_MAX, cap_ok, fetch_caps, grp_route, grp_score, in_pool,
    market_ok, own_score_v4, pool_sort_key, timing_lamp,
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
    _apply_durable_fallback(s)   # durable_5y 就緒——v5 起是 grp_score() 資格閘本體，見該函式
    g = grp_score(s)             # v5：品質派資格（成長/位置/上修否決/硬否決/耐久/融券高）皆已在 grp_score 內算好
    route, route_why = grp_route(s)
    # v5（2026-09-17，見 grp.py 檔頭 v5 段）：耐久與融券高已升級為 grp_score() 的
    # 資格閘本體（g["pass"] 已反映），「core_candidate」保留給 M5 對照組擂台頁
    # （_arena_body.html，PREREG 凍結、本輪不重做）的板凳/擂台邏輯沿用，定義簡化為
    # 「軌別為 core 且非融券高」——過熱不再排除核心候選（v5 核心＝池前 5，見
    # select_fresh_roster()/rotate_roster()，不再讀本欄位）。
    core_candidate = route == "core" and not g["high_short_interest"]
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
            # v5（2026-09-17，見 grp.py 檔頭 v5 段）：距歷史新高／implied_growth_pct
            # 是池排序（grp.pool_sort_key()）與 timing_lamp() 板機的原料，直接從 s
            # 讀（timing_lamp 已經讀過 s["ma"]，這裡另存一份供席位表欄位／tooltip用）。
            "dist_ath_pct": (s.get("ma") or {}).get("dist_ath_pct"),
            "ath_adj_price": (s.get("ma") or {}).get("ath_adj_price"),
            "ath_adj_date": (s.get("ma") or {}).get("ath_adj_date"),
            "ath_source": (s.get("ma") or {}).get("ath_source"),
            "implied_growth_pct": s.get("implied_growth_pct"),
            # VCP 深度 1（2026-09-18，見 notes/site-internal/root/
            # _seat_engine_v5_1_20260918.md §3／knowledge/rule_ledger.md「VCP 深度 1」
            # 列）：dd-screener 已算好（scripts/build_dd_screener.py::compute_vcp_tag()），
            # 這裡直接搬過來——只當③等待池 🟡 組排序鍵與「底部」欄標籤用，不進
            # timing_lamp()／grp_score()／LAMP_ACTION 任何一個燈號或倉位判斷。
            "vcp_scope": s.get("vcp_scope"), "vcp_gate": s.get("vcp_gate"),
            "vcp_score": s.get("vcp_score"), "vcp_pullback_count": s.get("vcp_pullback_count"),
            "vcp_last_pullback_pct": s.get("vcp_last_pullback_pct"),
            "vcp_vol_dryup_ratio": s.get("vcp_vol_dryup_ratio"),
            "vcp_base_age_days": s.get("vcp_base_age_days"),
            "vcp_tight": bool(s.get("vcp_tight")),
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
W_DISTATH = 7   # v5（2026-09-17）：距歷史新高% 欄寬，取代 v4 的 W_MOM12（12M 動能%欄，v5 排序不再用）
# 財報錨定上修（2026-09-17）：「下次財報」欄寬——board.txt 席位表新增欄，見
# _seat_section_lines()／knowledge/rule_ledger.md「上修改為財報後錨定」列。
W_NEXTEARN = 6
# v5.1（2026-09-18）：估值閘欄寬——格式「{G/R/-} {peg}/{pe_vs_5y_x}」（如 "G 1.4/1.1"），
# 光碼 ASCII 化沿用「規則 A」（見上方 _char_width 註解），emoji 燈號留給 HTML 版；
# 見 grp.py VAL_PEG_MAX／VAL_PE_VS_5Y_MAX、_val_ascii_cell()。
W_VAL = 11
VAL_LIGHT_ASCII = {"🟢": "G", "🔴": "R", "⚪": "-"}
# VCP 深度 1（2026-09-18）：「底部」欄寬——ASCII 代碼沿用「規則 A」（純 ASCII，中文
# 說明留給 HTML 版 _bottom_cell_html() 與圖例，見 _vcp_kind()／_bottom_ascii_cell()）。
# 最長字串「T4/100.0」8 字元，留一點餘裕。
W_BOTTOM = 10


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


def _val_ascii_cell(val: dict | None) -> str:
    """估值閘 ASCII 單欄（v5.1，2026-09-18）：「{G/R/-} {peg}/{multiple}」，缺值以
    "-" 佔位（規則 A：光碼用 ASCII 字母，emoji 留給 HTML 版的 _val_cell_html()）。
    `val` 是 grp["valuation"]（grp.valuation_gate() 輸出），可能是 None（舊資料）。"""
    val = val or {}
    code = VAL_LIGHT_ASCII.get(val.get("light"), "-")
    peg = val.get("peg"); x = val.get("pe_vs_5y_x")
    peg_s = f"{peg:.1f}" if peg is not None else "-"
    x_s = f"{x:.1f}" if x is not None else "-"
    return f"{code} {peg_s}/{x_s}"


def _vcp_kind(v: dict) -> str:
    """VCP 深度 1（2026-09-18，見 notes/site-internal/root/_seat_engine_v5_1_20260918.md
    §3／knowledge/rule_ledger.md「VCP 深度 1」列）：純分類函式，供 `_bottom_ascii_cell()`
    （ASCII 看板）與 `_bottom_cell_html()`（HTML 池表）共用，避免兩邊各判一次而日後
    漂移（同 `_val_ascii_cell()`／`_val_cell_html()` 都吃同一份 `val` dict 的慣例）。

    `v` 可以是 row_dict() 或 `_flat_view()` 的輸出——兩者都帶 `vcp_scope`／`vcp_tight`／
    `lamp` 同名欄位。回傳 "breakout_tight"／"breakout_loose"（🟢/🟠 燈號且 vcp_scope
    ="computed"，見下）／"tight"／"loose"（其餘 vcp_scope="computed"）／"far"
    （vcp_scope="far_from_ath"）／"insufficient"（vcp_scope="insufficient_bars"）／
    "none"（vcp_scope 缺值——舊資料或 skip_ma 建置）。

    breakout 判定只看 `lamp["code"] in ("green","hot")`——這是燈號本身已經亮起的列
    （可買／核心），VCP 只負責換一種措辭（「緊縮後突破」／「鬆散突破」），不影響
    燈號或倉位；🟡／🔴／⚫ 三組列一律走 tight/loose 分支。"""
    scope = v.get("vcp_scope")
    if scope == "far_from_ath":
        return "far"
    if scope == "insufficient_bars":
        return "insufficient"
    if scope != "computed":
        return "none"
    tight = bool(v.get("vcp_tight"))
    lamp_code = (v.get("lamp") or {}).get("code")
    if lamp_code in ("green", "hot"):
        return "breakout_tight" if tight else "breakout_loose"
    return "tight" if tight else "loose"


def _bottom_ascii_cell(v: dict) -> str:
    """底部欄 ASCII 單欄（VCP 深度 1，2026-09-18）——規則 A：光碼用 ASCII，中文說明
    （「緊 n段·末段 −x%」等）留給 HTML 版 `_bottom_cell_html()` 與圖例／欄位說明行。
    T=緊、L=鬆、BRKT=緊縮後突破、BRKL=鬆散突破、SHRT=資料不足（<221 根日線）、
    -=距新高超過 10%（未算）。"""
    kind = _vcp_kind(v)
    if kind == "far":
        return "-"
    if kind == "insufficient":
        return "SHRT"
    if kind == "breakout_tight":
        return "BRKT"
    if kind == "breakout_loose":
        return "BRKL"
    n = v.get("vcp_pullback_count")
    n_s = str(int(n)) if isinstance(n, (int, float)) else "-"
    if kind == "tight":
        last_pb = v.get("vcp_last_pullback_pct")
        pb_s = f"{last_pb:.1f}" if isinstance(last_pb, (int, float)) else "-"
        return f"T{n_s}/{pb_s}"
    if kind == "loose":
        return f"L{n_s}"
    return "-"


def _ticker_col(t) -> str:
    return _pad(str(t)[:W_TICKER], W_TICKER)


def _own_board_ascii_hdr() -> str:
    """全母體對照表（v4 對照排序）ASCII 表頭——render_board_text() 的唯一 source，
    避免手打第二份而漂移。v5（2026-09-17，見 grp.py 檔頭 v5 段）：rank/mom12 欄
    換成 distATH。v5.1（2026-09-18）：dur 之後新增 val（估值閘），見 _val_ascii_cell()。
    VCP 深度 1（2026-09-18）：dd 之後新增 bottom（底部緊度），見 _bottom_ascii_cell()。"""
    return (f"{'#':>{W_IDX}} {'ticker':<{W_TICKER}} {'rev':>{W_REV3M}} {'distATH':>{W_DISTATH}} "
           f"{'nextE':>{W_NEXTEARN}} {'dur':<{W_DUR}} {'val':<{W_VAL}} {'lamp':<{W_LAMPCODE}} "
           f"{'act':<{W_ACTCODE}} {'seat':<{W_SEATCODE}} {'dd':<{W_DD}} {'bottom':<{W_BOTTOM}} note")


def _own_board_ascii_row(i: int, v: dict, seat_code: dict) -> str:
    """全母體對照表單一 ASCII 列（own_board[]，`_flat_view()` 扁平 schema）。欄序與
    寬度同 `_pool_ascii_row()` 的池列（rev/distATH/nextE/dur/lamp/act/seat/dd/note），
    只是第一欄是 v4 對照排名名次而非席次代碼，且多一欄「席」標目前坐哪一核心席。
    `seat_code`＝{ticker: "C1"}，未坐席留空白。"""
    lamp = v.get("lamp") or {}
    days_ne = v.get("days_to_next_earnings")
    next_earn_cell = f"{int(days_ne)}d" if days_ne is not None else "-"
    note_bits = []
    if v.get("peak"):
        note_bits.append("頂點")
    if v.get("base_effect"):
        note_bits.append("基期")
    if v.get("cycle_guard"):
        note_bits.append("循環守門")
    elif v.get("cyclical"):
        note_bits.append("循環")
    if v.get("insider_signal") == "買":
        note_bits.append("內部人買")
    elif v.get("insider_signal") == "賣":
        note_bits.append("內部人賣")
    if days_ne is not None and 0 <= days_ne <= 7:
        note_bits.append("財報前")
    if v.get("g_method") == "FY1→FY2 單年":
        note_bits.append("成長=FY1→FY2 單年")
    return (
        f"{i:>{W_IDX}} {_ticker_col(v['ticker'])} "
        f"{_n(v.get('rev_used_pct'), W_REV3M)} {_n(v.get('dist_ath_pct'), W_DISTATH)} "
        f"{_pad(next_earn_cell, W_NEXTEARN, right=True)} "
        f"{_pad('Y' if v.get('durable_5y') else '-', W_DUR)} "
        f"{_pad(_val_ascii_cell(v.get('valuation')), W_VAL)} "
        f"{_pad(LAMP_CODE_ASCII.get(lamp.get('code'), '-'), W_LAMPCODE)} "
        f"{_pad(ACTION_CODE_ASCII.get(lamp.get('code'), '-'), W_ACTCODE)} "
        f"{_pad(seat_code.get(v['ticker'], ''), W_SEATCODE)} "
        f"{_pad(dd_ascii(v)[:W_DD], W_DD)} "
        f"{_pad(_bottom_ascii_cell(v), W_BOTTOM)} {'；'.join(note_bits)}"
    )


def _pool_ascii_row(label, r: dict) -> str:
    """v5 池／核心席 ASCII 單列（nested row_dict() 形狀）——① 核心席與 ②③ 池表共用
    同一份格式，`label` 是席次代碼（"C1"）或池內排序名次（int），見 grp.py 檔頭
    v5 段。取代 v4 `_seat_section_lines()` 逐列展開寫法。"""
    g = r["grp"]
    lamp = r.get("lamp") or {}
    note_bits = []
    if g.get("peak"):
        note_bits.append("頂點")
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
    if r.get("seat_note"):
        note_bits.append(r["seat_note"])
    next_earn_cell = f"{int(days_ne)}d" if days_ne is not None else "-"
    return (
        f"{_pad(str(label), W_SEATCODE)} {_ticker_col(r['ticker'])} "
        f"{_n(g.get('rev_used_pct'), W_REV3M)} {_n(r.get('dist_ath_pct'), W_DISTATH)} "
        f"{_pad(next_earn_cell, W_NEXTEARN, right=True)} "
        f"{_pad('Y' if r.get('durable_5y') else '-', W_DUR)} "
        f"{_pad(_val_ascii_cell(g.get('valuation')), W_VAL)} "
        f"{_pad(LAMP_CODE_ASCII.get(lamp.get('code'), '-'), W_LAMPCODE)} "
        f"{_pad(ACTION_CODE_ASCII.get(lamp.get('code'), '-'), W_ACTCODE)} "
        f"{_pad(dd_ascii(r)[:W_DD], W_DD)} "
        f"{_pad(_bottom_ascii_cell(r), W_BOTTOM)} {'；'.join(note_bits)}"
    )


_POOL_ASCII_HDR_SEAT = (f"{'seat':<{W_SEATCODE}} {'ticker':<{W_TICKER}} {'rev':>{W_REV3M}} "
                        f"{'distATH':>{W_DISTATH}} {'nextE':>{W_NEXTEARN}} {'dur':<{W_DUR}} "
                        f"{'val':<{W_VAL}} "
                        f"{'lamp':<{W_LAMPCODE}} {'act':<{W_ACTCODE}} {'dd':<{W_DD}} "
                        f"{'bottom':<{W_BOTTOM}} note")
_POOL_ASCII_HDR_IDX = (f"{'#':<{W_SEATCODE}} {'ticker':<{W_TICKER}} {'rev':>{W_REV3M}} "
                       f"{'distATH':>{W_DISTATH}} {'nextE':>{W_NEXTEARN}} {'dur':<{W_DUR}} "
                       f"{'val':<{W_VAL}} "
                       f"{'lamp':<{W_LAMPCODE}} {'act':<{W_ACTCODE}} {'dd':<{W_DD}} "
                       f"{'bottom':<{W_BOTTOM}} note")


def _group_waiting_pool_by_timing(waiting_rest: list) -> tuple[list, list, list]:
    """v5（2026-09-17 owner follow-up，見 knowledge/rule_ledger.md「v5 席位引擎」
    列）：③ 等待池依時機燈分三段顯示——🟡 接近新高（距新高 −10%~−3%，站上 200 日線）
    ／🔴 拉回中（距新高 <−10% 或跌破 200 日線）／⚫ 資料缺（`dist_ath_pct` 缺值，
    燈號退回 yellow fallback，無法歸類進前兩段）。分組只看 `dist_ath_pct` 是否存在
    與 `lamp["code"]`是否為 "red"——`waiting_rest` 本身已排除 green/hot（見②可買
    定義），故其餘只會落在 yellow 或 red，本函式不重算燈號。

    VCP 深度 1（2026-09-18，見 notes/site-internal/root/_seat_engine_v5_1_20260918.md
    §3／knowledge/rule_ledger.md「VCP 深度 1」列）：🟡 組另外用 `vcp_tight` 做一次
    穩定排序（`vcp_tight=True` 排前面），同值（tie）維持傳入順序——因為傳入順序本身
    已是 `grp.pool_sort_key()` 的上修降冪排序，Python `sort()` 是穩定排序，這一步
    等於「先看底部緊不緊，再看上修」而不用重新算 tie-break。🔴／⚫ 兩組不動，維持
    傳入順序（只有 🟡 是「還沒突破、值得盯緊」的池，🔴 已經在拉回、⚫ 沒資料可排）。"""
    yellow, red, gray = [], [], []
    for r in waiting_rest:
        if r.get("dist_ath_pct") is None:
            gray.append(r)
        elif (r.get("lamp") or {}).get("code") == "red":
            red.append(r)
        else:
            yellow.append(r)
    yellow.sort(key=lambda r: not r.get("vcp_tight"))
    return yellow, red, gray


_WAIT_GROUP_LABELS = (
    ("🟡 接近新高（距新高 −10%~−3%，站上 200 日線）", "yellow"),
    ("🔴 拉回中（距新高 <−10% 或跌破 200 日線）", "red"),
    ("⚫ 資料缺（距歷史新高資料不足，無法歸類）", "gray"),
)


def _pool_section_lines(core_seats, buyable, waiting_rest, prev_snap, rows,
                        lamp_as_of=None, last_rotation_date=None) -> list[str]:
    """v5『① 核心席（5）／② 可買／③ 等待池』區塊（board.txt 用，含 DOWN 異動列）——
    取代 v4「核心5＋衛星5＋候補5」（見 grp.py 檔頭 v5 段第 3-4 點／
    knowledge/rule_ledger.md「v5 席位引擎」列）。核心＝池前 5（月頻輪動，硬否決
    立即下席、空位由池遞補，見 rotate_roster()）；可買＝等待池中時機燈 green/hot
    者（「今天板機亮的」，可能是空清單）；等待池＝其餘池成員（依上修排序，即
    `pool_rows` 扣掉核心後剩下的，見呼叫端）。"""
    seat_of = {r["ticker"]: "核心席" for r in core_seats}
    prev_seats = {t: "核心席" for t in prev_snap.get("core", [])}

    L = ["== ① 核心席（5）"]
    if lamp_as_of or last_rotation_date:
        L.append(f"時機更新：{lamp_as_of or '—'}（每日）／席位更新：{last_rotation_date or '—'}（每月換席）")
    L.append(_POOL_ASCII_HDR_SEAT)
    for j, r in enumerate(core_seats, 1):
        L.append(_pool_ascii_row(f"C{j}", r))
    gone = [t for t in prev_seats if t not in seat_of]
    if gone:
        why = {r["ticker"]: r for r in rows}
        for t in gone:
            r = why.get(t)
            why_txt = "；".join((((r or {}).get("grp") or {}).get("why") or [])[:2]) or ("排名分被擠下" if r else "不在母體")
            L.append(f"  DOWN {_ticker_col(t)}：{why_txt}")
    L.append("")

    L.append(f"== ② 可買（等待池中時機燈綠/橘，共 {len(buyable)} 檔——今天板機亮的）")
    if buyable:
        L.append(_POOL_ASCII_HDR_IDX)
        for i, r in enumerate(buyable, 1):
            L.append(_pool_ascii_row(i, r))
    else:
        L.append("  （無——等待池目前沒有名字板機亮燈）")
    L.append("")

    L.append(f"== ③ 等待池（上修強、還沒突破，共 {len(waiting_rest)} 檔；依時機燈分組，組內依上修排序）")
    if not waiting_rest:
        L.append("  （無）")
    else:
        yellow, red, gray = _group_waiting_pool_by_timing(waiting_rest)
        groups = {"yellow": yellow, "red": red, "gray": gray}
        for label, key in _WAIT_GROUP_LABELS:
            group = groups[key]
            if not group:
                continue
            L.append(f"  -- {label}（{len(group)} 檔）")
            L.append(_POOL_ASCII_HDR_IDX)
            for i, r in enumerate(group, 1):
                L.append(_pool_ascii_row(i, r))
    L.append("")
    return L


def render_board_text(as_of, rows, core_seats, buyable, waiting_rest, not_in_pool_rows, prev_snap,
                      entered, lamp_map, rev_data_as_of=None, price_as_of=None,
                      lamp_as_of=None, last_rotation_date=None) -> str:
    """v5 附錄 B 式等寬看板（2026-09-17，見 grp.py 檔頭 v5 段／knowledge/rule_ledger.md
    「v5 席位引擎」列，取代 v4「核心5＋衛星5＋候補5」）：① 核心席（5）／② 可買／
    ③ 等待池／④ 品質過閘、上修未達 5%＋全母體 v4 對照排序＋DD 進場 vs 機械資格＋
    無 DD 過閘候選。純文字，同時寫 docs/engine/board.txt 與 <pre> 嵌頁
    （docs/engine/_arena_body.html、docs/cockpit/index.html 皆讀同一份文字）。

    對齊規則：瀏覽器對 CJK 常用 fallback 字型，其字寬不保證是等寬字型 cell 的精準 2 倍，
    f-string {x:w} 補白也只算 code point 不算顯示寬度——兩者都會讓含中文/emoji 的欄位
    在瀏覽器 <pre> 裡跑版。故主表 note 欄以左一律 ASCII 代碼，任何字型都保證對齊；
    中文只留在最後的 note 欄（不需要再對齊）與表頭上方的圖例行（純 prose，非欄位）。

    `rev_data_as_of`／`price_as_of`（daily 全量重跑，見 grp.py 檔頭 v5 段）：上修
    （池排序鍵）只在新的 Koyfin xlsx 匯入時真的變動，價格／距歷史新高／時機燈每天
    都變——頁首分開標兩個日期，讀者才看得出「排序」與「板機」各自的資料新鮮度。
    `lamp_as_of`／`last_rotation_date`：「核心席」區塊的兩行新鮮度戳記，見
    _pool_section_lines()。"""
    seat_code = {r["ticker"]: f"C{j}" for j, r in enumerate(core_seats, 1)}

    L = []
    freshness_bits = []
    if rev_data_as_of:
        freshness_bits.append(f"上修資料（Koyfin xlsx）as_of {rev_data_as_of}")
    if price_as_of:
        freshness_bits.append(f"價格/距新高/時機燈 as_of {price_as_of}")
    freshness = "｜".join(freshness_bits)
    L.append(f"選股看板 v5｜as_of {as_of}" + (f"｜{freshness}" if freshness else "")
             + f"｜母體 {len(rows)}（DD 池＋QGM 無 DD＋快審卡）"
             "｜母體＝美股含 ADR；台股另建（.TW 不在本看板）")
    L.append("資格＝品質派（品質閘×三年成長×站上 52 週線×耐久一致性）、排序＝上修"
             "（財報後錨定，缺值退回三月）、板機＝突破還原權息歷史新高。核心月頻換人，"
             "其餘每日重排；這是研究層陣容，不是帳戶持倉。")
    L.append("池＝資格全過且耐久達標的名字中，財報後上修 ≥5% 者；池內依上修降冪排序，"
             "同值 tie-break implied_growth_pct、再 tie-break 盈餘殖利率（own_score_v4 "
             "五百分位對照分保留一輪，見全母體對照表與各列 hover 的「v4 對照」，不參與"
             "本排序）。核心＝池前 5，月頻輪動（每月第一次排程整批重選一次，期間僅硬"
             "否決能換人、空位由池遞補）。衛星軌已取消——沒卡進核心前 5 的池成員全部"
             "叫「等待池」，依時機燈分組：②可買（綠/橘燈，今天板機亮的）；③等待池"
             "（其餘）再依時機燈細分🟡接近新高／🔴拉回中／⚫資料缺三段，組內依上修排序。")
    L.append("耐久＝QGM 五年 ROIC 穩定度 ≥75%，或 Koyfin 五年平均∧三年平均∧現值三者"
             "皆 ≥15%——一致性判準，不是單一數字；不耐久即不進池，v5 沒有衛星席可以"
             "退。融券占流通股比 >10% 亦整體排除（同理，沒有衛星席可以收留）。過熱"
             "（12-1 月動能 >150%）與頂點（roic_vs_5y_x ≥1.3）不擋資格：過熱只影響"
             "時機燈（🟠半倉），頂點純顯示。")
    L.append("估值閘（v5.1，2026-09-18）＝PEG（現價重算 live_peg 優先，缺則 Koyfin peg）"
             ">2.0，或 PE NTM 相對五年均倍數 >1.5x，任一則紅——紅燈整體排除、不進池；"
             "兩者皆缺不算否決，標 ⚪ 缺值。這是入池／月頻換席的資格閘，不是月中硬"
             "否決，核心席不因估值轉紅在月中被踢。")
    L.append("欄位說明：rev=財報後上修%（已排除匯率；以該股自己最近一次財報日前最新"
             "月度 snapshot 為基準，缺財報錨定退回三個月）、distATH=距還原權息全歷史"
             "最高收盤價%（非 52 週高）、nextE=距下次財報天數、dur=耐久（Y=達標）、"
             "val=估值閘（G=綠 R=紅 -=缺值，接 PEG/PE 相對五年均倍數）、"
             "lamp=時機燈、act=倉位（跟 lamp 一對一，每日更新）、seat/#=核心席次或池內"
             "排序名次、dd=DD 標籤（僅供顯示）、bottom=底部緊度（VCP，只在距新高 10% "
             "以內算，T{n}/{末段回檔%}=緊、L{n}=鬆、BRKT=緊縮後突破、BRKL=鬆散突破、"
             "SHRT=資料不足、-=距新高超過 10% 未算；只排 🟡 組序、不改燈號和倉位）、"
             "note=備註（頂點/循環/循環守門/基期/內部人/財報前/新席）")
    L.append("lamp/act 代碼：GRN/FULL=可進·正常倉（距新高 ≥−3% 且站上 200 日線）、"
             "YLW/HALF=半倉（距新高 −10%~−3%）、HOT/HALF=過熱·半倉（動能 >150% 但仍在"
             "突破帶附近）、RED/ZERO=等板機·零倉（距新高 <−10% 或跌破 200 日線）、"
             "OUT/-=不合格·未站上 52 週線")
    L.append("dd 代碼：IN/WATCH/AVOID/legacy/none，core/sat/trk=角色，Nd=天數，"
             "!old=逾 180 天過期")
    L.append("怎麼用：核心或②可買＝現在可以買；③等待池＝上修夠強但還沒突破，等板機。")
    L.append("")
    L.extend(_pool_section_lines(core_seats, buyable, waiting_rest, prev_snap, rows,
                                 lamp_as_of, last_rotation_date))

    L.append(f"== ④ 品質過閘、上修未達 5%（共 {len(not_in_pool_rows)} 檔，僅供複審，不進池）")
    if not_in_pool_rows:
        L.append(_POOL_ASCII_HDR_IDX)
        for i, r in enumerate(not_in_pool_rows[:40], 1):
            L.append(_pool_ascii_row(i, r))
    else:
        L.append("  （無）")
    L.append("")

    L.append("== 全母體看板（v4 對照排序，僅供對照——上方 ①②③ 才是 v5 實際排序）")
    L.append(_own_board_ascii_hdr())
    # v5：全母體對照表仍用舊 own_score_v4 名次（見 apply_own_score_v4()），只做對照，
    # 不影響 ①②③ 的池排序（後者用 grp.pool_sort_key()，見呼叫端 main()）。
    own = sorted((r for r in rows if r["grp"].get("pass")), key=lambda r: -(r["score"] or 0))
    for i, r in enumerate(own[:40], 1):
        L.append(_own_board_ascii_row(i, _flat_view(r), seat_code))
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
    (re.compile(r"^估值閘紅燈"), lambda w, m: "估值閘紅燈"),   # v5.1，見 grp.valuation_gate()
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


def _val_cell_html(val: dict | None) -> str:
    """估值閘欄（v5.1，2026-09-18，見 grp.valuation_gate()）：「{燈} {PEG}x／{倍數}x」，
    缺其一顯示「—」；兩者皆缺（⚪）整格顯示「⚪ 缺值」。`val` 是 grp["valuation"]，
    可能是 None（舊資料，缺該欄位）。紅燈在池／全母體表理論上不會出現——紅燈即不
    ELIGIBLE，見 grp_score() all_pass；此處仍完整處理三色，供「DD 進場 vs 機械
    資格」以外、未來若有別的呼叫端要顯示非 ELIGIBLE 列時沿用。"""
    val = val or {}
    light = val.get("light")
    if light != "🔴" and light != "🟢":
        title = val.get("why") or "估值閘：PEG 與五年均倍數皆缺"
        return f'<span class="bw-pill bw-pill-mut" title="{escape(title)}">⚪ 缺值</span>'
    peg, x = val.get("peg"), val.get("pe_vs_5y_x")
    peg_s = f"{peg:.1f}x" if peg is not None else "—"
    x_s = f"{x:.1f}x" if x is not None else "—"
    title_bits = [f"PEG 來源：{'現價重算 live_peg' if val.get('peg_source') == 'live' else 'Koyfin peg'}"
                 if val.get("peg_source") else "PEG 缺值"]
    if val.get("why"):
        title_bits.append(val["why"])
    cls = "up" if light == "🟢" else "dn"
    return (f'<span class="bw-pill bw-pill-{cls}" title="{escape("；".join(title_bits))}">'
            f"{light} {peg_s}／{x_s}</span>")


def _bottom_cell_html(v: dict) -> str:
    """底部欄（VCP 深度 1，2026-09-18，見 notes/site-internal/root/
    _seat_engine_v5_1_20260918.md §3／knowledge/rule_ledger.md「VCP 深度 1」列，
    見 scripts/build_dd_screener.py::compute_vcp_tag()）：距新高 10% 以內才算，
    tooltip 放原始數字（分數／回檔段數／末段回檔%／量縮比／底部天數）。純顯示與
    ③等待池 🟡 組排序用，不改燈號或倉位——`_vcp_kind()` 是 ASCII 版
    `_bottom_ascii_cell()` 共用的同一份分類，兩邊不會分岔。"""
    kind = _vcp_kind(v)
    if kind == "far":
        return '<span class="bw-muted">—</span>'
    if kind == "insufficient":
        return ('<span class="bw-muted" title="日線不足 221 根，算不出 VCP">'
                '資料短</span>')
    score = v.get("vcp_score"); n = v.get("vcp_pullback_count")
    last_pb = v.get("vcp_last_pullback_pct"); vol = v.get("vcp_vol_dryup_ratio")
    age = v.get("vcp_base_age_days")
    n_disp = int(n) if isinstance(n, (int, float)) else "—"
    age_disp = int(age) if isinstance(age, (int, float)) else "—"
    title = (f"VCP 分數 {_num(score, 0)}｜回檔 {n_disp} 段｜末段回檔 {_num(last_pb, 1)}%｜"
             f"量縮比 {_num(vol, 2)}｜底部天數 {age_disp} 天")
    if kind in ("breakout_tight", "breakout_loose"):
        text = "緊縮後突破" if kind == "breakout_tight" else "鬆散突破"
        cls = "up" if kind == "breakout_tight" else "mut"
        return f'<span class="bw-pill bw-pill-{cls}" title="{escape(title)}">{text}</span>'
    pb_s = f"{last_pb:.1f}" if isinstance(last_pb, (int, float)) else "—"
    if kind == "tight":
        return f'<span title="{escape(title)}">緊 {n_disp}段·末段 −{pb_s}%</span>'
    if kind == "loose":
        return f'<span title="{escape(title)}">鬆 {n_disp}段</span>'
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


def _dd_pill(tag, moat=None) -> str:
    """DD 裁決標籤 pill；`moat`（2026-09-17 全母體看板欄位對齊）＝護城河評級字串
    （如 "A+↑"），有值時併入 title——護城河欄本身已從全母體表移除，改摺進本 pill
    的 tooltip，見 knowledge/rule_ledger.md 同名設計稿。"""
    title_bits = []
    if tag:
        title_bits.append(tag)
    if moat and moat != "—":
        title_bits.append(f"護城河 {moat}")
    title_attr = f' title="{escape("；".join(title_bits))}"' if title_bits else ""
    if not tag:
        return f'<span class="bw-pill bw-pill-mut"{title_attr}>—</span>'
    if "進場" in tag:
        cls = "up"
    elif "觀望" in tag:
        cls = "neu"
    elif "迴避" in tag:
        cls = "dn"
    else:
        cls = "mut"
    return f'<span class="bw-pill bw-pill-{cls}"{title_attr}>{escape(tag)}</span>'


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


def _flat_view(r: dict) -> dict:
    """巢狀列（row_dict() 輸出，universe_rows／core_seats／sat_seats／bench_seats 共用
    這個形狀）→ 扁平顯示列——arena.json own_board[] 的同一份 schema（2026-09-02 起
    既有欄位不變，供 build_pipeline_page.py／generate_list_forecasts.py／
    build_weekly_mail.py／docs/assets/imq-badge.js 既有讀法照舊）。

    2026-09-17（全母體看板欄位對齊，見 notes/site-internal/root/
    _seat_engine_v4_20260917.md 同名段）：新增 5 個純附加欄位（mom／
    durable_roic_5y_avg_pct／durable_qgm_pct／base_effect_detail／cycle_guard_detail）
    供 `_row_cells()`／`_seat_remark()` 共用渲染——只加不減、不改既有欄位語意，
    上述既有消費端不受影響。這個函式也是 `_seat_tr()`／全母體表列渲染的共用
    入口：席位表與全母體表的每一列都先經過 `_flat_view()` 正規化成同一份形狀，
    再交給 `_row_cells()` 畫，兩表因此不會分岔成兩份邏輯。"""
    g = r["grp"]; o = g.get("own") or {}; raw = o.get("raw") or {}
    return {"ticker": r["ticker"], "score": r["score"], "rank": r.get("rank"),
            "role": r.get("role"), "dd_age_days": r.get("dd_age_days"),   # dd_ascii() 用
            "g": g.get("g"), "g_method": r.get("g_method"),
            "ey": raw.get("ey"), "roic": r.get("roic"), "fcf": r.get("fcf"),
            "peg": r.get("peg"), "eps_rev_3m_pct": g.get("eps_rev_3m_pct"), "p_label": g.get("p_label"),
            # 財報錨定上修（2026-09-17）：實際用於排序/否決的值＋錨定方式/基準快照日/
            # 距下次財報天數，見 grp._revision_anchor()。
            "rev_used_pct": g.get("rev_used_pct"), "rev_anchor": g.get("rev_anchor"),
            "rev_baseline_date": g.get("rev_baseline_date"),
            "days_to_next_earnings": g.get("days_to_next_earnings"),
            "p_rev": o.get("p_rev"), "p_mom": o.get("p_mom"), "p_g": o.get("p_g"),
            "p_q": o.get("p_q"), "p_ey": o.get("p_ey"),
            "mom": raw.get("mom"),   # 2026-09-17 新增：12M 動能原始值（排名分 tooltip／12M 動能%欄共用）
            "overheated": g.get("overheated"), "peak": g.get("peak"),
            "high_short_interest": g.get("high_short_interest"),
            "short_interest_pct_float": g.get("short_interest_pct_float"),
            "valuation": g.get("valuation"),   # v5.1（2026-09-18）：估值閘，見 grp.valuation_gate()
            "base_effect": g.get("base_effect"), "base_effect_detail": g.get("base_effect_detail"),
            "cyclical": o.get("cyclical"), "cycle_guard": o.get("cycle_guard"),
            "cycle_guard_detail": o.get("cycle_guard_detail"),
            "insider_signal": r.get("insider_signal"), "insider_net_buy_3m": r.get("insider_net_buy_3m"),
            "durable_5y": r.get("durable_5y"), "durable_source": r.get("durable_source"),
            "durable_roic_5y_avg_pct": r.get("durable_roic_5y_avg_pct"),
            "durable_qgm_pct": r.get("durable_qgm_pct"),
            "lamp": r.get("lamp"), "action": r.get("action"),
            # v5（2026-09-17）：距歷史新高／implied_growth_pct，見 row_dict() 同名欄位註解。
            "dist_ath_pct": r.get("dist_ath_pct"), "ath_adj_price": r.get("ath_adj_price"),
            "ath_adj_date": r.get("ath_adj_date"), "ath_source": r.get("ath_source"),
            "implied_growth_pct": r.get("implied_growth_pct"),
            # VCP 深度 1（2026-09-18）：同 row_dict() 同名欄位註解，純顯示，不進燈號。
            "vcp_scope": r.get("vcp_scope"), "vcp_gate": r.get("vcp_gate"),
            "vcp_score": r.get("vcp_score"), "vcp_pullback_count": r.get("vcp_pullback_count"),
            "vcp_last_pullback_pct": r.get("vcp_last_pullback_pct"),
            "vcp_vol_dryup_ratio": r.get("vcp_vol_dryup_ratio"),
            "vcp_base_age_days": r.get("vcp_base_age_days"), "vcp_tight": r.get("vcp_tight"),
            "r26": r.get("r26"), "pass": g.get("pass"), "why": g.get("why"),
            "route": r["route"], "route_why": r.get("route_why"),
            "dd_tag": r.get("dd_tag"), "verdict": r.get("verdict"),
            "moat": r.get("moat"), "src": r.get("src"), "seat_note": r.get("seat_note"),
            "dd_path": r.get("dd_path")}


def _seat_remark(v: dict) -> str:
    """備註欄（chip 清單）——席位表與全母體表共用，讀 `_flat_view()`/own_board 的
    扁平 schema（2026-09-17 全母體看板欄位對齊，取代舊版直接讀巢狀 r["grp"]）。"""
    bits = []
    if v.get("peak"):
        bits.append(_chip_html("⚠ 頂點", "ROIC 高於五年平均 1.3 倍以上——純顯示，非下市訊號"))
    # v5（2026-09-17，見 grp.py 檔頭 v5 段）：過熱不再是排除核心候選的旗標（時機燈
    # 🟠 過熱本身已經是這個資訊的呈現）；融券高升級為整體資格閘排除，凡是會出現在
    # 池／席位表的列，high_short_interest 必為 False（不可能出現在這裡），故兩個
    # chip 一併移除，不留死判斷式。
    if v.get("base_effect"):
        d = v.get("base_effect_detail") or {}
        bits.append(_chip_html("基期", f'FY1→FY2 跳 +{d.get("fy1_fy2_pct", "—")}%，'
                                      f'FY2→FY3 只 +{d.get("fy2_fy3_pct", "—")}%，成長改用 FY2→FY3'))
    if v.get("cycle_guard"):
        cd = v.get("cycle_guard_detail") or {}
        bits.append(_chip_html("循環守門", f'毛利跨距 {cd.get("gm_swing_pp", "—")}pp／資本支出佔營收 '
                                         f'{cd.get("capex_pct_rev", "—")}%／PEG {cd.get("peg", "—")}'
                                         '——成長與盈餘殖利率分位封頂 50'))
    elif v.get("cyclical"):
        bits.append(_chip_html("循環", "毛利率跨距 >20pp 或資本支出佔營收 >15%——純顯示，未觸發守門"))
    if v.get("insider_signal") == "買":
        insT = v.get("insider_net_buy_3m")
        insT = f"{insT:+,.0f} 股" if isinstance(insT, (int, float)) else "—"
        bits.append(_chip_html("內部人買", f"近 3 個月內部人淨買超 {insT}——僅供備註，不進資格與排序"))
    elif v.get("insider_signal") == "賣":
        insT = v.get("insider_net_buy_3m")
        insT = f"{insT:+,.0f} 股" if isinstance(insT, (int, float)) else "—"
        bits.append(_chip_html("內部人賣", f"近 3 個月內部人淨賣超 {insT}——僅供備註，不進資格與排序"))
    if v.get("seat_note"):
        bits.append(escape(v["seat_note"]))
    if v.get("route_why"):
        bits.append(f'<span class="bw-muted">{escape(v["route_why"])}</span>')
    return "".join(bits) or '<span class="bw-muted">—</span>'


def _shared_thead_cells() -> list[str]:
    """代號…備註 10 個共用 <th>——席位表（_seat_section_html／池表）與全母體表
    （render_board_html）逐字共用，避免兩表的表頭文字各寫一份而日後漂移。
    v5（2026-09-17，見 grp.py 檔頭 v5 段）：欄序改為代號／上修%（財報後）／
    距歷史新高%／下次財報／耐久／時機／倉位／DD／備註——移除 v4 的「排名分」
    （own_score 五百分位，v5 起降為本欄 tooltip 的「v4 對照」，不再單獨佔欄）與
    「12M 動能%」欄（v5 排序不再用價格動能，動能只留在時機燈 hover）。
    v5.1（2026-09-18，見 grp.py 檔頭 v5.1 段／grp.valuation_gate()）：耐久之後、
    時機之前插入「估值」欄——10 個共用欄，_board_tr() 的席欄插入點跟著往後挪一位。
    VCP 深度 1（2026-09-18，見 notes/site-internal/root/_seat_engine_v5_1_20260918.md
    §3）：DD 之後、備註之前插入「底部」欄——11 個共用欄，插在 _board_tr() 席欄
    插入點（index 8）之後，不需要跟著挪動任何既有 index（見該函式註解）。"""
    return [
        '<th class="bw-l">代號</th>',
        '<th title="v5 排序鍵：以該股自己最近一次財報日前最新月度 snapshot 為基準的 '
        'FY 加權 EPS 上修（已排除匯率），缺財報錨定時退回近三個月；池內依此欄降冪排序，'
        '同值 tie-break implied_growth_pct、再 tie-break 盈餘殖利率。hover 另列基準快照日、'
        '錨定方式、v4 對照排名分（五百分位平均，僅供對照，v5 不用於排序）">上修%（財報後）</th>',
        '<th title="距離還原權息全歷史最高收盤價（yfinance history period=max，非 52 週高）；'
        '負值＝現價低於史上最高。板機：站上此欄 ≥−3% 且站上 200 日線＝突破帶（時機燈綠燈）">距歷史新高%</th>',
        '<th class="bw-l" title="距下次財報天數；<=7 天標記——分數為財報前快照">下次財報</th>',
        '<th class="bw-l" title="池資格：QGM 五年 ROIC 穩定度 ≥75%，或 Koyfin 五年平均∧'
        '三年平均∧現值三者皆 ≥15%——一致性判準，非單一數字">耐久</th>',
        '<th class="bw-l" title="v5.1 估值閘：PEG（現價重算 live_peg 優先，缺則 Koyfin peg）'
        '&gt;2.0，或 PE NTM 相對五年均倍數 &gt;1.5x，任一則紅——紅燈整體排除、不進池'
        '（入池／月頻換席資格閘，非月中硬否決）。兩者皆缺不算否決，標 ⚪ 缺值。'
        '顯示「PEG／PE 相對五年均倍數」">估值</th>',
        '<th class="bw-l">時機</th>',
        '<th class="bw-l">倉位</th>',
        '<th class="bw-l" title="個股報告的裁決標籤，僅供顯示，不影響席位／排序；'
        '護城河評級摺入本欄 hover；⚠過期＝逾 180 天">DD</th>',
        '<th class="bw-l" title="VCP（回檔一次比一次小、量縮、離底部高點近）——只在'
        '距歷史新高 10% 以內算，只排③等待池 🟡 組序、標🟢/🟠突破措辭，不改燈號或倉位。'
        '緊 n段＝過閘、鬆 n段＝未過、資料短＝日線不足、—＝距新高超過 10% 未算">底部</th>',
        '<th class="bw-l">備註</th>',
    ]


def _row_cells(v: dict, lamp_map: dict) -> list[str]:
    """代號…備註 10 個共用 <td>——席位表（_seat_tr）與全母體表（_board_tr）共用同一份
    渲染，見兩處呼叫端。輸入 `v` 是 `_flat_view()`（或 arena.json own_board[] 原生）
    產出的扁平列。v5（2026-09-17，見 grp.py 檔頭 v5 段）：移除排名分／12M 動能%
    兩欄，新增距歷史新高%；v4 對照排名分與階段/RS 降為 tooltip 專屬資訊。v5.1
    （2026-09-18）：新增估值欄（見 _val_cell_html()）。VCP 深度 1（2026-09-18）：
    DD 欄之後新增底部欄（見 _bottom_cell_html()）。"""
    tk = v["ticker"]
    # 財報錨定上修（2026-09-17）＋ v5 對照（2026-09-17）：上修欄 tooltip 併入基準快照日、
    # 錨定方式（財報／日曆）與 v4 對照排名分（own_score_v4 五百分位平均，僅供對照）。
    rev_anchor_txt = {"earnings": "財報後", "calendar_3m": "日曆三個月（缺財報錨定）"}.get(
        v.get("rev_anchor"), "—")
    rev_title = (f"錨定：{rev_anchor_txt}｜基準快照 {v.get('rev_baseline_date') or '—'}｜"
                 f"v4 對照排名分（僅供對照，v5 不用於排序）：{_num(v.get('score'), 1)}｜"
                 f"implied_growth {_num(v.get('implied_growth_pct'), 1)}%｜"
                 f"EY {_num(v.get('ey'), 1)}%（tie-break 順序：上修→implied_growth→EY）")
    durable_bits = []
    if v.get("durable_roic_5y_avg_pct") is not None:
        durable_bits.append(f"五年 ROIC 平均 {v['durable_roic_5y_avg_pct']:.1f}%")
    if v.get("durable_qgm_pct") is not None:
        durable_bits.append(f"QGM 五年穩定度 {v['durable_qgm_pct']:.1f}%")
    durable_cell = (f'<span title="{escape("；".join(durable_bits) or "耐久資料不足")}">'
                    f'{"✓" if v.get("durable_5y") else "—"}</span>')
    days_ne = v.get("days_to_next_earnings")
    if days_ne is None:
        next_earn_cell = '<span class="bw-muted">—</span>'
    elif 0 <= days_ne <= 7:
        next_earn_cell = (f'<span class="bw-pill bw-pill-warn" '
                          f'title="距下次財報 {int(days_ne)} 天——分數為財報前快照">{int(days_ne)} 天</span>')
    else:
        next_earn_cell = f"{int(days_ne)} 天"
    lamp = v.get("lamp") or {}
    stage_txt = STAGE_LABEL.get(lamp_map.get(tk), "無資料")
    ath_bits = []
    if v.get("ath_adj_price") is not None:
        ath_bits.append(f"還原新高 {v['ath_adj_price']:.2f}"
                        + (f"（{v['ath_adj_date']}）" if v.get("ath_adj_date") else ""))
    if v.get("ath_source") == "5y":
        ath_bits.append("5 年高代理（全歷史查詢失敗）")
    dist_ath_title = "｜".join(ath_bits) or "資料缺"
    lamp_title = (f'{lamp.get("why", "")}｜階段：{stage_txt}（RS／階段僅供參考，不影響燈號）'
                 + (f'｜板機：{lamp["trigger"]}' if lamp.get("trigger") else ""))
    lamp_cell = f'<span class="bw-pill" title="{escape(lamp_title)}">{escape(lamp.get("label", "—"))}</span>'
    return [
        f'<td class="bw-l"><strong>{_tk_link(v)}</strong></td>',
        f'<td title="{escape(rev_title)}">{_num(v.get("rev_used_pct"), 1)}</td>',
        f'<td title="{escape(dist_ath_title)}">{_num(v.get("dist_ath_pct"), 1)}</td>',
        f'<td class="bw-l">{next_earn_cell}</td>',
        f'<td class="bw-l">{durable_cell}</td>',
        f'<td class="bw-l">{_val_cell_html(v.get("valuation"))}</td>',
        f'<td class="bw-l">{lamp_cell}</td>',
        f'<td class="bw-l">{escape(v.get("action") or "—")}</td>',
        f'<td class="bw-l">{_dd_pill(v.get("dd_tag"), v.get("moat"))}</td>',
        f'<td class="bw-l">{_bottom_cell_html(v)}</td>',
        f'<td class="bw-note">{_seat_remark(v)}</td>',
    ]


def _seat_tr(r: dict, code: str, lamp_map: dict, muted: bool = False) -> str:
    v = _flat_view(r)
    cls = ' class="bw-muted-row"' if muted else ""
    return (f'<tr{cls}><td class="bw-l">{escape(code)}</td>' + "".join(_row_cells(v, lamp_map))
            + "</tr>")


def _board_tr(v: dict, idx: int, seat_code: str | None, lamp_map: dict) -> str:
    """全母體表單列——# 排序名次 ＋ 11 個共用欄 ＋ 席（目前坐哪一席，未坐席留白）。
    `seat_code` 是 "C1"/"S2" 這類字串（與席位表自己的席次代碼同一套詞彙）或 None。
    v5（2026-09-17）：共用欄從 10 個減為 9 個（見 _shared_thead_cells()），席欄插入點
    跟著從 index 8 移到 index 7（倉位／DD 之間，語意不變：插在「倉位」欄之後）。
    v5.1（2026-09-18）：新增估值欄使共用欄變回 10 個，席欄插入點跟著從 index 7
    移到 index 8（估值欄插在耐久之後、倉位之前，不影響「插在倉位欄之後」的語意）。
    VCP 深度 1（2026-09-18）：新增底部欄使共用欄變 11 個，但插在 DD 之後、備註
    之前——晚於席欄插入點（index 8），故 `cells[:8]`／`cells[8:]` 兩段切法不用改，
    `cells[8:]` 現在多帶一個底部欄，順序自然是 DD／底部／備註。"""
    cells = _row_cells(v, lamp_map)
    seat_cell = (f'<td class="bw-l">{escape(seat_code)}</td>' if seat_code
                else '<td class="bw-l"><span class="bw-muted">—</span></td>')
    cls = ' class="bw-seated"' if seat_code else ""
    return (f'<tr{cls}><td>{idx}</td>' + "".join(cells[:8]) + seat_cell + "".join(cells[8:])
            + "</tr>")


def _pool_table_html(rows_list: list, lamp_map: dict, seat_prefix: str | None = None) -> str:
    """一張池表（① 核心席／② 可買／③ 等待池／④ 收合皆共用）：`seat_prefix` 給定
    （如 "C"）時第一欄是席次代碼 C1..；否則是池內排序名次 1.."""
    if not rows_list:
        return '<div class="bw-note-line">（無）</div>'
    thead = ('<tr><th class="bw-l">' + ("席" if seat_prefix else "#") + "</th>"
             + "".join(_shared_thead_cells()) + "</tr>")
    body = [_seat_tr(r, f"{seat_prefix}{i}" if seat_prefix else str(i), lamp_map)
            for i, r in enumerate(rows_list, 1)]
    return ('<div class="bw-scroll"><table><thead>' + thead + "</thead><tbody>"
            + "".join(body) + "</tbody></table></div>")


def _pool_section_html(core_seats, buyable, waiting_rest, prev_snap, rows, lamp_map,
                       lamp_as_of=None, last_rotation_date=None) -> str:
    """v5『① 核心席（5）／② 可買／③ 等待池』HTML 區塊（h3＋sub＋表＋legend＋DOWN
    變動列）——取代 v4「核心5＋衛星5＋候補5」，見 grp.py 檔頭 v5 段／
    knowledge/rule_ledger.md「v5 席位引擎」列。核心＝池前 5（月頻輪動，硬否決立即
    下席、空位由池遞補）；可買＝等待池中時機燈綠/橘者；等待池＝其餘池成員。"""
    seat_label = {r["ticker"]: f"核心 {i}" for i, r in enumerate(core_seats, 1)}
    prev_seats = {t: "核心席" for t in prev_snap.get("core", [])}

    core_tbl = _pool_table_html(core_seats, lamp_map, seat_prefix="C")
    buyable_tbl = _pool_table_html(buyable, lamp_map)
    waiting_yellow, waiting_red, waiting_gray = _group_waiting_pool_by_timing(waiting_rest)
    if not waiting_rest:
        waiting_tbl = '<div class="bw-note-line">（無）</div>'
    else:
        waiting_parts = []
        for label, group in ((_WAIT_GROUP_LABELS[0][0], waiting_yellow),
                             (_WAIT_GROUP_LABELS[1][0], waiting_red),
                             (_WAIT_GROUP_LABELS[2][0], waiting_gray)):
            if not group:
                continue
            waiting_parts.append(
                f'<div class="bw-sub" style="margin-top:10px"><b>{escape(label)}</b>'
                f'（{len(group)} 檔）</div>' + _pool_table_html(group, lamp_map))
        waiting_tbl = "".join(waiting_parts)

    legend = f"""<details class="bw-fold" open><summary>怎麼讀這張表（下方「全母體看板」共用本段說明）</summary>
<div class="bw-note-line"><b>三關一燈</b>：第一關看公司夠不夠好（資格），第二關看分析師有沒有在財報後上修（排序），第三關看股價離歷史新高多遠（時機燈，決定倉位）。核心 5 席每月換一次，其餘每天重算。這是研究名單，不是帳戶持倉。</div>
<div class="bw-note-line"><b>第一關 資格</b>：市值 200 億美元以上、品質閘、三年成長 15%（耐久達標者 10%）、站上 52 週線、耐久一致性。五項全過才有資格。另外六種情況直接出局：體質拒絕、衰退 ⛔、DD 迴避、融券占流通股比 &gt;10%、財報後上修低於 −5%（缺財報錨定時退回三個月）、估值閘紅燈（PEG &gt;2.0 或 PE 相對五年均倍數 &gt;1.5x，任一則紅；兩者皆缺不算否決，標 ⚪ 缺值）。不設產業上限。</div>
<div class="bw-note-line"><b>耐久</b>：兩種算法擇一達標即可。QGM 五年 ROIC 穩定度 ≥75%；或 Koyfin 五年平均、三年平均、現值三者都 ≥15%。看的是一致性，不是單一年份。不耐久就不進池，v5 沒有衛星席可退。</div>
<div class="bw-note-line"><b>第二關 排序</b>：只看財報後上修幅度。基準是該股最近一次財報日前的月度快照，缺財報錨定時退回三個月。上修 ≥5% 才入池，池內依上修由高到低排。同值先比 implied_growth_pct，再比盈餘殖利率。不看股價漲幅。own_score_v4 五百分位對照分只在「上修%（財報後）」欄 hover 顯示，不參與排序。</div>
<div class="bw-note-line"><b>第三關 時機燈</b>：量的是距還原權息全歷史最高收盤價多遠，燈號直接對應倉位。🟢 可進＝距新高 3% 以內且站上 200 日線，正常倉／🟡 半倉＝差 3%~10%／🟠 過熱＝12-1 月動能 &gt;150% 但仍在突破帶附近，半倉／🔴 等板機＝差超過 10% 或跌破 200 日線，零倉／⚫ 不合格＝未站上 52 週線。過熱與頂點不擋資格，只影響燈號。RS 與生命週期階段只在 hover 顯示，不影響燈號。時機燈與倉位每日更新，不用等月頻換席。</div>
<div class="bw-note-line"><b>席次怎麼分</b>：核心＝池內前 5，每月第一次排程整批重選一次；月中只有硬否決能換人，空位由池遞補。沒進核心的池成員全部叫等待池，依燈號分兩組：②可買＝今天綠燈或橘燈，板機已亮；③等待池＝其餘，再分 🟡 接近新高（組內先看底部緊不緊，再依上修排序）／🔴 拉回中／⚫ 資料缺（這兩組依上修排序），衛星席已取消。</div>
<div class="bw-note-line"><b>底部緊度</b>：量的是股價回檔的樣子。回檔一次比一次小、量縮、離底部最高點近，都算緊，否則算鬆，只在距歷史新高 10% 以內的名字才算。只用來排③等待池裡 🟡 組的順序，緊的排前面；🟢／🟠 兩種燈號改標「緊縮後突破」或「鬆散突破」。不改燈號，也不改倉位。</div>
<div class="bw-note-line"><b>DD</b>：個股報告的裁決標籤只是顯示，不影響席位與排序。有護城河評級時併入本欄 hover。</div>
<div class="bw-note-line"><b>備註欄</b>：以下都只是顯示，不進資格與排序。⚠ 頂點＝ROIC 高於五年平均 1.3 倍；基期＝三年 CAGR 因 FY1→FY2 低基期跳增，改用 FY2→FY3 成長率；循環守門＝循環股（毛利率跨距大或資本支出佔營收高）且 PEG 低到可疑；循環＝循環股但未觸發守門；財報前＝距下次財報 ≤7 天；內部人買／內部人賣＝近 3 個月內部人淨買賣方向；新席／現任／遞補＝本期席位異動狀態。</div>
<div class="bw-note-line"><b>怎麼用</b>：核心或②可買＝現在可以買。③等待池＝上修夠強但還沒突破，等板機。</div>
</details>"""

    gone = [t for t in prev_seats if t not in seat_label]
    if gone:
        why_map = {r["ticker"]: r for r in rows}
        lines = []
        for t in gone:
            r = why_map.get(t)
            why = (((r or {}).get("grp") or {}).get("why") or [])
            chips = _chips_from_why(why, limit=2) if why else []
            reason = _chips_html(chips) if chips else '<span class="bw-muted">上修排序被擠出前 5，或已不在母體</span>'
            lines.append(f'<div class="bw-note-line">🔻 DOWN <b>{escape(t)}</b>：{reason}</div>')
        changes_html = "".join(lines)
    else:
        changes_html = '<div class="bw-note-line">本期無下席變動。</div>'

    freshness = (f'<div class="bw-note-line">時機更新：{escape(lamp_as_of or "—")}（每日）／'
                f'席位更新：{escape(last_rotation_date or "—")}（每月換席）</div>'
                if (lamp_as_of or last_rotation_date) else "")

    return ('<h3 class="bw-sec">① 核心席（5）</h3>'
           + '<div class="bw-sub">池前 5，月頻輪動；硬否決立即下席，空位由池遞補。</div>'
           + freshness + core_tbl + legend + changes_html
           + f'<h3 class="bw-sec">② 可買（{len(buyable)} 檔）</h3>'
           + '<div class="bw-sub">等待池中時機燈綠/橘者——今天板機亮的，可能是空清單。</div>'
           + buyable_tbl
           + f'<h3 class="bw-sec">③ 等待池（{len(waiting_rest)} 檔）</h3>'
           + '<div class="bw-sub">上修強、還沒突破——池中扣掉核心與②可買後的其餘名字，'
             '依時機燈分組（🟡接近新高／🔴拉回中／⚫資料缺），組內依上修排序。</div>'
           + waiting_tbl)


def _collapsed_section_html(not_in_pool_rows: list, lamp_map: dict) -> str:
    """v5『④ 品質過閘、上修未達 5%』收合區塊——資格全過但財報後上修未達 +5%，不進池，
    僅供人工複審，見 grp.py 檔頭 v5 段第 4 點。"""
    return (f'<details class="bw-fold"><summary>④ 品質過閘、上修未達 5%'
            f'（{len(not_in_pool_rows)} 檔，點開複審）</summary>'
           + '<div class="bw-sub">資格全過（品質×三年成長×站上 52 週線×耐久）但財報後上修未達 +5%，'
             '不進池、不佔核心席，僅供人工複審；依上修排序，補上更新的財報或修正即可能進池。</div>'
           + _pool_table_html(not_in_pool_rows, lamp_map) + '</details>')


def _own_board_section_html(views: list[dict], seat_code_map: dict, lamp_map: dict) -> str:
    """『全母體看板（v4 對照排序）』h3＋說明＋表格——render_board_html() 用；`views`
    需已依 score（v4 五百分位對照分，僅供對照，見 grp.py 檔頭 v5 段第 3 點）降冪
    排序、至多 40 列；`seat_code_map`＝{ticker: "C1"/"S2"}。v5（2026-09-17）：席欄
    插入點從 index 8 移到 index 7，見 _board_tr() 註解。v5.1（2026-09-18）：估值欄
    插入使共用欄變回 10 個，席欄插入點跟著移到 index 8（同 _board_tr()）。VCP 深度 1
    （2026-09-18）：底部欄插在 DD 之後（晚於席欄插入點），共用欄變 11 個但
    `thead_cells[:8]`／`thead_cells[8:]` 切法不變（同 _board_tr() 註解）。"""
    thead_cells = _shared_thead_cells()
    thead = ('<tr><th title="排序名次（v4 對照分降冪，僅供對照——池的實際排序見上方表格）">#</th>'
             + "".join(thead_cells[:8])
             + '<th class="bw-l" title="目前坐核心席次；空白＝未坐席">席</th>'
             + "".join(thead_cells[8:]) + "</tr>")
    body_rows = [_board_tr(v, i, seat_code_map.get(v["ticker"]), lamp_map) for i, v in enumerate(views, 1)]
    main_tbl = ('<div class="bw-scroll"><table><thead>' + thead + "</thead><tbody>"
                + "".join(body_rows) + "</tbody></table></div>")
    return ('<h3 class="bw-sec">全母體看板（v4 對照排序）</h3>'
           + '<div class="bw-sub">v4 對照排名分（五百分位平均：上修／12M 動能／成長／品質／盈餘殖利率，'
             '僅供對照，不是 v5 池的排序鍵）攤平到全母體，只多一欄「席」；欄位定義見上方「怎麼讀這張表」，'
             '不重覆說明。核心席是從上方②③表格（池，依上修排序）取前 5，不是從這張表挑的'
             '<span class="stage-lamp-asof"></span>。</div>'
           + main_tbl)


def render_board_html(as_of, rows, core_seats, buyable, waiting_rest, not_in_pool_rows, prev_snap,
                      entered, lamp_map, rev_data_as_of=None, price_as_of=None,
                      lamp_as_of=None, last_rotation_date=None) -> str:
    """HTML TABLE 版看板 v5（2026-09-17，見 grp.py 檔頭 v5 段／knowledge/rule_ledger.md
    「v5 席位引擎」列，取代 v4「核心5＋衛星5＋候補5」）。回傳裸片段（無 html/head/body），
    可直接 innerHTML 或接進另一頁 <body>。內容與 render_board_text 同源同排序，只是
    呈現層換成表格＋燈號＋chip。

    `rev_data_as_of`／`price_as_of`：頁首分開標「上修資料（Koyfin xlsx）」與
    「價格/距新高/時機燈」兩個日期，見 render_board_text() docstring 同名段。
    `lamp_as_of`／`last_rotation_date`：轉交 _pool_section_html() 渲染成「① 核心席」
    區塊的兩行新鮮度戳記。"""
    # 席次代碼（C1-C5）——與「① 核心席」表自己的席次代碼同一套詞彙，供全母體表
    # 「席」欄顯示。
    seat_code_map = {r["ticker"]: f"C{i}" for i, r in enumerate(core_seats, 1)}

    # v4 對照：全母體看板仍用 own_score_v4 名次排序，只做對照，不影響 ①②③ 的池排序
    # （後者用 grp.pool_sort_key()，見呼叫端 main()）。
    rows_ranked = sorted((r for r in rows if r["grp"].get("pass")), key=lambda r: -(r["score"] or 0))
    own = rows_ranked[:40]
    own_section = _own_board_section_html([_flat_view(r) for r in own], seat_code_map, lamp_map)

    pool_section = _pool_section_html(core_seats, buyable, waiting_rest, prev_snap, rows, lamp_map,
                                      lamp_as_of, last_rotation_date)
    collapsed_section = _collapsed_section_html(not_in_pool_rows, lamp_map)

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
        # 2026-09-17（全母體看板欄位對齊）：欄名同步改叫「排名分」——與席位表／全母體
        # 表指的是同一個 own_score 數字，避免同頁面兩個名字誤讀成兩種分數；表格結構
        # 本身（含尚未過三年成長閘、故用單年成長率）不變。
        q_thead = ('<tr><th class="bw-l">Ticker</th><th>排名分</th>'
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

    freshness_bits = []
    if rev_data_as_of:
        freshness_bits.append(f"上修資料（Koyfin xlsx）as_of {rev_data_as_of}")
    if price_as_of:
        freshness_bits.append(f"價格/距新高/時機燈 as_of {price_as_of}")
    freshness_line = " · ".join(freshness_bits)
    head_line = (f"選股看板 v5 · as_of {as_of}" + (f" · {freshness_line}" if freshness_line else "")
                + f" · 母體 {len(rows)}（美股含 ADR；台股另建）")
    rule_line = ("同一套三關一燈。先過資格：市值 200 億以上、品質閘、三年成長、站上 52 週線、"
                 "耐久一致性。再依財報後上修排序，上修 ≥5% 入池。最後由時機燈決定倉位。"
                 "體質拒絕、衰退 ⛔、DD 迴避、融券占流通股比 >10%、財報後上修低於 −5%、"
                 "估值閘紅燈（PEG >2.0 或 PE 相對五年均倍數 >1.5x，兩者皆缺不算否決）都整體排除。"
                 "核心＝池前 5，每月換一次；其餘為等待池。不設產業上限；內部人買賣只是備註。"
                 "細節見上方「怎麼讀這張表」。")
    timing_note = ("過熱（12-1 月動能 >150%）與頂點不擋資格，只影響時機燈（🟠 半倉）或純顯示。"
                   "時機燈與倉位每日跟著 dd-screener 資料重算，不進排序。")

    return (
        '<div class="board-wrap">' + _BOARD_CSS
        + f'<div class="bw-head">{escape(head_line)}</div>'
        + f'<div class="bw-rule">{escape(rule_line)}</div>'
        + f'<div class="bw-rule">{escape(timing_note)}</div>'
        + pool_section
        + collapsed_section
        + own_section
        + '<h3 class="bw-sec">DD 進場 vs 機械資格</h3>'
        + f'<div class="bw-sub">{escape(dd_gate_sub)}——過閘者已在池或核心席中，這裡只列未過者供人工複審。</div>'
        + ng_tbl
        + '<h3 class="bw-sec">可選但先不入席：缺三年成長預估（加進 Koyfin 名單即可）</h3>'
        + '<div class="bw-sub">這些名字三閘都過，但成長只有單年預估（yfinance FY1→FY2，非 Koyfin FY1→FY3 CAGR），'
          '所以只列隊、不佔席、不計輪動。加進 Koyfin watchlist 補上三年成長率，下次 build 就會脫隊、'
          '以三年成長率重新競爭池排序（不需要先有 DD）。</div>'
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


def select_fresh_roster_v5(pool_ranked: list, core_slots: int = CORE_SLOTS) -> list:
    """v5 整批重選（pure，2026-09-17，見 grp.py 檔頭 v5 段第 3-4 點／
    knowledge/rule_ledger.md「v5 席位引擎」列）：`pool_ranked` 為池（資格閘全過 ∧
    耐久達標 ∧ 財報後上修 ≥5%）依 grp.pool_sort_key() 排序後的列表——池本身已經是
    全部資格檻，沒有 v4「core_candidate」那道濾網，池內名次就是唯一判準。回傳前
    `core_slots` 名的 ticker 清單。無產業/主題集中度上限（2026-09-17 持有人拍板，
    v4 已拍板、v5 沿用不變）。"""
    return [r["ticker"] for r in pool_ranked[:core_slots]]


def hard_veto_v5(r: dict, w52_fail_streak: int = 0) -> str | None:
    """v5 硬否決判定（pure，2026-09-17，見 grp.py 檔頭 v5 段）——回傳觸發理由，或
    None（未觸發）。七個條件之一（v4 六個 + 融券高，見下）：DD 迴避／體質拒絕／
    衰退 ⛔／上修達 5%（財報後錨定，缺值退回三個月）／融券占流通股比 >10%（v5 新增
    ——升級為整體資格閘排除後，現任核心席若融券轉高也該立即下席，見 grp_score()
    的 veto_high_short_interest）——皆已在 grp_score 算成 grp["veto_*"] 細項；
    市值不足（r["cap_ok"]，apply_cap() 算好）；連續 `w52_fail_streak` 次週跑站不上
    52 週線（跨次跑狀態，呼叫端從 ledger 讀，見 W52_FAIL_STREAK_VETO）。只用在
    「月中沿用現任核心席」的路徑——整批重選（select_fresh_roster_v5）不需要這個。
    耐久／成長／品質三道軟性資格閘掉出門檻不在此列，維持 v4 以來的容忍度（月頻
    輪動的重點就是不因單週/單月雜訊洗掉席位，只有這七個硬否決才立即下席）。

    刻意不包含 `g["veto_valuation"]`（v5.1，2026-09-18 持有人拍板，見 grp.py
    valuation_gate()／rule_ledger.md「v5.1 估值閘」列）：估值閘是入池／月頻換席
    的資格閘，owner 明確拍板它「不是月中硬否決」——核心席不因估值轉紅在月中被踢，
    要等下一次月頻整批重選（select_fresh_roster_v5）才會反映。七個條件維持不動。"""
    g = r.get("grp") or {}
    if g.get("veto_dd_avoid"):
        return "DD 迴避"
    if g.get("veto_quality_reject"):
        return "體質拒絕"
    if g.get("veto_decline"):
        return "衰退 ⛔"
    if g.get("veto_revision"):
        return "財報後上修 ≤ −5" if g.get("rev_anchor") == "earnings" else "三月上修 ≤ −5"
    if g.get("veto_high_short_interest"):
        return "融券占流通股比 >10%"
    if not r.get("cap_ok", True):
        return "市值不足"
    if w52_fail_streak >= W52_FAIL_STREAK_VETO:
        return "連續兩週跌破 52 週線"
    return None


def rotate_roster(current_month: str, last_rotation_month, prev_core_roster, pool_ranked: list,
                  w52_fail_streaks: dict | None = None,
                  core_slots: int = CORE_SLOTS,
                  all_by_ticker: dict | None = None) -> dict:
    """v5 月頻輪動主體（pure，2026-09-17，見 grp.py 檔頭 v5 段第 3 點／
    knowledge/rule_ledger.md「v5 席位引擎」列）——只管核心席；等待池（②可買／
    ③等待池）沒有衛星軌需要跨次跑持續追蹤的狀態，每次呼叫端直接從當次 `pool_ranked`
    扣掉核心即得，見 main()。
      - 本月第一次跑（last_rotation_month != current_month，或無 prev_core_roster）
        → 整批重選（select_fresh_roster_v5），rotated=True。
      - 同月內的後續跑（包含 `--daily`／`--lamp-only` 每日重跑，見檔頭 --daily 段）
        → 沿用 prev_core_roster；任何現任核心席命中 hard_veto_v5() 立即移除，空位
        由 `pool_ranked` 中尚未入席的下一名遞補；找不到人可補則留空。

    重要：現任席的沿用檢查查的是 `all_by_ticker`（全母體，含資格閘未過者），不是
    `pool_ranked`（只含池內、已排名者）——月中軟性資格失守（成長掉出門檻、品質閘
    未過、耐久跌出門檻等）不該立刻下席，只有 hard_veto_v5() 認定的七個硬否決才
    下席，這正是月頻輪動要給的「不因單週/單月雜訊洗掉席位」的容忍度。
    `all_by_ticker` 未提供時 fallback 用 `pool_ranked` 建索引（相容舊呼叫，但退化
    成「掉出池即視同跌出母體」，僅供測試用；正式呼叫請務必傳全母體）。
    回傳 {"core":[...], "rotated": bool, "removed":[(ticker,why),...],
    "filled":[(track,ticker),...]}（ticker 清單，不是列物件；`filled` 的 track 恆為
    "core"，欄位保留是為了與 v4 帳本格式相容、不必改 build_arena.py 其餘讀法）。"""
    w52_fail_streaks = w52_fail_streaks or {}
    universe_by_ticker = all_by_ticker if all_by_ticker is not None else {r["ticker"]: r for r in pool_ranked}

    if prev_core_roster is None or last_rotation_month != current_month:
        core = select_fresh_roster_v5(pool_ranked, core_slots)
        return {"core": core, "rotated": True, "removed": [], "filled": []}

    removed: list = []
    kept: list = []
    for t in prev_core_roster or []:
        r = universe_by_ticker.get(t)
        if r is None:
            removed.append((t, "跌出母體（下市或資料消失）"))
            continue
        why = hard_veto_v5(r, w52_fail_streaks.get(t, 0))
        if why:
            removed.append((t, why))
            continue
        kept.append(t)   # 沿用——即便本次未過全部資格閘，非硬否決不下席
    removed_tickers = {t for t, _why in removed}
    filled: list = []

    # 剛被硬否決下席的名字本回合不得遞補回自己的空位——即便它仍在 pool_ranked 裡
    # （例如 w52 連續兩週否決，資格本身其餘條件都還過），見
    # test_rotate_roster_w52_streak_evicts_after_two_consecutive_runs。
    seated = set(kept) | removed_tickers
    for r in pool_ranked:
        if len(kept) >= core_slots:
            break
        if r["ticker"] in seated:
            continue
        kept.append(r["ticker"])
        seated.add(r["ticker"])
        filled.append(("core", r["ticker"]))

    return {"core": kept, "rotated": False, "removed": removed, "filled": filled}


def _find_last_rotation_date(snapshots: list[dict]) -> str | None:
    """帳本 snapshots 中最近一筆 rotated=True 的日期——供席位表『席位更新：』顯示用。"""
    return next((sn.get("date") for sn in reversed(snapshots or []) if sn.get("rotated")), None)




def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", action="store_true",
                         help="寫入 arena-ledger.json（last_rotation_month／roster.core／snapshots，"
                              "月頻輪動時鐘前進）；僅 weekly-engine.yml 排程使用，手動跑不帶此旗標＝帳本唯讀")
    parser.add_argument("--daily", action="store_true",
                         help="daily-taipei-morning.yml 用：全量重跑資格/池/排序/時機燈/距歷史新高，"
                              "但不寫 arena-ledger.json——核心席名單仍從帳本 roster.core 讀（月頻輪動不變），"
                              "現任核心席若命中硬否決本次即被替換顯示（下次 --ledger 排程跑次才真正落帳）。"
                              "見 grp.py 檔頭 v5 段第 3-5 點。")
    parser.add_argument("--lamp-only", action="store_true",
                         help="v4 舊名，向下相容別名——語意等同 --daily（v5 起沒有窄流程的『只刷時機燈』，"
                              "資格/池/排序本來就便宜到可以每天全量重算，見 --daily 說明）")
    args = parser.parse_args()
    # --daily／--lamp-only 只是「不寫帳本」這件事的明講旗標——不帶 --ledger 的預設路徑
    # 本來就已經是「全量重算、帳本唯讀」，兩個旗標存在只為了讓 workflow 檔的意圖讀起來
    # 明確，並保留 v4 時代 --lamp-only 呼叫端字面相容，不觸發任何額外分支。
    if args.daily or args.lamp_only:
        print("daily 模式：全量重跑資格/池/排序/時機燈，帳本唯讀（核心席名單仍取自 roster.core）。")
    stocks = json.loads(DD_LATEST.read_text(encoding="utf-8"))["stocks"]
    # latest.json 若以 --include-non-dd 產出，無 DD 列（dd_status="none"）改由 load_qgm_rows 供給
    #（帶 _src／_durable_5y／_mktcap），這裡先排除以免搶走 QGM 列的身份標記
    # 2026-09-16：丟掉前先留一份給 load_qgm_rows 補三年 CAGR（見該函式 docstring）
    latest_none = {s["ticker"]: s for s in stocks if s.get("dd_status") == "none"}
    # 2026-09-18（v5.1 母體擴充，notes/site-internal/root/_seat_engine_v5_1_20260918.md
    # §2）：universe_source=="largecap-koyfin" 列是 dd-screener 直接供給的第三母體
    # 來源（不是 QGM 品質池），不比照上面 QGM 供給列改走 load_qgm_rows()——耐久／
    # 市值／缺值欄位已在 dd-screener enrich_ticker() 內用既有 None-safe 邏輯處理
    # （QGM／smallcap 供給列先例同一套機制，見 build_dd_screener.py enrich_ticker()
    # docstring），故這裡只需不被下一行「dd_status=none 一律丟給 QGM」規則連坐排除。
    # 補 _src 標籤（QGM 列由 load_qgm_rows() 標 "qgm"；一般 DD 池列靠 row_dict() 的
    # `or "dd-pool"` 預設——這批列兩者皆非，不補標籤會被誤標成 dd-pool，故在此就地
    # 補上，不改 row_dict() 本身）。
    for s in stocks:
        if s.get("universe_source") == "largecap-koyfin":
            s.setdefault("_src", "largecap-koyfin")
    stocks = [s for s in stocks if s.get("dd_status") != "none"
              or s.get("universe_source") == "largecap-koyfin"]
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

    # ── v4 own_score 跨檔百分位（見 grp.own_score_v4()）：保留一輪，只做「v4 對照」
    # tooltip 與全母體對照表排序，不影響下方 v5 池排序（見 grp.py 檔頭 v5 段第 3 點）──
    ranked = apply_own_score_v4(universe_rows)   # 已依 v4 score 降冪排序、只含有效名次者
    for i, r in enumerate(ranked, 1):
        r["rank"] = i

    # ── v5 池（品質派資格 ∧ 耐久 ∧ 財報後上修 ≥5%，見 grp.py 檔頭 v5 段第 1-4 點）──
    # r["grp"]["pass"] 已在 grp_score() 內反映品質閘/成長閘/位置閘/上修否決/新硬否決/
    # 耐久/融券高（見該函式 v5 段落），這裡只再疊加 v5 新增的「池」門檻（上修 ≥5%）。
    eligible = [r for r in universe_rows if r["grp"].get("pass")]

    def _pool_key(r: dict):
        ey = ((r["grp"].get("own") or {}).get("raw") or {}).get("ey")
        return pool_sort_key(r["grp"].get("rev_used_pct"), r.get("implied_growth_pct"), ey)

    pool_rows = sorted((r for r in eligible if in_pool(r["grp"].get("rev_used_pct"))), key=_pool_key)
    for i, r in enumerate(pool_rows, 1):
        r["pool_rank"] = i
    not_in_pool_rows = sorted((r for r in eligible if not in_pool(r["grp"].get("rev_used_pct"))), key=_pool_key)
    pool_by_ticker = {r["ticker"]: r for r in pool_rows}

    # ── 月頻輪動（arena-ledger.json，只管核心席，見 rotate_roster() docstring／
    # knowledge/rule_ledger.md「v5 席位引擎」列）──
    try:
        ledger0 = json.loads(LEDGER_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        ledger0 = {"schema_version": "5.0", "snapshots": []}
    try:
        _dd_latest_doc = json.loads(DD_LATEST.read_text(encoding="utf-8"))
        as_of = _dd_latest_doc.get("as_of", "—")
        # daily 全量重跑（見 --daily 段）：上修（池排序鍵）只在新的 Koyfin xlsx 匯入時
        # 真的變動，價格/距歷史新高/時機燈每天都變——頁首分開標兩個日期，見
        # render_board_text()/render_board_html() 的 rev_data_as_of/price_as_of 參數。
        rev_data_as_of = (_dd_latest_doc.get("eps_estimates_source") or {}).get("snapshot_date")
    except (OSError, json.JSONDecodeError):
        as_of = "—"
        rev_data_as_of = None
    price_as_of = as_of if as_of != "—" else None
    current_month = rotation_month(as_of)
    last_rotation_month = ledger0.get("last_rotation_month")
    prev_core_roster = (ledger0.get("roster") or {}).get("core")   # 月度持久化，只留核心
    w52_fail_streaks = ledger0.get("w52_fail_streak") or {}
    # prev＝上一筆「日期嚴格早於今天」的 snapshot，只給「席位變動帳本」的 up/down 對照用
    # （沿用既有 render_seat_changes 的 NEW/FROM 標記邏輯，與月頻輪動本身的 carry-forward
    # 狀態〔prev_core_roster〕是兩件事：後者決定「這個月核心坐誰」，前者只是「跟上一筆
    # 記錄比誰上誰下」的顯示層對照）。
    prev = _last_snapshot_before(ledger0.get("snapshots", []), as_of) or {"core": [], "sat": []}

    all_by_ticker = {r["ticker"]: r for r in universe_rows}
    rotation = rotate_roster(current_month, last_rotation_month, prev_core_roster, pool_rows,
                             w52_fail_streaks, all_by_ticker=all_by_ticker)
    # 沿用的現任核心席可能本次未過全部資格閘（非硬否決不下席，見 rotate_roster()）——
    # 這種列不在 pool_rows（池內、已排名者）裡，改查全母體 all_by_ticker 才能顯示。
    core_seats = [pool_by_ticker.get(t) or all_by_ticker.get(t) for t in rotation["core"]]
    core_seats = [r for r in core_seats if r is not None]
    core_seated = {r["ticker"] for r in core_seats}

    # 等待池＝池扣掉核心，依上修排序（已經是 pool_rows 的順序，直接篩即可）；
    # 可買＝等待池中時機燈綠/橘者（今天板機亮的，可能是空清單）；等待池（顯示用）＝
    # 其餘（見 grp.py 檔頭 v5 段第 5 點／knowledge/rule_ledger.md「v5 席位引擎」列）。
    waiting_pool = [r for r in pool_rows if r["ticker"] not in core_seated]
    buyable = [r for r in waiting_pool if (r.get("lamp") or {}).get("code") in ("green", "hot")]
    buyable_tickers = {r["ticker"] for r in buyable}
    waiting_rest = [r for r in waiting_pool if r["ticker"] not in buyable_tickers]

    # 備註欄用：新席／現任／遞補（核心席專屬——等待池不是持久化名單，沒有「新進池／
    # 退池」這種跨次跑狀態需要標記），並把移除理由掛回去顯示。
    prior_core_tickers = set(prev_core_roster or [])
    filled_tickers = {t for _, t in rotation["filled"]}
    removed_map = dict(rotation["removed"])
    for r in core_seats:
        t = r["ticker"]
        if rotation["rotated"]:
            r["seat_note"] = "現任" if t in prior_core_tickers else "新席"
        else:
            r["seat_note"] = "遞補" if t in filled_tickers else "現任"
        r["track"] = "core"
    for r in waiting_pool:
        r["track"] = "pool"   # 2026-09-17：backward-compat 標記，見 payload["sat_seats"] 註解

    # ── M5 對照組（_arena_body.html，PREREG 凍結，只換殼不改文，見 CLAUDE.md「Site
    # composition」段與 knowledge/rule_ledger.md）：這裡的「衛星」是凍結實驗自己的
    # 固定 5 席快照，取等待池前 5（依上修排序）當資料源，與下方真正的 v5「等待池」
    # （payload["sat_seats"]／waiting_pool 全量）是兩件事，故另立變數不共用。──
    sat_seats_m5 = waiting_pool[:SAT_SLOTS]
    seated_all = core_seated | {r["ticker"] for r in sat_seats_m5}

    core_bench = [r for r in pool_rows if r["ticker"] not in seated_all][:8]
    sat_bench: list = []   # v5 無獨立衛星候選概念（見上）；bench_seats 直接用 core_bench
    bench_seats = core_bench[:5]
    entered = [r for r in universe_rows if r["verdict"] == "進場"]

    challengers = [r for r in ranked if r["ticker"] not in seated_all]

    # 擂台配對（M5 對照組沿用不變）：軌別配對——核心席 vs 核心向挑戰者、衛星席 vs 衛星向挑戰者
    # （形狀降為資訊欄；moat 耐久性同級的才有資格互換）
    duels = []
    for seat in core_seats + sat_seats_m5:
        rivals = [c for c in challengers if c["route"] == seat["route"]]
        top = rivals[0] if rivals else None
        duels.append({"seat": seat, "challenger": top,
                      "alert": bool(top and top["score"] > seat["score"])})

    # 席位產業集中度（M5 對照組沿用不變）
    conc: dict[str, int] = {}
    for r in core_seats + sat_seats_m5:
        sec = sectors.get(r["ticker"]) or "（未分類）"
        conc[sec] = conc.get(sec, 0) + 1
    n_seated = len(core_seats + sat_seats_m5)
    conc_rows = sorted(conc.items(), key=lambda kv: -kv[1])
    max_share = (conc_rows[0][1] / n_seated * 100) if n_seated else 0

    # ── 席位變動帳本（append-only）：核心席組成變了才記一筆，換席決策從此可結算 ──
    # 帳本寫入只在 --ledger（weekly-engine.yml 排程）才發生；`--daily`／`--lamp-only`／
    # 手動跑只讀既有帳本算核心席、照常寫 arena.json 等輸出（含每日重算的池/排序/時機
    # 燈），不推進月頻輪動時鐘、不追加 snapshot（見檔頭 --daily 段與
    # knowledge/rule_ledger.md「v5 席位引擎」列）。`sat`（snapshot 內的等待池快照）
    # 純供歷史稽核用，不是持久化狀態——每次重跑都用當次 waiting_pool 重新填。
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
            "sat": [r["ticker"] for r in waiting_pool],
            "core_meta": [_seat_meta(r) for r in core_seats],
            "sat_meta": [_seat_meta(r) for r in waiting_pool],
            "rotated": rotation["rotated"],
            "removed": [{"ticker": t, "why": w} for t, w in rotation["removed"]],
            "rule_version": "v5"}
    changes = []
    # 比較基準＝嚴格早於今天的最後一筆——同日重跑不可拿「今天已寫入的自己」當基準
    # （self-referential bug：會把「今天跟今天比較」的假差異當成真變動，見檔頭說明）。
    prev_snap = _last_snapshot_before(ledger["snapshots"], as_of)
    today_entry_exists = bool(ledger["snapshots"]) and ledger["snapshots"][-1]["date"] == as_of
    if args.ledger:
        if prev_snap is None or (set(prev_snap["core"]) != set(snap["core"])
                                 or set(prev_snap.get("sat") or []) != set(snap["sat"])):
            if prev_snap:
                for track in ("core", "sat"):
                    up = sorted(set(snap[track]) - set(prev_snap.get(track) or []))
                    down = sorted(set(prev_snap.get(track) or []) - set(snap[track]))
                    if up or down:
                        changes.append({"track": track, "in": up, "out": down,
                                        "from": prev_snap["date"], "to": snap["date"]})
                snap["changes"] = changes
            if today_entry_exists:
                ledger["snapshots"][-1] = snap   # 同日重跑覆蓋（冪等）——不再依附自我比較
            else:
                ledger["snapshots"].append(snap)
        # v5 月頻輪動狀態（見 rotate_roster() docstring）——只在 --ledger 排程跑時前進：
        #   last_rotation_month／roster.core：下次跑靠這兩個值判斷「這個月核心是否已
        #   經選過」；w52_fail_streak：above_w52 為 False 逐次 +1、True 歸零（清掉不再
        #   追蹤的 ticker，避免帳本無限增長）、None（資料缺）維持原值不動。
        new_streak = dict(w52_fail_streaks)
        for r in universe_rows:
            above = r["grp"].get("above_w52")
            if above is False:
                new_streak[r["ticker"]] = new_streak.get(r["ticker"], 0) + 1
            elif above is True:
                new_streak.pop(r["ticker"], None)
        ledger["w52_fail_streak"] = new_streak
        ledger["last_rotation_month"] = current_month
        ledger["roster"] = {"core": [r["ticker"] for r in core_seats]}   # v5：等待池不持久化，見上
        LEDGER_JSON.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_JSON.write_text(json.dumps(ledger, ensure_ascii=False, indent=1),
                               encoding="utf-8")
    else:
        print("帳本唯讀（未帶 --ledger）：last_rotation_month／roster.core／snapshots 未寫入，輪動時鐘未前進。")
    recent_changes = [c for s in ledger["snapshots"][-6:] for c in (s.get("changes") or [])]

    dial = regime_dial()
    own_board = [_flat_view(r) for r in universe_rows
                 if (r["grp"].get("quality") or {}).get("pass") and (r["score"] or 0) > 0][:60]
    # 席位更新日戳記：全量重建時池/時機燈一定是這一跑剛算好的（as_of＝今天），
    # 核心席更新日＝今天（若本跑真的輪動）否則沿用帳本最近一次 rotated=True 的
    # snapshot 日期（見 --daily 段：`--daily`／`--lamp-only` 跑次因不帶 --ledger，
    # 即使命中硬否決換人也不會前進這個日期，等下次 --ledger 排程跑次才真的落帳）。
    last_rotation_date = as_of if rotation["rotated"] else _find_last_rotation_date(ledger.get("snapshots") or [])
    board_text = render_board_text(as_of, universe_rows, core_seats, buyable, waiting_rest, not_in_pool_rows,
                                   prev, entered, lamp_map, rev_data_as_of=rev_data_as_of,
                                   price_as_of=price_as_of, lamp_as_of=as_of,
                                   last_rotation_date=last_rotation_date)
    BOARD_TXT.write_text(board_text, encoding="utf-8")
    board_html = render_board_html(as_of, universe_rows, core_seats, buyable, waiting_rest, not_in_pool_rows,
                                   prev, entered, lamp_map, rev_data_as_of=rev_data_as_of,
                                   price_as_of=price_as_of, lamp_as_of=as_of,
                                   last_rotation_date=last_rotation_date)
    BOARD_HTML.write_text(board_html, encoding="utf-8")
    payload = {
        "schema_version": "5.0",
        "lamp_as_of": as_of, "lamp_source": "daily", "lamp_last_rotation_date": last_rotation_date,
        "rev_data_as_of": rev_data_as_of, "price_as_of": price_as_of,
        "method": ("v5 席位引擎（2026-09-17，owner thesis「品質派 ∩ 獲利上修 ∩ 突破還原權息歷史新高」）："
                  "資格＝品質派——品質閘（ROIC≥15∧FCF≥10，或 ROIC≥25∧FCF≥0 資本週期豁免）×三年成長"
                  "（Koyfin FY1→FY3 CAGR≥15%，耐久者 10%）×站上 52 週線×耐久一致性（QGM 五年穩定度 "
                  "≥75%，或 Koyfin 五年∧三年∧現值三者皆 ≥15%）；財報後上修 ≤−5%（缺財報錨定退回三個月）／"
                  "體質拒絕／衰退 ⛔／DD 迴避／融券占流通股比 >10% 皆整體排除（v5 無衛星軌可退）。排序＝"
                  "上修（財報後錨定，缺值退回三月）降冪，tie-break implied_growth_pct、再 tie-break 盈餘"
                  "殖利率——池＝資格全過名字中上修 ≥5% 者，own_score_v4 五百分位對照分保留一輪僅供 "
                  "hover 對照、不參與排序。板機＝時機燈（距還原權息全歷史最高收盤價與 200 日線）：綠＝"
                  "距新高 ≥−3% 且站上 200 日線；黃＝−10%~−3%；紅＝距新高 <−10% 或跌破 200 日線；橘＝過熱"
                  "（12-1 月動能 >150%）但仍在突破帶附近，倉位對應 1.0/0.5/0/0.5。核心＝池前 5，月頻輪動"
                  "（每月第一次排程整批重選一次，期間僅硬否決能換人、空位由池遞補）；衛星軌已取消，池扣掉"
                  "核心即「等待池」，依時機燈分②可買／③等待池顯示。無產業集中度上限；內部人買賣僅備註，"
                  "不進資格與排序。"),
        "universe_n": len(universe_rows),
        "seats_without_card": sorted(r["ticker"] for r in core_seats + waiting_pool if r["ticker"] not in card_stats),
        "own_board": own_board,
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regime": dial,
        "rotation": {"rotated": rotation["rotated"], "current_month": current_month,
                    "removed": [{"ticker": t, "why": w} for t, w in rotation["removed"]],
                    "filled": [{"track": tr, "ticker": t} for tr, t in rotation["filled"]]},
        "core_seats": core_seats, "core_bench": core_bench[:8],
        # v5：sat_seats 保留 key 供既有消費端（build_pipeline_page.py／
        # generate_list_forecasts.py／build_weekly_mail.py／docs/assets/imq-badge.js）
        # 向下相容，內容改成整個等待池（每列帶 track:"pool" 標記，見 row_dict()/
        # main() 上方賦值）；sat_vacant 恆為 0——池不是固定 5 席，沒有「空缺」概念，
        # 保留欄位只為了不讓舊消費端算術出錯。新欄位 buyable_seats／waiting_pool／
        # not_in_pool 供未來消費端直接讀對應區塊，不必自己重新篩 sat_seats。
        "sat_seats": waiting_pool, "sat_vacant": 0,
        "buyable_seats": buyable, "waiting_pool": waiting_rest, "not_in_pool": not_in_pool_rows,
        "pool_size": len(pool_rows),
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
    # M5 對照組（PREREG 凍結，見上方 sat_seats_m5 定義註解）：取等待池前 5 當這個
    # 凍結實驗自己的固定「衛星席位」快照，與下方 v5 真正的等待池表無關。
    sat_body = "".join(seat_tr(r, i) for i, r in enumerate(sat_seats_m5, 1))
    for i in range(SAT_SLOTS - len(sat_seats_m5)):
        sat_body += (f'<tr><td class="left">{len(sat_seats_m5)+i+1}. <span class="muted">（空缺）</span></td>'
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
<div class="hero-sub"><b>本頁「衛星席位」是 M5 對照組凍結下來的固定 {SAT_SLOTS} 檔快照（等待池前 {SAT_SLOTS} 檔，依上修排序）
——v5 起真正的衛星軌已取消，等待池本身沒有固定席次。完整等待池、時機燈與核心輪動請看上方「選股看板 v5」；
本頁只保留擂台配對／席位變動帳本／產業分布這些既有的凍結視圖，僅換殼不改文。</b></div>
<div class="hero-sub">組合才是產品：核心 {CORE_SLOTS} 席＋衛星快照 {SAT_SLOTS} 席，每席對決「同形狀最強挑戰者」。
⚔ 警報＝挑戰者分數超過席位 → 進<b>每月擂台的人工複審清單</b>。引擎不自動換席——換人是人的裁決。
資格（<b>v5 品質派</b>，2026-09-17 持有人拍板）＝<b>品質閘</b>（ROIC ≥15 ∧ FCF ≥10；capex 週期豁免 ROIC ≥25 ∧ FCF ≥0）×
<b>成長閘</b>（FY1→FY3 EPS CAGR ≥15%，耐久者放寬至 10%；且成長必須是三年期 Koyfin 數字——只有 FY1→FY2 單年 fallback 的名字不入池，改列「可選但先不入池」隊列）× <b>位置閘</b>（站上 52 週線）× <b>耐久一致性</b>（QGM 五年穩定度 ≥75%，或 Koyfin 五年∧三年∧現值三者皆 ≥15%）× <b>財報後上修否決</b>（≤−5%，以該股自己最近一次財報日前最新月度 snapshot 為基準，缺財報錨定退回舊制近三個月日曆窗；FY+1 單月 ≤−10% 僅兩者皆缺值時 fallback）× 新硬否決（體質拒絕／衰退 ⛔／DD 迴避 180 天內／融券占流通股比 &gt;10%）——<b>不耐久、融券高皆整體資格排除，v5 沒有衛星軌可以收留</b>。
排序＝<b>上修單一變數</b>（財報後錨定，缺值退回三個月）降冪，同值 tie-break implied_growth_pct、再 tie-break 盈餘殖利率——資格全過者中，上修 ≥+5% 才進「池」，池即候選／候補的全部。舊 <b>own_score v4</b>（財報後上修、12-1 月動能、成長封頂 30、品質、盈餘殖利率五個百分位平均）保留一輪只做逐檔「v4 對照」，不參與本排序。成長遇<b>基期效應</b>（FY1→FY2 因低基期跳增 &gt;1.6x 且 FY2→FY3 成長 &lt;20%）改用 FY2→FY3 成長率取代（此項仍作用於成長閘本身）。
<b>過熱／頂點不是資格閘</b>：12-1 月動能 &gt;150%（缺值 fallback 26 週漲幅 &gt;80%）＝過熱，只影響時機燈（🟠過熱，半倉），v5 起不再排除核心候選（核心純比池內排序前 5）；roic_vs_5y_x ≥1.3＝頂點，純顯示註記（⚠）。<b>內部人買賣</b>（近 3 個月淨股數）僅供備註，不進資格與排序。
<b>DD 選配</b>：不是入池前提，只做迴避否決（180 天內），觀望／進場僅供角色標籤參考（僅供顯示）。
<b>月頻輪動</b>：每月第一次排程整批重選一次；期間只有七項硬否決（迴避／拒絕／⛔／財報後上修跌破 ≤−5%／市值不足／連兩週跌破 52 週線／融券轉高）能讓現任核心下席，空位由池遞補。
<b>核心＝池前 5</b>（純比上修排序，不再有 DD 角色或護城河字母路由）；沒卡進核心前 5 名的池成員全部叫「等待池」，本頁的「衛星席位」只是取其中前 {SAT_SLOTS} 檔當這個凍結實驗自己的固定快照，並非真的還有一個 {SAT_SLOTS} 席的衛星軌。
<b>市值門檻 ≥ ${MKTCAP_MIN/1e9:.0f}B</b>（持有人 2026-07-04 拍板：席位與主榜資格層；雷達發現層照掃全宇宙）。
<b>母體＝美股含 ADR；台股另建（.TW 不在本看板，2026-09-02 持有人拍板）</b>。無產業/主題集中度上限（2026-09-17 持有人拍板）。
<b>快審卡</b>：等待池另接受 🪶 快審卡（週期位置＋陷阱＋護城河快評），與三年成長閘、DD 皆無關。
資格未過的進場票落板凳、寧缺勿濫。</div>
<div class="asof">資料源 dd-screener latest.json ＋ QGM 品質池（US／TW）＋週線 cache ｜ v5 品質派資格×上修排序×歷史新高板機 ｜ 月頻輪動</div>
</div>
<div class="block"><h2>選股看板 v5</h2>
<div class="block-sub">上修排序（值不值得擁有）與時機燈（現在能不能買）分開讀；DD 只做迴避否決與角色標籤。</div>
{board_html}</div>
<div class="stat-row">
<div class="stat"><strong>{dial['label'] if dial['level'] else '—'}</strong><span>Regime 撥盤（{dial['level'] if dial['level'] else '—'}×）</span></div>
<div class="stat"><strong>{sum(1 for d in duels if d['alert'])}</strong><span>⚔ 擂台警報</span></div>
<div class="stat"><strong>{len(core_seats)}/{CORE_SLOTS} · {len(sat_seats_m5)}/{SAT_SLOTS}</strong><span>核心 · 衛星快照</span></div>
<div class="stat"><strong>{payload['max_sector_share_pct']}%</strong><span>最大單一產業占席</span></div>
</div>
<div class="note">Regime：{escape(dial.get('detail') or '')}（as of {escape(str(dial.get('as_of') or '—'))}）。
撥盤規則 v1 鎖定：進攻 1.0＝confirmed_uptrend 且 distribution ≤3；中性 0.5＝under_pressure 或 4–7；
防守 0.25＝correction／跌破 200DMA／≥8。<b>資訊性，不接倉位系統</b>——新倉節奏由人按撥盤自裁。
形狀敏感度：突破帶/動能重估最敏感（防守時停新倉）、循環轉折次之（防守時只留回踩單）。</div>
<div class="block"><h2>核心席位（{len(core_seats)}/{CORE_SLOTS}）</h2>{core_tbl}</div>
<div class="block"><h2>衛星席位·M5 快照（{len(sat_seats_m5)}/{SAT_SLOTS}）</h2>{sat_tbl}</div>
<div class="block"><h2>擂台對戰表</h2>
<div class="block-sub">v5 起池內名字的軌別一律是「核心」（見 grp.grp_route() v5 附註：耐久已升級為資格閘本體，
沒過耐久的名字根本進不了池），故本表不再有「核心向」「衛星向」挑戰者的區分，核心席與衛星快照皆對比同一份
挑戰者池（形狀僅供資訊）；挑戰者資格＝裁決 ∈ {{進場、觀望}} ∩ 資格全過。觀望挑戰者勝出＝先觸發它的複審，不是直接換。</div>
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
    universe_board = build_universe_board(universe_rows, core_seats, sat_seats_m5, core_bench, sat_bench, as_of)
    UNIVERSE_BOARD_JSON.write_text(json.dumps(universe_board, ensure_ascii=False, indent=1), encoding="utf-8")
    ARENA_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    ARENA_HTML.write_text(
        page_embed_shell("席位擂台 · 席位排序", body,
                         "核心 5 席 vs 等待池前 5 檔快照（M5 對照組）vs 同形狀挑戰者的每月擂台 — regime 撥盤與集中度警戒"),
        encoding="utf-8")
    print(f"arena: regime={dial['label']} 警報={sum(1 for d in duels if d['alert'])} "
          f"核心={[r['ticker'] for r in core_seats]} 等待池={len(waiting_pool)}（可買 {len(buyable)}）"
          f" 集中度={payload['max_sector_share_pct']}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
