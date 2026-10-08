"""紐約聯準銀行研究頁面檔：衰退機率（xls）、MCT（csv）、GSCPI（xlsx）、HLW r*（xlsx）、消費者預期調查 SCE（xlsx）、
ACM 期限溢酬（xls）、家庭債務與信用報告 HHDC（xlsx，檔名帶季別）。

讀 .xls 需要 xlrd（CI 要 pip install xlrd）。各 parse_* 吃 DataFrame／文字，方便測試。
"""
import csv
import datetime as dt
import io
import re

from ._http import get, month_first, to_float
from .us_common import Cache


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


def _find_col(df, header, scan_rows=8):
    """在前幾列找欄名（不分大小寫，開頭符合即可），回傳欄序號。"""
    h = header.strip().lower()
    for i in range(min(scan_rows, len(df))):
        for j in range(1, df.shape[1]):
            v = df.iloc[i, j]
            if isinstance(v, str) and v.strip().lower().startswith(h):
                return j
    raise ValueError("找不到欄名：%s" % header)


def parse_sce(df, header):
    """SCE 各工作表：第 1 欄 'YYYYMM'，欄名在前幾列；回傳 [(月初, 值)]。"""
    col = _find_col(df, header)
    obs = []
    for i in range(len(df)):
        k = str(df.iloc[i, 0]).strip()
        if not re.fullmatch(r"\d{6}", k):
            continue
        v = to_float(df.iloc[i, col])
        if v is not None:
            obs.append(("%s-%s-01" % (k[:4], k[4:]), v))
    return obs


def parse_hhdc(df, header):
    """家庭債務與信用報告 'Page n Data'：第 1 欄 'YY:Qn'（例如 26:Q2），欄名在前幾列；回傳 [(季首月 1 日, 值)]。"""
    col = _find_col(df, header)
    obs = []
    for i in range(len(df)):
        m = re.fullmatch(r"(\d\d):Q([1-4])", str(df.iloc[i, 0]).strip())
        if not m:
            continue
        yy = int(m.group(1))
        yy += 2000 if yy < 80 else 1900
        v = to_float(df.iloc[i, col])
        if v is not None:
            obs.append(("%04d-%02d-01" % (yy, (int(m.group(2)) - 1) * 3 + 1), v))
    return obs


def parse_acm(df, col):
    """ACM Daily：DATE 欄為 '06-Oct-2026'，col 為欄名（例如 ACMTP10，單位 %）。df 用 header=0 讀。"""
    obs = []
    for t, v in zip(df["DATE"], df[col]):
        v = to_float(v)
        if v is None:
            continue
        d = t.date() if hasattr(t, "date") else dt.datetime.strptime(str(t).strip(), "%d-%b-%Y").date()
        obs.append((d.isoformat(), v))
    return obs


def hhdc_candidates(url_pattern, today=None, n=6):
    """報告檔名帶季別（HHD_C_Report_2026Q2.xlsx）：從今天所在季往前試 n 季。"""
    today = today or dt.date.today()
    y, q = today.year, (today.month - 1) // 3 + 1
    out = []
    for _ in range(n):
        out.append(url_pattern.replace("{YYYY}", str(y)).replace("{q}", str(q)))
        q -= 1
        if q == 0:
            y, q = y - 1, 4
    return out


def _load_hhdc_book(cache, p, state):
    if "book" not in state:
        last = None
        for u in hhdc_candidates(p["url_pattern"]):
            try:
                state["book"] = cache.book(u)
                state["url"] = u
                break
            except Exception as e:  # noqa: BLE001
                last = e
        if "book" not in state:
            raise RuntimeError("找不到家庭債務報告檔（往前試 6 季皆失敗）：%s" % last)
    return state["book"]


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
    cache = Cache()      # SCE／ACM／家庭債務報告：同一個檔一次抓、多條序列共用
    hh = {}
    for s in specs:
        p = s["params"]
        try:
            k = p["kind"]
            if k == "sce":
                obs = parse_sce(cache.book(p["url"])[p["sheet"]], p["header"])
            elif k == "acm":
                import pandas as pd
                key = ("acm", p["url"], p["sheet"])
                if key not in cache.books:
                    cache.books[key] = pd.read_excel(io.BytesIO(cache.bytes(p["url"])), sheet_name=p["sheet"])
                obs = parse_acm(cache.books[key], p["col"])
            elif k == "hhdc":
                obs = parse_hhdc(_load_hhdc_book(cache, p, hh)["Page %d Data" % p["page"]], p["header"])
            else:
                obs = _load(k, p["url"])
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
