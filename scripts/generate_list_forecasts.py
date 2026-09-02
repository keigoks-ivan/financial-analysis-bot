#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_list_forecasts.py — 名單 producer（forecast ledger v2 §9 row F2，包 F2）。

把三個既有的名單（**不是新的收斂面**，只是把既有名單的成員轉成可證偽的機率命題）
掃成 forecasts.jsonl 草案：

  1. `grp-seat` ── `docs/engine/arena.json` core_seats[]／sat_seats[]（週日更）
     「{resolve_by} 前（GRP 核心席位 {as_of} 起 91 曆日）：{ticker} 報酬跑贏 SPY」
     claim_template=`grp_beat_spy_91d`；核心 offset +0.10，衛星 offset +0.05
  2. `picks-baofa` ── `docs/picks/candidates.json` official_baofa[]（週更）
     「{resolve_by} 前（精選爆發榜 {as_of} 起 91 曆日）：{ticker} 報酬跑贏 SPY」
     claim_template=`picks_beat_spy_91d`；offset +0.05
  3. `tenbagger` ── `docs/picks/tenbagger.json` official[]（正式席位，候補 candidates[] 為退路；月頻；
     見設計稿 §9 row F2「currently empty」——0 筆草案是預期行為，不是錯誤）
     「{resolve_by} 前（十倍股候選 {as_of} 起 365 曆日）：{ticker} 報酬跑贏 SPY」
     claim_template=`tenbagger_beat_spy_365d`；offset +0.05（用 365d p_clim）

resolver（relspy 新域，逐字同 scripts/generate_dd_verdict_forecasts.py 慣例，由 A1 的
knowledge/settle_forecasts.py 結算——本檔只負責產出合法形狀，不做結算）：
    {"series": "relspy:<TICKER>", "op": ">", "value": 0, "window": "at_expiry",
     "base_date": "<list as_of>", "base_px": <price>, "base_spy": <SPY 同日或之前收盤>}
base_date：grp 取 arena.json `run_timestamp` 的日期部分；picks／tenbagger 取各自 `as_of`。
base_px：名單本身若帶價（目前只有 grp 的 `grp.price`）直接用；否則退回
`data/weekly_cache/<TICKER>.json`（ALIAS 對映後）weekly_bars 中 base_date 或之前最近一根收盤
（picks／tenbagger 目前兩份名單皆不帶價，一律走此退路）。
base_spy：`data/flowmap_prices.json` series.SPY 中 base_date 或之前最近一根收盤（同
generate_dd_verdict_forecasts.py `_close_at_or_before` 語意）。
resolve_by = base_date + horizon_days（91；tenbagger 365）曆日。

p 值（PREREG 凍結，設計稿 §9 row F2，sonnet 不得改）：
    p = clip(p_clim + offset, 0.05, 0.95)
    offset：GRP 核心 +0.10／GRP 衛星 +0.05／精選爆發榜 +0.05／十倍股候選 +0.05
p_clim 一律讀 data/dd_verdict_base_rates.json 的 `p_clim.dd_beat_spy_91d`（grp／picks 用）／
`p_clim.dd_beat_spy_365d`（tenbagger 用）——借用 dd-verdict 既有的宇宙相對 SPY 頻率表，本
producer 不自建新表（設計稿 §9 共同規則：「p_clim 一律引用 data/dd_verdict_base_rates.json
的 p_clim…除非另有自建表」，本包沒有自建表）。claim_template 仍是本包自己的新樣板名
（grp_beat_spy_91d／picks_beat_spy_91d／tenbagger_beat_spy_365d），與借來的 p_clim key
（dd_beat_spy_91d／dd_beat_spy_365d）刻意不同名，note 欄會註明借用關係。

episode_id = `{source}:{ticker}:{YYYY-MM}`（YYYY-MM 取 base_date 所在月）；
block_key = base_date 所在月（同 episode_id 的月份，逐字同 dd-verdict「裁決月」慣例，
forecast_lib.finalize() 對已設定的 block_key 不覆寫）。

查重（設計稿 §9 row F2 原文：「同 source 同 ticker 已有 open 命題→不重發（一檔一次只掛一張）」）
-----------------------------------------------------------------------------------------
dedupe key = (source, ticker)：掃 ledger（或 --ledger 指定的測試帳）中 `status == "open"`
的既有列，把 `resolver.series` 前綴 `relspy:` 之後的字串當 ticker（不新增專屬欄位，沿用
resolver 本身即可反解——sentinel-noise 哨兵 twin 的 `source` 已被 forecast_lib 覆寫成
"sentinel-noise"，不會誤入這個 (source, ticker) 集合）。同一批次執行內（例如同週 GRP 核心與
衛星席位剛好出現同一檔）也用同一個 set 即時更新，避免同批次自己重複掛兩張。**這條規則只看
「有沒有 open 命題」，不比較 resolve_by／claim_template──同 ticker 若已有一張在跑，即使即將
到期也不會補發新的一張，等舊的 settle 之後才會在下一輪自然補上**（PREREG，見設計稿 §9）。

ids：dry-run 用本檔本地 `fc_{YYYYMMDD}_{prefix}_{NN}` 生成（prefix 依名單：grp/picks/tb，
逐名單分開配號避免撞號，不 import forecast_lib）；`--write` 才
`sys.path.insert(0, str(ROOT / "knowledge")); import forecast_lib as fl`，改用
`fl.next_ids(ts, prefix, n, path=ledger)`，並經 `fl.finalize()` + `fl.append(..., write=True)`
落帳（含哨兵 twin，由 forecast_lib 生成，本檔不重造）。

CLI
---
  python scripts/generate_list_forecasts.py [--list grp|picks|tenbagger|all]
        dry-run（預設），草案印到 stdout（純 JSONL）
  python scripts/generate_list_forecasts.py --list all --write
        append 進 knowledge/forecasts.jsonl（經 forecast_lib，含哨兵 twin）
  python scripts/generate_list_forecasts.py --write --ledger /path/to/scratch.jsonl
        用測試用 scratch ledger 覆寫預設帳簿路徑（讀既有列查重、寫入亦寫該路徑）
訊息（掃描摘要／跳過原因）一律印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARENA = ROOT / "docs" / "engine" / "arena.json"
CANDIDATES = ROOT / "docs" / "picks" / "candidates.json"
TENBAGGER = ROOT / "docs" / "picks" / "tenbagger.json"
BASE_RATES = ROOT / "data" / "dd_verdict_base_rates.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
CACHE_DIR = ROOT / "data" / "weekly_cache"
FORECASTS_DEFAULT = ROOT / "knowledge" / "forecasts.jsonl"

P_LO, P_HI = 0.05, 0.95

# entity → weekly_cache 檔名別名（逐字照抄 knowledge/settle_outcomes.py ALIAS／
# scripts/generate_dd_verdict_forecasts.py ALIAS，三處必須一致）
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

GRP_OFFSETS = {"核心": 0.10, "衛星": 0.05}   # PREREG 凍結（設計稿 §9 row F2）
PICKS_OFFSET = 0.05                          # PREREG 凍結
TENBAGGER_OFFSET = 0.05                      # PREREG 凍結（365d 用 p_clim_365d）

# 每個名單的固定參數（PREREG 凍結，設計稿 §9 row F2）
LIST_SPECS = {
    "grp": {
        "source": "grp-seat",
        "claim_template": "grp_beat_spy_91d",
        "horizon_days": 91,
        "p_clim_key": "dd_beat_spy_91d",
        "id_prefix": "grp",
    },
    "picks": {
        "source": "picks-baofa",
        "claim_template": "picks_beat_spy_91d",
        "horizon_days": 91,
        "p_clim_key": "dd_beat_spy_91d",
        "id_prefix": "picks",
    },
    "tenbagger": {
        "source": "tenbagger",
        "claim_template": "tenbagger_beat_spy_365d",
        "horizon_days": 365,
        "p_clim_key": "dd_beat_spy_365d",
        "id_prefix": "tb",
    },
}


def warn(msg):
    print(f"[list-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[list-forecasts] {msg}", file=sys.stderr)


def _clip(x, lo, hi):
    return max(lo, min(hi, x))


def _plus_days(ymd, n):
    y, m, d = map(int, ymd.split("-"))
    return (date(y, m, d) + timedelta(days=n)).isoformat()


def _date_part(ts):
    """"2026-08-30T22:14:32Z" -> "2026-08-30"；空值原樣回傳空字串。"""
    return (ts or "")[:10]


def _load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {path}: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════
# 名單讀取（三個 extractor，各自回傳 normalized item dict 的 list）
# ═══════════════════════════════════════════════════════════════════════════

def extract_grp_items():
    data = _load_json(ARENA)
    if data is None:
        warn(f"{ARENA} 不存在或無法讀取，grp 名單本輪略過")
        return []
    base_date = _date_part(data.get("run_timestamp"))
    if not base_date:
        warn(f"{ARENA} 缺 run_timestamp，grp 名單本輪略過")
        return []
    items = []
    for seat_key, role_label, offset in (
        ("core_seats", "GRP 核心席位", GRP_OFFSETS["核心"]),
        ("sat_seats", "GRP 衛星席位", GRP_OFFSETS["衛星"]),
    ):
        for seat in data.get(seat_key) or []:
            ticker = seat.get("ticker")
            if not ticker:
                continue
            price = (seat.get("grp") or {}).get("price")
            items.append({
                "ticker": ticker,
                "role_label": role_label,
                "base_date": base_date,
                "list_price": price,
                "offset": offset,
                "source_ref": (f"docs/engine/arena.json run_timestamp={data.get('run_timestamp')}"
                               f" seat={seat_key} ticker={ticker}"),
            })
    return items


def extract_picks_items():
    data = _load_json(CANDIDATES)
    if data is None:
        warn(f"{CANDIDATES} 不存在或無法讀取，picks 名單本輪略過")
        return []
    base_date = data.get("as_of")
    if not base_date:
        warn(f"{CANDIDATES} 缺 as_of，picks 名單本輪略過")
        return []
    items = []
    for it in data.get("official_baofa") or []:
        ticker = it.get("ticker")
        if not ticker:
            continue
        items.append({
            "ticker": ticker,
            "role_label": "精選爆發榜",
            "base_date": base_date,
            "list_price": it.get("price"),   # 目前 official_baofa[] 不帶價，恆 None → 走 weekly_cache 退路
            "offset": PICKS_OFFSET,
            "source_ref": f"docs/picks/candidates.json as_of={base_date} ticker={ticker}",
        })
    return items


def extract_tenbagger_items():
    data = _load_json(TENBAGGER)
    if data is None:
        warn(f"{TENBAGGER} 不存在或無法讀取，tenbagger 名單本輪略過")
        return []
    base_date = data.get("as_of")
    if not base_date:
        warn(f"{TENBAGGER} 缺 as_of，tenbagger 名單本輪略過")
        return []
    candidates = (data.get("official") or data.get("candidates") or [])  # 2026-09-02 orchestrator 定案：official[]＝正式席位（本週 5 檔），candidates[] 為候補；席位優先
    if not candidates:
        info(f"docs/picks/tenbagger.json candidates[] 目前為空（0 筆）——"
             f"符合設計稿 §9 row F2 已知現況，本輪 tenbagger n_drafts=0，非錯誤")
    items = []
    for it in candidates:
        ticker = it.get("ticker")
        if not ticker:
            continue
        items.append({
            "ticker": ticker,
            "role_label": "十倍股候選",
            "base_date": base_date,
            "list_price": it.get("price"),   # 目前 schema 不帶價，恆 None → 走 weekly_cache 退路
            "offset": TENBAGGER_OFFSET,
            "source_ref": f"docs/picks/tenbagger.json as_of={base_date} ticker={ticker}",
        })
    return items


EXTRACTORS = {
    "grp": extract_grp_items,
    "picks": extract_picks_items,
    "tenbagger": extract_tenbagger_items,
}


# ═══════════════════════════════════════════════════════════════════════════
# 價格：base_px 退路（weekly_cache）／base_spy（flowmap_prices）
# ═══════════════════════════════════════════════════════════════════════════

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


def _load_flowmap_spy():
    data = _load_json(FLOWMAP_PRICES)
    if not data:
        return None
    bars = (data.get("series") or {}).get("SPY")
    if not bars:
        return None
    return sorted((d, c) for d, c in bars)


def _weekly_cache_close_at_or_before(ticker, ymd):
    fname = ALIAS.get(ticker, ticker)
    path = CACHE_DIR / f"{fname}.json"
    data = _load_json(path)
    if not data:
        return None
    raw = data.get("weekly_bars") or []
    bars = sorted((b["week_end"], b["close"]) for b in raw
                  if b.get("week_end") and b.get("close") is not None)
    if not bars:
        return None
    return _close_at_or_before(bars, ymd)


def p_clim_ref_text(base_rates, p_clim_key):
    cells = (base_rates.get("p_clim_cells") or {}).get(p_clim_key) or {}
    return (f"data/dd_verdict_base_rates.json（借用 p_clim_key={p_clim_key}）"
            f"built_at={base_rates.get('built_at')}｜clim_window_years={base_rates.get('clim_window_years')}｜"
            f"n_cells={cells.get('n_cells')}｜n_tickers={cells.get('n_tickers')}")


def load_base_rates():
    if not BASE_RATES.exists():
        raise SystemExit(f"找不到 {BASE_RATES} —— 先跑 python scripts/build_dd_verdict_base_rates.py")
    try:
        return json.loads(BASE_RATES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {BASE_RATES}: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# 查重（(source, ticker) 為鍵，見檔頭 docstring）
# ═══════════════════════════════════════════════════════════════════════════

def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _existing_open_keys(existing_rows):
    keys = set()
    for r in existing_rows:
        if r.get("status") != "open":
            continue
        source = r.get("source")
        series = (r.get("resolver") or {}).get("series") or ""
        if not series.startswith("relspy:"):
            continue
        ticker = series[len("relspy:"):]
        if source and ticker:
            keys.add((source, ticker))
    return keys


def _local_next_ids(ts_str, prefix, n, existing_rows):
    used = {r.get("id") for r in existing_rows if r.get("id")}
    fullprefix = f"fc_{ts_str.replace('-', '')}_{prefix}_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{fullprefix}{seq:02d}"
        if cand not in used:
            out.append(cand)
            used.add(cand)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

def build_draft(item, spec, ts_str, base_rates, spy_bars):
    ticker = item["ticker"]
    base_date = item["base_date"]
    horizon_days = spec["horizon_days"]
    p_clim_key = spec["p_clim_key"]
    offset = item["offset"]

    p_clim = (base_rates.get("p_clim") or {}).get(p_clim_key)
    if p_clim is None:
        return None, "p_clim_missing"

    base_px = item.get("list_price")
    if base_px is not None:
        base_px_source = "list"
    else:
        hit = _weekly_cache_close_at_or_before(ticker, base_date)
        if hit is None:
            return None, "base_px_missing"
        wc_date, base_px = hit
        base_px_source = f"weekly_cache@{wc_date}"

    if not spy_bars:
        return None, "base_spy_missing"
    spy_hit = _close_at_or_before(spy_bars, base_date)
    if spy_hit is None:
        return None, "base_spy_missing"
    base_spy_date, base_spy_px = spy_hit

    p = round(_clip(p_clim + offset, P_LO, P_HI), 4)
    resolve_by = _plus_days(base_date, horizon_days)
    month_key = base_date[:7]
    episode_id = f"{spec['source']}:{ticker}:{month_key}"
    p_clim_ref = p_clim_ref_text(base_rates, p_clim_key)

    claim = (f"{resolve_by} 前（{item['role_label']} {base_date} 起 {horizon_days} 曆日）："
             f"{ticker} 報酬跑贏 SPY")

    note = (f"{spec['source']} 機械賦值（PREREG offset，非人工判斷）｜role={item['role_label']}｜"
            f"offset={offset:+.2f}｜p_clim[{p_clim_key}]={p_clim}（{p_clim_ref}）｜"
            f"base_date={base_date}｜base_px={base_px}（{base_px_source}）｜"
            f"base_spy={base_spy_px}（{base_spy_date}）｜source_ref={item['source_ref']}")

    draft = {
        "id": None,
        "ts": ts_str,
        "schema": "fc-v2",
        "source": spec["source"],
        "source_ref": item["source_ref"],
        "claim": claim,
        "claim_template": spec["claim_template"],
        "p": p,
        "p_clim": p_clim,
        "p_clim_ref": p_clim_ref,
        "p_table_built_at": base_rates.get("built_at"),
        "horizon_days": horizon_days,
        "resolve_by": resolve_by,
        "resolver": {
            "series": f"relspy:{ticker}",
            "op": ">",
            "value": 0,
            "window": "at_expiry",
            "base_date": base_date,
            "base_px": base_px,
            "base_spy": base_spy_px,
        },
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "episode_id": episode_id,
        "block_key": month_key,
        "twin_of": None,
        "note": note,
    }
    return draft, None


def gather_for_list(list_name, items, ts_str, base_rates, spy_bars, dedupe_keys, skip_counts):
    spec = LIST_SPECS[list_name]
    info(f"{list_name}（source={spec['source']}）：讀到 {len(items)} 筆候選")

    drafts = []
    for item in items:
        ticker = item["ticker"]
        key = (spec["source"], ticker)
        if key in dedupe_keys:
            skip_counts[f"{list_name}:dedupe_open"] += 1
            continue

        resolve_by = _plus_days(item["base_date"], spec["horizon_days"])
        if resolve_by < ts_str:
            skip_counts[f"{list_name}:resolve_by_in_past"] += 1
            warn(f"{list_name}/{ticker}：resolve_by={resolve_by} < today={ts_str}，跳過")
            continue

        draft, skip_reason = build_draft(item, spec, ts_str, base_rates, spy_bars)
        if draft is None:
            skip_counts[f"{list_name}:{skip_reason}"] += 1
            warn(f"{list_name}/{ticker}：{skip_reason}，跳過")
            continue

        drafts.append(draft)
        dedupe_keys.add(key)  # 同批次內同 (source, ticker) 不重複掛（例如同週核心與衛星剛好同檔）

    return drafts


def main():
    ap = argparse.ArgumentParser(
        description="名單 producer（GRP 席位／精選爆發榜／十倍股候選 → 跑贏 SPY 機率命題，設計稿 §9 row F2）")
    ap.add_argument("--list", choices=["grp", "picks", "tenbagger", "all"], default="all",
                     help="只跑指定名單（預設 all＝三個都跑）")
    ap.add_argument("--write", action="store_true",
                     help="append 進 ledger（經 forecast_lib，含哨兵 twin；預設 dry-run）")
    ap.add_argument("--ledger", default=str(FORECASTS_DEFAULT),
                     help=f"覆寫 forecasts.jsonl 路徑（測試用 scratch ledger；預設 {FORECASTS_DEFAULT}）")
    args = ap.parse_args()

    ledger_path = Path(args.ledger)
    lists_to_run = ["grp", "picks", "tenbagger"] if args.list == "all" else [args.list]

    today = date.today()
    ts_str = today.isoformat()

    base_rates = load_base_rates()
    spy_bars = _load_flowmap_spy()
    if not spy_bars:
        warn(f"{FLOWMAP_PRICES} 讀取失敗或無 SPY 序列——所有候選將因 base_spy_missing 被跳過")

    existing = _existing_forecasts(ledger_path)
    dedupe_keys = _existing_open_keys(existing)

    skip_counts = Counter()
    per_list_n_candidates = {}
    per_list_drafts = {}

    fl = None
    if args.write:
        sys.path.insert(0, str(ROOT / "knowledge"))
        try:
            import forecast_lib as fl_mod
            fl = fl_mod
        except ImportError as e:
            print(f"[list-forecasts][ERROR] 找不到 knowledge/forecast_lib.py（{e}）——"
                  f"--write 依賴 A1 package 交付的 forecast_lib.py，尚未就緒。", file=sys.stderr)
            sys.exit(2)

    for list_name in lists_to_run:
        spec = LIST_SPECS[list_name]
        items = EXTRACTORS[list_name]()
        per_list_n_candidates[list_name] = len(items)
        drafts = gather_for_list(list_name, items, ts_str, base_rates, spy_bars, dedupe_keys, skip_counts)

        if drafts:
            if fl is not None:
                ids = fl.next_ids(ts_str, spec["id_prefix"], len(drafts), path=ledger_path)
            else:
                ids = _local_next_ids(ts_str, spec["id_prefix"], len(drafts), existing)
            for draft, rid in zip(drafts, ids):
                draft["id"] = rid

        per_list_drafts[list_name] = drafts

    all_drafts = [d for name in lists_to_run for d in per_list_drafts[name]]
    summary_counts = {name: len(per_list_drafts[name]) for name in lists_to_run}

    if fl is None:
        for d in all_drafts:
            print(json.dumps(d, ensure_ascii=False))
        info(f"summary: n_candidates={per_list_n_candidates} n_drafts={summary_counts} "
             f"skipped={dict(skip_counts)}")
        info(f"dry-run：共 {len(all_drafts)} 筆草案。--write 才會經 forecast_lib append 進 "
             f"{ledger_path}（含哨兵 twin）。")
        return

    fl.finalize(all_drafts)  # block_key 已由 build_draft() 設為 base_date 所在月，finalize 不覆寫
    n_written, n_twins = fl.append(all_drafts, path=ledger_path, write=True)

    info(f"summary: n_candidates={per_list_n_candidates} n_drafts={summary_counts} "
         f"skipped={dict(skip_counts)}")
    print(f"\n# --write：寫入 {n_written} 本尊 + {n_twins} 哨兵 twin → {ledger_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
