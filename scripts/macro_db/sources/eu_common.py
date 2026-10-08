"""歐洲 fetcher 共用工具：SDMX 期間轉日期、同一資料集多條序列合併成一個請求。

Eurostat 與 ECB 的 key 都是「維度用 . 隔開、同一維度多個值用 + 相接」。同一個資料集的多條序列
把各維度的值聯集成一個 key 一次抓，回傳的列再用完整 key 對回各序列；聯集後的組合數超過序列數的
4 倍就拆成較小的幾組（避免抓回一大堆用不到的序列）。
"""
from __future__ import annotations

import datetime as dt
import re

MAX_RATIO = 4


def period_to_date(p):
    """SDMX 期間 -> 'YYYY-MM-DD'。月＝1 日、季＝季首月 1 日、年＝1 月 1 日、
    ISO 週（2026-W40）＝該週星期五（ECB 週報的參考日）、日＝原樣。"""
    p = str(p).strip()
    m = re.fullmatch(r"(\d{4})-?Q([1-4])", p)
    if m:
        return "%s-%02d-01" % (m.group(1), (int(m.group(2)) - 1) * 3 + 1)
    m = re.fullmatch(r"(\d{4})-W(\d{2})", p)
    if m:
        return dt.date.fromisocalendar(int(m.group(1)), int(m.group(2)), 5).isoformat()
    if re.fullmatch(r"\d{4}-\d{2}", p):
        return p + "-01"
    if re.fullmatch(r"\d{4}", p):
        return p + "-01-01"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p):
        return p
    raise ValueError("看不懂的期間：%r" % p)


def _cartesian(parts_list):
    n = 1
    for dims in zip(*parts_list):
        n *= len(set(dims))
    return n


def plan_requests(keyed):
    """keyed: [(key 字串, 任意物件)]。回傳 [(聯集 key, [(key, 物件), ...]), ...]。"""
    if not keyed:
        return []
    parts = [k.split(".") for k, _ in keyed]
    if len({len(p) for p in parts}) != 1:
        return [(k, [(k, o)]) for k, o in keyed]
    n = len(keyed)
    if n == 1 or _cartesian(parts) <= max(MAX_RATIO * n, n + 6):
        union = ".".join("+".join(dict.fromkeys(dims)) for dims in zip(*parts))
        return [(union, keyed)]
    # 太散：沿著「不同值最少（但大於 1）」的維度切開，各自再規劃
    sizes = [len(set(dims)) for dims in zip(*parts)]
    cand = [(s, i) for i, s in enumerate(sizes) if s > 1]
    _, i = min(cand)
    buckets = {}
    for (k, o), p in zip(keyed, parts):
        buckets.setdefault(p[i], []).append((k, o))
    out = []
    for sub in buckets.values():
        out.extend(plan_requests(sub))
    return out
