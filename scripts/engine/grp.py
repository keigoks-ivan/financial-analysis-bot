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
"""
from __future__ import annotations

import json
from pathlib import Path

G_MIN_CAGR = 15.0        # G 閘：FY1→FY3 EPS CAGR
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
R_VETO_FY1 = -10.0       # R 否決（v2）：FY+1 單月下修超過此值才否決；−2% 降為燈號（見檔頭 v2）
P_BREAKOUT_DIST = -5.0   # 距 52 週高 ≥ -5% ＝突破帶
P_PULLBACK = (-25.0, -8.0)   # 回檔帶（含趨勢完好）


def _f(v):
    try:
        f = float(v)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


def grp_score(s: dict) -> dict:
    """latest.json 一檔 → GRP 判定。回傳 {pass, g, r, p_label, veto, score, why[]}。
    score 只在全過時有意義（= R 主排序鍵，tiebreak G）。"""
    why = []
    # G
    # v3 席位資格（2026-09-09）：g_three_year 記錄這個 g 是不是真的三年期 Koyfin
    # FY1→FY3 CAGR——QGM 供給列（_g_method=="FY1→FY2 單年"）把單年成長塞進同一個
    # eps_fy1_fy3_cagr_pct 欄位（見 build_arena.load_qgm_rows），欄位存在不代表
    # 三年，故排除該情況；一旦這檔改走 dd-screener（--include-non-dd）拿到真 Koyfin
    # 三年 CAGR，_g_method 就不會被設，g_three_year 會正確變 True。build_arena 的
    # seat_universe 用這個欄位當入席資格閘（見該檔 main()）。
    g_raw_3y = _f(s.get("eps_fy1_fy3_cagr_pct"))
    g_three_year = g_raw_3y is not None and s.get("_g_method") != "FY1→FY2 單年"
    g = g_raw_3y
    if g is None:
        g = _f(s.get("eps2y_live")) or _f(s.get("eps2y"))
        if g is not None:
            why.append("成長閘用 2 年成長率代替（缺 FY3 預估）")
    g_pass = g is not None and g >= G_MIN_CAGR
    if not g_pass:
        why.append(f"成長閘未過（CAGR {g if g is not None else '缺'}）")

    # R
    r_fy1 = _f(s.get("eps_fy_next_revision_pct"))
    r_2y = _f(s.get("eps2y_revision_pp"))
    veto = r_fy1 is not None and r_fy1 <= R_VETO_FY1
    r_pass = (not veto) and ((r_fy1 is not None and r_fy1 > R_MIN_FY1)
                             or (r_2y is not None and r_2y > R_MIN_2Y_PP))
    if veto:
        why.append(f"上修閘否決（FY+1 下修 {r_fy1:+.1f}%）")
    elif not r_pass:
        why.append(f"上修閘未過（FY+1 {r_fy1 if r_fy1 is not None else '缺'}％／2Y {r_2y if r_2y is not None else '缺'}pp）")
    r_strength = max(r_fy1 or 0.0, (r_2y or 0.0) * 2.0)   # pp 換算近似倍率，僅排序用

    # P
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
    p_pass = p_label in ("breakout", "pullback", "in_trend")
    if not p_pass:
        why.append("位置閘未過（站在 52 週線下或資料缺）")

    # v2：R 閘降為燈號——資格不再要求「有上修」，只留重下修否決；排序改擁有層 own_score
    all_pass = g_pass and (not veto) and p_pass
    if not r_pass and not veto:
        why = [w for w in why if not w.startswith("上修閘未過")]
    own = own_score(s, g)
    q = quality_gate(s)
    return {"pass": all_pass and q["pass"], "veto": veto,
            "g": round(g, 1) if g is not None else None,
            "g_three_year": g_three_year if g is not None else None,   # v3：入席資格用（僅 build_arena.seat_universe 讀）
            "r_fy1": r_fy1, "r_2y": r_2y, "r_pass": r_pass,
            "r_strength": round(r_strength, 2),
            "p_label": p_label, "dist_hi": dist_hi, "price": px,
            "quality": q, "own": own,
            "score": own["score"] if own["score"] is not None else 0.0,   # v2：擁有層排序鍵
            "score_v1": round(r_strength + (g or 0) / 100.0, 3),          # 舊 R 排序（對照用）
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
