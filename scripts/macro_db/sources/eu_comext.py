"""歐盟統計局 Comext（DS-045409）月度貿易值（現價歐元，未季調），SDMX-CSV。

params：
  reporter  申報國／區域，例如 DE、FR、IT、ES、EA21
  partner   貿易夥伴，例如 US、CN、GB、JP、CH、TR、IN、KR、WORLD
  flow      1＝進口、2＝出口
  product   產品代碼，預設 TOTAL
  url       完整網址（給 CI 的 probe 用）
與 eu_eurostat 同為 Eurostat，但走 comext 專用路徑（/api/comext/dissemination/），每條序列一個請求。
"""
from __future__ import annotations

import csv
import io
import time

from macro_db.sources import _http
from macro_db.sources.eu_common import period_to_date

GAP = 1.0  # 同站請求間隔（秒）
BACKOFF = (5, 15, 45)  # 429／5xx 的退避秒數，用完才放棄

BASE = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409"


def parse_csv(text):
    out = {}
    for row in csv.DictReader(io.StringIO(text)):
        v = _http.to_float(row.get("OBS_VALUE"))
        if v is None:
            continue
        out[period_to_date(row["TIME_PERIOD"])] = v
    return sorted(out.items())


def _get(url):
    """單一請求；429／5xx 或網路錯誤退避重試（共 3 次），其他錯誤直接丟出。"""
    last = None
    for wait in BACKOFF + (None,):
        try:
            return _http.get(url, params={"format": "SDMX-CSV"}, retries=0)
        except RuntimeError as e:
            last = e
            m = str(e)
            retryable = any(c in m for c in ("HTTP 429", "HTTP 5", "imed out", "Timeout", "Connection"))
            if wait is None or not retryable:
                break
            time.sleep(wait)
    raise last


def fetch(specs):
    res = {}
    for n, s in enumerate(specs):
        if n:
            time.sleep(GAP)
        p = s["params"]
        key = "M.%s.%s.%s.%s.VALUE_IN_EUROS" % (p["reporter"], p["partner"], p.get("product", "TOTAL"), p["flow"])
        try:
            obs = parse_csv(_get("%s/%s" % (BASE, key)))
            res[s["sid"]] = {"obs": obs} if obs else {"error": "Comext 沒有資料：" + key}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
