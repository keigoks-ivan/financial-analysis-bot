#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 data/tw_chips/*.jsonl 轉成 docs/tw-chips/data/*.json（欄式陣列、全部對齊同一條交易日曆）。

交易日曆 cal＝加權指數有收盤的日子（2016-10 起）；每個序列依 cal 對齊，沒有值的日子寫 null
（頁面畫成空點，不補假資料）。單位統一：金額＝億元新台幣、期貨選擇權＝口、融資融券＝張。

換算：
    TWSE BFI82U 金額單位＝元           → 億元：÷ 1e8
    TWSE MI_MARGN 融資金額單位＝仟元   → 億元：÷ 1e5
    TWSE 借券（TWT72U／TWT93U 換算）金額單位＝元 → 億元：÷ 1e8
    TWSE 市值週報總市值單位＝億元（不換算）
    TAIFEX 選擇權契約金額單位＝千元    → 億元：÷ 1e5
    FMTQIK 成交金額單位＝元            → 億元：÷ 1e8
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "tw_chips"
OUT = ROOT / "docs" / "tw-chips" / "data"
CSV_OUT = ROOT / "data" / "tw_chips" / "csv"
DISPLAY_START = "2016-10-01"
TZ_TAIPEI = dt.timezone(dt.timedelta(hours=8))


# ---------------------------------------------------------------- 純函式（有單元測試）

def yuan_to_yi(x):
    """元 → 億元（2 位小數）。"""
    return None if x is None else round(x / 1e8, 2) + 0.0   # + 0.0 去掉 -0.0


def qianyuan_to_yi(x):
    """仟元／千元 → 億元（2 位小數）。1 仟元 = 1e3 元，1 億 = 1e8 元，故 ÷ 1e5。"""
    return None if x is None else round(x / 1e5, 2) + 0.0


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


def weekly_cap_ratio(cal: list[str], sbl: dict[str, dict], cap: dict[str, dict], key: str, nd: int = 3) -> list:
    """借券金額（元）÷ 上市總市值（%），只在『市值週報』有值的週末日計算，其餘日子 None。

    總市值官方只有週末日數字（億元，×1e8 換成元）；當天沒有借券資料或不在日曆上也是 None。
    不拿前一週的市值去除日頻金額——那樣會把一週內的指數漲跌混進比率。"""
    out = []
    for d in cal:
        c, r = cap.get(d), sbl.get(d)
        out.append(None if c is None or r is None else ratio_pct(r[key], c["cap"] * 1e8, nd))
    return out


# ---------------------------------------------------------------- 回測用 CSV（扁平、一天一列、英文欄名）

WHO3 = (("foreign", "f"), ("trust", "t"), ("dealer", "dl"))


def _csv_columns() -> dict:
    """series → [(欄名, 取值函式(row))]。欄名後綴即單位：_twd＝元、_thousand_twd＝仟元／千元、_yi＝億元、
    _lots＝張、_oi＝未平倉口數、_pct＝百分比。第一欄一律是 date。"""
    cols = {}
    cols["taiex"] = [("open", lambda r: r["o"]), ("high", lambda r: r["h"]),
                     ("low", lambda r: r["l"]), ("close", lambda r: r["c"])]
    cols["turnover"] = [("turnover_twd", lambda r: r["amt"]), ("turnover_yi", lambda r: yuan_to_yi(r["amt"])),
                        ("volume_shares", lambda r: r["sh"])]
    c = []
    for name, k in WHO3:
        c += [(f"{name}_buy_twd", lambda r, k=k: r[k][0]), (f"{name}_sell_twd", lambda r, k=k: r[k][1]),
              (f"{name}_net_twd", lambda r, k=k: r[k][0] - r[k][1]),
              (f"{name}_net_yi", lambda r, k=k: yuan_to_yi(r[k][0] - r[k][1]))]
    cols["inst"] = c
    cols["margin"] = [
        ("margin_balance_lots", lambda r: r["mg"]), ("margin_balance_lots_prev_day", lambda r: r["mg_p"]),
        ("short_balance_lots", lambda r: r["sh"]), ("short_balance_lots_prev_day", lambda r: r["sh_p"]),
        ("margin_balance_thousand_twd", lambda r: r["mga"]), ("margin_balance_thousand_twd_prev_day", lambda r: r["mga_p"]),
        ("margin_balance_yi", lambda r: qianyuan_to_yi(r["mga"])),
        ("short_to_margin_ratio_pct", lambda r: ratio_pct(r["sh"], r["mg"])),
    ]
    c = []
    for name, k in WHO3:
        c += [(f"{name}_long_oi", lambda r, k=k: r[k][0]), (f"{name}_short_oi", lambda r, k=k: r[k][1]),
              (f"{name}_net_oi", lambda r, k=k: r[k][0] - r[k][1])]
    cols["fut_inst"] = c
    c = []
    for side, sk in (("call", "c"), ("put", "p")):
        for name, k in WHO3:
            p = f"{side}_{name}"
            c += [(f"{p}_long_oi", lambda r, sk=sk, k=k: r[sk][k][0]), (f"{p}_short_oi", lambda r, sk=sk, k=k: r[sk][k][1]),
                  (f"{p}_long_oi_amount_thousand_twd", lambda r, sk=sk, k=k: r[sk][k][2]),
                  (f"{p}_short_oi_amount_thousand_twd", lambda r, sk=sk, k=k: r[sk][k][3]),
                  (f"{p}_net_oi", lambda r, sk=sk, k=k: r[sk][k][0] - r[sk][k][1]),
                  (f"{p}_net_oi_amount_yi", lambda r, sk=sk, k=k: qianyuan_to_yi(r[sk][k][2] - r[sk][k][3]))]
    cols["opt_inst"] = c
    cols["pcr"] = [("put_volume", lambda r: r["pv"]), ("call_volume", lambda r: r["cv"]),
                   ("volume_ratio_pct", lambda r: r["vr"]), ("put_oi", lambda r: r["po"]),
                   ("call_oi", lambda r: r["co"]), ("oi_ratio_pct", lambda r: r["or"])]
    c = []
    for grp, key in (("all", "a"), ("specific", "s")):
        for i, nm in enumerate(("top5_long", "top5_short", "top10_long", "top10_short")):
            c.append((f"{grp}_{nm}", lambda r, key=key, i=i: r[key][i]))
        c.append((f"{grp}_top5_net", lambda r, key=key: r[key][0] - r[key][1]))
        c.append((f"{grp}_top10_net", lambda r, key=key: r[key][2] - r[key][3]))
    c.append(("market_oi", lambda r: r["oi"]))
    cols["large"] = c
    cols["usdtwd"] = [("usdtwd", lambda r: r["v"])]
    cols["sbl"] = [
        ("lend_balance_shares", lambda r: r["lend_sh"]), ("lend_balance_twd", lambda r: r["lend_amt"]),
        ("lend_balance_yi", lambda r: yuan_to_yi(r["lend_amt"])),
        ("short_sale_balance_shares", lambda r: r["slb_sh"]), ("short_sale_balance_twd", lambda r: r["slb_amt"]),
        ("short_sale_balance_yi", lambda r: yuan_to_yi(r["slb_amt"])),
        ("short_sale_balance_no_price_shares", lambda r: r["slb_nopx"]),
    ]
    cols["mktcap"] = [("listed_market_cap_yi", lambda r: r["cap"])]
    return cols


def export_csv() -> dict:
    """data/tw_chips/csv/{series}.csv：jsonl 全部歷史（含指數暖機年）扁平化，一天一列。
    融資融券另加 *_final 欄（以隔日『前日餘額』定稿，最新一日仍為當日餘額）。"""
    CSV_OUT.mkdir(parents=True, exist_ok=True)
    counts = {}
    for series, cols in _csv_columns().items():
        rows = load_jsonl(series)
        days = sorted(rows)
        extra = []
        if series == "margin":
            fin = margin_final(days, rows)
            extra = [("margin_balance_yi_final", lambda d: qianyuan_to_yi(fin[d]["mga"])),
                     ("margin_balance_lots_final", lambda d: fin[d]["mg"]),
                     ("short_balance_lots_final", lambda d: fin[d]["sh"]),
                     ("is_final", lambda d: int(fin[d]["final"]))]
        if series == "sbl":
            cap = load_jsonl("mktcap")
            extra = [("listed_market_cap_yi_weekly", lambda d: cap[d]["cap"] if d in cap else None),
                     ("lend_balance_to_market_cap_pct_weekly",
                      lambda d: ratio_pct(rows[d]["lend_amt"], cap[d]["cap"] * 1e8, 3) if d in cap else None),
                     ("short_sale_balance_to_market_cap_pct_weekly",
                      lambda d: ratio_pct(rows[d]["slb_amt"], cap[d]["cap"] * 1e8, 3) if d in cap else None)]
        with (CSV_OUT / f"{series}.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date"] + [n for n, _ in cols] + [n for n, _ in extra])
            for d in days:
                r = rows[d]
                w.writerow([d] + ["" if (v := fn(r)) is None else v for _, fn in cols]
                           + ["" if (v := fn(d)) is None else v for _, fn in extra])
        counts[series] = len(days)
    return counts


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
    sbl = load_jsonl("sbl")
    mktcap = load_jsonl("mktcap")

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

    # 4b. 借券：金額（億元，逐日）、占上市總市值（%，只在市值週報有值的週末日）
    dump("sbl.json", {
        "slb": align(cal, sbl, lambda r: yuan_to_yi(r["slb_amt"])),       # 借券賣出餘額金額（億元）
        "lend": align(cal, sbl, lambda r: yuan_to_yi(r["lend_amt"])),    # 借券餘額金額（億元）
        "cap": [mktcap[d]["cap"] if d in mktcap else None for d in cal],  # 上市總市值（億元，週末日）
        "slb_r": weekly_cap_ratio(cal, sbl, mktcap, "slb_amt"),          # 借券賣出餘額 ÷ 總市值（%）
        "lend_r": weekly_cap_ratio(cal, sbl, mktcap, "lend_amt"),        # 借券餘額 ÷ 總市值（%）
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
        info("sbl", sbl, "借券餘額／借券賣出餘額", "億元", "TWSE TWT72U（官方金額）＋TWT93U（股數×收盤價）"),
        {**info("mktcap", mktcap, "上市總市值（週）", "億元", "TWSE 市值週報"), "gaps": 0},
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
    n_csv = export_csv()
    print("csv：" + "、".join(f"{k} {v} 列" for k, v in n_csv.items()))
    print(f"built：日曆 {cal[0]}～{cal[-1]}（{len(cal)} 日）")
    for s in series:
        print(f"  {s['key']:9s} n={s['n']:5d} {s['first']}～{s['last']} gaps={s['gaps']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
