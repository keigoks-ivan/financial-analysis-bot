#!/usr/bin/env python3
"""scripts/intel/common.py — shared constants/paths/helpers for the intel
Phase 1 pipeline (classify.py / summarize.py / run_daily.py). Kept tiny and
dependency-light (yaml only, already required by fetch.py) so each stage can
import just what it needs.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
INTEL_DIR = ROOT / "scripts" / "intel"
SOURCES_YML = INTEL_DIR / "sources.yml"
DATA_DIR = ROOT / "docs" / "intel" / "data"
PENDING_DIR = ROOT / "docs" / "intel" / "pending"
PROMPTS_DIR = INTEL_DIR / "prompts"

# DESIGN.md §3 market-layer 13 dimensions, in the order the page renders them.
CATEGORY_ORDER = [
    "rates", "credit", "liquidity", "fx", "commodities", "vol",
    "breadth", "positioning", "econ", "cb", "geo", "regime", "asia",
]
CATEGORY_LABELS_ZH = {
    "rates": "利率", "credit": "信用", "liquidity": "流動性", "fx": "匯率",
    "commodities": "商品", "vol": "波動與壓力", "breadth": "股市內部",
    "positioning": "部位與情緒", "econ": "經濟數據", "cb": "央行與財政政策",
    "geo": "地緣", "regime": "跨市場 regime", "asia": "亞洲",
}

TIER_RANK = {"T1": 0, "T2": 1, "T3": 2, "T4": 3}

# Onsite/derived source ids that don't come from sources.yml (see fetch.py
# build_onsite_cards / fetch_fred_source) — human-readable names for the
# card schema's `source_name`.
_ONSITE_NAMES = {
    "onsite_monitor": "站內市場監測",
    "onsite_regime": "站內跨市場 regime",
    "onsite_rotation": "站內輪動雷達",
    "onsite_crowding": "站內擁擠交易監測",
    "onsite_detective": "站內 kill-watch",
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None = None) -> str:
    dt = dt or now_utc()
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path):
    path = Path(path)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def load_source_name_map() -> dict:
    """source_id -> 人類可讀名稱，來源 sources.yml ＋ onsite/FRED 特判。"""
    names = dict(_ONSITE_NAMES)
    try:
        with open(SOURCES_YML, "r", encoding="utf-8") as f:
            sources = yaml.safe_load(f) or []
        for s in sources:
            if s.get("id"):
                names[s["id"]] = s.get("name", s["id"])
    except (OSError, yaml.YAMLError):
        pass
    return names


def source_name_for(card: dict, name_map: dict) -> str:
    sid = card.get("source_id", "")
    if sid in name_map:
        return name_map[sid]
    if sid.startswith("fred_"):
        series = (card.get("data") or {}).get("series", sid.replace("fred_", "").upper())
        return f"FRED {series}"
    return card.get("source_id") or "未知來源"


def pending_path(date: str) -> Path:
    return PENDING_DIR / f"{date}.json"


def daily_output_path(date: str) -> Path:
    return DATA_DIR / f"{date}.json"


def read_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")
