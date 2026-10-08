"""歐洲央行（ECB）Data Portal SDMX 2.1 API，格式 csvdata。

params：
  dataset  資料流代碼，例如 FM、BSI、ILM
  key      維度 key（用 . 隔開），例如 D.U2.EUR.4F.KR.DFR.LEV
  url      完整網址（給 CI 的 probe 用）
回傳的 KEY 欄＝資料流代碼＋'.'＋key，直接對回各序列。
週資料（ILM）的期間是 ISO 週（2026-W40），轉成該週星期五：歐元體系週報的資產負債表
以星期五為參考日（週二公布）。
"""
from __future__ import annotations

import csv
import io

from macro_db.sources import _http
from macro_db.sources.eu_common import period_to_date, plan_requests

BASE = "https://data-api.ecb.europa.eu/service/data"


def parse_csv(text, wanted):
    """wanted：{KEY: sid 清單}。回傳 {sid: [(date, float)]}。"""
    out = {}
    for row in csv.DictReader(io.StringIO(text)):
        sids = wanted.get(row.get("KEY"))
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
                text = _http.get("%s/%s/%s" % (BASE, ds, union_key),
                                 params={"format": "csvdata", "detail": "dataonly"},
                                 headers={"Accept": "text/csv"})
                wanted = {}
                for k, sid in members:
                    wanted.setdefault("%s.%s" % (ds, k), []).append(sid)
                got = parse_csv(text, wanted)
            except Exception as e:  # noqa: BLE001
                for sid in sids:
                    res[sid] = {"error": str(e)[:200]}
                continue
            for sid in sids:
                res[sid] = {"obs": got[sid]} if got.get(sid) else {"error": "ECB 沒有回傳這條序列的資料（%s）" % ds}
    return res
