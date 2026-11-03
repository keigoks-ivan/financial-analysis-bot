#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 data/us_chips/*.jsonl 轉成 docs/us-chips/data/{spy,qqq,sox}.json（欄式陣列、對齊同一條交易日曆）與 csv/。

交易日曆 cal＝S&P 500 指數有收盤的日子（1990-01-02 起）。每個序列依 cal 對齊，沒有值的日子寫 null
（頁面畫成空點，不補假資料）。週、半月、月頻序列只在『資料日所在的交易日』有值：
    CFTC 週資料   → 調查日（週二）
    FINRA 放空餘額 → 結算日（每月 15 日與月底前後）
    週淨申購（槓桿 ETF）→ 該週最後一個交易日（週一為週標籤）
ETF 申購贖回與全市場融資餘額不在這裡產生：頁面直接讀 etf-dash 與 fear-greed 已有的檔案。
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import sys
from bisect import bisect_right
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "us_chips"
OUT = ROOT / "docs" / "us-chips" / "data"
CSV_OUT = SRC / "csv"
CROWD_LEV = ROOT / "data" / "crowding_monitor" / "leveraged_etf_flows_weekly.csv"
ETF_DASH_FLOWS = ROOT / "data" / "etf_dash" / "flows"
TZ_TAIPEI = dt.timezone(dt.timedelta(hours=8))
FLOW_START = "2016-11-07"     # 槓桿 ETF 週淨申購統一自此起（和 etf-dash 的週序列同起點）

TABS = {
    "spy": {"label": "SPY（S&P 500）", "idx": "spx", "etfs": ["SPY"], "cot": "spx", "lev": [("3 倍", "UPRO", "SPXU"), ("2 倍", "SSO", "SDS")], "vol": "vix"},
    "qqq": {"label": "QQQ（Nasdaq-100）", "idx": "ndx", "etfs": ["QQQ"], "cot": "ndx", "lev": [("3 倍", "TQQQ", "SQQQ")], "vol": "vxn"},
    "sox": {"label": "費半（SOX）", "idx": "sox", "etfs": ["SOXX", "SMH"], "cot": None, "lev": [("3 倍", "SOXL", "SOXS")], "vol": None},
}
PROSHARES = ("UPRO", "SPXU", "SSO", "SDS")


# ---------------------------------------------------------------- 讀檔

def load(name: str, key: str = "d") -> dict:
    p = SRC / f"{name}.jsonl"
    rows: dict = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                rows[r[key]] = r
    return rows


def place(cal: list[str], d: str):
    i = bisect_right(cal, d) - 1
    return i if i >= 0 else None


def daily(cal_idx: dict, n: int, rows: dict, fn, nd: int | None = None) -> list:
    out = [None] * n
    for d, r in rows.items():
        i = cal_idx.get(d)
        if i is not None:
            v = fn(r)
            out[i] = None if v is None else (round(v, nd) if nd is not None else v)
    return out


def spread(cal: list[str], n: int, pairs, nd: int | None = None) -> list:
    out = [None] * n
    for d, v in pairs:
        i = place(cal, d)
        if i is not None and v is not None:
            out[i] = round(v, nd) if nd is not None else v
    return out


def rolling_ratio(rows_sorted: list[tuple[str, float, float]], w: int, nd: int = 4) -> dict:
    """rows_sorted: [(date, 分子, 分母)]。回傳 {date: 近 w 筆分子合計 ÷ 分母合計}，不足 w 筆不給。"""
    out = {}
    for i in range(w - 1, len(rows_sorted)):
        win = rows_sorted[i - w + 1:i + 1]
        den = sum(x[2] for x in win)
        if den:
            out[rows_sorted[i][0]] = round(sum(x[1] for x in win) / den, nd)
    return out


def rolling_mean_daily(rows_sorted: list[tuple[str, float]], w: int, nd: int = 4) -> dict:
    out = {}
    for i in range(w - 1, len(rows_sorted)):
        win = [x[1] for x in rows_sorted[i - w + 1:i + 1]]
        out[rows_sorted[i][0]] = round(sum(win) / w, nd)
    return out


# ---------------------------------------------------------------- 週淨申購（槓桿 ETF）

def monday(d: str) -> str:
    x = dt.date.fromisoformat(d)
    return (x - dt.timedelta(days=x.weekday())).isoformat()


def proshares_weekly(tk: str) -> dict[str, float]:
    """逐日份額變化 × 當日淨值，併成週（週一起算），百萬美元；口徑同 scripts/crowding/build_dash.py。"""
    rows = sorted(load(f"lev_{tk}").values(), key=lambda r: r["d"])
    wk: dict[str, float] = {}
    for a, b in zip(rows, rows[1:]):
        wk[monday(b["d"])] = wk.get(monday(b["d"]), 0.0) + (b["sh"] - a["sh"]) * b["nav"] / 1e6
    return {k: round(v, 2) for k, v in wk.items() if k >= FLOW_START}


def crowding_weekly() -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    if CROWD_LEV.exists():
        with CROWD_LEV.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                try:
                    out.setdefault(r["etf"], {})[r["week"]] = float(r["flow_usd_m"])
                except (KeyError, ValueError):
                    continue
    return out


def lev_weekly_all() -> dict[str, dict[str, float]]:
    cw = crowding_weekly()
    res = {}
    for tk in ("TQQQ", "SQQQ", "SOXL", "SOXS"):
        res[tk] = {k: v for k, v in cw.get(tk, {}).items() if k >= FLOW_START}
    for tk in PROSHARES:
        res[tk] = proshares_weekly(tk)
    return res


# ---------------------------------------------------------------- 份額（放空餘額占份額）

def shares_series(sym: str) -> list[tuple[str, float]]:
    rows = {d: r["sh"] for d, r in load(f"shares_{sym}").items()}
    p = ETF_DASH_FLOWS / f"{sym}.jsonl"           # 發行商歷史抓不到時，退回 etf-dash 近 200 天
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r.get("shares_outstanding"):
                    rows.setdefault(r["date"][:10], r["shares_outstanding"])
    return sorted(rows.items())


def shares_at(ser: list[tuple[str, float]], d: str, max_gap: int = 10):
    ds = [x[0] for x in ser]
    i = bisect_right(ds, d) - 1
    if i < 0:
        return None
    if (dt.date.fromisoformat(d) - dt.date.fromisoformat(ds[i])).days > max_gap:
        return None
    return ser[i][1]


# ---------------------------------------------------------------- 各區塊

def cot_normalized(key: str) -> dict:
    """CFTC 在 2023-05-02 把 Consolidated 的契約單位從 $250（S&P）／$100（Nasdaq-100）改成 $50／$20，
    同一批部位的口數變成 5 倍。這裡把舊單位的口數全部乘上 (舊乘數 ÷ 最新乘數)，統一成最新單位（迷你契約約當口數）。"""
    rows = load(f"cot_{key}")
    if not rows:
        return rows
    cu_last = rows[max(rows)].get("cu")
    out = {}
    for d, r in rows.items():
        f = (r["cu"] / cu_last) if (r.get("cu") and cu_last) else 1
        out[d] = {k: (v * f if k != "d" and k != "cu" and v is not None else v) for k, v in r.items()}
        out[d] = {k: (int(round(v)) if isinstance(v, float) else v) for k, v in out[d].items()}
    return out


def block_cot(cal, n, key):
    rows = cot_normalized(key)
    if not rows:
        return None
    ci = {d: i for i, d in enumerate(cal)}

    def net(a):
        return lambda r: r[f"{a}_l"] - r[f"{a}_s"]

    def pct(a):
        return lambda r: (r[f"{a}_l"] - r[f"{a}_s"]) / r["oi"] * 100 if r["oi"] else None
    out = {"oi": spread(cal, n, [(d, r["oi"]) for d, r in rows.items()])}
    for a in ("dl", "am", "lv", "ot", "nr"):
        out[f"{a}_n"] = spread(cal, n, [(d, net(a)(r)) for d, r in rows.items()])
        out[f"{a}_p"] = spread(cal, n, [(d, pct(a)(r)) for d, r in rows.items()], 2)
    out["lv_l"] = spread(cal, n, [(d, r["lv_l"]) for d, r in rows.items()])
    out["lv_s"] = spread(cal, n, [(d, r["lv_s"]) for d, r in rows.items()])
    return out


def block_si(cal, n, syms):
    parts = []
    for s in syms:
        rows = load(f"si_{s}")
        sh = shares_series(s)
        parts.append((s, rows, sh))
    dates = sorted(set().union(*[set(r) for _, r, _ in parts]))
    # 只留每檔都有資料的結算日（費半兩檔合計不能一檔缺值）
    dates = [d for d in dates if all(d in r for _, r, _ in parts)]

    def comb(d):
        short = sum(r[d]["short"] for _, r, _ in parts)
        adv = sum(r[d]["adv"] for _, r, _ in parts)
        shs = [shares_at(sh, d) for _, _, sh in parts]
        ratio = None if any(x is None for x in shs) else short / sum(shs) * 100
        return short, (short / adv if adv else None), ratio

    out = {
        "short": spread(cal, n, [(d, comb(d)[0]) for d in dates]),
        "dtc": spread(cal, n, [(d, comb(d)[1]) for d in dates], 2),
        "ratio": spread(cal, n, [(d, comb(d)[2]) for d in dates], 3),
        "parts": [],
    }
    if len(parts) > 1:
        for s, rows, sh in parts:
            pr = []
            for d in dates:
                x = shares_at(sh, d)
                pr.append((d, None if x is None else rows[d]["short"] / x * 100))
            out["parts"].append({"name": s, "short": spread(cal, n, [(d, rows[d]["short"]) for d in dates]),
                                 "ratio": spread(cal, n, pr, 3),
                                 "dtc": spread(cal, n, [(d, rows[d]["dtc"]) for d in dates], 2)})
    return out


def block_svol(cal, n, syms):
    ci = {d: i for i, d in enumerate(cal)}
    per = [load(f"svol_{s}") for s in syms]
    dates = sorted(set.intersection(*[set(p) for p in per])) if per else []
    sv = {d: sum(p[d]["sv"] for p in per) for d in dates}
    tv = {d: sum(p[d]["tv"] for p in per) for d in dates}
    ratio_rows = [(d, sv[d] / tv[d] * 100) for d in dates if tv[d]]
    return {
        "ratio": daily(ci, n, dict(ratio_rows), lambda v: v, 2),
        "r20": daily(ci, n, rolling_mean_daily(ratio_rows, 20, 2), lambda v: v),
        "tv": daily(ci, n, tv, lambda v: v, 0),
    }


def block_occ(cal, n, syms):
    ci = {d: i for i, d in enumerate(cal)}
    per = [load(f"occ_{s}") for s in syms]
    dates = sorted(set.intersection(*[set(p) for p in per])) if per else []
    agg = {d: {k: sum(p[d][k] for p in per) for k in ("c_c", "c_p", "f_c", "f_p", "m_c", "m_p")} for d in dates}
    pc = [(d, a["c_p"] / a["c_c"]) for d, a in agg.items() if a["c_c"]]
    roll = rolling_ratio([(d, agg[d]["c_p"], agg[d]["c_c"]) for d in dates], 20, 3)
    return {
        "pc": daily(ci, n, dict(pc), lambda v: v, 3),
        "pc20": daily(ci, n, roll, lambda v: v),
        "cust": daily(ci, n, agg, lambda a: a["c_c"] + a["c_p"]),
        "firm": daily(ci, n, agg, lambda a: a["f_c"] + a["f_p"]),
        "mm": daily(ci, n, agg, lambda a: a["m_c"] + a["m_p"]),
        "cust_call": daily(ci, n, agg, lambda a: a["c_c"]),
        "cust_put": daily(ci, n, agg, lambda a: a["c_p"]),
    }


def block_pcr(cal, n):
    ci = {d: i for i, d in enumerate(cal)}
    rows = {d: r for d, r in load("pcr").items() if (r.get("calls") or 0) + (r.get("puts") or 0) >= 100000}   # 排除休市日的空檔列（如 2025-01-09 國殤日）
    tot = [(d, r["total"]) for d, r in sorted(rows.items()) if r.get("total") is not None]
    return {
        "total": daily(ci, n, rows, lambda r: r.get("total")),
        "total20": daily(ci, n, rolling_mean_daily(tot, 20, 3), lambda v: v),
        "index": daily(ci, n, rows, lambda r: r.get("index")),
        "etp": daily(ci, n, rows, lambda r: r.get("etp")),
        "equity": daily(ci, n, rows, lambda r: r.get("equity")),
    }


def block_lev(cal, n, pairs, weekly):
    out = []
    for name, bull, bear in pairs:
        item = {"name": name, "bull": bull, "bear": bear}
        for side, tk in (("bull_w", bull), ("bear_w", bear)):
            item[side] = spread(cal, n, [(dt.date.fromisoformat(w).__add__(dt.timedelta(days=4)).isoformat(), v) for w, v in weekly[tk].items()], 2)
        out.append(item)
    return out


def load_insider() -> dict:
    """data/us_chips/insider/{季}.jsonl → {(代號, 月): [買進人數, 賣出人數, 買進金額, 賣出金額]}，各季相加
    （同一個月的交易會出現在多個季度檔：晚申報的那幾筆落在之後的季度）。"""
    tot: dict = {}
    files = sorted((SRC / "insider").glob("*.jsonl"))
    if not files:
        return tot
    last_q = files[-1].stem                         # 例 2026q3：交易日期晚於該季季末的列是申報時打錯日期，不收
    hi = f"{last_q[:4]}-{int(last_q[5]) * 3:02d}"
    for p in files:
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if not ("2009-01" <= r["m"] <= hi):
                    continue
                a = tot.setdefault((r["t"], r["m"]), [0, 0, 0.0, 0.0])
                a[0] += r["nb"]; a[1] += r["ns"]; a[2] += r["buy"]; a[3] += r["sell"]
    return tot


def block_ins(cal, n, tickers: set, tot: dict):
    months: dict = {}
    for (t, m), v in tot.items():
        if t in tickers:
            a = months.setdefault(m, [0, 0, 0.0, 0.0])
            for i in range(4):
                a[i] += v[i]
    if not months:
        return None

    def end(m):
        y, mo = int(m[:4]), int(m[5:])
        return (dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1)).isoformat()
    ms = sorted(months)
    return {
        "nb": spread(cal, n, [(end(m), months[m][0]) for m in ms]),
        "ns": spread(cal, n, [(end(m), months[m][1]) for m in ms]),
        "net": spread(cal, n, [(end(m), (months[m][2] - months[m][3]) / 1e6) for m in ms], 2),
        "buy": spread(cal, n, [(end(m), months[m][2] / 1e6) for m in ms], 2),
        "sell": spread(cal, n, [(end(m), months[m][3] / 1e6) for m in ms], 2),
        "n_tickers": len(tickers),
    }


# ---------------------------------------------------------------- CSV

CSV_COLS = {
    "idx": {"spx": "sp500_close", "ndx": "nasdaq100_close", "sox": "sox_close"},
    "cot": {"cu": "contract_multiplier_usd_per_index_point", "oi": "open_interest", "dl_l": "dealer_long", "dl_s": "dealer_short", "dl_sp": "dealer_spreading",
            "am_l": "asset_manager_long", "am_s": "asset_manager_short", "am_sp": "asset_manager_spreading",
            "lv_l": "leveraged_funds_long", "lv_s": "leveraged_funds_short", "lv_sp": "leveraged_funds_spreading",
            "ot_l": "other_reportable_long", "ot_s": "other_reportable_short", "ot_sp": "other_reportable_spreading",
            "nr_l": "nonreportable_long", "nr_s": "nonreportable_short"},
    "si": {"short": "short_interest_shares", "prev": "previous_short_interest_shares",
           "adv": "average_daily_volume_shares", "dtc": "days_to_cover"},
    "svol": {"sv": "short_volume", "sxv": "short_exempt_volume", "tv": "total_volume"},
    "occ": {"c_c": "customer_call_contracts", "c_p": "customer_put_contracts", "f_c": "firm_call_contracts",
            "f_p": "firm_put_contracts", "m_c": "market_maker_call_contracts", "m_p": "market_maker_put_contracts"},
    "vix": {"v": "close"}, "vxn": {"v": "close"}, "skew": {"v": "skew_index"},
    "pcr": {"total": "put_call_ratio_total", "index": "put_call_ratio_index", "etp": "put_call_ratio_etp",
            "equity": "put_call_ratio_equity", "calls": "call_volume_all_products", "puts": "put_volume_all_products",
            "src": "source"},
    "shares": {"sh": "shares_outstanding", "nav": "nav_per_share"},
    "lev": {"sh": "shares_outstanding", "nav": "nav_per_share"},
}


def export_csv() -> dict:
    CSV_OUT.mkdir(parents=True, exist_ok=True)
    info = {}
    for p in sorted(SRC.glob("*.jsonl")):
        name = p.stem
        base = name.split("_")[0]
        cols = CSV_COLS.get(base)
        if not cols:
            continue
        rows = load(name)
        keys = list(cols)
        with (CSV_OUT / f"{name}.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date"] + [cols[k] for k in keys])
            for d in sorted(rows):
                w.writerow([d] + ["" if rows[d].get(k) is None else rows[d].get(k) for k in keys])
        info[name] = {"n": len(rows), "first": min(rows) if rows else None, "last": max(rows) if rows else None}
    # 槓桿 ETF 週淨申購（ProShares 自算）
    wk = {tk: proshares_weekly(tk) for tk in PROSHARES}
    with (CSV_OUT / "lev_weekly.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "etf", "net_creation_usd_million"])
        for tk, d in wk.items():
            for k in sorted(d):
                w.writerow([k, tk, d[k]])
    tot = load_insider()
    if tot:
        with (CSV_OUT / "insider_ticker_month.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date", "ticker", "buyer_count", "seller_count", "buy_amount_usd", "sell_amount_usd"])
            for (t, m), v in sorted(tot.items(), key=lambda kv: (kv[0][1], kv[0][0])):
                w.writerow([m + "-01", t, v[0], v[1], round(v[2], 2), round(v[3], 2)])
    return info


def dump(name: str, obj) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def main() -> int:
    idx = load("idx")
    cal = sorted(d for d, r in idx.items() if "spx" in r)
    n = len(cal)
    ci = {d: i for i, d in enumerate(cal)}
    weekly = lev_weekly_all()
    vols = {"vix": load("vix"), "vxn": load("vxn")}
    skew = load("skew")
    pcr = block_pcr(cal, n)
    ins_tot = load_insider()
    cons = json.loads((SRC / "constituents.json").read_text(encoding="utf-8"))["etfs"] if (SRC / "constituents.json").exists() else {}
    dump("cal.json", {"t": cal})
    for tab, cfg in TABS.items():
        etfs = cfg["etfs"]
        obj = {
            "tab": tab, "label": cfg["label"],
            "idx": {"k": cfg["idx"], "c": daily(ci, n, idx, lambda r, k=cfg["idx"]: r.get(k), 2)},
            "etfs": etfs,
            "cot": block_cot(cal, n, cfg["cot"]) if cfg["cot"] else None,
            "si": block_si(cal, n, etfs),
            "svol": block_svol(cal, n, etfs),
            "occ": block_occ(cal, n, etfs),
            "lev": block_lev(cal, n, cfg["lev"], weekly),
            "vol": ({"name": cfg["vol"].upper(), "v": daily(ci, n, vols[cfg["vol"]], lambda r: r["v"], 2)} if cfg["vol"] else None),
            "skew": daily(ci, n, skew, lambda r: r["v"], 2) if tab == "spy" else None,
            "pcr": pcr,
            "ins": block_ins(cal, n, set().union(*[set(cons.get(e, [])) for e in etfs]), ins_tot) if ins_tot else None,
        }
        dump(f"{tab}.json", obj)
    info = export_csv()
    now = dt.datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M")
    dump("meta.json", {"updated": now, "cal_first": cal[0], "cal_last": cal[-1], "n_cal": n, "series": info})
    print(f"build ok: cal {cal[0]}~{cal[-1]} ({n}), {len(info)} series")
    return 0


if __name__ == "__main__":
    sys.exit(main())
