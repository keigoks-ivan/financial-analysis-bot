"""泰國商務部貿易政策與策略辦公室（TPSO）指數：CPI、PPI、進出口物價、消費者信心（免金鑰）。

端點（皆為 POST，GET 會回 405）：
  月端點  POST https://index-api.tpso.go.th/OpenApi/{Cpig|Ppi|Imex}/Month
          body {"yearBase": 佛曆基期年, "year": 佛曆年, "month": 月, "type": 類型, "commodities": [品項碼…]}
          一次一個月、可同時帶多個品項；官方限速 10 秒 40 次。年份是佛曆（西元＋543）。
  區間端點 POST https://index.tpso.go.th/api/{cpig|ppi|imex|cci}/filter（要先 GET /api/csrf-token 取 cookie）
          一次可抓整段歷史，但 cpig 只回大類（沒有 91000／92000）。
平常只抓最近 4 個月（月端點）；MACRO_DB_BACKFILL=1 時用區間端點抓整段歷史，
並用月端點逐月補 CPI 的 91000（生鮮食品）、92000（能源）——約 320 次請求、同站隔 1 秒，需 6～7 分鐘，只要跑一次。

params：
  api        "cpig"｜"ppi"｜"imex"｜"cci"（必填）
  code       品項碼（cpig／ppi／imex 必填），如 "00000"
  type       類型碼（cpig 用 "TG"；ppi 用 "CPA"／"SOP"；imex 用 "EXI"／"IMI"）
  year_base  佛曆基期年（cpig 2566、ppi 2564、imex 2555）
  name       cci 專用：全國列的泰文名稱（รวม＝總指數、ปัจจุบัน＝現況、อนาคต＝未來預期）
  probe_url  選填（fetcher 不讀）
"""
from __future__ import annotations

import datetime as dt
import os
import time

import requests

try:
    from . import _http
    from . import an_common as A
except ImportError:
    import _http
    import an_common as A

OPEN = "https://index-api.tpso.go.th/OpenApi/%s/Month"
SITE = "https://index.tpso.go.th/"
RECENT_MONTHS = 4
GAP = 1.1
_last = [0.0]
CCI_MONTHS = ["january", "februay", "march", "april", "may", "june", "july", "august",
              "september", "october", "november", "december"]
API_NAME = {"cpig": "Cpig", "ppi": "Ppi", "imex": "Imex"}
# 區間端點的 body 範本與起始佛曆年
RANGE_START = {"cpig": 2530, "ppi": 2538, "imex": 2543}


def _thai_now():
    return dt.datetime.now(dt.timezone.utc).astimezone(dt.timezone(dt.timedelta(hours=7)))


def _wait():
    d = GAP - (time.time() - _last[0])
    if d > 0:
        time.sleep(d)
    _last[0] = time.time()


def _post(sess, url, body, tries=3):
    last = None
    for i in range(tries):
        _wait()
        try:
            r = sess.post(url, json=body, timeout=90)
            if r.status_code == 200:
                return r.json()
            last = RuntimeError("HTTP %s" % r.status_code)
            if r.status_code not in (429, 500, 502, 503, 504):
                break
        except (requests.RequestException, ValueError) as e:
            last = e
        time.sleep(5 * (i + 1))
    raise RuntimeError("%s：%s" % (url[:70], last))


def _csrf(sess):
    _wait()
    r = sess.get(SITE + "api/csrf-token", timeout=60)
    if r.status_code != 200:
        raise RuntimeError("csrf-token HTTP %s" % r.status_code)


def recent_months(today=None, n=RECENT_MONTHS):
    """回傳最近 n 個月的 (佛曆年, 月)，由舊到新（以泰國時間 UTC+7 為準）。"""
    t = today or _thai_now().date()
    y, m = t.year, t.month
    out = []
    for _ in range(n):
        out.append((y + 543, m))
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return out[::-1]


def be_date(be_year, month):
    return A.ym_date(int(be_year) - 543, int(month))


def parse_month_rows(rows) -> dict:
    """月端點回傳 -> {品項碼: [(日期, index)]}。"""
    out: dict = {}
    for r in rows or []:
        if r.get("index") is None:
            continue
        out.setdefault(str(r["commodityCode"]), []).append((be_date(r["year"], r["month"]), r["index"]))
    return out


def parse_range(res, field="index") -> dict:
    """區間端點回傳 -> {品項碼: [(日期, 值)]}；field 用 'indexD' 取美元計價。"""
    out: dict = {}
    for c in res or []:
        code = str(c.get("commodityCode"))
        for y in c.get("years", []):
            for m in y.get("months", []):
                v = m.get(field)
                if v is not None:
                    out.setdefault(code, []).append((be_date(y["year"], m["month"]), v))
    return out


def parse_cci(rows, name) -> list:
    """cci/filter 回傳（一年）-> 全國（typeID==1）指定名稱列的 12 個月值。"""
    out = []
    for r in rows or []:
        if r.get("typeID") == 1 and r.get("name") == name:
            y = r.get("year")
            for i, k in enumerate(CCI_MONTHS):
                if r.get(k) is not None and y:
                    out.append((A.ym_date(int(y) - 543, i + 1), r[k]))
    return out


def _merge(dst, key, pairs):
    dst.setdefault(key, {}).update({d: v for d, v in pairs})


def _fetch_index_group(sess, api, typ, year_base, codes, backfill, store):
    """抓某 (api, type, year_base) 的所有品項，結果寫進 store[code] = {日期: 值}。"""
    name = API_NAME[api]
    if backfill:
        _csrf(sess)
        body = {"YearBase": year_base, "TimeOption": True, "Categories": sorted(codes), "Types": [typ],
                "Period": {"StartYear": RANGE_START[api], "StartMonth": 1,
                           "EndYear": dt.date.today().year + 543, "EndMonth": 12}}
        res = _post(sess, SITE + "api/%s/filter" % api, body)
        # imex 的區間端點同時有泰銖 index 與美元 indexD；月端點的 index 是美元計價，所以取 indexD
        for code, pairs in parse_range(res, "indexD" if api == "imex" else "index").items():
            _merge(store, code, pairs)
    for by, bm in recent_months():
        rows = _post(sess, OPEN % name, {"yearBase": year_base, "year": by, "month": bm, "type": typ,
                                         "commodities": sorted(codes)})
        for code, pairs in parse_month_rows(rows).items():
            _merge(store, code, pairs)


def _backfill_cpi_second_level(sess, codes, year_base, store, start_be=2543):
    """區間端點沒有的第二層品項（91000、92000）：用月端點從 start_be 年逐月補。"""
    need = sorted(c for c in codes if not store.get(c) or len(store[c]) < 100)
    if not need:
        return
    now = dt.date.today()
    for by in range(start_be, now.year + 543 + 1):
        for bm in range(1, 13):
            if by == now.year + 543 and bm > now.month:
                break
            rows = _post(sess, OPEN % "Cpig", {"yearBase": year_base, "year": by, "month": bm, "type": "TG",
                                               "commodities": need})
            for code, pairs in parse_month_rows(rows).items():
                _merge(store, code, pairs)


def fetch(specs: list[dict]) -> dict:
    backfill = os.environ.get("MACRO_DB_BACKFILL") == "1"
    sess = requests.Session()
    sess.headers["User-Agent"] = _http.NAMED_UA
    res: dict = {}
    idx_groups: dict = {}
    cci_specs = []
    for s in specs:
        p = s["params"]
        if p["api"] == "cci":
            cci_specs.append(s)
        else:
            idx_groups.setdefault((p["api"], p["type"], int(p["year_base"])), []).append(s)

    for (api, typ, yb), group in idx_groups.items():
        store: dict = {}
        codes = {str(s["params"]["code"]) for s in group}
        try:
            _fetch_index_group(sess, api, typ, yb, codes, backfill, store)
            if backfill and api == "cpig":
                _backfill_cpi_second_level(sess, codes, yb, store)
        except Exception as e:  # noqa: BLE001
            if not store:
                for s in group:
                    res[s["sid"]] = {"error": "TPSO %s：%s" % (api, str(e)[:160])}
                continue
        for s in group:
            pairs = sorted(store.get(str(s["params"]["code"]), {}).items())
            obs = A.clean_obs(pairs)
            res[s["sid"]] = {"obs": obs} if obs else {"error": "TPSO %s：沒有品項 %s 的資料" % (api, s["params"]["code"])}

    if cci_specs:
        years = []
        this_be = _thai_now().year + 543
        years = list(range(2562, this_be + 1)) if backfill else [this_be - 1, this_be]
        rows_by_year: dict = {}
        err = None
        try:
            _csrf(sess)
            for y in years:
                rows = _post(sess, SITE + "api/cci/filter", {"Year": y})
                for r in rows or []:
                    r.setdefault("year", y)
                rows_by_year[y] = rows
        except Exception as e:  # noqa: BLE001
            err = str(e)[:160]
        for s in cci_specs:
            pairs = []
            for rows in rows_by_year.values():
                pairs += parse_cci(rows, s["params"]["name"])
            obs = A.clean_obs(pairs)
            res[s["sid"]] = {"obs": obs} if obs else {"error": "TPSO cci：%s" % (err or "沒有資料")}
    return res
