#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_credit_forecasts.py — 信用領先（HYG／LQD 比值 21 日動能）預測 producer
（forecast ledger P2 package G1 機械餵料）。

每月首次班車手動觸發（不掛 cron，同 rv-model／vrp producer「先手動、養出使用習慣」慣例）。
從 `docs/monitor/data/latest.json` categories[key="credit"] 的 `hyg_lqd` item 取最新 spark
（30 日 HYG／LQD 比值），算 x_t ＝ 100 × ln(spark[−1] ／ spark[−22])（21 個交易日對數變化，
%；口徑逐字同 scripts/build_credit_base_rates.py），查 `data/credit_base_rates.json` 的
三分位桶表分類，機械產生兩筆 forecast 草案（同一 episode_id，不同 horizon），append 進
帳簿（source="credit-lead"）：

  ① claim_template=credit_spy_up_21d：{resolve_by}（30 曆日後 ≈21 個交易日）SPY 收盤高於
     hyg_lqd item.date 當日收盤；resolver window=at_expiry, series=pxd:SPY, op=">"
  ② claim_template=credit_spy_up_63d：{resolve_by}（91 曆日後 ≈63 個交易日）同上

p 值完全由三分位桶表機械給出（該桶的經驗頻率；cell n < 30 時改用 pooled 頻率）——不需人工
判斷、也不接受人工覆寫。p_clim 取自同表的 pooled（無條件）頻率。

SPY 今收讀取順序（orchestrator 2026-09-02 補丁，因應 flowmap 快取常落後 hyg_lqd
item.date 一天的實測現況；設計稿 §1 對此順序未置一詞，屬機械口徑補充，非放寬命題）：
①`data/flowmap_prices.json` series.SPY 於 item.date **當日**的 bar；②同日皆無則退到
`data/statlab_prices.json` series.SPY 於 item.date 當日的 bar（同為 yfinance 還原收盤、
日頻，口徑相同來源）；③兩者皆無此日 → 跳過，reason=date_mismatch，不印任何 JSONL，下次
班車再試（不做「找最近一個交易日」的近似）。實際取用的來源記入草案 note（
`spy_close_src=flowmap`／`statlab`）供稽核。

CLI
---
  python scripts/generate_credit_forecasts.py                       dry-run，兩筆草案印到 stdout（純 JSONL）
  python scripts/generate_credit_forecasts.py --write                append 進 knowledge/forecasts.jsonl
                                                                       （查重：同一 YYYY-MM 若已有 source=
                                                                       "credit-lead" 的筆數，整批拒絕落帳）
  python scripts/generate_credit_forecasts.py --write --ledger PATH  測試用：覆寫查重／落帳目標路徑

跳過/拒絕原因印到 stderr，不混進 stdout 的 JSONL 草案。dry-run 路徑刻意不 import
knowledge/forecast_lib.py（沿用 scripts/generate_vrp_forecasts.py 慣例）——只有 --write 路徑
才 import，缺檔時清楚印訊息到 stderr 並 exit 2。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
STATLAB_PRICES = ROOT / "data" / "statlab_prices.json"  # SPY 收盤退路來源 #2（orchestrator 補丁）
BASE_RATES = ROOT / "data" / "credit_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

SOURCE = "credit-lead"
ID_PREFIX = "credit"
SCHEMA = "fc-v2"
SPY_TICKER = "SPY"
X_LOOKBACK_SPARK = 22   # spark[-1] vs spark[-22]（21 個交易日對數變化）；須與 builder 的
                        # X_LOOKBACK_TRADING_DAYS 一致（PREREG 凍結，設計稿 §1）
MIN_CELL_N = 30         # cell n < 30 → 用 pooled（PREREG 凍結，設計稿 §1）

# (claim_template, horizon_calendar_days, trading_days_label, n_key, freq_key)
TEMPLATES = [
    ("credit_spy_up_21d", 30, 21, "n_21d", "freq_up_21d"),
    ("credit_spy_up_63d", 91, 63, "n_63d", "freq_up_63d"),
]

BUCKET_ZH = {
    "low": "高收益利差走闊，風險偏好轉弱",
    "mid": "利差持平",
    "high": "高收益利差收斂，風險偏好轉強",
}


def warn(msg: str) -> None:
    print(f"[credit-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[credit-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：目前信用領先訊號（docs/monitor/data/latest.json credit/hyg_lqd）
# ═══════════════════════════════════════════════════════════════════════════

def load_credit_signal(latest_path=MONITOR_LATEST):
    """回傳 (item_date, x) 或 (None, None)（缺檔／缺 item）。spark 點數不足或含非正值屬資料
    異常，直接 SystemExit（同 vrp 慣例：致命資料問題不靜默跳過）。"""
    if not latest_path.exists():
        warn(f"找不到 {latest_path}")
        return None, None
    try:
        data = json.loads(latest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {latest_path}: {e}")
        return None, None

    item = None
    for cat in data.get("categories", []):
        if cat.get("key") == "credit":
            for it in cat.get("items", []):
                if it.get("key") == "hyg_lqd":
                    item = it
                    break
    if item is None:
        warn(f"{latest_path} 找不到 categories[key=credit] 的 hyg_lqd item")
        return None, None

    spark = item.get("spark") or []
    if len(spark) < X_LOOKBACK_SPARK:
        raise SystemExit(f"hyg_lqd spark 僅 {len(spark)} 點，不足 {X_LOOKBACK_SPARK} 點，"
                          f"無法算 x，中止")
    r_now, r_then = spark[-1], spark[-X_LOOKBACK_SPARK]
    if r_then <= 0 or r_now <= 0:
        raise SystemExit(f"hyg_lqd spark 含非正值（r_now={r_now}, r_then={r_then}），中止")

    x = round(100 * math.log(r_now / r_then), 4)
    return item.get("date"), x


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：SPY 於 item_date 當日收盤 —— 退路鏈（orchestrator 2026-09-02 補丁）：
#   ① data/flowmap_prices.json ② data/statlab_prices.json ③ 皆無 → None（date_mismatch）
# ═══════════════════════════════════════════════════════════════════════════

def _spy_close_from(prices_path, item_date):
    """單一來源查表，找不到檔／解析失敗／無該日 bar 一律回傳 None（不視為致命錯誤，
    由呼叫端決定要不要退到下一個來源）。"""
    if not prices_path.exists():
        return None
    try:
        data = json.loads(prices_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {prices_path}: {e}")
        return None
    bars = dict((d, c) for d, c in (data.get("series") or {}).get(SPY_TICKER, []))
    return bars.get(item_date)


def load_spy_close(item_date, flowmap_path=FLOWMAP_PRICES, statlab_path=STATLAB_PRICES):
    """回傳 (close, source) 或 (None, None)。退路順序：flowmap → statlab（同為 yfinance
    還原收盤、日頻，口徑相同來源，僅快取更新時點不同）→ 皆無此日則 (None, None)，由呼叫端
    以 date_mismatch 跳過。"""
    close = _spy_close_from(flowmap_path, item_date)
    if close is not None:
        return close, "flowmap"
    if not flowmap_path.exists():
        warn(f"找不到 {flowmap_path}")
    close = _spy_close_from(statlab_path, item_date)
    if close is not None:
        info(f"{flowmap_path.name} 無 {item_date} 的 SPY bar，退到 {statlab_path.name} 取得")
        return close, "statlab"
    if not statlab_path.exists():
        warn(f"找不到 {statlab_path}")
    return None, None


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：三分位桶 base rate 表（data/credit_base_rates.json）
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates(path=BASE_RATES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_credit_base_rates.py")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")


def classify_bucket(x, cuts):
    if x <= cuts["q33"]:
        return "low"
    if x <= cuts["q67"]:
        return "mid"
    return "high"


def lookup_bucket_row(base_rates, x):
    cuts = base_rates["cuts"]
    b = classify_bucket(x, cuts)
    row = (base_rates.get("buckets") or {}).get(b)
    if row is None:
        raise SystemExit(f"桶 {b} 不存在於 base rate 表，異常，中止")
    return b, row


# ═══════════════════════════════════════════════════════════════════════════
# id 產生（dry-run 本地版；--write 改走 forecast_lib.next_ids）
# ═══════════════════════════════════════════════════════════════════════════

def _local_next_ids(ts_str, n, path):
    """回傳 n 個未被佔用的 fc_{YYYYMMDD}_{ID_PREFIX}_NN id（掃現有帳簿避免同日重跑撞號）。
    僅供 dry-run 使用；--write 路徑改用 knowledge/forecast_lib.py 的 fl.next_ids。"""
    path = Path(path)
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
    prefix = f"fc_{ts_str.replace('-', '')}_{ID_PREFIX}_"
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

def build_drafts(ids, today=None, monitor_path=MONITOR_LATEST, flowmap_path=FLOWMAP_PRICES,
                  statlab_path=STATLAB_PRICES, base_rates_path=BASE_RATES):
    """回傳 (drafts, skip_reason)。skip_reason 非 None 時 drafts＝[]（date_mismatch：
    flowmap／statlab 兩個來源在 item_date 當日皆無 SPY bar，屬正常班車節奏落差，非資料異常，
    等下次班車再試）。"""
    today = today or date.today()
    ts_str = today.isoformat()
    month_prefix = today.strftime("%Y-%m")

    item_date, x = load_credit_signal(monitor_path)
    if item_date is None:
        raise SystemExit(f"無法從 {monitor_path} 取得 hyg_lqd 信用領先訊號，中止")

    spy_close, spy_src = load_spy_close(item_date, flowmap_path, statlab_path)
    if spy_close is None:
        warn(f"{flowmap_path} 與 {statlab_path} 皆找不到 SPY 於 {item_date} 當日的收盤"
             f"（date_mismatch），本次不產生草案，下次班車再試")
        return [], "date_mismatch"

    base_rates = load_base_rates(base_rates_path)
    bucket, row = lookup_bucket_row(base_rates, x)
    p_clim_table = base_rates.get("p_clim", {})

    src_fname = flowmap_path.name if spy_src == "flowmap" else statlab_path.name
    base_meta = f"base_rate built_at={base_rates.get('built_at')}｜桶={bucket}｜cuts={base_rates.get('cuts')}"
    source_ref = (f"docs/monitor/data/latest.json credit/hyg_lqd date={item_date} x={x:+.4f}%｜"
                  f"data/{src_fname} SPY close({item_date})={spy_close}（spy_close_src={spy_src}）｜"
                  f"data/credit_base_rates.json {base_meta}")

    episode_id = f"credit:{month_prefix}"
    block_key = month_prefix

    drafts = []
    for i, (claim_template, horizon_days, td_label, n_key, freq_key) in enumerate(TEMPLATES):
        n_cell = row.get(n_key)
        p = row.get(freq_key)
        used_pooled = False
        if p is None or (n_cell is not None and n_cell < MIN_CELL_N):
            pooled = base_rates.get("pooled", {})
            p = pooled.get(freq_key)
            used_pooled = True
        if p is None:
            raise SystemExit(f"桶 {bucket} 與 pooled 的 {freq_key} 皆為 null，base rate 表異常，中止")

        p_clim = p_clim_table.get(claim_template)
        resolve_by = (today + timedelta(days=horizon_days)).isoformat()

        claim = (f"{resolve_by} 前（約 {td_label} 個交易日）：SPY 收盤高於 {item_date} 的 {spy_close}"
                 f"｜信用領先條件：HYG／LQD 比值 21 日變化 {x:+.2f}%（{BUCKET_ZH[bucket]}）")

        p_note = (f"p 取自 pooled {freq_key}（桶 {bucket} n_{td_label}d={n_cell}<{MIN_CELL_N}）"
                  if used_pooled else f"p 取自桶 {bucket} 的 {freq_key}")

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
            "note": (f"credit-lead 機械賦值（無需人工判斷）｜x（HYG／LQD 21 日對數變化）＝{x:+.4f}%"
                     f"（as_of {item_date}）｜spy_close_src={spy_src}｜桶={bucket}｜{p_note}｜{base_meta}"),
            "schema": SCHEMA,
            "claim_template": claim_template,
            "p_clim": p_clim,
            "p_clim_ref": (f"data/credit_base_rates.json built_at={base_rates.get('built_at')}｜"
                           f"pooled 無條件頻率 {claim_template}｜取樣=每月首個交易日"
                           f"（n_samples={base_rates.get('n_samples')}）"),
            "p_table_built_at": base_rates.get("built_at"),
            "episode_id": episode_id,
            "block_key": block_key,
            "twin_of": None,
        }
        drafts.append(draft)

    return drafts, None


# ═══════════════════════════════════════════════════════════════════════════
# 查重 + 落帳
# ═══════════════════════════════════════════════════════════════════════════

def _existing_forecasts(path):
    path = Path(path)
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
    ap = argparse.ArgumentParser(description="信用領先（HYG/LQD 比值）預測 producer — 月頻手動觸發")
    ap.add_argument("--write", action="store_true", help="append 進帳簿（預設 dry-run）")
    ap.add_argument("--ledger", default=None,
                     help="覆寫查重／落帳目標路徑（測試用；預設 knowledge/forecasts.jsonl）")
    args = ap.parse_args()

    ledger_path = Path(args.ledger) if args.ledger else FORECASTS

    today = date.today()
    ts_str = today.isoformat()
    month_prefix = today.strftime("%Y-%m")

    dup = month_already_has_source(ledger_path, month_prefix)

    if not args.write:
        ids = _local_next_ids(ts_str, len(TEMPLATES), ledger_path)
        drafts, skip_reason = build_drafts(ids, today=today)
        if skip_reason:
            info(f"dry-run：本次無草案（{skip_reason}），不印 JSONL。")
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
        print(f"[credit-forecasts][ERROR] 找不到 knowledge/forecast_lib.py（package A1 交付，"
              f"可能尚未完成）：{e}", file=sys.stderr)
        sys.exit(2)

    ids = fl.next_ids(ts_str, ID_PREFIX, len(TEMPLATES), ledger_path)
    drafts, skip_reason = build_drafts(ids, today=today)
    if skip_reason:
        info(f"本次無草案（{skip_reason}），不落帳。")
        return

    fl.finalize(drafts)
    n_written, n_twins = fl.append(drafts, path=ledger_path, write=True)
    print(f"# --write：寫入 {n_written} 筆本尊 + {n_twins} 筆哨兵 twin → {ledger_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
