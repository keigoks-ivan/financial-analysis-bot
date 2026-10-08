"""美國下次公布日：每週抓一次，寫 data/macro_db/release_calendar.json。

來源：BLS 官方 ICS、Census 經濟指標行事曆 HTML、BEA 時程 HTML、FOMC 會期 JSON；
週頻的失業救濟金／房貸利率（週四）、H.4.1（週四）、H.8（週五）用規則產生。
任一來源失敗就沿用上次檔案裡那一部分。

注意：本檔名與標準庫 calendar 相同。執行時 sys.path 不可包含 scripts/macro_db/ 本身
（run.py 會處理）；其他模組一律用 `from macro_db import calendar as relcal` 引用。
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

if __name__ == "__main__":  # 避免本檔蓋掉標準庫 calendar
    _here = str(Path(__file__).resolve().parent)
    sys.path[:] = [p for p in sys.path if str(Path(p or ".").resolve()) != _here]
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from macro_db.sources._http import get  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "macro_db" / "release_calendar.json"

NAMES = {
    "nfp": "就業狀況報告（非農）",
    "cpi": "消費者物價指數（CPI）",
    "ppi": "生產者物價指數（PPI）",
    "jolts": "職缺與勞動異動調查（JOLTS）",
    "eci": "僱用成本指數（ECI）",
    "productivity": "勞動生產力與單位勞動成本",
    "retail": "零售銷售",
    "housing_starts": "新屋開工與營建許可",
    "new_home_sales": "新屋銷售",
    "durable": "耐久財訂單",
    "inventories": "企業存貨與銷售",
    "trade": "國際貿易",
    "gdp": "GDP",
    "pce": "個人所得與支出（PCE）",
    "fomc": "FOMC 利率決策",
    "claims": "初領失業救濟金（每週）",
    "pmms": "房貸利率（房地美，每週）",
    "h41": "Fed 資產負債表 H.4.1（每週）",
    "h8": "商業銀行 H.8（每週）",
}

BLS_MAP = {
    "Employment Situation": "nfp",
    "Consumer Price Index": "cpi",
    "Producer Price Index": "ppi",
    "Job Openings and Labor Turnover Survey": "jolts",
    "Employment Cost Index": "eci",
    "Productivity and Costs": "productivity",
}
CENSUS_MAP = [
    ("Advance Monthly Sales for Retail", "retail"),
    ("New Residential Construction", "housing_starts"),
    ("New Residential Sales", "new_home_sales"),
    ("Advance Report on Durable Goods", "durable"),
    ("Manufacturing and Trade: Inventories and Sales", "inventories"),
    ("U.S. International Trade in Goods and Services", "trade"),
]
MONTHS = {m: i + 1 for i, m in enumerate(
    "January February March April May June July August September October November December".split())}


def parse_bls_ics(text):
    text = re.sub(r"\r?\n[ \t]", "", text)
    out = {}
    for blk in text.split("BEGIN:VEVENT")[1:]:
        s = re.search(r"^SUMMARY:(.+)$", blk, re.M)
        d = re.search(r"^DTSTART[^:\n]*:(\d{4})(\d{2})(\d{2})", blk, re.M)
        if not s or not d:
            continue
        key = BLS_MAP.get(s.group(1).strip())
        if key:
            out.setdefault(key, set()).add("%s-%s-%s" % d.groups())
    return {k: sorted(v) for k, v in out.items()}


def parse_census(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    out = {}
    for tr in soup.select("tr"):
        td = tr.find_all("td")
        if len(td) < 4:
            continue
        name = re.sub(r"\s+", " ", td[0].get_text(" ", strip=True))
        key = next((k for pat, k in CENSUS_MAP if pat in name), None)
        if not key:
            continue
        m = re.match(r"([A-Za-z]+) (\d{1,2}), (\d{4})", td[1].get_text(" ", strip=True))
        if m and m.group(1) in MONTHS:
            out.setdefault(key, set()).add("%s-%02d-%02d" % (m.group(3), MONTHS[m.group(1)], int(m.group(2))))
    return {k: sorted(v) for k, v in out.items()}


def parse_bea(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    out, year = {}, None
    for tr in soup.select("#release-schedule-table tr"):
        th = tr.find("th")
        if th:
            m = re.search(r"Year (\d{4})", th.get_text())
            if m:
                year = int(m.group(1))
            continue
        d = tr.select_one(".release-date")
        t = tr.select_one(".release-title")
        if not d or not t or not year:
            continue
        m = re.match(r"([A-Za-z]+) (\d{1,2})", d.get_text(strip=True))
        if not m or m.group(1) not in MONTHS:
            continue
        title = t.get_text(" ", strip=True)
        key = None
        if title.startswith("GDP ("):
            key = "gdp"
        elif title.startswith("Personal Income and Outlays"):
            key = "pce"
        elif title.startswith("U.S. International Trade in Goods and Services"):
            key = "trade"
        if key:
            out.setdefault(key, set()).add("%d-%02d-%02d" % (year, MONTHS[m.group(1)], int(m.group(2))))
    return {k: sorted(v) for k, v in out.items()}


def parse_fomc(text):
    j = json.loads(text.lstrip("﻿"))
    ds = set()
    for e in j.get("events", []):
        if (e.get("title") or "").strip().lower() == "fomc meeting" and e.get("month") and e.get("days"):
            day = re.findall(r"\d+", str(e["days"]))
            if day:
                ds.add("%s-%02d" % (e["month"], int(day[-1])))
    return {"fomc": sorted(ds)}


def rule_dates(today, horizon=120):
    """週頻發布：失業救濟金／房貸利率／H.4.1 為週四，H.8 為週五。"""
    out = {"claims": [], "pmms": [], "h41": [], "h8": []}
    for i in range(-14, horizon):
        d = today + dt.timedelta(days=i)
        if d.weekday() == 3:
            for k in ("claims", "pmms", "h41"):
                out[k].append(d.isoformat())
        elif d.weekday() == 4:
            out["h8"].append(d.isoformat())
    return out


def _union(parts):
    out = {}
    for p in parts:
        for k, v in p.items():
            out.setdefault(k, set()).update(v)
    return {k: sorted(v) for k, v in out.items()}


SOURCES = [
    ("BLS ICS", lambda: parse_bls_ics(get("https://www.bls.gov/schedule/news_release/bls.ics"))),
    ("Census 經濟指標行事曆", lambda: _union(
        parse_census(get("https://www.census.gov/economic-indicators/calendar-listview-%d.html" % y))
        for y in (dt.date.today().year, dt.date.today().year + 1))),
    ("BEA 發布時程", lambda: parse_bea(get("https://www.bea.gov/news/schedule"))),
    ("FOMC 行事曆", lambda: parse_fomc(get("https://www.federalreserve.gov/json/calendar.json"))),
]


def build(old, today=None, sources=SOURCES):
    """回傳 (新檔內容, 失敗來源清單)。失敗的來源沿用 old 的對應 key。"""
    today = today or dt.date.today()
    rel = {k: dict(v) for k, v in (old or {}).get("releases", {}).items()}
    failed, fresh, src = [], {}, {}
    for name, fn in sources:
        try:
            got = fn()
            if not got:
                raise ValueError("解析不到任何日期")
            for k, dates in got.items():
                fresh.setdefault(k, set()).update(dates)
                src[k] = (src[k] + "＋" + name) if k in src else name
        except Exception as e:  # noqa: BLE001
            failed.append("%s：%s" % (name, str(e)[:120]))
    cutoff = (today - dt.timedelta(days=45)).isoformat()
    for k, dates in fresh.items():
        rel[k] = {"name_zh": NAMES.get(k, k), "dates": sorted(d for d in dates if d >= cutoff), "source": src[k]}
    for k, dates in rule_dates(today).items():
        rel[k] = {"name_zh": NAMES[k], "dates": dates, "source": "固定週期規則"}
    return {"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "releases": rel}, failed


def next_date(cal, key, today=None):
    today = (today or dt.date.today()).isoformat()
    for d in (cal or {}).get("releases", {}).get(key, {}).get("dates", []):
        if d >= today:
            return d
    return None


def load(path=OUT):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def main():
    old = load()
    new, failed = build(old)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(new, ensure_ascii=False, indent=1), encoding="utf-8")
    for f in failed:
        print("行事曆來源失敗，沿用舊資料：", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
