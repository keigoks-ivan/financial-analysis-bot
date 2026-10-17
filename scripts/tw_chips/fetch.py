#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""台股籌碼趨勢（/tw-chips/）資料抓取：每個資料源一個 fetcher，增量寫進 data/tw_chips/{series}.jsonl。

序列（一天一行，鍵 d＝YYYY-MM-DD；金額一律存來源原單位，換算成億元在 build.py 做）：
    taiex      加權指數 OHLC                      TWSE MI_5MINS_HIST（月查詢）
    turnover   全市場成交金額（元）/成交股數       TWSE FMTQIK（月查詢）
    inst       現貨三大法人買進/賣出金額（元）      TWSE BFI82U（逐日）
    margin     融資融券餘額（張、融資金額仟元）    TWSE MI_MARGN（逐日）
    fut_inst   臺股期貨三大法人未平倉口數          TAIFEX futContractsDateDown（近 3 年）＋ FinMind（2018-06 起，同源轉載）
    opt_inst   臺指選擇權三大法人買賣權未平倉      TAIFEX callsAndPutsDateDown（近 3 年）＋ FinMind（同上）
    pcr        選擇權 Put/Call Ratio              TAIFEX pcRatioDown（月查詢）
    large      臺股期貨大額交易人前五/前十大       TAIFEX largeTraderFutDown（月查詢）
    usdtwd     新台幣兌美元                        FRED DEXTAUS

期交所網站只開放「近 3 年」的三大法人期貨/選擇權日資料；更早的部分用 FinMind 轉載的同一份期交所資料補
（2023-10-16 起與期交所逐筆核對一致，見頁面資料來源說明）。FinMind 最早只到 2018-06-05，
之前沒有可取得的來源，照實留白，不補假資料。

TWSE 頻率限制：請求間隔 ≥ 3 秒；307/403/429/5xx/非 JSON 一律退避重試。
用法：
    python3 scripts/tw_chips/fetch.py                  # 日常：只抓缺的日子
    python3 scripts/tw_chips/fetch.py --backfill       # 回補 10 年（2016-10 起），可續跑
    python3 scripts/tw_chips/fetch.py --only inst,margin --backfill
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import random
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "tw_chips"
START = dt.date(2016, 10, 1)          # 回補起點（約 10 年）
TAIEX_START = dt.date(2015, 10, 1)    # 加權指數多抓 1 年，讓 240 日均線在 2016-10 就有值
FINMIND_START = dt.date(2018, 6, 1)   # FinMind 期貨/選擇權法人資料最早可得日
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
TWSE = "https://www.twse.com.tw/rwd/zh"
TAIFEX = "https://www.taifex.com.tw/cht/3"
TWSE_GAP = 3.2        # 秒；官方限制約 3 次/5 秒，保守取 3.2
TAIFEX_GAP = 1.5
BACKOFF = [20, 60, 180, 300]   # 退避秒數；用完仍失敗就放棄該請求
TZ_TAIPEI = dt.timezone(dt.timedelta(hours=8))

SERIES = ["taiex", "turnover", "inst", "margin", "fut_inst", "opt_inst", "pcr", "large", "usdtwd"]


# ---------------------------------------------------------------- 純解析函式（有單元測試）

def roc_to_iso(s: str) -> str | None:
    """'105/10/03' → '2016-10-03'；格式不符回 None。"""
    m = re.fullmatch(r"\s*(\d{2,3})/(\d{1,2})/(\d{1,2})\s*", s or "")
    if not m:
        return None
    return f"{int(m.group(1)) + 1911:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"


def slash_to_iso(s: str) -> str | None:
    """'2023/10/16' → '2023-10-16'。"""
    m = re.fullmatch(r"\s*(\d{4})/(\d{1,2})/(\d{1,2})\s*", s or "")
    if not m:
        return None
    return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"


def to_num(s):
    """'9,219.52' → 9219.52；'-83,006,510' → -83006510；空白/--/None → None。整數字串回 int。"""
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return s
    t = str(s).strip().replace(",", "")
    if t in ("", "-", "--", "---", "N/A", "X"):
        return None
    try:
        return int(t) if re.fullmatch(r"-?\d+", t) else float(t)
    except ValueError:
        return None


def parse_taiex_month(payload: dict) -> list[dict]:
    """MI_5MINS_HIST 月回應 → [{d,o,h,l,c}]。"""
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return []
    out = []
    for row in payload.get("data") or []:
        d = roc_to_iso(row[0])
        o, h, l, c = (to_num(x) for x in row[1:5])
        if d and None not in (o, h, l, c):
            out.append({"d": d, "o": o, "h": h, "l": l, "c": c})
    return out


def parse_turnover_month(payload: dict) -> list[dict]:
    """FMTQIK 月回應 → [{d, amt（元）, sh（股）}]。"""
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return []
    fields = payload.get("fields") or []
    try:
        i_d, i_amt, i_sh = fields.index("日期"), fields.index("成交金額"), fields.index("成交股數")
    except ValueError:
        return []
    out = []
    for row in payload.get("data") or []:
        d = roc_to_iso(row[i_d])
        amt, sh = to_num(row[i_amt]), to_num(row[i_sh])
        if d and amt is not None:
            out.append({"d": d, "amt": amt, "sh": sh})
    return out


def parse_bfi82u(payload: dict, d: str) -> dict | None:
    """BFI82U 日回應 → {d, f:[買,賣], t:[買,賣], dl:[買,賣]}（元）。

    外資＝「外資及陸資(不含外資自營商)」＋「外資自營商」（新版拆兩列、舊版一列，一律加總）；
    自營商＝自行買賣＋避險。休市／查無資料回 None。
    """
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return None
    acc = {"f": [0, 0], "t": [0, 0], "dl": [0, 0]}
    seen = set()
    for row in payload.get("data") or []:
        name = row[0]
        key = "f" if name.startswith("外資") else "t" if name.startswith("投信") else \
              "dl" if name.startswith("自營商") else None
        if key is None:
            continue
        b, s = to_num(row[1]), to_num(row[2])
        if b is None or s is None:
            return None
        acc[key][0] += b
        acc[key][1] += s
        seen.add(key)
    if seen != {"f", "t", "dl"}:
        return None
    return {"d": d, **acc}


def parse_margn(payload: dict, d: str) -> dict | None:
    """MI_MARGN（selectType=MS）日回應 → 融資/融券張數與融資金額（含前日餘額）。

    mg＝融資餘額（張）、sh＝融券餘額（張）、mga＝融資餘額（仟元）；*_p＝前日餘額（官方註明
    「以前日餘額為準」，隔日才完整揭露）。
    """
    if not isinstance(payload, dict) or payload.get("stat") != "OK":
        return None
    tables = payload.get("tables") or []
    if not tables:
        return None
    rows = {r[0]: r for r in tables[0].get("data") or []}
    def pick(prefix):
        for k, v in rows.items():
            if k.startswith(prefix):
                return v
        return None
    mg, sh, mga = pick("融資(交易單位)"), pick("融券(交易單位)"), pick("融資金額")
    if not (mg and sh and mga):
        return None
    vals = {
        "mg": to_num(mg[5]), "mg_p": to_num(mg[4]),
        "sh": to_num(sh[5]), "sh_p": to_num(sh[4]),
        "mga": to_num(mga[5]), "mga_p": to_num(mga[4]),
    }
    if None in vals.values():
        return None
    return {"d": d, **vals}


def _csv_rows(text: str) -> list[dict]:
    """期交所 CSV（cp950 解碼後）→ dict 列；欄名去空白，濾掉尾端空欄與 HTML 錯誤頁。"""
    if "<html" in text.lower()[:400] or "DateTime" in text[:400]:
        return []
    reader = csv.reader(io.StringIO(text))
    try:
        header = [h.strip() for h in next(reader)]
    except StopIteration:
        return []
    out = []
    for r in reader:
        if not r or not r[0].strip():
            continue
        out.append({h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(header) if h})
    return out


def _inst_key(name: str) -> str | None:
    if name.startswith("外資"):
        return "f"
    if name.startswith("投信"):
        return "t"
    if name.startswith("自營商"):
        return "dl"
    return None


def parse_fut_inst_csv(text: str) -> list[dict]:
    """futContractsDateDown（commodityId=TXF）CSV → [{d, f:[多單OI,空單OI], t:[..], dl:[..]}]（口）。"""
    by_day: dict[str, dict] = {}
    for r in _csv_rows(text):
        if r.get("商品名稱") != "臺股期貨":
            continue
        d, k = slash_to_iso(r["日期"]), _inst_key(r.get("身份別", ""))
        lo, so = to_num(r.get("多方未平倉口數")), to_num(r.get("空方未平倉口數"))
        if d and k and lo is not None and so is not None:
            by_day.setdefault(d, {"d": d})[k] = [lo, so]
    return [v for _, v in sorted(by_day.items()) if {"f", "t", "dl"} <= set(v)]


def parse_opt_inst_csv(text: str) -> list[dict]:
    """callsAndPutsDateDown（commodityId=TXO）CSV →
    [{d, c:{f:[多單OI口,空單OI口,多單OI金額千元,空單OI金額千元],t:..,dl:..}, p:{...}}]。"""
    by_day: dict[str, dict] = {}
    for r in _csv_rows(text):
        if r.get("商品名稱") != "臺指選擇權":
            continue
        d, k = slash_to_iso(r["日期"]), _inst_key(r.get("身份別", ""))
        cp = {"CALL": "c", "PUT": "p"}.get(r.get("買賣權別", "").upper())
        vals = [to_num(r.get(x)) for x in ("買方未平倉口數", "賣方未平倉口數",
                                           "買方未平倉契約金額(千元)", "賣方未平倉契約金額(千元)")]
        if d and k and cp and None not in vals:
            by_day.setdefault(d, {"d": d, "c": {}, "p": {}})[cp][k] = vals
    return [v for _, v in sorted(by_day.items())
            if all({"f", "t", "dl"} <= set(v[s]) for s in ("c", "p"))]


def parse_pcr_csv(text: str) -> list[dict]:
    """pcRatioDown CSV → [{d, pv, cv, vr（成交量比%）, po, co, or_（未平倉比%）}]。"""
    out = []
    for r in _csv_rows(text):
        d = slash_to_iso(r.get("日期", ""))
        pv, cv = to_num(r.get("賣權成交量")), to_num(r.get("買權成交量"))
        po, co = to_num(r.get("賣權未平倉量")), to_num(r.get("買權未平倉量"))
        vr, orr = to_num(r.get("買賣權成交量比率%")), to_num(r.get("買賣權未平倉量比率%"))
        if d and None not in (pv, cv, po, co, vr, orr):
            out.append({"d": d, "pv": pv, "cv": cv, "vr": vr, "po": po, "co": co, "or": orr})
    return sorted(out, key=lambda x: x["d"])


def parse_large_csv(text: str) -> list[dict]:
    """largeTraderFutDown CSV → 臺股期貨（代號 TX、到期月份 999999＝全部月份）：
    [{d, a:[前五大買,前五大賣,前十大買,前十大賣]（全部交易人）, s:[同上]（特定法人）, oi}]。"""
    by_day: dict[str, dict] = {}
    for r in _csv_rows(text):
        if r.get("商品(契約)", "").strip() != "TX" or r.get("到期月份(週別)", "").strip() != "999999":
            continue
        d = slash_to_iso(r["日期"])
        typ = r.get("交易人類別", "").strip()
        vals = [to_num(r.get(x)) for x in ("前五大交易人買方", "前五大交易人賣方",
                                           "前十大交易人買方", "前十大交易人賣方")]
        oi = to_num(r.get("全市場未沖銷部位數"))
        if not d or typ not in ("0", "1") or None in vals or oi is None:
            continue
        rec = by_day.setdefault(d, {"d": d})
        rec["a" if typ == "0" else "s"] = vals
        rec["oi"] = oi
    return [v for _, v in sorted(by_day.items()) if "a" in v and "s" in v]


def parse_fred_csv(text: str) -> list[dict]:
    """FRED fredgraph.csv → [{d, v}]；'.' 為缺值。"""
    out = []
    for i, line in enumerate(text.splitlines()):
        if i == 0 or "," not in line:
            continue
        d, v = line.split(",", 1)
        v = to_num(v.strip())
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) and v is not None:
            out.append({"d": d, "v": v})
    return out


def finmind_fut_rows(data: list[dict]) -> list[dict]:
    """FinMind TaiwanFuturesInstitutionalInvestors（futures_id=TX）→ 同 parse_fut_inst_csv 結構。"""
    m = {"外資": "f", "外資及陸資": "f", "投信": "t", "自營商": "dl"}
    by_day: dict[str, dict] = {}
    for r in data:
        k = m.get(r.get("institutional_investors"))
        if k and r.get("futures_id") == "TX":
            by_day.setdefault(r["date"], {"d": r["date"]})[k] = [
                r["long_open_interest_balance_volume"], r["short_open_interest_balance_volume"]]
    return [v for _, v in sorted(by_day.items()) if {"f", "t", "dl"} <= set(v)]


def finmind_opt_rows(data: list[dict]) -> list[dict]:
    """FinMind TaiwanOptionInstitutionalInvestors（option_id=TXO）→ 同 parse_opt_inst_csv 結構。"""
    m = {"外資": "f", "外資及陸資": "f", "投信": "t", "自營商": "dl"}
    cp_m = {"買權": "c", "賣權": "p"}
    by_day: dict[str, dict] = {}
    for r in data:
        k, cp = m.get(r.get("institutional_investors")), cp_m.get(r.get("call_put"))
        if k and cp and r.get("option_id") == "TXO":
            by_day.setdefault(r["date"], {"d": r["date"], "c": {}, "p": {}})[cp][k] = [
                r["long_open_interest_balance_volume"], r["short_open_interest_balance_volume"],
                r["long_open_interest_balance_amount"], r["short_open_interest_balance_amount"]]
    return [v for _, v in sorted(by_day.items())
            if all({"f", "t", "dl"} <= set(v[s]) for s in ("c", "p"))]


# ---------------------------------------------------------------- 存檔

class Store:
    """data/tw_chips/{name}.jsonl：一天一行，鍵 d；同日以後寫入者為準（讀入時覆蓋）。"""

    def __init__(self, name: str):
        self.name = name
        self.path = DATA / f"{name}.jsonl"
        self.rows: dict[str, dict] = {}
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    self.rows[r["d"]] = r

    def has(self, d: str) -> bool:
        return d in self.rows

    def add(self, row: dict) -> bool:
        """同日內容沒變就不寫；有新或有改才 append 一行。"""
        old = self.rows.get(row["d"])
        if old == row:
            return False
        DATA.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
        self.rows[row["d"]] = row
        return True

    def dates(self) -> list[str]:
        return sorted(self.rows)

    def last(self) -> str | None:
        return max(self.rows) if self.rows else None

    def compact(self):
        """重寫成依日期排序、每日一行（回補完成後整理用）。"""
        with self.path.open("w", encoding="utf-8") as f:
            for d in sorted(self.rows):
                f.write(json.dumps(self.rows[d], ensure_ascii=False, separators=(",", ":")) + "\n")


class State:
    """data/tw_chips/_state.json：months_done（已抓完的整月）與 gaps（逐日查無資料的嘗試次數）。"""

    def __init__(self):
        self.path = DATA / "_state.json"
        self.d = {"months_done": {}, "gaps": {}}
        if self.path.exists():
            self.d.update(json.loads(self.path.read_text(encoding="utf-8")))

    def save(self):
        DATA.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.d, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                             encoding="utf-8")

    def month_done(self, series: str, ym: str) -> bool:
        return ym in self.d["months_done"].get(series, [])

    def mark_month(self, series: str, ym: str):
        lst = self.d["months_done"].setdefault(series, [])
        if ym not in lst:
            lst.append(ym)
            lst.sort()

    def gap_attempts(self, series: str, d: str) -> int:
        return self.d["gaps"].get(series, {}).get(d, 0)

    def bump_gap(self, series: str, d: str):
        g = self.d["gaps"].setdefault(series, {})
        g[d] = g.get(d, 0) + 1


# ---------------------------------------------------------------- HTTP

class Throttle:
    def __init__(self, gap: float):
        self.gap, self.last = gap, 0.0

    def wait(self):
        dtm = time.monotonic() - self.last
        if dtm < self.gap:
            time.sleep(self.gap - dtm + random.uniform(0, 0.4))
        self.last = time.monotonic()


_twse_throttle = Throttle(TWSE_GAP)
_taifex_throttle = Throttle(TAIFEX_GAP)
_session = requests.Session()
_session.headers.update(UA)


class Blocked(Exception):
    pass


def twse_json(path: str, params: dict) -> dict:
    """打 TWSE rwd 端點；307/403/429/5xx、非 JSON、空回應一律退避重試，用完拋 Blocked。
    『查無資料』(stat 非 OK) 是正常回應，直接回傳給呼叫端判斷。"""
    last_err = ""
    for wait in [0] + BACKOFF:
        if wait:
            log(f"  退避 {wait}s（{last_err}）")
            time.sleep(wait)
        _twse_throttle.wait()
        try:
            r = _session.get(f"{TWSE}/{path}", params={**params, "response": "json"},
                             timeout=30, allow_redirects=False)
        except requests.RequestException as e:
            last_err = f"{type(e).__name__}"
            continue
        if r.status_code in (307, 302, 403, 429) or r.status_code >= 500:
            last_err = f"HTTP {r.status_code}"
            continue
        try:
            j = r.json()
        except ValueError:
            last_err = "非 JSON/空回應"
            continue
        if not isinstance(j, dict) or "stat" not in j:
            last_err = "缺 stat"
            continue
        return j
    raise Blocked(f"TWSE {path} {params} 重試用盡：{last_err}")


def taifex_post(endpoint: str, data: dict) -> str:
    last_err = ""
    for wait in [0, 10, 30, 90]:
        if wait:
            time.sleep(wait)
        _taifex_throttle.wait()
        try:
            r = _session.post(f"{TAIFEX}/{endpoint}", data=data, timeout=120)
        except requests.RequestException as e:
            last_err = type(e).__name__
            continue
        if r.status_code != 200:
            last_err = f"HTTP {r.status_code}"
            continue
        return r.content.decode("cp950", errors="replace")
    raise Blocked(f"TAIFEX {endpoint} {data} 重試用盡：{last_err}")


def log(msg: str):
    print(msg, flush=True)


# ---------------------------------------------------------------- 日期工具

def today_tpe() -> dt.date:
    return dt.datetime.now(TZ_TAIPEI).date()


def month_starts(a: dt.date, b: dt.date):
    y, m = a.year, a.month
    while (y, m) <= (b.year, b.month):
        yield dt.date(y, m, 1)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def month_end(d: dt.date) -> dt.date:
    return (dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1) - dt.timedelta(days=1))


# ---------------------------------------------------------------- fetchers

def fetch_taiex_turnover(st: State, start: dt.date, today: dt.date):
    """加權指數 OHLC＋成交金額，月查詢。已抓完的整月不重抓；當月永遠重抓（會更新到最新一天）。"""
    taiex, turn = Store("taiex"), Store("turnover")
    n_new = 0
    for ms in month_starts(start, today):
        ym = ms.strftime("%Y-%m")
        complete = month_end(ms) < today
        if complete and st.month_done("taiex", ym) and st.month_done("turnover", ym):
            continue
        d1 = ms.strftime("%Y%m01")
        a = parse_taiex_month(twse_json("TAIEX/MI_5MINS_HIST", {"date": d1}))
        b = parse_turnover_month(twse_json("afterTrading/FMTQIK", {"date": d1}))
        for r in a:
            n_new += taiex.add(r)
        for r in b:
            n_new += turn.add(r)
        if complete and a and b:
            st.mark_month("taiex", ym)
            st.mark_month("turnover", ym)
        if complete and not (a and b):
            # 整月無資料（例如超出歷史範圍）：記為已查，避免每天重抓
            st.mark_month("taiex", ym)
            st.mark_month("turnover", ym)
        st.save()
    log(f"taiex/turnover：新增/更新 {n_new} 筆；taiex 至 {taiex.last()}，turnover 至 {turn.last()}")


def missing_trading_days(store: Store, series: str, st: State, start: dt.date, today: dt.date,
                         recent_only_days: int | None) -> list[str]:
    cal = Store("taiex").dates()
    lo = start.isoformat()
    if recent_only_days is not None:
        lo = max(lo, (today - dt.timedelta(days=recent_only_days)).isoformat())
    out = []
    for d in cal:
        if d < lo or d > today.isoformat() or store.has(d):
            continue
        age = (today - dt.date.fromisoformat(d)).days
        if st.gap_attempts(series, d) >= 3 and age > 5:
            continue          # 多次查無資料且已非近期：視為該日無此資料，不再重抓
        out.append(d)
    return out


def fetch_daily_twse(which: list[str], st: State, start: dt.date, today: dt.date,
                     backfill: bool, limit: int | None):
    """逐日抓 inst / margin；最新日優先，這樣回補中途頁面也已有近期資料。"""
    stores = {"inst": Store("inst"), "margin": Store("margin")}
    todo = {s: missing_trading_days(stores[s], s, st, start, today, None if backfill else 45) for s in which}
    for s in which:
        log(f"{s}：待抓 {len(todo[s])} 天")
    all_dates = sorted(set(d for s in which for d in todo[s]), reverse=True)
    if limit:
        all_dates = all_dates[:limit]
    fails = 0
    n = 0
    for d in all_dates:
        d8 = d.replace("-", "")
        for s in which:
            if d not in todo[s]:
                continue
            try:
                if s == "inst":
                    row = parse_bfi82u(twse_json("fund/BFI82U", {"type": "day", "dayDate": d8}), d)
                else:
                    row = parse_margn(twse_json("marginTrading/MI_MARGN", {"date": d8, "selectType": "MS"}), d)
            except Blocked as e:
                fails += 1
                log(f"FAIL {s} {d}：{e}")
                if fails >= 3:
                    log("連續失敗 3 次，停止本輪（下次續跑）。")
                    st.save()
                    return
                continue
            fails = 0
            if row is None:
                st.bump_gap(s, d)
                log(f"  {s} {d} 查無資料（第 {st.gap_attempts(s, d)} 次）")
            else:
                stores[s].add(row)
                n += 1
        if n and n % 50 == 0:
            st.save()
            log(f"  ...已抓 {n} 筆，目前到 {d}")
    st.save()
    log(f"inst/margin：本輪新增 {n} 筆")


def _taifex_window(today: dt.date) -> dt.date:
    """期交所網站只提供近 3 年，起點取 3 年前＋1 天。"""
    try:
        return today.replace(year=today.year - 3) + dt.timedelta(days=1)
    except ValueError:      # 2/29
        return today.replace(year=today.year - 3, day=28) + dt.timedelta(days=1)


def _chunks(a: dt.date, b: dt.date, days: int):
    cur = a
    while cur <= b:
        end = min(cur + dt.timedelta(days=days - 1), b)
        yield cur, end
        cur = end + dt.timedelta(days=1)


def _fmt(d: dt.date) -> str:
    return d.strftime("%Y/%m/%d")


def fetch_range_csv(name: str, endpoint: str, extra: dict, parser, start: dt.date, today: dt.date,
                    chunk_days: int, floor: dt.date | None = None):
    """通用：依區間分段 POST 下載 CSV → parser → Store。從 max(start, floor, 最後一筆日期) 開始。"""
    store = Store(name)
    a = max(start, floor or start)
    # 日常模式：從已有最後日往前多抓 3 天（涵蓋修正與休市日），回補模式：缺口由 start 起掃
    if store.last() and not os.environ.get("TWCHIPS_FULL_SCAN"):
        a = max(a, dt.date.fromisoformat(store.last()) - dt.timedelta(days=3))
    n = 0
    for c0, c1 in _chunks(a, today, chunk_days):
        # 迄日若超過期交所當天已公布的最後一日會整段被拒（DateTime error）：最後一段往前退幾天再試
        for back in range(0, 5 if c1 == today else 1):
            e = c1 - dt.timedelta(days=back)
            if e < c0:
                break
            text = taifex_post(endpoint, {"queryStartDate": _fmt(c0), "queryEndDate": _fmt(e), **extra})
            rows = parser(text)
            if rows:
                for r in rows:
                    n += store.add(r)
                break
    log(f"{name}：新增/更新 {n} 筆；最早 {min(store.rows) if store.rows else None}，最新 {store.last()}")


def fetch_finmind_backfill(name: str, dataset: str, id_key: str, id_val: str, conv,
                           until: dt.date):
    """FinMind 補期交所網站 3 年窗口以外的舊資料（2018-06-05 起）；只補還沒有的日子。"""
    store = Store(name)
    if store.rows and min(store.rows) <= "2018-06-06":
        return          # 已補過
    end = until - dt.timedelta(days=1)
    if end < FINMIND_START:
        return
    r = _session.get("https://api.finmindtrade.com/api/v4/data",
                     params={"dataset": dataset, "start_date": FINMIND_START.isoformat(),
                             "end_date": end.isoformat(), id_key: id_val}, timeout=180)
    r.raise_for_status()
    data = r.json().get("data") or []
    n = 0
    for row in conv(data):
        if not store.has(row["d"]):
            n += store.add(row)
    log(f"{name}（FinMind 補舊資料）：新增 {n} 筆，最早 {min(store.rows) if store.rows else None}")


def fetch_fut_inst(start, today, backfill):
    win = _taifex_window(today)
    fetch_range_csv("fut_inst", "futContractsDateDown", {"commodityId": "TXF"}, parse_fut_inst_csv,
                    max(start, win), today, 360, floor=win)
    if backfill:
        s = Store("fut_inst")
        first_taifex = min([d for d in s.rows if d >= win.isoformat()] or [today.isoformat()])
        fetch_finmind_backfill("fut_inst", "TaiwanFuturesInstitutionalInvestors", "data_id", "TX",
                               finmind_fut_rows, dt.date.fromisoformat(first_taifex))


def fetch_opt_inst(start, today, backfill):
    win = _taifex_window(today)
    fetch_range_csv("opt_inst", "callsAndPutsDateDown", {"commodityId": "TXO"}, parse_opt_inst_csv,
                    max(start, win), today, 360, floor=win)
    if backfill:
        s = Store("opt_inst")
        first_taifex = min([d for d in s.rows if d >= win.isoformat()] or [today.isoformat()])
        fetch_finmind_backfill("opt_inst", "TaiwanOptionInstitutionalInvestors", "data_id", "TXO",
                               finmind_opt_rows, dt.date.fromisoformat(first_taifex))


def fetch_pcr(start, today, backfill):
    fetch_range_csv("pcr", "pcRatioDown", {}, parse_pcr_csv, start, today, 28)


def fetch_large(start, today, backfill):
    fetch_range_csv("large", "largeTraderFutDown", {}, parse_large_csv, start, today, 28)


def fetch_usdtwd(start, today, backfill):
    store = Store("usdtwd")
    r = None
    for attempt in range(4):      # FRED 偶爾慢，讀取逾時就重試
        try:
            # FRED 對瀏覽器 UA 會逾時，用 requests 預設 UA
            r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv", params={"id": "DEXTAUS"}, timeout=90)
            r.raise_for_status()
            break
        except requests.RequestException as e:
            log(f"  FRED 第 {attempt + 1} 次失敗：{type(e).__name__}")
            time.sleep(10 * (attempt + 1))
    else:
        raise Blocked("FRED DEXTAUS 重試用盡")
    n = 0
    for row in parse_fred_csv(r.text):
        if row["d"] >= start.isoformat():
            n += store.add(row)
    log(f"usdtwd：新增/更新 {n} 筆；最新 {store.last()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backfill", action="store_true", help="回補 10 年（2016-10 起），可續跑")
    ap.add_argument("--only", default="", help="逗號分隔：" + ",".join(SERIES))
    ap.add_argument("--limit", type=int, default=0, help="逐日 TWSE 序列最多抓幾天（測試用）")
    args = ap.parse_args()

    only = [s for s in args.only.split(",") if s] or SERIES
    unknown = set(only) - set(SERIES)
    if unknown:
        sys.exit(f"未知序列：{unknown}")
    today = today_tpe()
    start = START
    st = State()
    failed = []

    def run(label, fn, *a):
        try:
            fn(*a)
        except Blocked as e:
            failed.append(label)
            log(f"FAIL {label}：{e}")
        except Exception as e:   # 單一序列失敗不影響其他序列
            failed.append(label)
            log(f"FAIL {label}：{type(e).__name__}: {e}")

    if {"taiex", "turnover"} & set(only) or {"inst", "margin"} & set(only):
        run("taiex/turnover", fetch_taiex_turnover, st, TAIEX_START, today)
    daily = [s for s in ("inst", "margin") if s in only]
    if daily:
        run("inst/margin", fetch_daily_twse, daily, st, start, today, args.backfill, args.limit or None)
    if "fut_inst" in only:
        run("fut_inst", fetch_fut_inst, start, today, args.backfill)
    if "opt_inst" in only:
        run("opt_inst", fetch_opt_inst, start, today, args.backfill)
    if "pcr" in only:
        run("pcr", fetch_pcr, start, today, args.backfill)
    if "large" in only:
        run("large", fetch_large, start, today, args.backfill)
    if "usdtwd" in only:
        run("usdtwd", fetch_usdtwd, start, today, args.backfill)

    if args.backfill:       # 回補完整理檔案：依日期排序、每日一行
        for s in only:
            if (DATA / f"{s}.jsonl").exists():
                Store(s).compact()
    log("完成。" + (f" 失敗：{failed}" if failed else ""))
    if len(failed) >= 3:
        sys.exit(1)


if __name__ == "__main__":
    main()
