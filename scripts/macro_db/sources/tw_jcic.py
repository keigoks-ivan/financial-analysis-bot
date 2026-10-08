"""金融聯合徵信中心（JCIC）銀行局開放資料 CSV（UTF-8 BOM，西元年）。

欄：年, 月, <分類欄>, 人數, 授信餘額[仟元], 平均利率[%]
- Mortgage_Institution.CSV／NewMortgage_Institution.CSV：分類欄＝聯徵中心會員分類（取「A全體銀行」）
- NewMortgage_Location.CSV：分類欄＝擔保品所在縣市別（A台北市、F新北市、H桃園市、B台中市、D台南市、E高雄市）
- building_amt.csv：年, 月, 地區別, 貸款餘額[仟元]
分類字串帶全形空白，比對前先 strip（含全形空白）。
params: url, group（分類欄要等於的字串；比對時兩邊都 strip）, value（取值欄名）
"""
from __future__ import annotations

import csv
import io

try:
    from . import tw_common as C
except ImportError:
    import tw_common as C


def _norm(s: str) -> str:
    return (s or "").replace("　", " ").strip()


def parse(text: str, group: str, value: str) -> list:
    rows = list(csv.reader(io.StringIO(text)))
    hdr = [_norm(h) for h in rows[0]]
    for need in ("年", "月", value):
        if need not in hdr:
            raise KeyError(f"找不到欄「{need}」，表頭：{hdr}")
    iy, im, iv = hdr.index("年"), hdr.index("月"), hdr.index(value)
    ig = 2
    out = []
    for r in rows[1:]:
        if len(r) <= max(iy, im, iv, ig):
            continue
        if _norm(r[ig]) == _norm(group):
            out.append((C.d_month(r[iy], r[im]), r[iv]))
    return C.clean_obs(out)


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s: dict):
        p = C.params(s)
        raw = C.http_get_cached(cache, p["url"])
        return parse(raw.decode("utf-8-sig", errors="replace"), p["group"], p["value"])

    return C.run_specs(specs, one)
