#!/usr/bin/env python3
"""決策引擎 L2 — 一頁決策卡（渲染 + claim 結算）.

卡片真相 = docs/engine/cards/data/{TICKER}.json（card-v1 schema，由分析 session 從
v13/v14 DD 的 §13/§14 抽取——只抽已寫內容，不發明）。本 script 做兩件事：
  1. claim 結算：check=auto_price 的宣稱用 weekly_cache 最新收盤自動判 ✅/❌；
     manual 的看 deadline——過期未結算標「⏰ 到期待結算」（人工回填 status 欄）。
  2. 渲染 docs/engine/cards.html（卡片牆）＋ cards.json（聚合）。

卡片維護：DD 複審後跑對應分析 session 重抽該卡；卡片與 DD 版本綁定（source_dd）。
Usage: python3 scripts/engine/build_cards.py
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.common import OUT_DIR, ROOT, page_shell, pct  # noqa: E402
from engine.build_scoreboard import _bars  # noqa: E402
from engine.grp import G_MIN_CAGR, P_LABEL_HTML, R_VETO_FY1, grp_route, grp_score  # noqa: E402

DD_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"

CARDS_DIR = OUT_DIR / "cards" / "data"
CARDS_HTML = OUT_DIR / "cards.html"
CARDS_JSON = OUT_DIR / "cards.json"

TODAY = date.today().isoformat()


def settle_claim(c: dict, ticker: str) -> dict:
    """回傳 claim + 結算狀態。status: pass|breach|watch|due|manual_done"""
    out = dict(c)
    if c.get("status") in ("pass", "breach"):     # 人工已回填
        out["settle"] = "manual_done"
        return out
    if c.get("check") == "auto_price":
        # 防衛：auto_price 只准結算「價格」宣稱（unit=USD/元）——P/E、比率類一律降級人工，
        # 否則會拿股價去比倍數門檻產生假觸發（2026-07-04 MA/GOOGL Fwd PE 案例）
        if (c.get("unit") or "").upper() not in ("USD", "$", "元", "TWD"):
            out["settle"] = "due" if (c.get("deadline") or "9999") < TODAY else "watch"
            out["auto_downgraded"] = True
            return out
        bars = _bars(ticker)
        if bars:
            px = bars[-1][1]
            th = c.get("threshold")
            comp = c.get("comparator", "<=")
            breached = {"<=": px <= th, "<": px < th, ">=": px >= th, ">": px > th}.get(comp)
            out["last_price"] = round(px, 2)
            out["settle"] = "breach" if breached else "watch"
            return out
    out["settle"] = "due" if (c.get("deadline") or "9999") < TODAY else "watch"
    return out


def grp_guard(ticker: str, latest_map: dict) -> dict | None:
    """GRP 守門 — 席位存在理由的即時三閘（與擂台同一份活數據，週更自動結算）。"""
    s = latest_map.get(ticker)
    if not s:
        return None
    g = grp_score(s)
    route, route_why = grp_route(s)
    return {"grp": g, "route": route, "route_why": route_why}


def load_cards() -> list[dict]:
    try:
        latest_map = {s["ticker"]: s
                      for s in json.loads(DD_LATEST.read_text(encoding="utf-8"))["stocks"]}
    except (OSError, json.JSONDecodeError, KeyError):
        latest_map = {}
    cards = []
    for p in sorted(CARDS_DIR.glob("*.json")):
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"⚠ {p.name} JSON 壞：{e}", file=sys.stderr)
            continue
        if c.get("schema") != "card-v1":
            print(f"⚠ {p.name} 非 card-v1，跳過", file=sys.stderr)
            continue
        c["claims"] = [settle_claim(cl, c["ticker"]) for cl in (c.get("claims") or [])]
        bars = _bars(c["ticker"])
        if bars and c.get("price_at_dd"):
            c["ret_since_dd_pct"] = round(bars[-1][1] / c["price_at_dd"] * 100 - 100, 1)
        c["guard"] = grp_guard(c["ticker"], latest_map)
        cards.append(c)
    return cards


BADGE = {"watch": ('<span class="tag tag-pool">監測中</span>'),
         "breach": ('<span class="tag tag-dn">❌ 觸發</span>'),
         "due": ('<span class="tag tag-blind">⏰ 到期待結算</span>'),
         "manual_done": ('<span class="tag tag-up">已結算</span>')}


def render_card(c: dict) -> str:
    thesis = "".join(f"<li>{escape(t)}</li>" for t in (c.get("thesis") or [])[:5])
    claims = ""
    for cl in c["claims"]:
        dl = cl.get("deadline") or "—"
        dls = "（推定）" if cl.get("deadline_source") == "inferred" else ""
        claims += (f'<tr><td class="left">{escape(cl.get("claim") or "")}</td>'
                   f'<td>{escape(str(cl.get("metric") or ""))} {escape(cl.get("comparator") or "")} '
                   f'{cl.get("threshold")}</td>'
                   f'<td>{escape(dl)}{dls}</td>'
                   f'<td class="left">{escape(cl.get("action_on_fail") or "")}</td>'
                   f'<td>{BADGE.get(cl["settle"], cl["settle"])}</td></tr>')
    pm = "".join(f'<li><b>{escape(p.get("scenario") or "")}</b>：{escape(p.get("trigger") or "")}'
                 f'（{escape(p.get("impact") or "")}）</li>' for p in (c.get("premortem") or [])[:3])
    rg = c.get("range") or {}
    ret = c.get("ret_since_dd_pct")
    n_breach = sum(1 for cl in c["claims"] if cl["settle"] == "breach")
    n_due = sum(1 for cl in c["claims"] if cl["settle"] == "due")

    # ── GRP 守門（席位存在理由的即時三閘；週更自動結算，與擂台同數據）──
    guard_html = ""
    grp_fail = False
    gd = c.get("guard")
    if gd:
        g = gd["grp"]
        grp_fail = not g["pass"]
        g_ok = g["g"] is not None and g["g"] >= G_MIN_CAGR
        r_val = g["r_fy1"] if g["r_fy1"] is not None else g["r_2y"]
        r_ok = (not g["veto"]) and ((g["r_fy1"] or 0) > 0 or (g["r_2y"] or 0) > 0)
        p_ok = g["p_label"] is not None
        def cell(ok, veto=False):
            if veto:
                return '<span class="tag tag-dn">⛔ 下修否決</span>'
            return '<span class="tag tag-up">✅</span>' if ok else '<span class="tag tag-dn">❌</span>'
        dist = f'（距高 {g["dist_hi"]:+.0f}%）' if g["dist_hi"] is not None else ""
        guard_html = f"""<table style="margin-bottom:8px"><thead><tr>
<th class="left">GRP 守門（席位存在理由 · 週更自動）</th><th>現值</th><th>門檻</th><th>狀態</th><th class="left">破閘動作</th></tr></thead><tbody>
<tr><td class="left">G 高成長（FY1→FY3 CAGR）</td><td>{pct(g["g"], 1, False) if g["g"] is not None else "—"}</td>
<td>≥{G_MIN_CAGR:.0f}%</td><td>{cell(g_ok)}</td><td class="left">跌破 → 複審</td></tr>
<tr><td class="left">R 上修（FY+1 月修／2Y pp）</td>
<td>{pct(g["r_fy1"]) if g["r_fy1"] is not None else "—"}／{f'{g["r_2y"]:+.1f}pp' if g["r_2y"] is not None else "—"}</td>
<td>&gt;0（≤{R_VETO_FY1:.0f}% 否決）</td><td>{cell(r_ok, g["veto"])}</td><td class="left">下修 → 減碼複審</td></tr>
<tr><td class="left">P 位置（52 週線＋位置帶）</td>
<td class="left">{P_LABEL_HTML.get(g["p_label"])}{dist}</td>
<td>站上 52 週線</td><td>{cell(p_ok)}</td><td class="left">破線 → 複審</td></tr>
</tbody></table>"""
        _ = r_val

    alert = ""
    if grp_fail:
        alert = '<span class="tag tag-dn">⛔ GRP 落席</span>'
    elif n_breach:
        alert = f'<span class="tag tag-dn">❌ {n_breach} 條觸發</span>'
    elif n_due:
        alert = f'<span class="tag tag-blind">⏰ {n_due} 條到期</span>'
    seat_badge = {"core": '<span class="tag tag-up">🎯 核心席</span>',
                  "sat": '<span class="tag tag-pool">🛰 衛星席</span>'}.get(
        c.get("_seat"), '<span class="tag tag-blind">板凳</span>')
    return f"""<div class="block" id="{escape(c["ticker"])}">
<h2>{escape(c["ticker"])}　{seat_badge}　<span style="font-size:13px;font-weight:600;color:#64748b">{escape(c.get("verdict") or "")}
· {escape(c.get("role") or "")}</span>　{alert}</h2>
<div class="block-sub">DD {escape(c.get("dd_date") or "")}（<a href="{escape(c.get("source_dd") or "#")}#decision">原報告</a>）
· 裁決價 ${c.get("price_at_dd")} · 至今 {pct(ret) if ret is not None else "—"}</div>
{guard_html}
<ul style="margin:6px 0 10px 18px;font-size:13px">{thesis}</ul>
<table><thead><tr><th class="left">DD 深層證偽宣稱（財報期人工結算）</th><th>門檻</th><th>期限</th>
<th class="left">觸發動作</th><th>狀態</th></tr></thead><tbody>{claims}</tbody></table>
<div style="margin-top:8px;font-size:12.5px;color:#64748b"><b>Pre-mortem</b>
<ul style="margin:2px 0 6px 18px">{pm}</ul>
<b>進場節奏</b>　{escape(c.get("entry_plan") or "—")}
<span class="muted">｜DD 內部參考：5Y EV {rg.get("ev_pct") if rg.get("ev_pct") is not None else "—"}%
／IRR {rg.get("irr_base_pct") if rg.get("irr_base_pct") is not None else "—"}%
／Max DD {rg.get("max_dd_pct") if rg.get("max_dd_pct") is not None else "—"}%</span></div>
</div>"""


def main() -> int:
    cards = load_cards()
    if not cards:
        print("⚠ 無卡片（docs/engine/cards/data/ 空）— 不寫頁面")
        return 0
    # 席位分區（讀 arena.json；無檔則不分區）
    seated: dict[str, str] = {}
    try:
        a = json.loads((OUT_DIR / "arena.json").read_text(encoding="utf-8"))
        for r in a.get("core_seats", []):
            seated[r["ticker"]] = "core"
        for r in a.get("sat_seats", []):
            seated[r["ticker"]] = "sat"
    except (OSError, json.JSONDecodeError):
        pass
    for c in cards:
        c["_seat"] = seated.get(c["ticker"])
    cards.sort(key=lambda c: ({"core": 0, "sat": 1}.get(c["_seat"], 2), c["ticker"]))
    n_claims = sum(len(c["claims"]) for c in cards)
    n_breach = sum(1 for c in cards for cl in c["claims"] if cl["settle"] == "breach")
    n_due = sum(1 for c in cards for cl in c["claims"] if cl["settle"] == "due")

    body = f"""<div class="hero">
<h1>🗂 決策卡 · L2 判斷層</h1>
<div class="hero-sub">一席一卡，兩層守門：<b>上層＝GRP 守門</b>——讓這檔坐上席位的三個理由
（G 高成長／R 上修／P 位置）用活數據<b>每週自動結算</b>，任一破閘卡片自己亮 ⛔；
<b>下層＝DD 深層證偽</b>——從報告 §13/§14 抽的基本面宣稱（帶數字帶期限，財報期人工結算）。
5Y EV/IRR 降為 DD 內部參考附註。<b>宣稱沒有到期日就不是宣稱</b>。</div>
<div class="asof">{len(cards)} 張卡 ｜ {n_claims} 條宣稱（❌ 觸發 {n_breach} · ⏰ 到期 {n_due}）｜ 週更結算</div>
</div>
{''.join(render_card(c) for c in cards)}
<div class="note">卡片維護協議：新席位入場 → 抽卡；DD 複審 → 重抽；宣稱觸發（❌）→ 按 action_on_fail
處理並在卡片 JSON 回填 status；到期（⏰）→ 人工結算 pass/breach。卡片真相在
<code>docs/engine/cards/data/*.json</code>，本頁只渲染。</div>"""

    CARDS_JSON.write_text(json.dumps({
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_cards": len(cards), "n_claims": n_claims,
        "n_breach": n_breach, "n_due": n_due,
        "tickers": [c["ticker"] for c in cards],
        # 卡餵擂台：每檔的宣稱狀態摘要（arena 席位表消費）
        "by_ticker": {c["ticker"]: {
            "n_claims": len(c["claims"]),
            "n_breach": sum(1 for cl in c["claims"] if cl["settle"] == "breach"),
            "n_due": sum(1 for cl in c["claims"] if cl["settle"] == "due"),
            "next_deadline": min((cl.get("deadline") or "9999" for cl in c["claims"]
                                  if cl["settle"] in ("watch", "due")), default=None),
        } for c in cards},
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    CARDS_HTML.write_text(
        page_shell("決策卡 · 決策引擎", "/engine/cards.html", body,
                   "一頁決策卡 — 可證偽宣稱與自動結算"),
        encoding="utf-8")
    print(f"cards: {len(cards)} 張 {n_claims} 條宣稱（觸發 {n_breach}／到期 {n_due}）"
          f" {[c['ticker'] for c in cards]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
