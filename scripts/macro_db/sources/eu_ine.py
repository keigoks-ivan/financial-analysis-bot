"""西班牙國家統計局（INE）Tempus 3 API（免金鑰），JSON。

params：
  cod  INE 序列代碼，例如 ETDP1826（不動產買賣件數）、FREG651（入境旅客）
  url  完整網址（給 CI 的 probe 用）
網址：https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/<cod>?nult=2000（不帶 nult 或 date 參數會回 404；nult＝取最近 N 筆，2000 足以涵蓋全史）
Data[].Fecha 是西班牙當地期初的 epoch 毫秒（夏令時間下為前一日 22:00 UTC），加 12 小時再取 UTC 日期即可還原當月（季）1 日。
Secreto 為 true 或 Valor 為 null 的略過。
"""
from __future__ import annotations

import datetime as dt
import json

from macro_db.sources import _http

BASE = "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE"


def ms_to_date(ms):
    return dt.datetime.fromtimestamp(ms / 1000.0 + 12 * 3600, dt.timezone.utc).date().isoformat()


def parse(text):
    out = {}
    for x in json.loads(text).get("Data", []):
        if x.get("Valor") is None or x.get("Secreto"):
            continue
        out[ms_to_date(x["Fecha"])] = float(x["Valor"])
    return sorted(out.items())


def fetch(specs):
    res = {}
    for s in specs:
        try:
            obs = parse(_http.get("%s/%s" % (BASE, s["params"]["cod"]), params={"nult": 2000}))
            res[s["sid"]] = {"obs": obs} if obs else {"error": "INE 沒有資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
