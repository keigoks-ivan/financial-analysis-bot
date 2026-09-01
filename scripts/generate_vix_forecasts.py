#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_vix_forecasts.py — vix-model 預測 producer（forecast ledger G5，事件觸發）。

每次執行（週更 cron，`--write`）判定「今天是否為 VIX 期限結構倒掛 onset 日」（PREREG 凍結
定義，設計稿 §G3／§G5：slope=^VIX3M−^VIX 連續 ≥5 個交易日 >0 後首個 <0 的交易日）——
**不是每次跑都落帳**，只在真的偵測到 onset 事件當天才產兩筆草案，其餘時候印「無事件」
exit 0，不寫入 knowledge/forecasts.jsonl。

資料來源優先序（設計稿 §G5／交付清單原文）：
  1. data/statlab_prices.json（scripts/build_statlab.py 另一條 pipeline 維護，唯讀）—— 正常
     情況下的主要來源。
  2. 若該檔缺檔或無法讀取，fallback 到本 producer 自己的 base-rate raw cache
     data/vixts_base_rates_raw_cache.json（scripts/build_vixts_base_rates.py 產出），並印警告。

onset 判定用「兩序列共同交易日」中最新一筆（as_of）——**不強制 as_of 等於執行當日**，因為
^VIX3M 上游 feed 可能落後（實測 2026-09-01：yfinance 即時抓取的 ^VIX3M 十年歷史尾端本身就
落後 ^VIX 數週，非本檔或 stooq fallback 造成），若 as_of 落後執行日 >5 個曆日（沿用全站既
有 5 天 stale 慣例，見 scripts/build_statlab.py 的 vix_term_module），印警告但仍照 as_of 判
定——與 generate_rv_forecasts.py 用「flowmap_prices.json 最新一筆」而非強制當日的做法一致。

onset 時產兩筆草案（PREREG 凍結，設計稿 §G5）：
  ①「21 交易日內 slope 回正」  resolver vixts:SLOPE > 0 any_close，resolve_by = ts+30 曆日
  ②「63 交易日後 SPY 高於 onset 當日收盤」 resolver pxd:SPY > onset_close at_expiry，
     resolve_by = ts+92 曆日
p 值機械取自 data/vixts_base_rates.json（scripts/build_vixts_base_rates.py 產出的
freq_recovery_within_21td／freq_spy_higher_after_63td）——不接受人工覆寫。

已知的口徑近似（設計稿明文接受的既有取捨，非本檔臨時決定，同 generate_rv_forecasts.py
docstring 的先例）：base rate 用「交易日」（21／63）向前看，但 forecast 的 resolve_by 用
「曆日」（30／92）——兩者是同一件事的兩種近似表達，非精確對齊。

CLI
---
  python scripts/generate_vix_forecasts.py            dry-run，草案（若有）印到 stdout（純 JSONL）
  python scripts/generate_vix_forecasts.py --write     append 進 knowledge/forecasts.jsonl
                                                        （查重：同一 onset_date 已落過即拒）
無事件或跳過/拒絕原因印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATLAB_PRICES = ROOT / "data" / "statlab_prices.json"
RAW_CACHE = ROOT / "data" / "vixts_base_rates_raw_cache.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
BASE_RATES = ROOT / "data" / "vixts_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

SOURCE = "vix-model"
ONSET_STREAK_DAYS = 5              # 須與 build_vixts_base_rates.py 一致（PREREG 凍結）
GAP_THRESHOLD_CALENDAR_DAYS = 10   # 同上（safeguard，非 PREREG，見 build_vixts_base_rates.py）
STALE_WARN_CALENDAR_DAYS = 5       # 沿用全站既有 5 天 stale 慣例（build_statlab.py vix_term_module）
RECOVERY_HORIZON_CALENDAR_DAYS = 30
SPY_HORIZON_CALENDAR_DAYS = 92


def warn(msg: str) -> None:
    print(f"[vix-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[vix-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 讀取 slope 序列：statlab_prices.json 優先，缺檔 fallback 自家 raw cache
# ═══════════════════════════════════════════════════════════════════════════

def _load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {path}: {e}")
        return None


def load_slope_series():
    """回傳 (slope_ts, source_label)。slope_ts=[(date, slope), ...] 升冪，兩序列共同交易日。
    優先 data/statlab_prices.json；缺檔或無法讀取則 fallback 到本 producer 自家 raw cache
    （data/vixts_base_rates_raw_cache.json，由 build_vixts_base_rates.py 產出），兩者皆缺
    則回傳 (None, None)。"""
    data = _load_json(STATLAB_PRICES)
    source_label = "data/statlab_prices.json"
    if not data:
        warn(f"{STATLAB_PRICES} 缺檔或無法讀取，fallback 到自家 raw cache {RAW_CACHE}")
        data = _load_json(RAW_CACHE)
        source_label = "data/vixts_base_rates_raw_cache.json（fallback）"
        if not data:
            warn(f"{RAW_CACHE} 亦缺檔或無法讀取，無資料可判定")
            return None, None
    series = data.get("series") or {}
    vix = {d: c for d, c in (series.get("^VIX") or [])}
    vix3m = {d: c for d, c in (series.get("^VIX3M") or [])}
    common = sorted(set(vix) & set(vix3m))
    if not common:
        warn(f"{source_label}：^VIX／^VIX3M 無重疊交易日")
        return None, None
    slope_ts = [(d, round(vix3m[d] - vix[d], 4)) for d in common]
    return slope_ts, source_label


# ═══════════════════════════════════════════════════════════════════════════
# onset 判定（重寫，非 import build_vixts_base_rates.py——避免耦合，邏輯須與該檔逐字一致，
# PREREG 凍結見設計稿 §G3）
# ═══════════════════════════════════════════════════════════════════════════

def is_onset_at_last_point(slope_ts, streak_days=ONSET_STREAK_DAYS,
                            gap_threshold_days=GAP_THRESHOLD_CALENDAR_DAYS):
    """判定 slope_ts 最後一筆（as_of）是否為 onset 日。回傳 (is_onset, consec_pos_before)。"""
    n = len(slope_ts)
    if n == 0:
        return False, 0
    consec_pos = 0
    for i in range(n - 1):  # 走到 n-2，累積出「最後一筆之前」的 streak
        d, s = slope_ts[i]
        if i > 0:
            prev_d = slope_ts[i - 1][0]
            gap_days = (date.fromisoformat(d) - date.fromisoformat(prev_d)).days
            if gap_days > gap_threshold_days:
                consec_pos = 0
        if s > 0:
            consec_pos += 1
        else:
            consec_pos = 0
    # 檢查最後一筆與其前一筆之間是否也有資料缺口
    if n >= 2:
        gap_days_last = (date.fromisoformat(slope_ts[-1][0]) -
                         date.fromisoformat(slope_ts[-2][0])).days
        if gap_days_last > gap_threshold_days:
            consec_pos = 0
    last_date, last_slope = slope_ts[-1]
    is_onset = last_slope < 0 and consec_pos >= streak_days
    return is_onset, consec_pos


# ═══════════════════════════════════════════════════════════════════════════
# pxd:SPY 讀法（data/flowmap_prices.json，找 onset 當日或最近前一交易日收盤）
# ═══════════════════════════════════════════════════════════════════════════

def spy_close_on_or_before(onset_date):
    data = _load_json(FLOWMAP_PRICES)
    if not data:
        return None, None
    bars = sorted((data.get("series") or {}).get("SPY") or [])
    if not bars:
        return None, None
    dates = [d for d, _ in bars]
    pos = bisect.bisect_right(dates, onset_date) - 1
    if pos < 0:
        return None, None
    return bars[pos]


# ═══════════════════════════════════════════════════════════════════════════
# base rate 查表
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates():
    if not BASE_RATES.exists():
        raise SystemExit(f"找不到 {BASE_RATES} —— 先跑 python scripts/build_vixts_base_rates.py")
    try:
        return json.loads(BASE_RATES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {BASE_RATES}: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生 + 查重 + 落帳
# ═══════════════════════════════════════════════════════════════════════════

def _next_ids(ts_str, n, path=FORECASTS):
    used = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rid = json.loads(line).get("id", "")
            except json.JSONDecodeError:
                continue
            used.add(rid)
    prefix = f"fc_{ts_str.replace('-', '')}_vix_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{prefix}{seq:02d}"
        if cand not in used:
            out.append(cand)
    return out


def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def onset_already_logged(path, onset_date, source=SOURCE):
    """同一 onset_date 已有 source=vix-model 落帳紀錄 → True（查重口徑：同 onset 事件拒重複，
    設計稿 §G5「dry-run 預設、--write 查重（同市場同事件週拒重複）」的 vix-model 版本——這裡
    是「同一次倒掛 onset」而非「週」，因為 onset 是離散事件、天生不會同週重複觸發兩次）。"""
    needle = f"onset_date={onset_date}"
    for r in _existing_forecasts(path):
        if r.get("source") == source and needle in (r.get("source_ref") or ""):
            return True
    return False


def build_drafts(today, onset_date, onset_slope, base_rates):
    ts_str = today.isoformat()
    spy_date, spy_close = spy_close_on_or_before(onset_date)
    if spy_close is None:
        raise SystemExit(f"無法從 {FLOWMAP_PRICES} 找到 onset 日 {onset_date}（或其前）的 SPY 收盤，中止")

    p_recovery = base_rates.get("freq_recovery_within_21td")
    p_spy = base_rates.get("freq_spy_higher_after_63td")
    if p_recovery is None or p_spy is None:
        raise SystemExit(f"{BASE_RATES} 缺 freq_recovery_within_21td／freq_spy_higher_after_63td，中止（不可硬猜 p）")

    resolve_by_1 = (today + timedelta(days=RECOVERY_HORIZON_CALENDAR_DAYS)).isoformat()
    resolve_by_2 = (today + timedelta(days=SPY_HORIZON_CALENDAR_DAYS)).isoformat()

    base_meta = (f"base_rate built_at={base_rates.get('built_at')}｜n_events={base_rates.get('n_events')}｜"
                 f"confidence={base_rates.get('confidence')}")
    source_ref = (f"onset_date={onset_date}｜onset_slope={onset_slope}｜"
                  f"spy_close_at_onset={spy_close}（{spy_date}）｜data/vixts_base_rates.json {base_meta}")

    ids = _next_ids(ts_str, 2)

    draft_recovery = {
        "id": ids[0], "ts": ts_str, "source": SOURCE, "source_ref": source_ref,
        "claim": f"{resolve_by_1} 前（{RECOVERY_HORIZON_CALENDAR_DAYS} 曆日內，約 21 個交易日）：VIX 期限結構 slope（^VIX3M−^VIX）回正（>0）",
        "p": p_recovery, "horizon_days": RECOVERY_HORIZON_CALENDAR_DAYS, "resolve_by": resolve_by_1,
        "resolver": {"series": "vixts:SLOPE", "op": ">", "value": 0, "window": "any_close"},
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "note": (f"vix-model 機械賦值（無需人工判斷）｜onset={onset_date}（slope={onset_slope}）｜"
                 f"p 取自 vixts_base_rates.json freq_recovery_within_21td｜{base_meta}"),
    }
    draft_spy = {
        "id": ids[1], "ts": ts_str, "source": SOURCE, "source_ref": source_ref,
        "claim": f"{resolve_by_2} 前（{SPY_HORIZON_CALENDAR_DAYS} 曆日後，約 63 個交易日）：SPY 收盤高於 onset 當日收盤 {spy_close}（{spy_date}）",
        "p": p_spy, "horizon_days": SPY_HORIZON_CALENDAR_DAYS, "resolve_by": resolve_by_2,
        "resolver": {"series": "pxd:SPY", "op": ">", "value": spy_close, "window": "at_expiry"},
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "note": (f"vix-model 機械賦值（無需人工判斷）｜onset={onset_date}（slope={onset_slope}）｜"
                 f"p 取自 vixts_base_rates.json freq_spy_higher_after_63td｜{base_meta}"),
    }
    return [draft_recovery, draft_spy]


def write_drafts(drafts, path=FORECASTS):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for d in drafts:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description="vix-model 預測 producer — 事件觸發（VIX 期限結構倒掛 onset）")
    ap.add_argument("--write", action="store_true", help="偵測到 onset 且未查重命中時 append 進 knowledge/forecasts.jsonl（預設 dry-run）")
    args = ap.parse_args()

    today = date.today()

    slope_ts, source_label = load_slope_series()
    if not slope_ts:
        warn("無可用 slope 資料（statlab_prices.json 與自家 raw cache 皆缺或無重疊交易日），無法判定，視為無事件")
        info("無事件（無資料）：exit 0，不落帳。")
        return

    as_of = slope_ts[-1][0]
    lag_days = (today - date.fromisoformat(as_of)).days
    if lag_days > STALE_WARN_CALENDAR_DAYS:
        warn(f"slope 資料來源={source_label}，最新可觀察日 as_of={as_of} 落後執行日 {today.isoformat()} "
             f"共 {lag_days} 個曆日（> {STALE_WARN_CALENDAR_DAYS} 天 stale 門檻）——本次判定僅能依 as_of "
             f"當時的資料狀態，若 onset 已在資料缺口期間發生會被錯過，不代表資料完整")

    is_onset, consec_pos = is_onset_at_last_point(slope_ts)
    if not is_onset:
        info(f"無事件：as_of={as_of}（來源={source_label}）非 onset 日"
             f"（連續正值天數={consec_pos}，最新 slope={slope_ts[-1][1]}）。exit 0，不落帳。")
        return

    onset_date, onset_slope = as_of, slope_ts[-1][1]
    info(f"偵測到 onset：{onset_date}（slope={onset_slope}，來源={source_label}，前 {consec_pos} 個交易日連續 slope>0）")

    base_rates = load_base_rates()
    drafts = build_drafts(today, onset_date, onset_slope, base_rates)

    for d in drafts:
        print(json.dumps(d, ensure_ascii=False))

    dup = onset_already_logged(FORECASTS, onset_date)
    if dup:
        warn(f"onset_date={onset_date} 已有 source={SOURCE} 落帳紀錄——本次落帳將被拒絕（同一次 onset 不重複記）。")

    if not args.write:
        info(f"dry-run：共 {len(drafts)} 筆草案。--write 才會 append 進 {FORECASTS}"
             f"（若 onset_date={onset_date} 已落過則拒絕）。")
        return

    if dup:
        print(f"\n# --write 拒絕：onset_date={onset_date} 已有 source={SOURCE} 落帳紀錄，不重複落帳。",
              file=sys.stderr)
        sys.exit(1)

    write_drafts(drafts, FORECASTS)
    print(f"\n# --write：寫入 {len(drafts)} 筆 → {FORECASTS}", file=sys.stderr)


if __name__ == "__main__":
    main()
