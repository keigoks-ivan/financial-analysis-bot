#!/usr/bin/env python3
"""把 docs/simulation/data 底下的大型行情 JSON 壓成 .json.gz，並刪掉原檔。

2026-10-19：/simulation/ 的行情檔合計 207 MiB（站台體積的 21%），改存 gzip 後約 31 MiB。
頁面端由 docs/simulation/gzjson.js 用 DecompressionStream 解壓；GitHub Pages 對 .gz 不加
Content-Encoding，瀏覽器拿到的是原始 gzip 位元組。

四個小清單維持純 JSON（頁面照舊 fetch）：manifest.json、stocks/catalog.json、
stocks/index-etfs.json、campaigns/catalog.json。其餘 *.json 一律壓縮。

模擬頁的行情檔來源是 v7-backtest/market-replay 的匯出程式（不在本 repo），
之後重新匯出、複製進 docs/simulation/data 後，跑一次這支腳本再提交。

壓縮輸出固定（level 9、mtime 0），同一份輸入每次產生相同位元組；
每個檔先確認解壓後與原檔逐位元相同才刪原檔。可重跑（已壓縮的不動）。

用法：
  python3 scripts/gzip_simulation_data.py            # 壓縮並刪原檔
  python3 scripts/gzip_simulation_data.py --check    # 只檢查，有未壓縮的大檔或壞檔就回傳 1
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "simulation" / "data"
PLAIN = {"manifest.json", "stocks/catalog.json", "stocks/index-etfs.json", "campaigns/catalog.json"}


def compressible(data_dir):
    """尚未壓縮、應該壓縮的 JSON。"""
    data_dir = Path(data_dir)
    return [p for p in sorted(data_dir.rglob("*.json")) if p.relative_to(data_dir).as_posix() not in PLAIN]


def pack(data_dir):
    """壓縮並刪原檔，回傳 (檔數, 原始位元組, 壓縮後位元組)。"""
    n = raw_total = gz_total = 0
    for path in compressible(data_dir):
        raw = path.read_bytes()
        packed = gzip.compress(raw, 9, mtime=0)
        if gzip.decompress(packed) != raw:
            raise RuntimeError("壓縮後解壓與原檔不同：" + str(path))
        target = path.with_name(path.name + ".gz")
        target.write_bytes(packed)
        path.unlink()
        n += 1
        raw_total += len(raw)
        gz_total += len(packed)
    return n, raw_total, gz_total


def check(data_dir):
    """回傳問題清單：還沒壓縮的大檔、解壓失敗或不是 JSON 的 .gz。"""
    data_dir = Path(data_dir)
    problems = ["未壓縮：" + p.relative_to(data_dir).as_posix() for p in compressible(data_dir)]
    for path in sorted(data_dir.rglob("*.json.gz")):
        try:
            json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
        except (OSError, EOFError, ValueError) as exc:
            problems.append("壞檔：{0}（{1}）".format(path.relative_to(data_dir).as_posix(), exc))
    for rel in sorted(PLAIN):
        if not (data_dir / rel).exists():
            problems.append("缺少清單檔：" + rel)
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--data-dir", type=Path, default=DATA)
    args = ap.parse_args()
    if not args.check:
        n, raw, packed = pack(args.data_dir)
        print("壓縮 {0} 個檔：{1:.1f} MiB -> {2:.1f} MiB".format(n, raw / 2 ** 20, packed / 2 ** 20))
    problems = check(args.data_dir)
    for line in problems:
        print(line)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
