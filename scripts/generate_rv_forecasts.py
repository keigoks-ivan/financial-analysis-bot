#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_rv_forecasts.py — RV 預測 producer（forecast ledger 的機械餵料）。

每月首個交易日手動跑（不掛 cron，先養習慣——見設計稿 §E3）。從 data/flowmap_prices.json
算當前 SPY RV21（年化，日對數報酬 sample std×√252×100，口徑與 scripts/build_rv_base_rates.py
逐字一致），查 data/rv_base_rates.json 的五分位經驗轉移表取 p，機械產生兩筆 forecast 草案，
append 進 knowledge/forecasts.jsonl（source: "rv-model"）：

  ①「30 曆日後 SPY RV21 高於今日 X%」               resolver window=at_expiry, op=">"
  ②「30 曆日內 SPY RV21 觸及 X+5% 以上」            resolver window=any_close, op=">="

p 值完全由轉移表機械給出（該分位的經驗頻率，已四捨五入兩位）——不需人工判斷、也不接受
人工覆寫，這正是本 producer 要測的命題：「原始數據裡最可預測的量（波動率）能不能給出
校準的機率」。resolver 域 rv:<TICKER> 由 knowledge/settle_forecasts.py 結算（見該檔新增
的 rv: 域說明）。

已知的口徑近似（設計稿 §E3 明文接受，非本檔臨時決定）：base rate 轉移表用「21 個交易日」
向前看（約一個月的交易日數），但 forecast 的 resolve_by 用「30 個曆日」（含週末假日）——
兩者是同一件事的兩種近似表達（皆≈一個月），非精確對齊，此為設計稿既有取捨。

v2（forecast v2 設計稿 §5.1，`_forecast_v2_design_20260902.md`）：改用 knowledge/forecast_lib.py
（next_ids／finalize／append，含哨兵 twin 產生）；每筆額外填 claim_template
（rv21_higher_21d／rv21_touch_plus5_21d）、p_clim（取自 data/rv_base_rates.json 頂層 pooled
頻率，同表同 built_at、不分五分位）、p_clim_ref、p_table_built_at、episode_id
（`rv:{YYYY-MM}`）。查重規則、dry-run/--write 行為、stdout=JSONL only 慣例不變。

CLI
---
  python scripts/generate_rv_forecasts.py            dry-run，兩筆草案印到 stdout（純 JSONL）
  python scripts/generate_rv_forecasts.py --write     append 進 knowledge/forecasts.jsonl
                                                       （查重：同一 YYYY-MM 若已有 source=
                                                       "rv-model" 的筆數，整批拒絕落帳，不
                                                       重複灌月頻資料——見下方 dedupe 說明）
跳過/拒絕原因印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
BASE_RATES = ROOT / "data" / "rv_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

sys.path.insert(0, str(ROOT / "knowledge"))
import forecast_lib as fl  # noqa: E402 — id 產生／v2 欄位補齊／落帳＋哨兵 twin，見 forecast_lib.py

SOURCE = "rv-model"
TICKER = "SPY"
WINDOW_TRADING_DAYS = 21   # 須與 build_rv_base_rates.py 一致（PREREG 凍結，僅供口徑核對用）
VOL_POINT_THRESHOLD = 5.0  # 同上
HORIZON_CALENDAR_DAYS = 30


def warn(msg: str) -> None:
    print(f"[rv-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[rv-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：當前 RV21（data/flowmap_prices.json，SPY 日線）
# ═══════════════════════════════════════════════════════════════════════════

def _sample_std(xs):
    n = len(xs)
    if n < 2:
        return None
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / (n - 1)
    return var ** 0.5


def current_rv21(prices_path=FLOWMAP_PRICES, ticker=TICKER, window=WINDOW_TRADING_DAYS):
    """回傳 (as_of_date, rv21_pct)。歷史不足或找不到 ticker 時回傳 (None, None)。"""
    if not prices_path.exists():
        return None, None
    try:
        data = json.loads(prices_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {prices_path}: {e}")
        return None, None
    bars = (data.get("series") or {}).get(ticker)
    if not bars or len(bars) < window + 1:
        return None, None
    bars = sorted(bars, key=lambda b: b[0])
    closes = [c for _, c in bars]
    dates = [d for d, _ in bars]
    rets = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))
            if closes[i - 1] > 0 and closes[i] > 0]
    if len(rets) < window:
        return None, None
    window_rets = rets[-window:]
    s = _sample_std(window_rets)
    if s is None:
        return None, None
    rv21 = round(s * math.sqrt(252) * 100, 4)
    return dates[-1], rv21


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：五分位經驗轉移表（data/rv_base_rates.json）
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates(path=BASE_RATES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_rv_base_rates.py")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")


def classify_quintile(rv21, cutoffs):
    q20, q40, q60, q80 = cutoffs
    if rv21 <= q20:
        return "Q1"
    if rv21 <= q40:
        return "Q2"
    if rv21 <= q60:
        return "Q3"
    if rv21 <= q80:
        return "Q4"
    return "Q5"


def lookup_probabilities(base_rates, rv21):
    cutoffs = base_rates["quintile_cutoffs_pct20_40_60_80"]
    q = classify_quintile(rv21, cutoffs)
    row = next((r for r in base_rates["quintiles"] if r["quintile"] == q), None)
    if row is None or row.get("n", 0) == 0:
        raise SystemExit(f"分位 {q} 樣本數為 0，base rate 表異常，中止（不可硬猜 p）")
    return q, row


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

def build_drafts(today=None, prices_path=FLOWMAP_PRICES, base_rates_path=BASE_RATES,
                  forecasts_path=FORECASTS):
    today = today or date.today()
    ts_str = today.isoformat()
    resolve_by = (today + timedelta(days=HORIZON_CALENDAR_DAYS)).isoformat()

    as_of, rv21 = current_rv21(prices_path)
    if rv21 is None:
        raise SystemExit(f"無法從 {prices_path} 算出當前 SPY RV21（歷史不足或檔案缺失），中止")

    base_rates = load_base_rates(base_rates_path)
    quintile, row = lookup_probabilities(base_rates, rv21)
    p_higher = row["freq_rv21_higher_after_21d"]
    p_touch = row["freq_touch_plus5_within_21d"]
    touch_threshold = round(rv21 + VOL_POINT_THRESHOLD, 2)

    # v2（forecast v2 設計稿 §5.1）：p_clim 取自同一份表的頂層 pooled 頻率（見
    # scripts/build_rv_base_rates.py compute_pooled_p_clim），與 p（五分位條件頻率）同表
    # 同 built_at、同窗口／門檻，差別只在不分五分位。
    p_clim_map = base_rates.get("p_clim") or {}
    built_at = base_rates.get("built_at")
    p_clim_ref = (f"data/rv_base_rates.json p_clim（pooled，全部五分位合併，"
                  f"n={base_rates.get('n_transition_sample')}）built_at={built_at}")
    episode_id = f"rv:{ts_str[:7]}"

    base_meta = (f"base_rate built_at={built_at}｜quintile={quintile}"
                 f"（range={row.get('rv21_range')}, n={row.get('n')}）｜"
                 f"quintile_cutoffs={base_rates.get('quintile_cutoffs_pct20_40_60_80')}")
    source_ref = f"data/flowmap_prices.json SPY as_of={as_of}｜data/rv_base_rates.json {base_meta}"

    ids = fl.next_ids(ts_str, "rv", 2, forecasts_path)

    draft_higher = {
        "id": ids[0], "ts": ts_str, "source": SOURCE, "source_ref": source_ref,
        "claim": f"{resolve_by} 前（{HORIZON_CALENDAR_DAYS} 曆日後）：SPY RV21（年化已實現波動）高於今日的 {rv21}%",
        "p": p_higher, "horizon_days": HORIZON_CALENDAR_DAYS, "resolve_by": resolve_by,
        "resolver": {"series": f"rv:{TICKER}", "op": ">", "value": rv21, "window": "at_expiry"},
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "note": (f"rv-model 機械賦值（無需人工判斷）｜今日 RV21={rv21}%（as_of {as_of}）｜"
                 f"p 取自五分位轉移表 freq_rv21_higher_after_21d｜{base_meta}"),
        "claim_template": "rv21_higher_21d", "p_clim": p_clim_map.get("rv21_higher_21d"),
        "p_clim_ref": p_clim_ref, "p_table_built_at": built_at, "episode_id": episode_id,
    }
    draft_touch = {
        "id": ids[1], "ts": ts_str, "source": SOURCE, "source_ref": source_ref,
        "claim": f"{resolve_by} 前（{HORIZON_CALENDAR_DAYS} 曆日內）：SPY RV21 觸及 {touch_threshold}% 以上（即今日 +{VOL_POINT_THRESHOLD} 個 vol 點）",
        "p": p_touch, "horizon_days": HORIZON_CALENDAR_DAYS, "resolve_by": resolve_by,
        "resolver": {"series": f"rv:{TICKER}", "op": ">=", "value": touch_threshold, "window": "any_close"},
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "note": (f"rv-model 機械賦值（無需人工判斷）｜今日 RV21={rv21}%（as_of {as_of}）｜"
                 f"p 取自五分位轉移表 freq_touch_plus5_within_21d｜{base_meta}"),
        "claim_template": "rv21_touch_plus5_21d", "p_clim": p_clim_map.get("rv21_touch_plus5_21d"),
        "p_clim_ref": p_clim_ref, "p_table_built_at": built_at, "episode_id": episode_id,
    }
    return fl.finalize([draft_higher, draft_touch])


# ═══════════════════════════════════════════════════════════════════════════
# 查重 + 落帳
# ═══════════════════════════════════════════════════════════════════════════

def month_already_has_source(path, month_prefix, source=SOURCE):
    """同月同 source 已有落帳紀錄 → True（查重口徑：整批月頻拒絕重複，見檔頭 docstring）。"""
    for r in fl.existing(path):
        if r.get("source") == source and (r.get("ts") or "").startswith(month_prefix):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="RV 預測 producer — 月頻手動觸發")
    ap.add_argument("--write", action="store_true", help="append 進 knowledge/forecasts.jsonl（預設 dry-run）")
    args = ap.parse_args()

    today = date.today()
    month_prefix = today.strftime("%Y-%m")
    drafts = build_drafts(today=today)

    dup = month_already_has_source(FORECASTS, month_prefix)
    if dup:
        warn(f"{month_prefix} 已有 source={SOURCE} 的落帳紀錄——本月重複落帳將被拒絕"
             f"（查重口徑：同月同 source 整批拒絕，見檔頭 docstring）。")

    do_write = args.write and not dup
    n_written, n_twins = fl.append(drafts, path=FORECASTS, write=do_write)

    if not args.write:
        info(f"dry-run：共 {len(drafts)} 筆草案。--write 才會 append 進 {FORECASTS}"
             f"（若 {month_prefix} 已有紀錄則整批拒絕）。")
        return

    if dup:
        print(f"\n# --write 拒絕：{month_prefix} 已有 source={SOURCE} 落帳紀錄，本月不重複落帳。",
              file=sys.stderr)
        sys.exit(1)

    print(f"\n# --write：寫入 {n_written} 筆＋{n_twins} 筆哨兵 twin → {FORECASTS}", file=sys.stderr)


if __name__ == "__main__":
    main()
