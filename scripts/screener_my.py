"""
馬股 (Bursa Malaysia) RS + VCP Screener
Pool: FBM KLCI 30 (large cap) + ~60 liquid Mid/growth names = ~90 檔
Logic: identical to US/TW/JP screener (RS 60% + VCP 40%)
Benchmark: ^KLSE (FTSE Bursa Malaysia KLCI index) — yfinance native, no ETF proxy needed
Schedule: Mon-Fri 11:00 UTC = 19:00 MYT (Bursa 17:00 收盤後 2hr buffer)
Universe last reviewed: 2026-06-09
  - KLCI 30: large-cap tier (Bursa FBM KLCI, ~Jun 2026; IOIPG inclusion effective late-Jun 2026 not yet added)
  - Mid tier: seeded from FBM Mid 70 (Bursa Jun 2025 list) + Jun 2026 review entrants
    (AAX/ALLIANZ/RANHILL/SLVEST) + liquid Bursa mid/small growth names.
  - ALL codes + names sourced from Yahoo Finance shortName and yfinance-verified live
    (>=200 trading days of history) on 2026-06-09. Delisted names (e.g. MAHB 5014) excluded.
  - FBM index reviews are semi-annual (Jun/Dec); reconcile Mid tier against official
    FBM70 constituents at next review.
"""

import json, os, sys, math, warnings
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance', 'pandas', 'numpy', '-q'])
    import numpy as np
    import pandas as pd
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
SCREENER_DIR = ROOT / 'docs' / 'screener'
HISTORY_DIR = SCREENER_DIR / 'my_history'
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK = '^KLSE'  # FTSE Bursa Malaysia KLCI index — yfinance native (跟 US 'SPY' / TW '^TWII' 同模式)
EMA_ALPHA = 0.2

# ── FBM KLCI 30 (large cap tier) ────────────────────────────────────────
# Names = Yahoo Finance shortName (idiomatic Bursa tickers). Verified live 2026-06-09.
KLCI_30 = {
    '1155.KL': 'MAYBANK', '1295.KL': 'PBBANK', '1023.KL': 'CIMB',
    '5347.KL': 'TENAGA', '5225.KL': 'IHH', '5183.KL': 'PCHEM',
    '8869.KL': 'PMETAL', '5819.KL': 'HLBANK', '4197.KL': 'SIME',
    '6888.KL': 'AXIATA', '6033.KL': 'PETGAS', '6947.KL': 'CDB',
    '6012.KL': 'MAXIS', '4065.KL': 'PPB', '4707.KL': 'NESTLE',
    '3816.KL': 'MISC', '3182.KL': 'GENTING', '4715.KL': 'GENM',
    '1082.KL': 'HLFG', '4863.KL': 'TM', '1066.KL': 'RHBBANK',
    '2445.KL': 'KLK', '1961.KL': 'IOICORP', '5285.KL': 'SDG',
    '5296.KL': 'MRDIY', '7084.KL': 'QL', '5398.KL': 'GAMUDA',
    '4677.KL': 'YTL', '6742.KL': 'YTLPOWR', '5211.KL': 'SUNWAY',
}

# ── FBM Mid tier (liquid mid / growth) ──────────────────────────────────
# Names = Yahoo Finance shortName. Verified live 2026-06-09. KLCI 30 dups removed.
MID_70 = {
    '1163.KL': 'ALLIANZ', '1171.KL': 'MBSB', '1015.KL': 'AMBANK',
    '2852.KL': 'CMSB', '3336.KL': 'IJM', '3417.KL': 'E&O',
    '3859.KL': 'MAGNUM', '4162.KL': 'BAT', '4731.KL': 'SCIENTX',
    '5005.KL': 'UNISEM', '5012.KL': 'TAANN', '5031.KL': 'TIMECOM',
    '5099.KL': 'CAPITALA', '5106.KL': 'AXREIT', '5141.KL': 'DAYANG',
    '5142.KL': 'WASCO', '5176.KL': 'SUNREIT', '5202.KL': 'MSM',
    '5210.KL': 'ARMADA', '5212.KL': 'PAVREIT', '5218.KL': 'VANTNRG',
    '5227.KL': 'IGBREIT', '5238.KL': 'AAX', '5246.KL': 'WPRTS',
    '5263.KL': 'SUNCON', '5272.KL': 'RANHILL', '5306.KL': 'FFB',
    '5681.KL': 'PETDAG', '5878.KL': 'KPJ', '6076.KL': 'ENCORP',
    '6399.KL': 'ASTRO', '7022.KL': 'GTRONIC', '7100.KL': 'UCHITEC',
    '7106.KL': 'SUPERMX', '7113.KL': 'TOPGLOV', '7160.KL': 'PENTA',
    '7277.KL': 'DIALOG', '0072.KL': 'ERDASAN', '0097.KL': 'VITROX',
    '0138.KL': 'ZETRIX', '0146.KL': 'JFTECH', '0166.KL': 'INARI',
    '0200.KL': 'REVENUE', '0208.KL': 'GREATEC', '0215.KL': 'SLVEST',
    '5235SS.KL': 'KLCC', '2291.KL': 'GENP', '5168.KL': 'HARTA',
    '3794.KL': 'MCEMENT', '5102.KL': 'GCB', '0090.KL': 'ELSOFT',
    '0250.KL': 'YXPM', '6963.KL': 'VS', '5275.KL': 'MYNEWS',
    '5184.KL': 'CYPARK', '0035.KL': 'HEXCAP', '5258.KL': 'BIMB',
    '5072.KL': 'HIAPTEK', '5253.KL': 'ECONBHD', '0241.KL': 'TAGHILL',
}


def build_watchlist():
    """Merge KLCI30 + Mid70, dedup (KLCI30 wins so large caps tagged KLCI30)."""
    wl = {}
    for tier_name, tier_dict in [('KLCI30', KLCI_30), ('Mid70', MID_70)]:
        for ticker, name in tier_dict.items():
            if ticker not in wl:
                wl[ticker] = {'name': name, 'etf': tier_name}
    return wl


# ── Reuse core logic from US screener ────────────────────────────────────
sys.path.insert(0, str(ROOT / 'scripts'))
from screener import (
    calc_return, percentile_rank, find_local_highs, calc_vcp,
    EMA_ALPHA, NpEncoder
)


def load_previous_history():
    files = sorted(HISTORY_DIR.glob('*.json'))
    if not files:
        return {}
    try:
        with open(files[-1]) as f:
            data = json.load(f)
        return {r['ticker']: r for r in data.get('rankings', [])}
    except:
        return {}


def main():
    now = datetime.now(timezone.utc)
    today = now.strftime('%Y-%m-%d')
    print(f"=== 馬股 RS+VCP Screener: {today} ===\n")

    watchlist = build_watchlist()
    tickers = list(watchlist.keys())
    klci_count = sum(1 for v in watchlist.values() if v['etf'] == 'KLCI30')
    mid_count = len(watchlist) - klci_count
    print(f"  Pool: {len(tickers)} stocks (KLCI30:{klci_count} + Mid70:{mid_count})")

    # Fetch data
    print(f"  Fetching {len(tickers)} tickers (benchmark: {BENCHMARK})...")
    all_tickers = tickers + [BENCHMARK]
    data = yf.download(all_tickers, period='300d', interval='1d', group_by='ticker', progress=False, threads=True)
    prev = load_previous_history()

    # Calculate RS
    print("  Calculating RS scores...")
    rs_raw = {}
    for ticker in tickers:
        try:
            closes = data[ticker]['Close'].dropna()
            r1w = calc_return(closes, 5)
            r4w = calc_return(closes, 21)
            r13w = calc_return(closes, 63)
            if r1w is not None and r4w is not None and r13w is not None:
                rs_raw[ticker] = {'r1w': r1w, 'r4w': r4w, 'r13w': r13w}
        except:
            pass

    if not rs_raw:
        print("ERROR: No valid data")
        return

    valid_tickers = list(rs_raw.keys())
    pr1w = percentile_rank([rs_raw[t]['r1w'] for t in valid_tickers])
    pr4w = percentile_rank([rs_raw[t]['r4w'] for t in valid_tickers])
    pr13w = percentile_rank([rs_raw[t]['r13w'] for t in valid_tickers])

    results = []
    for i, ticker in enumerate(valid_tickers):
        raw_1w, raw_4w, raw_13w = pr1w[i], pr4w[i], pr13w[i]
        prev_data = prev.get(ticker, {})
        if prev_data:
            s1w = prev_data.get('rs_1w', raw_1w) * (1 - EMA_ALPHA) + raw_1w * EMA_ALPHA
            s4w = prev_data.get('rs_4w', raw_4w) * (1 - EMA_ALPHA) + raw_4w * EMA_ALPHA
            s13w = prev_data.get('rs_13w', raw_13w) * (1 - EMA_ALPHA) + raw_13w * EMA_ALPHA
        else:
            s1w, s4w, s13w = raw_1w, raw_4w, raw_13w

        persistence = s1w * 0.2 + s4w * 0.3 + s13w * 0.5
        if s1w > s4w > s13w: trend, bonus = 'accelerating', 5
        elif s1w >= s4w >= s13w: trend, bonus = 'steady', 2
        elif s1w < s4w < s13w: trend, bonus = 'fading', -5
        else: trend, bonus = 'choppy', 0
        rs_score = min(100, persistence + bonus)

        try:
            closes = data[ticker]['Close'].dropna()
            highs = data[ticker]['High'].dropna()
            lows = data[ticker]['Low'].dropna()
            volumes = data[ticker]['Volume'].dropna()
            price = float(closes.iloc[-1])
            ma200 = closes.iloc[-200:].mean() if len(closes) >= 200 else (closes.iloc[-60:].mean() if len(closes) >= 60 else price)
            vs_200ma = (price - ma200) / ma200 * 100
            vcp = calc_vcp(closes, highs, lows, volumes)
        except:
            price, vs_200ma = 0, 0
            vcp = {'score': 0, 'pullback_count': 0, 'last_pullback_pct': 0,
                   'dist_from_high_pct': 0, 'atr_ratio': 1.0, 'vol_ratio': 1.0, 'trend_ok': False}

        combined = round(rs_score * 0.6 + vcp['score'] * 0.4, 1)
        info = watchlist.get(ticker, {})

        results.append({
            'ticker': ticker,
            'name': info.get('name', ''),
            'etf': info.get('etf', ''),
            'rs_score': round(rs_score, 1),
            'rs_trend': trend,
            'rs_1w': round(s1w, 1),
            'rs_4w': round(s4w, 1),
            'rs_13w': round(s13w, 1),
            'vcp_score': vcp['score'],
            'pullback_count': vcp['pullback_count'],
            'last_pullback_pct': vcp['last_pullback_pct'],
            'dist_from_high_pct': vcp['dist_from_high_pct'],
            'atr_ratio': vcp['atr_ratio'],
            'vol_ratio': vcp.get('vol_ratio', 1.0),
            'combined': combined,
            'price': round(price, 2),
            'vs_200ma_pct': round(vs_200ma, 1),
            'trend_ok': bool(vcp['trend_ok']),
        })

    results.sort(key=lambda x: x['combined'], reverse=True)

    for i, r in enumerate(results):
        r['rank'] = i + 1
        prev_r = prev.get(r['ticker'], {})
        prev_rank = prev_r.get('rank')
        if prev_rank:
            diff = prev_rank - r['rank']
            r['rank_change'] = f'+{diff}' if diff > 0 else (str(diff) if diff < 0 else '—')
        else:
            r['rank_change'] = 'NEW'

    # Top Picks
    print("  Selecting top picks...")
    picks = {}
    used = set()
    def pick(key, cands):
        for r in cands:
            if r['ticker'] not in used:
                picks[key] = r['ticker']
                used.add(r['ticker'])
                return
    for label in ['minervini_1', 'minervini_2', 'minervini_3']:
        for cond in [
            lambda r: r['rs_score']>=80 and r['vcp_score']>=75 and r['rs_trend']=='accelerating',
            lambda r: r['rs_score']>=78 and r['vcp_score']>=70 and r['rs_trend'] in ('accelerating','steady'),
            lambda r: r['rs_score']>=75 and r['vcp_score']>=60,
            lambda r: r['rs_score']>=70 and r['vcp_score']>=50,
        ]:
            found = [r for r in results if r['ticker'] not in used and cond(r)]
            if found:
                pick(label, found)
                break
    try:
        mom = [r for r in results if r['rs_score']>=65 and r['rank_change'] not in ('—','NEW') and int(r['rank_change'].replace('+',''))>0]
        mom.sort(key=lambda r: int(r['rank_change'].replace('+','')), reverse=True)
        pick('momentum', mom)
    except: pass
    vcp_c = [r for r in results if r['vcp_score']>=60 and r['rs_score']>=55 and r['ticker'] not in used]
    vcp_c.sort(key=lambda r: r['vcp_score']*0.7+r['rs_score']*0.3, reverse=True)
    pick('vcp_1', vcp_c)
    pick('vcp_2', [r for r in vcp_c if r['ticker'] not in used])
    pick('vcp_3', [r for r in vcp_c if r['ticker'] not in used])

    # Tier ranking (KLCI30 vs Mid70)
    etf_scores = {}
    for r in results:
        e = r['etf']
        if e not in etf_scores: etf_scores[e] = []
        etf_scores[e].append(r['rs_score'])
    etf_ranking = [{'etf': e, 'avg_rs': round(np.mean(v), 1), 'count': len(v)}
                   for e, v in etf_scores.items()]
    etf_ranking.sort(key=lambda x: x['avg_rs'], reverse=True)

    output = {
        'date': today,
        'total_stocks': len(results),
        'benchmark': BENCHMARK,
        'top_picks': picks,
        'top_etf': etf_ranking[0] if etf_ranking else {},
        'etf_ranking': etf_ranking,
        'rankings': results,
    }

    latest_path = SCREENER_DIR / 'my_latest.json'
    with open(latest_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, cls=NpEncoder)

    history_path = HISTORY_DIR / f'{today}.json'
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, cls=NpEncoder)

    print(f"\n  ✓ Output: {latest_path}")
    print(f"  ✓ Top 5: {', '.join(r['ticker']+' '+r['name'] for r in results[:5])}")
    print(f"  ✓ Picks: {picks}")
    if etf_ranking:
        print(f"  ✓ Top tier: {etf_ranking[0]['etf']} (avg RS {etf_ranking[0]['avg_rs']})")

    gh_output = os.environ.get('GITHUB_OUTPUT')
    if gh_output:
        with open(gh_output, 'a') as f:
            f.write("has_changes=true\n")


if __name__ == '__main__':
    main()
