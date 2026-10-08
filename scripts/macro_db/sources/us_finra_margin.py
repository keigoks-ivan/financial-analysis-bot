"""FINRA 保證金統計（margin-statistics.xlsx）：客戶保證金帳戶借方餘額（融資餘額）。

第 1 列欄名，資料新到舊；欄 0＝'YYYY-MM'，欄 1＝借方餘額（百萬美元）。版權屬 FINRA。
"""
import re

from .us_common import Cache, num, run_specs


def parse(df, col_index=1):
    out = []
    for i in range(len(df)):
        k = str(df.iloc[i, 0]).strip()
        if not re.fullmatch(r"\d{4}-\d{2}", k):
            continue
        v = num(df.iloc[i, col_index])
        if v is not None:
            out.append((k + "-01", v))
    return sorted(out)


def fetch(specs):
    cache = Cache()

    def load(s):
        p = s["params"]
        return parse(next(iter(cache.book(p["url"]).values())), int(p.get("col_index", 1)))

    return run_specs(specs, load)
