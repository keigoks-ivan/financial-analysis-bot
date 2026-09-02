#!/usr/bin/env python3
"""
settle_forecasts.py — 機率化判讀對帳簿的機械結算（forecasts.jsonl → forecast_settlement.json）。

鏡像 settle_outcomes.py 的模式：讀 knowledge/forecasts.jsonl 的 open 筆，依各筆 resolver 判
resolved_yes／resolved_no／void，算 Brier，把 status/resolved_ts/outcome/brier 四欄就地回寫
forecasts.jsonl（整檔重寫、保序，其他欄位原樣）；彙總統計另存 knowledge/forecast_settlement.json
（衍生物，gitignore，本地重算）。q.py --forecasts 消費本檔：無檔或比 forecasts.jsonl／
monitor latest.json／週線 cache 舊會自動重跑。

resolver 八個 series 命名空間：
  - price:<TICKER>  → data/weekly_cache/<TICKER>.json 週線收盤（完整歷史；ALIAS／
                      _close_at_or_before 讀法照抄 settle_outcomes.py）。
  - monitor:<key>   → docs/monitor/data/latest.json 的 categories[].items[]（key 比對）。
                      歷史覆蓋只有 spark 陣列（近 ~30 個交易日、只排除週末不排除假日的近似
                      交易日反推，非精確交易日曆），故 any_close 窗口的完整性依賴本腳本的
                      執行頻率 —— **本腳本須至少每 30 天跑一次**，否則兩次執行之間若有瞬間
                      觸及可能被錯過（spark 只留最近窗，不保證看到全歷史）。每次執行都會在
                      輸出 JSON 記錄 last_run／prev_run，間隔過久或個別 forecast 的 ts 早於
                      本次可觀察範圍時一併印 coverage_warning，不靜默硬判。
                      **v2 單位正規化（forecast v2 設計稿 §4.1，根治 sofr_iorb bug）**：
                      scale = item.val 解析值 / spark 最後一點解析值（兩者皆非 0 時），若落在
                      {0.01, 0.1, 1, 10, 100, 1000} 任一值的 ±5% 內則取該值；否則 void，
                      reason=`unit_ambiguous:{key}`。比較時把 resolver.value（維持人讀得懂的
                      「顯示單位」，如 5 = 5bp）除以 scale 換算成 spark 的尺度再比對。兩者皆為
                      0 或 spark 空 → 沿用 v1 舊行為（不換算），並印警告（不寫入 forecast 列
                      本身的 note，只在本次結算的 stdout 提醒）。
  - rv:<TICKER>     → data/flowmap_prices.json 該 ticker 日線，逐日算 RV21（年化 21 交易日
                      日對數報酬 sample std×√252×100，口徑與 scripts/build_rv_base_rates.py／
                      scripts/generate_rv_forecasts.py 逐字一致），支援 at_expiry／any_close。
                      該快取為 rolling ~500 交易日（非完整歷史，會隨時間往前捲動裁切），故
                      forecast 的 ts 若早於目前快取可回看的最早 RV21 可算日期，代表視窗前段
                      已不可考——沿用既有 coverage_warning 機制浮出（coverage_gap 旗標），
                      不硬判 void 也不假裝完整。ticker 不在該快取（series 找不到 key）→ void。
  - pxd:<TICKER>    → data/flowmap_prices.json 該 ticker 日線收盤（直接讀收盤價，非 rv:
                      域的 RV21 轉換），支援 at_expiry／any_close，coverage_gap 判法與
                      rv: 域相同（rolling ~500 交易日快取）。ticker 不在該快取→void。設計稿
                      §G5：cot-model／vix-model 的「63 交易日後 SPY 高於 X」「4 週後價格反
                      向」等直接方向命題走本域。
  - vixts:SLOPE     → data/statlab_prices.json 的 ^VIX3M − ^VIX 收盤差（只支援 key=SLOPE，
                      唯一序列），與 scripts/build_vixts_base_rates.py／generate_vix_forecasts.py
                      口徑一致。statlab_prices.json 缺檔或 ^VIX／^VIX3M 無重疊交易日 →
                      **該筆保持 open＋印警告，不 void**（資料層暫缺是暫時狀態，非永久不可
                      判——與其他域「查無 ticker 即 void」不同，因為 statlab_prices.json 由
                      另一條 pipeline 維護，本腳本執行當下可能尚未產出或尚未追上）。
  - ttp:<TICKER>    → data/trend_track_prices.json 該 ticker 日線收盤（與 flowmap_prices
                      同構：{"meta":..., "series": {TICKER: [[date, close], ...]}}），語義與
                      pxd: 完全相同（at_expiry／any_close），由 B 包（tsmom producer）餵料
                      （forecast v2 設計稿 §4.2）。ticker 不在該快取→void。
  - relspy:<TICKER> → 相對 SPY 超額報酬命題（forecast v2 設計稿 §4.3；由 D 包 dd-verdict
                      producer 餵料）。resolver 額外攜帶 base_date／base_px／base_spy：
                      {"series":"relspy:NVDA","op":">","value":0,"window":"at_expiry",
                       "base_date":"YYYY-MM-DD","base_px":123.4,"base_spy":567.8}。
                      px_T＝data/weekly_cache/<ALIAS(TICKER)>.json resolve_by 當日或之前最近
                      收盤（_close_at_or_before，同 price: 域）；spy_T＝data/flowmap_prices.json
                      SPY 同規則；outcome = 1 若 (px_T/base_px − spy_T/base_spy) > value。**只
                      支援 at_expiry**（其他 window 值 → void，reason=`relspy_unsupported_
                      window:{window}`）。缺 base_px／base_spy 或缺任一價 → void，
                      reason=`relspy_missing_base:{TICKER}` 或 `relspy_missing_price:{TICKER}`。
  - detective:*     → 本期不實作。遇到即印警告、該筆保持 open，不硬判。

op 支援 >／<>=／<=；window 支援 any_close（區間內任一收盤觸及即 yes）與 at_expiry（只看到期
時的值）。

單位注意（monitor 域，v2 改版）：latest.json 的 val／spark 是各 series 自訂格式（如 dgs10
"4.73%"、sofr_iorb "3bps"），本腳本一律先取其去除逗號後第一個數字 token 的原始數值。**v1
舊行為**（resolver.value 須採與 spark 原始數值相同的尺度落帳）已於 v2 廢除——sofr_iorb 的
val 顯示「3bps」但 spark 陣列卻是以「百分點」記錄（如 0.03），v1 舊行為下 resolver.value 若
寫「顯示值」5（=5bp）永遠不會等於 spark 尺度的 0.05，門檻形同虛設（實測 bug，見設計稿
§0）。**v2 起 resolver.value 一律採「顯示單位」落帳**（人讀得懂：5 = 5bp），本腳本在結算前
會先算出 scale = val 解析值 / spark 最後一點解析值，換算成 spark 尺度後再比對（見上方
resolver 命名空間段落）；q.py --forecast-add／本檔 --check-resolver 都會印出顯示值、spark
尺度、scale 供對齊。

單位注意（rv 域）：RV21 一律以「百分比 vol 點」為尺度（例：10.26 代表年化已實現波動 10.26%，
非 0.1026）——與 scripts/build_rv_base_rates.py／scripts/generate_rv_forecasts.py 產出的
resolver.value 尺度一致，直接比對即可，不需換算。

單位注意（pxd／ttp 域）：與 price 域一致，直接是該 ticker 的日線收盤價原始尺度（美元／點數），
resolver.value 用同尺度落帳。

單位注意（vixts 域）：slope 一律以「vol 點」為尺度（^VIX3M − ^VIX 的收盤差，可正可負；
正＝contango，負＝inverted），與 scripts/build_vixts_base_rates.py／generate_vix_forecasts.py
產出的 resolver.value 尺度一致。

單位注意（relspy 域）：value 為「相對報酬差」的小數（如 0 = 兩者報酬率相等），base_px／
base_spy 為落帳當時記錄的基準收盤價，皆與 resolver 內攜帶的原始尺度一致，不需額外換算。

CLI：
  python knowledge/settle_forecasts.py                       # 正常結算，重寫 forecasts.jsonl + 輸出 settlement
  python knowledge/settle_forecasts.py --check-resolver price:NVDA     # 驗證 resolver 可解析（給 q.py 用）
  python knowledge/settle_forecasts.py --check-resolver monitor:hy_oas
  python knowledge/settle_forecasts.py --check-resolver rv:SPY
  python knowledge/settle_forecasts.py --check-resolver pxd:SPY
  python knowledge/settle_forecasts.py --check-resolver vixts:SLOPE
  python knowledge/settle_forecasts.py --check-resolver ttp:SPY
  python knowledge/settle_forecasts.py --check-resolver relspy:NVDA
"""
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

KDIR = Path(__file__).resolve().parent
ROOT = KDIR.parent
FORECASTS = KDIR / "forecasts.jsonl"
OUT = KDIR / "forecast_settlement.json"
CACHE_DIR = ROOT / "data" / "weekly_cache"
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"  # rv:／pxd:／relspy: 域讀法（見 build_rv_base_rates.py）
STATLAB_PRICES = ROOT / "data" / "statlab_prices.json"  # vixts: 域讀法（見 build_vixts_base_rates.py）
TREND_TRACK_PRICES = ROOT / "data" / "trend_track_prices.json"  # ttp: 域讀法（見 build_tsmom_base_rates.py，B 包）

RV_WINDOW_TRADING_DAYS = 21  # 須與 scripts/build_rv_base_rates.py／generate_rv_forecasts.py 一致（PREREG 凍結）

# ─────────────────────────── SPRT 常數（forecast v2 設計稿 §3.3，PREREG 凍結） ───────────────────────────
SPRT_P0 = 0.5
SPRT_P1 = 0.65
SPRT_ALPHA = 0.05
SPRT_BETA = 0.10
SPRT_A = 2.8904       # ln((1-beta)/alpha) = ln(18)
SPRT_B = -2.2513      # ln(beta/(1-alpha)) = ln(0.1/0.95)
SPRT_LLR_HIT = 0.26236    # ln(0.65/0.50)
SPRT_LLR_MISS = -0.35667  # ln(0.35/0.50)
SPRT_MIN_N_EFF = 20

# ─────────────────────────── block-bootstrap（§3.5，PREREG 凍結） ───────────────────────────
BOOTSTRAP_N = 2000
BOOTSTRAP_SEED = 20260902

# price:<TICKER> → weekly_cache 檔名（dd-meta ticker 慣例與 cache 命名不一致者）。
# 照抄 settle_outcomes.py 的 ALIAS —— 同一份 weekly_cache，同一批例外。
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

OPS = {
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
}

COVERAGE_WARN_DAYS = 30  # 上次執行距今超過此天數 → monitor any_close 覆蓋率警告


# ─────────────────────────── I/O ───────────────────────────

def _load_forecasts():
    if not FORECASTS.exists():
        return []
    return [json.loads(l) for l in FORECASTS.read_text(encoding="utf-8").splitlines() if l.strip()]


def _write_forecasts(rows):
    lines = [json.dumps(r, ensure_ascii=False) for r in rows]
    FORECASTS.write_text(("\n".join(lines) + "\n") if lines else "", encoding="utf-8")


def _days_between(a, b):
    ya, ma, da = map(int, a.split("-"))
    yb, mb, db = map(int, b.split("-"))
    return (date(yb, mb, db) - date(ya, ma, da)).days


# ─────────────────────────── price:<TICKER> 讀法（照抄 settle_outcomes.py） ───────────────────────────

def _price_bars(ticker, _cache={}):
    if ticker in _cache:
        return _cache[ticker]
    p = CACHE_DIR / f"{ALIAS.get(ticker, ticker)}.json"
    bars = None
    if p.exists():
        try:
            raw = json.loads(p.read_text(encoding="utf-8")).get("weekly_bars") or []
            bars = [(b["week_end"], b["close"]) for b in raw if b.get("close")]
        except (json.JSONDecodeError, KeyError):
            bars = None
    _cache[ticker] = bars
    return bars


def _close_at_or_before(bars, ymd):
    """最近一根 date ≤ ymd 的收盤；無則 None。bars 已按日期升冪。"""
    best = None
    for d, c in bars:
        if d <= ymd:
            best = (d, c)
        else:
            break
    return best


# ─────────────────────────── rv:<TICKER> 讀法 ───────────────────────────
# data/flowmap_prices.json 是 rolling ~500 交易日快取（非完整歷史，由 scripts/build_flowmap.py
# 維護），逐日算 RV21（年化 21 交易日日對數報酬 sample std×√252×100）——公式與
# scripts/build_rv_base_rates.py／scripts/generate_rv_forecasts.py 逐字一致，三處口徑必須同步
# 變動（PREREG 凍結，見設計稿 §E3）。

def _flowmap_prices_data(_cache={}):
    if "d" not in _cache:
        try:
            _cache["d"] = json.loads(FLOWMAP_PRICES.read_text(encoding="utf-8"))
        except Exception:
            _cache["d"] = None
    return _cache["d"]


def _flowmap_bars(ticker):
    data = _flowmap_prices_data()
    if not data:
        return None
    bars = (data.get("series") or {}).get(ticker)
    if not bars:
        return None
    return sorted(((d, c) for d, c in bars), key=lambda x: x[0])


def _sample_std(xs):
    n = len(xs)
    if n < 2:
        return None
    mean = sum(xs) / n
    var = sum((x - mean) ** 2 for x in xs) / (n - 1)
    return var ** 0.5


def _rv21_series(ticker, _cache={}):
    """回傳升冪 [(date, rv21_pct), ...]；ticker 不在快取或歷史不足回傳 None。
    rv21_pct[i] 以「日 i」為結尾的 21 個對數報酬年化 sample std×100（vol 點）。"""
    if ticker in _cache:
        return _cache[ticker]
    bars = _flowmap_bars(ticker)
    if not bars or len(bars) < RV_WINDOW_TRADING_DAYS + 1:
        _cache[ticker] = None
        return None
    dates = [d for d, _ in bars]
    closes = [c for _, c in bars]
    rets = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))
            if closes[i - 1] > 0 and closes[i] > 0]
    out = []
    for d in range(RV_WINDOW_TRADING_DAYS, len(closes)):
        window_rets = rets[d - RV_WINDOW_TRADING_DAYS:d]
        if len(window_rets) != RV_WINDOW_TRADING_DAYS:
            continue
        s = _sample_std(window_rets)
        if s is None:
            continue
        out.append((dates[d], round(s * math.sqrt(252) * 100, 4)))
    _cache[ticker] = out or None
    return _cache[ticker]


# ─────────────────────────── pxd:<TICKER>／ttp:<TICKER> 讀法 ───────────────────────────
# 兩域語義完全相同（at_expiry／any_close），差別只在資料來源：pxd: 讀 data/flowmap_prices.json、
# ttp: 讀 data/trend_track_prices.json（forecast v2 設計稿 §4.2，B 包 tsmom producer 餵料）。
# 共用同一段判定邏輯，coverage_gap 判法與 rv: 域一致。

def _resolve_close_series(bars, resolver, ts, resolve_by, today, no_bar_reason):
    op_fn = OPS.get(resolver.get("op"))
    if not op_fn:
        return {"status": "void", "reason": f"bad_op:{resolver.get('op')}", "outcome": None, "coverage_gap": False}
    value = resolver.get("value")
    window = resolver.get("window", "any_close")
    last_date = bars[-1][0]
    coverage_gap = ts < bars[0][0]

    if window == "any_close":
        hit = any(op_fn(c, value) for d, c in bars if ts <= d <= resolve_by)
        if hit:
            return {"status": "resolved_yes", "reason": None, "outcome": 1, "coverage_gap": coverage_gap}
        if today >= resolve_by:
            if last_date < resolve_by:
                # cache 尚未追上 resolve_by（資料落後），暫不硬判 no
                return {"status": "open", "reason": None, "outcome": None, "coverage_gap": coverage_gap}
            return {"status": "resolved_no", "reason": None, "outcome": 0, "coverage_gap": coverage_gap}
        return {"status": "open", "reason": None, "outcome": None, "coverage_gap": coverage_gap}
    else:  # at_expiry
        if today < resolve_by:
            return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}
        if last_date < resolve_by:
            return {"status": "open", "reason": None, "outcome": None, "coverage_gap": coverage_gap}
        at = _close_at_or_before(bars, resolve_by)
        if not at:
            return {"status": "void", "reason": no_bar_reason, "outcome": None, "coverage_gap": True}
        _, px = at
        outcome = 1 if op_fn(px, value) else 0
        status = "resolved_yes" if outcome else "resolved_no"
        return {"status": status, "reason": None, "outcome": outcome, "coverage_gap": coverage_gap}


def _resolve_pxd(resolver, ts, resolve_by, today):
    ticker = resolver["series"].split(":", 1)[1]
    bars = _flowmap_bars(ticker)
    if not bars:
        return {"status": "void", "reason": f"pxd_ticker_missing:{ticker}", "outcome": None, "coverage_gap": False}
    return _resolve_close_series(bars, resolver, ts, resolve_by, today, f"pxd_no_bar_at_expiry:{ticker}")


def _trend_track_prices_data(_cache={}):
    if "d" not in _cache:
        try:
            _cache["d"] = json.loads(TREND_TRACK_PRICES.read_text(encoding="utf-8"))
        except Exception:
            _cache["d"] = None
    return _cache["d"]


def _ttp_bars(ticker):
    data = _trend_track_prices_data()
    if not data:
        return None
    bars = (data.get("series") or {}).get(ticker)
    if not bars:
        return None
    return sorted(((d, c) for d, c in bars), key=lambda x: x[0])


def _resolve_ttp(resolver, ts, resolve_by, today):
    ticker = resolver["series"].split(":", 1)[1]
    bars = _ttp_bars(ticker)
    if not bars:
        return {"status": "void", "reason": f"ttp_ticker_missing:{ticker}", "outcome": None, "coverage_gap": False}
    return _resolve_close_series(bars, resolver, ts, resolve_by, today, f"ttp_no_bar_at_expiry:{ticker}")


# ─────────────────────────── relspy:<TICKER> 讀法 ───────────────────────────
# 相對 SPY 超額報酬命題（forecast v2 設計稿 §4.3，D 包 dd-verdict producer 餵料）。只支援
# at_expiry；px_T 讀 weekly_cache（同 price: 域），spy_T 讀 flowmap_prices.json SPY。

def _any_daily_bars(ticker, _cache={}):
    """relspy 用的價格退路鏈：weekly_cache（個股）→ statlab_prices（SPDR 類股／SPY／TLT／^VIX）
    → flowmap_prices（SPY/QQQ/IWM/AGG）→ trend_track_prices（9 檔資產）。ETF 類命題（rrg-sector
    等）不在 weekly_cache，若無此退路會全數 void（2026-09-02 整合時 F5 包發現，orchestrator 補）。"""
    key = ticker.upper()
    if key in _cache:
        return _cache[key]
    bars = _price_bars(ticker)
    if not bars:
        for path in (STATLAB_PRICES, FLOWMAP_PRICES, TREND_TRACK_PRICES):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            ser = (data.get("series") or {}).get(ticker) or (data.get("series") or {}).get(key)
            if ser:
                bars = sorted(((d, c) for d, c in ser), key=lambda x: x[0])
                break
    _cache[key] = bars or None
    return _cache[key]

def _resolve_relspy(resolver, ts, resolve_by, today):
    ticker = resolver["series"].split(":", 1)[1]
    op_fn = OPS.get(resolver.get("op"))
    if not op_fn:
        return {"status": "void", "reason": f"bad_op:{resolver.get('op')}", "outcome": None, "coverage_gap": False}
    window = resolver.get("window", "at_expiry")
    if window != "at_expiry":
        return {"status": "void", "reason": f"relspy_unsupported_window:{window}", "outcome": None, "coverage_gap": False}
    value = resolver.get("value")
    base_px = resolver.get("base_px")
    base_spy = resolver.get("base_spy")
    if not base_px or not base_spy:
        return {"status": "void", "reason": f"relspy_missing_base:{ticker}", "outcome": None, "coverage_gap": False}

    if today < resolve_by:
        return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}

    px_bars = _any_daily_bars(ticker)
    spy_bars = _flowmap_bars("SPY")
    if not px_bars or not spy_bars:
        return {"status": "void", "reason": f"relspy_missing_price:{ticker}", "outcome": None, "coverage_gap": False}
    if px_bars[-1][0] < resolve_by or spy_bars[-1][0] < resolve_by:
        # 任一快取尚未追上 resolve_by（資料落後），暫不硬判
        return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}

    px_at = _close_at_or_before(px_bars, resolve_by)
    # SPY 對齊到 ticker 實際採用的那根 bar 日期（weekly_cache 為週線，可能早於 resolve_by 數日；
    # 兩腿若量到不同日期會系統性偏差），而非各自對齊 resolve_by。
    spy_at = _close_at_or_before(spy_bars, px_at[0]) if px_at else None
    if not px_at or not spy_at:
        return {"status": "void", "reason": f"relspy_missing_price:{ticker}", "outcome": None, "coverage_gap": False}

    _, px_T = px_at
    _, spy_T = spy_at
    outcome = 1 if op_fn((px_T / base_px) - (spy_T / base_spy), value) else 0
    status = "resolved_yes" if outcome else "resolved_no"
    return {"status": status, "reason": None, "outcome": outcome, "coverage_gap": False}


# ─────────────────────────── vixts:SLOPE 讀法 ───────────────────────────
# data/statlab_prices.json 的 ^VIX3M − ^VIX 收盤差（只取兩序列共同交易日）。該檔
# 由另一條 pipeline（scripts/build_statlab.py）維護，本檔唯讀。缺檔或無重疊交易日
# 視為「資料層暫缺」——保持 open＋警告，不 void（見檔頭 docstring）。

def _statlab_prices_data(_cache={}):
    if "d" not in _cache:
        try:
            _cache["d"] = json.loads(STATLAB_PRICES.read_text(encoding="utf-8"))
        except Exception:
            _cache["d"] = None
    return _cache["d"]


def _vixts_slope_pts(_cache={}):
    if "d" in _cache:
        return _cache["d"]
    data = _statlab_prices_data()
    if not data:
        _cache["d"] = None
        return None
    series = data.get("series") or {}
    vix = {d: c for d, c in (series.get("^VIX") or [])}
    vix3m = {d: c for d, c in (series.get("^VIX3M") or [])}
    common = sorted(set(vix) & set(vix3m))
    pts = [(d, round(vix3m[d] - vix[d], 4)) for d in common] or None
    _cache["d"] = pts
    return pts


def _resolve_vixts(resolver, ts, resolve_by, today):
    key = resolver["series"].split(":", 1)[1]
    if key != "SLOPE":
        return {"status": "void", "reason": f"unknown_vixts_key:{key}", "outcome": None, "coverage_gap": False}
    pts = _vixts_slope_pts()
    if pts is None:
        return {"status": "open", "reason": "vixts_data_unavailable", "outcome": None, "coverage_gap": False}
    op_fn = OPS.get(resolver.get("op"))
    if not op_fn:
        return {"status": "void", "reason": f"bad_op:{resolver.get('op')}", "outcome": None, "coverage_gap": False}
    value = resolver.get("value")
    window = resolver.get("window", "any_close")
    last_date = pts[-1][0]
    coverage_gap = ts < pts[0][0]

    if window == "any_close":
        hit = any(op_fn(v, value) for d, v in pts if ts <= d <= resolve_by)
        if hit:
            return {"status": "resolved_yes", "reason": None, "outcome": 1, "coverage_gap": coverage_gap}
        if today >= resolve_by:
            if last_date < resolve_by:
                # statlab_prices.json 尚未追上 resolve_by（資料層暫缺／落後），暫不硬判 no
                return {"status": "open", "reason": "vixts_stale", "outcome": None, "coverage_gap": coverage_gap}
            return {"status": "resolved_no", "reason": None, "outcome": 0, "coverage_gap": coverage_gap}
        return {"status": "open", "reason": None, "outcome": None, "coverage_gap": coverage_gap}
    else:  # at_expiry
        if today < resolve_by:
            return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}
        if last_date < resolve_by:
            return {"status": "open", "reason": "vixts_stale", "outcome": None, "coverage_gap": coverage_gap}
        at = _close_at_or_before(pts, resolve_by)
        if not at:
            return {"status": "void", "reason": "vixts_no_point_at_expiry", "outcome": None, "coverage_gap": True}
        _, sl = at
        outcome = 1 if op_fn(sl, value) else 0
        status = "resolved_yes" if outcome else "resolved_no"
        return {"status": status, "reason": None, "outcome": outcome, "coverage_gap": coverage_gap}


# ─────────────────────────── monitor:<key> 讀法 ───────────────────────────

def _monitor_data(_cache={}):
    if "d" not in _cache:
        try:
            _cache["d"] = json.loads(MONITOR_LATEST.read_text(encoding="utf-8"))
        except Exception:
            _cache["d"] = None
    return _cache["d"]


def _monitor_item(key):
    data = _monitor_data()
    if not data:
        return None
    for cat in data.get("categories", []):
        for it in cat.get("items", []):
            if it.get("key") == key:
                return it
    return None


def _parse_num(v):
    """latest.json 的 val／spark 元素是各 series 自訂格式化字串或數字（"7,686.14"／"2.60%"／
    "0bps"）；一律取去除逗號後第一個數字 token，尺度照原樣、不做單位換算。"""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(",", "")
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def _approx_trading_dates(as_of_ymd, n):
    """由 as_of（spark 最後一點日期）往前反推 n 個近似交易日（只排除週末，不排除假日 ——
    近似值，供 any_close／at_expiry 判斷用，非精確交易日曆）。"""
    y, m, d = map(int, as_of_ymd.split("-"))
    cur = date(y, m, d)
    out = [cur]
    while len(out) < n:
        cur -= timedelta(days=1)
        if cur.weekday() < 5:
            out.append(cur)
    out.reverse()
    return [dt.isoformat() for dt in out]


def _monitor_series_points(item):
    """回傳 [(近似日期, 數值), ...] 升冪；最後一點對應 item['date']（精確），
    其餘為往前反推的近似交易日（見 _approx_trading_dates）。"""
    spark = item.get("spark") or []
    as_of = item.get("date")
    if not spark or not as_of:
        return []
    dates = _approx_trading_dates(as_of, len(spark))
    pts = [(dates[i], _parse_num(spark[i])) for i in range(len(spark))]
    return [(d, v) for d, v in pts if v is not None]


# ─────────────────────────── monitor 域單位正規化（forecast v2 設計稿 §4.1） ───────────────────────────

MONITOR_SCALE_CANDIDATES = [0.01, 0.1, 1, 10, 100, 1000]
MONITOR_SCALE_TOLERANCE = 0.05  # ±5%


def _compute_monitor_scale(item):
    """回傳 (scale, note)：
      scale=<候選值>, note=None            → 正常換算（scale 落在候選值 ±5% 內）
      scale=None, note="unit_scale_unknown" → val 或 spark 尾值為 0／缺值／spark 空，
                                               沿用 v1 舊行為（resolver.value 不換算，直接
                                               比對 spark 尺度）
      scale=False, note="unit_ambiguous"    → val/spark 尾值的比值不落在任何候選尺度 ±5%
                                               內，無法判定，落帳／結算皆拒絕（void）
    設計稿原文只點名「兩者皆為 0 或 spark 空」對應 unit_scale_unknown；val 無法解析
    （None）、或僅 spark 尾值為 0（除以零）皆屬同一精神下的防禦性延伸，一併退回舊行為
    而非拋例外。"""
    val = _parse_num(item.get("val"))
    spark = item.get("spark") or []
    spark_last = _parse_num(spark[-1]) if spark else None
    if val is None or spark_last is None or not spark:
        return None, "unit_scale_unknown"
    if val == 0 and spark_last == 0:
        return None, "unit_scale_unknown"
    if spark_last == 0:
        return None, "unit_scale_unknown"
    raw_scale = val / spark_last
    for cand in MONITOR_SCALE_CANDIDATES:
        if abs(raw_scale - cand) <= cand * MONITOR_SCALE_TOLERANCE:
            return cand, None
    return False, "unit_ambiguous"


# ─────────────────────────── resolver 驗證（給 q.py --forecast-add 用） ───────────────────────────

def check_resolver(series):
    """驗證 resolver.series 可機械解析；回傳 (ok, message)。"""
    if ":" not in series:
        return False, "series 格式須為 <domain>:<key>"
    ns, key = series.split(":", 1)
    if ns == "price":
        p = CACHE_DIR / f"{ALIAS.get(key, key)}.json"
        if not p.exists():
            return False, f"找不到 {p}"
        bars = _price_bars(key)
        if not bars:
            return False, f"{p} 存在但無可用週線資料"
        d, c = bars[-1]
        return True, f"{d} close={c}"
    if ns == "monitor":
        item = _monitor_item(key)
        if item is None:
            return False, f"docs/monitor/data/latest.json 找不到 key={key}"
        scale, note = _compute_monitor_scale(item)
        spark = item.get("spark") or []
        spark_last = _parse_num(spark[-1]) if spark else None
        if scale is False:
            return False, (f"{item.get('date')} val={item.get('val')}（顯示值）／spark 尾值={spark_last}："
                            f"scale 判定為 unit_ambiguous（比值不落在 {MONITOR_SCALE_CANDIDATES} 任一值 "
                            f"±{int(MONITOR_SCALE_TOLERANCE*100)}% 內），無法落帳／結算")
        if scale is None:
            return True, (f"{item.get('date')} val={item.get('val')}（顯示值）／spark 尾值={spark_last}／"
                           f"scale=unknown（val 或 spark 尾值為 0 或缺值，沿用 v1 舊行為：resolver.value "
                           f"須與 spark 原始尺度一致，不會換算）")
        return True, (f"{item.get('date')} val={item.get('val')}（顯示值）／spark 尾值={spark_last}／"
                       f"scale={scale}｜value 若寫 X（顯示單位）會被換成 X/{scale} 比對 spark")
    if ns == "rv":
        pts = _rv21_series(key)
        if not pts:
            return False, f"data/flowmap_prices.json 找不到 ticker={key}，或歷史不足 {RV_WINDOW_TRADING_DAYS + 1} 根日線"
        d, v = pts[-1]
        return True, f"{d} RV21={v:.2f}（年化 vol 點；21 交易日日對數報酬 sample std×√252×100）"
    if ns == "pxd":
        bars = _flowmap_bars(key)
        if not bars:
            return False, f"data/flowmap_prices.json 找不到 ticker={key}"
        d, c = bars[-1]
        return True, f"{d} close={c}"
    if ns == "ttp":
        bars = _ttp_bars(key)
        if not bars:
            return False, f"data/trend_track_prices.json 找不到 ticker={key}"
        d, c = bars[-1]
        return True, f"{d} close={c}"
    if ns == "relspy":
        bars = _any_daily_bars(key)
        spy_bars = _flowmap_bars("SPY")
        if not bars:
            return False, f"找不到 {CACHE_DIR / (ALIAS.get(key, key) + '.json')}"
        if not spy_bars:
            return False, "data/flowmap_prices.json 找不到 SPY"
        d, c = bars[-1]
        ds, cs = spy_bars[-1]
        return True, (f"{key}={d} close={c}／SPY={ds} close={cs}"
                       f"（relspy 另需 resolver.base_px／base_spy／base_date，由落帳端提供，本檢查不驗證）")
    if ns == "vixts":
        if key != "SLOPE":
            return False, f"vixts 域目前只支援 key=SLOPE（收到 {key}）"
        pts = _vixts_slope_pts()
        if pts is None:
            return False, (f"{STATLAB_PRICES} 不存在、無法讀取，或 ^VIX／^VIX3M 無重疊交易日"
                            f"（資料層暫缺——注意：結算時本域對此情形保持 open 不 void，"
                            f"與其他域的「查無即 void」不同）")
        d, v = pts[-1]
        state = "contango" if v > 0 else ("inverted" if v < 0 else "flat")
        return True, f"{d} slope=^VIX3M-^VIX={v:+.2f}（{state}）"
    if ns == "detective":
        return False, "detective 域結算未實作（見本檔 docstring），暫不接受此域落帳"
    return False, f"未知 domain：{ns}"


# ─────────────────────────── 結算主邏輯 ───────────────────────────

def _resolve_price(resolver, ts, resolve_by, today):
    ticker = resolver["series"].split(":", 1)[1]
    bars = _price_bars(ticker)
    if not bars:
        return {"status": "void", "reason": "price_no_cache", "outcome": None, "coverage_gap": False}
    op_fn = OPS.get(resolver.get("op"))
    if not op_fn:
        return {"status": "void", "reason": f"bad_op:{resolver.get('op')}", "outcome": None, "coverage_gap": False}
    value = resolver.get("value")
    window = resolver.get("window", "any_close")
    last_date = bars[-1][0]

    if window == "any_close":
        hit = any(op_fn(c, value) for d, c in bars if ts <= d <= resolve_by)
        if hit:
            return {"status": "resolved_yes", "reason": None, "outcome": 1, "coverage_gap": False}
        if today >= resolve_by:
            if last_date < resolve_by:
                # cache 尚未追上 resolve_by（資料落後），暫不硬判 no
                return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}
            return {"status": "resolved_no", "reason": None, "outcome": 0, "coverage_gap": False}
        return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}
    else:  # at_expiry
        if today < resolve_by:
            return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}
        at = _close_at_or_before(bars, resolve_by)
        if not at:
            return {"status": "void", "reason": "price_no_bar_at_expiry", "outcome": None, "coverage_gap": False}
        _, px = at
        outcome = 1 if op_fn(px, value) else 0
        status = "resolved_yes" if outcome else "resolved_no"
        return {"status": status, "reason": None, "outcome": outcome, "coverage_gap": False}


def _resolve_monitor(resolver, ts, resolve_by, today):
    key = resolver["series"].split(":", 1)[1]
    item = _monitor_item(key)
    if item is None:
        return {"status": "void", "reason": f"monitor_key_missing:{key}", "outcome": None, "coverage_gap": False}
    if item.get("stale"):
        return {"status": "void", "reason": f"monitor_series_stale:{key}", "outcome": None, "coverage_gap": False}
    op_fn = OPS.get(resolver.get("op"))
    if not op_fn:
        return {"status": "void", "reason": f"bad_op:{resolver.get('op')}", "outcome": None, "coverage_gap": False}

    # v2 單位正規化（§4.1）：resolver.value 維持「顯示單位」，換算成 spark 尺度後才比對。
    scale, scale_note = _compute_monitor_scale(item)
    if scale is False:
        return {"status": "void", "reason": f"unit_ambiguous:{key}", "outcome": None, "coverage_gap": False}
    raw_value = resolver.get("value")
    value = (raw_value / scale) if scale else raw_value  # scale=None（舊行為）時不換算
    if scale_note == "unit_scale_unknown":
        print(f"  ⚠ monitor:{key} scale 判定為 unit_scale_unknown（val 或 spark 尾值為 0/缺值），"
              f"沿用 v1 舊行為：resolver.value 未換算，直接比對 spark 原始尺度")

    window = resolver.get("window", "any_close")
    as_of = item.get("date")
    pts = _monitor_series_points(item)
    # ts 早於本次可觀察的最早近似日 → ts～窗口起點之間可能有漏判空窗（誠實標記，不影響判定）
    coverage_gap = bool(pts) and ts < pts[0][0]

    if window == "any_close":
        end = min(today, resolve_by)
        hit = any(op_fn(v, value) for d, v in pts if ts <= d <= end)
        if hit:
            return {"status": "resolved_yes", "reason": None, "outcome": 1, "coverage_gap": coverage_gap}
        if today >= resolve_by and as_of and as_of >= resolve_by:
            return {"status": "resolved_no", "reason": None, "outcome": 0, "coverage_gap": coverage_gap}
        return {"status": "open", "reason": None, "outcome": None, "coverage_gap": coverage_gap}
    else:  # at_expiry
        if today < resolve_by:
            return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}
        if not as_of or as_of < resolve_by:
            # series 資料尚未追上 resolve_by
            return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}
        at = None
        for d, v in pts:
            if d <= resolve_by:
                at = (d, v)
            else:
                break
        if at is None:
            return {"status": "void", "reason": f"monitor_no_point_at_expiry:{key}", "outcome": None, "coverage_gap": True}
        outcome = 1 if op_fn(at[1], value) else 0
        status = "resolved_yes" if outcome else "resolved_no"
        return {"status": status, "reason": None, "outcome": outcome, "coverage_gap": False}


def _resolve_rv(resolver, ts, resolve_by, today):
    ticker = resolver["series"].split(":", 1)[1]
    pts = _rv21_series(ticker)
    if not pts:
        return {"status": "void", "reason": f"rv_ticker_missing_or_insufficient:{ticker}", "outcome": None, "coverage_gap": False}
    op_fn = OPS.get(resolver.get("op"))
    if not op_fn:
        return {"status": "void", "reason": f"bad_op:{resolver.get('op')}", "outcome": None, "coverage_gap": False}
    value = resolver.get("value")
    window = resolver.get("window", "any_close")
    last_date = pts[-1][0]
    # ts 早於本次可觀察範圍最早的 RV21 可算日期 → data/flowmap_prices.json 是 rolling
    # ~500 交易日快取，隨時間往前捲動裁切，視窗前段可能已不可考——誠實標記，不硬判
    # （沿用 monitor 域 coverage_gap 慣例，浮出到既有 coverage_warning 機制）。
    coverage_gap = ts < pts[0][0]

    if window == "any_close":
        hit = any(op_fn(v, value) for d, v in pts if ts <= d <= resolve_by)
        if hit:
            return {"status": "resolved_yes", "reason": None, "outcome": 1, "coverage_gap": coverage_gap}
        if today >= resolve_by:
            if last_date < resolve_by:
                # 快取尚未追上 resolve_by（資料落後），暫不硬判 no
                return {"status": "open", "reason": None, "outcome": None, "coverage_gap": coverage_gap}
            return {"status": "resolved_no", "reason": None, "outcome": 0, "coverage_gap": coverage_gap}
        return {"status": "open", "reason": None, "outcome": None, "coverage_gap": coverage_gap}
    else:  # at_expiry
        if today < resolve_by:
            return {"status": "open", "reason": None, "outcome": None, "coverage_gap": False}
        if last_date < resolve_by:
            # 快取尚未追上 resolve_by（資料落後），暫不硬判
            return {"status": "open", "reason": None, "outcome": None, "coverage_gap": coverage_gap}
        at = _close_at_or_before(pts, resolve_by)
        if not at:
            return {"status": "void", "reason": f"rv_no_point_at_expiry:{ticker}", "outcome": None, "coverage_gap": True}
        _, rv = at
        outcome = 1 if op_fn(rv, value) else 0
        status = "resolved_yes" if outcome else "resolved_no"
        return {"status": status, "reason": None, "outcome": outcome, "coverage_gap": coverage_gap}


def settle(rows, today_str):
    updated = []
    resolved_ids, void_pairs, coverage_ids = [], [], []
    det_pending = 0
    for r in rows:
        if r.get("status") != "open":
            updated.append(r)
            continue
        resolver = r.get("resolver") or {}
        series = resolver.get("series", "")
        ns = series.split(":", 1)[0] if ":" in series else ""
        ts, resolve_by = r.get("ts"), r.get("resolve_by")

        if not (ts and resolve_by):
            r["status"] = "void"
            r["resolved_ts"] = today_str
            r["outcome"] = None
            r["brier"] = None
            void_pairs.append((r.get("id"), "missing_ts_or_resolve_by"))
            updated.append(r)
            continue

        if ns == "detective":
            print(f"  ⚠ {r.get('id')}: detective 域結算未實作，保持 open")
            det_pending += 1
            updated.append(r)
            continue
        elif ns == "price":
            res = _resolve_price(resolver, ts, resolve_by, today_str)
        elif ns == "monitor":
            res = _resolve_monitor(resolver, ts, resolve_by, today_str)
        elif ns == "rv":
            res = _resolve_rv(resolver, ts, resolve_by, today_str)
        elif ns == "pxd":
            res = _resolve_pxd(resolver, ts, resolve_by, today_str)
        elif ns == "ttp":
            res = _resolve_ttp(resolver, ts, resolve_by, today_str)
        elif ns == "relspy":
            res = _resolve_relspy(resolver, ts, resolve_by, today_str)
        elif ns == "vixts":
            res = _resolve_vixts(resolver, ts, resolve_by, today_str)
            if res["status"] == "open" and res.get("reason") in ("vixts_data_unavailable", "vixts_stale"):
                print(f"  ⚠ {r.get('id')}: vixts 域資料層暫缺（{res['reason']}），保持 open（不 void）")
        else:
            res = {"status": "void", "reason": f"unknown_namespace:{ns}", "outcome": None, "coverage_gap": False}

        if res["status"] == "open":
            updated.append(r)
            continue

        r["resolved_ts"] = today_str
        if res["status"] == "void":
            r["status"] = "void"
            r["outcome"] = None
            r["brier"] = None
            r["brier_clim"] = None
            r["beat_clim"] = None
            void_pairs.append((r.get("id"), res["reason"]))
        else:
            r["status"] = res["status"]
            outcome = res["outcome"]
            r["outcome"] = outcome
            p = r.get("p")
            r["brier"] = round((p - outcome) ** 2, 4) if p is not None else None
            # §4.4：每筆回寫 brier_clim／beat_clim（無 p_clim 的筆只計 raw Brier，見 §1）。
            p_clim = r.get("p_clim")
            if p_clim is not None:
                r["brier_clim"] = round((p_clim - outcome) ** 2, 4)
                if r["brier"] is None:
                    r["beat_clim"] = None
                elif r["brier"] < r["brier_clim"]:
                    r["beat_clim"] = True
                elif r["brier"] > r["brier_clim"]:
                    r["beat_clim"] = False
                else:
                    r["beat_clim"] = None  # 相等為 null（§2 原文）
            else:
                r["brier_clim"] = None
                r["beat_clim"] = None
            resolved_ids.append(r.get("id"))
        if res.get("coverage_gap"):
            coverage_ids.append(r.get("id"))
        updated.append(r)
    return updated, resolved_ids, void_pairs, det_pending, coverage_ids


# ─────────────────────────── sources 摘要（forecast v2 設計稿 §3.2） ───────────────────────────

def _calibration_buckets(rows):
    """10 桶校準曲線（預測機率 vs 實際頻率），對象＝該 source 全部 resolved 筆（不限定要有
    p_clim——校準曲線只看「p 本身準不準」，與 base rate 無關）。"""
    buckets = [[] for _ in range(10)]
    for r in rows:
        p = r.get("p")
        if p is None or r.get("outcome") is None:
            continue
        buckets[min(int(p * 10), 9)].append(r)
    labels = [f"[{i * 10}-{(i + 1) * 10}%]" for i in range(10)]
    out = []
    for i, b in enumerate(buckets):
        if not b:
            out.append({"bucket": labels[i], "n": 0, "avg_p": None, "freq": None})
            continue
        avg_p = round(sum(r["p"] for r in b) / len(b), 3)
        freq = round(sum(r["outcome"] for r in b) / len(b), 3)
        out.append({"bucket": labels[i], "n": len(b), "avg_p": avg_p, "freq": freq})
    return out


def _block_bootstrap_bss_ci(clim_rows):
    """§3.5：以 block_key 分塊整塊重抽（block bootstrap），2000 次，seed=20260902，
    回傳 [p5, p95] 的 BSS 90% 信賴區間。clim_rows 須已是「resolved 且 p_clim／brier／
    brier_clim 齊備」的列表。呼叫端負責先判斷 n_eff>=20 才呼叫本函式。"""
    blocks = defaultdict(list)
    for r in clim_rows:
        blocks[r.get("block_key")].append(r)
    block_keys = list(blocks.keys())
    if not block_keys:
        return [None, None]
    rng = random.Random(BOOTSTRAP_SEED)
    samples = []
    for _ in range(BOOTSTRAP_N):
        chosen = [rng.choice(block_keys) for _ in block_keys]
        pooled = [r for bk in chosen for r in blocks[bk]]
        if not pooled:
            continue
        mb = sum(r["brier"] for r in pooled) / len(pooled)
        mbc = sum(r["brier_clim"] for r in pooled) / len(pooled)
        if mbc <= 0:
            continue
        samples.append(1 - mb / mbc)
    if not samples:
        return [None, None]
    samples.sort()

    def _pct(q):
        idx = min(len(samples) - 1, max(0, int(round(q / 100 * (len(samples) - 1)))))
        return round(samples[idx], 4)

    return [_pct(5), _pct(95)]


def _compute_sprt(beat_clim_seq, n_eff, prior_sprt):
    """§3.3：SPRT 序貫檢定。beat_clim_seq 為依 resolved_ts 升冪排序的 bool 序列（每筆
    resolved 且 beat_clim 非 null 的 beat_clim）。決策需 n_eff>=SPRT_MIN_N_EFF 才允許落定；
    一旦落定（prior_sprt.state 為 accept_h1／accept_h0）即鎖存 state／decided_at／
    decided_n，之後樣本仍持續累計顯示（llr／n_used 每次都重算），但狀態不再改變——只有
    校準輪能重設（人工改 forecast_settlement.json 或砍檔重跑，本函式不提供自動重設）。"""
    llr = sum(SPRT_LLR_HIT if hit else SPRT_LLR_MISS for hit in beat_clim_seq)
    n_used = len(beat_clim_seq)

    prior_state = (prior_sprt or {}).get("state")
    if prior_state in ("accept_h1", "accept_h0"):
        state = prior_state
        decided_at = (prior_sprt or {}).get("decided_at")
        decided_n = (prior_sprt or {}).get("decided_n")
    else:
        decided_at, decided_n = None, None
        if n_eff < SPRT_MIN_N_EFF:
            state = "continue"
        elif llr >= SPRT_A:
            state = "accept_h1"
            decided_at = date.today().isoformat()
            decided_n = n_used
        elif llr <= SPRT_B:
            state = "accept_h0"
            decided_at = date.today().isoformat()
            decided_n = n_used
        else:
            state = "continue"

    return {
        "p0": SPRT_P0, "p1": SPRT_P1, "alpha": SPRT_ALPHA, "beta": SPRT_BETA,
        "A": SPRT_A, "B": SPRT_B,
        "llr": round(llr, 5), "n_used": n_used, "state": state,
        "decided_at": decided_at, "decided_n": decided_n,
    }


def _source_summary(rows_for_src, prior_sprt):
    resolved = [r for r in rows_for_src if r.get("status") in ("resolved_yes", "resolved_no")]
    n_resolved = len(resolved)

    episodes = {(r.get("episode_id") or r.get("id")) for r in resolved}
    n_eff = len(episodes)

    clim_rows = [r for r in resolved
                 if r.get("p_clim") is not None and r.get("brier") is not None
                 and r.get("brier_clim") is not None]
    n_with_clim = len(clim_rows)

    all_briers = [r["brier"] for r in resolved if r.get("brier") is not None]
    mean_brier = round(sum(all_briers) / len(all_briers), 4) if all_briers else None

    mean_brier_clim, bss = None, None
    if clim_rows:
        mbc = sum(r["brier_clim"] for r in clim_rows) / len(clim_rows)
        mb_clim_subset = sum(r["brier"] for r in clim_rows) / len(clim_rows)
        mean_brier_clim = round(mbc, 4)
        if mbc > 0:
            bss = round(1 - mb_clim_subset / mbc, 4)

    bss_ci90 = [None, None]
    if n_eff >= SPRT_MIN_N_EFF and clim_rows:
        bss_ci90 = _block_bootstrap_bss_ci(clim_rows)

    beat_clim_rows = sorted((r for r in resolved if r.get("beat_clim") is not None),
                            key=lambda r: r.get("resolved_ts") or "")
    beat_clim_seq = [bool(r["beat_clim"]) for r in beat_clim_rows]
    sprt = _compute_sprt(beat_clim_seq, n_eff, prior_sprt)

    if sprt["state"] == "accept_h1":
        status, status_label = "green", "🟢 已證實優於基準"
    elif sprt["state"] == "accept_h0":
        status, status_label = "red", "🔴 已證實不優於基準，等校準輪處決"
    else:
        status, status_label = "yellow", f"🟡 證據累積中（n_eff={n_eff}／{SPRT_MIN_N_EFF}，LLR={sprt['llr']}）"

    return {
        "n_resolved": n_resolved, "n_eff": n_eff, "n_with_clim": n_with_clim,
        "mean_brier": mean_brier, "mean_brier_clim": mean_brier_clim,
        "bss": bss, "bss_ci90": bss_ci90,
        "sprt": sprt,
        "status": status, "status_label": status_label,
        "calibration_buckets": _calibration_buckets(resolved),
    }


def build_sources_summary(updated, prior_sources):
    by_source = defaultdict(list)
    for r in updated:
        by_source[r.get("source") or "—"].append(r)
    out = {}
    for src, rs in by_source.items():
        prior_sprt = (prior_sources.get(src) or {}).get("sprt")
        out[src] = _source_summary(rs, prior_sprt)
    return out


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--check-resolver":
        if len(sys.argv) < 3:
            print("用法：python knowledge/settle_forecasts.py --check-resolver <domain>:<key>")
            sys.exit(2)
        ok, msg = check_resolver(sys.argv[2])
        print(("OK " if ok else "MISSING ") + msg)
        sys.exit(0 if ok else 1)

    today_str = date.today().isoformat()
    rows = _load_forecasts()

    prev_last_run = None
    prior_sources = {}
    if OUT.exists():
        try:
            prev_out = json.loads(OUT.read_text(encoding="utf-8"))
            prev_last_run = prev_out.get("last_run")
            prior_sources = prev_out.get("sources") or {}
        except Exception:
            prev_last_run = None
            prior_sources = {}

    updated, resolved_ids, void_pairs, det_pending, coverage_ids = settle(rows, today_str)
    _write_forecasts(updated)

    has_monitor = any((r.get("resolver") or {}).get("series", "").startswith("monitor:") for r in updated)
    coverage_warning = None
    if has_monitor and prev_last_run:
        gap = _days_between(prev_last_run, today_str)
        if gap > COVERAGE_WARN_DAYS:
            coverage_warning = (f"monitor 域上次結算距今 {gap} 天（> {COVERAGE_WARN_DAYS} 天門檻），"
                                 f"spark 只留最近約 30 個交易日，期間內若有瞬間觸及可能已被錯過，宜盡快加密執行頻率。")
    if coverage_ids:
        note = (f"另有 {len(coverage_ids)} 筆 forecast 的 ts 早於本次可觀察範圍的最早日期"
                f"（monitor 域＝spark 近似交易日反推；rv 域＝flowmap_prices.json rolling 快取邊界），"
                f"該筆窗口可能有漏判空窗：{coverage_ids}")
        coverage_warning = f"{coverage_warning} {note}" if coverage_warning else note

    n_open = sum(1 for r in updated if r.get("status") == "open")
    n_resolved_yes = sum(1 for r in updated if r.get("status") == "resolved_yes")
    n_resolved_no = sum(1 for r in updated if r.get("status") == "resolved_no")
    n_void = sum(1 for r in updated if r.get("status") == "void")

    sources = build_sources_summary(updated, prior_sources)

    out = {
        "schema": "forecast-settlement-v2",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "last_run": today_str,
        "prev_run": prev_last_run,
        "coverage_warning": coverage_warning,
        "n_open": n_open,
        "n_resolved_yes": n_resolved_yes,
        "n_resolved_no": n_resolved_no,
        "n_void": n_void,
        "n_detective_pending": det_pending,
        "void_reasons": void_pairs,
        "sources": sources,
        "rows": updated,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"forecast_settlement.json：open {n_open}／resolved_yes {n_resolved_yes}／resolved_no {n_resolved_no}／"
          f"void {n_void}／detective 待實作 {det_pending}，as_of {today_str}")
    if coverage_warning:
        print(f"⚠ {coverage_warning}")
    if void_pairs:
        print("  void 原因：", dict(Counter(reason for _, reason in void_pairs)))
    for src, summ in sorted(sources.items()):
        print(f"  sources[{src}]：n_resolved={summ['n_resolved']} n_eff={summ['n_eff']} "
              f"n_with_clim={summ['n_with_clim']} bss={summ['bss']} sprt={summ['sprt']['state']} "
              f"status={summ['status']}")


if __name__ == "__main__":
    main()
