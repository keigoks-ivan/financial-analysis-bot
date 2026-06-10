#!/usr/bin/env python3
"""五狀態機 §9 驗收自測。執行：python3 scripts/state_machine/test_state_machine.py

涵蓋 SPEC §9 的 7 條：①狀態流序、②財報 gap 當日確認、③態③一次性減碼、
④優先序 ②+④→④、⑤B 型板機恰亮一天、⑥週間凍結、⑦隱私（無部位數字）。
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE_DIR))

import pandas as pd  # noqa: E402

import state_machine as SM  # noqa: E402
from indicators import compute_indicators  # noqa: E402

_fails = []


def check(name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        _fails.append(name)


# ── 指標 / ctx 工廠 ─────────────────────────────────────────────────────────
def mk_ind(**over):
    """乾淨的態① indicator dict；以 over 覆寫誘發特定條件。"""
    d = dict(
        close=150.0, prev_close=149.0, open=150.0,
        ath=200.0, ath_date="2025-01-01", is_new_ath_today=False,
        prev_is_new_ath=False, ath_prev=200.0, pct_vs_ath=-0.25, prev_pct_vs_ath=-0.25,
        ma52w=120.0, ma104w=110.0, ma200w=100.0, alignment=True, short_history=False,
        n_weeks=260, is_week_complete=False,
        bb_mid=130.0, bb_sigma=10.0, bb_upper2=150.0, bb_upper3=160.0,
        bb_position=2.0, frozen_weekly_close=148.0, frozen_week_date="2026-06-05",
        week_high_so_far=149.0, ma60d=140.0,
        pct_vs_52w=0.25, pct_vs_60d=0.07,
        above_52w=True, below_52w=False, below_60d=False,
        vol=1e6, vol_ma20=1e6, volume_ratio=1.0, volume_spike=False,
        last_bar_date="2026-06-10", prev_bar_date="2026-06-09", last_bar_is_friday=False,
    )
    d.update(over)
    return d


def mk_ctx(**over):
    d = dict(held=True, quality_pass=True, today="2026-06-10", data_error=False,
             seed=False, next_earnings=None, earnings_blackout=False,
             earnings_unknown=False, is_first_day_after_earnings=False)
    d.update(over)
    return d


def seed_state(ticker, ind, ctx):
    return SM.evaluate(ticker, ind, None, None, mk_ctx(**{**ctx, "seed": True}))


# ── §9.1 狀態流序：① → ④ → ⑤待確認 → ⑤ ───────────────────────────────────
def test_state_flow():
    print("§9.1 狀態流序 ①→④→⑤待確認→⑤")
    r0 = seed_state("T", mk_ind(), dict(held=True))
    check("seed 起於態①", r0["state"] == 1)
    # 態④：跌破 60MA 但仍站上 52w
    r1 = SM.evaluate("T", mk_ind(below_60d=True, pct_vs_60d=-0.02),
                     r0["mem"], None, mk_ctx())
    check("跌破60MA→態④", r1["state"] == 4, f"got {r1['state']}")
    check("態④ held→TRIM_TO_CORE_50", r1["action"] == "TRIM_TO_CORE_50", r1["action"])
    # 非週五破 52w → 維持態④ + 黃色預警
    r2 = SM.evaluate("T", mk_ind(close=115.0, below_52w=True, below_60d=True,
                                 last_bar_is_friday=False),
                     r1["mem"], None, mk_ctx())
    check("非週五破線→維持④+pending", r2["state"] == 4 and "pending_state5_warning" in r2["flags"],
          f"state={r2['state']} flags={r2['flags']}")
    check("pending→WARN_PENDING_5", r2["action"] == "WARN_PENDING_5", r2["action"])
    # 週五收盤確認破線 → 態⑤
    r3 = SM.evaluate("T", mk_ind(close=115.0, below_52w=True, frozen_weekly_close=115.0,
                                 is_week_complete=True, last_bar_is_friday=True),
                     r2["mem"], None, mk_ctx())
    check("週五確認→態⑤", r3["state"] == 5, f"got {r3['state']}")
    check("態⑤ held→EXIT_ALL", r3["action"] == "EXIT_ALL", r3["action"])
    check("態⑤ exited 記憶=true", r3["mem"]["exited"] is True)


# ── §9.2 財報 gap：當日確認態⑤、不等週五 ─────────────────────────────────────
def test_earnings_gap():
    print("§9.2 財報 gap 當日確認")
    r0 = seed_state("T", mk_ind(), dict(held=True))
    r1 = SM.evaluate("T", mk_ind(open=110.0, close=112.0, below_52w=True,
                                 last_bar_is_friday=False),   # 非週五
                     r0["mem"], None, mk_ctx(is_first_day_after_earnings=True))
    check("gap 開低破線+收破線→當日態⑤", r1["state"] == 5, f"got {r1['state']}")
    check("flag earnings_gap_break", "earnings_gap_break" in r1["flags"])
    check("非週五也確認(不等週五)", r1["mem"]["exited"] is True)


# ── §9.3 態③一次性：TRIM_1_3 只輸出一次 ──────────────────────────────────────
def test_overheat_once():
    print("§9.3 態③一次性減碼")
    r0 = seed_state("T", mk_ind(), dict(held=True))
    touch = dict(week_high_so_far=170.0, bb_upper3=160.0, frozen_weekly_close=158.0,
                 bb_upper2=150.0)  # touch_3σ true；frozen 仍 > upper2（episode 不結束）
    r1 = SM.evaluate("T", mk_ind(**touch), r0["mem"], None, mk_ctx())
    r2 = SM.evaluate("T", mk_ind(**touch), r1["mem"], None, mk_ctx())
    r3 = SM.evaluate("T", mk_ind(**touch), r2["mem"], None, mk_ctx())
    check("第1週觸3σ→TRIM_1_3", r1["action"] == "TRIM_1_3", r1["action"])
    check("第2週→NO_ADD(不重複減)", r2["action"] == "NO_ADD", r2["action"])
    check("第3週→NO_ADD", r3["action"] == "NO_ADD", r3["action"])
    check("episode active 維持", r3["mem"]["overheat_episode"]["active"] is True)
    # 回落 2σ 內 → episode 結束；再觸 3σ = 新事件、重新減
    end = dict(week_high_so_far=145.0, frozen_weekly_close=145.0, bb_upper2=150.0, bb_upper3=160.0)
    r4 = SM.evaluate("T", mk_ind(**end), r3["mem"], None, mk_ctx())
    r5 = SM.evaluate("T", mk_ind(**touch), r4["mem"], None, mk_ctx())
    check("回落後再觸3σ→新事件再 TRIM_1_3", r5["action"] == "TRIM_1_3", r5["action"])


# ── §9.4 優先序：同日 ②+④ → 輸出 ④ ─────────────────────────────────────────
def test_priority():
    print("§9.4 優先序 ②+④→④")
    r0 = seed_state("T", mk_ind(), dict(held=True))
    # 同時：overheat_zone（frozen∈(upper2,upper3]）且 below_60d&above_52w
    both = mk_ind(below_60d=True, pct_vs_60d=-0.01,
                  frozen_weekly_close=155.0, bb_upper2=150.0, bb_upper3=160.0,
                  week_high_so_far=155.0)
    r1 = SM.evaluate("T", both, r0["mem"], None, mk_ctx())
    check("同日 ②+④ → 態④", r1["state"] == 4, f"got {r1['state']}（應 4）")


# ── §9.5 B 型板機：突破→回測→站回前高 恰亮一天 ──────────────────────────────
def test_btype_once():
    print("§9.5 B 型板機恰亮一天")
    base = dict(held=False, quality_pass=True)
    r0 = seed_state("T", mk_ind(), base)
    # day1 突破新高：is_new_ath_today, 前一日未創 → 登記 breakout(prior_ath=200)
    r1 = SM.evaluate("T", mk_ind(close=205.0, is_new_ath_today=True, prev_is_new_ath=False,
                                 ath=205.0, ath_prev=200.0, pct_vs_ath=0.0, prev_pct_vs_ath=-0.02),
                     r0["mem"], r0["breakout"], mk_ctx(**base))
    check("突破首日登記 breakout", r1["breakout"] and r1["breakout"]["prior_ath"] == 200.0,
          str(r1["breakout"]))
    # day2 收盤回落進入 prior_ath±2%（200×[0.98,1.02]=[196,204]）→ entered_band
    r2 = SM.evaluate("T", mk_ind(close=199.0), r1["mem"], r1["breakout"], mk_ctx(**base))
    check("回測進帶→entered_band", r2["breakout"]["entered_band"] is True)
    check("回測當日尚無 ENTRY_B", r2["entry_signal"] != "ENTRY_B", str(r2["entry_signal"]))
    # day3 收盤站回前高之上（≥200）→ ENTRY_B
    r3 = SM.evaluate("T", mk_ind(close=201.0), r2["mem"], r2["breakout"], mk_ctx(**base))
    check("站回前高→ENTRY_B", r3["entry_signal"] == "ENTRY_B", str(r3["entry_signal"]))
    check("first_retest_done 翻 true", r3["breakout"]["first_retest_done"] is True)
    # day4 再站回 → 不再給前高訊號
    r4 = SM.evaluate("T", mk_ind(close=202.0), r3["mem"], r3["breakout"], mk_ctx(**base))
    check("二次回測不再給前高 ENTRY_B", r4["entry_signal"] != "ENTRY_B", str(r4["entry_signal"]))


# ── §9.6 週間凍結：週三判定用上週五的週線值 ──────────────────────────────────
def test_weekly_freeze():
    print("§9.6 週間凍結（週三用上週五週線值）")
    # 造 ~80 週日線（週一～週五），週收盤遞增；最後一根停在週三。
    start = datetime(2024, 1, 1)  # Monday
    dates, closes = [], []
    price = 100.0
    d = start
    for _ in range(80 * 5 + 3):
        if d.weekday() < 5:  # 工作日
            dates.append(d)
            closes.append(price)
            price += 0.5
        d += timedelta(days=1)
    # 截到某個週三
    while dates[-1].weekday() != 2:  # Wednesday
        dates.pop(); closes.pop()
    idx = pd.DatetimeIndex(dates)
    df = pd.DataFrame({"Open": closes, "High": closes, "Low": closes,
                       "Close": closes, "Volume": [1e6] * len(closes)}, index=idx)
    ind = compute_indicators(df)
    # 手算：丟掉當週（週三未完成），用到上週五的週收盤序列算 MA52w
    weekly = df["Close"].resample("W-FRI").last().dropna()
    frozen = weekly.iloc[:-1]                    # 丟當週
    expect_ma52 = float(frozen.iloc[-52:].mean())
    last_friday = frozen.index[-1].strftime("%Y-%m-%d")
    check("is_week_complete=False(週三)", ind["is_week_complete"] is False)
    check("frozen_week_date=上週五", ind["frozen_week_date"] == last_friday,
          f"{ind['frozen_week_date']} vs {last_friday}")
    check("MA52w==凍結到上週五的手算值",
          ind["ma52w"] is not None and abs(ind["ma52w"] - expect_ma52) < 1e-6,
          f"{ind['ma52w']} vs {expect_ma52}")


# ── §9.7 隱私：daily.json row 無任何部位數字 ─────────────────────────────────
def test_privacy():
    print("§9.7 隱私（無部位數字）")
    from run_daily import _daily_row
    r0 = seed_state("T", mk_ind(), dict(held=True))
    ectx = dict(next_earnings="2026-06-18", earnings_blackout=False,
                earnings_unknown=False, is_first_day_after_earnings=False)
    row = _daily_row("T", True, r0, mk_ind(), ectx)
    forbidden = {"shares", "qty", "quantity", "cost", "cost_basis", "amount",
                 "value", "market_value", "position_size", "dollars", "notional"}
    keys = set(row.keys()) | set(row["metrics"].keys())
    check("held 為布林", isinstance(row["held"], bool))
    check("無任何部位欄位", not (keys & forbidden), f"leaked: {keys & forbidden}")
    check("metrics 僅允許白名單",
          set(row["metrics"].keys()) <= {"close", "pct_vs_52w", "pct_vs_60d",
                                          "pct_vs_ath", "bb_position", "volume_ratio",
                                          "next_earnings"},
          str(set(row["metrics"].keys())))


def main():
    for t in (test_state_flow, test_earnings_gap, test_overheat_once, test_priority,
              test_btype_once, test_weekly_freeze, test_privacy):
        t()
    print()
    if _fails:
        print(f"❌ {len(_fails)} FAIL: {_fails}")
        sys.exit(1)
    print("✅ 全部 §9 自測通過")


if __name__ == "__main__":
    main()
