#!/usr/bin/env python3
"""long_pe.py — build_etf_dash.py 的 Exhibit 4「長期本益比」資料（2026-10-19 加）。

Exhibit 3 的本益比是本頁自己用成分股「明年度」EPS 算的，只能從 dd_eps_history
起點（2026-05-19）往後畫。要看「現在跟過去十幾年比貴不貴」，只能用外部長期
序列；外部序列的口徑跟 Exhibit 3 不同，所以另畫一張圖，不接在一起。

來源：History of Market（historyofmarket.com）公開 API，資料授權 CC BY 4.0
（https://historyofmarket.com/license/ ，引用要註明出處；網站 /ideas/ai-hardware-cycle/
已在用同一個 API）。分母是未來 12 個月共識盈餘（FY1／FY2 依時間加權），週資料：
  - sp500／ndx：api/sp500/forward-pe.json、api/ndx/forward-pe.json 的 forward／forwardOwn
  - 產業與費半：api/sectors/forward-pe.json 的 sectors.{inft,finl,sox,cond,cons}
對方的終端機資料（forward／series）停在 2026-08 前後，之後對方改用自己依 ETF 持股
算的每日線（forwardOwn，對方實測跟終端機差 3% 以內，但刻意不併進 series）。本模組
在終端機最後一天之後接上 forwardOwn，每週取最後一筆，接點寫在輸出的 own_from，
頁面註明。

TAIEX 另用證交所官方「大盤本益比」（過去 12 個月實際盈餘，不是預估）：市場交易月報
C02001 表（{YYYYMM}_C02001.zip，內含 xls），證交所註解的定義是「月底大盤總市值 ÷
所有上市公司最近四季稅後純益總和」。月資料 1999-01 起；每個月檔含近 12 個月，最新
一個月是初值，下個月的檔會修正。第一次（CSV 不存在）逐年抓 12 月檔回補，之後每天
只在缺上個月時試抓一個檔。2026-10-19 驗算：2008-11、2009-01、2009-04、2010-01、
2026-06 五個點跟 CEIC／rich01 轉載的證交所數字完全相同。0050 頁也用這條線（註明代替）。

TOPIX 用日本交易所（JPX）「規模別・業種別 PER・PBR」長期檔 longrange-perpbr.xlsx 的
連結、加權平均 PER（總市值÷純益合計）：2022-04 起取 Prime 市場，2013-01～2022-03 取
第一部（改制時家數 2,159 → 1,821）。分母是各公司最近一期已公布的年度盈餘，不是近四季；
多數公司 3 月決算，6 月底才換新年度盈餘（2013–2026 純益合計單月變動超過 8% 的 9 次
全在 6 月）。2025-10～2026-09 四個時點跟 JPX TOPIX 資料表的 PER 差 2% 以內。資料版權
屬 JPX，持有人 2026-10-19 知情決定上站並註明。

存檔：data/etf_dash/long_pe/{key}.csv（date,pe,src；src＝terminal／own／twse／jpx），美股一列
一週、台股一列一月，每天的 CI 只會改最後幾列，不存整包 API 原始回應（單檔 285KB，天天改會讓公開
repo 長太快）。抓失敗沿用 CSV；API 回應比 CSV 短時，CSV 裡更早的列保留。
"""
from __future__ import annotations

import calendar
import csv
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LONG_PE_DIR = ROOT / "data" / "etf_dash" / "long_pe"

HOM_ATTRIBUTION = "History of Market（historyofmarket.com），CC BY 4.0"
HOM_URLS = {
    "sp500": "https://historyofmarket.com/api/sp500/forward-pe.json",
    "ndx": "https://historyofmarket.com/api/ndx/forward-pe.json",
    "sectors": "https://historyofmarket.com/api/sectors/forward-pe.json",
}
# 序列 key → (API 檔, sectors 子鍵, 中文名稱)
HOM_SERIES = {
    "sp500": ("sp500", None, "標普 500 指數"),
    "ndx": ("ndx", None, "那斯達克 100 指數"),
    "s5inft": ("sectors", "inft", "標普 500 資訊科技類股"),
    "s5finl": ("sectors", "finl", "標普 500 金融類股"),
    "s5cond": ("sectors", "cond", "標普 500 非必需消費類股"),
    "s5cons": ("sectors", "cons", "標普 500 必需消費類股"),
    "sox": ("sectors", "sox", "費城半導體指數"),
}
# 基金 → (序列 key, 代替說明；None＝同一個指數)
FUND_LONG_PE = {
    "SPY": ("sp500", None),
    "QQQ": ("ndx", None),
    "XLK": ("s5inft", None),
    "XLF": ("s5finl", None),
    "XLY": ("s5cond", None),
    "XLP": ("s5cons", None),
    "SMH": ("sox", "SMH 追蹤 MVIS 美國上市半導體 25 指數，這裡用成分相近的費城半導體指數（30 檔）代替。"),
    "SMH_UCITS": ("sox", "本基金追蹤 MVIS 美國上市半導體 25 指數（有單一個股權重上限），"
                         "這裡用成分相近的費城半導體指數（30 檔）代替。"),
    "TAIEX": ("twse", None),
    "0050": ("twse", "0050 只有市值前 50 大公司，這裡用全體上市公司的大盤本益比代替。"),
    "TOPIX": ("jpx", "這是東證 Prime 市場全體（2022-03 以前是第一部）的本益比，跟 TOPIX 成分相近但不完全相同；"
                     "2022-04 改制時家數從 2,159 家變成 1,821 家，前後不完全可比。"),
}
JPX_PE_URL = ("https://www.jpx.co.jp/markets/statistics-equities/misc/"
              "tvdivq00000015r6-att/longrange-perpbr.xlsx")
# （工作表, 該表第一個市場組的名稱關鍵字）；舊表先讀，新表覆蓋
JPX_SHEETS = (("Consolidated(WT AVG)～202203", "第一部"), ("Consolidated(Weighted avg.)", "プライム"))
# 過去實際盈餘的兩個來源，頁面文字（sub_zh 的 {y}＝起始年）
TRAILING_META = {
    "twse": {
        "title_zh": "長期本益比（過去四季實際盈餘）",
        "sub_zh": "台股上市公司整體的本益比（月底總市值÷近四季稅後純益），月資料，{y} 年起；虛線是這段期間的中位數",
        "compare_note_zh": "分母用過去四季實際盈餘，Exhibit 3 用明年度預估盈餘，兩張圖的數字不能直接相比；"
                           "盈餘衰退時這條線會往上衝。",
        "source_zh": "臺灣證券交易所 市場交易月報（大盤本益比）",
        "source_url": "https://www.twse.com.tw/zh/trading/statistics/index02.html",
    },
    "jpx": {
        "title_zh": "長期本益比（最近一個會計年度實際盈餘）",
        "sub_zh": "東證上市公司整體的本益比（月底總市值÷最近一期年度合併純益），月資料，{y} 年起；虛線是這段期間的中位數",
        "compare_note_zh": "分母是各公司最近一期已公布的年度盈餘，不是近四季。日本多數公司 3 月決算，6 月底才換上新年度盈餘，"
                           "線在 6 月的跳動多半是換盈餘，不是行情。Exhibit 3 用明年度預估盈餘，兩張圖的數字不能直接相比。",
        "source_zh": "日本取引所集團（JPX）規模別・業種別 PER・PBR（連結、加權平均），資料版權屬 JPX",
        "source_url": "https://www.jpx.co.jp/markets/statistics-equities/misc/04.html",
    },
}
TWSE_PE_URL = "https://www.twse.com.tw/staticFiles/inspection/inspection/02/001/{ym}_C02001.zip"
TWSE_PE_START = "1999-01-31"
TWSE_SLEEP_S = 4.5  # 證交所會封鎖太快的連線
UA = {"User-Agent": "Mozilla/5.0 (research.investmquest.com etf-dash)"}


def _get_json(url: str) -> dict:
    last = None
    for k in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(5 * (k + 1))
    raise RuntimeError(f"{url}: {last}")


def _weekly_last(points: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """同一個 ISO 週只留最後一筆（跟對方 series 的取樣規則一致）。"""
    by_week: dict[tuple[int, int], tuple[str, float]] = {}
    for d, v in sorted(points):
        by_week[date.fromisoformat(d).isocalendar()[:2]] = (d, v)
    return sorted(by_week.values())


def extract_hom_series(raw: dict, sub: str | None) -> list[dict]:
    """API 回應 → [{date, pe, src}]：終端機週資料，最後一天之後接 forwardOwn（每週最後一筆）。"""
    node = raw["sectors"][sub] if sub else raw
    terminal_raw = node.get("series") if sub else node.get("forward")
    terminal = sorted((p["date"], float(p["value"])) for p in (terminal_raw or [])
                      if p.get("value") is not None)
    own = [(p["date"], float(p["value"])) for p in (node.get("forwardOwn") or []) if p.get("value") is not None]
    last_terminal = terminal[-1][0] if terminal else ""
    own_tail = _weekly_last([p for p in own if p[0] > last_terminal])
    return ([{"date": d, "pe": v, "src": "terminal"} for d, v in terminal]
            + [{"date": d, "pe": v, "src": "own"} for d, v in own_tail])


def _csv_path(key: str) -> Path:
    return LONG_PE_DIR / f"{key}.csv"


def read_csv(key: str) -> list[dict]:
    p = _csv_path(key)
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        return [{"date": r["date"], "pe": float(r["pe"]), "src": r["src"]} for r in csv.DictReader(f)]


def write_csv(key: str, rows: list[dict]) -> None:
    LONG_PE_DIR.mkdir(parents=True, exist_ok=True)
    with _csv_path(key).open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "pe", "src"])
        for r in rows:
            w.writerow([r["date"], f"{r['pe']:.2f}", r["src"]])


def merge_rows(cached: list[dict], fresh: list[dict]) -> list[dict]:
    """fresh 涵蓋的日期範圍以 fresh 為準；fresh 第一天之前的快取列保留。"""
    if not fresh:
        return cached
    first = fresh[0]["date"]
    return [r for r in cached if r["date"] < first] + fresh


def refresh_hom(keys: set[str] | None = None) -> dict[str, list[dict]]:
    """抓需要的 API 檔（每檔一次），更新 CSV，回傳 {序列 key: rows}。任何一檔抓失敗
    只影響用到它的序列，沿用 CSV。"""
    keys = keys or set(HOM_SERIES)
    raws: dict[str, dict | None] = {}
    out: dict[str, list[dict]] = {}
    for key in sorted(keys):
        api, sub, _ = HOM_SERIES[key]
        if api not in raws:
            try:
                raws[api] = _get_json(HOM_URLS[api])
            except Exception as e:  # noqa: BLE001
                print(f"[long_pe] WARNING fetch {api} failed, using cached CSV: {e}", file=sys.stderr)
                raws[api] = None
        cached = read_csv(key)
        rows = cached
        if raws[api] is not None:
            try:
                rows = merge_rows(cached, extract_hom_series(raws[api], sub))
            except Exception as e:  # noqa: BLE001  API 改版
                print(f"[long_pe] WARNING parse {key} failed, using cached CSV: {e}", file=sys.stderr)
        if rows and rows != cached:
            write_csv(key, rows)
        out[key] = rows
    return out


def _eom(y: int, m: int) -> str:
    return f"{y:04d}-{m:02d}-{calendar.monthrange(y, m)[1]:02d}"


def _months_back(today: date, k: int) -> tuple[int, int]:
    y, m = today.year, today.month - k
    while m < 1:
        m += 12
        y -= 1
    return y, m


_PE_HDR = re.compile(r"本益比|PE\s*Ratio|^\s*P/?E\s*$|^\s*PE\s*$|\(PER\)", re.I)


def parse_twse_c02001(blob: bytes) -> dict[str, float]:
    """C02001 zip → {月底日期: 本益比}。用欄位標題找「本益比」欄（1999–2002、2003–2004、
    2005 以後三種版面欄位位置不同）；年度列（如「110(2021)」）記成該年 12-31。"""
    import xlrd
    out: dict[str, float] = {}
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        name = [n for n in z.namelist() if n.lower().endswith(".xls")][0]
        wb = xlrd.open_workbook(file_contents=z.read(name))
    for ws in wb.sheets():
        col = hdr_row = None
        for i in range(ws.nrows):
            for j, c in enumerate(ws.row_values(i)):
                if isinstance(c, str) and _PE_HDR.search(c) and "殖利率" not in c:
                    col, hdr_row = j, i
                    break
            if col is not None:
                break
        if col is None:
            continue
        year = None
        seen_rows = False
        for i in range(hdr_row + 1, ws.nrows):
            row = ws.row_values(i)
            lab = str(row[0]).strip() if row[0] != "" else ""
            if not lab and len(row) > 1:
                lab = str(row[1]).strip()
            if lab.startswith("註") or lab.startswith("Note"):
                break
            if lab and seen_rows and not re.match(r"^[\d(]", lab) and not re.match(r"^\d{1,2}\s*月", lab):
                break  # 下一張表的標題
            v = row[col] if col < len(row) else None
            v = float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None
            m = re.match(r"^(\d{2,3})\s*\((\d{4})\)", lab)
            if m:
                seen_rows = True
                if v is not None:
                    out[f"{int(m.group(2))}-12-31"] = v
                continue
            if re.search(r"\(1-\d+月?\)", lab):
                continue
            m = re.match(r"^(?:\()?(\d{2,3})?\s*(?:\((\d{4})\))?\s*年?\s*(\d{1,2})\s*月", lab)
            if not m:
                continue
            seen_rows = True
            if m.group(1):
                year = int(m.group(1)) + 1911
            elif m.group(2):
                year = int(m.group(2))
            if year is None or v is None:
                continue
            out[_eom(year, int(m.group(3)))] = v
        if out:
            break
    return out


def _twse_zip(ym: str, raw_dir: Path | None = None, sleep: float = TWSE_SLEEP_S) -> bytes | None:
    """抓一個月檔；檔案還沒發布（404 或回的不是 zip）回 None，不重試。raw_dir 有現成檔就不連網。"""
    local = raw_dir / f"{ym}_C02001.zip" if raw_dir else None
    if local and local.exists():
        return local.read_bytes()
    time.sleep(sleep)
    try:
        req = urllib.request.Request(TWSE_PE_URL.format(ym=ym), headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            blob = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    return blob if blob[:2] == b"PK" else None


def refresh_twse(today: date | None = None, raw_dir: Path | None = None) -> list[dict]:
    """更新 twse.csv。CSV 不存在時逐年抓 12 月檔回補（約 30 個檔）；之後只在缺上個月
    時試抓上個月（再不行抓前一個月）的檔，新檔的數字覆蓋舊值（初值會被修正）。"""
    today = today or date.today()
    cached = read_csv("twse")
    data = {r["date"]: r["pe"] for r in cached}
    jobs = [] if cached else [f"{y}12" for y in range(int(TWSE_PE_START[:4]), today.year)]
    for ym in jobs:
        blob = _twse_zip(ym, raw_dir)
        if blob is None:
            raise RuntimeError(f"TWSE C02001 {ym} missing during backfill")
        data.update(parse_twse_c02001(blob))
    last = cached[-1]["date"] if cached else ""
    for k in (1, 2):
        y, m = _months_back(today, k)
        if _eom(y, m) <= last:
            break
        blob = _twse_zip(f"{y}{m:02d}", raw_dir)
        if blob is not None:
            data.update(parse_twse_c02001(blob))
            break
    rows = [{"date": d, "pe": round(v, 2), "src": "twse"} for d, v in sorted(data.items())
            if d >= TWSE_PE_START]
    if rows and rows != cached:
        write_csv("twse", rows)
    return rows


def parse_jpx_perpbr(blob: bytes) -> dict[str, float]:
    """longrange-perpbr.xlsx → {月底日期: PER}。用標題列找「PER」欄，並確認上一列的市場組
    名稱是第一部／Prime，版面改了就報錯（沿用 CSV），不會默默讀到別的市場。"""
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(blob), read_only=True, data_only=True)
    out: dict[str, float] = {}
    for sheet, group_kw in JPX_SHEETS:
        rows = list(wb[sheet].iter_rows(values_only=True))
        hdr = next(i for i, r in enumerate(rows) if "PER" in r)
        col = rows[hdr].index("PER")
        group = " ".join(str(c) for c in rows[hdr - 1][:col + 1] if c)
        if group_kw not in group:
            raise RuntimeError(f"JPX {sheet}: PER 欄的市場組是 {group!r}，不是 {group_kw}")
        for r in rows[hdr + 1:]:
            if isinstance(r[0], (int, float)) and isinstance(r[1], (int, float)) and isinstance(r[col], (int, float)):
                out[_eom(int(r[0]), int(r[1]))] = float(r[col])  # 純益合計 ≤ 0 時是 "-"，略過
    return out


def refresh_jpx(today: date | None = None, blob: bytes | None = None) -> list[dict]:
    """更新 jpx.csv。CSV 已有上個月就不連網；否則抓整份長期檔（約 220KB）重讀。"""
    today = today or date.today()
    cached = read_csv("jpx")
    y, m = _months_back(today, 1)
    if blob is None:
        if cached and cached[-1]["date"] >= _eom(y, m):
            return cached
        req = urllib.request.Request(JPX_PE_URL, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            blob = r.read()
    data = {r["date"]: r["pe"] for r in cached}
    data.update(parse_jpx_perpbr(blob))
    rows = [{"date": d, "pe": round(v, 2), "src": "jpx"} for d, v in sorted(data.items())]
    if rows and rows != cached:
        write_csv("jpx", rows)
    return rows


def refresh(keys: set[str]) -> dict[str, list[dict]]:
    """build_etf_dash.py main() 的入口：依序列 key 分派到各來源，任何一個來源失敗只影響
    自己，沿用 CSV。"""
    out = refresh_hom({k for k in keys if k in HOM_SERIES}) if keys & set(HOM_SERIES) else {}
    for key, fn in (("twse", refresh_twse), ("jpx", refresh_jpx)):
        if key in keys:
            try:
                out[key] = fn()
            except Exception as e:  # noqa: BLE001
                print(f"[long_pe] WARNING {key} refresh failed, using cached CSV: {e}", file=sys.stderr)
                out[key] = read_csv(key)
    return out


def summarize(rows: list[dict]) -> dict:
    """中位數與「目前值高於歷史上多少比例的週」。"""
    vals = sorted(r["pe"] for r in rows)
    n = len(vals)
    cur = rows[-1]["pe"]
    median = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2
    pct_below = sum(1 for v in vals if v < cur) / n * 100
    return {"median": round(median, 2), "current": round(cur, 2), "pct_below": round(pct_below, 1)}


def build_long_pe(etf_key: str, series_by_key: dict[str, list[dict]]) -> dict:
    """給 docs/etf-dash/data/{ETF}.json 的 chart.long_pe。頁面要顯示的說明文字在這裡
    組好（兩種來源口徑不同），前端只負責畫圖。沒有對應序列的基金回 available=False，
    頁面顯示一行說明。"""
    if etf_key not in FUND_LONG_PE:
        return {"available": False,
                "note_zh": "這檔 ETF 找不到可以公開使用的長期本益比資料。"}
    key, proxy_note = FUND_LONG_PE[etf_key]
    rows = series_by_key.get(key) or []
    if not rows:
        return {"available": False, "note_zh": "長期本益比資料暫時抓不到，下次更新再試。"}
    start_year = rows[0]["date"][:4]
    out = {
        "available": True,
        "series_key": key,
        "proxy_note_zh": proxy_note,
        "series": [{"date": r["date"], "pe": round(r["pe"], 2)} for r in rows],
        "start_date": rows[0]["date"],
        "end_date": rows[-1]["date"],
        "stats": summarize(rows),
    }
    if key in TRAILING_META:
        meta = TRAILING_META[key]
        out.update({**meta, "sub_zh": meta["sub_zh"].format(y=start_year), "kind": "trailing",
                    "period_unit_zh": "月", "stale_days": 75,  # 月資料約在下個月中旬發布
                    "own_note_zh": None})
        return out
    own_from = next((r["date"] for r in rows if r["src"] == "own"), None)
    out.update({
        "kind": "forward_ntm",
        "title_zh": "長期預估本益比",
        "sub_zh": f"{HOM_SERIES[key][2]}的預估本益比（股價÷未來 12 個月共識盈餘），週資料，{start_year} 年起；"
                  "虛線是這段期間的中位數",
        "period_unit_zh": "週",
        "stale_days": 21,
        "compare_note_zh": "分母用未來 12 個月盈餘，Exhibit 3 用明年度盈餘，兩張圖的數字不能直接相比。",
        "own_note_zh": (f"{own_from} 起是對方依 ETF 持股自算的同口徑延伸線，對方實測跟原始資料差 3% 以內"
                        if own_from else None),
        "source_zh": HOM_ATTRIBUTION,
        "source_url": "https://historyofmarket.com/license/",
    })
    return out


if __name__ == "__main__":
    for k, rows in refresh(set(HOM_SERIES) | {"twse", "jpx"}).items():
        s = summarize(rows) if rows else {}
        print(k, len(rows), rows[0]["date"] if rows else None, rows[-1]["date"] if rows else None, s)
