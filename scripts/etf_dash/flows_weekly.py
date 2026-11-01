#!/usr/bin/env python3
"""flows_weekly.py — build_etf_dash.py 資金流章節的十年週序列（2026-11-01 加）。

來源：data/crowding_monitor/etf_flows_weekly.csv（50 檔，週一為週標籤）。2016-11 起的歷史由
TradingView 的 ETF 資金流欄一次匯出（source=tradingview）；之後的週由
scripts/crowding/build_dash.py 用發行商每日流通單位數×淨值併成（source=issuer）。
那支程式是週檔唯一的寫入者，這裡只讀。flow_usd_m 欄名沿用舊名，實際單位是「百萬 × currency 欄
的幣別」：0050 台幣、TOPIX 日圓、其餘美元。

補尾：週檔最後一週之後，etf-dash 自己的每日檔（data/etf_dash/flows/{ETF}.jsonl）若已經有新的
日子，照同一個口徑（週一起算、前後兩天份額來源相同才算、只用發行商逐日歷史）併成補尾的週，
只放進頁面 JSON，不寫回 CSV。那週還沒到週五就標 partial，統計數字不算它。

統計口徑照 scripts/crowding/build_dash.py 的 weekly_stats()／build_lev()：近四週合計在整段歷史
四週滾動合計裡的分位（含等於，0～100，一位小數）。
"""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
WEEKLY_CSV = ROOT / "data" / "crowding_monitor" / "etf_flows_weekly.csv"
# 要跟 scripts/crowding/build_dash.py 的 WEEKLY_MERGE_SOURCES 一致：yfinance 快照的流通單位數常停在
# 同一個數字好幾天，拿來併週會跟 TradingView 差到數倍，所以只用發行商逐日歷史。
TAIL_SOURCES = {"ssga_navhist", "vaneck_navhist_derived"}
MIN_WEEKS = 20
CURRENCY_ZH = {"USD": "美元", "TWD": "台幣", "JPY": "日圓"}


def load_weekly_csv(path: Path = WEEKLY_CSV) -> dict:
    """{etf: {"currency": str, "rows": [(週一, 流量百萬), …]}}，整份 CSV 只讀一次。"""
    out: dict = {}
    if not path.exists():
        return out
    with path.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            try:
                t, wk, fl = r["etf"], r["week"], float(r["flow_usd_m"])
            except (KeyError, ValueError, TypeError):
                continue
            e = out.setdefault(t, {"currency": (r.get("currency") or "USD").strip() or "USD", "rows": {}})
            e["rows"][wk] = fl
    for e in out.values():
        e["rows"] = sorted(e["rows"].items())
    return out


def pctile(values, x):
    """x 在 values 裡的百分位（含等於，0～100），同 crowding/build_dash.py。"""
    vs = [v for v in values if v is not None]
    if not vs or x is None:
        return None
    return round(100.0 * sum(1 for v in vs if v <= x) / len(vs), 1)


def _monday(d: str) -> str:
    wd = date.fromisoformat(d[:10])
    return (wd - timedelta(days=wd.weekday())).isoformat()


def tail_weeks(rows: list[dict], after_week: str) -> list[dict]:
    """rows＝flows.load_rows() 的每日紀錄。回傳 after_week 之後的週：
    [{"week", "flow_m", "last_date", "partial"}]。前後兩天份額來源不同、或來源不是發行商逐日歷史的
    那一天不算；一週裡沒有任何一天能算就不產生那一週。"""
    valid = sorted((r for r in rows if r.get("shares_outstanding") is not None and r.get("nav") is not None),
                   key=lambda r: r["date"])
    wk: dict[str, list] = {}
    for prev, cur in zip(valid, valid[1:]):
        src = cur.get("source") or ""
        if src not in TAIL_SOURCES or (prev.get("source") or "") != src:
            continue
        monday = _monday(cur["date"])
        if monday <= after_week:
            continue
        flow_m = (float(cur["shares_outstanding"]) - float(prev["shares_outstanding"])) * float(cur["nav"]) / 1e6
        e = wk.setdefault(monday, [0.0, cur["date"][:10]])
        e[0] += flow_m
        e[1] = max(e[1], cur["date"][:10])
    out = []
    for monday in sorted(wk):
        fl, last = wk[monday]
        friday = (date.fromisoformat(monday) + timedelta(days=4)).isoformat()
        out.append({"week": monday, "flow_m": round(fl, 2), "last_date": last, "partial": last < friday})
    return out


def build_flows_weekly(etf_key: str, index: dict, daily_rows: list[dict] | None = None) -> dict | None:
    """給 docs/etf-dash/data/{ETF}.json 的 chart.flows_weekly；週檔沒有這檔（TAIEX）回 None。"""
    e = index.get(etf_key)
    if not e or len(e["rows"]) < MIN_WEEKS:
        return None
    ser = [[w, round(v, 2)] for w, v in e["rows"]]
    tail = tail_weeks(daily_rows or [], ser[-1][0]) if daily_rows else []
    partial_week = None
    for t in tail:
        ser.append([t["week"], t["flow_m"]])
        if t["partial"]:
            partial_week = t["week"]  # 只可能是最後一週
    done = [x for x in ser if x[0] != partial_week]
    vals = [v for _, v in done]
    r4 = [sum(vals[i - 3:i + 1]) for i in range(3, len(vals))]
    f4, f13 = sum(vals[-4:]), sum(vals[-13:])
    mx, mn = max(r4), min(r4)
    mxi, mni = r4.index(mx) + 3, r4.index(mn) + 3
    year = done[-1][0][:4]
    ccy = e["currency"]
    return {
        "since": ser[0][0],
        "asof": done[-1][0],
        "currency": ccy,
        "unit_zh": "百萬" + CURRENCY_ZH.get(ccy, ccy),
        "series": ser,
        "tail_from": tail[0]["week"] if tail else None,
        "partial": partial_week is not None,
        "partial_week": partial_week,
        "partial_last_date": tail[-1]["last_date"] if partial_week else None,
        "stats": {
            "n_weeks": len(done),
            "flow_4w_m": round(f4, 1),
            "pct_4w_10y": pctile(r4, f4),
            "flow_13w_m": round(f13, 1),
            "ytd_m": round(sum(v for d, v in done if d.startswith(year)), 1),
            "ytd_year": year,
            "max_4w_m": round(mx, 1), "max_4w_week": done[mxi][0],
            "min_4w_m": round(mn, 1), "min_4w_week": done[mni][0],
            "yearly": sorted([y, round(sum(v for d, v in done if d.startswith(y)), 1)]
                             for y in {d[:4] for d, _ in done}),
        },
        "note_zh": ("2016 年 11 月起的週序列由 TradingView 匯出一次，之後由發行商每日資料併成；"
                    "分位是近四週合計在十年四週滾動值裡的位置。"),
    }
