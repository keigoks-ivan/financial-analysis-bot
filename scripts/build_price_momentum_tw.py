"""
Price-Momentum TW (P10-TW) weekly paper-track builder — feeds
docs/research/price-momentum-tw/track.json.

WHAT THIS IS
------------
P10-TW is the Taiwan-market mirror of P10 (scripts/build_price_momentum.py):
the same zero-fundamentals, fully mechanical, self-accounting-NAV pure
price-momentum paper track, run on TWSE-listed common stocks against a
0050.TW (元大台灣50) benchmark instead of the S&P 500 / SPY. Per design spec
(notes/site-internal/root/_p10_tw_design_spec_20260916.md §二), only THREE
things differ from the US line: (1) the stock universe — source, plus a
liquidity gate the US line gets for free from S&P 500 membership; (2) the
benchmark; (3) kill condition #2, which has no TW analogue and is marked
not applicable. Every other rule, threshold, formula and code path below is
copied byte-identical from build_price_momentum.py. Like the US line, this
is NOT a convergence surface: zero human intervention at the single-name
level, does not feed the DD verdict chain, does not enter picks/GRP/
three-track/cockpit, must not be cited as "ticker X is on P10-TW" grounds
for a position decision.

P10-TW runs TWO independent mechanical lines side by side from inception
(no retrofit history to narrate here, unlike the US line's 2026-09-01
L12->L12+L6 expansion): L12 (12-1 lookback) and L6 (6-1 lookback) — the
ONLY variable that differs between them; everything else (eligibility
shape, heat flag, buy/hold buffer, monthly rebalance, equal-weight reset,
cash seats, turnover accounting) is byte-identical code shared by both
lines.

FROZEN SPEC (PREREG'd 2026-09-16 — LOCKED, do not tune here)
--------------------------------------------------------------
Universe  : TWSE-listed companies (證交所 OpenAPI t187ap03_L, browser UA,
            requests, timeout 60). Keep 4-digit numeric 公司代號 only
            (excludes ETF/warrants/preferred shares); financials are KEPT
            (P10 is a pure-price series — the US line doesn't exclude any
            GICS sector either). TPEx (上櫃) is not included. Each name
            carries `name` (公司簡稱) and `sector` (產業別 code -> Chinese
            name via a hardcoded table; codes not in the table -> '未分類').
            A liquidity gate then narrows the >=253-close-sufficient names
            to this week's SCORING universe: rank by the trailing
            120-session median of Close*Volume, descending (ties broken by
            ticker code ascending), keep the top 300 — the TW-side
            mechanical analogue of the US line's "S&P 500 membership"
            large-cap proxy. Only these 300 names score on L12/L6 each
            week; a name that drops out of the top 300 is simply absent
            from that week's eligible set, same treatment as an index
            deletion on the US line (§11 of the design spec).
Signal (L12, slow line — unchanged from US line):
              c = a ticker's dropna'd adjusted-close series (>= 253 closes,
              else excluded from coverage).
              ret_12_1 = c.iloc[-22] / c.iloc[-253] - 1   (12-1 momentum:
                the standard skip-most-recent-month 11-month return)
              win = c.iloc[-253:-21]
              vol = win.pct_change().dropna().std() * sqrt(252)  (annualized
                vol over the SAME window as the return)
              score = ret_12_1 / vol.  vol == 0 or NaN -> excluded from L12.
Signal (L6, fast line): the ONLY delta from L12 is the lookback window;
  everything else below is shared.
              ret_6_1 = c.iloc[-22] / c.iloc[-127] - 1   (6-1 momentum:
                skip-most-recent-month 5-month return; 127 mirrors the US
                line's build_momentum5.py-derived convention)
              win = c.iloc[-127:-21]
              vol = win.pct_change().dropna().std() * sqrt(252)
              score = ret_6_1 / vol.  vol == 0 or NaN -> excluded from L6.
Eligibility (all price-only, zero fundamentals; deliberately no +250%
veto and no revision/earnings/valuation gate; shared shape, evaluated
independently per line off that line's own ret):
  1. ret_{12,6}_1 > 0                  (absolute-momentum bear-market valve)
  2. c.iloc[-1] > 200DMA (< 200 closes -> excluded; structurally unreachable
     here since the >=253 coverage floor already implies >= 200) — SAME
     200DMA gate for both lines.
  Heat flag (informational only, NOT a veto, shared by both lines — a
  property of the NAME, not of a line): plain 12M return
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
    same day. NAV = 100.0 for each line; nav_bench normalized to 100 the
    same day off 0050.TW's close (one shared benchmark series).
  - Every run (weekly) marks each line to market: NAV = cash + sum(units *
    that ticker's latest close). 0050.TW tracked once, shared.
  - Rebalance trigger: this run's calendar month != last_rebalance_month
    -> mark BOTH lines to market FIRST (on their outgoing holdings), THEN
    execute each line's rebalance at that same day's close. ONE shared
    last_rebalance_month drives both lines.
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
  2028-09-16 / 24 months, with turnover (#3) allowed to fire early; these
  apply INDEPENDENTLY to each line):
  1. 24-month NAV trails 0050.TW AND max drawdown is worse than 0050.TW ->
     close (per line).
  2. NOT APPLICABLE — no Momentum-5/shadow (revision-momentum) analogue
     exists on the TW side to reconcile against.
  3. turnover_12m_annualized > 300% -> the buffer-band design has failed,
     back to the drawing board (may fire before 24 months); 300% is a
     shared cost-viability threshold for BOTH lines, not a fairness knob.
Multiple-testing honesty: running two lines raises the odds one "wins" by
  luck alone. Winning requires beating BOTH 0050.TW AND the other line,
  with max drawdown no worse. A losing line is recorded and closed — no
  re-tuning, no re-adding it later.
50/50 blend: a derived quantity computable at any time straight off the
  two nav_series — never a third line, never promoted to a formal rule
  without a fresh PREREG.
Trading-calendar note: TW trades roughly 245 sessions/year vs. the US
  line's ~252; MIN_CLOSES=253 is deliberately left untouched (not tuned
  down for TW) — it works out to about 12.4 months of TW sessions, and the
  page discloses this rather than adjusting the constant.

FAIL-SAFE
---------
Any of the following -> print a warning, exit 0, and leave track.json
completely untouched:
  - TWSE OpenAPI t187ap03_L fetch fails, or yields < 700 four-digit codes.
  - Fewer than 250 tickers (across ALL TWSE-listed 4-digit codes, not just
    the liquidity-gated top 300) clear the >=253-close price-sufficiency
    floor, AFTER exhausting the download retry budget below.
  - 0050.TW's price series comes back empty after exhausting the retry
    budget.
  - Any uncaught exception anywhere in the build (top-level try/except
    around main()).

DOWNLOAD RESILIENCE (copied verbatim from build_price_momentum.py)
--------------------------------------------------------------------------
tickers + ['0050.TW'] is downloaded in ~100-ticker batches (identical
download kwargs per batch), concatenated into one DataFrame with the exact
same px[ticker]['Close'] access shape. The whole batched download is
retried up to 4 attempts total, with exponential backoff + jitter (~20s /
60s / 150s) between attempts, whenever 0050.TW comes back empty OR price
coverage on that attempt is below MIN_PRICE_COVERAGE_TW. Only after all
attempts fail does this escalate to the FAIL-SAFE abort above. When running
under GitHub Actions (GITHUB_ACTIONS env var set), a fail-safe abort or any
uncaught exception also emits a `::warning title=P10-TW build skipped::...`
annotation (and a GITHUB_STEP_SUMMARY line when available).

Runs in the weekly-price-momentum-tw GitHub Actions workflow.
"""

import io
import json
import os
import random
import sys
import time
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
TRACK_JSON = ROOT / 'docs' / 'research' / 'price-momentum-tw' / 'track.json'

TWSE_LISTED_URL = 'https://openapi.twse.com.tw/v1/opendata/t187ap03_L'
BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
BENCH_TICKER = '0050.TW'

# 證交所「產業別」代碼 -> 中文名稱，寫死於此（design spec §2.1 指定表）。不在表內
# 的代碼（例如 91＝存託憑證等非上市公司分類）一律歸「未分類」。
SECTOR_MAP = {
    '01': '水泥', '02': '食品', '03': '塑膠', '04': '紡織纖維', '05': '電機機械',
    '06': '電器電纜', '08': '玻璃陶瓷', '09': '造紙', '10': '鋼鐵', '11': '橡膠',
    '12': '汽車', '14': '建材營造', '15': '航運', '16': '觀光餐旅', '17': '金融保險',
    '18': '貿易百貨', '19': '綜合', '20': '其他', '21': '化學', '22': '生技醫療',
    '23': '油電燃氣', '24': '半導體', '25': '電腦及週邊設備', '26': '光電',
    '27': '通信網路', '28': '電子零組件', '29': '電子通路', '30': '資訊服務',
    '31': '其他電子', '32': '文化創意', '33': '農業科技', '34': '電子商務',
    '35': '綠能環保', '36': '數位雲端', '37': '運動休閒', '38': '居家生活',
}

# ── frozen thresholds (byte-identical to build_price_momentum.py — LOCKED,
#    do not tune) ──
MIN_CLOSES = 253            # per-ticker data-sufficiency floor, SHARED by both lines
MA_WINDOW = 200              # 200DMA eligibility gate, shared by both lines
VOL_ANNUALIZE = float(np.sqrt(252))
HEAT_RET12 = 2.5             # plain 12M return > +250% -> informational heat flag, shared
FAR_IDX_L12 = -253           # L12 (slow line) far anchor — 12-1 momentum
FAR_IDX_L6 = -127            # L6 (fast line) far anchor — 6-1 momentum
TOP_BUY = 10                 # buy zone (documented; buys are drawn from the
                              # eligible ranking generally, see do_rebalance)
TOP_HOLD = 40                # hold zone / sell buffer
N_SEATS = 10
TURNOVER_WINDOW = 12         # trailing rebalances for turnover_12m_annualized
TURNOVER_KILL_PCT = 300.0    # kill condition #3 watch threshold, same for both lines
LINE_KEYS = ('L12', 'L6')

# ── TW-specific universe thresholds (design spec §五 — the "換掉的三樣東西"
#    part of the spec, not a tuning of the frozen thresholds above) ──
MIN_LISTED_TW = 700          # fail-safe floor on TWSE OpenAPI 4-digit listed-code count
MIN_PRICE_COVERAGE_TW = 250  # fail-safe floor on >=253-close ticker count, ACROSS ALL
                              # TWSE-listed codes (not just the liquidity-gated 300);
                              # also the download-retry gate threshold
LIQUIDITY_WINDOW = 120       # trailing sessions for the median $-volume liquidity gate
LIQUIDITY_TOP_N = 300        # weekly scoring universe size after the liquidity gate


PREREG = {
    "title": "P10 台股 · 純價格動能 paper track — v0（雙線 L12/L6，PREREG，2026-09-16 凍結）",
    "frozen_date": "2026-09-16",
    "positioning": (
        "P10 台股版是零基本面成分、全機械、自帶 NAV 的純價格動能 paper track——"
        "鏡射美股版 P10（/research/price-momentum/）於台股市場：除股票名單、"
        "基準與資料來源三處外，規則、門檻與程式路徑逐字相同，用意是把兩個市場"
        "的表現差異歸因到市場本身，而不是規則本身。它不是收斂面：不回饋 DD 裁決"
        "鏈、不進 picks/GRP/三軌/cockpit 任何清單，不得被其他 session 引用為"
        "「某檔在 P10 台股上」的選股依據。個股層零人為干預；唯一人類接觸點是 "
        "prereg 的 review points 與 kill conditions。"
    ),
    "universe_and_data": {
        "universe": (
            "上市普通股。來源：證交所 OpenAPI t187ap03_L（上市公司基本資料，"
            "requests、瀏覽器 UA、timeout 60）。保留公司代號為 4 位數字者（排除 "
            "ETF、權證、特別股），金融股保留——P10 是純價格序列，美股版也未排除"
            "任何 GICS 產業。每檔記 name（公司簡稱）與 sector（產業別代碼轉中文，"
            "對照表寫死在 script 裡）。上櫃（TPEx）不納入。"
        ),
        "liquidity_gate": (
            "流動性閘（美股版沒有的一步，因為美股版直接借用 S&P 500 成分當大型股"
            "代理）：在通過 253 筆收盤門檻的名字中，計算最近 120 個交易日「收盤 "
            "× 成交股數」的中位數，降冪排序取前 300 名為本週 universe（同分以代號"
            "字母序 tie-break）。只有這 300 檔進入 L12/L6 計分；掉出前 300 名視為"
            "不合格，於下一次月度換倉賣出，與美股版指數剔除的處理邏輯一致。"
        ),
        "prices": (
            "把全部 4 位數字代號（yfinance 代碼 {代號}.TW）+ 0050.TW 切成每批約 "
            "100 檔，逐批呼叫 yf.download(period='2y', interval='1d', "
            "auto_adjust=True, group_by='ticker', threads=True)（下載參數、批次"
            "與重試邏輯逐字沿用美股版做法），批間 sleep 後合併回同一份 "
            "DataFrame；整批下載失敗（0050 序列是否成功、≥253-close 覆蓋率是否"
            "達標）即指數退避重試，最多 4 次嘗試（約 20s／60s／150s 遞增＋"
            "jitter）。"
        ),
        "sufficiency_floor": "個股資料充足門檻：dropna 後 close series 長度 ≥ 253，否則排除（記入 coverage 統計）。",
    },
    "signal": {
        "definition": "c＝該 ticker dropna 後的還原收盤 series，最後一筆為 t。",
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
        "inception": "Inception：首次執行日 = 首次 rebalance，NAV = 100.0；nav_bench 同日以 0050.TW 收盤 normalize 至 100。",
        "mark_to_market": "每次執行（週更）mark to market：NAV = cash + Σ units × 該檔最新收盤；0050.TW 同步。",
        "rebalance_trigger": "Rebalance 觸發：本次執行的日曆月份 ≠ last_rebalance_month → 先 mark to market，再以當日收盤執行 rebalance。",
        "idempotency": "同日重跑冪等：nav_series 同日期覆蓋不重複 append；同日重跑 rebalance 則以確定性結果覆蓋當日那筆 rebalance_history。",
        "rebalance_history_fields": "rebalance_history 每筆記：date、sells、buys、期末 holdings（ticker/name/rank/score/units）、eligible 數、現金席位數。",
    },
    "turnover": {
        "definition": "每次 rebalance 記 n_sells。turnover_12m_annualized = 近 12 次 rebalance 的 Σ n_sells / 10（不足 12 次先照實際次數年化，標註 partial: true）。",
    },
    "fail_safe": (
        "以下任一 → print warning、exit 0、完全不動 track.json：TWSE OpenAPI 抓取失敗，或 "
        "4 位數字代碼少於 700 筆；價格資料充足（≥253 closes）的 ticker 數少於 250（涵蓋全部"
        "上市代碼，非僅流動性前 300）；0050.TW 序列為空；任何未捕捉例外（top-level try/except "
        "包 main）。"
    ),
    "kill_conditions": {
        "evaluation_point": "正式評估點 2028-09-16（24 個月）；期中讀數可看、不具裁決力。No re-tuning、no re-adding、closed stays closed。",
        "kill_1": "24 個月 NAV 落後 0050.TW 且 Max DD 比 0050.TW 深 → 關閉。",
        "kill_2": "不適用：台股沒有可對帳的 revision-momentum 對照線（美股版對 Momentum-5 shadow line C），本條直接標示不適用，不生成替代條件。",
        "kill_3": "turnover_12m_annualized > 300%（即 12 個月 Σ n_sells > 30）→ 緩衝帶設計失敗，回爐（此條可提前觸發）。",
    },
    "disclosure": (
        "誠實標注：paper track、無交易成本、機械式、非投資建議。不是收斂面，不進任何裁決鏈"
        "（picks/GRP/三軌/cockpit）。個股層零人為干預；唯一人類接觸點是本 prereg 的 review "
        "points 與 kill conditions。本序列與美股版 P10 為同一套規則在不同市場的對照組，差異"
        "只在名單、基準與資料來源三處。"
    ),
    "two_line_expansion": {
        "title": "雙線設計（L12/L6，台股版自 inception 起即雙線並跑，與美股版同一套規則）",
        "objective": "P10 台股版兩條線並跑，回答「慢動能 vs 快動能誰對」，在台股市場對照美股版的同一問題。",
        "l12": "L12（慢線）：即上述訊號/資格/選股緩衝權重/NAV 記帳/換手/fail-safe/kill conditions 全部規格。",
        "l6": (
            "L6（快線）：與 L12 的唯一變數是 lookback，其餘 byte-identical：ret_6_1 = "
            "c.iloc[-22] / c.iloc[-127] - 1（6-1 動能：跳過最近 21 個交易日的 5 個月報酬）；"
            "win = c.iloc[-127:-21]；vol = win.pct_change().dropna().std() * sqrt(252)；"
            "score = ret_6_1 / vol。資格：ret_6_1 > 0 + 同一條 200DMA 閘。資料充足門檻維持 "
            "≥253（刻意：兩線 universe 必須完全相同，否則 lookback 不是唯一變數）。Heat flag "
            "定義不變（plain 12M > +250%，是名字的屬性非訊號的屬性，兩線共用）。top10/top40 "
            "緩衝、月度換倉、等權重置、現金席位、換手統計：全部與 L12 同一套規則、同一套程式"
            "路徑。"
        ),
        "inception": "兩線同日 inception、各自 NAV=100、各自持股/現金/換手記帳，完全獨立。",
        "tie_break": "排序 tie-break：score 同分以 ticker 字母序（穩定排序）——兩線同規則。",
        "turnover_kill_watch_note": "turnover kill watch：僅在滿 12 次 rebalance 窗口觸發——兩線同規則。",
        "multiple_testing_honesty": (
            "多重檢定誠實：兩條線並跑提高其中一條靠運氣贏的機率。「贏」的定義＝同時打敗 "
            "0050.TW 與另一條線，且 Max DD 不更差。輸的線記錄結論後關閉，不重調、不復活。"
        ),
        "per_line_kill_conditions": (
            "Kill conditions 逐線獨立適用：kill ①（vs 0050.TW）與 kill ③（換手 >300%）每條線"
            "各自評，kill ③ 門檻兩線同為 300%——這是成本可行性判準不是公平性判準。kill ②"
            "（vs revision-momentum 對照線）在台股版不適用，兩線皆同。"
        ),
        "blend_clause": (
            "50/50 混合 NAV 是事後衍生物：隨時可從兩條 nav_series 直接計算，不另立第三條線、"
            "不是收斂面；prereg 明文禁止未來 session 以「混合表現好」為由把混合升格為正式線"
            "（那是新規格，須重走 prereg）。"
        ),
    },
    "market_adaptation": {
        "title": "市場調整（台股版與美股版的三處差異；其餘規格逐字相同）",
        "universe_swap": (
            "名單來源由 Wikipedia S&P 500 + NQ100_EXTRAS 換成證交所 OpenAPI 上市公司名冊"
            "（4 位數字代碼、金融股保留、上櫃不納入），並加一道美股版沒有的流動性閘：對通過 "
            "253 筆收盤門檻的名字，取最近 120 個交易日「收盤 × 成交股數」中位數，降冪取前 "
            "300 名為本週 universe——這是用價量資料機械代理「大型股」，功能等同美股版用 "
            "S&P 500 成分篩大型股。"
        ),
        "benchmark_swap": (
            "基準由 SPY 換成元大台灣 50（0050.TW）還原收盤——0050 對台股的代表性等同 SPY "
            "對美股，但集中度更高（成分股中台積電占比約五成到六成）；加權指數 ^TWII 不含"
            "股利、會讓基準變好打，故不用。"
        ),
        "kill_2_swap": (
            "kill ②（與 Momentum-5 shadow line C 對帳）不適用——台股沒有對應的 "
            "revision-momentum 對照線可供對帳，本條在台股版直接標示不適用，不生成替代條件。"
        ),
        "trading_calendar_note": (
            "台股一年約 245 個交易日，MIN_CLOSES=253 筆收盤約等於 12.4 個月，比美股（一年約 "
            "252 個交易日）略長；此常數刻意不因市場調整，維持與美股版逐字相同的資料充足門檻。"
        ),
    },
}


class FailSafeAbort(Exception):
    """Raised for any of the fail-safe conditions above — caught in main()
    to print a warning and exit 0 without touching track.json."""


def fetch_twse_listed():
    """TWSE 上市公司名冊 — OpenAPI t187ap03_L（requests、瀏覽器 UA、timeout
    60），與 minervini-quality-backtest 的 universe_builder.py::fetch_twse_tickers()
    同一種抓法（見 data/universe_builder.py 第 85-105 行）。只保留公司代號為 4
    位數字者（排除 ETF/權證/特別股）；金融股保留（P10 是純價格序列，不排除任何
    產業）。產業別代碼經 SECTOR_MAP 轉中文，不在表內者記「未分類」。回傳
    (code_map, listed_raw)：code_map = {code: {'name': 公司簡稱, 'sector': ...}}，
    listed_raw = API 原始筆數（4 位數字過濾前），供 coverage 揭露用。少於
    MIN_LISTED_TW 筆 4 位數字代碼 → FailSafeAbort。"""
    try:
        resp = requests.get(TWSE_LISTED_URL, headers={'User-Agent': BROWSER_UA}, timeout=60)
        data = resp.json()
    except Exception as e:
        raise FailSafeAbort(f"TWSE OpenAPI t187ap03_L fetch failed ({type(e).__name__}: {e})")

    listed_raw = len(data)
    code_map = {}
    for row in data:
        code = str(row.get('公司代號', '')).strip()
        if not (len(code) == 4 and code.isdigit()):
            continue
        name = str(row.get('公司簡稱', '')).strip()
        ind_code = str(row.get('產業別', '')).strip()
        code_map[code] = {'name': name, 'sector': SECTOR_MAP.get(ind_code, '未分類')}

    if len(code_map) < MIN_LISTED_TW:
        raise FailSafeAbort(
            f"TWSE listed 4-digit codes only {len(code_map)} (< {MIN_LISTED_TW})")
    return code_map, listed_raw


def compute_line_signal(c, far_idx):
    """far_idx = FAR_IDX_L12 (-253, 12-1 momentum) or FAR_IDX_L6 (-127,
    6-1 momentum) — the ONLY variable that differs between the two lines.
    Near anchor is always -22 (skip most-recent 21 trading days); vol
    window is c.iloc[far_idx:-21]. Returns None if vol is 0/NaN (the only
    compute-time exclusion)."""
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
    of a line); sig_l12/sig_l6 = that line's (ret, vol, score), or None if
    that line's vol is 0/NaN."""
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
    since rows were inserted in alphabetical ticker order)."""
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
    """turnover_12m_annualized_pct: sum(n_sells) over the trailing
    TURNOVER_WINDOW rebalances / N_SEATS, expressed as a percent; with fewer
    than TURNOVER_WINDOW rebalances on record, annualize off the actual
    count instead and flag partial: true. Shared by the inception and
    weekly-update paths (and by both lines) so a same-day rerun is fully
    idempotent.

    turnover_kill_watch only arms on a FULL 12-rebalance window: kill
    condition #3 is defined on 12 個月 Σ n_sells > 30, and annualizing a
    partial window extrapolates noise (3 sells at the second rebalance
    would read as 360%)."""
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


# ── download resilience (byte-identical to build_price_momentum.py) ──
DOWNLOAD_BATCH_SIZE = 100
MAX_DOWNLOAD_ATTEMPTS = 4
RETRY_BACKOFF_SECONDS = (20.0, 60.0, 150.0)  # before attempts 2, 3, 4 respectively


def _count_price_sufficient(px, tickers):
    """How many of `tickers` have >=MIN_CLOSES dropna'd closes in `px`.
    Shared by the download-retry gate and build()'s own per-ticker loop so
    both use identical counting logic."""
    n = 0
    for t in tickers:
        try:
            c = px[t]['Close'].dropna()
        except Exception:
            continue
        if len(c) >= MIN_CLOSES:
            n += 1
    return n


def _download_prices_once(all_tickers):
    """One attempt: download all_tickers (already includes BENCH_TICKER) in
    DOWNLOAD_BATCH_SIZE-sized chunks with the SAME yf.download kwargs the
    US line uses, then concat into one DataFrame with the same
    px[ticker]['Close'] column shape. A chunk that raises is skipped (not
    fatal by itself) — the resulting bench/coverage check in the caller
    decides whether this whole attempt counts as a failure."""
    frames = []
    n_chunks = (len(all_tickers) + DOWNLOAD_BATCH_SIZE - 1) // DOWNLOAD_BATCH_SIZE
    for i in range(0, len(all_tickers), DOWNLOAD_BATCH_SIZE):
        chunk = all_tickers[i:i + DOWNLOAD_BATCH_SIZE]
        chunk_no = i // DOWNLOAD_BATCH_SIZE + 1
        try:
            frames.append(yf.download(chunk, period='2y', interval='1d', auto_adjust=True,
                                       group_by='ticker', progress=False, threads=True))
        except Exception as e:
            print(f"      ! batch {chunk_no}/{n_chunks} ({len(chunk)} tickers) raised "
                  f"{type(e).__name__}: {e} — skipped this batch")
        if chunk_no < n_chunks:
            time.sleep(3)
    if not frames:
        raise RuntimeError("all download batches failed")
    return pd.concat(frames, axis=1)


def download_prices_with_retry(tickers):
    """Retry the whole batched download up to MAX_DOWNLOAD_ATTEMPTS times
    with exponential backoff + jitter whenever 0050.TW comes back empty or
    price coverage is short. Returns (px, bench) on success; raises
    FailSafeAbort after the retry budget is exhausted."""
    all_tickers = tickers + [BENCH_TICKER]
    last_reason = None
    for attempt in range(1, MAX_DOWNLOAD_ATTEMPTS + 1):
        print(f"  · price download attempt {attempt}/{MAX_DOWNLOAD_ATTEMPTS} "
              f"({len(all_tickers)} tickers incl. {BENCH_TICKER}, batches of {DOWNLOAD_BATCH_SIZE})")
        try:
            px = _download_prices_once(all_tickers)
            bench = px[BENCH_TICKER]['Close'].dropna()
        except Exception as e:
            last_reason = f"attempt {attempt} raised {type(e).__name__}: {e}"
            print(f"    ! {last_reason}")
        else:
            if bench.empty:
                last_reason = f"attempt {attempt}: {BENCH_TICKER} price series empty after download"
                print(f"    ! {last_reason}")
            else:
                n_sufficient = _count_price_sufficient(px, tickers)
                if n_sufficient < MIN_PRICE_COVERAGE_TW:
                    last_reason = (f"attempt {attempt}: price coverage {n_sufficient} "
                                    f"< {MIN_PRICE_COVERAGE_TW}")
                    print(f"    ! {last_reason}")
                else:
                    print(f"    ✓ attempt {attempt} succeeded: {BENCH_TICKER} ok, "
                          f"coverage {n_sufficient} >= {MIN_PRICE_COVERAGE_TW}")
                    return px, bench
        if attempt < MAX_DOWNLOAD_ATTEMPTS:
            backoff = RETRY_BACKOFF_SECONDS[attempt - 1] + random.uniform(0, 5)
            print(f"    … retrying in {backoff:.0f}s")
            time.sleep(backoff)
    raise FailSafeAbort(
        f"price download failed after {MAX_DOWNLOAD_ATTEMPTS} attempts (last: {last_reason})")


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


def do_rebalance(nav, holdings, elig, price_now, as_of, name_map):
    """Sell anything not in this month's eligible top-40; backfill empty
    seats with the highest-ranked unheld eligible names; reset the WHOLE
    resulting holding set to equal weight NAV/N_SEATS. Shared code path for
    both lines — the caller passes in that line's own elig ranking.
    name_map = {ticker: 公司簡稱} — TW-only addition so each holding also
    carries a display name (design spec §四)."""
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
            'name': name_map.get(t, ''),
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


def process_line_inception(elig, price_now, as_of, eligible_count, name_map):
    """Build one line's inception state (NAV=100, first rebalance). Shared
    by both L12 and L6 — see build()."""
    nav = 100.0
    holdings, cash, sells, buys, cash_seats = do_rebalance(nav, [], elig, price_now, as_of, name_map)
    for h in holdings:
        h['eligible'] = True  # rebalance-fresh holdings are always eligible by construction
    rebalance_history = [{
        'date': as_of, 'event': 'inception', 'sells': [], 'buys': buys,
        'holdings': [{'ticker': h['ticker'], 'name': h.get('name', ''), 'rank': h['rank'],
                      'score': h['score'], 'units': round(h['units'], 6)} for h in holdings],
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
                         eligible_count, data_gaps_out, name_map):
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
            nav_pre, holdings, elig, price_now, as_of, name_map)
        for h in new_holdings:
            h['eligible'] = True  # rebalance-fresh holdings are always eligible by construction
        rebalance_entry = {
            'date': as_of, 'event': 'rebalance', 'sells': sells, 'buys': buys,
            'holdings': [{'ticker': h['ticker'], 'name': h.get('name', ''), 'rank': h['rank'],
                          'score': h['score'], 'units': round(h['units'], 6)} for h in new_holdings],
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
        # informational refresh only (rank/score/heat) — composition/units/cash untouched.
        # every holding carries an explicit `eligible` flag: a holding that dropped out
        # of this line's elig ranking (ret<=0 or below 200DMA) keeps its LAST KNOWN
        # rank/score/heat (staleness carried by the flag, not by blanking the values)
        # instead of being silently skipped.
        for h in holdings:
            h['eligible'] = bool(h['ticker'] in elig.index)
            if h['eligible']:
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
    print(f"=== Price-Momentum TW (P10-TW) Build: {as_of} ===")

    code_map, listed_raw = fetch_twse_listed()
    codes = sorted(code_map.keys())
    tickers = [f"{c}.TW" for c in codes]
    name_map = {f"{c}.TW": info['name'] for c, info in code_map.items()}
    print(f"TWSE listed 4-digit codes: {len(tickers)} (raw API rows: {listed_raw})")

    px, bench = download_prices_with_retry(tickers)
    bench_close = float(bench.iloc[-1])

    price_now = {}
    price_sufficient = []
    n_price_sufficient_all = 0
    for t in tickers:
        try:
            c = px[t]['Close'].dropna()
        except Exception:
            continue
        if len(c):
            price_now[t] = float(c.iloc[-1])
        if len(c) < MIN_CLOSES:
            continue
        n_price_sufficient_all += 1
        price_sufficient.append(t)
    print(f"price-sufficient (>=253 closes, ALL TWSE listed): {n_price_sufficient_all}")

    if n_price_sufficient_all < MIN_PRICE_COVERAGE_TW:
        raise FailSafeAbort(f"price coverage {n_price_sufficient_all} < {MIN_PRICE_COVERAGE_TW}")

    # ── liquidity gate (design spec §2.1): among price-sufficient names,
    #    rank by trailing 120-session median Close*Volume, descending; keep
    #    top LIQUIDITY_TOP_N. Ties broken by ticker code ascending — built
    #    by iterating price_sufficient in alphabetical order (already sorted
    #    from `tickers`) then a stable sort, per the same tie-break
    #    convention build_elig() uses. ──
    liq_rows = []
    for t in price_sufficient:  # already alphabetical (derived from sorted codes)
        try:
            dv = (px[t]['Close'] * px[t]['Volume']).dropna()
        except Exception:
            continue
        if dv.empty:
            continue
        liq_rows.append((t, float(dv.iloc[-LIQUIDITY_WINDOW:].median())))
    liq_rows.sort(key=lambda x: x[1], reverse=True)  # stable: ties keep alphabetical order
    universe = [t for t, _ in liq_rows[:LIQUIDITY_TOP_N]]
    print(f"liquidity universe (top {LIQUIDITY_TOP_N} by {LIQUIDITY_WINDOW}d median $ volume): {len(universe)}")

    rows_l12 = {}
    rows_l6 = {}
    for t in universe:
        c = px[t]['Close'].dropna()
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
    print(f"L12 scored (vol computable): {len(rows_l12)}")
    print(f"L6 scored (vol computable): {len(rows_l6)}")

    elig = {
        'L12': build_elig(rows_l12),
        'L6': build_elig(rows_l6),
    }

    coverage = dict(
        listed_raw=listed_raw,
        price_sufficient_all=n_price_sufficient_all,
        universe=len(universe),
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
            line_state, nav = process_line_inception(
                elig[lk], price_now, as_of, coverage[lk]['eligible'], name_map)
            lines_state[lk] = line_state
            nav_now[lk] = nav
            print(f"    {lk} holdings: {[h['ticker'] for h in line_state['holdings']]}")
        state = {
            'schema': 'price-momentum-tw-v1',
            'benchmark': BENCH_TICKER,
            'prereg': PREREG,
            'as_of': as_of,
            'inception_date': as_of,
            'bench_close_inception': round(bench_close, 2),
            'last_rebalance_month': month_of(as_of),
            'nav_series': [],
            'lines': lines_state,
            'data_gaps': [],
            'changelog': [{
                'date': as_of,
                'event': 'P10 台股（雙線 L12/L6）PREREG 凍結（2026-09-16），兩線同日 inception。',
            }],
        }
    else:
        # ── WEEKLY UPDATE (both lines, shared last_rebalance_month trigger) ──
        is_new_month = month_of(as_of) != state.get('last_rebalance_month')
        changelog_events = []
        for lk in LINE_KEYS:
            nav, event = process_line_update(
                lk, elig[lk], price_now, as_of, is_new_month,
                state['lines'][lk], coverage[lk]['eligible'], data_gaps, name_map)
            nav_now[lk] = nav
            if event:
                changelog_events.append(event)
        if is_new_month:
            state['last_rebalance_month'] = month_of(as_of)
            for event in changelog_events:
                state['changelog'].append({'date': as_of, 'event': event})

    # ── shared tail: nav_series append/overwrite — runs for BOTH inception
    #    and weekly-update so a same-day rerun is fully idempotent ──
    nav_bench = round(100.0 * bench_close / state['bench_close_inception'], 2)
    nav_entry = {
        'date': as_of, 'nav_L12': round(nav_now['L12'], 2), 'nav_L6': round(nav_now['L6'], 2),
        'nav_bench': nav_bench, 'bench_close': round(bench_close, 2),
    }
    if state['nav_series'] and state['nav_series'][-1]['date'] == as_of:
        state['nav_series'][-1] = nav_entry
    else:
        state['nav_series'].append(nav_entry)
    state['as_of'] = as_of
    state['prereg'] = PREREG  # numbers are frozen; keep the verbatim block in sync regardless
    state['data_gaps'] = (state.get('data_gaps') or []) + data_gaps

    print(f"    nav_L12={nav_now['L12']:.2f}  nav_L6={nav_now['L6']:.2f}  nav_bench={nav_bench:.2f}")
    for lk in LINE_KEYS:
        ls = state['lines'][lk]
        print(f"    {lk}: cash={ls['cash']:.2f}  holdings={[h['ticker'] for h in ls['holdings']]}  "
              f"flags={ls['flags']}")

    return state, coverage


def _existing_track_as_of():
    """Best-effort read of the current track.json's as_of, for the GH
    Actions warning annotation below. Must never raise — a missing or
    corrupt file just reads as unknown."""
    try:
        if TRACK_JSON.exists():
            return json.loads(TRACK_JSON.read_text(encoding='utf-8')).get('as_of')
    except Exception:
        pass
    return None


def _emit_gh_skip_warning(reason):
    """A fail-safe abort or uncaught exception used to be a silent exit 0
    (green workflow run, no trace). When running under GitHub Actions, also
    emit a `::warning::` workflow command so it shows up in the run
    summary, plus a GITHUB_STEP_SUMMARY line when available. No-op on a
    local run (keeps local output clean)."""
    if not os.environ.get('GITHUB_ACTIONS'):
        return
    stale_as_of = _existing_track_as_of() or '（無既有 track.json）'
    msg = f"{reason}；track.json 未更新，本週資料停在 {stale_as_of}"
    print(f"::warning title=P10-TW build skipped::{msg}")
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_path:
        try:
            with open(summary_path, 'a', encoding='utf-8') as f:
                f.write(f"- ⚠️ **P10-TW build skipped** — {msg}\n")
        except Exception:
            pass


def main():
    try:
        result = build()
    except FailSafeAbort as e:
        print(f"  ✗ fail-safe triggered: {e} — track.json left unchanged")
        _emit_gh_skip_warning(f"fail-safe triggered: {e}")
        sys.exit(0)
    except Exception as e:
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — track.json left unchanged")
        _emit_gh_skip_warning(f"build failed ({type(e).__name__}: {e})")
        sys.exit(0)

    state, coverage = result
    TRACK_JSON.parent.mkdir(parents=True, exist_ok=True)
    TRACK_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f"  ✓ wrote {TRACK_JSON.relative_to(ROOT)}")
    print(f"    coverage: {coverage}")
    for lk in LINE_KEYS:
        ls = state['lines'][lk]
        print(f"    {lk} holdings ({len(ls['holdings'])}): "
              f"{[(h['ticker'], h['name'], h['rank'], h['score'], h.get('heat')) for h in ls['holdings']]}")
        print(f"    {lk} flags: {ls['flags']}")


if __name__ == '__main__':
    main()
