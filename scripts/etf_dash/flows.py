#!/usr/bin/env python3
"""flows.py — 資金流 (creation/redemption flow) tracking for build_etf_dash.py.

flows = Δ(shares outstanding) × NAV — the standard ETF creation/redemption
flow proxy. Needs a daily shares-outstanding number per fund.

Source survey (2026-09-26, see report to task owner for the full per-fund
breakdown): issuer-side pages (SSGA fund-facts, Invesco fund overview, VanEck,
Yuanta, TWSE ETFortune) do not expose a plain, stable machine-readable
shares-outstanding endpoint we could find within this task's scope — several
either need a browser session or bury the number in a JS-rendered widget.
Instead we use **yfinance's quoteSummary `get_info()`**, which already
carries `sharesOutstanding` directly for most US-listed ETFs (confirmed
working for SPY/QQQ/RSP/SMH/XLF/XLE/XLV/XLI/XLY/XLP/XLB — see
SHARES_OUTSTANDING_DIRECT works). Where `sharesOutstanding` is null (SMH.L,
XLC, and both Asia funds 1475.T/0050.TW), we derive it as
`totalAssets / navPrice` (both present in the same `get_info()` payload) —
this is the textbook AUM/NAV shares-outstanding identity, not a new data
source, and is flagged `source="derived"` in the stored row and in the JSON
output so it's never silently presented as an issuer-reported figure.
TAIEX is an index, not a fund — it has no shares outstanding and is skipped
entirely by the caller (see build_etf_dash.py FUND_REGISTRY / build_fund()).

Storage: append-only JSONL, one row per calendar day per fund,
data/etf_dash/flows/{ETF}.jsonl:
    {"date": "YYYY-MM-DD", "shares_outstanding": 917782016, "nav": 767.4363,
     "nav_currency": "USD", "source": "direct"|"derived"}
Same idempotency convention as dd_eps_history.py / anchor_history.py — a
same-day rerun overwrites the last line, not appended twice. No backfill: the
task explicitly allows this ("otherwise it accumulates from today — say so on
the page") since none of the surveyed sources offer a free public history of
daily shares outstanding.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FLOWS_DIR = ROOT / "data" / "etf_dash" / "flows"


def _path(etf_key: str) -> Path:
    return FLOWS_DIR / f"{etf_key}.jsonl"


def load_rows(etf_key: str) -> list[dict]:
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
            print(f"[flows] WARNING skipping malformed line {i + 1} in {path}: {e}", file=sys.stderr)
    return out


def append_today(etf_key: str, row: dict) -> None:
    rows = load_rows(etf_key)
    if rows and rows[-1].get("date") == row.get("date"):
        rows[-1] = row
    else:
        rows.append(row)
    path = _path(etf_key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows),
        encoding="utf-8",
    )


def fetch_shares_snapshot(yf_module, yf_ticker: str) -> dict:
    """回傳 {"shares_outstanding", "nav", "nav_currency", "source", "reason"}；
    抓不到（get_info() 掛掉，或 sharesOutstanding／推算所需的
    totalAssets／navPrice 都缺）回傳 source=None，呼叫端不寫入這天的紀錄
    （跟既有 EPS 快取一樣：沒有真資料就不要用假資料蓋掉，缺這天就是缺這天，
    下游 Δshares 算法本來就能跳過缺值的日子——見 compute_flow_series()）。"""
    try:
        info = yf_module.Ticker(yf_ticker).get_info()
    except Exception as e:  # noqa: BLE001
        return {"shares_outstanding": None, "nav": None, "nav_currency": None,
                "source": None, "reason": f"get_info() failed: {e}"}
    so = info.get("sharesOutstanding")
    nav = info.get("navPrice")
    total_assets = info.get("totalAssets")
    currency = info.get("currency")
    source = None
    reason = None
    if so and nav:
        source = "direct"
    elif total_assets and nav:
        so = total_assets / nav
        source = "derived"
        reason = "sharesOutstanding 缺值，用 totalAssets/navPrice 推算（見本檔 module docstring）"
    else:
        reason = f"get_info() 缺 sharesOutstanding／navPrice／totalAssets（有的欄位：" \
                  f"nav={nav!r}, totalAssets={total_assets!r}）"
    return {
        "shares_outstanding": round(so) if so else None,
        "nav": round(float(nav), 6) if nav is not None else None,
        "nav_currency": str(currency).upper() if currency else None,
        "source": source,
        "reason": reason,
    }


def compute_flow_series(rows: list[dict]) -> dict:
    """純函式：把逐日 shares_outstanding／nav 紀錄轉成每日流量、週流量、累計
    流量。回傳：
      daily — [{"date","flow_shares","flow_amount","nav_currency"}, ...]
              （第一天沒有前一天可比，不產生 daily 紀錄；缺值的日子被跳過，
              下一筆有值的日子會跟「上一筆有值的日子」比，不是跟前一個曆
              日比，這樣缺資料的日子不會被錯誤地算成 0 流量）。
      weekly — 依 ISO 週彙總 daily 的 flow_shares 加總 × 週最後一天的 nav。
      cumulative_since_start — 從第一筆有值的日子累計到最新一筆的 flow_amount
              加總（不是「這檔基金自成立以來」的資金流——只是這份紀錄自己開
              始追蹤以來的累計，見 module docstring 的 no-backfill 說明）。
    """
    valid = [r for r in rows if r.get("shares_outstanding") is not None and r.get("nav") is not None]
    valid.sort(key=lambda r: r["date"])
    daily = []
    for prev, cur in zip(valid, valid[1:]):
        flow_shares = cur["shares_outstanding"] - prev["shares_outstanding"]
        flow_amount = flow_shares * cur["nav"]
        daily.append({
            "date": cur["date"], "flow_shares": flow_shares, "flow_amount": round(flow_amount, 2),
            "nav_currency": cur.get("nav_currency"),
        })

    weekly_map: dict[str, list[dict]] = {}
    for d in daily:
        # ISO 週（year, week）當 key——同一週的每日流量加總成一筆週流量。
        import datetime
        iso = datetime.date.fromisoformat(d["date"]).isocalendar()
        wk_key = f"{iso[0]}-W{iso[1]:02d}"
        weekly_map.setdefault(wk_key, []).append(d)
    weekly = []
    for wk_key in sorted(weekly_map.keys()):
        items = weekly_map[wk_key]
        weekly.append({
            "week": wk_key,
            "week_end_date": items[-1]["date"],
            "flow_shares": sum(i["flow_shares"] for i in items),
            "flow_amount": round(sum(i["flow_amount"] for i in items), 2),
            "n_days": len(items),
            "nav_currency": items[-1].get("nav_currency"),
        })

    cumulative_since_start = round(sum(d["flow_amount"] for d in daily), 2) if daily else None
    return {
        "n_snapshots": len(valid),
        "start_date": valid[0]["date"] if valid else None,
        "latest_date": valid[-1]["date"] if valid else None,
        "daily": daily,
        "weekly": weekly,
        "cumulative_since_start": cumulative_since_start,
        "nav_currency": valid[-1].get("nav_currency") if valid else None,
        "latest_source": valid[-1].get("source") if valid else None,
    }
