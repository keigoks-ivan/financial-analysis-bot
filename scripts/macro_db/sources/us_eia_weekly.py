"""美國能源資訊署（EIA）週報歷史 .xls（hist_xls/<代碼>w.xls、天然氣 NW2_EPG0_SWO_R48_BCFw.xls）。

工作表 Data 1：前 3 列是表頭，第 4 列起「日期（週五或週末）、值」。需 xlrd。
"""
import io

from .us_common import Cache, num, ymd, run_specs


def parse(df, skip_rows=3):
    out = []
    for i in range(skip_rows, len(df)):
        d, v = ymd(df.iloc[i, 0]), num(df.iloc[i, 1])
        if d and v is not None:
            out.append((d, v))
    return out


def fetch(specs):
    import pandas as pd
    cache = Cache()

    def load(s):
        p = s["params"]
        raw = cache.bytes(p["url"])
        df = pd.read_excel(io.BytesIO(raw), sheet_name=p.get("sheet", "Data 1"), header=None)
        return parse(df, int(p.get("skip_rows", 3)))

    return run_specs(specs, load)
