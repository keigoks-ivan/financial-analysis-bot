"""第二輪四區的資料抓取（會連網）。規則同 aic_sources.py：抓不到就丟例外，由呼叫端沿用上次值；絕不編數字。

內嵌 XBRL 的大申報檔以「申報序號」快取在 state 裡：同一份申報只下載、解析一次，
每天只有出現新申報時才會重新下載。
"""
from __future__ import annotations

import json
import re
import time
from datetime import timedelta

import requests

import aic_round2 as R
import aic_sources as SRC
import ixparse as IX
import sec_facts as S

UA_GENERIC = {"User-Agent": "financial-analysis-bot keigoks@gmail.com"}
FILING_TICKERS = ["MSFT", "GOOGL", "AMZN", "META", "ORCL", "CRWV", "NVDA", "AVGO", "AMD"] + R.BDC_ALL
PARSE_VER = 1   # 解析規則改版時加一，讓快取的申報檔重新解析


# ---------------------------------------------------------------------------
# 各公司最新 10-Q／10-K 的網址（頁面上每個數字的來源連結用）
# ---------------------------------------------------------------------------
def collect_filings() -> dict:
    out, err = {}, []
    for t in FILING_TICKERS:
        try:
            ps = IX.periodics(t, 12)
            q = next((p for p in ps if p["form"] == "10-Q"), None)
            k = next((p for p in ps if p["form"] == "10-K"), None)
            out[t] = {"10-Q": q, "10-K": k}
        except Exception as e:  # noqa: BLE001
            err.append(f"{t}: {e!r}"[:120])
        time.sleep(0.2)
    if len(out) < len(FILING_TICKERS) * 0.7:
        raise RuntimeError("申報檔清單大半抓不到：" + "；".join(err[:3]))
    return out


# ---------------------------------------------------------------------------
# 內嵌 XBRL 申報檔歷史（以申報序號快取）
# ---------------------------------------------------------------------------
def ix_history(t: str, name_rx: str, keep, sig: str, prev: dict | None, n: int = 4) -> dict:
    """最近 n 份 10-Q／10-K 的內嵌 XBRL 事實。keep(fact)->bool 決定存哪些；sig 是 keep 規則的簽名（變了就重解析）。"""
    metas = IX.periodics(t, n)
    old = {f["accession"]: f for f in (prev or {}).get("filings", []) if f.get("sig") == sig and f.get("ver") == PARSE_VER}
    filings = []
    for m in metas:
        if m["accession"] in old:
            filings.append(old[m["accession"]])
            continue
        h = IX.fetch_html(m["url"])
        fs = IX.facts(h, name_rx)
        kept = [{"name": f["name"], "value": f["value"], "dims": [list(d) for d in f["dims"]], "start": f["start"],
                 "end": f["end"], "instant": f["instant"]} for f in fs if keep(f)]
        filings.append({**m, "sig": sig, "ver": PARSE_VER, "facts": kept})
        time.sleep(0.4)
    return {"filings": filings}


# ---------------------------------------------------------------------------
# 區塊 D：IGV 對 QQQ
# ---------------------------------------------------------------------------
def collect_igv() -> dict:
    df = SRC._yf_download(["IGV", "QQQ"], "2y", auto_adjust=True)
    igv, qqq = SRC._closes(df, "IGV"), SRC._closes(df, "QQQ")
    from aic_metrics import REL_WINDOW, rel_drawdown_1y, rel_series
    series = rel_series(igv, qqq, REL_WINDOW)
    if not series:
        raise RuntimeError("IGV 歷史不足")
    asof, pp = series[-1]
    return {"asof": asof, "rel_pp": pp, "rel_dd_1y": rel_drawdown_1y(igv, qqq), "own_dd_1y": R.own_drawdown_1y(igv),
            "chart": R.weekly_index(igv, qqq)}


# ---------------------------------------------------------------------------
# 區塊 D：BDC 實物付息
# ---------------------------------------------------------------------------
def collect_pik(t: str, prev: dict | None) -> dict:
    spec = R.PIK_SPEC[t]
    if spec["mode"] == "cf":
        series = R.pik_series_cf(SRC.facts_for(t), spec)
        return {"series": series, "note": spec["note"], "source": "companyfacts"}
    hist = ix_history(t, R.PIK_NAME_RX, lambda f: not f["dims"] or (len(f["dims"]) == 1 and f["dims"][0][0].endswith("InvestmentIssuerAffiliationAxis")),
                      "pik1", prev)
    series = R.pik_series_ix(hist["filings"], spec)
    return {"series": series, "note": spec["note"], "source": "inline-xbrl", "filings": hist["filings"]}


# ---------------------------------------------------------------------------
# 區塊 D：BDC 軟體占比與不計息貸款（最近兩份申報）
# ---------------------------------------------------------------------------
def collect_bdc_filing(t: str, prev: dict | None) -> dict:
    metas = IX.periodics(t, 2)
    old = {f["accession"]: f for f in (prev or {}).get("filings", []) if f.get("ver") == PARSE_VER}
    out = []
    for m in metas:
        if m["accession"] in old:
            out.append(old[m["accession"]])
            continue
        h = IX.fetch_html(m["url"])
        text = IX.filing_text(h)
        rec = {**m, "ver": PARSE_VER, "software": None, "software_err": None, "nonaccrual": None}
        if t in R.SOFTWARE_MEMBERS:
            try:
                rec["software"] = R.software_share(IX.facts(h, r"^us-gaap:ConcentrationRiskPercentage1$"), R.SOFTWARE_MEMBERS[t])
            except Exception as e:  # noqa: BLE001
                rec["software_err"] = str(e)[:160]
        ixf = IX.facts(h, r"^arcc:InvestmentOwnedNonAccrualStatusPercentOf") if t == "ARCC" else None
        rec["nonaccrual"] = R.parse_nonaccrual(t, text, ixf)
        out.append(rec)
        time.sleep(0.4)
    return {"filings": out}


# ---------------------------------------------------------------------------
# 區塊 E：雲端營收 ÷ 資本支出
# ---------------------------------------------------------------------------
def _seg_keep(members: list[str]):
    ms = set(members) | {"OperatingSegmentsMember"}

    def keep(f):
        short = {m.split(":")[-1] for _, m in f["dims"]}
        return bool(short) and short <= ms and bool(short & set(members))
    return keep


def collect_cloud_roi(key: str, prev: dict | None) -> dict:
    """key：AWS／GCP／MSIC／ORCL。回傳近 8 季營收、資本支出與比值。"""
    cfg = {"AWS": ("AMZN", ["AWS"]), "GCP": ("GOOGL", ["GCP"]), "MSIC": ("MSFT", ["MSIC"]), "ORCL": ("ORCL", ["ORCL_CLOUD", "ORCL_IAAS"])}[key]
    t, subs = cfg
    all_members = sorted({m for s in subs for m in R.CLOUD_REV[s]["members"]})
    name_rx = REV_RX = R.REV_NAMES
    if key == "AWS":
        name_rx = r"^(us-gaap:(Revenues|RevenueFromContractWithCustomerExcludingAssessedTax)|us-gaap:SegmentExpenditureAdditionToLongLivedAssets)$"
    hist = ix_history(t, name_rx, _seg_keep(all_members), "seg1:" + ",".join(all_members), prev)
    facts_cap = SRC.facts_for(t)
    cx_tag = R.CAPEX_FIRM.get(t, R.CAPEX_FIRM_DEFAULT)
    capex_q = S.single_quarters(S.rows(facts_cap, cx_tag))
    if not capex_q:
        raise RuntimeError(f"{t} 沒有 {cx_tag} 單季值")
    revnames = {"us-gaap:Revenues", "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"}
    out = {"filings": hist["filings"], "capex_tag": cx_tag, "lines": {}}
    for s in subs:
        per = R.segment_periods(hist["filings"], revnames, R.CLOUD_REV[s]["members"])
        rev_q = R.periods_to_quarters(per)
        if len(rev_q) < 4:
            raise RuntimeError(f"{t} {s} 分部營收季數不足（{len(rev_q)}）")
        line = R.cloud_ratio_table(rev_q, capex_q)
        out["lines"][s] = {"label": R.CLOUD_REV[s]["label"], **line}
    if key == "AWS":
        per = R.segment_periods(hist["filings"], {R.AWS_CAPEX_NAME}, R.CLOUD_REV["AWS"]["members"], with_operating=True)
        seg_q = R.periods_to_quarters(per)
        rev_q = {r["end"]: r["rev"] for r in out["lines"]["AWS"]["rows"]}
        if len(seg_q) >= 4:
            out["lines"]["AWS_SEG"] = {"label": "AWS（分母改用 AWS 分部資本支出）", **R.cloud_ratio_table(rev_q, seg_q)}
    return out


# ---------------------------------------------------------------------------
# 區塊 E：GPU 租價（非官方端點；失敗不讓 workflow 失敗）
# ---------------------------------------------------------------------------
def _vast_query(names: list[str], lo: float, hi: float, rentable: bool | None) -> list[dict]:
    body = {"gpu_name": {"in": names}, "type": "on-demand", "limit": 1000, "num_gpus": {"gte": 1}, "dph_total": {"gte": lo, "lte": hi}}
    if rentable is not None:
        body["rentable"] = {"eq": rentable}
    last = None
    for i in range(3):
        try:
            r = requests.get("https://console.vast.ai/api/v0/bundles/", params={"q": json.dumps(body)}, headers=UA_GENERIC, timeout=60)
            r.raise_for_status()
            return r.json().get("offers", [])
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"vast.ai 查詢失敗：{last!r}")


def _vast_band(names, lo, hi, rentable, depth=0, cap=64) -> dict:
    """單一查詢最多回 64 筆；滿了就把價格區間對半切再查，直到每段都不滿。"""
    o = _vast_query(names, lo, hi, rentable)
    time.sleep(0.25)
    if len(o) < cap or depth >= 9 or hi - lo < 0.005:
        return {x["id"]: x for x in o}
    mid = (lo + hi) / 2
    a = _vast_band(names, lo, mid, rentable, depth + 1, cap)
    b = _vast_band(names, mid, hi, rentable, depth + 1, cap)
    a.update(b)
    return a


def collect_gpu_vast() -> dict:
    out = {}
    for model, names in R.VAST_NAMES.items():
        rentable = list(_vast_band(names, 0.0, 400.0, True).values())
        allo = list(_vast_band(names, 0.0, 400.0, None).values())
        rented = [o for o in allo if not o.get("rentable")]
        st = R.vast_stats(rentable, rented)
        if st:
            out[model] = st
    if not out:
        raise RuntimeError("vast.ai 沒有任何型號的報價")
    return out


def collect_gpu_shade() -> dict:
    r = requests.get("https://api.shadeform.ai/v1/instances/types", headers=UA_GENERIC, timeout=60)
    r.raise_for_status()
    types = r.json().get("instance_types", [])
    out = {}
    for model, gts in R.SHADE_TYPES.items():
        st = R.shade_stats(types, gts)
        if st:
            out[model] = st
    if not out:
        raise RuntimeError("Shadeform 沒有任何型號的報價")
    return out


# ---------------------------------------------------------------------------
# 區塊 E：伺服器折舊年限（每份新 10-K 比對）
# ---------------------------------------------------------------------------
def collect_dep(prev: dict | None) -> dict:
    """每家取最新 10-K，用 XBRL PropertyPlantAndEquipmentUsefulLife 解析伺服器耐用年限。"""
    old = (prev or {}).get("parsed", {})
    parsed, errors = {}, {}
    for row in R.DEP_TABLE:
        t = row["t"]
        try:
            ps = IX.periodics(t, 12)
            k = next((p for p in ps if p["form"] == "10-K"), None)
            if not k:
                raise RuntimeError("找不到 10-K")
            cached = old.get(t)
            if cached and cached.get("accession") == k["accession"] and cached.get("ver") == PARSE_VER and cached.get("years") is not None:
                parsed[t] = cached
                continue
            h = IX.fetch_html(k["url"])
            nn = IX.non_numeric(h, "us-gaap:PropertyPlantAndEquipmentUsefulLife")
            life = R.server_life(nn, R.DEP_SPEC[t]["members"])
            if not life:
                raise RuntimeError("耐用年限事實裡找不到伺服器類別")
            parsed[t] = {**life, "accession": k["accession"], "report_date": k["report_date"], "filing_date": k["filing_date"],
                         "url": k["url"], "ver": PARSE_VER}
            time.sleep(0.4)
        except Exception as e:  # noqa: BLE001
            errors[t] = str(e)[:160]
            if old.get(t):
                parsed[t] = old[t]
    if not parsed:
        raise RuntimeError("伺服器耐用年限全部解析失敗：" + "；".join(f"{k}:{v}" for k, v in list(errors.items())[:3]))
    return {"parsed": parsed, "errors": errors}


# ---------------------------------------------------------------------------
# 區塊 A 補充：負債公允價值 ÷ 帳面價值
# ---------------------------------------------------------------------------
def periodics_ext(t: str, n: int) -> list[dict]:
    """最近 n 份 10-Q／10-K（新到舊）。近期清單不夠 n 份時（如上市不久、申報檔很多的 CoreWeave）再補讀 submissions 的舊分頁。"""
    out = IX.periodics(t, n)
    if len(out) >= n:
        return out
    s = S.fetch_submissions(t)
    for fi in s["filings"].get("files", []):
        r = requests.get("https://data.sec.gov/submissions/" + fi["name"], headers=UA_GENERIC, timeout=60)
        r.raise_for_status()
        f = r.json()
        for i, form in enumerate(f["form"]):
            if form in ("10-Q", "10-K"):
                acc = f["accessionNumber"][i]
                out.append({"accession": acc, "form": form, "report_date": f["reportDate"][i], "filing_date": f["filingDate"][i],
                            "url": f"https://www.sec.gov/Archives/edgar/data/{S.CIKS[t]}/{acc.replace('-', '')}/{f['primaryDocument'][i]}"})
        time.sleep(0.2)
    out.sort(key=lambda m: m["filing_date"], reverse=True)
    return out[:n]


def collect_dfv(t: str, prev: dict | None, n: int = 8) -> dict:
    """負債公允價值 ÷ 帳面價值，近 n 季。Microsoft 走 companyfacts；其餘解析內嵌 XBRL（Meta 另有一條文字正規式補本金）。
    申報檔以申報序號快取在 state，同一份只下載解析一次；單一申報抓不到的欄位留 None，由頁面標示並通知。"""
    metas = periodics_ext(t, n)
    if t == "MSFT":
        return {"lines": R.dfv_lines_cf(SRC.facts_for(t), metas, n), "source": "companyfacts"}
    sig = R.DFV_SIG
    old = {f["accession"]: f for f in (prev or {}).get("filings", []) if f.get("sig") == sig and f.get("ver") == PARSE_VER}
    filings = []
    for m in metas:
        if m["accession"] in old:
            filings.append(old[m["accession"]])
            continue
        h = IX.fetch_html(m["url"])
        kept = [{"name": f["name"], "value": f["value"], "dims": [list(d) for d in f["dims"]], "start": f["start"], "end": f["end"],
                 "instant": f["instant"]} for f in IX.facts(h, R.DFV_NAME_RX) if R.dfv_keep(t, f)]
        tb = R.meta_principal(IX.filing_text(h)) if t == "META" else None
        filings.append({**m, "sig": sig, "ver": PARSE_VER, "facts": kept, "text_base": tb})
        time.sleep(0.4)
    return {"lines": R.dfv_lines(t, filings, n), "source": "inline-xbrl", "filings": filings}


# ---------------------------------------------------------------------------
# 區塊 C 補充：Broadcom
# ---------------------------------------------------------------------------
def collect_avgo(prev: dict | None) -> dict:
    f = SRC.facts_for("AVGO")
    g = S.latest_instant(f, "GuaranteeObligationsMaximumExposure")
    rpo = S.latest_instant(f, "RevenueRemainingPerformanceObligation")
    rows = S.rows(f, "RevenueFromContractWithCustomerExcludingAssessedTax")
    ttm = S.ttm_flow(rows)
    if not (g and rpo and ttm):
        raise RuntimeError("AVGO 保證、RPO 或近四季營收找不到")
    meta = IX.periodics("AVGO", 2)[0]
    if prev and prev.get("accession") == meta["accession"] and prev.get("convertible") is not None:
        conv, drawn = prev["convertible"], prev.get("drawn")
    else:
        h = IX.fetch_html(meta["url"])
        cv = [x for x in IX.facts(h, r"^avgo:UncommittedConvertibleNoteFacilityAvailableToCustomer(AmountDrawn)?$") if not x["dims"]]
        a = [x for x in cv if x["name"].endswith("Customer")]
        b = [x for x in cv if x["name"].endswith("Drawn")]
        if not a:
            raise RuntimeError("AVGO 內嵌 XBRL 找不到可轉債額度")
        conv = a[-1]["value"]
        drawn = b[-1]["value"] if b else None
    return {"accession": meta["accession"], "form": meta["form"], "report_date": meta["report_date"], "filing_date": meta["filing_date"],
            "url": meta["url"], "guarantee": g["val"], "guarantee_date": g["end"], "convertible": conv, "drawn": drawn,
            "rpo": rpo["val"], "rpo_date": rpo["end"], "rev_ttm": ttm["value"], "rev_end": ttm["end"]}


# ---------------------------------------------------------------------------
# 區塊 C 補充：OpenAI 曝險（只放財報有寫的數字）
# ---------------------------------------------------------------------------
def _num(s: str) -> float:
    return float(s.replace(",", "").strip())


def _rx(text: str, pat: str, what: str) -> re.Match:
    m = re.search(pat, text, re.S)
    if not m:
        raise RuntimeError(f"申報檔文字找不到：{what}")
    return m


def _latest(fs: list[dict], need: set[str], dur: bool = False) -> dict | None:
    c = [f for f in fs if {m.split(":")[-1] for _, m in f["dims"]} == need]
    if dur:
        c = [f for f in c if f["start"] and f["end"] and S.d(f["end"]) - S.d(f["start"]) >= timedelta(days=80)]
    if not c:
        return None
    last = max(f["end"] or f["instant"] for f in c)
    c = [f for f in c if (f["end"] or f["instant"]) == last]
    return max(c, key=lambda f: (S.d(f["end"]) - S.d(f["start"])).days if f["start"] and f["end"] else 0)


def _oa_msft(h: str, text: str, meta: dict) -> dict:
    fs = IX.facts(h, r"^(us-gaap|msft):(EquityMethod\w+|RevenueFromContractWithCustomerExcludingAssessedTax|AccountsReceivableNet|NonoperatingIncomeExpense|Revenues)$")
    oa = {"OpenAIGlobalLlcMember"}

    def pick(name, dur=False):
        return _latest([f for f in fs if f["name"].split(":")[-1] == name and f["dims"]], oa, dur)

    own = pick("EquityMethodInvestmentOwnershipPercentage")
    rev = pick("RevenueFromContractWithCustomerExcludingAssessedTax", True)
    ar = pick("AccountsReceivableNet")
    commit = pick("EquityMethodInvestmentsTotalFundingCommitments")
    funded = pick("EquityMethodInvestmentsFunded")
    gl = pick("NonoperatingIncomeExpense", True)
    if not (own and rev and ar and commit and funded):
        raise RuntimeError("MSFT 內嵌 XBRL 缺 OpenAI 持股、營收、應收或出資")
    tot = [f for f in fs if f["name"] in ("us-gaap:Revenues", "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax") and not f["dims"]
           and f["start"] == rev["start"] and f["end"] == rev["end"]]
    share = rev["value"] / tot[0]["value"] * 100 if tot else None
    return {"ownership_pct": own["value"] * 100, "own_date": own["instant"] or own["end"],
            "rev": rev["value"], "rev_start": rev["start"], "rev_end": rev["end"], "rev_share_pct": share,
            "ar": ar["value"], "ar_date": ar["instant"] or ar["end"], "commit": commit["value"], "funded": funded["value"],
            "commit_date": commit["instant"] or commit["end"], "gain": gl["value"] if gl else None,
            "gain_start": gl["start"] if gl else None, "gain_end": gl["end"] if gl else None}


def _oa_nvda(h: str, text: str, meta: dict) -> dict:
    m = _rx(text, r"guarantees, capped at a total of \$\s*([\d.,]+)\s*billion.{0,200}?OpenAI.{0,400}?approximately ([\d.]+) gigawatts", "SB Energy 保證上限")
    life = re.search(r"([\d]+)\s*-?\s*year lease term", text[m.end():m.end() + 1500])
    return {"cap": _num(m.group(1)) * 1e9, "gw": float(m.group(2)), "lease_years": int(life.group(1)) if life else None}


def _oa_amzn(h: str, text: str, meta: dict) -> dict:
    fs = IX.facts(h, r"^(us-gaap:RevenueRemainingPerformanceObligation|amzn:RevenueRemainingPerformanceObligationAmountPeriodIncreaseDecrease)$")
    oa = {"OpenAIGroupPBCMember"}
    base = _latest([f for f in fs if f["name"].endswith("Obligation")], oa)
    inc = _latest([f for f in fs if f["name"].endswith("IncreaseDecrease")], oa, True)
    if not base or not inc:
        raise RuntimeError("AMZN 內嵌 XBRL 缺 OpenAI 的 AWS 承諾")
    m1 = _rx(text, r"We also invested \$\s*([\d.]+)\s*billion in Series C Preferred Stock of OpenAI.{0,300}?aggregate purchase price of \$\s*([\d.]+)\s*billion", "對 OpenAI 的投資與承諾")
    m2 = re.search(r"In Q2 2026, we invested \$\s*([\d.]+)\s*billion of the Commitment Amount.{0,200}?\$\s*([\d.]+)\s*billion investment in Series C", text)
    m3 = re.search(r"Subsequent to [A-Za-z]+ \d+, \d{4}, we invested the remaining \$\s*([\d.]+)\s*billion Commitment Amount", text)
    m4 = re.search(r"expansion of the existing \$\s*([\d.]+)\s*billion multi-year commitment.{0,80}?by \$\s*([\d.]+)\s*billion over ([\d.]+) years", text)
    return {"aws_years": float(m4.group(3)) if m4 else None, "aws_commit": base["value"], "aws_commit_date": base["instant"] or base["end"], "aws_increase": inc["value"],
            "aws_increase_start": inc["start"], "aws_increase_end": inc["end"],
            "invested_first": float(m1.group(1)) * 1e9, "commitment": float(m1.group(2)) * 1e9,
            "invested_q2": float(m2.group(1)) * 1e9 if m2 else None, "invested_total": float(m2.group(2)) * 1e9 if m2 else None,
            "invested_after": float(m3.group(1)) * 1e9 if m3 else None}


def _oa_amd(h: str, text: str, meta: dict) -> dict:
    m = _rx(text, r"issued warrants to OpenAI OpCo, LLC \(OpenAI\) and Meta Platforms, Inc\. \(Meta\).{0,200}?up to (\d+) million shares.{0,120}?exercise price of \$\s*([\d.]+) per share", "OpenAI 認股權證")
    v = re.search(r"As of ([A-Za-z]+ \d+, \d{4}), no warrant tranches had vested", text)
    return {"shares_m": int(m.group(1)), "strike": float(m.group(2)), "vested_text": v.group(0) if v else None,
            "vested_asof": v.group(1) if v else None}


def _oa_crwv(h: str, text: str, meta: dict) -> dict:
    ms = re.findall(r"OpenAI (?:has )?committed to pay us up to approximately \$\s*([\d.]+)\s*billion through ([A-Za-z]+(?: \d+,)? \d{4})", text)
    if not ms:
        raise RuntimeError("CRWV 申報檔文字找不到 OpenAI 合約上限")
    seen, out = set(), []
    for amt, thr in ms:
        if (amt, thr) not in seen:
            seen.add((amt, thr))
            out.append({"amount": float(amt) * 1e9, "through": thr})
    return {"contracts": out}


OA_PARSERS = {"MSFT": _oa_msft, "NVDA": _oa_nvda, "AMZN": _oa_amzn, "AMD": _oa_amd}


def collect_openai(t: str, prev: dict | None) -> dict:
    """OpenAI 曝險：每家讀最新 10-Q 與 10-K。MSFT、NVDA、AMZN、AMD 從最新一份取數字；
    CRWV 兩份都取合約上限；ORCL、AVGO 只數 OpenAI 在全文出現幾次（0 次＝財報未揭露）。"""
    ps = IX.periodics(t, 12)
    metas = [m for m in (next((p for p in ps if p["form"] == "10-Q"), None), next((p for p in ps if p["form"] == "10-K"), None)) if m]
    metas.sort(key=lambda m: m["filing_date"], reverse=True)
    old = {f["accession"]: f for f in (prev or {}).get("filings", []) if f.get("ver") == PARSE_VER}
    recs = []
    for i, m in enumerate(metas):
        if m["accession"] in old:
            recs.append(old[m["accession"]])
            continue
        h = IX.fetch_html(m["url"])
        text = IX.filing_text(h)
        rec = {**m, "ver": PARSE_VER, "mentions": len(re.findall(r"OpenAI", text)), "parsed": None}
        fn = _oa_crwv if t == "CRWV" else (OA_PARSERS.get(t) if i == 0 else None)
        if fn:
            try:
                rec["parsed"] = fn(h, text, m)
            except Exception as e:  # noqa: BLE001
                rec["parse_err"] = str(e)[:200]
        recs.append(rec)
        time.sleep(0.4)
    return {"filings": recs}
