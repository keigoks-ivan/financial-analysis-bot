"""美債 3～5 年展望與債券腿選擇（/ideas/bond-outlook.html）的數據。

兩段：
1. `BACKTEST_DIR=<本機回測庫> python3.12 docs/ideas/data/bond-outlook/data.py --extract`（只在本機跑）：
   從本機回測庫（不公開）讀長歷史計算結果 results/bond_outlook/summary.json 與重建的債券總報酬指數
   data/bond_outlook/bond_tri.csv，抽出頁面要用的欄位，寫成同目錄的 history_extract.json。
   網站 CI 讀不到回測庫，所以抽出來的檔案進 repo，當靜態來源。
   2 年、10 年、20 年三條腿都由 bond_tri.csv 照同一套三條件重算，全期與 1994、2022 全年的累積
   超額報酬、最大跌幅和 summary.json 比對，不一致就停下。比對通過後，另算頁面引用的兩段債券
   熊市（高點到谷底）與 2019 年以來逐年的結果。
2. `python3.12 docs/ideas/data/bond-outlook/data.py`：讀 history_extract.json，加上頁面資料區的兩個
   量表（靜態值，標資料日），寫出 data.json。頁面的圖表讀 data.json。

長歷史方法（2026-10-18 跑結果之前定死）：FRED 殖利率重建平價債，每月換新債、每天重新定價；
超額報酬＝債券日報酬減 3 個月國庫券日報酬。條件式＝債券總報酬指數的週線三條件（週收盤 > 40 週
均線、> 52 週均線、> 52 週前收盤，嚴格大於），每成立一條持有三分之一，週五收盤的計數管下一個
交易日到下週五。不含交易成本。這是描述，不是事前登記的檢驗。
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "history_extract.json"
OUT = HERE / "data.json"

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

# 頁面資料區的兩個量表：靜態值，出處見頁面「資料型量表」一節。沒有排程更新。
GAUGES = [
    {"id": "spy_ief_corr60", "label": "60 日 SPY 對 IEF 日報酬相關係數", "value": 0.55, "unit": "",
     "asof": "2026-09-30", "zone": "red",
     "zones": {"green": "低於 −0.3", "yellow": "−0.3 到 +0.3", "red": "高於 +0.3"},
     "note": "還原日價自算；2026 年最高 +0.67（6 月 5 日），最低 −0.11（1 月 2 日）"},
    {"id": "t10y3m", "label": "10 年減 3 個月公債利差", "value": 1.00, "unit": "個百分點",
     "asof": "2026-10-15", "zone": "yellow",
     "zones": {"green": "2 個百分點以上", "yellow": "1～2 個百分點", "red": "1 個百分點以下"},
     "note": "FRED DGS10 5.10% 減 DTB3 4.10%；恰好在黃紅交界"},
]


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


def build():
    ex = json.loads(EXTRACT.read_text())
    data = {
        "page": "/ideas/bond-outlook.html",
        "history": ex,
        "gauges": GAUGES,
        "legs_status": {"asof": "2026-10-16", "ief": "0/3（9 月 4 日起連續七週）", "gold": "0/3",
                        "live_page": "/long-track-w52-adaptive/"},
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    print("寫出", OUT)


if __name__ == "__main__":
    if "--extract" in sys.argv:
        extract()
    build()
