#!/usr/bin/env python3
"""GRP 選股函數 — 高成長（Growth）× EPS 上修（Revision）× 股價位置（Price）.

持有人 2026-07-04 拍板：引擎的席位／挑戰者排序**不依賴 5Y EV/IRR**（DD 情境推導、
更新慢、模型味重），改用市場每月給的三個活數據閘：

  G 高成長：FY1→FY3 EPS CAGR ≥ 15%（沿用五條件成長門檻；缺 FY3 用 eps2y fallback）
  R 上修  ：FY+1 單月修正 ≥ +2% 或 2Y CAGR 修正 ≥ +1pp；**單月下修 < -2% 一票否決**
  P 位置  ：站上 52 週線（趨勢在）且未過熱（日收 < 週線布林 +2σ 凍結值）
            位置標籤：breakout（距 52w 高 ≤5%＝突破帶）／pullback（回檔 8–25% 且趨勢在）
            ／in_trend（其餘趨勢內）

排序＝過全部閘者按 R（上修幅度）降冪、tiebreak G——上修動能是 1–3Y 最強訊號
（驗屍依據：SNDK/MU 型贏家全部先出現在修正欄）。
EV5y×確定性自本日降級為 DD 裁決內部資訊，不再參與排序。門檻 v1 鎖定，季檢憑記分板調。

v2（2026-09-02 持有人拍板「照推薦執行」；依據 notes/site-internal/root/
_picks_first_principles_review_20260902.md Part A／D）——**擁有層與時機層分離**：
  擁有層（排序鍵，月尺度）：own_score ＝ min(G，30) ＋ FY1 盈餘殖利率% ＋ 持續期加分
      （ROIC ≥30 → +2）－ 倍數風險（PEG >2 → −5）。回答「值不值得擁有、排第幾」。
  品質閘（資格，擁有層）：ROIC ≥15 ∧ FCF margin ≥10；capex 週期豁免＝ROIC ≥25 ∧ FCF ≥0
      （FCF margin 在資本週期上半場量的是投資強度，用更高 ROIC 當代價換一條路）。
  時機層（燈號，週尺度）：P 位置閘照舊（席位仍要求站上 52 週線），R 上修降為燈號；
      R 一票否決由單月 −2% 放寬到 −10%（單月 −2% 是時機雜訊，讓核心席兩個月換三席）。
  排序不再用 R——站內 scoreboard by_shape：動能重估 n=237 中位 −6.3%／虧損率 66%，
  而 GRP 的 R×P 閘在定義上就是在挑這個形狀；擁有層排序讓席位回到「生意」尺度。
  遲滯（build_arena）：新席需連 2 次週跑過閘；現任席連 4 次不過才下席（硬 veto 除外）；
      DD 180 天內裁決＝觀望的現任席降權為連 2 次不過即下（B4② 2026-09-04）。
  規則登記：knowledge/rule_ledger.md（v2 三條；R −2% 否決同日提名候刪審查；B4② 降權版）。

v4（2026-09-17 持有人拍板「席位引擎 v4」；依據 10 週對照：核心 −3.8%／核心＋衛星 −8.4%
vs SPY +1.2%、首批 B&H +1.0%、10 週 23 檔坐過 10 席——換手率過高、單月尺度的週遲滯在
「保護」雜訊而非訊號）——五項改動：
  1. 成長閘：三年期 Koyfin CAGR 仍是硬性必備（單年 fallback 不算），門檻 15%，但
     durable_5y 為 True 者放寬到 10%（複利股基期已高，成長速度本來就該慢下來）。
  2. 上修否決：改看三個月（FY 加權 0.2/0.3/0.5）EPS 上修 eps_rev_3m_pct ≤ −5% 才否決，
     取代原本 FY+1 單月 ≤ −10%；後者只在前者缺值時當 fallback。
  3. 過熱不再是資格閘：12-1 個月動能 mom_12_1_pct > 150%（缺值 fallback 26 週漲幅
     > 80%）→ overheated=True，不否決資格，但排除出核心候選（只能衛星）。峰頂
     （roic_vs_5y_x ≥ 1.3）另立 peak 旗標，是純顯示註記（⚠ 頂點），**不**排除核心
     候選——實測回溯（NVDA／CLS 皆 peak 但穩居核心候選前 5）證明頂點是「賺得比五年
     均值快」的健康訊號，不是該離場的訊號；過熱（短線動能滿檔）才是該功成身退進
     衛星、讓時機燈接手判斷買點的訊號。兩者字面接近但語意不同，故意分開存放。
  4. 排序：own_score 改五個百分位（三月上修／12-1 月動能／成長封頂 30／品質／盈餘
     殖利率）在 ELIGIBLE 集合內互相比較後平均（需 ≥4/5），品質＝FCF/淨利與稀釋率
     百分位平均，但 incremental_roic_pct ≥15 者（投資有回報）免計 FCF/淨利、品質只看
     稀釋率。舊 own_score（v2 公式）保留一輪對照，存 own_v2。
  5. 時機燈 timing_lamp()：把位置／RS／200 日線／階段收斂成一個燈號＋倉位建議，
     不再是三個獨立欄位；核心 vs 衛星是「值不值得擁有」的月頻判斷，時機燈是「現在
     能不能買」的週頻判斷——CLS 是最佳示範：耐久＋不過熱→核心候選，但距高 −31%／
     RS 33／跌破 200 日線→🔴 等板機／零倉，兩層判斷刻意不互相污染。
  無產業/主題集中度上限（持有人拍板：席位本來就沒幾席，硬性 cap 只會逼著湊數）。
  月頻輪動（見 build_arena 檔頭）：每月第一次 --ledger 跑重新選一次，期間只有硬否決
  （迴避／拒絕/⛔／三月上修 ≤−5／市值不足／連兩週跌破 52 週線）能換人，空位由下一
  名遞補。規則登記：knowledge/rule_ledger.md「v4 席位引擎（2026-09-17）」。

v4.1（2026-09-17 持有人拍板，三項 DD-free 機械規則搬進引擎，皆非新創判準）：
  1. 融券高：short_interest_pct_float > 10% → high_short_interest=True，比照
     overheated 待遇——不進 own_score 排序、不是資格閘，只排除核心候選（衛星照樣能
     坐）。依據：高融券預測低報酬的學術證據集中在尾巴（>10-20% 流通股），大型優質
     股母體內 1-3% 的差異是雜訊。內部人買賣（insider_net_buy_3m／insider_signal）
     全程只是 build_arena 席位表的備註 badge，不是排序因子、不是資格閘。
  2. 基期效應（_base_effect_growth()）：Koyfin 三年 FY1→FY3 CAGR 若因 FY1→FY2 低
     基期跳增（>1.6x）而 FY2→FY3 成長 <20%，改用 FY2→FY3 成長率取代，同時用在
     成長閘（grp_score 的 g）與排序鍵（own_raw 的 g）——例：MRK／MU 兩檔原始三年
     CAGR 皆被 FY1→FY2 低基期跳增蓋掉真實的 FY2→FY3 穩態成長。
  3. 循環股守門（own_raw()／own_score_v4()）：毛利率四點跨距 >20pp 或資本支出佔
     營收 >15% → cyclical；cyclical 且 PEG（live_peg 優先，fallback peg）<0.3 →
     cycle_guard=True，成長分位／盈餘殖利率分位封頂 50 再平均——循環股在景氣高點
     常同時出現「爆量成長」與「PEG 低到可疑」，不封頂會讓排序誤判成複利成長。
  規則登記：knowledge/rule_ledger.md「v4.1 融券比 >10% 只能衛星」「v4.1 基期效應＋
  循環股守門」兩列（皆 2026-09-17）。設計稿：notes/site-internal/root/
  _seat_engine_v4_20260917.md「v4.1 追加」段。

財報錨定上修（2026-09-17 持有人拍板）——三月上修否決的固定 ~90 天日曆窗在報告日不
對齊的母體上不公平：7 月初就發財報的名字，上修動能一個月後就因為日曆理由過期出窗，
而還沒發財報的名字反而卡在接近零。改法：own_raw()／grp_score() 的上修輸入改讀
build_dd_screener._compute_eps_rev_since_earnings() 算好的 eps_rev_since_earnings_pct
（同一台 FY 加權 0.2/0.3/0.5 FX 正規化機械，只是 baseline 改成「這檔自己最近一次財報
日之前最新的月度 snapshot」），缺值才退回 eps_rev_3m_pct（見 _revision_anchor()，
兩者間的抉擇邏輯集中在這一個函式，own_raw／grp_score 都呼叫它，不各自判斷一次）。
Row 新帶 rev_anchor（"earnings"|"calendar_3m"）／rev_baseline_date／
days_to_next_earnings 供 build_arena 席位表 tooltip 與「下次財報」欄使用。
eps_rev_3m_pct／EPS_REV_3M_VETO 否決線本身不動（見 rule_ledger「上修改為財報後
錨定」列）。
"""
from __future__ import annotations

import json
from pathlib import Path

G_MIN_CAGR = 15.0        # G 閘：FY1→FY3 EPS CAGR（非耐久）
G_MIN_CAGR_DURABLE = 10.0  # v4：durable_5y=True 者放寬門檻（複利股基期高、成長本該慢）
# 擁有層（v2）：品質閘與排序鍵常數
Q_ROIC_MIN = 15.0        # 品質閘：ROIC ≥15%
Q_FCF_MIN = 10.0         # 品質閘：FCF margin ≥10%
Q_ROIC_EXEMPT = 25.0     # capex 週期豁免：ROIC ≥25 時 FCF margin 只需 ≥0
OWN_G_CAP = 30.0         # 排序鍵成長封頂（防基期效應排第一）
OWN_DURABLE_ROIC = 30.0  # 持續期加分門檻（ROIC ≥30 → +2）
OWN_PEG_PENALTY = 2.0    # PEG >2 → −5
# 市值門檻（持有人 2026-07-04 拍板 ≥$200 億）：管「席位資格＋GRP 主榜」，雷達照掃全宇宙。
# 理由：不要小股票的 risk profile；發現層看得見 ≠ 有資格買。
MKTCAP_MIN = 20_000_000_000
_CAP_CACHE = Path(__file__).resolve().parent.parent.parent / "data" / "engine" / "mktcap.json"
# 持有人 2026-09-02 拍板：選股系統 v2 先只做美股（含 ADR），台股另建獨立系統——
# 母體／席位／爆發正式榜一律排除 .TW（其他海外掛牌不受此拍板影響，維持原狀）。
EXCLUDED_SUFFIXES = (".TW",)


def market_ok(ticker) -> bool:
    """False＝該 ticker 屬本輪排除範圍（見上 EXCLUDED_SUFFIXES 拍板）。"""
    t = str(ticker or "")
    return not t.endswith(EXCLUDED_SUFFIXES)


def load_caps() -> dict:
    try:
        return json.loads(_CAP_CACHE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def fetch_caps(tickers: list[str], caps: dict | None = None) -> dict:
    """補抓缺少的市值（yfinance fast_info），寫回 cache。失敗沿用舊值（fail-open 顯示、
    fail-closed 資格——無市值資料者不給席位資格，但標示「市值未知」而非靜默通過）。"""
    caps = dict(caps if caps is not None else load_caps())
    missing = [t for t in tickers if t not in caps]
    if missing:
        try:
            import yfinance as yf
            for t in missing:
                try:
                    v = yf.Ticker(t.replace(".", "-")).fast_info["marketCap"]
                    if v:
                        caps[t] = float(v)
                except Exception:
                    pass
        except ImportError:
            pass
        _CAP_CACHE.parent.mkdir(parents=True, exist_ok=True)
        _CAP_CACHE.write_text(json.dumps(caps, ensure_ascii=False, indent=1), encoding="utf-8")
    return caps


def cap_ok(cap) -> bool | None:
    """None＝市值未知（資格 fail-closed、顯示標註）；True/False＝門檻判定。"""
    if cap is None:
        return None
    return float(cap) >= MKTCAP_MIN
# R 閘語意＝「有上修」（正向即可，非拐點級門檻——+2%/+1pp 是循環軌找拐點用的，
# 對穩定複利股會全滅；上修「幅度」由排序層獎勵，資格層只問方向）
R_MIN_FY1 = 0.0          # R 閘：FY+1 單月修正 > 0
R_MIN_2Y_PP = 0.0        # R 閘：eps2y 修正 pp > 0（替代路徑）
R_VETO_FY1 = -10.0       # R 否決 fallback（v4）：僅在 eps_rev_3m_pct 缺值時用 FY+1 單月 ≤ 此值否決
EPS_REV_3M_VETO = -5.0   # v4 主否決：三月上修（FY 加權）≤ 此值 → 否決（見 build_dd_screener._compute_eps_rev_3m）
P_BREAKOUT_DIST = -5.0   # 距 52 週高 ≥ -5% ＝突破帶
P_PULLBACK = (-25.0, -8.0)   # 回檔帶（含趨勢完好）
# v4：過熱／頂點——不是資格閘，只決定核心候選資格（過熱）與顯示註記（頂點）。見檔頭 v4 段。
MOM_12_1_OVERHEAT = 150.0   # 12-1 個月動能（ma.mom_12_1_pct）> 此值 → overheated
R26_OVERHEAT_FALLBACK = 80.0  # mom_12_1_pct 缺值時 fallback：26 週漲幅（_r26，build_arena.weekly_structure）
PEAK_ROIC_X = 1.3          # roic_vs_5y_x ≥ 此值 → peak（純顯示註記，不影響核心候選資格）
# v4.1（2026-09-17，見 knowledge/rule_ledger.md「v4.1 融券比 >10% 只能衛星」列）：
# 融券比不是排序因子、不是資格閘——只比照 overheated 的待遇，排除核心候選資格
# （衛星照樣能坐）。依據：高融券預測低報酬的學術證據集中在尾巴（>10-20% 流通股），
# 大型優質股母體內 1-3% 的差異是雜訊，故不進 own_score 排序。
SI_CORE_EXCLUDE_PCT = 10.0   # short_interest_pct_float > 此值 → high_short_interest（只能衛星）
# v4.1（2026-09-17，見 rule_ledger「v4.1 基期效應＋循環股守門」列）：基期效應與
# 循環股守門的門檻常數，DD 技能既有機械規則搬進引擎，不新創判準。
BASE_EFFECT_STEP12_X = 1.6     # FY1→FY2 跳增倍數門檻（f2/f1）
BASE_EFFECT_STEP23_CAP = 0.20  # FY2→FY3 成長需 < 此值（20%）才判定為基期失真
CYCLE_GM_SWING_PP = 20.0       # 循環股守門：毛利率（LTM/FY-1/FY-2/FY-3）四點跨距門檻（pp）
CYCLE_CAPEX_PCT_REV = 15.0     # 循環股守門：資本支出佔營收門檻（%）
CYCLE_GUARD_PEG_MAX = 0.3      # 循環股守門：PEG 需 < 此值才觸發 guard（cyclical 且低到可疑）
CYCLE_GUARD_PCTL_CAP = 50.0    # guard 觸發時，own_score_v4 的 p_g／p_ey 百分位上限
# v4 時機燈 action 對照（build_arena 倉位欄）
LAMP_ACTION = {"green": "正常倉", "yellow": "半倉", "hot": "半倉", "red": "零倉・等板機", "out": "—"}


def _f(v):
    try:
        f = float(v)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


def _revision_anchor(s: dict) -> tuple:
    """財報錨定上修（2026-09-17 owner decision — see knowledge/rule_ledger.md
    「上修改為財報後錨定」row）: revision input shared by own_raw() (ranking)
    and grp_score() (veto). Primary source is eps_rev_since_earnings_pct
    (build_dd_screener._compute_eps_rev_since_earnings() — anchored on THIS
    ticker's own last earnings date, not a fixed ~90-day calendar window);
    falls back to eps_rev_3m_pct (the old calendar-anchored value) only when
    the earnings-anchored field is entirely absent from `s` (e.g. an older
    dd-screener rebuild predating this feature, or a hand-built test fixture
    that only sets eps_rev_3m_pct — the screener itself already folds the
    calendar-3m fallback into eps_rev_since_earnings_pct via eps_rev_anchor
    when a ticker has no qualifying earnings-anchor baseline, so this second
    fallback layer is purely a back-compat safety net).

    Returns (value, anchor, baseline_date):
      anchor — "earnings" | "calendar_3m" | None (None only when both fields
                are missing).
    """
    since = _f(s.get("eps_rev_since_earnings_pct"))
    if since is not None:
        return since, (s.get("eps_rev_anchor") or "earnings"), s.get("eps_rev_since_earnings_baseline_date")
    threem = _f(s.get("eps_rev_3m_pct"))
    if threem is not None:
        return threem, "calendar_3m", s.get("eps_rev_3m_baseline_date")
    return None, None, None


def _base_effect_growth(s: dict) -> tuple:
    """v4.1（2026-09-17，見 knowledge/rule_ledger.md「v4.1 基期效應＋循環股守門」列）
    基期效應（base effect）：Koyfin 三年 FY1→FY3 CAGR 是幾何平均，若 FY1→FY2 因低基期
    （例如轉虧為盈次年、或極小分母）跳增，會把整段三年 CAGR 拉得虛高，蓋掉 FY2→FY3
    才是穩態成長的事實（例：MRK 2.75→9.55→10.62，CAGR 幾何平均看似高速，但 FY2→FY3
    只有 +11%；MU 73.4→156.3→171.6 同理）。DD 技能既有機械規則搬進引擎，不新創判準。

    f1/f2/f3（eps_fy_curr/eps_fy_next/eps_fy3）三者皆為正值時，若 FY2/FY1 之比
    > BASE_EFFECT_STEP12_X 且 FY3/FY2−1 < BASE_EFFECT_STEP23_CAP，改用 FY2→FY3
    成長率取代 eps_fy1_fy3_cagr_pct（回傳 base_effect=True）；其餘情況原樣沿用三年
    CAGR（base_effect=False）。改用的仍是三年期 Koyfin 預估資料本身，只是換一種
    算法讀穩態成長，**不影響** g_three_year 判定（不是退回單年 fallback）。
    回傳 (g, base_effect, detail|None)；detail 供 UI tooltip 顯示兩段成長率。"""
    cagr = _f(s.get("eps_fy1_fy3_cagr_pct"))
    f1, f2, f3 = _f(s.get("eps_fy_curr")), _f(s.get("eps_fy_next")), _f(s.get("eps_fy3"))
    if f1 is not None and f2 is not None and f3 is not None and f1 > 0 and f2 > 0 and f3 > 0:
        step12_x = f2 / f1
        step23_pct = (f3 / f2 - 1.0) * 100.0
        if step12_x > BASE_EFFECT_STEP12_X and step23_pct < BASE_EFFECT_STEP23_CAP * 100.0:
            detail = {"fy1_fy2_pct": round((step12_x - 1.0) * 100.0, 1), "fy2_fy3_pct": round(step23_pct, 1)}
            return round(step23_pct, 2), True, detail
    return cagr, False, None


def own_raw(s: dict) -> dict:
    """v4 own_score 單檔原始輸入（pure）——見 own_score_v4() 做跨檔百分位排序。
    g 只認真三年期 Koyfin CAGR（eps_fy1_fy3_cagr_pct，封頂 30，v4.1 起先過
    _base_effect_growth() 基期效應校正），不像 grp_score 的 g 閘變數那樣 fallback
    到 eps2y——ELIGIBLE 集合本身已要求 g_three_year=True，這裡沒有 fallback 的
    必要（也不該讓單年基期效應混進排序）。

    v4.1 另算循環股守門（cyclical／cycle_guard，見檔頭同名段）：cyclical＝毛利率
    （LTM/FY-1/FY-2/FY-3，需 ≥3 點）跨距 >20pp 或資本支出佔營收 >15%；guard＝
    cyclical 且 PEG（live_peg 優先，fallback peg）<0.3——PEG 低到可疑通常是循環股
    在景氣高點被低估未來獲利，own_score_v4() 依 cycle_guard 把 p_g／p_ey 百分位
    封頂 50，cyclical 本身即使未觸發 guard 也照樣回傳，供純顯示用的「循環」備註。"""
    g_raw, base_effect, base_effect_detail = _base_effect_growth(s)
    g = min(g_raw, OWN_G_CAP) if g_raw is not None else None
    fpe = _f(s.get("live_fpe_est"))
    ey = (100.0 / fpe) if fpe and fpe > 0 else None
    if ey is None:
        px = _f((s.get("ma") or {}).get("price")); e1 = _f(s.get("eps_fy_next"))
        if px and e1 and px > 0:
            ey = e1 / px * 100.0
    fund = s.get("fund") or {}
    gms = [v for v in (_f(fund.get(k)) for k in
                        ("gm_ltm_pct", "gm_fy1_pct", "gm_fy2_pct", "gm_fy3_pct")) if v is not None]
    gm_swing = (max(gms) - min(gms)) if len(gms) >= 3 else None
    capex_pct_rev = _f(s.get("capex_pct_rev"))
    cyclical = bool((gm_swing is not None and gm_swing > CYCLE_GM_SWING_PP)
                     or (capex_pct_rev is not None and capex_pct_rev > CYCLE_CAPEX_PCT_REV))
    peg = _f(s.get("live_peg"))
    if peg is None:
        peg = _f(s.get("peg"))
    cycle_guard = bool(cyclical and peg is not None and peg < CYCLE_GUARD_PEG_MAX)
    cycle_guard_detail = ({"gm_swing_pp": round(gm_swing, 1) if gm_swing is not None else None,
                           "capex_pct_rev": capex_pct_rev, "peg": peg} if cyclical else None)
    rev_value, rev_anchor, rev_baseline_date = _revision_anchor(s)
    return {
        # 財報錨定上修（2026-09-17，見 _revision_anchor() docstring）：eps_rev_
        # since_earnings_pct 優先，eps_rev_3m_pct 為後備。rev_anchor/
        # rev_baseline_date 純顯示，供席位表 tooltip 標「基準快照日／錨定方式」。
        "rev": rev_value,
        "rev_anchor": rev_anchor,
        "rev_baseline_date": rev_baseline_date,
        "mom": _f((s.get("ma") or {}).get("mom_12_1_pct")),
        "g": round(g, 2) if g is not None else None,
        "ey": round(ey, 2) if ey is not None else None,
        "fcf_ni": _f(s.get("fcf_ni_ratio")),
        "dilution": _f(s.get("sbc_dilution_pct_yr")),
        "incremental_roic_pct": _f(s.get("incremental_roic_pct")),
        "base_effect": base_effect, "base_effect_detail": base_effect_detail,
        "cyclical": cyclical, "cycle_guard": cycle_guard, "cycle_guard_detail": cycle_guard_detail,
    }


def own_score_v4(rows: list) -> list:
    """own_score v4 — 五個百分位排序鍵在 ELIGIBLE 集合內互相比較（pure，跨檔）。
    `rows`：ELIGIBLE 母體，元素可以是 own_raw() 的輸出（帶 "rev" key）或完整
    stock dict（本函式會自動套一次 own_raw()），順序與回傳列表一一對應。

    百分位＝100 × (population 中 ≤ 自己的比例)（"weak" 定義，含自己），dilution 反向
    （越低分位越高）。品質分位 p_q＝FCF/淨利與稀釋率兩個分位的平均，但
    incremental_roic_pct ≥15（投資有回報）者免計 FCF/淨利、p_q 只看稀釋率分位
    （見 grp.py 檔頭 v4 段第 4 點）。score＝五個分位（p_rev/p_mom/p_g/p_q/p_ey）
    平均，至少 4/5 有值才給分，否則 None（呼叫端應把 None 排除出排名，不要當 0 用）。
    """
    raws = [r if "rev" in r else own_raw(r) for r in rows]

    def pctl(key, sign=1.0):
        vals = sorted(rw[key] * sign for rw in raws if rw.get(key) is not None)
        n = len(vals)
        out = []
        for rw in raws:
            v = rw.get(key)
            if v is None or n == 0:
                out.append(None)
            else:
                out.append(round(100.0 * sum(1 for x in vals if x <= v * sign) / n, 1))
        return out

    p_rev = pctl("rev"); p_mom = pctl("mom"); p_g = pctl("g"); p_ey = pctl("ey")
    p_fcf_ni = pctl("fcf_ni"); p_dil = pctl("dilution", sign=-1.0)
    # v4.1 循環股守門（見 own_raw() docstring／rule_ledger「v4.1 基期效應＋循環股
    # 守門」列）：cycle_guard=True 的列，成長分位／盈餘殖利率分位封頂 50 再平均——
    # 循環股在景氣高點常同時出現「爆量成長」與「PEG 低到可疑」，不封頂會讓 own_score
    # 排序被循環見頂訊號誤判成複利成長。
    for i, rw in enumerate(raws):
        if rw.get("cycle_guard"):
            if p_g[i] is not None:
                p_g[i] = min(p_g[i], CYCLE_GUARD_PCTL_CAP)
            if p_ey[i] is not None:
                p_ey[i] = min(p_ey[i], CYCLE_GUARD_PCTL_CAP)
    out = []
    for i, rw in enumerate(raws):
        incr = rw.get("incremental_roic_pct")
        exempt = incr is not None and incr >= 15.0
        if exempt:
            p_q = p_dil[i]
        else:
            qs = [x for x in (p_fcf_ni[i], p_dil[i]) if x is not None]
            p_q = round(sum(qs) / len(qs), 1) if qs else None
        parts = [x for x in (p_rev[i], p_mom[i], p_g[i], p_q, p_ey[i]) if x is not None]
        score = round(sum(parts) / len(parts), 1) if len(parts) >= 4 else None
        out.append({"p_rev": p_rev[i], "p_mom": p_mom[i], "p_g": p_g[i], "p_q": p_q,
                    "p_ey": p_ey[i], "q_fcf_ni_exempt": exempt, "score": score, "raw": rw,
                    "base_effect": rw.get("base_effect"), "base_effect_detail": rw.get("base_effect_detail"),
                    "cyclical": rw.get("cyclical"), "cycle_guard": rw.get("cycle_guard"),
                    "cycle_guard_detail": rw.get("cycle_guard_detail")})
    return out


_STAGE_RED = ("S0",)
_STAGE_GREEN = ("S1", "S3", "S4")


def timing_lamp(s: dict) -> dict:
    """v4 時機燈（pure）——把位置／RS／200 日線／階段收斂成單一燈號＋倉位建議。
    輸入（皆從 s 讀，呼叫端須先把這些欄位就緒——build_arena 在呼叫前注入
    `s["_stage_code"]`＝docs/stages/data/lamp.json 查到的階段代碼，
    `s["_overheated"]`＝grp_score() 算好的 overheated 布林）：
      s["ma"]["above_w52"], s["timing"]["vs_200ma_pct"/"rs_score"/"dist_52w_high_pct"],
      s["_stage_code"], s["_overheated"]
    輸出：{"code","label","size","trigger","why"}，見 grp.py 檔頭 v4 段第 5 點。
    優先序：out（未站上 52 週線）＞ red（結構轉弱）＞ hot（過熱）＞ green（多頭排列）
    ＞ yellow（其餘站上 52 週線者）。"""
    ma = s.get("ma") or {}
    timing = s.get("timing") or {}
    above_w52 = ma.get("above_w52")
    vs200 = _f(timing.get("vs_200ma_pct"))
    rs = _f(timing.get("rs_score"))
    dist_hi = _f(timing.get("dist_52w_high_pct"))
    stage = s.get("_stage_code")
    overheated = bool(s.get("_overheated"))

    if not above_w52:
        return {"code": "out", "label": "⚫ 不合格", "size": 0.0, "trigger": None,
                "why": "未站上 52 週線"}

    red_hits = []
    if vs200 is not None and vs200 < 0:
        red_hits.append(("站回 200 日線且 RS ≥ 50", f"vs 200 日線 {vs200:+.1f}%"))
    if rs is not None and rs < 40:
        red_hits.append(("RS 回到 50 以上", f"RS {rs:.0f}"))
    if dist_hi is not None and dist_hi < -25:
        red_hits.append(("回到高點 25% 內", f"距高點 {dist_hi:+.1f}%"))
    if stage in _STAGE_RED:
        red_hits.append(("站回 200 日線且 RS ≥ 50", "階段 S0 弱勢"))
    if red_hits:
        trigger = red_hits[0][0]
        return {"code": "red", "label": "🔴 等板機", "size": 0.0, "trigger": trigger,
                "why": "、".join(h[1] for h in red_hits)}

    if overheated:
        return {"code": "hot", "label": "🟠 過熱", "size": 0.5, "trigger": None,
                "why": "12-1 個月動能過熱"}

    stage_ok = stage is None or stage in _STAGE_GREEN
    if (vs200 is not None and vs200 >= 0 and rs is not None and rs >= 50
            and dist_hi is not None and dist_hi >= -15 and stage_ok):
        return {"code": "green", "label": "🟢 可進", "size": 1.0, "trigger": None,
                "why": f"vs 200 日線 {vs200:+.1f}%、RS {rs:.0f}、距高點 {dist_hi:+.1f}%"
                       + (f"、階段 {stage}" if stage else "")}

    bits = []
    if vs200 is not None: bits.append(f"vs 200 日線 {vs200:+.1f}%")
    if rs is not None: bits.append(f"RS {rs:.0f}")
    if dist_hi is not None: bits.append(f"距高點 {dist_hi:+.1f}%")
    if stage: bits.append(f"階段 {stage}")
    return {"code": "yellow", "label": "🟡 半倉", "size": 0.5, "trigger": None,
            "why": "、".join(bits) or "站上 52 週線但未達綠燈條件"}


def grp_score(s: dict) -> dict:
    """latest.json 一檔 → GRP v4 判定。回傳 {pass, g, r, p_label, veto, overheated, peak,
    own, own_v2, score, why[]}。score 為 0.0 佔位——真正的 v4 排序分需要跨檔百分位
    （見 own_score_v4()），由呼叫端（build_arena）算完 ELIGIBLE 集合後回填 grp["own"]
    與 grp["score"]。"""
    why = []
    # G（v4：三年期 Koyfin CAGR 為硬性必備——g_three_year 記錄這個 g 是不是真的三年期
    # FY1→FY3 CAGR；QGM 供給列（_g_method=="FY1→FY2 單年"）把單年成長塞進同一個
    # eps_fy1_fy3_cagr_pct 欄位，欄位存在不代表三年，故排除該情況。門檻：durable_5y
    # 為 True 者 10%，否則 15%（見檔頭 v4 段）——durable_5y 由呼叫端 build_arena
    # ._apply_durable_fallback() 先補好，本函式只讀不算。）
    g_raw_3y, base_effect, base_effect_detail = _base_effect_growth(s)
    g_three_year = g_raw_3y is not None and s.get("_g_method") != "FY1→FY2 單年"
    g = g_raw_3y
    if g is None:
        g = _f(s.get("eps2y_live")) or _f(s.get("eps2y"))
        if g is not None:
            why.append("成長閘用 2 年成長率代替（缺 FY3 預估，v4 不採計為資格）")
    g_min = G_MIN_CAGR_DURABLE if s.get("durable_5y") else G_MIN_CAGR
    g_pass = bool(g_three_year) and g is not None and g >= g_min
    if not g_pass:
        if not g_three_year:
            why.append(f"成長閘未過（v4 需三年期 Koyfin CAGR，現值 {g if g is not None else '缺'}）")
        else:
            why.append(f"成長閘未過（CAGR {g if g is not None else '缺'} < {g_min:.0f}%）")

    # R（v4：上修否決；2026-09-17 財報錨定上修起改讀 eps_rev_since_earnings_pct
    # ／eps_rev_3m_pct 後備，見 _revision_anchor()；FY+1 單月否決仍是兩者皆缺時
    # 的最終 fallback）
    eps_rev_3m = _f(s.get("eps_rev_3m_pct"))   # 舊欄位，仍保留供顯示/對照（見 docstring）
    rev_value, rev_anchor, rev_baseline_date = _revision_anchor(s)
    r_fy1 = _f(s.get("eps_fy_next_revision_pct"))
    r_2y = _f(s.get("eps2y_revision_pp"))
    if rev_value is not None:
        r_veto = rev_value <= EPS_REV_3M_VETO
        if r_veto:
            anchor_label = "財報後上修" if rev_anchor == "earnings" else "三月上修"
            why.append(f"{anchor_label}否決（{rev_value:+.1f}% ≤ {EPS_REV_3M_VETO:.0f}%）")
    else:
        r_veto = r_fy1 is not None and r_fy1 <= R_VETO_FY1
        if r_veto:
            why.append(f"上修閘否決（財報後／三月上修皆缺值，fallback FY+1 下修 {r_fy1:+.1f}%）")
    r_pass = (not r_veto) and ((r_fy1 is not None and r_fy1 > R_MIN_FY1)
                               or (r_2y is not None and r_2y > R_MIN_2Y_PP))
    r_strength = max(r_fy1 or 0.0, (r_2y or 0.0) * 2.0)   # pp 換算近似倍率，僅舊排序對照用

    # P（不變：站上 52 週線＋距高位置標籤；過熱不再併入本閘，見下）
    ma = s.get("ma") or {}
    above_52w = bool(ma.get("above_w52"))
    dist_hi = _f((s.get("timing") or {}).get("dist_52w_high_pct"))   # 52 週高優先
    if dist_hi is None:
        dist_hi = _f(ma.get("dist_250w_high_pct"))                   # fallback：5 年高（較嚴）
    px = _f(ma.get("price"))
    p_label = None
    if above_52w and dist_hi is not None:
        if dist_hi >= P_BREAKOUT_DIST:
            p_label = "breakout"
        elif P_PULLBACK[0] <= dist_hi <= P_PULLBACK[1]:
            p_label = "pullback"
        else:
            p_label = "in_trend"
    p_pass = above_52w and (p_label in ("breakout", "pullback", "in_trend"))
    if not p_pass:
        why.append("位置閘未過（站在 52 週線下或資料缺）")

    # 新增硬否決（v4，2026-09-17）：體質拒絕／衰退 ⛔／DD 迴避（180 天內）
    quality_veto_level = s.get("quality_veto_level")
    decline_signal_light = s.get("decline_signal_light")
    veto_quality = quality_veto_level == "拒絕"
    veto_decline = decline_signal_light == "⛔"
    dd_age = _f(s.get("dd_age_days"))
    veto_dd_avoid = s.get("dca_verdict") == "迴避" and (dd_age is None or dd_age <= DD_FRESH_DAYS)
    if veto_quality:
        why.append("體質閘：拒絕（quality_veto_level）")
    if veto_decline:
        why.append("衰退訊號 ⛔（decline_signal_light）")
    if veto_dd_avoid:
        age_txt = f"{int(dd_age)}d 內" if dd_age is not None else ""
        why.append(f"DD 迴避否決{age_txt}")
    veto = bool(r_veto or veto_quality or veto_decline or veto_dd_avoid)

    # 過熱／頂點（v4）：不是資格閘，只決定核心候選資格（過熱）與顯示註記（頂點）。
    # 過熱＝12-1 個月動能 >150%，缺值 fallback 26 週漲幅 >80%（s["_r26"]，
    # build_arena.row_dict 在呼叫本函式前已就緒）。頂點＝roic_vs_5y_x ≥1.3，純顯示——
    # 實測回溯 NVDA／CLS 皆頂點仍穩居核心候選前 5，見檔頭 v4 段第 3 點。
    mom = _f(ma.get("mom_12_1_pct"))
    r26 = _f(s.get("_r26"))
    if mom is not None:
        overheated = mom > MOM_12_1_OVERHEAT
    else:
        overheated = r26 is not None and r26 > R26_OVERHEAT_FALLBACK
    roic_vs_5y_x = _f(s.get("roic_vs_5y_x"))
    peak = roic_vs_5y_x is not None and roic_vs_5y_x >= PEAK_ROIC_X

    # 融券高（v4.1，2026-09-17）：不是資格閘、不進 own_score 排序——只比照 overheated
    # 的待遇排除核心候選（衛星照樣能坐）。見檔頭 SI_CORE_EXCLUDE_PCT 常數註解。
    si_pct = _f(s.get("short_interest_pct_float"))
    high_short_interest = si_pct is not None and si_pct > SI_CORE_EXCLUDE_PCT

    all_pass = g_pass and (not veto) and p_pass
    if not r_pass and not r_veto:
        why = [w for w in why if not w.startswith("上修閘未過")]
    own_v2 = own_score(s, g)     # v2 公式原封不動，供對照一輪（own_v2，見檔頭 v4 段第 4 點）
    q = quality_gate(s)
    return {"pass": all_pass and q["pass"], "veto": veto,
            # v4 硬否決細項（build_arena.hard_veto_v4 月度輪動用，避免對 why[] 字串解析）：
            "veto_revision": r_veto, "veto_quality_reject": veto_quality,
            "veto_decline": veto_decline, "veto_dd_avoid": veto_dd_avoid,
            "g": round(g, 1) if g is not None else None,
            "g_three_year": g_three_year if g is not None else None,
            "g_min": g_min,
            "r_fy1": r_fy1, "r_2y": r_2y, "r_pass": r_pass,
            "eps_rev_3m_pct": eps_rev_3m,
            # 財報錨定上修（2026-09-17）：veto 與排序實際採用的值/錨定方式/基準
            # 快照日——build_arena 席位表用這三個欄位渲染「財報後上修」欄與
            # tooltip，不用再自行重跑 _revision_anchor()。
            "rev_used_pct": rev_value, "rev_anchor": rev_anchor,
            "rev_baseline_date": rev_baseline_date,
            "days_to_next_earnings": s.get("days_to_next_earnings"),
            "r_strength": round(r_strength, 2),
            "p_label": p_label, "dist_hi": dist_hi, "price": px, "above_w52": above_52w,
            "overheated": overheated, "peak": peak, "roic_vs_5y_x": roic_vs_5y_x,
            "high_short_interest": high_short_interest, "short_interest_pct_float": si_pct,
            "base_effect": base_effect, "base_effect_detail": base_effect_detail,
            "quality": q, "own": {"raw": own_raw(s), "score": None},   # 跨檔百分位由 build_arena 回填
            "own_v2": own_v2,
            "score": 0.0,   # 佔位；build_arena 算完 own_score_v4() 後覆寫
            "score_v1": round(r_strength + (g or 0) / 100.0, 3),          # v1/v2 R 排序（對照用）
            "why": why + ([] if q["pass"] else q["why"])}


def quality_gate(s: dict) -> dict:
    """擁有層品質閘（v2）：ROIC ≥15 ∧ FCF ≥10，或 capex 週期豁免（ROIC ≥25 ∧ FCF ≥0）。
    金融股（roic 與 fcf 皆缺）→ pass=None（另軌，不判過不過）。"""
    roic = _f(s.get("roic")); fcf = _f(s.get("fcf"))
    if roic is None and fcf is None:
        return {"pass": None, "roic": None, "fcf": None, "why": ["品質欄缺（金融／另軌）"], "exempt": False}
    why = []
    base = (roic is not None and roic >= Q_ROIC_MIN) and (fcf is not None and fcf >= Q_FCF_MIN)
    exempt = (not base) and (roic is not None and roic >= Q_ROIC_EXEMPT) and (fcf is not None and fcf >= 0)
    if not base and not exempt:
        if roic is None or roic < Q_ROIC_MIN:
            why.append(f"品質閘 ROIC {roic if roic is not None else '缺'}")
        if fcf is None or fcf < Q_FCF_MIN:
            why.append(f"品質閘 FCF {fcf if fcf is not None else '缺'}")
    return {"pass": bool(base or exempt), "roic": roic, "fcf": fcf, "exempt": exempt, "why": why}


def own_score(s: dict, g=None) -> dict:
    """擁有層排序鍵（v2）：min(G，30) ＋ FY1 盈餘殖利率% ＋ 持續期加分 － 倍數風險。
    盈餘殖利率優先取 live_fpe_est（與現價同尺）；缺則 eps_fy_next / price。"""
    if g is None:
        g = _f(s.get("eps_fy1_fy3_cagr_pct"))
        if g is None:
            g = _f(s.get("eps2y_live")) or _f(s.get("eps2y"))
    fpe = _f(s.get("live_fpe_est"))
    ey = (100.0 / fpe) if fpe and fpe > 0 else None
    if ey is None:
        px = _f((s.get("ma") or {}).get("price")); e1 = _f(s.get("eps_fy_next"))
        if px and e1 and px > 0:
            ey = e1 / px * 100.0
    roic = _f(s.get("roic")); peg = _f(s.get("live_peg")) or _f(s.get("peg"))
    if g is None:
        return {"score": None, "g_capped": None, "ey": ey, "durable": False, "peg_penalty": False}
    sc = min(g, OWN_G_CAP) + (ey or 0.0)
    durable = roic is not None and roic >= OWN_DURABLE_ROIC
    pen = peg is not None and peg > OWN_PEG_PENALTY
    sc += 2.0 if durable else 0.0
    sc -= 5.0 if pen else 0.0
    return {"score": round(sc, 2), "g_capped": round(min(g, OWN_G_CAP), 1),
            "ey": round(ey, 2) if ey is not None else None, "durable": durable, "peg_penalty": pen}


P_LABEL_HTML = {"breakout": '<span class="tag tag-up">🟢 突破帶</span>',
                "pullback": '<span class="tag tag-up">🟢 回踩到位</span>',
                "in_trend": '<span class="tag tag-pool">🟡 趨勢帶內</span>',
                None: '<span class="tag tag-dn">🔴 不適合</span>'}


# ── 軌別路由（核心 vs 衛星，v3 2026-09-09 持有人拍板改版）───────────────────
# v3 席位資格（見 knowledge/rule_ledger.md 同名列）：DD 不再是入席前提，DD 角色
# （dca_role）也不再決定軌別，只當顯示標籤（build_arena.row_dict 的 role_mismatch
# 仍拿它跟本函式的軌別比對、標記分歧供人工複審）。核心席資格改為單一耐久判定：
# 五年 ROIC 平均（Koyfin roic_5y_avg_pct via s["durable_5y"]/s["durable_source"]，
# 見 build_dd_screener.enrich_ticker）≥15%，或缺 Koyfin 資料時 fallback QGM 五年
# ROIC 穩定度（roic_5y_stability.pct_above）≥75%——耐久達標才進核心候選，否則
# （未達標或無耐久資料）只能衛星。s["durable_5y"]/s["durable_source"] 由呼叫方
# （build_arena._apply_durable_fallback）先行正規化好，本函式不再自行讀 QGM 檔。
DD_FRESH_DAYS = 180      # v2：DD 超過此天數視同無 DD（角色標籤失效、只留證據）

_DURABLE_LABEL = {"koyfin-xlsx": "五年 ROIC 平均 ≥15%", "qgm": "QGM 五年穩定度 ≥75%"}


def grp_route(s: dict) -> tuple[str, str]:
    """回傳 (軌別 core|satellite, 理由)。前提：GRP 已 pass。
    v3：耐久達標（durable_5y is True）→ 核心候選；未達標或無耐久資料 → 只能衛星。
    DD 角色不影響軌別，只在 build_arena.row_dict 當 role_mismatch 比對用的顯示標籤。"""
    durable = s.get("durable_5y")
    if durable:
        label = _DURABLE_LABEL.get(s.get("durable_source"), "耐久達標")
        return "core", f"{label}＝複利耐久"
    if durable is False:
        label = _DURABLE_LABEL.get(s.get("durable_source"), "耐久資料")
        return "satellite", f"{label}未達標，只能衛星"
    return "satellite", "耐久資料不足，只能衛星"
