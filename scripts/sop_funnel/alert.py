#!/usr/bin/env python3
"""SOP 漏斗 email 推播 — 板機日寫出 alert 檔給 Action 的寄信步驟。

讀 build.py 產出的 latest.json:today_signals(當日通過全部 veto 的板機事件,
歷史頻率極低 — ledger 58 個訊號僅 3 個 entered),非空時寫 repo 根目錄的
sop_funnel_alert.txt(gitignored);安靜日刪除殘檔。不碰 build.py 的引擎邏輯。

Run: python scripts/sop_funnel/alert.py   (daily-non-fundamental-refresh,
build.py 之後)
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LATEST = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel" / "latest.json"
ALERT = REPO_ROOT / "sop_funnel_alert.txt"


def main() -> int:
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    signals = latest.get("today_signals") or []
    vetoed = latest.get("today_vetoed") or []

    if not signals:
        if ALERT.exists():
            ALERT.unlink()
        print(f"sop-funnel alert: no triggers today ({latest.get('as_of')}), "
              f"vetoed={len(vetoed)}")
        return 0

    lines = [f"SOP 漏斗板機 — {latest.get('as_of')}", ""]
    for e in signals:
        name = e.get("name") or ""
        lines.append(f"🎯 {e.get('ticker')} {name}".rstrip())
        lines.append(f"   進場型態 {e.get('entry_type') or '—'} · 訊號收盤 {e.get('signal_close')}")
        lines.append(f"   停損距離 {e.get('stop_dist_pct')}% · 建議部位 {e.get('suggested_position_pct')}%")
        ec = e.get("earnings_check") or {}
        if ec.get("days_to_earnings") is not None:
            lines.append(f"   距下次財報 {ec['days_to_earnings']} 天"
                         f"{'' if ec.get('ok', True) else ' ⚠ 財報窗口內'}")
        lines.append("")
    if vetoed:
        lines.append(f"(另有 {len(vetoed)} 個訊號被 veto,詳見頁面)")
        lines.append("")
    lines.append("依 SOP 執行;否決紀律與部位公式見頁面。")
    lines.append("詳細: https://research.investmquest.com/dd-screener/sop-funnel.html")
    ALERT.write_text("\n".join(lines), encoding="utf-8")
    print(f"sop-funnel alert: {len(signals)} trigger(s) -> {ALERT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
