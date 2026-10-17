#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 data/kr_chips/（jsonl、csv/、README.md）同步一份副本到 ~/v7-backtest/data/korea_chips/，供回測共用。

正本在本 repo 的 data/kr_chips/（雲端 CI 每個交易日更新）；v7-backtest 的 data/ 不進 git，只在本機。
同步是單向複製：只覆蓋內容有差異的檔案，不刪除目的地多出來的檔案；不碰 _state.json（抓取進度，不是資料）。

用法：
    python3 scripts/kr_chips/sync_to_v7.py                 # 複製到預設位置 ~/v7-backtest/data/korea_chips
    python3 scripts/kr_chips/sync_to_v7.py --dest /path    # 指定目的地（測試用）
    python3 scripts/kr_chips/sync_to_v7.py --dry-run       # 只列出會複製哪些檔案
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "kr_chips"
DEFAULT_DEST = Path.home() / "v7-backtest" / "data" / "korea_chips"


def files_to_sync(src: Path) -> list[Path]:
    """要同步的檔案（相對 src 的路徑）：*.jsonl、csv/*.csv、README.md。"""
    out = sorted(p.relative_to(src) for p in src.glob("*.jsonl"))
    out += sorted(p.relative_to(src) for p in (src / "csv").glob("*.csv")) if (src / "csv").is_dir() else []
    if (src / "README.md").exists():
        out.append(Path("README.md"))
    return out


def sync(src: Path, dest: Path, dry_run: bool = False) -> tuple[int, int]:
    """回傳（複製檔數, 未變動檔數）。"""
    copied = same = 0
    for rel in files_to_sync(src):
        s, d = src / rel, dest / rel
        if d.exists() and filecmp.cmp(s, d, shallow=False):
            same += 1
            continue
        copied += 1
        print(("會複製 " if dry_run else "複製 ") + str(rel))
        if not dry_run:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
    return copied, same


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dest", default=str(DEFAULT_DEST))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not SRC.is_dir():
        print(f"找不到來源目錄：{SRC}", file=sys.stderr)
        return 1
    copied, same = sync(SRC, Path(args.dest).expanduser(), args.dry_run)
    print(f"完成：複製 {copied} 檔，未變動 {same} 檔 → {args.dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
