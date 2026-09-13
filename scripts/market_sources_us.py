#!/usr/bin/env python3
"""2026-09-13：美國官方市場資料 adapter；只解析供應商原始觀測，不估算缺值。"""
from __future__ import annotations

import csv
import io
import math
import re
from datetime import date, datetime
from typing import Any, Dict, List, Optional


FRED_OBSERVATIONS = "https://api.stlouisfed.org/fred/series/observations"
FRED_GRAPH = "https://fred.stlouisfed.org/graph/fredgraph.csv"
OFR_TIMESERIES = "https://data.financialresearch.gov/v1/series/timeseries"
NYFED_SOFR = "https://markets.newyorkfed.org/api/rates/secured/sofr/search.json"
CBOE_HISTORY = "https://cdn.cboe.com/api/global/us_indices/daily_prices/{0}_History.csv"
CFTC_DATASETS = {
    "tff": "gpe5-46if",
    "tff_futures_only": "gpe5-46if",
    "disaggregated": "72hh-3qpy",
    "disaggregated_futures_only": "72hh-3qpy",
}


def fetch_series(spec: dict, client: Any, start: str, end: str) -> List[dict]:
    """Fetch one bounded series using the injected provenance-recording client.

    ``client`` owns HTTP, credentials and raw request/response provenance.  This
    module deliberately makes no network call at import time and never fills a
    missing observation with an inferred value.
    """
    _validate_spec(spec, start, end)
    provider = spec["provider"].lower()
    if provider == "fred":
        return _fred(spec, client, start, end)
    if provider in ("ofr", "ofr_stfm"):
        return _ofr(spec, client, start, end)
    if provider in ("cboe", "cboe_csv"):
        return _cboe(spec, client, start, end)
    if provider in ("cftc", "cftc_pre"):
        return _cftc(spec, client, start, end)
    if provider in ("nyfed", "nyfed_sofr"):
        return _nyfed_sofr(spec, client, start, end)
    raise ValueError("unsupported provider: {0}".format(spec["provider"]))


def _validate_spec(spec: dict, start: str, end: str) -> None:
    if not isinstance(spec, dict):
        raise ValueError("spec must be a dict")
    for key in ("id", "provider", "series", "unit", "frequency"):
        if not isinstance(spec.get(key), str) or not spec[key].strip():
            raise ValueError("spec.{0} must be a non-empty string".format(key))
    if "params" in spec and not isinstance(spec["params"], dict):
        raise ValueError("spec.params must be a dict")
    start_day, end_day = _day(start, "start"), _day(end, "end")
    if start_day > end_day:
        raise ValueError("start must be on or before end")


def _day(raw: Any, label: str) -> str:
    if not isinstance(raw, str):
        raise ValueError("{0} must be YYYY-MM-DD".format(label))
    try:
        parsed = date.fromisoformat(raw)
    except ValueError:
        raise ValueError("{0} must be YYYY-MM-DD".format(label))
    if parsed.isoformat() != raw:
        raise ValueError("{0} must be YYYY-MM-DD".format(label))
    return raw


def _number(raw: Any) -> Optional[float]:
    if raw is None or isinstance(raw, bool):
        return None
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw or raw in (".", "NA", "N/A", "null", "None"):
            return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def _row(day_value: Any, value: Any, published_at: Any = None,
         vintage: Any = None, dimensions: Optional[Dict[str, Any]] = None) -> Optional[dict]:
    try:
        obs_day = _day(str(day_value)[:10], "observation date")
    except ValueError:
        return None
    numeric = _number(value)
    if numeric is None:
        return None
    result = {"date": obs_day, "value": numeric, "published_at": None, "vintage": None}
    if isinstance(published_at, str) and published_at:
        result["published_at"] = published_at
    if isinstance(vintage, str) and vintage:
        result["vintage"] = vintage
    if dimensions:
        result["dimensions"] = dimensions
    return result


def _bounded(rows: List[dict], start: str, end: str) -> List[dict]:
    bounded = [item for item in rows if start <= item["date"] <= end]
    if not bounded:
        raise ValueError("response contains no valid observations in requested range")
    return sorted(bounded, key=lambda item: item["date"])


def _params(spec: dict) -> dict:
    return dict(spec.get("params") or {})


def _fred(spec: dict, client: Any, start: str, end: str) -> List[dict]:
    """FRED API supports vintage dates only with a registered API key."""
    key = client.get_env("FRED_API_KEY")
    requested_vintage = spec.get("vintage")
    vintage_history = spec.get("data_mode") == "point_in_time"
    if vintage_history and not key:
        raise RuntimeError("requires FRED_API_KEY")
    if requested_vintage is not None:
        _day(requested_vintage, "spec.vintage")
        if requested_vintage > end:
            raise ValueError("vintage must not be after requested end")
    if key:
        request = _params(spec)
        request.update({
            "series_id": spec["series"], "api_key": key, "file_type": "json",
            "observation_start": start, "observation_end": end,
        })
        if requested_vintage:
            request["vintage_dates"] = requested_vintage
        elif vintage_history:
            # 2026-09-13：ALFRED 保存實際可得版本区間，不能把今天修訂值回填當時資訊集。
            request.update({"realtime_start": "1776-07-04", "realtime_end": end, "output_type": 1})
        request.update({"limit": 100000, "offset": 0})
        rows = []
        while True:
            raw = client.get_json(FRED_OBSERVATIONS, params=dict(request))
            if not isinstance(raw, dict) or not isinstance(raw.get("observations"), list):
                raise ValueError("malformed FRED observations response")
            for item in raw["observations"]:
                if not isinstance(item, dict):
                    continue
                version = item.get("realtime_start") if vintage_history else requested_vintage
                if version and _day(version, "FRED vintage") > end:
                    continue
                row = _row(item.get("date"), item.get("value"), vintage=version)
                if row:
                    rows.append(row)
            request["offset"] += len(raw["observations"])
            if request["offset"] >= int(raw.get("count", len(raw["observations"]))):
                break
            if not raw["observations"] or request["offset"] >= 1000000:
                raise ValueError("FRED pagination incomplete or safety limit reached")
        return _bounded(rows, start, end)
    if requested_vintage:
        raise RuntimeError("requires FRED_API_KEY")
    raw = client.get_text(FRED_GRAPH, params={"id": spec["series"], "cosd": start, "coed": end})
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("empty FRED CSV response")
    reader = csv.DictReader(io.StringIO(raw))
    if not reader.fieldnames or len(reader.fieldnames) < 2:
        raise ValueError("malformed FRED CSV response")
    if spec["series"] not in reader.fieldnames:
        raise ValueError("FRED CSV does not contain requested series")
    value_field = spec["series"]
    rows = []
    for item in reader:
        row = _row(item.get(reader.fieldnames[0]), item.get(value_field))
        if row:
            rows.append(row)
    return _bounded(rows, start, end)


def _ofr(spec: dict, client: Any, start: str, end: str) -> List[dict]:
    request = _params(spec)
    request.update({"mnemonic": spec["series"], "start_date": start, "end_date": end})
    raw = client.get_json(OFR_TIMESERIES, params=request)
    if not isinstance(raw, list):
        raise ValueError("malformed OFR STFM response")
    rows = []
    for item in raw:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        row = _row(item[0], item[1])
        if row:
            rows.append(row)
    return _bounded(rows, start, end)


def _cboe(spec: dict, client: Any, start: str, end: str) -> List[dict]:
    series = spec["series"].upper()
    if not re.match(r"^[A-Z0-9]+$", series):
        raise ValueError("Cboe series must contain only letters and digits")
    raw = client.get_text(CBOE_HISTORY.format(series))
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("empty Cboe CSV response")
    reader = csv.DictReader(io.StringIO(raw))
    if not reader.fieldnames:
        raise ValueError("malformed Cboe CSV response")
    normalized = {name.strip().upper(): name for name in reader.fieldnames if name}
    date_field = normalized.get("DATE")
    value_name = str(_params(spec).get("field", "CLOSE")).upper()
    value_field = normalized.get(value_name)
    if not date_field or not value_field:
        raise ValueError("Cboe CSV lacks DATE or requested value field")
    rows = []
    for item in reader:
        raw_date = item.get(date_field)
        # Cboe's historical files use MM/DD/YYYY for older (and current) rows.
        # Normalize that documented CSV convention before applying the boundary.
        if isinstance(raw_date, str) and "/" in raw_date:
            try:
                raw_date = datetime.strptime(raw_date.strip(), "%m/%d/%Y").date().isoformat()
            except ValueError:
                raw_date = None
        row = _row(raw_date, item.get(value_field))
        if row:
            rows.append(row)
    return _bounded(rows, start, end)


def _cftc(spec: dict, client: Any, start: str, end: str) -> List[dict]:
    dataset = CFTC_DATASETS.get(spec["series"].lower())
    if not dataset:
        raise ValueError("CFTC series must be TFF or disaggregated futures-only")
    field = spec.get("field")
    if not isinstance(field, str) or not re.match(r"^[a-z][a-z0-9_]*$", field):
        raise ValueError("CFTC spec.field must be a Socrata field name")
    options = _params(spec)
    if any(key.startswith("$") for key in options):
        raise ValueError("CFTC reserved query parameters cannot override bounded request")
    where = ("report_date_as_yyyy_mm_dd >= '{0}T00:00:00.000' AND "
             "report_date_as_yyyy_mm_dd <= '{1}T00:00:00.000'").format(start, end)
    market_code = options.pop("market_code", None)
    if market_code is not None:
        if not isinstance(market_code, str) or not market_code:
            raise ValueError("CFTC params.market_code must be a non-empty string")
        where += " AND cftc_contract_market_code = '{0}'".format(market_code.replace("'", "''"))
    extra_where = options.pop("where", None)
    if extra_where is not None:
        if not isinstance(extra_where, str) or not extra_where.strip():
            raise ValueError("CFTC params.where must be a non-empty string")
        where += " AND ({0})".format(extra_where)
    request = {"$where": where, "$order": "report_date_as_yyyy_mm_dd ASC", "$limit": 50000}
    request.update(options)
    raw = client.get_json("https://publicreporting.cftc.gov/resource/{0}.json".format(dataset),
                          params=request)
    if not isinstance(raw, list):
        raise ValueError("malformed CFTC PRE response")
    if len(raw) >= 50000:
        raise ValueError("CFTC response reached page limit; narrow market selection")
    rows = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        dimensions = {}
        for source, target in (("cftc_contract_market_code", "contract_market_code"),
                               ("market_and_exchange_names", "market_and_exchange_name")):
            if isinstance(item.get(source), str) and item[source]:
                dimensions[target] = item[source]
        # CFTC documents only current/future release schedules, not a complete
        # historic release-date series. Do not manufacture a Friday timestamp.
        row = _row(item.get("report_date_as_yyyy_mm_dd"), item.get(field), dimensions=dimensions)
        if row:
            rows.append(row)
    return _bounded(rows, start, end)


def _nyfed_sofr(spec: dict, client: Any, start: str, end: str) -> List[dict]:
    if spec["series"].upper() != "SOFR":
        raise ValueError("NY Fed adapter currently supports only SOFR")
    request = _params(spec)
    request.update({"startDate": start, "endDate": end, "type": "rate"})
    raw = client.get_json(NYFED_SOFR, params=request)
    if not isinstance(raw, dict):
        raise ValueError("malformed NY Fed SOFR response")
    source_rows = raw.get("refRates")
    if not isinstance(source_rows, list):
        raise ValueError("malformed NY Fed SOFR response")
    rows = []
    for item in source_rows:
        if not isinstance(item, dict):
            continue
        row = _row(item.get("effectiveDate"), item.get("percentRate"))
        if row:
            rows.append(row)
    return _bounded(rows, start, end)
