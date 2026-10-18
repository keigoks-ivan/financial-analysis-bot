"""美債 3～5 年展望與債券腿選擇（/ideas/bond-outlook.html）的數據。

兩段：
1. `BACKTEST_DIR=<本機回測庫> python3.12 docs/ideas/data/bond-outlook/data.py --extract`（只在本機跑）：
   從本機回測庫（不公開）讀長歷史計算結果 results/bond_outlook/summary.json 與重建的債券總報酬指數
   data/bond_outlook/bond_tri.csv，抽出頁面要用的欄位，寫成同目錄的 history_extract.json。
   網站 CI 讀不到回測庫，所以抽出來的檔案進 repo，當靜態來源。
   2 年、10 年、20 年三條腿都由 bond_tri.csv 照同一套三條件重算，全期與 1994、2022 全年的累積
   超額報酬、最大跌幅和 summary.json 比對，不一致就停下。比對通過後，另算頁面引用的兩段債券
   熊市（高點到谷底）與 2019 年以來逐年的結果。
2. `python3.12 docs/ideas/data/bond-outlook/data.py`：讀 history_extract.json 與 gauges.json（資料型量表
   的四列），寫出 data.json。頁面的圖表讀 data.json。
3. `python3.12 docs/ideas/data/bond-outlook/data.py --gauges`（每個美股交易日由 daily-us-close.yml 跑）：
   抓價與利率 → 算四列（SPY 對 IEF 60 日相關係數、10 年減 3 個月利差、IEF 三條件、黃金三條件）→ 寫 gauges.json
   → 用 `<!-- gauges:start -->`／`<!-- gauges:end -->` 標記重寫頁面表格的列 → 再做第 2 步。
   - 利差口徑與長歷史分組相同：3 個月國庫券的貼現率先換成債券等值殖利率（BEY＝365·d／(360−d·91)，
     與回測庫 reconstruct.py 同公式），利差四捨五入到整數基點後比分界（>=200 有利、>=100 中性、其餘不利）。
   - IEF／黃金條件數直接呼叫實單追蹤程式的 compute_overlay（同一個數字），不另寫一份。
   - 任何一項抓不到：該列保留 gauges.json 上一次的值與資料日（標 stale），其他列照常更新；本模式不會讓程式失敗。
   - 重跑冪等：同資料重跑，gauges.json、頁面、data.json 都不變（generated 只在內容變動時更新）。

長歷史方法（2026-10-18 跑結果之前定死）：FRED 殖利率重建平價債，每月換新債、每天重新定價；
超額報酬＝債券日報酬減 3 個月國庫券日報酬。條件式＝債券總報酬指數的週線三條件（週收盤 > 40 週
均線、> 52 週均線、> 52 週前收盤，嚴格大於），每成立一條持有三分之一，週五收盤的計數管下一個
交易日到下週五。不含交易成本。這是描述，不是事前登記的檢驗。
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "history_extract.json"
OUT = HERE / "data.json"
GAUGES_JSON = HERE / "gauges.json"
REPO = HERE.parents[3]
PAGE = HERE.parents[1] / "bond-outlook.html"
STATE_JSON = REPO / "docs" / "long-track-w52-adaptive" / "state.json"

# 美股 13 次跌 15% 以上（創高重置法）的中文標籤，順序同 summary.json extra.A rows（略過 1962 不可計）
EVENT_LABELS = {
    "1966-02-09": "1966", "1968-11-29": "1968～70", "1973-01-11": "1973～74",
    "1980-11-28": "1980～82", "1987-08-25": "1987", "1990-07-16": "1990",
    "1998-07-17": "1998", "2000-03-24": "2000～02", "2007-10-09": "2007～09",
    "2018-09-20": "2018", "2020-02-19": "2020", "2022-01-03": "2022", "2025-02-19": "2025",
}

# 頁面引用的兩段 10 年債熊市，高點與谷底週取自 results.md「掉到 0／回到 3」表（10 年債那一列）
WINDOWS = [
    {"id": "bear_1994", "label": "1993-10～1994-11 高點到谷底", "base": "1993-10-15", "end": "1994-11-04"},
    {"id": "bear_2020_23", "label": "2020-07～2023-10 高點到谷底", "base": "2020-07-31", "end": "2023-10-20"},
]
YEARS = list(range(2019, 2027))

# ══════════════════════════════════════════════════════════════════════
# 頁面「資料型量表」四列（--gauges）。算法與分界見檔頭說明。
# ══════════════════════════════════════════════════════════════════════
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv"
MARK_ROWS = ("<!-- gauges:start -->", "<!-- gauges:end -->")
MARK_LEAD = ("<!-- gauges-lead:start -->", "<!-- gauges-lead:end -->")
MINUS = "−"
ZONE_LABEL = {"green": "有利", "yellow": "中性", "red": "不利"}
ZONE_BADGE = {"green": "b-sup", "yellow": "b-mix", "red": "b-ref"}
CORR_ZONES = {"green": "低於 −0.3", "yellow": "−0.3 到 +0.3", "red": "高於 +0.3"}
SPREAD_ZONES = {"green": "2 個百分點以上", "yellow": "1～2 個百分點", "red": "低於 1 個百分點"}
GAUGE_ORDER = ("spy_ief_corr60", "t10y3m", "ief_3cond", "gld_3cond")
LEG_ID = {"ief": "ief_3cond", "gld": "gld_3cond"}
LEG_LABEL = {"ief": "IEF 三條件", "gld": "黃金三條件"}


def warn(msg):
    print(f"[bond-gauges][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[bond-gauges] {msg}")


# ── 純計算（整數空間比分界）──
def _half_up(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def bey_pct(d_pct):
    """3 個月國庫券貼現率（%）→ 債券等值殖利率（%）。BEY＝365·d／(360−d·91)，d 為小數；同回測庫 reconstruct.py。"""
    d = Decimal(str(d_pct)) / 100
    return Decimal(365) * d / (Decimal(360) - d * 91) * 100


def spread_bps(y10_pct, dtb3_pct):
    """10 年殖利率減 3 個月國庫券債券等值殖利率，四捨五入到整數基點。"""
    return _half_up((Decimal(str(y10_pct)) - bey_pct(dtb3_pct)) * 100)


def spread_zone(bps):
    """左閉右開：>= 200 有利、>= 100 中性（含 100）、其餘不利。bps 必須是整數。"""
    if bps >= 200:
        return "green"
    if bps >= 100:
        return "yellow"
    return "red"


def corr_c100(corr):
    """相關係數四捨五入到小數兩位，轉成整數百分位（+0.30 → 30）。"""
    return _half_up(Decimal(repr(float(corr))) * 100)


def corr_zone(c100):
    """< −30 有利、> +30 不利、其餘（含 ±30）中性。"""
    if c100 < -30:
        return "green"
    if c100 > 30:
        return "red"
    return "yellow"


def _hundredths(v, signed):
    """整數百分位 → 文字：55 → '0.55'；signed 時正數加 '+'，負號用 U+2212。"""
    a = abs(v)
    s = f"{a // 100}.{a % 100:02d}"
    if v < 0:
        return MINUS + s
    return ("+" + s) if (signed and v > 0) else s


def _md(d):
    return f"{int(d[5:7])}/{int(d[8:10])}"


def _zh_md(d):
    return f"{int(d[5:7])} 月 {int(d[8:10])} 日"


# ── 資料抓取 ──
def _http_get(url, params, tries=3, timeout=30):
    import requests

    last = None
    for i in range(tries):
        try:
            # FRED 對自訂 User-Agent 會擋到逾時，必須用 requests 預設 UA（同 update_fear_greed.py 的註記）
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.text
        except Exception as e:  # noqa: BLE001
            last = e
            if i < tries - 1:
                time.sleep(2 * (i + 1))
    raise last


def parse_fred_csv(text):
    """FRED fredgraph.csv → {日期: 值}；空值與 '.' 略過。"""
    lines = text.strip().splitlines()
    if not lines or not lines[0].lower().startswith(("observation_date", "date")):
        raise ValueError("FRED 回傳的不是 CSV")
    out = {}
    for ln in lines[1:]:
        d, _, v = ln.partition(",")
        v = v.strip()
        if v in ("", "."):
            continue
        out[d.strip()] = float(v)
    return out


def latest_common(a, b):
    """兩個 {日期: 值} 都有值的最新一天。"""
    days = sorted(set(a) & set(b))
    if not days:
        raise ValueError("DGS10 與 DTB3 沒有共同資料日")
    d = days[-1]
    return d, a[d], b[d]


def fetch_adj_close(sym, start, tries=3):
    """yfinance 還原收盤（auto_adjust=True），index 為無時區日期。"""
    import pandas as pd
    import yfinance as yf

    last = None
    for i in range(tries):
        try:
            df = yf.download(sym, start=start, progress=False, auto_adjust=True)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            c = df["Close"]
            if isinstance(c, pd.DataFrame):
                c = c.iloc[:, 0]
            c = c.dropna()
            if getattr(c.index, "tz", None) is not None:
                c.index = c.index.tz_localize(None)
            if len(c) < 120:
                raise ValueError(f"{sym} 價格筆數不足（{len(c)}）")
            return c
        except Exception as e:  # noqa: BLE001
            last = e
            if i < tries - 1:
                time.sleep(3 * (i + 1))
    raise last


# ── 四列 ──
def corr_series(spy, ief, window=60):
    """兩條還原收盤取共同交易日，算日報酬，滾動 window 個日報酬（＝window+1 個收盤）的 Pearson 相關。"""
    import pandas as pd

    df = pd.concat([spy.rename("spy"), ief.rename("ief")], axis=1, join="inner").dropna()
    ret = df.pct_change().dropna()
    return ret["spy"].rolling(window).corr(ret["ief"]).dropna()


def corr_row(rc):
    """rc：corr_series 的結果。備註放今年以來的最高與最低。"""
    day = rc.index[-1]
    c100 = corr_c100(rc.iloc[-1])
    zone = corr_zone(c100)
    ytd = rc[rc.index.year == day.year]
    hi, lo = ytd.idxmax(), ytd.idxmin()
    hi_t = _hundredths(corr_c100(ytd.loc[hi]), True)
    lo_t = _hundredths(corr_c100(ytd.loc[lo]), True)
    return {
        "id": "spy_ief_corr60", "label": "60 日 SPY 對 IEF 日報酬相關係數",
        "value": c100 / 100, "value_text": _hundredths(c100, True), "unit": "",
        "asof": day.strftime("%Y-%m-%d"), "zone": zone, "zone_label": ZONE_LABEL[zone], "zones": CORR_ZONES,
        "note": (f"還原日價自算；{day.year} 年最高 {hi_t}（{_zh_md(hi.strftime('%Y-%m-%d'))}），"
                 f"最低 {lo_t}（{_zh_md(lo.strftime('%Y-%m-%d'))}）"),
    }


def spread_row(date, y10, dtb3):
    bps = spread_bps(y10, dtb3)
    zone = spread_zone(bps)
    bey = round(bey_pct(dtb3), 2)
    return {
        "id": "t10y3m", "label": "10 年減 3 個月公債利差",
        "value": bps / 100, "value_text": _hundredths(bps, False) + " 個百分點", "unit": "個百分點", "bps": bps,
        "asof": date, "zone": zone, "zone_label": ZONE_LABEL[zone], "zones": SPREAD_ZONES,
        "note": f"FRED DGS10 {y10:.2f}% 減 DTB3 貼現率 {dtb3:.2f}%（換成債券等值殖利率 {bey:.2f}%）",
    }


def fetch_corr_row():
    today = datetime.now(timezone.utc)
    start = f"{today.year - 1}-01-01"
    rc = corr_series(fetch_adj_close("SPY", start), fetch_adj_close("IEF", start))
    if len(rc) < 20:
        raise ValueError("相關係數樣本不足")
    return corr_row(rc)


def fetch_spread_row():
    start = f"{datetime.now(timezone.utc).year - 1}-01-01"
    y10 = parse_fred_csv(_http_get(FRED_CSV, {"id": "DGS10", "cosd": start}))
    b3 = parse_fred_csv(_http_get(FRED_CSV, {"id": "DTB3", "cosd": start}))
    date, a, b = latest_common(y10, b3)
    return spread_row(date, a, b)


def streak_of(ns, dates):
    """ns：依時間排序的「已收盤週」條件數；回傳目前分數、起始週、連續週數、前一個不同分數。"""
    i = len(ns) - 1
    while i > 0 and ns[i - 1] == ns[-1]:
        i -= 1
    return {"n": ns[-1], "start": dates[i], "weeks": len(ns) - i, "prev_n": ns[i - 1] if i > 0 else None}


def streak_text(st):
    md = _md(st["start"])
    if st["prev_n"] is None:
        return f"{md} 起 {st['n']}/3"
    if st["weeks"] >= 2:
        return f"{md} 起連續 {st['weeks']} 週"
    return f"{md} 由 {st['prev_n']}/3 {'升' if st['n'] > st['prev_n'] else '降'}為 {st['n']}/3"


def leg_row(k, ov, st):
    """ov：實單程式 compute_overlay 的單腿結果（只取條件數與週線日，不帶價格以外的欄位）；st：streak_of。"""
    n = ov["n"]
    text = streak_text(st)
    return {
        "id": LEG_ID[k], "kind": "leg", "label": LEG_LABEL[k],
        "value": n, "value_text": f"{n}/3", "unit": "",
        "asof": ov["week_date"], "zone": "on" if n else "off", "zone_label": f"持有 {n}/3" if n else "不持有",
        "conditions": {"ma40": ov["c_ma40"], "ma52": ov["c_ma52"], "px52": ov["c_px52"]},
        "streak_start": st["start"], "streak_weeks": st["weeks"], "prev_n": st["prev_n"],
        "streak_text": text,
        "note": text + (f" {n}/3" if st["weeks"] >= 2 and st["prev_n"] is not None else ""),
    }


def fetch_legs():
    """IEF、黃金條件數：直接呼叫實單程式 scripts/update_long_track_w52_adaptive.py 的 compute_overlay
    （兩個模組 import 無副作用）。每條腿各呼叫一次（暫時把 OVERLAY_LEGS 縮成單腿），一條抓不到不影響另一條。
    回傳 {'ief': 列 或 Exception, 'gld': ...}。"""
    import pandas as pd

    sys.path.insert(0, str(REPO / "scripts"))
    import update_long_track_w52_adaptive as w52
    import update_long_track_w52_adaptive_c1 as c1

    cache = {}
    orig_fetch = c1.fetch_adj

    def cached(sym):
        if sym not in cache:
            cache[sym] = orig_fetch(sym)
        return cache[sym]

    asof = pd.Timestamp(datetime.now(timezone.utc).date())
    legs = tuple(w52.OVERLAY_LEGS)
    out = {}
    c1.fetch_adj = cached
    try:
        for k in legs:
            try:
                w52.OVERLAY_LEGS = (k,)
                ov = w52.compute_overlay(asof)[k]
            except Exception as e:  # noqa: BLE001
                out[k] = e
                continue
            finally:
                w52.OVERLAY_LEGS = legs
            try:
                adj = cache[w52.OVERLAY_SYM[k]]
                wk = c1.e3_weekly(adj)
                done = wk[wk.index <= min(asof, adj.index[-1])]
                ns = [int(x) for x in done["n"]]
                dates = [d.strftime("%Y-%m-%d") for d in done.index]
                if ns[-1] != ov["n"] or dates[-1] != ov["week_date"]:
                    raise AssertionError(f"連續週數與 compute_overlay 不一致：{ns[-1]}@{dates[-1]} 對 {ov['n']}@{ov['week_date']}")
                out[k] = leg_row(k, ov, streak_of(ns, dates))
            except Exception as e:  # noqa: BLE001
                out[k] = e
    finally:
        c1.fetch_adj = orig_fetch
        w52.OVERLAY_LEGS = legs
    return out


def check_against_state(rows):
    """和 docs/long-track-w52-adaptive/state.json 的 overlay 區塊交叉核對（只印出，不影響輸出）。"""
    try:
        ov = json.loads(STATE_JSON.read_text(encoding="utf-8")).get("overlay") or {}
    except Exception as e:  # noqa: BLE001
        info(f"state.json 讀不到，略過核對：{type(e).__name__}")
        return
    for k, gid in LEG_ID.items():
        row = next((g for g in rows if g["id"] == gid), None)
        s = ov.get(k)
        if not row or not s:
            info(f"state.json 沒有 {k} 的 overlay，略過核對")
        elif s.get("week_date") != row["asof"]:
            info(f"{k}：state.json 週線日 {s.get('week_date')}、本次 {row['asof']}，週線日不同，未核對")
        elif s.get("n") != row["value"]:
            warn(f"{k}：state.json 條件數 {s.get('n')} 與本次 {row['value']} 不一致")
        else:
            info(f"{k}：與 state.json 一致（{row['value']}/3，週線日 {row['asof']}）")


# ── 頁面 ──
def render_rows(rows):
    out = []
    for g in rows:
        head = f"<tr><td>{escape(g['label'])}</td><td>{escape(g['value_text'])}</td><td>{escape(g['asof'])}</td>"
        if g.get("kind") == "leg":
            badge = "b-sup" if g["zone"] == "on" else "b-un"
            out.append(f'{head}<td colspan="3">{escape(g["note"])}</td>'
                       f'<td><span class="badge {badge}">{escape(g["zone_label"])}</span></td></tr>')
        else:
            z = g["zones"]
            out.append(f'{head}<td>{escape(z["green"])}</td><td>{escape(z["yellow"])}</td><td>{escape(z["red"])}</td>'
                       f'<td><span class="badge {ZONE_BADGE[g["zone"]]}">{ZONE_LABEL[g["zone"]]}</span></td></tr>')
    return "\n".join(out)


def render_lead(rows):
    daily = [g for g in rows if g["id"] in ("spy_ief_corr60", "t10y3m")]
    green = [g for g in daily if g["zone"] == "green"]
    if not green:
        tail = "目前都不在有利區"
    elif len(green) == len(daily):
        tail = "目前都在有利區"
    else:
        tail = "目前只有" + ("相關係數" if green[0]["id"] == "spy_ief_corr60" else "利差") + "在有利區"
    return f"<b>決定債券腿能不能發揮作用的兩個數字，{tail}。</b>"


def _replace_between(html, marks, body):
    a, b = marks
    if html.count(a) != 1 or html.count(b) != 1 or html.index(a) > html.index(b):
        raise ValueError(f"頁面缺少唯一的標記 {a}／{b}")
    pat = re.compile(re.escape(a) + r".*?" + re.escape(b), re.S)
    return pat.sub(lambda m: a + body + b, html, count=1)


def apply_gauges(html, rows):
    """把四列與標題句寫進頁面標記之間；idea-meta 的資料日一併更新。重複套用結果不變。"""
    html = _replace_between(html, MARK_ROWS, "\n" + render_rows(rows) + "\n")
    html = _replace_between(html, MARK_LEAD, render_lead(rows))
    by = {g["id"]: g for g in rows}
    html = re.sub(r'("data_asof": ")[0-9-]+(")', lambda m: m.group(1) + max(g["asof"] for g in rows) + m.group(2), html)
    html = re.sub(r'("data_last_trading_day": ")[0-9-]+(")',
                  lambda m: m.group(1) + by["spy_ief_corr60"]["asof"] + m.group(2), html)
    return html


def _write_if_changed(path, text):
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def refresh_gauges(fetchers=None, now=None):
    """抓資料 → 算四列 → 寫 gauges.json → 重寫頁面。任何一列失敗就沿用 gauges.json 上一次的那列（標 stale）。"""
    f = {"corr": fetch_corr_row, "spread": fetch_spread_row, "legs": fetch_legs}
    f.update(fetchers or {})
    prev = json.loads(GAUGES_JSON.read_text(encoding="utf-8")) if GAUGES_JSON.exists() else {}
    prev_rows = {g["id"]: g for g in prev.get("gauges", [])}

    fresh = {}
    for gid, key in (("spy_ief_corr60", "corr"), ("t10y3m", "spread")):
        try:
            fresh[gid] = f[key]()
        except Exception as e:  # noqa: BLE001
            warn(f"{gid} 抓不到：{type(e).__name__}: {e}")
    try:
        legs = f["legs"]()
    except Exception as e:  # noqa: BLE001
        legs = {k: e for k in LEG_ID}
    for k, gid in LEG_ID.items():
        v = legs.get(k)
        if isinstance(v, dict):
            fresh[gid] = v
        else:
            warn(f"{gid} 抓不到：{type(v).__name__ if v is not None else '無結果'}: {v}")

    rows = []
    for gid in GAUGE_ORDER:
        if gid in fresh:
            rows.append(fresh[gid])
        elif gid in prev_rows:
            rows.append({**prev_rows[gid], "stale": True})
        else:
            warn(f"{gid} 抓不到、也沒有上次的值，這一列缺")
    if len(rows) == len(GAUGE_ORDER):
        check_against_state(rows)

    generated = prev.get("generated") if prev.get("gauges") == rows else None
    generated = generated or (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    doc = {"generated": generated, "gauges": rows}
    changed = _write_if_changed(GAUGES_JSON, json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    info(f"gauges.json {'已更新' if changed else '無變動'}；" + "；".join(
        f"{g['id']}={g['value_text']}（{g['asof']}，{g.get('zone_label', '')}{'，沿用' if g.get('stale') else ''}）" for g in rows))

    if len(rows) == len(GAUGE_ORDER):
        html = PAGE.read_text(encoding="utf-8")
        if _write_if_changed(PAGE, apply_gauges(html, rows)):
            info("頁面量表已重寫")
    else:
        warn("四列不齊，頁面不動")
    return doc


def extract():
    import numpy as np
    import pandas as pd

    root = os.environ.get("BACKTEST_DIR")
    if not root:
        raise SystemExit("請設定 BACKTEST_DIR 指向本機回測庫")
    root = Path(root).expanduser()
    summary = json.loads((root / "results/bond_outlook/summary.json").read_text())
    tb = pd.read_csv(root / "data/bond_outlook/bond_tri.csv", index_col=0, parse_dates=True)

    def leg(k):
        """回傳 (條件式日超額, 一直抱著日超額, 持有比例)，與回測庫的訊號規則相同。"""
        tri = tb[f"tri_{k}"]
        wk = tri.resample("W-FRI").last()
        if wk.isna().any():
            raise SystemExit(f"{k} 週線出現空週")
        x = wk.values.astype(float)
        ma40 = wk.rolling(40).mean().values
        ma52 = wk.rolling(52).mean().values
        cnt = np.full(len(x), -1, dtype=int)
        for i in range(52, len(x)):
            cnt[i] = int(x[i] > ma40[i]) + int(x[i] > ma52[i]) + int(x[i] > x[i - 52])
        prev = np.concatenate([[-1], cnt[:-1]])
        pos = wk.index.searchsorted(tb.index, side="left")
        held = np.where(prev[pos] >= 0, prev[pos], 0)
        bond = tb[f"ret_{k}"].values
        cash = tb["ret_cash"].values
        return (pd.Series(held * (bond - cash) / 3.0, index=tb.index),
                pd.Series(bond - cash, index=tb.index),
                pd.Series(held / 3.0, index=tb.index))

    legs = {k: leg(k) for k in ("2y", "10y", "20y")}

    def curve(ex, base, end):
        """基準日收盤＝1，之後逐日複利到 end（含）。"""
        s = ex[(ex.index > pd.Timestamp(base)) & (ex.index <= pd.Timestamp(end))]
        c = pd.Series(np.concatenate([[1.0], np.cumprod(1.0 + np.nan_to_num(s.values))]),
                      index=[pd.Timestamp(base)] + list(s.index))
        return c

    def stats(k, base, end):
        cond, hold, held = legs[k]
        out = {}
        for key, ex in (("cond", cond), ("hold", hold)):
            c = curve(ex, base, end)
            out[key] = {"cum": float(c.iloc[-1] - 1.0), "mdd": float((c / c.cummax() - 1.0).min())}
        h = held[(held.index > pd.Timestamp(base)) & (held.index <= pd.Timestamp(end))]
        out["held"] = float(h.mean())
        return out

    # ── 與 summary.json 比對：全期、1994 全年、2022 全年，三條腿 ──
    full = [r for r in summary["decades"] if r["label"].startswith("全期")][0]["bonds"]
    bears = {b["label"]: b["bonds"] for b in summary["bear"]}
    checks = [("全期", full), ("1994 全年", bears["1994 全年"]), ("2022 全年", bears["2022 全年"])]
    for name, bonds in checks:
        for k in ("2y", "10y", "20y"):
            want = bonds[k]
            got = stats(k, want["base_date"], want["end_date"])
            for key in ("cond", "hold"):
                dc = abs(got[key]["cum"] - want[key]["excess_cum"])
                dm = abs(got[key]["mdd"] - want[key]["excess_mdd"])
                if dc > 1e-6 or dm > 1e-6:
                    raise SystemExit(f"{name} {k} {key} 與 summary.json 不一致："
                                     f"累積 {got[key]['cum']} 對 {want[key]['excess_cum']}，"
                                     f"最大跌幅 {got[key]['mdd']} 對 {want[key]['excess_mdd']}")

    # ── 全期月底曲線（10 年債） ──
    f10 = full["10y"]
    out_curves = {}
    for key, ex in (("cond", legs["10y"][0]), ("hold", legs["10y"][1])):
        m = curve(ex, f10["base_date"], f10["end_date"]).resample("ME").last()
        out_curves[key] = [round((v - 1.0) * 100, 2) for v in m.values]
        out_curves["dates"] = [d.strftime("%Y-%m") for d in m.index]

    def pct(v, nd=1):
        return round(v * 100, nd)

    windows = []
    for w in WINDOWS:
        row = {"id": w["id"], "label": w["label"], "base": w["base"], "end": w["end"]}
        for k in ("2y", "10y", "20y"):
            s = stats(k, w["base"], w["end"])
            row[k] = {"cond": pct(s["cond"]["cum"]), "hold": pct(s["hold"]["cum"]), "held": pct(s["held"], 0)}
        windows.append(row)

    yearly = []
    for y in YEARS:
        base = tb.index[tb.index < pd.Timestamp(f"{y}-01-01")][-1].strftime("%Y-%m-%d")
        end = tb.index[tb.index <= pd.Timestamp(f"{y}-12-31")][-1].strftime("%Y-%m-%d")
        row = {"year": y, "end": end}
        for k in ("2y", "10y"):
            s = stats(k, base, end)
            row[k] = {"cond": pct(s["cond"]["cum"]), "hold": pct(s["hold"]["cum"]), "held": pct(s["held"], 0)}
        yearly.append(row)

    events = []
    for row in summary["extra"]["A"]["rows"]:
        if not row.get("usable"):
            continue
        l10 = row["legs"]["10y"]
        events.append({
            "label": EVENT_LABELS[row["peak_date"]],
            "peak_date": row["peak_date"], "trough_date": row["trough_date"],
            "spx_drawdown": pct(row["drawdown"]),
            "score_week": l10["score_week"],
            "inforce_10y": l10["inforce"],
            "cond_10y": pct(l10["cond_excess"]),
            "hold_10y": pct(l10["hold_excess"]),
            "cond_20y": pct(row["legs"]["20y"]["cond_excess"]),
            "cond_2y": pct(row["legs"]["2y"]["cond_excess"]),
        })
    if len(events) != 13:
        raise SystemExit(f"事件數 {len(events)} 不是 13")
    avg = summary["extra"]["A"]["average"]

    def avg_of(k):
        a = avg[k]
        return {"cond_mean": pct(a["cond_mean"]), "cond_median": pct(a["cond_median"]),
                "hold_mean": pct(a["hold_mean"]), "hold_median": pct(a["hold_median"]),
                "cond_positive": a["cond_positive"], "n": a["n"]}

    def full_of(k):
        f = full[k]
        return {"base_date": f["base_date"], "end_date": f["end_date"],
                "cond": {"excess_ann": pct(f["cond"]["excess_ann"], 2), "excess_cum": pct(f["cond"]["excess_cum"]),
                         "excess_mdd": pct(f["cond"]["excess_mdd"])},
                "hold": {"excess_ann": pct(f["hold"]["excess_ann"], 2), "excess_cum": pct(f["hold"]["excess_cum"]),
                         "excess_mdd": pct(f["hold"]["excess_mdd"])}}

    ex = {
        "source": "本機回測庫 results/bond_outlook/summary.json＋data/bond_outlook/bond_tri.csv",
        "generated": summary["meta"]["generated"],
        "bond_data_last": summary["meta"]["last"],
        "spx_last": summary["meta"]["spx_last"],
        "events": events,
        "events_average": avg_of("10y"),
        "events_average_2y": avg_of("2y"),
        "full_period": full_of("10y"),
        "full_period_2y": full_of("2y"),
        "windows": windows,
        "yearly": yearly,
        "curve_monthly": out_curves,
    }
    EXTRACT.write_text(json.dumps(ex, ensure_ascii=False, indent=1) + "\n")
    print("寫出", EXTRACT)


def legs_status(rows):
    by = {g["id"]: g for g in rows}
    ief, gld = by["ief_3cond"], by["gld_3cond"]
    return {"asof": max(ief["asof"], gld["asof"]),
            "ief": f"{ief['value_text']}（{ief['streak_text']}）",
            "gold": f"{gld['value_text']}（{gld['streak_text']}）",
            "live_page": "/long-track-w52-adaptive/"}


def build():
    ex = json.loads(EXTRACT.read_text())
    g = json.loads(GAUGES_JSON.read_text(encoding="utf-8"))
    rows = g["gauges"]
    data = {
        "page": "/ideas/bond-outlook.html",
        "history": ex,
        "gauges": [r for r in rows if r.get("kind") != "leg"],
        "gauges_generated": g["generated"],
        "legs_status": legs_status(rows),
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    print("寫出", OUT)


if __name__ == "__main__":
    if "--extract" in sys.argv:
        extract()
    if "--gauges" in sys.argv:
        # CI 模式：任何錯誤都只印警告，不讓 workflow 失敗
        try:
            refresh_gauges()
            build()
        except BaseException as e:  # noqa: BLE001
            warn(f"量表更新失敗，檔案維持原樣：{type(e).__name__}: {e}")
        sys.exit(0)
    build()
