#!/usr/bin/env python3
"""跨資產擁擠交易監測（/crowding/）的儀表資料：docs/crowding/data/dash.json。

只用標準函式庫。輸入：
  data/cot_history.json                      CFTC 15 市場投機淨部位（build_crowding.py 每週維護）
  data/crowding_monitor/aaii_weekly.csv       AAII 散戶調查（scripts/crowding/fetch_sentiment.py 每週抓）
  data/crowding_monitor/naaim_weekly.csv      NAAIM 顧問曝險（同上）
  docs/crowding/data/bofa_fms_monthly.csv     BofA 基金經理人調查最擁擠交易（人工每月補）
  data/etf_dash/flows/{ETF}.jsonl             發行商流通單位數×淨值（etf-dash 每日維護，只留 200 天）
  data/crowding_monitor/leveraged_etf_flows_weekly.csv  槓桿 ETF（TQQQ/SQQQ/SOXL/SOXS）週淨申購，2016-11 起
                                              （TradingView 匯出一次；之後由下面的每日檔接續）
  data/crowding_monitor/leveraged_etf_daily.csv  同四檔的發行商每日流通單位數與淨值（fetch_leveraged.py）
  docs/crowding/data/readings.json            手寫短判讀（有日期）
輸出：
  docs/crowding/data/dash.json
  data/crowding_monitor/etf_flows_daily.csv   ETF 每日資金流的累積檔（etf-dash 只留 200 天，這裡不丟；flows 資料夾全部基金）
  data/crowding_monitor/etf_flows_weekly.csv  每日檔算出的新週會寫回這裡（source=issuer；本檔是週檔唯一寫入者，
                                              etf-dash 只讀不寫）
  data/crowding_monitor/leveraged_etf_flows_weekly.csv  每日檔算出的新週會寫回這裡（source=issuer）
用法：python3 scripts/crowding/build_dash.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
from datetime import date, datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = lambda *a: os.path.join(ROOT, *a)  # noqa: E731

COT_HISTORY = P("data", "cot_history.json")
AAII_CSV = P("data", "crowding_monitor", "aaii_weekly.csv")
NAAIM_CSV = P("data", "crowding_monitor", "naaim_weekly.csv")
FMS_CSV = P("docs", "crowding", "data", "bofa_fms_monthly.csv")
FLOWS_DIR = P("data", "etf_dash", "flows")
FLOWS_ACC = P("data", "crowding_monitor", "etf_flows_daily.csv")
FLOWS_WEEKLY = P("data", "crowding_monitor", "etf_flows_weekly.csv")
LEV_WEEKLY = P("data", "crowding_monitor", "leveraged_etf_flows_weekly.csv")
LEV_DAILY = P("data", "crowding_monitor", "leveraged_etf_daily.csv")
LEV_ETFS = {"SOXL": ("半導體 3 倍多", "semi", "bull"), "SOXS": ("半導體 3 倍空", "semi", "bear"),
            "TQQQ": ("Nasdaq-100 3 倍多", "ndx", "bull"), "SQQQ": ("Nasdaq-100 3 倍空", "ndx", "bear")}
LEV_CHART_FROM = "2021-01-04"
READINGS = P("docs", "crowding", "data", "readings.json")
OUT = P("docs", "crowding", "data", "dash.json")

FLOW_ETFS = {
    "SPY": "S&P 500", "XLK": "科技", "XLC": "通訊", "XLY": "非必需消費", "XLP": "必需消費",
    "XLE": "能源", "XLF": "金融", "XLV": "醫療", "XLI": "工業", "XLB": "原物料",
    "XLRE": "不動產", "XLU": "公用事業", "SMH": "半導體",
}  # QQQ 的流通單位數有來源切換造成的跳動、SOXX 只有 2026-10 起，先不用
# SMH 2026-06-17 +1,090 萬單位、06-22 −1,090 萬單位是一組互相抵銷的資料跳動：略過這兩天（06-18～06-21 單位數不變，略過後 06-23 對 06-16 的差就是真實變化）
# 併成新週只用發行商逐日歷史（SPDR、VanEck）。yfinance 快照（另外 37 檔）的流通單位數常停在同一個數字好幾天，
# 2026-10-19 那週拿來跟 TradingView 對：SPDR 各檔差 1～3%，yfinance 各檔差到數倍或方向相反（0050 50,100 對 28,020
# 百萬台幣、QQQ 0 對 2,694、EWZ 0 對 21）。這些基金的週序列先停在 TradingView 匯出的最後一週，每日檔照樣累積。
WEEKLY_MERGE_SOURCES = {"ssga_navhist", "vaneck_navhist_derived"}
SKIP_FLOW_DAYS = {("SMH", "2026-06-17"), ("SMH", "2026-06-18"), ("SMH", "2026-06-19"), ("SMH", "2026-06-20"), ("SMH", "2026-06-21"), ("SMH", "2026-06-22")}
COT_ORDER = ["13874A", "209742", "239742", "1170E1", "020601", "043602", "044601", "042601",
             "098662", "099741", "097741", "088691", "084691", "085692", "067651"]
COT_ZH = {
    "S&P 500 E-mini": "S&P 500 期貨", "Nasdaq-100 E-mini": "Nasdaq-100 期貨", "Russell 2000 E-mini": "Russell 2000 期貨",
    "VIX futures": "VIX 期貨", "US Treasury Bonds (30Y)": "美債 30 年", "US Treasury 10Y": "美債 10 年",
    "US Treasury 5Y": "美債 5 年", "US Treasury 2Y": "美債 2 年", "US Dollar Index (DX)": "美元指數",
    "EUR (Euro FX)": "歐元", "JPY (Japanese Yen)": "日圓", "Gold": "黃金", "Silver": "白銀", "Copper": "銅", "WTI Crude": "WTI 原油",
}


def warn(m):
    print(f"[warn] {m}", file=sys.stderr)


def fnum(x):
    try:
        if x is None or str(x).strip() == "":
            return None
        return float(str(x).replace(",", ""))
    except ValueError:
        return None


def pctile(values, x):
    """x 在 values 裡的百分位（含等於，0～100）。"""
    vs = [v for v in values if v is not None]
    if not vs or x is None:
        return None
    return round(100.0 * sum(1 for v in vs if v <= x) / len(vs), 1)


def read_csv(path):
    if not os.path.exists(path):
        warn(f"缺 {os.path.relpath(path, ROOT)}")
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# ── BofA FMS ────────────────────────────────────────────────────────────────
def fms_category(name):
    n = (name or "").lower()
    if not n:
        return "", ""
    if any(k in n for k in ("semiconductor", "semis", "chip")):
        return "semis", "半導體"
    if any(k in n for k in ("tech", "magnificent", "mag 7", "mag7", "faang", "fang", "nasdaq", "growth", "ai ")):
        return "tech", "美國科技"
    if "gold" in n:
        return "gold", "黃金"
    if "dollar" in n or "usd" in n:
        return "usd", "美元"
    if any(k in n for k in ("treasur", "bond", "credit", "ig ", "duration")):
        return "bonds", "債券"
    if any(k in n for k in ("bitcoin", "crypto")):
        return "crypto", "加密"
    if any(k in n for k in ("cash",)):
        return "cash", "現金"
    if any(k in n for k in ("em ", "emerging", "china", "europe", "japan", "eu ")):
        return "region", "區域"
    if any(k in n for k in ("oil", "commodit", "copper", "energy")):
        return "commod", "商品"
    return "other", "其他"


def build_fms():
    rows = read_csv(FMS_CSV)
    out = []
    for r in rows:
        m = (r.get("survey_month") or "").strip()
        if len(m) != 7:
            continue
        cat, cat_zh = fms_category(r.get("top_trade"))
        out.append({
            "m": m, "pub": (r.get("publish_date") or "").strip() or None,
            "top": (r.get("top_trade") or "").strip() or None, "top_pct": fnum(r.get("top_pct")),
            "second": (r.get("second_trade") or "").strip() or None, "second_pct": fnum(r.get("second_pct")),
            "third": (r.get("third_trade") or "").strip() or None, "third_pct": fnum(r.get("third_pct")),
            "cash": fnum(r.get("cash_pct")), "tier": (r.get("tier") or "").strip() or None,
            "cat": cat, "cat_zh": cat_zh, "note": (r.get("note") or "").strip() or None,
        })
    out.sort(key=lambda x: x["m"])
    tops = [x["top_pct"] for x in out if x["top_pct"] is not None]
    cash = [x["cash"] for x in out if x["cash"] is not None]
    latest = next((x for x in reversed(out) if x["top_pct"] is not None), None)
    latest_cash = next((x for x in reversed(out) if x["cash"] is not None), None)
    stats = {}
    if tops:
        s = sorted(tops)
        stats = {"n": len(s), "median": s[len(s) // 2], "p90": s[int(0.9 * (len(s) - 1))],
                 "max": s[-1], "max_m": next(x["m"] for x in out if x["top_pct"] == s[-1]),
                 "n_ge60": sum(1 for v in s if v >= 60)}
    cash_stats = {}
    if cash:
        s = sorted(cash)
        cash_stats = {"n": len(s), "median": s[len(s) // 2], "min": s[0], "max": s[-1]}
    return {"monthly": out, "latest": latest, "latest_cash": latest_cash, "stats": stats, "cash_stats": cash_stats,
            "coverage": {"first": out[0]["m"] if out else None, "last": out[-1]["m"] if out else None,
                         "n_top_pct": len(tops), "n_cash": len(cash)}}


# ── CFTC COT ────────────────────────────────────────────────────────────────
def build_cot():
    if not os.path.exists(COT_HISTORY):
        warn("缺 data/cot_history.json")
        return {"markets": [], "asof": None}
    with open(COT_HISTORY, encoding="utf-8") as f:
        d = json.load(f)
    mk = d.get("markets", {})
    out = []
    asof = None
    for code in COT_ORDER + [c for c in mk if c not in COT_ORDER]:
        v = mk.get(code)
        if not v:
            continue
        ser = [[s[0], s[1]] for s in v["series"] if s[1] is not None]
        if not ser:
            continue
        vals = [s[1] for s in ser]
        last_d, last = ser[-1]
        asof = max(asof or last_d, last_d)
        w5 = vals[-260:]
        w3 = vals[-156:]
        p5 = pctile(w5, last)
        p3 = pctile(w3, last)
        d4 = round(last - vals[-5], 2) if len(vals) >= 5 else None
        d13 = round(last - vals[-14], 2) if len(vals) >= 14 else None
        band = "極端偏多" if p5 is not None and p5 >= 90 else "極端偏空" if p5 is not None and p5 <= 10 else \
            "偏多" if p5 is not None and p5 >= 75 else "偏空" if p5 is not None and p5 <= 25 else "中性"
        out.append({"code": code, "label": v["label"], "zh": COT_ZH.get(v["label"], v["label"]),
                    "series": ser, "latest": last, "asof": last_d, "pct5y": p5, "pct3y": p3,
                    "d4w": d4, "d13w": d13, "band": band,
                    "min5y": min(w5), "max5y": max(w5)})
    return {"markets": out, "asof": asof, "since": min((m["series"][0][0] for m in out), default=None),
            "method": d.get("meta", {}).get("methodology")}


# ── AAII / NAAIM ────────────────────────────────────────────────────────────
def build_aaii():
    rows = read_csv(AAII_CSV)
    ser = []
    for r in rows:
        d, b, n, be = r.get("date"), fnum(r.get("bullish")), fnum(r.get("neutral")), fnum(r.get("bearish"))
        if not d or b is None or be is None:
            continue
        sp = fnum(r.get("spread"))
        if sp is None:
            sp = round(b - be, 2)
        ser.append([d[:10], b, n, be, round(sp, 2)])
    ser.sort(key=lambda x: x[0])
    if not ser:
        return {"series": [], "latest": None}
    sp = [x[4] for x in ser]
    bull = [x[1] for x in ser]
    last = ser[-1]
    mean = sum(sp) / len(sp)
    sd = (sum((v - mean) ** 2 for v in sp) / len(sp)) ** 0.5
    # 連續幾週多空差為負（或為正）
    streak = 0
    sign = 1 if last[4] >= 0 else -1
    for x in reversed(ser):
        if (1 if x[4] >= 0 else -1) == sign:
            streak += 1
        else:
            break
    return {"series": ser, "latest": {"date": last[0], "bull": last[1], "neutral": last[2], "bear": last[3], "spread": last[4]},
            "pct_all": pctile(sp, last[4]), "pct_5y": pctile(sp[-260:], last[4]),
            "bull_pct_all": pctile(bull, last[1]), "bear_pct_all": pctile([x[3] for x in ser], last[3]),
            "mean_spread": round(mean, 1), "sd_spread": round(sd, 1), "streak": streak, "streak_sign": sign,
            "since": ser[0][0], "n": len(ser),
            "band": ("樂觀極端" if last[4] >= mean + sd else "悲觀極端" if last[4] <= mean - sd else "中性")}


def build_naaim():
    rows = read_csv(NAAIM_CSV)
    ser = []
    for r in rows:
        d, m = r.get("date"), fnum(r.get("mean_exposure"))
        if not d or m is None:
            continue
        ser.append([d[:10], m, fnum(r.get("quart1")), fnum(r.get("quart2")), fnum(r.get("quart3")),
                    fnum(r.get("bearish_min")), fnum(r.get("bullish_max"))])
    ser.sort(key=lambda x: x[0])
    if not ser:
        return {"series": [], "latest": None}
    vals = [x[1] for x in ser]
    last = ser[-1]
    return {"series": ser, "latest": {"date": last[0], "mean": last[1], "q1": last[2], "q2": last[3], "q3": last[4],
                                      "min": last[5], "max": last[6]},
            "pct_all": pctile(vals, last[1]), "pct_5y": pctile(vals[-260:], last[1]),
            "since": ser[0][0], "n": len(ser),
            "band": ("高曝險" if last[1] >= 90 else "低曝險" if last[1] <= 40 else "中性")}


# ── ETF 資金流 ──────────────────────────────────────────────────────────────
def load_flow_jsonl(t):
    p = os.path.join(FLOWS_DIR, f"{t}.jsonl")
    if not os.path.exists(p):
        return []
    rows = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("shares_outstanding") and r.get("nav"):
                rows.append((r["date"][:10], float(r["shares_outstanding"]), float(r["nav"]), r.get("source") or ""))
    rows.sort()
    return rows


def same_source(a, b):
    """份額來源相同才算當日流量。舊列沒有 source 欄（空字串）時視為與相鄰列相同。"""
    return not a or not b or a == b


def build_flows():
    acc = {}
    for r in read_csv(FLOWS_ACC):
        try:
            acc[(r["etf"], r["date"])] = (float(r["shares"]), float(r["nav"]), (r.get("source") or "").strip())
        except (KeyError, ValueError):
            continue
    # flows 資料夾裡全部基金都累積（週檔要接 50 檔）；儀表板輸出仍只用 FLOW_ETFS 的 13 檔
    all_etfs = sorted(os.path.basename(p)[:-6] for p in os.listdir(FLOWS_DIR) if p.endswith(".jsonl")) \
        if os.path.isdir(FLOWS_DIR) else []
    for t in all_etfs:
        for d, sh, nav, src in load_flow_jsonl(t):
            acc[(t, d)] = (sh, nav, src)
    # 累積檔：前後兩天份額來源不同（例如 yfinance 直接值與推算值互換）的那一天，流量記 0
    os.makedirs(os.path.dirname(FLOWS_ACC), exist_ok=True)
    keys = sorted(acc)
    with open(FLOWS_ACC, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "etf", "shares", "nav", "flow_usd_m", "source"])
        prev = {}
        for t, d in keys:
            sh, nav, src = acc[(t, d)]
            if t not in prev:
                flow = ""
            elif same_source(prev[t][1], src):
                flow = round((sh - prev[t][0]) * nav / 1e6, 2)
            else:
                flow = 0.0
            w.writerow([d, t, int(sh), nav, flow, src])
            prev[t] = (sh, src)
    # 週序列：TradingView 匯出的 2016 年起歷史，之後由上面的每日資料併成新週接續
    weekly = load_weekly(FLOWS_WEEKLY)
    daily_by_etf = {}
    for (t, d), (sh, nav, src) in acc.items():
        if (t, d) not in SKIP_FLOW_DAYS:
            daily_by_etf.setdefault(t, []).append((d, sh, nav, src))
    if weekly:
        weekly = merge_daily_into_weekly(weekly, daily_by_etf, FLOWS_WEEKLY, set(all_etfs) | set(FLOW_ETFS),
                                         sources=WEEKLY_MERGE_SOURCES)
    # 組輸出
    etfs = {}
    for t, zh in FLOW_ETFS.items():
        rows = [(d, acc[(t, d)][:2]) for (tt, d) in keys if tt == t]
        if len(rows) < 10:
            continue
        daily, monthly, prev_sh = [], {}, None
        for d, (sh, nav) in rows:
            if (t, d) in SKIP_FLOW_DAYS:
                continue  # 發行商資料的假跳動，連同它的反向抵銷日一起略過
            if prev_sh is not None:
                fl = (sh - prev_sh) * nav / 1e6
                daily.append([d, round(fl, 1)])
                monthly[d[:7]] = monthly.get(d[:7], 0.0) + fl
            prev_sh = sh
        last_d = rows[-1][0]
        cut4 = (datetime.strptime(last_d, "%Y-%m-%d") - timedelta(days=28)).strftime("%Y-%m-%d")
        cut13 = (datetime.strptime(last_d, "%Y-%m-%d") - timedelta(days=91)).strftime("%Y-%m-%d")
        f4 = sum(v for d, v in daily if d > cut4)
        f13 = sum(v for d, v in daily if d > cut13)
        aum = rows[-1][1][0] * rows[-1][1][1] / 1e6
        etfs[t] = {"zh": zh, "since": rows[0][0], "asof": last_d, "aum_usd_m": round(aum),
                   "monthly": sorted((k, round(v, 1)) for k, v in monthly.items()),
                   "flow_4w": round(f4, 1), "flow_13w": round(f13, 1),
                   "flow_4w_pct_aum": round(100 * f4 / aum, 2) if aum else None,
                   "flow_13w_pct_aum": round(100 * f13 / aum, 2) if aum else None,
                   "shares_latest": int(rows[-1][1][0])}
        ws = weekly_stats(weekly, t) if weekly else None
        if ws:
            etfs[t].update({"flow_4w_w": ws["flow_4w_w"], "pct_4w_10y": ws["pct_4w"], "weekly_since": ws["since"],
                            "weekly_asof": ws["asof"], "weekly_n": ws["n"],
                            "yearly": sorted((y, round(sum(v for d, v in ws["series"] if d.startswith(y)), 1))
                                             for y in {d[:4] for d, _ in ws["series"]})})
            if t == "SMH":
                etfs[t]["weekly"] = [[d, round(v, 1)] for d, v in ws["series"]]
        if t == "SMH":
            etfs[t]["daily"] = daily
    return {"etfs": etfs, "note": "資金流＝每日流通單位數變化×淨值（發行商資料）。SMH 2026-06-17 與 06-22 各有一次約 1,090 萬單位的反向跳動，互相抵銷。"
                                  "週序列 2016-11 起由 TradingView 匯出一次，之後由發行商每日資料併成新週。"}


# ── 週淨申購共用：TradingView 匯出的歷史 ＋ 發行商每日檔接續 ───────────────
def load_weekly(path):
    """{(etf, 週一): [close, flow_m, source, currency]}"""
    weekly = {}
    for r in read_csv(path):
        try:
            weekly[(r["etf"], r["week"])] = [float(r["close"]) if r.get("close") else None, float(r["flow_usd_m"]),
                                             r.get("source") or "tradingview", r.get("currency") or "USD"]
        except (KeyError, ValueError):
            continue
    return weekly


def merge_daily_into_weekly(weekly, daily_by_etf, path, etfs, sources=None):
    """daily_by_etf：{etf: [(date, shares, nav[, source]), …]}。每日流通單位數變化×淨值併成週（週一起算），
    只補 TradingView 最後一週之後的週，寫回 path（source=issuer，每次重算）。
    有第四欄 source 時，前後兩天來源不同的那一天不算流量（來源切換造成的假跳動）；
    一週裡沒有任何一天能算流量就不寫那一週（留空，不寫成 0）。sources 有給時，只有來源在這個集合裡的日子才算。"""
    changed = False
    for t, rows in daily_by_etf.items():
        if t not in etfs:
            continue
        rows = sorted(rows)
        last_tv = max((w for (e, w), v in weekly.items() if e == t and v[2] == "tradingview"), default="")
        cur = next((v[3] for (e, w), v in weekly.items() if e == t), "USD")
        wk, prev, prev_src = {}, None, ""
        for row in rows:
            d, sh, nav = row[:3]
            src = row[3] if len(row) > 3 else ""
            if prev is not None and same_source(prev_src, src) and (sources is None or src in sources):
                wd = date.fromisoformat(d)
                monday = (wd - timedelta(days=wd.weekday())).isoformat()
                wk.setdefault(monday, [0.0, nav])
                wk[monday][0] += (sh - prev) * nav / 1e6
                wk[monday][1] = nav
            prev, prev_src = sh, src
        for monday, (fl, nav) in wk.items():
            if monday <= last_tv:
                continue
            new = [round(nav, 4), round(fl, 2), "issuer", cur]
            if weekly.get((t, monday)) != new:
                weekly[(t, monday)] = new
                changed = True
    if changed:
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["week", "etf", "close", "flow_usd_m", "currency", "source"])
            for (t, wkk), (c, fl, src, cur) in sorted(weekly.items()):
                w.writerow([wkk, t, c if c is not None else "", fl, cur, src])
    return weekly


def weekly_stats(weekly, t):
    """近四週（週資料）的合計與它在整段歷史四週滾動值的分位。"""
    ser = sorted((wkk, v[1]) for (e, wkk), v in weekly.items() if e == t)
    if len(ser) < 20:
        return None
    vals = [v for _, v in ser]
    r4 = [sum(vals[i - 3:i + 1]) for i in range(3, len(vals))]
    f4 = sum(vals[-4:])
    return {"series": ser, "flow_4w_w": round(f4, 1), "pct_4w": pctile(r4, f4), "since": ser[0][0], "asof": ser[-1][0],
            "n": len(ser), "r4": r4, "source_latest": weekly[(t, ser[-1][0])][2]}


# ── 槓桿 ETF 多空流量 ───────────────────────────────────────────────────────
def build_lev():
    """週淨申購：TradingView 匯出的歷史（2016-11 起）＋發行商每日檔接續的新週。"""
    weekly = load_weekly(LEV_WEEKLY)
    if not weekly:
        return {"etfs": {}}
    daily = {}
    if os.path.exists(LEV_DAILY):
        for r in read_csv(LEV_DAILY):
            try:
                daily.setdefault(r["etf"], []).append((r["date"][:10], float(r["shares"]), float(r["nav"])))
            except (KeyError, ValueError):
                continue
    weekly = merge_daily_into_weekly(weekly, daily, LEV_WEEKLY, LEV_ETFS)
    etfs = {}
    for t, (zh, pair, side) in LEV_ETFS.items():
        ws = weekly_stats(weekly, t)
        if not ws:
            continue
        ser, r4 = ws["series"], ws["r4"]
        vals = [v for _, v in ser]
        f4, f13 = sum(vals[-4:]), sum(vals[-13:])
        mx = max(r4)
        mxi = r4.index(mx) + 3
        mn = min(r4)
        mni = r4.index(mn) + 3
        year = ser[-1][0][:4]
        ytd = sum(v for d, v in ser if d.startswith(year))
        etfs[t] = {"zh": zh, "pair": pair, "side": side, "since": ser[0][0], "asof": ser[-1][0], "n": len(ser),
                   "flow_4w": round(f4, 1), "flow_13w": round(f13, 1), "ytd": round(ytd, 1),
                   "pct_4w": pctile(r4, f4),
                   "max_4w": round(mx, 1), "max_4w_week": ser[mxi][0], "min_4w": round(mn, 1), "min_4w_week": ser[mni][0],
                   "yearly": sorted((y, round(sum(v for d, v in ser if d.startswith(y)), 1)) for y in {d[:4] for d, _ in ser}),
                   "series": [[d, round(v, 1)] for d, v in ser if d >= LEV_CHART_FROM],
                   "source_latest": weekly[(t, ser[-1][0])][2]}
    return {"etfs": etfs, "chart_from": LEV_CHART_FROM,
            "note": "週淨申購，百萬美元。2016-11 起的歷史由 TradingView 的 ETF 資金流欄一次匯出；之後的週由發行商每日流通單位數×淨值接續。"}


# ── 狀態列與判讀 ────────────────────────────────────────────────────────────
def build_status(fms, cot, aaii, naaim, flows, lev=None):
    st = []
    if fms.get("latest"):
        L = fms["latest"]
        c = fms.get("latest_cash") or {}
        cash = c.get("cash")
        hot = L["top_pct"] >= 60 or (cash is not None and cash < 4.0)
        band = "共識集中" if L["top_pct"] >= 60 else "共識分散" if L["top_pct"] < 35 else "普通"
        if cash is not None and cash < 4.0:
            band += "；現金低於 4%（BofA 賣出訊號）"
        elif cash is not None and cash > 5.0:
            band += "；現金高於 5%（BofA 買進訊號）"
        st.append({"key": "fms", "label": "基金經理人：最擁擠交易", "value": f"{L['top']}　{L['top_pct']:.0f}%",
                   "sub": f"{L['m']} 調查；現金 {cash:.1f}%（{c.get('m')}）" if cash is not None else f"{L['m']} 調查",
                   "band": band, "hot": hot})
    ext_long = [m["zh"] for m in cot["markets"] if m["band"] == "極端偏多"]
    ext_short = [m["zh"] for m in cot["markets"] if m["band"] == "極端偏空"]
    st.append({"key": "cot", "label": "期貨投機部位（CFTC）",
               "value": ("極端偏多：" + "、".join(ext_long) if ext_long else "沒有極端偏多") + "；" +
                        ("極端偏空：" + "、".join(ext_short) if ext_short else "沒有極端偏空"),
               "sub": f"15 市場，五年分位 ≥90 或 ≤10 算極端；資料到 {cot.get('asof')}",
               "band": f"{len(ext_long) + len(ext_short)} 個極端", "hot": bool(ext_long)})
    if aaii.get("latest"):
        L = aaii["latest"]
        st.append({"key": "aaii", "label": "散戶（AAII 多空差）",
                   "value": f"{L['spread']:+.1f} 個百分點（多 {L['bull']:.0f}%、空 {L['bear']:.0f}%）",
                   "sub": f"{L['date']}；1987 年起分位 {aaii['pct_all']:.0f}%，連續 {aaii['streak']} 週{'偏多' if aaii['streak_sign'] > 0 else '偏空'}",
                   "band": aaii["band"], "hot": aaii["band"] == "樂觀極端"})
    if naaim.get("latest"):
        L = naaim["latest"]
        st.append({"key": "naaim", "label": "主動經理人曝險（NAAIM）", "value": f"{L['mean']:.0f}%",
                   "sub": f"{L['date']}；2006 年起分位 {naaim['pct_all']:.0f}%", "band": naaim["band"], "hot": naaim["band"] == "高曝險"})
    if flows.get("etfs"):
        E = flows["etfs"]
        sec = [(t, v) for t, v in E.items() if t.startswith("XL") or t == "SMH"]
        if sec:
            top_in = max(sec, key=lambda kv: kv[1]["flow_4w_pct_aum"] or -1e9)
            top_out = min(sec, key=lambda kv: kv[1]["flow_4w_pct_aum"] or 1e9)
            st.append({"key": "flows", "label": "ETF 資金流（近四週，占資產）",
                       "value": f"流入最多 {top_in[1]['zh']} {top_in[1]['flow_4w_pct_aum']:+.1f}%；流出最多 {top_out[1]['zh']} {top_out[1]['flow_4w_pct_aum']:+.1f}%",
                       "sub": f"S&P 500 與 11 個產業 ETF 加 SMH；資料到 {E.get('SPY', E.get('SMH'))['asof']}",
                       "band": "", "hot": False})
    if lev and lev.get("etfs"):
        L = lev["etfs"]
        def seg(bull, bear, name):
            parts = [f"{name}：多 {L[t]['flow_4w'] / 100:+.0f} 億" if t == bull else f"空 {L[t]['flow_4w'] / 100:+.0f} 億"
                     for t in (bull, bear) if t in L]
            return "、".join(parts)
        hi = [t for t, v in L.items() if v["pct_4w"] >= 95]
        lo = [t for t, v in L.items() if v["pct_4w"] <= 5]
        band = "；".join(x for x in [("十年分位 ≥95：" + "、".join(hi)) if hi else "", ("≤5：" + "、".join(lo)) if lo else ""] if x)
        asof = max(v["asof"] for v in L.values())
        st.append({"key": "lev", "label": "槓桿 ETF 多空流量（近四週，美元）",
                   "value": "；".join(x for x in [seg("SOXL", "SOXS", "半導體"), seg("TQQQ", "SQQQ", "Nasdaq")] if x),
                   "sub": f"3 倍多空各一檔；2016 年起週資料，到 {asof} 那週",
                   "band": band, "hot": bool(hi or lo)})
    return st


def main():
    fms = build_fms()
    cot = build_cot()
    aaii = build_aaii()
    naaim = build_naaim()
    flows = build_flows()
    lev = build_lev()
    readings = []
    if os.path.exists(READINGS):
        with open(READINGS, encoding="utf-8") as f:
            readings = json.load(f)
    asof = max(x for x in [cot.get("asof"), (aaii.get("latest") or {}).get("date"), (naaim.get("latest") or {}).get("date"),
                           max((e["asof"] for e in flows["etfs"].values()), default=None)] if x)
    payload = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "asof": asof,
        "status": build_status(fms, cot, aaii, naaim, flows, lev),
        "readings": readings,
        "fms": fms, "cot": cot, "aaii": aaii, "naaim": naaim, "flows": flows, "lev": lev,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    s = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    def strip(t):
        return t.replace(t[t.find('"generated_at"'):t.find('"generated_at"') + 40], "") if '"generated_at"' in t else t
    if strip(old) == strip(s):
        print("dash.json：沒有變化")
        return
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"dash.json：寫入 {len(s):,} bytes；FMS {fms['coverage']}，COT {len(cot['markets'])} 市場到 {cot.get('asof')}，"
          f"AAII {aaii.get('n', 0)} 週，NAAIM {naaim.get('n', 0)} 週，ETF {len(flows['etfs'])} 檔，槓桿 ETF {len(lev['etfs'])} 檔")


if __name__ == "__main__":
    main()
