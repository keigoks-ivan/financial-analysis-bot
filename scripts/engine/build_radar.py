#!/usr/bin/env python3
"""決策引擎 L0+L1 — 全市場雷達（結構掃描 × 形狀路由 × EPS 修正確認）.

兩階段設計（決策帶寬原則：廣掃自動化、深挖只給候選）：
  Stage 1（批量，全 universe ~1,500 檔）：25 個月週線 → 結構訊號
    ret_12m / ret_13w / RS 百分位 / 距 ATH / 基期週數 / 40 週線 / 深跌-轉折
  Stage 2（逐檔，只對四形狀候選 ≤160 檔）：yfinance eps_trend →
    FY+1 EPS 30 天修正%（拐點確認）。抓取失敗 → 沿用上一版 radar.json 的值。

四形狀（v1 門檻 2026-07-04 鎖定 — PREREG 慣例：季檢才可調，禁止盤中調參）：
  breakout_base 長基期突破帶：基期 ≥26 週 ∩ 距 ATH ≥ -5% ∩ 站上 40 週線
  cyclical_turn 循環轉折：自高點深跌 ≤ -40% ∩ 13 週 ≥ +10% ∩ 距 ATH ≤ -25%（早段）
  momentum_rerate 動能重估：12M RS ≥ P90 ∩ 站上 40 週線 ∩ 距 ATH ≥ -15%
  theme_smallmid 主題下沉：中型股（sp400）∩ RS ≥ P75 ∩ 站上 40 週線 ∩ 產業 13 週熱度 top3
  （universe v1.1 2026-07-04 持有人拍板：sp500 ∪ ndx100 ∪ sp400，排除 sp600 小型股）

輸出：docs/engine/radar.json + docs/engine/radar.html（成功才寫檔 — fail-safe 慣例）。
Usage: python3 scripts/engine/build_radar.py [--skip-stage2]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.common import OUT_DIR, ROOT, page_shell, pct  # noqa: E402

UNIVERSE = ROOT / "data" / "engine" / "universe.json"
DD_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
WEEKLY_CACHE = ROOT / "data" / "weekly_cache"
RADAR_JSON = OUT_DIR / "radar.json"
RADAR_HTML = OUT_DIR / "radar.html"

# ── v1 形狀門檻（2026-07-04 鎖定；季檢才可調）────────────────────────────────
P = {
    "base_age_min_w": 26, "breakout_dist_ath": -5.0,
    "cyc_depth": -40.0, "cyc_turn_13w": 10.0, "cyc_dist_ath_max": -25.0,
    "mom_rs_pct": 90.0, "mom_dist_ath": -15.0,
    "theme_rs_pct": 75.0, "theme_hot_sectors": 3,
    "display_top_n": 25, "stage2_top_n": 30,
    "rev_confirm_pct": 2.0,   # 30 天 FY+1 上修 ≥ +2% = 拐點確認 ★
}

SHAPES = {
    "breakout_base": ("🟩 長基期突破帶", "s-breakout",
                      f"基期 ≥{P['base_age_min_w']} 週 ∩ 距 ATH ≥{P['breakout_dist_ath']:.0f}% ∩ 站上 40 週線 — A1 型贏家的孵化池"),
    "cyclical_turn": ("🟧 循環轉折", "s-cyclical",
                      f"自高點 ≤{P['cyc_depth']:.0f}% ∩ 13 週 ≥+{P['cyc_turn_13w']:.0f}% ∩ 距 ATH ≤{P['cyc_dist_ath_max']:.0f}%（早段）— MU/SNDK 型出身"),
    "momentum_rerate": ("🟪 動能重估", "s-momentum",
                        f"12M RS ≥P{P['mom_rs_pct']:.0f} ∩ 站上 40 週線 ∩ 距 ATH ≥{P['mom_dist_ath']:.0f}% — PLTR/APP 型出身"),
    "theme_smallmid": ("🟦 主題下沉", "s-theme",
                       f"中型股（sp400）∩ RS ≥P{P['theme_rs_pct']:.0f} ∩ 熱產業 top{P['theme_hot_sectors']} — 大主題的中型 beta（池外稽核最大缺口）"),
}


def stage1(universe: list[dict]) -> tuple[list[dict], str]:
    import yfinance as yf
    yf_map = {r["ticker"]: r["ticker"].replace(".", "-") for r in universe}
    meta = {r["ticker"]: r for r in universe}
    rows: list[dict] = []
    as_of = None
    tickers = list(yf_map.values())
    CHUNK = 250
    for i in range(0, len(tickers), CHUNK):
        chunk = tickers[i:i + CHUNK]
        data = yf.download(chunk, period="25mo", interval="1wk",
                           progress=False, auto_adjust=True, group_by="column")
        closes = data["Close"] if "Close" in data else data
        if isinstance(closes, pd.Series):
            closes = closes.to_frame(chunk[0])
        for col in closes.columns:
            s = closes[col].dropna()
            if len(s) < 56:
                continue
            px = float(s.iloc[-1])
            ret_12m = px / float(s.iloc[-53]) * 100 - 100
            ret_13w = px / float(s.iloc[-14]) * 100 - 100
            hi_pos = int(np.argmax(s.values))
            hi = float(s.iloc[hi_pos])
            dist_ath = px / hi * 100 - 100
            base_age_w = len(s) - 1 - hi_pos
            after = s.iloc[hi_pos:]
            trough = float(after.min())
            depth = trough / hi * 100 - 100
            ma40 = float(s.iloc[-40:].mean())
            t = next((k for k, v in yf_map.items() if v == col), col)
            rows.append({
                "ticker": t, "sector": meta.get(t, {}).get("sector", ""),
                "tier": meta.get(t, {}).get("tier", ""),
                "price": round(px, 2), "ret_12m": round(ret_12m, 1),
                "ret_13w": round(ret_13w, 1), "dist_ath": round(dist_ath, 1),
                "base_age_w": int(base_age_w), "depth": round(depth, 1),
                "above_40w": px > ma40,
            })
            if as_of is None or str(s.index[-1].date()) > as_of:
                as_of = str(s.index[-1].date())
        print(f"  stage1 …{min(i + CHUNK, len(tickers))}/{len(tickers)}", file=sys.stderr)
    # RS 百分位（全樣本）
    rets = sorted(r["ret_12m"] for r in rows)
    n = len(rets)
    for r in rows:
        import bisect
        r["rs_pct"] = round(bisect.bisect_left(rets, r["ret_12m"]) / n * 100, 1)
    return rows, as_of or "—"


def tag_shapes(rows: list[dict]) -> dict[str, list[dict]]:
    # 產業熱度 = 13 週報酬中位數 top N（供主題下沉用）
    by_sector: dict[str, list[float]] = {}
    for r in rows:
        if r["sector"]:
            by_sector.setdefault(r["sector"], []).append(r["ret_13w"])
    hot = sorted(by_sector, key=lambda s: -float(np.median(by_sector[s])))[:P["theme_hot_sectors"]]

    shapes: dict[str, list[dict]] = {k: [] for k in SHAPES}
    for r in rows:
        if (r["base_age_w"] >= P["base_age_min_w"] and r["dist_ath"] >= P["breakout_dist_ath"]
                and r["above_40w"]):
            shapes["breakout_base"].append(r)
        if (r["depth"] <= P["cyc_depth"] and r["ret_13w"] >= P["cyc_turn_13w"]
                and r["dist_ath"] <= P["cyc_dist_ath_max"]):
            shapes["cyclical_turn"].append(r)
        if r["rs_pct"] >= P["mom_rs_pct"] and r["above_40w"] and r["dist_ath"] >= P["mom_dist_ath"]:
            shapes["momentum_rerate"].append(r)
        if (r["tier"] == "sp400" and r["rs_pct"] >= P["theme_rs_pct"]
                and r["above_40w"] and r["sector"] in hot):
            shapes["theme_smallmid"].append(r)
    sort_key = {"breakout_base": lambda r: -r["base_age_w"],
                "cyclical_turn": lambda r: -r["ret_13w"],
                "momentum_rerate": lambda r: -r["ret_12m"],
                "theme_smallmid": lambda r: -r["rs_pct"]}
    for k in shapes:
        shapes[k].sort(key=sort_key[k])
    return shapes, hot


def stage2_revisions(cands: list[str], prev: dict[str, dict]) -> dict[str, dict]:
    """FY+1 EPS 30 天修正%＋隱含成長率（yfinance eps_trend）；逐檔失敗 → 沿用上一版。
    g_fy1_pct = (+1y EPS / 0y EPS − 1)×100 ＝ 前瞻一年 EPS 成長（GRP 主榜的 G 閘用）。"""
    import yfinance as yf
    out: dict[str, dict] = {}
    for i, t in enumerate(cands, 1):
        try:
            tr = yf.Ticker(t.replace(".", "-")).eps_trend
            row = tr.loc["+1y"] if "+1y" in tr.index else tr.iloc[-1]
            cur, d30 = float(row["current"]), float(row["30daysAgo"])
            rev = (cur / d30 - 1) * 100 if d30 else None
            g = None
            if "0y" in tr.index and "+1y" in tr.index:
                e0, e1 = float(tr.loc["0y"]["current"]), float(tr.loc["+1y"]["current"])
                if e0 > 0:
                    g = (e1 / e0 - 1) * 100
            out[t] = {"fy1_rev_30d_pct": round(rev, 1) if rev is not None else None,
                      "g_fy1_pct": round(g, 1) if g is not None else None}
        except Exception:
            if t in prev:
                out[t] = {**prev[t], "stale": True}
        if i % 40 == 0:
            print(f"  stage2 …{i}/{len(cands)}", file=sys.stderr)
    return out


def load_pool() -> set[str]:
    pool: set[str] = {p.stem for p in WEEKLY_CACHE.glob("*.json")}
    try:
        pool |= {s["ticker"] for s in json.loads(DD_LATEST.read_text(encoding="utf-8")).get("stocks", [])}
    except (OSError, json.JSONDecodeError):
        pass
    return pool


P_LABEL_TXT = {"breakout": "🟢 突破帶", "pullback": "🟢 回踩帶", "in_trend": "🟡 趨勢內"}


def render_grp_board(payload: dict) -> str:
    board = payload.get("grp_board") or []
    if not board:
        return ""
    trs = []
    for r in board[:30]:
        pool = ('<span class="tag tag-pool">池內</span>' if r.get("in_pool")
                else '<span class="tag tag-blind">池外 → 補 DD</span>')
        trs.append(f'<tr><td class="left"><strong>{escape(r["ticker"])}</strong></td>'
                   f'<td class="left">{escape((r["sector"] or "")[:20])}</td>'
                   f'<td>{escape(r["tier"].replace("sp", "").replace("ndx", "N"))}</td>'
                   f'<td>{pct(r.get("g_fy1_pct"), 0, False)}</td>'
                   f'<td><strong>{pct(r.get("fy1_rev_30d_pct"))}</strong></td>'
                   f'<td class="left">{P_LABEL_TXT.get(r.get("p_label"), "—")}（距高 {r["dist_ath"]:+.0f}%）</td>'
                   f'<td>{pct(r["ret_12m"], 0)}</td><td>{pool}</td></tr>')
    return f"""<div class="shape-card" style="border-left-color:#b45309">
<h3>⭐ GRP 主榜 <span class="cnt">{len(board)} 檔全過三閘（顯示 top 30，按上修幅度）</span></h3>
<div class="shape-desc"><b>持有人選股準則（2026-07-04 拍板）：高成長 × EPS 上修 × 位置適合</b>——
G＝FY+1 隱含 EPS 成長 ≥15% ｜ R＝FY+1 EPS 30 天修正 &gt;0（下修否決）｜ P＝站上 40 週線＋位置標籤。
排序＝上修幅度。這是研究優先序，進場仍走 DD 裁決＋板機。</div>
<table><thead><tr><th class="left">Ticker</th><th class="left">產業</th><th>層</th>
<th>G 成長</th><th>R 30d修正</th><th class="left">P 位置</th><th>12M</th><th>DD池</th></tr></thead>
<tbody>{''.join(trs)}</tbody></table>
</div>"""


def render(payload: dict) -> str:
    shapes = payload["shapes"]
    covered = payload["coverage"]

    def row_html(r):
        rev = r.get("fy1_rev_30d_pct")
        star = " ★" if (rev is not None and rev >= P["rev_confirm_pct"]) else ""
        rev_html = pct(rev) if rev is not None else '<span class="muted">—</span>'
        pool = ('<span class="tag tag-pool">池內</span>' if r["in_pool"]
                else '<span class="tag tag-blind">池外</span>')
        return (f'<tr><td class="left"><strong>{escape(r["ticker"])}</strong>{star}</td>'
                f'<td class="left">{escape(r["sector"][:20])}</td>'
                f'<td>{escape(r["tier"].replace("sp", ""))}</td>'
                f'<td>{pct(r["ret_12m"], 0)}</td><td>{pct(r["ret_13w"], 0)}</td>'
                f'<td>{pct(r["dist_ath"], 0)}</td><td>{r["base_age_w"]}w</td>'
                f'<td>{r["rs_pct"]:.0f}</td><td>{rev_html}</td><td>{pool}</td></tr>')

    counts = payload.get("shape_counts") or {k: len(v) for k, v in shapes.items()}
    cards = []
    for key, (label, css, desc) in SHAPES.items():
        rows = shapes[key][:P["display_top_n"]]
        body = ("".join(row_html(r) for r in rows)) if rows else ""
        tbl = (f"""<table><thead><tr><th class="left">Ticker</th><th class="left">產業</th>
<th>層</th><th>12M</th><th>13W</th><th>距ATH</th><th>基期</th><th>RS</th>
<th>FY+1 30d修正</th><th>DD池</th></tr></thead><tbody>{body}</tbody></table>"""
               if rows else '<div class="empty">本週無符合形狀的名字。</div>')
        n_total = counts[key]
        n_blind = sum(1 for r in shapes[key] if not r["in_pool"])
        cards.append(f"""<div class="shape-card {css}">
<h3>{label}<span class="cnt">{n_total} 檔（顯示 top {min(n_total, P['display_top_n'])}；池外 {n_blind}）</span></h3>
<div class="shape-desc">{desc}</div>
{tbl}
</div>""")

    body = f"""<div class="hero">
<h1>📡 全市場雷達 · L0 發現層</h1>
<div class="hero-sub">S&amp;P 500＋Nasdaq 100＋S&amp;P 400 中型股（~920 檔，2026-07-04 持有人拍板排除小型股）每週全掃 — 結構訊號批量計算，四形狀路由，
候選再逐檔做 FY+1 EPS 30 天修正確認（★＝上修 ≥+{P['rev_confirm_pct']:.0f}%，拐點確認）。
<b>這是研究導航不是買入清單</b>：池外名字＝候選入池補 DD；要進場一律走 DD 裁決＋板機。</div>
<div class="asof">{payload['as_of']} 價格 as of ｜ universe {payload['universe_n']} 檔
｜ 可算 {payload['scored_n']} 檔 ｜ 修正確認覆蓋 {covered['stage2_ok']}/{covered['stage2_cand']} 檔</div>
</div>
{render_grp_board(payload)}
<div class="stat-row">
<div class="stat"><strong>{len(shapes['breakout_base'])}</strong><span>長基期突破帶</span></div>
<div class="stat"><strong>{len(shapes['cyclical_turn'])}</strong><span>循環轉折</span></div>
<div class="stat"><strong>{len(shapes['momentum_rerate'])}</strong><span>動能重估</span></div>
<div class="stat"><strong>{len(shapes['theme_smallmid'])}</strong><span>主題下沉</span></div>
<div class="stat"><strong>{payload['blind_total']}</strong><span>形狀命中·池外</span></div>
</div>
{''.join(cards)}
<div class="note">熱產業（13 週報酬中位數 top {P['theme_hot_sectors']}）：{escape('、'.join(payload['hot_sectors']))}。
形狀門檻 v1 於 2026-07-04 鎖定（PREREG 慣例，季檢才可調）；四形狀出身依據＝12M/24M 發現力驗屍
＋池外贏家稽核（top50 有 54% 在池外、集中於主題中小型）。一檔可同時命中多形狀。</div>"""
    return page_shell("全市場雷達 · 決策引擎", "/engine/radar.html", body,
                      "S&P 1500 全市場結構掃描 × 四形狀路由 × EPS 修正拐點確認")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-stage2", action="store_true")
    args = ap.parse_args()

    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))["tickers"]
    rows, as_of = stage1(universe)
    shapes, hot = tag_shapes(rows)

    # GRP 主榜的結構資格（P 閘，週線版）：站上 40 週線；位置標籤同 grp.py 語意
    def p_label(r):
        if not r["above_40w"]:
            return None
        if r["dist_ath"] >= -5.0:
            return "breakout"
        if -25.0 <= r["dist_ath"] <= -8.0:
            return "pullback"
        return "in_trend"
    grp_struct = [r for r in rows if p_label(r)]
    grp_struct.sort(key=lambda r: -r["rs_pct"])

    # stage2 候選 = 各形狀 top N 聯集 ∪ GRP 結構資格 RS top 200
    cands: list[str] = []
    for k in SHAPES:
        cands.extend(r["ticker"] for r in shapes[k][:P["stage2_top_n"]])
    cands.extend(r["ticker"] for r in grp_struct[:200])
    cands = list(dict.fromkeys(cands))
    prev: dict[str, dict] = {}
    if RADAR_JSON.exists():
        try:
            old = json.loads(RADAR_JSON.read_text(encoding="utf-8"))
            prev = old.get("stage2") or {}
        except (OSError, json.JSONDecodeError):
            pass
    revs = {} if args.skip_stage2 else stage2_revisions(cands, prev)

    # ── GRP 主榜（高成長 × 上修 × 位置；G 用 FY+1 隱含成長，R 用 30 天修正）──
    grp_board = []
    for r in grp_struct:
        s2 = revs.get(r["ticker"]) or {}
        g, rev = s2.get("g_fy1_pct"), s2.get("fy1_rev_30d_pct")
        if g is None or rev is None:
            continue
        if g >= 15.0 and rev > 0 and rev > -2.0:
            grp_board.append({**r, **s2, "p_label": p_label(r)})
    grp_board.sort(key=lambda r: -(r["fy1_rev_30d_pct"] or 0))

    pool = load_pool()
    shape_counts = {k: len(v) for k, v in shapes.items()}   # 截斷前的真實命中數
    for k in shapes:
        for r in shapes[k]:
            r["in_pool"] = r["ticker"] in pool
            r.update(revs.get(r["ticker"], {}))
        shapes[k] = shapes[k][:P["display_top_n"] * 2]   # JSON 留 2 倍餘裕

    for r in grp_board:
        r["in_pool"] = r["ticker"] in pool
    blind_total = len({r["ticker"] for lst in shapes.values() for r in lst if not r["in_pool"]})
    payload = {
        "schema_version": "1.1",
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": as_of, "universe_n": len(universe), "scored_n": len(rows),
        "params": P, "hot_sectors": hot, "shape_counts": shape_counts,
        "coverage": {"stage2_cand": len(cands),
                     "stage2_ok": sum(1 for t in cands if t in revs and revs[t].get("fy1_rev_30d_pct") is not None)},
        "blind_total": blind_total,
        "grp_board": grp_board[:40],
        "stage2": revs,
        "shapes": shapes,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RADAR_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    RADAR_HTML.write_text(render(payload), encoding="utf-8")
    print(f"radar: as_of={as_of} 可算={len(rows)} 形狀命中={shape_counts} 池外={blind_total} "
          f"stage2={payload['coverage']['stage2_ok']}/{len(cands)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
