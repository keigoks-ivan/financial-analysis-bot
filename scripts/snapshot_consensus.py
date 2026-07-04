#!/usr/bin/env python3
"""賽前共識凍結快照 — pre-earnings preview 的錨（Phase 4）.

一次執行，把「財報前市場對這一季的期望」定格成一份不可變的 JSON 錨，供
`pre-earnings-preview` skill 事後渲染成前瞻報告，並在財報後做「賽前 vs 賽後」
的錯價/期望落差複盤。核心精神：**賽前錨，事後不改** —— 檔案一旦寫下即凍結，
重跑一律拒絕覆寫，讓事後複盤永遠對照的是當初真正的市場期望，而非事後偷改的數字。

單次抓取（yfinance 一趟）：
  · 本季共識 EPS + 營收   earnings_estimate / revenue_estimate 的 0q avg
  · 現價                  fast_info → info 退位
  · 下次財報日            docs/catalyst/calendar.json 優先 → yf .calendar 退位
                          （--earnings-date 可強制指定）
  · ATM straddle 隱含波動   財報日「之後」最近一個到期日的價平 call+put 中價，
                          implied_move_pct = (call_mid + put_mid) / spot × 100
                          無選擇權鏈（如台股）→ null + note；2330.TW 以 TSM ADR
                          選擇權鏈代理，implied_move_proxy = "TSM ADR"

並嵌入 base_path_ref：讀該 ticker 最新 v13/v14 DD 的 dd-meta，取「財報那一季所屬
財年」的 fy_label / base_eps / dd_file（用 dd_meta_reader）。

輸出：docs/catalyst/snapshots/preview_{TICKER}_{YYYYMMDD}.json
      （YYYYMMDD = 財報日）

誠實失敗：任一欄位抓取失敗 → 該欄 null + 記 notes[]，仍寫檔（有殘缺的凍結錨也
勝過沒有錨）。唯一硬失敗：**財報日本身無法解析** → 直接 error out（檔名靠它）。

永不覆寫：檔案已存在 → 非零離開，告知使用者該快照已凍結。

Usage:
  python3 scripts/snapshot_consensus.py TICKER
  python3 scripts/snapshot_consensus.py TICKER --earnings-date YYYY-MM-DD
"""
from __future__ import annotations

import argparse
import calendar as _calmod
import json
import logging
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

try:
    from zoneinfo import ZoneInfo
    TAIPEI = ZoneInfo("Asia/Taipei")
except Exception:  # pragma: no cover
    TAIPEI = timezone(timedelta(hours=8))

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from dd_meta_reader import iter_dd_metas  # noqa: E402

CALENDAR_JSON = ROOT / "docs" / "catalyst" / "calendar.json"
DD_DIR = ROOT / "docs" / "dd"
SNAP_DIR = ROOT / "docs" / "catalyst" / "snapshots"

# 無自有選擇權鏈、但可用另一標的 ADR 鏈代理隱含波動的 ticker（使用者核可）。
OPTION_PROXY = {"2330.TW": ("TSM", "TSM ADR")}


# ── small utils ───────────────────────────────────────────────────────────────
def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI).isoformat(timespec="seconds")


def _month_end(year: int, month: int) -> date:
    return date(year, month, _calmod.monthrange(year, month)[1])


def _fy_label_year(label: str) -> Optional[int]:
    """FY26 → 2026、FY2026 → 2026。回傳財年截止所在的行事曆年。"""
    digits = "".join(ch for ch in str(label) if ch.isdigit())
    if not digits:
        return None
    try:
        n = int(digits)
    except ValueError:
        return None
    return 2000 + n if n < 100 else n


def _load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _mid(bid, ask, last) -> Optional[float]:
    """買賣中價；bid/ask 任一為 0/None 則退位到 lastPrice。"""
    try:
        b = float(bid) if bid is not None else 0.0
        a = float(ask) if ask is not None else 0.0
    except (TypeError, ValueError):
        b = a = 0.0
    if b > 0 and a > 0:
        return round((b + a) / 2, 4)
    try:
        lv = float(last) if last is not None else 0.0
    except (TypeError, ValueError):
        lv = 0.0
    return round(lv, 4) if lv > 0 else None


# ── earnings-date resolution（硬失敗來源）─────────────────────────────────────
def resolve_earnings_date(ticker: str, override: Optional[str],
                          notes: list) -> Optional[str]:
    """回傳 YYYY-MM-DD 或 None（None → caller 硬失敗）。

    順序：--earnings-date > calendar.json（type=earnings、最近未過期）> yf .calendar。
    """
    if override:
        try:
            date.fromisoformat(override)
            notes.append("財報日：使用 --earnings-date 指定值")
            return override
        except ValueError:
            notes.append(f"--earnings-date 非法（{override!r}），改自動解析")

    # calendar.json 優先
    cal = _load_json(CALENDAR_JSON)
    if cal:
        today = date.today().isoformat()
        cands = [
            e for e in (cal.get("events") or [])
            if e.get("ticker") == ticker and e.get("type") == "earnings"
            and e.get("date")
        ]
        future = sorted(e["date"] for e in cands if e["date"] >= today)
        picked = future[0] if future else (
            sorted((e["date"] for e in cands))[-1] if cands else None)
        if picked:
            notes.append(f"財報日：來自 calendar.json（{picked}）")
            return picked

    # yfinance 退位
    try:
        import yfinance as yf
        c = yf.Ticker(ticker).calendar
        raw = None
        if isinstance(c, dict):
            raw = c.get("Earnings Date")
        elif c is not None and hasattr(c, "loc"):
            try:
                raw = list(c.loc["Earnings Date"])
            except Exception:
                raw = None
        d0 = raw[0] if isinstance(raw, (list, tuple)) and raw else raw
        if isinstance(d0, datetime):
            iso = d0.date().isoformat()
        elif isinstance(d0, date):
            iso = d0.isoformat()
        else:
            import pandas as pd
            iso = pd.Timestamp(d0).date().isoformat()
        if iso:
            notes.append(f"財報日：yfinance calendar 退位（{iso}）")
            return iso
    except Exception as exc:
        notes.append(f"財報日：yfinance calendar 失敗（{str(exc)[:80]}）")
    return None


# ── consensus + price ─────────────────────────────────────────────────────────
def fetch_consensus_and_price(ticker: str, notes: list) -> tuple[dict, Optional[float]]:
    """回傳 (consensus_dict, price)。全部欄位 nullable、honest-fail。"""
    consensus = {"eps": None, "revenue": None, "source": "yfinance",
                 "period": "0q"}
    price = None
    try:
        import yfinance as yf
    except Exception as exc:
        notes.append(f"共識/現價：yfinance import 失敗（{str(exc)[:80]}）")
        return consensus, price

    tk = yf.Ticker(ticker)

    # 共識 EPS（earnings_estimate 0q avg）
    try:
        ee = tk.earnings_estimate
        if ee is not None and not getattr(ee, "empty", True) and "0q" in ee.index:
            v = ee.loc["0q"].get("avg")
            if v is not None and float(v) == float(v):  # not NaN
                consensus["eps"] = round(float(v), 4)
        if consensus["eps"] is None:
            notes.append("共識 EPS：earnings_estimate 0q avg 缺失")
    except Exception as exc:
        notes.append(f"共識 EPS：抓取失敗（{str(exc)[:80]}）")

    # 共識營收（revenue_estimate 0q avg）
    try:
        re_ = tk.revenue_estimate
        if re_ is not None and not getattr(re_, "empty", True) and "0q" in re_.index:
            v = re_.loc["0q"].get("avg")
            if v is not None and float(v) == float(v):
                consensus["revenue"] = float(v)
        if consensus["revenue"] is None:
            notes.append("共識營收：revenue_estimate 0q avg 缺失")
    except Exception as exc:
        notes.append(f"共識營收：抓取失敗（{str(exc)[:80]}）")

    # 現價
    try:
        fi = getattr(tk, "fast_info", None)
        if fi is not None:
            for key in ("last_price", "lastPrice"):
                try:
                    p = fi[key] if not hasattr(fi, "get") else fi.get(key)
                except Exception:
                    p = None
                if p:
                    price = round(float(p), 4)
                    break
        if price is None:
            info = tk.info
            for key in ("regularMarketPrice", "currentPrice", "previousClose"):
                p = info.get(key)
                if p:
                    price = round(float(p), 4)
                    break
        if price is None:
            notes.append("現價：fast_info / info 皆無")
    except Exception as exc:
        notes.append(f"現價：抓取失敗（{str(exc)[:80]}）")

    return consensus, price


# ── ATM straddle implied move ─────────────────────────────────────────────────
def fetch_implied_move(ticker: str, earnings_date: str, price: Optional[float],
                       notes: list) -> tuple[Optional[float], Optional[str],
                                             Optional[str]]:
    """回傳 (implied_move_pct, straddle_expiry, implied_move_proxy)。

    財報日「之後」最近到期的價平 call+put 中價 / spot × 100。無鏈 → null。
    2330.TW → 以 TSM ADR 鏈代理（implied_move_proxy="TSM ADR"，以 TSM spot 計）。
    """
    try:
        import yfinance as yf
    except Exception as exc:
        notes.append(f"隱含波動：yfinance import 失敗（{str(exc)[:80]}）")
        return None, None, None

    opt_ticker = ticker
    proxy = None
    opt_spot = price
    if ticker in OPTION_PROXY:
        opt_ticker, proxy = OPTION_PROXY[ticker]
        opt_spot = None  # 代理標的自有 spot，稍後抓

    tk = yf.Ticker(opt_ticker)

    # 代理標的：改用代理自己的 spot
    if proxy is not None:
        try:
            fi = getattr(tk, "fast_info", None)
            if fi is not None:
                p = fi.get("last_price") if hasattr(fi, "get") else fi["last_price"]
                if p:
                    opt_spot = round(float(p), 4)
            if opt_spot is None:
                opt_spot = float(tk.info.get("regularMarketPrice") or 0) or None
        except Exception:
            opt_spot = None

    if not opt_spot:
        notes.append(f"隱含波動：無 spot 可計算（{opt_ticker}）")
        return None, None, proxy

    try:
        expiries = list(tk.options or [])
    except Exception as exc:
        notes.append(f"隱含波動：無選擇權鏈（{opt_ticker}，{str(exc)[:60]}）")
        return None, None, proxy
    if not expiries:
        notes.append(f"隱含波動：無選擇權鏈（{opt_ticker}；台股常態）")
        return None, None, proxy

    after = sorted(e for e in expiries if e > earnings_date)
    if not after:
        notes.append(f"隱含波動：無財報日（{earnings_date}）之後的到期日")
        return None, None, proxy
    expiry = after[0]

    try:
        chain = tk.option_chain(expiry)
        calls, puts = chain.calls, chain.puts
    except Exception as exc:
        notes.append(f"隱含波動：option_chain({expiry}) 失敗（{str(exc)[:60]}）")
        return None, None, proxy

    def _atm_mid(df) -> Optional[float]:
        if df is None or getattr(df, "empty", True):
            return None
        row = df.iloc[(df["strike"] - opt_spot).abs().argsort()[:1]]
        r = row.iloc[0]
        return _mid(r.get("bid"), r.get("ask"), r.get("lastPrice"))

    call_mid = _atm_mid(calls)
    put_mid = _atm_mid(puts)
    if call_mid is None or put_mid is None:
        notes.append(f"隱含波動：價平 call/put 中價缺失（{expiry}）")
        return None, expiry, proxy

    move = round((call_mid + put_mid) / opt_spot * 100, 2)
    if proxy:
        notes.append(f"隱含波動：以 {proxy} 鏈代理（call+put 中價 / {opt_ticker} spot）")
    return move, expiry, proxy


# ── base_path_ref from dd-meta ────────────────────────────────────────────────
def resolve_base_path_ref(ticker: str, earnings_date: str,
                          notes: list) -> Optional[dict]:
    """讀最新 v13/v14 dd-meta，取財報季所屬財年的 fy_label / base_eps / dd_file。"""
    latest_path = None
    latest_meta = None
    for path, meta in iter_dd_metas(DD_DIR):
        if not str(meta.get("schema", "")).startswith(("v13", "v14")):
            continue
        if meta.get("ticker") != ticker:
            continue
        d = meta.get("date")
        if not d:
            continue
        if latest_meta is None or d > latest_meta.get("date", ""):
            latest_meta, latest_path = meta, path

    if latest_meta is None:
        notes.append(f"base_path_ref：無 {ticker} 的 v13/v14 DD")
        return None

    base_path = latest_meta.get("base_eps_path") or {}
    fy_end_month = latest_meta.get("fy_end_month")
    dd_file = f"/dd/{latest_path.name}"
    if not base_path or not isinstance(fy_end_month, int):
        notes.append(f"base_path_ref：DD 無 base_eps_path/fy_end_month（{dd_file}）")
        return {"fy_label": None, "base_eps": None, "dd_file": dd_file}

    # 財報季所屬財年 = 第一個 fy-end >= 財報日 的財年
    ed = date.fromisoformat(earnings_date)
    target_year = None
    for y in range(ed.year - 1, ed.year + 3):
        if _month_end(y, fy_end_month) >= ed:
            target_year = y
            break

    fy_label, base_eps = None, None
    if target_year is not None:
        for label, eps in base_path.items():
            if _fy_label_year(label) == target_year:
                fy_label, base_eps = label, eps
                break
    if fy_label is None:
        notes.append(f"base_path_ref：base_eps_path 無涵蓋財報季財年（{target_year}）")

    return {"fy_label": fy_label, "base_eps": base_eps, "dd_file": dd_file}


# ── main ──────────────────────────────────────────────────────────────────────
def build(ticker: str, override_date: Optional[str]) -> int:
    ticker = ticker.strip().upper()
    logging.getLogger("yfinance").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)

    notes: list = []
    print(f"=== consensus snapshot · {ticker} · {_now_taipei_iso()} ===")

    earnings_date = resolve_earnings_date(ticker, override_date, notes)
    if not earnings_date:
        print(f"  ✗ 財報日無法解析（calendar.json / yfinance 皆無、且未給 "
              f"--earnings-date）。快照檔名倚賴財報日，中止不寫檔。", file=sys.stderr)
        for n in notes:
            print(f"    · {n}", file=sys.stderr)
        return 2

    ymd = earnings_date.replace("-", "")
    out_path = SNAP_DIR / f"preview_{ticker}_{ymd}.json"
    if out_path.exists():
        print(f"  ✗ 快照已凍結，拒絕覆寫：{out_path}", file=sys.stderr)
        print(f"    賽前錨一旦寫下即不可變。要重做請先人工刪除該檔（並理解你正在"
              f"改寫事後複盤的基準）。", file=sys.stderr)
        return 3

    consensus, price = fetch_consensus_and_price(ticker, notes)
    implied_move_pct, straddle_expiry, implied_move_proxy = fetch_implied_move(
        ticker, earnings_date, price, notes)
    base_path_ref = resolve_base_path_ref(ticker, earnings_date, notes)

    snapshot = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "frozen_at": _now_taipei_iso(),
        "consensus": consensus,
        "price": price,
        "implied_move_pct": implied_move_pct,
        "implied_move_proxy": implied_move_proxy,
        "straddle_expiry": straddle_expiry,
        "base_path_ref": base_path_ref,
        "notes": notes,
    }

    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2),
                        encoding="utf-8")

    # console summary
    print(f"  財報日      : {earnings_date}")
    print(f"  共識 EPS    : {consensus['eps']}   營收: {consensus['revenue']}")
    print(f"  現價        : {price}")
    print(f"  隱含波動 %  : {implied_move_pct}"
          f"{f'  (proxy={implied_move_proxy})' if implied_move_proxy else ''}"
          f"  到期: {straddle_expiry}")
    print(f"  base_path_ref: {base_path_ref}")
    if notes:
        print("  notes:")
        for n in notes:
            print(f"    · {n}")
    print(f"  ✓ Wrote {out_path} ({out_path.stat().st_size:,} B)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ticker", help="標的代號（如 TSM、2330.TW）")
    p.add_argument("--earnings-date", default=None,
                   help="強制指定財報日 YYYY-MM-DD（否則自動解析）")
    args = p.parse_args()
    return build(args.ticker, args.earnings_date)


if __name__ == "__main__":
    sys.exit(main())
