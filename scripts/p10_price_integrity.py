"""P10 價格動能（美股 build_price_momentum.py、台股 build_price_momentum_tw.py）共用的收盤價檢查。

2026-11-03 起。起因：11-02 台股每日排程抓價時，Yahoo 只給了 0050 的 11-02 收盤，
19 檔持股那天都是空值；舊程式「取該日或之前最近一筆」默默拿 10-30 的價格，兩線淨值
跟 10-30 一模一樣（L12 寫 100.78、實際 99.77；L6 寫 105.61、實際 103.19），只有完全
抓不到的 2383 被記成舊價。

規則（兩支程式一致，純資料處理，不動 PREREG 的任何數字或選股規則）：
1. 每一列淨值只用「該日」的收盤。持股缺當天收盤時，只重抓缺的那幾檔，最多再抓
   len(REFETCH_BACKOFF_SECONDS) 次。
2. 還是缺：用之前最近一筆收盤暫代，該列寫 provisional＝[缺價代號]，頁面標「暫估」。
3. 自上次換股之後的每一列都用目前的持股、股數、現金計算（兩次換股之間持股不變），
   所以每次執行都把這一段整段重算：暫估列等資料出來就自動改成正式值，之前寫錯的列
   也會被改正，改了哪一列、改多少都印在 log。已確認的列不會被暫估值蓋掉。
4. 重算用不含股息還原的收盤（auto_adjust=False 的 Close，只做拆股／減資還原），維持
   價格報酬口徑；當天那一根兩種口徑相同，所以跟完整建置寫的數字一致。
5. 換股那天持股或要買進的股票缺當天收盤 → 不換股（FailSafeAbort），由排程重試。
"""
from __future__ import annotations

import random
import time

import pandas as pd
import yfinance as yf

REFETCH_BACKOFF_SECONDS = (45.0, 120.0)  # 缺價時再抓的等待秒數（第 2、3 次）
PROVISIONAL_ESCALATE_ROWS = 2            # 暫估列落後最新一列超過這麼多個交易日 → 結束碼 EXIT_DATA_WARNING
EXIT_ABORT = 2                           # 安全機制觸發，track.json 沒寫（排程可重試）
EXIT_DATA_WARNING = 3                    # track.json 已寫，但有暫估列太久沒補上（需要人看）
LEGACY_WEEKLY_ROWS_BEFORE = '2026-10-30'  # 這天以前的週列標執行日（週六），之後一律標收盤日


def day(ts) -> str:
    return ts.strftime('%Y-%m-%d')


def close_on(c, date_str):
    """收盤恰好在 date_str 那天的價格，沒有就 None（不往前找）。"""
    if c is None or not len(c):
        return None
    hit = c[c.index.strftime('%Y-%m-%d') == date_str]
    return float(hit.iloc[-1]) if len(hit) else None


def close_on_or_before(c, date_str):
    if c is None or not len(c):
        return None
    c = c[c.index.strftime('%Y-%m-%d') <= date_str]
    return float(c.iloc[-1]) if len(c) else None


def _closes_from(px, tickers):
    out = {}
    for t in tickers:
        try:
            c = px[t]['Close'].dropna()
        except Exception:
            c = None
        out[t] = c if c is not None and len(c) else None
    return out


def missing_exact(closes, tickers, dates):
    """{ticker: [缺收盤的日期]}，只列有缺的。"""
    miss = {}
    for t in tickers:
        c = closes.get(t)
        have = set(c.index.strftime('%Y-%m-%d')) if c is not None else set()
        lack = [d for d in dates if d not in have]
        if lack:
            miss[t] = lack
    return miss


def ensure_exact(closes, tickers, dates, period, auto_adjust, label):
    """缺當天收盤的代號只重抓那幾檔；抓到的日期併進原序列（新值優先）。回傳更新後的 closes。"""
    miss = missing_exact(closes, tickers, dates)
    for attempt, wait in enumerate(REFETCH_BACKOFF_SECONDS, start=2):
        if not miss:
            break
        print(f"    ! [{label}] 缺當天收盤：{ {t: v[-3:] for t, v in miss.items()} }；{wait:.0f} 秒後重抓（第 {attempt} 次）")
        time.sleep(wait + random.uniform(0, 5))
        try:
            px = yf.download(sorted(miss), period=period, interval='1d', auto_adjust=auto_adjust,
                             group_by='ticker', progress=False, threads=True)
        except Exception as e:
            print(f"    ! [{label}] 重抓失敗（{type(e).__name__}: {e}）")
            continue
        if isinstance(px.columns, pd.MultiIndex):
            fresh = _closes_from(px, sorted(miss))
        else:  # 單一代號且 yfinance 回單層欄位
            c = px['Close'].dropna() if 'Close' in px else None
            fresh = {next(iter(miss)): c}
        for t, c in fresh.items():
            if c is None or not len(c):
                continue
            old = closes.get(t)
            closes[t] = c if old is None else c.combine_first(old)
        miss = missing_exact(closes, tickers, dates)
    if miss:
        print(f"    ! [{label}] 重抓後仍缺當天收盤：{ {t: v[-3:] for t, v in miss.items()} }")
    return closes


def window_start(state, line_keys):
    """上次換股的日期（各線最後一筆 rebalance_history 的最大值）；之後的列都用目前持股計算。"""
    dates = [state['lines'][lk]['rebalance_history'][-1]['date']
             for lk in line_keys if state['lines'][lk].get('rebalance_history')]
    return max(dates) if dates else state['inception_date']


def trading_days(px, bench_ticker, bench):
    """基準有收盤、而且成交量不是 0 的日子。Yahoo 台股休市日（例：2026-10-23 颱風）會補一根
    成交量 0 的平盤，那天不算交易日。"""
    try:
        vol = px[bench_ticker]['Volume']
    except Exception:
        vol = None
    out = []
    for ts in bench.index:
        v = vol.get(ts) if vol is not None else None
        if v is None or v != v or v > 0:
            out.append(day(ts))
    return out


def plan_dates(state, trading, start, upto):
    """[(價格日, 寫入的列日期)]，價格日在 start 之後、upto 以前。

    2026-10-30 以前的週列標的是執行日（通常是週六），代表前一個交易日的收盤；
    那個交易日的值寫回週六那一列，不另開新列，序列結構維持原樣。"""
    tset = set(trading)
    alias = {}
    for r in state['nav_series']:
        d = r['date']
        # 只認 2026-10-30 以前、落在週末的舊週列；比最新收盤還晚的列（Yahoo 晚出資料時）不能拿來對應
        if (d > start and d < LEGACY_WEEKLY_ROWS_BEFORE and d not in tset
                and pd.Timestamp(d).weekday() >= 5):
            prev = [t for t in trading if t < d]
            if prev and prev[-1] > start:
                alias[prev[-1]] = d
    return [(d, alias.get(d, d)) for d in trading if start < d <= upto]


def mark_rows(state, line_keys, closes, bench, dates, keys):
    """用目前的持股、股數、現金，算每一天的淨值列。dates＝plan_dates() 的 [(價格日, 列日期)]。

    keys＝(nav 基準欄, 基準收盤欄, 基準成立日收盤欄)，美股 ('nav_spy','spy_close','spy_close_inception')、
    台股 ('nav_bench','bench_close','bench_close_inception')。缺當天收盤的持股用之前最近一筆暫代，
    列上寫 provisional。"""
    nav_key, close_key, inc_key = keys
    bench_by_day = {day(ts): float(v) for ts, v in bench.items()}
    rows = []
    for d, row_date in dates:
        entry = {'date': row_date}
        prov = set()
        for lk in line_keys:
            ls = state['lines'][lk]
            total = float(ls['cash'])
            for h in ls['holdings']:
                c = closes.get(h['ticker'])
                p = close_on(c, d)
                if p is None:
                    prov.add(h['ticker'])
                    p = close_on_or_before(c, d)
                    if p is None:
                        p = h.get('last_price', h['entry_price'])
                total += h['units'] * p
            entry[f'nav_{lk}'] = round(total, 2)
        b = bench_by_day[d]
        entry[nav_key] = round(100.0 * b / state[inc_key], 2)
        entry[close_key] = round(b, 2)
        if prov:
            entry['provisional'] = sorted(prov)
        rows.append(entry)
    return rows


def merge_rows(state, rows, line_keys, nav_key):
    """把重算的列寫回 nav_series（同日覆蓋，保留 backfill 等其他欄位），印出有改到的數字。回傳改動清單。"""
    by_date = {r['date']: r for r in state['nav_series']}
    changes = []
    for new in rows:
        old = by_date.get(new['date'])
        if old is not None and not old.get('provisional') and new.get('provisional'):
            # 已確認的數字不拿這次缺價的暫估值蓋掉（Yahoo 偶爾少給舊資料）
            print(f"    · 淨值列 {new['date']} 這次缺 {new['provisional']} 的收盤，保留原值")
            continue
        merged = dict(old) if old else {}
        merged.pop('provisional', None)
        merged.update(new)
        if old is None:
            changes.append(f"{new['date']} 新增")
        else:
            diffs = [f"{k} {old.get(k)}→{new[k]}" for k in [f'nav_{lk}' for lk in line_keys] + [nav_key]
                     if old.get(k) != new[k]]
            if old.get('provisional') != new.get('provisional'):
                diffs.append(f"暫估 {old.get('provisional') or '無'}→{new.get('provisional') or '無'}")
            if diffs:
                changes.append(f"{new['date']} " + "、".join(diffs))
        by_date[new['date']] = merged
    state['nav_series'] = sorted(by_date.values(), key=lambda r: r['date'])
    for c in changes:
        print(f"    · 淨值列 {c}")
    return changes


def provisional_gaps(rows, label_reason):
    """暫估列轉成 data_gaps 項目（只給最新一列，避免每天重複記同一件事）。"""
    if not rows or not rows[-1].get('provisional'):
        return []
    r = rows[-1]
    return [{'date': r['date'], 'line': 'all', 'reason': label_reason, 'tickers': r['provisional']}]


def add_gaps(state, gaps):
    existing = state.get('data_gaps') or []
    for g in gaps:
        if g not in existing:
            existing.append(g)
    state['data_gaps'] = existing


def stale_provisional(state, bench_dates, start):
    """自上次換股後、落後最新交易日超過 PROVISIONAL_ESCALATE_ROWS 列還是暫估的日期。"""
    recent = [d for d in bench_dates if d > start]
    cutoff = recent[-PROVISIONAL_ESCALATE_ROWS - 1] if len(recent) > PROVISIONAL_ESCALATE_ROWS else None
    if cutoff is None:
        return []
    return [r['date'] for r in state['nav_series']
            if r.get('provisional') and start < r['date'] <= cutoff]


def gh_annotate(level, title, msg):
    import os
    if os.environ.get('GITHUB_ACTIONS'):
        print(f"::{level} title={title}::{msg}")
        path = os.environ.get('GITHUB_STEP_SUMMARY')
        if path:
            try:
                with open(path, 'a', encoding='utf-8') as f:
                    f.write(f"- {'⚠️' if level == 'warning' else '❌'} **{title}** — {msg}\n")
            except Exception:
                pass
