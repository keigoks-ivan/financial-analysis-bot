"""財務省貿易統計（海關通關統計）月別 CSV（Shift_JIS）。

https://www.customs.go.jp/toukei/suii/html/data/d41ma.csv（全世界）／d42ma001.csv（亞洲）／d42ma003.csv（北美）／d42ma010.csv（EU）
結構：第 3 列為欄名（Years/Months,Exp-Total,Imp-Total,Exp-304,Imp-304,...），之後每列 YYYY/MM，單位千日圓。
尚未發生的月份官方補 0，這裡把尾端連續的 0 去掉（不是缺值填 0，是還沒公布）。

params: url, col_name（例如 Exp-Total、Imp-304）, scale（選填，預設 1；千日圓 -> 億日圓 用 0.00001）
"""
from __future__ import annotations

import re

from .jp_common import Cache, csv_rows, d_month, num, run_specs


def customs_obs(raw: bytes, col_name: str, scale: float = 1.0) -> list:
    rows = csv_rows(raw, "cp932")
    hi = next((i for i, r in enumerate(rows) if r and r[0].strip() == "Years/Months"), None)
    if hi is None:
        raise ValueError("找不到欄名列（Years/Months）")
    names = [c.strip() for c in rows[hi]]
    if col_name not in names:
        raise ValueError("欄名 %s 不在檔內（欄位順序可能已改版）" % col_name)
    c = names.index(col_name)
    pts = []
    for r in rows[hi + 1:]:
        m = re.match(r"^(\d{4})/(\d{2})$", (r[0] if r else "").strip())
        if m and c < len(r):
            v = num(r[c])
            if v is not None:
                pts.append((d_month(m.group(1), m.group(2)), round(v * scale, 6)))
    while pts and pts[-1][1] == 0:
        pts.pop()
    return pts


def fetch(specs):
    cache = Cache()

    def one(s):
        p = s["params"]
        return customs_obs(cache.get_url(p["url"]), p["col_name"], p.get("scale", 1.0))
    return run_specs(specs, one)
