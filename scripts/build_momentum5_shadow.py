"""
Momentum-5 SHADOW TRACK builder — 90D vs 30D revision-window mechanical A/B.

WHAT THIS IS
------------
A pre-registered (PREREG, frozen 2026-08-20), fully mechanical shadow
experiment that rides alongside the human-curated Momentum-5 portfolio. It
does NOT touch portfolio.json, data.json, or the frozen composite in
build_momentum5.py. It reads the full-universe raw factor dump
(docs/research/momentum-5/raw_factors.json, written by build_momentum5.py)
and runs TWO purely mechanical top-5 lines on the SAME data:

  line C (control) : frozen composite exactly as-is (rev_avg = 90-day window).
  line F (fresh)   : ONLY the revision factor changed to the 30-day window
                     (rev30_fy1/rev30_fy2 average) — both in the composite's
                     rev term AND in the rev_avg<=0 veto. Everything else
                     (weights, other two factors, other vetoes, universe,
                     winsorize/z) is byte-identical to line C's logic.

Purpose: test whether "freshest revision wins" (30D window) beats the
portfolio's current 90D window, in a clean, deterministic, cost-free,
equal-weight, monthly-rebalance paper track. Full spec lives in the
"prereg" block of shadow.json (verbatim, do not edit outside of the
2026-11-22 review point below).

Review point: 2026-11-22 (first successful weekly update on/after this date)
— human review of cumulative return & max drawdown, F vs C vs SPY. F wins ->
monthly-review process to consider promoting the rule. F loses -> record and
close, no re-tuning, no re-adding the loser (anti p-hacking).

MECHANICS
---------
- Universe & vetoes: identical structure to build_momentum5.py, just with
  the 90D/30D swap for line F's rev_avg.
- Equal weight, 5 seats, inception 2026-08-20.
- Rebalance: mechanical, on the first successful weekly update day of each
  calendar month (whole-month buy & hold otherwise).
- NAV: paper NAV, marked at each week's close. No transaction costs (both
  lines identical assumption, so the A/B comparison stays fair).
- Ties: broken by ticker alphabetical order (deterministic).
- Exclusions: tickers missing eps_trend data are excluded (same as the main
  script — they never entered raw_factors.json's universe in the first
  place, since that dump is sourced from the main script's post-dropna
  frame).

All state (holdings, nav_series, rebalance_history, changelog, prereg spec)
lives in docs/research/momentum-5/raw_factors.json's sibling,
docs/research/momentum-5/shadow.json.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_FACTORS_JSON = ROOT / 'docs' / 'research' / 'momentum-5' / 'raw_factors.json'
SHADOW_JSON = ROOT / 'docs' / 'research' / 'momentum-5' / 'shadow.json'
DATA_JSON = ROOT / 'docs' / 'research' / 'momentum-5' / 'data.json'

# ── frozen thresholds — MUST mirror build_momentum5.py exactly (do not tune) ──
CLIP_LO, CLIP_HI = 0.02, 0.98
W_REV, W_MOM, W_GROWTH = 0.5, 0.3, 0.2
VETO_RET12 = 2.5
N_SEATS = 5
WEIGHT_PCT = 100.0 / N_SEATS
SANITY_TOL = 0.01

PREREG = {
    "title": "影子對照實驗：財報後新鮮上修優先（30 天修正窗）vs 現行 90 天窗",
    "frozen_date": "2026-08-20",
    "objective": "檢定「財報後新鮮上修優先（30 天修正窗）」是否優於現行 90 天窗。",
    "design": (
        "兩條純機械線，同一天同一份原始資料："
        "line C（control）：現行凍結公式原樣（rev_avg＝90d 窗），全 universe 過否決後取 composite 前 5 名。"
        "line F（fresh）：唯一改動——凡用到修正因子之處（composite 的 rev 項＋rev_avg≤0 否決）"
        "一律改用 30d 窗（rev30_fy1/rev30_fy2 平均）；其餘完全相同。"
    ),
    "portfolio_rules": {
        "weighting": "等權 5 席",
        "inception": "2026-08-20",
        "rebalance": "每月第一個成功週更日機械換倉（整月持有不動）",
        "nav_update": "紙上 NAV 以每週 close 更新",
        "transaction_cost": "無交易成本（兩線一致，公平比較）",
        "tie_break": "分數同分以 ticker 字母序決勝（確保 deterministic）",
        "exclusion": "缺 eps_trend 的股票排除（同主腳本）",
    },
    "review": {
        "date": "2026-11-22",
        "trigger": "2026-11-22 起的第一次週更後由持有人人工評審",
        "metrics": ["累積報酬", "最大回撤", "對比另一線與 SPY"],
        "outcome_rule": (
            "F 勝→走月度複審流程再議升級正式規則；"
            "F 敗→記錄結案，不回頭調參、不加回（防參數擇優滑坡）。"
        ),
    },
    "disclosure": (
        "誠實標注：機械線與主組合（人工判斷選席）不可直接比較；"
        "本實驗只隔離「修正窗口新舊」一個變數。紙上、無交易成本、機械式、"
        "非投資建議。"
    ),
}


def z(s):
    s = s.astype(float).clip(s.quantile(CLIP_LO), s.quantile(CLIP_HI))
    return (s - s.mean()) / s.std()


def build_line(df, window):
    """window: '90' -> rev_fy1/rev_fy2 ; '30' -> rev30_fy1/rev30_fy2.

    Returns (scored_univ_df, eligible_sorted_df) using the frozen composite
    structure, differing ONLY in which revision columns feed rev_avg.
    """
    rev_cols = ('rev_fy1', 'rev_fy2') if window == '90' else ('rev30_fy1', 'rev30_fy2')
    d = df.copy()
    d['rev_avg'] = d[list(rev_cols)].astype(float).mean(axis=1, skipna=True)

    univ = d.dropna(subset=['rev_avg', 'growth', 'relmom6']).copy()
    univ['score'] = (W_REV * z(univ['rev_avg'])
                      + W_MOM * z(univ['relmom6'])
                      + W_GROWTH * z(univ['growth']))
    univ['eligible'] = (univ['above200'].astype(bool)
                         & (univ['rev_avg'] > 0)
                         & (univ['ret12'] < VETO_RET12))

    elig = univ[univ['eligible']].copy()
    elig['_tkr_sort'] = elig.index
    elig = elig.sort_values(['score', '_tkr_sort'], ascending=[False, True])
    elig = elig.drop(columns=['_tkr_sort'])
    return univ, elig


def sanity_check_line_c(univ_c):
    """Line C's score, recomputed from raw_factors.json's full universe, must
    match data.json's top20 scores within SANITY_TOL. Returns (ok, detail)."""
    if not DATA_JSON.exists():
        return False, "data.json not found"
    data = json.loads(DATA_JSON.read_text(encoding='utf-8'))
    top20 = data.get('top20', [])
    if not top20:
        return False, "data.json top20 empty"
    mismatches = []
    for row in top20:
        t = row['ticker']
        expected = row['score']
        if t not in univ_c.index:
            mismatches.append(f"{t}: missing from raw_factors universe")
            continue
        got = float(univ_c.at[t, 'score'])
        if abs(got - expected) > SANITY_TOL:
            mismatches.append(f"{t}: data.json={expected} recomputed={got:.4f}")
    if mismatches:
        return False, "; ".join(mismatches)
    return True, f"{len(top20)} top20 scores matched within {SANITY_TOL}"


def load_raw_factors():
    raw = json.loads(RAW_FACTORS_JSON.read_text(encoding='utf-8'))
    as_of = raw['as_of']
    spy_close = float(raw['spy_close'])
    spy6 = float(raw['spy6'])
    rows = raw['universe']
    df = pd.DataFrame(rows).set_index('ticker')
    df['relmom6'] = df['mom6'].astype(float) - spy6
    return as_of, spy_close, df


def price_lookup(df, ticker):
    if ticker in df.index and pd.notna(df.at[ticker, 'price']):
        return float(df.at[ticker, 'price'])
    return None


def make_holdings(elig, df, as_of):
    top5 = elig.head(N_SEATS)
    holdings = []
    for t in top5.index:
        holdings.append({
            'ticker': t,
            'entry_date': as_of,
            'entry_price': round(price_lookup(df, t), 2),
            'score': round(float(top5.at[t, 'score']), 2),
            'weight_pct': WEIGHT_PCT,
        })
    return holdings


def mark_to_market(holdings, df, nav_base):
    """Equal-weight buy&hold NAV since the holding period started."""
    rets = []
    stale = []
    for h in holdings:
        p_now = price_lookup(df, h['ticker'])
        if p_now is None:
            p_now = h.get('last_price', h['entry_price'])
            stale.append(h['ticker'])
        else:
            h['last_price'] = p_now
        rets.append(p_now / h['entry_price'] - 1.0)
    nav = nav_base * (1.0 + sum(rets) / len(rets))
    return nav, stale


def month_of(date_str):
    return date_str[:7]


def main():
    if not RAW_FACTORS_JSON.exists():
        print(f"  ✗ {RAW_FACTORS_JSON} not found — run build_momentum5.py first")
        sys.exit(1)

    as_of, spy_close, df = load_raw_factors()

    univ_c, elig_c = build_line(df, '90')
    univ_f, elig_f = build_line(df, '30')

    ok, detail = sanity_check_line_c(univ_c)
    if not ok:
        print(f"  ✗ sanity check FAILED against data.json top20: {detail}")
        sys.exit(1)
    print(f"  ✓ sanity check OK: {detail}")

    if len(elig_c) < N_SEATS or len(elig_f) < N_SEATS:
        print(f"  ✗ not enough eligible names (C={len(elig_c)}, F={len(elig_f)}) — aborting")
        sys.exit(1)

    if SHADOW_JSON.exists():
        state = json.loads(SHADOW_JSON.read_text(encoding='utf-8'))
    else:
        state = None

    if state is None:
        # ── INCEPTION ──
        print(f"  · no existing shadow.json — building inception ({as_of})")
        holdings_c = make_holdings(elig_c, df, as_of)
        holdings_f = make_holdings(elig_f, df, as_of)
        state = {
            'schema': 'momentum5-shadow-v1',
            'prereg': PREREG,
            'as_of': as_of,
            'inception_date': as_of,
            'spy_close_inception': spy_close,
            'last_rebalance_month': month_of(as_of),
            'lines': {
                'C': {'nav_base': 100.0, 'nav': 100.0, 'holdings': holdings_c},
                'F': {'nav_base': 100.0, 'nav': 100.0, 'holdings': holdings_f},
            },
            'nav_series': [{
                'date': as_of, 'nav_C': 100.0, 'nav_F': 100.0, 'nav_spy': 100.0,
                'spy_close': spy_close,
            }],
            'rebalance_history': [
                {'date': as_of, 'event': 'inception', 'line': 'C',
                 'holdings': [h['ticker'] for h in holdings_c], 'turnover_pct': None},
                {'date': as_of, 'event': 'inception', 'line': 'F',
                 'holdings': [h['ticker'] for h in holdings_f], 'turnover_pct': None},
            ],
            'changelog': [
                {'date': as_of, 'event': '影子對照實驗 PREREG 凍結，兩線 inception（90d vs 30d 修正窗）。'},
            ],
        }
        print(f"    line C: {[h['ticker'] for h in holdings_c]}")
        print(f"    line F: {[h['ticker'] for h in holdings_f]}")
    else:
        # ── WEEKLY UPDATE (and possibly monthly rebalance) ──
        last_nav_date = state['nav_series'][-1]['date'] if state['nav_series'] else None
        if last_nav_date == as_of:
            print(f"  · shadow.json already has as_of={as_of} — no-op (idempotent)")
            SHADOW_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n',
                                    encoding='utf-8')
            return

        is_new_month = month_of(as_of) != state.get('last_rebalance_month')

        for line_key, elig in (('C', elig_c), ('F', elig_f)):
            line = state['lines'][line_key]
            if is_new_month:
                # mark-to-market the OUTGOING holdings first, then rebalance
                nav_close, stale = mark_to_market(line['holdings'], df, line['nav_base'])
                old_tickers = set(h['ticker'] for h in line['holdings'])
                new_holdings = make_holdings(elig, df, as_of)
                new_tickers = set(h['ticker'] for h in new_holdings)
                turnover_pct = round(len(old_tickers - new_tickers) / N_SEATS * 100, 1)
                line['nav_base'] = nav_close
                line['nav'] = nav_close
                line['holdings'] = new_holdings
                state['rebalance_history'].append({
                    'date': as_of, 'event': 'rebalance', 'line': line_key,
                    'holdings': sorted(new_tickers), 'turnover_pct': turnover_pct,
                    'stale_prices': stale or None,
                })
            else:
                nav_now, stale = mark_to_market(line['holdings'], df, line['nav_base'])
                line['nav'] = nav_now
                if stale:
                    print(f"    ! line {line_key}: stale price carried forward for {stale}")

        if is_new_month:
            state['last_rebalance_month'] = month_of(as_of)
            state['changelog'].append({
                'date': as_of,
                'event': f"月度機械換倉：line C -> {[h['ticker'] for h in state['lines']['C']['holdings']]}, "
                         f"line F -> {[h['ticker'] for h in state['lines']['F']['holdings']]}",
            })

        nav_spy = round(100.0 * spy_close / state['spy_close_inception'], 2)
        state['as_of'] = as_of
        state['nav_series'].append({
            'date': as_of,
            'nav_C': round(state['lines']['C']['nav'], 2),
            'nav_F': round(state['lines']['F']['nav'], 2),
            'nav_spy': nav_spy,
            'spy_close': spy_close,
        })
        print(f"    nav_C={state['lines']['C']['nav']:.2f}  "
              f"nav_F={state['lines']['F']['nav']:.2f}  nav_spy={nav_spy:.2f}")

    SHADOW_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n',
                            encoding='utf-8')
    print(f"  ✓ wrote {SHADOW_JSON.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
