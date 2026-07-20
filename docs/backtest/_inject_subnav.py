#!/usr/bin/env python3
"""Surgically refresh the /backtest/ pill-bar in every page.

The pill-bar is baked into each page's HTML by that page's own generator, most
of which live in the sibling v7-backtest repo and re-run with drifting numbers.
So when _nav_common.py changes, we cannot simply re-run the generators — we
replace only the pill-bar block and touch nothing else.

The block is delimited by `<style id="bt-subnav-style">` … the first `</nav>`
after it. Each page's active key is recovered from its existing markup (the
`class="bt-on"` link), so the highlight is preserved exactly rather than guessed.

Idempotent: running twice is a no-op. Reports pages whose active key no longer
resolves (e.g. the key was retired from _nav_common) instead of silently
dropping their highlight.

Usage:
    python3 _inject_subnav.py --check   # report only, write nothing
    python3 _inject_subnav.py           # apply
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _nav_common as NC  # noqa: E402

START = '<style id="bt-subnav-style">'
GROUPS = ["COMPARISON", "INDIVIDUAL", "MULTI", "TAIWAN", "OPTIONS", "INTRADAY",
          "RESEARCH_ETF", "RESEARCH_FREQ", "RESEARCH_MA", "RESEARCH_CRASH"]


def valid_keys() -> set[str]:
    out = set()
    for g in GROUPS:
        for _u, _n, k, _s in getattr(NC, f"{g}_LINKS"):
            out.add(k)
    return out


def url_to_key() -> dict[str, str]:
    out = {}
    for g in GROUPS:
        for u, _n, k, _s in getattr(NC, f"{g}_LINKS"):
            out[u] = k
    return out


def main() -> int:
    check = "--check" in sys.argv
    root = Path(__file__).parent
    u2k, keys = url_to_key(), valid_keys()
    pages = sorted(p for p in root.glob("*/*.html"))
    if (root / "index.html").exists():
        pages.append(root / "index.html")

    changed = same = skipped = 0
    problems: list[str] = []
    for p in pages:
        html = p.read_text(encoding="utf-8")
        i = html.find(START)
        if i < 0:
            skipped += 1
            continue
        j = html.find("</nav>", i)
        if j < 0:
            problems.append(f"{p}: 找到 style 但無 </nav>")
            continue
        j += len("</nav>")
        m = re.search(r'<a href="([^"]+)" class="bt-on"', html[i:j])
        if not m:
            problems.append(f"{p}: 無 bt-on，無法反解 active key")
            continue
        key = u2k.get(m.group(1))
        if key is None or key not in keys:
            problems.append(f"{p}: active 指向 {m.group(1)}，該連結已不在 _nav_common")
            continue
        fresh = NC.make_toggle(key)
        if html[i:j] == fresh:
            same += 1
            continue
        changed += 1
        if not check:
            p.write_text(html[:i] + fresh + html[j:], encoding="utf-8")

    verb = "需更新" if check else "已更新"
    print(f"掃描 {len(pages)} 檔：{verb} {changed}、已是最新 {same}、無 pill-bar {skipped}")
    if problems:
        print(f"\n⚠ 需人工處理 {len(problems)} 項：")
        for x in problems:
            print(f"  {x}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
