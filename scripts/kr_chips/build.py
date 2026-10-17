#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 data/kr_chips/*.jsonl 轉成 docs/kr-chips/data/*.json（欄式陣列、全部對齊同一條交易日曆）。

交易日曆 cal＝KOFIA KOSPI 有收盤的日子 ∪ Naver KOSPI 有 OHLC 的日子（2016-10 起）；每個序列依 cal 對齊，
沒有值的日子寫 null（頁面畫成空點，不補假資料）。單位統一：金額＝億韓元、股數＝股、比例＝%、指數＝點。

換算：
    KOFIA 金額單位＝百萬韓元   → 億韓元：÷ 100（1 億 = 1e8 元，1 百萬 = 1e6 元）
    Naver 買賣超單位＝億韓元   → 不換算
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "kr_chips"
OUT = ROOT / "docs" / "kr-chips" / "data"
CSV_OUT = ROOT / "data" / "kr_chips" / "csv"
DISPLAY_START = "2016-10-01"
TZ_TAIPEI = dt.timezone(dt.timedelta(hours=8))
BAN_START, BAN_END = "2023-11-06", "2025-03-30"      # 全面禁止放空期間（2025-03-31 起恢復）


# ---------------------------------------------------------------- 純函式（有單元測試）

def mil_to_eok(x):
    """百萬韓元 → 億韓元（2 位小數）。1 百萬 = 1e6，1 億 = 1e8，故 ÷ 100。"""
    return None if x is None else round(x / 100, 2) + 0.0     # + 0.0 去掉 -0.0


def load_jsonl(name: str) -> dict[str, dict]:
    p = SRC / f"{name}.jsonl"
    rows: dict[str, dict] = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                rows[r["d"]] = r
    return rows


def align(cal: list[str], rows: dict[str, dict], fn) -> list:
    """依交易日曆取值；該日沒有資料或 fn 回 None → None。"""
    out = []
    for d in cal:
        r = rows.get(d)
        out.append(fn(r) if r is not None else None)
    return out


def rolling_mean(xs: list, n: int, nd: int = 2) -> list:
    """簡單移動平均；視窗內有缺值或不足 n 筆 → None。"""
    out = []
    for i in range(len(xs)):
        w = xs[i - n + 1:i + 1] if i >= n - 1 else None
        out.append(None if w is None or any(v is None for v in w) else round(sum(w) / n, nd))
    return out


def ratio_pct(a, b, nd: int = 2):
    """a / b × 100；b 為 0 或缺 → None。"""
    return None if a is None or not b else round(a / b * 100, nd)


def ffill(xs: list, max_gap: int = 5) -> list:
    """往後補值，最多連補 max_gap 天（匯率用：美國休市日沿用前一營業日）。
    最後一筆真實資料之後不補（FRED 約晚一週更新，不能把舊值當成最新日）。"""
    last_real = max((i for i, v in enumerate(xs) if v is not None), default=-1)
    out, last, age = [], None, 0
    for i, v in enumerate(xs):
        if v is not None:
            last, age = v, 0
            out.append(v)
        elif last is not None and age < max_gap and i < last_real:
            age += 1
            out.append(last)
        else:
            out.append(None)
    return out


def total_mcap(k, q):
    """KOSPI＋KOSDAQ 上市總市值（百萬韓元）；任一缺 → None。"""
    return None if k is None or q is None else k + q


# ---------------------------------------------------------------- 回測用 CSV（扁平、一天一列、英文欄名）

def _csv_columns() -> dict:
    """series → [(欄名, 取值函式(row))]。欄名後綴即單位：_million_krw＝百萬韓元（KOFIA 原單位）、
    _100m_krw＝億韓元、_shares＝股、_pct＝百分比。第一欄一律是 date。"""
    cols = {}
    for s in ("kospi", "kosdaq"):
        cols[s] = [("close", lambda r: r["c"]), ("volume_shares", lambda r: r["vol"]),
                   ("turnover_million_krw", lambda r: r["amt"]), ("turnover_100m_krw", lambda r: mil_to_eok(r["amt"])),
                   ("market_cap_million_krw", lambda r: r["mcap"]), ("market_cap_100m_krw", lambda r: mil_to_eok(r["mcap"])),
                   ("foreign_holding_cap_million_krw", lambda r: r["fmcap"]),
                   ("foreign_holding_cap_100m_krw", lambda r: mil_to_eok(r["fmcap"])),
                   ("foreign_holding_pct", lambda r: r["fpct"])]
        cols["px_" + s] = [("open", lambda r: r["o"]), ("high", lambda r: r["h"]),
                           ("low", lambda r: r["l"]), ("close", lambda r: r["c"])]
        cols["inst_" + s] = [("individual_net_100m_krw", lambda r: r["p"]), ("foreign_net_100m_krw", lambda r: r["f"]),
                             ("institution_net_100m_krw", lambda r: r["i"])]
    cols["deposit"] = [("investor_deposit_million_krw", lambda r: r["dep"]),
                       ("investor_deposit_100m_krw", lambda r: mil_to_eok(r["dep"])),
                       ("unsettled_buy_million_krw", lambda r: r["unpaid"]),
                       ("unsettled_buy_100m_krw", lambda r: mil_to_eok(r["unpaid"])),
                       ("forced_liquidation_million_krw", lambda r: r["forced"]),
                       ("forced_liquidation_100m_krw", lambda r: mil_to_eok(r["forced"])),
                       ("forced_liquidation_pct_of_prev_unsettled", lambda r: r["forced_pct"]),
                       ("unverified_col3_million_krw", lambda r: r["x3"]),
                       ("unverified_col4_million_krw", lambda r: r["x4"])]
    cols["credit"] = [("margin_total_million_krw", lambda r: r["tot"]), ("margin_total_100m_krw", lambda r: mil_to_eok(r["tot"])),
                      ("margin_kospi_million_krw", lambda r: r["kospi"]), ("margin_kospi_100m_krw", lambda r: mil_to_eok(r["kospi"])),
                      ("margin_kosdaq_million_krw", lambda r: r["kosdaq"]), ("margin_kosdaq_100m_krw", lambda r: mil_to_eok(r["kosdaq"])),
                      ("short_loan_total_million_krw", lambda r: r["sh_tot"]),
                      ("short_loan_kospi_million_krw", lambda r: r["sh_kospi"]),
                      ("short_loan_kosdaq_million_krw", lambda r: r["sh_kosdaq"]),
                      ("unverified_col8_million_krw", lambda r: r["x8"]),
                      ("unverified_col9_million_krw", lambda r: r["x9"])]
    cols["lend"] = [("lending_new_shares", lambda r: r["new"]), ("lending_returned_shares", lambda r: r["ret"]),
                    ("lending_balance_shares", lambda r: r["bal"]),
                    ("lending_balance_million_krw", lambda r: r["bal_amt"]),
                    ("lending_balance_100m_krw", lambda r: mil_to_eok(r["bal_amt"]))]
    cols["usdkrw"] = [("usdkrw", lambda r: r["v"])]
    return cols


def export_csv() -> dict:
    """data/kr_chips/csv/{series}.csv：jsonl 全部歷史扁平化，一天一列。"""
    CSV_OUT.mkdir(parents=True, exist_ok=True)
    counts = {}
    for series, cols in _csv_columns().items():
        rows = load_jsonl(series)
        days = sorted(rows)
        with (CSV_OUT / f"{series}.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date"] + [n for n, _ in cols])
            for d in days:
                r = rows[d]
                w.writerow([d] + ["" if (v := fn(r)) is None else v for _, fn in cols])
        counts[series] = len(days)
    return counts


# ---------------------------------------------------------------- 建檔

def dump(name: str, obj) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def main() -> int:
    kospi, kosdaq = load_jsonl("kospi"), load_jsonl("kosdaq")
    pxk, pxq = load_jsonl("px_kospi"), load_jsonl("px_kosdaq")
    if not kospi and not pxk:
        print("沒有 KOSPI 資料，無法建立日曆", file=sys.stderr)
        return 1
    cal_all = sorted(set(kospi) | set(pxk))
    cal = [d for d in cal_all if d >= DISPLAY_START]

    dump("cal.json", {"t": cal, "ban": [1 if BAN_START <= d <= BAN_END else 0 for d in cal]})

    # 1-2. 指數 OHLC、成交金額、均線、外資持股
    def market(px, kf, pxname):
        # 均線用 Naver 收盤的全歷史算（1990 起），所以 2016-10 的 240 日均線已有值
        days_all = sorted(px)
        closes_all = [px[d]["c"] for d in days_all]
        ma = {n: dict(zip(days_all, rolling_mean(closes_all, n))) for n in (20, 60, 240)}
        return {
            "o": align(cal, px, lambda r: r["o"]), "h": align(cal, px, lambda r: r["h"]),
            "l": align(cal, px, lambda r: r["l"]), "c": align(cal, px, lambda r: r["c"]),
            "amt": align(cal, kf, lambda r: mil_to_eok(r["amt"])),
            "mcap": align(cal, kf, lambda r: mil_to_eok(r["mcap"])),
            "fcap": align(cal, kf, lambda r: mil_to_eok(r["fmcap"])),
            "fpct": align(cal, kf, lambda r: r["fpct"]),
            "ma20": [ma[20].get(d) for d in cal], "ma60": [ma[60].get(d) for d in cal],
            "ma240": [ma[240].get(d) for d in cal],
        }
    dump("kospi.json", market(pxk, kospi, "px_kospi"))
    dump("kosdaq.json", market(pxq, kosdaq, "px_kosdaq"))

    # 3-4. 投資人別買賣超（億韓元）
    ik, iq = load_jsonl("inst_kospi"), load_jsonl("inst_kosdaq")
    dump("inst.json", {
        "kp": align(cal, ik, lambda r: r["p"]), "kf": align(cal, ik, lambda r: r["f"]), "ki": align(cal, ik, lambda r: r["i"]),
        "qp": align(cal, iq, lambda r: r["p"]), "qf": align(cal, iq, lambda r: r["f"]), "qi": align(cal, iq, lambda r: r["i"]),
    })

    # 6. 投資人預託金、未收款、反向交易
    dep = load_jsonl("deposit")
    dump("deposit.json", {
        "dep": align(cal, dep, lambda r: mil_to_eok(r["dep"])),
        "unpaid": align(cal, dep, lambda r: mil_to_eok(r["unpaid"])),
        "forced": align(cal, dep, lambda r: mil_to_eok(r["forced"])),
        "forced_pct": align(cal, dep, lambda r: r["forced_pct"]),
    })

    # 7. 信用融資（分市場）與佔市值比
    cr = load_jsonl("credit")
    mc_k = align(cal, kospi, lambda r: r["mcap"])
    mc_q = align(cal, kosdaq, lambda r: r["mcap"])
    c_tot = align(cal, cr, lambda r: r["tot"])
    c_k = align(cal, cr, lambda r: r["kospi"])
    c_q = align(cal, cr, lambda r: r["kosdaq"])
    dump("credit.json", {
        "tot": [mil_to_eok(v) for v in c_tot], "kospi": [mil_to_eok(v) for v in c_k],
        "kosdaq": [mil_to_eok(v) for v in c_q],
        "r_tot": [ratio_pct(a, total_mcap(b, c), 3) for a, b, c in zip(c_tot, mc_k, mc_q)],
        "r_kospi": [ratio_pct(a, b, 3) for a, b in zip(c_k, mc_k)],
        "r_kosdaq": [ratio_pct(a, b, 3) for a, b in zip(c_q, mc_q)],
    })

    # 8. 借券餘額與佔總市值比
    ld = load_jsonl("lend")
    l_amt = align(cal, ld, lambda r: r["bal_amt"])
    dump("lend.json", {
        "amt": [mil_to_eok(v) for v in l_amt],
        "sh": align(cal, ld, lambda r: r["bal"]),
        "new": align(cal, ld, lambda r: r["new"]), "ret": align(cal, ld, lambda r: r["ret"]),
        "ratio": [ratio_pct(a, total_mcap(b, c), 3) for a, b, c in zip(l_amt, mc_k, mc_q)],
    })

    # 9. 韓元
    fx = load_jsonl("usdkrw")
    dump("fx.json", {"v": ffill(align(cal, fx, lambda r: r["v"]))})

    # 序列摘要（頁尾資料來源表用）
    def info(name, rows, label, unit, source, since=DISPLAY_START):
        ds = sorted(d for d in rows if d >= since)
        first = ds[0] if ds else None
        # 缺漏：該序列起訖範圍內、交易日曆上有、但序列沒有的日子
        gaps = [d for d in cal if first and d >= first and d <= ds[-1] and d not in rows]
        return {"key": name, "label": label, "unit": unit, "source": source,
                "first_all": min(rows) if rows else None, "first": first,
                "last": ds[-1] if ds else None, "n": len(ds), "n_all": len(rows), "gaps": len(gaps)}

    series = [
        info("px_kospi", pxk, "KOSPI 日 OHLC", "點", "Naver 行動版 API"),
        info("px_kosdaq", pxq, "KOSDAQ 日 OHLC", "點", "Naver 行動版 API"),
        info("kospi", kospi, "KOSPI 成交金額、上市總市值、外資持股", "億韓元／%", "KOFIA FreeSIS"),
        info("kosdaq", kosdaq, "KOSDAQ 成交金額、上市總市值、外資持股", "億韓元／%", "KOFIA FreeSIS"),
        info("inst_kospi", ik, "KOSPI 外國人、機構、個人買賣超", "億韓元", "Naver 行動版 API"),
        info("inst_kosdaq", iq, "KOSDAQ 外國人、機構、個人買賣超", "億韓元", "Naver 行動版 API"),
        info("deposit", dep, "投資人預託金、未收款、反向交易", "億韓元／%", "KOFIA FreeSIS"),
        info("credit", cr, "信用交易融資餘額", "億韓元", "KOFIA FreeSIS"),
        info("lend", ld, "借券餘額（全市場合計）", "億韓元／股", "KOFIA FreeSIS"),
        info("usdkrw", fx, "韓元兌美元", "KRW/USD", "FRED DEXKOUS"),
    ]
    dump("meta.json", {
        "updated": dt.datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M"),
        "cal_first": cal[0], "cal_last": cal[-1], "n_cal": len(cal),
        "ban": [BAN_START, BAN_END],
        "series": series,
    })
    n_csv = export_csv()
    print("csv：" + "、".join(f"{k} {v} 列" for k, v in n_csv.items()))
    print(f"built：日曆 {cal[0]}～{cal[-1]}（{len(cal)} 日）")
    for s in series:
        print(f"  {s['key']:12s} n={s['n']:5d}/{s['n_all']:5d} {s['first']}～{s['last']} gaps={s['gaps']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
