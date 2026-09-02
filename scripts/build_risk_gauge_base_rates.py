#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_risk_gauge_base_rates.py — 風險偏好分數（risk gauge）13 週前瞻經驗轉移表
（forecast ledger v2 §9／`_market_cockpit_design_20260902.md` §9 package F4 機械餵料）。

季度手動重建（`--if-due` 供 cron 掛用；PREREG 凍結至 SPRT 判決或 2027-03 校準輪，見設計稿
§9 共同規則）。讀 `docs/cache/risk_history.json`（三個等長平行陣列 `weeks`／`score`／`spx`，
週頻，2000-12 起 1,345 週；`score` 為 −1..+1 風險偏好分數），純本地檔案運算，**不打網路**。

取樣與分位
----------
* **取樣點** ＝ 每個日曆月第一週（`weeks[i]` 的 `YYYY-MM` 前綴首次出現的索引 `i`）——非每週
  取樣，理由同設計稿 §9 F4 列："sample = first week of each calendar month"。
* **可驗證樣本** ＝ 取樣點中 `i + 13 < len(weeks)`（第 13 週後的 `spx` 值存在）者——這批同時
  用來：(a) 算五分位切點、(b) 算每分位 13 週後上漲頻率、(c) 算 pooled 無條件頻率 `p_clim`。
* **五分位切點在可驗證樣本上算（in-sample）**：與 `scripts/build_rv_base_rates.py` 相同取捨
  ——分位定義與轉移頻率統計用同一個母體，但仍是 in-sample 切點（見下方誠實註記），不是滾動
  或擴張窗口的即時分位，不能宣稱樣本外預測力。
* **結果 ＝ SPX 13 週後收盤 > 取樣當週收盤**（`outcome`），用陣列索引 `+13`（週頻陣列，故
  13 週 ≈ 91 曆日，與 producer 的 `horizon_days=91` 對齊）。

誠實註記（務必讀）
------------------
* **月度取樣、13 週視窗，樣本仍重疊**：相鄰兩個月的取樣點通常相距 4-5 週，遠小於 13 週的
  前瞻視窗，故相鄰樣本點的結果視窗高度重疊（約共用 8-9 週）——這不是獨立試驗，頻率是重疊
  樣本的經驗估計，不做假設檢定，信賴區間不適用傳統獨立樣本公式（同 build_rv_base_rates.py
  的既有立場）。
* **`score` 本身是複合週頻指標**（結構未知，來自既有 `docs/cache/risk_history.json` 產線，
  非本檔定義）——本檔只對其做分位切分與轉移頻率統計，不重新定義或平滑該分數。
* **切點用同一可驗證子樣本（in-sample）算出**，不是每次重建時只用「過去」資料的擴張窗口，
  故本表是 base rate 參照表，不是樣本外驗證過的預測模型（同 rv base rate 表的既有立場）。

用法
----
  python scripts/build_risk_gauge_base_rates.py                離線重算（預設，唯讀本地檔）
  python scripts/build_risk_gauge_base_rates.py --if-due       built_at 距今 <85 天則跳過
                                                                （exit 0，印 not due）
  python scripts/build_risk_gauge_base_rates.py --out /tmp/x.json  測試用輸出路徑覆寫
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RISK_HISTORY = ROOT / "docs" / "cache" / "risk_history.json"
OUT_JSON = ROOT / "data" / "risk_gauge_base_rates.json"

SCHEMA = "risk-gauge-base-rates-v1"
HORIZON_WEEKS = 13         # PREREG 凍結（設計稿 §9 F4："SPY 13 週後更高"）
IF_DUE_MAX_AGE_DAYS = 85   # --if-due 門檻，同 build_rv_base_rates.py／build_vrp_base_rates.py 慣例


def warn(msg: str) -> None:
    print(f"[risk-gauge-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[risk-gauge-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 讀取
# ═══════════════════════════════════════════════════════════════════════════

def load_risk_history(path=RISK_HISTORY):
    if not path.exists():
        raise SystemExit(f"找不到 {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取/解析 {path}: {e}")

    weeks = data.get("weeks")
    score = data.get("score")
    spx = data.get("spx")
    if not (isinstance(weeks, list) and isinstance(score, list) and isinstance(spx, list)):
        raise SystemExit(f"{path} 缺 weeks/score/spx 陣列")
    if not (len(weeks) == len(score) == len(spx)):
        raise SystemExit(f"{path} 的 weeks/score/spx 長度不一致"
                          f"（{len(weeks)}/{len(score)}/{len(spx)}）")
    if any(v is None for v in score) or any(v is None for v in spx):
        warn(f"{path} 的 score/spx 含 None——若落在取樣點會被防禦性跳過")
    return data, weeks, score, spx


# ═══════════════════════════════════════════════════════════════════════════
# 取樣（每個日曆月第一週）
# ═══════════════════════════════════════════════════════════════════════════

def build_monthly_sample(weeks):
    """回傳升冪索引列表：每個日曆月（依 weeks[i][:7]）首次出現的索引 i。"""
    seen = set()
    idxs = []
    for i, w in enumerate(weeks):
        ym = w[:7]
        if ym not in seen:
            seen.add(ym)
            idxs.append(i)
    return idxs


def build_verifiable_rows(sample_idxs, weeks, score, spx, horizon=HORIZON_WEEKS):
    """回傳可驗證觀測列表：{"week","idx","score","outcome_up"}，
    僅取 i+horizon < len(weeks) 且 score[i]／spx[i]／spx[i+horizon] 皆非 None 者。"""
    n = len(weeks)
    rows = []
    for i in sample_idxs:
        fut_idx = i + horizon
        if fut_idx >= n:
            continue
        s, now_px, fut_px = score[i], spx[i], spx[fut_idx]
        if s is None or now_px is None or fut_px is None:
            continue
        rows.append({
            "week": weeks[i],
            "idx": i,
            "score": s,
            "spx_now": now_px,
            "spx_future": fut_px,
            "outcome_up": fut_px > now_px,
        })
    return rows


# ═══════════════════════════════════════════════════════════════════════════
# 五分位（切點在可驗證樣本上算，in-sample；線性內插同 numpy 'linear'）
# ═══════════════════════════════════════════════════════════════════════════

def _percentile(sorted_vals, q):
    n = len(sorted_vals)
    if n == 0:
        return None
    if n == 1:
        return sorted_vals[0]
    idx = q / 100.0 * (n - 1)
    lo = int(idx)
    hi = min(lo + 1, n - 1)
    frac = idx - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac


def _quintile_label(v, cutoffs):
    q20, q40, q60, q80 = cutoffs
    if v <= q20:
        return "Q1"
    if v <= q40:
        return "Q2"
    if v <= q60:
        return "Q3"
    if v <= q80:
        return "Q4"
    return "Q5"


def build_quintile_table(rows):
    scores_sorted = sorted(r["score"] for r in rows)
    cutoffs = [
        round(_percentile(scores_sorted, 20), 4),
        round(_percentile(scores_sorted, 40), 4),
        round(_percentile(scores_sorted, 60), 4),
        round(_percentile(scores_sorted, 80), 4),
    ]
    buckets = {q: [] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")}
    for r in rows:
        buckets[_quintile_label(r["score"], cutoffs)].append(r)

    quintiles = []
    for q in ("Q1", "Q2", "Q3", "Q4", "Q5"):
        bucket_rows = buckets[q]
        n = len(bucket_rows)
        if n == 0:
            quintiles.append({"quintile": q, "n": 0, "score_range": None, "freq_up_13w": None})
            continue
        vals = [r["score"] for r in bucket_rows]
        freq_up = sum(1 for r in bucket_rows if r["outcome_up"]) / n
        quintiles.append({
            "quintile": q,
            "n": n,
            "score_range": [round(min(vals), 4), round(max(vals), 4)],
            "freq_up_13w": round(freq_up, 3),
        })
    return quintiles, cutoffs


def compute_p_clim(rows):
    """pooled（無條件、不分五分位）13 週後上漲頻率——與五分位表用同一批可驗證樣本
    （設計稿 §9 F4："p_clim＝無條件"），供 producer 的 forecasts.jsonl p_clim 欄位取值。"""
    n = len(rows)
    if n == 0:
        return None
    return round(sum(1 for r in rows if r["outcome_up"]) / n, 3)


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="風險偏好分數 13 週前瞻經驗轉移表 builder（forecast ledger 機械餵料）")
    ap.add_argument("--input", default=str(RISK_HISTORY),
                     help="輸入路徑（測試用；預設 docs/cache/risk_history.json）")
    ap.add_argument("--out", default=str(OUT_JSON),
                     help="輸出路徑（測試用；預設 data/risk_gauge_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建"
                          "（exit 0，印 not due）；供 cron 掛「季度自動重建」用")
    args = ap.parse_args()

    out_path = Path(args.out)

    if args.if_due:
        if out_path.exists():
            try:
                existing = json.loads(out_path.read_text(encoding="utf-8"))
                built_at = existing.get("built_at")
                if built_at:
                    built_dt = datetime.strptime(built_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    age_days = (datetime.now(timezone.utc) - built_dt).total_seconds() / 86400.0
                    if age_days < IF_DUE_MAX_AGE_DAYS:
                        info(f"--if-due: {out_path} built_at={built_at}（{age_days:.1f} 天前）< "
                             f"{IF_DUE_MAX_AGE_DAYS} 天門檻，not due，本次不重建")
                        return
                    info(f"--if-due: {out_path} built_at={built_at}（{age_days:.1f} 天前）≥ "
                         f"{IF_DUE_MAX_AGE_DAYS} 天門檻，due，繼續重建")
                else:
                    info(f"--if-due: {out_path} 無 built_at 欄位，視為需要重建")
            except (OSError, json.JSONDecodeError, ValueError) as e:
                warn(f"--if-due: 無法讀取/解析既有 {out_path}（{e}），視為需要重建")
        else:
            info(f"--if-due: {out_path} 不存在，視為需要重建")

    data, weeks, score, spx = load_risk_history(Path(args.input))

    sample_idxs = build_monthly_sample(weeks)
    rows = build_verifiable_rows(sample_idxs, weeks, score, spx)
    if not rows:
        raise SystemExit("可驗證樣本為 0（歷史長度不足以同時取月度樣本點 + 未來 13 週資料），中止")

    quintiles, cutoffs = build_quintile_table(rows)
    p_clim = compute_p_clim(rows)

    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "docs/cache/risk_history.json",
        "source_as_of": data.get("as_of"),
        "sample_method": "每個日曆月第一週（weeks[i] 的 YYYY-MM 前綴首次出現的索引），非每週取樣",
        "window_weeks": HORIZON_WEEKS,
        "n_months_total": len(sample_idxs),
        "n": len(rows),
        "n_transition_sample": len(rows),
        "score_quintile_cutoffs_pct20_40_60_80": cutoffs,
        "quintiles": quintiles,
        "p_clim": {"risk_spy_up_13w": p_clim},
        "p_clim_n": len(rows),
        "p_clim_note": (
            "無條件（pooled，不分五分位）13 週後 SPX 收盤高於取樣當週頻率，與同檔 quintiles "
            "用同一批可驗證樣本（每月首週、i+13 週資料存在）——供 forecasts.jsonl "
            "risk_spy_up_13w 命題的 p_clim 欄位取值。"
        ),
        "methodology_note": (
            "取樣為每個日曆月第一週（非每週），但 13 週前瞻視窗遠長於月度取樣間距（約 4-5 週），"
            "相鄰取樣點的前瞻視窗高度重疊，非獨立試驗——本表只報告經驗頻率與樣本數 n，不做假設"
            "檢定，信賴區間不適用傳統獨立樣本公式。五分位切點（score_quintile_cutoffs）用同一個"
            "可驗證子樣本（in-sample）的 20/40/60/80 百分位算出，非滾動或擴張窗口即時分位，不能"
            "宣稱樣本外預測力——本表定位是 base rate 參照表，不是模型。"
        ),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")
    info(f"wrote {out_path} — {len(rows)} 筆可驗證觀測（{len(sample_idxs)} 個月度取樣點），"
         f"source_as_of={data.get('as_of')}")
    for q in quintiles:
        info(f"  {q['quintile']}: n={q['n']:<4} range={q['score_range']}  freq_up_13w={q['freq_up_13w']}")
    info(f"  p_clim（pooled，n={len(rows)}）: {p_clim}")


if __name__ == "__main__":
    main()
