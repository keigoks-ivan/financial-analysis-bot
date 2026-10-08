"""日本銀行 時系列統計データ検索サイト API（免金鑰）。

https://www.stat-search.boj.or.jp/api/v1/getDataCode?format=csv&lang=en&db=<DB>&code=<碼1,碼2,...>
同一資料庫（db）的多條序列合併成一次請求（上限 250 條、6 萬筆；超過時用 NEXTPOSITION 續抓）。
CSV 欄位：SERIES_CODE,NAME_OF_TIME_SERIES,UNIT,FREQUENCY,CATEGORY,LAST_UPDATE,SURVEY_DATES,VALUES
VALUES 為 null 代表缺值（略過）。

params: db, code, scale（選填，乘上去；預設 1）, url（只給 probe 用）
另有 kind=cpirev：日銀「基本通貨膨脹率」cpirev.xlsx（固定網址，每月更新；sheet chart，第 1 欄日期）。
  params: url, cols（0 起算欄位，新基準在前：25 年基準、20 年基準、15 年基準…）, col_label（第 2 列表頭應含的字串）
  每個月取新基準欄第一個有值者；新基準只涵蓋近期，早年由舊基準欄補。

日期：
  DAILY      YYYYMMDD -> 該日
  MONTHLY    YYYYMM   -> 當月 1 日
  QUARTERLY  YYYYQQ   -> 季首月 1 日（短觀：01=3 月調查、02=6 月、03=9 月、04=12 月，都落在對應日曆季）
  其他頻率（年、半年）不支援，會回報錯誤。
"""
from __future__ import annotations

import csv
import io
import time

import datetime as dt

from ._http import get
from .jp_common import Cache, compact, d_month, d_quarter, num, run_specs, xlsx_sheets

API = "https://www.stat-search.boj.or.jp/api/v1/getDataCode"
MAX_CODES = 250


def to_date(code_freq: str, s: str) -> str:
    s = s.strip()
    f = code_freq.upper()
    if f == "DAILY" and len(s) == 8:
        return "%s-%s-%s" % (s[:4], s[4:6], s[6:8])
    if f.startswith("MONTHLY") and len(s) == 6:
        return d_month(s[:4], s[4:6])
    if f.startswith("QUARTERLY") and len(s) == 6:
        return d_quarter(s[:4], s[4:6])
    raise ValueError("不支援的頻率／日期格式：%s %s" % (code_freq, s))


def parse(text: str):
    """BOJ CSV -> ({code: [(date, float)]}, next_position 或 None)。STATUS 非 200 丟例外。"""
    rows = list(csv.reader(io.StringIO(text)))
    if not rows or rows[0][0] != "STATUS":
        raise ValueError("BOJ 回傳不是預期的 CSV：%r" % text[:80])
    if rows[0][1].strip() != "200":
        msg = next((r[1] for r in rows if r and r[0] == "MESSAGE"), "")
        raise ValueError("BOJ API STATUS=%s %s" % (rows[0][1], msg))
    nxt = None
    out: dict = {}
    start = None
    for i, r in enumerate(rows):
        if r and r[0] == "NEXTPOSITION" and len(r) > 1 and r[1].strip():
            nxt = int(r[1])
        if r and r[0] == "SERIES_CODE":
            start = i
            break
    if start is None:
        return out, nxt
    for r in rows[start + 1:]:
        if len(r) < 8:
            continue
        v = num(r[-1]) if r[-1] != "null" else None
        out.setdefault(r[0], [])
        if v is None:
            continue
        out[r[0]].append((to_date(r[3], r[6]), v))
    return out, nxt


def request(db: str, codes: list) -> dict:
    """一個 db 的多條序列；NEXTPOSITION 續抓。回傳 {code: obs}。"""
    res: dict = {}
    pos = None
    for _ in range(40):
        params = {"format": "csv", "lang": "en", "db": db, "code": ",".join(codes)}
        if pos:
            params["startPosition"] = pos
        text = get(API, params=params)
        part, nxt = parse(text)
        for k, v in part.items():
            res.setdefault(k, []).extend(v)
        if not nxt:
            return res
        pos = nxt
        time.sleep(0.5)
    raise RuntimeError("BOJ 續抓超過 40 次")


def cpirev_obs(rows, cols, col_label) -> list:
    hdr = rows[1]
    for c in cols:
        if c >= len(hdr) or compact(col_label) not in compact(hdr[c]):
            raise ValueError("cpirev 第 %d 欄表頭應含「%s」，實為「%s」（欄位順序可能已改版）"
                             % (c, col_label, compact(hdr[c])[:30] if c < len(hdr) else "(超出範圍)"))
    out = []
    for r in rows[5:]:
        if r and isinstance(r[0], (dt.datetime, dt.date)):
            for c in cols:
                v = num(r[c]) if c < len(r) else None
                if v is not None:
                    out.append((d_month(r[0].year, r[0].month), v))
                    break
    return out


def fetch_cpirev(specs):
    cache = Cache()

    def one(s):
        p = s["params"]
        sheets = xlsx_sheets(cache.get_url(p["url"]))
        return cpirev_obs(sheets["chart"], p["cols"], p["col_label"])
    return run_specs(specs, one)


def fetch(specs):
    result = {}
    special = [s for s in specs if s["params"].get("kind") == "cpirev"]
    if special:
        result.update(fetch_cpirev(special))
    specs = [s for s in specs if s["params"].get("kind") != "cpirev"]
    by_db: dict = {}
    for s in specs:
        by_db.setdefault(s["params"]["db"], []).append(s)
    for db, group in by_db.items():
        codes = sorted({s["params"]["code"] for s in group})
        data: dict = {}
        err = None
        try:
            for i in range(0, len(codes), MAX_CODES):
                data.update(request(db, codes[i:i + MAX_CODES]))
        except Exception as e:  # noqa: BLE001
            err = "%s：%s" % (type(e).__name__, e)
        for s in group:
            code = s["params"]["code"]
            obs = data.get(code)
            if obs:
                k = s["params"].get("scale", 1)
                result[s["sid"]] = {"obs": sorted(set((d, round(v * k, 6) if k != 1 else v) for d, v in obs))}
            else:
                result[s["sid"]] = {"error": (err or "BOJ 沒有回傳 %s/%s（代碼可能已變）" % (db, code))[:300]}
    return result
