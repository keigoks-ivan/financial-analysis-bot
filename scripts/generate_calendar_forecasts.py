#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_calendar_forecasts.py — 日曆效應（月末四日窗 TOM／假日前一日）預測 producer
（forecast ledger P2 package G3）。

設計凍結稿 notes/site-internal/root/_forecast_p2_design_20260902.md §3。每週班車都跑（供
.github/workflows/weekly-market-update.yml 掛，本檔不改該 workflow）。

命題（PREREG 凍結，逐字同設計稿 §3，p 完全由 data/calendar_base_rates.json 機械給出）
--------------------------------------------------------------------------------
  tom_spy_up_4d：「月末四日窗：{resolve_by}（次月第三個交易日）SPY 收盤高於 {base_date} 收盤」
    L＝月最後交易日，base_date＝L 的前一交易日，resolve_by＝次月第三個交易日
    （窗＝L−1 收盤 → L＋3 收盤，4 個交易日）。
  preholiday_spy_up_1d：「假日前一日：{P} SPY 收盤高於前一交易日收盤（{假日名} 前）」
    P＝假日前最後一個交易日，base_date＝P 的前一交易日，resolve_by＝P。

resolver（vs_base_date 窗，由 G4 knowledge/settle_forecasts.py 結算，本檔只負責產出合法形狀）：
    {"series": "pxd:SPY", "op": ">", "value": 0, "window": "vs_base_date",
     "base_date": "<base_date>"}
outcome = (close_end/close_base − 1) {op} value，close_base 讀 base_date 當日或之前最近收盤，
close_end 讀 resolve_by 當日或之前最近收盤（本檔不實作此結算邏輯，只發出上述形狀）。

未來交易日曆（逐字寫入 NYSE_HOLIDAYS，設計稿 §3；不得用套件推算，缺表逼維護）
--------------------------------------------------------------------------------
2026／2027 兩年、週一至週五扣掉 NYSE_HOLIDAYS 即為未來交易日。若計算所需日期落在表格年份
範圍外（含跨年推算「次月第三個交易日」需要用到表外月份），一律跳過該筆並印 stderr
`holiday_table_exhausted`，不得用套件外推猜測（設計稿 §3 明文「逼維護，不猜」）。

事件枚舉與落帳節奏
------------------
ts_date（＝--as-of，預設今天）起 60 天內的每個月末 L、每個假日 H 皆為候選；候選算出
base_date／resolve_by 後，只有 **base_date ∈ [ts_date, ts_date＋7 天)** 才真正落帳（每週跑一次，
7 天視窗對應週頻班車；base_date＝ts_date 本身也合法——班車固定週一 02:00 UTC 執行，在美股
當日收盤前，此時 base_date 若恰為當天，其收盤價尚未落地，屬於「合法但待結算」的正常狀態）。

查重鍵 = (source, claim_template, resolve_by)，對既有帳簿（或 --ledger 覆寫路徑）逐列比對。

episode_id：cal:tom:{L 所在 YYYY-MM} ／ cal:pre:{H，YYYY-MM-DD}；block_key：resolve_by 的
YYYY-MM；horizon_days：(resolve_by − ts_date).days；p／p_clim 完全由
data/calendar_base_rates.json 機械讀出（tom_spy_up_4d 用 tom.p／p_clim.tom_spy_up_4d；
preholiday_spy_up_1d 用 preholiday.p／p_clim.preholiday_spy_up_1d）；note 記 L／H／P 供追溯。

首張預期（設計稿 §3）：TOM 2026-09-30（base 09-29、resolve_by 10-05，於 09-28 班車落帳）；
假日前一日首張＝感恩節（P 11-25，於 11-23 班車落帳；勞動節 09-04 已過——見下方【已知偏誤】）。

CLI
---
  python scripts/generate_calendar_forecasts.py [--as-of YYYY-MM-DD]
      dry-run，草案印到 stdout（純 JSONL）
  python scripts/generate_calendar_forecasts.py --write [--ledger PATH] [--as-of YYYY-MM-DD]
      經 forecast_lib append 進帳簿（含哨兵 twin）；--ledger 覆寫落帳/查重目標路徑（測試用，
      預設 knowledge/forecasts.jsonl）
訊息（枚舉摘要／跳過原因／holiday_table_exhausted）一律印到 stderr，不混進 stdout 的 JSONL。

dry-run 路徑不 import knowledge/forecast_lib.py，只有 --write 路徑才 import（同批 G1/G2 慣例）。

【已知偏誤，供 orchestrator 複審】
本檔對 base_date 的視窗判定是純日期算術，不特別對齊「下一次真正的週一班車」。經實測：
以 --as-of 2026-09-02（非週一）跑，會偵測到 Labor Day（H=2026-09-07）的 base_date=2026-09-03
落在 [2026-09-02, 2026-09-09) 視窗內，因而**仍會產生一筆草案**，不是設計稿narrative暗示的
「零筆」。另外以 --as-of 2026-12-28 跑 TOM（Dec，L=2026-12-31）時，2026-12-31 同時是「12 月
最後交易日」也是「2027 元旦前最後交易日」（兩者相鄰、中間無週末），故 New Year 的
preholiday_spy_up_1d 事件（base_date 同為 2026-12-30）**會與 TOM 一起被枚舉**，不是唯一一筆。
本檔未加裝這兩處的額外抑制規則——設計稿 §3 逐字文本並未定義「週一起算」或「TOM／pre-holiday
撞期時擇一」這類規則，加規則屬於猜測，故保留純日期算術的字面實作，把兩處落差留給 orchestrator
複審裁定（不可證偽的隱性規則不應在 sonnet 分包階段自行拍板）。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_RATES = ROOT / "data" / "calendar_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

SOURCE = "calendar"
SPY_TICKER = "SPY"
ENUMERATION_WINDOW_DAYS = 60   # ts_date 起 60 天內枚舉候選（設計稿 §3）
EMISSION_WINDOW_DAYS = 7       # base_date ∈ [ts_date, ts_date+7) 才真正落帳（設計稿 §3）
NTH_TRADING_DAY_OF_NEXT_MONTH = 3  # resolve_by＝次月第三個交易日（設計稿 §3）

TOM_TEMPLATE = "tom_spy_up_4d"
PREHOLIDAY_TEMPLATE = "preholiday_spy_up_1d"

# NYSE_HOLIDAYS — 逐字寫入，設計稿 §3 PREREG 凍結，不得用套件推算。
NYSE_HOLIDAYS = {
    date(2026, 1, 1): "元旦",
    date(2026, 1, 19): "馬丁路德金恩日",
    date(2026, 2, 16): "總統日",
    date(2026, 4, 3): "耶穌受難日",
    date(2026, 5, 25): "陣亡將士紀念日",
    date(2026, 6, 19): "六月節",
    date(2026, 7, 3): "獨立紀念日（補假）",
    date(2026, 9, 7): "勞動節",
    date(2026, 11, 26): "感恩節",
    date(2026, 12, 25): "聖誕節",
    date(2027, 1, 1): "元旦",
    date(2027, 1, 18): "馬丁路德金恩日",
    date(2027, 2, 15): "總統日",
    date(2027, 3, 26): "耶穌受難日",
    date(2027, 5, 31): "陣亡將士紀念日",
    date(2027, 6, 18): "六月節（補假）",
    date(2027, 7, 5): "獨立紀念日（補假）",
    date(2027, 9, 6): "勞動節",
    date(2027, 11, 25): "感恩節",
    date(2027, 12, 24): "聖誕節（補假）",
}
TABLE_MIN_YEAR = 2026
TABLE_MAX_YEAR = 2027

def warn(msg: str) -> None:
    print(f"[calendar-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[calendar-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 未來交易日曆（週一至週五 − NYSE_HOLIDAYS；超出表年份範圍 → None，呼叫端印
# holiday_table_exhausted）
# ═══════════════════════════════════════════════════════════════════════════

def is_trading_day(d):
    """d 是否為未來交易日；None＝超出 NYSE_HOLIDAYS 表年份範圍，無法判斷。"""
    if d.year < TABLE_MIN_YEAR or d.year > TABLE_MAX_YEAR:
        return None
    if d.weekday() >= 5:
        return False
    return d not in NYSE_HOLIDAYS


def trading_days_in_range(start, end):
    """回傳升冪 [date, ...]；範圍內任一日期超出表年份範圍 → 回傳 None。"""
    if start.year < TABLE_MIN_YEAR or end.year > TABLE_MAX_YEAR:
        return None
    out = []
    d = start
    while d <= end:
        result = is_trading_day(d)
        if result is None:
            return None
        if result:
            out.append(d)
        d += timedelta(days=1)
    return out


def prev_trading_day(d, max_lookback=10):
    """d 之前最近一個交易日；None＝超出表年份範圍，無法判斷。"""
    cur = d - timedelta(days=1)
    for _ in range(max_lookback):
        result = is_trading_day(cur)
        if result is None:
            return None
        if result:
            return cur
        cur -= timedelta(days=1)
    return None


def month_last_day(year, month):
    if month == 12:
        return date(year, 12, 31)
    return date(year, month + 1, 1) - timedelta(days=1)


def last_trading_day_of_month(year, month):
    """該月最後交易日；None＝表年份範圍不足以判斷。"""
    days = trading_days_in_range(date(year, month, 1), month_last_day(year, month))
    if not days:
        return None
    return days[-1]


def nth_trading_day_of_month(year, month, n):
    """該月第 n 個交易日（n 從 1 起算）；None＝表範圍不足或該月交易日不足 n 天。"""
    days = trading_days_in_range(date(year, month, 1), month_last_day(year, month))
    if days is None or len(days) < n:
        return None
    return days[n - 1]


def month_range(start, end):
    """回傳 [(y, m), ...]（升冪），涵蓋 [start, end] 所跨的每個 (年, 月)。"""
    months = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return months


def next_month(year, month):
    return (year + 1, 1) if month == 12 else (year, month + 1)


# ═══════════════════════════════════════════════════════════════════════════
# 事件枚舉
# ═══════════════════════════════════════════════════════════════════════════

def enumerate_tom_events(ts_date, window_end):
    """回傳 [{"L","base_date","resolve_by"}, ...]（L ∈ [ts_date, window_end]）。"""
    events = []
    for y, m in month_range(ts_date, window_end):
        L = last_trading_day_of_month(y, m)
        if L is None:
            warn(f"holiday_table_exhausted：無法計算 {y}-{m:02d} 月末交易日（超出 NYSE_HOLIDAYS 表年份範圍）")
            continue
        if not (ts_date <= L <= window_end):
            continue
        base_date = prev_trading_day(L)
        if base_date is None:
            warn(f"holiday_table_exhausted：無法計算 {L.isoformat()} 的前一交易日")
            continue
        ny, nm = next_month(y, m)
        resolve_by = nth_trading_day_of_month(ny, nm, NTH_TRADING_DAY_OF_NEXT_MONTH)
        if resolve_by is None:
            warn(f"holiday_table_exhausted：無法計算 {ny}-{nm:02d} 第 {NTH_TRADING_DAY_OF_NEXT_MONTH} 個交易日（超出表年份範圍）")
            continue
        events.append({"L": L, "base_date": base_date, "resolve_by": resolve_by})
    return events


def enumerate_preholiday_events(ts_date, window_end):
    """回傳 [{"H","name","P","base_date"}, ...]（H ∈ [ts_date, window_end]）。"""
    events = []
    for H, name in sorted(NYSE_HOLIDAYS.items()):
        if not (ts_date <= H <= window_end):
            continue
        P = prev_trading_day(H)
        if P is None:
            warn(f"holiday_table_exhausted：無法計算 {H.isoformat()}（{name}）的前一交易日")
            continue
        base_date = prev_trading_day(P)
        if base_date is None:
            warn(f"holiday_table_exhausted：無法計算 {P.isoformat()} 的前一交易日")
            continue
        events.append({"H": H, "name": name, "P": P, "base_date": base_date})
    return events


# ═══════════════════════════════════════════════════════════════════════════
# base rate 表
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates(path=BASE_RATES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_calendar_base_rates.py")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

def build_tom_draft(ev, ts_date, ts_str, base_rates, rid):
    L, base_date, resolve_by = ev["L"], ev["base_date"], ev["resolve_by"]
    p = base_rates["tom"]["p"]
    n = base_rates["tom"]["n"]
    p_clim = base_rates["p_clim"].get(TOM_TEMPLATE)
    built_at = base_rates.get("built_at")

    claim = (f"月末四日窗：{resolve_by.isoformat()}（次月第三個交易日）SPY 收盤高於 "
             f"{base_date.isoformat()} 收盤")
    note = (f"calendar 機械賦值（無需人工判斷）｜L={L.isoformat()}｜p 取自 "
            f"data/calendar_base_rates.json tom.p（n={n}，built_at={built_at}）｜"
            f"p_clim=p_clim.{TOM_TEMPLATE}")

    episode_id = f"cal:tom:{L.strftime('%Y-%m')}"
    block_key = resolve_by.strftime("%Y-%m")
    horizon_days = (resolve_by - ts_date).days

    return {
        "id": rid, "ts": ts_str, "schema": "fc-v2",
        "source": SOURCE,
        "source_ref": f"data/calendar_base_rates.json built_at={built_at}｜L={L.isoformat()}",
        "claim": claim, "claim_template": TOM_TEMPLATE,
        "p": p, "p_clim": p_clim,
        "p_clim_ref": f"data/calendar_base_rates.json p_clim.{TOM_TEMPLATE} built_at={built_at}",
        "p_table_built_at": built_at,
        "horizon_days": horizon_days, "resolve_by": resolve_by.isoformat(),
        "resolver": {"series": f"pxd:{SPY_TICKER}", "op": ">", "value": 0,
                     "window": "vs_base_date", "base_date": base_date.isoformat()},
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "episode_id": episode_id, "block_key": block_key, "twin_of": None,
        "note": note,
    }


def build_preholiday_draft(ev, ts_date, ts_str, base_rates, rid):
    H, name, P, base_date = ev["H"], ev["name"], ev["P"], ev["base_date"]
    p = base_rates["preholiday"]["p"]
    n = base_rates["preholiday"]["n"]
    p_clim = base_rates["p_clim"].get(PREHOLIDAY_TEMPLATE)
    built_at = base_rates.get("built_at")
    resolve_by = P

    claim = f"假日前一日：{P.isoformat()} SPY 收盤高於前一交易日收盤（{name}前）"
    note = (f"calendar 機械賦值（無需人工判斷）｜H={H.isoformat()}（{name}）｜P={P.isoformat()}｜"
            f"p 取自 data/calendar_base_rates.json preholiday.p（n={n}，built_at={built_at}）｜"
            f"p_clim=p_clim.{PREHOLIDAY_TEMPLATE}")

    episode_id = f"cal:pre:{H.isoformat()}"
    block_key = resolve_by.strftime("%Y-%m")
    horizon_days = (resolve_by - ts_date).days

    return {
        "id": rid, "ts": ts_str, "schema": "fc-v2",
        "source": SOURCE,
        "source_ref": f"data/calendar_base_rates.json built_at={built_at}｜H={H.isoformat()}（{name}）",
        "claim": claim, "claim_template": PREHOLIDAY_TEMPLATE,
        "p": p, "p_clim": p_clim,
        "p_clim_ref": f"data/calendar_base_rates.json p_clim.{PREHOLIDAY_TEMPLATE} built_at={built_at}",
        "p_table_built_at": built_at,
        "horizon_days": horizon_days, "resolve_by": resolve_by.isoformat(),
        "resolver": {"series": f"pxd:{SPY_TICKER}", "op": ">", "value": 0,
                     "window": "vs_base_date", "base_date": base_date.isoformat()},
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "episode_id": episode_id, "block_key": block_key, "twin_of": None,
        "note": note,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 查重 + id
# ═══════════════════════════════════════════════════════════════════════════

def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def existing_dedupe_keys(rows, source=SOURCE):
    return {(r.get("source"), r.get("claim_template"), r.get("resolve_by"))
            for r in rows if r.get("source") == source}


def _local_next_ids(ts_str, n, existing_rows):
    used = {r.get("id") for r in existing_rows if r.get("id")}
    prefix = f"fc_{ts_str.replace('-', '')}_cal_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{prefix}{seq:02d}"
        if cand not in used:
            out.append(cand)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="日曆效應（TOM／假日前一日）預測 producer — 每週班車")
    ap.add_argument("--write", action="store_true", help="append 進帳簿（經 forecast_lib，含哨兵 twin；預設 dry-run）")
    ap.add_argument("--ledger", default=None,
                     help="落帳/查重目標帳簿路徑覆寫（測試用；預設 knowledge/forecasts.jsonl）")
    ap.add_argument("--as-of", default=None,
                     help="模擬班車執行日 YYYY-MM-DD（測試用；預設今天，供驗收模擬未來班車日）")
    args = ap.parse_args()

    forecasts_path = Path(args.ledger) if args.ledger else FORECASTS

    if args.as_of:
        try:
            ts_date = date.fromisoformat(args.as_of)
        except ValueError:
            raise SystemExit(f"--as-of 格式錯誤（需 YYYY-MM-DD）：{args.as_of}")
    else:
        ts_date = date.today()
    ts_str = ts_date.isoformat()
    window_end = ts_date + timedelta(days=ENUMERATION_WINDOW_DAYS)
    emission_hi = ts_date + timedelta(days=EMISSION_WINDOW_DAYS)  # 上界不含

    base_rates = load_base_rates()

    tom_candidates = enumerate_tom_events(ts_date, window_end)
    preholiday_candidates = enumerate_preholiday_events(ts_date, window_end)
    info(f"枚舉（ts_date={ts_str}，60 天窗至 {window_end.isoformat()}）："
         f"TOM 候選 {len(tom_candidates)} 筆、假日候選 {len(preholiday_candidates)} 筆")

    tom_due = [e for e in tom_candidates if ts_date <= e["base_date"] < emission_hi]
    preholiday_due = [e for e in preholiday_candidates if ts_date <= e["base_date"] < emission_hi]
    info(f"落帳條件 base_date ∈ [{ts_str}, {emission_hi.isoformat()})："
         f"TOM {len(tom_due)} 筆、假日 {len(preholiday_due)} 筆")

    existing = _existing_forecasts(forecasts_path)
    dedupe_keys = existing_dedupe_keys(existing)

    drafts = []
    skipped_dedupe = 0
    for ev in tom_due:
        resolve_by_str = ev["resolve_by"].isoformat()
        if (SOURCE, TOM_TEMPLATE, resolve_by_str) in dedupe_keys:
            skipped_dedupe += 1
            continue
        drafts.append(("tom", ev))
    for ev in preholiday_due:
        resolve_by_str = ev["P"].isoformat()
        if (SOURCE, PREHOLIDAY_TEMPLATE, resolve_by_str) in dedupe_keys:
            skipped_dedupe += 1
            continue
        drafts.append(("preholiday", ev))

    if not drafts:
        info("本次無符合落帳條件的事件——" +
             ("60 天窗內無候選事件。" if not (tom_candidates or preholiday_candidates) else
              "候選事件的 base_date 皆落在 7 天落帳視窗之外（下次班車再檢查），"
              "或已被查重（同 source/claim_template/resolve_by 已存在）。"))

    if not args.write:
        ids = _local_next_ids(ts_str, len(drafts), existing)
        out_rows = []
        for (kind, ev), rid in zip(drafts, ids):
            if kind == "tom":
                out_rows.append(build_tom_draft(ev, ts_date, ts_str, base_rates, rid))
            else:
                out_rows.append(build_preholiday_draft(ev, ts_date, ts_str, base_rates, rid))
        for row in out_rows:
            print(json.dumps(row, ensure_ascii=False))
        info(f"dry-run：共 {len(out_rows)} 筆草案（查重跳過 {skipped_dedupe} 筆）。"
             f"--write 才會經 forecast_lib append 進 {forecasts_path}（含哨兵 twin）。")
        return

    sys.path.insert(0, str(ROOT / "knowledge"))
    try:
        import forecast_lib as fl
    except ImportError as e:
        print(f"[calendar-forecasts][ERROR] 找不到 knowledge/forecast_lib.py（{e}）——"
              f"--write 依賴 forecast_lib.py，尚未就緒。", file=sys.stderr)
        sys.exit(2)

    ids = fl.next_ids(ts_str, "cal", len(drafts), path=forecasts_path)
    out_rows = []
    for (kind, ev), rid in zip(drafts, ids):
        if kind == "tom":
            out_rows.append(build_tom_draft(ev, ts_date, ts_str, base_rates, rid))
        else:
            out_rows.append(build_preholiday_draft(ev, ts_date, ts_str, base_rates, rid))

    fl.finalize(out_rows)  # block_key 已由 build_*_draft 設為 resolve_by 月，finalize 不覆寫
    n_written, n_twins = fl.append(out_rows, path=forecasts_path, write=True)
    info(f"summary: tom_due={len(tom_due)} preholiday_due={len(preholiday_due)} "
         f"skipped_dedupe={skipped_dedupe}")
    print(f"# --write：寫入 {n_written} 本尊 + {n_twins} 哨兵 twin → {forecasts_path}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
