"""美債 3～5 年展望與債券腿選擇（/ideas/bond-outlook.html）的數據。

兩段：
1. `python3.12 docs/ideas/data/bond-outlook/data.py --from-v7`（只在本機跑）：
   從 ~/v7-backtest 讀長歷史計算結果（results/bond_outlook/summary.json）與重建的債券總報酬指數
   （data/bond_outlook/bond_tri.csv），抽出頁面要用的欄位，寫成同目錄的 v7_extract.json。
   網站 CI 讀不到 v7，所以抽出來的檔案進 repo，當靜態來源。
   累積超額報酬曲線由 bond_tri.csv 照 v7 同一套三條件重算，算完與 summary.json 的全期累積
   超額報酬、最大跌幅比對，不一致就停下。
2. `python3.12 docs/ideas/data/bond-outlook/data.py`：讀 v7_extract.json，加上頁面資料區的兩個
   量表（靜態值，標資料日），寫出 data.json。頁面的圖表讀 data.json。

長歷史方法（v7 src/bond_outlook，2026-10-18 跑結果之前定死）：FRED 殖利率重建 10 年期平價債，
每月換新債、每天重新定價；超額報酬＝債券日報酬減 3 個月國庫券日報酬。條件式＝債券總報酬指數的
週線三條件（週收盤 > 40 週均線、> 52 週均線、> 52 週前收盤，嚴格大於），每成立一條持有三分之一，
週五收盤的計數管下一個交易日到下週五。不含交易成本。這是描述，不是事前登記的檢驗。
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTRACT = HERE / "v7_extract.json"
OUT = HERE / "data.json"
V7 = Path.home() / "v7-backtest"

# 美股 13 次跌 15% 以上（創高重置法）的中文標籤，順序同 summary.json extra.A rows（略過 1962 不可計）
EVENT_LABELS = {
    "1966-02-09": "1966", "1968-11-29": "1968～70", "1973-01-11": "1973～74",
    "1980-11-28": "1980～82", "1987-08-25": "1987", "1990-07-16": "1990",
    "1998-07-17": "1998", "2000-03-24": "2000～02", "2007-10-09": "2007～09",
    "2018-09-20": "2018", "2020-02-19": "2020", "2022-01-03": "2022", "2025-02-19": "2025",
}

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


def extract_from_v7():
    import numpy as np
    import pandas as pd

    summary = json.loads((V7 / "results/bond_outlook/summary.json").read_text())
    tb = pd.read_csv(V7 / "data/bond_outlook/bond_tri.csv", index_col=0, parse_dates=True)

    # ── 條件式持有：與 v7 src/bond_outlook/signals.py 同一套規則 ──
    tri = tb["tri_10y"]
    wk = tri.resample("W-FRI").last()
    if wk.isna().any():
        raise SystemExit("週線出現空週")
    x = wk.values.astype(float)
    ma40 = wk.rolling(40).mean().values
    ma52 = wk.rolling(52).mean().values
    cnt = np.full(len(x), -1, dtype=int)
    for i in range(52, len(x)):
        cnt[i] = int(x[i] > ma40[i]) + int(x[i] > ma52[i]) + int(x[i] > x[i - 52])
    prev = np.concatenate([[-1], cnt[:-1]])
    pos = wk.index.searchsorted(tb.index, side="left")
    held = np.where(prev[pos] >= 0, prev[pos], 0)

    bond = tb["ret_10y"].values
    cash = tb["ret_cash"].values
    cond_ex = held * (bond - cash) / 3.0
    hold_ex = bond - cash

    # 全期窗口：基準日 1962-12-31（1963-01-01 之前最後一個交易日），到資料最後一天
    full = [r for r in summary["decades"] if r["label"].startswith("全期")][0]["bonds"]["10y"]
    i0 = tb.index.searchsorted(pd.Timestamp(full["base_date"]), side="right") - 1
    dates = tb.index[i0:]

    def curve(ex):
        r = np.nan_to_num(ex[i0 + 1:])
        c = np.concatenate([[1.0], np.cumprod(1.0 + r)])
        return pd.Series(c, index=dates)

    out_curves = {}
    for key, ex in (("cond", cond_ex), ("hold", hold_ex)):
        c = curve(ex)
        cum = float(c.iloc[-1] - 1.0)
        mdd = float((c / c.cummax() - 1.0).min())
        want_cum, want_mdd = full[key]["excess_cum"], full[key]["excess_mdd"]
        if abs(cum - want_cum) > 1e-6 or abs(mdd - want_mdd) > 1e-6:
            raise SystemExit(f"{key} 曲線與 summary.json 不一致：累積 {cum} 對 {want_cum}，最大跌幅 {mdd} 對 {want_mdd}")
        m = c.resample("ME").last()
        out_curves[key] = [round((v - 1.0) * 100, 2) for v in m.values]
        out_curves["dates"] = [d.strftime("%Y-%m") for d in m.index]

    events = []
    for row in summary["extra"]["A"]["rows"]:
        if not row.get("usable"):
            continue
        leg = row["legs"]["10y"]
        events.append({
            "label": EVENT_LABELS[row["peak_date"]],
            "peak_date": row["peak_date"], "trough_date": row["trough_date"],
            "spx_drawdown": round(row["drawdown"] * 100, 1),
            "score_week": leg["score_week"],
            "cond_10y": round(leg["cond_excess"] * 100, 1),
            "hold_10y": round(leg["hold_excess"] * 100, 1),
            "cond_20y": round(row["legs"]["20y"]["cond_excess"] * 100, 1),
        })
    if len(events) != 13:
        raise SystemExit(f"事件數 {len(events)} 不是 13")
    avg = summary["extra"]["A"]["average"]["10y"]

    extract = {
        "source": "v7-backtest results/bond_outlook/summary.json＋data/bond_outlook/bond_tri.csv",
        "generated": summary["meta"]["generated"],
        "bond_data_last": summary["meta"]["last"],
        "spx_last": summary["meta"]["spx_last"],
        "events": events,
        "events_average": {
            "cond_mean": round(avg["cond_mean"] * 100, 1), "cond_median": round(avg["cond_median"] * 100, 1),
            "hold_mean": round(avg["hold_mean"] * 100, 1), "hold_median": round(avg["hold_median"] * 100, 1),
            "cond_positive": avg["cond_positive"], "n": avg["n"],
        },
        "full_period": {
            "base_date": full["base_date"], "end_date": full["end_date"],
            "cond": {"excess_ann": round(full["cond"]["excess_ann"] * 100, 2),
                     "excess_cum": round(full["cond"]["excess_cum"] * 100, 1),
                     "excess_mdd": round(full["cond"]["excess_mdd"] * 100, 1)},
            "hold": {"excess_ann": round(full["hold"]["excess_ann"] * 100, 2),
                     "excess_cum": round(full["hold"]["excess_cum"] * 100, 1),
                     "excess_mdd": round(full["hold"]["excess_mdd"] * 100, 1)},
        },
        "curve_monthly": out_curves,
    }
    EXTRACT.write_text(json.dumps(extract, ensure_ascii=False, indent=1) + "\n")
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
    if "--from-v7" in sys.argv:
        extract_from_v7()
    build()
