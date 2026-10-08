"""堪薩斯市聯邦準備銀行製造業調查（Tenth District Manufacturing Survey）歷史 xlsx。

檔名每月變（例如 2026Sept24historicalmfg.xlsx），所以先抓調查頁，從頁面連結找出含 historicalmfg.xlsx 的網址；
找不到連結就整批回 error，不猜檔名。工作表只有一張：第 3 列是日期（月底，取年月），第 1 欄是指標名，
同樣的指標名在不同區塊（對比上月季調、對比上月未季調、對比去年、未來 6 個月預期）各出現一次，
所以用「區塊標題＋括號說明＋指標名」定位。
"""
import re
from urllib.parse import urljoin

from .us_common import Cache, num, ym1, run_specs

PAGE = "https://www.kansascityfed.org/surveys/manufacturing-survey/"
LINK_RE = re.compile(r'href="([^"]*historicalmfg\.xlsx)"', re.I)


def find_link(html, base=PAGE):
    m = LINK_RE.search(html)
    if not m:
        raise ValueError("調查頁找不到 historicalmfg.xlsx 連結")
    return urljoin(base, m.group(1))


def parse_block(df, block, note, label, date_row=2):
    """找 block（如 'Versus a Month Ago'）後一列為 note（如 '(seasonally adjusted)'）的區塊，取其中 label 那列。"""
    start = None
    for i in range(len(df) - 1):
        a, b = df.iloc[i, 0], df.iloc[i + 1, 0]
        if isinstance(a, str) and isinstance(b, str) and a.strip() == block and b.strip() == note:
            start = i + 2
            break
    if start is None:
        raise ValueError("找不到區塊：%s %s" % (block, note))
    row = None
    for i in range(start, min(start + 16, len(df))):
        a = df.iloc[i, 0]
        if isinstance(a, str) and a.strip() == label:
            row = i
            break
        if isinstance(a, str) and a.strip() == block:   # 走到下一個區塊
            break
    if row is None:
        raise ValueError("區塊內找不到指標：%s" % label)
    out = []
    for j in range(1, df.shape[1]):
        d, v = ym1(df.iloc[date_row, j]), num(df.iloc[row, j])
        if d and v is not None:
            out.append((d, v))
    return out


def fetch(specs):
    cache = Cache()
    state = {}

    def book():
        if "df" not in state:
            page = specs[0]["params"].get("page", PAGE)
            url = find_link(cache.text(page), page)
            state["url"] = url
            state["df"] = next(iter(cache.book(url).values()))
        return state["df"]

    def load(s):
        p = s["params"]
        return parse_block(book(), p["block"], p["note"], p["label"])

    return run_specs(specs, load)
