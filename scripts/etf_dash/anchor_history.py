#!/usr/bin/env python3
"""anchor_history.py — "anchor line" fallback for build_etf_dash.py's
Exhibit 2 long EPS-index chart.

Background: build_long_eps_index() (see build_etf_dash.py) chains the
dd-screener latest.json git history into a long weighted-EPS index, but that
history is overwhelmingly US large-cap names (docs/dd-screener/latest.json's
current universe) — funds with little/no overlap with that universe (today:
TOPIX, ~2% coverage) fall below LONG_EPS_LINE_MIN_COVERAGE_PCT and the chart
shows a "coverage too low, not drawn" note instead of a line.

This module is the fallback: every FULL run (see build_etf_dash.py's tiered
update — persistent holdings+eps_trend refresh) already fetches, per
constituent, yfinance eps_trend's 7/30/60/90-days-ago "+1y" EPS estimates
(see ANCHOR_LINE_DEFS in build_etf_dash.py). Those four points plus "today"
give five ETF-level relative-EPS-level snapshots per FULL run, cheap to
compute (no extra API calls — same data already fetched for Exhibit 1's
period table) and worth keeping even though a single run's memory only spans
90 days: chained across FULL runs (weekly for most funds, monthly for
TOPIX — see FUND_REGISTRY["TOPIX"]["full_refresh"]), it accumulates into a
line with much longer memory, the same way build_long_eps_index()'s
dd-screener chain does, just from a different upstream source and with much
sparser sampling (one 5-point snapshot per FULL run instead of one point per
trading day).

Storage: append-only JSONL, one line per FULL run (not one per day — see
above), data/etf_dash/anchor_history/{ETF}.jsonl:
    {"eps_as_of": "YYYY-MM-DD",
     "points": [{"date": "...", "level": 92.3, "coverage_pct": 88.1}, ...]}
  "points" has exactly 5 entries (eps_as_of minus 90/60/30/7/0 days, sorted
  oldest-to-newest); "level" is THAT RUN'S OWN relative level with
  eps_as_of == 100 (see build_etf_dash.py::build_anchor_line_point()) — not
  yet chained to any other run's scale, that happens in splice_runs() below.
  A same-day rerun (same eps_as_of) only rewrites the last line — same
  idempotency convention as dd_eps_history.py::append_today().

Splicing (splice_runs()) is this module's core logic — see its docstring for
the exact chain-linking rule and the >90-day gap → new-segment rule.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ANCHOR_HISTORY_DIR = ROOT / "data" / "etf_dash" / "anchor_history"

# 銜接錨點所在日期，與「目前序列最後一個已存點」日期相距超過這麼多天，視為
# 斷點（不再信任比例銜接），另起一段——同一個門檻沿用 yfinance eps_trend 本身
# 記憶的長度（90 天），因為一個 FULL run 的 5 個點本來就只覆蓋 eps_as_of 前
# 90 天，超過這個天數兩次 run 之間就不可能有任何一個點重疊得上。
GAP_SEGMENT_THRESHOLD_DAYS = 90


def _path(etf_key: str) -> Path:
    return ANCHOR_HISTORY_DIR / f"{etf_key}.jsonl"


# ---------------------------------------------------------------------------
# Persistence — append-only JSONL, mirrors dd_eps_history.py's conventions.
# ---------------------------------------------------------------------------


def load_runs(etf_key: str) -> list[dict]:
    """回傳這檔基金已存的全部 FULL run 快照（依檔案順序——理論上已經是
    eps_as_of 由舊到新，因為只 append／改最後一行）。不存在或壞掉的行都不會
    讓整個讀取失敗（壞行跳過並警告），跟 dd_eps_history.py 的既有行為一致。"""
    path = _path(etf_key)
    if not path.exists():
        return []
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError as e:
            print(f"[anchor_history] WARNING skipping malformed line {i + 1} in {path}: {e}", file=sys.stderr)
    return out


def append_run(etf_key: str, run: dict) -> None:
    """Append 一筆 FULL run 快照；同一個 eps_as_of 重跑只覆寫最後一行（冪等，
    跟 dd_eps_history.py::append_today() 同一個慣例）。規模天生很小（一檔基金
    一次 FULL 一行，多數基金週頻、TOPIX 月頻），用「整份讀出、必要時換掉最後
    一行、整份寫回」不會有效能問題，不需要 dd_eps_history.py 那種「只 append
    不重寫」的效能考量。"""
    rows = load_runs(etf_key)
    if rows and rows[-1].get("eps_as_of") == run.get("eps_as_of"):
        rows[-1] = run
    else:
        rows.append(run)
    path = _path(etf_key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Splicing — pure functions, no file I/O, easy to unit test directly.
# ---------------------------------------------------------------------------


def _value_on_or_before(points: list[dict], target_date: str) -> dict | None:
    """跟 build_etf_dash.py::_closest_close_on_or_before() 同一種「找不到當天
    就退回前一個有資料的點」近似——銜接錨點的日期不一定精確等於某個已存點的
    日期（例如月頻 run 彼此間隔 28-31 天，不是剛好 30 天），這裡用「最接近但
    不晚於」取代線性內插，跟本檔案／建構模組其餘部分的既有設計一致，避免
    多引入一種插值方法。"""
    candidates = [p for p in points if p["date"] <= target_date]
    return candidates[-1] if candidates else None


def splice_runs(runs: list[dict]) -> tuple[list[dict], list[dict]]:
    """把多次 FULL run 各自的 5 點快照（每個 run 自己的 eps_as_of == 100，見
    模組開頭 docstring）串成一條連續序列。

    規則：
      - 第一個 run（依 eps_as_of 由舊到新排序後的第一筆）：5 個點原封不動當
        序列起點——run 自己的 eps_as_of 這個點定義上就是 100，更早的四個點
        （90/60/30/7 天前）是這次 run 自己算出的相對水準，直接乘 100 沿用。
      - 之後每個 run 依序處理：
          1. 只加「日期晚於目前序列最後一個已存點日期」的點（同一天不重複
             記錄，舊 run 的點不會被新 run 覆寫）。
          2. 銜接錨點＝這個 run 自己 5 個點裡，日期 <= 目前序列最後已存點
             日期、且最接近的那一個（"closest to but not after"）。
          3. 找不到銜接錨點（代表這個 run 最早的點——90 天前——都還晚於目前
             序列最後已存點，兩者間隔 > GAP_SEGMENT_THRESHOLD_DAYS 天，見該
             常數）：斷點，另起一段（segment_id+1），這個 run 的 5 個點原封
             不動（自己的 100 基準）當新一段的起點，記一筆 segment_notes 說明
             原因；不嘗試把新舊兩段硬接在一起（沒有可信的銜接依據）。
          4. 找得到：chain-link——把這個 run 全部「新的」點（規則 1）乘上同一
             個比例常數，使銜接錨點那天的水準對齊「目前序列裡，日期 <= 銜接
             錨點日期、最接近的已存點」的水準（見 _value_on_or_before()）。

    回傳 (points, segment_notes)：
      points — [{"date","level","coverage_pct","segment_id"}, ...]，依日期由
               舊到新，segment_id 由 0 起算，同一個 segment_id 內部才是彼此
               可信的連續銜接。
      segment_notes — [{"segment_id","prev_date","new_eps_as_of","gap_days",
                        "reason"}, ...]——第一段（segment_id=0）不記 note。
    """
    if not runs:
        return [], []
    runs_sorted = sorted(runs, key=lambda r: r["eps_as_of"])

    first = runs_sorted[0]
    points: list[dict] = [
        {"date": p["date"], "level": p["level"], "coverage_pct": p.get("coverage_pct"), "segment_id": 0}
        for p in sorted(first.get("points") or [], key=lambda p: p["date"])
    ]
    segment_notes: list[dict] = []
    segment_id = 0
    last_stored_date = points[-1]["date"] if points else None

    def _start_new_segment(run_points: list[dict], reason: str, gap_days: int | None) -> None:
        nonlocal segment_id, last_stored_date
        segment_id += 1
        segment_notes.append({
            "segment_id": segment_id, "prev_date": last_stored_date,
            "new_eps_as_of": run.get("eps_as_of"), "gap_days": gap_days, "reason": reason,
        })
        for p in run_points:
            points.append({"date": p["date"], "level": p["level"], "coverage_pct": p.get("coverage_pct"),
                            "segment_id": segment_id})
        if run_points:
            last_stored_date = run_points[-1]["date"]

    for run in runs_sorted[1:]:
        run_points = sorted(run.get("points") or [], key=lambda p: p["date"])
        if not run_points:
            continue
        if last_stored_date is None:
            _start_new_segment(run_points, "序列目前是空的（第一個 run 沒有任何有效點），改用這個 run 當起點。", None)
            continue

        new_points = [p for p in run_points if p["date"] > last_stored_date]
        if not new_points:
            continue  # 這個 run 沒有任何比目前序列新的點（例如重跑同一段時間內的舊資料），略過

        anchor_candidates = [p for p in run_points if p["date"] <= last_stored_date and p.get("level") is not None]
        earliest_date = run_points[0]["date"]
        gap_days = (datetime.strptime(earliest_date, "%Y-%m-%d")
                    - datetime.strptime(last_stored_date, "%Y-%m-%d")).days

        if not anchor_candidates or gap_days > GAP_SEGMENT_THRESHOLD_DAYS:
            _start_new_segment(
                run_points,
                f"銜接錨點與上次存檔日期（{last_stored_date}）相距 {gap_days} 天，超過 "
                f"{GAP_SEGMENT_THRESHOLD_DAYS} 天門檻，視為斷點另起一段——這段改用自己的 eps_as_of "
                f"（{run.get('eps_as_of')}）重新當作 100 基準，不與前一段銜接比例。",
                gap_days,
            )
            continue

        anchor_pt = max(anchor_candidates, key=lambda p: p["date"])
        stored_ref = _value_on_or_before(points, anchor_pt["date"])
        if stored_ref is None or not stored_ref.get("level") or not anchor_pt.get("level"):
            # 理論上不會發生（anchor_candidates 已保證 anchor_pt 日期 <=
            # last_stored_date，points 至少有 last_stored_date 這筆）——防禦性
            # 處理，找不到可信的銜接基準時視同斷點，不要用 0／None 硬除。
            _start_new_segment(
                run_points,
                f"銜接錨點（{anchor_pt['date']}）或既有序列在該日期缺水準值，無法算出銜接比例，"
                "視為斷點另起一段。",
                gap_days,
            )
            continue

        scale = stored_ref["level"] / anchor_pt["level"]
        for p in new_points:
            points.append({
                "date": p["date"],
                "level": round(p["level"] * scale, 4) if p.get("level") is not None else None,
                "coverage_pct": p.get("coverage_pct"),
                "segment_id": segment_id,
            })
        last_stored_date = new_points[-1]["date"]

    return points, segment_notes


def build_display_points(points: list[dict]) -> list[dict]:
    """只取「最新一段」（most recent segment_id）——斷點之前的舊資料不接續
    畫進圖裡（沒有可信的銜接比例，硬接只會造成誤導的跳空），斷點本身在
    segment_notes 交代即可。取到的這段 rebase 成「這段第一個點＝100」，跟
    build_long_eps_index() 的 index=100-at-start_date 設計一致，這樣才能跟
    ETF 股價（同樣 rebase 到同一個起點＝100）疊在同一張圖上比較。"""
    if not points:
        return []
    last_seg = points[-1]["segment_id"]
    seg_points = [p for p in points if p["segment_id"] == last_seg]
    base_level = seg_points[0]["level"] if seg_points else None
    if not base_level:
        return []
    out = []
    for p in seg_points:
        level = p["level"]
        out.append({
            "date": p["date"],
            "level": round(level / base_level * 100, 4) if level is not None else None,
            "coverage_pct": p.get("coverage_pct"),
        })
    return out
