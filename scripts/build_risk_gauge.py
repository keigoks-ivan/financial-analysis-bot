"""
Risk-On / Risk-Off composite gauge — markets.html section + homepage chart data.

Six market-based signals, each scored +1 (risk-on) / 0 (neutral) / -1 (risk-off):
  1. Equity trend      — S&P 500 vs 200DMA + 200DMA slope
  2. Volatility        — VIX level + VIX/VIX3M term structure
  3. Credit appetite   — HYG vs IEF 63-day relative return (adjusted, incl. dividends)
  4. Cyclical vs haven — Copper (HG=F) vs Gold (GC=F) 63-day relative return
  5. Offense/defense   — XLY vs XLP 63-day relative return
  6. FX carry          — AUD/JPY vs 200DMA + 63-day direction

Composite = mean of available component scores (>=4 required), 5-level label.
Scoring is computed VECTORIZED over full history so the live reading and the
homepage chart share one implementation (thresholds frozen; backtested 2026-07,
see transcripts — useful as risk description, not as a mechanical timing signal).

Outputs:
  - bilingual gauge section injected into docs/markets.html
    between <!-- RISK_GAUGE:START --> / <!-- RISK_GAUGE:END -->
  - docs/cache/risk_gauge.json     (current reading + 52-week history)
  - docs/cache/risk_history.json   (weekly score/SPX/NFCI since 2004 for the
                                    homepage interactive chart)

NFCI (Chicago Fed, FRED free CSV) is fetched best-effort; on failure the
previous NFCI history is reused so the chart degrades gracefully.

Runs in the weekly-market-update GitHub Actions workflow (Sat 00:00 UTC).
"""

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
MARKETS_HTML = ROOT / 'docs' / 'markets.html'
GAUGE_JSON = ROOT / 'docs' / 'cache' / 'risk_gauge.json'
HISTORY_JSON = ROOT / 'docs' / 'cache' / 'risk_history.json'

MARKER_START = '<!-- RISK_GAUGE:START -->'
MARKER_END = '<!-- RISK_GAUGE:END -->'

TICKERS = ['^GSPC', '^VIX', '^VIX3M', 'HYG', 'IEF', 'XLY', 'XLP',
           'HG=F', 'GC=F', 'AUDJPY=X']
NFCI_URL = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=NFCI'

LOOKBACK_63D = 63   # ~3 months of trading days


def fetch_closes():
    """Full-history adjusted daily closes per ticker (native calendars, NaN gaps)."""
    data = yf.download(TICKERS, period='max', interval='1d', auto_adjust=True,
                       group_by='ticker', progress=False, threads=True)
    px = pd.DataFrame()
    for t in TICKERS:
        try:
            px[t] = data[t]['Close']
        except Exception:
            px[t] = np.nan
    px = px.sort_index()
    if px.index.tz is not None:
        px.index = px.index.tz_localize(None)
    return px


def fetch_nfci():
    """Weekly NFCI from FRED; None on any failure."""
    try:
        import requests
        csv = requests.get(NFCI_URL, timeout=60).text
        s = pd.read_csv(io.StringIO(csv), parse_dates=[0], index_col=0).iloc[:, 0]
        s = pd.to_numeric(s, errors='coerce').dropna()
        return s if len(s) > 100 else None
    except Exception as e:
        print(f"  ⚠ NFCI fetch failed: {e}")
        return None


def band(s, w):
    return pd.Series(np.where(s > w, 1, np.where(s < -w, -1, 0)),
                     index=s.index).where(s.notna())


def calc_components(px):
    """Each component scored on its own native trading calendar (same semantics
    as computing per-ticker at 'today'), full history.

    Returns (scores_df on union index, comps list for the markets.html chips).
    Chip values = last point of the exact same series that produce the scores.
    """
    score_series = {}
    comps = []

    def last(s):
        s = s.dropna()
        return float(s.iloc[-1]) if len(s) else None

    def add(key, name_en, name_zh, s_score, value_en, value_zh):
        score_series[key] = s_score
        v = last(s_score)
        comps.append(dict(key=key, name_en=name_en, name_zh=name_zh,
                          value_en=value_en, value_zh=value_zh,
                          score=None if v is None else int(v)))

    # 1. Equity trend — S&P 500 vs 200DMA (native SPX days)
    spx = px['^GSPC'].dropna()
    ma200 = spx.rolling(200).mean()
    s = pd.Series(np.where((spx > ma200) & (ma200 > ma200.shift(22)), 1,
                           np.where(spx < ma200, -1, 0)),
                  index=spx.index).where(ma200.notna())
    gap = last((spx / ma200 - 1) * 100)
    add('trend', 'Equity trend', '股指趨勢', s,
        'n/a' if gap is None else f"S&P 500 {gap:+.1f}% vs 200DMA",
        'n/a' if gap is None else f"標普500 對200日線 {gap:+.1f}%")

    # 2. Volatility — VIX level + term structure (VIX3M aligned to VIX days)
    vix = px['^VIX'].dropna()
    v3 = px['^VIX3M'].dropna().reindex(vix.index).ffill(limit=10)
    with_ts = np.where((vix >= 24) | (vix > v3), -1,
                       np.where((vix < 17) & (vix < v3), 1, 0))
    no_ts = np.where(vix >= 24, -1, np.where(vix < 17, 1, 0))
    s = pd.Series(np.where(v3.notna(), with_ts, no_ts), index=vix.index)
    v, v3l = last(vix), last(v3)
    if v is None:
        val_en = val_zh = 'n/a'
    else:
        contango = v3l is not None and v < v3l
        backward = v3l is not None and v > v3l
        ts_en = ' · contango' if contango else (' · backwardation' if backward else '')
        ts_zh = '，期限結構正價差' if contango else ('，期限結構逆價差' if backward else '')
        val_en, val_zh = f"VIX {v:.1f}{ts_en}", f"VIX {v:.1f}{ts_zh}"
    add('vol', 'Volatility', '波動率', s, val_en, val_zh)

    # 3-5. Pairwise 63-day relative returns (inner-joined native calendars)
    for key, a, b, w, ne, nz, fe, fz in [
        ('credit', 'HYG', 'IEF', 1.0, 'Credit appetite', '信用偏好',
         'HYG−IEF 3M {v:+.1f}%', 'HYG−IEF 三個月相對 {v:+.1f}%'),
        ('commod', 'HG=F', 'GC=F', 3.0, 'Copper / Gold', '銅金比',
         'Copper−Gold 3M {v:+.1f}%', '銅−金 三個月相對 {v:+.1f}%'),
        ('sector', 'XLY', 'XLP', 2.0, 'Offense / defense', '攻守類股',
         'XLY−XLP 3M {v:+.1f}%', '可選消費−必需 三個月 {v:+.1f}%'),
    ]:
        pair = pd.concat([px[a], px[b]], axis=1, join='inner').dropna()
        sa, sb = pair.iloc[:, 0], pair.iloc[:, 1]
        rr = ((sa / sa.shift(LOOKBACK_63D) - 1) - (sb / sb.shift(LOOKBACK_63D) - 1)) * 100
        v = last(rr)
        add(key, ne, nz, band(rr, w),
            'n/a' if v is None else fe.format(v=v),
            'n/a' if v is None else fz.format(v=v))

    # 6. FX carry — AUD/JPY vs 200DMA (native FX days)
    aj = px['AUDJPY=X'].dropna()
    ajma = aj.rolling(200).mean()
    ajr = (aj / aj.shift(LOOKBACK_63D) - 1) * 100
    s = pd.Series(np.where((aj > ajma) & (ajr > 0), 1,
                           np.where((aj < ajma) & (ajr < 0), -1, 0)),
                  index=aj.index).where(ajma.notna() & ajr.notna())
    gap = last((aj / ajma - 1) * 100)
    add('fx', 'FX carry', '套息貨幣', s,
        'n/a' if gap is None else f"AUD/JPY {gap:+.1f}% vs 200DMA",
        'n/a' if gap is None else f"澳幣兌日圓 對200日線 {gap:+.1f}%")

    # union calendar; a score computed on its own last trading day persists
    # up to 5 sessions so mixed holidays don't drop components
    sc = pd.DataFrame(score_series).sort_index().ffill(limit=5)
    return sc, comps


def composite_label(score):
    """Map composite score [-1, +1] to (label_en, label_zh, color)."""
    if score >= 0.67:
        return 'STRONG RISK-ON', '強風險偏好', 'var(--pos)'
    if score >= 0.34:
        return 'RISK-ON', '風險偏好', 'var(--pos)'
    if score <= -0.67:
        return 'STRONG RISK-OFF', '強風險趨避', 'var(--neg)'
    if score <= -0.34:
        return 'RISK-OFF', '風險趨避', 'var(--neg)'
    return 'NEUTRAL', '中性', 'var(--warn)'


def render_block(score, label_en, label_zh, color, comps, as_of, prev):
    """Render the injectable HTML section (bilingual, self-contained styles)."""
    pos = (score + 1) / 2 * 100  # needle position 0-100

    chips = []
    for c in comps:
        if c['score'] is None:
            dot, dot_color, chip_bg = '–', 'var(--muted)', 'var(--line-soft)'
        elif c['score'] > 0:
            dot, dot_color, chip_bg = '▲', 'var(--pos)', '#eaf5ef'
        elif c['score'] < 0:
            dot, dot_color, chip_bg = '▼', 'var(--neg)', '#faecea'
        else:
            dot, dot_color, chip_bg = '●', 'var(--warn)', '#f8f1e2'
        chips.append(
            f'<div class="rg-chip" style="background:{chip_bg}">'
            f'<div class="rg-chip-top"><span style="color:{dot_color}">{dot}</span>'
            f'<span class="rg-chip-name"><span class="lang-en">{c["name_en"]}</span>'
            f'<span class="lang-zh">{c["name_zh"]}</span></span></div>'
            f'<div class="rg-chip-val"><span class="lang-en">{c["value_en"]}</span>'
            f'<span class="lang-zh">{c["value_zh"]}</span></div></div>')

    prev_html = ''
    if prev:
        arrow = '→'
        if score > prev['score'] + 0.01:
            arrow = '↑'
        elif score < prev['score'] - 0.01:
            arrow = '↓'
        prev_html = (f'<div class="rg-prev"><span class="lang-en">Prev week: '
                     f'{prev["label_en"]} ({prev["score"]:+.2f}) {arrow}</span>'
                     f'<span class="lang-zh">上週：{prev["label_zh"]}（{prev["score"]:+.2f}）{arrow}</span></div>')

    return f'''{MARKER_START}
<section style="background:var(--paper)">
  <div class="section" style="padding-bottom:0">
    <style>
    .rg-card{{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px 24px}}
    .rg-head{{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:14px}}
    .rg-label{{font-size:22px;font-weight:700;letter-spacing:.04em}}
    .rg-score{{font-size:13px;color:var(--sec);font-variant-numeric:tabular-nums}}
    .rg-prev{{font-size:11px;color:var(--muted)}}
    .rg-bar-wrap{{position:relative;height:10px;border-radius:5px;margin:6px 2px 22px;
      background:linear-gradient(90deg,var(--neg) 0%,#f59e0b 40%,var(--line) 50%,#84cc16 60%,var(--pos) 100%)}}
    .rg-needle{{position:absolute;top:-5px;width:4px;height:20px;background:var(--ink);border-radius:2px;transform:translateX(-50%)}}
    .rg-bar-lbl{{position:absolute;top:14px;font-size:9px;letter-spacing:.08em;color:var(--muted);font-weight:600}}
    .rg-chips{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px}}
    .rg-chip{{border:1px solid var(--line);border-radius:var(--r);padding:8px 10px}}
    .rg-chip-top{{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:600;color:var(--ink)}}
    .rg-chip-val{{font-size:10px;color:var(--sec);margin-top:3px;font-variant-numeric:tabular-nums}}
    .rg-note{{font-size:10px;color:var(--muted);margin-top:12px;line-height:1.5}}
    </style>
    <div class="section-hdr" style="margin-bottom:12px">
      <span class="section-title lang-en">RISK ON / RISK OFF GAUGE</span>
      <span class="section-title lang-zh">風險偏好儀表</span>
      <span class="section-desc lang-en">6 market-based signals · updated {as_of}</span>
      <span class="section-desc lang-zh">六個市場訊號綜合 · 更新於 {as_of}</span>
    </div>
    <div class="rg-card">
      <div class="rg-head">
        <span class="rg-label" style="color:{color}"><span class="lang-en">{label_en}</span><span class="lang-zh">{label_zh}</span></span>
        <span class="rg-score"><span class="lang-en">composite {score:+.2f} (−1 ~ +1)</span><span class="lang-zh">綜合分數 {score:+.2f}（−1 ~ +1）</span></span>
        {prev_html}
      </div>
      <div class="rg-bar-wrap">
        <div class="rg-needle" style="left:{pos:.1f}%"></div>
        <span class="rg-bar-lbl" style="left:0">RISK-OFF</span>
        <span class="rg-bar-lbl" style="left:50%;transform:translateX(-50%)"><span class="lang-en">NEUTRAL</span><span class="lang-zh">中性</span></span>
        <span class="rg-bar-lbl" style="right:0">RISK-ON</span>
      </div>
      <div class="rg-chips">
        {''.join(chips)}
      </div>
      <div class="rg-note">
        <span class="lang-en">Each signal scores +1 / 0 / −1: S&amp;P 500 vs 200DMA · VIX level &amp; term structure · HYG−IEF 3-month relative return · copper−gold 3-month · XLY−XLP 3-month · AUD/JPY vs 200DMA. Composite = average. Weekly auto-update, same cadence as the table below. Not investment advice.</span>
        <span class="lang-zh">每個訊號各打 +1／0／−1 分：標普500 對200日線、VIX 水位與期限結構、HYG−IEF 三個月相對報酬、銅金比三個月、可選消費−必需消費三個月、澳幣兌日圓對200日線。綜合分數＝六者平均。每週六與下方表格同步自動更新。非投資建議。</span>
      </div>
    </div>
  </div>
</section>
{MARKER_END}'''


def inject(html, block):
    """Replace existing marker block, or insert after the hero section."""
    if MARKER_START in html and MARKER_END in html:
        pre = html.split(MARKER_START)[0]
        post = html.split(MARKER_END)[1]
        return pre + block + post
    hero_close = html.find('</section>', html.find('<section class="hero">'))
    if hero_close == -1:
        raise RuntimeError('cannot locate hero section in markets.html')
    insert_at = hero_close + len('</section>')
    return html[:insert_at] + '\n\n' + block + html[insert_at:]


def main():
    now = datetime.now(timezone.utc)
    as_of = now.strftime('%Y-%m-%d')
    print(f"=== Risk Gauge Build: {as_of} ===")

    px = fetch_closes()
    missing = [t for t in TICKERS if px[t].dropna().empty]
    if missing:
        print(f"  ⚠ missing data for: {', '.join(missing)}")

    sc, comps = calc_components(px)
    avail = sc.notna().sum(axis=1)
    comp_daily = sc.mean(axis=1).where(avail >= 4)
    scored = [c['score'] for c in comps if c['score'] is not None]
    if len(scored) < 4:
        print(f"  ✗ only {len(scored)}/6 components available — aborting, page left unchanged")
        sys.exit(0)

    score = sum(scored) / len(scored)
    label_en, label_zh, color = composite_label(score)
    for c in comps:
        print(f"  {c['name_en']:<18} {c['score'] if c['score'] is not None else 'n/a':>4}  {c['value_en']}")
    print(f"  → composite {score:+.2f} = {label_en}")

    # ── weekly history (homepage chart) ──
    wk_score = comp_daily.resample('W-FRI').last().dropna().round(3)
    wk_spx = px['^GSPC'].resample('W-FRI').last().reindex(wk_score.index).round(2)
    wk_vix = px['^VIX'].resample('W-FRI').last().reindex(wk_score.index).round(2)
    wk_vixhi = px['^VIX'].resample('W-FRI').max().reindex(wk_score.index).round(2)  # intraweek daily-close max, drives the >=40 panic-entry markers
    nfci = fetch_nfci()
    if nfci is not None:
        wk_nfci = nfci.reindex(wk_score.index).ffill(limit=4).round(2)
    elif HISTORY_JSON.exists():
        old = json.loads(HISTORY_JSON.read_text(encoding='utf-8'))
        old_n = pd.Series(old.get('nfci', []),
                          index=pd.to_datetime(old.get('weeks', [])))
        wk_nfci = old_n.reindex(wk_score.index).round(2)
        print("  ⚠ reusing previous NFCI history")
    else:
        wk_nfci = pd.Series(np.nan, index=wk_score.index)

    def _nan_to_none(s):
        return [None if pd.isna(v) else float(v) for v in s]

    HISTORY_JSON.write_text(json.dumps({
        'as_of': as_of,
        'weeks': [d.strftime('%Y-%m-%d') for d in wk_score.index],
        'score': _nan_to_none(wk_score),
        'spx': _nan_to_none(wk_spx),
        'nfci': _nan_to_none(wk_nfci),
        'vix': _nan_to_none(wk_vix),
        'vixhi': _nan_to_none(wk_vixhi),
    }, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {HISTORY_JSON.relative_to(ROOT)} ({len(wk_score)} weeks since {wk_score.index[0].date()})")

    # prev week for the markets.html block
    prev = None
    if len(wk_score) >= 2:
        ps = float(wk_score.iloc[-2])
        pl_en, pl_zh, _ = composite_label(ps)
        prev = {'score': ps, 'label_en': pl_en, 'label_zh': pl_zh}

    # ── current-reading JSON (52-week rolling history, append style) ──
    state = {'history': []}
    if GAUGE_JSON.exists():
        try:
            state = json.loads(GAUGE_JSON.read_text(encoding='utf-8'))
        except Exception:
            pass
    history = [h for h in state.get('history', []) if h.get('date') != as_of]
    history.append({'date': as_of, 'score': round(score, 3),
                    'label_en': label_en, 'label_zh': label_zh})
    payload = {
        'as_of': as_of,
        'score': round(score, 3),
        'label_en': label_en, 'label_zh': label_zh,
        'components': [{k: c[k] for k in ('key', 'name_en', 'name_zh', 'value_en', 'value_zh', 'score')}
                       for c in comps],
        'history': history[-52:],
    }
    GAUGE_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {GAUGE_JSON.relative_to(ROOT)}")

    # ── inject into markets.html ──
    html = MARKETS_HTML.read_text(encoding='utf-8')
    block = render_block(score, label_en, label_zh, color, comps, as_of, prev)
    new_html = inject(html, block)
    if new_html != html:
        MARKETS_HTML.write_text(new_html, encoding='utf-8')
        print(f"  ✓ injected gauge into {MARKETS_HTML.relative_to(ROOT)}")
    else:
        print("  – markets.html unchanged")


if __name__ == '__main__':
    main()
