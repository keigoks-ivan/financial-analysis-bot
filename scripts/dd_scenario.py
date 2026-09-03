#!/usr/bin/env python3
"""dd_scenario.py — v15.2.1 DD 情境樹確定性計算器（0 LLM 手算，stdlib only）。

動機（2026-09-03 AVGO 首份 v15.2 實測 critic 8 🔴 中 3 條為純算術：§10.6 年期
混用／Bear EPS 未下滑致 AR 虛高／內生天花板未真算）——§10.5／§10.6／AR／10Y
的算術改由本腳本確定性產出，LLM writer 只負責填 EPS 路徑／終端倍數／機率／
基本假設（`basis`），不再手算 IRR／三分量／AR／10Y。

輸入：`.dd_build/{TICKER}_{YYYYMMDD}.scenario.json`（見 SKILL.md §10.5+10.6 引用範例）。

用法：
  python3 scripts/dd_scenario.py FILE.json                      # 終端機表格＋驗證
  python3 scripts/dd_scenario.py FILE.json --html OUT.html       # 另寫 E11 表片段
  python3 scripts/dd_scenario.py FILE.json --meta OUT.json       # 另寫 dd-meta 片段
  python3 scripts/dd_scenario.py --check docs/dd/DD_X_Y.html     # 讀既有 DD 重算比對

驗證 FAIL（任一命中 → exit 1）：
  - 終端 EPS 排序 Bear < Base < Bull 不成立
  - Bear 終端 EPS > consensus.fy2（Bear 沒有真正下滑路徑）
  - 三情境機率加總 ≠ 100
  - p_bear < 20
  - endo_ceiling_exceeded=true 且 p_bear < 30
  - p_base > 50
  - 任一 eps_path 長度 ≠ 5

驗證 WARN（只印，不擋）：
  - bull terminal_pe > peer_max_fpe
  - base 不含息 IRR > 15%（skill：罕見，須檢查機率分配是否過度樂觀）

`check_meta(meta: dict) -> (fails, warns)` 供 `verify_dd_math.py` 匯入：從
dd-meta 的 `scenario_tree`（原始情境輸入）重算，比對 dd-meta 六個情境欄
（`bull_5y_price`／`bear_5y_price`／`p_bull_pct`／`p_bear_pct`／`upside_5y_pct`／
`asym_ratio`；價格 tol 1%、% tol 1.0pp、AR tol 0.06）。ev5y_pct／irr_base_pct
的機率加權對帳已由 `verify_dd_math.py` 檢查 A 覆蓋，此處不重複。
"""
import argparse
import html as html_lib
import json
import re
import sys
from pathlib import Path

YEARS = 5
PRICE_TOL_PCT = 0.01   # 1%
PCT_TOL_PP = 1.0        # 1.0pp
AR_TOL = 0.06
GUARDRAIL_TOL_PP = 0.1  # (1+EPS)(1+re-rate)-1 vs 不含息 IRR


def cagr_pct(ratio, years=YEARS):
    """年化百分比：(ratio)^(1/years) - 1，以 % 表示。ratio 須為正數。"""
    if ratio is None or ratio <= 0:
        raise ValueError(f"CAGR 基期比率須為正數，得到 {ratio!r}")
    return (ratio ** (1.0 / years) - 1.0) * 100.0


def compute_one(price, start, yield_pct, key, s):
    eps_path = s["eps_path"]
    if not eps_path:
        raise ValueError(f"{key} eps_path 為空")
    terminal_eps = eps_path[-1]
    terminal_pe = s["terminal_pe"]
    p = s["p"]
    terminal_price = terminal_eps * terminal_pe
    five_y_pct = (terminal_price / price - 1.0) * 100.0
    irr_ex_div = cagr_pct(1.0 + five_y_pct / 100.0)
    eps_contrib = cagr_pct(terminal_eps / start["eps"])
    rerate_contrib = cagr_pct(terminal_pe / start["pe"])
    yield_total = (yield_pct or {}).get("dividend", 0.0) + (yield_pct or {}).get("net_buyback", 0.0)
    ex_div_total = ((1.0 + eps_contrib / 100.0) * (1.0 + rerate_contrib / 100.0) - 1.0) * 100.0
    incl_div_total = ex_div_total + yield_total
    return {
        "key": key,
        "eps_path": eps_path,
        "terminal_eps": terminal_eps,
        "terminal_pe": terminal_pe,
        "terminal_price": terminal_price,
        "five_y_pct": five_y_pct,
        "irr_ex_div": irr_ex_div,
        "eps_contrib": eps_contrib,
        "rerate_contrib": rerate_contrib,
        "yield_total": yield_total,
        "ex_div_total": ex_div_total,
        "incl_div_total": incl_div_total,
        "p": p,
        "basis": s.get("basis", ""),
    }


def compute(data):
    price = data["price"]
    start = data["start"]
    yield_pct = data.get("yield_pct", {"dividend": 0.0, "net_buyback": 0.0})
    scen = data["scenarios"]
    rows = {k: compute_one(price, start, yield_pct, k, scen[k]) for k in ("bull", "base", "bear")}

    p_bull, p_base, p_bear = rows["bull"]["p"], rows["base"]["p"], rows["bear"]["p"]
    ev5y = (p_bull * rows["bull"]["five_y_pct"]
            + p_base * rows["base"]["five_y_pct"]
            + p_bear * rows["bear"]["five_y_pct"]) / 100.0
    ev_annualized = cagr_pct(1.0 + ev5y / 100.0)

    bear_5y = rows["bear"]["five_y_pct"]
    if bear_5y >= 0 or not p_bear:
        ar = None
    else:
        ar = (p_bull * abs(rows["bull"]["five_y_pct"])) / (p_bear * abs(bear_5y))

    ten_y = {}
    ss = data.get("second_stage")
    if ss:
        for k in ("bull", "base"):
            g = ss.get(f"{k}_cagr_pct")
            if g is None:
                continue
            terminal_eps = rows[k]["terminal_eps"]
            terminal_pe = rows[k]["terminal_pe"]
            eps10 = terminal_eps * (1.0 + g / 100.0) ** 5
            price10 = eps10 * terminal_pe
            multiple10 = price10 / price
            irr10 = cagr_pct(multiple10, years=10)
            ten_y[k] = {
                "g_pct": g, "eps10": eps10, "price10": price10,
                "multiple10": multiple10, "irr10_pct": irr10,
            }

    base_row = rows["base"]
    val_dep = False
    if base_row["ex_div_total"]:
        ratio = base_row["rerate_contrib"] / base_row["ex_div_total"]
        if ratio >= 0.40:
            val_dep = True

    guardrail_diff = abs(base_row["ex_div_total"] - base_row["irr_ex_div"])

    return {
        "rows": rows,
        "ev5y_pct": ev5y,
        "ev_annualized_pct": ev_annualized,
        "ar": ar,
        "ten_y": ten_y,
        "valuation_dependent": val_dep,
        "guardrail_diff_pp": guardrail_diff,
    }


def validate(data, result):
    fails, warns = [], []
    rows = result["rows"]
    bull, base, bear = rows["bull"], rows["base"], rows["bear"]
    scen = data["scenarios"]
    consensus = data.get("consensus", {})

    if not (bear["terminal_eps"] < base["terminal_eps"] < bull["terminal_eps"]):
        fails.append(
            f"終端 EPS 排序不成立（須 Bear<Base<Bull）：Bear {bear['terminal_eps']} / "
            f"Base {base['terminal_eps']} / Bull {bull['terminal_eps']}"
        )

    fy2 = consensus.get("fy2")
    if fy2 is not None and bear["terminal_eps"] > fy2:
        fails.append(
            f"Bear 終端 EPS {bear['terminal_eps']} > consensus.fy2 {fy2}"
            f"——Bear 沒有真正下滑路徑"
        )

    p_sum = bull["p"] + base["p"] + bear["p"]
    if p_sum != 100:
        fails.append(f"三情境機率加總 {p_sum} ≠ 100")

    if bear["p"] < 20:
        fails.append(f"p_bear {bear['p']} < 20")

    if data.get("endo_ceiling_exceeded") and bear["p"] < 30:
        fails.append(f"endo_ceiling_exceeded=true 但 p_bear {bear['p']} < 30")

    if base["p"] > 50:
        fails.append(f"p_base {base['p']} > 50")

    for k in ("bull", "base", "bear"):
        n = len(scen[k]["eps_path"])
        if n != 5:
            fails.append(f"{k} eps_path 長度 {n} ≠ 5")

    peer_max = data.get("peer_max_fpe")
    if peer_max is not None and bull["terminal_pe"] > peer_max:
        warns.append(f"bull terminal_pe {bull['terminal_pe']} > peer_max_fpe {peer_max}")

    if base["irr_ex_div"] > 15:
        warns.append(
            f"base 不含息 IRR {base['irr_ex_div']:.1f}%/yr > 15%"
            f"——罕見，須檢查機率分配是否過度樂觀"
        )

    return fails, warns


# ---------------------------------------------------------------------------
# 呈現層
# ---------------------------------------------------------------------------

def _fmt_price(x):
    return f"{x:,.1f}"


def _fmt_pct(x, suffix=""):
    return f"{x:+.1f}%{suffix}"


def print_table(data, result):
    price = data["price"]
    start = data["start"]
    rows = result["rows"]
    print(f"{data.get('ticker', '?')} 情境樹（{data.get('date', '?')}，現價 {_fmt_price(price)}，"
          f"起始 {start.get('eps_label', '')} EPS {start['eps']:.2f} @ {start['pe']:.2f}x，"
          f"終端年 {data.get('terminal_label', '')}）")
    print("-" * 100)
    for k in ("bull", "base", "bear"):
        r = rows[k]
        print(f"[{k.upper():5}] 終端EPS={r['terminal_eps']:.2f}  終端倍數={r['terminal_pe']:.1f}x  "
              f"5Y目標價={_fmt_price(r['terminal_price'])}  5Y%={_fmt_pct(r['five_y_pct'])}  "
              f"不含息IRR={_fmt_pct(r['irr_ex_div'], '/yr')}  機率={r['p']}%")
        print(f"         EPS貢獻={_fmt_pct(r['eps_contrib'], '/yr')}  "
              f"re-rate={_fmt_pct(r['rerate_contrib'], '/yr')}  "
              f"股息回購={_fmt_pct(r['yield_total'], '/yr')}  "
              f"不含息合計={_fmt_pct(r['ex_div_total'], '/yr')}  "
              f"含息合計={_fmt_pct(r['incl_div_total'], '/yr')}")
        if r.get("basis"):
            print(f"         依據：{r['basis']}")
    print("-" * 100)
    ar_str = f"{result['ar']:.1f}" if result["ar"] is not None else "N/A（Bear 5Y%≥0）"
    print(f"機率加權：EV5y={_fmt_pct(result['ev5y_pct'])}  年化={_fmt_pct(result['ev_annualized_pct'], '/yr')}  AR={ar_str}")
    print(f"估值依賴型：{'是（re-rate≥Base不含息合計40%）' if result['valuation_dependent'] else '否'}")
    print(f"Guardrail 自洽差：{result['guardrail_diff_pp']:.2f}pp（(1+EPS)(1+re-rate)-1 vs 不含息IRR，≤0.1pp 為自洽）")
    if result["ten_y"]:
        print("-" * 100)
        print("10Y 二段延伸：")
        for k in ("bull", "base"):
            t = result["ten_y"].get(k)
            if not t:
                continue
            print(f"[{k.upper():5}] 第二段CAGR={t['g_pct']:.1f}%  EPS10={t['eps10']:.2f}  "
                  f"10Y倍數={t['multiple10']:.2f}x  10Y IRR={_fmt_pct(t['irr10_pct'], '/yr')}")


def print_validation(fails, warns):
    print("-" * 100)
    if not fails and not warns:
        print("驗證：全數通過")
        return
    for f in fails:
        print(f"✗ FAIL：{f}")
    for w in warns:
        print(f"⚠ WARN：{w}")


def build_html(data, result):
    rows = result["rows"]
    terminal_label = html_lib.escape(str(data.get("terminal_label", "")))
    lines = ['<div class="sec-irr">', "<table>", (
        "<tr><th>情境</th><th>終端 EPS</th><th>終端倍數</th><th>5Y 目標價</th>"
        "<th>5Y%</th><th>不含息 IRR</th><th>EPS 貢獻</th><th>re-rate</th>"
        "<th>股息回購</th><th>含息合計</th><th>機率</th><th>依據</th></tr>"
    )]
    for k, label in (("bull", "Bull"), ("base", "Base"), ("bear", "Bear")):
        r = rows[k]
        basis = html_lib.escape(str(r.get("basis", "")))
        lines.append(
            "<tr><td>{label}</td><td>{eps:.2f}（{term}）</td><td>{pe:.1f}x</td>"
            "<td>{price}</td><td>{p5y}</td><td>{irr}</td><td>{eps_c}</td>"
            "<td>{rr}</td><td>{yld}</td><td>{incl}</td><td>{p}%</td><td>{basis}</td></tr>".format(
                label=label, eps=r["terminal_eps"], term=terminal_label,
                pe=r["terminal_pe"], price=_fmt_price(r["terminal_price"]),
                p5y=_fmt_pct(r["five_y_pct"]), irr=_fmt_pct(r["irr_ex_div"], "/yr"),
                eps_c=_fmt_pct(r["eps_contrib"], "/yr"), rr=_fmt_pct(r["rerate_contrib"], "/yr"),
                yld=_fmt_pct(r["yield_total"], "/yr"), incl=_fmt_pct(r["incl_div_total"], "/yr"),
                p=r["p"], basis=basis,
            )
        )
    ar_str = f"{result['ar']:.1f}" if result["ar"] is not None else "N/A"
    lines.append(
        "<tr><td><strong>機率加權</strong></td><td></td><td></td><td></td>"
        "<td><strong>EV {ev}</strong></td><td><strong>{ann}</strong></td>"
        "<td></td><td></td><td></td><td></td><td>100%</td>"
        "<td>AR={ar}</td></tr>".format(
            ev=_fmt_pct(result["ev5y_pct"]), ann=_fmt_pct(result["ev_annualized_pct"], "/yr"), ar=ar_str,
        )
    )
    lines.append("</table>")
    if result["ten_y"]:
        lines.append("<table>")
        lines.append("<tr><th>情境（10Y）</th><th>第二段 CAGR</th><th>EPS10</th><th>10Y 倍數</th><th>10Y IRR</th></tr>")
        for k, label in (("bull", "Bull"), ("base", "Base")):
            t = result["ten_y"].get(k)
            if not t:
                continue
            lines.append(
                "<tr><td>{label}</td><td>{g:.1f}%/yr</td><td>{eps10:.2f}</td>"
                "<td>{mult:.2f}x</td><td>{irr}</td></tr>".format(
                    label=label, g=t["g_pct"], eps10=t["eps10"], mult=t["multiple10"],
                    irr=_fmt_pct(t["irr10_pct"], "/yr"),
                )
            )
        lines.append("</table>")
    lines.append("</div>")
    return "\n".join(lines) + "\n"


def _round1(x):
    return None if x is None else round(x, 1)


def build_meta(data, result):
    rows = result["rows"]
    scenario_tree = {
        "terminal_label": data.get("terminal_label"),
        "start": data["start"],
        "eps": {k: rows[k]["eps_path"] for k in ("bull", "base", "bear")},
        "pe": {k: rows[k]["terminal_pe"] for k in ("bull", "base", "bear")},
        "p": {k: rows[k]["p"] for k in ("bull", "base", "bear")},
        "yield_pct": data.get("yield_pct", {"dividend": 0.0, "net_buyback": 0.0}),
        "second_stage": data.get("second_stage"),
        "valuation_dependent": result["valuation_dependent"],
    }
    meta = {
        "bull_5y_price": _round1(rows["bull"]["terminal_price"]),
        "bear_5y_price": _round1(rows["bear"]["terminal_price"]),
        "p_bull_pct": _round1(rows["bull"]["p"]),
        "p_bear_pct": _round1(rows["bear"]["p"]),
        "upside_5y_pct": _round1(rows["base"]["five_y_pct"]),
        "ev5y_pct": _round1(result["ev5y_pct"]),
        "irr_base_pct": _round1(rows["base"]["irr_ex_div"]),
        "asym_ratio": _round1(result["ar"]) if result["ar"] is not None else None,
        "scenario_tree": scenario_tree,
    }
    return meta


# ---------------------------------------------------------------------------
# --check：讀既有 DD html 的 dd-meta，重算 scenario_tree 比對六欄
# ---------------------------------------------------------------------------

def _load_meta_from_html(html_text):
    m = re.search(r'<script[^>]*id="dd-meta"[^>]*>(.*?)</script>', html_text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def check_meta(meta):
    """從 dd-meta 的 scenario_tree 重算，比對 dd-meta 六個情境欄。

    回傳 (fails, warns)；供 verify_dd_math.py 匯入串接。
    """
    fails, warns = [], []
    st = meta.get("scenario_tree")
    if not st:
        warns.append("dd-meta 缺 scenario_tree，無法重算比對（v15.2.1 起建議由 dd_scenario.py 產出）")
        return fails, warns

    price = meta.get("price_at_dd")
    if price is None:
        fails.append("dd-meta 缺 price_at_dd，無法重算 scenario_tree")
        return fails, warns

    try:
        rebuilt = {
            "price": price,
            "start": st["start"],
            "terminal_label": st.get("terminal_label"),
            "yield_pct": st.get("yield_pct", {"dividend": 0.0, "net_buyback": 0.0}),
            "scenarios": {
                k: {
                    "eps_path": st["eps"][k],
                    "terminal_pe": st["pe"][k],
                    "p": st["p"][k],
                }
                for k in ("bull", "base", "bear")
            },
        }
        if st.get("second_stage"):
            rebuilt["second_stage"] = st["second_stage"]
        result = compute(rebuilt)
    except Exception as e:  # noqa: BLE001 — 任何重算失敗都直接回報為 FAIL
        fails.append(f"scenario_tree 重算失敗：{e}")
        return fails, warns

    rows = result["rows"]
    checks = [
        ("bull_5y_price", rows["bull"]["terminal_price"], "price"),
        ("bear_5y_price", rows["bear"]["terminal_price"], "price"),
        ("p_bull_pct", rows["bull"]["p"], "pct"),
        ("p_bear_pct", rows["bear"]["p"], "pct"),
        ("upside_5y_pct", rows["base"]["five_y_pct"], "pct"),
        ("asym_ratio", result["ar"], "ar"),
    ]
    for key, calc, kind in checks:
        meta_val = meta.get(key)
        if calc is None:
            if meta_val is not None:
                fails.append(f"{key}：重算為 N/A（Bear 5Y%≥0）但 dd-meta 仍有值 {meta_val}——應省略此欄")
            continue
        if meta_val is None:
            warns.append(f"{key}：dd-meta 缺此欄，無法比對（重算值 {calc:.2f}）")
            continue
        if kind == "price":
            tol = max(abs(calc), abs(meta_val), 1e-9) * PRICE_TOL_PCT
            if abs(calc - meta_val) > tol:
                fails.append(f"{key} 對不上：dd-meta {meta_val} vs 重算 {calc:.1f}（tol 1%）")
        elif kind == "pct":
            if abs(calc - meta_val) > PCT_TOL_PP:
                fails.append(f"{key} 對不上：dd-meta {meta_val} vs 重算 {calc:.1f}（tol {PCT_TOL_PP}pp）")
        elif kind == "ar":
            if abs(calc - meta_val) > AR_TOL:
                fails.append(f"{key} 對不上：dd-meta {meta_val} vs 重算 {calc:.2f}（tol {AR_TOL}）")

    return fails, warns


def cmd_check(html_path):
    p = Path(html_path)
    if not p.exists():
        print(f"✗ {p}: 檔案不存在")
        return 1
    meta = _load_meta_from_html(p.read_text(encoding="utf-8"))
    if meta is None:
        print(f"✗ {p}: 找不到或無法解析 dd-meta")
        return 1
    fails, warns = check_meta(meta)
    tag = "FAIL" if fails else "pass"
    print(f"[{tag}] {p.name} scenario_tree 對帳")
    for f in fails:
        print(f"    ✗ {f}")
    for w in warns:
        print(f"    ⚠ {w}")
    if not fails and not warns:
        print("    全數通過")
    return 1 if fails else 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(description="v15.2.1 DD 情境樹確定性計算器")
    parser.add_argument("json_file", nargs="?", help="情境輸入 json 路徑")
    parser.add_argument("--html", metavar="OUT", help="寫 E11 表 HTML 片段")
    parser.add_argument("--meta", metavar="OUT", help="寫 dd-meta 情境欄 JSON 片段")
    parser.add_argument("--check", metavar="DD_HTML", help="讀既有 DD html 的 dd-meta，重算比對 scenario_tree")
    args = parser.parse_args(argv)

    if args.check:
        return cmd_check(args.check)

    if not args.json_file:
        parser.error("需要情境輸入 json 路徑（或改用 --check DD_HTML）")

    data = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    result = compute(data)
    fails, warns = validate(data, result)

    print_table(data, result)
    print_validation(fails, warns)

    if args.html:
        Path(args.html).write_text(build_html(data, result), encoding="utf-8")
        print(f"已寫 {args.html}")
    if args.meta:
        Path(args.meta).write_text(
            json.dumps(build_meta(data, result), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"已寫 {args.meta}")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
