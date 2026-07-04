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
"""
from __future__ import annotations

G_MIN_CAGR = 15.0        # G 閘：FY1→FY3 EPS CAGR
# R 閘語意＝「有上修」（正向即可，非拐點級門檻——+2%/+1pp 是循環軌找拐點用的，
# 對穩定複利股會全滅；上修「幅度」由排序層獎勵，資格層只問方向）
R_MIN_FY1 = 0.0          # R 閘：FY+1 單月修正 > 0
R_MIN_2Y_PP = 0.0        # R 閘：eps2y 修正 pp > 0（替代路徑）
R_VETO_FY1 = -2.0        # R 否決：FY+1 單月下修超過此值
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
    g = _f(s.get("eps_fy1_fy3_cagr_pct"))
    if g is None:
        g = _f(s.get("eps2y_live")) or _f(s.get("eps2y"))
        if g is not None:
            why.append("G 用 eps2y fallback（無 FY3 預估）")
    g_pass = g is not None and g >= G_MIN_CAGR
    if not g_pass:
        why.append(f"G fail（CAGR {g if g is not None else '缺'}）")

    # R
    r_fy1 = _f(s.get("eps_fy_next_revision_pct"))
    r_2y = _f(s.get("eps2y_revision_pp"))
    veto = r_fy1 is not None and r_fy1 <= R_VETO_FY1
    r_pass = (not veto) and ((r_fy1 is not None and r_fy1 > R_MIN_FY1)
                             or (r_2y is not None and r_2y > R_MIN_2Y_PP))
    if veto:
        why.append(f"R 否決（FY+1 下修 {r_fy1:+.1f}%）")
    elif not r_pass:
        why.append(f"R fail（FY+1 {r_fy1 if r_fy1 is not None else '缺'}％／2Y {r_2y if r_2y is not None else '缺'}pp）")
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
        why.append("P fail（52 週線下或無資料）")

    all_pass = g_pass and r_pass and p_pass
    return {"pass": all_pass, "veto": veto,
            "g": round(g, 1) if g is not None else None,
            "r_fy1": r_fy1, "r_2y": r_2y,
            "r_strength": round(r_strength, 2),
            "p_label": p_label, "dist_hi": dist_hi, "price": px,
            "score": round(r_strength + (g or 0) / 100.0, 3),  # R 主鍵、G 微 tiebreak
            "why": why}


P_LABEL_HTML = {"breakout": '<span class="tag tag-up">🟢 突破帶</span>',
                "pullback": '<span class="tag tag-up">🟢 回踩到位</span>',
                "in_trend": '<span class="tag tag-pool">🟡 趨勢內</span>',
                None: '<span class="tag tag-dn">🔴 不適合</span>'}
