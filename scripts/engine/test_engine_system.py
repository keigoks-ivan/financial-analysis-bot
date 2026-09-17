#!/usr/bin/env python3
"""決策引擎系統測試 — GRP 閘門／軌別路由／市值門檻／卡片結算／光卡合併／資料一致性.

跑法：python3 scripts/engine/test_engine_system.py
涵蓋：
  [1] GRP 三閘語義（合成輸入的邊界值）
  [2] 軌別路由（v3：耐久判定 durable_5y → core/satellite；DD/moat 降為顯示標籤）
  [3] 市值門檻（cap_ok 三態：過/不過/未知 fail-closed）
  [4] 卡片 claim 結算（auto_price 比較子、非價格單位防衛、到期判定）
  [5] 光卡合併優先序（dd-meta 裁決讓位）
  [6] 站上資料一致性（席位∈卡片牆、席位全過 GRP＋市值、REIT 不在主榜、
      帳本 append-only 結構、五頁可解析）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.grp import (  # noqa: E402
    MKTCAP_MIN, cap_ok, grp_route, grp_score, market_ok,
)
from engine.build_cards import settle_claim  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
ENG = ROOT / "docs" / "engine"
N_PASS = 0


def ok(cond, msg):
    global N_PASS
    if not cond:
        raise AssertionError(f"FAIL: {msg}")
    N_PASS += 1
    print(f"  ✓ {msg}")


def _stock(**kw):
    base = {"eps_fy1_fy3_cagr_pct": 25.0, "eps_fy_next_revision_pct": 1.0,
            "eps2y_revision_pp": 0.5, "moat_grade": "A", "moat_trend": "→",
            "roic": 20.0, "fcf": 15.0, "live_fpe_est": 25.0,
            "ma": {"above_w52": True, "price": 100.0},
            "timing": {"dist_52w_high_pct": -10.0}}
    base.update(kw)
    return base


def test_grp_gates():
    print("[1] GRP v4 資格閘語義")
    g = grp_score(_stock())
    ok(g["pass"] and g["p_label"] == "pullback", "基準樣本全過、回踩帶標籤")
    ok(not grp_score(_stock(eps_fy1_fy3_cagr_pct=14.9, durable_5y=False))["pass"],
       "非耐久 G 14.9 < 15 → fail")
    ok(grp_score(_stock(eps_fy1_fy3_cagr_pct=12.0, durable_5y=True))["pass"],
       "v4：durable_5y=True 放寬成長門檻至 10%，12% 應過")
    ok(not grp_score(_stock(eps_fy1_fy3_cagr_pct=12.0, durable_5y=False))["pass"],
       "同一個 12%，非耐久仍卡在 15% 門檻")
    g = grp_score(_stock(eps_fy1_fy3_cagr_pct=None, eps2y=40.0, durable_5y=True))
    ok(not g["pass"], "v4：成長閘硬性要求三年期 Koyfin CAGR，單年 fallback 不算資格")
    # v4：三月上修否決取代 FY+1 單月否決
    g = grp_score(_stock(eps_rev_3m_pct=-6.0, eps_fy_next_revision_pct=5.0))
    ok(g["veto"] and not g["pass"], "三月上修 -6% ≤ -5% → 否決（FY+1 正值也救不回）")
    g = grp_score(_stock(eps_rev_3m_pct=None, eps_fy_next_revision_pct=-12.0))
    ok(g["veto"], "三月上修缺值 → fallback FY+1 單月 ≤-10% 否決")
    g = grp_score(_stock(eps_rev_3m_pct=None, eps_fy_next_revision_pct=-8.0))
    ok(not g["veto"], "fallback 否決線是 -10%，-8% 不否決")
    g = grp_score(_stock(eps_rev_3m_pct=1.0, eps_fy_next_revision_pct=-50.0))
    ok(not g["veto"], "三月上修存在時不看 FY+1 fallback")
    # v4：新硬否決（體質拒絕／衰退 ⛔／DD 迴避 180 天內）
    ok(grp_score(_stock(quality_veto_level="拒絕"))["veto"], "體質閘拒絕 → 否決")
    ok(grp_score(_stock(decline_signal_light="⛔"))["veto"], "衰退訊號 ⛔ → 否決")
    ok(grp_score(_stock(dca_verdict="迴避", dd_age_days=30))["veto"], "180 天內 DD 迴避 → 否決")
    ok(not grp_score(_stock(dca_verdict="迴避", dd_age_days=200))["veto"],
       "超過 180 天的舊迴避裁決不否決")
    # v4：過熱／頂點不擋資格，只是旗標
    g = grp_score(_stock(ma={"above_w52": True, "price": 100.0, "mom_12_1_pct": 200.0},
                         timing={"dist_52w_high_pct": -10.0}))
    ok(g["overheated"] and g["pass"], "過熱（12-1 月動能 >150%）不擋資格，只標旗標")
    g = grp_score(_stock(roic_vs_5y_x=2.0))
    ok(g["peak"] and g["pass"], "頂點（roic_vs_5y_x ≥1.3）純顯示，不擋資格")
    ok(not grp_score(_stock(roic=12.0))["pass"], "品質閘 ROIC 12 < 15 → fail")
    ok(not grp_score(_stock(fcf=5.0))["pass"], "品質閘 FCF 5 < 10（ROIC 20 未達豁免）→ fail")
    g = grp_score(_stock(roic=26.0, fcf=3.0))
    ok(g["pass"] and g["quality"]["exempt"], "capex 週期豁免：ROIC 26 ∧ FCF 3 → 過")
    ok(grp_score(_stock(roic=None, fcf=None))["quality"]["pass"] is None, "金融（品質欄全缺）→ None 另軌")
    g = grp_score(_stock(ma={"above_w52": False, "price": 100.0}))
    ok(not g["pass"] and g["p_label"] is None, "52 週線下 → P fail")
    ok(grp_score(_stock(timing={"dist_52w_high_pct": -3.0}))["p_label"] == "breakout",
       "距高 -3% → 突破帶")
    ok(grp_score(_stock(timing={"dist_52w_high_pct": -30.0}))["p_label"] == "in_trend",
       "距高 -30%（趨勢在但深回檔）→ 趨勢內，不給回踩帶標籤")


def test_own_score_v4():
    print("[1b] own_score v4：跨檔百分位＋FCF/淨利豁免")
    from engine.grp import own_score_v4
    rows = [
        {"rev": 10, "mom": 20, "g": 25, "ey": 4, "fcf_ni": 1.2, "dilution": 1.0,
         "incremental_roic_pct": None},
        {"rev": 5, "mom": 10, "g": 15, "ey": 3, "fcf_ni": 0.8, "dilution": 2.0,
         "incremental_roic_pct": 20.0},
        {"rev": -2, "mom": -5, "g": 10, "ey": 2, "fcf_ni": 0.5, "dilution": 3.0,
         "incremental_roic_pct": None},
        {"rev": 20, "mom": 30, "g": 30, "ey": 5, "fcf_ni": None, "dilution": 0.5,
         "incremental_roic_pct": None},
        {"rev": 0, "mom": 0, "g": None, "ey": None, "fcf_ni": 1.0, "dilution": 1.5,
         "incremental_roic_pct": None},
    ]
    out = own_score_v4(rows)
    ok(out[3]["score"] == 100.0, "全軸最佳值 → 排名分 100")
    ok(out[4]["score"] is None, "只有 3/5 百分位有值 → score None（不參與排名）")
    ok(out[1]["q_fcf_ni_exempt"] is True, "incremental_roic_pct ≥15 → 免計 FCF/淨利")


def test_route():
    print("[2] 軌別路由（v3：耐久判定，DD 角色/moat 只當顯示標籤）")
    ok(grp_route(_stock(durable_5y=True, durable_source="koyfin-xlsx"))[0] == "core",
       "Koyfin 五年 ROIC 平均 ≥15%（durable_5y=True）→ 核心")
    ok(grp_route(_stock(durable_5y=True, durable_source="qgm"))[0] == "core",
       "QGM 五年穩定度 ≥75%（durable_5y=True）→ 核心")
    ok(grp_route(_stock(durable_5y=False, durable_source="koyfin-xlsx"))[0] == "satellite",
       "耐久數字存在但未達門檻（durable_5y=False）→ 衛星")
    ok(grp_route(_stock(durable_5y=None))[0] == "satellite",
       "無耐久資料（durable_5y=None）→ 衛星（保守）")
    # DD 角色與 moat 字母不再決定軌別，只當顯示標籤（見 build_arena.row_dict 的 role_mismatch）——
    # 就算 DD 判過進場＋核心角色、moat S，耐久未達標／缺耐久資料一樣落衛星。
    ok(grp_route(_stock(durable_5y=None, moat_grade="S", dca_verdict="進場", dca_role="核心",
                        dd_age_days=30))[0] == "satellite",
       "v3：DD 角色核心＋moat S 但無耐久資料 → 仍衛星（DD/moat 降為顯示標籤，不影響軌別）")
    ok(grp_route(_stock(durable_5y=True, durable_source="qgm", dca_verdict="迴避",
                        dca_role="衛星"))[0] == "core",
       "v3：DD 角色衛星但耐久達標 → 核心（軌別只看耐久，veto 由 row_dict 另外處理）")


def test_cap_floor():
    print("[3] 市值門檻（≥$%dB）" % (MKTCAP_MIN / 1e9))
    ok(cap_ok(MKTCAP_MIN) is True, "剛好在門檻 → 過")
    ok(cap_ok(MKTCAP_MIN - 1) is False, "低一元 → 不過")
    ok(cap_ok(None) is None, "市值未知 → None（資格層 fail-closed）")


def test_market_gate():
    print("[3b] 母體市場門檻（v2：美股含 ADR，台股另建 2026-09-02）")
    ok(market_ok("2330.TW") is False, ".TW 掛牌 → 排除")
    ok(market_ok("TSM") is True, "ADR → 照常納入")


def test_claim_settlement():
    print("[4] 卡片 claim 結算")
    # 防衛：非價格單位的 auto_price 不得用股價結算
    c = settle_claim({"check": "auto_price", "unit": "x", "comparator": ">=",
                      "threshold": 30.0, "deadline": "2099-01-01"}, "NVDA")
    ok(c["settle"] == "watch" and c.get("auto_downgraded"), "P/E 類 auto_price → 降級人工（防假觸發）")
    # 到期判定
    c = settle_claim({"check": "manual", "deadline": "2020-01-01"}, "NVDA")
    ok(c["settle"] == "due", "過期未結算 → ⏰ due")
    c = settle_claim({"check": "manual", "deadline": "2099-01-01"}, "NVDA")
    ok(c["settle"] == "watch", "未到期 → 監測中")
    # 人工回填凍結
    c = settle_claim({"check": "manual", "status": "pass", "deadline": "2020-01-01"}, "NVDA")
    ok(c["settle"] == "manual_done", "人工已回填 → 凍結不重算")
    # auto_price 真結算（NVDA 現價遠高於 1，比較子方向）
    c = settle_claim({"check": "auto_price", "unit": "USD", "comparator": "<=",
                      "threshold": 1.0, "deadline": "2099-01-01"}, "NVDA")
    ok(c["settle"] == "watch" and c.get("last_price", 0) > 1, "價格未破線 → watch（帶現價）")
    c = settle_claim({"check": "auto_price", "unit": "USD", "comparator": ">=",
                      "threshold": 1.0, "deadline": "2099-01-01"}, "NVDA")
    ok(c["settle"] == "breach", "價格越線 → breach")


def test_dual_source_r():
    print("[5b] 兩源一致性防線（Koyfin × yfinance）")
    from engine.build_arena import cross_check_r
    base = {"grp": {"r_fy1": 1.0, "veto": False, "pass": True, "why": []}}
    r = cross_check_r(json.loads(json.dumps(base)), -12.0)
    ok(r["grp"]["veto"] and not r["grp"]["pass"], "yf 30d -12% → 保守否決（Koyfin 正也不豁免；v2 否決線 −10%）")
    r = cross_check_r(json.loads(json.dumps(base)), -2.5)
    ok(r["grp"]["pass"] and r.get("r_conflict"), "yf -2.5%（v2 未達否決線）→ 只標 ⚠ 源分歧不否決")
    r = cross_check_r(json.loads(json.dumps(base)), 5.0)
    ok(r["grp"]["pass"] and not r.get("r_conflict"), "兩源同向 → 無標記")
    r = cross_check_r(json.loads(json.dumps(base)), None)
    ok(r["grp"]["pass"] and "r_alt_yf30d" not in r, "第二源缺值 → 主源規則照舊，不誤傷")


def test_light_merge():
    print("[5] 光卡合併優先序")
    from engine.build_arena import load_light_rows
    stocks_map = {"SMTC": {"ticker": "SMTC", "dca_verdict": None},
                  "NVDA": {"ticker": "NVDA", "dca_verdict": "進場"}}
    rows = load_light_rows(stocks_map)
    tickers = {r["ticker"] for r in rows}
    ok("NVDA" not in tickers, "dd-meta 有裁決的名字光卡讓位")
    ok(all(r["route"] == "satellite" for r in rows), "光卡一律衛星路由（快審卡是衛星專屬第二資格來源，與 DD／耐久無關）")


def test_site_consistency():
    print("[6] 站上資料一致性")
    arena = json.loads((ENG / "arena.json").read_text(encoding="utf-8"))
    cards = json.loads((ENG / "cards.json").read_text(encoding="utf-8"))
    seats = arena["core_seats"] + arena["sat_seats"]
    missing = sorted(r["ticker"] for r in seats if r["ticker"] not in cards["by_ticker"])
    ok(missing == arena.get("seats_without_card", missing),
       f"無決策卡的席位已在 arena.json 明列（{len(missing)}/{len(seats)} 席：{'、'.join(missing) or '—'}）")
    ok(all(r["grp"]["pass"] or r.get("seat_note") == "現任" for r in seats),
       "席位全數過閘，或為月頻輪動沿用中的現任席（v4 寬限期：非硬否決不下席）")
    ok(all(r.get("cap_ok") for r in seats if "cap_ok" in r),
       "席位全數通過市值門檻")
    ok(all(r["route"] == "core" for r in arena["core_seats"]), "核心席全為 core 路由")
    # v3 席位資格修復（2026-09-09）：衛星席公開競爭——route=="core"（耐久達標）但沒卡進
    # 核心前 5 名的名字會跟 route=="satellite" 名字一起按 own_score 搶衛星席，故衛星席
    # 的 route 不再限定 satellite；改驗證核心／衛星席無重複 ticker（沒人同時坐兩席）。
    ok(all(r["route"] in ("core", "satellite") for r in arena["sat_seats"]),
       "衛星席由 satellite 路由、或耐久達標（core 路由）但未進核心前 5 名而暫居衛星的名字組成")
    core_tickers = {r["ticker"] for r in arena["core_seats"]}
    sat_tickers = {r["ticker"] for r in arena["sat_seats"]}
    ok(not (core_tickers & sat_tickers), "核心席與衛星席無重複 ticker（沒人同時坐兩席）")
    ok(all(not r["ticker"].endswith(".TW") for r in seats),
       "無席位為 .TW 掛牌（v2：台股另建，2026-09-02 拍板）")
    radar = json.loads((ENG / "radar.json").read_text(encoding="utf-8"))
    ok(all(r.get("sector") != "Real Estate" for r in radar["grp_board"]),
       "REIT 不在 GRP 主榜（Bug #1 迴歸防線）")
    ok(all((r.get("mktcap") or 0) >= MKTCAP_MIN for r in radar["grp_board"]),
       "主榜全數達市值門檻")
    ledger = json.loads((ENG / "arena-ledger.json").read_text(encoding="utf-8"))
    dates = [s["date"] for s in ledger["snapshots"]]
    ok(dates == sorted(dates), "席位帳本時序遞增（append-only 結構）")
    import html.parser
    for f in ("index", "radar", "arena", "cards", "scoreboard"):
        p = html.parser.HTMLParser()
        p.feed((ENG / f"{f}.html").read_text(encoding="utf-8"))
    ok(True, "五頁 HTML 全部可解析")


if __name__ == "__main__":
    for fn in (test_grp_gates, test_own_score_v4, test_route, test_cap_floor, test_market_gate,
               test_claim_settlement, test_dual_source_r, test_light_merge,
               test_site_consistency):
        fn()
    print(f"\nALL PASS — {N_PASS} 斷言")
