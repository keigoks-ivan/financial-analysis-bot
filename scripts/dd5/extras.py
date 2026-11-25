#!/usr/bin/env python3
"""dd5 加掛模組：程式算、程式畫、不經模型（零 LLM）。

build(ticker, run_dir) -> dict      抓 yfinance 財報與 dd-screener 欄位，寫 run_dir/extras.json
blocks(extras, section) -> html      section = "quality"（錢花到哪裡＋現金轉換天數）或 "valuation"（利潤率走勢＋共識修正）
insert(article_html, extras) -> html 把兩組區塊插到「獲利的品質」「估值」兩章的章尾（找不到標題就不插）
header_item(extras) -> dict|None     頁首結論卡的欄位：下次財報日與倒數天數

出處只有兩個：yfinance（年報、季報）、dd-screener 每日資料（docs/dd-screener/latest.json）。
不給買賣裁決、目標價、機率、技術面。

用法：python3 scripts/dd5/extras.py <代號> <run 目錄>
"""
from __future__ import annotations

import html as _html
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
SCREENER = HERE.parents[1] / "docs" / "dd-screener" / "latest.json"

CUR_NAME = {"USD": "美元", "TWD": "新台幣", "EUR": "歐元", "JPY": "日圓", "HKD": "港幣", "CNY": "人民幣", "KRW": "韓元", "GBP": "英鎊", "CHF": "瑞士法郎", "CAD": "加幣"}


def esc(s):
    return _html.escape(str(s), quote=True)


def _num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if (math.isnan(v) or math.isinf(v)) else v


def _row(df, names):
    """依序找第一個存在的列名，回傳 {欄位日期: 值}（NaN 略過）。"""
    if df is None or getattr(df, "empty", True):
        return {}
    for n in names:
        if n in df.index:
            s = df.loc[n]
            return {c: _num(v) for c, v in s.items() if _num(v) is not None}
    return {}


def _yi(v):
    return None if v is None else round(v / 1e8, 2)


# ---------------------------------------------------------------- 抓資料
def _screener(ticker):
    try:
        d = json.loads(SCREENER.read_text(encoding="utf-8"))
    except Exception:
        return {}, None
    for s in d.get("stocks", []):
        if s.get("ticker") == ticker:
            return s, d.get("as_of")
    return {}, d.get("as_of")


def _safe(fn):
    try:
        return fn()
    except Exception:
        return None


def build(ticker, run_dir):
    import warnings
    warnings.filterwarnings("ignore")
    import yfinance as yf
    from peers import is_financial

    t = yf.Ticker(ticker)
    info = _safe(lambda: t.info) or {}
    fin = bool(_safe(lambda: is_financial(info)))
    cur = info.get("financialCurrency") or info.get("currency") or "USD"
    unit = "億" + CUR_NAME.get(cur, cur)
    sc, sc_asof = _screener(ticker)
    out = {"ticker": ticker, "currency": cur, "unit": unit, "is_financial": fin,
           "sources": {"financials": "yfinance（年報、季報）", "screener": "dd-screener 每日資料（docs/dd-screener/latest.json）"},
           "screener_as_of": sc_asof, "skipped": {}}

    inc = _safe(lambda: t.income_stmt)
    cf = _safe(lambda: t.cashflow)
    bs = _safe(lambda: t.balance_sheet)
    qinc = _safe(lambda: t.quarterly_income_stmt)

    # ---- 錢花到哪裡（年度）
    rev = _row(inc, ["Total Revenue", "Operating Revenue"])
    ocf = _row(cf, ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"])
    capex = _row(cf, ["Capital Expenditure", "Purchase Of PPE"])
    fcf = _row(cf, ["Free Cash Flow"])
    buyb = _row(cf, ["Repurchase Of Capital Stock", "Common Stock Payments"])
    divi = _row(cf, ["Cash Dividends Paid", "Common Stock Dividend Paid"])
    acq = _row(cf, ["Purchase Of Business", "Acquisitions Net", "Net Business Purchase And Sale"])
    sbc = _row(cf, ["Stock Based Compensation"])
    shs = _row(inc, ["Diluted Average Shares"])
    dates = sorted(set(ocf) | set(rev))
    rows = []
    for i, d in enumerate(dates):
        if d not in ocf and d not in rev:
            continue
        o, cx = ocf.get(d), capex.get(d)
        f = fcf.get(d)
        if f is None and o is not None and cx is not None:
            f = o + cx  # yfinance 的資本支出是負數
        prev = dates[i - 1] if i else None
        chg = None
        if prev is not None and shs.get(d) and shs.get(prev):
            chg = round((shs[d] / shs[prev] - 1) * 100, 2)
        r_ = rev.get(d)
        rows.append({
            "year": d.strftime("%Y-%m"), "revenue": _yi(r_), "ocf": _yi(o), "capex": _yi(abs(cx)) if cx is not None else None,
            "fcf": _yi(f), "buyback": _yi(abs(buyb[d])) if d in buyb else None, "dividend": _yi(abs(divi[d])) if d in divi else None,
            "acquisition": _yi(abs(acq[d])) if d in acq else None, "sbc": _yi(sbc.get(d)),
            "sbc_pct_rev": round(sbc[d] / r_ * 100, 2) if d in sbc and r_ else None,
            "diluted_shares_yi": round(shs[d] / 1e8, 3) if d in shs else None, "share_change_pct": chg,
        })
    if fin:  # 銀行的營運現金流含交易資產進出，常出現大幅負值，不能當「賺進的現金」看
        for r in rows:
            r["ocf"] = r["fcf"] = r["capex"] = None
        out["skipped"]["ocf"] = "銀行、保險、券商的營運現金流含交易資產與存放款進出，不列營運現金流、資本支出與自由現金流"
    out["spend"] = rows[-4:]
    out["spend_screener"] = {"buyback_fcf_pct": sc.get("buyback_fcf_pct"), "sbc_dilution_pct_yr": sc.get("sbc_dilution_pct_yr"),
                             "sbc_pct_rev": sc.get("sbc_pct_rev"), "capex_fcf_pct": sc.get("capex_fcf_pct"),
                             "note": "dd-screener 口徑：回購占自由現金流％、股票薪酬造成的年稀釋％（dd-screener 自己的算法，與左表以財報股數算的不同）"}

    # ---- 利潤率走勢（季度，有幾季給幾季）
    qrev = _row(qinc, ["Total Revenue", "Operating Revenue"])
    qgp = _row(qinc, ["Gross Profit"])
    qcogs = _row(qinc, ["Cost Of Revenue", "Reconciled Cost Of Revenue"])
    qop = _row(qinc, ["Operating Income", "Total Operating Income As Reported"])
    op_label = "營益率"
    if not qop and fin:  # 銀行季報沒有營業利益，改用稅前利潤率
        qop, op_label = _row(qinc, ["Pretax Income"]), "稅前利潤率"
    marg = []
    for d in sorted(qrev):
        r_ = qrev[d]
        if not r_ or r_ <= 0:
            continue
        gp = qgp.get(d)
        if gp is None and d in qcogs:
            gp = r_ - qcogs[d]
        gm = None if fin or gp is None else round(gp / r_ * 100, 2)
        om = round(qop[d] / r_ * 100, 2) if d in qop else None
        if gm is None and om is None:
            continue
        marg.append({"period": d.strftime("%Y-%m"), "gross_margin_pct": gm, "op_margin_pct": om})
    out["margins"] = marg[-8:]
    out["op_label"] = op_label
    if fin:
        out["skipped"]["gross_margin"] = "銀行、保險、券商沒有毛利的概念，不列毛利率"
    if not marg:
        out["skipped"]["margins"] = "yfinance 沒有季報損益表"

    # ---- 共識修正（dd-screener）
    cons = {
        "d1m": sc.get("eps_revision_pct"), "d1m_base": sc.get("eps_revision_baseline_date"),
        "d3m": sc.get("eps_rev_3m_pct"), "d3m_base": sc.get("eps_rev_3m_baseline_date"),
        "since_earnings": sc.get("eps_rev_since_earnings_pct"), "since_earnings_base": sc.get("eps_rev_since_earnings_baseline_date"),
        "next_earnings_date": sc.get("next_earnings_date"), "days_to_next_earnings": sc.get("days_to_next_earnings"),
        "currency_normalized": sc.get("eps_revision_fx_normalized"), "source": "dd-screener（Koyfin 每股盈餘預估快照）", "as_of": sc_asof,
    }
    out["consensus"] = cons if sc else {}
    if not sc:
        out["skipped"]["consensus"] = "不在 dd-screener 名單，沒有共識修正與下次財報日"

    # ---- 現金轉換天數（年度）
    if fin:
        out["ccc"] = []
        out["skipped"]["ccc"] = "銀行、保險、券商的應收、存貨、應付不是營運資金，現金轉換天數不適用"
    else:
        ar = _row(bs, ["Accounts Receivable", "Receivables"])
        inv = _row(bs, ["Inventory"])
        ap = _row(bs, ["Accounts Payable", "Payables"])
        cogs = _row(inc, ["Cost Of Revenue", "Reconciled Cost Of Revenue"])
        ccc = []
        for d in sorted(rev):
            r_, c_ = rev.get(d), cogs.get(d)
            if not r_ or r_ <= 0:
                continue
            dso = ar[d] / r_ * 365 if d in ar else None
            dio = inv[d] / c_ * 365 if (d in inv and c_ and c_ > 0) else (0.0 if d not in inv and c_ else None)
            dpo = ap[d] / c_ * 365 if (d in ap and c_ and c_ > 0) else None
            if dso is None and dio is None and dpo is None:
                continue
            tot = None if (dso is None or dpo is None or dio is None) else dso + dio - dpo
            ccc.append({"year": d.strftime("%Y-%m"), "dso": _r1(dso), "dio": _r1(dio), "dpo": _r1(dpo), "ccc": _r1(tot),
                        "no_inventory": d not in inv})
        out["ccc"] = ccc[-4:]
        if not ccc:
            out["skipped"]["ccc"] = "yfinance 沒有年度資產負債表的應收、存貨或應付"
    out["ccc_screener"] = {"ccc_days": sc.get("ccc_days"), "note": "dd-screener 的口徑（可能用近四季或不同的分母），與左表年底餘額算法不同"}
    out["method"] = "應收天數＝年底應收÷營收×365；存貨天數、應付天數＝年底餘額÷營業成本×365；現金轉換天數＝應收＋存貨－應付"

    Path(run_dir, "extras.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def _r1(v):
    return None if v is None else round(v, 1)


# ---------------------------------------------------------------- 畫圖
STYLE = """<style>
.xt{--xs1:#257de0;--xs2:#f47230;--xs3:#1a9a8a;--xs4:#a9b0b9;--xneg:#b3261e;margin:1.4em 0}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .xt{--xs1:#338ced;--xs2:#e76624;--xs3:#2fb8a6;--xs4:#5d6670;--xneg:#ff7b72}}
:root[data-theme=dark] .xt{--xs1:#338ced;--xs2:#e76624;--xs3:#2fb8a6;--xs4:#5d6670;--xneg:#ff7b72}
.xt h4{margin:0 0 .3em;font-size:1.02rem;font-weight:700;color:var(--fg,#1b1d20)}
.xt .xsub{margin:.1em 0 .4em;font-size:.85rem;color:var(--mut,#5f6772);line-height:1.6}
.xt svg{display:block;width:100%;height:auto}
.xt .g{stroke:var(--line,#e2e5e9);stroke-width:1}.xt .z{stroke:var(--mut,#5f6772);stroke-width:1}
.xt text{fill:var(--mut,#5f6772);font-size:11px;font-family:inherit}.xt text.v{fill:var(--fg,#1b1d20);font-weight:600}
.xt .c1{fill:var(--xs1)}.xt .c2{fill:var(--xs2)}.xt .c3{fill:var(--xs3)}.xt .c4{fill:var(--xs4)}
.xt .l1{stroke:var(--xs1);fill:none;stroke-width:2.2}.xt .l2{stroke:var(--xs2);fill:none;stroke-width:2.2}
.xt .d1{fill:var(--xs1)}.xt .d2{fill:var(--xs2)}
.xt .tk{stroke:var(--fg,#1b1d20);stroke-width:2.4}
.xt .lg{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:.82rem;color:var(--mut,#5f6772);margin:.3em 0}
.xt .lg i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:baseline}
.xt .lg i.ln{height:3px;vertical-align:middle;border-radius:0}
.xt .lg i.c1{background:var(--xs1)}.xt .lg i.c2{background:var(--xs2)}.xt .lg i.c3{background:var(--xs3)}.xt .lg i.c4{background:var(--xs4)}.xt .lg i.tkk{background:var(--fg,#1b1d20);height:3px;vertical-align:middle}
.xt details{margin:.4em 0}.xt summary{cursor:pointer;font-size:.85rem;color:var(--acc,#1d62b8)}
.xt table{border-collapse:collapse;width:100%;font-size:.84rem;font-variant-numeric:tabular-nums}
.xt th,.xt td{padding:6px 10px;text-align:right;border-bottom:1px solid var(--line,#e2e5e9);white-space:nowrap}
.xt th:first-child,.xt td:first-child{text-align:left}.xt th{background:var(--bg2,var(--card,#f5f6f8));font-weight:600}
.xt .tw{overflow-x:auto;margin:.5em 0;border:1px solid var(--line,#e2e5e9);border-radius:10px}
.xt .src{font-size:.78rem;color:var(--mut,#5f6772);margin:.3em 0 0;line-height:1.6}
.xt .neg{color:var(--xneg)}
</style>"""


def _nice(lo, hi, n=4):
    if hi == lo:
        hi = lo + 1
    span = hi - lo
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    step = min((m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw), default=mag)
    a = math.floor(lo / step) * step
    b = math.ceil(hi / step) * step
    ticks, v = [], a
    while v <= b + step * 1e-6:
        ticks.append(round(v, 10))
        v += step
    return a, b, ticks


def _fmt(v, d=None):
    if v is None:
        return "—"
    if d is None:
        d = 0 if abs(v) >= 100 else 1 if abs(v) >= 10 else 2
    return "{:,.{d}f}".format(v, d=d).replace("-", "−")


def _pct(v, d=1, sign=False):
    if v is None:
        return "—"
    s = "{:+.{d}f}%".format(v, d=d) if sign else "{:.{d}f}%".format(v, d=d)
    return s.replace("-", "−")


def _short(period):  # 2026-09 -> 26/09
    return period[2:4] + "/" + period[5:7] if len(period) >= 7 else period


def _spend_chart(rows, unit):
    W, H, L, R, T, B = 640, 270, 54, 14, 18, 30
    uses = []
    for r in rows:
        stack = [r.get("capex") or 0, r.get("buyback") or 0, r.get("dividend") or 0, r.get("acquisition") or 0]
        uses.append(stack)
    vals = [sum(u) for u in uses] + [r["ocf"] for r in rows if r.get("ocf") is not None] + [0]
    a, b, ticks = _nice(min(vals), max(vals))
    ys = lambda v: T + (b - v) / (b - a) * (H - T - B)
    cw = (W - L - R) / len(rows)
    bw = min(cw * 0.5, 70)
    p = ['<svg viewBox="0 0 {0} {1}" role="img" aria-label="近四年資金用途與營運現金流">'.format(W, H)]
    for tv in ticks:
        p.append('<line class="{0}" x1="{1}" x2="{2}" y1="{3:.1f}" y2="{3:.1f}"/><text x="{4}" y="{5:.1f}" text-anchor="end">{6}</text>'.format(
            "z" if tv == 0 else "g", L, W - R, ys(tv), L - 6, ys(tv) + 4, _fmt(tv, 0)))
    for i, (r, st) in enumerate(zip(rows, uses)):
        cx = L + cw * (i + 0.5)
        for k, v in enumerate(st):
            if v <= 0:
                continue
            y1 = ys(sum(st[:k + 1]))
            h = ys(sum(st[:k])) - y1
            p.append('<rect class="c{0}" x="{1:.1f}" y="{2:.1f}" width="{3:.1f}" height="{4:.1f}" rx="2"/>'.format(
                [2, 1, 3, 4][k], cx - bw / 2, y1, bw, max(h, 0.5)))
        if r.get("ocf") is not None:
            p.append('<line class="tk" x1="{0:.1f}" x2="{1:.1f}" y1="{2:.1f}" y2="{2:.1f}"/>'.format(cx - bw / 2 - 8, cx + bw / 2 + 8, ys(r["ocf"])))
        p.append('<text x="{0:.1f}" y="{1}" text-anchor="middle">{2}</text>'.format(cx, H - 10, esc(r["year"][:4] + "年")))
        tot = sum(st)
        p.append('<text class="v" x="{0:.1f}" y="{1:.1f}" text-anchor="middle">{2}</text>'.format(cx, ys(max(tot, r.get("ocf") or 0)) - 6, _fmt(tot, 0)))
    p.append("</svg>")
    return "".join(p)


def _spend_table(rows, unit, fin=False):
    hd = ["年度", "營運現金流", "資本支出", "自由現金流", "回購", "股息", "併購", "股票薪酬", "股票薪酬占營收", "稀釋股數年變化"]
    keys = ["ocf", "capex", "fcf", "buyback", "dividend", "acquisition", "sbc"]
    if fin:
        hd = [h for h in hd if h not in ("營運現金流", "資本支出", "自由現金流")]
        keys = ["buyback", "dividend", "acquisition", "sbc"]
    t = ['<div class="tw"><table><thead><tr>' + "".join("<th>{0}</th>".format(h) for h in hd) + "</tr></thead><tbody>"]
    for r in rows:
        cells = ["<td>{0}</td>".format(esc(r["year"][:4]))]
        for k in keys:
            v = r.get(k)
            cells.append('<td{0}>{1}</td>'.format(' class="neg"' if (v is not None and v < 0) else "", _fmt(v)))
        cells.append("<td>{0}</td>".format(_pct(r.get("sbc_pct_rev"))))
        cells.append("<td>{0}</td>".format(_pct(r.get("share_change_pct"), 1, True)))
        t.append("<tr>" + "".join(cells) + "</tr>")
    t.append("</tbody></table></div>")
    return "".join(t)


def block_spend(ex):
    rows = [r for r in ex.get("spend", []) if r.get("ocf") is not None or r.get("buyback") is not None or r.get("dividend") is not None]
    if len(rows) < 2:
        return ""
    unit = ex["unit"]
    fin = bool(ex.get("is_financial"))
    ss = ex.get("spend_screener") or {}
    lg = ('<div class="lg">{0}<span><i class="c1"></i>回購</span><span><i class="c3"></i>股息</span>'
          '<span><i class="c4"></i>併購</span>{1}</div>').format('' if fin else '<span><i class="c2"></i>資本支出</span>', '' if fin else '<span><i class="tkk"></i>營運現金流（黑線）</span>')
    last = rows[-1]
    bits = []
    if last.get("share_change_pct") is not None and last.get("sbc_pct_rev") is not None:
        bits.append("{0} 年稀釋股數{1}{2}，同年股票薪酬占營收 {3}".format(
            esc(last["year"][:4]), "增加" if last["share_change_pct"] > 0 else "減少", _pct(abs(last["share_change_pct"])), _pct(last["sbc_pct_rev"])))
    if ss.get("buyback_fcf_pct") is not None:
        bits.append("dd-screener 算的回購占自由現金流 {0}".format(_pct(ss["buyback_fcf_pct"])))
    if ss.get("sbc_dilution_pct_yr") is not None:
        bits.append("股票薪酬年稀釋 {0}".format(_pct(ss["sbc_dilution_pct_yr"], 1, True)))
    sub = "；".join(bits) + "。" if bits else ""
    return ('<div class="xt"><h4>錢花到哪裡</h4><p class="xsub">近四個會計年度，單位{0}。{6}{1}</p>{2}{3}'
            '<details><summary>看數字</summary>{4}</details>'
            '<p class="src">出處：yfinance 年度現金流量表與損益表；稀釋股數用損益表的稀釋加權平均股數；回購占自由現金流、年稀釋％為 dd-screener（{5}）。</p></div>').format(
        esc(unit), esc(sub), lg, _spend_chart(rows, unit), _spend_table(rows, unit, fin), esc(ex.get("screener_as_of") or "—"),
        "柱高是回購、股息、併購合計。銀行的營運現金流含交易資產進出，不列。" if fin else "柱高是資本支出、回購、股息、併購合計；黑線是營運現金流，柱高過黑線代表花的比賺的多。")


def block_ccc(ex):
    rows = [r for r in ex.get("ccc", []) if r.get("ccc") is not None]
    if len(rows) < 2:
        return ""
    W, H, L, R, T, B = 640, 200, 54, 14, 22, 30
    vals = [r["ccc"] for r in rows] + [0]
    a, b, ticks = _nice(min(vals), max(vals), 3)
    ys = lambda v: T + (b - v) / (b - a) * (H - T - B)
    cw = (W - L - R) / len(rows)
    bw = min(cw * 0.45, 64)
    p = ['<svg viewBox="0 0 {0} {1}" role="img" aria-label="近四年現金轉換天數">'.format(W, H)]
    for tv in ticks:
        p.append('<line class="{0}" x1="{1}" x2="{2}" y1="{3:.1f}" y2="{3:.1f}"/><text x="{4}" y="{5:.1f}" text-anchor="end">{6}</text>'.format(
            "z" if tv == 0 else "g", L, W - R, ys(tv), L - 6, ys(tv) + 4, _fmt(tv, 0)))
    for i, r in enumerate(rows):
        cx = L + cw * (i + 0.5)
        v = r["ccc"]
        y1, y0 = ys(max(v, 0)), ys(min(v, 0))
        p.append('<rect class="c1" x="{0:.1f}" y="{1:.1f}" width="{2:.1f}" height="{3:.1f}" rx="2"/>'.format(cx - bw / 2, y1, bw, max(y0 - y1, 0.5)))
        p.append('<text class="v" x="{0:.1f}" y="{1:.1f}" text-anchor="middle">{2}</text>'.format(cx, (y1 - 6) if v >= 0 else (y0 + 14), _fmt(v, 0) + " 天"))
        p.append('<text x="{0:.1f}" y="{1}" text-anchor="middle">{2}</text>'.format(cx, H - 10, esc(r["year"][:4] + "年")))
    p.append("</svg>")
    hd = ["年度", "應收天數", "存貨天數", "應付天數", "現金轉換天數"]
    t = ['<div class="tw"><table><thead><tr>' + "".join("<th>{0}</th>".format(h) for h in hd) + "</tr></thead><tbody>"]
    for r in rows:
        t.append("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>".format(
            esc(r["year"][:4]), _fmt(r["dso"], 0), "—" if r.get("no_inventory") else _fmt(r["dio"], 0), _fmt(r["dpo"], 0), _fmt(r["ccc"], 0)))
    t.append("</tbody></table></div>")
    sc = (ex.get("ccc_screener") or {}).get("ccc_days")
    cmp_ = "；dd-screener 另算的現金轉換天數為 {0} 天（口徑不同，只作對照）".format(_fmt(sc, 0)) if sc is not None else ""
    last, first = rows[-1], rows[0]
    trend = "{0} 年 {1} 天，{2} 年 {3} 天".format(first["year"][:4], _fmt(first["ccc"], 0), last["year"][:4], _fmt(last["ccc"], 0))
    inv_note = "沒有存貨的行業，存貨天數不列。" if any(r.get("no_inventory") for r in rows) else ""
    return ('<div class="xt"><h4>現金轉換天數</h4><p class="xsub">從付錢給供應商到收到客戶的錢，要等多少天；數字越大，營運資金壓得越久。{0}{1}。{2}</p>{3}'
            '<details><summary>看數字</summary>{4}</details>'
            '<p class="src">出處：yfinance 年度資產負債表與損益表。應收天數＝年底應收÷營收×365；存貨、應付天數＝年底餘額÷營業成本×365；現金轉換天數＝應收＋存貨－應付。{5}</p></div>').format(
        esc(trend), esc(cmp_), esc(inv_note), "".join(p), "".join(t), "")


def block_margins(ex):
    rows = ex.get("margins") or []
    if len(rows) < 2:
        return ""
    W, H, L, R, T, B = 640, 230, 46, 124, 16, 30
    gm = [(i, r["gross_margin_pct"]) for i, r in enumerate(rows) if r.get("gross_margin_pct") is not None]
    om = [(i, r["op_margin_pct"]) for i, r in enumerate(rows) if r.get("op_margin_pct") is not None]
    vals = [v for _, v in gm + om] + [0]
    a, b, ticks = _nice(min(vals), max(vals))
    ys = lambda v: T + (b - v) / (b - a) * (H - T - B)
    n = len(rows)
    xs = lambda i: L + (W - L - R) * (i / (n - 1))
    p = ['<svg viewBox="0 0 {0} {1}" role="img" aria-label="近幾季毛利率與營益率">'.format(W, H)]
    for tv in ticks:
        p.append('<line class="{0}" x1="{1}" x2="{2}" y1="{3:.1f}" y2="{3:.1f}"/><text x="{4}" y="{5:.1f}" text-anchor="end">{6}%</text>'.format(
            "z" if tv == 0 else "g", L, W - R, ys(tv), L - 6, ys(tv) + 4, _fmt(tv, 0)))
    for i, r in enumerate(rows):
        if n <= 8 or i % 2 == (n - 1) % 2:
            p.append('<text x="{0:.1f}" y="{1}" text-anchor="middle">{2}</text>'.format(xs(i), H - 10, esc(_short(r["period"]))))
    for pts, cl, name in ((gm, 1, "毛利率"), (om, 2, ex.get("op_label") or "營益率")):
        if not pts:
            continue
        p.append('<polyline class="l{0}" points="{1}"/>'.format(cl, " ".join("{0:.1f},{1:.1f}".format(xs(i), ys(v)) for i, v in pts)))
        for i, v in pts:
            p.append('<circle class="d{0}" cx="{1:.1f}" cy="{2:.1f}" r="3"/>'.format(cl, xs(i), ys(v)))
        i, v = pts[-1]
        p.append('<text class="v" x="{0:.1f}" y="{1:.1f}">{2} {3}</text>'.format(xs(i) + 8, ys(v) + 4, name, _pct(v)))
    p.append("</svg>")
    opl = ex.get("op_label") or "營益率"
    hd = ["季度（期末）", "毛利率", opl]
    t = ['<div class="tw"><table><thead><tr>' + "".join("<th>{0}</th>".format(h) for h in hd) + "</tr></thead><tbody>"]
    for r in rows:
        t.append("<tr><td>{0}</td><td>{1}</td><td{2}>{3}</td></tr>".format(
            esc(r["period"]), _pct(r.get("gross_margin_pct")), ' class="neg"' if (r.get("op_margin_pct") or 0) < 0 else "", _pct(r.get("op_margin_pct"))))
    t.append("</tbody></table></div>")
    lg = '<div class="lg">{0}<span><i class="ln c2"></i>{1}</span></div>'.format('<span><i class="ln c1"></i>毛利率</span>' if gm else "", esc(opl))
    skip = (ex.get("skipped") or {}).get("gross_margin")
    return ('<div class="xt"><h4>利潤率走勢</h4><p class="xsub">近 {0} 季，每季損益表算出的{5}。{1}</p>{2}{3}<details><summary>看數字</summary>{4}</details>'
            '<p class="src">出處：yfinance 季度損益表；毛利率＝毛利÷營收，{6}。</p></div>').format(
        n, esc(skip + "。") if skip else "", lg, "".join(p), "".join(t), "毛利率與" + opl if gm else opl, "營益率＝營業利益÷營收" if opl == "營益率" else "稅前利潤率＝稅前利潤÷營收（銀行季報沒有營業利益）")


def block_consensus(ex):
    c = ex.get("consensus") or {}
    items = [("近一個月", c.get("d1m"), c.get("d1m_base")), ("近三個月", c.get("d3m"), c.get("d3m_base")), ("上次財報後", c.get("since_earnings"), c.get("since_earnings_base"))]
    if all(v is None for _, v, _ in items):
        return ""
    W, L, R = 640, 118, 70
    rowh, T = 40, 12
    H = T + rowh * 3 + 8
    vals = [abs(v) for _, v, _ in items if v is not None]
    m = max(max(vals), 1.0)
    a, b, _ = _nice(-m, m, 2)
    xs = lambda v: L + (v - a) / (b - a) * (W - L - R)
    p = ['<svg viewBox="0 0 {0} {1}" role="img" aria-label="共識每股盈餘預估的修正幅度">'.format(W, H)]
    p.append('<line class="z" x1="{0:.1f}" x2="{0:.1f}" y1="{1}" y2="{2}"/>'.format(xs(0), T - 4, H - 4))
    for k, (name, v, base) in enumerate(items):
        y = T + rowh * k
        p.append('<text x="{0}" y="{1}" text-anchor="end">{2}</text>'.format(L - 10, y + 18, esc(name)))
        if base:
            p.append('<text x="{0}" y="{1}" text-anchor="end" style="font-size:10px">對比 {2}</text>'.format(L - 10, y + 31, esc(base[5:] if len(base) >= 10 else base)))
        if v is None:
            p.append('<text x="{0:.1f}" y="{1}">—</text>'.format(xs(0) + 8, y + 22))
            continue
        x0, x1 = sorted((xs(0), xs(v)))
        p.append('<rect class="{0}" x="{1:.1f}" y="{2}" width="{3:.1f}" height="18" rx="2"/>'.format("c1" if v >= 0 else "c2", x0, y + 6, max(x1 - x0, 1.5)))
        tx = x1 + 6 if v >= 0 else x0 - 6
        p.append('<text class="v" x="{0:.1f}" y="{1}" text-anchor="{2}">{3}</text>'.format(tx, y + 20, "start" if v >= 0 else "end", _pct(v, 1, True)))
    p.append("</svg>")
    ne = ""
    if c.get("next_earnings_date"):
        d = c.get("days_to_next_earnings")
        ne = "下次財報日 {0}{1}。".format(esc(c["next_earnings_date"]), "（{0} 天後）".format(d) if d is not None else "")
    lg = '<div class="lg"><span><i class="c1"></i>預估上修</span><span><i class="c2"></i>預估下修</span></div>'
    return ('<div class="xt"><h4>共識預期的修正</h4><p class="xsub">分析師對今年度每股盈餘的平均預估，比起三個基準日的變化。{0}</p>{1}{2}'
            '<p class="src">出處：dd-screener（Koyfin 預估快照，{3}）。只描述預估怎麼動，不是對股價的判斷。{4}</p></div>').format(
        ne, lg, "".join(p), esc(c.get("as_of") or "—"), "")


# ---------------------------------------------------------------- 介面
def blocks(extras, section):
    """section: 'quality'＝錢花到哪裡＋現金轉換天數；'valuation'＝利潤率走勢＋共識修正。沒資料的區塊不輸出。"""
    if not extras:
        return ""
    if section == "quality":
        parts = [block_spend(extras), block_ccc(extras)]
    elif section == "valuation":
        parts = [block_margins(extras), block_consensus(extras)]
    else:
        raise ValueError(section)
    return "".join(p for p in parts if p)


def header_item(extras):
    c = (extras or {}).get("consensus") or {}
    if not c.get("next_earnings_date"):
        return None
    d = c.get("days_to_next_earnings")
    return {"label": "下次財報", "value": c["next_earnings_date"], "note": "還有 {0} 天".format(d) if d is not None else "", "source": "dd-screener"}


def _after_chapter(h, title, add):
    """把 add 插在標題為 title 的 h2 那一章章尾（下一個 h2 之前；沒有下一個 h2 就在 </main> 或文末前）。"""
    m = re.search(r"<h2[^>]*>\s*" + re.escape(title) + r"\s*</h2>", h)
    if not m or not add:
        return h, False
    n = re.search(r"<h2[ >]", h[m.end():])
    if n:
        pos = m.end() + n.start()
    else:
        e = re.search(r"</main>|</article>", h[m.end():])
        pos = m.end() + e.start() if e else len(h)
    return h[:pos] + add + h[pos:], True


def insert(article_html, extras):
    """article_html：正文 HTML（含 <h2>獲利的品質</h2>、<h2>估值</h2>）。回傳插入後的 HTML；章節名稱找不到就略過該組。
    樣式（STYLE）只在有任何區塊插入時加一份，放在第一個區塊前。"""
    h = article_html
    q, v = blocks(extras, "quality"), blocks(extras, "valuation")
    h, ok1 = _after_chapter(h, "獲利的品質", q)
    h, ok2 = _after_chapter(h, "估值", v)
    if ok1 or ok2:
        i = h.find('<div class="xt">')
        h = h[:i] + STYLE + h[i:]
    return h


if __name__ == "__main__":
    ex = build(sys.argv[1], sys.argv[2])
    print(json.dumps({k: (v if k in ("ticker", "unit", "is_financial", "skipped") else "…") for k, v in ex.items()}, ensure_ascii=False))
