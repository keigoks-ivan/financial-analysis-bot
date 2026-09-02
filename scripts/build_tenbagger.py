#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_tenbagger.py — 第三軌「十倍・結構長坡」發現引擎，寫 docs/picks/tenbagger.json。

WHAT THIS IS
------------
真・十倍股發現層。掃 S&P 400（中型）+ S&P 600（小型）約 1,000 檔 universe，
用持有人的「結構六條件」機械化成 gate-set（現 v0.1），找還在 DD universe 市值門檻
（$200 億）之下、體質已具十倍胚胎（高成長 × 定價權 × 內部人 skin-in-the-game
× 低稀釋 × 自籌資力 × 估值防線）的中小型股。這是與前兩軌互補的發現層——
市值太小、尚未經 DD 深度驗證，風險等級高於「長熬」「爆發」兩組。

治理模型同 build_picks.py：規則自動上榜（rank by 最近 4 季營收 yoy 中位數，v0.2）＋ 持有人 veto
（讀 docs/picks/picks.json 的 veto[]，本檔只讀不寫）。SEAT_CAP_10X＝5 進正式榜，
next 15 進候選區。

CADENCE
-------
月頻（前兩軌週頻）。掛在 weekly workflow 裡但用 21 天 cadence guard 節流——
若既有 tenbagger.json 的 refreshed_at 距今 < 21 天且無 --force → 印 skip、exit 0。
有效上等於「月頻刷新」。

FAIL-SAFE（mirrors build_picks.py / build_momentum5.py culture）
----------------------------------------------------------------
yfinance 逐檔容錯（單檔失敗跳過）。若最終 coverage < universe 的 60% →
印 warning、保留既有檔案不覆蓋、exit 0，讓頁面留住上一份好資料而非渲染破榜。

GATE-SET v0.1（2026-07-05，持有人拍板結構修正）
------------------------------------------------
v0 的成長 gate 用「最近季 yoy ≥25%」單點代理，實證放進運價/週期尖峰假陽性
（LPG +105%、INSW +78% 油輪循環誤入正式榜）。v0.1 結構修正：
  - 成長主閘改「3 年營收 CAGR ≥20%」（annual income_stmt Total Revenue；
    4 欄→3Y CAGR、3 欄→2Y 年化並標示、<3 欄→史料不足淘汰）——要求成長是
    「持續的」而非單季尖峰；季 yoy ≥15% 降為確認條件（仍在成長，非已見頂）。
  - 稀釋主源改 annual balance_sheet 'Ordinary Shares Number'（as-reported
    年度股數，對 IPO 期雜訊穩定——治 CAVA −20.5%/y 假負稀釋 artifact）；
    get_shares_full split-adjusted 路徑降為 fallback，逐檔記 dilution_source。
門檻 20/15 圓整數未調參。

SPLIT-ADJUSTED DILUTION（已驗證的雷，fallback 路徑仍強制修正）
------------------------------------------------
get_shares_full 的股數 CAGR **必須先除掉區間內的分割因子**（tk.splits 累乘）
——否則 SMCI 這種 10:1 分割會被讀成 +134%/年的假稀釋而被誤殺。此修正為強制項。

RANK KEY v0.2（2026-09-02，持有人拍板——治「最近一次爆發性成長」基期效應）
------------------------------------------------
v0.1 排序鍵「3 年營收 CAGR」與「最近一次起漲點多近」高度等價：低基期起漲的名字
天生贏過穩健複利的名字（TGTX +505%，基期僅約 $280 萬——單一年度的分母效應，不
是九倍坡道的證據）。v0.2 改排序鍵為「最近 4 季營收 yoy 的中位數」（quarterly_
income_stmt 的 Total Revenue，逐季配對約一年前同季算 yoy，取中位數）——量的是
「最近是否持續成長」而非單一起訖點的比值，較不受單季基期異常主導；3 年 CAGR
（rev_cagr_3y）保留為既有主閘（gate_rev_cagr 不變）與顯示欄，不下架。輸出 JSON
記 `rank_key_version: "v0.2"`（gate_version 仍是 v0.1——本次只換排序鍵，六條件
gate-set 本身未動）。

同一輪冷讀（G7：notes/site-internal/dd/_coldread_20260902/G7_tenbagger.md；
Part D3：notes/site-internal/root/_picks_first_principles_review_20260902.md）
另指出本 gate-set 完全沒有「坡道還有多長」這一軸——TGTX（單一產品 ~95%＋類別
生物相似藥 2029+ 到期）、HRMY（單一產品 ~100%＋學名藥 2029-09 到期）這類「近三
年漲得快但終局已在望」的名字，六條件機械閘全數放行。v0.2 不新增機械 veto
gate（單一產品佔比／專利到期年／TAM 上限這三者跨產業口徑不可比、自動化易誤
殺或誤放），改為三個**持有人手填顯示欄**：`single_product_pct`（單一產品營收
占比）／`patent_expiry_year`（主要專利或獨占到期年）／`tam_cap_note`（TAM 上
限估，文字）。讀 `docs/picks/picks.json` 的可選鍵 `tenbagger_notes{TICKER:{...}}`
（本檔對 picks.json 只讀不寫，veto[] 同源沿用既有慣例）；缺填 → 三欄皆 null、
`runway_status="坡長未知"`；`single_product_pct ≥ 70` 或
`patent_expiry_year ≤ 今年+5` → `runway_status="短坡警示"`；否則
`runway_status="已填"`。**這三欄與 runway_status 純顯示，不影響 gate 通過/淘
汰**（Part D3 拍板：本軌是發現層不是收斂面，見上 CADENCE／treatment 段）。
"""
import io
import json
import os
import sys
import time
import warnings
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
PICKS = os.path.join(DOCS, "picks", "picks.json")
OUT = os.path.join(DOCS, "picks", "tenbagger.json")

TW8 = timezone(timedelta(hours=8))

WIKI_400 = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
WIKI_600 = "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"
BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

# ── fetch / cadence knobs ──
WORKERS = 8
CADENCE_DAYS = 21          # < 21 天且無 --force → skip（有效月頻）
COVERAGE_FLOOR = 0.60      # coverage < 60% universe → fail-safe，保留舊檔
SEAT_CAP_10X = 5           # 正式榜席位（持有人 2026-07-05 再拍板 10→5，與另兩組一致）
CAND_CAP = 15             # 候選區席位（正式榜之後接續 15 檔）

# ── 結構六條件 → gate-set v0.1（frozen constants，未調參）────────────────
# 這些門檻是十倍發現層的 pre-registered 規則。**未調參**——調參前先跟持有人討論
# 方法（優化 logic/structure 不是 tune 數字，避免 in-sample overfit）。
GATE_VERSION = "v0.1"
RANK_KEY_VERSION = "v0.2"  # 2026-09-02：排序鍵改「最近 4 季營收 yoy 中位數」（gate-set 本身未動，見上 docstring）
CAP_LO = 1e9               # 市值地板 $10 億（太小流動性/資料品質不可靠）    未調參
CAP_HI = 20e9             # 市值天板 $200 億——DD universe 地板之下＝發現層互補   未調參
# v0.1 成長雙閘：v0 的「最近季 yoy ≥25%」單點代理會放進運價/週期尖峰（實證：
# LPG +105%、INSW +78% 油輪循環誤入正式榜）；3 年 CAGR 要求成長是「持續的」，
# 季 yoy 下修為確認條件。門檻 20/15 圓整數未調參。
MIN_REV_CAGR = 0.20       # 主閘：3 年營收 CAGR ≥ 20%（annual income_stmt）      未調參
MIN_REV_YOY = 0.15        # 確認：最近季 yoy ≥ 15%（仍在成長，非已見頂）          未調參
MIN_GROSS_MARGIN = 0.35   # 毛利率 ≥ 35%（定價權地板）                          未調參
MIN_INSIDER = 0.05        # 內部人持股 ≥ 5%（skin in the game）；缺→放行不殺    未調參
MAX_SHARE_CAGR = 0.03     # 股數 CAGR ≤ 3%/年（split-adjusted）；缺→淘汰
#                            稀釋是十倍路上最大的隱形稅——寧可資料缺就保守淘汰   未調參
SELFFUND_CASH_MULT = 2.0  # 燒錢者需 現金 ≥ 2×|FCF|（自籌資力）                 未調參
MAX_EV_S = 15.0           # EV/Sales ≤ 15（估值防線，避免買在已定價完的夢）     未調參


def warn(msg):
    print(f"[build_tenbagger] WARN: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Universe（S&P 400 + 600，Wikipedia constituents，browser UA）
# ---------------------------------------------------------------------------
def fetch_constituents(url):
    """回傳該 Wikipedia 頁 constituents 表的 ticker list（'.'→'-'）。失敗 raise。"""
    html = requests.get(url, headers={"User-Agent": BROWSER_UA}, timeout=60).text
    tables = pd.read_html(io.StringIO(html))
    for tb in tables:
        cols = [str(c).strip() for c in tb.columns]
        symcol = None
        for orig, name in zip(tb.columns, cols):
            if name.lower() in ("symbol", "ticker symbol", "ticker"):
                symcol = orig
                break
        if symcol is not None and len(tb) > 100:
            syms = (
                tb[symcol].astype(str)
                .str.replace(".", "-", regex=False)
                .str.strip()
                .tolist()
            )
            return [s for s in syms if s and s.lower() != "nan"]
    raise RuntimeError(f"找不到 constituents 表：{url}")


def build_universe():
    seen, universe = set(), []
    for label, url in (("S&P 400", WIKI_400), ("S&P 600", WIKI_600)):
        try:
            syms = fetch_constituents(url)
            print(f"[build_tenbagger] {label}: {len(syms)} 檔")
        except Exception as e:
            warn(f"{label} constituents 抓取失敗（{type(e).__name__}: {e}）")
            syms = []
        for s in syms:
            if s not in seen:
                seen.add(s)
                universe.append(s)
    return universe


# ---------------------------------------------------------------------------
# Split-adjusted share-count CAGR（強制除分割因子）
# ---------------------------------------------------------------------------
def share_cagr_split_adjusted(tk, start_dt):
    """回傳 (cagr, note) 或 (None, reason)。

    raw 股數 CAGR 會把 10:1 分割讀成假稀釋；此處把區間內 tk.splits 累乘除掉，
    把最早的股數還原到最新的分割基準上，CAGR 才是真稀釋。
    """
    try:
        shares = tk.get_shares_full(start=start_dt)
    except Exception as e:
        return None, f"get_shares_full 失敗（{type(e).__name__}）"
    if shares is None or len(shares) < 2:
        return None, "股數序列不足"
    shares = shares.dropna()
    if len(shares) < 2:
        return None, "股數序列不足"
    if getattr(shares.index, "tz", None) is not None:
        shares.index = shares.index.tz_localize(None)

    first_date, last_date = shares.index[0], shares.index[-1]
    first_val, last_val = float(shares.iloc[0]), float(shares.iloc[-1])
    if first_val <= 0 or last_val <= 0:
        return None, "股數 ≤ 0"

    # 區間內分割累乘（strictly after first_date, up to last_date）
    cum_split = 1.0
    try:
        splits = tk.splits
        if splits is not None and len(splits):
            if getattr(splits.index, "tz", None) is not None:
                splits.index = splits.index.tz_localize(None)
            win = splits[(splits.index > first_date) & (splits.index <= last_date)]
            for v in win.values:
                fv = float(v)
                if fv and fv > 0:
                    cum_split *= fv
    except Exception:
        cum_split = 1.0  # 拿不到 splits 就當無分割（保守：不誇大也不誤殺 raw）

    # 把最早股數還原到最新分割基準（× 之後發生的分割因子）
    adj_first = first_val * cum_split
    years = (last_date - first_date).days / 365.25
    if years <= 0 or adj_first <= 0:
        return None, "區間過短"
    cagr = (last_val / adj_first) ** (1.0 / years) - 1.0
    note = f"{years:.1f}y・split×{cum_split:.0f}" if cum_split != 1.0 else f"{years:.1f}y"
    return cagr, note


# ---------------------------------------------------------------------------
# Per-ticker fetch（三段式：.info 全掃 → income_stmt 只對 stage-1 存活者 →
# 稀釋（balance_sheet/get_shares_full）只對 stage-2 存活者。phase-1 每檔只打
# 一支 endpoint，Yahoo rate-limit（Invalid Crumb 401）壓力最小；配 retry +
# recovery sweep 把被限流的補回。）
# ---------------------------------------------------------------------------
INFO_RETRIES = 3


def fetch_info_one(t):
    """只抓 .info（帶 retry/backoff）。回傳 rec dict 或 None。"""
    for k in range(INFO_RETRIES):
        try:
            info = yf.Ticker(t).info or {}
        except Exception:
            info = {}
        if info and info.get("marketCap") is not None:
            return {
                "ticker": t,
                "name": info.get("shortName") or t,
                "sector": info.get("sector") or "",
                "marketCap": info.get("marketCap"),
                "revenueGrowth": info.get("revenueGrowth"),
                "grossMargins": info.get("grossMargins"),
                "heldPercentInsiders": info.get("heldPercentInsiders"),
                "freeCashflow": info.get("freeCashflow"),
                "totalCash": info.get("totalCash"),
                "enterpriseToRevenue": info.get("enterpriseToRevenue"),
                "share_cagr": None,
                "share_cagr_note": None,
            }
        time.sleep(1.5 * (k + 1))  # 限流退避（Invalid Crumb 多為短暫 rate-limit）
    return None


def _sweep(tickers, workers, label):
    recs, done, total = {}, 0, len(tickers)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fetch_info_one, t): t for t in tickers}
        for f in as_completed(futs):
            done += 1
            try:
                r = f.result()
            except Exception:
                r = None
            if r is not None:
                recs[r["ticker"]] = r
            if done % 100 == 0:
                print(f"[build_tenbagger] {label} {done}/{total}（有效 {len(recs)}）")
    return recs


def fetch_universe(universe):
    """Phase 1：.info 全掃 + recovery sweep 補限流檔。回傳 rec dict list。"""
    recs = _sweep(universe, WORKERS, "info 掃描")
    missing = [t for t in universe if t not in recs]
    # recovery sweep：被 rate-limit 掉的用低併發＋退避補一輪
    if missing and len(recs) / max(1, len(universe)) < 0.90:
        print(f"[build_tenbagger] recovery sweep：{len(missing)} 檔限流未取，"
              f"降併發重試（sleep 8s 讓 Yahoo crumb 冷卻）")
        time.sleep(8)
        rec2 = _sweep(missing, max(2, WORKERS // 3), "recovery")
        recs.update(rec2)
    out = list(recs.values())
    print(f"[build_tenbagger] info 完成：{len(out)}/{len(universe)} 有效")
    return out


# 各 fetch phase 健康度（main 據此判「funnel 崩塌是限流不是真篩選」→ fail-safe）
FETCH_HEALTH = {}
GROWTH_FETCH_FLOOR = 0.70  # income_stmt 成功率 < 70% → 不寫檔（保留上一份好資料）


def attach_growth(survivors):
    """Phase 2（v0.1）：只對 stage-1 存活者抓 annual income_stmt 算 3 年營收 CAGR。

    income_stmt 是額外一支 call——先用 cap/margin/insider 卡到 ~100-400 檔再抓。
    4 欄年報 → 3Y CAGR；3 欄 → 2Y 年化（rev_cagr_years=2 標示）；有資料但 <3 欄
    （不足 2 個年度區間）→ status=short_history（上市歷史不足，gate 淘汰）。

    抗限流（2026-07-05 實跑教訓：1000 檔 info 掃描後緊接 income_stmt 被 Yahoo
    限流到 14/124，「抓取失敗」被誤當「史料不足」殺掉 110 檔，差點寫出空榜）：
      - fetch 失敗與史料不足分開記（status: ok / short_history / no_data），
        funnel 各自一行，失敗永遠可見不沉默；
      - 先冷卻 10s、低併發（2-4 workers）＋逐檔 retry/backoff；
      - no_data 者再跑 2 輪 sequential recovery（逐檔間隔 1-2s，完整性優先於速度）；
      - main 端：成功率 < GROWTH_FETCH_FLOOR → 不寫檔。
    """
    if not survivors:
        FETCH_HEALTH["growth_success_frac"] = 1.0
        return

    def work(r):
        r["rev_cagr"], r["rev_cagr_years"] = None, None
        r["rev_cagr_status"] = "no_data"
        inc = None
        for k in range(3):
            try:
                inc = yf.Ticker(r["ticker"]).income_stmt
            except Exception:
                inc = None
            if inc is not None and not inc.empty:
                break
            time.sleep(1.5 * (k + 1))  # 限流退避
        if inc is None or inc.empty:
            return r  # 全部 retry 失敗 → no_data（抓取失敗，非史料不足）
        if "Total Revenue" not in inc.index:
            r["rev_cagr_status"] = "short_history"  # 有回資料但無營收列——當史料不足
            return r
        rev = inc.loc["Total Revenue"].dropna()
        if len(rev) < 3:
            r["rev_cagr_status"] = "short_history"  # <2 個年度區間 → 上市歷史不足
            return r
        rev = rev.sort_index()  # 由舊到新
        oldest, newest = float(rev.iloc[0]), float(rev.iloc[-1])
        n_int = len(rev) - 1  # 年度區間數（4 欄=3、3 欄=2）
        if oldest <= 0 or newest <= 0:
            r["rev_cagr_status"] = "short_history"  # 基期 ≤0 無法算 CAGR
            return r
        r["rev_cagr"] = (newest / oldest) ** (1.0 / n_int) - 1.0
        r["rev_cagr_years"] = n_int
        r["rev_cagr_status"] = "ok"
        return r

    print(f"[build_tenbagger] income_stmt {len(survivors)} 檔：先冷卻 10s"
          f"（避開 info 掃描後的限流窗），低併發抓取")
    time.sleep(10)
    done = 0
    with ThreadPoolExecutor(max_workers=max(2, WORKERS // 2)) as ex:
        for _ in ex.map(work, survivors):
            done += 1
            if done % 50 == 0:
                print(f"[build_tenbagger] income_stmt {done}/{len(survivors)}")

    # recovery：no_data（疑似被限流）sequential 補 2 輪——完整性優先於速度
    for rnd in (1, 2):
        retry = [r for r in survivors if r.get("rev_cagr_status") == "no_data"]
        if not retry:
            break
        print(f"[build_tenbagger] income_stmt recovery 第 {rnd} 輪："
              f"{len(retry)} 檔 no_data，冷卻 15s 後逐檔重試（間隔 1.5s）")
        time.sleep(15)
        for r in retry:
            work(r)
            time.sleep(1.5)

    got = sum(1 for r in survivors if r.get("rev_cagr") is not None)
    two_y = sum(1 for r in survivors if r.get("rev_cagr_years") == 2)
    short = sum(1 for r in survivors if r.get("rev_cagr_status") == "short_history")
    nodata = sum(1 for r in survivors if r.get("rev_cagr_status") == "no_data")
    # 成功率＝有拿到年報資料者（含史料不足——那也是成功的 fetch）
    FETCH_HEALTH["growth_success_frac"] = (len(survivors) - nodata) / len(survivors)
    print(f"[build_tenbagger] 營收 CAGR（annual income_stmt）：{got}/{len(survivors)} "
          f"檔算得（2Y 年化 {two_y}・上市歷史不足 {short}・抓取失敗 {nodata}・"
          f"fetch 成功率 {FETCH_HEALTH['growth_success_frac']:.1%}）")


def attach_dilution(survivors):
    """Phase 3（v0.1）：稀釋主源＝annual balance_sheet 'Ordinary Shares Number'
    （as-reported 年度股數，對 IPO 期雜訊穩定——治 CAVA −20.5%/y 假負稀釋）；
    拿不到 ≥2 個年度點才 fallback 到 get_shares_full split-adjusted 路徑。
    逐檔記 dilution_source。
    """
    if not survivors:
        return
    start_dt = datetime.now(timezone.utc) - timedelta(days=365 * 3 + 5)

    def work(r):
        r["share_cagr"], r["share_cagr_note"], r["dilution_source"] = None, None, None
        try:
            tk = yf.Ticker(r["ticker"])
        except Exception:
            return r
        # ── primary：balance_sheet 年度股數 ──
        try:
            bs = tk.balance_sheet
            if bs is not None and not bs.empty and "Ordinary Shares Number" in bs.index:
                sh = bs.loc["Ordinary Shares Number"].dropna().sort_index()
                if len(sh) >= 2:
                    first_d, last_d = sh.index[0], sh.index[-1]
                    first_v, last_v = float(sh.iloc[0]), float(sh.iloc[-1])
                    years = (last_d - first_d).days / 365.25
                    if first_v > 0 and last_v > 0 and years > 0.5:
                        r["share_cagr"] = (last_v / first_v) ** (1.0 / years) - 1.0
                        r["share_cagr_note"] = f"{years:.1f}y・年報股數"
                        r["dilution_source"] = "balance_sheet"
                        return r
        except Exception:
            pass
        # ── fallback：get_shares_full（split-adjusted，強制除分割因子）──
        try:
            cagr, note = share_cagr_split_adjusted(tk, start_dt)
        except Exception:
            cagr, note = None, "get_shares_full 例外"
        r["share_cagr"], r["share_cagr_note"] = cagr, note
        if cagr is not None:
            r["dilution_source"] = "shares_full"
        return r

    with ThreadPoolExecutor(max_workers=min(4, WORKERS)) as ex:
        list(ex.map(work, survivors))
    got = sum(1 for r in survivors if r.get("share_cagr") is not None)
    n_bs = sum(1 for r in survivors if r.get("dilution_source") == "balance_sheet")
    n_sf = sum(1 for r in survivors if r.get("dilution_source") == "shares_full")
    print(f"[build_tenbagger] 稀釋：{got}/{len(survivors)} 檔取得"
          f"（balance_sheet {n_bs}・shares_full fallback {n_sf}）")


# ---------------------------------------------------------------------------
# Rank key v0.2：最近 4 季營收 yoy 中位數（治 v0.1「3Y CAGR≈最近一次起漲點」
# 的基期效應；見上 docstring RANK KEY v0.2 段）。
# ---------------------------------------------------------------------------
def _yoy_pairs_from_quarterly_revenue(rev):
    """rev：pandas Series，index=季末 Timestamp（升冪、已去 NaN），value=營收。

    對「最近 4 季」逐季找「約一年前」的同季營收配對算 yoy（350–400 天窗，取離
    365 天最近者）；找不到配對的季度跳過——yfinance quarterly_income_stmt 常
    只回 4-5 欄，未必湊得滿 8 季，故本函式盡力配對而非硬性要求 8 欄。
    回傳 [(asof_date, yoy), ...]，可能為空 list。
    """
    dates = list(rev.index)
    n = len(dates)
    if n < 2:
        return []
    recent = dates[-4:] if n >= 4 else dates[:]
    pairs = []
    for d in recent:
        cur_val = float(rev.loc[d])
        lo, hi = d - timedelta(days=400), d - timedelta(days=330)
        cands = [dd for dd in dates if dd < d and lo <= dd <= hi]
        if not cands:
            continue
        match = min(cands, key=lambda dd: abs((d - dd).days - 365))
        prev_val = float(rev.loc[match])
        if prev_val == 0:
            continue
        pairs.append((d, cur_val / prev_val - 1.0))
    return pairs


def rev_yoy_4q_median_from_series(rev):
    """回傳 (median_yoy 或 None, 可配對的季數 n)。找不到任何可配對季度 → (None, 0)。"""
    pairs = _yoy_pairs_from_quarterly_revenue(rev)
    if not pairs:
        return None, 0
    yoys = [p[1] for p in pairs]
    return float(np.median(yoys)), len(yoys)


def attach_quarterly_yoy_median(passers):
    """只對已過完整 gate-set 的 survivors（passers，非全 universe）抓
    tk.quarterly_income_stmt 算 rank key。同 income_stmt fetch 的 fail-safe
    文化：per-ticker try/except，缺 → rev_yoy_4q_median=None（排序墊底，不 raise）。
    """
    if not passers:
        return
    for r in passers:
        r["rev_yoy_4q_median"], r["rev_yoy_4q_n"] = None, 0
        try:
            q = yf.Ticker(r["ticker"]).quarterly_income_stmt
            if q is None or q.empty or "Total Revenue" not in q.index:
                continue
            rev = q.loc["Total Revenue"].dropna()
            if len(rev) < 2:
                continue
            rev.index = pd.to_datetime(rev.index)
            if getattr(rev.index, "tz", None) is not None:
                rev.index = rev.index.tz_localize(None)
            rev = rev.sort_index()
            med, n = rev_yoy_4q_median_from_series(rev)
            r["rev_yoy_4q_median"], r["rev_yoy_4q_n"] = med, n
        except Exception:
            continue  # 缺 → None，排序墊底，不 raise（fail-safe 文化）
    got = sum(1 for r in passers if r.get("rev_yoy_4q_median") is not None)
    print(f"[build_tenbagger] 排序鍵（近4季yoy中位數）：{got}/{len(passers)} 檔取得")


def _rank_key(r):
    """None 墊底；有值者依 yoy 中位數由高到低（Python 排序：先比 tuple[0]，
    False(0) < True(1)，故 None 一律排在有值者之後）。"""
    v = r.get("rev_yoy_4q_median")
    return (v is None, -(v if v is not None else 0.0))


# ---------------------------------------------------------------------------
# 十倍軌 v0.2 手填顯示欄（single_product_pct / patent_expiry_year /
# tam_cap_note）：讀 picks.json 可選鍵 tenbagger_notes{}，本檔只讀不寫，
# 純顯示不影響 gate 通過/淘汰（見上 docstring）。
# ---------------------------------------------------------------------------
SHORT_RUNWAY_SINGLE_PRODUCT_PCT = 70   # 單一產品營收占比 ≥ 此值 → 短坡警示
SHORT_RUNWAY_PATENT_YEARS_OUT = 5      # 專利/獨占到期年 ≤ 今年 + 此值 → 短坡警示


def load_tenbagger_notes():
    """讀 docs/picks/picks.json 的可選鍵 tenbagger_notes{TICKER: {...}}（只讀不寫）。
    缺檔／缺鍵／格式不符 → 回傳空 dict，不 raise。"""
    try:
        with open(PICKS, encoding="utf-8") as f:
            pj = json.load(f)
        tn = pj.get("tenbagger_notes")
        if isinstance(tn, dict):
            return tn
    except Exception as e:
        warn(f"picks.json tenbagger_notes 讀取失敗（{type(e).__name__}）——手填欄留空")
    return {}


def compute_runway_status(note, current_year):
    """note：tenbagger_notes[TICKER]（dict 或 None/缺）。

    回傳 (single_product_pct, patent_expiry_year, tam_cap_note, runway_status)。
    三欄皆缺 → ('坡長未知')；觸發短坡條件（單一產品占比 ≥70 或專利到期 ≤ 今年+5）
    → '短坡警示'；否則（至少一欄有填且未觸發）→ '已填'。純顯示，不影響 gate。
    """
    sp = pey = tam = None
    if isinstance(note, dict):
        sp = note.get("single_product_pct")
        pey = note.get("patent_expiry_year")
        tam = note.get("tam_cap_note")
    if sp is None and pey is None and tam is None:
        return None, None, None, "坡長未知"
    short_flag = (
        (isinstance(sp, (int, float)) and not isinstance(sp, bool) and sp >= SHORT_RUNWAY_SINGLE_PRODUCT_PCT)
        or (isinstance(pey, (int, float)) and not isinstance(pey, bool)
            and pey <= current_year + SHORT_RUNWAY_PATENT_YEARS_OUT)
    )
    return sp, pey, tam, ("短坡警示" if short_flag else "已填")


# ---------------------------------------------------------------------------
# Gate-set v0.1（結構六條件機械化）
# ---------------------------------------------------------------------------
def gate_cap(r):
    mc = r.get("marketCap")
    return mc is not None and CAP_LO <= mc < CAP_HI


def gate_growth_fetch(r):
    # 年報抓取失敗（全 retry 後仍 no_data）→ 淘汰，但在 funnel 獨立一行可見——
    # 「抓取失敗」與「史料不足」是兩回事，失敗永遠不沉默
    return r.get("rev_cagr_status") != "no_data"


def gate_history(r):
    # 上市歷史不足（年報 <3 欄＝不足 2 個年度區間，或基期 ≤0）→ 淘汰
    return r.get("rev_cagr_status") == "ok"


def gate_rev_cagr(r):
    # 主閘：3 年營收 CAGR ≥ 20%
    c = r.get("rev_cagr")
    return c is not None and c >= MIN_REV_CAGR


def gate_rev_confirm(r):
    # 確認：最近季 yoy ≥ 15%（仍在成長，非已見頂）；缺 → 無從確認，淘汰
    g = r.get("revenueGrowth")
    return g is not None and g >= MIN_REV_YOY


def gate_margin(r):
    m = r.get("grossMargins")
    return m is not None and m >= MIN_GROSS_MARGIN


def gate_insider(r):
    # 缺 → 放行（keep），只在「有值且 < 5%」時殺
    i = r.get("heldPercentInsiders")
    return i is None or i >= MIN_INSIDER


def gate_dilution(r):
    # 缺 → 淘汰（稀釋是最大隱形稅，資料缺就保守）
    c = r.get("share_cagr")
    return c is not None and c <= MAX_SHARE_CAGR


def gate_selffund(r):
    fcf = r.get("freeCashflow")
    if fcf is None:
        return False  # 無法評估自籌資力 → 淘汰
    if fcf > 0:
        return True
    cash = r.get("totalCash")
    return cash is not None and cash >= SELFFUND_CASH_MULT * abs(fcf)


def gate_evs(r):
    v = r.get("enterpriseToRevenue")
    return v is not None and 0 < v <= MAX_EV_S


# 三段式 fetch/gate（v0.1）：
#   stage 1（.info 便宜判定）：cap / margin / insider → 存活 ~200-400 檔
#   → attach_growth（income_stmt 只對存活者抓）→ stage 2：CAGR 主閘 + 季 yoy 確認
#   → attach_dilution（balance_sheet/get_shares_full 只對存活者抓）→ stage 3
GATES_STAGE1 = [
    ("市值 $10–200 億", gate_cap),
    ("毛利率 ≥35%", gate_margin),
    ("內部人 ≥5%（缺→放行）", gate_insider),
]
GATES_STAGE2 = [
    ("年報抓取失敗（fetch 失敗可見化）", gate_growth_fetch),
    ("上市歷史不足（<3 欄年報）", gate_history),
    ("營收 3Y CAGR ≥20%", gate_rev_cagr),
    ("最近季 yoy ≥15%（確認）", gate_rev_confirm),
]
GATES_STAGE3 = [
    ("稀釋 CAGR ≤3%（缺→淘汰）", gate_dilution),
    ("自籌資力（FCF>0 或 現金≥2×|FCF|）", gate_selffund),
    ("EV/S 0–15", gate_evs),
]


def run_funnel(recs, growth_hook, dilution_hook):
    """依序過 gate，回傳 (passers, funnel OrderedDict)。

    growth_hook(survivors)：stage-1（cap/margin/insider）之後呼叫，對存活者補
    rev_cagr（income_stmt 是額外 call，不對整個 universe 抓）。
    dilution_hook(survivors)：stage-2（成長雙閘）之後呼叫，補 share_cagr。
    """
    funnel = OrderedDict()
    funnel["已擷取"] = len(recs)
    alive = recs
    for name, fn in GATES_STAGE1:
        alive = [r for r in alive if fn(r)]
        funnel[name] = len(alive)
    growth_hook(alive)
    for name, fn in GATES_STAGE2:
        alive = [r for r in alive if fn(r)]
        funnel[name] = len(alive)
    dilution_hook(alive)
    for name, fn in GATES_STAGE3:
        alive = [r for r in alive if fn(r)]
        funnel[name] = len(alive)
    return alive, funnel


# ---------------------------------------------------------------------------
# Price context（passers only；display-only，非 gate）
# ---------------------------------------------------------------------------
def attach_prices(passers):
    tickers = [p["ticker"] for p in passers]
    if not tickers:
        return
    try:
        px = yf.download(tickers, period="1y", interval="1d", auto_adjust=True,
                         group_by="ticker", progress=False, threads=True)
    except Exception as e:
        warn(f"價格 batch 下載失敗（{type(e).__name__}）——位置欄以 n/a 呈現")
        return
    single = len(tickers) == 1
    for p in passers:
        t = p["ticker"]
        try:
            c = (px["Close"] if single else px[t]["Close"]).dropna()
        except Exception:
            continue
        if len(c) < 20:
            continue
        last = float(c.iloc[-1])
        first = float(c.iloc[0])
        p["ret_12m_pct"] = round((last / first - 1.0) * 100, 1) if first > 0 else None
        win = min(200, len(c))
        ma = float(c.rolling(win).mean().iloc[-1])          # 年線代理（1y 資料上取 ≤200D MA）
        p["above_w52"] = bool(last > ma)


# ---------------------------------------------------------------------------
# 四件事 + per-name record
# ---------------------------------------------------------------------------
def make_record(r, note=None, current_year=None):
    g = r.get("revenueGrowth")
    m = r.get("grossMargins")
    i = r.get("heldPercentInsiders")
    ev = r.get("enterpriseToRevenue")
    c = r.get("share_cagr")
    mc = r.get("marketCap")

    gp = g * 100 if g is not None else None
    mp = m * 100 if m is not None else None
    ip = i * 100 if i is not None else None
    cp = c * 100 if c is not None else None

    cagr = r.get("rev_cagr")
    cagr_p = cagr * 100 if cagr is not None else None
    cagr_years = r.get("rev_cagr_years")

    med = r.get("rev_yoy_4q_median")
    med_p = med * 100 if med is not None else None
    med_n = r.get("rev_yoy_4q_n") or 0

    itxt = f"{ip:.0f}%" if ip is not None else "n/a"
    # v0.1：why 的營收數字改用持續性口徑（3Y CAGR），非單季尖峰；2Y 年化如實標示
    if cagr_p is not None:
        gtxt = f"CAGR {cagr_p:+.0f}%" + ("（2Y 年化）" if cagr_years == 2 else "")
    else:
        gtxt = f"{gp:+.0f}%"
    # v0.2：排序鍵已改「近4季yoy中位數」，why 開頭改帶這個數字，CAGR 降為併陳
    medtxt = f"近4季yoy中位數 {med_p:+.0f}%（n={med_n}）" if med_p is not None else "近4季yoy中位數 n/a"
    why = (f"{medtxt}；3Y {gtxt}×毛利 {mp:.0f}%×內部人 {itxt}"
           "——雙渦輪體質（盈餘成長×重評）")
    multiple = f"10x 目標／5-10 年；起始 EV/S {ev:.1f}"

    cy = current_year if current_year is not None else datetime.now(timezone.utc).year
    sp, pey, tam, runway_status = compute_runway_status(note, cy)

    ret = r.get("ret_12m_pct")
    above = r.get("above_w52")
    rtxt = f"12M {ret:+.0f}%" if ret is not None else "12M n/a"
    line = "站上" if above is True else ("跌破" if above is False else "—")
    position = f"{rtxt}；{line}年線（參考用，本軌不擇時）"

    exit_txt = ("營收成長連四季 <15%、稀釋失控（>3%/年）或 thesis 結構斷裂；"
                "−50% 回撤不是賣出理由")

    return {
        "ticker": r["ticker"],
        "name": r.get("name") or r["ticker"],
        "sector": r.get("sector") or "",
        "why": why,
        "multiple": multiple,
        "position": position,
        "exit": exit_txt,
        # raw metric values（給頁面 compact gate 欄用）
        "growth_pct": round(gp, 1) if gp is not None else None,
        "rev_cagr_3y": round(cagr_p, 1) if cagr_p is not None else None,
        "rev_cagr_years": cagr_years,
        # v0.2 排序鍵：最近 4 季營收 yoy 中位數（rev_cagr_3y 仍保留為 gate + 顯示欄）
        "rev_yoy_4q_median_pct": round(med_p, 1) if med_p is not None else None,
        "rev_yoy_4q_n": med_n,
        "margin_pct": round(mp, 1) if mp is not None else None,
        "insiders_pct": round(ip, 1) if ip is not None else None,
        "dilution_cagr_pct": round(cp, 1) if cp is not None else None,
        "dilution_source": r.get("dilution_source"),
        "ev_s": round(ev, 1) if ev is not None else None,
        "cap_B": round(mc / 1e9, 2) if mc is not None else None,
        "ret_12m_pct": ret,
        "above_w52": above,
        # v0.2 手填顯示欄（picks.json tenbagger_notes；缺 → null + 坡長未知）
        "single_product_pct": sp,
        "patent_expiry_year": pey,
        "tam_cap_note": tam,
        "runway_status": runway_status,
    }


# ---------------------------------------------------------------------------
# Cadence guard
# ---------------------------------------------------------------------------
def check_cadence(force):
    if force or not os.path.exists(OUT):
        return False
    try:
        with open(OUT, encoding="utf-8") as f:
            prev = json.load(f)
        ra = prev.get("refreshed_at")
        then = datetime.fromisoformat(ra)
        if then.tzinfo is None:
            then = then.replace(tzinfo=timezone.utc)
        age = (datetime.now(timezone.utc) - then).days
        if age < CADENCE_DAYS:
            print(f"[build_tenbagger] cadence guard：既有檔 refreshed_at 距今 {age} 天 "
                  f"(< {CADENCE_DAYS})，跳過（--force 可強制）。")
            return True
    except Exception as e:
        warn(f"cadence guard 讀既有檔失敗（{type(e).__name__}）——照常重算")
    return False


# ---------------------------------------------------------------------------
def main():
    force = "--force" in sys.argv[1:]

    if check_cadence(force):
        return 0

    universe = build_universe()
    if len(universe) < 200:
        warn(f"universe 僅 {len(universe)} 檔（Wikipedia 抓取異常？）——不覆蓋既有檔，退出。")
        return 0

    recs = fetch_universe(universe)
    coverage = len(recs) / len(universe) if universe else 0.0

    # fail-safe：coverage 不足 → 保留既有檔
    if coverage < COVERAGE_FLOOR:
        warn(f"coverage {coverage:.1%} < {COVERAGE_FLOOR:.0%}——"
             f"保留既有 tenbagger.json 不覆蓋，退出。")
        return 0

    passers, funnel = run_funnel(recs, attach_growth, attach_dilution)

    # fail-safe（2026-07-05 事故加設）：income_stmt 成功率 < 70% ＝ funnel 崩塌
    # 是限流不是真篩選 → 不寫檔，保留上一份好資料。空榜若出自乾淨的 fetch
    # （成功率 ≥ 70%）則是誠實結果（寧缺勿濫），照寫。
    gsf = FETCH_HEALTH.get("growth_success_frac", 1.0)
    if gsf < GROWTH_FETCH_FLOOR:
        warn(f"income_stmt fetch 成功率 {gsf:.1%} < {GROWTH_FETCH_FLOOR:.0%}——"
             f"資料層失敗（限流），不寫 tenbagger.json，保留上一份好資料，退出。")
        return 0

    # 診斷（不調參，僅回報給持有人判斷確認閘鬆緊）：CAGR 過但季 yoy 確認沒過
    cagr_pass_yoy_fail = [
        r for r in recs
        if r.get("rev_cagr") is not None and r["rev_cagr"] >= MIN_REV_CAGR
        and not gate_rev_confirm(r)
    ]
    if cagr_pass_yoy_fail:
        print(f"[build_tenbagger] 診斷：3Y CAGR ≥20% 但最近季 yoy <15% 被確認閘擋下 "
              f"{len(cagr_pass_yoy_fail)} 檔：")
        for r in cagr_pass_yoy_fail:
            g = r.get("revenueGrowth")
            gtxt = f"{g*100:+.1f}%" if g is not None else "n/a"
            print(f"    {r['ticker']:<7} CAGR {r['rev_cagr']*100:+.1f}%/y"
                  f"（{r.get('rev_cagr_years')}Y）  季yoy {gtxt}")

    # veto（讀 picks.json，只讀不寫）
    veto = set()
    try:
        with open(PICKS, encoding="utf-8") as f:
            pj = json.load(f)
        if isinstance(pj.get("veto"), list):
            veto = {t for t in pj["veto"] if isinstance(t, str)}
    except Exception as e:
        warn(f"picks.json veto 讀取失敗（{type(e).__name__}）——不套 veto")
    vetoed = [p["ticker"] for p in passers if p["ticker"] in veto]
    if vetoed:
        print(f"[build_tenbagger] veto 生效（持有人 veto，排除）：{sorted(vetoed)}")
    passers = [p for p in passers if p["ticker"] not in veto]

    # v0.2 排序鍵：只對已過完整 gate-set 的 survivors 抓 quarterly_income_stmt
    # 算「最近 4 季營收 yoy 中位數」（treat TGTX 型基期效應；見上 docstring）
    attach_quarterly_yoy_median(passers)
    passers.sort(key=_rank_key)  # None 墊底；有值者由高到低

    official_recs = passers[:SEAT_CAP_10X]
    candidate_recs = passers[SEAT_CAP_10X:SEAT_CAP_10X + CAND_CAP]

    # price context 只對進榜/候選（≤25 檔）
    attach_prices(official_recs + candidate_recs)

    # v0.2 手填顯示欄（single_product_pct/patent_expiry_year/tam_cap_note）
    tb_notes = load_tenbagger_notes()
    now = datetime.now(timezone.utc)
    current_year = now.year
    official = [make_record(r, note=tb_notes.get(r["ticker"]), current_year=current_year)
                for r in official_recs]
    candidates = [make_record(r, note=tb_notes.get(r["ticker"]), current_year=current_year)
                  for r in candidate_recs]

    payload = {
        "as_of": datetime.now(TW8).strftime("%Y-%m-%d"),
        "refreshed_at": now.isoformat(),
        "universe_size": len(universe),
        "coverage": {
            "fetched": len(recs),
            "pct": round(coverage * 100, 1),
        },
        "gate_funnel": funnel,
        "gate_version": GATE_VERSION,
        "rank_key_version": RANK_KEY_VERSION,
        "seat_cap": SEAT_CAP_10X,
        "note": ("十倍・結構長坡＝發現層：S&P 400+600 universe 過結構六條件 gate-set v0.1"
                 "（市值 $10–200 億 × 營收 3Y CAGR≥20% ∩ 最近季 yoy≥15% × 毛利≥35% × "
                 "內部人≥5% × 稀釋≤3%/年（年報股數為主源）× 自籌資力 × EV/S≤15）；"
                 "排序鍵 v0.2＝最近 4 季營收 yoy 中位數（治基期效應，3Y CAGR 仍為"
                 "gate＋顯示欄）；SEAT_CAP=5 進正式榜、next 15 候選；持有人 veto 通用。"
                 "single_product_pct／patent_expiry_year／tam_cap_note 三欄由持有人"
                 "手填（picks.json tenbagger_notes，本檔只讀不寫），純顯示不影響 gate。"
                 "月頻刷新。未經 DD 深度驗證，風險高於前兩組。"),
        "official": official,
        "candidates": candidates,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # ── console summary ──
    print(f"\n[build_tenbagger] wrote {OUT}")
    print(f"[build_tenbagger] universe={len(universe)}  coverage={coverage:.1%} "
          f"({len(recs)} 檔)")
    print(f"[build_tenbagger] gate funnel（結構六條件 {GATE_VERSION}）：")
    prev = None
    for name, n in funnel.items():
        drop = "" if prev is None else f"  (−{prev - n})"
        print(f"    {name:<28} {n:>5}{drop}")
        prev = n
    print(f"[build_tenbagger] passers={len(passers)}  正式榜={len(official)} "
          f"候選={len(candidates)}")

    def _fmt(p):
        yr = p.get("rev_cagr_years")
        cagr_txt = f"CAGR{p['rev_cagr_3y']}%" + (f"({yr}Y)" if yr else "")
        med = p.get("rev_yoy_4q_median_pct")
        med_txt = f"近4Qyoy中位{med}%(n={p.get('rev_yoy_4q_n')})" if med is not None else "近4Qyoy中位n/a"
        return (f"{p['ticker']:<7} {med_txt:<24} {cagr_txt:<16} 季yoy{p['growth_pct']}% "
                f"毛利{p['margin_pct']}% 內部人{p['insiders_pct']}% "
                f"稀釋{p['dilution_cagr_pct']}%/y[{p['dilution_source']}] "
                f"EV/S {p['ev_s']} 市值${p['cap_B']}B  12M {p['ret_12m_pct']}% "
                f"{'站上' if p['above_w52'] else '跌破' if p['above_w52'] is False else '?'}年線 "
                f"坡道：{p['runway_status']}")

    print(f"[build_tenbagger] 正式榜 {len(official)} 檔（rank by 近4季yoy中位數，v0.2）：")
    for i, p in enumerate(official, 1):
        print(f"    #{i:>2} {_fmt(p)}")
    print(f"[build_tenbagger] 候選 {len(candidates)} 檔：")
    for p in candidates:
        print(f"        {_fmt(p)}")
    return 0


# ---------------------------------------------------------------------------
# 離線自測（stub 資料，不打 yfinance／網路）：
#   python3.12 scripts/build_tenbagger.py --selftest
# ---------------------------------------------------------------------------
def _selftest():
    ok_msg = []

    # ── rev_yoy_4q_median_from_series：4 季齊全，yoy 各 30/20/10/5% → 中位數 15% ──
    dates = pd.to_datetime([
        "2023-03-31", "2023-06-30", "2023-09-30", "2023-12-31",
        "2024-03-31", "2024-06-30", "2024-09-30", "2024-12-31",
    ])
    vals = [100, 100, 100, 100, 130, 120, 110, 105]
    rev = pd.Series(vals, index=dates).sort_index()
    med, n = rev_yoy_4q_median_from_series(rev)
    assert n == 4, f"預期配對 4 季，實得 {n}"
    assert med is not None and abs(med - 0.15) < 1e-9, f"預期中位數 0.15，實得 {med}"
    ok_msg.append(f"rev_yoy_4q_median_from_series（8 季齊全）：median={med:.3f} n={n}")

    # ── 資料只有 1 季（<2 季）→ 無法配對 → None ──
    short_rev = pd.Series([100.0], index=pd.to_datetime(["2024-01-01"]))
    med2, n2 = rev_yoy_4q_median_from_series(short_rev)
    assert med2 is None and n2 == 0, f"預期 (None, 0)，實得 ({med2}, {n2})"
    ok_msg.append("rev_yoy_4q_median_from_series（資料不足 <2 季）：(None, 0)")

    # ── 只有 5 季（僅 1 組可配對 yoy）→ median = 該 1 個值 ──
    dates5 = pd.to_datetime([
        "2023-12-31", "2024-03-31", "2024-06-30", "2024-09-30", "2024-12-31",
    ])
    vals5 = [100, 130, 120, 110, 105]
    rev5 = pd.Series(vals5, index=dates5).sort_index()
    med5, n5 = rev_yoy_4q_median_from_series(rev5)
    assert n5 == 1 and med5 is not None and abs(med5 - 0.05) < 1e-9, f"預期 (0.05, 1)，實得 ({med5}, {n5})"
    ok_msg.append(f"rev_yoy_4q_median_from_series（5 季僅 1 組可配對）：median={med5:.3f} n={n5}")

    # ── 排序鍵 _rank_key：有值者高到低、None 一律墊底（穩定排序）──
    stub = [
        {"ticker": "AAA", "rev_yoy_4q_median": 0.30},
        {"ticker": "BBB", "rev_yoy_4q_median": None},
        {"ticker": "CCC", "rev_yoy_4q_median": 0.10},
        {"ticker": "DDD", "rev_yoy_4q_median": 0.50},
        {"ticker": "EEE", "rev_yoy_4q_median": None},
    ]
    stub.sort(key=_rank_key)
    order = [r["ticker"] for r in stub]
    assert order == ["DDD", "AAA", "CCC", "BBB", "EEE"], f"排序錯誤：{order}"
    ok_msg.append(f"_rank_key 排序（None 墊底）：{order}")

    # ── compute_runway_status：四情境（缺填／單一產品觸發／專利觸發／已填不觸發）──
    cy = 2026
    r1 = compute_runway_status(None, cy)
    assert r1 == (None, None, None, "坡長未知"), f"缺填案例錯誤：{r1}"
    r2 = compute_runway_status(
        {"single_product_pct": 95, "patent_expiry_year": None, "tam_cap_note": None}, cy)
    assert r2[3] == "短坡警示", f"單一產品觸發案例錯誤：{r2}"
    r3 = compute_runway_status(
        {"single_product_pct": None, "patent_expiry_year": 2029, "tam_cap_note": None}, cy)
    assert r3[3] == "短坡警示", f"專利到期觸發案例錯誤（2029 ≤ 2026+5）：{r3}"
    r4 = compute_runway_status(
        {"single_product_pct": 20, "patent_expiry_year": 2040, "tam_cap_note": "1000店天花板"}, cy)
    assert r4 == (20, 2040, "1000店天花板", "已填"), f"已填不觸發案例錯誤：{r4}"
    r5 = compute_runway_status(
        {"single_product_pct": None, "patent_expiry_year": None, "tam_cap_note": None}, cy)
    assert r5[3] == "坡長未知", f"全 None dict 案例錯誤：{r5}"
    r6 = compute_runway_status(
        {"single_product_pct": None, "patent_expiry_year": 2032, "tam_cap_note": None}, cy)
    assert r6[3] == "已填", f"專利到期未觸發案例錯誤（2032 > 2026+5）：{r6}"
    ok_msg.append("compute_runway_status 六情境（缺填/單一產品觸發/專利觸發/已填/全None/未觸發）：OK")

    print("[selftest] build_tenbagger.py 自測全數通過：")
    for m in ok_msg:
        print(f"    - {m}")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    sys.exit(main())
