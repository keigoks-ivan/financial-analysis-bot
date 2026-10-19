#!/usr/bin/env python3
"""pe_daily.py — 每日本益比紀錄（Exhibit 3 的備援線）。2026-10-19 加。

Exhibit 3「預估本益比走勢」靠 dd-screener 名單的每日 EPS 紀錄往回推；名單涵蓋
盈餘權重低於門檻時（XLE、XLB、TOPIX，以及 EWY／EWM／EWZ／IEV）build_pe_history()
不畫線。這支模組從上線日起，每次 build（FULL 與 PRICE 都要）把頁面當天算出的
加權預估本益比記一列到 data/etf_dash/pe_daily/{ETF}.csv，往後每天延長一點，
讓沒有推算線的基金也有一條自己累積的線。

CSV 欄位：date,pe,coverage_pct,mode
  date          ETF 收盤日（不是執行日）；同一天重跑覆蓋那一列，不重複
  pe            頁面上的加權預估本益比（harmonic mean）
  coverage_pct  本益比涵蓋率（占基金權重 %）
  mode          full／price
依日期排序。不做歷史回補。

只有 dd-screener 推算線被抑制（pe_history.series 為空）時才用這份紀錄當線；
有推算線的基金行為完全不變。
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PE_DAILY_DIR = ROOT / "data" / "etf_dash" / "pe_daily"
FIELDS = ["date", "pe", "coverage_pct", "mode"]

NOTE_ZH = ("這檔基金的成分股不在 dd-screener 名單，無法往回推算；改用本頁每天算出的加權預估本益比，"
           "{start} 起記錄，每天延長。每週重抓成分股 EPS 那天，線可能跳一下。")
NOTE_ZH_MONTHLY = ("這檔基金的成分股不在 dd-screener 名單，無法往回推算；改用本頁每天算出的加權預估本益比，"
                   "{start} 起記錄，每天延長。每月重抓成分股 EPS 那天，線可能跳一下。")


def _path(etf_key: str, base_dir: Path | None = None) -> Path:
    return (base_dir or PE_DAILY_DIR) / f"{etf_key}.csv"


def load(etf_key: str, base_dir: Path | None = None) -> list[dict]:
    p = _path(etf_key, base_dir)
    if not p.exists():
        return []
    out = []
    with p.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            try:
                out.append({"date": r["date"], "pe": float(r["pe"]),
                            "coverage_pct": float(r["coverage_pct"]) if r.get("coverage_pct") not in (None, "") else None,
                            "mode": r.get("mode") or ""})
            except (KeyError, ValueError):
                continue
    return out


def record(etf_key: str, date: str, pe: float | None, coverage_pct: float | None, mode: str,
           base_dir: Path | None = None) -> bool:
    """寫入（或覆蓋同日）一列，依日期排序後整檔重寫。pe 缺值或非正數不寫（回
    False）——不要讓一個壞值汙染這條線。"""
    if not date or pe is None or pe <= 0:
        return False
    rows = {r["date"]: r for r in load(etf_key, base_dir)}
    rows[date] = {"date": date, "pe": round(float(pe), 2),
                  "coverage_pct": round(float(coverage_pct), 2) if coverage_pct is not None else None,
                  "mode": mode}
    p = _path(etf_key, base_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(FIELDS)
        for d in sorted(rows):
            r = rows[d]
            w.writerow([r["date"], f"{r['pe']:.2f}",
                        "" if r["coverage_pct"] is None else f"{r['coverage_pct']:.2f}", r["mode"]])
    return True


def apply_fallback(data: dict, etf_key: str, base_dir: Path | None = None) -> dict:
    """build_fund() 回傳的 data 就地處理：(1) 記今天的本益比；(2) 若 Exhibit 3
    的推算線被抑制（series 為空），改用每日紀錄當線，並標 source。回傳
    chart.pe_history。"""
    ph = (data.get("chart") or {}).get("pe_history")
    if ph is None:
        return {}
    fpe = data.get("weighted_forward_pe") or {}
    price = data.get("price") or {}
    record(etf_key, price.get("date"), fpe.get("value"), fpe.get("coverage_pct"), data.get("mode") or "", base_dir)

    if ph.get("series"):
        ph.setdefault("source", "dd_backcast")
        return ph
    rows = load(etf_key, base_dir)
    if not rows:
        ph.setdefault("source", "none")
        return ph
    ph["source"] = "daily_record"
    ph["start_date"] = rows[0]["date"]
    ph["series"] = [{"date": r["date"], "pe": r["pe"], "coverage_pct": r["coverage_pct"]} for r in rows]
    ph["earnings_coverage_pct"] = rows[-1]["coverage_pct"]
    tpl = NOTE_ZH_MONTHLY if data.get("full_refresh") == "monthly" else NOTE_ZH
    ph["source_note_zh"] = tpl.format(start=rows[0]["date"])
    return ph
