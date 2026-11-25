#!/usr/bin/env python3
"""替已寫好的精簡版個股研究補一章「資本報酬」（不重寫全文）。

1. 重抓 yfinance 年報，把投入資本報酬率段 [p:roic] 補進 run 目錄的 pack.md／pack.json（零 LLM）。
2. 一通 opus（不上網、effort low）只寫「## 資本報酬」這一章，插在「## 護城河與競爭」之後、下一個二級標題之前；
   機器欄位 capital_return 寫進 machine.json。
3. 不渲染、不發布：之後跑 `python3 scripts/dd5/dd.py <T> --date <D> --reuse` 重排並發布。

用法：python3 scripts/dd5/add_roic.py TICKER [--date YYYYMMDD] [--force]
  --force  文章已有「## 資本報酬」時仍重寫（先拿掉舊的那章）
每檔約 0.1～0.3 美元、1～2 分鐘。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (str(HERE.parent), str(HERE.parent / "dd2"), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import importlib.util  # noqa: E402


def _load(name, path):  # 照路徑載入：pack.py 會把 dd2 插到搜尋路徑前面，dd2 也有 run.py，直接 import 會抓錯
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


import os  # noqa: E402
os.environ.setdefault("DD5_RUN_LIMIT", "5")  # 跟 dd.py 一樣用單檔累計上限，不看全部試跑累計
rn = _load("dd5_run", HERE / "run.py")
pk_ = _load("dd5_pack", HERE / "pack.py")

CHAPTER = "## 資本報酬"


def card_parts():
    """從 lite_card.md 取出「資本報酬」那段規則、文字規則、數字與出處規則，不另寫一份以免兩邊走樣。"""
    card = (rn.CARDS / "lite_card.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*資本報酬\*\*：.*?(?=\n\*\*獲利的品質\*\*)", card, re.S)
    if not m:
        raise SystemExit("lite_card.md 找不到「資本報酬」段")
    sec = {}
    for name in ("文字", "數字與出處"):
        mm = re.search(r"^## {0}\n(.*?)(?=^## )".format(name), card, re.S | re.M)
        sec[name] = mm.group(1).strip() if mm else ""
    return m.group(0).strip(), sec["文字"], sec["數字與出處"]


def refresh_pack(run_dir, t, date):
    """把 [p:roic] 段補進（或換掉）既有資料包。回傳該段 markdown（金融業或算不出來時回傳 None）。"""
    import yfinance as yf
    p = pk_.Pack(t, date)
    pk_.roic_section(p, yf.Ticker(t))
    md_path, js_path = run_dir / "pack.md", run_dir / "pack.json"
    md = md_path.read_text(encoding="utf-8")
    js = json.loads(js_path.read_text(encoding="utf-8"))
    md = re.sub(r"(?ms)^## \[p:roic\] .*?(?=^## \[p:)", "", md)  # 重跑時先拿掉舊段
    sec_md = None
    for tag, title, body in p.sections:
        sec_md = "## [p:{0}] {1}\n\n{2}\n\n".format(tag, title, body)
        md = md.replace("## [p:gaps] 缺口清單", sec_md + "## [p:gaps] 缺口清單", 1)
        js.setdefault("tags", {})[tag] = p.tags[tag]
    if "roic" in p.extra:
        js["roic"] = p.extra["roic"]
    else:
        js.pop("roic", None)
    for g in p.gaps:
        if g not in js.get("gaps", []):
            js.setdefault("gaps", []).append(g)
    md_path.write_text(md, encoding="utf-8")
    js_path.write_text(json.dumps(js, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return sec_md, p.gaps


def section(md, tag):
    m = re.search(r"(?ms)^## \[p:{0}\] .*?(?=^## \[p:)".format(re.escape(tag)), md)
    return m.group(0).strip() if m else ""


def build_prompt(run_dir, article, roic_md, gaps):
    rule, prose, nums = card_parts()
    pack_md = (run_dir / "pack.md").read_text(encoding="utf-8")
    peers_md = (run_dir / "peers.md").read_text(encoding="utf-8") if (run_dir / "peers.md").exists() else ""
    ctx = "\n\n".join(x for x in [section(pack_md, "consensus"), section(pack_md, "fin_annual"), roic_md or "", peers_md] if x)
    fin_note = ""
    if not roic_md:
        fin_note = "\n資料包沒有 [p:roic] 段（{0}）。照規則的金融業寫法：用同業表的股東權益報酬率回答前兩件事，不放圖。\n".format("；".join(gaps) or "算不出來")
    return """你是買方分析師。下面是一份已經寫好的個股研究正文，以及程式備好的資料。這份報告少了一章「資本報酬」，你只寫這一章，不改其他章。

## 這一章的規則

{rule}
{fin_note}
## 文字

{prose}

## 數字與出處

{nums}

不上網。只用下面的資料與正文已有的事實；跟正文已講過的內容不要重複，必要時一句帶過並指回該節。

## 輸出

只輸出兩樣東西：
1. 這一章的 Markdown，第一行是 `## 資本報酬`，不要輸出其他章、不要開場白。
2. 一個 ```json 區塊：{{"capital_return": {{"trend": "變強|持平|變弱", "evidence": "一句話帶數字，註明口徑（程式自算或 dd-screener）"}}}}

## 程式備好的資料（共識、年報、投入資本報酬率、同業表）

{ctx}

## 已寫好的正文

{article}
""".format(rule=rule, fin_note=fin_note, prose=prose, nums=nums, ctx=ctx, article=article)


def insert_chapter(article, chapter):
    article = re.sub(r"(?ms)^## 資本報酬\n.*?(?=^## )", "", article)  # --force：先拿掉舊章
    m = re.search(r"(?m)^## 護城河與競爭\s*$", article)
    if m:
        nxt = re.search(r"(?m)^## ", article[m.end():])
        if nxt:
            pos = m.end() + nxt.start()
            return article[:pos] + chapter.strip() + "\n\n" + article[pos:]
    m = re.search(r"(?m)^## 獲利的品質\s*$", article)
    if m:
        return article[:m.start()] + chapter.strip() + "\n\n" + article[m.start():]
    raise SystemExit("找不到「## 護城河與競爭」或「## 獲利的品質」，不知道插在哪")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--date", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--from-raw", action="store_true", help="不呼叫模型，改用 run 目錄已存的 raw_roic_add.json 取章（上次解析失敗時用）")
    a = ap.parse_args()
    t = a.ticker.upper()
    date = a.date
    if not date:
        import datetime as dt
        from zoneinfo import ZoneInfo
        date = dt.datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y%m%d")
    run = rn.Run(t, date)
    art_path = run.dir / "article.md"
    article = art_path.read_text(encoding="utf-8")
    if re.search(r"(?m)^## 資本報酬\s*$", article) and not (a.force or a.from_raw):
        print("{0}：文章已有「資本報酬」章，略過（要重寫加 --force）".format(t))
        return
    if a.from_raw:
        raw = json.loads((run.dir / "raw_roic_add.json").read_text(encoding="utf-8"))
        text = raw.get("stitched_text") or (raw.get("result_event") or {}).get("result") or ""
        roic_md = section((run.dir / "pack.md").read_text(encoding="utf-8"), "roic") or None
    else:
        roic_md, gaps = refresh_pack(run.dir, t, date)
        run.pack_md = (run.dir / "pack.md").read_text(encoding="utf-8")
        prompt = build_prompt(run.dir, article, roic_md, gaps)
        rn.EFFORT.setdefault("roic_add", "low")
        r = run.oneshot("roic_add", "opus", prompt, "roic_add")
        text = rn.need_text(r)
    body, machine, err = rn.extract_machine(text)
    m = re.search(r"## 資本報酬", body)  # 模型偶爾把思考貼在標題前、標題不在行首，所以不限行首
    if not m:
        raise SystemExit("輸出沒有「## 資本報酬」：" + body[:300])
    chapter = body[m.start():].strip()
    chapter = re.split(r"(?m)^## (?!資本報酬)", chapter)[0].strip()  # 只留這一章
    if roic_md and "{{圖:資本報酬}}" not in chapter:
        chapter = re.sub(r"^## 資本報酬\s*\n", "## 資本報酬\n\n{{圖:資本報酬}}\n\n", chapter, count=1)
    (run.dir / "article.md.pre_roic").write_text(article, encoding="utf-8")
    art_path.write_text(insert_chapter(article, chapter), encoding="utf-8")
    mj = run.dir / "machine.json"
    mach = json.loads(mj.read_text(encoding="utf-8"))
    if machine and machine.get("capital_return"):
        mach["capital_return"] = machine["capital_return"]
        mj.write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        print("（機器欄位 capital_return 沒解析到：{0}）".format(err))
    print("{0}：已補「資本報酬」章（{1} 字），原文備份 article.md.pre_roic".format(t, len(re.sub(r"\s+", "", chapter))))


if __name__ == "__main__":
    main()
