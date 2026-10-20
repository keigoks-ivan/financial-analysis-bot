#!/usr/bin/env python3
"""產生 docs/supply-chain/data/content_asof.json：各主題 JSON「內容最後一次變動」的日期。

供 engine.js 在 share／marketSize／growth／terminal_markets 數字旁標「YYYY-MM 估」，
也供頁頂「結構資料截至 …」使用。格式：{topic: "YYYY-MM-DD"}。

判定：沿 git 歷史（只看已 commit 的版本）比對相鄰兩版，下列不算內容變動：
  - JSON 排版／縮排（比對的是解析後的物件）
  - companies[].ticker 欄位的差異
  - commit 標題含 ticker 或「代號」的 commit（代號修正常順手拆分「A / B」複合列、補公司列，
    那是讓價格層對得上代號，不是重新研究 share／marketSize／growth）
所以代號修正 commit 的標題要寫 ticker 或代號；寫別的字會被當成內容更新，日期被推到修正當天。
重跑後腳本會列出和既有 content_asof.json 不同的主題，請先看過再 commit。

需要完整 git 歷史（CI 淺 checkout 讀不到），所以在本機跑、結果 commit；
淺 checkout 下找不到歷史時保留舊檔該主題的值。
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "supply-chain" / "data"
OUT = DATA / "content_asof.json"
NON_TOPIC = {"topics", "dd_links", "terminal_markets", "substitution_lags",
             "live", "live_health", "live_mcap", "content_asof"}


SKIP_SUBJECT = re.compile(r"ticker|代號", re.I)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def normalize(raw: str) -> str:
    d = json.loads(raw)
    for n in d.get("nodes", []) or []:
        for c in n.get("companies", []) or []:
            if isinstance(c, dict):
                c.pop("ticker", None)
    return json.dumps(d, sort_keys=True, ensure_ascii=False)


def content_date(path: Path, today: str) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    log = [ln.split(" ", 2) for ln in git("log", "--format=%H %cs %s", "--", rel).splitlines() if ln.strip()]
    if not log:
        return today if path.exists() else None
    # 代號修正 commit 不算內容變動：把它的變動併回下一個版本（等同跳過）
    log = [x for x in log if not SKIP_SUBJECT.search(x[2])] or log[-1:]
    versions = []
    for h, d, _subj in log:
        try:
            versions.append((d, normalize(git("show", f"{h}:{rel}"))))
        except Exception:  # noqa: BLE001  檔案在該版不存在或壞掉
            versions.append((d, None))
    for i in range(len(versions) - 1):
        if versions[i][1] != versions[i + 1][1]:
            return versions[i][0]
    return versions[-1][0]  # 從建檔起沒變過


def main() -> int:
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d")
    old = {}
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
    res = {}
    for f in sorted(DATA.glob("*.json")):
        if f.stem in NON_TOPIC:
            continue
        try:
            d = content_date(f, today)
        except Exception as e:  # noqa: BLE001
            print(f"{f.stem}: {e}", file=sys.stderr)
            d = None
        res[f.stem] = d or old.get(f.stem)
    res = {k: v for k, v in res.items() if v}
    for k, v in sorted(res.items()):
        if old.get(k) not in (None, v):
            print(f"  變動：{k} {old[k]} -> {v}")
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    vals = sorted(set(res.values()))
    print(f"content_asof.json：{len(res)} 個主題，日期 {', '.join(vals)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
