"""
One-off (2026-10-30): correct two bookkeeping errors in the P10-TW paper track
(docs/research/price-momentum-tw/track.json). Both are mechanical — no
signal, eligibility, selection or rebalance decision changes.

1. 0050 benchmark one trading day stale. At the Saturday-morning builds
   Yahoo's 0050 bar often lagged the stocks by a day: the inception base 106.9
   is the 09-14 close (stocks were marked on 09-15, 0050 closed at 106.25), and
   the 09-19 / 10-17 rows carry Thursday's 0050. Fix: base = 0050 close on the
   inception close date; every weekly row's bench_close = 0050 on the close
   date its stocks were marked; nav_bench recomputed for every row.

2. 6173.TWO cash capital reduction (Yahoo split 0.94 dated 10-07, trading
   suspended 10-07..10-16). L6 kept the pre-reduction share count, so the 10-07
   and 10-08 marks overstate the position by units * (1 - 0.94) * price. Fix:
   subtract that on those two rows; the 10-08 rebalance (row 10-10) sized
   every new seat off the overstated NAV, so all later L6 rows, the 10-10
   rebalance units and the current holdings' units/cash scale by the same
   factor k = corrected / recorded NAV at the rebalance. Cash returned with the
   reduction is not added (price-return basis, same as dividends).

Weekly rows' close dates are the ones the line reconstruction in
backfill_price_momentum_daily.py matched exactly; this script re-derives them
from 0050's calendar (latest bar with volume > 0 before the run-day label) and
aborts if they differ. Idempotent: does nothing once its changelog note exists.

Usage: python3 scripts/backfill_price_momentum_tw_corrections.py [--write]
"""

import json
import sys
from pathlib import Path

import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
TRACK = ROOT / 'docs/research/price-momentum-tw/track.json'
BENCH = '0050.TW'
FIX_TICKER, FIX_LINE = '6173.TWO', 'L6'
WEEKLY_CLOSE = {   # run-day label -> close date its stocks were marked on (verified 2026-10-30)
    '2026-09-16': '2026-09-15', '2026-09-19': '2026-09-18', '2026-09-26': '2026-09-24',
    '2026-10-10': '2026-10-08', '2026-10-17': '2026-10-16', '2026-10-24': '2026-10-22',
}
NOTE_MARK = '2026-10-30 修正兩個記帳問題'


def daily(ticker):
    df = yf.download(ticker, start='2026-09-01', end='2026-11-15', auto_adjust=False, progress=False)
    df.columns = df.columns.get_level_values(0)
    return {ts.strftime('%Y-%m-%d'): (float(c), float(v)) for ts, c, v in zip(df.index, df['Close'], df['Volume'])
            if c == c}


def main():
    write = '--write' in sys.argv[1:]
    state = json.loads(TRACK.read_text(encoding='utf-8'))
    if any(e.get('event', '').startswith(NOTE_MARK) for e in state.get('changelog', [])):
        print('already corrected — nothing to do')
        return
    rows = state['nav_series']

    # ── 1. benchmark ──
    bench = daily(BENCH)
    traded = sorted(d for d, (_, v) in bench.items() if v > 0)
    derived = {lbl: [d for d in traded if d < lbl][-1] for lbl in WEEKLY_CLOSE}
    if derived != WEEKLY_CLOSE:
        raise SystemExit(f'weekly close dates differ from the verified map: {derived}')
    inception_close = WEEKLY_CLOSE[state['inception_date']]
    base = bench[inception_close][0]
    print(f"0050 base {state['bench_close_inception']} -> {base:.2f} ({inception_close} close)")
    for r in rows:
        if r['date'] in WEEKLY_CLOSE:
            c = round(bench[WEEKLY_CLOSE[r['date']]][0], 2)
            if c != r['bench_close']:
                print(f"  row {r['date']}: bench_close {r['bench_close']} -> {c} ({WEEKLY_CLOSE[r['date']]})")
            r['bench_close'] = c
        r['nav_bench'] = round(100.0 * r['bench_close'] / base, 2)
    state['bench_close_inception'] = round(base, 2)

    # ── 2. 6173.TWO reduction in L6 ──
    splits = [(ts.strftime('%Y-%m-%d'), float(x)) for ts, x in yf.Ticker(FIX_TICKER).splits.items()
              if ts.strftime('%Y-%m-%d') >= '2026-09-01']
    if len(splits) != 1:
        raise SystemExit(f'expected one {FIX_TICKER} split since 09-01, got {splits}')
    split_date, ratio = splits[0]
    line = state['lines'][FIX_LINE]
    hist = sorted(line['rebalance_history'], key=lambda r: r['date'])
    units_old = [h['units'] for h in hist[0]['holdings'] if h['ticker'] == FIX_TICKER][0]
    rebal_label = hist[1]['date']                       # 2026-10-10, marked on the 10-08 close
    rebal_close = WEEKLY_CLOSE[rebal_label]
    px = daily(FIX_TICKER)
    by_date = {r['date']: r for r in rows}
    old_rebal_nav = by_date[rebal_label][f'nav_{FIX_LINE}']
    for r in rows:
        close = WEEKLY_CLOSE.get(r['date'], r['date'])
        if split_date <= close <= rebal_close:
            delta = units_old * (1 - ratio) * px[close][0]
            print(f"  {FIX_LINE} row {r['date']} (close {close}): {r[f'nav_{FIX_LINE}']} - {delta:.4f}")
            r[f'nav_{FIX_LINE}'] = round(r[f'nav_{FIX_LINE}'] - delta, 2)
    k = by_date[rebal_label][f'nav_{FIX_LINE}'] / old_rebal_nav
    print(f"  k = {k:.6f} applied to {FIX_LINE} rows after {rebal_label}, its {rebal_label} rebalance units, current units/cash")
    for r in rows:
        if r['date'] > rebal_label:
            r[f'nav_{FIX_LINE}'] = round(r[f'nav_{FIX_LINE}'] * k, 2)
    for h in hist[1]['holdings']:
        h['units'] = round(h['units'] * k, 6)
    for h in line['holdings']:
        h['units'] = h['units'] * k
    line['cash'] = line['cash'] * k

    # ── check: the latest row equals cash + units * last_price on the corrected holdings ──
    last = rows[-1]
    recon = line['cash'] + sum(h['units'] * h['last_price'] for h in line['holdings'])
    print(f"  check {last['date']}: recomputed {FIX_LINE} {recon:.2f} vs row {last[f'nav_{FIX_LINE}']}")
    if abs(recon - last[f'nav_{FIX_LINE}']) > 0.02:
        raise SystemExit('corrected holdings do not reproduce the latest row — nothing written')

    note = (f"{NOTE_MARK}。一、0050 基準：週六建置時 Yahoo 的 0050 常少了前一天的收盤，成立基準 "
            f"106.9 其實是 09-14 收盤；改以 {inception_close} 收盤 {base:.2f} 為 100，09-19、10-17 兩筆週紀錄的 "
            f"0050 換成與持股同一天的收盤，整條 0050 淨值重算。二、{FIX_TICKER} {split_date} 現金減資（股數乘 "
            f"{ratio}），L6 當時沒有調整股數，{split_date} 到 {rebal_close} 多算約 "
            f"{units_old * (1 - ratio) * px[rebal_close][0]:.2f} 點；這兩天扣回，{rebal_label} 換股之後的股數、現金與淨值"
            f"按同一比例下修（乘 {k:.5f}）。退回的現金照價格報酬口徑不計，與一般股利相同。")
    state['changelog'].append({'date': '2026-10-30', 'event': note})
    print(note)
    if write:
        TRACK.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f"✓ wrote {TRACK.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
