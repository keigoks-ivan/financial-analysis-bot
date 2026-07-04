#!/usr/bin/env python3
"""決策引擎 L3 — 席位擂台（seat vs challenger）＋ regime 撥盤.

擂台規則（v1，2026-07-04 鎖定）：
  席位 = 現行漏斗同口徑（裁決＝進場＋核心角色，無條件優先，EV5y×確定性排序，核心 5 席；
         衛星 = 進場＋衛星角色，上限 5 席，空缺明示）。
  挑戰者 = 同「形狀」的未坐席候選（裁決 ∈ {進場, 觀望}），按 EV5y×確定性排序。
  ⚔ 擂台警報 = 挑戰者分數 > 席位分數 → 進人工複審清單（每月擂台裁決是人做的，
  本頁只把對戰表擺好——引擎不自動換席）。

Regime 撥盤（v1 規則鎖定；資訊性，不接倉位系統）：
  進攻 1.0 = SPY confirmed_uptrend 且 25 日 distribution ≤ 3
  中性 0.5 = under_pressure 或 distribution 4–7
  防守 0.25 = correction 或跌破 200DMA 或 distribution ≥ 8
  形狀敏感度：突破帶/動能重估 對 regime 最敏感；循環轉折次之；規則詳頁尾。

輸出：docs/engine/arena.json + arena.html。
Usage: python3 scripts/engine/build_arena.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.common import OUT_DIR, ROOT, page_shell, pct  # noqa: E402
from engine.build_scoreboard import _bars, classify_shape  # noqa: E402
from build_pipeline_page import (  # noqa: E402
    _certainty, _ev5y, _is_unconditional_core, _safe_float, is_core_role,
)

DD_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
MARKET_STATE = ROOT / "docs" / "screener" / "market_state.json"
UNIVERSE = ROOT / "data" / "engine" / "universe.json"
ARENA_JSON = OUT_DIR / "arena.json"
ARENA_HTML = OUT_DIR / "arena.html"

CORE_SLOTS = 5
SAT_SLOTS = 5
SHAPE_LABELS = {"breakout_base": "🟩 突破帶", "cyclical_turn": "🟧 循環轉折",
                "momentum_rerate": "🟪 動能重估", "other": "⬜ 其他"}


def regime_dial() -> dict:
    try:
        ms = json.loads(MARKET_STATE.read_text(encoding="utf-8"))
        spy = ms["indices"]["SPY"]
    except (OSError, json.JSONDecodeError, KeyError):
        return {"level": None, "label": "market_state 不可用", "detail": ""}
    state = spy.get("state")
    dist = (spy.get("distribution_days") or {}).get("count_25d") or 0
    below_200 = (spy.get("vs_200dma_pct") or 0) < 0
    if state == "correction" or below_200 or dist >= 8:
        level, label = 0.25, "🛡 防守"
    elif state == "under_pressure" or dist >= 4:
        level, label = 0.5, "⚖ 中性"
    else:
        level, label = 1.0, "🚀 進攻"
    return {"level": level, "label": label,
            "detail": f"SPY {state}（{spy.get('state_since', '—')} 起）· 25 日 distribution {dist} · "
                      f"vs 200DMA {spy.get('vs_200dma_pct', '—')}%",
            "as_of": ms.get("data_date")}


def shape_of(ticker: str) -> str:
    bars = _bars(ticker)
    if not bars:
        return "other"
    return classify_shape(bars, bars[-1][0])


def row_dict(s: dict) -> dict:
    return {"ticker": s["ticker"], "verdict": s.get("dca_verdict"),
            "role": s.get("dca_role"), "score": round(_ev5y(s) * _certainty(s), 2),
            "ev5y": round(_ev5y(s), 1), "cert": round(_certainty(s), 2),
            "upside_mid_pct": _safe_float(s.get("upside_mid_pct")),
            "moat": f'{s.get("moat_grade") or "?"}{s.get("moat_trend") or ""}',
            "shape": shape_of(s["ticker"]),
            "dd_path": s.get("dd_path")}


def main() -> int:
    stocks = json.loads(DD_LATEST.read_text(encoding="utf-8"))["stocks"]
    try:
        sectors = {r["ticker"]: r["sector"]
                   for r in json.loads(UNIVERSE.read_text(encoding="utf-8"))["tickers"]}
    except (OSError, json.JSONDecodeError, KeyError):
        sectors = {}

    core_pool = [s for s in stocks if s.get("dca_verdict") == "進場" and is_core_role(s)]
    for s in core_pool:
        s["_sc"] = _ev5y(s) * _certainty(s)
    uncond = sorted([s for s in core_pool if _is_unconditional_core(s)], key=lambda s: -s["_sc"])
    cond = sorted([s for s in core_pool if not _is_unconditional_core(s)], key=lambda s: -s["_sc"])
    core_seats = [row_dict(s) for s in (uncond + cond)[:CORE_SLOTS]]
    core_bench = [row_dict(s) for s in (uncond + cond)[CORE_SLOTS:]]

    sat_pool = [s for s in stocks if s.get("dca_verdict") == "進場" and not is_core_role(s)]
    for s in sat_pool:
        s["_sc"] = _ev5y(s) * _certainty(s)
    sat_seats = [row_dict(s) for s in sorted(sat_pool, key=lambda s: -s["_sc"])[:SAT_SLOTS]]

    seated = {r["ticker"] for r in core_seats + sat_seats}
    challengers = [row_dict(s) for s in stocks
                   if s.get("dca_verdict") in ("進場", "觀望") and s["ticker"] not in seated]
    challengers.sort(key=lambda r: -r["score"])

    # 擂台配對：每席 vs 同形狀最強挑戰者
    duels = []
    for seat in core_seats + sat_seats:
        rivals = [c for c in challengers if c["shape"] == seat["shape"]]
        top = rivals[0] if rivals else None
        duels.append({"seat": seat, "challenger": top,
                      "alert": bool(top and top["score"] > seat["score"])})

    # 席位產業集中度
    conc: dict[str, int] = {}
    for r in core_seats + sat_seats:
        sec = sectors.get(r["ticker"]) or "（未分類）"
        conc[sec] = conc.get(sec, 0) + 1
    n_seated = len(core_seats + sat_seats)
    conc_rows = sorted(conc.items(), key=lambda kv: -kv[1])
    max_share = (conc_rows[0][1] / n_seated * 100) if n_seated else 0

    dial = regime_dial()
    payload = {
        "schema_version": "1.0",
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regime": dial,
        "core_seats": core_seats, "core_bench": core_bench[:8],
        "sat_seats": sat_seats, "sat_vacant": SAT_SLOTS - len(sat_seats),
        "duels": duels, "challengers_top": challengers[:15],
        "concentration": [{"sector": k, "n": v} for k, v in conc_rows],
        "max_sector_share_pct": round(max_share),
    }

    # ── render ──
    def seat_tr(r, seat_no=None):
        up = pct(r["upside_mid_pct"], 0) if r["upside_mid_pct"] is not None else '<span class="muted">—</span>'
        link = f'<a href="{escape(r["dd_path"])}#decision">{escape(r["ticker"])}</a>' if r.get("dd_path") else escape(r["ticker"])
        return (f'<tr><td class="left">{f"{seat_no}." if seat_no else ""} <strong>{link}</strong></td>'
                f'<td class="left">{SHAPE_LABELS.get(r["shape"], r["shape"])}</td>'
                f'<td>{r["score"]:.1f}</td><td>{pct(r["ev5y"], 1, False)}</td>'
                f'<td>{r["cert"]:.2f}</td><td>{up}</td>'
                f'<td class="left">{escape(r["moat"])}</td></tr>')

    def duel_tr(d):
        s, c = d["seat"], d["challenger"]
        if not c:
            rhs = '<span class="muted">同形狀無挑戰者</span>'
        else:
            link = f'<a href="{escape(c["dd_path"])}#decision">{escape(c["ticker"])}</a>' if c.get("dd_path") else escape(c["ticker"])
            rhs = (f'{link}（{c["verdict"]}，分數 {c["score"]:.1f}）')
        flag = '<span class="tag tag-dn">⚔ 警報</span>' if d["alert"] else '<span class="tag tag-up">守住</span>'
        return (f'<tr><td class="left"><strong>{escape(s["ticker"])}</strong>（{s["score"]:.1f}）</td>'
                f'<td class="left">{SHAPE_LABELS.get(s["shape"], s["shape"])}</td>'
                f'<td class="left">{rhs}</td><td>{flag}</td></tr>')

    head = ('<table><thead><tr><th class="left">席位</th><th class="left">形狀</th>'
            '<th>分數</th><th>EV5y</th><th>確定性</th><th>2Y upside</th><th class="left">護城河</th>'
            '</tr></thead><tbody>')
    core_tbl = head + "".join(seat_tr(r, i) for i, r in enumerate(core_seats, 1)) + "</tbody></table>"
    sat_body = "".join(seat_tr(r, i) for i, r in enumerate(sat_seats, 1))
    for i in range(payload["sat_vacant"]):
        sat_body += (f'<tr><td class="left">{len(sat_seats)+i+1}. <span class="muted">（空缺）</span></td>'
                     f'<td class="left muted" colspan="6">等衛星候選拿到進場裁決 — 見補 DD 隊列</td></tr>')
    sat_tbl = head + sat_body + "</tbody></table>"
    duel_tbl = ('<table><thead><tr><th class="left">席位（分數）</th><th class="left">形狀</th>'
                '<th class="left">同形狀最強挑戰者</th><th>裁定</th></tr></thead><tbody>'
                + "".join(duel_tr(d) for d in duels) + "</tbody></table>")
    conc_html = "、".join(f'{escape(k["sector"])} ×{k["n"]}' for k in payload["concentration"])
    conc_warn = (f'<div class="note warn">⚠ 單一產業占席 {payload["max_sector_share_pct"]}%'
                 f'（>50% 集中度警戒）——擂台換人時優先考慮異產業挑戰者。</div>'
                 if payload["max_sector_share_pct"] > 50 else "")

    body = f"""<div class="hero">
<h1>⚔ 席位擂台 · L3 組合層</h1>
<div class="hero-sub">組合才是產品：核心 {CORE_SLOTS} 席＋衛星 {SAT_SLOTS} 席，每席對決「同形狀最強挑戰者」。
⚔ 警報＝挑戰者分數超過席位 → 進<b>每月擂台的人工複審清單</b>。引擎不自動換席——換人是人的裁決。
分數＝EV5y×確定性；2Y upside 併列給 1–3 年 mandate 參照。</div>
<div class="asof">資料源 dd-screener latest.json ｜ 席位口徑與 Pipeline 頁一致 ｜ 週更</div>
</div>
<div class="stat-row">
<div class="stat"><strong>{dial['label'] if dial['level'] else '—'}</strong><span>Regime 撥盤（{dial['level'] if dial['level'] else '—'}×）</span></div>
<div class="stat"><strong>{sum(1 for d in duels if d['alert'])}</strong><span>⚔ 擂台警報</span></div>
<div class="stat"><strong>{len(core_seats)}/{CORE_SLOTS} · {len(sat_seats)}/{SAT_SLOTS}</strong><span>核心 · 衛星席位</span></div>
<div class="stat"><strong>{payload['max_sector_share_pct']}%</strong><span>最大單一產業占席</span></div>
</div>
<div class="note">Regime：{escape(dial.get('detail') or '')}（as of {escape(str(dial.get('as_of') or '—'))}）。
撥盤規則 v1 鎖定：進攻 1.0＝confirmed_uptrend 且 distribution ≤3；中性 0.5＝under_pressure 或 4–7；
防守 0.25＝correction／跌破 200DMA／≥8。<b>資訊性，不接倉位系統</b>——新倉節奏由人按撥盤自裁。
形狀敏感度：突破帶/動能重估最敏感（防守時停新倉）、循環轉折次之（防守時只留回踩單）。</div>
<div class="block"><h2>核心席位（{len(core_seats)}/{CORE_SLOTS}）</h2>{core_tbl}</div>
<div class="block"><h2>衛星席位（{len(sat_seats)}/{SAT_SLOTS}）</h2>{sat_tbl}</div>
<div class="block"><h2>擂台對戰表</h2>
<div class="block-sub">每席 vs 同形狀最強未坐席挑戰者（裁決 ∈ {{進場, 觀望}}）。觀望挑戰者勝出＝先觸發它的複審，不是直接換。</div>
{duel_tbl}</div>
<div class="block"><h2>席位產業分布</h2><div class="block-sub">{conc_html}</div>{conc_warn}</div>
<div class="note">板凳（核心第 6 席起）：{escape('、'.join(r['ticker'] for r in core_bench[:8]) or '—')}。
挑戰者池 top：{escape('、'.join(r['ticker'] for r in payload['challengers_top'][:10]))}。</div>"""

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ARENA_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    ARENA_HTML.write_text(
        page_shell("席位擂台 · 決策引擎", "/engine/arena.html", body,
                   "核心 5＋衛星 5 席位 vs 同形狀挑戰者的每月擂台 — regime 撥盤與集中度警戒"),
        encoding="utf-8")
    print(f"arena: regime={dial['label']} 警報={sum(1 for d in duels if d['alert'])} "
          f"核心={[r['ticker'] for r in core_seats]} 衛星={[r['ticker'] for r in sat_seats]} "
          f"集中度={payload['max_sector_share_pct']}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
