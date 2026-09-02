#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_risk_gauge_forecasts.py — 風險偏好分數（risk gauge）預測 producer
（forecast ledger v2 `_market_cockpit_design_20260902.md` §9 package F4 機械餵料）。

每月首週手動跑（不掛 cron，同 rv-model／vrp producer「先手動、養出使用習慣」慣例；設計稿
§9 F4 節奏欄："每月首週（查重同月）"）。從 `docs/cache/risk_history.json`（1,345 週的
`weeks`／`score`／`spx` 平行陣列）取最新一筆風險偏好分數，用
`scripts/build_risk_gauge_base_rates.py` 產出的 `data/risk_gauge_base_rates.json` 五分位表
分類，機械產生一筆 forecast 草案（source="risk-gauge"），append 進帳簿：

  claim_template=risk_spy_up_13w：{resolve_by}（13 週後，91 曆日）SPY 收盤高於今日
  {SPY 最新收盤}（{現值風險偏好分數} 落在第 {分位} 分位）
  resolver：pxd:SPY，op=">"，value=SPY 最新收盤（`data/flowmap_prices.json`），window=at_expiry

p 值完全由五分位表機械給出（該分位的經驗頻率 freq_up_13w）——不需人工判斷、也不接受人工
覆寫。p_clim 取自同表的無條件（pooled）頻率。

CLI
---
  python scripts/generate_risk_gauge_forecasts.py             dry-run，一筆草案印到 stdout（純 JSONL）
  python scripts/generate_risk_gauge_forecasts.py --write      append 進 knowledge/forecasts.jsonl
                                                                （查重：同一 YYYY-MM 若已有 source=
                                                                "risk-gauge" 的筆數，整批拒絕落帳）
  python scripts/generate_risk_gauge_forecasts.py --ledger /tmp/scratch.jsonl [--write]
                                                                測試用：覆寫查重／落帳目標路徑

跳過/拒絕原因印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RISK_HISTORY = ROOT / "docs" / "cache" / "risk_history.json"
BASE_RATES = ROOT / "data" / "risk_gauge_base_rates.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

SOURCE = "risk-gauge"
ID_PREFIX = "risk"
CLAIM_TEMPLATE = "risk_spy_up_13w"
HORIZON_CALENDAR_DAYS = 91  # 13 週 ≈ 91 曆日（同 rv-model／vrp producer 交易日↔曆日既有近似取捨）
SPY_TICKER = "SPY"

sys.path.insert(0, str(ROOT / "knowledge"))
import forecast_lib as fl  # noqa: E402 — id 產生／v2 欄位補齊／落帳＋哨兵 twin


def warn(msg: str) -> None:
    print(f"[risk-gauge-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[risk-gauge-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：目前風險偏好分數（docs/cache/risk_history.json 最新一週）
# ═══════════════════════════════════════════════════════════════════════════

def current_risk_score(path=RISK_HISTORY):
    """回傳 (week_label, score) 或 (None, None)（缺檔/格式錯誤/空陣列）。"""
    if not path.exists():
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {path}: {e}")
        return None, None
    weeks = data.get("weeks") or []
    score = data.get("score") or []
    if not weeks or not score or len(weeks) != len(score):
        warn(f"{path} 的 weeks/score 陣列缺失或長度不一致")
        return None, None
    return weeks[-1], score[-1]


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：SPY 最新收盤（data/flowmap_prices.json）
# ═══════════════════════════════════════════════════════════════════════════

def latest_spy_close(path=FLOWMAP_PRICES, ticker=SPY_TICKER):
    """回傳 (date, close) 或 (None, None)。"""
    if not path.exists():
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {path}: {e}")
        return None, None
    bars = (data.get("series") or {}).get(ticker)
    if not bars:
        return None, None
    bars_sorted = sorted(bars, key=lambda x: x[0])
    d, c = bars_sorted[-1]
    return d, c


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：五分位 base rate 表（data/risk_gauge_base_rates.json）
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates(path=BASE_RATES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_risk_gauge_base_rates.py")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")


def classify_quintile(score, cutoffs):
    q20, q40, q60, q80 = cutoffs
    if score <= q20:
        return "Q1"
    if score <= q40:
        return "Q2"
    if score <= q60:
        return "Q3"
    if score <= q80:
        return "Q4"
    return "Q5"


def lookup_quintile_row(base_rates, score):
    cutoffs = base_rates["score_quintile_cutoffs_pct20_40_60_80"]
    q = classify_quintile(score, cutoffs)
    row = next((r for r in base_rates["quintiles"] if r["quintile"] == q), None)
    if row is None or not row.get("n"):
        raise SystemExit(f"分位 {q} 樣本數為 0，base rate 表異常，中止（不可硬猜 p）")
    return q, row


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

def build_drafts(ids, today=None, risk_history_path=RISK_HISTORY, base_rates_path=BASE_RATES,
                  flowmap_prices_path=FLOWMAP_PRICES):
    today = today or date.today()
    ts_str = today.isoformat()
    month_prefix = today.strftime("%Y-%m")

    week_label, current_score = current_risk_score(risk_history_path)
    if current_score is None:
        raise SystemExit(f"無法從 {risk_history_path} 取得目前風險偏好分數，中止")

    spy_date, spy_close = latest_spy_close(flowmap_prices_path)
    if spy_close is None:
        raise SystemExit(f"無法從 {flowmap_prices_path} 取得 {SPY_TICKER} 最新收盤，中止")

    base_rates = load_base_rates(base_rates_path)
    quintile, row = lookup_quintile_row(base_rates, current_score)
    p = row.get("freq_up_13w")
    if p is None:
        raise SystemExit(f"分位 {quintile} 的 freq_up_13w 為 null，base rate 表異常，中止")
    p_clim = (base_rates.get("p_clim") or {}).get("risk_spy_up_13w")

    q_num = quintile[1] if len(quintile) > 1 else quintile
    resolve_by = (today + timedelta(days=HORIZON_CALENDAR_DAYS)).isoformat()

    claim = (f"{resolve_by} 前（13 週後）：SPY 收盤高於今日 {spy_close}"
             f"（風險偏好分數 {current_score} 落在第 {q_num} 分位）")

    base_meta = (f"base_rate built_at={base_rates.get('built_at')}｜分位={quintile}"
                 f"（range={row.get('score_range')}, n={row.get('n')}）｜"
                 f"cutoffs={base_rates.get('score_quintile_cutoffs_pct20_40_60_80')}")
    source_ref = (f"docs/cache/risk_history.json week={week_label} score={current_score}｜"
                  f"data/flowmap_prices.json {SPY_TICKER} date={spy_date} close={spy_close}｜"
                  f"data/risk_gauge_base_rates.json {base_meta}")

    episode_id = f"{ID_PREFIX}:{month_prefix}"
    block_key = month_prefix

    draft = {
        "id": ids[0],
        "ts": ts_str,
        "source": SOURCE,
        "source_ref": source_ref,
        "claim": claim,
        "p": p,
        "horizon_days": HORIZON_CALENDAR_DAYS,
        "resolve_by": resolve_by,
        "resolver": {"series": f"pxd:{SPY_TICKER}", "op": ">", "value": spy_close, "window": "at_expiry"},
        "status": "open",
        "resolved_ts": None,
        "outcome": None,
        "brier": None,
        "note": (f"risk-gauge 機械賦值（無需人工判斷）｜取樣週={week_label}、"
                 f"風險偏好分數={current_score}｜分位={quintile}｜p 取自五分位表 freq_up_13w｜"
                 f"{base_meta}"),
        "schema": fl.SCHEMA_V2,
        "claim_template": CLAIM_TEMPLATE,
        "p_clim": p_clim,
        "p_clim_ref": (f"data/risk_gauge_base_rates.json built_at={base_rates.get('built_at')}｜"
                       f"無條件頻率 {CLAIM_TEMPLATE}｜取樣=每月首週"
                       f"（n={base_rates.get('p_clim_n')}）"),
        "p_table_built_at": base_rates.get("built_at"),
        "episode_id": episode_id,
        "block_key": block_key,
        "twin_of": None,
    }
    return [draft]


# ═══════════════════════════════════════════════════════════════════════════
# 查重 + 落帳
# ═══════════════════════════════════════════════════════════════════════════

def month_already_has_source(ledger_path, month_prefix, source=SOURCE):
    """同月同 source 已有落帳紀錄 → True（查重口徑：整批月頻拒絕重複，同
    scripts/generate_vrp_forecasts.py 慣例）。"""
    for r in fl.existing(ledger_path):
        if r.get("source") == source and (r.get("ts") or "").startswith(month_prefix):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="風險偏好分數（risk gauge）預測 producer — 月頻手動觸發")
    ap.add_argument("--write", action="store_true", help="append 進帳簿（預設 dry-run）")
    ap.add_argument("--ledger", default=None,
                     help="覆寫查重／落帳目標路徑（預設 knowledge/forecasts.jsonl）")
    args = ap.parse_args()

    ledger_path = Path(args.ledger) if args.ledger else FORECASTS

    today = date.today()
    ts_str = today.isoformat()
    month_prefix = today.strftime("%Y-%m")

    dup = month_already_has_source(ledger_path, month_prefix)

    if not args.write:
        ids = fl.next_ids(ts_str, ID_PREFIX, 1, ledger_path)
        drafts = fl.finalize(build_drafts(ids, today=today))
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

    ids = fl.next_ids(ts_str, ID_PREFIX, 1, ledger_path)
    drafts = fl.finalize(build_drafts(ids, today=today))
    n_written, n_twins = fl.append(drafts, path=ledger_path, write=True)
    print(f"# --write：寫入 {n_written} 筆本尊 + {n_twins} 筆哨兵 twin → {ledger_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
