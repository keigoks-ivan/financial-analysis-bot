#!/usr/bin/env python3
"""CEO 關注清單（/horizon/）合成層。

照 CEO 的時間分配排一頁：遠方（2–5 年）、60 天內、今天要處理、各部門方向是否一致，
每塊分「外面」與「公司自己」。全部從既有 CI 產物與 yfinance 算，不呼叫模型、
不靠任何報告刷新（DD／產業報告可能不再更新，只當基準線連結）。

輸入（缺檔不 crash，記進 gaps[]）：
  docs/horizon/questions.json          遠方大問題（人工維護，很少改）
  docs/dd-screener/latest.json         EPS 上修、下次財報日
  docs/dd-screener/eps-estimates-snapshots/YYYY-MM.json  三年成長預估月序列
  docs/intel/data/threads.json         新聞故事線 → 關鍵字配到各題
  docs/market/data/state.json          市況合成層（環境、異常、觸發價、新鮮度、預測到期）
  docs/monitor/data/latest.json        紅燈警報
  docs/monitor/data/macro_calendar.json
  docs/engine/arena-ledger.json        席位名單
  docs/engine/cards.json               查核卡（主張被破、到期）
  docs/long-track-w52-adaptive/state.json  實單主系統權重歷史
  docs/track-record/data/latest.json   DD 裁決事後報酬
  data/sahm_rule.json                  失業率
  gh run list（有 gh 時）              排程失敗
輸出：
  docs/horizon/data/horizon.json       頁面讀這份
  docs/horizon/data/history.json       每日追加各題數字（會累積）
  docs/horizon/data/evidence_log.json  配到各題的故事線（會累積，不刪）

Usage: python3 scripts/build_horizon.py [--no-prices]
"""
from __future__ import annotations

import json
import re
import statistics
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT_DIR = DOCS / "horizon" / "data"
TODAY = datetime.now(timezone(timedelta(hours=8))).date()  # 台北日期

gaps: list[str] = []


def load(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        gaps.append(f"{path.relative_to(ROOT)}：讀取失敗（{type(e).__name__}）")
        return default


def med(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    return round(statistics.median(vals), 2) if vals else None


def parse_date(s):
    try:
        return date.fromisoformat(str(s)[:10])
    except Exception:  # noqa: BLE001
        return None


# ───────────────────────── 價格 ─────────────────────────

def fetch_prices(symbols: list[str]):
    """回傳 {sym: pandas.Series(收盤, 日期索引)}；失敗回空 dict。"""
    try:
        import yfinance as yf
    except ImportError:
        gaps.append("yfinance 未安裝：相對強弱與總經序列略過")
        return {}
    out = {}
    try:
        df = yf.download(symbols, period="7y", interval="1d", auto_adjust=True,
                         progress=False, group_by="ticker", threads=True)
    except Exception as e:  # noqa: BLE001
        gaps.append(f"yfinance 下載失敗：{e}")
        return {}
    for s in symbols:
        try:
            col = df[s]["Close"] if len(symbols) > 1 else df["Close"]
            col = col.dropna()
            if len(col) > 30:
                out[s] = col
        except Exception:  # noqa: BLE001
            continue
    missing = [s for s in symbols if s not in out]
    if missing:
        gaps.append("價格缺：" + "、".join(missing))
    return out


def ret_pct(series, days: int, end_offset: int = 0):
    """過去 days 個日曆日的報酬（%），可往前平移 end_offset 日。"""
    if series is None or len(series) < 5:
        return None
    end_date = series.index[-1] - timedelta(days=end_offset)
    s_end = series[series.index <= end_date]
    if s_end.empty:
        return None
    start_date = s_end.index[-1] - timedelta(days=days)
    s_start = series[series.index <= start_date]
    if s_start.empty:
        return None
    return (float(s_end.iloc[-1]) / float(s_start.iloc[-1]) - 1) * 100


def yf_sym(t: str) -> str:
    return t + ".TW" if t.isdigit() else t


# ───────────────────────── 遠方：各題數字 ─────────────────────────

def basket_metrics(tickers, screener, prices, snaps):
    rows = [screener.get(t) for t in tickers]
    rows = [r for r in rows if r]
    spy = prices.get("SPY")
    m = {
        "n_total": len(tickers),
        "n_eps": sum(1 for r in rows if isinstance(r.get("eps_rev_3m_pct"), (int, float))),
        "eps_rev_3m": med([r.get("eps_rev_3m_pct") for r in rows]),
        # 自有資金撐得起的成長＝增量 ROIC × 再投資率（build_dd_screener 的 implied_growth_pct）
        "self_funded": med([r.get("implied_growth_pct") for r in rows]),
        "n_self": sum(1 for r in rows if isinstance(r.get("implied_growth_pct"), (int, float))),
    }
    # 相對強弱：個股報酬 − SPY 報酬，取中位數
    for key, days, off in (("rs_26w", 182, 0), ("rs_52w", 365, 0), ("rs_52w_prev", 365, 28)):
        vals = []
        spy_r = ret_pct(spy, days, off)
        for t in tickers:
            r = ret_pct(prices.get(yf_sym(t)), days, off)
            if r is not None and spy_r is not None:
                vals.append(r - spy_r)
        m[key] = med(vals)
        if key == "rs_52w":
            m["n_price"] = len(vals)
    # 三年成長預估（月快照，FY1→FY3 年化）：同一批公司前後月比較，避免成分漂移
    series = []
    for month, tick in snaps:
        vals = [tick[t].get("eps_cagr_2y") for t in tickers if t in tick]
        series.append({"month": month, "value": med(vals)})
    m["growth_3y_series"] = series
    m["growth_3y"] = series[-1]["value"] if series else None
    if len(snaps) >= 2:
        (_, cur), (_, prev) = snaps[-1], snaps[-2]
        common = [t for t in tickers if t in cur and t in prev]
        a = med([cur[t].get("eps_cagr_2y") for t in common])
        b = med([prev[t].get("eps_cagr_2y") for t in common])
        m["growth_3y_chg"] = round(a - b, 2) if a is not None and b is not None else None
    else:
        m["growth_3y_chg"] = None
    return m


def macro_series(q, prices, sahm):
    out = {}
    for s in q.get("series", []):
        k = s["key"]
        if s.get("src") == "sahm":
            for suf in ("", "_prev", "_as_of"):
                out[k + suf] = sahm.get(k + suf)
            continue
        ser = prices.get(s["sym"])
        if ser is None:
            out[k] = None
            continue
        last = float(ser.iloc[-1])
        yr = ser[ser.index <= ser.index[-1] - timedelta(days=365)]
        m4 = ser[ser.index <= ser.index[-1] - timedelta(days=28)]
        three = ser.tail(756)
        pct = round(sum(1 for v in three if v <= last) / len(three) * 100, 1)
        out[k] = round(last, 2)
        out[k + "_prev"] = round(float(m4.iloc[-1]), 2) if not m4.empty else None
        # 殖利率這類本身是 % 的序列，一年變化用百分點；其他用漲跌幅
        if yr.empty:
            out[k + "_chg_52w"] = None
        elif s.get("unit") == "%":
            out[k + "_chg_52w"] = round(last - float(yr.iloc[-1]), 2)
        else:
            out[k + "_chg_52w"] = round((last / float(yr.iloc[-1]) - 1) * 100, 2)
        out[k + "_pctile_3y"] = pct
        out[k + "_as_of"] = str(ser.index[-1].date())
    return out


def compute_sahm(sahm_doc):
    try:
        us = sahm_doc["countries"]["US"]["unemployment_series"]
    except Exception:  # noqa: BLE001
        return {}
    vals = [v for _, v in us]
    ma3 = [sum(vals[i - 2:i + 1]) / 3 for i in range(2, len(vals))]
    if len(ma3) < 13:
        return {}
    s_now = ma3[-1] - min(ma3[-13:-1])
    s_prev = ma3[-2] - min(ma3[-14:-2])
    return {"unrate": vals[-1], "unrate_prev": vals[-2], "unrate_as_of": us[-1][0],
            "sahm": round(s_now, 2), "sahm_prev": round(s_prev, 2), "sahm_as_of": us[-1][0]}


def metric_value(path: str, metrics: dict):
    """alarm metric 路徑：gain.eps_rev_3m／lose.rs_52w／spread.eps_rev_3m／series.dxy.chg_52w。"""
    parts = path.split(".")
    if parts[0] == "series":
        key = parts[1] + ("_" + parts[2] if len(parts) > 2 else "")
        return metrics.get("series", {}).get(key)
    return (metrics.get(parts[0]) or {}).get(parts[1])


def check_alarm(alarm, metrics):
    ops = {"<": lambda a, b: a < b, ">": lambda a, b: a > b, ">=": lambda a, b: a >= b}
    vals = [metric_value(p, metrics) for p in alarm["metric"].split("&")]
    if any(v is None for v in vals):
        return {"hit": None, "values": vals}
    return {"hit": all(ops[alarm["op"]](v, alarm["value"]) for v in vals), "values": vals}


def match_threads(q, threads):
    kws = [k.lower() for k in q.get("keywords", [])]
    cats = set(q.get("categories", []))
    hits = []
    for th in threads:
        text = (th.get("title_zh", "") + " " + " ".join(th.get("keywords", []))).lower()
        if any(k in text for k in kws) or th.get("category") in cats:
            hits.append(th)
    return hits


def lean_of(q, metrics):
    """市場目前站哪邊：三個訊號（EPS 上修、三年成長月變、一年對大盤；成對題用差）多數決。"""
    if q["kind"] == "industry":
        g = metrics.get("gain") or {}
        sig = [g.get("eps_rev_3m"), g.get("growth_3y_chg"), g.get("rs_52w")]
        yes, no = "偏是", "偏否"
    elif q["kind"] == "pair":
        sp = metrics.get("spread") or {}
        sig = [sp.get("eps_rev_3m"), sp.get("rs_52w"), sp.get("rs_26w")]
        yes, no = f"偏{q['gain']['label']}", f"偏{q['lose']['label']}"
    else:
        return None
    vals = [v for v in sig if v is not None]
    if len(vals) < 2:
        return {"text": "資料不足", "n_pos": None, "n": len(vals)}
    pos = sum(1 for v in vals if v > 0)
    text = yes if pos * 2 > len(vals) else (no if pos * 2 < len(vals) else "分歧")
    return {"text": text, "n_pos": pos, "n": len(vals)}


BASE_DATE = "2026-01-02"  # 籃子指數基期；回頭對帳用兩個日期的比值，基期本身不影響結果


def basket_px(tickers, prices):
    vals = []
    for t in tickers:
        s = prices.get(yf_sym(t))
        if s is None:
            continue
        b = s[s.index <= BASE_DATE]
        if not b.empty:
            vals.append(float(s.iloc[-1]) / float(b.iloc[-1]))
    return round(sum(vals) / len(vals), 4) if vals else None


def weekly_basket(tickers, prices, weeks=104):
    """等權籃子的週報酬（近兩年）。"""
    import pandas as pd
    cols = {t: prices[yf_sym(t)] for t in tickers if yf_sym(t) in prices}
    if not cols:
        return None
    df = pd.DataFrame(cols).resample("W-FRI").last().pct_change(fill_method=None).tail(weeks)
    return df.mean(axis=1, skipna=True)


def question_series(q, prices):
    if q["kind"] == "industry":
        return weekly_basket(q["gain"]["tickers"], prices)
    if q["kind"] == "pair":
        a, b = weekly_basket(q["gain"]["tickers"], prices), weekly_basket(q["lose"]["tickers"], prices)
        return a - b if a is not None and b is not None else None
    s = (q.get("series") or [{}])[0]
    ser = prices.get(s.get("sym")) if s.get("sym") else None
    if ser is None:
        return None
    w = ser.resample("W-FRI").last()
    # 殖利率看週變化（百分點），其他看週報酬
    return (w.diff() if s.get("unit") == "%" else w.pct_change(fill_method=None)).tail(104)


def real_bets(questions, prices, seats_by_q, threshold=0.6, show=0.4):
    """用近兩年週報酬相關係數，把一起動的題目併成同一個押注。"""
    import pandas as pd
    ser = {q["id"]: question_series(q, prices) for q in questions}
    ser = {k: v for k, v in ser.items() if v is not None and v.dropna().size > 40}
    if len(ser) < 2:
        return [], {}
    corr = pd.DataFrame(ser).corr(min_periods=40)
    ids = list(corr.columns)
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    moves_with = {i: [] for i in ids}
    for i_, a in enumerate(ids):
        for b in ids[i_ + 1:]:
            c = corr.loc[a, b]
            if pd.isna(c):
                continue
            if abs(c) >= show:
                moves_with[a].append({"id": b, "corr": round(float(c), 2)})
                moves_with[b].append({"id": a, "corr": round(float(c), 2)})
            if abs(c) >= threshold:
                parent[find(a)] = find(b)
    groups = {}
    for i in ids:
        groups.setdefault(find(i), []).append(i)
    qmap = {q["id"]: q for q in questions}
    bets = []
    for members in groups.values():
        pairs = [abs(float(corr.loc[a, b])) for n, a in enumerate(members) for b in members[n + 1:]]
        seats = sorted({t for m in members for t in seats_by_q.get(m, [])})
        bets.append({"qids": members, "labels": [qmap[m]["q"] for m in members],
                     "avg_corr": round(sum(pairs) / len(pairs), 2) if pairs else None,
                     "seats": seats})
    bets.sort(key=lambda b: (-len(b["seats"]), -len(b["qids"])))
    for v in moves_with.values():
        v.sort(key=lambda x: -abs(x["corr"]))
    no_series = [q["id"] for q in questions if q["id"] not in ser]
    return bets, {"moves_with": moves_with, "no_series": no_series}


SCENARIOS = [
    {"key": "2022", "label": "2022 升息與科技股修正", "start": "2022-01-03", "end": "2022-10-14"},
    {"key": "2020", "label": "2020 疫情急跌", "start": "2020-02-19", "end": "2020-03-23"},
    {"key": "2024", "label": "2024 年 7 月 AI 股急修正", "start": "2024-07-10", "end": "2024-08-07"},
]


def window_ret(series, start, end):
    if series is None:
        return None
    a = series[series.index >= start]
    b = series[series.index <= end]
    if a.empty or b.empty or a.index[0] > b.index[-1]:
        return None
    return (float(b.iloc[-1]) / float(a.iloc[0]) - 1) * 100


def sim_live(hist, legs, px, start, end):
    """用實單主系統當時的權重（含回測期）重算區間報酬；權重隔天生效。"""
    w = {h["date"]: {t: (v.get("final_pct") or 0) / 100 for t, v in h["tickers"].items()} for h in hist}
    if not w or min(w) > start:
        return None
    dates = [d for d in px[legs[0]].index if start <= str(d.date()) <= end]
    nav, last_w = 1.0, None
    earlier = [k for k in w if k < start]
    last_w = w[max(earlier)] if earlier else None
    for d in dates:
        if last_w is not None:
            r = 0.0
            for l in legs:
                s = px[l]
                prev = s[s.index < d]
                if d in s.index and not prev.empty:
                    r += last_w.get(l, 0) * (float(s[d]) / float(prev.iloc[-1]) - 1)
            nav *= 1 + r
        ds = str(d.date())
        if ds in w:
            last_w = w[ds]
    return round((nav - 1) * 100, 1)


# ───────────────────────── 主流程 ─────────────────────────

def main():
    no_prices = "--no-prices" in sys.argv
    qdoc = load(DOCS / "horizon" / "questions.json", {"questions": []})
    questions = qdoc["questions"]
    scr_doc = load(DOCS / "dd-screener" / "latest.json", {"stocks": []})
    screener = {r["ticker"]: r for r in scr_doc.get("stocks", [])}
    state = load(DOCS / "market" / "data" / "state.json", {}) or {}
    monitor = load(DOCS / "monitor" / "data" / "latest.json", {}) or {}
    cal = load(DOCS / "monitor" / "data" / "macro_calendar.json", {"events": []}) or {"events": []}
    ledger = load(DOCS / "engine" / "arena-ledger.json", {}) or {}
    cards = load(DOCS / "engine" / "cards.json", {}) or {}
    live = load(DOCS / "long-track-w52-adaptive" / "state.json", {}) or {}
    track = load(DOCS / "track-record" / "data" / "latest.json", {}) or {}
    threads = (load(DOCS / "intel" / "data" / "threads.json", {}) or {}).get("threads", [])
    sahm = compute_sahm(load(ROOT / "data" / "sahm_rule.json", {}) or {})

    # 月快照（只取 YYYY-MM.json，月中補拍的 -DD 檔略過）
    snaps = []
    for p in sorted((DOCS / "dd-screener" / "eps-estimates-snapshots").glob("*.json")):
        if re.fullmatch(r"\d{4}-\d{2}", p.stem):
            d = load(p, {})
            if d and d.get("tickers"):
                snaps.append((p.stem, d["tickers"]))

    # 席位
    snap = (ledger.get("snapshots") or [{}])[-1]
    seats_core = snap.get("core", [])
    seats_sat = snap.get("sat", [])
    seats = seats_core + seats_sat

    def tlink(t):
        """站內個股頁 /t/{T}.html；台股代號試 .TW。沒有頁面回 None。"""
        for name in (t, t + ".TW"):
            if (DOCS / "t" / f"{name}.html").exists():
                return f"/t/{name}.html"
        return None

    # 價格
    syms = {"SPY", "QQQ", "SMH", "0050.TW", "2330.TW"}
    for q in questions:
        for k in ("gain", "lose"):
            if q.get(k):
                syms.update(yf_sym(t) for t in q[k]["tickers"])
        for s in q.get("series", []):
            if s.get("sym"):
                syms.add(s["sym"])
    syms.update(yf_sym(t) for t in seats)
    prices = {} if no_prices else fetch_prices(sorted(syms))

    # ── 遠方：外面（大問題） ──
    far = []
    for q in questions:
        metrics = {}
        if q.get("gain"):
            metrics["gain"] = basket_metrics(q["gain"]["tickers"], screener, prices, snaps)
        if q.get("lose"):
            metrics["lose"] = basket_metrics(q["lose"]["tickers"], screener, prices, snaps)
        if q.get("gain") and q.get("lose"):
            sp = {}
            for k in ("eps_rev_3m", "rs_26w", "rs_52w", "growth_3y"):
                a, b = metrics["gain"].get(k), metrics["lose"].get(k)
                sp[k] = round(a - b, 2) if a is not None and b is not None else None
            metrics["spread"] = sp
        if q.get("capex"):
            metrics["capex"] = {"capex_pct_rev": med([(screener.get(t) or {}).get("capex_pct_rev")
                                                      for t in q["capex"]["tickers"]])}
        if q.get("series"):
            metrics["series"] = macro_series(q, prices, sahm)
        alarm = check_alarm(q["alarm"], metrics) if q.get("alarm") else None
        exposure = set(q.get("gain", {}).get("tickers", [])) | set(q.get("lose", {}).get("tickers", [])) \
            | set(q.get("related", {}).get("tickers", []))
        my_seats = [t for t in seats if t in exposure]
        hits = match_threads(q, threads)
        far.append({
            "id": q["id"], "kind": q["kind"], "q": q["q"], "why": q.get("why"),
            "gain": q.get("gain"), "lose": q.get("lose"), "capex": q.get("capex"),
            "series_def": q.get("series"), "alarm_def": q.get("alarm"),
            "baseline": q.get("baseline", []), "metrics": metrics, "alarm": alarm,
            "my_seats": my_seats,
            "lean": lean_of(q, metrics),
            "px": {"gain": basket_px(q["gain"]["tickers"], prices) if q.get("gain") else None,
                   "lose": basket_px(q["lose"]["tickers"], prices) if q.get("lose") else None},
            "threads_now": [{"title": t["title_zh"], "heat": t.get("heat"), "status": t.get("status"),
                             "last_seen": t.get("last_seen")} for t in
                            sorted(hits, key=lambda x: x.get("last_seen", ""), reverse=True)[:5]],
        })

    # 新聞累積帳（不刪，只加與更新）
    ev_path = OUT_DIR / "evidence_log.json"
    ev = load(ev_path, {"entries": {}}) if ev_path.exists() else {"entries": {}}
    for q in questions:
        for th in match_threads(q, threads):
            key = f"{q['id']}|{th['id']}"
            e = ev["entries"].get(key) or {"qid": q["id"], "thread_id": th["id"], "title": th["title_zh"],
                                          "first_seen": th.get("first_seen"), "logged_at": str(TODAY)}
            e.update({"last_seen": th.get("last_seen"), "heat": th.get("heat"), "status": th.get("status"),
                      "days": len(th.get("daily_counts") or {})})
            ev["entries"][key] = e
    for f in far:
        mine = [e for e in ev["entries"].values() if e["qid"] == f["id"]]
        f["evidence_total"] = len(mine)
        f["evidence_recent"] = sorted(mine, key=lambda e: e.get("last_seen") or "", reverse=True)[:6]

    # ── 連動：哪幾題其實是同一個押注 ──
    bets, link_info = ([], {}) if not prices else real_bets(
        questions, prices, {f["id"]: f["my_seats"] for f in far})
    for f in far:
        f["moves_with"] = (link_info.get("moves_with") or {}).get(f["id"], [])

    # ── 盲點：還在追、但九題都沒涵蓋的故事線 ──
    matched = {e["thread_id"] for e in ev["entries"].values()}
    seen_titles = set()
    blind = []
    for th in sorted(threads, key=lambda t: (t.get("heat") != "up", -len(t.get("daily_counts") or {}))):
        if th["id"] in matched or th.get("status") != "active" or th["title_zh"] in seen_titles:
            continue
        seen_titles.add(th["title_zh"])
        blind.append({"title": th["title_zh"], "category": th.get("category"), "heat": th.get("heat"),
                      "days": len(th.get("daily_counts") or {}), "first_seen": th.get("first_seen"),
                      "last_seen": th.get("last_seen")})
    n_active = sum(1 for t in threads if t.get("status") == "active")

    # ── 遠方：公司（策略還有效嗎） ──
    strategy = []
    # 實單主系統：以權重歷史 × 日報酬重算，對照同一組標的等權持有
    def live_perf(hist_key, legs, days):
        hist = live.get(hist_key) or []
        if not hist or not all(prices.get(yf_sym(l)) is not None for l in legs):
            return None
        w = {h["date"]: {t: (v.get("final_pct") or 0) / 100 for t, v in h["tickers"].items()} for h in hist}
        start = TODAY - timedelta(days=days)
        px = {l: prices[yf_sym(l)] for l in legs}
        dates = [d for d in px[legs[0]].index if d.date() > start]
        nav = bench = 1.0
        last_w = None
        for i, d in enumerate(dates):
            ds = str(d.date())
            if last_w is not None:
                rets = {}
                for l in legs:
                    s = px[l]
                    prev = s[s.index < d]
                    if d in s.index and not prev.empty:
                        rets[l] = float(s[d]) / float(prev.iloc[-1]) - 1
                nav *= 1 + sum(last_w.get(l, 0) * rets.get(l, 0) for l in legs)
                bench *= 1 + sum(rets.get(l, 0) for l in legs) / len(legs)
            if ds in w:
                last_w = w[ds]
            elif last_w is None:
                earlier = [k for k in w if k <= ds]
                last_w = w[max(earlier)] if earlier else None
        return {"ret": round((nav - 1) * 100, 1), "bench": round((bench - 1) * 100, 1)}

    for label, key, legs in (("實單主系統・美股（QQQ＋SMH）", "history_us", ["QQQ", "SMH"]),
                             ("實單主系統・台股（0050＋2330）", "history_tw", ["0050", "2330"])):
        p1 = live_perf(key, legs, 365)
        if p1:
            strategy.append({"label": label, "window": "近 1 年", "ret": p1["ret"], "bench": p1["bench"],
                             "bench_label": "同標的等權持有", "diff": round(p1["ret"] - p1["bench"], 1),
                             "note": "權重含回測期（實單 2026-07-18 起）",
                             "link": "/long-track-w52-adaptive/"})
    # 席位：現任名單自上次換席日以來等權報酬 vs SPY
    sd = parse_date(snap.get("date"))
    if sd and seats and prices.get("SPY") is not None:
        days = (TODAY - sd).days
        rs = [ret_pct(prices.get(yf_sym(t)), days) for t in seats]
        rs = [r for r in rs if r is not None]
        spy_r = ret_pct(prices["SPY"], days)
        if rs and spy_r is not None:
            avg = sum(rs) / len(rs)
            strategy.append({"label": f"席位引擎（{len(seats)} 席等權）", "window": f"{sd} 起",
                             "ret": round(avg, 1), "bench": round(spy_r, 1), "bench_label": "SPY",
                             "diff": round(avg - spy_r, 1), "note": "期間短，只看方向",
                             "link": "/cockpit/"})
    # DD 裁決：進場 vs 觀望，30 天報酬中位數
    try:
        v = track["tables"]["v13plus"]
        e30, w30 = v["進場"]["windows"]["d30"], v["觀望"]["windows"]["d30"]
        strategy.append({"label": "DD 裁決：進場 vs 觀望", "window": "發布後 30 天",
                         "ret": e30["median"], "bench": w30["median"], "bench_label": "觀望組",
                         "diff": round(e30["median"] - w30["median"], 1) if None not in (e30["median"], w30["median"]) else None,
                         "note": f"進場 {e30['n']} 份、觀望 {w30['n']} 份；進場贏 SPY 比例 {e30['pct_beat_spy']}%",
                         "link": "/track-record/"})
    except Exception:  # noqa: BLE001
        gaps.append("track-record 裁決表讀不到")

    # ── 遠方：公司（生存風險） ──
    risks = []
    q_ai = next((f for f in far if f["id"] == "ai_compute"), None)
    if q_ai and seats:
        core_in = [t for t in seats_core if t in q_ai["my_seats"]]
        risks.append({
            "key": "concentration",
            "title": "押注集中在「AI 算力還在加速」",
            "value": f"核心 {len(core_in)}/{len(seats_core)}、全部 {len(q_ai['my_seats'])}/{len(seats)} 席",
            "level": "high" if len(q_ai["my_seats"]) / len(seats) >= 0.5 else "mid",
            "detail": "席位裡屬於 AI 硬體鏈（晶片、設備、代工組裝、儲存）的比例；實單的 SMH 與台積電也在同一題。",
            "link": "/cockpit/",
        })
    exp_tw = live.get("combined_exposure_tw_pct")
    exp_us = live.get("combined_exposure_us_pct")
    if exp_tw is not None:
        risks.append({
            "key": "leverage",
            "title": "實單曝險",
            "value": f"美股 {exp_us}%、台股 {exp_tw}%",
            "level": "high" if max(exp_tw or 0, exp_us or 0) > 100 else "low",
            "detail": "超過 100% 代表有用槓桿。台股兩條腿是 0050 與台積電，跟上一條的 AI 題目重疊。",
            "link": "/long-track-w52-adaptive/",
        })
    geo = [t for t in threads if t.get("category") == "geo" and any(
        k in t.get("title_zh", "") for k in ("台灣", "台海", "中國", "川習", "晶片", "半導體", "出口管制"))]
    risks.append({
        "key": "taiwan",
        "title": "台海與美中晶片管制",
        "value": f"情報故事線 {len(geo)} 條在追",
        "level": "mid" if geo else "low",
        "detail": "台積電同時在席位、實單美股（SMH）、實單台股裡；這條風險一旦發生，三處一起受影響。",
        "threads": [t["title_zh"] for t in geo[:4]],
        "link": "/intel/threads.html",
    })

    # ── 壓力測試：歷史上三次大跌重演一次 ──
    stress = []
    if prices:
        px_live = {l: prices.get(yf_sym(l)) for l in ("QQQ", "SMH", "0050", "2330")}
        last_us = ((live.get("history_us") or [{}])[-1]).get("tickers", {})
        last_tw = ((live.get("history_tw") or [{}])[-1]).get("tickers", {})
        for sc in SCENARIOS:
            a, b = sc["start"], sc["end"]
            r = {l: window_ret(px_live[l], a, b) for l in px_live}

            def hold(last, legs):
                if any(r[l] is None for l in legs):
                    return None
                return round(sum((last.get(l, {}).get("final_pct") or 0) / 100 * r[l] for l in legs), 1)
            seat_r, proxied = [], []
            for t in seats:
                x = window_ret(prices.get(yf_sym(t)), a, b)
                if x is None:
                    x = r["SMH"]
                    proxied.append(t)
                if x is not None:
                    seat_r.append(x)
            ok_us = all(px_live[l] is not None for l in ("QQQ", "SMH"))
            ok_tw = all(px_live[l] is not None for l in ("0050", "2330"))
            stress.append({
                **sc,
                "spy": round(window_ret(prices.get("SPY"), a, b) or 0, 1),
                "smh": round(r["SMH"], 1) if r["SMH"] is not None else None,
                "live_us_hold": hold(last_us, ["QQQ", "SMH"]),
                "live_tw_hold": hold(last_tw, ["0050", "2330"]),
                "live_us_rule": sim_live(live.get("history_us") or [], ["QQQ", "SMH"],
                                         {l: px_live[l] for l in ("QQQ", "SMH")}, a, b) if ok_us else None,
                "live_tw_rule": sim_live(live.get("history_tw") or [], ["0050", "2330"],
                                         {l: px_live[l] for l in ("0050", "2330")}, a, b) if ok_tw else None,
                "seats": round(sum(seat_r) / len(seat_r), 1) if seat_r else None,
                "seats_proxied": proxied,
            })

    # ── 60 天內 ──
    horizon_end = TODAY + timedelta(days=60)
    upcoming = []
    for e in cal.get("events", []):
        d = parse_date(e.get("date"))
        if d and TODAY <= d <= horizon_end:
            upcoming.append({"date": str(d), "side": "外面", "type": e.get("type"), "label": e.get("label"),
                             "tag": "總經", "link": "/intel/calendar.html"})
    basket_t = {}
    for q in questions:
        for k in ("gain", "lose"):
            for t in (q.get(k) or {}).get("tickers", []):
                basket_t.setdefault(t, q["q"])
    for t in sorted(set(seats) | set(basket_t)):
        r = screener.get(t)
        d = parse_date((r or {}).get("next_earnings_date"))
        if d and TODAY <= d <= horizon_end:
            upcoming.append({"date": str(d), "side": "外面", "type": "財報",
                             "label": f"{t} 財報", "tag": "席位" if t in seats else "遠方問題",
                             "note": basket_t.get(t), "link": tlink(t)})
    # 公司自己的日程
    lr = ledger.get("last_rotation_month")
    if lr:
        y, m = map(int, lr.split("-")[:2])
        nm = date(y + (m // 12), m % 12 + 1, 1)
        if nm <= horizon_end:
            upcoming.append({"date": str(max(nm, TODAY)), "side": "公司", "type": "換席",
                             "label": "席位引擎月度換席", "tag": "系統", "link": "/cockpit/"})
    # 預測對帳、總經引信、查核卡到期：同一天合併成一行，避免洗版
    def grouped(items, kind, fmt, tag, link):
        by_day = {}
        for d, name in items:
            if d and TODAY <= d <= horizon_end:
                by_day.setdefault(str(d), []).append(name)
        for d, names in by_day.items():
            upcoming.append({"date": d, "side": "公司", "type": kind, "label": fmt(names), "tag": tag,
                             "items": names, "link": link})
    grouped([(parse_date(c.get("resolve_by")), c.get("label")) for c in state.get("council", [])],
            "預測到期", lambda n: f"市況預測對帳 {len(n)} 筆", "市況", "/market/")
    grouped([(parse_date(f.get("resolve_by")), f"{f.get('metric')} 門檻 {f.get('threshold')}（現 {f.get('now')}）")
             for f in state.get("fuses", [])],
            "引信到期", lambda n: f"總經引信到期 {len(n)} 條", "市況", "/market/")
    card_items = [(parse_date(c.get("next_deadline")), t) for t, c in (cards.get("by_ticker") or {}).items()]
    grouped([x for x in card_items if x[1] in seats], "查核到期",
            lambda n: f"席位查核卡到期：{'、'.join(n)}", "席位", "/engine/cards.html")
    grouped([x for x in card_items if x[1] not in seats], "查核到期",
            lambda n: f"查核卡到期 {len(n)} 檔：{'、'.join(n[:5])}{'…' if len(n) > 5 else ''}", "查核卡", "/engine/cards.html")
    upcoming.sort(key=lambda x: (x["date"], x["side"]))

    # ── 今天要處理 ──
    fires_out = []
    for a in state.get("anomalies", []):
        if a.get("sev") == "crit":
            fires_out.append({"side": "外面", "level": "high", "text": a["msg"], "link": "/market/"})
    for a in monitor.get("alerts_today", []):
        if a.get("sev") == "red" and not any(a["msg"] == f["text"] for f in fires_out):
            fires_out.append({"side": "外面", "level": "high", "text": a["msg"], "link": "/intel/gauges.html"})
    triggers = state.get("triggers", [])
    fires_co = []
    fresh_link = {"monitor": "/monitor/", "detective": "/detective/", "flowmap": "/flowmap/",
                  "statlab": "/statlab/", "regime": "/regime/", "crowding": "/crowding/",
                  "總經時鐘": "/macro/", "intel": "/intel/"}
    for f in state.get("freshness", []):
        # 週更、月頻來源天生有發布時滯（COT 週五才公布上週二的部位；月資料下個月中才出），
        # 健康時也常落在 warn，只在真正 stale 才列。日更的 warn 照列（2026-09-24 flowmap／
        # statlab 卡在 9/21 就是靠 warn 抓到的）；總經時鐘卡在 7 月時已是 stale，照樣會列。
        if f.get("status") == "warn" and f.get("cadence") in ("週更", "月頻"):
            continue
        if f.get("status") not in ("ok", None):
            link = next((v for k, v in fresh_link.items() if k in f["pipeline"]), "/market/")
            fires_co.append({"side": "公司", "level": "mid",
                             "text": f"{f['pipeline']} 資料停在 {f.get('as_of')}（應為{f.get('cadence')}）",
                             "link": link})
    breach = [(t, c) for t, c in (cards.get("by_ticker") or {}).items() if c.get("n_breach")]
    if breach:
        fires_co.append({"side": "公司", "level": "high",
                         "text": "查核卡主張被推翻：" + "、".join(f"{t}（{c['n_breach']} 條）" for t, c in breach),
                         "link": "/engine/cards.html"})
    overdue = [t for t, c in (cards.get("by_ticker") or {}).items()
               if c.get("n_due") and (parse_date(c.get("next_deadline")) or TODAY) < TODAY]
    if overdue:
        fires_co.append({"side": "公司", "level": "mid",
                         "text": f"查核卡過期沒複查：{len(overdue)} 檔（{'、'.join(overdue[:6])}{'…' if len(overdue) > 6 else ''}）",
                         "link": "/engine/cards.html"})
    # 排程失敗（每個 workflow 只看最近一次）
    try:
        res = subprocess.run(["gh", "run", "list", "--limit", "200", "--json",
                              "workflowName,conclusion,createdAt,url"],
                             capture_output=True, text=True, timeout=60, cwd=ROOT)
        runs = json.loads(res.stdout) if res.returncode == 0 else None
        if runs is None:
            gaps.append("gh run list 失敗：排程狀態略過")
        else:
            latest = {}
            for r in runs:
                latest.setdefault(r["workflowName"], r)
            for name, r in latest.items():
                if r.get("conclusion") == "failure":
                    fires_co.append({"side": "公司", "level": "high",
                                     "text": f"排程失敗：{name}（{r['createdAt'][:10]}）", "link": r["url"]})
    except Exception:  # noqa: BLE001
        gaps.append("找不到 gh：排程狀態略過")

    # ── 方向一致嗎 ──
    env = state.get("environment", [])
    market_rows = [e for e in env if e.get("key") != "system_cockpit"]
    n_warn = sum(1 for e in market_rows if e.get("tone") == "warn" and not e.get("stale"))
    n_fresh = sum(1 for e in market_rows if not e.get("stale"))
    exp_rule = (state.get("exposure_rule") or {}).get("target")
    kelly = (state.get("kelly_rule") or {}).get("exposure")
    env_link = {"regime": "/regime/", "macro_clock": "/macro/", "detective": "/detective/", "monitor": "/monitor/"}
    depts = [{"label": e["label"], "value": e["value"], "tone": e.get("tone"), "stale": e.get("stale"),
              "link": e.get("link") or env_link.get(e.get("key"))} for e in market_rows]
    depts.append({"label": "實單主系統目標曝險", "value": f"美 {exp_us}%・台 {exp_tw}%", "tone": "info",
                  "link": "/long-track-w52-adaptive/"})
    if exp_rule is not None:
        depts.append({"label": "曝險規則（波動・趨勢・信用）", "value": f"{round(exp_rule * 100)}%", "tone": "info"})
    if kelly is not None:
        depts.append({"label": "凱利規則", "value": f"{round(kelly * 100)}%", "tone": "info"})
    depts.append({"label": "席位引擎", "value": f"核心 {len(seats_core)}＋衛星 {len(seats_sat)} 席（{snap.get('date')}）",
                  "tone": "info", "link": "/cockpit/"})
    conflicts = []
    if n_fresh and n_warn * 2 > n_fresh and max(exp_us or 0, exp_tw or 0) >= 100:
        conflicts.append(f"市況 {n_warn}/{n_fresh} 項偏警戒，實單曝險仍在 {max(exp_us or 0, exp_tw or 0)}%。"
                         "兩邊規則各自成立，但方向不同，值得看一下原因。")
    alarmed_with_seats = [f for f in far if (f["alarm"] or {}).get("hit") and f["my_seats"]]
    for f in alarmed_with_seats:
        conflicts.append(f"「{f['q']}」碰到警戒線，但席位裡還有 {len(f['my_seats'])} 檔押在這題。")

    # ── 今天先看（規則排序，最多 5 件） ──
    top = []
    for f in alarmed_with_seats:
        top.append({"rank": 1, "text": f"遠方警戒：{f['alarm_def']['text']}，席位有 {len(f['my_seats'])} 檔在這題",
                    "anchor": f"#q-{f['id']}"})
    for x in fires_co:
        if x["level"] == "high":
            top.append({"rank": 2, "text": x["text"], "anchor": "#today", "link": x.get("link")})
    for x in fires_out:
        top.append({"rank": 3, "text": "市場：" + x["text"], "anchor": "#today", "link": x.get("link")})
    soon = [u for u in upcoming if parse_date(u["date"]) <= TODAY + timedelta(days=7)
            and (u["tag"] in ("席位",) or u["type"] in ("FOMC", "CPI", "NFP", "PCE", "換席"))]
    for u in soon[:3]:
        top.append({"rank": 4, "text": f"{u['date'][5:]} {u['label']}", "anchor": "#soon", "link": u.get("link")})
    for f in far:
        if (f["alarm"] or {}).get("hit") and not f["my_seats"]:
            top.append({"rank": 5, "text": f"遠方警戒：{f['alarm_def']['text']}", "anchor": f"#q-{f['id']}"})
    for r in risks:
        if r["level"] == "high":
            top.append({"rank": 6, "text": f"{r['title']}：{r['value']}", "anchor": "#risk", "link": r.get("link")})
    top.sort(key=lambda x: x["rank"])
    top = top[:5]

    # ── 歷史累積 ──
    hist_path = OUT_DIR / "history.json"
    hist = load(hist_path, {"rows": {}}) if hist_path.exists() else {"rows": {}}
    row = {}
    for f in far:
        m = f["metrics"]
        row[f["id"]] = {k: v for k, v in {
            "gain_eps": (m.get("gain") or {}).get("eps_rev_3m"),
            "gain_rs52": (m.get("gain") or {}).get("rs_52w"),
            "lose_eps": (m.get("lose") or {}).get("eps_rev_3m"),
            "lose_rs52": (m.get("lose") or {}).get("rs_52w"),
            "growth3y": (m.get("gain") or {}).get("growth_3y"),
            **{k: v for k, v in (m.get("series") or {}).items() if not k.endswith(("_as_of", "_prev"))},
            "alarm": (f["alarm"] or {}).get("hit"),
            "lean": (f.get("lean") or {}).get("text"),
            "gain_px": f["px"]["gain"],
            "lose_px": f["px"]["lose"],
        }.items() if v is not None}
    row["_spy_px"] = basket_px(["SPY"], prices) if prices else None
    hist["rows"][str(TODAY)] = row
    # 一個月前的 EPS 上修，給箭頭用
    past = [d for d in hist["rows"] if parse_date(d) and parse_date(d) <= TODAY - timedelta(days=28)]
    ref = hist["rows"][max(past)] if past else {}
    for f in far:
        f["eps_prev_month"] = (ref.get(f["id"]) or {}).get("gain_eps")
    first_day = min(hist["rows"])

    # ── 自己考自己：30／90 天前市場站哪邊，後來籃子有沒有贏 ──
    review = []
    for f in far:
        if f["kind"] == "macro":
            continue
        for days in (30, 90):
            olds = [d for d in hist["rows"] if parse_date(d) <= TODAY - timedelta(days=days)
                    and (hist["rows"][d].get(f["id"]) or {}).get("lean")]
            if not olds:
                continue
            d0 = max(olds)
            then, now_row = hist["rows"][d0][f["id"]], row.get(f["id"]) or {}
            if f["kind"] == "pair":
                a0, a1, b0, b1 = then.get("gain_px"), now_row.get("gain_px"), then.get("lose_px"), now_row.get("lose_px")
                vs = "對照籃"
            else:
                a0, a1 = then.get("gain_px"), now_row.get("gain_px")
                b0, b1 = hist["rows"][d0].get("_spy_px"), row.get("_spy_px")
                vs = "SPY"
            if None in (a0, a1, b0, b1):
                continue
            diff = round(((a1 / a0) - (b1 / b0)) * 100, 1)
            review.append({"id": f["id"], "q": f["q"], "days": days, "date": d0, "lean_then": then["lean"],
                           "diff": diff, "vs": vs, "alarm_then": then.get("alarm")})
    first_review = str(parse_date(first_day) + timedelta(days=30))

    out = {
        "schema": "horizon-v1",
        "as_of": str(TODAY),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "history_since": first_day,
        "top": top,
        "far": far,
        "strategy": strategy,
        "bets": bets,
        "no_series": link_info.get("no_series", []),
        "blind_spots": blind[:8],
        "blind_total": len(blind),
        "threads_active": n_active,
        "stress": stress,
        "review": review,
        "first_review": first_review,
        "risks": risks,
        "upcoming": upcoming,
        "fires_out": fires_out,
        "fires_co": fires_co,
        "triggers": triggers,
        "depts": depts,
        "conflicts": conflicts,
        "market_headline": state.get("read_headline"),
        "market_read_as_of": state.get("read_as_of"),
        "seats": {"core": seats_core, "sat": seats_sat, "date": snap.get("date")},
        "tlinks": {t: tlink(t) for t in sorted(set(seats) | set(basket_t) | {x for q in questions
                   for x in (q.get("related") or {}).get("tickers", [])}) if tlink(t)},
        "gaps": gaps,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "horizon.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    hist_path.write_text(json.dumps(hist, ensure_ascii=False, indent=1), encoding="utf-8")
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"horizon: {len(far)} 題、{len(upcoming)} 件 60 天內、{len(fires_out) + len(fires_co)} 件今天、"
          f"今天先看 {len(top)} 件、gaps {len(gaps)}")


if __name__ == "__main__":
    main()
