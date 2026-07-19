#!/usr/bin/env python3
"""PM 出場閉環 L1 — detective→pm 串接（build_pm_flags.py）.

把「市場偵探」當日產出交叉持倉檔的 ticker：凡系統組合裡的持倉股
（index_sleeve 成分＋stock_sleeve 在席者）被 detective 任一警報命中
（每日異常訊號 latest.json signals ／ 週更 kill 指標 kill_watch.json）→
寫進 docs/pm/flags.json（accumulating，含 first_seen／last_seen／status），
供 position-thesis-monitor 週報與人眼快查。

比對是 token 級精確比對（ticker 需以完整 token 出現在訊號 key／label／fact
或 kill 條目 id／metric／threshold 文字中）。detective 目前多為總體/市場層訊號，
單一持倉股命中通常少見——命中數為 0 是誠實結果，機制照樣把帳記著。

Accumulating：舊命中若當日仍在→last_seen 更新為當日、status=active；
當日不再命中→status=cleared（保留 first_seen 與最後一次 last_seen）。
zero-churn：flags 陣列內容不變則不重寫。
輸出：docs/pm/flags.json。
Usage: python3 scripts/build_pm_flags.py
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOLDINGS = ROOT / "docs" / "pm" / "holdings.json"
DET_LATEST = ROOT / "docs" / "detective" / "data" / "latest.json"
KILL_WATCH = ROOT / "docs" / "detective" / "data" / "kill_watch.json"
OUT = ROOT / "docs" / "pm" / "flags.json"

SCHEMA_VERSION = "1.0"
_TOKEN = re.compile(r"[A-Z0-9]{2,6}")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _tokens(*parts) -> set:
    out = set()
    for p in parts:
        if isinstance(p, str):
            out |= set(_TOKEN.findall(p.upper()))
        elif isinstance(p, (list, tuple)):
            for x in p:
                if isinstance(x, str):
                    out |= set(_TOKEN.findall(x.upper()))
    return out


def _holding_tickers(holdings: dict) -> list:
    """持倉 ticker（不含挑戰者——挑戰者非持倉）。回傳 [(ticker, sleeve)]。"""
    rows = []
    for c in holdings.get("index_sleeve", {}).get("components", []):
        rows.append((c["ticker"], "index"))
    ss = holdings.get("stock_sleeve", {})
    for r in ss.get("core_seats", []) + ss.get("sat_seats", []):
        rows.append((r["ticker"], "stock"))
    # 去重、保序
    seen, uniq = set(), []
    for t, sl in rows:
        if t not in seen:
            seen.add(t)
            uniq.append((t, sl))
    return uniq


def _detective_hits(det: dict, ticker: str) -> list:
    hits = []
    for s in det.get("signals", []):
        toks = _tokens(s.get("key"), s.get("label"), s.get("fact"),
                       s.get("composite_members"))
        if ticker.upper() in toks:
            hits.append({
                "source": "detective_signal",
                "key": s.get("key"),
                "label": s.get("label"),
                "fact": s.get("fact"),
                "sev": s.get("sev"),
                "cat": s.get("cat"),
            })
    return hits


def _kill_hits(kw: dict, ticker: str) -> list:
    hits = []
    for it in kw.get("items", []):
        toks = _tokens(it.get("id"), it.get("doc"), it.get("metric_text"),
                       it.get("threshold_text"), it.get("theme"))
        if ticker.upper() in toks:
            hits.append({
                "source": "kill_watch",
                "key": it.get("id"),
                "label": it.get("metric_text"),
                "fact": it.get("threshold_text"),
                "sev": it.get("status"),
                "cat": it.get("theme"),
            })
    return hits


def build() -> dict:
    holdings = _load(HOLDINGS)
    try:
        det = _load(DET_LATEST)
    except (OSError, json.JSONDecodeError):
        det = {}
    try:
        kw = _load(KILL_WATCH)
    except (OSError, json.JSONDecodeError):
        kw = {}

    det_as_of = det.get("as_of")
    kw_as_of = kw.get("as_of")
    as_of = det_as_of or kw_as_of

    tickers = _holding_tickers(holdings)
    sleeve_of = dict(tickers)

    # 當日命中
    today_hits = {}   # (ticker, source, key) → hit dict
    for t, _sl in tickers:
        for h in _detective_hits(det, t) + _kill_hits(kw, t):
            today_hits[(t, h["source"], h["key"])] = h

    # 讀舊帳（accumulating）
    prior = {}
    if OUT.exists():
        try:
            for f in _load(OUT).get("flags", []):
                prior[(f["ticker"], f["source"], f["key"])] = f
        except (OSError, json.JSONDecodeError):
            pass

    flags = []
    keys = set(prior) | set(today_hits)
    for k in keys:
        t, source, key = k
        h = today_hits.get(k)
        old = prior.get(k)
        seen_date = as_of if source == "detective_signal" else (kw_as_of or as_of)
        if h:   # 今天命中
            first = old["first_seen"] if old else seen_date
            flags.append({
                "ticker": t,
                "sleeve": sleeve_of.get(t, old["sleeve"] if old else "?"),
                "source": source,
                "key": key,
                "label": h.get("label"),
                "fact": h.get("fact"),
                "sev": h.get("sev"),
                "cat": h.get("cat"),
                "first_seen": first,
                "last_seen": seen_date,
                "status": "active",
            })
        else:   # 舊命中，今天不再命中 → cleared（不動 first/last_seen）
            f = dict(old)
            f["status"] = "cleared"
            flags.append(f)

    flags.sort(key=lambda f: (f["status"] != "active", f["ticker"],
                              f["source"], f["key"] or ""))

    active = sum(1 for f in flags if f["status"] == "active")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": as_of,
        "detective_as_of": det_as_of,
        "kill_watch_as_of": kw_as_of,
        "holdings_as_of": holdings.get("as_of"),
        "summary": {
            "holdings_scanned": len(tickers),
            "active": active,
            "cleared": len(flags) - active,
        },
        "flags": flags,
    }
    return payload


def _stable(payload: dict) -> str:
    """只比較 flags 陣列（zero-churn）——空命中且無狀態轉移則不重寫。"""
    return json.dumps(payload.get("flags", []), ensure_ascii=False, sort_keys=True)


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        try:
            if _stable(_load(OUT)) == _stable(payload):
                print(f"pm-flags: no change ({OUT.relative_to(ROOT)})")
                return
        except (OSError, json.JSONDecodeError):
            pass
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    s = payload["summary"]
    print(f"pm-flags: wrote {OUT.relative_to(ROOT)} · as_of {payload['as_of']}")
    print(f"  掃描持倉 {s['holdings_scanned']} 檔 · 命中 active {s['active']} · cleared {s['cleared']}")
    for f in payload["flags"]:
        if f["status"] == "active":
            print(f"  ⚑ {f['ticker']} ← {f['source']}:{f['key']}")


if __name__ == "__main__":
    main()
