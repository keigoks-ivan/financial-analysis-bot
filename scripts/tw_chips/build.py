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


def third_wednesday(y: int, m: int) -> dt.date:
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(2 - d.weekday()) % 7)      # 當月第一個星期三
    return d + dt.timedelta(days=14)


def expiry_date(ym: str, calset: set, last_cal: str) -> str:
    """臺指期貨最後交易日＝到期月份第三個星期三；遇休市順延到下一個交易日（以交易日曆判斷）。
    日曆之後的月份沒有曆可查，直接回第三個星期三。2016-10～2026-10 共 123 個已到期契約，
    此規則算出的日期與『契約最後一次出現在行情檔的日期』逐一相同（見測試與 README）。"""
    d = third_wednesday(int(ym[:4]), int(ym[4:]))
    while d.isoformat() not in calset and d.isoformat() <= last_cal:
        d += dt.timedelta(days=1)
    return d.isoformat()


def near_month_pick(day: str, months: list, calset: set, last_cal: str):
    """換月規則：近月契約在最後交易日（結算日）當天就改看次月；其餘日子看近月。
    months＝當天掛牌的月份契約 [[YYYYMM, 收盤價, 結算價], ...]（由近到遠）。回 (契約月份, 收盤價) 或 (None, None)。"""
    for c, close, _settle in months:
        if expiry_date(c, calset, last_cal) > day:
            return c, close
    return None, None


def basis_series(cal: list[str], tx: dict[str, dict], taiex: dict[str, dict]) -> dict:
    """期貨正逆價差：台指期近月一般盤收盤（13:45）−加權指數收盤（13:30）。
    回 {"contract":[...], "fut":[...], "pts":[...], "pct":[...]}，對齊 cal；缺值 None。
    點數＝期貨收盤 − 指數收盤（正值＝正價差、負值＝逆價差）；百分比＝點數 ÷ 指數收盤 × 100。"""
    calset, last_cal = set(taiex), max(taiex, default="")
    contract, fut, pts, pct = [], [], [], []
    for d in cal:
        r, t = tx.get(d), taiex.get(d)
        c, f = near_month_pick(d, r["m"], calset, last_cal) if r else (None, None)
        s = t["c"] if t else None
        contract.append(c)
        fut.append(f)
        if f is None or s is None:
            pts.append(None)
            pct.append(None)
        else:
            pts.append(round(f - s, 2) + 0.0)
            pct.append(round((f - s) / s * 100, 3) + 0.0)
    return {"contract": contract, "fut": fut, "pts": pts, "pct": pct}


def retail_ratio(cal: list[str], inst: dict[str, dict], mkt: dict[str, dict], nd: int = 2) -> dict:
    """散戶多空比（小型／微型臺指期貨）＝ −(三大法人淨未平倉口數合計) ÷ 全市場所有月份未平倉口數 × 100。
    淨口數＝多方未平倉口數 − 空方未平倉口數；三大法人以外的交易人（含散戶、法人以外的大戶）視為同一方。
    正值＝三大法人以外的交易人整體偏多（法人整體偏空）。回 {net, oi, ratio}，對齊 cal。"""
    net, oi, ratio = [], [], []
    for d in cal:
        r, m = inst.get(d), mkt.get(d)
        n = None if r is None else sum(r[k][0] - r[k][1] for k in ("f", "t", "dl"))
        o = None if m is None else m["oi"]
        net.append(n)
        oi.append(o)
        ratio.append(None if n is None or not o else round(-n / o * 100, nd) + 0.0)
    return {"net": net, "oi": oi, "ratio": ratio}


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
    c = []
    for name, k in WHO3:
        c += [(f"{name}_long_oi", lambda r, k=k: r[k][0]), (f"{name}_short_oi", lambda r, k=k: r[k][1]),
              (f"{name}_net_oi", lambda r, k=k: r[k][0] - r[k][1])]
    cols["mtx_inst"] = c
    cols["tmf_inst"] = c
    cols["mtx_mkt"] = [("market_oi_all_contracts", lambda r: r["oi"]), ("market_oi_weekly_contracts", lambda r: r["oi_wk"])]
    cols["tmf_mkt"] = cols["mtx_mkt"]
    c = []
    for i in (1, 2, 3):
        c += [(f"contract_{i}", lambda r, i=i: r["m"][i - 1][0] if len(r["m"]) >= i else None),
              (f"close_{i}", lambda r, i=i: r["m"][i - 1][1] if len(r["m"]) >= i else None),
              (f"settlement_{i}", lambda r, i=i: r["m"][i - 1][2] if len(r["m"]) >= i else None)]
    cols["tx_daily"] = c
    cols["vix"] = [("taiwan_vix_close", lambda r: r["v"]), ("taiwan_vix_last_minute_avg", lambda r: r["v1"])]
    cols["dtrade"] = [("daytrade_shares", lambda r: r["sh"]), ("daytrade_shares_pct_of_market", lambda r: r["sh_p"]),
                      ("daytrade_buy_amount_twd", lambda r: r["buy"]), ("daytrade_buy_amount_yi", lambda r: yuan_to_yi(r["buy"])),
                      ("daytrade_buy_amount_pct_of_market", lambda r: r["buy_p"]),
                      ("daytrade_sell_amount_twd", lambda r: r["sell"]), ("daytrade_sell_amount_pct_of_market", lambda r: r["sell_p"])]
    c = []
    for name, k in WHO3:
        c += [(f"{name}_buy_twd", lambda r, k=k: r[k][0] if k in r else None),
              (f"{name}_sell_twd", lambda r, k=k: r[k][1] if k in r else None),
              (f"{name}_net_twd", lambda r, k=k: r[k][0] - r[k][1] if k in r else None),
              (f"{name}_net_yi", lambda r, k=k: yuan_to_yi(r[k][0] - r[k][1]) if k in r else None)]
    cols["otc_inst"] = c
    cols["otc_margin"] = cols["margin"]
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
        if series in ("margin", "otc_margin"):
            fin = margin_final(days, rows)
            extra = [("margin_balance_yi_final", lambda d: qianyuan_to_yi(fin[d]["mga"])),
                     ("margin_balance_lots_final", lambda d: fin[d]["mg"]),
                     ("short_balance_lots_final", lambda d: fin[d]["sh"]),
                     ("is_final", lambda d: int(fin[d]["final"]))]
        if series in ("mtx_inst", "tmf_inst"):
            mk = load_jsonl("mtx_mkt" if series == "mtx_inst" else "tmf_mkt")
            rr = retail_ratio(days, rows, mk)
            pos = {d: i for i, d in enumerate(days)}
            extra = [("market_oi_all_contracts", lambda d: mk[d]["oi"] if d in mk else None),
                     ("inst_net_oi_total", lambda d: rr["net"][pos[d]]),
                     ("retail_long_short_ratio_pct", lambda d: rr["ratio"][pos[d]])]
        if series == "tx_daily":
            tai = load_jsonl("taiex")
            bs = basis_series(days, rows, tai)
            pos = {d: i for i, d in enumerate(days)}
            extra = [("near_month_contract", lambda d: bs["contract"][pos[d]]),
                     ("near_month_close", lambda d: bs["fut"][pos[d]]),
                     ("taiex_close", lambda d: tai[d]["c"] if d in tai else None),
                     ("basis_points", lambda d: bs["pts"][pos[d]]),
                     ("basis_pct", lambda d: bs["pct"][pos[d]])]
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
    mtx_i, tmf_i = load_jsonl("mtx_inst"), load_jsonl("tmf_inst")
    mtx_m, tmf_m = load_jsonl("mtx_mkt"), load_jsonl("tmf_mkt")
    tx_daily, vix = load_jsonl("tx_daily"), load_jsonl("vix")
    dtrade = load_jsonl("dtrade")
    otc_inst, otc_margin = load_jsonl("otc_inst"), load_jsonl("otc_margin")

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

    # 10. 小型／微型臺指期貨：三大法人淨未平倉口數與散戶多空比
    rr_m, rr_t = retail_ratio(cal, mtx_i, mtx_m), retail_ratio(cal, tmf_i, tmf_m)
    dump("mtx.json", {
        "f": align(cal, mtx_i, lambda r: r["f"][0] - r["f"][1]),
        "t": align(cal, mtx_i, lambda r: r["t"][0] - r["t"][1]),
        "dl": align(cal, mtx_i, lambda r: r["dl"][0] - r["dl"][1]),
        "net": rr_m["net"], "oi": rr_m["oi"], "ratio": rr_m["ratio"],
        "tmf_net": rr_t["net"], "tmf_oi": rr_t["oi"], "tmf_ratio": rr_t["ratio"],
    })

    # 11. 期貨正逆價差（近月收盤 − 加權指數收盤）與臺指選擇權波動率指數
    bs = basis_series(cal, tx_daily, taiex_all)
    dump("basis.json", {
        "pts": bs["pts"], "pct": bs["pct"], "fut": bs["fut"], "contract": bs["contract"],
        "vix": align(cal, vix, lambda r: r["v"]),
    })

    # 12. 上市當日沖銷（占市場成交金額、股數比重；當沖買進金額）
    dump("dtrade.json", {
        "r_amt": align(cal, dtrade, lambda r: r["buy_p"]),
        "r_sh": align(cal, dtrade, lambda r: r["sh_p"]),
        "amt": align(cal, dtrade, lambda r: yuan_to_yi(r["buy"])),
    })

    # 13. 上櫃（櫃買中心）三大法人買賣超（億元）與融資融券餘額
    ofin = margin_final(cal, otc_margin)
    omg = align(cal, ofin, lambda r: r["mg"])
    osh = align(cal, ofin, lambda r: r["sh"])
    dump("otc.json", {
        "f": align(cal, otc_inst, lambda r: yuan_to_yi(r["f"][0] - r["f"][1]) if "f" in r else None),
        "t": align(cal, otc_inst, lambda r: yuan_to_yi(r["t"][0] - r["t"][1])),
        "dl": align(cal, otc_inst, lambda r: yuan_to_yi(r["dl"][0] - r["dl"][1])),
        "mga": align(cal, ofin, lambda r: qianyuan_to_yi(r["mga"])),
        "mg": omg, "sh": osh,
        "ratio": [ratio_pct(s_, m_) for s_, m_ in zip(osh, omg)],
    })

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
        info("mtx_inst", mtx_i, "小型臺指期貨三大法人未平倉", "口", "TAIFEX futContractsDateDown MXF（2023-10 起）＋FinMind 轉載（2018-06 起）"),
        info("tmf_inst", tmf_i, "微型臺指期貨三大法人未平倉", "口", "TAIFEX futContractsDateDown TMF"),
        info("mtx_mkt", mtx_m, "小型臺指期貨全市場未平倉口數", "口", "TAIFEX dlFutDataDown MTX"),
        info("tmf_mkt", tmf_m, "微型臺指期貨全市場未平倉口數", "口", "TAIFEX dlFutDataDown TMF"),
        info("tx_daily", tx_daily, "臺股期貨近月收盤（正逆價差）", "點", "TAIFEX dlFutDataDown TX"),
        {**info("vix", vix, "臺指選擇權波動率指數", "點", "TAIFEX 波動率指數月檔（官網只留近約 4 個月）"), "gaps": 0},
        info("dtrade", dtrade, "上市當日沖銷統計", "億元／%", "TWSE dayTrading/TWTB4U"),
        info("otc_inst", otc_inst, "上櫃三大法人買賣超", "億元", "TPEx insti/summary"),
        info("otc_margin", otc_margin, "上櫃融資融券餘額", "億元／張", "TPEx margin/balance"),
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
