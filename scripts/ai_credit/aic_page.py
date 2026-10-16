"""AI 信用風險監測頁面（docs/ai-credit/index.html）。純函式：state＋指標＋事件 → HTML 字串。"""
from __future__ import annotations

import html
import sys
from pathlib import Path

from aic_metrics import GROUPS, NAMES, REGISTERED_ON, THRESHOLD_TEXT, usd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

esc = html.escape

CSS = """
:root{--brand:#1a56db;--bg:#f9fafb;--card:#fff;--text:#111827;--muted:#6b7280;--border:#e5e7eb;--red:#b91c1c;--red-bg:#fef2f2;--ok:#047857;--ok-bg:#ecfdf5;--na:#6b7280;--amber:#92400e;--amber-bg:#fffbeb}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans TC',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1080px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.6rem 0 1.1rem;background:linear-gradient(180deg,#eff6ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.5rem;font-weight:700;letter-spacing:-.03em}
.page-hdr .sub{color:var(--muted);font-size:.92rem;margin-top:.3rem;max-width:78ch}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}.crumb a{color:var(--muted)}
.updated{font-size:.82rem;color:var(--muted);margin-top:.5rem}
.warn{background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:.6rem .9rem;margin:.8rem 0;font-size:.86rem;color:#991b1b}
.headline{margin:1.2rem 0 .2rem;background:var(--card);border:1px solid var(--border);border-radius:10px;padding:1.1rem 1.3rem}
.headline .big{font-size:1.7rem;font-weight:800;letter-spacing:-.02em}
.headline .big em{font-style:normal;color:var(--red)}
.headline ul{margin:.5rem 0 0 1.2rem;font-size:.92rem}
.headline .fine{margin-top:.5rem}
.section{padding:1.6rem 0 0}
.section-title{font-size:1.15rem;font-weight:700;margin-bottom:.4rem;padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.section-sub{font-size:.88rem;color:var(--muted);margin-bottom:.9rem}
.ind{background:var(--card);border:1px solid var(--border);border-left:5px solid var(--ok);border-radius:8px;padding:1rem 1.2rem;margin-bottom:1rem}
.ind.b{border-left-color:var(--red);background:#fffdfd}
.ind.na{border-left-color:var(--na)}
.ind-h{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap}
.ind-h .num{font-weight:800;color:var(--muted);font-variant-numeric:tabular-nums}
.ind-h h3{font-size:1.02rem;font-weight:700;flex:1;min-width:14rem}
.pill{color:#fff;font-weight:700;font-size:.8rem;border-radius:999px;padding:.1rem .8rem;background:var(--ok)}
.pill.b{background:var(--red)}.pill.na{background:var(--na)}
.kv{display:flex;gap:1.6rem;flex-wrap:wrap;margin:.6rem 0 .2rem}
.kv div{font-size:.78rem;color:var(--muted)}
.kv b{display:block;font-size:1.05rem;color:var(--text);font-variant-numeric:tabular-nums}
.kv b.val{font-size:1.35rem}
.plain{margin:.4rem 0 .6rem;font-size:.93rem;max-width:84ch}
.stale{display:inline-block;margin:.2rem 0 .4rem;font-size:.78rem;color:var(--amber);background:var(--amber-bg);border-radius:6px;padding:.1rem .5rem}
.fine{font-size:.82rem;color:var(--muted);line-height:1.7}
.tbl-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.84rem}
th,td{text-align:left;padding:.4rem .6rem;border-bottom:1px solid var(--border);vertical-align:top}
th{background:#f9fafb;font-weight:600;font-size:.74rem;color:var(--muted)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem 1.2rem;margin-bottom:1rem}
.card h3{font-size:1rem;font-weight:700;margin-bottom:.3rem}
.prose{font-size:.92rem;max-width:84ch}.prose p{margin-bottom:.7rem}
.prose ul{margin:.2rem 0 .8rem 1.2rem}.prose li{margin-bottom:.3rem}
.tag-info{font-size:.72rem;font-weight:700;color:#374151;background:#e5e7eb;border-radius:6px;padding:.1rem .5rem;margin-left:.4rem}
footer{padding:2rem 0 3rem;font-size:.8rem;color:var(--muted)}
"""


def _table(t: dict | None, num_cols: set[int] | None = None) -> str:
    if not t:
        return ""
    head = "".join(f"<th>{esc(str(h))}</th>" for h in t["head"])
    body = []
    for r in t["rows"]:
        body.append("<tr>" + "".join(f"<td>{esc(str(c))}</td>" for c in r) + "</tr>")
    return f'<div class="tbl-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def _card(x: dict) -> str:
    b = x["breached"]
    cls = "b" if b is True else ("na" if b is None else "")
    pill = "越線" if b is True else ("資料不全" if b is None else "未越線")
    stale = '<div class="stale">抓取失敗，沿用上次值；日期為原始資料日期</div>' if x.get("stale") else ""
    notes = "".join(f'<p class="fine">{esc(n)}</p>' for n in x.get("notes") or [])
    return (
        f'<div class="ind {cls}" id="i{x["id"]}"><div class="ind-h"><span class="num">{x["id"]}</span><h3>{esc(x["name"])}</h3>'
        f'<span class="pill {cls}">{pill}</span></div>'
        f'<div class="kv"><div>現值<b class="val">{esc(x["value_text"])}</b></div><div>門檻（事前登記）<b>{esc(x["threshold"])}</b></div>'
        f'<div>資料日期<b>{esc(x["date_text"])}</b></div></div>{stale}'
        f'<p class="plain">{esc(x["plain"])}</p>{_table(x.get("table"))}{notes}</div>'
    )


def _spreads(fred: dict | None, stale: bool) -> str:
    if not fred:
        return '<div class="card"><h3>背景利差（日，不計入越線條數）</h3><p class="fine">FRED 資料尚無可用值。</p></div>'
    rows = []
    for sid, s in fred.items():
        pos = "—" if s.get("pos") is None else f"{s['pos'] * 100:.0f}%"
        ago = "—" if s.get("year_ago") is None else f"{s['year_ago']:.2f}%（{s['year_ago_date']}）"
        rows.append(f"<tr><td>{esc(s['label'])}（{sid}）</td><td class=\"num\">{s['latest']:.2f}%</td><td>{s['asof']}</td>"
                    f"<td class=\"num\">{pos}</td><td class=\"num\">{s['min']:.2f}%～{s['max']:.2f}%</td><td class=\"num\">{ago}</td></tr>")
    st = '<div class="stale">抓取失敗，沿用上次值</div>' if stale else ""
    return (
        '<div class="card"><h3>背景利差（日，不計入越線條數）<span class="tag-info">只顯示</span></h3>' + st +
        '<div class="tbl-wrap"><table><thead><tr><th>系列</th><th class="num">最新</th><th>資料日</th><th class="num">三年區間位置</th>'
        '<th class="num">區間</th><th class="num">一年前</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'
        '<p class="fine">FRED 的 ICE BofA 系列只提供約三年資料，區間位置是在這三年內的相對高低（0% 最低，100% 最高），不代表長期歷史。</p></div>'
    )


def _rpo(units: dict) -> str:
    names = {"ORCL": "Oracle", "MSFT": "Microsoft", "GOOGL": "Alphabet", "CRWV": "CoreWeave"}
    rows = []
    for t, n in names.items():
        u = units.get(f"rpo:{t}")
        if not u or not u.get("data"):
            rows.append(f"<tr><td>{n}</td><td colspan=\"8\">資料尚無可用值</td></tr>")
            continue
        s = u["data"]["series"]
        cells = "".join(f'<td class="num">{usd(p["value"]).replace(" 億美元", "")}<br><span class="fine">{p["end"]}</span></td>' for p in reversed(s))
        cells += "<td></td>" * (8 - len(s))
        flag = "（沿用上次值）" if u.get("stale") else ""
        rows.append(f"<tr><td>{n}{flag}</td>{cells}</tr>")
    head = "<th>公司（單位：億美元）</th>" + "".join(f'<th class="num">{h}</th>' for h in ["最新", "前 1 季", "前 2 季", "前 3 季", "前 4 季", "前 5 季", "前 6 季", "前 7 季"])
    return ('<div class="card"><h3>未履約合約金額（RPO）近 8 季<span class="tag-info">只顯示</span></h3>'
            f'<div class="tbl-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="fine">未履約合約是已簽約、尚未認列的營收。CoreWeave 2025 年 3 月上市，季數較少。</p></div>')


def _leases(units: dict) -> str:
    order = [("MSFT", "Microsoft"), ("ORCL", "Oracle"), ("META", "Meta"), ("AMZN", "Amazon"), ("GOOGL", "Alphabet"), ("CRWV", "CoreWeave")]
    rows = []
    for t, n in order:
        u = units.get(f"lease:{t}")
        if not u or not u.get("data"):
            rows.append(f"<tr><td>{n}</td><td colspan=\"3\">資料尚無可用值</td></tr>")
            continue
        d = u["data"]
        extra = f"；期後另簽 {usd(d['subsequent'])}" if d.get("subsequent") else ""
        stale = "（解析失敗，沿用上次值）" if u.get("stale") else ""
        rows.append(f"<tr><td>{n}</td><td class=\"num\">{usd(d['value'])}</td><td>{d['as_of']}</td>"
                    f"<td>{esc(d['report_date'])} 季報（{esc(d['filing_date'])} 申報）{extra}{stale}</td></tr>")
    return ('<div class="card"><h3>尚未起租的資料中心租約<span class="tag-info">只顯示</span></h3>'
            '<div class="tbl-wrap"><table><thead><tr><th>公司</th><th class="num">金額</th><th>資料日</th><th>來源</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>'
            '<p class="fine">已簽約、尚未開始計入資產負債表的租賃承諾，是還沒出現在負債裡的固定支出。各家揭露口徑不同（有的含營業與融資租賃，有的只含資料中心），金額不宜直接橫向相加。</p></div>')


def _customers(units: dict) -> str:
    u = units.get("customers")
    if not u or not u.get("data"):
        return '<div class="card"><h3>CoreWeave 客戶集中度</h3><p class="fine">資料尚無可用值。</p></div>'
    d = u["data"]
    rows = "".join(f'<tr><td>{esc(c["label"])}</td><td class="num">{c["pct"]:.0f}%</td></tr>' for c in d["customers"])
    ya = f"；一年前同季最大客戶占 {d['year_ago_top']:.0f}%" if d.get("year_ago_top") is not None else ""
    st = "（解析失敗，沿用上次值）" if u.get("stale") else ""
    return ('<div class="card"><h3>CoreWeave 客戶集中度<span class="tag-info">只顯示</span></h3>'
            f'<div class="tbl-wrap"><table><thead><tr><th>客戶（申報檔以匿名代號揭露）</th><th class="num">占單季營收</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="fine">季度 {d["quarter_end"]}{ya}。資料來源：{esc(d["report_date"])} 季報{st}。</p></div>')


def _events(events: list[dict], total: int) -> str:
    if not events:
        return '<p class="fine">目前沒有符合關鍵字的事件。</p>'
    rows = []
    for e in events:
        title = esc(e["title"])
        link = f'<a href="{esc(e["url"])}" rel="noopener nofollow" target="_blank">{esc(e["source"] or "原文")}</a>' if e.get("url") else esc(e.get("source") or "—")
        rows.append(f"<tr><td>{esc(e['date'])}</td><td>{title}</td><td>{link}</td></tr>")
    return (f'<div class="tbl-wrap"><table><thead><tr><th>日期</th><th>標題</th><th>來源</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<p class="fine">最近 30 筆，累計收錄 {total} 筆。</p>')


METHOD_ROWS = {
    1: ("蓋資料中心的錢，本業現金流付不起，一定要對外借款或增資。",
        "股息與庫藏股同樣耗現金，這裡沒有扣；融資租賃不在資本支出裡，Microsoft 一年約 246 億美元；各家用自己最新四季，截止日不同。"),
    2: ("五家裡過半數自由現金流為負，整個族群的建設要靠債市養。",
        "Amazon 含零售業務，現金流受庫存與季節影響；單一年度為負也可能只是投資高峰。"),
    3: ("近四季建設費用超過一半來自新借的錢。",
        "用淨發債，已扣掉還款；借到的錢不一定當年花掉。各家發債 tag 不同，Alphabet 的還債標準 tag 含融資租賃本金，會讓淨發債偏低。"),
    4: ("一般產業淨負債 3.5 至 4 倍 EBITDA，約在投資等級最低一級的邊緣。被降成垃圾債，只能買投資等級債的基金會被迫賣出。",
        "3.5 倍是通用經驗值，不是評等機構寫明的 Oracle 觸發點；融資租賃與尚未起租的租約不在分子裡。"),
    5: ("高收益債的利息保障倍數低於 1.5 倍，通常落在 CCC 評等群。",
        "EBITDA 沒扣 GPU 折舊，GPU 三到五年就要換，數字比實際寬裕；用 EBITDA 是因為營業利益接近零或為負。"),
    6: ("假設停止擴建，現金加一年的本業現金流夠不夠還明年到期的債；小於 1 倍，不借新還舊就撐不過去。",
        "刻意沒扣資本支出，所以是停止擴建的情境，不是現況；已簽約、無法中止的建設支出會讓實際更緊。"),
    7: ("近三個月比 QQQ 多跌 20 個百分點，代表市場對這家公司的擔心又加重。進入（−20）與解除（−10）門檻分開，避免在邊界來回進出。",
        "股價下跌也可能只是估值修正，不一定是信用惡化。"),
    8: ("同上。", "同上。CoreWeave 2025 年 3 月才上市，歷史較短。"),
    9: ("同上。", "同上。"),
    10: ("BDC 股價明顯低於帳面淨值，代表市場不相信帳上貸款的價值。",
         "淨值每季才更新，股價每天變動，兩者日期不同；折價也可能反映對利率或股息的看法。"),
    11: ("應收帳款天數拉長，代表客戶付款變慢；Lucent 在 2000 年出事前也出現過。",
         "Nvidia 出貨集中在季底，單季天數會跳動；大客戶付款條件改變也會拉長天數。"),
    12: ("供應商對客戶的保證與融資承諾占營收比重過高，等於供應商替需求出錢。門檻依據：Lucent 1999 年底對客戶的融資承諾約 84 億美元（Lucent 10-Q），2000 財年營收 338.13 億美元（10-K405），約 25%；加上 14 億美元的客戶債務保證約 29%。",
         "保證是最大可能損失，不是已借出的錢；Nvidia 的股權投資承諾是投資，不是放款。口徑比 Lucent 寬。"),
}


def _method() -> str:
    rows = []
    for i in range(1, 13):
        what, wrong = METHOD_ROWS[i]
        rows.append(f"<tr><td class=\"num\">{i}</td><td>{esc(NAMES[i])}</td><td>{esc(THRESHOLD_TEXT[i])}</td><td>{esc(what)}</td><td>{esc(wrong)}</td></tr>")
    return (
        '<div class="tbl-wrap"><table><thead><tr><th class="num">條</th><th>指標</th><th>門檻</th><th>代表什麼</th><th>可能看錯</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def build_page(state: dict, inds: list[dict], summary: dict, events: list[dict], events_total: int) -> str:
    from site_nav import full_nav_block  # noqa: E402

    nav = full_nav_block("market", "aicredit")
    units = state["units"]
    by_group = {g: [x for x in inds if x["group"] == g] for g in GROUPS}
    n_b, n_total = summary["n_breached"], summary["n_total"]
    breached = [x for x in inds if x["breached"] is True]
    lst = "".join(f'<li><a href="#i{x["id"]}">第 {x["id"]} 條　{esc(x["name"])}</a>：{esc(x["value_text"])}（門檻 {esc(x["threshold"])}）</li>' for x in breached)
    none_line = '<p class="fine">目前沒有任何一條越線。</p>' if not breached else f"<ul>{lst}</ul>"
    unknown = (f'<p class="fine">另有 {summary["n_unknown"]} 條因資料不全暫不計算，不算在越線也不算在未越線。</p>' if summary["n_unknown"] else "")
    stale_names = sorted({k for k, u in units.items() if u and u.get("stale")})
    stale_html = (f'<div class="warn">下列資料來源本次抓取失敗，頁面沿用上次值並標明資料日期：{esc("、".join(stale_names))}。</div>' if stale_names else "")
    gen = esc(state["generated_at"])

    sec_a = "".join(_card(x) for x in by_group["A"])
    sec_b = "".join(_card(x) for x in by_group["B"]) + _spreads((units.get("fred") or {}).get("data"), bool((units.get("fred") or {}).get("stale")))
    sec_c = "".join(_card(x) for x in by_group["C"]) + _rpo(units) + _leases(units) + _customers(units)
    desc = "追蹤 AI 資料中心建設的資金是否撐得住：12 條信用與市場指標、事前登記的門檻、每日更新，越線時通知。"

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 信用風險監測 | InvestMQuest</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://research.investmquest.com/ai-credit/">
<meta property="og:title" content="AI 信用風險監測">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://research.investmquest.com/ai-credit/">
<style>{CSS}</style>
</head>
<body>
{nav}
<div class="page-hdr"><div class="container">
  <div class="crumb"><a href="/">首頁</a> / <a href="/monitor/">市場監測</a> / AI 信用風險監測</div>
  <h1>AI 信用風險監測</h1>
  <div class="sub">這一頁看 AI 資料中心的建設資金還撐不撐得住。12 條指標各有事前登記的門檻，逐條標示越線或未越線，不合成分數。每個交易日更新。</div>
  <div class="updated">更新時間：{gen}（台北時間）　資料來源：SEC EDGAR、Yahoo Finance、FRED、每日早報新聞</div>
</div></div>
<div class="container">
{stale_html}
<div class="headline">
  <div class="big">12 條裡 <em>{n_b}</em> 條越線</div>
  {none_line}
  {unknown}
</div>

<div class="section"><div class="section-title">第一區　{esc(GROUPS["A"])}</div>
<div class="section-sub">指標 1 至 6。看建設公司的本業現金、借款與償債能力，資料來自財報，每季更新。</div>
{sec_a}</div>

<div class="section"><div class="section-title">第二區　{esc(GROUPS["B"])}</div>
<div class="section-sub">指標 7 至 10。看股價與折價，反映市場當下的擔心程度；資料每日更新，BDC 淨值每季更新。</div>
{sec_b}</div>

<div class="section"><div class="section-title">第三區　{esc(GROUPS["C"])}</div>
<div class="section-sub">指標 11 至 12。看晶片供應商如何用保證與承諾支撐客戶的需求，以及已簽約但尚未入帳的固定支出。</div>
{sec_c}</div>

<div class="section"><div class="section-title">融資事件紀錄</div>
<div class="section-sub">從每日早報新聞用關鍵字挑出的 AI 融資事件（資料中心、晶片、公司債、貸款、私人信用、SPV、租賃等），同網址或同標題只留一筆。</div>
<div class="card">{_events(events, events_total)}</div></div>

<div class="section"><div class="section-title">方法與門檻</div>
<div class="section-sub">12 條門檻於 {REGISTERED_ON} 事前登記，之後不改。</div>
<div class="card">{_method()}</div>
<div class="card prose">
<h3>這一頁的限制</h3>
<p>AI 信用沒有可回測的歷史，所以門檻是結構線或經驗值，不是用資料擬合出來的。可類比的前例是 2000 年的電信設備商與 2015 年的頁岩油。</p>
<p>第 7 至 9 條用的是股價，不是信用本身。它是免費資料裡最弱的一環，股價反映的東西比信用多。</p>
<p>最可能先出事的是不上市的 SPV 與 AI 實驗室，這兩類公開資料最少。這一頁抓到的，多半是第二波。</p>
<p>資料處理：近四季一律用最新年報減去年同期累計加今年累計，不取最後四筆，因為零值季在 SEC 資料裡常常整筆缺漏。任一來源抓取失敗時沿用上次值並標示資料日期，不補數字、不以 0 代替。第 7 至 9 條的進出狀態每日存檔延續。</p>
</div></div>

<footer><div><a href="/disclosures.html">方法論與揭露</a> · 本站內容僅供研究參考，不構成投資建議</div></footer>
</div>
</body>
</html>
"""
