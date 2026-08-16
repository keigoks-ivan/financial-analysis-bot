#!/usr/bin/env python3
"""verify_dd_math.py — v15+ DD 機械驗算 gate（確定性重算，0 LLM token）。

動機（2026-08-08 SHOP/ANET 同尺稽核）：情境樹年期錯配、EV/IRR/AR 對帳、
Max DD 恆等式、必交模組缺章、版本戳漂移——這類錯誤 LLM critic 反覆漏抓，
但全部可由腳本確定性驗證。本 gate 與 validate_dd_meta.py 互補：後者驗
schema 形狀，本檔驗「數字之間的數學關係」。

檢查項（FAIL 擋 commit / WARN 只提示）：
  A. dd-meta 內部重算：EV5y＝機率加權（tol 1.5pp）、IRR_base＝(1+base_ret)^(1/5)−1
     （tol 1.0pp）、AR＝bull_ret/|bear_ret|（tol 0.06）、|max_dd| ≥ |bear_ret|−2pp。
  B. 情境樹年期：正文宣告「FY20XX 情境樹」必須等於情境表頭 max「FY20XX EPS」
     （FAIL）；終端年與報告年+5 差 >1 年（WARN，容忍財年錯位）。
  C. v15 必交模組存在性：§6.I／§5.F／§7.E／§3.F／§9.D 出現 0 次＝FAIL、
     僅 1 次＝WARN（疑似只有交叉引用、模組本體缺席）。
  D. 版本戳一致：dd-schema-version meta tag／topbar／頁尾 skill 版號必須等於
     dd-meta "schema"（報告端一號到底，skill 檔內部版號不外流）。

未覆蓋（由 skill 條文＋critic 把守）：upside_short/mid 與附錄 A 的對帳（附錄
為散文無機器欄）、一手財報數字 vs yfinance、PEG 分母窗口。

用法：
  python3 scripts/verify_dd_math.py docs/dd/DD_XXX_YYYYMMDD.html [...]
  python3 scripts/verify_dd_math.py --all        # 全掃 docs/dd/ 的 v15+ 檔
非 v15+ 檔（legacy v12–v14）自動跳過。任何 FAIL → exit 1。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DD_DIR = ROOT / "docs" / "dd"

EV_TOL = 1.5      # pp
IRR_TOL = 1.0     # pp
AR_TOL = 0.06
MAXDD_TOL = 2.0   # pp
# 模組存在性：§ 標號為主，中文關鍵字為 fallback（早期 v15 檔標號未統一）
MODULES = {
    "§6.I": ["分部前瞻"],
    "§5.F": ["對手損益", "對手 P&amp;L", "對手P&amp;L", "競品損益", "對手 P&L"],
    "§7.E": ["DuPont"],
    "§3.F": ["TAM／SAM", "TAM/SAM", "逐段 TAM"],
    "§9.D": ["資本配置"],
}
SP = "[  \\t]*"   # 半形/全形空白


def load_meta(html):
    m = re.search(r'<script[^>]*id="dd-meta"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def check_file(path):
    fails, warns = [], []
    html = path.read_text(encoding="utf-8")
    meta = load_meta(html)
    if meta is None:
        return None  # 無 dd-meta，不在本 gate 範圍
    schema = str(meta.get("schema", ""))
    ver = re.match(r"v(\d+)\.(\d+)", schema)
    if not ver or int(ver.group(1)) < 15:
        return None  # legacy（<v15）跳過

    # ---- A. dd-meta 內部重算 ----
    price = meta.get("price_at_dd")
    bull_p, bear_p = meta.get("bull_5y_price"), meta.get("bear_5y_price")
    p_bull, p_bear = meta.get("p_bull_pct"), meta.get("p_bear_pct")
    base_ret = meta.get("upside_5y_pct")   # Base 情境 5Y 報酬（%）
    ev, irr, ar, mdd = (meta.get(k) for k in
                        ("ev5y_pct", "irr_base_pct", "asym_ratio", "max_dd_pct"))
    have = all(v is not None for v in (price, bull_p, bear_p, p_bull, p_bear, base_ret))
    if have and price > 0:
        bull_ret = (bull_p / price - 1) * 100
        bear_ret = (bear_p / price - 1) * 100
        p_base = 100 - p_bull - p_bear
        ev_calc = (p_bull * bull_ret + p_base * base_ret + p_bear * bear_ret) / 100
        if ev is not None and abs(ev_calc - ev) > EV_TOL:
            fails.append(f"EV5y 對不上：meta {ev} vs 重算 {ev_calc:.1f}"
                         f"（{p_bull}%×{bull_ret:.1f} + {p_base}%×{base_ret:.1f}"
                         f" + {p_bear}%×{bear_ret:.1f}）")
        irr_calc = ((1 + base_ret / 100) ** 0.2 - 1) * 100
        if irr is not None and abs(irr_calc - irr) > IRR_TOL:
            fails.append(f"IRR_base 對不上：meta {irr} vs (1{base_ret:+.1f}%)^(1/5)−1"
                         f"＝{irr_calc:.1f}%/yr")
        if bear_ret < 0 and p_bear:
            # canonical（SKILL.md）：AR = (P_bull×|Bull 5Y%|)/(P_bear×|Bear 5Y%|)
            ar_calc = (p_bull * abs(bull_ret)) / (p_bear * abs(bear_ret))
            if ar is not None and abs(ar_calc - ar) > AR_TOL:
                fails.append(f"AR 對不上（canonical 機率加權口徑）：meta {ar} vs 重算 "
                             f"{ar_calc:.2f}（({p_bull}×{abs(bull_ret):.1f})/"
                             f"({p_bear}×{abs(bear_ret):.1f})）")
            if mdd is not None and abs(mdd) + MAXDD_TOL < abs(bear_ret):
                fails.append(f"Max DD 恆等式違反：|{mdd}| < |Bear 終點 {bear_ret:.1f}|"
                             f"——路徑最大回撤不可能小於任一情境終點跌幅")
    else:
        # 2026-08-08 TSM 同尺稽核：缺欄位靜默跳過會讓整組 A 驗算失效卻報 pass
        # ——v15+ 檔六個情境輸入欄一律必填，缺欄即 FAIL（fix-on-touch：只擋新增/被改的檔）
        missing = [k for k, v in (("price_at_dd", price), ("bull_5y_price", bull_p),
                                  ("bear_5y_price", bear_p), ("p_bull_pct", p_bull),
                                  ("p_bear_pct", p_bear), ("upside_5y_pct", base_ret))
                   if v is None]
        fails.append(f"dd-meta 情境欄位缺失（A 組 0 項可驗）：{', '.join(missing)}")

    # ---- B. 情境樹年期 ----
    declared = set(re.findall(rf"FY(20\d\d){SP}情境樹", html))
    eps_years = [int(y) for y in re.findall(rf"FY(20\d\d){SP}EPS", html)]
    if eps_years:
        terminal = max(eps_years)
        if declared and str(terminal) not in declared:
            fails.append(f"情境樹年期錯配：宣告 FY{'/'.join(sorted(declared))}"
                         f" 情境樹，但情境表頭終端年是 FY{terminal}")
        dd_year = int(str(meta.get("date", "0000"))[:4])
        if dd_year and abs(terminal - (dd_year + 5)) > 1:
            warns.append(f"終端年 FY{terminal} 與報告年+5（{dd_year + 5}）差 >1 年"
                         f"——確認主時距宣告與財年口徑")

    # ---- C. v15 必交模組存在性 ----
    for mod, kws in MODULES.items():
        n = html.count(mod) + sum(html.count(k) for k in kws)
        if n == 0:
            fails.append(f"必交模組 {mod} 全文 0 次出現（含關鍵字 fallback）——整章缺席")
        elif n == 1:
            warns.append(f"必交模組 {mod} 僅 1 處痕跡——疑似只有交叉引用、本體缺席")

    # ---- D. 版本戳一致 ----
    stamps = set(re.findall(r'dd-schema-version"\s+content="(v[\d.]+)"', html))
    stamps |= set(re.findall(r"DD Schema (v[\d.]+)", html))
    stamps |= set(re.findall(r"stock-analyst (v[\d.]+)", html))
    bad = {s for s in stamps if s != schema}
    if bad:
        fails.append(f"版本戳不一致：dd-meta schema={schema}，但頁面出現 {sorted(bad)}"
                     f"（報告端一號到底，skill 內部版號不外流）")

    return fails, warns


def main(argv):
    if "--all" in argv:
        targets = sorted(DD_DIR.glob("DD_*.html"))
    else:
        targets = [Path(a) for a in argv if a.endswith(".html")]
    if not targets:
        print("用法：verify_dd_math.py <DD html...> 或 --all")
        return 2
    any_fail, checked = False, 0
    for p in targets:
        if not p.exists():
            print(f"✗ {p}: 檔案不存在")
            any_fail = True
            continue
        res = check_file(p)
        if res is None:
            continue  # legacy / 無 meta
        checked += 1
        fails, warns = res
        tag = "FAIL" if fails else "pass"
        print(f"[{tag}] {p.name}")
        for f in fails:
            print(f"    ✗ {f}")
        for w in warns:
            print(f"    ⚠ {w}")
        if fails:
            any_fail = True
    print(f"—— 驗算 {checked} 檔（v15+），{'有 FAIL' if any_fail else '全數通過'}")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
