#!/usr/bin/env python3
"""態④觸發變體研究 — run_study.py（接線 + 報告）。

血統：六狀態機白皮書 §7 預登記法；引擎本體 study_trim_variants.py 已通過合成驗證
（test_study.py 5 情境 16 斷言），本檔只做接線、執行、報告，不碰演算法。

管線：
  load_universe（複用 run_daily）→ _yf_ticker 解析 → load_prices（生產 price_cache，
  period=max + auto_adjust）→ 取每檔 Close 對齊成寬表 → 持久化寬表（供日後復用）→
  study_trim_variants.run_study(closes, eras) → trim_variants.json（公開）+
  study-report.md（機械推導：R1/R2/R3 淘汰 → S1/S2 選擇，結論不含自由評論）。

用法：
  python3 scripts/state_machine/study/run_study.py                 # 全 universe（抓價）+ 跑研究
  python3 scripts/state_machine/study/run_study.py --refresh-only  # 只增量更新寬表股價（split-exact）
  python3 scripts/state_machine/study/run_study.py --rebuild       # base + repo 每日切片 → 最新寬表
  python3 scripts/state_machine/study/run_study.py --from-saved P  # 從已存寬表重跑研究（不抓價）

寬表股價持續更新：兩條路
  A. 全抓（split-exact，本機重 baseline）：--refresh-only。走 price_cache 6mo 增量 +
     拆股偵測，最準；但每次抓 226 檔。
  B. repo 自更新（CI 維護，本機只 pull+stitch）：CI 每日跑 write_daily_close.py commit
     一支 ~4.6KB 切片到 docs/.../study/closes_daily/；本機 `git pull` 後跑 --rebuild，把
     base（本機 latest.csv.gz）+ 累積切片併成最新寬表。git 只長 ~1MB/年。
     注意：切片是 forward auto_adjust 收盤，不回算拆股 → 尾段久了會有微幅 split 漂移；
     需 split-exact 時偶爾改跑 A 重 baseline。
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from itertools import combinations
from pathlib import Path

import pandas as pd

STUDY_DIR = Path(__file__).resolve().parent
ENGINE_DIR = STUDY_DIR.parent
sys.path.insert(0, str(STUDY_DIR))
sys.path.insert(0, str(ENGINE_DIR))
sys.path.insert(0, str(ENGINE_DIR.parent))   # scripts/ — dd_screener_quality ticker maps

import config as CFG  # noqa: E402
from price_cache import load_prices  # noqa: E402
from run_daily import _yf_ticker, load_universe  # noqa: E402
import study_trim_variants as STV  # noqa: E402

# ── 預登記閘門（原文照抄，跑後不可改）────────────────────────────────────────
PREREG = """**決策指標**：M1 觸發頻率（med/p75 次/年）· M2 假警報率（確認後10交易日內收回且未升級⑤）· M3 真崩代價（升級⑤事件的首碰→確認額外跌幅 med/p90）· M4 折騰單位（Σ減碼比例×來回/年）
**淘汰 R1**：M2 未較 V0 基準降 ≥40% → 淘汰 · **R2**：M3 med>3% 或 p90>8% → 淘汰 · **R3**：平原失敗（相鄰格關鍵指標相對變動>30%）→ 標「脆弱」，僅無倖存者時可選
**選擇 S1**：時代排名翻轉 → 退回倖存者中文法序最前 · **S2**：倖存者 M1-M4 互在 ±20% → 文法序決勝
**文法序**：V1 A-or-B > V3 延伸度 > V2 階梯 > V4 週線節奏
**禁區**：不算 CAGR/Sharpe/報酬；報告結論段每句以「依 R_/S_」開頭"""

ERAS = {"2020crash": ("2020-01-01", "2020-07-01"),
        "2022bear": ("2022-01-01", "2023-01-01"),
        "2023-24trend": ("2023-01-01", "2025-01-01"),
        "front_half": ("1900-01-01", "2019-01-01"),
        "back_half": ("2019-01-01", "2099-01-01")}

GRAMMAR_ORDER = ["V1", "V3", "V2", "V4"]      # 文法序（預登記）
OUT_JSON = CFG.DATA_DIR / "study" / "trim_variants.json"
REPORT_PATH = STUDY_DIR / "study-report.md"
LATEST_CLOSES = CFG.PRICE_CACHE_DIR / "study_closes_wide_latest.csv.gz"   # 穩定指標（免找日期檔名）
CLOSES_DAILY = CFG.DATA_DIR / "study" / "closes_daily"   # CI 每日 commit 的 forward 切片
MIN_BARS = 300


# ── 接線：universe → 寬表 ────────────────────────────────────────────────────
def build_closes() -> tuple[pd.DataFrame, list[str], list[str]]:
    universe = load_universe()
    symbols = [u["symbol"] for u in universe]
    yf_map = {s: _yf_ticker(s) for s in symbols}
    print(f"  universe: {len(symbols)} symbols", file=sys.stderr)
    prices, _ = load_prices(list(yf_map.values()))
    cols, missing, short_hist = {}, [], []
    for s in symbols:
        df = prices.get(yf_map[s])
        if df is None or "Close" not in df.columns:
            missing.append(s)
            continue
        c = df["Close"].dropna()
        if len(c) < MIN_BARS:
            short_hist.append(s)        # 仍納入：引擎 per_ticker_frames 會自動跳過
        cols[s] = c
    closes = pd.DataFrame(cols).sort_index()
    return closes, missing, short_hist


def save_closes(closes: pd.DataFrame) -> Path:
    """持久化寬表收盤價（adjusted, period=max），供日後直接復用：
    pd.read_csv(path, index_col=0, parse_dates=True)

    寫兩份：① 以收盤末日命名的快照（study 跑用，可釘住可重現）② study_closes_wide_latest.csv.gz
    （穩定指標，自己日常取用免找日期）。兩份同內容。"""
    asof = closes.index[-1].strftime("%Y-%m-%d")
    p = CFG.PRICE_CACHE_DIR / f"study_closes_wide_{asof}.csv.gz"
    p.parent.mkdir(parents=True, exist_ok=True)
    closes.to_csv(p, compression="gzip")
    shutil.copyfile(p, LATEST_CLOSES)
    return p


def rebuild_from_slices() -> tuple[pd.DataFrame, Path, int, int]:
    """本機全歷史 base（latest.csv.gz）+ repo 累積的 closes_daily/*.json forward 切片
    → 併成最新寬表。回傳 (closes, saved_path, n_new_cells, n_slices)。

    冪等：切片日期已在 base 內則覆寫同值；只計真正新增的格子。base 缺失時報錯（請先跑
    一次全抓建立 base）。split 漂移見 write_daily_close.py 註記。"""
    if not LATEST_CLOSES.exists():
        raise SystemExit(f"找不到 base 寬表 {LATEST_CLOSES}；請先跑 "
                         f"`run_study.py --refresh-only`（或不帶旗標跑完整研究）建立 base。")
    closes = pd.read_csv(LATEST_CLOSES, index_col=0, parse_dates=True)
    files = sorted(CLOSES_DAILY.glob("*.json")) if CLOSES_DAILY.exists() else []
    new_cells, n_slices = 0, 0
    for f in files:
        try:
            rec = json.loads(f.read_text(encoding="utf-8")).get("closes", {})
        except Exception as exc:
            print(f"  WARN: 略過壞切片 {f.name}: {exc}", file=sys.stderr)
            continue
        n_slices += 1
        for tk, cell in rec.items():
            ts = pd.Timestamp(cell["date"])
            if tk not in closes.columns:
                closes[tk] = pd.NA
            is_new = ts not in closes.index or pd.isna(closes.at[ts, tk])
            closes.loc[ts, tk] = cell["close"]
            if is_new:
                new_cells += 1
    closes = closes.apply(pd.to_numeric, errors="coerce").sort_index()
    saved = save_closes(closes)
    return closes, saved, new_cells, n_slices


# ── 機械規則引擎（R1/R2/R3 → S1/S2）─────────────────────────────────────────
def relchg(a, b):
    """對稱相對變動 |a-b| / mean(|a|,|b|)；任一為 None → None（不可判）。"""
    if a is None or b is None:
        return None
    m = (abs(a) + abs(b)) / 2
    if m == 0:
        return 0.0
    return abs(a - b) / m


def apply_r1(res: dict) -> dict:
    """R1：M2 未較 V0 降 ≥40% → 淘汰。回傳 {variant: (passed, reduction)}。"""
    base = res["variants"]["V0"]["m2"]
    out = {}
    for v in GRAMMAR_ORDER:
        m2 = res["variants"][v]["m2"]
        if base is None:
            out[v] = (True, None)               # 基準不可計 → R1 不可判 → 不淘汰
        elif base == 0:
            out[v] = (m2 == 0, None)            # 基準已為 0 → 只有同為 0 視為過
        elif m2 is None:
            out[v] = (True, 1.0)                # 無確認事件 → 假警報率視為 0 → 降 100%
        else:
            red = (base - m2) / base
            out[v] = (red >= 0.40, red)
    return out


def apply_r2(res: dict) -> dict:
    """R2：M3 med>3% 或 p90>8% → 淘汰。回傳 {variant: (passed, med, p90)}。"""
    out = {}
    for v in GRAMMAR_ORDER:
        a = res["variants"][v]
        med, p90 = a["m3_med"], a["m3_p90"]
        bad = (med is not None and med > 0.03) or (p90 is not None and p90 > 0.08)
        out[v] = (not bad, med, p90)
    return out


def _plateau_pairs_v1():
    cells = [(b, d) for b in (0.96, 0.97, 0.98) for d in (2, 3, 4)]
    pairs = []
    for (b1, d1) in cells:
        for (b2, d2) in cells:
            if (b1, d1) < (b2, d2) and ((b1 == b2 and abs(d1 - d2) == 1)
                                        or (d1 == d2 and abs(round((b1 - b2), 2)) == 0.01)):
                pairs.append((f"{b1}/{d1}", f"{b2}/{d2}"))
    return pairs


def apply_r3(res: dict) -> dict:
    """R3：平原相鄰格關鍵指標（M1_med / M2）相對變動 >30% → 標「脆弱」。
    平原僅存在於 V1（九宮格）與 V3（三點）；V2/V4 無參數平原 → 不適用。"""
    out = {"V2": (False, []), "V4": (False, [])}
    for v, grid, pairs in (
        ("V1", res["plateau_v1"], _plateau_pairs_v1()),
        ("V3", res["plateau_v3"], [("0.12", "0.15"), ("0.15", "0.18")]),
    ):
        viol = []
        for k1, k2 in pairs:
            for metric in ("m1_med", "m2"):
                rc = relchg(grid[k1][metric], grid[k2][metric])
                if rc is not None and rc > 0.30:
                    viol.append((k1, k2, metric, rc))
        out[v] = (bool(viol), viol)
    return out


def _era_rank(res: dict, survivors: list[str]) -> dict:
    """每時代窗以 M2 升冪（次鍵 M3 med、再 M1 med）排名倖存者。
    比率類指標不受 measure() 年數分母稀釋，時代窗內可比。"""
    INF = float("inf")
    ranks = {}
    for era, vr in res["eras"].items():
        def key(v):
            a = vr[v]
            return (a["m2"] if a["m2"] is not None else INF,
                    a["m3_med"] if a["m3_med"] is not None else INF,
                    a["m1_med"] if a["m1_med"] is not None else INF)
        ranks[era] = sorted(survivors, key=key)
    return ranks


def select(res: dict):
    """機械推導：R1∧R2 → 倖存者；R3 脆弱者僅在無非脆弱倖存者時可選；
    S1 時代排名翻轉 / S2 互在 ±20% → 文法序；否則全期 M2 最佳。
    回傳 (winner or None, trace 句子清單（每句以「依 R_/S_」開頭）)。"""
    r1, r2, r3 = apply_r1(res), apply_r2(res), apply_r3(res)
    trace = []
    for v in GRAMMAR_ORDER:
        if not r1[v][0]:
            red = r1[v][1]
            trace.append(f"依 R1，{v} 淘汰（M2 較 V0 變動 {-red*100:+.1f}%，未達 −40% 門檻）。"
                         if red is not None else f"依 R1，{v} 淘汰（M2 基準不可比）。")
        if not r2[v][0]:
            med, p90 = r2[v][1], r2[v][2]
            trace.append(f"依 R2，{v} 淘汰（M3 med={_pct(med)}、p90={_pct(p90)}，"
                         f"超出 med≤3% / p90≤8%）。")
    pool = [v for v in GRAMMAR_ORDER if r1[v][0] and r2[v][0]]
    fragile = {v for v in pool if r3[v][0]}
    robust = [v for v in pool if v not in fragile]
    for v in sorted(fragile, key=GRAMMAR_ORDER.index):
        n = len(r3[v][1])
        trace.append(f"依 R3，{v} 標「脆弱」（平原相鄰格相對變動 >30% 共 {n} 處），"
                     f"僅於無非脆弱倖存者時可選。")
    survivors = robust if robust else sorted(fragile, key=GRAMMAR_ORDER.index)
    if robust:
        trace.append("依 R1/R2/R3，倖存者（非脆弱）：" + "、".join(robust) + "。")
    elif fragile:
        trace.append("依 R3 但書，無非脆弱倖存者 → 脆弱者進入選擇：" + "、".join(survivors) + "。")
    if not survivors:
        trace.append("依 R1/R2，V1-V4 全數淘汰 → 維持 V0 現行。")
        return None, trace
    if len(survivors) == 1:
        trace.append(f"依 R1/R2/R3，唯一倖存者 {survivors[0]} 為機械勝出變體。")
        return survivors[0], trace
    # S1：時代排名翻轉（任兩倖存者在不同時代窗順序對調）
    ranks = _era_rank(res, survivors)
    flipped = False
    for a, b in combinations(survivors, 2):
        orders = {r.index(a) < r.index(b) for r in ranks.values()}
        if len(orders) > 1:
            flipped = True
            break
    if flipped:
        w = min(survivors, key=GRAMMAR_ORDER.index)
        trace.append(f"依 S1，時代排名翻轉成立 → 退回倖存者中文法序最前 = {w}。")
        return w, trace
    # S2：倖存者 M1-M4 互在 ±20%
    close_all = True
    for a, b in combinations(survivors, 2):
        for metric in ("m1_med", "m2", "m3_med", "m4_med"):
            rc = relchg(res["variants"][a][metric], res["variants"][b][metric])
            if rc is not None and rc > 0.20:
                close_all = False
    if close_all:
        w = min(survivors, key=GRAMMAR_ORDER.index)
        trace.append(f"依 S2，倖存者 M1-M4 互在 ±20% → 文法序決勝 = {w}。")
        return w, trace
    INF = float("inf")
    w = min(survivors, key=lambda v: (res["variants"][v]["m2"] if res["variants"][v]["m2"] is not None else INF,
                                      res["variants"][v]["m3_med"] if res["variants"][v]["m3_med"] is not None else INF))
    trace.append(f"依 S1/S2 皆不成立，倖存者按決策指標 M2（次鍵 M3 med）全期排序，最佳 = {w}。")
    return w, trace


# ── 報告（Step 4：一頁，機械推導）────────────────────────────────────────────
def _pct(x):
    return "—" if x is None else f"{x*100:.2f}%"


def _num(x):
    return "—" if x is None else f"{x:.3f}"


def _vrow(v, a):
    return (f"| {v} | {_num(a['m1_med'])} | {_num(a['m1_p75'])} | {_pct(a['m2'])} "
            f"({a['m2_confirmed']}) | {_pct(a['m3_med'])} | {_pct(a['m3_p90'])} "
            f"({a['m3_n']}) | {_num(a['m4_med'])} |")


def write_report(res, winner, trace, meta):
    L = []
    L.append(f"# 態④觸發變體研究 — study-report.md（{meta['asof']}）\n")
    L.append("## ① 預登記規則（原文，跑前鎖定）\n")
    L.append(PREREG + "\n")
    L.append("## ② 倖存者偏差聲明\n")
    L.append("本 universe 為今日 dd-screener 倖存者（226 檔現存優質股），歷史上已下市/"
             "跌出名單者不在樣本內。故本報告**只用變體間排名與相對差**做淘汰與選擇，"
             "不引用任何絕對值作結論依據；M1-M4 絕對數字僅供對照表呈現。\n")
    L.append(f"樣本：universe {meta['n_universe']} 檔 → 取得價格 {meta['n_priced']} 檔 → "
             f"引擎實用 {res['n_tickers_used']} 檔。抓取失敗 {len(meta['missing'])} 檔"
             f"{('：' + '、'.join(meta['missing'])) if meta['missing'] else ''}。"
             f"短歷史排除（<{MIN_BARS} 根日線，引擎自動跳過）{len(meta['short_hist'])} 檔"
             f"{('：' + '、'.join(meta['short_hist'])) if meta['short_hist'] else ''}。\n")
    L.append("## ③ 全期 V0-V4 M1-M4 表\n")
    L.append("| 變體 | M1 med (次/年) | M1 p75 | M2 假警報率 (確認數) | M3 med | M3 p90 (n) | M4 med |")
    L.append("|---|---|---|---|---|---|---|")
    for v in ["V0"] + GRAMMAR_ORDER:
        L.append(_vrow(v, res["variants"][v]))
    L.append("")
    L.append("## ④ 平原表\n")
    L.append("R3 判定口徑（預登記補充，跑前鎖定）：平原 = V1 九宮格全格 / V3 三點全點；"
             "「相鄰格」= 單一參數差一檔；「關鍵指標」= M1 med 與 M2；"
             "「相對變動」= |a−b| ÷ 兩格平均。任一相鄰格對任一關鍵指標 >30% → 整變體標「脆弱」。\n")
    L.append("### V1 九宮格（band/days）\n")
    L.append("| band\\days | 2 | 3 | 4 |")
    L.append("|---|---|---|---|")
    for b in (0.96, 0.97, 0.98):
        cells = []
        for d in (2, 3, 4):
            a = res["plateau_v1"][f"{b}/{d}"]
            cells.append(f"M1 {_num(a['m1_med'])} · M2 {_pct(a['m2'])}")
        L.append(f"| {b} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("### V3 三點平原（延伸度門檻）\n")
    L.append("| 門檻 | M1 med | M2 | M3 med | M4 med |")
    L.append("|---|---|---|---|---|")
    for e in ("0.12", "0.15", "0.18"):
        a = res["plateau_v3"][e]
        L.append(f"| {e} | {_num(a['m1_med'])} | {_pct(a['m2'])} | {_pct(a['m3_med'])} | {_num(a['m4_med'])} |")
    L.append("")
    r3 = apply_r3(res)
    for v in ("V1", "V3"):
        bad, viol = r3[v]
        if bad:
            L.append(f"{v} 相鄰格違規（>30%）：" + "；".join(
                f"{k1}↔{k2} {m}={rc*100:.0f}%" for k1, k2, m, rc in viol) + "\n")
        else:
            L.append(f"{v} 平原通過（所有相鄰格關鍵指標相對變動 ≤30%）。\n")
    L.append("## ⑤ 五時代窗排名表（以 M2 升冪，次鍵 M3 med；比率類不受年數分母影響）\n")
    L.append("| 時代窗 | 排名（佳→劣） |")
    L.append("|---|---|")
    all_v = ["V0"] + GRAMMAR_ORDER
    ranks_all = _era_rank(res, all_v)
    for era in ERAS:
        L.append(f"| {era} | " + " > ".join(ranks_all[era]) + " |")
    L.append("")
    L.append("## ⑥ 結論（機械推導，逐條對照 R/S）\n")
    for s in trace:
        L.append(f"- {s}")
    L.append("")
    L.append(f"**機械勝出變體：{winner if winner else '無（全淘汰，維持 V0 現行）'}**\n")
    L.append("> 最終變體選擇與寫入總守則 v2.0 由持有人於季檢拍板；本研究只產生證據，"
             "不修改 state_machine.py / config.py 態④生產規則。\n")
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")


# ── main ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-saved", help="已存寬表 csv(.gz) 路徑，跳過抓價")
    ap.add_argument("--refresh-only", action="store_true",
                    help="只增量更新寬表收盤價並存檔（dated + latest），不跑研究、不動報告/JSON")
    ap.add_argument("--rebuild", action="store_true",
                    help="本機 base + repo closes_daily 切片 → 併成最新寬表（不抓價、不跑研究）")
    args = ap.parse_args()

    if args.rebuild:
        closes, saved, new_cells, n_slices = rebuild_from_slices()
        print(f"  寬表已重建：{closes.shape[1]} 檔 × {closes.shape[0]} 日（截至 "
              f"{closes.index[-1].strftime('%Y-%m-%d')}）")
        print(f"  併入 {n_slices} 支切片 · 新增 {new_cells} 格收盤")
        print(f"    dated  → {saved}")
        print(f"    latest → {LATEST_CLOSES}")
        return

    if args.refresh_only:
        closes, missing, short_hist = build_closes()
        saved = save_closes(closes)
        print(f"  寬表已更新：{closes.shape[1]} 檔 × {closes.shape[0]} 日（截至 "
              f"{closes.index[-1].strftime('%Y-%m-%d')}）")
        print(f"    dated  → {saved}")
        print(f"    latest → {LATEST_CLOSES}")
        if missing:
            print(f"  抓取失敗 {len(missing)} 檔：{', '.join(missing)}")
        if short_hist:
            print(f"  短歷史（<{MIN_BARS} 根，研究時引擎自動跳過）{len(short_hist)} 檔："
                  f"{', '.join(short_hist)}")
        return

    print("── 預登記閘門（跑數據前鎖定）──")
    print(PREREG)
    print("──")

    if args.from_saved:
        closes = pd.read_csv(args.from_saved, index_col=0, parse_dates=True)
        missing, short_hist = [], [c for c in closes.columns
                                   if closes[c].dropna().shape[0] < MIN_BARS]
        saved = Path(args.from_saved)
    else:
        closes, missing, short_hist = build_closes()
        saved = save_closes(closes)
    print(f"  寬表：{closes.shape[1]} 檔 × {closes.shape[0]} 日 → {saved}", file=sys.stderr)

    res = STV.run_study(closes, ERAS)
    winner, trace = select(res)
    res["_meta"] = {
        "asof": closes.index[-1].strftime("%Y-%m-%d"),
        "prereg": PREREG,
        "winner": winner,
        "n_universe": closes.shape[1] + len(missing),
        "missing": missing, "short_history": short_hist,
        "closes_snapshot": str(saved),
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(res, winner, trace, dict(
        asof=res["_meta"]["asof"], n_universe=res["_meta"]["n_universe"],
        n_priced=closes.shape[1], missing=missing, short_hist=short_hist))
    print(f"  JSON → {OUT_JSON}", file=sys.stderr)
    print(f"  報告 → {REPORT_PATH}", file=sys.stderr)
    for s in trace:
        print("  " + s)
    print(f"  機械勝出：{winner if winner else '無（維持 V0）'}")


if __name__ == "__main__":
    main()
