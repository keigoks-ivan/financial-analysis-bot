"""「多類同時」恐慌訊號頁面：/backtest/viable/panic_multi/。

update.py 每次跑完呼叫 write(state, generated)。回測數字讀 data/panic_multi/backtest.json
（v7-backtest `python3 -m src.panic_call.export_page_data` 產生，取審查時算好的結果，不重算）。
"""
from __future__ import annotations

import html as H
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BT = ROOT / "docs" / "backtest"
OUT = BT / "viable" / "panic_multi" / "index.html"
URL = "/backtest/viable/panic_multi/"
LAUNCH = "2026-11-24"
TITLE = "多類同時恐慌訊號：三類恐慌指標裡兩類同一天到極端，隔天買 call 或期貨"
SHORT = "多類同時恐慌訊號"
DESC = ("台股、S&P 500、Nasdaq-100 的「多類同時」恐慌訊號每日狀態：波動率、連三天加速下跌、"
        "期限結構或鎖跌停三類裡兩類同一天落在歷史最極端 5%，隔天收盤買三個月價內 call 或同名目期貨。")
MK = ("TW", "SPX", "NDX")
MNAME = {"TW": "台股", "SPX": "S&amp;P 500", "NDX": "Nasdaq-100"}
ANCHOR = {"TW": "tw", "SPX": "spx", "NDX": "ndx"}
C_CALL, C_FUT = "#2a78d6", "#eb6834"   # dataviz 參考色盤第 1、2 格，已跑過色盲與對比檢查


def M(s: str) -> str:
    return s.replace("-", "−")


def pc(x, d=0) -> str:
    return "—" if x is None else M(f"{x * 100:+.{d}f}%")


def pp(x, d=2) -> str:
    return "—" if x is None else M(f"{x:+.{d}f}")


def share(x) -> str:
    if x is None:
        return "—"
    v = x * 100
    return f"{v:.1f}%" if v >= 0.1 else "不到 0.1%"


def num(x, d=2) -> str:
    return "—" if x is None else M(f"{x:,.{d}f}")


CSS = """
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;--text:#111827;--muted:#6b7280;--border:#e5e7eb}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Noto Sans TC',sans-serif;background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.75rem 0 1.25rem;background:linear-gradient(180deg,#eff6ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.55rem;font-weight:700;letter-spacing:-.03em}
.page-hdr .sub{color:var(--muted);font-size:.88rem;margin-top:.2rem}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}.crumb a{color:var(--muted)}
.section{padding:1.75rem 0 0}
.section-title{font-size:1.08rem;font-weight:700;margin-bottom:1rem;padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.1rem 1.25rem;margin-bottom:1rem}
.card p,.prose p{font-size:.92rem;max-width:64rem;margin:.55rem 0}
.card p:first-child{margin-top:0}.card p:last-child{margin-bottom:0}
.bul{margin:.2rem 0 .6rem 1.3rem;font-size:.92rem;max-width:64rem}.bul li{margin:.35rem 0}
.tbl-cap{font-size:.86rem;font-weight:700;margin:1.1rem 0 .5rem}
table{width:100%;border-collapse:collapse;font-size:.82rem;background:var(--card);border:1px solid var(--border);border-radius:8px;overflow:hidden}
th,td{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--border)}
th{background:#f9fafb;font-weight:600;font-size:.7rem;letter-spacing:.03em;color:var(--muted)}
td{font-variant-numeric:tabular-nums;vertical-align:top}td.num,th.num{text-align:right}td.lbl{font-weight:500}
tbody tr:last-child td{border-bottom:0}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.table-note{font-size:.83rem;color:var(--muted);margin:.5rem 0}
.verdict{margin:1.25rem 0;border:1px solid var(--border);border-left:4px solid var(--brand);border-radius:8px;background:var(--card);padding:1rem 1.25rem}
.verdict-hd{font-size:.78rem;font-weight:700;color:var(--brand);margin-bottom:.35rem;letter-spacing:.04em}
.verdict ul{margin:.2rem 0 0 1.2rem;font-size:.92rem}.verdict li{margin:.3rem 0}
.st-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:1rem}
.st-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem 1.1rem;min-width:0}
.st-head{display:flex;justify-content:space-between;align-items:baseline;gap:.5rem;flex-wrap:wrap}
.st-name{font-weight:700;font-size:1rem}.st-date{color:var(--muted);font-size:.8rem}
.st-badge{display:inline-block;font-size:.78rem;font-weight:700;padding:.12rem .6rem;border-radius:999px;margin:.45rem 0 .3rem;border:1px solid}
.b-fire{background:#fbeceb;color:#b42318;border-color:#f0c4c0}
.b-recent{background:#fff7ed;color:#9a3412;border-color:#fed7aa}
.b-wait{background:#eef1f4;color:#374151;border-color:#d7dce2}
.b-armed{background:#e8f0fb;color:#1d4ea0;border-color:#b9cdee}
.st-card p{font-size:.86rem;margin:.35rem 0}
.cls{margin-top:.5rem;font-size:.82rem}.cls td,.cls th{padding:.4rem .55rem}.cls td.lbl{white-space:nowrap}
.lit{font-weight:700;color:#b42318}.dim{color:var(--muted)}
.order{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid #d97706;border-radius:8px;padding:.7rem .9rem;margin:.6rem 0 0;font-size:.85rem}
.order p{margin:.3rem 0}
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1rem}
.chart{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:.8rem .9rem;position:relative;min-width:0}
.chart h4{font-size:.86rem;margin-bottom:.2rem}.chart .lg{font-size:.76rem;color:var(--muted);margin-bottom:.3rem}
.sw{display:inline-block;width:14px;height:2px;vertical-align:middle;margin:0 .3rem 0 .6rem}
.chart svg{width:100%;height:auto;display:block}
.tip{position:absolute;pointer-events:none;background:#111827;color:#fff;font-size:.75rem;padding:.35rem .5rem;border-radius:6px;white-space:nowrap;display:none;z-index:5}
footer{margin-top:2.5rem;padding:1.25rem 0 2rem;border-top:1px solid var(--border);font-size:.78rem;color:var(--muted)}
@media(max-width:640px){.container{padding:0 1rem}.page-hdr h1{font-size:1.3rem}}
"""

JS = """
document.querySelectorAll('.chart').forEach(function(box){
  var tip=box.querySelector('.tip');
  box.querySelectorAll('[data-t]').forEach(function(el){
    el.addEventListener('mouseenter',function(){tip.textContent=el.getAttribute('data-t');tip.style.display='block';});
    el.addEventListener('mousemove',function(e){var r=box.getBoundingClientRect();tip.style.left=Math.max(4,Math.min(e.clientX-r.left+12,r.width-tip.offsetWidth-4))+'px';tip.style.top=(e.clientY-r.top-38)+'px';});
    el.addEventListener('mouseleave',function(){tip.style.display='none';});
  });
});
"""


def load_nav() -> str:
    spec = importlib.util.spec_from_file_location("fab_site_nav", ROOT / "scripts" / "site_nav.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.full_nav_block("system", "bt")


def toggle() -> str:
    sys.path.insert(0, str(BT))
    from _nav_common import make_toggle  # noqa: E402
    return make_toggle("viable_panic_multi")


# ───────────────────────── 今天的狀態 ─────────────────────────
def vn(s: dict) -> str:
    """「要等 VIX 收盤」：英文名前後留空格，中文括號結尾的不加。"""
    n = s["vol_name"]
    return ("" if not n[0].isascii() else " ") + n + ("" if n.endswith("）") else " ")


def status_card(m: str, s: dict) -> str:
    c = s["classes"]
    med = s.get("vol_median_next")
    if s["event_today"]:
        badge, cls = "今天亮起", "b-fire"
        say = f"三類裡亮了 {s['n_lit']} 類，而且上一波已經結束，算新的一波。隔天收盤進場。"
    elif s.get("order_for_event"):
        ev = s["order_for_event"]
        o = s.get("order") or {}
        badge, cls = f"{ev[5:7]}/{ev[8:]} 亮起", "b-recent"
        say = f"{ev} 收盤亮起（{s['event_state']['n_lit']} 類）。規則的進場點是隔天 {o.get('entry_est')} 收盤"
        say += "，已經過了。" if o.get("entry_est") and o["entry_est"] <= s["date"] else "。"
        if ev < LAUNCH:
            say += f"本頁 {LAUNCH} 才上線，這一筆沒有即時通知。"
        say += f"之後要等{vn(s)}收盤回到約 {num(med)} 以下，才能算下一波。"
    elif s["multi_lit"] and not s["armed_open"]:
        badge, cls = "亮兩類但不算", "b-wait"
        say = (f"今天三類亮了 {s['n_lit']} 類，但上一波（{s['last_event']}）還沒結束：{s['vol_name']}從那次之後沒有回到"
               f"自己歷史中位數（約 {num(med)}）以下，依規則不算新的訊號。")
    elif not s["armed_open"]:
        badge, cls = "上一波還沒結束", "b-wait"
        say = f"上一波是 {s['last_event']}。要等{vn(s)}收盤回到約 {num(med)} 以下，之後再亮才算。今天亮 {s['n_lit']} 類。"
    else:
        badge, cls = "可以觸發", "b-armed"
        say = f"今天亮 {s['n_lit']} 類，要兩類同一天亮才算。上一波是 {s['last_event'] or '無'}。"
    a, b, r = c["vol"], c["accel"], c["ratio"]
    rd = 4

    def flag(x):
        return "<span class='lit'>亮</span>" if x else "<span class='dim'>沒亮</span>"
    bp = "、".join(M(f"{x / 100:+.2f}%") for x in b["last3_bp"]) if b.get("last3_bp") else "—"
    thr_b = num(b["next_threshold"]) if b.get("next_threshold") is not None else "—"
    rows = [
        (f"甲 {s['vol_name']}", num(a["value"]), share(a["share"]),
         f"高於 {num(a['next_threshold'])}" if a.get("next_threshold") is not None else "—", flag(a["lit"])),
        ("乙 連三天加速下跌", f"近三天 {bp}<br>標準化 {num(b['value'])}", share(b["share"]),
         f"連三天跌、一天比一天多，且標準化低於 {thr_b}", flag(b["lit"])),
        (f"丙 {s['ratio_name']}", num(r["value"], rd), share(r["share"]),
         f"高於 {num(r['next_threshold'], rd)}" if r.get("next_threshold") is not None else "—", flag(r["lit"])),
    ]
    trs = "".join(f"<tr><td class='lbl'>{x[0]}</td><td class='num'>{x[1]}</td><td class='num'>{x[2]}</td>"
                  f"<td>{x[3]}</td><td>{x[4]}</td></tr>" for x in rows)
    tbl = (f"<div class='scroll'><table class='cls'><thead><tr><th>類別</th><th class='num'>今天</th>"
           f"<th class='num'>歷史上一樣極端的比例</th><th>明天要亮的條件</th><th>亮了沒</th></tr></thead><tbody>{trs}</tbody></table></div>")
    order = order_html(m, s) if s.get("order") else ""
    return (f"<div class='st-card' id='{ANCHOR[m]}'><div class='st-head'><span class='st-name'>{H.escape(s['name'])}</span>"
            f"<span class='st-date'>資料到 {s['date']}，收盤 {num(s['close'])}</span></div>"
            f"<span class='st-badge {cls}'>{badge}</span><p>{H.escape(say)}</p>{tbl}{order}</div>")


def order_html(m: str, s: dict) -> str:
    o = s["order"]
    past = o.get("entry_est") and o["entry_est"] <= s["date"]
    head = "規則當時的進場規格（進場日已過，只供對照）：" if past else "規則的進場規格："
    ps = [f"<p><b>{head}</b>訊號日 {s['order_for_event']}，{o.get('entry_est')} 收盤進場，遇休市順延；call 版與期貨版二選一。</p>"]
    if m == "TW":
        if "call" not in o:
            return "<div class='order'>" + "".join(ps) + f"<p>{H.escape(o.get('note', ''))}</p></div>"
        c, f = o["call"], o["fut"]
        ps.append(f"<p>call 版：台指選擇權 {o['expiry'][:4]}-{o['expiry'][4:]} 月（{o['expiry_date']} 到期，{o['days']} 天）、履約價 {c['strike']:,.0f} 的買權。"
                  f"訊號日結算價 {c['settle']:,.0f} 點，一口約 {c['premium_twd']:,.0f} 元；訊號日成交 {c['volume']} 口，要掛限價。抱到到期。</p>")
        ps.append(f"<p>期貨版：每 1 口買權改買 1 口小台（同月份，每點 50 元），名目一樣。收盤虧損達到權利金點數"
                  f"（約 {f['stop_pts']:,.0f} 點，加權指數約 {f['stop_level']:,.0f}）就在收盤停損，否則抱到同一個到期日。</p>")
    else:
        c, f = o["call"], o["fut"]
        ps.append(f"<p>call 版：{H.escape(c['product'])}，{o['expiry']} 到期（{o['days']} 天）、履約價 {c['strike']:,.0f}。"
                  f"公式估每口約 {c['premium_usd']:,.0f} 美元（隱含波動率 {c['vol_used']}%），下單看實際報價。抱到到期。{H.escape(c['alt'])}。</p>")
        ps.append(f"<p>期貨版：每 1 口 call 改買 {f['per_call']:g} 口 {H.escape(f['product'])}，{f['month']} 月合約，名目一樣。"
                  f"收盤虧損達到同一筆權利金（從進場價跌約 {f['stop_pts']:,.0f} 點）就在收盤停損，否則抱到 {o['expiry']} 收盤。</p>")
    ps.append(f"<p>預算：每次權利金＝帳戶的 1%，口數＝帳戶 1% ÷ 每口權利金，取整數。同一個市場一年最多 4 次，今年已亮 {s['events_this_year']} 次。</p>")
    return "<div class='order'>" + "".join(ps) + "</div>"


# ───────────────────────── 回測 ─────────────────────────
def chart(m: str, B: dict) -> str:
    tr = B["markets"][m]["trades"]
    W, Hh, L, R, T, Bm = 520, 230, 40, 78, 14, 26
    y0 = min(int(t["entry_date"][:4]) for t in tr)
    y1 = max(int(t["exit_date"][:4]) for t in tr) + 1

    def X(dstr):
        y, mo = int(dstr[:4]), int(dstr[5:7])
        return L + (y + (mo - 0.5) / 12 - y0) / (y1 - y0) * (W - L - R)
    start = X(tr[0]["entry_date"])
    cc = cf = 0.0
    pc_, pf = [(0.0, start)], [(0.0, start)]
    for t in tr:
        cc += t["call_ret"]
        cf += t["fut_ret"]
        pc_.append((cc, X(t["exit_date"])))
        pf.append((cf, X(t["exit_date"])))
    lo = min(0.0, min(v for v, _ in pc_ + pf))
    hi = max(v for v, _ in pc_ + pf)
    hi += (hi - lo) * 0.08

    def Y(v):
        return T + (hi - v) / (hi - lo) * (Hh - T - Bm)

    def path(pts):
        d = f"M{pts[0][1]:.1f},{Y(pts[0][0]):.1f}"
        for v, x in pts[1:]:
            d += f" H{x:.1f} V{Y(v):.1f}"
        return d + f" H{W - R:.1f}"
    step = 2 if hi - lo > 6 else 1
    grid = ""
    for v in sorted(set(list(range(0, int(hi) + 1, step)) + list(range(0, int(lo) - 1, -step)))):
        if v < lo or v > hi:
            continue
        lab = M(f"{v:+d}") if v else "0"
        grid += (f"<line x1='{L}' x2='{W - R}' y1='{Y(v):.1f}' y2='{Y(v):.1f}' stroke='{'#9ca3af' if v == 0 else '#eef0f3'}'/>"
                 f"<text x='{L - 6}' y='{Y(v) + 3:.1f}' text-anchor='end' font-size='10' fill='#6b7280'>{lab}</text>")
    gap = 5 if y1 - y0 > 14 else 2
    ticks = ""
    for y in range(y0 + (gap - y0 % gap) % gap, y1 + 1, gap):
        x = L + (y - y0) / (y1 - y0) * (W - L - R)
        ticks += f"<text x='{x:.1f}' y='{Hh - 8}' text-anchor='middle' font-size='10' fill='#6b7280'>{y}</text>"
    dots = ""
    for i, t in enumerate(tr):
        tip = (f"{t['entry_date']} 進場、{t['exit_date']} 出場：call {pc(t['call_ret'])}、期貨 {pc(t['fut_ret'])}"
               + ("（停損）" if t["fut_stopped"] else ""))
        for pts, col in ((pf, C_FUT), (pc_, C_CALL)):
            v, x = pts[i + 1]
            dots += f"<circle cx='{x:.1f}' cy='{Y(v):.1f}' r='4' fill='{col}' stroke='#fff' stroke-width='2'/>"
        v, x = pc_[i + 1]
        dots += f"<rect x='{x - 9:.1f}' y='{T}' width='18' height='{Hh - T - Bm}' fill='transparent' data-t='{H.escape(tip)}'/>"
    yc, yf = Y(cc), Y(cf)
    if abs(yc - yf) < 13:
        mid = (yc + yf) / 2
        yc, yf = (mid - 7, mid + 7) if cc >= cf else (mid + 7, mid - 7)
    end = (f"<text x='{W - R + 6}' y='{yc + 3:.1f}' font-size='10.5' fill='#374151'>call {M(f'{cc:+.1f}')}</text>"
           f"<text x='{W - R + 6}' y='{yf + 3:.1f}' font-size='10.5' fill='#374151'>期貨 {M(f'{cf:+.1f}')}</text>")
    return (f"<svg viewBox='0 0 {W} {Hh}' role='img' aria-label='{MNAME[m]}每次拿帳戶 1% 的累計損益，call 版與期貨版'>"
            f"{grid}{ticks}<path d='{path(pf)}' fill='none' stroke='{C_FUT}' stroke-width='2'/>"
            f"<path d='{path(pc_)}' fill='none' stroke='{C_CALL}' stroke-width='2'/>{dots}{end}</svg>")


def bt_table(B: dict) -> str:
    rows = []
    names = {"TW": "台股（真實台指選擇權價格）", "SPX": "S&amp;P 500（公式估價）", "NDX": "Nasdaq-100（公式估價）"}
    for m in MK:
        x = B["markets"][m]
        for key, lab in (("call", "call 版"), ("fut", "期貨版")):
            s = x[key]
            acct = x["call_acct"] if key == "call" else s
            stop = "—" if key == "call" else f"{s['stop_rate'] * 100:.0f}%"
            rows.append(f"<tr><td class='lbl'>{names[m] if key == 'call' else ''}</td><td>{lab}</td><td class='num'>{s['n']}</td>"
                        f"<td class='num'>{pc(s['mean'])}</td><td class='num'>{pc(s['median'])}</td><td class='num'>{s['win'] * 100:.0f}%</td>"
                        f"<td class='num'>{pc(s['worst'])}</td><td class='num'>{pc(s['mean_ex_top3'])}</td>"
                        f"<td class='num'>{pp(acct['total_pp'])}</td><td class='num'>{pp(acct['worst_year_pp'])}（{acct['worst_year']}）</td>"
                        f"<td class='num'>{stop}</td></tr>")
    return ("<div class='scroll'><table><thead><tr><th>市場</th><th>做法</th><th class='num'>筆數</th><th class='num'>平均每筆</th>"
            "<th class='num'>中位數</th><th class='num'>賺錢比例</th><th class='num'>最差一筆</th><th class='num'>去掉最賺三筆的平均</th>"
            "<th class='num'>帳戶全期合計（個百分點）</th><th class='num'>最差一年（個百分點）</th><th class='num'>期貨停損比例</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table></div>")


def trades_table(m: str, B: dict) -> str:
    x = B["markets"][m]
    nd = 0 if m == "TW" else 2
    rows = []
    for t in x["trades"]:
        extra = f"<td class='num'>{int(t['entry_volume'])}</td>" if m == "TW" else ""
        rows.append(f"<tr><td>{t['sig_date']}</td><td>{t['entry_date']}</td><td>{t['exit_date']}</td><td class='num'>{num(t['S0'], nd)}</td>"
                    f"<td class='num'>{num(t['strike'], nd)}</td><td class='num'>{num(t['prem'], nd)}</td>"
                    f"<td class='num'>{pc(t['idx_move_exp'], 1)}</td><td class='num'>{pc(t['call_ret'])}</td>"
                    f"<td class='num'>{pc(t['fut_ret'])}{'（停損）' if t['fut_stopped'] else ''}</td>{extra}</tr>")
    ext_h = "<th class='num'>進場合約當天成交（口）</th>" if m == "TW" else ""
    return ("<div class='scroll'><table><thead><tr><th>訊號日</th><th>進場日</th><th>出場日</th><th class='num'>進場指數</th><th class='num'>履約價</th>"
            "<th class='num'>權利金（點）</th><th class='num'>到期時指數漲跌</th><th class='num'>call 報酬</th><th class='num'>期貨報酬</th>"
            f"{ext_h}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>")


def put_table(B: dict) -> str:
    rows = []
    names = {"TW": "台股（真實價格）", "SPX": "S&amp;P 500（公式估價）", "NDX": "Nasdaq-100（公式估價）"}
    for m in MK:
        for ent, lab in (("panic", "恐慌當天"), ("stab", "止穩後")):
            p = B["markets"][m][f"put_{ent}"]
            rows.append(f"<tr><td class='lbl'>{names[m] if ent == 'panic' else ''}</td><td>{lab}</td><td class='num'>{p['n']}</td>"
                        f"<td class='num'>{pc(p['mean'])}</td><td class='num'>{pc(p['median'])}</td><td class='num'>{p['win'] * 100:.0f}%</td>"
                        f"<td class='num'>{pc(p['worst'])}</td><td class='num'>{pp(p['acct']['total_pp'])}</td></tr>")
    return ("<div class='scroll'><table><thead><tr><th>市場</th><th>進場</th><th class='num'>筆數</th><th class='num'>平均每筆</th>"
            "<th class='num'>中位數</th><th class='num'>賺錢比例</th><th class='num'>最差一筆</th><th class='num'>帳戶全期合計（個百分點）</th>"
            f"</tr></thead><tbody>{''.join(rows)}</tbody></table></div>")


def sections(state: dict, B: dict) -> str:
    tw, spx, ndx = (B["markets"][m] for m in MK)
    out = []
    cards = "".join(status_card(m, state[m]) for m in MK if m in state)
    out.append(("今天的狀態", "<p class='table-note'>每天從全部歷史重算一次，不存任何中間狀態。美股在台北清晨更新；"
                "台股要等上市櫃全部個股的收盤資料，通常隔天清晨才算得出來。「歷史上一樣極端的比例」是跟到前一天為止的全部歷史比，"
                "5% 以內才算亮。</p>"
                f"<div class='st-grid'>{cards}</div>"))
    rule = (
        "<div class='card'><p><b>三類恐慌指標，兩類同一天落在歷史最極端的 5%，就是訊號。</b></p><ul class='bul'>"
        "<li>甲，隱含波動率：S&amp;P 500 看 VIX，Nasdaq-100 看 VXN，台股看用台指選擇權結算價自算的台指 VIX。越高越極端。</li>"
        "<li>乙，連三天加速下跌：三天都收跌，跌幅一天比一天大（以整數基點比），而且三天累計報酬除以之前 20 個交易日的日波動"
        "（再乘根號 3），落在歷史最差的 5%。</li>"
        "<li>丙，美股看 VIX 除以三個月 VIX（VIX3M）：短天期的恐慌高過長天期時，這個比值會大於 1。台股看收盤鎖跌停的家數占上市櫃家數的比率。"
        "越高越極端。</li>"
        "<li>「極端」一律跟到前一天為止的全部歷史比，至少累積五年才開始算，平手算極端。丙類在美股要到 2011 年 7 月、台股要到 2012 年才有五年歷史，"
        "之前只剩甲、乙兩類可湊。</li>"
        "<li>同一波只算一次：亮過之後，要等波動率指數收盤回到自己歷史中位數以下，才能再算新的一波。</li></ul>"
        "<p><b>進場：訊號日收盤後確認，隔天收盤進場。</b>台指 VIX 用選擇權當天的結算價算，美股 VIX 比指數晚 15 分鐘收盤，"
        "訊號當天的收盤價其實買不到。回測裡當天進場與隔天進場的 call 平均：台股 "
        f"{pc(tw['call_sameday']['mean'])} 對 {pc(tw['call']['mean'])}，S&amp;P 500 {pc(spx['call_sameday']['mean'])} 對 "
        f"{pc(spx['call']['mean'])}，Nasdaq-100 {pc(ndx['call_sameday']['mean'])} 對 {pc(ndx['call']['mean'])}。</p>"
        "<p><b>call 版：</b>三個月價內 5% 的買權（到期日在進場後 60～100 天、最接近 91 天；履約價最接近進場價的 95%），抱到到期。"
        "台股用台指選擇權。S&amp;P 500 用 XSP（S&amp;P 500 除以 10 的小型指數選擇權，歐式、現金結算），帳戶夠大可改 SPX。"
        "Nasdaq-100 用 QQQ 選擇權：NDX 一口名目兩百多萬美元，小型的 XND 幾乎沒有成交。</p>"
        "<p><b>期貨版：</b>跟 call 一樣的名目買指數期貨（台股小台、S&amp;P 500 用 MES、Nasdaq-100 用 MNQ），"
        "每天收盤檢查，虧損達到那筆權利金的金額就停損，否則抱到同一個到期日。</p>"
        "<p><b>預算：</b>每次權利金占帳戶 1%，同一個市場一年最多 4 次。上一筆還沒到期時新訊號不加碼。期貨版用同一筆金額當停損額度。</p></div>")
    out.append(("規則", rule))
    worst_fut = min(tw["fut"]["worst"], spx["fut"]["worst"], ndx["fut"]["worst"])
    intro = (
        f"<p>call 版三個市場都賺錢。台股 {tw['call']['n']} 筆，每筆平均賺權利金的 {pc(tw['call']['mean'])}；"
        f"每次拿帳戶 1% 下去，全期合計帳戶多 {pp(tw['call_acct']['total_pp'])} 個百分點。"
        f"S&amp;P 500 {spx['call']['n']} 筆平均 {pc(spx['call']['mean'])}，Nasdaq-100 {ndx['call']['n']} 筆平均 {pc(ndx['call']['mean'])}。"
        "比較的基準是什麼都不做，也就是 0。</p>"
        f"<p>同樣的錢買期貨，大致也賺得到：台股每筆 {pc(tw['fut']['mean'])}（call {pc(tw['call']['mean'])}），"
        f"S&amp;P 500 {pc(spx['fut']['mean'])}（call {pc(spx['call']['mean'])}），Nasdaq-100 {pc(ndx['fut']['mean'])}（call {pc(ndx['call']['mean'])}），"
        "都以那筆權利金當分母。錢主要來自指數反彈。"
        f"call 換到的是虧損有上限：期貨最差一筆跳空，賠到權利金的 {abs(worst_fut):.1f} 倍；call 最多賠光權利金。</p>"
        f"<p>回測資料到 {B['data_end']}。台股用台指選擇權每天的真實報價（買進用收盤時最後的委賣價）；"
        "美股沒有歷史報價，用公式估（隱含波動率用 VIX3M、VXN，加價內偏斜，再扣 3% 成本）。拿台股真實價格對照，"
        "公式把三個月價內 call 的權利金估貴約 10%、報酬估低約 10 個百分點，所以美股 call 的結果偏保守。期貨版不用估價。</p>"
        # 下面數字取自 v7 docs/Panic_Call_Results.md 第七節「跟跌勢中隨機日比」（恐慌當天進場、三個月價內 call）
        "<p>再跟「跌勢中隨便挑一天買同樣的 call」比：從收盤比 252 日高點低 10% 以上的日子裡，隨機抽同樣筆數，抽 2,000 次。"
        "恐慌當天進場的三個月價內 call，台股事件平均 +92%、隨機 +22%，排在隨機的第 95 百分位；S&amp;P 500 +28% 對 −8%，第 93 百分位；"
        "Nasdaq-100 +48% 對 +6%，第 82 百分位。這組比較只做了當天進場，隔天進場與期貨版沒有做。</p>")
    charts = "".join(
        f"<div class='chart'><h4>{MNAME[m]}：每次拿帳戶 1% 的累計損益（個百分點）</h4><div class='lg'>"
        f"<span class='sw' style='background:{C_CALL}'></span>call 版<span class='sw' style='background:{C_FUT}'></span>期貨版</div>"
        f"{chart(m, B)}<div class='tip'></div></div>" for m in MK)
    out.append(("回測結果", f"<div class='prose'>{intro}</div><div class='tbl-cap'>隔天收盤進場、抱到到期（報酬以權利金為分母）</div>{bt_table(B)}"
                "<p class='table-note'>帳戶全期合計：每次拿帳戶 1%，把每筆報酬加總，單位是帳戶的個百分點。最差一年含沒有進場的年份。"
                "期貨停損是收盤虧到權利金的金額就出場。</p>"
                f"<div class='charts' style='margin-top:1rem'>{charts}</div>"
                "<p class='table-note'>階梯線在每筆出場的月份往上或往下跳。滑過圓點看那一筆，逐筆數字在下一節。</p>"))
    tables = "".join(f"<div class='tbl-cap' id='trades-{ANCHOR[m]}'>{MNAME[m]}逐筆</div>{trades_table(m, B)}" for m in MK)
    skip = [f"{MNAME[m]} {k['sig_date']}" for m in ("SPX", "NDX", "TW") for k in B["markets"][m]["skipped"]]
    out.append(("逐筆", tables + (f"<p class='table-note'>訊號有亮但沒有進場：{'、'.join(skip)}。上一筆還沒到期，依規則不加碼。</p>" if skip else "")))
    lim = (
        "<div class='card'><ul class='bul'>"
        f"<li><b>次數太少。</b>台股 {tw['call']['n']} 筆、S&amp;P 500 {spx['call']['n']} 筆、Nasdaq-100 {ndx['call']['n']} 筆；"
        f"三個市場合起來 {B['pooled_call_nd']['n']} 筆，同一季不分市場算一波，只有 {B['pooled_call_nd']['waves']} 波。台股只有 8～9 波獨立的恐慌。</li>"
        f"<li><b>最賺三筆占了大部分獲利。</b>台股最賺三筆占全部賺錢筆的 {tw['call']['top3_share_of_gain'] * 100:.0f}%，"
        f"S&amp;P 500 占 {spx['call']['top3_share_of_gain'] * 100:.0f}%；去掉這三筆，S&amp;P 500 的 call 平均變成 {pc(spx['call']['mean_ex_top3'])}。</li>"
        "<li><b>2008 年沒有事件。</b>台股是因為 2007-07-27 那一波之後，台指 VIX 到 2009 年 11 月才回到中位數以下，依「同一波只算一次」不能再亮。"
        "美股是因為丙類要到 2011 年才有五年歷史，2008 年只剩兩類可湊，兩類同一天亮只發生在 2009-03-02。"
        "一路跌、沒有快速反彈的行情，這條訊號幾乎沒有被測過。</li>"
        "<li><b>同樣的錢買期貨，大致也賺得到。</b>錢來自指數反彈；call 換到的只是虧損有上限。</li>"
        "<li><b>台股價內 call 常常沒成交。</b>這個規格的進場合約，回測裡 72% 的日子當天沒有成交；"
        f"這條訊號隔天進場的 {tw['call']['n']} 筆，進場那天全部沒有成交。回測用收盤時最後的委賣價買，"
        "2025-04-01 那筆連委賣價都沒有，用結算價加成本。改用隔天有成交的最近履約價，平均是 +89%。實際要掛限價，可能買不到或要多付。</li>"
        "<li><b>證明不了，只能說是線索。</b>同一批研究的帳本記了 705 組試驗，這條是看過結果才挑出來上線的；樣本這麼少，分不出是本事還是運氣。</li>"
        "<li>美股的 call 報酬是公式估的，不是真實報價。台指 VIX 是自算的：2011 年以前履約價少、品質較差，2008 年 10 月最急的六天沒有值，"
        "2026 年以前沒有官方值可以對。</li>"
        "</ul></div>")
    out.append(("限制", lim))
    ps, pst = tw["put_panic"], tw["put_stab"]
    pre = [t for t in ps["trades"] if t["entry_date"] < "2012"]
    put = (
        "<div class='card'><p><b>這是對照版，不是建議做法。</b>同一批訊號，改站賣方：一個月到期，賣出履約價最接近收盤 95% 的賣權、"
        "買進最接近 90% 的賣權，抱到到期。報酬以最大虧損（兩個履約價的差減掉收進的權利金）當分母。"
        "恐慌當天進場與止穩後進場兩種並列，不分主從。止穩後是指訊號後 20 個交易日內，第一個收盤高過前三天最高收盤、"
        "而且波動率指數低於訊號以來最高收盤的日子。恐慌當天用當天價格進場，跟上面 call 版的隔天進場不同。</p>"
        f"<p>台股恐慌當天 {ps['n']} 筆，平均 {pc(ps['mean'])}、中位數 {pc(ps['median'])}、賺錢 {ps['win'] * 100:.0f}%；"
        f"止穩後 {pst['n']} 筆，平均 {pc(pst['mean'])}，{pst['n']} 筆全賺。美股是公式估的，拿台股真實價格對照，公式對賣價差偏樂觀約 5.5 個百分點。</p>"
        f"{put_table(B)}<ul class='bul' style='margin-top:.8rem'>"
        f"<li>止穩後 {pst['n']} 筆全賺，是看過結果才看到的。兩種進場時點，事先沒有理由挑哪一個。</li>"
        f"<li>台股只有 {ps['n']} 筆，除了 {pre[0]['sig_date'] if pre else ''} 那一筆，都在 2012 年以後：鎖跌停比率要到 2012 年才有五年歷史，"
        "之前只能靠甲、乙兩類同時亮。沒碰過 2008 那種一路跌的行情，賣價差最怕的就是這種行情。</li>"
        f"<li>換成帳戶來看：同樣每次拿帳戶 1% 去冒險，三個月價內 call 恐慌當天進場一次平均約賺帳戶 {tw['call_sameday']['mean']:.1f}%"
        f"（上面隔天進場的版本是 {tw['call']['mean']:.2f}%），止穩後賣價差約 {pst['mean']:.2f}%。賣方比較穩，但收進的權利金就是獲利上限。</li>"
        "<li>跟跌勢中隨便挑一天賣同樣的價差比，台股恐慌當天的 +2% 不如隨機的 +3%（排在第 43 百分位），止穩後的 +16% 排在第 87 百分位。</li>"
        "<li>之前站賣方的研究都沒過：台指波動高的時候賣跨式，2020-03 單月虧 124%；11-07 的雙賣價差腿，留出來驗證的那段淨虧。</li>"
        "</ul><p class='table-note'>這一版不進 TradingView，也不進通知。</p></div>")
    out.append(("對照版：賣出賣權價差", put))
    notify = (
        "<div class='card'><p>S&amp;P 500、Nasdaq-100 在 TradingView 有同算法的提醒（門檻值由本頁的程式算好寫死，標了日期，"
        "以本頁為準）。台股的自算台指 VIX 與鎖跌停家數比率 TradingView 上沒有，台股只靠本頁、Email 與 Discord。</p>"
        "<p>新事件出現那天寄 Email 並發 Discord，內容寫三類各自的分位、隔天要買的 call 與期貨規格、預算，以及下次重新觸發要等什麼。</p>"
        "<p>資料：美股 Yahoo Finance 收盤（S&amp;P 500、Nasdaq-100、VIX、VXN、VIX3M）；台股證交所加權指數收盤、期交所台指選擇權每日行情（自算台指 VIX）、"
        "上市櫃個股日線（鎖跌停家數）。舊資料取自回測用的同一份，之後每天從同一來源接上。"
        "事前登記與結果：v7-backtest 的 docs/Panic_Call_Prereg.md、docs/Panic_Call_Results.md。</p></div>")
    out.append(("通知與資料", notify))
    return "\n".join(f"<div class='section'><h2 class='section-title'>{t}</h2>{b}</div>" for t, b in out)


def check_punct(html: str) -> None:
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    bad = re.findall(r"[一-鿿][,.:;!?()]", text)
    assert not bad, f"半形標點跟在中文後：{bad[:5]}"


def write(state: dict, generated: str) -> None:
    B = json.loads((ROOT / "data" / "panic_multi" / "backtest.json").read_text())
    hero = ("<div class='verdict'><div class='verdict-hd'>一句話</div><ul>"
            "<li>恐慌指標三類裡兩類同一天落在歷史最極端 5%，隔天收盤買三個月價內 call，或同名目的指數期貨。</li>"
            "<li>回測三個市場都賺錢，但每個市場只有 5～12 筆，最賺三筆占大部分獲利，只能當線索。</li>"
            "<li>每次只拿帳戶 1%，一年最多 4 次。</li></ul></div>")
    body = (f'<div class="page-hdr"><div class="container"><div class="crumb"><a href="/">首頁</a> / <a href="/backtest/">回測</a> / '
            f'<a href="/backtest/viable/">可行策略專區</a> / {SHORT}</div><h1>{TITLE}</h1>'
            f'<div class="sub">台股、S&amp;P 500、Nasdaq-100 每天更新狀態；三個月價內 call 與同名目期貨兩種做法；回測到 {B["data_end"]}</div>'
            f"{toggle()}</div></div><div class='container'>{hero}{sections(state, B)}</div>")
    html = (f"<!DOCTYPE html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"UTF-8\">\n"
            f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n<title>{TITLE} | InvestMQuest Research</title>\n"
            f"<meta name=\"description\" content=\"{DESC}\">\n<style>{CSS}</style>\n</head>\n<body>\n{load_nav()}\n{body}\n"
            f"<footer><div class=\"container\">&copy; 2026 InvestMQuest Research &middot; 回測資料到 {B['data_end']}，每日狀態更新於 {generated}（台北時間）"
            f" &middot; 僅供研究參考，不構成投資建議</div></footer>\n<script>{JS}</script>\n</body>\n</html>\n")
    check_punct(html)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    sys.path.insert(0, str(BT))
    import _apply_meta as AM  # noqa: E402
    import _page_meta as PM  # noqa: E402
    meta = PM.MEMBERS.get(URL)
    if meta:
        r = AM.apply_one(URL, meta["title"], meta["short"], meta["status"])
        if r not in ("changed", "same"):
            print(f"頁首標籤沒有套上：{r}")
