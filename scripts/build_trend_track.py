"""
Trend-Track (TSMOM) paper-track builder — feeds
docs/research/trend-track/track.json.

WHAT THIS IS
------------
A zero-fundamentals, fully mechanical, self-accounting-NAV time-series
momentum (TSMOM) paper track across 9 asset-class proxies — deliberately
the SIBLING line to P10 (docs/research/price-momentum/), not a merge:

  P10 (price-momentum)  = CROSS-SECTIONAL momentum — stocks ranked against
                           EACH OTHER (S&P 500 ∪ NQ100_EXTRAS universe).
  Trend-Track (this file) = TIME-SERIES momentum — each of 9 fixed assets
                           compared only against ITS OWN PAST (12-1 trend).

Mirrors the QGM x RS+VCP "deliberately dual lens" convention already in
the repo (see CLAUDE.md 選股體系治理). Judgment (universe, signal
definition, rebalance cadence, kill conditions) is FROZEN in the design
doc — notes/site-internal/root/_flowmap_forecast_ledger_design_20260901.md
§G6/§G7 — this file only implements it; it must not tune any of it.

It is NOT a convergence surface: it does not feed the DD verdict chain,
does not enter picks/GRP/three-track/cockpit, and must not be cited by
any other session as "asset X is in-trend on Trend-Track" grounds for a
position decision. Zero human intervention at the asset level; the only
human touchpoints are the PREREG review point and kill condition below.

FROZEN SPEC (design doc §G6, 2026-09-01 — LOCKED, do not tune here)
--------------------------------------------------------------------
Universe   : SPY QQQ IWM EFA EEM TLT IEF GLD DBC — 9 fixed asset-class
             proxies (US large-cap / US tech / US small-cap / developed
             ex-US / emerging markets / long-duration UST / intermediate
             UST / gold / broad commodities). If DBC is unobtainable,
             fall back to PDBC and record which symbol was actually used
             in meta; if BOTH are unobtainable, that slot is booked as
             cash and logged to data_gaps (design doc §G6, verbatim).
Signal     : 12-1 momentum — total return from ~12 months ago to ~1 month
             ago (skip the most recent month), the standard literature
             definition. Implemented with the SAME index convention as
             P10's L12 line (scripts/build_price_momentum.py):
                 c = that asset's dropna'd adjusted-close series
                 ret_12_1 = c.iloc[-22] / c.iloc[-253] - 1
             (c.iloc[-253] ~ 12 months ago, c.iloc[-22] ~ 1 month ago,
             skipping the most recent 21 trading days — equivalent to the
             design doc's "t-252 to t-21" phrasing). >=253 closes required
             per asset, else that asset is data-insufficient this run
             (falls back to a cash slot, logged to data_gaps).
Rule       : ret_12_1 > 0 -> hold that asset; else that slot is booked as
             CASH (0% return) for this rebalance period. No cross-asset
             ranking, no buffer band, no backfilling one slot's cash into
             another asset's weight — each of the 9 slots is dedicated to
             ONE fixed asset for the life of the track.
Weighting  : Equal weight 1/9 across all 9 slots, regardless of how many
             assets are currently in-trend. A non-invested slot's NAV
             share simply sits in cash; it is never redistributed to the
             invested slots.
Rebalance  : Monthly, on the first trading day of the month (operationally:
             the first weekly-cadence run whose calendar month differs
             from last_rebalance_month — same idiom as P10/shadow's
             last_rebalance_month convention). On rebalance the WHOLE book
             resets to equal weight off that day's mark-to-market NAV.
NAV        : Inception = 2026-09-01, NAV = 100.0 for the trend line, the
             9-asset equal-weight buy-and-hold benchmark, AND nav_spy (all
             three normalized to 100 the same day). Every run marks to
             market. Same-day reruns are idempotent (nav_series /
             rebalance_history entries for an existing date are
             overwritten in place, never duplicated).
Benchmarks : (1) 9-asset equal-weight buy-and-hold — bought once at
             inception, weights drift with relative performance, NEVER
             rebalanced. (2) SPY, tracked standalone.
Kill       : 24 months out, if Sharpe AND Max DD are BOTH not better than
             the 9-asset equal-weight buy-and-hold -> close the line. No
             re-tuning during the window. Paper only, never connects to a
             live book.

Implementation choices NOT dictated verbatim by the design doc (flagged
here for holder review, not a judgment-layer change):
  - MIN_SUFFICIENT_ASSETS fail-safe floor (7 of 9) — the design doc only
    specifies the DBC->PDBC->cash fallback for the commodity slot; this
    file additionally aborts the whole build (mirrors P10/flowmap
    fail-safe culture) if catastrophic data loss leaves fewer than 7 of
    the 9 fixed slots computable, rather than silently limping on a
    near-empty universe.
  - Both DBC and PDBC are cached and re-evaluated every run (whichever
    currently has >=253 closes wins that run) rather than being locked in
    permanently at inception — simpler and self-healing if one symbol's
    data feed recovers; flagged as a design nuance since both trackers
    are highly correlated broad-commodity funds and a mid-track symbol
    switch is a low-probability edge case in practice.

FAIL-SAFE (mirrors scripts/build_price_momentum.py / build_flowmap.py)
------------------------------------------------------------------------
Any of the following -> print a warning, exit 0, leave track.json
completely untouched:
  - SPY price series empty (breaks both the core signal and the SPY
    benchmark).
  - Fewer than MIN_SUFFICIENT_ASSETS (7) of the 9 canonical slots clear
    the >=253-close data-sufficiency floor.
  - Any uncaught exception anywhere in the build (top-level try/except
    around main()).

Price cache (data/trend_track_prices.json): incremental, yfinance->stooq
fallback, zero-churn writes — mirrors data/flowmap_prices.json exactly
(scripts/build_flowmap.py's build_price_cache).

Runs in the weekly-market-update GitHub Actions workflow, same step
family as build_price_momentum.py.
"""

import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

import requests

ROOT = Path(__file__).resolve().parent.parent
PRICE_CACHE = ROOT / 'data' / 'trend_track_prices.json'
TRACK_JSON = ROOT / 'docs' / 'research' / 'trend-track' / 'track.json'

SCHEMA = 'trend-track-v1'

# ── frozen thresholds (PREREG'd 2026-09-01, design doc §G6 — LOCKED) ──
CORE_ROLES = [
    ('SPY', '美股大盤（S&P 500）'),
    ('QQQ', '美股科技（Nasdaq 100）'),
    ('IWM', '美股小型股（Russell 2000）'),
    ('EFA', '成熟市場（歐澳遠東）'),
    ('EEM', '新興市場'),
    ('TLT', '長天期美債（20 年以上）'),
    ('IEF', '中天期美債（7–10 年）'),
    ('GLD', '黃金'),
]
CORE_SYMBOLS = [t for t, _ in CORE_ROLES]
COMMODITY_ROLE = '大宗商品'
COMMODITY_PRIMARY = 'DBC'
COMMODITY_FALLBACK = 'PDBC'
FETCH_UNIVERSE = CORE_SYMBOLS + [COMMODITY_PRIMARY, COMMODITY_FALLBACK]  # 10 tickers cached
N_ASSETS = 9  # canonical slot count (8 core + 1 commodity slot)

MIN_CLOSES = 253             # per-asset data-sufficiency floor for the 12-1 signal (§G6)
FAR_IDX = -253                # ~12 months ago
NEAR_IDX = -22                 # ~1 month ago (skip most recent 21 trading days)
ROLLING_TRADING_DAYS = 400 + 20  # "~400 交易日足以算 12-1" + small buffer for weekly top-ups

MIN_SUFFICIENT_ASSETS = 7    # implementation fail-safe floor (see docstring), NOT literal §G6 text

INCEPTION_DATE = '2026-09-01'

PREREG = {
    "title": "趨勢追蹤 paper track（TSMOM）— v0（PREREG，2026-09-01 凍結）",
    "frozen_date": "2026-09-01",
    "family_distinction": (
        "與 P10（純價格動能 paper track，docs/research/price-momentum/）刻意雙軌，"
        "比照站內 QGM×RS+VCP screener 雙鏡頭慣例，不合併：P10 是橫斷面動能——"
        "S&P 500∪NQ100_EXTRAS 一個大池子的股票彼此比誰更強；本線是時間序列動能"
        "（TSMOM）——固定 9 檔資產，每一檔只跟自己的過去比，趨勢向上就持有、"
        "向下就退到現金，這是有百年跨資產證據的規則家族（Moskowitz/Ooi/Pedersen "
        "2012《Time Series Momentum》一類文獻）。"
    ),
    "positioning": (
        "本線是零基本面成分、全機械、自帶 NAV 的跨資產時間序列動能 paper track。"
        "它不是收斂面：不回饋 DD 裁決鏈、不進 picks/GRP/三軌/cockpit 任何清單，"
        "不得被其他 session 引用為「某資產在趨勢追蹤上」的選股或擇時依據。資產層"
        "零人為干預；唯一人類接觸點是本 prereg 的正式評審點與 kill condition。"
    ),
    "universe_and_data": {
        "universe": (
            "SPY、QQQ、IWM、EFA、EEM、TLT、IEF、GLD、DBC 共 9 檔固定資產類別代理"
            "（美股大盤／美股科技／美股小型股／成熟市場〔歐澳遠東〕／新興市場／"
            "長天期美債／中天期美債／黃金／大宗商品）。DBC 若當期資料不可得"
            "（<253 筆收盤），改試 PDBC，並在 track.json 的 commodity_symbol_used "
            "欄位註記當期實際採用的代理；若兩者皆不可得，該 slot 以現金記帳"
            "（0% 報酬）並記入 data_gaps，不捏造數字。"
        ),
        "prices": (
            "yfinance 日線收盤（auto_adjust=True），yfinance 失敗 fallback stooq；"
            "自建快取 data/trend_track_prices.json，incremental 增量合併、"
            "rolling ~400 個交易日（signal 只需 253 筆，多留緩衝供週度增量與 "
            "12-1 視窗滑動）。"
        ),
        "sufficiency_floor": (
            "個股（資產）資料充足門檻：dropna 後 close 序列長度 ≥253，否則該資產"
            "本期排除、記入 data_gaps，該 slot 以現金記帳。"
        ),
    },
    "signal": {
        "definition": (
            "12-1 動能：t−252 至 t−21 交易日總報酬（12 個月前至 1 個月前，跳過"
            "最近 1 個月），與 P10 L12 慢線同一套標準定義、同一套 index 慣例"
            "（c.iloc[-22] / c.iloc[-253] − 1，-253 約 12 個月前、-22 約 1 個月前，"
            "跳過最近 21 個交易日）。"
        ),
        "ret_12_1": "ret_12_1 = c.iloc[-22] / c.iloc[-253] − 1。",
        "rule": ">0 → 該資產本期持有；否則該 slot 記現金（0% 報酬）。無其他否決條件。",
    },
    "weighting_and_rebalance": {
        "equal_weight": (
            "等權 1/9——無論本期幾檔在趨勢中，未持有的 slot 就是現金，其權重"
            "不會被轉移給其他持有中的資產（不是「在趨勢的資產瓜分全部曝險」，"
            "是「固定 9 席，每席各自決定持有或現金」）。"
        ),
        "monthly_rebalance": (
            "月度首交易日換倉（判定＝當月第一個有價格的交易日，操作上＝本次"
            "執行的日曆月份 ≠ 上次 rebalance 月份，與 P10/shadow 的 "
            "last_rebalance_month 慣例一致）：重新計算 9 檔各自訊號，整組重置"
            "等權——當日 mark-to-market NAV／9 換算每個持有 slot 的 units，"
            "現金 slot 對應比例留現金。"
        ),
        "idempotency": "同日重跑冪等：nav_series 與 rebalance_history 同日期覆蓋，不重複 append。",
    },
    "nav_accounting": {
        "inception": (
            "Inception：2026-09-01，趨勢線 NAV=100.0；9 檔等權 buy-and-hold 對照組"
            "同日 NAV=100.0；nav_spy 同日以 SPY 收盤 normalize 至 100。"
        ),
        "mark_to_market": "每次執行（週更）mark to market：NAV = 現金 + Σ units × 該資產最新收盤。",
    },
    "benchmarks": {
        "buy_and_hold": (
            "9 檔等權 buy-and-hold：inception 當日等權買入（每檔 NAV/9），此後"
            "永不再平衡，權重隨相對表現自然漂移——與趨勢線的「每月機械換倉、"
            "訊號決定持有或現金」對照，回答「機械擇時是否比單純持有更好」。"
        ),
        "spy": "SPY 單一標的，同日 inception=100，作為傳統大盤基準對照。",
    },
    "kill_conditions": {
        "evaluation_point": "正式評估點 2028-09-01（24 個月）；期中讀數可看、不具裁決力。",
        "kill_1": (
            "24 個月後 Sharpe 與 Max DD 皆未優於 9 檔等權 buy-and-hold → 收線；"
            "期間不調參、不重調、不復活。"
        ),
        "paper_only": "Paper only，永不連實倉。",
    },
    "disclosure": (
        "誠實標注：paper track、無交易成本、無滑價、機械式、非投資建議。不是收斂面，"
        "不進任何裁決鏈（picks/GRP/三軌/cockpit）。資產層零人為干預；唯一人類接觸點"
        "是本 prereg 的正式評審點與 kill condition。"
    ),
}


class FailSafeAbort(Exception):
    """Raised for any of the PREREG'd fail-safe conditions — caught in
    main() to print a warning and exit 0 without touching track.json."""


def warn(msg):
    print(f"[trend-track][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[trend-track] {msg}")


def month_of(date_str):
    return date_str[:7]


# ═══════════════════════════════════════════════════════════════════════
# Zero-churn IO for the price cache (mirrors build_flowmap.py exactly)
# ═══════════════════════════════════════════════════════════════════════

def _serialize(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def _strip_volatile(obj, keys):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def load_json(path, default=None):
    if not path.exists():
        return default
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        warn(f"could not read {path.name}: {e}")
        return default


def write_json_if_changed(path, obj, volatile=('built_at',)):
    vset = set(volatile)
    if path.exists():
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(_serialize(obj))
    return True


def _http_get(url, timeout=45):
    try:
        r = requests.get(url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 trend-track'})
        r.raise_for_status()
        return r.content
    except Exception:
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 trend-track'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()


# ═══════════════════════════════════════════════════════════════════════
# Price cache（daily close, yfinance -> stooq fallback, incremental）—
# mirrors data/flowmap_prices.json / build_flowmap.py's build_price_cache
# ═══════════════════════════════════════════════════════════════════════

def _yf_daily(tickers, period='2y'):
    """Batch daily close download -> {ticker: [(date, close), ...]}."""
    out = {}
    if not tickers:
        return out
    df = yf.download(tickers, period=period, interval='1d', auto_adjust=True,
                      group_by='ticker', threads=True, progress=False)
    is_multi = hasattr(df.columns, 'nlevels') and df.columns.nlevels > 1
    for tk in tickers:
        try:
            sub = df[tk] if is_multi else df
            close = sub['Close']
            rows = []
            for idx, val in close.items():
                try:
                    c = float(val)
                except (TypeError, ValueError):
                    continue
                if c != c:  # NaN
                    continue
                rows.append((idx.date().isoformat(), round(c, 4)))
            if rows:
                out[tk] = rows
        except (KeyError, AttributeError, ValueError, TypeError):
            continue
    return out


def _stooq_daily(ticker):
    sym = ticker.lower()
    if '.' not in sym:
        sym = sym + '.us'
    url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
    try:
        raw = _http_get(url, timeout=30).decode('utf-8', 'replace')
    except Exception:
        return None
    lines = raw.strip().splitlines()
    if len(lines) < 2 or not lines[0].lower().startswith('date'):
        return None
    rows = []
    for ln in lines[1:]:
        parts = ln.split(',')
        if len(parts) < 5:
            continue
        try:
            rows.append((parts[0], round(float(parts[4]), 4)))
        except ValueError:
            continue
    return rows or None


def build_price_cache(skip_fetch=False):
    """Incrementally refresh data/trend_track_prices.json. Returns
    {symbol: [(date, close), ...]} for FETCH_UNIVERSE (10 tickers: 8 core
    + DBC + PDBC, both commodity candidates cached every run)."""
    cache = load_json(PRICE_CACHE, {'meta': {}, 'series': {}})
    series = cache.setdefault('series', {})
    fetched = {}
    if not skip_fetch:
        missing = [t for t in FETCH_UNIVERSE if not series.get(t)]
        existing = [t for t in FETCH_UNIVERSE if series.get(t)]
        for label, batch, period in (('bootstrap', missing, '2y'), ('topup', existing, '10d')):
            if not batch:
                continue
            got = None
            for attempt in range(3):
                try:
                    got = _yf_daily(batch, period=period)
                    if got:
                        break
                except Exception as e:
                    warn(f"yfinance {label} attempt {attempt+1} failed: {e}")
            if got:
                fetched.update(got)
            info(f"prices {label}: requested {len(batch)}, got "
                 f"{sum(1 for t in batch if t in fetched)}")
        for t in FETCH_UNIVERSE:
            if t in fetched or series.get(t):
                continue
            s = _stooq_daily(t)
            if s:
                fetched[t] = s
                info(f"prices stooq fallback: {t} ({len(s)} days)")

    for t, rows in fetched.items():
        merged = {d: c for d, c in series.get(t, [])}
        for d, c in rows:
            merged[d] = c
        merged_sorted = sorted(merged.items())
        if len(merged_sorted) > ROLLING_TRADING_DAYS:
            merged_sorted = merged_sorted[-ROLLING_TRADING_DAYS:]
        series[t] = merged_sorted

    cache['meta'] = {
        'built_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'symbols': FETCH_UNIVERSE,
        'note': ('daily close cache for trend-track (TSMOM) 12-1 momentum signal — '
                 '9 canonical slots (SPY QQQ IWM EFA EEM TLT IEF GLD + commodity); '
                 'DBC and PDBC both cached so the commodity slot can fall back per '
                 'PREREG (design doc §G6); yfinance->stooq fallback; incremental, '
                 'rolling ~400 trading days.'),
    }
    wrote = write_json_if_changed(PRICE_CACHE, cache)
    n = {t: len(series.get(t, [])) for t in FETCH_UNIVERSE}
    info(f"price cache: {n}, {'written' if wrote else 'no change'}")
    return {t: [(d, c) for d, c in series.get(t, [])] for t in FETCH_UNIVERSE}


# ═══════════════════════════════════════════════════════════════════════
# Signal + commodity-slot resolution
# ═══════════════════════════════════════════════════════════════════════

def resolve_commodity(series_map):
    """DBC preferred; PDBC fallback if DBC lacks >=MIN_CLOSES this run;
    None (both insufficient) if neither qualifies (design doc §G6)."""
    for sym in (COMMODITY_PRIMARY, COMMODITY_FALLBACK):
        rows = series_map.get(sym) or []
        if len(rows) >= MIN_CLOSES:
            return sym, rows
    return None, []


def compute_signal(rows):
    """rows: [(date, close), ...] ascending. Returns
    {ret_12_1, in_trend} or None if data-insufficient (<MIN_CLOSES) or the
    far anchor is degenerate (0/NaN close, defensive only — not a §G6
    veto, purely a divide-by-zero guard)."""
    if not rows or len(rows) < MIN_CLOSES:
        return None
    closes = [c for _, c in rows]
    far = closes[FAR_IDX]
    near = closes[NEAR_IDX]
    if not far:
        return None
    ret_12_1 = near / far - 1.0
    return {'ret_12_1': float(ret_12_1), 'in_trend': bool(ret_12_1 > 0)}


# ═══════════════════════════════════════════════════════════════════════
# NAV bookkeeping — trend line
# ═══════════════════════════════════════════════════════════════════════

def do_rebalance(nav, assets_def, signals, price_now, as_of):
    """Equal-weight reset across the 9 fixed slots: in-trend assets get
    NAV/9 converted to units at today's close; everything else (not
    in-trend, data-insufficient, or commodity slot unresolved) is cash.
    Returns (new_holdings: {ticker: {...}}, cash, cash_slots)."""
    seat_value = nav / N_ASSETS
    new_holdings = {}
    cash_slots = 0
    for t, _role in assets_def:
        if t is None:
            cash_slots += 1
            continue
        sig = signals.get(t)
        if sig is None or not sig['in_trend']:
            cash_slots += 1
            continue
        p = price_now.get(t)
        if p is None or p <= 0:
            cash_slots += 1
            continue
        new_holdings[t] = {
            'ticker': t, 'entry_date': as_of, 'entry_price': round(float(p), 2),
            'units': seat_value / p, 'last_price': float(p),
        }
    cash = nav * cash_slots / N_ASSETS
    return new_holdings, cash, cash_slots


def mark_to_market(cash, holdings, price_now):
    """NAV = cash + sum(units * latest close); stale carry-forward for a
    ticker missing this run (mirrors P10's mark_to_market)."""
    total = float(cash)
    stale = []
    for t, h in holdings.items():
        p = price_now.get(t)
        if p is None:
            p = h.get('last_price', h['entry_price'])
            stale.append(t)
        else:
            h['last_price'] = float(p)
        total += h['units'] * p
    return total, stale


def build_inception_trend(assets_def, signals, price_now, as_of):
    nav = 100.0
    holdings, cash, cash_slots = do_rebalance(nav, assets_def, signals, price_now, as_of)
    entered = sorted(holdings.keys())
    rebalance_history = [{
        'date': as_of, 'event': 'inception', 'entered': entered, 'exited': [],
        'cash_slots': cash_slots,
        'holdings': [{'ticker': t, 'units': round(h['units'], 6), 'entry_price': h['entry_price']}
                     for t, h in sorted(holdings.items())],
    }]
    trend_state = {'cash': cash, 'holdings': holdings, 'rebalance_history': rebalance_history}
    return trend_state, nav


def update_trend(assets_def, signals, price_now, as_of, is_new_month, trend_state, data_gaps_out):
    cash = trend_state['cash']
    holdings = trend_state['holdings']

    if is_new_month:
        nav_pre, stale = mark_to_market(cash, holdings, price_now)
        if stale:
            info(f"    ! stale price carried forward pre-rebalance for {stale}")
            data_gaps_out.append({'date': as_of, 'reason': 'stale price pre-rebalance', 'tickers': stale})
        new_holdings, new_cash, cash_slots = do_rebalance(nav_pre, assets_def, signals, price_now, as_of)
        prior = set(holdings.keys())
        now_ = set(new_holdings.keys())
        entered = sorted(now_ - prior)
        exited = sorted(prior - now_)
        entry = {
            'date': as_of, 'event': 'rebalance', 'entered': entered, 'exited': exited,
            'cash_slots': cash_slots,
            'holdings': [{'ticker': t, 'units': round(h['units'], 6), 'entry_price': h['entry_price']}
                         for t, h in sorted(new_holdings.items())],
        }
        if trend_state['rebalance_history'] and trend_state['rebalance_history'][-1]['date'] == as_of:
            trend_state['rebalance_history'][-1] = entry
        else:
            trend_state['rebalance_history'].append(entry)
        trend_state['holdings'] = new_holdings
        trend_state['cash'] = new_cash
        nav_now = nav_pre  # equal-weight reset conserves total NAV, no transaction cost
        event = f"月度機械換倉：進場 {entered or ['無']}，出場 {exited or ['無']}，現金席位 {cash_slots}。"
    else:
        nav_now, stale = mark_to_market(cash, holdings, price_now)
        if stale:
            info(f"    ! stale price carried forward for {stale}")
            data_gaps_out.append({'date': as_of, 'reason': 'stale price', 'tickers': stale})
        trend_state['holdings'] = holdings
        trend_state['cash'] = cash
        event = None

    return nav_now, event


# ═══════════════════════════════════════════════════════════════════════
# NAV bookkeeping — 9-asset equal-weight buy-and-hold benchmark (never
# rebalances; bought once at inception with whatever priced that day)
# ═══════════════════════════════════════════════════════════════════════

def build_inception_bh(assets_def, price_now):
    nav = 100.0
    units = {}
    missing = []
    for t, _role in assets_def:
        if t is None or price_now.get(t) is None:
            missing.append(t or f'{COMMODITY_PRIMARY}/{COMMODITY_FALLBACK}')
            continue
        units[t] = (nav / N_ASSETS) / price_now[t]
    cash = nav * len(missing) / N_ASSETS
    return {'units': units, 'cash': cash, 'last_price': dict(price_now), 'missing_at_inception': missing}, nav


def mark_to_market_bh(bh_state, price_now):
    total = float(bh_state.get('cash', 0.0))
    last_price = bh_state.setdefault('last_price', {})
    for t, u in bh_state.get('units', {}).items():
        p = price_now.get(t)
        if p is None:
            p = last_price.get(t)
        else:
            last_price[t] = p
        if p is not None:
            total += u * p
    return total


# ═══════════════════════════════════════════════════════════════════════
# Main build
# ═══════════════════════════════════════════════════════════════════════

def load_state():
    if TRACK_JSON.exists():
        return json.loads(TRACK_JSON.read_text(encoding='utf-8'))
    return None


def build():
    now = datetime.now(timezone.utc)
    as_of = now.strftime('%Y-%m-%d')
    print(f"=== Trend-Track (TSMOM) Build: {as_of} ===")

    price_series = build_price_cache(skip_fetch=False)

    spy_rows = price_series.get('SPY', [])
    if not spy_rows:
        raise FailSafeAbort("SPY price series empty — cannot build core signal or SPY benchmark")
    spy_close = float(spy_rows[-1][1])

    commodity_symbol, _commodity_rows = resolve_commodity(price_series)
    data_gaps = []
    if commodity_symbol is None:
        warn("commodity slot (DBC/PDBC) both unavailable/insufficient this run — booked as cash")
        data_gaps.append({'date': as_of, 'reason': 'commodity slot unavailable (DBC+PDBC both insufficient)',
                           'tickers': [COMMODITY_PRIMARY, COMMODITY_FALLBACK]})
    elif commodity_symbol == COMMODITY_FALLBACK:
        warn(f"commodity slot fell back to {COMMODITY_FALLBACK} ({COMMODITY_PRIMARY} insufficient this run)")
        data_gaps.append({'date': as_of, 'reason': f'commodity fallback to {COMMODITY_FALLBACK}',
                           'tickers': [COMMODITY_PRIMARY]})

    assets_def = list(CORE_ROLES) + [(commodity_symbol, COMMODITY_ROLE)]

    sufficient = [t for t, _ in assets_def if t and len(price_series.get(t, [])) >= MIN_CLOSES]
    info(f"data-sufficient assets (>= {MIN_CLOSES} closes): {sufficient} ({len(sufficient)}/9)")
    if len(sufficient) < MIN_SUFFICIENT_ASSETS:
        raise FailSafeAbort(f"only {len(sufficient)} of 9 assets have >= {MIN_CLOSES} closes "
                             f"(floor {MIN_SUFFICIENT_ASSETS})")

    price_now = {}
    signals = {}
    for t, _role in assets_def:
        if t is None:
            continue
        rows = price_series.get(t, [])
        if rows:
            price_now[t] = float(rows[-1][1])
        sig = compute_signal(rows)
        if sig is not None:
            signals[t] = sig
        elif rows:
            data_gaps.append({'date': as_of, 'reason': 'insufficient closes for 12-1 signal', 'tickers': [t]})

    for t in sorted(signals):
        s = signals[t]
        info(f"    {t}: ret_12_1={s['ret_12_1']*100:+.2f}%  in_trend={s['in_trend']}")

    state = load_state()

    if state is None:
        info("no existing track.json — building inception")
        trend_state, nav_trend = build_inception_trend(assets_def, signals, price_now, as_of)
        bh_state, nav_bh = build_inception_bh(assets_def, price_now)
        state = {
            'schema': SCHEMA,
            'prereg': PREREG,
            'as_of': as_of,
            'inception_date': as_of,
            'spy_close_inception': round(spy_close, 2),
            'last_rebalance_month': month_of(as_of),
            'commodity_symbol_used': commodity_symbol,
            'nav_series': [],
            'trend': trend_state,
            'benchmark_bh': bh_state,
            'data_gaps': [],
            'changelog': [{
                'date': as_of,
                'event': (f"趨勢追蹤 paper track（TSMOM）PREREG 凍結（{as_of}），inception。"
                          f"當期持有：{sorted(trend_state['holdings'].keys()) or ['無（全現金）']}。"),
            }],
        }
    else:
        is_new_month = month_of(as_of) != state.get('last_rebalance_month')
        nav_trend, event = update_trend(assets_def, signals, price_now, as_of, is_new_month,
                                         state['trend'], data_gaps)
        nav_bh = mark_to_market_bh(state['benchmark_bh'], price_now)
        if is_new_month:
            state['last_rebalance_month'] = month_of(as_of)
            if event:
                state['changelog'].append({'date': as_of, 'event': event})
        if commodity_symbol:
            state['commodity_symbol_used'] = commodity_symbol

    nav_spy = round(100.0 * spy_close / state['spy_close_inception'], 2)
    nav_entry = {'date': as_of, 'nav_trend': round(nav_trend, 2), 'nav_bh': round(nav_bh, 2),
                 'nav_spy': nav_spy, 'spy_close': round(spy_close, 2)}
    if state['nav_series'] and state['nav_series'][-1]['date'] == as_of:
        state['nav_series'][-1] = nav_entry
    else:
        state['nav_series'].append(nav_entry)

    # ── current signal/holdings table (refreshed every run; composition
    #    itself only changes at monthly rebalance, mirrors P10) ──
    held_tickers = set(state['trend']['holdings'].keys())
    assets_out = []
    for t, role in assets_def:
        sig = signals.get(t) if t else None
        h = state['trend']['holdings'].get(t) if t else None
        assets_out.append({
            'ticker': t, 'role': role,
            'price': round(price_now[t], 2) if t and t in price_now else None,
            'ret_12_1_pct': round(sig['ret_12_1'] * 100, 2) if sig else None,
            'signal_in_trend': bool(sig['in_trend']) if sig else False,
            'data_sufficient': sig is not None,
            'held': t in held_tickers if t else False,
            'entry_date': h['entry_date'] if h else None,
            'entry_price': h['entry_price'] if h else None,
            'last_price': round(h['last_price'], 2) if h else None,
            'units': round(h['units'], 6) if h else None,
        })
    state['assets'] = assets_out

    state['as_of'] = as_of
    state['prereg'] = PREREG  # numbers are frozen; keep the verbatim block in sync regardless
    state['data_gaps'] = (state.get('data_gaps') or []) + data_gaps

    print(f"    nav_trend={nav_trend:.2f}  nav_bh={nav_bh:.2f}  nav_spy={nav_spy:.2f}")
    print(f"    held: {sorted(held_tickers)}  cash={state['trend']['cash']:.2f}")
    print(f"    commodity_symbol_used={state.get('commodity_symbol_used')}")

    return state


def main():
    try:
        state = build()
    except FailSafeAbort as e:
        print(f"  ✗ fail-safe triggered: {e} — track.json left unchanged")
        sys.exit(0)
    except Exception as e:
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — track.json left unchanged")
        sys.exit(0)

    TRACK_JSON.parent.mkdir(parents=True, exist_ok=True)
    TRACK_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {TRACK_JSON.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
