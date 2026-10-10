"""
台股 RS + VCP Screener
Pool: 0050 + 0051 + 006201 ≈ 200 支
Logic: identical to US screener (RS 60% + VCP 40%)
Schedule: Mon-Fri 16:00 Taiwan (08:00 UTC)
成分股對照日：2026-10-08。下次調整：富櫃50 2026-10-19 生效（1、4、7、10 月審核），
0050/0051 2026-12（3、6、9、12 月審核）。調整後要手動更新下面三份名單。
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
HISTORY_DIR = SCREENER_DIR / 'tw_history'
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK = '^TWII'
EMA_ALPHA = 0.2

# ── 0050 台灣50（臺灣50指數）────────────────────────────────────────────
# 成分股＝元大 0050 / 0051 持股（2026-10-08，依權重排序）、櫃買中心富櫃50指數當日成分股
# （2026-10-08）。名稱後的 * 已去掉。
ETF_0050 = {
    '2330.TW':'台積電','2454.TW':'聯發科','2308.TW':'台達電','2317.TW':'鴻海',
    '3711.TW':'日月光投控','2383.TW':'台光電','2303.TW':'聯電','3037.TW':'欣興',
    '1303.TW':'南亞','2881.TW':'富邦金','2891.TW':'中信金','3017.TW':'奇鋐',
    '2882.TW':'國泰金','2345.TW':'智邦','2327.TW':'國巨','2887.TW':'台新新光金',
    '2360.TW':'致茂','2382.TW':'廣達','2885.TW':'元大金','2884.TW':'玉山金',
    '6669.TW':'緯穎','2408.TW':'南亞科','2357.TW':'華碩','3443.TW':'創意',
    '3008.TW':'大立光','3653.TW':'健策','2883.TW':'凱基金','2059.TW':'川湖',
    '2301.TW':'光寶科','2886.TW':'兆豐金','2890.TW':'永豐金','3231.TW':'緯創',
    '2412.TW':'中華電','2344.TW':'華邦電','4958.TW':'臻鼎-KY','2368.TW':'金像電',
    '2880.TW':'華南金','2892.TW':'第一金','3665.TW':'貿聯-KY','1216.TW':'統一',
    '6446.TW':'藥華藥','8046.TW':'南電','2449.TW':'京元電子','7769.TW':'鴻勁',
    '2395.TW':'研華','5880.TW':'合庫金','2603.TW':'長榮','4904.TW':'遠傳',
    '3045.TW':'台灣大','6505.TW':'台塑化',
}

# ── 0051 中型100（臺灣中型100指數）──────────────────────────────────────
ETF_0051 = {
    '3481.TW':'群創','2379.TW':'瑞昱','3661.TW':'世芯-KY','3189.TW':'景碩',
    '1301.TW':'台塑','3034.TW':'聯詠','1326.TW':'台化','6770.TW':'力積電',
    '2313.TW':'華通','3044.TW':'健鼎','2404.TW':'漢唐','2409.TW':'友達',
    '2337.TW':'旺宏','2801.TW':'彰銀','6239.TW':'力成','2002.TW':'中鋼',
    '2376.TW':'技嘉','5876.TW':'上海商銀','6213.TW':'聯茂','4938.TW':'和碩',
    '3702.TW':'大聯大','1101.TW':'台泥','1590.TW':'亞德客-KY','3036.TW':'文曄',
    '2615.TW':'萬海','3533.TW':'嘉澤','6415.TW':'矽力-KY','2207.TW':'和泰車',
    '2324.TW':'仁寶','6515.TW':'穎崴','5871.TW':'中租-KY','8996.TW':'高力',
    '2356.TW':'英業達','2834.TW':'臺企銀','6805.TW':'富世達','6257.TW':'矽格',
    '6139.TW':'亞翔','2347.TW':'聯強','2492.TW':'華新科','1605.TW':'華新',
    '2618.TW':'長榮航','2912.TW':'統一超','3026.TW':'禾伸堂','1560.TW':'中砂',
    '6442.TW':'光聖','1519.TW':'華城','2377.TW':'微星','2609.TW':'陽明',
    '6531.TW':'愛普','2455.TW':'全新','2049.TW':'上銀','5434.TW':'崇越',
    '6285.TW':'啟碁','1402.TW':'遠東新','2353.TW':'宏碁','1504.TW':'東元',
    '2027.TW':'大成鋼','1102.TW':'亞泥','2474.TW':'可成','2812.TW':'台中銀',
    '3706.TW':'神達','6919.TW':'康霈','7750.TW':'新代','3023.TW':'信邦',
    '2385.TW':'群光','6196.TW':'帆宣','1513.TW':'中興電','3167.TW':'大量',
    '1802.TW':'台玻','3006.TW':'晶豪科','1717.TW':'長興','2354.TW':'鴻準',
    '2610.TW':'華航','7610.TW':'聯友金屬-創','8464.TW':'億豐','6409.TW':'旭隼',
    '1476.TW':'儒鴻','9904.TW':'寶成','5269.TW':'祥碩','6691.TW':'洋基工程',
    '8210.TW':'勤誠','1503.TW':'士電','2451.TW':'創見','2542.TW':'興富發',
    '2105.TW':'正新','2467.TW':'志聖','2633.TW':'台灣高鐵','6789.TW':'采鈺',
    '9945.TW':'潤泰新','3005.TW':'神基','3030.TW':'德律','1229.TW':'聯華',
    '3532.TW':'台勝科','6526.TW':'達發','6781.TW':'AES-KY','6949.TW':'沛爾生醫-創',
    '9910.TW':'豐泰','2646.TW':'星宇航空','2838.TW':'聯邦銀','2645.TW':'長榮航太',
}

# ── 006201 富櫃50（櫃買中心富櫃五十指數）────────────────────────────────
# 2026-10-10 前這份名單標成 00714，但 00714 是群益道瓊美國地產；追蹤富櫃50 的是元大 006201。
ETF_006201 = {
    '1785.TWO':'光洋科','3374.TWO':'精材','5439.TWO':'高技','6510.TWO':'精測',
    '1815.TWO':'富喬','3491.TWO':'昇達科','5483.TWO':'中美晶','6548.TWO':'長科',
    '3081.TWO':'聯亞','3529.TWO':'力旺','5536.TWO':'聖暉','6584.TWO':'南俊國際',
    '3105.TWO':'穩懋','3680.TWO':'家登','5904.TWO':'寶雅','6683.TWO':'雍智科技',
    '3131.TWO':'弘塑','3718.TWO':'中光電投控','6121.TWO':'新普','7734.TWO':'印能科技',
    '3163.TWO':'波若威','4749.TWO':'新應材','6147.TWO':'頎邦','7828.TWO':'創新服務',
    '3211.TWO':'順達','4772.TWO':'台特化','6173.TWO':'信昌電','7856.TWO':'漢測',
    '3227.TWO':'原相','4966.TWO':'譜瑞-KY','6182.TWO':'合晶','8069.TWO':'元太',
    '3260.TWO':'威剛','4979.TWO':'華星光','6187.TWO':'萬潤','8299.TWO':'群聯',
    '3264.TWO':'欣銓','4991.TWO':'環宇-KY','6223.TWO':'旺矽','8358.TWO':'金居',
    '3293.TWO':'鈊象','5274.TWO':'信驊','6274.TWO':'台燿','8932.TWO':'智通',
    '3324.TWO':'雙鴻','5289.TWO':'宜鼎','6290.TWO':'良維','3357.TWO':'臺慶科',
    '5347.TWO':'世界','6488.TWO':'環球晶',
}


def build_watchlist():
    """Merge 0050 + 0051 + 006201, dedup (first wins)."""
    wl = {}
    for etf_name, etf_dict in [('0050', ETF_0050), ('0051', ETF_0051), ('006201', ETF_006201)]:
        for ticker, name in etf_dict.items():
            if ticker not in wl:
                wl[ticker] = {'name': name, 'etf': etf_name}
    return wl


# ── Reuse core logic from US screener ────────────────────────────────────
# Import shared functions
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
    print(f"=== 台股 RS+VCP Screener: {today} ===\n")

    watchlist = build_watchlist()
    tickers = list(watchlist.keys())
    print(f"  Pool: {len(tickers)} stocks (0050:{len(ETF_0050)} + 0051:{len(ETF_0051)} + 006201:{len(ETF_006201)})")

    # Fetch data
    print(f"  Fetching {len(tickers)} tickers...")
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

    # Top Picks (same logic as US)
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

    # ETF ranking
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

    latest_path = SCREENER_DIR / 'tw_latest.json'
    with open(latest_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, cls=NpEncoder)

    history_path = HISTORY_DIR / f'{today}.json'
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, cls=NpEncoder)

    print(f"\n  ✓ Output: {latest_path}")
    print(f"  ✓ Top 5: {', '.join(r['ticker']+' '+r['name'] for r in results[:5])}")
    print(f"  ✓ Picks: {picks}")
    print(f"  ✓ Top ETF: {etf_ranking[0]['etf']} (avg RS {etf_ranking[0]['avg_rs']})")

    gh_output = os.environ.get('GITHUB_OUTPUT')
    if gh_output:
        with open(gh_output, 'a') as f:
            f.write("has_changes=true\n")


if __name__ == '__main__':
    main()
