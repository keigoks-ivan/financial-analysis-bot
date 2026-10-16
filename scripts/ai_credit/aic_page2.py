"""第二輪四區的頁面片段（只顯示，不計入越線條數）。純函式：units＋歷史列 → HTML 字串。

顏色一律用 imq-base.css 的 token（--pos／--neg／--warn 與頁面沿用 etf-dash 的 --x-* 圖表色）；
圖表用 Chart.js 小圖，資料由 Charts 物件收集後在頁尾一次輸出。
"""
from __future__ import annotations

import html
import json

import aic_round2 as R
from aic_metrics import usd

esc = html.escape
SEC_BROWSE = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik:010d}&type=10-&dateb=&owner=include&count=40"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
CO_NAME = {"MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "META": "Meta", "ORCL": "Oracle", "CRWV": "CoreWeave",
           "NVDA": "Nvidia", "AVGO": "Broadcom", "AMD": "AMD"}
CO_NAME.update(R.BDC_NAME)


class Charts:
    """收集頁面上的小圖資料。add() 回傳 canvas 的 HTML；to_script() 輸出資料與繪圖程式。"""

    def __init__(self) -> None:
        self.data: dict[str, dict] = {}

    def add(self, cid: str, labels: list[str], series: list[dict], height: int = 180, ref: float | None = None, fmt: str = "") -> str:
        self.data[cid] = {"labels": labels, "series": series, "ref": ref, "fmt": fmt}
        return f'<div class="chart-box" style="height:{height}px"><canvas data-chart="{cid}"></canvas></div>'

    def to_script(self) -> str:
        if not self.data:
            return ""
        return ("<script src=\"https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js\"></script>\n<script>\n"
                f"var CHARTS={json.dumps(self.data, ensure_ascii=False, separators=(',', ':'))};\n" + CHART_JS + "\n</script>")


CHART_JS = """
(function(){
function cssVar(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim();}
if(typeof Chart==='undefined'){return;}
var COL={navy:cssVar('--x-navy'),gold:cssVar('--gold-deep'),blue:cssVar('--x-blue'),teal:cssVar('--x-teal'),sky:cssVar('--x-sky'),grey:cssVar('--x-grey'),muted:cssVar('--muted'),sec:cssVar('--sec'),line:cssVar('--line')};
document.querySelectorAll('canvas[data-chart]').forEach(function(cv){
  var c=CHARTS[cv.getAttribute('data-chart')]; if(!c){return;}
  var ds=c.series.map(function(s){return {label:s.label,data:s.data,borderColor:COL[s.color]||COL.navy,backgroundColor:COL[s.color]||COL.navy,pointRadius:s.points?2.5:0,borderWidth:1.6,spanGaps:true,tension:0,borderDash:s.dash?[5,4]:[]};});
  if(c.ref!==null&&c.ref!==undefined){ds.push({label:'基準 '+c.ref,data:c.labels.map(function(){return c.ref;}),borderColor:COL.muted,borderDash:[4,3],borderWidth:1,pointRadius:0});}
  new Chart(cv,{type:'line',data:{labels:c.labels,datasets:ds},options:{responsive:true,maintainAspectRatio:false,
    scales:{x:{ticks:{color:COL.muted,font:{size:9},maxTicksLimit:6},grid:{display:false}},y:{ticks:{color:COL.muted,font:{size:9}},grid:{color:COL.line}}},
    plugins:{legend:{display:c.series.length>1,position:'bottom',labels:{color:COL.sec,font:{size:10},boxWidth:12}}}}});
});
})();
"""


def _table(head: list[str], rows: list[list[str]], num_cols: set[int] | None = None, raw: bool = False, wrap: bool = False) -> str:
    num_cols = num_cols or set()
    th = "".join(f'<th class="{"num" if i in num_cols else ""}">{h if raw else esc(h)}</th>' for i, h in enumerate(head))
    body = "".join("<tr>" + "".join(f'<td class="{"num" if i in num_cols else ""}">{c if raw else esc(str(c))}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tbl-wrap"><table class="imq-table{" wrapt" if wrap else ""}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def link(url: str | None, text: str) -> str:
    if not url:
        return esc(text)
    return f'<a href="{esc(url)}" rel="noopener" target="_blank">{esc(text)}</a>'


def filing_link(f: dict | None, label: str | None = None) -> str:
    """申報檔 → 「10-Q（截止日）」連結。"""
    if not f:
        return "—"
    return link(f.get("url"), label or f"{f['form']}（{f['report_date']}）")


def cik_of(t: str) -> int:
    import sec_facts as S
    return S.CIKS[t]


def sec_sources(units: dict, tickers: list[str], facts: bool = True) -> str:
    """每家公司：最新 10-Q、10-K 與 XBRL 資料（companyfacts）連結。"""
    fl = (units.get("filings") or {}).get("data") or {}
    parts = []
    for t in tickers:
        f = fl.get(t) or {}
        bits = [filing_link(f.get("10-Q")), filing_link(f.get("10-K"))]
        bits = [b for b in bits if b != "—"]
        if facts:
            bits.append(link(FACTS_URL.format(cik=cik_of(t)), "XBRL 資料"))
        parts.append(f"{esc(CO_NAME.get(t, t))}：" + "、".join(bits))
    return "；".join(parts)


def _stale(u: dict | None, text: str = "抓取失敗，沿用上次值") -> str:
    return f'<span class="imq-badge warn">{esc(text)}（{esc((u or {}).get("fetched", ""))}）</span>' if u and u.get("stale") else ""


def _ex(label: str, title: str, sub: str = "") -> str:
    s = f'<div class="ex-sub">{sub}</div>' if sub else ""
    return f'<div class="exhibit"><div class="ex-label">{esc(label)}</div><div class="ex-title">{esc(title)}</div>{s}</div>'


_MON = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])}


def _cn_date(s: str) -> str:
    """'May 31, 2031' → '2031-05-31'；'October 2030' → '2030 年 10 月'；其他原樣。"""
    import re
    m = re.match(r"([A-Za-z]+) (\d{1,2}), (\d{4})$", s.strip())
    if m and m.group(1) in _MON:
        return f"{m.group(3)}-{_MON[m.group(1)]:02d}-{int(m.group(2)):02d}"
    m = re.match(r"([A-Za-z]+) (\d{4})$", s.strip())
    if m and m.group(1) in _MON:
        return f"{m.group(2)} 年 {_MON[m.group(1)]} 月"
    return s


def latest_filing(units: dict, t: str) -> dict | None:
    """最近一份 10-Q／10-K（以截止日較晚者為準）。"""
    fl = ((units.get("filings") or {}).get("data") or {}).get(t) or {}
    c = [f for f in (fl.get("10-Q"), fl.get("10-K")) if f]
    return max(c, key=lambda f: f["report_date"]) if c else None


def _fmt_pct(x: float | None, nd: int = 1) -> str:
    return "—" if x is None else f"{x:.{nd}f}%"


# ---------------------------------------------------------------------------
# 第三區補充：Broadcom 與 Nvidia 並列、OpenAI 曝險表
# ---------------------------------------------------------------------------
def avgo_block(units: dict, inds: list[dict]) -> str:
    u = units.get("avgo")
    a = (u or {}).get("data")
    nv = next((x for x in inds if x["id"] == 12), None)
    nvu = (units.get("nvda_fin") or {}).get("data")
    nvc = (units.get("nvda_commit") or {}).get("data")
    if not a:
        return '<div class="imq-card blk"><h3>Broadcom 對客戶的保證與可轉債額度</h3><p class="fine">資料尚無可用值。</p></div>'
    num = a["guarantee"] + a["convertible"]
    r = num / a["rev_ttm"]
    rows = []
    if nvu and nvc:
        nsum = nvu["guarantee"] + nvc["ai_cloud"] + nvc["equity"]
        rows.append(["Nvidia", usd(nvu["guarantee"]), f"{usd(nvc['ai_cloud'])}（AI 雲端夥伴承諾）＋{usd(nvc['equity'])}（股權投資承諾）", usd(nsum),
                     usd(nvu["rev_ttm"]), f"{nsum / nvu['rev_ttm'] * 100:.1f}%", nvu["guarantee_date"] if nvu["guarantee_date"] == nvc["report_date"] else f"{nvu['guarantee_date']}／{nvc['report_date']}"])
    rows.append(["Broadcom", usd(a["guarantee"]), f"{usd(a['convertible'])}（客戶可向 Broadcom 發行的可轉換本票額度，" + ("目前未動用）" if not a.get("drawn") else f"已動用 {usd(a['drawn'])}）"), usd(num),
                 usd(a["rev_ttm"]), f"{r * 100:.1f}%", a["guarantee_date"]])
    tbl = _table(["公司", "對客戶的保證（最大可能損失）", "承諾與額度", "合計", "近四季營收", "合計 ÷ 近四季營收", "資料日"], rows, {1, 3, 4, 5}, wrap=True)
    txt = (f"Broadcom 在 {esc(a['report_date'])} 季報揭露兩項：為客戶的 AI 機架租約對金融夥伴出具後盾（backstop），全部機架部署後的最大可能責任約 {usd(a['guarantee'])}（客戶違約時，補足租約未付金額的 85% 與機架處分價值之間的差額）；"
           f"客戶在特定條件下可向 Broadcom 發行最多 {usd(a['convertible'])}的可轉換本票，只能用於清償該租約義務，" + ("目前未動用。" if not a.get("drawn") else f"已動用 {usd(a['drawn'])}。") + f"兩項加總占近四季營收 {r * 100:.1f}%，只顯示，不計入第 12 條。"
           f"財報沒有點名客戶。未履約合約（RPO）為 {usd(a['rpo'])}（{esc(a['rpo_date'])}）。")
    src = f'<p class="src">來源：{link(a["url"], "Broadcom " + a["form"] + "（" + a["report_date"] + "）")}、{link(FACTS_URL.format(cik=cik_of("AVGO")), "XBRL 資料")}。Nvidia 數字見第 12 條。</p>'
    return f'<div class="imq-card blk"><h3>供應商替客戶出錢：Nvidia 與 Broadcom 並列<span class="imq-badge">只顯示</span></h3>{_stale(u)}<p class="plain">{txt}</p>{tbl}{src}</div>'


def _news_for(events: list[dict], co_rx: tuple[str, ...]) -> str | None:
    out = []
    for e in events:
        t = e["title"].lower()
        if "openai" in t and any(c in t for c in co_rx):
            out.append(f'{esc(e["date"])} {link(e.get("url"), e["title"])}（{esc(e.get("source") or "")}）')
    return "<br>".join(out[:5]) if out else None


def openai_block(units: dict, events: list[dict]) -> str:
    def recs(t):
        d = (units.get(f"oa:{t}") or {}).get("data") or {}
        return sorted(d.get("filings", []), key=lambda f: f["filing_date"], reverse=True)

    def top(t):
        r = recs(t)
        return r[0] if r else None

    rows: list[list[str]] = []

    def add(co, item, val, asof, f):
        rows.append([esc(co), item, val, esc(asof), filing_link(f)])

    m = top("MSFT")
    p = (m or {}).get("parsed")
    if p:
        add("Microsoft", "持有 OpenAI 股權（權益法）", f"約 {p['ownership_pct']:.0f}%", p["own_date"], m)
        sh = f"，占 Microsoft 總營收 {p['rev_share_pct']:.1f}%" if p.get("rev_share_pct") is not None else ""
        add("Microsoft", "來自 OpenAI 的營收", f"{usd(p['rev'])}{sh}", f"{p['rev_start']}～{p['rev_end']}", m)
        add("Microsoft", "對 OpenAI 的應收帳款", usd(p["ar"]), p["ar_date"], m)
        add("Microsoft", "出資承諾／已出資", f"{usd(p['commit'])}／{usd(p['funded'])}", p["commit_date"], m)
        if p.get("gain") is not None:
            add("Microsoft", "OpenAI 相關投資損益（其他收益費用）", f"{p['gain'] / 1e8:+,.1f} 億美元", f"{p['gain_start']}～{p['gain_end']}", m)
    else:
        add("Microsoft", "OpenAI 曝險", "本期未解析，沿用上次值或見申報檔", "—", m)
    n = top("NVDA")
    p = (n or {}).get("parsed")
    if p:
        life = f"、租期 {p['lease_years']} 年" if p.get("lease_years") else ""
        add("Nvidia", "為 SB Energy 租約出具的保證（承租人為 OpenAI 的關聯公司）", f"上限 {usd(p['cap'])}；約 {p['gw']:g} GW 資料中心容量{life}",
            f"{n['report_date']} 季報（保證 2026-08 簽訂）", n)
    a = top("AMZN")
    p = (a or {}).get("parsed")
    if p:
        yrs = f"（{p['aws_years']:g} 年）" if p.get("aws_years") else ""
        add("Amazon", "OpenAI 對 AWS 的承諾", f"原有 {usd(p['aws_commit'])}；{p['aws_increase_start'][:4]} 年第一季再增加 {usd(p['aws_increase'])}{yrs}", p["aws_commit_date"], a)
        extra = ""
        if p.get("invested_total"):
            extra = f"；至 {a['report_date']} 累計已投資 {usd(p['invested_total'])}"
        if p.get("invested_after"):
            extra += f"，期後再投 {usd(p['invested_after'])}"
        add("Amazon", "Amazon 對 OpenAI 的投資（Series C 特別股）", f"首筆 {usd(p['invested_first'])}；另承諾 {usd(p['commitment'])}{extra}", a["report_date"], a)
    d = top("AMD")
    p = (d or {}).get("parsed")
    if p:
        vt = p.get("vested_text") or ""
        v = f"；截至 {d['report_date']}，尚無任何批次歸屬" if "no warrant tranches had vested" in vt else (f"；{esc(vt)}" if vt else "")
        add("AMD", "給 OpenAI 的認股權證", f"最多 {p['shares_m']} 百萬股、行使價 ${p['strike']:g}，依 GPU 採購里程碑與股價門檻分批歸屬{v}", d["report_date"], d)
    # CoreWeave
    cr = recs("CRWV")
    seen = set()
    for f in cr:
        for c in ((f.get("parsed") or {}).get("contracts") or []):
            k = (c["amount"], c["through"])
            if k in seen:
                continue
            seen.add(k)
            add("CoreWeave", "OpenAI 承諾支付的合約上限", f"{usd(c['amount'])}，期限至 {esc(_cn_date(c['through']))}", f["report_date"], f)
    nw = _news_for(events, ("coreweave",))
    if nw:
        rows.append(["CoreWeave", "相關新聞（事件紀錄，不取數字）", nw, "—", "—"])
    for t in ("ORCL", "AVGO"):
        rs = recs(t)
        if rs:
            hit = "；".join(f"{f['form']}（{f['report_date']}）{f['mentions']} 次" for f in rs)
            rows.append([CO_NAME[t], "財報未揭露 OpenAI 相關金額", f"最新 10-Q 與 10-K 全文搜尋「OpenAI」：{esc(hit)}", esc(rs[0]["report_date"]),
                         " ".join(filing_link(f) for f in rs)])
        else:
            rows.append([CO_NAME[t], "財報未揭露 OpenAI 相關金額", "資料尚無可用值", "—", "—"])
        nw = _news_for(events, ("oracle",) if t == "ORCL" else ("broadcom", "avgo"))
        if nw:
            rows.append([CO_NAME[t], "相關新聞（事件紀錄，不取數字）", nw, "—", "—"])
    stale = "".join(_stale(units.get(f"oa:{t}")) for t in ("MSFT", "NVDA", "AMZN", "AMD", "CRWV", "ORCL", "AVGO"))
    tbl = _table(["公司", "項目", "數字", "截止日", "申報檔"], rows, raw=True, wrap=True)
    note = ('<p class="fine">只放財報有寫的數字，每格標申報檔與截止日，不從新聞補數字。各家口徑不同，不宜加總。'
            'Microsoft、Amazon、AMD 的數字取自內嵌 XBRL 與申報檔文字；Oracle 與 Broadcom 的財報全文沒有出現 OpenAI 一詞。</p>')
    return (f'<div class="imq-card blk"><h3>OpenAI 曝險：誰的財報寫了多少<span class="imq-badge">只顯示</span></h3>{stale}'
            f'<p class="plain">OpenAI 是未上市公司，沒有自己的信用資料。它的曝險只能從供應商與客戶的財報側面看：誰持股、誰簽了長約、誰替它的租約擔保。</p>{tbl}{note}</div>')


# ---------------------------------------------------------------------------
# 四、AI 傷到借款人
# ---------------------------------------------------------------------------
def igv_block(units: dict, charts: Charts) -> str:
    u = units.get("igv")
    d = (u or {}).get("data")
    if not d:
        return '<div class="imq-card blk"><h3>軟體業股價（IGV）對 QQQ</h3><p class="fine">資料尚無可用值。</p></div>'
    ch = d["chart"]
    chart = charts.add("igv", [c[0] for c in ch], [{"label": "IGV（起點 = 100）", "data": [c[1] for c in ch], "color": "navy"},
                                                  {"label": "QQQ（起點 = 100）", "data": [c[2] for c in ch], "color": "gold"}], 190)
    cls = lambda v: "x-pos" if v >= 0 else "x-neg"  # noqa: E731
    stats = (f'<div class="stat-row"><div class="imq-stat"><span class="v {cls(d["rel_pp"])}">{d["rel_pp"]:+.1f} 個百分點</span><span class="k">近 63 日報酬減 QQQ</span></div>'
             f'<div class="imq-stat"><span class="v {cls(d["rel_dd_1y"])}">{d["rel_dd_1y"]:.1f}%</span><span class="k">IGV ÷ QQQ 一年相對回撤</span></div>'
             f'<div class="imq-stat"><span class="v {cls(d["own_dd_1y"])}">{d["own_dd_1y"]:.1f}%</span><span class="k">IGV 自己一年回撤</span></div>'
             f'<div class="imq-stat"><span class="v">{esc(d["asof"])}</span><span class="k">資料日</span></div></div>')
    txt = ("私募信貸的借款人有相當比重是軟體公司。AI 若削弱軟體業的獲利，這些貸款會先受影響；軟體股價相對 QQQ 的表現，是市場對這件事的每日定價。"
           "相對回撤是 IGV 對 QQQ 的比值離近一年高點的距離，比單看 63 日報酬更能看出累積的落後幅度。")
    src = f'<p class="src">來源：{link("https://finance.yahoo.com/quote/IGV/history", "Yahoo Finance IGV")}、{link("https://finance.yahoo.com/quote/QQQ/history", "QQQ")}（還原收盤價）。圖每週取一點。</p>'
    return (f'<div class="imq-card blk"><h3>軟體業股價（IGV）對 QQQ<span class="imq-badge">只顯示</span></h3>{_stale(u)}<p class="plain">{txt}</p>{stats}{chart}{src}</div>')


def pik_block(units: dict, charts: Charts) -> str:
    cells, rows, latest = [], [], []
    ends_all: list[str] = []
    for t in R.BDC_ALL:
        u = units.get(f"pik:{t}")
        d = (u or {}).get("data")
        if not d:
            cells.append(f'<div class="mini"><div class="mini-h">{t}</div><p class="fine">資料尚無可用值</p></div>')
            continue
        s = d["series"]
        ends_all = [x["end"] for x in s] if len(s) > len(ends_all) else ends_all
        chart = charts.add(f"pik_{t}", [x["end"][2:7] for x in s], [{"label": f"{t} 實物付息占比（%）", "data": [round(x["pct"], 1) for x in s], "color": "navy"}], 90)
        cells.append(f'<div class="mini"><div class="mini-h">{t}<span>{s[-1]["pct"]:.1f}%</span></div>{chart}</div>')
        rows.append([f"{t}（{R.BDC_NAME[t]}）"] + [("—" if x["pct"] is None else f"{x['pct']:.1f}%") for x in s[-8:]] + [d["note"]])
    head = ["BDC"] + [e[2:7] for e in ends_all[-8:]] + ["口徑"]
    tbl = _table(head, rows, set(range(1, 9)), wrap=True)
    txt = ("BDC 的利息有一部分不是收現金，而是把利息加進本金（實物付息，PIK）。占比上升，代表借款人付不出現金利息。"
           "各家對 PIK 的定義與計算口徑不同，所以只看各家自己的趨勢，不比水平高低。")
    return (f'<div class="imq-card blk"><h3>BDC 實物付息占總投資收益（近 8 季）<span class="imq-badge">只顯示</span></h3>{"".join(_stale(units.get(f"pik:{t}")) for t in R.BDC_ALL)}'
            f'<p class="plain">{txt}</p><div class="mini-grid">{"".join(cells)}</div>'
            f'<details><summary>明細與各家口徑</summary>{tbl}<p class="fine">分母為總投資收益（GrossInvestmentIncomeOperating）；ARCC、GBDC、BBDC 的分子含股利的實物付息。'
            f'OBDC 的合併 tag 季值不可靠，改用利息實物付息；BXSL 與 MAIN 的 companyfacts 沒有值，改解析內嵌 XBRL。季別為日曆季末，GBDC、OCSL 的財年在 9 月結。</p>'
            f'<p class="src">來源：{sec_sources(units, R.BDC_ALL)}</p></details></div>')


def _na_row(t: str, la: dict) -> list[str]:
    v = la.get("value")
    if la["status"] == "none":
        return [f"{t}（{R.BDC_NAME[t]}）", "—", "—", esc(R.NONACCRUAL_BASIS[t]), "本期未抓到，且沒有上次值", filing_link({"url": la.get("miss_url"), "form": "申報檔", "report_date": la.get("miss_report_date", "")})]
    cost = "—" if v.get("cost") is None else f"{v['cost']:.1f}%"
    fv = "—" if v.get("fv") is None else f"{v['fv']:.1f}%"
    state = "最新" if la["status"] == "ok" else f"本期（{la.get('miss_report_date')}）未抓到，顯示上次值"
    return [f"{t}（{R.BDC_NAME[t]}）", cost, fv, esc(R.NONACCRUAL_BASIS[t]), f"{la['report_date']}（{state}）",
            filing_link({"url": la["url"], "form": "10-Q／10-K", "report_date": la["report_date"]}, f"申報檔 {la['report_date']}")]


def bdc_filings(units: dict, t: str) -> list[dict]:
    d = (units.get(f"bdcf:{t}") or {}).get("data") or {}
    return sorted(d.get("filings", []), key=lambda f: f["report_date"], reverse=True)


def software_block(units: dict) -> str:
    rows = []
    for t in R.SOFTWARE_MEMBERS:
        fs = bdc_filings(units, t)
        cur = next((f for f in fs if f.get("software")), None)
        if not cur:
            rows.append([f"{t}（{R.BDC_NAME[t]}）", "—", "—", "—", R.SOFTWARE_NOTE[t], "本期未抓到"])
            continue
        prev = next((f for f in fs if f is not cur and f.get("software")), None)
        sw = cur["software"]
        rows.append([f"{t}（{R.BDC_NAME[t]}）", f"{sw['pct']:.1f}%", "—" if not prev else f"{prev['software']['pct']:.1f}%（{prev['software']['asof']}）",
                     f"{sw['total_pct']:.0f}%（{sw['n_industries']} 個產業）", R.SOFTWARE_NOTE[t],
                     f"{filing_link(cur, '申報檔 ' + cur['report_date'])}（{sw['asof']}）"])
    tbl = _table(["BDC", "軟體業占比（公允價值）", "上一季", "各產業加總（自檢）", "「軟體」算哪些成員", "來源（資料日）"], rows, {1, 2, 3}, raw=True, wrap=True)
    txt = ("BDC 的產業分布以公允價值占比揭露。軟體業是私募信貸最大的單一產業之一，占比越高，AI 對軟體公司的衝擊就越直接傳到這些基金。"
           "各家的產業分類名稱不同，頁面逐家寫明「軟體」算哪些成員；各產業加總應接近 100%，用來檢查有沒有漏項。")
    return f'<div class="imq-card blk"><h3>BDC 的軟體業占比<span class="imq-badge">只顯示</span></h3><p class="plain">{txt}</p>{tbl}</div>'


def nonaccrual_block(units: dict) -> str:
    rows = []
    for t in ("ARCC", "OBDC", "BXSL", "FSK", "MAIN", "GBDC"):
        rows.append(_na_row(t, R.latest_nonaccrual(bdc_filings(units, t))))
    tbl = _table(["BDC", "占總投資（成本）", "占總投資（公允價值）", "各家揭露口徑", "資料日", "來源"], rows, {1, 2}, raw=True, wrap=True)
    txt = ("不計息貸款是借款人已停止付息、BDC 不再認列利息收入的貸款，是信用惡化最直接的訊號。成本口徑反映當初放出去的錢，公允價值口徑已扣掉帳面減損，"
           "兩者差距越大，代表已經認列的損失越多。各家只給其中一種或兩種，有哪個列哪個。")
    return f'<div class="imq-card blk"><h3>BDC 不計息貸款<span class="imq-badge">只顯示</span></h3><p class="plain">{txt}</p>{tbl}<p class="fine">ARCC 取自 XBRL 標籤，其餘取自 10-Q 文字。抓不到時顯示上次值與日期，並通知。</p></div>'


# ---------------------------------------------------------------------------
# 五、投資回不回得了本
# ---------------------------------------------------------------------------
def cloud_block(units: dict, charts: Charts) -> str:
    order = [("AWS", "AWS", "navy"), ("AWS", "AWS_SEG", "sky"), ("GCP", "GCP", "teal"), ("MSIC", "MSIC", "blue"), ("ORCL", "ORCL_CLOUD", "gold"), ("ORCL", "ORCL_IAAS", "grey")]
    sumrows, srcs, st = [], [], ""
    labels = None
    series = []
    for key, line, color in order:
        u = units.get(f"croi:{key}")
        d = (u or {}).get("data")
        if u:
            st += _stale(u)
        if not d or line not in d["lines"]:
            continue
        ln = d["lines"][line]
        if labels is None or len(ln["rows"]) > len(labels):
            labels = [r["end"][2:7] for r in ln["rows"]]
        sumrows.append([ln["label"], "—" if ln["ttm"] is None else f"{ln['ttm']:.2f}", usd(ln["ttm_rev"]), usd(ln["ttm_capex"]) if ln["ttm_capex"] else "—",
                        f"{ln['rows'][-1]['end']}"])
        pad = [None] * (len(labels) - len(ln["rows"]))
        series.append({"label": ln["label"], "data": pad + [None if r["ratio"] is None else round(r["ratio"], 2) for r in ln["rows"]], "color": color,
                       "dash": line in ("AWS_SEG", "ORCL_IAAS")})
    tbl = _table(["雲端業務", "近四季 營收 ÷ 資本支出", "近四季營收", "近四季資本支出", "最新季末"], sumrows, {1, 2, 3}) if sumrows else '<p class="fine">資料尚無可用值。</p>'
    chart = charts.add("cloud_roi", labels, series, 220, ref=1.0) if series else ""
    # 8 季明細
    drows = []
    for key, line, _c in order:
        d = ((units.get(f"croi:{key}") or {}).get("data") or {}).get("lines", {}).get(line)
        if d:
            drows.append([d["label"]] + ["—" if r["ratio"] is None else f"{r['ratio']:.2f}" for r in d["rows"]])
    dh = ["業務"] + (labels or [])
    detail = _table(dh, drows, set(range(1, 9))) if drows else ""
    fl = (units.get("filings") or {}).get("data") or {}
    srcs = "；".join(f"{CO_NAME[t]}：{filing_link((fl.get(t) or {}).get('10-Q'))}、{filing_link((fl.get(t) or {}).get('10-K'))}、{link(FACTS_URL.format(cik=cik_of(t)), 'XBRL 資料')}"
                     for t in ("AMZN", "GOOGL", "MSFT", "ORCL"))
    txt = ("比值是單季雲端營收除以同季資本支出，大於 1 代表一年的雲端營收超過同期投入的資本支出。AI 建設期間，資本支出領先營收，比值低於 1 是預期中的狀態；"
           "要看的是比值是否隨營收放量回升，還是持續下滑。")
    note = ("<p class=\"fine\">分母是全公司資本支出（現金流量表購置固定資產），不含融資租賃；唯一例外是 AWS 另列一條，分母改用 AWS 分部的資本支出（含融資租賃與應付未付）。"
            "Google Cloud 與 Microsoft Intelligent Cloud 的分子是分部營收，分母卻是全公司資本支出，所以比值偏低；Microsoft Intelligent Cloud 含非 Azure 業務（伺服器產品、企業服務），"
            "且 FY2025 分部經過重編，這裡只用新口徑。Oracle 雲端為 Cloud revenues，另列雲端基礎設施（IaaS）。Oracle 財年於 5 月結。</p>")
    return (f'<div class="imq-card blk"><h3>雲端營收 ÷ 資本支出<span class="imq-badge">只顯示</span></h3>{st}<p class="plain">{txt}</p>{tbl}{chart}'
            f'<div class="ex-src">圖：近 8 季單季比值，虛線為基準 1.0；AWS 分部與 Oracle IaaS 為虛線。</div>'
            f'<details><summary>8 季明細</summary>{detail}</details>{note}<p class="src">來源：{srcs}</p></div>')


def gpu_block(units: dict, rows: list[dict], charts: Charts) -> str:
    uv, us = units.get("gpu_vast"), units.get("gpu_shade")
    dv, ds = (uv or {}).get("data"), (us or {}).get("data")
    trs = []
    for m in R.GPU_MODELS:
        v = (dv or {}).get(m)
        s = (ds or {}).get(m)
        f = lambda x: "—" if x is None else f"${x:.2f}"  # noqa: E731
        trs.append([m, f(v and v["rentable_median"]), "—" if not v else str(v["rentable_n"]), f(v and v["all_median"]), "—" if not v else str(v["all_n"]),
                    f(s and s["avail_median"]), "—" if not s else str(s["avail_n"]), f(s and s["all_median"]), "—" if not s else str(s["all_n"])])
    tbl = _table(["型號", "vast.ai 可租中位數", "筆數", "vast.ai 含已租中位數", "筆數", "Shadeform 有庫存中位數", "型號數", "Shadeform 全部標價中位數", "型號數"], trs, set(range(1, 9)))
    dates = []
    if uv:
        dates.append(f"vast.ai 資料日 {uv.get('fetched', '—')}")
    if us:
        dates.append(f"Shadeform 資料日 {us.get('fetched', '—')}")
    n_days = len(rows)
    first = rows[0]["date"] if rows else None
    chart = ""
    if n_days >= 5:
        labels = [r["date"][5:] for r in rows]
        series = [{"label": f"{m}（vast.ai 可租）", "data": [((r.get("vast") or {}).get(m) or {}).get("rentable_median") for r in rows], "color": c}
                  for m, c in (("H100", "navy"), ("H200", "blue"), ("B200", "gold"), ("A100", "teal"))]
        chart = charts.add("gpu", labels, [{**s, "data": [None if x is None else round(x, 3) for x in s["data"]]} for s in series], 200)
        chart += '<div class="ex-src">圖：vast.ai 可租中位數，每 GPU 每小時（美元）。</div>'
    else:
        chart = f'<p class="fine">每日記錄，首筆快照 {first or "尚未產生"}，目前累積 {n_days} 天；累積到 5 天以上才畫圖。不回補歷史。</p>'
    txt = ("GPU 的二手租價反映這批設備的剩餘價值：租價若快速下滑，用 GPU 當抵押的貸款與帳上折舊年限都會被質疑。"
           "這裡每日記錄 H100、H200、B200、B300、A100 的每 GPU 每小時租價。")
    note = ("<p class=\"fine\">vast.ai 是點對點市集，價格由出租者自訂，「可租」是目前未被租走的報價，「含已租」另含已租出者的標價；單一查詢回傳上限 64 筆，程式依價格區間切段取全。"
            "Shadeform 為標價而非成交價（hourly_price 單位為美分，已除以 GPU 數與 100），有庫存指任一地區可立即部署。"
            "兩者都是非官方公開端點，抓取失敗時沿用上次值並標日期。H100 含 SXM、PCIe、NVL，A100 含各版本，型號內規格不同價格有差。</p>")
    return (f'<div class="imq-card blk"><h3>GPU 租價（每日快照）<span class="imq-badge">只顯示</span></h3>{_stale(uv)}{_stale(us)}<p class="plain">{txt}</p>{tbl}'
            f'<div class="ex-src">{esc("；".join(dates)) or "資料尚無可用值"}；單位：美元每 GPU 每小時。</div>{chart}{note}'
            f'<p class="src">來源：{link("https://console.vast.ai/", "vast.ai 公開市集 API")}、{link("https://www.shadeform.ai/", "Shadeform 公開型號 API")}。</p></div>')


def dep_block(units: dict) -> str:
    u = units.get("dep")
    parsed = ((u or {}).get("data") or {}).get("parsed", {})
    rows = []
    for r in R.DEP_TABLE:
        p = parsed.get(r["t"])
        chk = "—" if not p else (f"{p['years']:g} 年（{filing_link(p, '10-K ' + p['report_date'])}）" + ("，與常數表不同" if abs(p["years"] - r["years"]) > 1e-9 else "，與常數表一致"))
        rows.append([f"{r['name']}（{r['fy']}）", r["years_text"], r["hist"], r["src"], chk])
    tbl = _table(["公司", "伺服器耐用年限", "變動紀錄", "來源申報檔", "最新 10-K 自動比對（XBRL）"], rows, raw=True, wrap=True)
    txt = ("折舊年限決定一台 GPU 的成本分幾年攤。年限拉長，每年的折舊費用變小、帳面獲利變大；若 GPU 實際三年就被淘汰，獲利與作為抵押品的帳面價值都被高估。"
           "六家公司的年限都落在 5 至 6 年，而且過去幾年多半是往長的方向調。每份新 10-K 出來時，程式會用 XBRL 的耐用年限標籤自動比對，年限有變就發通知。")
    return (f'<div class="imq-card blk"><h3>伺服器折舊年限<span class="imq-badge">只顯示</span></h3>{_stale(u)}<p class="plain">{txt}</p>{tbl}'
            '<p class="fine">年限與變動紀錄為依各公司申報檔整理的常數表；最後一欄為最新 10-K 的自動比對，兩者不同時另行通知。</p></div>')
