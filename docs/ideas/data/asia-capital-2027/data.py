"""亞洲資金與 1997（/ideas/asia-capital-2027.html）圖表用的數據。

重跑：python3.12 docs/ideas/data/asia-capital-2027/data.py
輸出：同目錄 data.json。頁面只讀這份 json 畫圖與填數字，前端不計算。
每個美股交易日由 .github/workflows/daily-us-close.yml 跑一次。

每次執行重算：
- markets：台股加權指數、南韓 KOSPI 自 2025 年最後一個交易日起的指數化路徑（=100）、
  外資買賣超累計（台股億元、韓股兆韓元）、融資餘額（台股上市億元、韓股合計兆韓元）。
  讀 repo 內 data/tw_chips/{taiex,inst,margin,mktcap}.jsonl 與 data/kr_chips/{kospi,inst_kospi,credit}.jsonl
  （由 tw-chips-daily.yml、kr-chips-daily.yml 每日更新，欄位與單位見各資料夾 README.md）。
  台股外資＝inst.jsonl 的 f[0]−f[1]（元）；韓股外資＝inst_kospi.jsonl 的 f（億韓元）。
  融資：台股 margin.jsonl 的 mga（仟元，今日餘額）；韓股 credit.jsonl 的 tot（百萬韓元）。
  融資占市值：台股上市融資÷上市總市值週報（mktcap.jsonl，億元）；韓股 credit.jsonl 的 kospi÷kospi.jsonl 的 mcap（皆百萬韓元）。
- gap52：兩個指數的週五收盤距 52 週均線 %（最近 52 個週五收盤平均，含當週），2026 年起。
- latest：實盤六檔（QQQ、SMH、0050、2330、IEF、GLD）的收盤與週線條件，yfinance 還原權息。
  股票四檔：52 週均線與距離；IEF、GLD：40 週均線、52 週均線、52 週前收盤三條件各算一次。
任何一塊抓不到：該塊保留 data.json 上一版並標 stale: true，程式照常 exit 0。

不重算、照舊寫入（常數在本檔）：
- SEC：四大雲、Oracle、CoreWeave 近四季營運現金流與資本支出、長期負債一年前與最新（SEC XBRL companyfacts，
  2026-10-20 下載，副本在 ~/v7-backtest/data/edgar/facts/）；Nvidia 應收帳款與季營收。
- base_rates：同目錄 base_rate_events.csv（25 個歷史事件，定義見頁面「拋物線行情之後」一節；
  2026-10-20 以 v7-backtest price_store 價格指數算出，不含息）。
"""
import csv
import json
import sys
import time
import datetime as dt
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
OUT = HERE / "data.json"
ROOT = HERE.parents[3]
TW = ROOT / "data" / "tw_chips"
KR = ROOT / "data" / "kr_chips"
EVENTS_CSV = HERE / "base_rate_events.csv"

BASE_YEAR_END = "2025-12-31"   # 指數化基期：2025 年最後一個交易日（含）之前的最後收盤
START = "2026-01-01"
PRICE_START = "2024-09-01"     # 52 週均線＋52 週前收盤要一年多的週線
STOCKS = [("QQQ", "QQQ"), ("SMH", "SMH"), ("0050.TW", "0050"), ("2330.TW", "2330")]
LEGS = [("IEF", "IEF"), ("GLD", "GLD")]

# SEC XBRL companyfacts（10-K／10-Q），單位十億美元；近四季＝最新年報＋本年累計−去年同期累計。
# 資本支出＝PaymentsToAcquirePropertyPlantAndEquipment（Amazon 用 PaymentsToAcquireProductiveAssets），不含融資租賃。
# 長期負債取 LongTermDebt／LongTermDebtNoncurrent／DebtInstrumentCarryingAmount 中最新一期有值者；一年前取同一概念。
SEC = {
    "asof": "2026-10-20",
    "note": "資本支出不含融資租賃；Microsoft、Amazon 的融資租賃金額大，實際支出高於表列。",
    "rows": [
        {"name": "Oracle", "period": "2026-08-31", "ocf": 46.9, "capex": 75.7, "debt_prev": 92.9, "debt_prev_date": "2025-05-31", "debt": 130.1, "debt_date": "2026-05-31"},
        {"name": "Amazon", "period": "2026-06-30", "ocf": 161.4, "capex": 173.0, "debt_prev": 56.1, "debt_prev_date": "2025-06-30", "debt": 133.0, "debt_date": "2026-06-30"},
        {"name": "Alphabet", "period": "2026-06-30", "ocf": 185.7, "capex": 132.4, "debt_prev": 23.6, "debt_prev_date": "2025-06-30", "debt": 98.2, "debt_date": "2026-06-30"},
        {"name": "Meta", "period": "2026-06-30", "ocf": 130.3, "capex": 89.3, "debt_prev": 28.8, "debt_prev_date": "2025-06-30", "debt": 83.7, "debt_date": "2026-06-30"},
        {"name": "Microsoft", "period": "2026-06-30", "ocf": 182.9, "capex": 115.9, "debt_prev": 43.2, "debt_prev_date": "2025-06-30", "debt": 40.3, "debt_date": "2026-06-30"},
        {"name": "CoreWeave", "period": "2026-06-30", "ocf": 6.9, "capex": 20.6, "debt_prev": 11.2, "debt_prev_date": "2025-06-30", "debt": 35.6, "debt_date": "2026-06-30"},
    ],
    "nvidia": {"ar_prev": 40.7, "ar": 63.1, "rev_prev": 81.6, "rev": 96.2, "q_prev": "2026-04-26", "q": "2026-07-26"},
}


def r(x, n=2):
    return round(float(x), n)


def _ymd(ts):
    return pd.Timestamp(ts).strftime("%Y-%m-%d")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def series(rows, fn):
    s = pd.Series({pd.Timestamp(x["d"]): fn(x) for x in rows})
    return s.sort_index().dropna()


def market(close, fnet, margin, scale_f, scale_m):
    """close／fnet／margin 都是日頻 Series。回傳 2026 年起的日序列與摘要。"""
    base = close.loc[:BASE_YEAR_END]
    if base.empty:
        raise ValueError("缺 2025 年底收盤")
    b = float(base.iloc[-1])
    c = close.loc[START:]
    if c.empty:
        raise ValueError("2026 年沒有收盤")
    idx = c / b * 100
    f = fnet.loc[START:].reindex(c.index).fillna(0) / scale_f
    fcum = f.cumsum()
    m_all = margin / scale_m
    mb = m_all.loc[:BASE_YEAR_END]
    m = m_all.loc[START:].reindex(c.index).ffill()
    hi_d = c.idxmax()
    m_hi_d = m.idxmax()
    pre = float(f.loc[:hi_d].sum())
    post = float(f.loc[hi_d:].iloc[1:].sum())
    return {
        "dates": [_ymd(x) for x in c.index],
        "idx": [r(v, 1) for v in idx.values],
        "close": [r(v, 2) for v in c.values],
        "fcum": [r(v, 2) for v in fcum.values],
        "margin": [None if pd.isna(v) else r(v, 2) for v in m.values],
        "summary": {
            "base_close": r(b), "last_date": _ymd(c.index[-1]), "last_close": r(c.iloc[-1]),
            "high_date": _ymd(hi_d), "high_close": r(c.max()),
            "pct_from_high": r((c.iloc[-1] / c.max() - 1) * 100, 1),
            "pct_ytd": r((c.iloc[-1] / b - 1) * 100, 1),
            "foreign_ytd": r(fcum.iloc[-1], 1),
            "foreign_pre_high": r(pre, 1), "foreign_post_high": r(post, 1),
            "foreign_min_day": r(f.min(), 1), "foreign_min_day_date": _ymd(f.idxmin()),
            "margin_base": r(mb.iloc[-1], 2) if not mb.empty else None,
            "margin_last": r(m.dropna().iloc[-1], 2), "margin_high": r(m.max(), 2), "margin_high_date": _ymd(m_hi_d),
            "margin_from_high_pct": r((m.dropna().iloc[-1] / m.max() - 1) * 100, 1),
        },
    }


def gap52(close):
    w = close.resample("W-FRI").last().dropna()
    ma = w.rolling(52).mean()
    g = ((w / ma - 1) * 100).loc[START:].dropna()
    return {"dates": [_ymd(x) for x in g.index], "gap": [r(v, 1) for v in g.values]}


def calc_markets():
    tw_close = series(read_jsonl(TW / "taiex.jsonl"), lambda x: x.get("c"))
    tw_f = series(read_jsonl(TW / "inst.jsonl"), lambda x: (x["f"][0] - x["f"][1]) if x.get("f") else None)
    tw_m = series(read_jsonl(TW / "margin.jsonl"), lambda x: x.get("mga"))
    kr_close = series(read_jsonl(KR / "kospi.jsonl"), lambda x: x.get("c"))
    kr_f = series(read_jsonl(KR / "inst_kospi.jsonl"), lambda x: x.get("f"))
    kr_m = series(read_jsonl(KR / "credit.jsonl"), lambda x: x.get("tot"))
    tw = market(tw_close, tw_f, tw_m, 1e8, 1e5)        # 元→億元；仟元→億元
    kr = market(kr_close, kr_f, kr_m, 1e4, 1e6)        # 億韓元→兆韓元；百萬韓元→兆韓元
    # 融資占市值：台股＝上市融資（億元）÷ 上市總市值週報（億元）；韓股＝KOSPI 融資（百萬韓元）÷ KOSPI 市值（百萬韓元）
    tw_cap = series(read_jsonl(TW / "mktcap.jsonl"), lambda x: x.get("cap"))
    tw_ratio = ((tw_m / 1e5).resample("W-FRI").last() / tw_cap.resample("W-FRI").last() * 100).dropna()
    kr_ratio = (series(read_jsonl(KR / "credit.jsonl"), lambda x: x.get("kospi"))
                / series(read_jsonl(KR / "kospi.jsonl"), lambda x: x.get("mcap")) * 100).dropna()
    for mk, rt in ((tw, tw_ratio), (kr, kr_ratio)):
        mk["summary"]["margin_cap_pct"] = r(rt.iloc[-1], 2)
        mk["summary"]["margin_cap_date"] = _ymd(rt.index[-1])
    tw["unit"] = {"foreign": "億元", "margin": "億元（上市融資餘額）"}
    kr["unit"] = {"foreign": "兆韓元", "margin": "兆韓元（融資餘額合計）"}
    last = min(tw["summary"]["last_date"], kr["summary"]["last_date"])
    return {"tw": tw, "kr": kr, "gap52": {"tw": gap52(tw_close), "kr": gap52(kr_close)},
            "last_date": max(tw["summary"]["last_date"], kr["summary"]["last_date"]), "common_date": last}


def fetch_prices(symbols, start=PRICE_START, tries=3):
    import yfinance as yf
    last = None
    for i in range(tries):
        try:
            df = yf.download(list(symbols), start=start, auto_adjust=True, progress=False, threads=False)["Close"]
            if isinstance(df, pd.Series):
                df = df.to_frame(list(symbols)[0])
            df = df.dropna(how="all")
            if not df.empty:
                return df
            last = "empty"
        except Exception as e:  # noqa: BLE001
            last = str(e)[:100]
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"yfinance 抓不到：{last}")


def calc_latest(df):
    out = {"ma_rule": "週五收盤最近 N 筆平均（含本週最新收盤）；above_pct＝(收盤／均線−1)×100，drop_pct＝(1−均線／收盤)×100",
           "stocks": [], "legs": []}
    dates = []
    for sym, label in STOCKS + LEGS:
        if sym not in df.columns:
            raise ValueError(f"缺少 {sym}")
        s = df[sym].dropna()
        w = s.resample("W-FRI").last().dropna()
        if len(w) < 53:
            raise ValueError(f"{sym} 週收盤不足 53 筆")
        close = float(s.iloc[-1])
        ma52 = float(w.iloc[-52:].mean())
        row = {"ticker": label, "date": _ymd(s.index[-1]), "close": r(close), "ma52": r(ma52),
               "above_pct": r((close / ma52 - 1) * 100, 1), "drop_pct": r((1 - ma52 / close) * 100, 1)}
        dates.append(row["date"])
        if (sym, label) in STOCKS:
            hi = float(s.loc[START:].max())
            row["high_2026"] = r(hi)
            row["ma_from_high_pct"] = r((ma52 / hi - 1) * 100, 1)
            out["stocks"].append(row)
        else:
            ma40 = float(w.iloc[-40:].mean())
            prev52 = float(w.iloc[-53])
            conds = [close > ma40, close > ma52, close > prev52]
            row.update({"ma40": r(ma40), "prev52": r(prev52), "conds": conds, "n_pass": sum(conds),
                        "weight_pct": r(sum(conds) / 3 * 20, 1)})
            out["legs"].append(row)
    out["date"] = max(dates)
    return out


def load_events():
    rows = []
    with open(EVENTS_CSV, encoding="utf-8") as f:
        for x in csv.DictReader(f):
            def num(k):
                v = x.get(k, "")
                return None if v in ("", "nan", "None") else float(v)
            rows.append({"idx": x["idx"], "peak": x["peak"], "pre1y": num("pre1y"), "mdd": num("mdd"),
                         "r1": num("r1"), "r3": num("r3"), "r5": num("r5"), "r10": num("r10"),
                         "recov": num("recov"), "exit_dd": num("exit_dd"), "rule5": num("rule5"), "bh5": num("bh5")})
    return rows


def summarize(rows):
    def med(k, rs):
        v = sorted(x[k] for x in rs if x[k] is not None)
        if not v:
            return None
        n = len(v)
        return r((v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2) * 100, 1)

    def pos(k, rs):
        v = [x[k] for x in rs if x[k] is not None]
        return r(sum(1 for t in v if t > 0) / len(v) * 100, 0) if v else None

    ex = [x for x in rows if not x["peak"].startswith("2000")]
    out = {}
    for name, rs in (("all", rows), ("ex2000", ex)):
        out[name] = {"n": len(rs), "horizons": [
            {"h": h, "median": med(k, rs), "pos": pos(k, rs)} for h, k in (("1 年", "r1"), ("3 年", "r3"), ("5 年", "r5"), ("10 年", "r10"))],
            "exit_dd_median": med("exit_dd", rs), "rule5_median": med("rule5", rs), "bh5_median": med("bh5", rs),
            "rule_wins": sum(1 for x in rs if x["rule5"] is not None and x["bh5"] is not None and x["rule5"] > x["bh5"])}
    return out


def load_old():
    try:
        return json.loads(OUT.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def build(old, fetch=fetch_prices):
    old = old or {}

    def block(name, fn):
        try:
            res = fn()
            prev = (old.get(name) or {}).get("last_date") or (old.get(name) or {}).get("date")
            cur = res.get("last_date") or res.get("date")
            if prev and cur and cur < prev:
                raise ValueError(f"新資料日 {cur} 早於上一版 {prev}")
            res["stale"] = False
            return res
        except Exception as e:  # noqa: BLE001
            print(f"{name} 沿用上一版（stale）：", str(e)[:160])
            if name in old:
                return {**old[name], "stale": True}
            return None

    out = {}
    m = block("markets", calc_markets)
    if m is not None:
        out["markets"] = m
    lt = block("latest", lambda: calc_latest(fetch([s for s, _ in STOCKS + LEGS])))
    if lt is not None:
        out["latest"] = lt
    events = load_events()
    done = [x for x in events if x["peak"] < "2026-01-01"]       # 2026 年的事件還在進行中，不進統計
    out["base_rates"] = {"events": done, "ongoing": [x for x in events if x["peak"] >= "2026-01-01"],
                         "summary": summarize(done),
                         "definition": "252 個交易日內漲 ≥80% 之後 126 個交易日內的最高收盤為高點，從高點回撤 ≥30% 才算事件；價格指數，不含息"}
    out["sec"] = SEC
    out["stale"] = any((out.get(n) or {"stale": True}).get("stale", True) for n in ("markets", "latest"))
    return out


def main():
    old = load_old()
    out = build(old)
    out["generated"] = dt.date.today().isoformat()
    if old and {k: v for k, v in old.items() if k != "generated"} == {k: v for k, v in out.items() if k != "generated"}:
        out["generated"] = old.get("generated", out["generated"])
    out = {"generated": out.pop("generated"), **out}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("寫入", OUT, OUT.stat().st_size, "bytes", "（有 stale 區塊）" if out["stale"] else "")
    if "markets" in out:
        for k in ("tw", "kr"):
            print(k, json.dumps(out["markets"][k]["summary"], ensure_ascii=False))
    if "latest" in out:
        for x in out["latest"]["stocks"] + out["latest"]["legs"]:
            print(json.dumps(x, ensure_ascii=False))
    print(json.dumps(out["base_rates"]["summary"], ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001  CI 不要因為這支變紅；上一版 data.json 原封不動
        print("data.py 失敗，data.json 未更新：", str(e)[:200])
        sys.exit(0)
