"""
Momentum-5 SHADOW TRACK builder — four mechanical variants of the frozen
composite, run as a paper A/B/C/D alongside the human-curated Momentum-5
portfolio.

WHAT THIS IS
------------
A pre-registered (PREREG, frozen 2026-08-20), fully mechanical shadow
experiment that rides alongside the human-curated Momentum-5 portfolio. It
does NOT touch portfolio.json, data.json, or the frozen composite in
build_momentum5.py. It reads the full-universe raw factor dump
(docs/research/momentum-5/raw_factors.json, written by build_momentum5.py)
and runs FOUR purely mechanical top-5 lines on the SAME data:

  line C (control) : frozen composite exactly as-is (rev_avg = 90-day window).
  line F (fresh)   : ONLY the revision factor changed to the 30-day window
                     (rev30_fy1/rev30_fy2 average) — both in the composite's
                     rev term AND in the rev_avg<=0 veto. Everything else
                     (weights, other two factors, other vetoes, universe,
                     winsorize/z) is byte-identical to line C's logic.
  line P (PEAD)    : 2026-08-20 addition. ONLY the revision factor is
                     replaced with z(surprise) — the most recent already-
                     reported quarter's EPS surprise% (yfinance
                     Ticker.earnings_history, must be <=120 days old or the
                     ticker is excluded). rev_avg<=0 veto becomes
                     surprise<=0. Data gate: surprise coverage <300 ->
                     line P does not rebalance that week (NAV still marks
                     to market on existing holdings); logged as a data_gap.
  line Q (path)    : 2026-08-20 addition. Composite and vetoes identical to
                     line C. Secondary filter: take line C's eligible top 20
                     by composite score, then re-rank by smoothness (up-day
                     ratio over the trailing 126 trading days, pct_up_126,
                     descending) and take the top 5. Ties broken by ticker.

Purpose: test three single-variable deviations from the frozen 90-day-window
composite — revision freshness (F), earnings-surprise substitution (P), and
path-quality re-ranking (Q) — against the control line and SPY, in a clean,
deterministic, cost-free, equal-weight, monthly-rebalance paper track. Full
spec lives in the "prereg" block of shadow.json (verbatim, do not edit
outside of the 2026-11-22 review point below).

MULTIPLE-TESTING HONESTY (PREREG'd 2026-08-20, do not relax): running three
experimental lines at once raises the odds that one wins by chance alone.
"Winning" requires beating BOTH line C AND SPY, with max drawdown no worse.
Promoting any line to a real rule still requires a human monthly-review
sign-off. A losing line is recorded and closed — no re-tuning, no re-adding
it later (anti p-hacking).

Review point: 2026-11-22 (first successful weekly update on/after this date)
— human review of cumulative return & max drawdown, F/P/Q vs C vs SPY.

MECHANICS
---------
- Universe & vetoes: identical structure to build_momentum5.py for C/F/Q;
  line P swaps the revision term/veto for a freshness-gated earnings
  surprise term (see above).
- Equal weight, 5 seats each line, inception 2026-08-20.
- Rebalance: mechanical, on the first successful weekly update day of each
  calendar month (whole-month buy & hold otherwise). Line P skips a
  scheduled rebalance if the surprise data gate trips (see above).
- NAV: paper NAV, marked at each week's close. No transaction costs (all
  lines identical assumption, so the A/B/C/D comparison stays fair).
- Ties: broken by ticker alphabetical order (deterministic).
- Exclusions: tickers missing eps_trend data are excluded (same as the main
  script — they never entered raw_factors.json's universe in the first
  place, since that dump is sourced from the main script's post-dropna
  frame). Line P additionally excludes tickers whose most recent reported
  quarter's surprise is >120 days old.

All state (holdings, nav_series, rebalance_history, changelog, data_gaps,
prereg spec) lives in docs/research/momentum-5/raw_factors.json's sibling,
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
Q_POOL_SIZE = 20                # line Q reselects from line C's eligible top-N
SURPRISE_FRESH_DAYS = 120       # line P: surprise must be from a quarter reported within this window
SURPRISE_MIN_COVERAGE = 300     # line P data gate: below this, skip the scheduled rebalance

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
    # 2026-08-20 擴充：加開 line P（財報驚喜／PEAD）與 line Q（路徑品質）
    # 兩條實驗線，與既有 line C／line F 並跑於同一份 shadow.json。
    "design_p": {
        "title": "Line P（PEAD 財報驚喜線，2026-08-20 新增）",
        "objective": "檢定「財報後實際-預估驚喜」是否比「分析師修正動能」更能預測未來 12 個月表現。",
        "design": (
            "與 line C 同公式，唯一改動：composite 中 0.5 權重那一項由 z(rev_avg 90d) "
            "換成 z(surprise)；否決中的 rev_avg≤0 相應換成 surprise≤0；"
            "其餘兩項因子（relmom6、growth）與其餘否決（200DMA、12M>+250%）完全相同。"
        ),
        "surprise_definition": (
            "surprise 取 yfinance Ticker.earnings_history 最近一筆已公布季度的 "
            "surprisePercent（語意＝（實際 EPS－預估 EPS）／|預估 EPS|，yfinance 原始欄位為分數，"
            "本系統換算為百分點單位以對齊 rev_fy1/rev_fy2/growth 的慣例）。"
        ),
        "freshness_gate": (
            "該筆財報所屬季度須在 120 天內，逾期視為不合格，該股直接排除出 universe"
            "（不是記為 0，是不進場）。"
        ),
        "data_gate": (
            "全 universe 的新鮮（120 天內）surprise 覆蓋 <300 檔時，line P 該週不換倉"
            "（NAV 仍照既有持倉最新價格更新），並在 shadow.json 記一筆 data_gap。"
        ),
    },
    "design_q": {
        "title": "Line Q（路徑品質線，2026-08-20 新增，frog in the pan）",
        "objective": "檢定「漲勢平滑度」能否篩掉噴出型假動能，選出更抗回撤的路徑。",
        "design": (
            "composite 與否決跟 line C 完全一樣；多一道二次篩選——先取 line C composite "
            "前 20 名，再按近 126 個交易日上漲天數佔比（up-day ratio，平滑度代理）由高到低"
            "取前 5 檔；同分以 ticker 字母序決勝。"
        ),
        "sanity": (
            "line Q 的 20 檔候選池須與 line C 當週的 20 檔候選池集合完全一致；"
            "建置腳本內建此檢查，不一致時報錯且不寫入 shadow.json。"
        ),
    },
    "multiple_testing": (
        "三條實驗線並跑，隨機矇對機率上升；『勝出』門檻＝同時勝過 line C 與 SPY 且最大回撤不更差；"
        "升級正式規則仍須人工月度複審拍板。敗者記錄結案，不回頭調參。"
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


def build_line_p(df, as_of):
    """Line P: revision term replaced with a freshness-gated earnings-surprise
    term. rev_avg<=0 veto becomes surprise<=0; everything else identical to
    line C's structure. Returns (univ, elig, coverage) where coverage is the
    count of tickers whose surprise is present AND within SURPRISE_FRESH_DAYS
    of as_of (the data-gate metric)."""
    as_of_ts = pd.Timestamp(as_of)

    def fresh_surprise(row):
        sd, sp = row.get('surprise_date'), row.get('surprise_pct')
        if sd is None or sp is None or (isinstance(sp, float) and np.isnan(sp)):
            return np.nan
        try:
            age_days = (as_of_ts - pd.Timestamp(sd)).days
        except (ValueError, TypeError):
            return np.nan
        if age_days < 0 or age_days > SURPRISE_FRESH_DAYS:
            return np.nan
        return float(sp)

    d = df.copy()
    d['surprise'] = d.apply(fresh_surprise, axis=1)
    coverage = int(d['surprise'].notna().sum())

    univ = d.dropna(subset=['surprise', 'growth', 'relmom6']).copy()
    univ['score'] = (W_REV * z(univ['surprise'])
                      + W_MOM * z(univ['relmom6'])
                      + W_GROWTH * z(univ['growth']))
    univ['eligible'] = (univ['above200'].astype(bool)
                         & (univ['surprise'] > 0)
                         & (univ['ret12'] < VETO_RET12))

    elig = univ[univ['eligible']].copy()
    elig['_tkr_sort'] = elig.index
    elig = elig.sort_values(['score', '_tkr_sort'], ascending=[False, True])
    elig = elig.drop(columns=['_tkr_sort'])
    return univ, elig, coverage


def build_line_q(df, elig_c_ref):
    """Line Q: line C's eligible top-Q_POOL_SIZE, re-ranked by smoothness
    (pct_up_126, descending; ties by ticker). Sanity: independently
    recomputes line C's composite/eligibility and asserts the top-N ticker
    SET matches elig_c_ref's top-N — guards against future drift decoupling
    Q's base pool from the frozen line-C composite. Raises RuntimeError (and
    therefore aborts the whole build, writing nothing) on mismatch."""
    _, elig_c_check = build_line(df, '90')
    pool_check = set(elig_c_check.head(Q_POOL_SIZE).index)
    pool_ref = set(elig_c_ref.head(Q_POOL_SIZE).index)
    if pool_check != pool_ref:
        raise RuntimeError(
            f"line Q sanity check FAILED: recomputed line-C top{Q_POOL_SIZE} "
            f"{sorted(pool_check)} != reference top{Q_POOL_SIZE} {sorted(pool_ref)}"
        )

    pool = elig_c_ref.head(Q_POOL_SIZE).copy()
    pool['_tkr_sort'] = pool.index
    pool['_smooth_sort'] = pool['pct_up_126'] if 'pct_up_126' in pool.columns else np.nan
    pool['_smooth_sort'] = pool['_smooth_sort'].fillna(-1.0)
    pool = pool.sort_values(['_smooth_sort', '_tkr_sort'], ascending=[False, True])
    elig_q = pool.drop(columns=['_tkr_sort', '_smooth_sort'])
    return elig_q, pool_ref


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
    univ_p, elig_p, coverage_p = build_line_p(df, as_of)
    elig_q, q_pool = build_line_q(df, elig_c)  # raises RuntimeError (abort, write nothing) on pool mismatch

    ok, detail = sanity_check_line_c(univ_c)
    if not ok:
        print(f"  ✗ sanity check FAILED against data.json top20: {detail}")
        sys.exit(1)
    print(f"  ✓ sanity check line C OK: {detail}")
    print(f"  ✓ sanity check line Q pool OK: matches line C top{Q_POOL_SIZE} ({len(q_pool)} tickers)")
    print(f"  · line P surprise coverage (fresh <= {SURPRISE_FRESH_DAYS}d): {coverage_p}")

    if len(elig_c) < Q_POOL_SIZE:
        print(f"  ✗ line C eligible pool ({len(elig_c)}) < {Q_POOL_SIZE} — cannot build line Q base — aborting")
        sys.exit(1)
    if len(elig_c) < N_SEATS or len(elig_f) < N_SEATS or len(elig_q) < N_SEATS:
        print(f"  ✗ not enough eligible names (C={len(elig_c)}, F={len(elig_f)}, Q={len(elig_q)}) — aborting")
        sys.exit(1)

    p_gate_ok = coverage_p >= SURPRISE_MIN_COVERAGE and len(elig_p) >= N_SEATS

    if SHADOW_JSON.exists():
        state = json.loads(SHADOW_JSON.read_text(encoding='utf-8'))
    else:
        state = None

    if state is None:
        # ── FULL INCEPTION (all four lines) ──
        print(f"  · no existing shadow.json — building inception ({as_of})")
        if not p_gate_ok:
            print(f"  ✗ line P cannot launch at inception: coverage={coverage_p} "
                  f"(need >= {SURPRISE_MIN_COVERAGE}), eligible={len(elig_p)} (need >= {N_SEATS}) "
                  f"— aborting whole build")
            sys.exit(1)
        holdings = {
            'C': make_holdings(elig_c, df, as_of),
            'F': make_holdings(elig_f, df, as_of),
            'P': make_holdings(elig_p, df, as_of),
            'Q': make_holdings(elig_q, df, as_of),
        }
        state = {
            'schema': 'momentum5-shadow-v2',
            'prereg': PREREG,
            'as_of': as_of,
            'inception_date': as_of,
            'spy_close_inception': spy_close,
            'last_rebalance_month': month_of(as_of),
            'lines': {k: {'nav_base': 100.0, 'nav': 100.0, 'holdings': h} for k, h in holdings.items()},
            'nav_series': [{
                'date': as_of, 'nav_C': 100.0, 'nav_F': 100.0, 'nav_P': 100.0, 'nav_Q': 100.0,
                'nav_spy': 100.0, 'spy_close': spy_close,
            }],
            'rebalance_history': [
                {'date': as_of, 'event': 'inception', 'line': k,
                 'holdings': [h['ticker'] for h in hs], 'turnover_pct': None}
                for k, hs in holdings.items()
            ],
            'changelog': [
                {'date': as_of, 'event': '影子對照實驗 PREREG 凍結，四線 inception'
                                          '（90d／30d 修正窗／PEAD 財報驚喜／路徑品質）。'},
            ],
            'data_gaps': [],
        }
        for k in ('C', 'F', 'P', 'Q'):
            print(f"    line {k}: {[h['ticker'] for h in holdings[k]]}")
    else:
        # ── one-time backfill of any line missing from an already-existing
        #    state (P/Q added 2026-08-20, same calendar day as C/F's original
        #    inception commit) — then the normal weekly-update path below ──
        state.setdefault('data_gaps', [])
        added = []
        if 'P' not in state['lines']:
            if not p_gate_ok:
                print(f"  ✗ cannot backfill line P: coverage={coverage_p} < {SURPRISE_MIN_COVERAGE} "
                      f"or eligible={len(elig_p)} < {N_SEATS} — aborting")
                sys.exit(1)
            holdings_p = make_holdings(elig_p, df, as_of)
            state['lines']['P'] = {'nav_base': 100.0, 'nav': 100.0, 'holdings': holdings_p}
            state['rebalance_history'].append({
                'date': as_of, 'event': 'inception', 'line': 'P',
                'holdings': [h['ticker'] for h in holdings_p], 'turnover_pct': None,
            })
            added.append('P')
            print(f"    line P (backfilled): {[h['ticker'] for h in holdings_p]}")
        if 'Q' not in state['lines']:
            holdings_q = make_holdings(elig_q, df, as_of)
            state['lines']['Q'] = {'nav_base': 100.0, 'nav': 100.0, 'holdings': holdings_q}
            state['rebalance_history'].append({
                'date': as_of, 'event': 'inception', 'line': 'Q',
                'holdings': [h['ticker'] for h in holdings_q], 'turnover_pct': None,
            })
            added.append('Q')
            print(f"    line Q (backfilled): {[h['ticker'] for h in holdings_q]}")
        if added:
            state['prereg'] = PREREG
            state['schema'] = 'momentum5-shadow-v2'
            added_zh = '、'.join('財報驚喜' if x == 'P' else '路徑品質' for x in added)
            state['changelog'].append({
                'date': as_of,
                'event': f"新增 line {'、'.join(added)} inception（{added_zh}），同日補建於既有 line C／F 序列。",
            })

        last_nav_date = state['nav_series'][-1]['date'] if state['nav_series'] else None

        if last_nav_date == as_of:
            # same day as the last recorded row: either a pure no-op re-run,
            # or today's backfill — either way, patch today's row in place
            # and do NOT append a second row for the same date.
            if added and state['nav_series']:
                row = state['nav_series'][-1]
                if 'P' in added:
                    row['nav_P'] = 100.0
                if 'Q' in added:
                    row['nav_Q'] = 100.0
            SHADOW_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n',
                                    encoding='utf-8')
            if added:
                print(f"  ✓ wrote {SHADOW_JSON.relative_to(ROOT)} (backfilled: {', '.join(added)})")
            else:
                print(f"  · shadow.json already has as_of={as_of} — no-op (idempotent)")
            return

        # ── WEEKLY UPDATE (and possibly monthly rebalance) ──
        is_new_month = month_of(as_of) != state.get('last_rebalance_month')

        for line_key, elig in (('C', elig_c), ('F', elig_f), ('Q', elig_q)):
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

        # ── line P: data-gated rebalance ──
        line_p = state['lines']['P']
        if is_new_month and p_gate_ok:
            nav_close, stale = mark_to_market(line_p['holdings'], df, line_p['nav_base'])
            old_tickers = set(h['ticker'] for h in line_p['holdings'])
            new_holdings = make_holdings(elig_p, df, as_of)
            new_tickers = set(h['ticker'] for h in new_holdings)
            turnover_pct = round(len(old_tickers - new_tickers) / N_SEATS * 100, 1)
            line_p['nav_base'] = nav_close
            line_p['nav'] = nav_close
            line_p['holdings'] = new_holdings
            state['rebalance_history'].append({
                'date': as_of, 'event': 'rebalance', 'line': 'P',
                'holdings': sorted(new_tickers), 'turnover_pct': turnover_pct,
                'stale_prices': stale or None,
            })
        else:
            nav_now, stale = mark_to_market(line_p['holdings'], df, line_p['nav_base'])
            line_p['nav'] = nav_now
            if stale:
                print(f"    ! line P: stale price carried forward for {stale}")
            if is_new_month and not p_gate_ok:
                reason = (f"surprise 覆蓋 {coverage_p} < {SURPRISE_MIN_COVERAGE}"
                          if coverage_p < SURPRISE_MIN_COVERAGE
                          else f"合格檔數 {len(elig_p)} < {N_SEATS}")
                state['data_gaps'].append({
                    'date': as_of, 'line': 'P', 'reason': reason, 'coverage': coverage_p,
                })
                state['changelog'].append({
                    'date': as_of,
                    'event': f"line P 資料閘觸發（{reason}），本月不換倉，NAV 照原持倉更新。",
                })

        if is_new_month:
            state['last_rebalance_month'] = month_of(as_of)
            p_note = (f", line P -> {[h['ticker'] for h in state['lines']['P']['holdings']]}"
                      if p_gate_ok else " (line P 本月資料閘觸發，未換倉)")
            state['changelog'].append({
                'date': as_of,
                'event': f"月度機械換倉：line C -> {[h['ticker'] for h in state['lines']['C']['holdings']]}, "
                         f"line F -> {[h['ticker'] for h in state['lines']['F']['holdings']]}, "
                         f"line Q -> {[h['ticker'] for h in state['lines']['Q']['holdings']]}" + p_note,
            })

        nav_spy = round(100.0 * spy_close / state['spy_close_inception'], 2)
        state['as_of'] = as_of
        state['nav_series'].append({
            'date': as_of,
            'nav_C': round(state['lines']['C']['nav'], 2),
            'nav_F': round(state['lines']['F']['nav'], 2),
            'nav_P': round(state['lines']['P']['nav'], 2),
            'nav_Q': round(state['lines']['Q']['nav'], 2),
            'nav_spy': nav_spy,
            'spy_close': spy_close,
        })
        print(f"    nav_C={state['lines']['C']['nav']:.2f}  nav_F={state['lines']['F']['nav']:.2f}  "
              f"nav_P={state['lines']['P']['nav']:.2f}  nav_Q={state['lines']['Q']['nav']:.2f}  "
              f"nav_spy={nav_spy:.2f}")

    SHADOW_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n',
                            encoding='utf-8')
    print(f"  ✓ wrote {SHADOW_JSON.relative_to(ROOT)}")


if __name__ == '__main__':
    main()
