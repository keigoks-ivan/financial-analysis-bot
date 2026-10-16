"""AI 信用風險監測頁面（docs/ai-credit/index.html）。純函式：state＋指標＋事件 → HTML 字串。

版面照全站設計系統（docs/assets/imq-base.css；規範 notes/site-internal/root/_styleguide_v1_20260707.md §9）：
頁內 CSS 只用其 token，圖表色沿用 etf-dash 的 --x-* 組。第二輪四區的片段在 aic_page2.py。
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

from aic_metrics import GROUPS, NAMES, REGISTERED_ON, THRESHOLD_TEXT, usd
import aic_page2 as P2
import aic_round2 as R

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

esc = html.escape

CSS = """
:root{
  --x-navy:#0d2244; --x-navy-2:#173564; --x-blue:#3f6a9c; --x-sky:#8fb0cf;
  --x-teal:#3d7a70; --x-grey:#9aa7b8; --x-rule:var(--gold-deep);
}
*{box-sizing:border-box;min-width:0}
html,body{max-width:100%;overflow-x:hidden}
body{margin:0;font-family:var(--sans);background:var(--paper);color:var(--body);line-height:1.6;font-size:14px}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px 60px}
.x-pos{color:var(--pos)} .x-neg{color:var(--neg)}
a{color:var(--accent)}

.cover{background:linear-gradient(135deg,var(--x-navy) 0%,var(--x-navy-2) 100%);padding:22px 28px;margin-bottom:0}
.cover-inner{max-width:1100px;margin:0 auto}
.crumb{font-size:12px;color:rgba(255,255,255,.6);margin-bottom:6px}
.crumb a{color:rgba(255,255,255,.8);text-decoration:none}
.cover h1{font-family:var(--serif);font-size:1.6rem;font-weight:700;line-height:1.25;letter-spacing:-.01em;color:#fff;margin:0}
.cover .sub{font-size:13px;color:rgba(255,255,255,.75);margin-top:6px;max-width:80ch;line-height:1.75}
.cover .updated{font-family:var(--mono);font-size:11px;color:rgba(255,255,255,.55);margin-top:8px}

.headline{display:flex;flex-wrap:wrap;gap:12px 32px;align-items:center;margin:18px 0 4px;padding:14px 16px;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--x-navy);border-radius:var(--r)}
.headline .imq-stat .v{font-size:1.9rem}
.headline em{font-style:normal;font-weight:700;color:var(--ink)}
.headline ul{margin:0;padding-left:1.1rem;font-size:13px}
.warnbar{font-size:12px;color:var(--warn);background:var(--gold-bg);border:1px solid var(--gold-soft);border-radius:6px;padding:6px 10px;margin-top:10px}

.chapter-head{background:var(--x-navy);border-bottom:2px solid var(--x-rule);padding:7px 12px;margin:26px 0 8px}
.chapter-head .ch-title{font-family:var(--serif);font-size:1rem;font-weight:700;color:#fff}
.ch-sub{font-size:12px;color:var(--sec);margin:0 0 10px}
.exhibit{margin:18px 0 4px}
.ex-label{font-family:var(--mono);font-size:.66rem;font-weight:700;letter-spacing:.06em;color:var(--x-navy)}
.ex-title{font-family:var(--sans);font-size:.95rem;font-weight:700;color:var(--ink);margin:1px 0 2px}
.ex-sub{font-size:11.5px;color:var(--sec);margin-bottom:8px}
.ex-src{font-family:var(--mono);font-size:9.5px;color:var(--muted);margin-top:5px}

.ind,.blk{padding:14px 16px;margin:12px 0}
.ind-h{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.ind-h .n{font-family:var(--mono);font-size:.78rem;font-weight:700;color:var(--muted)}
.ind-h h3,.blk h3{font-size:1rem;font-weight:700;color:var(--ink);margin:0;flex:1;min-width:12rem}
.blk h3 .imq-badge{margin-left:8px;vertical-align:middle}
.stat-row{display:flex;flex-wrap:wrap;gap:14px 28px;margin:10px 0}
.imq-table{border-collapse:collapse;font-size:.82rem;background:var(--card);width:100%;max-width:100%}
.imq-table th{font-family:var(--mono);font-size:.62rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:var(--x-navy);text-align:left;padding:.5rem .7rem;border-bottom:2px solid var(--x-navy);white-space:nowrap}
.imq-table td,.imq-table th{overflow-wrap:break-word;word-break:break-word}
.imq-table td{padding:.44rem .7rem;border-bottom:1px solid var(--line-soft);color:var(--body);line-height:1.5;white-space:nowrap}
.imq-table td.num,.imq-table th.num{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right;width:1%;white-space:nowrap}
.imq-table tbody tr:nth-child(even) td{background:#f5f6f8}
.imq-stat{display:inline-flex;flex-direction:column;gap:.1rem}
.imq-stat .v{font-family:var(--mono);font-size:1.05rem;font-weight:700;color:var(--ink)}
.imq-stat .k{font-size:.64rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.why{font-size:12.5px;color:var(--body);background:var(--gold-bg);border:1px solid var(--gold-soft);border-left:3px solid var(--gold-deep);border-radius:var(--r);padding:7px 11px;margin:8px 0}
.why b{color:var(--gold-deep)}
.plain{font-size:13px;color:var(--body);line-height:1.75;margin:8px 0;max-width:86ch}
.fine{font-size:11.5px;color:var(--sec);line-height:1.75;margin:6px 0}
.src{font-size:11px;color:var(--muted);line-height:1.8;margin:6px 0}
.src a{color:var(--sec)}
details{margin-top:8px}
summary{cursor:pointer;font-size:12px;font-weight:600;color:var(--accent)}
.tbl-wrap{overflow-x:auto;margin-top:8px}
.imq-table td.wrap-ok,.imq-table.wrapt td{white-space:normal;min-width:6rem;vertical-align:top}
.imq-table.wrapt td.num{white-space:nowrap;min-width:0}
.chart-box{width:100%;position:relative;margin-top:8px}
.mini-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:8px 0}
.mini{border:1px solid var(--line-soft);border-radius:var(--r);padding:8px 10px;background:var(--card)}
.mini-h{display:flex;justify-content:space-between;font-family:var(--mono);font-size:12px;font-weight:700;color:var(--ink)}
.mini-h span{color:var(--sec)}
@media(max-width:800px){.mini-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.mini-grid{grid-template-columns:1fr}.cover{padding:18px 16px}}
.prose p{font-size:13px;max-width:86ch;margin:0 0 .7rem;line-height:1.8}
.imq-table.method td{white-space:normal;min-width:7rem;vertical-align:top;font-size:.8rem}
.imq-table.method td:nth-child(5),.imq-table.method td:nth-child(6),.imq-table.method td:nth-child(7){min-width:15rem}
"""

# ---------------------------------------------------------------------------
# 每條門檻「為什麼是這個數字」。type：結構線＝越過去狀態真的改變；經驗值＝業界常用、未用歷史擬合。
# short 放在每條指標卡片的門檻旁；long 放在方法表。數字來自 2026-10-16 的實測計算。
# ---------------------------------------------------------------------------
THRESH_WHY = {
    1: ("結構線", "1 是分界：小於 1 本業現金付得起建設，大於 1 就必須對外借錢或增資才蓋得下去。",
        "1 是分界。小於 1，本業現金付得起建設；大於 1，必須對外借錢或增資才蓋得下去。"),
    2: ("結構線", "五家取過半：兩家為負是個別公司的事，過半代表整個族群要靠債市養。",
        "五家取過半。兩家為負是個別公司的事；過半代表族群整體要靠債市養，債市一緊就一起受影響。"),
    3: ("結構線", "取一半：超過一半的建設費用來自新借的錢，就從用賺的錢蓋變成主要用借的錢蓋。",
        "取一半。超過一半的建設費用來自新借的錢，建設就從用賺的錢蓋，變成主要用借的錢蓋。用淨發債，避免借新還舊被算成新增借款。"),
    4: ("經驗值", "一般產業公司淨負債約 3.5 至 4 倍 EBITDA，通常落在投資等級最低一級的邊緣；取區間下緣 3.5，提早看到。",
        "一般產業公司淨負債約 3.5 至 4 倍 EBITDA 時，通常落在投資等級最低一級的邊緣。被降為垃圾債，只能持有投資等級債的基金得賣出，借錢成本跳一階。"
        "取區間下緣 3.5 是為了提早看到。這不是評等機構針對 Oracle 寫明的觸發點，那份資料需付費，未取得。"),
    5: ("經驗值", "高收益債中利息保障低於 1.5 倍，通常落在 CCC 那一群，賺的錢扣完利息所剩無幾。",
        "高收益債中，利息保障低於 1.5 倍的公司通常落在 CCC 那一群，賺的錢扣完利息所剩無幾；2015 年頁岩油違約潮的公司多在這附近。用 EBITDA 是因為 CoreWeave 的營業利益為負。"),
    6: ("結構線", "1 是分界：現金加一年本業現金流不夠還明年到期的本金，就只能借新還舊。",
        "1 是分界。現金加一年的本業現金流若不夠還明年到期的本金，就只能靠借新還舊，債市一關門就出事。刻意不扣資本支出，問的是停建的話撐不撐得住。"),
    7: ("經驗值", "−20 個百分點在 Oracle 是罕見的跌幅（約第 3 百分位），解除線 −10 是進入線的一半，避免來回進出。",
        "近 63 日報酬減 QQQ 小於等於 −20 個百分點的日子，Oracle（2000 年起）占 3.2%，所以 −20 約是 Oracle 過去約第 3 百分位的跌幅。"
        "解除線設在 −10（進入線的一半），是為了避免在門檻附近來回進出：若只用單一 −20 線，Oracle 2026-04-16 起的 127 個交易日內進入 5 次、解除 5 次；加上遲滯後同期只有 3 次狀態改變。"
        "這條規則在 2025-11-24 抓到 Oracle 那一波，當日相對值 −20.15，股價已比 2025-09-10 高點低 38.9%（63 日窗口有落後性），直到 2026-04-21 才解除。"),
    8: ("經驗值", "−20 個百分點在 CoreWeave 約是第 37 百分位，對這檔是常態波動，不是罕見跌幅。",
        "CoreWeave 2025-03 上市，有資料的 327 個交易日中，63 日報酬減 QQQ 小於等於 −20 個百分點的占 36.7%，所以 −20 對這檔約是第 37 百分位，不罕見。"
        "三檔共用同一條線，沒有各自調整；樣本只有約一年半，百分位不穩。遲滯規則在這段期間進入 5 次、解除 5 次。"),
    9: ("經驗值", "−20 個百分點在 Blue Owl 約是第 14 百分位；樣本含前身 SPAC 期間。",
        "Blue Owl（yfinance 代號 OWL）有資料的 1,403 個交易日中，63 日報酬減 QQQ 小於等於 −20 個百分點的占 13.9%，約是第 14 百分位。"
        "樣本從 2020-12 起，含合併前的 SPAC 期間（2021 年 5 月前股價約 10 美元），2021-08 前的窗口仍用到 SPAC 期的基期價。遲滯規則進入 9 次、解除 9 次。"),
    10: ("經驗值", "ARCC 自 2012 年起股價 ÷ 淨值的中位數 1.03，0.85 只在 2015–16 年與 2020 年被穿過，約離中位數往危機低點三分之一處。",
         "以 Ares Capital（ARCC）2012 年底至今的日收盤價（未還原）除以所屬季度的每股淨值計算：股價 ÷ 淨值的中位數約 1.03。"
         "2016 年 2 月能源違約期最低約 0.76，2020 年 3 月疫情最低約 0.47；2022 年與 2023 年的低點是 0.90 與 0.93。"
         "低於 0.85 的日子只出現在 2015–16 年與 2020 年。以 2020 年低點計，0.85 位於中位數往危機低點約三分之一處；"
         "2022、2023 年的升息與銀行危機壓力，這條線沒有抓到，所以它偏向只在大型信用事件時才會越線。"),
    11: ("經驗值", "Nvidia 2010 年起 65 季裡，+10 天約在第 92 百分位，只有 5 季達標；Lucent 出事前應收天數明顯拉長。",
         "Nvidia 2010 年 8 月至今共 65 季，單季應收天數減前四季平均：平均 +0.4 天，標準差 7.5 天，+10 天約落在第 92 百分位。"
         "65 季裡有 5 季達標（2018-10、2019-01、2022-07、2022-10、2025-01）；最新一季（2026-07）為 +8.6 天，離門檻不遠。"
         "類比：Lucent 在 2000 年出事前，應收天數由 1999-09 的 89.8 天（原公布口徑）升到 2000-03 的 93.8 天，重編口徑下 2000-06 為 105.5 天、2000-12 為 113.5 天"
         "（2000-06 起企業網路事業改列停業單位，口徑中斷，前後不能直接相減）。"),
    12: ("經驗值", "歷史類比：Lucent 1999-12 對客戶融資承諾約 84 億美元，相當於 2000 財年營收的約 25%；Nvidia 的分子口徑比 Lucent 寬。",
         "Lucent 在 1999-12-31 對客戶的融資承諾約 84 億美元（10-Q），2000 財年（至 2000-09）營收 338.13 億美元（10-K），約 25%；再加約 14 億美元客戶債務保證，約 29%。"
         "在 1999-09 至 2000-09 五個時點中，84 億是最高的一次（71、84、72、77、67 億），那是電信泡沫破裂前供應商融資的高點。"
         "分子與分母的時點不同（1999 年底的存量對 2000 財年的流量）。Nvidia 的分子含股權投資承諾，並以保證的最大可能損失計，口徑比 Lucent 寬。"),
}

METHOD_ROWS = {
    1: ("蓋資料中心的錢，本業現金流付不起，一定要對外借款或增資。",
        "股息與庫藏股同樣耗現金，這裡沒有扣；融資租賃不在資本支出裡，Microsoft 一年約 246 億美元；各家用自己最新四季，截止日不同。"),
    2: ("五家裡過半數自由現金流為負，整個族群的建設要靠債市養。",
        "Amazon 含零售業務，現金流受庫存與季節影響；單一年度為負也可能只是投資高峰。"),
    3: ("近四季建設費用超過一半來自新借的錢。",
        "用淨發債，已扣掉還款；借到的錢不一定當年花掉。各家發債 tag 不同，Alphabet 的還債標準 tag 含融資租賃本金，會讓淨發債偏低。"),
    4: ("被降成垃圾債，只能買投資等級債的基金會被迫賣出。",
        "融資租賃與尚未起租的租約不在分子裡。"),
    5: ("利息保障倍數過低，賺的錢扣完利息所剩無幾。",
        "EBITDA 沒扣 GPU 折舊，GPU 三到五年就要換，數字比實際寬裕；用 EBITDA 是因為營業利益接近零或為負。"),
    6: ("假設停止擴建，現金加一年的本業現金流夠不夠還明年到期的債；小於 1 倍，不借新還舊就撐不過去。",
        "刻意沒扣資本支出，所以是停止擴建的情境，不是現況；已簽約、無法中止的建設支出會讓實際更緊。"),
    7: ("近三個月比 QQQ 多跌 20 個百分點，代表市場對這家公司的擔心又加重。",
        "股價下跌也可能只是估值修正，不一定是信用惡化。"),
    8: ("同上。", "同上。CoreWeave 2025 年 3 月才上市，歷史較短。"),
    9: ("同上。", "同上。"),
    10: ("BDC 股價明顯低於帳面淨值，代表市場不相信帳上貸款的價值。",
         "淨值每季才更新，股價每天變動，兩者日期不同；折價也可能反映對利率或股息的看法。"),
    11: ("應收帳款天數拉長，代表客戶付款變慢。",
         "Nvidia 出貨集中在季底，單季天數會跳動；大客戶付款條件改變也會拉長天數。"),
    12: ("供應商對客戶的保證與融資承諾占營收比重過高，等於供應商替需求出錢。",
         "保證是最大可能損失，不是已借出的錢；Nvidia 的股權投資承諾是投資，不是放款。"),
}

# 各條指標的資料來源（SEC 申報檔 ticker；另附 Yahoo／FRED 連結）
IND_SEC = {1: ["MSFT", "GOOGL", "AMZN", "META", "ORCL"], 2: ["MSFT", "GOOGL", "AMZN", "META", "ORCL"], 3: ["MSFT", "GOOGL", "AMZN", "META", "ORCL"],
           4: ["ORCL"], 5: ["CRWV"], 6: ["CRWV"], 7: [], 8: [], 9: [], 10: ["ARCC", "OBDC", "BXSL"], 11: ["NVDA"], 12: ["NVDA"]}
IND_YAHOO = {7: ["ORCL", "QQQ"], 8: ["CRWV", "QQQ"], 9: ["OWL", "QQQ"], 10: ["ARCC", "OBDC", "BXSL"]}


def _table(t: dict | None) -> str:
    if not t:
        return ""
    head = "".join(f"<th>{esc(str(h))}</th>" for h in t["head"])
    body = "".join("<tr>" + "".join(f"<td>{esc(str(c))}</td>" for c in r) + "</tr>" for r in t["rows"])
    return f'<div class="tbl-wrap"><table class="imq-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _sources(units: dict, i: int) -> str:
    parts = []
    if IND_SEC.get(i):
        parts.append(P2.sec_sources(units, IND_SEC[i]))
    if IND_YAHOO.get(i):
        parts.append("Yahoo Finance：" + "、".join(P2.link(f"https://finance.yahoo.com/quote/{t}/history", t) for t in IND_YAHOO[i]))
    return f'<p class="src">資料來源：{"；".join(parts)}</p>' if parts else ""


def _card(x: dict, units: dict, extra: str = "") -> str:
    b = x["breached"]
    badge = ('<span class="imq-badge neg">越線</span>' if b is True else ('<span class="imq-badge">資料不全</span>' if b is None else '<span class="imq-badge pos">未越線</span>'))
    vcls = " x-neg" if b is True else ""
    stale = '<span class="imq-badge warn">抓取失敗，沿用上次值；日期為原始資料日期</span>' if x.get("stale") else ""
    notes = "".join(f'<p class="fine">{esc(n)}</p>' for n in x.get("notes") or [])
    typ, short, _long = THRESH_WHY[x["id"]]
    tbl = _table(x.get("table"))
    det = f"<details><summary>明細</summary>{tbl}{notes}</details>" if (tbl or notes) else ""
    return (
        f'<article class="imq-card ind" id="i{x["id"]}"><div class="ind-h"><span class="n">{x["id"]}</span><h3>{esc(x["name"])}</h3>{badge}</div>'
        f'<div class="stat-row"><div class="imq-stat"><span class="v{vcls}">{esc(x["value_text"])}</span><span class="k">現值</span></div>'
        f'<div class="imq-stat"><span class="v">{esc(x["threshold"])}</span><span class="k">門檻（{REGISTERED_ON} 登記）</span></div>'
        f'<div class="imq-stat"><span class="v">{esc(x["date_text"])}</span><span class="k">資料日期</span></div></div>{stale}'
        f'<div class="why"><b>{typ}</b>　{esc(short)}</div>'
        f'<p class="plain">{esc(x["plain"])}</p>{extra}{det}{_sources(units, x["id"])}</article>'
    )


def _spreads(fred: dict | None, stale: bool) -> str:
    if not fred:
        return '<div class="imq-card blk"><h3>背景利差（日）</h3><p class="fine">FRED 資料尚無可用值。</p></div>'
    rows = []
    for sid, s in fred.items():
        pos = "—" if s.get("pos") is None else f"{s['pos'] * 100:.0f}%"
        ago = "—" if s.get("year_ago") is None else f"{s['year_ago']:.2f}%（{s['year_ago_date']}）"
        rows.append(f"<tr><td>{P2.link('https://fred.stlouisfed.org/series/' + sid, s['label'] + '（' + sid + '）')}</td><td class=\"num\">{s['latest']:.2f}%</td><td>{s['asof']}</td>"
                    f"<td class=\"num\">{pos}</td><td class=\"num\">{s['min']:.2f}%～{s['max']:.2f}%</td><td class=\"num\">{ago}</td></tr>")
    st = '<span class="imq-badge warn">抓取失敗，沿用上次值</span>' if stale else ""
    return (
        '<div class="imq-card blk"><h3>背景利差（日）<span class="imq-badge">只顯示，不計入越線條數</span></h3>' + st +
        '<div class="tbl-wrap"><table class="imq-table"><thead><tr><th>系列</th><th class="num">最新</th><th>資料日</th><th class="num">三年區間位置</th>'
        '<th class="num">區間</th><th class="num">一年前</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'
        '<p class="fine">FRED 的 ICE BofA 系列只提供約三年資料，區間位置是在這三年內的相對高低（0% 最低，100% 最高），不代表長期歷史。</p></div>'
    )


def _rpo(units: dict, charts: P2.Charts) -> str:
    names = {"ORCL": "Oracle", "MSFT": "Microsoft", "GOOGL": "Alphabet", "CRWV": "CoreWeave"}
    fl = (units.get("filings") or {}).get("data") or {}
    rows, series = [], []
    for (t, n), color in zip(names.items(), ("gold", "navy", "teal", "blue")):
        u = units.get(f"rpo:{t}")
        if not u or not u.get("data"):
            rows.append(f"<tr><td>{n}</td><td colspan=\"8\">資料尚無可用值</td></tr>")
            continue
        s = u["data"]["series"]
        cells = "".join(f'<td class="num">{usd(p["value"]).replace(" 億美元", "")}<br><span class="fine">{p["end"]}</span></td>' for p in reversed(s))
        cells += "<td></td>" * (8 - len(s))
        flag = "（沿用上次值）" if u.get("stale") else ""
        rows.append(f"<tr><td>{n}{flag}<br><span class=\"fine\">{P2.filing_link(P2.latest_filing(units, t))}</span></td>{cells}</tr>")
        vals = [round(p["value"] / 1e8, 1) for p in s]
        series.append({"label": n, "data": [None] * (8 - len(vals)) + vals, "color": color})
    head = "<th>公司（單位：億美元）</th>" + "".join(f'<th class="num">{h}</th>' for h in ["最新", "前 1 季", "前 2 季", "前 3 季", "前 4 季", "前 5 季", "前 6 季", "前 7 季"])
    chart = charts.add("rpo", ["前 7 季", "前 6 季", "前 5 季", "前 4 季", "前 3 季", "前 2 季", "前 1 季", "最新"], series, 190) if series else ""
    return ('<div class="imq-card blk"><h3>未履約合約金額（RPO）近 8 季<span class="imq-badge">只顯示</span></h3>'
            '<p class="plain">未履約合約是已簽約、尚未認列的營收。它越大，代表未來的收入越有保障，也代表對方未來的付款義務越大。</p>'
            f'{chart}<div class="ex-src">圖：億美元；各家財年不同，橫軸為相對季數。</div>'
            f'<details><summary>明細與資料日</summary><div class="tbl-wrap"><table class="imq-table"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="fine">CoreWeave 2025 年 3 月上市，季數較少。</p>'
            f'<p class="src">來源：{P2.sec_sources(units, ["ORCL", "MSFT", "GOOGL", "CRWV"])}</p></details></div>')


def _leases(units: dict) -> str:
    order = [("MSFT", "Microsoft"), ("ORCL", "Oracle"), ("META", "Meta"), ("AMZN", "Amazon"), ("GOOGL", "Alphabet"), ("CRWV", "CoreWeave")]
    fl = (units.get("filings") or {}).get("data") or {}
    rows = []
    for t, n in order:
        u = units.get(f"lease:{t}")
        if not u or not u.get("data"):
            rows.append(f"<tr><td>{n}</td><td colspan=\"3\">資料尚無可用值</td></tr>")
            continue
        d = u["data"]
        extra = f"；期後另簽 {usd(d['subsequent'])}" if d.get("subsequent") else ""
        stale = "（解析失敗，沿用上次值）" if u.get("stale") else ""
        f = next((x for x in (fl.get(t) or {}).values() if x and x.get("accession") == d.get("accession")), None)
        rows.append(f"<tr><td>{n}</td><td class=\"num\">{usd(d['value'])}</td><td>{d['as_of']}</td>"
                    f"<td>{P2.filing_link(f, esc(d['report_date']) + ' 季報') if f else esc(d['report_date']) + ' 季報'}（{esc(d['filing_date'])} 申報）{extra}{stale}</td></tr>")
    return ('<div class="imq-card blk"><h3>尚未起租的資料中心租約<span class="imq-badge">只顯示</span></h3>'
            '<div class="tbl-wrap"><table class="imq-table wrapt"><thead><tr><th>公司</th><th class="num">金額</th><th>資料日</th><th>來源</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="fine">已簽約、尚未開始計入資產負債表的租賃承諾，是還沒出現在負債裡的固定支出。各家揭露口徑不同（有的含營業與融資租賃，有的只含資料中心），金額不宜直接橫向相加。</p></div>')


def _customers(units: dict) -> str:
    u = units.get("customers")
    if not u or not u.get("data"):
        return '<div class="imq-card blk"><h3>CoreWeave 客戶集中度</h3><p class="fine">資料尚無可用值。</p></div>'
    d = u["data"]
    fl = (units.get("filings") or {}).get("data") or {}
    f = next((x for x in (fl.get("CRWV") or {}).values() if x and x.get("accession") == d.get("accession")), None)
    rows = "".join(f'<tr><td>{esc(c["label"])}</td><td class="num">{c["pct"]:.0f}%</td></tr>' for c in d["customers"])
    ya = f"；一年前同季最大客戶占 {d['year_ago_top']:.0f}%" if d.get("year_ago_top") is not None else ""
    st = "（解析失敗，沿用上次值）" if u.get("stale") else ""
    src = P2.filing_link(f, esc(d["report_date"]) + " 季報") if f else esc(d["report_date"]) + " 季報"
    return ('<div class="imq-card blk"><h3>CoreWeave 客戶集中度<span class="imq-badge">只顯示</span></h3>'
            f'<div class="tbl-wrap"><table class="imq-table"><thead><tr><th>客戶（申報檔以匿名代號揭露）</th><th class="num">占單季營收</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="fine">季度 {d["quarter_end"]}{ya}。資料來源：{src}{st}。</p></div>')


def _events(events: list[dict], total: int) -> str:
    if not events:
        return '<p class="fine">目前沒有符合關鍵字的事件。</p>'
    rows = []
    for e in events:
        if e.get("url"):
            title = f'<a href="{esc(e["url"])}" rel="noopener nofollow" target="_blank">{esc(e["title"])}</a>'
            src = esc(e.get("source") or "原文")
        else:
            title, src = esc(e["title"]), esc(e.get("source") or "—") + "（無連結）"
        rows.append(f"<tr><td>{esc(e['date'])}</td><td>{title}</td><td>{src}</td></tr>")
    return (f'<div class="tbl-wrap"><table class="imq-table wrapt"><thead><tr><th>日期</th><th>標題（可點開原文）</th><th>來源</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="fine">最近 30 筆，累計收錄 {total} 筆。</p>')


def _method() -> str:
    rows = []
    for i in range(1, 13):
        what, wrong = METHOD_ROWS[i]
        typ, _short, long = THRESH_WHY[i]
        rows.append(f"<tr><td class=\"num\">{i}</td><td>{esc(NAMES[i])}</td><td>{esc(THRESHOLD_TEXT[i])}</td><td><span class=\"imq-badge\">{typ}</span></td>"
                    f"<td>{esc(what)}</td><td>{esc(long)}</td><td>{esc(wrong)}</td></tr>")
    return ('<div class="tbl-wrap"><table class="imq-table method"><thead><tr><th class="num">條</th><th>指標</th><th>門檻</th><th>類型</th><th>代表什麼</th><th>為什麼是這個數字</th><th>可能看錯</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def _nvda_chart(units: dict, charts: P2.Charts) -> str:
    d = ((units.get("nvda_fin") or {}).get("data")) or {}
    q = d.get("quarters") or []
    if not q:
        return ""
    return charts.add("nvda_dso", [x["end"][2:7] for x in q], [{"label": "Nvidia 應收天數", "data": [round(x["dso"], 1) for x in q], "color": "navy"}], 150) + \
        '<div class="ex-src">圖：近 8 季應收帳款天數（季末應收 ÷ 單季營收 × 91）。</div>'


def build_page(state: dict, inds: list[dict], summary: dict, events: list[dict], events_total: int,
               gpu_rows: list[dict] | None = None, events_all: list[dict] | None = None) -> str:
    from site_nav import full_nav_block  # noqa: E402

    nav = full_nav_block("market", "aicredit")
    units = state["units"]
    charts = P2.Charts()
    by_group = {g: [x for x in inds if x["group"] == g] for g in GROUPS}
    n_b, n_total = summary["n_breached"], summary["n_total"]
    breached = [x for x in inds if x["breached"] is True]
    lst = "".join(f'<li><a href="#i{x["id"]}">第 {x["id"]} 條　{esc(x["name"])}</a>：{esc(x["value_text"])}（門檻 {esc(x["threshold"])}）</li>' for x in breached)
    none_line = '<p class="fine" style="margin:0">目前沒有任何一條越線。</p>' if not breached else f"<ul>{lst}</ul>"
    unknown = (f'<p class="fine" style="margin:0">另有 {summary["n_unknown"]} 條因資料不全暫不計算，不算在越線也不算在未越線。</p>' if summary["n_unknown"] else "")
    stale_names = sorted({k for k, u in units.items() if u and u.get("stale")})
    stale_html = (f'<div class="warnbar">下列資料來源本次抓取失敗，頁面沿用上次值並標明資料日期：{esc("、".join(stale_names))}。</div>' if stale_names else "")
    gen = esc(state["generated_at"])
    ev_all = events_all if events_all is not None else events

    def sec(n: str, title: str, sub: str) -> str:
        return f'<section><div class="chapter-head"><span class="ch-title">{n}　{esc(title)}</span></div><p class="ch-sub">{sub}</p>'

    sec_a = "".join(_card(x, units) for x in by_group["A"])
    sec_b = "".join(_card(x, units) for x in by_group["B"]) + _spreads((units.get("fred") or {}).get("data"), bool((units.get("fred") or {}).get("stale")))
    sec_c = ("".join(_card(x, units, _nvda_chart(units, charts) if x["id"] == 11 else "") for x in by_group["C"])
             + P2.avgo_block(units, inds) + P2.openai_block(units, ev_all) + _rpo(units, charts) + _leases(units) + _customers(units))
    sec_d = P2.igv_block(units, charts) + P2.pik_block(units, charts) + P2.software_block(units) + P2.nonaccrual_block(units)
    sec_e = P2.cloud_block(units, charts) + P2.gpu_block(units, gpu_rows or [], charts) + P2.dep_block(units)
    desc = "追蹤 AI 資料中心建設的資金是否撐得住：12 條信用與市場指標、事前登記的門檻、每日更新，越線時通知。"

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 信用風險監測 — InvestMQuest Research</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://research.investmquest.com/ai-credit/">
<meta property="og:title" content="AI 信用風險監測">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://research.investmquest.com/ai-credit/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;600;700&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/imq-base.css">
<style>{CSS}</style>
</head>
<body>
{nav}
<header class="cover"><div class="cover-inner">
  <div class="crumb"><a href="/">首頁</a> / <a href="/market/">市場</a> / AI 信用監測</div>
  <h1>AI 信用風險監測</h1>
  <div class="sub">本頁追蹤 AI 資料中心的建設資金還撐不撐得住：12 條指標各有事前登記的門檻，逐條標示越線或未越線，不合成分數；另有第二輪「只顯示」的觀察區塊，不計入越線條數。資料來源為 SEC EDGAR、Yahoo Finance、FRED 與每日早報新聞，每個交易日更新。</div>
  <div class="updated">更新時間：{gen}（台北時間）</div>
</div></header>
<div class="wrap">
{stale_html}
<div class="headline">
  <div class="imq-stat"><span class="v{' x-neg' if n_b else ''}">{n_b} / {n_total}</span><span class="k">12 條裡 <em>{n_b}</em> 條越線</span></div>
  <div>{none_line}{unknown}</div>
</div>

{sec("一", GROUPS["A"], "指標 1 至 6。看建設公司的本業現金、借款與償債能力，資料來自財報，每季更新。")}
{sec_a}</section>

{sec("二", GROUPS["B"], "指標 7 至 10。看股價與折價，反映市場當下的擔心程度；資料每日更新，BDC 淨值每季更新。")}
{sec_b}</section>

{sec("三", GROUPS["C"], "指標 11 至 12，以及供應商保證、OpenAI 曝險、未履約合約、尚未起租的租約與客戶集中度。看晶片供應商如何用保證與承諾支撐客戶的需求，以及已簽約但尚未入帳的固定支出。")}
{sec_c}</section>

{sec("四", "AI 傷到借款人：軟體業與私募信貸", "只顯示，不計入越線條數，尚未設門檻。私募信貸的借款人以軟體公司居多，AI 若削弱軟體公司的獲利，壓力會先出現在這裡。")}
{sec_d}</section>

{sec("五", "投資回不回得了本", "只顯示，不計入越線條數，尚未設門檻。看 AI 建設換來的營收追不追得上投入的資本，以及設備的剩餘價值。")}
{sec_e}</section>

<section><div class="chapter-head"><span class="ch-title">融資事件紀錄</span></div>
<p class="ch-sub">從每日早報新聞用關鍵字挑出的 AI 融資事件（資料中心、晶片、公司債、貸款、私人信用、SPV、租賃等），同網址或同標題只留一筆。</p>
<div class="imq-card blk">{_events(events, events_total)}</div></section>

<section><div class="chapter-head"><span class="ch-title">方法與門檻</span></div>
<p class="ch-sub">12 條門檻於 {REGISTERED_ON} 事前登記，之後不改。</p>
<div class="imq-card blk prose">
<p>AI 信用沒有歷史可以回測，所以門檻不是擬合出來的。結構線看狀態有沒有改變：越過去，付得起變付不起、自己賺的變主要靠借的。經驗值參考 2000 年的電信設備商與 2015 年的頁岩油。門檻在 {REGISTERED_ON} 登記後不改，就算事後看起來太鬆或太緊也不改，避免看結果調門檻。</p>
</div>
<div class="imq-card blk">{_method()}</div>
<div class="imq-card blk prose">
<h3>第二輪區塊（只顯示）</h3>
<p>第四區與第五區，以及第三區的 Broadcom 並列、OpenAI 曝險表，都只顯示，尚未設門檻，不計入 12 條的越線條數。日後若設門檻，另行登記日期，不回頭改動已登記的 12 條。</p>
<h3>這一頁的限制</h3>
<p>第 7 至 9 條用的是股價，不是信用本身。它是免費資料裡最弱的一環，股價反映的東西比信用多。</p>
<p>最可能先出事的是不上市的 SPV 與 AI 實驗室，這兩類公開資料最少。這一頁抓到的，多半是第二波。</p>
<p>資料處理：近四季一律用最新年報減去年同期累計加今年累計，不取最後四筆，因為零值季在 SEC 資料裡常常整筆缺漏。任一來源抓取失敗時沿用上次值並標示資料日期，不補數字、不以 0 代替。第 7 至 9 條的進出狀態每日存檔延續。內嵌 XBRL 的大型申報檔以申報序號快取，同一份申報只解析一次。</p>
</div></section>

<footer class="imq-foot">
  <div>© 2026 InvestMQuest Research</div>
  <div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</div>
{charts.to_script()}
</body>
</html>
"""
