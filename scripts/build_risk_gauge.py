"""
Risk-On / Risk-Off composite gauge for markets.html

Six market-based signals, each scored +1 (risk-on) / 0 (neutral) / -1 (risk-off):
  1. Equity trend      — S&P 500 vs 200DMA + 200DMA slope
  2. Volatility        — VIX level + VIX/VIX3M term structure
  3. Credit appetite   — HYG vs IEF 63-day relative return (adjusted, incl. dividends)
  4. Cyclical vs haven — Copper (HG=F) vs Gold (GC=F) 63-day relative return
  5. Offense/defense   — XLY vs XLP 63-day relative return
  6. FX carry          — AUD/JPY vs 200DMA + 63-day direction

Composite = mean of available component scores, mapped to a 5-level label.
Outputs:
  - injects a bilingual gauge section into docs/markets.html
    between <!-- RISK_GAUGE:START --> / <!-- RISK_GAUGE:END --> markers
  - writes docs/cache/risk_gauge.json (with 52-week history)

Runs in the weekly-market-update GitHub Actions workflow (Sat 00:00 UTC),
same cadence as update_markets.py. Safe to run locally.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

ROOT = Path(__file__).resolve().parent.parent
MARKETS_HTML = ROOT / 'docs' / 'markets.html'
GAUGE_JSON = ROOT / 'docs' / 'cache' / 'risk_gauge.json'

MARKER_START = '<!-- RISK_GAUGE:START -->'
MARKER_END = '<!-- RISK_GAUGE:END -->'

TICKERS = ['^GSPC', '^VIX', '^VIX3M', 'HYG', 'IEF', 'XLY', 'XLP',
           'HG=F', 'GC=F', 'AUDJPY=X']

LOOKBACK_63D = 63   # ~3 months of trading days


def fetch_closes():
    """Batch-download 2y adjusted daily closes; return {ticker: pd.Series}."""
    data = yf.download(TICKERS, period='2y', interval='1d', auto_adjust=True,
                       group_by='ticker', progress=False, threads=True)
    closes = {}
    for t in TICKERS:
        try:
            s = data[t]['Close'].dropna()
            if len(s) >= 20:
                closes[t] = s
        except Exception:
            pass
    return closes


def rel_return_63d(a, b):
    """63-trading-day return of a minus that of b, in %; None if insufficient."""
    if a is None or b is None:
        return None
    if len(a) < LOOKBACK_63D + 1 or len(b) < LOOKBACK_63D + 1:
        return None
    ra = (a.iloc[-1] / a.iloc[-(LOOKBACK_63D + 1)] - 1) * 100
    rb = (b.iloc[-1] / b.iloc[-(LOOKBACK_63D + 1)] - 1) * 100
    return ra - rb


def band_score(value, band):
    """+1 above +band, -1 below -band, 0 inside."""
    if value is None:
        return None
    if value > band:
        return 1
    if value < -band:
        return -1
    return 0


def build_components(closes):
    """Return list of component dicts: key, name_en, name_zh, value_en, value_zh, score."""
    comps = []

    # 1. Equity trend — S&P 500 vs 200DMA
    spx = closes.get('^GSPC')
    score = None
    val_en = val_zh = 'n/a'
    if spx is not None and len(spx) >= 221:
        ma200 = spx.rolling(200).mean()
        px, ma = spx.iloc[-1], ma200.iloc[-1]
        gap = (px / ma - 1) * 100
        slope_up = ma200.iloc[-1] > ma200.iloc[-22]
        if px > ma and slope_up:
            score = 1
        elif px < ma:
            score = -1
        else:
            score = 0
        val_en = f"S&P 500 {gap:+.1f}% vs 200DMA"
        val_zh = f"標普500 對200日線 {gap:+.1f}%"
    comps.append(dict(key='trend', name_en='Equity trend', name_zh='股指趨勢',
                      value_en=val_en, value_zh=val_zh, score=score))

    # 2. Volatility — VIX level + term structure
    vix, vix3m = closes.get('^VIX'), closes.get('^VIX3M')
    score = None
    val_en = val_zh = 'n/a'
    if vix is not None:
        v = vix.iloc[-1]
        v3 = vix3m.iloc[-1] if vix3m is not None else None
        contango = (v3 is not None and v < v3)
        backwardation = (v3 is not None and v > v3)
        if v >= 24 or backwardation:
            score = -1
        elif v < 17 and (v3 is None or contango):
            score = 1
        else:
            score = 0
        ts_en = ' · contango' if contango else (' · backwardation' if backwardation else '')
        ts_zh = '，期限結構正價差' if contango else ('，期限結構逆價差' if backwardation else '')
        val_en = f"VIX {v:.1f}{ts_en}"
        val_zh = f"VIX {v:.1f}{ts_zh}"
    comps.append(dict(key='vol', name_en='Volatility', name_zh='波動率',
                      value_en=val_en, value_zh=val_zh, score=score))

    # 3. Credit appetite — HYG vs IEF, 63d relative return, ±1% band
    rr = rel_return_63d(closes.get('HYG'), closes.get('IEF'))
    comps.append(dict(key='credit', name_en='Credit appetite', name_zh='信用偏好',
                      value_en=('n/a' if rr is None else f"HYG−IEF 3M {rr:+.1f}%"),
                      value_zh=('n/a' if rr is None else f"HYG−IEF 三個月相對 {rr:+.1f}%"),
                      score=band_score(rr, 1.0)))

    # 4. Cyclical vs haven — Copper vs Gold, 63d relative return, ±3% band
    rr = rel_return_63d(closes.get('HG=F'), closes.get('GC=F'))
    comps.append(dict(key='commod', name_en='Copper / Gold', name_zh='銅金比',
                      value_en=('n/a' if rr is None else f"Copper−Gold 3M {rr:+.1f}%"),
                      value_zh=('n/a' if rr is None else f"銅−金 三個月相對 {rr:+.1f}%"),
                      score=band_score(rr, 3.0)))

    # 5. Offense / defense — XLY vs XLP, 63d relative return, ±2% band
    rr = rel_return_63d(closes.get('XLY'), closes.get('XLP'))
    comps.append(dict(key='sector', name_en='Offense / defense', name_zh='攻守類股',
                      value_en=('n/a' if rr is None else f"XLY−XLP 3M {rr:+.1f}%"),
                      value_zh=('n/a' if rr is None else f"可選消費−必需 三個月 {rr:+.1f}%"),
                      score=band_score(rr, 2.0)))

    # 6. FX carry — AUD/JPY vs 200DMA + 63d direction
    aj = closes.get('AUDJPY=X')
    score = None
    val_en = val_zh = 'n/a'
    if aj is not None and len(aj) >= 200 + 1:
        ma200 = aj.rolling(200).mean().iloc[-1]
        px = aj.iloc[-1]
        r63 = (px / aj.iloc[-(LOOKBACK_63D + 1)] - 1) * 100 if len(aj) > LOOKBACK_63D else 0
        above = px > ma200
        if above and r63 > 0:
            score = 1
        elif not above and r63 < 0:
            score = -1
        else:
            score = 0
        gap = (px / ma200 - 1) * 100
        val_en = f"AUD/JPY {gap:+.1f}% vs 200DMA"
        val_zh = f"澳幣兌日圓 對200日線 {gap:+.1f}%"
    comps.append(dict(key='fx', name_en='FX carry', name_zh='套息貨幣',
                      value_en=val_en, value_zh=val_zh, score=score))

    return comps


def composite_label(score):
    """Map composite score [-1, +1] to (label_en, label_zh, color)."""
    if score >= 0.67:
        return 'STRONG RISK-ON', '強風險偏好', '#16a34a'
    if score >= 0.34:
        return 'RISK-ON', '風險偏好', '#16a34a'
    if score <= -0.67:
        return 'STRONG RISK-OFF', '強風險趨避', '#dc2626'
    if score <= -0.34:
        return 'RISK-OFF', '風險趨避', '#dc2626'
    return 'NEUTRAL', '中性', '#d97706'


def render_block(score, label_en, label_zh, color, comps, as_of, prev):
    """Render the injectable HTML section (bilingual, self-contained styles)."""
    pos = (score + 1) / 2 * 100  # needle position 0-100

    chips = []
    for c in comps:
        if c['score'] is None:
            dot, dot_color, chip_bg = '–', '#94a3b8', '#f1f5f9'
        elif c['score'] > 0:
            dot, dot_color, chip_bg = '▲', '#16a34a', '#f0fdf4'
        elif c['score'] < 0:
            dot, dot_color, chip_bg = '▼', '#dc2626', '#fef2f2'
        else:
            dot, dot_color, chip_bg = '●', '#d97706', '#fffbeb'
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
<section style="background:#f0f5fb">
  <div class="section" style="padding-bottom:0">
    <style>
    .rg-card{{background:#fff;border:1px solid #dce8f5;border-radius:12px;padding:20px 24px}}
    .rg-head{{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:14px}}
    .rg-label{{font-size:22px;font-weight:700;letter-spacing:.04em}}
    .rg-score{{font-size:13px;color:#5a7a9a;font-variant-numeric:tabular-nums}}
    .rg-prev{{font-size:11px;color:#94a3b8}}
    .rg-bar-wrap{{position:relative;height:10px;border-radius:5px;margin:6px 2px 22px;
      background:linear-gradient(90deg,#dc2626 0%,#f59e0b 40%,#e2e8f0 50%,#84cc16 60%,#16a34a 100%)}}
    .rg-needle{{position:absolute;top:-5px;width:4px;height:20px;background:#0f2a45;border-radius:2px;transform:translateX(-50%)}}
    .rg-bar-lbl{{position:absolute;top:14px;font-size:9px;letter-spacing:.08em;color:#94a3b8;font-weight:600}}
    .rg-chips{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px}}
    .rg-chip{{border:1px solid #e2e8f0;border-radius:8px;padding:8px 10px}}
    .rg-chip-top{{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:600;color:#1e3a5f}}
    .rg-chip-val{{font-size:10px;color:#5a7a9a;margin-top:3px;font-variant-numeric:tabular-nums}}
    .rg-note{{font-size:10px;color:#94a3b8;margin-top:12px;line-height:1.5}}
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

    closes = fetch_closes()
    missing = [t for t in TICKERS if t not in closes]
    if missing:
        print(f"  ⚠ missing data for: {', '.join(missing)}")

    comps = build_components(closes)
    scored = [c['score'] for c in comps if c['score'] is not None]
    if len(scored) < 4:
        print(f"  ✗ only {len(scored)}/6 components available — aborting, page left unchanged")
        sys.exit(0)

    score = sum(scored) / len(scored)
    label_en, label_zh, color = composite_label(score)
    for c in comps:
        print(f"  {c['name_en']:<18} {c['score'] if c['score'] is not None else 'n/a':>4}  {c['value_en']}")
    print(f"  → composite {score:+.2f} = {label_en}")

    # ── JSON with history ──
    state = {'history': []}
    if GAUGE_JSON.exists():
        try:
            state = json.loads(GAUGE_JSON.read_text(encoding='utf-8'))
        except Exception:
            pass
    history = [h for h in state.get('history', []) if h.get('date') != as_of]
    prev = history[-1] if history else None
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

    # ── Inject into markets.html ──
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
