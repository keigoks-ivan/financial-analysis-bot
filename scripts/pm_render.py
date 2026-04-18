#!/usr/bin/env python3
"""
pm_render.py — PM 決策 JSON → HTML 儀表 + research 首頁 markers

PM 的核心價值是判斷（Opus 的工作），不是 HTML 排版（Python 的工作）。
Opus 吐 /tmp/pm_decisions.json，這個腳本讀它然後：
  1. 產 docs/pm/PM_YYYYMMDD.html（固定 template，儀表風格）
  2. 追加一行到 docs/pm/INDEX.md
  3. 替換 docs/research/index.html 的 PM_HOLDINGS / PM_ACTIONS markers

用法：
  python3 scripts/pm_render.py /tmp/pm_decisions.json

JSON 輸入 schema（Opus 要產出的）：
{
  "report_date": "YYYY-MM-DD",
  "mode": "proposal" | "review",
  "spx_regime": "normal" | "below_w104",
  "core": [
    {"ticker": "NVDA", "target_pct": 15, "signal": "A+", "price": 200.94,
     "dd_path": "/dd/DD_NVDA_20260416.html", "reason": "AI infra leader"}
  ],
  "satellite": [...],
  "cash_pct": 10,
  "actions": [
    {"type": "buy"|"sell"|"trim"|"hold"|"new_entry",
     "ticker": "NVDA", "from_pct": 0, "to_pct": 15, "reason": "first entry, A+ signal"}
  ],
  "risks": ["首次提案，待建立 current_holdings.yaml", "Sector concentration tech 80%"],
  "overrides": [{"level": "L1|L2|L3", "ticker": "X", "reason": "...", "reversal": "..."}]
}
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def render_holding_row(r, tier):
    dd = f'<a href="{r["dd_path"]}">→</a>' if r.get("dd_path") else "—"
    price = f'${r["price"]:.2f}' if r.get("price") else "—"
    return (
        f'<tr><td>{tier}</td><td>{r["ticker"]}</td>'
        f'<td>{r["target_pct"]}%</td><td>{r["signal"]}</td>'
        f'<td>{price}</td><td>{dd}</td></tr>'
    )


def render_action(a):
    type_map = {
        "buy": ('<span style="color:#166534;font-weight:500">加碼</span>', "→"),
        "sell": ('<span style="color:#991B1B;font-weight:500">賣出</span>', "→"),
        "trim": ('<span style="color:#9A3412;font-weight:500">減碼</span>', "→"),
        "hold": ('<span style="color:#64748b">維持</span>', "·"),
        "new_entry": ('<span style="color:#92400E;font-weight:500">新進</span>', "→"),
    }
    label, arrow = type_map.get(a["type"], ("—", "·"))
    size = f'{a.get("from_pct", 0)}% {arrow} {a.get("to_pct", 0)}%' if a["type"] != "hold" else f'{a.get("to_pct", 0)}%'
    return f'<li>{label} <strong>{a["ticker"]}</strong> {size} <span style="color:#64748b">· {a.get("reason","")}</span></li>'


def render_risk(r):
    return f"• {r}"


def render_html(d):
    date = d["report_date"]
    mode_label = {"proposal": "新組合提案", "review": "標準複盤"}.get(d.get("mode", "review"), "複盤")
    spx = d.get("spx_regime", "normal")
    spx_label = "破 W104 ⚠️" if spx == "below_w104" else "正常"
    fetched = d.get("fetched_at", "")

    rows = [render_holding_row(r, "Core") for r in d.get("core", [])]
    rows += [render_holding_row(r, "Satellite") for r in d.get("satellite", [])]
    cash_pct = d.get("cash_pct", 10)
    rows.append(f'<tr><td>現金</td><td>—</td><td>{cash_pct}%</td><td>—</td><td>—</td><td>—</td></tr>')
    rows_html = "\n".join(rows)

    actions_html = "\n".join(render_action(a) for a in d.get("actions", []))
    if not actions_html:
        actions_html = '<li style="color:#64748b">維持現有配置，無需調整</li>'

    risks_html = "<br>".join(render_risk(r) for r in d.get("risks", []))
    if not risks_html:
        risks_html = "• 無特別風險警示"

    rationale_html = ""
    if d.get("selection_rationale"):
        sr = d["selection_rationale"]
        bullets = []
        if sr.get("inclusion_criteria"):
            bullets.append(f'<li><strong>篩選標準：</strong>{sr["inclusion_criteria"]}</li>')
        if sr.get("universe_size"):
            bullets.append(f'<li><strong>候選池：</strong>{sr["universe_size"]}</li>')
        if sr.get("why_these"):
            bullets.append(f'<li><strong>為何選這幾檔：</strong>{sr["why_these"]}</li>')
        if sr.get("why_reject"):
            bullets.append(f'<li><strong>主要排除原因：</strong>{sr["why_reject"]}</li>')
        if sr.get("sizing_logic"):
            bullets.append(f'<li><strong>權重邏輯：</strong>{sr["sizing_logic"]}</li>')
        rationale_html = f'<h2>§4 選擇邏輯</h2><ul>{"".join(bullets)}</ul>'

    overrides_html = ""
    if d.get("overrides"):
        items = [f'<li><strong>{o["level"]}</strong> {o["ticker"]}: {o["reason"]} (解除條件：{o.get("reversal","—")})</li>' for o in d["overrides"]]
        overrides_html = f'<h2>§5 Override 清單</h2><ul>{"".join(items)}</ul>'

    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8"><title>PM 儀表 {date}</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Noto Sans TC',sans-serif;background:#F8FAFC;padding:20px;max-width:900px;margin:0 auto;color:#0F172A;font-size:14px;line-height:1.5}}
h1{{color:#1E3A5F;border-bottom:3px solid #3B82F6;padding-bottom:8px;font-size:22px;margin:0 0 8px}}
h2{{color:#1E3A5F;margin:20px 0 8px;font-size:16px}}
table{{width:100%;border-collapse:collapse;margin:8px 0;font-size:13px;background:#fff}}
th{{background:#1E3A5F;color:#fff;padding:6px 8px;text-align:left}}
td{{padding:6px 8px;border-bottom:1px solid #E2E8F0}}
.muted{{color:#64748b;font-size:12px}}
ul,ol{{padding-left:22px;margin:8px 0}}
li{{margin:3px 0}}
a{{color:#1E3A5F}}
</style></head><body>
<h1>🏛 PM 儀表 — {date}</h1>
<p class="muted">模式：{mode_label} · SPX：{spx_label} · 數據鮮度：{fetched}</p>
<h2>§1 配置</h2>
<table><tr><th>Tier</th><th>Ticker</th><th>目標%</th><th>訊號</th><th>現價</th><th>DD</th></tr>
{rows_html}
</table>
<h2>§2 本週動作</h2>
<ul>{actions_html}</ul>
<h2>§3 風險備註</h2>
<p class="muted">{risks_html}</p>
{rationale_html}
{overrides_html}
<p class="muted" style="margin-top:20px">PM Skill v1.0 · <a href="/research/">回研究首頁</a></p>
</body></html>
"""


def render_holdings_marker(d):
    date = d["report_date"]
    fname = f"PM_{date.replace('-','')}.html"
    core = d.get("core", [])
    sat = d.get("satellite", [])
    cash_pct = d.get("cash_pct", 10)

    lines = [
        f'          <div style="font-size:12px;color:#64748b;margin-bottom:6px">提案日：{date} · <a href="/pm/{fname}">詳細→</a></div>',
        '          <ul style="padding-left:18px;margin:4px 0;list-style:none;font-size:13px">',
        f'            <li style="font-weight:600">核心 ({len(core)}/5)</li>',
    ]
    for r in core:
        lines.append(f'            <li>{r["ticker"]} {r["target_pct"]}% · {r["signal"]}</li>')
    lines.append(f'            <li style="font-weight:600;margin-top:6px">衛星 ({len(sat)}/3)</li>')
    for r in sat:
        lines.append(f'            <li>{r["ticker"]} {r["target_pct"]}% · {r["signal"]}</li>')
    lines.append('            <li style="font-weight:600;margin-top:6px">現金</li>')
    lines.append(f'            <li>{cash_pct}%</li>')
    lines.append('          </ul>')
    return "\n".join(lines)


def render_actions_marker(d):
    actions = d.get("actions", [])
    if not actions:
        return '          <ol style="padding-left:20px;margin:4px 0;font-size:13px">\n            <li class="wr-empty">維持現有配置，無需調整</li>\n          </ol>'
    lines = ['          <ol style="padding-left:20px;margin:4px 0;font-size:13px">']
    type_emoji = {"buy": "加", "sell": "賣", "trim": "減", "hold": "維持", "new_entry": "新進"}
    for a in actions[:6]:
        emoji = type_emoji.get(a["type"], "·")
        to_pct = a.get("to_pct", 0)
        lines.append(f'            <li>{emoji} {a["ticker"]} → {to_pct}% <span style="color:#64748b">· {a.get("reason","")}</span></li>')
    lines.append('          </ol>')
    return "\n".join(lines)


def update_research_page(d):
    path = REPO / "docs" / "research" / "index.html"
    text = path.read_text()
    holdings_new = render_holdings_marker(d)
    actions_new = render_actions_marker(d)

    text = re.sub(
        r"<!-- PM_HOLDINGS_START -->.*?<!-- PM_HOLDINGS_END -->",
        f"<!-- PM_HOLDINGS_START -->\n{holdings_new}\n<!-- PM_HOLDINGS_END -->",
        text, flags=re.DOTALL,
    )
    text = re.sub(
        r"<!-- PM_ACTIONS_START -->.*?<!-- PM_ACTIONS_END -->",
        f"<!-- PM_ACTIONS_START -->\n{actions_new}\n<!-- PM_ACTIONS_END -->",
        text, flags=re.DOTALL,
    )
    path.write_text(text)


def append_index(d):
    date = d["report_date"]
    fname = f"PM_{date.replace('-','')}.html"
    mode = d.get("mode", "review")
    core_n = len(d.get("core", []))
    sat_n = len(d.get("satellite", []))
    note = d.get("summary", "新組合提案" if mode == "proposal" else "標準複盤")

    line = f"| {date} | {mode} | {core_n}核心 | {sat_n}衛星 | {fname} | {note} |\n"
    (REPO / "docs" / "pm" / "INDEX.md").open("a").write(line)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pm_render.py <decisions.json>", file=sys.stderr)
        sys.exit(1)

    d = json.loads(Path(sys.argv[1]).read_text())
    d.setdefault("fetched_at", datetime.now(tz=timezone.utc).isoformat(timespec="seconds"))

    date = d["report_date"]
    fname = f"PM_{date.replace('-','')}.html"
    out = REPO / "docs" / "pm" / fname
    out.write_text(render_html(d))
    print(f"wrote {out}")

    append_index(d)
    print("appended docs/pm/INDEX.md")

    update_research_page(d)
    print("updated docs/research/index.html markers")


if __name__ == "__main__":
    main()
