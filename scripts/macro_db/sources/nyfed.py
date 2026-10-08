"""紐約聯準銀行研究頁面檔：衰退機率（xls）、MCT（csv）、GSCPI（xlsx）、HLW r*（xlsx）。

讀 .xls 需要 xlrd（CI 要 pip install xlrd）。各 parse_* 吃 DataFrame／文字，方便測試。
"""
import csv
import io
import re

from ._http import get, month_first, to_float


def _excel(raw, **kw):
    import pandas as pd
    return pd.read_excel(io.BytesIO(raw), **kw)


def parse_recprob(df):
    """Date＝目標月（含未來 12 個月預測列）；Rec_prob 為 0-1 機率，轉成 %。"""
    obs = []
    for d, v in zip(df["Date"], df["Rec_prob"]):
        v = to_float(v)
        if v is None or d != d:
            continue
        obs.append((month_first(str(d)[:10]), round(v * 100, 4)))
    return obs


def parse_gscpi(df):
    """前幾列是表頭／空白；前兩欄＝日期（'31-Jan-1998'）、值。"""
    import pandas as pd
    obs = []
    for d, v in zip(df.iloc[:, 0], df.iloc[:, 1]):
        v = to_float(v)
        if v is None or d != d:
            continue
        try:
            dt = pd.to_datetime(d)
        except Exception:  # noqa: BLE001
            continue
        obs.append(("%04d-%02d-01" % (dt.year, dt.month), v))
    return obs


def parse_mct(text):
    """第 4 欄起為資料；第 2 欄是 m/d/yyyy 日期，第 4 欄（索引 3）是 MCT 中值（年化 %）。"""
    obs = []
    for r in csv.reader(io.StringIO(text)):
        if len(r) < 4 or not re.match(r"\d+/\d+/\d{4}$", r[1].strip()):
            continue
        m, _, y = r[1].strip().split("/")
        v = to_float(r[3])
        if v is not None:
            obs.append(("%s-%02d-01" % (y, int(m)), v))
    return obs


def parse_hlw(df):
    """最新 vintage 工作表：找 'Natural Rate (r*)' 標題欄（US 在同欄），日期在第 0 欄。"""
    import pandas as pd
    col = None
    for i in range(min(12, len(df))):
        for j, x in enumerate(df.iloc[i].tolist()):
            if isinstance(x, str) and x.strip().startswith("Natural Rate"):
                col = j
                break
        if col is not None:
            break
    if col is None:
        raise ValueError("找不到 Natural Rate 欄")
    obs = []
    for d, v in zip(df.iloc[:, 0], df.iloc[:, col]):
        v = to_float(v)
        if v is None:
            continue
        try:
            dt = pd.to_datetime(d)
        except Exception:  # noqa: BLE001
            continue
        obs.append(("%04d-%02d-01" % (dt.year, dt.month), v))
    return obs


def _load(kind, url):
    if kind == "recprob":
        return parse_recprob(_excel(get(url, binary=True)))
    if kind == "gscpi":
        return parse_gscpi(_excel(get(url, binary=True), sheet_name="GSCPI Monthly Data", header=None))
    if kind == "mct":
        return parse_mct(get(url))
    if kind == "hlw":
        import pandas as pd
        raw = get(url, binary=True)
        names = pd.ExcelFile(io.BytesIO(raw)).sheet_names
        vint = sorted(n for n in names if re.match(r"^\d{4}Q\d$", n))
        return parse_hlw(_excel(raw, sheet_name=vint[-1], header=None))
    raise ValueError("未知 kind：%s" % kind)


def fetch(specs):
    res = {}
    for s in specs:
        p = s["params"]
        try:
            obs = _load(p["kind"], p["url"])
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
