#!/usr/bin/env python3
"""C1 影子對照（美股）— 每日更新：cap 1.0 股票部分 ＋ IEF／GLD 週線趨勢疊加
================================================================================
2026-10-17 新增。實盤（W52 × 自適應 σ × cap_eff × A2，update_long_track_w52_adaptive.py）不動；
本檔只是並排追蹤的「影子對照線」，無 email、不入實單、不寫任何持倉金額或股數。

C1 定義（唯一依據：v7-backtest/src/pain_reduction/ 的 README、PREREG_pain_robustness_20261017.md、
robust_test.build_candidate("C1")；本檔照抄邏輯、不改參數）：
  1. 股票部分 ＝ cap 1.0（不借錢）：每腿 = 0.5 × W52 閘門 × min(1, σ_t/RV20)，執行層 A2
     （20pp 門檻／10% 取整／clamp 50pp 每腿）。與記分板 S-A10 影子（build_live_scoreboard.py
     的 band_exec_replay_capped）同一套程式，直接重用，不另寫一份。
  2. 疊加 ＝ IEF 最多 20%、GLD 最多 20%。各自用週線三條件 E3，每成立一條 ＋1/3：
        週收 > 40 週均、週收 > 52 週均、週收 > 52 週前。
     權重 = 20% × (條件數/3)，訊號 t 收盤 → t+2 起計報酬（研究的 shift(2)）。
     疊加報酬 = 權重 × (資產日報酬 − ^IRX 日率) − 權重和 × roll(8bp/年) − |Δ權重| × 1bp。
     （以超額報酬計＝疊加部位以現金利率融資；roll／換手成本為研究凍結值 B3／A-i。）

追蹤口徑（與記分板一致，才能和「實盤」並排）：
  起點 ＝ 實盤 state.json 第一筆 source=='live' 日（NAV=100，該日不計報酬）；
  股票部分日報酬 ＝ Σ腿 前日執行率 × 腿日報酬 ＋ 現金部分 × ^IRX 日率 − 換手 × 7bps（重用
  build_live_scoreboard.leg_daily_returns_generic）；C1 日報酬 ＝ 股票部分 ＋ 疊加部分。
  「實盤」NAV 與 cap 1.0 影子 NAV 都用同一個函式從同一份 state.json 重算，兩者與
  docs/market/data/live_scoreboard.json 的 nav_sys／nav_a10 逐日一致（啟動時自檢）。

研究期回測（2005-01-03～2026-10-16）是凍結的歷史曲線，由 gen_c1_backtest_series.py 在本機產生
docs/long-track-w52-adaptive/c1_backtest.json，本檔只讀取並渲染；兩段在頁面上分開標示。

輸出：docs/long-track-w52-adaptive/c1-shadow.html、c1_shadow_state.json。
FAIL-SAFE：任何資料缺口或例外一律印警告、exit 0、不動既有輸出檔（比照 build_live_scoreboard.py）。
"""
from __future__ import annotations

import json
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import update_long_track_w52_adaptive as _w52  # noqa: E402  (fetch_close／band_exec_replay／WEIGHTS)
import build_live_scoreboard as _lsb  # noqa: E402  (S-A10 執行層與日報酬簿記，原函式重用)

try:                                       # fab: scripts/site_nav.py
    from site_nav import full_nav_block
except ImportError:                        # pragma: no cover
    full_nav_block = None

DOCS = _w52.DOCS
DIR = DOCS / "long-track-w52-adaptive"
STATE_IN = DIR / "state.json"
BT_JSON = DIR / "c1_backtest.json"
OUT_HTML = DIR / "c1-shadow.html"
OUT_STATE = DIR / "c1_shadow_state.json"
SCOREBOARD_JSON = DOCS / "market" / "data" / "live_scoreboard.json"

# ── 研究凍結常數（run_a_defensive_fill／PREREG；不得調整）──
W_OVERLAY = 0.20                  # IEF、GLD 各最多 20%
ROLL_D = 0.0008 / 252.0           # roll 8bp/年
GATE_TURN = 0.0001                # 閘門變動 1bp/邊
LAG = 2                           # 訊號 t 收盤 → 報酬序列 shift(2)
SA10_CLAMP = 50.0                 # cap 1.0：clamp 50pp/腿（恆不觸發）
LEGS = _w52.US_TICKERS
MARKET = _lsb.MARKETS[0]          # 美股


class Abort(Exception):
    pass


def warn(msg):
    print(f"[c1-shadow][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[c1-shadow] {msg}")


# ═══════════════════════════════════════════════════════════════════════
# 價格與 E3
# ═══════════════════════════════════════════════════════════════════════
def fetch_adj(sym: str) -> pd.Series:
    end = datetime.now() + timedelta(days=1)
    df = yf.download(sym, start="2004-06-01", end=end.strftime("%Y-%m-%d"),
                     progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    c = df["Close"]
    if isinstance(c, pd.DataFrame):
        c = c.iloc[:, 0]
    c = c.dropna()
    if getattr(c.index, "tz", None) is not None:
        c.index = c.index.tz_localize(None)
    if len(c) < 400:
        raise Abort(f"{sym} 價格筆數不足（{len(c)}）")
    return c


def e3_weekly(adj: pd.Series) -> pd.DataFrame:
    """逐字對齊 put_timing_backtest.trend.gate_e3：W-FRI 收盤，三條件各 1/3。"""
    w = adj.resample("W-FRI").last().dropna()
    m40, m52, p52 = w.rolling(40).mean(), w.rolling(52).mean(), w.shift(52)
    df = pd.DataFrame({"close": w, "ma40": m40, "ma52": m52, "px52": p52})
    df["c1"] = (w > m40).astype(int)
    df["c2"] = (w > m52).astype(int)
    df["c3"] = (w > p52).astype(int)
    df["n"] = df["c1"] + df["c2"] + df["c3"]
    return df


def e3_daily_count(adj: pd.Series, index: pd.DatetimeIndex) -> pd.Series:
    """條件數（0..3）ffill 到日線；只在週五（含）之後生效，進行中的週不提前採用。"""
    wk = e3_weekly(adj)["n"] / 3.0
    return (wk.reindex(index, method="ffill").fillna(0.0) * 3.0).round()


def cash_series(index: pd.DatetimeIndex, irx: dict) -> pd.Series:
    s = pd.Series(irx)
    s.index = pd.to_datetime(s.index)
    return (s.sort_index().reindex(index, method="ffill") / 100.0 / 252.0)


# ═══════════════════════════════════════════════════════════════════════
# 主計算
# ═══════════════════════════════════════════════════════════════════════
def drawdown_pct(navs: list) -> list:
    peak, out = -1e18, []
    for v in navs:
        peak = max(peak, v)
        out.append(round((v / peak - 1.0) * 100.0, 3))
    return out


def build():
    try:
        state = json.loads(STATE_IN.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        raise Abort(f"讀不到 {STATE_IN.name}: {e}")
    history = sorted(state.get("history_us") or [], key=lambda r: r["date"])
    live_rows = [r for r in history if r.get("source") == "live"]
    if not history or not live_rows:
        raise Abort("state.json 缺 history_us 或無 live 實錄")
    inception = live_rows[0]["date"]
    live_dates = [r["date"] for r in live_rows]
    date_to_idx = {r["date"]: i for i, r in enumerate(history)}

    # 腿價格與現金率（重用實盤腳本／記分板的取價函式）
    px = {t: {ts.strftime("%Y-%m-%d"): float(c) for ts, c in _w52.fetch_close(t).items()} for t in LEGS}
    px_dates = {t: sorted(px[t]) for t in LEGS}
    irx = _lsb.fetch_us_cash_series()
    irx_dates = sorted(irx)
    gaps: list = []

    # 實盤與 cap 1.0 影子（同一套簿記）
    ex_main = _w52.band_exec_replay(history, LEGS)["executed"]
    ex_a10 = _lsb.band_exec_replay_capped(history, LEGS, _w52.WEIGHTS, SA10_CLAMP)
    rows_main = _lsb.leg_daily_returns_generic(MARKET, LEGS, history, live_dates, date_to_idx, ex_main,
                                               px, px_dates, irx, irx_dates, gaps, "C1-main")
    rows_a10 = _lsb.leg_daily_returns_generic(MARKET, LEGS, history, live_dates, date_to_idx, ex_a10,
                                              px, px_dates, irx, irx_dates, gaps, "C1-a10")
    if gaps:
        raise Abort(f"腿報酬缺口：{gaps[:2]}")
    nav_main = _lsb.nav_from_returns(rows_main, inception)
    nav_a10 = _lsb.nav_from_returns(rows_a10, inception)

    # 自檢：與記分板已發布的 nav_sys／nav_a10 逐日比對（容許 4 位小數四捨五入）
    sb_diff = None
    if SCOREBOARD_JSON.exists():
        try:
            sb = json.loads(SCOREBOARD_JSON.read_text(encoding="utf-8"))["markets"]["us"]
            m_sys = {r["date"]: r["nav"] for r in sb["nav_sys"]}
            m_a10 = {r["date"]: r["nav"] for r in sb["nav_a10"]}
            d1 = max((abs(r["nav"] - m_sys[r["date"]]) for r in nav_main if r["date"] in m_sys), default=0.0)
            d2 = max((abs(r["nav"] - m_a10[r["date"]]) for r in nav_a10 if r["date"] in m_a10), default=0.0)
            sb_diff = {"main_vs_scoreboard_max_abs": round(d1, 4), "a10_vs_scoreboard_max_abs": round(d2, 4),
                       "scoreboard_as_of": sb.get("data_through")}
            info(f"自檢 vs 記分板：實盤 {d1:.4f}、cap1.0 {d2:.4f}（截至 {sb.get('data_through')}）")
        except Exception as e:  # noqa: BLE001
            warn(f"記分板自檢略過：{type(e).__name__}: {e}")

    # 疊加：IEF／GLD 週線三條件，日曆＝QQQ 交易日
    cal = pd.DatetimeIndex(sorted(pd.to_datetime(list(px["QQQ"].keys()))))
    ief, gld = fetch_adj("IEF"), fetch_adj("GLD")
    cash = cash_series(cal, irx).fillna(0.0)
    ret_x = {}
    for k, a in (("ief", ief), ("gld", gld)):
        ret_x[k] = a.pct_change().reindex(cal).fillna(0.0) - cash
    cnt = {"ief": e3_daily_count(ief, cal), "gld": e3_daily_count(gld, cal)}
    w = {k: (W_OVERLAY * cnt[k] / 3.0).shift(LAG).fillna(0.0) for k in cnt}
    turn = (w["ief"].diff().abs() + w["gld"].diff().abs()).fillna(0.0) * GATE_TURN
    sleeve = (w["ief"] * ret_x["ief"] + w["gld"] * ret_x["gld"]
              - (w["ief"] + w["gld"]) * ROLL_D - turn)

    # C1 日報酬 ＝ cap1.0 股票部分 ＋ 疊加；NAV 起點同實盤
    nav_c1, nav = [], 100.0
    for r in rows_a10:
        d = r["date"]
        if d != inception:
            nav *= 1.0 + r["ret"] + float(sleeve.get(pd.Timestamp(d), 0.0))
        nav_c1.append({"date": d, "nav": round(nav, 4)})

    # 逐日曝險／權重（% of 淨值）
    daily = []
    for i, d in enumerate(live_dates):
        idx = date_to_idx[d]
        ts = pd.Timestamp(d)
        e_main = sum(ex_main[t][idx] for t in LEGS)
        e_c1 = sum(ex_a10[t][idx] for t in LEGS)
        daily.append({
            "date": d,
            "nav_main": nav_main[i]["nav"], "nav_cap10": nav_a10[i]["nav"], "nav_c1": nav_c1[i]["nav"],
            "stock_main_pct": round(e_main, 1), "stock_c1_pct": round(e_c1, 1),
            "ief_w_pct": round(float(w["ief"].get(ts, 0.0)) * 100, 2),
            "gld_w_pct": round(float(w["gld"].get(ts, 0.0)) * 100, 2),
            "ief_n": int(cnt["ief"].get(ts, 0)), "gld_n": int(cnt["gld"].get(ts, 0)),
        })

    # 目前條件明細（最後一根「已收盤」的週五 bar）
    last_trade = cal[-1]
    latest = {}
    for k, a in (("ief", ief), ("gld", gld)):
        wk = e3_weekly(a)
        done = wk[wk.index <= last_trade]
        if done.empty:
            raise Abort(f"{k} 無已收盤週線")
        r = done.iloc[-1]
        latest[k] = {
            "week_date": str(done.index[-1].date()),
            "close": round(float(r["close"]), 2),
            "ma40": None if pd.isna(r["ma40"]) else round(float(r["ma40"]), 2),
            "ma52": None if pd.isna(r["ma52"]) else round(float(r["ma52"]), 2),
            "px52": None if pd.isna(r["px52"]) else round(float(r["px52"]), 2),
            "c_ma40": bool(r["c1"]), "c_ma52": bool(r["c2"]), "c_px52": bool(r["c3"]),
            "n": int(r["n"]),
            "target_w_pct": round(W_OVERLAY * int(r["n"]) / 3.0 * 100, 2),
            "applied_w_pct": round(float(w[k].iloc[-1]) * 100, 2),
            "last_close": round(float(a.iloc[-1]), 2), "last_close_date": str(a.index[-1].date()),
        }

    navs = {"main": [d["nav_main"] for d in daily], "cap10": [d["nav_cap10"] for d in daily],
            "c1": [d["nav_c1"] for d in daily]}
    dd = {k: drawdown_pct(v) for k, v in navs.items()}
    # 疊加對 NAV 的累計貢獻（C1 − cap 1.0）
    ov_contrib = round(daily[-1]["nav_c1"] - daily[-1]["nav_cap10"], 3)

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data_date": daily[-1]["date"],
        "inception": inception,
        "n_live_days": len(daily),
        "mechanism": ("C1 shadow: stock part = cap 1.0 (no borrowing, same W52 x adaptive sigma x A2 exec, clamp 50); "
                      "overlay = IEF <=20% + GLD <=20%, each weekly E3 (close>MA40w, >MA52w, >close 52w ago; 1/3 each), "
                      "signal t -> return from t+2; excess return vs ^IRX, roll 8bp/yr, 1bp/side"),
        "status": "SHADOW only (not adopted for live trading); side-by-side tracking vs live main system",
        "selfcheck_vs_scoreboard": sb_diff,
        "latest": latest,
        "overlay_contrib_nav_pts": ov_contrib,
        "daily": daily,
        "drawdown_pct": dd,
    }


# ═══════════════════════════════════════════════════════════════════════
# 頁面
# ═══════════════════════════════════════════════════════════════════════
def f1(x, sign=False):
    return (f"{x:+.1f}" if sign else f"{x:.1f}")


def cond_row(label, ok, val, thr):
    mark = "成立" if ok else "未成立"
    cls = "pos" if ok else "neg"
    return (f"<tr><td>{label}</td><td class='num'>{val}</td><td class='num'>{thr}</td>"
            f"<td><span class='{cls}'>{mark}</span></td></tr>")


def cond_table(name, lat):
    rows = "".join([
        cond_row("週收 &gt; 40 週均", lat["c_ma40"], f"{lat['close']:.2f}", "—" if lat["ma40"] is None else f"{lat['ma40']:.2f}"),
        cond_row("週收 &gt; 52 週均", lat["c_ma52"], f"{lat['close']:.2f}", "—" if lat["ma52"] is None else f"{lat['ma52']:.2f}"),
        cond_row("週收 &gt; 52 週前", lat["c_px52"], f"{lat['close']:.2f}", "—" if lat["px52"] is None else f"{lat['px52']:.2f}"),
    ])
    return (f"<div class='card'><h3>{name}：目前 {lat['n']}／3 條成立（週線截至 {lat['week_date']}）</h3>"
            f"<table><thead><tr><th>條件</th><th class='num'>週收盤</th><th class='num'>門檻</th><th>狀態</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
            f"<div class='takeaway'>依條件數換算的目標權重 {lat['target_w_pct']:.1f}%；"
            f"依研究規則延後兩個交易日生效，今天實際計入的權重為 {lat['applied_w_pct']:.1f}%。</div></div>")


def stats_row(label, s, hl=False):
    cls = " class='rowhl'" if hl else ""
    return (f"<tr{cls}><td>{label}</td><td class='num'>{s['cagr']:.1f}%</td><td class='num'>{s['mdd']:.1f}%</td>"
            f"<td class='num'>{s['ulcer']:.2f}</td><td class='num'>{s['uw10_frac']:.0f}%</td></tr>")


def render(st: dict, bt: dict) -> str:
    d = st["daily"]
    last = d[-1]
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    ret = {k: last[f"nav_{k}"] - 100.0 for k in ("main", "cap10", "c1")}
    dd_now = {k: st["drawdown_pct"][k][-1] for k in ("main", "cap10", "c1")}
    dd_min = {k: min(st["drawdown_pct"][k]) for k in ("main", "cap10", "c1")}
    ief, gld = st["latest"]["ief"], st["latest"]["gld"]
    s_bt = bt["stats_daily_wfri"]
    med = bt["anchor_median"]
    live_data = {
        "dates": [r["date"] for r in d],
        "main": [r["nav_main"] for r in d], "cap10": [r["nav_cap10"] for r in d], "c1": [r["nav_c1"] for r in d],
        "dd_main": st["drawdown_pct"]["main"], "dd_cap10": st["drawdown_pct"]["cap10"], "dd_c1": st["drawdown_pct"]["c1"],
        "stock_main": [r["stock_main_pct"] for r in d], "stock_c1": [r["stock_c1_pct"] for r in d],
        "ief_w": [r["ief_w_pct"] for r in d], "gld_w": [r["gld_w_pct"] for r in d],
    }
    bt_dd = {}
    for k in ("nav_c1", "nav_c0", "nav_bh"):
        peak, out = -1e18, []
        for v in bt[k]:
            peak = max(peak, v)
            out.append(round((v / peak - 1.0) * 100.0, 2))
        bt_dd[k] = out
    bt_data = {
        "dates": bt["dates"], "c1": bt["nav_c1"], "c0": bt["nav_c0"], "bh": bt["nav_bh"],
        "dd_c1": bt_dd["nav_c1"], "dd_c0": bt_dd["nav_c0"], "dd_bh": bt_dd["nav_bh"],
        "ief_n": bt["ief_cond"], "gld_n": bt["gld_cond"],
    }
    stress_rows = ""
    for lab, v in bt["stress"].items():
        stress_rows += (f"<tr><td>{lab}</td><td class='num'>{v['C0']['ret']:+.1f}%</td><td class='num'>{v['C1']['ret']:+.1f}%</td>"
                        f"<td class='num'>{v['C0']['mdd']:.1f}%</td><td class='num'>{v['C1']['mdd']:.1f}%</td></tr>")
    era_rows = ""
    for lab, v in bt["eras"].items():
        era_rows += (f"<tr><td>{lab}</td><td class='num'>{v['C0']['ulcer']:.2f}</td><td class='num'>{v['C1']['ulcer']:.2f}</td>"
                     f"<td class='num'>{v['C0']['cagr']:.1f}%</td><td class='num'>{v['C1']['cagr']:.1f}%</td></tr>")

    nav_html = full_nav_block("system", "lthub") if full_nav_block else ""
    sb = st.get("selfcheck_vs_scoreboard") or {}
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>債金版影子對照｜實盤未採用，僅並排追蹤 | InvestMQuest Research</title>
  <meta name="description" content="美股債金版影子對照：股票部分 cap 1.0 不借錢，加 IEF／GLD 週線趨勢疊加；與實單主系統並排追蹤，實盤未採用。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/imq-base.css">
  <script src="https://cdn.jsdelivr.net/npm/lightweight-charts@4.2.3/dist/lightweight-charts.standalone.production.js"></script>
  <style>
:root{{--brand:#0d2244;--bg:#f7f3ea;--card:#ffffff;--text:#0c1521;--muted:#6b7686;--border:#e5dfd0;
  --green:#15803d;--red:#b91c1c;--amber:#a16207;--blue:#1d4ed8}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--sans),-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.65;font-size:14px}}
a{{color:var(--brand);text-decoration:none}}a:hover{{text-decoration:underline}}
.container{{max-width:1140px;margin:0 auto;padding:0 1.5rem}}
.page-hdr{{padding:1.5rem 0 1.2rem;background:var(--card);border-bottom:1px solid var(--border)}}
.page-hdr h1{{font-family:var(--serif);font-size:1.5rem;font-weight:700;letter-spacing:-.01em}}
.page-hdr .sub{{color:var(--muted);font-size:.85rem;margin-top:.2rem}}
.crumb{{font-size:.8rem;color:var(--muted);margin-bottom:.35rem}}.crumb a{{color:var(--muted)}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--r,10px);padding:1.25rem;margin:1rem 0;box-shadow:var(--sh-1,none)}}
.card h2{{font-size:1.05rem;font-weight:700;margin-bottom:.4rem}}
.card h3{{font-size:.95rem;font-weight:600;margin-bottom:.75rem}}
.takeaway{{font-size:.82rem;margin-top:.75rem;padding:.6rem .9rem;border-radius:8px;background:#f6f8fb;border-left:3px solid var(--brand)}}
.banner{{background:#fff7e0;border:1px solid #e8d49a;border-radius:10px;padding:.8rem 1.1rem;margin:1rem 0;font-size:.88rem}}
.banner b.tag{{display:inline-block;background:var(--amber);color:#fff;border-radius:4px;padding:.05rem .5rem;margin-right:.5rem;font-size:.78rem}}
.phase{{display:inline-block;font-size:.74rem;font-weight:700;border-radius:4px;padding:.1rem .55rem;margin-right:.5rem;vertical-align:middle}}
.phase.live{{background:#e6f4ea;color:var(--green)}}.phase.bt{{background:#e8eef5;color:var(--blue)}}
table{{width:100%;border-collapse:collapse;font-size:.82rem}}
th,td{{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--border)}}
th{{font-family:var(--mono);font-weight:600;font-size:.72rem;color:var(--muted)}}
td{{font-variant-numeric:tabular-nums}}td.num,th.num{{text-align:right}}
.pos{{color:var(--green);font-weight:600}}.neg{{color:var(--red);font-weight:600}}
.rowhl td{{background:#eef3fb;font-weight:600}}
.tiles{{display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem;margin:1rem 0}}
.tile{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.8rem 1rem}}
.tile .k{{font-size:.74rem;color:var(--muted)}}.tile .v{{font-size:1.45rem;font-weight:800;letter-spacing:-.02em;line-height:1.25}}.tile .s{{font-size:.74rem;color:var(--muted)}}
.chart{{width:100%;height:300px;position:relative}}
.chart-sm{{width:100%;height:220px;position:relative}}
.legend{{display:flex;gap:1rem;flex-wrap:wrap;font-size:.78rem;color:var(--muted);margin:.4rem 0}}
.legend i{{display:inline-block;width:18px;height:0;border-top:3px solid;vertical-align:middle;margin-right:.3rem}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
.small{{font-size:.78rem;color:var(--muted)}}
.tablewrap{{overflow-x:auto}}
@media(max-width:768px){{.container{{padding:0 1rem}}.tiles{{grid-template-columns:1fr 1fr}}.grid2{{grid-template-columns:1fr}}.chart{{height:260px}}table{{font-size:.74rem}}th,td{{padding:.4rem .4rem}}}}
  </style>
</head>
<body>
{nav_html}
<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/long-track/#live">系統主控台</a> / <a href="/long-track-w52-adaptive/">實單主系統</a> / 債金版影子對照</div>
    <h1>債金版影子對照（美股）</h1>
    <div class="sub">股票部分上限 100% 不借錢，另疊 IEF、GLD 週線趨勢 · 與實單主系統並排追蹤 · 無 email</div>
  </div>
</div>
<div class="container">

<div class="banner"><b class="tag">實盤未採用</b>債金版只在這裡並排追蹤，實盤不動、不下單、不構成任何配置建議。數據截至 {last['date']}，頁面更新 {now} 台北時間。</div>

<div class="card">
<h2>債金版是什麼</h2>
<p>股票部分沿用現行引擎（週線 W52 閘門 × 自適應波動率 × 執行層），但曝險上限收回 100%，不借錢。另外各拿最多 20% 的資金配置 IEF（美國 7–10 年公債）與 GLD（黃金），每個資產看週線三個條件：週收盤高於 40 週均線、高於 52 週均線、高於 52 週前的價格。每成立一條，配置加三分之一，三條全成立才是 20%。條件成立與否在週五收盤判定，延後兩個交易日生效。</p>
<p class="small" style="margin-top:.5rem">疊加部分以超額報酬計（資產報酬減短期利率），已扣 roll 成本與換手成本。定義全部照抄 v7-backtest 的研究程式（src/pain_reduction），沒有調任何參數。</p>
</div>

<h2 style="margin:1.4rem 0 .2rem;font-size:1.15rem"><span class="phase live">上線後追蹤</span>{st['inception']} 起，每交易日更新</h2>
<p class="small">起點與實單主系統相同（淨值 100），三條線用同一套日報酬簿記與同一份實錄執行層算出，因此可以直接並排。下方回測是另一段口徑，不與這裡混看。</p>

<div class="tiles">
  <div class="tile"><div class="k">債金版累計報酬（{st['n_live_days']} 個交易日）</div><div class="v">{ret['c1']:+.1f}%</div><div class="s">實盤 {ret['main']:+.1f}% · cap 1.0 影子 {ret['cap10']:+.1f}%</div></div>
  <div class="tile"><div class="k">目前自高點回撤</div><div class="v">{dd_now['c1']:.1f}%</div><div class="s">實盤 {dd_now['main']:.1f}% · 追蹤期最深債金版 {dd_min['c1']:.1f}% 對實盤 {dd_min['main']:.1f}%</div></div>
  <div class="tile"><div class="k">IEF 條件數／今日權重</div><div class="v">{ief['n']}／3 · {ief['applied_w_pct']:.1f}%</div><div class="s">目標權重 {ief['target_w_pct']:.1f}%（週線截至 {ief['week_date']}）</div></div>
  <div class="tile"><div class="k">GLD 條件數／今日權重</div><div class="v">{gld['n']}／3 · {gld['applied_w_pct']:.1f}%</div><div class="s">目標權重 {gld['target_w_pct']:.1f}%（週線截至 {gld['week_date']}）</div></div>
</div>

<div class="card">
<h3>淨值對照（起點 100）</h3>
<div class="legend"><span><i style="border-color:#1d4ed8"></i>債金版（不借錢＋IEF／GLD）</span><span><i style="border-color:#0c1521"></i>實單主系統</span><span><i style="border-color:#d97706;border-top-style:dashed"></i>cap 1.0 影子（未疊加）</span></div>
<div id="ch-live-nav" class="chart"></div>
<div class="takeaway">到 {last['date']}，債金版為 {last['nav_c1']:.1f}，實單主系統為 {last['nav_main']:.1f}，只有股票部分的 cap 1.0 影子為 {last['nav_cap10']:.1f}。債金版與 cap 1.0 影子的差距（{ret['c1'] - ret['cap10']:+.1f}）就是 IEF、GLD 疊加累計貢獻的淨值點數。追蹤期很短，只能看運作是否如預期，不能據此比較優劣。</div>
</div>

<div class="grid2">
<div class="card">
<h3>回撤對照（自追蹤期高點）</h3>
<div class="legend"><span><i style="border-color:#1d4ed8"></i>債金版</span><span><i style="border-color:#0c1521"></i>實單主系統</span></div>
<div id="ch-live-dd" class="chart-sm"></div>
</div>
<div class="card">
<h3>股票曝險與債金權重（% 淨值）</h3>
<div class="legend"><span><i style="border-color:#0c1521"></i>實單股票曝險</span><span><i style="border-color:#1d4ed8"></i>債金版股票曝險</span><span><i style="border-color:#15803d"></i>IEF 權重</span><span><i style="border-color:#d97706"></i>GLD 權重</span></div>
<div id="ch-live-expo" class="chart-sm"></div>
</div>
</div>

<div class="grid2">
{cond_table('IEF', ief)}
{cond_table('GLD', gld)}
</div>

<h2 style="margin:1.8rem 0 .2rem;font-size:1.15rem"><span class="phase bt">研究期回測</span>{bt['window'][0]} ～ {bt['window'][1]}，凍結的歷史曲線</h2>
<p class="small">由研究程式一次產生（週五錨點），不隨每日資料重算。回測用的是研究引擎的日報酬，與上方追蹤段的實錄執行層口徑不同；兩段在 {st['inception']} 之後的日曆時間有重疊，但數字來源不同，請分開看。</p>

<div class="card">
<h3>回測淨值（起點 100，對數座標）</h3>
<div class="legend"><span><i style="border-color:#1d4ed8"></i>債金版</span><span><i style="border-color:#0c1521"></i>現行規則（cap 1.5 ＋ 均線層）</span><span><i style="border-color:#9aa7b8"></i>50/50 買進持有</span></div>
<div id="ch-bt-nav" class="chart"></div>
</div>
<div class="grid2">
<div class="card">
<h3>回測回撤</h3>
<div id="ch-bt-dd" class="chart-sm"></div>
</div>
<div class="card">
<h3>回測期 IEF／GLD 週線條件數</h3>
<div class="legend"><span><i style="border-color:#15803d"></i>IEF</span><span><i style="border-color:#d97706"></i>GLD</span></div>
<div id="ch-bt-cond" class="chart-sm"></div>
</div>
</div>

<div class="card">
<h3>回測統計</h3>
<div class="tablewrap"><table>
<thead><tr><th>規則</th><th class="num">年化</th><th class="num">最大回撤</th><th class="num">Ulcer</th><th class="num">低於前高 10% 的時間</th></tr></thead>
<tbody>
{stats_row('債金版（W-FRI 錨點，日頻）', s_bt['C1'], True)}
{stats_row('現行規則（W-FRI 錨點，日頻）', s_bt['C0'])}
{stats_row('50/50 買進持有', s_bt['BH'])}
{stats_row('債金版（五個週線錨點中位數）', med['C1'])}
{stats_row('現行規則（五個週線錨點中位數）', med['C0'])}
</tbody></table></div>
<div class="takeaway">五個週線錨點（週一至週五收盤各算一次）的中位數：債金版年化 {med['C1']['cagr']:.1f}%、Ulcer {med['C1']['ulcer']:.1f}，現行規則年化 {med['C0']['cagr']:.1f}%、Ulcer {med['C0']['ulcer']:.1f}。Ulcer 是回撤深度與時間的綜合指標，數字越低代表持有過程越平順。</div>
</div>

<div class="grid2">
<div class="card">
<h3>升息與壓力期（W-FRI 錨點）</h3>
<div class="tablewrap"><table>
<thead><tr><th>期間</th><th class="num">現行報酬</th><th class="num">債金版報酬</th><th class="num">現行回撤</th><th class="num">債金版回撤</th></tr></thead>
<tbody>{stress_rows}</tbody></table></div>
<div class="takeaway">2022 年 1 月至 2023 年 10 月的升息期，債金版報酬為 {bt['stress']['升息 2022-01～2023-10']['C1']['ret']:+.1f}%，現行規則為 {bt['stress']['升息 2022-01～2023-10']['C0']['ret']:+.1f}%。債券與股票同時下跌時，債金疊加沒有保護作用，這是債金版最明確的弱點。</div>
</div>
<div class="card">
<h3>分期（W-FRI 錨點）</h3>
<div class="tablewrap"><table>
<thead><tr><th>期間</th><th class="num">現行 Ulcer</th><th class="num">債金版 Ulcer</th><th class="num">現行年化</th><th class="num">債金版年化</th></tr></thead>
<tbody>{era_rows}</tbody></table></div>
</div>
</div>

<div class="card">
<h3>讀這條線前要知道的事</h3>
<ul style="margin-left:1.2rem;font-size:.86rem">
<li>事前登記的六條判準全數通過（年化不低於現行 1pp、最大回撤不惡化超過 2pp、Ulcer 至少低 20%、低於前高 10% 的時間較短、五個分期至少三個不劣於現行、2022 年回撤不惡化超過 3pp）。</li>
<li>W-FRI 錨點的全窗數字在門檻定案前已看過，所以那一欄不算新證據；新資訊來自五個錨點、分期、壓力期與單一資產拆解。</li>
<li>債券與黃金在 2005 至 2026 年整體是順風，結論只在這段樣本內成立，也只測了美股。</li>
<li>疊加部位的資金成本若比短期利率高 1.5%，債金版的年化仍比現行高約 0.3 個百分點（研究敏感度測試）。</li>
<li>追蹤期只有 {st['n_live_days']} 個交易日，不足以判斷任何優劣；本頁只回答「並排看起來如何」。</li>
</ul>
<p class="small" style="margin-top:.6rem">資料：QQQ、SMH、IEF、GLD 為還原股價，現金利率用 ^IRX（yfinance）。自檢：本頁重算的實單與 cap 1.0 影子淨值，與記分板發布值最大差 {('%.4f' % sb.get('main_vs_scoreboard_max_abs', 0)) if sb else '—'}／{('%.4f' % sb.get('a10_vs_scoreboard_max_abs', 0)) if sb else '—'}（淨值點）。</p>
</div>

</div>
<script>
var LIVE={json.dumps(live_data, ensure_ascii=False, separators=(',', ':'))};
var BT={json.dumps(bt_data, ensure_ascii=False, separators=(',', ':'))};
(function(){{
  function opts(el, log){{ return {{width: el.clientWidth, height: el.clientHeight,
    layout:{{background:{{color:'transparent'}}, textColor:'#0c1521', fontSize:11}},
    grid:{{vertLines:{{color:'rgba(0,0,0,0.05)'}}, horzLines:{{color:'rgba(0,0,0,0.05)'}}}},
    rightPriceScale:{{borderColor:'#e5dfd0', mode: log?1:0}}, timeScale:{{borderColor:'#e5dfd0', timeVisible:false}},
    crosshair:{{mode:0}}, localization:{{locale:'zh-TW'}} }}; }}
  function pts(dates, vals){{ var o=[]; for(var i=0;i<dates.length;i++){{ o.push({{time:dates[i], value:vals[i]}}); }} return o; }}
  function mk(id, log){{ var el=document.getElementById(id); var c=LightweightCharts.createChart(el, opts(el, log));
    new ResizeObserver(function(){{ c.applyOptions({{width: el.clientWidth}}); }}).observe(el); return c; }}
  function line(c, color, data, w, dashed){{ var s=c.addLineSeries({{color:color, lineWidth:w||2, priceLineVisible:false, lastValueVisible:true,
      lineStyle: dashed?2:0}}); s.setData(data); return s; }}
  var c1=mk('ch-live-nav', false);
  line(c1,'#d97706',pts(LIVE.dates,LIVE.cap10),1,true); line(c1,'#0c1521',pts(LIVE.dates,LIVE.main),2); line(c1,'#1d4ed8',pts(LIVE.dates,LIVE.c1),2);
  c1.timeScale().fitContent();
  var c2=mk('ch-live-dd', false);
  line(c2,'#0c1521',pts(LIVE.dates,LIVE.dd_main),2); line(c2,'#1d4ed8',pts(LIVE.dates,LIVE.dd_c1),2); c2.timeScale().fitContent();
  var c3=mk('ch-live-expo', false);
  line(c3,'#0c1521',pts(LIVE.dates,LIVE.stock_main),2); line(c3,'#1d4ed8',pts(LIVE.dates,LIVE.stock_c1),2);
  line(c3,'#15803d',pts(LIVE.dates,LIVE.ief_w),2); line(c3,'#d97706',pts(LIVE.dates,LIVE.gld_w),2); c3.timeScale().fitContent();
  var b1=mk('ch-bt-nav', true);
  line(b1,'#9aa7b8',pts(BT.dates,BT.bh),1); line(b1,'#0c1521',pts(BT.dates,BT.c0),2); line(b1,'#1d4ed8',pts(BT.dates,BT.c1),2); b1.timeScale().fitContent();
  var b2=mk('ch-bt-dd', false);
  line(b2,'#0c1521',pts(BT.dates,BT.dd_c0),1); line(b2,'#1d4ed8',pts(BT.dates,BT.dd_c1),1); b2.timeScale().fitContent();
  var b3=mk('ch-bt-cond', false);
  line(b3,'#15803d',pts(BT.dates,BT.ief_n),1); line(b3,'#d97706',pts(BT.dates,BT.gld_n),1); b3.timeScale().fitContent();
}})();
</script>
</body>
</html>
"""


def main():
    try:
        st = build()
        bt = json.loads(BT_JSON.read_text(encoding="utf-8"))
        html = render(st, bt)
    except Abort as e:
        print(f"  ✗ fail-safe: {e} — outputs left unchanged")
        sys.exit(0)
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        print(f"  ✗ build failed ({type(e).__name__}: {e}) — outputs left unchanged")
        sys.exit(0)
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    last = st["daily"][-1]
    info(f"wrote {OUT_HTML.name} ({len(html):,} bytes), {OUT_STATE.name}；"
         f"{last['date']} 債金版={last['nav_c1']} 實盤={last['nav_main']} cap1.0={last['nav_cap10']}；"
         f"IEF {st['latest']['ief']['n']}/3 GLD {st['latest']['gld']['n']}/3")


if __name__ == "__main__":
    main()
