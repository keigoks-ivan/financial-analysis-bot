#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主動式 ETF 折溢價（/active-etf/）每日資料：docs/active-etf/data/premium.json。

折溢價 %＝(證交所收盤價 ÷ 每單位淨值 − 1) × 100。正數＝收盤價高於淨值（溢價）。

資料來源：
  1. 收盤價：證交所 MI_INDEX?type=0099P（每日收盤行情 ETF）。逐日抓，快取在
     data/active_etf/close_twse.jsonl；只抓「有淨值、尚未快取」的日期，休市日回空表不寫入。
  2. 淨值（優先）：證交所 MIS all_etf.txt（h＝前一營業日每單位淨值）。每次執行抓一次，
     用 h 對投信 PCF 淨值判斷 h 屬於哪一天，存 data/active_etf/nav_twse.jsonl。
     MIS 從 GitHub Actions 不一定連得到，抓不到只記錄、不影響其他步驟。
  3. 淨值（補）：data/active_etf/holdings/{code}.jsonl 的 nav.nav_per_unit（投信 PCF，
     as_of 當日淨值）。同一 as_of 取最後一行。

  python3 scripts/active_etf/premium.py
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_holdings import FUND_REGISTRY  # noqa: E402

HOLDINGS_DIR = REPO_ROOT / "data" / "active_etf" / "holdings"
CLOSE_PATH = REPO_ROOT / "data" / "active_etf" / "close_twse.jsonl"
NAV_TWSE_PATH = REPO_ROOT / "data" / "active_etf" / "nav_twse.jsonl"
OUT_PATH = REPO_ROOT / "docs" / "active-etf" / "data" / "premium.json"

BENCH = "0050"
CODES = list(FUND_REGISTRY) + [BENCH]
MI_INDEX_URL = "https://www.twse.com.tw/exchangeReport/MI_INDEX"
MIS_URL = "https://mis.twse.com.tw/stock/data/all_etf.txt"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
PACE_SEC = 1.3                 # 證交所限流，兩次請求至少隔 1.2 秒
SUSPECT_PCT = 5.0              # |折溢價| 超過這個值視為資料對不齊，不進序列與統計
MIN_MATCH = 10                 # MIS 的 h 判斷日期至少要有幾檔和 PCF 淨值相符
AVG_N = 20

# 不能用投信 PCF 淨值的基金。理由寫在這裡，不是靜默剔除。
# 2026-10-29 核對：00401A 的 PCF 淨值日期標錯。10-28 PCF 寫 13.42，證交所公告淨值
# 13.75（收盤 13.76）；用 PCF 會算出 −4.47%／+1.6% 的假折溢價。其他 20 檔 10-28 的
# PCF 淨值和證交所 h 完全相同。
PCF_NAV_UNRELIABLE = {
    "00401A": "投信 PCF 淨值日期標錯（2026-10-28 PCF 13.42，證交所公告 13.75）",
}

# 頁面顯示用說明
FUND_NOTES = {
    "00401A": "投信 PCF 淨值日期不準，折溢價只用證交所每日公告淨值，從 2026-10-28 起累積，歷史較短。",
    "00996A": "投信淨值自 2026-09-24 起無法自動取得，只能用證交所公告淨值從 2026-10-28 起累積，目前資料點很少。",
}


# ── 檔案 ─────────────────────────────────────────────────────────────────
def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def write_jsonl(path: Path, rows: list[dict], key: str) -> None:
    rows = sorted(rows, key=lambda r: r[key])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n"
                            for r in rows), encoding="utf-8")


def load_pcf_nav() -> dict[str, dict[str, float]]:
    """{code: {as_of: nav_per_unit}}，同一 as_of 取最後一行；排除 PCF_NAV_UNRELIABLE。"""
    out: dict[str, dict[str, float]] = {}
    for code in FUND_REGISTRY:
        if code in PCF_NAV_UNRELIABLE:
            continue
        p = HOLDINGS_DIR / f"{code}.jsonl"
        d: dict[str, float] = {}
        for rec in read_jsonl(p):
            nav = (rec.get("nav") or {}).get("nav_per_unit")
            if rec.get("as_of") and nav:
                d[rec["as_of"]] = float(nav)
        out[code] = d
    return out


# ── 證交所收盤價 ─────────────────────────────────────────────────────────
def _num(s) -> float | None:
    try:
        v = float(str(s).replace(",", ""))
    except (TypeError, ValueError):
        return None
    return v if v > 0 else None


def parse_close_table(payload: dict) -> dict[str, float]:
    """從 MI_INDEX 回應取出每日收盤行情(ETF)表的 {代號: 收盤價}；休市日回空 dict。"""
    for t in payload.get("tables") or []:
        fields = t.get("fields") or []
        if "證券代號" in fields and "收盤價" in fields and "每日收盤行情" in (t.get("title") or ""):
            ic, ip = fields.index("證券代號"), fields.index("收盤價")
            out = {}
            for row in t.get("data") or []:
                v = _num(row[ip])
                if v is not None:
                    out[str(row[ic]).strip()] = v
            return out
    return {}


def fetch_close(date: str, session: requests.Session) -> dict[str, float]:
    """抓單日 ETF 收盤。date＝YYYY-MM-DD。暫時性錯誤重試 3 次，仍失敗就丟例外。"""
    params = {"response": "json", "date": date.replace("-", ""), "type": "0099P"}
    last = None
    for i in range(3):
        try:
            r = session.get(MI_INDEX_URL, params=params, headers=UA, timeout=30)
            r.raise_for_status()
            return parse_close_table(r.json())
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"MI_INDEX {date} 失敗：{last}")


def update_close_cache(need_dates: list[str], session: requests.Session) -> dict[str, dict]:
    """補抓 need_dates 裡尚未快取的日期；回傳 {date: {code: close}}（只含 CODES）。"""
    rows = {r["date"]: r["close"] for r in read_jsonl(CLOSE_PATH)}
    todo = sorted(d for d in set(need_dates) if d not in rows)
    added = 0
    for i, d in enumerate(todo):
        if i:
            time.sleep(PACE_SEC)
        try:
            tbl = fetch_close(d, session)
        except Exception as e:  # noqa: BLE001
            print(f"WARN close {d}: {e}")
            continue
        close = {c: tbl[c] for c in CODES if c in tbl}
        if not tbl:
            print(f"close {d}: 空表（休市），不寫入")
            continue
        rows[d] = close
        added += 1
    if added:
        write_jsonl(CLOSE_PATH, [{"date": d, "close": c} for d, c in rows.items()], "date")
    print(f"close cache: {len(rows)} 日，本次新增 {added}（待抓 {len(todo)}）")
    return rows


# ── MIS 淨值快照 ─────────────────────────────────────────────────────────
def fetch_mis(session: requests.Session) -> list[dict] | None:
    try:
        r = session.get(MIS_URL, headers=UA, timeout=30)
        r.raise_for_status()
        # a1 是多個分組，每組各有 msgArray，要全部攤平
        return [m for g in r.json()["a1"] for m in (g.get("msgArray") or [])]
    except Exception as e:  # noqa: BLE001
        print(f"WARN MIS all_etf.txt 抓不到：{e}")
        return None


def prev_trading_date(d: str, close_dates: list[str], session: requests.Session | None = None) -> str | None:
    """d 之前最近的交易日。先看收盤快取（已涵蓋所有 PCF 日期），不夠再往回查 MI_INDEX 最多 7 天。"""
    earlier = [x for x in close_dates if x < d]
    cand = max(earlier) if earlier else None
    dt = datetime.date.fromisoformat(d)
    # 快取最近一筆若離 d 超過 1 天，中間可能還有沒快取的交易日，再往回探（週末跳過）
    if session is not None and (cand is None or (dt - datetime.date.fromisoformat(cand)).days > 1):
        for k in range(1, 8):
            x = dt - datetime.timedelta(days=k)
            if cand is not None and x.isoformat() <= cand:
                break
            if x.weekday() >= 5:
                continue
            time.sleep(PACE_SEC)
            try:
                if fetch_close(x.isoformat(), session):
                    return x.isoformat()
            except Exception as e:  # noqa: BLE001
                print(f"WARN prev_trading_date {x}: {e}")
    return cand


def match_nav_date(mis_h: dict[str, float], pcf: dict[str, dict[str, float]],
                   candidates: list[str]) -> tuple[str | None, dict[str, int]]:
    """判斷 MIS 的 h（每單位淨值）屬於哪一天。

    對每個候選日，數有幾檔「h 四捨五入到小數 2 位＝該日 PCF 淨值」。取相符最多的日期；
    最多的也少於 MIN_MATCH，或兩個日期並列，就回 None（寧可不寫）。
    pcf 已排除 PCF_NAV_UNRELIABLE。回傳 (日期或 None, {候選日: 相符檔數})。
    """
    counts = {}
    for d in candidates:
        n = 0
        for code, h in mis_h.items():
            if code in PCF_NAV_UNRELIABLE:
                continue
            v = pcf.get(code, {}).get(d)
            if v is not None and round(h, 2) == round(v, 2):
                n += 1
        counts[d] = n
    best = max(counts.values()) if counts else 0
    winners = [d for d, n in counts.items() if n == best]
    if best < MIN_MATCH or len(winners) != 1:
        return None, counts
    return winners[0], counts


def update_nav_snapshot(pcf: dict, close_rows: dict, session: requests.Session) -> None:
    rows = fetch_mis(session)
    if rows is None:
        return
    by = {str(r.get("a")): r for r in rows if r.get("a") in CODES}
    mis_h = {}
    for c, r in by.items():
        v = _num(r.get("h"))
        if v is not None:
            mis_h[c] = v
    if not mis_h:
        print("WARN MIS 沒有 registry 內的基金，不寫入")
        return
    snaps = [str(r.get("i")) for r in by.values() if r.get("i")]
    if not snaps:
        print("WARN MIS 沒有快照日期，不寫入")
        return
    i_raw = max(set(snaps), key=snaps.count)
    snap_date = f"{i_raw[:4]}-{i_raw[4:6]}-{i_raw[6:]}"
    prev = prev_trading_date(snap_date, sorted(close_rows), session)
    cands = [d for d in (snap_date, prev) if d]
    nav_date, counts = match_nav_date(mis_h, pcf, cands)
    if nav_date is None:
        print(f"WARN MIS h 日期無法判斷（相符檔數 {counts}，需 ≥{MIN_MATCH} 且唯一），不寫入")
        return
    times = [str(r.get("j")) for r in by.values() if r.get("j")]
    rec = {
        "nav_date": nav_date,
        "snapshot_date": snap_date,
        "snapshot_time": max(set(times), key=times.count) if times else None,
        "nav": {c: v for c, v in sorted(mis_h.items())},
        "units": {c: u for c, u in sorted((c, _num(r.get("c"))) for c, r in by.items()) if u is not None},
    }
    existing = [r for r in read_jsonl(NAV_TWSE_PATH) if r["nav_date"] != nav_date]
    write_jsonl(NAV_TWSE_PATH, existing + [rec], "nav_date")
    print(f"MIS: h 歸屬 {nav_date}（快照 {snap_date} {rec['snapshot_time']}，相符 {counts}），{len(mis_h)} 檔")


# ── 折溢價計算 ───────────────────────────────────────────────────────────
def compute_premium(close_rows: dict[str, dict], twse_nav: dict[str, dict], pcf: dict) -> dict:
    """回傳 {code: {"series": [(date, pct, close, nav, source)], "suspect": [...]}}。

    淨值：證交所快照有就用，否則用 PCF（PCF_NAV_UNRELIABLE 內的基金 pcf 裡沒有）。
    |折溢價| > SUSPECT_PCT 當成日期對不齊：不進 series，放 suspect。
    """
    out = {}
    for code in CODES:
        series, suspect = [], []
        for d in sorted(close_rows):
            close = close_rows[d].get(code)
            if close is None:
                continue
            if d in twse_nav and code in twse_nav[d]["nav"]:
                nav, src = twse_nav[d]["nav"][code], "twse"
            elif d in pcf.get(code, {}):
                nav, src = pcf[code][d], "pcf"
            else:
                continue
            pct = round((close / nav - 1) * 100, 2)
            if abs(pct) > SUSPECT_PCT:
                suspect.append({"date": d, "close": close, "nav": nav, "nav_source": src, "pct": pct})
            else:
                series.append((d, pct, close, nav, src))
        out[code] = {"series": series, "suspect": suspect}
    return out


def summarize(code: str, res: dict) -> dict | None:
    s = res["series"]
    if not s and not res["suspect"]:
        return None
    d: dict = {"n": len(s)}
    if s:
        last = s[-1]
        pcts = [x[1] for x in s]
        tail = pcts[-AVG_N:]
        mx = max(s, key=lambda x: x[1])
        mn = min(s, key=lambda x: x[1])
        d.update({
            "latest": {"date": last[0], "pct": last[1], "close": last[2], "nav": last[3], "nav_source": last[4]},
            "avg20_pct": round(sum(tail) / len(tail), 2),
            "max_pct": {"date": mx[0], "pct": mx[1]},
            "min_pct": {"date": mn[0], "pct": mn[1]},
            "days_over_1pct": sum(1 for p in pcts if p > 1),
            "days_under_minus1pct": sum(1 for p in pcts if p < -1),
            "first_date": s[0][0],
            "series": [[x[0], x[1]] for x in s],
        })
    if res["suspect"]:
        d["suspect"] = res["suspect"]
    if code in FUND_NOTES:
        d["note"] = FUND_NOTES[code]
    return d


def main() -> int:
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
    session = requests.Session()
    pcf = load_pcf_nav()
    close_rows = {r["date"]: r["close"] for r in read_jsonl(CLOSE_PATH)}

    # 先抓 MIS（需要 close 快取判斷前一交易日），再補收盤價
    update_nav_snapshot(pcf, close_rows, session)
    twse_nav = {r["nav_date"]: r for r in read_jsonl(NAV_TWSE_PATH)}

    nav_dates = set(twse_nav)
    for d in pcf.values():
        nav_dates.update(d)
    today = datetime.date.today().isoformat()
    close_rows = update_close_cache([d for d in nav_dates if d <= today], session)

    res = compute_premium(close_rows, twse_nav, pcf)
    funds = {}
    for code in CODES:
        s = summarize(code, res[code])
        if s is not None:
            funds[code] = s
    latest = max((f["latest"]["date"] for f in funds.values() if "latest" in f), default=None)
    out = {
        "schema": "active-etf-premium-v1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "latest_date": latest,
        "method": "折溢價＝(證交所每日收盤價 ÷ 每單位淨值 − 1) × 100，正數為溢價。收盤價取證交所每日收盤行情(ETF)；"
                  "淨值以證交所 MIS 公告為主，缺的日期用投信 PCF 淨值補。|折溢價| 超過 5% 視為日期對不齊，"
                  "不進序列與統計，列在各檔 suspect。",
        "funds": funds,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(REPO_ROOT)}：{len(funds)} 檔，最新 {latest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
