#!/usr/bin/env python3
"""每日 Koyfin 抓取的三塊共用邏輯（2026-10-21）：

  1. 閘門逐檔處理（取代「任何一檔超過 35% 就整批停」）
  2. 每日 EPS 快照（data/eps-estimates/daily/{dd,smallcap,tw}/YYYY-MM-DD.json）
  3. 「財報後」基準挑選、「財報後第 k 天」對位

stdlib + load_eps_estimates_xlsx（只讀 xlsx，不需要 openpyxl），python3 與 python3.12 都能 import。
網路查詢（財報日）全部走可注入的函式，單元測試不碰網路。

閘門規則（持有人 2026-10-21 拍板）：
  a. 前後兩次 FY1 絕對值都小於 0.10（美元）：不算異常，記在 tiny_eps_skipped。
  b. 被標的股票在最近 3 個交易日內發過財報：收下新值，記在 accepted_after_earnings
     （「財報後大幅修正」）。美股家族看美股交易日，台股家族看台股交易日。
  c. 其他被標的股票：EPS 預估相關欄位（HELD_COLUMNS）沿用前一份 xlsx 的值，其他欄位用新值，
     記在 held。同一檔連續兩次每日抓取的新 FY1 相差在 1% 以內，就收下（released_after_2_days）。
  d. 同一家族 held 檔數超過 max(10, 列數的 5%)：視為整批抓壞，exit 6。
  e. 每次執行寫一份 gate report JSON。
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import market_sessions as ms  # noqa: E402

ROOT = SCRIPTS_DIR.parent
GATE_DIR = ROOT / "data" / "eps-estimates" / "gate"
HELD_STATE_PATH = GATE_DIR / "held_state.json"

FY1_GATE_PCT = 35.0
TINY_EPS_ABS = 0.10
EARNINGS_WINDOW_TRADING_DAYS = 3
RELEASE_TOLERANCE = 0.01
HELD_MAX_ABS = 10
HELD_MAX_FRAC = 0.05
RELEASE_MAX_GAP_DAYS = 5     # 前一次被標到的日期離今天不超過這麼多天，才算「連續兩次」

# 原始 txt 欄位位置（koyfin_xlsx_from_raw.build_row）→ ExcelSnapshot 欄位名 → xlsx 欄名。
# 這六欄由分析師預估推導；其餘（價格、目標價、財報數字、品質欄位）都不沿用舊值。
HELD_COLUMNS = [
    (1, "fy1", "FY1E EPS"),
    (2, "fy2", "FY2E EPS"),
    (3, "fy3", "FY3E EPS"),
    (37, "pe_ntm_x", "PE NTM x"),
    (48, "est_rev_cagr_3y_pct", "Est Rev CAGR 3Y %"),
    (49, "est_eps_cagr_3y_pct", "Est EPS CAGR 3Y %"),
]

# 家族 → 月快照目錄（相對 docs/dd-screener）與每日快照的合併群組（每日快照目錄見 daily_dir）
SNAPSHOT_GROUPS = {
    "dd": {"families": ["screener", "largecap"], "dir": "eps-estimates-snapshots"},
    "smallcap": {"families": ["smallcap"], "dir": "smallcap/eps-estimates-snapshots"},
    "tw": {"families": ["tw"], "dir": "tw/eps-estimates-snapshots"},
}
DD_SCREENER_DIR = ROOT / "docs" / "dd-screener"


def family_market(family_key: str) -> str:
    return "TW" if family_key == "tw" else "US"


# ---------------------------------------------------------------------------
# 1. 閘門
# ---------------------------------------------------------------------------

def is_tiny_eps(prev_v, new_v) -> bool:
    return abs(prev_v) < TINY_EPS_ABS and abs(new_v) < TINY_EPS_ABS


def reported_within_window(report_dates, market: str, ref_session, n: int = EARNINGS_WINDOW_TRADING_DAYS) -> bool:
    """report_dates 裡有沒有一天落在「最近 n 個交易日」（以 ref_session 為最後一天，含 ref_session）。
    ref_session = 抓取當下最近一個已收盤的交易日。財報日晚於 ref_session 不算（資料還沒包含）。"""
    ref = ms._to_date(ref_session)
    for d in report_dates or []:
        try:
            d = ms._to_date(d)
        except ValueError:
            continue
        if d <= ref and ms.sessions_elapsed(market, d, ref) <= n - 1:
            return True
    return False


def resolve_flagged(flagged: list[dict], *, family_key: str, today: str, state_before: dict,
                    report_dates_for, ref_session) -> dict:
    """把閘門標出的股票分成三類，並算出下一份 held 狀態。

    flagged: [{"ticker","prev_fy1","new_fy1","pct_move","sign_flip"}]
    state_before: {ticker: {"history": [{"date","new_fy1"}...]}}（前一天跑完的狀態）
    report_dates_for(ticker) -> list[date-like]（只對被標的股票查，查不到回空 list）
    """
    market = family_market(family_key)
    today_d = ms._to_date(today)
    accepted, held, released = [], [], []
    state_after: dict = {}
    for r in flagged:
        t = r["ticker"]
        prior = [h for h in (state_before.get(t) or {}).get("history", []) if h["date"] < today]
        last = prior[-1] if prior else None

        dates = report_dates_for(t)
        if reported_within_window(dates, market, ref_session):
            recent = sorted(ms._to_date(d) for d in dates if ms._to_date(d) <= ms._to_date(ref_session))
            accepted.append({**r, "report_date": recent[-1].isoformat() if recent else None})
            continue

        if last and (today_d - ms._to_date(last["date"])).days <= RELEASE_MAX_GAP_DAYS \
                and last["new_fy1"] not in (None, 0) \
                and abs(r["new_fy1"] - last["new_fy1"]) <= RELEASE_TOLERANCE * abs(last["new_fy1"]):
            released.append({**r, "first_seen": last["date"], "first_seen_new_fy1": last["new_fy1"]})
            continue

        held.append(r)
        state_after[t] = {"history": ([prior[-1]] if prior else []) + [{"date": today, "new_fy1": r["new_fy1"]}]}
    return {"accepted_after_earnings": accepted, "held": held,
            "released_after_2_days": released, "state_after": state_after}


def held_limit(n_rows: int) -> float:
    return max(HELD_MAX_ABS, HELD_MAX_FRAC * n_rows)


def load_held_state(family_key: str, today: str, path: Path | None = None) -> tuple[dict, bool]:
    """(這次執行的起始狀態, 可寫入)。同一天重跑用當天第一次跑之前的狀態（冪等）；
    檔案日期比 today 晚（補跑舊日期）時用空狀態、不寫回。"""
    p = path or HELD_STATE_PATH
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        doc = {}
    fam = doc.get(family_key) or {}
    as_of = fam.get("as_of")
    if not as_of:
        return {}, True
    if as_of == today:
        return fam.get("before") or {}, True
    if as_of < today:
        return fam.get("after") or {}, True
    return {}, False


def save_held_state(family_key: str, today: str, before: dict, after: dict, path: Path | None = None) -> None:
    p = path or HELD_STATE_PATH
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        doc = {}
    doc[family_key] = {"as_of": today, "before": before, "after": after}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def _fmt_raw_num(v) -> str:
    return "-" if v is None else f"{float(v):.6f}"


def apply_held_to_raw_lines(lines: list[str], held_tickers: set[str], prev_snapshot) -> list[str]:
    """held 檔的 HELD_COLUMNS 換成前一份 xlsx 的值（其餘欄位原樣）。回傳新的原始 txt 行。"""
    out = []
    for line in lines:
        f = line.split("|")
        if f and f[0] in held_tickers and len(f) > max(i for i, _, _ in HELD_COLUMNS):
            prev = prev_snapshot.get(f[0]) or {}
            for idx, key, _ in HELD_COLUMNS:
                f[idx] = _fmt_raw_num(prev.get(key))
            line = "|".join(f)
        out.append(line)
    return out


def write_gate_report(report_dir: Path, date_str: str, family_key: str, family_report: dict) -> Path:
    """gate_report_YYYYMMDD.json 裝所有家族；同一天重跑只覆蓋該家族的區塊。另存 gate_report_latest.json。"""
    report_dir.mkdir(parents=True, exist_ok=True)
    p = report_dir / f"gate_report_{date_str}.json"
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        doc = {"date": date_str, "families": {}}
    doc["families"][family_key] = family_report
    text = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    p.write_text(text, encoding="utf-8")
    (report_dir / "gate_report_latest.json").write_text(text, encoding="utf-8")
    return p


# ---- 財報日查詢（預設實作，可注入替換） --------------------------------------

def make_report_dates_lookup(family_key: str, today_d: date):
    """回傳 f(ticker) -> [date,...]（已發布財報日）。只在被標的股票上呼叫，失敗回空 list。
    美股：yfinance get_earnings_dates 有 Reported EPS 的列。台股：.TW／.TWO 都試，
    再補公開資訊觀測站董事會通過日。"""
    mops_cache: dict = {}

    def _yf_dates(sym: str) -> list[date]:
        try:
            import yfinance as yf
            ed = yf.Ticker(sym).get_earnings_dates(limit=12)
            if ed is None or ed.empty:
                return []
            idx = ed.index
            if getattr(idx, "tz", None) is not None:
                idx = idx.tz_localize(None)
            mask = ed["Reported EPS"].notna().to_numpy() if "Reported EPS" in ed.columns else [False] * len(ed)
            return [ts.date() for ts, m in zip(idx, mask) if m and ts.date() <= today_d]
        except Exception:  # noqa: BLE001
            return []

    def lookup(ticker: str) -> list[date]:
        if family_key != "tw":
            return _yf_dates(ticker)
        out: list[date] = []
        for suf in (".TW", ".TWO"):
            out = _yf_dates(ticker + suf)
            if out:
                break
        try:
            import tw_mops_earnings
            ap = tw_mops_earnings.prefetch([ticker], mops_cache, today_d).get(ticker) or {}
            out += [date.fromisoformat(v) for v in ap.values() if date.fromisoformat(v) <= today_d]
        except Exception:  # noqa: BLE001
            pass
        return out

    return lookup


# ---------------------------------------------------------------------------
# 2. 每日 EPS 快照
# ---------------------------------------------------------------------------

# 每日快照放 data/（不發布到網站）：data/eps-estimates/daily/{dd,smallcap,tw}/YYYY-MM-DD.json
DAILY_SNAPSHOT_ROOT = ROOT / "data" / "eps-estimates" / "daily"


def daily_dir(group: str, root: Path | None = None) -> Path:
    return (root or DAILY_SNAPSHOT_ROOT) / group


def snapshot_record(rec: dict) -> dict:
    """ExcelSnapshot 一檔的記錄 → 每日快照的一列（欄位名與月快照相同，只留修正率會讀的）。"""
    fy1, fy3 = rec.get("fy1"), rec.get("fy3")
    cagr = rec.get("cagr_fy1_fy3_pct")
    if cagr is None and fy1 and fy3 and fy1 > 0 and fy3 > 0:
        cagr = ((fy3 / fy1) ** 0.5 - 1) * 100
    return {
        "eps_fy_curr": fy1, "eps_fy_next": rec.get("fy2"), "eps_fy3": fy3,
        "eps_cagr_2y": None if cagr is None else round(float(cagr), 2),
        "source": "xlsx",
    }


def _latest_monthly_keys(group: str, docs_dir: Path | None = None) -> list[str]:
    d = (docs_dir or DD_SCREENER_DIR) / SNAPSHOT_GROUPS[group]["dir"]
    best = None
    for p in d.glob("????-??.json"):
        if best is None or p.name > best.name:
            best = p
    if best is None:
        return []
    try:
        return list((json.loads(best.read_text(encoding="utf-8")).get("tickers") or {}).keys())
    except (OSError, ValueError):
        return []


def build_daily_snapshot(group: str, excels: list, *, scraped_at_utc: str, source_files: list[str],
                         docs_dir: Path | None = None, tw_resolver=None) -> dict:
    """excels: 同一群組各家族的 ExcelSnapshot（排在前面的優先）。"""
    snap_date = excels[0].snapshot_date
    tickers: dict = {}
    if group == "tw":
        monthly = {k.split(".")[0]: k for k in _latest_monthly_keys(group, docs_dir)}
        codes = sorted({c for ex in excels for c in ex.tickers})
        unknown = [c for c in codes if c not in monthly]
        if unknown:
            try:
                if tw_resolver is None:
                    from tw_listing_suffix import resolve_tw_codes as tw_resolver
                resolved, _ = tw_resolver(unknown)
                monthly.update({c: r["ticker"] for c, r in resolved.items()})
            except Exception as exc:  # noqa: BLE001
                print(f"  WARN: TW 代號解析失敗，這些代號不進每日快照: {unknown} ({exc})", file=sys.stderr)
        for c in codes:
            key = monthly.get(c)
            if not key:
                continue
            for ex in excels:
                rec = ex.tickers.get(c)
                if rec:
                    tickers[key] = snapshot_record(rec)
                    break
    else:
        keys = set(_latest_monthly_keys(group, docs_dir))
        for ex in excels:
            keys |= set(ex.tickers)
        for k in sorted(keys):
            for ex in excels:
                rec = ex.get(k)
                if rec:
                    tickers[k] = snapshot_record(rec)
                    break
    return {
        "kind": "daily", "snapshot_date": snap_date, "scraped_at_utc": scraped_at_utc,
        "for_month": snap_date[:7], "source": "xlsx", "source_files": source_files,
        "universe_size": len(tickers), "tickers": tickers,
    }


def write_daily_snapshot(path: Path, doc: dict) -> None:
    """同一天重跑覆蓋；只部分家族重跑時（--only）保留同日檔裡其他家族的列。"""
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
            if old.get("snapshot_date") == doc["snapshot_date"]:
                merged = dict(old.get("tickers") or {})
                merged.update(doc["tickers"])
                doc = {**doc, "tickers": merged, "universe_size": len(merged),
                       "source_files": sorted(set(old.get("source_files") or []) | set(doc["source_files"]))}
        except (OSError, ValueError):
            pass
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def load_daily_snapshots(directory: Path) -> dict:
    """{YYYY-MM-DD: snapshot}。壞檔略過。"""
    out: dict = {}
    if not directory.exists():
        return out
    for p in sorted(directory.glob("????-??-??.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if d.get("scraped_at_utc") and d.get("snapshot_date"):
            out[p.stem] = d
    return out


# ---------------------------------------------------------------------------
# 3. 基準挑選與第 k 天對位
# ---------------------------------------------------------------------------

BASELINE_MAX_DAYS = 10
US_BASELINE_CUTOFF_UTC_HOUR = 10          # 財報日 10:00 UTC（美股盤前之前）
TW_BASELINE_CUTOFF = (5, 30)              # 財報日 13:30 台北 = 05:30 UTC（台股收盤）


def _parse_utc(s: str) -> datetime | None:
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def baseline_cutoff_utc(earnings_date, market: str) -> datetime:
    d = ms._to_date(earnings_date)
    h, m = (TW_BASELINE_CUTOFF if market == "TW" else (US_BASELINE_CUTOFF_UTC_HOUR, 0))
    return datetime(d.year, d.month, d.day, h, m, tzinfo=timezone.utc)


def pick_daily_baseline(daily_snapshots: dict | None, earnings_date, market: str,
                        max_days: int = BASELINE_MAX_DAYS) -> dict | None:
    """財報前最後一份每日快照：scraped_at_utc 早於財報日截止時間，且 snapshot_date 離財報日不超過
    max_days 個日曆天。沒有就回 None（呼叫端退回月快照）。"""
    if not daily_snapshots or not earnings_date:
        return None
    try:
        e = ms._to_date(earnings_date)
    except ValueError:
        return None
    cutoff = baseline_cutoff_utc(e, market)
    best, best_ts = None, None
    for snap in daily_snapshots.values():
        ts = _parse_utc(snap.get("scraped_at_utc"))
        if ts is None or ts >= cutoff:
            continue
        try:
            sd = ms._to_date(snap.get("snapshot_date"))
        except ValueError:
            continue
        if (e - sd).days > max_days:
            continue
        if best_ts is None or ts > best_ts:
            best, best_ts = snap, ts
    return best


def reaction_day(market: str, earnings_date, timing: str | None) -> date:
    """財報公布後第一個交易日 R。盤前（BMO）＝財報日當天；盤後、時間不明、台股＝財報日的下一個交易日。"""
    e = ms._to_date(earnings_date)
    if timing == "BMO" and market != "TW":
        return ms.first_session_on_or_after(market, e)
    return ms.next_session(market, e)


def day_k_cutoff_utc(market: str, r_day, k: int) -> datetime:
    """第 k 天的門檻時刻＝交易日 R+k-1 的收盤。"""
    d = ms._to_date(r_day)
    for _ in range(k - 1):
        d = ms.next_session(market, d)
    return ms.close_utc(market, d)


def first_snapshot_after(daily_snapshots: dict | None, cutoff_utc: datetime) -> dict | None:
    best, best_ts = None, None
    for snap in (daily_snapshots or {}).values():
        ts = _parse_utc(snap.get("scraped_at_utc"))
        if ts is None or ts <= cutoff_utc:
            continue
        if best_ts is None or ts < best_ts:
            best, best_ts = snap, ts
    return best


def post_earnings_snapshots(daily_snapshots: dict | None, market: str, earnings_date, timing: str | None,
                            days: int = 2) -> dict:
    """{"reaction_day","before","day1","day2"}：每一項是快照 dict 或 None。"""
    r = reaction_day(market, earnings_date, timing)
    out = {"reaction_day": r, "before": pick_daily_baseline(daily_snapshots, earnings_date, market)}
    for k in range(1, days + 1):
        out[f"day{k}"] = first_snapshot_after(daily_snapshots, day_k_cutoff_utc(market, r, k))
    return out


def reaction_in_recent_window(market: str, r_day, now_utc: datetime, n: int = 5) -> bool:
    """R 是否落在「最近 n 個已收盤交易日」或是下一個尚未收盤的交易日（剛發完、等第 1 天）。"""
    ref = ms.latest_closed_session(market, now_utc)
    r = ms._to_date(r_day)
    if r > ref:
        return r == ms.next_session(market, ref)
    return ms.sessions_elapsed(market, r, ref) <= n - 1


# ---------------------------------------------------------------------------
# 4. 近期財報修正（財報前／第 1 天／第 2 天）
# ---------------------------------------------------------------------------

POST_EARNINGS_WINDOW_SESSIONS = 5
_FY_KEYS = ("eps_fy_curr", "eps_fy_next", "eps_fy3")


def timing_label(market: str, timing: str | None) -> str:
    if market == "TW":
        return "盤後（假設）"
    return {"BMO": "盤前", "AMC": "盤後"}.get(timing or "", "時間不明（當盤後）")


def _snap_eps(snapshot: dict | None, ticker: str, fy_args: dict, year: int, adr_fn):
    """某份快照裡，日曆年 year 對應的 EPS（美元，已套 ADR 比例）。查不到回 None。"""
    if not snapshot:
        return None
    row = (snapshot.get("tickers") or {}).get(ticker)
    if not row:
        return None
    import eps_fy_shift as fys
    fy1_end = fys.snapshot_fy1_end(fy_args.get("last_fye"), snapshot.get("snapshot_date"),
                                   fy_args.get("past_earnings_dates"), row.get("source"),
                                   fy_args.get("last_earnings_date"))
    if fy1_end is None:
        return None
    col = fys.calendar_year_columns(fy1_end, [year]).get(year)
    if not col:
        return None
    v = row.get(_FY_KEYS[col - 1])
    if v is None:
        return None
    adj = adr_fn(ticker, {"fy1": v})
    return adj.get("fy1") if adj else v


def compute_post_earnings_tracks(rows: list[dict], *, daily_snapshots: dict, years: tuple[int, int],
                                 now_utc: datetime, market_for, currency_for=None, fx_for=None,
                                 adr_fn=None, window_sessions: int = POST_EARNINGS_WINDOW_SESSIONS) -> dict:
    """每檔財報後 EPS 預估的逐日變化。

    rows: latest.json 的 stocks（要有 ticker、last_earnings_date、last_earnings_time、
          fiscal_year_end、past_earnings_dates）。years: 頁面的兩個條件年（日曆年）。
    market_for(row) -> "US"/"TW"。currency_for(ticker) -> 財報幣別或 None；
    fx_for(ccy, date_str) -> 當日 1 美元兌本幣或 None。外幣公司若三份快照都查得到匯率，
    就換成財報幣別比較（避免匯率波動被當成修正）；否則用美元。
    回傳 {"tracks": {ticker: track}, "recent": [track...], "no_baseline": [ticker...]}。
    """
    if adr_fn is None:
        from load_eps_estimates_xlsx import apply_adr_ratio as adr_fn
    tracks: dict = {}
    no_baseline: list = []
    for row in rows:
        e = row.get("last_earnings_date")
        if not e:
            continue
        market = market_for(row)
        timing = None if market == "TW" else row.get("last_earnings_time")
        try:
            r_day = reaction_day(market, e, timing)
        except ValueError:
            continue
        if not reaction_in_recent_window(market, r_day, now_utc, window_sessions):
            continue
        t = row["ticker"]
        snaps = post_earnings_snapshots(daily_snapshots, market, e, timing)
        if not snaps["before"] or t not in (snaps["before"].get("tickers") or {}):
            no_baseline.append(t)
            continue

        fy_args = {"last_fye": row.get("fiscal_year_end"), "past_earnings_dates": row.get("past_earnings_dates"),
                   "last_earnings_date": e}
        chosen = [("before", snaps["before"]), ("day1", snaps["day1"]), ("day2", snaps["day2"])]
        ccy, fx = "USD", {}
        c = currency_for(t) if currency_for else None
        if c and c.upper() != "USD" and fx_for:
            rates = {name: fx_for(c.upper(), s["snapshot_date"]) for name, s in chosen if s}
            if rates and all(v for v in rates.values()):
                ccy, fx = c.upper(), rates

        out_years = []
        for y in years:
            vals = {}
            for name, s in chosen:
                v = _snap_eps(s, t, fy_args, y, adr_fn)
                if v is not None and ccy != "USD":
                    v = v * fx[name]
                vals[name] = None if v is None else round(v, 4)
            base = vals["before"]
            last_day = "day2" if vals["day2"] is not None else ("day1" if vals["day1"] is not None else None)
            chg = None
            if base is not None and base > 0 and last_day:
                chg = round((vals[last_day] / base - 1) * 100, 2)
            out_years.append({"year": y, "before": vals["before"], "day1": vals["day1"], "day2": vals["day2"],
                              "change_pct": chg, "change_day": {"day1": 1, "day2": 2}.get(last_day)})
        tracks[t] = {
            "ticker": t, "name": row.get("name"), "market": market,
            "last_earnings_date": e, "timing": timing_label(market, timing),
            "reaction_day": r_day.isoformat(), "ccy": ccy,
            "before_snapshot": snaps["before"]["snapshot_date"],
            "day1_snapshot": snaps["day1"]["snapshot_date"] if snaps["day1"] else None,
            "day2_snapshot": snaps["day2"]["snapshot_date"] if snaps["day2"] else None,
            "years": out_years,
        }
    recent = sorted(tracks.values(), key=lambda x: (x["reaction_day"], x["ticker"]), reverse=True)
    return {"tracks": tracks, "recent": recent, "no_baseline": sorted(no_baseline)}
