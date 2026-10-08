"""法國國家統計局（INSEE）BDM 時間序列資料庫，SDMX 2.1 XML（免金鑰）。

params：
  idbank  INSEE 序列代碼（9 位數），例如 001565530（營商景氣綜合指標）
  url     完整網址（給 CI 的 probe 用）
網址：https://www.bdm.insee.fr/series/sdmx/data/SERIES_BDM/<idbank>[+<idbank>…]
回傳 StructureSpecificData，<Series IDBANK=…> 底下的 <Obs TIME_PERIOD=… OBS_VALUE=…/>。
期間 YYYY-MM／YYYY-Qn／YYYY，轉換同 eu_common.period_to_date。多條序列用 + 併成一個請求。
"""
from __future__ import annotations

import re

from macro_db.sources import _http
from macro_db.sources.eu_common import period_to_date

BASE = "https://www.bdm.insee.fr/series/sdmx/data/SERIES_BDM"


def parse_xml(text):
    out = {}
    for blk in re.findall(r"<Series .*?</Series>", text, re.S):
        idb = re.search(r'IDBANK="(\d+)"', blk).group(1)
        m = out.setdefault(idb, {})
        for per, val in re.findall(r'<Obs TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]*)"', blk):
            v = _http.to_float(val)
            if v is not None:
                m[period_to_date(per)] = v
    return {k: sorted(m.items()) for k, m in out.items()}


def fetch(specs):
    res = {}
    ids = {}
    for s in specs:
        ids.setdefault(s["params"]["idbank"], []).append(s["sid"])
    keys = sorted(ids)
    for i in range(0, len(keys), 8):
        chunk = keys[i:i + 8]
        try:
            got = parse_xml(_http.get("%s/%s" % (BASE, "+".join(chunk))))
        except Exception as e:  # noqa: BLE001
            for k in chunk:
                for sid in ids[k]:
                    res[sid] = {"error": str(e)[:200]}
            continue
        for k in chunk:
            for sid in ids[k]:
                res[sid] = {"obs": got[k]} if got.get(k) else {"error": "INSEE 沒有資料：" + k}
    return res
