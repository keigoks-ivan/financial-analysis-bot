"""把原始序列換成網頁要畫的數值（display）。全部在 Python 端做。

年增率一律按日期對齊去年同期，不是往回數 12 筆（2025-10 美國 CPI 缺月，數筆數會錯位）。
對應不到去年同期的那一點就不出值。
"""
import datetime as dt

DAY = dt.date.fromisoformat


def _ymd(s):
    return dt.date.fromisoformat(s[:10])


def minus_months(d, n):
    y, m = d.year, d.month - n
    while m <= 0:
        m += 12
        y -= 1
    day = d.day
    while True:
        try:
            return dt.date(y, m, day)
        except ValueError:
            day -= 1


def prev_period(date_s, freq):
    """前一期的日期字串（只用於 M/Q/A/W 有固定間隔者）。D 不適用，回 None。"""
    d = _ymd(date_s)
    if freq == "M":
        return minus_months(d, 1).isoformat()
    if freq == "Q":
        return minus_months(d, 3).isoformat()
    if freq == "A":
        return minus_months(d, 12).isoformat()
    if freq == "W":
        return (d - dt.timedelta(days=7)).isoformat()
    return None


def year_ago(date_s):
    return minus_months(_ymd(date_s), 12).isoformat()


def _lookup(dmap, keys_sorted, target, tol_days):
    """exact；否則取 target 之前最近一筆且在 tol_days 內。"""
    if target in dmap:
        return dmap[target]
    if not tol_days:
        return None
    t = _ymd(target)
    lo, hi = 0, len(keys_sorted)
    while lo < hi:
        mid = (lo + hi) // 2
        if keys_sorted[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    if lo == 0:
        return None
    k = keys_sorted[lo - 1]
    if (t - _ymd(k)).days <= tol_days:
        return dmap[k]
    return None


def yoy(obs, freq):
    d = dict(obs)
    keys = [k for k, _ in obs]
    tol = 7 if freq in ("D", "W") else 0
    out = []
    for k, v in obs:
        p = _lookup(d, keys, year_ago(k), tol)
        if p is None or p == 0:
            continue
        out.append((k, (v / p - 1.0) * 100.0))
    return out


def mom(obs, freq):
    """對前一期的變動率 %。D 頻用前一筆。"""
    d = dict(obs)
    out = []
    prev_v = None
    for k, v in obs:
        if freq == "D":
            p = prev_v
            prev_v = v
        else:
            p = d.get(prev_period(k, freq))
        if p is None or p == 0:
            continue
        out.append((k, (v / p - 1.0) * 100.0))
    return out


def diff(obs, freq):
    d = dict(obs)
    out = []
    prev_v = None
    for k, v in obs:
        if freq == "D":
            p = prev_v
            prev_v = v
        else:
            p = d.get(prev_period(k, freq))
        if p is None:
            continue
        out.append((k, v - p))
    return out


def ratio(num, den, scale=1.0, max_gap_days=100):
    """num*scale/den*100。分母同日；沒有則取之前最近一筆（max_gap_days 內）。"""
    dd = dict(den)
    keys = [k for k, _ in den]
    out = []
    for k, v in num:
        b = _lookup(dd, keys, k, max_gap_days)
        if b is None or b == 0:
            continue
        out.append((k, v * scale / b * 100.0))
    return out


def combine(op, a, b=None, *more):
    """sum（可多條）／sub（a-b），只取各序列都有的同一日期。"""
    maps = [dict(a)] + [dict(x) for x in ([b] if b is not None else []) + list(more)]
    common = set(maps[0])
    for m in maps[1:]:
        common &= set(m)
    out = []
    for k in sorted(common):
        if op == "sum":
            out.append((k, sum(m[k] for m in maps)))
        elif op == "sub":
            out.append((k, maps[0][k] - maps[1][k]))
        else:
            raise ValueError(op)
    return out


def clip_to(obs, last_date):
    return [(k, v) for k, v in obs if k <= last_date]


def downsample_daily(obs, keep_days=3660, today=None):
    """日頻：10 年以前的部分降成週資料（每週保留最後一筆），10 年內保留日資料。"""
    if not obs:
        return obs
    cut = ((today or _ymd(obs[-1][0])) - dt.timedelta(days=keep_days)).isoformat()
    out, last_wk = [], None
    for k, v in obs:
        if k >= cut:
            out.append((k, v))
            continue
        iso = _ymd(k).isocalendar()
        wk = (iso[0], iso[1])
        if out and last_wk == wk and out[-1][0] < cut:
            out[-1] = (k, v)
        else:
            out.append((k, v))
        last_wk = wk
    return out


def apply_display(obs, spec, get_series):
    """spec：catalog 的 series dict；get_series(sid) 回傳該序列的 obs（原始值）。"""
    disp = spec.get("display", "level")
    freq = spec.get("freq", "M")
    if disp == "yoy":
        return yoy(obs, freq)
    if disp == "mom":
        return mom(obs, freq)
    if disp == "diff":
        return diff(obs, freq)
    if disp == "ratio":
        return ratio(obs, get_series(spec["denominator"]), spec.get("num_scale", 1.0))
    return list(obs)  # level / stack / qoq_saar（來源本身已是年化季增率）
