#!/usr/bin/env python3
"""dd2 卡片管理：檢查 scripts/dd2/cards/*.md 的來源檔是否已變。

卡是人工濃縮的 prompt 片段（判斷卡、附卡、閘卡、呈現卡），不是程式產物。
每張卡第一行是來源戳：
    <!-- source: <path> sha256:<16碼>[; <path> sha256:<16碼>] git:<hash> condensed:<date> model:<m> -->
本腳本重算各來源的 sha256 前 16 碼，跟戳比對。變了就印 STALE，exit 1。

用法：
    python3 scripts/dd2/cards.py check            # 全部卡
    python3 scripts/dd2/cards.py check judge_card # 單張
    python3 scripts/dd2/cards.py sizes            # 印各卡 byte 數與上限
"""
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CARDS_DIR = Path(__file__).resolve().parent / "cards"

# 設計稿 §4 的硬上限（bytes）
SIZE_LIMITS = {
    "judge_card.md": 16_000,
    "judge_addendum_roic.md": 4_000,
    "judge_addendum_playbook.md": 4_000,
    "judge_addendum_cyclical.md": 4_000,
    "judge_addendum_archetype.md": 4_000,
    "gate_card.md": 8_000,
    "prose_card.md": 10_000,
}

_HEAD_RE = re.compile(r"<!--\s*source:\s*(?P<body>.+?)\s*-->")
_PAIR_RE = re.compile(r"(?P<path>\S+)\s+sha256:(?P<sha>[0-9a-f]{8,64})")


def _sha16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _parse_header(card: Path):
    first = card.read_text(encoding="utf-8").splitlines()[0] if card.stat().st_size else ""
    m = _HEAD_RE.search(first)
    if not m:
        return None
    body = m.group("body")
    # 去掉 git:/condensed:/model: 尾巴，只留 path sha 配對
    body = re.split(r"\s+git:", body)[0]
    return [(p.group("path"), p.group("sha")) for p in _PAIR_RE.finditer(body)]


def cmd_check(names):
    cards = sorted(CARDS_DIR.glob("*.md")) if not names else [CARDS_DIR / (n if n.endswith(".md") else n + ".md") for n in names]
    bad = 0
    for card in cards:
        if card.name.startswith("_"):
            continue
        if not card.exists():
            print(f"MISSING  {card.name}")
            bad += 1
            continue
        pairs = _parse_header(card)
        if not pairs:
            print(f"NOHEADER {card.name}")
            bad += 1
            continue
        for rel, sha in pairs:
            src = REPO / rel
            if not src.exists():
                print(f"NOSRC    {card.name} <- {rel}")
                bad += 1
                continue
            now = _sha16(src)
            if now.startswith(sha) or sha.startswith(now):
                print(f"OK       {card.name} <- {rel}")
            else:
                print(f"STALE    {card.name} <- {rel} (card {sha}, now {now})")
                bad += 1
        limit = SIZE_LIMITS.get(card.name)
        size = card.stat().st_size
        if limit and size > limit:
            print(f"OVERSIZE {card.name} {size:,} > {limit:,}")
            bad += 1
    return 1 if bad else 0


def cmd_sizes():
    for card in sorted(CARDS_DIR.glob("*.md")):
        if card.name.startswith("_"):
            continue
        limit = SIZE_LIMITS.get(card.name)
        size = card.stat().st_size
        flag = "" if not limit or size <= limit else "  <-- OVER"
        print(f"{card.name:32s} {size:>7,} / {limit or '-':>7}{flag}")
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] not in ("check", "sizes"):
        print(__doc__)
        return 2
    if argv[1] == "check":
        return cmd_check(argv[2:])
    return cmd_sizes()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
