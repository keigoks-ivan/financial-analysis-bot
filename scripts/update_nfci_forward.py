#!/usr/bin/env python3
"""NFCI 紅燈減半往前測：影子線每日計算
================================================================================
事前登記：v7-backtest docs/NFCI_Forward_Prereg.md（2026-10-18，持有人確認；起始日 2026-10-19，
判定日最早 2029-10-19）。規則一字不改，本檔只是照登記實作：

  紅綠燈  每週三公布的 NFCI，取該版最後一筆與同版四週前的值（各取兩位小數），高於＝紅，相等算綠。
          週三公布、週四收盤調整、週五起生效；週四休市就順延到下一個交易日。
  影子線  紅燈時每檔目標水位＝實單目標水位 × 0.5，綠燈＝實單目標；執行層、成本、現金利率、成交時序全部
          沿用實單程式。美股只改 QQQ、SMH（公債、黃金兩腿照實單，不在這裡比），台股改 0050、2330。
  起始    2026-10-19 當天收盤，影子線的持股＝實單的持股；起始顏色用 2026-10-14 公布的那一版（紅）。

實單的計算一律 import 實單程式，不複製、不改寫：
  update_long_track_w52_adaptive  fetch_close（取價）、band_exec_replay（實單現持）、
                                  next_exec（執行層單日更新：加碼 20pp／減碼門檻依 exec_down_band_for、10% 取整、單腿 clamp）、
                                  exec_clamp_for（依紀錄的規則標籤取 clamp）
  build_live_scoreboard           leg_daily_returns_generic／nav_from_returns（實單追蹤的淨值簿記：
                                  前日現持 × 當日報酬、現金利率、換手 7 bps）、fetch_us_cash_series、MARKETS
影子線與實單用同一個簿記函式、同一份價格，唯一差別是目標權重在紅燈時乘 0.5。

輸入  docs/long-track-w52-adaptive/state.json 的 history_us／history_tw（實單每日目標）
      docs/long-track/data/nfci_releases.csv（每週三公布值存檔，只增不改）
輸出  docs/long-track/data/nfci_forward_state.json（影子線狀態，每次由存檔與實單紀錄整段重算）

每週存檔：週三版本在週四（UTC）起才抓，用 ALFRED 的 vintage_date＝該週三（得到當天有效的版本；
遇假日 NFCI 週四才公布時，週三版本就是前一週的值，登記規則取週三版本，不另補）。抓得到的當週
存檔記「當週存檔」，過了週四才補到的記「事後補抓（ALFRED）」並在備註寫明。
公開檔不放帳戶結構或金額。判定日之前只顯示累積中的數字，不提前判。
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import traceback
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import update_long_track_w52_adaptive as _w52  # noqa: E402  實單：取價／現持／執行層
import build_live_scoreboard as _lsb  # noqa: E402  實單追蹤：淨值簿記

# ── 事前登記的常數（不得調整）──────────────────────────────────────────────
START_DATE = "2026-10-19"
SEED_VINTAGE = "2026-10-14"          # 起始顏色用的那一版
EARLIEST_DECISION = "2029-10-19"
LATEST_DECISION = "2031-10-19"
RED_FACTOR = 0.5                     # 紅燈目標＝實單目標 × 0.5（乘 0.5 在浮點數是精確的）
NFCI_PREV_DAYS = 28                  # 四週前＝同一版中最後一筆往前 28 天（含）以前的最後一筆
CRASH_DROP_BP = 1000                 # 股災：從前高跌超過 10%（先四捨五入到 1 bp，再比 > 1000）
CRASH_BENEFIT_BP = 300               # 判準 1：影子線少跌 ≥ 3 個百分點（300 bp）
MIN_CRASHES = 3                      # 判定要求每個市場至少 3 次股災
CALMAR_KEEP_PCT = 95                 # 判準 2：影子線 Calmar ≥ 實單的 0.95 倍
ADJ_RATIO_MAX_X10 = 25               # 判準 3：每年調整次數 ≤ 實單的 2.5 倍
CALMAR_MIN_DAYS = 365                # 顯示用：未滿一年不年化（登記文件沒規定，純顯示選擇）

MARKET_INDEX_LEG = {"us": "QQQ", "tw": "0050"}   # 股災看的指數腿（還原收盤）
MARKET_LABEL = {"us": "美股", "tw": "台股"}

DOCS = _w52.DOCS
DATA_DIR = DOCS / "long-track" / "data"
RELEASES_CSV = DATA_DIR / "nfci_releases.csv"
STATE_OUT = DATA_DIR / "nfci_forward_state.json"
LIVE_STATE = _w52.STATE_JSON
SCOREBOARD_JSON = _lsb.OUT_JSON

ALFRED_URL = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=NFCI&vintage_date={d}"
RELEASE_COLS = ["release_date", "last_obs_date", "value", "value_2dp", "value_4w_ago_date",
                "value_4w_ago", "value_4w_ago_2dp", "color", "captured_on", "source", "note"]


class Abort(Exception):
    pass


def warn(msg: str) -> None:
    print(f"[nfci-forward][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[nfci-forward] {msg}")


# ═══════════════════════════════════════════════════════════════════════
# 紅綠燈
# ═══════════════════════════════════════════════════════════════════════
def hundredths(v) -> int:
    """兩位小數後的整數百分位（-0.49 → -49）。取兩位小數的方式與 10-17 回測
    （experiments/nfci_overlay/run_nfci.py color_at）相同：round(float(x), 2)。"""
    return int(round(round(float(v), 2) * 100))


def nfci_color(value, value_4w_ago) -> str:
    """高於四週前＝紅，相等或較低＝綠。整數百分位比較。"""
    return "red" if hundredths(value) > hundredths(value_4w_ago) else "green"


def parse_vintage(text: str) -> list:
    """ALFRED／FRED graph csv → [(觀測日, 值字串)]，依日期排序，略過空值。"""
    r = csv.reader(io.StringIO(text))
    header = next(r, None)
    if not header or header[0] != "observation_date":
        raise ValueError("不是 ALFRED/FRED graph csv")
    rows = [(row[0], row[1].strip()) for row in r
            if len(row) >= 2 and row[1].strip() not in ("", ".")]
    rows.sort(key=lambda x: x[0])
    return rows


def release_from_vintage(vintage_date: str, obs: list, captured_on: str, source: str, note: str = "") -> dict:
    """一份當週版本 → 存檔一列。四週前＝同一版中、最後一筆觀測日往前 28 天（含）以前的最後一筆。"""
    if not obs:
        raise ValueError("版本沒有任何觀測值")
    last_d, last_v = obs[-1]
    cutoff = (date.fromisoformat(last_d) - timedelta(days=NFCI_PREV_DAYS)).isoformat()
    prev = [o for o in obs if o[0] <= cutoff]
    if not prev:
        raise ValueError("版本沒有四週前的值")
    prev_d, prev_v = prev[-1]
    return {
        "release_date": vintage_date, "last_obs_date": last_d,
        "value": last_v, "value_2dp": f"{round(float(last_v), 2):.2f}",
        "value_4w_ago_date": prev_d, "value_4w_ago": prev_v,
        "value_4w_ago_2dp": f"{round(float(prev_v), 2):.2f}",
        "color": nfci_color(last_v, prev_v),
        "captured_on": captured_on, "source": source, "note": note,
    }


def fetch_alfred_vintage(vintage_date: str, retries: int = 3, timeout: int = 45):
    """ALFRED 在 vintage_date 當天有效的 NFCI 版本（含當時完整歷史）；抓不到回 None。"""
    url = ALFRED_URL.format(d=vintage_date)
    for k in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; investmquest-nfci/1.0)"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                text = resp.read().decode("utf-8")
            if text.startswith("observation_date"):
                return text
            warn(f"ALFRED {vintage_date} 回應格式不對（第 {k + 1} 次）")
        except Exception as e:  # noqa: BLE001
            warn(f"ALFRED {vintage_date} 抓取失敗（第 {k + 1} 次）：{type(e).__name__}: {e}")
        time.sleep(2 + 3 * k)
    return None


def due_wednesdays(seed: str, today: date) -> list:
    """起始版本之後，每個「公布日隔天（UTC）已到」的週三。週三版本要等到週四才抓。"""
    out, w = [], date.fromisoformat(seed)
    while w + timedelta(days=1) <= today:
        out.append(w.isoformat())
        w += timedelta(days=7)
    return out


def load_releases(path: Path) -> list:
    """讀存檔並檢查每列的顏色與兩位小數值一致；依公布日排序。檔案不存在回空串列。"""
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        want = nfci_color(r["value_2dp"], r["value_4w_ago_2dp"])
        if r["color"] != want:
            raise Abort(f"存檔 {r['release_date']} 的顏色（{r['color']}）與兩位小數值不一致（應為 {want}）")
    rows.sort(key=lambda r: r["release_date"])
    return rows


def append_release(path: Path, row: dict) -> None:
    """只增不改：以附加方式寫，已存在的列一個位元組都不動。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=RELEASE_COLS, lineterminator="\n")
        if new_file:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in RELEASE_COLS})


def capture_missing(path: Path, seed: str, today: date, fetch=fetch_alfred_vintage) -> dict:
    """補上存檔裡還沒有的週三版本。回傳 {'added': [...], 'missing': [...]}。"""
    have = {r["release_date"] for r in load_releases(path)}
    added, missing = [], []
    for w in due_wednesdays(seed, today):
        if w in have:
            continue
        text = fetch(w)
        if text is None:
            missing.append(w)
            continue
        try:
            obs = parse_vintage(text)
            last_d = obs[-1][0]
            gap = (date.fromisoformat(w) - date.fromisoformat(last_d)).days
            if gap < 0 or gap > 20:
                raise ValueError(f"最後一筆觀測日 {last_d} 離公布日 {w} 差 {gap} 天，版本不對")
            if w == seed:
                source, note = "起始版本", "登記文件指定的起始顏色版本（ALFRED vintage_date＝公布日）"
            elif today <= date.fromisoformat(w) + timedelta(days=1):
                source, note = "當週存檔", ""
            else:
                source, note = "事後補抓（ALFRED）", f"CI 當週沒存到，{today.isoformat()} 用 ALFRED 補抓 {w} 的版本"
            if gap > 6:
                note = (note + "；" if note else "") + f"最後一筆離公布日 {gap} 天，這一版沒有新一週的值（依登記規則仍取週三版本）"
            row = release_from_vintage(w, obs, today.isoformat(), source, note)
        except (ValueError, IndexError) as e:
            warn(f"{w} 的版本不能用：{e}")
            missing.append(w)
            continue
        append_release(path, row)
        added.append(w)
        info(f"存檔 {w}：最後一筆 {row['last_obs_date']} {row['value_2dp']}，四週前 {row['value_4w_ago_2dp']}，{row['color']}（{row['source']}）")
    return {"added": added, "missing": missing}


def release_for_day(releases: list, d: str):
    """交易日 d 適用的版本：公布日 + 1 天 <= d 的最後一版（週三公布，週四收盤起用）。
    週四休市時 d 最早是下一個交易日，同一條式子自然順延。"""
    dd = date.fromisoformat(d)
    best = None
    for r in releases:
        if date.fromisoformat(r["release_date"]) + timedelta(days=1) <= dd:
            best = r
    return best


def adjust_date(release_date: str, trading_days: list):
    """公布日隔天起第一個交易日＝調整日（週四；休市則順延）。沒有就回 None。"""
    t = (date.fromisoformat(release_date) + timedelta(days=1)).isoformat()
    for d in sorted(trading_days):
        if d >= t:
            return d
    return None


def effective_date(release_date: str, trading_days: list):
    """調整日的下一個交易日＝新持股開始承擔報酬的第一天（週五）。"""
    a = adjust_date(release_date, trading_days)
    if a is None:
        return None
    for d in sorted(trading_days):
        if d > a:
            return d
    return None


# ═══════════════════════════════════════════════════════════════════════
# 影子線模擬（實單的計算全部 import 自實單程式）
# ═══════════════════════════════════════════════════════════════════════
def simulate_market(mkt: dict, history: list, start_date: str, release_fn, px: dict, px_dates: dict,
                    irx: dict, irx_dates: list, force_color: str | None = None) -> dict | None:
    """起始日之後逐日重放：影子線目標＝實單當日目標（紅燈 × 0.5），現持用 _w52.next_exec 更新，
    淨值用 _lsb.leg_daily_returns_generic／nav_from_returns（與實單同一個簿記函式）。
    起始日當天影子線的現持＝實單當天收盤後的現持。起始日之前沒有紀錄時回 None。"""
    legs = mkt["legs"]
    hist = sorted(history, key=lambda r: r["date"])
    dates = [r["date"] for r in hist]
    start_idx = next((i for i, d in enumerate(dates) if d >= start_date), None)
    if start_idx is None:
        return None
    if start_idx == 0:
        raise Abort("實單紀錄從起始日就開頭，缺前一日現持，無法簿記")

    live_ex = _w52.band_exec_replay(hist, legs)["executed"]
    sh_ex = {t: list(live_ex[t]) for t in legs}     # 起始日（含）之前與實單相同
    held = {t: live_ex[t][start_idx] for t in legs}
    live_target = {t: [None] * len(hist) for t in legs}
    sh_target = {t: [None] * len(hist) for t in legs}
    color = [None] * len(hist)

    def day_color(d):
        if force_color:
            return force_color
        rel = release_fn(d)
        return rel["color"] if rel else None

    color[start_idx] = day_color(dates[start_idx])
    for i in range(start_idx + 1, len(hist)):
        c = day_color(dates[i])
        if c is None:
            raise Abort(f"{dates[i]} 沒有適用的 NFCI 版本")
        color[i] = c
        for t in legs:
            tk = hist[i]["tickers"][t]
            lt = float(tk["final_pct"])
            st = lt * RED_FACTOR if c == "red" else lt
            live_target[t][i], sh_target[t][i] = lt, st
            # 執行層照實單（登記檔：執行層照實單）：2026-11-02 起實單減碼門檻 10pp，影子線跟著用
            held[t] = _w52.next_exec(held[t], st, _w52.exec_clamp_for(tk), _w52.exec_down_band_for(tk, dates[i]))
            sh_ex[t][i] = held[t]

    live_dates = dates[start_idx:]
    date_to_idx = {d: i for i, d in enumerate(dates)}
    gaps: list = []
    rows_live = _lsb.leg_daily_returns_generic(mkt, legs, hist, live_dates, date_to_idx, live_ex, px, px_dates,
                                               irx, irx_dates, gaps, "NFCI-live")
    rows_sh = _lsb.leg_daily_returns_generic(mkt, legs, hist, live_dates, date_to_idx, sh_ex, px, px_dates,
                                             irx, irx_dates, gaps, "NFCI-shadow")
    nav_live = _lsb.nav_from_returns(rows_live, live_dates[0])
    nav_sh = _lsb.nav_from_returns(rows_sh, live_dates[0])
    return {
        "mkt": mkt, "legs": legs, "dates": live_dates, "start_idx": start_idx, "gaps": gaps,
        "color": color[start_idx:],
        "nav_live": [r["nav"] for r in nav_live], "nav_shadow": [r["nav"] for r in nav_sh],
        "ex_live": {t: live_ex[t][start_idx:] for t in legs},
        "ex_shadow": {t: sh_ex[t][start_idx:] for t in legs},
        "target_live": {t: live_target[t][start_idx:] for t in legs},
        "target_shadow": {t: sh_target[t][start_idx:] for t in legs},
    }


# ═══════════════════════════════════════════════════════════════════════
# 指標（整數基點）
# ═══════════════════════════════════════════════════════════════════════
def drop_bp(peak: float, c: float) -> int:
    """從高點跌了幾個基點（四捨五入到 1 bp 的整數）。"""
    return int(round((peak - c) / peak * 10000))


def find_crashes(closes: list) -> list:
    """股災切分。高點＝起始日起的滾動最高收盤；跌幅（整數 bp）> 1000 開始一次股災，區間從那個高點
    當天起，到收盤回到（>=）該高點為止；還沒回到的算到最後一天（recovered＝False）。"""
    out = []
    if not closes:
        return out
    peak_i, peak_v = 0, closes[0]
    cur = None
    for i in range(1, len(closes)):
        c = closes[i]
        if cur is not None:
            cur["trough_bp"] = max(cur["trough_bp"], drop_bp(peak_v, c))
            if c >= peak_v:
                cur["end_i"], cur["recovered"] = i, True
                out.append(cur)
                cur = None
                peak_i, peak_v = i, c
        else:
            if c > peak_v:
                peak_i, peak_v = i, c
            elif drop_bp(peak_v, c) > CRASH_DROP_BP:
                cur = {"peak_i": peak_i, "end_i": None, "recovered": False, "trough_bp": drop_bp(peak_v, c)}
    if cur is not None:
        cur["end_i"] = len(closes) - 1
        out.append(cur)
    return out


def interval_depth_bp(nav: list, i0: int, i1: int) -> int:
    """區間 [i0, i1] 內、從 i0 當天淨值起算的最大回撤（正的整數 bp）：滾動高點從 i0 的淨值起，
    之後的淨值創高會抬高滾動高點。"""
    peak, worst = nav[i0], 0.0
    for v in nav[i0:i1 + 1]:
        peak = max(peak, v)
        worst = max(worst, (peak - v) / peak)
    return int(round(worst * 10000))


def crash_report(dates: list, closes: list, nav_live: list, nav_shadow: list) -> list:
    out = []
    for ep in find_crashes(closes):
        a, b = ep["peak_i"], ep["end_i"]
        dl, ds = interval_depth_bp(nav_live, a, b), interval_depth_bp(nav_shadow, a, b)
        out.append({"peak_date": dates[a], "end_date": dates[b], "recovered": ep["recovered"],
                    "index_depth_bp": ep["trough_bp"], "live_depth_bp": dl, "shadow_depth_bp": ds,
                    "benefit_bp": dl - ds})
    return out


def max_drawdown_bp(nav: list) -> int:
    peak, worst = nav[0], 0.0
    for v in nav:
        peak = max(peak, v)
        worst = max(worst, (peak - v) / peak)
    return int(round(worst * 10000))


def cagr_bp(nav: list, days: int):
    if days < 1 or nav[0] <= 0 or nav[-1] <= 0:
        return None
    return int(round(((nav[-1] / nav[0]) ** (365.25 / days) - 1.0) * 10000))


def count_adjustments(ex: dict) -> int:
    """各腿現持變動的次數合計（起始日不算；現持乘 100 轉整數 bp 後比）。"""
    n = 0
    for arr in ex.values():
        bp = [int(round(v * 100)) for v in arr]
        n += sum(1 for a, b in zip(bp, bp[1:]) if a != b)
    return n


# ── 三條判準（只在判定日之後才會輸出）────────────────────────────────────────
def required_crashes(n: int) -> int:
    """判準 1：至少三分之二，無條件進位（3 次要 2、4 次要 3、5 次要 4、6 次要 4）。整數運算。"""
    return (2 * n + 2) // 3


def crash_pass(benefits_bp: list) -> bool:
    n = len(benefits_bp)
    hits = sum(1 for b in benefits_bp if b >= CRASH_BENEFIT_BP)
    return n > 0 and hits >= required_crashes(n)


def calmar_pass(s_cagr_bp, s_mdd_bp, l_cagr_bp, l_mdd_bp):
    """影子 Calmar >= 0.95 × 實單 Calmar，兩邊乘開成整數比較（回撤基點皆 > 0 才有定義）。"""
    if None in (s_cagr_bp, l_cagr_bp) or s_mdd_bp <= 0 or l_mdd_bp <= 0:
        return None
    return 100 * s_cagr_bp * l_mdd_bp >= CALMAR_KEEP_PCT * l_cagr_bp * s_mdd_bp


def adj_pass(n_shadow: int, n_live: int):
    """影子線調整次數 <= 實單的 2.5 倍（兩者同一段期間，次數比即每年次數比）。"""
    if n_live == 0:
        return None if n_shadow else True
    return 10 * n_shadow <= ADJ_RATIO_MAX_X10 * n_live


def decision_status(asof: str, counts: dict) -> str:
    """判定日規則：最早 2029-10-19 且兩市場都至少 3 次股災；不夠就等，最晚 2031-10-19。"""
    if asof < EARLIEST_DECISION:
        return "累積中"
    if counts and all(n >= MIN_CRASHES for n in counts.values()) and len(counts) == len(MARKET_LABEL):
        return "可判定"
    if asof >= LATEST_DECISION:
        return "已到最晚判定日"
    return "股災次數不足，延後"


def market_metrics(sim: dict, closes: list) -> dict:
    dates, nl, ns = sim["dates"], sim["nav_live"], sim["nav_shadow"]
    days = (date.fromisoformat(dates[-1]) - date.fromisoformat(dates[0])).days
    crashes = crash_report(dates, closes, nl, ns)
    n_live, n_sh = count_adjustments(sim["ex_live"]), count_adjustments(sim["ex_shadow"])
    m = {
        "legs": sim["legs"], "index_leg": MARKET_INDEX_LEG[sim["mkt"]["key"]],
        "inception": dates[0], "data_through": dates[-1], "n_days": len(dates), "elapsed_days": days,
        "nav": {"live": round(nl[-1], 4), "shadow": round(ns[-1], 4)},
        "return_bp": {"live": int(round((nl[-1] / nl[0] - 1) * 10000)),
                      "shadow": int(round((ns[-1] / ns[0] - 1) * 10000))},
        "mdd_bp": {"live": max_drawdown_bp(nl), "shadow": max_drawdown_bp(ns)},
        "cagr_bp": {"live": cagr_bp(nl, days), "shadow": cagr_bp(ns, days)},
        "adjustments": {"live": n_live, "shadow": n_sh},
        "crashes": {"count": len(crashes), "required_hits": required_crashes(len(crashes)), "episodes": crashes},
        "exposure_now_pp": {"live": round(sum(sim["ex_live"][t][-1] for t in sim["legs"]), 1),
                            "shadow": round(sum(sim["ex_shadow"][t][-1] for t in sim["legs"]), 1)},
    }
    year_ok = days >= CALMAR_MIN_DAYS
    for k in ("live", "shadow"):
        mdd, cg = m["mdd_bp"][k], m["cagr_bp"][k]
        m.setdefault("calmar", {})[k] = round(cg / mdd, 3) if (year_ok and mdd > 0 and cg is not None) else None
    m["adjustments"]["ratio"] = round(n_sh / n_live, 2) if n_live else None
    return m


def criteria_for(m: dict) -> dict:
    ben = [e["benefit_bp"] for e in m["crashes"]["episodes"]]
    return {
        "crashes_enough": m["crashes"]["count"] >= MIN_CRASHES,
        "crash_rule": crash_pass(ben),
        "calmar_rule": calmar_pass(m["cagr_bp"]["shadow"], m["mdd_bp"]["shadow"],
                                   m["cagr_bp"]["live"], m["mdd_bp"]["live"]),
        "trade_rule": adj_pass(m["adjustments"]["shadow"], m["adjustments"]["live"]),
    }


# ═══════════════════════════════════════════════════════════════════════
# 輸出
# ═══════════════════════════════════════════════════════════════════════
def _compact_scalar_arrays(s: str) -> str:
    return re.sub(r"\[\s+([^\[\]{}]*?)\s+\]", lambda m: "[" + re.sub(r"\s+", " ", m.group(1)) + "]", s)


def dump_json(obj) -> str:
    return _compact_scalar_arrays(json.dumps(obj, ensure_ascii=False, indent=1)) + "\n"


def release_brief(r: dict | None) -> dict | None:
    if not r:
        return None
    return {"release_date": r["release_date"], "last_obs_date": r["last_obs_date"], "color": r["color"],
            "value": r["value_2dp"], "value_4w_ago": r["value_4w_ago_2dp"]}


def build_state(start_date: str, releases: list, cap: dict, market_sims: dict, closes: dict,
                selfcheck: dict | None, forced: str | None = None) -> dict:
    markets, counts, asof = {}, {}, None
    for key, sim in market_sims.items():
        if sim is None:
            continue
        m = market_metrics(sim, closes[key])
        m["daily"] = {
            "dates": sim["dates"], "color": sim["color"],
            "nav_live": sim["nav_live"], "nav_shadow": sim["nav_shadow"],
            "exposure_live_pp": [round(sum(sim["ex_live"][t][i] for t in sim["legs"]), 1) for i in range(len(sim["dates"]))],
            "exposure_shadow_pp": [round(sum(sim["ex_shadow"][t][i] for t in sim["legs"]), 1) for i in range(len(sim["dates"]))],
        }
        markets[key] = m
        counts[key] = m["crashes"]["count"]
        asof = max(asof or "", m["data_through"])
    cur_rel = release_for_day(releases, asof) if asof else release_for_day(releases, start_date)
    status = "尚無資料" if not markets else decision_status(asof, counts)
    state = {
        "schema": "nfci-forward-v1",
        "title": "NFCI 紅燈減半往前測",
        "prereg": "事前登記 2026-10-18（持有人確認）",
        "start_date": start_date, "earliest_decision_date": EARLIEST_DECISION, "latest_decision_date": LATEST_DECISION,
        "data_through": asof, "status": status,
        "rule": "紅燈時每檔目標水位＝實單目標水位 × 0.5；綠燈＝實單目標；執行層、成本、時序同實單。",
        "scope": ("比較範圍只含股票檔：美股 QQQ、SMH，台股 0050、2330。美股公債與黃金兩檔照實單、"
                  "兩邊相同，不計入。影子線不下單。"),
        "nfci": {"current": release_brief(cur_rel), "releases_total": len(releases),
                 "missing": cap.get("missing", [])},
        "markets": markets,
    }
    if selfcheck:
        state["selfcheck_vs_scoreboard"] = selfcheck
    if forced:
        state["forced_color"] = forced
    if status in ("可判定", "已到最晚判定日"):
        state["criteria"] = {k: criteria_for(m) for k, m in markets.items()}
        state["criteria_note"] = "判準三條：股災、整段報酬回撤比、調整次數；兩個市場都三條全過才算通過。"
    return state


def selfcheck_scoreboard(sim_live_dates: list, nav_live: list, key: str):
    """影子線檔裡的「實單」淨值，對記分板已發布的 nav_sys 比相對變化（同一個簿記函式，應逐日吻合）。"""
    try:
        sb = json.loads(SCOREBOARD_JSON.read_text(encoding="utf-8"))["markets"][key]["nav_sys"]
        by = {r["date"]: r["nav"] for r in sb}
        if sim_live_dates[0] not in by:
            return None
        base_sb, base_me = by[sim_live_dates[0]], nav_live[0]
        diffs = [abs(by[d] / base_sb - n / base_me) for d, n in zip(sim_live_dates, nav_live) if d in by]
        return {"max_abs_rel_diff": round(max(diffs), 6), "days_compared": len(diffs)} if diffs else None
    except Exception as e:  # noqa: BLE001
        warn(f"記分板自檢略過（{key}）：{type(e).__name__}: {e}")
        return None


def run(args) -> int:
    today = date.fromisoformat(args.today) if args.today else datetime.now(timezone.utc).date()
    releases_path, out_path = Path(args.releases), Path(args.out)

    cap = capture_missing(releases_path, args.seed_vintage, today)
    if cap["missing"]:
        warn(f"NFCI 版本還沒存到：{cap['missing']}（下次執行會再補抓）")
    releases = load_releases(releases_path)

    live = json.loads(Path(args.live_state).read_text(encoding="utf-8"))
    market_sims, closes, sc = {}, {}, {}
    px_cache = {}
    irx = None
    for mkt in _lsb.MARKETS:
        key, hist = mkt["key"], live.get(mkt["hist_key"]) or []
        if not any(r["date"] >= args.start_date for r in hist):
            market_sims[key] = None
            info(f"{key}：實單紀錄還沒到起始日 {args.start_date}，尚無影子資料")
            continue
        legs = mkt["legs"]
        for t in legs:
            if t not in px_cache:
                px_cache[t] = {ts.strftime("%Y-%m-%d"): float(c) for ts, c in _w52.fetch_close(t).items()}
        px = {t: px_cache[t] for t in legs}
        px_dates = {t: sorted(px[t]) for t in legs}
        cash, cash_dates = None, None
        if mkt["cash_ticker"] == "^IRX":
            irx = irx or _lsb.fetch_us_cash_series()
            cash, cash_dates = irx, sorted(irx)
        sim = simulate_market(mkt, hist, args.start_date, lambda d: release_for_day(releases, d), px, px_dates,
                              cash, cash_dates, force_color=args.force_color)
        if sim["gaps"]:
            raise Abort(f"{key} 報酬缺口：{sim['gaps'][:2]}")
        market_sims[key] = sim
        idx_leg = MARKET_INDEX_LEG[key]
        closes[key] = [px[idx_leg][d] for d in sim["dates"]] if all(d in px[idx_leg] for d in sim["dates"]) else None
        if closes[key] is None:
            raise Abort(f"{key} 指數腿 {idx_leg} 缺收盤價")
        sc[key] = selfcheck_scoreboard(sim["dates"], sim["nav_live"], key)

    sc_flat = {k: v for k, v in sc.items() if v} or None
    state = build_state(args.start_date, releases, cap, market_sims, closes, sc_flat, args.force_color)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    new_text = dump_json(state)
    if not out_path.exists() or out_path.read_text(encoding="utf-8") != new_text:
        out_path.write_text(new_text, encoding="utf-8")
        info(f"寫入 {out_path}（狀態：{state['status']}）")
    else:
        info("狀態檔沒有變動")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="NFCI 紅燈減半影子線（事前登記往前測）")
    ap.add_argument("--live-state", default=str(LIVE_STATE), help="實單 state.json")
    ap.add_argument("--releases", default=str(RELEASES_CSV), help="每週三公布值存檔（只增不改）")
    ap.add_argument("--out", default=str(STATE_OUT), help="影子線狀態檔")
    ap.add_argument("--start-date", default=START_DATE, help="（測試用）起始日")
    ap.add_argument("--seed-vintage", default=SEED_VINTAGE, help="（測試用）起始顏色版本")
    ap.add_argument("--today", default=None, help="（測試用）今天，YYYY-MM-DD，預設 UTC 今天")
    ap.add_argument("--force-color", choices=("red", "green"), default=None, help="（結構檢查用）強制燈色")
    args = ap.parse_args()
    overridden = (args.start_date != START_DATE or args.seed_vintage != SEED_VINTAGE or args.force_color
                  or args.live_state != str(LIVE_STATE))
    if overridden and (args.out == str(STATE_OUT) or args.releases == str(RELEASES_CSV)):
        print("測試用參數（起始日／起始版本／強制燈色／實單檔）必須同時指定 --out 與 --releases，避免污染正式檔。",
              file=sys.stderr)
        return 2
    try:
        return run(args)
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        print(f"::error::NFCI 影子線失敗：{type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
