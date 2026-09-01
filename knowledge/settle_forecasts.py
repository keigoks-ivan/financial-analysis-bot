#!/usr/bin/env python3
"""
settle_forecasts.py — 機率化判讀對帳簿的機械結算（forecasts.jsonl → forecast_settlement.json）。

鏡像 settle_outcomes.py 的模式：讀 knowledge/forecasts.jsonl 的 open 筆，依各筆 resolver 判
resolved_yes／resolved_no／void，算 Brier，把 status/resolved_ts/outcome/brier 四欄就地回寫
forecasts.jsonl（整檔重寫、保序，其他欄位原樣）；彙總統計另存 knowledge/forecast_settlement.json
（衍生物，gitignore，本地重算）。q.py --forecasts 消費本檔：無檔或比 forecasts.jsonl／
monitor latest.json／週線 cache 舊會自動重跑。

resolver 六個 series 命名空間：
  - price:<TICKER>  → data/weekly_cache/<TICKER>.json 週線收盤（完整歷史；ALIAS／
                      _close_at_or_before 讀法照抄 settle_outcomes.py）。
  - monitor:<key>   → docs/monitor/data/latest.json 的 categories[].items[]（key 比對）。
                      歷史覆蓋只有 spark 陣列（近 ~30 個交易日、只排除週末不排除假日的近似
                      交易日反推，非精確交易日曆），故 any_close 窗口的完整性依賴本腳本的
                      執行頻率 —— **本腳本須至少每 30 天跑一次**，否則兩次執行之間若有瞬間
                      觸及可能被錯過（spark 只留最近窗，不保證看到全歷史）。每次執行都會在
                      輸出 JSON 記錄 last_run／prev_run，間隔過久或個別 forecast 的 ts 早於
                      本次可觀察範圍時一併印 coverage_warning，不靜默硬判。
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
  - detective:*     → 本期不實作。遇到即印警告、該筆保持 open，不硬判。

op 支援 >／<>=／<=；window 支援 any_close（區間內任一收盤觸及即 yes）與 at_expiry（只看到期
時的值）。

單位注意（monitor 域）：latest.json 的 val／spark 是各 series 自訂格式（如 dgs10 "4.73%"、
sofr_iorb "0bps"），本腳本一律取其去除逗號後第一個數字 token 的原始尺度（例：hy_oas
val="2.60%" → 比較數值 2.60，非 260bp；sofr_iorb val="0bps" → 比較數值 0，本身就是 bp 整數）。
**尺度因 series 而異、不統一換算**——resolver.value 須採與該 series 原始數值相同的尺度落帳，
q.py --forecast-add／本檔 --check-resolver 都會印出目前值供對齊。

單位注意（rv 域）：RV21 一律以「百分比 vol 點」為尺度（例：10.26 代表年化已實現波動 10.26%，
非 0.1026）——與 scripts/build_rv_base_rates.py／scripts/generate_rv_forecasts.py 產出的
resolver.value 尺度一致，直接比對即可，不需換算。

單位注意（pxd 域）：與 price 域一致，直接是該 ticker 的日線收盤價原始尺度（美元／點數），
resolver.value 用同尺度落帳。

單位注意（vixts 域）：slope 一律以「vol 點」為尺度（^VIX3M − ^VIX 的收盤差，可正可負；
正＝contango，負＝inverted），與 scripts/build_vixts_base_rates.py／generate_vix_forecasts.py
產出的 resolver.value 尺度一致。

CLI：
  python knowledge/settle_forecasts.py                       # 正常結算，重寫 forecasts.jsonl + 輸出 settlement
  python knowledge/settle_forecasts.py --check-resolver price:NVDA     # 驗證 resolver 可解析（給 q.py 用）
  python knowledge/settle_forecasts.py --check-resolver monitor:hy_oas
  python knowledge/settle_forecasts.py --check-resolver rv:SPY
  python knowledge/settle_forecasts.py --check-resolver pxd:SPY
  python knowledge/settle_forecasts.py --check-resolver vixts:SLOPE
"""
import json
import math
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

KDIR = Path(__file__).resolve().parent
ROOT = KDIR.parent
FORECASTS = KDIR / "forecasts.jsonl"
OUT = KDIR / "forecast_settlement.json"
CACHE_DIR = ROOT / "data" / "weekly_cache"
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"  # rv:／pxd: 域讀法（見 build_rv_base_rates.py）
STATLAB_PRICES = ROOT / "data" / "statlab_prices.json"  # vixts: 域讀法（見 build_vixts_base_rates.py）

RV_WINDOW_TRADING_DAYS = 21  # 須與 scripts/build_rv_base_rates.py／generate_rv_forecasts.py 一致（PREREG 凍結）

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


# ─────────────────────────── pxd:<TICKER> 讀法 ───────────────────────────
# data/flowmap_prices.json 該 ticker 日線收盤，直接讀（非 rv: 域的 RV21 轉換）。
# 同一份 rolling ~500 交易日快取，coverage_gap 判法與 rv: 域一致。

def _resolve_pxd(resolver, ts, resolve_by, today):
    ticker = resolver["series"].split(":", 1)[1]
    bars = _flowmap_bars(ticker)
    if not bars:
        return {"status": "void", "reason": f"pxd_ticker_missing:{ticker}", "outcome": None, "coverage_gap": False}
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
            return {"status": "void", "reason": f"pxd_no_bar_at_expiry:{ticker}", "outcome": None, "coverage_gap": True}
        _, px = at
        outcome = 1 if op_fn(px, value) else 0
        status = "resolved_yes" if outcome else "resolved_no"
        return {"status": status, "reason": None, "outcome": outcome, "coverage_gap": coverage_gap}


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
        return True, (f"{item.get('date')} val={item.get('val')}"
                       f"（比較數值＝去除逗號/單位符號後的原始數字，尺度依 series 而定，非統一 bp 或 %，落帳前請對齊）")
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
    value = resolver.get("value")
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
            void_pairs.append((r.get("id"), res["reason"]))
        else:
            r["status"] = res["status"]
            r["outcome"] = res["outcome"]
            p = r.get("p")
            r["brier"] = round((p - res["outcome"]) ** 2, 4) if p is not None else None
            resolved_ids.append(r.get("id"))
        if res.get("coverage_gap"):
            coverage_ids.append(r.get("id"))
        updated.append(r)
    return updated, resolved_ids, void_pairs, det_pending, coverage_ids


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
    if OUT.exists():
        try:
            prev_last_run = json.loads(OUT.read_text(encoding="utf-8")).get("last_run")
        except Exception:
            prev_last_run = None

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

    out = {
        "schema": "forecast-settlement-v1",
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
        "rows": updated,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"forecast_settlement.json：open {n_open}／resolved_yes {n_resolved_yes}／resolved_no {n_resolved_no}／"
          f"void {n_void}／detective 待實作 {det_pending}，as_of {today_str}")
    if coverage_warning:
        print(f"⚠ {coverage_warning}")
    if void_pairs:
        print("  void 原因：", dict(Counter(reason for _, reason in void_pairs)))


if __name__ == "__main__":
    main()
