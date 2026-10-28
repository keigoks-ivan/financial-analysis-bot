#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主動式 ETF「本站挑選」候選數據（雲端排程的證據包）。

22 檔每檔一列：含息報酬（多個區間）、最大回檔、近三年週報酬 beta、頁面自有指標
（遠期本益比、前十大、20／60 日命中率、持有天數、規模、費率），加持股重疊矩陣。

  python3 scripts/active_etf/picks_candidates.py            # 寫 data/active_etf/picks_candidates.json
  python3 scripts/active_etf/picks_candidates.py --brief    # 同上，並把證據包印到 stdout（≤ 8 KB）
  python3 scripts/active_etf/picks_candidates.py --from-json --brief   # 不抓價，從現有 JSON 印證據包

--brief 是模型唯一可以引用的數字來源。報酬全部用 yfinance auto_adjust=True 的還原收盤（含息）；
每檔抓失敗不會讓整支掛掉，該格寫 null 並進 notes。雲端 CI 只有 yfinance／pandas／numpy／requests。
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT / "scripts" / "etf_dash"))  # append：etf_dash 也有同名 picks_candidates.py，自己目錄要排前面

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

FUND_DATA_DIR = REPO_ROOT / "docs" / "active-etf" / "data"
OUT_PATH = REPO_ROOT / "data" / "active_etf" / "picks_candidates.json"
BENCH = "0050.TW"
BENCH_CODE = "0050"
DOWNLOAD_START = "2021-12-01"
BRIEF_MAX_BYTES = 8 * 1024

# 固定錨點日（舊基金的共同區間、持股資料起日、近期高點）
ANCHORS = [("s20250715", "2025-07-15"), ("s20260211", "2026-02-11"), ("s20260620", "2026-06-20")]
BEAR_2022 = ("2022-01-03", "2022-10-12")
BETA_MIN_WEEKS = 26

RET_KEYS = ["r3m", "r6m", "ytd", "r1y", "r3y", "bear2022", "s20250715", "s20260211", "s20260620", "since_listing"]
MDD_KEYS = ["m1y", "m3y", "s20250715", "since_listing"]
PAGE_KEYS = ["fwd_pe", "fwd_pe_coverage_pct", "top10_pct", "hit20_pct", "n20", "hit60_pct", "n60",
             "avg_hold_days", "aum_100m_twd", "fee_mgmt_pct", "fee_custody_pct",
             "eps_chg_90d_pct", "active_share_pct", "holdings_as_of"]


# ── 價格與報酬 ─────────────────────────────────────────────────────────────
def download_adjusted(tickers: list[str], start: str) -> tuple[dict, list[str]]:
    """回傳 ({ticker: Series(index=YYYY-MM-DD 字串, 還原收盤)}, 失敗清單)。"""
    import yfinance as yf  # 延後 import：--from-json 不需要
    import build_etf_dash as etfdash

    errors: list[str] = []
    df = None
    try:
        df = etfdash.yf_call_with_backoff(
            lambda: yf.download(tickers, start=start, group_by="ticker", progress=False,
                                auto_adjust=True, threads=True),
            label=f"picks candidates ({len(tickers)} tickers)")
    except Exception as e:  # noqa: BLE001
        errors.append(f"批次下載失敗：{e}")
    out: dict = {}
    if df is None or df.empty:
        return out, errors or ["批次下載沒有資料"]
    top = set(df.columns.get_level_values(0)) if isinstance(df.columns, pd.MultiIndex) else set()
    for tk in tickers:
        try:
            if isinstance(df.columns, pd.MultiIndex):
                if tk not in top:
                    errors.append(f"{tk}: 下載結果沒有這個代號")
                    continue
                s = df[tk]["Close"]
            else:  # 只有一檔
                s = df["Close"]
            s = s.dropna()  # Yahoo 午夜後最新一根可能全 NaN，丟掉
            if s.empty:
                errors.append(f"{tk}: 沒有有效收盤價")
                continue
            s.index = [pd.Timestamp(i).strftime("%Y-%m-%d") for i in s.index]
            out[tk] = s.astype(float)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{tk}: {e}")
    return out, errors


def _on_or_after(s: pd.Series, d: str):
    idx = s.index[s.index >= d]
    return idx[0] if len(idx) else None


def _on_or_before(s: pd.Series, d: str):
    idx = s.index[s.index <= d]
    return idx[-1] if len(idx) else None


def _pct(a: float, b: float):
    return round((b / a - 1) * 100, 2)


def _window_mdd(s: pd.Series, d0: str, d1: str):
    w = s[(s.index >= d0) & (s.index <= d1)]
    if len(w) < 2:
        return None
    return round(float((w / w.cummax() - 1).min()) * 100, 2)


def _back(as_of: str, years: int = 0, months: int = 0) -> str:
    d = pd.Timestamp(as_of) - pd.DateOffset(years=years, months=months)
    return d.strftime("%Y-%m-%d")


def windows(as_of: str) -> dict:
    """區間定義：key -> (kind, base 規則參數)。kind=back 用「as_of 往回推」取 base 日當天或之前最後一筆；
    kind=from 用「該日當天或之後第一筆」（與 picks.py 的起算日規則一致）。"""
    w = {
        "r3m": ("back", _back(as_of, months=3)), "r6m": ("back", _back(as_of, months=6)),
        "ytd": ("back", f"{int(as_of[:4]) - 1}-12-31"),
        "r1y": ("back", _back(as_of, years=1)), "r3y": ("back", _back(as_of, years=3)),
        "bear2022": ("span", BEAR_2022),
    }
    for k, d in ANCHORS:
        w[k] = ("from", d)
    w["since_listing"] = ("listing", None)
    return w


def returns_for(s: pd.Series, as_of: str) -> dict:
    """一檔的各區間含息報酬（%）。基金歷史不足（第一筆收盤晚於該區間起算日）→ None。"""
    out = {k: None for k in RET_KEYS}
    end_d = _on_or_before(s, as_of)
    if end_d is None:
        return out
    first = s.index[0]
    for k, (kind, arg) in windows(as_of).items():
        if kind == "back":
            if first > arg:
                continue
            b = _on_or_before(s, arg)
            out[k] = _pct(s[b], s[end_d]) if b is not None and b < end_d else None
        elif kind == "from":
            if first > arg:
                continue
            b = _on_or_after(s, arg)
            out[k] = _pct(s[b], s[end_d]) if b is not None and b < end_d else None
        elif kind == "span":
            if first > arg[0]:
                continue
            b, e = _on_or_after(s, arg[0]), _on_or_before(s, arg[1])
            out[k] = _pct(s[b], s[e]) if b is not None and e is not None and b < e else None
        else:  # listing
            out[k] = _pct(s[first], s[end_d]) if first < end_d else None
    return out


def mdd_for(s: pd.Series, as_of: str) -> dict:
    out = {k: None for k in MDD_KEYS}
    end_d = _on_or_before(s, as_of)
    if end_d is None:
        return out
    first = s.index[0]
    for k, arg in (("m1y", _back(as_of, years=1)), ("m3y", _back(as_of, years=3)), ("s20250715", "2025-07-15")):
        if first > arg:
            continue
        b = _on_or_after(s, arg)
        out[k] = _window_mdd(s, b, end_d) if b is not None else None
    out["since_listing"] = _window_mdd(s, first, end_d)
    return out


def beta_for(s: pd.Series, bench: pd.Series, as_of: str) -> tuple:
    """近三年（含上市以來較短者）週報酬 beta 對基準。週數不足 BETA_MIN_WEEKS → (None, n)。"""
    lo = _back(as_of, years=3)
    a = s[(s.index >= lo) & (s.index <= as_of)]
    b = bench[(bench.index >= lo) & (bench.index <= as_of)]
    if len(a) < 10:
        return None, 0
    df = pd.DataFrame({"f": a, "b": b}).dropna()
    df.index = pd.to_datetime(df.index)
    wk = df.resample("W-FRI").last().dropna().pct_change().dropna()
    n = len(wk)
    if n < BETA_MIN_WEEKS:
        return None, n
    var = float(np.var(wk["b"], ddof=1))
    if var <= 0:
        return None, n
    return round(float(np.cov(wk["f"], wk["b"], ddof=1)[0, 1]) / var, 3), n


# ── 頁面自有指標與持股重疊 ──────────────────────────────────────────────────
def _num(x):
    return None if x is None else round(float(x), 4)


def page_metrics(fund: dict) -> dict:
    """照各基金頁面 JSON 抄；沒有的欄位 None。費率不在頁面資料內，固定 None。"""
    pt = ((fund.get("manager_skill") or {}).get("post_trade") or {}).get("buys") or {}
    p20, p60 = pt.get("20") or {}, pt.get("60") or {}
    wpe = fund.get("weighted_forward_pe")
    if isinstance(wpe, dict):
        pe, pe_cov = wpe.get("value"), wpe.get("coverage_pct")
    else:
        pe, pe_cov = wpe, None
    hp = (fund.get("operations") or {}).get("holding_period") or {}
    aum = (fund.get("twse_aum") or {}).get("aum_100m_twd")
    return {
        "fwd_pe": _num(pe), "fwd_pe_coverage_pct": _num(pe_cov),
        "top10_pct": _num(fund.get("top10_concentration_pct")),
        "hit20_pct": _num(p20.get("hit_rate_pct")), "n20": p20.get("n_events"),
        "hit60_pct": _num(p60.get("hit_rate_pct")), "n60": p60.get("n_events"),
        "avg_hold_days": _num(hp.get("avg_days")), "aum_100m_twd": _num(aum),
        "fee_mgmt_pct": None, "fee_custody_pct": None,
        "eps_chg_90d_pct": _num(fund.get("eps_chg_pct_90d")),
        "active_share_pct": _num(fund.get("active_share_vs_0050_pct")),
        "holdings_as_of": fund.get("holdings_as_of") or fund.get("as_of"),
    }


def overlap_pct(a: dict, b: dict):
    wa = {h["ticker"]: float(h.get("weight_pct") or 0) for h in (a.get("holdings") or [])}
    wb = {h["ticker"]: float(h.get("weight_pct") or 0) for h in (b.get("holdings") or [])}
    if not wa or not wb:
        return None
    return round(sum(min(wa.get(t, 0), wb.get(t, 0)) for t in set(wa) | set(wb)), 2)


def load_funds() -> dict:
    out = {}
    for p in sorted(FUND_DATA_DIR.glob("*.json")):
        if re.fullmatch(r"\d{5}[A-Z]", p.stem):
            try:
                out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                pass
    return out


def load_bench_page() -> dict:
    try:
        ov = json.loads((FUND_DATA_DIR / "overview.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    for f in ov.get("funds") or []:
        if f.get("code") == BENCH_CODE:
            return f
    return {}


# ── 組候選資料 ─────────────────────────────────────────────────────────────
def build_candidates() -> dict:
    funds = load_funds()
    codes = sorted(funds)
    notes: list[str] = []
    tickers = [c + ".TW" for c in codes] + [BENCH]
    px, errs = download_adjusted(tickers, DOWNLOAD_START)
    notes += errs
    bench_s = px.get(BENCH)
    if bench_s is None:
        raise RuntimeError("抓不到 0050.TW 還原收盤，無法定 as_of：" + "；".join(errs))
    as_of = bench_s.index[-1]

    rows = []
    for c in codes:
        f = funds[c]
        s = px.get(c + ".TW")
        row = {"code": c, "name": f.get("name"), "issuer": f.get("issuer"), "listed_on": None,
               "last_date": None, "n_days": 0,
               "returns": {k: None for k in RET_KEYS}, "mdd": {k: None for k in MDD_KEYS},
               "beta_3y": None, "beta_weeks": 0}
        if s is not None:
            row["listed_on"] = s.index[0]
            row["last_date"] = _on_or_before(s, as_of)
            row["n_days"] = int(len(s))
            row["returns"] = returns_for(s, as_of)
            row["mdd"] = mdd_for(s, as_of)
            row["beta_3y"], row["beta_weeks"] = beta_for(s, bench_s, as_of)
            if row["last_date"] != as_of:
                notes.append(f"{c}: 最新收盤 {row['last_date']} 早於 as_of {as_of}，報酬算到該日")
        else:
            notes.append(f"{c}: 沒有價格，報酬與回檔全部留空")
        row.update(page_metrics(f))
        rows.append(row)

    bp = load_bench_page()
    # 0050 的「上市起」沒有意義（下載只從 DOWNLOAD_START 起），留空
    b_ret, b_mdd = returns_for(bench_s, as_of), mdd_for(bench_s, as_of)
    b_ret["since_listing"] = None
    b_mdd["since_listing"] = None
    bench_row = {"code": BENCH_CODE, "name": "元大台灣50", "listed_on": None, "last_date": as_of,
                 "returns": b_ret, "mdd": b_mdd,
                 "fwd_pe": _num((bp.get("weighted_forward_pe"))), "eps_chg_90d_pct": _num(bp.get("eps_chg_pct_90d"))}

    overlap = {}
    for i, a in enumerate(codes):
        for b in codes[i + 1:]:
            v = overlap_pct(funds[a], funds[b])
            if v is None:
                notes.append(f"{a}|{b}: 缺持股，重疊留空")
            overlap[f"{a}|{b}"] = v

    ha = sorted({r["holdings_as_of"] for r in rows if r["holdings_as_of"]})
    if ha:
        notes.append(f"頁面指標（本益比、前十大、命中率、持有天數、規模、重疊）取自各基金 JSON，持股日 {ha[0]}～{ha[-1]}")
    notes.append("費率不在頁面資料內，fee_mgmt_pct／fee_custody_pct 一律留空")
    notes.append("beta＝近三年（含上市以來不足三年者）週報酬對 0050，週數不足 "
                 f"{BETA_MIN_WEEKS} 週留空；上市日取自 Yahoo 第一筆收盤，可能晚於實際掛牌日")
    return {"schema": "picks-candidates-v1", "as_of": as_of, "benchmark": BENCH,
            "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "funds": rows, "benchmark_row": bench_row, "overlap": overlap, "notes": notes}


# ── 證據包（純文字）────────────────────────────────────────────────────────
def _f(v, signed=False, nd=1):
    if v is None:
        return "na"
    return f"{v:+.{nd}f}" if signed else f"{v:.{nd}f}"


def _hit(h, n):
    return "na" if h is None else f"{h:.1f}({n})"


def render_brief(c: dict) -> str:
    """從 picks_candidates 的 dict 畫證據包。--brief 與 picks_register.py（跑文字檢查）共用。"""
    funds = c["funds"]
    br = c["benchmark_row"]
    L = []
    L.append(f"本站挑選候選證據包（主動式 ETF 22 檔）as_of {c['as_of']}，基準 0050。")
    L.append("這份是唯一可引用的數字來源。報酬為 Yahoo 還原收盤（含息），單位 %；na＝歷史不足或無資料；"
             "區間 0715／0211／0620 指自 2025-07-15、2026-02-11、2026-06-20 起。")
    # A 報酬
    keys = [("r3m", "3m"), ("r6m", "6m"), ("ytd", "YTD"), ("r1y", "1y")]
    for k, lab in (("r3y", "3y"), ("bear2022", "bear22")):
        if any(r["returns"].get(k) is not None for r in funds):
            keys.append((k, lab))
    keys += [("s20250715", "0715"), ("s20260211", "0211"), ("s20260620", "0620"), ("since_listing", "listed")]
    L.append("")
    L.append("[A 含息報酬 %] code 名稱 上市日 | " + " ".join(lab for _, lab in keys))
    for r in funds:
        L.append(f"{r['code']} {r['name']} {r['listed_on'] or 'na'} | " +
                 " ".join(_f(r["returns"].get(k), True) for k, _ in keys))
    L.append(f"{br['code']} {br['name']} na | " +
             " ".join(_f(br["returns"].get(k), True) for k, _ in keys))
    # B 風險與規模
    L.append("")
    L.append("[B 最大回檔 % / beta / 規模] code | 1y 3y 0715起 上市起 | beta(週數) | 規模億")
    for r in funds:
        m = r["mdd"]
        L.append(f"{r['code']} | {_f(m.get('m1y'))} {_f(m.get('m3y'))} {_f(m.get('s20250715'))} "
                 f"{_f(m.get('since_listing'))} | {_f(r['beta_3y'], nd=2)}({r['beta_weeks']}) | "
                 f"{_f(r['aum_100m_twd'], nd=0)}")
    bm = br["mdd"]
    L.append(f"{br['code']} | {_f(bm.get('m1y'))} {_f(bm.get('m3y'))} {_f(bm.get('s20250715'))} "
             f"{_f(bm.get('since_listing'))} | 1.00 |")
    # C 結構
    L.append("")
    L.append("[C 頁面指標] code | 遠期PE倍 | 前十大% | 20日命中%(事件) | 60日命中%(事件) | 持有天數 | EPS90日修正% | 主動度%")
    for r in funds:
        L.append(f"{r['code']} | {_f(r['fwd_pe'])} | {_f(r['top10_pct'])} | {_hit(r['hit20_pct'], r['n20'])} | "
                 f"{_hit(r['hit60_pct'], r['n60'])} | {_f(r['avg_hold_days'], nd=0)} | "
                 f"{_f(r['eps_chg_90d_pct'], True)} | {_f(r['active_share_pct'])}")
    L.append(f"{br['code']} | {_f(br.get('fwd_pe'))} | | | | | {_f(br.get('eps_chg_90d_pct'), True)} |")
    # D 重疊矩陣
    codes = [r["code"] for r in funds]
    L.append("")
    L.append("[D 持股加權重疊 %] 列與欄為代號後三碼（含 A），下三角")
    short = [x[2:] for x in codes]
    L.append("     " + " ".join(f"{s:>4}" for s in short[:-1]))
    for i in range(1, len(codes)):
        cells = []
        for j in range(i):
            v = c["overlap"].get(f"{codes[j]}|{codes[i]}")
            cells.append(f"{v:4.1f}" if v is not None else "  na")
        L.append(f"{short[i]:>4} " + " ".join(cells))
    if c.get("notes"):
        L.append("")
        L.append("[註記]")
        for n in c["notes"]:
            L.append("- " + n)
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brief", action="store_true", help="把證據包印到 stdout（≤ 8 KB）")
    ap.add_argument("--from-json", action="store_true", help="不抓價，用現有 picks_candidates.json")
    a = ap.parse_args()
    if a.from_json:
        cands = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    else:
        cands = build_candidates()
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(json.dumps(cands, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if a.brief:
        text = render_brief(cands)
        size = len(text.encode("utf-8"))
        print(text, end="")
        if size > BRIEF_MAX_BYTES:
            print(f"WARN: brief {size} bytes 超過 {BRIEF_MAX_BYTES}", file=sys.stderr)
            return 2
    else:
        print(f"wrote {OUT_PATH}（as_of {cands['as_of']}，{len(cands['funds'])} 檔，notes {len(cands['notes'])}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
