#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""韓股籌碼趨勢（/kr-chips/）資料抓取：每個資料源一個 fetcher，增量寫進 data/kr_chips/{series}.jsonl。

序列（一天一行，鍵 d＝YYYY-MM-DD；金額一律存來源原單位，換算成億韓元在 build.py 做）：
    kospi        KOSPI 收盤、成交量、成交金額、上市總市值、外資持股市值與比重   KOFIA FreeSIS STATSCU0100000020BO
    kosdaq       KOSDAQ 同上                                                    KOFIA FreeSIS STATSCU0100000030BO
    deposit      投資人預託金、未收款（미수금）、反向交易（반대매매）            KOFIA FreeSIS STATSCU0100000060BO
    credit       信用交易融資餘額（合計／KOSPI／KOSDAQ）與融券（대주）            KOFIA FreeSIS STATSCU0100000070BO
    lend         借券餘額（대차잔고，全市場合計；股數與金額）                    KOFIA FreeSIS STATSCU0100000180BO（逐日，取「合計」列）
    inst_kospi   KOSPI 外國人／機構／個人買賣超（億韓元）                         Naver 行動版 API index/KOSPI/trend（逐日）
    inst_kosdaq  KOSDAQ 同上                                                    Naver 行動版 API index/KOSDAQ/trend（逐日）
    px_kospi     KOSPI 日 OHLC                                                  Naver 行動版 API index/KOSPI/price
    px_kosdaq    KOSDAQ 日 OHLC                                                 Naver 行動版 API index/KOSDAQ/price
    usdkrw       韓元兌美元                                                      FRED DEXKOUS

需要韓國交易所（KRX）帳號才拿得到的放空、期貨選擇權投資人別、VKOSPI 不在範圍內。

用法：
    python3 scripts/kr_chips/fetch.py                  # 日常：只抓缺的日子
    python3 scripts/kr_chips/fetch.py --backfill       # 回補全歷史，可續跑
    python3 scripts/kr_chips/fetch.py --only inst_kospi,inst_kosdaq --backfill
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "kr_chips"

KOFIA_URL = "https://freesis.kofia.or.kr/meta/getMetaDataList.do"
NAVER = "https://m.stock.naver.com/api/index"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
KOFIA_HEAD = {**UA, "Content-Type": "application/json; charset=UTF-8",
              "Referer": "https://freesis.kofia.or.kr/stat/FreeSIS.do?parentDivId=MSIS10000000000000&serviceId=STATSCU0100000060"}
KOFIA_GAP = 0.2
NAVER_GAP = 0.15
BACKOFF = [10, 30, 90, 180]
TZ_SEOUL = dt.timezone(dt.timedelta(hours=9))
TZ_TAIPEI = dt.timezone(dt.timedelta(hours=8))

LEND_START = "2009-01-02"      # KOFIA 借券逐檔資料最早有值的年份（2008 年及以前回傳 0 列）
INST_START = "2005-01-03"      # Naver 投資人別買賣超最早有值日（之前一律回 0）
SERIES = ["kospi", "kosdaq", "px_kospi", "px_kosdaq", "deposit", "credit", "usdkrw",
          "lend", "inst_kospi", "inst_kosdaq"]


# ---------------------------------------------------------------- 純解析函式（有單元測試）

def ymd_to_iso(s) -> str | None:
    """'20261015' → '2026-10-15'；格式不符回 None。"""
    m = re.fullmatch(r"(\d{4})(\d{2})(\d{2})", str(s or ""))
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def num(s):
    """'5,554.22' → 5554.22；'+13,967' → 13967；'-37,637' → -37637；空白、None → None。"""
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return s
    t = str(s).strip().replace(",", "").replace("+", "")
    if t in ("", "-", "--"):
        return None
    try:
        return int(t) if re.fullmatch(r"-?\d+", t) else float(t)
    except ValueError:
        return None


def parse_kofia_index(rows: list[dict]) -> list[dict]:
    """STATSCU0100000020BO／030BO → [{d, c, vol, amt, mcap, fmcap, fpct}]。
    c＝收盤指數；vol＝成交量（股）；amt＝成交金額（百萬韓元）；mcap＝上市總市值（百萬韓元）；
    fmcap＝外國人持股市值（百萬韓元）；fpct＝外國人持股比重（%）。收盤為 0 的列丟棄。"""
    out = []
    for r in rows or []:
        d = ymd_to_iso(r.get("TMPV1"))
        c = num(r.get("TMPV2"))
        if d and c:
            out.append({"d": d, "c": c, "vol": num(r.get("TMPV3")), "amt": num(r.get("TMPV4")),
                        "mcap": num(r.get("TMPV5")), "fmcap": num(r.get("TMPV6")), "fpct": num(r.get("TMPV7"))})
    return out


def parse_kofia_deposit(rows: list[dict]) -> list[dict]:
    """STATSCU0100000060BO → [{d, dep, x3, x4, unpaid, forced, forced_pct}]。
    dep＝投資人預託金；unpaid＝委託買賣未收款（위탁매매 미수금）；forced＝反向交易金額（반대매매，隔日強制賣出）；
    forced_pct＝反向交易金額 ÷ 前一日未收款（%）；金額單位百萬韓元。
    x3、x4 兩欄（推定為衍生品保證金與 RP 賣出餘額）標籤未核對，只存檔、頁面不用。"""
    out = []
    for r in rows or []:
        d = ymd_to_iso(r.get("TMPV1"))
        dep = num(r.get("TMPV2"))
        if d and dep:
            out.append({"d": d, "dep": dep, "x3": num(r.get("TMPV3")), "x4": num(r.get("TMPV4")),
                        "unpaid": num(r.get("TMPV5")), "forced": num(r.get("TMPV6")),
                        "forced_pct": num(r.get("TMPV7"))})
    return out


def parse_kofia_credit(rows: list[dict]) -> list[dict]:
    """STATSCU0100000070BO → [{d, tot, kospi, kosdaq, sh_tot, sh_kospi, sh_kosdaq, x8, x9}]。
    tot／kospi／kosdaq＝信用交易融資餘額（合計、有價證券市場、KOSDAQ）；sh_*＝信用交易融券（대주）餘額；單位百萬韓元。
    x8、x9 標籤未核對，只存檔。早期（融資合計為 0）的列丟棄。"""
    out = []
    for r in rows or []:
        d = ymd_to_iso(r.get("TMPV1"))
        tot = num(r.get("TMPV2"))
        if d and tot:
            out.append({"d": d, "tot": tot, "kospi": num(r.get("TMPV3")), "kosdaq": num(r.get("TMPV4")),
                        "sh_tot": num(r.get("TMPV5")), "sh_kospi": num(r.get("TMPV6")),
                        "sh_kosdaq": num(r.get("TMPV7")), "x8": num(r.get("TMPV8")), "x9": num(r.get("TMPV9"))})
    return out


def parse_kofia_lend_total(rows: list[dict], d: str) -> dict | None:
    """STATSCU0100000180BO 單日回應 → {d, new, ret, bal, bal_amt}（取名稱為「합계」的那一列）。
    new＝當日新增借券（股）；ret＝當日還券（股）；bal＝借券餘額（股）；bal_amt＝借券餘額金額（百萬韓元）。
    沒有合計列或餘額為 0（休市／無資料）回 None。"""
    for r in rows or []:
        if r.get("TMPV1") == "합계" and r.get("TMPV2") == "-":
            bal = num(r.get("TMPV5"))
            if not bal:
                return None
            return {"d": d, "new": num(r.get("TMPV3")), "ret": num(r.get("TMPV4")),
                    "bal": bal, "bal_amt": num(r.get("TMPV6"))}
    return None


def parse_naver_trend(j: dict, d: str) -> dict | None:
    """Naver index/{KOSPI|KOSDAQ}/trend?bizdate= → {d, p, f, i}（億韓元，買超為正）。
    三項全為 0 視為休市或尚未公布，回 None。bizdate 與請求日不同也回 None。"""
    if not isinstance(j, dict) or j.get("bizdate") != d.replace("-", ""):
        return None
    p, f, i = num(j.get("personalValue")), num(j.get("foreignValue")), num(j.get("institutionalValue"))
    if None in (p, f, i) or (p == 0 and f == 0 and i == 0):
        return None
    return {"d": d, "p": p, "f": f, "i": i}


def parse_naver_price(rows: list[dict]) -> list[dict]:
    """Naver index/{code}/price → [{d, o, h, l, c}]。"""
    out = []
    for r in rows or []:
        d = r.get("localTradedAt")
        o, h, l, c = (num(r.get(k)) for k in ("openPrice", "highPrice", "lowPrice", "closePrice"))
        if d and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d) and None not in (o, h, l, c):
            out.append({"d": d, "o": o, "h": h, "l": l, "c": c})
    return out


def parse_fred_csv(text: str) -> list[dict]:
    """FRED fredgraph.csv（observation_date,DEXKOUS）→ [{d, v}]；'.' 或空白略過。"""
    out = []
    for line in text.splitlines()[1:]:
        parts = line.strip().split(",")
        if len(parts) >= 2 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", parts[0]):
            v = num(parts[1])
            if v is not None:
                out.append({"d": parts[0], "v": v})
    return out


# ---------------------------------------------------------------- 存檔

class Store:
    """data/kr_chips/{name}.jsonl：一天一行，鍵 d；同日以後寫入者為準（讀入時覆蓋）。"""

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
        if self.rows.get(row["d"]) == row:
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
    """data/kr_chips/_state.json：gaps＝逐日查無資料的嘗試次數。"""

    def __init__(self):
        self.path = DATA / "_state.json"
        self.d = {"gaps": {}}
        self.touched: set[str] = set()
        if self.path.exists():
            self.d.update(json.loads(self.path.read_text(encoding="utf-8")))

    def save(self):
        """多個程序同時回補不同序列時，只覆蓋自己動過的序列，不蓋掉別人剛寫的。"""
        DATA.mkdir(parents=True, exist_ok=True)
        if self.path.exists() and self.touched:
            disk = json.loads(self.path.read_text(encoding="utf-8"))
            merged = dict(disk.get("gaps", {}))
            for s in self.touched:
                merged[s] = self.d["gaps"].get(s, {})
            self.d["gaps"] = merged
        self.path.write_text(json.dumps(self.d, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                             encoding="utf-8")

    def gap_attempts(self, series: str, d: str) -> int:
        return self.d["gaps"].get(series, {}).get(d, 0)

    def bump_gap(self, series: str, d: str):
        self.touched.add(series)
        g = self.d["gaps"].setdefault(series, {})
        g[d] = g.get(d, 0) + 1


# ---------------------------------------------------------------- HTTP

class Throttle:
    def __init__(self, gap: float):
        self.gap, self.last = gap, 0.0

    def wait(self):
        dtm = time.monotonic() - self.last
        if dtm < self.gap:
            time.sleep(self.gap - dtm + random.uniform(0, 0.1))
        self.last = time.monotonic()


class Blocked(Exception):
    pass


_kofia_throttle = Throttle(KOFIA_GAP)
_naver_throttle = Throttle(NAVER_GAP)
_session = requests.Session()
_session.headers.update(UA)


def log(msg: str):
    print(msg, flush=True)


def _get_json(label: str, throttle: Throttle, send, ok) -> object:
    """共用重試：連線錯誤、非 200、非 JSON、ok(j) 為假都退避重試，用完拋 Blocked。"""
    last_err = ""
    for wait in [0] + BACKOFF:
        if wait:
            log(f"  退避 {wait}s（{last_err}）")
            time.sleep(wait)
        throttle.wait()
        try:
            r = send()
        except requests.RequestException as e:
            last_err = type(e).__name__
            continue
        if r.status_code != 200:
            last_err = f"HTTP {r.status_code}"
            continue
        try:
            j = r.json()
        except ValueError:
            last_err = "非 JSON（來源回了錯誤頁）"
            continue
        if not ok(j):
            last_err = "回應格式不符"
            continue
        return j
    raise Blocked(f"{label} 重試用盡：{last_err}")


def kofia(obj: str, d1: str, d2: str) -> list[dict]:
    """KOFIA FreeSIS：日期區間 d1～d2（YYYYMMDD），回 ds1 列表。"""
    body = {"dmSearch": {"tmpV40": "1000000", "tmpV41": "1", "tmpV1": "D",
                         "tmpV45": d1, "tmpV46": d2, "OBJ_NM": obj}}
    j = _get_json(f"KOFIA {obj} {d1}-{d2}", _kofia_throttle,
                  lambda: _session.post(KOFIA_URL, headers=KOFIA_HEAD, data=json.dumps(body), timeout=60),
                  lambda j: isinstance(j, dict) and isinstance(j.get("ds1"), list))
    return j["ds1"]


def naver(path: str, params: dict | None = None):
    return _get_json(f"Naver {path} {params}", _naver_throttle,
                     lambda: _session.get(f"{NAVER}/{path}", params=params, timeout=30),
                     lambda j: isinstance(j, (dict, list)))


# ---------------------------------------------------------------- 日期工具

def today_seoul() -> dt.date:
    return dt.datetime.now(TZ_SEOUL).date()


def ymd(d: str) -> str:
    return d.replace("-", "")


def calendar() -> list[str]:
    """交易日曆＝KOFIA KOSPI 有收盤的日子 ∪ Naver KOSPI 有 OHLC 的日子（Naver 當天就有，KOFIA 約晚一個交易日）。"""
    return sorted(set(Store("kospi").rows) | set(Store("px_kospi").rows))


# ---------------------------------------------------------------- fetchers

def fetch_kofia_bulk(name: str, obj: str, parser, backfill: bool):
    """KOFIA 區間序列：一次請求拉整段。日常只重抓最近 40 天（涵蓋 KOFIA 事後修正）；回補或本機沒資料就抓全歷史。"""
    store = Store(name)
    last = store.last()
    start = "19900101" if (backfill or not last) else ymd((dt.date.fromisoformat(last) - dt.timedelta(days=40)).isoformat())
    end = today_seoul().strftime("%Y%m%d")
    rows = parser(kofia(obj, start, end))
    n = sum(store.add(r) for r in rows)
    log(f"{name}：新增/更新 {n} 筆；最早 {min(store.rows) if store.rows else None}，最新 {store.last()}")
    if not rows and not store.rows:
        raise Blocked(f"{name} 沒有取得任何資料")


def fetch_naver_price(name: str, code: str, backfill: bool):
    """Naver OHLC：每頁 60 筆由新往舊翻；日常翻到整頁都已存檔且內容相同就停，回補翻到沒有資料為止。"""
    store = Store(name)
    n = 0
    page = 1
    while True:
        rows = parse_naver_price(naver(f"{code}/price", {"pageSize": 60, "page": page}))
        if not rows:
            break
        changed = sum(store.add(r) for r in rows)
        n += changed
        if not backfill and changed == 0:
            break
        page += 1
        if page > 400:        # 400 頁 × 60 ＝ 24,000 日，遠超歷史長度；防無窮迴圈
            break
    log(f"{name}：新增/更新 {n} 筆；最早 {min(store.rows) if store.rows else None}，最新 {store.last()}")


def fetch_usdkrw(backfill: bool):
    store = Store("usdkrw")
    r = None
    for attempt in range(4):      # FRED 偶爾慢，讀取逾時就重試；FRED 對瀏覽器 UA 會逾時，用 requests 預設 UA
        try:
            r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv", params={"id": "DEXKOUS"}, timeout=90)
            r.raise_for_status()
            break
        except requests.RequestException as e:
            log(f"  FRED 第 {attempt + 1} 次失敗：{type(e).__name__}")
            time.sleep(10 * (attempt + 1))
    else:
        raise Blocked("FRED DEXKOUS 重試用盡")
    n = sum(store.add(row) for row in parse_fred_csv(r.text))
    log(f"usdkrw：新增/更新 {n} 筆；最早 {min(store.rows) if store.rows else None}，最新 {store.last()}")


def missing_days(store: Store, series: str, st: State, lo: str, today: dt.date, recent_days: int | None) -> list[str]:
    """交易日曆上、store 還沒有的日子（最新日在前）。多次查無資料且已非近期的日子視為該日無此資料。"""
    cal = calendar()
    if recent_days is not None:
        lo = max(lo, (today - dt.timedelta(days=recent_days)).isoformat())
    out = []
    for d in cal:
        if d < lo or d > today.isoformat() or store.has(d):
            continue
        age = (today - dt.date.fromisoformat(d)).days
        if st.gap_attempts(series, d) >= 3 and age > 5:
            continue
        out.append(d)
    return sorted(out, reverse=True)


def fetch_daily(series: str, st: State, backfill: bool, limit: int | None):
    """逐日序列：lend（KOFIA 借券）、inst_kospi、inst_kosdaq（Naver 買賣超）。最新日優先，回補中途頁面就已有近期資料。"""
    today = today_seoul()
    store = Store(series)
    lo = LEND_START if series == "lend" else INST_START
    todo = missing_days(store, series, st, lo, today, None if backfill else 45)
    if limit:
        todo = todo[:limit]
    log(f"{series}：待抓 {len(todo)} 天")
    n, fails = 0, 0
    for k, d in enumerate(todo, 1):
        try:
            if series == "lend":
                row = parse_kofia_lend_total(kofia("STATSCU0100000180BO", ymd(d), ymd(d)), d)
            else:
                code = "KOSPI" if series == "inst_kospi" else "KOSDAQ"
                row = parse_naver_trend(naver(f"{code}/trend", {"bizdate": ymd(d)}), d)
        except Blocked as e:
            fails += 1
            log(f"FAIL {series} {d}：{e}")
            if fails >= 3:
                log("連續失敗 3 次，停止本輪（下次續跑）。")
                st.save()
                raise Blocked(f"{series} 連續失敗")
            continue
        fails = 0
        if row is None:
            st.bump_gap(series, d)
            log(f"  {series} {d} 查無資料（第 {st.gap_attempts(series, d)} 次）")
        else:
            n += store.add(row)
        if k % 200 == 0:
            st.save()
            log(f"  ...{series} 已處理 {k}/{len(todo)}，目前到 {d}")
    st.save()
    log(f"{series}：本輪新增 {n} 筆；最新 {store.last()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backfill", action="store_true", help="回補全歷史，可續跑")
    ap.add_argument("--only", default="", help="逗號分隔：" + ",".join(SERIES))
    ap.add_argument("--limit", type=int, default=0, help="逐日序列最多抓幾天（測試用）")
    args = ap.parse_args()

    only = [s for s in args.only.split(",") if s] or SERIES
    unknown = set(only) - set(SERIES)
    if unknown:
        sys.exit(f"未知序列：{unknown}")
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

    bulk = {"kospi": "STATSCU0100000020BO", "kosdaq": "STATSCU0100000030BO"}
    for name, obj in bulk.items():
        if name in only:
            run(name, fetch_kofia_bulk, name, obj, parse_kofia_index, args.backfill)
    for name, code in (("px_kospi", "KOSPI"), ("px_kosdaq", "KOSDAQ")):
        if name in only:
            run(name, fetch_naver_price, name, code, args.backfill)
    if "deposit" in only:
        run("deposit", fetch_kofia_bulk, "deposit", "STATSCU0100000060BO", parse_kofia_deposit, args.backfill)
    if "credit" in only:
        run("credit", fetch_kofia_bulk, "credit", "STATSCU0100000070BO", parse_kofia_credit, args.backfill)
    if "usdkrw" in only:
        run("usdkrw", fetch_usdkrw, args.backfill)
    for s in ("lend", "inst_kospi", "inst_kosdaq"):
        if s in only:
            run(s, fetch_daily, s, st, args.backfill, args.limit or None)

    if args.backfill:       # 回補完整理檔案：依日期排序、每日一行
        for s in only:
            if (DATA / f"{s}.jsonl").exists():
                Store(s).compact()
    log("完成。" + (f" 失敗：{failed}" if failed else ""))
    if len(failed) >= 3:
        sys.exit(1)


if __name__ == "__main__":
    main()
