"""債市重定價與市場分化（/ideas/bond-repricing.html）的數據。

重跑：python3.12 docs/ideas/data/bond-repricing/data.py
輸出：同目錄 data.json。文章裡的市場數字都從這份來。

- 價格：yfinance，auto_adjust=True（還原股價）。殖利率指數（^TNX 等）單位是 %。
- FRED：CSV 直抓，不用 key。BAMLH0A0HYM2／BAMLC0A0CM 在 FRED 只給近 3 年。
- 區間：2026-08-13 收盤 → 最新交易日；YTD 以 2025 年最後一個交易日收盤為基期。
"""
import io
import json
import datetime as dt
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf

OUT = Path(__file__).with_name("data.json")
WINDOW_START = "2026-08-13"
PHASE2_START = "2026-09-22"  # 熊平轉熊陡的分界：9/16 升息後，長端開始領漲
YTD_BASE = "2025-12-31"
FETCH_FROM = "2025-12-01"

YF = {
    "yields": ["^FVX", "^TNX", "^TYX"],
    "oil": ["BZ=F", "CL=F"],
    "equity": ["SPY", "RSP", "IWM", "SOXX", "QQQ"],
    "curve": ["KRE", "TLT", "XHB"],
    "credit": ["HYG", "LQD", "SHY", "AGG", "EMB"],
    "fx": ["DX-Y.NYB"],
}
FRED = {
    "DGS2": "2Y 公債殖利率",
    "DGS5": "5Y 公債殖利率",
    "DGS10": "10Y 公債殖利率",
    "DGS30": "30Y 公債殖利率",
    "DFII5": "5Y TIPS 實質殖利率",
    "DFII10": "10Y TIPS 實質殖利率",
    "DFII30": "30Y TIPS 實質殖利率",
    "T10YIE": "10Y breakeven（FRED 官方）",
    "THREEFYTP10": "10Y 期限溢價（Kim-Wright）",
    "BAMLH0A0HYM2": "HY OAS",
    "BAMLC0A0CM": "IG OAS",
    "MORTGAGE30US": "30 年房貸利率（Freddie Mac）",
    "DFEDTARU": "聯邦基金目標上限",
    "DFEDTARL": "聯邦基金目標下限",
    "EXPINF10YR": "10Y 預期通膨（Cleveland Fed 模型）",
    "DFF": "有效聯邦基金利率",
}
# 30 天聯邦基金期貨：11 月合約＝10/28 會後利率、1 月合約＝12/9 會後利率（11、1 月無 FOMC）
ZQ = {"ZQV26.CBT": "2026-10", "ZQX26.CBT": "2026-11", "ZQZ26.CBT": "2026-12", "ZQF27.CBT": "2027-01"}
LONG_HISTORY = {"DFII10": "2003-01-01", "THREEFYTP10": "1990-01-01", "MORTGAGE30US": "1971-01-01"}
RATIOS = {"RSP/SPY": ("RSP", "SPY"), "IWM/SPY": ("IWM", "SPY"),
          "KRE/TLT": ("KRE", "TLT"), "SOXX/RSP": ("SOXX", "RSP")}


def fred(series_id, start="1990-01-01"):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    s = pd.to_numeric(df.iloc[:, 1], errors="coerce")
    s.index = pd.to_datetime(df.iloc[:, 0])
    return s.dropna()


def yf_close(tickers, start, end=None):
    df = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)["Close"]
    if isinstance(df, pd.Series):
        df = df.to_frame(tickers[0])
    return df


def at(s, date):
    """date 當天或之前最近一筆。"""
    s = s.dropna()
    s = s[s.index <= pd.Timestamp(date)]
    return (s.index[-1].strftime("%Y-%m-%d"), float(s.iloc[-1])) if len(s) else (None, None)


def r4(x):
    return None if x is None else round(float(x), 4)


def level_block(s, unit):
    s = s.dropna()
    d0, v0 = at(s, WINDOW_START)
    dy, vy = at(s, YTD_BASE)
    dl, vl = s.index[-1].strftime("%Y-%m-%d"), float(s.iloc[-1])
    mult = 100 if unit == "pct" else 1
    return {"latest": r4(vl), "latest_date": dl, "base": r4(v0), "base_date": d0,
            "ytd_base": r4(vy), "ytd_base_date": dy,
            "chg_since_base_bp" if unit == "pct" else "chg_since_base": r4((vl - v0) * mult),
            "chg_ytd_bp" if unit == "pct" else "chg_ytd": r4((vl - vy) * mult)}


def return_block(s):
    s = s.dropna()
    d0, v0 = at(s, WINDOW_START)
    dy, vy = at(s, YTD_BASE)
    vl = float(s.iloc[-1])
    return {"latest": r4(vl), "latest_date": s.index[-1].strftime("%Y-%m-%d"),
            "ret_since_base_pct": r4((vl / v0 - 1) * 100), "ret_ytd_pct": r4((vl / vy - 1) * 100),
            "ret_60d_pct": r4((vl / float(s.iloc[-61]) - 1) * 100) if len(s) > 60 else None}


def breadth_history():
    """廣度弱＋指數新高之後 6 個月（126 交易日）SPY 報酬的分布。RSP 2003-04 上市，樣本從 2003-05 起。
    訊號：SPY 收在歷史新高，且 RSP/SPY 63 日變化落在全樣本最低 10%。同一段行情只取第一天（之後 63 日內不重複計）。"""
    px = yf_close(["SPY", "RSP"], start="2003-05-01").dropna()
    ratio = px["RSP"] / px["SPY"]
    r63 = ratio.pct_change(63)
    ath = px["SPY"] >= px["SPY"].cummax()
    fwd = px["SPY"].shift(-126) / px["SPY"] - 1
    cut = r63.quantile(0.10)
    raw = (ath & (r63 <= cut)).fillna(False)
    sig_dates, last = [], None
    for d in raw[raw].index:
        if last is None or px.index.get_loc(d) - px.index.get_loc(last) >= 63:
            sig_dates.append(d)
            last = d
    done = [d for d in sig_dates if pd.notna(fwd.loc[d])]
    f = fwd.loc[done] * 100

    def dist(x):
        x = x.dropna()
        return {"n": int(len(x)), "median_pct": r4(x.median()), "p25_pct": r4(x.quantile(.25)),
                "p75_pct": r4(x.quantile(.75)), "min_pct": r4(x.min()), "max_pct": r4(x.max()),
                "share_negative": r4((x < 0).mean())}

    ath_fwd = fwd[ath] * 100
    return {
        "sample_from": px.index[0].strftime("%Y-%m-%d"),
        "r63_bottom10_cut_pct": r4(cut * 100),
        "signal_dates": [d.strftime("%Y-%m-%d") for d in sig_dates],
        "fwd126_after_signal": dist(f),
        "fwd126_signal_detail": [{"date": d.strftime("%Y-%m-%d"), "fwd126_pct": r4(fwd.loc[d] * 100)} for d in done],
        "fwd126_all_ath_days": dist(ath_fwd),
        "fwd126_all_days": dist(fwd * 100),
        "now": {"date": px.index[-1].strftime("%Y-%m-%d"),
                "spy_at_ath": bool(ath.iloc[-1]),
                "spy_pct_below_ath": r4((px["SPY"].iloc[-1] / px["SPY"].cummax().iloc[-1] - 1) * 100),
                "rsp_spy_r63_pct": r4(r63.iloc[-1] * 100),
                "rsp_spy_r63_percentile": r4((r63.dropna() <= r63.iloc[-1]).mean()),
                "rsp_spy_ratio": r4(ratio.iloc[-1]),
                "rsp_spy_ratio_percentile_since_2003": r4((ratio <= ratio.iloc[-1]).mean()),
                "rsp_spy_ratio_min_date": ratio.idxmin().strftime("%Y-%m-%d")},
    }


def last_time_at_least(series_id, start):
    """最新值上一次（60 天以前）出現同樣高或更高是哪一天。"""
    s = fred(series_id, start)
    now = s.iloc[-1]
    prev = s[(s >= now) & (s.index < s.index[-1] - pd.Timedelta(days=60))]
    return {"latest": r4(now), "latest_date": s.index[-1].strftime("%Y-%m-%d"), "history_from": s.index[0].strftime("%Y-%m-%d"),
            "last_time_at_least": prev.index[-1].strftime("%Y-%m-%d") if len(prev) else None,
            "value_then": r4(prev.iloc[-1]) if len(prev) else None}


def fed_futures(effr):
    """FedWatch 式簡算：升息機率＝(會後月份合約隱含利率 − 基準利率)/25bp。基準＝有效聯邦基金利率。"""
    rows = {}
    for t, m in ZQ.items():
        h = yf.Ticker(t).history(period="15d")["Close"].dropna()
        rows[m] = [[d.strftime("%Y-%m-%d"), r4(100 - v)] for d, v in h.items()]
    out = {"contracts": rows, "effr": r4(effr), "by_date": {}}
    nov = dict(rows["2026-11"]); jan = dict(rows["2027-01"])
    for d in sorted(set(nov) & set(jan)):
        out["by_date"][d] = {"oct_hike_prob": r4((nov[d] - effr) / 0.25),
                             "dec_hike_prob_after_oct": r4((jan[d] - nov[d]) / 0.25),
                             "cum_hikes_by_jan": r4((jan[d] - effr) / 0.25)}
    return out


def intraday_tnx(day):
    """^TNX 5 分鐘線（yfinance 只保留約 60 天，過期就留空，data.json 保留當時抓到的值）。"""
    try:
        x = yf.download("^TNX", interval="5m", start=day, end=(pd.Timestamp(day) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"), progress=False)["Close"]
        x = x.iloc[:, 0] if isinstance(x, pd.DataFrame) else x
        x = x.dropna()
        x.index = x.index.tz_convert("America/New_York")
        return {"open": r4(x.iloc[0]), "low": r4(x.min()), "low_time": x.idxmin().strftime("%H:%M"),
                "high": r4(x.max()), "high_time": x.idxmax().strftime("%H:%M"), "last": r4(x.iloc[-1]), "tz": "America/New_York"}
    except Exception as e:
        return {"error": str(e)[:120]}


def macro():
    """總經：能從 FRED 算的用算的；BEA 第三次估計的分項手動填、附原文出處。"""
    pay = fred("PAYEMS", "2026-01-01")
    chg = pay.diff().dropna()
    yoy = {}
    for sid in ("PCEPI", "PCEPILFE", "CPIAUCSL", "CPILFESL", "CES0500000003"):
        x = fred(sid, "2025-01-01")
        # 用日期對齊去年同月（2025-10 CPI 因政府關門缺一筆，不能往回數 12 筆）
        prev = x.get(x.index[-1] - pd.DateOffset(years=1))
        yoy[sid] = {"month": x.index[-1].strftime("%Y-%m"), "yoy_pct": r4((x.iloc[-1] / prev - 1) * 100) if prev else None}
    return {
        "payrolls_monthly_change_k": [[d.strftime("%Y-%m"), int(v)] for d, v in chg.iloc[-4:].items()],
        "payrolls_3m_avg_k": r4(chg.iloc[-3:].mean()),
        "unemployment_rate": at(fred("UNRATE", "2026-01-01"), "2100-01-01"),
        "yoy": yoy,
        "bea_gdp_2026q2_third": {
            "source": "https://www.bea.gov/sites/default/files/2026-09/gdp2q26-3rd.pdf",
            "real_gdp_saar": 2.2, "current_dollar_gdp_saar": 8.5,
            "real_final_sales_private_domestic_saar": 4.6,
            "gross_domestic_purchases_price_saar": 5.6, "pce_price_saar": 5.0, "core_pce_price_saar": 3.3},
        "bls_2026_09_release": {"source": "https://www.bls.gov/news.release/empsit.nr0.htm",
                                "revision_jul_aug_k": -60},
        "treasury_debt_to_penny": {"source": "https://api.fiscaldata.treasury.gov (debt_to_penny)",
                                   "date": "2026-10-02", "total_public_debt_tn": 40.24, "held_by_public_tn": 32.43},
    }


def nominal_growth_vs_10y():
    """名目 GDP 年增 vs 10Y 殖利率季均：2006–2007 與最近 4 季。"""
    gdp = fred("GDP", "2004-01-01")
    yoy = (gdp / gdp.shift(4) - 1) * 100
    saar = ((gdp / gdp.shift(1)) ** 4 - 1) * 100
    y10 = fred("DGS10", "2004-01-01").resample("QS").mean()
    rows = []
    for d in yoy.index:
        if (d.year in (2006, 2007)) or d >= yoy.index[-4]:
            rows.append({"quarter": f"{d.year}Q{(d.month - 1) // 3 + 1}", "nominal_gdp_yoy_pct": r4(yoy.loc[d]), "nominal_gdp_saar_pct": r4(saar.loc[d]),
                         "dgs10_qavg_pct": r4(y10.get(d))})
    return rows


def main():
    out = {"asof": dt.date.today().isoformat(), "window_start": WINDOW_START, "ytd_base": YTD_BASE,
           "sources": {"prices": "yfinance (auto_adjust=True)", "fred": "fred.stlouisfed.org fredgraph.csv"}}

    all_t = [t for v in YF.values() for t in v]
    px = yf_close(all_t, start=FETCH_FROM)
    out["yf_last_date"] = px.dropna(how="all").index[-1].strftime("%Y-%m-%d")

    out["yields_yf"] = {t: level_block(px[t], "pct") for t in YF["yields"]}
    out["returns"] = {t: return_block(px[t]) for g in ("oil", "equity", "curve", "credit", "fx") for t in YF[g]}

    fr = {sid: fred(sid, "2023-01-01" if sid.startswith("BAML") else "2025-06-01") for sid in FRED}
    out["fred"] = {sid: {"name": FRED[sid], **level_block(fr[sid], "pct")} for sid in FRED}
    for sid in ("DGS2", "DGS5", "DGS10", "DGS30", "DFII5", "DFII10", "DFII30", "T10YIE", "THREEFYTP10", "BAMLH0A0HYM2"):
        d2, v2 = at(fr[sid], PHASE2_START)
        out["fred"][sid]["at_phase2_start"] = [d2, r4(v2)]
    out["long_history"] = {sid: last_time_at_least(sid, st) for sid, st in LONG_HISTORY.items()}
    ig = fr["BAMLC0A0CM"]
    out["ig_oas"] = {"latest_pct": r4(ig.iloc[-1]), "window_from": ig.index[0].strftime("%Y-%m-%d"),
                     "window_min_pct": r4(ig.min()), "window_min_date": ig.idxmin().strftime("%Y-%m-%d"),
                     "percentile_in_window": r4((ig <= ig.iloc[-1]).mean())}
    out["fed_futures"] = fed_futures(float(fr["DFF"].iloc[-1]))
    out["tnx_intraday_2026_10_02"] = intraday_tnx("2026-10-02")
    # 5 年後 5 年期遠期殖利率（由 DGS5、DGS10 推）
    y5, y10 = fr["DGS5"].iloc[-1] / 100, fr["DGS10"].iloc[-1] / 100
    out["fwd_5y5y_pct"] = r4((((1 + y10) ** 10 / (1 + y5) ** 5) ** (1 / 5) - 1) * 100)

    # breakeven：^TNX − DFII10（推算）；另列 FRED 官方 T10YIE 對照
    tnx = px["^TNX"].dropna()
    dfii = fr["DFII10"]
    be = (tnx - dfii.reindex(tnx.index, method="ffill")).dropna()
    out["breakeven_10y_derived"] = {"note": "^TNX − DFII10，推算值", **level_block(be, "pct")}

    # 曲線：^TNX − ^FVX（替代）與 DGS10 − DGS2
    s5 = (px["^TNX"] - px["^FVX"]).dropna()
    out["curve"] = {"TNX_minus_FVX": level_block(s5, "pct")}
    s2 = (fr["DGS10"] - fr["DGS2"].reindex(fr["DGS10"].index)).dropna()
    out["curve"]["DGS10_minus_DGS2"] = level_block(s2, "pct")
    out["curve"]["DGS10_minus_DGS2"]["at_phase2_start"] = [at(s2, PHASE2_START)[0], r4(at(s2, PHASE2_START)[1])]
    s30 = (fr["DGS30"] - fr["DGS5"].reindex(fr["DGS30"].index)).dropna()
    out["curve"]["DGS30_minus_DGS5"] = level_block(s30, "pct")
    out["curve"]["DGS30_minus_DGS5"]["at_phase2_start"] = [at(s30, PHASE2_START)[0], r4(at(s30, PHASE2_START)[1])]

    # HY OAS：30 天變化、FRED 可得區間的分位
    hy = fr["BAMLH0A0HYM2"]
    d30, v30 = at(hy, hy.index[-1] - pd.Timedelta(days=30))
    out["hy_oas"] = {"latest_pct": r4(hy.iloc[-1]), "latest_date": hy.index[-1].strftime("%Y-%m-%d"),
                     "chg_30d_bp": r4((hy.iloc[-1] - v30) * 100), "chg_30d_from": d30,
                     "window_from": hy.index[0].strftime("%Y-%m-%d"),
                     "window_min_pct": r4(hy.min()), "window_min_date": hy.idxmin().strftime("%Y-%m-%d"),
                     "window_max_pct": r4(hy.max()), "window_max_date": hy.idxmax().strftime("%Y-%m-%d"),
                     "percentile_in_window": r4((hy <= hy.iloc[-1]).mean()),
                     "max_30d_widening_bp_in_window": r4((hy - hy.rolling("30D").min()).max() * 100)}
    w30 = (hy - hy.rolling("30D").min()) * 100
    out["hy_oas"]["share_days_30d_widening_ge_75bp"] = r4((w30 >= 75).mean())
    out["hy_oas"]["dates_30d_widening_ge_75bp"] = sorted({d.strftime("%Y-%m") for d in w30[w30 >= 75].index})
    out["hy_oas"]["p95_30d_widening_bp"] = r4(w30.quantile(.95))

    # 比值（日頻）
    ratios = {}
    for name, (a, b) in RATIOS.items():
        s = (px[a] / px[b]).dropna()
        d0, v0 = at(s, WINDOW_START)
        dy, vy = at(s, YTD_BASE)
        tail = s.iloc[-60:]
        ratios[name] = {"latest": r4(s.iloc[-1]), "chg_since_base_pct": r4((s.iloc[-1] / v0 - 1) * 100),
                        "chg_ytd_pct": r4((s.iloc[-1] / vy - 1) * 100),
                        "series_60d": [[d.strftime("%Y-%m-%d"), r4(v)] for d, v in tail.items()]}
    out["ratios"] = ratios
    out["series_60d"] = {k: [[d.strftime("%Y-%m-%d"), r4(v)] for d, v in s.dropna().iloc[-60:].items()]
                         for k, s in {"^TNX": px["^TNX"], "TNX_minus_FVX": s5, "BZ=F": px["BZ=F"]}.items()}
    out["series_60d"]["HY_OAS"] = [[d.strftime("%Y-%m-%d"), r4(v)] for d, v in hy.iloc[-60:].items()]
    out["series_60d"]["DFII10"] = [[d.strftime("%Y-%m-%d"), r4(v)] for d, v in dfii.iloc[-60:].items()]

    out["macro"] = macro()
    out["breadth_history"] = breadth_history()
    out["nominal_growth_vs_10y"] = nominal_growth_vs_10y()

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("wrote", OUT, "yf_last_date", out["yf_last_date"])


if __name__ == "__main__":
    main()
