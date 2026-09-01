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

SOURCE = "cot-model"
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
    """回傳 [{code, label, proxy, cot_date, net_pct_oi, pctile, direction}, ...]
    只含目前處於極端分位（≥95 或 ≤5）的市場；direction ∈ {"long","short"}。"""
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
    return out


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

def _next_ids(ts_str, n, used_so_far, path=FORECASTS):
    used = set(used_so_far)
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rid = json.loads(line).get("id", "")
            except json.JSONDecodeError:
                continue
            used.add(rid)
    prefix = f"fc_{ts_str.replace('-', '')}_cot_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{prefix}{seq:02d}"
        if cand not in used:
            out.append(cand)
    return out


def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def market_week_already_logged(path, code, cot_date, source=SOURCE):
    """同一市場（code）同一 COT 事件週（cot_date）已有落帳紀錄 → True（查重口徑：設計稿 §G5
    「同市場同事件週拒重複」）。"""
    needle = f"cot_code={code}|cot_week={cot_date}"
    for r in _existing_forecasts(path):
        if r.get("source") == source and needle in (r.get("source_ref") or ""):
            return True
    return False


def build_draft(today, extreme, pooled_p, base_rates):
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

    base_meta = (f"base_rate built_at={base_rates.get('built_at')}｜"
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
    }
    return draft


def write_drafts(drafts, path=FORECASTS):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for d in drafts:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description="cot-model 預測 producer — 事件觸發（權益三指數 COT 極端部位）")
    ap.add_argument("--write", action="store_true", help="偵測到極端事件且未查重命中時 append 進 knowledge/forecasts.jsonl（預設 dry-run）")
    args = ap.parse_args()

    today = date.today()
    extremes = current_extremes()

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
    drafts = []
    dup_codes = []
    used_ids = []
    for ex in extremes:
        dup = market_week_already_logged(FORECASTS, ex["code"], ex["cot_date"])
        if dup:
            dup_codes.append(ex["code"])
            warn(f"{ex['label']}（{ex['code']}）cot_week={ex['cot_date']} 已有 source={SOURCE} "
                 f"落帳紀錄——本次落帳將被拒絕（同市場同事件週不重複記）。")
            continue
        draft = build_draft(today, ex, pooled_p, base_rates)
        rid = _next_ids(ts_str, 1, used_ids)[0]
        used_ids.append(rid)
        draft["id"] = rid
        drafts.append(draft)

    for d in drafts:
        print(json.dumps(d, ensure_ascii=False))

    if not drafts:
        info(f"本次偵測到的 {len(extremes)} 個極端事件皆已查重命中（{dup_codes}），無新草案可產。")
        return

    if not args.write:
        info(f"dry-run：共 {len(drafts)} 筆草案（另有 {len(dup_codes)} 筆查重被拒）。"
             f"--write 才會 append 進 {FORECASTS}。")
        return

    write_drafts(drafts, FORECASTS)
    print(f"\n# --write：寫入 {len(drafts)} 筆 → {FORECASTS}（另有 {len(dup_codes)} 筆查重被拒）", file=sys.stderr)


if __name__ == "__main__":
    main()
