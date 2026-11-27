#!/usr/bin/env python3
"""dd5 第 1 步：備料（零 LLM）。

用法：python3 scripts/dd5/pack.py TICKER [--date YYYYMMDD]
輸出：~/dd5-pilot/runs/{T}_{date}/pack.md、pack.json（tags 對照、價格序列、gaps）

每段 pack.md 以 `## [p:標籤] 標題` 開頭；正文用 [p:標籤] 引用。
重用零 LLM 零件：scripts/dd_numbers_extra.py（共識、淨債、估值歷史）、
scripts/dd_sections.py（dd-meta）、scripts/dd2/primary_us.py（EDGAR 年報切節）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
REPO = SCRIPTS.parent
for p in (str(SCRIPTS), str(SCRIPTS / "dd2"), str(Path.home() / "v7-backtest")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pandas as pd  # noqa: E402

PILOT = Path.home() / "dd5-pilot"
_drive = sorted(glob.glob(str(Path.home() / "Library/CloudStorage/GoogleDrive-*/我的雲端硬碟/007美股")))
DRIVE = Path(_drive[0]) if _drive else Path("/nonexistent")

CAPS = {"pr": 24000, "call": 54000, "biz": 11000, "risk": 13000, "mda": 16000}


def clip(text, n, label):
    if len(text) <= n:
        return text
    cut = text[:n]
    i = cut.rfind("\n")
    if i > n // 2:
        cut = cut[:i]
    return cut + "\n\n[截斷：原文 {0:,} 字元，只放前 {1:,} 字元（{2}）]".format(len(text), len(cut), label)


class Pack:
    def __init__(self, ticker, date):
        self.t, self.date = ticker, date
        self.sections = []
        self.tags = {}
        self.gaps = []
        self.extra = {}

    def add(self, tag, title, body, source="", url="", asof=""):
        self.sections.append((tag, title, body.strip()))
        self.tags[tag] = {"title": title, "source": source, "url": url, "asof": asof}

    def gap(self, msg):
        self.gaps.append(msg)

    def md(self):
        out = ["# 資料包：{0}（備料日 {1}）".format(self.t, self.date), ""]
        out.append("標籤規則：每段標題的 [p:標籤] 就是引用用的標籤。金額單位見各段。")
        out.append("")
        for tag, title, body in self.sections:
            out.append("## [p:{0}] {1}".format(tag, title))
            out.append("")
            out.append(body)
            out.append("")
        out.append("## [p:gaps] 缺口清單")
        out.append("")
        out.append("\n".join("- " + g for g in self.gaps) if self.gaps else "- （無）")
        out.append("")
        return "\n".join(out)


def fmt_m(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    return "{0:,.0f}".format(x / 1e6)


def md_table(header, rows):
    s = "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n"
    for r in rows:
        s += "| " + " | ".join(str(c) for c in r) + " |\n"
    return s


# ---------------------------------------------------------------- 財報
LINES = [
    ("營收", "Total Revenue"), ("毛利", "Gross Profit"), ("營業利益", "Operating Income"),
    ("淨利", "Net Income"), ("稀釋EPS（報表幣別）", "Diluted EPS"), ("稀釋股數（百萬）", "Diluted Average Shares"),
    ("研發費", "Research And Development"), ("利息費用", "Interest Expense"),
]


def _get(df, name, col):
    try:
        v = df.loc[name, col]
        return None if pd.isna(v) else float(v)
    except Exception:
        return None


def currency_info(yt):
    try:
        i = yt.info or {}
    except Exception:
        i = {}
    return i.get("financialCurrency") or "美元", i.get("currency") or "美元", i


def currency_section(pk, yt):
    """報表幣別、股價幣別、ADR 比例、匯率；兩者不同時才寫成獨立區段。"""
    import multiples as mp
    fin, quote, info = currency_info(yt)
    if fin == quote:
        return
    lines = ["報表幣別：{0}（損益、現金流、資產負債表的金額都是 {0}）；股價幣別：{1}（股價、市值、共識 EPS 若為 {1} 另行標明）。".format(fin, quote)]
    try:
        d = dt.datetime.strptime(pk.date, "%Y%m%d")
        spot, sd = mp.fx_rate(fin, quote, d, "end")
        inc = yt.income_stmt
        c0 = inc.columns[0]
        avg, _ = mp.fx_rate(fin, quote, c0, "avg")
        lines.append("匯率：1 {0}＝{1:.5f} {2}（{3} 現匯；每 1 {2} 約 {4:.2f} {0}）；最近會計年度（{5}）平均 1 {0}＝{6:.5f} {2}。".format(
            fin, spot, quote, sd, 1 / spot, c0.date(), avg))
        lines.append("歷史倍數換算：EPS、營收、現金流用該年度平均匯率，淨負債用年底匯率，股價用當日報價幣別收盤。匯率日線來源：yfinance「{0}=X」經 price_store。".format(fin if quote == "USD" else fin + "、" + quote))
    except Exception as e:
        pk.gap("匯率取不到（{0}），報表金額未換算：{1}".format(fin + "→" + quote, str(e)[:60]))
    sh = info.get("sharesOutstanding")
    try:
        ni = float(yt.income_stmt.loc["Net Income", yt.income_stmt.columns[0]])
        dil = float(yt.income_stmt.loc["Diluted Average Shares", yt.income_stmt.columns[0]])
        eps = float(yt.income_stmt.loc["Diluted EPS", yt.income_stmt.columns[0]])
        lines.append("股數口徑：yfinance 的稀釋股數 {0:,.0f} 百萬、EPS {1:.2f} {2} 與「淨利÷股數＝{3:.2f}」互相對得上，表示 yfinance 已經把股數與 EPS 折成「每 1 單位上市證券」（ADR 或存託憑證）的口徑；不必再乘除 ADR 比例（ADR 實際兌普通股比例：以公司公告為準，未由程式取得）。".format(
            dil / 1e6, eps, fin, ni / dil))
    except Exception:
        pass
    if sh:
        lines.append("目前流通股數（yfinance sharesOutstanding，同上單位口徑）{0:,.0f} 百萬。".format(sh / 1e6))
    pk.add("fx", "幣別、匯率與股數口徑", "\n".join(lines), "yfinance＋price_store", asof=pk.date)


def fin_tables(pk, yt):
    fin_cur = currency_info(yt)[0]
    inc, cf, bs = yt.income_stmt, yt.cashflow, yt.balance_sheet
    qinc, qcf, qbs = yt.quarterly_income_stmt, yt.quarterly_cashflow, yt.quarterly_balance_sheet

    def block(inc_, cf_, bs_, ncols):
        cols = [c for c in list(inc_.columns)[:ncols] if _get(inc_, "Total Revenue", c) is not None][::-1]
        hdr = ["項目（百萬{0}，除EPS）".format(fin_cur)] + [c.strftime("%Y-%m-%d") for c in cols]
        rows = []
        for lab, key in LINES:
            r = [lab]
            for c in cols:
                v = _get(inc_, key, c)
                if v is None:
                    r.append("—")
                elif "EPS" in lab:
                    r.append("{0:.2f}".format(v))
                elif "股數" in lab:
                    r.append("{0:,.0f}".format(v / 1e6))
                else:
                    r.append(fmt_m(v))
            rows.append(r)
        for lab, key in [("營運現金流", "Operating Cash Flow"), ("資本支出", "Capital Expenditure"),
                         ("自由現金流", "Free Cash Flow"), ("股票薪酬", "Stock Based Compensation"),
                         ("回購", "Repurchase Of Capital Stock"), ("股息支付", "Cash Dividends Paid"),
                         ("併購支出", "Purchase Of Business")]:
            rows.append([lab] + [fmt_m(_get(cf_, key, c)) if c in cf_.columns else "—" for c in cols])
        for lab, key in [("現金及約當", "Cash And Cash Equivalents"), ("總債務", "Total Debt"),
                         ("商譽", "Goodwill"), ("存貨", "Inventory"), ("股東權益", "Stockholders Equity")]:
            rows.append([lab] + [fmt_m(_get(bs_, key, c)) if c in bs_.columns else "—" for c in cols])
        return hdr, rows

    hdr, rows = block(inc, cf, bs, 4)
    pk.add("fin_annual", "年度損益、現金流、資產負債（近 4 個會計年度，yfinance）", md_table(hdr, rows),
           "yfinance", asof=str(inc.columns[0].date()))
    if qinc is not None and len(qinc.columns):
        hdr, rows = block(qinc, qcf, qbs, 8)
        n = min(8, len(qinc.columns))
        pk.add("fin_quarter", "單季損益、現金流、資產負債（近 {0} 季，yfinance）".format(n), md_table(hdr, rows),
               "yfinance", asof=str(qinc.columns[0].date()))
        if n < 8:
            pk.gap("單季報表 yfinance 只回 {0} 季，不足 8 季".format(n))
    else:
        pk.gap("單季報表取不到")
    cols = list(inc.columns)[:4][::-1]
    rows = []
    for c in cols:
        ni, rev = _get(inc, "Net Income", c), _get(inc, "Total Revenue", c)
        ebit, intr = _get(inc, "Operating Income", c), _get(inc, "Interest Expense", c)
        cfo = _get(cf, "Operating Cash Flow", c) if c in cf.columns else None
        sbc = _get(cf, "Stock Based Compensation", c) if c in cf.columns else None
        rep = _get(cf, "Repurchase Of Capital Stock", c) if c in cf.columns else None
        sh = _get(inc, "Diluted Average Shares", c)
        debt = _get(bs, "Total Debt", c) if c in bs.columns else None
        cash = _get(bs, "Cash And Cash Equivalents", c) if c in bs.columns else None
        gw = _get(bs, "Goodwill", c) if c in bs.columns else None
        ta = _get(bs, "Total Assets", c) if c in bs.columns else None
        acq = _get(cf, "Purchase Of Business", c) if c in cf.columns else None
        rows.append([c.strftime("%Y"),
                     "{0:.0f}%".format(cfo / ni * 100) if cfo and ni else "—",
                     "{0:.1f}%".format(sbc / rev * 100) if sbc and rev else "—",
                     fmt_m(rep), "{0:,.0f}".format(sh / 1e6) if sh else "—",
                     fmt_m(debt - cash) if debt is not None and cash is not None else "—",
                     "{0:.1f}x".format(ebit / abs(intr)) if ebit and intr else "—",
                     "{0:.0f}%".format(gw / ta * 100) if gw and ta else "—", fmt_m(acq)])
    pk.add("routine_fin", "例行檢查：獲利品質、股票薪酬、回購、淨負債、利息保障、商譽、併購（年度）",
           md_table(["年度", "營運現金流÷淨利", "股票薪酬÷營收", "回購（百萬，報表幣別）", "稀釋股數（百萬）", "淨負債（百萬，報表幣別）",
                     "利息保障倍數（營業利益÷利息費用）", "商譽÷總資產", "併購支出（百萬，報表幣別）"], rows)
           + "\n（回購與併購支出為負數代表現金流出；程式依 yfinance 欄位自算。）", "yfinance 自算",
           asof=str(inc.columns[0].date()))


def _first(df, names, col):
    for n in names:
        v = _get(df, n, col) if df is not None and col in df.columns else None
        if v is not None:
            return v
    return None


def roic_section(pk, yt):
    """投入資本報酬率逐年＋拆解＋增量（零 LLM，標籤 [p:roic]）。
    算法與同業表（peers.py）相同：稅後營業利益＝營業利益×(1－稅率)，稅率＝所得稅÷稅前淨利（限 0～35%），
    投入資本＝年底（股東權益＋總債務－現金），所以最近一年的數字跟同業表那一格一致。
    另附 dd-screener（Koyfin 資料）同一檔的欄位；口徑不同，分開列。銀行、保險、券商不算。"""
    import peers as pr_
    try:
        info = yt.info or {}
    except Exception:
        info = {}
    if pr_.is_financial(info):
        pk.gap("金融業（銀行、保險、券商）不算投入資本報酬率，資本報酬改看同業表的股東權益報酬率")
        return
    fin_cur = currency_info(yt)[0]
    inc, bs = yt.income_stmt, yt.balance_sheet
    cols = [c for c in list(inc.columns) if _get(inc, "Total Revenue", c) is not None][::-1]  # 舊到新
    years = []
    for c in cols:
        rev, ebit = _get(inc, "Total Revenue", c), _get(inc, "Operating Income", c)
        tax, pti = _get(inc, "Tax Provision", c), _get(inc, "Pretax Income", c)
        eq = _first(bs, ["Stockholders Equity", "Common Stock Equity"], c)
        debt = _first(bs, ["Total Debt"], c)
        cash = _first(bs, ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"], c)
        y = {"fy": str(c.date()), "rev": rev, "ebit": ebit, "tax_rate": None, "nopat": None, "ic": None,
             "nopat_margin": None, "turnover": None, "roic": None}
        if tax is not None and pti:
            y["tax_rate"] = min(max(tax / pti, 0.0), 0.35)
        if ebit is not None and y["tax_rate"] is not None:
            y["nopat"] = ebit * (1 - y["tax_rate"])
        if eq is not None and debt is not None and cash is not None:
            y["ic"] = eq + debt - cash
        if y["nopat"] is not None and rev:
            y["nopat_margin"] = y["nopat"] / rev
        if y["ic"] and y["ic"] > 0:
            if rev:
                y["turnover"] = rev / y["ic"]
            if y["nopat"] is not None:
                y["roic"] = y["nopat"] / y["ic"]
        years.append(y)
    ok = [y for y in years if y["roic"] is not None]
    if not ok:
        pk.gap("投入資本報酬率算不出來（yfinance 年報缺營業利益、稅、權益、債務或現金，或投入資本為負）")
        return

    def p(v):
        return "—" if v is None else "{0:.1f}%".format(v * 100)
    rows = [[y["fy"], fmt_m(y["rev"]), fmt_m(y["ebit"]), p(y["tax_rate"]), fmt_m(y["nopat"]), fmt_m(y["ic"]),
             p(y["nopat_margin"]), "—" if y["turnover"] is None else "{0:.2f}".format(y["turnover"]), p(y["roic"])] for y in years]
    body = ["### 逐年（程式用 yfinance 年報自算，金額單位：百萬{0}）".format(fin_cur), "",
            md_table(["年度（年底）", "營收", "營業利益", "稅率", "稅後營業利益", "投入資本", "稅後營業利益率", "投入資本周轉（次）", "投入資本報酬率"], rows),
            "算法：稅後營業利益＝營業利益×(1－稅率)，稅率＝所得稅費用÷稅前淨利（限制在 0～35%）；投入資本＝年底（股東權益＋總債務－現金）；"
            "投入資本報酬率＝稅後營業利益÷投入資本＝稅後營業利益率×投入資本周轉，投入資本周轉＝營收÷投入資本。最近一年與同業表 [p:peers] 同一格的算法相同。"
            "營業利益若含一次性費用（例如收購研發、減損、訴訟和解），當年的報酬率會被壓低，引用時要講。"]
    inc_ = None
    a, b = ok[0], ok[-1]
    if a is not b and a["ic"] and b["ic"]:
        n = len([y for y in years if a["fy"] < y["fy"] <= b["fy"]])
        d_ic, d_np = b["ic"] - a["ic"], b["nopat"] - a["nopat"]
        cum = sum(y["nopat"] for y in years if a["fy"] < y["fy"] <= b["fy"] and y["nopat"] is not None)
        inc_ = {"from": a["fy"], "to": b["fy"], "years": n, "d_ic": d_ic, "d_nopat": d_np, "cum_nopat": cum,
                "incremental_roic": d_np / d_ic if d_ic > 0 and a["nopat"] > 0 and b["nopat"] > 0 else None,
                "reinvest_rate": d_ic / cum if cum > 0 else None}
        body += ["", "### 增量（{0} → {1}，{2} 個年度）".format(a["fy"], b["fy"], n), ""]
        body.append("- 投入資本增加 {0} 百萬，稅後營業利益增加 {1} 百萬，期間稅後營業利益累計 {2} 百萬。".format(fmt_m(d_ic), fmt_m(d_np), fmt_m(cum)))
        if inc_["incremental_roic"] is not None:
            body.append("- 增量投入資本報酬率＝稅後營業利益增加÷投入資本增加＝{0}。".format(p(inc_["incremental_roic"])))
        elif a["nopat"] <= 0 or b["nopat"] <= 0:
            body.append("- 期初或期末稅後營業利益是負的，增量投入資本報酬率不算（虧損縮小不是投資報酬）。")
        else:
            body.append("- 投入資本沒有增加，增量投入資本報酬率不算。")
        if inc_["reinvest_rate"] is not None:
            body.append("- 再投資率＝投入資本增加÷期間稅後營業利益累計＝{0}。".format(p(inc_["reinvest_rate"])))
        if inc_["incremental_roic"] is not None and inc_["reinvest_rate"] is not None and inc_["reinvest_rate"] > 0:
            body.append("- 兩者相乘＝{0}，是「把賺來的錢照這個報酬率再投進去」時稅後營業利益每年能長多少的粗略上限；投入資本靠舉債或增資增加時會高估。".format(
                p(inc_["incremental_roic"] * inc_["reinvest_rate"])))
    # dd-screener（Koyfin）
    try:
        scr = json.loads((REPO / "docs/dd-screener/latest.json").read_text(encoding="utf-8"))
        row = next((s for s in scr.get("stocks", []) if s.get("ticker") == pk.t), None)
    except Exception:
        row, scr = None, {}
    if row and row.get("roic") is not None:
        def f(k, suf="%"):
            v = row.get(k)
            return "—" if v is None else "{0}{1}".format(v, suf)
        body += ["", "### dd-screener 欄位（Koyfin 資料，資料日 {0}；口徑與上表不同，不要混用）".format(scr.get("as_of") or "—"), ""]
        body.append("- 投入資本報酬率 {0}，三年平均 {1}，五年平均 {2}，現在÷五年平均 {3}（≥1.1 記上升、≤0.9 記下滑）：{4}".format(
            f("roic"), f("roic_3y_avg_pct"), f("roic_5y_avg_pct"), f("roic_vs_5y_x", " 倍"), row.get("roic_trend_5y") or "—"))
        body.append("- 拆解：營業利益率 {0}，稅率 {1}，稅後營業利益率 {2}，投入資本周轉 {3}；歸類「{4}」（稅後營業利益率 15% 與周轉 1 次為分界）".format(
            f("ebit_margin_pct"), f("tax_rate_pct"), f("nopat_margin_pct"), f("ic_turnover_x", " 次"), row.get("roic_quadrant") or "—"))
        body.append("- 近三個會計年度：增量投入資本報酬率 {0}，再投資率 {1}（投入資本增加÷三年稅後營業利益），相乘 {2}".format(
            f("incremental_roic_pct"), f("reinvest_rate_pct"), f("implied_growth_pct")))
        body.append("- Koyfin 的投入資本定義與 yfinance 自算不同（例如是否扣現金、是否含租賃負債），兩組數字差幾個百分點是口徑差，不是錯。")
    else:
        pk.gap("dd-screener 沒有這檔的投入資本報酬率欄位，只有程式自算的逐年數字")
    pk.extra["roic"] = {"currency": fin_cur, "years": years, "incremental": inc_}
    pk.add("roic", "投入資本報酬率（逐年、拆解、增量）", "\n".join(body), "yfinance 年報自算＋dd-screener（Koyfin）", asof=pk.date)


def holders_insiders(pk, yt):
    body = ""
    try:
        it = yt.insider_transactions
        if it is not None and len(it):
            it = it.copy()
            dcol = [c for c in it.columns if "Date" in c][0]
            it[dcol] = pd.to_datetime(it[dcol])
            cut = it[dcol].max() - pd.Timedelta(days=365)
            it = it[it[dcol] >= cut]
            txt = it["Text"].fillna("") if "Text" in it.columns else pd.Series([""] * len(it), index=it.index)
            sale = it[txt.str.contains("Sale", case=False)]
            buy = it[txt.str.contains("Purchase", case=False)]

            def tot(d, col):
                return float(d[col].fillna(0).sum()) if col in d.columns and len(d) else 0.0
            body += "近 12 個月（至 {0}）內部人申報：賣出 {1} 筆、合計 {2:,.0f} 股、約 {3:,.1f} 百萬美元；買進 {4} 筆、合計 {5:,.0f} 股、約 {6:,.1f} 百萬美元。\n".format(
                it[dcol].max().date(), len(sale), tot(sale, "Shares"), tot(sale, "Value") / 1e6,
                len(buy), tot(buy, "Shares"), tot(buy, "Value") / 1e6)
            body += "（其餘為贈與、選擇權行使等 {0} 筆。）\n\n".format(len(it) - len(sale) - len(buy))
            cols = [c for c in ["Insider", "Position", dcol, "Text", "Shares", "Value"] if c in it.columns]
            body += md_table(cols, it.sort_values(dcol, ascending=False).head(12)[cols].astype(str).values.tolist())
        else:
            pk.gap("內部人交易 yfinance 無資料")
    except Exception as e:
        pk.gap("內部人交易取得失敗：{0}".format(str(e)[:80]))
    try:
        mh = yt.major_holders
        if mh is not None and len(mh):
            body += "\n大股東與持股結構：\n" + md_table(["項目", "比例"], [[str(i), "{0:.2%}".format(float(v)) if abs(float(v)) < 5 else str(v)] for i, v in mh["Value"].items()])
        ih = yt.institutional_holders
        if ih is not None and len(ih):
            ih = ih.head(8)
            body += "\n前 8 大機構股東：\n" + md_table(["機構", "占比", "股數"], [[r["Holder"], "{0:.2%}".format(r["pctHeld"]), "{0:,.0f}".format(r["Shares"])] for _, r in ih.iterrows()])
    except Exception as e:
        pk.gap("股東結構取得失敗：{0}".format(str(e)[:80]))
    if body:
        pk.add("routine_holders", "例行檢查：內部人交易與大股東", body, "yfinance", asof=str(dt.date.today()))


# ---------------------------------------------------------------- 價格
def price_section(pk):
    from src.price_store import get_ohlcv
    df = get_ohlcv(pk.t, start="1990-01-01")
    if df.empty:
        pk.gap("價格序列取不到")
        return
    last_d = df.index[-1]
    lc = float(df.iloc[-1]["close"])
    close = df["close"]
    hi_close_d, hi_close = close.idxmax(), float(close.max())
    hi_intra_d, hi_intra = df["high"].idxmax(), float(df["high"].max())
    y = df[df.index > last_d - pd.Timedelta(days=365)]
    wk = close.resample("W-FRI").last().dropna()
    mo = close.resample("ME").last().dropna()

    def ma(s, n):
        return float(s.tail(n).mean()) if len(s) >= n else None

    def rel(v):
        return "—" if v is None else "{0:,.2f}（現價相對 {1:+.1f}%）".format(v, (lc / v - 1) * 100)

    def ret(n):
        return "{0:+.1f}%".format((lc / float(wk.iloc[-n - 1]) - 1) * 100) if len(wk) > n else "—"
    body = (
        "資料為未還原股息的收盤與盤中價（已調拆股），來源 price_store，序列自 {first} 起。\n\n"
        "- 現價（{ld} 收盤）：{lc:,.2f}\n"
        "- 歷史最高收盤（未還原股息）：{hc:,.2f}，日期 {hcd}；現價距該高點 {dh:+.1f}%\n"
        "- 歷史最高盤中價（未還原股息）：{hi:,.2f}，日期 {hid}\n"
        "- 52 週最高盤中／最低盤中：{y_hi:,.2f}（{y_hid}）／{y_lo:,.2f}（{y_lod}）；距 52 週高 {d52:+.1f}%\n"
        "- 週線均線（週五收盤）：10 週 {w10}；30 週 {w30}；40 週 {w40}；52 週 {w52}\n"
        "- 月線均線（月底收盤）：10 個月 {m10}；20 個月 {m20}；40 個月 {m40}\n"
        "- 近 13 週報酬 {r13}；近 26 週報酬 {r26}；近 52 週報酬 {r52}（不含股息）\n"
    ).format(first=df.index[0].date(), ld=last_d.date(), lc=lc, hc=hi_close, hcd=hi_close_d.date(), dh=(lc / hi_close - 1) * 100,
             hi=hi_intra, hid=hi_intra_d.date(), y_hi=y["high"].max(), y_hid=y["high"].idxmax().date(),
             y_lo=y["low"].min(), y_lod=y["low"].idxmin().date(), d52=(lc / y["high"].max() - 1) * 100,
             w10=rel(ma(wk, 10)), w30=rel(ma(wk, 30)), w40=rel(ma(wk, 40)), w52=rel(ma(wk, 52)),
             m10=rel(ma(mo, 10)), m20=rel(ma(mo, 20)), m40=rel(ma(mo, 40)),
             r13=ret(13), r26=ret(26), r52=ret(52))
    dv = df["dividends"]
    ttm_div = float(dv[dv.index > last_d - pd.Timedelta(days=365)].sum())
    body += "- 近 12 個月每股股息合計：{0:.2f}（殖利率 {1:.2f}%）\n".format(ttm_div, ttm_div / lc * 100)
    pk.add("price", "股價位置", body, "price_store（yfinance 未還原股息）", asof=str(last_d.date()))
    m = mo.tail(120)
    mm = [(str(i.date()), round(float(v), 2)) for i, v in m.items()]
    ma10 = [(str(i.date()), round(float(mo.loc[:i].tail(10).mean()), 2)) for i in m.index if len(mo.loc[:i]) >= 10]
    ma20 = [(str(i.date()), round(float(mo.loc[:i].tail(20).mean()), 2)) for i in m.index if len(mo.loc[:i]) >= 20]
    pk.extra["price_chart"] = {"monthly_close": mm, "ma10": ma10, "ma20": ma20, "ath_close": hi_close,
                               "ath_date": str(hi_close_d.date()), "last": lc, "last_date": str(last_d.date())}
    pk.extra["last_price"] = lc
    pk.extra["ttm_div"] = ttm_div


# ---------------------------------------------------------------- 共識
def consensus_section(pk, yt):
    import dd_numbers_extra as nx
    d = dt.datetime.strptime(pk.date, "%Y%m%d")
    lines = []
    src = "yfinance"
    try:
        cr = nx.compute_consensus_revision(pk.t, d)
        ls = cr.get("latest_snapshot") or {}
        if ls.get("fy1") is not None:
            lines.append("Koyfin 快照 {0}：FY1 EPS {1}、FY2 EPS {2}、FY3 EPS {3}（美元；快照檔 {4}）".format(
                ls.get("date"), ls.get("fy1"), ls.get("fy2"), ls.get("fy3"), ls.get("file")))
            p90 = cr.get("snapshot_90d_prior") or {}
            if p90.get("fy1") is not None:
                lines.append("約 90 天前快照 {0}：FY1 {1}、FY2 {2}、FY3 {3}".format(p90.get("date"), p90.get("fy1"), p90.get("fy2"), p90.get("fy3")))
            lines.append("快照是否過期：{0}；EPS 口徑說明：{1}".format(cr.get("stale"), cr.get("eps_basis") or cr.get("note") or "快照未標口徑"))
            src = "Koyfin 快照"
            pk.extra["consensus"] = {"fy1": ls.get("fy1"), "fy2": ls.get("fy2"), "fy3": ls.get("fy3"), "date": ls.get("date")}
        else:
            pk.gap("Koyfin 快照沒有此檔，共識 EPS 只有 yfinance")
    except Exception as e:
        pk.gap("共識修正計算失敗：{0}".format(str(e)[:80]))
    try:
        ee = yt.earnings_estimate
        re_ = yt.revenue_estimate
        lines.append("\nyfinance 共識（對照用）：")
        lines.append(md_table(["期間", "EPS 平均（股價幣別）", "EPS 分析師數", "營收平均（百萬，報表幣別）", "營收分析師數", "營收年增（共識）"],
                              [[i, "{0:.2f}".format(ee.loc[i, "avg"]), int(ee.loc[i, "numberOfAnalysts"]),
                                fmt_m(re_.loc[i, "avg"]), int(re_.loc[i, "numberOfAnalysts"]),
                                "{0:+.1%}".format(re_.loc[i, "growth"]) if pd.notna(re_.loc[i, "growth"]) else "—"]
                               for i in ee.index if i in re_.index and i in ("0y", "+1y")]))
        lines.append("（0y＝本會計年度、+1y＝下一會計年度；yfinance 沒有 FY3 營收共識。）")
    except Exception as e:
        pk.gap("yfinance 共識取得失敗：{0}".format(str(e)[:80]))
    pk.add("consensus", "共識 EPS 與營收（FY1～FY3）", "\n".join(lines), src, asof=pk.date)
    try:
        cs = nx.compute_capital_structure(pk.t, d)
        fin_c, quote_c = cs.get("currency"), cs.get("price_currency")
        if cs.get("fx_mismatch"):
            import multiples as mp
            rt, rd = mp.fx_rate(fin_c, quote_c, d, "end")
            conv = {k: (cs[k] * rt if cs.get(k) is not None else None) for k in ("total_debt_m", "cash_m", "net_debt_m")}
            ev = cs["market_cap_m"] + conv["net_debt_m"] if cs.get("market_cap_m") is not None and conv["net_debt_m"] is not None else None
            body = ("報表幣別 {0}、股價幣別 {1}，下列金額已全部換成 {1}（現匯 1 {0}＝{2:.5f} {1}，{3}）。"
                    "市值 {4:,.0f} 百萬 {1}、總債務 {5:,.0f} 百萬 {1}、現金 {6:,.0f} 百萬 {1}、淨負債 {7:,.0f} 百萬 {1}、企業價值 {8} 百萬 {1}；"
                    "稀釋股數約 {9:,.1f} 百萬（{10}，與股價同一單位口徑）。報表幣別原值：總債務 {11:,.0f}、現金 {12:,.0f}、淨負債 {13:,.0f} 百萬 {0}。").format(
                fin_c, quote_c, rt, rd, cs["market_cap_m"], conv["total_debt_m"], conv["cash_m"], conv["net_debt_m"],
                "{0:,.0f}".format(ev) if ev is not None else "—", cs["shares_diluted_m"] or 0, cs.get("shares_basis"),
                cs["total_debt_m"], cs["cash_m"], cs["net_debt_m"])
        else:
            nz = lambda k: cs.get(k)
            f0 = lambda x: "{0:,.0f}".format(x) if x is not None else "—"
            body = "市值 {0} 百萬、總債務 {1} 百萬、現金 {2} 百萬、淨負債 {3} 百萬、企業價值 {4} 百萬；稀釋股數約 {5:,.1f} 百萬（{6}）。".format(
                f0(cs.get("market_cap_m")), f0(cs.get("total_debt_m")), f0(cs.get("cash_m")), f0(cs.get("net_debt_m")), f0(cs.get("ev_m")),
                cs.get("shares_diluted_m") or 0, cs.get("shares_basis"))
        pk.add("capital", "市值、淨負債、企業價值", body, "yfinance", asof=cs.get("as_of", ""))
    except Exception as e:
        pk.gap("市值與淨負債計算失敗：{0}".format(str(e)[:80]))
    try:
        import yfinance as yf
        import multiples as mp
        fc, qc = mp.currencies(yf.Ticker(pk.t))
        if fc and qc and fc != qc:  # 跨幣別（ADR）：nx 版沒換算，改用 multiples.py 的換算版
            mu = mp.build(pk.t)
            parts = []
            for k, lab in [("pe", "trailing 本益比"), ("ps", "trailing 市銷率"), ("evs", "EV／營收")]:
                st_, now_ = mu["stats"].get(k), (mu.get("now") or {}).get(k)
                if st_ and now_ is not None:
                    parts.append("{0}：現值 {1:.2f}、年度取樣高 {2:.2f}、低 {3:.2f}、中位 {4:.2f}（{5} 個年度點；已換成 {6}）".format(
                        lab, now_, st_["max"], st_["min"], st_["med"], st_["n"], qc))
            if parts:
                pk.add("val_hist", "估值歷史（年度點，trailing 口徑，已換成股價幣別）", "\n".join("- " + x for x in parts), "yfinance＋匯率自算", asof=pk.date)
            return
        vh = nx.compute_valuation_history(pk.t, d)
        tr = vh.get("trailing", {})
        parts = []
        for k, lab in [("pe", "trailing 本益比"), ("ps", "trailing 市銷率"), ("ev_s", "EV/營收")]:
            v = tr.get(k)
            if v:
                parts.append("{0}：現值 {1}、年度取樣高 {2}（{3}）、低 {4}（{5}）、現值在 {6} 個年度點中的分位 {7}%".format(
                    lab, v["current"], v["high"]["value"], v["high"]["date"], v["low"]["value"], v["low"]["date"], v["n_points"], v["current_percentile_within_annual_points"]))
        if parts:
            pk.add("val_hist", "估值歷史（只有 4 到 5 個年度點，trailing 口徑）", "\n".join("- " + x for x in parts), "yfinance 自算", asof=pk.date)
    except Exception as e:
        pk.gap("估值歷史計算失敗：{0}".format(str(e)[:80]))


# ---------------------------------------------------------------- 上一份 DD
def prior_section(pk):
    import dd_sections
    files = sorted(glob.glob(str(REPO / "docs/dd/DD_{0}_*.html".format(pk.t))))
    files = [f for f in files if re.search(r"_(\d{8})\.html$", f)]
    if not files:
        pk.gap("沒有上一份 DD")
        return
    f = files[-1]
    m = dd_sections.dd_meta_json(Path(f).read_text(encoding="utf-8")) or {}
    lab = {"date": "日期", "price_at_dd": "當時股價", "dca_verdict": "裁決", "dca_role": "角色", "oneliner": "一句話結論",
           "rearm_trigger": "重新加碼觸發條件", "bull_5y_price": "樂觀情境五年價", "bear_5y_price": "悲觀情境五年價",
           "p_bull_pct": "樂觀機率%", "p_bear_pct": "悲觀機率%", "irr_base_pct": "基準年化報酬%", "ev5y_pct": "五年期望報酬%",
           "upside_mid_pct": "中期上檔%", "fpe_fy2": "FY2 前瞻本益比", "base_eps_path": "基準 EPS 路徑", "eps_basis": "EPS 口徑",
           "cycle_position": "循環位置", "cycle_verdict": "循環判斷", "kill_metrics": "否證指標", "catalysts": "催化劑",
           "archetype": "類型", "trap_label": "陷阱標籤"}
    lines = []
    for k, name in lab.items():
        v = m.get(k)
        if v in (None, ""):
            continue
        if k in ("kill_metrics", "catalysts"):
            v = "；".join(" / ".join(str(x) for x in (i.values() if isinstance(i, dict) else [i]) if x is not None)[:220] for i in v[:6])
        elif isinstance(v, (dict, list)):
            v = json.dumps(v, ensure_ascii=False)
        lines.append("- {0}：{1}".format(name, v))
    pk.add("prior", "上一份 DD 的結論（現行站上版 {0}，舊流程產出）".format(Path(f).name), "\n".join(lines),
           "docs/dd dd-meta", asof=str(m.get("date", "")))
    pk.extra["prior_file"] = f
    pk.extra["prior_meta"] = {k: m.get(k) for k in lab}



# ---------------------------------------------------------------- 管理層指引紀錄
GUIDE_RE = re.compile(r"(outlook|guidance|guide\b|expects?\b|expected to|forecast|anticipat|we project|target range)", re.I)
HEAD_RE = re.compile(r"^\W*(?:(?:business|financial|fiscal[^\n]{0,20}|q[1-4][^\n]{0,20}|full[- ]year|first|second|third|fourth)\s+)*(?:outlook|guidance)\b[^\n]{0,80}$", re.I)


def fetch_pr_text(ctx, cik, r, accept=None):
    from primary_common import html_to_text
    accn = r["accessionNumber"].replace("-", "")
    base = "https://www.sec.gov/Archives/edgar/data/{0}/{1}/".format(int(cik), accn)
    idx = ctx.http_sec.get(base + "index.json", timeout=30).json()
    items = [(i["name"], int(i.get("size") or 0)) for i in idx["directory"]["item"]]
    htm = [(n, z) for n, z in items if n.lower().endswith((".htm", ".html")) and not re.match(r"R\d+\.htm", n, re.I)
           and "index" not in n.lower() and n != r["primaryDocument"]]
    first = [n for n, z in htm if re.search(r"press|release|earn", n, re.I)]
    second = [n for n, z in htm if re.search(r"99|pr", n, re.I) and n not in first]
    rest = [n for n, z in sorted(htm, key=lambda x: -x[1]) if n not in first and n not in second]
    cands = (first + second + rest) or [r["primaryDocument"]]
    last = None
    for n in cands[:5]:
        txt = html_to_text(ctx.http_sec.get(base + n, timeout=60).text)
        last = (txt, base + n)
        if accept is None or accept(txt):
            return last
    return last if accept is None else (None, None)


def outlook_excerpt(txt, limit=1500):
    """只擷取原文，不判讀。優先找「Outlook／Guidance」標題後的段落；找不到就挑含 expects 且有金額或百分比的連續行。"""
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    start = None
    for i, l in enumerate(lines):
        if len(l) < 100 and HEAD_RE.match(l):
            start = i
            break
    if start is None:
        for i, l in enumerate(lines):
            if re.search(r"\boutlook\b.{0,40}\b(is|for)\b|\bexpects?\b.{0,80}\b(revenue|sales|EPS|earnings)|guidance (is|for)", l, re.I) and re.search(r"\d", l):
                start = i
                break
    if start is None:
        best, bi = 0, None
        for i, l in enumerate(lines):
            if GUIDE_RE.search(l) and re.search(r"[$%]|\d", l) and not re.search(r"forward-looking|safe harbor|private securities", l, re.I):
                sc = 3 * len(re.findall(r"outlook|guidance", l, re.I)) + len(GUIDE_RE.findall(l)) + (2 if re.search(r"(revenue|sales|EPS|earnings per share|margin)", l, re.I) else 0)
                if re.search(r"\breported\b|\bannounced\b", l, re.I) and not re.search(r"outlook|guidance", l, re.I):
                    sc -= 3
                if sc > best:
                    best, bi = sc, i
        start = bi
    if start is None:
        return None
    if not HEAD_RE.match(lines[start]):
        start = max(0, start - 1)
    out, n = [], 0
    for l in lines[start:start + 40]:
        if re.search(r"forward-looking statements|safe harbor", l, re.I) and n > 200:
            break
        out.append(l)
        n += len(l)
        if n >= limit:
            break
    t = "\n".join(out)
    return t[:limit] + ("…" if len(t) > limit else "")


def guidance_history(pk, ctx, cik, rows, yt, quarters=8):
    d = pk.date
    dmax = dt.datetime.strptime(d, "%Y%m%d").date().isoformat()
    # 8-K 看 Item 2.02；外國發行人時期的 6-K 沒有項目編號，抓下來用內容判斷是不是財報稿
    prs = [r for r in rows if r["filingDate"] <= dmax and ((r["form"] == "8-K" and "2.02" in (r["items"] or "")) or r["form"] == "6-K")]
    prs.sort(key=lambda r: r["filingDate"], reverse=True)
    prs = prs[:quarters + 6]
    try:
        qi, ai = yt.quarterly_income_stmt, yt.income_stmt
    except Exception:
        qi = ai = None

    def act(df, col):
        def g(k):
            try:
                v = df.loc[k, col]
                return None if pd.isna(v) else float(v)
            except Exception:
                return None
        rev, gp, eps = g("Total Revenue"), g("Gross Profit"), g("Diluted EPS")
        return "營收 {0}、毛利率 {1}、稀釋 EPS {2}".format(
            "{0:,.0f} 百萬".format(rev / 1e6) if rev else "—", "{0:.1f}%".format(gp / rev * 100) if gp and rev else "—",
            "{0:.2f}".format(eps) if eps is not None else "—")
    got, body = 0, []
    n_done = 0
    for r in prs:
        if n_done >= quarters:
            break
        fd = pd.Timestamp(r["filingDate"])
        try:
            if r["form"] == "6-K":
                txt, url = fetch_pr_text(ctx, cik, r, accept=lambda t: len(t) > 5000 and bool(re.search(r"(first|second|third|fourth) quarter|full[- ]year|fiscal year", t[:3000], re.I))
                                         and bool(re.search(r"results|reports", t[:3000], re.I)) and "INDEX TO CONDENSED" not in t[:600])
                if txt is None:
                    continue
            else:
                txt, url = fetch_pr_text(ctx, cik, r)
            n_done += 1
            ex = outlook_excerpt(txt)
        except Exception as e:
            body.append("### {0} 財報新聞稿\n\n（抓取失敗：{1}）\n".format(r["filingDate"], str(e)[:60]))
            continue
        nq = nyr = "—（yfinance 沒有）"
        if qi is not None and len(qi.columns):
            later = [c for c in qi.columns if c > fd]
            if later:
                nq = "{0} 季（季末 {1}）：".format("下一", min(later).date()) + act(qi, min(later))
        if ai is not None and len(ai.columns):
            later = [c for c in ai.columns if c > fd - pd.Timedelta(days=45)]
            if later:
                nyr = "會計年度（年底 {0}）：".format(min(later).date()) + act(ai, min(later))
        if ex:
            got += 1
        body.append("### {0} 財報新聞稿的展望段落原文（{1}）\n\n{2}\n\n- 之後實際，下一季：{3}\n- 之後實際，該年度：{4}\n".format(
            r["filingDate"], url, ex or "（找不到展望或指引段落）", nq, nyr))
    eh = ""
    try:
        h = yt.earnings_history
        if h is not None and len(h):
            eh = "\n### 共識對實際（yfinance earnings_history，每股盈餘）\n\n" + md_table(
                ["季度", "共識 EPS", "實際 EPS", "差距%"],
                [[str(i.date()) if hasattr(i, "date") else str(i), "{0:.2f}".format(r["epsEstimate"]) if pd.notna(r.get("epsEstimate")) else "—",
                  "{0:.2f}".format(r["epsActual"]) if pd.notna(r.get("epsActual")) else "—",
                  "{0:+.1f}".format(r["surprisePercent"] * 100) if pd.notna(r.get("surprisePercent")) and abs(r["surprisePercent"]) < 5 else (str(r.get("surprisePercent")))]
                 for i, r in h.iterrows()])
    except Exception as e:
        pk.gap("earnings_history 取得失敗：{0}".format(str(e)[:60]))
    prs = prs[:max(n_done, 1)] if n_done else prs[:0]
    head = ("過去 {0} 季財報新聞稿（EDGAR 8-K／6-K 附件）裡的展望段落原文，每季截到約 1,500 字元；下面的「實際」來自 yfinance，"
            "季報只回約 6 季，較舊的季度沒有，可以直接讀下一季新聞稿的實際數。程式只擷取原文與實際數，沒有判讀指引數字。\n").format(n_done)
    pk.add("guidance_history", "管理層指引紀錄（近 {0} 季展望原文與之後的實際）".format(n_done), head + "\n" + "\n".join(body) + eh,
           "SEC EDGAR 8-K 附件 99.1＋yfinance", asof=pk.date)
    pk.extra["guidance_quarters_with_text"] = got
    pk.extra["guidance_quarters_total"] = n_done
    if n_done < quarters:
        pk.gap("指引紀錄：只找到 {0} 份財報新聞稿（要求 {1} 份）".format(n_done, quarters))
    if got < n_done:
        pk.gap("指引紀錄：{0} 份新聞稿中只有 {1} 份找得到展望段落".format(n_done, got))


# ---------------------------------------------------------------- EDGAR
NEWS_PER, NEWS_TOTAL = 6000, 30000


def news_section(pk, ctx, cik, rows, d, pr_rows):
    """財報後公司公告：最新一次財報 8-K（Item 2.02）申報日前 7 天到今天的所有 8-K／6-K，含本文 Item 敘述與附件 99.x。新到舊。"""
    from primary_common import html_to_text
    if pr_rows:
        anchor = pr_rows[0]["filingDate"]
        start = (dt.datetime.strptime(anchor, "%Y-%m-%d").date() - dt.timedelta(days=7)).isoformat()
        pr_acc = pr_rows[0]["accessionNumber"]
    else:  # 外國發行人 6-K 沒有 Item 編號，找不到「最新一次財報申報日」：改取備料日前 45 天內
        anchor = None
        start = (d - dt.timedelta(days=45)).isoformat()
        pr_acc = None
    cand = [r for r in rows if r["form"] in ("8-K", "6-K") and start <= r["filingDate"] <= d.isoformat()]
    cand.sort(key=lambda r: (r["filingDate"], r["accessionNumber"]), reverse=True)
    blocks, errs = [], 0
    for r in cand:
        items = (r["items"] or "").strip()
        its = [x.strip() for x in items.split(",") if x.strip()]
        if r["accessionNumber"] == pr_acc and set(its) <= {"2.02", "9.01"}:
            continue  # 財報新聞稿本身已放在 [p:pr]
        accn = r["accessionNumber"].replace("-", "")
        base = "https://www.sec.gov/Archives/edgar/data/{0}/{1}/".format(int(cik), accn)
        try:
            idx = ctx.http_sec.get(base + "index.json", timeout=30).json()
            files = [i["name"] for i in idx["directory"]["item"]]
            main = r["primaryDocument"]
            mt = html_to_text(ctx.http_sec.get(base + main, timeout=60).text) if main else ""
            m = re.search(r"(?im)^\s*item\s+\d\.\d\d", mt)
            if m:
                mt = mt[m.start():]
            if r["form"] == "8-K":
                mt = re.split(r"(?im)^\s*signatures?\s*$", mt)[0].strip()
            others = [n for n in files if n.lower().endswith((".htm", ".html")) and n != main and not re.match(r"R\d+\.htm", n, re.I) and "index" not in n.lower()]
            ex = [n for n in others if re.search(r"99|ex|press|release", n, re.I)] or others if r["form"] == "8-K" else others
            et = ""
            for n in ex[:3]:
                t = html_to_text(ctx.http_sec.get(base + n, timeout=60).text).strip()
                t = re.sub(r"\A(?:(?:EX-[\d.]+|\d{1,2}|[\w.\-]+\.html?|Document)\s*\n)+", "", t).strip()
                if len(t) > 200:
                    et += ("\n\n" if et else "") + t
            if r["form"] == "6-K":  # 6-K 本文只是封面，內容在附件；沒有附件才用封面之後的文字
                ls_ = mt.split("\n")
                di = [i for i, l in enumerate(ls_) if re.match(r"(?i)\s*date\s*:", l)]
                k = max([i for i, l in enumerate(ls_) if "101(b)(7)" in l] or [-1])
                if di:  # 封面→簽名頁（Date: 之後兩行是簽署人與職稱）→ 公告內容
                    mt = "\n".join(ls_[di[0] + 3:]).strip()
                elif k >= 0:
                    mt = "\n".join(ls_[k + 1:]).strip()
            body = mt
            if et:
                body = (body + "\n\n【附件新聞稿】\n" + et) if body else et
            elif not body:
                body = mt
            body = body.strip()
            if not body:
                continue
            first = next((l.strip() for l in (mt if r["form"] == "6-K" else (et or mt)).split("\n") if len(l.strip()) > 12 and not re.match(r"(?i)item\s+\d|.*\.htm$|exhibit", l.strip())), "")
            title = re.sub(r"\s+", " ", first)[:60]
            head = "### {0}｜{1}｜{2}".format(r["filingDate"], ("Item " + "、".join(its)) if its else r["form"] + "（無 Item，外國發行人）", title)
            blocks.append((r["filingDate"], head, clip(body, NEWS_PER, "公告 " + r["filingDate"]), len(body)))
        except Exception as e:
            errs += 1
            pk.gap("財報後公告抓取失敗 {0} {1}：{2}".format(r["form"], r["filingDate"], str(e)[:60]))
    if not blocks:
        if cand and errs == len(cand):
            pk.gap("財報後公司公告全部抓取失敗")
        return
    out, used, dropped = [], 0, 0
    for _, head, body, _n in blocks:
        if used + len(body) + len(head) > NEWS_TOTAL and out:
            dropped += 1
            continue
        out.append(head + "\n\n" + body)
        used += len(body) + len(head)
    note = ("（涵蓋 {0} 至 {1} 的 8-K／6-K，最新一次財報申報日 {2} 前 7 天起；新到舊。財報新聞稿本身見 [p:pr]。）".format(start, d.isoformat(), anchor) if anchor else
            "（涵蓋 {0} 至 {1} 的 6-K：外國發行人沒有 Item 2.02 可定位最新財報，改取備料日前 45 天；新到舊。）".format(start, d.isoformat()))
    if dropped:
        note += "\n（超過總長上限，較舊的 {0} 則未放入。）".format(dropped)
    pk.add("news", "財報後公司公告（8-K／6-K，最新一次財報申報日前 7 天起）", note + "\n\n" + "\n\n".join(out), "SEC EDGAR 8-K／6-K",
           "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type=&dateb=&owner=include&count=40".format(int(cik)), d.isoformat())
    pk.extra["news_count"] = len(out)


def edgar(pk):
    import primary_docs as pdocs
    import primary_us as us
    from primary_common import html_to_text
    d = dt.datetime.strptime(pk.date, "%Y%m%d").date()
    ctx = pdocs._make_ctx(pk.t, "us", pk.t, "", d, PILOT / "runs" / "_tmp")
    cik, sub = us.fetch_submissions(ctx)
    rows = list(us._recent_rows(sub))
    pr_rows = [r for r in rows if r["form"] in ("8-K", "6-K") and "2.02" in (r["items"] or "") and r["filingDate"] <= d.isoformat()]
    pr_rows.sort(key=lambda r: r["filingDate"], reverse=True)
    pr_done = False
    for r in pr_rows[:2]:
        accn = r["accessionNumber"].replace("-", "")
        base = "https://www.sec.gov/Archives/edgar/data/{0}/{1}/".format(int(cik), accn)
        try:
            idx = ctx.http_sec.get(base + "index.json", timeout=30).json()
            items = [(i["name"], int(i.get("size") or 0)) for i in idx["directory"]["item"]]
            htm = [(n, z) for n, z in items if n.lower().endswith((".htm", ".html")) and not re.match(r"R\d+\.htm", n, re.I)
                   and "index" not in n.lower() and n != r["primaryDocument"]]
            pref = [n for n, z in htm if re.search(r"99|earn|release|press|pr", n, re.I)]
            cands = pref or [n for n, z in sorted(htm, key=lambda x: -x[1])] or [r["primaryDocument"]]
            txt = html_to_text(ctx.http_sec.get(base + cands[0], timeout=60).text)
            if len(txt) < 3000:
                continue
            pk.add("pr", "最新一季財報新聞稿（{0} Item 2.02，{1}，附件 {2}）".format(r["form"], r["filingDate"], cands[0]),
                   clip(txt, CAPS["pr"], "新聞稿"), "SEC EDGAR " + r["form"], base + cands[0], r["filingDate"])
            pk.extra["pr_date"] = r["filingDate"]
            pr_done = True
            break
        except Exception as e:
            pk.gap("新聞稿抓取失敗 {0}：{1}".format(r["filingDate"], str(e)[:80]))
    if not pr_done:
        pk.gap("最新財報新聞稿（8-K Item 2.02 附件 99.1）取不到")
    try:
        news_section(pk, ctx, cik, rows, d, pr_rows)
    except Exception as e:
        pk.gap("財報後公司公告區段失敗：{0}".format(str(e)[:80]))
    try:
        import yfinance as _yf
        guidance_history(pk, ctx, cik, rows, _yf.Ticker(pk.t), 8)
    except Exception as e:
        pk.gap("指引紀錄建置失敗：{0}".format(str(e)[:100]))
    row = us.pick_annual_filing(sub, d.isoformat())
    if not row:
        pk.gap("EDGAR 沒有 10-K／20-F")
        return
    form = row["form"]
    url = us.filing_url(cik, row)
    try:
        text = html_to_text(ctx.http_sec.get(url, timeout=90).text)
        lines, spans = us.split_sections(text, form)
        pk.extra["annual_url"] = url
        for role, tag, ttl in [("business", "biz", "業務"), ("risk", "risk", "風險因素"), ("mda", "mda", "MD&A")]:
            iid = us.ROLE[form][role]
            if iid not in spans:
                pk.gap("年報 {0} 章節沒切出來".format(ttl))
                continue
            a, b = spans[iid]
            body = "\n".join(l for l in lines[a:b] if len(l) > 3)
            pk.add(tag, "最新年報（{0}，申報 {1}）：{2}".format(form, row["filingDate"], ttl),
                   clip(body, CAPS[tag], ttl), "SEC EDGAR " + form, url, row["filingDate"])
    except Exception as e:
        pk.gap("年報抓取或切節失敗：{0}".format(str(e)[:100]))
    qs = [r for r in rows if r["form"] == "10-Q" and r["filingDate"] <= d.isoformat()]
    qs.sort(key=lambda r: r["filingDate"], reverse=True)
    if qs:
        try:
            q = qs[0]
            qurl = us.filing_url(cik, q)
            qt = html_to_text(ctx.http_sec.get(qurl, timeout=90).text)
            ms = [x.start() for x in re.finditer(r"(?im)^\s*item\s*2\.?\s*management[’']?s\s+discussion", qt)]
            if ms:
                start = ms[-1] if len(ms) > 1 else ms[0]
                pk.add("q_mda", "最新 10-Q（申報 {0}）MD&A 開頭（含分部與業績驅動）".format(q["filingDate"]),
                       clip(qt[start:start + 18000], 14000, "10-Q MD&A"), "SEC EDGAR 10-Q", qurl, q["filingDate"])
            else:
                pk.gap("10-Q MD&A 切不出來")
        except Exception as e:
            pk.gap("10-Q 抓取失敗：{0}".format(str(e)[:80]))


# ---------------------------------------------------------------- 逐字稿
def transcript(pk):
    d = DRIVE / pk.t
    fs = sorted(glob.glob(str(d / "{0}_Q*_Earnings_Call_*.md".format(pk.t))), key=lambda f: re.search(r"(\d{8})\.md$", f).group(1))
    fs = [f for f in fs if re.search(r"(\d{8})\.md$", f).group(1) <= pk.date]
    # 財報與投資人日合開的公司（例如 CLS 2026-10-27）只有投資人日逐字稿；比最新一季法說還新才採用
    iv = [f for f in glob.glob(str(d / "{0}_Analyst_Investor_Day_*.md".format(pk.t)))
          if re.search(r"(\d{8})\.md$", f) and re.search(r"(\d{8})\.md$", f).group(1) <= pk.date]
    if iv:
        lv = max(iv, key=lambda f: re.search(r"(\d{8})\.md$", f).group(1))
        if not fs or re.search(r"(\d{8})\.md$", lv).group(1) > re.search(r"(\d{8})\.md$", fs[-1]).group(1):
            fs.append(lv)
    if not fs:
        pk.gap("磁碟上沒有法說逐字稿")
        return
    f = fs[-1]
    txt = Path(f).read_text(encoding="utf-8")
    cd = re.search(r"(\d{8})\.md$", f).group(1)
    pk.add("call", "最新法說逐字稿全文（{0}）".format(Path(f).name), clip(txt, CAPS["call"], "逐字稿"),
           "Koyfin 逐字稿（磁碟）", asof=cd)
    pr = pk.extra.get("pr_date", "")
    if pr and pr.replace("-", "") > cd:
        pk.gap("最新逐字稿（{0}）比最新財報新聞稿（{1}）舊".format(cd, pr))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--date", default=dt.date.today().strftime("%Y%m%d"))
    a = ap.parse_args()
    import yfinance as yf
    t = a.ticker.upper()
    pk = Pack(t, a.date)
    run = PILOT / "runs" / "{0}_{1}".format(t, a.date)
    run.mkdir(parents=True, exist_ok=True)
    yt = yf.Ticker(t)
    steps = [("price", lambda: price_section(pk)), ("fin", lambda: fin_tables(pk, yt)), ("fx", lambda: currency_section(pk, yt)),
             ("holders", lambda: holders_insiders(pk, yt)), ("consensus", lambda: consensus_section(pk, yt)), ("roic", lambda: roic_section(pk, yt)),
             ("prior", lambda: prior_section(pk)), ("edgar", lambda: edgar(pk)), ("call", lambda: transcript(pk))]
    for name, fn in steps:
        try:
            fn()
        except Exception as e:
            import traceback
            traceback.print_exc()
            pk.gap("步驟 {0} 失敗：{1}".format(name, str(e)[:120]))
    order = ["prior", "news", "price", "fx", "consensus", "capital", "val_hist", "fin_annual", "roic", "fin_quarter", "routine_fin", "routine_holders",
             "pr", "guidance_history", "call", "q_mda", "biz", "risk", "mda"]
    pk.sections.sort(key=lambda s: order.index(s[0]) if s[0] in order else 99)
    md = pk.md()
    limit, shrunk = 170 * 1000, []
    for tag, f in [("mda", 0.7), ("risk", 0.7), ("biz", 0.7), ("q_mda", 0.7), ("mda", 0.7), ("risk", 0.7)]:
        if len(md.encode()) <= limit:
            break
        for i, (tg, ttl, body) in enumerate(pk.sections):
            if tg == tag:
                raw = re.sub(r"\n\n\[截斷：.*\]$", "", body, flags=re.S)
                pk.sections[i] = (tg, ttl, clip(raw, int(len(raw) * f), ttl))
                shrunk.append(tag)
        md = pk.md()
    if shrunk:
        pk.gap("pack 超過 170KB，年報／10-Q 分節再截短：" + "、".join(shrunk))
        md = pk.md()
    (run / "pack.md").write_text(md, encoding="utf-8")
    (run / "pack.json").write_text(json.dumps({"ticker": t, "date": a.date, "tags": pk.tags, "gaps": pk.gaps, **pk.extra},
                                              ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    try:  # 零 LLM 加掛模組資料（錢花到哪裡、現金轉換天數、利潤率走勢、共識修正），排版時插入
        import extras
        extras.build(t, run)
    except Exception as e:
        print("extras 失敗（不影響資料包）：" + str(e)[:120])
    print("{0}: pack.md {1:,} bytes".format(t, len(md.encode())))
    for tag, ttl, body in pk.sections:
        print("  {0:16s} {1:>7,} 字元".format(tag, len(body)))
    print("  缺口：", pk.gaps or "無")


if __name__ == "__main__":
    main()
