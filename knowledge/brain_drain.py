#!/usr/bin/env python3
"""
brain_drain.py — 收取公開頁餵腦框（/jot.html → cPanel 接收器）的筆記。

讀 ~/.brain_relay.json（{url, pass}，600 權限、不進 git）→ GET {url}/drain.php
→ 每則寫成 ~/BrainInbox/relay-*.txt → 既有 WatchPaths 管線自動入腦。
無料、無設定檔、斷網皆靜默 exit 0（launchd 每 5 分鐘跑，com.ivanchang.brain-drain）。
"""
import json
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

CFG = Path.home() / ".brain_relay.json"


def main():
    if not CFG.exists():
        return
    try:
        cfg = json.loads(CFG.read_text(encoding="utf-8"))
        url = cfg["url"].rstrip("/") + "/drain.php?pass=" + quote(cfg["pass"])
        with urlopen(url, timeout=20) as r:
            items = json.loads(r.read().decode("utf-8"))
    except Exception:
        return
    if not items:
        return
    inbox = Path.home() / "BrainInbox"
    inbox.mkdir(exist_ok=True)
    for i, it in enumerate(items):
        text = (it.get("text") or "").strip()
        if not text:
            continue
        ts = "".join(ch for ch in (it.get("ts") or "")[:19] if ch.isdigit()) \
            or str(int(time.time()))
        (inbox / f"relay-{ts}-{i}.txt").write_text(text, encoding="utf-8")
    print(f"收到 {len(items)} 則")


if __name__ == "__main__":
    main()
