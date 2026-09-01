"""
Price-Momentum (P10) weekly paper-track builder — feeds
docs/research/price-momentum/track.json.

WHAT THIS IS
------------
P10 is a zero-fundamentals, fully mechanical, self-accounting-NAV pure
price-momentum paper track — deliberately the fourth, separate lens
alongside the RS+VCP screener (discovery radar), QGM (quality-gated
momentum) and Momentum-5/shadow (EPS-revision momentum). It is NOT a
convergence surface: it does not feed the DD verdict chain, does not enter
picks/GRP/three-track/cockpit, and must not be cited by any other session
as "ticker X is on P10" grounds for a position decision. There is zero
human intervention at the single-name level; the only human touchpoints
are this file's PREREG review points and kill conditions.

As of the 2026-09-01 two-line expansion (PREREG §11, folded into the same
v0 freeze before first commit), P10 runs TWO independent mechanical lines
side by side on the SAME universe/data to answer "slow momentum vs fast
momentum": L12 (12-1 lookback, the original §2-§8 spec, unchanged) and L6
(6-1 lookback — the ONLY variable that differs from L12; everything else —
eligibility shape, heat flag, buy/hold buffer, monthly rebalance,
equal-weight reset, cash seats, turnover accounting — is byte-identical
code shared by both lines).

FROZEN SPEC (PREREG'd 2026-09-01 — LOCKED, do not tune here)
--------------------------------------------------------------
Universe  : S&P 500 constituents (Wikipedia scrape, browser UA, `.` -> `-`,
            identical approach to build_momentum5.py) UNION NQ100_EXTRAS
            (24 tickers copied verbatim from scripts/screener.py — see
            below). On overlap the S&P sector wins. SAME universe feeds
            BOTH lines (§11: the data-sufficiency floor stays >=253 closes
            for both lines deliberately, so lookback is the only variable).
Signal (L12, slow line — §2, unchanged):
              c = a ticker's dropna'd adjusted-close series (>= 253 closes,
              else excluded from coverage).
              ret_12_1 = c.iloc[-22] / c.iloc[-253] - 1   (12-1 momentum:
                the standard skip-most-recent-month 11-month return)
              win = c.iloc[-253:-21]
              vol = win.pct_change().dropna().std() * sqrt(252)  (annualized
                vol over the SAME window as the return)
              score = ret_12_1 / vol.  vol == 0 or NaN -> excluded from L12.
Signal (L6, fast line — §11, 2026-09-01 addition): the ONLY delta from L12
  is the lookback window; everything else below is shared.
              ret_6_1 = c.iloc[-22] / c.iloc[-127] - 1   (6-1 momentum:
                skip-most-recent-month 5-month return; 127 mirrors
                build_momentum5.py's spy6 convention)
              win = c.iloc[-127:-21]
              vol = win.pct_change().dropna().std() * sqrt(252)
              score = ret_6_1 / vol.  vol == 0 or NaN -> excluded from L6.
Eligibility (all price-only, zero fundamentals; deliberately no +250%
veto and no revision/earnings/valuation gate — PREREG says so explicitly;
shared shape, evaluated independently per line off that line's own ret):
  1. ret_{12,6}_1 > 0                  (absolute-momentum bear-market valve)
  2. c.iloc[-1] > 200DMA (< 200 closes -> excluded; structurally unreachable
     here since the >=253 coverage floor already implies >= 200) — SAME
     200DMA gate for both lines.
  Heat flag (informational only, NOT a veto, shared by both lines — it is a
  property of the NAME, not of a line, per §11): plain 12M return
  c.iloc[-1]/c.iloc[-253] - 1 > 2.5 -> flagged 'heat' on the holding.
Selection / buffer / weight (shared rules, shared code path, applied
independently per line):
  - Rank that line's eligible list by its score, descending; score ties
    break by ticker alphabetical order (stable sort over the alphabetized
    universe) so the ranking is fully deterministic.
  - Buy zone = top 10.  Hold zone = top 40 (fall out of top 40, or turn
    ineligible, -> sell).
  - Monthly rebalance: sell anything not in this month's eligible top 40
    (ineligible names are automatically absent from that set — same rule,
    no separate branch); backfill empty seats with the highest-ranked
    unheld eligible names in rank order, up to 10 seats or until the
    eligible list is exhausted; unfillable seats stay CASH (0 return) —
    never force-filled.
  - On every rebalance the WHOLE line resets to equal weight: each held
    ticker's weight = NAV/10, converted to units at that day's close;
    cash = NAV * (10 - held_count) / 10.
NAV accounting (shared code path, independent bookkeeping per line):
  - Inception = the first run ever = the first rebalance for BOTH lines,
    same day. NAV = 100.0 for each line; nav_spy normalized to 100 the
    same day off SPY's close (one shared SPY series/benchmark).
  - Every run (weekly) marks each line to market: NAV = cash + sum(units *
    that ticker's latest close). SPY tracked once, shared.
  - Rebalance trigger: this run's calendar month != last_rebalance_month
    -> mark BOTH lines to market FIRST (on their outgoing holdings), THEN
    execute each line's rebalance at that same day's close. ONE shared
    last_rebalance_month drives both lines (same last_rebalance_month
    convention as build_momentum5_shadow.py).
  - Same-day reruns are idempotent: a nav_series row for a date already
    present is overwritten in place, never duplicated; ditto for each
    line's rebalance_history.
Turnover (kill condition #3's data basis, evaluated independently per
  line): every rebalance records n_sells for that line.
  turnover_12m_annualized = (sum of n_sells over the trailing 12
  rebalances) / 10, expressed as a percent; with fewer than 12 rebalances
  on record it is annualized off the actual count instead and flagged
  partial: true. turnover_kill_watch only arms on a FULL 12-rebalance
  window (annualizing a partial window extrapolates noise).
Kill conditions (verbatim in track.json's prereg block; NOT auto-enforced
  by this script — they are human review triggers, evaluated formally at
  2028-09-01 / 24 months, with turnover (#3) allowed to fire early; per
  §11 these now apply INDEPENDENTLY to each line):
  1. 24-month NAV trails SPY AND max drawdown is worse than SPY -> close
     (per line).
  2. Reconciled against Momentum-5 shadow line C over the overlapping
     window; behind at BOTH the 12M and 24M checkpoints -> record "in this
     universe, revision momentum beat price momentum" and close (per line).
  3. turnover_12m_annualized > 300% -> the buffer-band design has failed,
     back to the drawing board (may fire before 24 months); 300% is a
     shared cost-viability threshold for BOTH lines, not a fairness knob —
     if L6 structurally can't stay under 300% turnover, that itself is the
     finding (fast momentum isn't investable at this seat count/buffer).
Multiple-testing honesty (§11, mirrors momentum5_shadow.py's culture):
  running two lines raises the odds one "wins" by luck alone. Winning
  requires beating BOTH SPY AND the other line, with max drawdown no
  worse. A losing line is recorded and closed — no re-tuning, no re-adding
  it later.
50/50 blend (§11): a derived quantity computable at any time straight off
  the two nav_series — never a third line, never promoted to a formal rule
  without a fresh PREREG.

FAIL-SAFE (mirrors scripts/build_momentum5.py culture)
-------------------------------------------------------
Any of the following -> print a warning, exit 0, and leave track.json
completely untouched:
  - Wikipedia scrape fails, or yields < 400 constituents.
  - Fewer than 400 tickers clear the >=253-close price-sufficiency floor
    (shared floor — gates both lines at once).
  - Any uncaught exception anywhere in the build (top-level try/except
    around main()).

Runs in the weekly-market-update GitHub Actions workflow (wired by
maintainer), same step family as build_momentum5.py.
"""

import io
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

import requests

ROOT = Path(__file__).resolve().parent.parent
TRACK_JSON = ROOT / 'docs' / 'research' / 'price-momentum' / 'track.json'

WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'

# NQ100_EXTRAS — copied verbatim from scripts/screener.py (as of 2026-09-01),
# ticker -> sector. PREREG requires a straight copy, not an import, so this
# builder stays self-contained (see docstring / handoff spec §1, §9).
NQ100_EXTRAS = {
    'ARM':'Technology','MSTR':'Technology','SMCI':'Technology','APP':'Technology',
    'COIN':'Financials','DASH':'Consumer Disc','DDOG':'Technology','MNDY':'Technology',
    'TEAM':'Technology','TTD':'Technology','ZS':'Technology','RIVN':'Consumer Disc',
    'MELI':'Consumer Disc','GFS':'Technology','GEHC':'Health Care','WBD':'Communication',
    'LULU':'Consumer Disc','MRNA':'Health Care','CPRT':'Industrials','TTWO':'Communication',
    'WDAY':'Technology','ABNB':'Consumer Disc','PYPL':'Financials','PCAR':'Industrials',
}

# ── frozen thresholds (PREREG'd 2026-09-01, LOCKED — do not tune) ──
MIN_CLOSES = 253            # per-ticker data-sufficiency floor, SHARED by both lines (§1, §11)
MA_WINDOW = 200              # 200DMA eligibility gate, shared by both lines (§3)
VOL_ANNUALIZE = float(np.sqrt(252))
HEAT_RET12 = 2.5             # plain 12M return > +250% -> informational heat flag, shared (§3, §11)
FAR_IDX_L12 = -253           # L12 (slow line) far anchor — 12-1 momentum (§2)
FAR_IDX_L6 = -127            # L6 (fast line) far anchor — 6-1 momentum (§11)
TOP_BUY = 10                 # buy zone (documented; buys are drawn from the
                              # eligible ranking generally, see do_rebalance)
TOP_HOLD = 40                # hold zone / sell buffer (§4)
N_SEATS = 10
MIN_CONSTITUENTS = 400       # fail-safe floor on raw Wikipedia scrape (§7)
MIN_PRICE_COVERAGE = 400     # fail-safe floor on >=253-close ticker count (§7), shared by both lines
TURNOVER_WINDOW = 12         # trailing rebalances for turnover_12m_annualized (§6)
TURNOVER_KILL_PCT = 300.0    # kill condition #3 watch threshold (§8), same for both lines (§11)
LINE_KEYS = ('L12', 'L6')

PREREG = {
    "title": "P10 純價格動能 paper track — v0（雙線 L12/L6，PREREG，2026-09-01 凍結）",
    "frozen_date": "2026-09-01",
    "positioning": (
        "P10 是零基本面成分、全機械、自帶 NAV 的純價格動能 paper track——"
        "與 RS+VCP screener（發現雷達）、QGM（品質閘門後動能）、Momentum-5/shadow"
        "（EPS 修正動能）刻意分離的第四條線。它不是收斂面：不回饋 DD 裁決鏈、"
        "不進 picks/GRP/三軌/cockpit 任何清單，不得被其他 session 引用為"
        "「某檔在 P10 上」的選股依據。個股層零人為干預；唯一人類接觸點是 "
        "prereg 的 review points 與 kill conditions。"
    ),
    "universe_and_data": {
        "universe": "S&P 500 成分（Wikipedia scrape，瀏覽器 UA，完全照抄 build_momentum5.py 做法，`.`→`-`），加上 NQ100_EXTRAS（copy scripts/screener.py 的 NQ100_EXTRAS dict，24 檔，ticker→sector），與 S&P 名單 union 去重（若某 extra 已入 S&P 以 S&P 的 sector 為準）。",
        "prices": "yf.download(tickers + ['SPY'], period='2y', interval='1d', auto_adjust=True, group_by='ticker', threads=True)，同 build_momentum5 模式。",
        "sufficiency_floor": "個股資料充足門檻：dropna 後 close series 長度 ≥ 253，否則排除（記入 coverage 統計）。",
    },
    "signal": {
        "definition": "c＝該 ticker dropna 後的 adjusted close series，最後一筆為 t。",
        "ret_12_1": "ret_12_1 = c.iloc[-22] / c.iloc[-253] - 1（12-1 動能：跳過最近 21 個交易日的 11 個月報酬，這是文獻標準定義）。",
        "vol": "win = c.iloc[-253:-21]；vol = win.pct_change().dropna().std() * sqrt(252)（與報酬同窗的年化波動）。",
        "score": "score = ret_12_1 / vol。vol 為 0 或 NaN → 排除。",
    },
    "eligibility": {
        "gate_1": "ret_12_1 > 0（絕對動能——內建熊市閥）。",
        "gate_2": "c.iloc[-1] > 200DMA（最近 200 筆 close 的簡單平均；不足 200 筆 → 排除）。",
        "no_extra_vetoes": "沒有 +250% 過熱否決、沒有任何 revision/獲利/估值條件——這是刻意的，prereg 已明文。",
        "heat_flag": "Heat flag（純資訊、非否決）：plain 12M 報酬 c.iloc[-1]/c.iloc[-253] - 1 > 2.5 → 該持股掛 heat flag。",
    },
    "selection_buffer_weight": {
        "ranking": "對 eligible 名單按 score 降冪排名；score 同分以 ticker 字母序 tie-break（穩定排序疊在字母序 universe 上），排名完全確定性。",
        "zones": "買進區 = top 10；持有區 = top 40（eligible 排名；跌出 top 40 或變不合格 → 賣）。",
        "monthly_rebalance": (
            "每月 rebalance：先賣出「不在 eligible top 40 內」的持股（變不合格者自然不在名單內，"
            "同一條規則覆蓋）；空出的席位由排名最高的未持有 eligible 名字依序補入，補到 10 席或"
            "名單耗盡；補不滿的席位留現金（報酬 0），不硬湊。"
        ),
        "weight_reset": "Rebalance 時全組合重置等權：每檔持股權重 = NAV/10 ÷ 該日收盤價 → 換算成 units 記帳；現金 = NAV × (10 − 持股數)/10。",
    },
    "nav_accounting": {
        "inception": "Inception：首次執行日 = 首次 rebalance，NAV = 100.0；nav_spy 同日以 SPY 收盤 normalize 至 100。",
        "mark_to_market": "每次執行（週更）mark to market：NAV = cash + Σ units × 該檔最新收盤；SPY 同步。",
        "rebalance_trigger": "Rebalance 觸發：本次執行的日曆月份 ≠ last_rebalance_month → 先 mark to market，再以當日收盤執行 rebalance（與 shadow 的 last_rebalance_month 慣例一致）。",
        "idempotency": "同日重跑冪等：nav_series 同日期覆蓋不重複 append；同日重跑 rebalance 則以確定性結果覆蓋當日那筆 rebalance_history。",
        "rebalance_history_fields": "rebalance_history 每筆記：date、sells、buys、期末 holdings（ticker/rank/score/units）、eligible 數、現金席位數。",
    },
    "turnover": {
        "definition": "每次 rebalance 記 n_sells。turnover_12m_annualized = 近 12 次 rebalance 的 Σ n_sells / 10（不足 12 次先照實際次數年化，標註 partial: true）。",
    },
    "fail_safe": (
        "以下任一 → print warning、exit 0、完全不動 track.json：Wikipedia scrape 失敗或成分 < 400；"
        "價格資料充足（≥253 closes）的 ticker 數 < 400；任何未捕捉例外（top-level try/except 包 main）。"
    ),
    "kill_conditions": {
        "evaluation_point": "正式評估點 2028-09-01（24 個月）；期中讀數（如 2027-09-01）可看、不具裁決力。No re-tuning、no re-adding、closed stays closed。",
        "kill_1": "24 個月 NAV 落後 SPY 且 Max DD 比 SPY 深 → 關閉。",
        "kill_2": "與 shadow line C 在重疊窗口對帳，12M 與 24M 檢查點皆落後 → 記錄「本宇宙中獲利修正動能 > 價格動能」結論後關閉。",
        "kill_3": "turnover_12m_annualized > 300%（即 12 個月 Σ n_sells > 30）→ 緩衝帶設計失敗，回爐（此條可提前觸發）。",
    },
    "disclosure": (
        "誠實標注：paper track、無交易成本、機械式、非投資建議。不是收斂面，不進任何裁決鏈"
        "（picks/GRP/三軌/cockpit）。個股層零人為干預；唯一人類接觸點是本 prereg 的 review points 與 kill conditions。"
    ),
    "two_line_expansion": {
        "title": "雙線擴建（2026-09-01 持有人拍板，commit 前納入 v0 凍結範圍）",
        "objective": "P10 track 擴為兩條線並跑，回答「慢動能 vs 快動能誰對」。",
        "l12": "L12（慢線）：即上述 §2–§8（signal/eligibility/selection_buffer_weight/nav_accounting/turnover/fail_safe/kill_conditions）全部規格，原樣不動。",
        "l6": (
            "L6（快線）：與 L12 的唯一變數是 lookback，其餘 byte-identical：ret_6_1 = "
            "c.iloc[-22] / c.iloc[-127] - 1（6-1 動能：跳過最近 21 個交易日的 5 個月報酬；"
            "127 與 build_momentum5.py 的 spy6 慣例一致）；win = c.iloc[-127:-21]；"
            "vol = win.pct_change().dropna().std() * sqrt(252)；score = ret_6_1 / vol。"
            "資格：ret_6_1 > 0 + 同一條 200DMA 閘。資料充足門檻維持 ≥253（刻意：兩線 universe "
            "必須完全相同，否則 lookback 不是唯一變數）。Heat flag 定義不變（plain 12M > "
            "+250%，是名字的屬性非訊號的屬性，兩線共用）。top10/top40 緩衝、月度換倉、等權重置、"
            "現金席位、換手統計：全部與 L12 同一套規則、同一套程式路徑。"
        ),
        "inception": "兩線同日 inception、各自 NAV=100、各自持股/現金/換手記帳，完全獨立。",
        "tie_break": "排序 tie-break：score 同分以 ticker 字母序（穩定排序）——兩線同規則。",
        "turnover_kill_watch_note": "turnover kill watch：僅在滿 12 次 rebalance 窗口觸發——兩線同規則。",
        "multiple_testing_honesty": (
            "多重檢定誠實（比照 shadow.json）：兩條線並跑提高其中一條靠運氣贏的機率。"
            "「贏」的定義＝同時打敗 SPY 與另一條線，且 Max DD 不更差。輸的線記錄結論後關閉，"
            "不重調、不復活。"
        ),
        "per_line_kill_conditions": (
            "Kill conditions 逐線獨立適用：kill ①（vs SPY）與 kill ③（換手 >300%）每條線各自評；"
            "kill ③ 門檻兩線同為 300%——這是成本可行性判準不是公平性判準，若 6-1 天生活不過 300% "
            "換手，那本身就是結論（快動能在此席位數/緩衝帶下不可投資）。kill ②（vs shadow line C）"
            "亦逐線對帳。"
        ),
        "blend_clause": (
            "50/50 混合 NAV 是事後衍生物：隨時可從兩條 nav_series 直接計算，不另立第三條線、"
            "不是收斂面；prereg 明文禁止未來 session 以「混合表現好」為由把混合升格為正式線"
            "（那是新規格，須重走 prereg）。"
        ),
    },
}


class FailSafeAbort(Exception):
    """Raised for any of the three PREREG'd fail-safe conditions (§7) — caught
    in main() to print a warning and exit 0 without touching track.json."""


def scrape_sp500():
    """S&P 500 constituents from Wikipedia — identical approach to
    scripts/build_momentum5.py (same URL, same browser UA, `.` -> `-`)."""
    try:
        html = requests.get(WIKI_URL, headers={'User-Agent': BROWSER_UA}, timeout=60).text
        tables = pd.read_html(io.StringIO(html))
        cons = tables[0]
        cons['yf'] = cons['Symbol'].str.replace('.', '-', regex=False)
        sector = dict(zip(cons['yf'], cons['GICS Sector']))
        tickers = cons['yf'].tolist()
    except Exception as e:
        raise FailSafeAbort(f"Wikipedia scrape failed ({type(e).__name__}: {e})")
    return tickers, sector


def build_universe():
    """S&P 500 ∪ NQ100_EXTRAS; S&P sector wins on overlap (PREREG §1). Shared
    by both lines (§11)."""
    sp_tickers, sp_sector = scrape_sp500()
    if len(sp_tickers) < MIN_CONSTITUENTS:
        raise FailSafeAbort(
            f"Wikipedia scrape returned only {len(sp_tickers)} constituents (< {MIN_CONSTITUENTS})")
    sector = dict(sp_sector)
    for t, s in NQ100_EXTRAS.items():
        sector.setdefault(t, s)
    tickers = sorted(sector.keys())
    return tickers, sector


def compute_line_signal(c, far_idx):
    """far_idx = FAR_IDX_L12 (-253, 12-1 momentum, §2) or FAR_IDX_L6 (-127,
    6-1 momentum, §11) — the ONLY variable that differs between the two
    lines. Near anchor is always -22 (skip most-recent 21 trading days);
    vol window is c.iloc[far_idx:-21]. Returns None if vol is 0/NaN (the
    only compute-time exclusion)."""
    ret = c.iloc[-22] / c.iloc[far_idx] - 1.0
    win = c.iloc[far_idx:-21]
    vol = win.pct_change().dropna().std() * VOL_ANNUALIZE
    if vol == 0 or pd.isna(vol):
        return None
    return dict(ret=float(ret), vol=float(vol), score=float(ret / vol))


def compute_ticker(c):
    """c: dropna'd adjusted-close Series (ascending by date), already gated
    by the caller to len(c) >= MIN_CLOSES. Returns (base, sig_l12, sig_l6):
    base = lookback-independent metrics shared by both lines (price,
    above200 200DMA gate, heat flag — heat is a property of the NAME, not
    of a line, per §11); sig_l12/sig_l6 = that line's (ret, vol, score),
    or None if that line's vol is 0/NaN."""
    ma200 = c.rolling(MA_WINDOW).mean().iloc[-1] if len(c) >= MA_WINDOW else np.nan
    above200 = bool(c.iloc[-1] > ma200) if pd.notna(ma200) else False
    ret12_plain = c.iloc[-1] / c.iloc[-253] - 1.0
    heat = bool(ret12_plain > HEAT_RET12)
    base = dict(price=float(c.iloc[-1]), above200=above200, heat=heat)

    sig_l12 = compute_line_signal(c, FAR_IDX_L12)
    sig_l6 = compute_line_signal(c, FAR_IDX_L6)
    return base, sig_l12, sig_l6


def build_elig(rows):
    """rows: {ticker: {price, above200, heat, ret, vol, score, eligible}}
    for ONE line. Returns the eligible subset, ranked by score descending
    (stable mergesort — score ties break by ticker alphabetical order,
    since rows were inserted in alphabetical ticker order; PREREG §4/§11)."""
    if not rows:
        return pd.DataFrame(columns=['price', 'above200', 'heat', 'ret', 'vol', 'score', 'eligible', 'rank'])
    df = pd.DataFrame(rows).T
    elig = df[df['eligible'].astype(bool)].sort_values(
        'score', ascending=False, kind='mergesort').copy()
    elig['rank'] = range(1, len(elig) + 1)
    return elig


def month_of(date_str):
    return date_str[:7]


def compute_turnover_flags(rebalance_history):
    """turnover_12m_annualized_pct (§6): sum(n_sells) over the trailing
    TURNOVER_WINDOW rebalances / N_SEATS, expressed as a percent; with fewer
    than TURNOVER_WINDOW rebalances on record, annualize off the actual
    count instead and flag partial: true. Shared by the inception and
    weekly-update paths (and by both lines) so a same-day rerun is fully
    idempotent.

    turnover_kill_watch only arms on a FULL 12-rebalance window: kill
    condition #3 is defined on 12 個月 Σ n_sells > 30 (see PREREG kill_3), and
    annualizing a partial window extrapolates noise (3 sells at the second
    rebalance would read as 360%)."""
    rebal_events = [r for r in rebalance_history if r['event'] in ('inception', 'rebalance')]
    window = rebal_events[-TURNOVER_WINDOW:]
    n_events = len(window)
    turnover_sum = sum(r.get('n_sells', 0) for r in window)
    if n_events == 0:
        turnover_pct, partial = None, True
    elif n_events >= TURNOVER_WINDOW:
        turnover_pct, partial = round(turnover_sum / N_SEATS * 100, 1), False
    else:
        annualized_sells = turnover_sum / n_events * TURNOVER_WINDOW
        turnover_pct, partial = round(annualized_sells / N_SEATS * 100, 1), True
    return {
        'turnover_12m_annualized_pct': turnover_pct,
        'turnover_partial': partial,
        'turnover_kill_watch': bool(turnover_pct is not None and not partial
                                    and turnover_pct > TURNOVER_KILL_PCT),
    }


def load_state():
    if TRACK_JSON.exists():
        return json.loads(TRACK_JSON.read_text(encoding='utf-8'))
    return None


def mark_to_market(cash, holdings, price_now):
    """NAV = cash + sum(units * latest close). Falls back to the last known
    price (stale carry-forward) when a held ticker is missing this run."""
    total = float(cash)
    stale = []
    for h in holdings:
        p = price_now.get(h['ticker'])
        if p is None:
            p = h.get('last_price', h['entry_price'])
            stale.append(h['ticker'])
        else:
            h['last_price'] = p
        total += h['units'] * p
    return total, stale


def do_rebalance(nav, holdings, elig, price_now, as_of):
    """Sell anything not in this month's eligible top-40; backfill empty
    seats with the highest-ranked unheld eligible names; reset the WHOLE
    resulting holding set to equal weight NAV/N_SEATS (PREREG §4). Shared
    code path for both lines — the caller passes in that line's own elig
    ranking."""
    top40 = set(elig.head(TOP_HOLD).index)
    held_tickers = [h['ticker'] for h in holdings]
    survivors = [t for t in held_tickers if t in top40]
    sells = [t for t in held_tickers if t not in top40]

    held_set = set(survivors)
    buys = []
    for t in elig.index:  # already rank-sorted, best first
        if len(survivors) + len(buys) >= N_SEATS:
            break
        if t in held_set:
            continue
        buys.append(t)
        held_set.add(t)

    new_tickers = survivors + buys
    seat_value = nav / N_SEATS
    new_holdings = []
    for t in new_tickers:
        p = price_now.get(t)
        if p is None or p <= 0:
            continue  # shouldn't happen — t is drawn from elig, itself priced off price_now
        row = elig.loc[t]
        units = seat_value / p
        new_holdings.append({
            'ticker': t,
            'entry_date': as_of,
            'entry_price': round(float(p), 2),
            'rank': int(row['rank']),
            'score': round(float(row['score']), 2),
            'heat': bool(row['heat']),
            'units': float(units),
            'last_price': float(p),
        })
    cash_seats = N_SEATS - len(new_holdings)
    cash = nav * cash_seats / N_SEATS
    return new_holdings, cash, sells, buys, cash_seats


def process_line_inception(elig, price_now, as_of, eligible_count):
    """Build one line's inception state (NAV=100, first rebalance). Shared
    by both L12 and L6 — see build()."""
    nav = 100.0
    holdings, cash, sells, buys, cash_seats = do_rebalance(nav, [], elig, price_now, as_of)
    rebalance_history = [{
        'date': as_of, 'event': 'inception', 'sells': [], 'buys': buys,
        'holdings': [{'ticker': h['ticker'], 'rank': h['rank'], 'score': h['score'],
                      'units': round(h['units'], 6)} for h in holdings],
        'eligible_count': eligible_count, 'cash_seats': cash_seats, 'n_sells': 0,
    }]
    line_state = {
        'cash': cash,
        'holdings': holdings,
        'rebalance_history': rebalance_history,
        # computed off the just-built rebalance_history (not []) so a same-day
        # rerun is idempotent from the very first write — flags must not
        # change between the inception write and the next run's recompute.
        'flags': compute_turnover_flags(rebalance_history),
    }
    return line_state, nav


def process_line_update(line_key, elig, price_now, as_of, is_new_month, line_state,
                         eligible_count, data_gaps_out):
    """Mark-to-market (and rebalance, if is_new_month) one line's existing
    state in place. Shared by both L12 and L6 — see build(). Returns
    (nav_now, changelog_event_or_None)."""
    cash = line_state['cash']
    holdings = line_state['holdings']

    if is_new_month:
        nav_pre, stale = mark_to_market(cash, holdings, price_now)
        if stale:
            print(f"    ! [{line_key}] stale price carried forward pre-rebalance for {stale}")
            data_gaps_out.append({'date': as_of, 'line': line_key,
                                  'reason': 'stale price pre-rebalance', 'tickers': stale})
        new_holdings, new_cash, sells, buys, cash_seats = do_rebalance(
            nav_pre, holdings, elig, price_now, as_of)
        rebalance_entry = {
            'date': as_of, 'event': 'rebalance', 'sells': sells, 'buys': buys,
            'holdings': [{'ticker': h['ticker'], 'rank': h['rank'], 'score': h['score'],
                          'units': round(h['units'], 6)} for h in new_holdings],
            'eligible_count': eligible_count, 'cash_seats': cash_seats, 'n_sells': len(sells),
        }
        if line_state['rebalance_history'] and line_state['rebalance_history'][-1]['date'] == as_of:
            line_state['rebalance_history'][-1] = rebalance_entry
        else:
            line_state['rebalance_history'].append(rebalance_entry)
        line_state['holdings'] = new_holdings
        line_state['cash'] = new_cash
        nav_now = nav_pre  # equal-weight reset conserves total NAV, no transaction cost
        event = (f"[{line_key}] 月度機械換倉：賣出 {sells or ['無']}，買入 {buys or ['無']}，"
                 f"持股 {[h['ticker'] for h in new_holdings]}，現金席位 {cash_seats}。")
    else:
        nav_now, stale = mark_to_market(cash, holdings, price_now)
        if stale:
            print(f"    ! [{line_key}] stale price carried forward for {stale}")
            data_gaps_out.append({'date': as_of, 'line': line_key, 'reason': 'stale price', 'tickers': stale})
        # informational refresh only (rank/score/heat) — composition/units/cash untouched
        for h in holdings:
            if h['ticker'] in elig.index:
                row = elig.loc[h['ticker']]
                h['rank'] = int(row['rank'])
                h['score'] = round(float(row['score']), 2)
                h['heat'] = bool(row['heat'])
        line_state['holdings'] = holdings
        line_state['cash'] = cash
        event = None

    line_state['flags'] = compute_turnover_flags(line_state['rebalance_history'])
    return nav_now, event


def build():
    now = datetime.now(timezone.utc)
    as_of = now.strftime('%Y-%m-%d')
    print(f"=== Price-Momentum (P10) Build: {as_of} ===")

    tickers, sector = build_universe()
    print(f"universe (S&P500 ∪ NQ100_EXTRAS): {len(tickers)}")

    px = yf.download(tickers + ['SPY'], period='2y', interval='1d', auto_adjust=True,
                      group_by='ticker', progress=False, threads=True)
    spy = px['SPY']['Close'].dropna()
    if spy.empty:
        raise FailSafeAbort("SPY price series empty after download")
    spy_close = float(spy.iloc[-1])

    price_now = {}
    rows_l12 = {}
    rows_l6 = {}
    n_sufficient = 0
    for t in tickers:
        try:
            c = px[t]['Close'].dropna()
        except Exception:
            continue
        if len(c):
            price_now[t] = float(c.iloc[-1])
        if len(c) < MIN_CLOSES:
            continue
        n_sufficient += 1
        base, sig_l12, sig_l6 = compute_ticker(c)
        if sig_l12 is not None:
            row = dict(base)
            row.update(sig_l12)
            row['eligible'] = bool(sig_l12['ret'] > 0 and base['above200'])
            rows_l12[t] = row
        if sig_l6 is not None:
            row = dict(base)
            row.update(sig_l6)
            row['eligible'] = bool(sig_l6['ret'] > 0 and base['above200'])
            rows_l6[t] = row
    print(f"price-sufficient (>=253 closes, shared floor for both lines): {n_sufficient}")
    print(f"L12 scored (vol computable): {len(rows_l12)}")
    print(f"L6 scored (vol computable): {len(rows_l6)}")

    if n_sufficient < MIN_PRICE_COVERAGE:
        raise FailSafeAbort(f"price coverage {n_sufficient} < {MIN_PRICE_COVERAGE}")

    elig = {
        'L12': build_elig(rows_l12),
        'L6': build_elig(rows_l6),
    }

    coverage = dict(
        universe=len(tickers), price_sufficient=n_sufficient,
        L12=dict(scored=len(rows_l12), eligible=int(len(elig['L12']))),
        L6=dict(scored=len(rows_l6), eligible=int(len(elig['L6']))),
    )
    print(f"coverage: {coverage}")

    state = load_state()
    data_gaps = []
    nav_now = {}

    if state is None:
        # ── INCEPTION (both lines, same day) ──
        print(f"  · no existing track.json — building inception ({as_of}), both lines")
        lines_state = {}
        for lk in LINE_KEYS:
            line_state, nav = process_line_inception(elig[lk], price_now, as_of, coverage[lk]['eligible'])
            lines_state[lk] = line_state
            nav_now[lk] = nav
            print(f"    {lk} holdings: {[h['ticker'] for h in line_state['holdings']]}")
        state = {
            'schema': 'price-momentum-v2',
            'prereg': PREREG,
            'as_of': as_of,
            'inception_date': as_of,
            'spy_close_inception': round(spy_close, 2),
            'last_rebalance_month': month_of(as_of),
            'nav_series': [],
            'lines': lines_state,
            'data_gaps': [],
            'changelog': [{
                'date': as_of,
                'event': 'P10 雙線（L12/L6）PREREG 凍結（2026-09-01），兩線同日 inception。',
            }],
        }
    else:
        # ── WEEKLY UPDATE (both lines, shared last_rebalance_month trigger) ──
        is_new_month = month_of(as_of) != state.get('last_rebalance_month')
        changelog_events = []
        for lk in LINE_KEYS:
            nav, event = process_line_update(
                lk, elig[lk], price_now, as_of, is_new_month,
                state['lines'][lk], coverage[lk]['eligible'], data_gaps)
            nav_now[lk] = nav
            if event:
                changelog_events.append(event)
        if is_new_month:
            state['last_rebalance_month'] = month_of(as_of)
            for event in changelog_events:
                state['changelog'].append({'date': as_of, 'event': event})

    # ── shared tail: nav_series append/overwrite — runs for BOTH inception
    #    and weekly-update so a same-day rerun is fully idempotent ──
    nav_spy = round(100.0 * spy_close / state['spy_close_inception'], 2)
    nav_entry = {
        'date': as_of, 'nav_L12': round(nav_now['L12'], 2), 'nav_L6': round(nav_now['L6'], 2),
        'nav_spy': nav_spy, 'spy_close': round(spy_close, 2),
    }
    if state['nav_series'] and state['nav_series'][-1]['date'] == as_of:
        state['nav_series'][-1] = nav_entry
    else:
        state['nav_series'].append(nav_entry)
    state['as_of'] = as_of
    state['prereg'] = PREREG  # numbers are frozen; keep the verbatim block in sync regardless
    state['data_gaps'] = (state.get('data_gaps') or []) + data_gaps

    print(f"    nav_L12={nav_now['L12']:.2f}  nav_L6={nav_now['L6']:.2f}  nav_spy={nav_spy:.2f}")
    for lk in LINE_KEYS:
        ls = state['lines'][lk]
        print(f"    {lk}: cash={ls['cash']:.2f}  holdings={[h['ticker'] for h in ls['holdings']]}  "
              f"flags={ls['flags']}")

    return state, coverage


def main():
    try:
        result = build()
    except FailSafeAbort as e:
        print(f"  ✗ fail-safe triggered: {e} — track.json left unchanged")
        sys.exit(0)
    except Exception as e:
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — track.json left unchanged")
        sys.exit(0)

    state, coverage = result
    TRACK_JSON.parent.mkdir(parents=True, exist_ok=True)
    TRACK_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {TRACK_JSON.relative_to(ROOT)}")
    print(f"    coverage: {coverage}")
    for lk in LINE_KEYS:
        ls = state['lines'][lk]
        print(f"    {lk} holdings ({len(ls['holdings'])}): "
              f"{[(h['ticker'], h['rank'], h['score'], h.get('heat')) for h in ls['holdings']]}")
        print(f"    {lk} flags: {ls['flags']}")


if __name__ == '__main__':
    main()
