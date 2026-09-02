#!/usr/bin/env python3
"""SOP 漏斗 email 推播 — 板機日寫出 alert 檔給 Action 的寄信步驟。

讀 build.py 產出的 latest.json:today_signals(當日通過全部 veto 的板機事件,
歷史頻率極低 — ledger 58 個訊號僅 3 個 entered),非空時寫 repo 根目錄的
sop_funnel_alert.txt(gitignored,純文字 fallback body,byte-identical 邏輯不變);
同時寫 sop_funnel_mail.html(美觀版 HTML,gitignored,html_body 用);
安靜日兩者皆刪除殘檔。不碰 build.py 的引擎邏輯。

Run: python scripts/sop_funnel/alert.py   (daily-non-fundamental-refresh,
build.py 之後)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from mail_html import esc, frame, note, one_minute, pill, section, table, tiles  # noqa: E402

LATEST = REPO_ROOT / "docs" / "dd-screener" / "sop-funnel" / "latest.json"
ALERT = REPO_ROOT / "sop_funnel_alert.txt"
ALERT_HTML = REPO_ROOT / "sop_funnel_mail.html"

PAGE_URL = "https://research.investmquest.com/dd-screener/sop-funnel.html"


def build_html(as_of: str, signals: list, vetoed: list) -> str:
    bullets = [
        f"<strong>{esc(e.get('ticker'))}</strong>（{esc(e.get('name') or '—')}）"
        f"進場型態 {esc(e.get('entry_type') or '—')}，建議部位 "
        f"{esc(e.get('suggested_position_pct'))}%"
        for e in signals
    ]
    tile_items = [
        ("今日板機訊號", str(len(signals)), None),
        ("被 veto 訊號", str(len(vetoed)), None),
    ]
    pos_vals = [e.get("suggested_position_pct") for e in signals
                if isinstance(e.get("suggested_position_pct"), (int, float))]
    tile_items.append(("最大建議部位", f"{max(pos_vals):.1f}%" if pos_vals else "—", None))

    # 5 欄（非 7 欄）：375px 手機寬度實測 7 欄會把「距財報」擠出卡片右緣——
    # 名稱併入 Ticker 儲存格當小字副標（比照 weekly mail 的粗體主欄＋灰色副標
    # 樣式），訊號收盤／停損距離併成一格兩行，換取「距財報」留在可視範圍內。
    headers = ["Ticker", "型態", "收盤／停損", "建議部位", "距財報"]
    rows = []
    for e in signals:
        ec = e.get("earnings_check") or {}
        days = ec.get("days_to_earnings")
        if days is None:
            earn_cell = "—"
        elif ec.get("ok", True):
            earn_cell = f"{days} 天"
        else:
            earn_cell = f"{days} 天 " + pill("財報前觀察期", "gray")
        ticker_cell = (f"<strong>{esc(e.get('ticker'))}</strong>"
                      f'<br><span style="color:#6b6b6b;font-size:11px;">'
                      f'{esc(e.get("name") or "—")}</span>')
        close_stop_cell = (f"{esc(e.get('signal_close'))}"
                           f'<br><span style="color:#6b6b6b;font-size:11px;">'
                           f'停損 {esc(e.get("stop_dist_pct"))}%</span>')
        rows.append([
            ticker_cell,
            pill(e.get("entry_type") or "—", "green"),
            close_stop_cell,
            f"{esc(e.get('suggested_position_pct'))}%",
            earn_cell,
        ])

    body = one_minute(bullets)
    body += tiles(tile_items)
    body += section(
        "TRIGGER SIGNALS", "今日板機訊號",
        table(headers, rows, numeric_cols={3}),
    )
    if vetoed:
        body += note(f"另有 {len(vetoed)} 個訊號被 veto，詳見頁面。")
    body += note("依 SOP 執行；否決紀律與部位公式見頁面。")

    return frame(
        title="SOP 漏斗板機",
        date=as_of,
        body_html=body,
        button_label="前往 SOP 漏斗頁 →",
        button_url=PAGE_URL,
        accent="navy",
        disclaimer="本信為機械訊號通知（描述器），非投資建議；進出場決策仍需依頁面完整規則自行判斷。",
    )


def main() -> int:
    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    signals = latest.get("today_signals") or []
    vetoed = latest.get("today_vetoed") or []

    if not signals:
        if ALERT.exists():
            ALERT.unlink()
        if ALERT_HTML.exists():
            ALERT_HTML.unlink()
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
                         f"{'' if ec.get('ok', True) else ' ⚠ 財報前觀察期內'}")
        lines.append("")
    if vetoed:
        lines.append(f"(另有 {len(vetoed)} 個訊號被 veto,詳見頁面)")
        lines.append("")
    lines.append("依 SOP 執行;否決紀律與部位公式見頁面。")
    lines.append("詳細: https://research.investmquest.com/dd-screener/sop-funnel.html")
    ALERT.write_text("\n".join(lines), encoding="utf-8")

    ALERT_HTML.write_text(build_html(latest.get("as_of"), signals, vetoed), encoding="utf-8")
    print(f"sop-funnel alert: {len(signals)} trigger(s) -> {ALERT} + {ALERT_HTML}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
