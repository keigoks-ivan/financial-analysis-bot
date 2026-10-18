"""AI 硬體循環（/ideas/ai-hardware-cycle.html）圖表用的數據。

重跑：python3.12 docs/ideas/data/ai-hardware-cycle/data.py [--fpe]
輸出：同目錄 data.json。頁面只讀這份 json 畫圖與填 W52 距離數字，前端不計算。
每個美股交易日由 .github/workflows/daily-us-close.yml 跑一次（不帶旗標）。

每次執行重抓（yfinance，還原權息 auto_adjust）：
- 圖 1 的「現在 2026-06-22」那條路徑：^SOX 收盤，延伸到最新交易日。
- 圖 7a：2026-06-22 收盤到最新交易日的漲跌，10 檔（見 REL_TICKERS）。
- 圖 7b：NVDA ÷ ^SOX，2026-01-02 起，以 2026-06-22 為 100。
- 圖 8：亞洲與美國半導體 16 檔（見 ASIA_TICKERS），今年（2026-01-01 起）最高收盤與日期、最新收盤距該高點的 %、
  近 1 週（往前第 5 個交易日）%、距 52 週均線 %（均線規則同 latest）。各檔用自己市場的交易日，不跨市場取交集；
  跟圖 7 分開抓一次，抓不到或少任何一檔，asia 整塊沿用上一版並標 stale，不影響其他區塊。
- latest：SMH／^SOX／QQQ 的收盤、52 週均線（週五收盤的最近 52 筆平均，含本週最新收盤）、
  距均線 drop_pct＝(1−均線／收盤)×100（還要跌多少碰到均線）、NVDA 收盤、資料日期。
任何一塊抓不到（或少一檔）：該塊保留 data.json 上一版並標 stale: true，程式照常 exit 0。
最新日以 10 檔＋三個均線標的都有收盤的最後一天為準，不用缺資料的半天。

不重抓、照舊寫入（常數在本檔）：圖 3～6 的靜態資料，以及圖 2 的遠期本益比（沿用上一版 data.json）。
圖 2 要更新時加 --fpe：先抓網路，失敗退回本機快取，再退回上一版（標 stale）。

- 圖 1 其他高點（歷史）：~/v7-backtest/data/semi_cycle_drawdowns/SOX.csv（date, close）；
  沒有這個檔（例如 CI）就沿用上一版 data.json 的路徑；兩者都沒有才退回 yfinance ^SOX 全史。高點日取當日收盤。
- 圖 2 費半 12 個月遠期本益比：History of Market（CC BY 4.0）
  https://historyofmarket.com/api/sectors/forward-pe.json 的 sectors.sox。
  週頻 series 到 2026-08-05 為止；其後是同站 forwardOwn（日頻、自算混合遠期，與 series
  口徑相差 3% 以內），這裡取每週最後一筆接在後面，圖上用虛線區分。
  先抓網路，失敗退回本機快取（FPE_CACHE 環境變數或下面的預設路徑），再退回上一版 data.json。
- 圖 3～6：數字抄自頁面正文與表格，頁面沒有的點（圖 4 的中間點）註明出處。
"""
import json
import os
import sys
import time
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


# 圖 7、latest 用的價格參數
BASE_DATE = "2026-06-22"            # 這一輪費半高點（收盤）
RATIO_START = "2026-01-02"
PRICE_START = "2025-06-01"          # 52 週均線要 52 個週五收盤，多抓一些
EVENT = {"date": "2026-11-19", "label": "Nvidia FQ3 財報"}
REL_TICKERS = [  # (yfinance 代號, 圖上標籤)
    ("NVDA", "NVDA"), ("QQQ", "QQQ"), ("AMD", "AMD"), ("TSM", "TSM"), ("AVGO", "AVGO"),
    ("SMH", "SMH"), ("^SOX", "費半 ^SOX"), ("ORCL", "ORCL"), ("MU", "MU"), ("CRWV", "CRWV"),
]
LATEST_KEYS = {"SMH": "smh", "^SOX": "sox", "QQQ": "qqq"}   # 有 52 週均線的三檔
ASIA_START = "2026-01-01"           # 圖 8：今年最高收盤的起算日
ASIA_TICKERS = [  # (yfinance 代號, 中文標籤, 地區)
    ("000660.KS", "海力士", "kr"), ("005930.KS", "三星", "kr"), ("^KS11", "KOSPI", "kr"),
    ("6146.T", "Disco", "jp"), ("8035.T", "東京威力", "jp"), ("6857.T", "愛德萬", "jp"),
    ("0981.HK", "中芯", "cn"),
    ("2330.TW", "台積電", "tw"), ("^TWII", "台股加權", "tw"), ("2454.TW", "聯發科", "tw"),
    ("3711.TW", "日月光", "tw"), ("2317.TW", "鴻海", "tw"),
    ("^SOX", "費半", "us"), ("SMH", "SMH", "us"), ("MU", "美光", "us"), ("NVDA", "Nvidia", "us"),
]
BLOCKS = ("rel", "ratio", "latest", "asia")


def fetch_prices(symbols, start=PRICE_START, tries=3):
    """yfinance 還原權息收盤，回傳 DataFrame（欄＝代號）。三次都失敗就丟例外，由呼叫端沿用舊值。"""
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


def _ymd(ts):
    return pd.Timestamp(ts).strftime("%Y-%m-%d")


def common_frame(df, symbols):
    """只留 symbols 都有收盤的日期（最新日若有一檔還沒出就退到前一天）。"""
    miss = [s for s in symbols if s not in df.columns]
    if miss:
        raise ValueError(f"缺少代號 {miss}")
    d = df[list(symbols)].dropna()
    if d.empty:
        raise ValueError("沒有共同交易日")
    return d


def calc_rel(df):
    """圖 7a：BASE_DATE 收盤到最新共同交易日的漲跌 %，由大到小。"""
    d = common_frame(df, [s for s, _ in REL_TICKERS])
    base = pd.Timestamp(BASE_DATE)
    if base not in d.index:
        raise ValueError(f"基準日 {BASE_DATE} 不在收盤序列內")
    b, last = d.loc[base], d.iloc[-1]
    labels = dict(REL_TICKERS)
    items = [{"ticker": s, "label": labels[s], "pct": r((last[s] / b[s] - 1) * 100, 1),
              "base_close": r(b[s]), "last_close": r(last[s])} for s, _ in REL_TICKERS]
    items.sort(key=lambda x: -x["pct"])
    return {"base_date": BASE_DATE, "last_date": _ymd(d.index[-1]), "adjusted": True, "items": items}


def calc_ratio(df):
    """圖 7b：NVDA ÷ ^SOX，以 BASE_DATE 為 100。"""
    d = common_frame(df, ["NVDA", "^SOX"])
    base = pd.Timestamp(BASE_DATE)
    if base not in d.index:
        raise ValueError(f"基準日 {BASE_DATE} 不在收盤序列內")
    ratio = d["NVDA"] / d["^SOX"]
    idx = (ratio / ratio.loc[base] * 100).loc[RATIO_START:]
    return {"base_date": BASE_DATE, "start": _ymd(idx.index[0]), "last_date": _ymd(idx.index[-1]),
            "event": EVENT, "dates": [_ymd(x) for x in idx.index], "values": [r(v) for v in idx.values]}


def calc_latest(df):
    """SMH／^SOX／QQQ 收盤、52 週均線（週五收盤最近 52 筆平均）、距均線 %；NVDA 收盤；資料日。"""
    d = common_frame(df, list(LATEST_KEYS) + ["NVDA"])
    out = {"date": _ymd(d.index[-1]), "ma_rule": "週五收盤最近 52 筆平均（含本週最新收盤）；drop_pct＝(1−均線／收盤)×100"}
    for sym, key in LATEST_KEYS.items():
        s = d[sym]
        w = s.resample("W-FRI").last().dropna()
        if len(w) < 52:
            raise ValueError(f"{sym} 週收盤不足 52 筆")
        close, ma = float(s.iloc[-1]), float(w.iloc[-52:].mean())
        out[key] = {"close": r(close), "ma52": r(ma), "drop_pct": r((1 - ma / close) * 100, 1)}
    out["nvda"] = {"close": r(d["NVDA"].iloc[-1])}
    return out


def calc_asia(df):
    """圖 8：每檔用自己的交易日（不取交集）。今年最高收盤、距高點 %、近 1 週 %、距 52 週均線 %。跌最多的排前面。"""
    items = []
    for sym, label, region in ASIA_TICKERS:
        if sym not in df.columns:
            raise ValueError(f"缺少代號 {sym}")
        s = df[sym].dropna()
        if len(s) < 6:
            raise ValueError(f"{sym} 收盤不足 6 筆")
        w = s.resample("W-FRI").last().dropna()
        if len(w) < 52:
            raise ValueError(f"{sym} 週收盤不足 52 筆")
        ytd = s.loc[ASIA_START:]
        if ytd.empty:
            raise ValueError(f"{sym} 沒有 {ASIA_START} 之後的收盤")
        close, ma = float(s.iloc[-1]), float(w.iloc[-52:].mean())
        hi = float(ytd.max())
        items.append({"ticker": sym, "label": label, "region": region,
                      "ytd_high": r(hi), "ytd_high_date": _ymd(ytd.idxmax()),
                      "pct_from_high": r((close / hi - 1) * 100, 1),
                      "pct_1w": r((close / float(s.iloc[-6]) - 1) * 100, 1),
                      "ma52": r(ma), "pct_vs_ma52": r((close / ma - 1) * 100, 1),
                      "last_close": r(close), "last_date": _ymd(s.index[-1])})
    items.sort(key=lambda x: x["pct_from_high"])
    return {"start": ASIA_START, "last_date": max(i["last_date"] for i in items), "adjusted": True,
            "ma_rule": "週五收盤最近 52 筆平均（含本週最新收盤）；pct_vs_ma52＝(收盤／均線−1)×100，負數＝已跌破",
            "items": items}


def _path(close, d, grp):
    ts = pd.Timestamp(d)
    if ts not in close.index:
        raise ValueError(f"高點日 {d} 不在費半收盤序列內")
    i = close.index.get_loc(ts)
    seg = close.iloc[i:i + MAX_DAYS + 1]
    # 第一次收盤回到（或高於）高點就截斷，最後一點記 0：圖只畫「跌幅」，不畫創新高之後的漲幅
    back = [k for k in range(1, len(seg)) if seg.iloc[k] >= seg.iloc[0]]
    if back:
        seg = seg.iloc[:back[0] + 1]
    pct = [r((v / seg.iloc[0] - 1) * 100, 1) for v in seg.values]
    if back:
        pct[-1] = 0.0
    return {"peak": d, "group": grp, "peak_close": r(seg.iloc[0]),
            "days": len(pct) - 1, "recovered": bool(back),
            "last_date": seg.index[-1].strftime("%Y-%m-%d"),
            "last_pct": pct[-1], "min_pct": min(pct), "path": pct}


def load_hist_sox(old_paths):
    """歷史高點用的費半收盤：本機 v7 CSV；沒有就回 None（改沿用上一版路徑）；上一版也沒有才抓 yfinance 全史。"""
    if SOX_CSV.exists():
        df = pd.read_csv(SOX_CSV, parse_dates=["date"]).set_index("date")["close"]
        return df.dropna(), f"v7-backtest {SOX_CSV.name}"
    if old_paths:
        return None, "上一版 data.json"
    import yfinance as yf
    df = yf.download("^SOX", start="1994-01-01", auto_adjust=False, progress=False)["Close"]
    df = df.iloc[:, 0] if isinstance(df, pd.DataFrame) else df
    return df.dropna(), "yfinance ^SOX"


def drawdown_paths(live_sox, old):
    """live_sox：yfinance ^SOX 收盤序列（含 BASE_DATE 之後），None 表示這次沒抓到。
    現在這條路徑用 live_sox 延伸到最新日；抓不到就沿用上一版並標 stale。其餘歷史高點不隨日更新。"""
    old_dd = (old or {}).get("drawdown") or {}
    old_paths = {p["peak"]: p for p in old_dd.get("paths", [])}
    hist, hist_src = load_hist_sox(old_paths)
    paths, now_stale = [], False
    for d, grp in PEAKS:
        p = None
        if grp == "now":
            if live_sox is not None:
                try:
                    p = _path(live_sox, d, grp)
                except Exception as e:  # noqa: BLE001
                    print("現在路徑算不出來：", str(e)[:100])
            if p is None:
                p, now_stale = old_paths.get(d), True
        elif hist is not None:
            p = _path(hist, d, grp)
        else:
            p = old_paths.get(d)
        if p is None:
            raise SystemExit(f"高點 {d} 沒有可用資料（沒有 v7 CSV、沒有上一版、也抓不到）")
        paths.append(p)
    now = [p for p in paths if p["group"] == "now"][0]
    src = f"歷史高點：{hist_src}；現在路徑：" + ("yfinance ^SOX" if not now_stale else "上一版 data.json（本次沒抓到）")
    out = {"source": src, "last_close_date": now["last_date"], "paths": paths}
    if now_stale:
        out["stale"] = True
    return out


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
                return {**old, "stale": True}
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


def load_old():
    try:
        return json.loads(OUT.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def build(argv, old, fetch=fetch_prices):
    """組出新的 data.json 內容（不含 generated）。抓價失敗的區塊沿用 old 並標 stale: true。"""
    old = old or {}
    symbols = [s for s, _ in REL_TICKERS]
    px = None
    try:
        px = fetch(symbols)
    except Exception as e:  # noqa: BLE001
        print("抓價失敗，全部價格類區塊沿用上一版：", str(e)[:120])

    # 圖 8 另抓一次（獨立 try）：失敗只讓 asia 沿用舊值，不影響 rel／ratio／latest
    px_asia = None
    try:
        px_asia = fetch([s for s, _, _ in ASIA_TICKERS])
    except Exception as e:  # noqa: BLE001
        print("亞洲價格抓取失敗，圖 8 沿用上一版：", str(e)[:120])

    def block(name, fn, frame):
        try:
            if frame is None:
                raise RuntimeError("沒有價格")
            res = fn(frame)
            # 不讓資料日倒退（例如來源回傳比上一版更舊的資料）
            prev = (old.get(name) or {}).get("last_date") or (old.get(name) or {}).get("date")
            cur = res.get("last_date") or res.get("date")
            if prev and cur and cur < prev:
                raise ValueError(f"新資料日 {cur} 早於上一版 {prev}")
            res["stale"] = False
            return res
        except Exception as e:  # noqa: BLE001
            print(f"{name} 沿用上一版（stale）：", str(e)[:120])
            if name in old:
                return {**old[name], "stale": True}
            return None

    live_sox = None
    if px is not None and "^SOX" in px.columns:
        live_sox = px["^SOX"].dropna()
    out = {"drawdown": drawdown_paths(live_sox, old)}
    if "--fpe" in argv or "fpe" not in old:
        out["fpe"] = forward_pe()
    else:
        out["fpe"] = old["fpe"]
    for name, fn, frame in (("rel", calc_rel, px), ("ratio", calc_ratio, px), ("latest", calc_latest, px),
                            ("asia", calc_asia, px_asia)):
        b = block(name, fn, frame)
        if b is not None:
            out[name] = b
    out.update({"nvidia": NVIDIA, "ai_revenue": AI_REV, "exposure": EXPOSURE, "scenarios": SCENARIOS})
    out["stale"] = bool(out["drawdown"].get("stale") or out["fpe"].get("stale")
                        or any(out.get(n, {}).get("stale", True) for n in BLOCKS))
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    old = load_old()
    out = build(argv, old)
    # generated 只在內容有變時更新，同資料重跑 data.json 不變（CI 才不會天天空 commit）
    out["generated"] = dt.date.today().isoformat()
    if old and {k: v for k, v in old.items() if k != "generated"} == {k: v for k, v in out.items() if k != "generated"}:
        out["generated"] = old.get("generated", out["generated"])
    out = {"generated": out.pop("generated"), **out}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("寫入", OUT, OUT.stat().st_size, "bytes", "（有 stale 區塊）" if out["stale"] else "")
    for p in out["drawdown"]["paths"]:
        print(p["peak"], p["group"], "第", p["days"], "日", "回前高" if p["recovered"] else "未回前高", p["last_pct"], "%（最深", p["min_pct"], "%）")
    for m in out["fpe"]["marks"]:
        print(m["label"], m["date"], m["value"])
    if "rel" in out:
        print("圖 7a", out["rel"]["last_date"], " ".join(f"{i['ticker']} {i['pct']:+.1f}" for i in out["rel"]["items"]))
    if "latest" in out:
        print("latest", json.dumps(out["latest"], ensure_ascii=False))
    if "asia" in out:
        print("圖 8", out["asia"]["last_date"], " ".join(f"{i['label']} {i['pct_from_high']:+.1f}" for i in out["asia"]["items"]))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001  CI 不要因為這支變紅；上一版 data.json 原封不動
        print("data.py 非預期錯誤，未更新：", repr(e)[:200])
