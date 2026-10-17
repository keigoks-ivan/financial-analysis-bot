#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""台股籌碼趨勢（/tw-chips/）資料抓取：每個資料源一個 fetcher，增量寫進 data/tw_chips/{series}.jsonl。

序列（一天一行，鍵 d＝YYYY-MM-DD；金額一律存來源原單位，換算成億元在 build.py 做）：
    taiex      加權指數 OHLC                      TWSE MI_5MINS_HIST（月查詢）
    turnover   全市場成交金額（元）/成交股數       TWSE FMTQIK（月查詢）
    inst       現貨三大法人買進/賣出金額（元）      TWSE BFI82U（逐日）
    margin     融資融券餘額（張、融資金額仟元）    TWSE MI_MARGN（逐日）
    sbl        上市借券餘額（官方金額）＋借券賣出餘額（股數×收盤價）  TWSE lending/TWT72U ＋ marginTrading/TWT93U（逐日）
    mktcap     上市股票總市值（億元，週末）          TWSE statisticsWeek『市值週報』（單一 zip，2005-09 起）
    fut_inst   臺股期貨三大法人未平倉口數          TAIFEX futContractsDateDown（近 3 年）＋ FinMind（2018-06 起，同源轉載）
    opt_inst   臺指選擇權三大法人買賣權未平倉      TAIFEX callsAndPutsDateDown（近 3 年）＋ FinMind（同上）
    pcr        選擇權 Put/Call Ratio              TAIFEX pcRatioDown（月查詢）
    large      臺股期貨大額交易人前五/前十大       TAIFEX largeTraderFutDown（月查詢）
    usdtwd     新台幣兌美元                        FRED DEXTAUS
    mtx_inst   小型臺指期貨三大法人未平倉口數        TAIFEX futContractsDateDown（MXF，近 3 年）＋ FinMind（2018-06 起，同源轉載）
    tmf_inst   微型臺指期貨三大法人未平倉口數        TAIFEX futContractsDateDown（TMF，2024-07 上市起）
    mtx_mkt    小型臺指期貨全市場未平倉口數合計      TAIFEX dlFutDataDown（MTX，月查詢，2016-10 起）
    tmf_mkt    微型臺指期貨全市場未平倉口數合計      TAIFEX dlFutDataDown（TMF，月查詢，2024-07 起）
    tx_daily   臺股期貨各到期月收盤／結算價（前 3 個月份）TAIFEX dlFutDataDown（TX，月查詢，2016-10 起）
    vix        臺指選擇權波動率指數（TAIWAN VIX）日收盤  TAIFEX vix/log2data/YYYYMMnew.txt（官網只留最近約 4 個月）
    dtrade     上市當日沖銷交易統計（股數、金額、占市場比重）  TWSE dayTrading/TWTB4U（逐日）
    otc_inst   上櫃三大法人買賣金額彙總（元）        TPEx insti/summary（逐日；2017-01 起只有投信、自營商，外資 2018-01-15 起）
    otc_margin 上櫃融資融券餘額彙總（張、融資金額仟元）TPEx margin/balance（逐日）

期交所網站只開放「近 3 年」的三大法人期貨/選擇權日資料；更早的部分用 FinMind 轉載的同一份期交所資料補
（2023-10-16 起與期交所逐筆核對一致，見頁面資料來源說明）。FinMind 最早只到 2018-06-05，
之前沒有可取得的來源，照實留白，不補假資料。

TWSE 頻率限制：請求間隔 ≥ 3 秒；307/403/429/5xx/非 JSON 一律退避重試。
用法：
    python3 scripts/tw_chips/fetch.py                  # 日常：只抓缺的日子
    python3 scripts/tw_chips/fetch.py --backfill       # 回補 10 年（2016-10 起），可續跑
    python3 scripts/tw_chips/fetch.py --only inst,margin --backfill
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import random
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "tw_chips"
START = dt.date(2016, 10, 1)          # 回補起點（約 10 年）
TAIEX_START = dt.date(2015, 10, 1)    # 加權指數多抓 1 年，讓 240 日均線在 2016-10 就有值
FINMIND_START = dt.date(2018, 6, 1)   # FinMind 期貨/選擇權法人資料最早可得日
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
TWSE = "https://www.twse.com.tw/rwd/zh"
TAIFEX = "https://www.taifex.com.tw/cht/3"
TPEX = "https://www.tpex.org.tw/www/zh-tw"
TPEX_GAP = 2.5        # 秒；櫃買中心沒有公布頻率限制，比照 TWSE 保守放慢
TMF_START = dt.date(2024, 7, 1)        # 微型臺指期貨 2024-07-29 上市
OTC_INST_START = dt.date(2017, 1, 1)   # 櫃買三大法人彙總最早有資料的年份（2017-01-03 起，之前整天查無資料）
VIX_URL = "https://www.taifex.com.tw/file/taifex/Dailydownload/vix/log2data/{ym}new.txt"
TWSE_GAP = 3.2        # 秒；官方限制約 3 次/5 秒，保守取 3.2
TAIFEX_GAP = 1.5
BACKOFF = [20, 60, 180, 300]   # 退避秒數；用完仍失敗就放棄該請求
TZ_TAIPEI = dt.timezone(dt.timedelta(hours=8))

SERIES = ["taiex", "turnover", "inst", "margin", "sbl", "mktcap", "fut_inst", "opt_inst", "pcr", "large", "usdtwd",
          "mtx_inst", "tmf_inst", "mtx_mkt", "tmf_mkt", "tx_daily", "vix", "dtrade", "otc_inst", "otc_margin"]


# ---------------------------------------------------------------- 純解析函式（有單元測試）

def roc_to_iso(s: str) -> str | None:
    """'105/10/03' → '2016-10-03'；格式不符回 None。"""
    m = re.fullmatch(r"\s*(\d{2,3})/(\d{1,2})/(\d{1,2})\s*", s or "")
    if not m:
        return None
    return f"{int(m.group(1)) + 1911:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"


def slash_to_iso(s: str) -> str | None:
    """'2023/10/16' → '2023-10-16'。"""
    m = re.fullmatch(r"\s*(\d{4})/(\d{1,2})/(\d{1,2})\s*", s or "")
    if not m:
        return None
    return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"


def to_num(s):
    """'9,219.52' → 9219.52；'-83,006,510' → -83006510；空白/--/None → None。整數字串回 int。"""
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return s
    t = str(s).strip().replace(",", "")
    if t in ("", "-", "--", "---", "N/A", "X"):
        return None
    try:
        return int(t) if re.fullmatch(r"-?\d+", t) else float(t)
    except ValueError:
        return None


def parse_taiex_month(payload: dict) -> list[dict]:
    """MI_5MINS_HIST 月回應 → [{d,o,h,l,c}]。"""
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return []
    out = []
    for row in payload.get("data") or []:
        d = roc_to_iso(row[0])
        o, h, l, c = (to_num(x) for x in row[1:5])
        if d and None not in (o, h, l, c):
            out.append({"d": d, "o": o, "h": h, "l": l, "c": c})
    return out


def parse_turnover_month(payload: dict) -> list[dict]:
    """FMTQIK 月回應 → [{d, amt（元）, sh（股）}]。"""
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return []
    fields = payload.get("fields") or []
    try:
        i_d, i_amt, i_sh = fields.index("日期"), fields.index("成交金額"), fields.index("成交股數")
    except ValueError:
        return []
    out = []
    for row in payload.get("data") or []:
        d = roc_to_iso(row[i_d])
        amt, sh = to_num(row[i_amt]), to_num(row[i_sh])
        if d and amt is not None:
            out.append({"d": d, "amt": amt, "sh": sh})
    return out


def parse_bfi82u(payload: dict, d: str) -> dict | None:
    """BFI82U 日回應 → {d, f:[買,賣], t:[買,賣], dl:[買,賣]}（元）。

    外資＝「外資及陸資(不含外資自營商)」＋「外資自營商」（新版拆兩列、舊版一列，一律加總）；
    自營商＝自行買賣＋避險。休市／查無資料回 None。
    """
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return None
    acc = {"f": [0, 0], "t": [0, 0], "dl": [0, 0]}
    seen = set()
    for row in payload.get("data") or []:
        name = row[0]
        key = "f" if name.startswith("外資") else "t" if name.startswith("投信") else \
              "dl" if name.startswith("自營商") else None
        if key is None:
            continue
        b, s = to_num(row[1]), to_num(row[2])
        if b is None or s is None:
            return None
        acc[key][0] += b
        acc[key][1] += s
        seen.add(key)
    if seen != {"f", "t", "dl"}:
        return None
    return {"d": d, **acc}


def parse_margn(payload: dict, d: str) -> dict | None:
    """MI_MARGN（selectType=MS）日回應 → 融資/融券張數與融資金額（含前日餘額）。

    mg＝融資餘額（張）、sh＝融券餘額（張）、mga＝融資餘額（仟元）；*_p＝前日餘額（官方註明
    「以前日餘額為準」，隔日才完整揭露）。
    """
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return None
    tables = payload.get("tables") or []
    if not tables:
        return None
    rows = {r[0]: r for r in tables[0].get("data") or []}
    def pick(prefix):
        for k, v in rows.items():
            if k.startswith(prefix):
                return v
        return None
    mg, sh, mga = pick("融資(交易單位)"), pick("融券(交易單位)"), pick("融資金額")
    if not (mg and sh and mga):
        return None
    vals = {
        "mg": to_num(mg[5]), "mg_p": to_num(mg[4]),
        "sh": to_num(sh[5]), "sh_p": to_num(sh[4]),
        "mga": to_num(mga[5]), "mga_p": to_num(mga[4]),
    }
    if None in vals.values():
        return None
    return {"d": d, **vals}


def parse_lending_total(payload: dict, d: str) -> dict | None:
    """lending/TWT72U（selectType=SLBNLB）日回應 → 上市（集中市場）借券餘額與各股收盤價。

    回傳 {lend_sh, lend_amt, px:{代號:收盤價}}：
    lend_sh＝上市借券餘額（股）、lend_amt＝上市借券餘額市值（元，證交所官方彙總，
    ＝各股本日借券餘額 × 本日收盤價加總）；px 供借券賣出餘額換算金額用。
    只取「合計」列中市場別為「集中市場」的那一列（櫃檯買賣中心、整體市場兩列不用）。
    日期不符（休市日被導到別天）或欄位改版回 None。
    """
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return None
    if payload.get("date") and payload["date"] != d.replace("-", ""):
        return None
    fields = payload.get("fields") or []
    if len(fields) < 9 or not fields[5].startswith("本日借券餘額") or "收盤價" not in fields[6] \
            or "市值" not in fields[7] or fields[8] != "市場別":
        return None
    tot, px = None, {}
    for row in payload.get("data") or []:
        if len(row) < 9:
            continue
        if row[0].strip() == "合計":
            if row[8].strip() == "集中市場":
                tot = row
            continue
        c = to_num(row[6])
        if c is not None:
            px[row[0].strip()] = c
    if tot is None:
        return None
    sh, amt = to_num(tot[5]), to_num(tot[7])
    if sh is None or amt is None:
        return None
    return {"lend_sh": sh, "lend_amt": amt, "px": px}


def parse_short_balance(payload: dict, d: str, px: dict) -> dict | None:
    """marginTrading/TWT93U（融券借券賣出餘額）日回應 → 上市借券賣出餘額（股）與金額（元）。

    借券賣出餘額金額＝各股「借券賣出當日餘額」× 當日收盤價（收盤價取自 TWT72U 同日同代號）加總。
    證交所沒有借券賣出餘額的金額彙總，所以這條是自己乘出來的；找不到收盤價的股數記在 slb_nopx。
    """
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return None
    if payload.get("date") and payload["date"] != d.replace("-", ""):
        return None
    fields = payload.get("fields") or []
    if len(fields) < 15 or fields[0] != "代號" or fields[12] != "當日餘額" or fields[8] != "前日餘額":
        return None
    sh = amt = nopx = 0
    total_row = None
    for row in payload.get("data") or []:
        if len(row) < 13:
            continue
        code = row[0].strip()
        if not code:                       # 表尾「合計」列代號是空字串
            if row[1].strip() == "合計":
                total_row = row
            continue
        n = to_num(row[12])
        if not n:
            continue
        sh += n
        if code in px:
            amt += n * px[code]
        else:
            nopx += n
    if total_row is None:
        return None
    return {"slb_sh": sh, "slb_amt": round(amt, 2), "slb_nopx": nopx}


def parse_mktcap_xls(path_or_bytes) -> list[dict]:
    """市值週報 week1-new.xls → [{d, cap}]；cap＝上市股票總市值（億元），d＝週末日（通常週五）。

    需要 xlrd（.xls 舊格式）。第 0、1 列是表頭，之後每列一週：[Excel 日期序號, 總市值]。
    """
    import xlrd
    book = xlrd.open_workbook(file_contents=path_or_bytes) if isinstance(path_or_bytes, bytes) \
        else xlrd.open_workbook(path_or_bytes)
    sh = book.sheet_by_index(0)
    out = []
    for r in range(2, sh.nrows):
        row = sh.row_values(r)
        try:
            serial, cap = float(row[0]), float(row[1])
        except (TypeError, ValueError, IndexError):
            continue
        day = dt.date(1899, 12, 30) + dt.timedelta(days=int(serial))
        out.append({"d": day.isoformat(), "cap": cap})
    return out


def parse_fut_daily_csv(text: str) -> list[dict]:
    """dlFutDataDown（down_type=1，單一商品）日行情 CSV → [{d, oi, oi_wk, m}]。

    只取『一般』交易時段（盤後列沒有未沖銷口數）、略過跨月價差單（到期月份含 '/'）。
    oi＝所有到期契約（含週契約）未沖銷口數合計；oi_wk＝其中週契約（月份欄形如 202610W4）；
    m＝最近三個月份契約 [[月份 YYYYMM, 收盤價, 結算價], ...]（收盤價『-』＝當天沒成交，存 None）。"""
    by_day: dict[str, dict] = {}
    for r in _csv_rows(text):
        if r.get("交易時段", "一般") not in ("一般", ""):
            continue
        d = slash_to_iso(r.get("交易日期", ""))
        c = r.get("到期月份(週別)", "").strip()
        if not d or not c or "/" in c:
            continue
        oi = to_num(r.get("未沖銷契約數")) or 0
        rec = by_day.setdefault(d, {"d": d, "oi": 0, "oi_wk": 0, "m": []})
        rec["oi"] += oi
        if re.fullmatch(r"\d{6}", c):
            rec["m"].append([c, to_num(r.get("收盤價")), to_num(r.get("結算價"))])
        else:
            rec["oi_wk"] += oi
    for rec in by_day.values():
        rec["m"] = sorted(rec["m"])[:3]
    return [v for _, v in sorted(by_day.items()) if v["m"] or v["oi_wk"]]


def parse_vix_txt(text: str) -> list[dict]:
    """期交所臺指選擇權波動率指數月檔（cp950 解碼後）→ [{d, v, v1}]。
    欄位：日期、時間（13450000＝13:45:00）、臺指選擇權波動率指數、收盤前 1 分鐘平均。
    v＝當日收盤（13:45 最後一筆）；v1＝收盤前 1 分鐘平均。"""
    out = []
    for line in text.splitlines():
        m = re.match(r"\s*(\d{8})\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s*$", line)
        if m:
            d = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}"
            out.append({"d": d, "v": float(m.group(3)), "v1": float(m.group(4))})
    return sorted(out, key=lambda x: x["d"])


def parse_dtrade(payload: dict, d: str) -> dict | None:
    """dayTrading/TWTB4U 日回應 → 上市當日沖銷統計。

    sh＝當日沖銷成交股數、sh_p＝占市場成交股數比重%；
    buy／sell＝當日沖銷買進／賣出成交金額（元）、buy_p／sell_p＝占市場買進／賣出平均成交金額比重%
    （官方公式：÷（整體市場買進＋賣出）÷2，市場含一般、盤後定價、零股、鉅額，與 FMTQIK 成交金額一致）。
    日期不符或欄位改版回 None。"""
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return None
    if payload.get("date") and payload["date"] != d.replace("-", ""):
        return None
    for t in payload.get("tables") or []:
        f = t.get("fields") or []
        if len(f) >= 6 and f[0] == "當日沖銷交易總成交股數" and f[1].startswith("當日沖銷交易總成交股數占市場比重") \
                and "買進成交金額" in f[2] and "買進成交金額占市場比重" in f[3] \
                and "賣出成交金額" in f[4] and "賣出成交金額占市場比重" in f[5] and t.get("data"):
            vals = [to_num(x) for x in t["data"][0][:6]]
            if len(vals) < 6 or None in vals:
                return None
            return {"d": d, "sh": vals[0], "sh_p": vals[1], "buy": vals[2], "buy_p": vals[3],
                    "sell": vals[4], "sell_p": vals[5]}
    return None


def _norm_name(s: str) -> str:
    return re.sub(r"[\s　*＊]", "", s or "")


def parse_tpex_inst(payload: dict, d: str) -> dict | None:
    """櫃買中心 insti/summary（三大法人買賣金額彙總表）→ {d, f?:[買,賣], t:[買,賣], dl:[買,賣]}（元）。

    f＝外資及陸資（不含外資自營商，外資自營商已含在自營商內）、t＝投信、dl＝自營商合計。
    2017-01-03～2018-01-12 官方只列投信與自營商（沒有外資列與合計列），此時不含 f；
    2017-01 以前整天查無資料。休市／日期不符回 None。"""
    if not isinstance(payload, dict) or payload.get("stat") != "ok":
        return None
    if payload.get("date") and payload["date"] != d.replace("-", ""):
        return None
    tabs = payload.get("tables") or []
    if not tabs:
        return None
    found: dict[str, list] = {}
    for row in tabs[0].get("data") or []:
        if not row or len(row) < 3:
            continue
        name = _norm_name(row[0])
        b, s = to_num(row[1]), to_num(row[2])
        if b is None or s is None:
            continue
        key = {"外資及陸資(不含自營商)": "f", "外資及陸資合計": "f_all", "投信": "t",
               "自營商合計": "dl", "自營商": "dl"}.get(name)
        if key and key not in found:
            found[key] = [b, s]
    if "t" not in found or "dl" not in found:
        return None
    rec = {"d": d, "t": found["t"], "dl": found["dl"]}
    f = found.get("f") or found.get("f_all")
    if f:
        rec["f"] = f
    return rec


def parse_tpex_margin(payload: dict, d: str) -> dict | None:
    """櫃買中心 margin/balance（上櫃股票融資融券餘額）表尾合計列 → 與 TWSE margin 同結構。

    mg＝融資餘額（張）、sh＝融券餘額（張）、mga＝融資餘額（仟元）；*_p＝前日餘額。
    直接取官方『合計(張)』與『融資金(仟元)』兩列，不逐檔加總。"""
    if not isinstance(payload, dict) or payload.get("stat") != "ok":
        return None
    if payload.get("date") and payload["date"] != d.replace("-", ""):
        return None
    tabs = payload.get("tables") or []
    if not tabs:
        return None
    f = tabs[0].get("fields") or []
    try:
        i_mg, i_mgp = f.index("資餘額"), f.index("前資餘額(張)")
        i_sh, i_shp = f.index("券餘額"), f.index("前券餘額(張)")
    except ValueError:
        return None
    tot = amt = None
    for row in tabs[0].get("summary") or []:
        if len(row) > max(i_mg, i_mgp, i_sh, i_shp):
            if row[1].startswith("合計"):
                tot = row
            elif row[1].startswith("融資金"):
                amt = row
    if tot is None or amt is None:
        return None
    vals = {"mg": to_num(tot[i_mg]), "mg_p": to_num(tot[i_mgp]), "sh": to_num(tot[i_sh]),
            "sh_p": to_num(tot[i_shp]), "mga": to_num(amt[i_mg]), "mga_p": to_num(amt[i_mgp])}
    if None in vals.values():
        return None
    return {"d": d, **vals}


def _csv_rows(text: str) -> list[dict]:
    """期交所 CSV（cp950 解碼後）→ dict 列；欄名去空白，濾掉尾端空欄與 HTML 錯誤頁。"""
    if "<html" in text.lower()[:400] or "DateTime" in text[:400]:
        return []
    reader = csv.reader(io.StringIO(text))
    try:
        header = [h.strip() for h in next(reader)]
    except StopIteration:
        return []
    out = []
    for r in reader:
        if not r or not r[0].strip():
            continue
        out.append({h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(header) if h})
    return out


def _inst_key(name: str) -> str | None:
    if name.startswith("外資"):
        return "f"
    if name.startswith("投信"):
        return "t"
    if name.startswith("自營商"):
        return "dl"
    return None


def parse_fut_inst_csv(text: str, prod: str = "臺股期貨") -> list[dict]:
    """futContractsDateDown（commodityId=TXF／MXF／TMF）CSV → [{d, f:[多單OI,空單OI], t:[..], dl:[..]}]（口）。
    prod＝CSV『商品名稱』欄：臺股期貨（TXF）、小型臺指期貨（MXF）、微型臺指期貨（TMF）。"""
    by_day: dict[str, dict] = {}
    for r in _csv_rows(text):
        if r.get("商品名稱") != prod:
            continue
        d, k = slash_to_iso(r["日期"]), _inst_key(r.get("身份別", ""))
        lo, so = to_num(r.get("多方未平倉口數")), to_num(r.get("空方未平倉口數"))
        if d and k and lo is not None and so is not None:
            by_day.setdefault(d, {"d": d})[k] = [lo, so]
    return [v for _, v in sorted(by_day.items()) if {"f", "t", "dl"} <= set(v)]


def parse_opt_inst_csv(text: str) -> list[dict]:
    """callsAndPutsDateDown（commodityId=TXO）CSV →
    [{d, c:{f:[多單OI口,空單OI口,多單OI金額千元,空單OI金額千元],t:..,dl:..}, p:{...}}]。"""
    by_day: dict[str, dict] = {}
    for r in _csv_rows(text):
        if r.get("商品名稱") != "臺指選擇權":
            continue
        d, k = slash_to_iso(r["日期"]), _inst_key(r.get("身份別", ""))
        cp = {"CALL": "c", "PUT": "p"}.get(r.get("買賣權別", "").upper())
        vals = [to_num(r.get(x)) for x in ("買方未平倉口數", "賣方未平倉口數",
                                           "買方未平倉契約金額(千元)", "賣方未平倉契約金額(千元)")]
        if d and k and cp and None not in vals:
            by_day.setdefault(d, {"d": d, "c": {}, "p": {}})[cp][k] = vals
    return [v for _, v in sorted(by_day.items())
            if all({"f", "t", "dl"} <= set(v[s]) for s in ("c", "p"))]


def parse_pcr_csv(text: str) -> list[dict]:
    """pcRatioDown CSV → [{d, pv, cv, vr（成交量比%）, po, co, or_（未平倉比%）}]。"""
    out = []
    for r in _csv_rows(text):
        d = slash_to_iso(r.get("日期", ""))
        pv, cv = to_num(r.get("賣權成交量")), to_num(r.get("買權成交量"))
        po, co = to_num(r.get("賣權未平倉量")), to_num(r.get("買權未平倉量"))
        vr, orr = to_num(r.get("買賣權成交量比率%")), to_num(r.get("買賣權未平倉量比率%"))
        if d and None not in (pv, cv, po, co, vr, orr):
            out.append({"d": d, "pv": pv, "cv": cv, "vr": vr, "po": po, "co": co, "or": orr})
    return sorted(out, key=lambda x: x["d"])


def parse_large_csv(text: str) -> list[dict]:
    """largeTraderFutDown CSV → 臺股期貨（代號 TX、到期月份 999999＝全部月份）：
    [{d, a:[前五大買,前五大賣,前十大買,前十大賣]（全部交易人）, s:[同上]（特定法人）, oi}]。"""
    by_day: dict[str, dict] = {}
    for r in _csv_rows(text):
        if r.get("商品(契約)", "").strip() != "TX" or r.get("到期月份(週別)", "").strip() != "999999":
            continue
        d = slash_to_iso(r["日期"])
        typ = r.get("交易人類別", "").strip()
        vals = [to_num(r.get(x)) for x in ("前五大交易人買方", "前五大交易人賣方",
                                           "前十大交易人買方", "前十大交易人賣方")]
        oi = to_num(r.get("全市場未沖銷部位數"))
        if not d or typ not in ("0", "1") or None in vals or oi is None:
            continue
        rec = by_day.setdefault(d, {"d": d})
        rec["a" if typ == "0" else "s"] = vals
        rec["oi"] = oi
    return [v for _, v in sorted(by_day.items()) if "a" in v and "s" in v]


def parse_fred_csv(text: str) -> list[dict]:
    """FRED fredgraph.csv → [{d, v}]；'.' 為缺值。"""
    out = []
    for i, line in enumerate(text.splitlines()):
        if i == 0 or "," not in line:
            continue
        d, v = line.split(",", 1)
        v = to_num(v.strip())
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) and v is not None:
            out.append({"d": d, "v": v})
    return out


def finmind_fut_rows(data: list[dict], fid: str = "TX") -> list[dict]:
    """FinMind TaiwanFuturesInstitutionalInvestors（futures_id=TX／MTX／TMF）→ 同 parse_fut_inst_csv 結構。"""
    m = {"外資": "f", "外資及陸資": "f", "投信": "t", "自營商": "dl"}
    by_day: dict[str, dict] = {}
    for r in data:
        k = m.get(r.get("institutional_investors"))
        if k and r.get("futures_id") == fid:
            by_day.setdefault(r["date"], {"d": r["date"]})[k] = [
                r["long_open_interest_balance_volume"], r["short_open_interest_balance_volume"]]
    return [v for _, v in sorted(by_day.items()) if {"f", "t", "dl"} <= set(v)]


def finmind_opt_rows(data: list[dict]) -> list[dict]:
    """FinMind TaiwanOptionInstitutionalInvestors（option_id=TXO）→ 同 parse_opt_inst_csv 結構。"""
    m = {"外資": "f", "外資及陸資": "f", "投信": "t", "自營商": "dl"}
    cp_m = {"買權": "c", "賣權": "p"}
    by_day: dict[str, dict] = {}
    for r in data:
        k, cp = m.get(r.get("institutional_investors")), cp_m.get(r.get("call_put"))
        if k and cp and r.get("option_id") == "TXO":
            by_day.setdefault(r["date"], {"d": r["date"], "c": {}, "p": {}})[cp][k] = [
                r["long_open_interest_balance_volume"], r["short_open_interest_balance_volume"],
                r["long_open_interest_balance_amount"], r["short_open_interest_balance_amount"]]
    return [v for _, v in sorted(by_day.items())
            if all({"f", "t", "dl"} <= set(v[s]) for s in ("c", "p"))]


# ---------------------------------------------------------------- 存檔

class Store:
    """data/tw_chips/{name}.jsonl：一天一行，鍵 d；同日以後寫入者為準（讀入時覆蓋）。"""

    def __init__(self, name: str):
        self.name = name
        self.path = DATA / f"{name}.jsonl"
        self.rows: dict[str, dict] = {}
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    self.rows[r["d"]] = r

    def has(self, d: str) -> bool:
        return d in self.rows

    def add(self, row: dict) -> bool:
        """同日內容沒變就不寫；有新或有改才 append 一行。"""
        old = self.rows.get(row["d"])
        if old == row:
            return False
        DATA.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
        self.rows[row["d"]] = row
        return True

    def dates(self) -> list[str]:
        return sorted(self.rows)

    def last(self) -> str | None:
        return max(self.rows) if self.rows else None

    def compact(self):
        """重寫成依日期排序、每日一行（回補完成後整理用）。"""
        with self.path.open("w", encoding="utf-8") as f:
            for d in sorted(self.rows):
                f.write(json.dumps(self.rows[d], ensure_ascii=False, separators=(",", ":")) + "\n")


class State:
    """data/tw_chips/_state.json：months_done（已抓完的整月）與 gaps（逐日查無資料的嘗試次數）。"""

    def __init__(self):
        self.path = DATA / "_state.json"
        self.d = {"months_done": {}, "gaps": {}}
        if self.path.exists():
            self.d.update(json.loads(self.path.read_text(encoding="utf-8")))

    def save(self):
        DATA.mkdir(parents=True, exist_ok=True)
        # 多個回補程序同時跑（TWSE／TPEx 各一個）時，先併入磁碟上別人剛寫的內容，避免互相覆蓋
        if self.path.exists():
            try:
                disk = json.loads(self.path.read_text(encoding="utf-8"))
            except ValueError:
                disk = {}
            for s, lst in (disk.get("months_done") or {}).items():
                mine = self.d["months_done"].setdefault(s, [])
                self.d["months_done"][s] = sorted(set(mine) | set(lst))
            for s, g in (disk.get("gaps") or {}).items():
                mine = self.d["gaps"].setdefault(s, {})
                for day, n in g.items():
                    mine[day] = max(mine.get(day, 0), n)
        self.path.write_text(json.dumps(self.d, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                             encoding="utf-8")

    def month_done(self, series: str, ym: str) -> bool:
        return ym in self.d["months_done"].get(series, [])

    def mark_month(self, series: str, ym: str):
        lst = self.d["months_done"].setdefault(series, [])
        if ym not in lst:
            lst.append(ym)
            lst.sort()

    def gap_attempts(self, series: str, d: str) -> int:
        return self.d["gaps"].get(series, {}).get(d, 0)

    def bump_gap(self, series: str, d: str):
        g = self.d["gaps"].setdefault(series, {})
        g[d] = g.get(d, 0) + 1


# ---------------------------------------------------------------- HTTP

class Throttle:
    def __init__(self, gap: float):
        self.gap, self.last = gap, 0.0

    def wait(self):
        dtm = time.monotonic() - self.last
        if dtm < self.gap:
            time.sleep(self.gap - dtm + random.uniform(0, 0.4))
        self.last = time.monotonic()


_twse_throttle = Throttle(TWSE_GAP)
_taifex_throttle = Throttle(TAIFEX_GAP)
_tpex_throttle = Throttle(TPEX_GAP)
_session = requests.Session()
_session.headers.update(UA)


class Blocked(Exception):
    pass


def twse_json(path: str, params: dict) -> dict:
    """打 TWSE rwd 端點；307/403/429/5xx、非 JSON、空回應一律退避重試，用完拋 Blocked。
    『查無資料』(stat 非 OK) 是正常回應，直接回傳給呼叫端判斷。"""
    last_err = ""
    for wait in [0] + BACKOFF:
        if wait:
            log(f"  退避 {wait}s（{last_err}）")
            time.sleep(wait)
        _twse_throttle.wait()
        try:
            r = _session.get(f"{TWSE}/{path}", params={**params, "response": "json"},
                             timeout=30, allow_redirects=False)
        except requests.RequestException as e:
            last_err = f"{type(e).__name__}"
            continue
        if r.status_code in (307, 302, 403, 429) or r.status_code >= 500:
            last_err = f"HTTP {r.status_code}"
            continue
        try:
            j = r.json()
        except ValueError:
            last_err = "非 JSON/空回應"
            continue
        if not isinstance(j, dict) or "stat" not in j:
            last_err = "缺 stat"
            continue
        return j
    raise Blocked(f"TWSE {path} {params} 重試用盡：{last_err}")


def tpex_json(path: str, params: dict) -> dict:
    """打櫃買中心 www/zh-tw 端點（回 JSON，成功時 stat＝ok）；非 JSON／5xx／429 退避重試，用完拋 Blocked。"""
    last_err = ""
    for wait in [0] + BACKOFF[:3]:
        if wait:
            log(f"  退避 {wait}s（{last_err}）")
            time.sleep(wait)
        _tpex_throttle.wait()
        try:
            r = _session.get(f"{TPEX}/{path}", params={**params, "response": "json"},
                             timeout=60, allow_redirects=False)
        except requests.RequestException as e:
            last_err = f"{type(e).__name__}"
            continue
        if r.status_code in (301, 302, 307, 403, 429) or r.status_code >= 500:
            last_err = f"HTTP {r.status_code}"
            continue
        try:
            j = r.json()
        except ValueError:
            last_err = "非 JSON/空回應"
            continue
        if not isinstance(j, dict) or "stat" not in j:
            last_err = "缺 stat"
            continue
        return j
    raise Blocked(f"TPEx {path} {params} 重試用盡：{last_err}")


def taifex_post(endpoint: str, data: dict) -> str:
    last_err = ""
    for wait in [0, 10, 30, 90]:
        if wait:
            time.sleep(wait)
        _taifex_throttle.wait()
        try:
            r = _session.post(f"{TAIFEX}/{endpoint}", data=data, timeout=120)
        except requests.RequestException as e:
            last_err = type(e).__name__
            continue
        if r.status_code != 200:
            last_err = f"HTTP {r.status_code}"
            continue
        return r.content.decode("cp950", errors="replace")
    raise Blocked(f"TAIFEX {endpoint} {data} 重試用盡：{last_err}")


def log(msg: str):
    print(msg, flush=True)


# ---------------------------------------------------------------- 日期工具

def today_tpe() -> dt.date:
    return dt.datetime.now(TZ_TAIPEI).date()


def month_starts(a: dt.date, b: dt.date):
    y, m = a.year, a.month
    while (y, m) <= (b.year, b.month):
        yield dt.date(y, m, 1)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def month_end(d: dt.date) -> dt.date:
    return (dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1) - dt.timedelta(days=1))


# ---------------------------------------------------------------- fetchers

def fetch_taiex_turnover(st: State, start: dt.date, today: dt.date):
    """加權指數 OHLC＋成交金額，月查詢。已抓完的整月不重抓；當月永遠重抓（會更新到最新一天）。"""
    taiex, turn = Store("taiex"), Store("turnover")
    n_new = 0
    for ms in month_starts(start, today):
        ym = ms.strftime("%Y-%m")
        complete = month_end(ms) < today
        if complete and st.month_done("taiex", ym) and st.month_done("turnover", ym):
            continue
        d1 = ms.strftime("%Y%m01")
        a = parse_taiex_month(twse_json("TAIEX/MI_5MINS_HIST", {"date": d1}))
        b = parse_turnover_month(twse_json("afterTrading/FMTQIK", {"date": d1}))
        for r in a:
            n_new += taiex.add(r)
        for r in b:
            n_new += turn.add(r)
        if complete and a and b:
            st.mark_month("taiex", ym)
            st.mark_month("turnover", ym)
        if complete and not (a and b):
            # 整月無資料（例如超出歷史範圍）：記為已查，避免每天重抓
            st.mark_month("taiex", ym)
            st.mark_month("turnover", ym)
        st.save()
    log(f"taiex/turnover：新增/更新 {n_new} 筆；taiex 至 {taiex.last()}，turnover 至 {turn.last()}")


def missing_trading_days(store: Store, series: str, st: State, start: dt.date, today: dt.date,
                         recent_only_days: int | None) -> list[str]:
    cal = Store("taiex").dates()
    lo = start.isoformat()
    if recent_only_days is not None:
        lo = max(lo, (today - dt.timedelta(days=recent_only_days)).isoformat())
    out = []
    for d in cal:
        if d < lo or d > today.isoformat() or store.has(d):
            continue
        age = (today - dt.date.fromisoformat(d)).days
        if st.gap_attempts(series, d) >= 3 and age > 5:
            continue          # 多次查無資料且已非近期：視為該日無此資料，不再重抓
        out.append(d)
    return out


def fetch_daily_twse(which: list[str], st: State, start: dt.date, today: dt.date,
                     backfill: bool, limit: int | None):
    """逐日抓 inst / margin；最新日優先，這樣回補中途頁面也已有近期資料。"""
    stores = {"inst": Store("inst"), "margin": Store("margin")}
    todo = {s: missing_trading_days(stores[s], s, st, start, today, None if backfill else 45) for s in which}
    for s in which:
        log(f"{s}：待抓 {len(todo[s])} 天")
    all_dates = sorted(set(d for s in which for d in todo[s]), reverse=True)
    if limit:
        all_dates = all_dates[:limit]
    fails = 0
    n = 0
    for d in all_dates:
        d8 = d.replace("-", "")
        for s in which:
            if d not in todo[s]:
                continue
            try:
                if s == "inst":
                    row = parse_bfi82u(twse_json("fund/BFI82U", {"type": "day", "dayDate": d8}), d)
                else:
                    row = parse_margn(twse_json("marginTrading/MI_MARGN", {"date": d8, "selectType": "MS"}), d)
            except Blocked as e:
                fails += 1
                log(f"FAIL {s} {d}：{e}")
                if fails >= 3:
                    log("連續失敗 3 次，停止本輪（下次續跑）。")
                    st.save()
                    return
                continue
            fails = 0
            if row is None:
                st.bump_gap(s, d)
                log(f"  {s} {d} 查無資料（第 {st.gap_attempts(s, d)} 次）")
            else:
                stores[s].add(row)
                n += 1
        if n and n % 50 == 0:
            st.save()
            log(f"  ...已抓 {n} 筆，目前到 {d}")
    st.save()
    log(f"inst/margin：本輪新增 {n} 筆")


def fetch_sbl(st: State, start: dt.date, today: dt.date, backfill: bool, limit: int | None):
    """逐日抓借券：TWT72U（上市借券餘額，官方金額彙總＋各股收盤價）＋TWT93U（各股借券賣出餘額股數）。
    兩個都抓到才寫一行；最新日優先；每天 2 次請求。"""
    store = Store("sbl")
    todo = missing_trading_days(store, "sbl", st, start, today, None if backfill else 45)
    log(f"sbl：待抓 {len(todo)} 天")
    todo = sorted(todo, reverse=True)
    if limit:
        todo = todo[:limit]
    fails = n = 0
    for d in todo:
        d8 = d.replace("-", "")
        try:
            lend = parse_lending_total(twse_json("lending/TWT72U", {"date": d8, "selectType": "SLBNLB"}), d)
            short = parse_short_balance(twse_json("marginTrading/TWT93U", {"date": d8}), d, lend["px"]) \
                if lend else None
        except Blocked as e:
            fails += 1
            log(f"FAIL sbl {d}：{e}")
            if fails >= 3:
                log("連續失敗 3 次，停止本輪（下次續跑）。")
                st.save()
                return
            continue
        fails = 0
        if lend is None or short is None:
            st.bump_gap("sbl", d)
            log(f"  sbl {d} 查無資料（第 {st.gap_attempts('sbl', d)} 次）")
            continue
        store.add({"d": d, "lend_sh": lend["lend_sh"], "lend_amt": lend["lend_amt"], **short})
        n += 1
        if n % 50 == 0:
            st.save()
            log(f"  ...已抓 {n} 筆，目前到 {d}")
    st.save()
    log(f"sbl：本輪新增 {n} 筆；最新 {store.last()}")


def fetch_mktcap(start: dt.date):
    """證交所『市值週報』：一個 zip 含 2005-09 起每週末的上市股票總市值（億元），整檔下載、每次覆蓋。"""
    store = Store("mktcap")
    j = twse_json("statisticsWeek/index", {})
    url = None
    for row in j.get("data") or []:
        if len(row) >= 2 and str(row[1]).endswith(".zip"):
            url = row[1]
    if not url:
        raise Blocked("市值週報：找不到 zip 連結")
    import zipfile
    last_err = ""
    for wait in [0] + BACKOFF:
        if wait:
            time.sleep(wait)
        _twse_throttle.wait()
        try:
            r = _session.get("https://www.twse.com.tw" + url, timeout=60)
            if r.status_code != 200:
                last_err = f"HTTP {r.status_code}"
                continue
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                name = next(n for n in z.namelist() if n.lower().endswith(".xls"))
                rows = parse_mktcap_xls(z.read(name))
            break
        except (requests.RequestException, zipfile.BadZipFile, StopIteration) as e:
            last_err = type(e).__name__
    else:
        raise Blocked(f"市值週報下載失敗：{last_err}")
    n = 0
    for row in rows:
        if row["d"] >= (start - dt.timedelta(days=45)).isoformat():
            n += store.add(row)
    log(f"mktcap：新增/更新 {n} 筆；最新 {store.last()}")


def _taifex_window(today: dt.date) -> dt.date:
    """期交所網站只提供近 3 年，起點取 3 年前＋1 天。"""
    try:
        return today.replace(year=today.year - 3) + dt.timedelta(days=1)
    except ValueError:      # 2/29
        return today.replace(year=today.year - 3, day=28) + dt.timedelta(days=1)


def _chunks(a: dt.date, b: dt.date, days: int):
    """切查詢區間。days>0＝每段最多 days 天；days<=0＝依曆月切（每段不跨月）。
    dlFutDataDown 的區間上限是『起日起算一個曆月』，固定 30 天會在跨 2 月的段被整段拒絕（回空檔），所以用曆月切。"""
    cur = a
    while cur <= b:
        end = min(month_end(cur) if days <= 0 else cur + dt.timedelta(days=days - 1), b)
        yield cur, end
        cur = end + dt.timedelta(days=1)


def _fmt(d: dt.date) -> str:
    return d.strftime("%Y/%m/%d")


def fetch_range_csv(name: str, endpoint: str, extra: dict, parser, start: dt.date, today: dt.date,
                    chunk_days: int, floor: dt.date | None = None):
    """通用：依區間分段 POST 下載 CSV → parser → Store。從 max(start, floor, 最後一筆日期) 開始。"""
    store = Store(name)
    a = max(start, floor or start)
    # 日常模式：從已有最後日往前多抓 3 天（涵蓋修正與休市日），回補模式：缺口由 start 起掃
    if store.last() and not os.environ.get("TWCHIPS_FULL_SCAN"):
        a = max(a, dt.date.fromisoformat(store.last()) - dt.timedelta(days=3))
    n = 0
    for c0, c1 in _chunks(a, today, chunk_days):
        # 迄日若超過期交所當天已公布的最後一日會整段被拒（DateTime error）：最後一段往前退幾天再試
        for back in range(0, 5 if c1 == today else 1):
            e = c1 - dt.timedelta(days=back)
            if e < c0:
                break
            text = taifex_post(endpoint, {"queryStartDate": _fmt(c0), "queryEndDate": _fmt(e), **extra})
            rows = parser(text)
            if rows:
                for r in rows:
                    n += store.add(r)
                break
        else:
            if (e - c0).days >= 6 and c1 < today - dt.timedelta(days=10):
                log(f"  警告：{name} {c0}～{c1} 回空檔（可能被區間規則拒絕或當期無資料）")
    log(f"{name}：新增/更新 {n} 筆；最早 {min(store.rows) if store.rows else None}，最新 {store.last()}")


def fetch_finmind_backfill(name: str, dataset: str, id_key: str, id_val: str, conv,
                           until: dt.date):
    """FinMind 補期交所網站 3 年窗口以外的舊資料（2018-06-05 起）；只補還沒有的日子。"""
    store = Store(name)
    if store.rows and min(store.rows) <= "2018-06-06":
        return          # 已補過
    end = until - dt.timedelta(days=1)
    if end < FINMIND_START:
        return
    r = _session.get("https://api.finmindtrade.com/api/v4/data",
                     params={"dataset": dataset, "start_date": FINMIND_START.isoformat(),
                             "end_date": end.isoformat(), id_key: id_val}, timeout=180)
    r.raise_for_status()
    data = r.json().get("data") or []
    n = 0
    for row in conv(data):
        if not store.has(row["d"]):
            n += store.add(row)
    log(f"{name}（FinMind 補舊資料）：新增 {n} 筆，最早 {min(store.rows) if store.rows else None}")


def fetch_fut_inst(start, today, backfill):
    win = _taifex_window(today)
    fetch_range_csv("fut_inst", "futContractsDateDown", {"commodityId": "TXF"}, parse_fut_inst_csv,
                    max(start, win), today, 360, floor=win)
    if backfill:
        s = Store("fut_inst")
        first_taifex = min([d for d in s.rows if d >= win.isoformat()] or [today.isoformat()])
        fetch_finmind_backfill("fut_inst", "TaiwanFuturesInstitutionalInvestors", "data_id", "TX",
                               finmind_fut_rows, dt.date.fromisoformat(first_taifex))


def fetch_opt_inst(start, today, backfill):
    win = _taifex_window(today)
    fetch_range_csv("opt_inst", "callsAndPutsDateDown", {"commodityId": "TXO"}, parse_opt_inst_csv,
                    max(start, win), today, 360, floor=win)
    if backfill:
        s = Store("opt_inst")
        first_taifex = min([d for d in s.rows if d >= win.isoformat()] or [today.isoformat()])
        fetch_finmind_backfill("opt_inst", "TaiwanOptionInstitutionalInvestors", "data_id", "TXO",
                               finmind_opt_rows, dt.date.fromisoformat(first_taifex))


def fetch_pcr(start, today, backfill):
    fetch_range_csv("pcr", "pcRatioDown", {}, parse_pcr_csv, start, today, 28)


def fetch_large(start, today, backfill):
    fetch_range_csv("large", "largeTraderFutDown", {}, parse_large_csv, start, today, 28)


def fetch_mtx_inst(start, today, backfill):
    win = _taifex_window(today)
    fetch_range_csv("mtx_inst", "futContractsDateDown", {"commodityId": "MXF"},
                    lambda t: parse_fut_inst_csv(t, "小型臺指期貨"), max(start, win), today, 360, floor=win)
    if backfill:
        s = Store("mtx_inst")
        first_taifex = min([d for d in s.rows if d >= win.isoformat()] or [today.isoformat()])
        fetch_finmind_backfill("mtx_inst", "TaiwanFuturesInstitutionalInvestors", "data_id", "MTX",
                               lambda data: finmind_fut_rows(data, "MTX"), dt.date.fromisoformat(first_taifex))


def fetch_tmf_inst(start, today, backfill):
    """微型臺指期貨 2024-07-29 上市，期交所 3 年窗口已涵蓋全部歷史，不需要 FinMind。"""
    win = max(_taifex_window(today), TMF_START)
    fetch_range_csv("tmf_inst", "futContractsDateDown", {"commodityId": "TMF"},
                    lambda t: parse_fut_inst_csv(t, "微型臺指期貨"), max(start, win), today, 360, floor=win)


def fetch_fut_daily(name: str, prod: str, parser, start: dt.date, today: dt.date):
    """期交所『期貨每日交易行情』dlFutDataDown：一次最多一個曆月，依曆月逐段補。"""
    fetch_range_csv(name, "dlFutDataDown", {"down_type": "1", "commodity_id": prod}, parser, start, today, 0)


def _oi_only(text: str) -> list[dict]:
    return [{"d": r["d"], "oi": r["oi"], "oi_wk": r["oi_wk"]} for r in parse_fut_daily_csv(text)]


def fetch_mtx_mkt(start, today, backfill):
    fetch_fut_daily("mtx_mkt", "MTX", _oi_only, start, today)


def fetch_tmf_mkt(start, today, backfill):
    fetch_fut_daily("tmf_mkt", "TMF", _oi_only, max(start, TMF_START), today)


def fetch_tx_daily(start, today, backfill):
    fetch_fut_daily("tx_daily", "TX", lambda t: [{"d": r["d"], "m": r["m"]} for r in parse_fut_daily_csv(t)],
                    start, today)


def fetch_vix(today: dt.date):
    """臺指選擇權波動率指數：官網每月一個 txt，只留最近約 4 個月（更早的月份檔已下架），
    所以這條序列的最早日就是我們開始抓的那個月，之後每天累積。"""
    store = Store("vix")
    n = 0
    seen = []
    for k in range(6):                       # 本月往前 6 個月，抓得到的就收
        y, m = today.year, today.month - k
        while m <= 0:
            y, m = y - 1, m + 12
        ym = f"{y:04d}{m:02d}"
        _taifex_throttle.wait()
        try:
            r = _session.get(VIX_URL.format(ym=ym), timeout=60)
        except requests.RequestException as e:
            log(f"  VIX {ym} 失敗：{type(e).__name__}")
            continue
        text = r.content.decode("cp950", errors="replace")
        if r.status_code != 200 or "<html" in text[:300].lower():
            continue                         # 月檔不存在（已下架或還沒到）
        rows = parse_vix_txt(text)
        seen.append(ym)
        for row in rows:
            n += store.add(row)
    log(f"vix：新增/更新 {n} 筆（讀到月檔 {sorted(seen)}）；最早 {min(store.rows) if store.rows else None}，最新 {store.last()}")


def fetch_daily_series(series: str, st: State, start: dt.date, today: dt.date, backfill: bool,
                       limit: int | None, getter):
    """通用逐日抓取（單一序列）：缺的交易日、最新日優先、連續 3 次被擋就停、查無資料記 gap。"""
    store = Store(series)
    todo = sorted(missing_trading_days(store, series, st, start, today, None if backfill else 45), reverse=True)
    log(f"{series}：待抓 {len(todo)} 天")
    if limit:
        todo = todo[:limit]
    fails = n = 0
    for d in todo:
        try:
            row = getter(d)
        except Blocked as e:
            fails += 1
            log(f"FAIL {series} {d}：{e}")
            if fails >= 3:
                log("連續失敗 3 次，停止本輪（下次續跑）。")
                st.save()
                return
            continue
        fails = 0
        if row is None:
            st.bump_gap(series, d)
            log(f"  {series} {d} 查無資料（第 {st.gap_attempts(series, d)} 次）")
            continue
        store.add(row)
        n += 1
        if n % 50 == 0:
            st.save()
            log(f"  ...已抓 {n} 筆，目前到 {d}")
    st.save()
    log(f"{series}：本輪新增 {n} 筆；最新 {store.last()}")


def fetch_dtrade(st, start, today, backfill, limit):
    fetch_daily_series("dtrade", st, start, today, backfill, limit,
                       lambda d: parse_dtrade(twse_json("dayTrading/TWTB4U", {"date": d.replace("-", "")}), d))


def fetch_otc_inst(st, start, today, backfill, limit):
    fetch_daily_series("otc_inst", st, max(start, OTC_INST_START), today, backfill, limit,
                       lambda d: parse_tpex_inst(tpex_json("insti/summary", {
                           "type": "Daily", "date": d.replace("-", "/"), "id": ""}), d))


def fetch_otc_margin(st, start, today, backfill, limit):
    fetch_daily_series("otc_margin", st, start, today, backfill, limit,
                       lambda d: parse_tpex_margin(tpex_json("margin/balance", {
                           "date": d.replace("-", "/"), "id": ""}), d))


def fetch_usdtwd(start, today, backfill):
    store = Store("usdtwd")
    r = None
    for attempt in range(4):      # FRED 偶爾慢，讀取逾時就重試
        try:
            # FRED 對瀏覽器 UA 會逾時，用 requests 預設 UA
            r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv", params={"id": "DEXTAUS"}, timeout=90)
            r.raise_for_status()
            break
        except requests.RequestException as e:
            log(f"  FRED 第 {attempt + 1} 次失敗：{type(e).__name__}")
            time.sleep(10 * (attempt + 1))
    else:
        raise Blocked("FRED DEXTAUS 重試用盡")
    n = 0
    for row in parse_fred_csv(r.text):
        if row["d"] >= start.isoformat():
            n += store.add(row)
    log(f"usdtwd：新增/更新 {n} 筆；最新 {store.last()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backfill", action="store_true", help="回補 10 年（2016-10 起），可續跑")
    ap.add_argument("--only", default="", help="逗號分隔：" + ",".join(SERIES))
    ap.add_argument("--limit", type=int, default=0, help="逐日 TWSE 序列最多抓幾天（測試用）")
    args = ap.parse_args()

    only = [s for s in args.only.split(",") if s] or SERIES
    unknown = set(only) - set(SERIES)
    if unknown:
        sys.exit(f"未知序列：{unknown}")
    today = today_tpe()
    start = START
    st = State()
    failed = []

    def run(label, fn, *a):
        try:
            fn(*a)
        except Blocked as e:
            failed.append(label)
            log(f"FAIL {label}：{e}")
        except Exception as e:   # 單一序列失敗不影響其他序列
            failed.append(label)
            log(f"FAIL {label}：{type(e).__name__}: {e}")

    if {"taiex", "turnover"} & set(only) or {"inst", "margin", "sbl", "dtrade", "otc_inst", "otc_margin"} & set(only):
        run("taiex/turnover", fetch_taiex_turnover, st, TAIEX_START, today)
    daily = [s for s in ("inst", "margin") if s in only]
    if daily:
        run("inst/margin", fetch_daily_twse, daily, st, start, today, args.backfill, args.limit or None)
    if "sbl" in only:
        run("sbl", fetch_sbl, st, start, today, args.backfill, args.limit or None)
    if "mktcap" in only:
        run("mktcap", fetch_mktcap, start)
    if "fut_inst" in only:
        run("fut_inst", fetch_fut_inst, start, today, args.backfill)
    if "opt_inst" in only:
        run("opt_inst", fetch_opt_inst, start, today, args.backfill)
    if "pcr" in only:
        run("pcr", fetch_pcr, start, today, args.backfill)
    if "large" in only:
        run("large", fetch_large, start, today, args.backfill)
    if "usdtwd" in only:
        run("usdtwd", fetch_usdtwd, start, today, args.backfill)
    if "mtx_inst" in only:
        run("mtx_inst", fetch_mtx_inst, start, today, args.backfill)
    if "tmf_inst" in only:
        run("tmf_inst", fetch_tmf_inst, start, today, args.backfill)
    if "mtx_mkt" in only:
        run("mtx_mkt", fetch_mtx_mkt, start, today, args.backfill)
    if "tmf_mkt" in only:
        run("tmf_mkt", fetch_tmf_mkt, start, today, args.backfill)
    if "tx_daily" in only:
        run("tx_daily", fetch_tx_daily, start, today, args.backfill)
    if "vix" in only:
        run("vix", fetch_vix, today)
    if "dtrade" in only:
        run("dtrade", fetch_dtrade, st, start, today, args.backfill, args.limit or None)
    if "otc_inst" in only:
        run("otc_inst", fetch_otc_inst, st, start, today, args.backfill, args.limit or None)
    if "otc_margin" in only:
        run("otc_margin", fetch_otc_margin, st, start, today, args.backfill, args.limit or None)

    if args.backfill:       # 回補完整理檔案：依日期排序、每日一行
        for s in only:
            if (DATA / f"{s}.jsonl").exists():
                Store(s).compact()
    log("完成。" + (f" 失敗：{failed}" if failed else ""))
    if len(failed) >= 3:
        sys.exit(1)


if __name__ == "__main__":
    main()
