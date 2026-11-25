#!/usr/bin/env python3
"""把精簡版研究發布到個股儀表板（零 LLM）。

用法：python3 scripts/dd5/publish.py TICKER --date YYYYMMDD --site <網站 worktree 根目錄>
做四件事：先跑 lint（block 為 0 才往下）→ 輸出全文頁到 <site>/docs/stock-dash/research/<T>_<YYYYMMDD>.html
→ 對新頁注入站上導覽列（失敗直接報錯）→ 更新 <site>/docs/stock-dash/research/index.json（每檔只留最新一份）。
一般用 scripts/dd5/dd.py 一鍵跑；本檔的 publish() 函式給它呼叫，也可單獨執行。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent), str(HERE.parent / "dd2"), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import lint  # noqa: E402
import render as rd  # noqa: E402

PILOT = Path.home() / "dd5-pilot"


class LintBlocked(Exception):
    def __init__(self, blocks):
        super().__init__("lint 有 {0} 個 block".format(len(blocks)))
        self.blocks = blocks


def inject_nav(page, site, scripts_dir):
    """對新頁注入站上導覽列。site_nav 從 scripts_dir 載入，其 ROOT 改指到 <site>/docs（預覽目錄也能用）。"""
    sd_ = str(scripts_dir)
    if sd_ not in sys.path:
        sys.path.insert(0, sd_)
    import site_nav  # noqa: E402
    site_nav.ROOT = Path(site).resolve() / "docs"
    st = site_nav.process(Path(page).resolve())
    if st not in ("updated", "unchanged"):
        raise RuntimeError("注入導覽列失敗：site_nav.process 回傳 {0}（{1}）".format(st, page))
    return st


def publish(t, d, site, scripts_dir=None):
    """發布到 <site>/docs/stock-dash/research/。回傳 dict：page、index、removed（被刪掉的舊頁，相對 site）、
    lint_hits、res（render 結果）、changed（是否有寫入新索引）。lint 有 block 丟 LintBlocked，不寫任何檔。"""
    run = PILOT / "runs" / "{0}_{1}".format(t, d)
    sd = Path(site) / "docs" / "stock-dash"
    out = lint.lint_run(run)
    blocks = [h for h in out["hits"] if h["severity"] == "block"]
    if blocks:
        raise LintBlocked(blocks)

    rdir = sd / "research"
    rdir.mkdir(parents=True, exist_ok=True)
    fname = "{0}_{1}.html".format(t, d)
    page = rdir / fname
    res = rd.render(run, out=page, back_link="/stock-dash/?t=" + t)
    inject_nav(page, site, scripts_dir or HERE.parent)

    pack = json.loads((run / "pack.json").read_text(encoding="utf-8"))
    mach = json.loads((run / "machine.json").read_text(encoding="utf-8"))
    article = (run / "article.md").read_text(encoding="utf-8")
    title = t
    for ln in article.splitlines():
        if ln.startswith("# "):
            title = ln[2:].strip()
            break
    mo = mach.get("moat") or {}
    iso = "{0}-{1}-{2}".format(d[:4], d[4:6], d[6:])
    entry = {
        "date": iso,
        "path": "research/" + fname,
        "title": title,
        "one_liner": mach.get("one_liner"),
        "business_direction": mach.get("business_direction"),
        "price_implies": mach.get("price_implies"),
        "moat": {"source": mo.get("source"), "trend": mo.get("trend"), "main_threat": mo.get("main_threat")},
        "tracking": [{k: x.get(k) for k in ("metric", "bull_if", "warn_if", "next_check")} for x in mach.get("tracking", [])],
        "price": pack.get("last_price"),
        "price_date": (pack.get("price_chart") or {}).get("last_date"),
    }
    ip = rdir / "index.json"
    idx = json.loads(ip.read_text(encoding="utf-8")) if ip.exists() else {}
    old = idx.get(t)
    removed = []
    changed = True
    if old and old.get("date", "") > iso:
        print("{0} 已有較新的 {1}，不覆蓋索引".format(t, old["date"]))
        page.unlink(missing_ok=True)  # 不留沒被索引指到的孤兒頁
        changed = False
    else:
        if old and old.get("path") != entry["path"]:
            (sd / old["path"]).unlink(missing_ok=True)  # 每檔只留最新一份
            removed.append("docs/stock-dash/" + old["path"])
        idx[t] = entry
    ip.write_text(json.dumps(idx, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return {"page": page, "index": ip, "removed": removed, "lint_hits": out["hits"], "res": res, "changed": changed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--date", required=True, help="YYYYMMDD")
    ap.add_argument("--site", required=True, help="網站 worktree 根目錄")
    a = ap.parse_args()
    t, d = a.ticker.upper(), a.date
    if len(d) != 8 or not d.isdigit():
        raise SystemExit("--date 要 YYYYMMDD")
    if not (Path(a.site) / "docs" / "stock-dash").is_dir():
        raise SystemExit("找不到 " + str(Path(a.site) / "docs" / "stock-dash"))
    try:
        r = publish(t, d, a.site, scripts_dir=Path(a.site) / "scripts")
    except LintBlocked as e:
        for h in e.blocks:
            print("  [block] {0} L{1}: {2}".format(h["rule"], h["line"], h["text"]), file=sys.stderr)
        raise SystemExit("{0} lint 有 {1} 個 block，未發布".format(t, len(e.blocks)))
    print("{0} 已發布 → {1}（number_check_bad={2}）".format(t, r["page"], r["res"].get("number_check_bad")))


if __name__ == "__main__":
    main()
