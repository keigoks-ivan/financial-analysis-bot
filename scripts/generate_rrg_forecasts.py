#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_rrg_forecasts.py — RRG 類股輪動預測 producer
（forecast ledger v2 `_market_cockpit_design_20260902.md` §9 package F5，source="rrg-sector"）。

每月首週手動跑（不掛 cron，同 risk-gauge／vrp producer「先手動、養出使用習慣」慣例；設計稿
§9 F5 節奏欄：「每月首週（查重同月）」）。對 11 檔 SPDR 類股 ETF（XLK/XLC/XLY/XLP/XLV/XLF/
XLI/XLE/XLB/XLRE/XLU）各自對 SPY，用 `scripts/build_rotation_radar.py` 的 frame 120 公式
（逐字重用，`import build_rotation_radar as brr`，呼叫 `brr.quadrant()`／`brr._compute_frames()`
——同 `scripts/build_rrg_base_rates.py` 的 import 慣例）算出**目前**（`data/statlab_prices.json`
最新一筆）rs_ratio／rs_mom，分類進四象限（leading／weakening／lagging／improving），查
`data/rrg_base_rates.json` 的象限經驗轉移表取 p（own-cell n>=30 用 own，否則退回 pooled 同
象限格），每檔一筆草案（最多 11 筆），append 進 `knowledge/forecasts.jsonl`（source="rrg-sector"）：

  「{resolve_by} 前（63 個交易日）：{ETF} 報酬跑贏 SPY（輪動象限 {quadrant 白話}）」
  claim_template=rrg_beat_spy_63d
  resolver relspy:{ETF}，base_date=as_of（statlab 最新收盤日），base_px=ETF 收盤，
  base_spy=SPY 同日收盤，horizon=91 曆日（63 交易日的曆日近似）

p 值機械賦值：查 `data/rrg_base_rates.json` 該 ETF 在目前象限下的 own-cell freq_beat；若該格
n < `min_cell_n_for_own_table`（樣本薄），改用 pooled（11 檔合併）同象限 freq_beat——查表規則
與 `scripts/generate_tsmom_forecasts.py` 的 own/pooled fallback 邏輯同構。p_clim 一律取該 ETF
自己的無條件 freq_beat（不論 p 是否 fallback 到 pooled）。若連 pooled 格都 n<30（樣本極薄），
note 欄額外記 `confidence=lo`（設計稿 §9 F5「樣本薄標 lo」的操作化——見
`scripts/build_rrg_base_rates.py` 檔頭「誠實註記」對這句的解讀）。

交叉核對（非落帳邏輯，僅診斷輸出）
----------------------------------
同時讀 `docs/rotation/data/radar.json` 的 `us_sectors` 宇宙 frame 120 最新 trail 點，與本檔
自算結果並列印出（stderr）——兩者價格來源管線不同（radar.json 走 yfinance/stooq 每日增量
快取＋自己的 rotation_radar_daily.json；本檔走 `data/statlab_prices.json` 另一條獨立快取），
數值理應接近但不保證逐位元相同；quadrant 不同、或 |Δr|>1.0、或 |Δm|>1.0 時印 MISMATCH 警告，
**不影響落帳**——本檔的 p／base_px／base_spy 一律以自算的 statlab 數字為準，不採 radar.json
的數字（避免落帳邏輯依賴另一條 pipeline 的 as-of 時效）。

已知的口徑近似（設計稿明文接受，同 tsmom／risk-gauge producer 先例）
---------------------------------------------------------------------
base rate 表用「63 個交易日」向前看，但 forecast 的 `resolve_by` 用「91 個曆日」——兩者是
同一件事的兩種近似表達（皆≈一季），非精確對齊。

已知限制：weekly_cache 缺口（本檔不處理，誠實記錄）
----------------------------------------------------
`knowledge/settle_forecasts.py` 的 `relspy:` 域在 `resolve_by` 到期結算時讀
`data/weekly_cache/<TICKER>.json` 取 px_T（同 `price:` 域慣例，見該檔 `_price_bars()`），
但截至本檔交付時，`data/weekly_cache/` 只涵蓋 DD 覆蓋的個股，**不含任何 SPDR 類股 ETF**
（`ls data/weekly_cache | grep -i '^XL'` 為空）。本包 11 檔草案落帳後，到期結算時大機率會
`status=void`（`reason=relspy_missing_price:<ETF>`），除非另有管線把 XLK…XLU 的週線收盤餵進
`data/weekly_cache/`（例如比照 `weekly-fundamental-refresh.yml` 但擴及這 11 檔 ETF）。本檔
**不**在落帳前做 weekly_cache 存在性檢查（不像 `generate_dd_verdict_forecasts.py` 對
`decisions.jsonl` 任意 ticker 做 gate）——因為本包的 11 檔 ETF 宇宙是固定、已知、非任意輸入
的，設計稿 §9 F5 明文要求「11 檔」草案，本檔照樣機械產生 11 筆，不因下游可能 void 而自行
減產；這個缺口需要 F6（接線與治理）或後續校準輪處理，不在本包（builder + producer 兩檔）
範圍內。

CLI
---
  python scripts/generate_rrg_forecasts.py             dry-run，草案印到 stdout（純 JSONL）+
                                                          交叉核對表印到 stderr
  python scripts/generate_rrg_forecasts.py --write      append 進 knowledge/forecasts.jsonl
                                                          （查重：同 ETF 同 YYYY-MM 已有
                                                          source="rrg-sector" 筆 → 拒絕該 ETF，
                                                          其餘 ETF 正常落帳；經 forecast_lib，
                                                          含哨兵 twin）
  python scripts/generate_rrg_forecasts.py --ledger /path/to/scratch.jsonl [--write]
                                                          測試用：覆寫查重／落帳目標路徑
訊息（掃描摘要／跳過原因／交叉核對）一律印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATLAB_PRICES = ROOT / "data" / "statlab_prices.json"
BASE_RATES = ROOT / "data" / "rrg_base_rates.json"
RADAR = ROOT / "docs" / "rotation" / "data" / "radar.json"
FORECASTS_DEFAULT = ROOT / "knowledge" / "forecasts.jsonl"

sys.path.insert(0, str(ROOT / "scripts"))
import build_rotation_radar as brr  # noqa: E402 — quadrant()/_compute_frames()/FRAMES 逐字重用

sys.path.insert(0, str(ROOT / "knowledge"))
import forecast_lib as fl  # noqa: E402 — id 產生／v2 欄位補齊／落帳＋哨兵 twin

SOURCE = "rrg-sector"
ID_PREFIX = "rrg"
CLAIM_TEMPLATE = "rrg_beat_spy_63d"
FRAME_KEY = "120"
BENCH = "SPY"
HORIZON_CALENDAR_DAYS = 91   # 63 交易日的曆日近似（同 tsmom／risk-gauge producer 既有取捨）
OUTCOME_WINDOW_TD = 63
CROSSCHECK_TOL = 1.0         # r／m 差異超過此值即印 MISMATCH（診斷用，非落帳門檻）

QUAD_LABEL_ZH = {"leading": "領先", "weakening": "轉弱", "lagging": "落後", "improving": "改善"}

# 逐字同 scripts/build_rrg_base_rates.py SECTOR_ETFS（= build_rotation_radar.py
# UNIVERSES["us_sectors"] members，排除 SMH——半導體 ETF 非 SPDR 板塊基金）
SECTOR_ETFS = [
    ("XLK", "科技"), ("XLC", "通訊服務"), ("XLY", "非必需消費"), ("XLP", "必需消費"),
    ("XLV", "醫療保健"), ("XLF", "金融"), ("XLI", "工業"), ("XLE", "能源"),
    ("XLB", "原物料"), ("XLRE", "房地產"), ("XLU", "公用事業"),
]


def warn(msg: str) -> None:
    print(f"[rrg-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[rrg-forecasts] {msg}", file=sys.stderr)


def _plus_days(ymd, n):
    y, m, d = map(int, ymd.split("-"))
    return (date(y, m, d) + timedelta(days=n)).isoformat()


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：data/statlab_prices.json + 目前 frame 120 訊號（本檔自算，不讀 radar.json 簿記）
# ═══════════════════════════════════════════════════════════════════════════

def load_statlab(path=STATLAB_PRICES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_statlab.py")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")
    return data, (data.get("series") or {})


def _to_series(pts, pd):
    idx = [pd.Timestamp(d) for d, _ in pts]
    return pd.Series([float(c) for _, c in pts], index=idx).sort_index()


def compute_current(spy_s, member_s, pd):
    """回傳 dict 或 None（歷史不足）：{"as_of","close","spy_close","r","m","quadrant"}。"""
    grid = spy_s.index
    aligned = member_s.reindex(grid).ffill()
    rs = 100.0 * aligned / spy_s
    rs = rs.dropna()
    if rs.empty:
        return None
    frames, series_by_frame = brr._compute_frames(rs, aligned, spy_s, pd)
    full = series_by_frame.get(FRAME_KEY)
    if full is None or full.empty:
        return None
    last_ts = full.index[-1]
    r, m = (float(v) for v in full.loc[last_ts].values)
    q = brr.quadrant(r, m)
    return {
        "as_of": last_ts.strftime("%Y-%m-%d"),
        "close": float(aligned.loc[last_ts]),
        "spy_close": float(spy_s.loc[last_ts]),
        "r": round(r, 3), "m": round(m, 3), "quadrant": q,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：data/rrg_base_rates.json 象限經驗轉移表
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates(path=BASE_RATES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_rrg_base_rates.py")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")


def lookup_p(base_rates, etf, quadrant):
    """回傳 (p, p_clim, cell_used, n_used, lo_sample) 或 None（表無此 ETF 或 pooled 亦無資料）。
    cell_used ∈ {"own","pooled"}。own-cell n < min_cell_n_for_own_table 時 fallback pooled
    （設計稿 §9 F5 凍結規則）。lo_sample＝實際採用的那一格（own 或 fallback 後的 pooled）
    n 是否仍 < min_cell_n_for_own_table。"""
    tickers_tbl = base_rates.get("tickers") or {}
    min_n = base_rates.get("min_cell_n_for_own_table", 30)
    row = tickers_tbl.get(etf)
    if row is None:
        return None
    p_clim = row.get("p_clim")
    own_cell = (row.get("quadrants") or {}).get(quadrant) or {}
    own_n = own_cell.get("n") or 0
    own_freq = own_cell.get("freq_beat")
    if own_freq is not None and own_n >= min_n:
        return own_freq, p_clim, "own", own_n, False
    pooled = base_rates.get("pooled") or {}
    pooled_cell = (pooled.get("quadrants") or {}).get(quadrant) or {}
    pooled_freq = pooled_cell.get("freq_beat")
    pooled_n = pooled_cell.get("n") or 0
    if pooled_freq is None:
        return None
    return pooled_freq, p_clim, "pooled", pooled_n, pooled_n < min_n


# ═══════════════════════════════════════════════════════════════════════════
# 交叉核對：docs/rotation/data/radar.json us_sectors frame 120 最新點
# ═══════════════════════════════════════════════════════════════════════════

def load_radar_crosscheck(path=RADAR):
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {path}（交叉核對將略過）: {e}")
        return {}
    out = {}
    for uni in data.get("universes") or []:
        if uni.get("key") != "us_sectors":
            continue
        for m in uni.get("members") or []:
            if m.get("status") != "ok":
                continue
            trail = ((m.get("frames") or {}).get(FRAME_KEY) or {}).get("trail") or []
            if not trail:
                continue
            last = trail[-1]
            out[m["ticker"]] = {"d": last.get("d"), "r": last.get("r"), "m": last.get("m")}
    return out


def print_crosscheck(signals, radar_cc):
    info("── 交叉核對：本檔自算（statlab, frame 120）vs docs/rotation/data/radar.json us_sectors frame 120 ──")
    for etf, _ in SECTOR_ETFS:
        sig = signals.get(etf)
        cc = radar_cc.get(etf)
        if sig is None:
            info(f"  {etf:<5} 本檔=無資料（歷史不足）")
            continue
        mine = f"as_of={sig['as_of']} r={sig['r']:<8} m={sig['m']:<8} quadrant={sig['quadrant']}"
        if cc is None or cc.get("r") is None or cc.get("m") is None:
            info(f"  {etf:<5} 本檔[{mine}]  radar.json=無資料")
            continue
        radar_q = brr.quadrant(cc["r"], cc["m"])
        flag = ""
        if radar_q != sig["quadrant"]:
            flag = "  ⚠ MISMATCH quadrant"
        elif abs(cc["r"] - sig["r"]) > CROSSCHECK_TOL:
            flag = f"  ⚠ MISMATCH r (Δ={cc['r'] - sig['r']:+.2f})"
        elif abs(cc["m"] - sig["m"]) > CROSSCHECK_TOL:
            flag = f"  ⚠ MISMATCH m (Δ={cc['m'] - sig['m']:+.2f})"
        info(f"  {etf:<5} 本檔[{mine}]  radar.json[d={cc['d']} r={cc['r']:<8} m={cc['m']:<8} "
             f"quadrant={radar_q}]{flag}")


# ═══════════════════════════════════════════════════════════════════════════
# 查重（episode_id 為鍵，設計稿 §9 F5："rrg:{YYYY-MM}:{ETF}／月"）
# ═══════════════════════════════════════════════════════════════════════════

def already_has_episode(existing_rows, episode_id, source=SOURCE):
    return any(r.get("source") == source and r.get("episode_id") == episode_id for r in existing_rows)


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

def build_draft(etf, sig, base_rates, ts_str, existing_rows):
    month_key = sig["as_of"][:7]
    episode_id = f"rrg:{month_key}:{etf}"
    if already_has_episode(existing_rows, episode_id):
        return None, f"{episode_id} 已有 source={SOURCE} 落帳紀錄，本月本檔拒絕重複落帳"

    lookup = lookup_p(base_rates, etf, sig["quadrant"])
    if lookup is None:
        return None, f"data/rrg_base_rates.json 查無 {etf} 的表格資料（own 與 pooled 皆無）"
    p, p_clim, cell_used, n_used, lo_sample = lookup

    resolve_by = _plus_days(sig["as_of"], HORIZON_CALENDAR_DAYS)
    if resolve_by < ts_str:
        return None, f"resolve_by={resolve_by} < today={ts_str}"

    quad_zh = QUAD_LABEL_ZH.get(sig["quadrant"], sig["quadrant"])
    claim = f"{resolve_by} 前（63 個交易日）：{etf} 報酬跑贏 SPY（輪動象限 {quad_zh}）"

    p_clim_ref = (f"data/rrg_base_rates.json built_at={base_rates.get('built_at')}｜"
                  f"ticker={etf} 全取樣點無條件 freq_beat")
    source_ref = (f"data/statlab_prices.json {etf} as_of={sig['as_of']}｜"
                  f"data/rrg_base_rates.json built_at={base_rates.get('built_at')}｜"
                  f"quadrant={sig['quadrant']}｜cell={cell_used}(n={n_used})")

    confidence_note = f"｜confidence=lo（{cell_used}-cell n={n_used}<min_cell_n）" if lo_sample else ""
    note = (f"rrg-sector 機械賦值（無需人工判斷）｜as_of={sig['as_of']}｜close={sig['close']}｜"
            f"r={sig['r']} m={sig['m']}｜quadrant={sig['quadrant']}｜"
            f"p={p}（來自 {cell_used}-cell, n={n_used}）｜p_clim={p_clim}（{etf} 無條件 freq_beat）｜"
            f"base_rates built_at={base_rates.get('built_at')}{confidence_note}")

    draft = {
        "id": None,
        "ts": ts_str,
        "schema": fl.SCHEMA_V2,
        "source": SOURCE,
        "source_ref": source_ref,
        "claim": claim,
        "claim_template": CLAIM_TEMPLATE,
        "p": p,
        "p_clim": p_clim,
        "p_clim_ref": p_clim_ref,
        "p_table_built_at": base_rates.get("built_at"),
        "horizon_days": HORIZON_CALENDAR_DAYS,
        "resolve_by": resolve_by,
        "resolver": {
            "series": f"relspy:{etf}",
            "op": ">", "value": 0, "window": "at_expiry",
            "base_date": sig["as_of"], "base_px": sig["close"], "base_spy": sig["spy_close"],
        },
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "episode_id": episode_id,
        "block_key": month_key,
        "twin_of": None,
        "note": note,
    }
    return draft, None


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="RRG 類股輪動預測 producer（設計稿 §9 row F5）— 月頻手動觸發")
    ap.add_argument("--write", action="store_true",
                     help="append 進 ledger（經 forecast_lib，含哨兵 twin；預設 dry-run）")
    ap.add_argument("--ledger", default=str(FORECASTS_DEFAULT),
                     help=f"覆寫查重／落帳目標路徑（測試用 scratch ledger；預設 {FORECASTS_DEFAULT}）")
    args = ap.parse_args()

    ledger_path = Path(args.ledger)
    today = date.today()
    ts_str = today.isoformat()

    import pandas as pd

    statlab_meta, series = load_statlab()
    if BENCH not in series:
        raise SystemExit(f"{STATLAB_PRICES} 缺 {BENCH} 序列")
    spy_s = _to_series(series[BENCH], pd)

    base_rates = load_base_rates()
    radar_cc = load_radar_crosscheck()

    existing_rows = fl.existing(ledger_path)

    skip_counts = Counter()
    signals = {}
    drafts = []

    for etf, label in SECTOR_ETFS:
        if etf not in series or not series[etf]:
            skip_counts["ticker_missing_in_statlab"] += 1
            warn(f"{etf}：{STATLAB_PRICES} 無此序列，跳過")
            continue
        member_s = _to_series(series[etf], pd)
        sig = compute_current(spy_s, member_s, pd)
        if sig is None:
            skip_counts["insufficient_history"] += 1
            warn(f"{etf}：歷史不足以算 frame 120（暖身門檻），跳過")
            continue
        signals[etf] = sig

        draft, skip_reason = build_draft(etf, sig, base_rates, ts_str, existing_rows)
        if draft is None:
            skip_counts["skipped"] += 1
            warn(f"{etf}：{skip_reason}，跳過")
            continue
        drafts.append(draft)
        existing_rows.append(draft)  # 同批次內防重複（11 檔各不相同 ticker，理論上不會撞，仍比照 F2 慣例保險）

    print_crosscheck(signals, radar_cc)

    if not args.write:
        ids = fl.next_ids(ts_str, ID_PREFIX, len(drafts), path=ledger_path) if drafts else []
        for d, rid in zip(drafts, ids):
            d["id"] = rid
        if drafts:
            fl.finalize(drafts)
        for d in drafts:
            print(json.dumps(d, ensure_ascii=False))
        info(f"summary: n_signals={len(signals)} n_drafts={len(drafts)} skipped={dict(skip_counts)}")
        info(f"dry-run：共 {len(drafts)} 筆草案。--write 才會經 forecast_lib append 進 {ledger_path}"
             f"（含哨兵 twin）。")
        return

    if not drafts:
        info(f"summary: n_signals={len(signals)} n_drafts=0 skipped={dict(skip_counts)}")
        info("無草案（全部 ETF 被略過，見上方 stderr 原因），不落帳。")
        return

    ids = fl.next_ids(ts_str, ID_PREFIX, len(drafts), path=ledger_path)
    for d, rid in zip(drafts, ids):
        d["id"] = rid
    fl.finalize(drafts)
    n_written, n_twins = fl.append(drafts, path=ledger_path, write=True)

    info(f"summary: n_signals={len(signals)} n_drafts={len(drafts)} skipped={dict(skip_counts)}")
    print(f"\n# --write：寫入 {n_written} 本尊 + {n_twins} 哨兵 twin → {ledger_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
