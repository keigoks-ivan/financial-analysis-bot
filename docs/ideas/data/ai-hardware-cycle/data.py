"""AI 硬體循環（/ideas/ai-hardware-cycle.html）圖表用的數據。

重跑：python3.12 docs/ideas/data/ai-hardware-cycle/data.py
輸出：同目錄 data.json。頁面只讀這份 json 畫圖，前端不計算。

- 圖 1 費半高點後路徑：~/v7-backtest/data/semi_cycle_drawdowns/SOX.csv（date, close）；
  沒有這個檔（例如 CI）就退回 yfinance ^SOX。高點日取當日收盤。
- 圖 2 費半 12 個月遠期本益比：History of Market（CC BY 4.0）
  https://historyofmarket.com/api/sectors/forward-pe.json 的 sectors.sox。
  週頻 series 到 2026-08-05 為止；其後是同站 forwardOwn（日頻、自算混合遠期，與 series
  口徑相差 3% 以內），這裡取每週最後一筆接在後面，圖上用虛線區分。
  先抓網路，失敗退回本機快取（FPE_CACHE 環境變數或下面的預設路徑），再退回上一版 data.json。
- 圖 3～6：數字抄自頁面正文與表格，頁面沒有的點（圖 4 的中間點）註明出處。
"""
import json
import os
import datetime as dt
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).parent
OUT = HERE / "data.json"
SOX_CSV = Path.home() / "v7-backtest/data/semi_cycle_drawdowns/SOX.csv"
FPE_URL = "https://historyofmarket.com/api/sectors/forward-pe.json"
FPE_CACHE = Path(os.environ.get(
    "FPE_CACHE",
    "/private/tmp/claude-501/-Users-ivanchang/8ee9b8d9-b763-4a19-885a-b6791d31e39c/scratchpad/fpe.json"))

# 圖 1：高點日（依頁面「歷次高點之後的跌幅」表）。group：top 循環頂、digest 消化期、now 現在
PEAKS = [
    ("2000-03-10", "top"), ("2007-07-17", "top"), ("2021-12-27", "top"), ("2024-07-10", "top"),
    ("2015-06-01", "digest"), ("2018-03-12", "digest"), ("2020-02-19", "digest"),
    ("2026-06-22", "now"),
]
MAX_DAYS = 500


def r(x, n=2):
    return round(float(x), n)


def load_sox():
    if SOX_CSV.exists():
        df = pd.read_csv(SOX_CSV, parse_dates=["date"]).set_index("date")["close"]
        return df.dropna(), f"v7-backtest {SOX_CSV.name}"
    import yfinance as yf
    df = yf.download("^SOX", start="1994-01-01", auto_adjust=False, progress=False)["Close"]
    df = df.iloc[:, 0] if isinstance(df, pd.DataFrame) else df
    return df.dropna(), "yfinance ^SOX"


def drawdown_paths():
    close, src = load_sox()
    paths = []
    for d, grp in PEAKS:
        ts = pd.Timestamp(d)
        if ts not in close.index:
            raise SystemExit(f"高點日 {d} 不在費半收盤序列內")
        i = close.index.get_loc(ts)
        seg = close.iloc[i:i + MAX_DAYS + 1]
        # 第一次收盤回到（或高於）高點就截斷，最後一點記 0：圖只畫「跌幅」，不畫創新高之後的漲幅
        back = [k for k in range(1, len(seg)) if seg.iloc[k] >= seg.iloc[0]]
        if back:
            seg = seg.iloc[:back[0] + 1]
        pct = [r((v / seg.iloc[0] - 1) * 100, 1) for v in seg.values]
        if back:
            pct[-1] = 0.0
        paths.append({"peak": d, "group": grp, "peak_close": r(seg.iloc[0]),
                      "days": len(pct) - 1, "recovered": bool(back),
                      "last_date": seg.index[-1].strftime("%Y-%m-%d"),
                      "last_pct": pct[-1], "min_pct": min(pct), "path": pct})
    return {"source": src, "last_close_date": close.index[-1].strftime("%Y-%m-%d"), "paths": paths}


def load_fpe():
    try:
        resp = requests.get(FPE_URL, timeout=30)
        resp.raise_for_status()
        return resp.json(), "network"
    except Exception as e:  # noqa: BLE001
        print("fpe 網路失敗：", str(e)[:100])
    if FPE_CACHE.exists():
        return json.loads(FPE_CACHE.read_text()), "cache"
    return None, "none"


def forward_pe():
    raw, how = load_fpe()
    if raw is None:
        if OUT.exists():
            old = json.loads(OUT.read_text()).get("fpe")
            if old:
                print("fpe 沿用上一版 data.json")
                return old
        raise SystemExit("取不到遠期本益比，也沒有上一版可沿用")
    sox = raw["sectors"]["sox"]
    weekly = [(x["date"], x["value"]) for x in sox["series"] if x["date"] >= "2011-01-01"]
    last_w = weekly[-1][0]
    own = pd.Series({x["date"]: x["value"] for x in sox.get("forwardOwn", [])})
    own.index = pd.to_datetime(own.index)
    wk = own.groupby(own.index.to_period("W")).tail(1)  # 每週最後一筆
    ext = [(d.strftime("%Y-%m-%d"), float(v)) for d, v in wk.items() if d.strftime("%Y-%m-%d") > last_w]
    latest = sox.get("forwardOwnLatest") or {"date": weekly[-1][0], "value": weekly[-1][1]}
    if not ext or ext[-1][0] != latest["date"]:
        ext.append((latest["date"], float(latest["value"])))

    def pick(lo, hi, fn):
        rows = [(d, v) for d, v in weekly if lo <= d <= hi]
        return fn(rows, key=lambda t: t[1])

    marks = [
        {"key": "top2018", "label": "2018-03 頂", **dict(zip(("date", "value"), pick("2018-01-01", "2018-06-30", max)))},
        {"key": "top2021", "label": "2021-11 頂", **dict(zip(("date", "value"), pick("2021-09-01", "2021-12-31", max)))},
        {"key": "top2024", "label": "2024-06 頂", **dict(zip(("date", "value"), pick("2024-04-01", "2024-08-31", max)))},
        {"key": "top2026", "label": "2026-06 頂", **dict(zip(("date", "value"), pick("2026-05-01", "2026-07-31", max)))},
        {"key": "bot2018", "label": "2018-12 底", **dict(zip(("date", "value"), pick("2018-12-01", "2018-12-31", min)))},
        {"key": "bot2022", "label": "2022-10 底", **dict(zip(("date", "value"), pick("2022-08-01", "2022-12-31", min)))},
        {"key": "now", "label": "最新", "date": ext[-1][0], "value": ext[-1][1]},
    ]
    return {
        "source": "History of Market (historyofmarket.com), CC BY 4.0",
        "url": "https://historyofmarket.com/semi/semi-fwdpe/", "fetched_from": how,
        "api_updated": raw.get("updated"),
        "weekly": {"dates": [d for d, _ in weekly], "values": [r(v) for _, v in weekly]},
        "extension": {"dates": [d for d, _ in ext], "values": [r(v) for _, v in ext],
                      "note": "weekly 到 " + last_w + " 為止；其後為 forwardOwn（日頻、自算混合遠期）取每週最後一筆"},
        "marks": [{**m, "value": r(m["value"])} for m in marks],
    }


# 圖 3：Nvidia 10-Q（億美元）。頁面正文：供應與產能承諾 1,190 → 2,790；存貨 214.0（年初）→ 315.75（季末）；
# 保證 1,050 + AI 雲夥伴 35 = 1,085；AI 雲協議 360；股權投資 250。
# FQ1（2026-04-26）存貨 258.0 不在頁面正文，取自 SEC companyfacts InventoryNet = 25,797 百萬美元。
NVIDIA = {
    "unit": "億美元",
    "periods": ["FY26 年底", "FQ1", "FQ2（最新）"],
    "groups": [
        {"name": "供應與產能承諾", "values": [None, 1190, 2790]},
        {"name": "存貨", "values": [214.0, 258.0, 315.75], "decimals": 1},
        {"name": "保證上限", "values": [None, None, 1085]},
        {"name": "AI 雲協議", "values": [None, None, 360]},
        {"name": "股權投資承諾", "values": [None, None, 250]},
    ],
}

# 圖 4：年化營收（億美元），全部是媒體報導、未審計。頁面表格只寫兩端（OpenAI 100 億 2025-06、近 500 億 2026-09；
# Anthropic 約 90 億 2025-12、650 億 2026-07），中間點與日期取自本頁研究底稿（二手來源：
# OpenAI 2024-12 約 55 億、2025-12 逾 200 億（CFO）、2026-02 逾 250 億（The Information）；
# Anthropic 2026-02 140 億（Series G）、2026-04 逾 300 億、2026-05 初逾 470 億（Series H））。
AI_REV = {
    "unit": "億美元",
    "openai": [["2024-12", 55], ["2025-06", 100], ["2025-12", 200], ["2026-02", 250], ["2026-09", 500]],
    "anthropic": [["2025-12", 90], ["2026-02", 140], ["2026-04", 300], ["2026-05", 470], ["2026-07", 650]],
    "thresholds": [{"label": "高盛打平門檻", "value": 3000}, {"label": "10% 報酬門檻", "value": 4170}],
    "start": "2024-12", "end": "2026-09",
}

# 圖 5：SMH 美國版 vs UCITS 版（%），頁面「持有的是 UCITS 版」表；其他＝100 減四類合計。
_US = {"GPU 鏈": 45.7, "記憶體": 8.7, "設備": 19.2, "類比、PC、手機": 19.9}
_UC = {"GPU 鏈": 44.0, "記憶體": 17.7, "設備": 20.8, "類比、PC、手機": 14.7}
EXPOSURE = {
    "unit": "%", "rows": ["美國版 SMH", "UCITS 版"],
    "segments": [{"name": k, "values": [_US[k], _UC[k]]} for k in _US]
                + [{"name": "其他", "values": [r(100 - sum(_US.values()), 1), r(100 - sum(_UC.values()), 1)]}],
    "nvda": {"name": "NVDA（已含在 GPU 鏈內）", "values": [19.77, 10.06]},
}

# 圖 6：三種情境（頁面「三種情境」表）與價位線（頁面「市場已反映什麼」「W52 規則」）
SCENARIOS = {
    "unit": "美元（SMH 美國版）",
    "items": [
        {"key": "A", "name": "A 消化期已近尾聲", "prob": 25, "lo": 600, "hi": 670, "text": "600 以上"},
        {"key": "B", "name": "B 消化期拉長", "prob": 30, "lo": 480, "hi": 540, "text": "480～540"},
        {"key": "C", "name": "C 循環頂", "prob": 45, "lo": 370, "hi": 400, "text": "370～400"},
    ],
    "lines": [
        {"key": "ma52", "label": "52 週均線", "value": 479.69},
        {"key": "px", "label": "現價", "value": 539.79},
        {"key": "peak", "label": "6/22 高點", "value": 668.91},
    ],
}


def main():
    out = {
        "generated": dt.date.today().isoformat(),
        "drawdown": drawdown_paths(),
        "fpe": forward_pe(),
        "nvidia": NVIDIA, "ai_revenue": AI_REV, "exposure": EXPOSURE, "scenarios": SCENARIOS,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("寫入", OUT, OUT.stat().st_size, "bytes")
    for p in out["drawdown"]["paths"]:
        print(p["peak"], p["group"], "第", p["days"], "日", "回前高" if p["recovered"] else "未回前高", p["last_pct"], "%（最深", p["min_pct"], "%）")
    for m in out["fpe"]["marks"]:
        print(m["label"], m["date"], m["value"])


if __name__ == "__main__":
    main()
