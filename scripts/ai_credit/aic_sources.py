"""AI 信用風險監測：各資料來源的抓取與整理（會連網）。

每個 collect_* 回傳一個 data dict，抓不到就丟例外；呼叫端（build_ai_credit.py）負責
「失敗時沿用上次值並標資料日期」，這裡絕不編數字、不以 0 代替缺漏的必要欄位。
"""
from __future__ import annotations

import csv
import io
import re
from datetime import date, timedelta

import requests

import ixparse as IX
import sec_facts as S
from aic_metrics import BDCS, CLOUDS, REL_NAME, REL_WINDOW, rel_drawdown_1y, rel_series, run_hysteresis

# ---------------------------------------------------------------------------
# 常數：各家 tag（逐家核對過 companyfacts）
# ---------------------------------------------------------------------------
CAPEX_TAG = {"AMZN": "PaymentsToAcquireProductiveAssets"}   # 其餘用 PaymentsToAcquirePropertyPlantAndEquipment
CAPEX_DEFAULT = "PaymentsToAcquirePropertyPlantAndEquipment"
OCF_TAG = "NetCashProvidedByUsedInOperatingActivities"
# 發債 tag（依優先序；每個期間元件取第一個有值的 tag，不跨 tag 相加）
ISSUE_TAGS = {
    "MSFT": ["ProceedsFromDebtMaturingInMoreThanThreeMonths"],
    "GOOGL": ["ProceedsFromDebtNetOfIssuanceCosts"],
    "AMZN": ["ProceedsFromIssuanceOfLongTermDebt"],
    "META": ["ProceedsFromIssuanceOfLongTermDebt"],
    "ORCL": ["ProceedsFromIssuanceOfSeniorLongTermDebt", "ProceedsFromIssuanceOfLongTermDebt"],  # 2025-08 前用後者
}
# 還債 tag。GOOGL 的標準 tag 含融資租賃本金（RepaymentsOfDebtAndCapitalLeaseObligations）。
REPAY_TAGS = {
    "MSFT": ["RepaymentsOfDebtMaturingInMoreThanThreeMonths"],
    "GOOGL": ["RepaymentsOfDebtAndCapitalLeaseObligations"],
    "AMZN": ["RepaymentsOfLongTermDebt"],
    "META": [],   # Meta 現金流量表自 2015 年起沒有還債列，視為 0 並在頁面註明
    "ORCL": ["RepaymentsOfDebt"],
}
REPAY_NOTE = {"META": "現金流量表沒有還債列，還債以 0 計"}
UNREC = "us-gaap:UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount"
# 尚未起租的資料中心租約：(tag, 維度成員集合；空集合＝無維度)
LEASE_RULES = {
    "ORCL": ("orcl:LesseeOperatingLeaseLeaseNotYetCommencedLeaseCommitments", set()),
    "MSFT": (UNREC, {"msft:FinanceLeaseMember"}),
    "GOOGL": (UNREC, {"us-gaap:OperatingLeaseLeaseNotYetCommencedMember"}),
    "META": (UNREC, set()),
    "AMZN": (UNREC, {"amzn:OperatingAndFinanceLeasesLeaseNotYetCommencedMember"}),
    "CRWV": (UNREC, {"crwv:DataCenterAndOfficeBuildingsMember"}),
}
RPO_COMPANIES = ["ORCL", "MSFT", "GOOGL", "CRWV"]
FRED_SERIES = [("BAMLH0A0HYM2", "高收益債利差"), ("BAMLC0A4CBBB", "BBB 公司債利差"), ("BAMLH0A3HYC", "CCC 以下利差")]

_FACTS: dict[str, dict] = {}
_FILING_META: dict[str, dict] = {}
_HTML: dict[str, tuple[str, dict]] = {}


def facts_for(t: str) -> dict:
    if t not in _FACTS:
        _FACTS[t] = S.fetch_companyfacts(t)
    return _FACTS[t]


def filing_meta(t: str) -> dict:
    if t not in _FILING_META:
        _FILING_META[t] = IX.latest_periodic(t)
    return _FILING_META[t]


def filing_html(t: str) -> tuple[str, dict]:
    """(html, contexts)；只快取最新一份，避免記憶體堆積。"""
    meta = filing_meta(t)
    key = meta["accession"]
    if key not in _HTML:
        _HTML.clear()
        h = IX.fetch_html(meta["url"])
        _HTML[key] = (h, IX.contexts(h))
    return _HTML[key]


_PART_ZH = {"A": "最新年報", "P": "去年同期累計", "C": "今年累計"}


def _require_recent(tag_rows: list[list[dict]], win_end: str, label: str) -> None:
    """發債／還債類科目允許「沒發生就不列示」補 0，但該公司至少要在近兩年內用過其中一個 tag，
    否則視為 tag 對不上而報錯，避免把整個科目靜默吞成 0。"""
    cutoff = (S.d(win_end) - timedelta(days=800)).isoformat()
    if not any(rs and rs[-1]["end"] >= cutoff for rs in tag_rows):
        raise RuntimeError(f"{label}：近兩年沒有任何候選 tag 的事實，tag 可能已更名")


# ---------------------------------------------------------------------------
# 五大雲端（指標 1–3）
# ---------------------------------------------------------------------------
def collect_cloud(t: str) -> dict:
    f = facts_for(t)
    ocf_rows = S.rows(f, OCF_TAG)
    win = S.ttm_window(ocf_rows)
    if win is None:
        raise RuntimeError(f"{t} 營運現金流找不到年報")
    ocf = S.ttm_flow(ocf_rows, win)
    cx_tag = CAPEX_TAG.get(t, CAPEX_DEFAULT)
    capex = S.ttm_flow(S.rows(f, cx_tag), win)
    if ocf is None or capex is None:
        raise RuntimeError(f"{t} 近四季營運現金流或資本支出算不出（期間元件缺漏）")
    iss_rows = [S.rows(f, k) for k in ISSUE_TAGS[t]]
    _require_recent(iss_rows, win["end"], f"{t} 發債")
    issued = S.ttm_flow(iss_rows, win, zero_ok=True)
    rep_rows = [S.rows(f, k) for k in REPAY_TAGS[t]]
    assumed: list[str] = []
    if REPAY_TAGS[t]:
        _require_recent(rep_rows, win["end"], f"{t} 還債")
    elif t in REPAY_NOTE:
        assumed.append(REPAY_NOTE[t])
    repaid = S.ttm_flow(rep_rows, win, zero_ok=True)
    if issued is None or repaid is None:
        raise RuntimeError(f"{t} 發債或還債算不出")
    if issued["assumed_zero"]:
        assumed.append("發債在" + "、".join(_PART_ZH[x] for x in issued["assumed_zero"]) + "期間沒有事實，以 0 計")
    if repaid["assumed_zero"] and REPAY_TAGS[t]:
        assumed.append("還債在" + "、".join(_PART_ZH[x] for x in repaid["assumed_zero"]) + "期間沒有事實，以 0 計")
    return {"capex": capex["value"], "ocf": ocf["value"], "issued": issued["value"], "repaid": repaid["value"],
            "end": win["end"], "capex_tag": cx_tag, "assumed_zero": assumed}


# ---------------------------------------------------------------------------
# Oracle（指標 4）
# ---------------------------------------------------------------------------
def collect_orcl() -> dict:
    f = facts_for("ORCL")
    lt = S.latest_instant(f, "LongTermNotesAndLoans")
    if not lt:
        raise RuntimeError("ORCL 找不到 LongTermNotesAndLoans")
    bs_end = lt["end"]
    nc = S.instant_at(f, "NotesPayableCurrent", bs_end)
    cash = S.instant_at(f, "CashAndCashEquivalentsAtCarryingValue", bs_end)
    if nc is None or cash is None:
        raise RuntimeError(f"ORCL {bs_end} 缺短期債務或現金")
    afs = S.instant_at(f, "AvailableForSaleSecuritiesDebtSecuritiesCurrent", bs_end)
    notes = []
    if afs is None:
        afs = 0.0
        notes.append("有價債券該日無事實，以 0 計")
    fin_lease = S.instant_at(f, "FinanceLeaseLiability", bs_end)
    # 驗證：兩項債務相加應等於申報的總債務（該 tag 只在年報日出現，所以用它最新的日期對照）
    check = None
    comb = S.latest_instant(f, "DebtLongtermAndShorttermCombinedAmount")
    if comb:
        a, b = S.instant_at(f, "NotesPayableCurrent", comb["end"]), S.instant_at(f, "LongTermNotesAndLoans", comb["end"])
        if a is not None and b is not None:
            check = {"end": comb["end"], "sum": a + b, "combined": comb["val"], "diff_pct": abs(a + b - comb["val"]) / comb["val"] * 100}
    oi_rows = S.rows(f, "OperatingIncomeLoss")
    win = S.ttm_window(oi_rows)
    oi = S.ttm_flow(oi_rows, win)
    dep = S.ttm_flow(S.rows(f, "Depreciation"), win)
    am = S.ttm_flow(S.rows(f, "AmortizationOfIntangibleAssets"), win)
    if not (oi and dep and am):
        raise RuntimeError("ORCL 近四季營業利益、折舊或攤銷算不出")
    return {"debt_current": nc, "debt_lt": lt["val"], "debt_check": check, "cash": cash, "afs": afs,
            "fin_lease": fin_lease, "oi": oi["value"], "dep": dep["value"], "amort": am["value"],
            "bs_end": bs_end, "flow_end": win["end"], "notes": notes}


# ---------------------------------------------------------------------------
# CoreWeave（指標 5、6）
# ---------------------------------------------------------------------------
def collect_crwv() -> dict:
    f = facts_for("CRWV")
    oi_rows = S.rows(f, "OperatingIncomeLoss")
    win = S.ttm_window(oi_rows)
    oi = S.ttm_flow(oi_rows, win)
    dda = S.ttm_flow(S.rows(f, "DepreciationDepletionAndAmortization"), win)
    intr = S.ttm_flow(S.rows(f, "InterestExpenseDebt"), win)
    ocf = S.ttm_flow(S.rows(f, OCF_TAG), win)
    if not (oi and dda and intr and ocf):
        raise RuntimeError("CRWV 近四季營業利益、折舊攤銷、利息或營運現金流算不出")
    cashrec = S.latest_instant(f, "CashAndCashEquivalentsAtCarryingValue")
    if not cashrec:
        raise RuntimeError("CRWV 找不到現金")
    bs_end = cashrec["end"]
    mat_tag = "LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths"
    mat = S.instant_at(f, mat_tag, bs_end)
    src = "companyfacts"
    if mat is None:
        # 標準 tag 缺（資產負債表改自訂 tag 的季度）：退用內嵌 XBRL
        h, ctx = filing_html("CRWV")
        hit = IX.pick_instant(IX.facts(h, re.escape("us-gaap:" + mat_tag) + "$", ctx), "us-gaap:" + mat_tag, set())
        if not hit or hit["instant"] != bs_end:
            raise RuntimeError(f"CRWV {bs_end} 找不到一年內到期本金")
        mat, src = hit["value"], "inline-xbrl"
    return {"oi": oi["value"], "dda": dda["value"], "interest": intr["value"], "ocf": ocf["value"], "cash": cashrec["val"],
            "maturities_12m": mat, "bs_end": bs_end, "flow_end": win["end"], "maturity_source": src}


# ---------------------------------------------------------------------------
# Nvidia（指標 11、12）
# ---------------------------------------------------------------------------
def collect_nvda_fin() -> dict:
    f = facts_for("NVDA")
    rev_rows = S.rows(f, "Revenues")
    rev_q = S.single_quarters(rev_rows)
    cogs_q = S.single_quarters(S.rows(f, "CostOfRevenue"))
    ar = {r["end"]: r["val"] for r in S.instants(f, "AccountsReceivableNetCurrent")}
    inv = {r["end"]: r["val"] for r in S.instants(f, "InventoryNet")}
    ends = [e for e in rev_q if e in ar][-8:]
    if len(ends) < 6:
        raise RuntimeError("NVDA 應收帳款與營收對得上的季數不足")
    quarters = []
    for e in ends:
        dio = inv[e] / cogs_q[e] * 91 if (e in inv and cogs_q.get(e)) else None
        quarters.append({"end": e, "rev": rev_q[e], "ar": ar[e], "dso": ar[e] / rev_q[e] * 91, "dio": dio})
    rev_ttm = S.ttm_flow(rev_rows)
    g = S.latest_instant(f, "GuaranteeObligationsMaximumExposure")
    if not rev_ttm or not g:
        raise RuntimeError("NVDA 近四季營收或保證承諾找不到")
    return {"quarters": quarters, "rev_ttm": rev_ttm["value"], "rev_end": rev_ttm["end"],
            "guarantee": g["val"], "guarantee_date": g["end"]}


def _parse_nvda_commit(h: str, ctx: dict, meta: dict) -> dict:
    fs = IX.facts(h, r"^us-gaap:OtherCommitment$", ctx)
    axis = "us-gaap:OtherCommitmentsAxis"

    def one(member: str) -> float | None:
        c = [x for x in fs if x["instant"] and IX.members(x) == frozenset([member]) and x["dims"][0][0] == axis]
        if not c:
            return None
        last = max(x["instant"] for x in c)
        return [x for x in c if x["instant"] == last][0]["value"]

    ai, eq = one("nvda:AICloudPartnershipCommitmentsMember"), one("nvda:EquityInvestmentCommitmentsMember")
    if ai is None or eq is None:
        raise RuntimeError("NVDA 10-Q 內嵌 XBRL 找不到 AI 雲端夥伴承諾或股權投資承諾")
    return {"accession": meta["accession"], "report_date": meta["report_date"], "filing_date": meta["filing_date"],
            "ai_cloud": ai, "equity": eq}


def collect_nvda_commit(prev: dict | None) -> dict:
    meta = filing_meta("NVDA")
    if prev and prev.get("accession") == meta["accession"]:
        return prev
    h, ctx = filing_html("NVDA")
    return _parse_nvda_commit(h, ctx, meta)


# ---------------------------------------------------------------------------
# 尚未起租租約、CoreWeave 客戶占比（內嵌 XBRL；同一份申報只解析一次）
# ---------------------------------------------------------------------------
def collect_lease(t: str, prev: dict | None) -> dict:
    meta = filing_meta(t)
    if prev and prev.get("accession") == meta["accession"]:
        return prev
    h, ctx = filing_html(t)
    name, need = LEASE_RULES[t]
    fs = IX.facts(h, "^" + re.escape(name) + "$", ctx)
    hit = IX.pick_instant(fs, name, need)
    if not hit:
        raise RuntimeError(f"{t} 找不到尚未起租租約（{name} {sorted(need) or '無維度'}）")
    sub = None
    if t == "META":
        subs = [x for x in fs if x["instant"] and "us-gaap:SubsequentEventMember" in IX.members(x)]
        if subs:
            sub = max(subs, key=lambda x: x["instant"])["value"]
    return {"accession": meta["accession"], "report_date": meta["report_date"], "filing_date": meta["filing_date"],
            "value": hit["value"], "as_of": hit["instant"], "tag": name, "subsequent": sub}


def collect_customers(prev: dict | None) -> dict:
    meta = filing_meta("CRWV")
    if prev and prev.get("accession") == meta["accession"]:
        return prev
    h, ctx = filing_html("CRWV")
    fs = IX.facts(h, r"^us-gaap:ConcentrationRiskPercentage1$", ctx)
    rows = []
    for x in fs:
        ms = IX.members(x)
        if "us-gaap:RevenueFromContractWithCustomerMember" not in ms or "us-gaap:CustomerConcentrationRiskMember" not in ms:
            continue
        cust = [m for m in ms if m.startswith("crwv:Customer")]
        if len(cust) != 1 or not x["start"] or not x["end"]:
            continue
        days = (S.d(x["end"]) - S.d(x["start"])).days
        if 80 <= days <= 100:
            rows.append((x["end"], cust[0], x["value"]))
    if not rows:
        raise RuntimeError("CRWV 找不到單季客戶營收占比")
    last = max(r[0] for r in rows)
    cur = sorted(((c, v) for e, c, v in rows if e == last), key=lambda z: -z[1])
    ya_end = (S.d(last) - timedelta(days=365)).isoformat()
    ya = [(c, v) for e, c, v in rows if abs((S.d(e) - S.d(ya_end)).days) <= 6]
    label = lambda m: m.replace("crwv:", "").replace("Member", "").replace("Customer", "客戶 ")  # noqa: E731
    return {"accession": meta["accession"], "report_date": meta["report_date"], "filing_date": meta["filing_date"],
            "quarter_end": last, "customers": [{"label": label(c), "pct": v * 100 if v <= 1 else v} for c, v in cur],
            "year_ago_top": (max(v for _, v in ya) * 100 if ya and max(v for _, v in ya) <= 1 else (max(v for _, v in ya) if ya else None)),
            "year_ago_end": ya_end if ya else None}


# ---------------------------------------------------------------------------
# 未履約合約（RPO）近 8 季
# ---------------------------------------------------------------------------
def collect_rpo(t: str) -> dict:
    f = facts_for(t)
    xs = S.instants(f, "RevenueRemainingPerformanceObligation")
    if not xs:
        raise RuntimeError(f"{t} 沒有 RPO 事實")
    xs = xs[-8:]
    return {"series": [{"end": r["end"], "value": r["val"]} for r in xs]}


# ---------------------------------------------------------------------------
# BDC 淨值與股價（指標 10）
# ---------------------------------------------------------------------------
def collect_bdc_nav(t: str) -> dict:
    f = facts_for(t)
    rs = S.rows(f, "NetAssetValuePerShare", unit="USD/shares")
    if not rs:
        rs = S.rows(f, "NetAssetValuePerShare")
    rs = [r for r in rs if not r.get("start") or r.get("start") == r["end"]]
    if not rs:
        raise RuntimeError(f"{t} 沒有每股淨值（10-Q／10-K）")
    last = max(rs, key=lambda r: (r["end"], r.get("filed", "")))
    return {"nav": last["val"], "asof": last["end"], "filed": last.get("filed")}


def _yf_download(tickers: list[str], period: str, auto_adjust: bool):
    import yfinance as yf
    df = yf.download(tickers, period=period, interval="1d", auto_adjust=auto_adjust, progress=False,
                     group_by="ticker", threads=False)
    if df is None or len(df) == 0:
        raise RuntimeError("yfinance 回傳空資料")
    return df


def _closes(df, t: str) -> list[tuple[str, float]]:
    s = df[t]["Close"].dropna()
    return [(i.strftime("%Y-%m-%d"), float(v)) for i, v in s.items()]


def collect_bdc_px() -> dict:
    df = _yf_download(BDCS, "10d", auto_adjust=False)   # 淨值比用未還原收盤價
    out = {}
    for t in BDCS:
        c = _closes(df, t)
        if not c:
            raise RuntimeError(f"{t} 沒有收盤價")
        out[t] = {"price": c[-1][1], "asof": c[-1][0]}
    return out


# ---------------------------------------------------------------------------
# 第 7–9 條：相對 QQQ 與遲滯狀態
# ---------------------------------------------------------------------------
def collect_market(prev_data: dict | None) -> dict:
    tickers = list(REL_NAME) + ["QQQ"]
    bootstrap = (not prev_data) or any(t not in prev_data or not prev_data[t].get("flag") for t in REL_NAME)
    df = _yf_download(tickers, "max" if bootstrap else "3y", auto_adjust=True)
    bench = _closes(df, "QQQ")
    out = {}
    for t in REL_NAME:
        stock = _closes(df, t)
        series = rel_series(stock, bench, REL_WINDOW)
        if not series:
            raise RuntimeError(f"{t} 歷史不足 {REL_WINDOW} 個交易日")
        pf = (prev_data or {}).get(t, {}).get("flag") if not bootstrap else None
        state, trans = run_hysteresis(series, state=pf["breached"] if pf else None, after=pf["asof"] if pf else None)
        asof, pp = series[-1]
        b, s = dict(bench), dict(stock)
        j = [dt for dt, _ in stock if dt in b]
        i_now, i_then = j[-1], j[-1 - REL_WINDOW]
        since = trans[-1]["date"] if trans else (pf.get("since") if pf else None)
        out[t] = {
            "rel_pp": pp, "asof": asof,
            "ret_stock": (s[i_now] / s[i_then] - 1) * 100, "ret_bench": (b[i_now] / b[i_then] - 1) * 100,
            "dd1y_rel": rel_drawdown_1y(stock, bench),
            "flag": {"breached": state, "asof": asof, "since": since, "bootstrapped": bool(bootstrap)},
        }
    return out


# ---------------------------------------------------------------------------
# FRED 背景利差
# ---------------------------------------------------------------------------
def fetch_fred(sid: str, tries: int = 3) -> list[tuple[str, float]]:
    err = None
    for _ in range(tries):
        try:
            r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", timeout=40)  # 預設 UA；偽瀏覽器 UA 會 stall
            r.raise_for_status()
            out = []
            for row in list(csv.reader(io.StringIO(r.text)))[1:]:
                if len(row) >= 2 and row[1] not in ("", "."):
                    out.append((row[0], float(row[1])))
            if not out:
                raise RuntimeError("空資料")
            return out
        except Exception as e:  # noqa: BLE001
            err = e
    raise RuntimeError(f"FRED {sid} 抓取失敗：{err!r}")


def spread_stats(series: list[tuple[str, float]]) -> dict:
    last_d, last_v = series[-1]
    ago_cut = (date.fromisoformat(last_d) - timedelta(days=365)).isoformat()
    ago = [x for x in series if x[0] <= ago_cut]
    vals = [v for _, v in series]
    lo, hi = min(vals), max(vals)
    return {"latest": last_v, "asof": last_d, "year_ago": ago[-1][1] if ago else None, "year_ago_date": ago[-1][0] if ago else None,
            "min": lo, "max": hi, "range_start": series[0][0], "pos": (last_v - lo) / (hi - lo) if hi > lo else None}


def collect_fred() -> dict:
    out = {}
    for sid, label in FRED_SERIES:
        st = spread_stats(fetch_fred(sid))
        st["label"] = label
        out[sid] = st
    return out
