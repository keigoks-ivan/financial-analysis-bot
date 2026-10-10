#!/usr/bin/env python3
"""台股全市場雷達 — docs/cockpit-tw/data/_radar_tw_body.html + radar_tw.json (2026-10-10).

The US radar's four shapes (scripts/engine/build_radar.py, v1 thresholds locked
2026-07-04) run on the TW stage universe: 0050 + 0051 + 006201 constituents ∪
the TW pool, the same list as build_stages_tw.py (~220 names). build_radar.P
and tag_shapes() are imported, not copied or modified, so a threshold change
in the US radar carries over. What differs from the US radar:

  * Weekly bars are downloaded here (yfinance 25mo / 1wk, auto-adjusted) and
    never written to data/weekly_cache or data/weekly_cache_universe. Those
    directories feed the US DD base rates and the US arena.
  * Industry is the TWSE/TPEx official classification (tw_listing_suffix), not
    GICS. An industry needs HOT_MIN_MEMBERS names in the universe to count as
    hot: the official classification has ~30 groups and several have one or
    two names here, where one stock's 13-week move would decide the median.
  * 主題下沉 uses 0051 (臺灣中型100) membership where the US uses S&P 400.
  * 金融保險業 names are not listed and not counted in the hot-industry
    ranking (owner decision 2026-10-10): the radar finds names for the TW
    pool, and the pool excludes the same industries
    (build_dd_screener.TW_EXCLUDED_INDUSTRIES). They stay in the RS
    percentile, which measures a name against the whole universe (owner
    decision, same day). The stages page keeps them everywhere.
  * No stage 2 (30-day yfinance EPS revision) and no 三閘主榜. The TW revision
    source is the Koyfin snapshots, which have no post-earnings baseline yet
    (the TW seats wait for the same data), and the TW market-cap floor is the
    pool's own.
  * 「距高點」 is the distance from the highest weekly close in the 25-month
    window. The US column says ATH but computes the same thing.

The per-ticker formulas repeat build_radar.stage1() (inline there, not a
function): 12M / 13W return, distance from the window high, weeks since that
high, deepest drawdown after it, 40-week average, RS percentile within the
universe.

Weekly: daily-taipei-morning.yml runs it on Saturday (Taipei) after the Friday
close. Writes only when at least MIN_SCORED_SHARE of the universe has 56+
weekly bars; otherwise the previous files stay.

Usage:
  python3 scripts/build_radar_tw.py
"""
from __future__ import annotations

import bisect
import json
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from engine import build_radar as br  # noqa: E402
from engine.build_arena import _BOARD_CSS  # noqa: E402
import build_stages_tw  # noqa: E402
from build_dd_screener import TW_EXCLUDED_INDUSTRIES  # noqa: E402
import screener_tw  # noqa: E402

OUT_DIR = ROOT / 'docs' / 'cockpit-tw' / 'data'
RADAR_TW_JSON = OUT_DIR / 'radar_tw.json'
RADAR_TW_HTML = OUT_DIR / '_radar_tw_body.html'
TW_POOL_JSON = build_stages_tw.TW_POOL_JSON

MIN_WEEKS = 56            # same as build_radar.stage1()
MIN_SCORED_SHARE = 0.7    # fail-safe: below this share of the universe, keep the old files
HOT_MIN_MEMBERS = 5
THEME_TIER = '0051'
TIER_LABEL = {'0050': '0050', '0051': '0051', '006201': '006201', 'pool': '池'}

SHAPE_TEXT = {
    'breakout_base': ('🟩 長基期突破帶',
                      f"兩年內的最高週收盤出現在 {br.P['base_age_min_w']} 週以前，現價離那個高點不到 "
                      f"{-br.P['breakout_dist_ath']:.0f}%，而且站上 40 週均線。整理越久排越前面。"),
    'cyclical_turn': ('🟧 循環轉折',
                      f"從兩年內高點跌過 {-br.P['cyc_depth']:.0f}% 以上，近 13 週反彈 {br.P['cyc_turn_13w']:.0f}% 以上，"
                      f"現價仍比高點低 {-br.P['cyc_dist_ath_max']:.0f}% 以上。近 13 週漲得多的排前面。"),
    'momentum_rerate': ('🟪 動能重估',
                        f"RS 百分位 ≥{br.P['mom_rs_pct']:.0f}，站上 40 週均線，離高點不到 "
                        f"{-br.P['mom_dist_ath']:.0f}%。近 12 個月漲得多的排前面。"),
    'theme_smallmid': ('🟦 主題下沉',
                       f"0051 成分股（臺灣中型100），RS 百分位 ≥{br.P['theme_rs_pct']:.0f}，站上 40 週均線，"
                       f"而且屬於近 13 週最熱的 {br.P['theme_hot_sectors']} 個產業。RS 高的排前面。"),
}


def download(tickers):
    """ticker → weekly close Series. TW tickers go to yfinance as written."""
    import yfinance as yf
    data = yf.download(tickers, period='25mo', interval='1wk', progress=False,
                       auto_adjust=True, group_by='column')
    closes = data['Close'] if 'Close' in data else data
    if isinstance(closes, pd.Series):
        closes = closes.to_frame(tickers[0])
    return {str(c): closes[c] for c in closes.columns}


def structure(closes):
    """build_radar.stage1() formulas on already-downloaded closes. Returns (rows, as_of)."""
    rows, as_of = [], None
    for t, s in closes.items():
        s = s.dropna()
        if len(s) < MIN_WEEKS:
            continue
        px = float(s.iloc[-1])
        hi_pos = int(np.argmax(s.values))
        hi = float(s.iloc[hi_pos])
        rows.append({
            'ticker': t, 'price': round(px, 2),
            'ret_12m': round(px / float(s.iloc[-53]) * 100 - 100, 1),
            'ret_13w': round(px / float(s.iloc[-14]) * 100 - 100, 1),
            'dist_ath': round(px / hi * 100 - 100, 1),
            'base_age_w': int(len(s) - 1 - hi_pos),
            'depth': round(float(s.iloc[hi_pos:].min()) / hi * 100 - 100, 1),
            'above_40w': bool(px > float(s.iloc[-40:].mean())),
        })
        d = str(s.index[-1].date())
        if as_of is None or d > as_of:
            as_of = d
    rets = sorted(r['ret_12m'] for r in rows)
    for r in rows:
        r['rs_pct'] = round(bisect.bisect_left(rets, r['ret_12m']) / len(rets) * 100, 1)
    return rows, as_of


def hot_industries(rows):
    by = {}
    for r in rows:
        if r.get('sector'):
            by.setdefault(r['sector'], []).append(r['ret_13w'])
    big = {k: v for k, v in by.items() if len(v) >= HOT_MIN_MEMBERS}
    return sorted(big, key=lambda k: -float(np.median(big[k])))[:br.P['theme_hot_sectors']]


def tag(rows):
    """Three shapes from build_radar.tag_shapes() (TW tiers never equal 'sp400',
    so its 主題下沉 comes back empty) plus the TW 主題下沉 on 0051 members."""
    shapes, _us_hot = br.tag_shapes(rows)
    hot = hot_industries(rows)
    shapes['theme_smallmid'] = sorted(
        (r for r in rows if r['tier'] == THEME_TIER and r['rs_pct'] >= br.P['theme_rs_pct']
         and r['above_40w'] and r.get('sector') in hot),
        key=lambda r: -r['rs_pct'])
    return shapes, hot


def industries(tickers, pool_stocks):
    """ticker → official industry. Pool names carry tw_industry; the rest go
    through the TWSE/TPEx rosters (network; on failure they stay unclassified)."""
    out = {s['ticker']: s.get('tw_industry') for s in pool_stocks if s.get('tw_industry')}
    missing = [t for t in tickers if t not in out]
    if missing:
        try:
            import tw_listing_suffix
            resolved, _ = tw_listing_suffix.resolve_tw_codes(t.split('.')[0] for t in missing)
            for t in missing:
                ind = (resolved.get(t.split('.')[0]) or {}).get('industry')
                if ind:
                    out[t] = ind
        except Exception as e:  # noqa: BLE001 — industry is display + hot ranking only
            print(f"  WARN: industry lookup failed ({type(e).__name__}: {e})", file=sys.stderr)
    return out


def _pct(v):
    return '<span class="bw-muted">—</span>' if v is None else f'{v:+.0f}%'


def _table(rows):
    head = ('<tr><th class="bw-l">代號／名稱</th><th class="bw-l">產業</th><th class="bw-l">指數</th>'
            '<th>12 個月</th><th>13 週</th><th title="離 25 個月內最高週收盤">距高點</th>'
            '<th title="最高點到現在幾週">基期</th><th title="近 12 個月漲幅在雷達名單裡的百分位">RS</th>'
            '<th class="bw-l">台股池</th></tr>')
    body = []
    for r in rows:
        code = escape(r['ticker'].split('.')[0])
        label = f"{code} {escape(r['name'])}" if r.get('name') else code
        pool = ('<span class="bw-pill bw-pill-accent">池內</span>' if r.get('in_pool')
                else '<span class="bw-pill bw-pill-mut">池外</span>')
        body.append(f'<tr><td class="bw-l"><strong>{label}</strong></td>'
                    f'<td class="bw-l">{escape(r.get("sector") or "—")}</td>'
                    f'<td class="bw-l">{escape(TIER_LABEL.get(r.get("tier"), "—"))}</td>'
                    f'<td>{_pct(r["ret_12m"])}</td><td>{_pct(r["ret_13w"])}</td>'
                    f'<td>{_pct(r["dist_ath"])}</td><td>{r["base_age_w"]} 週</td>'
                    f'<td>{r["rs_pct"]:.0f}</td><td class="bw-l">{pool}</td></tr>')
    return ('<div class="bw-scroll"><table><thead>' + head + '</thead><tbody>'
            + ''.join(body) + '</tbody></table></div>')


def render(payload):
    top = br.P['display_top_n']
    cards = []
    for key, (label, desc) in SHAPE_TEXT.items():
        rows = payload['shapes'][key]
        n = payload['shape_counts'][key]
        blind = sum(1 for r in rows if not r.get('in_pool'))
        shown = f"，列前 {top}" if n > top else ''
        cards.append(f'<h3 class="bw-sec">{label}（{n} 檔{shown}；池外 {blind}）</h3>'
                     f'<div class="bw-sub">{escape(desc)}</div>'
                     + (_table(rows[:top]) if rows else '<div class="bw-note-line">這週沒有符合的名字。</div>'))
    hot = '、'.join(payload['hot_industries']) or '（無）'
    excl = (f"{'、'.join(payload['excluded_industries'])} {payload['excluded_n']} 檔算進 RS 的比較對象，"
            "但不列出、不參加熱產業排名，因為台股池不收。" if payload.get('excluded_n') else "")
    return (
        '<div class="board-wrap">' + _BOARD_CSS
        + f'<div class="bw-head">台股全市場雷達 · {escape(payload["as_of"])} 起那一週的週收盤 · '
          f'{payload["scored_n"]} 檔</div>'
        + '<div class="bw-rule">四種形狀每週六（台北）依週五收盤掃一次，門檻跟美股雷達相同。'
          '名單是用來找名字的，不是買進名單：池外的名字要先補 DD，進場仍看上面的時機燈。</div>'
        + f'<div class="bw-note-line">掃描範圍：0050、0051、006201 成分股加台股池，共 {payload["universe_n"]} 檔，'
          f'其中 {payload["scored_n"]} 檔有 56 週以上的週線可以算。高點取近 25 個月的最高週收盤。'
          f'RS 百分位是近 12 個月漲幅在這 {payload["scored_n"]} 檔裡贏過幾成，0 到 100。{excl}</div>'
        + '<div class="bw-note-line">跟美股雷達不同的地方：沒有分析師上修欄，也沒有「三閘主榜」，'
          '台股的上修數字要等第三季財報後的 Koyfin 快照。「主題下沉」用 0051 成分股代替美股的 S&amp;P 400 中型股。'
          f'產業用證交所／櫃買中心產業別，名單裡少於 {HOT_MIN_MEMBERS} 檔的產業不列入熱產業。</div>'
        + ''.join(cards)
        + f'<div class="bw-note-line">熱產業（近 13 週報酬中位數前 {br.P["theme_hot_sectors"]} 名）：'
          f'{escape(hot)}。一檔可以同時符合幾種形狀。</div>'
        + '</div>'
    )


def build(closes=None):
    tickers, sizes, names = build_stages_tw.universe_with_names()
    wl = screener_tw.build_watchlist()
    try:
        pool_stocks = json.loads(TW_POOL_JSON.read_text(encoding='utf-8')).get('stocks') or []
    except (OSError, json.JSONDecodeError):
        pool_stocks = []
    pool = {s['ticker'] for s in pool_stocks}
    closes = download(tickers) if closes is None else closes
    rows, as_of = structure(closes)
    if len(rows) < MIN_SCORED_SHARE * len(tickers):
        print(f"  ✗ radar-tw: only {len(rows)}/{len(tickers)} names have {MIN_WEEKS}+ weekly bars "
              "— files left unchanged", file=sys.stderr)
        return None
    ind = industries([r['ticker'] for r in rows], pool_stocks)
    for r in rows:
        t = r['ticker']
        r.update(name=names.get(t), sector=ind.get(t) or '', tier=(wl.get(t) or {}).get('etf') or 'pool',
                 in_pool=t in pool)
    # rs_pct is already set against every scored name; only listing and the
    # hot-industry ranking drop the excluded industries
    listed = [r for r in rows if r['sector'] not in TW_EXCLUDED_INDUSTRIES]
    shapes, hot = tag(listed)
    counts = {k: len(v) for k, v in shapes.items()}
    payload = {
        'schema_version': 'radar-tw-1',
        'run_timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'as_of': as_of, 'as_of_note': 'yfinance labels a weekly bar with the Monday it starts',
        'universe_n': len(tickers), 'scored_n': len(rows), 'universe': sizes,
        'excluded_industries': sorted(TW_EXCLUDED_INDUSTRIES), 'excluded_n': len(rows) - len(listed),
        'params': {**br.P, 'hot_min_members': HOT_MIN_MEMBERS, 'theme_tier': THEME_TIER},
        'hot_industries': hot, 'shape_counts': counts,
        'blind_total': len({r['ticker'] for v in shapes.values() for r in v if not r['in_pool']}),
        'shapes': {k: v[:br.P['display_top_n'] * 2] for k, v in shapes.items()},
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RADAR_TW_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    RADAR_TW_HTML.write_text(render(payload), encoding='utf-8')
    print(f"  ✓ radar-tw {as_of}: scored {len(rows)}/{len(tickers)}, shapes {counts}, hot {hot}")
    return payload


def main():
    try:
        build()
    except Exception as e:  # noqa: BLE001 — weekly display job; never fail the workflow
        print(f"  ✗ radar-tw build failed ({type(e).__name__}: {e}) — files left unchanged")
        print(f"::warning::radar-tw build failed ({type(e).__name__}: {e})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
