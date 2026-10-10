#!/usr/bin/env python3
"""docs/dd-screener/tw/index.html — DD Screener 台股池頁（2026-10-09）。

The page is derived from the main DD Screener page (docs/dd-screener/index.html)
on every run instead of being a hand-kept fork:

  * the main page loads its data with fetch('./latest.json'), a relative path,
    so the same HTML placed in docs/dd-screener/tw/ reads tw/latest.json
    (build_dd_screener.py --universe tw) with no JS change;
  * only the <title> and the hero's left column are replaced, the moat filter
    opens on [All] instead of [S] (only DD names carry a moat grade), and a TW notice
    box is inserted under the hero. The box carries what differs from the US
    page: the OCF cash-flow condition, pool definition, TWD EPS, the TW timing
    reference, the revision baseline, no-EPS names and DD coverage. Counts come from the JSONs at
    generation time, so the workflow reruns this after each TW build;
  * when tw/latest.json scores cash flow as OCF (criteria key "ocf"), the
    three JS spots that hard-code the FCF criterion are pointed at it
    (CASH_PATCHES), each with an exact-count check;
  * when tw/latest.json scores EPS growth as FY+1→FY+2 (the TW criterion label),
    the growth column is pointed at eps2y and its FY+1→FY+3 revision chip is
    dropped (GROWTH_PATCHES), with the same exact-count check;
  * the site nav is re-injected with site_nav.process(), so the page gets the
    research/dds highlight and the DD Screener sub-nav like its siblings.

If an anchor in the main page moves, the script exits 1 and leaves the old
tw/index.html in place (the workflow step only warns).

Usage:
  python3 scripts/build_dd_screener_tw_page.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MAIN_PAGE = DOCS / "dd-screener" / "index.html"
MAIN_JSON = DOCS / "dd-screener" / "latest.json"
TW_JSON = DOCS / "dd-screener" / "tw" / "latest.json"
TW_SNAP_DIR = DOCS / "dd-screener" / "tw" / "eps-estimates-snapshots"
TW_SCREENER = DOCS / "screener" / "tw_latest.json"
OUT = DOCS / "dd-screener" / "tw" / "index.html"

TITLE_RE = re.compile(r"<title>[^<]*</title>")
HERO_LEFT_RE = re.compile(
    r'(<div class="hero-inner">\s*<div>)(.*?)(</div>\s*<div class="hero-badge")', re.S)
SPOTLIGHT_RE = re.compile(r'<section class="ath-spotlight"')
# The main page opens on the S-moat filter. Only the DD names carry a moat
# grade, and 60 of the 69 TW names have no DD, so the TW page opens on [All].
MOAT_STATE_RE = re.compile(r"(\n\s*moat:\s*)'S'(,)")
MOAT_CHIP_S = '<span class="chip active" data-filter="moat" data-value="S"'
MOAT_CHIP_ALL = '<span class="chip" data-filter="moat" data-value="All"'
# 2026-10-09: the TW pool scores cash flow as OCF≥10% instead of FCF≥10%
# (build_dd_screener.py TW_OCF_CRITERION), so its criteria list carries the key
# "ocf". The main page JS hard-codes critByKey.fcf three times (profit-group
# header and cell) and the custom panel reads only the FCF box. These patches
# point both at ocf. They are applied only when tw/latest.json really carries
# the ocf criterion, so page and data never disagree.
CASH_PATCHES = (
    ("critByKey.fcf", "critByKey.ocf", 3),
    ("    fcf:   parseFloat(document.getElementById('cust-fcf').value)   || 10,\n",
     "    fcf:   parseFloat(document.getElementById('cust-fcf').value)   || 10,\n"
     "    ocf:   parseFloat(document.getElementById('cust-fcf').value)   || 10,\n", 1),
    ("<label>FCF ≥ (%)</label>", "<label>OCF ≥ (%)</label>", 1),
    # The quality veto's cash/NI item and the decline signal "FCF 遜於淨利" are
    # computed on OCF in the TW pool too (build_dd_screener.py CASH_BASIS).
    ("FCF對淨利率偏低", "營業現金流對淨利率偏低", 1),
    ("FCF 遜於淨利", "營業現金流遜於淨利", 1),
)
# 2026-10-09: the TW pool scores EPS growth as Koyfin FY+1→FY+2
# (build_dd_screener.py TW_EPS_GROWTH_LABEL / EPS_GROWTH_SPAN), stored in eps2y.
# The main page's growth column shows eps_fy1_fy3_cagr_pct under the criterion
# label, with a month-on-month chip that compares FY+1→FY+3 CAGRs. These patches
# make the TW column show and sort by eps2y and drop that chip, since it measures
# a different span. Applied only when tw/latest.json carries the TW label.
TW_GROWTH_LABEL = "FY+1→FY+2 成長≥15%"
GROWTH_PATCHES = (
    ("  var cagr = s.eps_fy1_fy3_cagr_pct;\n", "  var cagr = s.eps2y;\n", 1),
    ("  var revPp = s.eps2y_revision_pp;\n", "  var revPp = null;\n", 1),
    ("  var revDir = s.eps2y_revision_dir;\n", "  var revDir = null;\n", 1),
    ("'Excel FY+1→FY+3 forward CAGR ' + cagr.toFixed(1)",
     "'Koyfin FY+1→FY+2 EPS 成長 ' + cagr.toFixed(1)", 1),
    ("'修正動能 baseline 累積中（首月 snapshot 尚未對照）'",
     "'台股池此欄不顯示月修正（月快照比的是 FY+1→FY+3 年化成長）'", 1),
    ("_thSortable(critByKey.eps2y.label, 'eps_fy1_fy3_cagr_pct', {title: 'Excel FY+1→FY+3 forward 2Y CAGR — "
     "buy-side consensus，覆蓋隨 Koyfin watchlist 動態變動'})",
     "_thSortable(critByKey.eps2y.label, 'eps2y', {title: 'Koyfin FY+1→FY+2 EPS 成長率（今年到明年），台股池的成長條件'})", 1),
)


def esc(s) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — missing file degrades to "—" in the box
        return {}


def facts() -> dict:
    tw = load(TW_JSON)
    main = load(MAIN_JSON)
    rows = tw.get("stocks", []) or []
    pool_codes = {str(r.get("ticker", "")).split(".")[0] for r in rows}
    dd_in = [r for r in rows if r.get("dd_status") == "dd"]
    dd_out = [r for r in main.get("stocks", []) or []
              if r.get("dd_status") == "dd"
              and str(r.get("ticker", "")).upper().endswith((".TW", ".TWO"))
              and str(r.get("ticker", "")).split(".")[0] not in pool_codes]
    no_eps = [r for r in rows
              if r.get("eps_fy_curr") is None and r.get("eps_fy_next") is None
              and r.get("eps_fy3") is None]
    as_of = str(tw.get("as_of") or "")[:10]
    month = as_of[:7]
    earlier = sorted(p.stem for p in TW_SNAP_DIR.glob("*.json")
                     if re.fullmatch(r"\d{4}-\d{2}", p.stem) and p.stem < month)
    fx = tw.get("display_fx") or {}
    listing = tw.get("tw_listing") or {}
    fcf_low = [r for r in rows if r.get("fcf") is not None and r["fcf"] < 10]
    return {
        "ocf_mode": any(c.get("key") == "ocf" for c in tw.get("criteria") or []),
        "growth_mode": any(c.get("key") == "eps2y" and c.get("label") == TW_GROWTH_LABEL
                           for c in tw.get("criteria") or []),
        "n_fy2": sum(1 for r in rows if r.get("eps_fy_curr") is not None and r.get("eps_fy_next") is not None),
        "n_fy3": sum(1 for r in rows if r.get("eps_fy_curr") is not None and r.get("eps_fy3") is not None),
        "n_fcf_low": len(fcf_low),
        "n_ocf_ok": sum(1 for r in fcf_low if r.get("ocf") is not None and r["ocf"] >= 10),
        "as_of": as_of or "—",
        "n": len(rows),
        "tpex": len(listing.get("tpex") or []),
        "emerging": len(listing.get("emerging") or []),
        "fx": fx.get("local_per_usd"),
        "fx_date": fx.get("as_of") or "—",
        # DD rows go through the main build's per-row conversion (rate backed
        # out of yfinance's local-currency EPS), so they match the main page
        # and carry their own eps_fx_rate instead of the pool's spot rate.
        "n_own_fx": sum(1 for r in rows
                        if r.get("eps_fx_rate") is not None and fx.get("local_per_usd")
                        and abs(r["eps_fx_rate"] - fx["local_per_usd"]) > 1e-6),
        "dd_in": dd_in,
        "dd_out": dd_out,
        "no_eps": no_eps,
        "has_baseline": bool(earlier),
        "first_snapshot": min((p.stem for p in TW_SNAP_DIR.glob("*.json")), default=None),
        "tw_ref_n": len(load(TW_SCREENER).get("rankings") or []),
    }


def hero_html(f: dict) -> str:
    return (
        '\n      <div class="hero-h1">DD Screener 台股池</div>\n'
        '      <div class="hero-sub">母體是 Koyfin 的台股篩選：市值 10 億美元以上、'
        'ROIC（投入資本報酬率）15% 以上，'
        f'目前 {f["n"]} 檔，其中上櫃 {f["tpex"]} 檔'
        + (f'、興櫃 {f["emerging"]} 檔' if f.get("emerging") else '') + '。'
        '評分與排序規則跟美股主頁相同，資料各自獨立。</div>\n'
        '      <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:6px;align-items:center">'
        '<a href="/dd-screener/" style="display:inline-flex;align-items:center;gap:5px;padding:5px 10px;'
        'background:var(--line-soft);color:var(--accent);border:1px solid var(--line);border-radius:6px;'
        'font-size:12px;font-weight:600;text-decoration:none">← 美股主頁</a>'
        '<a href="/cockpit-tw/" style="display:inline-flex;align-items:center;gap:5px;padding:5px 10px;'
        'background:var(--line-soft);color:var(--accent);border:1px solid var(--line);border-radius:6px;'
        'font-size:12px;font-weight:600;text-decoration:none">台股選股主控台 →</a></div>\n    ')


def notice_html(f: dict) -> str:
    fx = f'{f["fx"]:.2f}' if f["fx"] else "—"
    own = (f'有 DD 報告的其中 {f["n_own_fx"]} 檔沿用美股主頁的換算，數字跟主頁一致。'
           if f["n_own_fx"] else '')
    items = [
        f'<b>幣別</b>：股價與目標價是新台幣。EPS 原本是 Koyfin 的美元數字，'
        f'這裡按 1 美元兌 {fx} 元（{esc(f["fx_date"])}）換回新台幣，滑過 EPS 可看美元原值。{own}',
        f'<b>時機欄</b>：距 52 週高點、RS（相對強弱，近 1、4、13 週漲幅在一群股票裡的百分位）'
        f'是跟台股 RS 雷達的 {f["tw_ref_n"] or "—"} 檔比，不跟美股比。',
    ]
    if f["ocf_mode"]:
        items.insert(0, '<b>現金流條件</b>：四條件裡的現金流一條，台股池看營業現金流利潤率（OCF，'
                     '扣資本支出之前的現金流占營收）10% 以上，不看自由現金流利潤率。'
                     '台股不少公司正在擴產，資本支出壓低了自由現金流。資本支出值不值得，交給 ROIC 那一條判斷。'
                     f'池內 {f["n_fcf_low"]} 檔自由現金流利潤率不到 10%，其中 {f["n_ocf_ok"]} 檔營業現金流利潤率在 10% 以上。'
                     '排序的品質面向，以及體質、衰退訊號裡跟淨利比的那一項，也改用營業現金流。')
    if f["growth_mode"]:
        items.insert(1 if f["ocf_mode"] else 0,
                     '<b>成長條件</b>：EPS 成長一條，台股池看 Koyfin 分析師預估的今年到明年（FY+1→FY+2）'
                     'EPS 成長率，15% 以上算過。美股主頁看的是今年到後年（FY+1→FY+3）的年化成長。'
                     f'池內 {f["n"]} 檔有明年預估的 {f["n_fy2"]} 檔，有後年預估的只有 {f["n_fy3"]} 檔，'
                     '所以台股只看到明年。Koyfin 沒有預估的，這一條算不過。'
                     '月修正比的是今年到後年的年化成長，跟這一條不同，所以成長欄不顯示月修正。'
                     '名次排序裡的成長面向仍用今年到後年的年化成長，沒有後年預估的少這一項。')
    if f["has_baseline"]:
        items.append('<b>上修</b>：每月 2 日存一次 EPS 快照，「上修」欄是跟上月快照比。')
    else:
        first = esc(f["first_snapshot"] or "—")
        items.append(f'<b>上修</b>：「上修」是本月 EPS 預估跟上月快照比。台股池第一份快照是 {first}，'
                     '要到下個月才有第一筆上修數字，在那之前上修欄是空的，排序也少了這一塊。')
    if f["no_eps"]:
        names = "、".join(esc(r.get("name") or r.get("ticker")) for r in f["no_eps"][:8])
        more = f" 等 {len(f['no_eps'])} 檔" if len(f["no_eps"]) > 8 else ""
        items.append(f'<b>沒有分析師預估</b>：{names}{more}在 Koyfin 沒有 EPS 預估。'
                     '它們的名次只看品質和股價，沒有成長預估可比，參考價值較低。')
    if f["dd_in"]:
        names = "、".join(esc(r.get("name") or r.get("ticker")) for r in f["dd_in"])
        items.append(f'<b>DD 報告</b>：池內 {len(f["dd_in"])} 檔有 DD 報告（{names}），'
                     '裁決與護城河分數沿用美股主頁。')
    if f["dd_out"]:
        names = "、".join(esc(str(r.get("ticker")).split(".")[0]) for r in f["dd_out"])
        items.append(f'另有 {len(f["dd_out"])} 檔台股 DD 不符合本池篩選（{names}），'
                     '只列在<a href="/dd-screener/">美股主頁</a>。')
    items.append('下方各欄說明文字沿用美股主頁，跟本框有出入時以本框為準。')
    lis = "".join(f"<li>{x}</li>" for x in items)
    return (
        '<section id="tw-pool-note" style="margin:12px 20px">'
        '<div style="background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);'
        'border-radius:8px;padding:12px 16px;font-size:12.5px;line-height:1.75;color:var(--ink)">'
        f'<div style="font-weight:700;margin-bottom:4px">台股池跟美股主頁的差別（資料日 {esc(f["as_of"])}）</div>'
        f'<ul style="margin:0;padding-left:18px">{lis}</ul></div></section>\n'
    )


def main() -> int:
    if not TW_JSON.exists():
        print(f"ERROR: {TW_JSON} missing — run build_dd_screener.py --universe tw first",
              file=sys.stderr)
        return 1
    html = MAIN_PAGE.read_text(encoding="utf-8")
    f = facts()
    new, n1 = TITLE_RE.subn("<title>DD Screener 台股池 — InvestMQuest Research</title>", html, count=1)
    new, n2 = HERO_LEFT_RE.subn(lambda m: m.group(1) + hero_html(f) + m.group(3), new, count=1)
    new, n3 = SPOTLIGHT_RE.subn(lambda m: notice_html(f) + m.group(0), new, count=1)
    new, n4 = MOAT_STATE_RE.subn(lambda m: m.group(1) + "'All'" + m.group(2), new, count=1)
    n5 = new.count(MOAT_CHIP_S) + new.count(MOAT_CHIP_ALL)
    new = (new.replace(MOAT_CHIP_S, MOAT_CHIP_S.replace("chip active", "chip"), 1)
              .replace(MOAT_CHIP_ALL, MOAT_CHIP_ALL.replace('"chip"', '"chip active"'), 1))
    if (n1, n2, n3, n4, n5) != (1, 1, 1, 1, 2):
        print(f"ERROR: main page anchors moved (title={n1} hero={n2} spotlight={n3} "
              f"moat_state={n4} moat_chips={n5}); {OUT} left unchanged", file=sys.stderr)
        return 1
    if f["ocf_mode"]:
        for old, rep, want in CASH_PATCHES:
            got = new.count(old)
            if got != want:
                print(f"ERROR: OCF patch anchor {old[:40]!r} found {got}x, expected {want}x; "
                      f"{OUT} left unchanged", file=sys.stderr)
                return 1
            new = new.replace(old, rep)
    if f["growth_mode"]:
        for old, rep, want in GROWTH_PATCHES:
            got = new.count(old)
            if got != want:
                print(f"ERROR: growth patch anchor {old[:40]!r} found {got}x, expected {want}x; "
                      f"{OUT} left unchanged", file=sys.stderr)
                return 1
            new = new.replace(old, rep)
    if "fetch('./latest.json')" not in new:
        print("ERROR: main page no longer loads ./latest.json relatively; "
              f"{OUT} left unchanged", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(new, encoding="utf-8")
    sys.path.insert(0, str(ROOT / "scripts"))
    import site_nav  # noqa: E402
    status = site_nav.process(OUT)
    print(f"wrote {OUT} ({len(new):,} bytes, nav {status}); pool {f['n']}, "
          f"DD in pool {len(f['dd_in'])}, DD outside {len(f['dd_out'])}, no-EPS {len(f['no_eps'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
