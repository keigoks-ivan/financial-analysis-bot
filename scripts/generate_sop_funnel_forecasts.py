#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_sop_funnel_forecasts.py — sop-funnel 板機訊號預測 producer（市況主控台設計稿
§9，包 F1）。

掃 docs/dd-screener/sop-funnel/ledger.json 的 `events[]`，取 `status ∈ {entered, skipped,
closed}`（`vetoed` 不算訊號，設計稿明文排除）且 `signal_date ≥ 2026-06-01` 的每一筆，各產一份
草案：「{ticker} 板機訊號後 91 曆日跑贏 SPY」（`sop_beat_spy_91d`，resolver 走既有 relspy: 域，
base_date=signal_date、base_px=signal_close）。命題**不分**進場/略過/收盤——skipped 一樣落帳，
因為本命題測的是「訊號本身」的預測力，不是「操作者是否進場」（比照 dd-verdict producer 把
進場/觀望/迴避收斂成同一命題、只調機率的精神；此處連機率都不調，見下）。

p 值（PREREG 凍結，設計稿 §9 F1，sonnet 不得改）：
    p = freq_beat_91d（data/sop_funnel_base_rates.json，n_valid ≥ 30 時）
        或 PREREG 0.58（n_valid < 30 時的固定退回值）
    對本次執行內全部草案套用同一個 p（不分 entry_type/status——by_type 僅供觀察，「只列不採」，
    見 base rates builder 的 methodology_note）。
p_clim 讀自 data/dd_verdict_base_rates.json 的 `p_clim.dd_beat_spy_91d`（DD 宇宙相對 SPY 的
pooled 無條件頻率）——與本檔的自建表（sop_funnel_base_rates.json）是**兩張不同的表**：p 用
自建表（訊號本身的歷史勝率），p_clim 用 DD 宇宙表（不知道任何訊號存在的基準），兩者刻意不
同源，才能看出訊號相對「什麼都不知道」有沒有邊際訊息。`p_table_built_at` 因此記的是**賦 p
所用表**（sop_funnel_base_rates.json）的 built_at，不是 p_clim 所用表的 built_at（語意見
knowledge/forecast_lib.py migrate 段註解「p_table_built_at 是賦 p 本身所用表的 built_at，
非 p_clim 所用表」）。

resolver（relspy 域，由 knowledge/settle_forecasts.py 結算，本檔只負責產出合法形狀）：
    {"series": "relspy:<TICKER>", "op": ">", "value": 0, "window": "at_expiry",
     "base_date": "<signal_date>", "base_px": <signal_close>, "base_spy": <SPY signal_date 收盤>}
base_px 取 ledger.json 該筆事件的 `signal_close`；base_spy 取 data/flowmap_prices.json 的 SPY
「signal_date 當日或之前最近收盤」（同 generate_dd_verdict_forecasts.py 既有慣例）；<TICKER>
直接用 ledger.json 的 `ticker` 字串（ALIAS 對映留給結算端的 relspy: 域處理，本檔的 ALIAS 只用
來檢查該 ticker 是否真的在 data/weekly_cache/ 裡，逐字照抄 knowledge/settle_outcomes.py）。

查重 / 落帳
-----------
dedupe key = event id（ledger.json 該筆事件的 `id`，如 "ASML:2026-05-22:A2"）：先比對既有
forecasts.jsonl 每筆的 `event_id` 欄位（本 producer 自己寫入的新欄，非 schema v2 標準 13＋8
欄之一，但 additive、其餘 producer 不受影響）；若該筆缺 `event_id`（理論上不會發生於本
producer 自己寫的行，但防禦性保留），退而在 `note` 文字裡找 `event_id=<id>` 子字串。一檔
（一個 event id）只掛一次——同一 event 不會因重跑而重複落帳。

ids：dry-run 用本檔本地 `fc_{YYYYMMDD}_sop_{NN}` 生成（不 import forecast_lib）；`--write` 才
`sys.path.insert(0, str(ROOT / "knowledge")); import forecast_lib as fl`，用
`fl.next_ids(ts, "sop", n)` 取代本地生成，並經 `fl.append(..., write=True)` 落帳（含哨兵
twin，由 forecast_lib 生成，本檔不重造）。

episode_id / block_key：`sop:{ticker}:{signal_date}`／signal 所在月 `YYYY-MM`（非 ts 月——
backfill 批次單次執行 ts 相同、signal_date 橫跨數月，若塌成同一 ts 月會破壞 §3.5
block-bootstrap 的月間結構，理由同 generate_dd_verdict_forecasts.py）。`forecast_lib.finalize()`
對已設定的 block_key 不覆寫，--write 路徑照常呼叫 finalize。

CLI
---
  python scripts/generate_sop_funnel_forecasts.py
      dry-run，草案印到 stdout（純 JSONL）
  python scripts/generate_sop_funnel_forecasts.py --write
      append 進 knowledge/forecasts.jsonl（經 forecast_lib，含哨兵 twin）
  python scripts/generate_sop_funnel_forecasts.py --write --ledger PATH
      --write 落帳目標改為 PATH（測試用；讀既有筆做查重與寫入都改讀/寫 PATH，
      不動 knowledge/forecasts.jsonl）
訊息（掃描摘要／跳過原因）一律印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "dd-screener" / "sop-funnel" / "ledger.json"
SOP_BASE_RATES = ROOT / "data" / "sop_funnel_base_rates.json"
DD_BASE_RATES = ROOT / "data" / "dd_verdict_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
CACHE_DIR = ROOT / "data" / "weekly_cache"

SOURCE = "sop-funnel"
TEMPLATE = "sop_beat_spy_91d"
STATUS_ELIGIBLE = {"entered", "skipped", "closed"}   # vetoed 不算訊號（設計稿 §9 F1）
SIGNAL_DATE_CUTOFF = "2026-06-01"                     # PREREG 凍結（設計稿 §9 F1）
HORIZON_DAYS = 91
N_VALID_MIN = 30
PREREG_FALLBACK_P = 0.58
P_LO, P_HI = 0.05, 0.95

# ledger ticker → weekly_cache 檔名（照抄 knowledge/settle_outcomes.py ALIAS，逐字一致）
ALIAS = {
    "5274.TW": "5274.TWO",
    "8299.TW": "8299.TWO",
    "AENA": "AENA.MC",
    "BESI": "BESI.AS",
    "RMS": "RMS.PA",
    "SU": "SU.PA",
    "LVMH": "MC.PA",
    "ABB": "ABBNY",
}

EVENT_ID_NOTE_RE = re.compile(r"event_id=([^｜]+)")  # ｜ 為欄位分隔符（U+FF5C）


def warn(msg):
    print(f"[sop-funnel-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[sop-funnel-forecasts] {msg}", file=sys.stderr)


def _clip(x, lo, hi):
    return max(lo, min(hi, x))


def _plus_days(ymd, n):
    y, m, d = map(int, ymd.split("-"))
    return (date(y, m, d) + timedelta(days=n)).isoformat()


# ═══════════════════════════════════════════════════════════════════════════
# ledger.json
# ═══════════════════════════════════════════════════════════════════════════

def load_ledger():
    if not LEDGER.exists():
        raise SystemExit(f"找不到 {LEDGER}")
    try:
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {LEDGER}: {e}")
    return data.get("events") or []


def is_eligible(e):
    return (e.get("status") in STATUS_ELIGIBLE
            and (e.get("signal_date") or "") >= SIGNAL_DATE_CUTOFF)


# ═══════════════════════════════════════════════════════════════════════════
# base rates（p、p_clim 兩張不同表，見檔頭 docstring）
# ═══════════════════════════════════════════════════════════════════════════

def load_sop_base_rates():
    if not SOP_BASE_RATES.exists():
        raise SystemExit(f"找不到 {SOP_BASE_RATES} —— 先跑 "
                          f"python scripts/build_sop_funnel_base_rates.py")
    try:
        return json.loads(SOP_BASE_RATES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {SOP_BASE_RATES}: {e}")


def load_dd_base_rates():
    if not DD_BASE_RATES.exists():
        raise SystemExit(f"找不到 {DD_BASE_RATES} —— 先跑 "
                          f"python scripts/build_dd_verdict_base_rates.py")
    try:
        return json.loads(DD_BASE_RATES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {DD_BASE_RATES}: {e}")


def resolve_p(sop_rates):
    """回傳 (p, p_source, p_table_built_at)。p_source ∈ {"table", "prereg_fallback"}，
    對本次執行內全部草案套用同一個值（設計稿 §9 F1：by_type 只列不採）。"""
    n_valid = sop_rates.get("n_valid")
    freq = sop_rates.get("freq_beat_91d")
    built_at = sop_rates.get("built_at")
    if n_valid is not None and n_valid >= N_VALID_MIN and freq is not None:
        return freq, "table", built_at
    return PREREG_FALLBACK_P, "prereg_fallback", built_at


# ═══════════════════════════════════════════════════════════════════════════
# data/flowmap_prices.json SPY 讀法（base_spy：signal_date 當日或之前最近收盤）
# ═══════════════════════════════════════════════════════════════════════════

def _load_flowmap_spy():
    if not FLOWMAP_PRICES.exists():
        return None
    try:
        data = json.loads(FLOWMAP_PRICES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    bars = (data.get("series") or {}).get("SPY")
    if not bars:
        return None
    return sorted((d, c) for d, c in bars)


def _close_at_or_before(bars, ymd):
    """最近一根 date ≤ ymd 的收盤；無則 None。bars 已按日期升冪（照抄
    knowledge/settle_outcomes.py `_close_at_or_before` 語意）。"""
    best = None
    for d, c in bars:
        if d <= ymd:
            best = (d, c)
        else:
            break
    return best


# ═══════════════════════════════════════════════════════════════════════════
# 查重
# ═══════════════════════════════════════════════════════════════════════════

def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _existing_dedupe_keys(existing_rows):
    keys = set()
    for r in existing_rows:
        if r.get("source") != SOURCE:
            continue
        eid = r.get("event_id")
        if not eid:
            m = EVENT_ID_NOTE_RE.search(r.get("note") or "")
            if m:
                eid = m.group(1).strip()
        if eid:
            keys.add(eid)
    return keys


def _local_next_ids(ts_str, n, existing_rows):
    used = {r.get("id") for r in existing_rows if r.get("id")}
    prefix = f"fc_{ts_str.replace('-', '')}_sop_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{prefix}{seq:02d}"
        if cand not in used:
            out.append(cand)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

def build_draft(e, ts_str, p, p_source, p_table_built_at, p_clim, p_clim_ref,
                 base_spy_date, base_spy_px):
    event_id = e["id"]
    ticker = e["ticker"]
    entry_type = e["entry_type"]
    status = e["status"]
    signal_date = e["signal_date"]
    signal_close = e["signal_close"]

    resolve_by = _plus_days(signal_date, HORIZON_DAYS)
    month_key = signal_date[:7]
    episode_id = f"sop:{ticker}:{signal_date}"

    claim = (f"{resolve_by} 前（板機訊號 {signal_date}，{entry_type} 型）："
             f"{ticker} 報酬跑贏 SPY")

    p_source_text = "sop_funnel_base_rates.json 表值" if p_source == "table" else \
        f"PREREG {PREREG_FALLBACK_P} fallback（n_valid < {N_VALID_MIN}）"

    note = (f"sop-funnel 機械賦值（PREREG p，非人工判斷）｜event_id={event_id}｜status={status}｜"
            f"entry_type={entry_type}｜p={p}（{p_source_text}，data/sop_funnel_base_rates.json "
            f"built_at={p_table_built_at}）｜p_clim[dd_beat_spy_91d]={p_clim}（{p_clim_ref}）｜"
            f"base_date={signal_date}｜base_px={signal_close}｜base_spy={base_spy_px}（{base_spy_date}）")

    draft = {
        "id": None,
        "ts": ts_str,
        "schema": "fc-v2",
        "source": SOURCE,
        "source_ref": f"docs/dd-screener/sop-funnel/ledger.json id={event_id}",
        "claim": claim,
        "claim_template": TEMPLATE,
        "p": round(_clip(p, P_LO, P_HI), 4),
        "p_clim": p_clim,
        "p_clim_ref": p_clim_ref,
        "p_table_built_at": p_table_built_at,
        "horizon_days": HORIZON_DAYS,
        "resolve_by": resolve_by,
        "resolver": {
            "series": f"relspy:{ticker}",
            "op": ">",
            "value": 0,
            "window": "at_expiry",
            "base_date": signal_date,
            "base_px": signal_close,
            "base_spy": base_spy_px,
        },
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "episode_id": episode_id,
        "block_key": month_key,
        "twin_of": None,
        "event_id": event_id,
        "note": note,
    }
    return draft


def main():
    ap = argparse.ArgumentParser(description="sop-funnel 板機訊號預測 producer"
                                              "（ledger.json 事件 → 跑贏 SPY 機率命題）")
    ap.add_argument("--write", action="store_true",
                     help="append 進帳簿（經 forecast_lib，含哨兵 twin；預設 dry-run）")
    ap.add_argument("--ledger", default=None,
                     help="落帳/查重目標帳簿路徑覆寫（測試用；預設 knowledge/forecasts.jsonl，"
                          "與『sop-funnel 板機訊號帳』ledger.json 無關，純粹沿用 forecasts.jsonl "
                          "口語別名）")
    args = ap.parse_args()

    forecasts_path = Path(args.ledger) if args.ledger else FORECASTS

    today = date.today()
    ts_str = today.isoformat()

    events = load_ledger()
    eligible = [e for e in events if is_eligible(e)]
    info(f"ledger.json 掃描：{len(events)} 筆事件")
    info(f"符合條件（status∈{sorted(STATUS_ELIGIBLE)}, signal_date≥{SIGNAL_DATE_CUTOFF}）："
         f"{len(eligible)} 筆")

    sop_rates = load_sop_base_rates()
    dd_rates = load_dd_base_rates()
    p, p_source, p_table_built_at = resolve_p(sop_rates)
    p_clim = (dd_rates.get("p_clim") or {}).get("dd_beat_spy_91d")
    dd_built_at = dd_rates.get("built_at")
    p_clim_ref = f"data/dd_verdict_base_rates.json p_clim.dd_beat_spy_91d built_at={dd_built_at}"
    info(f"p={p}（來源={p_source}，{SOP_BASE_RATES.name} built_at={p_table_built_at}，"
         f"n_valid={sop_rates.get('n_valid')}）")
    info(f"p_clim={p_clim}（{p_clim_ref}）")

    spy_bars = _load_flowmap_spy()

    existing = _existing_forecasts(forecasts_path)
    dedupe_keys = _existing_dedupe_keys(existing)

    skip_counts = Counter()
    unresolvable_tickers = set()
    drafts = []

    for e in eligible:
        event_id = e["id"]
        ticker = e["ticker"]

        if e.get("signal_close") is None:
            skip_counts["no_signal_close"] += 1
            warn(f"{event_id}：signal_close 為 null，跳過")
            continue

        alias_fname = ALIAS.get(ticker, ticker)
        if not (CACHE_DIR / f"{alias_fname}.json").exists():
            skip_counts["ticker_not_in_weekly_cache"] += 1
            unresolvable_tickers.add(ticker)
            continue

        if not spy_bars:
            skip_counts["base_spy_missing"] += 1
            warn(f"{event_id}：{FLOWMAP_PRICES} 讀取失敗或無 SPY 序列，跳過")
            continue
        base_spy = _close_at_or_before(spy_bars, e["signal_date"])
        if base_spy is None:
            skip_counts["base_spy_missing"] += 1
            warn(f"{event_id}：flowmap SPY 找不到 {e['signal_date']} 或之前的收盤，跳過")
            continue
        base_spy_date, base_spy_px = base_spy

        resolve_by = _plus_days(e["signal_date"], HORIZON_DAYS)
        if resolve_by < ts_str:
            skip_counts["resolve_by_in_past"] += 1
            continue

        if event_id in dedupe_keys:
            skip_counts["dedupe"] += 1
            continue

        draft = build_draft(e, ts_str, p, p_source, p_table_built_at, p_clim, p_clim_ref,
                            base_spy_date, base_spy_px)
        drafts.append(draft)

    if unresolvable_tickers:
        warn(f"以下 ticker 不在 data/weekly_cache/（含 ALIAS 對映）：{sorted(unresolvable_tickers)}")

    if not args.write:
        ids = _local_next_ids(ts_str, len(drafts), existing)
        for draft, rid in zip(drafts, ids):
            draft["id"] = rid
        for draft in drafts:
            print(json.dumps(draft, ensure_ascii=False))
        info(f"summary: n_events_scanned={len(events)} n_eligible={len(eligible)} "
             f"n_drafts={len(drafts)} skipped={dict(skip_counts)}")
        info(f"dry-run：共 {len(drafts)} 筆草案。--write 才會經 forecast_lib append 進 "
             f"{forecasts_path}（含哨兵 twin）。")
        return

    sys.path.insert(0, str(ROOT / "knowledge"))
    try:
        import forecast_lib as fl
    except ImportError as e:
        print(f"[sop-funnel-forecasts][ERROR] 找不到 knowledge/forecast_lib.py（{e}）——"
              f"--write 依賴 forecast_lib.py，尚未就緒。", file=sys.stderr)
        sys.exit(2)

    ids = fl.next_ids(ts_str, "sop", len(drafts), path=forecasts_path)
    for draft, rid in zip(drafts, ids):
        draft["id"] = rid

    fl.finalize(drafts)  # block_key 已由 build_draft() 設為 signal 月，finalize 不覆寫（見檔頭）

    n_written, n_twins = fl.append(drafts, path=forecasts_path, write=True)

    info(f"summary: n_events_scanned={len(events)} n_eligible={len(eligible)} "
         f"n_drafts={len(drafts)} skipped={dict(skip_counts)}")
    print(f"\n# --write：寫入 {n_written} 本尊 + {n_twins} 哨兵 twin → {forecasts_path}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
