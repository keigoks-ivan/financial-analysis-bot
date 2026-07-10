#!/usr/bin/env python3
"""宏觀投資時鐘（美林框架）機械層 — 增長×通膨兩軸合成針位＋歷史驗證.

v1 方法（2026-07-10 持有人拍板：美國單一座標、搭 weekly-market-update 班車）：
  增長軸 = mean(z6[CFNAI], z6[PAYEMS 3M 均月增], -z6[UNRATE])
  通膨軸 = mean(z6[核心 PCE YoY], z6[CPI YoY], z6[T10YIE 月均], z6[PPIACO YoY])
  z6[x] = (x_t − x_{t−6}) / std(全史 6 個月變化)——「方向動能」，非水位
  象限：G↑I↓ 復甦(股) / G↑I↑ 過熱(商品) / G↓I↑ 滯脹(現金) / G↓I↓ 再通脹(債)
  針角 = atan2(I, G)，0°=正北（增長上行、通膨中性），順時針

PREREG（凍結，季檢才可調；比照四形狀門檻慣例）：
  6 個月變化窗、等權合成、z-score 全史 std、T10YIE 缺值期（<2003）通膨軸降級三序列。

驗證（describer 檢定，非擇時）：
  逐月象限 × 次月資產報酬（股 ^GSPC / 債 GS10 合成 TR / 商品 PPIACO / 現金 TB3MS），
  含出版時滯版（象限訊號 +2 個月再對報酬——可實作視角）。兩窗：1972+ 與 2000+。

輸出：docs/macro/data/clock.json（現況針位＋逐月歷史＋驗證統計）。
Fail-safe：任一序列抓取失敗 → 保留舊檔 exit 0（比照 universe 慣例）。
Usage: python3 scripts/build_macro_clock.py
"""
from __future__ import annotations

import io
import json
import math
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "macro" / "data" / "clock.json"

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
UA = {"User-Agent": "Mozilla/5.0 (imq-macro-clock; research script)"}

GROWTH = {"CFNAI": +1, "PAYEMS": +1, "UNRATE": -1}
INFLATION = {"PCEPILFE": +1, "CPIAUCSL": +1, "T10YIE": +1, "PPIACO": +1}
ASSETS = {"GS10": None, "TB3MS": None}  # 另抓 ^GSPC via yfinance

QUAD = {(+1, -1): "復甦", (+1, +1): "過熱", (-1, +1): "滯脹", (-1, -1): "再通脹"}
QUAD_ASSET = {"復甦": "股票", "過熱": "商品", "滯脹": "現金", "再通脹": "債券"}


def fred(sid: str) -> pd.Series:
    req = urllib.request.Request(FRED.format(sid=sid), headers=UA)
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    df = pd.read_csv(io.StringIO(raw))
    df.columns = ["date", "v"]
    df["date"] = pd.to_datetime(df["date"])
    s = pd.to_numeric(df.set_index("date")["v"], errors="coerce").dropna()
    return s


def monthly(s: pd.Series) -> pd.Series:
    return s.resample("ME").mean().dropna()


def z6(x: pd.Series) -> pd.Series:
    d = x - x.shift(6)
    sd = d.std()
    return d / sd if sd and not math.isnan(sd) else d * 0


def build_axes() -> tuple[pd.DataFrame, dict]:
    raw: dict[str, pd.Series] = {}
    for sid in [*GROWTH, *INFLATION, *ASSETS, "SP500_dummy"][:-1]:
        raw[sid] = monthly(fred(sid))
        print(f"  fred {sid}: {len(raw[sid])} 月 [{raw[sid].index[0]:%Y-%m}..{raw[sid].index[-1]:%Y-%m}]", file=sys.stderr)

    # 轉換層
    t: dict[str, pd.Series] = {}
    t["CFNAI"] = raw["CFNAI"]                                   # 已是動能複合
    pay = raw["PAYEMS"].diff()                                   # 月增（千人）
    t["PAYEMS"] = pay.rolling(3).mean()
    t["UNRATE"] = raw["UNRATE"]
    t["PCEPILFE"] = raw["PCEPILFE"].pct_change(12) * 100         # YoY
    t["CPIAUCSL"] = raw["CPIAUCSL"].pct_change(12) * 100
    t["T10YIE"] = raw["T10YIE"]
    t["PPIACO"] = raw["PPIACO"].pct_change(12) * 100

    g = pd.DataFrame({k: z6(t[k]) * sgn for k, sgn in GROWTH.items()}).mean(axis=1)
    # 通膨軸：T10YIE 2003 年才有——缺值期以其餘三序列平均（PREREG 明文降級，非靜默）
    infl_parts = pd.DataFrame({k: z6(t[k]) * sgn for k, sgn in INFLATION.items()})
    i = infl_parts.mean(axis=1, skipna=True)
    axes = pd.DataFrame({"g": g, "i": i}).dropna()
    latest_detail = {k: round(float(z6(t[k]).iloc[-1] * sgn), 2)
                     for k, sgn in [*GROWTH.items(), *INFLATION.items()]
                     if len(z6(t[k]).dropna())}
    return axes, {"series_z6_latest": latest_detail,
                  "series_asof": {k: f"{v.index[-1]:%Y-%m}" for k, v in raw.items()}}


def asset_returns() -> pd.DataFrame:
    import yfinance as yf
    spx = yf.download("^GSPC", start="1970-01-01", interval="1mo",
                      progress=False, auto_adjust=True)["Close"]
    if isinstance(spx, pd.DataFrame):
        spx = spx.iloc[:, 0]
    spx = spx.resample("ME").last()
    r_stock = spx.pct_change() * 100
    gs10 = monthly(fred("GS10"))
    # 10Y 合成 TR：收益 + 久期價格效應（D≈8）
    r_bond = gs10 / 12 + 8 * (-gs10.diff())
    tb = monthly(fred("TB3MS"))
    r_cash = tb / 12
    ppi = monthly(fred("PPIACO"))
    r_cmdy = ppi.pct_change() * 100
    return pd.DataFrame({"股票": r_stock, "債券": r_bond, "商品": r_cmdy, "現金": r_cash}).dropna()


def validate(axes: pd.DataFrame, rets: pd.DataFrame) -> dict:
    quad = axes.apply(lambda r: QUAD[(1 if r.g >= 0 else -1, 1 if r.i >= 0 else -1)], axis=1)
    out = {}
    for lag, tag in [(1, "contemporaneous_next_month"), (2, "publication_lagged")]:
        sig = quad.shift(lag).reindex(rets.index).dropna()
        joined = rets.reindex(sig.index)
        stats: dict[str, dict] = {}
        for win, since in [("1972+", "1972-01-01"), ("2000+", "2000-01-01")]:
            sub_sig = sig[sig.index >= since]
            sub = joined[joined.index >= since]
            per = {}
            for q in QUAD.values():
                m = sub[sub_sig == q]
                if len(m) < 12:
                    continue
                per[q] = {"months": int(len(m)),
                          **{a: round(float(m[a].mean()) * 12, 1) for a in rets.columns}}
            stats[win] = per
        out[tag] = stats
    return out


def main() -> int:
    try:
        axes, meta = build_axes()
        rets = asset_returns()
    except Exception as e:
        if OUT.exists():
            print(f"⚠ 抓取失敗（{e}）— 保留舊檔")
            return 0
        raise
    g, i = float(axes.g.iloc[-1]), float(axes.i.iloc[-1])
    quadrant = QUAD[(1 if g >= 0 else -1, 1 if i >= 0 else -1)]
    angle = round(math.degrees(math.atan2(i, g)) % 360, 1)  # 0°=北(G+), 90°=東(I+)
    hist = [{"d": f"{d:%Y-%m}", "g": round(float(r.g), 2), "i": round(float(r.i), 2)}
            for d, r in axes.iterrows()]
    payload = {
        "schema": "macro-clock-v1",
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": f"{axes.index[-1]:%Y-%m}",
        "growth_score": round(g, 2), "inflation_score": round(i, 2),
        "quadrant": quadrant, "quadrant_asset": QUAD_ASSET[quadrant],
        "angle_deg": angle,
        "method": "z6 等權：G=CFNAI+非農3M動能−失業率 / I=核心PCE+CPI+T10YIE+PPI 商品（YoY 動能）；PREREG 凍結",
        **meta,
        "validation": validate(axes, rets),
        "history": hist,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"clock.json: {payload['as_of']} G={g:+.2f} I={i:+.2f} → {quadrant}（{angle}°）· 歷史 {len(hist)} 月")
    return 0


if __name__ == "__main__":
    sys.exit(main())
