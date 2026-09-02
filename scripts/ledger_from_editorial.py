#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ledger_from_editorial.py — 把判讀層（monitor-read／detective-read／crowding-monitor／
market-read）editorial JSON 裡的 `forecasts[]` 命題擬成 knowledge/forecasts.jsonl 草案（市況
主控台設計稿 `notes/site-internal/root/_market_cockpit_design_20260902.md` §3；schema="fc-v2"；
market-read 分包規格見 `notes/site-internal/root/_market_read_design_20260903.md` §2.3）。

背景：§0 拍板 2「判讀必留命題」——monitor-read／detective-read／crowding-monitor／
macro-analyst／market-read 每次判讀至少 1 條、至多 8 條（market-read 5–8 條，見 §2.3）帶
resolver＋p 的命題進帳簿；不留命題＝沒說話。本檔是共用的機械落帳腳本：驗 resolver、查重、生
p_clim、append（含哨兵 twin）。判讀技能本身（monitor-read.md／detective-read.md／
crowding-monitor.md／market-read.md）產出 `forecasts[]` 這個欄位是 orchestrator 的職責
（改 skill 條文），本檔只消費既有 JSON 檔的這個欄位，不管它從哪個 skill 產生。

輸入 `--file` 指向的 JSON 須有：
  - 頂層 `as_of`（或 `date`）：判讀所屬日期，YYYY-MM-DD；缺欄退回今天並印警告。
  - 頂層 `forecasts[]`：`[{"claim":"…","p":0.3,"horizon_days":30,
    "resolver":{"series":"monitor:hy_oas","op":">","value":3.0,"window":"any_close"},
    "why":"一句白話理由"}]`（monitor-editorial-v1／detective-editorial-v1 additive 欄位；
    crowding-monitor 另存 `docs/crowding/data/forecasts_{YYYYMMDD}.json` 同 schema）。

每筆處理流程：
  1. 型別驗證（claim 非空字串／p∈[0,1]／horizon_days 正整數／resolver 四欄型別與合法值），
     不合格印原因、跳過（不 raise、不擋其餘筆）。
  2. resolver.series 驗證：`knowledge/settle_forecasts.check_resolver(series)`——這是廣義
     驗證（price/monitor/rv/pxd/ttp/relspy/vixts 皆可通過，不限本檔的 p_clim 白名單），驗證
     失敗即拒絕並印原因（見下方 p_clim 白名單與此處驗證範圍的差異：驗證廣、p_clim 窄）。
  3. 查重：同 `--source` 且同 claim 文字（去頭尾空白後比對），在 forecasts.jsonl 近 30 天
     （依 `ts` 欄）內已存在 → 拒絕。
  4. p_clim（p 本身由判讀者已給，本檔不重算 p，只補 p_clim 供事後對帳）：
       - `monitor:{dgs10,dgs30,hy_oas,tp10y,sofr_iorb}` → `build_macro_base_rates.climatology()`
         （delta＝resolver.value（顯示單位門檻）− monitor 現值，同 harvest_macro_falsifiers.py
         的單位口徑：dgs10/dgs30/hy_oas/tp10y 為 %、sofr_iorb 為 bp）。
       - **`pxd:SPY`（2026-09-03 起，market-read 專用覆寫，見設計稿 §2.3）** → 一律改用
         `data/calendar_base_rates_raw_cache.json`（25 年 SPY 日線，季度手動重建，非
         flowmap 的 ~2 年 rolling 快取）。H_td=round(horizon_days×252/365)：
         `window="at_expiry"` 算「t+H_td 收盤 op t 收盤」在全部起始日 t 上的無條件頻率
         （op ">"／">=" 算上漲、"<"／"<=" 算下跌，同 `_pxd_direction_p_clim` 的方向判定）；
         `window="any_close"` 先把 resolver.value 換算成相對比例 r＝value／快取最後收盤，
         再算全部起始日 t 上「close(t+1..t+H_td)／close(t) 的最大值（op 為 ">"／">="）或
         最小值（op 為 "<"／"<="）是否穿越 r」的無條件頻率（即「H_td 天內任一收盤達到該相對
         漲跌幅」的頻率，價格本身跨 25 年成長約 30 倍，故不能直接比較絕對價位，只能比例對齊）。
         `pxd:{QQQ,IWM}` 與其餘 source 不受影響，仍走下一條的 2 年規則。
       - `pxd:{SPY,QQQ,IWM}`（SPY 已被上一條攔截，此處實際只剩 QQQ／IWM）方向命題
         （value≈現價，語意上是 at_expiry 型的漲跌判斷）→ data/flowmap_prices.json 近 ~2 年
         （快取本身 rolling ~500 交易日）在同一 horizon（交易日=round(horizon_days×252/365)）
         下「t+H_td 收盤 op t 收盤」的無條件頻率。
       - `vixts:SLOPE` → data/vixts_base_rates_raw_cache.json 的 SLOPE（^VIX3M−^VIX 共同
         交易日）同一 horizon 下對 resolver.value／op／window 的無條件頻率。
       - 其餘 series（price:／rv:／ttp:／relspy:／pxd 非白名單 ticker 等）→ p_clim=None
         （仍是合法草案，只是沒有可比對的無條件參照頻率）。
  5. episode_id = `{source}:{as_of}:{n}`（n＝本次批次內第幾筆「通過驗證」的草案，1 起算）；
     resolve_by = as_of + horizon_days（曆日）；ts = 今天（落帳當下，非 as_of——與
     harvest_macro_falsifiers.py 對「報告日」vs「落帳日」的既有取捨一致）；source_ref =
     `--file` 路徑＋as_of；claim_template：resolver.series 屬價格方向類命名空間
     （pxd／ttp／price／relspy）→ `editorial_direction`，其餘（monitor／vixts／rv 等門檻類）
     → `editorial_threshold`；block_key 交給 `forecast_lib.finalize()` 用預設規則（ts 所在月）
     補齊，本檔不自訂；id prefix＝`ed`（`fc_{YYYYMMDD}_ed_{NN}`）。

CLI
---
  python scripts/ledger_from_editorial.py --source monitor-read --file docs/monitor/data/editorial.json
                                            # dry-run，草案印到 stdout（純 JSONL）
  python scripts/ledger_from_editorial.py --source monitor-read --file <path> --write
                                            # 落帳：append 進 knowledge/forecasts.jsonl（含哨兵 twin）
  python scripts/ledger_from_editorial.py --source crowding-monitor --file docs/crowding/data/forecasts_20260906.json --write
  python scripts/ledger_from_editorial.py --source market-read --file docs/market/data/read.json --write
                                            # 市況主控台判讀層（設計稿 §2.3）；--write 後把落帳
                                            # id 依序回填 docs/market/data/read.json 的
                                            # claim_ids[]（僅當落帳目標是預設真帳簿時才回填，
                                            # 見下方 --ledger 說明）

`--ledger PATH`：覆寫查重／落帳目標（預設 knowledge/forecasts.jsonl）。測試或離線核對用，
指向 scratch 檔即可，絕不可指向真帳簿之外的用途誤用來覆蓋真檔。**回填 claim_ids[] 只在落帳
目標是預設真帳簿（未給 `--ledger`）時才會寫回 `--file` 來源檔**；給了 `--ledger`（測試／離線）
時，落帳 id 仍會印出，但不會動來源檔一根汗毛（stderr 會明講原因）。

拒絕原因、每筆 p_clim 診斷與統計印到 stderr，不混進 stdout 的 JSONL。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
VIXTS_RAW_CACHE = ROOT / "data" / "vixts_base_rates_raw_cache.json"
CALENDAR_RAW_CACHE = ROOT / "data" / "calendar_base_rates_raw_cache.json"  # SPY 25 年日線，
# market-read 專用 p_clim 覆寫（設計稿 §2.3；build_calendar_base_rates.py 季度手動重建）

sys.path.insert(0, str(ROOT / "knowledge"))
import forecast_lib as fl  # noqa: E402 — id 產生／v2 欄位補齊（block_key）／落帳＋哨兵 twin
import settle_forecasts as sf  # noqa: E402 — check_resolver()（resolver 廣義驗證）

sys.path.insert(0, str(ROOT / "scripts"))
import build_macro_base_rates as bmr  # noqa: E402 — climatology()／raw cache（monitor 五個 FRED key）

SOURCES = ("monitor-read", "detective-read", "crowding-monitor", "market-read")
ID_PREFIX = "ed"

MONITOR_CLIMATOLOGY_KEYS = {"dgs10", "dgs30", "hy_oas", "tp10y", "sofr_iorb"}
PXD_TICKERS = {"SPY", "QQQ", "IWM"}
DIRECTION_NAMESPACES = {"pxd", "ttp", "price", "relspy"}  # → claim_template=editorial_direction
DEDUPE_WINDOW_DAYS = 30

_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def warn(msg: str) -> None:
    print(f"[ledger-from-editorial][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[ledger-from-editorial] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# p_clim（設計稿 §3；三條規則，其餘 None——與 harvest_intel_claims.py 邏輯刻意重複實作，
# 兩檔各自獨立可執行，不互相 import，同 codebase 既有「避免耦合並行檔案」慣例）
# ═══════════════════════════════════════════════════════════════════════════

def _parse_monitor_num(val):
    if val is None:
        return None
    m = _NUM_RE.search(str(val).replace(",", ""))
    return float(m.group(0)) if m else None


def _load_monitor_item(key, monitor_path=MONITOR_LATEST):
    try:
        data = json.loads(monitor_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    for cat in data.get("categories", []):
        for it in cat.get("items", []):
            if it.get("key") == key:
                return it
    return None


def _monitor_p_clim(key, op, value, horizon_days, monitor_path=MONITOR_LATEST):
    item = _load_monitor_item(key, monitor_path)
    if item is None:
        return None, f"monitor:{key} 在 {monitor_path} 找不到，無法算 p_clim"
    cur = _parse_monitor_num(item.get("val"))
    if cur is None:
        return None, f"monitor:{key} 現值缺失（val={item.get('val')!r}），無法算 p_clim"
    delta = round(value - cur, 6)
    clim = bmr.climatology(key, op, delta, horizon_days)
    p = clim.get("p")
    ref = (f"climatology(key={key!r}, op={op!r}, delta={delta}, horizon_days={horizon_days}) | "
           f"{clim.get('window')} | n={clim.get('n')}")
    return (round(p, 4) if isinstance(p, float) else p), ref


def _pxd_direction_p_clim(ticker, op, horizon_days, prices_path=FLOWMAP_PRICES):
    """pxd:{SPY,QQQ,IWM} 方向命題（value≈現價）：t+H_td 收盤 op t 收盤 的無條件頻率，取
    data/flowmap_prices.json 全部歷史（快取本身 rolling ~500 交易日 ≈ 2 年，設計稿「近 ~2 年」
    語意即此）。"""
    try:
        data = json.loads(prices_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, f"{prices_path} 無法讀取，無法算 p_clim"
    bars = (data.get("series") or {}).get(ticker)
    if not bars:
        return None, f"{prices_path} 找不到 {ticker}，無法算 p_clim"
    bars = sorted(bars, key=lambda x: x[0])
    vals = [c for _, c in bars]
    n_total = len(vals)
    H_td = max(1, round(horizon_days * 252 / 365))
    op_eff = ">" if op in (">", ">=") else "<"
    hits = count = 0
    for t in range(0, n_total - H_td):
        future, cur = vals[t + H_td], vals[t]
        hit = (future > cur) if op_eff == ">" else (future < cur)
        count += 1
        hits += hit
    if count == 0:
        return None, f"{prices_path} {ticker} 歷史不足 H_td={H_td} 交易日，無法算 p_clim"
    p = hits / count
    ref = (f"data/flowmap_prices.json {ticker} 近 {n_total} 個交易日（≈2 年）｜H_td={H_td}"
           f"（horizon_days={horizon_days}×252/365 四捨五入）｜op={op_eff} 無條件"
           f"{'上漲' if op_eff == '>' else '下跌'}頻率（t+H_td 收盤 vs t 收盤）｜n={count}")
    return round(p, 4), ref


def _spy_calendar_bars(cache_path=CALENDAR_RAW_CACHE):
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    bars = (data.get("series") or {}).get("SPY")
    if not bars:
        return None
    return sorted(bars, key=lambda x: x[0])


def _spy_calendar_p_clim(op, value, horizon_days, window, cache_path=CALENDAR_RAW_CACHE):
    """`pxd:SPY` 專用覆寫（2026-09-03 起，設計稿 §2.3）：一律改用
    `data/calendar_base_rates_raw_cache.json` 的 25 年 SPY 日線（非 flowmap 的 ~2 年 rolling
    快取），理由是市況判讀層的三框架機率與回撤命題需要橫跨多個景氣循環的無條件參照，而不是近
    兩年這種單一體制樣本。

    window="at_expiry"：與 `_pxd_direction_p_clim` 同一種「t+H_td 收盤 op t 收盤」方向頻率，
    只是換一個更長的價格序列。

    window="any_close"：resolver.value 是絕對價位（如「跌破 685.62」），但 25 年裡 SPY 從
    24 漲到 761，絕對價位無法跨期比較，所以先換算成相對今收的比例 r=value/最後收盤，再算
    「未來 H_td 個交易日內，close(t+1..t+H_td)/close(t) 的最大值（op 為漲）或最小值（op 為跌）
    是否穿越 r」在全部起始日 t 上的無條件頻率——即「H_td 天內任一收盤達到這個相對漲跌幅」的
    歷史頻率。"""
    vals_bars = _spy_calendar_bars(cache_path)
    if not vals_bars:
        return None, f"{cache_path} 無法讀取或找不到 SPY，無法算 p_clim"
    vals = [c for _, c in vals_bars]
    n_total = len(vals)
    H_td = max(1, round(horizon_days * 252 / 365))
    op_eff = ">" if op in (">", ">=") else "<"
    last_close = vals[-1]

    if window == "at_expiry":
        hits = count = 0
        for t in range(0, n_total - H_td):
            future, cur = vals[t + H_td], vals[t]
            hit = (future > cur) if op_eff == ">" else (future < cur)
            count += 1
            hits += hit
        if count == 0:
            return None, f"{cache_path} SPY 歷史不足 H_td={H_td} 交易日，無法算 p_clim"
        p = hits / count
        ref = (f"data/calendar_base_rates_raw_cache.json SPY 25 年（{vals_bars[0][0]}~"
               f"{vals_bars[-1][0]}，n={n_total} 交易日）｜H_td={H_td}"
               f"（horizon_days={horizon_days}×252/365 四捨五入）｜at_expiry｜op={op_eff} 無條件"
               f"{'上漲' if op_eff == '>' else '下跌'}頻率（t+H_td 收盤 vs t 收盤）｜n={count}")
        return round(p, 4), ref

    # window == "any_close"
    r = value / last_close
    hits = count = 0
    for t in range(0, n_total - H_td):
        cur = vals[t]
        window_vals = vals[t + 1:t + H_td + 1]
        if len(window_vals) != H_td:
            continue
        ratios = [w / cur for w in window_vals]
        extreme = max(ratios) if op_eff == ">" else min(ratios)
        hit = (extreme > r) if op_eff == ">" else (extreme < r)
        count += 1
        hits += hit
    if count == 0:
        return None, f"{cache_path} SPY 歷史不足 H_td={H_td} 交易日，無法算 p_clim"
    p = hits / count
    ref = (f"data/calendar_base_rates_raw_cache.json SPY 25 年（{vals_bars[0][0]}~"
           f"{vals_bars[-1][0]}，n={n_total} 交易日）｜H_td={H_td}"
           f"（horizon_days={horizon_days}×252/365 四捨五入）｜any_close｜r=value/最後收盤="
           f"{value}/{last_close}={r:.4f}｜op={op_eff} 任一收盤穿越比例 r 的無條件頻率"
           f"（close(t+1..t+H_td)/close(t) 的{'最大值' if op_eff == '>' else '最小值'}）｜n={count}")
    return round(p, 4), ref


def _vixts_slope_series(cache_path=VIXTS_RAW_CACHE):
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    series = data.get("series") or {}
    vix = dict(series.get("^VIX") or [])
    vix3m = dict(series.get("^VIX3M") or [])
    common = sorted(set(vix) & set(vix3m))
    if not common:
        return None
    return [(d, round(vix3m[d] - vix[d], 4)) for d in common]


def _vixts_p_clim(op, value, horizon_days, window, cache_path=VIXTS_RAW_CACHE):
    pts = _vixts_slope_series(cache_path)
    if not pts:
        return None, f"{cache_path} 無法讀取或 ^VIX／^VIX3M 無共同交易日，無法算 p_clim"
    vals = [v for _, v in pts]
    n_total = len(vals)
    H_td = max(1, round(horizon_days * 252 / 365))
    op_eff = ">" if op in (">", ">=") else "<"
    hits = count = 0
    for t in range(0, n_total - H_td):
        window_vals = vals[t + 1:t + H_td + 1]
        if len(window_vals) != H_td:
            continue
        if window == "at_expiry":
            hit = (window_vals[-1] > value) if op_eff == ">" else (window_vals[-1] < value)
        else:  # any_close
            hit = (max(window_vals) > value) if op_eff == ">" else (min(window_vals) < value)
        count += 1
        hits += hit
    if count == 0:
        return None, f"vixts raw cache 歷史不足 H_td={H_td} 交易日，無法算 p_clim"
    p = hits / count
    ref = (f"data/vixts_base_rates_raw_cache.json SLOPE（^VIX3M−^VIX 共同交易日，n={n_total}）｜"
           f"H_td={H_td}（horizon_days={horizon_days}×252/365 四捨五入）｜window={window}｜"
           f"op={op_eff} value={value} 無條件頻率｜n={count}")
    return round(p, 4), ref


def compute_p_clim(resolver: dict, horizon_days: int):
    series = resolver.get("series") or ""
    ns, _, key = series.partition(":")
    op, value, window = resolver.get("op"), resolver.get("value"), resolver.get("window")
    if ns == "monitor" and key in MONITOR_CLIMATOLOGY_KEYS:
        return _monitor_p_clim(key, op, value, horizon_days)
    if ns == "pxd" and key == "SPY":
        return _spy_calendar_p_clim(op, value, horizon_days, window)
    if ns == "pxd" and key in PXD_TICKERS:
        return _pxd_direction_p_clim(key, op, horizon_days)
    if ns == "vixts" and key == "SLOPE":
        return _vixts_p_clim(op, value, horizon_days, window)
    return None, None


# ═══════════════════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════════════════

def _existing_recent_claims(ledger_path, source, today):
    """回傳 {claim_text, ...}：同 source 且 ts 在近 DEDUPE_WINDOW_DAYS 天內（ts 缺失或無法解析
    的舊筆保守視為「在窗內」，寧可誤拒不要誤放重複）。"""
    cutoff = today - timedelta(days=DEDUPE_WINDOW_DAYS)
    out = set()
    for r in fl.existing(ledger_path):
        if r.get("source") != source:
            continue
        ts_raw = r.get("ts")
        try:
            r_date = date.fromisoformat(ts_raw) if ts_raw else None
        except ValueError:
            r_date = None
        if r_date is None or r_date >= cutoff:
            out.add((r.get("claim") or "").strip())
    return out


def _validate_item(item):
    """回傳 (ok, reason_if_not_ok, normalized_dict)。normalized_dict 只在 ok=True 時有效，
    含 claim/p/horizon_days/resolver（series/op/value/window 四鍵齊全）/why。"""
    if not isinstance(item, dict):
        return False, "item 非物件", None
    claim = item.get("claim")
    if not isinstance(claim, str) or not claim.strip():
        return False, "claim 非字串或為空", None
    p = item.get("p")
    if not isinstance(p, (int, float)) or isinstance(p, bool) or not (0.0 <= float(p) <= 1.0):
        return False, f"p={p!r} 不是 [0,1] 內的數字", None
    horizon_days = item.get("horizon_days")
    if not isinstance(horizon_days, int) or isinstance(horizon_days, bool) or horizon_days <= 0:
        return False, f"horizon_days={horizon_days!r} 不是正整數", None
    resolver = item.get("resolver")
    if not isinstance(resolver, dict):
        return False, "resolver 非物件", None
    series = resolver.get("series")
    if not isinstance(series, str) or ":" not in series:
        return False, f"resolver.series={series!r} 格式不合法", None
    op = resolver.get("op")
    if op not in (">", "<", ">=", "<="):
        return False, f"resolver.op={op!r} 不合法", None
    value = resolver.get("value")
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False, f"resolver.value={value!r} 不是數字", None
    window = resolver.get("window")
    if window not in ("any_close", "at_expiry"):
        return False, f"resolver.window={window!r} 不合法", None

    ok, msg = sf.check_resolver(series)
    if not ok:
        return False, f"resolver 驗證失敗：{msg}", None

    return True, None, {
        "claim": claim.strip(), "p": round(float(p), 4), "horizon_days": int(horizon_days),
        "resolver": {"series": series, "op": op, "value": value, "window": window},
        "why": item.get("why") if isinstance(item.get("why"), str) else None,
    }


def build_drafts(source, file_path, items, as_of, ledger_path, today=None):
    """回傳 (drafts_without_id, rejected, orig_indices)。rejected：[(index, reason), ...]。
    orig_indices[i] = drafts[i] 對應在原始 `items`（即來源檔 forecasts[]）的索引，供呼叫端
    落帳後把 id 依序回填回來源檔 claim_ids[]（與 forecasts[] 同序，未通過驗證／查重的位置留
    None）。drafts 尚未經 fl.next_ids／fl.finalize（呼叫端負責，與 generate_cot_forecasts.py
    既有慣例一致）。"""
    today = today or date.today()
    ts_str = today.isoformat()
    recent_claims = _existing_recent_claims(ledger_path, source, today)

    drafts, rejected, orig_indices = [], [], []
    n = 0
    for idx, item in enumerate(items):
        ok, reason, norm = _validate_item(item)
        if not ok:
            rejected.append((idx, reason))
            continue
        if norm["claim"] in recent_claims:
            rejected.append((idx, "查重命中：同 source 30 天內已有相同 claim 文字"))
            continue

        n += 1
        orig_indices.append(idx)
        resolver = norm["resolver"]
        series = resolver["series"]
        ns = series.split(":", 1)[0]
        claim_template = "editorial_direction" if ns in DIRECTION_NAMESPACES else "editorial_threshold"
        resolve_by = (date.fromisoformat(as_of) + timedelta(days=norm["horizon_days"])).isoformat()
        p_clim, p_clim_ref = compute_p_clim(resolver, norm["horizon_days"])
        episode_id = f"{source}:{as_of}:{n}"
        source_ref = f"{file_path}｜as_of={as_of}"

        note_parts = [f"editorial 判讀命題（source={source}）"]
        if norm["why"]:
            note_parts.append(f"理由：{norm['why']}")
        note_parts.append(f"來源檔：{file_path}（as_of={as_of}）")
        note_parts.append("p 由判讀者（skill／LLM）自行給定，本檔不重算、只補 p_clim 供事後對帳")

        drafts.append({
            "id": None, "ts": ts_str, "source": source, "source_ref": source_ref,
            "claim": norm["claim"], "p": norm["p"], "horizon_days": norm["horizon_days"],
            "resolve_by": resolve_by, "resolver": resolver,
            "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
            "note": "｜".join(note_parts),
            "claim_template": claim_template,
            "p_clim": p_clim, "p_clim_ref": p_clim_ref, "p_table_built_at": None,
            "episode_id": episode_id,
            # block_key 刻意不設——交給 fl.finalize() 用預設規則（ts 所在月）補齊
        })
    return drafts, rejected, orig_indices


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, choices=SOURCES)
    ap.add_argument("--file", required=True, help="editorial JSON 路徑（含頂層 forecasts[] 與 as_of）")
    ap.add_argument("--write", action="store_true", help="落帳：append 進帳簿（含哨兵 twin）")
    ap.add_argument("--ledger", default=None, help="覆寫查重／落帳目標路徑（預設 knowledge/forecasts.jsonl）")
    args = ap.parse_args()

    ledger_path = Path(args.ledger) if args.ledger else FORECASTS
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[ledger-from-editorial][ERROR] 找不到 {file_path}", file=sys.stderr)
        sys.exit(2)
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"[ledger-from-editorial][ERROR] 無法讀取/解析 {file_path}：{e}", file=sys.stderr)
        sys.exit(2)

    as_of = data.get("as_of") or data.get("date")
    if not as_of:
        as_of = date.today().isoformat()
        warn(f"{file_path} 缺 as_of／date 欄位，退回今天 {as_of}")

    items = data.get("forecasts")
    if not isinstance(items, list):
        if items is not None:
            warn(f"{file_path} 的 forecasts 不是陣列（type={type(items).__name__}），視為空清單")
        items = []

    today = date.today()
    drafts, rejected, orig_indices = build_drafts(args.source, str(args.file), items, as_of,
                                                   ledger_path, today=today)

    if drafts:
        ids = fl.next_ids(today.isoformat(), ID_PREFIX, len(drafts), ledger_path)
        for d, rid in zip(drafts, ids):
            d["id"] = rid
        drafts = fl.finalize(drafts)

    n_written, n_twins = fl.append(drafts, path=ledger_path, write=args.write)

    for idx, reason in rejected:
        warn(f"forecasts[{idx}] 拒絕：{reason}")

    for d in drafts:
        info(f"{d['id']}: p={d['p']} p_clim={d['p_clim']} resolver={d['resolver']['series']} "
             f"{d['resolver']['op']} {d['resolver']['value']}｜claim_template={d['claim_template']}")

    if not args.write:
        info(f"dry-run：{len(items)} 條輸入，{len(drafts)} 筆通過驗證與查重（{len(rejected)} 筆拒絕）。"
             f"--write 才會 append 進 {ledger_path}（含哨兵 twin）。")
    else:
        info(f"--write：寫入 {n_written} 本尊 + {n_twins} 哨兵 → {ledger_path}"
             f"（{len(rejected)} 筆拒絕，{len(items) - len(drafts) - len(rejected)} 筆其他原因跳過）。")

        # 回填 claim_ids[]（與 forecasts[] 同序；未通過驗證／查重的位置留 None）——只有落帳
        # 目標是預設真帳簿（未給 --ledger）時才動來源檔，測試／離線核對絕不可誤寫回真判讀檔。
        ordered_ids = [None] * len(items)
        for d, oidx in zip(drafts, orig_indices):
            ordered_ids[oidx] = d["id"]
        info(f"落帳 id（依 forecasts[] 原序，未落帳位置為 null）：{ordered_ids}")
        if args.ledger is None:
            data["claim_ids"] = ordered_ids
            file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            info(f"已回填 claim_ids[] → {file_path}")
        else:
            warn(f"--ledger 指向非預設路徑（{ledger_path}），僅印出落帳 id，"
                 f"不回填來源檔 {file_path} 的 claim_ids[]")

    if not items:
        warn(f"{file_path}（as_of={as_of}）forecasts[] 為空——本次判讀未留下任何命題"
             f"（§0 拍板 2：判讀無命題視為未完成，這是紀律訊號非本腳本的錯，僅如實回報）。")


if __name__ == "__main__":
    main()
