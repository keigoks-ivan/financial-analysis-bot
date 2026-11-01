#!/usr/bin/env python3
"""抓 AAII 投資人情緒調查（週）與 NAAIM Exposure Index（週），輸出 CSV。

用法：
    python3 fetch_sentiment.py [--out-dir DIR] [--only aaii|naaim]

來源（皆不需 cookie／登入／瀏覽器 session，一般 User-Agent 即可）：
  AAII : https://www.aaii.com/files/surveys/sentiment.xls   （BIFF .xls，需 xlrd：pip install xlrd）
  NAAIM: 先用 WordPress REST 媒體庫找最新的 USE_Data-since-Inception_*.xlsx
         https://naaim.org/wp-json/wp/v2/media?search=USE_Data&orderby=date&order=desc
         再下載該 xlsx（只用標準函式庫解析）

行為：增量更新（新資料依日期覆蓋舊資料）、由舊到新、原子寫檔；任一來源失敗時保留舊檔、
該來源以非 0 結束碼回報，另一來源照跑。
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import tempfile
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
AAII_URL = "https://www.aaii.com/files/surveys/sentiment.xls"
NAAIM_MEDIA_API = ("https://naaim.org/wp-json/wp/v2/media?search=USE_Data"
                   "&orderby=date&order=desc&per_page=5&_fields=date,source_url")
DEFAULT_OUT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "crowding_monitor"))

AAII_COLS = ["date", "bullish", "neutral", "bearish", "spread"]
NAAIM_COLS = ["date", "mean_exposure", "bearish_min", "quart1", "quart2", "quart3",
              "bullish_max", "deviation", "naaim_number", "sp500"]


def http_get(url, timeout=60, tries=3):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f"下載失敗 {url}: {last}")


def excel_date(serial):
    return (dt.date(1899, 12, 30) + dt.timedelta(days=int(serial))).isoformat()


def read_csv(path, cols):
    if not os.path.exists(path):
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {r["date"]: {c: r.get(c, "") for c in cols} for r in csv.DictReader(f)}


def write_csv_atomic(path, cols, rows_by_date):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for d in sorted(rows_by_date):
            w.writerow(rows_by_date[d])
    os.replace(tmp, path)


def fmt(x, nd=2):
    return "" if x is None else f"{round(x, nd):.{nd}f}".rstrip("0").rstrip(".") if nd else str(x)


# ---------------------------------------------------------------- AAII
def parse_aaii(blob):
    try:
        import xlrd  # noqa: WPS433
    except ImportError as e:
        raise RuntimeError("需要 xlrd（pip install xlrd）才能讀 AAII 的 .xls") from e
    book = xlrd.open_workbook(file_contents=blob)
    sh = book.sheet_by_name("SENTIMENT")
    # 欄位：0 Date,1 Bullish,2 Neutral,3 Bearish（小數 0~1）
    out = {}
    for i in range(sh.nrows):
        c = sh.row(i)
        if len(c) < 4 or c[0].ctype != 3:  # 3 = XL_CELL_DATE
            continue
        if not all(c[k].ctype == 2 for k in (1, 2, 3)):  # 數字
            continue
        bull, neu, bear = (c[k].value * 100 for k in (1, 2, 3))
        d = excel_date(c[0].value)
        out[d] = {"date": d, "bullish": fmt(bull), "neutral": fmt(neu),
                  "bearish": fmt(bear), "spread": fmt(bull - bear)}
    if len(out) < 1500:
        raise RuntimeError(f"AAII 解析列數異常：{len(out)}")
    return out


def run_aaii(out_dir):
    path = os.path.join(out_dir, "aaii_weekly.csv")
    new = parse_aaii(http_get(AAII_URL))
    old = read_csv(path, AAII_COLS)
    old.update(new)
    write_csv_atomic(path, AAII_COLS, old)
    return path, old


# ---------------------------------------------------------------- NAAIM
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def parse_xlsx_first_sheet(blob):
    z = zipfile.ZipFile(io.BytesIO(blob))
    sst = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            sst.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    rows = []
    for r in sheet.iter("{%s}row" % NS["m"]):
        row = {}
        for c in r.findall("m:c", NS):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            v = c.find("m:v", NS)
            if v is None:
                continue
            row[col] = sst[int(v.text)] if c.get("t") == "s" else v.text
        rows.append(row)
    return rows


def parse_naaim(blob):
    rows = parse_xlsx_first_sheet(blob)
    hdr = rows[0]
    want = {"Date": "date", "Mean/Average": "mean_exposure", "Most Bearish Response": "bearish_min",
            "Quart 1 (25% at/below)": "quart1", "Quart 2 (median)": "quart2",
            "Quart 3 (25% at/above)": "quart3", "Most Bullish Response": "bullish_max",
            "Standard Deviation": "deviation", "NAAIM Number": "naaim_number", "S&P 500": "sp500"}
    colmap = {k: want[v] for k, v in hdr.items() if v in want}
    if "date" not in colmap.values():
        raise RuntimeError(f"NAAIM 表頭異常：{hdr}")
    out = {}
    for row in rows[1:]:
        rec = {c: "" for c in NAAIM_COLS}
        for k, name in colmap.items():
            if k in row and row[k] != "":
                rec[name] = row[k]
        try:
            d = excel_date(float(rec["date"]))
        except ValueError:
            continue
        rec["date"] = d
        for name in NAAIM_COLS[1:]:
            if rec[name] != "":
                rec[name] = fmt(float(rec[name]), 4)
        out[d] = rec  # 檔尾偶有重複日期，後面的覆蓋前面
    if len(out) < 800:
        raise RuntimeError(f"NAAIM 解析列數異常：{len(out)}")
    return out


def run_naaim(out_dir):
    path = os.path.join(out_dir, "naaim_weekly.csv")
    meta = json.loads(http_get(NAAIM_MEDIA_API))
    urls = [m["source_url"] for m in meta if "USE_Data-since-Inception" in m.get("source_url", "")]
    if not urls:
        raise RuntimeError("媒體庫找不到 USE_Data-since-Inception xlsx")
    new = parse_naaim(http_get(urls[0]))
    old = read_csv(path, NAAIM_COLS)
    old.update(new)
    write_csv_atomic(path, NAAIM_COLS, old)
    return path, old, urls[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=DEFAULT_OUT)
    ap.add_argument("--only", choices=["aaii", "naaim"])
    a = ap.parse_args()
    fail = 0
    for name, fn in (("aaii", run_aaii), ("naaim", run_naaim)):
        if a.only and a.only != name:
            continue
        try:
            res = fn(a.out_dir)
            rows = res[1]
            ds = sorted(rows)
            extra = f" 來源 {res[2]}" if len(res) > 2 else ""
            print(f"[{name}] OK {res[0]} 列數={len(ds)} 首筆={ds[0]} 末筆={ds[-1]}{extra}")
        except Exception as e:  # noqa: BLE001
            fail += 1
            print(f"[{name}] 失敗（保留舊檔）：{e}", file=sys.stderr)
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
