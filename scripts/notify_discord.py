#!/usr/bin/env python3
"""Post one Discord embed mirroring an email alert.

Webhook URL comes only from env DISCORD_WEBHOOK (never printed). Always exits 0.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

COLOR = 0x2B6CB0
MAX_DESC = 3500
TRUNC_LINE = "…（完整內容請看連結）"


def clean_body(text):
    text = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.S | re.I)
    text = re.sub(r"<br\s*/?>|</p>|</div>|</tr>|</li>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate_lines(text, limit):
    if len(text) <= limit:
        return text
    budget = limit - len(TRUNC_LINE) - 1
    kept, used = [], 0
    for line in text.split("\n"):
        if used + len(line) + 1 > budget:
            break
        kept.append(line)
        used += len(line) + 1
    if not kept:  # first line alone too long: hard cut
        kept = [text[:budget]]
    return "\n".join(kept).rstrip() + "\n" + TRUNC_LINE


def build_payload(title, body, url):
    tail = []
    if url:
        tail.append(f"[打開完整頁面]({url})")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    server = os.environ.get("GITHUB_SERVER_URL", "")
    if repo and run_id and server:
        tail.append(f"[這次執行]({server}/{repo}/actions/runs/{run_id})")
    tail_text = "\n".join(tail)
    room = MAX_DESC - (len(tail_text) + 2 if tail_text else 0)
    desc = truncate_lines(clean_body(body), room) if body else ""
    desc = (desc + "\n\n" + tail_text).strip() if tail_text else desc
    embed = {"title": (title or "(no title)")[:256], "color": COLOR}
    if url:
        embed["url"] = url
    if desc:
        embed["description"] = desc
    footer = " · ".join(
        x for x in (repo, os.environ.get("GITHUB_WORKFLOW", "")) if x
    )
    if footer:
        embed["footer"] = {"text": footer}
    return {"embeds": [embed], "allowed_mentions": {"parse": []}}


def post(webhook, payload):
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "investmquest-notify/1.0",
    }
    for attempt in (1, 2):
        req = urllib.request.Request(webhook, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                print(f"discord: HTTP {r.status}")
                return
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                try:
                    wait = float(json.loads(e.read().decode()).get("retry_after", 1))
                except Exception:
                    wait = 1.0
                time.sleep(min(max(wait, 0), 30))
                continue
            print(f"discord: HTTP {e.code}")
            return
        except Exception as e:
            print(f"discord: {type(e).__name__}")
            return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title-env", required=True)
    ap.add_argument("--body-env")
    ap.add_argument("--body-file")
    ap.add_argument("--url")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    webhook = os.environ.get("DISCORD_WEBHOOK", "").strip()
    if not webhook and not a.dry_run:
        print("DISCORD_WEBHOOK not set, skip")
        return 0

    title = os.environ.get(a.title_env, "").strip()
    body = ""
    if a.body_env:
        body = os.environ.get(a.body_env, "")
    if not body.strip() and a.body_file:
        try:
            with open(a.body_file, encoding="utf-8", errors="replace") as f:
                body = f.read()
        except OSError:
            body = ""
    try:
        payload = build_payload(title, body, a.url)
        if a.dry_run:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        post(webhook, payload)
    except Exception as e:
        print(f"discord: {type(e).__name__}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
