"""Render docs/backtest/revmom/index.html in financial-analysis-bot from results/revmom/.

Usage:  ~/.venvs/v7bt/bin/python -m src.revmom_backtest.generate_page [output_path]
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_env as SE  # noqa: E402  (local v7-backtest vs. cloud copy in the site repo)

_kit = SE.site_kit()
section_exposure, section_monthly_dist, section_rolling12 = (_kit.section_exposure, _kit.section_monthly_dist,
                                                             _kit.section_rolling12)
ROOT = SE.ROOT
RES = ROOT / "results" / "revmom"
DEFAULT_OUTPUT = SE.SITE / "docs" / "backtest" / "revmom" / "index.html"
BRAND, GREY = "#1a56db", "#6b7280"


def pct(x, nd=1, sign=False):
    if x is None:
        return "—"
    return (f"{x * 100:+.{nd}f}%" if sign else f"{x * 100:.{nd}f}%").replace("-", "−")


def colored(x, nd=1):
    c = "var(--green)" if x > 0 else "var(--red)" if x < 0 else "inherit"
    return f'<td style="color:{c}">{pct(x, nd, sign=True)}</td>'


def row(label, s, hl=False):
    style = ' style="background:var(--brand-light)"' if hl else ""
    return (f'<tr{style}><td>{label}</td><td>{pct(s["cagr"])}</td><td style="color:var(--red)">{pct(s["mdd"])}</td>'
            f'<td>{s["sharpe"]:.2f}</td><td>{(s["sortino"] or 0):.2f}</td><td>{(s["calmar"] or 0):.2f}</td>'
            f'<td>{pct(s["month_win"], 0)}</td></tr>')


def main(out=DEFAULT_OUTPUT):
    full_nav_block, make_toggle = SE.full_nav_block, SE.make_toggle

    R = json.loads((RES / "results.json").read_text())
    V = json.loads((RES / "verify.json").read_text())
    C = R["cases"]
    a, b = C["V1a_base"], C["bench_0050"]
    daily = pd.read_csv(RES / "V1a_base_daily.csv.gz", parse_dates=["date"], index_col="date")
    bench = pd.read_csv(RES / "bench_0050_daily.csv.gz", parse_dates=["date"], index_col="date")
    eq, beq = daily.nav, bench.nav
    rep, trials = SE.ledger("REVMOM")
    t1 = trials["REVMOM-001"]
    best_name = {t["exp_id"]: t["reason"].split("：")[-1] for t in trials.values()}[rep["best"]["exp_id"]]
    sl = R["slice_2009_2014"]
    oos, boos = a["periods"]["oos_2008_2014"], b["periods"]["oos_2008_2014"]

    # ---- tables
    summary_rows = (row("月營收動能（營收比值排序，主要版本）", a["full"], hl=True)
                    + row("股價排序（同條件，改依 60 日漲幅）", C["V1b_base"]["full"])
                    + row("只看營收年增率", C["V2_base"]["full"])
                    + row("0050（含股利，買進持有）", b["full"])
                    + row("加權股價報酬指數（2009 起）", C["bench_taiex_tr_2009"]["full"]))
    plabel = {"oos_2008_2014": "2008–2014（規則沒用過）", "is_2015_2025": "2015–2025（FinLab 設計期間）",
              "post_finlab": "2026-01-12 起（FinLab 發表後，年化）"}
    period_rows = "".join(
        f'<tr><td>{plabel[k]}</td><td>{pct(a["periods"][k]["cagr"])}</td><td style="color:var(--red)">{pct(a["periods"][k]["mdd"])}</td>'
        f'<td>{a["periods"][k]["calmar"]:.2f}</td><td>{pct(b["periods"][k]["cagr"])}</td>'
        f'<td style="color:var(--red)">{pct(b["periods"][k]["mdd"])}</td><td>{b["periods"][k]["calmar"]:.2f}</td></tr>'
        for k in plabel)
    period_rows += (f'<tr><td>2009–2014（去掉 2008 年）</td><td>{pct(sl["V1a"]["cagr"])}</td><td style="color:var(--red)">{pct(sl["V1a"]["mdd"])}</td>'
                    f'<td>{sl["V1a"]["calmar"]:.2f}</td><td>{pct(sl["0050"]["cagr"])}</td><td style="color:var(--red)">{pct(sl["0050"]["mdd"])}</td>'
                    f'<td>{sl["0050"]["calmar"]:.2f}</td></tr>')
    years = list(a["yearly"])
    yearly_rows = "".join(f"<tr><td>{y}{'（1–9 月）' if y == years[-1] else ''}</td>{colored(a['yearly'][y])}"
                          f"{colored(b['yearly'][y])}{colored(a['yearly'][y] - b['yearly'][y])}</tr>" for y in years)
    wins = sum(a["yearly"][y] > b["yearly"][y] for y in years)
    stress_rows, better, worse = "", [], []
    for k in a["stress"]:
        s1, s2 = a["stress"][k], b["stress"][k]
        d = s1 - s2
        (better if d >= 0.02 else worse if d <= -0.02 else []).append(k)
        tag = "tag-best" if d >= 0.02 else "tag-fail" if d <= -0.02 else "tag-pass"
        p0, p1 = R["stress_windows"][k]
        stress_rows += (f'<tr><td>{k}<br><span style="color:var(--muted);font-size:.78rem">{p0} → {p1}</span></td>'
                        f'<td>{pct(s1, sign=True)}</td><td>{pct(s2, sign=True)}</td>'
                        f'<td><span class="tag {tag}">{f"{d * 100:+.1f}".replace("-", "−")} 個百分點</span></td></tr>')
    diffs = {k: a["stress"][k] - b["stress"][k] for k in a["stress"]}
    kb, kw = max(diffs, key=diffs.get), min(diffs, key=diffs.get)
    stress_note = (f"{len(a['stress'])} 次事件裡，{len(better)} 次跌得比 0050 少（{'、'.join(better)}），"
                   f"{len(worse)} 次跌得更多（{'、'.join(worse)}），其餘差不多。差最多的兩次："
                   f"{kb} 策略 {pct(a['stress'][kb], sign=True)}、0050 {pct(b['stress'][kb], sign=True)}；"
                   f"{kw} 策略 {pct(a['stress'][kw], sign=True)}、0050 {pct(b['stress'][kw], sign=True)}。")
    cost_lab = [("zero", "零成本"), ("slip0", "手續費 0.1425%×0.3＋證交稅 0.3%，滑價 0"),
                ("base", "同上，滑價 10 bp（主要結果）"), ("slip30", "同上，滑價 30 bp"),
                ("fullfee_slip30", "手續費不打折＋證交稅 0.3%＋滑價 30 bp")]
    cost_rows = "".join(row(l, (a if k == "base" else C[f"V1a_{k}"])["full"], hl=(k == "base")) for k, l in cost_lab)
    sens_lab = [("V1a_base", "原設定：前 10 檔、流動性 1,000 萬、截止日隔天換股", None),
                ("sens_n5", "只取前 5 檔", "事前"), ("sens_n20", "取前 20 檔", "事前"),
                ("sens_liq5m", "流動性門檻 500 萬", "事前"), ("sens_liq30m", "流動性門檻 3,000 萬", "事前"),
                ("sens_day15", "15 日後換股", "事前"), ("sens_notech", "拿掉股價條件", "事前"),
                ("sens_delay1", "比原規則晚 1 個交易日", "事後"), ("sens_day12", "12 日後換股", "事後"),
                ("sens_day13", "13 日後換股", "事後")]
    sens_rows = ""
    for k, l, tag in sens_lab:
        s = C[k]["full"]
        chip = ("—" if tag is None else '<span class="tag tag-pass">事前寫好</span>' if tag == "事前"
                else '<span class="tag tag-fail">看完結果才加</span>')
        style = ' style="background:var(--brand-light)"' if tag is None else ""
        sens_rows += (f'<tr{style}><td>{l}</td><td>{chip}</td><td>{pct(s["cagr"])}</td>'
                      f'<td style="color:var(--red)">{pct(s["mdd"])}</td><td>{(s["calmar"] or 0):.2f}</td></tr>')

    # ---- charts (monthly)
    m = eq.resample("ME").last()
    mb = beq.reindex(eq.index).ffill().resample("ME").last()
    lbl = [d.strftime("%Y-%m") for d in m.index]
    dd = (eq / eq.cummax() - 1).resample("ME").min()
    ddb = (beq / beq.cummax() - 1).reindex(eq.index).ffill().resample("ME").min()
    kit = [section_monthly_dist([("月營收動能", BRAND, eq), ("0050", GREY, beq)]),
           section_rolling12([("月營收動能", BRAND, eq), ("0050", GREY, beq)]),
           section_exposure([("月營收動能", BRAND, daily.exposure)], title="持股比例",
                            sub="月底持股占淨值的比例（1＝全部持股，0＝全部現金）。通過條件的股票不足 10 檔時留現金。")]

    cap = V["capacity_ntd_10pct_rule_p10"]
    inc = C["V1a_incl_innovation"]
    d11 = C["V1a_signal_day11"]
    removed = R["innovation_removed_list"]
    rm_years = sorted({d[:4] for d, _ in removed})
    n_saw = sum(1 for t in trials.values() if t["saw_oos_before_change"])
    n_human = sum(1 for t in trials.values() if t["proposed_by"] == "human")
    rp = {
        "%SITE_NAV%": full_nav_block("system", "bt"), "%TOGGLE%": make_toggle("revmom"),
        "%END%": R["end"], "%NOW%": datetime.now().strftime("%Y-%m-%d"),
        "%CAGR%": pct(a["full"]["cagr"]), "%MDD%": pct(a["full"]["mdd"]), "%CALMAR%": f'{a["full"]["calmar"]:.2f}',
        "%B_CAGR%": pct(b["full"]["cagr"]), "%B_MDD%": pct(b["full"]["mdd"]), "%B_CALMAR%": f'{b["full"]["calmar"]:.2f}',
        "%OOS%": pct(oos["cagr"]), "%OOS_MDD%": pct(oos["mdd"]), "%OOS_CAL%": f'{oos["calmar"]:.2f}',
        "%B_OOS%": pct(boos["cagr"]), "%B_OOS_MDD%": pct(boos["mdd"]), "%B_OOS_CAL%": f'{boos["calmar"]:.2f}',
        "%Y08%": pct(a["yearly"]["2008"], sign=True), "%B_Y08%": pct(b["yearly"]["2008"], sign=True),
        "%S09%": pct(sl["V1a"]["cagr"]), "%S09_CAL%": f'{sl["V1a"]["calmar"]:.2f}',
        "%S09_WORD%": ("略高" if sl["V1a"]["calmar"] - sl["taiex_tr"]["calmar"] > 0.02 else
                       "略低" if sl["taiex_tr"]["calmar"] - sl["V1a"]["calmar"] > 0.02 else "差不多"),
        "%T09%": pct(sl["taiex_tr"]["cagr"]), "%T09_CAL%": f'{sl["taiex_tr"]["calmar"]:.2f}',
        "%POST%": pct(a["periods"]["post_finlab"]["cagr"]), "%B_POST%": pct(b["periods"]["post_finlab"]["cagr"]),
        "%DELAY1%": pct(C["sens_delay1"]["full"]["cagr"]), "%DAY13%": pct(C["sens_day13"]["full"]["cagr"]),
        "%NOTECH%": pct(C["sens_notech"]["full"]["cagr"]), "%N5%": pct(C["sens_n5"]["full"]["cagr"]),
        "%STRESS30%": pct(C["V1a_fullfee_slip30"]["full"]["cagr"]), "%ZERO%": pct(C["V1a_zero"]["full"]["cagr"]),
        "%TURN%": f'{a["turnover_ann"]:.0f}', "%CORR%": f'{R["corr_0050_monthly"]:.2f}',
        "%WINS%": str(wins), "%NY%": str(len(years)), "%PASS%": f'{a["avg_pass"]:.0f}',
        "%EXPO%": pct(a["avg_exposure"], 0), "%CAP%": f"{cap / 1e4:,.0f} 萬",
        "%V1B_OOS%": pct(C["V1b_base"]["periods"]["oos_2008_2014"]["cagr"]), "%V1B_MDD%": pct(C["V1b_base"]["full"]["mdd"]),
        "%V1B_POST%": pct(C["V1b_base"]["periods"]["post_finlab"]["cagr"]),
        "%NT%": str(rep["n_trials"]), "%NPOST%": str(n_saw), "%NHUMAN%": str(n_human),
        "%INC_CAGR%": pct(inc["full"]["cagr"]), "%INC_POST%": pct(inc["periods"]["post_finlab"]["cagr"]),
        "%NREM%": str(len(removed)), "%REM_YEARS%": "、".join(rm_years),
        "%D11_CAGR%": pct(d11["full"]["cagr"]), "%D11_OOS%": pct(d11["periods"]["oos_2008_2014"]["cagr"]),
        "%NSHIFT%": str(R["deadline_shift_months"]),
        "%BEST%": best_name, "%BEST_IS%": f'{rep["best"]["is_sharpe_ann"]:.2f}',
        "%LUCK%": f'{rep["best"]["luck_threshold_sharpe_ann"]:.2f}', "%DSR%": pct(rep["best"]["dsr"], 1),
        "%V1A_IS%": f'{t1["is"]["sharpe_ann"]:.2f}', "%V1A_OOS%": f'{t1["oos"]["sharpe_ann"]:.2f}',
        "%XCHK%": f'{V["research_crosscheck"]["site_engine"]["cagr"] * 100:.2f}%',
        "%PEND%": str(V["pending_order_days"]),
        "%SUMMARY_ROWS%": summary_rows, "%PERIOD_ROWS%": period_rows, "%YEARLY_ROWS%": yearly_rows,
        "%STRESS_ROWS%": stress_rows, "%STRESS_NOTE%": stress_note, "%COST_ROWS%": cost_rows, "%SENS_ROWS%": sens_rows,
        "%KIT_HTML%": "\n".join(k["html"] for k in kit), "%KIT_JS%": "\n".join(k["js"] for k in kit),
        "%JS_LBL%": json.dumps(lbl), "%JS_NAV%": json.dumps([round(float(v), 4) for v in m]),
        "%JS_NAV_B%": json.dumps([round(float(v), 4) for v in mb]),
        "%JS_DD%": json.dumps([round(float(v) * 100, 2) for v in dd]),
        "%JS_DD_B%": json.dumps([round(float(v) * 100, 2) for v in ddb]),
        "%JS_YEARS%": json.dumps(years), "%JS_RET%": json.dumps([round(a["yearly"][y] * 100, 1) for y in years]),
        "%JS_RET_B%": json.dumps([round(b["yearly"][y] * 100, 1) for y in years]),
    }
    html = TEMPLATE
    for k, v in rp.items():
        html = html.replace(k, v)
    assert "%" not in "".join(t for t in __import__("re").findall(r"%[A-Z_0-9]+%", html)), "unfilled placeholder"
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out, len(html))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>月營收動能選股回測 | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;
      --text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--red-text:#991b1b;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang TC','Noto Sans TC',sans-serif;
     background:var(--bg);color:var(--text);line-height:1.7;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.75rem 0 1.25rem;background:linear-gradient(180deg,#eff6ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.6rem;font-weight:700;letter-spacing:-.02em;color:var(--brand)}
.page-hdr .sub{color:var(--muted);font-size:.9rem;margin-top:.2rem}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}
.crumb a{color:var(--muted)}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.15rem;font-weight:700;margin-bottom:1rem;padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.section-sub{font-size:.88rem;color:var(--muted);margin:-.5rem 0 1rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem;overflow-x:auto}
.card h3{font-size:1rem;font-weight:600;margin-bottom:.85rem}
.card .takeaway{font-size:.9rem;margin-top:.75rem;padding:.6rem .9rem;border-radius:6px;background:var(--brand-light);border-left:3px solid var(--brand)}
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{text-align:left;padding:.6rem .75rem;border-bottom:1px solid var(--border)}
th{background:#f9fafb;font-weight:600;font-size:.78rem;letter-spacing:.03em;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
tbody tr:hover td{background:#f3f4f6}
.hero{margin:1.25rem 0;border:1px solid #bfdbfe;border-radius:12px;overflow:hidden;background:var(--card)}
.hero-top{background:linear-gradient(135deg,#eff6ff 0%,#f8fafc 100%);padding:1.4rem 1.6rem;border-bottom:1px solid #bfdbfe}
.hero-top .verdict-tag{display:inline-block;background:var(--brand);color:#fff;font-size:.74rem;font-weight:700;letter-spacing:.05em;padding:.25rem .7rem;border-radius:99px;margin-bottom:.5rem}
.hero-top h2{font-size:1.35rem;font-weight:800;letter-spacing:-.01em;margin-bottom:.5rem}
.hero-top p{font-size:.93rem;color:#374151;max-width:62rem;margin-bottom:.5rem}
.hero-stats{display:grid;grid-template-columns:repeat(4,1fr);background:var(--card)}
.hero-stats > div{padding:1rem 1.2rem;text-align:center;border-right:1px solid var(--border)}
.hero-stats > div:last-child{border-right:none}
.hero-stats .hs-label{font-size:.74rem;color:var(--muted);letter-spacing:.03em}
.hero-stats .hs-value{font-size:1.55rem;font-weight:800;letter-spacing:-.02em}
.hero-stats .hs-sub{font-size:.76rem;color:var(--muted)}
.note{background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px;padding:.85rem 1.1rem;font-size:.86rem;color:var(--amber-text);margin:1rem 0}
.tag{display:inline-block;padding:.15rem .55rem;border-radius:4px;font-size:.72rem;font-weight:600;white-space:nowrap}
.tag-best{background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)}
.tag-fail{background:var(--red-bg);color:var(--red-text);border:1px solid var(--red-border)}
.tag-pass{background:#f3f4f6;color:#374151;border:1px solid #d1d5db}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.chart-card h3{font-size:.95rem;font-weight:600;margin-bottom:.5rem}
.chart-wrap{position:relative;width:100%;height:380px}
.chart-wrap-sm{position:relative;width:100%;height:220px}
details{background:var(--card);border:1px solid var(--border);border-radius:8px;margin-bottom:.75rem}
details summary{padding:.9rem 1.25rem;font-weight:600;font-size:.95rem;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.5rem}
details summary::before{content:'▸';color:var(--brand);transition:transform .15s}
details[open] summary::before{transform:rotate(90deg)}
details .d-body{padding:0 1.25rem 1.25rem;font-size:.9rem;color:#374151}
.issue-list{font-size:.9rem;color:#374151;padding-left:1.2rem;line-height:1.9}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.25rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){.hero-stats{grid-template-columns:repeat(2,1fr)}.hero-stats > div{border-bottom:1px solid var(--border)}table{font-size:.78rem}th,td{padding:.45rem .5rem}}
</style>
</head>
<body>
%SITE_NAV%
%TOGGLE%

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / 月營收動能選股</div>
    <h1>月營收動能選股（FinLab 規則）</h1>
    <div class="sub">台股上市櫃普通股（不含創新板）· 每月營收截止日隔天換股、持有 10 檔 · 2008-01 ~ %END% · 證交所、櫃買、公開資訊觀測站官方資料</div>
  </div>
</div>

<div class="container">

<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag">值得繼續驗證</span>
    <h2>規則沒用過的七年仍贏 0050，領先多半來自 2008 年少跌</h2>
    <p>規則由 FinLab 公開：每月挑營收加溫、股價也走強的 10 檔股票。FinLab 用 2015 年以後的資料設計這套規則，所以 2015 年以後的成績不能拿來證明它有效。我們把官方資料往前補到 2007 年，拿它沒用過的 2008–2014 年重測。</p>
    <p>2008–2014 扣成本後 CAGR（年化報酬，每年平均的複利報酬）%OOS%，同期 0050 %B_OOS%；Calmar（年化報酬 ÷ 最大回撤）%OOS_CAL% 對 %B_OOS_CAL%。領先有一大塊來自 2008 年：策略 %Y08%，0050 %B_Y08%。只看 2009–2014，CAGR %S09% 對加權股價報酬指數 %T09%，但 Calmar %S09_CAL% 對 %T09_CAL%，%S09_WORD%。</p>
  </div>
  <div class="hero-stats">
    <div><div class="hs-label">CAGR 2008–2014</div><div class="hs-value" style="color:var(--brand)">%OOS%</div><div class="hs-sub">0050 %B_OOS%</div></div>
    <div><div class="hs-label">CAGR 全期</div><div class="hs-value" style="color:var(--brand)">%CAGR%</div><div class="hs-sub">0050 %B_CAGR%</div></div>
    <div><div class="hs-label">MDD 全期</div><div class="hs-value" style="color:var(--red)">%MDD%</div><div class="hs-sub">0050 %B_MDD%</div></div>
    <div><div class="hs-label">CAGR FinLab 發表後</div><div class="hs-value">%POST%</div><div class="hs-sub">0050 %B_POST%</div></div>
  </div>
</div>

<div class="note"><b>三個前提。</b>①換股要準時：比規則晚 1 個交易日，全期 CAGR 從 %CAGR% 降到 %DELAY1%；拖到 13 日以後只剩 %DAY13%。②MDD（最大回撤，從前一個高點最多跌掉多少）%MDD%，全部投入跌得很深。③本頁一共試了 %NT% 組設定，其中 %NPOST% 組是看完結果才加或才改的；帳本算出的運氣門檻見「實驗帳本」一節。</div>

<div class="section">
<h2 class="section-title">績效摘要</h2>
<div class="section-sub">2008-01-02 起，淨值從 1 開始，可持有零碎部位，不設本金也不提領。隔日開盤成交；手續費 0.1425%×0.3、賣出證交稅 0.3%、滑價 10 bp（每邊 0.1%）。股利再投入。Sharpe（夏普值）＝每承受一單位波動換到的報酬；Sortino 只算下跌的波動；月勝率＝上漲月份的比例。</div>
<div class="card">
<table>
<thead><tr><th>策略</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Sortino</th><th>Calmar</th><th>月勝率</th></tr></thead>
<tbody>%SUMMARY_ROWS%</tbody>
</table>
<div class="takeaway">股價排序 2008–2014 CAGR %V1B_OOS%，也贏 0050；但全期 MDD %V1B_MDD%，比營收比值排序深，FinLab 發表後年化 %V1B_POST% 也較低，所以本頁以營收比值排序為主。只看營收年增率、不看股價的版本不賺錢。</div>
</div>
</div>

<div class="section">
<h2 class="section-title">分段：規則沒用過 vs FinLab 設計期間</h2>
<div class="card">
<table>
<thead><tr><th>期間</th><th>月營收動能 CAGR</th><th>MDD</th><th>Calmar</th><th>0050 CAGR</th><th>MDD</th><th>Calmar</th></tr></thead>
<tbody>%PERIOD_ROWS%</tbody>
</table>
<div class="takeaway">事前寫好的判準：2008–2014 的 CAGR 與 Calmar 都要高於 0050。兩項都過，所以判定「值得繼續驗證」。但去掉 2008 年後，Calmar %S09_CAL% 對加權股價報酬指數 %T09_CAL%，%S09_WORD%。FinLab 發表後的 8 個多月，年化 %POST%，低於 0050 的 %B_POST%。</div>
</div>
</div>

<div class="section">
<h2 class="section-title">淨值與回撤</h2>
<div class="section-sub">月底淨值，對數座標（每往上一格代表同樣倍數）。精確 MDD 以表格為準。</div>
<div class="chart-card"><h3>淨值曲線 — 起始 1.0</h3><div class="chart-wrap"><canvas id="chart-nav"></canvas></div></div>
<div class="chart-card"><h3>回撤 — 月營收動能 vs 0050</h3><div class="chart-wrap-sm"><canvas id="chart-dd"></canvas></div></div>
<div class="chart-card"><h3>逐年報酬</h3><div class="chart-wrap"><canvas id="chart-yearly"></canvas></div></div>
<div class="card">
<h3>逐年報酬全表 — %NY% 年裡 %WINS% 年贏 0050</h3>
<table>
<thead><tr><th>年</th><th>月營收動能</th><th>0050</th><th>差距</th></tr></thead>
<tbody>%YEARLY_ROWS%</tbody>
</table>
<div class="takeaway">與 0050 月報酬的相關係數（1＝完全同步，0＝無關）%CORR%。平均持股比例 %EXPO%；平均每月有 %PASS% 檔通過條件。</div>
</div>
</div>

%KIT_HTML%

<div class="section">
<h2 class="section-title">壓力事件（區間報酬 vs 0050）</h2>
<div class="card">
<table>
<thead><tr><th>事件</th><th>月營收動能</th><th>0050</th><th>相對</th></tr></thead>
<tbody>%STRESS_ROWS%</tbody>
</table>
<div class="takeaway">事件區間由程式在每個年度找出 0050 最深一次的高點與低點。%STRESS_NOTE%</div>
</div>
</div>

<div class="section">
<h2 class="section-title">成本</h2>
<div class="card">
<table>
<thead><tr><th>成本設定</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Sortino</th><th>Calmar</th><th>月勝率</th></tr></thead>
<tbody>%COST_ROWS%</tbody>
</table>
<div class="takeaway">一年買進加賣出的金額約是淨值的 %TURN% 倍，成本影響很大：零成本 CAGR %ZERO%，手續費不打折加 30 bp 滑價剩 %STRESS30%。</div>
</div>
</div>

<div class="section">
<h2 class="section-title">參數敏感度</h2>
<div class="section-sub">「事前寫好」的 6 項在看到 2008–2014 結果之前決定；「看完結果才加」的 3 項，是看到 15 日版本變差後補的，只用來確認原因。</div>
<div class="card">
<table>
<thead><tr><th>設定（全期）</th><th>何時決定</th><th>CAGR</th><th>MDD</th><th>Calmar</th></tr></thead>
<tbody>%SENS_ROWS%</tbody>
</table>
<div class="takeaway">股價條件不能拿掉（只看營收剩 %NOTECH%）。只取前 5 檔反而變差（%N5%）：營收比值最高的幾檔，常是單月營收一次性大增的公司。換股日越晚越差，營收公布後的前幾個交易日最重要。</div>
</div>
</div>

<div class="section">
<h2 class="section-title">實驗帳本</h2>
<div class="card">
<table>
<thead><tr><th>項目</th><th>數值</th></tr></thead>
<tbody>
<tr><td>試過的設定</td><td>%NT% 組（family REVMOM）</td></tr>
<tr><td>看完結果才加或才改的</td><td>%NPOST% 組（其中 %NHUMAN% 組由站主提出：排除創新板）</td></tr>
<tr><td>設計期間（2015–2025）Sharpe 最高的一組</td><td>%BEST%，Sharpe %BEST_IS%</td></tr>
<tr><td>試 %NT% 次、純靠運氣能挑到的 Sharpe</td><td>%LUCK%</td></tr>
<tr><td>Deflated Sharpe（最佳結果真的打贏運氣的機率）</td><td>%DSR%</td></tr>
<tr><td>主要版本 Sharpe：設計期間／規則沒用過的 2008–2014</td><td>%V1A_IS% ／ %V1A_OOS%</td></tr>
</tbody>
</table>
<div class="takeaway">Sharpe 以扣掉年息 1% 後的日報酬計算。主要版本在規則沒用過的年份 Sharpe 明顯較低，這是比「打贏運氣的機率」更直接的提醒。</div>
</div>
</div>

<div class="section">
<h2 class="section-title">方法論與查核</h2>
<details open><summary>選股規則</summary><div class="d-body">
<ul class="issue-list">
<li><b>換股時點：</b>每月營收截止日（10 日；遇休市順延到下一個交易日）的下一個交易日收盤後判斷，隔天開盤成交。</li>
<li><b>母體：</b>上市、上櫃 4 位數代號普通股，近 20 個交易日平均成交金額 1,000 萬元以上，不含臺灣創新板（一般投資人不一定能買）。已下市股票也在資料裡。</li>
<li><b>條件：</b>近 3 個月平均營收高於近 12 個月平均；股價（把股利加回去算）高於 20、60、120 日平均，且比 5 個交易日前高。</li>
<li><b>排序：</b>近 3 個月平均營收 ÷ 近 12 個月平均營收，取前 10 檔，每檔 10%，不足 10 檔留現金。排序方式 FinLab 未公開，在看任何結果前選定。</li>
<li><b>出處：</b><a href="https://finlab.finance/blog/monthly-revenue-momentum" rel="noopener">FinLab〈月營收動能〉</a>（2026-01-12）。</li>
</ul>
</div></details>
<details open><summary>2026-10-01 修訂：判斷日改到營收截止日的隔天</summary><div class="d-body">
<ul class="issue-list">
<li>月營收的截止日是 10 日，遇到休市順延到下一個上班日。原本的規則是「11 日以後第一個交易日」判斷；當 10 日休市時，這一天剛好就是截止日，有些公司當晚才公布，回測卻已經用到完整營收，等於偷看未來。</li>
<li>現在改成截止日的下一個交易日判斷。2007-12 以來有 %NSHIFT% 個月的判斷日因此往後一天。這項修正由站主指出，記在實驗帳本裡。</li>
<li>影響：全期 CAGR 從 %D11_CAGR% 變成 %CAGR%；2008–2014 從 %D11_OOS% 變成 %OOS%。</li>
</ul>
</div></details>
<details open><summary>2026-10-01 修訂：排除創新板</summary><div class="d-body">
<ul class="issue-list">
<li>原本的母體包含創新板。看過全部結果後，站主要求名單要是一般投資人買得到的，所以改成排除創新板，全部版本重跑。這項修改記在實驗帳本裡，算在「看完結果才改」的設定。</li>
<li>判斷方式：訊號日當天的股票名稱以「-創」結尾。證交所歷史檔會用現在的名稱回填已回收的代號（例如 2432 在 2007–2008 年是倚天資訊，現在是倚天酷碁-創），所以只採用 2021 年 7 月創新板開板以後的名稱。</li>
<li>影響：歷史上一共排除 %NREM% 次入選，都在 %REM_YEARS% 年。全期 CAGR 從 %INC_CAGR% 變成 %CAGR%；FinLab 發表後的年化從 %INC_POST% 降到 %POST%，2026 年有一部分報酬來自創新板股票。2008–2014 不受影響。</li>
</ul>
</div></details>
<details><summary>成交與成本</summary><div class="d-body">
<ul class="issue-list">
<li>當天沒有成交，或開盤就鎖在漲停（要買）、跌停（要賣），順延到之後的開盤，直到下一次換股取代；全期有 %PEND% 個交易日有順延中的委託。漲跌停 2015-06-01 以前是 7%，之後 10%。</li>
<li>股利以還原股價計入並再投入，不扣所得稅與健保補充保費；現金不計息。</li>
<li>容量：若要 90% 的委託不超過當天成交金額的 10%，資金約 %CAP% 以內。</li>
</ul>
</div></details>
<details><summary>資料</summary><div class="d-body">
<ul class="issue-list">
<li>證交所每日收盤行情、除權息、減資、變更面額公告；櫃買中心每日行情、除權息、減資公告；公開資訊觀測站月營收彙總。股價 2007-01 起、營收 2006-01 起。</li>
<li>2007–2011 年櫃買無成交日的價格欄印成 0.00，改為無成交；其中有成交量卻沒有開收盤價的列，成交量不計入流動性。2008 年證交所除權息表多兩欄，改用欄位名稱讀取。</li>
<li>加權股價報酬指數在證交所日資料裡 2009 年才有，所以 2008 年只和 0050 比。</li>
</ul>
</div></details>
<details><summary>查核</summary><div class="d-body">
<ul class="issue-list">
<li><b>沒有偷看未來：</b>選 6 個日期，把那天以後的資料全部刪掉重選，三種排序選出的股票都相同。</li>
<li><b>引擎對帳：</b>用研究版的權重與成本重跑，CAGR %XCHK%，與研究版 36.7% 相同。研究版另以整張交易、500 萬本金重跑過，結論一致。</li>
<li><b>除權息參考價：</b>2007–2014 年 7,812 筆有 7,811 筆與官方公告相同；2015 年以後 21,921 筆全部相同。</li>
<li><b>下市與異常價格：</b>期末沒有卡在已停止交易的股票；持有期間沒有「漲跌超過當時漲跌停、又查不到公司行動紀錄」的價格。</li>
<li><b>人工抽查：</b>規則沒用過的年份抽 3 筆（6005 群益證 2009-03、3687 歐買尬 2011-08、1432 大魯閣 2013-05），條件都成立。</li>
</ul>
</div></details>
</div>

</div>

<footer>InvestMQuest Research · 月營收動能選股回測 · 生成於 %NOW% · 僅供研究，非投資建議</footer>

<script>
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang TC',sans-serif";
Chart.defaults.font.size=11;
const LBL=%JS_LBL%;
new Chart(document.getElementById('chart-nav'),{type:'line',
 data:{labels:LBL,datasets:[
  {label:'月營收動能',data:%JS_NAV%,borderColor:'#1a56db',borderWidth:1.8,pointRadius:0,tension:.05},
  {label:'0050（含股利）',data:%JS_NAV_B%,borderColor:'#6b7280',borderWidth:1.3,pointRadius:0,tension:.05}
 ]},
 options:{responsive:true,maintainAspectRatio:false,interaction:{intersect:false,mode:'index'},
  scales:{y:{type:'logarithmic',ticks:{callback:v=>v.toLocaleString()}},x:{ticks:{maxTicksLimit:14,autoSkip:true}}},
  plugins:{legend:{position:'top'}}}});
new Chart(document.getElementById('chart-dd'),{type:'line',
 data:{labels:LBL,datasets:[
  {label:'月營收動能',data:%JS_DD%,borderColor:'#dc2626',backgroundColor:'rgba(220,38,38,.10)',fill:true,borderWidth:1.3,pointRadius:0},
  {label:'0050',data:%JS_DD_B%,borderColor:'#6b7280',borderWidth:1,pointRadius:0}
 ]},
 options:{responsive:true,maintainAspectRatio:false,interaction:{intersect:false,mode:'index'},
  scales:{y:{ticks:{callback:v=>v+'%'}},x:{ticks:{maxTicksLimit:14,autoSkip:true}}},
  plugins:{legend:{position:'top'}}}});
new Chart(document.getElementById('chart-yearly'),{type:'bar',
 data:{labels:%JS_YEARS%,datasets:[
  {label:'月營收動能',data:%JS_RET%,backgroundColor:'#1a56db'},
  {label:'0050',data:%JS_RET_B%,backgroundColor:'#9ca3af'}
 ]},
 options:{responsive:true,maintainAspectRatio:false,scales:{y:{ticks:{callback:v=>v+'%'}}},plugins:{legend:{position:'top'}}}});
%KIT_JS%
</script>
</body>
</html>"""


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT)
