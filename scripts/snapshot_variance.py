#!/usr/bin/env python3
"""財務 variance 週快照 — 把 `docs/catalyst/variance.json` 每週的橫斷面疊成史。

`build_variance_tracker.py` 每週日只覆寫 `docs/catalyst/variance.json`（單一橫
斷面，前一週的漂移數字沒地方看）。本腳本讀那份橫斷面，append 一筆到
`docs/catalyst/variance_history.json`（schema `variance-history-v1`），讓下游
（未來的 `epsdrift:` resolver、趨勢圖）能看到 base_eps／consensus_eps／
drift_pct 隨時間怎麼變。

規則：
  · as_of = variance.json 的 generated_at 前 10 碼（YYYY-MM-DD）。
  · 同 as_of 已存在 → 整筆覆寫（冪等：同一份 variance.json 重跑兩次，輸出
    byte-for-byte 相同）；否則新增。
  · snapshots 依 as_of 升冪排序；不裁舊（史料只增不減）。
  · variance.json 的 rows[] 同一 ticker 固定兩筆（FY+0／FY+1 兩個財年），故
    本檔 rows 兩層巢狀：TICKER → FY_LABEL → {fy_end, base_eps, consensus_eps,
    drift_pct, flag}，讓未來 `epsdrift:` resolver 能點名指定財年（如 FY+1）
    取值，不會被同 ticker 的另一財年蓋掉。萬一來源真的出現同 ticker＋同
    fy_label 兩筆（目前資料未見），單純依來源順序覆寫、最後一筆為準。
  · n = variance.json 原始 rows[] 筆數（含每 ticker 兩財年，故 = 2 × 檔數，
    現況 214）；n_tickers = 去重後的 ticker 數（現況 107）。
  · `docs/catalyst/variance.json` 不存在 → 印訊息到 stderr、exit 0（週更管線
    這步失敗不該擋掉整個 catalyst 工作流）。

CLI：
  python3 scripts/snapshot_variance.py
  python3 scripts/snapshot_variance.py --variance path/to/variance.json --out path/to/variance_history.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
VARIANCE_JSON = ROOT / "docs" / "catalyst" / "variance.json"
HISTORY_JSON = ROOT / "docs" / "catalyst" / "variance_history.json"

SCHEMA = "variance-history-v1"
INNER_FIELDS = ("fy_end", "base_eps", "consensus_eps", "drift_pct", "flag")


def build_snapshot(doc: dict) -> dict:
    """把 variance.json 的整份文件收斂成一筆
    {as_of, generated_at, n, n_tickers, rows}，rows 為 TICKER → FY_LABEL →
    {fy_end, base_eps, consensus_eps, drift_pct, flag} 兩層巢狀。"""
    generated_at = doc.get("generated_at", "")
    as_of = generated_at[:10]

    rows: dict = {}
    n = 0
    for row in doc.get("rows", []):
        ticker = row.get("ticker")
        fy_label = row.get("fy_label")
        if not ticker or not fy_label:
            continue
        n += 1
        rows.setdefault(ticker, {})[fy_label] = {
            field: row.get(field) for field in INNER_FIELDS
        }

    return {
        "as_of": as_of,
        "generated_at": generated_at,
        "n": n,
        "n_tickers": len(rows),
        "rows": rows,
    }


def load_history(path: Path) -> dict:
    if not path.exists():
        return {"schema": SCHEMA, "snapshots": []}
    return json.loads(path.read_text(encoding="utf-8"))


def upsert_snapshot(history: dict, snapshot: dict) -> dict:
    snapshots = [s for s in history.get("snapshots", []) if s.get("as_of") != snapshot["as_of"]]
    snapshots.append(snapshot)
    snapshots.sort(key=lambda s: s.get("as_of", ""))
    history["schema"] = SCHEMA
    history["snapshots"] = snapshots
    return history


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--variance", default=None,
                   help=f"variance.json 路徑覆寫（預設 {VARIANCE_JSON}）")
    p.add_argument("--out", default=None,
                   help=f"variance_history.json 路徑覆寫（預設 {HISTORY_JSON}）")
    args = p.parse_args()

    variance_path = Path(args.variance) if args.variance else VARIANCE_JSON
    out_path = Path(args.out) if args.out else HISTORY_JSON

    if not variance_path.exists():
        print(f"snapshot_variance: {variance_path} 不存在，略過本次快照。",
              file=sys.stderr)
        return 0

    doc = json.loads(variance_path.read_text(encoding="utf-8"))
    snapshot = build_snapshot(doc)

    history = load_history(out_path)
    history = upsert_snapshot(history, snapshot)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(history, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    print(f"snapshot_variance: as_of={snapshot['as_of']} n={snapshot['n']} "
          f"n_tickers={snapshot['n_tickers']} → {out_path} "
          f"({len(history['snapshots'])} snapshots total)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
