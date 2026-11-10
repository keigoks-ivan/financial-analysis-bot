#!/usr/bin/env python3
"""Supertrend 共用核心：算法、K 棒、收完判斷、實盤參數、OHLC 抓取（美股未調股息、台股還原全息）。

實單主系統（update_long_track_w52_adaptive.py）與提醒腳本（supertrend_alert.py）共用這一份，
避免兩邊各寫一份算法而漂移。算法照 TradingView ta.supertrend（ATR 用 RMA、價格取 hl2），
K 線：美股用 Yahoo 未調股息價（auto_adjust=False，已調拆股）；台股（.TW）2026-11-08 起用還原全息（持有人拍板，tw_adjust），算法與 v7-backtest src/supertrend_vs_live/run.py
的 supertrend()／bars() 同一寫法（驗證見交付說明）。

每檔水位 = 0.7 × 週線（多=1／空=0）＋ 0.3 × 月線；只做多，所以趨勢水位只有 100／70／30／0% 四種。
2026-11-06 訊號起加下軌接回（takeback_*）：趨勢水位 30 時週收盤跌破 2.5σ 下軌改成 50。
週線 W-FRI，月線取日曆月底；一根 K 棒要等該期最後一個平日收盤後才算數（is_complete／complete_asof）。
"""
from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

# ---- 實盤參數（持有人 2026-11-04 拍板；v7 /backtest/supertrend_vs_live/ 第十三節鄰近表後選定）----
# 鍵＝Yahoo 代號。美股／倫敦 ATR 14、倍數 3；台股 ATR 14、倍數 2；IEF／GLD 只在債金換規則時用（ATR 14、倍數 3）。
ST_PARAMS = {
    "QQQ": (14, 3.0), "SMH": (14, 3.0), "SMH.L": (14, 3.0),
    "0050.TW": (14, 2.0), "2330.TW": (14, 2.0),
    "IEF": (14, 3.0), "GLD": (14, 3.0),
}
W_WEEK, W_MONTH = 0.7, 0.3
TF = {"week": ("W-FRI", "週線"), "month": ("ME", "月線")}
SETTLE = timedelta(minutes=45)   # 收盤後多久才視為定案

# 實單切換：資料日（訊號日）>= 此日的紀錄照 Supertrend；2026-11-04（週三）收盤訊號、11-05（週四）第一次下單。
# 環境變數 W52_ST_CUTOVER_DATE 只供本機模擬用，CI 不設。
import os as _os
ST_CUTOVER_DATE = _os.environ.get("W52_ST_CUTOVER_DATE") or "2026-11-04"
ST_CUTOVER_DECISION_DATE = "2026-11-04"

# 美股指數部權重切換：資料日（訊號日）>= 此日的紀錄，QQQ 0.7／SMH（含 SMH.L）0.3；之前各 0.5。
# 2026-11-04 收盤的訊號起、11-05 下單（持有人 11-05 拍板，當天生效）。環境變數 W52_LEG_WEIGHTS_CUTOVER_DATE 只供本機模擬用，CI 不設。
LEG_WEIGHTS_CUTOVER_DATE = _os.environ.get("W52_LEG_WEIGHTS_CUTOVER_DATE") or "2026-11-04"
LEG_WEIGHTS_DECISION_DATE = "2026-11-05"

# 台股指數部加正二：資料日（訊號日）>= 此日的紀錄，00631L 0.2、0050 0.4、2330 0.4；之前 0050／2330 各 0.5。
# 2026-11-13（週五）收盤的訊號起、11-16 第一次下單（持有人 2026-11-10 拍板）。環境變數 W52_TW_L2_CUTOVER_DATE 只供本機模擬用，CI 不設。
TW_L2_CUTOVER_DATE = _os.environ.get("W52_TW_L2_CUTOVER_DATE") or "2026-11-13"
TW_L2_DECISION_DATE = "2026-11-10"
TW_L2_WEIGHT = 0.2
TW_L2_TB_LEVEL = 30
TW_L2_MULT = 2


def leg_weights(ds: str) -> dict:
    """每檔占各市場指數部的權重（鍵＝Yahoo 代號）。依據 knowledge/rule_ledger.md「2026-11-05：美股指數部權重由
    QQQ 50／SMH 50 改為 QQQ 70／SMH 30」（持有人 2026-11-05 拍板）：資料日 >= LEG_WEIGHTS_CUTOVER_DATE 時
    美股 QQQ 0.7、SMH／SMH.L 0.3，之前全部 0.5。台股依 rule_ledger「2026-11-10：台股指數部加正二 20%」：
    資料日 >= TW_L2_CUTOVER_DATE 時 0050／2330 各 0.4（正二 0.2 不在這張表，見 l2_table），之前各 0.5。
    每檔占指數部淨值＝水位 × 該檔權重；只給實盤 profile 用，舊 W52 對照線維持各半。"""
    new = str(ds)[:10] >= LEG_WEIGHTS_CUTOVER_DATE
    tw = 0.4 if str(ds)[:10] >= TW_L2_CUTOVER_DATE else 0.5
    return {"QQQ": 0.7 if new else 0.5, "SMH": 0.3 if new else 0.5, "SMH.L": 0.3 if new else 0.5,
            "0050.TW": tw, "2330.TW": tw}


# ---------------------------------------------------------------- Supertrend
def supertrend(b: pd.DataFrame, n: int, f: float) -> pd.DataFrame:
    """回傳每根 K 棒的 dir（1 多、0 空）、line（多頭時是下方支撐線、空頭時是上方壓力線）、lo／up。
    lo／up 是翻轉門檻：多頭時收盤低於 lo 翻空，空頭時收盤高於 up 翻多。"""
    h, l, c = b.high.values, b.low.values, b.close.values
    k = len(c)
    out = pd.DataFrame({"dir": np.nan, "line": np.nan, "lo": np.nan, "up": np.nan}, index=b.index)
    if k <= n:
        return out
    pc = np.r_[np.nan, c[:-1]]
    tr = np.where(np.isnan(pc), h - l, np.maximum.reduce([h - l, np.abs(h - pc), np.abs(l - pc)]))
    atr = np.full(k, np.nan)
    atr[n - 1] = tr[:n].mean()
    for i in range(n, k):
        atr[i] = (atr[i - 1] * (n - 1) + tr[i]) / n
    hl2 = (h + l) / 2
    up0, lo0 = hl2 + f * atr, hl2 - f * atr
    up, lo = up0.copy(), lo0.copy()
    d, st = np.full(k, np.nan), np.full(k, np.nan)
    for i in range(k):
        if np.isnan(atr[i]):
            continue
        if i > 0 and not np.isnan(atr[i - 1]):
            lo[i] = lo0[i] if (lo0[i] > lo[i - 1] or c[i - 1] < lo[i - 1]) else lo[i - 1]
            up[i] = up0[i] if (up0[i] < up[i - 1] or c[i - 1] > up[i - 1]) else up[i - 1]
        if i == 0 or np.isnan(atr[i - 1]):
            d[i] = 1
        elif st[i - 1] == up[i - 1]:
            d[i] = -1 if c[i] > up[i] else 1
        else:
            d[i] = 1 if c[i] < lo[i] else -1
        st[i] = lo[i] if d[i] == -1 else up[i]
    out["dir"] = np.where(np.isnan(d), np.nan, (d == -1).astype(float))
    out["line"] = st
    out["lo"], out["up"] = lo, up
    return out


def bars(d: pd.DataFrame, rule: str) -> pd.DataFrame:
    g = d.resample(rule)
    b = pd.DataFrame({"high": g.high.max(), "low": g.low.min(), "close": g.close.last(),
                      "last_day": g.close.apply(lambda s: s.index.max() if len(s) else pd.NaT)})
    return b.dropna(subset=["close"])


def last_weekday(d: pd.Timestamp) -> pd.Timestamp:
    while d.weekday() >= 5:
        d -= pd.Timedelta(days=1)
    return d


def is_complete(label: pd.Timestamp, last_data: pd.Timestamp, now_local: datetime, close_t: time) -> bool:
    """週期（日曆標籤 label）是否已收完：之後已有資料，或最後一個平日已收盤且資料到那天。"""
    if last_data > label:
        return True
    end = last_weekday(label)
    close_dt = datetime.combine(end.date(), close_t, tzinfo=now_local.tzinfo) + SETTLE
    return last_data.normalize() == end.normalize() and now_local >= close_dt


def complete_asof(label: pd.Timestamp, d: pd.Timestamp) -> bool:
    """資料日 d 的日紀錄（盤後才寫，當天已定案）看，標籤 label 的週期是否已收完。
    與 is_complete 在「最新一根已定案」時等價：d 已到該期最後一個平日（或更晚）即收完。"""
    return pd.Timestamp(d).normalize() >= last_weekday(pd.Timestamp(label)).normalize()


# ---------------------------------------------------------------- 週／月狀態
def make_frames(ohlc: pd.DataFrame, n: int, f: float) -> dict:
    """ohlc 需含 high／low／close（美股未調股息、台股還原全息）。回傳 {tf: (K 棒表, Supertrend 表)}。"""
    out = {}
    for key, (rule, _) in TF.items():
        b = bars(ohlc, rule)
        out[key] = (b, supertrend(b[["high", "low", "close"]], n, f))
    return out


def state_asof(frames: dict, d: pd.Timestamp) -> dict:
    """資料日 d 當下：每個週期「最後一根已收完的 K 棒」狀態（confirmed），以及還沒收完的進行中 K 棒
    （partial，含翻轉門檻 lo／up）。partial 要 ohlc 結束在 d 才準（實盤即如此；回放歷史日只用 confirmed）。"""
    d = pd.Timestamp(d).normalize()
    out = {}
    for key, (b, s) in frames.items():
        done = np.array([complete_asof(ix, d) for ix in b.index])
        valid = s["dir"].notna().values
        comp = s[done & valid]
        if comp.empty:
            out[key] = None
            continue
        ix = comp.index[-1]
        c = comp.iloc[-1]
        res = {"dir": int(c["dir"]), "line": float(c["line"]), "bar_end": str(ix.date()),
               "close": float(b.close[ix]), "partial": None}
        # 進行中 K 棒：最後一根、尚未收完、資料不晚於 d
        if not done[-1] and b.last_day.iloc[-1] <= d and valid[-1]:
            cur = s.iloc[-1]
            res["partial"] = {"dir": int(cur["dir"]), "line": float(cur["line"]), "lo": float(cur["lo"]),
                              "up": float(cur["up"]), "bar_end": str(b.index[-1].date()),
                              "close": float(b.close.iloc[-1]), "as_of": str(b.last_day.iloc[-1].date())}
        out[key] = res
    return out


def level_pct(w_dir: int, m_dir: int) -> int:
    """水位（%）＝ 70 × 週線 ＋ 30 × 月線；整數 %，只會是 100／70／30／0。"""
    return int(round((W_WEEK * w_dir + W_MONTH * m_dir) * 100))


# ---------------------------------------------------------------- 下軌接回（持有人 2026-11-06 拍板）
# 依據 knowledge/rule_ledger.md「2026-11-06：指數部加下軌接回」；回測 v7-backtest docs/BB_Extreme_Overlay_Results.md
# 「追加：接到 50」（fe66464，帳本 BB_EXTREME_OVERLAY-023／028 那組）。每一腿各自算：
# - z ＝（週收盤 − 20 週均線）÷ 20 週母體標準差；週收盤用跟 Supertrend 同一份週 K，只用已收完的週。
# - 觸發：週收盤 z ≤ −2.5，而且當週趨勢水位剛好 30（週線空、月線多）→ 水位改成 50。
# - 結束（先到的為準）：週收盤 z ≥ 0（回到 20 週均線，水位回 30）；趨勢水位離開 30（週線翻多 → 100、月線翻空 → 0）。
#   不設時間上限、不設價格停損。z 要先回到 −1 以上才能再觸發。
# - 同一天先處理結束、再處理重新觸發、最後處理觸發；之後若趨勢水位不是 30 就結束（跟回測同順序）。
# 從頭重播整段歷史，不存狀態；資料日（訊號日）>= BB_TAKEBACK_CUTOVER_DATE 才套用。環境變數只供本機模擬。
BB_TAKEBACK_CUTOVER_DATE = _os.environ.get("W52_BB_TAKEBACK_CUTOVER_DATE") or "2026-11-06"
BB_TAKEBACK_DECISION_DATE = "2026-11-06"
BB_K, BB_REARM, BB_LEVEL, BB_WIN = 2.5, -1.0, 50, 20


def weekly_z(wclose: pd.Series, win: int = BB_WIN) -> pd.DataFrame:
    """20 週均線、母體標準差與 z（跟 v7 src/weekly_bb_put/signals.weekly_z 同算法）。"""
    ma = wclose.rolling(win).mean()
    sd = wclose.rolling(win).std(ddof=0)
    return pd.DataFrame({"ma": ma, "sd": sd, "z": (wclose - ma) / sd})


def takeback_table(frames: dict) -> pd.DataFrame:
    """依完成日（標籤所在週／月的最後一個平日）逐一重播。回傳以完成日為索引的狀態表：
    trend（趨勢水位）、level（接回後水位，未套生效日）、active、z、ma、sd、start（觸發那週標籤）、
    trigger_z、ended（這天結束的原因，沒有就空字串）。資料日 d 的狀態＝完成日 <= d 的最後一列。"""
    wb, ws = frames["week"]
    mb, ms = frames["month"]
    zt = weekly_z(wb["close"])
    ev: dict = {}
    for ix in wb.index:
        ev.setdefault(last_weekday(ix).normalize(), {})["w"] = ix
    for ix in mb.index:
        ev.setdefault(last_weekday(ix).normalize(), {})["m"] = ix
    w_dir = m_dir = None
    active, armed = None, True
    rows = []
    for key in sorted(ev):
        e = ev[key]
        if "w" in e and ws["dir"].notna()[e["w"]]:
            w_dir = int(ws["dir"][e["w"]])
        if "m" in e and ms["dir"].notna()[e["m"]]:
            m_dir = int(ms["dir"][e["m"]])
        trend = level_pct(w_dir, m_dir) if (w_dir is not None and m_dir is not None) else None
        ended = ""
        z = ma = sd = np.nan
        if "w" in e:
            z, ma, sd = (float(zt[c][e["w"]]) for c in ("z", "ma", "sd"))
            if z == z:
                if active is not None and z >= 0:
                    active, ended = None, "回到 20 週均線"
                if z > BB_REARM:
                    armed = True
                if active is None and armed and z <= -BB_K and trend == 30:
                    active = {"start": e["w"], "trigger_z": z}
                    armed = False
        if active is not None and trend != 30:
            active, ended = None, ("週線翻多" if trend == 100 else "月線翻空" if trend == 0 else f"趨勢水位變成 {trend}")
        rows.append({"date": key, "trend": trend, "level": BB_LEVEL if active is not None else trend,
                     "active": active is not None, "z": z, "ma": ma, "sd": sd,
                     "start": active["start"] if active is not None else pd.NaT,
                     "trigger_z": active["trigger_z"] if active is not None else np.nan, "ended": ended})
    return pd.DataFrame(rows).set_index("date")


def takeback_asof(frames: dict, d, table: pd.DataFrame | None = None) -> dict | None:
    """資料日 d 當下的接回狀態；已套生效日（d < BB_TAKEBACK_CUTOVER_DATE 時 applied=False、level＝trend）。
    回傳 {trend, level, applied, active, start, trigger_z, z, ma, sd, z_bar}；z／ma／sd 是最後一根已收完週 K 的值。"""
    t = takeback_table(frames) if table is None else table
    d = pd.Timestamp(d).normalize()
    t = t[t.index <= d]
    if t.empty:
        return None
    r = t.iloc[-1]
    wz = t[t["z"].notna()]
    applied = str(d.date()) >= BB_TAKEBACK_CUTOVER_DATE
    act = bool(r["active"]) and applied
    return {"trend": None if pd.isna(r["trend"]) else int(r["trend"]),
            "level": int(r["level"]) if act else (None if pd.isna(r["trend"]) else int(r["trend"])),
            "applied": applied, "active": act,
            "start": str(pd.Timestamp(r["start"]).date()) if act else None,
            "trigger_z": float(r["trigger_z"]) if act else None,
            "z": float(wz["z"].iloc[-1]) if len(wz) else None, "ma": float(wz["ma"].iloc[-1]) if len(wz) else None,
            "sd": float(wz["sd"].iloc[-1]) if len(wz) else None, "z_bar": str(wz.index[-1].date()) if len(wz) else None}


def takeback_daily(frames: dict, idx: pd.DatetimeIndex) -> pd.Series:
    """每個資料日的最終水位（整數 %）：生效日以前＝趨勢水位，生效日起接回中＝50。給歷史重播／頁面用。"""
    t = takeback_table(frames)
    pos = t.index.searchsorted(pd.DatetimeIndex(idx).normalize(), side="right") - 1
    lv = np.where(pos >= 0, t["level"].values[np.clip(pos, 0, None)], np.nan).astype(float)
    tr = np.where(pos >= 0, t["trend"].values[np.clip(pos, 0, None)], np.nan).astype(float)
    on = np.array([str(x.date()) >= BB_TAKEBACK_CUTOVER_DATE for x in pd.DatetimeIndex(idx)])
    return pd.Series(np.where(on, lv, tr), index=idx)


# ---------------------------------------------------------------- 台股正二（持有人 2026-11-10 拍板）
# 依據 knowledge/rule_ledger.md「2026-11-10：台股指數部加正二 20%」；回測 v7-backtest src/l2_vs_981a/sleeve_20_40_40.py
# （帳本 TW-SLEEVE-L2-20-40-40）。00631L 占台股指數部 20%，訊號只看 0050 的週線 Supertrend（跟 0050 同一份週 K，14／2、還原全息）：
# - 週線多水位 100、週線空水位 0；不看月線。
# - 接回：週線空時週收盤 z ≤ −2.5 → 水位 30（占指數部 6%）；週收盤 z ≥ 0 或週線翻多就結束；z 回到 −1 以上才能再觸發。
#   不設時間上限、不設價格停損；同一天先結束、再解鎖、後觸發（跟 takeback_table 同順序）。
# 從頭重播整段歷史，不存狀態；資料日 >= TW_L2_CUTOVER_DATE 才實際持有，之前只預覽。


def l2_table(frames: dict) -> pd.DataFrame:
    """依週線完成日逐一重播，回傳以完成日為索引的狀態表：trend（100／0）、level（接回後水位）、active、z、ma、sd、start、trigger_z、ended。"""
    wb, ws = frames["week"]
    zt = weekly_z(wb["close"])
    w_dir = None
    active, armed = None, True
    rows = []
    for ix in wb.index:
        if ws["dir"].notna()[ix]:
            w_dir = int(ws["dir"][ix])
        trend = None if w_dir is None else 100 * w_dir
        ended = ""
        z, ma, sd = (float(zt[c][ix]) for c in ("z", "ma", "sd"))
        if z == z:
            if active is not None and z >= 0:
                active, ended = None, "回到 20 週均線"
            if z > BB_REARM:
                armed = True
            if active is None and armed and z <= -BB_K and trend == 0:
                active = {"start": ix, "trigger_z": z}
                armed = False
        if active is not None and trend != 0:
            active, ended = None, "週線翻多"
        rows.append({"date": last_weekday(ix).normalize(), "trend": trend,
                     "level": TW_L2_TB_LEVEL if active is not None else trend,
                     "active": active is not None, "z": z, "ma": ma, "sd": sd,
                     "start": active["start"] if active is not None else pd.NaT,
                     "trigger_z": active["trigger_z"] if active is not None else np.nan, "ended": ended})
    return pd.DataFrame(rows).set_index("date")


def l2_asof(frames: dict, d, table: pd.DataFrame | None = None) -> dict | None:
    """資料日 d 當下的正二狀態（水位不受生效日影響，生效日前當預覽；applied 表示是否已實際持有）。"""
    t = l2_table(frames) if table is None else table
    d = pd.Timestamp(d).normalize()
    t = t[t.index <= d]
    if t.empty or pd.isna(t["trend"].iloc[-1]):
        return None
    r = t.iloc[-1]
    wz = t[t["z"].notna()]
    act = bool(r["active"])
    return {"trend": int(r["trend"]), "level": int(r["level"]), "applied": str(d.date()) >= TW_L2_CUTOVER_DATE, "active": act,
            "start": str(pd.Timestamp(r["start"]).date()) if act else None,
            "trigger_z": float(r["trigger_z"]) if act else None,
            "z": float(wz["z"].iloc[-1]) if len(wz) else None, "ma": float(wz["ma"].iloc[-1]) if len(wz) else None,
            "sd": float(wz["sd"].iloc[-1]) if len(wz) else None, "z_bar": str(wz.index[-1].date()) if len(wz) else None}


def l2_daily(frames: dict, idx: pd.DatetimeIndex) -> pd.Series:
    """每個資料日的正二水位（整數 %）：生效日以前 0（還沒持有），生效日起照 l2_table。給記分板重播用。"""
    t = l2_table(frames)
    pos = t.index.searchsorted(pd.DatetimeIndex(idx).normalize(), side="right") - 1
    lv = np.where(pos >= 0, t["level"].values[np.clip(pos, 0, None)], np.nan).astype(float)
    on = np.array([str(x.date()) >= TW_L2_CUTOVER_DATE for x in pd.DatetimeIndex(idx)])
    return pd.Series(np.where(on, lv, 0.0), index=idx)


# ---------------------------------------------------------------- 取價
OFFICIAL_TOL = 1e-4          # 相對差門檻
OFFICIAL_MAX_BARS = 3
OFFICIAL_MAX_MOVE = 0.11     # 台股漲跌停 ±10%


def _roc_to_ts(s):
    try:
        s = str(s).strip()
        if "/" in s:
            y, m, d = s.split("/")
        else:
            y, m, d = s[:-4], s[-4:-2], s[-2:]
        return pd.Timestamp(int(y) + 1911, int(m), int(d))
    except Exception:
        return None


def _num(x):
    try:
        v = float(str(x).replace(",", ""))
        return v if v > 0 else None
    except Exception:
        return None


def fetch_official_ohlc(code: str, since: pd.Timestamp, now_tpe: datetime) -> dict | None:
    """證交所官方日 K（原始價）{Timestamp: (high, low, close)}。月檔 STOCK_DAY，since 當月到本月。
    抓不到回 None；任何例外都不外拋（官方抓不到不得讓實單主程式掛掉）。"""
    import time as _t
    import requests
    out: dict = {}
    months = pd.period_range(pd.Timestamp(since).to_period("M"),
                             pd.Timestamp(now_tpe.year, now_tpe.month, 1).to_period("M"), freq="M")
    ok_any = False
    for k, per in enumerate(months):
        try:
            if k:
                _t.sleep(1.5)
            r = requests.get("https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY",
                             params={"date": f"{per.year}{per.month:02d}01", "stockNo": code, "response": "json"},
                             headers={"User-Agent": "Mozilla/5.0 (compatible; investmquest-w52/1.0)"}, timeout=20)
            r.raise_for_status()
            j = r.json()
            if not isinstance(j, dict):
                continue
            ok_any = True
            for row in j.get("data") or []:
                ts, hi, lo, cl = _roc_to_ts(row[0]), _num(row[4]), _num(row[5]), _num(row[6])
                if ts is not None and hi and lo and cl:
                    out[ts] = (hi, lo, cl)
        except Exception as e:  # noqa: BLE001
            print(f"  official STOCK_DAY {code} {per} failed: {e}")
    return out if ok_any and out else None


def reconcile_ohlc(d: pd.DataFrame, off: dict | None):
    """純函式：用官方日 K 補 yfinance 序列最新的一兩根（只動最新幾根，歷史不動）。
    (1) 最後一根與官方差 > 容許且前一根吻合 → 換成官方 high／low／close；(2) 晚到的日子（≤3 根）用官方補上。"""
    notes = {"yf_last": str(d.index[-1].date()), "official": bool(off), "appended": [], "refreshed": [], "skipped": None}
    if not off:
        return d, notes
    # 中間漏掉的日子（Yahoo 偶爾少一天，例如 0050 的 2026-11-03）：官方有、Yahoo 沒有、且落在最後 10 天內 → 補上
    gaps = sorted(x for x in off if d.index[0] < x < d.index[-1] and x not in d.index
                  and x >= d.index[-1] - pd.Timedelta(days=10))
    if gaps:
        add_rows, ok_gaps = [], []
        for x in gaps:
            prev_close = float(d.close[d.index < x].iloc[-1])
            if abs(off[x][2] / prev_close - 1) > OFFICIAL_MAX_MOVE:
                continue
            add_rows.append({"high": off[x][0], "low": off[x][1], "close": off[x][2]})
            ok_gaps.append(x)
        if add_rows:
            d = pd.concat([d, pd.DataFrame(add_rows, index=pd.DatetimeIndex(ok_gaps))]).sort_index()
            notes["gap_filled"] = [str(x.date()) for x in ok_gaps]
    last = d.index[-1]
    if last in off and len(d) >= 2:
        prev = d.index[-2]
        if prev in off and abs(float(d.close.iloc[-2]) / off[prev][2] - 1) <= OFFICIAL_TOL:
            hi, lo, cl = off[last]
            cur = d.iloc[-1]
            if any(abs(float(cur[k]) / v - 1) > OFFICIAL_TOL for k, v in (("high", hi), ("low", lo), ("close", cl))):
                d = d.copy()
                d.loc[last, ["high", "low", "close"]] = [hi, lo, cl]
                notes["refreshed"].append(str(last.date()))
    new_dates = sorted(x for x in off if x > last)
    if new_dates:
        if len(new_dates) > OFFICIAL_MAX_BARS:
            notes["skipped"] = f"缺口 {len(new_dates)} 根 > {OFFICIAL_MAX_BARS}，不補"
            return d, notes
        rows, ref = [], float(d.close.iloc[-1])
        for x in new_dates:
            if abs(off[x][2] / ref - 1) > OFFICIAL_MAX_MOVE:
                notes["skipped"] = f"{x.date()} 相對前值變動超過 {OFFICIAL_MAX_MOVE:.0%}，不補"
                break
            rows.append((x, off[x]))
            ref = off[x][2]
        if rows:
            add = pd.DataFrame([{"high": v[0], "low": v[1], "close": v[2]} for _, v in rows],
                               index=pd.DatetimeIndex([x for x, _ in rows]))
            d = pd.concat([d, add])
            notes["appended"] = [str(x.date()) for x, _ in rows]
    return d, notes


# 各代號的交易所時區與「當日日線可採用」時間（收盤＋緩衝）；盤中或剛收盤的未定案日線不進決策。
SETTLE_LOCAL = {
    "America/New_York": time(16, 30),
    "Asia/Taipei": time(14, 15),
    "Europe/London": time(17, 20),
}
TZ_OF = {"QQQ": "America/New_York", "SMH": "America/New_York", "IEF": "America/New_York", "GLD": "America/New_York",
         "SMH.L": "Europe/London", "0050.TW": "Asia/Taipei", "2330.TW": "Asia/Taipei"}


def yahoo_daily(sym: str, tries: int = 3, wait_s: int = 40) -> pd.DataFrame:
    """Yahoo 日線（auto_adjust=False、欄名小寫、index 為日期）。UTC 午夜後最新一根可能還沒定稿、OHLC 全 NaN
    （2026-11-07 美股週五收盤因此漏算），最新一根有 NaN 就等一下重抓；重抓後還是 NaN 就照舊交給呼叫端 dropna。"""
    import time as _time
    import yfinance as yf
    h = pd.DataFrame()
    for i in range(tries):
        h = yf.Ticker(sym).history(period="max", interval="1d", auto_adjust=False)
        if h.empty:
            raise RuntimeError(f"{sym}: Yahoo 沒有資料")
        if h[["High", "Low", "Close"]].iloc[-1].notna().all():
            break
        print(f"  {sym}: Yahoo 最新一根 {h.index[-1].date()} 還沒定稿（第 {i + 1} 次）")
        if i < tries - 1:
            _time.sleep(wait_s)
    h.index = pd.to_datetime(h.index).tz_localize(None).normalize()
    return h.rename(columns=str.lower)


def tw_adjust(d: pd.DataFrame, raw: pd.DataFrame) -> pd.DataFrame:
    """台股訊號用還原全息（持有人 2026-11-08 拍板）：高、低、收 × Adj Close／Close。raw＝yahoo_daily 的結果。
    證交所官方補上的最新幾根 Yahoo 還沒有比值，沿用最後一個比值（最近一次除權息之後比值是 1）。"""
    r = (raw["adj close"] / raw["close"]).dropna()
    r = r[~r.index.duplicated(keep="last")].reindex(d.index).ffill().bfill()
    out = d.copy()
    for c in ("high", "low", "close"):
        out[c] = d[c] * r
    return out


def fetch_ohlc(sym: str, now_utc: datetime | None = None) -> tuple[pd.DataFrame, dict]:
    """日 K（high／low／close，已調拆股）：美股未調股息，台股還原全息（tw_adjust）。台股最新一兩根用證交所官方日 K 補值；
    當地時間還沒到定案時間的當天那根丟掉；now_utc 給了就把資料截到那一刻（模擬用）。"""
    now_utc = now_utc or datetime.now(timezone.utc)
    raw = yahoo_daily(sym)
    d = raw[["high", "low", "close"]].dropna()   # Yahoo 未定稿的最新一根會是 NaN
    d = d[~d.index.duplicated(keep="last")]
    notes = {"official": False, "appended": [], "refreshed": [], "skipped": None}
    tz = TZ_OF[sym]
    local = now_utc.astimezone(ZoneInfo(tz))
    if sym.endswith(".TW"):
        off = fetch_official_ohlc(sym.split(".")[0], d.index[-1] - pd.Timedelta(days=7),
                                  now_utc.astimezone(ZoneInfo("Asia/Taipei")))
        if off:
            off = {k: v for k, v in off.items() if k.date() <= local.date()}
        d = d[d.index.date <= local.date()]
        d, notes = reconcile_ohlc(d, off)
    d = d[d.index.date <= local.date()]
    if d.index[-1].date() == local.date() and local.time() < SETTLE_LOCAL[tz]:
        print(f"  {sym}: 當地 {local:%H:%M} 未到定案時間，不採用 {d.index[-1].date()} 這根")
        d = d.iloc[:-1]
    if sym.endswith(".TW"):
        d = tw_adjust(d, raw)
    return d, notes


# ---------------------------------------------------------------- 翻轉門檻（頁面與信件共用）
def thresholds(leg_state: dict) -> dict:
    """由 state_asof 的結果（週線／月線 confirmed＋partial）算出「收盤到哪裡會翻」。
    有進行中 K 棒：門檻＝該棒目前的 lo（多頭）或 up（空頭），收完前會小幅移動（exact=True 表示來自進行中 K 棒）；
    還沒開新棒（例如剛收完週五）：只能用上一根的線當近似（exact=False），新棒一開始線值會微調。
    回傳 {tf: {"thr", "exact", "dir", "close", "as_of", "gap_pct", "flip_to"}}，close／gap 以進行中 K 棒最新價計。"""
    out = {}
    for key in ("week", "month"):
        c = leg_state[key]
        p = c.get("partial")
        if p:
            thr = p["lo"] if c["dir"] == 1 else p["up"]
            px, as_of = p["close"], p["as_of"]
        else:
            thr, px, as_of = c["line"], c["close"], c["bar_end"]
        out[key] = {"thr": float(thr), "exact": bool(p), "dir": c["dir"], "close": float(px), "as_of": as_of,
                    "gap_pct": (float(px) / float(thr) - 1) * 100, "flip_to": 0 if c["dir"] == 1 else 1,
                    "partial_flipped": bool(p and p["dir"] != c["dir"])}
    return out
