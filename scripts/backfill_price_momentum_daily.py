"""
One-off (2026-10-30): backfill daily NAV rows into the two P10 paper tracks
(docs/research/price-momentum{,-tw}/track.json) for the weekly-only era,
inception -> the last weekly row before the daily mark-only mode went live.

Holdings are fixed between rebalances, so every trading day's NAV is
cash + sum(units * close) on that period's holdings — the same arithmetic
mark_to_market() uses. Units and cash_seats come from each line's
rebalance_history; cash = NAV at the rebalance * cash_seats / N_SEATS.

Prices are yfinance closes with auto_adjust=False: each live run marked the
day's latest bar, which carried no later dividend adjustment, so raw closes
reproduce what a daily run would have recorded. Dividend-adjusted closes
would sit up to ~0.25 pt off the recorded rows (SPY's September ex-date).
Yahoo still back-adjusts those closes for later splits / capital reductions
(6173.TWO, 0.94 on 2026-10-07), so closes before such an event are multiplied
back by the ratio to get the price that actually traded and was marked.

Recorded weekly rows are never modified. Each one is dated by its run day
(usually Saturday) and stands for an earlier close; this script finds that
close by reconstructing both lines on the last few trading days and taking
the exact match, then aborts unless both lines of every recorded row are
reproduced within MAX_ABS_DIFF. The benchmark is only reported, not gated:
on the TW track Yahoo's 0050 bar often lagged the stocks by a day at run time
(the inception base 106.9 is the 09-14 close; the 09-19 and 10-17 rows carry
Thursday's 0050), so recorded nav_bench can sit one trading day behind.
Trading days between a row's close and its run-day label are skipped so the
series never runs backwards in time.

Usage: python3 scripts/backfill_price_momentum_daily.py [--write]
(without --write it only prints the check and the rows it would add).
"""

import json
import sys
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
LINE_KEYS = ('L12', 'L6')
N_SEATS = 10
CUTOFF = '2026-10-24'   # last weekly-era row; daily rows start after it
MAX_ABS_DIFF = 0.02     # recorded rows must be reproduced within this (NAV points)
MARKETS = [
    dict(path=ROOT / 'docs/research/price-momentum/track.json', bench='SPY',
         nav_key='nav_spy', close_key='spy_close', base_key='spy_close_inception'),
    dict(path=ROOT / 'docs/research/price-momentum-tw/track.json', bench='0050.TW',
         nav_key='nav_bench', close_key='bench_close', base_key='bench_close_inception'),
]
CHANGELOG_NOTE = (
    "2026-10-30 補算每日淨值：成立日到 2026-10-23 之間原本只有每週一筆，現在依換股紀錄的股數與現金席位，"
    "用當天實際收盤價（未還原除息，與當時每次執行記到的價格一致）補上每個交易日，補的列標 backfill。"
    "原本的週紀錄一筆都沒改；補算前先用同一方法重算每筆週紀錄，全部對上才寫入。"
)


def closes_by_date(px, ticker):
    """Closes as they traded: Yahoo's split back-adjustment undone for every
    split dated after the close."""
    try:
        c = px[ticker]['Close'].dropna()
    except Exception:
        return {}
    splits = yf.Ticker(ticker).splits
    splits = [(ts.strftime('%Y-%m-%d'), float(r)) for ts, r in splits.items()]
    out = {}
    for ts, v in c.items():
        d = ts.strftime('%Y-%m-%d')
        for sd, ratio in splits:
            if d < sd:
                v *= ratio
        out[d] = float(v)
    return out


def periods_for(state):
    """Per line: [(rebalance_label, holdings[(ticker, units)], cash_seats)] in date order."""
    out = {}
    for lk in LINE_KEYS:
        hist = sorted(state['lines'][lk]['rebalance_history'], key=lambda r: r['date'])
        out[lk] = [(r['date'], [(h['ticker'], h['units']) for h in r['holdings']], r['cash_seats'])
                   for r in hist]
    return out


def backfill(m, write):
    state = json.loads(m['path'].read_text(encoding='utf-8'))
    rows = state['nav_series']
    recorded = {r['date']: r for r in rows}
    periods = periods_for(state)
    tickers = sorted({t for lk in LINE_KEYS for _, hs, _ in periods[lk] for t, _ in hs})
    px = yf.download(tickers + [m['bench']], period='6mo', interval='1d', auto_adjust=False,
                     group_by='ticker', progress=False, threads=True)
    closes = {t: closes_by_date(px, t) for t in tickers}
    bench = closes_by_date(px, m['bench'])
    days = sorted(bench)

    def price(t, d):
        known = [x for x in closes[t] if x <= d]
        return closes[t][known[-1]] if known else None

    def period_of(lk, label):
        """Holdings in force after the latest rebalance whose label <= label."""
        ps = [p for p in periods[lk] if p[0] <= label]
        return ps[-1]

    def nav(lk, period, d):
        lbl, hs, cash_seats = period
        cash = recorded[lbl][f'nav_{lk}'] * cash_seats / N_SEATS
        return cash + sum(u * price(t, d) for t, u in hs)

    # 1) find each weekly-era recorded row's actual close date
    rep = {}
    worst = 0.0
    for r in rows:
        if r['date'] > CUTOFF:
            continue
        best = None
        for d in [x for x in days if x <= r['date']][-4:]:
            err = sum(abs(nav(lk, period_of(lk, r['date']), d) - r[f'nav_{lk}']) for lk in LINE_KEYS)
            if best is None or err < best[1]:
                best = (d, err)
        rep[r['date']] = best[0]
        diffs = [abs(round(nav(lk, period_of(lk, r['date']), best[0]), 2) - r[f'nav_{lk}']) for lk in LINE_KEYS]
        worst = max(worst, *diffs)
        bench_diff = round(100.0 * bench[best[0]] / state[m['base_key']], 2) - r[m['nav_key']]
        print(f"  row {r['date']} = close {best[0]}  lines max diff {max(diffs):.2f}"
              f"  (benchmark {m['bench']} {bench[best[0]]:.2f} vs recorded {r[m['close_key']]}, nav diff {bench_diff:+.2f})")
    if worst > MAX_ABS_DIFF:
        raise SystemExit(f"{m['path']}: recorded rows not reproduced (worst {worst:.2f} > {MAX_ABS_DIFF}) — nothing written")

    # 2) trading days to add: inside the weekly era, not already a recorded close,
    #    and not between a row's close and its later run-day label
    labels = sorted(d for d in rep)
    start, end = rep[labels[0]], rep[labels[-1]]
    taken = set(rep.values())
    blocked = {d for lbl, c in rep.items() for d in days if c < d <= lbl}
    rebal_close = {lk: [(rep[p[0]], p) for p in periods[lk]] for lk in LINE_KEYS}
    new_rows = []
    for d in days:
        if not (start < d < end) or d in taken or d in blocked:
            continue
        row = {'date': d}
        for lk in LINE_KEYS:
            period = [p for c, p in rebal_close[lk] if c < d][-1]
            row[f'nav_{lk}'] = round(nav(lk, period, d), 2)
        row[m['nav_key']] = round(100.0 * bench[d] / state[m['base_key']], 2)
        row[m['close_key']] = round(bench[d], 2)
        row['backfill'] = True
        new_rows.append(row)
    print(f"  {len(new_rows)} rows to add: {new_rows[0]['date']} … {new_rows[-1]['date']}" if new_rows else "  nothing to add")

    if write and new_rows:
        state['nav_series'] = sorted(rows + new_rows, key=lambda r: r['date'])
        if not any(e.get('event') == CHANGELOG_NOTE for e in state.get('changelog', [])):
            state['changelog'].append({'date': '2026-10-30', 'event': CHANGELOG_NOTE})
        m['path'].write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f"  ✓ wrote {m['path'].relative_to(ROOT)}")
    return new_rows


def main():
    write = '--write' in sys.argv[1:]
    for m in MARKETS:
        print(f"== {m['path'].relative_to(ROOT)}")
        backfill(m, write)


if __name__ == '__main__':
    main()
