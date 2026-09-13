#!/usr/bin/env python3
"""2026-09-13：官方全球與台灣市場來源 adapter；只取資料，不呼叫模型。

所有 adapter 經由 market_sources.HttpClient，沒有 import-time 網路行為。台灣
OpenAPI 是 latest_only：每次保存該機關公開的當日值，不能拿一筆目前資料假裝
成歷史回補。
"""
from __future__ import annotations

import csv
import io
import math
import re
from datetime import date


ECB_URL = "https://data-api.ecb.europa.eu/service/data/"
BIS_URL = "https://stats.bis.org/api/v1/data/"
BOJ_URL = "https://www.stat-search.boj.or.jp/api/v1/getDataCode"
TWSE_URL = "https://openapi.twse.com.tw/v1/exchangeReport/"
TWSE_HISTORY_URL = "https://www.twse.com.tw/exchangeReport/FMTQIK"
TPEX_URL = "https://www.tpex.org.tw/openapi/v1/"
TAIFEX_URL = "https://openapi.taifex.com.tw/v1/"

# 2026-09-13：可直接放進 registry 的已知官方序列；BIS 未放樣例，因本次無法
# 讀取其 catalog 確認一個特定 credit/liquidity key，不能把猜測當正式資料定義。
SAMPLE_SPECS = [
    {"id": "ecb-eurusd", "provider": "ecb", "series": "EXR/D.USD.EUR.SP00.A",
     "unit": "USD per EUR", "frequency": "daily"},
    {"id": "ecb-dfr", "provider": "ecb", "series": "FM/D.U2.EUR.4F.KR.DFR.LEV",
     "unit": "percent", "frequency": "daily"},
    {"id": "boj-tankan", "provider": "boj", "series": "TK99F1000601GCQ01000",
     "unit": "index", "frequency": "quarterly", "params": {"db": "CO"}},
    {"id": "twse-taiex-close", "provider": "twse", "series": "MI_INDEX",
     "unit": "index points", "frequency": "daily",
     "params": {"row_name": "發行量加權股價指數", "name_field": "指數", "value_field": "收盤指數"}},
    {"id": "twse-taiex-history", "provider": "twse", "series": "FMTQIK",
     "unit": "index points", "frequency": "daily", "data_mode": "rolling_history",
     "params": {"field": "發行量加權股價指數"}},
    {"id": "twse-turnover-history", "provider": "twse", "series": "FMTQIK",
     "unit": "TWD", "frequency": "daily", "data_mode": "rolling_history",
     "params": {"field": "成交金額"}},
]

_IDS = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
_DATE_KEYS = ("date", "Date", "DATE", "日期", "交易日期", "資料日期", "TIME_PERIOD", "TIME", "period")
_VALUE_KEYS = ("value", "VALUE", "OBS_VALUE", "收盤指數", "收盤價", "指數", "成交金額", "未平倉量", "數值")
_SDMX_ATTRIBUTES = {
    "COLLECTION", "DECIMALS", "UNIT_MEASURE", "UNIT_MULT", "TIME_FORMAT", "TITLE_TS", "OBS_COM",
    "PUBL_ECB", "PUBL_MU", "PUBL_PUBLIC", "UNIT_INDEX_BASE", "COMPILATION", "COVERAGE", "BREAKS",
    "COMPILING_ORG", "DISS_ORG", "DOM_SER_IDS", "NAT_TITLE", "SOURCE_AGENCY", "SOURCE_PUB", "TITLE",
    "TITLE_COMPL", "UNIT", "OBS_STATUS", "OBS_CONF", "OBS_PRE_BREAK",
}


def _bad(message):
    raise ValueError(message)


def _as_number(value):
    """Convert official display numbers, including ROC-market comma and bracket negatives."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value) if math.isfinite(value) else None
    text = str(value).strip().replace("，", ",").replace("−", "-").replace("－", "-")
    if not text or text.lower() in ("na", "n/a", "null", "-", "--", "…"):
        return None
    negative = text.startswith("(") and text.endswith(")")
    if negative:
        text = text[1:-1]
    text = text.replace(",", "").replace(" ", "")
    try:
        result = float(text)
    except ValueError:
        return None
    return -result if negative else result


def _period_start(year, month):
    # 2026-09-13：月／季序列以期間首日落帳，與 FRED／BLS 對齊，不把月中查詢誤判成未來資料。
    return date(year, month, 1).isoformat()


def _as_date(value, frequency):
    """Return ISO observation date; ROC years are normalized only when explicit."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        value = str(int(value))
    text = str(value or "").strip()
    if not text:
        return None
    iso = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text)
    if iso:
        try:
            return date(*map(int, iso.groups())).isoformat()
        except ValueError:
            return None
    plain = re.sub(r"[^0-9]", "", text)
    # YYYYMMDD and an explicit three-digit ROC year (e.g. 1140912).
    if len(plain) == 8:
        try:
            return date(int(plain[:4]), int(plain[4:6]), int(plain[6:])).isoformat()
        except ValueError:
            return None
    if len(plain) == 7 and plain[:3] in ("0" + plain[:2], plain[:3]):
        try:
            return date(int(plain[:3]) + 1911, int(plain[3:5]), int(plain[5:])).isoformat()
        except ValueError:
            return None
    if len(plain) == 6:
        try:
            return _period_start(int(plain[:4]), int(plain[4:])) if frequency == "monthly" else None
        except ValueError:
            return None
    # BOJ quarterly dates sometimes appear as YYYYQ1 / YYYY-Q1.
    quarter = re.match(r"^(\d{4})\D*Q?([1-4])$", text, re.I)
    if quarter and frequency == "quarterly":
        return _period_start(int(quarter.group(1)), (int(quarter.group(2)) - 1) * 3 + 1)
    roc = re.match(r"^(\d{2,3})\D+(\d{1,2})\D+(\d{1,2})", text)
    if roc:
        try:
            return date(int(roc.group(1)) + 1911, int(roc.group(2)), int(roc.group(3))).isoformat()
        except ValueError:
            return None
    return None


def _validate(spec, start, end):
    if not isinstance(spec, dict):
        _bad("來源定義必須是物件")
    for key in ("id", "provider", "series", "unit", "frequency"):
        if not isinstance(spec.get(key), str) or not spec[key].strip():
            _bad("來源定義缺少 " + key)
    if not _IDS.fullmatch(spec["id"]):
        _bad("來源代碼只允許小寫英數、底線與連字號")
    if spec["frequency"] not in ("daily", "weekly", "monthly", "quarterly", "annual"):
        _bad("不支援的頻率")
    start_day, end_day = _as_date(start, "daily"), _as_date(end, "daily")
    if start_day is None or end_day is None or start_day > end_day:
        _bad("start 與 end 必須是遞增 YYYY-MM-DD 日期")
    return start_day, end_day


def _row(day, value, dimensions=None, published_at=None, vintage=None, raw_hashes=None):
    number = _as_number(value)
    if day is None or number is None:
        return None
    result = {"date": day, "value": number, "published_at": published_at, "vintage": vintage}
    if dimensions:
        result["dimensions"] = dimensions
    if raw_hashes is not None:
        result["raw_hashes"] = raw_hashes
    return result


def _dedupe(rows):
    unique = {}
    for item in rows:
        if item is not None:
            unique[(item["date"], repr(item.get("dimensions")))] = item
    return [unique[key] for key in sorted(unique)]


def _bounded(rows, start, end):
    """Every provider enforces the caller range even if its official API ignores it."""
    return [row for row in rows if start <= row["date"] <= end]


def _csv_rows(text, spec):
    try:
        records = list(csv.DictReader(io.StringIO(text)))
    except (csv.Error, TypeError) as exc:
        _bad("SDMX CSV 無法解析：" + str(exc))
    rows, signatures = [], set()
    for record in records:
        day = _as_date(record.get("TIME_PERIOD") or record.get("TIME"), spec["frequency"])
        dimensions = {key: value for key, value in record.items()
                      if key not in _SDMX_ATTRIBUTES | {"KEY", "TIME_PERIOD", "TIME", "OBS_VALUE"}
                      and value not in (None, "")}
        # KEY is the authoritative series identity when supplied (ECB); BIS csvfile has no KEY,
        # so its structural columns such as CG_DTYPE are used while annotations are excluded.
        signature = record.get("KEY") or tuple(sorted(dimensions.items()))
        signatures.add(signature)
        # 2026-09-13：PUBL_ECB、DECIMALS 是旗標／顯示精度，不是可比較的發布日或版本。
        rows.append(_row(day, record.get("OBS_VALUE"), dimensions or None))
    # 2026-09-13：單一 spec 不可把不同 SDMX 維度的同日觀測混成一條時間序列。
    if len(signatures) > 1:
        _bad("SDMX 回應包含多個維度序列；請把 series 改成單一完整 key")
    return _dedupe(rows)


def _fetch_ecb(spec, client, start, end):
    text = client.get_text(ECB_URL + spec["series"], params={"format": "csvdata", "startPeriod": start, "endPeriod": end})
    return _bounded(_csv_rows(text, spec), start, end)


def _fetch_bis(spec, client, start, end):
    # series must be the confirmed official FLOW/SDMX_KEY, e.g. supplied from BIS catalog.
    if "/" not in spec["series"] or spec["series"].startswith("/"):
        _bad("BIS series 必須是已確認的 FLOW/SDMX_KEY；本模組不猜測 credit 或 liquidity 代碼")
    _, key = spec["series"].split("/", 1)
    if not key or any(marker in key for marker in ("+", ",", "*")):
        _bad("BIS series 必須指定單一完整 SDMX key，不能合併 CG_DTYPE A/B/C 等多序列")
    text = client.get_text(BIS_URL + spec["series"], params={"startPeriod": start, "endPeriod": end, "format": "csvfile"})
    return _bounded(_csv_rows(text, spec), start, end)


def _fetch_boj(spec, client, start, end):
    params = dict(spec.get("params") or {})
    db = params.pop("db", None)
    if not isinstance(db, str) or not db:
        _bad("BOJ params.db 為必填資料庫代碼")
    params.update({"format": "json", "lang": "en", "db": db, "code": spec["series"],
                   "startDate": _boj_period(start, spec["frequency"], False),
                   "endDate": _boj_period(end, spec["frequency"], True)})
    payload = client.get_json(BOJ_URL, params=params, headers={"Accept-Encoding": "gzip"})
    result_set = payload.get("RESULTSET") if isinstance(payload, dict) else None
    if not isinstance(result_set, list) or len(result_set) != 1 or not isinstance(result_set[0], dict):
        _bad("BOJ RESULTSET 必須剛好含一個已指定 series")
    record = result_set[0]
    if record.get("SERIES_CODE") != spec["series"]:
        _bad("BOJ 回應 series code 與請求不同")
    values = record.get("VALUES")
    if not isinstance(values, dict) or not isinstance(values.get("SURVEY_DATES"), list) or not isinstance(values.get("VALUES"), list):
        _bad("BOJ 回應缺少 VALUES.SURVEY_DATES 或 VALUES.VALUES")
    survey_dates, observations = values["SURVEY_DATES"], values["VALUES"]
    if len(survey_dates) != len(observations):
        _bad("BOJ 調查期間與數值長度不同")
    dimensions = {"series_code": record["SERIES_CODE"], "name": record.get("NAME_OF_TIME_SERIES"),
                  "unit": record.get("UNIT"), "frequency": record.get("FREQUENCY"),
                  "category": record.get("CATEGORY"), "last_update": record.get("LAST_UPDATE")}
    rows = []
    for survey_date, observation in zip(survey_dates, observations):
        day = _boj_survey_date(survey_date, spec["frequency"])
        rows.append(_row(day, observation, dimensions))
    return _bounded(_dedupe(rows), start, end)


def _first(item, keys):
    """Return the first nonblank official field from an ordered field-name list."""
    return next((item[key] for key in keys if key in item and item[key] not in (None, "")), None)


def _boj_period(day, frequency, is_end):
    parsed = date.fromisoformat(day)
    if frequency == "quarterly":
        quarter = (parsed.month - 1) // 3 + 1
        return "{0}{1:02d}".format(parsed.year, quarter)
    return "{0}{1:02d}".format(parsed.year, parsed.month)


def _boj_survey_date(value, frequency):
    text = str(value)
    if frequency == "quarterly" and re.fullmatch(r"\d{6}", text):
        quarter = int(text[-2:])
        if 1 <= quarter <= 4:
            return _period_start(int(text[:4]), (quarter - 1) * 3 + 1)
    return _as_date(text, frequency)


def _json_records(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "Data", "result", "Result", "tables"):
            if isinstance(payload.get(key), list):
                return payload[key]
        return [payload]
    _bad("官方 OpenAPI 回應不是 JSON 物件或列")


def _taiwan_url(provider, series, params):
    endpoint = params.get("endpoint") or series
    if not isinstance(endpoint, str) or not re.fullmatch(r"[A-Za-z0-9_/-]+", endpoint):
        _bad("台灣 OpenAPI endpoint 格式不符")
    return {"twse": TWSE_URL, "tpex": TPEX_URL, "taifex": TAIFEX_URL}[provider] + endpoint.lstrip("/")


def _month_starts(start, end):
    current = date.fromisoformat(start).replace(day=1)
    last = date.fromisoformat(end).replace(day=1)
    while current <= last:
        yield current
        current = date(current.year + (current.month == 12), current.month % 12 + 1, 1)


def _new_raw_hashes(client, receipt_start):
    receipts = getattr(client, "receipts", None)
    if not isinstance(receipts, list):
        return []
    return [item["raw_hash"] for item in receipts[receipt_start:]
            if isinstance(item, dict) and isinstance(item.get("raw_hash"), str) and item["raw_hash"]]


class PartialHistoryError(RuntimeError):
    """2026-09-13：中途限流保留已驗證月份，但不能宣稱回補完成。"""
    def __init__(self, message, observations):
        super().__init__(message)
        self.observations = observations


def _fetch_twse_fmtqik(spec, client, start, end):
    params = dict(spec.get("params") or {})
    field = params.get("field", params.get("value_field", "發行量加權股價指數"))
    if not isinstance(field, str) or not field:
        _bad("TWSE FMTQIK params.field 必須是官方欄位名稱")
    rows = []
    for month in _month_starts(start, end):
        request_date = month.strftime("%Y%m01")
        receipt_start = len(getattr(client, "receipts", []))
        try:
            payload = client.get_json(TWSE_HISTORY_URL, params={"response": "json", "date": request_date})
        except Exception as exc:
            if rows:
                raise PartialHistoryError("歷史回補停在 " + request_date + "：" + str(exc), _bounded(rows, start, end)) from exc
            raise
        raw_hashes = _new_raw_hashes(client, receipt_start)
        if not isinstance(payload, dict) or payload.get("stat") != "OK" or payload.get("date") != request_date:
            _bad("TWSE FMTQIK 月份 " + request_date + " 無有效官方回應")
        fields, data = payload.get("fields"), payload.get("data")
        if not isinstance(fields, list) or not isinstance(data, list) or not data:
            _bad("TWSE FMTQIK 月份 " + request_date + " 缺少資料，不能視為完整歷史")
        try:
            date_index, value_index = fields.index("日期"), fields.index(field)
        except ValueError:
            _bad("TWSE FMTQIK 月份 " + request_date + " 缺少欄位 日期 或 " + field)
        month_rows = []
        for item in data:
            if not isinstance(item, list) or len(item) <= max(date_index, value_index):
                _bad("TWSE FMTQIK 月份 " + request_date + " 有格式不完整的列")
            day = _as_date(item[date_index], "daily")
            if day is None or day[:7] != month.isoformat()[:7]:
                _bad("TWSE FMTQIK 月份 " + request_date + " 含不屬於該月的公開日期")
            row = _row(day, item[value_index], {"data_mode": spec.get("data_mode", "rolling_history"),
                                                 "official_date_field": "日期", "field": field},
                       raw_hashes=raw_hashes)
            if row is None:
                _bad("TWSE FMTQIK 月份 " + request_date + " 有不可解析的 " + field)
            month_rows.append(row)
        if not month_rows:
            _bad("TWSE FMTQIK 月份 " + request_date + " 沒有有效觀測列")
        rows.extend(month_rows)
    return _bounded(_dedupe(rows), start, end)


def _fetch_taiwan(spec, client, start, end):
    params = dict(spec.get("params") or {})
    url = _taiwan_url(spec["provider"], spec["series"], params)
    request_params = params.pop("request_params", None)
    if request_params is not None and not isinstance(request_params, dict):
        _bad("request_params 必須是物件")
    records = _json_records(client.get_json(url, params=request_params))
    name_field, wanted_name = params.get("name_field"), params.get("row_name")
    value_field = params.get("value_field")
    rows = []
    for record in records:
        if not isinstance(record, dict):
            continue
        if wanted_name is not None and record.get(name_field or "名稱") != wanted_name:
            continue
        date_value = _first(record, tuple(params.get("date_fields") or ()) + _DATE_KEYS)
        day = _as_date(date_value, spec["frequency"])
        value = record.get(value_field) if value_field else _first(record, _VALUE_KEYS)
        dimensions = {"data_mode": spec.get("data_mode", "latest_only"),
                      "official_date_field": next((key for key in _DATE_KEYS if key in record), None)}
        if wanted_name is not None:
            dimensions["series_name"] = wanted_name
        rows.append(_row(day, value, dimensions))
    rows = _dedupe(rows)
    return _bounded(rows, start, end)


def fetch_series(spec, client, start, end):
    """Fetch one bounded official series into collector's normalized row contract."""
    start, end = _validate(spec, start, end)
    provider = spec["provider"]
    if provider == "ecb":
        rows = _fetch_ecb(spec, client, start, end)
    elif provider == "bis":
        rows = _fetch_bis(spec, client, start, end)
    elif provider == "boj":
        rows = _fetch_boj(spec, client, start, end)
    elif provider == "twse" and spec["series"] == "FMTQIK":
        rows = _fetch_twse_fmtqik(spec, client, start, end)
    elif provider in ("twse", "tpex", "taifex"):
        rows = _fetch_taiwan(spec, client, start, end)
    else:
        _bad("不支援的全球來源 provider：" + str(provider))
    if not rows:
        _bad(spec["provider"] + " 沒有可驗證的觀測值；請檢查官方 series、欄位和公開日期")
    return rows
