#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""idea_watch_summary.py — 把 `docs/ideas/data/research.json`
收斂成一封「要不要寄」的 email 摘要（HTML 版型＋純文字備援），
供 `.github/workflows/idea-watch-notify.yml` 消費。

寄信規則（僅兩種情況寄信，其餘一律不寄）：
  1. `run.status == "failed"` → 主旨「想法查核失敗 <date>」，內文帶失敗原因。
  2. 當天（`date == run.date`）的 `changes` 裡，有 `keystone: true` 且
     `to == "refutes"` 的查核點變化 → 主旨「關鍵查核點轉為推翻：<idea short>・
     <checkpoint label>」，內文逐筆列出每個這類變化（from→to、理由、複審、
     連到 https://research.investmquest.com<idea url>#<cp> 的連結），
     後面附一小段「當天其他狀態變化」。
  其他情況（沒有 run，或 run.status=="pending"／"ok" 但當天沒有關鍵查核點
  轉推翻）一律不寄。

stdout 合約（`.github/workflows/idea-watch-notify.yml` 依此解析）：
  第 1 行：`true` 或 `false`（要不要寄信）
  第 2 行：主旨（不寄信時為空行）
  第 3 行：空白
  之後：純文字信文（與 `--text` 檔案內容相同）
exit code 恆為 0（本腳本本身絕不能讓 workflow 因未預期例外卡住）。

用法
----
  python3 scripts/idea_watch_summary.py
  python3 scripts/idea_watch_summary.py --file docs/ideas/data/research.json \\
      --ideas docs/ideas/ideas.json --html /tmp/idea_watch_mail.html \\
      --text /tmp/idea_watch_mail.txt
  python3 scripts/idea_watch_summary.py --dry-run   # 內建情境自我檢查，不讀真檔
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = ROOT / "docs" / "ideas" / "data" / "research.json"
DEFAULT_IDEAS = ROOT / "docs" / "ideas" / "ideas.json"
SITE = "https://research.investmquest.com"
IDEAS_URL = SITE + "/ideas/"

STATUS_ZH = {"supports": "支持", "shaky": "動搖", "refutes": "推翻", "no_data": "尚無資料"}

FONT_STACK = "-apple-system, 'PingFang TC', 'Noto Sans TC', 'Segoe UI', sans-serif"
COLOR_BG = "#f6f5f2"
COLOR_CARD = "#ffffff"
COLOR_BORDER = "#e6e2d8"
COLOR_NAVY = "#0f1f3d"
COLOR_NAVY_SUB = "#c9d2e3"
COLOR_DARK = "#1c1c1c"
COLOR_GRAY = "#6b6b6b"
COLOR_RED = "#b3261e"
COLOR_RED_BG = "#fbe9e7"


def esc(x) -> str:
    if x is None:
        return ""
    return html.escape(str(x), quote=True)


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def status_zh(s: str) -> str:
    return STATUS_ZH.get(s, s or "—")


def idea_meta(ideas_data) -> dict:
    """id -> {'short', 'title', 'url', 'checkpoints': {cpid: label}}"""
    out = {}
    if not isinstance(ideas_data, dict):
        return out
    for idea in ideas_data.get("ideas") or []:
        if not isinstance(idea, dict):
            continue
        cps = {}
        for cp in idea.get("checkpoints") or []:
            if isinstance(cp, dict):
                cps[cp.get("id")] = cp.get("label", cp.get("id", ""))
        idea_id = idea.get("id", "")
        out[idea_id] = {
            "short": idea.get("short") or idea.get("title") or idea_id,
            "title": idea.get("title") or idea_id,
            "url": idea.get("url") or f"/ideas/{idea_id}.html",
            "checkpoints": cps,
        }
    return out


def cp_label(meta: dict, idea_id: str, cp_id: str) -> str:
    return (meta.get(idea_id) or {}).get("checkpoints", {}).get(cp_id, cp_id)


def idea_short(meta: dict, idea_id: str) -> str:
    return (meta.get(idea_id) or {}).get("short", idea_id)


def cp_link(meta: dict, idea_id: str, cp_id: str) -> str:
    url = (meta.get(idea_id) or {}).get("url", f"/ideas/{idea_id}.html")
    return f"{SITE}{url}#{cp_id}"


def change_line(meta: dict, c: dict) -> str:
    idea_id = c.get("idea", "")
    cpid = c.get("checkpoint", "")
    return (
        f"{idea_short(meta, idea_id)}・{cp_label(meta, idea_id, cpid)}："
        f"{status_zh(c.get('from', ''))} → {status_zh(c.get('to', ''))}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# 純文字信文
# ═══════════════════════════════════════════════════════════════════════════

def build_failure_text(run: dict):
    date = run.get("date") or "（日期未知）"
    reason = run.get("reason") or "（未提供原因）"
    subject = f"想法查核失敗 {date}"
    lines = [
        f"想法查核在 {date} 失敗，查核點狀態沒有更新。",
        "",
        f"原因：{reason}",
        "",
        f"連結：{IDEAS_URL}",
    ]
    return subject, "\n".join(lines)


def build_keystone_text(meta: dict, date: str, keystone_refutes: list, other_changes: list):
    first = keystone_refutes[0]
    subject = (
        f"關鍵查核點轉為推翻："
        f"{idea_short(meta, first.get('idea',''))}・{cp_label(meta, first.get('idea',''), first.get('checkpoint',''))}"
    )
    lines = [f"{date} 有關鍵查核點轉為推翻：", ""]
    for c in keystone_refutes:
        lines.append(f"★ {change_line(meta, c)}")
        lines.append(f"　理由：{c.get('reason') or '（無）'}")
        if c.get("review"):
            lines.append(f"　複審：{c['review']}")
        lines.append(f"　{cp_link(meta, c.get('idea',''), c.get('checkpoint',''))}")
        lines.append("")
    if other_changes:
        lines.append("當天其他狀態變化：")
        for c in other_changes:
            lines.append(f"－{change_line(meta, c)}")
        lines.append("")
    lines.append(f"連結：{IDEAS_URL}")
    return subject, "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# HTML 版型（沿用 market_read_summary.py 的版型標準：600px 卡片、頂欄深藍）
# ═══════════════════════════════════════════════════════════════════════════

def render_email_shell_html(title: str, status_html: str, body_html: str) -> str:
    return f'''<meta charset="utf-8">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="width:100%;table-layout:fixed;background-color:{COLOR_BG};" bgcolor="{COLOR_BG}">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;table-layout:fixed;background-color:{COLOR_CARD};border:1px solid {COLOR_BORDER};border-radius:8px;font-family:{FONT_STACK};" bgcolor="{COLOR_CARD}">
<tr><td style="background-color:{COLOR_NAVY};padding:20px 24px;border-radius:8px 8px 0 0;" bgcolor="{COLOR_NAVY}">
<div style="color:#ffffff;font-size:18px;font-weight:700;font-family:{FONT_STACK};">{esc(title)}</div>
{status_html}
</td></tr>
<tr><td style="padding:20px 24px 4px 24px;font-family:{FONT_STACK};">
{body_html}
</td></tr>
<tr><td style="padding:12px 24px 24px 24px;text-align:center;">
<a href="{IDEAS_URL}" style="background-color:{COLOR_NAVY};color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 32px;border-radius:6px;display:inline-block;font-family:{FONT_STACK};">打開投資想法</a>
</td></tr>
<tr><td style="padding:0 24px 24px 24px;">
<div style="font-size:11px;color:{COLOR_GRAY};line-height:1.6;border-top:1px solid {COLOR_BORDER};padding-top:12px;font-family:{FONT_STACK};">
本信為想法查核點的機械通知，只描述狀態變化與理由，不下買賣指令；完整查核紀錄請見網站原文。
</div>
</td></tr>
</table>
</td></tr>
</table>'''


def build_failure_html(run: dict) -> str:
    date = run.get("date") or "（日期未知）"
    reason = run.get("reason") or "（未提供原因）"
    status_html = (
        f'<div style="margin-top:10px;"><span style="display:inline-block;background-color:{COLOR_RED_BG};'
        f'color:{COLOR_RED};font-size:12px;font-weight:700;padding:2px 10px;border-radius:999px;">查核失敗</span>'
        f'<span style="color:{COLOR_NAVY_SUB};font-size:12px;margin-left:8px;">{esc(date)}</span></div>'
    )
    body_html = (
        f'<div style="font-size:15px;line-height:1.65;color:{COLOR_DARK};margin-bottom:8px;">'
        f'想法查核在 {esc(date)} 失敗，查核點狀態沒有更新。</div>'
        f'<div style="font-size:13px;color:{COLOR_DARK};margin-top:8px;"><b>原因：</b>{esc(reason)}</div>'
    )
    return render_email_shell_html(f"想法查核失敗｜{date}", status_html, body_html)


def build_keystone_html(meta: dict, date: str, keystone_refutes: list, other_changes: list) -> str:
    status_html = (
        f'<div style="margin-top:10px;"><span style="display:inline-block;background-color:{COLOR_RED_BG};'
        f'color:{COLOR_RED};font-size:12px;font-weight:700;padding:2px 10px;border-radius:999px;">關鍵查核點推翻</span>'
        f'<span style="color:{COLOR_NAVY_SUB};font-size:12px;margin-left:8px;">{esc(date)}</span></div>'
    )
    rows = []
    for c in keystone_refutes:
        idea_id, cpid = c.get("idea", ""), c.get("checkpoint", "")
        rows.append(
            f'<div style="border:1px solid {COLOR_RED_BG};background-color:#fff8f7;border-radius:8px;'
            f'padding:12px 14px;margin-bottom:10px;">'
            f'<div style="font-size:14px;font-weight:700;color:{COLOR_RED};">★ {esc(change_line(meta, c))}</div>'
            f'<div style="font-size:13px;color:{COLOR_DARK};margin-top:6px;">理由：{esc(c.get("reason") or "（無）")}</div>'
            + (f'<div style="font-size:12px;color:{COLOR_GRAY};margin-top:4px;">複審：{esc(c["review"])}</div>' if c.get("review") else "")
            + f'<div style="font-size:12px;margin-top:6px;"><a href="{esc(cp_link(meta, idea_id, cpid))}" style="color:{COLOR_NAVY};">看這個查核點 →</a></div>'
            f'</div>'
        )
    other_html = ""
    if other_changes:
        items = "".join(
            f'<div style="font-size:12px;color:{COLOR_DARK};margin-bottom:4px;">－{esc(change_line(meta, c))}</div>'
            for c in other_changes
        )
        other_html = (
            f'<div style="margin-top:16px;font-size:12px;letter-spacing:.05em;color:{COLOR_GRAY};'
            f'font-weight:700;text-transform:uppercase;">當天其他狀態變化</div><div style="margin-top:6px;">{items}</div>'
        )
    body_html = "".join(rows) + other_html
    return render_email_shell_html(f"關鍵查核點轉為推翻｜{date}", status_html, body_html)


# ═══════════════════════════════════════════════════════════════════════════
# 決策層：從 research.json 判斷要不要寄信
# ═══════════════════════════════════════════════════════════════════════════

def decide(research, ideas_data):
    """回傳 (send: bool, subject: str, text: str, html_body: str)"""
    meta = idea_meta(ideas_data)
    run = (research or {}).get("run") or {}
    status = run.get("status")

    if status == "failed":
        subject, text = build_failure_text(run)
        return True, subject, text, build_failure_html(run)

    date = run.get("date") or ""
    changes = (research or {}).get("changes") or []
    today_changes = [c for c in changes if date and c.get("date") == date]
    keystone_refutes = [c for c in today_changes if c.get("keystone") and c.get("to") == "refutes"]

    if not keystone_refutes:
        return False, "", "", ""

    other_changes = [c for c in today_changes if c not in keystone_refutes]
    subject, text = build_keystone_text(meta, date, keystone_refutes, other_changes)
    html_body = build_keystone_html(meta, date, keystone_refutes, other_changes)
    return True, subject, text, html_body


# ═══════════════════════════════════════════════════════════════════════════
# --dry-run 自我檢查（不讀真檔，內建四種情境；stdlib assert，無需 pytest）
# ═══════════════════════════════════════════════════════════════════════════

def _fixture_ideas():
    return {
        "ideas": [
            {
                "id": "ai-scissors", "short": "AI 剪刀差", "url": "/ideas/ai-scissors.html",
                "checkpoints": [
                    {"id": "cp1", "label": "AI 營收成長跑贏降價"},
                    {"id": "cp2", "label": "GPU 雲同代旗艦租金與長約價格守住"},
                    {"id": "cp3", "label": "記憶體季度合約價續漲"},
                ],
            }
        ]
    }


def _run_dry_run_cases():
    cases = []

    # 1) pending：不寄
    cases.append((
        "pending 不寄",
        {"run": {"date": "", "status": "pending", "reason": ""}, "status": {}, "entries": [], "changes": []},
        False, None,
    ))

    # 2) ok 但當天沒有 keystone refutes：不寄
    cases.append((
        "ok 無關鍵推翻不寄",
        {
            "run": {"date": "2026-09-24", "status": "ok"},
            "changes": [
                {"date": "2026-09-24", "idea": "ai-scissors", "checkpoint": "cp3", "keystone": False,
                 "from": "no_data", "to": "supports", "reason": "x"},
            ],
        },
        False, None,
    ))

    # 3) ok 且有 keystone refutes：寄，主旨含 idea short + checkpoint label
    cases.append((
        "keystone refutes 寄信",
        {
            "run": {"date": "2026-09-24", "status": "ok"},
            "changes": [
                {"date": "2026-09-24", "idea": "ai-scissors", "checkpoint": "cp2", "keystone": True,
                 "from": "supports", "to": "refutes", "reason": "CoreWeave 新約降價 6%", "review": "sonnet 同意"},
                {"date": "2026-09-24", "idea": "ai-scissors", "checkpoint": "cp1", "keystone": True,
                 "from": "supports", "to": "shaky", "reason": "y"},
            ],
        },
        True, "關鍵查核點轉為推翻：AI 剪刀差・GPU 雲同代旗艦租金與長約價格守住",
    ))

    # 4) 昨天的 keystone refutes 不算今天：不寄
    cases.append((
        "非當天變化不寄",
        {
            "run": {"date": "2026-09-24", "status": "ok"},
            "changes": [
                {"date": "2026-09-23", "idea": "ai-scissors", "checkpoint": "cp2", "keystone": True,
                 "from": "supports", "to": "refutes", "reason": "z"},
            ],
        },
        False, None,
    ))

    # 5) failed：寄，主旨帶日期
    cases.append((
        "failed 寄信",
        {"run": {"date": "2026-09-24", "status": "failed", "reason": "GE Vernova IR 逾時"}},
        True, "想法查核失敗 2026-09-24",
    ))

    # 6) 非 keystone 的 refutes：不寄
    cases.append((
        "非關鍵查核點推翻不寄",
        {
            "run": {"date": "2026-09-24", "status": "ok"},
            "changes": [
                {"date": "2026-09-24", "idea": "ai-scissors", "checkpoint": "cp3", "keystone": False,
                 "from": "supports", "to": "refutes", "reason": "w"},
            ],
        },
        False, None,
    ))

    return cases


def dry_run() -> int:
    ideas_data = _fixture_ideas()
    failed = 0
    for name, research, expect_send, expect_subject in _run_dry_run_cases():
        send, subject, text, html_body = decide(research, ideas_data)
        ok = (send == expect_send) and (expect_subject is None or subject == expect_subject)
        if send:
            ok = ok and bool(text) and bool(html_body)
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        print(f"[{status}] {name}  send={send} subject={subject!r}")
    print(f"\n{len(_run_dry_run_cases()) - failed}/{len(_run_dry_run_cases())} passed")
    return 1 if failed else 0


# ═══════════════════════════════════════════════════════════════════════════
# main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=str(DEFAULT_FILE), help="research.json 路徑（預設 %(default)s）")
    ap.add_argument("--ideas", default=str(DEFAULT_IDEAS), help="ideas.json 路徑（預設 %(default)s）")
    ap.add_argument("--html", default=None, help="額外寫出美化版 HTML 信到此路徑")
    ap.add_argument("--text", default=None, help="額外寫出純文字備援信文到此路徑（與 stdout 信文段相同）")
    ap.add_argument("--dry-run", action="store_true", help="內建情境自我檢查，不讀真檔、不寫檔，exit code 反映是否全過")
    args = ap.parse_args()

    if args.dry_run:
        sys.exit(dry_run())

    send, subject, text, html_body = False, "", "", ""
    try:
        research = load_json(Path(args.file))
        ideas_data = load_json(Path(args.ideas))
        send, subject, text, html_body = decide(research, ideas_data)
    except Exception as e:  # noqa: BLE001 — 摘要腳本絕不能讓 workflow 因未預期例外而卡住
        send = True
        subject = "想法查核摘要腳本發生未預期錯誤"
        text = f"idea_watch_summary.py 拋出例外：{e!r}\n\n連結：{IDEAS_URL}"
        html_body = render_email_shell_html(
            subject, "",
            f'<div style="font-size:13px;color:{COLOR_DARK};">{esc(repr(e))}</div>',
        )

    if args.html:
        try:
            Path(args.html).write_text(html_body or "", encoding="utf-8")
        except OSError:
            pass
    if args.text:
        try:
            Path(args.text).write_text(text or "", encoding="utf-8")
        except OSError:
            pass

    print("true" if send else "false")
    print(subject)
    print()
    print(text)
    sys.exit(0)


if __name__ == "__main__":
    main()
