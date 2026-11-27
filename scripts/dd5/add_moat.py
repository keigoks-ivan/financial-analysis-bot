#!/usr/bin/env python3
"""替已寫好的精簡版個股研究重判護城河、重寫「護城河與競爭」一章（不重寫全文）。2026-11-27 起改用競爭結構版（moat_judge.py）。

1. 同業：沿用 run 目錄的 peers.json（不重抓，其他章引用的同業數字才不會變）；若還沒有固定名單，順手把這份名單存成固定名單。
2. 程式算十年財報數字（moat_long.py，零 LLM），pack.json 登記 [p:moat_long]。
3. 事實檔：~/dd5-pilot/moat_facts/<代號>_F.json 180 天內有就沿用，沒有就一通 opus 上網建（約 0.5 美元、一分鐘）。
4. 一通 opus（不上網、effort low，約 0.2 美元）照 cards/moat_card.md 判寬度、證據強度、走勢，重寫這一章並換掉機器欄位 moat。
5. 不渲染、不發布：之後跑 `python3 scripts/dd5/dd.py <T> --date <D> --reuse` 重排並發布。

用法：python3 scripts/dd5/add_moat.py TICKER --date YYYYMMDD [--force] [--from-raw]
  --force     已經是競爭結構版的也重判
  --from-raw  不呼叫模型，用 run 目錄已存的 raw_moat_judge.json 取章（上次解析失敗時用）
原文備份 article.md.pre_moat、machine.json.pre_moat。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent), str(HERE.parent / "dd2"), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _load(name, path):  # 照路徑載入：dd2 也有 run.py，直接 import 會抓錯
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


os.environ.setdefault("DD5_RUN_LIMIT", "5")
rn = _load("dd5_run", HERE / "run.py")
import moat_judge  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--date", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--from-raw", action="store_true")
    a = ap.parse_args()
    t = a.ticker.upper()
    run = rn.Run(t, a.date)
    mach = json.loads((run.dir / "machine.json").read_text(encoding="utf-8"))
    if (mach.get("moat") or {}).get("rule") == "競爭結構版 2026-11-27" and not (a.force or a.from_raw):
        print("{0}：護城河已是競爭結構版，略過（要重判加 --force）".format(t))
        return
    pj = run.dir / "peers.json"
    if pj.exists():
        fixed = rn.PEERS_FIXED / "{0}.json".format(t)
        if not fixed.exists():
            peers = [k for k in json.loads(pj.read_text(encoding="utf-8")).get("data", {}) if k != t]
            rn.PEERS_FIXED.mkdir(parents=True, exist_ok=True)
            fixed.write_text(json.dumps({"ticker": t, "peers": peers, "source": "沿用 {0}_{1} 已發布研究的同業名單".format(t, a.date),
                                         "saved": a.date}, ensure_ascii=False, indent=1), encoding="utf-8")
    moat_judge.rewrite(run, from_raw=a.from_raw)


if __name__ == "__main__":
    main()
