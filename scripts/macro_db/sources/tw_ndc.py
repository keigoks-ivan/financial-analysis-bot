"""國家發展委員會（NDC）：景氣指標與燈號 ZIP、臺灣採購經理人指數（PMI／NMI，中華經濟研究院編製）。

下載網址含 GUID，每月更新會變，所以每次先問 data.gov.tw（dataset 6099＝ZIP、6100＝PMI CSV）。
params:
  kind: "zip"（預設）或 "csv"
  dataset: data.gov.tw 資料集 id；url: 寫死的備援網址
  member: ZIP 內的 CSV 檔名（kind=zip）
  col: 欄名（CSV 表頭）
  text_map: 選填，文字值轉數字（景氣燈號：藍1 黃藍2 綠3 黃紅4 紅5）
Date 欄為西元 YYYYMM。缺值為空白或「-」。
"""
from __future__ import annotations

import csv
import io
import zipfile

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C


def parse_table(text: str, col: str, text_map: dict | None = None) -> list:
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("CSV 沒有資料列")
    if col not in rows[0]:
        raise KeyError(f"CSV 找不到欄「{col}」，表頭：{list(rows[0])[:12]}")
    out = []
    for r in rows:
        d = C.period_to_date((r.get("Date") or "").strip())
        v = (r.get(col) or "").strip()
        if text_map is not None:
            v = text_map.get(v, v)
        out.append((d, v))
    return C.clean_obs(out)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}
    zips: dict = {}

    def one(s: dict):
        p = C.params(s)
        kind = p.get("kind", "zip")
        url = C.resolve_url(p.get("dataset"), cache, p["url"])
        raw = C.http_get_cached(cache, url)
        if kind == "zip":
            if url not in zips:
                zips[url] = zipfile.ZipFile(io.BytesIO(raw))
            text = zips[url].read(p["member"]).decode("utf-8-sig")
        else:
            text = raw.decode("utf-8-sig")
        return parse_table(text, p["col"], p.get("text_map"))

    return C.run_specs(specs, one)
