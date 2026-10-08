"""跨國共用 fetcher（intl_imf／intl_bis／intl_worldbank）共用的小工具：期別轉日期、批次抓取。

日期規則同 SPEC：月＝當月 1 日、季＝季首月 1 日、年＝1 月 1 日、日＝當日。
"""
from __future__ import annotations

import concurrent.futures as cf
import re

try:
    from ._http import to_float
except ImportError:  # 直接以腳本方式載入時
    from _http import to_float

__all__ = ["to_float", "period_to_date", "clean_obs", "run_specs"]

_PATTERNS = [
    (re.compile(r"^(\d{4})-M(\d{2})$"), lambda m: "%s-%s-01" % (m[1], m[2])),              # IMF 月：2026-M06
    (re.compile(r"^(\d{4})-Q([1-4])$"), lambda m: "%s-%02d-01" % (m[1], (int(m[2]) - 1) * 3 + 1)),  # 季：2026-Q2
    (re.compile(r"^(\d{4})-(\d{2})-(\d{2})$"), lambda m: m[0]),                            # 日
    (re.compile(r"^(\d{4})-(\d{2})$"), lambda m: "%s-%s-01" % (m[1], m[2])),               # BIS 月：2026-08
    (re.compile(r"^(\d{4})(?:-A\d?)?$"), lambda m: "%s-01-01" % m[1]),                     # 年：2025／2025-A
]


def period_to_date(p) -> str | None:
    s = str(p).strip()
    for rx, fn in _PATTERNS:
        m = rx.match(s)
        if m:
            return fn(m)
    return None


def clean_obs(rows, scale: float = 1.0) -> list:
    """rows: [(期別字串, 值)]。略過無法解析的期別與缺值，依日期排序、同日取後者。"""
    out = {}
    for p, v in rows:
        d = period_to_date(p)
        x = to_float(v)
        if d is None or x is None:
            continue
        out[d] = x * scale if scale != 1.0 else x
    return sorted(out.items())


def run_specs(specs, one, workers: int = 4) -> dict:
    """對每條 spec 呼叫 one(spec) -> obs 清單；個別失敗寫進 error，不影響其他條。同一網站並行不超過 4。"""
    res = {}

    def wrap(s):
        try:
            obs = one(s)
            if not obs:
                return s["sid"], {"error": "解析後沒有任何觀測值"}
            return s["sid"], {"obs": obs}
        except Exception as e:  # noqa: BLE001
            return s["sid"], {"error": str(e)[:200]}

    with cf.ThreadPoolExecutor(max_workers=min(workers, 4)) as ex:
        for sid, r in ex.map(wrap, specs):
            res[sid] = r
    return res
