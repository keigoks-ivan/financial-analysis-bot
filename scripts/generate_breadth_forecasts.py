#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_breadth_forecasts.py — 市場廣度（sector-ETF breadth）預測 producer（forecast
ledger P2 package G2 機械餵料）。

每月首次班車手動／週更班車跑（沿用 scripts/generate_vrp_forecasts.py 的既有節奏）。t＝
data/statlab_prices.json SPY 最後一根 bar 開始、最多回溯 5 個 statlab 自身交易日內，第一個
「同時存在於 data/flowmap_prices.json SPY 序列」的日期（orchestrator 2026-09-02 裁定：規格
原文未講兩份日線快取的 build 時間差，實測常態性差 1 天——見 5 個交易日回溯窗）；用同一日 t
的 11 檔 SPDR 類股 ETF 自身收盤與自身 50 日簡單均線算 b_t（口徑逐字同
scripts/build_breadth_base_rates.py），查 data/breadth_base_rates.json 的固定門檻桶表分類，
機械產生兩筆 forecast 草案（同一 episode_id，不同 horizon），append 進
knowledge/forecasts.jsonl（source: "breadth"）：

  ① claim_template=breadth_spy_up_21d：{resolve_by}（30 曆日後）SPY 收盤高於 t 的收盤
     resolver window=at_expiry, series=pxd:SPY, op=">"
  ② claim_template=breadth_spy_up_63d：{resolve_by}（91 曆日後）SPY 收盤高於 t 的收盤
     resolver window=at_expiry, series=pxd:SPY, op=">"（同一 resolver.value）

p 值完全由桶表機械給出（cell n<30 時退回 pooled）——不需人工判斷、也不接受人工覆寫。
p_clim 取自同表的無條件（pooled）頻率。

**resolver 數值來源刻意跨檔**：b_t 用 data/statlab_prices.json 算，但 SPY 收盤
（resolver.value、claim 文字中的 {close}）改讀 data/flowmap_prices.json 於「同一日期 t」的
bar——因為 pxd: 域結算時讀的正是 data/flowmap_prices.json（見
knowledge/settle_forecasts.py），若改用 statlab 的收盤，落帳當下記的 value 會與日後結算
實際比對的來源不一致。t 若早於 statlab 自身最後一根 bar（即回溯命中），落點與落差會印到
stderr（不靜默）；回溯 5 個交易日內仍找不到共同日期，才整批跳過（reason=date_mismatch，
下週再試）。

CLI
---
  python scripts/generate_breadth_forecasts.py            dry-run，兩筆草案印到 stdout（純 JSONL）
  python scripts/generate_breadth_forecasts.py --write     append 進 knowledge/forecasts.jsonl
                                                            （查重：同一 YYYY-MM 若已有 source=
                                                            "breadth" 的筆數，整批拒絕落帳）
  python scripts/generate_breadth_forecasts.py --write --ledger <path>   落帳到指定帳簿（測試用）
跳過/拒絕原因印到 stderr，不混進 stdout 的 JSONL 草案。

dry-run 路徑刻意不 import knowledge/forecast_lib.py——只有 --write 路徑才 import，缺檔時
清楚印訊息到 stderr 並 exit 2（慣例同 scripts/generate_vrp_forecasts.py）。
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
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
BASE_RATES = ROOT / "data" / "breadth_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

SOURCE = "breadth"
SCHEMA = "fc-v2"
SPY_TICKER = "SPY"
SECTOR_TICKERS = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
SMA_WINDOW = 50                 # 須與 build_breadth_base_rates.py 一致（僅供口徑核對）
MIN_AVAILABLE_SECTORS = 9       # 同上
MIN_CELL_N = 30                 # cell n < 30 → 用 pooled（同上）
MAX_LOOKBACK_TRADING_DAYS = 5   # statlab／flowmap 共同 SPY 日期回溯上限（orchestrator 2026-09-02 裁定）

TEMPLATES = [
    # (claim_template, freq_key, n_key, horizon_calendar_days, trading_days_label)
    ("breadth_spy_up_21d", "freq_up_21d", "n_21d", 30, 21),
    ("breadth_spy_up_63d", "freq_up_63d", "n_63d", 91, 63),
]

BUCKET_DESC_ZH = {
    "low": "參與度低（洗盤區）",
    "mid": "參與度中性",
    "high": "參與度高（廣度強）",
}


def warn(msg: str) -> None:
    print(f"[breadth-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[breadth-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：共同日 t（statlab／flowmap 皆有 SPY bar，回溯上限 MAX_LOOKBACK_TRADING_DAYS）+
# 該日的 b_t
# ═══════════════════════════════════════════════════════════════════════════

def _load_series(data, ticker):
    bars = (data.get("series") or {}).get(ticker)
    if not bars:
        return None
    return sorted(((d, c) for d, c in bars), key=lambda x: x[0])


def resolve_common_t_and_breadth(statlab_path=STATLAB_PRICES, flowmap_path=FLOWMAP_PRICES,
                                  sector_tickers=SECTOR_TICKERS, window=SMA_WINDOW,
                                  max_lookback=MAX_LOOKBACK_TRADING_DAYS):
    """回傳 (t, b_t, n_avail, spy_close, statlab_last, flowmap_last)。

    t＝從 statlab SPY 最後一根 bar（statlab_last）開始，最多回溯 max_lookback 個 statlab
    自身交易日，找到的第一個「同時存在於 data/flowmap_prices.json SPY 序列」的日期；
    5 個交易日內仍找不到共同日期 → 丟出 DateMismatch（缺檔/無 SPY 資料同樣視為
    DateMismatch，因為問題本質相同：resolver 值來源缺席）。

    b_t／n_avail 口徑逐字同 scripts/build_breadth_base_rates.py：對每檔類股 ETF 各自的
    日線序列找 t 當日的收盤與自身累計根數是否 ≥ window，可算則判斷是否站上自身 50 日 SMA
    （用該 ETF 自己的最近 window 根收盤，非用 SPY 的位置索引對齊——各序列起始日可能相差
    一天，位置索引不可靠，須逐檔以日期字串精確比對）。統計不足（可用 < MIN_AVAILABLE_SECTORS
    檔）視為結構性資料問題，直接 SystemExit（非 date_mismatch 這種「下週再試」可回復的狀況）。
    """
    if not statlab_path.exists():
        raise SystemExit(f"找不到 {statlab_path}")
    try:
        statlab_data = json.loads(statlab_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {statlab_path}: {e}")

    spy_bars = _load_series(statlab_data, SPY_TICKER)
    if not spy_bars:
        raise SystemExit(f"{statlab_path} 無 {SPY_TICKER} 資料")
    statlab_last = spy_bars[-1][0]
    statlab_spy_dates = [d for d, _ in spy_bars]

    if not flowmap_path.exists():
        raise DateMismatch(f"{flowmap_path} 不存在")
    try:
        flowmap_data = json.loads(flowmap_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise DateMismatch(f"無法讀取 {flowmap_path}: {e}")
    flowmap_spy_bars = _load_series(flowmap_data, SPY_TICKER)
    if not flowmap_spy_bars:
        raise DateMismatch(f"{flowmap_path} 無 {SPY_TICKER} 資料")
    flowmap_map = dict(flowmap_spy_bars)
    flowmap_last = flowmap_spy_bars[-1][0]

    # candidates：statlab 最後 max_lookback 個交易日，由近到遠排序
    candidates = list(reversed(statlab_spy_dates[-max_lookback:]))
    t = next((d for d in candidates if d in flowmap_map), None)
    if t is None:
        raise DateMismatch(
            f"statlab SPY 最後 {max_lookback} 個交易日（{candidates[-1]}..{candidates[0]}）"
            f"皆不在 {flowmap_path} 的 SPY 序列中（flowmap 最新={flowmap_last}）")

    spy_close = flowmap_map[t]

    flags = []
    for tk in sector_tickers:
        bars = _load_series(statlab_data, tk)
        if not bars:
            continue
        dates = [d for d, _ in bars]
        closes = [c for _, c in bars]
        pos = bisect.bisect_left(dates, t)
        if pos >= len(dates) or dates[pos] != t:
            continue  # 該 ETF 於 t 當日無 bar（不在母體可用集合）
        if pos + 1 < window:
            continue  # 累計根數不足，非「可用」
        window_closes = closes[pos - window + 1: pos + 1]
        sma = sum(window_closes) / window
        flags.append(closes[pos] > sma)

    n_avail = len(flags)
    if n_avail < MIN_AVAILABLE_SECTORS:
        raise SystemExit(f"{t} 可用類股 ETF 僅 {n_avail} 檔（< {MIN_AVAILABLE_SECTORS}），無法算 b_t")

    b = round(100.0 * sum(1 for f in flags if f) / n_avail, 4)
    return t, b, n_avail, spy_close, statlab_last, flowmap_last


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：桶表（data/breadth_base_rates.json，固定門檻，非 in-sample 切點）
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates(path=BASE_RATES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_breadth_base_rates.py")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")


def classify_bucket(b, cuts):
    if b < cuts["low_max"]:
        return "low"
    if b > cuts["high_min"]:
        return "high"
    return "mid"


def lookup_bucket_row(base_rates, b):
    cuts = base_rates["cuts"]
    bucket = classify_bucket(b, cuts)
    row = base_rates["buckets"].get(bucket)
    if row is None:
        raise SystemExit(f"桶 {bucket} 不存在於 base rate 表，異常，中止")
    return bucket, row


def pick_p(base_rates, bucket, row, freq_key, n_key):
    """cell n < MIN_CELL_N（或 freq 為 None）→ 退回 pooled（設計稿 §2 明文）。回傳
    (p, n_used, used_pooled)。"""
    n = row.get(n_key)
    freq = row.get(freq_key)
    if freq is not None and n is not None and n >= MIN_CELL_N:
        return freq, n, False
    pooled = base_rates.get("pooled", {})
    p_pooled = pooled.get(freq_key)
    n_pooled = pooled.get(n_key)
    if p_pooled is None:
        raise SystemExit(f"桶 {bucket} 的 {freq_key} 為 None 且 pooled 亦無值，base rate 表異常，中止")
    return p_pooled, n_pooled, True


# ═══════════════════════════════════════════════════════════════════════════
# id 產生（dry-run 本地版；--write 改走 forecast_lib.next_ids）
# ═══════════════════════════════════════════════════════════════════════════

def _local_next_ids(ts_str, n, path=FORECASTS):
    """回傳 n 個未被佔用的 fc_{YYYYMMDD}_breadth_NN id（掃現有檔避免同日重跑撞號）。
    僅供 dry-run 使用；--write 路徑改用 knowledge/forecast_lib.py 的 fl.next_ids
    （單一權威來源，慣例同 scripts/generate_vrp_forecasts.py）。"""
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
    prefix = f"fc_{ts_str.replace('-', '')}_{SOURCE}_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{prefix}{seq:02d}"
        if cand not in used:
            out.append(cand)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

class DateMismatch(Exception):
    """statlab 最後 MAX_LOOKBACK_TRADING_DAYS 個交易日回溯範圍內找不到與 flowmap 的共同
    SPY 日期（或 flowmap 缺檔/無 SPY 資料）——非致命，呼叫端印 warn 後乾淨跳過（下週再試）。"""


def build_drafts(ids, today=None, statlab_path=STATLAB_PRICES, flowmap_path=FLOWMAP_PRICES,
                  base_rates_path=BASE_RATES):
    today = today or date.today()
    ts_str = today.isoformat()
    month_prefix = today.strftime("%Y-%m")

    t, b, n_avail, spy_close, statlab_last, flowmap_last = resolve_common_t_and_breadth(
        statlab_path=statlab_path, flowmap_path=flowmap_path)
    if t != statlab_last:
        info(f"statlab 最新 {statlab_last}，flowmap 最新 {flowmap_last}，取共同日 {t}")

    base_rates = load_base_rates(base_rates_path)
    bucket, row = lookup_bucket_row(base_rates, b)
    p_clim_table = base_rates.get("p_clim", {})

    base_meta = (f"base_rate built_at={base_rates.get('built_at')}｜bucket={bucket}"
                 f"（b_range={row.get('b_range')}）｜cuts={base_rates.get('cuts')}")
    source_ref = (f"data/statlab_prices.json 類股 ETF as_of={t}（可用={n_avail}/{len(SECTOR_TICKERS)}）｜"
                  f"data/flowmap_prices.json SPY at {t}｜data/breadth_base_rates.json {base_meta}")

    drafts = []
    episode_id = f"breadth:{month_prefix}"
    block_key = month_prefix
    bucket_zh = BUCKET_DESC_ZH[bucket]

    for i, (claim_template, freq_key, n_key, horizon_days, td_label) in enumerate(TEMPLATES):
        p, n_used, used_pooled = pick_p(base_rates, bucket, row, freq_key, n_key)
        p_clim = p_clim_table.get(claim_template)
        resolve_by = (today + timedelta(days=horizon_days)).isoformat()

        claim = (f"{resolve_by} 前（約 {td_label} 個交易日）：SPY 收盤高於 {t} 的 {spy_close}｜"
                 f"市場廣度條件：11 個類股 ETF 站上 50 日均線比例 {b:.0f}%（{bucket_zh}）")

        draft = {
            "id": ids[i],
            "ts": ts_str,
            "source": SOURCE,
            "source_ref": source_ref,
            "claim": claim,
            "p": p,
            "horizon_days": horizon_days,
            "resolve_by": resolve_by,
            "resolver": {"series": f"pxd:{SPY_TICKER}", "op": ">", "value": spy_close, "window": "at_expiry"},
            "status": "open",
            "resolved_ts": None,
            "outcome": None,
            "brier": None,
            "note": (f"breadth 機械賦值（無需人工判斷）｜b_t={b:.2f}%（可用={n_avail}/{len(SECTOR_TICKERS)}，"
                     f"as_of {t}）｜桶={bucket}｜p 取自 {'pooled（cell n<' + str(MIN_CELL_N) + ' 退回)' if used_pooled else '桶表'} "
                     f"{freq_key}（n={n_used}）｜{base_meta}"),
            # schema v2 additive 欄位（設計稿 §2）——dry-run 亦直接填齊，寫檔路徑
            # forecast_lib.finalize/append 對已齊欄位為冪等覆核，不重算既有值。
            "schema": SCHEMA,
            "claim_template": claim_template,
            "p_clim": p_clim,
            "p_clim_ref": (f"data/breadth_base_rates.json built_at={base_rates.get('built_at')}｜"
                           f"pooled（無條件）頻率 {claim_template}｜取樣=SPY 每月首個交易日"
                           f"（n={base_rates.get('n_samples')}）"),
            "p_table_built_at": base_rates.get("built_at"),
            "episode_id": episode_id,
            "block_key": block_key,
            "twin_of": None,
        }
        drafts.append(draft)

    return drafts


# ═══════════════════════════════════════════════════════════════════════════
# 查重 + 落帳
# ═══════════════════════════════════════════════════════════════════════════

def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def month_already_has_source(path, month_prefix, source=SOURCE):
    """同月同 source 已有落帳紀錄 → True（查重口徑：整批月頻拒絕重複，同
    scripts/generate_vrp_forecasts.py 慣例）。"""
    for r in _existing_forecasts(path):
        if r.get("source") == source and (r.get("ts") or "").startswith(month_prefix):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="市場廣度預測 producer — 月頻手動觸發")
    ap.add_argument("--write", action="store_true", help="append 進帳簿（預設 dry-run）")
    ap.add_argument("--ledger", default=str(FORECASTS), help="帳簿路徑（測試用；預設 knowledge/forecasts.jsonl）")
    args = ap.parse_args()
    ledger_path = Path(args.ledger)

    today = date.today()
    ts_str = today.isoformat()
    month_prefix = today.strftime("%Y-%m")

    dup = month_already_has_source(ledger_path, month_prefix)

    if not args.write:
        try:
            ids = _local_next_ids(ts_str, len(TEMPLATES), ledger_path)
            drafts = build_drafts(ids, today=today)
        except DateMismatch as e:
            warn(f"date_mismatch：{e}——本次跳過，下週再試（不產生草案）。")
            return
        for d in drafts:
            print(json.dumps(d, ensure_ascii=False))
        if dup:
            warn(f"{month_prefix} 已有 source={SOURCE} 的落帳紀錄——本月重複落帳將被拒絕"
                 f"（查重口徑：同月同 source 整批拒絕）。")
        info(f"dry-run：共 {len(drafts)} 筆草案。--write 才會 append 進 {ledger_path}"
             f"（若 {month_prefix} 已有紀錄則整批拒絕）。")
        return

    if dup:
        print(f"# --write 拒絕：{month_prefix} 已有 source={SOURCE} 落帳紀錄，本月不重複落帳。",
              file=sys.stderr)
        sys.exit(1)

    sys.path.insert(0, str(ROOT / "knowledge"))
    try:
        import forecast_lib as fl  # noqa: E402
    except ImportError as e:
        print(f"[breadth-forecasts][ERROR] 找不到 knowledge/forecast_lib.py：{e}", file=sys.stderr)
        sys.exit(2)

    try:
        ids = fl.next_ids(ts_str, SOURCE, len(TEMPLATES), ledger_path)
        drafts = build_drafts(ids, today=today)
    except DateMismatch as e:
        warn(f"date_mismatch：{e}——本次跳過，下週再試（不落帳）。")
        return

    n_written, n_twins = fl.append(drafts, path=ledger_path, write=True)
    print(f"# --write：寫入 {n_written} 筆本尊 + {n_twins} 筆哨兵 twin → {ledger_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
