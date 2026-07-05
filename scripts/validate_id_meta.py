#!/usr/bin/env python3
"""Validate <script id="id-meta"> JSON blocks in industry DD (ID) HTML files.

Mirror of validate_dd_meta.py for the industry-analyst skill output. The ID
schema is sector-focused (theme, related_tickers, TAM, CAGR, ...) rather than
ticker-focused.

Usage:
  python scripts/validate_id_meta.py            # strict: exit 1 on any issue
  python scripts/validate_id_meta.py --report   # exit 0 always
  python scripts/validate_id_meta.py FILE...    # specific files
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
ID_DIR = ROOT / "docs" / "id"

ID_META_RE = re.compile(
    r'<script\s+id="id-meta"\s+type="application/json"\s*>(.*?)</script>',
    re.DOTALL,
)
ID_VERSION_TAG_RE = re.compile(
    r'<meta\s+name="id-skill-version"\s+content="([^"]+)"', re.IGNORECASE
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Allow vN.N or vN.N.N patch versions
SKILL_VERSION_RE = re.compile(r"^v\d+\.\d+(?:\.\d+)?$")
ID_VERSION_RE = re.compile(r"^v\d+\.\d+(?:\.\d+)?$")

REQUIRED_FIELDS = {
    "theme": str,
    "skill_version": str,
    "id_version": str,
    "publish_date": str,
    "thesis_type": str,
    "ai_exposure": str,
    "oneliner": str,
    "related_tickers": list,
}

ENUM_FIELDS = {
    "thesis_type": {"structural", "event-triggered", "mixed"},
    "ai_exposure": {"🟢", "🟡", "🔴"},
    "growth_phase": {"early", "mid", "late", "declining"},
    "value_chain_position": {"upstream", "midstream", "downstream", "cross-tier"},
    "industry_structure": {"monopoly", "duopoly", "oligopoly", "fragmented"},
    # v2.5: 趨勢結構化欄位（present 才驗；v2.5+ 另加必填閘，見下方）
    "sd_verdict": {"shortage", "balanced", "surplus", "split"},
    "clock_phase": {"I", "II", "III", "IV"},
    "conviction": {"high", "mid", "low"},
    # v1.9: quality_tier — determines which retrofit mechanisms apply
    # Q0 Flagship: full FET + thesis-trace + redteam (≥30 verified T1)
    # Q1 Standard: FET required, thesis-trace warning, redteam light (≥10 T1)
    # Q2 Quick:    FET warning only, no thesis-trace, no redteam (≥5 T1)
    "quality_tier": {"Q0", "Q1", "Q2"},
}

# v1.8 taxonomy — mega 大類別 × sub_group 子群組（白名單）
# Source of truth: docs/id/taxonomy.md
TAXONOMY = {
    "semi": {"compute_demand", "memory", "storage", "networking", "dc_infra",
             "advanced_packaging", "foundry_process", "equipment_test", "eda_ip",
             "edge_ai", "emerging_compute"},
    "bio": {"glp1", "gene_cell", "medical_device", "cdmo_cro", "digital_health",
            "hospital_chain", "china_pharma"},
    "cloud": {"cybersecurity", "agentic_ai", "ai_cross_domain", "media_publishing",
              "vertical_saas", "devops_data", "communication"},
    "energy": {"nuclear", "solar", "wind", "hydrogen", "ev_oem", "battery_metals",
               "oil_gas", "utilities"},
    "consumer": {"apparel", "luxury", "restaurant", "discount_retail", "ecommerce",
                 "fitness_personal", "home_furniture"},
    "finance": {"payment_network", "banks", "stablecoin", "wealth_mgmt",
                "insurance", "asset_mgmt_pe", "fintech_lending"},
    "industrial": {"defense", "commercial_aero", "robotics", "heavy_machinery",
                   "autonomous_driving", "hvac_electrical", "engineering_construction"},
    "staples": {"beverage", "packaged_food", "restaurant_glp1", "alcohol_tobacco",
                "personal_care_beauty", "household_products"},
    "reits": {"data_center", "industrial_logistics", "retail_mall",
              "healthcare_senior", "cell_tower"},
    "space": {"launch", "satellite_comm", "space_materials", "defense_space"},
    "housing": {"us_builders", "intl_property", "mortgage_mbs", "land_development"},
    "transport": {"travel_master", "hotel_lodging", "cruise_luxury_travel",
                  "ota_distribution", "airline", "casino_gaming", "shipping_freight"},
    "materials": {"industrial_metals", "aerospace_defense_metals", "battery_metals",
                  "steel", "precious_metals", "specialty_chemicals",
                  "cement_construction", "rare_earth"},
    "agri": {"livestock_meat", "grains_oilseeds", "fishery_aqua",
             "fertilizer_seeds", "farm_equipment"},
    "macro": {"geopolitics_cntw", "geopolitics_other", "demographics", "thematic_other"},
}

NUMERIC_RANGES = {
    "tam_usd_2030": (0, 10_000),
    "cagr_pct_5y": (-50, 200),
    # v2.4: 5Y demand multiple = base-case 5Y TAM ÷ current TAM (§4 → §0 TL;DR).
    # Optional at validator level (legacy exempt); required by skill flow for v2.4+.
    "demand_5y_multiple": (0, 50),
}

ONELINER_HARD_CAP = 200
TICKER_DEPTH_ALLOWED = {"🔴", "🟡", "🟢"}
# v2.4 related_tickers optional keys — validated only when present (legacy exempt).
TICKER_MCAP_BUCKETS = {"mega", "large", "mid", "small"}

# v2.2 §0「三句話看完」— 現在 / 未來 / 怎麼做，同步寫進 id-meta。
# v2.x ID 必填（validator 阻斷）；legacy v1.x 不受影響（startswith v2. 才觸發）。
# 每句「一句結論 + 一個證據子句」，硬上限比 oneliner 略寬以容納證據錨點。
THREE_SENTENCE_FIELDS = ("now_state", "future_state", "action")
THREE_SENTENCE_HARD_CAP = 240
V2_RE = re.compile(r"^v2\.")

# v2.5 趨勢結構化欄位 — 供需裁決 / 投資時鐘 / conviction / 證偽表機器化。
# 邏輯：present 時驗型 / 驗 enum（sd_verdict / clock_phase / conviction 已進 ENUM_FIELDS）；
#       skill_version ≥ v2.5 時新欄位（含 v2.4 三欄）升為「必填阻斷」；v2.0–v2.4 present 才驗、
#       absent 放行；v1.x legacy 全豁免（與 now_state 三欄的 V2_RE 模式同構，但門檻是 v2.5+）。
V2_5_MIN = (2, 5)
SD_VERDICT_DETAIL_CAP = 160
KILL_METRICS_MIN = 3
KILL_METRIC_STATUS = {"ok", "warning", "triggered", "unknown"}
# kill_metrics[] 每項欄位長度上限（source / last_status 選填）
KILL_FIELD_CAPS = {"metric": 120, "bear_threshold": 120, "window": 60, "source": 120}
VERSION_TUPLE_RE = re.compile(r"^v(\d+)\.(\d+)")


def _version_tuple(v):
    """Parse skill_version 'vN.N[.N]' → (major, minor); None if malformed."""
    m = VERSION_TUPLE_RE.match(str(v))
    return (int(m.group(1)), int(m.group(2))) if m else None


def validate_meta(meta: dict) -> list:
    errs = []
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in meta:
            errs.append(f"missing required field: {field}")
            continue
        v = meta[field]
        if v is None:
            errs.append(f"{field}: must not be null")
            continue
        if not isinstance(v, expected_type):
            errs.append(
                f"{field}: expected {expected_type.__name__}, got {type(v).__name__}"
            )

    for field, allowed in ENUM_FIELDS.items():
        v = meta.get(field)
        if v is not None and v not in allowed:
            errs.append(
                f"{field}: invalid value {v!r}; allowed {sorted(allowed)}"
            )

    if "publish_date" in meta and not DATE_RE.match(str(meta["publish_date"])):
        errs.append(f"publish_date: must be YYYY-MM-DD, got {meta['publish_date']!r}")
    if "skill_version" in meta and not SKILL_VERSION_RE.match(str(meta["skill_version"])):
        errs.append(f"skill_version: must match vN.N, got {meta['skill_version']!r}")
    if "id_version" in meta and not ID_VERSION_RE.match(str(meta["id_version"])):
        errs.append(f"id_version: must match vN.N, got {meta['id_version']!r}")

    for field, (lo, hi) in NUMERIC_RANGES.items():
        v = meta.get(field)
        if isinstance(v, (int, float)) and not (lo <= v <= hi):
            errs.append(f"{field}: {v} out of range [{lo}, {hi}]")

    one = meta.get("oneliner")
    if isinstance(one, str) and len(one) > ONELINER_HARD_CAP:
        errs.append(f"oneliner: {len(one)} chars exceeds hard cap {ONELINER_HARD_CAP}")

    # v2.2 §0 三句話（now_state / future_state / action）— v2.x 必填 + 長度上限。
    is_v2 = bool(V2_RE.match(str(meta.get("skill_version", ""))))
    ver = _version_tuple(meta.get("skill_version", ""))
    is_v25_plus = ver is not None and ver >= V2_5_MIN
    for field in THREE_SENTENCE_FIELDS:
        v = meta.get(field)
        if is_v2 and not (isinstance(v, str) and v.strip()):
            errs.append(f"{field}: required (non-empty) for skill_version v2.x (§0 三句話看完)")
        if isinstance(v, str) and len(v) > THREE_SENTENCE_HARD_CAP:
            errs.append(f"{field}: {len(v)} chars exceeds hard cap {THREE_SENTENCE_HARD_CAP}")

    # v2.5 趨勢結構化欄位（sd_verdict / clock_phase / conviction / kill_metrics + v2.4 三欄升必填）。
    # enum 驗證由 ENUM_FIELDS 迴圈負責；此處補「v2.5+ 必填」+ sd_verdict_detail + kill_metrics 結構。
    if is_v25_plus:
        for field in ("sd_verdict", "clock_phase", "conviction"):
            v = meta.get(field)
            if not (isinstance(v, str) and v.strip()):
                errs.append(f"{field}: required (non-empty) for skill_version >= v2.5 (趨勢結構化欄位)")
        dm = meta.get("demand_5y_multiple")
        if not (isinstance(dm, (int, float)) and not isinstance(dm, bool)):
            errs.append("demand_5y_multiple: required (number) for skill_version >= v2.5")

    # sd_verdict_detail — split 時必填、任何時候有值都驗型/長度。
    detail = meta.get("sd_verdict_detail")
    if detail is not None:
        if not isinstance(detail, str):
            errs.append(f"sd_verdict_detail: expected str, got {type(detail).__name__}")
        elif len(detail) > SD_VERDICT_DETAIL_CAP:
            errs.append(f"sd_verdict_detail: {len(detail)} chars exceeds hard cap {SD_VERDICT_DETAIL_CAP}")
    if meta.get("sd_verdict") == "split" and not (isinstance(detail, str) and detail.strip()):
        errs.append("sd_verdict_detail: required (non-empty) when sd_verdict == 'split'")

    # kill_metrics[] — present 才驗結構；v2.5+ 必填且 ≥3 items（對齊 §8 證偽表 3-5 條）。
    km = meta.get("kill_metrics")
    if km is None:
        if is_v25_plus:
            errs.append(
                f"kill_metrics: required (array of ≥{KILL_METRICS_MIN}) for skill_version >= v2.5"
            )
    elif not isinstance(km, list):
        errs.append(f"kill_metrics: expected array, got {type(km).__name__}")
    else:
        if is_v25_plus and len(km) < KILL_METRICS_MIN:
            errs.append(
                f"kill_metrics: requires ≥{KILL_METRICS_MIN} items for skill_version >= v2.5, got {len(km)}"
            )
        for i, k in enumerate(km):
            if not isinstance(k, dict):
                errs.append(f"kill_metrics[{i}]: must be object, got {type(k).__name__}")
                continue
            for key in ("metric", "bear_threshold", "window"):
                if key not in k:
                    errs.append(f"kill_metrics[{i}].{key}: required key missing")
            for key, cap in KILL_FIELD_CAPS.items():
                if key in k:
                    vv = k[key]
                    if not isinstance(vv, str):
                        errs.append(f"kill_metrics[{i}].{key}: expected str, got {type(vv).__name__}")
                    elif len(vv) > cap:
                        errs.append(f"kill_metrics[{i}].{key}: {len(vv)} chars exceeds cap {cap}")
            if "last_status" in k and k["last_status"] not in KILL_METRIC_STATUS:
                errs.append(
                    f"kill_metrics[{i}].last_status: invalid {k['last_status']!r}, "
                    f"allowed {sorted(KILL_METRIC_STATUS)}"
                )

    # related_tickers entries
    rt = meta.get("related_tickers")
    if isinstance(rt, list):
        if len(rt) == 0:
            errs.append("related_tickers: must contain ≥ 1 entry (use empty array only for cross-cutting themes)")
        for i, t in enumerate(rt):
            if not isinstance(t, dict):
                errs.append(f"related_tickers[{i}]: must be object, got {type(t).__name__}")
                continue
            for key in ("ticker", "role", "depth", "beneficiary"):
                if key not in t:
                    errs.append(f"related_tickers[{i}].{key}: required key missing")
            if "depth" in t and t["depth"] not in TICKER_DEPTH_ALLOWED:
                errs.append(
                    f"related_tickers[{i}].depth: invalid {t['depth']!r}, "
                    f"allowed {sorted(TICKER_DEPTH_ALLOWED)}"
                )
            if "beneficiary" in t and not isinstance(t["beneficiary"], bool):
                errs.append(
                    f"related_tickers[{i}].beneficiary: must be bool, "
                    f"got {type(t['beneficiary']).__name__}"
                )
            # v2.4 optional keys: purity_pct (0-100 number) / mcap_bucket (enum)
            if "purity_pct" in t:
                pv = t["purity_pct"]
                if not isinstance(pv, (int, float)) or isinstance(pv, bool) or not (0 <= pv <= 100):
                    errs.append(
                        f"related_tickers[{i}].purity_pct: must be number in [0, 100], got {pv!r}"
                    )
            if "mcap_bucket" in t and t["mcap_bucket"] not in TICKER_MCAP_BUCKETS:
                errs.append(
                    f"related_tickers[{i}].mcap_bucket: invalid {t['mcap_bucket']!r}, "
                    f"allowed {sorted(TICKER_MCAP_BUCKETS)}"
                )
            # v2.5+: depth=🔴 的 pure-play 必附 purity_pct + mcap_bucket（多倍候選機器初篩）；
            # 🟡🟢 邊緣股選填（全項強制會對邊緣股過苛）。
            if is_v25_plus and t.get("depth") == "🔴":
                for key in ("purity_pct", "mcap_bucket"):
                    if key not in t:
                        errs.append(
                            f"related_tickers[{i}].{key}: required for depth=🔴 when skill_version >= v2.5"
                        )

    # sections_refreshed structure (optional)
    sr = meta.get("sections_refreshed")
    if isinstance(sr, dict):
        for k in sr:
            if k not in ("technical", "market", "judgment"):
                errs.append(f"sections_refreshed: unknown key {k!r}")
            if not DATE_RE.match(str(sr[k])):
                errs.append(f"sections_refreshed.{k}: must be YYYY-MM-DD")

    # v1.8 mega + sub_group taxonomy validation (QC-I37)
    # If either is present it must be valid; if both missing it's a soft warning
    # (existing IDs pre-v1.8 have neither — only block when one is malformed).
    mega = meta.get("mega")
    sub_group = meta.get("sub_group")
    if mega is not None or sub_group is not None:
        if not isinstance(mega, str) or mega not in TAXONOMY:
            errs.append(
                f"mega: invalid value {mega!r}; must be one of {sorted(TAXONOMY.keys())}"
            )
        elif not isinstance(sub_group, str) or sub_group not in TAXONOMY[mega]:
            errs.append(
                f"sub_group: invalid value {sub_group!r} for mega={mega!r}; "
                f"must be one of {sorted(TAXONOMY[mega])}"
            )

    return errs


def validate_file(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return {"status": "read_error", "errors": [str(e)]}

    has_skill_meta = bool(ID_VERSION_TAG_RE.search(text))
    if not has_skill_meta:
        return {"status": "non_id"}  # not an industry-analyst output

    # Skip non-industry-analyst outputs that share the ID_*.html naming.
    # Currently: geopolitics-dd skill uses skill_version like "geopolitics-v1.0"
    # (or with stray "v" prefix from older backfills).
    skill_meta = ID_VERSION_TAG_RE.search(text).group(1)
    if "geopolitics" in skill_meta:
        return {"status": "non_id"}

    meta_m = ID_META_RE.search(text)
    if not meta_m:
        return {
            "status": "missing_block",
            "errors": ['no <script id="id-meta"> found in <head>'],
        }

    raw = meta_m.group(1).strip()
    try:
        meta = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"status": "parse_error", "errors": [f"JSON parse error: {e}"]}

    errs = validate_meta(meta)
    if errs:
        return {"status": "invalid", "errors": errs, "theme": meta.get("theme")}
    return {"status": "ok", "theme": meta.get("theme")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--json", dest="json_out", action="store_true")
    args = parser.parse_args()

    targets = [Path(p) for p in args.files] if args.files else sorted(ID_DIR.glob("ID_*.html"))

    results = [{"file": p.name, **validate_file(p)} for p in targets]

    if args.json_out:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        bad = any(r["status"] not in ("ok", "non_id") for r in results)
        sys.exit(0 if (args.report or not bad) else 1)

    counts = {"ok": 0, "non_id": 0, "missing_block": 0, "parse_error": 0, "invalid": 0}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    print(f"Scanned {len(results)} ID file(s):")
    print(f"  ✅ ok                : {counts['ok']}")
    print(f"  ⚠  missing id-meta  : {counts.get('missing_block', 0)}")
    print(f"  ❌ JSON parse error : {counts.get('parse_error', 0)}")
    print(f"  ❌ validation error : {counts.get('invalid', 0)}")
    print(f"  ↪  non-ID (skipped) : {counts.get('non_id', 0)}")

    bad = [r for r in results if r["status"] in ("missing_block", "parse_error", "invalid")]
    if bad:
        print()
        for r in bad:
            theme = r.get("theme", "?")
            print(f"\n[{r['status'].upper()}] {r['file']} (theme={theme})")
            for e in r.get("errors", []):
                print(f"    - {e}")

    if bad and not args.report:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
