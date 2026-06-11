#!/usr/bin/env python3
"""SOP 漏斗 5 年歷史回測 — 含態④減碼幅度 A/B（供 2026-09 季檢）。

⚠ 偏誤明標（頁面照列）：
- 質量閘門凍結今日值（今日過閘的 19 檔回放 5 年）→ survivorship + look-ahead，
  結果僅供「這套技術規則歷史上長怎樣」參考，不是嚴格 point-in-time 回測。
- 同 backtest_entry_state.py 的既有 repo 慣例。

A/B：charter 現行（態④一次減至核心 50%）vs 階梯式（25% + 破 0.94 再 25%）。
進場訊號兩變體完全相同（態④不影響進場），差異純在持有期報酬。

用法：python3 scripts/sop_funnel/backtest.py [--years 5]
輸出：docs/dd-screener/sop-funnel/backtest.json（build.py 下次 render 自動帶入 §4）
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sop_funnel import prices  # noqa: E402
from sop_funnel.engine import (  # noqa: E402
    PARAMS, build_frame, next_trading_close, quality_check, scan_ticker,
    simulate_trade,
)
from sop_funnel.build import DD_LATEST, OUT_DIR  # noqa: E402

BACKTEST_PATH = OUT_DIR / "backtest.json"

VARIANTS = {
    "charter": {"label": "現行：一次減至核心 50%", "t4_staged": False},
    "staged": {"label": "階梯：25% + 破×0.94 再 25%", "t4_staged": True},
}


def _stats(trades: list[dict]) -> dict:
    """雙口徑：closed-only（保守）+ all（open 按期末 mark-to-market）。
    趨勢跟蹤的獲利集中在仍在跑的 open 尾巴，closed-only 對系統有結構性低估
    （被停損的都已關、贏家還掛著）——兩個口徑都給，頁面以 all 為主、closed 為輔。"""
    def _agg(sub):
        rets = sorted(t["sim"]["ret_pct"] for t in sub if t["sim"]["ret_pct"] is not None)
        alphas = [t["sim"]["alpha_pct"] for t in sub if t["sim"].get("alpha_pct") is not None]
        rs = [t["sim"]["r_multiple"] for t in sub if t["sim"]["r_multiple"] is not None]
        hold = sorted(t["sim"]["holding_days"] for t in sub)
        return {
            "n": len(sub),
            "win_rate": round(sum(1 for r in rets if r > 0) / len(rets) * 100, 1) if rets else None,
            "median_ret_pct": rets[len(rets) // 2] if rets else None,
            "mean_ret_pct": round(sum(rets) / len(rets), 2) if rets else None,
            "mean_alpha_pct": round(sum(alphas) / len(alphas), 2) if alphas else None,
            "mean_r": round(sum(rs) / len(rs), 2) if rs else None,
            "median_holding_days": hold[len(hold) // 2] if hold else None,
        }
    closed = [t for t in trades if t["sim"]["status"] == "closed"
              and t["sim"]["ret_pct"] is not None]
    allm = _agg(trades)
    return {
        "n_signals": len(trades),
        "n_trades": len(closed),
        "n_open_at_end": len(trades) - len(closed),
        # all 口徑（主）：open 按期末 mark
        "win_rate": allm["win_rate"],
        "median_ret_pct": allm["median_ret_pct"],
        "mean_ret_pct": allm["mean_ret_pct"],
        "mean_alpha_pct": allm["mean_alpha_pct"],
        "mean_r": allm["mean_r"],
        "median_holding_days": allm["median_holding_days"],
        # closed-only 口徑（輔）
        "closed_only": _agg(closed),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, default=5)
    args = ap.parse_args()

    closes = prices.load_closes()
    spy, _ = prices.load_benchmark(refresh=False)
    quality = json.loads(DD_LATEST.read_text(encoding="utf-8"))
    passers = []
    for s in quality.get("stocks", []):
        p, _, _ = quality_check(s)
        if p:
            passers.append(s["ticker"])
    today = closes.index.max()
    window_start = today - pd.DateOffset(years=args.years)

    results: dict[str, list[dict]] = {k: [] for k in VARIANTS}
    for t in passers:
        if t not in closes.columns:
            continue
        frame = build_frame(closes[t])
        if frame is None:
            continue
        events = [e for e in scan_ticker(frame, True, [])
                  if not e["vetoes"] and window_start <= e["date"] <= today]
        for vkey, vconf in VARIANTS.items():
            params = dict(PARAMS)
            params["t4_staged"] = vconf["t4_staged"]
            busy_until: pd.Timestamp | None = None
            for e in events:
                if busy_until is not None and e["date"] <= busy_until:
                    continue   # 每 ticker 同時一筆
                ntc = next_trading_close(frame.close, e["date"])
                if ntc is None:
                    continue
                res = simulate_trade(frame, ntc[0], params=params)
                end_d = pd.Timestamp(res["exit_date"]) if res["exit_date"] else today
                spy_ret = prices.benchmark_ret_pct(spy, ntc[0], end_d)
                res["spy_ret_pct"] = round(spy_ret, 2) if spy_ret is not None else None
                res["alpha_pct"] = round(res["ret_pct"] - spy_ret, 2) \
                    if (res["ret_pct"] is not None and spy_ret is not None) else None
                results[vkey].append({"ticker": t, "entry_type": e["type"],
                                      "signal_date": str(e["date"].date()), "sim": res})
                busy_until = end_d if res["status"] == "closed" else today

    out = {
        "schema_version": "1.0",
        "run_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_start": str(window_start.date()),
        "window_end": str(today.date()),
        "n_tickers": len(passers),
        "caveat": "質量閘門凍結今日值（survivorship + look-ahead），僅供技術規則參考",
        "variants": {k: {"label": VARIANTS[k]["label"], **_stats(v)}
                     for k, v in results.items()},
        "by_type": {et: _stats([r for r in results["charter"] if r["entry_type"] == et])
                    for et in ("A1", "A2", "B")},
        "trades_charter": [{"ticker": r["ticker"], "type": r["entry_type"],
                            "signal_date": r["signal_date"],
                            "entry_date": r["sim"]["entry_date"],
                            "exit_date": r["sim"]["exit_date"],
                            "exit_reason": r["sim"]["exit_reason"],
                            "ret_pct": r["sim"]["ret_pct"],
                            "alpha_pct": r["sim"].get("alpha_pct"),
                            "r": r["sim"]["r_multiple"],
                            "status": r["sim"]["status"]}
                           for r in sorted(results["charter"],
                                           key=lambda x: x["signal_date"])],
    }
    BACKTEST_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1),
                             encoding="utf-8")
    for k, v in out["variants"].items():
        print(f"{k}: {v}")
    print(f"by_type: {json.dumps(out['by_type'], ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
