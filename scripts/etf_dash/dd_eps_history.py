#!/usr/bin/env python3
"""dd_eps_history.py — 從 docs/dd-screener/latest.json 的 git 歷史重建每日
「明年度 EPS 預估」時間序列，供 ETF 儀表板 Exhibit 2 的長線 EPS 指數用。

背景：dd-screener 的 latest.json 幾乎每個交易日都重新 commit 一次（109 個
不同日期，自 2026-05-15 起），但底層 EPS 預估（Koyfin Excel 來源）通常是
月頻更新——同一檔股票的 eps_fy_next 常常連續好幾週不變，價格與動能等其他
欄位才每天變。這正好給了 ETF 加權 EPS 指數一條遠比 yfinance eps_trend（只
記得 90 天）更長的歷史線。

兩段式資料源，刻意設計成 CI 友善（GitHub Actions checkout 預設 shallow
clone，沒有完整 git 歷史）：
  1. backfill_from_git()：只在本機（有完整 git log）跑一次，把既有 commit
     日期的 latest.json 逐一 `git show` 出來解析，寫進
     data/etf_dash/dd_eps_history.jsonl。之後只要這份檔案存在，就不用再碰
     git 歷史。
  2. append_today()：每次 build_etf_dash.py 執行都呼叫，只讀「目前 checkout
     出來的」docs/dd-screener/latest.json（不需要 git log／git show，shallow
     clone 也能跑），把當天這筆記錄併入檔案末端。同一天重跑只重寫最後一行
     （冪等，不重寫整份檔案）。

儲存格式：append-only JSONL，一行一天，每行：
    {"date": "YYYY-MM-DD", "sha": "...", "t": {"NVDA": [15.68, 21.06, null, null, "USD", "+1y"], ...}}
  "t" 的每個 ticker 是精簡陣列，順序固定＝FIELDS（見下），不是 dict——這是
  2026-09-24 從物件式 dict-of-dict 快取（單一 ~4MB 檔案、每天整檔重寫）改過
  來的：repo 是公開的，單檔每天整份重寫會讓 git 歷史迅速膨脹；append-only
  JSONL 讓正常的每日一行只增加幾十 KB，且只有「同一天重跑」才需要重寫最後
  一行（見 append_today() 的 in-place 邏輯），git diff 也只顯示真正新增/變動
  的那一行。全空值（六個欄位都是 null）的 ticker 直接不寫進該行，省空間。
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
JSONL_PATH = ROOT / "data" / "etf_dash" / "dd_eps_history.jsonl"
DD_SCREENER_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"

# 只留 build_long_eps_index() 用得到的欄位（見 build_etf_dash.py 的 rollover
# 偵測與 FX 正規化邏輯）。eps_fy_next/eps_fy3 是核心；*_usd_orig 與
# eps_display_currency 是 v1.8.5 起非美元報表股票改顯示本地幣別後，原始美元
# 基準值的落點（見 get_usd_value() 用法）；yf_fy_label 留著備查但目前 rollover
# 偵測改用 fy3→fy_next 連續性法（見 build_etf_dash.py 說明），不直接用這欄。
# 順序固定——JSONL 裡每個 ticker 存的是這個順序的精簡陣列，不是具名 dict。
FIELDS = [
    "eps_fy_next", "eps_fy3",
    "eps_fy_next_usd_orig", "eps_fy3_usd_orig",
    "eps_display_currency", "yf_fy_label",
]


def _array_to_record(arr: list) -> dict:
    return {f: (arr[i] if i < len(arr) else None) for i, f in enumerate(FIELDS)}


def _record_to_array(rec: dict) -> list:
    return [rec.get(f) for f in FIELDS]


def get_usd_value(day_ticker_rec: dict, field: str) -> float | None:
    """v1.8.5 起非美元報表的股票，{field} 本身可能已經被改顯示成本地幣別，
    原始美元值搬進 {field}_usd_orig；此前所有值都還是美元。一律優先取
    _usd_orig，沒有才退回原欄位——確保拿到的永遠是美元基準。"""
    usd_orig = day_ticker_rec.get(f"{field}_usd_orig")
    if usd_orig is not None:
        return float(usd_orig)
    v = day_ticker_rec.get(field)
    return float(v) if v is not None else None


def _extract_day_tickers(stocks: list[dict]) -> dict[str, list]:
    """每檔股票的六個欄位壓成精簡陣列；六個欄位都是 null 的 ticker 直接丟掉
    （「drop nulls-only tickers」），不占 JSONL 空間。"""
    out: dict[str, list] = {}
    for s in stocks:
        tk = s.get("ticker")
        if not tk:
            continue
        arr = _record_to_array(s)
        if all(v is None for v in arr):
            continue
        out[tk] = arr
    return out


# ---------------------------------------------------------------------------
# Reading the JSONL file
# ---------------------------------------------------------------------------


def _read_lines() -> list[dict]:
    """回傳檔案裡每一行解析後的 dict（{"date","sha","t"}），依檔案順序（理論上
    已經是日期由舊到新，因為只 append／改最後一行）。壞掉的行跳過並警告，
    不讓整份檔案因為一行壞資料而讀不出來。"""
    if not JSONL_PATH.exists():
        return []
    out = []
    for i, line in enumerate(JSONL_PATH.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError as e:
            print(f"[dd_eps_history] WARNING skipping malformed line {i+1} in {JSONL_PATH}: {e}", file=sys.stderr)
    return out


def load_days() -> dict:
    """把 JSONL 讀成 build_long_eps_index() 要的形狀：
    {"YYYY-MM-DD": {"sha": ..., "tickers": {"NVDA": {field: value, ...}, ...}}}
    精簡陣列在這裡展開回具名欄位，呼叫端（build_etf_dash.py）不需要知道
    底層存的是陣列還是 dict。"""
    days: dict[str, dict] = {}
    for row in _read_lines():
        date = row.get("date")
        if not date:
            continue
        tickers = {tk: _array_to_record(arr) for tk, arr in row.get("t", {}).items()}
        days[date] = {"sha": row.get("sha"), "tickers": tickers}
    return days


# ---------------------------------------------------------------------------
# One-time local backfill (needs full git history — not for CI)
# ---------------------------------------------------------------------------


def _last_commit_per_day() -> list[tuple[str, str]]:
    """回傳 [(date, sha), ...] 由舊到新，每個曆日只留當天最後一個 commit。
    `git log` 預設新到舊排列，同一天的 commit 會連續出現、且該天最新的排最
    前面——由上往下掃、每個新日期第一次出現時記錄，就是「當天最後一個
    commit」。"""
    out = subprocess.run(
        ["git", "log", "--follow", "--format=%H %ad", "--date=short", "--",
         "docs/dd-screener/latest.json"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    seen_dates: dict[str, str] = {}
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        sha, date = line.split(" ", 1)
        if date not in seen_dates:
            seen_dates[date] = sha
    return sorted(seen_dates.items())  # [(date, sha), ...] 由舊到新


def backfill_from_git() -> int:
    """一次性從本機完整 git 歷史重建，只補檔案裡還沒有的日期（冪等、可重跑），
    新的日期依時間順序 append 到 JSONL 末端。需要完整 git log（不能是 shallow
    clone）——CI 不跑這個，見模組頂端說明。回傳新增的天數。"""
    try:
        day_shas = _last_commit_per_day()
    except subprocess.CalledProcessError as e:
        print(f"[dd_eps_history] git log failed (shallow clone / not a git repo?): {e}", file=sys.stderr)
        return 0
    existing_dates = set(load_days().keys())
    added = 0
    JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JSONL_PATH.open("a", encoding="utf-8") as f:
        for date, sha in day_shas:
            if date in existing_dates:
                continue
            try:
                raw = subprocess.run(
                    ["git", "show", f"{sha}:docs/dd-screener/latest.json"],
                    cwd=ROOT, capture_output=True, text=True, check=True,
                ).stdout
                payload = json.loads(raw)
            except (subprocess.CalledProcessError, ValueError) as e:
                print(f"[dd_eps_history] WARNING skip {date} ({sha[:8]}): {e}", file=sys.stderr)
                continue
            tickers = _extract_day_tickers(payload.get("stocks", []))
            if not tickers:
                continue
            f.write(json.dumps({"date": date, "sha": sha, "t": tickers}, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
            added += 1
    return added


# ---------------------------------------------------------------------------
# Cheap daily append (no git needed — CI-safe even on a shallow checkout)
# ---------------------------------------------------------------------------


def append_today(latest_json_path: Path | None = None, date_str: str | None = None, sha: str | None = None) -> bool:
    """把目前 checkout 出來的 docs/dd-screener/latest.json 併入「今天」這一行。
    不呼叫任何 git 指令，shallow clone 也能跑。

    - 今天還沒有記錄：append 一行到檔案末端。
    - 今天已經有記錄（同一天重跑，latest.json 內容可能變了）：只重寫最後一行
      （讀出既有內容、把最後一行換掉、整檔寫回——JSONL 沒有真正的「原地改某
      一行」，但效果等同「只有最後一行變動」，其餘行 byte-for-byte 不變）。
    - 其他天的既有記錄一律不動。

    回傳是否有寫入（latest.json 不存在/解析失敗/沒有任何 ticker 資料時回
    False，檔案不變）。"""
    path = latest_json_path or DD_SCREENER_LATEST
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"[dd_eps_history] WARNING could not read {path}: {e}", file=sys.stderr)
        return False
    date = date_str or datetime.now().strftime("%Y-%m-%d")
    tickers = _extract_day_tickers(payload.get("stocks", []))
    if not tickers:
        return False
    new_row = {"date": date, "sha": sha, "t": tickers}
    new_line = json.dumps(new_row, ensure_ascii=False, separators=(",", ":"))

    rows = _read_lines()
    if rows and rows[-1].get("date") == date:
        rows[-1] = new_row  # 同一天重跑：只換最後一行
        JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSONL_PATH.write_text(
            "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows),
            encoding="utf-8",
        )
    else:
        JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
        with JSONL_PATH.open("a", encoding="utf-8") as f:
            f.write(new_line + "\n")
    return True


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--backfill", action="store_true", help="一次性從本機完整 git 歷史補齊")
    ap.add_argument("--append-today", action="store_true", help="把目前 checkout 的 latest.json 併入今天這一行")
    args = ap.parse_args()
    if args.backfill:
        n = backfill_from_git()
        print(f"[dd_eps_history] backfilled {n} new day(s)")
    if args.append_today:
        ok = append_today()
        print(f"[dd_eps_history] append_today: {'wrote' if ok else 'no-op'}")
    if not args.backfill and not args.append_today:
        days = load_days()
        print(f"[dd_eps_history] {JSONL_PATH} has {len(days)} day(s); pass --backfill or --append-today")
    if JSONL_PATH.exists():
        print(f"[dd_eps_history] {JSONL_PATH}: {len(load_days())} day(s), "
              f"{JSONL_PATH.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
