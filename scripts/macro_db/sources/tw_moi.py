"""內政部。

kind=statis：statis.moi.gov.tw/micst/webMain.aspx 統計資料庫 CSV（UTF-8 BOM，民國年）。
  列標籤：「115年 8月/ 區域別總計/ 買賣」或「115年 8月/ 區域別總計」；「115年/ …」是年度合計列，略過。
  params: url, label（月份之後的列標籤，如「區域別總計/ 買賣」）, col（0 起算，0＝列標籤）

kind=hpi_pdf：不動產資訊平台「表2 全國及六都住宅價格指數」PDF（季，基期 105 年＝100）。
  用 pdftotext -layout（poppler-utils）轉文字後逐列解析：「115 年第 1 季  143.85  139.79 ...」。
  params: url, col（1＝全國、2＝新北、3＝臺北、4＝桃園、5＝臺中、6＝臺南、7＝高雄；依 PDF 表頭）
  PDF 結構一變就會壞：表頭欄名與預期不符時回錯誤，不會悄悄抓錯欄。
"""
from __future__ import annotations

import csv
import io
import re
import shutil
import subprocess

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C

HPI_HEADER = ["全國", "新北市", "臺北市", "桃園市", "臺中市", "臺南市", "高雄市"]


def parse_statis(text: str, label: str, col: int) -> list:
    out = []
    pat = re.compile(r"^\s*(\d{1,3}年\s*\d{1,2}月)/\s*" + re.escape(label) + r"\s*$")
    for r in csv.reader(io.StringIO(text)):
        if not r or col >= len(r):
            continue
        m = pat.match(r[0])
        if m:
            out.append((C.roc_label_to_date(m.group(1)), r[col]))
    return C.clean_obs(out)


def pdf_to_text(pdf: bytes) -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        raise RuntimeError("找不到 pdftotext（需安裝 poppler-utils）")
    p = subprocess.run([exe, "-layout", "-", "-"], input=pdf, capture_output=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError("pdftotext 失敗：" + p.stderr.decode("utf-8", "replace")[:200])
    return p.stdout.decode("utf-8", errors="replace")


def parse_hpi_text(text: str, col: int) -> list:
    # 表頭驗證：欄名順序必須是 全國 新北市 臺北市 桃園市 臺中市 臺南市 高雄市
    head = None
    for line in text.splitlines():
        if "全國" in line and "新北" in line:
            head = re.findall(r"[^\s]+", line.replace("縣市", " "))
            break
    if head != HPI_HEADER:
        raise ValueError(f"住宅價格指數 PDF 表頭與預期不符：{head}")
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*(\d{2,3})\s*年第\s*([1-4])\s*季\s+(.*)$", line)
        if not m:
            continue
        nums = re.findall(r"-?\d+(?:\.\d+)?", m.group(3))
        if len(nums) != len(HPI_HEADER):
            raise ValueError(f"列欄數 {len(nums)} 不是 7：{line.strip()[:60]}")
        out.append((C.d_quarter(int(m.group(1)) + 1911, int(m.group(2))), nums[col - 1]))
    return C.clean_obs(out)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s: dict):
        p = C.params(s)
        raw = C.http_get_cached(cache, p["url"])
        if p.get("kind") == "hpi_pdf":
            key = ("pdftext", p["url"])
            if key not in cache:
                cache[key] = pdf_to_text(raw)
            return parse_hpi_text(cache[key], int(p["col"]))
        return parse_statis(raw.decode("utf-8-sig", errors="replace"), p["label"], int(p["col"]))

    return C.run_specs(specs, one)
