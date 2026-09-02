#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_cot_forecasts.py — cot-model 預測 producer（forecast ledger G5，事件觸發）。

每次執行（週更 cron，`--write`）判定「權益三指數（S&P/NDX/RTY e-mini）目前是否有任一檔的
COT net_pct_oi 處於 3 年滾動極端分位」（PREREG 凍結定義，設計稿 §G4／§G5：分位 ≥95 或
≤5）——只在真的偵測到極端事件當週才產草案，其餘時候印「無事件」exit 0，不寫入
knowledge/forecasts.jsonl。

分位計算口徑與 scripts/build_cot_base_rates.py 逐字一致（156 週滾動視窗、inclusive
percentile），但這裡是「即時現況檢查」而非該檔的「歷史事件挖掘」——沿用
scripts/build_crowding.py cot_compute() 的既有慣例：用「目前可得的最後 min(156, 週數) 週」
視窗（不強制滿 156 週才判定，樣本不足時印警告，但仍照現有資料判斷「現在是不是極端」，因為
這是即時現況、不是可證偽的歷史 base rate 統計）。

極端觸發時（可能同時 0～3 個市場觸發，各自獨立判定），對每個觸發的市場各產一筆「4 週後價格
反向」草案：極端偏多（long，percentile≥95）→ claim 為 20 交易日後該市場代理 ETF 價格低於今
收（resolver pxd:<proxy> < 今收，at_expiry）；極端偏空（short，percentile≤5）→ 反向（>今收）。
resolve_by = ts+30 曆日（同 generate_rv_forecasts.py／generate_vix_forecasts.py 的既有取捨：
20 個交易日 ≈ 30 個曆日，非精確對齊）。p 值機械取自 data/cot_base_rates.json 的
`pooled.reversal_hit_rate`（三市場合併 base rate，不分市場各自的 hit rate——設計稿 §G5「p
取 pooled base rate」）——不接受人工覆寫。

v2（forecast v2 設計稿 §5.1）：改用 knowledge/forecast_lib.py（next_ids／finalize／append，
含哨兵 twin 產生）；每筆額外填 claim_template（單一樣板 `cot_reversal_20d`，不分方向）、
p_clim（依方向取 data/cot_base_rates.json 頂層 unconditional 頻率——極端偏多對應
px_down_20d、極端偏空對應 px_up_20d，方向判斷與 claim 本身的漲跌方向一致）、p_clim_ref、
p_table_built_at、episode_id（`cot:{code}:{run_start_week}`，run_start_week 為回看
cot_history 找到的「本次連續極端週」起點，見 _run_start_week()）。查重規則、dry-run/--write
行為、stdout=JSONL only 慣例不變。

CLI
---
  python scripts/generate_cot_forecasts.py            dry-run，草案（若有）印到 stdout（純 JSONL）
  python scripts/generate_cot_forecasts.py --write     append 進 knowledge/forecasts.jsonl
                                                        （查重：同市場同事件週已落過即拒）
無事件或跳過/拒絕原因印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COT_HISTORY = ROOT / "data" / "cot_history.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
BASE_RATES = ROOT / "data" / "cot_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

sys.path.insert(0, str(ROOT / "knowledge"))
import forecast_lib as fl  # noqa: E402 — id 產生／v2 欄位補齊／落帳＋哨兵 twin，見 forecast_lib.py

SOURCE = "cot-model"
CLAIM_TEMPLATE = "cot_reversal_20d"  # forecast v2 設計稿 §5.1（單一樣板，不分方向）
PCTILE_WINDOW_WEEKS = 156   # 須與 build_cot_base_rates.py 一致（PREREG 凍結）
EXTREME_HI = 95
EXTREME_LO = 5
HORIZON_CALENDAR_DAYS = 30  # ≈20 個交易日（PREREG 近似，見檔頭 docstring）

EQUITY_MARKETS = {
    "13874A": {"label": "S&P 500 E-mini", "proxy": "SPY"},
    "209742": {"label": "Nasdaq-100 E-mini", "proxy": "QQQ"},
    "239742": {"label": "Russell 2000 E-mini", "proxy": "IWM"},
}


def warn(msg: str) -> None:
    print(f"[cot-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[cot-forecasts] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# percentile（照抄 scripts/build_crowding.py pctile_incl／build_cot_base_rates.py 定義）
# ═══════════════════════════════════════════════════════════════════════════

def pctile_incl(values, x):
    v = [z for z in values if z is not None]
    n = len(v)
    if n == 0 or x is None:
        return None
    return round(100.0 * sum(1 for z in v if z <= x) / n, 1)


def current_extremes():
    """回傳 ([{code, label, proxy, cot_date, net_pct_oi, pctile, direction}, ...], cot_history)。
    第一項只含目前處於極端分位（≥95 或 ≤5）的市場；direction ∈ {"long","short"}。第二項
    （cot_history 原始 dict）回傳給呼叫端供 _run_start_week() 回看連續極端週的 run 起點
    （episode_id 用，見 §5.1），避免重複讀檔。"""
    if not COT_HISTORY.exists():
        raise SystemExit(f"找不到 {COT_HISTORY}")
    cot_history = json.loads(COT_HISTORY.read_text(encoding="utf-8"))
    markets_map = cot_history.get("markets") or {}

    out = []
    for code, meta in EQUITY_MARKETS.items():
        label, proxy = meta["label"], meta["proxy"]
        m = markets_map.get(code)
        if not m or not m.get("series"):
            warn(f"{COT_HISTORY} 找不到市場 {code}（{label}），略過")
            continue
        s = sorted(tuple(pt) for pt in m["series"])
        dates = [d for d, _ in s]
        vals = [v for _, v in s]
        cur_date, cur_val = dates[-1], vals[-1]
        win = vals[-PCTILE_WINDOW_WEEKS:]
        if len(win) < PCTILE_WINDOW_WEEKS:
            warn(f"{label}：3 年分位樣本僅 {len(win)} 週（<{PCTILE_WINDOW_WEEKS}），"
                 f"分位可信度打折，仍照現有資料判定現況")
        p = pctile_incl(win, cur_val)
        if p is None:
            continue
        direction = None
        if p >= EXTREME_HI:
            direction = "long"
        elif p <= EXTREME_LO:
            direction = "short"
        if direction:
            out.append({"code": code, "label": label, "proxy": proxy, "cot_date": cur_date,
                        "net_pct_oi": cur_val, "pctile": p, "direction": direction})
    return out, cot_history


def _run_start_week(code, cot_history, direction, cur_date):
    """episode_id（§5.1：`cot:{code}:{run_start_week}`）用——從 cur_date 往回走，只要前一週
    在「該週自己的 156 週滾動視窗」下仍是同方向極端，就把 run_start 往前推；遇到非極端、
    方向反轉、或視窗不足 156 週（無法判定）即停。回傳 run 起點的週日期字串；查無市場資料或
    cur_date 不在序列內則保守回傳 cur_date 本身（run 視為只有一週）。"""
    m = (cot_history.get("markets") or {}).get(code)
    if not m or not m.get("series"):
        return cur_date
    s = sorted(tuple(pt) for pt in m["series"])
    dates = [d for d, _ in s]
    vals = [v for _, v in s]
    try:
        i = dates.index(cur_date)
    except ValueError:
        return cur_date
    run_start_idx = i
    j = i
    while j - 1 >= PCTILE_WINDOW_WEEKS - 1:
        jj = j - 1
        w = vals[jj - PCTILE_WINDOW_WEEKS + 1:jj + 1]
        p = pctile_incl(w, vals[jj])
        if p is None:
            break
        d = "long" if p >= EXTREME_HI else ("short" if p <= EXTREME_LO else None)
        if d != direction:
            break
        run_start_idx = jj
        j = jj
    return dates[run_start_idx]


# ═══════════════════════════════════════════════════════════════════════════
# pxd:<TICKER> 讀法（data/flowmap_prices.json，取最新收盤）
# ═══════════════════════════════════════════════════════════════════════════

def latest_close(ticker):
    if not FLOWMAP_PRICES.exists():
        return None, None
    try:
        data = json.loads(FLOWMAP_PRICES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, None
    bars = sorted((data.get("series") or {}).get(ticker) or [])
    if not bars:
        return None, None
    return bars[-1]


# ═══════════════════════════════════════════════════════════════════════════
# base rate 查表
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates():
    if not BASE_RATES.exists():
        raise SystemExit(f"找不到 {BASE_RATES} —— 先跑 python scripts/build_cot_base_rates.py")
    try:
        return json.loads(BASE_RATES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {BASE_RATES}: {e}")


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生 + 查重 + 落帳
# ═══════════════════════════════════════════════════════════════════════════

def market_week_already_logged(path, code, cot_date, source=SOURCE):
    """同一市場（code）同一 COT 事件週（cot_date）已有落帳紀錄 → True（查重口徑：設計稿 §G5
    「同市場同事件週拒重複」）。"""
    needle = f"cot_code={code}|cot_week={cot_date}"
    for r in fl.existing(path):
        if r.get("source") == source and needle in (r.get("source_ref") or ""):
            return True
    return False


def build_draft(today, extreme, pooled_p, base_rates, cot_history):
    code, label, proxy = extreme["code"], extreme["label"], extreme["proxy"]
    cot_date, pctile, direction = extreme["cot_date"], extreme["pctile"], extreme["direction"]

    px_date, px_close = latest_close(proxy)
    if px_close is None:
        raise SystemExit(f"無法從 {FLOWMAP_PRICES} 找到 {proxy} 最新收盤，中止")

    ts_str = today.isoformat()
    resolve_by = (today + timedelta(days=HORIZON_CALENDAR_DAYS)).isoformat()
    op = "<" if direction == "long" else ">"
    direction_zh = "偏多（long，可能過度樂觀）" if direction == "long" else "偏空（short，可能過度悲觀）"
    move_zh = "下跌、低於" if direction == "long" else "上漲、高於"

    # v2（forecast v2 設計稿 §5.1）：p_clim 依方向取「同一份表」的頂層 unconditional 頻率——
    # 極端偏多（long）事件的命題方向是「跌」，對應 px_down_20d；極端偏空（short）事件的命題
    # 方向是「漲」，對應 px_up_20d（與上面 op/move_zh 的方向判斷邏輯一致）。
    p_clim_map = base_rates.get("p_clim") or {}
    clim_key = "px_down_20d" if direction == "long" else "px_up_20d"
    p_clim = (p_clim_map.get(clim_key) or {}).get(proxy)
    built_at = base_rates.get("built_at")
    p_clim_ref = (f"data/cot_base_rates.json p_clim.{clim_key}.{proxy}"
                  f"（unconditional，全樣本交易日取樣）built_at={built_at}")
    run_start_week = _run_start_week(code, cot_history, direction, cot_date)
    episode_id = f"cot:{code}:{run_start_week}"

    base_meta = (f"base_rate built_at={built_at}｜"
                 f"pooled.n_valid={base_rates.get('pooled', {}).get('n_valid')}｜"
                 f"pooled.reversal_hit_rate={pooled_p}｜confidence={base_rates.get('confidence')}")
    source_ref = (f"cot_code={code}|cot_week={cot_date}｜market={label}｜net_pct_oi={extreme['net_pct_oi']}｜"
                  f"pctile_3y={pctile}｜direction={direction}｜proxy_close={px_close}（{px_date}）｜"
                  f"data/cot_base_rates.json {base_meta}")
    claim = (f"{resolve_by} 前（30 曆日內，約 20 個交易日）：{label} 部位極端{direction_zh}"
             f"（COT 3 年滾動分位 {pctile}，{cot_date} 當週）後，{proxy} 收盤{move_zh}今收 {px_close}")

    draft = {
        "id": None, "ts": ts_str, "source": SOURCE, "source_ref": source_ref,
        "claim": claim,
        "p": pooled_p, "horizon_days": HORIZON_CALENDAR_DAYS, "resolve_by": resolve_by,
        "resolver": {"series": f"pxd:{proxy}", "op": op, "value": px_close, "window": "at_expiry"},
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "note": (f"cot-model 機械賦值（無需人工判斷）｜{label} pctile_3y={pctile}（{cot_date} 當週，"
                 f"net_pct_oi={extreme['net_pct_oi']}）｜p 取自 cot_base_rates.json "
                 f"pooled.reversal_hit_rate（三市場合併，非該市場單獨 hit rate）｜{base_meta}"),
        "claim_template": CLAIM_TEMPLATE, "p_clim": p_clim,
        "p_clim_ref": p_clim_ref, "p_table_built_at": built_at, "episode_id": episode_id,
    }
    return draft


def main():
    ap = argparse.ArgumentParser(description="cot-model 預測 producer — 事件觸發（權益三指數 COT 極端部位）")
    ap.add_argument("--write", action="store_true", help="偵測到極端事件且未查重命中時 append 進 knowledge/forecasts.jsonl（預設 dry-run）")
    args = ap.parse_args()

    today = date.today()
    extremes, cot_history = current_extremes()

    if not extremes:
        info("無事件：權益三指數目前皆未處於 3 年滾動極端分位（≥95 或 ≤5）。exit 0，不落帳。")
        return

    base_rates = load_base_rates()
    pooled_p = (base_rates.get("pooled") or {}).get("reversal_hit_rate")
    if pooled_p is None:
        raise SystemExit(f"{BASE_RATES} 缺 pooled.reversal_hit_rate，中止（不可硬猜 p）")

    for ex in extremes:
        info(f"偵測到極端：{ex['label']}（{ex['code']}）pctile_3y={ex['pctile']}｜"
             f"direction={ex['direction']}｜cot_week={ex['cot_date']}")

    ts_str = today.isoformat()
    dup_codes = []
    non_dup_extremes = []
    for ex in extremes:
        if market_week_already_logged(FORECASTS, ex["code"], ex["cot_date"]):
            dup_codes.append(ex["code"])
            warn(f"{ex['label']}（{ex['code']}）cot_week={ex['cot_date']} 已有 source={SOURCE} "
                 f"落帳紀錄——本次落帳將被拒絕（同市場同事件週不重複記）。")
            continue
        non_dup_extremes.append(ex)

    drafts = []
    if non_dup_extremes:
        ids = fl.next_ids(ts_str, "cot", len(non_dup_extremes), FORECASTS)
        for ex, rid in zip(non_dup_extremes, ids):
            draft = build_draft(today, ex, pooled_p, base_rates, cot_history)
            draft["id"] = rid
            drafts.append(draft)
        drafts = fl.finalize(drafts)

    if not drafts:
        info(f"本次偵測到的 {len(extremes)} 個極端事件皆已查重命中（{dup_codes}），無新草案可產。")
        return

    n_written, n_twins = fl.append(drafts, path=FORECASTS, write=args.write)

    if not args.write:
        info(f"dry-run：共 {len(drafts)} 筆草案（另有 {len(dup_codes)} 筆查重被拒）。"
             f"--write 才會 append 進 {FORECASTS}。")
        return

    print(f"\n# --write：寫入 {n_written} 筆＋{n_twins} 筆哨兵 twin → {FORECASTS}"
          f"（另有 {len(dup_codes)} 筆查重被拒）", file=sys.stderr)


if __name__ == "__main__":
    main()
