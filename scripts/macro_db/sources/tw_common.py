"""台灣 fetcher 共用工具：下載（含重試）、日期轉換、數值解析、data.gov.tw 網址解析。

fetcher 介面（SPEC）：fetch(specs) -> {sid: {"obs": [(YYYY-MM-DD, float)]} | {"error": str}}
一條失敗不得讓整批失敗，所以每個 fetcher 都用 run_specs() 逐條包 try/except。
"""
from __future__ import annotations

import os
import re
import tempfile
import time
from pathlib import Path
from typing import Callable, Iterable

import requests

TIMEOUT = 60
RETRIES = 2           # 失敗後再試 2 次（共 3 次嘗試）
RETRY_WAIT = 5        # 秒
UA_NAME = "investmquest-research/1.0 (+https://research.investmquest.com/macro/db/)"

DATAGOV_API = "https://data.gov.tw/api/v2/rest/dataset/{id}"

# 缺值字串：直接略過，不填 0
MISSING = {"", "-", "--", "---", "…", "...", "—", "nan", "NaN", "NA", "N/A", "n.a.", "x", "X", "－"}


class FetchError(Exception):
    pass



# 台灣政府網站（例如 ws.dgbas.gov.tw）送出的憑證鏈缺中繼憑證（TWCA Secure SSL CA），瀏覽器與 macOS curl
# 會自動補，Python／OpenSSL 不會。做法：certifi 根憑證＋repo 內附的中繼憑證合成一份 bundle，照常完整驗證。
# 中繼憑證來源：葉憑證 AIA 欄位 http://sslserver.twca.com.tw/cacert/secure_sha2_2023G3.crt（2030-10-16 到期）。
# 2026-10-07 主計總處換成 TWCA SSL Certification Authority 簽發的葉憑證，又補一張：
# http://sslserver.twca.com.tw/cacert/Cyber_SSL_2023.crt（上層 TWCA CYBER Root CA，在 certifi 內；2033-02-23 到期）。
_EXTRA_CA_DIR = Path(__file__).resolve().parent.parent / "certs"
_CA_BUNDLE: str | None = None


def _ca_bundle() -> str:
    global _CA_BUNDLE
    if _CA_BUNDLE is None:
        import certifi
        parts = [Path(certifi.where()).read_text()]
        parts += [p.read_text() for p in sorted(_EXTRA_CA_DIR.glob("*.pem"))]
        fd, path = tempfile.mkstemp(prefix="macro_db_ca_", suffix=".pem")
        with os.fdopen(fd, "w") as f:
            f.write("\n".join(parts))
        _CA_BUNDLE = path
    return _CA_BUNDLE


def _request(method, url, data, hdr, timeout):
    return requests.request(method, url, data=data, headers=hdr, timeout=timeout, verify=_ca_bundle())


def http_get(url: str, *, method: str = "GET", data=None, headers=None, timeout: int = TIMEOUT,
             retries: int = RETRIES, wait: float = RETRY_WAIT) -> bytes:
    """下載並回傳 bytes。失敗重試；HTTP 4xx/5xx 視為失敗。"""
    hdr = {"User-Agent": UA_NAME}   # 能源署等站會擋 python-requests 預設 UA，統一帶「名稱＋網址」
    hdr.update(headers or {})
    last = None
    for attempt in range(retries + 1):
        try:
            r = _request(method, url, data, hdr, timeout)
            if r.status_code != 200:
                raise FetchError(f"HTTP {r.status_code} {url[:120]}")
            return r.content
        except Exception as e:  # noqa: BLE001
            last = e
            if attempt < retries:
                time.sleep(wait)
    raise FetchError(f"下載失敗：{last}") from last


def http_get_cached(cache: dict, url: str, **kw) -> bytes:
    key = (url, kw.get("method", "GET"), repr(kw.get("data")))
    if key not in cache:
        cache[key] = http_get(url, **kw)
    return cache[key]


def get_json(url: str, **kw):
    import json
    return json.loads(http_get(url, **kw).decode("utf-8-sig"))


# ---------- 數值 ----------

def to_float(v) -> float | None:
    """'1,234.5' -> 1234.5；缺值（- … 空白 NaN）-> None。"""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        f = float(v)
        return None if f != f else f
    s = str(v).strip().replace(",", "").replace("，", "").replace("％", "").replace("%", "")
    if s in MISSING:
        return None
    try:
        f = float(s)
    except ValueError:
        return None
    return None if f != f else f


# ---------- 日期 ----------

def d_month(y: int, m: int) -> str:
    return f"{int(y):04d}-{int(m):02d}-01"


def d_quarter(y: int, q: int) -> str:
    return f"{int(y):04d}-{(int(q) - 1) * 3 + 1:02d}-01"


def d_year(y: int) -> str:
    return f"{int(y):04d}-01-01"


def d_day(y: int, m: int, d: int) -> str:
    return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"


def roc_ym_to_date(s: str) -> str | None:
    """民國 'YYYMM'（如 11507）-> '2026-07-01'。"""
    m = re.match(r"^\s*(\d{2,3})(\d{2})\s*$", str(s))
    if not m:
        return None
    return d_month(int(m.group(1)) + 1911, int(m.group(2)))


def roc_label_to_date(s: str) -> str | None:
    """民國 '115年 8月' / '115年8月' -> '2026-08-01'；'115年'（年合計）-> None。"""
    m = re.match(r"^\s*(\d{1,3})\s*年\s*(\d{1,2})\s*月\s*$", str(s))
    if not m:
        return None
    return d_month(int(m.group(1)) + 1911, int(m.group(2)))


def roc_date_to_iso(s: str) -> str | None:
    """民國 '115/09/01'（前導空白可有）-> '2026-09-01'；或 '1150901'。"""
    s = str(s).strip()
    m = re.match(r"^(\d{2,3})[/-](\d{1,2})[/-](\d{1,2})$", s) or re.match(r"^(\d{2,3})(\d{2})(\d{2})$", s)
    if not m:
        return None
    return d_day(int(m.group(1)) + 1911, int(m.group(2)), int(m.group(3)))


def period_to_date(p: str) -> str | None:
    """主計總處／央行常見期間字串 -> 日期。
    '2026M08' / '202608' / '202607Ⓟ' -> 月；'2026Q2' -> 季首月；'20260831' -> 日；'2026' -> 年(僅限 4 位純數字)。
    """
    p = str(p).strip()
    p = re.sub(r"[ⓅⓇⓔ\s]+$", "", p)
    m = re.match(r"^(\d{4})M(\d{2})$", p)
    if m:
        return d_month(m.group(1), m.group(2))
    m = re.match(r"^(\d{4})Q([1-4])$", p)
    if m:
        return d_quarter(m.group(1), m.group(2))
    m = re.match(r"^(\d{4})(\d{2})(\d{2})$", p)
    if m:
        return d_day(m.group(1), m.group(2), m.group(3))
    m = re.match(r"^(\d{4})(\d{2})$", p)
    if m and 1 <= int(m.group(2)) <= 12:
        return d_month(m.group(1), m.group(2))
    m = re.match(r"^(\d{4})$", p)
    if m:
        return d_year(m.group(1))
    return None


def clean_obs(rows: Iterable[tuple]) -> list[tuple[str, float]]:
    """去重（後者覆蓋前者）、略過缺值、依日期排序。rows: (date, raw_value)。"""
    out: dict[str, float] = {}
    for d, v in rows:
        if d is None:
            continue
        f = to_float(v)
        if f is None:
            continue
        out[d] = f
    return sorted(out.items())


# ---------- data.gov.tw ----------

def datagov_urls(dataset_id, cache: dict) -> list[str]:
    """回傳資料集所有下載網址（resourceDownloadUrl，分號分隔者展開）。"""
    key = ("datagov", str(dataset_id))
    if key not in cache:
        d = get_json(DATAGOV_API.format(id=dataset_id))
        urls: list[str] = []
        for x in d.get("result", {}).get("distribution", []) or []:
            u = x.get("resourceDownloadUrl") or ""
            urls.extend(p.strip() for p in u.split(";") if p.strip())
        cache[key] = urls
    return cache[key]


def resolve_url(dataset_id, cache: dict, fallback: str, pick: Callable[[str], bool] | None = None) -> str:
    """先問 data.gov.tw 最新網址；問不到（或找不到符合 pick 的）就用 fallback（寫死的舊網址）。"""
    if dataset_id:
        try:
            urls = datagov_urls(dataset_id, cache)
            if pick:
                urls = [u for u in urls if pick(u)]
            if urls:
                return urls[0]
        except Exception:  # noqa: BLE001
            pass
    return fallback


# ---------- 逐條包 try/except ----------

def run_specs(specs: list[dict], fn: Callable[[dict], list[tuple[str, float]]]) -> dict:
    """fn(spec) -> obs list；例外 -> {"error": ...}；空 obs 也視為錯誤（來源可能改版）。"""
    res: dict = {}
    for s in specs:
        sid = s["sid"]
        try:
            obs = fn(s)
            if not obs:
                res[sid] = {"error": "解析後沒有任何資料（來源格式可能改版）"}
            else:
                res[sid] = {"obs": obs}
        except Exception as e:  # noqa: BLE001
            res[sid] = {"error": f"{type(e).__name__}: {e}"[:300]}
    return res


def params(spec: dict) -> dict:
    return spec.get("params") or {}


# ---------- 禮貌節流與台北日期（TWSE／TPEx 日資料用）----------

_last_call: dict = {}


def throttle(key: str, gap: float) -> None:
    """同一站兩次請求至少間隔 gap 秒。"""
    now = time.time()
    last = _last_call.get(key)
    if last is not None and now - last < gap:
        time.sleep(gap - (now - last))
    _last_call[key] = time.time()


def today_taipei():
    """台北今天的日期（測試可 monkeypatch）。"""
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) + timedelta(hours=8)).date()


def recent_weekdays(n_days: int, today=None) -> list:
    """從今天往回 n_days 個日曆日內的平日（新到舊），格式 datetime.date。"""
    from datetime import timedelta
    t = today or today_taipei()
    out = []
    for i in range(n_days):
        d = t - timedelta(days=i)
        if d.weekday() < 5:
            out.append(d)
    return out
