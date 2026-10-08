"""東南亞（an）fetcher 共用的小工具：月名、期別字串轉日期。"""
from __future__ import annotations

import re

try:
    from .intl_common import clean_obs, run_specs, to_float  # noqa: F401
except ImportError:
    from intl_common import clean_obs, run_specs, to_float  # noqa: F401

MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def month_num(name: str) -> int | None:
    """'Jan'／'January'／'JANUARY' -> 1；認不得（Ave、Annual、Total）回傳 None。"""
    return MONTHS.get(str(name).strip()[:3].lower()) if str(name).strip()[:3].isalpha() else None


def ym_date(year, month: int) -> str:
    return "%04d-%02d-01" % (int(year), month)


def yq_date(year, q: int) -> str:
    return "%04d-%02d-01" % (int(year), (q - 1) * 3 + 1)


def year_of(label: str) -> int | None:
    m = re.search(r"(\d{4})", str(label))
    return int(m.group(1)) if m else None
