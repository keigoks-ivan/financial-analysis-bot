"""OECD SDMX REST API（sdmx.oecd.org，免金鑰）。跨國共用，不綁特定國家。

網址：https://sdmx.oecd.org/public/rest/data/<dataflow>/<key>?...，要求 Accept: application/vnd.sdmx.data+csv。
回應 CSV，欄位含 TIME_PERIOD（2026-07、2026-Q2、2025）與 OBS_VALUE；缺值略過。
OECD 有限流（超額回 429），所以：同一個網址只抓一次、不同網址之間隔 1 秒、遇 429／5xx 退避重試 3 次。
OECD 轉載的資料多半沒有寫明原始機關，catalog 的 source 要寫清楚「OECD 轉載、原始機關未於資料集註明」或另行查證。

params：
  dataflow  資料流（必填），agency 與 id 用逗號相連，如 "OECD.SDD.STES,DSD_KEI@DF_KEI"
  key       完整 key（必填，點分隔，維度順序依各資料流），須對到「單一序列」
            DF_KEI 維度順序：REF_AREA.FREQ.MEASURE.UNIT_MEASURE.ACTIVITY.ADJUSTMENT.TRANSFORMATION
            例：印尼 CPI 年增率 "IDN.M.CP.GR._Z._Z.GY"
  accept    選填，預設 "application/vnd.sdmx.data+csv"
  scale     選填，乘以此數後再存
  probe_url 選填，catalog 放完整網址給 CI probe 用（fetcher 不讀）

key 對到多條序列（同一期出現不同值）時回報 error，不猜。
"""
from __future__ import annotations

import csv
import io
import time

try:
    from . import _http
    from . import intl_common as C
except ImportError:
    import _http
    import intl_common as C

BASE = "https://sdmx.oecd.org/public/rest/data/%s/%s"
DEFAULT_ACCEPT = "application/vnd.sdmx.data+csv"
_GAP = 1.0


def build_url(p: dict) -> str:
    return BASE % (p["dataflow"], p["key"])


def parse(text: str) -> list:
    """SDMX-CSV -> [(期別字串, 值字串)]；同期出現不同值代表 key 沒鎖定單一序列。"""
    rows, seen = [], {}
    for r in csv.DictReader(io.StringIO(text)):
        t, v = r.get("TIME_PERIOD"), r.get("OBS_VALUE")
        if not t:
            continue
        if t in seen and seen[t] != v:
            raise ValueError("key 對到多條序列（%s 有不同值）" % t)
        seen[t] = v
        rows.append((t, v))
    return rows


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}
    state = {"n": 0}

    def get(url, accept):
        if url not in cache:
            if state["n"]:
                time.sleep(_GAP)
            state["n"] += 1
            try:
                cache[url] = _http.get(url, headers={"Accept": accept}, retries=3, sleep=8)
            except Exception as e:  # noqa: BLE001
                cache[url] = e
        if isinstance(cache[url], Exception):
            raise cache[url]
        return cache[url]

    def one(s):
        p = s["params"]
        text = get(build_url(p), p.get("accept", DEFAULT_ACCEPT))
        return C.clean_obs(parse(text), float(p.get("scale", 1.0)))

    return C.run_specs(specs, one, workers=1)
