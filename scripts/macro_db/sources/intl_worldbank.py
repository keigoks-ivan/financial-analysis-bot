"""世界銀行 Open Data API v2（api.worldbank.org，免金鑰）。跨國共用，不綁特定國家。

params：
  indicator  指標代碼（必填），如 "NY.GDP.MKTP.KD.ZG"（實質 GDP 年增率，%）
  country    ISO3 國碼（必填），如 "VNM"
  scale      選填，乘以此數後再存
  probe_url  選填，catalog 放完整網址給 CI probe 用（fetcher 不讀）

只有年資料；日期＝該年 1 月 1 日；value 為 null 的年份略過。

例（越南實質 GDP 年增率）：
  {"sid": "an.vn_gdp_growth_wb", "fetcher": "intl_worldbank",
   "params": {"indicator": "NY.GDP.MKTP.KD.ZG", "country": "VNM",
              "probe_url": "https://api.worldbank.org/v2/country/VNM/indicator/NY.GDP.MKTP.KD.ZG?format=json&per_page=20000"}}
"""
from __future__ import annotations

import json

try:
    from . import _http
    from . import intl_common as C
except ImportError:
    import _http
    import intl_common as C

BASE = "https://api.worldbank.org/v2/country/%s/indicator/%s?format=json&per_page=20000"


def build_url(p: dict) -> str:
    return BASE % (p["country"], p["indicator"])


def parse(text: str) -> list:
    d = json.loads(text)
    if not isinstance(d, list) or len(d) < 2 or d[1] is None:
        msg = d[0] if isinstance(d, list) and d else d
        raise ValueError("世界銀行回傳無資料：%s" % str(msg)[:120])
    return [(r["date"], r["value"]) for r in d[1]]


def fetch(specs: list[dict]) -> dict:
    def one(s):
        p = s["params"]
        return C.clean_obs(parse(_http.get(build_url(p))), float(p.get("scale", 1.0)))

    return C.run_specs(specs, one)
