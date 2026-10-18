"""AI 信用風險監測：12 條指標的門檻、越線判斷與頁面所需的文字（純函式，不連網）。

門檻全部是事前登記值（2026-10-16 登記，之後不改）。AI 信用沒有可回測的歷史，
這些門檻是結構線或經驗值，不是由歷史資料擬合出來的。
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# 事前登記 2026-10-16，之後不改
# ---------------------------------------------------------------------------
REGISTERED_ON = "2026-10-16"
TH = {
    1: {"op": ">", "x": 1.0},       # 五大雲端 近四季資本支出 ÷ 營運現金流
    2: {"op": ">=", "x": 3},        # 自由現金流為負的家數
    3: {"op": ">", "x": 0.50},      # 近四季淨發債 ÷ 資本支出
    4: {"op": ">", "x": 3.5},       # Oracle 淨負債 ÷ EBITDA（不含融資租賃）
    5: {"op": "<", "x": 1.5},       # CoreWeave EBITDA ÷ 利息
    6: {"op": "<", "x": 1.0},       # CoreWeave（現金＋近四季 OCF）÷ 一年內到期本金
    7: {"op": "hyst", "enter": -20.0, "exit": -10.0},   # Oracle 相對 QQQ（個百分點）
    8: {"op": "hyst", "enter": -20.0, "exit": -10.0},   # CoreWeave
    9: {"op": "hyst", "enter": -20.0, "exit": -10.0},   # Blue Owl
    10: {"op": "<", "x": 0.85},     # 三檔 BDC 平均 股價 ÷ 淨值
    11: {"op": ">=", "x": 10.0},    # Nvidia 應收帳款天數 − 前四季平均（天）
    12: {"op": ">", "x": 0.25},     # Nvidia 保證＋融資承諾 ÷ 近四季營收
}
REL_WINDOW = 63   # 交易日
CLOUDS = ["MSFT", "GOOGL", "AMZN", "META", "ORCL"]
CLOUD_NAME = {"MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "META": "Meta", "ORCL": "Oracle"}
REL_NAME = {"ORCL": "Oracle", "CRWV": "CoreWeave", "OWL": "Blue Owl"}
BDCS = ["ARCC", "OBDC", "BXSL"]

GROUPS = {
    "A": "借錢的人撐不撐得住",
    "B": "市場怎麼定價",
    "C": "錢怎麼繞回來",
}
GROUP_OF = {1: "A", 2: "A", 3: "A", 4: "A", 5: "A", 6: "A", 7: "B", 8: "B", 9: "B", 10: "B", 11: "C", 12: "C"}
NAMES = {
    1: "五大雲端：資本支出 ÷ 營運現金流",
    2: "五大雲端：自由現金流為負的家數",
    3: "五大雲端：淨發債 ÷ 資本支出",
    4: "Oracle：淨負債 ÷ EBITDA",
    5: "CoreWeave：EBITDA ÷ 利息",
    6: "CoreWeave：(現金＋營運現金流) ÷ 一年內到期本金",
    7: "Oracle：近 63 個交易日報酬減 QQQ",
    8: "CoreWeave：近 63 個交易日報酬減 QQQ",
    9: "Blue Owl：近 63 個交易日報酬減 QQQ",
    10: "三檔 BDC：平均股價 ÷ 淨值",
    11: "Nvidia：應收帳款天數減前四季平均",
    12: "Nvidia：客戶保證與融資承諾 ÷ 近四季營收",
}
THRESHOLD_TEXT = {
    1: "> 1.0 倍",
    2: "≥ 3 家",
    3: "> 50%",
    4: "> 3.5 倍",
    5: "< 1.5 倍",
    6: "< 1.0 倍",
    7: "進入 ≤ −20 個百分點；解除 > −10 個百分點",
    8: "進入 ≤ −20 個百分點；解除 > −10 個百分點",
    9: "進入 ≤ −20 個百分點；解除 > −10 個百分點",
    10: "< 0.85 倍",
    11: "≥ +10 天",
    12: "> 25%",
}


def breach(i: int, v: float | None) -> bool | None:
    """非遲滯型指標的越線判斷；v 為 None 回 None。"""
    if v is None:
        return None
    t = TH[i]
    op, x = t["op"], t["x"]
    if op == ">":
        return v > x
    if op == ">=":
        return v >= x
    if op == "<":
        return v < x
    raise ValueError(f"指標 {i} 不是單一門檻型")


# ---------------------------------------------------------------------------
# 遲滯規則（第 7–9 條）
# ---------------------------------------------------------------------------
def rel_series(stock: list[tuple[str, float]], bench: list[tuple[str, float]], n: int = REL_WINDOW) -> list[tuple[str, float]]:
    """近 n 個交易日報酬減基準同期報酬（個百分點），依兩者共同交易日對齊。"""
    b = dict(bench)
    joint = [(dt, p, b[dt]) for dt, p in stock if dt in b]
    out = []
    for i in range(n, len(joint)):
        dt, p, q = joint[i]
        p0, q0 = joint[i - n][1], joint[i - n][2]
        out.append((dt, (p / p0 - 1.0) * 100.0 - (q / q0 - 1.0) * 100.0))
    return out


def rel_drawdown_1y(stock: list[tuple[str, float]], bench: list[tuple[str, float]], window: int = 252) -> float | None:
    """相對 QQQ 的一年回撤：(股價 ÷ QQQ) 現值相對近 window 個共同交易日高點的變動（%）。"""
    b = dict(bench)
    ratio = [p / b[dt] for dt, p in stock if dt in b]
    if len(ratio) < 2:
        return None
    w = ratio[-window:]
    return (w[-1] / max(w) - 1.0) * 100.0


def run_hysteresis(series: list[tuple[str, float]], state: bool | None = None, after: str | None = None,
                   enter: float = TH[7]["enter"], exit_: float = TH[7]["exit"]) -> tuple[bool, list[dict]]:
    """逐日套用遲滯規則。

    未越線時：值 ≤ enter 才進入越線；已越線時：值 > exit_ 才解除；介於兩者維持前一狀態。
    state=None 代表首次建立，從 series 開頭以「未越線」起跑；after 之前（含）的日子視為已處理而跳過。
    """
    cur = bool(state)
    trans: list[dict] = []
    for dt, v in series:
        if after is not None and dt <= after:
            continue
        if not cur and v <= enter:
            cur = True
            trans.append({"date": dt, "to": "in", "value": v})
        elif cur and v > exit_:
            cur = False
            trans.append({"date": dt, "to": "out", "value": v})
    return cur, trans


# ---------------------------------------------------------------------------
# 格式
# ---------------------------------------------------------------------------
def usd(x: float | None) -> str:
    """美元（元）→ 「x 億美元」。"""
    if x is None:
        return "—"
    v = x / 1e8
    return f"{v:,.0f} 億美元" if abs(v) >= 1000 else f"{v:,.1f} 億美元"


def pct(x: float | None, nd: int = 0) -> str:
    return "—" if x is None else f"{x * 100:.{nd}f}%"


def _dates(ds: list[str | None]) -> str:
    ds = sorted({d for d in ds if d})
    if not ds:
        return "—"
    return ds[0] if len(ds) == 1 else f"{ds[0]}～{ds[-1]}"


def _unit_data(u: dict | None) -> dict | None:
    return None if not u else u.get("data")


def _stale(units: list[dict | None]) -> bool:
    return any(u and u.get("stale") for u in units)


def _blank(i: int, why: str) -> dict:
    return {
        "id": i, "group": GROUP_OF[i], "name": NAMES[i], "value": None, "value_text": "無資料", "threshold": THRESHOLD_TEXT[i],
        "breached": None, "date_text": "—", "stale": False, "plain": why, "table": None, "notes": [],
    }


# ---------------------------------------------------------------------------
# 各指標
# ---------------------------------------------------------------------------
def _clouds_ready(units: dict) -> list[dict] | None:
    cs = [units.get(f"cloud:{t}") for t in CLOUDS]
    if any(not c or not c.get("data") for c in cs):
        return None
    return cs


def ind_1_2_3(units: dict) -> list[dict]:
    cs = _clouds_ready(units)
    if cs is None:
        return [_blank(i, "五大雲端至少一家尚無可用資料，這條暫不計算。") for i in (1, 2, 3)]
    rows = [(t, c["data"]) for t, c in zip(CLOUDS, cs)]
    capex = sum(d["capex"] for _, d in rows)
    ocf = sum(d["ocf"] for _, d in rows)
    issued = sum(d["issued"] for _, d in rows)
    repaid = sum(d["repaid"] for _, d in rows)
    net = issued - repaid
    dates = _dates([d["end"] for _, d in rows])
    stale = _stale(cs)
    notes = []
    for t, d in rows:
        if d.get("assumed_zero"):
            notes.append(f"{CLOUD_NAME[t]}：" + "；".join(d["assumed_zero"]))

    # 1
    r1 = capex / ocf
    tbl1 = {
        "head": ["公司", "近四季資本支出", "近四季營運現金流", "比值", "截止日"],
        "rows": [[CLOUD_NAME[t], usd(d["capex"]), usd(d["ocf"]), f"{d['capex'] / d['ocf']:.2f}", d["end"]] for t, d in rows]
        + [["合計", usd(capex), usd(ocf), f"{r1:.2f}", ""]],
    }
    b1 = breach(1, r1)
    p1 = (f"五家合計近四季資本支出是營運現金流的 {r1:.2f} 倍，已超過 1 倍，蓋資料中心的錢本業現金付不起，缺口要靠對外借款或增資補。"
          if b1 else f"五家合計近四季資本支出是營運現金流的 {r1:.2f} 倍，沒有超過 1 倍，整體而言本業現金仍付得起建設支出。")
    i1 = {"id": 1, "group": "A", "name": NAMES[1], "value": r1, "value_text": f"{r1:.2f} 倍", "threshold": THRESHOLD_TEXT[1],
          "breached": b1, "date_text": dates, "stale": stale, "plain": p1, "table": tbl1, "notes": []}

    # 2
    fcf = [(t, d["ocf"] - d["capex"]) for t, d in rows]
    neg = [t for t, v in fcf if v < 0]
    n_neg = len(neg)
    tbl2 = {
        "head": ["公司", "近四季自由現金流（營運現金流減資本支出）", "是否為負"],
        "rows": [[CLOUD_NAME[t], usd(v), "是" if v < 0 else "否"] for t, v in fcf],
    }
    b2 = breach(2, n_neg)
    names = "、".join(CLOUD_NAME[t] for t in neg) or "無"
    p2 = (f"五家裡有 {n_neg} 家近四季自由現金流為負（{names}），達到 3 家門檻，整個族群的建設要靠債市與股市提供資金。"
          if b2 else f"五家裡有 {n_neg} 家近四季自由現金流為負（{names}），未達 3 家的門檻。")
    i2 = {"id": 2, "group": "A", "name": NAMES[2], "value": float(n_neg), "value_text": f"{n_neg} 家", "threshold": THRESHOLD_TEXT[2],
          "breached": b2, "date_text": dates, "stale": stale, "plain": p2, "table": tbl2, "notes": []}

    # 3
    r3 = net / capex
    tbl3 = {
        "head": ["公司", "近四季發債", "近四季還債", "淨發債", "淨發債 ÷ 資本支出", "截止日"],
        "rows": [[CLOUD_NAME[t], usd(d["issued"]), usd(d["repaid"]), usd(d["issued"] - d["repaid"]),
                  pct((d["issued"] - d["repaid"]) / d["capex"]), d["end"]] for t, d in rows]
        + [["合計", usd(issued), usd(repaid), usd(net), pct(r3), ""]],
    }
    b3 = breach(3, r3)
    p3 = (f"五家近四季總發債 {usd(issued)}，扣掉還債後淨發債 {usd(net)}，相當於資本支出的 {pct(r3)}，超過一半的建設費用來自新借的錢。"
          if b3 else f"五家近四季總發債 {usd(issued)}，扣掉還債後淨發債 {usd(net)}，相當於資本支出的 {pct(r3)}，沒有超過一半。")
    i3 = {"id": 3, "group": "A", "name": NAMES[3], "value": r3, "value_text": pct(r3, 1), "threshold": THRESHOLD_TEXT[3],
          "breached": b3, "date_text": dates, "stale": stale, "plain": p3, "table": tbl3, "notes": notes,
          "extra": {"gross_issued": issued, "net_issued": net, "repaid": repaid}}
    return [i1, i2, i3]


def ind_4(units: dict) -> dict:
    u = units.get("orcl")
    d = _unit_data(u)
    if not d:
        return _blank(4, "Oracle 資產負債表或損益資料尚無可用值，這條暫不計算。")
    debt = d["debt_current"] + d["debt_lt"]
    cash = d["cash"] + d["afs"]
    nd = debt - cash
    ebitda = d["oi"] + d["dep"] + d["amort"]
    m = nd / ebitda
    m2 = (nd + d["fin_lease"]) / ebitda if d.get("fin_lease") is not None else None
    b = breach(4, m)
    chk = ""
    ck = d.get("debt_check")
    if ck:
        chk = f"驗證：{ck['end']} 兩項債務相加 {usd(ck['sum'])}，與申報的總債務 {usd(ck['combined'])} 相差 {ck['diff_pct']:.2f}%。"
    tbl = {
        "head": ["項目", "金額"],
        "rows": [
            ["短期債務（NotesPayableCurrent）", usd(d["debt_current"])],
            ["長期債務（LongTermNotesAndLoans）", usd(d["debt_lt"])],
            ["現金及約當現金", usd(d["cash"])],
            ["有價債券（可供出售，流動）", usd(d["afs"])],
            ["淨負債", usd(nd)],
            ["近四季營業利益", usd(d["oi"])],
            ["近四季折舊", usd(d["dep"])],
            ["近四季無形資產攤銷", usd(d["amort"])],
            ["近四季 EBITDA", usd(ebitda)],
            ["融資租賃負債（另列，不計入門檻判斷）", usd(d.get("fin_lease"))],
            ["含融資租賃的淨負債 ÷ EBITDA", "—" if m2 is None else f"{m2:.2f} 倍"],
        ],
    }
    tail = "" if m2 is None else f"。含融資租賃為 {m2:.2f} 倍"
    p = (f"Oracle 淨負債約為近四季 EBITDA 的 {m:.2f} 倍，已超過 3.5 倍{tail}。"
         if b else f"Oracle 淨負債約為近四季 EBITDA 的 {m:.2f} 倍，低於 3.5 倍{tail}。")
    return {"id": 4, "group": "A", "name": NAMES[4], "value": m, "value_text": f"{m:.2f} 倍", "threshold": THRESHOLD_TEXT[4],
            "breached": b, "date_text": _dates([d["bs_end"], d["flow_end"]]), "stale": _stale([u]), "plain": p, "table": tbl,
            "notes": ([chk] if chk else []) + list(d.get("notes") or []), "extra": {"incl_lease": m2}}


def ind_5(units: dict) -> dict:
    u = units.get("crwv")
    d = _unit_data(u)
    if not d:
        return _blank(5, "CoreWeave 損益資料尚無可用值，這條暫不計算。")
    ebitda = d["oi"] + d["dda"]
    m = ebitda / d["interest"]
    b = breach(5, m)
    tbl = {
        "head": ["項目", "近四季金額"],
        "rows": [["營業利益", usd(d["oi"])], ["折舊、耗竭與攤銷", usd(d["dda"])], ["EBITDA", usd(ebitda)],
                 ["利息費用（債務）", usd(d["interest"])]],
    }
    p = (f"CoreWeave 近四季 EBITDA 只有利息費用的 {m:.1f} 倍，低於 1.5 倍。此處 EBITDA 還沒扣 GPU 折舊，實際更緊。"
         if b else f"CoreWeave 近四季 EBITDA 是利息費用的 {m:.1f} 倍，高於 1.5 倍。此處 EBITDA 沒扣 GPU 折舊，實際比這個數字窄。")
    return {"id": 5, "group": "A", "name": NAMES[5], "value": m, "value_text": f"{m:.1f} 倍", "threshold": THRESHOLD_TEXT[5],
            "breached": b, "date_text": d["flow_end"], "stale": _stale([u]), "plain": p, "table": tbl, "notes": []}


def ind_6(units: dict) -> dict:
    u = units.get("crwv")
    d = _unit_data(u)
    if not d:
        return _blank(6, "CoreWeave 現金與到期本金資料尚無可用值，這條暫不計算。")
    liq = d["cash"] + d["ocf"]
    m = liq / d["maturities_12m"]
    b = breach(6, m)
    tbl = {
        "head": ["項目", "金額"],
        "rows": [["現金及約當現金", usd(d["cash"])], ["近四季營運現金流", usd(d["ocf"])], ["兩者合計", usd(liq)],
                 ["一年內到期本金", usd(d["maturities_12m"])]],
    }
    p = (f"CoreWeave 的現金加近四季營運現金流只有一年內到期本金的 {m:.1f} 倍，低於 1 倍，不借新還舊就還不完明年到期的債。"
         if b else f"CoreWeave 的現金加近四季營運現金流是一年內到期本金的 {m:.1f} 倍，高於 1 倍。此處沒有扣資本支出。")
    return {"id": 6, "group": "A", "name": NAMES[6], "value": m, "value_text": f"{m:.1f} 倍", "threshold": THRESHOLD_TEXT[6],
            "breached": b, "date_text": _dates([d["bs_end"], d["flow_end"]]), "stale": _stale([u]), "plain": p, "table": tbl, "notes": []}


def ind_rel(i: int, ticker: str, units: dict) -> dict:
    u = units.get("market")
    d = _unit_data(u)
    r = (d or {}).get(ticker)
    flag = (r or {}).get("flag")
    if not r or flag is None:
        return _blank(i, f"{REL_NAME[ticker]} 的股價資料尚無可用值，這條暫不計算。")
    pp = r["rel_pp"]
    b = bool(flag["breached"])
    state = "越線" if b else "未越線"
    if b:
        p = (f"{REL_NAME[ticker]} 近 63 個交易日報酬比 QQQ 少 {abs(pp):.1f} 個百分點" if pp < 0
             else f"{REL_NAME[ticker]} 近 63 個交易日報酬比 QQQ 多 {pp:.1f} 個百分點")
        p += "，仍在越線狀態。要超過 −10 個百分點才解除。"
    else:
        p = (f"{REL_NAME[ticker]} 近 63 個交易日報酬比 QQQ " + (f"少 {abs(pp):.1f}" if pp < 0 else f"多 {pp:.1f}")
             + " 個百分點，未越線。要跌到 −20 個百分點以下才進入。")
    tbl = {
        "head": ["項目", "數值"],
        "rows": [
            [f"{REL_NAME[ticker]} 近 63 日報酬", f"{r['ret_stock']:+.1f}%"],
            ["QQQ 同期報酬", f"{r['ret_bench']:+.1f}%"],
            ["相對 QQQ", f"{pp:+.1f} 個百分點"],
            ["目前狀態", state + (f"（{flag.get('since')} 起）" if flag.get("since") else "")],
            ["相對 QQQ 的一年回撤（不計入）", f"{r['dd1y_rel']:.1f}%" if r.get("dd1y_rel") is not None else "—"],
        ],
    }
    return {"id": i, "group": "B", "name": NAMES[i], "value": pp, "value_text": f"{pp:+.1f} 個百分點", "threshold": THRESHOLD_TEXT[i],
            "breached": b, "date_text": r["asof"], "stale": _stale([u]), "plain": p, "table": tbl, "notes": []}


def ind_10(units: dict) -> dict:
    px = units.get("bdc_px")
    pxd = _unit_data(px)
    navs = {t: _unit_data(units.get(f"bdc_nav:{t}")) for t in BDCS}
    if not pxd or any(navs[t] is None or t not in pxd for t in BDCS):
        return _blank(10, "BDC 的股價或淨值資料不全，這條暫不計算。")
    ratios = {t: pxd[t]["price"] / navs[t]["nav"] for t in BDCS}
    avg = sum(ratios.values()) / len(ratios)
    b = breach(10, avg)
    low_t = min(ratios, key=ratios.get)
    tbl = {
        "head": ["BDC", "股價", "股價日", "每股淨值", "淨值日", "股價 ÷ 淨值"],
        "rows": [[t, f"{pxd[t]['price']:.2f}", pxd[t]["asof"], f"{navs[t]['nav']:.2f}", navs[t]["asof"], f"{ratios[t]:.2f}"] for t in BDCS]
        + [["平均", "", "", "", "", f"{avg:.2f}"]],
    }
    p = (f"三檔 BDC 平均股價是淨值的 {avg:.2f} 倍，低於 0.85，市場不相信帳上貸款的價值。最低的是 {low_t}（{ratios[low_t]:.2f}）。"
         if b else f"三檔 BDC 平均股價是淨值的 {avg:.2f} 倍，高於 0.85。最低的是 {low_t}（{ratios[low_t]:.2f}）。")
    return {"id": 10, "group": "B", "name": NAMES[10], "value": avg, "value_text": f"{avg:.2f} 倍", "threshold": THRESHOLD_TEXT[10],
            "breached": b, "date_text": _dates([pxd[t]["asof"] for t in BDCS] + [navs[t]["asof"] for t in BDCS]),
            "stale": _stale([px] + [units.get(f"bdc_nav:{t}") for t in BDCS]), "plain": p, "table": tbl, "notes": [],
            "extra": {"ratios": ratios}}


def ind_11(units: dict) -> dict:
    u = units.get("nvda_fin")
    d = _unit_data(u)
    if not d:
        return _blank(11, "Nvidia 應收帳款資料尚無可用值，這條暫不計算。")
    q = d["quarters"]
    latest = q[-1]
    prev4 = q[-5:-1]
    base = sum(x["dso"] for x in prev4) / len(prev4)
    delta = latest["dso"] - base
    b = breach(11, delta)
    tbl = {
        "head": ["季末", "營收", "應收帳款", "應收天數", "存貨天數（只顯示）"],
        "rows": [[x["end"], usd(x["rev"]), usd(x["ar"]), f"{x['dso']:.1f}", "—" if x.get("dio") is None else f"{x['dio']:.1f}"] for x in q],
    }
    p = (f"Nvidia 最新應收帳款天數 {latest['dso']:.1f} 天，比前四季平均 {base:.1f} 天多 {delta:.1f} 天，客戶付款明顯變慢。"
         if b else f"Nvidia 最新應收帳款天數 {latest['dso']:.1f} 天，比前四季平均 {base:.1f} 天{'多' if delta >= 0 else '少'} {abs(delta):.1f} 天，未達 +10 天的門檻。")
    return {"id": 11, "group": "C", "name": NAMES[11], "value": delta, "value_text": f"{delta:+.1f} 天", "threshold": THRESHOLD_TEXT[11],
            "breached": b, "date_text": latest["end"], "stale": _stale([u]), "plain": p, "table": tbl, "notes": [],
            "extra": {"latest_dso": latest["dso"], "base_dso": base}}


def ind_12(units: dict) -> dict:
    uf, uc = units.get("nvda_fin"), units.get("nvda_commit")
    f, c = _unit_data(uf), _unit_data(uc)
    ex = c
    if not f or not ex or ex.get("ai_cloud") is None or ex.get("equity") is None:
        return _blank(12, "Nvidia 保證或融資承諾資料不全，這條暫不計算。")
    num = f["guarantee"] + ex["ai_cloud"] + ex["equity"]
    r = num / f["rev_ttm"]
    b = breach(12, r)
    tbl = {
        "head": ["項目", "金額", "資料日"],
        "rows": [
            ["對客戶與夥伴的保證（最大可能損失）", usd(f["guarantee"]), f["guarantee_date"]],
            ["AI 雲端夥伴承諾（10-Q 附註「Additional commitments」）", usd(ex["ai_cloud"]), c.get("report_date", "")],
            ["股權投資承諾（投資，不是放款）", usd(ex["equity"]), c.get("report_date", "")],
            ["合計", usd(num), ""],
            ["近四季營收", usd(f["rev_ttm"]), f["rev_end"]],
            ["合計 ÷ 近四季營收", pct(r, 1), ""],
        ],
    }
    calc = (f"算式：保證 {usd(f['guarantee'])} ＋ AI 雲端夥伴承諾 {usd(ex['ai_cloud'])} ＋ 股權投資承諾 {usd(ex['equity'])}；"
            "不含供應與產能承諾、雲端服務協議、未起租資料中心租約、資本支出，以及替第三方簽的資料中心租約。")
    p = (f"Nvidia 對客戶的保證與融資承諾合計 {usd(num)}，是近四季營收的 {pct(r, 1)}，高於 25% 的門檻。{calc}其中保證是最大可能損失，不是已借出的錢。"
         if b else f"Nvidia 對客戶的保證與融資承諾合計 {usd(num)}，是近四季營收的 {pct(r, 1)}，未超過 25%。{calc}")
    return {"id": 12, "group": "C", "name": NAMES[12], "value": r, "value_text": pct(r, 1), "threshold": THRESHOLD_TEXT[12],
            "breached": b, "date_text": _dates([f["guarantee_date"], f["rev_end"], c.get("report_date")]),
            "stale": _stale([uf, uc]), "plain": p, "table": tbl, "notes": []}


def compute_indicators(units: dict) -> list[dict]:
    out = ind_1_2_3(units)
    out += [ind_4(units), ind_5(units), ind_6(units)]
    out += [ind_rel(7, "ORCL", units), ind_rel(8, "CRWV", units), ind_rel(9, "OWL", units)]
    out += [ind_10(units), ind_11(units), ind_12(units)]
    return sorted(out, key=lambda x: x["id"])


def summarize(inds: list[dict]) -> dict:
    n_b = sum(1 for x in inds if x["breached"] is True)
    n_na = sum(1 for x in inds if x["breached"] is None)
    return {"n_breached": n_b, "n_total": len(inds), "n_unknown": n_na,
            "breached_ids": [x["id"] for x in inds if x["breached"] is True]}
