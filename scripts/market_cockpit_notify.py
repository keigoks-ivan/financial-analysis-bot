#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""market_cockpit_notify.py — 市況主控台每日摘要（email＋Discord）。

2026-11-23 持有人拍板：市場偵探的「每日摘要」改成首頁市況主控台卡片的內容
（state.json 的 home_card：結論、依主張分組的證據、資產動能四格、儀表的現在與
接下來一個月）。偵探的即時警報與週六週報不動。

由 `.github/workflows/market-state-daily.yml` 在每次重算 state.json 之後呼叫，
決定這一班要不要寄：

1. 當天的判讀推上（home_card.read_as_of＝台北今天）、今天還沒寄 → 寄。
   判讀 17:15 跑、推上後主控台馬上重算，所以平常約 17:30 寄出。
2. 補寄：最近一個已過台北 18:30 的平日還沒寄 → 寄，結論沿用最近一次判讀並標日期。
   判讀沒跑、證據沒變或沒過關的日子靠這條。
3. 同一個日期最多一封；寄過的日期記在 data/market_cockpit_notify.json，
   跟 state.json 同一個 commit 推上（推不上就不寄，下一班重新判斷）。

要寄時寫出純文字與 HTML 信文，並在 --github-output 寫 send=true 與 subject；
不寄寫 send=false。零 LLM、只用標準庫；任何例外都不擋 workflow（exit 0、send=false）。

用法
----
  python scripts/market_cockpit_notify.py --text cockpit_mail.txt --html cockpit_mail.html \\
      --github-output "$GITHUB_OUTPUT"
  python scripts/market_cockpit_notify.py --now 2026-11-23T17:30 --dry-run   # 只看判斷，不寫檔
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

import market_read_summary as mrs

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE = ROOT / "docs" / "market" / "data" / "state.json"
DEFAULT_STATUS = ROOT / "docs" / "market" / "data" / "read_status.json"
DEFAULT_LEDGER = ROOT / "data" / "market_cockpit_notify.json"
PAGE_URL = "https://research.investmquest.com/market/"

TPE = timezone(timedelta(hours=8))
FALLBACK_CUTOFF = time(18, 30)   # 過了這個時間還沒有當天判讀，就用最近一次判讀補寄


def load_json(path: Path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def fallback_day(now: datetime) -> date:
    """最近一個已過 18:30 的平日（週一到週五）。"""
    d = now.date()
    if now.time() < FALLBACK_CUTOFF:
        d -= timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def decide(card, last_sent: str, now: datetime):
    """回傳 (要寄的日期或 None, 原因)。日期字串一律 YYYY-MM-DD，可直接比大小。"""
    if not card:
        return None, "state.json 沒有可用的 home_card"
    last_sent = last_sent or ""
    today = now.date().isoformat()
    if card.get("read_as_of") == today and last_sent < today:
        return today, "read"
    fb = fallback_day(now).isoformat()
    if last_sent < fb:
        return fb, "fallback"
    return None, f"{max(last_sent, fb)} 已寄過"


def stale_note(card, day: str, status) -> str:
    """結論不是當天判讀時的說明句；是當天判讀就回空字串。"""
    ra = card.get("read_as_of") or ""
    if ra == day:
        return ""
    ra_txt = mrs._md(ra) or "上一次"
    if isinstance(status, dict) and status.get("as_of") == day and status.get("status") == "failed":
        head = f"{mrs._md(day)} 的判讀沒有過關（{status.get('stage') or '?'}）"
    else:
        head = f"{mrs._md(day)} 沒有新的判讀"
    return f"{head}，結論沿用 {ra_txt} 的判讀；證據、動能、儀表都是最新數字。"


def build_mail(card, day: str, note: str):
    headline = (card.get("headline") or "").rstrip("。")
    subject = f"📊 市況主控台 · {mrs._md(day)}｜{headline}"

    lines = []
    if note:
        lines += [note, ""]
    lines += mrs.build_home_card_lines(card)
    lines += [f"連結：{PAGE_URL}", "—", "本信是市況主控台的摘要，陳述數據狀態，不構成投資建議。"]
    text = "\n".join(lines).rstrip() + "\n"

    status_html = (
        f'<div style="margin-top:8px;color:{mrs.COLOR_NAVY_SUB};font-size:12px;line-height:1.6;">{mrs.esc(note)}</div>'
        if note else ""
    )
    html_body = mrs.render_email_shell_html(day, status_html, mrs.render_home_card_html(card), title="市況主控台")
    return subject, text, html_body


def write_output(path, send: bool, subject: str = ""):
    if not path:
        return
    delim = f"EOF_{datetime.now().timestamp():.0f}"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(f"send={'true' if send else 'false'}\n")
        if send:
            fh.write(f"subject<<{delim}\n{subject}\n{delim}\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", default=str(DEFAULT_STATE))
    ap.add_argument("--status-file", default=str(DEFAULT_STATUS))
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    ap.add_argument("--text", default="cockpit_mail.txt")
    ap.add_argument("--html", default="cockpit_mail.html")
    ap.add_argument("--github-output", default=None)
    ap.add_argument("--now", default=None, help="測試用：台北時間，如 2026-11-23T17:30")
    ap.add_argument("--dry-run", action="store_true", help="只印判斷與信文，不寫任何檔")
    args = ap.parse_args()

    try:
        now = datetime.fromisoformat(args.now).replace(tzinfo=TPE) if args.now else datetime.now(TPE)
        state = load_json(Path(args.state))
        card = mrs._home_card(state)
        ledger = load_json(Path(args.ledger)) or {}
        day, reason = decide(card, ledger.get("last_sent_day"), now)
        print(f"cockpit-notify: now={now:%Y-%m-%d %H:%M} 台北, last_sent={ledger.get('last_sent_day')}, "
              f"read_as_of={(card or {}).get('read_as_of')} → {'寄 ' + day if day else '不寄'}（{reason}）")
        if not day:
            write_output(args.github_output, False)
            return

        note = stale_note(card, day, load_json(Path(args.status_file)))
        subject, text, html_body = build_mail(card, day, note)
        if args.dry_run:
            print(subject)
            print()
            print(text)
            return

        Path(args.text).write_text(text, encoding="utf-8")
        Path(args.html).write_text(html_body, encoding="utf-8")
        Path(args.ledger).parent.mkdir(parents=True, exist_ok=True)
        Path(args.ledger).write_text(json.dumps({
            "last_sent_day": day,
            "reason": reason,
            "read_as_of": card.get("read_as_of"),
            "data_as_of": card.get("data_as_of"),
            "decided_at": now.isoformat(timespec="minutes"),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_output(args.github_output, True, subject)
        print(f"cockpit-notify: subject={subject}")
    except Exception as e:  # noqa: BLE001 — 通知不能擋 state.json 的提交
        print(f"cockpit-notify: 例外，這班不寄：{e!r}", file=sys.stderr)
        write_output(args.github_output, False)


if __name__ == "__main__":
    main()
