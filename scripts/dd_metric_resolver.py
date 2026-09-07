#!/usr/bin/env python3
"""DD judgment 與 scenario_meta 的共用機械欄位解析器。"""
from __future__ import annotations

import sys
from typing import Dict, Optional


# 2026-09-07：沿用既有 brief／gen_dd_tables 容差；容差只控制歷史存查的
# 漂移警告，不再讓 judgment 蓋過 scenario 的權威重算值。
SCENARIO_METRIC_TOLERANCES = {
    "irr_base_pct": 0.5,
    "ev5y_pct": 1.0,
    "asym_ratio": 0.06,
}
SCENARIO_METRIC_FIELDS = ("ev5y_pct", "irr_base_pct", "asym_ratio")


def resolve_scenario_metrics(
    judgment: dict,
    scenario_meta: Optional[dict],
    source: str = "dd",
) -> Dict[str, object]:
    """解析 EV／IRR／AR；scenario 有值時一律是發布權威值。

    新版 judgment 依設計填 null；歷史 judgment 若仍有值，沿用既有容差判斷
    是否印漂移警告，但不再用近似的判斷值取代 scenario 重算值。
    """
    decision_inputs = (judgment or {}).get("decision_inputs") or {}
    scenario = scenario_meta or {}
    resolved = {}
    ticker = ((judgment or {}).get("meta") or {}).get("ticker") or "—"
    for field in SCENARIO_METRIC_FIELDS:
        judgment_value = decision_inputs.get(field)
        scenario_value = scenario.get(field)
        if scenario_value is None:
            resolved[field] = judgment_value
            continue
        if judgment_value is not None:
            try:
                difference = abs(float(scenario_value) - float(judgment_value))
            except (TypeError, ValueError):
                difference = None
            tolerance = SCENARIO_METRIC_TOLERANCES[field]
            if difference is not None and difference > tolerance:
                print(
                    "[warn] {0}: {1} {2} 判斷值 {3} 與機械重算 {4} 相差 {5:.2f}"
                    "（>{6} 門檻）——改採機械重算值".format(
                        source, ticker, field, judgment_value, scenario_value,
                        difference, tolerance,
                    ),
                    file=sys.stderr,
                )
        resolved[field] = scenario_value
    return resolved


def resolve_max_dd_pct(judgment: dict):
    """2026-09-07：依既有發布契約由 premortem.max_dd 解析 Max DD。"""
    max_dd = (((judgment or {}).get("premortem") or {}).get("max_dd") or {})
    lo, hi = max_dd.get("lo"), max_dd.get("hi")
    if lo is not None and hi is not None:
        return min(lo, hi)
    if lo is not None:
        return lo
    return None
