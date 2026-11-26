#!/usr/bin/env python3
"""dd5 同業對照表（零 LLM）。出題後、寫作前由程式算，標籤 [p:peers]。

每家（含本檔）近三個年度：營收成長、毛利率、營益率、投入資本報酬率、資本支出占營收、研發占營收；
加現在的過去十二個月本益比、預估本益比、市銷率、市值。
投入資本報酬率 ＝ 稅後營業利益 ÷（股東權益＋有息負債－現金），稅後營業利益＝營業利益×(1－稅率)，
稅率＝所得稅費用÷稅前淨利（限制在 0～35%，算不出來就留空）；分母用該年度年底餘額。
yfinance 抓不到的格子留空，不估。外國代號抓不到就略過該家並記在缺口。

用法：python3 scripts/dd5/peers.py TICKER PEER1,PEER2,... [--out DIR]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


def _g(df, names, col):
    if df is None or col not in df.columns:
        return None
    for n in ([names] if isinstance(names, str) else names):
        if n in df.index:
            v = df.loc[n, col]
            if pd.notna(v):
                return float(v)
    return None


def company(t):
    """回傳 dict：years（近三年各指標）、val（現在的倍數）；失敗丟例外。"""
    import yfinance as yf
    yt = yf.Ticker(t)
    inc, bs, cf = yt.income_stmt, yt.balance_sheet, yt.cashflow
    if inc is None or inc.empty:
        raise ValueError("沒有年度損益表")
    cols = list(inc.columns)  # 新到舊
    out = []
    for i, c in enumerate(cols[:3]):
        rev = _g(inc, "Total Revenue", c)
        prev = _g(inc, "Total Revenue", cols[i + 1]) if i + 1 < len(cols) else None
        gp, ebit = _g(inc, "Gross Profit", c), _g(inc, "Operating Income", c)
        rd = _g(inc, "Research And Development", c)
        tax, pti = _g(inc, "Tax Provision", c), _g(inc, ["Pretax Income"], c)
        eq = _g(bs, ["Stockholders Equity", "Common Stock Equity"], c)
        debt = _g(bs, "Total Debt", c)
        cash = _g(bs, ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"], c)
        capex = _g(cf, "Capital Expenditure", c)
        ni = _g(inc, ["Net Income Common Stockholders", "Net Income"], c)
        ceq = _g(bs, ["Common Stock Equity", "Stockholders Equity"], c)
        nie = _g(inc, "Non Interest Expense", c)
        roic = None
        if ebit is not None and tax is not None and pti and eq is not None and debt is not None and cash is not None:
            tr = min(max(tax / pti, 0.0), 0.35)
            ic = eq + debt - cash
            if ic > 0:
                roic = ebit * (1 - tr) / ic
        out.append({"fy": str(c.date()),
                    "growth": (rev / prev - 1) if rev and prev else None,
                    "gm": gp / rev if gp is not None and rev else None,
                    "om": ebit / rev if ebit is not None and rev else None,
                    "roic": roic,
                    "capex": abs(capex) / rev if capex is not None and rev else None,
                    "rd": rd / rev if rd is not None and rev else None,
                    # 金融股用：股東權益報酬率（普通股淨利÷年底普通股權益）、效率比（非利息費用÷營收，只有報表有「Non Interest Expense」才算）
                    "roe": ni / ceq if ni is not None and ceq and ceq > 0 else None,
                    "eff": nie / rev if nie is not None and rev else None,
                    "ptm": pti / rev if pti is not None and rev else None})
    info = {}
    try:
        info = yt.info or {}
    except Exception:
        pass
    val = _val(yt, info)
    fin = is_financial(info)
    if fin:
        _pb(val, info, bs)
    return {"years": out, "val": val, "fin": fin}


def is_financial(info):
    """銀行、保險、券商（yfinance 產業 banks-*、insurance-*、capital-markets）。支付、資產管理、交易所不算。"""
    k = info.get("industryKey") or ""
    return info.get("sector") == "Financial Services" and (k.startswith(("banks-", "insurance")) or k == "capital-markets")


def _pb(v, info, bs):
    """股價淨值比＝info.priceToBook；用「市值÷最近年度年底普通股權益」交叉核對（同幣別才核對），差超過 35% 就留空。
    （例：BRK-B 的 priceToBook 因 A／B 股別算出 0.001，會被擋下。）"""
    v["pb"] = None
    pb, mcap = info.get("priceToBook"), info.get("marketCap")
    if not pb:
        v["notes"].append("股價淨值比：yfinance 沒有 priceToBook")
        return
    try:
        eq = _g(bs, ["Common Stock Equity", "Stockholders Equity"], bs.columns[0])
    except Exception:
        eq = None
    cur, fin_cur = info.get("currency"), info.get("financialCurrency")
    if mcap and eq and eq > 0 and cur and cur == fin_cur:
        chk = mcap / eq
        if abs(pb / chk - 1) > 0.35:
            v["notes"].append("股價淨值比：priceToBook {0:.2f} 與市值÷年底普通股權益 {1:.2f} 差超過 35%，留空".format(pb, chk))
            return
    elif not (mcap and eq):
        v["notes"].append("股價淨值比：無法交叉核對，採 yfinance priceToBook")
    v["pb"] = float(pb)


def _val(yt, info):
    """現在的倍數，全部在該公司報價幣別內算：
    過去十二個月本益比＝股價÷最近四季稀釋 EPS 加總（報表幣別以該四季平均匯率換成報價幣別）；
    預估本益比＝股價÷info.forwardEps（報價幣別），並用 info.forwardPE 交叉核對；
    市銷率＝市值÷最近四季營收（同樣換幣別）。算不出或落在 3～200 倍之外就留空並記 notes。"""
    import multiples as mp
    cur, fin = info.get("currency"), info.get("financialCurrency")
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    mcap = info.get("marketCap")
    v = {"cur": cur, "fin_cur": fin, "mcap": mcap, "pe_ttm": None, "pe_fwd": None, "ps": None, "notes": []}
    if not price:
        v["notes"].append("沒有股價")
        return v
    fa = 1.0
    try:
        qi = yt.quarterly_income_stmt
        cols = [c for c in qi.columns if _g(qi, "Total Revenue", c) is not None][:4]
        gaps = [(cols[i] - cols[i + 1]).days for i in range(len(cols) - 1)]
        if len(cols) == 4 and max(gaps) > 100:  # yfinance 缺季：四欄不連續就不算過去十二個月倍數
            v["notes"].append("最近四季不連續（缺季），過去十二個月本益比與市銷率留空")
        elif len(cols) == 4:
            if fin and cur and fin != cur:
                fa, _ = mp.fx_rate(fin, cur, cols[0], "avg")
            es = [_g(qi, "Diluted EPS", c) for c in cols]
            if all(e is not None for e in es):
                eps_ttm = sum(es)
            else:  # 季報沒有 EPS：改用四季淨利加總÷最近一季稀釋平均股數
                ni = [_g(qi, ["Net Income Common Stockholders", "Net Income"], c) for c in cols]
                sh = _g(qi, "Diluted Average Shares", cols[0])
                eps_ttm = sum(ni) / sh if sh and all(x is not None for x in ni) else None
                if eps_ttm is not None:
                    v["notes"].append("過去十二個月 EPS 缺，改用四季淨利加總÷最近一季稀釋股數")
            if eps_ttm is not None and eps_ttm > 0:
                v["pe_ttm"] = price / (eps_ttm * fa)
            elif eps_ttm is not None:
                v["notes"].append("過去十二個月 EPS 為負，本益比留空")
            rev = sum(_g(qi, "Total Revenue", c) for c in cols) * fa
            if mcap and rev > 0:
                v["ps"] = mcap / rev
        else:
            v["notes"].append("單季報表不足四季")
    except Exception as e:
        v["notes"].append("過去十二個月倍數算不出（{0}）".format(str(e)[:50]))
    fe, fpe = info.get("forwardEps"), info.get("forwardPE")
    if fe and fe > 0:
        pf = price / fe
        if fpe and abs(pf / fpe - 1) > 0.05:
            v["notes"].append("預估本益比：forwardEps 與 forwardPE 對不上（{0:.1f} 對 {1:.1f}），留空".format(pf, fpe))
        else:
            v["pe_fwd"] = pf
    elif fpe:
        v["notes"].append("預估本益比：yfinance 只有 forwardPE {0:.1f}、沒有 forwardEps，口徑與幣別無法核對，留空".format(fpe))
    for k, lab in (("pe_ttm", "過去十二個月本益比"), ("pe_fwd", "預估本益比")):
        if v[k] is not None and not (3 <= v[k] <= 200):
            v["notes"].append("{0} 算出 {1:.1f} 倍，落在 3～200 之外，視為異常留空".format(lab, v[k]))
            v[k] = None
    return v


PICK_PROMPT = """公司：{t}（{name}）
yfinance 產業：{industry}
業務簡介：{summary}

請點名 6～8 家「產品與客戶直接重疊、投資人會拿來比的上市對手」，依相關度由高到低排序。
規則：
- 寧可少不要湊；只有 3 家真正對得上，就只給 3 家。
- 同產業但生意不同的不要（例如晶圓代工不要拿 IC 設計公司來比，床墊、家具不要拿來比小家電）。
- 不要未上市公司，不要已下市或已被併購的公司。
- code 要是 yfinance 代號；海外公司要帶交易所後綴，例如 005930.KS、SU.PA、2379.TW、0981.HK、DLG.MI、BRG.AX、688169.SS。
只輸出一個 JSON 物件，前後不要其他文字：
{{"peers": [{{"code": "...", "name": "公司名", "why": "一句話：為什麼是對手"}}]}}
"""


def pick_prompt(ticker):
    """組給 haiku 的點名提示詞；抓不到公司資料丟例外。"""
    import yfinance as yf
    info = yf.Ticker(ticker.upper()).info or {}
    name = info.get("longName") or info.get("shortName")
    if not name:
        raise ValueError("yfinance 沒有 {0} 的公司資料".format(ticker))
    return PICK_PROMPT.format(t=ticker.upper(), name=name, industry=info.get("industry") or "（無）",
                              summary=(info.get("longBusinessSummary") or "（無）")[:900])


def verify_peer(code):
    """代號驗證：yfinance 查得到、年度損益表有營收。回傳 (ok, 原因)。"""
    import yfinance as yf
    try:
        inc = yf.Ticker(code).income_stmt
    except Exception as e:
        return False, "查詢失敗（{0}）".format(str(e)[:60])
    if inc is None or inc.empty:
        return False, "沒有年度損益表"
    if _g(inc, "Total Revenue", inc.columns[0]) is None:
        return False, "最新年度營收是空的"
    return True, ""


def verify_picks(ticker, picks, n=5):
    """picks：haiku 回的 [{code, name, why}]。回傳 (驗過的前 n 家代號, 逐筆驗證紀錄)。"""
    good, log, seen = [], [], {ticker.upper()}
    for p in picks:
        code = str((p or {}).get("code") or "").strip().upper()
        if not code:
            log.append({"code": "", "kept": False, "reason": "沒有代號"})
            continue
        if code in seen:
            log.append({"code": code, "kept": False, "reason": "重複或就是本檔"})
            continue
        seen.add(code)
        if len(good) >= n:
            log.append({"code": code, "kept": False, "reason": "已湊滿 {0} 家，未驗證".format(n)})
            continue
        ok, why = verify_peer(code)
        log.append({"code": code, "kept": ok, "reason": why})
        if ok:
            good.append(code)
    return good, log


def auto_peers(ticker, n=5, pool=25):
    """沒有人工名單時自動挑同業：yfinance 的產業（industryKey）→ Industry.top_companies 前 pool 名，
    排除本檔，依市值（換成美元）跟本檔的對數距離由近到遠取 n 家。只做到「同一個 yfinance 產業」這一層，
    產業分得粗（例如半導體不分晶圓代工、IC 設計、記憶體），名單要人看過。
    回傳 (peers, notes)；產業抓不到就回傳 ([], [原因])，不補湊。"""
    import math
    import yfinance as yf
    t = ticker.upper()
    notes = []
    try:
        info = yf.Ticker(t).info or {}
        key = info.get("industryKey")
        if not key:
            return [], ["同業名單自動產生失敗：yfinance 沒有 {0} 的產業分類".format(t)]
        tc = yf.Industry(key).top_companies
    except Exception as e:
        return [], ["同業名單自動產生失敗（{0}）".format(str(e)[:60])]
    if tc is None or len(tc) == 0:
        return [], ["同業名單自動產生失敗：yfinance 產業 {0} 沒有公司清單".format(key)]
    fx_cache = {}

    def usd_mcap(inf):
        mc, cur = inf.get("marketCap"), inf.get("currency") or "USD"
        if not mc:
            return None
        if cur == "USD":
            return float(mc)
        if cur not in fx_cache:
            try:
                fx_cache[cur] = float(yf.Ticker(cur + "USD=X").history(period="5d")["Close"].dropna().iloc[-1])
            except Exception:
                fx_cache[cur] = None
        return float(mc) * fx_cache[cur] if fx_cache[cur] else None

    mine = usd_mcap(info)
    if not mine:
        return [], ["同業名單自動產生失敗：算不出 {0} 的美元市值".format(t)]
    scored = []
    for sym in list(tc.index)[:pool]:
        if str(sym).upper() == t:
            continue
        try:
            m = usd_mcap(yf.Ticker(sym).info or {})
        except Exception:
            m = None
        if m:
            scored.append((abs(math.log(m / mine)), str(sym)))
    scored.sort()
    picks = [s for _, s in scored[:n]]
    notes.append("同業名單由程式自動產生：yfinance 產業「{0}」前 {1} 大公司中，取市值（換成美元）與本檔最接近的 {2} 家；產業分類很粗，名單未經人看過".format(info.get("industry") or key, pool, len(picks)))
    if len(picks) < 4:
        notes.append("自動同業只湊到 {0} 家，少於 4 家".format(len(picks)))
    return picks, notes


def pct(x, d=1):
    return "" if x is None else "{0:.{1}f}%".format(x * 100, d)


def num(x, d=1):
    return "" if x is None or (isinstance(x, float) and pd.isna(x)) else "{0:,.{1}f}".format(x, d)


def build(ticker, peers, extra_gaps=None):
    names = [ticker.upper()] + [p.upper() for p in peers if p.upper() != ticker.upper()]
    data, gaps = {}, list(extra_gaps or [])
    for t in names:
        try:
            data[t] = company(t)
        except Exception as e:
            gaps.append("同業 {0} 抓不到（{1}），略過".format(t, str(e)[:60]))
    fin_mode = bool(data.get(ticker.upper(), {}).get("fin"))  # 本檔是銀行／保險／券商才換欄位；非金融股輸出不變
    eff_any = any(y["eff"] is not None for d in data.values() for y in d["years"])
    if fin_mode:
        hdr = ["公司", "年度（年底）", "營收成長", "股東權益報酬率", "稅前淨利率（稅前淨利÷營收）"] + (["效率比（非利息費用÷營收）"] if eff_any else [])
        keys = ("growth", "roe", "ptm", "eff")
        if not eff_any:
            gaps.append("效率比缺：yfinance 報表沒有非利息費用總額（只有拆開的細項），程式不拿其他科目湊")
    else:
        hdr = ["公司", "年度（年底）", "營收成長", "毛利率", "營益率", "投入資本報酬率", "資本支出÷營收", "研發÷營收"]
        keys = ("growth", "gm", "om", "roic", "capex", "rd")
    rows = []
    for t, d in data.items():
        for y in reversed(d["years"]):
            if all(y[k] is None for k in keys):
                gaps.append("{0} {1} 年度資料全空（yfinance 尚未提供），略過該列".format(t, y["fy"]))
                continue
            name = ("**" + t + "**（本檔）") if t == ticker.upper() else t
            if fin_mode:
                rows.append([name, y["fy"], pct(y["growth"]), pct(y["roe"]), pct(y["ptm"])] + ([pct(y["eff"])] if eff_any else []))
            else:
                rows.append([name, y["fy"], pct(y["growth"]), pct(y["gm"]), pct(y["om"]), pct(y["roic"]), pct(y["capex"]), pct(y["rd"])])
    s = "| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr) + "\n" + "\n".join("| " + " | ".join(r) + " |" for r in rows) + "\n"
    vh = ["公司", "市值（百萬，報價幣別）", "過去十二個月本益比", "預估本益比（yfinance 預估 EPS）", "過去十二個月市銷率"]
    if fin_mode:
        vh[4] = "股價淨值比"
    vr = []
    for t, d in data.items():
        v = d["val"]
        last = num(v.get("pb"), 2) if fin_mode else num(v.get("ps"), 2)
        vr.append([t, ("{0:,.0f} {1}".format(v["mcap"] / 1e6, v["cur"] or "")) if v.get("mcap") else "", num(v.get("pe_ttm")), num(v.get("pe_fwd")), last])
    s2 = "| " + " | ".join(vh) + " |\n|" + "---|" * len(vh) + "\n" + "\n".join("| " + " | ".join(r) + " |" for r in vr) + "\n"
    vnotes = []
    for t, d in data.items():
        for n in d["val"].get("notes", []):
            vnotes.append("- {0}：{1}".format(t, n))
        c_, f_ = d["val"].get("cur"), d["val"].get("fin_cur")
        if c_ and f_ and c_ != f_:
            vnotes.append("- {0}：報價幣別 {1}、報表幣別 {2}，營收與 EPS 已用該四季平均匯率換成 {1} 再算倍數".format(t, c_, f_))
    note = ("算法：營收成長＝該年度營收÷前一年度營收－1；投入資本報酬率＝營業利益×(1－稅率)÷（股東權益＋總債務－現金），稅率＝所得稅費用÷稅前淨利（限制在 0～35%），分母用該年度年底餘額；"
            "各家會計年度結束月不同，年度欄是各家自己的年底。倍數在各家自己的報價幣別內算（過去十二個月本益比＝股價÷最近四季稀釋 EPS，預估本益比＝股價÷yfinance forwardEps，市銷率＝市值÷最近四季營收）；預估與過去十二個月的盈餘定義可能不同；空白＝算不出或落在 3～200 倍之外，程式不估。")
    if fin_mode:
        note = ("算法（金融業欄位）：營收成長＝該年度營收÷前一年度營收－1（營收＝yfinance 的 Total Revenue，銀行多為淨利息收入加非利息收入）；"
                "股東權益報酬率＝該年度歸屬普通股淨利÷該年度年底普通股權益（用年底餘額、不取平均，成長快的銀行會略低估）；"
                "稅前淨利率＝稅前淨利÷營收（已扣掉利息以外的費用與信用損失，所以比效率比低，兩者不能直接比）；"
                "效率比＝非利息費用÷營收，只有 yfinance 報表有「Non Interest Expense」這一列才算；沒有這一列時整欄不列、缺口記在資料缺口（目前美國大型銀行 yfinance 都沒有），程式不用其他科目推；"
                "股價淨值比＝yfinance priceToBook，並用市值÷最近年度年底普通股權益交叉核對，差超過 35% 留空。"
                "毛利率、營益率、投入資本報酬率、資本支出對金融業沒有可比的意義，這張表不列。"
                "各家會計年度結束月不同，年度欄是各家自己的年底。倍數在各家自己的報價幣別內算（過去十二個月本益比＝股價÷最近四季稀釋 EPS，預估本益比＝股價÷yfinance forwardEps）；"
                "預估與過去十二個月的盈餘定義可能不同；空白＝算不出或落在 3～200 倍之外，程式不估。"
                "保險與券商的營收、費用科目跟銀行不同，效率比與營收成長只供參考。")
    md = "同業對照（程式用 yfinance 年度財報自算）\n\n" + s + "\n現在的倍數與市值：\n\n" + s2 + "\n" + note + ("\n\n倍數備註：\n" + "\n".join(vnotes) if vnotes else "")
    return md, data, gaps


if __name__ == "__main__":
    t, ps = sys.argv[1], [x for x in sys.argv[2].split(",") if x]
    md, data, gaps = build(t, ps)
    print(md)
    print("GAPS:", gaps)
    # 空格統計
    for k, d in data.items():
        miss = {m for y in d["years"] for m in ("growth", "gm", "om", "roic", "capex", "rd") if y[m] is None}
        vmiss = [k2 for k2, v in d["val"].items() if v is None]
        print(k, "年度指標有空格：", sorted(miss), "倍數空：", vmiss)
