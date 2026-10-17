#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 data/tw_chips/*.jsonl 轉成 docs/tw-chips/data/*.json（欄式陣列、全部對齊同一條交易日曆）。

交易日曆 cal＝加權指數有收盤的日子（2016-10 起）；每個序列依 cal 對齊，沒有值的日子寫 null
（頁面畫成空點，不補假資料）。單位統一：金額＝億元新台幣、期貨選擇權＝口、融資融券＝張。

換算：
    TWSE BFI82U 金額單位＝元           → 億元：÷ 1e8
    TWSE MI_MARGN 融資金額單位＝仟元   → 億元：÷ 1e5
    TAIFEX 選擇權契約金額單位＝千元    → 億元：÷ 1e5
    FMTQIK 成交金額單位＝元            → 億元：÷ 1e8
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "tw_chips"
OUT = ROOT / "docs" / "tw-chips" / "data"
DISPLAY_START = "2016-10-01"
TZ_TAIPEI = dt.timezone(dt.timedelta(hours=8))


# ---------------------------------------------------------------- 純函式（有單元測試）

def yuan_to_yi(x):
    """元 → 億元（2 位小數）。"""
    return None if x is None else round(x / 1e8, 2)


def qianyuan_to_yi(x):
    """仟元／千元 → 億元（2 位小數）。1 仟元 = 1e3 元，1 億 = 1e8 元，故 ÷ 1e5。"""
    return None if x is None else round(x / 1e5, 2)


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


def rolling_sum(xs: list, n: int, nd: int = 2) -> list:
    out = []
    for i in range(len(xs)):
        w = xs[i - n + 1:i + 1] if i >= n - 1 else None
        out.append(None if w is None or any(v is None for v in w) else round(sum(w), nd))
    return out


def cumulate(xs: list, nd: int = 2) -> list:
    """累計：遇到缺值時該點為 None，之後接續累計（缺的日子不算 0 也不中斷總和）。"""
    out, tot = [], 0.0
    for v in xs:
        if v is None:
            out.append(None)
        else:
            tot += v
            out.append(round(tot, nd))
    return out


def ffill(xs: list, max_gap: int = 5) -> list:
    """往後補值，最多連補 max_gap 天（匯率用：美國休市日沿用前一營業日）。"""
    out, last, age = [], None, 0
    for v in xs:
        if v is not None:
            last, age = v, 0
            out.append(v)
        elif last is not None and age < max_gap:
            age += 1
            out.append(last)
        else:
            out.append(None)
    return out


def margin_final(cal: list[str], rows: dict[str, dict]) -> dict[str, dict]:
    """融資融券官方註明『以前日餘額為準』：下一個交易日的『前日餘額』才是前一天的定稿數字。
    若下一個交易日也有資料，就用它的 *_p 覆蓋前一天的 mg/sh/mga；沒有就保留當日『今日餘額』。"""
    out = {}
    for i, d in enumerate(cal):
        r = rows.get(d)
        if r is None:
            continue
        nxt = rows.get(cal[i + 1]) if i + 1 < len(cal) else None
        if nxt is not None:
            out[d] = {"d": d, "mg": nxt["mg_p"], "sh": nxt["sh_p"], "mga": nxt["mga_p"], "final": True}
        else:
            out[d] = {"d": d, "mg": r["mg"], "sh": r["sh"], "mga": r["mga"], "final": False}
    return out


def ratio_pct(a, b, nd: int = 2):
    """a / b × 100；b 為 0 或缺 → None。"""
    return None if a is None or not b else round(a / b * 100, nd)


# ---------------------------------------------------------------- 建檔

def dump(name: str, obj) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def main() -> int:
    taiex_all = load_jsonl("taiex")
    if not taiex_all:
        print("沒有 taiex 資料，無法建立日曆", file=sys.stderr)
        return 1
    all_days = sorted(taiex_all)
    closes_all = [taiex_all[d]["c"] for d in all_days]
    ma_all = {n: dict(zip(all_days, rolling_mean(closes_all, n))) for n in (20, 60, 240)}
    cal = [d for d in all_days if d >= DISPLAY_START]

    turn = load_jsonl("turnover")
    inst = load_jsonl("inst")
    margin = load_jsonl("margin")
    fut = load_jsonl("fut_inst")
    opt = load_jsonl("opt_inst")
    pcr = load_jsonl("pcr")
    large = load_jsonl("large")
    fx = load_jsonl("usdtwd")

    dump("cal.json", {"t": cal})

    # 1. 加權指數 + 成交金額 + 均線
    dump("price.json", {
        "o": align(cal, taiex_all, lambda r: r["o"]),
        "h": align(cal, taiex_all, lambda r: r["h"]),
        "l": align(cal, taiex_all, lambda r: r["l"]),
        "c": align(cal, taiex_all, lambda r: r["c"]),
        "amt": align(cal, turn, lambda r: yuan_to_yi(r["amt"])),
        "ma20": [ma_all[20].get(d) for d in cal],
        "ma60": [ma_all[60].get(d) for d in cal],
        "ma240": [ma_all[240].get(d) for d in cal],
    })

    # 2-3. 三大法人現貨買賣超（億元）、累計、外資 20 日合計
    net = {k: align(cal, inst, (lambda kk: lambda r: yuan_to_yi(r[kk][0] - r[kk][1]))(k)) for k in ("f", "t", "dl")}
    dump("inst.json", {
        "f": net["f"], "t": net["t"], "dl": net["dl"],
        "f_cum": cumulate(net["f"]), "t_cum": cumulate(net["t"]),
        "f_r20": rolling_sum(net["f"], 20),
    })

    # 4. 融資融券
    mfin = margin_final(cal, margin)
    mga = align(cal, mfin, lambda r: qianyuan_to_yi(r["mga"]))
    mg = align(cal, mfin, lambda r: r["mg"])
    sh = align(cal, mfin, lambda r: r["sh"])
    dump("margin.json", {
        "mga": mga,                                   # 融資餘額（億元）
        "mg": mg,                                     # 融資餘額（張）
        "sh": sh,                                     # 融券餘額（張）
        "ratio": [ratio_pct(s, m) for s, m in zip(sh, mg)],   # 券資比（%）＝融券張數 ÷ 融資張數
        "mga_chg": [None if i == 0 or mga[i] is None or mga[i - 1] is None else round(mga[i] - mga[i - 1], 2)
                    for i in range(len(cal))],
    })

    # 5. 臺股期貨三大法人未平倉淨口數
    def fnet(k):
        return align(cal, fut, lambda r: r[k][0] - r[k][1])
    dump("fut.json", {
        "f": fnet("f"), "t": fnet("t"), "dl": fnet("dl"),
        "f_lo": align(cal, fut, lambda r: r["f"][0]),
        "f_so": align(cal, fut, lambda r: r["f"][1]),
    })

    # 6. 臺指選擇權三大法人買權/賣權未平倉（淨口數、淨金額億元）
    o = {}
    for cp in ("c", "p"):
        for k in ("f", "t", "dl"):
            o[f"{cp}_{k}_n"] = align(cal, opt, (lambda a, b: lambda r: r[a][b][0] - r[a][b][1])(cp, k))
            o[f"{cp}_{k}_a"] = align(cal, opt, (lambda a, b: lambda r: qianyuan_to_yi(r[a][b][2] - r[a][b][3]))(cp, k))
    dump("opt.json", o)

    # 7. Put/Call Ratio（%）
    dump("pcr.json", {
        "vr": align(cal, pcr, lambda r: r["vr"]),
        "or": align(cal, pcr, lambda r: r["or"]),
    })

    # 8. 大額交易人（臺股期貨，全部月份）：買方減賣方
    dump("large.json", {
        "a5": align(cal, large, lambda r: r["a"][0] - r["a"][1]),
        "a10": align(cal, large, lambda r: r["a"][2] - r["a"][3]),
        "s5": align(cal, large, lambda r: r["s"][0] - r["s"][1]),
        "s10": align(cal, large, lambda r: r["s"][2] - r["s"][3]),
        "oi": align(cal, large, lambda r: r["oi"]),
    })

    # 9. 新台幣
    dump("fx.json", {"v": ffill(align(cal, fx, lambda r: r["v"]))})

    # 序列摘要（頁尾資料來源表用）
    def info(name, rows, label, unit, source):
        ds = sorted(d for d in rows if d >= DISPLAY_START)
        calset = set(cal)
        covered = [d for d in ds if d in calset]
        first = ds[0] if ds else None
        # 缺漏：該序列起訖範圍內、交易日曆上有、但序列沒有的日子
        gaps = [d for d in cal if first and d >= first and d <= (ds[-1] if ds else "") and d not in rows]
        return {"key": name, "label": label, "unit": unit, "source": source, "first": first,
                "last": ds[-1] if ds else None, "n": len(ds), "gaps": len(gaps)}

    series = [
        info("taiex", {d: r for d, r in taiex_all.items()}, "加權指數 OHLC", "點", "TWSE MI_5MINS_HIST"),
        info("turnover", turn, "成交金額", "億元", "TWSE FMTQIK"),
        info("inst", inst, "三大法人現貨買賣超", "億元", "TWSE BFI82U"),
        info("margin", margin, "融資融券餘額", "億元／張", "TWSE MI_MARGN"),
        info("fut_inst", fut, "臺股期貨三大法人未平倉", "口", "TAIFEX（2023-10 起）＋FinMind 轉載（2018-06 起）"),
        info("opt_inst", opt, "臺指選擇權三大法人未平倉", "口／億元", "TAIFEX（2023-10 起）＋FinMind 轉載（2018-06 起）"),
        info("pcr", pcr, "選擇權 Put/Call Ratio", "%", "TAIFEX pcRatio"),
        info("large", large, "大額交易人（臺股期貨）", "口", "TAIFEX largeTraderFut"),
        info("usdtwd", fx, "新台幣兌美元", "TWD/USD", "FRED DEXTAUS"),
    ]
    dump("meta.json", {
        "updated": dt.datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M"),
        "cal_first": cal[0], "cal_last": cal[-1], "n_cal": len(cal),
        "series": series,
    })
    print(f"built：日曆 {cal[0]}～{cal[-1]}（{len(cal)} 日）")
    for s in series:
        print(f"  {s['key']:9s} n={s['n']:5d} {s['first']}～{s['last']} gaps={s['gaps']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
