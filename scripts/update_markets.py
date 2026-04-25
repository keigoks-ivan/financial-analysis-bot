"""
Weekly auto-updater for markets.html and sectors.html
Fetches live data from Yahoo Finance via yfinance.
Runs every Saturday 08:00 Taiwan time (00:00 UTC) via GitHub Actions.

Updates: index levels, YTD, dividend yields, market caps, bond yields
Does NOT update: PE, PB, PEG, EPS growth, outlook, P/NAV, gearing, payout
"""

import re
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    print("Installing yfinance...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent

# ── Market index tickers (Yahoo Finance format) ─────────────────────────
MARKET_TICKERS = {
    # key must match the 'index' field in markets.html MARKETS array
    'SPX':    '^GSPC',
    'NDX':    '^NDX',
    'TPX':    '1306.T',      # TOPIX ETF as proxy
    'NKY':    '^N225',
    'UKX':    '^FTSE',
    'DAX':    '^GDAXI',
    'CAC':    '^FCHI',
    'IBEX':   '^IBEX',
    'AEX':    '^AEX',
    'SMI':    '^SSMI',
    'MIB':    '^FTSEMIB',    # FTSE MIB
    'AS51':   '^AXJO',       # ASX 200
    'TWSE':   '^TWII',       # TAIEX
    'KOSPI':  '^KS11',
    'STI':    '^STI',
    'HSI':    '^HSI',
    'CSI300': '000300.SS',
    'NIFTY':  '^NSEI',
    'KLCI':   '^KLSE',
    'SET':    '^SET.BK',
    'VNI':    '^VNINDEX',
    'JCI':    '^JKSE',
    'PSEI':   'PSEI.PS',
    'NZX50':  '^NZ50',
    'TSX':    '^GSPTSE',
    'IBOV':   '^BVSP',
    'MEXBOL': '^MXX',
    'TASI':   '^TASI.SR',
}

# ── 10-year bond tickers ───────────────────────────────────────────────
BOND_TICKERS = {
    'USD': '^TNX',      # US 10yr
    'JPY': '^TNX',      # placeholder — will manually offset
    'GBP': '^TNX',      # placeholder
    'EUR': '^TNX',      # placeholder
    'AUD': '^TNX',      # placeholder
    'SGD': '^TNX',      # placeholder
}


def fetch_quote(ticker_symbol):
    """Fetch current price and basic info from yfinance."""
    try:
        t = yf.Ticker(ticker_symbol)
        info = t.info
        return info
    except Exception as e:
        print(f"  ⚠ Failed to fetch {ticker_symbol}: {e}")
        return None


def get_ytd_return(ticker_symbol):
    """Calculate YTD return from Jan 1 to now."""
    try:
        t = yf.Ticker(ticker_symbol)
        year_start = datetime(datetime.now().year, 1, 2)
        hist = t.history(start=year_start.strftime('%Y-%m-%d'), period='1d')
        if hist.empty:
            return None
        first_close = hist['Close'].iloc[0]
        hist_recent = t.history(period='1d')
        if hist_recent.empty:
            return None
        last_close = hist_recent['Close'].iloc[-1]
        return round((last_close / first_close - 1) * 100, 1)
    except Exception as e:
        print(f"  ⚠ YTD calc failed for {ticker_symbol}: {e}")
        return None


def update_market_field(html, index_key, field, value):
    """Update a specific field for a market entry in the MARKETS JS array."""
    if value is None:
        return html
    pattern = rf"(index:'{re.escape(index_key)}'[^}}]*?{re.escape(field)}:)(-?[\d.]+)"
    new_html, count = re.subn(pattern, rf'\g<1>{value}', html)
    if count > 0:
        print(f"  ✓ {index_key}.{field} → {value}")
    return new_html


def update_ticker_field(html, ticker_key, field, value):
    """Update a specific field for a ticker-keyed entry (sectors)."""
    if value is None:
        return html
    pattern = rf"(ticker:'{re.escape(ticker_key)}'[^}}]*?{re.escape(field)}:)(-?[\d.]+)"
    new_html, count = re.subn(pattern, rf'\g<1>{value}', html)
    if count > 0:
        print(f"  ✓ {ticker_key}.{field} → {value}")
    return new_html


def main():
    changes = False
    now = datetime.now(timezone.utc)
    print(f"=== Market Data Update: {now.strftime('%Y-%m-%d %H:%M UTC')} ===\n")

    # ── Update markets.html ─────────────────────────────────────────────
    markets_path = ROOT / 'docs' / 'markets.html'
    markets_html = markets_path.read_text(encoding='utf-8')
    original_markets = markets_html

    print("── Fetching market indices ──")
    for index_key, ticker in MARKET_TICKERS.items():
        print(f"  Fetching {index_key} ({ticker})...")
        info = fetch_quote(ticker)
        if not info:
            continue

        # Update level (current price / index value)
        price = info.get('regularMarketPrice') or info.get('previousClose')
        if price:
            level = int(round(price))
            markets_html = update_market_field(markets_html, index_key, 'level', level)

        # Update YTD
        ytd = get_ytd_return(ticker)
        if ytd is not None:
            markets_html = update_market_field(markets_html, index_key, 'ytd', ytd)

        # Update dividend yield if available
        # For indices, trailingAnnualDividendYield is decimal (0.013 = 1.3%)
        div_yield_raw = info.get('trailingAnnualDividendYield')
        if div_yield_raw and div_yield_raw > 0:
            markets_html = update_market_field(markets_html, index_key, 'divYld', round(div_yield_raw * 100, 1))

    # ── Calculate RS for market indices (benchmark: VT) ──────────────
    print("\n── Calculating RS for market indices ──")
    try:
        all_idx_tickers = list(MARKET_TICKERS.values()) + ['VT']
        idx_data = yf.download(all_idx_tickers, period='100d', interval='1d',
                               group_by='ticker', progress=False, threads=True)

        def calc_ret(closes, days):
            if len(closes) < days + 1: return None
            return (closes.iloc[-1] / closes.iloc[-(days+1)] - 1) * 100

        idx_returns = {}
        for idx_key, yf_ticker in MARKET_TICKERS.items():
            try:
                c = idx_data[yf_ticker]['Close'].dropna()
                r1 = calc_ret(c, 5); r4 = calc_ret(c, 21); r13 = calc_ret(c, 63)
                if r1 is not None and r4 is not None and r13 is not None:
                    idx_returns[idx_key] = (r1, r4, r13)
            except: pass

        valid_keys = list(idx_returns.keys())
        if valid_keys:
            v1 = [idx_returns[k][0] for k in valid_keys]
            v4 = [idx_returns[k][1] for k in valid_keys]
            v13 = [idx_returns[k][2] for k in valid_keys]
            for k in valid_keys:
                r1, r4, r13 = idx_returns[k]
                pr1 = sum(1 for x in v1 if x <= r1) / len(v1) * 100
                pr4 = sum(1 for x in v4 if x <= r4) / len(v4) * 100
                pr13 = sum(1 for x in v13 if x <= r13) / len(v13) * 100
                rs = pr1 * 0.2 + pr4 * 0.3 + pr13 * 0.5
                if pr1 > pr4 > pr13: trend = 'accelerating'; rs = min(100, rs + 5)
                elif pr1 >= pr4 >= pr13: trend = 'steady'; rs = min(100, rs + 2)
                elif pr1 < pr4 < pr13: trend = 'fading'; rs = max(0, rs - 5)
                else: trend = 'choppy'
                markets_html = update_market_field(markets_html, k, 'rs', round(rs, 1))
                # Update rs_trend via regex
                import re as _re
                pat = rf"(index:'{_re.escape(k)}'[^}}]*?rs_trend:')([a-z]+)(')"
                markets_html = _re.sub(pat, rf"\g<1>{trend}\3", markets_html)
            print(f"  ✓ RS updated for {len(valid_keys)} indices")
    except Exception as e:
        print(f"  ⚠ RS calculation failed: {e}")

    if markets_html != original_markets:
        markets_path.write_text(markets_html, encoding='utf-8')
        changes = True
        print("\n✓ markets.html updated")
    else:
        print("\n– markets.html: no changes")

    # ── Update sectors.html ──────────────────────────────────────────────
    sectors_path = ROOT / 'docs' / 'sectors.html'
    if sectors_path.exists():
        sectors_html = sectors_path.read_text(encoding='utf-8')
        original_sectors = sectors_html

        SECTOR_TICKERS = [
            'XLK','XLF','XLE','XLV','XLY','XLP','XLI','XLC','XLU','XLRE','XLB',
            'VNQ','SMH','GDX','SOXX','ITA','IGV','XBI','ARKK','XOP','KRE','HACK','XHB'
        ]

        print("\n── Fetching sector ETF data ──")
        for sticker in SECTOR_TICKERS:
            print(f"  Fetching {sticker}...")
            info = fetch_quote(sticker)
            if not info:
                continue

            # Update price
            price = info.get('regularMarketPrice') or info.get('previousClose')
            if price:
                sectors_html = update_ticker_field(sectors_html, sticker, 'price', round(price, 2))

            # Update YTD
            ytd = get_ytd_return(sticker)
            if ytd is not None:
                sectors_html = update_ticker_field(sectors_html, sticker, 'ytd', ytd)

            # Update PE
            pe = info.get('trailingPE')
            if pe and pe > 0 and pe < 200:
                sectors_html = update_ticker_field(sectors_html, sticker, 'pe', round(pe, 1))

            # Update AUM
            aum = info.get('totalAssets')
            if aum and aum > 0:
                sectors_html = update_ticker_field(sectors_html, sticker, 'aum', round(aum / 1e9, 1))

        if sectors_html != original_sectors:
            sectors_path.write_text(sectors_html, encoding='utf-8')
            changes = True
            print("\n✓ sectors.html updated")
        else:
            print("\n– sectors.html: no changes")

    # ── Output for GitHub Actions ───────────────────────────────────────
    if changes:
        print(f"\n{'='*50}")
        print(f"✓ Data updated on {now.strftime('%Y-%m-%d')}")
        # Set output for GitHub Actions
        import os
        gh_output = os.environ.get('GITHUB_OUTPUT')
        if gh_output:
            with open(gh_output, 'a') as f:
                f.write("has_changes=true\n")
                f.write(f"summary=markets only data {now.strftime('%Y-%m-%d')}\n")
    else:
        print("\nNo changes detected.")
        import os
        gh_output = os.environ.get('GITHUB_OUTPUT')
        if gh_output:
            with open(gh_output, 'a') as f:
                f.write("has_changes=false\n")


if __name__ == '__main__':
    main()
