#!/usr/bin/env python3
"""
retrofit_dd_id_banner.py — 給所有 v11+ DD HTML 加「所屬產業」banner

在 <h1> 下方插入 ID reference block，列出該 ticker 所屬的所有 ID。
若沒有對應 ID，不插入（保持原樣）。
重跑 idempotent — 會先移除既有 banner 再重新插入。

依賴：portfolio/id_dd_map.json（由 id_dd_mapping.py 產出）
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MAP_FILE = REPO / "portfolio" / "id_dd_map.json"
DD_DIR = REPO / "docs" / "dd"

BANNER_START = "<!-- ID_BANNER_START -->"
BANNER_END = "<!-- ID_BANNER_END -->"


def build_banner(ticker: str, id_files: list[str], id_meta: dict) -> str:
    links = []
    for fn in sorted(id_files):
        topic = id_meta.get(fn, {}).get("topic", fn)
        # 去掉括號英文版本以免太長
        short = re.sub(r"（.*?）|\(.*?\)", "", topic).strip()
        links.append(f'<a href="/id/{fn}">{short}</a>')
    joined = " · ".join(links)
    return (
        f"{BANNER_START}\n"
        f'<div style="background:#F0F9FF;border-left:3px solid #3B82F6;padding:10px 16px;margin:14px 0 18px;font-size:13px;color:#1E3A5F;border-radius:3px">'
        f'<strong style="color:#1E40AF">📐 所屬產業 ID：</strong>{joined}'
        f' <span style="color:#64748b;font-size:11px;margin-left:8px">· DD 結論請對照 ID 核心假設</span>'
        f"</div>\n"
        f"{BANNER_END}"
    )


def normalize_ticker(raw: str) -> str:
    if re.fullmatch(r"\d{4,5}", raw):
        return raw + ".TW"
    return raw


def ticker_from_filename(fn: str) -> str | None:
    """DD_NVDA_20260416.html → NVDA"""
    m = re.match(r"DD_(.+?)_(\d{8})(?:_.*)?\.html$", fn)
    if not m:
        return None
    return normalize_ticker(m.group(1))


def retrofit(html: str, banner: str) -> str:
    # 先移除既有 banner（為 idempotent）
    html = re.sub(
        rf"{re.escape(BANNER_START)}.*?{re.escape(BANNER_END)}\n?",
        "",
        html,
        flags=re.DOTALL,
    )
    # 在 <h1> 那一行之後插入 banner
    new_html, n = re.subn(
        r"(<h1[^>]*>.*?</h1>)",
        r"\1\n" + banner,
        html,
        count=1,
    )
    if n == 0:
        # 沒找到 h1，插到 body 後
        new_html, n = re.subn(r"(<body[^>]*>)", r"\1\n" + banner, html, count=1)
    return new_html


def main():
    mapping = json.loads(MAP_FILE.read_text())
    ticker_to_ids = mapping["ticker_to_ids"]
    id_meta = mapping["id_meta"]

    # 收集每個 ticker 的 DD 檔案清單
    dd_files = sorted(DD_DIR.glob("DD_*.html"))

    patched = 0
    skipped_no_match = 0
    skipped_parse = 0

    for fp in dd_files:
        t = ticker_from_filename(fp.name)
        if t is None:
            skipped_parse += 1
            continue
        ids = ticker_to_ids.get(t)
        if not ids:
            # 沒對應 ID → 移除既有 banner（若有）使檔案乾淨
            html = fp.read_text()
            new = re.sub(
                rf"{re.escape(BANNER_START)}.*?{re.escape(BANNER_END)}\n?",
                "",
                html,
                flags=re.DOTALL,
            )
            if new != html:
                fp.write_text(new)
            skipped_no_match += 1
            continue
        banner = build_banner(t, ids, id_meta)
        html = fp.read_text()
        new_html = retrofit(html, banner)
        if new_html != html:
            fp.write_text(new_html)
            patched += 1

    print(f"Patched (added/updated banner): {patched}")
    print(f"No matching ID, skipped: {skipped_no_match}")
    print(f"Filename parse failed: {skipped_parse}")


if __name__ == "__main__":
    main()
