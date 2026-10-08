"""共用 HTTP：timeout 60 秒、失敗重試 2 次（間隔 5 秒）。

FRED 要用 requests 預設 User-Agent（自訂會被擋到逾時）；BLS／NY Fed 等要帶「名稱＋網址」UA（不放個人 email，repo 是公開的）。
"""
import time

import requests

NAMED_UA = "investmquest-research/1.0 (+https://research.investmquest.com/macro/db/)"
TIMEOUT = 60
RETRIES = 2
RETRY_SLEEP = 5


def get(url, *, ua="named", binary=False, params=None, timeout=TIMEOUT, retries=RETRIES,
        sleep=RETRY_SLEEP, headers=None):
    """GET。ua='named' 帶名稱＋網址；ua=None 用 requests 預設。回傳 bytes（binary）或 str。"""
    h = dict(headers or {})
    if ua == "named":
        h["User-Agent"] = NAMED_UA
    elif ua:
        h["User-Agent"] = ua
    last = None
    for i in range(retries + 1):
        try:
            r = requests.get(url, params=params, headers=h, timeout=timeout)
            if r.status_code != 200:
                raise RuntimeError("HTTP %s" % r.status_code)
            return r.content if binary else r.content.decode("utf-8-sig", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            if i < retries:
                time.sleep(sleep)
    raise RuntimeError("%s：%s" % (url[:90], last))


def month_first(s):
    """'2026-08-31' / '2026-08' -> '2026-08-01'"""
    s = str(s)[:10]
    if len(s) == 7:
        return s + "-01"
    return s[:7] + "-01"


def to_float(x):
    if x is None:
        return None
    s = str(x).strip().replace(",", "")
    if s in ("", ".", "-", "…", "NaN", "nan", "None", "null", "NA", "n/a"):
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    if v != v:
        return None
    return v
