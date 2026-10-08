"""IMF 新版 SDMX 3.0 API（api.imf.org，免金鑰）。跨國共用，不綁特定國家。

request 必須帶 Accept: application/json；回應為 SDMX-JSON：
  data.dataSets[0].series["0:0:0"].observations{索引: [值字串]}、
  時間在 data.structures[0].dimensions.observation[0].values[].value（如 2026-M06、2026-Q2、2025）。

params：
  dataflow  資料流（必填），如 "CPI"、"IRFCL"、"ITG"、"IMTS"、"QNEA"、"MFS_MA"、"PI"
  key       完整 key（必填，點分隔，維度順序依各資料流），須對到「單一序列」
  agency    選填，預設 "IMF.STA"
  scale     選填，乘以此數後再存（例如原值是美元、要存百萬美元就給 1e-6）
  probe_url 選填，catalog 放完整網址給 CI probe 用（fetcher 不讀）

例（泰國 CPI 年增率）：
  {"sid": "an.cpi_yoy_th", "fetcher": "intl_imf",
   "params": {"dataflow": "CPI", "key": "THA.CPI._T.YOY_PCH_PA_PT.M",
              "probe_url": "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/CPI/+/THA.CPI._T.YOY_PCH_PA_PT.M?attributes=none"}}
"""
from __future__ import annotations

import json

try:
    from . import _http
    from . import intl_common as C
except ImportError:
    import _http
    import intl_common as C

BASE = "https://api.imf.org/external/sdmx/3.0/data/dataflow/%s/%s/+/%s?attributes=none"


def build_url(p: dict) -> str:
    return BASE % (p.get("agency", "IMF.STA"), p["dataflow"], p["key"])


def parse(text: str) -> list:
    """SDMX-JSON 3.0 -> [(期別字串, 值字串)]；只接受單一序列。"""
    d = json.loads(text)
    data = d["data"]
    times = data["structures"][0]["dimensions"]["observation"][0]["values"]
    series = data["dataSets"][0]["series"]
    if len(series) != 1:
        raise ValueError("key 對到 %d 條序列，需剛好 1 條" % len(series))
    obs = next(iter(series.values())).get("observations", {})
    rows = []
    for idx, arr in obs.items():
        t = times[int(idx)]
        rows.append((t.get("id") or t.get("value"), arr[0] if arr else None))
    return rows


def fetch(specs: list[dict]) -> dict:
    cache: dict = {}

    def one(s):
        p = s["params"]
        url = build_url(p)
        if url not in cache:
            cache[url] = _http.get(url, headers={"Accept": "application/json"})
        return C.clean_obs(parse(cache[url]), float(p.get("scale", 1.0)))

    return C.run_specs(specs, one)
