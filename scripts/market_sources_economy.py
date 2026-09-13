#!/usr/bin/env python3
"""Small adapters for official US economic data APIs.

The adapters deliberately accept a very small client protocol so they can be
used by the market collector and tested without network access.  Official
endpoint references:

* BLS JSON API: https://www.bls.gov/developers/api_signature_v2.htm
* BEA API: https://apps.bea.gov/api/bea_web_service_api_user_guide.pdf
* EIA API v2: https://www.eia.gov/opendata/documentation.php
* SEC companyfacts: https://www.sec.gov/edgar/sec-api-documentation
* Fiscal Data API: https://fiscaldata.treasury.gov/api-documentation/

Fiscal Data is bounded to the verified Debt to the Penny v2 table.  It is a
public endpoint and does not require an API key.
"""
from __future__ import annotations

import calendar
import datetime as _dt
import math
import re
from typing import Any, Dict, Iterable, List, Mapping, Optional


BLS_V1_URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
BLS_V2_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
BEA_URL = "https://apps.bea.gov/api/data/"
EIA_URL = "https://api.eia.gov/v2"
SEC_COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
FISCALDATA_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny"

SUPPORTED_PROVIDERS = ("bls", "bea", "eia", "sec", "fiscaldata")
FISCALDATA_FIELDS = frozenset((
    "debt_held_public_amt",
    "intragov_hold_amt",
    "tot_pub_debt_out_amt",
))

# 2026-09-13：新增 bounded official adapters，先把四個已選定且有可測
# JSON schema 的來源隔離；FiscalData 已用官方即時回應核對欄位。
SAMPLE_SPECS = (
    {
        "id": "us.cpi.all_items",
        "provider": "bls",
        "series": "CUSR0000SA0",
        "unit": "index",
        "frequency": "monthly",
        "params": {},
    },
    {
        "id": "us.real_gdp_growth",
        "provider": "bea",
        "series": "T10101:1",
        "unit": "percent",
        "frequency": "quarterly",
        "params": {"datasetname": "NIPA", "tablename": "T10101"},
    },
    {
        "id": "us.crude_oil.stocks",
        "provider": "eia",
        "series": "WCESTUS1",
        "unit": "thousand_barrels",
        "frequency": "weekly",
        "params": {"route": "petroleum/stoc/wstk"},
    },
    {
        "id": "us.company.revenue",
        "provider": "sec",
        "series": "us-gaap:Revenues",
        "unit": "USD",
        "frequency": "annual",
        "params": {"cik": "0000320193"},
    },
    {
        "id": "us.treasury.debt_held_public",
        "provider": "fiscaldata",
        "series": "debt_held_public_amt",
        "unit": "USD",
        "frequency": "daily",
        "params": {"date_field": "record_date"},
    },
)


class EconomySourceError(RuntimeError):
    """A bounded, user-actionable source or payload error."""


def sample_specs() -> List[Dict[str, Any]]:
    """Return independent sample specifications for callers and smoke tests."""
    return [dict(spec, params=dict(spec.get("params") or {})) for spec in SAMPLE_SPECS]


def _require_spec(spec: Mapping[str, Any]) -> None:
    for key in ("id", "provider", "series", "unit", "frequency"):
        if key not in spec or spec[key] in (None, ""):
            raise EconomySourceError("spec requires " + key)
    if not isinstance(spec.get("params", {}), Mapping):
        raise EconomySourceError("spec params must be an object")


def _date(value: str, label: str) -> _dt.date:
    try:
        parsed = _dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        raise EconomySourceError("invalid " + label + "; expected YYYY-MM-DD")
    if parsed.isoformat() != value:
        raise EconomySourceError("invalid " + label + "; expected YYYY-MM-DD")
    return parsed


def _number(value: Any) -> Optional[float]:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if text in {"", "...", "-", "NA", "N/A", "null", "None"}:
            return None
        # BEA appends a footnote marker such as (D) to some values.
        text = re.sub(r"\s*\([^)]*\)\s*$", "", text).strip()
    else:
        text = value
    try:
        number = float(text)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def _record(
    date_value: str,
    value: Any,
    published_at: Optional[str] = None,
    vintage: Optional[str] = None,
    dimensions: Optional[Mapping[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    number = _number(value)
    if number is None:
        return None
    try:
        day = _date(date_value, "observation date")
    except EconomySourceError:
        return None
    row: Dict[str, Any] = {
        "date": day.isoformat(),
        "value": number,
        "published_at": published_at,
        "vintage": vintage,
    }
    if dimensions:
        row["dimensions"] = dict(dimensions)
    return row


def _in_range(row: Mapping[str, Any], start: _dt.date, end: _dt.date) -> bool:
    try:
        day = _date(str(row["date"]), "observation date")
    except EconomySourceError:
        return False
    return start <= day <= end


def _finish(rows: Iterable[Optional[Dict[str, Any]]], start: _dt.date, end: _dt.date) -> List[Dict[str, Any]]:
    out = [row for row in rows if row is not None and _in_range(row, start, end)]
    # Keep same-date rows when they carry distinct vintages (SEC restatements).
    # Only exact duplicate payloads are removed.
    unique: List[Dict[str, Any]] = []
    seen = set()
    for row in out:
        marker = repr(sorted(row.items()))
        if marker not in seen:
            seen.add(marker)
            unique.append(row)
    unique.sort(key=lambda row: (row["date"], row.get("published_at") or "", row.get("vintage") or ""))
    return unique


def _env(client: Any, name: str, provider: str) -> str:
    value = client.get_env(name)
    if not value:
        raise EconomySourceError("" + provider + " requires " + name)
    return str(value)


def _json(client: Any, url: str, params: Optional[Mapping[str, Any]] = None, headers: Optional[Mapping[str, str]] = None) -> Any:
    try:
        return client.get_json(url, params=dict(params or {}), headers=headers)
    except Exception as exc:
        # Do not include request arguments: they may contain API credentials.
        raise EconomySourceError("official source request failed") from exc


def _post_json(client: Any, url: str, payload: Mapping[str, Any], headers: Optional[Mapping[str, str]] = None) -> Any:
    try:
        return client.post_json(url, dict(payload), headers=headers)
    except Exception as exc:
        raise EconomySourceError("official source request failed") from exc


def _period_date(year: Any, period: Any) -> Optional[str]:
    """Map BLS periods to period starts; M13 annual averages are excluded."""
    try:
        year_number = int(str(year))
    except (TypeError, ValueError):
        return None
    match = re.fullmatch(r"([MQA])(\d{2})", str(period or "").upper())
    if not match:
        return None
    kind, number = match.group(1), int(match.group(2))
    if kind == "M":
        if not 1 <= number <= 12:  # M13 is an annual average, not a month.
            return None
        return "{0:04d}-{1:02d}-01".format(year_number, number)
    if kind == "Q" and 1 <= number <= 4:
        return "{0:04d}-{1:02d}-01".format(year_number, (number - 1) * 3 + 1)
    if kind == "A" and number == 1:
        return "{0:04d}-01-01".format(year_number)
    return None


def _fetch_bls(spec: Mapping[str, Any], client: Any, start: _dt.date, end: _dt.date) -> List[Dict[str, Any]]:
    params = dict(spec.get("params") or {})
    series = spec["series"]
    # 2026-09-13：單一序列不得混收別的系列；長歷史按 BLS 每次年份上限分段。
    if not isinstance(series, str):
        raise EconomySourceError("BLS requires one series per specification")
    series_ids = [series]
    payload: Dict[str, Any] = {
        "seriesid": series_ids,
        "startyear": str(start.year),
        "endyear": str(end.year),
    }
    payload.update({key: value for key, value in params.items() if key not in {"seriesid", "startyear", "endyear", "registrationkey"}})
    key = client.get_env("BLS_API_KEY")
    if key:
        payload["registrationkey"] = str(key)
    # BLS v1 is the public no-registration endpoint; registered requests use
    # v2 and carry the key in the documented JSON payload.
    rows: List[Optional[Dict[str, Any]]] = []
    span = 20 if key else 10
    for year in range(start.year, end.year + 1, span):
        payload["startyear"] = str(year)
        payload["endyear"] = str(min(year + span - 1, end.year))
        data = _post_json(client, BLS_V2_URL if key else BLS_V1_URL, payload)
        if not isinstance(data, Mapping) or data.get("status") != "REQUEST_SUCCEEDED":
            raise EconomySourceError("BLS returned an unsuccessful response")
        result = data.get("Results", {})
        for series_row in result.get("series", []) if isinstance(result, Mapping) else []:
            if not isinstance(series_row, Mapping) or series_row.get("seriesID") != series:
                continue
            for item in series_row.get("data", []) or []:
                if not isinstance(item, Mapping):
                    continue
                observed = _period_date(item.get("year"), item.get("period"))
                if observed is not None:
                    rows.append(_record(observed, item.get("value")))
    return _finish(rows, start, end)


def _bea_period_date(value: Any) -> Optional[str]:
    text = str(value or "").strip().upper()
    match = re.fullmatch(r"(\d{4})(?:Q([1-4])|M(0[1-9]|1[0-2]))?", text)
    if not match:
        return None
    year = int(match.group(1))
    # 2026-09-13：季／年觀測日改為期間首日，與 FRED、BLS、ECB／BIS／BOJ 及本檔月頻一致，
    # 否則同一季度的 BEA 與 FRED 會標成不同日期，無法同日對帳。
    if match.group(2):
        quarter = int(match.group(2))
        month = quarter * 3 - 2
        return "{0:04d}-{1:02d}-01".format(year, month)
    if match.group(3):
        month = int(match.group(3))
        return "{0:04d}-{1:02d}-01".format(year, month)
    return "{0:04d}-01-01".format(year)


def _fetch_bea(spec: Mapping[str, Any], client: Any, start: _dt.date, end: _dt.date) -> List[Dict[str, Any]]:
    key = _env(client, "BEA_API_KEY", "BEA")
    params = dict(spec.get("params") or {})
    query: Dict[str, Any] = {
        "UserID": key,
        "method": params.pop("method", "GETDATA"),
        "ResultFormat": params.pop("ResultFormat", "JSON"),
        "datasetname": params.pop("datasetname", "NIPA"),
        "Frequency": params.pop("Frequency", "Q" if str(spec.get("frequency", "")).lower().startswith("q") else "M"),
        "Year": params.pop("Year", ",".join(str(year) for year in range(start.year, end.year + 1))),
    }
    table = params.pop("tablename", params.pop("TableName", None))
    if table:
        query["TableName"] = table
    line = params.pop("LineNumber", None)
    if line is not None:
        query["LineNumber"] = line
    query.update(params)
    data = _json(client, BEA_URL, query)
    if not isinstance(data, Mapping):
        raise EconomySourceError("BEA returned an invalid response")
    envelope = data.get("BEAAPI", {})
    result = envelope.get("Results", {}) if isinstance(envelope, Mapping) else {}
    if isinstance(result, Mapping) and result.get("Error"):
        raise EconomySourceError("BEA returned an unsuccessful response")
    observations = result.get("Data", []) if isinstance(result, Mapping) else []
    target = str(spec["series"])
    target_line = target.rsplit(":", 1)[-1] if ":" in target else None
    rows: List[Optional[Dict[str, Any]]] = []
    for item in observations:
        if not isinstance(item, Mapping):
            continue
        line_number = str(item.get("LineNumber", ""))
        if not target_line or line_number != target_line:
            continue
        observed = _bea_period_date(item.get("TimePeriod"))
        if observed is None:
            continue
        dimensions = {}
        for key in ("LineNumber", "LineDescription", "CL_UNIT", "METRIC_NAME"):
            if key in item and item[key] not in (None, ""):
                dimensions[key] = item[key]
        rows.append(_record(observed, item.get("DataValue"), dimensions=dimensions or None))
    return _finish(rows, start, end)


def _fetch_eia(spec: Mapping[str, Any], client: Any, start: _dt.date, end: _dt.date) -> List[Dict[str, Any]]:
    key = _env(client, "EIA_API_KEY", "EIA")
    params = dict(spec.get("params") or {})
    route = str(params.pop("route", "" )).strip("/")
    if not route:
        raise EconomySourceError("EIA spec requires params.route")
    frequency = str(spec["frequency"]).strip().lower()
    monthly_request = frequency in {"m", "month", "monthly"}
    query: Dict[str, Any] = {
        "api_key": key,
        "frequency": spec["frequency"],
        "data[]": params.pop("data", "value"),
        "start": start.strftime("%Y-%m") if monthly_request else start.isoformat(),
        "end": end.strftime("%Y-%m") if monthly_request else end.isoformat(),
    }
    try:
        length = int(params.pop("length", 5000))
        offset = int(params.pop("offset", 0))
    except (TypeError, ValueError):
        raise EconomySourceError("EIA length and offset must be integers")
    if not 1 <= length <= 5000 or offset < 0:
        raise EconomySourceError("EIA page length must be between 1 and 5000")
    series = spec["series"]
    if series:
        query["facets[seriesId][]"] = series
    query.update(params)
    rows: List[Optional[Dict[str, Any]]] = []
    # 2026-09-13：EIA 的單頁上限是 5,000；依 total/offset 逐頁回補，並
    # 對不一致的 total 或空頁明確失敗，避免把截斷資料當完整歷史。
    pages = 0
    while True:
        page_query = dict(query, length=length, offset=offset)
        data = _json(client, EIA_URL + "/" + route + "/data/", page_query)
        response = data.get("response", {}) if isinstance(data, Mapping) else {}
        if not isinstance(response, Mapping):
            raise EconomySourceError("EIA returned an invalid response")
        observations = response.get("data", [])
        if not isinstance(observations, list):
            raise EconomySourceError("EIA returned an invalid data page")
        try:
            total = int(response.get("total", offset + len(observations)))
        except (TypeError, ValueError):
            raise EconomySourceError("EIA returned an invalid total")
        if total < offset + len(observations):
            raise EconomySourceError("EIA page exceeds reported total")
        for item in observations:
            if not isinstance(item, Mapping):
                continue
            observed = _eia_period_date(item.get("period"), spec.get("frequency"))
            if observed is None:
                continue
            published = item.get("published_at") or item.get("publishedAt")
            vintage = item.get("vintage") or item.get("realtime_start")
            rows.append(_record(observed, item.get("value"), published_at=published, vintage=vintage))
        pages += 1
        next_offset = offset + len(observations)
        if next_offset >= total:
            break
        if not observations:
            raise EconomySourceError("EIA returned a truncated page")
        offset = next_offset
        if pages >= 10000:
            raise EconomySourceError("EIA pagination exceeded safety limit")
    return _finish(rows, start, end)


def _eia_period_date(value: Any, frequency: Any) -> Optional[str]:
    text = str(value or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text
    if re.fullmatch(r"\d{4}-\d{2}", text):
        return text + "-01"
    if re.fullmatch(r"\d{4}", text):
        # A year observation is represented by its period end, consistent
        # with the quarterly BEA mapping and the output's date-only contract.
        return text + "-12-31"
    return None


def _fetch_fiscaldata(spec: Mapping[str, Any], client: Any, start: _dt.date, end: _dt.date) -> List[Dict[str, Any]]:
    """Read the verified Treasury Debt to the Penny table.

    Fiscal Data's ``record_date`` is the observation date, not a release timestamp;
    its ``meta.total-pages`` value is the authoritative pagination bound.
    """
    field = str(spec["series"])
    if field not in FISCALDATA_FIELDS:
        raise EconomySourceError("Fiscal Data series is unavailable")
    params = dict(spec.get("params") or {})
    date_field = str(params.pop("date_field", "record_date"))
    if date_field != "record_date":
        raise EconomySourceError("Fiscal Data requires date_field=record_date")
    try:
        page_size = int(params.pop("page_size", 1000))
    except (TypeError, ValueError):
        raise EconomySourceError("Fiscal Data page_size must be an integer")
    if not 1 <= page_size <= 5000:
        raise EconomySourceError("Fiscal Data page_size must be between 1 and 5000")
    extra_filter = params.pop("filter", None)
    date_filter = "record_date:gte:{0},record_date:lte:{1}".format(start.isoformat(), end.isoformat())
    if extra_filter:
        date_filter += "," + str(extra_filter)
    query: Dict[str, Any] = {"filter": date_filter, "page[size]": page_size}
    query.update(params)
    rows: List[Optional[Dict[str, Any]]] = []
    page_number = 1
    total_pages: Optional[int] = None
    while True:
        page_query = dict(query, **{"page[number]": page_number})
        data = _json(client, FISCALDATA_URL, page_query)
        if not isinstance(data, Mapping) or not isinstance(data.get("data"), list):
            raise EconomySourceError("Fiscal Data returned an invalid response")
        meta = data.get("meta")
        if not isinstance(meta, Mapping) or "total-pages" not in meta:
            raise EconomySourceError("Fiscal Data response lacks total-pages metadata")
        try:
            observed_total_pages = int(meta["total-pages"])
        except (TypeError, ValueError):
            raise EconomySourceError("Fiscal Data returned an invalid total-pages")
        if observed_total_pages < 1:
            raise EconomySourceError("Fiscal Data returned an invalid total-pages")
        if total_pages is None:
            total_pages = observed_total_pages
        elif observed_total_pages != total_pages:
            raise EconomySourceError("Fiscal Data total-pages changed during pagination")
        for item in data["data"]:
            if not isinstance(item, Mapping):
                continue
            observed = item.get(date_field)
            if observed is None:
                continue
            observed = str(observed)[:10]
            rows.append(_record(observed, item.get(field)))
        if page_number >= total_pages:
            break
        page_number += 1
        if page_number > 10000:
            raise EconomySourceError("Fiscal Data pagination exceeded safety limit")
    return _finish(rows, start, end)


def _sec_concept(series: Any) -> tuple[str, str]:
    text = str(series)
    if ":" in text:
        namespace, concept = text.split(":", 1)
        return namespace, concept
    return "us-gaap", text


def _fetch_sec(spec: Mapping[str, Any], client: Any, start: _dt.date, end: _dt.date) -> List[Dict[str, Any]]:
    user_agent = _env(client, "SEC_USER_AGENT", "SEC")
    params = dict(spec.get("params") or {})
    cik = str(params.get("cik", "")).strip()
    if not re.fullmatch(r"\d{1,10}", cik):
        raise EconomySourceError("SEC spec requires params.cik")
    namespace, concept = _sec_concept(spec["series"])
    data = _json(
        client,
        SEC_COMPANYFACTS_URL.format(cik=cik.zfill(10)),
        headers={"User-Agent": user_agent, "Accept": "application/json"},
    )
    facts = data.get("facts", {}) if isinstance(data, Mapping) else {}
    concept_data = facts.get(namespace, {}).get(concept, {}) if isinstance(facts, Mapping) else {}
    units = concept_data.get("units", {}) if isinstance(concept_data, Mapping) else {}
    unit = str(params.get("unit", spec.get("unit", "")))
    # 2026-09-13：缺指定單位不能偷換單位；流量要區分單季、全年與累計。
    if unit not in units:
        raise EconomySourceError("SEC requested unit is unavailable")
    unit_rows = units[unit]
    default_kind = "annual" if str(spec["frequency"]).lower() == "annual" else (
        "quarter" if str(spec["frequency"]).lower() in {"quarter", "quarterly"} else "instant"
    )
    period_kind = str(params.get("period_kind", default_kind)).lower()
    rows: List[Optional[Dict[str, Any]]] = []
    for item in unit_rows:
        if not isinstance(item, Mapping) or not item.get("end"):
            continue
        observed = str(item["end"])
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", observed):
            continue
        if period_kind == "instant":
            if item.get("start"):
                continue
        elif not item.get("start"):
            continue
        else:
            start_date = _date(str(item["start"]), "start")
            if period_kind == "ytd":
                try:
                    fiscal_start_month = int(params.get("fiscal_start_month", 1))
                except (TypeError, ValueError):
                    raise EconomySourceError("SEC fiscal_start_month must be an integer")
                if not 1 <= fiscal_start_month <= 12 or start_date.month != fiscal_start_month or start_date.day != 1:
                    continue
            duration = (_date(observed, "end") - start_date).days
            low, high = {
                "annual": (300, 400),
                "quarter": (60, 120),
                "ytd": (60, 300),
            }.get(period_kind, (0, -1))
            if not low <= duration <= high:
                continue
        filed = item.get("filed") or item.get("filed_at")
        if filed:
            filed = str(filed)[:10]
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", filed):
                filed = None
        # Preserve every distinct filed/accession version.  Dropping same-date
        # facts by latest filed value would create undocumented survivor bias.
        vintage = item.get("accn") or None
        dimensions = {key: item[key] for key in ("form", "fp", "fy", "frame", "start") if item.get(key) is not None}
        rows.append(_record(observed, item.get("val"), published_at=filed, vintage=vintage, dimensions=dimensions or None))
    return _finish(rows, start, end)


def fetch_series(spec: Mapping[str, Any], client: Any, start: str, end: str) -> List[Dict[str, Any]]:
    """Fetch one bounded series using a caller supplied client.

    The client must expose ``get_json``, ``post_json`` and ``get_env``.  A
    missing provider key raises :class:`EconomySourceError`; credentials are
    never included in exception text or request diagnostics.
    """
    _require_spec(spec)
    start_day, end_day = _date(start, "start"), _date(end, "end")
    if start_day > end_day:
        raise EconomySourceError("start must not be after end")
    provider = str(spec["provider"]).strip().lower()
    if provider == "bls":
        return _fetch_bls(spec, client, start_day, end_day)
    if provider == "bea":
        return _fetch_bea(spec, client, start_day, end_day)
    if provider == "eia":
        return _fetch_eia(spec, client, start_day, end_day)
    if provider == "fiscaldata":
        return _fetch_fiscaldata(spec, client, start_day, end_day)
    if provider == "sec":
        return _fetch_sec(spec, client, start_day, end_day)
    raise EconomySourceError("unsupported economy provider: " + provider)


__all__ = ["EconomySourceError", "SAMPLE_SPECS", "SUPPORTED_PROVIDERS", "fetch_series", "sample_specs"]
