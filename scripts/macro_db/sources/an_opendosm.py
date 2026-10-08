"""馬來西亞統計局（DOSM）OpenDOSM／data.gov.my 資料目錄 API（免金鑰）。

網址：https://api.data.gov.my/data-catalogue/?id=<id>&limit=100000&sort=date[&filter=<值>@<欄>]
  網址在 data-catalogue 後面要有斜線（沒有會 301）。date 為每期第一天（季＝該季首月 1 日）。
params：
  id      資料集代碼（必填），如 "gdp_qtr_real"
  field   取值的欄位（必填），如 "value"、"index"、"exports"
  filter  選填，如 "abs@series"（series 欄等於 abs）、"overall@division"
  scale   選填，乘以此數後再存
  probe_url 選填（fetcher 不讀）
  to_quarterly 選填，true＝來源以月列出但每季三個月同值（如正式部門薪資），收成季資料（季首月 1 日）
同一個 (id, filter) 只抓一次；data.gov.my 會對連續請求回 429，所以請求之間至少隔 1 秒，429／5xx 退避重試（最多 3 次）。
"""
from __future__ import annotations

import json
import re
import time

try:
    from . import _http
    from . import an_common as A
except ImportError:
    import _http
    import an_common as A

URL = "https://api.data.gov.my/data-catalogue/"
MIN_GAP = 1.0          # 兩次請求之間至少隔幾秒
RETRIES = 3            # 429／5xx 退避重試次數
BACKOFF = 8.0          # 第 n 次重試等 BACKOFF * n 秒
_last = [0.0]


def _get(url: str) -> str:
    """限速＋退避的 GET（只用於 api.data.gov.my）。_http.get 不重試，429／5xx 由這裡退避。"""
    last = None
    for i in range(RETRIES + 1):
        wait = MIN_GAP - (time.monotonic() - _last[0])
        if wait > 0:
            time.sleep(wait)
        try:
            txt = _http.get(url, retries=0)
            _last[0] = time.monotonic()
            return txt
        except Exception as e:  # noqa: BLE001
            _last[0] = time.monotonic()
            last = e
            m = re.search(r"HTTP (\d+)", str(e))
            retryable = m is None or m.group(1) == "429" or int(m.group(1)) >= 500
            if not retryable:
                break
        if i < RETRIES:
            time.sleep(BACKOFF * (i + 1))
    raise RuntimeError("%s：%s" % (url[:90], last))


def build_url(p: dict) -> str:
    u = "%s?id=%s&limit=100000&sort=date" % (URL, p["id"])
    if p.get("filter"):
        u += "&filter=" + p["filter"]
    return u


def parse(text: str, field: str) -> list:
    rows = json.loads(text)
    if not isinstance(rows, list):
        raise ValueError("回應不是資料列：%s" % str(rows)[:120])
    return [(r["date"][:10], r.get(field)) for r in rows if "date" in r]


def to_quarterly(obs: list) -> list:
    """月列但季內同值：每季只留第一筆，日期落在季首月 1 日。"""
    out, seen = [], set()
    for d, v in sorted(obs):
        q = (d[:4], (int(d[5:7]) - 1) // 3)
        if q in seen:
            continue
        seen.add(q)
        out.append(("%s-%02d-01" % (q[0], q[1] * 3 + 1), v))
    return out


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}
    # 先依序抓完所有不同網址（限速、同一網址只抓一次），再平行解析
    for sp in specs:
        url = build_url(sp["params"])
        if url not in cache:
            try:
                cache[url] = _get(url)
            except Exception as e:  # noqa: BLE001
                cache[url] = e

    def one(s):
        p = s["params"]
        txt = cache[build_url(p)]
        if isinstance(txt, Exception):
            raise txt
        obs = A.clean_obs(parse(txt, p["field"]), float(p.get("scale", 1.0)))
        if p.get("to_quarterly"):
            obs = to_quarterly(obs)
        return obs

    return A.run_specs(specs, one)
