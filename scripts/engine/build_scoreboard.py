#!/usr/bin/env python3
"""決策引擎 L4 — 形狀別記分板（裁決結算公開版）.

每筆 DD 裁決（dd-meta，公開資料）× weekly_cache 週線 → forward return 結算，
並按「裁決當下的價格形狀」分桶——回答「哪種形狀我判得準、哪種形狀我系統性錯過」。

形狀分類（裁決日當下、只用價格結構 — 與雷達同鏡頭、可歷史重算）：
  breakout_base：距 2 年 ATH ≥ -5% 且基期 ≥26 週
  cyclical_turn：自 2 年高點深跌 ≤ -40% 後 13 週 ≥ +10%
  momentum_rerate：12M 報酬 ≥ +60%（單檔絕對門檻替代全市場 RS——歷史時點無全市場截面）
  other：其餘

資料源：knowledge/decisions.jsonl（由公開 dd-meta 重算的衍生物；缺檔自動 rebuild）。
輸出：docs/engine/scoreboard.json + scoreboard.html（成功才寫檔）。
Usage: python3 scripts/engine/build_scoreboard.py
"""
from __future__ import annotations

import json
import statistics
import subprocess
import sys
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.common import OUT_DIR, ROOT, page_shell, pct  # noqa: E402

DECISIONS = ROOT / "knowledge" / "decisions.jsonl"
BUILD_KNOWLEDGE = ROOT / "knowledge" / "build_knowledge.py"
WEEKLY_CACHE = ROOT / "data" / "weekly_cache"
SB_JSON = OUT_DIR / "scoreboard.json"
SB_HTML = OUT_DIR / "scoreboard.html"

MIN_AGE_DAYS = 28          # 聚合最低結算齡（同 knowledge/ 口徑）
GATE_CHANGES = [           # 記分板分段線（PREREG：gate 變更日，歷史不重算）
    {"date": "2026-07-03", "label": "C 冷卻再武裝上線（態②否決由終局改延遲）"},
    {"date": "2026-07-04", "label": "觀望複審隊列上線（錯過成本/上修觸發回爐）"},
    {"date": "2026-07-04", "label": "GRP 選股準則上線（高成長×上修×位置取代 EV5y×確定性排序；"
                                    "軌別＝moat 路由）——GRP 記分維度自本日起累積，歷史裁決不補算"},
]

SHAPE_LABELS = {
    "breakout_base": "🟩 長基期突破帶",
    "cyclical_turn": "🟧 循環轉折",
    "momentum_rerate": "🟪 動能重估",
    "other": "⬜ 其他",
}


def _bars(t, _c={}):
    if t not in _c:
        p = WEEKLY_CACHE / f"{t}.json"
        if p.exists():
            try:
                raw = json.loads(p.read_text(encoding="utf-8")).get("weekly_bars") or []
                _c[t] = [(b["week_end"], b["close"]) for b in raw if b.get("close")]
            except (json.JSONDecodeError, KeyError):
                _c[t] = None
        else:
            _c[t] = None
    return _c[t]


def classify_shape(bars, d0: str) -> str:
    """裁決日當下的價格形狀（只用 ≤ d0 的 104 根週線，無 look-ahead）。"""
    hist = [(d, c) for d, c in bars if d <= d0][-104:]
    if len(hist) < 56:
        return "other"
    closes = [c for _, c in hist]
    px = closes[-1]
    hi_pos = max(range(len(closes)), key=lambda i: closes[i])
    hi = closes[hi_pos]
    dist_ath = px / hi * 100 - 100
    base_age_w = len(closes) - 1 - hi_pos
    trough = min(closes[hi_pos:])
    depth = trough / hi * 100 - 100
    ret_13w = px / closes[-14] * 100 - 100 if len(closes) >= 14 else 0.0
    ret_12m = px / closes[-53] * 100 - 100 if len(closes) >= 53 else 0.0
    if dist_ath >= -5 and base_age_w >= 26:
        return "breakout_base"
    if depth <= -40 and ret_13w >= 10:
        return "cyclical_turn"
    if ret_12m >= 60:
        return "momentum_rerate"
    return "other"


def settle(decisions: list[dict]) -> list[dict]:
    rows = []
    for r in decisions:
        if r.get("kind") != "decision" or r.get("entity_type") != "company":
            continue
        t, d0 = r.get("entity"), r.get("date")
        bars = _bars(t) if (t and d0) else None
        if not bars:
            continue
        p0 = None
        for d, c in bars:
            if d <= d0:
                p0 = c
            else:
                break
        after = [(d, c) for d, c in bars if d > d0]
        if not (p0 and after):
            continue
        last_d, p1 = after[-1]
        y0, m0, dd0 = map(int, d0.split("-"))
        y1, m1, dd1 = map(int, last_d.split("-"))
        rows.append({
            "ticker": t, "date": d0,
            "verdict": r.get("verdict"), "grade": r.get("fundamental_grade"),
            "shape": classify_shape(bars, d0),
            "to_date_pct": round(p1 / p0 * 100 - 100, 1),
            "days": (date(y1, m1, dd1) - date(y0, m0, dd0)).days,
        })
    return rows


def agg(rows: list[dict]) -> dict:
    if not rows:
        return {"n": 0}
    rets = [r["to_date_pct"] for r in rows]
    return {"n": len(rows),
            "median": round(statistics.median(rets), 1),
            "mean": round(statistics.mean(rets), 1),
            "loss_rate": round(sum(1 for x in rets if x < 0) / len(rets) * 100),
            "thin": len(rows) < 20}


def render(payload: dict) -> str:
    def table(title, sub, buckets, order):
        trs = []
        for label in order:
            a = buckets.get(label)
            if not a or a["n"] == 0:
                continue
            thin = ' <span class="muted">（樣本未熟）</span>' if a.get("thin") else ""
            trs.append(f'<tr><td class="left">{label}{thin}</td><td>{a["n"]}</td>'
                       f'<td>{pct(a["median"])}</td><td>{pct(a["mean"])}</td>'
                       f'<td>{a["loss_rate"]}%</td></tr>')
        return f"""<div class="block"><h2>{title}</h2><div class="block-sub">{sub}</div>
<table><thead><tr><th class="left">分桶</th><th>n</th><th>中位報酬</th><th>平均</th>
<th>虧損比例</th></tr></thead><tbody>{''.join(trs)}</tbody></table></div>"""

    by_shape = payload["by_shape"]
    by_verdict = payload["by_verdict"]
    by_shape_verdict = payload["by_shape_verdict"]

    sv_trs = []
    for sk, label in SHAPE_LABELS.items():
        for v in ("進場", "觀望", "迴避", "（無裁決）"):
            a = by_shape_verdict.get(f"{sk}|{v}")
            if not a or a["n"] < 3:
                continue
            sv_trs.append(f'<tr><td class="left">{label}</td><td class="left">{v}</td>'
                          f'<td>{a["n"]}</td><td>{pct(a["median"])}</td>'
                          f'<td>{a["loss_rate"]}%</td></tr>')
    sv_html = (f"""<div class="block"><h2>形狀 × 裁決 交叉</h2>
<div class="block-sub">「哪種形狀我說觀望之後漲最多」— 校準的最小單位（n&lt;3 不顯示）。</div>
<table><thead><tr><th class="left">形狀</th><th class="left">裁決</th><th>n</th>
<th>中位報酬</th><th>虧損比例</th></tr></thead><tbody>{''.join(sv_trs)}</tbody></table></div>"""
               if sv_trs else "")

    gates = "".join(f'<li><b>{g["date"]}</b>　{escape(g["label"])}</li>' for g in GATE_CHANGES)
    body = f"""<div class="hero">
<h1>形狀記分板 · L4 結算層</h1>
<div class="hero-sub">每筆 DD 裁決 × 週線自動結算（裁決日 → 最新價），按「裁決當下的價格形狀」分桶。
回答一個問題：<b>哪種形狀我判得準、哪種形狀我系統性錯過</b>。判斷函數的季度校準以此為據。</div>
<div class="asof">價格 as of {payload['as_of']} ｜ 結算 {payload['n_settled']} 筆
（聚合取結算齡 ≥{MIN_AGE_DAYS} 天者 {payload['n_aged']} 筆）｜ 各筆視窗不等長：方向可信、量級慎讀</div>
</div>
{table("依形狀", "裁決當下的價格結構分桶（無 look-ahead：只用裁決日前 104 週線）。",
       by_shape, list(SHAPE_LABELS.values()))}
{table("依裁決", "觀望/迴避的正報酬＝錯過成本——與套牢同權重對答案。裁決欄 2026-06（v13）起才有。",
       by_verdict, ["進場", "觀望", "迴避", "（無裁決）"])}
{sv_html}
<div class="note"><b>Gate 變更分段線</b>（append-only，歷史不重算）：<ul style="margin:4px 0 0 18px">{gates}</ul></div>
<div class="note warn">誠實邊界：決策史自 2026-03 起（~4 個月）、單一多頭 regime、樣本仍薄——
本頁的用途是「讓校準有地方看」，不是「已可下結論」。第一批裁決滿 91 天約在 2026-09 底。</div>"""
    return page_shell("形狀記分板 · 決策引擎", "/engine/scoreboard.html", body,
                      "DD 裁決 × 價格形狀的自動結算記分板 — 判斷函數的校準依據")


def main() -> int:
    if not DECISIONS.exists():
        subprocess.run([sys.executable, str(BUILD_KNOWLEDGE)], check=True)
    decisions = [json.loads(l) for l in DECISIONS.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = settle(decisions)
    aged = [r for r in rows if r["days"] >= MIN_AGE_DAYS]

    shape_key = {v: k for k, v in SHAPE_LABELS.items()}
    by_shape = {SHAPE_LABELS[k]: agg([r for r in aged if r["shape"] == k]) for k in SHAPE_LABELS}
    by_verdict = {v: agg([r for r in aged if (r["verdict"] or "（無裁決）") == v])
                  for v in ("進場", "觀望", "迴避", "（無裁決）")}
    by_shape_verdict = {f"{k}|{v}": agg([r for r in aged if r["shape"] == k
                                         and (r["verdict"] or "（無裁決）") == v])
                        for k in SHAPE_LABELS for v in ("進場", "觀望", "迴避", "（無裁決）")}

    payload = {
        "schema_version": "1.0",
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": max((max(d for d, _ in _bars(r["ticker"]) or [("—", 0)]) for r in rows), default="—"),
        "n_settled": len(rows), "n_aged": len(aged),
        "min_age_days": MIN_AGE_DAYS, "gate_changes": GATE_CHANGES,
        "by_shape": by_shape, "by_verdict": by_verdict,
        "by_shape_verdict": by_shape_verdict,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SB_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    SB_HTML.write_text(render(payload), encoding="utf-8")
    print(f"scoreboard: 結算 {len(rows)} 筆（齡≥{MIN_AGE_DAYS}d {len(aged)}）"
          f" 形狀分布={ {k: v['n'] for k, v in by_shape.items()} }")
    _ = shape_key
    return 0


if __name__ == "__main__":
    sys.exit(main())
