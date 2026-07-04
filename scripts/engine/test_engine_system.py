#!/usr/bin/env python3
"""決策引擎系統測試 — GRP 閘門／軌別路由／市值門檻／卡片結算／光卡合併／資料一致性.

跑法：python3 scripts/engine/test_engine_system.py
涵蓋：
  [1] GRP 三閘語義（合成輸入的邊界值）
  [2] 軌別路由（moat → core/satellite）
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
    MKTCAP_MIN, cap_ok, grp_route, grp_score,
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
            "ma": {"above_w52": True, "price": 100.0},
            "timing": {"dist_52w_high_pct": -10.0}}
    base.update(kw)
    return base


def test_grp_gates():
    print("[1] GRP 三閘語義")
    g = grp_score(_stock())
    ok(g["pass"] and g["p_label"] == "pullback", "基準樣本全過、回踩帶標籤")
    ok(not grp_score(_stock(eps_fy1_fy3_cagr_pct=14.9))["pass"], "G 14.9 < 15 → fail")
    g = grp_score(_stock(eps_fy_next_revision_pct=0.0, eps2y_revision_pp=0.0))
    ok(not g["pass"], "R 零修正＝沒有上修 → fail（>0 嚴格）")
    g = grp_score(_stock(eps_fy_next_revision_pct=-2.5, eps2y_revision_pp=3.0))
    ok(g["veto"] and not g["pass"], "FY+1 下修 -2.5% → 一票否決（2Y 正也救不回）")
    g = grp_score(_stock(eps_fy_next_revision_pct=None, eps2y_revision_pp=0.7))
    ok(g["pass"], "FY+1 缺值、2Y +0.7pp → 替代路徑過")
    g = grp_score(_stock(ma={"above_w52": False, "price": 100.0}))
    ok(not g["pass"] and g["p_label"] is None, "52 週線下 → P fail")
    ok(grp_score(_stock(timing={"dist_52w_high_pct": -3.0}))["p_label"] == "breakout",
       "距高 -3% → 突破帶")
    ok(grp_score(_stock(timing={"dist_52w_high_pct": -30.0}))["p_label"] == "in_trend",
       "距高 -30%（趨勢在但深回檔）→ 趨勢內，不給回踩帶標籤")


def test_route():
    print("[2] 軌別路由")
    ok(grp_route(_stock(moat_grade="S"))[0] == "core", "moat S → 核心")
    ok(grp_route(_stock(moat_grade="A", moat_trend="↓"))[0] == "satellite",
       "moat A 但趨勢 ↓ → 衛星（耐久性存疑）")
    ok(grp_route(_stock(moat_grade="B", moat_trend="↑"))[0] == "satellite", "moat B↑ → 衛星")
    ok(grp_route(_stock(moat_grade=None))[0] == "satellite", "moat 未知 → 衛星（保守）")


def test_cap_floor():
    print("[3] 市值門檻（≥$%dB）" % (MKTCAP_MIN / 1e9))
    ok(cap_ok(MKTCAP_MIN) is True, "剛好在門檻 → 過")
    ok(cap_ok(MKTCAP_MIN - 1) is False, "低一元 → 不過")
    ok(cap_ok(None) is None, "市值未知 → None（資格層 fail-closed）")


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
    r = cross_check_r(json.loads(json.dumps(base)), -2.5)
    ok(r["grp"]["veto"] and not r["grp"]["pass"], "yf 30d -2.5% → 保守否決（Koyfin 正也不豁免）")
    r = cross_check_r(json.loads(json.dumps(base)), -1.5)
    ok(r["grp"]["pass"] and r.get("r_conflict"), "yf -1.5%（未達否決線）→ 只標 ⚠ 源分歧不否決")
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
    ok(all(r["route"] == "satellite" for r in rows), "光卡一律衛星路由（核心席必須完整 DD）")


def test_site_consistency():
    print("[6] 站上資料一致性")
    arena = json.loads((ENG / "arena.json").read_text(encoding="utf-8"))
    cards = json.loads((ENG / "cards.json").read_text(encoding="utf-8"))
    seats = arena["core_seats"] + arena["sat_seats"]
    ok(all(r["ticker"] in cards["by_ticker"] for r in seats),
       f"每個席位都有決策卡（{len(seats)} 席）")
    ok(all(r["grp"]["pass"] for r in seats), "席位全數 GRP 三閘通過")
    ok(all(r.get("cap_ok") for r in seats if "cap_ok" in r),
       "席位全數通過市值門檻")
    ok(all(r["route"] == "core" for r in arena["core_seats"]), "核心席全為 core 路由")
    ok(all(r["route"] == "satellite" for r in arena["sat_seats"]), "衛星席全為 satellite 路由")
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
    for fn in (test_grp_gates, test_route, test_cap_floor,
               test_claim_settlement, test_dual_source_r, test_light_merge,
               test_site_consistency):
        fn()
    print(f"\nALL PASS — {N_PASS} 斷言")
