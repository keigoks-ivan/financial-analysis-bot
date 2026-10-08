"""產生 docs/macro/db/ 的網頁與圖表資料。

每個類別一頁（us/<category>.html、tw/<category>.html），圖表資料放 data/<country>/<category>.json，
總覽 index.html。數值換算（年增率、月增率、比率等）在這裡用 Python 做好再寫進 json。
"""
import datetime as dt
import html
import json
import shutil
from pathlib import Path

from macro_db import catalog_io, store, transform
from macro_db import calendar as relcal

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "macro" / "db"
CATALOG_DIR = Path(__file__).resolve().parent / "catalog"
WEB_DIR = Path(__file__).resolve().parent / "web"

# 國家／區域的顯示名稱與順序（總覽分頁照這個順序）；沒有 catalog/<代碼>.json 的會自動略過
COUNTRY_NAME = {"us": "美國", "tw": "台灣", "jp": "日本", "cn": "中國", "eu": "歐洲", "an": "東南亞"}
WD = "一二三四五六日"
STALE_DAYS = {"D": 12, "W": 20, "M": 110, "Q": 230, "A": 820}   # 從資料期間的起日算；年資料 Y 年的值要到 Y+1 年才公布
BAR_DISPLAYS = ("diff", "mom")
SUFFIX = {"yoy": "年增率", "diff": "變動"}
NO_NOTE_PREFIX = ("分母", "縱軸", "橫軸")


def esc(s):
    return html.escape(str(s), quote=True)


def hspace(s):
    """中文與半形數字之間補半形空格（站上慣例）。"""
    import re
    s = re.sub(r"([一-鿿）」])(\d)", r"\1 \2", s)
    s = re.sub(r"(\d)([一-鿿（「])", r"\1 \2", s)
    return s


# ---------- 格式化 ----------
def auto_nd(v):
    """fnum 預設的小數位數；整數值（例如景氣分數 41）不帶小數。"""
    a = abs(v)
    if a >= 1000 or (a >= 1 and float(v).is_integer()):
        return 0
    if a >= 100:
        return 1
    if a >= 1:
        return 2
    return 3


def _z(v, nd):
    """四捨五入後是 0 的負數（例如 −0.004）當成 0，免得顯示「−0.0%」。"""
    return 0.0 if round(v, nd) == 0 else v


def fnum(v, nd=None):
    if v is None:
        return "–"
    nd = auto_nd(v) if nd is None else nd
    return f"{_z(v, nd):,.{nd}f}"


LIGHTS = {1: "藍燈", 2: "黃藍燈", 3: "綠燈", 4: "黃紅燈", 5: "紅燈"}


def is_light(spec):
    return (spec.get("unit") or "").startswith("燈號序數")


def unit_nd(spec):
    """依單位固定小數位：利差等「百分點」2 位、擴散指數 1 位；catalog 可用 nd 指定（例如人民幣中間價 4 位）；其他回 None（依數值大小）。"""
    if spec.get("nd") is not None:
        return spec["nd"]
    u = unit_of(spec)
    if u.startswith("百分點"):
        return 2
    if u.startswith("擴散指數"):
        return 1
    return None


def is_index_unit(u):
    return u.startswith("指數") and u != "指數點"


def unit_of(spec):
    """顯示用單位（短）。"""
    d = spec.get("display", "level")
    if d in ("yoy", "mom"):
        return "%"
    if d == "ratio":
        return "%"
    return spec.get("unit_out") or spec.get("unit", "")


def short_unit(u):
    return (u or "").split("（")[0].split("(")[0]


def vtxt(v, spec):
    d = spec.get("display", "level")
    u = unit_of(spec)
    if is_light(spec):
        return LIGHTS.get(int(round(v)), fnum(v))
    if d == "yoy":
        return f"{_z(v, 1):.1f}%".replace("-", "−")
    if d == "mom":
        return f"{_z(v, 2):.2f}%".replace("-", "−")
    if d == "ratio":
        return f"{_z(v, 2):.2f}%".replace("-", "−")
    if d == "diff":
        return (f"{fnum(v, 0 if abs(v) >= 10 else 1)} {short_unit(u)}".strip()).replace("-", "−", 1)
    if u.startswith("%"):
        extra = u[1:]
        return f"{v:.2f}%{extra}".replace("-", "−", 1) if v < 0 else f"{v:.2f}%{extra}"
    if unit_nd(spec) is not None:
        return f"{fnum(v, unit_nd(spec))} {short_unit(u)}".replace("-", "−", 1)
    if is_index_unit(u):   # 指數的基期寫在「單位：」那一行，數字後面不重複
        return fnum(v).replace("-", "−", 1)
    if u in ("", "擴散指數", "標準差"):
        return fnum(v) + ("" if u == "" else " " + short_unit(u))
    return (f"{fnum(v)} {short_unit(u)}".strip()).replace("-", "−", 1)


def period_txt(date_s, freq):
    y, m = int(date_s[:4]), int(date_s[5:7])
    if freq == "M":
        return f"{y} 年 {m} 月"
    if freq == "Q":
        return f"{y} 年第 {(m - 1) // 3 + 1} 季"
    if freq == "A":
        return f"{y} 年"
    return date_s


def change_txt(latest, prev, spec, signed=False):
    d = spec.get("display", "level")
    u = unit_of(spec)
    pct_like = d in ("yoy", "mom", "ratio") or u.startswith("%") or u.startswith("百分點")
    if pct_like:
        nd = 1 if d == "yoy" else 2
        diff = round(latest, nd) - round(prev, nd)
        sign = "+" if diff > 0.0001 else ("−" if diff < -0.0001 else "")
        return f"{sign}{abs(diff):.{nd}f} 個百分點"
    if is_light(spec):
        a, b = LIGHTS.get(int(round(prev))), LIGHTS.get(int(round(latest)))
        return "持平" if a == b else f"由{a}轉{b}"
    nd = unit_nd(spec) if unit_nd(spec) is not None else max(auto_nd(latest), auto_nd(prev))   # 變動的精度跟著顯示值走，避免 3.4 對 3.3 寫成 +0.05
    diff = round(latest, nd) - round(prev, nd)
    sign = "+" if diff > 0 else ("−" if diff < 0 else "")
    unit_s = "" if is_index_unit(u) else short_unit(u)
    s = f"{sign}{fnum(abs(diff), nd)} {unit_s}".strip()
    # 會正負翻轉的序列（貿易差額、經常帳等）百分比變動沒有意義，不附
    # 未季調的季、月水準值（例如中國單季現價 GDP）跟上一期比會混進季節波動，catalog 標 pct_change: false 就不附
    if d == "level" and not signed and spec.get("pct_change", True) and prev not in (0, None) and latest > 0 and prev > 0:
        s += f"（{'+' if diff >= 0 else '−'}{abs(diff / prev * 100):.1f}%）"
    return s


def measure_label(spec):
    d = spec.get("display", "level")
    f = spec.get("freq", "M")
    base = spec["label_zh"]
    # 標籤本身已經寫了「年增率」「月增率」的就不再加，免得出現「年增率 年增率」
    if d == "mom":
        suf = {"M": " 月增率", "Q": " 季增率", "W": " 週增率"}.get(f, " 變動率")
        base += "" if suf.strip() in base else suf
    elif d == "yoy":
        base += "" if "年增率" in base else " 年增率"
    elif d == "diff":
        base += " 月變動" if f == "M" else " 變動"
    elif d == "sum12m":
        base += " 近4季合計" if f == "Q" else " 近12個月合計"
    elif d == "ratio" and spec.get("unit_out"):
        pass
    return base


# ---------- 讀資料 ----------
class Ctx:
    def __init__(self, today=None, data_dir=None, cal=None, status=None):
        self.today = today or dt.date.today()
        self.data_dir = data_dir
        self.cache = {}
        self.status = status if status is not None else store.load_status(data_dir)
        self.cal = cal if cal is not None else relcal.load()

    def raw(self, sid):
        if sid not in self.cache:
            self.cache[sid] = store.read(sid, self.data_dir)
        return self.cache[sid]


def stale_info(spec, ctx):
    """回傳 (是否過期, 訊息)。"""
    if spec.get("discontinued"):
        return False, None
    sid = spec["sid"]
    e = ctx.status.get(sid)
    base = spec.get("base_sid")
    if spec.get("derived"):
        msgs = [stale_info({"sid": x, "freq": spec.get("freq", "M")}, ctx) for x in spec["derived"]["sids"]]
        for s, m in msgs:
            if s:
                return True, m
        return False, None
    if not e or not e.get("last_date"):
        return True, "尚未抓到資料"
    last = e["last_date"]
    age = (ctx.today - dt.date.fromisoformat(last)).days
    thr = spec.get("stale_days") or STALE_DAYS.get(spec.get("freq", "M"), 110)
    err = e.get("last_error")
    if age > thr or err:
        last_txt = period_txt(last, spec.get("freq", "M"))
        if age <= thr and err:
            return True, f"資料可能過期，最新資料為 {last_txt}（最近一次抓取失敗，沿用舊資料）"
        return True, f"資料可能過期，最新資料為 {last_txt}" + ("（最近一次抓取失敗）" if err else "")
    return False, None


def compute_series(spec, ctx):
    """回傳這條序列在這張圖要畫的 [(date, value)]（已換算 display）。"""
    d = spec.get("derived")
    if d:
        base = transform.combine(d["op"], *[ctx.raw(x) for x in d["sids"]])
    else:
        base = ctx.raw(spec["sid"])
    if spec.get("clip_to_sid"):
        ref = ctx.raw(spec["clip_to_sid"])
        if ref:
            base = transform.clip_to(base, ref[-1][0])
    obs = transform.apply_display(base, spec, ctx.raw)
    if spec.get("freq") == "D":
        obs = transform.downsample_daily(obs, today=ctx.today)
    return obs


def kind_of(spec):
    d = spec.get("display", "level")
    if d == "stack":
        return "stack"
    if d in BAR_DISPLAYS:
        return "bar"
    return "line"


def round_v(v):
    a = abs(v)
    return round(v, 2) if a >= 1000 else round(v, 4)


def epoch_day(s):
    return (dt.date.fromisoformat(s) - dt.date(1970, 1, 1)).days


# ---------- 單張圖 ----------
def build_chart(country, chart, ctx):
    """回傳 (json 內容, summaries, card html)。"""
    series_json, sums = [], []
    visible = [s for s in chart["series"] if not s.get("hidden")]
    scatter = any(s.get("axis") in ("X", "Y") for s in visible)
    for i, spec in enumerate(visible):
        obs = compute_series(spec, ctx)
        sid_id = f"{spec['sid']}:{spec.get('display', 'level')}"
        stale, smsg = stale_info(spec, ctx)
        item = {"id": sid_id, "label": measure_label(spec), "axis": spec.get("axis", "L"),
                "kind": kind_of(spec), "u": short_unit(unit_of(spec))}
        # tooltip 的小數位跟卡片一致：年增率 1 位、月增率／比率／百分比 2 位，其餘依數值大小（db.js fmt）
        d_ = spec.get("display", "level")
        if d_ == "yoy":
            item["nd"] = 1
        elif d_ in ("mom", "ratio") or unit_of(spec).startswith("%"):
            item["nd"] = 2
        elif unit_nd(spec) is not None:
            item["nd"] = unit_nd(spec)
        if is_light(spec):
            item["light"] = True
            item["u"] = ""
        if obs:
            item["d"] = [epoch_day(k) for k, _ in obs]
            item["v"] = [round_v(v) for _, v in obs]
            if (dt.date.fromisoformat(obs[-1][0]) - ctx.today).days > 30:
                item["future"] = True
        else:
            item["d"], item["v"] = [], []
        series_json.append(item)
        sums.append(summary(spec, obs, stale, smsg, ctx, i, chart))
    jd = {"series": [s for s in series_json if s["d"]]}
    if scatter:
        jd["scatter"] = True
    return jd, sums, card_html(country, chart, visible, sums, series_json, ctx)


def summary(spec, obs, stale, smsg, ctx, idx, chart):
    freq = spec.get("freq", "M")
    out = {"sid": spec["sid"], "label": measure_label(spec), "unit": short_unit(unit_of(spec)),
           "stale": stale, "stale_msg": smsg, "idx": idx, "chart_key": chart["key"],
           "chart_title": chart["title_zh"], "spec": spec}
    if spec.get("note"):
        out["note"] = spec["note"]
    nxt = None
    if spec.get("release") and ctx.cal:
        nxt = relcal.next_date(ctx.cal, spec["release"], ctx.today)
    out["next"] = nxt
    if not obs:
        out["latest"] = None
        return out
    d, v = obs[-1]
    out.update(latest=v, latest_date=d, latest_txt=vtxt(v, spec), period=period_txt(d, freq))
    if len(obs) >= 2:
        pd_, pv = obs[-2]
        out.update(prev_txt=vtxt(pv, spec), prev_period=period_txt(pd_, freq), change=change_txt(v, pv, spec, signed=any(x < 0 for _, x in obs)))
    return out


PAL = ['#1e3a5f', '#b8924a', '#2a9d8f', '#c0392b', '#7c5cbf', '#4f8a3a', '#e07b39', '#5a7a9a', '#8c564b', '#17becf']


def src_line(visible):
    seen, parts = set(), []
    for s in visible:
        lic = s.get("license", "public")
        key = (s.get("source", ""), lic)
        if key in seen:
            continue
        seen.add(key)
        t = s.get("source", "")
        if lic and lic != "public":
            owner = lic.split(":", 1)[1] if ":" in lic else lic
            owner = owner.split("（")[0]
            t += f"（版權屬 {owner}）"
        parts.append(t)
    return "；".join(parts)


def weekday(date_s):
    return WD[dt.date.fromisoformat(date_s).weekday()]


def card_html(country, chart, visible, sums, series_json, ctx):
    h = [f'<section class="card" id="{esc(chart["key"])}">', f'<h3>{esc(hspace(chart["title_zh"]))}</h3>']
    if chart.get("definition"):
        h.append(f'<div class="def">{esc(hspace(chart["definition"]))}</div>')
    h.append('<div class="tools"><div class="rng">'
             '<button type="button" data-r="1">1 年</button><button type="button" data-r="5" class="on">5 年</button>'
             '<button type="button" data-r="10">10 年</button><button type="button" data-r="0">全部</button></div>'
             '<div class="legend"></div></div>')
    h.append(f'<div class="chart" data-key="{esc(chart["key"])}" data-range="5"></div>')
    h.append('<div class="srows">')
    for i, (spec, sm) in enumerate(zip(visible, sums)):
        col = PAL[i % len(PAL)]
        un = sm["unit"]
        note = spec.get("use_note")
        nm = f'<i style="background:{col}"></i><b>{esc(hspace(sm["label"]))}</b>'
        if un:
            nm += f'<span class="un">單位：{esc(un)}</span>'
        if note and not note.startswith(NO_NOTE_PREFIX):
            nm += f'<span class="un">（{esc(hspace(note))}）</span>'
        vals = []
        if sm.get("latest") is None:
            vals.append('<span class="k">尚無資料</span>')
        else:
            vals.append(f'<span><span class="k">最新</span> {esc(hspace(sm["period"]))}　<b>{esc(sm["latest_txt"])}</b></span>')
            if sm.get("prev_txt"):
                vals.append(f'<span><span class="k">前值</span> {esc(sm["prev_txt"])}（{esc(hspace(sm["prev_period"]))}）</span>')
                vals.append(f'<span><span class="k">變動</span> {esc(hspace(sm["change"]))}</span>')
        if sm.get("next"):
            vals.append(f'<span><span class="k">下次公布</span> {sm["next"]}（週{weekday(sm["next"])}）</span>')
        row = f'<div class="srow"><div class="nm">{nm}</div><div class="vals">{"".join(vals)}</div>'
        if sm["stale"]:
            row += f'<div class="stale">{esc(hspace(sm["stale_msg"]))}</div>'
        if spec.get("discontinued"):
            row += f'<div class="stale">{esc(spec["discontinued"])}</div>'
        row += "</div>"
        h.append(row)
    h.append("</div>")
    notes = []
    for s in visible:
        if s.get("history_note"):
            notes.append(f'{measure_label(s)}：{s["history_note"]}')
        if s.get("self_calc") and not chart.get("definition"):
            notes.append(f'{measure_label(s)} 為自算指標')
    h.append('<div class="src">')
    h.append(f'<p>資料來源：{esc(hspace(src_line(visible)))}</p>')
    for n in notes:
        h.append(f'<p>{esc(hspace(n))}</p>')
    h.append("</div></section>")
    return "\n".join(h)


# ---------- 頁面外框 ----------
def nav_block():
    """全站選單從 scripts/site_nav.py 產生，高亮「市場 ▾ 總經資料庫」；與 site_nav.py 重注入的結果逐字相同。"""
    try:
        import site_nav
        return site_nav.full_nav_block("market", "macrodb")
    except Exception:  # noqa: BLE001
        return ""


def page(title, body, base, extra_head="", scripts=""):
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Playfair+Display:wght@600;700&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/imq-base.css">
<link rel="stylesheet" href="{base}db.css">
{extra_head}
</head>
<body>
{nav_block()}
<div class="container">
{body}
<footer class="imq-foot">
<div>© 2026 InvestMQuest Research</div>
<div><a href="/disclosures.html">方法論與揭露</a> · 數據版權屬各來源機構 · 本站內容僅供研究參考，不構成投資建議</div>
</footer>
</div>
{scripts}
</body>
</html>
"""


def country_seg(country, active_on_index=False):
    a = []
    for c in ("us", "tw"):
        cls = "on" if c == country else ""
        a.append(f'<a class="{cls}" href="/macro/db/{"#" + c if c == "tw" else ""}">{COUNTRY_NAME[c]}</a>')
    return '<div class="seg">' + "".join(a) + "</div>"


def category_page(country, cat, cats, ctx, all_cats_present):
    charts = sorted(cat["charts"], key=lambda c: (c["priority"], cat["charts"].index(c)))
    cards, jdata, sums_all = [], {}, []
    for ch in charts:
        jd, sums, card = build_chart(country, ch, ctx)
        jdata[ch["key"]] = jd
        cards.append(card)
        sums_all.append((ch, sums))
    grp = cat.get("group")
    shown = [c for c in cats if c["charts"] and c.get("group") == grp]
    pills = "".join(f'<a class="{"on" if c["key"] == cat["key"] else ""}" href="/macro/db/{country}/{c["key"]}.html">{esc(c["name_zh"])}</a>'
                    for c in shown)
    pills = f'<div class="pills">{pills}</div>'
    if grp:
        # 一區有好幾國（東南亞）：上排選國家（連到該國第一類），下排是這一國的大類
        firsts = {}
        for c in cats:
            if c["charts"] and c.get("group"):
                firsts.setdefault(c["group"], c["key"])
        grow = "".join(f'<a class="{"on" if g == grp else ""}" href="/macro/db/{country}/{k}.html">{esc(g)}</a>' for g, k in firsts.items())
        pills = f'<div class="pills grp">{grow}</div>' + pills
    place = grp if cat.get("part") else COUNTRY_NAME[country]
    mid = f'{esc(grp)} / ' if cat.get("part") else ""
    n = len(charts)
    body = (f'<div class="crumb"><a href="/">首頁</a> / <a href="/macro/">總經</a> / <a href="/macro/db/">資料庫</a> / '
            f'<a href="/macro/db/#{country}">{COUNTRY_NAME[country]}</a> / {mid}{esc(cat["name_zh"])}</div>'
            f'<div class="overline">Macro Database · {country.upper()}</div>'
            f'<h1>{esc(place)}　{esc(cat["name_zh"])}</h1>'
            f'<p class="sub">{n} 張圖。資料每日自官方來源更新，歷史完整保存；數字都標了期間與單位，年增率按日期對齊去年同期。</p>'
            f'{pills}' + "\n".join(cards))
    scripts = f'<script src="../db.js"></script>\n<script>MacroDB.start("../data/{country}/{cat["key"]}.json");</script>'
    return (page(f"{place}　{cat['name_zh']} — 總經資料庫", body, "../", scripts=scripts),
            {"asof": ctx.today.isoformat(), "charts": jdata}, sums_all)


# ---------- 總覽 ----------
def area_names(built):
    names = [COUNTRY_NAME[c] for c in COUNTRY_NAME if c in built]
    return names[0] if len(names) == 1 else "、".join(names[:-1]) + "與" + names[-1]


def overview(countries, built, ctx):
    secs = []
    for c in COUNTRY_NAME:
        if c not in built:
            continue
        cat = built[c]["cat"]
        sums_by_cat = built[c]["sums"]
        grid, groups = [], {}
        for k in cat["categories"]:
            if not k["charts"]:
                continue
            rows = []
            for ch, sums in sums_by_cat[k["key"]][:3]:
                s = next((x for x in sums if x.get("latest") is not None), None)
                if s:
                    rows.append(f'<div class="kv"><span>{esc(hspace(s["label"]))}</span><b>{esc(s["latest_txt"])}<br>'
                                f'<small class="note">{esc(hspace(s["period"]))}</small></b></div>')
            card = (f'<a class="cat" href="/macro/db/{c}/{k["key"]}.html"><div class="t">{esc(k["name_zh"])}</div>'
                    f'<div class="n">{len(k["charts"])} 張圖</div>{"".join(rows)}</a>')
            if k.get("group"):
                groups.setdefault(k["group"], []).append(card)
            else:
                grid.append(card)
        blocks = f'<div class="grid">{"".join(grid)}</div>' if grid else ""
        # 有分國家的區（東南亞）：每國一段，標題是國名
        blocks += "".join(f'<h2 class="grph">{esc(g)}</h2><div class="grid">{"".join(cs)}</div>' for g, cs in groups.items())
        secs.append(f'<div data-sec="{c}" class="{"hide" if c != "us" else ""}">{blocks}'
                    f'{recent_html(c, built[c], ctx)}{upcoming_html(c, ctx)}{stale_html(c, built[c], ctx)}</div>')
    tabs = ""
    for c in (c for c in COUNTRY_NAME if c in built):
        tabs += f'<button type="button" data-c="{c}" class="{"on" if c == "us" else ""}{"" if c in built else " off"}">{COUNTRY_NAME[c]}</button>'
    body = ('<div class="crumb"><a href="/">首頁</a> / <a href="/macro/">總經</a> / 資料庫</div>'
            '<div class="overline">Macro Database</div>'
            '<h1>總經資料庫</h1>'
            f'<p class="sub">{area_names(built)}的總體經濟數據，全部取自官方原始來源，完整歷史保存，每日自動更新。只提供看圖，不提供下載。</p>'
            f'<div class="seg">{tabs}</div>' + "".join(secs))
    scripts = '<script src="db.js"></script>\n<script>MacroDB.country();</script>'
    return page("總經資料庫 — InvestMQuest Research", body, "", scripts=scripts)


def recent_html(c, b, ctx):
    items = []
    seen = set()
    firsts = {}
    for k, lst in b["sums"].items():
        for ch, sums in lst:
            for s in sums:
                firsts.setdefault(s["sid"], (k, ch, s))
    adv = [(e.get("advanced"), sid) for sid, e in ctx.status.items() if e.get("advanced") and sid in firsts]
    adv.sort(reverse=True)
    for ts, sid in adv:
        day = ts[:10]
        if (ctx.today - dt.date.fromisoformat(day)).days > 14 or len(items) >= 15:
            continue
        k, ch, s = firsts[sid]
        if s.get("latest") is None:
            continue
        items.append(f'<li><span class="d">{day}</span><a href="/macro/db/{c}/{k}.html#{esc(ch["key"])}">{esc(hspace(ch["title_zh"]))}</a>'
                     f'　{esc(hspace(s["label"]))}　{esc(hspace(s["period"]))}　<b>{esc(s["latest_txt"])}</b></li>')
    if not items:
        return '<h2>最近公布</h2><div class="panel note">近 14 天沒有新公布的數據。資料庫從 2026 年 10 月 8 日起記錄公布時間，之後每次有新數據都會列在這裡。</div>'
    return '<h2>最近公布</h2><div class="panel"><ul>' + "".join(items) + "</ul></div>"


def upcoming_html(c, ctx):
    if c != "us":
        return f'<h2>即將公布</h2><div class="panel note">{COUNTRY_NAME[c]}的公布日行事曆還沒有建置。</div>'
    if not ctx.cal:
        return ""
    today = ctx.today
    end = today + dt.timedelta(days=14)
    rows = []
    weekly = {"claims", "pmms", "h41", "h8"}
    for k, v in ctx.cal.get("releases", {}).items():
        ds = [d for d in v["dates"] if today.isoformat() <= d <= end.isoformat()]
        if k in weekly:
            ds = ds[:1]
        for d in ds:
            rows.append((d, v["name_zh"], k))
    rows.sort()
    if not rows:
        return ""
    li = "".join(f'<li><span class="d">{d}（週{weekday(d)}）</span>{esc(n)}</li>' for d, n, _ in rows)
    return f'<h2>即將公布（未來 14 天）</h2><div class="panel"><ul>{li}</ul><p class="note">日期來自 BLS、Census、BEA、聯準會的官方時程；每週更新一次。</p></div>'


def stale_html(c, b, ctx):
    seen, rows = set(), []
    for k, lst in b["sums"].items():
        for ch, sums in lst:
            for s in sums:
                if s["stale"] and s["sid"] not in seen:
                    seen.add(s["sid"])
                    rows.append((k, ch, s))
    if not rows:
        return '<h2>資料異常提示</h2><div class="panel note">目前所有序列都在預期的更新週期內。</div>'
    li = "".join(f'<li><a href="/macro/db/{c}/{k}.html#{esc(ch["key"])}">{esc(hspace(ch["title_zh"]))}</a>　{esc(hspace(s["label"]))}　'
                 f'<span class="w">{esc(hspace(s["stale_msg"]))}</span></li>' for k, ch, s in rows)
    return f'<h2>資料異常提示</h2><details class="panel"{" open" if len(rows) <= 10 else ""}><summary>{len(rows)} 條序列可能過期</summary><ul>{li}</ul></details>'


# ---------- 主流程 ----------
def load_catalog(country):
    return catalog_io.load_catalog(country, CATALOG_DIR)


def redirect_page(country, new_key):
    """舊網址（大類改名或拆開後）轉到新頁。"""
    u = f"/macro/db/{country}/{new_key}.html"
    return ('<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={u}"><link rel="canonical" href="https://research.investmquest.com{u}">'
            f'<title>此頁已搬家 — 總經資料庫</title></head><body><p>此頁已搬到 <a href="{u}">新位置</a>。</p></body></html>\n')


def write_if_changed(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def render_all(countries=tuple(COUNTRY_NAME), ctx=None, docs=None):
    global DOCS
    docs = Path(docs) if docs else DOCS
    ctx = ctx or Ctx()
    built = {}
    for c in countries:
        cat = load_catalog(c)
        if not cat:
            continue
        sums_by_cat = {}
        for k in cat["categories"]:
            if not k["charts"]:
                continue
            html_, jdata, sums = category_page(c, k, cat["categories"], ctx, True)
            write_if_changed(docs / c / (k["key"] + ".html"), html_)
            write_if_changed(docs / "data" / c / (k["key"] + ".json"), json.dumps(jdata, ensure_ascii=False, separators=(",", ":")))
            sums_by_cat[k["key"]] = sums
        for old, new in cat.get("redirects", {}).items():
            write_if_changed(docs / c / (old + ".html"), redirect_page(c, new))
        built[c] = {"cat": cat, "sums": sums_by_cat}
    for name in ("db.css", "db.js"):
        write_if_changed(docs / name, (WEB_DIR / name).read_text(encoding="utf-8"))
    write_if_changed(docs / "index.html", overview(countries, built, ctx))
    print("render 完成：%s" % "、".join("%s %d 類" % (COUNTRY_NAME[c], len(b["sums"])) for c, b in built.items()))
    return built
