#!/usr/bin/env python3
"""Target generator — 跨層最強訊號，一鍵吐出一份可帶走的標的清單.

The dd-screener site is a multi-layer funnel (shape radar → main-table verdict →
candidate pool → timing sub-pages). That is the right structure for *managing*
research, but it is a lot to walk through when all you want is "give me the names
worth my own research today." This collapses all three discovery layers into ONE
static page: docs/dd-screener/targets.html.

Concentrated firepower = MULTIPLE INDEPENDENT lenses pointing at the same name.
A single signal is noise; three signals agreeing is a target. Each ticker is
scored by how many of six independent lenses light up — no fragile weighted
score, just a transparent count of confirmations:

  🚀 形狀   shape-scan hit (營收 YoY ≥ +20% + 股價轉強 + 毛利 OK)
  🟢 前瞻   analyst forward strong (FY+1→FY3 或 FY+1 營收預估 ≥ +15%)
  📈 加速   revenue growth accelerating (預估下季 YoY 明顯高於已報告)
  ✅ 進場   site DD §14 統一裁決 = 進場
  🎯 產業核心 flagged 🔴 core beneficiary in some ID (產業論述認證)
  ⏳ 持續   連續 ≥ 2 週在形狀榜（非一日遊）

Sources merged by normalized ticker:
  docs/dd-screener/pre_id_scan.json   (shape radar: lenses 🚀🟢📈⏳ + coverage)
  docs/dd-screener/latest.json        (main table: lens ✅ + FunnelRank/IRR/moat)
  docs/dd-screener/discovery_pool.json (candidate pool: lens 🎯 + ID themes)

Output is BAKED into the HTML (static, self-contained, deterministic) — the site
header + sub-nav are injected separately by scripts/site_nav.py. Regenerate with:
  python3 scripts/generate_targets.py            # merge + write targets.html
  python3 scripts/generate_targets.py --dry-run  # print distribution only
Then (first time / after adding to subnav): python3 scripts/site_nav.py
"""
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DDS = ROOT / "docs" / "dd-screener"
SCAN = DDS / "pre_id_scan.json"
LATEST = DDS / "latest.json"
POOL = DDS / "discovery_pool.json"
OUT = DDS / "targets.html"

FWD_STRONG_MIN = 15.0
PERSIST_MIN_WEEKS = 2
BOARD_MIN_FIREPOWER = 2  # main board = ≥2 independent lenses agree（集中火力）


def norm(t):
    return re.sub(r"[^A-Za-z0-9]", "", str(t)).upper()


def load():
    scan = json.loads(SCAN.read_text()) if SCAN.exists() else {"rows": [], "as_of": "—"}
    latest = json.loads(LATEST.read_text()) if LATEST.exists() else {"stocks": []}
    pool = json.loads(POOL.read_text()) if POOL.exists() else {"rows": []}
    stocks = latest.get("stocks", [])
    if isinstance(stocks, dict):
        stocks = [dict(v, ticker=k) for k, v in stocks.items()]
    return scan, {norm(s["ticker"]): s for s in stocks if s.get("ticker")}, \
        {norm(r["ticker"]): r for r in pool.get("rows", []) if r.get("ticker")}


def merge():
    scan, dd_by, pool_by = load()
    targets = {}

    def slot(tk):
        return targets.setdefault(tk, {
            "ticker": tk, "lenses": set(), "name": None, "industry": None,
            "mcap_bucket": None, "rev_growth": None, "fwd_pct": None, "accel": None,
            "coverage": None, "weeks": None, "verdict": None, "role": None,
            "irr": None, "funnel": None, "moat": None, "runway": None,
            "dd_path": None, "themes": None,
        })

    # ── shape radar (lenses 🚀 前瞻 加速 持續) ──────────────────────────────
    for r in scan.get("rows", []):
        tk = norm(r["ticker"])
        t = slot(tk)
        t["lenses"].add("shape")
        t["name"] = t["name"] or r.get("name")
        t["industry"] = t["industry"] or r.get("industry")
        t["mcap_bucket"] = t["mcap_bucket"] or r.get("mcap_bucket")
        t["rev_growth"] = r.get("rev_growth")
        t["fwd_pct"] = r.get("fwd_growth_pct")
        t["accel"] = r.get("accel")
        t["coverage"] = r.get("coverage")
        t["weeks"] = r.get("weeks_on_list")
        if r.get("dd_path"):
            t["dd_path"] = r["dd_path"]
        if isinstance(r.get("fwd_growth_pct"), (int, float)) and r["fwd_growth_pct"] >= FWD_STRONG_MIN:
            t["lenses"].add("fwd")
        if r.get("accel") == "up":
            t["lenses"].add("accel")
        if isinstance(r.get("weeks_on_list"), int) and r["weeks_on_list"] >= PERSIST_MIN_WEEKS:
            t["lenses"].add("persist")

    # ── main table (lens ✅ 進場 + decision-layer context) ───────────────────
    for tk, s in dd_by.items():
        if s.get("dca_verdict") == "進場":
            t = slot(tk)
            t["lenses"].add("enter")
    # attach DD context to every target that has a DD report (for display)
    for tk, t in targets.items():
        s = dd_by.get(tk)
        if not s:
            continue
        t["name"] = t["name"] or s.get("name")
        t["industry"] = t["industry"] or s.get("sector")
        t["verdict"] = s.get("dca_verdict")
        t["role"] = s.get("dca_role")
        t["irr"] = s.get("live_ev5y_pct")
        t["funnel"] = s.get("funnel_rank")
        t["moat"] = (s.get("moat_grade"), s.get("moat_score"), s.get("moat_trend"))
        t["runway"] = s.get("runway_post_y5")
        t["dd_path"] = t["dd_path"] or s.get("dca_path") or s.get("dd_path")
        if t["mcap_bucket"] is None:
            t["mcap_bucket"] = s.get("mcap_bucket")

    # ── candidate pool (lens 🎯 產業核心 + ID themes) ────────────────────────
    for tk, r in pool_by.items():
        if (r.get("core_count") or 0) >= 1:
            t = slot(tk)
            t["lenses"].add("thesis")
            t["themes"] = r.get("themes")
            t["name"] = t["name"] or r.get("ticker")
            t["mcap_bucket"] = t["mcap_bucket"] or r.get("mcap_bucket")
            if r.get("has_dd") and not t["dd_path"]:
                pass  # pool doesn't carry the path; main-table pass already set it

    for t in targets.values():
        t["firepower"] = len(t["lenses"])
    return scan.get("as_of", "—"), targets


LENS_META = [  # order = display order
    ("shape",   "🚀", "形狀",   "爆發形狀命中：季營收 YoY ≥ +20% + 股價轉強 + 毛利 OK"),
    ("fwd",     "🟢", "前瞻",   "分析師預估續強：FY+1→FY3 EPS CAGR 或 FY+1 營收預估 ≥ +15%"),
    ("accel",   "📈", "加速",   "營收成長加速中：預估下季 YoY 明顯高於已報告 YoY"),
    ("enter",   "✅", "進場",   "站上 DD §14 統一裁決 = 進場（已深研且判進場）"),
    ("thesis",  "🎯", "產業核心", "產業報告 §9 標為 🔴 核心受益（產業論述認證）"),
    ("persist", "⏳", "持續",   "連續 ≥ 2 週在形狀榜（非一日遊）"),
]
LENS_LABEL = {k: (emo, name) for k, emo, name, _ in LENS_META}


def main():
    dry = "--dry-run" in sys.argv
    as_of, targets = merge()
    ranked = sorted(
        targets.values(),
        key=lambda t: (-t["firepower"],
                       -(t["fwd_pct"] if isinstance(t["fwd_pct"], (int, float)) else -999),
                       -(t["rev_growth"] or 0)),
    )
    board = [t for t in ranked if t["firepower"] >= BOARD_MIN_FIREPOWER]
    watch = [t for t in ranked if t["firepower"] == 1]

    from collections import Counter
    fp_dist = Counter(t["firepower"] for t in ranked)
    print(f"標的合併 {len(ranked)} 檔 ｜ 火力分布 " +
          " ".join(f"{k}燈×{fp_dist[k]}" for k in sorted(fp_dist, reverse=True)))
    print(f"主榜（≥{BOARD_MIN_FIREPOWER} 燈）{len(board)} 檔 ｜ 觀察區（1 燈）{len(watch)} 檔\n")
    for t in board[:25]:
        lset = "".join(LENS_LABEL[k][0] for k, *_ in LENS_META if k in t["lenses"])
        print(f"  🔥{t['firepower']} {t['ticker']:<7}{lset:<8}"
              f"cov={t['coverage'] or '—':<4}rev={t['rev_growth']}  fwd={t['fwd_pct']}  "
              f"verdict={t['verdict'] or '—'}")
    if dry:
        print("\n(dry-run) 不寫 HTML")
        return
    html = render(as_of, board, watch, fp_dist)
    OUT.write_text(html, encoding="utf-8")
    print(f"\n✓ Wrote {OUT} ({OUT.stat().st_size:,} bytes) — 記得跑 python3 scripts/site_nav.py 套 nav")


def _cov_badge(t):
    c = t.get("coverage")
    if c == "dd" or t.get("verdict"):
        return '<span class="cov cov-dd">✅ 有 DD</span>'
    if c == "id":
        return '<span class="cov cov-id">🟡 有 ID</span>'
    if "thesis" in t["lenses"]:
        return '<span class="cov cov-id">🎯 候選池</span>'
    return '<span class="cov cov-blind">🔭 盲區</span>'


def _start_link(t):
    """起點：已研究連站上裁決當起點；未研究就是你的研究清單。"""
    if t.get("dd_path"):
        return f'<a class="start start-dd" href="{t["dd_path"]}" target="_blank">讀站上裁決 →</a>'
    theme = (t.get("themes") or [None])[0]
    if theme:
        return f'<span class="start start-self" title="{theme}">你的研究起點（產業：{theme[:16]}）</span>'
    return '<span class="start start-self">你的研究起點（零覆蓋）</span>'


def _row(t):
    lenses_html = "".join(
        f'<span class="lens lens-on" title="{tip}">{emo}{name}</span>' if k in t["lenses"]
        else f'<span class="lens lens-off" title="{tip}">{emo}</span>'
        for k, emo, name, tip in LENS_META
    )
    rev = f'+{round(t["rev_growth"]*100)}%' if isinstance(t["rev_growth"], (int, float)) else "—"
    fwd = (f'{"+" if t["fwd_pct"] >= 0 else ""}{round(t["fwd_pct"])}%'
           if isinstance(t["fwd_pct"], (int, float)) else "—")
    verdict = t.get("verdict")
    vclass = {"進場": "v-in", "觀望": "v-watch", "迴避": "v-avoid"}.get(verdict, "")
    vhtml = f'<span class="verdict {vclass}">{verdict}</span>' if verdict else '<span class="verdict v-none">—</span>'
    irr = f'{t["irr"]:+.0f}%' if isinstance(t.get("irr"), (int, float)) else "—"
    wk = f'{t["weeks"]}週' if isinstance(t.get("weeks"), int) else "—"
    researched = "1" if t.get("dd_path") else "0"
    return (
        f'<tr data-fp="{t["firepower"]}" data-researched="{researched}" data-verdict="{verdict or ""}">'
        f'<td class="fp">🔥{t["firepower"]}</td>'
        f'<td class="tk"><strong>{t["ticker"]}</strong>'
        + (f'<span class="nm">{t["name"]}</span>' if t.get("name") and t["name"] != t["ticker"] else "")
        + f'</td>'
        f'<td class="lenses">{lenses_html}</td>'
        f'<td>{_cov_badge(t)}</td>'
        f'<td class="mc">{t.get("mcap_bucket") or "—"}</td>'
        f'<td class="num">{rev}</td>'
        f'<td class="num fwd">{fwd}</td>'
        f'<td>{vhtml}</td>'
        f'<td class="num">{irr}</td>'
        f'<td class="wk">{wk}</td>'
        f'<td class="ind">{t.get("industry") or "—"}</td>'
        f'<td class="start-cell">{_start_link(t)}</td>'
        f'</tr>'
    )


def render(as_of, board, watch, fp_dist):
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    legend = "".join(
        f'<span class="lg"><b>{emo} {name}</b> — {tip}</span>' for k, emo, name, tip in LENS_META
    )
    rows = "\n".join(_row(t) for t in board)
    watch_rows = "\n".join(_row(t) for t in watch)
    n3 = sum(v for k, v in fp_dist.items() if k >= 3)
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>🎯 標的產生器 — 跨層最強訊號 | InvestMQuest</title>
<style>
  :root {{ --ink:#1e293b; --mut:#64748b; --line:#e2e8f0; --bg:#f8fafc; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:'Inter','Noto Sans TC',-apple-system,sans-serif; color:var(--ink); background:var(--bg); }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:22px 18px 60px; }}
  h1 {{ font-size:22px; margin:0 0 4px; }}
  .sub {{ color:var(--mut); font-size:13px; line-height:1.7; margin:0 0 16px; }}
  .sub b {{ color:var(--ink); }}
  .legend {{ display:flex; flex-wrap:wrap; gap:6px 14px; background:#fff; border:1px solid var(--line); border-radius:10px; padding:12px 16px; margin-bottom:14px; }}
  .lg {{ font-size:11px; color:var(--mut); }}
  .lg b {{ color:var(--ink); font-weight:600; }}
  .controls {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px; font-size:12px; }}
  .controls button {{ font:inherit; font-size:12px; padding:5px 12px; border:1px solid #cbd5e1; background:#fff; border-radius:99px; cursor:pointer; color:var(--mut); }}
  .controls button.active {{ background:#0f172a; color:#fff; border-color:#0f172a; font-weight:600; }}
  .count {{ color:var(--mut); margin-left:auto; }}
  .tbl-scroll {{ overflow-x:auto; background:#fff; border:1px solid var(--line); border-radius:10px; }}
  table {{ width:100%; border-collapse:collapse; font-size:12px; white-space:nowrap; }}
  thead th {{ background:#f1f5f9; color:#334155; text-align:left; padding:8px 10px; font-weight:600; position:sticky; top:0; }}
  td {{ padding:7px 10px; border-top:1px solid #eef2f7; }}
  .fp {{ font-weight:700; color:#b45309; }}
  .tk strong {{ color:#0f172a; }}
  .tk .nm {{ display:block; font-weight:400; color:var(--mut); font-size:10.5px; }}
  .lenses {{ white-space:nowrap; }}
  .lens {{ display:inline-block; margin-right:2px; font-size:10.5px; }}
  .lens-on {{ background:#ecfdf5; color:#166534; padding:1px 5px; border-radius:6px; }}
  .lens-off {{ opacity:.22; }}
  .cov {{ padding:1px 7px; border-radius:99px; font-size:10.5px; }}
  .cov-dd {{ background:#dcfce7; color:#166534; }}
  .cov-id {{ background:#fef9c3; color:#92400e; }}
  .cov-blind {{ background:#e0f2fe; color:#075985; }}
  .num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .fwd {{ color:#166534; font-weight:600; }}
  .verdict {{ padding:1px 7px; border-radius:99px; font-size:10.5px; font-weight:700; }}
  .v-in {{ background:#dcfce7; color:#166534; }}
  .v-watch {{ background:#fef3c7; color:#92400e; }}
  .v-avoid {{ background:#fee2e2; color:#991b1b; }}
  .v-none {{ color:#cbd5e1; }}
  .ind {{ color:var(--mut); max-width:180px; overflow:hidden; text-overflow:ellipsis; }}
  .start {{ font-size:10.5px; }}
  .start-dd {{ color:#1d4ed8; text-decoration:none; font-weight:600; }}
  .start-self {{ color:#7c3aed; }}
  .watch-h {{ margin:26px 0 8px; font-size:14px; color:var(--mut); }}
  .note {{ font-size:11px; color:var(--mut); background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:10px 14px; margin:14px 0; line-height:1.7; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>🎯 標的產生器 — 跨層最強訊號</h1>
  <p class="sub">
    把三層漏斗（<b>形狀掃描</b> × <b>主表 §14 裁決</b> × <b>產業候選池</b>）疊在一起，只留<b>多個獨立訊號同時指向</b>的名字——單一訊號是雜訊，多層同意才是火力。
    <b>用途：</b>帶走做你自己的研究。已研究的（✅ 有 DD）連到站上裁決當<b>起點</b>；未研究的就是<b>你的研究清單</b>。
    這裡只給「該研究誰」的排序，不是買入清單。<br>
    <span style="color:#94a3b8">資料 as of {as_of}｜生成 {now}｜六燈全亮＝六種獨立方法一致，越多燈火力越集中（≥3 燈共 {n3} 檔）</span>
  </p>
  <div class="legend">{legend}</div>
  <div class="controls">
    <button data-f="all" class="active">全部（{len(board)}）</button>
    <button data-f="self">只看未研究（我的研究清單）</button>
    <button data-f="enter">只看站上判進場</button>
    <span class="count" id="shown"></span>
  </div>
  <div class="tbl-scroll">
    <table id="tbl">
      <thead><tr>
        <th title="亮燈數＝幾種獨立方法指向這檔">火力</th><th>Ticker</th><th>六燈（獨立訊號）</th>
        <th>覆蓋</th><th>市值級</th><th class="num">營收YoY</th><th class="num">前瞻</th>
        <th>裁決</th><th class="num">5Y IRR</th><th>週</th><th>Industry</th><th>起點</th>
      </tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>
  <p class="note">
    <b>怎麼用：</b>火力越高＝越多獨立方法同意，優先看。<b>✅ 有 DD</b> 的名字站上已深研，點「讀站上裁決」看 §14 結論當你研究的起點；
    <b>🔭 盲區 / 🎯 候選池</b> 的名字站上還沒建 DD——這些就是你自己研究最有增量的地方（沒人先入為主）。
    「前瞻」與「加速」用分析師預估過濾掉基期效應/週期頂，讓「正在噴」與「將持續噴」分開。
    估值與獲利品質<b>刻意不在這層把關</b>（多倍股早期永遠看起來貴），那是你研究時自己判。<br>
    <b>循環標的另有專軌：</b>trailing 財務難看但分析師正在上修的循環底部候選，見 <a href="/dd-screener/cyclical-track.html" style="color:#1d4ed8;text-decoration:none;font-weight:600">衛星·循環軌 →</a>（研究提名，非進場清單）。
  </p>

  <h2 class="watch-h">觀察區 — 單一訊號（{len(watch)} 檔，火力未集中）</h2>
  <p class="sub" style="margin-bottom:8px">只有一種方法指向、其他層還沒跟上——留著追蹤，週數累積或其他訊號亮起就會升上主榜。</p>
  <div class="tbl-scroll">
    <table>
      <thead><tr>
        <th>火力</th><th>Ticker</th><th>六燈</th><th>覆蓋</th><th>市值級</th>
        <th class="num">營收YoY</th><th class="num">前瞻</th><th>裁決</th><th class="num">5Y IRR</th><th>週</th><th>Industry</th><th>起點</th>
      </tr></thead>
      <tbody>
{watch_rows}
      </tbody>
    </table>
  </div>
</div>
<script>
(function() {{
  var buttons = document.querySelectorAll('.controls button');
  var rows = Array.prototype.slice.call(document.querySelectorAll('#tbl tbody tr'));
  var shown = document.getElementById('shown');
  function apply(f) {{
    var n = 0;
    rows.forEach(function(r) {{
      var ok = f === 'all'
        || (f === 'self' && r.getAttribute('data-researched') === '0')
        || (f === 'enter' && r.getAttribute('data-verdict') === '進場');
      r.style.display = ok ? '' : 'none';
      if (ok) n++;
    }});
    shown.textContent = '顯示 ' + n + ' 檔';
  }}
  buttons.forEach(function(b) {{
    b.addEventListener('click', function() {{
      buttons.forEach(function(x) {{ x.classList.remove('active'); }});
      b.classList.add('active');
      apply(b.getAttribute('data-f'));
    }});
  }});
  apply('all');
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
