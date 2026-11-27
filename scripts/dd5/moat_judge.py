#!/usr/bin/env python3
"""護城河判定（競爭結構版，2026-11-27 起）：事實檔＋十年財報數字＋不上網判定，重寫「## 護城河與競爭」一章。

流程（規格見 cards/moat_card.md，試驗紀錄 ~/dd5-pilot/moat_trial/）：
  1. moat_long.py 算十年財報數字 R（零 LLM，讀本機共用資料庫）。
  2. 事實檔 F：一通 opus 上網查八格（份額、家數、新進者、客戶、主力生意、轉換成本、價格），存 ~/dd5-pilot/moat_facts/<代號>_F.json，
     之後重複用（180 天內不重查；DD5_MOAT_FACTS_REFRESH=1 強制重查）。新研究時在 peers 步驟就背景開跑，跟寫稿並行。
  3. 一通 opus（不上網、effort low）照判準卡判寬度、證據強度、走勢，並重寫這一章：保留原章事實與數字，補事實檔的出處。
費用：事實檔約 0.5 美元、一分鐘（每檔第一次）；判定加改寫約 0.2 美元、半分鐘。
"""
from __future__ import annotations

import concurrent.futures
import datetime as dt
import json
import os
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARDS = HERE / "cards"
FACTS_DIR = Path.home() / "dd5-pilot" / "moat_facts"  # 本機，不進 git
FACTS_TTL_DAYS = 180
CHAPTER = "## 護城河與競爭"

F_FMT = """{"F1": {"market": "主要市場的界定", "value": "本檔份額與排名、第二名份額", "link": "", "date": "", "level": "研調或主管機關|券商或媒體估計|公司公布|管理層說法|查不到"},
 "F2": {...同格式：兩到三年前的份額，同一來源同一口徑},
 "F3": {...有效供應商家數},
 "F4": {...新進者、客戶自製、替代技術已拿到的份額與三年變化},
 "F5": {...最大客戶占營收多少、客戶有沒有第二供應商},
 "F6": {...現在主力生意占營收多少；程式找到的下行年那一年它占營收多少；下滑是否因分拆、出售事業或會計改變},
 "F7": {...換供應商的代價：認證幾個月、合約幾年、續約率},
 "F8": {...價格：實際漲價、對對手溢價或價差、成本大漲年毛利率變化}}"""

MOAT_FMT = """{"moat": {
  "width": "寬|窄|無",
  "strength": "強|中|弱",
  "trend": "變強|持平|變弱",
  "source": "一句話：主要的結構來源",
  "width_basis": "一句話帶數字：憑哪幾項判這個寬度；觸發否決或卡在哪一條也寫",
  "evidence": "一句話帶數字：走勢的依據",
  "position": "一句地位，例如：份額第一，利潤被客戶拿走",
  "sources": [{"type": "轉換成本|網路效應|成本優勢|無形資產|有效規模", "evidence": "一句話＋數字", "level": "第三方|公司|管理層", "cells": ["F1"]}],
  "erosion": {"share": {"light": "綠|黃|紅|查不到", "fact": ""}, "entrants": {"light": "", "fact": ""}, "customer_power": {"light": "", "fact": ""},
              "downturn": {"light": "綠|黃|紅|未經下行檢驗", "year": "", "fact": ""}},
  "returns_check": {"metric": "", "avg": 0, "min": 0, "veto": "沒有觸發|最高窄|最高無|不適用"},
  "cyclical": false,
  "main_threat": "誰、用什麼方式",
  "threat_first_sign": "威脅成真時最先變壞的數字，與現值",
  "warnings": ["還沒發生的威脅＋哪個數字出現就算成真"]
}}"""


# ---------------------------------------------------------------- 事實檔
def facts_path(t):
    return FACTS_DIR / "{0}_F.json".format(t)


def facts_fresh(t):
    p = facts_path(t)
    if os.environ.get("DD5_MOAT_FACTS_REFRESH") or not p.exists():
        return False
    try:
        saved = json.loads(p.read_text(encoding="utf-8")).get("_saved", "")
        return (dt.date.today() - dt.date.fromisoformat(saved)).days <= FACTS_TTL_DAYS
    except Exception:
        return False


def _biz(run_dir):
    pk = Path(run_dir) / "pack.md"
    if not pk.exists():
        return ""
    m = re.search(r"(?ms)^## \[p:biz\] .*?(?=^## \[p:)", pk.read_text(encoding="utf-8"))
    return m.group(0).strip()[:2500] if m else ""


def facts_prompt(t, run_dir, r):
    return """你是研究助理，要替 {t} 建一份護城河事實檔。只蒐集事實，不判寬度。

規則：
- 八格各寫：數值或事實、出處連結、資料日期、證據等級（研調或主管機關／券商或媒體估計／公司公布／管理層說法）。
- 查不到就把 value 寫「查不到」、level 寫「查不到」。憑記憶的數字一律不能填；每個數字都要有你這次打開或搜尋到的出處。
- 份額優先找研調或主管機關（TrendForce、Counterpoint、IDC、Gartner、Yole、Prismark、Omdia、Euromonitor、Nilson、Drewry、Alphaliner、worldsteel、DOT／BTS 等）；F2 要跟 F1 同一來源、同一口徑，找不到同口徑就寫查不到。
- F5 只記事實（客戶占比、已經發生的二供），預估與傳聞另寫在 note，不要混進 value。
- 最多搜尋十次。

## 公司概況（程式資料包）
{biz}

## 程式算好的十年財報數字（R）
{R}

## 輸出
只輸出一個 ```json 區塊，格式（每格可加 "note"）：
{fmt}
""".format(t=t, biz=_biz(run_dir) or "（資料包沒有概況段）", R=json.dumps(r, ensure_ascii=False, indent=1) if r else "（沒有）", fmt=F_FMT)


def _spawn(run_dir, tag, prompt, web, budget, effort):
    import dd_headless
    import llm
    import spawn as sp
    llm.NEUTRAL_CWD.mkdir(parents=True, exist_ok=True)
    pp = Path(run_dir) / "prompt_{0}.md".format(tag)
    pp.write_text(prompt, encoding="utf-8")
    out_json = str((Path(run_dir) / "raw_{0}.json".format(tag)).resolve())
    t0 = time.time()
    r = dd_headless.spawn(prompt_path=str(pp.resolve()), model="opus", allowed_tools=(["WebSearch", "WebFetch"] if web else None),
                          max_turns=(16 if web else 2), out_json=out_json, cwd=llm.NEUTRAL_CWD,
                          extra_args=["--setting-sources", "project", "--effort", effort, "--max-budget-usd", str(budget)] + ([] if web else ["--tools", ""]))
    return sp._augment_with_raw_usage(r, out_json), t0


def _json_block(txt):
    ms = list(re.finditer(r"```json\s*(\{.*?\})\s*```", txt or "", re.S))
    for m in reversed(ms):
        try:
            return json.loads(m.group(1))
        except Exception:
            continue
    return None


def build_facts(t, run_dir, r):
    """上網建事實檔；回傳 (F, 呼叫結果, t0)。不寫 manifest（可能在背景執行緒跑），由呼叫端記帳。"""
    res, t0 = _spawn(run_dir, "moat_facts", facts_prompt(t, run_dir, r), True, 1.5, "medium")
    F = _json_block(res.get("result_text"))
    if F:
        F["_saved"] = dt.date.today().isoformat()
        F["_run"] = Path(run_dir).name
        FACTS_DIR.mkdir(parents=True, exist_ok=True)
        facts_path(t).write_text(json.dumps(F, ensure_ascii=False, indent=1), encoding="utf-8")
    return F, res, t0


_bg = {}
_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


def start_facts_bg(t, run_dir, r):
    """事實檔過期或沒有時背景開跑（跟寫稿並行）；有新鮮的就不跑。"""
    if facts_fresh(t) or t in _bg:
        return False
    _bg[t] = _pool.submit(build_facts, t, run_dir, r)
    return True


def get_facts(run, r):
    """取事實檔：背景有在跑就等它；沒有新鮮的就同步建。花費記進 manifest。"""
    t = run.t
    fut = _bg.pop(t, None)
    if fut is None and not facts_fresh(t):
        run.guard()
        fut = _pool.submit(build_facts, t, run.dir, r)
    if fut is not None:
        F, res, t0 = fut.result()
        c = run.record("moat_facts", "moat_facts", "opus", res, t0)
        run.save()
        print("[moat_facts] opus ok={0} ${1} {2}s turns={3}".format(res.get("ok"), c["cost_usd"], c["duration_s"], c["num_turns"]))
        if not F:
            raise SystemExit("事實檔 json 解析失敗（raw_moat_facts.json）；文章沒改")
    F = json.loads(facts_path(t).read_text(encoding="utf-8"))
    (run.dir / "moat_facts.json").write_text(json.dumps(F, ensure_ascii=False, indent=1), encoding="utf-8")  # 也進 lint 參考文字
    return F


# ---------------------------------------------------------------- 判定與改寫
def card_rules():
    card = (CARDS / "lite_card.md").read_text(encoding="utf-8")
    sec = {}
    for name in ("文字", "數字與出處"):
        mm = re.search(r"^## {0}\n(.*?)(?=^## )".format(name), card, re.S | re.M)
        sec[name] = mm.group(1).strip() if mm else ""
    return (CARDS / "moat_card.md").read_text(encoding="utf-8"), sec["文字"], sec["數字與出處"]


def old_chapter(article):
    m = re.search(r"(?ms)^## 護城河與競爭\s*\n.*?(?=^## )", article)
    if not m:
        raise SystemExit("文章找不到「## 護城河與競爭」章")
    return m


def judge_prompt(run_dir, t, chapter, r, F):
    spec, prose, nums = card_rules()
    peers_md = (Path(run_dir) / "peers.md").read_text(encoding="utf-8") if (Path(run_dir) / "peers.md").exists() else "（沒有同業對照表）"
    return """你是買方分析師。下面是一份已經寫好的個股研究（{t}）裡的「護城河與競爭」一章，以及程式數字與事實檔。請照判準判這家公司的護城河，並重寫這一章。不上網，只能用下面給的材料。

重寫的方式：
- 原章的事實、數字、出處標記與對手表照舊保留，可以刪掉重複的句子，但不要換掉數字。
- 事實檔的數字可以補進來，後面放它的出處連結：`（[來源名稱](網址)）`；程式十年數字後面加 `[p:moat_long]`。事實檔是「查不到」的格子就寫公開資料沒有，不要補。
- 結構：先講對手與差距（原章的表），再講結構來源（最多兩個，各附證據），再用一段講侵蝕四項（份額、新進者與替代、客戶議價、下行年）各是什麼情況，最後兩三句下判斷：寬度、證據強度、走勢，各憑哪個數字；觸發報酬率否決或卡在哪一條要寫出來。
- 正文不要提判準、燈號、事實檔、機器欄位或 json 這些字，用一般研究報告的說法寫。
- 篇幅：跟原章差不多長，最多多三成（原章約 {n} 字）。侵蝕四項合起來一段、每項一兩句；威脅只寫最大的一兩個。原章裡跟寬度判斷無關的細節可以刪。

## 判準

{spec}

## 文字

{prose}

## 數字與出處

{nums}

## 輸出

只輸出兩樣東西：
1. 這一章的 Markdown，第一行是 `## 護城河與競爭`，不要輸出其他章、不要開場白。
2. 一個 ```json 區塊：
{fmt}

## 程式十年財報數字（R，引用標記 [p:moat_long]）
{R}

## 事實檔（F，已凍結）
{F}

## 同業對照表（引用標記 [p:peers]）
{peers}

## 原章
{chapter}
""".format(t=t, spec=spec, prose=prose, nums=nums, fmt=MOAT_FMT, R=json.dumps(r, ensure_ascii=False, indent=1) if r else "（本檔沒有年度財報資料）",
           F=json.dumps({k: v for k, v in F.items() if not k.startswith("_")}, ensure_ascii=False, indent=1), peers=peers_md, chapter=chapter, n=len(re.sub(r"\s", "", chapter)))


def ensure_long(run):
    import moat_long
    pj = run.dir / "moat_long.json"
    if pj.exists():
        return json.loads(pj.read_text(encoding="utf-8"))
    r = moat_long.build(run.dir, run.t, moat_long.peers_of(run.dir, run.t))
    tag_long(run.dir, run.date, r)
    return r


def tag_long(run_dir, date, r):
    if not r:
        return
    pk = Path(run_dir) / "pack.json"
    js = json.loads(pk.read_text(encoding="utf-8"))
    js.setdefault("tags", {})["moat_long"] = {"title": "護城河十年財報數字（程式用{0}算）".format(r["source"]), "source": r["source"], "url": "", "asof": date}
    pk.write_text(json.dumps(js, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


def rewrite(run, from_raw=False):
    """判定＋重寫「護城河與競爭」；改 article.md 與 machine.json 的 moat（備份 *.pre_moat）。"""
    art_path, mj = run.dir / "article.md", run.dir / "machine.json"
    article = art_path.read_text(encoding="utf-8")
    mach = json.loads(mj.read_text(encoding="utf-8"))
    old = old_chapter(article)
    r = ensure_long(run)
    if from_raw:
        raw = json.loads((run.dir / "raw_moat_judge.json").read_text(encoding="utf-8"))
        text = raw.get("stitched_text") or (raw.get("result_event") or {}).get("result") or ""
    else:
        F = get_facts(run, r)
        run.guard()
        res, t0 = _spawn(run.dir, "moat_judge", judge_prompt(run.dir, run.t, old.group(0).strip(), r, F), False, 1, "low")
        c = run.record("moat_judge", "moat_judge", "opus", res, t0)
        run.save()
        print("[moat_judge] opus ok={0} ${1} {2}s out_tok={3}".format(res.get("ok"), c["cost_usd"], c["duration_s"], c["output_tokens"]))
        text = res.get("result_text") or ""
    obj = _json_block(text)
    m = re.search(r"^## 護城河與競爭", text, re.M)
    if not m:
        raise SystemExit("輸出沒有「## 護城河與競爭」；文章沒改：" + text[:300])
    chapter = text[m.start():]
    chapter = re.split(r"(?m)^```json", chapter)[0]
    chapter = re.split(r"(?m)^## (?!護城河與競爭)", chapter)[0].strip()
    mo = (obj or {}).get("moat")
    if not (isinstance(mo, dict) and mo.get("width") in ("寬", "窄", "無")):
        raise SystemExit("機器欄位 moat 沒解析到或缺 width；文章沒改。可用 --from-raw 重取")
    (run.dir / "article.md.pre_moat").write_text(article, encoding="utf-8")
    (run.dir / "machine.json.pre_moat").write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")
    art_path.write_text(article[:old.start()] + chapter + "\n\n" + article[old.end():], encoding="utf-8")
    if r:
        mo["roic_10y"] = {"avg_2016_2025": r["R1_roic"]["avg_2016_2025"], "min_2016_2025": r["R1_roic"]["min_2016_2025"], "source": r["source"]}
    mo["rule"] = "競爭結構版 2026-11-27"
    mach["moat"] = mo
    mj.write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")
    print("{0}：護城河 {1}／證據{2}／{3}（{4}）".format(run.t, mo.get("width"), mo.get("strength"), mo.get("trend"), mo.get("width_basis", "")[:60]))
    return mo
