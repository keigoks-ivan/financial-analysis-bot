#!/usr/bin/env python3
"""
brain_server.py — 第二大腦本機 server（launchd 常駐，只綁 127.0.0.1）。

- GET：靜態服務 repo 根目錄（wiki、docs 原始報告——手機經 Tailscale 也走這裡）
- POST /jot：免終端機餵腦。body＝純文字（或 JSON {"text": …}）→ append 到
  vault/notes/inbox/ 週檔（與 bj 同格式）→ 背景增量入腦
- POST /sweep：觸發 q.py --inbox --quiet（收 Downloads 匯出＋BrainInbox 資料夾）

CORS 全開（file:// 開的 wiki 頁 origin 為 null，需要 * 才打得進來）；
寫入面只有 append 純文字到固定資料夾，無路徑參數，無刪改能力。

用法：python3 knowledge/brain_server.py [port]（launchd plist 見 install 記錄）
"""
import json
import subprocess
import sys
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

KDIR = Path(__file__).resolve().parent
REPO = KDIR.parent
INBOX = KDIR / "vault" / "notes" / "inbox"


def jot(text):
    now = datetime.now()
    week = now.strftime("%G-W%V")
    INBOX.mkdir(parents=True, exist_ok=True)
    f = INBOX / f"{week}.md"
    if not f.exists():
        f.write_text(
            f"---\ntype: usernote\ntitle: \"收件匣 {week}\"\n"
            f"date: {now.strftime('%Y-%m-%d')}\ntags: [inbox]\n---\n\n"
            f"# 收件匣 {week}\n\n", encoding="utf-8")
    with f.open("a", encoding="utf-8") as fh:
        fh.write(f"- **{now.strftime('%m/%d %H:%M')}** {text.strip()}\n")
    # 背景增量入腦（不阻塞回應）
    subprocess.Popen([sys.executable, str(KDIR / "brain_build.py"), "--no-wiki"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return f.name


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def _reply(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            n = min(int(self.headers.get("Content-Length") or 0), 65536)
            raw = self.rfile.read(n).decode("utf-8", errors="replace")
            if self.path == "/jot":
                text = raw
                if raw.lstrip().startswith("{"):
                    try:
                        text = json.loads(raw).get("text", "")
                    except json.JSONDecodeError:
                        pass
                if not text.strip():
                    return self._reply(400, {"ok": False, "err": "空的"})
                fname = jot(text)
                return self._reply(200, {"ok": True, "file": fname})
            if self.path == "/sweep":
                r = subprocess.run(
                    [sys.executable, str(KDIR / "q.py"), "--inbox", "--quiet"],
                    capture_output=True, text=True, timeout=300)
                return self._reply(200, {"ok": r.returncode == 0})
            return self._reply(404, {"ok": False, "err": "unknown endpoint"})
        except Exception as e:
            return self._reply(500, {"ok": False, "err": str(e)[:200]})

    def log_message(self, *a):
        pass  # launchd 常駐，不刷 log


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8873
    handler = partial(Handler, directory=str(REPO))
    ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    main()
