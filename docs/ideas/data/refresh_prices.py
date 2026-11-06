#!/usr/bin/env python3
"""想法頁靜態「市場已反映」股價表：每天重算純價格欄（2026-11-01 草稿，尚未接進 workflow）。

重算的只有純價格欄（今年以來、距 52 週高、某日以來、均線距離…）。盈餘預估、本益比、營收倍數、
「所以呢」等欄一律不碰；正文引用的數字也不碰（月檢視處理）。

用法（repo 根目錄）
  python3 docs/ideas/data/refresh_prices.py --dry-run          只印 diff，並寫預覽到 PREVIEW_DIR/<page>.diff
  python3 docs/ideas/data/refresh_prices.py --add-markers      第一次：替既有表加 <!-- prices:<name>:start/end --> 標記
  python3 docs/ideas/data/refresh_prices.py --apply            重算並寫檔（頁面沒有標記的表會略過並警告）
  選項：--tables a,b 只跑指定表；--asof YYYY-MM-DD 用指定日當「最新」（核對用）；
        --include-manual 讓 --apply 也處理 autorun=False 的表（預設不處理，原因見 SPEC 的 note）

設計
  - 標記與先例 bond-outlook/data.py 一致：<!-- prices:NAME:start -->…<!-- prices:NAME:end -->，各恰好一次；
    資料日期用 <!-- prices-asof:NAME.K:start -->…end --> 包住。重複套用結果不變（_write_if_changed）。
  - 只改標記內每列 <td> 的指定欄，其他欄、標籤欄（連結）原樣保留；列順序與 SPEC 不一致就整表不動。
  - 價格來源：~/v7-backtest/data/price_store 存在就先用（唯讀，不下載）；缺的代號、或雲端 CI 沒有該庫，
    改用 yfinance（auto_adjust=False，close＝拆股調整未調息、adj_close＝含息還原）。
  - 任何代號抓不到或資料日落後：該列保留舊值、記 stale，不讓整表失敗；預設永遠 exit 0（--strict 例外）。
  - 漲跌幅以 float 算後 ROUND_HALF_UP 到顯示位數；列順序、日期用字串比對。
  - semis-degross 另寫 drawdown_table.csv 與 data.json 的 c2（同源，一起更新）。
"""
from __future__ import annotations

import argparse
import difflib
import html as htmllib
import json
import re
import os
import sys
import tempfile
import warnings
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve().parent
IDEAS = HERE.parent
# 預覽只給本機看；原本寫死某次對話的暫存路徑，CI 上建不了資料夾，整支在寫表前就中止（11-02～11-06）。
PREVIEW_DIR = Path(os.environ.get("REFRESH_PRICES_PREVIEW_DIR") or Path(tempfile.gettempdir()) / "refresh_prices_preview")
STORE_DIR = Path.home() / "v7-backtest" / "data" / "price_store" / "daily"
MINUS = "−"
ASIA_SUFFIX = (".T", ".SS", ".SZ", ".KS", ".TW", ".HK")

# ─────────────────────────── SPEC ───────────────────────────
# cols: {欄位索引(0 起算，含標籤欄): (計算, 格式)}
#   計算：ytd | from_52w_high | window_from:YYYY-MM-DD | close | ma50_pct | ma200_pct |
#         from_low_between:a,b | one_month | d1 | w1 | high_date
#   格式：pct0（+210%）| pct1（+16.2%）| pct0_suffix（+78%（美元），後綴取 row 的第 3 個值）
#         | pct1_posneg（半導體表：class pos/neg）| pct1_nocls | md（06/22）
# rows: (html 第一欄文字, 代號, 後綴)；代號 None 表示該列不重算（布蘭特、美元指數）
# field：close（拆股調整未調息）或 adj_close（還原含息），照各頁原口徑，已用頁面現有數字回算確認。
# asof：(整段錨點文字, 錨點內要換的日期字串, 格式)；錨點必須在頁面恰好出現一次
SPEC = {
    "ai-scissors": {
        "page": "ai-scissors.html", "autorun": True, "field": "close", "ref": "MU",
        "locate": "<h2>市場已反映什麼（截至",
        "rows": [
            ("美光（記憶體）", "MU", None), ("SK 海力士", "000660.KS", None), ("三星電子", "005930.KS", None),
            ("GE Vernova（發電設備）", "GEV", None), ("Siemens Energy", "ENR.DE", None), ("AMD（CPU）", "AMD", None),
            ("Intel", "INTC", None), ("Arm", "ARM", None), ("台積電 ADR（晶圓代工）", "TSM", None),
            ("Nebius（GPU 雲）", "NBIS", None), ("CoreWeave", "CRWV", None),
        ],
        "cols": {1: ("ytd", "pct0"), 2: ("from_52w_high", "pct0"), 3: ("window_from:2026-07-14", "pct0")},
        "asof": [
            ("市場已反映什麼（截至 10/30）", "10/30", "m/d"),
            ("股價截至 10/30 收盤；共識預估", "10/30", "m/d"),
            ("<th>7/14 至 10/30 股價</th>", "10/30", "m/d"),
            ("股價三欄是 10/30 收盤", "10/30", "m/d"),
            ("7/14 至 10/30 股價三欄", "10/30", "m/d"),
        ],
        "note": "Siemens Energy 那句『沒有 10/30 收盤資料』11-07 已刪（該列已有收盤）；正文 L309 引用表中數字不更新。",
    },
    "consumer-agents": {
        "page": "consumer-agents.html", "autorun": True, "field": "close", "ref": "AMD",
        "locate": "<h2>股價已經反映多少</h2>",
        "rows": [
            ("AMD", "AMD", None), ("Intel", "INTC", None), ("Cloudflare", "NET", None), ("Visa", "V", None),
            ("Mastercard", "MA", None), ("PayPal", "PYPL", None), ("Shopify", "SHOP", None), ("Meta", "META", None),
            ("Arm", "ARM", None),
        ],
        "cols": {1: ("window_from:2026-07-14", "pct1")},
        "asof": [
            ("股價欄截至 2026-10-30 收盤", "2026-10-30", "Y-m-d"),
            ("7/14 至 10/30 股價", "10/30", "m/d"),
            ("股價欄為 7 月 14 日至 10 月 30 日", "10 月 30 日", "zh_md"),
        ],
        "note": "表後第一段正文（Shopify、PayPal 漲 25.3%…）引用表中數字，不更新；L342-353 另一張表標題含數字，不碰。",
    },
    "china-litho": {
        "page": "china-litho.html", "autorun": False, "field": "close", "ref": "ASML", "asia_shift": True,
        "locate": "<h2>市場已反映什麼</h2>",
        "rows": [
            ("ASML", "ASML", "美元"), ("應材", "AMAT", "美元"), ("科林", "LRCX", "美元"), ("科磊", "KLAC", "美元"),
            ("東京威力科創", "8035.T", "日圓"), ("北方華創", "002371.SZ", "人民幣"), ("中微", "688012.SS", "人民幣"),
            ("費城半導體指數", "^SOX", None),
        ],
        "cols": {1: ("window_from:2025-10-14", "pct0_suffix")},
        "asof": [("股價漲幅（2025-10-14 至 2026-10-12）", "2026-10-12", "Y-m-d")],
        "note": "autorun=False：同表的本益比、預估本益比欄與前後正文（平均漲 104%、相關係數 0.83～0.89）都停在 10/12，"
                "只更新股價會讓表內口徑混在一起。亞洲代號起訖日用『下一個交易日』（頁面現有數字就是這樣對的），見 asia_shift。",
    },
    "semis-degross": {
        "page": "semis-degross.html", "autorun": True, "field": "adj_close", "ref": "SMH", "csv": True,
        "locate": "<th>離 52 週高</th>",
        "rows": [
            ("費城半導體", "^SOX", None), ("SMH", "SMH", None), ("QQQ", "QQQ", None), ("S&P 500", "^GSPC", None),
            ("NVDA", "NVDA", None), ("AMD", "AMD", None), ("AVGO", "AVGO", None), ("MU", "MU", None), ("TSM", "TSM", None),
            ("ASML", "ASML", None), ("AMAT", "AMAT", None), ("LRCX", "LRCX", None), ("KLAC", "KLAC", None),
            ("MRVL", "MRVL", None), ("ARM", "ARM", None), ("QCOM", "QCOM", None), ("INTC", "INTC", None),
            ("SMCI", "SMCI", None), ("VRT", "VRT", None), ("ORCL", "ORCL", None), ("CRWV", "CRWV", None),
        ],
        "cols": {1: ("from_52w_high", "pct1_posneg"), 2: ("high_date", "md"), 3: ("d1", "pct1_posneg"),
                 4: ("one_month", "pct1_posneg"), 5: ("ytd", "pct1_posneg"), 6: ("ma50_pct", "pct1_posneg"),
                 7: ("ma200_pct", "pct1_posneg"), 8: ("from_low_between:2026-06-22,2026-10-15", "pct1_nocls")},
        "asof": [
            ("10/30 當日", "10/30", "m/d"),
            ("還原收盤，截至 2026-10-30。", "2026-10-30", "Y-m-d"),
            ("資料：共用價格庫，截至 2026-10-30。", "2026-10-30", "Y-m-d"),  # 緊接在 c2 橫條圖下方，c2 與表同源
        ],
        "note": "同時寫 drawdown_table.csv 與 data.json 的 c2。c2 canvas 的 aria-label（L261，含 CoreWeave −60% 等數字）與"
                "正文 L256 是手寫，不更新。『距 6～10 月低點』的低點窗固定 06-22～10-15，只有分子（最新價）會變。",
    },
    "bond-repricing": {
        "page": "bond-repricing.html", "autorun": False, "field": "adj_close", "ref": "SPY",
        "locate": "<h3>已定價：利率管道</h3>",
        "rows": [
            ("半導體 SOXX", "SOXX", None), ("那斯達克 100 QQQ", "QQQ", None), ("S&P 500 SPY", "SPY", None),
            ("等權重 RSP", "RSP", None), ("羅素 2000 IWM", "IWM", None), ("區域銀行 KRE", "KRE", None),
            ("房屋建商 XHB", "XHB", None), ("20 年以上公債 TLT", "TLT", None), ("綜合債券 AGG", "AGG", None),
            ("投資級公司債 LQD", "LQD", None), ("高收益債 HYG", "HYG", None), ("新興市場美元債 EMB", "EMB", None),
            ("短期公債 SHY", "SHY", None),
            ("布蘭特原油", None, None), ("美元指數", None, None),  # 頁面口徑與 BZ=F、DX-Y.NYB 對不上（差 0.4～0.6pp），保持原樣
        ],
        "cols": {1: ("window_from:2026-08-13", "pct1"), 2: ("ytd", "pct1")},
        "asof": [("8/13 收盤到 10/5 收盤", "10/5", "m/d")],
        "note": "autorun=False：頁面整段（SPY 距高點 0.1%、KRE 對 TLT 比值、高收益債 −0.2% 等正文）都是 10/5 的口徑，"
                "只動表會與正文互相矛盾。表是含息還原價（adj_close）。",
    },
}


# ─────────────────────────── 價格 ───────────────────────────
def warn(msg):
    print(f"[refresh_prices] 警告：{msg}", file=sys.stderr)


def info(msg):
    print(f"[refresh_prices] {msg}", file=sys.stderr)


class Prices:
    """代號 → DataFrame(index=date, close, adj_close)。先看本機共用庫（唯讀），缺的才 yfinance。"""

    def __init__(self, tickers):
        self.data, self.source = {}, {}
        self._load(sorted(set(tickers)))

    def _load(self, tickers):
        import pandas as pd
        need = []
        for t in tickers:
            p = STORE_DIR / f"{t}.parquet"
            if p.exists():
                try:
                    d = pd.read_parquet(p)
                    d["date"] = pd.to_datetime(d["date"])
                    self.data[t] = d.set_index("date")[["close", "adj_close"]].dropna(how="all")
                    self.source[t] = "price_store"
                    continue
                except Exception as e:  # noqa: BLE001
                    warn(f"{t} 共用庫讀取失敗：{e}")
            need.append(t)
        if need:
            self._yf(need)

    def _yf(self, tickers):
        import pandas as pd
        try:
            import yfinance as yf
        except Exception as e:  # noqa: BLE001
            warn(f"沒有 yfinance，{tickers} 抓不到：{e}")
            return
        start = f"{date.today().year - 1}-01-01"
        df = None
        for attempt in range(3):
            try:
                df = yf.download(tickers, start=start, auto_adjust=False, progress=False, threads=False)
                if df is not None and not df.empty:
                    break
            except Exception as e:  # noqa: BLE001
                warn(f"yfinance 第 {attempt + 1} 次失敗：{type(e).__name__}: {e}")
        if df is None or df.empty:
            return
        for t in tickers:
            try:
                if isinstance(df.columns, pd.MultiIndex):
                    c, a = df["Close"][t], df["Adj Close"][t]
                else:
                    c, a = df["Close"], df["Adj Close"]
                d = pd.DataFrame({"close": c, "adj_close": a}).dropna(how="all")
                d.index = pd.to_datetime(d.index).tz_localize(None)
                if len(d):
                    self.data[t], self.source[t] = d, "yfinance"
            except Exception as e:  # noqa: BLE001
                warn(f"{t} yfinance 無資料：{type(e).__name__}: {e}")


def _round(x, nd):
    return Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)


def calc(series, kind, asof, asia_shift=False):
    """series：pandas Series（升序、index=日期）。回傳 (數值或日期字串, 實際最後一根日期)。
    asia_shift：亞洲代號的起訖日取『指定日之後第一根』（沒有就取最後一根）——china-litho 現有數字是這樣對的。"""
    import pandas as pd
    asof_ts = pd.Timestamp(asof)
    if asia_shift:
        later = series[series.index > asof_ts]
        s = series[: later.index[0]] if len(later) else series[:asof_ts]
    else:
        s = series[:asof_ts]
    s = s.dropna()
    last, end = float(s.iloc[-1]), s.index[-1]
    if kind == "close":
        return last, end
    if kind == "ytd":
        base = s[: pd.Timestamp(year=asof_ts.year - 1, month=12, day=31)]
        return (last / float(base.iloc[-1]) - 1) * 100, end
    if kind == "high_date":
        return s.iloc[-252:].idxmax().strftime("%m/%d"), end
    if kind == "from_52w_high":
        return (last / float(s.iloc[-252:].max()) - 1) * 100, end
    if kind.startswith("window_from:"):
        d0 = pd.Timestamp(kind.split(":", 1)[1])
        base = s[s.index > d0].iloc[:1] if asia_shift else s[:d0].iloc[-1:]
        if base.empty:
            raise ValueError(f"{kind} 沒有基期價")
        return (last / float(base.iloc[0]) - 1) * 100, end
    if kind == "ma50_pct":
        return (last / float(s.iloc[-50:].mean()) - 1) * 100, end
    if kind == "ma200_pct":
        return (last / float(s.iloc[-200:].mean()) - 1) * 100, end
    if kind == "one_month":  # 21 個交易日前（與 drawdown_table.csv 現有口徑一致）
        return (last / float(s.iloc[-22]) - 1) * 100, end
    if kind == "d1":
        return (last / float(s.iloc[-2]) - 1) * 100, end
    if kind == "w1":
        return (last / float(s.iloc[-6]) - 1) * 100, end
    if kind.startswith("from_low_between:"):
        a, b = kind.split(":", 1)[1].split(",")
        return (last / float(s[pd.Timestamp(a):pd.Timestamp(b)].min()) - 1) * 100, end
    raise ValueError(f"不認得的計算 {kind}")


# ─────────────────────────── 格式 ───────────────────────────
def fmt_pct(v, nd):
    d = _round(v, nd)
    if d == 0:
        return f"{0:.{nd}f}%"
    return ("+" if d > 0 else MINUS) + f"{abs(d):.{nd}f}%"


def cls_of(v, nd):
    d = _round(v, nd)
    return "pos" if d > 0 else "neg" if d < 0 else ""


def render_cell(attrs, fmt, value, suffix):
    if fmt == "pct0":
        return f"<td{attrs}>{fmt_pct(value, 0)}</td>"
    if fmt == "pct1":
        return f"<td{attrs}>{fmt_pct(value, 1)}</td>"
    if fmt == "pct0_suffix":
        return f"<td{attrs}>{fmt_pct(value, 0)}" + (f"（{suffix}）" if suffix else "") + "</td>"
    if fmt == "pct1_posneg":
        c = cls_of(value, 1)
        return f'<td class="{c}">{fmt_pct(value, 1)}</td>' if c else f"<td>{fmt_pct(value, 1)}</td>"
    if fmt == "pct1_nocls":
        return f"<td>{fmt_pct(value, 1)}</td>"
    if fmt == "md":
        return f"<td{attrs}>{value}</td>"
    raise ValueError(fmt)


def fmt_date(d, how):
    if how == "m/d":
        return f"{d.month}/{d.day}"
    if how == "Y-m-d":
        return d.isoformat()
    if how == "zh_md":
        return f"{d.month} 月 {d.day} 日"
    raise ValueError(how)


# ─────────────────────────── 標記 ───────────────────────────
def marks(name):
    return f"<!-- prices:{name}:start -->", f"<!-- prices:{name}:end -->"


def asof_marks(name, k):
    return f"<!-- prices-asof:{name}.{k}:start -->", f"<!-- prices-asof:{name}.{k}:end -->"


def _replace_between(text, mk, body):
    a, b = mk
    if text.count(a) != 1 or text.count(b) != 1 or text.index(a) > text.index(b):
        raise ValueError(f"頁面缺少唯一的標記 {a}／{b}")
    return text[: text.index(a) + len(a)] + body + text[text.index(b):]


def _write_if_changed(path, text):
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<td([^>]*)>(.*?)</td>", re.S)


def label_of(cell_inner):
    return htmllib.unescape(re.sub(r"<[^>]+>", "", cell_inner)).strip()


def add_markers(text, name, spec):
    """替既有表加標記：找 locate 之後第一個 <tbody>…</tbody>，列順序與 SPEC 一致才包。"""
    a, b = marks(name)
    if a in text:
        return text, "已有標記"
    n = text.count(spec["locate"])
    if n != 1:
        raise ValueError(f"locate 錨點出現 {n} 次（要恰好 1 次）：{spec['locate']}")
    i = text.index(spec["locate"])
    t0 = text.index("<tbody>", i) + len("<tbody>")
    t1 = text.index("</tbody>", t0)
    labels = [label_of(CELL_RE.search(r).group(2)) for r in ROW_RE.findall(text[t0:t1])]
    want = [r[0] for r in spec["rows"]]
    if labels != want:
        raise ValueError(f"列順序與 SPEC 不一致：頁面 {labels}；SPEC {want}")
    return text[:t0] + a + text[t0:t1] + b + text[t1:], "已加標記"


def add_asof_markers(text, name, spec):
    for k, (anchor, dtext, _fmt) in enumerate(spec["asof"]):
        sa, sb = asof_marks(name, k)
        if sa in text:
            continue
        if text.count(anchor) != 1 or anchor.count(dtext) != 1:
            raise ValueError(f"asof 錨點需在頁面恰好出現一次且含日期一次：{anchor}（頁面 {text.count(anchor)} 次）")
        text = text.replace(anchor, anchor.replace(dtext, sa + dtext + sb))
    return text


# ─────────────────────────── 重算 ───────────────────────────
def refresh_table(text, name, spec, px, asof, report):
    a, b = marks(name)
    i, j = text.index(a) + len(a), text.index(b)
    block = text[i:j]
    rows = ROW_RE.findall(block)
    if [label_of(CELL_RE.search(r).group(2)) for r in rows] != [r[0] for r in spec["rows"]]:
        raise ValueError("標記內列順序與 SPEC 不一致，整表不動")
    shift = spec.get("asia_shift", False)
    out, stale_rows = block, []
    for (label, ticker, suffix), row_html in zip(spec["rows"], rows):
        if ticker is None:
            continue
        try:
            ser = px.data.get(ticker)
            if ser is None:
                raise LookupError("無價格資料")
            s = ser[spec["field"]].dropna()
            is_asia = shift and ticker.endswith(ASIA_SUFFIX)
            cells = list(CELL_RE.finditer(row_html))
            vals = {}
            for ci, (kind, fmt) in spec["cols"].items():  # 先全部算完，任何一欄失敗整列保留舊值
                v, end = calc(s, kind, asof, asia_shift=is_asia)
                if not is_asia and (datetime.fromisoformat(asof) - end.to_pydatetime()).days > 4:
                    raise LookupError(f"最新一根 {end.date()} 比 asof {asof} 落後超過 4 天")
                vals[ci] = (v, fmt)
            new_row = row_html
            for ci in sorted(vals, reverse=True):
                m = cells[ci]
                new_row = new_row[: m.start()] + render_cell(m.group(1), vals[ci][1], vals[ci][0], suffix) + new_row[m.end():]
            out = out.replace(row_html, new_row, 1)
            report.setdefault(name, {})[label] = {spec["cols"][c][0]: vals[c][0] for c in vals}
        except Exception as e:  # noqa: BLE001
            stale_rows.append(label)
            warn(f"[{name}] {label}（{ticker}）保留舊值、標 stale：{type(e).__name__}: {e}")
    text = text[:i] + out + text[j:]
    if len(stale_rows) < len([r for r in spec["rows"] if r[1]]):  # 整表都失敗才不動日期
        for k, (_anchor, _dtext, how) in enumerate(spec["asof"]):
            text = _replace_between(text, asof_marks(name, k), fmt_date(datetime.fromisoformat(asof).date(), how))
    return text, stale_rows


# ─────────────────────────── semis：CSV + data.json ───────────────────────────
CSV_HEAD = ("ticker,close,high_52w,high_date,off_high_pct,d1_pct,w1_pct,m1_pct,ytd_pct,vs_ma50_pct,"
            "vs_ma200_pct,low_since_jun_date,above_low_since_jun_pct")
SEMIS_NAMES = {"^SOX": "費城半導體", "^GSPC": "S&P 500"}


def semis_csv_and_json(spec, px, asof, stale):
    """回傳 (csv 文字, data.json 文字)。stale 的列沿用 CSV 舊列。"""
    import pandas as pd
    old = {ln.split(",")[0]: ln for ln in (HERE / "semis-degross" / "drawdown_table.csv").read_text(encoding="utf-8").splitlines()[1:]}
    out_lines, rows_json = [CSV_HEAD], []
    lo_a, lo_b = "2026-06-22", "2026-10-15"
    for label, t, _ in spec["rows"]:
        if label in stale or t not in px.data:
            ln = old[t]
        else:
            s = px.data[t][spec["field"]].dropna()[: pd.Timestamp(asof)]
            w, lo = s.iloc[-252:], s[lo_a:lo_b]
            r2 = lambda k: repr(float(_round(calc(s, k, asof)[0], 2)))  # noqa: E731
            ln = ",".join([t, repr(float(_round(float(s.iloc[-1]), 2))), repr(float(_round(float(w.max()), 2))),
                           w.idxmax().strftime("%Y-%m-%d"), r2("from_52w_high"), r2("d1"), r2("w1"), r2("one_month"),
                           r2("ytd"), r2("ma50_pct"), r2("ma200_pct"), lo.idxmin().strftime("%Y-%m-%d"),
                           r2(f"from_low_between:{lo_a},{lo_b}")])
        out_lines.append(ln)
        f = ln.split(",")
        num = lambda x: None if x == "" else float(x)  # noqa: E731
        rows_json.append({"ticker": SEMIS_NAMES.get(f[0], f[0]), "off_high": num(f[4]), "high_date": f[3], "d1": num(f[5]),
                          "w1": num(f[6]), "m1": num(f[7]), "ytd": num(f[8]), "vs50": num(f[9]), "vs200": num(f[10]),
                          "above_low": num(f[12]), "low_date": f[11]})
    D = json.loads((HERE / "semis-degross" / "data.json").read_text(encoding="utf-8"))
    D["c2"]["rows"] = rows_json
    D["c2"]["asof"] = asof
    return "\n".join(out_lines) + "\n", json.dumps(D, ensure_ascii=False, separators=(",", ":"))


# ─────────────────────────── 主流程 ───────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(description="想法頁靜態股價表每日重算（說明見檔頭）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--add-markers", action="store_true")
    ap.add_argument("--tables")
    ap.add_argument("--asof")
    ap.add_argument("--include-manual", action="store_true")
    ap.add_argument("--strict", action="store_true", help="有 stale 或錯誤就 exit 1（預設永遠 exit 0）")
    args = ap.parse_args(argv)

    names = args.tables.split(",") if args.tables else list(SPEC)
    if args.apply and not args.tables and not args.include_manual:
        skipped = [n for n in names if not SPEC[n]["autorun"]]
        names = [n for n in names if SPEC[n]["autorun"]]
        if skipped:
            info(f"--apply 略過 autorun=False 的表：{skipped}（加 --include-manual 或 --tables 指名才處理）")
    px = Prices([r[1] for n in names for r in SPEC[n]["rows"] if r[1]])
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    problems, report = [], {}

    for name in names:
        spec = SPEC[name]
        path = IDEAS / spec["page"]
        try:
            text, st = add_markers(path.read_text(encoding="utf-8"), name, spec)
            text = add_asof_markers(text, name, spec)
            if args.add_markers:
                info(f"[{name}] {st}" + ("，已寫入" if _write_if_changed(path, text) else "，無變動"))
                continue
            if args.asof:
                asof = args.asof
            elif spec["ref"] in px.data:
                asof = px.data[spec["ref"]].index[-1].date().isoformat()
            else:
                raise LookupError(f"參考代號 {spec['ref']} 沒有資料")
            text, stale = refresh_table(text, name, spec, px, asof, report)
            if stale:
                problems.append((name, stale))
            extra = []
            if spec.get("csv"):
                c, j = semis_csv_and_json(spec, px, asof, set(stale))
                extra = [(HERE / "semis-degross" / "drawdown_table.csv", c), (HERE / "semis-degross" / "data.json", j)]
            info(f"[{name}] asof={asof}；來源 " + "、".join(sorted({px.source.get(r[1], '無') for r in spec['rows'] if r[1]})))
        except Exception as e:  # noqa: BLE001
            warn(f"[{name}] 整表略過：{type(e).__name__}: {e}")
            problems.append((name, [str(e)]))
            continue

        diffs = []
        for p, new in [(path, text)] + extra:
            old = p.read_text(encoding="utf-8")
            if p.suffix == ".json":  # 單行 JSON，只比 c2，逐列排開
                old_l = json.dumps(json.loads(old)["c2"], ensure_ascii=False, indent=0).splitlines()
                new_l = json.dumps(json.loads(new)["c2"], ensure_ascii=False, indent=0).splitlines()
            elif p.suffix == ".html":  # 表格常是單行，按 </tr> 斷行才看得見
                old_l, new_l = old.replace("</tr>", "</tr>\n").splitlines(), new.replace("</tr>", "</tr>\n").splitlines()
            else:
                old_l, new_l = old.splitlines(), new.splitlines()
            diffs += list(difflib.unified_diff(old_l, new_l, f"a/{p.name}", f"b/{p.name}", lineterm="", n=0))
        if args.dry_run:
            (PREVIEW_DIR / f"{name}.diff").write_text("\n".join(diffs) + "\n", encoding="utf-8")
            print(f"\n===== {name}（{len(diffs)} 行 diff）→ {PREVIEW_DIR / (name + '.diff')} =====")
            print("\n".join(diffs[:400]))
        else:
            n = sum(bool(_write_if_changed(p, new)) for p, new in [(path, text)] + extra)
            info(f"[{name}] " + (f"已寫入 {n} 檔" if n else "無變動"))
    if problems:
        warn("stale／略過：" + json.dumps(problems, ensure_ascii=False))
    return 1 if (problems and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
