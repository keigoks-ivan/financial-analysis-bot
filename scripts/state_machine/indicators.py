"""五狀態機 — indicators.py：純指標計算（無 I/O、無狀態）。

輸入 = 單檔日線 OHLCV DataFrame（auto_adjust=True 調整價），輸出 = 指標 dict。

週間凍結原則（SPEC §3）：所有週線指標（MA52w/104w/200w、BBand）使用「最近一個
已完成週（上週五）」的值，週內不滾動；週五收盤後當週才納入計算。本模組以資料本身
的日期判定「本週是否已完成」（最後一根日線 weekday == 週五 → 已完成），不依賴
wall-clock 時區，保證每日判定可重現。
"""
from __future__ import annotations

import math
from typing import Optional

import pandas as pd

from config import (
    BB_DDOF,
    BB_LEN_WEEKS,
    BB_SIGMA_EXTREME,
    BB_SIGMA_OVERHEAT,
    MA_DAILY,
    MA_W,
    SHORT_HISTORY_WEEKS,
    VOL_MA_DAYS,
    VOLUME_SPIKE,
)

_FRIDAY = 4  # Monday=0 … Friday=4


def _f(v) -> Optional[float]:
    """float-or-None，過濾 NaN/inf。"""
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return x


def to_weekly(daily: "pd.DataFrame") -> tuple["pd.DataFrame", bool]:
    """日線 → 週線（W-FRI）。回傳 (weekly_full, is_week_complete)。

    weekly_full 每一列：close=該週最後收盤、high=該週日高最大、low=該週日低最小。
    is_week_complete = 最後一根日線為週五（該週已收）。
    """
    if daily is None or daily.empty:
        return pd.DataFrame(), False
    w = pd.DataFrame({
        "close": daily["Close"].resample("W-FRI").last(),
        "high": daily["High"].resample("W-FRI").max(),
        "low": daily["Low"].resample("W-FRI").min(),
    }).dropna(subset=["close"])
    last_bar_date = daily.index[-1]
    is_week_complete = (last_bar_date.weekday() == _FRIDAY)
    return w, is_week_complete


def _sma(series: "pd.Series", n: int) -> Optional[float]:
    if len(series) < n:
        return None
    return _f(series.iloc[-n:].mean())


def compute_indicators(daily: "pd.DataFrame") -> Optional[dict]:
    """從日線 OHLCV 算出全部指標 + 旗標。資料太少（< ~2 個月）回傳 None。"""
    if daily is None or daily.empty or len(daily) < 30:
        return None
    daily = daily[~daily.index.duplicated(keep="last")].sort_index()
    close = daily["Close"].dropna()
    if len(close) < 30:
        return None

    today_close = _f(close.iloc[-1])
    prev_close = _f(close.iloc[-2]) if len(close) >= 2 else None
    today_open = _f(daily["Open"].iloc[-1]) if "Open" in daily else None

    # ── ATH（全歷史收盤；用收盤不用盤中高）─────────────────────────────────
    ath = _f(close.max())
    ath_date = close.idxmax().strftime("%Y-%m-%d") if ath is not None else None
    ath_prev = _f(close.iloc[:-1].max()) if len(close) >= 2 else None
    ath_prev2 = _f(close.iloc[:-2].max()) if len(close) >= 3 else None
    is_new_ath_today = bool(ath_prev is not None and today_close is not None
                            and today_close > ath_prev)
    # 前一日是否「也」創高（用於只在突破首日登記，§4.5「前一日未創」）。
    prev_is_new_ath = bool(ath_prev2 is not None and prev_close is not None
                           and prev_close > ath_prev2)
    pct_vs_ath = (today_close / ath - 1.0) if (today_close and ath) else None
    prev_pct_vs_ath = ((prev_close / ath_prev - 1.0)
                       if (prev_close and ath_prev) else None)

    # ── 日線指標：MA60d、量 ────────────────────────────────────────────────
    ma60d = _sma(close, MA_DAILY)
    vol = _f(daily["Volume"].iloc[-1]) if "Volume" in daily else None
    vol_ma20 = _sma(daily["Volume"].dropna(), VOL_MA_DAYS) if "Volume" in daily else None
    volume_ratio = (vol / vol_ma20) if (vol and vol_ma20) else None
    volume_spike = bool(volume_ratio is not None and volume_ratio >= VOLUME_SPIKE)

    # ── 週線（凍結）──────────────────────────────────────────────────────────
    weekly, is_week_complete = to_weekly(daily)
    if is_week_complete:
        frozen = weekly                 # 本週已收 → 納入
    else:
        frozen = weekly.iloc[:-1]       # 本週未完成 → 丟掉當週、用到上週五
    fclose = frozen["close"] if not frozen.empty else pd.Series(dtype=float)
    n_weeks = len(fclose)

    ma52w = _sma(fclose, MA_W[0])
    ma104w = _sma(fclose, MA_W[1])
    ma200w = _sma(fclose, MA_W[2])
    short_history = n_weeks < SHORT_HISTORY_WEEKS

    # 多頭排列：MA52w>MA104w>MA200w；short_history 降級為 MA52w>MA104w。
    if short_history or ma200w is None:
        alignment = bool(ma52w is not None and ma104w is not None and ma52w > ma104w)
    else:
        alignment = bool(ma52w is not None and ma104w is not None
                         and ma52w > ma104w > ma200w)

    # ── 週線 BBand（凍結週收盤，20 週）─────────────────────────────────────
    bb_mid = bb_sigma = bb_upper2 = bb_upper3 = bb_position = None
    if n_weeks >= BB_LEN_WEEKS:
        window = fclose.iloc[-BB_LEN_WEEKS:]
        bb_mid = _f(window.mean())
        bb_sigma = _f(window.std(ddof=BB_DDOF))
        if bb_mid is not None and bb_sigma is not None:
            bb_upper2 = bb_mid + BB_SIGMA_OVERHEAT * bb_sigma
            bb_upper3 = bb_mid + BB_SIGMA_EXTREME * bb_sigma
            if bb_sigma > 0:
                bb_position = (_f(fclose.iloc[-1]) - bb_mid) / bb_sigma

    frozen_weekly_close = _f(fclose.iloc[-1]) if n_weeks else None
    frozen_week_date = (frozen.index[-1].strftime("%Y-%m-%d")
                        if not frozen.empty else None)

    # 本週至今日高最大（態③觸及判定用）；取 weekly_full 最後一桶（含未完成週）。
    week_high_so_far = _f(weekly["high"].iloc[-1]) if not weekly.empty else None

    pct_vs_52w = (today_close / ma52w - 1.0) if (today_close and ma52w) else None
    pct_vs_60d = (today_close / ma60d - 1.0) if (today_close and ma60d) else None

    return {
        "close": today_close,
        "prev_close": prev_close,
        "open": today_open,
        "ath": ath,
        "ath_date": ath_date,
        "is_new_ath_today": is_new_ath_today,
        "prev_is_new_ath": prev_is_new_ath,
        "ath_prev": ath_prev,
        "pct_vs_ath": pct_vs_ath,
        "prev_pct_vs_ath": prev_pct_vs_ath,
        "ma52w": ma52w,
        "ma104w": ma104w,
        "ma200w": ma200w,
        "alignment": alignment,
        "short_history": short_history,
        "n_weeks": n_weeks,
        "is_week_complete": is_week_complete,
        "bb_mid": bb_mid,
        "bb_sigma": bb_sigma,
        "bb_upper2": bb_upper2,
        "bb_upper3": bb_upper3,
        "bb_position": bb_position,
        "frozen_weekly_close": frozen_weekly_close,
        "frozen_week_date": frozen_week_date,
        "week_high_so_far": week_high_so_far,
        "ma60d": ma60d,
        "pct_vs_52w": pct_vs_52w,
        "pct_vs_60d": pct_vs_60d,
        "above_52w": bool(today_close is not None and ma52w is not None and today_close > ma52w),
        "below_52w": bool(today_close is not None and ma52w is not None and today_close < ma52w),
        "below_60d": bool(today_close is not None and ma60d is not None and today_close < ma60d),
        "vol": vol,
        "vol_ma20": vol_ma20,
        "volume_ratio": volume_ratio,
        "volume_spike": volume_spike,
        "last_bar_date": daily.index[-1].strftime("%Y-%m-%d"),
        "prev_bar_date": daily.index[-2].strftime("%Y-%m-%d") if len(daily) >= 2 else None,
        "last_bar_is_friday": bool(daily.index[-1].weekday() == _FRIDAY),
    }
