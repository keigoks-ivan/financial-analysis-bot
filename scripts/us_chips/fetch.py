#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""美股籌碼（/us-chips/）資料抓取：只抓缺的日子，append 進 data/us_chips/{series}.jsonl。

序列（來源、起始日見 data/us_chips/README.md）：
  idx          三個指數日線收盤（yfinance ^GSPC ^NDX ^SOX）
  cot_spx/ndx  CFTC Traders in Financial Futures（Socrata gpe5-46if，Consolidated 13874+／20974+），週
  si_<ETF>     FINRA 放空餘額（consolidatedShortInterest），每月兩次
  svol_<ETF>   FINRA 每日放空量（CNMSshvol），日
  occ_<ETF>    OCC 分帳戶選擇權成交量（volume-query），日
  vix/vxn/skew Cboe 指數日線 CSV
  pcr          Cboe 全市場 put／call（2006-11 至 2019-10-04 舊 CSV；2019-10-07 起每日 JSON）
  shares_<ETF> 發行商逐日流通份額（沿用 scripts/etf_dash/flows.py 的發行商歷史檔抓法，不限 200 天）
  lev_<ETF>    ProShares 槓桿 ETF 逐日份額與淨值（UPRO／SPXU／SSO／SDS，官方 historical_nav.csv）

用法：
  python3 scripts/us_chips/fetch.py                  # 日常增量
  python3 scripts/us_chips/fetch.py --only svol,occ  # 只跑指定來源
  python3 scripts/us_chips/fetch.py --backfill       # 補歷史（svol 2018-08 起、occ/pcr 各自起點）

每個來源獨立 try/except：失敗印一行 `FAIL <來源>: 原因`，不影響其他來源。
exit code：失敗來源 >= 3 才非 0（代表被擋或整體改版），1～2 個失敗只警告。
jsonl 是 append-only：同鍵內容沒變不寫，有修正就在檔尾加一行，讀入時以同鍵最後一行為準。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "us_chips"
STATE = DATA / "_state.json"
sys.path.insert(0, str(ROOT / "scripts"))

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ET = ZoneInfo("America/New_York")

ETFS = ["SPY", "QQQ", "SMH", "SOXX"]
LEV_PROSHARES = ["UPRO", "SPXU", "SSO", "SDS"]
IDX = {"^GSPC": "spx", "^NDX": "ndx", "^SOX": "sox"}
COT_MARKETS = {"spx": "13874+", "ndx": "20974+"}
SVOL_START = dt.date(2018, 8, 1)     # CNMS 檔最早（更早的 403）
OCC_START = dt.date(2024, 10, 23)    # OCC 只給近兩年；2026-11-03 實測 2024-10-22 以前回空表、2024-10-30 有資料
PCR_DAILY_START = dt.date(2019, 10, 7)   # Cboe 每日 JSON 最早；舊 CSV 到 2019-10-04 止，剛好接上

_s = requests.Session()
_s.headers.update({"User-Agent": UA})


# ------------------------------------------------------------------ jsonl 工具

def load_jsonl(name: str, key: str = "d") -> dict:
    p = DATA / f"{name}.jsonl"
    rows: dict = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                rows[r[key]] = r
    return rows


def append_jsonl(name: str, new_rows: list[dict], key: str = "d") -> int:
    """同鍵內容沒變不寫；回傳實際新增／修正的筆數。"""
    if not new_rows:
        return 0
    DATA.mkdir(parents=True, exist_ok=True)
    cur = load_jsonl(name, key)
    out = []
    for r in new_rows:
        if cur.get(r[key]) != r:
            out.append(r)
            cur[r[key]] = r
    if out:
        with (DATA / f"{name}.jsonl").open("a", encoding="utf-8") as f:
            for r in out:
                f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
    return len(out)


def compact(name: str, key: str = "d") -> None:
    """回補完成後整理成依鍵排序、每鍵一行。"""
    cur = load_jsonl(name, key)
    p = DATA / f"{name}.jsonl"
    with p.open("w", encoding="utf-8") as f:
        for k in sorted(cur):
            f.write(json.dumps(cur[k], ensure_ascii=False, separators=(",", ":")) + "\n")


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"no_data": {}}


def save_state(st: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def get(url: str, retries: int = 3, **kw) -> requests.Response:
    last = None
    for i in range(retries):
        try:
            r = _s.get(url, timeout=40, **kw)
            return r
        except requests.RequestException as e:
            last = e
            time.sleep(2 + 3 * i)
    raise RuntimeError(f"GET {url}: {last}")


def weekdays(a: dt.date, b: dt.date):
    d = a
    while d <= b:
        if d.weekday() < 5:
            yield d
        d += dt.timedelta(days=1)


def today_et() -> dt.date:
    return dt.datetime.now(ET).date()


# ------------------------------------------------------------------ 指數（yfinance）

def fetch_idx(backfill=False):
    import yfinance as yf
    cur = load_jsonl("idx")
    start = "1990-01-01" if not cur else (dt.date.fromisoformat(max(cur)) - dt.timedelta(days=14)).isoformat()
    rows: dict[str, dict] = {}
    for tk, k in IDX.items():
        df = yf.download(tk, start=start, auto_adjust=False, progress=False, threads=False)
        if df is None or df.empty:
            raise RuntimeError(f"{tk} 沒有資料")
        close = df["Close"]
        if hasattr(close, "columns"):
            close = close.iloc[:, 0]
        for ts, v in close.dropna().items():     # 最新一根 NaN（Yahoo 午夜後未定稿）一律丟掉
            rows.setdefault(ts.strftime("%Y-%m-%d"), {"d": ts.strftime("%Y-%m-%d")})[k] = round(float(v), 4)
    # 各指數有值的日子都寫（每個指數起點不同，缺的欄位不寫）；自 1990 起，和 SKEW 同起點
    new = [r for r in rows.values() if r["d"] > "1989-12-31"]
    n = append_jsonl("idx", sorted(new, key=lambda r: r["d"]))
    return f"idx +{n}"


# ------------------------------------------------------------------ CFTC

COT_FIELDS = {
    "oi": "open_interest_all",
    "dl_l": "dealer_positions_long_all", "dl_s": "dealer_positions_short_all", "dl_sp": "dealer_positions_spread_all",
    "am_l": "asset_mgr_positions_long", "am_s": "asset_mgr_positions_short", "am_sp": "asset_mgr_positions_spread",
    "lv_l": "lev_money_positions_long", "lv_s": "lev_money_positions_short", "lv_sp": "lev_money_positions_spread",
    "ot_l": "other_rept_positions_long", "ot_s": "other_rept_positions_short", "ot_sp": "other_rept_positions_spread",
    "nr_l": "nonrept_positions_long_all", "nr_s": "nonrept_positions_short_all",
}


def fetch_cot(backfill=False):
    msgs = []
    for k, code in COT_MARKETS.items():
        cur = load_jsonl(f"cot_{k}")
        params = {"cftc_contract_market_code": code, "$order": "report_date_as_yyyy_mm_dd ASC", "$limit": "50000"}
        if cur:
            params["$where"] = f"report_date_as_yyyy_mm_dd >= '{(dt.date.fromisoformat(max(cur)) - dt.timedelta(days=21)).isoformat()}'"
        r = get("https://publicreporting.cftc.gov/resource/gpe5-46if.json", params=params)
        r.raise_for_status()
        rows = []
        for x in r.json():
            row = {"d": x["report_date_as_yyyy_mm_dd"][:10]}
            m = re.search(r"\$(\d+)", x.get("contract_units") or "")
            row["cu"] = int(m.group(1)) if m else None       # 契約乘數（美元／指數點）：2023-05-02 起由 $250／$100 改成 $50／$20，口數單位跟著變
            for kk, f in COT_FIELDS.items():
                row[kk] = int(float(x[f]))
            rows.append(row)
        n = append_jsonl(f"cot_{k}", rows)
        msgs.append(f"cot_{k} +{n}")
    return ", ".join(msgs)


# ------------------------------------------------------------------ FINRA 放空餘額

def fetch_si(backfill=False):
    msgs = []
    for sym in ETFS:
        r = _s.post("https://api.finra.org/data/group/otcMarket/name/consolidatedShortInterest",
                    json={"limit": 5000, "compareFilters": [{"compareType": "EQUAL", "fieldName": "symbolCode", "fieldValue": sym}]},
                    headers={"Accept": "application/json"}, timeout=60)
        r.raise_for_status()
        rows = [{"d": x["settlementDate"], "short": x["currentShortPositionQuantity"],
                 "prev": x["previousShortPositionQuantity"], "adv": x["averageDailyVolumeQuantity"],
                 "dtc": x["daysToCoverQuantity"]} for x in r.json()]
        rows.sort(key=lambda x: x["d"])
        n = append_jsonl(f"si_{sym}", rows)
        msgs.append(f"si_{sym} +{n}")
    return ", ".join(msgs)


# ------------------------------------------------------------------ 逐日抓檔的共同骨架

def pending_days(source: str, first: dt.date, last_have: str | None, backfill: bool) -> list[dt.date]:
    """要抓的平日：last_have 之後（回補時從 first 起，扣掉已有與已確認沒資料的日子）。"""
    st = load_state()
    nod = set(st["no_data"].get(source, []))
    end = today_et()
    have = set()
    return [d for d in weekdays(first if (backfill or not last_have) else max(first, dt.date.fromisoformat(last_have) + dt.timedelta(days=1)), end)
            if d.isoformat() not in nod]


def mark_no_data(source: str, days: list[str]) -> None:
    """平日但來源回 403／404／空表（多半是美股休市）：超過 5 天前的才記下來不再重試。"""
    st = load_state()
    nod = set(st["no_data"].get(source, []))
    cutoff = (today_et() - dt.timedelta(days=5)).isoformat()
    nod |= {d for d in days if d < cutoff}
    st["no_data"][source] = sorted(nod)
    save_state(st)


# ------------------------------------------------------------------ FINRA 每日放空量

def _svol_day(d: dt.date):
    url = f"https://cdn.finra.org/equity/regsho/daily/CNMSshvol{d:%Y%m%d}.txt"
    for _ in range(3):
        try:
            r = _s.get(url, timeout=60)
        except requests.RequestException:
            time.sleep(3)
            continue
        if r.status_code in (403, 404):
            return d, None
        if r.status_code != 200:
            time.sleep(3)
            continue
        out = {}
        for line in r.text.splitlines():
            p = line.split("|")
            if len(p) >= 5 and p[1] in ETFS:
                out[p[1]] = {"d": d.isoformat(), "sv": float(p[2]), "sxv": float(p[3]), "tv": float(p[4])}
        return d, out
    raise RuntimeError(f"CNMS {d} 連續失敗")


def fetch_svol(backfill=False):
    last = {s: max(load_jsonl(f"svol_{s}") or [""]) or None for s in ETFS}
    have_last = min(v for v in last.values()) if all(last.values()) else None
    days = pending_days("svol", SVOL_START, have_last, backfill)
    got = {s: [] for s in ETFS}
    nod = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for d, out in ex.map(_svol_day, days):
            if out is None or not out:
                nod.append(d.isoformat())
                continue
            for s, r in out.items():
                got[s].append(r)
    for s in ETFS:
        append_jsonl(f"svol_{s}", got[s])
        if backfill:
            compact(f"svol_{s}")
    mark_no_data("svol", nod)
    return f"svol 檢查 {len(days)} 天，新增 {sum(len(v) for v in got.values())//4} 天（無檔 {len(nod)} 天）"


# ------------------------------------------------------------------ OCC

OCC_URL = ("https://marketdata.theocc.com/volume-query?reportDate={d}&format=csv&volumeQueryType=O&symbolType=U"
           "&symbol={s}&reportType=D&accountType=ALL&productKind=ALL&porc=BOTH")


def _occ_day(sym: str, d: dt.date):
    for _ in range(3):
        try:
            r = _s.get(OCC_URL.format(d=f"{d:%Y%m%d}", s=sym), timeout=60)
        except requests.RequestException:
            time.sleep(3)
            continue
        if r.status_code != 200:
            time.sleep(3)
            continue
        tot: dict[str, int] = {}
        for x in csv.DictReader(io.StringIO(r.text)):
            if not x.get("actype") or x.get("underlying") != sym:
                continue
            k = f"{x['actype'].lower()}_{x['porc'].lower()}"      # c_c = 客戶買權、c_p = 客戶賣權、f_*＝券商自營、m_*＝造市商
            tot[k] = tot.get(k, 0) + int(x["quantity"])
        if not tot:
            return None
        row = {"d": d.isoformat()}
        for a in "cfm":
            for p in "cp":
                row[f"{a}_{p}"] = tot.get(f"{a}_{p}", 0)
        return row
    raise RuntimeError(f"OCC {sym} {d} 連續失敗")


def fetch_occ(backfill=False):
    last = {s: max(load_jsonl(f"occ_{s}") or [""]) or None for s in ETFS}
    have_last = min(v for v in last.values()) if all(last.values()) else None
    days = pending_days("occ", OCC_START, have_last, backfill)
    got = {s: [] for s in ETFS}
    nod = []
    for d in days:
        okday = False
        for s in ETFS:
            row = _occ_day(s, d)
            time.sleep(1.0)       # 規格：每次請求間隔約 1 秒
            if row:
                got[s].append(row)
                okday = True
        if not okday:
            nod.append(d.isoformat())
    for s in ETFS:
        append_jsonl(f"occ_{s}", got[s])
        if backfill:
            compact(f"occ_{s}")
    mark_no_data("occ", nod)
    return f"occ 檢查 {len(days)} 天，新增 {sum(len(v) for v in got.values())//4} 天（無資料 {len(nod)} 天）"


# ------------------------------------------------------------------ Cboe 指數 CSV

def _cboe_csv(name: str, col: str):
    r = get(f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{name}_History.csv", allow_redirects=True)
    r.raise_for_status()
    rows = []
    for x in csv.DictReader(io.StringIO(r.text)):
        m, d, y = x["DATE"].split("/")
        try:
            v = float(x[col])
        except (TypeError, ValueError):
            continue
        rows.append({"d": f"{y}-{int(m):02d}-{int(d):02d}", "v": round(v, 4)})
    if not rows:
        raise RuntimeError(f"{name} 沒有資料")
    rows.sort(key=lambda r: r["d"])
    return rows


def fetch_vol(backfill=False):
    msgs = []
    for name, col, series in (("VIX", "CLOSE", "vix"), ("VXN", "CLOSE", "vxn"), ("SKEW", "SKEW", "skew")):
        n = append_jsonl(series, _cboe_csv(name, col))
        msgs.append(f"{series} +{n}")
    return ", ".join(msgs)


# ------------------------------------------------------------------ Cboe 全市場 put／call

def _pcr_legacy():
    """2006-11 至 2019-10-04：舊 CSV（總計、指數、股票；沒有 ETP 分項）。"""
    out: dict[str, dict] = {}
    for fn, key in (("totalpc", "total"), ("indexpc", "index"), ("equitypc", "equity")):
        r = get(f"https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/{fn}.csv")
        r.raise_for_status()
        lines = r.text.splitlines()
        i = next(k for k, l in enumerate(lines) if l.upper().startswith("DATE"))
        for x in csv.DictReader(io.StringIO("\n".join(lines[i:]))):
            x = {k.strip(): (v or "").strip() for k, v in x.items() if k}
            m, d, y = x["DATE"].split("/")
            call = int(x.get("CALLS") or x.get("CALL")); put = int(x.get("PUTS") or x.get("PUT"))
            iso = f"{y}-{int(m):02d}-{int(d):02d}"
            row = out.setdefault(iso, {"d": iso, "src": "csv"})
            row[key] = round(put / call, 4) if call else None
            if key == "total":
                row["calls"], row["puts"] = call, put
    return sorted(out.values(), key=lambda r: r["d"])


def _pcr_day(d: dt.date):
    url = f"https://cdn.cboe.com/data/us/options/market_statistics/daily/{d:%Y-%m-%d}_daily_options"
    for _ in range(3):
        try:
            r = _s.get(url, timeout=40)
        except requests.RequestException:
            time.sleep(2)
            continue
        if r.status_code in (403, 404):
            return d, None
        if r.status_code != 200:
            time.sleep(2)
            continue
        j = r.json()
        rt = {x["name"]: float(x["value"]) for x in j["ratios"] if x["name"] in
              ("TOTAL PUT/CALL RATIO", "INDEX PUT/CALL RATIO", "EXCHANGE TRADED PRODUCTS PUT/CALL RATIO", "EQUITY PUT/CALL RATIO")}
        vol = next(x for x in j["SUM OF ALL PRODUCTS"] if x["name"] == "VOLUME")
        return d, {"d": d.isoformat(), "src": "json",
                   "total": rt.get("TOTAL PUT/CALL RATIO"), "index": rt.get("INDEX PUT/CALL RATIO"),
                   "etp": rt.get("EXCHANGE TRADED PRODUCTS PUT/CALL RATIO"), "equity": rt.get("EQUITY PUT/CALL RATIO"),
                   "calls": vol["call"], "puts": vol["put"]}
    raise RuntimeError(f"Cboe daily {d} 連續失敗")


def fetch_pcr(backfill=False):
    cur = load_jsonl("pcr")
    msg = ""
    if not any(r.get("src") == "csv" for r in cur.values()):
        n = append_jsonl("pcr", _pcr_legacy())
        msg += f"舊 CSV +{n}；"
    last = max((d for d, r in cur.items() if r.get("src") == "json"), default=None)
    days = pending_days("pcr", PCR_DAILY_START, last, backfill)
    rows, nod = [], []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for d, row in ex.map(_pcr_day, days):
            if row is None:
                nod.append(d.isoformat())
            else:
                rows.append(row)
    n = append_jsonl("pcr", rows)
    if backfill:
        compact("pcr")
    mark_no_data("pcr", nod)
    return f"pcr {msg}每日 JSON 檢查 {len(days)} 天，+{n}（無檔 {len(nod)}）"


# ------------------------------------------------------------------ 發行商份額歷史

def _shares_one(sym: str, backfill: bool) -> str:
    import re
    from etf_dash import flows as fl
    from etf_dash import build_etf_dash as bd
    big = 100000
    cfg = bd.FUND_REGISTRY[sym]
    tier = bd.FLOWS_SOURCE_TIER[sym]
    if tier == "ssga_navhist":
        rows = fl.parse_ssga_navhist_xlsx(fl.fetch_ssga_navhist_xlsx(cfg["yf_ticker"]), big)
    elif tier == "vaneck_navhist":
        url = cfg["holdings_url"].replace("/downloads/holdings/", "/downloads/fundhistoprices/")
        rows = fl.parse_vaneck_navhist_xlsx(fl.fetch_vaneck_navhist_xlsx(url, cfg["holdings_cookies"]), big)
    elif tier == "ishares_navhist":
        pid = re.search(r"/products/(\d+)/", cfg["holdings_page_url"]).group(1)
        rows = fl.parse_ishares_navhist_xml(fl.fetch_ishares_navhist_xml(pid), big)
    elif tier == "invesco_navhist":
        rows = fl.parse_invesco_navhist_json(fl.fetch_invesco_navhist_json(cfg["yf_ticker"]), big)
    else:
        raise RuntimeError(f"{sym}: 未知來源 {tier}")
    out = [{"d": r["date"], "sh": int(r["shares_outstanding"]), "nav": r["nav"]} for r in rows if r.get("shares_outstanding")]
    n = append_jsonl(f"shares_{sym}", out)
    if backfill:
        compact(f"shares_{sym}")
    return f"shares_{sym} +{n}（{out[0]['d']} 起）"


def fetch_shares(backfill=False):
    """沿用 scripts/etf_dash/flows.py 的發行商逐日歷史檔（SSGA／Invesco／VanEck／iShares），不截 200 天。
    etf-dash 自己的 jsonl 只留近 200 天，放空餘額占份額比要回到 2017，所以這裡另存全歷史。
    一檔失敗不擋其他檔；有失敗就在最後丟出例外，讓 log 標 FAIL。"""
    msgs, bad = [], []
    for sym in ETFS:
        try:
            msgs.append(_shares_one(sym, backfill))
        except Exception as e:    # noqa: BLE001
            bad.append(f"{sym}: {type(e).__name__}: {e}")
    if bad:
        raise RuntimeError("；".join(bad) + "｜成功：" + ", ".join(msgs))
    return ", ".join(msgs)


# ------------------------------------------------------------------ ProShares 槓桿 ETF

def fetch_lev(backfill=False):
    msgs = []
    for tk in LEV_PROSHARES:
        r = get(f"https://accounts.profunds.com/etfdata/ByFund/{tk}-historical_nav.csv")
        r.raise_for_status()
        rows = []
        for x in csv.DictReader(io.StringIO(r.text.lstrip("﻿"))):
            try:
                m, d, y = x["Date"].split("/")
                rows.append({"d": f"{y}-{int(m):02d}-{int(d):02d}", "sh": int(float(x["Shares Outstanding (000)"].replace(",", "")) * 1000),
                             "nav": float(x["NAV"].replace(",", ""))})
            except (KeyError, ValueError):
                continue
        rows.sort(key=lambda r: r["d"])
        n = append_jsonl(f"lev_{tk}", rows)
        msgs.append(f"lev_{tk} +{n}")
    return ", ".join(msgs)


# ------------------------------------------------------------------ 內部人買賣（SEC Form 3/4/5 季度資料集）

INSIDER_DIR = DATA / "insider"
SEC_UA = "InvestMQuest Research admin@investmquest.com"
SEC_URLS = [
    "https://www.sec.gov/files/datastandardsinnovation/data/insider-transactions-data-sets/{q}_form345.zip",   # 2026q2 起的新路徑
    "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{q}_form345.zip",
]
INSIDER_FIRST = (2009, 1)


def norm_ticker(t: str) -> str:
    return "".join(c for c in (t if isinstance(t, str) else "").upper() if c.isalnum())


def constituents() -> dict:
    """etf-dash 現有持股名單（今天的成分股）。回傳 {etf: [norm ticker]}，並存一份快照到 data/us_chips/constituents.json。"""
    out = {}
    for e in ETFS:
        j = json.loads((ROOT / "docs" / "etf-dash" / "data" / f"{e}.json").read_text(encoding="utf-8"))
        out[e] = sorted({norm_ticker(c["ticker"]) for c in j["constituents"] if c.get("ticker")})
        asof = j.get("holdings_as_of")
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "constituents.json").write_text(json.dumps({"asof": asof, "etfs": out}, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    return out


def quarters_until(today: dt.date):
    y, q = INSIDER_FIRST
    while dt.date(y, 3 * q - 2, 1) <= today:
        yield f"{y}q{q}"
        q += 1
        if q == 5:
            y, q = y + 1, 1


def quarter_end(qs: str) -> dt.date:
    y, q = int(qs[:4]), int(qs[5])
    m = 3 * q
    return (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1))


def aggregate_zip(path: Path, tickers: set) -> list[dict]:
    """只算公開市場買進（P）與賣出（S）的 Form 4（不含 4/A 更正）。依『交易日所在月份』與代號彙總：
    nb／ns＝該月有買進／賣出的不同申報人數，buy／sell＝成交金額（股數 × 單價，美元；缺單價的列不計金額）。"""
    import zipfile
    import pandas as pd
    with zipfile.ZipFile(path) as z:
        def rd(name, cols):
            with z.open(name) as f:
                return pd.read_csv(f, sep="\t", usecols=cols, dtype=str, low_memory=False, encoding="latin-1")
        sub = rd("SUBMISSION.tsv", ["ACCESSION_NUMBER", "DOCUMENT_TYPE", "ISSUERTRADINGSYMBOL"])
        own = rd("REPORTINGOWNER.tsv", ["ACCESSION_NUMBER", "RPTOWNERCIK"])
        tr = rd("NONDERIV_TRANS.tsv", ["ACCESSION_NUMBER", "TRANS_DATE", "TRANS_CODE", "TRANS_SHARES", "TRANS_PRICEPERSHARE"])
    sub = sub[sub["DOCUMENT_TYPE"] == "4"].copy()
    sub["t"] = sub["ISSUERTRADINGSYMBOL"].map(norm_ticker)
    sub = sub[sub["t"].isin(tickers)][["ACCESSION_NUMBER", "t"]]
    tr = tr[tr["TRANS_CODE"].isin(["P", "S"])].merge(sub, on="ACCESSION_NUMBER")
    if tr.empty:
        return []
    d = pd.to_datetime(tr["TRANS_DATE"], format="%d-%b-%Y", errors="coerce")
    tr = tr.assign(m=d.dt.strftime("%Y-%m"))
    tr = tr[tr["m"].notna()]
    sh = pd.to_numeric(tr["TRANS_SHARES"], errors="coerce")
    px = pd.to_numeric(tr["TRANS_PRICEPERSHARE"], errors="coerce")
    tr["amt"] = sh * px
    # 申報人手誤（單價或股數多打幾個零，2017-08 AMD 一個月算出 2e16 美元）：單價 > 5,000 美元或單筆 > 50 億美元的金額不計；
    # 同一家公司、同一天、同股數同單價的同方向交易只算一筆（母公司與關係企業各自申報同一筆交易的重複列）
    tr["amt"] = tr["amt"].where((tr["amt"] > 0) & (px <= 5000) & (tr["amt"] <= 5e9))
    dup = tr.duplicated(["t", "TRANS_DATE", "TRANS_CODE", "TRANS_SHARES", "TRANS_PRICEPERSHARE"])
    tr["amt"] = tr["amt"].where(~dup)
    rows = []
    owners = tr[["ACCESSION_NUMBER", "t", "m", "TRANS_CODE"]].drop_duplicates().merge(own, on="ACCESSION_NUMBER")
    nown = owners.groupby(["t", "m", "TRANS_CODE"])["RPTOWNERCIK"].nunique()
    amt = tr.groupby(["t", "m", "TRANS_CODE"])["amt"].sum()
    keys = sorted(set(nown.index) | set(amt.index))
    by: dict = {}
    for t, m, c in keys:
        r = by.setdefault((t, m), {"t": t, "m": m, "nb": 0, "ns": 0, "buy": 0.0, "sell": 0.0})
        n = int(nown.get((t, m, c), 0)); a = float(amt.get((t, m, c), 0.0))
        if c == "P":
            r["nb"], r["buy"] = n, round(a, 2)
        else:
            r["ns"], r["sell"] = n, round(a, 2)
    return [by[k] for k in sorted(by)]


def fetch_insider(backfill=False):
    import os
    import tempfile
    cons = constituents()
    tickers = set().union(*cons.values())
    st = load_state()
    done = set(st.get("insider_done", []))
    raw_dir = os.environ.get("US_CHIPS_INSIDER_RAW")        # 本機已有的原始 zip（v7-backtest/data/insider/raw），有就不重抓
    today = today_et()
    INSIDER_DIR.mkdir(parents=True, exist_ok=True)
    msgs, notyet = [], []
    for qs in quarters_until(today):
        if qs in done:
            continue
        zp = Path(raw_dir) / f"{qs}_form345.zip" if raw_dir else None
        tmp = None
        if not (zp and zp.exists()):
            for tmpl in SEC_URLS:
                time.sleep(0.2)
                r = _s.get(tmpl.format(q=qs), headers={"User-Agent": SEC_UA}, timeout=120)
                if r.status_code == 200 and r.content[:2] == b"PK":
                    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
                    tmp.write(r.content); tmp.close()
                    zp = Path(tmp.name)
                    break
            else:
                notyet.append(qs)
                continue
        try:
            rows = aggregate_zip(zp, tickers)
        finally:
            if tmp:
                os.unlink(tmp.name)
        with (INSIDER_DIR / f"{qs}.jsonl").open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
        if quarter_end(qs) < today - dt.timedelta(days=5):
            done.add(qs)
        msgs.append(f"{qs}:{len(rows)}")
    st["insider_done"] = sorted(done)
    save_state(st)
    return f"insider 新處理 {len(msgs)} 季{('（' + ' '.join(msgs[-3:]) + '）') if msgs else ''}；尚未發布 {notyet or '無'}"


SOURCES = {
    "idx": fetch_idx, "cot": fetch_cot, "si": fetch_si, "svol": fetch_svol, "occ": fetch_occ,
    "vol": fetch_vol, "pcr": fetch_pcr, "shares": fetch_shares, "lev": fetch_lev, "insider": fetch_insider,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--backfill", action="store_true")
    a = ap.parse_args()
    names = [x for x in a.only.split(",") if x] or list(SOURCES)
    fails = 0
    for n in names:
        try:
            print(f"OK   {n}: {SOURCES[n](a.backfill)}", flush=True)
        except Exception as e:    # noqa: BLE001  單一來源失敗不拖垮其他來源
            fails += 1
            print(f"FAIL {n}: {type(e).__name__}: {e}", flush=True)
    return 1 if fails >= 3 else 0


if __name__ == "__main__":
    sys.exit(main())
