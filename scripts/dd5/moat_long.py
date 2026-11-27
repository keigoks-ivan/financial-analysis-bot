#!/usr/bin/env python3
"""護城河用的十年以上年度財報數字（程式算、零 LLM）。

資料（只讀本機共用資料庫，不上網抓財報）：
  - 台股：~/v7-backtest/data/tw_finmind_statements_full（FinMind 單季損益表加總成年，資產負債表取 12 月底）
  - 美股：~/v7-backtest/data/edgar/facts（SEC companyfacts 快取，取 CY 年度 frame）
  - 其他市場或本機沒有的代號：退回 yfinance 年報（約四年），標明來源
算出（2012～2025）：
  - R1 投入資本報酬率＝營業利益×79%÷(權益＋有息負債－現金)，年底值；十年（2016～2025）平均與最低
  - R2 營益率減直接對手（同業名單前兩家），逐年
  - R3 下行年：本檔或同業中位數營收年減 ≥5% 的年度，附本檔毛利率、營益率前後與相對掉幅
  - R5 營收成長減直接對手，逐年
  - cyclical_hint：十年報酬率最高減最低超過 25 個百分點、或有一年為負另一年超過 15%、或本檔自己營收年減 ≥5% 有三次以上
輸出 run 目錄的 moat_long.json（給判定模型）與 moat_long.md（引用標記 [p:moat_long]，也進 lint 參考文字）。
規格：判準見 cards/moat_card.md（2026-11-27 持有人選「競爭結構版＋十年財報」，試驗紀錄 ~/dd5-pilot/moat_trial/）。
"""
from __future__ import annotations

import json
import os
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
DATA = Path(os.environ.get("DD5_V7_DATA", str(Path.home() / "v7-backtest" / "data")))
TAX = 0.21
_cik = None
_tw = None


def _cik_of(t):
    global _cik
    if _cik is None:
        p = DATA / "edgar" / "company_tickers.json"
        if not p.exists():
            _cik = {}
        else:
            m = json.loads(p.read_text())
            _cik = {v["ticker"]: int(v["cik_str"]) for v in (m.values() if isinstance(m, dict) else m)}
    return _cik.get(t.replace("-", ".")) or _cik.get(t)


def us_annual(t):
    c = _cik_of(t)
    p = DATA / "edgar" / "facts" / ("CIK%010d.json" % c) if c else None
    if not p or not p.exists():
        return None
    f = json.loads(p.read_text()).get("facts", {}).get("us-gaap", {})

    def dur(names):
        out = {}
        for n in names:
            for u in f.get(n, {}).get("units", {}).get("USD", []):
                fr = u.get("frame") or ""
                if re.fullmatch(r"CY\d{4}", fr):
                    y = int(fr[2:])
                    out[y] = max(out.get(y, float("-inf")), u["val"])
        return out

    def inst(name):
        out = {}
        for u in f.get(name, {}).get("units", {}).get("USD", []):
            fr = u.get("frame") or ""
            if re.fullmatch(r"CY\d{4}Q4I", fr):
                out[int(fr[2:6])] = u["val"]
        return out

    rev = dur(["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
               "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueGoodsNet"])
    gp = dur(["GrossProfit"])
    cogs = dur(["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold"])
    oi = dur(["OperatingIncomeLoss"])
    eq = {}
    for n in ("StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"):
        for y, v in inst(n).items():
            eq.setdefault(y, v)
    debt = {}
    for n in ("LongTermDebt", "LongTermDebtNoncurrent", "DebtCurrent", "LongTermDebtCurrent", "ShortTermBorrowings", "CommercialPaper"):
        for y, v in inst(n).items():
            debt.setdefault(y, {})[n] = v
    cash = inst("CashAndCashEquivalentsAtCarryingValue")
    rows = {}
    for y in sorted(rev):
        if y < 2010 or y > 2025 or not rev[y]:
            continue
        g = gp.get(y) if y in gp else (rev[y] - cogs[y] if y in cogs else None)
        d = debt.get(y, {})
        dsum = (d.get("LongTermDebt") or (d.get("LongTermDebtNoncurrent", 0) + d.get("LongTermDebtCurrent", 0))) \
            + max(d.get("DebtCurrent", 0) - d.get("LongTermDebtCurrent", 0), 0) + d.get("ShortTermBorrowings", 0) + d.get("CommercialPaper", 0)
        ic = eq[y] + dsum - (cash.get(y) or 0) if y in eq else None
        rows[y] = {"rev": rev[y], "gm": g / rev[y] * 100 if g is not None else None, "om": oi[y] / rev[y] * 100 if y in oi else None,
                   "roic": (oi[y] * (1 - TAX) / ic * 100) if (y in oi and ic and ic > 0) else None, "ic_neg": bool(ic is not None and ic <= 0)}
    return rows or None


def tw_annual(t):
    global _tw
    import pandas as pd
    code = t.split(".")[0]
    if _tw is None:
        base = DATA / "tw_finmind_statements_full"
        if not (base / "is_long.parquet").exists():
            _tw = (None, None)
        else:
            _tw = (pd.read_parquet(base / "is_long.parquet", filters=[("type", "in", ["Revenue", "GrossProfit", "OperatingIncome"])]),
                   pd.read_parquet(base / "bs_long.parquet", filters=[("type", "in", ["Equity", "CashAndCashEquivalents", "ShorttermBorrowings",
                                                                                      "LongtermBorrowings", "BondsPayable"])]))
    is_, bs = _tw
    if is_ is None:
        return None
    x = is_[is_.code == code]
    if x.empty:
        return None
    x = x.assign(y=pd.to_datetime(x.date).dt.year).groupby(["y", "type"]).agg(v=("value", "sum"), n=("value", "size")).reset_index()
    b = bs[(bs.code == code) & (pd.to_datetime(bs.date).dt.month == 12)]
    b = b.assign(y=pd.to_datetime(b.date).dt.year).pivot_table(index="y", columns="type", values="value") if not b.empty else None
    rows = {}
    for y in sorted(x.y.unique()):
        s = x[x.y == y].set_index("type")
        if "Revenue" not in s.index or s.loc["Revenue", "n"] < 4 or y < 2010 or y > 2025:
            continue
        rv = float(s.loc["Revenue", "v"])
        if not rv:
            continue
        gp = float(s.loc["GrossProfit", "v"]) if "GrossProfit" in s.index else None
        oi = float(s.loc["OperatingIncome", "v"]) if "OperatingIncome" in s.index else None
        ic = None
        if b is not None and y in b.index:
            r = b.loc[y].fillna(0)
            ic = float(r.get("Equity", 0) + r.get("ShorttermBorrowings", 0) + r.get("LongtermBorrowings", 0) + r.get("BondsPayable", 0)
                       - r.get("CashAndCashEquivalents", 0))
        rows[int(y)] = {"rev": rv, "gm": gp / rv * 100 if gp is not None else None, "om": oi / rv * 100 if oi is not None else None,
                        "roic": oi * (1 - TAX) / ic * 100 if (oi is not None and ic and ic > 0) else None, "ic_neg": bool(ic is not None and ic <= 0)}
    return rows or None


def yf_annual(t):
    try:
        import yfinance as yf
        i = yf.Ticker(t).income_stmt
    except Exception:
        return None
    rows = {}
    for c in getattr(i, "columns", []):
        try:
            rv = float(i.loc["Total Revenue", c])
            oi = float(i.loc["Operating Income", c])
            gp = float(i.loc["Gross Profit", c]) if "Gross Profit" in i.index else float("nan")
        except Exception:
            continue
        if rv != rv or rv == 0:
            continue
        y = c.year if c.month >= 6 else c.year - 1
        rows[y] = {"rev": rv, "gm": gp / rv * 100 if gp == gp else None, "om": oi / rv * 100 if oi == oi else None, "roic": None, "ic_neg": False}
    return rows or None


_cache = {}


def annual(t):
    if t in _cache:
        return _cache[t]
    if re.search(r"\.(TW|TWO)$", t):
        a, src = tw_annual(t), "FinMind 年報"
    else:
        a, src = us_annual(t), "SEC 年報"
    if not a:
        a, src = yf_annual(t), "yfinance 年報（約四年）"
    _cache[t] = (a, src)
    return a, src


def _growth(rows, y):
    if not rows or y not in rows or y - 1 not in rows or not rows[y - 1]["rev"]:
        return None
    return (rows[y]["rev"] / rows[y - 1]["rev"] - 1) * 100


def _r(v):
    return None if v is None else round(v, 1)


def compute(t, peers):
    me, src = annual(t)
    if not me:
        return None
    rivals = [p for p in peers if p != t][:2]
    riv = {r: annual(r) for r in rivals}
    grp = {p: annual(p)[0] for p in peers if p != t}
    yrs = [y for y in sorted(me) if y >= 2012]
    down = []
    for y in yrs:
        g = _growth(me, y)
        pg = sorted(x for x in (_growth(v, y) for v in grp.values() if v) if x is not None)
        pm = pg[len(pg) // 2] if pg else None
        if (g is not None and g <= -5) or (pm is not None and pm <= -5):
            gm0, gm1 = (me.get(y - 1) or {}).get("gm"), me[y]["gm"]
            om0, om1 = (me.get(y - 1) or {}).get("om"), me[y]["om"]
            down.append({"year": y, "rev_growth": _r(g), "peer_median_growth": _r(pm), "self_fell": bool(g is not None and g <= -5),
                         "gm_prev": _r(gm0), "gm": _r(gm1), "gm_rel_drop_pct": _r((gm0 - gm1) / gm0 * 100) if gm0 and gm1 is not None else None,
                         "om_prev": _r(om0), "om": _r(om1),
                         "om_rel_drop_pct": _r((om0 - om1) / abs(om0) * 100) if om0 and om1 is not None else None})
    ro = [(y, me[y]["roic"]) for y in yrs if me[y]["roic"] is not None]
    last10 = [v for y, v in ro if y >= 2016]
    hint = False
    if last10:
        hint = (max(last10) - min(last10) > 25) or (min(last10) < 0 and max(last10) > 15)
    hint = hint or sum(1 for d in down if d["self_fell"]) >= 3
    r1 = {"by_year": [[y, _r(v)] for y, v in ro], "avg_2016_2025": _r(sum(last10) / len(last10)) if last10 else None,
          "min_2016_2025": _r(min(last10)) if last10 else None, "n_years": len(last10),
          "ic_negative_years": [y for y in yrs if me[y].get("ic_neg")], "small_base": bool(last10 and min(last10) > 60),
          "note": "營業利益×79%÷(權益＋有息負債－現金)，年底值；併購商譽大的公司會被壓低，改看營益率"}
    R2 = {str(y): {r: _r(me[y]["om"] - v[0][y]["om"]) for r, v in riv.items()
                   if v[0] and y in v[0] and v[0][y]["om"] is not None and me[y]["om"] is not None} for y in yrs}
    R5 = {str(y): {r: _r(_growth(me, y) - _growth(v[0], y)) for r, v in riv.items()
                   if _growth(v[0], y) is not None and _growth(me, y) is not None} for y in yrs}
    return {"ticker": t, "source": src, "rivals": rivals, "rival_sources": {r: v[1] for r, v in riv.items()},
            "peer_group_for_downturn": sorted(k for k, v in grp.items() if v), "cyclical_hint": bool(hint),
            "years": [yrs[0], yrs[-1]] if yrs else [],
            "R1_roic": r1,
            "R2_om_minus_rival": {k: v for k, v in R2.items() if v},
            "R3_downturn": down or "未經下行（{0}～{1} 本檔與同業中位數營收都沒有年減 5% 以上）".format(yrs[0], yrs[-1]) if yrs else "沒有年度資料",
            "R5_growth_minus_rival": {k: v for k, v in R5.items() if v},
            "me": {str(y): {"rev_growth": _r(_growth(me, y)), "gm": _r(me[y]["gm"]), "om": _r(me[y]["om"])} for y in yrs}}


def to_md(r):
    L = ["## [p:moat_long] 護城河十年財報數字（程式用{0}算，{1}～{2}）".format(r["source"], *(r["years"] or ["", ""])), ""]
    r1 = r["R1_roic"]
    L.append("- 投入資本報酬率 2016～2025 平均 {0}%，最低 {1}%（{2} 年有值）".format(r1["avg_2016_2025"], r1["min_2016_2025"], r1["n_years"]))
    L.append("- 逐年投入資本報酬率：" + "、".join("{0} 年 {1}%".format(y, v) for y, v in r1["by_year"]))
    L.append("- 直接對手：" + "、".join(r["rivals"]) + "；下行年比較的同業：" + "、".join(r["peer_group_for_downturn"]))
    if isinstance(r["R3_downturn"], list):
        for d in r["R3_downturn"]:
            L.append("- 下行年 {year}：本檔營收 {rev_growth}%、同業中位數 {peer_median_growth}%；毛利率 {gm_prev}% → {gm}%（相對掉 {gm_rel_drop_pct}%），"
                     "營益率 {om_prev}% → {om}%".format(**d))
    else:
        L.append("- " + r["R3_downturn"])
    L.append("- 逐年本檔：" + "；".join("{0} 年營收成長 {1}%、毛利率 {2}%、營益率 {3}%".format(y, v["rev_growth"], v["gm"], v["om"]) for y, v in r["me"].items()))
    for y, v in r["R2_om_minus_rival"].items():
        L.append("- {0} 年營益率減對手：".format(y) + "、".join("{0} {1} 個百分點".format(k, x) for k, x in v.items()))
    return "\n".join(L) + "\n"


def build(run_dir, t, peers):
    run_dir = Path(run_dir)
    r = compute(t, list(peers))
    if not r:
        return None
    (run_dir / "moat_long.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    (run_dir / "moat_long.md").write_text(to_md(r), encoding="utf-8")
    return r


def peers_of(run_dir, t):
    pj = Path(run_dir) / "peers.json"
    if not pj.exists():
        return []
    return [k for k in json.loads(pj.read_text(encoding="utf-8")).get("data", {}) if k != t]


if __name__ == "__main__":
    # 用法：python3 moat_long.py RUN_DIR TICKER → 寫 moat_long.json／.md 並印出摘要
    rd, tk = sys.argv[1], sys.argv[2]
    res = build(rd, tk, peers_of(rd, tk))
    print(to_md(res) if res else "（本檔沒有年度財報資料）")
