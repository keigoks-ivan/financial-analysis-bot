#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_tsmom_forecasts.py — TSMOM（時間序列動能）預測 producer
（forecast ledger v2 §5.2，source: "tsmom"）。

每月首個交易日手動跑（不掛 cron，同 rv/vix/cot producer 慣例）。從
data/trend_track_prices.json 讀 9 個 canonical 資產類別代理（SPY QQQ IWM EFA
EEM TLT IEF GLD + 大宗商品格，DBC 不足 253 筆收盤時 fallback PDBC——判法與
scripts/build_trend_track.py resolve_commodity() 逐字一致）的**當前**收盤與
12-1 訊號（t-252 至 t-21 交易日總報酬，一樣是 scripts/build_trend_track.py 的
定義，本檔自算、不讀 track.json 的簿記），查 data/tsmom_base_rates.json 的
經驗轉移表取 p，機械產生每檔一筆 forecast 草案（最多 9 筆），append 進
knowledge/forecasts.jsonl（source: "tsmom"）：

  「{resolve_by} 前（21 個交易日後）：{ticker} 收盤高於今日 {close}」
  resolver {"series": "ttp:<TICKER>", "op": ">", "value": <今收>, "window": "at_expiry"}

p 值機械賦值：先查該 ticker 在當前 state（in_trend/not_in_trend）下的 own-cell
freq_up；若該格 n < 30（樣本薄，見 data/tsmom_base_rates.json 的
min_cell_n_for_own_table），改用 pooled（9 個 canonical slot 合併）同 state 的
freq_up——查表規則凍結於設計稿
notes/site-internal/root/_forecast_v2_design_20260902.md §5.2，不接受人工覆寫。
p_clim 一律取該 ticker 自己的無條件 freq_up（不論 p 是否 fallback 到 pooled）。

已知的口徑近似（設計稿明文接受，非本檔臨時決定，同 generate_rv_forecasts.py
的先例）：base rate 表用「21 個交易日」向前看，但 forecast 的 resolve_by 用
「30 個曆日」——兩者是同一件事的兩種近似表達（皆≈一個月），非精確對齊。

dry-run 路徑刻意不 import knowledge/forecast_lib.py（該模組由並行的 A1 包
交付，dry-run 執行時可能尚未存在）——id 產生與草案欄位（schema/block_key）
本檔就地實作，不依賴 fl；只有 --write 才 import fl 並透過 fl.next_ids／
fl.append 落帳（含哨兵 twin 產生）。

CLI
---
  python scripts/generate_tsmom_forecasts.py            dry-run，草案印到 stdout（純 JSONL）
  python scripts/generate_tsmom_forecasts.py --write     append 進 knowledge/forecasts.jsonl
                                                          （查重：同 ticker 同 YYYY-MM 已有
                                                          source="tsmom" 筆 → 拒絕該 ticker，
                                                          其餘 ticker 正常落帳）
跳過/拒絕原因印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRICE_CACHE = ROOT / "data" / "trend_track_prices.json"
BASE_RATES = ROOT / "data" / "tsmom_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

SOURCE = "tsmom"
CLAIM_TEMPLATE = "tsmom_up_21d"
SCHEMA_V2 = "fc-v2"
HORIZON_CALENDAR_DAYS = 30   # 曆日近似（base rate 表用 21 交易日，見檔頭 docstring）

# 須與 scripts/build_trend_track.py / scripts/build_tsmom_base_rates.py 逐字一致（PREREG 凍結）
CORE_ROLES = [
    ("SPY", "美股大盤（S&P 500）"),
    ("QQQ", "美股科技（Nasdaq 100）"),
    ("IWM", "美股小型股（Russell 2000）"),
    ("EFA", "成熟市場（歐澳遠東）"),
    ("EEM", "新興市場"),
    ("TLT", "長天期美債（20 年以上）"),
    ("IEF", "中天期美債（7–10 年）"),
    ("GLD", "黃金"),
]
CORE_SYMBOLS = [t for t, _ in CORE_ROLES]
COMMODITY_ROLE = "大宗商品"
COMMODITY_PRIMARY = "DBC"
COMMODITY_FALLBACK = "PDBC"
ROLE_MAP = dict(CORE_ROLES)
ROLE_MAP[COMMODITY_PRIMARY] = COMMODITY_ROLE
ROLE_MAP[COMMODITY_FALLBACK] = COMMODITY_ROLE

MIN_CLOSES = 253   # 資料充足門檻（§G6／build_tsmom_base_rates.py 逐字一致）
FAR_IDX = -253      # ~12 個月前（對齊 build_trend_track.py FAR_IDX）
NEAR_IDX = -22       # ~1 個月前，跳過最近 21 個交易日（對齊 build_trend_track.py NEAR_IDX）


def warn(msg: str) -> None:
    print(f"[tsmom-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[tsmom-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：data/trend_track_prices.json + 12-1 訊號自算（不讀 track.json 簿記）
# ═══════════════════════════════════════════════════════════════════════════

def load_price_series(path=PRICE_CACHE):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_trend_track.py 產生價格快取")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")
    return data.get("series") or {}


def compute_signal(rows):
    """rows: 升冪 [(date, close), ...]。回傳 {"as_of","close","ret_12_1","state"} 或
    None（資料不足 <253 筆，或 far anchor 為 0/None——防禦性 guard，非 §G6 否決條件）。"""
    if not rows or len(rows) < MIN_CLOSES:
        return None
    closes = [c for _, c in rows]
    dates = [d for d, _ in rows]
    far = closes[FAR_IDX]
    near = closes[NEAR_IDX]
    if not far:
        return None
    ret_12_1 = near / far - 1.0
    state = "in_trend" if ret_12_1 > 0 else "not_in_trend"
    return {"as_of": dates[-1], "close": closes[-1], "ret_12_1": round(ret_12_1, 6), "state": state}


def resolve_commodity(series_map):
    """DBC 優先；本期 <MIN_CLOSES 筆則 fallback PDBC；兩者皆不足回傳 (None, [])。
    判法與 scripts/build_trend_track.py resolve_commodity() 逐字一致。"""
    for sym in (COMMODITY_PRIMARY, COMMODITY_FALLBACK):
        rows = series_map.get(sym) or []
        if len(rows) >= MIN_CLOSES:
            return sym, [(d, c) for d, c in rows]
    return None, []


def slots_to_evaluate(series_map):
    """回傳 [(role_symbol_for_lookup, actual_ticker_for_signal, rows), ...] 供 9 個
    canonical slot 各自解析：8 核心資產直接用自身 ticker；大宗商品格用
    resolve_commodity() 決定實際採用 DBC 或 PDBC（該 slot 的「ticker」就是實際採用者，
    base rate 表用同一個 symbol 查表——見設計稿 §5.2「DBC→PDBC fallback」）。"""
    out = []
    for t in CORE_SYMBOLS:
        rows = series_map.get(t) or []
        out.append((t, [(d, c) for d, c in rows]))
    commodity_sym, commodity_rows = resolve_commodity(series_map)
    out.append((commodity_sym, commodity_rows))  # commodity_sym 可能是 None（兩者皆不足）
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：data/tsmom_base_rates.json 經驗轉移表
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates(path=BASE_RATES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_tsmom_base_rates.py")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")


def lookup_p(base_rates, ticker, state):
    """回傳 (p, p_clim, cell_used, n_used) 或 None（表無此 ticker 或 pooled 亦無資料）。
    cell_used ∈ {"own","pooled"}。own-cell n < min_cell_n_for_own_table 時 fallback pooled
    （設計稿 §5.2 凍結規則）。"""
    tickers_tbl = base_rates.get("tickers") or {}
    min_n = base_rates.get("min_cell_n_for_own_table", 30)
    row = tickers_tbl.get(ticker)
    if row is None:
        return None
    p_clim = row.get("p_clim")
    own_cell = (row.get("states") or {}).get(state) or {}
    own_n = own_cell.get("n") or 0
    own_freq = own_cell.get("freq_up")
    if own_freq is not None and own_n >= min_n:
        return own_freq, p_clim, "own", own_n
    pooled = base_rates.get("pooled") or {}
    pooled_cell = (pooled.get("states") or {}).get(state) or {}
    pooled_freq = pooled_cell.get("freq_up")
    pooled_n = pooled_cell.get("n") or 0
    if pooled_freq is None:
        return None
    return pooled_freq, p_clim, "pooled", pooled_n


# ═══════════════════════════════════════════════════════════════════════════
# id 產生（dry-run 本地實作，pattern 與 fl.next_ids 一致：fc_{YYYYMMDD}_tsmom_{NN}）
# ═══════════════════════════════════════════════════════════════════════════

def _local_next_ids(ts_str, n, path=FORECASTS):
    used = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rid = json.loads(line).get("id", "")
            except json.JSONDecodeError:
                continue
            used.add(rid)
    prefix = f"fc_{ts_str.replace('-', '')}_tsmom_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{prefix}{seq:02d}"
        if cand not in used:
            out.append(cand)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 查重
# ═══════════════════════════════════════════════════════════════════════════

def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def already_has_episode(existing, episode_id, source=SOURCE):
    return any(r.get("source") == source and r.get("episode_id") == episode_id for r in existing)


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

def build_drafts(today=None, price_path=PRICE_CACHE, base_rates_path=BASE_RATES,
                  forecasts_path=FORECASTS):
    """回傳 (drafts, skipped)。skipped: [(role_ticker_or_'commodity', reason), ...]。"""
    today = today or date.today()
    ts_str = today.isoformat()
    month_key = ts_str[:7]
    resolve_by = (today + timedelta(days=HORIZON_CALENDAR_DAYS)).isoformat()
    block_key = month_key

    series_map = load_price_series(price_path)
    base_rates = load_base_rates(base_rates_path)
    table_built_at = base_rates.get("built_at")
    existing = _existing_forecasts(forecasts_path)

    drafts = []
    skipped = []

    for slot_ticker, rows in slots_to_evaluate(series_map):
        if slot_ticker is None:
            skipped.append(("commodity", "DBC 與 PDBC 皆 <253 筆收盤，本期無法算 12-1 訊號，商品格略過"))
            continue

        sig = compute_signal(rows)
        if sig is None:
            skipped.append((slot_ticker, f"{slot_ticker}：收盤筆數不足 {MIN_CLOSES}（實得 {len(rows)}）"
                                          "或 far anchor 為 0，無法算 12-1 訊號，略過"))
            continue

        episode_id = f"tsmom:{month_key}:{slot_ticker}"
        if already_has_episode(existing, episode_id):
            skipped.append((slot_ticker, f"{episode_id} 已有 source={SOURCE} 落帳紀錄，本月本檔拒絕重複落帳"))
            continue

        lookup = lookup_p(base_rates, slot_ticker, sig["state"])
        if lookup is None:
            skipped.append((slot_ticker, f"data/tsmom_base_rates.json 查無 {slot_ticker} 的表格資料（own 與 pooled 皆無），略過"))
            continue
        p, p_clim, cell_used, n_used = lookup

        close = sig["close"]
        as_of = sig["as_of"]

        p_clim_ref = (f"data/tsmom_base_rates.json built_at={table_built_at}｜ticker={slot_ticker} "
                      f"全取樣點無條件 freq_up")
        source_ref = (f"data/trend_track_prices.json {slot_ticker} as_of={as_of}｜"
                      f"data/tsmom_base_rates.json built_at={table_built_at}｜"
                      f"state={sig['state']}｜cell={cell_used}(n={n_used})")

        draft = {
            "id": None,  # 由 dry-run 本地 id 或 fl.next_ids 補
            "ts": ts_str,
            "source": SOURCE,
            "source_ref": source_ref,
            "claim": f"{resolve_by} 前（21 個交易日後）：{slot_ticker} 收盤高於今日 {close}",
            "p": p,
            "horizon_days": HORIZON_CALENDAR_DAYS,
            "resolve_by": resolve_by,
            "resolver": {"series": f"ttp:{slot_ticker}", "op": ">", "value": close, "window": "at_expiry"},
            "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
            "note": (f"tsmom 機械賦值（無需人工判斷）｜今日收盤={close}（as_of {as_of}）｜"
                     f"12-1 訊號 ret_12_1={sig['ret_12_1']}｜state={sig['state']}｜"
                     f"p={p}（來自 {cell_used}-cell, n={n_used}）｜p_clim={p_clim}（{slot_ticker} 無條件 freq_up）｜"
                     f"base_rates built_at={table_built_at}"),
            "schema": SCHEMA_V2,
            "claim_template": CLAIM_TEMPLATE,
            "p_clim": p_clim,
            "p_clim_ref": p_clim_ref,
            "p_table_built_at": table_built_at,
            "episode_id": episode_id,
            "block_key": block_key,
            "twin_of": None,
        }
        drafts.append(draft)

    return drafts, skipped


# ═══════════════════════════════════════════════════════════════════════════
# 落帳
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="TSMOM 預測 producer — 月頻手動觸發")
    ap.add_argument("--write", action="store_true", help="append 進 knowledge/forecasts.jsonl（預設 dry-run）")
    args = ap.parse_args()

    today = date.today()
    ts_str = today.isoformat()
    drafts, skipped = build_drafts(today=today)

    for reason_ticker, reason in skipped:
        warn(f"skip {reason_ticker}: {reason}")

    if not drafts:
        info("無草案（全部 slot 被略過，見上方 stderr 原因），不輸出、不落帳。")
        return

    if not args.write:
        ids = _local_next_ids(ts_str, len(drafts))
        for d, rid in zip(drafts, ids):
            d["id"] = rid
            print(json.dumps(d, ensure_ascii=False))
        info(f"dry-run：共 {len(drafts)} 筆草案（{len(skipped)} 個 slot 略過）。"
             f"--write 才會 append 進 {FORECASTS}。")
        return

    try:
        sys.path.insert(0, str(ROOT / "knowledge"))
        import forecast_lib as fl  # noqa: E402
    except ImportError as e:
        print(f"[tsmom-forecasts][ERROR] 找不到 knowledge/forecast_lib.py（{e}）——"
              "--write 依賴該模組（帳簿核心包 A1 交付），無法落帳。", file=sys.stderr)
        sys.exit(2)

    ids = fl.next_ids(ts_str, "tsmom", len(drafts), FORECASTS)
    for d, rid in zip(drafts, ids):
        d["id"] = rid

    n_written, n_twins = fl.append(drafts, path=FORECASTS, write=True)
    for d in drafts:
        print(json.dumps(d, ensure_ascii=False))
    info(f"--write：寫入 {n_written} 筆本尊 + {n_twins} 筆哨兵 twin → {FORECASTS}"
         f"（{len(skipped)} 個 slot 略過）")


if __name__ == "__main__":
    main()
