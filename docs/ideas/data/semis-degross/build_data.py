"""半導體去槓桿想法頁（/ideas/semis-degross.html）的圖表資料。

重跑：python3 -I docs/ideas/data/semis-degross/build_data.py
輸出：同目錄 data.json。頁面只讀這份 json 畫圖，前端不計算。
只用標準函式庫、不抓網路。CSV 由 v7-backtest 的 src/semis_degross/build_dataset.py 產生並複製到這裡，
正本在 ~/v7-backtest/data/semis_degross_2026/。

CSV 對應：
- prices_daily.csv：指數與 17 檔日收盤（Yahoo 還原收盤），畫布 c1。
- drawdown_table.csv：截至 10/30 各檔離 52 週高、均線距離，畫布 c2 與表 T1。
- breadth_daily.csv：SMH 成分股（24 檔，缺 SK 海力士）站上 50／200 日線比例，畫布 c3。
- degross_events.csv、episode_environment.csv：大摩去槓桿六次＋這次，畫布 c4、c12 與表 T2、T5。
- control_months.csv：對照組基準率，表 T3。
- sox_dd_events_52w.csv、sox_dd_paths_52w.csv：SOX 離 52 週高跌 25% 的 13 段，畫布 c5、c6 與表 T4。
- sox_bigdown_days.csv：SOX 單日跌 6% 以上的 59 次，畫布 c7。
- sox_forward_pe_weekly.csv：費城半導體預估本益比週資料 2002 起（etf-dash 的長期序列），畫布 c8。
- smh_eps_index_daily.csv、smh_eps_vs_price_periods.csv、smh_forward_summary.json：SMH 加權預估 EPS 對價格，畫布 c9。
- smh_constituents_revisions.csv：25 檔成分股預估 EPS 修正，畫布 c10 與表 T9。
- etf_flows_daily.csv、etf_flows_monthly.csv：SMH、SOXX、QQQ 流通單位數推算的資金流，畫布 c11。
- positioning_secondhand.csv、events_oct2026.csv、credit_oct2026.csv：研究整理的二手資料，表 T6～T8（正文直接引用，不進圖）。
"""
import csv
import json
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "data.json"
ASOF = "2026-10-30"
SRC_PX = "共用價格庫（Yahoo 還原收盤）"


def read(name):
    with open(HERE / name, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def num(s):
    s = (s or "").strip()
    if s in ("", "None", "nan", "NaN"):
        return None
    return float(s)


def r1(v):
    return None if v is None else round(v, 1)


def r2(v):
    return None if v is None else round(v, 2)


def main():
    D = {"asof": ASOF, "generated_for": "/ideas/semis-degross.html"}

    # c1：2026 年各指數離 52 週高（日）
    px = read("prices_daily.csv")
    cols = ["^SOX", "SMH", "QQQ", "^GSPC"]
    hist = {c: [] for c in cols}
    series = {c: [] for c in cols}
    for row in px:
        d = row["date"]
        for c in cols:
            v = num(row[c])
            if v is None:
                continue
            hist[c].append(v)
            if d >= "2026-01-01":
                hi = max(hist[c][-252:])
                series[c].append([d, round((v / hi - 1) * 100, 2)])
    D["c1"] = {"series": series, "labels": {"^SOX": "費城半導體", "SMH": "SMH", "QQQ": "QQQ", "^GSPC": "S&P 500"},
               "marks": [["2026-06-22", "半導體高點"], ["2026-07-29", "7 月低點"], ["2026-10-06", "S&P 高點"], ["2026-10-30", "10/30"]],
               "source": SRC_PX, "asof": ASOF}

    # c2＋T1：跌幅表
    dt = read("drawdown_table.csv")
    names = {"^SOX": "費城半導體", "^GSPC": "S&P 500"}
    rows = []
    for r in dt:
        rows.append({"ticker": names.get(r["ticker"], r["ticker"]), "off_high": num(r["off_high_pct"]), "high_date": r["high_date"],
                     "d1": num(r["d1_pct"]), "w1": num(r["w1_pct"]), "m1": num(r["m1_pct"]), "ytd": num(r["ytd_pct"]),
                     "vs50": num(r["vs_ma50_pct"]), "vs200": num(r["vs_ma200_pct"]),
                     "above_low": num(r["above_low_since_jun_pct"]), "low_date": r["low_since_jun_date"]})
    D["c2"] = {"rows": rows, "source": SRC_PX, "asof": ASOF}

    # c3：寬度（週五取樣）
    br = read("breadth_daily.csv")
    wk = []
    last_week = None
    for r in br:
        d = date.fromisoformat(r["date"])
        key = (d.isocalendar()[0], d.isocalendar()[1])
        if key != last_week and wk:
            pass
        wk.append([r["date"], num(r["pct_above_ma50"]), num(r["pct_above_ma200"]), num(r["pct_down_25_from_52w_high"]), int(float(r["n"]))])
        last_week = key
    # 每週留最後一天，最後一天一定留
    keep = []
    for i, w in enumerate(wk):
        d = date.fromisoformat(w[0])
        nxt = date.fromisoformat(wk[i + 1][0]) if i + 1 < len(wk) else None
        if nxt is None or nxt.isocalendar()[1] != d.isocalendar()[1]:
            keep.append(w)
    D["c3"] = {"weekly": keep, "note": "SMH 25 檔成分股，缺 SK 海力士（美股沒有日線），2018 年起 22～24 檔有 200 日線",
               "source": SRC_PX + "；成分與權重來自 etf-dash（VanEck 持股表）", "asof": ASOF}

    # c4＋T2＋T5：去槓桿事件
    dg = read("degross_events.csv")
    env = {r["event"]: r for r in read("episode_environment.csv")}
    ev = []
    for r in dg:
        e = env.get("degross " + r["month"], {})
        ev.append({"month": r["month"], "trough": num(r["degross_trough_pct"]),
                   "spx_low_date": r.get("spx_month_low_date"), "sox_off52": num(e.get("sox_off_52w_high_pct")),
                   "spx_off52": num(e.get("spx_off_52w_high_pct")),
                   "spx_fwd1m": num(r.get("spx_fwd_1m_pct")), "spx_fwd3m": num(r.get("spx_fwd_3m_pct")), "spx_worst4w": num(r.get("spx_worst_next_4w_pct")),
                   "sox_fwd1m": num(r.get("sox_fwd_1m_pct")), "sox_fwd3m": num(r.get("sox_fwd_3m_pct")), "sox_worst4w": num(r.get("sox_worst_next_4w_pct")),
                   "sox_broke_low": r.get("sox_broke_month_low_90d"), "spx_broke_low": r.get("spx_broke_month_low_90d"),
                   "sox_pe": num(e.get("sox_fwd_pe")), "us10y": num(e.get("us10y")), "vix": num(e.get("vix")),
                   "baa10y": num(e.get("baa10y")), "fedfunds": num(e.get("fedfunds")), "ff_chg6m": num(e.get("fedfunds_chg_6m"))})
    D["c4"] = {"events": ev, "source": "去槓桿月份與谷底讀數：Morgan Stanley Prime Brokerage 圖（Steno Research 按月數位化，二手）；價格：" + SRC_PX + "；利率與利差：FRED", "asof": ASOF}

    # T3：對照組
    ctrl = read("control_months.csv")
    def stats(rows, key):
        vals = sorted(num(r[key]) for r in rows if num(r[key]) is not None)
        if not vals:
            return None
        med = vals[len(vals) // 2] if len(vals) % 2 else (vals[len(vals) // 2 - 1] + vals[len(vals) // 2]) / 2
        return {"n": len(vals), "median": round(med, 1), "pos_pct": round(sum(v > 0 for v in vals) / len(vals) * 100), "le_minus5_pct": round(sum(v <= -5 for v in vals) / len(vals) * 100)}
    T3 = {}
    for idx in ("spx", "sox"):
        rows = [r for r in ctrl if r["index"] == idx]
        T3[idx] = {k: stats(rows, k) for k in ("worst_next_4w_pct", "fwd_1m_pct", "fwd_3m_pct")}
        T3[idx]["threshold"] = "離高點 ≥3%" if idx == "spx" else "離高點 ≥10%"
    # 六次事件（不含這次）的中位
    past = [r for r in dg if r["month"] != "2026-10"]
    T3["degross_spx"] = {k: stats(past, "spx_" + k) for k in ("worst_next_4w_pct", "fwd_1m_pct", "fwd_3m_pct")}
    T3["degross_sox"] = {k: stats(past, "sox_" + k) for k in ("worst_next_4w_pct", "fwd_1m_pct", "fwd_3m_pct")}
    D["t3"] = T3

    # c5＋c6＋T4：SOX 跌 25% 事件
    evs = read("sox_dd_events_52w.csv")
    D["c6"] = {"events": [{"peak_date": r["peak_date"], "first25": r["first_25_date"], "trough_date": r["trough_date"],
                           "depth": num(r["depth_pct"]), "fall_after_25": num(r["fall_after_25_pct"]),
                           "days_25_to_trough": int(float(r["days_25_to_trough"])), "days_peak_to_trough": int(float(r["days_peak_to_trough"])),
                           "end_date": r["end_date"] or None, "ongoing": r["ongoing"] == "True",
                           "fwd1m": num(r["fwd_1m_from_25_pct"]), "fwd3m": num(r["fwd_3m_from_25_pct"]),
                           "fwd6m": num(r["fwd_6m_from_25_pct"]), "fwd12m": num(r["fwd_12m_from_25_pct"]),
                           "env": env.get("sox25 " + r["peak_date"], {})} for r in evs],
               "source": SRC_PX + "；事件定義：收盤離 252 日高點 25% 起算，回到 252 日新高結束", "asof": ASOF}
    for e in D["c6"]["events"]:
        e["env"] = {k: num(v) for k, v in e["env"].items() if k not in ("event", "date")}
    paths = read("sox_dd_paths_52w.csv")
    keys = [k for k in paths[0].keys() if k != "days_since_peak"]
    P = {k: [] for k in keys}
    for r in paths:
        for k in keys:
            v = num(r[k])
            if v is not None:
                P[k].append(round(v, 1))
    D["c5"] = {"paths": P, "current": "2026-06-22", "source": SRC_PX, "asof": ASOF}

    # c7：單日跌 6%
    bd = read("sox_bigdown_days.csv")
    D["c7"] = {"days": [{"date": r["date"], "day": num(r["day_pct"]), "off_peak": num(r["off_peak_pct"]), "worst20": num(r["worst_next_20d_pct"]),
                         "fwd1m": num(r["fwd_1m_pct"]), "fwd3m": num(r["fwd_3m_pct"])} for r in bd],
               "stats": {k: stats(bd, k) for k in ("worst_next_20d_pct", "fwd_1m_pct", "fwd_3m_pct")},
               "stats_deep": {k: stats([r for r in bd if num(r["off_peak_pct"]) <= -20], k) for k in ("worst_next_20d_pct", "fwd_1m_pct", "fwd_3m_pct")},
               "source": SRC_PX + "；1994 年起，同一事件 10 天內重複只算第一天", "asof": ASOF}

    # c8：預估本益比週資料
    pe = read("sox_forward_pe_weekly.csv")
    ser = [[r["date"], num(r["pe"])] for r in pe if num(r["pe"]) is not None]
    vals = sorted(v for _, v in ser)
    def q(p):
        return vals[min(len(vals) - 1, int(p * len(vals)))]
    D["c8"] = {"weekly": ser, "median": round(q(0.5), 1), "p10": round(q(0.1), 1), "p90": round(q(0.9), 1),
               "latest": ser[-1], "peak_2026": max((x for x in ser if x[0] >= "2026-01-01"), key=lambda x: x[1]),
               "troughs": [["2008-11-20", None], ["2011-08-19", None], ["2016-02-11", None], ["2018-12-24", None], ["2020-03-18", None], ["2022-10-14", None], ["2025-04-08", None]],
               "note": open(HERE / "sox_forward_pe_note.txt", encoding="utf-8").read().strip(),
               "source": "etf-dash 長期序列（費城半導體指數預估本益比，週）", "asof": ser[-1][0]}
    for t in D["c8"]["troughs"]:
        prior = [x for x in ser if x[0] <= t[0]]
        t[1] = prior[-1][1] if prior else None

    # c9：SMH 加權 EPS 對價格
    ei = read("smh_eps_index_daily.csv")
    k_eps = [k for k in ei[0].keys() if "eps" in k.lower()][0]
    k_px = [k for k in ei[0].keys() if "price" in k.lower() or "close" in k.lower()]
    k_px = k_px[0] if k_px else None
    base_e = num(ei[0][k_eps])
    base_p = num(ei[0][k_px]) if k_px else None
    D["c9"] = {"daily": [[r["date"], round(num(r[k_eps]) / base_e * 100, 2), round(num(r[k_px]) / base_p * 100, 2) if k_px and num(r[k_px]) else None] for r in ei if num(r[k_eps])],
               "periods": read("smh_eps_vs_price_periods.csv"),
               "summary": json.load(open(HERE / "smh_forward_summary.json", encoding="utf-8")),
               "source": "etf-dash（Yahoo 共識預估，成分股加權）", "asof": ei[-1]["date"]}
    if not k_px:
        # 沒有價格欄就用 SMH 收盤
        smh = {r["date"]: num(r["SMH"]) for r in px}
        b = None
        out = []
        for d, e, _ in D["c9"]["daily"]:
            v = smh.get(d)
            if v is not None and b is None:
                b = v
            out.append([d, e, round(v / b * 100, 2) if v is not None and b else None])
        D["c9"]["daily"] = out

    # c10＋T9：成分股修正
    cr = read("smh_constituents_revisions.csv")
    D["c10"] = {"rows": [{"ticker": r["ticker"], "name": r["name"], "w": num(r["weight_pct"]), "r30": num(r["rev_30d_pct"]), "r60": num(r["rev_60d_pct"]), "r90": num(r["rev_90d_pct"])} for r in cr],
                "source": "etf-dash（Yahoo 明年度共識 EPS，美元）", "asof": "2026-10-31"}

    # c11：ETF 資金流
    fm = read("etf_flows_monthly.csv")
    fd = read("etf_flows_daily.csv")
    monthly = {}
    for r in fm:
        monthly.setdefault(r["etf"], []).append([r["date"][:7], num(r["flow_usd_m"])])
    so = {}
    for r in fd:
        so.setdefault(r["etf"], []).append([r["date"][:10], num(r["shares_outstanding"]), num(r["flow_usd_m"])])
    D["c11"] = {"monthly": monthly, "daily": so, "source": "etf-dash（發行商每日流通單位數與淨值；資金流＝單位數變化 × 淨值）", "asof": fd[-1]["date"][:10]}

    # T6～T8：二手整理
    D["t6"] = read("positioning_secondhand.csv")
    D["t7"] = read("events_oct2026.csv")
    D["t8"] = read("credit_oct2026.csv")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(D, f, ensure_ascii=False, separators=(",", ":"))
    print("wrote", OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
