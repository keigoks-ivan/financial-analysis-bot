"""Render the live pick-list page (docs/revmom-picks/index.html in financial-analysis-bot).

Usage:  ~/.venvs/v7bt/bin/python -m src.revmom_backtest.generate_picks_page [output_path]
Inputs: results/revmom/picks_*.json (src/revmom_backtest/picks.py), results/revmom/{V1a_base,bench_0050}_daily.csv.gz
(src/revmom_backtest/run.py), data/revmom/extra_etf.parquet (00981A, src/revmom_backtest/update_data.py).
Forward tracking starts at TRACK_START's close; history before it lives on /backtest/revmom/ only.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_env as SE  # noqa: E402  (local v7-backtest vs. cloud copy in the site repo)

ROOT = SE.ROOT
RES = ROOT / "results" / "revmom"
DATA = ROOT / "data" / "revmom"
DEFAULT_OUTPUT = SE.SITE / "docs" / "revmom-picks" / "index.html"
TRACK_START = pd.Timestamp("2026-09-30")


def pct(x, sign=True, nd=1):
    if x is None or x != x:
        return "—"
    return (f"{x * 100:+.{nd}f}%" if sign else f"{x * 100:.{nd}f}%").replace("-", "−")


def num(x):
    if x is None or x != x:
        return "—"
    return f"{x:,.2f}".rstrip("0").rstrip(".") if x < 1000 else f"{x:,.0f}"


def color(x):
    return "" if x is None or x != x or x == 0 else (' style="color:var(--green)"' if x > 0 else ' style="color:var(--red)"')


def next_signal_guess(sig: str) -> str:
    """Next month's signal day assuming weekends are the only closures: the weekday after the deadline
    (the 10th, or the first weekday after it). National holidays (e.g. 10/10) can push it later."""
    p = pd.Period(sig, "M") + 1
    d = pd.Timestamp(p.year, p.month, 10)
    while d.weekday() >= 5:
        d += pd.Timedelta(days=1)
    d += pd.Timedelta(days=1)
    while d.weekday() >= 5:
        d += pd.Timedelta(days=1)
    return str(d.date())


def tracking():
    nav = pd.read_csv(RES / "V1a_base_daily.csv.gz", parse_dates=["date"], index_col="date").nav
    b = pd.read_csv(RES / "bench_0050_daily.csv.gz", parse_dates=["date"], index_col="date").nav
    e = pd.read_parquet(DATA / "extra_etf.parquet")
    e = e[e.code == "00981A"].set_index("date").sort_index()
    f = (e.close / (e.close - e.chg)).fillna(1.0)            # total-return daily factor from the official change
    etf = f.cumprod()
    out = {}
    for name, s in (("月營收動能", nav), ("0050", b), ("00981A", etf)):
        s = s[s.index >= TRACK_START]
        out[name] = {"start": str(s.index[0].date()) if len(s) else None, "last": str(s.index[-1].date()) if len(s) else None,
                     "ret": float(s.iloc[-1] / s.iloc[0] - 1) if len(s) > 1 else None,
                     "mdd": float((s / s.cummax() - 1).min()) if len(s) > 1 else None}
    return out, nav


def period_rows(lists, nav):
    """Each list's return from its signal-day close to the next signal-day close (or the latest close), NAV basis,
    counted only from TRACK_START on."""
    rows = []
    sigs = [pd.Timestamp(r["signal_day"]) for r in lists]
    for i, r in enumerate(lists):
        a = max(sigs[i], TRACK_START)
        z = sigs[i + 1] if i + 1 < len(sigs) else nav.index[-1]
        s = nav[(nav.index >= a) & (nav.index <= z)]
        ret = float(s.iloc[-1] / s.iloc[0] - 1) if len(s) > 1 else None
        note = "（自追蹤起點起算）" if sigs[i] < TRACK_START else ""
        rows.append((r["signal_day"], r["buy_day"], "、".join(f'{p["code"]} {p["name"]}' for p in r["picks"]),
                     f"{a.date()} → {z.date() if len(s) else '—'}{note}", ret))
    return rows


def main(out=DEFAULT_OUTPUT):
    full_nav_block = SE.full_nav_block
    lists = [json.loads(p.read_text()) for p in sorted(RES.glob("picks_*.json"))]
    lists = sorted(lists, key=lambda r: r["signal_day"])
    cur = lists[-1]
    trk, nav = tracking()
    pick_rows = "".join(
        f'<tr><td>{p["rank"]}</td><td>{p["code"]}</td><td>{p["name"]}</td><td>{p["market"]}</td>'
        f'<td>{p["rev_ratio_3m_12m"]:.2f}</td><td{color(p["rev_3m_yoy"])}>{pct(p["rev_3m_yoy"])}</td>'
        f'<td>{num(p["signal_close"])}</td><td>{num(p["buy_open"])}</td>'
        f'<td{color(p["ret_since_buy_to_asof"])}>{pct(p["ret_since_buy_to_asof"])}</td></tr>' for p in cur["picks"])
    alt_rows = "".join(
        f'<tr><td>{a["rank"]}</td><td>{a["code"]}</td><td>{a["name"]}</td><td>{a["market"]}</td>'
        f'<td>{a["rev_ratio_3m_12m"]:.2f}</td><td{color(a["rev_3m_yoy"])}>{pct(a["rev_3m_yoy"])}</td>'
        f'<td>{num(a["signal_close"])}</td></tr>' for a in cur["alternates"])
    trk_rows = "".join(
        f'<tr><td>{k}</td><td>{v["start"] or "—"}</td><td>{v["last"] or "—"}</td><td{color(v["ret"])}>{pct(v["ret"])}</td>'
        f'<td style="color:var(--red)">{pct(v["mdd"])}</td></tr>' for k, v in trk.items())
    per = period_rows(lists, nav)
    per_rows = "".join(f'<tr><td>{s}</td><td>{bday}</td><td style="font-size:.82rem">{names}</td><td>{span}</td>'
                       f'<td{color(r)}>{pct(r)}</td></tr>' for s, bday, names, span, r in per)
    arch_rows = "".join(f'<tr><td>{r["signal_day"]}</td><td>{r["buy_day"]}</td><td>{r["revenue_month_used"]}</td>'
                        f'<td style="font-size:.82rem">{"、".join(p["code"] + " " + p["name"] for p in r["picks"])}</td></tr>'
                        for r in reversed(lists))
    started = trk["月營收動能"]["ret"] is not None
    rp = {
        "%SITE_NAV%": full_nav_block("pick", None),
        "%NOW%": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "%SIG%": cur["signal_day"], "%BUY%": cur["buy_day"] or "—", "%REVM%": cur["revenue_month_used"],
        "%DATA%": cur["data_last_day"], "%REVLAST%": cur["revenue_last_month"],
        "%NEXT%": next_signal_guess(cur["signal_day"]), "%NEXTREV%": str(pd.Period(cur["signal_day"], "M")),
        "%NU%": f'{cur["n_universe"]:,}', "%NP%": str(cur["n_pass"]),
        "%PICK_ROWS%": pick_rows, "%ALT_ROWS%": alt_rows, "%TRK_ROWS%": trk_rows, "%PER_ROWS%": per_rows,
        "%ARCH_ROWS%": arch_rows, "%TRACK_START%": str(TRACK_START.date()),
        "%TRK_NOTE%": ("" if started else "追蹤剛從起點開始，還沒有可比較的報酬；之後每個交易日自動更新。"),
    }
    html = TEMPLATE
    for k, v in rp.items():
        html = html.replace(k, v)
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
<title>台股月營收動能名單 | InvestMQuest Research</title>
<style>
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;--text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--red:#dc2626;--amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang TC','Noto Sans TC',sans-serif;
     background:var(--bg);color:var(--text);line-height:1.7;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.75rem 0 1.25rem;background:linear-gradient(180deg,#eff6ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.6rem;font-weight:700;color:var(--brand)}
.page-hdr .sub{color:var(--muted);font-size:.9rem;margin-top:.2rem}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}.crumb a{color:var(--muted)}
.badge{display:inline-block;background:#f3f4f6;color:#374151;border:1px solid #d1d5db;font-size:.72rem;font-weight:600;padding:.1rem .5rem;border-radius:4px;margin-left:.4rem;vertical-align:3px}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.15rem;font-weight:700;margin-bottom:1rem;padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.section-sub{font-size:.88rem;color:var(--muted);margin:-.5rem 0 1rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem;overflow-x:auto}
.card .takeaway{font-size:.9rem;margin-top:.75rem;padding:.6rem .9rem;border-radius:6px;background:var(--brand-light);border-left:3px solid var(--brand)}
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{text-align:left;padding:.55rem .7rem;border-bottom:1px solid var(--border)}
th{background:#f9fafb;font-weight:600;font-size:.78rem;color:var(--muted);white-space:nowrap}
td{font-variant-numeric:tabular-nums}
.kv{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:8px;overflow:hidden;margin:1rem 0}
.kv>div{background:var(--card);padding:.8rem 1rem}
.kv .k{font-size:.75rem;color:var(--muted)}.kv .v{font-size:1.05rem;font-weight:700}
.note{background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px;padding:.85rem 1.1rem;font-size:.86rem;color:var(--amber-text);margin:1rem 0}
.rules{padding-left:1.2rem;font-size:.9rem;color:#374151;line-height:1.9}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.25rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){.kv{grid-template-columns:repeat(2,1fr)}table{font-size:.78rem}th,td{padding:.45rem .5rem}}
</style>
</head>
<body>
%SITE_NAV%

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/cockpit/">選股主控台</a> / 台股月營收動能名單</div>
    <h1>台股月營收動能名單<span class="badge">對照組</span></h1>
    <div class="sub">回測規則機械產生的名單 · 每月營收截止日的下一個交易日換股 · 資料到 %DATA%，每個交易日自動更新</div>
  </div>
</div>

<div class="container">

<div class="note"><b>對照組 · 不是投資建議 · 名單只在下次換股前有效。</b>這份名單照 <a href="/backtest/revmom/">月營收動能選股回測</a> 的規則自動產生，沒有人工挑選。回測在規則沒用過的 2008–2014 年贏 0050，但最近一年多輸 0050 與 00981A；這裡從 %TRACK_START% 起逐日記錄它往後的實際表現。</div>

<div class="kv">
  <div><div class="k">判斷日</div><div class="v">%SIG%</div></div>
  <div><div class="k">買進日（開盤）</div><div class="v">%BUY%</div></div>
  <div><div class="k">使用的月營收</div><div class="v">%REVM%</div></div>
  <div><div class="k">下次換股（預定）</div><div class="v">%NEXT%</div></div>
</div>

<div class="section">
<h2 class="section-title">本期名單</h2>
<div class="section-sub">母體 %NU% 檔裡，同時符合營收與股價條件的有 %NP% 檔，取營收比值最高的 10 檔，各占 10%。營收比值＝近 3 個月平均營收 ÷ 近 12 個月平均營收。</div>
<div class="card">
<table>
<thead><tr><th>名次</th><th>代號</th><th>名稱</th><th>市場</th><th>營收比值</th><th>近 3 月營收年增</th><th>判斷日收盤</th><th>買進日開盤</th><th>買進後報酬（含息）</th></tr></thead>
<tbody>%PICK_ROWS%</tbody>
</table>
<div class="takeaway">買進後報酬從買進日開盤算到 %DATA% 收盤，股利加回去計算，未扣手續費與稅。前 10 名有股票買不到時，規則本身不遞補。</div>
</div>
<div class="card">
<h3 style="font-size:1rem;margin-bottom:.6rem">備取（同樣通過全部條件，排第 11–20 名）</h3>
<table>
<thead><tr><th>名次</th><th>代號</th><th>名稱</th><th>市場</th><th>營收比值</th><th>近 3 月營收年增</th><th>判斷日收盤</th></tr></thead>
<tbody>%ALT_ROWS%</tbody>
</table>
</div>
</div>

<div class="section">
<h2 class="section-title">規則</h2>
<div class="card">
<ul class="rules">
<li>每月營收截止日（10 日；遇休市順延到下一個交易日）的下一個交易日收盤後判斷，隔天開盤換股。等截止日過了才判斷，才能確定所有公司都已公布；下次換股用 %NEXTREV% 營收，等營收公布後名單才會產生。</li>
<li>母體：上市、上櫃 4 位數普通股，近 20 個交易日平均成交金額 1,000 萬元以上，不含臺灣創新板。</li>
<li>條件：近 3 個月平均營收高於近 12 個月平均；股價用還原權息價格（股利加回去）計算，要高於 20、60、120 日平均，且比 5 個交易日前高。</li>
<li>排序：營收比值由大到小取前 10 檔，每檔 10%，不足 10 檔的部分留現金。</li>
<li>資料：證交所、櫃買中心每日行情與除權息公告，公開資訊觀測站月營收，都是官方免費資料。</li>
</ul>
</div>
</div>

<div class="section">
<h2 class="section-title">前進追蹤（%TRACK_START% 收盤起）</h2>
<div class="section-sub">「前進追蹤」只記錄名單公開之後的表現，不含任何回測期間。月營收動能用回測同一套帳戶算（可買零碎部位、扣手續費 0.1425%×0.3、證交稅 0.3%、滑價 0.1%）；0050 與 00981A 為總報酬。%TRK_NOTE%</div>
<div class="card">
<table>
<thead><tr><th>標的</th><th>起點</th><th>最新</th><th>累計報酬</th><th>期間最大回撤</th></tr></thead>
<tbody>%TRK_ROWS%</tbody>
</table>
</div>
<div class="card">
<h3 style="font-size:1rem;margin-bottom:.6rem">逐期表現</h3>
<table>
<thead><tr><th>判斷日</th><th>買進日</th><th>名單</th><th>計算區間</th><th>該期報酬</th></tr></thead>
<tbody>%PER_ROWS%</tbody>
</table>
<div class="takeaway">該期報酬以月營收動能帳戶的淨值計算，從判斷日收盤到下一個判斷日收盤；最新一期算到最新收盤。</div>
</div>
</div>

<div class="section">
<h2 class="section-title">歷代名單</h2>
<div class="card">
<table>
<thead><tr><th>判斷日</th><th>買進日</th><th>月營收</th><th>名單</th></tr></thead>
<tbody>%ARCH_ROWS%</tbody>
</table>
</div>
</div>

</div>

<footer>InvestMQuest Research · 台股月營收動能名單（對照組）· 更新於 %NOW% · 月營收到 %REVLAST% · 僅供研究，非投資建議</footer>
</body>
</html>"""


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT)
