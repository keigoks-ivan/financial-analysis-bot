"""第二輪四區（只顯示、不計入越線條數）的純函式與常數。不連網，可離線測試。

登記的 12 條指標與門檻（aic_metrics.py）一律不動；這裡的東西都只在頁面上顯示。
"""
from __future__ import annotations

import re
import statistics
from collections import defaultdict
from datetime import date

import sec_facts as S

# ---------------------------------------------------------------------------
# 區塊 D-1：BDC 實物付息（PIK）占總投資收益
# ---------------------------------------------------------------------------
BDC_ALL = ["ARCC", "OBDC", "BXSL", "FSK", "GBDC", "OCSL", "BBDC", "HTGC", "MAIN"]
BDC_NAME = {"ARCC": "Ares Capital", "OBDC": "Blue Owl Capital Corp", "BXSL": "Blackstone Secured Lending", "FSK": "FS KKR Capital",
            "GBDC": "Golub Capital BDC", "OCSL": "Oaktree Specialty Lending", "BBDC": "Barings BDC", "HTGC": "Hercules Capital",
            "MAIN": "Main Street Capital"}
GROSS_TAG = "GrossInvestmentIncomeOperating"
INT_PIK = "InterestIncomeOperatingPaidInKind"
DIV_PIK = "DividendIncomeOperatingPaidInKind"
# mode "cf"＝companyfacts；mode "ix"＝解析內嵌 XBRL（companyfacts 沒值）
PIK_SPEC = {
    "ARCC": {"mode": "cf", "pik": [INT_PIK, DIV_PIK], "note": "利息與股利的實物付息"},
    "OBDC": {"mode": "cf", "pik": [INT_PIK], "note": "只含利息的實物付息；合併 tag 季值不可靠，不採用"},
    "FSK": {"mode": "cf", "pik": [INT_PIK], "note": "只含利息的實物付息"},
    "GBDC": {"mode": "cf", "pik": [INT_PIK, DIV_PIK], "note": "利息與股利的實物付息"},
    "OCSL": {"mode": "cf", "pik": [INT_PIK], "note": "只含利息的實物付息"},
    "BBDC": {"mode": "cf", "pik": [INT_PIK, DIV_PIK], "note": "利息與股利的實物付息"},
    "HTGC": {"mode": "cf", "pik": [INT_PIK], "note": "只含利息的實物付息"},
    "BXSL": {"mode": "ix", "pik": "us-gaap:" + INT_PIK, "note": "內嵌 XBRL 的利息實物付息（依發行人關係分項加總）"},
    "MAIN": {"mode": "ix", "pik": "main:InvestmentCompanyPercentageOfTotalInvestmentIncomeAttributableToNoncashPaidInKindInterestIncome",
             "note": "公司自己揭露的「實物付息占總投資收益」百分比（取三個月欄）；第四季由年度減前九個月推算"},
}
PIK_NAME_RX = r"^(us-gaap:%s|us-gaap:%s|main:InvestmentCompanyPercentageOfTotalInvestmentIncomeAttributableToNoncashPaidInKindInterestIncome)$" % (INT_PIK, GROSS_TAG)


def quarter_ends(n: int, rows_by_end: dict[str, float]) -> list[str]:
    return sorted(rows_by_end)[-n:]


def pik_series_cf(facts: dict, spec: dict, n: int = 8) -> list[dict]:
    """companyfacts 的 BDC：分子（一至二個 tag 相加）÷ 總投資收益，近 n 季。"""
    gross = S.single_quarters(S.rows(facts, GROSS_TAG))
    piks = [S.single_quarters(S.rows(facts, t)) for t in spec["pik"]]
    piks = [p for p in piks if p]
    if not gross or not piks:
        raise RuntimeError("缺總投資收益或實物付息 tag")
    out = []
    for e in sorted(gross)[-n:]:
        p = sum(q.get(e, 0.0) for q in piks)
        out.append({"end": e, "pik": p, "gross": gross[e], "pct": p / gross[e] * 100 if gross[e] else None})
    return out


def _fact_dollars_by_period(facts: list[dict], name: str, affil_axis: str = "InvestmentIssuerAffiliationAxis") -> dict[tuple, float]:
    """某 tag 的 {(start,end): 值}。有無維度事實就用；否則把「發行人關係」軸的各成員加總。"""
    nodim: dict[tuple, float] = {}
    dim: dict[tuple, dict] = defaultdict(dict)
    for f in facts:
        if f["name"] != name or not f.get("start"):
            continue
        k = (f["start"], f["end"])
        if not f["dims"]:
            nodim[k] = f["value"]
        elif len(f["dims"]) == 1 and f["dims"][0][0].split(":")[-1] == affil_axis:
            dim[k][f["dims"][0][1]] = f["value"]
    out = {k: sum(v.values()) for k, v in dim.items()}
    out.update(nodim)
    return out


def merge_periods(filings: list[dict], name: str) -> dict[tuple, float]:
    """多份申報檔（舊到新）合併同一 tag 的期間值；同一期間以較新申報為準。"""
    per: dict[tuple, float] = {}
    for fl in sorted(filings, key=lambda x: x["filing_date"]):
        per.update(_fact_dollars_by_period(fl["facts"], name))
    return per


def periods_to_quarters(per: dict[tuple, float]) -> dict[str, float]:
    return S.single_quarters([{"start": s, "end": e, "val": v} for (s, e), v in per.items()])


def pik_series_ix(filings: list[dict], spec: dict, n: int = 8) -> list[dict]:
    gross_per = merge_periods(filings, "us-gaap:" + GROSS_TAG)
    pik_per = merge_periods(filings, spec["pik"])
    if not gross_per or not pik_per:
        raise RuntimeError("內嵌 XBRL 缺總投資收益或實物付息")
    if spec["pik"].startswith("main:"):
        # 公司揭露的是百分比：同一期間乘上總投資收益換成金額，再走一般的累計相減求單季
        pik_per = {k: v * gross_per[k] for k, v in pik_per.items() if k in gross_per}
    gq, pq = periods_to_quarters(gross_per), periods_to_quarters(pik_per)
    ends = [e for e in sorted(gq) if e in pq][-n:]
    return [{"end": e, "pik": pq[e], "gross": gq[e], "pct": pq[e] / gq[e] * 100 if gq[e] else None} for e in ends]


# ---------------------------------------------------------------------------
# 區塊 D-2：BDC 軟體業占比（公允價值）
# ---------------------------------------------------------------------------
# 各家「軟體」算哪些 XBRL 成員（EquitySecuritiesByIndustryAxis 的成員）。成員名稱各家不同，逐家核對過。
SOFTWARE_MEMBERS = {
    "ARCC": ["SoftwareAndServicesMember"],
    "OBDC": ["InternetSoftwareAndServicesMember"],
    "BXSL": ["SoftwareSectorMember"],
    "FSK": ["SoftwareServicesSectorMember"],
    "GBDC": ["SoftwareSectorMember"],
    "MAIN": ["SoftwareMember"],
}
SOFTWARE_NOTE = {
    "ARCC": "軟體與服務（Software and Services）",
    "OBDC": "網路軟體與服務（Internet Software and Services）；不含醫療科技",
    "BXSL": "軟體（Software）",
    "FSK": "軟體與服務（Software and Services）；不含科技硬體",
    "GBDC": "軟體（Software）；不含 IT 服務與醫療科技",
    "MAIN": "軟體（Software）；不含 IT 服務與網路軟體服務",
}


def _short(m: str) -> str:
    return m.split(":")[-1]


def software_share(facts: list[dict], members: list[str]) -> dict:
    """facts：ConcentrationRiskPercentage1 的內嵌 XBRL 事實。取公允價值口徑、最新日期。

    回傳 {pct, asof, total_pct, n_industries}；total_pct 是所有產業加總（自檢，應接近 100）。
    """
    rows = []
    for f in facts:
        d = {a.split(":")[-1]: _short(m) for a, m in f["dims"]}
        ind = d.get("EquitySecuritiesByIndustryAxis")
        bm = d.get("ConcentrationRiskByBenchmarkAxis", "")
        dt = f.get("instant") or f.get("end")
        if ind and "FairValue" in bm and dt:
            rows.append((dt, ind, f["value"] * 100))
    if not rows:
        raise RuntimeError("找不到公允價值口徑的產業占比")
    last = max(r[0] for r in rows)
    cur = {ind: v for dt, ind, v in rows if dt == last}
    sw = [cur[m] for m in members if m in cur]
    if not sw:
        raise RuntimeError(f"產業成員 {members} 不在 {sorted(cur)[:5]}…")
    return {"pct": sum(sw), "asof": last, "total_pct": sum(cur.values()), "n_industries": len(cur)}


# ---------------------------------------------------------------------------
# 區塊 D-3：BDC 不計息貸款
# ---------------------------------------------------------------------------
# 一家一條正規式（文字口徑，各家措辭不同）；ARCC 另有 XBRL tag。group 對應見 parse_nonaccrual。
NONACCRUAL_RX = {
    "ARCC": r"non-accrual status represented ([\d.]+)\s*% of the total investments at amortized cost \(or ([\d.]+)\s*% at fair value\)",
    "OBDC": r"(\w+) of our portfolio companies are on non-accrual, which represents ([\d.]+)% of our portfolio at fair value",
    "BXSL": r"Percentage of assets on non-accrual, at amortized cost \(5\)\s*([\d.]+)\s*%\s*([\d.]+)\s*%\s*Percentage of assets on non-accrual, at fair value \(5\)\s*([\d.]+)\s*%\s*([\d.]+)",
    "FSK": r"% of Investments on Non-Accrual \(based on fair value\)\s*([\d.]+)%\s*([\d.]+)%",
    "MAIN": r"comprised ([\d.]+)% and ([\d.]+)% of our total Investment Portfolio at fair value and cost",
    "GBDC": r"at cost and fair value were ([\d.]+)% and ([\d.]+)%",
}
NONACCRUAL_BASIS = {"ARCC": "成本與公允價值", "OBDC": "只給公允價值", "BXSL": "成本與公允價值", "FSK": "只給公允價值",
                    "MAIN": "成本與公允價值", "GBDC": "成本與公允價值"}
ARCC_XBRL = ("arcc:InvestmentOwnedNonAccrualStatusPercentOfCost", "arcc:InvestmentOwnedNonAccrualStatusPercentOfFairValue")


def parse_nonaccrual(t: str, text: str, ix_facts: list[dict] | None = None) -> dict | None:
    """回傳 {cost, fv, via}（百分比，沒有就 None）；全部抓不到回 None。"""
    if t == "ARCC" and ix_facts:
        got = {}
        for nm in ARCC_XBRL:
            c = [f for f in ix_facts if f["name"] == nm and f["instant"] and not f["dims"]]
            if c:
                last = max(f["instant"] for f in c)
                got[nm] = [f for f in c if f["instant"] == last][0]["value"] * 100
        if len(got) == 2:
            return {"cost": got[ARCC_XBRL[0]], "fv": got[ARCC_XBRL[1]], "via": "XBRL"}
    m = re.search(NONACCRUAL_RX[t], text)
    if not m:
        return None
    g = m.groups()
    if t == "ARCC":
        return {"cost": float(g[0]), "fv": float(g[1]), "via": "文字"}
    if t == "OBDC":
        return {"cost": None, "fv": float(g[1]), "via": "文字"}
    if t == "BXSL":
        return {"cost": float(g[0]), "fv": float(g[2]), "via": "文字"}
    if t == "FSK":
        return {"cost": None, "fv": float(g[0]), "via": "文字"}
    if t == "MAIN":
        return {"cost": float(g[1]), "fv": float(g[0]), "via": "文字"}
    if t == "GBDC":
        return {"cost": float(g[0]), "fv": float(g[1]), "via": "文字"}
    return None


def latest_nonaccrual(filings: list[dict]) -> dict:
    """filings 新到舊，各含 meta 與 nonaccrual（dict 或 None）。

    回傳 {value, report_date, filing_date, accession, status}；status：ok＝最新一份抓到；
    miss＝最新一份沒抓到，value 沿用較舊一份；none＝全部沒抓到。miss_accession 是沒抓到的那份。
    """
    if not filings:
        return {"status": "none", "value": None}
    top = filings[0]
    if top.get("nonaccrual"):
        return {"status": "ok", "value": top["nonaccrual"], "report_date": top["report_date"], "filing_date": top["filing_date"],
                "accession": top["accession"], "url": top["url"]}
    for f in filings[1:]:
        if f.get("nonaccrual"):
            return {"status": "miss", "value": f["nonaccrual"], "report_date": f["report_date"], "filing_date": f["filing_date"],
                    "accession": f["accession"], "url": f["url"], "miss_accession": top["accession"], "miss_report_date": top["report_date"],
                    "miss_url": top["url"]}
    return {"status": "none", "value": None, "miss_accession": top["accession"], "miss_report_date": top["report_date"], "miss_url": top["url"]}


# ---------------------------------------------------------------------------
# 區塊 E-1：雲端營收 ÷ 資本支出
# ---------------------------------------------------------------------------
# 分部營收：(公司, 顯示名, 成員, 營收 tag 優先序)；成員必須是該事實唯一的維度成員
CLOUD_REV = {
    "AWS": {"t": "AMZN", "members": ["AmazonWebServicesSegmentMember", "AmazonWebServicesMember"], "label": "AWS"},
    "GCP": {"t": "GOOGL", "members": ["GoogleCloudMember"], "label": "Google Cloud"},
    "MSIC": {"t": "MSFT", "members": ["IntelligentCloudMember"], "label": "Microsoft Intelligent Cloud"},
    "ORCL_CLOUD": {"t": "ORCL", "members": ["CloudRevenuesMember"], "label": "Oracle 雲端（Cloud revenues）"},
    "ORCL_IAAS": {"t": "ORCL", "members": ["CloudInfrastructureMember"], "label": "Oracle 雲端基礎設施（IaaS）"},
}
REV_NAMES = r"^us-gaap:(Revenues|RevenueFromContractWithCustomerExcludingAssessedTax)$"
AWS_CAPEX_NAME = "us-gaap:SegmentExpenditureAdditionToLongLivedAssets"
CAPEX_FIRM = {"AMZN": "PaymentsToAcquireProductiveAssets"}  # 其餘 PaymentsToAcquirePropertyPlantAndEquipment
CAPEX_FIRM_DEFAULT = "PaymentsToAcquirePropertyPlantAndEquipment"


def segment_periods(filings: list[dict], names: set[str] | None, members: list[str], with_operating: bool = False) -> dict[tuple, float]:
    """某分部成員的 {(start,end): 值}。維度成員必須恰好是 [成員]（with_operating 時是 [OperatingSegmentsMember, 成員]）。"""
    per: dict[tuple, float] = {}
    for fl in sorted(filings, key=lambda x: x["filing_date"]):
        for f in fl["facts"]:
            if names is not None and f["name"] not in names:
                continue
            ms = sorted(_short(m) for _, m in f["dims"])
            ok = False
            for m in members:
                want = sorted([m, "OperatingSegmentsMember"]) if with_operating else [m]
                if ms == want:
                    ok = True
            if ok and f.get("start"):
                per[(f["start"], f["end"])] = f["value"]
    return per


def _near(a: str, b: str, tol: int = 4) -> bool:
    return abs((S.d(a) - S.d(b)).days) <= tol


def cloud_ratio_table(rev_q: dict[str, float], capex_q: dict[str, float], n: int = 8) -> dict:
    """營收季序列與資本支出季序列（季末日容許幾天誤差）→ 近 n 季比值與近四季比值。"""
    ends = sorted(rev_q)[-n:]
    rows = []
    for e in ends:
        ce = next((k for k in capex_q if _near(k, e)), None)
        rows.append({"end": e, "rev": rev_q[e], "capex": capex_q.get(ce) if ce else None,
                     "ratio": (rev_q[e] / capex_q[ce]) if ce and capex_q[ce] else None})
    last4 = rows[-4:]
    ttm = None
    if len(last4) == 4 and all(r["capex"] for r in last4):
        ttm = sum(r["rev"] for r in last4) / sum(r["capex"] for r in last4)
    return {"rows": rows, "ttm": ttm, "ttm_rev": sum(r["rev"] for r in last4) if len(last4) == 4 else None,
            "ttm_capex": sum(r["capex"] for r in last4 if r["capex"]) if len(last4) == 4 and all(r["capex"] for r in last4) else None}


# ---------------------------------------------------------------------------
# 區塊 E-2：GPU 租價
# ---------------------------------------------------------------------------
GPU_MODELS = ["H100", "H200", "B200", "B300", "A100"]
VAST_NAMES = {"H100": ["H100 SXM", "H100 PCIE", "H100 NVL"], "H200": ["H200", "H200 NVL"], "B200": ["B200"], "B300": ["B300"],
              "A100": ["A100 SXM4", "A100 PCIE", "A100 SXM"]}
SHADE_TYPES = {"H100": ["H100", "H100_nvl"], "H200": ["H200"], "B200": ["B200"], "B300": ["B300"], "A100": ["A100", "A100_80G"]}
GPU_START = "2026-10-17"


def vast_stats(rentable: list[dict], rented: list[dict]) -> dict | None:
    """每 GPU 每小時價（dph_total ÷ num_gpus）：可租中位數、含已租中位數。"""
    r1 = [o["dph_total"] / o["num_gpus"] for o in rentable if o.get("num_gpus")]
    allp = r1 + [o["dph_total"] / o["num_gpus"] for o in rented if o.get("num_gpus")]
    if not allp:
        return None
    return {"rentable_median": statistics.median(r1) if r1 else None, "rentable_n": len(r1),
            "all_median": statistics.median(allp), "all_n": len(allp)}


def shade_stats(types: list[dict], gpu_types: list[str]) -> dict | None:
    """Shadeform 標價：hourly_price 單位是美分，除以 100 再除以 GPU 數。"""
    allp, avail = [], []
    for t in types:
        if t.get("gpu_type") not in gpu_types or not t.get("num_gpus"):
            continue
        p = t["hourly_price"] / 100.0 / t["num_gpus"]
        allp.append(p)
        if any(a.get("available") for a in t.get("availability", [])):
            avail.append(p)
    if not allp:
        return None
    return {"avail_median": statistics.median(avail) if avail else None, "avail_n": len(avail),
            "all_median": statistics.median(allp), "all_n": len(allp)}


# ---------------------------------------------------------------------------
# 區塊 E-3：伺服器折舊年限
# ---------------------------------------------------------------------------
DEP_SPEC = {   # 該公司「伺服器／電腦設備」在耐用年限附註的維度成員（全部要出現）
    "MSFT": {"members": ["ComputerEquipmentMember", "MaximumMember"]},
    "GOOGL": {"members": ["ServersAndNetworkEquipmentMember"]},
    "AMZN": {"members": ["TechnologyEquipmentMember", "MaximumMember"]},
    "META": {"members": ["ServersAndNetworkAssetsComponentsStoredBySuppliersMember", "MaximumMember"]},
    "ORCL": {"members": ["ServersAndNetworkingEquipmentMember"]},
    "CRWV": {"members": ["TechnologyEquipmentMember"]},
}
DEP_TABLE = [   # 常數表。years＝目前伺服器耐用年限；hist＝變動紀錄；src＝來源申報檔
    {"t": "MSFT", "name": "Microsoft", "years": 6.0, "years_text": "6 年", "fy": "6 月結",
     "hist": "2022 年 7 月由 4 年延到 6 年", "src": "10-K FY2023（2023-06-30）附註「會計估計變更」"},
    {"t": "GOOGL", "name": "Alphabet", "years": 6.0, "years_text": "6 年", "fy": "12 月結",
     "hist": "2023 年 1 月起伺服器與網路設備改為 6 年", "src": "10-K FY2023（2023-12-31）管理層討論"},
    {"t": "AMZN", "name": "Amazon", "years": 6.0, "years_text": "6 年（部分設備 5 年）", "fy": "12 月結",
     "hist": "2024 年 1 月由 5 年延到 6 年；2025 年 1 月部分設備縮回 5 年", "src": "10-K FY2023（2023-12-31）、10-K FY2024（2024-12-31）"},
    {"t": "META", "name": "Meta", "years": 5.5, "years_text": "5.5 年", "fy": "12 月結",
     "hist": "2022 年由 4 年延到 4.5 年再延到 5 年；2025 年 1 月延到 5.5 年", "src": "10-K FY2022（2022-12-31）、10-K FY2024（2024-12-31）"},
    {"t": "ORCL", "name": "Oracle", "years": 6.0, "years_text": "6 年", "fy": "5 月結",
     "hist": "FY2023 由 4 年延到 5 年；FY2025 第一季由 5 年延到 6 年", "src": "10-K FY2025（2025-05-31）"},
    {"t": "CRWV", "name": "CoreWeave", "years": 6.0, "years_text": "6 年", "fy": "12 月結",
     "hist": "2023 年 1 月由 5 年延到 6 年", "src": "10-K FY2025（2025-12-31）資料中心設備耐用年限附註"},
]
_WORD_NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
             "twelve": 12, "thirteen": 13, "fifteen": 15, "twenty": 20, "twenty-five": 25, "thirty": 30, "forty": 40}


def parse_years(text: str) -> float | None:
    """耐用年限文字 → 年：P6Y、P5Y0M、six years、5.5、6 years。"""
    s = text.strip().lower()
    m = re.fullmatch(r"p(\d+)y(?:(\d+)m)?", s)
    if m:
        return int(m.group(1)) + (int(m.group(2)) / 12 if m.group(2) else 0)
    m = re.match(r"([\d.]+)", s)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    m = re.match(r"([a-z-]+)", s)
    if m and m.group(1) in _WORD_NUM:
        return float(_WORD_NUM[m.group(1)])
    return None


def server_life(nn_facts: list[dict], members: list[str]) -> dict | None:
    """耐用年限事實裡，維度成員包含 members 全部、且不含 MinimumMember（除非要求）的最新一筆。"""
    want = set(members)
    cand = []
    for f in nn_facts:
        ms = {_short(m) for _, m in f["dims"]}
        if not want <= ms:
            continue
        if "MinimumMember" in ms and "MinimumMember" not in want:
            continue
        y = parse_years(f["text"])
        dt = f.get("instant") or f.get("end")
        if y is not None and dt:
            cand.append((dt, y, f["text"]))
    if not cand:
        return None
    last = max(c[0] for c in cand)
    ys = {c[1] for c in cand if c[0] == last}
    if len(ys) != 1:
        return None
    return {"years": ys.pop(), "asof": last}


def dep_changed(table: list[dict], parsed: dict[str, dict | None]) -> list[dict]:
    """parsed：{ticker: {years, asof, accession, report_date}|None}。回傳年限與常數表不同的項目。"""
    out = []
    for row in table:
        p = parsed.get(row["t"])
        if p and abs(p["years"] - row["years"]) > 1e-9:
            out.append({"t": row["t"], "name": row["name"], "old": row["years"], "new": p["years"], "accession": p.get("accession"),
                        "report_date": p.get("report_date")})
    return out


# ---------------------------------------------------------------------------
# 區塊 D 開頭：IGV 對 QQQ
# ---------------------------------------------------------------------------
def own_drawdown_1y(px: list[tuple[str, float]], window: int = 252) -> float | None:
    if len(px) < 2:
        return None
    w = [p for _, p in px][-window:]
    return (w[-1] / max(w) - 1.0) * 100.0


def weekly_index(stock: list[tuple[str, float]], bench: list[tuple[str, float]], window: int = 252, step: int = 5) -> list[list]:
    """近 window 個共同交易日、每 step 個取一點（含最後一天）；兩條都在起點訂為 100。"""
    b = dict(bench)
    joint = [(dt, p, b[dt]) for dt, p in stock if dt in b][-window:]
    if len(joint) < 2:
        return []
    idx = list(range(0, len(joint), step))
    if idx[-1] != len(joint) - 1:
        idx.append(len(joint) - 1)
    p0, q0 = joint[0][1], joint[0][2]
    return [[joint[i][0], round(joint[i][1] / p0 * 100, 2), round(joint[i][2] / q0 * 100, 2)] for i in idx]


def days_between(a: str, b: str) -> int:
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


# ---------------------------------------------------------------------------
# 通知與每日快照（純函式，build_ai_credit.py 呼叫）
# ---------------------------------------------------------------------------
NONACCRUAL_BDCS = ["ARCC", "OBDC", "BXSL", "FSK", "MAIN", "GBDC"]


def build_notices(bdc_filings: dict[str, list[dict]], dep_rows: list[dict], notified: dict) -> tuple[list[dict], dict]:
    """產生資料通知。同一份申報只通知一次（以申報序號記在 notified）。

    bdc_filings：{ticker: 新到舊的申報列}；dep_rows：dep_changed() 的結果。
    回傳 (notices, 新的 notified)；呼叫端決定要不要把新的 notified 寫回 state（--no-notify 時不寫）。
    """
    notices: list[dict] = []
    new = {k: dict(v) for k, v in notified.items()}
    for t in NONACCRUAL_BDCS:
        la = latest_nonaccrual(bdc_filings.get(t) or [])
        if la["status"] == "ok":
            continue
        acc = la.get("miss_accession")
        if not acc or acc in new.get("nonaccrual", {}):
            continue
        last = ("，頁面顯示上次值（%s 申報檔）" % la["report_date"]) if la["status"] == "miss" else "，目前沒有可顯示的上次值"
        notices.append({"kind": "fetch", "key": ("nonaccrual", acc),
                        "title": f"{t} 不計息貸款 {la['miss_report_date']} 申報檔本期未抓到",
                        "body": f"{t}（{BDC_NAME[t]}）{la['miss_report_date']} 的申報檔解析不到不計息貸款占比{last}。申報檔：{la['miss_url']}。可能是文字格式改了，需要調整解析規則。"})
        new.setdefault("nonaccrual", {})[acc] = t
    for c in dep_rows:
        acc = c.get("accession")
        if not acc or acc in new.get("dep", {}):
            continue
        notices.append({"kind": "change", "key": ("dep", acc),
                        "title": f"{c['name']} 伺服器耐用年限由 {c['old']:g} 年改為 {c['new']:g} 年",
                        "body": f"{c['name']} 最新 10-K（{c.get('report_date')}）的伺服器耐用年限為 {c['new']:g} 年，與頁面常數表的 {c['old']:g} 年不同。請核對申報檔並更新 DEP_TABLE。"})
        new.setdefault("dep", {})[acc] = c["t"]
    return notices, new


def gpu_row(today: str, vast: dict | None, shade: dict | None) -> dict:
    """當天一列 GPU 租價；兩個來源都沒有資料時 vast、shade 都是 None。"""
    return {"date": today, "vast": vast, "shade": shade}


def upsert_gpu_rows(lines: list[str], row: dict) -> list[str]:
    """同一天重跑就覆寫當天那一列。lines 是既有 jsonl 的各行。"""
    import json as _json
    keep = [ln for ln in lines if ln.strip() and _json.loads(ln).get("date") != row["date"]]
    keep.append(_json.dumps(row, ensure_ascii=False))
    return sorted(keep, key=lambda ln: _json.loads(ln)["date"])
