"""費城聯邦準備銀行：ADS 景氣指數（日）、專業預測者調查 SPF（季，中位數水準檔）、
SPF 衰退機率（Anxious Index）、非製造業調查 NBOS（月，Diffusion 工作表）。

同一個檔一次抓、多條序列共用。日期：日資料＝當日；季資料＝季首月 1 日；月資料＝當月 1 日。
Anxious Index 的日期＝「調查進行的那一季」（值是該次調查對『下一季』實質 GDP 負成長的機率）。
"""
from .us_common import Cache, num, ym1, ymd, run_specs


def parse_ads(df):
    """Date 欄是 'YYYY:MM:DD'，冒號換成連字號。df 用 header=0 讀。"""
    out = []
    for d, v in zip(df["Date"], df["ADS_Index"]):
        v = num(v)
        if v is not None:
            out.append((str(d)[:10].replace(":", "-"), v))
    return out


def parse_spf(df, col):
    """YEAR＋QUARTER 欄＋指定欄 -> 季首月 1 日。df 用 header=0 讀。"""
    out = []
    for y, q, v in zip(df["YEAR"], df["QUARTER"], df[col]):
        v = num(v)
        if v is None or num(y) is None or num(q) is None:
            continue
        out.append(("%04d-%02d-01" % (int(y), (int(q) - 1) * 3 + 1), v))
    return out


def parse_anxious(df, shift_quarters=-1):
    """工作表 Data：第 5 列起，欄 0＝年、欄 1＝季、欄 2＝機率（%）。df 用 header=None 讀。

    檔案的年季是「預測的目標季」（Quarter for Decline），不是調查進行的季；本庫日期用調查進行的那一季，
    所以預設往前挪一季（shift_quarters=-1）：例如檔內 2026Q4 的值＝2026 年第 3 季調查對下一季（Q4）負成長的機率。
    """
    out = []
    for i in range(len(df)):
        y, q, v = num(df.iloc[i, 0]), num(df.iloc[i, 1]), num(df.iloc[i, 2])
        if y is None or q is None or v is None or not (1 <= q <= 4) or y < 1900:
            continue
        n = int(y) * 4 + int(q) - 1 + shift_quarters
        out.append(("%04d-%02d-01" % (n // 4, (n % 4) * 3 + 1), v))
    return out


def parse_nbos(df, col):
    """欄名在第 0 列、date 欄為日期。df 用 header=0 讀。"""
    out = []
    for t, v in zip(df["date"], df[col]):
        d, v = ym1(t), num(v)
        if d and v is not None:
            out.append((d, v))
    return out


def _header0(book, sheet):
    df = book[sheet]
    df = df.copy()
    df.columns = [str(x).strip() for x in df.iloc[0].tolist()]
    return df.iloc[1:].reset_index(drop=True)


def fetch(specs):
    cache = Cache()

    def load(s):
        p = s["params"]
        k = p["kind"]
        book = cache.book(p["url"])
        if k == "ads":
            return parse_ads(_header0(book, next(iter(book))))
        if k == "spf":
            return parse_spf(_header0(book, p["sheet"]), p["col"])
        if k == "anxious":
            return parse_anxious(book["Data"], int(p.get("shift_quarters", -1)))
        if k == "nbos":
            return parse_nbos(_header0(book, p["sheet"]), p["col"])
        raise ValueError("未知 kind：%s" % k)

    return run_specs(specs, load)
