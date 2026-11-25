#!/usr/bin/env python3
"""dd5 第 5 步：算與排版（零 LLM）。

讀 run 目錄的 pack.json／pack.md／ask.json／lookups.json／article.md／machine.json，
算情境估值、畫表與圖、換掉佔位記號與引用標記、做數字出處檢查、輸出單檔 HTML。
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

PILOT = Path.home() / "dd5-pilot"


def esc(s):
    return html.escape(str(s), quote=True)


# ------------------------------------------------------------ 估值計算
def target_price(sc):
    eps, mult, basis = float(sc.get("eps") or 0), float(sc.get("multiple") or 0), sc.get("basis") or "eps_pe"
    if basis == "fcf_yield":
        y = mult / 100.0 if mult > 1 else mult
        return eps / y if y else None
    return eps * mult  # eps_pe、sales_multiple：每股指標 × 倍數


def compute(machine, price):
    h = float(machine.get("horizon_years") or 3)
    div = float(machine.get("annual_dividend_per_share") or 0)
    out = {"horizon": h, "price": price, "div": div, "rows": {}}
    psum = 0.0
    for k in ("bear", "base", "bull"):
        sc = machine["scenarios"][k]
        tp = target_price(sc)
        total = tp + div * h
        ret = tp / price - 1
        tot_ret = total / price - 1
        ann = (total / price) ** (1 / h) - 1 if total > 0 else None
        out["rows"][k] = {"prob": float(sc["prob"]), "eps": sc.get("eps"), "multiple": sc.get("multiple"), "basis": sc.get("basis"),
                          "target": tp, "ret": ret, "tot_ret": tot_ret, "ann": ann, "driver": sc.get("driver", "")}
        psum += float(sc["prob"])
    out["prob_sum"] = psum
    ev_tp = sum(r["prob"] * r["target"] for r in out["rows"].values())
    ev_total = ev_tp + div * h
    out["ev_target"] = ev_tp
    out["ev_ret"] = ev_tp / price - 1
    out["ev_tot_ret"] = ev_total / price - 1
    out["ev_ann"] = (ev_total / price) ** (1 / h) - 1 if ev_total > 0 else None
    bull, bear = out["rows"]["bull"]["tot_ret"], out["rows"]["bear"]["tot_ret"]
    out["updown"] = (bull / abs(bear)) if bear < 0 and bull > 0 else None
    return out


def pct(x, d=1):
    return "—" if x is None else "{0:+.{1}f}%".format(x * 100, d)


BASIS = {"eps_pe": "EPS × 本益比", "sales_multiple": "每股營收 × 市銷率", "fcf_yield": "每股自由現金流 ÷ 殖利率"}
PROB_LAB = {"bear": "悲觀", "base": "基準", "bull": "樂觀"}


def table_html(header, rows, cls=""):
    s = '<div class="tw"><table class="{0}"><thead><tr>{1}</tr></thead><tbody>'.format(cls, "".join("<th>{0}</th>".format(h) for h in header))
    for r in rows:
        s += "<tr>" + "".join("<td>{0}</td>".format(c) for c in r) + "</tr>"
    return s + "</tbody></table></div>"


def scenario_table(c):
    rows = []
    for k in ("bear", "base", "bull"):
        r = c["rows"][k]
        rows.append([PROB_LAB[k], "{0:.0f}%".format(r["prob"] * 100), esc(r["driver"]),
                     "{0:,.2f} × {1:,.1f}（{2}）".format(float(r["eps"] or 0), float(r["multiple"] or 0), BASIS.get(r["basis"], r["basis"])),
                     "{0:,.0f}".format(r["target"]), pct(r["ret"]), pct(r["tot_ret"]), pct(r["ann"])])
    t = table_html(["情境", "機率", "假設", "每股指標 × 倍數", "{0:g} 年後目標價".format(c["horizon"]), "價差報酬", "含股息報酬", "年化（含股息）"], rows, "scen")
    note = ("<p class='note'>現價 {0:,.2f}；機率加權目標價 {1:,.0f}，價差報酬 {2}，含股息 {3}，年化 {4}；上檔對下檔比（樂觀含息報酬 ÷ 悲觀含息虧損）{5}。"
            "股息以現行每股年配 {6:,.2f} 美元乘以年數單利累加，不計再投資。</p>").format(
        c["price"], c["ev_target"], pct(c["ev_ret"]), pct(c["ev_tot_ret"]), pct(c["ev_ann"]),
        "{0:.1f} 倍".format(c["updown"]) if c["updown"] else "—（悲觀情境未虧損或樂觀未賺）", c["div"])
    if abs(c["prob_sum"] - 1) > 0.011:
        note += "<p class='warn'>注意：三情境機率加總為 {0:.2f}，不等於 1。</p>".format(c["prob_sum"])
    return t + note


# ------------------------------------------------------------ 歷史倍數與獲利乘倍數對照
MET_NAME = {"pe": "過去十二個月本益比", "ps": "過去十二個月市銷率", "evs": "過去十二個月 EV／營收", "pfcf": "股價／過去十二個月自由現金流"}
BASIS_MET = {"eps": "pe", "sales_per_share": "ps", "fcf_per_share": "pfcf"}


def fx(v, d=1):
    return "—" if v is None else "{0:.{1}f}".format(v, d)


def hist_table(mu, cons, price):
    if not mu or not mu.get("years"):
        return "<p class='note'>（沒有歷史倍數資料。）</p>"
    yrs, st, now = mu["years"], mu["stats"], mu.get("now") or {}
    hdr = ["指標"] + [y["fy_end"] for y in yrs] + ["最低", "中位", "最高", "現在（過去十二個月，至 {0}）".format(esc(now.get("ttm_end", "?")))]
    rows = []
    for k, name in [("pe", "本益比"), ("ps", "市銷率"), ("evs", "EV／營收"), ("pfcf", "股價／自由現金流")]:
        s_ = st.get(k)
        rows.append([name] + [fx(y.get(k)) for y in yrs] + ([fx(s_["min"]), fx(s_["med"]), fx(s_["max"])] if s_ else ["—"] * 3) + [fx(now.get(k))])
    out = table_html(hdr, rows)
    notes = ["年度欄是各會計年度結束日的過去十二個月倍數（股價＝當日或之前最近收盤，未還原股息）；最低、中位、最高只在有值的年度之間算（{0} 個年度點）。".format(max([(v or {}).get("n", 0) for v in st.values()] or [0]))]
    for y in yrs:
        for n in y.get("notes", []):
            notes.append("{0}：{1}。".format(y["fy_end"], n))
    for d in mu.get("dropped_years", []):
        notes.append("{0}：yfinance 年度財報欄位全空，略過。".format(d))
    if cons and price:
        fw = []
        for lab, k in (("FY1", "fy1"), ("FY2", "fy2"), ("FY3", "fy3")):
            e = cons.get(k)
            if e:
                fw.append("{0} 共識 EPS {1} → {2:.1f} 倍".format(lab, e, price / float(e)))
        if fw:
            notes.append("預估口徑只有現在這一點，歷史上沒有同口徑可比，不放進上表：現價 {0:,.2f} 對 {1}（Koyfin {2}）。".format(price, "；".join(fw), esc(cons.get("date"))))
    notes.append("每股營收與每股自由現金流用年度稀釋平均股數，EV 的股數同，是近似值。")
    fxi = mu.get("fx") or {}
    if fxi.get("cross"):
        fr = "；".join("{0} 平均 {1:.5f}／年底 {2:.5f}".format(r["fy_end"][:4], r["avg"], r["end"]) for r in sorted(fxi.get("rows", []), key=lambda r: r["fy_end"]) if any(y["fy_end"] == r["fy_end"] for y in yrs))
        fn = fxi.get("now") or {}
        notes.append("報表幣別 {0}、股價幣別 {1}：EPS、營收、現金流用該年度平均匯率、淨負債用年底匯率，全部換成 {1} 再與股價相比（1 {0}＝多少 {1}：{2}；現在欄：過去十二個月平均 {3:.5f}、現價日 {4} 現匯 {5:.5f}）。股數與 EPS 是 yfinance 的每單位上市證券口徑。".format(
            fxi["fin"], fxi["quote"], fr, fn.get("avg", 0), esc(fn.get("end_date", "?")), fn.get("end", 0)))
        for e in fxi.get("errors", []):
            notes.append("匯率問題：{0}".format(esc(e)))
    return out + "".join("<p class='note'>{0}</p>".format(n) for n in notes)


def cases(machine, mu, price, price_date=None, strict=False):
    """獲利乘倍數。新流程（strict）：每檔要有 fiscal_year_end 且三檔同一年度，年化年數＝現價日到該日的實際年數；
    不合格就回 {"error": 原因}，表的位置顯示原因、不硬算。舊 machine（沒有 fiscal_year_end）照舊用 horizon_years，表下註明。"""
    div = float(machine.get("annual_dividend_per_share") or 0)
    cl = machine.get("earnings_cases") or []
    fyes = {str(c.get("fiscal_year_end") or "").strip() for c in cl}
    legacy = fyes == {""} or not cl
    if strict and (not cl or "" in fyes or len(fyes) != 1):
        return {"error": "judge 輸出不合格：獲利三檔缺 fiscal_year_end，或三檔不是同一個會計年度（{0}）".format("、".join(sorted(x or "空白" for x in fyes)) or "沒有三檔"),
                "rows": [], "price": price}
    if legacy:
        h = float(machine.get("horizon_years") or 3)
        ann_ok, fye = True, None
    else:
        fye = fyes.pop()
        try:
            d1 = dt.datetime.strptime(fye, "%Y-%m-%d").date()
            d0 = dt.datetime.strptime(str(price_date), "%Y-%m-%d").date()
        except Exception:
            return {"error": "fiscal_year_end 或現價日格式不對（{0}／{1}）".format(fye, price_date), "rows": [], "price": price}
        h = (d1 - d0).days / 365.25
        ann_ok = h >= 0.5
    out = {"horizon": h, "div": div, "price": price, "rows": [], "legacy": legacy, "fiscal_year_end": fye, "price_date": price_date, "annualized": ann_ok}
    st = (mu or {}).get("stats", {})
    now = (mu or {}).get("now") or {}
    for c in cl:
        met = BASIS_MET.get(c.get("basis"), "pe")
        s_ = st.get(met)
        mults = {"低": s_["min"] if s_ else None, "中位": s_["med"] if s_ else None, "高": s_["max"] if s_ else None, "現在": now.get(met)}
        cells = {}
        for k, m in mults.items():
            if m is None:
                cells[k] = None
                continue
            p = float(c["eps"]) * m
            tot = p + div * h
            ann = ((tot / price) ** (1 / h) - 1) if ann_ok and tot > 0 and price else None
            cells[k] = {"mult": m, "price": p, "ann": ann, "total": (tot / price - 1) if price else None}
        out["rows"].append({"label": c.get("label"), "eps": c.get("eps"), "eps_adjusted": c.get("eps_adjusted"), "basis": c.get("basis"), "metric": met,
                            "what": c.get("what", ""), "cells": cells})
    return out


def cases_table(cs, mu):
    if cs.get("error"):
        return "<p class='bad'>獲利乘倍數對照表未產生：{0}。</p>".format(esc(cs["error"]))
    if not cs["rows"]:
        return "<p class='note'>（沒有獲利三檔資料。）</p>"
    ann_ok = cs.get("annualized", True)
    hdr = ["獲利檔位（每股{0}）".format("，帳面口徑" if not cs.get("legacy") else ""), "倍數：歷史低", "倍數：歷史中位", "倍數：歷史高", "倍數：現在"]
    rows = []
    for r in cs["rows"]:
        adj = ""
        if r.get("eps_adjusted") is not None and abs(float(r["eps_adjusted"]) - float(r["eps"])) > 1e-9:
            adj = "（調整後 {0:,.2f}）".format(float(r["eps_adjusted"]))
        line = ["<b>{0}</b>　{1:,.2f}{2}（{3}）<br><span class='note'>{4}</span>".format(esc(r["label"]), float(r["eps"]), adj, esc(MET_NAME.get(r["metric"], r["metric"])), esc(r["what"]))]
        for k in ("低", "中位", "高", "現在"):
            c = r["cells"].get(k)
            if not c:
                line.append("—")
            else:
                tail = pct(c["ann"]) if ann_ok else "總報酬 " + pct(c["total"])
                line.append("{0:.1f} 倍<br>{1:,.0f}｜{2}".format(c["mult"], c["price"], tail))
        rows.append(line)
    yrs = "、".join(y["fy_end"][:4] for y in (mu or {}).get("years", []))
    now = (mu or {}).get("now") or {}
    h = cs["horizon"]
    if cs.get("legacy"):
        when = "{0:g} 年後".format(h)
        base = "這份的獲利檔位未標年度與口徑，年化年數取自 horizon_years（{0:g} 年）。".format(h)
        ann_txt = "年化＝((價格＋每股年配 {0:,.2f}×{1:g} 年)÷現價 {2:,.2f})^(1/{1:g})－1".format(cs["div"], h, cs["price"])
    else:
        when = cs["fiscal_year_end"]
        base = ("獲利檔位是 {0} 會計年度結束時的帳面口徑每股獲利；價格＝該檔獲利×倍數，含義是「該會計年度結束時，股價＝當年帳面 EPS×屆時的過去十二個月本益比」。"
                "從現價日 {1} 到 {0} 共 {2:.2f} 年。").format(esc(cs["fiscal_year_end"]), esc(cs["price_date"]), h)
        if ann_ok:
            ann_txt = "年化＝((價格＋每股年配 {0:,.2f}×{1:.2f} 年)÷現價 {2:,.2f})^(1/{1:.2f})－1".format(cs["div"], h, cs["price"])
        else:
            ann_txt = "不到 0.5 年，不年化，只列總報酬＝(價格＋股息)÷現價－1（股息按年數比例加）"
    note = ("每格上行是倍數，下行是 {0} 的價格｜{1}。{2}股息單利累加、不計再投資。倍數檔位取自 {3} 各年度年底的過去十二個月倍數（低＝最低、中位、高＝最高，各指標有值的年度數不一定相同）；"
            "「現在」是現價對最近四季（至 {4}）的倍數。獲利三檔是作者依正文所述的情況設定，倍數檔位是歷史取值，表內任何一格都不是預測。").format(
        when, "含股息年化報酬" if ann_ok else "含股息總報酬", ann_txt + "。" + base, yrs or "—", esc(now.get("ttm_end", "?")))
    return table_html(hdr, rows, "cases") + "<p class='note'>{0}</p>".format(note)


CASE_BASIS_NAME = {"eps": "獲利", "sales_per_share": "每股營收", "fcf_per_share": "每股自由現金流"}


def cases3_rows(cs, price):
    """獲利三檔：每檔的帳面、調整後獲利與「現價是這個獲利的幾倍」。獲利 ≤ 0 或沒有現價時倍數為 None。只做現價反推倍數，不算任何價位。"""
    out = []
    for r in cs.get("rows", []):
        def mult(v):
            try:
                v = float(v)
            except (TypeError, ValueError):
                return None
            return price / v if (v > 0 and price) else None
        eps = r.get("eps")
        adj = r.get("eps_adjusted")
        try:
            has_adj = adj is not None and eps is not None and abs(float(adj) - float(eps)) > 1e-9
        except (TypeError, ValueError):
            has_adj = False
        out.append({"label": r.get("label"), "basis": r.get("basis") or "eps", "what": r.get("what", ""), "eps": eps,
                    "adj": adj if has_adj else None, "m": mult(eps), "m_adj": mult(adj) if has_adj else None})
    return out


def cases3_table(cs, price, price_date=None):
    if cs.get("error"):
        return "<p class='bad'>獲利三檔表未產生：{0}。</p>".format(esc(cs["error"]))
    rows3 = cases3_rows(cs, price)
    if not rows3:
        return "<p class='note'>（沒有獲利三檔資料。）</p>"
    basis = rows3[0]["basis"]
    unit = CASE_BASIS_NAME.get(basis, "獲利")
    has_adj = any(r["adj"] is not None for r in rows3)
    eps_name = {"eps": "每股盈餘", "sales_per_share": "每股營收", "fcf_per_share": "每股自由現金流"}.get(basis, "每股盈餘")
    hdr = ["檔位", eps_name + ("（帳面口徑）" if has_adj else "")]
    if has_adj:
        hdr.append("每股盈餘（調整後）")
    hdr.append("對應情況")
    if basis == "eps":
        hdr.append("現價是帳面獲利的幾倍" if has_adj else "現價是這個獲利的幾倍")
    else:
        hdr.append("現價是{0}的幾倍".format(unit))
    if has_adj:
        hdr.append("現價是調整後獲利的幾倍")

    def cell(v, d=2):
        return "—" if v is None else "{0:,.{1}f}".format(float(v), d)

    def mcell(m):
        return "—" if m is None else "{0:.1f} 倍".format(m)
    rows = []
    for r in rows3:
        line = ["<b>{0}</b>".format(esc(r["label"])), cell(r["eps"])]
        if has_adj:
            line.append(cell(r["adj"]) if r["adj"] is not None else "—")
        line.append(esc(r["what"]))
        line.append(mcell(r["m"]))
        if has_adj:
            line.append(mcell(r["m_adj"]) if r["adj"] is not None else "—")
        rows.append(line)
    if cs.get("legacy"):
        yr = "獲利檔位未標會計年度"
    else:
        yr = "獲利檔位是 {0} 會計年度的{1}".format(esc(cs.get("fiscal_year_end")), eps_name + ("（帳面口徑）" if has_adj else ""))
    note = ("{0}，由作者依正文所述的情況設定，不是預測；倍數＝現價 {1:,.2f}（{2} 收盤）÷ 該檔獲利，獲利 ≤ 0 的檔位不算倍數。"
            "這張表只說明現價對應哪一檔獲利，不推算任何價位。").format(yr, price, esc(price_date or cs.get("price_date") or "?"))
    return table_html(hdr, rows, "cases3") + "<p class='note'>{0}</p>".format(note)


def tracking_table(machine):
    rows = [[esc(t.get("metric", "")), esc(t.get("bull_if", "")), esc(t.get("warn_if", "")), esc(t.get("next_check", ""))] for t in machine.get("tracking", [])]
    out = table_html(["追蹤指標", "偏樂觀的條件", "警訊條件", "下次檢查"], rows) if rows else ""
    cm = machine.get("change_my_mind") or []
    if cm:
        out += "<p><b>會讓結論翻面的事：</b></p><ul>" + "".join("<li>{0}</li>".format(esc(x)) for x in cm) + "</ul>"
    return out


def prior_table(machine, pack):
    vp = machine.get("vs_prior") or []
    pm = pack.get("prior_meta") or {}
    head = ""
    if pm:
        head = "<p class='note'>上一份（{0}，舊流程）：裁決 {1}｜{2}，當時股價 {3}；本份現價 {4:,.2f}。</p>".format(
            esc(pm.get("date")), esc(pm.get("dca_verdict")), esc(pm.get("dca_role")), esc(pm.get("price_at_dd")), pack.get("last_price", 0))
    if not vp:
        return head
    return head + table_html(["變了什麼", "上一份", "這一份", "對結論的影響"],
                             [[esc(v.get("what", "")), esc(v.get("before", "")), esc(v.get("now", "")), esc(v.get("effect", ""))] for v in vp])


def routine_table(ask):
    rows = []
    for r in ask.get("routine", []):
        ok = str(r.get("status", "")).startswith("無")
        rows.append([esc(r.get("item", "")), ("<span class='ok'>無事</span>" if ok else "<span class='bad'>有事</span>"), esc(r.get("line", ""))])
    return table_html(["例行檢查", "結果", "說明"], rows) if rows else ""


def price_svg(pc):
    if not pc:
        return "<p class='note'>（沒有價格序列，圖略。）</p>"
    mc = pc["monthly_close"]
    W, H, L, R, T, B = 720, 300, 52, 14, 14, 30
    vals = [v for _, v in mc] + [pc["ath_close"]]
    lo, hi = min(vals) * 0.95, max(vals) * 1.05
    n = len(mc)

    def x(i):
        return L + (W - L - R) * i / max(n - 1, 1)

    def y(v):
        return T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    idx = {d: i for i, (d, _) in enumerate(mc)}

    def path(series):
        pts = [(x(idx[d]), y(v)) for d, v in series if d in idx]
        return "M" + " L".join("{0:.1f},{1:.1f}".format(a, b) for a, b in pts)
    s = ['<svg viewBox="0 0 {0} {1}" class="chart" role="img" aria-label="月線收盤價與 10 個月、20 個月均線，以及歷史最高收盤水平線">'.format(W, H)]
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        s.append('<line x1="{0}" x2="{1}" y1="{2:.1f}" y2="{2:.1f}" class="grid"/><text x="{3}" y="{4:.1f}" class="ax" text-anchor="end">{5:,.0f}</text>'.format(L, W - R, y(v), L - 6, y(v) + 4, v))
    for i in range(0, n, 24):
        s.append('<text x="{0:.1f}" y="{1}" class="ax" text-anchor="middle">{2}</text>'.format(x(i), H - 10, mc[i][0][:7]))
    s.append('<line x1="{0}" x2="{1}" y1="{2:.1f}" y2="{2:.1f}" class="ath"/>'.format(L, W - R, y(pc["ath_close"])))
    s.append('<text x="{0}" y="{1:.1f}" class="lab ath-t" text-anchor="end">歷史最高收盤 {2:,.0f}（{3}）</text>'.format(W - R, y(pc["ath_close"]) - 5, pc["ath_close"], pc["ath_date"][:7]))
    s.append('<path d="{0}" class="ma20"/>'.format(path(pc["ma20"])))
    s.append('<path d="{0}" class="ma10"/>'.format(path(pc["ma10"])))
    s.append('<path d="{0}" class="px"/>'.format(path(mc)))
    s.append('<circle cx="{0:.1f}" cy="{1:.1f}" r="3.5" class="dot"/>'.format(x(n - 1), y(pc["last"])))
    s.append('<text x="{0:.1f}" y="{1:.1f}" class="lab" text-anchor="end">現價 {2:,.1f}</text>'.format(x(n - 1) - 8, y(pc["last"]) - 8, pc["last"]))
    s.append("</svg>")
    leg = "<p class='legend'><span class='k px'></span>月底收盤 <span class='k ma10'></span>10 個月均線 <span class='k ma20'></span>20 個月均線 <span class='k ath'></span>歷史最高收盤（未還原股息）</p>"
    return "".join(s) + leg


# ------------------------------------------------------------ Markdown
def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]\n]+)\]\((https?://[^\s)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def md_to_html(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("<!--RAW"):
            out.append(ln[len("<!--RAW"):-3] if ln.endswith("-->") else ln)
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            lv = len(m.group(1))
            out.append("<h{0}>{1}</h{0}>".format(lv, inline(m.group(2))))
            i += 1
            continue
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            hdr = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append(table_html([inline(h) for h in hdr], [[inline(c) for c in r] for r in rows]))
            continue
        if re.match(r"^\s*[-*]\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join("<li>{0}</li>".format(inline(t)) for t in items) + "</ul>")
            continue
        if re.match(r"^\s*\d+[.、]\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+[.、]\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+[.、]\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join("<li>{0}</li>".format(inline(t)) for t in items) + "</ol>")
            continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> "))
                i += 1
            out.append("<blockquote>{0}</blockquote>".format(inline(" ".join(buf))))
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\s*[-*]\s|\s*\||>|<!--RAW)", lines[i]):
            buf.append(lines[i])
            i += 1
        if not buf:
            buf = [lines[i]]
            i += 1
        out.append("<p>{0}</p>".format(inline(" ".join(buf))))
    return "\n".join(out)


# ------------------------------------------------------------ 引用
PLACEHOLDERS = ["表:歷史倍數", "表:獲利乘倍數對照", "表:獲利三檔", "表:追蹤條件", "表:跟上一份比", "表:例行檢查", "圖:股價位置"]
OLD_CASE_PLACEHOLDERS = ["表:歷史倍數", "表:獲利乘倍數對照"]  # 舊文章用的佔位：有就照舊排版，新文章不必放，缺了不算缺
LEGACY_PLACEHOLDERS = ["表:情境估值"]  # 舊版佔位記號：出現時換成空字串，不崩


def collect_refs(article, pack, lookups, computes=()):
    """回傳 (換好上標的文字, 來源清單 html, 未解析的標籤)。引用先換成 \x00N\x01 記號，等 inline 之後再換成連結。"""
    order, unresolved = [], []
    lk = {str(l.get("id")): l for l in lookups}
    cm = {str(c.get("id")): c for c in computes}

    def key_of(kind, name):
        return (kind, name)

    def repl(m):
        body = m.group(0)[1:-1]
        keys = []
        for part in re.split(r"[,，、;；]\s*", body):
            part = part.strip()
            mm = re.match(r"^([plc]):\s*(.+)$", part)
            if mm:
                keys.append((mm.group(1), mm.group(2).strip()))
            elif keys and part:
                keys.append((keys[-1][0], part))
        marks = []
        for kind, name in keys:
            if kind == "l" and name not in lk and ("l" + name) in lk:
                name = "l" + name
            ok = (kind == "p" and name in pack["tags"]) or (kind == "l" and name in lk) or (kind == "c" and name in cm)
            if not ok:
                unresolved.append("[{0}:{1}]".format(kind, name))
                marks.append("\x02{0}:{1}\x03".format(kind, name))
                continue
            k = key_of(kind, name)
            if k not in order:
                order.append(k)
            marks.append("\x00{0}\x01".format(order.index(k) + 1))
        return "".join(marks)
    text = re.sub(r"\[[plc]:[^\]\n]+\]", repl, article)
    items = []
    for n, (kind, name) in enumerate(order, 1):
        if kind == "p":
            t = pack["tags"][name]
            label = esc(t["title"])
            src = esc(t.get("source", ""))
            if t.get("url"):
                src = '<a href="{0}" rel="noopener">{1}</a>'.format(esc(t["url"]), src or esc(t["url"]))
            items.append('<li id="src-{0}"><span class="sn">{0}</span> {1}｜{2}｜資料日 {3}</li>'.format(n, label, src, esc(t.get("asof", ""))))
        elif kind == "c":
            c = cm[name]
            body = "；".join("{0} {1:+.1f}%（含息 {2:+.1f}%）".format(r["ticker"], r["price_chg_pct"], r["total_ret_pct"]) for r in c.get("rows", []) if r.get("price_chg_pct") is not None)
            items.append('<li id="src-{0}"><span class="sn">{0}</span> 程式計算 {1}（price_store，{2} 至 {3}）：{4}｜{5}</li>'.format(
                n, esc(name), esc(c.get("from")), esc(c.get("to")), esc(body), esc(c.get("why", ""))))
        else:
            l = lk[name]
            qs = "".join('<div class="q">「{0}」 <a href="{1}" rel="noopener">{2}</a> {3}</div>'.format(
                esc(q.get("text", "")[:300]), esc(q.get("url", "")), esc(re.sub(r"^https?://(www\.)?", "", q.get("url", ""))[:60]), esc(q.get("date", "")))
                for q in (l.get("quotes") or []))
            items.append('<li id="src-{0}"><span class="sn">{0}</span> 查證 {1}：{2}（信心：{3}）{4}</li>'.format(
                n, esc(name), esc((l.get("question") or "")[:120]), esc(l.get("confidence", "")), qs))
    return text, "<ol class='srcs'>" + "".join(items) + "</ol>", unresolved


def finalize_marks(h):
    h = re.sub(r"\x00(\d+)\x01", lambda m: '<sup><a href="#src-{0}">{0}</a></sup>'.format(m.group(1)), h)
    h = re.sub(r"\x02([pl]):(.*?)\x03", lambda m: '<sup class="bad">[{0}:{1}?]</sup>'.format(m.group(1), m.group(2)), h)
    return h


# ------------------------------------------------------------ 數字檢查
NUM_RE = re.compile(r"(?<![\w.])[-+−]?\d[\d,]*(?:\.\d+)?")
SCALES = [1, 1e-3, 1e3, 1e-2, 1e2, 1e-4, 1e4, 1e-6, 1e6]
FORMULA_RE = re.compile(r"[×÷＝=＋−＊/]|乘以|除以|相當於|折合|換算|合計|加總|減去|扣掉|占比|佔比|年增|年化")


def nums_in(text):
    vals = []
    for m in NUM_RE.finditer(text):
        raw = m.group(0).replace(",", "").replace("−", "-")
        try:
            v = float(raw.lstrip("+"))
        except ValueError:
            continue
        dec = len(raw.split(".")[1]) if "." in raw else 0
        vals.append((m.group(0), abs(v), dec, m.start()))
    return vals


def build_refset(texts):
    ref = set()
    for t in texts:
        for _, v, _, _ in nums_in(t):
            ref.add(round(v, 6))
    return ref


def number_check(article, ref_texts, strict=False):
    body = re.sub(r"\[[plc]:[^\]\n]+\]", "", article)
    body = re.sub(r"\{\{[^}]+\}\}", "", body)
    ref = build_refset(ref_texts)
    refl = sorted(ref)

    def matched(v, dec):
        tol = 0.5 * 10 ** (-dec) + 1e-9
        for s in SCALES:
            tv = v * s
            for r in refl:
                if abs(r - tv) <= tol * s + 1e-9:
                    return True
        return False
    bad = []
    paras = [p for p in re.split(r"\n+", body) if p.strip()]
    for pi, para in enumerate(paras):
        adj = para.lstrip().startswith("算式") or (pi + 1 < len(paras) and paras[pi + 1].lstrip().startswith("算式")) or (pi > 0 and paras[pi - 1].lstrip().startswith("算式"))
        for sent in re.split(r"(?<=[。；？！])", para):
            if not sent.strip():
                continue
            has_formula = (not strict) and (adj or bool(FORMULA_RE.search(sent)))
            for raw, v, dec, pos in nums_in(sent):
                ctx = sent[max(0, pos - 2): pos + len(raw) + 3]
                if 1990 <= v <= 2040 and dec == 0:
                    continue
                if dec == 0 and v <= 12 and not re.search(r"[%％]", sent[pos + len(raw): pos + len(raw) + 1]):
                    continue
                if re.search(r"^\D{0,2}\d+\s*[月日季]|FY\d|Q\d|第\s*\d", ctx) and dec == 0 and v <= 31:
                    continue
                if matched(v, dec):
                    continue
                if has_formula:
                    continue
                bad.append({"number": raw, "sentence": sent.strip()[:160]})
    return bad


CSS = """
:root{--bg:#fff;--fg:#1c1f23;--mut:#5d6672;--line:#d9dee4;--acc:#1b5fa8;--card:#f5f7fa;--ok:#1a7a3c;--bad:#b3261e;--px:#1c1f23;--m10:#1b5fa8;--m20:#c77d0a;--ath:#b3261e}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#14171b;--fg:#e6e9ed;--mut:#9aa4b0;--line:#2c333b;--acc:#6aa9ee;--card:#1c2127;--ok:#52c27a;--bad:#ff7b72;--px:#e6e9ed;--m10:#6aa9ee;--m20:#e0a43b;--ath:#ff7b72}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 -apple-system,BlinkMacSystemFont,"PingFang TC","Noto Sans TC",sans-serif}
main{max-width:760px;margin:0 auto;padding:20px 16px 80px}
h1{font-size:1.5rem;line-height:1.4;margin:.4em 0 .3em}h2{font-size:1.2rem;margin:2em 0 .4em;padding-top:.6em;border-top:1px solid var(--line)}h3{font-size:1.05rem;margin:1.4em 0 .3em}
p{margin:.7em 0}.meta{color:var(--mut);font-size:.85rem}.tag{display:inline-block;padding:2px 10px;border-radius:99px;background:var(--card);border:1px solid var(--line);font-size:.85rem;margin-right:6px}
.tw{overflow-x:auto;margin:1em 0}table{border-collapse:collapse;width:100%;font-size:.88rem}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:var(--card);white-space:nowrap}
.note{color:var(--mut);font-size:.88rem}.warn,.bad{color:var(--bad)}.ok{color:var(--ok)}
blockquote{margin:1em 0;padding:.2em 1em;border-left:3px solid var(--acc);background:var(--card)}
sup a{color:var(--acc);text-decoration:none;font-size:.7rem;padding:0 1px}
.srcs{font-size:.8rem;color:var(--mut);padding-left:0;list-style:none}.srcs li{margin:.5em 0}.sn{display:inline-block;min-width:1.6em;color:var(--acc);font-weight:600}.q{margin:.2em 0 0 1.8em}
.chart{width:100%;height:auto}.chart .grid{stroke:var(--line);stroke-width:1}.chart .ax{fill:var(--mut);font-size:11px}.chart .px{fill:none;stroke:var(--px);stroke-width:1.8}.chart .ma10{fill:none;stroke:var(--m10);stroke-width:1.5}.chart .ma20{fill:none;stroke:var(--m20);stroke-width:1.5}.chart .ath{stroke:var(--ath);stroke-dasharray:5 4;stroke-width:1.3}.chart .ath-t{fill:var(--ath)}.chart .lab{fill:var(--fg);font-size:11px}.chart .dot{fill:var(--px)}
.legend{font-size:.8rem;color:var(--mut)}.k{display:inline-block;width:18px;height:0;border-top:2px solid;vertical-align:middle;margin:0 4px 0 10px}.k.px{border-color:var(--px)}.k.ma10{border-color:var(--m10)}.k.ma20{border-color:var(--m20)}.k.ath{border-top-style:dashed;border-color:var(--ath)}
"""


def render(run, out=None, back_link=None):
    run = Path(run)
    pack = json.loads((run / "pack.json").read_text(encoding="utf-8"))
    pack_md = (run / "pack.md").read_text(encoding="utf-8")
    ask = json.loads((run / "ask.json").read_text(encoding="utf-8")) if (run / "ask.json").exists() else {}  # 精簡版沒有出題步驟
    lookups = json.loads((run / "lookups.json").read_text(encoding="utf-8")) if (run / "lookups.json").exists() else []
    article = (run / "article.md").read_text(encoding="utf-8")
    if (run / "base.md").exists() and "## 公司底稿" not in article:
        base = (run / "base.md").read_text(encoding="utf-8").strip()
        m2 = re.search(r"(?m)^## (?!結論)", article[article.find("## 結論") + 5:]) if "## 結論" in article else None
        if m2:
            pos = article.find("## 結論") + 5 + m2.start()
            article = article[:pos] + base + "\n\n" + article[pos:]
        else:
            article = article.rstrip() + "\n\n" + base + "\n"
    machine = json.loads((run / "machine.json").read_text(encoding="utf-8"))
    price = pack["last_price"]
    try:
        import multiples as mp
        mu = mp.build(pack["ticker"], price_override=price)
    except Exception as e:
        mu = {"years": [], "stats": {}, "now": {"error": str(e)[:80]}}
    cs = cases(machine, mu, price, pack.get("price_chart", {}).get("last_date"), strict=(run / "brief.json").exists())
    calc = {"multiples": mu, "cases": cs}
    (run / "calc.json").write_text(json.dumps(calc, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    blocks = {"表:歷史倍數": hist_table(mu, pack.get("consensus"), price), "表:獲利乘倍數對照": cases_table(cs, mu), "表:獲利三檔": cases3_table(cs, price, pack.get("price_chart", {}).get("last_date")),
              "表:追蹤條件": tracking_table(machine), "表:跟上一份比": prior_table(machine, pack),
              "表:例行檢查": routine_table(ask), "圖:股價位置": price_svg(pack.get("price_chart"))}
    for lp in LEGACY_PLACEHOLDERS:
        blocks[lp] = ""
    left = []
    text = article
    for ph in PLACEHOLDERS + LEGACY_PLACEHOLDERS:
        pat = re.compile(r"\{\{\s*" + re.escape(ph) + r"\s*\}\}")
        if ph in LEGACY_PLACEHOLDERS:
            text = pat.sub("", text)
        elif pat.search(text):
            text = pat.sub(lambda m, ph=ph: "\n<!--RAW" + blocks[ph].replace("\n", " ") + "-->\n", text)
        elif ph == "表:跟上一份比" and any("沒有上一份 DD" in g for g in pack.get("gaps", [])):
            pass  # 資料包沒有上一份報告，這張表本來就沒東西可放，不算缺
        elif ph in OLD_CASE_PLACEHOLDERS:
            pass  # 舊佔位：新文章不再要求
        elif ph == "表:獲利三檔" and re.search(r"\{\{\s*表:獲利乘倍數對照\s*\}\}", article):
            pass  # 舊文章用舊的情境表佔位，不算缺新佔位
        else:
            left.append("正文沒有放 {{" + ph + "}}")
    leftover = re.findall(r"\{\{[^}]*\}\}", text)
    computes = json.loads((run / "compute.json").read_text(encoding="utf-8")) if (run / "compute.json").exists() else []
    text, srcs, unresolved = collect_refs(text, pack, lookups, computes)
    h = finalize_marks(md_to_html(text))
    h = finalize_marks(h)
    # 數字檢查
    peers_md = (run / "peers.md").read_text(encoding="utf-8") if (run / "peers.md").exists() else ""
    ref_texts = [pack_md, peers_md, json.dumps(lookups, ensure_ascii=False), json.dumps(computes, ensure_ascii=False),
                 json.dumps(calc, ensure_ascii=False, default=str), json.dumps(machine, ensure_ascii=False)]
    for r in cs.get("rows", []):
        for c in r["cells"].values():
            if c:
                ref_texts.append("{0:.1f} {1:.0f} {2:.1f}".format(c["mult"], c["price"], (c["ann"] or 0) * 100))
    for r in (cases3_rows(cs, price) if re.search(r"\{\{\s*表:獲利三檔\s*\}\}", article) else []):  # 只有用新佔位的文章才把倍數算進可引用的數字
        for m_ in (r["m"], r["m_adj"]):
            if m_ is not None:
                ref_texts.append("{0:.1f} {1:.0f}".format(m_, m_))
    bad = number_check(article, ref_texts)
    nib = None
    if (run / "brief.json").exists():  # 兩通寫作：文章每個數字要在底稿，或在資料包／查證／程式比較／同業表裡，都沒有的列出（不放寬算式句）
        nib = number_check(article, [(run / "brief.json").read_text(encoding="utf-8"), pack_md, peers_md, json.dumps(lookups, ensure_ascii=False),
                                     json.dumps(computes, ensure_ascii=False)], strict=True)
    ncj = {"count": len(bad), "items": bad, "unresolved_refs": unresolved, "placeholders_missing": left, "placeholders_leftover": leftover}
    if nib is not None:
        ncj["not_in_brief_count"] = len(nib)
        ncj["not_in_brief"] = nib
    (run / "number_check.json").write_text(json.dumps(ncj, ensure_ascii=False, indent=1), encoding="utf-8")
    m = re.search(r"^#\s+(.+)$", article, re.M)
    title = m.group(1) if m else pack["ticker"]
    mo = machine.get("moat") or {}
    moat_line = '<p class="note">護城河：{0}｜{1}｜{2}</p>'.format(esc(mo.get("source")), esc(mo.get("trend")), esc(mo.get("evidence"))) if mo else ""
    head = ('<p class="meta">{0}｜資料日 {1}｜現價 {2:,.2f}（{3} 收盤）｜精簡版</p>'
            '<p><span class="tag">生意方向：{4}</span></p><p class="note"><b>{5}</b></p>'
            '<p class="note">現價預設了什麼：{6}</p>{7}').format(
        esc(pack["ticker"]), esc(pack["date"]), price, esc(pack["price_chart"]["last_date"]), esc(machine.get("business_direction", "—")),
        esc(machine.get("one_liner")), esc(machine.get("price_implies", "—")), moat_line)
    mh = re.match(r"\s*(<h1>.*?</h1>)(.*)", h, re.S)
    body_html = (mh.group(1) + head + mh.group(2)) if mh else head + h
    if back_link:  # 可選：全文頁頂端（h1 之前）加回儀表板的小連結，預設不加
        body_html = '<p class="note"><a href="{0}">← 回個股儀表板</a></p>'.format(esc(back_link)) + body_html
    doc = ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
           '<title>{0} 個股研究</title><style>{1}.doc{{max-width:820px;margin:0 auto}}</style></head><body><main><article class="doc">{2}<h2>來源</h2>{3}</article></main></body></html>').format(
        esc(pack["ticker"]), CSS, body_html, srcs)
    # 把正文裡的 h1 保留；head 放在 h1 後面較佳，簡單做法：不調整
    out = Path(out) if out else PILOT / "{0}.html".format(pack["ticker"])
    out.write_text(doc, encoding="utf-8")
    return {"html": str(out), "chars": len(re.sub(r"\s+", "", article)), "number_check_bad": len(bad), "unresolved": unresolved,
            "ph_missing": left, "ph_leftover": leftover, "not_in_brief": None if nib is None else len(nib)}


if __name__ == "__main__":
    import sys
    print(json.dumps(render(sys.argv[1]), ensure_ascii=False, indent=1))
