"""
日股 RS + VCP Screener
Pool: Nikkei 225 (225 檔,含 TOPIX Core 30 子集 30 檔)
Logic: identical to US/TW screener (RS 60% + VCP 40%)
Schedule: Mon-Fri 08:00 UTC = 17:00 JST (TSE 15:00 收盤後 2hr)
Universe last reviewed: 2026-05-07 (Nikkei 半年 review: 4 月 / 10 月)
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
HISTORY_DIR = SCREENER_DIR / 'jp_history'
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK = '1306.T'  # TOPIX ETF (NEXT FUNDS) — proxy for TOPIX (market-cap-weighted), 跟 US 'SPY' / TW '^TWII' 同模式; ^TPX yfinance 不支援故用 ETF
EMA_ALPHA = 0.2

# ── TOPIX Core 30 (top tier mega cap) ───────────────────────────────────
# Source: Wikipedia TOPIX article (2025 review). Subset of Nikkei 225.
TOPIX_CORE30 = {
    '4503.T': 'Astellas Pharma',
    '4568.T': 'Daiichi Sankyo',
    '6367.T': 'Daikin',
    '6902.T': 'Denso',
    '6954.T': 'FANUC',
    '6501.T': 'Hitachi',
    '7267.T': 'Honda',
    '7741.T': 'HOYA',
    '8001.T': 'Itochu',
    '9433.T': 'KDDI',
    '6861.T': 'Keyence',
    '8058.T': 'Mitsubishi Corp',
    '8031.T': 'Mitsui & Co',
    '8411.T': 'Mizuho FG',
    '8306.T': 'MUFG',
    '6981.T': 'Murata',
    '6594.T': 'Nidec',
    '7974.T': 'Nintendo',
    '9432.T': 'NTT',
    '6098.T': 'Recruit',
    '3382.T': 'Seven & i',
    '4063.T': 'Shin-Etsu Chemical',
    '8316.T': 'SMFG',
    '6273.T': 'SMC',
    '9984.T': 'SoftBank Group',
    '6758.T': 'Sony',
    '4502.T': 'Takeda Pharma',
    '8766.T': 'Tokio Marine',
    '8035.T': 'Tokyo Electron',
    '7203.T': 'Toyota',
}

# ── Nikkei 225 (broad blue-chip universe) ──────────────────────────────
# Source: Wikipedia Nikkei 225 article, 225 constituents grouped by sector.
NIKKEI_225 = {
    # Air transport (2)
    '9202.T': 'ANA Holdings', '9201.T': 'Japan Airlines',
    # Automotive (10)
    '543A.T': 'Archion', '7267.T': 'Honda', '7202.T': 'Isuzu', '7261.T': 'Mazda',
    '7211.T': 'Mitsubishi Motors', '7201.T': 'Nissan', '7270.T': 'Subaru',
    '7269.T': 'Suzuki', '7203.T': 'Toyota', '7272.T': 'Yamaha Motor',
    # Banking (10)
    '8304.T': 'Aozora Bank', '8331.T': 'Chiba Bank', '8354.T': 'Fukuoka FG',
    '8306.T': 'MUFG', '8411.T': 'Mizuho FG', '8308.T': 'Resona',
    '5831.T': 'Shizuoka FG', '8316.T': 'SMFG', '8309.T': 'SMTH', '7186.T': 'Concordia',
    # Chemicals (16)
    '3407.T': 'Asahi Kasei', '4061.T': 'Denka', '4901.T': 'Fujifilm', '4452.T': 'Kao',
    '3405.T': 'Kuraray', '4188.T': 'Mitsubishi Chemical', '4183.T': 'Mitsui Chemicals',
    '4021.T': 'Nissan Chemical', '6988.T': 'Nitto Denko', '4004.T': 'Resonac',
    '4063.T': 'Shin-Etsu Chemical', '4911.T': 'Shiseido', '4005.T': 'Sumitomo Chemical',
    '4043.T': 'Tokuyama', '4042.T': 'Tosoh', '4208.T': 'Ube',
    # Communications (4)
    '9433.T': 'KDDI', '9432.T': 'NTT', '9434.T': 'SoftBank Corp', '9984.T': 'SoftBank Group',
    # Construction (9)
    '1721.T': 'Comsys', '1925.T': 'Daiwa House', '1808.T': 'Haseko', '1963.T': 'JGC',
    '1812.T': 'Kajima', '1802.T': 'Obayashi', '1928.T': 'Sekisui House',
    '1803.T': 'Shimizu', '1801.T': 'Taisei',
    # Electric machinery (32)
    '6857.T': 'Advantest', '6770.T': 'Alps Alpine', '7751.T': 'Canon', '6902.T': 'Denso',
    '6954.T': 'FANUC', '6504.T': 'Fuji Electric', '6702.T': 'Fujitsu', '6501.T': 'Hitachi',
    '6861.T': 'Keyence', '285A.T': 'Kioxia', '6971.T': 'Kyocera', '6920.T': 'Lasertec',
    '6479.T': 'MinebeaMitsumi', '6503.T': 'Mitsubishi Electric', '6981.T': 'Murata',
    '6701.T': 'NEC', '6594.T': 'Nidec', '6645.T': 'Omron', '6752.T': 'Panasonic',
    '6723.T': 'Renesas', '7752.T': 'Ricoh', '6963.T': 'Rohm', '7735.T': 'SCREEN',
    '6724.T': 'Seiko Epson', '6753.T': 'Sharp', '6758.T': 'Sony', '6526.T': 'Socionext',
    '6976.T': 'Taiyo Yuden', '6762.T': 'TDK', '8035.T': 'Tokyo Electron',
    '6506.T': 'Yaskawa', '6841.T': 'Yokogawa',
    # Electric power (3)
    '9502.T': 'Chubu Electric', '9503.T': 'Kansai Electric', '9501.T': 'TEPCO',
    # Fishery (1)
    '1332.T': 'Nissui',
    # Foods (10)
    '2802.T': 'Ajinomoto', '2502.T': 'Asahi Group', '2914.T': 'Japan Tobacco',
    '2801.T': 'Kikkoman', '2503.T': 'Kirin', '2269.T': 'Meiji', '2282.T': 'NH Foods',
    '2871.T': 'Nichirei', '2002.T': 'Nisshin Seifun', '2501.T': 'Sapporo',
    # Gas (2)
    '9532.T': 'Osaka Gas', '9531.T': 'Tokyo Gas',
    # Glass & ceramics (6)
    '5201.T': 'AGC', '5333.T': 'NGK Insulators', '5214.T': 'Nippon Electric Glass',
    '5233.T': 'Taiheiyo Cement', '5301.T': 'Tokai Carbon', '5332.T': 'Toto',
    # Insurance (5)
    '8750.T': 'Dai-ichi Life', '8725.T': 'MS&AD', '8630.T': 'Sompo',
    '8795.T': 'T&D', '8766.T': 'Tokio Marine',
    # Land transport (2)
    '9147.T': 'Nippon Express', '9064.T': 'Yamato',
    # Machinery (16)
    '6113.T': 'Amada', '6367.T': 'Daikin', '6361.T': 'Ebara',
    '6305.T': 'Hitachi Construction', '7004.T': 'Kanadevia', '7013.T': 'IHI',
    '5631.T': 'Japan Steel Works', '6473.T': 'JTEKT', '6301.T': 'Komatsu',
    '6326.T': 'Kubota', '7011.T': 'Mitsubishi Heavy', '6471.T': 'NSK', '6472.T': 'NTN',
    '6103.T': 'Okuma', '6302.T': 'Sumitomo Heavy', '6273.T': 'SMC',
    # Marine transport (3)
    '9107.T': 'K Line', '9104.T': 'Mitsui OSK', '9101.T': 'NYK',
    # Mining (1)
    '1605.T': 'Inpex',
    # Nonferrous metals (8)
    '5714.T': 'Dowa', '5803.T': 'Fujikura', '5801.T': 'Furukawa Electric',
    '5711.T': 'Mitsubishi Materials', '5706.T': 'Mitsui Mining & Smelting',
    '3436.T': 'SUMCO', '5802.T': 'Sumitomo Electric', '5713.T': 'Sumitomo Metal Mining',
    # Other financial (3)
    '8253.T': 'Credit Saison', '8697.T': 'JPX', '8591.T': 'Orix',
    # Other manufacturing (4)
    '7832.T': 'Bandai Namco', '7912.T': 'DNP', '7911.T': 'Toppan', '7951.T': 'Yamaha Corp',
    # Petroleum (2)
    '5020.T': 'Eneos', '5019.T': 'Idemitsu',
    # Pharmaceuticals (9)
    '4503.T': 'Astellas', '4519.T': 'Chugai', '4568.T': 'Daiichi Sankyo',
    '4523.T': 'Eisai', '4151.T': 'Kyowa Kirin', '4578.T': 'Otsuka',
    '4506.T': 'Sumitomo Pharma', '4507.T': 'Shionogi', '4502.T': 'Takeda',
    # Precision instruments (6)
    '6146.T': 'Disco', '7741.T': 'HOYA', '4902.T': 'Konica Minolta',
    '7731.T': 'Nikon', '7733.T': 'Olympus', '4543.T': 'Terumo',
    # Pulp & paper (1)
    '3861.T': 'Oji',
    # Railway/bus (8)
    '9022.T': 'JR Central', '9020.T': 'JR East', '9008.T': 'Keio',
    '9009.T': 'Keisei', '9007.T': 'Odakyu', '9001.T': 'Tobu',
    '9005.T': 'Tokyu', '9021.T': 'JR West',
    # Real estate (5)
    '8802.T': 'Mitsubishi Estate', '8801.T': 'Mitsui Fudosan',
    '8830.T': 'Sumitomo Realty', '8804.T': 'Tokyo Tatemono', '3289.T': 'Tokyu Land',
    # Retail (11)
    '8267.T': 'Aeon', '9983.T': 'Fast Retailing', '3099.T': 'Isetan Mitsukoshi',
    '3086.T': 'J Front', '8252.T': 'Marui', '7453.T': 'Ryohin Keikaku (Muji)',
    '9843.T': 'Nitori', '7532.T': 'Pan Pacific (Don Quijote)',
    '3382.T': 'Seven & i', '8233.T': 'Takashimaya', '3092.T': 'ZOZO',
    # Rubber (2)
    '5108.T': 'Bridgestone', '5101.T': 'Yokohama Rubber',
    # Securities (2)
    '8601.T': 'Daiwa Securities', '8604.T': 'Nomura',
    # Services (19)
    '6532.T': 'Baycurrent', '4751.T': 'CyberAgent', '2432.T': 'DeNA', '4324.T': 'Dentsu',
    '6178.T': 'Japan Post', '9766.T': 'Konami', '4689.T': 'LY Corp',
    '4385.T': 'Mercari', '2413.T': 'M3', '3659.T': 'Nexon', '7974.T': 'Nintendo',
    '4307.T': 'NRI', '4661.T': 'Oriental Land', '4755.T': 'Rakuten',
    '6098.T': 'Recruit', '9735.T': 'Secom', '3697.T': 'SHIFT',
    '9602.T': 'Toho', '4704.T': 'Trend Micro',
    # Shipbuilding (1)
    '7012.T': 'Kawasaki Heavy',
    # Steel (3)
    '5411.T': 'JFE', '5406.T': 'Kobe Steel', '5401.T': 'Nippon Steel',
    # Textiles (2)
    '3401.T': 'Teijin', '3402.T': 'Toray',
    # Trading (7)
    '8001.T': 'Itochu', '8002.T': 'Marubeni', '8058.T': 'Mitsubishi Corp',
    '8031.T': 'Mitsui & Co', '2768.T': 'Sojitz', '8053.T': 'Sumitomo Corp',
    '8015.T': 'Toyota Tsusho',
}


def build_watchlist():
    """Merge Core30 + Nikkei225, dedup (Core30 wins so 30 mega-caps tagged Core30)."""
    wl = {}
    for tier_name, tier_dict in [('Core30', TOPIX_CORE30), ('N225', NIKKEI_225)]:
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
    print(f"=== 日股 RS+VCP Screener: {today} ===\n")

    watchlist = build_watchlist()
    tickers = list(watchlist.keys())
    core30_count = sum(1 for v in watchlist.values() if v['etf'] == 'Core30')
    n225_count = len(watchlist) - core30_count
    print(f"  Pool: {len(tickers)} stocks (Core30:{core30_count} + N225:{n225_count})")

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

    # Tier ranking (Core30 vs N225)
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

    latest_path = SCREENER_DIR / 'jp_latest.json'
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
