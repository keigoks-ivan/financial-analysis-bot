"""一次性歷史回填：加權股價指數與成交值（TWSE）、櫃買指數與成交值（TPEx）。

【不隨每日流程執行】每日 fetcher（tw_twse／tw_tpex）只抓最近一兩個月，靠 store 合併規則累積；
這支只在需要補長歷史時手動跑一次：

    python scripts/macro_db/sources/tw_backfill_twse.py --dry-run            # 只印要打幾次請求與預估時間
    python scripts/macro_db/sources/tw_backfill_twse.py --target twse        # 1990-01 起
    python scripts/macro_db/sources/tw_backfill_twse.py --target tpex        # 櫃買指數 2000-01 起、成交值 1999-06 起

只用「月資料」端點（一次請求回整個月），每次請求間隔 GAP 秒（預設 3 秒，不要調小，避免被 TWSE／TPEx 封鎖）。
預估請求數與時間（以 2026-10 為終點、3 秒間隔，不含網路延遲）：
    twse  1990-01 ~ 2026-10 = 442 個月 -> 442 次 ≈ 22 分鐘（一次請求同時得到收盤與成交值）
    tpex  inx 2000-01 起 322 次 + tradingIndex 1999-06 起 329 次 = 651 次 ≈ 33 分鐘
    全部約 1100 次 ≈ 55 分鐘。中斷後重跑安全（store 合併：新值覆蓋、舊檔保留）。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))  # scripts/

from macro_db import store  # noqa: E402
from macro_db.sources import tw_common as C  # noqa: E402
from macro_db.sources import tw_tpex, tw_twse  # noqa: E402

GAP = 3.0


def months(start: tuple[int, int], end: tuple[int, int]):
    y, m = start
    while (y, m) <= end:
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def _get(url: str, key: str):
    C.throttle(key, GAP)
    return json.loads(C.http_get(url).decode("utf-8-sig"))


def backfill_twse(start, end, dry):
    close, turnover = [], []
    n = 0
    for y, m in months(start, end):
        n += 1
        if dry:
            continue
        d = _get(f"{tw_twse.BASE}afterTrading/FMTQIK?date={y:04d}{m:02d}01&response=json", "twse")
        close.extend(tw_twse.fmtqik_obs(d, 4))
        turnover.extend(tw_twse.fmtqik_obs(d, 2))
    if not dry:
        store.write_merged("tw.mk.taiex_close", C.clean_obs(close))
        store.write_merged("tw.mk.twse_turnover", C.clean_obs(turnover))
    return n


def backfill_tpex(inx_start, trading_start, end, dry):
    n = 0
    for sid, path, col, start in (("tw.mk.tpex_close", "indexInfo/inx", 4, inx_start),
                                  ("tw.mk.tpex_turnover", "afterTrading/tradingIndex", 2, trading_start)):
        rows = []
        for y, m in months(start, end):
            n += 1
            if dry:
                continue
            d = _get(f"{tw_tpex.BASE}{path}?date={y:04d}%2F{m:02d}%2F01&id=&response=json", "tpex")
            rows.extend(tw_tpex.month_obs(d, col))
        if not dry:
            store.write_merged(sid, C.clean_obs(rows))
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["twse", "tpex", "all"], default="all")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    t = date.today()
    end = (t.year, t.month)
    n = 0
    if a.target in ("twse", "all"):
        n += backfill_twse((1990, 1), end, a.dry_run)
    if a.target in ("tpex", "all"):
        n += backfill_tpex((2000, 1), (1999, 6), end, a.dry_run)
    print(f"{'預計' if a.dry_run else '已送出'}請求 {n} 次，約 {n * GAP / 60:.0f} 分鐘（間隔 {GAP:g} 秒）")


if __name__ == "__main__":
    main()
