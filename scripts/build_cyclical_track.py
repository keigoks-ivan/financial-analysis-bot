#!/usr/bin/env python3
"""Cyclical Track (衛星·循環軌) — QC-42 代理版 v0 循環候選提名層.

設計 source-of-truth: docs/_handoff_stock_sleeve_pipeline_20260703.md（Task 2）

定位：**研究提名清單，不是進場清單**。挑出「trailing 財務難看（循環底部）但
分析師正在上修」的標的，供 stock-analyst v14 DD（含 QC-42 循環鏡頭附錄 B）與
sop-funnel 板機接手。每檔要進場仍須 (a) DD 裁決＝進場 (b) 板機亮燈。

資格規則（門檻為持有人拍板，勿自行調參）：
  1. 循環特徵：fail_criteria ∩ {fcf, roic} ≠ ∅（trailing 財務難看）
  2. 上修動能（單月，baseline 見 latest.json eps_revision_baseline_date）：
       eps2y_revision_pp ≥ +3  或  eps_fy_next_revision_pct ≥ +5
       或  eps_fy_curr_revision_pct ≥ +3
  3. 護城河底線：moat_grade ≠ X 且非（C 且 trend ↓）
  4. 排除已過品質閘者（歸核心/結構軌，一檔一軌）：
       fail_criteria 去掉 'de' 後為空 且 moat_grade∈{S,A,B} 且 moat_trend≠↓
       —— 此口徑不依賴 latest.json 的 pass_count 欄位（Task 1 並行改動中，
          該欄口徑可能新舊不一），直接自算。

熱度閘（反動能）：12M 報酬 > +250%（用 data/weekly_cache 週線算）→ 標 🔥
「等回踩」，名單保留但排序沉底、明文不可追。

排序：eps2y_revision_pp + eps_fy_next_revision_pct 降冪；低熱組置頂。

Usage:
  python3 scripts/build_cyclical_track.py
  python3 scripts/build_cyclical_track.py --dry-run     # 不寫檔
  python3 scripts/build_cyclical_track.py --no-snapshot # 不寫 daily snapshot
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import DD_SCREENER_SUBNAV, build_subnav, full_nav_block  # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
LATEST_JSON = ROOT / "docs" / "dd-screener" / "latest.json"
WEEKLY_CACHE_DIR = ROOT / "data" / "weekly_cache"
OUTPUT_DIR = ROOT / "docs" / "dd-screener"
HTML_OUT = OUTPUT_DIR / "cyclical-track.html"
JSON_OUT = OUTPUT_DIR / "cyclical-track.json"
SNAPSHOT_DIR = OUTPUT_DIR / "cyclical-track-snapshots"

NAV_BLOCK = full_nav_block(
    "pick", "dds", build_subnav(DD_SCREENER_SUBNAV, "/dd-screener/cyclical-track.html")
)

TAIPEI_TZ = timezone(timedelta(hours=8))
SCHEMA_VERSION = "1.0"

# ── 門檻常數（持有人拍板，勿自行調參）─────────────────────────────────────────
CYCLICAL_FAIL_KEYS = {"fcf", "roic"}        # rule 1
REV_EPS2Y_PP_MIN = 3.0                      # rule 2a
REV_FY_NEXT_PCT_MIN = 5.0                   # rule 2b
REV_FY_CURR_PCT_MIN = 3.0                   # rule 2c
QUALITY_MOAT_GRADES = {"S", "A", "B"}       # rule 4
HEAT_12M_RET_THRESHOLD = 2.50               # 熱度閘：12M 報酬 > +250% → 🔥
SINGLE_NAME_CAP_PCT = 3.0                   # 單檔上限（個股部淨值）


# ── helpers ───────────────────────────────────────────────────────────────────
def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def _today() -> str:
    return datetime.now(TAIPEI_TZ).strftime("%Y-%m-%d")


def _safe_float(x) -> Optional[float]:
    if x is None:
        return None
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    if f != f:  # NaN
        return None
    return f


def return_12m(ticker: str) -> Optional[float]:
    """12M 報酬 = weekly_bars[-1].close / weekly_bars[-53].close - 1（bars 不足→None）."""
    p = WEEKLY_CACHE_DIR / f"{ticker}.json"
    if not p.exists():
        return None
    try:
        bars = json.loads(p.read_text(encoding="utf-8")).get("weekly_bars", []) or []
    except (json.JSONDecodeError, OSError):
        return None
    if len(bars) < 53:
        return None
    c_now = _safe_float(bars[-1].get("close"))
    c_prev = _safe_float(bars[-53].get("close"))
    if not c_now or not c_prev:
        return None
    return c_now / c_prev - 1.0


# ── qualification ─────────────────────────────────────────────────────────────
def is_cyclical(s: dict) -> bool:
    """Rule 1: trailing 財務難看（fcf 或 roic 未過）."""
    fail = set(s.get("fail_criteria") or [])
    return bool(fail & CYCLICAL_FAIL_KEYS)


def has_upward_revision(s: dict) -> bool:
    """Rule 2: 任一上修訊號達門檻."""
    a = _safe_float(s.get("eps2y_revision_pp"))
    b = _safe_float(s.get("eps_fy_next_revision_pct"))
    c = _safe_float(s.get("eps_fy_curr_revision_pct"))
    return ((a is not None and a >= REV_EPS2Y_PP_MIN)
            or (b is not None and b >= REV_FY_NEXT_PCT_MIN)
            or (c is not None and c >= REV_FY_CURR_PCT_MIN))


def passes_moat_floor(s: dict) -> bool:
    """Rule 3: moat_grade ≠ X 且非（C 且 trend ↓）."""
    mg = s.get("moat_grade")
    mt = s.get("moat_trend")
    if mg == "X":
        return False
    if mg == "C" and mt == "↓":
        return False
    return True


def already_quality_passed(s: dict) -> bool:
    """Rule 4: 已過品質閘（歸核心/結構軌）— 自算口徑，不依賴 pass_count.

    fail_criteria 去掉 'de' 後為空 且 moat_grade∈{S,A,B} 且 moat_trend≠↓.
    """
    fail_no_de = set(s.get("fail_criteria") or []) - {"de"}
    mg = s.get("moat_grade")
    mt = s.get("moat_trend")
    return (len(fail_no_de) == 0
            and mg in QUALITY_MOAT_GRADES
            and mt != "↓")


def revision_rank_score(s: dict) -> float:
    """排序鍵：eps2y_revision_pp + eps_fy_next_revision_pct 降冪."""
    a = _safe_float(s.get("eps2y_revision_pp")) or 0.0
    b = _safe_float(s.get("eps_fy_next_revision_pct")) or 0.0
    return a + b


def build_row(s: dict) -> dict:
    ret = return_12m(s["ticker"])
    hot = ret is not None and ret > HEAT_12M_RET_THRESHOLD
    return {
        "ticker": s["ticker"],
        "name": s.get("name", ""),
        "sector": s.get("sector", ""),
        "signal": s.get("signal"),
        "moat_grade": s.get("moat_grade"),
        "moat_trend": s.get("moat_trend"),
        "fail_criteria": s.get("fail_criteria") or [],
        "eps2y_revision_pp": _safe_float(s.get("eps2y_revision_pp")),
        "eps_fy_next_revision_pct": _safe_float(s.get("eps_fy_next_revision_pct")),
        "eps_fy_curr_revision_pct": _safe_float(s.get("eps_fy_curr_revision_pct")),
        "revision_rank_score": round(revision_rank_score(s), 2),
        "ret_12m_pct": round(ret * 100, 1) if ret is not None else None,
        "hot": hot,
        "dca_verdict": s.get("dca_verdict"),
        "ev5y_pct": s.get("ev5y_pct"),
        "live_ev5y_pct": s.get("live_ev5y_pct"),
        "dd_path": s.get("dd_path"),
        "dd_age_days": s.get("dd_age_days"),
    }


# ── build pipeline ────────────────────────────────────────────────────────────
def build_pipeline() -> dict:
    print(f"=== Cyclical-Track build · {_now_taipei_iso()} ===\n")
    if not LATEST_JSON.exists():
        print(f"  ERR: {LATEST_JSON} not found — run scripts/build_dd_screener.py first",
              file=sys.stderr)
        sys.exit(2)

    data = json.loads(LATEST_JSON.read_text(encoding="utf-8"))
    universe = data.get("stocks", []) or []
    schema_ver = data.get("schema_version", "?")
    as_of = data.get("as_of", _today())
    baseline_date = data.get("eps_revision_baseline_date")
    print(f"  Loaded latest.json schema_version={schema_ver} as_of={as_of} "
          f"universe={len(universe)} stocks")

    qualified: list[dict] = []
    for s in universe:
        if not is_cyclical(s):
            continue
        if not has_upward_revision(s):
            continue
        if not passes_moat_floor(s):
            continue
        if already_quality_passed(s):
            continue
        qualified.append(build_row(s))

    # 排序：revision_rank_score 降冪；低熱組整體置頂於熱組之上
    low_heat = [r for r in qualified if not r["hot"]]
    hot_heat = [r for r in qualified if r["hot"]]
    low_heat.sort(key=lambda r: (-r["revision_rank_score"], r["ticker"]))
    hot_heat.sort(key=lambda r: (-r["revision_rank_score"], r["ticker"]))

    print(f"  Qualified: {len(qualified)} "
          f"(低熱 {len(low_heat)} / 🔥已熱 {len(hot_heat)})")
    if low_heat:
        print(f"  低熱 top: {[r['ticker'] for r in low_heat[:8]]}")
    if hot_heat:
        print(f"  🔥已熱: {[r['ticker'] for r in hot_heat]}")

    return {
        "schema_version": SCHEMA_VERSION,
        "run_timestamp": _now_taipei_iso(),
        "as_of": as_of,
        "eps_revision_baseline_date": baseline_date,
        "universe_total": len(universe),
        "qualified_total": len(qualified),
        "low_heat_count": len(low_heat),
        "hot_count": len(hot_heat),
        "thresholds": {
            "cyclical_fail_keys": sorted(CYCLICAL_FAIL_KEYS),
            "rev_eps2y_pp_min": REV_EPS2Y_PP_MIN,
            "rev_fy_next_pct_min": REV_FY_NEXT_PCT_MIN,
            "rev_fy_curr_pct_min": REV_FY_CURR_PCT_MIN,
            "heat_12m_ret_threshold": HEAT_12M_RET_THRESHOLD,
            "single_name_cap_pct": SINGLE_NAME_CAP_PCT,
        },
        "low_heat": low_heat,
        "hot": hot_heat,
    }


# ── HTML rendering ────────────────────────────────────────────────────────────
def _fmt_signed(v: Optional[float], decimals: int = 1) -> str:
    if v is None:
        return "—"
    return f"{'+' if v >= 0 else ''}{v:.{decimals}f}"


def _ticker_link(row: dict) -> str:
    dd = row.get("dd_path")
    label = row["ticker"]
    if dd:
        return f'<a href="{dd}#decision">{label}</a>'
    return label


def _verdict_badge(v: Optional[str]) -> str:
    if not v:
        return '<span class="verdict v-none">待補 DD</span>'
    cls = {"進場": "v-in", "觀望": "v-watch", "迴避": "v-avoid"}.get(v, "v-none")
    return f'<span class="verdict {cls}">{v}</span>'


def _fail_tags(fc: list) -> str:
    return " ".join(f'<span class="ftag">{k}</span>' for k in fc) or "—"


def _row_html(row: dict) -> str:
    ret = row.get("ret_12m_pct")
    ret_str = f"{'+' if (ret or 0) >= 0 else ''}{ret:.0f}%" if ret is not None else "—"
    ret_cls = "ret-hot" if row.get("hot") else ("ret-pos" if (ret or 0) >= 0 else "ret-neg")
    name = row.get("name") or ""
    name_html = f'<span class="nm">{name}</span>' if name and name != row["ticker"] else ""
    return f"""<tr>
  <td class="left">{_ticker_link(row)}{name_html}</td>
  <td class="score-cell"><strong>{row['revision_rank_score']:.1f}</strong></td>
  <td>{_fmt_signed(row.get('eps2y_revision_pp'))}</td>
  <td>{_fmt_signed(row.get('eps_fy_next_revision_pct'))}</td>
  <td>{_fmt_signed(row.get('eps_fy_curr_revision_pct'))}</td>
  <td class="{ret_cls}">{ret_str}</td>
  <td class="meta-cell">{row.get('moat_grade') or '—'} {row.get('moat_trend') or ''} · {_fail_tags(row.get('fail_criteria'))}</td>
  <td>{_verdict_badge(row.get('dca_verdict'))}</td>
</tr>"""


def _section_table(rows: list[dict], empty_msg: str) -> str:
    if not rows:
        return f'<div class="empty-row">{empty_msg}</div>'
    body = "\n".join(_row_html(r) for r in rows)
    return f"""<table>
<thead>
<tr>
  <th class="left">Ticker</th>
  <th>排序分</th>
  <th>2Y修正pp</th>
  <th>FY+1修正%</th>
  <th>FY0修正%</th>
  <th>12M報酬</th>
  <th class="left">護城河 · 未過項</th>
  <th>站上裁決</th>
</tr>
</thead>
<tbody>
{body}
</tbody>
</table>"""


def _fmt_taipei_stamp(iso_str: Optional[str]) -> str:
    if not iso_str or "T" not in iso_str:
        return iso_str or "—"
    date, time = iso_str.split("T", 1)
    return f"{date} {time[:5]}"


def render_html(doc: dict, out_path: Path) -> None:
    as_of = doc["as_of"]
    baseline = doc.get("eps_revision_baseline_date") or "—"
    run_ts_display = _fmt_taipei_stamp(doc.get("run_timestamp"))
    universe_total = doc["universe_total"]
    qualified_total = doc["qualified_total"]
    low_heat = doc["low_heat"]
    hot = doc["hot"]

    low_html = _section_table(
        low_heat,
        '目前無低熱循環候選 —— 可能是上修動能整體降溫，或候選都已進 🔥 等回踩組。'
    )
    hot_html = _section_table(
        hot,
        '目前無 🔥 已熱候選。'
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>衛星·循環軌 — 循環底部 × 上修動能提名層 | InvestMQuest</title>
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/imq-base.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:var(--sans);background:var(--paper);color:var(--body);line-height:1.5}}
.hero{{background:var(--card);border-bottom:1px solid var(--line);padding:24px 32px 18px}}
.hero-inner{{max-width:min(1400px,96vw);margin:0 auto}}
.hero-h1{{font-family:var(--serif);font-size:22px;font-weight:700;letter-spacing:-.01em;color:var(--ink);margin-bottom:6px}}
.hero-sub{{font-size:12px;color:var(--sec);line-height:1.6;max-width:960px}}
.hero-stats{{display:flex;gap:14px;margin-top:12px;flex-wrap:wrap}}
.hero-stat{{background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:7px 11px;font-size:11px;color:var(--sec)}}
.hero-stat strong{{font-family:var(--mono);font-variant-numeric:tabular-nums;color:var(--ink);font-size:13px;display:block;margin-bottom:1px}}
.section{{max-width:min(1400px,96vw);margin:0 auto;padding:24px 32px}}
.formula-panel{{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh-1);padding:14px 18px;margin-bottom:20px}}
.formula-panel h3{{font-family:var(--sans);font-size:13px;font-weight:700;color:var(--ink);margin-bottom:8px}}
.formula-panel code{{background:var(--line-soft);padding:1px 6px;border-radius:5px;font-family:var(--mono);font-size:11.5px;color:var(--ink)}}
.formula-row{{font-size:12px;color:var(--body);line-height:1.85}}
.warn-panel{{background:#f8f1e2;border:1px solid rgba(138,109,31,.25);border-radius:var(--r);padding:14px 18px;margin-bottom:20px;font-size:12.5px;color:var(--warn);line-height:1.7}}
.warn-panel strong{{color:var(--warn);display:block;margin-bottom:6px;font-size:13px}}
.warn-panel ul{{margin-left:18px;margin-top:6px}}
.tier-card{{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh-1);padding:16px 18px;margin-bottom:22px}}
.tier-card h2{{font-family:var(--serif);font-size:16px;font-weight:700;margin-bottom:4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;color:var(--ink)}}
.tier-card.tier-low h2{{color:var(--pos)}}
.tier-card.tier-hot h2{{color:var(--warn)}}
.tier-card h2 .badge{{display:inline-block;padding:2px 9px;border-radius:5px;font-family:var(--mono);font-size:11px;font-weight:700}}
.tier-card.tier-low h2 .badge{{background:#eaf5ef;color:var(--pos)}}
.tier-card.tier-hot h2 .badge{{background:#f8f1e2;color:var(--warn)}}
.tier-card .desc{{font-size:12px;color:var(--sec);margin-bottom:10px;line-height:1.6}}
.tier-card table{{width:100%;border-collapse:collapse;font-size:12px}}
.tier-card th{{font-family:var(--mono);background:none;color:var(--sec);font-weight:600;padding:8px 10px;text-align:right;border-bottom:1px solid var(--line);font-size:10px;letter-spacing:.08em;text-transform:uppercase}}
.tier-card th.left{{text-align:left}}
.tier-card td{{padding:8px 10px;text-align:right;border-bottom:1px solid var(--line-soft);font-variant-numeric:tabular-nums;color:var(--body)}}
.tier-card tbody tr:hover td{{background:#f7f4ec}}
.tier-card td.left{{text-align:left;color:var(--ink);font-weight:500}}
.tier-card td.left .nm{{display:block;font-size:10px;color:var(--muted);font-weight:400;margin-top:1px}}
.tier-card td:nth-child(3),.tier-card td:nth-child(4),.tier-card td:nth-child(5){{font-family:var(--mono)}}
.tier-card td a{{color:var(--accent);text-decoration:none;font-weight:700}}
.tier-card td a:hover{{text-decoration:underline}}
.score-cell{{color:var(--ink);font-family:var(--mono)}}
.ret-hot{{color:var(--warn);font-weight:700;font-family:var(--mono)}}
.ret-pos{{color:var(--pos);font-family:var(--mono)}}
.ret-neg{{color:var(--neg);font-family:var(--mono)}}
.meta-cell{{font-size:10.5px;color:var(--sec);text-align:left !important}}
.ftag{{display:inline-block;background:#faecea;color:var(--neg);padding:0 5px;border-radius:5px;font-size:9.5px;margin-left:2px}}
.verdict{{padding:1px 8px;border-radius:5px;font-family:var(--mono);font-size:10.5px;font-weight:700}}
.v-in{{background:#eaf5ef;color:var(--pos)}}
.v-watch{{background:#f8f1e2;color:var(--warn)}}
.v-avoid{{background:#faecea;color:var(--neg)}}
.v-none{{background:var(--line-soft);color:var(--muted);font-weight:600}}
.empty-row{{padding:14px;text-align:center;color:var(--muted);font-size:12px;font-style:italic}}
.meta-note{{padding:30px 32px 4px;font-size:11px;color:var(--sec);line-height:1.7;max-width:min(1400px,96vw);margin:0 auto;border-top:1px solid var(--line)}}
.meta-note h4{{color:var(--ink);font-size:12px;margin-top:14px;margin-bottom:6px;font-weight:700}}
.meta-note code{{background:var(--line-soft);padding:1px 5px;border-radius:5px;font-family:var(--mono);font-size:10px;color:var(--ink)}}
.imq-foot{{margin-top:8px;padding:16px 32px 24px;font-size:11px;color:var(--muted);line-height:1.8;max-width:min(1400px,96vw);margin-left:auto;margin-right:auto;text-align:center}}
.imq-foot a{{color:var(--accent);text-decoration:none}}
.imq-foot a:hover{{text-decoration:underline}}
</style>
</head>
<body>
{NAV_BLOCK}

<div class="hero">
  <div class="hero-inner">
    <div class="hero-h1">衛星·循環軌 — 循環底部 × 上修動能</div>
    <div class="hero-sub">
      個股部第三軌（衛星·循環）的<b>研究提名層</b>。鎖定「trailing 財務難看（FCF／ROIC 未過＝循環底部）
      <b>但分析師正在上修</b>」的標的——這是 QC-42 診斷的 mandate gap（SNDK／MU 型循環贏家全滅於品質閘）的
      代理捕手。輸出<b>不是進場清單</b>，是交給個股 DD（QC-42 循環鏡頭附錄 B）與板機接手的候選池。
    </div>
    <div class="hero-stats">
      <div class="hero-stat"><strong>{run_ts_display}</strong>最後更新（台北）</div>
      <div class="hero-stat"><strong>{as_of}</strong>資料 as of</div>
      <div class="hero-stat"><strong>{baseline}</strong>上修 baseline</div>
      <div class="hero-stat"><strong>{universe_total}</strong>universe</div>
      <div class="hero-stat"><strong>{qualified_total}</strong>循環候選</div>
      <div class="hero-stat"><strong>{len(low_heat)} / {len(hot)}</strong>低熱 / 🔥已熱</div>
    </div>
  </div>
</div>

<div class="section">

  <div class="warn-panel">
    <strong>⚠ 研究提名清單，不是進場清單</strong>
    本軌只回答「該研究誰」。每檔要真正進場，仍須同時通過：
    <ul>
      <li>(a) v14 個股 DD 統一裁決＝<b>進場</b>（含 QC-42 循環鏡頭附錄 B 的反動能硬閘）；</li>
      <li>(b) sop-funnel 板機亮燈（T+1 執行）。</li>
    </ul>
    單檔上限 <b>{SINGLE_NAME_CAP_PCT:.0f}%</b>（個股部淨值，衛星倉位）。🔥 標記者為 12M 報酬 &gt; +250%，
    <b>明文不可追高</b>——名單保留、排序沉底，等回踩進 sweet spot 再由 DD／板機把關。
  </div>

  <div class="formula-panel">
    <h3>資格規則（QC-42 代理版 v0，門檻為持有人拍板）</h3>
    <div class="formula-row">
      <b>1 循環特徵</b>：<code>fail_criteria ∩ {{fcf, roic}} ≠ ∅</code>（trailing 財務難看＝循環底部）
    </div>
    <div class="formula-row">
      <b>2 上修動能</b>（單月，baseline {baseline}）：<code>eps2y_revision_pp ≥ +{REV_EPS2Y_PP_MIN:.0f}</code>
      或 <code>eps_fy_next_revision_pct ≥ +{REV_FY_NEXT_PCT_MIN:.0f}</code>
      或 <code>eps_fy_curr_revision_pct ≥ +{REV_FY_CURR_PCT_MIN:.0f}</code>
    </div>
    <div class="formula-row">
      <b>3 護城河底線</b>：<code>moat_grade ≠ X</code> 且非（<code>C</code> 且 trend <code>↓</code>）
    </div>
    <div class="formula-row">
      <b>4 排除已過品質閘者</b>（歸核心／結構軌，一檔一軌）：<code>fail_criteria −{{de}} 為空 且 moat∈{{S,A,B}} 且 trend≠↓</code>
    </div>
    <div class="formula-row" style="margin-top:8px;color:var(--sec)">
      <b>熱度閘</b>：12M 報酬（週線 <code>close[-1]/close[-53]−1</code>）&gt; +250% → 🔥「等回踩」，排序沉底。
      <b>排序</b>：<code>eps2y_revision_pp + eps_fy_next_revision_pct</code> 降冪；低熱組整體置頂。
    </div>
  </div>

  <div class="tier-card tier-low">
    <h2>🟢 低熱組 — 可研究 <span class="badge">12M ≤ +250% · 上修中</span></h2>
    <div class="desc">循環底部 + 分析師上修，且尚未過熱——這是本軌最有研究增量的名字。點 Ticker 連站上 DD 裁決錨點；「待補 DD」者即研究隊列。</div>
    {low_html}
  </div>

  <div class="tier-card tier-hot">
    <h2>🔥 已熱組 — 等回踩，明文不可追 <span class="badge">12M &gt; +250%</span></h2>
    <div class="desc">同樣通過循環＋上修資格，但 12M 報酬已 &gt; +250%，反動能閘擋在門外。保留追蹤，等回踩到 sweet spot 再由 DD／板機把關；<b>此組不可直接追高</b>。</div>
    {hot_html}
  </div>

  <div class="meta-note">
    <h4>數據來源</h4>
    <ul style="margin-left:18px">
      <li><code>docs/dd-screener/latest.json</code>（fail_criteria / eps_*_revision_* / moat_grade / moat_trend / dca_verdict 等 dd-meta propagated 欄位）</li>
      <li>12M 報酬：<code>data/weekly_cache/{{TICKER}}.json</code> 週線 <code>close[-1]/close[-53]−1</code>（bars 不足即不計熱度）</li>
    </ul>
    <h4>下游</h4>
    <p>候選 → <code>stock-analyst</code> v14 DD（QC-42 循環鏡頭附錄 B）→ sop-funnel 板機 → 個股部衛星倉位（單檔 ≤ {SINGLE_NAME_CAP_PCT:.0f}%）。</p>
    <h4>機器可讀</h4>
    <p>JSON sidecar: <a href="/dd-screener/cyclical-track.json"><code>/dd-screener/cyclical-track.json</code></a> · 每週快照：<code>/dd-screener/cyclical-track-snapshots/YYYY-MM-DD.json</code>（schema v{SCHEMA_VERSION}）</p>
  </div>

</div>

<footer class="imq-foot">
  <div>© 2026 InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✓ Wrote {out_path} ({out_path.stat().st_size:,} bytes)")


# ── main ──────────────────────────────────────────────────────────────────────
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Don't write files")
    p.add_argument("--no-snapshot", action="store_true", help="Skip snapshot write")
    args = p.parse_args()

    doc = build_pipeline()

    if args.dry_run:
        print("\n  (dry-run) skipping writes")
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  ✓ Wrote {JSON_OUT} ({JSON_OUT.stat().st_size:,} bytes)")

    render_html(doc, HTML_OUT)

    if not args.no_snapshot:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        snap_path = SNAPSHOT_DIR / f"{_today()}.json"
        snap_path.write_text(
            json.dumps(doc, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  ✓ Wrote snapshot {snap_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
