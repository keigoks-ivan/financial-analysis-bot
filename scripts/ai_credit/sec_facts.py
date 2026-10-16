"""SEC companyfacts 讀取與季度／近四季計算（純函式，可離線測試）。

重點：
- companyfacts 的流量事實多為年累計（3M／6M／9M／12M），零值季常常整筆缺漏，
  所以近四季一律用「最新年報 − 去年同期累計 + 今年累計」，不取最後四筆。
- 只收 10-Q／10-K（含 10-K405 等變體以外的 424B2、8-K 都濾掉）。
- 日期一律字串 YYYY-MM-DD，避免時區與浮點問題。
"""
from __future__ import annotations

import time
from datetime import date, timedelta

import requests

SEC_UA = {"User-Agent": "financial-analysis-bot keigoks@gmail.com"}
CIKS = {
    "MSFT": 789019, "GOOGL": 1652044, "AMZN": 1018724, "META": 1326801, "ORCL": 1341439,
    "CRWV": 1769628, "NVDA": 1045810, "ARCC": 1287750, "OBDC": 1655888, "BXSL": 1736035,
    # 第二輪：BDC、Broadcom、AMD
    "FSK": 1422183, "MAIN": 1396440, "GBDC": 1476765, "HTGC": 1280784, "OCSL": 1414932, "BBDC": 1379785,
    "AVGO": 1730168, "AMD": 2488,
}
PERIODIC_FORMS = ("10-Q", "10-K", "10-K/A", "10-Q/A", "10-K405")


def d(s: str) -> date:
    return date.fromisoformat(s)


def fetch_companyfacts(ticker: str, tries: int = 3, timeout: int = 120) -> dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIKS[ticker]:010d}.json"
    err = None
    for i in range(tries):
        try:
            r = requests.get(url, headers=SEC_UA, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"companyfacts {ticker} 抓取失敗：{err!r}")


def fetch_submissions(ticker: str, tries: int = 3, timeout: int = 60) -> dict:
    url = f"https://data.sec.gov/submissions/CIK{CIKS[ticker]:010d}.json"
    err = None
    for i in range(tries):
        try:
            r = requests.get(url, headers=SEC_UA, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"submissions {ticker} 抓取失敗：{err!r}")


def rows(facts: dict, tag: str, ns: str = "us-gaap", unit: str | None = None) -> list[dict]:
    """某 tag 的全部事實列（僅 10-Q／10-K 系列），去重（同 start/end 取最後申報者）。"""
    x = facts.get("facts", {}).get(ns, {}).get(tag)
    if not x:
        return []
    units = x["units"]
    u = unit or ("USD" if "USD" in units else next(iter(units)))
    raw = [r for r in units.get(u, []) if str(r.get("form", "")).split("/")[0] in ("10-Q", "10-K", "10-K405")]
    best: dict[tuple, dict] = {}
    for r in sorted(raw, key=lambda r: (r.get("filed", ""), r["end"])):
        best[(r.get("start"), r["end"])] = r
    return sorted(best.values(), key=lambda r: (r["end"], r.get("start") or ""))


def _days(r: dict) -> int:
    return (d(r["end"]) - d(r["start"])).days


def _near(a: str, b: str, tol: int) -> bool:
    return abs((d(a) - d(b)).days) <= tol


def ttm_window(rs: list[dict]) -> dict | None:
    """由主要 tag（如營運現金流）決定近四季的窗口：最新年報 A、其後最新的年初至今累計 C。

    回傳 {annual_end, ytd_start, ytd_end, end}；沒有年報回 None。最新年報之後沒有更新累計時 ytd_* 為 None。
    """
    annual = [r for r in rs if r.get("start") and 340 <= _days(r) <= 380]
    if not annual:
        return None
    A = annual[-1]
    nxt = (d(A["end"]) + timedelta(days=1)).isoformat()
    after = [r for r in rs if r.get("start") and r["end"] > A["end"] and 60 <= _days(r) <= 300 and _near(r["start"], nxt, 10)]
    if not after:
        return {"annual_end": A["end"], "ytd_start": None, "ytd_end": None, "end": A["end"]}
    C = max(after, key=lambda r: r["end"])
    return {"annual_end": A["end"], "ytd_start": C["start"], "ytd_end": C["end"], "end": C["end"]}


def _pick(rs: list[dict], start: str | None, end: str, tol: int, annual: bool = False) -> dict | None:
    for r in reversed(rs):
        if not r.get("start"):
            continue
        if annual:
            if 340 <= _days(r) <= 380 and _near(r["end"], end, tol):
                return r
        elif _near(r["end"], end, tol) and start is not None and _near(r["start"], start, tol):
            return r
    return None


def _shift_year(s: str) -> str:
    return (d(s) - timedelta(days=365)).isoformat()


def ttm_flow(tag_rows: list[list[dict]] | list[dict], win: dict | None = None, zero_ok: bool = False) -> dict | None:
    """近四季 = 最新年報 A − 去年同期累計 P + 今年累計 C。

    tag_rows：一個或多個候選 tag 的事實列（依優先序）；A／P／C 各自取第一個有該期間事實的 tag，
    不跨 tag 相加，避免同一筆事件被兩個 tag 重複計入。
    win：沿用另一個主要 tag 的窗口，讓所有流量對齊同一截止日；省略時由本 tag 自己決定。
    zero_ok：該期間完全沒有事實時視為 0（只給發債／還債這類「沒發生就不列示」的科目用），
             並把補 0 的元件記在 assumed_zero；否則任何元件缺漏都回 None。
    """
    if tag_rows and isinstance(tag_rows[0], dict):
        tag_rows = [tag_rows]  # type: ignore[assignment]
    tag_rows = [t for t in tag_rows if t] if zero_ok is False else list(tag_rows)
    win = win or (ttm_window(tag_rows[0]) if tag_rows and tag_rows[0] else None)
    if win is None:
        return None
    assumed: list[str] = []

    def comp(name: str, start: str | None, end: str, annual: bool = False):
        for rs in tag_rows:
            r = _pick(rs, start, end, 6 if annual or name == "C" else 12, annual)
            if r is not None:
                return r["val"]
        if zero_ok:
            assumed.append(name)
            return 0.0
        return None

    A = comp("A", None, win["annual_end"], annual=True)
    if A is None:
        return None
    if win["ytd_end"] is None:
        return {"value": A, "end": win["end"], "annual_end": win["annual_end"], "parts": {"A": A, "P": None, "C": None}, "assumed_zero": assumed}
    C = comp("C", win["ytd_start"], win["ytd_end"])
    P = comp("P", _shift_year(win["ytd_start"]), _shift_year(win["ytd_end"]))
    if C is None or P is None:
        return None
    return {"value": A - P + C, "end": win["end"], "annual_end": win["annual_end"], "start_ytd": win["ytd_start"],
            "parts": {"A": A, "P": P, "C": C}, "assumed_zero": assumed}


def single_quarters(rs: list[dict]) -> dict[str, float]:
    """單季值 {季末: 值}：直接 3 個月事實優先，其餘用同財年累計逐段相減（含 Q4＝年報 − 9M）。"""
    out: dict[str, float] = {}
    flows = [r for r in rs if r.get("start")]
    for r in flows:
        if 80 <= _days(r) <= 100:
            out[r["end"]] = r["val"]
    groups: dict[str, list[dict]] = {}
    for r in flows:
        groups.setdefault(r["start"], []).append(r)
    for _, g in groups.items():
        g = sorted(g, key=lambda r: r["end"])
        for prev, cur in zip(g, g[1:]):
            gap = (d(cur["end"]) - d(prev["end"])).days
            if 80 <= gap <= 100 and cur["end"] not in out:
                out[cur["end"]] = cur["val"] - prev["val"]
    return dict(sorted(out.items()))


def instants(facts: dict, tag: str, ns: str = "us-gaap", unit: str | None = None) -> list[dict]:
    """時點事實（資產負債表），同日取最後申報者；依日期升冪。"""
    rs = rows(facts, tag, ns, unit)
    best: dict[str, dict] = {}
    for r in rs:
        if not r.get("start") or r.get("start") == r["end"]:
            best[r["end"]] = r
    return [best[k] for k in sorted(best)]


def latest_instant(facts: dict, tag: str, ns: str = "us-gaap", unit: str | None = None) -> dict | None:
    xs = instants(facts, tag, ns, unit)
    return xs[-1] if xs else None


def instant_at(facts: dict, tag: str, end: str, ns: str = "us-gaap", unit: str | None = None) -> float | None:
    for r in instants(facts, tag, ns, unit):
        if r["end"] == end:
            return r["val"]
    return None
