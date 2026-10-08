"""國際清算銀行（BIS）Data Portal SDMX API（stats.bis.org，免金鑰）。跨國共用，不綁特定國家。

網址：https://stats.bis.org/api/v1/data/<dataflow>/<key>?format=csv，取 TIME_PERIOD、OBS_VALUE 欄。

params：
  dataflow  資料流（必填），如 "WS_CBPOL"（政策利率）、"WS_XRU"（對美元匯率）、"WS_SPP"（住宅價格）、"WS_EER"（有效匯率）
  key       完整 key（必填，點分隔），須對到「單一序列」，如 "M.TH"、"D.MY"、"Q.TH.N.628"、"M.R.B.SG"
  scale     選填，乘以此數後再存
  probe_url 選填，catalog 放完整網址給 CI probe 用（fetcher 不讀）

期別：2026-08（月）、2026-Q2（季）、2026-09-29（日）；缺值（NaN、空白）略過。

例（泰國政策利率）：
  {"sid": "an.cbpol_th", "fetcher": "intl_bis",
   "params": {"dataflow": "WS_CBPOL", "key": "M.TH",
              "probe_url": "https://stats.bis.org/api/v1/data/WS_CBPOL/M.TH?format=csv"}}
"""
from __future__ import annotations

import csv
import io

try:
    from . import _http
    from . import intl_common as C
except ImportError:
    import _http
    import intl_common as C

BASE = "https://stats.bis.org/api/v1/data/%s/%s?format=csv"


def build_url(p: dict) -> str:
    return BASE % (p["dataflow"], p["key"])


def parse(text: str) -> list:
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("BIS 回傳沒有資料列")
    titles = {r.get("TITLE", "").strip() for r in rows}
    if len(titles) > 1:
        raise ValueError("key 對到 %d 條序列，需剛好 1 條" % len(titles))
    return [(r["TIME_PERIOD"], r["OBS_VALUE"]) for r in rows]


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s):
        p = s["params"]
        url = build_url(p)
        if url not in cache:
            cache[url] = _http.get(url)
        return C.clean_obs(parse(cache[url]), float(p.get("scale", 1.0)))

    return C.run_specs(specs, one)
