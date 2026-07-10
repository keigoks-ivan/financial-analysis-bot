#!/usr/bin/env python3
"""前瞻催化劑日曆 — 資料建構器（Phase 2）.

把三個來源的「未來事件」收斂成單一 forward calendar：

  1. yfinance 下次財報日（Ticker.calendar，mimic sop_funnel/earnings_guard 的
     per-ticker 7 天 TTL cache 模式，但用**獨立** cache 檔，不碰 sop-funnel 的）。
     timestamp → 轉 US/Eastern 後取日期。查詢失敗 → 記 errors[]，退回來源 2。
  2. DD §15 靜態解析：財報日期 row 的 ISO 日期（yfinance 失敗時的備援財報日，
     標 source=s15_static、註「可能過期」）＋ 保質期日期 → 若在 30 天內或已過，
     emit 一筆 dd_expiry（報告保質期屆滿警示）。
  3. dd-meta 的 catalysts[] 陣列 → source=dd-meta 的結構化事件。格式錯誤的項目
     skip-and-log 進 skipped[]。

宇宙：v13/v14 latest-per-ticker dd-meta，且（DD 日期距今 ≤ 90 天）或
（dca_verdict == 進場）。

誠實失敗：若本次執行**每一個** yfinance 呼叫都失敗，保留上一版 calendar.json
的前瞻事件並把 stale 設為 true；絕不捏造日期，絕不無聲清空檔案。

輸出：
  docs/catalyst/calendar.json        前瞻事件（date >= today）
  docs/catalyst/archive.json         已過事件（date < today），read-modify-write
                                     merge by id；outcome / outcome_note /
                                     ledger_ref 三欄為人工所有，永不覆寫
  docs/catalyst/earnings_cache.json  yfinance 財報日 cache（獨立於 sop-funnel）

Usage:
  python3 scripts/build_catalyst_calendar.py
  python3 scripts/build_catalyst_calendar.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    EASTERN = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover — zoneinfo always present on 3.9+
    EASTERN = None

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dd_meta_reader import iter_dd_metas  # noqa: E402

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DD_DIR = ROOT / "docs" / "dd"
OUT_DIR = ROOT / "docs" / "catalyst"
CALENDAR_JSON = OUT_DIR / "calendar.json"
ARCHIVE_JSON = OUT_DIR / "archive.json"
CACHE_JSON = OUT_DIR / "earnings_cache.json"

# ── constants ─────────────────────────────────────────────────────────────────
TAIPEI = timezone(timedelta(hours=8))
CACHE_TTL_DAYS = 7
UNIVERSE_DD_WINDOW_DAYS = 90
DD_EXPIRY_WARN_DAYS = 30            # 保質期距今 ≤ 此值（含已過）才 emit dd_expiry

# dd-meta catalyst 的 type 白名單；未知 → other
VALID_TYPES = {
    "earnings", "dd_expiry", "product", "regulatory",
    "capacity", "guidance", "macro", "other",
}
# 人工所有、cron 永不覆寫的 archive 欄位
HUMAN_OWNED = ("outcome", "outcome_note", "ledger_ref")

_ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


# ── small utils ───────────────────────────────────────────────────────────────

def _norm_dca_role(role):
    """v14.12 四值歸一（核心/衛星/追蹤/不持有）；legacy 值映射，canonical 定義見 aggregate_dca_stats._categorize。"""
    r = (role or "").strip()
    if not r:
        return r
    if r in ("核心", "衛星", "追蹤", "不持有"):
        return r
    if "候選" in r or "追蹤池" in r:
        return "追蹤"
    if r.startswith(("不持有", "暫不持有", "迴避")):
        return "不持有"
    if "核心" in r:
        return "核心"
    if "衛星" in r or "投機" in r or r.lower().startswith("satellite"):
        return "衛星"
    return r

def _today() -> date:
    return date.today()


def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI).isoformat(timespec="seconds")


def _load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _parse_iso(s: str):
    if not s or not isinstance(s, str):
        return None
    m = _ISO_RE.search(s)
    if not m:
        return None
    try:
        return date.fromisoformat(m.group(0))
    except ValueError:
        return None


def _is_v13_v14(meta: dict) -> bool:
    return str(meta.get("schema", "")).startswith(("v13", "v14"))


# ── universe ──────────────────────────────────────────────────────────────────
def build_universe() -> list[tuple[Path, dict]]:
    """v13/v14 latest-per-ticker，且（DD ≤ 90 天）或（進場）。回傳 [(path, meta)]."""
    today = _today()
    latest: dict[str, tuple[Path, dict]] = {}
    for path, meta in iter_dd_metas(DD_DIR):
        if not _is_v13_v14(meta):
            continue
        t, d = meta.get("ticker"), meta.get("date")
        if not t or not d:
            continue
        prev = latest.get(t)
        if prev is None or d > prev[1]["date"]:
            latest[t] = (path, meta)

    out = []
    for path, meta in latest.values():
        dd_date = _parse_iso(meta.get("date", ""))
        recent = dd_date is not None and (today - dd_date).days <= UNIVERSE_DD_WINDOW_DAYS
        entering = meta.get("dca_verdict") == "進場"
        if recent or entering:
            out.append((path, meta))
    out.sort(key=lambda pm: pm[1]["ticker"])
    return out


# ── source 1: yfinance next earnings (independent cache) ──────────────────────
def _to_eastern_iso(d0) -> str | None:
    """把 yfinance 回傳的日期物件轉成 US/Eastern 的 YYYY-MM-DD."""
    if d0 is None:
        return None
    # datetime（可能帶 tz）
    if isinstance(d0, datetime):
        dt = d0
        if dt.tzinfo is not None and EASTERN is not None:
            dt = dt.astimezone(EASTERN)
        return dt.date().isoformat()
    # 純日期
    if isinstance(d0, date):
        return d0.isoformat()
    # pandas Timestamp / 字串
    try:
        import pandas as pd
        ts = pd.Timestamp(d0)
        if ts.tzinfo is not None and EASTERN is not None:
            ts = ts.tz_convert(EASTERN)
        return ts.date().isoformat()
    except Exception:
        m = _ISO_RE.search(str(d0))
        return m.group(0) if m else None


def _fetch_next_earnings(ticker: str) -> str:
    """yfinance 下次財報日（YYYY-MM-DD）；查無 / 失敗 raise。"""
    import yfinance as yf
    cal = yf.Ticker(ticker).calendar
    dates = None
    if isinstance(cal, dict):
        dates = cal.get("Earnings Date")
    elif cal is not None and hasattr(cal, "loc"):
        try:
            dates = list(cal.loc["Earnings Date"])
        except Exception:
            dates = None
    if not dates:
        raise RuntimeError("calendar 無 Earnings Date")
    d0 = dates[0] if isinstance(dates, (list, tuple)) else dates
    iso = _to_eastern_iso(d0)
    if not iso:
        raise RuntimeError(f"無法解析財報日: {d0!r}")
    return iso


def earnings_from_yf(ticker: str, cache: dict, stats: dict) -> tuple[str | None, str]:
    """回傳 (next_earnings_iso | None, source_kind)。

    source_kind ∈ cache | fetched | error。只有真正發網路請求才計入
    stats['attempted'] / stats['failed']（cache 命中不計）。
    """
    now = datetime.now(timezone.utc)
    rec = cache.get(ticker)
    if rec:
        try:
            age = (now - datetime.fromisoformat(rec["fetched"])).days
        except Exception:
            age = CACHE_TTL_DAYS + 1
        if age <= CACHE_TTL_DAYS:
            return rec.get("next_earnings"), "cache"
    stats["attempted"] += 1
    try:
        ne = _fetch_next_earnings(ticker)
    except Exception as exc:
        stats["failed"] += 1
        cache[ticker] = {"next_earnings": None, "fetched": now.isoformat(),
                         "error": str(exc)[:140]}
        return None, "error"
    cache[ticker] = {"next_earnings": ne, "fetched": now.isoformat()}
    return ne, "fetched"


# ── source 2: DD §15 static parse ─────────────────────────────────────────────
def parse_s15(path: Path) -> dict:
    """回傳 {earnings_iso, expiry_iso}（任一可能為 None）。防禦式解析，失敗 → None。"""
    out = {"earnings_iso": None, "expiry_iso": None}
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return out
    i = text.find('id="s15"')
    if i < 0:
        return out
    seg = text[i:i + 6000]
    j = seg.find("<details")          # 附錄 A 之前為 §15 本體
    if j > 0:
        seg = seg[:j]
    # 財報日期 row（類型欄含「財報日期」）
    erow = re.search(r"<tr>(?:(?!</tr>).)*財報日期.*?</tr>", seg, re.S)
    if erow:
        m = _ISO_RE.search(erow.group(0))
        if m:
            out["earnings_iso"] = m.group(0)
    # 保質期段落（用冒號區隔 §15 標題裡的「保質期」）
    bao = re.search(r"保質期[：:].{0,140}", seg, re.S)
    if bao:
        m = _ISO_RE.search(bao.group(0))
        if m:
            out["expiry_iso"] = m.group(0)
    return out


# ── event constructors ────────────────────────────────────────────────────────
def _positioning(meta: dict) -> dict:
    return {
        "dca_verdict": meta.get("dca_verdict"),
        "dca_role": _norm_dca_role(meta.get("dca_role")),
        "holding": None,
    }


def _dd_file(path: Path) -> str:
    return f"/dd/{path.name}"


def _make_event(ticker, date_iso, event, etype, impact, source, meta, path,
                watch="", extra=None) -> dict:
    etype = etype if etype in VALID_TYPES else "other"
    ev = {
        "id": f"{ticker}|{date_iso}|{etype}",
        "date": date_iso,
        "ticker": ticker,
        "event": event,
        "type": etype,
        "impact": impact,
        "source": source,
        "positioning": _positioning(meta),
        "dd_file": _dd_file(path),
        "watch": watch or "",
    }
    if extra:
        ev.update(extra)
    return ev


# ── main build ────────────────────────────────────────────────────────────────
def build_events(universe, cache, stats, skipped, errors):
    """對宇宙每檔跑三來源，回傳 events（未排序、含過去與未來）。"""
    events = []
    today = _today()
    for path, meta in universe:
        ticker = meta["ticker"]
        s15 = parse_s15(path)

        # ── 來源 1：yfinance 財報日 ──
        ne, kind = earnings_from_yf(ticker, cache, stats)
        if ne:
            events.append(_make_event(
                ticker, ne, "下一次財報（yfinance 預估）", "earnings", "高",
                "yfinance", meta, path,
                watch="財報前 5 個交易日靜默期禁新倉；財報後以新數據重估裁決。"))
        else:
            errors.append({"ticker": ticker, "source": "yfinance",
                           "reason": "無法取得下次財報日（查詢失敗或無資料）"})
            # ── 來源 2 備援：§15 靜態財報日 ──
            if s15["earnings_iso"]:
                events.append(_make_event(
                    ticker, s15["earnings_iso"], "下一次財報（§15 靜態，可能過期）",
                    "earnings", "高", "s15_static", meta, path,
                    watch="yfinance 未取得，改用 DD §15 靜態日期，可能已過期，僅供參考。"))

        # ── 來源 2：DD 保質期 → dd_expiry（30 天內或已過才 emit）──
        exp = _parse_iso(s15["expiry_iso"]) if s15["expiry_iso"] else None
        if exp is not None and (exp - today).days <= DD_EXPIRY_WARN_DAYS:
            events.append(_make_event(
                ticker, exp.isoformat(),
                "DD 保質期屆滿 — 裁決需複審", "dd_expiry", "中",
                "s15_static", meta, path,
                watch="保質期後 §14 裁決可能失效，重跑 stock-analyst 複審。"))

        # ── 來源 3：dd-meta catalysts[] ──
        for idx, c in enumerate(meta.get("catalysts") or []):
            if not isinstance(c, dict):
                skipped.append({"ticker": ticker, "index": idx,
                                "reason": "catalyst 非物件"})
                continue
            cdate = _parse_iso(c.get("date", ""))
            if cdate is None:
                skipped.append({"ticker": ticker, "index": idx,
                                "reason": f"date 缺失或非 ISO: {c.get('date')!r}"})
                continue
            if not c.get("event"):
                skipped.append({"ticker": ticker, "index": idx,
                                "reason": "event 欄缺失"})
                continue
            extra = {}
            if c.get("date_precision"):
                extra["date_precision"] = c["date_precision"]
            events.append(_make_event(
                ticker, cdate.isoformat(), c["event"], c.get("type", "other"),
                c.get("impact", ""), "dd-meta", meta, path,
                watch=c.get("watch", ""), extra=extra))
    return events


def merge_archive(past_events, dry_run=False):
    """read-modify-write merge by id。人工欄位（outcome / outcome_note /
    ledger_ref）永不覆寫；新記錄這三欄設 null。回傳 merged archive dict。"""
    arch = _load_json(ARCHIVE_JSON) or {}
    by_id: dict[str, dict] = {e["id"]: e for e in (arch.get("events") or [])
                              if isinstance(e, dict) and "id" in e}
    for pe in past_events:
        eid = pe["id"]
        if eid in by_id:
            rec = by_id[eid]
            preserved = {k: rec.get(k) for k in HUMAN_OWNED}
            rec.update(pe)                 # 刷新描述性欄位
            rec.update(preserved)          # 還原人工欄位
        else:
            rec = dict(pe)
            for k in HUMAN_OWNED:
                rec[k] = None
            by_id[eid] = rec
    merged = sorted(by_id.values(), key=lambda e: (e.get("date", ""), e.get("id", "")))
    return {"generated_at": _now_taipei_iso(), "events": merged}


def build(dry_run: bool = False) -> int:
    print(f"=== Catalyst-calendar build · {_now_taipei_iso()} ===\n")
    today = _today()
    universe = build_universe()
    print(f"  universe = {len(universe)} tickers "
          f"(v13/v14 latest ∧ (DD ≤{UNIVERSE_DD_WINDOW_DAYS}d ∨ 進場))")

    cache = _load_json(CACHE_JSON) or {}
    stats = {"attempted": 0, "failed": 0}
    skipped: list = []
    errors: list = []

    events = build_events(universe, cache, stats, skipped, errors)

    # ── 誠實失敗：本次每個 yfinance 呼叫都失敗 → 保留上一版前瞻事件、標 stale ──
    stale = stats["attempted"] > 0 and stats["failed"] == stats["attempted"]
    if stale:
        prev = _load_json(CALENDAR_JSON) or {}
        current_ids = {e["id"] for e in events}
        recovered = 0
        for e in (prev.get("events") or []):
            if e.get("id") not in current_ids and e.get("date", "") >= today.isoformat():
                events.append(e)
                current_ids.add(e.get("id"))
                recovered += 1
        print(f"  ⚠ STALE：全部 {stats['attempted']} 個 yfinance 呼叫失敗 → "
              f"保留上一版 {recovered} 筆前瞻事件、stale=true（不捏造日期）。")

    # ── split future / past ──
    future = sorted((e for e in events if e.get("date", "") >= today.isoformat()),
                    key=lambda e: (e["date"], e["ticker"], e["type"]))
    past = [e for e in events if e.get("date", "") < today.isoformat()]

    calendar = {
        "generated_at": _now_taipei_iso(),
        "stale": stale,
        "universe_count": len(universe),
        "events": future,
        "skipped": skipped,
        "errors": errors,
    }
    archive = merge_archive(past, dry_run=dry_run)

    # ── console summary ──
    from collections import Counter
    tcount = Counter(e["type"] for e in future)
    scount = Counter(e["source"] for e in future)
    print(f"  yfinance: attempted={stats['attempted']} failed={stats['failed']} "
          f"cache_size={len(cache)}")
    print(f"  events: forward={len(future)} past→archive={len(past)} "
          f"skipped={len(skipped)} errors={len(errors)}")
    print(f"    forward by type   : {dict(tcount)}")
    print(f"    forward by source : {dict(scount)}")
    print(f"  archive total records: {len(archive['events'])}")
    if errors:
        print(f"    yfinance 失敗 tickers: {[e['ticker'] for e in errors][:30]}")
    if skipped:
        print(f"    skipped catalysts: {[(s['ticker'], s['reason']) for s in skipped][:10]}")

    if dry_run:
        print("\n  (dry-run) 不寫檔。")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CALENDAR_JSON.write_text(json.dumps(calendar, ensure_ascii=False, indent=2),
                             encoding="utf-8")
    ARCHIVE_JSON.write_text(json.dumps(archive, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    CACHE_JSON.write_text(json.dumps(cache, ensure_ascii=False, indent=1),
                          encoding="utf-8")
    print(f"\n  ✓ Wrote {CALENDAR_JSON} ({CALENDAR_JSON.stat().st_size:,} B)")
    print(f"  ✓ Wrote {ARCHIVE_JSON} ({ARCHIVE_JSON.stat().st_size:,} B)")
    print(f"  ✓ Wrote {CACHE_JSON} ({CACHE_JSON.stat().st_size:,} B)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="不寫檔，只印摘要")
    args = p.parse_args()
    return build(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
