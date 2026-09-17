#!/usr/bin/env python3
"""DD Screener Phase 1 — stateless orchestrator.

Pipeline:
  Step 1-2  load 98 DDs + latest DCA per ticker  (dd_screener_dd_loader)
  Step 3    hybrid quality data (QGM + yfinance)  (dd_screener_quality)
  Step 4    MA snapshot                            (dd_screener_ma)
  Step 5    compute pass/fail per criterion
  Step 6    write docs/dd-screener/latest.json

Output schema: scripts/dd_screener_schema.md (locked v1.0)

Usage:
  python3 scripts/build_dd_screener.py             # full universe, ~6-8 min
  python3 scripts/build_dd_screener.py --top 10    # smoke-test first 10 tickers
  python3 scripts/build_dd_screener.py --dry-run   # don't write file
  python3 scripts/build_dd_screener.py --no-ma     # skip MA fetch (faster smoke)

Timing fallback (added 2026-05-17):
  DD tickers not in the S&P500/NQ100 screener universe (e.g. ALAB, MRVL, SPOT,
  TW/JP local listings) receive timing data from a yfinance batch fetch instead of
  docs/screener/latest.json.

  rs_score methodology for fallback tickers:
    - Fetch 300d daily closes for all missing tickers in one yf.download() call.
    - Use docs/screener/latest.json rankings as the reference population: each
      ranking entry already carries rs_1w/rs_4w/rs_13w (EMA-smoothed percentile
      scores). These are treated as the "anchored" distribution.
    - For each missing ticker compute raw r1w/r4w/r13w returns, then percentile-rank
      them against the union of (screener smoothed scores + missing ticker raw scores).
      This is an approximation (no EMA smoothing for fallback tickers) but consistent
      with the page's existing framing (all scores are relative to the same ~511-stock
      US universe).
    - TW/JP local-listings (2330.TW, etc.) are ranked against the same US universe.
      This is noisy because of JPY/TWD FX effects but chosen for consistency over a
      parallel methodology. The timing_source field is set to "yfinance_fallback" for
      all fallback tickers so the FE can surface caveats if needed.
    - Tickers that yfinance refuses to serve for any metric get timing=null for that
      metric (never raises, graceful degradation).
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
import warnings
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "pandas", "numpy", "-q"])
    import numpy as np
    import pandas as pd
    import yfinance as yf

logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("peewee").setLevel(logging.CRITICAL)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dd_screener_dd_loader import load_dd_universe, load_non_dd_universe, _norm_dca_role  # noqa: E402
from dd_screener_quality import (  # noqa: E402
    EU_SUFFIX_MAP,
    TICKER_YF_OVERRIDE,
    get_quality_for_ticker,
    load_qgm_durability_index,
    load_qgm_index,
)
from dd_screener_ma import compute_ma_snapshot  # noqa: E402
from update_dd_index import (  # noqa: E402
    collect_dca_ev_map,
    collect_dca_moat_trend_map,
    compute_dca_irr,
)
from load_eps_estimates_xlsx import (  # noqa: E402
    ExcelSnapshot,
    SKIP_TICKERS,
    apply_adr_ratio,
    find_latest_excel,
    load_latest_excel,
)
from eps_fx_normalize import (  # noqa: E402
    compute_fx_normalized_revision,
    get_fx_rate,
    get_reporting_currency,
    load_fx_daily_cache,
    load_reporting_currency_cache,
    save_fx_daily_cache,
    save_reporting_currency_cache,
)

OUTPUT_DIR = ROOT / "docs" / "dd-screener"
OUTPUT_PATH = OUTPUT_DIR / "latest.json"
SCREENER_LATEST = ROOT / "docs" / "screener" / "latest.json"
# P1: 機器抽取的 v12 舊 DD 裁決 overlay（僅補 dd-meta 沒有原生 dca_verdict 的 ticker）。
# 缺檔／壞檔一律靜默降級（見 apply_verdict_overlay），screener 行為回到現狀。
VERDICT_OVERLAY_PATH = ROOT / "docs" / "dd" / "verdict_overlay.json"

# Locked v1.0 criteria — matches scripts/dd_screener_schema.md
#
# 2026-07-03（Task 1）：D/E 退出 pass_count 計分，降為 advisory（`advisory: True`）。
# 持有人 2026-06-11 拍板的質量五條件並無 D/E —— D/E≤0.7 是實作私加的第五條，
# 在成長 / 循環贏家樣本誤殺 AVGO / LLY / APP / SEZL / STX（皆槓桿或資本結構因子，
# 非品質本體缺陷）。改法：欄位照算照顯示，但 (1) 不計入 pass_count / fail_criteria
# (2) 不進 FunnelRank QualityGate 分母 (3) 前端改成 D/E>0.7 顯示 ⚠ 警示 badge、不擋閘。
# 質量閘回歸「四條件（FCF / ROIC / EPS CAGR / PEG）＋護城河 veto」。護城河 veto
# （grade∉{C,X} 且 trend≠↓）在 sop_funnel.engine.quality_check 實作，故 pass_count
# 維持四條件；前端文案如實寫「4 條件＋護城河 veto」。
CRITERIA = [
    {"key": "fcf",   "label": "FCF≥10%",  "threshold": 10.0, "invert": False, "unit": "%"},
    {"key": "roic",  "label": "ROIC≥15%", "threshold": 15.0, "invert": False, "unit": "%"},
    {"key": "eps2y", "label": "FY+1→FY+3 CAGR≥15%",  "threshold": 15.0, "invert": False, "unit": "%"},
    {"key": "peg",   "label": "PEG≤2.0",  "threshold": 2.0,  "invert": True,  "unit": "x"},
    {"key": "de",    "label": "D/E≤0.7",  "threshold": 0.7,  "invert": True,  "unit": "x",
     "advisory": True},
]

# 進 pass_count / fail_criteria / QualityGate 計分的條件（排除 advisory 的 D/E）。
SCORED_CRITERIA = [c for c in CRITERIA if not c.get("advisory")]

PRESETS = {
    "MLB": {"fcf": 10.0, "roic": 15.0, "eps2y": 15.0, "peg": 2.0, "de": 0.7},
}

DEFAULT_FILTER = {"moat_min": 9.5, "directions": ["↑", "→"]}

# ---------------------------------------------------------------------------
# FunnelRank (v1.3) — 漏斗綜合排序分
# ---------------------------------------------------------------------------
# 把「QGM 5/5 → Moat → 修正動能 → 時機」四層人工漏斗的前三層（基本面）固化成
# 一個 0–1 排序鍵。時機（第四層）維持 filter 不進排序分 —— 與 entry-state 的
# 「基本面排序、時機另看」哲學一致。
#
#   FunnelRank = w_quality·QualityGate + w_moat·MoatScore + w_revision·RevisionScore
#
# 全部用既有欄位合成，不新增任何外部資料抓取。權重與映射值集中於此，方便調參。
FUNNEL_WEIGHTS = {"quality": 0.40, "moat": 0.30, "revision": 0.30}

# QualityGate 映射 — 帶「可原諒條件」：PEG fail 視為估值問題，非品質本體缺陷，
# 扣分較輕；FCF / ROIC / EPS CAGR fail 是品質本體缺陷，重扣。
# 2026-07-03：D/E 退出計分（advisory），故不再列為 forgivable fail —— 它根本不進
# QualityGate 分母。滿分現為四條件全過（ratio 1.0），唯一 fail 在 PEG → forgivable。
FUNNEL_QUALITY_MAP = {
    "pass5": 1.00,              # 四條件全過（key 名沿用歷史，不改以維持下游相容）
    "pass4_forgivable": 0.85,   # 唯一 fail 在 PEG
    "pass4_core": 0.50,         # fail 在 FCF / ROIC / EPS CAGR
    "pass3": 0.30,
    "pass_le2": 0.10,
}
FUNNEL_FORGIVABLE_FAILS = {"peg"}

# MoatScore：base = moat_score/10，再乘趨勢乘數，cap 1.0。
FUNNEL_MOAT_TREND_MULT = {"↑": 1.10, "→": 1.00, "↓": 0.80}
FUNNEL_MOAT_NO_DATA = 0.50

# RevisionScore：FY1/FY2/FY3 各自上修(+1)/持平(0)/下修(-1)，FY3 權重最大
# （成長曲線後段）。raw ∈ [-1, +1] → (raw+1)/2 ∈ [0, 1]。
FUNNEL_REVISION_THRESHOLD = 0.5   # |diff| ≥ 0.5% 才算上修/下修
FUNNEL_REVISION_FY_WEIGHTS = {"fy1": 0.2, "fy2": 0.3, "fy3": 0.5}
FUNNEL_REVISION_STEEPENING_BONUS = 0.05   # FY3 上修幅度 > FY1 上修幅度 → 加分
FUNNEL_REVISION_NO_BASELINE = 0.50        # 「新」chip / 無 baseline → 中性

# Hard veto / cap（不進加權公式，直接處置）。
FUNNEL_MOAT_DOWN_CAP = 0.50   # moat trend ↓ 且非四條件全過 → FunnelRank cap

# 2026-09-17（owner 拍板）：體質五項 veto（compute_fundamental_gates 的
# quality_veto_level）與衰退訊號（decline_signal_light）併入 FunnelRank —— 見
# compute_funnel_rank() docstring「四道處置」。
FUNNEL_QUALITY_REJECT_CAP = 0.30      # quality_veto_level == "拒絕" → cap
FUNNEL_QUALITY_DOWNGRADE_CAP = 0.60   # quality_veto_level == "降一級" → cap


def compute_quality_gate(quality: dict) -> tuple[float, bool]:
    """QualityGate (0–1) with forgivable-fail logic + partial-data scaling.

    Returns (gate, partial). `partial` is True when any of the 5 criteria has
    no data (null) — that criterion drops out of the denominator and the pass
    *ratio* over the present criteria is mapped through the same anchor points,
    so a full-data 4/5 and a partial 3/4 (both ratio 0.75) score alike.

    Anchor points (ratio → score) reproduce the full-data mapping exactly.
    2026-07-03: scoring is over SCORED_CRITERIA (4 conditions — D/E excluded);
    "forgivable" now means the sole fail is PEG.
        ratio 1.0          → 1.00
        ratio [0.7, 1.0)   → 0.85 (forgivable: only PEG failed) else 0.50
        ratio [0.5, 0.7)   → 0.30
        ratio < 0.5        → 0.10
    """
    # 2026-07-03: score over SCORED_CRITERIA only (D/E advisory 已排除)。
    present = [c for c in SCORED_CRITERIA if quality.get(c["key"]) is not None]
    n_present = len(present)
    if n_present == 0:
        # No quality data at all — bottom bucket, flagged partial.
        return FUNNEL_QUALITY_MAP["pass_le2"], True

    fails_present: list[str] = []
    for c in present:
        v = quality[c["key"]]
        ok = (v <= c["threshold"]) if c["invert"] else (v >= c["threshold"])
        if not ok:
            fails_present.append(c["key"])
    n_pass = n_present - len(fails_present)
    partial = n_present < len(SCORED_CRITERIA)

    forgivable = bool(fails_present) and set(fails_present) <= FUNNEL_FORGIVABLE_FAILS
    ratio = n_pass / n_present

    if ratio >= 1.0 - 1e-9:
        gate = FUNNEL_QUALITY_MAP["pass5"]
    elif ratio >= 0.7:
        gate = FUNNEL_QUALITY_MAP["pass4_forgivable"] if forgivable \
            else FUNNEL_QUALITY_MAP["pass4_core"]
    elif ratio >= 0.5:
        gate = FUNNEL_QUALITY_MAP["pass3"]
    else:
        gate = FUNNEL_QUALITY_MAP["pass_le2"]
    return gate, partial


def compute_moat_score_adj(moat_score, moat_trend: str) -> tuple[float, bool]:
    """MoatScore (0–1) = (moat_score/10) × trend-multiplier, cap 1.0.

    Returns (score, no_data). no_data=True (→ 0.50) when moat_score is absent
    (rare — loader requires it, but guard anyway).
    """
    if moat_score is None:
        return FUNNEL_MOAT_NO_DATA, True
    base = float(moat_score) / 10.0
    mult = FUNNEL_MOAT_TREND_MULT.get(moat_trend, 1.0)
    return min(1.0, base * mult), False


def _revision_signal(diff) -> int:
    """+1 上修 / 0 持平 or 無資料 / -1 下修."""
    if diff is None:
        return 0
    if diff >= FUNNEL_REVISION_THRESHOLD:
        return 1
    if diff <= -FUNNEL_REVISION_THRESHOLD:
        return -1
    return 0


def compute_revision_score(rev_fy1, rev_fy2, rev_fy3) -> tuple[float, bool]:
    """RevisionScore (0–1) from FY1/FY2/FY3 EPS revision % vs prior snapshot.

    Returns (score, no_baseline). no_baseline=True (→ 0.50 中性) when ALL three
    FY revision values are None (ticker new to snapshot, or no baseline yet).
    When a baseline exists but a single FY column is missing, that column is
    treated as a neutral (0) signal rather than collapsing the whole score —
    this is the edge case most prone to error, kept explicit on purpose.
    """
    if rev_fy1 is None and rev_fy2 is None and rev_fy3 is None:
        return FUNNEL_REVISION_NO_BASELINE, True

    s1 = _revision_signal(rev_fy1)
    s2 = _revision_signal(rev_fy2)
    s3 = _revision_signal(rev_fy3)
    w = FUNNEL_REVISION_FY_WEIGHTS
    raw = w["fy1"] * s1 + w["fy2"] * s2 + w["fy3"] * s3   # ∈ [-1, +1]
    score = (raw + 1.0) / 2.0

    # Steepening bonus: FY3 上修幅度 > FY1 上修幅度（成長曲線後段變陡），須兩者皆上修。
    if (rev_fy1 is not None and rev_fy3 is not None
            and s1 == 1 and s3 == 1 and rev_fy3 > rev_fy1):
        score = min(1.0, score + FUNNEL_REVISION_STEEPENING_BONUS)
    return score, False


def compute_funnel_rank(
    quality: dict,
    pass_count: int,
    moat_score,
    moat_trend: str,
    rev_fy1,
    rev_fy2,
    rev_fy3,
    quality_veto_level: str | None = None,
    decline_signal_light: str | None = None,
) -> dict:
    """Compose FunnelRank (0–1) from the three fundamental sub-scores + vetoes.

    Four processes outside the weighted formula (max-severity wins — a hard 0
    always stays 0 regardless of what the soft caps below would have computed):
      1. FY1/FY2/FY3 三欄全部下修 → FunnelRank 強制歸 0（領先指標壓過落後的品質分），
         該列沉底 + veto_all_downgrade=True（FE 顯示 ⛔）。三欄須皆有資料且皆下修。
      2. moat trend ↓ 且非四條件全過（pass_count < len(SCORED_CRITERIA)）→ FunnelRank cap 0.50。
      3. （2026-09-17 owner 拍板）decline_signal_light == "⛔"（compute_fundamental_gates
         的衰退訊號 6 項機械指標命中 ≥5 項）→ FunnelRank 同樣強制歸 0，
         veto_decline_signal=True——衰退訊號跟 FY 下修一樣屬領先指標，一併壓過落後的
         品質分。
      4. （2026-09-17 owner 拍板）quality_veto_level（compute_fundamental_gates 的
         體質五項 veto）="拒絕" → cap 0.30；="降一級" → cap 0.60，
         funnel_cap_quality=True + funnel_cap_quality_level 記錄命中的級別。
         但當 rev_fy1/rev_fy2/rev_fy3 三欄皆有資料且皆 ≥ +0.5%（FUNNEL_REVISION_THRESHOLD，
         全部上修）時，此封頂不生效（quality_cap_overridden_by_revision=True）——
         上修同樣是領先指標，壓過落後的體質評等。

    Returns a dict of all funnel fields (rounded to 4dp so the FE can re-derive
    the weighted sum within < 0.001 for non-veto, non-capped rows).
    """
    quality_gate, q_partial = compute_quality_gate(quality)
    moat_adj, moat_missing = compute_moat_score_adj(moat_score, moat_trend)
    revision_score, no_baseline = compute_revision_score(rev_fy1, rev_fy2, rev_fy3)

    quality_gate = round(quality_gate, 4)
    moat_adj = round(moat_adj, 4)
    revision_score = round(revision_score, 4)

    w = FUNNEL_WEIGHTS
    funnel = (w["quality"] * quality_gate
              + w["moat"] * moat_adj
              + w["revision"] * revision_score)

    # Veto 1: all three FY downgraded (each present and ≤ -0.5%).
    all_down = (
        rev_fy1 is not None and rev_fy2 is not None and rev_fy3 is not None
        and rev_fy1 <= -FUNNEL_REVISION_THRESHOLD
        and rev_fy2 <= -FUNNEL_REVISION_THRESHOLD
        and rev_fy3 <= -FUNNEL_REVISION_THRESHOLD
    )
    # Veto 3 (new): decline-signal light at ⛔ (≥5 of 6 mechanical hits).
    veto_decline_signal = decline_signal_light == "⛔"

    # Override (c): leading revisions (all three FY, each ≥ +0.5%) override the
    # lagging quality-cap in (b) — same FX-normalized inputs as veto 1 above.
    revisions_all_up = (
        rev_fy1 is not None and rev_fy2 is not None and rev_fy3 is not None
        and rev_fy1 >= FUNNEL_REVISION_THRESHOLD
        and rev_fy2 >= FUNNEL_REVISION_THRESHOLD
        and rev_fy3 >= FUNNEL_REVISION_THRESHOLD
    )
    quality_cap_overridden_by_revision = (
        quality_veto_level in ("拒絕", "降一級") and revisions_all_up
    )

    cap_moat_down = False
    funnel_cap_quality = False
    funnel_cap_quality_level = None
    if all_down or veto_decline_signal:
        funnel = 0.0
    else:
        if moat_trend == "↓" and pass_count < len(SCORED_CRITERIA):
            # Cap 2: weakening moat WITHOUT a clean full pass → cap.
            # 2026-07-03: max pass_count 由 5→4（D/E 退出計分）。原條件硬編 `<= 4`
            # ＝「非 5/5」；現改 `< len(SCORED_CRITERIA)`（＝「非 4/4」）以維持相同語義
            # ——四條件全過的 ↓-trend 名字不被 cap，未全過的才 cap。
            cap_moat_down = funnel > FUNNEL_MOAT_DOWN_CAP
            funnel = min(funnel, FUNNEL_MOAT_DOWN_CAP)

        if not quality_cap_overridden_by_revision:
            cap_value = None
            if quality_veto_level == "拒絕":
                cap_value = FUNNEL_QUALITY_REJECT_CAP
            elif quality_veto_level == "降一級":
                cap_value = FUNNEL_QUALITY_DOWNGRADE_CAP
            if cap_value is not None:
                funnel_cap_quality = funnel > cap_value
                funnel = min(funnel, cap_value)
                if funnel_cap_quality:
                    funnel_cap_quality_level = quality_veto_level

    return {
        "funnel_rank": round(funnel, 4),
        "quality_gate": quality_gate,
        "moat_score_adj": moat_adj,
        "revision_score": revision_score,
        "veto_all_downgrade": all_down,
        "funnel_cap_moat_down": cap_moat_down,
        "veto_decline_signal": veto_decline_signal,
        "funnel_cap_quality": funnel_cap_quality,
        "funnel_cap_quality_level": funnel_cap_quality_level,
        "quality_cap_overridden_by_revision": quality_cap_overridden_by_revision,
        "quality_gate_partial": q_partial,
        "moat_no_data": moat_missing,
        "revision_no_baseline": no_baseline,
    }


# ---------------------------------------------------------------------------
# Step 5: pass/fail
# ---------------------------------------------------------------------------


def evaluate_criteria(quality: dict) -> tuple[int, list[str]]:
    """Return (pass_count, fail_criteria) using locked MLB thresholds.

    2026-07-03 (Task 1): scored over SCORED_CRITERIA — the four quality
    conditions (FCF / ROIC / EPS CAGR / PEG). D/E is advisory and never
    enters pass_count or fail_criteria (surfaced separately via
    `de_advisory_flag()` so the FE renders a ⚠ badge, not a red fail cell).
    pass_count therefore tops out at 4; the 5th condition (moat grade/trend
    veto) lives in sop_funnel.engine.quality_check, not here.

    A null field is treated as a failed criterion (can't verify), recorded
    in fail_criteria so the front-end can show "—" rather than red.
    """
    fails: list[str] = []
    passes = 0
    for c in SCORED_CRITERIA:
        v = quality.get(c["key"])
        if v is None:
            fails.append(c["key"])
            continue
        ok = (v <= c["threshold"]) if c["invert"] else (v >= c["threshold"])
        if ok:
            passes += 1
        else:
            fails.append(c["key"])
    return passes, fails


def de_advisory_flag(quality: dict) -> bool:
    """True when D/E is present and breaches the advisory threshold (>0.7).

    Advisory only — does NOT affect pass_count / fail_criteria. The FE turns
    this into a ⚠ badge on the D/E cell (warn, don't gate).
    """
    de_crit = next((c for c in CRITERIA if c["key"] == "de"), None)
    if de_crit is None:
        return False
    v = quality.get("de")
    if v is None:
        return False
    # de is an "invert" criterion (pass = v <= threshold); advisory warn = fail side.
    return v > de_crit["threshold"]


# ---------------------------------------------------------------------------
# Step 7: orchestrate
# ---------------------------------------------------------------------------


def _sort_key(s: dict) -> tuple:
    # v1.3: default ordering is FunnelRank desc (漏斗綜合分 — 基本面三層合成).
    # all-downgrade veto rows carry funnel_rank=0 so they sink to the bottom.
    # Tie-break preserves the legacy chain: pass_count → moat_score → 5Y IRR
    # → ticker. The FE honours this order when no column sort is active.
    funnel = s.get("funnel_rank")
    irr = s.get("ev5y_pct")
    return (
        -(funnel if funnel is not None else -1.0),
        -s["pass_count"],
        -(s.get("moat_score") or 0),
        -(irr if irr is not None else -1e9),
        s["ticker"],
    )


def _yf_ticker_for_ma(dd_ticker: str) -> str:
    """Same resolution as quality module: explicit override → EU suffix → pass-through."""
    if dd_ticker in TICKER_YF_OVERRIDE:
        return TICKER_YF_OVERRIDE[dd_ticker]
    if dd_ticker in EU_SUFFIX_MAP:
        return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}"
    return dd_ticker


def _empty_ma() -> dict:
    return {
        "price": None, "w52": None, "w104": None, "w250": None,
        "slope_w250_pct": None, "drift_4w_pct": None,
        "above_w52": None, "above_w250": None,
        # v1.6: 5y cycle context for entry-state-machine (additive, all None on failure)
        "high_250w_price": None, "dist_250w_high_pct": None,
        "weeks_since_250w_high": None, "is_full_5y": None,
        "drift_4w_min_in_8w": None,
    }


def load_ma_cache(path: Path) -> dict[str, dict]:
    """v1.4: Read existing latest.json's MA snapshots so they can be reused
    when yfinance fails (rate-limit, network blip). Each cache entry carries
    `_stamp` = date of the snapshot it came from, for FE staleness display.

    Without this, a single failed yfinance batch wipes all MA data; with it,
    we degrade gracefully to last known value.
    """
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    stamp = data.get("as_of") or "unknown"
    cache: dict[str, dict] = {}
    for s in data.get("stocks", []) or []:
        t = s.get("ticker")
        ma = s.get("ma") or {}
        # Only cache rows where at least the price + w250 came through last time
        if t and ma.get("price") is not None and ma.get("w250") is not None:
            cache[t] = {**ma, "_stamp": stamp}
    return cache


_QUALITY_FIELDS = ("fcf", "roic", "eps2y", "peg", "de")


def load_quality_cache(path: Path) -> dict[str, dict]:
    """v1.5: Read existing latest.json's quality fields (fcf/roic/eps2y/peg/de)
    so they can be reused when yfinance fails for the quality fetch path.

    Mirrors load_ma_cache(). Only caches yfinance-source rows where at least
    one of the 5 fields was non-None last run (i.e. previous fetch wasn't
    itself a total wipe). QGM-sourced rows are skipped — those load from
    QGM JSON on disk and don't need cache fallback. koyfin-xlsx rows (roic/fcf
    override, 2026-09-09) are skipped for the same reason: they're re-derived
    fresh from the Excel snapshot on every build, not fetched over the
    network, so there's no outage signature to cache against.

    To avoid recursive cache pollution after multi-day outages, we still
    cache rows previously served from cache, but propagate the original
    `_cache_stamp` instead of bumping it — so FE always shows the true
    freshness of the underlying yfinance data.
    """
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    stamp = data.get("as_of") or "unknown"
    cache: dict[str, dict] = {}
    for s in data.get("stocks", []) or []:
        t = s.get("ticker")
        if not t:
            continue
        src = s.get("quality_source") or ""
        # Only cache yfinance-path rows (QGM rows load from JSON, no need)
        if not src.startswith("yfinance"):
            continue
        quality = {k: s.get(k) for k in _QUALITY_FIELDS}
        non_null = sum(1 for v in quality.values() if v is not None)
        if non_null == 0:
            continue
        # Preserve original cache stamp if previous run was already cached
        existing_stamp = s.get("quality_cache_stamp")
        cache[t] = {
            **quality,
            "_stamp": existing_stamp or stamp,
            "_was_cached": bool(s.get("quality_from_cache")),
        }
    return cache


def load_screener_timing_map() -> dict[str, dict]:
    """Build {ticker: {dist_52w_high_pct, ma50_pct, vs_200ma_pct, rs_score,
    rs_1w, rs_4w, rs_13w, timing_source}} from `docs/screener/latest.json`.

    Also carries rs_1w/rs_4w/rs_13w so compute_yfinance_timing_fallback() can
    use the screener's EMA-smoothed sub-scores as the reference population for
    percentile-ranking the 34 DD tickers that aren't in the screener universe.

    Non-US DD tickers (TW/JP/EU) will not appear here — caller falls back to
    compute_yfinance_timing_fallback() for them.
    """
    if not SCREENER_LATEST.exists():
        print(f"  WARN: {SCREENER_LATEST} not found — timing fields will be null", file=sys.stderr)
        return {}
    try:
        data = json.loads(SCREENER_LATEST.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  WARN: failed to parse {SCREENER_LATEST}: {exc}", file=sys.stderr)
        return {}
    out: dict[str, dict] = {}
    for r in data.get("rankings", []) or []:
        t = r.get("ticker")
        if not t:
            continue
        out[t] = {
            "dist_52w_high_pct": r.get("dist_52w_high_pct"),
            "ma50_pct": r.get("ma50_pct"),
            "vs_200ma_pct": r.get("vs_200ma_pct"),
            "rs_score": r.get("rs_score"),
            # Sub-scores for RS reference population (used by fallback only)
            "rs_1w": r.get("rs_1w"),
            "rs_4w": r.get("rs_4w"),
            "rs_13w": r.get("rs_13w"),
            "timing_source": "screener",
        }
    return out


def _calc_return(closes: "pd.Series", days: int) -> float | None:
    """Return % return over last N trading days; None if insufficient history."""
    if len(closes) < days + 1:
        return None
    v = float(closes.iloc[-1])
    vn = float(closes.iloc[-(days + 1)])
    if vn == 0:
        return None
    return (v / vn - 1) * 100.0


def _percentile_rank_value(val: float, population: list[float]) -> float:
    """Percentile rank (0-100) of val within population (including val itself)."""
    if not population:
        return 50.0
    return sum(1 for x in population if x <= val) / len(population) * 100.0


def _chunked_download_with_retry(
    tickers: list[str],
    period: str = "300d",
    interval: str = "1d",
    chunk_size: int = 50,
    max_retries: int = 3,
    backoff_seconds: tuple[int, ...] = (15, 60, 180),
) -> "pd.DataFrame":
    """Batch-fetch daily OHLC for many tickers, robust to yfinance rate-limits.

    Splits the ticker list into chunks of ``chunk_size`` and downloads each
    chunk independently. If a chunk raises ``YFRateLimitError`` or returns an
    empty frame, it is retried up to ``max_retries`` times with exponential
    backoff per ``backoff_seconds``. Successful chunks are concatenated into
    a single multi-index DataFrame (columns = MultiIndex(ticker, ohlc)) that
    matches the shape of ``yf.download(group_by='ticker')``.

    Failed chunks are silently dropped — downstream callers handle missing
    tickers via ``_get_closes() returning None``. Never raises.
    """
    if not tickers:
        return pd.DataFrame()

    chunks: list[pd.DataFrame] = []
    n_chunks = (len(tickers) + chunk_size - 1) // chunk_size
    failed_tickers: list[str] = []

    for chunk_idx in range(n_chunks):
        chunk_tickers = tickers[chunk_idx * chunk_size:(chunk_idx + 1) * chunk_size]
        chunk_df: pd.DataFrame | None = None

        for attempt in range(max_retries):
            try:
                df = yf.download(
                    chunk_tickers,
                    period=period,
                    interval=interval,
                    group_by="ticker",
                    progress=False,
                    threads=True,
                    auto_adjust=True,
                )
                # Empty frame = rate-limited or all tickers invalid — retry.
                if df is None or df.empty:
                    raise RuntimeError("empty frame returned (likely rate-limited)")
                chunk_df = df
                break
            except Exception as exc:
                exc_name = type(exc).__name__
                if attempt < max_retries - 1:
                    delay = backoff_seconds[min(attempt, len(backoff_seconds) - 1)]
                    print(
                        f"  [chunked] chunk {chunk_idx + 1}/{n_chunks} "
                        f"attempt {attempt + 1}/{max_retries} failed "
                        f"({exc_name}); sleeping {delay}s ...",
                        file=sys.stderr,
                    )
                    time.sleep(delay)
                else:
                    print(
                        f"  [chunked] chunk {chunk_idx + 1}/{n_chunks} "
                        f"exhausted {max_retries} retries ({exc_name}); "
                        f"dropping {len(chunk_tickers)} tickers",
                        file=sys.stderr,
                    )
                    failed_tickers.extend(chunk_tickers)

        if chunk_df is not None:
            chunks.append(chunk_df)
            # Small inter-chunk delay to be gentle on yfinance even on success.
            if chunk_idx < n_chunks - 1:
                time.sleep(2)

    if not chunks:
        print(f"  [chunked] all {n_chunks} chunks failed", file=sys.stderr)
        return pd.DataFrame()

    # Concat along columns axis; pandas will align ticker MultiIndex correctly.
    try:
        combined = pd.concat(chunks, axis=1)
    except Exception as exc:
        print(f"  [chunked] concat failed: {exc}", file=sys.stderr)
        return pd.DataFrame()

    succeeded = len(tickers) - len(failed_tickers)
    print(
        f"  [chunked] Done: {succeeded}/{len(tickers)} tickers fetched "
        f"across {n_chunks} chunks (chunk_size={chunk_size})",
        file=sys.stderr,
    )
    return combined


def compute_yfinance_timing_fallback(
    missing_tickers: list[str],
    screener_data: dict[str, dict],
) -> dict[str, dict]:
    """Batch-fetch timing fields for DD tickers not in the screener universe.

    For dist_52w_high_pct / ma50_pct / vs_200ma_pct: computed directly from
    ~300d daily closes via yfinance.

    For rs_score: each missing ticker's r1w/r4w/r13w **raw % returns** are
    percentile-ranked against **raw % returns** from the full screener universe
    (~511 tickers), fetched via yfinance in the same batch.  This is
    methodologically correct — apples-to-apples raw vs raw — unlike the
    previous approach that mixed raw returns against screener's already-EMA-
    smoothed percentile-rank values (0-100 range vs -50/+50 range).

    No EMA smoothing is applied to fallback tickers (no prior history).
    Fallback tickers get timing_source="yfinance_fallback".

    TW/JP local listings are ranked against the same US universe by design
    (consistent methodology; FX noise documented in module docstring).

    Never raises — returns empty dict for tickers that yfinance fails on.
    """
    if not missing_tickers:
        return {}

    # Resolve yfinance tickers (EU suffix mapping) for missing DD tickers
    yf_map: dict[str, str] = {}  # dd_ticker -> yf_ticker
    for t in missing_tickers:
        yf_map[t] = _yf_ticker_for_ma(t)

    # Build full universe: screener tickers + missing DD tickers
    screener_tickers: list[str] = list(screener_data.keys())
    all_yf_tickers = list(set(list(yf_map.values()) + screener_tickers))
    print(
        f"  [fallback] Fetching {len(all_yf_tickers)} tickers "
        f"({len(screener_tickers)} screener universe + {len(yf_map)} missing) ...",
        file=sys.stderr,
    )

    # Chunked download with retry/backoff (added 2026-05-24).
    # Yahoo Finance tightened rate-limits in 2024-2025; a single batch of
    # 500+ tickers reliably trips YFRateLimitError, wiping the entire
    # timing column. Chunks of 50 with exponential backoff make the build
    # resilient without re-runs.
    raw = _chunked_download_with_retry(
        all_yf_tickers,
        period="300d",
        interval="1d",
        chunk_size=50,
        max_retries=3,
        backoff_seconds=(15, 60, 180),
    )
    if raw is None or raw.empty:
        print(f"  [fallback] yf.download returned empty after retries", file=sys.stderr)
        return {}

    # Helper: extract Close series for a yf ticker from the multi-ticker frame.
    # Captures `raw` (the yfinance DataFrame) and `all_yf_tickers` from enclosing scope.
    # IMPORTANT: never use `raw` as a local variable name in this function's outer
    # scope after this point — it would shadow the DataFrame for this closure.
    def _get_closes(yf_ticker: str) -> "pd.Series | None":
        try:
            if len(all_yf_tickers) == 1:
                # Single-ticker download returns flat columns
                closes = raw["Close"].dropna()
            else:
                # Multi-ticker: top level is ticker name
                closes = raw[yf_ticker]["Close"].dropna()
            if closes.empty:
                return None
            return closes
        except (KeyError, TypeError):
            return None

    # Compute raw returns for the full screener universe to use as reference population.
    # These are raw % returns (apples-to-apples with missing tickers' raw returns).
    ref_r1w: list[float] = []
    ref_r4w: list[float] = []
    ref_r13w: list[float] = []
    for sc_t in screener_tickers:
        closes = _get_closes(sc_t)
        if closes is None:
            continue
        v1 = _calc_return(closes, 5)
        v4 = _calc_return(closes, 21)
        v13 = _calc_return(closes, 63)
        if v1 is not None and v4 is not None and v13 is not None:
            ref_r1w.append(v1)
            ref_r4w.append(v4)
            ref_r13w.append(v13)
    print(
        f"  [fallback] Reference population: {len(ref_r1w)} tickers with full raw returns",
        file=sys.stderr,
    )

    # Compute raw returns for missing tickers
    missing_raw: dict[str, dict] = {}  # dd_ticker -> {r1w, r4w, r13w}
    for dd_t, yf_t in yf_map.items():
        closes = _get_closes(yf_t)
        if closes is None:
            continue
        r1w = _calc_return(closes, 5)
        r4w = _calc_return(closes, 21)
        r13w = _calc_return(closes, 63)
        if r1w is not None and r4w is not None and r13w is not None:
            missing_raw[dd_t] = {"r1w": r1w, "r4w": r4w, "r13w": r13w}

    # Combined reference population: screener universe raw returns + missing tickers' raw returns.
    # Both sides are now raw % returns — methodologically correct.
    all_r1w = ref_r1w + [v["r1w"] for v in missing_raw.values()]
    all_r4w = ref_r4w + [v["r4w"] for v in missing_raw.values()]
    all_r13w = ref_r13w + [v["r13w"] for v in missing_raw.values()]

    # Build output
    out: dict[str, dict] = {}
    for dd_t, yf_t in yf_map.items():
        closes = _get_closes(yf_t)
        timing: dict = {
            "dist_52w_high_pct": None,
            "ma50_pct": None,
            "vs_200ma_pct": None,
            "rs_score": None,
            "timing_source": "yfinance_fallback",
        }

        if closes is not None and len(closes) > 1:
            price = float(closes.iloc[-1])

            # dist_52w_high_pct: last close vs trailing 252-day max
            window = min(252, len(closes))
            high_52w = float(closes.iloc[-window:].max())
            if high_52w > 0:
                timing["dist_52w_high_pct"] = round((price / high_52w - 1) * 100, 1)

            # ma50_pct: last close vs 50-day SMA
            if len(closes) >= 50:
                ma50 = float(closes.iloc[-50:].mean())
                if ma50 > 0:
                    timing["ma50_pct"] = round((price / ma50 - 1) * 100, 1)

            # vs_200ma_pct: last close vs 200-day SMA
            if len(closes) >= 200:
                ma200 = float(closes.iloc[-200:].mean())
                if ma200 > 0:
                    timing["vs_200ma_pct"] = round((price / ma200 - 1) * 100, 1)

        # rs_score via percentile rank against combined population
        if dd_t in missing_raw and all_r1w:
            _raw_ret = missing_raw[dd_t]  # renamed to avoid shadowing outer `raw` DataFrame
            pr1w = _percentile_rank_value(_raw_ret["r1w"], all_r1w)
            pr4w = _percentile_rank_value(_raw_ret["r4w"], all_r4w)
            pr13w = _percentile_rank_value(_raw_ret["r13w"], all_r13w)
            # Persistence formula matches screener.py (no EMA — no prior history)
            persistence = pr1w * 0.2 + pr4w * 0.3 + pr13w * 0.5
            # Trend bonus (matches screener.py logic)
            if pr1w > pr4w > pr13w:
                bonus = 5.0
            elif pr1w >= pr4w >= pr13w:
                bonus = 2.0
            elif pr1w < pr4w < pr13w:
                bonus = -5.0
            else:
                bonus = 0.0
            timing["rs_score"] = round(min(100.0, persistence + bonus), 1)

        out[dd_t] = timing

    succeeded = sum(1 for v in out.values() if v.get("dist_52w_high_pct") is not None)
    print(f"  [fallback] Done: {succeeded}/{len(missing_tickers)} tickers got dist_52w_high_pct", file=sys.stderr)
    return out


def compute_daily_5y_highs(dd_tickers: list[str]) -> dict[str, dict]:
    """Batch-fetch 5y DAILY closes and compute true 5Y daily high per ticker.

    Returns {dd_ticker: {high_5y_daily_price, dist_5y_high_daily_pct, days_since_5y_high}}.
    Tickers yfinance can't fetch are omitted; merge code defaults them to None.

    Why this exists: dd_screener_ma.compute_ma_snapshot() pulls 5y WEEKLY closes
    (cached in data/weekly_cache/). Weekly highs compress intraweek peaks out and
    can be up to 7 days stale between Friday closes. For the ATH spotlight
    surfaced above the main table, we want today-fresh DAILY granularity over
    the same 5y window — meaningful "did this ticker just print a new ATH" vs.
    "what was Friday's peak weekly close."

    Cost: one chunked yf.download per build (~30-60s for 200 tickers, chunk_size=50).
    Reuses _chunked_download_with_retry() infrastructure so rate-limit handling
    matches the timing-fallback path.
    """
    if not dd_tickers:
        return {}

    yf_map: dict[str, str] = {t: _yf_ticker_for_ma(t) for t in dd_tickers}
    yf_tickers = list(set(yf_map.values()))
    print(
        f"  [daily-5y] Fetching {len(yf_tickers)} tickers (5y daily) for ATH high ...",
        file=sys.stderr,
    )
    raw = _chunked_download_with_retry(
        yf_tickers,
        period="5y",
        interval="1d",
        chunk_size=50,
        max_retries=3,
        backoff_seconds=(15, 60, 180),
    )
    if raw is None or raw.empty:
        print("  [daily-5y] yf.download returned empty after retries", file=sys.stderr)
        return {}

    def _get_closes(yf_ticker: str):
        try:
            if len(yf_tickers) == 1:
                s = raw["Close"].dropna()
            else:
                s = raw[yf_ticker]["Close"].dropna()
            return s if not s.empty else None
        except (KeyError, TypeError):
            return None

    out: dict[str, dict] = {}
    for dd_t, yf_t in yf_map.items():
        closes = _get_closes(yf_t)
        if closes is None or len(closes) < 50:
            continue
        try:
            high = float(closes.max())
            argmax = int(closes.values.argmax())
            last = float(closes.iloc[-1])
            if high <= 0:
                continue
            out[dd_t] = {
                "high_5y_daily_price": round(high, 2),
                "dist_5y_high_daily_pct": round((last - high) / high * 100, 2),
                "days_since_5y_high": len(closes) - argmax - 1,
            }
        except Exception:
            continue
    print(
        f"  [daily-5y] Computed for {len(out)}/{len(dd_tickers)} tickers",
        file=sys.stderr,
    )
    return out


def _ev5y_for(ticker: str, dca_ev_map: dict) -> float | None:
    """Resolve DCA §4 5Y EV → annualized IRR (%) for one ticker.

    `dca_ev_map` keys are filename-normalized (no dots, e.g. "2330TW"), so
    "2330.TW" must fall back to the dot-stripped form.
    """
    ev = dca_ev_map.get(ticker)
    if ev is None:
        ev = dca_ev_map.get(ticker.replace(".", ""))
    if ev is None:
        return None
    return round(compute_dca_irr(ev), 2)


def _moat_trend_for(ticker: str, dca_trend_map: dict, fallback: str) -> str:
    """Resolve moat trend arrow per DCA Phase A1; fallback when no DCA arrow.

    `dca_trend_map` keys are normalized (no dots, e.g. "2330TW").
    """
    arrow = dca_trend_map.get(ticker)
    if arrow is None:
        arrow = dca_trend_map.get(ticker.replace(".", ""))
    return arrow or fallback


def _fetch_live_fy_eps(
    yf_ticker: str,
    p_at_dd: float,
    fpe_fy2: float,
    excel_record: dict | None = None,
    dd_ticker: str | None = None,
) -> dict:
    """v1.7.1: fetch fresh FY EPS estimate from yfinance, auto-match the FY
    row that the DD anchored on, AND return raw 0y/+1y values + trailingEps
    for proper 2Y CAGR computation.

    v1.8: when `excel_record` is provided (Excel row for this ticker),
    override eps_0y_raw / eps_1y_raw with Excel values. yearAgoEps + trailingEps
    still come from yfinance (historical actual). FY-match (eps_now) is
    recomputed against Excel values. Adds Excel-only fields eps_fy3 +
    growth_fy1_fy2_pct + growth_fy2_fy3_pct + cagr_fy1_fy3_pct.

    DD label "FY+1" vs "FY+2" semantics vary by writer (some count from last
    fiscal year-end, some from current ongoing FY). Instead of guessing, we
    reverse-engineer the implied EPS at DD time (price_at_dd / fpe_fy2) and
    pick whichever yfinance annual row (0y / +1y) is closest. This works
    per-ticker without needing labels.

    2Y CAGR caveat (v1.7.2 fix): yfinance's "0y" and "+1y" rows are 1 year
    apart (current FY vs next FY). The proper 2Y CAGR end is +1y, but the
    base must be on the **same accounting basis** as the estimate (non-GAAP
    for SaaS analysts). info.trailingEps is GAAP TTM — for high-SBC names
    (DDOG, NET, CRWD, MDB, SNOW…) GAAP TTM ≪ non-GAAP forward, which inflates
    the CAGR by 5-10×. We now prefer earnings_estimate's "0y" yearAgoEps
    (last FY actual, same non-GAAP basis as the +1y estimate) and fall back
    to trailingEps only when yearAgoEps is missing.

    Returns dict with:
      live_fpe_real:    price_now / yf_eps_matched (None on failure)
      yf_fy_label:      "0y" | "+1y" — which yfinance row was matched
      eps_at_dd:        DD-implied EPS (price_at_dd / fpe_fy2)
      eps_now:          fresh consensus EPS for matched FY
      eps_revision_pct: (eps_now - eps_at_dd) / eps_at_dd × 100
      eps_0y_raw:       raw 0y avg EPS (current FY estimate) — kept for audit
      eps_1y_raw:       raw +1y avg EPS (next FY estimate) — used as CAGR end
      eps_year_ago:     0y.yearAgoEps (last FY actual, same basis as estimate)
      trailing_eps:     info.trailingEps — GAAP TTM fallback CAGR base
    """
    out = {
        "live_fpe_real": None,
        "yf_fy_label": None,
        "eps_at_dd": None,
        "eps_now": None,
        "eps_revision_pct": None,
        # v1.7: raw values for 2Y CAGR computation (independent of DD match)
        "eps_0y_raw": None,
        "eps_1y_raw": None,
        # v1.7.2: yearAgoEps — same-basis CAGR base (preferred over GAAP TTM)
        "eps_year_ago": None,
        # v1.7.1: trailing EPS — GAAP TTM fallback when yearAgoEps missing
        "trailing_eps": None,
        # v1.8: Excel-derived fields (None when no Excel record for ticker)
        "eps_fy3": None,
        "growth_fy1_fy2_pct": None,
        "growth_fy2_fy3_pct": None,
        "cagr_fy1_fy3_pct": None,
        "eps_source": "yfinance",
        # v1.8.2: True when Excel covers ticker AND yfinance.info.currency !=
        # info.financialCurrency (e.g., TSM ADR USD vs TWD-reported earnings).
        # When True, _compute_live_eps_cagr() switches eps2y_live to use Excel's
        # own forward CAGR (cagr_fy1_fy3_pct) to avoid FX-ratio nonsense.
        "currency_mismatch_xlsx_yf": False,
        # v1.8.5: foreign-listing native-currency display. For .TW/.T/.HK/.KS
        # tickers, Excel reports in USD but local investors think in TWD/JPY/etc.
        # We back-compute an implicit FX from yfinance (financialCurrency) ÷ Excel
        # (USD) for the same FY, then surface local-currency values for display.
        # ADRs (TSM/ASML/LVMH ADR forms) are NOT converted — ADR holders trade USD.
        "eps_display_currency": "USD",
        "eps_fx_rate": None,
        "eps_fy_curr_local": None,
        "eps_fy_next_local": None,
        "eps_fy3_local": None,
        "eps_fy_curr_usd_orig": None,  # original Excel USD value (audit)
        "eps_fy_next_usd_orig": None,
        "eps_fy3_usd_orig": None,
        # 2026-09-12: set only when excel_record went through apply_adr_ratio()
        # (data/adr_ratios.json 表列 ticker，如 TSM) — None for the vast majority
        # of tickers, matching every other field's "not applicable" default here.
        "eps_basis": None,
    }
    if not (p_at_dd and fpe_fy2 and p_at_dd > 0 and fpe_fy2 > 0):
        return out
    implied = p_at_dd / fpe_fy2
    out["eps_at_dd"] = round(implied, 4)

    # v1.8: Excel takes priority for FY1/FY2/FY3 + growth fields.
    # yearAgoEps + trailingEps still come from yfinance (historical actuals).
    if excel_record is not None:
        out["eps_source"] = "xlsx"
        out["eps_0y_raw"] = excel_record.get("fy1")
        out["eps_1y_raw"] = excel_record.get("fy2")
        out["eps_fy3"] = excel_record.get("fy3")
        out["growth_fy1_fy2_pct"] = excel_record.get("growth_fy1_fy2_pct")
        out["growth_fy2_fy3_pct"] = excel_record.get("growth_fy2_fy3_pct")
        out["cagr_fy1_fy3_pct"] = excel_record.get("cagr_fy1_fy3_pct")
        out["eps_basis"] = excel_record.get("eps_basis")
        # Fallback: compute growth/CAGR from FY1/FY2/FY3 when the Excel drops the
        # pre-computed columns (2026-06-23 Koyfin export left cols 5/6/7 blank for
        # the whole universe). Without this the xlsx_forward eps2y fallback and
        # live PEG go dark whenever yfinance is also rate-limited. Same formulas
        # as the yfinance-source path below (line ~1015).
        _xf1, _xf2, _xf3 = excel_record.get("fy1"), excel_record.get("fy2"), excel_record.get("fy3")
        if out["growth_fy1_fy2_pct"] is None and _xf1 and _xf2 and _xf1 > 0:
            out["growth_fy1_fy2_pct"] = round((_xf2 / _xf1 - 1) * 100, 4)
        if out["growth_fy2_fy3_pct"] is None and _xf2 and _xf3 and _xf2 > 0:
            out["growth_fy2_fy3_pct"] = round((_xf3 / _xf2 - 1) * 100, 4)
        if out["cagr_fy1_fy3_pct"] is None and _xf1 and _xf3 and _xf1 > 0 and _xf3 > 0:
            out["cagr_fy1_fy3_pct"] = round(((_xf3 / _xf1) ** 0.5 - 1) * 100, 4)

    # v1.8.1: ALWAYS fetch yfinance 0y/+1y into local vars (independent of Excel
    # override). Used for:
    #   (1) FY-match → eps_now → eps_revision_pct (vs DD-time anchor) — kept on
    #       yfinance baseline for backward compat with v1.7.x (consistent input
    #       to breakout / bottom-out scoring; avoids Excel-vs-yfinance consensus
    #       mean drift falsely showing as "EPS revision").
    #   (2) yearAgoEps (historical actual) — never overridden by Excel.
    #   Excel still overrides eps_0y_raw / eps_1y_raw / eps_fy3 / growth fields
    #   in `out` for DISPLAY purposes only.
    yf_eps_0y = None
    yf_eps_1y = None
    yf_eps_2y = None
    try:
        tk = yf.Ticker(yf_ticker)
        ee = tk.earnings_estimate
        if ee is None or getattr(ee, "empty", True):
            ee = None

        if ee is not None:
            # Always read yfinance 0y / +1y / +2y avg into a dict (audit baseline,
            # never overridden by Excel — used for FY-match below)
            _yf = {"0y": None, "+1y": None, "+2y": None}
            for row_label in _yf:
                try:
                    if row_label in ee.index:
                        val = ee.loc[row_label].get("avg")
                        if val is not None and float(val) > 0:
                            _yf[row_label] = round(float(val), 4)
                except Exception:
                    pass
            yf_eps_0y = _yf["0y"]
            yf_eps_1y = _yf["+1y"]
            yf_eps_2y = _yf["+2y"]

            # Populate display fields: Excel overrides win for eps_0y_raw / eps_1y_raw / eps_fy3
            if out["eps_source"] != "xlsx":
                # yfinance fallback path: copy yfinance locals into display fields
                out["eps_0y_raw"] = yf_eps_0y
                out["eps_1y_raw"] = yf_eps_1y
                if out["eps_fy3"] is None:
                    out["eps_fy3"] = yf_eps_2y
                # Compute growth/CAGR for yfinance-sourced rows
                _fy1 = out["eps_0y_raw"]
                _fy2 = out["eps_1y_raw"]
                _fy3 = out["eps_fy3"]
                if _fy1 and _fy2 and _fy1 > 0:
                    out["growth_fy1_fy2_pct"] = round((_fy2 / _fy1 - 1) * 100, 4)
                if _fy2 and _fy3 and _fy2 > 0:
                    out["growth_fy2_fy3_pct"] = round((_fy3 / _fy2 - 1) * 100, 4)
                if _fy1 and _fy3 and _fy1 > 0 and _fy3 > 0:
                    out["cagr_fy1_fy3_pct"] = round(((_fy3 / _fy1) ** 0.5 - 1) * 100, 4)
            # else: Excel already wrote eps_0y_raw / eps_1y_raw / eps_fy3 + growth/CAGR

            # yearAgoEps (always from yfinance — historical actual, never Excel)
            try:
                if "0y" in ee.index:
                    yag = ee.loc["0y"].get("yearAgoEps")
                    if yag is not None and float(yag) > 0:
                        out["eps_year_ago"] = round(float(yag), 4)
            except Exception:
                pass

        # trailingEps fallback (always yfinance) +
        # v1.8.3: for Excel-covered tickers, probe info.financialCurrency to
        # detect currency mismatch. Excel is *always* in USD (Koyfin export
        # convention), so any ticker whose yfinance financialCurrency ≠ USD
        # has its yearAgoEps in a foreign currency — dividing Excel USD by
        # foreign yearAgo gives FX-ratio nonsense. Covers BOTH:
        #   (a) ADRs where info.currency=USD but financialCurrency=EUR/TWD/CHF
        #       (TSM, ASML, ONON, SPOT)
        #   (b) Foreign local listings where both = TWD/JPY but Excel = USD
        #       (2330.TW, 2454.TW, 2308.TW, etc.)
        # Cost: ~134 extra info calls per build (cached client-side).
        need_info = (
            (out["eps_1y_raw"] is not None and out["eps_year_ago"] is None)
            or excel_record is not None
        )
        if need_info:
            try:
                info = tk.info
                trailing = info.get("trailingEps")
                if trailing is not None and float(trailing) > 0:
                    out["trailing_eps"] = round(float(trailing), 4)
                if excel_record is not None:
                    fc = info.get("financialCurrency")
                    if fc and fc.upper() != "USD":
                        out["currency_mismatch_xlsx_yf"] = True
            except Exception:
                pass

        # v1.8.1: FY-match against yfinance values (NOT Excel) so eps_revision_pct
        # remains apples-to-apples vs DD-time anchor (which was reverse-engineered
        # from frozen price_at_dd / fpe_fy2 — typically anchored on yfinance-era
        # consensus). Mixing Excel (Koyfin-source) consensus with yfinance-anchored
        # DD value introduces ~1-4pp systematic bias that misleads breakout /
        # bottom-out scoring (real-world: 5 ticker demoted out of breakout tier_a).
        best = None
        candidates = [("0y", yf_eps_0y), ("+1y", yf_eps_1y)]
        for row_label, eps in candidates:
            if eps and eps > 0:
                err = abs(eps - implied) / implied
                if best is None or err < best[1]:
                    best = (row_label, err, float(eps))
        if best is None:
            return out
        if best[1] > 0.30:
            return out
        out["yf_fy_label"] = best[0]
        out["eps_now"] = round(best[2], 4)
        out["eps_revision_pct"] = round((best[2] - implied) / implied * 100, 1)
    except Exception:
        pass

    # v1.8.5: foreign-listing native-currency conversion.
    # For .TW/.T/.HK/.KS/.SS/.SZ tickers: Excel reports USD per ord share but
    # local investors think in TWD/JPY/HKD/KRW/etc. Back-compute implicit FX
    # using yfinance native value (in financialCurrency) vs Excel USD value
    # for the same FY (typically FY+1, the "0y" row). Then convert FY1/FY2/FY3.
    # ADRs (no foreign suffix on DD ticker) are skipped — USD is the natural unit.
    _FOREIGN_SUFFIXES_DISPLAY = (".TW", ".T", ".HK", ".KS", ".KQ", ".SS", ".SZ", ".JP")
    if (
        excel_record is not None
        and dd_ticker
        and any(dd_ticker.endswith(s) for s in _FOREIGN_SUFFIXES_DISPLAY)
    ):
        # FX = yfinance native (financialCurrency) ÷ Excel USD, for "0y" FY
        # Prefer yf_eps_0y / excel.fy1; fall back to yf_eps_1y / excel.fy2 if 0y unavailable.
        xlsx_usd_fy1 = excel_record.get("fy1")
        xlsx_usd_fy2 = excel_record.get("fy2")
        xlsx_usd_fy3 = excel_record.get("fy3")
        fx = None
        if yf_eps_0y and xlsx_usd_fy1 and xlsx_usd_fy1 > 0:
            fx = yf_eps_0y / xlsx_usd_fy1
        elif yf_eps_1y and xlsx_usd_fy2 and xlsx_usd_fy2 > 0:
            fx = yf_eps_1y / xlsx_usd_fy2
        # Fallback: yfinance.info.epsCurrentYear / forwardEps (separate endpoint
        # bucket — survives earnings_estimate rate-limit). Both are in local
        # currency (financialCurrency). epsCurrentYear matches Excel fy1 semantics
        # most closely; forwardEps is NTM and slightly biased toward fy2.
        if (not fx or fx <= 0) and xlsx_usd_fy1 and xlsx_usd_fy1 > 0:
            try:
                _info = yf.Ticker(yf_ticker).info
                _eps_cy = _info.get("epsCurrentYear")
                _eps_fw = _info.get("forwardEps")
                if _eps_cy and float(_eps_cy) > 0:
                    fx = float(_eps_cy) / xlsx_usd_fy1
                elif _eps_fw and float(_eps_fw) > 0:
                    fx = float(_eps_fw) / xlsx_usd_fy1
            except Exception:
                pass
        if fx and fx > 0:
            # Try to read financialCurrency from yfinance info (typically already
            # fetched above for currency_mismatch detection; this is best-effort).
            local_ccy = None
            try:
                local_ccy = yf.Ticker(yf_ticker).info.get("financialCurrency")
            except Exception:
                pass
            if not local_ccy:
                # Suffix-based default (covers most cases without an extra API call)
                local_ccy = {
                    ".TW": "TWD", ".T": "JPY", ".JP": "JPY",
                    ".HK": "HKD", ".KS": "KRW", ".KQ": "KRW",
                    ".SS": "CNY", ".SZ": "CNY",
                }.get(next(s for s in _FOREIGN_SUFFIXES_DISPLAY if dd_ticker.endswith(s)), "USD")
            out["eps_display_currency"] = local_ccy
            out["eps_fx_rate"] = round(float(fx), 4)
            # Stash USD originals (audit) before overwriting display fields
            out["eps_fy_curr_usd_orig"] = xlsx_usd_fy1
            out["eps_fy_next_usd_orig"] = xlsx_usd_fy2
            out["eps_fy3_usd_orig"] = xlsx_usd_fy3
            # Compute local-currency values
            if xlsx_usd_fy1 is not None:
                out["eps_fy_curr_local"] = round(xlsx_usd_fy1 * fx, 2)
            if xlsx_usd_fy2 is not None:
                out["eps_fy_next_local"] = round(xlsx_usd_fy2 * fx, 2)
            if xlsx_usd_fy3 is not None:
                out["eps_fy3_local"] = round(xlsx_usd_fy3 * fx, 2)
            # OVERWRITE display fields with local-currency values so downstream
            # (latest.json + UI) consistently shows TWD/JPY/etc. for foreign listings.
            # Growth/CAGR percentages are currency-agnostic — leave unchanged.
            if out["eps_fy_curr_local"] is not None:
                out["eps_0y_raw"] = out["eps_fy_curr_local"]
            if out["eps_fy_next_local"] is not None:
                out["eps_1y_raw"] = out["eps_fy_next_local"]
            if out["eps_fy3_local"] is not None:
                out["eps_fy3"] = out["eps_fy3_local"]

    return out


def _compute_live_pe_drift(
    entry: dict, ma: dict, live_fy_result: dict | None = None
) -> dict:
    """Compute live FwdPE — preferring fresh yfinance EPS over price-drift heuristic.

    Primary path (v1.6): live_fpe_real = price_now / yfinance FY EPS estimate
      Captures both price drift AND analyst EPS revisions since DD. Auto-matches
      the right FY row by implied EPS (DD writers use FY+1 vs FY+2 differently).

    Fallback path (v1.3): live_fpe_heur = fpe_fy2 × (price_now / price_at_dd)
      Assumes EPS unchanged since DD. Used when yfinance has no earnings_estimate
      or the match is off (BESI etc).

    v1.7: accepts optional pre-fetched `live_fy_result` to avoid duplicate
    yfinance calls when enrich_ticker also needs eps_0y_raw / eps_1y_raw.
    If not provided, calls _fetch_live_fy_eps() internally (backward-compat).

    Returns dict with:
      live_fpe_est: live FwdPE (real if matched, heuristic otherwise), None if inputs missing
      pe_drift_pct: % change from DD-time fpe_fy2 (combines price drift + EPS revision when method=eps)
      dd_age_days: days since DD write date
      live_pct_5y_est: heuristic current 5Y FwdPE percentile (60% relative range)
      live_fpe_method: "eps" (real path) | "drift" (heuristic) | None
      eps_revision_pct: % change in FY EPS estimate since DD (only when method=eps)
      yf_fy_label: "0y" | "+1y" — which yfinance row was matched (only when method=eps)
    """
    out = {
        "live_fpe_est": None,
        "pe_drift_pct": None,
        "dd_age_days": None,
        "live_pct_5y_est": None,
        "live_fpe_method": None,
        "eps_revision_pct": None,
        "yf_fy_label": None,
    }
    fpe = entry.get("fpe_fy2")
    p_dd = entry.get("price_at_dd")
    p_now = ma.get("price") if ma else None
    pct_5y = entry.get("pct_5y")
    dd_date = entry.get("dd_date")

    if dd_date:
        try:
            d = datetime.strptime(dd_date, "%Y-%m-%d").date()
            out["dd_age_days"] = (datetime.now().date() - d).days
        except (TypeError, ValueError):
            pass

    if fpe is None or p_dd is None or p_now is None or p_dd <= 0 or fpe <= 0:
        return out

    # Primary: real EPS path — use pre-fetched result if provided (v1.7 no-dupe)
    real = live_fy_result if live_fy_result is not None else _fetch_live_fy_eps(
        _yf_ticker_for_ma(entry["ticker"]), p_dd, fpe
    )
    if real["eps_now"] is not None and real["eps_now"] > 0:
        out["live_fpe_est"] = round(p_now / real["eps_now"], 2)
        out["pe_drift_pct"] = round((out["live_fpe_est"] / fpe - 1) * 100, 1)
        out["live_fpe_method"] = "eps"
        out["eps_revision_pct"] = real["eps_revision_pct"]
        out["yf_fy_label"] = real["yf_fy_label"]
    else:
        # Fallback: price-drift heuristic
        drift_factor = p_now / p_dd
        out["live_fpe_est"] = round(fpe * drift_factor, 2)
        out["pe_drift_pct"] = round((drift_factor - 1) * 100, 1)
        out["live_fpe_method"] = "drift"

    # Heuristic live pct_5y: assume the 5Y FwdPE range has relative width ~60%
    # centered on fpe_dd, so [low, high] = [fpe·(1−0.6·pct/100), fpe·(1+0.6·(1−pct/100))].
    # Then live_pct_5y = (live_fpe − low) / (high − low) × 100, clamped [0, 100].
    # Caveat: cyclicals / high-growth stocks have much wider ranges.
    if pct_5y is not None and 0 <= pct_5y <= 100:
        REL_WIDTH = 0.6
        low = fpe * (1 - REL_WIDTH * pct_5y / 100)
        high = fpe * (1 + REL_WIDTH * (100 - pct_5y) / 100)
        if high > low:
            live_pct = (out["live_fpe_est"] - low) / (high - low) * 100
            out["live_pct_5y_est"] = round(max(0, min(100, live_pct)), 1)
    return out


# ---------------------------------------------------------------------------
# EPS 2Y CAGR live compute helpers (v1.7 — EPS revision momentum)
# ---------------------------------------------------------------------------

def _compute_live_eps_cagr(entry: dict, live_fy_result: dict) -> dict:
    """Compute live 2Y EPS CAGR from yfinance earnings_estimate.

    v1.7.2 fix: prior trailingEps-based formula mixed GAAP TTM (denominator)
    with non-GAAP forward estimate (numerator) for high-SBC SaaS names,
    inflating CAGR 5-10× (DDOG observed at 170% vs DD 17.8%). Now prefers
    0y.yearAgoEps — the last FY actual on the same accounting basis as the
    analysts' forward estimate — and falls back to trailingEps only when
    yearAgoEps is missing.

    Formula:
      base = eps_year_ago (preferred) or trailing_eps (fallback)
      cagr = ((eps_+1y / base) ** 0.5 - 1) * 100

    v1.8.2 fix: for Excel-covered ADRs whose ADR currency differs from yfinance
    financialCurrency (TSM USD vs TWD, ASML/SPOT USD vs EUR, ONON USD vs CHF),
    dividing Excel FY+1 (USD) by yfinance yearAgoEps (foreign currency) gives
    FX-ratio nonsense (TSM observed −39.8% vs Excel forward CAGR +25%). When
    `currency_mismatch_xlsx_yf` flag is set upstream, switch to Excel's own
    `cagr_fy1_fy3_pct` (FY+1 → FY+3 forward 2Y CAGR — currency-safe).

    Writes:
      eps2y_live:         live 2Y EPS CAGR % (None on failure)
      eps2y_live_method:  "yearago" (yearAgoEps + +1y, same-basis, preferred)
                          | "xlsx_forward" (Excel FY+1→FY+3 — ADR currency-mismatch path)
                          | "trailing" (trailingEps + +1y, GAAP/non-GAAP risk)
                          | "missing"
    """
    eps_1y = live_fy_result.get("eps_1y_raw")
    year_ago = live_fy_result.get("eps_year_ago")
    trailing = live_fy_result.get("trailing_eps")
    currency_mismatch = live_fy_result.get("currency_mismatch_xlsx_yf", False)
    xlsx_forward_cagr = live_fy_result.get("cagr_fy1_fy3_pct")

    # v1.8.2: ADR currency-mismatch path — use Excel's own forward CAGR
    if currency_mismatch and xlsx_forward_cagr is not None:
        return {
            "eps2y_live": round(float(xlsx_forward_cagr), 2),
            "eps2y_live_method": "xlsx_forward",
        }

    if eps_1y is not None and year_ago is not None and year_ago > 0 and eps_1y > 0:
        cagr = ((eps_1y / year_ago) ** 0.5 - 1) * 100
        return {
            "eps2y_live": round(cagr, 2),
            "eps2y_live_method": "yearago",
        }
    if eps_1y is not None and trailing is not None and trailing > 0 and eps_1y > 0:
        cagr = ((eps_1y / trailing) ** 0.5 - 1) * 100
        return {
            "eps2y_live": round(cagr, 2),
            "eps2y_live_method": "trailing",
        }
    # v1.8.4: last-resort — Excel covers the ticker but yfinance returned no
    # earnings_estimate / info (e.g., LVMH ticker not in yfinance; LVMUY would
    # be). With no yearAgoEps available we can't compute the anchored CAGR,
    # but Excel's own forward CAGR is still currency-safe and usable.
    if xlsx_forward_cagr is not None:
        return {
            "eps2y_live": round(float(xlsx_forward_cagr), 2),
            "eps2y_live_method": "xlsx_forward",
        }
    return {
        "eps2y_live": None,
        "eps2y_live_method": "missing",
    }


# Module-level cache: avoid re-reading snapshot file on every per-ticker call.
_PREV_MONTH_SNAPSHOT_CACHE: dict = {}
_PREV_MONTH_SNAPSHOT_LOADED: bool = False


def _load_prev_month_snapshot() -> dict:
    """Load the previous EPS snapshot used as baseline for revision computation.

    Lookup order:
      1. Intra-month dated baseline within current Excel's month:
         eps-estimates-snapshots/{YYYY-MM}-DD.json with DD < current Excel date.
         Picks the most recent one — supports multiple intra-month refreshes
         (e.g. 5/20 Excel then 5/25 Excel: 5/25 build compares vs 5/20).
      2. Existing month-back fallback: 1 then 2 months back from wall clock,
         {YYYY-MM}.json (canonical month-end snapshot).
    Returns the full snapshot dict (with "tickers" key), or {} if not found.
    Cached at module level so subsequent per-ticker calls don't re-read disk.
    """
    global _PREV_MONTH_SNAPSHOT_CACHE, _PREV_MONTH_SNAPSHOT_LOADED
    if _PREV_MONTH_SNAPSHOT_LOADED:
        return _PREV_MONTH_SNAPSHOT_CACHE

    _PREV_MONTH_SNAPSHOT_LOADED = True
    snapshot_dir = ROOT / "docs" / "dd-screener" / "eps-estimates-snapshots"

    # Step 1: intra-month dated baseline. Derive current Excel snapshot date
    # from data/eps-estimates/ filename (DD_universe_EPS_estimates_YYYYMMDD.xlsx).
    try:
        latest_xlsx = find_latest_excel()
    except Exception:
        latest_xlsx = None
    if latest_xlsx is not None:
        import re
        m = re.search(r"_(\d{4})(\d{2})(\d{2})\.xlsx$", latest_xlsx.name)
        if m:
            cy, cm, cd = m.group(1), m.group(2), m.group(3)
            current_date_iso = f"{cy}-{cm}-{cd}"
            current_month = f"{cy}-{cm}"
            # Find dated baselines in the same month, strictly older
            dated_re = re.compile(rf"^{current_month}-(\d{{2}})\.json$")
            candidates = []
            if snapshot_dir.exists():
                for p in snapshot_dir.iterdir():
                    mm = dated_re.match(p.name)
                    if mm and mm.group(1) < cd:
                        candidates.append(p)
            if candidates:
                pick = sorted(candidates, key=lambda p: p.name)[-1]
                try:
                    data = json.loads(pick.read_text(encoding="utf-8"))
                    _PREV_MONTH_SNAPSHOT_CACHE = data
                    print(f"  EPS baseline: intra-month {pick.name} "
                          f"(current Excel {current_date_iso})", file=sys.stderr)
                    return _PREV_MONTH_SNAPSHOT_CACHE
                except Exception as exc:
                    print(f"  WARN: failed to load intra-month baseline {pick}: {exc}",
                          file=sys.stderr)

    # Step 2: existing month-back fallback
    now = datetime.now(timezone(timedelta(hours=8)))  # Taipei TZ
    for months_back in (1, 2):
        # Compute YYYY-MM for (now - N months)
        m = now.month - months_back
        y = now.year
        while m <= 0:
            m += 12
            y -= 1
        candidate = snapshot_dir / f"{y:04d}-{m:02d}.json"
        if candidate.exists():
            try:
                data = json.loads(candidate.read_text(encoding="utf-8"))
                _PREV_MONTH_SNAPSHOT_CACHE = data
                return _PREV_MONTH_SNAPSHOT_CACHE
            except Exception as exc:
                print(f"  WARN: failed to load EPS snapshot {candidate}: {exc}", file=sys.stderr)

    _PREV_MONTH_SNAPSHOT_CACHE = {}
    return _PREV_MONTH_SNAPSHOT_CACHE


# Module-level cache for the v4 席位引擎 3-month revision baseline (see
# _load_eps_rev_3m_baseline()) — same pattern as _PREV_MONTH_SNAPSHOT_CACHE.
_EPS_REV_3M_BASELINE_CACHE: dict = {}
_EPS_REV_3M_BASELINE_LOADED: bool = False


def _load_eps_rev_3m_baseline() -> dict:
    """v4 席位引擎 (2026-09-17): load the canonical monthly EPS snapshot closest
    to 90 days before the current Excel snapshot date — baseline for
    `eps_rev_3m_pct` (own_score v4 revision percentile input, see
    knowledge/rule_ledger.md v4 席位引擎列). Only considers canonical
    month-end snapshots (`{YYYY-MM}.json`), not intra-month dated refreshes
    (`{YYYY-MM}-DD.json`) — a "3-month-ago roster", not "last refresh before
    today". Cached at module level, same pattern as _load_prev_month_snapshot().
    Returns the full snapshot dict (with "tickers" key), or {} if none found.
    """
    global _EPS_REV_3M_BASELINE_CACHE, _EPS_REV_3M_BASELINE_LOADED
    if _EPS_REV_3M_BASELINE_LOADED:
        return _EPS_REV_3M_BASELINE_CACHE
    _EPS_REV_3M_BASELINE_LOADED = True
    snapshot_dir = ROOT / "docs" / "dd-screener" / "eps-estimates-snapshots"

    import re

    try:
        latest_xlsx = find_latest_excel()
    except Exception:
        latest_xlsx = None
    current_date = None
    if latest_xlsx is not None:
        m = re.search(r"_(\d{4})(\d{2})(\d{2})\.xlsx$", latest_xlsx.name)
        if m:
            try:
                current_date = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date()
            except ValueError:
                current_date = None
    if current_date is None:
        current_date = datetime.now(timezone(timedelta(hours=8))).date()
    target = current_date - timedelta(days=90)

    canonical_re = re.compile(r"^(\d{4})-(\d{2})\.json$")
    best_path, best_diff, best_data = None, None, None
    if snapshot_dir.exists():
        for p in snapshot_dir.iterdir():
            if not canonical_re.match(p.name):
                continue
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            sd = data.get("snapshot_date")
            if not sd:
                continue
            try:
                sd_date = datetime.strptime(sd, "%Y-%m-%d").date()
            except ValueError:
                continue
            diff = abs((sd_date - target).days)
            if best_diff is None or diff < best_diff:
                best_diff, best_path, best_data = diff, p, data

    if best_path is not None:
        _EPS_REV_3M_BASELINE_CACHE = best_data
        print(f"  EPS 3m-revision baseline: {best_path.name} "
              f"(snapshot {best_data.get('snapshot_date')}, target ~{target.isoformat()})",
              file=sys.stderr)
    return _EPS_REV_3M_BASELINE_CACHE


def _compute_eps_revision(entry: dict, eps2y_live: float | None, prev_snapshot: dict) -> dict:
    """Compute EPS revision momentum vs last month's snapshot.

    revision_dir:
      "新增"  — ticker not in last month's snapshot (new to universe or snapshot missing)
      "持平"  — |revision_pp| < 0.5pp
      "上修"  — revision_pp > 0
      "下修"  — revision_pp < 0

    Writes:
      eps2y_prev_month:      last month's eps_cagr_2y value (float or None)
      eps2y_prev_month_date: month key string e.g. "2026-05" (or None)
      eps2y_revision_pp:     eps2y_live - eps2y_prev_month (float or None)
      eps2y_revision_dir:    "新增" | "持平" | "上修" | "下修" | None
    """
    ticker = entry.get("ticker")
    out = {
        "eps2y_prev_month": None,
        "eps2y_prev_month_date": None,
        "eps2y_revision_pp": None,
        "eps2y_revision_dir": None,
    }

    if eps2y_live is None:
        # Can't compute revision without live value
        return out

    if not prev_snapshot:
        # No snapshot at all — can't classify
        return out

    for_month = prev_snapshot.get("for_month")
    prev_tickers = prev_snapshot.get("tickers") or {}
    prev_row = prev_tickers.get(ticker)

    if prev_row is None:
        out["eps2y_revision_dir"] = "新增"
        out["eps2y_prev_month_date"] = for_month
        return out

    prev_cagr = prev_row.get("eps_cagr_2y")
    out["eps2y_prev_month_date"] = for_month

    if prev_cagr is None:
        out["eps2y_revision_dir"] = "新增"
        return out

    out["eps2y_prev_month"] = prev_cagr
    pp = eps2y_live - prev_cagr
    out["eps2y_revision_pp"] = round(pp, 2)

    if abs(pp) < 0.5:
        out["eps2y_revision_dir"] = "持平"
    elif pp > 0:
        out["eps2y_revision_dir"] = "上修"
    else:
        out["eps2y_revision_dir"] = "下修"

    return out


def _compute_live_peg(pe_drift: dict, eps2y_live: float | None,
                       live_fy_result: dict | None = None) -> dict:
    """Derive live PEG from live_fpe_est / CAGR.

    v1.10: prefer Excel pure-forward CAGR (eps_fy1_fy3_cagr_pct, what the UI's
    "CAGR" column displays) over eps2y_live (yfinance yearAgo→FY+1, basis
    can mix GAAP TTM with non-GAAP forward → fake-low PEG for SBC-heavy SaaS).
    CDNS observed: eps_fy1_fy3_cagr_pct=17.15, eps2y_live=52.0 → old PEG
    39.83/52 = 0.77 (misleading), new PEG 39.83/17.15 = 2.32 (realistic).

    Falls back to eps2y_live only when Excel CAGR is unavailable
    (FY1 negative for NBIS/CRWV/NVTS; yfinance-only tickers like 6857.T).

    pe_drift: the dict returned by _compute_live_pe_drift() (contains live_fpe_est).
    live_fy_result: dict returned by _fetch_live_fy_eps() (contains cagr_fy1_fy3_pct).

    Writes:
      live_peg: live PEG ratio (None if FPE or CAGR is missing/≤ 0)
    """
    fpe = pe_drift.get("live_fpe_est")
    excel_cagr = (live_fy_result or {}).get("cagr_fy1_fy3_pct")
    cagr = excel_cagr if excel_cagr is not None else eps2y_live
    if fpe and cagr and fpe > 0 and cagr > 0:
        return {"live_peg": round(fpe / cagr, 2)}
    return {"live_peg": None}


def _compute_live_ev5y(entry: dict, ma: dict) -> dict:
    """Heuristic live 5Y IRR, adjusting for price drift since DD.

    Formula (heuristic — terminal value assumed unchanged):
      live_ev5y = ((1 + ev5y_pct/100) * (price_at_dd / price_now) ** (1/5) - 1) * 100

    This approximates: if price rose but terminal value (EV at year 5) stayed
    the same, the annualized IRR from current price is lower.

    Writes:
      live_ev5y_pct:    adjusted 5Y annualized IRR % (None if inputs missing)
      live_ev5y_method: "heur" (always; indicates heuristic, not re-modelled)
    """
    ev5y = entry.get("ev5y_pct")
    p_dd = entry.get("price_at_dd")
    p_now = ma.get("price") if ma else None

    if ev5y is not None and p_dd and p_now and p_dd > 0 and p_now > 0:
        adj = ((1 + ev5y / 100) * (p_dd / p_now) ** 0.2 - 1) * 100
        return {
            "live_ev5y_pct": round(adj, 2),
            "live_ev5y_method": "heur",
        }
    return {
        "live_ev5y_pct": None,
        "live_ev5y_method": None,
    }


def compute_asym_flag(row: dict) -> str | None:
    """正不對稱三級標記（◆ 好球帶／★★／★）— 純下游機械描述器，非裁決。

    單一權威實作。全部從既有欄位機械算，現價重算值優先：
      ar_live         — 現價重算的不對稱比（§11.5 asymmetry ratio at today's price）
      live_ev5y_pct   — 現價重算的 5Y 年化 IRR %（本檔已是年化，非累積 EV；
                        源自 _ev5y_for→compute_dca_irr 已年化，再經 _compute_live_ev5y
                        依股價漂移重新年化，值域 13-18 即年化 IRR，直接用）
      trap / moat_trend / dca_verdict / dd_age_days — dd-meta 決策層欄位

    三級門檻（PREREG 凍結至 2026-10；見 knowledge/rule_ledger.md）：
      ◆（好球帶·重壓複審候選）: ar_live≥9 且 liveIRR≥13 且 trap=🟢
                                 且 moat_trend≠↓ 且 dca_verdict=進場 且報告齡≤90 天
      ★★（乾淨不對稱）        : ar_live≥6 且 liveIRR≥12 且 trap=🟢 且 moat_trend≠↓
      ★（不對稱但陷阱疑慮未決）: ar_live≥4 且 liveIRR≥10 且 trap≠🔴 且 moat_trend≠↓

    取最高符合級。判定欄位（ar_live/liveIRR/trap/moat_trend）缺任一 → 無標記（None）。
    描述器非加倉指令：只描述現價下的不對稱狀態，不下買賣單。
    """
    ar = row.get("ar_live")
    irr = row.get("live_ev5y_pct")
    trap = row.get("trap")
    moat_trend = row.get("moat_trend")
    # 判定欄位缺任一 → 無標記
    if ar is None or irr is None or trap is None or moat_trend is None:
        return None
    if moat_trend == "↓":
        return None
    verdict = row.get("dca_verdict")
    age = row.get("dd_age_days")
    # ◆ 好球帶（最嚴）
    if (ar >= 9 and irr >= 13 and trap == "🟢"
            and verdict == "進場"
            and age is not None and age <= 90):
        return "◆"
    # ★★ 乾淨不對稱
    if ar >= 6 and irr >= 12 and trap == "🟢":
        return "★★"
    # ★ 不對稱但陷阱疑慮未決
    if ar >= 4 and irr >= 10 and trap != "🔴":
        return "★"
    return None


def _compute_fy_eps_revision(ticker: str, yf_ticker: str, eps_curr: float | None,
                              eps_next: float | None, eps_fy3: float | None,
                              prev_snapshot: dict, current_snapshot_date: str | None,
                              reporting_ccy_cache: dict, fx_cache: dict) -> dict:
    """Compute period-over-period FY1 / FY2 / FY3 EPS revision % vs prev snapshot.

    2026-09-17: two fixes on top of the plain (eps_curr/prev_curr - 1) ratio:

      1. ADR ratio — baseline snapshots (docs/dd-screener/eps-estimates-
         snapshots/*.json, written by snapshot_eps_estimates.py) always store
         raw Koyfin ordinary-share EPS, never ADR-adjusted, whereas `eps_curr`
         /`eps_next`/`eps_fy3` here already went through apply_adr_ratio() at
         the call site (build_dd_screener.py's excel_record). Re-apply the
         same ratio to the baseline row so e.g. TSM's 3.40/4.49/5.70 baseline
         is compared against its own ADR basis (17.0/22.45/28.5), not against
         the current ADR-adjusted value (which made TSM show a fake +397%).
      2. FX normalization — both snapshots' EPS are USD-converted by Koyfin at
         each export's own FX rate, so a non-USD reporter (ASML/EUR,
         2330.TW/TWD, RACE/EUR, ...) shows a fake revision whenever the FX
         rate moved between the two dates. Compare in the reporting currency
         instead (see eps_fx_normalize.py); falls back to the raw USD ratio
         (flagged via eps_revision_fx_normalized=False) when the reporting
         currency or either day's FX rate can't be resolved.

    Returns dict with eps_fy_curr_revision_pct, eps_fy_next_revision_pct,
    eps_fy3_revision_pct, eps_revision_baseline_date, eps_revision_currency,
    eps_revision_fx_normalized. Revision % values are None when previous
    snapshot is missing or ticker wasn't in prior snapshot (new addition).
    """
    out = {
        "eps_fy_curr_revision_pct": None,
        "eps_fy_next_revision_pct": None,
        "eps_fy3_revision_pct": None,
        "eps_revision_baseline_date": None,
        "eps_revision_currency": None,
        "eps_revision_fx_normalized": None,
    }
    if not prev_snapshot:
        return out
    prev_tickers = prev_snapshot.get("tickers") or {}
    prev_row = prev_tickers.get(ticker)
    baseline_date = prev_snapshot.get("snapshot_date") or prev_snapshot.get("for_month")
    out["eps_revision_baseline_date"] = baseline_date
    if prev_row is None:
        return out
    prev_curr_raw = prev_row.get("eps_fy_curr") or prev_row.get("eps_0y")
    prev_next_raw = prev_row.get("eps_fy_next") or prev_row.get("eps_1y")
    prev_fy3_raw = prev_row.get("eps_fy3")
    # Fix 1: ADR-adjust the baseline the same way the current side already was.
    _prev_adr = apply_adr_ratio(ticker, {"fy1": prev_curr_raw, "fy2": prev_next_raw,
                                          "fy3": prev_fy3_raw})
    prev_curr = _prev_adr.get("fy1")
    prev_next = _prev_adr.get("fy2")
    prev_fy3 = _prev_adr.get("fy3")

    # Fix 2: FX-normalize to the reporting currency. Resolved once per ticker
    # (same currency/dates for all three FY buckets).
    currency = get_reporting_currency(ticker, yf_ticker, reporting_ccy_cache)
    fx_current = fx_baseline = None
    if currency and currency.upper() != "USD":
        # Prefer the baseline snapshot's own stored rate (fx_local_per_usd,
        # written by snapshot_eps_estimates.py from 2026-09 onward) over a
        # fresh history lookup — deterministic, and the correct "as of that
        # export" rate rather than whatever a later re-derivation would find.
        fx_baseline = (prev_snapshot.get("fx_local_per_usd") or {}).get(currency)
        if fx_baseline is None and baseline_date:
            fx_baseline = get_fx_rate(currency, baseline_date, fx_cache)
        if current_snapshot_date:
            fx_current = get_fx_rate(currency, current_snapshot_date, fx_cache)

    fx_normalized_flags = []
    for cur_val, prev_val, out_key in (
        (eps_curr, prev_curr, "eps_fy_curr_revision_pct"),
        (eps_next, prev_next, "eps_fy_next_revision_pct"),
        (eps_fy3, prev_fy3, "eps_fy3_revision_pct"),
    ):
        if not cur_val or not prev_val or prev_val <= 0:
            continue
        pct, normalized = compute_fx_normalized_revision(
            cur_val, prev_val, currency, fx_current, fx_baseline
        )
        if pct is not None:
            out[out_key] = round(pct, 2)
            fx_normalized_flags.append(normalized)

    out["eps_revision_currency"] = currency
    if fx_normalized_flags:
        out["eps_revision_fx_normalized"] = all(fx_normalized_flags)
    return out


# FY weights for eps_rev_3m_pct — see _compute_eps_rev_3m() (v4 席位引擎, 2026-09-17).
EPS_REV_3M_FY_WEIGHTS = {
    "eps_fy_curr_revision_pct": 0.2,
    "eps_fy_next_revision_pct": 0.3,
    "eps_fy3_revision_pct": 0.5,
}


def _compute_eps_rev_3m(ticker: str, yf_ticker: str, eps_curr: float | None,
                         eps_next: float | None, eps_fy3: float | None,
                         baseline_snapshot: dict, current_snapshot_date: str | None,
                         reporting_ccy_cache: dict, fx_cache: dict) -> dict:
    """v4 席位引擎 (2026-09-17): FY-weighted (0.2/0.3/0.5) FX-normalized EPS
    revision of the current xlsx vs a ~90-day-back monthly baseline (see
    _load_eps_rev_3m_baseline()) — own_score v4's revision percentile input
    (knowledge/rule_ledger.md v4 席位引擎列). Reuses _compute_fy_eps_revision()
    verbatim (same ADR-adjust + eps_fx_normalize machinery) against the 3m
    baseline instead of the 1-month-back one, then folds the three per-FY
    revision %s into a single weighted number — same weights available
    renormalize (e.g. FY3 missing → weight over FY1/FY2 only).

    Returns eps_rev_3m_pct / eps_rev_3m_baseline_date / eps_rev_3m_fx_normalized.
    All None when the baseline snapshot lacks the ticker (see
    _compute_fy_eps_revision's own prev_row is None short-circuit).
    """
    rev = _compute_fy_eps_revision(
        ticker, yf_ticker, eps_curr, eps_next, eps_fy3, baseline_snapshot,
        current_snapshot_date, reporting_ccy_cache, fx_cache,
    )
    parts, weight_sum = [], 0.0
    for key, w in EPS_REV_3M_FY_WEIGHTS.items():
        v = rev.get(key)
        if v is not None:
            parts.append(v * w)
            weight_sum += w
    eps_rev_3m_pct = round(sum(parts) / weight_sum, 2) if weight_sum > 0 else None
    return {
        "eps_rev_3m_pct": eps_rev_3m_pct,
        "eps_rev_3m_baseline_date": rev.get("eps_revision_baseline_date"),
        "eps_rev_3m_fx_normalized": rev.get("eps_revision_fx_normalized"),
    }


# 2026-09-16: default effective tax rate used whenever the xlsx "Tax Rate %"
# column is blank or outside the 0..50 sanity band (see compute_roic_decomposition).
ROIC_DECOMP_DEFAULT_TAX_RATE = 21.0


def compute_roic_decomposition(record: dict | None, roic_pct) -> dict:
    """ROIC 分解 ×存續力 × 增量 ROIC×再投資率 —— 三個機械模組（2026-09-16）。

    Derived entirely from the optional Koyfin xlsx columns documented in
    load_eps_estimates_xlsx.py's module docstring (EBIT Margin % / ROIC 3Y
    Avg % / Tax Rate % / Revenue FY(-3) / EBIT FY(-3) / Invested Capital
    FY(-3)). `record` is the RAW per-ticker dict from ExcelSnapshot.get(t) —
    i.e. `_excel_record_for_eps2y` in enrich_ticker(), NOT the ADR-adjusted
    apply_adr_ratio() version: these are aggregate financials/margins, not
    per-share EPS, so ADR conversion doesn't apply (same rationale as the
    existing roic_pct/fcf_margin_pct/roic_5y_avg_pct reads). `roic_pct` is
    the screener's already-resolved current-period ROIC % (post koyfin-xlsx/
    QGM/yfinance priority — see enrich_ticker), passed in separately so this
    function stays pure/testable without the full enrich_ticker context.

    Pure function — no I/O, no side effects. All outputs None when the
    underlying inputs are missing (record=None or column absent on a legacy
    xlsx), except tax_rate_pct/tax_rate_source which always resolve (falling
    back to the 21% default) since that's the documented behavior for a
    blank/garbage Tax Rate % cell. Every percent value rounded to 2dp.

    Field contract (see 2026-09-16 dd-screener build spec):
      ebit_margin_pct, tax_rate_pct, tax_rate_source ("xlsx"|"default21"),
      nopat_margin_pct, ic_turnover_x, roic_quadrant, roic_quadrant_code,
      roic_3y_avg_pct, roic_vs_5y_x, roic_trend_5y, incremental_roic_pct,
      incremental_roic_note, incremental_roic_clamped, reinvest_rate_pct,
      implied_growth_pct, capital{rev_fy,rev_fy3,ebit_fy,ebit_fy3,ic_fy,ic_fy3}.
    """
    rec = record or {}

    def _num(x):
        return float(x) if isinstance(x, (int, float)) else None

    ebit_margin = _num(rec.get("ebit_margin_pct"))
    tax_rate_raw = _num(rec.get("tax_rate_pct"))
    rev_fy = _num(rec.get("rev_fy"))
    rev_fy3 = _num(rec.get("rev_fy3"))
    ebit_fy = _num(rec.get("ebit_fy"))
    ebit_fy3 = _num(rec.get("ebit_fy3"))
    ic_fy = _num(rec.get("ic_fy"))
    ic_fy3 = _num(rec.get("ic_fy3"))
    roic_3y = _num(rec.get("roic_3y_avg_pct"))
    roic_5y = _num(rec.get("roic_5y_avg_pct"))
    roic_now = _num(roic_pct)

    out = {
        "ebit_margin_pct": round(ebit_margin, 2) if ebit_margin is not None else None,
        "tax_rate_pct": None,
        "tax_rate_source": None,
        "nopat_margin_pct": None,
        "ic_turnover_x": None,
        "roic_quadrant": None,
        "roic_quadrant_code": None,
        "roic_3y_avg_pct": round(roic_3y, 2) if roic_3y is not None else None,
        "roic_vs_5y_x": None,
        "roic_trend_5y": None,
        "incremental_roic_pct": None,
        "incremental_roic_note": None,
        "incremental_roic_clamped": False,
        "reinvest_rate_pct": None,
        "implied_growth_pct": None,
        "capital": {
            "rev_fy": round(rev_fy, 2) if rev_fy is not None else None,
            "rev_fy3": round(rev_fy3, 2) if rev_fy3 is not None else None,
            "ebit_fy": round(ebit_fy, 2) if ebit_fy is not None else None,
            "ebit_fy3": round(ebit_fy3, 2) if ebit_fy3 is not None else None,
            "ic_fy": round(ic_fy, 2) if ic_fy is not None else None,
            "ic_fy3": round(ic_fy3, 2) if ic_fy3 is not None else None,
        },
    }

    # Tax rate: xlsx value sane-checked to [0, 50]; else default 21% (always
    # resolves — see docstring).
    if tax_rate_raw is not None and 0 <= tax_rate_raw <= 50:
        tax_rate = tax_rate_raw
        out["tax_rate_source"] = "xlsx"
    else:
        tax_rate = ROIC_DECOMP_DEFAULT_TAX_RATE
        out["tax_rate_source"] = "default21"
    out["tax_rate_pct"] = round(tax_rate, 2)

    # 1) ROIC decomposition: NOPAT margin × invested-capital turnover, 4-quadrant.
    nopat_margin = None
    if ebit_margin is not None:
        nopat_margin = ebit_margin * (1 - tax_rate / 100.0)
        out["nopat_margin_pct"] = round(nopat_margin, 2)

    ic_turnover = None
    if ic_fy is not None and ic_fy > 0 and rev_fy is not None:
        ic_turnover = rev_fy / ic_fy
        out["ic_turnover_x"] = round(ic_turnover, 2)

    if nopat_margin is not None and ic_turnover is not None:
        high_margin = nopat_margin >= 15
        high_turnover = ic_turnover >= 1.0
        if high_margin and high_turnover:
            out["roic_quadrant"], out["roic_quadrant_code"] = "利厚轉快", "HH"
        elif high_margin:
            out["roic_quadrant"], out["roic_quadrant_code"] = "利厚轉慢", "HL"
        elif high_turnover:
            out["roic_quadrant"], out["roic_quadrant_code"] = "利薄轉快", "LH"
        else:
            out["roic_quadrant"], out["roic_quadrant_code"] = "利薄轉慢", "LL"

    # 2) ROIC persistence: current ROIC vs 5Y average.
    if roic_now is not None and roic_5y is not None and roic_5y > 0:
        ratio = roic_now / roic_5y
        out["roic_vs_5y_x"] = round(ratio, 2)
        if ratio >= 1.10:
            out["roic_trend_5y"] = "上升"
        elif ratio <= 0.90:
            out["roic_trend_5y"] = "下滑"
        else:
            out["roic_trend_5y"] = "持平"

    # 3) Incremental ROIC × reinvestment rate over the last 3 fiscal years.
    delta_ic = None
    if ic_fy is not None and ic_fy3 is not None:
        delta_ic = ic_fy - ic_fy3

    nopat_fy = ebit_fy * (1 - tax_rate / 100.0) if ebit_fy is not None else None
    nopat_fy3 = ebit_fy3 * (1 - tax_rate / 100.0) if ebit_fy3 is not None else None

    if delta_ic is not None and nopat_fy is not None and nopat_fy3 is not None:
        if delta_ic > 0 and ic_fy3 is not None and ic_fy3 > 0:
            incr_roic = (nopat_fy - nopat_fy3) / delta_ic * 100.0
            clamped = False
            if incr_roic > 500:
                incr_roic, clamped = 500.0, True
            elif incr_roic < -200:
                incr_roic, clamped = -200.0, True
            out["incremental_roic_pct"] = round(incr_roic, 2)
            out["incremental_roic_clamped"] = clamped
        elif delta_ic <= 0:
            out["incremental_roic_note"] = "資本縮減"

        denom = 3 * (nopat_fy + nopat_fy3) / 2.0
        if denom > 0:
            reinvest = delta_ic / denom * 100.0
            if reinvest > 200:
                reinvest = 200.0
            elif reinvest < -100:
                reinvest = -100.0
            out["reinvest_rate_pct"] = round(reinvest, 2)

    # implied_growth_pct = incremental_roic_pct × reinvest_rate_pct / 100 —
    # only when both resolved and incremental_roic_pct wasn't saturated by
    # the [-200, 500] clamp (a clamped value is a sentinel, not a real rate).
    if (out["incremental_roic_pct"] is not None
            and out["reinvest_rate_pct"] is not None
            and not out["incremental_roic_clamped"]):
        out["implied_growth_pct"] = round(
            out["incremental_roic_pct"] * out["reinvest_rate_pct"] / 100.0, 2
        )

    return out


# 2026-09-17: 體質五項 veto zh 標籤 — see compute_fundamental_gates() item A.
QUALITY_VETO_LABELS = {
    "gm_3y_decline": "毛利連降",
    "fcf_ni": "FCF/淨利",
    "rev_4q_negative": "營收連四季負",
    "leverage": "槓桿",
    "eps_fy1_consec_down": "FY1連三月下修",
}

# A5 baseline months for eps_fy1_consec_down — canonical month-end snapshots
# under docs/dd-screener/eps-estimates-snapshots/.
_EPS_FY1_BASELINE_MONTHS = ("2026-06", "2026-07", "2026-08")
_eps_fy1_baseline_cache: dict | None = None


def _load_eps_fy1_baselines() -> dict:
    """Load the 3 monthly EPS snapshots used by compute_eps_fy1_consec_down()
    (compute_fundamental_gates item A5). Cached at module level, same pattern
    as _load_prev_month_snapshot()."""
    global _eps_fy1_baseline_cache
    if _eps_fy1_baseline_cache is not None:
        return _eps_fy1_baseline_cache
    snapshot_dir = ROOT / "docs" / "dd-screener" / "eps-estimates-snapshots"
    out = {}
    for month in _EPS_FY1_BASELINE_MONTHS:
        try:
            out[month] = json.loads((snapshot_dir / f"{month}.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            out[month] = {}
    _eps_fy1_baseline_cache = out
    return out


def compute_eps_fy1_consec_down(ticker: str, yf_ticker: str, eps_fy1_current: float | None,
                                 current_snapshot_date: str | None,
                                 reporting_ccy_cache: dict, fx_cache: dict,
                                 baselines: dict | None = None) -> str | None:
    """體質五項 veto item A5 [timing-appendix §B/H]: fail if FY1 EPS was
    revised down in each of the last 3 monthly baselines (2026-06->07,
    07->08, 08->current xlsx), each step <= -0.5%. FX-normalized (to the
    reporting currency) + ADR-adjusted exactly like _compute_fy_eps_revision
    does, so non-USD names / ADRs aren't false positives from a pure FX or
    share-count-basis move.

    Kept separate from compute_fundamental_gates() (which stays a pure,
    network-free function) because this item alone needs the 3 on-disk
    baseline snapshots + get_reporting_currency()/get_fx_rate() (yfinance-
    backed, cached). `baselines` is injectable so tests can supply synthetic
    snapshots without touching disk/network. Returns None (unknown) when
    any step's data or FX rate can't be resolved — never raises.
    """
    baselines = baselines if baselines is not None else _load_eps_fy1_baselines()
    points = []
    for month in _EPS_FY1_BASELINE_MONTHS:
        snap = baselines.get(month) or {}
        row = (snap.get("tickers") or {}).get(ticker)
        if row is None:
            return None
        raw = row.get("eps_fy_curr") or row.get("eps_0y")
        adj = apply_adr_ratio(ticker, {"fy1": raw}).get("fy1")
        points.append((snap.get("snapshot_date") or month, adj))
    points.append((current_snapshot_date, eps_fy1_current))
    if any(v is None for _, v in points):
        return None

    currency = get_reporting_currency(ticker, yf_ticker, reporting_ccy_cache)
    steps = []
    for (d0, v0), (d1, v1) in zip(points, points[1:]):
        fx0 = fx1 = None
        if currency and currency.upper() != "USD":
            fx0 = get_fx_rate(currency, d0, fx_cache) if d0 else None
            fx1 = get_fx_rate(currency, d1, fx_cache) if d1 else None
        pct, _ = compute_fx_normalized_revision(v1, v0, currency, fx1, fx0)
        if pct is None:
            return None
        steps.append(pct)
    return "fail" if all(p <= -0.5 for p in steps) else "pass"


_FUND_RAW_FIELDS = (
    "rev_yoy_fq0_pct", "rev_yoy_fq1_pct", "rev_yoy_fq2_pct", "rev_yoy_fq3_pct",
    "gm_ltm_pct", "gm_fy1_pct", "gm_fy2_pct", "gm_fy3_pct",
    "sales_ltm", "ebit_ltm", "net_debt_ebitda_x",
    "sales_growth_fy_pct", "ebit_growth_fy_pct",
    "dil_shares_fy", "dil_shares_fy3",
    "sbc_ltm", "capex_ltm", "fcf_ltm", "net_debt_ltm", "buyback_ltm",
    "ccc_days", "pe_ntm_x", "pe_ntm_5y_avg_x", "pb_x", "pb_5y_avg_x",
    "rsi14", "price_chg_6m_pct",
    "target_high", "target_low", "target_avg", "last_price_local",
    "ni_margin_ltm_pct", "est_rev_cagr_3y_pct", "est_eps_cagr_3y_pct",
    "below_52w_high_pct",
    # 2026-09-17 (second same-day refresh, 籌碼面): see compute_fundamental_gates()
    # §L below and scripts/load_eps_estimates_xlsx.py docstring "Two more optional
    # columns" section.
    "short_interest_pct_float", "insider_net_buy_3m",
)

# v4.1（2026-09-17，見 knowledge/rule_ledger.md「v4.1 融券比 >10% 只能衛星」列）：
# 融券占流通股比門檻——超過此值只在 GRP 席位引擎（scripts/engine/grp.py）排除核心
# 候選資格（衛星照樣能坐），不是這裡的資格閘，這裡只算旗標供顯示。
SHORT_SQUEEZE_PCT = 10.0
# 內部人訊號門檻：insider_net_buy_3m（近 3 個月淨買賣股數，Koyfin "Insider
# Transactions, Shares (Net) - 3M"）> 0 視為淨買超（"買"）、< 0 視為淨賣超
# （"賣"）、= 0 或缺值不判定方向（None）——單純看淨股數正負號，不設額外門檻
# （3 個月窗已經是 Koyfin 提供的最短週期，方向本身就是訊號，不疊加大小門檻）。
# 純備註 badge，不是排序因子、不是資格閘。


def compute_fundamental_gates(record: dict | None, roic_quadrant_code: str | None,
                               eps_fy1: float | None,
                               eps_fy1_consec_down: str | None = None) -> dict:
    """DD 技能既有的機械化規則逐字搬進 screener（2026-09-17）——體質五項 veto
    [timing-appendix §B/H] + 六組衍生 gate（營運槓桿 QC-27 / 毛利觸發 QC-26 /
    資本配置機械版 問四 / capex 強度 §1 / 虧損股 gate QC-45 / 衰退訊號 問三 /
    估值對自身歷史 閘3閘5 / 目標價分歧 #23 / 動能 rows 5,8a / CCC）+ §L 籌碼面
    （融券占流通股比旗標 short_squeeze_flag、內部人淨買賣方向 insider_signal，
    2026-09-17 第二次同日更新新增）。不新創門檻，來源見各節內註解。

    `record` is the RAW per-ticker Excel dict (ExcelSnapshot.get(t)) — same
    convention as compute_roic_decomposition(): aggregate financials/margins/
    prices, not per-share EPS, so no ADR adjustment. Target High/Low/Avg and
    Last Price Local are the listing's LOCAL currency and only ever used as
    ratios to each other here (never mixed with USD).

    `eps_fy1_consec_down` (item A5) is computed upstream by
    compute_eps_fy1_consec_down() — needs network/disk I/O, so it's passed in
    as a plain "pass"|"fail"|None to keep this function itself pure and
    unit-testable without network. All outputs None when the underlying
    inputs are missing; every percent/ratio value rounded to 2dp.
    """
    rec = record or {}

    def _n(key):
        v = rec.get(key)
        return float(v) if isinstance(v, (int, float)) else None

    def _r2(x):
        return round(x, 2) if isinstance(x, (int, float)) else None

    fund = {k: _r2(_n(k)) for k in _FUND_RAW_FIELDS}
    out = {"fund": fund}

    gm_ltm, gm_fy1, gm_fy2, gm_fy3 = (fund["gm_ltm_pct"], fund["gm_fy1_pct"],
                                       fund["gm_fy2_pct"], fund["gm_fy3_pct"])
    ni_margin = fund["ni_margin_ltm_pct"]
    fcf_margin = _r2(_n("fcf_margin_pct"))  # pre-existing 2026-09-09 Koyfin column, same record
    net_debt_ebitda = fund["net_debt_ebitda_x"]
    net_debt_ltm = fund["net_debt_ltm"]
    rev_yoy = [fund["rev_yoy_fq0_pct"], fund["rev_yoy_fq1_pct"],
               fund["rev_yoy_fq2_pct"], fund["rev_yoy_fq3_pct"]]
    sales_growth, ebit_growth = fund["sales_growth_fy_pct"], fund["ebit_growth_fy_pct"]
    ebit_ltm = fund["ebit_ltm"]
    dil_fy, dil_fy3 = fund["dil_shares_fy"], fund["dil_shares_fy3"]
    sbc_ltm, capex_ltm, fcf_ltm, buyback_ltm = (fund["sbc_ltm"], fund["capex_ltm"],
                                                 fund["fcf_ltm"], fund["buyback_ltm"])
    sales_ltm = fund["sales_ltm"]

    # --- A. 體質五項 veto ---------------------------------------------------
    veto = {}

    if None not in (gm_ltm, gm_fy1, gm_fy2, gm_fy3):
        monotonic = gm_ltm < gm_fy1 < gm_fy2 < gm_fy3
        veto["gm_3y_decline"] = "fail" if monotonic and (gm_fy3 - gm_ltm) > 2.0 else "pass"
    else:
        veto["gm_3y_decline"] = None

    fcf_ni_ratio = None
    if fcf_margin is not None and ni_margin is not None and ni_margin > 0:
        fcf_ni_ratio = fcf_margin / ni_margin
        veto["fcf_ni"] = "fail" if fcf_ni_ratio < 0.7 else "pass"
    else:
        veto["fcf_ni"] = None

    if all(v is not None for v in rev_yoy):
        veto["rev_4q_negative"] = "fail" if all(v < 0 for v in rev_yoy) else "pass"
    else:
        veto["rev_4q_negative"] = None

    if net_debt_ebitda is not None:
        veto["leverage"] = "fail" if net_debt_ebitda > 3.0 else "pass"
    elif net_debt_ltm is not None:
        veto["leverage"] = "pass" if net_debt_ltm < 0 else None
    else:
        veto["leverage"] = None

    veto["eps_fy1_consec_down"] = eps_fy1_consec_down if eps_fy1_consec_down in ("pass", "fail") else None

    fail_count = sum(1 for v in veto.values() if v == "fail")
    known_count = sum(1 for v in veto.values() if v is not None)
    out.update(veto)
    # v4 席位引擎 (2026-09-17): own_score v4 的品質百分位輸入之一（見 grp.own_raw()）
    # ——之前只在本函式內部算 fcf_ni 的 pass/fail，沒有把比值本身曝出去。
    out["fcf_ni_ratio"] = _r2(fcf_ni_ratio)
    out["quality_veto_fail_count"] = fail_count
    out["quality_veto_fails"] = [QUALITY_VETO_LABELS[k] for k, v in veto.items() if v == "fail"]
    if known_count == 0:
        # No coverage at all (e.g. ticker predates the 2026-09-17 xlsx columns) —
        # None, not a misleading "維持" default (see FE _fundHasAnyData() gate).
        out["quality_veto_level"] = None
    elif fail_count >= 4:
        out["quality_veto_level"] = "拒絕"
    elif fail_count == 3:
        out["quality_veto_level"] = "降一級"
    else:
        out["quality_veto_level"] = "維持"

    # --- B. Operating-leverage divergence [QC-27] ----------------------------
    ol_divergence_pp = None
    ol_divergence_label = None
    if sales_growth is not None and ebit_growth is not None and ebit_ltm is not None and ebit_ltm > 0:
        ol_divergence_pp = sales_growth - ebit_growth
        if ol_divergence_pp < 0:
            ol_divergence_label = "利潤率擴張"
        elif ol_divergence_pp <= 3:
            ol_divergence_label = "接近平衡"
        elif ol_divergence_pp <= 7:
            ol_divergence_label = "壓縮"
        else:
            ol_divergence_label = "嚴重壓縮"
    out["ol_divergence_pp"] = _r2(ol_divergence_pp)
    out["ol_divergence_label"] = ol_divergence_label

    # --- C. Gross-margin trigger [QC-26] --------------------------------------
    gm_yoy_pp = (gm_ltm - gm_fy1) if gm_ltm is not None and gm_fy1 is not None else None
    out["gm_yoy_pp"] = _r2(gm_yoy_pp)
    out["gm_trigger"] = (gm_yoy_pp < -1.5) if gm_yoy_pp is not None else None

    # --- D. Capital allocation, mechanical 2-of-3 [問四] -----------------------
    sbc_dilution_pct_yr = None
    dilution_ok = None
    if dil_fy is not None and dil_fy3 is not None and dil_fy3 > 0 and dil_fy > 0:
        sbc_dilution_pct_yr = ((dil_fy / dil_fy3) ** (1 / 3) - 1) * 100
        dilution_ok = sbc_dilution_pct_yr <= 1.5
    out["sbc_dilution_pct_yr"] = _r2(sbc_dilution_pct_yr)

    buyback_fcf_pct = None
    buyback_ok = None
    if buyback_ltm is not None:
        if buyback_ltm == 0:
            buyback_ok = True
        elif fcf_ltm is not None and fcf_ltm > 0:
            buyback_fcf_pct = abs(buyback_ltm) / fcf_ltm * 100
            buyback_ok = buyback_fcf_pct <= 80
    out["buyback_fcf_pct"] = _r2(buyback_fcf_pct)

    sbc_pct_rev = (sbc_ltm / sales_ltm * 100) if sbc_ltm is not None and sales_ltm is not None and sales_ltm > 0 else None
    out["sbc_pct_rev"] = _r2(sbc_pct_rev)

    leverage_ok = (veto["leverage"] == "pass") if veto["leverage"] is not None else None
    capalloc_items = [x for x in (dilution_ok, buyback_ok, leverage_ok) if x is not None]
    if len(capalloc_items) < 2:
        out["capalloc_mech_grade"] = None
    else:
        passes = sum(1 for x in capalloc_items if x)
        out["capalloc_mech_grade"] = "A" if passes >= 3 else ("B" if passes == 2 else "C")

    # --- E. Capex intensity [§1 預設尺] -----------------------------------------
    capex_pct_rev = (abs(capex_ltm) / sales_ltm * 100) if capex_ltm is not None and sales_ltm is not None and sales_ltm > 0 else None
    out["capex_pct_rev"] = _r2(capex_pct_rev)
    out["capex_intensity_label"] = (
        None if capex_pct_rev is None else ("輕" if capex_pct_rev < 5 else ("中" if capex_pct_rev < 10 else "重"))
    )
    capex_fcf_pct = (abs(capex_ltm) / fcf_ltm * 100) if capex_ltm is not None and fcf_ltm is not None and fcf_ltm > 0 else None
    out["capex_fcf_pct"] = _r2(capex_fcf_pct)

    # --- F. Unprofitable-company gates [QC-45] ---------------------------------
    rule_of_40 = None
    cash_runway_months = None
    unprofitable = (ni_margin is not None and ni_margin < 0) or (eps_fy1 is not None and eps_fy1 < 0)
    if unprofitable:
        if sales_growth is not None and fcf_margin is not None:
            rule_of_40 = sales_growth + fcf_margin
        if fcf_ltm is not None and fcf_ltm < 0 and net_debt_ltm is not None and net_debt_ltm < 0:
            cash_runway_months = (-net_debt_ltm) / (abs(fcf_ltm) / 12)
    out["rule_of_40"] = _r2(rule_of_40)
    out["rule_of_40_flag"] = (rule_of_40 < 20) if rule_of_40 is not None else None
    out["cash_runway_months"] = _r2(cash_runway_months)
    out["cash_runway_flag"] = (cash_runway_months < 12) if cash_runway_months is not None else None

    # --- G. Decline-signal count [問三，6 個機械項] -------------------------------
    est_rev_cagr, est_eps_cagr = fund["est_rev_cagr_3y_pct"], fund["est_eps_cagr_3y_pct"]
    gm_2y_known = gm_ltm is not None and gm_fy1 is not None and gm_fy2 is not None
    eps_engineer_known = est_eps_cagr is not None and est_rev_cagr is not None
    decline_checks = (
        (gm_2y_known, gm_2y_known and gm_ltm < gm_fy1 and gm_fy1 < gm_fy2, "毛利連兩年降"),
        (eps_engineer_known, eps_engineer_known and (est_eps_cagr - est_rev_cagr) > 5, "EPS 成長靠財務工程"),
        (fcf_ni_ratio is not None, fcf_ni_ratio is not None and fcf_ni_ratio < 0.75, "FCF 遜於淨利"),
        (sbc_pct_rev is not None, sbc_pct_rev is not None and sbc_pct_rev > 5, "SBC 佔營收偏高"),
        (capex_fcf_pct is not None, capex_fcf_pct is not None and capex_fcf_pct > 60, "資本支出侵蝕 FCF"),
        (veto["rev_4q_negative"] is not None, veto["rev_4q_negative"] == "fail", "營收連四季負"),
    )
    decline_signals = [label for known, hit, label in decline_checks if known and hit]
    out["decline_signal_count"] = len(decline_signals)
    out["decline_signals"] = decline_signals
    if len(decline_signals) == 0:
        out["decline_signal_light"] = "🟢"
    elif len(decline_signals) <= 2:
        out["decline_signal_light"] = "🟡"
    elif len(decline_signals) <= 4:
        out["decline_signal_light"] = "🔴"
    else:
        out["decline_signal_light"] = "⛔"

    # --- H. Valuation vs own history [閘3/閘5] -----------------------------------
    pe_x, pe_5y = fund["pe_ntm_x"], fund["pe_ntm_5y_avg_x"]
    pb_x, pb_5y = fund["pb_x"], fund["pb_5y_avg_x"]
    pe_vs_5y_x = pe_x / pe_5y if pe_x is not None and pe_5y is not None and pe_5y > 0 else None
    pb_vs_5y_x = pb_x / pb_5y if pb_x is not None and pb_5y is not None and pb_5y > 0 else None
    out["pe_vs_5y_x"] = _r2(pe_vs_5y_x)
    out["pe_vs_5y_flag"] = (pe_vs_5y_x > 1.5) if pe_vs_5y_x is not None else None
    out["pb_vs_5y_x"] = _r2(pb_vs_5y_x)
    out["pb_vs_5y_flag"] = (pb_vs_5y_x > 2.0) if pb_vs_5y_x is not None else None

    # --- I. Consensus dispersion [#23] -------------------------------------------
    t_high, t_low, t_avg, last_px = (fund["target_high"], fund["target_low"],
                                      fund["target_avg"], fund["last_price_local"])
    target_range_x = t_high / t_low if t_high is not None and t_low is not None and t_low > 0 else None
    target_upside_pct = ((t_avg / last_px - 1) * 100
                          if t_avg is not None and last_px is not None and last_px > 0 else None)
    out["target_range_x"] = _r2(target_range_x)
    out["target_range_flag"] = (target_range_x > 2.5) if target_range_x is not None else None
    out["target_upside_pct"] = _r2(target_upside_pct)

    # --- J. Momentum gates [decision-layer rows 5 / 8a] ---------------------------
    rsi14 = fund["rsi14"]
    ret_6m = fund["price_chg_6m_pct"]
    below_52w = fund["below_52w_high_pct"]
    out["rsi14"] = rsi14
    out["rsi_overheated"] = (rsi14 > 70) if rsi14 is not None else None
    out["return_6m_pct"] = ret_6m
    if ret_6m is None:
        out["return_6m_gate"] = None
    elif ret_6m > 150:
        out["return_6m_gate"] = "擋下"
    elif ret_6m >= 100:
        out["return_6m_gate"] = "邊界"
    else:
        out["return_6m_gate"] = "放行"
    out["rsi_usable"] = (abs(below_52w) > 3) if below_52w is not None else None

    # --- K. CCC passthrough + LH note ----------------------------------------------
    ccc = fund["ccc_days"]
    out["ccc_days"] = ccc
    out["ccc_supplier_financed"] = (ccc < 0) if ccc is not None else None
    lh_note = None
    if roic_quadrant_code == "LH" and ccc is not None:
        lh_note = "供應商融資" if ccc < 0 else ("需查 CCC" if ccc > 60 else None)
    out["lh_ccc_note"] = lh_note

    # --- L. Short interest / insider (2026-09-17, 籌碼面) ------------------------
    # 兩者皆純描述器：short_squeeze_flag 不是資格閘（GRP 席位引擎的融券排除核心候選
    # 判定另在 scripts/engine/grp.py grp_score() 讀 short_interest_pct_float 自算，
    # 不讀這個旗標）；insider_signal 只是備註 badge，兩者都不進 funnel_rank 公式。
    si_pct = fund["short_interest_pct_float"]
    out["short_interest_pct_float"] = si_pct
    out["short_squeeze_flag"] = (si_pct > SHORT_SQUEEZE_PCT) if si_pct is not None else None
    insider_net = fund["insider_net_buy_3m"]
    out["insider_net_buy_3m"] = insider_net
    if insider_net is None:
        out["insider_signal"] = None
    elif insider_net > 0:
        out["insider_signal"] = "買"
    elif insider_net < 0:
        out["insider_signal"] = "賣"
    else:
        out["insider_signal"] = None

    return out


def enrich_ticker(
    entry: dict,
    qgm_index: dict,
    dca_ev_map: dict,
    dca_trend_map: dict,
    screener_timing: dict,
    timing_fallback: dict,
    skip_ma: bool,
    ma_cache: dict | None = None,
    quality_cache: dict | None = None,
    prev_snapshot: dict | None = None,
    excel_snapshot: ExcelSnapshot | None = None,
    qgm_durable_index: dict | None = None,
    reporting_ccy_cache: dict | None = None,
    fx_cache: dict | None = None,
    eps_rev_3m_baseline: dict | None = None,
) -> dict:
    """Add quality + MA + ev5y_pct + pass_count + fail_criteria + timing to entry.

    Also overrides moat_trend with DCA Phase A1 authoritative arrow (the loader
    defaults all 98 to ↑ because dd-meta rarely carries this field; DCA does).

    `timing` joins `docs/screener/latest.json` by ticker — for tickers not in
    the screener universe (TW/JP/EU + niche US), falls back to `timing_fallback`
    computed by compute_yfinance_timing_fallback() from a yfinance batch fetch.

    v1.3: also computes live_fpe_est / pe_drift_pct / dd_age_days / live_pct_5y_est
    from price drift since DD write (unfreezes valuation columns).

    v1.5: when yfinance returns all-None quality (rate-limit) for a yfinance-
    source ticker, fall back to previous latest.json's cached values + tag
    quality_from_cache=True + carry quality_cache_stamp. QGM rows never touch
    the cache (they load from JSON on disk). Sister to MA cache fallback (v1.4).

    v1.7: fetches _fetch_live_fy_eps() once per ticker and shares result with
    both _compute_live_pe_drift() and _compute_live_eps_cagr() to avoid a
    duplicate yfinance call. Also computes EPS revision momentum vs prev_snapshot
    (monthly snapshot), live_peg, and live_ev5y_pct.

    2026-09-09: source priority for roic/fcf is now koyfin-xlsx (Excel record's
    roic_pct/fcf_margin_pct, scraped by refresh-eps-screener-web) → QGM →
    yfinance. When the Excel record carries either field, it overrides
    quality["roic"]/quality["fcf"] independently, quality_source becomes
    "koyfin-xlsx", and quality_koyfin_stamp records the Excel snapshot date.
    peg/de/eps2y are untouched by this override.

    2026-09-09 (v3 席位資格): also emits `durable_5y` (True/False/None) and
    `durable_source` ("koyfin-xlsx"/"qgm"/None) — core-seat eligibility input
    for scripts/engine/grp.py's route logic. Priority: Excel roic_5y_avg_pct
    (>=15 -> True) first; if absent, QGM roic_5y_stability.pct_above via
    `qgm_durable_index` (>=0.75 -> True); None when neither source has this
    ticker. See knowledge/rule_ledger.md v3 席位資格 row.
    """
    t = entry["ticker"]
    # 2026-09-17: shared, thread-safe caches for FX-normalized EPS revision
    # (see _compute_fy_eps_revision) — default to a fresh dict when the
    # caller doesn't pass one (e.g. ad-hoc/test calls), same pattern as the
    # other Optional[dict]=None params on this function.
    if reporting_ccy_cache is None:
        reporting_ccy_cache = {}
    if fx_cache is None:
        fx_cache = {}
    quality, source, quality_meta = get_quality_for_ticker(t, qgm_index)
    # v1.3: peg_fallback — frozen PEG came from yfinance manual forwardPE/CAGR
    # path (denominator not comparable to mainstream forward consensus). The
    # PEG pass/fail is still computed normally; this only annotates provenance.
    peg_fallback = bool(quality_meta.get("peg_fallback"))

    # v1.5: quality cache fallback for yfinance-path rows on total-wipe outages.
    # Only triggers when ALL 5 fields are None AND source is yfinance (QGM rows
    # come from local JSON, no outage signature). Per-field substitution
    # preserves any partial fresh data when only some fields fail.
    quality_from_cache = False
    quality_cache_stamp = None
    if source.startswith("yfinance") and quality_cache and t in quality_cache:
        non_null_fresh = sum(1 for v in quality.values() if v is not None)
        if non_null_fresh == 0:
            cached = quality_cache[t]
            for k in _QUALITY_FIELDS:
                v = cached.get(k)
                if v is not None:
                    quality[k] = v
            quality_from_cache = True
            quality_cache_stamp = cached.get("_stamp")

    # v1.9: Override `eps2y` with Excel forward CAGR (eps_fy1_fy3_cagr_pct) BEFORE
    # evaluate_criteria, so the QGM "EPS 2Y CAGR ≥ 15%" rule (now labelled
    # "FY+1→FY+3 CAGR ≥ 15%") anchors on Excel buy-side pure forward consensus
    # instead of yfinance YearAgo→FY+1 mixed window.
    _excel_record_for_eps2y = excel_snapshot.get(t) if excel_snapshot else None
    if _excel_record_for_eps2y is not None:
        _excel_cagr = _excel_record_for_eps2y.get("cagr_fy1_fy3_pct")
        if _excel_cagr is not None:
            quality["eps2y"] = round(float(_excel_cagr), 2)

    # 2026-09-09: Koyfin-scraped ROIC / FCF Margin override (refresh-eps-
    # screener-web §1/§6, load_eps_estimates_xlsx.py roic_pct/fcf_margin_pct).
    # Owner decision: once these two columns are present in the xlsx, they take
    # priority over QGM/yfinance for those two fields specifically — everything
    # else (peg/de/eps2y, and the QGM vs yfinance path for roic/fcf when the
    # xlsx doesn't carry them) is untouched. Placed AFTER the v1.5 cache-
    # fallback block above so cache-fallback (which only ever fires on a total
    # yfinance wipe, checked against `source` before this block relabels it)
    # can never clobber a Koyfin value landing here — this override always
    # runs last and wins.
    quality_koyfin_stamp = None
    if _excel_record_for_eps2y is not None:
        _koyfin_roic = _excel_record_for_eps2y.get("roic_pct")
        _koyfin_fcf = _excel_record_for_eps2y.get("fcf_margin_pct")
        koyfin_hit = False
        if _koyfin_roic is not None:
            quality["roic"] = round(float(_koyfin_roic), 2)
            koyfin_hit = True
        if _koyfin_fcf is not None:
            quality["fcf"] = round(float(_koyfin_fcf), 2)
            koyfin_hit = True
        if koyfin_hit:
            source = "koyfin-xlsx"
            quality_koyfin_stamp = excel_snapshot.snapshot_date if excel_snapshot else None

    # durable_5y — core-seat durability signal. v3 (2026-09-09): priority Koyfin
    # roic_5y_avg_pct (>=15% -> True) then QGM roic_5y_stability.pct_above
    # (>=75% -> True) via qgm_durable_index; None when neither source covers t.
    # v4 (2026-09-17, knowledge/rule_ledger.md v4 席位引擎列): when BOTH sources
    # cover the ticker, OR them (either threshold met -> durable) instead of
    # letting Koyfin's presence hide a QGM pass — priority-only meant a Koyfin
    # roic_5y_avg_pct just under 15% could mask a QGM stability >=75% that would
    # otherwise have qualified the name. Single-source coverage still behaves
    # exactly as v3 (OR against None is a no-op).
    _koyfin_r5y = _excel_record_for_eps2y.get("roic_5y_avg_pct") if _excel_record_for_eps2y else None
    _qgm_r5y = (qgm_durable_index or {}).get(t)
    _koyfin_pass = None if _koyfin_r5y is None else _koyfin_r5y >= 15.0
    _qgm_pass = None if _qgm_r5y is None else _qgm_r5y >= 0.75
    if _koyfin_pass is None and _qgm_pass is None:
        durable_5y = None
        durable_source = None
    elif _koyfin_pass or _qgm_pass:
        durable_5y = True
        durable_source = "koyfin-xlsx" if _koyfin_pass else "qgm"
    else:
        durable_5y = False
        durable_source = "koyfin-xlsx" if _koyfin_pass is not None else "qgm"

    # 2026-09-16: ROIC 分解 + 存續力 + 增量 ROIC×再投資率 —— pure derivation,
    # see compute_roic_decomposition() docstring. Uses the resolved current
    # ROIC % (post koyfin-xlsx/QGM/yfinance priority above) + the raw Excel
    # record (roic_5y_avg_pct / roic_3y_avg_pct / EBIT / IC / revenue columns).
    roic_decomp = compute_roic_decomposition(_excel_record_for_eps2y, quality.get("roic"))

    pass_count, fails = evaluate_criteria(quality)

    if skip_ma:
        ma = _empty_ma()
        ma_from_cache = False
    else:
        try:
            ma = compute_ma_snapshot(_yf_ticker_for_ma(t))
        except Exception:
            ma = _empty_ma()
        # v1.4: 若 yfinance 抓不到（rate-limit / 網路 hiccup）就用上次 latest.json
        # 的 cached MA — 比顯示空白好，且 FE 可以 surface staleness via ma._stamp
        ma_from_cache = False
        if ma.get("price") is None and ma_cache and t in ma_cache:
            cached = ma_cache[t]
            ma = {k: v for k, v in cached.items() if k != "_stamp"}
            ma["_cache_stamp"] = cached.get("_stamp")
            ma_from_cache = True

    # Override the loader's "↑" default with DCA Phase A1 arrow; "→" when DCA
    # has none (conservative — don't assume strengthening without evidence).
    moat_trend = _moat_trend_for(t, dca_trend_map, fallback="→")

    # Timing: prefer screener (EMA-smoothed, consistent); fall back to yfinance
    # batch for tickers not in the screener universe.
    timing = screener_timing.get(t)
    if timing is None:
        timing = timing_fallback.get(t)  # may still be None if yfinance failed

    # Strip internal sub-score fields from timing dict before storing — they
    # are only needed for RS reference population computation, not for the FE.
    if timing is not None:
        timing = {k: v for k, v in timing.items()
                  if k not in ("rs_1w", "rs_4w", "rs_13w")}

    # v1.7: fetch yfinance EPS once; share with both PE drift + 2Y CAGR helpers.
    # Guard: requires fpe_fy2 + price_at_dd (needed to match the right FY row).
    # p_now is NOT required here — CAGR only needs eps_0y/eps_1y, not current price.
    # PE drift will still degrade gracefully when p_now is None.
    # v1.8: pass excel_record so Excel overrides FY1/FY2/FY3 when ticker is covered.
    fpe = entry.get("fpe_fy2")
    p_dd = entry.get("price_at_dd")
    p_now = ma.get("price") if ma else None
    excel_record = apply_adr_ratio(t, excel_snapshot.get(t)) if excel_snapshot else None
    live_fy_result: dict | None = None
    if fpe and p_dd and fpe > 0 and p_dd > 0:
        live_fy_result = _fetch_live_fy_eps(
            _yf_ticker_for_ma(t), p_dd, fpe,
            excel_record=excel_record, dd_ticker=t,
        )
    elif excel_record is not None:
        # No DD anchor — still surface Excel FY1/FY2/FY3 (no eps_now / revision)
        live_fy_result = {
            "live_fpe_real": None, "yf_fy_label": None,
            "eps_at_dd": None, "eps_now": None, "eps_revision_pct": None,
            "eps_0y_raw": excel_record.get("fy1"),
            "eps_1y_raw": excel_record.get("fy2"),
            "eps_year_ago": None,
            "trailing_eps": None,
            "eps_fy3": excel_record.get("fy3"),
            "growth_fy1_fy2_pct": excel_record.get("growth_fy1_fy2_pct"),
            "growth_fy2_fy3_pct": excel_record.get("growth_fy2_fy3_pct"),
            "cagr_fy1_fy3_pct": excel_record.get("cagr_fy1_fy3_pct"),
            "eps_source": "xlsx",
            "eps_basis": excel_record.get("eps_basis"),
        }

    pe_drift = _compute_live_pe_drift(entry, ma, live_fy_result=live_fy_result)

    # v1.7: EPS 2Y CAGR live + revision momentum
    eps2y_live_result = _compute_live_eps_cagr(entry, live_fy_result or {})
    eps2y_live = eps2y_live_result.get("eps2y_live")

    # v1.9: revision MoM diff anchors on Excel forward CAGR (eps_fy1_fy3_cagr_pct)
    # instead of yfinance-derived eps2y_live, so the UI's ↑↓pp delta reflects
    # buy-side consensus shift rather than yfinance YearAgo→FY+1 window noise.
    excel_cagr_for_rev = (live_fy_result or {}).get("cagr_fy1_fy3_pct")
    eps_revision = _compute_eps_revision(entry, excel_cagr_for_rev, prev_snapshot or {})
    live_peg = _compute_live_peg(pe_drift, eps2y_live, live_fy_result)  # FPE & Excel CAGR

    # Compute ev5y_pct before passing to live_ev5y helper (entry doesn't carry it yet)
    ev5y_pct = _ev5y_for(t, dca_ev_map)
    # Build a minimal context dict for _compute_live_ev5y (needs ev5y_pct + price_at_dd)
    ev5y_entry = {**entry, "ev5y_pct": ev5y_pct}
    live_ev5y = _compute_live_ev5y(ev5y_entry, ma)

    # v1.7.2: surface raw EPS estimates so the FE can show per-FY EPS columns
    # (current FY / next FY consensus + TTM EPS used as CAGR base).
    _lfy = live_fy_result or {}

    # v1.8: per-FY EPS revision vs previous month's Excel snapshot
    eps_curr_val = _lfy.get("eps_0y_raw")
    eps_next_val = _lfy.get("eps_1y_raw")
    # v1.8.6: revision must compare apples-to-apples in USD. When FX conversion
    # ran (foreign listings), eps_0y_raw / eps_1y_raw are in local currency but
    # the prior snapshot stored raw Excel USD. Use *_usd_orig for the diff so
    # TW/JP/HK don't show absurd ~3000% revisions on currency basis change.
    _rev_curr = _lfy.get("eps_fy_curr_usd_orig") or eps_curr_val
    _rev_next = _lfy.get("eps_fy_next_usd_orig") or eps_next_val
    _rev_fy3 = _lfy.get("eps_fy3_usd_orig") or _lfy.get("eps_fy3")
    fy_revision = _compute_fy_eps_revision(
        t, _yf_ticker_for_ma(t), _rev_curr, _rev_next, _rev_fy3, prev_snapshot or {},
        excel_snapshot.snapshot_date if excel_snapshot else None,
        reporting_ccy_cache, fx_cache,
    )

    # v4 席位引擎 (2026-09-17): own_score v4 的三月上修輸入 — 同一台機械對 ~90 天前
    # 的月度 baseline 算一次（見 _compute_eps_rev_3m() docstring）。
    eps_rev_3m = _compute_eps_rev_3m(
        t, _yf_ticker_for_ma(t), _rev_curr, _rev_next, _rev_fy3, eps_rev_3m_baseline or {},
        excel_snapshot.snapshot_date if excel_snapshot else None,
        reporting_ccy_cache, fx_cache,
    )

    # 2026-09-17: fundamental gates — DD 技能既有機械規則搬進 screener (see
    # compute_fundamental_gates() docstring). eps_fy1_consec_down (item A5)
    # needs the 3 monthly baselines + FX/ADR normalization, so it's computed
    # separately and passed in, keeping compute_fundamental_gates itself pure.
    eps_fy1_consec_down = compute_eps_fy1_consec_down(
        t, _yf_ticker_for_ma(t), _rev_curr,
        excel_snapshot.snapshot_date if excel_snapshot else None,
        reporting_ccy_cache, fx_cache,
    )
    fund_gates = compute_fundamental_gates(
        _excel_record_for_eps2y, roic_decomp.get("roic_quadrant_code"),
        eps_curr_val, eps_fy1_consec_down,
    )

    # v1.3: FunnelRank — 漏斗綜合分 (基本面三層: QualityGate + Moat + Revision).
    # 用 per-FY revision %（vs 上一份 snapshot）的 FY1/FY2/FY3 三欄合成 RevisionScore;
    # quality 已含 Excel-overridden eps2y; moat_score 來自 dd-meta (entry); moat_trend
    # 已套 DCA 箭頭。時機 (第四層) 不進公式 — 維持 filter。
    # 2026-09-17: 併入 fund_gates 的 quality_veto_level / decline_signal_light
    # （見 compute_funnel_rank() docstring「四道處置」）。
    funnel = compute_funnel_rank(
        quality,
        pass_count,
        entry.get("moat_score"),
        moat_trend,
        fy_revision.get("eps_fy_curr_revision_pct"),
        fy_revision.get("eps_fy_next_revision_pct"),
        fy_revision.get("eps_fy3_revision_pct"),
        quality_veto_level=fund_gates.get("quality_veto_level"),
        decline_signal_light=fund_gates.get("decline_signal_light"),
    )

    return {
        **entry,
        **quality,
        "moat_trend": moat_trend,
        "pass_count": pass_count,
        "fail_criteria": fails,
        # 2026-07-03: D/E advisory flag (>0.7) — FE 顯示 ⚠ badge，不進 pass_count。
        "de_advisory": de_advisory_flag(quality),
        "peg_fallback": peg_fallback,
        **funnel,   # funnel_rank + 3 sub-scores + veto/cap/partial flags
        "quality_source": source,
        "quality_from_cache": quality_from_cache,
        "quality_cache_stamp": quality_cache_stamp,
        # 2026-09-09: Excel snapshot date the roic/fcf koyfin-xlsx override (if
        # any) came from. None when quality_source != "koyfin-xlsx".
        "quality_koyfin_stamp": quality_koyfin_stamp,
        # 2026-09-09 (v3 席位資格): core-seat durability signal — see docstring.
        "durable_5y": durable_5y,
        "durable_source": durable_source,
        # v4 席位引擎 (2026-09-17): raw durability magnitudes, for the seat-table 耐久
        # column's hover tooltip (engine/build_arena.py) — durable_5y/durable_source
        # alone tell pass/fail + which source, not the underlying number.
        "roic_5y_avg_pct": round(_koyfin_r5y, 2) if _koyfin_r5y is not None else None,
        "qgm_roic_5y_stability_pct": round(_qgm_r5y * 100, 1) if _qgm_r5y is not None else None,
        **roic_decomp,   # ebit_margin_pct/tax_rate_*/nopat_margin_pct/ic_turnover_x/
                         # roic_quadrant*/roic_3y_avg_pct/roic_vs_5y_x/roic_trend_5y/
                         # incremental_roic_*/reinvest_rate_pct/implied_growth_pct/capital
        **fund_gates,    # 2026-09-17: 體質五項 veto/quality_veto_*/ol_divergence_*/
                         # gm_yoy_pp/gm_trigger/capalloc_mech_grade/capex_*/rule_of_40/
                         # cash_runway_months/decline_signal_*/pe_vs_5y_x/pb_vs_5y_x/
                         # target_range_x/target_upside_pct/rsi14/return_6m_*/ccc_*/fund/
                         # short_interest_pct_float/short_squeeze_flag/insider_net_buy_3m/
                         # insider_signal（皆純描述器，見 compute_fundamental_gates §L）
        "ev5y_pct": ev5y_pct,
        "ma": ma,
        "ma_from_cache": ma_from_cache,
        "timing": timing,
        **pe_drift,         # live_fpe_est, pe_drift_pct, dd_age_days, live_pct_5y_est
        **eps2y_live_result,  # eps2y_live, eps2y_live_method
        **eps_revision,     # eps2y_prev_month, eps2y_prev_month_date, eps2y_revision_pp, eps2y_revision_dir
        **live_peg,         # live_peg
        **live_ev5y,        # live_ev5y_pct, live_ev5y_method
        # v1.7.2: raw yfinance EPS estimates (current FY / next FY / TTM)
        "eps_fy_curr": eps_curr_val,
        "eps_fy_next": eps_next_val,
        "eps_trailing": _lfy.get("trailing_eps"),
        # v1.8: Excel-derived FY3 + growth/CAGR columns + provenance
        "eps_fy3": _lfy.get("eps_fy3"),
        "eps_fy3_yoy_pct": _lfy.get("growth_fy2_fy3_pct"),
        "eps_fy1_fy3_cagr_pct": _lfy.get("cagr_fy1_fy3_pct"),
        "eps_source": _lfy.get("eps_source", "yfinance"),
        # 2026-09-12: 換算註記（None 除非 ticker 在 data/adr_ratios.json 表列，如 TSM）
        "eps_basis": _lfy.get("eps_basis"),
        # v1.8: month-over-month revision per FY (vs prev Excel snapshot)
        **fy_revision,  # eps_fy_curr_revision_pct, eps_fy_next_revision_pct, eps_fy3_revision_pct,
                        # eps_revision_baseline_date, eps_revision_currency, eps_revision_fx_normalized
        **eps_rev_3m,   # v4 席位引擎: eps_rev_3m_pct, eps_rev_3m_baseline_date, eps_rev_3m_fx_normalized
        # v1.8.5: foreign-listing native-currency display (TWD/JPY/etc.)
        "eps_display_currency": _lfy.get("eps_display_currency", "USD"),
        "eps_fx_rate": _lfy.get("eps_fx_rate"),
        "eps_fy_curr_usd_orig": _lfy.get("eps_fy_curr_usd_orig"),
        "eps_fy_next_usd_orig": _lfy.get("eps_fy_next_usd_orig"),
        "eps_fy3_usd_orig": _lfy.get("eps_fy3_usd_orig"),
    }


def apply_verdict_overlay(universe: list[dict]) -> dict:
    """P1: 對 dd-meta 沒有原生 dca_verdict 的 ticker，補上機器抽取自 v12 舊 DD 的裁決。

    每筆 universe entry 一律標 `dca_verdict_source`：
      - dd-meta 原生（v13/v14 報告自帶 dca_verdict）→ "dd_meta"
      - overlay 補上 → "overlay_extracted"（另帶 dca_verdict_confidence）
      - 兩者皆無 → None

    防呆：overlay 以 DD 檔名（file）為鍵比對——只有當 overlay 記錄的 file 與該
    ticker「當前最新 DD 檔名」一致時才生效。未來出了新版 DD（自帶裁決或換檔名）後，
    舊 overlay 記錄自動失效，不會蓋過新報告。

    失敗安全：overlay 檔不存在／解析失敗／格式非預期 → 印一行警告後靜默降級
    （原生裁決照標 dd_meta，其餘留 None），screener 行為回到現狀。

    回傳統計 dict 供 build() 印出。
    """
    stats = {"dd_meta": 0, "overlay_extracted": 0, "none": 0,
             "overlay_stale_skipped": 0, "overlay_loaded": 0}

    # 先為所有 entry 標記來源，確保 overlay 缺檔時行為仍一致（additive、向後相容）。
    for e in universe:
        e["dca_verdict_source"] = "dd_meta" if e.get("dca_verdict") is not None else None
        e.setdefault("dca_verdict_confidence", None)

    index: dict[str, dict] = {}
    try:
        with open(VERDICT_OVERLAY_PATH, encoding="utf-8") as f:
            raw = json.load(f)
        entries = raw.get("entries", {})
        if not isinstance(entries, dict):
            raise ValueError("entries 非物件")
        for rec in entries.values():
            fname = rec.get("file")
            if fname:
                index[fname] = rec
        stats["overlay_loaded"] = len(index)
    except FileNotFoundError:
        print(f"  [overlay] {VERDICT_OVERLAY_PATH.name} 不存在 — 略過 overlay，"
              f"裁決回到現狀", file=sys.stderr)
        return _finalize_overlay_stats(universe, stats)
    except Exception as exc:  # noqa: BLE001 — 任何解析/格式錯誤都必須失敗安全
        print(f"  [overlay] 讀取失敗（{exc}）— 略過 overlay，裁決回到現狀",
              file=sys.stderr)
        return _finalize_overlay_stats(universe, stats)

    for e in universe:
        if e.get("dca_verdict") is not None:
            continue  # 原生裁決優先，overlay 永不覆蓋
        dd_path = e.get("dd_path") or ""
        cur_filename = dd_path.rsplit("/", 1)[-1]
        rec = index.get(cur_filename)
        if rec is None:
            continue
        verdict = rec.get("extracted_verdict")
        if verdict is None:
            continue
        # 防呆已由 file 為鍵天然涵蓋：index 命中即代表 file 與當前 DD 檔名一致。
        e["dca_verdict"] = verdict
        e["dca_role"] = _norm_dca_role(rec.get("extracted_role"))
        e["dca_verdict_source"] = "overlay_extracted"
        e["dca_verdict_confidence"] = rec.get("confidence")

    # 統計 overlay 記錄中「file 與當前 DD 不符」而被跳過的筆數（防呆生效證據）。
    applied_files = {(e.get("dd_path") or "").rsplit("/", 1)[-1]
                     for e in universe if e.get("dca_verdict_source") == "overlay_extracted"}
    stats["overlay_stale_skipped"] = sum(1 for fn in index if fn not in applied_files)
    return _finalize_overlay_stats(universe, stats)


def _finalize_overlay_stats(universe: list[dict], stats: dict) -> dict:
    for e in universe:
        src = e.get("dca_verdict_source")
        if src == "dd_meta":
            stats["dd_meta"] += 1
        elif src == "overlay_extracted":
            stats["overlay_extracted"] += 1
        else:
            stats["none"] += 1
    return stats


def build(top_n: int | None, skip_ma: bool, dry_run: bool, workers: int,
          include_non_dd: bool = False) -> dict:
    print(f"=== DD Screener build · {datetime.now().isoformat(timespec='seconds')} ===\n")
    t0 = time.time()

    # Step 0: v1.4 — load previous latest.json's MA snapshots as fallback cache
    ma_cache = load_ma_cache(OUTPUT_PATH)
    print(f"  Step 0    MA cache from prev latest.json: {len(ma_cache)} tickers")

    # Step 0b: v1.5 — load previous latest.json's quality fields as fallback
    # cache for yfinance-source rows (sister to MA cache, same rate-limit cause)
    quality_cache = load_quality_cache(OUTPUT_PATH)
    print(f"  Step 0    quality cache from prev latest.json: {len(quality_cache)} yfinance tickers")

    # Step 1-2
    universe = load_dd_universe()
    if top_n:
        universe = universe[:top_n]
    print(f"  Step 1-2  DD universe: {len(universe)} tickers")

    # Step 1-2c (選股系統 v2, 2026-09): optional non-DD universe from QGM quality
    # pools (US + TW) — DD becomes optional. OFF by default so CI/prod build
    # behaviour is unchanged until this is flipped on deliberately; every field
    # that would normally come from dd-meta is null on these rows (dd_status
    # "none"), and Step 5's evaluate_criteria()/enrich_ticker() are already
    # None-safe on those fields (see downstream-risk audit in the PR notes).
    if include_non_dd:
        existing_tickers = {e["ticker"] for e in universe}
        non_dd_universe = load_non_dd_universe(existing_tickers)
        universe = universe + non_dd_universe
        print(f"  Step 1-2c non-DD universe (QGM): +{len(non_dd_universe)} tickers "
              f"({sum(1 for r in non_dd_universe if r['universe_source'] == 'qgm-us')} US, "
              f"{sum(1 for r in non_dd_universe if r['universe_source'] == 'qgm-tw')} TW) "
              f"→ total {len(universe)}")

    # Step 1-2b: P1 — 補機器抽取的 v12 舊 DD 裁決（失敗安全；overlay 缺檔則行為回到現狀）
    ov = apply_verdict_overlay(universe)
    print(f"  Step 1-2  verdict source: dd_meta={ov['dd_meta']} "
          f"overlay_extracted={ov['overlay_extracted']} none={ov['none']} "
          f"(overlay 記錄 {ov['overlay_loaded']}，file 不符跳過 {ov['overlay_stale_skipped']})")

    # Step 3 prep
    qgm_index = load_qgm_index()
    print(f"  Step 3    QGM index: {len(qgm_index)} entries ({sum(1 for s,_ in qgm_index.values() if s=='qgm-us')} US, {sum(1 for s,_ in qgm_index.values() if s=='qgm-tw')} TW)")
    # 2026-09-09 (v3 席位資格): QGM roic_5y_stability.pct_above index — enrich_ticker's
    # durable_5y fallback source when the Excel roic_5y_avg_pct column is absent.
    qgm_durable_index = load_qgm_durability_index()
    print(f"  Step 3    QGM durability index: {len(qgm_durable_index)} entries (roic_5y_stability.pct_above)")

    # DCA §4 EV map → 5Y annualized IRR per ticker (96/98 typical coverage)
    dca_ev_map = collect_dca_ev_map()
    print(f"  Step 3    DCA EV map: {len(dca_ev_map)} tickers (for 5Y IRR column)")

    # DCA Phase A1 moat trend arrows (94/98 typical coverage; dd-meta rarely carries this)
    dca_trend_map = collect_dca_moat_trend_map()
    print(f"  Step 3    DCA moat-trend map: {len(dca_trend_map)} tickers")

    # Screener daily-cron timing snapshot — same source as flow/ath-hunter.html.
    # US tickers join here; TW/JP/EU stay null (screener is US-only).
    screener_timing = load_screener_timing_map()
    print(f"  Step 3    screener timing map: {len(screener_timing)} tickers (for 起漲點 detection)")

    # Identify DD tickers missing from the screener universe and compute their
    # timing fields via a yfinance batch fetch (fallback path).
    all_dd_tickers = [e["ticker"] for e in universe]
    missing_from_screener = [t for t in all_dd_tickers if t not in screener_timing]
    print(f"  Step 3    timing fallback needed: {len(missing_from_screener)} tickers not in screener universe")
    timing_fallback: dict[str, dict] = {}
    if missing_from_screener:
        timing_fallback = compute_yfinance_timing_fallback(missing_from_screener, screener_timing)
        fb_ok = sum(1 for v in timing_fallback.values() if v.get("dist_52w_high_pct") is not None)
        print(f"  Step 3    timing fallback: {fb_ok}/{len(missing_from_screener)} tickers backfilled")

    # Step 0c: v1.7 — load previous month's EPS snapshot for revision momentum.
    # Module-level cache (_PREV_MONTH_SNAPSHOT_CACHE) prevents re-read per ticker.
    prev_snapshot = _load_prev_month_snapshot()
    has_prev = bool(prev_snapshot.get("tickers"))
    if has_prev:
        print(f"  Step 0    EPS prev-month snapshot: {prev_snapshot.get('for_month')} "
              f"({prev_snapshot.get('xlsx_covered', prev_snapshot.get('succeeded', '?'))}"
              f"/{prev_snapshot.get('universe_size', '?')} tickers)")
    else:
        print("  Step 0    EPS prev-month snapshot: not found (revision_dir=新增 for all)")

    # v4 席位引擎 (2026-09-17): ~90-day-back monthly baseline for eps_rev_3m_pct.
    eps_rev_3m_baseline = _load_eps_rev_3m_baseline()
    if eps_rev_3m_baseline.get("tickers"):
        print(f"  Step 0    EPS 3m-revision baseline: {eps_rev_3m_baseline.get('snapshot_date')} "
              f"({len(eps_rev_3m_baseline.get('tickers') or {})} tickers)")
    else:
        print("  Step 0    EPS 3m-revision baseline: not found (eps_rev_3m_pct=None for all)")

    # Step 0d: v1.8 — load EPS estimates Excel (primary EPS source)
    excel_snapshot = load_latest_excel()
    if excel_snapshot is not None:
        all_dd_tk = [e["ticker"] for e in universe]
        us_adr = {t for t in all_dd_tk if "." not in t}
        # v1.8.3: use alias-aware lookup so 2330.TW resolves to Excel '2330'
        covered = sorted(t for t in all_dd_tk if excel_snapshot.has(t))
        # Exclude SKIP_TICKERS from the "naming mismatch" red callout — those
        # are intentionally dropped at load time (known-bad Koyfin rows), not
        # a naming inconsistency. They still appear in fallback_yf below.
        missing_us = sorted(t for t in us_adr
                            if not excel_snapshot.has(t) and t not in SKIP_TICKERS)
        fallback_yf = sorted(t for t in all_dd_tk if not excel_snapshot.has(t))
        print(f"  Step 0    Excel EPS source: {excel_snapshot.source_file} "
              f"(snapshot {excel_snapshot.snapshot_date}, covers {len(covered)}/{len(all_dd_tk)})")
        if missing_us:
            print(f"  Step 0    Excel missing US/ADR ({len(missing_us)}): {', '.join(missing_us)}")
    else:
        print("  Step 0    Excel EPS source: NOT FOUND in data/eps-estimates/ — all tickers fall back to yfinance")
        missing_us = []
        fallback_yf = [e["ticker"] for e in universe]

    # Step 0e: 2026-09-17 — persistent caches for FX-normalized EPS revision
    # (reporting currency + daily FX rate; see eps_fx_normalize.py). Loaded
    # once, mutated in place (thread-safe) inside enrich_ticker, saved back
    # after the enrichment loop below so rebuilds don't re-hit yfinance for
    # tickers/dates already resolved.
    reporting_ccy_cache = load_reporting_currency_cache()
    fx_cache = load_fx_daily_cache()
    print(f"  Step 0    reporting-currency cache: {len(reporting_ccy_cache)} tickers known "
          f"({sum(1 for v in fx_cache.values() for _ in v)} FX rate(s) cached)")

    # Step 3.5: daily 5y high — single batched yf.download, fresh today for the
    # ATH spotlight on the main page. Weekly ma.high_250w_price stays for
    # backward compat (entry-state.html consumers); the daily fields live
    # alongside it in the same `ma` sub-object.
    daily_5y_map: dict[str, dict] = {}
    if not skip_ma:
        daily_5y_map = compute_daily_5y_highs(all_dd_tickers)

    # Step 3 + 4 enrichment, parallel
    print(f"  Step 3-4  enriching (workers={workers}, skip_ma={skip_ma}) ...")
    enriched: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(enrich_ticker, e, qgm_index, dca_ev_map, dca_trend_map, screener_timing, timing_fallback, skip_ma, ma_cache, quality_cache, prev_snapshot, excel_snapshot, qgm_durable_index, reporting_ccy_cache, fx_cache, eps_rev_3m_baseline): e["ticker"]
            for e in universe
        }
        for i, fut in enumerate(as_completed(futs), 1):
            t = futs[fut]
            try:
                row = fut.result()
                enriched.append(row)
            except Exception as exc:
                print(f"    ERR {t}: {exc}", file=sys.stderr)
            if i % 10 == 0 or i == len(futs):
                elapsed = time.time() - t0
                print(f"    [{i:>3}/{len(futs)}] {elapsed:.0f}s")

    # Step 4.4: persist the reporting-currency / FX caches (new tickers/dates
    # resolved during this run) — best-effort, never blocks the build.
    if not dry_run:
        try:
            save_reporting_currency_cache(reporting_ccy_cache)
            save_fx_daily_cache(fx_cache)
        except Exception as exc:
            print(f"  WARN: failed to save FX/reporting-currency cache: {exc}", file=sys.stderr)

    # Step 4.5: merge daily 5y high fields into ma sub-object (post-enrich so
    # we don't widen enrich_ticker's signature). For tickers whose daily fetch
    # failed, leave keys absent — FE renders the spotlight conservatively.
    if daily_5y_map:
        for row in enriched:
            d5y = daily_5y_map.get(row.get("ticker"))
            if d5y and isinstance(row.get("ma"), dict):
                row["ma"].update(d5y)

    # Step 4.6 (v1.9, v14.3 F4): AR Live — recompute the §11.5 asymmetry ratio
    # at today's price for reports that emit bull/bear targets + probabilities.
    # ar_live = (p_bull × upside%) / (p_bear × downside%); breakout_watch fires
    # when a runway-🟢, moat-not-↓ name's pullback pushes ar_live ≥ 4 — the
    # "觀望等回檔" verdict becomes a standing order instead of a memory item.
    ar_live_count = watch_count = 0
    for row in enriched:
        row["ar_live"] = None
        row["breakout_watch"] = False
        price = (row.get("ma") or {}).get("price")
        vals = (price, row.get("bull_5y_price"), row.get("bear_5y_price"),
                row.get("p_bull_pct"), row.get("p_bear_pct"))
        if not all(isinstance(v, (int, float)) and v > 0 for v in vals):
            continue
        price, bull, bear, p_b, p_br = vals
        up, down = bull / price - 1, 1 - bear / price
        if up <= 0 or down <= 0:
            continue  # price outside [bear, bull] band — scenario tree stale, skip
        row["ar_live"] = round((p_b * up) / (p_br * down), 1)
        ar_live_count += 1
        if (row["ar_live"] >= 4
                and row.get("runway_post_y5") == "🟢"
                and row.get("moat_trend") != "↓"):
            row["breakout_watch"] = True
            watch_count += 1
    print(f"  Step 4.6  AR Live: {ar_live_count} tickers computed, {watch_count} on breakout watch")

    # Step 4.7: 正不對稱三級標記（◆/★★/★）— 純機械描述器，須在 ar_live 算完後跑。
    # 單一權威實作在 compute_asym_flag（門檻與 PREREG 見該 docstring + rule_ledger）。
    asym_counts = Counter()
    for row in enriched:
        row["asym_flag"] = compute_asym_flag(row)
        asym_counts[row["asym_flag"]] += 1
    print(f"  Step 4.7  Asym flags: ◆={asym_counts.get('◆', 0)} "
          f"★★={asym_counts.get('★★', 0)} ★={asym_counts.get('★', 0)}")

    # Step 5: sort (pass/fail already computed above)
    enriched.sort(key=_sort_key)

    # Source-tag breakdown
    src_counts = Counter(s["quality_source"] for s in enriched)
    print(f"  Step 5    quality sources: {dict(src_counts)}")
    ma_fresh = sum(1 for s in enriched if (s.get("ma") or {}).get("price") is not None and not s.get("ma_from_cache"))
    ma_cached = sum(1 for s in enriched if s.get("ma_from_cache"))
    ma_missing = len(enriched) - ma_fresh - ma_cached
    print(f"  Step 5    MA snapshot: fresh={ma_fresh} cached={ma_cached} missing={ma_missing}")
    yf_rows = [s for s in enriched if (s.get("quality_source") or "").startswith("yfinance")]
    q_cached = sum(1 for s in yf_rows if s.get("quality_from_cache"))
    q_wipe = sum(1 for s in yf_rows if all(s.get(k) is None for k in _QUALITY_FIELDS))
    q_fresh = len(yf_rows) - q_cached - q_wipe
    print(f"  Step 5    quality (yfinance path): fresh={q_fresh} cached={q_cached} wiped={q_wipe} (of {len(yf_rows)})")
    # 2026-09-09: koyfin-xlsx rows — relabeled by the roic/fcf Excel override in
    # enrich_ticker(), doesn't overlap with the yfinance/QGM buckets above.
    koyfin_rows = [s for s in enriched if s.get("quality_source") == "koyfin-xlsx"]
    if koyfin_rows:
        k_roic = sum(1 for s in koyfin_rows if s.get("roic") is not None)
        k_fcf = sum(1 for s in koyfin_rows if s.get("fcf") is not None)
        print(f"  Step 5    quality (koyfin-xlsx path): rows={len(koyfin_rows)} roic={k_roic} fcf={k_fcf}")
    print(f"  Step 5    pass distribution: pass5={sum(1 for s in enriched if s['pass_count']==5)} "
          f"pass4={sum(1 for s in enriched if s['pass_count']==4)} "
          f"pass3={sum(1 for s in enriched if s['pass_count']==3)}")

    # 選股系統 v3 (2026-09): universe composition banner — DD vs 待DD (QGM
    # 品質池、dd_status="none") 拆開列印，避免 universe_size 單一數字讓人誤以為
    # 全數都是 DD 報告。
    dd_status_counts = Counter(s.get("dd_status") for s in enriched)
    print(f"  Step 5    universe composition: DD={dd_status_counts.get('dd', 0)} "
          f"待DD={dd_status_counts.get('none', 0)} (total {len(enriched)})")

    # Summary
    pass_counts = Counter(s["pass_count"] for s in enriched)
    no_data = sum(
        1 for s in enriched
        if all(s.get(c["key"]) is None for c in CRITERIA)
    )
    summary = {
        "pass_5":  pass_counts.get(5, 0),
        "pass_4":  pass_counts.get(4, 0),
        "pass_3":  pass_counts.get(3, 0),
        "pass_lt3": sum(v for k, v in pass_counts.items() if k < 3),
        "no_data": no_data,
    }

    # 2026-09-16: ROIC decomposition summary — counts per quadrant, coverage
    # of the incremental-ROIC module, and how many hit "資本縮減" (capital
    # shrank over the 3Y window, e.g. buybacks, so incremental ROIC is
    # undefined). See compute_roic_decomposition().
    quadrant_counts = Counter(s.get("roic_quadrant_code") for s in enriched if s.get("roic_quadrant_code"))
    roic_decomp_summary = {
        "quadrant_hh": quadrant_counts.get("HH", 0),
        "quadrant_hl": quadrant_counts.get("HL", 0),
        "quadrant_lh": quadrant_counts.get("LH", 0),
        "quadrant_ll": quadrant_counts.get("LL", 0),
        "incremental_roic_count": sum(1 for s in enriched if s.get("incremental_roic_pct") is not None),
        "capital_shrink_count": sum(1 for s in enriched if s.get("incremental_roic_note") == "資本縮減"),
    }

    # 2026-09-17: fundamental gates summary — counts per quality_veto_level /
    # decline_signal_light, plus three momentum/valuation flag tallies. See
    # compute_fundamental_gates().
    veto_level_counts = Counter(s.get("quality_veto_level") for s in enriched if s.get("quality_veto_level"))
    decline_light_counts = Counter(s.get("decline_signal_light") for s in enriched if s.get("decline_signal_light"))
    fundamental_gates_summary = {
        "veto_level_maintain": veto_level_counts.get("維持", 0),
        "veto_level_downgrade": veto_level_counts.get("降一級", 0),
        "veto_level_reject": veto_level_counts.get("拒絕", 0),
        "decline_light_green": decline_light_counts.get("🟢", 0),
        "decline_light_yellow": decline_light_counts.get("🟡", 0),
        "decline_light_red": decline_light_counts.get("🔴", 0),
        "decline_light_black": decline_light_counts.get("⛔", 0),
        "pe_vs_5y_high_count": sum(1 for s in enriched if s.get("pe_vs_5y_x") is not None and s["pe_vs_5y_x"] > 1.5),
        "rsi_overheated_count": sum(1 for s in enriched if s.get("rsi14") is not None and s["rsi14"] > 70),
        "return_6m_blocked_count": sum(1 for s in enriched if s.get("return_6m_gate") == "擋下"),
    }

    # 2026-09-17: FunnelRank gate summary — counts for the two new hard/soft
    # processes wired into compute_funnel_rank() (veto_decline_signal /
    # funnel_cap_quality by level / quality_cap_overridden_by_revision).
    quality_cap_level_counts = Counter(
        s.get("funnel_cap_quality_level") for s in enriched if s.get("funnel_cap_quality")
    )
    funnel_gate_summary = {
        "veto_decline_signal_count": sum(1 for s in enriched if s.get("veto_decline_signal")),
        "quality_cap_reject_count": quality_cap_level_counts.get("拒絕", 0),
        "quality_cap_downgrade_count": quality_cap_level_counts.get("降一級", 0),
        "quality_cap_overridden_by_revision_count": sum(
            1 for s in enriched if s.get("quality_cap_overridden_by_revision")
        ),
    }

    # Build final document
    tz_taipei = timezone(timedelta(hours=8))
    now = datetime.now(tz_taipei)
    doc = {
        # v1.3: + FunnelRank (漏斗綜合排序分) per stock — funnel_rank + 3 sub-scores
        # (quality_gate / moat_score_adj / revision_score) + veto/cap/partial flags
        # + peg_fallback. Default sort is now funnel_rank desc. See dd_screener_schema.md.
        "schema_version": "1.3",
        "run_timestamp": now.isoformat(timespec="seconds"),
        "as_of": now.strftime("%Y-%m-%d"),
        "universe_size": len(enriched),
        "default_preset": "MLB",
        "criteria": CRITERIA,
        "presets": PRESETS,
        "default_filter": DEFAULT_FILTER,
        # v1.3: FunnelRank weights/mapping surfaced for the FE methodology panel
        # and audit (per-row sub-scores are computed from these constants).
        "funnel_config": {
            "weights": FUNNEL_WEIGHTS,
            "quality_map": FUNNEL_QUALITY_MAP,
            "forgivable_fails": sorted(FUNNEL_FORGIVABLE_FAILS),
            "moat_trend_mult": FUNNEL_MOAT_TREND_MULT,
            "revision_fy_weights": FUNNEL_REVISION_FY_WEIGHTS,
            "revision_threshold_pct": FUNNEL_REVISION_THRESHOLD,
            "moat_down_cap": FUNNEL_MOAT_DOWN_CAP,
            # 2026-09-17: 體質五項 veto 併入 FunnelRank 的兩個軟性封頂值。
            "quality_reject_cap": FUNNEL_QUALITY_REJECT_CAP,
            "quality_downgrade_cap": FUNNEL_QUALITY_DOWNGRADE_CAP,
        },
        "summary": summary,
        "roic_decomp_summary": roic_decomp_summary,
        "fundamental_gates_summary": fundamental_gates_summary,
        "funnel_gate_summary": funnel_gate_summary,
        "stocks": enriched,
    }
    # v1.8: surface Excel provenance + diff for the FE banner
    if excel_snapshot is not None:
        doc["eps_estimates_source"] = {
            "snapshot_date": excel_snapshot.snapshot_date,
            "source_file": excel_snapshot.source_file,
            "coverage_count": len([t for t in (e["ticker"] for e in universe)
                                    if excel_snapshot.has(t)]),
            "missing_us_adr_tickers": missing_us,
            "fallback_yfinance_tickers": fallback_yf,
        }
    else:
        doc["eps_estimates_source"] = {
            "snapshot_date": None,
            "source_file": None,
            "coverage_count": 0,
            "missing_us_adr_tickers": [],
            "fallback_yfinance_tickers": fallback_yf,
        }

    print(f"\n  ✓ Elapsed: {time.time()-t0:.0f}s")

    if dry_run:
        print(f"  (dry-run) skipping write to {OUTPUT_PATH}")
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Wrote {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size:,} bytes)")

    return doc


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top", type=int, default=None, help="Limit to first N tickers (smoke test)")
    p.add_argument("--no-ma", action="store_true", help="Skip MA fetch (faster smoke)")
    p.add_argument("--dry-run", action="store_true", help="Don't write latest.json")
    p.add_argument("--workers", type=int, default=8, help="Concurrent yfinance fetchers (default 8)")
    p.add_argument("--include-non-dd", action="store_true",
                   help="選股系統 v2: also carry QGM quality-pool tickers with no DD "
                        "(dd_status=none). Default OFF — CI/prod behaviour unchanged "
                        "until deliberately flipped on.")
    args = p.parse_args()
    build(top_n=args.top, skip_ma=args.no_ma, dry_run=args.dry_run, workers=args.workers,
          include_non_dd=args.include_non_dd)

    # Discovery pool refresh (v2.4 chain): "ID 標 🔴 核心受益但尚未建 DD" 名單
    # → docs/dd-screener/discovery_pool.json，供 /dd-screener/ 折疊區塊渲染。
    # 純本地掃描（id-meta + DD 檔名），不碰網路；失敗只 warn 不 abort（同
    # yfinance-failure 政策 — screener 主表永遠優先）。
    if not args.dry_run:
        try:
            from list_breakout_candidates import write_pool
            pool_path = write_pool()
            print(f"  ✓ Discovery pool refreshed: {pool_path}")
        except Exception as exc:  # noqa: BLE001
            print(f"  ⚠ Discovery pool refresh failed (non-fatal): {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
