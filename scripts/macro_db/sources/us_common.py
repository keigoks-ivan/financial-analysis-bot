"""美國擴充 fetcher 共用小工具：Excel 讀取、快取（每次 fetch() 呼叫一份，同一個檔只抓一次）。"""
import io
import time

from ._http import get

SITE_GAP = 1.0   # 同一站兩次請求之間至少隔 1 秒


class Cache:
    """同一次 fetch() 內共用：同一網址只抓一次、同一份工作簿只解析一次。"""

    def __init__(self):
        self.raw = {}
        self.books = {}
        self._last = 0.0

    def bytes(self, url, **kw):
        if url not in self.raw:
            wait = SITE_GAP - (time.time() - self._last)
            if self._last and wait > 0:
                time.sleep(wait)
            self.raw[url] = get(url, binary=True, **kw)
            self._last = time.time()
        return self.raw[url]

    def text(self, url, **kw):
        key = ("t", url)
        if key not in self.raw:
            wait = SITE_GAP - (time.time() - self._last)
            if self._last and wait > 0:
                time.sleep(wait)
            self.raw[key] = get(url, **kw)
            self._last = time.time()
        return self.raw[key]

    def book(self, url, **kw):
        """整本工作簿 {工作表名: DataFrame(header=None)}。"""
        import pandas as pd
        key = (url, tuple(sorted(kw.items())))
        if key not in self.books:
            self.books[key] = pd.read_excel(io.BytesIO(self.bytes(url)), sheet_name=None, header=None, **kw)
        return self.books[key]


def num(v):
    """轉 float；NaN／空白／文字回 None。"""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x != x else x


def ymd(t):
    """datetime／Timestamp -> 'YYYY-MM-DD'；不是日期回 None。"""
    if hasattr(t, "year") and hasattr(t, "month") and hasattr(t, "day"):
        try:
            return "%04d-%02d-%02d" % (t.year, t.month, t.day)
        except Exception:  # noqa: BLE001
            return None
    return None


def ym1(t):
    d = ymd(t)
    return d[:7] + "-01" if d else None


def run_specs(specs, load):
    """逐條呼叫 load(spec) -> obs；一條失敗不影響其他。"""
    res = {}
    for s in specs:
        try:
            obs = load(s)
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
