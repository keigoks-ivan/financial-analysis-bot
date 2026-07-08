#!/usr/bin/env python3
"""
fetch_corpus.py — 抓蒙格腦公開語料 → knowledge/munger/corpus/*.md（gitignored）。

sources.json 每個 source 依序試 urls[]，第一個成功即存檔（html 剝 tag／pdf 走
pdftotext）。drop/ 內用戶自有 PDF 一併轉 corpus/。跨機：pull 後跑一次本檔即可。

用法：python3 knowledge/munger/fetch_corpus.py
"""
import json
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"
DROP = HERE / "drop"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) personal-archive/1.0"}


def strip_html(html):
    html = re.sub(r"<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ",
                  html, flags=re.DOTALL | re.IGNORECASE)
    # 常見主文容器優先
    m = re.search(r"<(article|main)[^>]*>(.*?)</\1>", html, re.DOTALL | re.IGNORECASE)
    if m:
        html = m.group(2)
    text = re.sub(r"<br\s*/?>|</p>|</div>|</h\d>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("&amp;", "&").replace("&quot;", '"').replace("&#8217;", "'") \
               .replace("&#8220;", '"').replace("&#8221;", '"').replace("&nbsp;", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch(url, timeout=30):
    with urlopen(Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def pdf_to_text(data, tmp):
    tmp.write_bytes(data)
    r = subprocess.run(["pdftotext", "-layout", str(tmp), "-"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def save(sid, title, url, text):
    if len(text) < 3000:
        return False
    out = CORPUS / f"{sid}.md"
    out.write_text(
        f"---\ntitle: \"{title}\"\nsource_url: {url}\n"
        f"fetched: {date.today().isoformat()}\ntags: [munger-corpus]\n---\n\n"
        f"# {title}\n\n{text}\n", encoding="utf-8")
    print(f"  ✅ {sid}.md  {len(text)//1024}KB  ← {url}")
    return True


def main():
    CORPUS.mkdir(exist_ok=True)
    DROP.mkdir(exist_ok=True)
    cfg = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))
    for src in cfg["sources"]:
        sid, urls = src["id"], src.get("urls") or []
        if not urls:
            continue
        if (CORPUS / f"{sid}.md").exists():
            print(f"  ↩ {sid} 已存在，跳過（要重抓先刪檔）")
            continue
        ok = False
        for url in urls:
            try:
                data = fetch(url)
                if url.lower().endswith(".pdf") or data[:5] == b"%PDF-":
                    text = pdf_to_text(data, HERE / ".tmp.pdf")
                    (HERE / ".tmp.pdf").unlink(missing_ok=True)
                else:
                    text = strip_html(data.decode("utf-8", errors="replace"))
                if save(sid, src["title"], url, text):
                    ok = True
                    break
            except Exception as e:
                print(f"  ✗ {url} → {type(e).__name__}: {e}")
        if not ok:
            print(f"  ⚠ {sid} 全部來源失敗")

    # drop/：用戶自有 PDF → corpus/private_{name}.md
    for pdf in sorted(DROP.glob("*.pdf")):
        sid = "private_" + re.sub(r"[^A-Za-z0-9_-]+", "_", pdf.stem)
        out = CORPUS / f"{sid}.md"
        if out.exists():
            continue
        text = pdf_to_text(pdf.read_bytes(), HERE / ".tmp.pdf")
        (HERE / ".tmp.pdf").unlink(missing_ok=True)
        if len(text) > 1000:
            out.write_text(
                f"---\ntitle: \"{pdf.stem}\"\nsource_url: drop/{pdf.name}\n"
                f"fetched: {date.today().isoformat()}\ntags: [munger-corpus, private]\n---\n\n"
                f"# {pdf.stem}\n\n{text}\n", encoding="utf-8")
            print(f"  ✅ {sid}.md（drop PDF）")
    print("done — 跑 python3 knowledge/brain_build.py 入腦")


if __name__ == "__main__":
    main()
