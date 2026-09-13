#!/usr/bin/env python3
"""2026-09-13：把官方觀測史整理成市況歷史比較與跨市場事實卡。"""
from __future__ import annotations

import json
import math
import calendar
from datetime import date, timedelta
from pathlib import Path


WINDOWS = (("7d", 7, "7 日"), ("30d", 30, "30 日"),
           ("90d", 90, "90 日"), ("365d", 365, "365 日"))
REGIONS = (("TW", "台灣"), ("JP", "日本"), ("EA", "歐洲"), ("US", "美國"))
MONITOR_REFS = {
    "TW": ("monitor:twii", "monitor:usdtwd"),
    "JP": ("monitor:n225", "monitor:usdjpy"),
    "EA": ("monitor:dax", "monitor:stoxx", "monitor:eurusd"),
    "US": ("monitor:sp500",),
}
SOURCE_REFS = {
    "TW": ("twse_taiex_history", "twse_turnover_history", "taifex_putcall_oi", "taifex_putcall_volume"),
    "JP": ("boj_tankan_manufacturing",),
    "EA": ("ecb_eurusd", "ecb_deposit_rate"),
    "US": ("fred_treasury_10y", "fred_dollar"),
}
REQUIREMENTS = {
    "TW": (("台灣加權指數", ("source:twse_taiex_history", "monitor:twii")),
           ("成交金額", ("source:twse_turnover_history",)),
           ("USD/TWD", ("monitor:usdtwd",)),
           ("TAIFEX", ("source:taifex_putcall_oi", "source:taifex_putcall_volume"))),
    "JP": (("日經 225", ("monitor:n225",)), ("USD/JPY", ("monitor:usdjpy",)),
           ("日銀短觀", ("source:boj_tankan_manufacturing",))),
    "EA": (("DAX", ("monitor:dax",)), ("STOXX 50", ("monitor:stoxx",)),
           ("EUR/USD", ("source:ecb_eurusd", "monitor:eurusd")),
           ("ECB 存款利率", ("source:ecb_deposit_rate",))),
    "US": (("S&P 500", ("monitor:sp500",)),
           ("美國十年期公債殖利率", ("source:fred_treasury_10y",)),
           ("美元指數", ("source:fred_dollar",))),
}
MISSING = (
    ("bea_real_gdp_growth", "缺少 BEA 官方年化季增率，無法直接核對 GDP 成長口徑。", "source:fred_real_gdp", "FRED 實質 GDP 水準可算現行修訂後季增率，但不是 BEA 發布值的完整替代。"),
    ("eia_crude_stocks", "缺少 EIA 庫存，不能判斷油價變動是否由實體庫存收緊支持。", None, "價格反映多種力量，不能冒充庫存。"),
    ("sec_msft_capex", "缺少微軟申報資本支出，不能硬推 AI 產業資本投入或回報。", None, "其他市場或公司指標不能完整替代公司申報。"),
    ("sec_amzn_capex", "缺少亞馬遜申報資本支出，不能硬推 AI 產業資本投入或回報。", None, "其他市場或公司指標不能完整替代公司申報。"),
    ("alfred_cpiaucsl", "缺少 CPI 當時可得版本，不能做無前視偏誤的通膨回測。", "source:fred_cpi", "FRED 現行修訂史只適合描述現在看到的歷史。"),
    ("alfred_payems", "缺少非農就業當時可得版本，不能做無前視偏誤的就業回測。", "source:fred_payrolls", "FRED 現行修訂史只適合描述現在看到的歷史。"),
)


def _day(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _load(path):
    try:
        with Path(path).open(encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, ValueError):
        return None


def _current_rows(stored, today):
    """取截至 today 的現行觀測史；latest_revised 不冒充歷史 vintage。"""
    chosen = {}
    mode = (stored or {}).get("data_mode")
    for raw in (stored or {}).get("observations", []):
        when = _day(raw.get("date"))
        published = _day(raw.get("published_at"))
        vintage = _day(raw.get("vintage"))
        if not when or when > today or not _number(raw.get("value")):
            continue
        if published and published > today:
            continue
        if mode == "point_in_time" and vintage and vintage > today:
            continue
        old = chosen.get(raw["date"])
        version = raw.get("published_at") or raw.get("vintage") or ""
        old_version = (old or {}).get("published_at") or (old or {}).get("vintage") or ""
        if old and old_version and version and version < old_version:
            continue
        chosen[raw["date"]] = raw
    return [chosen[key] for key in sorted(chosen)]


def _change_kind(frequency, days):
    if frequency in ("daily", "weekly"):
        return "window" if frequency == "daily" or days >= 30 else None
    if frequency == "monthly":
        return {30: "mom", 365: "yoy"}.get(days)
    if frequency == "quarterly":
        return {90: "qoq", 365: "yoy"}.get(days)
    if frequency == "annual":
        return "yoy" if days == 365 else None
    return None


def _is_rate(unit):
    return unit in ("percent", "percentage_points")


def _shift_month(day, months):
    total = day.year * 12 + day.month - 1 + months
    year, month0 = divmod(total, 12)
    month = month0 + 1
    return day.replace(year=year, month=month, day=min(day.day, calendar.monthrange(year, month)[1]))


def _aligned_base(rows, latest_day, frequency, days):
    if frequency in ("daily", "weekly"):
        target = latest_day - timedelta(days=days)
        tolerance = 7 if frequency == "daily" else 14
        eligible = [row for row in rows[:-1]
                    if target - timedelta(days=tolerance) <= _day(row["date"]) <= target]
        return eligible[-1] if eligible else None, target
    months = {("monthly", 30): 1, ("monthly", 365): 12,
              ("quarterly", 90): 3, ("quarterly", 365): 12,
              ("annual", 365): 12}.get((frequency, days))
    if months is None:
        return None, latest_day - timedelta(days=days)
    target = _shift_month(latest_day, -months)
    eligible = [row for row in rows[:-1]
                if (_day(row["date"]).year, _day(row["date"]).month) == (target.year, target.month)]
    return (eligible[-1] if eligible else None), target


def compare_observations(rows, frequency, unit, days):
    """2026-09-13：依序列頻率找可比較的實際觀測期，供來源摘要共用。"""
    if not rows:
        return {"status": "insufficient_history", "comparison": None,
                "comparison_label": None, "requested_start": None,
                "actual_start": None, "actual_end": None}
    kind = _change_kind(frequency, days)
    latest = rows[-1]
    base, requested = _aligned_base(rows, _day(latest["date"]), frequency, days)
    labels = {"window": str(days) + " 日變化", "mom": "月增", "qoq": "季增", "yoy": "年增"}
    if not kind:
        base = None
    result = {"status": "ok" if base else "incompatible_frequency" if not kind else "insufficient_history",
              "comparison": kind, "comparison_label": labels.get(kind), "requested_start": requested.isoformat(),
              "actual_start": base.get("date") if base else None, "actual_end": latest["date"]}
    if not base:
        return result
    delta = latest["value"] - base["value"]
    result.update({"before": base["value"], "current": latest["value"], "delta": round(delta, 6)})
    if _is_rate(unit):
        result["change_unit"] = "pp"
        result["bp"] = round(delta * 100, 2)
    elif base["value"] != 0:
        result["change_unit"] = "return_pct"
        result["return_pct"] = round(delta / abs(base["value"]) * 100, 4)
    else:
        result["change_unit"] = "delta"
    return result


def _transform_rows(source_id, frequency, unit, rows):
    # 價格水準經濟序列優先呈現成長率，避免把水準分位解讀成通膨熱或景氣好。
    economic = source_id.startswith(("fred_cpi", "fred_core_cpi", "fred_pce", "fred_core_pce",
                                     "bls_cpi", "fred_real_gdp", "fred_industrial_production",
                                     "fred_retail_sales", "fred_payrolls"))
    if not economic or len(rows) < 2:
        return rows, "level", unit
    # 2026-09-13：缺月／缺季時仍比去年同一觀測期，不能退回第十二個舊值。
    by_month = {(_day(row["date"]).year, _day(row["date"]).month): row for row in rows}
    transformed = []
    for row in rows:
        when = _day(row["date"])
        previous = by_month.get((when.year - 1, when.month))
        if previous and previous["value"]:
            transformed.append({"date": row["date"], "value": round((row["value"] / previous["value"] - 1) * 100, 6)})
    if not transformed:
        return rows, "level", unit
    return transformed, "yoy", "percent"


def _compact(rows, maximum=120):
    if len(rows) <= maximum:
        return [{"date": row["date"], "value": row["value"]} for row in rows]
    indices = [round(index * (len(rows) - 1) / (maximum - 1)) for index in range(maximum)]
    return [{"date": rows[index]["date"], "value": rows[index]["value"]} for index in indices]


def _quote_card(ref, quote, today):
    as_of = _day(quote.get("as_of"))
    if not as_of or as_of > today or not _number(quote.get("num")):
        return None
    if quote.get("status") not in (None, "ok", "stale"):
        return None
    spark = quote.get("spark") if isinstance(quote.get("spark"), list) else []
    spark = [value for value in spark if _number(value)]
    return {"ref": ref, "label": quote.get("label", ref), "value": quote.get("num"),
            "display": quote.get("val"), "unit": quote.get("unit"), "as_of": quote.get("as_of"),
            "frequency": quote.get("frequency") or "unknown",
            "chg30_pct": quote.get("chg30_pct") if _number(quote.get("chg30_pct")) else None,
            "status": quote.get("status") or "ok", "stale": quote.get("status") == "stale",
            "history": spark, "long_history": False,
            "source_url": quote.get("source_url")}


def build_history_context(state, source_dir, today):
    """建立可直接序列化的歷史與四區事實層；輸入不會被修改。"""
    today = _day(today)
    if not today:
        raise ValueError("today 必須是 ISO 日期")
    source_dir = Path(source_dir)
    quotes = ((state or {}).get("evidence") or {}).get("quotes") or {}
    latest = _load(source_dir.parent / "latest.json") or {}
    source_quotes = latest.get("quotes") or {}
    registry = _load(source_dir.parent.parent / "market_source_registry.json") or {}
    specs = {item.get("id"): item for item in registry.get("sources", []) if item.get("id")}
    files = sorted(source_dir.glob("*.json")) if source_dir.exists() else []
    series, by_id, gaps = [], {}, []
    for path in files:
        stored = _load(path)
        if not isinstance(stored, dict) or not stored.get("id"):
            gaps.append(path.name + " 無法解析")
            continue
        source_id = stored["id"]
        rows = _current_rows(stored, today)
        if not rows:
            gaps.append(source_id + " 沒有截至指定日期的觀測")
            continue
        spec = specs.get(source_id, {})
        frequency = stored.get("frequency") or spec.get("frequency") or "daily"
        unit = stored.get("unit") or spec.get("unit")
        view_rows, transform, view_unit = _transform_rows(source_id, frequency, unit, rows)
        if not view_rows:
            continue
        changes = {key: compare_observations(view_rows, frequency, view_unit, days)
                   for key, days, _label in WINDOWS}
        mode = stored.get("data_mode") or spec.get("data_mode")
        source_quote = source_quotes.get("source:" + source_id, {})
        replay_eligible = mode in ("point_in_time", "filing_versions") and any(
            row.get("vintage") or row.get("published_at") for row in stored.get("observations", []))
        item = {"id": source_id, "label": spec.get("label") or source_quotes.get("source:" + source_id, {}).get("label") or source_id,
                "region": spec.get("region"), "source_ref": "source:" + source_id,
                "source_url": stored.get("source_url") or spec.get("source_url"), "unit": view_unit,
                "original_unit": unit, "frequency": frequency, "data_mode": mode, "transform": transform,
                "latest": {"date": view_rows[-1]["date"], "value": view_rows[-1]["value"]},
                "coverage": {"first_date": view_rows[0]["date"], "last_date": view_rows[-1]["date"],
                             "observation_count": len(view_rows), "long_history": len(view_rows) >= 13},
                "status": source_quote.get("status") or "unknown",
                "stale": source_quote.get("stale") if source_quote.get("stale") is not None else source_quote.get("status") == "stale",
                "changes": changes, "chart": _compact(view_rows),
                "replay_eligible": replay_eligible}
        series.append(item)
        by_id[source_id] = item
    regions = []
    for region_id, label in REGIONS:
        observations = []
        for ref in MONITOR_REFS[region_id]:
            if ref in quotes:
                card = _quote_card(ref, quotes[ref], today)
                if card:
                    observations.append(card)
        for source_id in SOURCE_REFS[region_id]:
            item = by_id.get(source_id)
            if item:
                observations.append({"ref": item["source_ref"], "label": item["label"],
                                     "value": item["latest"]["value"], "display": None,
                                     "unit": item["unit"], "as_of": item["latest"]["date"],
                                     "frequency": item["frequency"],
                                     "chg30_pct": item["changes"]["30d"].get("return_pct"),
                                     "status": item["status"], "stale": item["stale"],
                                     "source_url": item["source_url"]})
        available_refs = {row["ref"] for row in observations}
        satisfied = [(name, bool(available_refs.intersection(refs)))
                     for name, refs in REQUIREMENTS[region_id]]
        missing = [name for name, available in satisfied if not available]
        monitor_only = [row["label"] for row in observations
                        if row["ref"].startswith("monitor:") and not row.get("long_history")]
        region_gaps = (["缺少附日期的長期歷史；以下指標僅提供最新值與近 30 筆觀測變化：" + "、".join(monitor_only)]
                       if monitor_only else [])
        if missing:
            region_gaps.append("缺少：" + "、".join(missing))
        regions.append({"id": region_id, "label": label, "observations": observations,
                        "changes": [{"ref": row["source_ref"], "changes": row["changes"]}
                                    for sid, row in by_id.items() if sid in SOURCE_REFS[region_id]],
                        "data_gaps": region_gaps,
                        "coverage": {"available": sum(available for _name, available in satisfied),
                                     "requested": len(REQUIREMENTS[region_id])}})
    transmission = []
    us10 = by_id.get("fred_treasury_10y")
    dollar = by_id.get("fred_dollar")
    if us10 and us10["changes"]["30d"]["status"] == "ok":
        direction = "上升" if us10["changes"]["30d"]["delta"] > 0 else "下降"
        transmission.append({"title": "美債殖利率如何傳到全球估值", "condition": "若美國十年期殖利率持續" + direction,
                             "mechanism": "折現率與跨境資金成本會同向改變；各股市反應仍須由當期價格確認。",
                             "evidence_refs": ["source:fred_treasury_10y"]})
    if dollar and dollar["changes"]["30d"]["status"] == "ok":
        direction = "走強" if dollar["changes"]["30d"]["delta"] > 0 else "走弱"
        transmission.append({"title": "美元如何傳到非美市場", "condition": "若廣義美元持續" + direction,
                             "mechanism": "美元融資條件與換匯壓力會改變；區域股市與本幣方向以當期卡片為準。",
                             "evidence_refs": ["source:fred_dollar"]})
    present = set(by_id)
    missing_sources = [{"id": sid, "impact": impact, "substitute_ref": substitute,
                        "substitute_limit": limit} for sid, impact, substitute, limit in MISSING if sid not in present]
    return {"schema": "market-history-context-v1", "as_of": today.isoformat(),
            "windows": [{"id": key, "days": days, "label": label} for key, days, label in WINDOWS],
            "series": series, "regions": regions, "transmission": transmission,
            "replay": {"supported": any(row["replay_eligible"] for row in series),
                       "note": "latest_revised 只代表目前修訂後的觀測史；只有 point_in_time／filing_versions 可供當時可得回放。"},
            "missing_sources": missing_sources, "data_gaps": gaps}
