"""德國聯邦網路局 SMARD（電力市場資料平台）chart_data。

params：
  filter      資料類別，410＝實際用電量（Realisierter Stromverbrauch）
  region      DE
  resolution  day
  url         index 網址（給 CI 的 probe 用）
先抓 index_<resolution>.json 取得各年份檔的起始時間戳，再逐年抓
<filter>_<region>_<resolution>_<ts>.json；series＝[[epoch 毫秒, MWh]]，null 表示尚未結算。
時間戳是德國當地 00:00，加 12 小時再取 UTC 日期就是德國當地日期（不受夏令時間影響）。
"""
from __future__ import annotations

import datetime as dt
import json

from macro_db.sources import _http

BASE = "https://www.smard.de/app/chart_data"


def ms_to_date(ms):
    return (dt.datetime.fromtimestamp(ms / 1000.0 + 12 * 3600, dt.timezone.utc)).date().isoformat()


def parse_series(text):
    out = {}
    for ts, val in json.loads(text).get("series", []):
        if val is None:
            continue
        out[ms_to_date(ts)] = float(val)
    return out


def fetch(specs):
    res = {}
    for s in specs:
        p = s["params"]
        try:
            f, rg, rs = p["filter"], p["region"], p["resolution"]
            idx = json.loads(_http.get("%s/%s/%s/index_%s.json" % (BASE, f, rg, rs)))["timestamps"]
            obs = {}
            for ts in idx:
                obs.update(parse_series(_http.get("%s/%s/%s/%s_%s_%s_%s.json" % (BASE, f, rg, f, rg, rs, ts))))
            res[s["sid"]] = {"obs": sorted(obs.items())} if obs else {"error": "SMARD 沒有資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
