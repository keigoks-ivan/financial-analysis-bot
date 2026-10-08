"""美國財政部 FiscalData API：公共債務（每日）、關稅收入（MTS 月）、TGA（DTS 每日）、MTS 表 9 收支分項（月）、
公債未償餘額組成（MSPD 表 1）、平均票面利率、利息費用、標售結果。"""
import json
import time

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


def _f(v):
    return to_float(v)


def parse_mts9(rows, section, label, scale=1e9):
    """MTS 表 9（按來源與功能別）：S 列標出「Receipts／Net Outlays」兩段，同名項目只取指定段的當月金額（美元 -> scale）。"""
    rows = sorted(rows, key=lambda r: (r["record_date"], int(to_float(r.get("src_line_nbr")) or 0)))
    out, cur = {}, {}
    for r in rows:
        d = r["record_date"]
        name = (r.get("classification_desc") or "").strip()
        if r.get("data_type_cd") == "S" and name in ("Receipts", "Net Outlays"):
            cur[d] = name
        if cur.get(d) == section and name == label:
            v = _f(r.get("current_month_rcpt_outly_amt"))
            if v is not None:
                out[month_first(d)] = round(v / scale, 4)
    return sorted(out.items())


def parse_mspd1(rows, scale=1e6):
    """MSPD 表 1：公眾持有金額（百萬美元）-> 兆美元。只取該類證券，月末日期轉當月 1 日。"""
    out = {}
    for r in rows:
        v = _f(r.get("debt_held_public_mil_amt"))
        if v is not None:
            out[month_first(r["record_date"])] = round(v / scale, 6)
    return sorted(out.items())


def parse_avg_rate(rows, field="avg_interest_rate_amt"):
    out = {}
    for r in rows:
        v = _f(r.get(field))
        if v is not None:
            out[month_first(r["record_date"])] = v
    return sorted(out.items())


def parse_int_exp(rows, prefix, field="month_expense_amt", scale=1e9):
    """利息費用：同月內 expense_catg_desc 以 prefix 開頭的各列加總（美元 -> scale）。"""
    acc = {}
    for r in rows:
        if not (r.get("expense_catg_desc") or "").startswith(prefix):
            continue
        v = _f(r.get(field))
        if v is not None:
            k = month_first(r["record_date"])
            acc[k] = acc.get(k, 0.0) + v
    return sorted((k, round(v / scale, 4)) for k, v in acc.items())


def parse_auction(rows, orig_term, field, exclude=None, share_of=None):
    """標售結果（每場一點，日期＝標售日）：original_security_term 取指定年期；排除 TIPS（inflation_index_security=Yes）與浮動利率債。
    share_of：用 field／share_of ×100 算占比（例如間接投標人得標額／競標得標額）。"""
    out = {}
    for r in rows:
        if r.get("original_security_term") != orig_term:
            continue
        if any(r.get(k) == v for k, v in (exclude or {}).items()):
            continue
        v = _f(r.get(field))
        if v is None:
            continue
        if share_of:
            den = _f(r.get(share_of))
            if not den:
                continue
            v = v / den * 100.0
        out[r["auction_date"]] = v
    return sorted(out.items())


_CACHE = {}


def _cached(path):
    """同一次抓取內同一張表只下載一次（MTS 表 9 有十幾條序列共用）。"""
    if path not in _CACHE:
        if _CACHE:
            time.sleep(1.0)
        _CACHE[path] = _pages(path)
    return _CACHE[path]


def _load_spec(p):
    kind = p["kind"]
    if kind == "mts9":
        return parse_mts9(_cached("v1/accounting/mts/mts_table_9?sort=record_date,src_line_nbr"),
                          p["section"], p["label"], float(p.get("scale", 1e9)))
    if kind == "mspd1":
        return parse_mspd1(_cached("v1/debt/mspd/mspd_table_1?filter=security_class_desc:eq:%s&sort=record_date"
                                   % p["security_class_desc"].replace(" ", "%20")), float(p.get("scale", 1e6)))
    if kind == "avg_rate":
        return parse_avg_rate(_cached("v2/accounting/od/avg_interest_rates?filter=security_desc:eq:%s&sort=record_date"
                                      % p["security_desc"].replace(" ", "%20")), p.get("field", "avg_interest_rate_amt"))
    if kind == "int_exp":
        return parse_int_exp(_cached("v2/accounting/od/interest_expense?sort=record_date"), p["catg_prefix"],
                             p.get("field", "month_expense_amt"), float(p.get("scale", 1e9)))
    if kind == "auction":
        return parse_auction(_cached("v1/accounting/od/auctions_query?filter=security_type:eq:%s&sort=auction_date"
                                     % p["security_type"]), p["original_security_term"], p["field"],
                             p.get("exclude"), p.get("share_of"))
    return None


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
    _CACHE.clear()
    for s in specs:
        try:
            obs = _load_spec(s["params"])
            if obs is None:
                obs = _load(s["params"]["kind"])
            res[s["sid"]] = {"obs": obs} if obs else {"error": "解析不到資料"}
        except Exception as e:  # noqa: BLE001
            res[s["sid"]] = {"error": str(e)[:200]}
    return res
