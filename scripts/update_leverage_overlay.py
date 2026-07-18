#!/usr/bin/env python3
"""Live vol-target leverage-overlay signal — sub-page of /long-track-smh/.

Renders docs/long-track-smh/leverage/index.html: the CURRENT vol-target leverage
reading for the STX50 stock core. Each run pulls fresh QQQ, computes 20-day
realized vol vs its 252-day median → L = clip(median/vol, 1, 1.8) → recommended
overlay f = (L−1)×0.5 of MNQ (Nasdaq micro futures, levers the QQQ half), and the
contract count for a nominal NAV. Reads the STX50 exposure from the sibling
long-track-smh/state.json for the combined picture.

STATUS — EXPERIMENTAL / OOS-UNCONFIRMED. The 2026-06 review found this is a thin,
EQUITY-SPECIFIC edge whose risk-adjusted value vanishes out-of-sample (the crisis
protection can't be OOS-tested). It is NOT an adopted live-money system — this
page is a paper reading only. Full evidence + caveats: /backtest/leverage/.

Schedule: daily after US close (vol is a daily quantity).
"""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_nav import full_nav_block  # noqa: E402

NAV_BLOCK = full_nav_block("system", "ltsmh")
OUTPUT = Path(__file__).parent.parent / "docs" / "long-track-smh" / "leverage" / "index.html"
STATE_JSON = Path(__file__).parent.parent / "docs" / "long-track-smh" / "leverage" / "state.json"
STX_STATE = Path(__file__).parent.parent / "docs" / "long-track-smh" / "state.json"

WIN, MEDWIN, CAP, WQ = 20, 252, 1.8, 0.5     # vol window, median window, cap, QQQ weight in STX50
NOMINAL_NAV = 1_000_000.0                     # for MNQ contract sizing (scale linearly)
MNQ_MULT = 2.0                                # MNQ = $2 per Nasdaq-100 index point


def fetch_close(ticker: str) -> pd.Series:
    end = datetime.now() + timedelta(days=1)
    start = end - timedelta(days=365 * 4)     # 4y: covers 252d median + 20d vol warmup
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"),
                     end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    return (c.iloc[:, 0] if isinstance(c, pd.DataFrame) else c).dropna()


def vol_target():
    qc = fetch_close("QQQ")
    r = qc.pct_change()
    vol = r.rolling(WIN).std() * np.sqrt(252)
    med = vol.rolling(MEDWIN, min_periods=60).median()
    L = (med / vol).clip(1.0, CAP)
    f = (L - 1.0) * WQ                         # MNQ overlay on the QQQ half, max +0.4x
    df = pd.DataFrame({"vol": vol, "med": med, "L": L, "f": f}).dropna()
    wk = df.resample("W-FRI").last().dropna().tail(12)
    cur = df.iloc[-1]
    return cur, wk, qc.index[-1]


def read_stx_exposure():
    try:
        return float(json.loads(STX_STATE.read_text()).get("combined_exposure_pct", 0.0))
    except Exception:
        return None


def fmt_pct(v):
    return f"{v*100:.0f}%"


def main():
    cur, wk, asof = vol_target()
    L, f, vol, med = float(cur["L"]), float(cur["f"]), float(cur["vol"]), float(cur["med"])
    try:
        nq_px = float(fetch_close("NQ=F").iloc[-1])
    except Exception:
        nq_px = float(fetch_close("QQQ").iloc[-1]) * 41.0   # NDX ≈ QQQ × ~41 fallback
    unit = nq_px * MNQ_MULT                                  # $ notional per MNQ contract
    contracts = int((f * NOMINAL_NAV) / unit) if unit > 0 else 0
    stx_exp = read_stx_exposure()
    asof_str = pd.Timestamp(asof).strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    on = f > 0.005
    hero = "green" if f >= 0.25 else ("amber" if on else "grey")
    big = f"+{f:.2f}x" if on else "0x（不加）"
    calm = "比平常平靜 → 加槓桿" if L > 1.001 else "沒有比平常平靜 → 不加"

    # trajectory rows (recent 12 weekly samples)
    rows = ""
    for d, row in wk.iterrows():
        fv = float(row["f"])
        col = "var(--green)" if fv > 0.005 else "var(--muted)"
        rows += (f"<tr><td>{d.date()}</td><td>{float(row['vol'])*100:.0f}%</td>"
                 f"<td>{float(row['med'])*100:.0f}%</td><td>{float(row['L']):.2f}</td>"
                 f"<td style='color:{col};font-weight:600'>+{fv:.2f}x</td></tr>")

    stx_line = (f"股票核心 STX50 目前曝險 <b>{stx_exp:.0f}%</b>(見 <a href='/long-track-smh/'>主頁</a>)。"
                if stx_exp is not None else "")
    combined_note = (f"組合圖像:股票核心約 {stx_exp:.0f}%(STX50),vol-target 建議在 QQQ/那指半邊"
                     f"<b>{'再加 +%.2fx MNQ' % f if on else '不額外加槓桿'}</b>。"
                     if stx_exp is not None else "")

    html = PAGE.format(
        NAV=NAV_BLOCK, hero=hero, big=big, L=L, f=f, vol_pct=f"{vol*100:.0f}%",
        med_pct=f"{med*100:.0f}%", calm=calm, contracts=contracts, unit=f"{unit:,.0f}",
        nav=f"{NOMINAL_NAV:,.0f}", asof=asof_str, now=now, rows=rows,
        stx_line=stx_line, combined_note=combined_note)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Written {OUTPUT} ({len(html):,} bytes) | L={L:.2f} f=+{f:.2f}x ~{contracts} MNQ")

    STATE_JSON.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": asof_str, "status": "experimental_paper",
        "vol20_pct": round(vol * 100, 1), "median252_pct": round(med * 100, 1),
        "L": round(L, 3), "f_mnq": round(f, 3), "mnq_contracts_per_1M": contracts,
        "stx50_exposure_pct": stx_exp,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Sidecar JSON: {STATE_JSON}")


PAGE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>vol-target 槓桿層 · STX50 即時讀數(實驗) | InvestMQuest Research</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/imq-base.css">
<style>
:root{{--brand:#0d2244;--bg:#f7f3ea;--card:#ffffff;--text:#0c1521;--muted:#9aa7b8;--border:#e5dfd0;
  --green:#15803d;--green-bg:#eafaef;--green-border:var(--line);--green-text:#15803d;
  --amber:#a16207;--amber-bg:#fbf3df;--amber-border:var(--line);--amber-text:#a16207;--grey:#9aa7b8}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;font-size:14px}}
a{{color:var(--brand);text-decoration:none}}a:hover{{text-decoration:underline}}
.container{{max-width:1000px;margin:0 auto;padding:0 1.5rem}}
.page-hdr{{padding:1.5rem 0 1.2rem;background:var(--card);border-bottom:1px solid var(--border)}}
.page-hdr h1{{font-family:var(--serif);font-size:1.4rem;font-weight:700;letter-spacing:-.01em}}
.page-hdr .sub{{color:var(--muted);font-size:.85rem;margin-top:.2rem}}
.crumb{{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}}.crumb a{{color:var(--muted)}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;margin-bottom:1rem;box-shadow:var(--sh-1)}}
.card h3{{font-size:.95rem;font-weight:600;margin-bottom:.75rem}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th,td{{text-align:left;padding:.5rem .7rem;border-bottom:1px solid var(--border)}}
th{{background:transparent;font-family:var(--mono);font-weight:600;font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}}
td{{font-variant-numeric:tabular-nums}}
.banner{{background:var(--amber-bg);border:1px solid var(--amber-border);color:var(--amber-text);border-radius:var(--r);padding:.7rem 1rem;font-size:.8rem;margin:1rem 0}}
.status-hero{{padding:2rem 0 1rem;text-align:center}}
.status-badge{{display:inline-flex;align-items:center;gap:.75rem;padding:.9rem 2.2rem;border-radius:var(--r);font-size:1.2rem;font-weight:800;margin-bottom:.5rem}}
.status-badge .dot{{width:13px;height:13px;border-radius:50%;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.status-exposure{{font-size:2.6rem;font-weight:800;margin:.3rem 0}}
.status-date{{font-size:.8rem;color:var(--muted)}}
.hero-green .status-badge{{background:var(--green-bg);color:var(--green-text);border:2px solid var(--green-border)}}
.hero-green .dot{{background:var(--green)}}.hero-green .status-exposure{{color:var(--green)}}
.hero-amber .status-badge{{background:var(--amber-bg);color:var(--amber-text);border:2px solid var(--amber-border)}}
.hero-amber .dot{{background:var(--amber)}}.hero-amber .status-exposure{{color:var(--amber)}}
.hero-grey .status-badge{{background:var(--line-soft);color:var(--muted);border:2px solid var(--border)}}
.hero-grey .dot{{background:var(--grey)}}.hero-grey .status-exposure{{color:var(--muted)}}
.kpi{{display:grid;grid-template-columns:repeat(4,1fr);gap:.7rem;margin:.5rem 0 1rem}}
.kpi>div{{text-align:center;background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:.6rem .3rem}}
.kpi span{{display:block;font-size:.64rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}
.kpi b{{font-size:1.2rem;font-weight:800}}
.rule-list{{font-size:.82rem;line-height:1.9}}
@media(max-width:768px){{.status-exposure{{font-size:2rem}}.kpi{{grid-template-columns:repeat(2,1fr)}}table{{font-size:.74rem}}}}
</style>
</head>
<body>
{NAV}
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / <a href="/long-track-smh/">美股長線訊號</a> / vol-target 槓桿層</div>
  <h1>vol-target 槓桿層 — STX50 即時讀數</h1>
  <div class="sub">在 STX50 股票核心上，用 MNQ 微型那指期貨的「波動目標」槓桿讀數 · 平靜加碼、變亂收手 · Long only</div>
</div></div>
<div class="container">

<div style="background:var(--amber-bg);border:2px solid var(--amber-border);color:var(--amber-text);border-radius:10px;padding:.9rem 1.2rem;margin:1rem 0;font-size:.92rem;font-weight:600;text-align:center">2026-07-18 起母系統（STX50）非實單系統（實單已改為 <a href="/long-track-w52-adaptive/" style="color:var(--amber-text);text-decoration:underline">W52 × 自適應波動率 150%</a>）；本頁本為實驗性紙上讀數、保留作對照。</div>

<div class="banner">
  <b>⚠ 實驗性 · 紙上讀數 · 非實倉。</b>2026-06 review 結論:這是一個<b>很薄、股票特有、且 out-of-sample 風險調整 edge ≈ 0</b> 的小東西
  (危機保護無法被 OOS 證明)。<b>不是已採用的系統</b>，這頁只是當前讀數。完整證據與缺陷見 <a href="/backtest/leverage/">回測頁</a>。
</div>

<div class="status-hero hero-{hero}">
  <div class="status-badge"><span class="dot"></span><span>vol-target 目前建議槓桿</span></div>
  <div class="status-exposure">{big}</div>
  <div style="font-size:.82rem;color:var(--muted)">MNQ 疊加(QQQ/那指半邊，上限 +0.40x)· {calm}</div>
  <div class="status-date">資料截至 {asof}(收盤)· 頁面更新 {now}</div>
</div>

<div class="card">
<h3>怎麼算出來的(今天)</h3>
<div class="kpi">
  <div><span>QQQ 20 日波動</span><b>{vol_pct}</b></div>
  <div><span>過去一年中位數</span><b>{med_pct}</b></div>
  <div><span>槓桿倍數 L</span><b>{L:.2f}</b></div>
  <div><span>建議疊加 f</span><b style="color:var(--green)">+{f:.2f}x</b></div>
</div>
<div class="rule-list">
規則:<b>L = clip( 中位數 ÷ 20日波動 , 1.0 , 1.8 )</b>，疊加 <b>f = (L−1) × 0.5</b> 的 MNQ。
波動<b>比平常低</b> → L&gt;1 加槓桿;<b>一變亂</b> → L=1 收回。<br>
口數:以名目 NAV ${nav} 計，1 口 MNQ ≈ ${unit} 名目 → 目前約 <b>{contracts} 口</b>(按實際 STX50 資金等比例縮放)。<br>
{stx_line}
</div>
</div>

<div class="card">
<h3>近 12 週軌跡</h3>
<table><thead><tr><th>週(五)</th><th>20日波動</th><th>一年中位數</th><th>L</th><th>建議疊加 f</th></tr></thead>
<tbody>{rows}</tbody></table>
<div style="font-size:.76rem;color:var(--muted);margin-top:.6rem">{combined_note}</div>
</div>

<div class="card">
<h3>為什麼這頁存在(且為什麼要小心)</h3>
<div class="rule-list">
· <b>用途</b>:在 STX50 上「平靜時用 MNQ 多壓一點」的當前讀數。最大價值是危機年波動一升它自動收回、不放大尾部。<br>
· <b>很薄</b>:全期 Sharpe 只 +0.02~0.05、Calmar +0.02;OOS 風險調整 edge ≈ 0(<a href="/backtest/leverage/">walk-forward 見回測頁</a>)。<br>
· <b>股票特有</b>:同規則放到黃金/油/債/匯/農 6 取 1 才有效 —— 不是普遍原理。<br>
· <b>可執行性</b>:MNQ 微型 2019 才上市;小帳戶在那之前切不出這麼細的曝險(平均才 +0.09x)。<br>
· <b>作空已否決</b>:期貨作空在股票上 4 次都失敗(軋空)。
</div>
</div>

</div>
<footer class="imq-foot">
  <div>&copy; 2026 InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</body></html>"""


if __name__ == "__main__":
    main()
