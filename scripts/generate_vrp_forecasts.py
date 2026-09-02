#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_vrp_forecasts.py — VRP（波動風險溢酬）預測 producer（forecast ledger v2
package C 機械餵料）。

每月首個交易日手動跑（不掛 cron，先養習慣——沿用 scripts/generate_rv_forecasts.py 的
「先手動、養出使用習慣後再考慮排程」慣例）。從 data/statlab_prices.json 取 ^VIX 與 SPY
最新共同交易日，算當前 VRP_t = VIX_t² − RV21_t²（RV21 口徑逐字同
scripts/build_rv_base_rates.py／scripts/build_vrp_base_rates.py），查
data/vrp_base_rates.json 的三分位表分類，機械產生兩筆 forecast 草案（同一 episode_id，
不同 horizon），append 進 knowledge/forecasts.jsonl（source: "vrp"）：

  ① claim_template=vrp_spy_up_21d：{resolve_by}（30 曆日後）SPY 收盤高於今日
     resolver window=at_expiry, series=pxd:SPY, op=">"
  ② claim_template=vrp_spy_up_63d：{resolve_by}（91 曆日後）SPY 收盤高於今日
     resolver window=at_expiry, series=pxd:SPY, op=">"（同一 resolver.value）

p 值完全由三分位表機械給出（該分位的經驗頻率）——不需人工判斷、也不接受人工覆寫。
p_clim 取自同表的無條件頻率（同一取樣點、同一窗口，設計稿 §3.1）。

已知的口徑近似（設計稿 §5.3 明文接受）：base rate 表用「21／63 個交易日」向前看，但
forecast 的 resolve_by 用「30／91 個曆日」（含週末假日）——兩者是同一件事的兩種近似表達，
非精確對齊，此為既有 rv-model producer 的既有取捨的延伸。

CLI
---
  python scripts/generate_vrp_forecasts.py            dry-run，兩筆草案印到 stdout（純 JSONL）
  python scripts/generate_vrp_forecasts.py --write     append 進 knowledge/forecasts.jsonl
                                                        （查重：同一 YYYY-MM 若已有 source=
                                                        "vrp" 的筆數，整批拒絕落帳）
跳過/拒絕原因印到 stderr，不混進 stdout 的 JSONL 草案。

dry-run 路徑刻意不 import knowledge/forecast_lib.py（package A1 交付、可能尚未存在）——
只有 --write 路徑才 import，缺檔時清楚印訊息到 stderr 並 exit 2（發包分工見設計稿 §7）。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATLAB_PRICES = ROOT / "data" / "statlab_prices.json"
BASE_RATES = ROOT / "data" / "vrp_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

SOURCE = "vrp"
SCHEMA = "fc-v2"
VIX_TICKER = "^VIX"
SPY_TICKER = "SPY"
RV_WINDOW_TRADING_DAYS = 21  # 須與 build_vrp_base_rates.py 一致（PREREG 凍結，僅供口徑核對）

TEMPLATES = [
    # (claim_template, up_key, horizon_calendar_days, trading_days_label)
    ("vrp_spy_up_21d", "freq_up_21d", 30, 21),
    ("vrp_spy_up_63d", "freq_up_63d", 91, 63),
]


def warn(msg: str) -> None:
    print(f"[vrp-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[vrp-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：當前 VRP（data/statlab_prices.json，^VIX 與 SPY 最新共同交易日）
# ═══════════════════════════════════════════════════════════════════════════

def _sample_std(xs):
    n = len(xs)
    if n < 2:
        return None
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / (n - 1)
    return var ** 0.5


def _load_series(data, ticker):
    bars = (data.get("series") or {}).get(ticker)
    if not bars:
        return None
    return sorted(((d, c) for d, c in bars), key=lambda x: x[0])


def current_vrp(prices_path=STATLAB_PRICES, vix_ticker=VIX_TICKER, spy_ticker=SPY_TICKER,
                 window=RV_WINDOW_TRADING_DAYS):
    """回傳 (common_date, vix_close, rv21_pct, spy_close, vrp) 或全 None（資料不足/缺檔）。
    common_date = ^VIX 與 SPY 的最新共同交易日；RV21 用 SPY 自身序列、以 common_date 為
    結尾的 21 個對數報酬年化 sample std（ddof=1）×sqrt(252)×100，口徑逐字同
    scripts/build_rv_base_rates.py／scripts/build_vrp_base_rates.py。"""
    if not prices_path.exists():
        return None, None, None, None, None
    try:
        data = json.loads(prices_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {prices_path}: {e}")
        return None, None, None, None, None

    vix_bars = _load_series(data, vix_ticker)
    spy_bars = _load_series(data, spy_ticker)
    if not vix_bars or not spy_bars:
        return None, None, None, None, None

    vix_map = dict(vix_bars)
    spy_dates = [d for d, _ in spy_bars]
    spy_closes = [c for _, c in spy_bars]
    spy_idx = {d: i for i, d in enumerate(spy_dates)}

    common_dates = sorted(set(vix_map) & set(spy_idx))
    if not common_dates:
        warn(f"{prices_path} 的 {vix_ticker} 與 {spy_ticker} 無共同交易日")
        return None, None, None, None, None

    common_date = common_dates[-1]
    idx = spy_idx[common_date]
    if idx < window:
        warn(f"{spy_ticker} 在 {common_date} 之前歷史不足 {window} 根日線，無法算 RV21")
        return None, None, None, None, None

    window_closes = spy_closes[idx - window: idx + 1]
    if len(window_closes) != window + 1:
        return None, None, None, None, None
    rets = [math.log(window_closes[i] / window_closes[i - 1]) for i in range(1, len(window_closes))
            if window_closes[i - 1] > 0 and window_closes[i] > 0]
    if len(rets) != window:
        return None, None, None, None, None
    s = _sample_std(rets)
    if s is None:
        return None, None, None, None, None
    rv21 = round(s * math.sqrt(252) * 100, 4)

    vix_close = vix_map[common_date]
    spy_close = spy_closes[idx]
    vrp = round(vix_close ** 2 - rv21 ** 2, 4)
    return common_date, vix_close, rv21, spy_close, vrp


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：三分位 base rate 表（data/vrp_base_rates.json）
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates(path=BASE_RATES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_vrp_base_rates.py")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")


def classify_tercile(vrp, cutoffs):
    c33, c67 = cutoffs
    if vrp <= c33:
        return "T1"
    if vrp <= c67:
        return "T2"
    return "T3"


def lookup_tercile_row(base_rates, vrp):
    cutoffs = base_rates["tercile_cutoffs_pct33_67"]
    t = classify_tercile(vrp, cutoffs)
    row = next((r for r in base_rates["terciles"] if r["tercile"] == t), None)
    if row is None or row.get("n", 0) == 0:
        raise SystemExit(f"分位 {t} 樣本數為 0，base rate 表異常，中止（不可硬猜 p）")
    return t, row


# ═══════════════════════════════════════════════════════════════════════════
# id 產生（dry-run 本地版；--write 改走 forecast_lib.next_ids）
# ═══════════════════════════════════════════════════════════════════════════

def _local_next_ids(ts_str, n, path=FORECASTS):
    """回傳 n 個未被佔用的 fc_{YYYYMMDD}_vrp_NN id（掃現有檔避免同日重跑撞號）。
    僅供 dry-run 使用；--write 路徑改用 knowledge/forecast_lib.py 的 fl.next_ids
    （package A1 交付，單一權威來源）。"""
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
    prefix = f"fc_{ts_str.replace('-', '')}_{SOURCE}_"
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

def build_drafts(ids, today=None, prices_path=STATLAB_PRICES, base_rates_path=BASE_RATES):
    today = today or date.today()
    ts_str = today.isoformat()
    month_prefix = today.strftime("%Y-%m")

    common_date, vix_close, rv21, spy_close, vrp = current_vrp(prices_path)
    if vrp is None:
        raise SystemExit(f"無法從 {prices_path} 算出當前 VRP（^VIX／SPY 歷史不足或缺檔），中止")

    base_rates = load_base_rates(base_rates_path)
    tercile, row = lookup_tercile_row(base_rates, vrp)
    p_clim_table = base_rates.get("p_clim", {})

    base_meta = (f"base_rate built_at={base_rates.get('built_at')}｜tercile={tercile}"
                 f"（range={row.get('vrp_range')}, n={row.get('n')}）｜"
                 f"tercile_cutoffs={base_rates.get('tercile_cutoffs_pct33_67')}")
    source_ref = (f"data/statlab_prices.json ^VIX/SPY common_date={common_date}｜"
                  f"data/vrp_base_rates.json {base_meta}")

    drafts = []
    episode_id = f"vrp:{month_prefix}"
    block_key = month_prefix

    for i, (claim_template, freq_key, horizon_days, td_label) in enumerate(TEMPLATES):
        p = row.get(freq_key)
        if p is None:
            raise SystemExit(f"tercile {tercile} 的 {freq_key} 為 null，base rate 表異常，中止")
        p_clim = p_clim_table.get(claim_template)
        resolve_by = (today + timedelta(days=horizon_days)).isoformat()

        claim = (f"{resolve_by} 前（{td_label} 個交易日後）：SPY 收盤高於今日 {spy_close}"
                 f"（VRP 第 {tercile[1]} 分位＝{row.get('description')}）")

        draft = {
            "id": ids[i],
            "ts": ts_str,
            "source": SOURCE,
            "source_ref": source_ref,
            "claim": claim,
            "p": p,
            "horizon_days": horizon_days,
            "resolve_by": resolve_by,
            "resolver": {"series": f"pxd:{SPY_TICKER}", "op": ">", "value": spy_close, "window": "at_expiry"},
            "status": "open",
            "resolved_ts": None,
            "outcome": None,
            "brier": None,
            "note": (f"vrp 機械賦值（無需人工判斷）｜今日 VIX={vix_close}、RV21={rv21}%、"
                     f"VRP={vrp}（as_of {common_date}）｜分位={tercile}｜p 取自三分位表 {freq_key}｜"
                     f"{base_meta}"),
            # schema v2 additive 欄位（設計稿 §2）——dry-run 亦直接填齊，寫檔路徑
            # forecast_lib.finalize/append 對已齊欄位為冪等覆核，不重算既有值。
            "schema": SCHEMA,
            "claim_template": claim_template,
            "p_clim": p_clim,
            "p_clim_ref": (f"data/vrp_base_rates.json built_at={base_rates.get('built_at')}｜"
                           f"無條件頻率 {claim_template}｜取樣=每月首個交易日"
                           f"（n={base_rates.get('n_transition_sample')}）"),
            "p_table_built_at": base_rates.get("built_at"),
            "episode_id": episode_id,
            "block_key": block_key,
            "twin_of": None,
        }
        drafts.append(draft)

    return drafts


# ═══════════════════════════════════════════════════════════════════════════
# 查重 + 落帳
# ═══════════════════════════════════════════════════════════════════════════

def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def month_already_has_source(path, month_prefix, source=SOURCE):
    """同月同 source 已有落帳紀錄 → True（查重口徑：整批月頻拒絕重複，同
    scripts/generate_rv_forecasts.py 慣例）。"""
    for r in _existing_forecasts(path):
        if r.get("source") == source and (r.get("ts") or "").startswith(month_prefix):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="VRP 預測 producer — 月頻手動觸發")
    ap.add_argument("--write", action="store_true", help="append 進 knowledge/forecasts.jsonl（預設 dry-run）")
    args = ap.parse_args()

    today = date.today()
    ts_str = today.isoformat()
    month_prefix = today.strftime("%Y-%m")

    dup = month_already_has_source(FORECASTS, month_prefix)

    if not args.write:
        ids = _local_next_ids(ts_str, len(TEMPLATES), FORECASTS)
        drafts = build_drafts(ids, today=today)
        for d in drafts:
            print(json.dumps(d, ensure_ascii=False))
        if dup:
            warn(f"{month_prefix} 已有 source={SOURCE} 的落帳紀錄——本月重複落帳將被拒絕"
                 f"（查重口徑：同月同 source 整批拒絕）。")
        info(f"dry-run：共 {len(drafts)} 筆草案。--write 才會 append 進 {FORECASTS}"
             f"（若 {month_prefix} 已有紀錄則整批拒絕）。")
        return

    if dup:
        print(f"# --write 拒絕：{month_prefix} 已有 source={SOURCE} 落帳紀錄，本月不重複落帳。",
              file=sys.stderr)
        sys.exit(1)

    sys.path.insert(0, str(ROOT / "knowledge"))
    try:
        import forecast_lib as fl  # noqa: E402
    except ImportError as e:
        print(f"[vrp-forecasts][ERROR] 找不到 knowledge/forecast_lib.py（package A1 交付，"
              f"可能尚未完成）：{e}", file=sys.stderr)
        sys.exit(2)

    ids = fl.next_ids(ts_str, SOURCE, len(TEMPLATES), FORECASTS)
    drafts = build_drafts(ids, today=today)
    n_written, n_twins = fl.append(drafts, path=FORECASTS, write=True)
    print(f"# --write：寫入 {n_written} 筆本尊 + {n_twins} 筆哨兵 twin → {FORECASTS}", file=sys.stderr)


if __name__ == "__main__":
    main()
