"""亞特蘭大聯邦準備銀行薪資成長追蹤（Wage Growth Tracker）：wage-growth-data.xlsx，多張工作表。

每張工作表第 1 欄是月份（datetime，月初），欄名在資料上方數列；用欄名文字找欄，不寫死欄位序號。
data_overall 為 3 個月移動平均中位數；Age、Industry 等工作表為 12 個月移動平均。
"""
from .us_common import Cache, num, ym1, run_specs


def parse_sheet(df, header, scan_rows=6):
    """df：header=None 讀進來的工作表；header：欄名文字。回傳 [(月初, 值)]。"""
    col = None
    for i in range(min(scan_rows, len(df))):
        for j in range(1, df.shape[1]):
            v = df.iloc[i, j]
            if isinstance(v, str) and v.strip() == header:
                col = j
                break
        if col is not None:
            break
    if col is None:
        raise ValueError("找不到欄名：%s" % header)
    out = []
    for i in range(len(df)):
        d = ym1(df.iloc[i, 0])
        v = num(df.iloc[i, col])
        if d and v is not None:
            out.append((d, v))
    return out


def fetch(specs):
    cache = Cache()

    def load(s):
        p = s["params"]
        book = cache.book(p["url"])
        return parse_sheet(book[p["sheet"]], p["header"])

    return run_specs(specs, load)
