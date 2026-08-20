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
THEMES_YML = INTEL_DIR / "themes.yml"  # Phase 2（2026-08-20）：固定主題註冊表
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

_ONSITE_SHORTS = {
    "onsite_monitor": "站內監測",
    "onsite_regime": "站內regime",
    "onsite_rotation": "站內輪動",
    "onsite_crowding": "站內擁擠",
    "onsite_detective": "站內偵探",
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


def load_source_short_map() -> dict:
    """source_id -> ≤8 字短名（用於 brief_zh 的 <a> 連結文字／finalize_card 的
    source_short），來源 sources.yml 的 `short:` 欄位 ＋ onsite 特判。缺
    `short:` 的來源 fall back 到 name 前 8 字（source_name_for/source_short_for
    再兜底一次），不因漏填整條 pipeline 掛掉。"""
    shorts = dict(_ONSITE_SHORTS)
    try:
        with open(SOURCES_YML, "r", encoding="utf-8") as f:
            sources = yaml.safe_load(f) or []
        for s in sources:
            if s.get("id") and s.get("short"):
                shorts[s["id"]] = s["short"]
    except (OSError, yaml.YAMLError):
        pass
    return shorts


def source_name_for(card: dict, name_map: dict) -> str:
    if card.get("source_name_override"):
        return card["source_name_override"]
    sid = card.get("source_id", "")
    if sid in name_map:
        return name_map[sid]
    if sid.startswith("fred_"):
        series = (card.get("data") or {}).get("series", sid.replace("fred_", "").upper())
        return f"FRED {series}"
    return card.get("source_id") or "未知來源"


def source_short_for(card: dict, short_map: dict, name_map: dict | None = None) -> str:
    """≤8 字短名。gnews 卡片逐則帶 `source_short_override`（發布方名稱依卡片
    而異，不能用 source_id 查表）；其餘來源查 sources.yml `short:`，缺表就用
    全名/來源名前 8 字兜底。"""
    if card.get("source_short_override"):
        return card["source_short_override"][:14]
    sid = card.get("source_id", "")
    if sid in short_map:
        return short_map[sid][:14]
    return source_name_for(card, name_map or {})[:10] or (card.get("source_id") or "")[:10]


def pending_path(date: str) -> Path:
    return PENDING_DIR / f"{date}.json"


def daily_output_path(date: str) -> Path:
    return DATA_DIR / f"{date}.json"


def read_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


_THEMES_CACHE: list | None = None


def load_themes() -> list:
    """Phase 2（2026-08-20）：讀 scripts/intel/themes.yml 的固定主題清單
    （見該檔案頭註解）。fail-safe——缺檔／壞 YAML 回 []，呼叫端（classify.py
    的 prompt 組裝、theme_weekly.py 的每主題掃描）都要能接受空清單而不掛掉。
    Process 內快取一次（themes.yml 在同一次執行中不會變動）。"""
    global _THEMES_CACHE
    if _THEMES_CACHE is not None:
        return _THEMES_CACHE
    try:
        with open(THEMES_YML, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
        _THEMES_CACHE = [t for t in data if isinstance(t, dict) and t.get("key")]
    except (OSError, yaml.YAMLError):
        _THEMES_CACHE = []
    return _THEMES_CACHE


def theme_keys() -> list:
    return [t["key"] for t in load_themes()]
