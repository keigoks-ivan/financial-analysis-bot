"""歐盟統計局（Eurostat）SDMX 2.1 資料 API，格式 SDMX-CSV。

params：
  dataset  資料集代碼，例如 namq_10_gdp
  key      維度 key（用 . 隔開），例如 Q.CLV10_MEUR.SCA.B1GQ.EA21
  url      完整網址（給 CI 的 probe 用；實際抓取由 dataset＋key 組成）
同一個資料集的多條序列合併成一個請求（見 eu_common.plan_requests）。
回傳列的維度欄位順序與 key 相同，用 '.'.join(維度欄) 對回各序列。
"""
from __future__ import annotations

import csv
import io

from macro_db.sources import _http
from macro_db.sources.eu_common import period_to_date, plan_requests

BASE = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
META_COLS = ("DATAFLOW", "LAST UPDATE")
TAIL_COLS = ("TIME_PERIOD", "OBS_VALUE", "OBS_FLAG", "CONF_STATUS")


def parse_csv(text, wanted):
    """text：SDMX-CSV；wanted：{完整 key: sid 清單}。回傳 {sid: [(date, float)]}。"""
    out = {}
    rdr = csv.DictReader(io.StringIO(text))
    dims = [c for c in (rdr.fieldnames or []) if c not in META_COLS and c not in TAIL_COLS]
    for row in rdr:
        sids = wanted.get(".".join(row[d] for d in dims))
        if not sids:
            continue
        v = _http.to_float(row.get("OBS_VALUE"))
        if v is None:
            continue
        d = period_to_date(row["TIME_PERIOD"])
        for sid in sids:
            out.setdefault(sid, {})[d] = v
    return {sid: sorted(m.items()) for sid, m in out.items()}


def fetch(specs):
    res = {}
    by_ds = {}
    for s in specs:
        p = s["params"]
        by_ds.setdefault(p["dataset"], []).append((p["key"], s["sid"]))
    for ds, items in by_ds.items():
        for union_key, members in plan_requests(items):
            sids = [sid for _, sid in members]
            try:
                text = _http.get("%s/%s/%s" % (BASE, ds, union_key), params={"format": "SDMX-CSV"})
                wanted = {}
                for k, sid in members:
                    wanted.setdefault(k, []).append(sid)
                got = parse_csv(text, wanted)
            except Exception as e:  # noqa: BLE001
                for sid in sids:
                    res[sid] = {"error": str(e)[:200]}
                continue
            for sid in sids:
                res[sid] = {"obs": got[sid]} if got.get(sid) else {"error": "Eurostat 沒有回傳這條序列的資料（%s）" % ds}
    return res
