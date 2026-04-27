"""Tier Matrix gap checker — run after industry-analyst / stock-analyst.

Purpose:
  1. Scan all docs/id/ID_*.html for tickers in §11 玩家矩陣 / §6 玩家清單
  2. Scan docs/id/tier_matrix.html for currently classified tickers (Tier 1-4)
  3. Scan docs/dd/ for recent DD signal changes (via dd-meta JSON)
  4. Output gap report:
     - 🆕 New tickers in IDs but not in Tier Matrix (need Tier classification)
     - 🔄 DD signal changes affecting tickers already in Matrix (need Tier review)
     - 🗑 Tickers in Matrix but no longer in any ID (potential cleanup)
     - ⏰ Tier Matrix half-life warning (60 days from last refresh)

Usage:
  python3 scripts/check_tier_matrix.py
  python3 scripts/check_tier_matrix.py --json     # machine-readable output
  python3 scripts/check_tier_matrix.py --quiet    # only show actions needed

Exit codes:
  0 = no action needed (all in sync)
  1 = action needed (gaps found, message printed)
  2 = error (file missing, parse failure)

Stdlib-only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
ID_DIR = REPO_ROOT / "docs" / "id"
DD_DIR = REPO_ROOT / "docs" / "dd"
TIER_MATRIX = ID_DIR / "tier_matrix.html"

# ---------------------------------------------------------------------------
# Ticker extraction patterns
# ---------------------------------------------------------------------------

# Matches US tickers in <strong>TICKER</strong> tags (uppercase 1-5 letters)
RE_US_TICKER = re.compile(r"<strong>([A-Z]{1,5})</strong>")

# Matches Taiwan tickers like 2330.TW, 6857.T, etc.
RE_TW_TICKER = re.compile(r"\b(\d{4})\.(?:TW|T|TWO|HK|MC|PA|DE|KS|SS|SW|L)\b")

# Tickers we recognize even without explicit <strong> tags (for §6 narratives)
# This is a curated whitelist of tickers from existing IDs; extend as needed.
KNOWN_TICKERS = {
    # Silicon
    "NVDA", "AVGO", "AMD", "INTC", "ASML", "AMAT", "LRCX", "KLAC",
    "TER", "FORM", "COHU", "TPRO", "AEM", "AEHR", "CAMT",
    "ADEA", "BESI", "ASMPT",
    # Memory
    "MU", "SNDK", "WDC", "PSTG", "NTAP",
    # Hyperscaler / Big Tech
    "MSFT", "GOOGL", "AMZN", "META", "AAPL", "ORCL",
    # Networking
    "ANET", "CRDO", "MRVL", "COHR", "LITE", "FN", "APH",
    # Edge / cloud
    "NET", "CRWV", "DDOG", "MDB", "SNOW",
    # Cybersec
    "CRWD", "PANW", "ZS", "FTNT", "OKTA", "S", "SAIL", "RBRK", "VRNS",
    "CHKP", "CSCO", "FFIV", "PYPL",
    # AI agentic / SaaS
    "CRM", "NOW", "WDAY", "INTU", "DOCU", "BOX", "TEAM", "ZM",
    "HUBS", "ADBE", "PLTR", "PATH", "TWLO",
    # Power / industrial
    "ETN", "VRT", "GEV", "ROK", "EMR", "PWR", "ABB",
    "SU", "HON", "JCI",
    # Defense / aerospace
    "LMT", "RTX", "NOC", "GD", "BA", "AVAV", "SAIC", "HWM", "TDG", "HEI", "ATI",
    # Heavy machinery
    "CAT", "DE", "CMI", "AGCO",
    # EV
    "TSLA",
    # Edge / device
    "QCOM", "ARM", "SYNA", "NXP", "AMBA",
    # Cruise / travel
    "RCL", "CCL", "NCLH", "VIK", "BKNG", "ABNB", "TRIP", "EXPE",
    # Luxury / consumer
    "TPR", "CPRI",
    # Foundry geo
}

# Non-tickers that match the regex but should be excluded
EXCLUDE_TOKENS = {
    "AI", "API", "ARR", "ASIC", "ASP", "ATE", "BB", "BG", "BLS", "BPS", "CAGR",
    "CAPEX", "CCS", "CDS", "CEO", "CFO", "COO", "CHF", "CMD", "CMOS", "CMS",
    "CPI", "CPU", "CRM", "CSO", "CSU", "CTO", "DC", "DDR", "DDR5", "DSO",
    "EBIT", "EBITDA", "ECC", "EDA", "EM", "EMEA", "ENA", "EOS", "EPS", "ETF",
    "EU", "EUR", "EUV", "FY", "FCF", "FED", "FY25", "FY26", "FY27", "FY28",
    "GAAP", "GBP", "GCP", "GDP", "GE", "GIPL", "GLP", "GM", "GMV", "GN",
    "GPU", "HBM", "HBM4", "HBM5", "HFI", "HKS", "HPC", "HPS", "HQ", "HR",
    "I", "IAM", "ID", "IDM", "IDR", "IEEE", "IO", "IP", "IPO", "IRA", "IRR",
    "ISO", "IT", "JPY", "JV", "KPI", "L1", "L2", "LCD", "LCM", "LIDE",
    "LIFO", "LLM", "LP", "LPDDR", "LPT", "LSE", "M", "MA", "MAU", "MBA",
    "MCU", "MFG", "MFU", "MIT", "MOM", "MRP", "MTM", "MWh", "NAND", "NATO",
    "NDA", "NDR", "NLR", "NPS", "NPU", "NRR", "NX", "NYSE", "OAM", "OAT",
    "OECD", "OEM", "OS", "OSAT", "OTA", "P", "PAM", "PC", "PE", "PEG", "PHY",
    "PMI", "PR", "PS", "Q", "Q1", "Q2", "Q3", "Q4", "QC", "QE", "QSL", "RD",
    "RG", "RMB", "ROCm", "ROE", "ROI", "ROIC", "RPK", "RSU", "S1", "S5",
    "SAM", "SAT", "SDC", "SDK", "SDLC", "SEC", "SEM", "SLT", "SMB", "SOC",
    "SOM", "SOR", "SOX", "SPAC", "SQ", "SSC", "SSD", "T", "T1", "T2", "T3",
    "T4", "TAM", "TBR", "TCO", "TFP", "TI", "TIN", "TLB", "TPS", "TSV",
    "TWh", "U", "UI", "UK", "ULA", "UPS", "US", "USD", "UX", "VC", "VFX",
    "VR", "WACC", "WFE", "X", "Y", "YOY", "YR", "Z", "ZB",
    # Common false matches
    "TSMC",  # we match TSMC explicitly elsewhere
}


def extract_tickers_from_html(path: Path) -> set[str]:
    """Extract unique tickers from a single HTML file."""
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()

    tickers: set[str] = set()

    # 1. Pure US tickers in <strong>TICKER</strong>
    for match in RE_US_TICKER.finditer(content):
        tk = match.group(1)
        if tk in EXCLUDE_TOKENS:
            continue
        if tk in KNOWN_TICKERS:
            tickers.add(tk)
        elif len(tk) >= 3:
            # Heuristic: 3-5 letter all-caps in <strong> usually a ticker
            tickers.add(tk)

    # 2. International tickers (TSMC 2330, AENA.MC, etc.)
    for match in RE_TW_TICKER.finditer(content):
        tickers.add(match.group(0))

    # 3. Special: TSMC and named tickers
    if "TSMC" in content or "2330.TW" in content:
        tickers.add("TSMC（2330.TW）")
    if "Hermès" in content or "RMS.PA" in content:
        tickers.add("RMS（Hermès）")
    if "Richemont" in content or "CFR.SW" in content:
        tickers.add("CFR（Richemont）")
    if "AENA" in content:
        tickers.add("AENA.MC")
    if "Viking" in content and "VIK" in content:
        tickers.add("VIK")

    return tickers


# ---------------------------------------------------------------------------
# Tier Matrix parsing
# ---------------------------------------------------------------------------

def extract_tier_matrix_tickers() -> dict[str, str]:
    """Return {ticker: tier_name} from current tier_matrix.html."""
    if not TIER_MATRIX.exists():
        return {}

    content = TIER_MATRIX.read_text(encoding="utf-8")

    # Find Tier sections by class names
    result: dict[str, str] = {}
    tier_pattern = re.compile(
        r'<div class="tier-head tier(\d+)">.*?</table>',
        re.DOTALL,
    )

    for m in tier_pattern.finditer(content):
        tier_num = m.group(1)
        section = m.group(0)
        for tk_match in RE_US_TICKER.finditer(section):
            tk = tk_match.group(1)
            if tk in EXCLUDE_TOKENS:
                continue
            result[tk] = f"Tier {tier_num}"
        # Special tickers
        if "TSMC" in section or "2330.TW" in section:
            result["TSMC（2330.TW）"] = f"Tier {tier_num}"
        if "RMS（Hermès" in section:
            result["RMS（Hermès）"] = f"Tier {tier_num}"
        if "CFR（Richemont" in section:
            result["CFR（Richemont）"] = f"Tier {tier_num}"
        if "AENA" in section:
            result["AENA.MC"] = f"Tier {tier_num}"

    return result


def get_tier_matrix_publish_date() -> date | None:
    """Read publish date from tier_matrix.html meta tag."""
    if not TIER_MATRIX.exists():
        return None
    content = TIER_MATRIX.read_text(encoding="utf-8")
    m = re.search(r'page-publish-date" content="(\d{4}-\d{2}-\d{2})"', content)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# DD signal change detection
# ---------------------------------------------------------------------------

def get_recent_dd_signals(days: int = 7) -> dict[str, dict]:
    """Read recent DD files and return their signals.

    Returns: {ticker: {date, signal, verdict}}
    """
    if not DD_DIR.exists():
        return {}

    cutoff = (datetime.now() - timedelta(days=days)).date()
    result: dict[str, dict] = {}

    for dd_file in DD_DIR.glob("DD_*_*.html"):
        # Parse filename for ticker and date
        m = re.match(r"DD_([A-Z0-9]+)_(\d{8})\.html", dd_file.name)
        if not m:
            continue
        ticker, date_str = m.group(1), m.group(2)
        try:
            dd_date = datetime.strptime(date_str, "%Y%m%d").date()
        except ValueError:
            continue
        if dd_date < cutoff:
            continue

        # Try to read dd-meta JSON
        try:
            content = dd_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        meta_match = re.search(
            r'<script id="dd-meta"[^>]*>(.*?)</script>',
            content,
            re.DOTALL,
        )
        if not meta_match:
            continue

        try:
            meta = json.loads(meta_match.group(1))
        except json.JSONDecodeError:
            continue

        # Keep most recent per ticker
        existing = result.get(ticker)
        if existing is None or dd_date > existing["date"]:
            result[ticker] = {
                "date": dd_date,
                "signal": meta.get("signal"),
                "verdict": meta.get("verdict"),
                "long_term_confidence": meta.get("long_term_confidence"),
            }

    return result


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def run_check(quiet: bool = False, json_out: bool = False, min_id_count: int = 2,
              include_geopolitics: bool = False) -> int:
    """Run the full check. Returns exit code.

    Args:
        min_id_count: Only flag tickers appearing in >= N IDs (filter narrative mentions)
        include_geopolitics: Include CNTW_* geopolitics IDs (default: exclude)
    """

    # 1. Collect all tickers from IDs (excluding tier_matrix itself)
    id_tickers: dict[str, list[str]] = {}  # ticker -> list of ID files
    if not ID_DIR.exists():
        if not quiet:
            print(f"❌ ID directory not found: {ID_DIR}")
        return 2

    for id_file in ID_DIR.glob("ID_*.html"):
        # Skip geopolitics scenario IDs (not investment plays)
        if not include_geopolitics and id_file.name.startswith("ID_CNTW_"):
            continue
        tickers = extract_tickers_from_html(id_file)
        for tk in tickers:
            id_tickers.setdefault(tk, []).append(id_file.name)

    # 2. Get current Tier Matrix tickers
    matrix_tickers = extract_tier_matrix_tickers()

    # 3. Get recent DD signals
    dd_signals = get_recent_dd_signals(days=7)

    # 4. Compute gaps
    new_in_id = sorted(set(id_tickers.keys()) - set(matrix_tickers.keys()))
    only_in_matrix = sorted(set(matrix_tickers.keys()) - set(id_tickers.keys()))

    # Filter new_in_id to known tickers only (avoid false positives)
    new_in_id_filtered = [
        tk for tk in new_in_id
        if tk in KNOWN_TICKERS or "（" in tk or "." in tk
    ]

    # 5. Half-life check
    publish_date = get_tier_matrix_publish_date()
    days_since_publish = (
        (date.today() - publish_date).days if publish_date else None
    )
    half_life_warning = (
        days_since_publish is not None and days_since_publish > 53
    )

    # 6. DD signal changes for tickers in matrix
    dd_changes_for_matrix = {
        tk: signal
        for tk, signal in dd_signals.items()
        if tk in matrix_tickers
    }

    # 7. Output
    if json_out:
        report = {
            "publish_date": str(publish_date) if publish_date else None,
            "days_since_publish": days_since_publish,
            "half_life_warning": half_life_warning,
            "matrix_total": len(matrix_tickers),
            "new_in_id": new_in_id_filtered,
            "new_in_id_with_sources": {
                tk: id_tickers[tk] for tk in new_in_id_filtered
            },
            "only_in_matrix": only_in_matrix,
            "recent_dd_changes": {
                tk: {**v, "current_tier": matrix_tickers.get(tk, "—")}
                for tk, v in dd_signals.items()
            },
            "dd_changes_for_matrix": dd_changes_for_matrix,
        }
        # Convert dates to strings for JSON
        for tk, v in report["recent_dd_changes"].items():
            v["date"] = str(v["date"])
        print(json.dumps(report, indent=2, ensure_ascii=False))

        action_needed = (
            len(new_in_id_filtered) > 0
            or len(dd_changes_for_matrix) > 0
            or half_life_warning
        )
        return 1 if action_needed else 0

    # Pretty-print mode
    print("=" * 70)
    print("  🎯 Tier Matrix 健康度檢查（check_tier_matrix.py）")
    print("=" * 70)

    if publish_date:
        print(f"  Tier Matrix 上次更新：{publish_date}（距今 {days_since_publish} 天）")
    print(f"  目前已收錄 ticker：{len(matrix_tickers)} 檔")
    print()

    action_needed = False

    # Half-life warning
    if half_life_warning:
        action_needed = True
        print("⏰ **半衰期警示** — Tier Matrix 已超過 53 天未更新（半衰期 60 天）")
        print(f"   建議在 {(publish_date + timedelta(days=60)).isoformat()} 之前完整 review")
        print()

    # New tickers in IDs
    if new_in_id_filtered:
        action_needed = True
        print(f"🆕 **{len(new_in_id_filtered)} 檔在 ID 中出現但<strong>未列入 Tier Matrix</strong>：**")
        for tk in new_in_id_filtered:
            sources = id_tickers[tk][:3]
            extra = f"... +{len(id_tickers[tk]) - 3}" if len(id_tickers[tk]) > 3 else ""
            print(f"   • {tk:<12} 出現於 {len(id_tickers[tk])} 份 ID："
                  f" {', '.join(s.replace('ID_', '').replace('.html', '')[:30] for s in sources)}{extra}")
        print()
        print("   → 建議：請判斷是否加入 Tier Matrix（3 軸打分 + Tier 分級）")
        print()

    # DD signal changes
    if dd_changes_for_matrix:
        action_needed = True
        print(f"🔄 **{len(dd_changes_for_matrix)} 檔在 7 天內有 DD 更新且已在 Tier Matrix 中：**")
        for tk, info in sorted(dd_changes_for_matrix.items()):
            print(f"   • {tk:<8} 目前 {matrix_tickers[tk]}"
                  f" / DD 訊號 {info.get('signal', '—')}"
                  f" / 信心 {info.get('long_term_confidence', '—')}"
                  f"（{info['date']}）")
        print()
        print("   → 建議：檢查 DD 訊號變化是否觸發 Tier 重評")
        print()

    # Stale matrix tickers (in matrix but no ID source)
    if only_in_matrix and not quiet:
        print(f"🗑 **{len(only_in_matrix)} 檔在 Tier Matrix 中但未在任何 ID 出現（可考慮清理）：**")
        for tk in only_in_matrix[:5]:
            print(f"   • {tk:<12} {matrix_tickers[tk]}")
        if len(only_in_matrix) > 5:
            print(f"   ... +{len(only_in_matrix) - 5} 檔")
        print()

    # Summary
    print("=" * 70)
    if not action_needed:
        print("  ✅ Tier Matrix 與 ID / DD 同步，無需更新")
    else:
        print("  ⚠️  上述提示需要 PM 級判斷處理")
    print("=" * 70)

    return 1 if action_needed else 0


# ---------------------------------------------------------------------------
# HTML injection (for /research/ and /id/ landing pages)
# ---------------------------------------------------------------------------

INJECTION_MARKER_START = "<!-- TIER_MATRIX_ALERT_START -->"
INJECTION_MARKER_END = "<!-- TIER_MATRIX_ALERT_END -->"


def build_alert_html(report: dict) -> str:
    """Build HTML fragment for alert box."""
    new_in_id = report.get("new_in_id", [])
    dd_changes = report.get("dd_changes_for_matrix", {})
    half_life = report.get("half_life_warning", False)
    matrix_total = report.get("matrix_total", 0)
    publish_date = report.get("publish_date", "—")
    days_since = report.get("days_since_publish", 0)

    # Filter new_in_id to those in 2+ IDs (signal vs noise)
    sources = report.get("new_in_id_with_sources", {})
    high_signal_new = [
        tk for tk in new_in_id
        if len(sources.get(tk, [])) >= 2
    ]

    # Determine alert level
    has_action = bool(high_signal_new) or bool(dd_changes) or half_life

    if not has_action:
        # All in sync — show green status
        return f"""{INJECTION_MARKER_START}
<div style="background:linear-gradient(135deg,#DCFCE7,#F0FDF4);border-left:6px solid #166534;border-radius:8px;padding:14px 18px;margin:14px 0;color:#14532D;font-size:13px;line-height:1.7">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
    <strong>🎯 Tier Matrix 健康度：✅ 與 ID / DD 同步</strong>
    <span style="font-size:11px;color:#15803D">最新 {publish_date} · {matrix_total} 檔 · {days_since} 天前更新</span>
  </div>
</div>
{INJECTION_MARKER_END}"""

    # Build detailed alert
    alerts = []

    if half_life:
        alerts.append(
            f'<div><strong>⏰ 半衰期警示</strong>：'
            f'Tier Matrix {publish_date} 更新後已 {days_since} 天（半衰期 60 天），建議完整 review</div>'
        )

    if high_signal_new:
        ticker_list = "、".join(high_signal_new[:8])
        if len(high_signal_new) > 8:
            ticker_list += f" ...（共 {len(high_signal_new)} 檔）"
        alerts.append(
            f'<div><strong>🆕 {len(high_signal_new)} 檔新 ticker</strong>'
            f'（在 ≥ 2 份 ID 出現但未列入 Matrix）：<span style="font-family:monospace;color:#7F1D1D">'
            f'{ticker_list}</span></div>'
        )

    if dd_changes:
        # Show tickers with DD changes
        change_list = []
        for tk in sorted(dd_changes.keys())[:6]:
            info = dd_changes[tk]
            change_list.append(
                f'{tk}（DD {info.get("signal", "—")} / 信心 {info.get("long_term_confidence", "—")}）'
            )
        change_str = "、".join(change_list)
        if len(dd_changes) > 6:
            change_str += f" ...（共 {len(dd_changes)} 檔）"
        alerts.append(
            f'<div><strong>🔄 {len(dd_changes)} 檔近 7 天 DD 更新</strong>'
            f'（已在 Matrix 中，可能需重評 Tier）：<span style="font-family:monospace;color:#7F1D1D">'
            f'{change_str}</span></div>'
        )

    alerts_html = "\n  ".join(alerts)

    return f"""{INJECTION_MARKER_START}
<div style="background:linear-gradient(135deg,#FEF3C7,#FEFCE8);border-left:6px solid #CA8A04;border-radius:8px;padding:14px 18px;margin:14px 0;color:#713F12;font-size:13px;line-height:1.7">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:8px">
    <strong>🎯 Tier Matrix 健康度：⚠️ 需要 PM 級 review</strong>
    <span style="font-size:11px;color:#92400E">最新 {publish_date} · {matrix_total} 檔 · {days_since} 天前</span>
  </div>
  {alerts_html}
  <div style="margin-top:8px;font-size:12px"><a href="/id/tier_matrix.html" style="color:#7C3AED;font-weight:600">→ 查看 / 更新 Tier Matrix</a></div>
</div>
{INJECTION_MARKER_END}"""


def inject_html_alert(min_id_count: int = 2, include_geopolitics: bool = False) -> int:
    """Generate alert HTML and inject into /research/ and /id/ landing pages."""
    # First run check in JSON mode internally
    id_tickers: dict[str, list[str]] = {}
    if not ID_DIR.exists():
        print(f"❌ ID directory not found: {ID_DIR}")
        return 2

    for id_file in ID_DIR.glob("ID_*.html"):
        if not include_geopolitics and id_file.name.startswith("ID_CNTW_"):
            continue
        for tk in extract_tickers_from_html(id_file):
            id_tickers.setdefault(tk, []).append(id_file.name)

    matrix_tickers = extract_tier_matrix_tickers()
    dd_signals = get_recent_dd_signals(days=7)

    new_in_id = sorted(set(id_tickers.keys()) - set(matrix_tickers.keys()))
    new_in_id_filtered = [
        tk for tk in new_in_id
        if tk in KNOWN_TICKERS or "（" in tk or "." in tk
    ]

    publish_date = get_tier_matrix_publish_date()
    days_since_publish = (
        (date.today() - publish_date).days if publish_date else 0
    )
    half_life_warning = days_since_publish > 53

    dd_changes_for_matrix = {
        tk: signal
        for tk, signal in dd_signals.items()
        if tk in matrix_tickers
    }
    # Convert dates for serialization
    for tk in dd_changes_for_matrix:
        if isinstance(dd_changes_for_matrix[tk].get("date"), date):
            dd_changes_for_matrix[tk] = {
                **dd_changes_for_matrix[tk],
                "date": str(dd_changes_for_matrix[tk]["date"]),
            }

    report = {
        "publish_date": str(publish_date) if publish_date else "—",
        "days_since_publish": days_since_publish,
        "half_life_warning": half_life_warning,
        "matrix_total": len(matrix_tickers),
        "new_in_id": new_in_id_filtered,
        "new_in_id_with_sources": {
            tk: id_tickers[tk] for tk in new_in_id_filtered
        },
        "dd_changes_for_matrix": dd_changes_for_matrix,
    }

    alert_html = build_alert_html(report)

    # Inject into both pages
    targets = [
        REPO_ROOT / "docs" / "research" / "index.html",
        REPO_ROOT / "docs" / "id" / "index.html",
    ]

    for target in targets:
        if not target.exists():
            print(f"⚠️ {target} not found; skipping")
            continue
        content = target.read_text(encoding="utf-8")
        # Replace existing block if present
        pattern = re.compile(
            re.escape(INJECTION_MARKER_START) + r".*?" + re.escape(INJECTION_MARKER_END),
            re.DOTALL,
        )
        if pattern.search(content):
            new_content = pattern.sub(alert_html, content)
            print(f"✅ Updated alert in {target.relative_to(REPO_ROOT)}")
        else:
            # First time — insert at appropriate marker based on file
            if "research/index.html" in str(target):
                # Per user spec: insert AFTER "已發財報但 DD 未更新" banner
                anchor = "<!-- OUTDATED_DDS_BANNER_END -->"
                if anchor in content:
                    new_content = content.replace(
                        anchor, anchor + "\n" + alert_html, 1
                    )
                else:
                    # Fallback: after </header>
                    anchor = "</header>"
                    if anchor in content:
                        new_content = content.replace(anchor, anchor + "\n" + alert_html, 1)
                    else:
                        print(f"⚠️ Could not find insertion anchor in {target.name}; skipping")
                        continue
            else:
                # /id/index.html — per user spec: insert BEFORE "已建 ID 總數" flash card section
                # Use the 統計卡片 section comment as anchor
                anchor = "<!-- ========== 統計卡片 ========== -->"
                if anchor in content:
                    new_content = content.replace(anchor, alert_html + "\n\n  " + anchor, 1)
                else:
                    # Fallback: before <div class="stats-row">
                    fallback = '<div class="stats-row">'
                    if fallback in content:
                        new_content = content.replace(fallback, alert_html + "\n  " + fallback, 1)
                    else:
                        print(f"⚠️ Could not find insertion anchor in {target.name}; skipping")
                        continue
            print(f"✅ Inserted alert in {target.relative_to(REPO_ROOT)}")

        target.write_text(new_content, encoding="utf-8")

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--quiet", action="store_true", help="Only show actions needed")
    ap.add_argument("--min-id-count", type=int, default=2,
                    help="Only flag tickers in >= N IDs (default 2)")
    ap.add_argument("--include-geopolitics", action="store_true",
                    help="Include CNTW_* geopolitics IDs (default exclude)")
    ap.add_argument("--inject-html", action="store_true",
                    help="Inject HTML alert into /research/ and /id/ landing pages")
    args = ap.parse_args()

    if args.inject_html:
        return inject_html_alert(min_id_count=args.min_id_count,
                                  include_geopolitics=args.include_geopolitics)
    return run_check(quiet=args.quiet, json_out=args.json,
                     min_id_count=args.min_id_count,
                     include_geopolitics=args.include_geopolitics)


if __name__ == "__main__":
    sys.exit(main())
