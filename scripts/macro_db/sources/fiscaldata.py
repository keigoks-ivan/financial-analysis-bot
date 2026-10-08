"""美國財政部 FiscalData API：公共債務（每日）、關稅收入（MTS 月）、TGA（DTS 每日）。"""
import json

from ._http import get, month_first, to_float

BASE = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"


def _pages(path):
    out, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        j = json.loads(get(BASE + path + "%spage[size]=10000&page[number]=%d" % (sep, page)))
        out += j.get("data", [])
        meta = j.get("meta", {})
        if page >= int(meta.get("total-pages", 1)):
            return out
        page += 1


def parse_debt(rows):
    """每日公共債務總額（美元）-> 十億美元。"""
    obs = {}
    for r in rows:
        v = to_float(r.get("tot_pub_debt_out_amt"))
        if v is not None:
            obs[r["record_date"]] = round(v / 1e9, 3)
    return sorted(obs.items())


def parse_customs(rows):
    """MTS Table 4：關稅收入，當月金額（美元）-> 百萬美元，月末日期轉當月 1 日。"""
    obs = {}
    for r in rows:
        if r.get("classification_desc") != "Customs Duties":
            continue
        v = to_float(r.get("current_month_gross_rcpt_amt"))
        if v is not None:
            obs[month_first(r["record_date"])] = round(v / 1e6, 3)
    return sorted(obs.items())


def parse_tga(rows):
    """TGA 期初餘額（百萬美元）。"""
    obs = {}
    for r in rows:
        v = to_float(r.get("open_today_bal"))
        if v is not None:
            obs[r["record_date"]] = v
    return sorted(obs.items())


def _load(kind):
    if kind == "debt_penny":
        return parse_debt(_pages("v2/accounting/od/debt_to_penny?sort=record_date&fields=record_date,tot_pub_debt_out_amt"))
    if kind == "customs":
        return parse_customs(_pages(
            "v1/accounting/mts/mts_table_4?sort=record_date&fields=record_date,classification_desc,current_month_gross_rcpt_amt"
            "&filter=classification_desc:eq:Customs%20Duties"))
    if kind == "tga":
        return parse_tga(_pages(
            "v1/accounting/dts/operating_cash_balance?sort=record_date&fields=record_date,account_type,open_today_bal"
            "&filter=account_type:eq:Treasury%20General%20Account%20(TGA)%20Opening%20Balance"))
    raise ValueError("未知 kind：%s" % kind)


def fetch(specs):
    res = {}
    for s in specs:
        try:
            obs = _load(s["params"]["kind"])
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
