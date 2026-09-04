#!/usr/bin/env python3
"""dd_decision.py — v16 WP1b 決策矩陣機械路由器（0 LLM，stdlib only）。

把 `.claude/skills/stock-analyst/references/decision-layer.md` 的決策矩陣
（rows 1-10，含 row 4/5 節奏調節、row 7a/7b 軟否決、row 8a/8b 條件式進場）
逐字翻譯成可執行的路由函式。**本檔是翻譯，不是修訂**——任何條件的語意、
門檻數字、優先序，一律照 decision-layer.md 原文，不得因為要湊 backtest
對齊而改變判斷方向。

輸入契約：見 `scripts/dd_schema/decision_inputs.md`（WP1b 交付物之一）。

用法：
  python3 scripts/dd_decision.py run INPUT.json [--html OUT.html] [--json OUT.json]
  python3 scripts/dd_decision.py check DD.html [--infer-from-html]
  python3 scripts/dd_decision.py check-all [--glob 'docs/dd/DD_*.html'] [--infer-from-html]

矩陣 rows 1-10 之外仍有兩層覆寫（見 `decision_inputs.md` §2.4，2026-09 追加）：
  - §11 4b.1 分母爭議檢查（`val_denominator_disputed`）——估值燈機械讀數可能因
    分母爭議被判定不可用；已內建於 `_evaluate_matrix` 的 baseline 段（rows
    8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望）。
  - QC-49 裁決 hysteresis（`qc49_inherit_prior`/`prior_verdict`/`prior_role`）
    ——90 天內翻面須引前次已發火觸發器，否則承繼前裁決；在 `evaluate()` 內
    矩陣算完「之後」套用。**本腳本不做觸發器查證**，`qc49_inherit_prior=true`
    是「已查證過、確定引不出觸發器」的既成事實輸入。
  - `held_now`（既有持倉時觀望裁決的 role 例外）同樣在 `evaluate()` 內矩陣
    輸出之後套用，只影響 role 不影響 verdict。
  三者皆為矩陣「之前/之後」的覆寫，**矩陣 rows 1-10 本身語意仍一字不動**。
  三個欄位若全部缺值（`null`），`evaluate()` 的行為與只有 `_evaluate_matrix`
  時完全相同（純矩陣機械輸出）。

  **仍刻意不做**：`DD_5398KL_20260811.html` 的 row1「signal=X 但報告從輕發落
  到觀望」——這是報告偏離矩陣字面本身（非覆寫層問題），不得為了對齊而修改
  row1 語意，見 decision_inputs.md §4 與 §5 矛盾點 #1。
"""
from __future__ import annotations

import argparse
import glob as globmod
import html as html_lib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

SIGNAL_RANK = {"X": 0, "C": 1, "B": 2, "A": 3, "A+": 4}
MOAT_RANK = {"S": 0, "A": 1, "B": 2, "C": 3, "X": 4}
VAL_GREEN_YELLOW = ("🟢", "🟡")
VAL_ORANGE_RED = ("🟠", "🔴")
MA_GREEN = ("🟢", "✅")
MA_MID = ("🟡", "🟠", "-")
MA_RED = "❌"
CYCLE_POS_EARLY = ("深谷投降", "早循環")
CYCLICAL_RE = re.compile(r"循環|商品|EMS/ODM")

DD_META_RE = re.compile(
    r'<script\s+id="dd-meta"\s+type="application/json"\s*>(.*?)</script>', re.DOTALL
)


# ---------------------------------------------------------------------------
# 決策矩陣核心：evaluate(inputs) -> decision_out dict
# ---------------------------------------------------------------------------

def _audit(rows, row, cond, hit, basis, gap=None, inferred=False):
    entry = {"row": row, "condition": cond, "hit": hit, "basis": basis}
    if gap:
        entry["input_gap"] = gap if isinstance(gap, list) else [gap]
    if inferred:
        entry["inferred_from_html"] = True
    rows.append(entry)
    return entry


def _evaluate_matrix(inputs: dict) -> dict:
    """決策矩陣 rows 1-10 本體（含 row4/5 節奏調節、row7a/7b 軟否決、row8a/8b）
    ＋§11 4b.1 分母爭議檢查（在 baseline 段內套用，因為它改變的是 rows 8/9/9b/10
    讀 `val` 的方式，屬矩陣求值的一部分，不是矩陣輸出後的覆寫）。
    QC-49 裁決 hysteresis 與 held_now role 例外**不在此函式**，由外層 `evaluate()`
    在矩陣算完之後套用——見該函式docstring 的覆蓋層順序說明。
    """
    audit_rows = []

    signal = inputs.get("signal")
    val = inputs.get("val")
    ma = inputs.get("ma")
    runway = inputs.get("runway_post_y5")
    moat_trend = inputs.get("moat_trend")
    moat = inputs.get("moat")
    capalloc = inputs.get("capalloc_grade")
    archetype = inputs.get("archetype") or ""
    cycle_position = inputs.get("cycle_position")
    thesis_irreconcilable = inputs.get("thesis_irreconcilable")
    valuation_dependent = inputs.get("valuation_dependent")
    market_wrong_reason_given = inputs.get("market_wrong_reason_given")
    week26 = inputs.get("week26_return_pct")
    momentum_overheated = inputs.get("momentum_overheated")
    cycle_gates_pass = inputs.get("cycle_gates_pass")
    consensus_rev = inputs.get("consensus_rev_3m_pct")
    role_hint = inputs.get("role_hint")

    sig_rank = SIGNAL_RANK.get(signal, -1)
    moat_rank = MOAT_RANK.get(moat)

    pacing = []
    holding_cap = None
    requires_critic = []

    # ---- Hard Veto rows 1-3 (max-severity: first hit wins, but we record all) ----
    hard_veto_row = None

    hit1 = signal == "X"
    _audit(audit_rows, "1", "基本面評級 signal = X → 迴避", hit1, f"signal={signal!r}")
    if hit1 and hard_veto_row is None:
        hard_veto_row = "1"

    if thesis_irreconcilable is None:
        _audit(
            audit_rows, "2", "§11 強制裁決：thesis 不可調和不成立 → 迴避", False,
            "輸入缺(thesis_irreconcilable=null)，依保守方向處理：不視為觸發（不manufacture一個查不到證據的否決）",
            gap="thesis_irreconcilable",
        )
    else:
        hit2 = bool(thesis_irreconcilable)
        _audit(
            audit_rows, "2", "§11 強制裁決：thesis 不可調和不成立 → 迴避", hit2,
            f"thesis_irreconcilable={thesis_irreconcilable}",
        )
        if hit2 and hard_veto_row is None:
            hard_veto_row = "2"

    hit3 = (moat_trend == "↓") and (moat_rank is not None and moat_rank >= MOAT_RANK["B"])
    _audit(
        audit_rows, "3", "moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避", hit3,
        f"moat_trend={moat_trend!r}, moat={moat!r}"
        + ("" if moat_rank is not None else "（moat 未提供，視為不觸發）"),
    )
    if hit3 and hard_veto_row is None:
        hard_veto_row = "3"

    # ---- Row 4/5 節奏調節（非裁決閘，永遠評估、永遠疊加） ----
    hit4 = ma == MA_RED
    _audit(audit_rows, "4", "週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）", hit4, f"ma={ma!r}")
    if hit4:
        pacing.append("row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」")

    if momentum_overheated is None:
        _audit(
            audit_rows, "5", "動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）", False,
            "輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發",
            gap="momentum_overheated",
        )
    else:
        hit5 = bool(momentum_overheated)
        _audit(audit_rows, "5", "動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）", hit5,
               f"momentum_overheated={momentum_overheated}")
        if hit5:
            pacing.append("row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」")

    if hard_veto_row:
        verdict = "迴避"
        row_hit = hard_veto_row
        role = "不持有"
        return {
            "verdict": verdict,
            "role": role,
            "row_hit": row_hit,
            "pacing": pacing,
            "holding_cap": holding_cap,
            "requires_critic": requires_critic,
            "audit_rows": audit_rows,
        }

    # ---- Soft Veto rows 6/7/7a（上限觀望）+ 7b（只設持有年限上限，不降裁決） ----
    soft_veto_rows = []

    hit6 = signal == "C"
    _audit(audit_rows, "6", "基本面評級 signal = C → ≥ 觀望", hit6, f"signal={signal!r}")
    if hit6:
        soft_veto_rows.append("6")

    hit7 = runway == "🔴"
    _audit(audit_rows, "7", "runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）", hit7,
           f"runway_post_y5={runway!r}")
    if hit7:
        soft_veto_rows.append("7")

    if valuation_dependent is None or market_wrong_reason_given is None:
        gaps = [k for k, v in (
            ("valuation_dependent", valuation_dependent),
            ("market_wrong_reason_given", market_wrong_reason_given),
        ) if v is None]
        _audit(
            audit_rows, "7a",
            "§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年",
            False, "輸入缺，依保守方向處理：不視為觸發", gap=gaps,
        )
    else:
        hit7a = bool(valuation_dependent) and not bool(market_wrong_reason_given)
        _audit(
            audit_rows, "7a",
            "§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年",
            hit7a,
            f"valuation_dependent={valuation_dependent}, market_wrong_reason_given={market_wrong_reason_given}",
        )
        if hit7a:
            soft_veto_rows.append("7a")
            holding_cap = "中期 2-5 年"

    hit7b = capalloc == "C"
    _audit(audit_rows, "7b", "dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）",
           hit7b, f"capalloc_grade={capalloc!r}")
    if hit7b:
        holding_cap = "中期 2-5 年"

    has_soft_veto = len(soft_veto_rows) > 0

    # ---- Row 8a（Baseline·爆發候選；row6/7/7a soft veto 一律封鎖 8a） ----
    row8a_hit = False
    row8a_gaps = []
    row8a_eligible_base = (
        not has_soft_veto
        and sig_rank >= SIGNAL_RANK["B"]
        and runway == "🟢"
        and val in VAL_ORANGE_RED
        and moat_trend != "↓"
    )
    row8a_disqualified = False
    if row8a_eligible_base:
        if valuation_dependent is None:
            row8a_gaps.append("valuation_dependent")
        elif valuation_dependent:
            row8a_disqualified = True
        if week26 is None:
            row8a_gaps.append("week26_return_pct")
        elif week26 > 150:
            row8a_disqualified = True
        elif week26 >= 100:
            row8a_gaps.append("week26_return_pct 落 100-150% 邊界帶，QC-42 反動能閘裁量範圍，本腳本無法自動判定，預設不放行")
        row8a_hit = row8a_eligible_base and not row8a_disqualified and not row8a_gaps
    _audit(
        audit_rows, "8a",
        "無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + "
        "非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）",
        row8a_hit,
        f"signal={signal!r}, runway={runway!r}, val={val!r}, moat_trend={moat_trend!r}, week26={week26!r}, "
        f"valuation_dependent={valuation_dependent!r}",
        gap=row8a_gaps or None,
    )

    if row8a_hit:
        verdict = "進場·條件式（爆發候選）"
        row_hit = "8a"
        role = "衛星"
        requires_critic.append("QC-48")
        return {
            "verdict": verdict, "role": role, "row_hit": row_hit,
            "pacing": pacing, "holding_cap": holding_cap,
            "requires_critic": requires_critic, "audit_rows": audit_rows,
        }

    # ---- Row 8b（Baseline·循環衛星；可越過 6/7 soft veto，但已無 Hard Veto） ----
    cyclical = bool(CYCLICAL_RE.search(archetype))
    pos_ok = cycle_position in CYCLE_POS_EARLY
    moat_baseline_ok = (moat != "X") and not (moat_trend == "↓" and moat == "C")
    row8b_gaps = []
    row8b_hit = False
    row8b_eligible_partial = cyclical and pos_ok and moat_baseline_ok
    if row8b_eligible_partial:
        if cycle_gates_pass is None:
            row8b_gaps.append("cycle_gates_pass")
        else:
            row8b_hit = bool(cycle_gates_pass)
    _audit(
        audit_rows, "8b",
        "無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + "
        "moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）",
        row8b_hit,
        f"archetype={archetype!r}, cycle_position={cycle_position!r}, moat={moat!r}, moat_trend={moat_trend!r}, "
        f"cycle_gates_pass={cycle_gates_pass!r}",
        gap=row8b_gaps or None,
    )

    if row8b_hit:
        verdict = "進場·條件式（循環衛星）"
        row_hit = "8b"
        role = "衛星"
        requires_critic.append("循環位置獨立critic(同QC-42/QC-48機制)")
        return {
            "verdict": verdict, "role": role, "row_hit": row_hit,
            "pacing": pacing, "holding_cap": holding_cap,
            "requires_critic": requires_critic, "audit_rows": audit_rows,
        }

    # ---- Soft Veto 生效（8a/8b 皆未命中） ----
    if has_soft_veto:
        verdict = "觀望"
        row_hit = ",".join(soft_veto_rows)
        role = role_hint if role_hint else "追蹤"
        if signal == "C" and "6" not in ("",):
            pass
        _audit(
            audit_rows, "6/7/7a-verdict", "Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）",
            True, f"soft_veto_rows={soft_veto_rows}",
        )
        # QC-50 錯過成本反向 critic（觀望的唯一向上通道）——僅能用 consensus_rev_3m_pct 判定
        # 其一觸發條件（前次觀望/迴避 to-date >+30% 需 q.py 歷史，非本腳本輸入範圍內，見
        # decision_inputs.md「已知範圍外」）。
        if consensus_rev is not None and consensus_rev >= 10:
            requires_critic.append("QC-50")
        return {
            "verdict": verdict, "role": role, "row_hit": row_hit,
            "pacing": pacing, "holding_cap": holding_cap,
            "requires_critic": requires_critic, "audit_rows": audit_rows,
        }

    # ---- Baseline rows 8/9/9b/10（無 Veto） ----
    val_denominator_disputed = inputs.get("val_denominator_disputed")
    if val_denominator_disputed is True:
        _audit(
            audit_rows, "11.4b-denom",
            "§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 "
            "的估值條件視為不可判 → 落 row8 觀望（保守方向）",
            True, f"val_denominator_disputed=True, val(機械讀數)={val!r}",
        )
        verdict = "觀望"
        row_hit = "8(val爭議)"
        role = role_hint if role_hint else "追蹤"
        return {
            "verdict": verdict, "role": role, "row_hit": row_hit,
            "pacing": pacing, "holding_cap": holding_cap,
            "requires_critic": requires_critic, "audit_rows": audit_rows,
        }
    elif val_denominator_disputed is None:
        _audit(
            audit_rows, "11.4b-denom",
            "§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）",
            False, "輸入缺(val_denominator_disputed=null)，依保守方向處理：不視為觸發（沿用 val 機械讀數）",
            gap="val_denominator_disputed",
        )
    else:
        _audit(
            audit_rows, "11.4b-denom",
            "§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）",
            False, "val_denominator_disputed=False",
        )

    val_le_yellow = val in VAL_GREEN_YELLOW
    val_stretched = val in VAL_ORANGE_RED
    ma_green = ma in MA_GREEN
    ma_mid = ma in MA_MID
    ma_red = ma == MA_RED

    hit8 = sig_rank >= SIGNAL_RANK["B"] and val_stretched
    _audit(audit_rows, "8", "無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）", hit8,
           f"signal={signal!r}, val={val!r}")

    row10_hit = sig_rank >= SIGNAL_RANK["A"] and val_le_yellow and (ma_green or ma_red)
    row9_hit = (not row10_hit) and sig_rank >= SIGNAL_RANK["B"] and val_le_yellow and (ma_green or ma_red)
    row9b_hit = (
        (not row10_hit) and (not row9_hit)
        and sig_rank >= SIGNAL_RANK["B"] and val_le_yellow and ma_mid
    )

    _audit(audit_rows, "9", "無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅} → 進場", row9_hit,
           f"signal={signal!r}, val={val!r}, ma={ma!r}")
    _audit(audit_rows, "9b", "無 Veto + signal≥B + val≤🟡 + MA∈{🟡,🟠,-}（W250斜率未轉負）→ 進場·條件式（長波段佈局）",
           row9b_hit, f"signal={signal!r}, val={val!r}, ma={ma!r}")
    _audit(audit_rows, "10", "無 Veto + signal≥A + MA∈{🟢,✅} + val∈{🟢,🟡} → 進場", row10_hit,
           f"signal={signal!r}, val={val!r}, ma={ma!r}")

    if row10_hit or row9_hit:
        # row9/10 皆映射 dd-meta dca_verdict=「進場」（plain，enum 無 baseline 條件式變體）
        chosen = "10" if row10_hit else "9"
        exception_note = None
        if ma_red:
            exception_note = (
                "MA=❌ 但 signal≥B 且 val≤🟡 且無 Veto：依「baseline rows 9/9b/10 的 MA 條件字面不含 ❌ 時，"
                "該組合不落空、不降觀望——按對應 val 燈 baseline row 裁決，MA❌ 僅作 row4 節奏調節」推論，"
                "verdict=進場（row4 pacing 已疊加，見上）"
            )
        verdict = "進場"
        row_hit = chosen + ("（MA❌例外）" if ma_red else "")
        if role_hint:
            role = role_hint
        else:
            role = "核心" if (sig_rank >= SIGNAL_RANK["A"] and moat_trend != "↓") else "衛星"
        entry = _audit(audit_rows, f"{chosen}-verdict", "命中 row" + chosen + " → 進場", True,
                        exception_note or f"row_hit={chosen}")
        return {
            "verdict": verdict, "role": role, "row_hit": row_hit,
            "pacing": pacing, "holding_cap": holding_cap,
            "requires_critic": requires_critic, "audit_rows": audit_rows,
        }

    if row9b_hit:
        verdict = "進場"  # dd-meta dca_verdict enum 無獨立值；row9b 的條件式語意只落在 §13a 執行語
        row_hit = "9b"
        role = role_hint if role_hint else "衛星"
        return {
            "verdict": verdict, "role": role, "row_hit": row_hit,
            "pacing": pacing, "holding_cap": holding_cap,
            "requires_critic": requires_critic, "audit_rows": audit_rows,
        }

    if hit8:
        verdict = "觀望"
        row_hit = "8"
        role = role_hint if role_hint else "追蹤"
        return {
            "verdict": verdict, "role": role, "row_hit": row_hit,
            "pacing": pacing, "holding_cap": holding_cap,
            "requires_critic": requires_critic, "audit_rows": audit_rows,
        }

    # 理論上不應到達——所有已知 (signal,val,ma) 組合應被 8/9/9b/10 之一覆蓋；
    # 到這裡代表輸入落在矩陣未涵蓋的角落（例如 val 缺值），誠實回報 unresolved。
    _audit(audit_rows, "unresolved", "無 row 命中——輸入組合落在矩陣文字未涵蓋角落", True,
           f"signal={signal!r}, val={val!r}, ma={ma!r}, runway={runway!r}")
    return {
        "verdict": "unresolved",
        "role": role_hint or "追蹤",
        "row_hit": "none",
        "pacing": pacing,
        "holding_cap": holding_cap,
        "requires_critic": requires_critic,
        "audit_rows": audit_rows,
    }


def _role_heuristic(final_verdict, sig_rank, moat_trend):
    """矩陣以外的 role 預設啟發式（見 decision_inputs.md §3），供 QC-49 override
    在 prior_role 缺值時的 fallback。"""
    if final_verdict == "迴避":
        return "不持有"
    if final_verdict == "觀望":
        return "追蹤"
    if isinstance(final_verdict, str) and final_verdict.startswith("進場"):
        return "核心" if (sig_rank >= SIGNAL_RANK["A"] and moat_trend != "↓") else "衛星"
    return "追蹤"


def evaluate(inputs: dict) -> dict:
    """對外唯一入口。覆蓋層順序（coordinator 2026-09 追加，矩陣 rows 1-10 語意仍
    一字不動——三層都是矩陣「之前/之後」的覆寫，非新矩陣列）：

      1. §11 4b.1 分母爭議 —— 已內建於 `_evaluate_matrix` 的 baseline 段（改變的
         是 rows 8/9/9b/10 怎麼讀 `val`，屬矩陣求值本身的一部分）。
      2. 矩陣 rows 1-10 —— `_evaluate_matrix`。
      3. QC-49 裁決 hysteresis —— 矩陣算完「之後」，若 90 天內翻面且引不出前次
         已發火觸發器 → 承繼前次裁決（此處以 `qc49_inherit_prior`/`prior_verdict`
         模擬「引不出觸發器」的既成事實，本腳本不做觸發器查證）。
      4. held_now role 例外 —— 觀望但現持有此檔（既有持倉條款）時 role 沿用
         `prior_role`，而非預設的「追蹤」。
    """
    out = _evaluate_matrix(inputs)
    audit_rows = out["audit_rows"]

    signal = inputs.get("signal")
    moat_trend = inputs.get("moat_trend")
    sig_rank = SIGNAL_RANK.get(signal, -1)
    role_hint = inputs.get("role_hint")

    # ---- 3. QC-49 裁決 hysteresis（矩陣輸出之後） ----
    qc49_inherit = inputs.get("qc49_inherit_prior")
    prior_verdict = inputs.get("prior_verdict")
    prior_role = inputs.get("prior_role")

    def _bucket(v):
        if not v:
            return None
        return "進場" if v.startswith("進場") else v

    if qc49_inherit is None:
        _audit(
            audit_rows, "QC-49",
            "90 天內翻面須引前次已發火觸發器，否則承繼前次裁決", False,
            "輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）",
            gap="qc49_inherit_prior",
        )
    elif qc49_inherit is True:
        if prior_verdict is None:
            _audit(
                audit_rows, "QC-49", "qc49_inherit_prior=True 但 prior_verdict 缺，無法承繼", False,
                "輸入缺(prior_verdict=null)，依保守方向處理：不套用（維持矩陣機械輸出）",
                gap="prior_verdict",
            )
        elif _bucket(prior_verdict) == _bucket(out["verdict"]):
            _audit(
                audit_rows, "QC-49", "qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼",
                False, f"prior_verdict={prior_verdict!r}, 矩陣機械輸出={out['verdict']!r}",
            )
        else:
            _audit(
                audit_rows, "QC-49",
                f"QC-49 承繼前次裁決（矩陣機械輸出＝{out['verdict']}／row{out['row_hit']}，"
                f"前次裁決＝{prior_verdict}，90 天內翻面查無已發火觸發器）",
                True, f"qc49_inherit_prior=True, prior_verdict={prior_verdict!r}",
            )
            out["row_hit"] = f"{out['row_hit']}→QC-49({prior_verdict})"
            out["verdict"] = prior_verdict
            if not role_hint:
                out["role"] = prior_role if prior_role else _role_heuristic(prior_verdict, sig_rank, moat_trend)
    else:
        _audit(audit_rows, "QC-49", "qc49_inherit_prior=False，不套用", False, "qc49_inherit_prior=False")

    # ---- 4. held_now：觀望但現持有此檔（既有持倉條款）→ role 沿用 prior_role ----
    held_now = inputs.get("held_now")
    if out["verdict"] == "觀望" and not role_hint:
        if held_now is True:
            if prior_role:
                _audit(
                    audit_rows, "role-held_now",
                    "觀望但 held_now=True（既有持倉／現持有）→ role 沿用 prior_role，而非預設追蹤",
                    True, f"held_now=True, prior_role={prior_role!r}",
                )
                out["role"] = prior_role
            else:
                _audit(
                    audit_rows, "role-held_now",
                    "觀望且 held_now=True 但 prior_role 缺，無法沿用，維持預設角色", False,
                    "輸入缺(prior_role=null)", gap="prior_role",
                )
        elif held_now is None:
            _audit(
                audit_rows, "role-held_now",
                "觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role", False,
                "輸入缺(held_now=null)，依保守方向處理：維持預設追蹤",
                gap="held_now",
            )
        else:
            _audit(audit_rows, "role-held_now", "held_now=False → 非既有持倉，role 維持預設追蹤", False,
                   "held_now=False")

    return out


# ---------------------------------------------------------------------------
# 呈現層：<details class="audit"> 片段
# ---------------------------------------------------------------------------

def build_audit_html(decision_out: dict) -> str:
    lines = ['<details class="audit">', "<summary>決策矩陣逐 row 檢核（機械輸出）</summary>", "<table>"]
    lines.append("<tr><th>Row</th><th>條件</th><th>命中</th><th>依據</th><th>備註</th></tr>")
    for r in decision_out["audit_rows"]:
        note_bits = []
        if r.get("input_gap"):
            note_bits.append("輸入缺：" + "、".join(r["input_gap"]))
        if r.get("inferred_from_html"):
            note_bits.append("（--infer-from-html 推斷）")
        note = html_lib.escape("；".join(note_bits))
        lines.append(
            "<tr><td>{row}</td><td>{cond}</td><td>{hit}</td><td>{basis}</td><td>{note}</td></tr>".format(
                row=html_lib.escape(str(r["row"])),
                cond=html_lib.escape(r["condition"]),
                hit=("✓" if r["hit"] else "—"),
                basis=html_lib.escape(r["basis"]),
                note=note,
            )
        )
    lines.append("</table>")
    lines.append(
        "<p>結論：verdict={verdict}／role={role}／row_hit={row_hit}"
        "{pacing}{cap}{critic}</p>".format(
            verdict=html_lib.escape(decision_out["verdict"]),
            role=html_lib.escape(decision_out["role"]),
            row_hit=html_lib.escape(str(decision_out["row_hit"])),
            pacing=("；pacing：" + html_lib.escape("；".join(decision_out["pacing"])) if decision_out["pacing"] else ""),
            cap=("；holding_cap：" + html_lib.escape(decision_out["holding_cap"]) if decision_out["holding_cap"] else ""),
            critic=("；requires_critic：" + html_lib.escape("、".join(decision_out["requires_critic"])) if decision_out["requires_critic"] else ""),
        )
    )
    lines.append("</details>")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# check：從既有 dd-meta 抽 decision_inputs，跑矩陣，比對 dca_verdict/dca_role
# ---------------------------------------------------------------------------

DD_META_TO_INPUT_KEYS = (
    "signal", "trap", "val", "ma", "runway_post_y5", "moat_trend",
    "capalloc_grade", "archetype", "cycle_position", "cycle_verdict",
    "asym_ratio", "irr_base_pct", "ev5y_pct", "price_at_dd",
)

NON_DD_META_KEYS = (
    "thesis_irreconcilable", "valuation_dependent", "market_wrong_reason_given",
    "week26_return_pct", "momentum_overheated", "cycle_gates_pass",
    "consensus_rev_3m_pct", "role_hint",
    # 2026-09 coordinator 追加（矩陣「之前/之後」的覆寫層，見 evaluate() docstring）：
    "val_denominator_disputed", "qc49_inherit_prior", "prior_verdict", "prior_role",
    "held_now",
)


def _load_meta_from_html(html_text: str):
    m = DD_META_RE.search(html_text)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


# --- infer-from-html：盡力推斷，預設關；命中一律在 audit 標記 inferred ---

_VALDEP_RE = re.compile(r"估值依賴型")
_VALDEP_YES_RE = re.compile(r"(屬於|是|標記為?)?估值依賴型|估值依賴型[^。\n]{0,6}(成立|是)")
_VALDEP_NO_RE = re.compile(r"(非|不構成|不屬於)估值依賴型")
_MARKET_WRONG_RE = re.compile(r"市場錯在")
_WEEK26_RE = re.compile(r"26\s*週(?:漲幅|報酬)[^0-9+\-%]{0,6}([+\-]?\d+(?:\.\d+)?)\s*%")
_MOMENTUM_RE = re.compile(r"(RSI\s*\(?14\)?\D{0,10}(\d+(?:\.\d+)?)|4\s*週(?:漂移|價格漂移)[^0-9+\-%]{0,6}([+\-]?\d+(?:\.\d+)?)\s*%)")
# NOTE（backtest 實測發現）：row2 的條件文字本身（「thesis 不可調和不成立」）幾乎逐字
# 出現在每份 v15 DD 自己渲染的 <details class="audit"> 矩陣稽核表「條件」欄（即使該
# row 明明「未命中」），對此字串做裸 substring 搜尋等於在搜自己的條件標籤，precision
# 極低（backtest 中造成 5/31 誤判為迴避）。目前沒有夠可靠的正則能分辨「條件敘述」與
# 「肯定結論」，故此欄**刻意不做 HTML 推斷**，一律留 null，交由 audit_rows 標記
# input_gap；需要更精準判定時應等 WP1c 判斷物 JSON 直接寫 `thesis_irreconcilable`
# 欄位（不再依賴散文正則）。

# ── 2026-09 coordinator 追加三欄的推斷 regex ──────────────────────────────
# `分母爭議成立` 是精確片語（非泛用「分母爭議」——後者是 §11 4b.1 checklist 每份
# v15 報告都會渲染的條件標籤，裸字會全庫誤命中；backtest 對 31 份 schema=v15 檔
# 全掃「分母爭議成立」只命中 1 份〔MELI，即本欄設計對應的真實案例〕，precision 高）。
_VALDEP_DISPUTED_TRUE_RE = re.compile(r"分母爭議成立")
# QC-49 觸發語（coordinator 指定的兩個片語 + 報告常見的「裁決一致性覆寫」標題）。
_QC49_INHERIT_RE = re.compile(r"依QC-49承繼|承繼前次裁決|裁決一致性覆寫")
# 取文件中第一個「承繼前次裁決（X）」或「維持X」——document order 上第一個出現的
# 具體 verdict 詞，backtest 驗證對 MRVL（「維持迴避」出現在「維持觀望」之後，取
# 第一個即正確）／SBUX／MELI 三案例皆準確。
_QC49_PRIOR_VERDICT_RE = re.compile(r"承繼前次裁決（(進場|觀望|迴避)）|維持(進場|觀望|迴避)")
_HELD_NOW_RE = re.compile(r"既有持倉|現有持倉|既有部位|現有部位")
_PRIOR_ROLE_RE = re.compile(r"(?:投資組合角色|組合角色（?dca_role）?)\D{0,10}(核心|衛星|追蹤|不持有)")


def infer_from_html(text: str, base_inputs: dict) -> dict:
    """在 base_inputs 缺值處，用正則從 HTML 正文盡力推斷；命中一律標記於回傳的
    `_inferred` 集合供呼叫端在 audit 加註記。不覆蓋 base_inputs 已有的非 null 值。
    """
    inferred = dict(base_inputs)
    marks = set()
    plain = re.sub(r"<[^>]+>", "", text)

    if inferred.get("valuation_dependent") is None:
        if _VALDEP_NO_RE.search(plain):
            inferred["valuation_dependent"] = False
            marks.add("valuation_dependent")
        elif _VALDEP_YES_RE.search(plain) or ("re-rate" in plain.lower() and _VALDEP_RE.search(plain)):
            # 只在明確出現「估值依賴型」字樣且非「非估值依賴型」時才判 True
            if _VALDEP_RE.search(plain) and not _VALDEP_NO_RE.search(plain):
                inferred["valuation_dependent"] = True
                marks.add("valuation_dependent")

    if inferred.get("market_wrong_reason_given") is None:
        if _MARKET_WRONG_RE.search(plain):
            inferred["market_wrong_reason_given"] = True
            marks.add("market_wrong_reason_given")

    if inferred.get("week26_return_pct") is None:
        m = _WEEK26_RE.search(plain)
        if m:
            try:
                inferred["week26_return_pct"] = float(m.group(1))
                marks.add("week26_return_pct")
            except ValueError:
                pass

    if inferred.get("momentum_overheated") is None:
        m = _MOMENTUM_RE.search(plain)
        if m:
            rsi = m.group(2)
            drift = m.group(3)
            overheated = False
            if rsi and float(rsi) > 70:
                overheated = True
            if drift and float(drift) > 10:
                overheated = True
            inferred["momentum_overheated"] = overheated
            marks.add("momentum_overheated")

    # thesis_irreconcilable：刻意不做 HTML 推斷（見上方 NOTE），永遠留 null。

    if inferred.get("val_denominator_disputed") is None:
        if _VALDEP_DISPUTED_TRUE_RE.search(plain):
            inferred["val_denominator_disputed"] = True
            marks.add("val_denominator_disputed")

    if inferred.get("qc49_inherit_prior") is None:
        if _QC49_INHERIT_RE.search(plain):
            inferred["qc49_inherit_prior"] = True
            marks.add("qc49_inherit_prior")
            if inferred.get("prior_verdict") is None:
                vm = _QC49_PRIOR_VERDICT_RE.search(plain)
                if vm:
                    inferred["prior_verdict"] = vm.group(1) or vm.group(2)
                    marks.add("prior_verdict")

    if inferred.get("held_now") is None:
        if _HELD_NOW_RE.search(plain):
            inferred["held_now"] = True
            marks.add("held_now")
            if inferred.get("prior_role") is None:
                rm = _PRIOR_ROLE_RE.search(plain)
                if rm:
                    inferred["prior_role"] = rm.group(1)
                    marks.add("prior_role")

    inferred["_inferred_keys"] = sorted(marks)
    return inferred


def decision_inputs_from_meta(meta: dict) -> dict:
    d = {k: meta.get(k) for k in DD_META_TO_INPUT_KEYS}
    d["moat"] = meta.get("moat")
    for k in NON_DD_META_KEYS:
        d[k] = None
    return d


def cmd_check(html_path: str, infer=False, quiet=False) -> dict:
    p = Path(html_path)
    text = p.read_text(encoding="utf-8", errors="ignore")
    meta = _load_meta_from_html(text)
    if meta is None:
        return {"file": p.name, "status": "no-dd-meta"}
    inputs = decision_inputs_from_meta(meta)
    inferred_keys = []
    if infer:
        inputs = infer_from_html(text, inputs)
        inferred_keys = inputs.pop("_inferred_keys", [])
    out = evaluate(inputs)
    actual_verdict = meta.get("dca_verdict")
    actual_role = meta.get("dca_role")
    computed_verdict = out["verdict"]
    match = (computed_verdict == actual_verdict)
    result = {
        "file": p.name,
        "ticker": meta.get("ticker"),
        "computed_verdict": computed_verdict,
        "actual_verdict": actual_verdict,
        "computed_role": out["role"],
        "actual_role": actual_role,
        "row_hit": out["row_hit"],
        "match": match,
        "inferred_keys": inferred_keys,
        "decision_out": out,
    }
    if not quiet:
        tag = "MATCH" if match else "MISMATCH"
        print(f"[{tag}] {p.name} ticker={meta.get('ticker')} "
              f"computed={computed_verdict}(row{out['row_hit']}) actual={actual_verdict} "
              f"role: computed={out['role']} actual={actual_role}"
              + (f" inferred={inferred_keys}" if inferred_keys else ""))
    return result


def cmd_check_all(glob_pat: str, infer=False) -> int:
    files = sorted(globmod.glob(glob_pat))
    in_scope = []
    for f in files:
        text = Path(f).read_text(encoding="utf-8", errors="ignore")
        if re.search(r'"schema"\s*:\s*"v15', text):
            in_scope.append(f)

    rows = []
    n_match = 0
    for f in in_scope:
        r = cmd_check(f, infer=infer, quiet=True)
        if r.get("status") == "no-dd-meta":
            continue
        rows.append(r)
        if r["match"]:
            n_match += 1

    print(f"{'檔名':<32}{'dd-meta裁決':<14}{'腳本裁決':<20}{'row_hit':<10}{'相同':<6}")
    print("-" * 90)
    for r in rows:
        print(
            f"{r['file']:<32}{str(r['actual_verdict']):<14}{str(r['computed_verdict']):<20}"
            f"{str(r['row_hit']):<10}{'✓' if r['match'] else '✗':<6}"
        )
    print("-" * 90)
    print(f"{n_match}/{len(rows)} 相同")

    mismatches = [r for r in rows if not r["match"]]
    if mismatches:
        print()
        print("Mismatch 明細：")
        for r in mismatches:
            print(f"  {r['file']}：dd-meta={r['actual_verdict']!r}(role={r['actual_role']!r}) "
                  f"vs 腳本={r['computed_verdict']!r}(row{r['row_hit']}, role={r['computed_role']!r})")
            gaps = sorted({g for row in r["decision_out"]["audit_rows"] for g in row.get("input_gap", [])})
            if gaps:
                print(f"      缺輸入：{', '.join(gaps)}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

# v16 修法(c)（2026-09-04 SNOW dry-run §12 讀數③）：critic 徒手抓到「Soft
# Veto 與無 Veto baseline 互斥」尚未機械化——只加自檢斷言，不改矩陣任何 row
# 的語意或門檻（PREREG 凍結）。_evaluate_matrix 的 early-return 控制流本已
# 保證兩者互斥（has_soft_veto=True 時，函式在跑到 rows 8/9/9b/10 判斷之前就
# 已經 return），這裡只是把它從「結構上理所當然」變成「機械可驗證」的事後
# 斷言，供未來若有人改動控制流時當場攔下，而不是留給下一輪 critic 徒手抓。
_SOFT_VETO_ROW_IDS = {"6", "7", "7a"}
_BASELINE_NO_VETO_ROW_IDS = {"8", "9", "9b", "10"}


def check_soft_veto_baseline_exclusivity(audit_rows):
    """回傳互斥自檢的衝突 audit-row 清單（Soft Veto 命中列 + 無 Veto baseline
    命中列各自附上），空 list = 通過。"""
    soft_hits = [r for r in audit_rows if r.get("row") in _SOFT_VETO_ROW_IDS and r.get("hit")]
    baseline_hits = [r for r in audit_rows if r.get("row") in _BASELINE_NO_VETO_ROW_IDS and r.get("hit")]
    if soft_hits and baseline_hits:
        return soft_hits + baseline_hits
    return []


# WP1c 修法4：run 對一份完整 judgment.json（帶既有 decision_out）寫回時，只
# 覆寫機械可判欄；rearm_trigger／exec_line／人工補的 requires_critic 條目
#一律保留，不被矩陣重跑清空（v16 dry-run §11 item 4 教訓）。
_MECHANICAL_DECISION_OUT_KEYS = ["verdict", "role", "row_hit", "pacing", "holding_cap", "audit_rows"]


def _merge_decision_out(existing: dict, computed: dict) -> dict:
    """合併規則：`_MECHANICAL_DECISION_OUT_KEYS`（矩陣機械輸出，逐次覆寫）＋
    `requires_critic`（既有＋新算，去重、保留順序）；`existing` 其餘欄位
    （rearm_trigger／exec_line／任何未來新增的人工欄）原樣保留。"""
    merged = dict(existing)
    for k in _MECHANICAL_DECISION_OUT_KEYS:
        merged[k] = computed.get(k)
    combined_rc = list(existing.get("requires_critic") or []) + list(computed.get("requires_critic") or [])
    seen = []
    for item in combined_rc:
        if item not in seen:
            seen.append(item)
    merged["requires_critic"] = seen
    return merged


def cmd_run(args):
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    inputs = data.get("decision_inputs", data)  # 容許直接餵 decision_inputs 或包一層
    computed = evaluate(inputs)

    conflicts = check_soft_veto_baseline_exclusivity(computed["audit_rows"])
    if conflicts:
        print("dd_decision run 自檢失敗：Soft Veto(6/7/7a) 與無 Veto baseline(8/9/9b/10) 同時命中：",
              file=sys.stderr)
        for r in conflicts:
            print(f"  衝突：row {r['row']} 命中 — {r['basis']}", file=sys.stderr)
        return 1

    # 輸入若是完整 judgment.json（帶既有 decision_out）→ 合併寫回，不覆蓋
    # 手填欄；輸入若只是裸 decision_inputs.json（無 decision_out）→ 舊行為
    # 不變（out＝矩陣機械輸出本身）。
    is_judgment = isinstance(data, dict) and "decision_out" in data
    if is_judgment:
        out = _merge_decision_out(data.get("decision_out") or {}, computed)
        data["decision_out"] = out
    else:
        out = computed

    print(json.dumps(out, ensure_ascii=False, indent=2))
    if args.json:
        payload = data if is_judgment else out
        Path(args.json).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"已寫 {args.json}"
            + ("（輸入含既有 decision_out：已合併機械欄，rearm_trigger/exec_line/人工requires_critic保留）"
               if is_judgment else ""),
            file=sys.stderr,
        )
    if args.html:
        Path(args.html).write_text(build_audit_html(out), encoding="utf-8")
        print(f"已寫 {args.html}", file=sys.stderr)
    return 0


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser(
        "run",
        help="跑一份 decision_inputs.json 或完整 judgment.json，輸出 decision_out",
        description=(
            "INPUT 可以是裸 decision_inputs.json，也可以是完整 judgment.json"
            "（帶 decision_inputs + 既有 decision_out）。\n"
            "INPUT 帶既有 decision_out 時（WP1c 修法4）：只覆寫機械可判欄"
            "（verdict/role/row_hit/pacing/holding_cap/audit_rows）＋"
            "requires_critic（既有條目＋矩陣新算條目，合併去重，保留順序）；"
            "既有 decision_out 其餘欄（rearm_trigger／exec_line／任何人工欄）"
            "原樣保留，不被本次重跑清空。--json 此時寫回的是整份 judgment.json"
            "（decision_out 已合併），不是裸 decision_out。\n"
            "INPUT 不帶 decision_out（裸 decision_inputs.json）時：行為不變，"
            "--json 寫的就是矩陣機械輸出本身。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_run.add_argument("input")
    p_run.add_argument("--html", metavar="OUT", help="寫 <details class=\"audit\"> HTML 片段")
    p_run.add_argument(
        "--json", metavar="OUT",
        help="寫回 JSON；INPUT 是完整 judgment.json 時寫回整份合併後檔案，"
             "INPUT 是裸 decision_inputs.json 時寫回裸 decision_out",
    )

    p_check = sub.add_parser("check", help="從既有 DD html 的 dd-meta 抽 decision_inputs，跑矩陣比對")
    p_check.add_argument("html")
    p_check.add_argument("--infer-from-html", action="store_true", dest="infer")

    p_all = sub.add_parser("check-all", help="對所有 schema=v15 的 DD 逐檔 check，印彙總表")
    p_all.add_argument("--glob", default="docs/dd/DD_*.html")
    p_all.add_argument("--infer-from-html", action="store_true", dest="infer")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        return cmd_run(args)
    if args.cmd == "check":
        r = cmd_check(args.html, infer=args.infer)
        return 0 if r.get("match") else 1
    if args.cmd == "check-all":
        return cmd_check_all(args.glob, infer=args.infer)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
