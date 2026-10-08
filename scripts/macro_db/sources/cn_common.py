"""中國區 fetcher 共用小工具：同一網站請求間隔、重試、回傳必須是 JSON、判斷是否要回補歷史。

不嘗試繞過任何網站防護：回應不是預期格式（挑戰頁、驗證頁）就丟 Blocked，由呼叫端把整批標成 error。
"""
from __future__ import annotations

import datetime as dt
import re
import threading
import time
from urllib.parse import urlparse

import requests

try:
    from ._http import NAMED_UA, TIMEOUT, to_float
    from .. import store
except ImportError:  # 直接以腳本方式載入時
    from _http import NAMED_UA, TIMEOUT, to_float
    import store

__all__ = ["Blocked", "throttle", "session", "http", "http_json", "need_backfill", "clean", "to_float",
           "first_date_in_store"]

GAP = 1.0   # 同一網站相鄰兩次請求至少隔幾秒
_LAST: dict = {}
_LOCK = threading.Lock()


class Blocked(RuntimeError):
    """網站回了挑戰頁或其他非預期內容。"""


def throttle(url_or_host: str, gap: float = GAP):
    host = urlparse(url_or_host).netloc or url_or_host
    with _LOCK:
        wait = _LAST.get(host, 0.0) + gap - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _LAST[host] = time.monotonic()


def session(ua: str | None = "named") -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = NAMED_UA if ua == "named" else (ua or requests.utils.default_user_agent())
    return s


def http(s: requests.Session, method: str, url: str, *, retries: int = 2, sleep: float = 5.0,
         gap: float = GAP, **kw) -> requests.Response:
    """帶間隔與重試的請求；非 200 重試，仍失敗丟 RuntimeError。"""
    kw.setdefault("timeout", TIMEOUT)
    last = None
    for i in range(retries + 1):
        throttle(url, gap)
        try:
            r = s.request(method, url, **kw)
            if r.status_code != 200:
                raise RuntimeError("HTTP %s" % r.status_code)
            return r
        except Exception as e:  # noqa: BLE001
            last = e
            if i < retries:
                time.sleep(sleep)
    raise RuntimeError("%s：%s" % (url[:90], last))


def http_json(s, method, url, **kw):
    """回傳解析後的 JSON；內容不是 JSON 就丟 Blocked（不重試、不繞過）。"""
    r = http(s, method, url, **kw)
    try:
        return r.json()
    except ValueError:
        raise Blocked("%s 回應不是 JSON（可能被網站防護擋下）：%s" % (url[:70], r.text[:60].replace("\n", " ")))


def first_date_in_store(sid: str, data_dir=None):
    obs = store.read(sid, data_dir)
    return obs[0][0] if obs else None


def need_backfill(sid: str, since_year: int, data_dir=None) -> bool:
    """本地沒有這條序列、或最早一筆比 since_year 晚超過 14 個月，就回補完整歷史；否則只抓近期。"""
    first = first_date_in_store(sid, data_dir)
    if first is None:
        return True
    return first > "%d-03-01" % (since_year + 1)


def clean(s) -> str:
    """去掉全部空白（含 \\xa0、全形空白）以便比對名稱。"""
    return re.sub(r"[\s 　]+", "", str(s or ""))


def today() -> dt.date:
    return dt.date.today()
