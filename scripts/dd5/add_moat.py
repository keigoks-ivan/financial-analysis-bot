#!/usr/bin/env python3
"""替已寫好的精簡版個股研究重寫「護城河與競爭」一章，補上寬度判斷（不重寫全文）。

1. 同業：沿用 run 目錄的 peers.json（不重抓，其他章引用的同業數字才不會變）；若還沒有固定名單，順手把這份名單存成固定名單。
2. 程式算對同業中位數的三年差距與初判（moat_gap.py，零 LLM），寫 moat_gap.md／moat_gap.json，pack.json 登記 [p:moat_gap]。
3. 一通 opus（effort low；只為了查需求轉弱年度可上網三次）只重寫「## 護城河與競爭」這一章：保留原章的事實與數字，最後的判斷改成寬度＋走勢，
   機器欄位 moat 換成新格式（width、width_basis、width_cap、early_signal、threat_first_sign、unproven_edges）。
4. 不渲染、不發布：之後跑 `python3 scripts/dd5/dd.py <T> --date <D> --reuse` 重排並發布。

用法：python3 scripts/dd5/add_moat.py TICKER --date YYYYMMDD [--force] [--from-raw]
  --force     machine.json 的 moat 已有 width 時仍重寫
  --from-raw  不呼叫模型，用 run 目錄已存的 raw_moat_add.json 取章（上次解析失敗時用）
每檔約 0.25～0.4 美元、一分鐘左右。原文備份 article.md.pre_moat、machine.json.pre_moat。
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
import moat_gap  # noqa: E402

CHAPTER = "## 護城河與競爭"


def card_parts():
    """從 lite_card.md 取「護城河與競爭」規則、文字規則、數字與出處規則、機器欄位 moat 的格式，不另寫一份以免走樣。"""
    card = (rn.CARDS / "lite_card.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*護城河與競爭\*\*：.*?(?=\n\*\*資本報酬\*\*)", card, re.S)
    if not m:
        raise SystemExit("lite_card.md 找不到「護城河與競爭」段")
    sec = {}
    for name in ("文字", "數字與出處"):
        mm = re.search(r"^## {0}\n(.*?)(?=^## )".format(name), card, re.S | re.M)
        sec[name] = mm.group(1).strip() if mm else ""
    mf = re.search(r'  "moat": \{.*?\n  \},', card, re.S)
    if not mf:
        raise SystemExit("lite_card.md 找不到 moat 欄位格式")
    return m.group(0).strip(), sec["文字"], sec["數字與出處"], mf.group(0).strip().rstrip(",")


def section(md, tag):
    m = re.search(r"(?ms)^## \[p:{0}\] .*?(?=^## \[p:)".format(re.escape(tag)), md)
    return m.group(0).strip() if m else ""


def old_chapter(article):
    m = re.search(r"(?ms)^## 護城河與競爭\s*\n.*?(?=^## )", article)
    if not m:
        raise SystemExit("文章找不到「## 護城河與競爭」章")
    return m


def build_prompt(run_dir, article, gap_md):
    rule, prose, nums, moat_fmt = card_parts()
    pack_md = (run_dir / "pack.md").read_text(encoding="utf-8")
    peers_md = (run_dir / "peers.md").read_text(encoding="utf-8") if (run_dir / "peers.md").exists() else "（這份研究沒有同業對照表）"
    ctx = "\n\n".join(x for x in [section(pack_md, "biz"), section(pack_md, "fin_annual"), section(pack_md, "roic"), peers_md,
                                  gap_md or "（程式算不出初判：沒有同業表或可比年度不足，照「缺同業」上限處理）"] if x)
    return """你是買方分析師。下面是一份已經寫好的個股研究正文，以及程式備好的資料。請只重寫「護城河與競爭」這一章，其他章不動。

重寫的方式：
- 原章的事實、數字、出處標記與對手表照舊保留，可以刪掉重複的句子，但不要換掉數字，也不要新增沒有出處的數字。
- 章末的判斷改成照下面規則判寬度（寬、窄、無）與走勢（變強、持平、變弱），寫出各憑哪個數字；改了程式初判要寫套用哪一條。
- 照規則補「說得出來、但數字上看不到的優勢」，最多兩條，寫進 json；正文在判斷之前用一兩句列出這幾條優勢、各看哪個數字，正文不要提機器欄位或 json。
- 判斷需要的事實正文與資料都沒有時，寫「公開資料沒有」，照規則套上限，不要猜。

## 這一章的規則

{rule}

## 文字

{prose}

## 數字與出處

{nums}

原則上不上網。只有一個例外：判斷「品牌」上限時，資料包看不到 2020 年或 2008～2009 年這類需求轉弱年度，可以上網查那一年的營收與毛利率（或飯店、郵輪改看營業利益率），最多搜尋三次；查到就照實判，並在正文附連結。

## 輸出

只輸出兩樣東西：
1. 這一章的 Markdown，第一行是 `## 護城河與競爭`，不要輸出其他章、不要開場白。
2. 一個 ```json 區塊：{{{moat_fmt}}}

## 程式備好的資料（生意概況、年報、投入資本報酬率、同業表、護城河寬度初判）

{ctx}

## 已寫好的正文

{article}
""".format(rule=rule, prose=prose, nums=nums, moat_fmt=moat_fmt, ctx=ctx, article=article)


def call_with_web(run, prompt):
    """一通 opus，只為了查「需求轉弱年度」那一條可以上網（最多三次搜尋）；照 step_lite 的寫法呼叫，花費記進 manifest。"""
    import time
    import dd_headless
    import llm
    run.guard()
    pp = run.dir / "prompt_moat_add.md"
    pp.write_text(prompt, encoding="utf-8")
    llm.NEUTRAL_CWD.mkdir(parents=True, exist_ok=True)
    out_json = str((run.dir / "raw_moat_add.json").resolve())
    t0 = time.time()
    r = dd_headless.spawn(prompt_path=str(pp.resolve()), model="opus", allowed_tools=["WebSearch", "WebFetch"], max_turns=8,
                          out_json=out_json, cwd=llm.NEUTRAL_CWD,
                          extra_args=["--setting-sources", "project", "--effort", "low", "--max-budget-usd", "1"])
    r = rn.sp._augment_with_raw_usage(r, out_json)
    c = run.record("moat_add", "moat_add", "opus", r, t0)
    run.save()
    print("[moat_add] opus ok={0} ${1} {2}s turns={3} out_tok={4}".format(r.get("ok"), c["cost_usd"], c["duration_s"], c["num_turns"], c["output_tokens"]))
    return rn.need_text(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--date", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--from-raw", action="store_true")
    a = ap.parse_args()
    t = a.ticker.upper()
    run = rn.Run(t, a.date)
    art_path, mj = run.dir / "article.md", run.dir / "machine.json"
    article = art_path.read_text(encoding="utf-8")
    mach = json.loads(mj.read_text(encoding="utf-8"))
    if (mach.get("moat") or {}).get("width") and not (a.force or a.from_raw):
        print("{0}：護城河已有寬度，略過（要重寫加 --force）".format(t))
        return
    old = old_chapter(article)

    # 同業與初判（零 LLM）
    pj = run.dir / "peers.json"
    if pj.exists():
        fixed = rn.PEERS_FIXED / "{0}.json".format(t)
        if not fixed.exists():
            peers = [k for k in json.loads(pj.read_text(encoding="utf-8")).get("data", {}) if k != t]
            rn.PEERS_FIXED.mkdir(parents=True, exist_ok=True)
            fixed.write_text(json.dumps({"ticker": t, "peers": peers, "source": "沿用 {0}_{1} 已發布研究的同業名單".format(t, a.date),
                                         "saved": a.date}, ensure_ascii=False, indent=1), encoding="utf-8")
    res = moat_gap.build(run.dir, t)
    gap_md = (run.dir / "moat_gap.md").read_text(encoding="utf-8") if res else ""
    if res:
        pk = run.dir / "pack.json"
        js = json.loads(pk.read_text(encoding="utf-8"))
        js.setdefault("tags", {})["moat_gap"] = {"title": "護城河寬度初判（程式用同業對照表算）", "source": "yfinance", "url": "", "asof": a.date}
        pk.write_text(json.dumps(js, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("[moat_gap]", (res or {}).get("width_initial"), (res or {}).get("trend_initial"), (res or {}).get("gap_vs_peer_median"))

    if a.from_raw:
        raw = json.loads((run.dir / "raw_moat_add.json").read_text(encoding="utf-8"))
        text = raw.get("stitched_text") or (raw.get("result_event") or {}).get("result") or ""
    else:
        prompt = build_prompt(run.dir, article, gap_md)
        text = call_with_web(run, prompt)
    body, machine, err = rn.extract_machine(text)
    m = re.search(r"## 護城河與競爭", body)
    if not m:
        raise SystemExit("輸出沒有「## 護城河與競爭」：" + body[:300])
    chapter = body[m.start():].strip()
    chapter = re.split(r"(?m)^## (?!護城河與競爭)", chapter)[0].strip()
    if not (machine and isinstance(machine.get("moat"), dict) and machine["moat"].get("width")):
        raise SystemExit("機器欄位 moat 沒解析到或缺 width（{0}）；文章沒改。可用 --from-raw 重取".format(err))

    (run.dir / "article.md.pre_moat").write_text(article, encoding="utf-8")
    (run.dir / "machine.json.pre_moat").write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")
    art_path.write_text(article[:old.start()] + chapter + "\n\n" + article[old.end():], encoding="utf-8")
    mach["moat"] = machine["moat"]
    mj.write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")
    moat_gap.merge_into_machine(run.dir)
    mo = machine["moat"]
    print("{0}：已重寫「護城河與競爭」（{1} 字）→ 寬度 {2}／走勢 {3}／上限 {4}；原文備份 article.md.pre_moat".format(
        t, len(re.sub(r"\s+", "", chapter)), mo.get("width"), mo.get("trend"), mo.get("width_cap") or "無"))


if __name__ == "__main__":
    main()
