#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_rrg_base_rates.py — RRG 類股輪動象限經驗轉移表
（forecast ledger v2 §9／`_market_cockpit_design_20260902.md` §9 package F5 機械餵料）。

季度手動重建（`--if-due` 供 cron 掛用；PREREG 凍結至 SPRT 判決或 2027-03 校準輪，見設計稿
§9 共同規則）。讀 `data/statlab_prices.json`（SPY + 11 檔 SPDR 類股 ETF，日線收盤，
~850 個交易日 ≈ 3.3 年；該檔由 `scripts/build_statlab.py` 維護，本檔唯讀）， **不打網路**。

RRG 計算（frame 120，逐字重用 `scripts/build_rotation_radar.py`）
--------------------------------------------------------------
本檔不重寫 rs_ratio／rs_mom 公式——`sys.path.insert(0, str(ROOT/"scripts"))` 後
`import build_rotation_radar as brr`，直接呼叫其 `brr.quadrant()`／`brr._compute_frames()`，
並讀其 `brr.FRAMES["120"]`／`brr.TRAIL_SMOOTH`／`brr.STD_FLOOR`／`brr.MOM_STD_FLOOR` 常數
（該模組頂層只 import stdlib，無網路／無 side effect，import 安全；pandas 由本檔自己
import 後以參數傳入 `_compute_frames(rs, aligned, bench, pd)`，同該函式簽名）：

  RS       = 100 * price / SPY_price（member 序列 reindex 到 SPY 的交易日格、ffill 對齊）
  rs_ratio = 100 + (RS - SMA(RS, 120)) / STD(RS, max(120, 60))
  rs_mom   = 100 + (rs_ratio - SMA(rs_ratio, 30)) / STD(rs_ratio, max(30, 24))
  （rs_ratio／rs_mom 皆再用 SMA(3) 平滑，逐字同 build_rotation_radar.py TRAIL_SMOOTH）
  quadrant(r, m) = brr.quadrant()：r>=100,m>=100→leading；r>=100,m<100→weakening；
                   r<100,m<100→lagging；r<100,m>=100→improving（**用既有函式的 >= 邊界**，
                   非本檔另訂——見下方「已知的口徑近似」）。

取樣與結果定義（PREREG 凍結，設計稿 §9 F5）
------------------------------------------
* **取樣點** ＝ frame-120 平滑序列（`_compute_frames()` 回傳的第二個值
  `series_by_frame["120"]`，即該框架「暖身後」的**完整**歷史，非只有 trail 最後 N 筆）中
  每個日曆月第一個可得交易日。
* **可驗證樣本** ＝ 取樣點中該點在 SPY 交易日格（`grid`）上的位置 idx 滿足
  `idx + 63 < len(grid)`（63 個交易日後的收盤存在）者。
* **結果 ＝ ETF 63 個交易日後累積報酬 > SPY 同窗累積報酬**（`outcome_beat`），與
  `knowledge/settle_forecasts.py` 的 `relspy:` 域結算邏輯
  `(px_T/base_px) - (spy_T/base_spy) > 0` 同義（只是本表用交易日窗，producer 端的
  resolver 用 91 曆日近似——見下方近似說明）。

誠實註記（務必讀）
------------------
* **樣本期僅 statlab_prices.json 的 ~3.3 年**（非 20 年）：frame 120 暖身
  （rs_ratio 需 W=120、rs_mom 再需 Wm=30、外加 SMA(3) 平滑，約 152 個交易日暖身）後
  剩約 2.7 年可取樣；扣掉尾端無法驗證 63 交易日後結果的最近 ~3 個月，實得約 30 個月
  ×11 檔 ≈ 300 餘筆觀測，樣本天生薄——四象限拆分後單一 ETF×象限格幾乎必然 n<30，
  **pooled 是主力查表對象**，這是資料本身限制，非本腳本 bug（同
  `build_tsmom_base_rates.py`／`build_risk_gauge_base_rates.py` 既有立場）。
* **月度取樣、63 交易日視窗，樣本重疊**：相鄰月取樣點間距約 21 個交易日，遠短於 63 個
  交易日的前瞻視窗，相鄰樣本點的結果視窗高度重疊（約共用 42 個交易日）——非獨立試驗，
  頻率是重疊樣本的經驗估計，不做假設檢定，信賴區間不適用傳統獨立樣本公式。
* **quadrant 邊界逐字沿用 `build_rotation_radar.quadrant()`**（r>=100 那側算
  leading/weakening，不是嚴格 `>`）——設計稿 §9 F5 列的象限說明文字用的是類似 `r>100`
  的敘述性寫法，但「逐字照 frame 120／可 import 則 import」是更高優先的凍結指令，本檔選
  擇與全站唯一權威的 `quadrant()` 保持位元一致（`/rotation/` 頁面與 `radar.json` 都是這個
  函式），而不是另訂一套邊界語意——若日後校準輪認為兩者不一致有問題，應改的是設計稿文字
  而非本檔另立新函式製造第二種象限定義。
* **63 個交易日 ↔ 91 個曆日**：本表用交易日窗取樣（與 rs_ratio/rs_mom 的交易日語意一致），
  但 `scripts/generate_rrg_forecasts.py` 產生的 forecast `resolve_by` 用 91 曆日
  （同 tsmom／risk-gauge producer 既有的交易日↔曆日近似取捨，非本表精確對齊）。
* **cell n<30 一律標 `lo_sample`**（own 每檔×象限格、pooled×象限格都標，不只其中一種）：
  producer 端 own-cell n<30 時 fallback 用 pooled 同象限格（`min_cell_n_for_own_table`）；
  若連 pooled 格都 n<30，producer 會在該筆 note 額外記 `confidence=lo`——本檔只誠實列出
  每格的 n 與 lo_sample，不做任何替換或隱藏樣本薄的格。

用法
----
  python scripts/build_rrg_base_rates.py                離線重算（預設，唯讀本地檔）
  python scripts/build_rrg_base_rates.py --if-due        built_at 距今 <85 天則跳過
                                                           （exit 0，印 not due）
  python scripts/build_rrg_base_rates.py --out /tmp/x.json   測試用輸出路徑覆寫
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STATLAB_PRICES = DATA / "statlab_prices.json"
OUT_JSON = DATA / "rrg_base_rates.json"

sys.path.insert(0, str(ROOT / "scripts"))
import build_rotation_radar as brr  # noqa: E402 — quadrant()/_compute_frames()/FRAMES 逐字重用

SCHEMA = "rrg-base-rates-v1"
FRAME_KEY = "120"
BENCH = "SPY"
OUTCOME_WINDOW_TD = 63     # PREREG 凍結（設計稿 §9 F5："63 個交易日跑贏 SPY"）
MIN_CELL_N = 30            # producer 端 own-cell < 此門檻 → fallback 用 pooled（本檔僅標註，不替換）
IF_DUE_MAX_AGE_DAYS = 85   # --if-due 門檻，同 build_tsmom_base_rates.py／build_risk_gauge_base_rates.py 慣例

QUADRANTS = ["leading", "weakening", "lagging", "improving"]
QUAD_LABEL_ZH = {"leading": "領先", "weakening": "轉弱", "lagging": "落後", "improving": "改善"}

# 11 檔 SPDR 類股 ETF（逐字同 build_rotation_radar.py UNIVERSES["us_sectors"] 的 members，
# 排除 SMH——半導體 ETF 非 SPDR 板塊基金，設計稿 §9 F5 明文「11 檔 SPDR 對 SPY」）
SECTOR_ETFS = [
    ("XLK", "科技"), ("XLC", "通訊服務"), ("XLY", "非必需消費"), ("XLP", "必需消費"),
    ("XLV", "醫療保健"), ("XLF", "金融"), ("XLI", "工業"), ("XLE", "能源"),
    ("XLB", "原物料"), ("XLRE", "房地產"), ("XLU", "公用事業"),
]


def warn(msg: str) -> None:
    print(f"[rrg-base-rates][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[rrg-base-rates] {msg}")


# ═══════════════════════════════════════════════════════════════════════════
# 讀取：data/statlab_prices.json（唯讀，本檔不打網路）
# ═══════════════════════════════════════════════════════════════════════════

def load_statlab(path=STATLAB_PRICES):
    if not path.exists():
        raise SystemExit(f"找不到 {path} —— 先跑 python scripts/build_statlab.py")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {path}: {e}")
    series = data.get("series") or {}
    return data, series


def _to_series(pts, pd):
    idx = [pd.Timestamp(d) for d, _ in pts]
    return pd.Series([float(c) for _, c in pts], index=idx).sort_index()


# ═══════════════════════════════════════════════════════════════════════════
# 每檔：frame 120 全歷史平滑序列 + 月度取樣 + 63 交易日後結果
# ═══════════════════════════════════════════════════════════════════════════

def process_etf(spy_s, member_s, pd):
    """回傳 (rows, data_start, data_end) 或 None（歷史不足，frame 120 全程無有效值）。
    rows: [{"date","month","quadrant","r","m","outcome_beat"}, ...]（升冪，僅可驗證樣本）。"""
    grid = spy_s.index
    aligned = member_s.reindex(grid).ffill()
    rs = 100.0 * aligned / spy_s
    rs = rs.dropna()
    if rs.empty:
        return None

    frames, series_by_frame = brr._compute_frames(rs, aligned, spy_s, pd)
    full = series_by_frame.get(FRAME_KEY)
    if full is None or full.empty:
        return None

    grid_pos = {ts: i for i, ts in enumerate(grid)}
    n_grid = len(grid)

    rows = []
    seen_months = set()
    for ts in full.index:
        mk = ts.strftime("%Y-%m")
        if mk in seen_months:
            continue
        seen_months.add(mk)
        idx = grid_pos.get(ts)
        if idx is None or idx + OUTCOME_WINDOW_TD >= n_grid:
            continue  # 63 交易日後的資料尚不存在，非可驗證樣本
        r, m = (float(v) for v in full.loc[ts].values)
        q = brr.quadrant(r, m)
        px0, px1 = float(aligned.iloc[idx]), float(aligned.iloc[idx + OUTCOME_WINDOW_TD])
        spy0, spy1 = float(spy_s.iloc[idx]), float(spy_s.iloc[idx + OUTCOME_WINDOW_TD])
        ret_etf = px1 / px0 - 1.0
        ret_spy = spy1 / spy0 - 1.0
        rows.append({
            "date": ts.strftime("%Y-%m-%d"), "month": mk,
            "quadrant": q, "r": round(r, 3), "m": round(m, 3),
            "ret_etf_pct": round(ret_etf * 100.0, 3), "ret_spy_pct": round(ret_spy * 100.0, 3),
            "outcome_beat": bool(ret_etf > ret_spy),
        })

    data_start = aligned.dropna().index[0].strftime("%Y-%m-%d") if aligned.dropna().size else None
    data_end = aligned.index[-1].strftime("%Y-%m-%d")
    return rows, data_start, data_end


# ═══════════════════════════════════════════════════════════════════════════
# 象限彙總（own 每檔 + pooled）
# ═══════════════════════════════════════════════════════════════════════════

def summarize_by_quadrant(rows, min_n=MIN_CELL_N):
    """回傳 {quadrant: {"n","freq_beat","lo_sample"}, ...}，四象限皆列（n=0 時 freq_beat=None）。"""
    out = {}
    for q in QUADRANTS:
        sub = [r for r in rows if r["quadrant"] == q]
        n = len(sub)
        if n == 0:
            out[q] = {"n": 0, "freq_beat": None, "lo_sample": True}
            continue
        freq = sum(1 for r in sub if r["outcome_beat"]) / n
        out[q] = {"n": n, "freq_beat": round(freq, 4), "lo_sample": n < min_n}
    return out


def p_clim_unconditional(rows):
    """該母體（單檔或 pooled）全部可驗證樣本、不分象限的無條件 freq_beat。"""
    n = len(rows)
    if n == 0:
        return None
    return round(sum(1 for r in rows if r["outcome_beat"]) / n, 4)


# ═══════════════════════════════════════════════════════════════════════════
# Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="RRG 類股輪動象限經驗轉移表 builder（forecast ledger 機械餵料）")
    ap.add_argument("--input", default=str(STATLAB_PRICES),
                     help="輸入路徑（測試用；預設 data/statlab_prices.json）")
    ap.add_argument("--out", default=str(OUT_JSON),
                     help="輸出路徑（測試用；預設 data/rrg_base_rates.json）")
    ap.add_argument("--if-due", action="store_true",
                     help=f"現有輸出（--out 路徑）built_at 距今 <{IF_DUE_MAX_AGE_DAYS} 天則跳過重建"
                          "（exit 0，印 not due）；供 cron 掛「季度自動重建」用")
    args = ap.parse_args()

    out_path = Path(args.out)

    if args.if_due:
        if out_path.exists():
            try:
                existing = json.loads(out_path.read_text(encoding="utf-8"))
                built_at = existing.get("built_at")
                if built_at:
                    built_dt = datetime.strptime(built_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    age_days = (datetime.now(timezone.utc) - built_dt).total_seconds() / 86400.0
                    if age_days < IF_DUE_MAX_AGE_DAYS:
                        info(f"--if-due: {out_path} built_at={built_at}（{age_days:.1f} 天前）< "
                             f"{IF_DUE_MAX_AGE_DAYS} 天門檻，not due，本次不重建")
                        return
                    info(f"--if-due: {out_path} built_at={built_at}（{age_days:.1f} 天前）≥ "
                         f"{IF_DUE_MAX_AGE_DAYS} 天門檻，due，繼續重建")
                else:
                    info(f"--if-due: {out_path} 無 built_at 欄位，視為需要重建")
            except (OSError, json.JSONDecodeError, ValueError) as e:
                warn(f"--if-due: 無法讀取/解析既有 {out_path}（{e}），視為需要重建")
        else:
            info(f"--if-due: {out_path} 不存在，視為需要重建")

    import pandas as pd

    statlab_meta, series = load_statlab(Path(args.input))
    if BENCH not in series:
        raise SystemExit(f"{args.input} 缺 {BENCH} 序列")
    spy_s = _to_series(series[BENCH], pd)

    tickers_out = {}
    rows_by_ticker = {}
    gaps = []

    for etf, label in SECTOR_ETFS:
        if etf not in series or not series[etf]:
            warn(f"{etf}：{args.input} 無此序列，略過")
            gaps.append({"ticker": etf, "reason": "missing_in_statlab_prices"})
            tickers_out[etf] = {"role": label, "n_samples": 0, "quadrants": summarize_by_quadrant([]),
                                 "p_clim": None, "note": "無價格資料"}
            rows_by_ticker[etf] = []
            continue

        member_s = _to_series(series[etf], pd)
        result = process_etf(spy_s, member_s, pd)
        if result is None:
            warn(f"{etf}：frame 120 全程無有效值（歷史不足暖身門檻），略過")
            gaps.append({"ticker": etf, "reason": "insufficient_history_for_frame_120"})
            tickers_out[etf] = {"role": label, "n_samples": 0, "quadrants": summarize_by_quadrant([]),
                                 "p_clim": None, "note": "歷史不足以算 frame 120"}
            rows_by_ticker[etf] = []
            continue

        rows, data_start, data_end = result
        rows_by_ticker[etf] = rows
        tickers_out[etf] = {
            "role": label,
            "data_start": data_start, "data_end": data_end,
            "n_samples": len(rows),
            "quadrants": summarize_by_quadrant(rows),
            "p_clim": p_clim_unconditional(rows),
        }
        if not rows:
            warn(f"{etf}：frame 120 有效歷史存在，但可驗證月度取樣點為 0"
                 f"（歷史不足以同時取樣 + {OUTCOME_WINDOW_TD} 交易日後結果）")

    pooled_rows = []
    for etf, _ in SECTOR_ETFS:
        pooled_rows.extend(rows_by_ticker.get(etf, []))
    pooled_quadrants = summarize_by_quadrant(pooled_rows)
    pooled_p_clim = p_clim_unconditional(pooled_rows)

    payload = {
        "schema": SCHEMA,
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "data/statlab_prices.json",
        "source_built_at": statlab_meta.get("built_at"),
        "frame": FRAME_KEY,
        "frame_params": {
            "W": brr.FRAMES[FRAME_KEY][0], "Wm": brr.FRAMES[FRAME_KEY][1],
            "trail_smooth": brr.TRAIL_SMOOTH, "std_floor": brr.STD_FLOOR, "mom_std_floor": brr.MOM_STD_FLOOR,
        },
        "quadrant_definition": (
            "brr.quadrant(r,m)（scripts/build_rotation_radar.py 逐字重用，非本檔另訂）："
            "r>=100 and m>=100 -> leading；r>=100 and m<100 -> weakening；"
            "r<100 and m<100 -> lagging；否則(r<100 and m>=100) -> improving。"
        ),
        "sample_definition": (
            "取樣點＝frame 120 平滑序列（暖身後）每個日曆月第一個可得交易日；可驗證樣本＝"
            "該點在 SPY 交易日格上的位置 idx 滿足 idx+63 < len(grid)（63 個交易日後收盤存在）。"
        ),
        "outcome_definition": f"outcome_beat = ETF {OUTCOME_WINDOW_TD} 個交易日後累積報酬 > SPY 同窗累積報酬。",
        "outcome_window_trading_days": OUTCOME_WINDOW_TD,
        "min_cell_n_for_own_table": MIN_CELL_N,
        "sector_etfs": [t for t, _ in SECTOR_ETFS],
        "benchmark": BENCH,
        "tickers": tickers_out,
        "pooled": {
            "n_samples": len(pooled_rows),
            "quadrants": pooled_quadrants,
            "p_clim": pooled_p_clim,
            "note": "11 檔 SPDR 類股 ETF 全部可驗證樣本合併（跨象限、跨 ETF），供 producer own-cell "
                    "n<min_cell_n_for_own_table 時的 fallback 對象。",
        },
        "fetch_gaps": gaps,
        "methodology_note": (
            "月度取樣、63 交易日視窗，相鄰取樣點結果視窗高度重疊（非獨立試驗），本表只報告經驗"
            "頻率與樣本數 n，不做假設檢定。cell n<min_cell_n_for_own_table 的樣本薄格已標 "
            "lo_sample（own 與 pooled 皆標），由 generate_rrg_forecasts.py 查表時 fallback 用 "
            "pooled 同象限的格（見設計稿 notes/site-internal/root/_market_cockpit_design_20260902.md "
            "§9 row F5），本檔不預先替換。樣本期僅 statlab_prices.json 的 ~3.3 年（非長期歷史），"
            "四象限拆分後單一 ETF×象限格幾乎必然樣本薄，pooled 是主力查表對象——這是資料本身"
            "限制，非本腳本 bug。"
        ),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
                        encoding="utf-8")

    info(f"wrote {out_path}")
    info(f"pooled quadrant table (n / freq_beat / lo_sample):")
    for q in QUADRANTS:
        c = pooled_quadrants[q]
        thin = "  ← THIN" if c["lo_sample"] else ""
        info(f"  {q:<10} ({QUAD_LABEL_ZH[q]})  n={c['n']:>4}  freq_beat={c['freq_beat']}{thin}")
    info(f"  pooled p_clim（無條件，n={len(pooled_rows)}）: {pooled_p_clim}")
    info(f"{'ticker':<6} {'n_samp':>7} {'p_clim':>8}  per-quadrant n(freq)")
    for etf, _ in SECTOR_ETFS:
        row = tickers_out[etf]
        qtxt = " ".join(f"{q[:4]}={row['quadrants'][q]['n']}({row['quadrants'][q]['freq_beat']})"
                         for q in QUADRANTS) if row.get("quadrants") else ""
        info(f"{etf:<6} {row.get('n_samples', 0):>7} {str(row.get('p_clim')):>8}  {qtxt}")


if __name__ == "__main__":
    main()
