#!/usr/bin/env python3
"""
fetch_corpus.py — 抓智慧語料公開文本 → knowledge/wisdom/corpus/{collection}/{id}.md（gitignored）。

sources.json 每個 source：{id, collection, title, urls[], tags?}。依序試 urls[]，第一個
成功即存 corpus/{collection}/{id}.md（html 剝 tag／pdf 走 pdftotext；帶 frontmatter：
title/source_url/fetched/tags）。逐檔 sleep 禮貌節流。全文受版權，故 gitignored；本檔＋
sources.json committed，另一台機 pull 後重跑即可。

跨機注意：部分站（如 Sucuri CDN 的 berkshirehathaway.com）強制 brotli 回應——需要
`pip install brotli`。缺套件時該來源會被記為失敗，補裝後重跑即可。

用法：python3 knowledge/wisdom/fetch_corpus.py
"""
import gzip
import json
import re
import subprocess
import sys
import time
import unicodedata
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

try:
    import brotli  # noqa: F401
    _HAS_BR = True
except ImportError:
    _HAS_BR = False

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "corpus"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) personal-archive/1.0"}
SLEEP = 1.5  # 逐檔節流秒數


def strip_html(html):
    html = re.sub(r"<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ",
                  html, flags=re.DOTALL | re.IGNORECASE)
    m = re.search(r"<(article|main)[^>]*>(.*?)</\1>", html, re.DOTALL | re.IGNORECASE)
    if m:
        html = m.group(2)
    text = re.sub(r"<br\s*/?>|</p>|</div>|</h\d>|</tr>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unicodedata.normalize("NFKC", text)
    text = (text.replace("&amp;", "&").replace("&quot;", '"').replace("&#8217;", "'")
                .replace("&#8220;", '"').replace("&#8221;", '"').replace("&#8212;", "—")
                .replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">"))
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch(url, timeout=40):
    with urlopen(Request(url, headers=UA), timeout=timeout) as r:
        data = r.read()
        enc = (r.headers.get("Content-Encoding") or "").lower()
    if enc == "br":
        if not _HAS_BR:
            raise RuntimeError("brotli 回應但未安裝 brotli 套件（pip install brotli）")
        import brotli
        data = brotli.decompress(data)
    elif enc == "gzip":
        data = gzip.decompress(data)
    return data


def pdf_to_text(data, tmp):
    tmp.write_bytes(data)
    r = subprocess.run(["pdftotext", "-layout", str(tmp), "-"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def save(coll, sid, title, url, text, tags):
    if len(text) < 3000:
        return False
    outdir = CORPUS / coll
    outdir.mkdir(parents=True, exist_ok=True)
    taglist = ", ".join(["wisdom-corpus", coll] + list(tags or []))
    out = outdir / f"{sid}.md"
    out.write_text(
        f"---\ntitle: \"{title}\"\nsource_url: {url}\n"
        f"fetched: {date.today().isoformat()}\ntags: [{taglist}]\n---\n\n"
        f"# {title}\n\n{text}\n", encoding="utf-8")
    print(f"  ✅ {coll}/{sid}.md  {len(text)//1024}KB  ← {url}")
    return True


def main():
    CORPUS.mkdir(exist_ok=True)
    cfg = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))
    ok_list, fail_list = [], []
    for src in cfg["sources"]:
        sid = src["id"]
        coll = src["collection"]
        urls = src.get("urls") or []
        if not urls:
            continue
        if (CORPUS / coll / f"{sid}.md").exists():
            print(f"  ↩ {coll}/{sid} 已存在，跳過（要重抓先刪檔）")
            ok_list.append(sid)
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
                if save(coll, sid, src["title"], url, text, src.get("tags")):
                    ok = True
                    break
                else:
                    print(f"  ✗ {url} → 內容過短（{len(text)}B）")
            except Exception as e:
                print(f"  ✗ {url} → {type(e).__name__}: {e}")
            time.sleep(SLEEP)
        (ok_list if ok else fail_list).append(sid)
        if not ok:
            print(f"  ⚠ {sid} 全部來源失敗（記為 gap）")
        time.sleep(SLEEP)

    print(f"\ndone — 成功 {len(ok_list)}／失敗 {len(fail_list)}")
    if fail_list:
        print("  gap:", ", ".join(fail_list))
    print("跑 python3 knowledge/brain_build.py --full 入腦")


if __name__ == "__main__":
    main()
