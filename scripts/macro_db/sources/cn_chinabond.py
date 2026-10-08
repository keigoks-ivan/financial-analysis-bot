"""中央國債登記結算（中債）國債即期收益率曲線（yield.chinabond.com.cn）。

網站只提供「最近一個交易日」的整條曲線快照（workTime 參數無效），所以這支 fetcher 每次只回一筆，
歷史靠 store 每日累積。

params：
  term      年期（年），如 10 代表 10 年期（曲線點 [10.0, 殖利率]）
  probe_url 完整網址（CI probe 用）
"""
from __future__ import annotations

try:
    from . import cn_common as C
except ImportError:
    import cn_common as C

URL = "https://yield.chinabond.com.cn/cbweb-czb-web/czb/czbChartSearch?locale=zh_CN"


def parse(j, term: float):
    """-> (日期, 殖利率)。j 為曲線清單；取名稱含「国债」的第一條。"""
    curves = j if isinstance(j, list) else [j]
    for c in curves:
        if "国债" in str(c.get("ycDefName", "")):
            day = str(c.get("worktime", ""))[:10]
            for t, y in c.get("seriesData", []):
                if abs(float(t) - term) < 1e-9 and C.to_float(y) is not None:
                    return day, float(y)
            raise ValueError("曲線上沒有 %s 年期" % term)
    raise ValueError("回應裡沒有國債收益率曲線")


def fetch(specs: list[dict]) -> dict:
    s = C.session()
    try:
        j = C.http_json(s, "GET", URL)
    except Exception as e:  # noqa: BLE001
        return {sp["sid"]: {"error": "中債抓取失敗：%s" % str(e)[:150]} for sp in specs}
    res = {}
    for sp in specs:
        try:
            d, y = parse(j, float(sp["params"]["term"]))
            res[sp["sid"]] = {"obs": [(d, y)]}
        except Exception as e:  # noqa: BLE001
            res[sp["sid"]] = {"error": str(e)[:150]}
    return res
