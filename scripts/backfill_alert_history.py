#!/usr/bin/env python3
"""backfill_alert_history.py — 一次性回填 detective 警戒度（alert_level）歷史.

用途（ONE-SHOT，非 cron、非 pipeline）：把市場偵探 v2 的警戒度 0-100 描述器
用 **同一套 PREREG 凍結權重（build_detective.ALERT_WEIGHTS）** 對可忠實重建的
成分逐日重算、狀態機逐日回放，產出 2-3 年回測歷史，輸出
docs/detective/data/alert_history_backfill.json（schema detective-alert-backfill-v1）。
與實盤線（docs/detective/data/alert_history.json，2026-07-15 起累積）不重疊：
回測 end 固定 2026-07-14。

單一真相源：不複製任何權重／閾值／規則／狀態機邏輯，全部 import 自現行 build：
  · build_monitor        — 96 series 定義（S）、compute_stats、series_alerts、
                           structural_alerts、RULES、fmt_*、CATEGORIES、STALE_DAYS
  · build_detective      — ALERT_WEIGHTS／compute_alert_level／monitor_signals／
                           reversal_signals／sector_signals／kill_signals／
                           inject_composites／fill_composite_members／render_signals／
                           build_composites_output（**權重與公式零複製**）
  · detective_rules      — R1-R9 複合規則評估
  · detective_state      — 狀態機 advance（escalated／sustained／days_active）
  · build_monitor_internals — pc_equity（CBOE）／yoy／mom／treasury 標售 fetch
  · build_kill_watch     — evaluate（breach／near 判定）

誠實分級（見輸出檔 metadata / fidelity_notes）：回測分數是 **下界近似**。
納入（可忠實重建）：
  monitor z／pctile／streak 異常 + 結構事件（曲線翻轉／VIX 期限倒掛／股漲信用
  背離；F&G 排除，無歷史）、reversal 三點翻折、composites R1-R5/R7（純 monitor）、
  R9（pc_equity CBOE，深度足夠、全窗可重建）、kill 12 條機械對帳（text_hash 凍結）、
  狀態機逐日回放。
排除（記入 fidelity_notes）：
  variance（歷史共識不可得）、crowding COT／主題擁擠、rotation RRG 象限、
  regime、macro_clock（→ composites R6／R8 連帶 dormant，sector 象限翻轉排除）、
  Fear&Greed、internals breadth／NAAIM／FINRA（不進 detective 主鏈）。
→ 缺部分黃燈源；但 yellow 硬封頂 18，繁忙日封頂飽和時缺源不影響，平靜日才是
   真正的下界。

重跑方式：
  python3 scripts/backfill_alert_history.py            # 用 scratchpad 快取（若有）→ 秒級、逐位元相同
  python3 scripts/backfill_alert_history.py --refetch  # 強制重抓所有外部資料（yf/FRED/CBOE/Treasury）
兩次連續執行（同快取）輸出逐位元相同（除 generated_at）。CBOE 逐日抓取 0.2s 禮貌節流。
不 commit、不 push；只新增本 script 與輸出檔。
"""
import argparse
import json
import os
import sys
import time
from datetime import date, datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
DOCS = os.path.join(ROOT, "docs")
sys.path.insert(0, SCRIPTS)

import build_monitor as bm            # noqa: E402
import build_monitor_internals as bmi  # noqa: E402
import build_detective as bd          # noqa: E402
import build_kill_watch as bkw        # noqa: E402
import detective_rules as drules      # noqa: E402
import detective_state as dstate      # noqa: E402

# ── 回測窗（end 固定 2026-07-14；實盤線 07-15 起，不重疊）──────────────────────
BACKTEST_START = "2023-07-15"     # ~3 年
BACKTEST_END = "2026-07-14"
YF_START = "2021-07-01"           # ≥ 4 年原始資料（回測 3 年 + 252 日滾動窗暖機）
CBOE_START = "2022-07-01"         # pc_equity 需 252 日窗 → 回測起點前一年
STATE_WARMUP_DAYS = 45            # 記錄起點前先空跑 N 交易日暖機狀態機（days_active／
#                                   escalated／sustained 有足夠前史，避免 cold-start 低估）
THROTTLE_S = 0.2                  # CBOE 逐日禮貌節流
UA = {"User-Agent": "Mozilla/5.0 (compatible; imq-monitor/1.0)"}

CACHE_DIR = os.environ.get(
    "BACKFILL_CACHE_DIR",
    "/private/tmp/claude-501/-Users-ivanchang-financial-analysis-bot/"
    "3b14e764-5448-491b-bd99-24ae93001935/scratchpad")
CACHE_PATH = os.path.join(CACHE_DIR, "alert_backfill_rawcache.json")

OUT_PATH = os.path.join(DOCS, "detective", "data", "alert_history_backfill.json")


def log(msg):
    print(f"[backfill] {msg}", flush=True)


# ── 外部資料抓取（無 400 上限的長史版本）────────────────────────────────────

def fetch_fred_full(series_id):
    """FRED CSV 全史（不套 build_monitor 的 400 上限；不帶假 UA）。"""
    import requests
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        r = requests.get(url, timeout=45)
        r.raise_for_status()
    except Exception as e:
        log(f"FRED {series_id} FAIL: {e}")
        return None
    pts = []
    for line in r.text.strip().split("\n")[1:]:
        parts = line.split(",")
        if len(parts) < 2 or parts[1] in ("", "."):
            continue
        try:
            pts.append((parts[0], float(parts[1])))
        except ValueError:
            continue
    return pts or None


def fetch_yf_long(tickers):
    """一次批抓 5y 日線（auto_adjust；抄 build_monitor.fetch_yf 的清洗，改長期間）。"""
    import pandas as pd
    import yfinance as yf
    out = {}
    df = yf.download(tickers, start=YF_START, interval="1d", auto_adjust=True,
                     progress=False, threads=True, group_by="column")
    if df is None or len(df) == 0:
        return out
    close = (df["Close"] if isinstance(df.columns, pd.MultiIndex)
             else df[["Close"]].rename(columns={"Close": tickers[0]}))
    for tk in close.columns:
        pts = []
        for idx, val in close[tk].items():
            try:
                c = float(val)
            except (TypeError, ValueError):
                continue
            if c != c or c <= 0:
                continue
            pts.append((idx.date().isoformat(), round(c, 6)))
        if pts:
            out[str(tk)] = pts
    return out


def fetch_cboe_pc_equity(start_iso, end_iso):
    """逐商業日抓 CBOE 個股 put/call（pc_equity），回傳 [(date, val)] 升冪。
    複用 build_monitor_internals.fetch_cboe_day（單一真相源）。0.2s 節流。"""
    d0 = datetime.strptime(start_iso, "%Y-%m-%d").date()
    d1 = datetime.strptime(end_iso, "%Y-%m-%d").date()
    days = []
    d = d0
    while d <= d1:
        if d.weekday() < 5:
            days.append(d.isoformat())
        d = date.fromordinal(d.toordinal() + 1)
    pts, got, miss = [], 0, 0
    for i, dd in enumerate(days):
        day = bmi.fetch_cboe_day(dd)
        time.sleep(THROTTLE_S)
        if day and "pc_equity" in day:
            pts.append((dd, day["pc_equity"]))
            got += 1
        else:
            miss += 1
        if (i + 1) % 100 == 0:
            log(f"  CBOE {i + 1}/{len(days)} (got {got}, miss {miss})")
    log(f"CBOE pc_equity: {got} days ({miss} miss/holiday) over {start_iso}→{end_iso}")
    return pts


def acquire_raw(refetch):
    """抓齊全部外部原始資料並存 scratchpad 快取（重跑逐位元相同）。"""
    if not refetch and os.path.exists(CACHE_PATH):
        log(f"loading raw cache: {CACHE_PATH}")
        with open(CACHE_PATH, encoding="utf-8") as fh:
            return json.load(fh)

    log("fetching raw external data (this is the slow one-shot step) …")
    # 1. yfinance（build_monitor S 的所有 yf 腳）
    yf_tickers = sorted({sp["ticker"] for sp in bm.S.values() if sp["src"] == "yf"})
    log(f"yfinance: {len(yf_tickers)} tickers from {YF_START} …")
    yf_data = fetch_yf_long(yf_tickers)
    missing = [t for t in yf_tickers if t not in yf_data]
    if missing:
        log(f"yfinance MISSING: {missing}")

    # 2. FRED（build_monitor S 的所有 fred 腳，全史）
    fred_ids = sorted({sp["ticker"] for sp in bm.S.values() if sp["src"] == "fred"})
    fred_data = {}
    for fid in fred_ids:
        pts = fetch_fred_full(fid)
        if pts:
            fred_data[fid] = pts
    log(f"FRED (monitor): {len(fred_data)}/{len(fred_ids)} series")

    # 3. FRED（internals kill 用：核心 PCE／PAYEMS／10Y BEI）全史
    internals_fred = {}
    for fid in ("PCEPILFE", "PAYEMS", "T10YIE"):
        pts = fetch_fred_full(fid)
        if pts:
            internals_fred[fid] = pts
    log(f"FRED (internals): {len(internals_fred)}/3 series")

    # 4. Treasury 標售（auct_dealer；複用 internals fetch，全史）
    _b2c, dealer_pts = bmi.fetch_treasury_auctions()
    log(f"Treasury auctions: {len(dealer_pts)} dealer-takedown points")

    # 5. CBOE pc_equity（R9）
    cboe_pc = fetch_cboe_pc_equity(CBOE_START, BACKTEST_END)

    raw = {"yf": yf_data, "fred": fred_data, "internals_fred": internals_fred,
           "treasury_dealer": dealer_pts, "cboe_pc_equity": cboe_pc}
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as fh:
        json.dump(raw, fh)
    log(f"raw cache written: {CACHE_PATH}")
    return raw


# ── raw → 每 series 全史（複用 build_monitor.main 的 raw 組裝邏輯）─────────────

def build_raw_full(yf_data, fred_data):
    """組 build_monitor.S 每 key 的全史 [(date,val)]（yf/fred 直取，ratio/spread 導出）。"""
    raw = {}
    for key, sp in bm.S.items():
        if sp["src"] == "yf":
            raw[key] = yf_data.get(sp["ticker"])
        elif sp["src"] == "fred":
            pts = fred_data.get(sp["ticker"])
            if pts and sp["scale"] != 1.0:
                pts = [(d, v * sp["scale"]) for d, v in pts]
            raw[key] = pts
    for key, sp in bm.S.items():
        if sp["src"] in ("ratio", "spread"):
            nk, dk = sp["ticker"]
            a, b = raw.get(nk), raw.get(dk)
            if not a or not b:
                raw[key] = None
                continue
            bmap = dict(b)
            if sp["src"] == "ratio":
                raw[key] = [(d, round(v / bmap[d], 8)) for d, v in a
                            if d in bmap and bmap[d]]
            else:
                raw[key] = [(d, round(v - bmap[d], 8)) for d, v in a if d in bmap]
    return raw


def _last_leq(pts, d):
    """升冪序列中日期 <= d 的最後一點的值（等同 spark[-1] 的 as-of 語意）。"""
    val = None
    for dd, v in pts or []:
        if dd <= d:
            val = v
        else:
            break
    return val


def _days_diff(a, b):
    return (datetime.strptime(a, "%Y-%m-%d") - datetime.strptime(b, "%Y-%m-%d")).days


# ── 每日 monitor 層重建（複用 build_monitor.compute_stats / series_alerts / …）──

def monitor_asof(raw_full, D):
    """重建當日 monitor latest（categories）＋ alerts（複用 build_monitor 函數）。"""
    items = {}
    for key, sp in bm.S.items():
        pts = [(dd, v) for dd, v in (raw_full.get(key) or []) if dd <= D]
        st = bm.compute_stats(pts, sp["unit"], sp["freq"])
        if st is None:
            continue
        st["val_fmt"] = bm.fmt_val(st["last"], sp)
        st["chg_fmt"] = bm.fmt_chg(st["chg"], sp["unit"])
        if st["chg"] is None:
            st["dir"] = "neu"
        else:
            up = st["chg"] > 0
            st["dir"] = ("neg" if up else "pos") if sp["invert"] else ("pos" if up else "neg")
        items[key] = st
    # stale（同 build_monitor.main：日頻 5 天、其餘 12 天）
    for key, it in items.items():
        limit = bm.STALE_DAYS if bm.S[key]["freq"] == "d" else 12
        it["stale"] = _days_diff(D, it["date"]) > limit

    # alerts：series 級 + 結構級（fear_greed=None → F&G 分支略過，誠實排除）
    alerts = []
    for key, it in items.items():
        sp = bm.S[key]
        if sp["cat"] == "_hidden" or it["stale"]:
            continue
        alerts.extend(bm.series_alerts(it, sp))
    st_alerts, status = bm.structural_alerts(items, None)
    alerts.extend(st_alerts)
    alerts.sort(key=lambda a: (a["sev"] != "red", a["cat"]))

    # categories（同 build_monitor.main 的欄位）
    categories = []
    for cat_key, cat_label in bm.CATEGORIES:
        if cat_key == "alerts":
            continue
        rows = []
        for key, sp in bm.S.items():
            if sp["cat"] != cat_key or key not in items:
                continue
            it = items[key]
            row = {"key": key, "label": sp["label"], "unit": sp["unit"],
                   "val": it["val_fmt"], "chg": it["chg_fmt"], "dir": it["dir"],
                   "z": it["z"], "pctile": it["pctile"],
                   "p20": it["p20"], "p60": it["p60"],
                   "hi52": it["hi52"], "lo52": it["lo52"],
                   "streak": it["streak"], "spark": it["spark"],
                   "date": it["date"], "stale": it["stale"]}
            # build_detective.monitor_signals 的軌跡 enrich 以 `k in it` 判存在後直接
            # 格式化，遇 None 值會炸（production 資料史夠長不觸發；回測起點短史 series
            # 會）。三軌跡欄為 None 時刪鍵，使該 guard 正確落到「不可用」分支——純
            # 影響 context 字串（非計分），其餘 consumer 皆用 .get（None-safe）。
            for _k in ("p20", "p60", "pctile"):
                if row[_k] is None:
                    del row[_k]
            rows.append(row)
        categories.append({"key": cat_key, "label": cat_label, "items": rows})

    latest = {"schema": "monitor-v1", "as_of": D, "categories": categories,
              "alerts_today": alerts, "status": status}
    return latest, {"days": {D: alerts}}


def internals_asof(cboe_pc, D):
    """重建當日 internals（僅 pc_equity，供 R9）。pctile 未成窗（暖機）→ 標 stale
    使 R9 dormant（誠實：pc_equity 尚無一年分位時 R9 不算 active）。"""
    pts = [(dd, v) for dd, v in cboe_pc if dd <= D]
    st = bm.compute_stats(pts, "abs", "d")
    if st is None:
        return {}
    warming = st["pctile"] is None
    stale = _days_diff(D, st["date"]) > bm.STALE_DAYS
    it = {"key": "pc_equity", "label": "Put/Call 個股選擇權",
          "val": f"{st['last']:.2f}", "z": st["z"], "pctile": st["pctile"],
          "p20": st["p20"], "p60": st["p60"], "streak": st["streak"],
          "dir": "neu", "date": st["date"], "stale": bool(stale or warming)}
    return {"schema": "monitor-internals-v1", "as_of": D,
            "categories": [{"key": "options_vol", "items": [it]}]}


# ── 每日 kill 機械對帳（12 條，text_hash 凍結；複用 build_kill_watch.evaluate）──

def load_mechanical():
    reg = bkw.load_json(os.path.join(DOCS, "detective", "data", "kill_registry.json"))
    if not reg:
        raise SystemExit("kill_registry.json missing")
    return [it for it in reg.get("items", [])
            if it.get("parse", {}).get("mode") == "mechanical"]


# monitor series key（'cat/skey'）→ build_monitor.S key
_KILL_MON = {"fx/usdcny": "usdcny", "fx/dxy": "dxy",
             "liquidity/sofr_iorb": "sofr_iorb", "credit/hy_oas": "hy_oas",
             "rates/tp10y": "tp10y", "rates/dgs30": "dgs30"}


def kill_asof(mech, raw_full, internals_series, D):
    """回傳合成 kill_watch（breached／near／items）供 kill_signals 與 compute_alert_level。
    text_hash 檢查跳過（回測凍結 registry 版本，記入 fidelity_notes）。取數失敗的
    條目 → 跳過不計（誠實下界，不外推）。"""
    breached, near, items = [], [], []
    for it in mech:
        p = it["parse"]
        ds = p["data_source"]
        typ, key = ds.get("type"), ds.get("key")
        cur = None
        if typ == "monitor":
            mk = _KILL_MON.get(key)
            if mk:
                cur = _last_leq(raw_full.get(mk), D)
        elif typ == "internals":
            skey = key.split("/", 1)[-1]
            cur = _last_leq(internals_series.get(skey), D)
        if cur is None:
            continue  # 該日無此 series 資料 → 誠實跳過
        status = bkw.evaluate(cur, p["op"], p["value"])
        items.append({"id": it["id"], "doc": it["doc"], "theme": it["theme"],
                      "metric_text": it["metric_text"], "op": p["op"],
                      "value": p["value"], "unit": p.get("unit", ""),
                      "current": round(cur, 6)})
        if status == "breached":
            breached.append(it["id"])
        elif status == "near":
            near.append(it["id"])
    return {"as_of": D, "breached": sorted(breached), "near": sorted(near),
            "items": items}


# ── 主流程 ──────────────────────────────────────────────────────────────────

def build_internals_series(internals_fred, treasury_dealer):
    """組 internals kill 用序列：core_pce_yoy / payems_3m / bei10y / auct_dealer
    （複用 build_monitor_internals 的 yoy／mom 導出）。"""
    out = {}
    if "PCEPILFE" in internals_fred:
        y = bmi.yoy_series([tuple(x) for x in internals_fred["PCEPILFE"]])
        if y:
            out["core_pce_yoy"] = y
    if "PAYEMS" in internals_fred:
        m = bmi.mom_3mavg_series([tuple(x) for x in internals_fred["PAYEMS"]])
        if m:
            out["payems_3m"] = m
    if "T10YIE" in internals_fred:
        out["bei10y"] = [tuple(x) for x in internals_fred["T10YIE"]]
    if treasury_dealer:
        out["auct_dealer"] = [tuple(x) for x in treasury_dealer]
    return out


def trading_days_with_warmup(raw_full, start, end, warmup):
    """回傳 (all_days_incl_warmup, first_record_index)。warmup 個交易日在 start 之前。"""
    gspc_dates = [d for d, _ in (raw_full.get("sp500") or [])]
    rec = [d for d in gspc_dates if start <= d <= end]
    if not rec:
        return [], 0
    i0 = gspc_dates.index(rec[0])
    w0 = max(0, i0 - warmup)
    all_days = [d for d in gspc_dates[w0:] if d <= end]
    first_rec = all_days.index(rec[0])
    return all_days, first_rec


def run_backtest(raw, verbose_anchors):
    yf_data = {k: [tuple(x) for x in v] for k, v in raw["yf"].items()}
    fred_data = {k: [tuple(x) for x in v] for k, v in raw["fred"].items()}
    raw_full = build_raw_full(yf_data, fred_data)
    cboe_pc = [tuple(x) for x in raw["cboe_pc_equity"]]
    internals_series = build_internals_series(raw["internals_fred"], raw["treasury_dealer"])
    mech = load_mechanical()

    all_days, first_rec = trading_days_with_warmup(
        raw_full, BACKTEST_START, BACKTEST_END, STATE_WARMUP_DAYS)
    log(f"trading days: {len(all_days)} incl warmup ({all_days[0]} → {all_days[-1]}); "
        f"recording from index {first_rec} = {all_days[first_rec]}")

    # R9 起點：pc_equity 首個有 pctile（成一年窗）的交易日
    r9_since = None
    for D in all_days[first_rec:]:
        st = bm.compute_stats([(d, v) for d, v in cboe_pc if d <= D], "abs", "d")
        if st and st["pctile"] is not None:
            r9_since = D
            break

    state = dstate.empty_state()
    points = []
    band_counts = {}
    anchors = {}
    kill_track = {}   # 報告用：逐月 kill breach/near（非計分，見 fidelity_notes）
    anchor_set = {"2024-08-02", "2024-08-05", "2024-08-06",
                  "2025-04-03", "2025-04-04", "2025-04-07", "2025-04-08",
                  "2026-07-14"}
    calm_probe = {"2024-06-14", "2024-05-15", "2025-06-16", "2026-05-15"}  # 平靜段抽樣

    for idx, D in enumerate(all_days):
        recording = idx >= first_rec
        latest, alerts = monitor_asof(raw_full, D)
        internals = internals_asof(cboe_pc, D)
        # kill：計算供報告（逐月抽樣），但 **不計入分數** — 12 條門檻為 as-of-2026
        # level/regime 觸發（DXY≥102／CNY>7.2／PCE≥3.5／dgs30≥5.5…），非平穩，套用
        # 於歷史會造出時代錯置的持續 breach（見 fidelity_notes / components_excluded）。
        kw = kill_asof(mech, raw_full, internals_series, D)
        if recording and D[:7] not in kill_track:
            kill_track[D[:7]] = {"breached": len(kw["breached"]), "near": len(kw["near"])}

        rule_sources = {"monitor": latest, "crowding": {}, "rotation": {},
                        "macro_clock": {}, "internals": internals}
        rule_evals = drules.evaluate_rules(rule_sources)

        sigs = []
        sigs += bd.monitor_signals(latest, alerts, D)
        sigs += bd.reversal_signals(latest)
        sigs += bd.sector_signals(latest, {})
        met = {}
        for s in sigs:
            met[s["key"]] = {"sev": s["sev"], "score": s["score_base"],
                             "display": {k: s[k] for k in
                                         ("source", "cat", "label", "fact",
                                          "context", "score_base")}}
        bd.inject_composites(met, rule_evals, state)
        state = dstate.advance(state, met, D)
        bd.fill_composite_members(state, rule_evals)

        composites_out = bd.build_composites_output(rule_evals, state, D)
        signals = bd.render_signals(state)
        # kw={} → kill 成分不計分（誠實排除，見上）
        alert_level = bd.compute_alert_level(signals, composites_out, {}, D)

        if not recording:
            continue
        band = alert_level["band"]
        points.append([D, alert_level["score"], band])
        band_counts[band] = band_counts.get(band, 0) + 1

        if D in anchor_set or D in calm_probe:
            n_red = sum(1 for s in signals if s["sev"] == "red")
            n_yel = len(signals) - n_red
            fired = [c["id"] for c in composites_out if c["fired"]]
            near_c = [c["id"] for c in composites_out
                      if not c["fired"] and c.get("status") == "active"
                      and (c.get("min_true") or 0) >= 1
                      and c.get("met_count", 0) == (c.get("min_true") or 0) - 1]
            anchors[D] = {
                "score": alert_level["score"], "band": band,
                "band_label": alert_level["band_label"],
                "red": n_red, "yellow": n_yel,
                "composites_fired": fired, "composites_near": near_c,
                "kill_breached": len(kw["breached"]), "kill_near": len(kw["near"]),
                "escalated": sum(1 for s in signals if s["state"] == "escalated"),
                "drivers": alert_level["drivers"]}

    return points, band_counts, anchors, r9_since, kill_track


def make_output(points, r9_since, kill_track):
    excluded = [
        {"name": "variance", "why": "歷史財測共識不可重建（DD 基準 × 逐期共識快照無歷史）"},
        {"name": "crowding", "why": "COT 5 年分位與主題擁擠需 8 年 CFTC 檔案工程，本輪排除"},
        {"name": "rotation", "why": "RRG 120 日象限逐日重放工程大，本輪排除"},
        {"name": "regime", "why": "大類資產 regime composite 無逐日歷史快照"},
        {"name": "macro_clock", "why": "總經時鐘象限逐月序列未保存歷史"},
        {"name": "composite_R6", "why": "成員為 crowding×rotation join，來源排除 → 全窗 dormant"},
        {"name": "composite_R8", "why": "成員含 macro_clock 象限，來源排除 → 全窗 dormant"},
        {"name": "sector_rotation_quadrant", "why": "us_sectors RRG 象限翻轉需 radar 歷史，排除；sector 單日 z 分歧仍納入"},
        {"name": "fear_and_greed", "why": "CNN F&G 無公開歷史序列，結構事件此支排除"},
        {"name": "internals_breadth_naaim_finra", "why": "只影響 internals 異常，不進 detective 主鏈，無需重建"},
        {"name": "kill_mechanical",
         "why": ("刻意排除計分（雖機械可算）：12 條門檻為 as-of-2026 的 level/regime "
                 "觸發（DXY≥102／USDCNY>7.2／核心PCE≥3.5／DGS30≥5.5／HY OAS≥3.5…），"
                 "非平穩。套用於 2023-2025（當時 DXY 常>102、CNY 常>7.2、2023 PCE 高）"
                 "會造出時代錯置的持續 breach（實測逐月 1-5 條長期 breach），以 14 分/條"
                 "（cap 42）＋紅燈雙計會把整段歷史釘在 alert，抹除描述器動態範圍。"
                 "live 描述器顯示 0 breached 正因門檻是對 2026 水位校準。逐月 breach/near "
                 "抽樣見 kill_reconstructed_monthly（僅供對照，未計分）。")},
    ]
    fidelity_notes = [
        "回測分數為下界近似：缺 variance／crowding／rotation／regime／macro_clock／F&G／kill "
        "等黃燈與紅燈源；惟 yellow_signal 硬封頂 18，繁忙日封頂飽和時缺源不影響分數，"
        "平靜/留意日才是真正的下界。",
        "kill 機械對帳刻意不計分（門檻非平穩、歷史套用會時代錯置，見 components_excluded）；"
        "auct_dealer 用 TreasuryDirect 標售全史、core_pce_yoy／payems_3m／bei10y 用 FRED "
        "全史，逐日可算，但因上述理由不進分數，只在 kill_reconstructed_monthly 供對照。",
        "composites R6／R8 因來源家族排除而全窗 dormant；R1-R5／R7 純 monitor 全窗可重建。",
        f"R9（自滿組合，含 pc_equity）自 {r9_since} 起可評估（CBOE 個股 put/call 一年分位成窗，"
        "CBOE 日檔深度實測回抓至 2020-07 仍在，故全回測窗可用）；此前標 dormant。",
        "monitor 逐日 z／pctile／streak 以 252 日滾動窗重算（暖機自 " + YF_START + "）；"
        "結構事件（曲線翻轉／VIX 期限倒掛／股漲信用背離）納入，F&G 極端排除。",
        f"狀態機自記錄起點前 {STATE_WARMUP_DAYS} 交易日空跑暖機，使 days_active／escalated／"
        "sustained 在記錄起點已有前史（避免 cold-start 低估持續與升級成分）。",
        "權重與公式零複製：全程呼叫 build_detective.compute_alert_level 與 ALERT_WEIGHTS"
        "（PREREG 凍結至 2026-10 校準），僅餵入可重建的成分（kw 傳空 dict 使 kill 不計分）。",
    ]
    return {
        "schema": "detective-alert-backfill-v1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "method": ("同一 ALERT_WEIGHTS 對可重建成分逐日重算；狀態機逐日回放"
                   "（build_detective 函數直用）；kill 成分刻意不計分"),
        "start": points[0][0], "end": points[-1][0],
        "components_included": ["monitor_z_pctile", "monitor_structural",
                                "reversal", "sector_single_day_divergence",
                                "composites_R1_R5_R7",
                                f"composites_R9_since_{r9_since}",
                                "state_machine_replay"],
        "components_excluded": excluded,
        "fidelity": "lower_bound",
        "fidelity_notes": fidelity_notes,
        "weights_source": "build_detective.ALERT_WEIGHTS (PREREG frozen)",
        "kill_reconstructed_monthly": kill_track,
        "point_count": len(points),
        "points": points,
    }


def write_output(out):
    body = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(body)
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refetch", action="store_true",
                    help="強制重抓所有外部資料（否則用 scratchpad 快取）")
    args = ap.parse_args()

    raw = acquire_raw(args.refetch)
    points, band_counts, anchors, r9_since, kill_track = run_backtest(raw, True)
    out = make_output(points, r9_since, kill_track)
    write_output(out)

    # ── 驗收報告 ──
    log("=" * 60)
    log(f"OUTPUT: {OUT_PATH}")
    log(f"points: {len(points)}  window: {points[0][0]} → {points[-1][0]}")
    log(f"R9 active since: {r9_since}")
    total = len(points)
    log("band distribution:")
    order = ["calm", "watch", "warming", "tense", "alert"]
    for b in order:
        n = band_counts.get(b, 0)
        log(f"  {b:8s} {n:4d}  {n / total * 100:5.1f}%")
    log("anchor-day scores:")
    for d in sorted(anchors):
        a = anchors[d]
        log(f"  {d}  score={a['score']:3d} {a['band']:8s}  "
            f"red={a['red']} yel={a['yellow']} "
            f"comp_fired={a['composites_fired']} comp_near={a['composites_near']} "
            f"kill_br={a['kill_breached']} kill_near={a['kill_near']} esc={a['escalated']}")
    # 與實盤 seed 銜接
    seed = bkw.load_json(os.path.join(DOCS, "detective", "data", "alert_history.json"))
    live = None
    if seed and seed.get("points"):
        live = seed["points"][-1]
    bt_end = points[-1]
    log("live seed vs backtest end:")
    log(f"  backtest {bt_end[0]}: score={bt_end[1]} band={bt_end[2]}")
    if live:
        log(f"  live     {live[0]}: score={live[1]} band={live[2]} "
            f"(gap explained by excluded kill_near + crowding/variance yellows)")
    log("kill reconstructed monthly (NOT scored — as-of-2026 non-stationary thresholds):")
    for ym in sorted(kill_track):
        k = kill_track[ym]
        log(f"  {ym}: breached={k['breached']} near={k['near']}")


if __name__ == "__main__":
    main()
