#!/usr/bin/env python3
"""dd5 新版面：render.py 的產物套上新外觀（固定側邊目錄、頂部列、結論卡、內嵌 SVG 圖）。

用法：python3 scripts/dd5/render_pretty.py <run目錄> [--out html] [--back /stock-dash/?t=XXX]
做法：先呼叫 render.render（寫 calc.json、number_check.json、取得回傳值），期間暫時換掉
render.py 的 table_html／price_svg／cases3_table 與 collect_refs 掛鉤，讓表格與圖用新版樣式；
再把產出的正文（<article class="doc">）拆出標題、章節、來源，套進新外殼覆蓋 out。
佔位與正文由 render.py 處理，render.py 新增的佔位會自動流進新版頁面，這裡不維護清單。
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import render as R  # noqa: E402

esc = R.esc
_CTX = {}  # render() 期間的上下文（run 目錄、同業資料），給掛鉤函式用


# ------------------------------------------------------------ 表格：數字欄靠右
NUM_CH = r"[\d,.\s%+\-−–～~／/x×倍億美元：:]"


def _plain(c):
    return re.sub(r"<[^>]+>", "", c).strip()


def is_num(c):
    t = _plain(c)
    return bool(re.fullmatch(NUM_CH + "*\\d" + NUM_CH + "*", t)) or t in ("—", "")


def table_html(header, rows, cls=""):
    ncol = len(header)
    numcol = []
    for j in range(ncol):
        vals = [r[j] for r in rows if j < len(r) and _plain(r[j]) not in ("", "—")]
        numcol.append(bool(vals) and all(is_num(v) for v in vals) and j > 0)
    s = '<div class="tw"><table class="{0}{2}"><thead><tr>{1}</tr></thead><tbody>'.format(
        cls, "".join('<th{1}>{0}</th>'.format(h, ' class="num"' if numcol[j] else "") for j, h in enumerate(header)), " w4" if ncol >= 4 else "")
    for r in rows:
        s += "<tr>" + "".join('<td{1}>{0}</td>'.format(c, ' class="num"' if j < ncol and numcol[j] else "") for j, c in enumerate(r)) + "</tr>"
    return s + "</tbody></table></div>"



def f1(v, d=1):
    return "{0:.{1}f}".format(v, d)


# ------------------------------------------------------------ 股價位置圖
def price_chart(pc):
    if not pc:
        return "<p class='note'>（沒有價格序列，圖略。）</p>"
    mc = pc["monthly_close"]
    W, H, L, Rr, T, B = 720, 300, 62, 16, 16, 32
    vals = [v for _, v in mc] + [pc["ath_close"]]
    lo, hi = min(vals) * 0.95, max(vals) * 1.05
    n = len(mc)
    idx = {d: i for i, (d, _) in enumerate(mc)}

    def x(i):
        return L + (W - L - Rr) * i / max(n - 1, 1)

    def y(v):
        return T + (H - T - B) * (1 - (v - lo) / (hi - lo))

    def path(series):
        pts = [(x(idx[d]), y(v)) for d, v in series if d in idx]
        return "M" + " L".join("{0:.1f},{1:.1f}".format(a, b) for a, b in pts)
    s = ['<svg viewBox="0 0 {0} {1}" class="chart pc" role="img" aria-label="月底收盤價、10 個月與 20 個月均線，以及歷史最高收盤水平線" data-l="{2}" data-r="{3}" data-w="{0}">'.format(W, H, L, Rr)]
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        s.append('<line x1="{0}" x2="{1}" y1="{2:.1f}" y2="{2:.1f}" class="grid"/><text x="{3}" y="{4:.1f}" class="ax" text-anchor="end">{5:,.0f}</text>'.format(L, W - Rr, y(v), L - 8, y(v) + 4, v))
    for i in range(0, n, 24):
        s.append('<text x="{0:.1f}" y="{1}" class="ax" text-anchor="middle">{2}</text>'.format(x(i), H - 10, mc[i][0][:4]))
    s.append('<line x1="{0}" x2="{1}" y1="{2:.1f}" y2="{2:.1f}" class="ath"/>'.format(L, W - Rr, y(pc["ath_close"])))
    s.append('<text x="{0}" y="{1:.1f}" class="lab mut" text-anchor="start">歷史最高收盤 {2:,.0f}（{3}）</text>'.format(L + 6, y(pc["ath_close"]) - 7, pc["ath_close"], pc["ath_date"][:7]))
    s.append('<path d="{0}" class="ma20"/>'.format(path(pc["ma20"])))
    s.append('<path d="{0}" class="ma10"/>'.format(path(pc["ma10"])))
    s.append('<path d="{0}" class="px"/>'.format(path(mc)))
    s.append('<circle cx="{0:.1f}" cy="{1:.1f}" r="4" class="dot"/>'.format(x(n - 1), y(pc["last"])))
    s.append('<text x="{0:.1f}" y="{1:.1f}" class="lab" text-anchor="end">現價 {2:,.1f}</text>'.format(x(n - 1) - 9, y(pc["last"]) + 18, pc["last"]))
    s.append('<line class="xh" x1="0" x2="0" y1="{0}" y2="{1}" style="display:none"/><circle class="xd" r="4" style="display:none"/>'.format(T, H - B))
    s.append("</svg>")
    ma10 = dict(map(tuple, pc["ma10"]))
    ma20 = dict(map(tuple, pc["ma20"]))
    data = [[d, v, ma10.get(d), ma20.get(d)] for d, v in mc]
    ys = [round(y(v), 1) for _, v in mc]
    leg = ('<p class="legend"><span class="k px"></span>月底收盤　<span class="k ma10"></span>10 個月均線　<span class="k ma20"></span>20 個月均線　'
           '<span class="k ath"></span>歷史最高收盤（未還原股息）</p>')
    return ('<figure class="fig"><figcaption>股價位置（月線）</figcaption><div class="cbox">' + "".join(s) +
            '<div class="tip" hidden></div></div>' + leg +
            '<script type="application/json" class="pcdata">' + json.dumps({"d": data, "y": ys, "x": [round(x(i), 1) for i in range(n)]}, ensure_ascii=False) + "</script></figure>")



# ------------------------------------------------------------ 同業橫條圖
PEER_METRICS = [("毛利率", "gm", "pct"), ("營益率", "om", "pct"), ("投入資本報酬率", "roic", "pct"), ("營收成長", "growth", "pct"), ("預估本益比", "pe_fwd", "x")]


def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v == v else None


def bar_panel(title, items, kind):
    """items: [(name, value, is_target)]；沒有任何數值回傳空字串；負值往零線左邊畫。"""
    items = [i for i in items if _num(i[1]) is not None]
    if not items:
        return ""
    items.sort(key=lambda i: -i[1])
    W, rowh, padt, lw, rw = 360, 28, 26, 52, 58
    H = padt + rowh * len(items) + 6
    vmin, vmax = min(0, min(i[1] for i in items)), max(0, max(i[1] for i in items))
    span = (vmax - vmin) or 1
    x0 = lw
    tw = W - lw - rw

    def X(v):
        return x0 + tw * (v - vmin) / span
    zero = X(0)
    s = ['<svg viewBox="0 0 {0} {1}" class="chart bp" role="img" aria-label="{2}">'.format(W, H, esc(title)), '<text x="0" y="14" class="ptitle">{0}</text>'.format(esc(title))]
    for k, (nm, v, tgt) in enumerate(items):
        yy = padt + rowh * k
        a, b = sorted((zero, X(v)))
        lab = ("{0:.1f}%".format(v * 100) if kind == "pct" else "{0:.1f} 倍".format(v))
        s.append('<text x="{0}" y="{1}" class="rn" text-anchor="end">{2}</text>'.format(lw - 8, yy + 17, esc(nm)))
        s.append('<rect x="{0:.1f}" y="{1}" width="{2:.1f}" height="16" rx="3" class="{3}"><title>{4} {5}</title></rect>'.format(a, yy + 4, max(b - a, 1.5), "b-t" if tgt else "b-o", esc(nm), lab))
        if v >= 0:
            s.append('<text x="{0:.1f}" y="{1}" class="rv{3}">{2}</text>'.format(b + 6, yy + 17, lab, " t" if tgt else ""))
        else:
            s.append('<text x="{0:.1f}" y="{1}" class="rv{3}">{2}</text>'.format(zero + 6, yy + 17, lab, " t" if tgt else ""))
    s.append('<line x1="{0:.1f}" x2="{0:.1f}" y1="{1}" y2="{2}" class="zero"/>'.format(zero, padt, H - 4))
    s.append("</svg>")
    return '<div class="panel">' + "".join(s) + "</div>"


def peers_chart(peers, ticker):
    data = peers.get("data") or {}
    if not data:
        return ""
    panels, fys = [], {}
    for title, key, kind in PEER_METRICS:
        items = []
        for t, d in data.items():
            d = d or {}
            if key == "pe_fwd":
                v = (d.get("val") or {}).get("pe_fwd")
            else:
                yrs = d.get("years") or []
                v = yrs[0].get(key) if yrs else None
                if yrs and yrs[0].get("fy"):
                    fys[t] = str(yrs[0]["fy"])[:4]
            items.append((t, _num(v), t == ticker))
        panels.append(bar_panel(title, items, kind))
    panels = [p for p in panels if p]
    if not panels:
        return ""
    fy = "、".join("{0} {1}".format(t, y) for t, y in fys.items())
    return ('<figure class="fig"><figcaption>同業對照</figcaption><div class="pgrid">' + "".join(panels) + "</div>"
            '<p class="note">各圖是各家最近一個會計年度（{0}）的數字，沒有數字的指標不畫；預估本益比是現價對 yfinance 預估每股盈餘。藍色是 {1}，灰色是同業。</p></figure>').format(esc(fy), esc(ticker))


# ------------------------------------------------------------ 獲利三檔圖
def cases_chart(cs, price):
    rows = R.cases3_rows(cs, price)
    rows = [r for r in rows if r["m"] is not None]
    if not rows:
        return ""
    W, rowh, padt, lw, rw = 640, 46, 8, 44, 90
    H = padt + rowh * len(rows) + 4
    mx = max(r["m"] for r in rows)
    tw = W - lw - rw
    s = ['<svg viewBox="0 0 {0} {1}" class="chart cp" role="img" aria-label="獲利三檔對應的本益比">'.format(W, H)]
    for k, r in enumerate(rows):
        yy = padt + rowh * k
        w = tw * r["m"] / mx
        sub = "每股盈餘 {0:,.2f}".format(float(r["eps"]))
        s.append('<text x="{0}" y="{1}" class="rn big" text-anchor="end">{2}</text>'.format(lw - 10, yy + 26, esc(r["label"])))
        s.append('<rect x="{0}" y="{1}" width="{2:.1f}" height="26" rx="4" class="b-t"><title>{3}｜{4:.1f} 倍</title></rect>'.format(lw, yy + 8, w, esc(r["label"]), r["m"]))
        s.append('<text x="{0:.1f}" y="{1}" class="rv t big">{2:.1f} 倍</text>'.format(lw + w + 8, yy + 27, r["m"]))
        s.append('<text x="{0}" y="{1}" class="bin">{2}</text>'.format(lw + 10, yy + 26, sub))
    s.append('<line x1="{0}" x2="{0}" y1="{1}" y2="{2}" class="zero"/>'.format(lw, padt, H - 4))
    s.append("</svg>")
    dl = "".join("<li><b>{0}</b><span>{1}{2}</span></li>".format(
        esc(r["label"]), esc(r["what"]),
        "<span class='dim'>　調整後每股盈餘 {0:,.2f}，{1:.1f} 倍</span>".format(float(r["adj"]), r["m_adj"]) if r["adj"] is not None and r["m_adj"] else "") for r in rows)
    return ('<figure class="fig"><figcaption>現價是各檔獲利的幾倍</figcaption>' + "".join(s) + '<ul class="cases">' + dl + "</ul></figure>")


# ------------------------------------------------------------ 頁首結論卡
DIR_ARROW = {"變好": "▲", "變強": "▲", "變壞": "▼", "變差": "▼", "變弱": "▼"}


def hero(machine, pack, calc, ex=None):
    price = pack["last_price"]
    cons = pack.get("consensus") or {}
    pe27 = price / float(cons["fy2"]) if cons.get("fy2") else None
    ttm = ((calc.get("multiples") or {}).get("now") or {}).get("pe")
    mo = machine.get("moat") or {}

    def cell(label, val, sub=""):
        arrow = DIR_ARROW.get(val, "")
        return ('<div class="cell"><div class="cl">{0}</div><div class="cv">{1}{2}</div>{3}</div>').format(
            esc(label), '<span class="ar">{0}</span>'.format(arrow) if arrow else "", esc(val), '<div class="cs">{0}</div>'.format(esc(sub)) if sub else "")
    stats = [("現價", "{0:,.2f}".format(price)), ("收盤日", pack["price_chart"]["last_date"])]
    if pe27:
        # 共識 FY2＝下一個會計年度；會計年度不在 12 月結束的公司（AMAT 10 月、KLAC 6 月）不能寫死成 2027
        lab27 = "下個會計年度預估本益比"
        try:
            import datetime as _dt
            import yfinance as _yf
            nfy = (_yf.Ticker(pack["ticker"]).info or {}).get("nextFiscalYearEnd")
            if nfy:
                e = _dt.datetime.utcfromtimestamp(nfy).date()
                if e.month == 1 and e.day <= 7:  # 52／53 週制（ONTO 結在 1 月初的星期六）視為 12 月年度
                    e = _dt.date(e.year - 1, 12, 31)
                lab27 = "{0} 預估本益比".format(e.year + 1) if e.month == 12 else "預估本益比（{0}-{1:02d} 結束的年度）".format(e.year + 1, e.month)
        except Exception:
            pass
        stats.append((lab27, "{0:.1f} 倍".format(pe27) if pe27 > 0 else "預估仍虧損"))
    if ttm:
        stats.append(("過去十二個月本益比", "{0:.1f} 倍".format(ttm) if ttm > 0 else "過去仍虧損"))
    hi = None
    if ex:
        try:
            import extras as _xt
            hi = _xt.header_item(ex)
        except Exception:
            hi = None
    if hi:
        stats.append((hi.get("label", ""), hi.get("value", "") + ("（{0}）".format(hi["note"]) if hi.get("note") else "")))
    st = "".join('<div class="st"><div class="sl">{0}</div><div class="sv">{1}</div></div>'.format(esc(a), esc(b)) for a, b in stats)
    return ('<section class="hero"><p class="one">{0}</p><div class="cells">{1}{2}{3}</div><div class="stats">{4}</div></section>').format(
        esc(machine.get("one_liner", "")),
        cell("生意方向", machine.get("business_direction", "—")),
        (cell("護城河寬度", mo.get("width"), mo.get("width_basis", "")) if mo.get("width") else "") +
        cell("護城河趨勢", mo.get("trend", "—"), mo.get("source", "")) +
        (cell("資本報酬趨勢", (machine.get("capital_return") or {}).get("trend", "—"), (machine.get("capital_return") or {}).get("evidence", ""))
         if machine.get("capital_return") else ""),
        cell("現價預設了什麼", "", machine.get("price_implies", "")).replace('<div class="cv"></div>', "").replace('class="cs"', 'class="cs long"').replace('class="cell"', 'class="cell wide"', 1),
        st)


# ------------------------------------------------------------ 組頁
CSS = r"""
:root{color-scheme:light;--bg:#fff;--bg2:#f5f6f8;--fg:#1b1d20;--mut:#5f6772;--line:#e2e5e9;--acc:#1d62b8;--s1:#257de0;--s2:#f47230;--other:#a9b0b9;--ok:#1a7a3c;--bad:#b3261e;--banner:#fff3bf;--bannerfg:#5c4700}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){color-scheme:dark;--bg:#14171a;--bg2:#1c2025;--fg:#ecedef;--mut:#9ca3ac;--line:#2d333a;--acc:#6aa9ee;--s1:#338ced;--s2:#e76624;--other:#5d6670;--ok:#52c27a;--bad:#ff7b72;--banner:#4a3d0b;--bannerfg:#ffe9a0}}
:root[data-theme=dark]{color-scheme:dark;--bg:#14171a;--bg2:#1c2025;--fg:#ecedef;--mut:#9ca3ac;--line:#2d333a;--acc:#6aa9ee;--s1:#338ced;--s2:#e76624;--other:#5d6670;--ok:#52c27a;--bad:#ff7b72;--banner:#4a3d0b;--bannerfg:#ffe9a0}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.85 -apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif;-webkit-text-size-adjust:100%}
.bar{position:sticky;top:var(--nh,0px);z-index:30;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar .in{max-width:1080px;margin:0 auto;padding:8px 16px;display:flex;align-items:center;gap:12px}
.bar .back{font-size:.85rem;text-decoration:none;white-space:nowrap}.bar .tk{font-weight:700;letter-spacing:.04em}.bar .sp{flex:1}
.bar button,.mtoc summary{font:inherit;font-size:.85rem;color:var(--fg);background:var(--bg2);border:1px solid var(--line);border-radius:8px;padding:4px 12px;cursor:pointer;line-height:1.6}
.mtoc{position:relative;display:none}.mtoc summary{list-style:none}.mtoc summary::-webkit-details-marker{display:none}
.mtoc .panel{position:absolute;left:0;top:calc(100% + 8px);width:min(300px,calc(100vw - 32px));background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:8px;box-shadow:0 8px 24px rgba(0,0,0,.18)}
.mtoc a{display:block;padding:7px 10px;border-radius:8px;color:var(--fg);text-decoration:none;font-size:.95rem}
.mtoc a.on{background:var(--bg2);color:var(--acc);font-weight:600}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px;display:grid;grid-template-columns:200px minmax(0,1fr);gap:48px}
.toc{position:sticky;top:calc(var(--nh,0px) + 64px);align-self:start;padding:36px 0;font-size:.88rem;max-height:calc(100vh - var(--nh,0px) - 80px);overflow:auto}
.toc .th{color:var(--mut);font-size:.75rem;letter-spacing:.12em;margin-bottom:8px}
.toc a{display:block;padding:5px 0 5px 12px;color:var(--mut);text-decoration:none;border-left:2px solid var(--line);line-height:1.5}
.toc a:hover{color:var(--fg)}.toc a.on{color:var(--acc);border-left-color:var(--acc);font-weight:600}
main{min-width:0;max-width:760px;padding:32px 0 96px}
h1{font-size:1.85rem;line-height:1.38;margin:.1em 0 .35em;letter-spacing:-.01em;font-weight:750}
.meta{color:var(--mut);font-size:.85rem;margin:0 0 20px}
h2{font-size:1.4rem;line-height:1.4;margin:2.4em 0 .6em;font-weight:720;scroll-margin-top:calc(var(--nh,0px) + 72px);display:flex;gap:.6em;align-items:baseline}
h2:before{content:"";flex:none;width:4px;height:1.05em;background:var(--acc);border-radius:2px;transform:translateY(.12em)}
h3{font-size:1.1rem;margin:1.6em 0 .3em}
p{margin:.85em 0}
a{color:var(--acc)}
ul,ol{padding-left:1.3em;margin:.8em 0}li{margin:.5em 0;padding-left:.2em}li::marker{color:var(--mut)}
p.mh{margin:1.7em 0 .2em;font-weight:700;font-size:1.02rem;color:var(--fg)}
.lead>b:first-child,li>b:first-child{font-weight:700;color:var(--fg)}
b{font-weight:680}
sup{font-size:.68em;line-height:0;vertical-align:super;margin-left:1px}
sup a{color:var(--mut);text-decoration:none;font-weight:500;padding:0 1px;opacity:.85}sup a:hover{color:var(--acc);opacity:1}
sup.bad{color:var(--bad)}
code{background:var(--bg2);padding:1px 5px;border-radius:4px;font-size:.88em}
blockquote{margin:1em 0;padding:.1em 1em;border-left:3px solid var(--acc);background:var(--bg2);border-radius:0 8px 8px 0}
.tw{overflow-x:auto;margin:1.1em 0;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.88rem;line-height:1.6;font-variant-numeric:tabular-nums}
th,td{padding:9px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
tr:last-child td{border-bottom:0}
th{background:var(--bg2);font-weight:650;color:var(--mut);font-size:.8rem;white-space:nowrap}
td.num,th.num{text-align:right;white-space:nowrap}
tbody tr:hover td{background:color-mix(in srgb,var(--bg2) 60%,transparent)}
.note{color:var(--mut);font-size:.86rem;line-height:1.7}.warn,.bad{color:var(--bad)}.ok{color:var(--ok)}
.hero{background:var(--bg2);border:1px solid var(--line);border-radius:16px;padding:22px 22px 18px;margin:0 0 8px}
.hero .one{font-size:1.2rem;line-height:1.7;font-weight:650;margin:0 0 18px}
.cells{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}.cell.wide{grid-column:1/-1}
.cell{background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.cl{font-size:.75rem;color:var(--mut);letter-spacing:.08em}
.cv{font-size:1.5rem;font-weight:750;line-height:1.4;margin-top:2px}.cv .ar{font-size:.8rem;color:var(--ok);margin-right:6px;vertical-align:.15em}
.cs{font-size:.84rem;line-height:1.65;color:var(--mut);margin-top:4px}.cs.long{margin-top:6px;color:var(--fg)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px;padding-top:14px;border-top:1px solid var(--line)}
.sl{font-size:.74rem;color:var(--mut)}.sv{font-size:1.25rem;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.5}
.fig{margin:1.6em 0;padding:16px 16px 10px;background:var(--bg);border:1px solid var(--line);border-radius:14px}
.fig figcaption{font-weight:700;font-size:.98rem;margin-bottom:8px}
.cbox{position:relative}.chart{width:100%;height:auto;display:block;overflow:visible}
.chart .grid{stroke:var(--line);stroke-width:1}.chart .ax{fill:var(--mut);font-size:11px}
.chart .px{fill:none;stroke:var(--fg);stroke-width:2;stroke-linejoin:round}.chart .ma10{fill:none;stroke:var(--s1);stroke-width:1.6}.chart .ma20{fill:none;stroke:var(--s2);stroke-width:1.6}
.chart .ath{stroke:var(--mut);stroke-dasharray:5 4;stroke-width:1.2}.chart .lab{fill:var(--fg);font-size:12px;font-weight:600}.chart .lab.mut{fill:var(--mut);font-weight:500}
.chart .dot{fill:var(--fg);stroke:var(--bg);stroke-width:2}.chart .xh{stroke:var(--mut);stroke-width:1}.chart .xd{fill:var(--fg);stroke:var(--bg);stroke-width:2}
.legend{font-size:.8rem;color:var(--mut);margin:.4em 0 .2em}.k{display:inline-block;width:18px;height:0;border-top:2px solid;vertical-align:middle;margin:0 6px 0 0}
.k.px{border-color:var(--fg)}.k.ma10{border-color:var(--s1)}.k.ma20{border-color:var(--s2)}.k.ath{border-top-style:dashed;border-color:var(--mut)}
.tip{position:absolute;pointer-events:none;background:var(--bg);border:1px solid var(--line);box-shadow:0 4px 14px rgba(0,0,0,.18);border-radius:8px;padding:6px 10px;font-size:.78rem;line-height:1.6;white-space:nowrap;z-index:5;font-variant-numeric:tabular-nums}
.pgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px 24px}
.bp .ptitle{fill:var(--mut);font-size:12px;font-weight:650}.bp .rn,.cp .rn{fill:var(--mut);font-size:12px}.cp .rn.big{font-size:15px;fill:var(--fg);font-weight:650}
.bp .rv,.cp .rv{fill:var(--mut);font-size:12px;font-variant-numeric:tabular-nums}.bp .rv.t,.cp .rv.t{fill:var(--fg);font-weight:700}.cp .rv.big{font-size:16px}
.b-t{fill:var(--s1)}.b-o{fill:var(--other)}.chart .zero{stroke:var(--mut);stroke-width:1}
.cp .bin{fill:#fff;font-size:13px;font-weight:600}
ul.cases{list-style:none;padding:0;margin:10px 0 4px;font-size:.88rem;line-height:1.7}ul.cases li{display:grid;grid-template-columns:2.2em 1fr;margin:.35em 0}ul.cases b{color:var(--acc)}.dim{color:var(--mut)}
details.raw{margin:1em 0;border:1px solid var(--line);border-radius:10px;padding:0 14px;background:var(--bg)}
details.raw>summary{cursor:pointer;padding:10px 0;font-size:.88rem;color:var(--mut);font-weight:600}
details.raw[open]>summary{border-bottom:1px solid var(--line);margin-bottom:6px}
.srcs{font-size:.8rem;color:var(--mut);padding-left:0;list-style:none;line-height:1.65}.srcs li{margin:.5em 0;display:grid;grid-template-columns:2em 1fr;padding:0}.sn{color:var(--acc);font-weight:600}.q{margin:.2em 0 0;grid-column:2}
.srcs a{color:var(--mut)}
@media (max-width:1000px){.wrap{display:block}.toc{display:none}.mtoc{display:block}main{padding-top:20px}}
@media (max-width:640px){
body{font-size:16px;line-height:1.85}h1{font-size:1.5rem}h2{font-size:1.25rem}
.cells{grid-template-columns:1fr 1fr}.cell.wide{grid-column:1/-1}
.stats{grid-template-columns:1fr 1fr}.hero{padding:16px}.hero .one{font-size:1.08rem}
.pgrid{grid-template-columns:1fr}.fig{padding:12px 12px 6px;border-radius:12px}
.chart.pc .ax{font-size:19px}.chart.pc .lab{font-size:20px}.cp .bin{font-size:14px}
th,td{padding:8px 9px}table.w4 td:not(.num){min-width:11em}table.w4 td:first-child:not(.num){min-width:6em}
}
"""

JS = r"""
(function(){
var root=document.documentElement;
function navh(){var n=document.querySelector('.imq-nav-root'),h=0;if(n&&getComputedStyle(n).position==='sticky')h=n.offsetHeight;root.style.setProperty('--nh',h+'px');return h}
navh();addEventListener('resize',navh);addEventListener('load',navh);
if(window.ResizeObserver){var _n=document.querySelector('.imq-nav-root');if(_n)new ResizeObserver(navh).observe(_n)}
function setTheme(t){root.setAttribute('data-theme',t);try{localStorage.setItem('dd5theme',t)}catch(e){}}
try{var s=localStorage.getItem('dd5theme');if(s)root.setAttribute('data-theme',s)}catch(e){}
document.getElementById('tt').addEventListener('click',function(){
 var cur=root.getAttribute('data-theme');
 if(!cur)cur=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';
 setTheme(cur==='dark'?'light':'dark');});
var hs=[].slice.call(document.querySelectorAll('main h2[id]'));
var links=[].slice.call(document.querySelectorAll('.toc a,.mtoc a'));
function spy(){var cur=hs[0];for(var i=0;i<hs.length;i++){if(hs[i].getBoundingClientRect().top<navh()+120)cur=hs[i];}
 links.forEach(function(a){a.classList.toggle('on',cur&&a.getAttribute('href')==='#'+cur.id)});}
addEventListener('scroll',spy,{passive:true});spy();
document.querySelectorAll('.mtoc a').forEach(function(a){a.addEventListener('click',function(){document.querySelector('.mtoc').open=false})});
document.querySelectorAll('figure.fig').forEach(function(f){
 var sc=f.querySelector('script.pcdata');if(!sc)return;
 var D=JSON.parse(sc.textContent),svg=f.querySelector('svg.pc'),tip=f.querySelector('.tip'),
  xh=svg.querySelector('.xh'),xd=svg.querySelector('.xd'),VW=+svg.dataset.w;
 function mv(e){var r=svg.getBoundingClientRect(),vx=(e.clientX-r.left)/r.width*VW,b=0,bd=1e9;
  for(var i=0;i<D.x.length;i++){var d=Math.abs(D.x[i]-vx);if(d<bd){bd=d;b=i}}
  var p=D.d[b],px=D.x[b],py=D.y[b];xh.setAttribute('x1',px);xh.setAttribute('x2',px);xh.style.display='';
  xd.setAttribute('cx',px);xd.setAttribute('cy',py);xd.style.display='';
  var fmt=function(v){return v==null?'—':v.toLocaleString('en-US',{maximumFractionDigits:1})};
  tip.innerHTML=p[0].slice(0,7)+'<br>收盤 '+fmt(p[1])+'<br>10 月線 '+fmt(p[2])+'　20 月線 '+fmt(p[3]);tip.hidden=false;
  var sx=px/VW*r.width,w=tip.offsetWidth;tip.style.left=Math.max(0,Math.min(r.width-w,sx+12))+'px';tip.style.top='4px';}
 function lv(){xh.style.display='none';xd.style.display='none';tip.hidden=true}
 svg.addEventListener('pointermove',mv);svg.addEventListener('pointerleave',lv);});
})();
"""



# ------------------------------------------------------------ 掛鉤：換掉 render.py 的表格與圖
def _details(summary, inner):
    return '<details class="raw"><summary>{0}</summary>{1}</details>'.format(summary, inner)


def _cases3(cs, price, price_date=None, *a, **k):
    raw = _orig["cases3_table"](cs, price, price_date, *a, **k)
    if cs.get("error"):
        return raw
    return cases_chart(cs, price) + _details("看原始表格：獲利三檔與現價倍數", raw)


def _price_svg(pc_):
    return price_chart(pc_)


def _collect_refs(text, *a, **k):
    """同業圖：放在「同業」小節之後（下一個粗體小標前），找不到就放在獲利三檔圖前。"""
    run = _CTX.get("run")
    peers = _CTX.get("peers") or {}
    if peers.get("data"):
        pm = (run / "peers.md").read_text(encoding="utf-8") if (run / "peers.md").exists() else ""
        blk = peers_chart(peers, _CTX.get("ticker", ""))
        if blk:
            blk += _details("看原始表格：同業財務與倍數", R.md_to_html(pm)) if pm else ""
            lines = text.split("\n")
            ins = None
            for i, ln in enumerate(lines):
                if re.match(r"^\*\*同業", ln):
                    j = i + 1
                    while j < len(lines) and (not lines[j].strip() or re.match(r"^\s*([-*]|\d+[.、])\s", lines[j])):
                        j += 1
                    ins = j  # 同業段落（含後面的條列）結束處
                    break
            if ins is None:
                for j, ln in enumerate(lines):
                    if "現價是各檔獲利" in ln or "<!--RAW" in ln and "現價是各檔獲利" in ln:
                        ins = j
                        break
            if ins is not None:
                lines.insert(ins, "<!--RAW" + blk.replace("\n", " ") + "-->")
                text = "\n".join(lines)
    return _orig["collect_refs"](text, *a, **k)


_orig = {}
_PATCH = {"table_html": table_html, "price_svg": _price_svg, "cases3_table": _cases3, "collect_refs": _collect_refs}


def _patch():
    for k, f in _PATCH.items():
        _orig[k] = getattr(R, k)
        setattr(R, k, f)


def _unpatch():
    for k in _PATCH:
        setattr(R, k, _orig[k])


# ------------------------------------------------------------ 組頁
def render(run, out=None, back_link=None):
    run = Path(run)
    pack = json.loads((run / "pack.json").read_text(encoding="utf-8"))
    machine = json.loads((run / "machine.json").read_text(encoding="utf-8"))
    _CTX.clear()
    _CTX.update(run=run, ticker=pack["ticker"],
                peers=json.loads((run / "peers.json").read_text(encoding="utf-8")) if (run / "peers.json").exists() else {})
    out = Path(out) if out else Path.home() / "dd5-pilot" / "preview" / "{0}_pretty".format(pack["ticker"]) / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    _patch()
    try:
        res = R.render(run, out=out)  # 不傳 back_link：回連結放在頂部列
    finally:
        _unpatch()
    old = out.read_text(encoding="utf-8")
    m = re.search(r'<article class="doc">(.*)</article>', old, re.S)
    inner = m.group(1) if m else old
    inner = re.sub(r'<p class="note"><a href="[^"]*">← 回個股儀表板</a></p>', "", inner)
    mt = re.match(r"\s*<h1>(.*?)</h1>(.*)", inner, re.S)
    title, rest = (mt.group(1), mt.group(2)) if mt else (esc(pack["ticker"]), inner)
    # 去掉舊版頁首（meta、方向標籤、一句話、現價預設、護城河），這些改放結論卡
    for pat in (r'\s*<p class="meta">.*?</p>', r'\s*<p><span class="tag">.*?</span></p>'):
        rest = re.sub("^" + pat, "", rest, count=1, flags=re.S)
    while True:
        r2 = re.sub(r'^\s*<p class="note">(?:<b>.*?</b>|現價預設了什麼：.*?|護城河：.*?)</p>', "", rest, count=1, flags=re.S)
        if r2 == rest:
            break
        rest = r2
    parts = rest.rsplit("<h2>來源</h2>", 1)
    body = parts[0]
    srcs = parts[1] if len(parts) == 2 else ""
    ex = json.loads((run / "extras.json").read_text(encoding="utf-8")) if (run / "extras.json").exists() else None
    if ex:  # 零 LLM 加掛模組（錢花到哪裡、現金轉換天數、利潤率走勢、共識修正），插在固定章節尾
        import extras as _xt
        body = _xt.insert(body, ex)
    body = re.sub(r"<p>\s*-{3,}\s*</p>", "", body)  # 正文裡殘留的分隔線標記
    body = re.sub(r"<p>(<b>[^<]{1,24}</b>)</p>", r'<p class="mh">\1</p>', body)
    body = re.sub(r"<p>(?=<b>)", '<p class="lead">', body)
    toc = []

    def h2(mm):
        k = len(toc) + 1
        toc.append((k, re.sub(r"<[^>]+>", "", mm.group(1))))
        return '<h2 id="s{0}">{1}</h2>'.format(k, mm.group(1))
    body = re.sub(r"<h2>(.*?)</h2>", h2, body)
    if srcs:
        k = len(toc) + 1
        toc.append((k, "來源"))
        body += '<h2 id="s{0}">來源</h2>{1}'.format(k, srcs)
    toc_links = "".join('<a href="#s{0}">{1}</a>'.format(i, esc(t)) for i, t in toc)
    calc = json.loads((run / "calc.json").read_text(encoding="utf-8"))
    price = pack["last_price"]
    last_date = (pack.get("price_chart") or {}).get("last_date", "")
    d = pack["date"]
    dd = "{0}-{1}-{2}".format(d[:4], d[4:6], d[6:8]) if len(d) == 8 else d
    back = '<a class="back" href="{0}">← 個股儀表板</a>'.format(esc(back_link)) if back_link else ""
    doc = ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
           '<title>{tk} 個股研究</title><style>{css}</style></head><body>'
           '<div class="bar"><div class="in"><details class="mtoc"><summary>目錄</summary><div class="panel">{toc}</div></details>'
           '{back}<span class="tk">{tk}</span><span class="sp"></span><button id="tt" type="button" aria-label="切換淺色或深色">淺／深</button></div></div>'
           '<div class="wrap"><nav class="toc" aria-label="目錄"><div class="th">目錄</div>{toc}</nav>'
           '<main><h1>{title}</h1><p class="meta">{tk}｜資料日 {dd}｜現價 {px:,.2f}（{ld} 收盤）｜精簡版</p>{hero}{body}</main></div>'
           '<script>{js}</script></body></html>').format(
        tk=esc(pack["ticker"]), css=CSS, toc=toc_links, back=back, title=title, dd=dd, px=price, ld=esc(last_date),
        hero=hero(machine, pack, calc, ex), body=body, js=JS)
    out.write_text(doc, encoding="utf-8")
    res["html"] = str(out)
    res["bytes"] = len(doc.encode())
    return res


if __name__ == "__main__":
    a = sys.argv[1:]
    o = bk = None
    for flag in ("--out", "--back"):
        if flag in a:
            i = a.index(flag)
            v = a[i + 1]
            del a[i:i + 2]
            if flag == "--out":
                o = v
            else:
                bk = v
    print(json.dumps(render(a[0], o, bk), ensure_ascii=False, indent=1))
