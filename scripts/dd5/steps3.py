#!/usr/bin/env python3
"""dd5 兩通寫作：judge（判斷）→ critic_brief → patch_brief → prose（成文）。舊的 write／critic／fix 不動。
由 run.py 的 main 呼叫，函式吃 run.Run 物件。"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
from pathlib import Path

import llm

CARDS = Path(__file__).resolve().parent / "cards"
sp = llm.sp


def _need(r):
    txt = r.get("result_text")
    if not r.get("ok") or not txt:
        raise SystemExit("LLM 通失敗：" + str(txt)[:300])
    return txt


def _cap(run, step, model, prompt, name, default="32000"):
    """只對這一步設輸出上限（環境變數 DD5_MAX_OUTPUT_TOKENS 已設就以它為準）。"""
    prev = os.environ.get("DD5_MAX_OUTPUT_TOKENS")
    if prev is None:
        os.environ["DD5_MAX_OUTPUT_TOKENS"] = default
    try:
        return run.oneshot(step, model, prompt, name)
    finally:
        if prev is None:
            os.environ.pop("DD5_MAX_OUTPUT_TOKENS", None)


def pack_summary(pack_md):
    keep = ("prior", "price", "fx", "consensus", "capital", "val_hist", "fin_annual", "fin_quarter", "routine_fin")
    parts = re.split(r"(?m)^(?=## \[p:)", pack_md)
    return "\n".join(p for p in parts if any(p.startswith("## [p:{0}]".format(k)) for k in keep))


def hist_summary(run):
    import multiples as mp
    pack = json.loads((run.dir / "pack.json").read_text(encoding="utf-8"))
    mu = mp.build(run.t, price_override=pack.get("last_price"))
    L = ["各年度底「過去十二個月」倍數（程式算好，已換成股價幣別；引用標記 `[p:val_hist]`）："]
    for y in mu["years"]:
        L.append("- {0}：本益比 {1}、市銷率 {2}、EV／營收 {3}、股價／自由現金流 {4}".format(
            y["fy_end"], *["{0:.1f}".format(y[k]) if y.get(k) is not None else "—" for k in ("pe", "ps", "evs", "pfcf")]))
    n = mu.get("now") or {}
    L.append("- 現在（過去十二個月至 {0}）：本益比 {1}、市銷率 {2}、EV／營收 {3}、股價／自由現金流 {4}".format(
        n.get("ttm_end"), *["{0:.1f}".format(n[k]) if n.get(k) is not None else "—" for k in ("pe", "ps", "evs", "pfcf")]))
    for k, lab in (("pe", "本益比"), ("ps", "市銷率"), ("evs", "EV／營收"), ("pfcf", "股價／自由現金流")):
        s = mu["stats"].get(k)
        if s:
            L.append("- {0}：最低 {1:.1f}、中位 {2:.1f}、最高 {3:.1f}（{4} 個年度點）".format(lab, s["min"], s["med"], s["max"], s["n"]))
    return "\n".join(L)


JUDGE_FOOT = """

---

# 補充說明

- 今天是 {today}。資料包裡的現價是 {pxd} 收盤價。
- 查證答案的引用標記用 `[l:編號]`（例如 `[l:l1]`），資料包用 `[p:標籤]`，程式比較用 `[c:編號]`，同業表用 `[p:peers]`。一個標記一個方括號，多個來源連寫。
- 只輸出 JSON 物件，前後不要有其他文字。
"""


def step_judge(run):
    card = (CARDS / "judge_card.md").read_text(encoding="utf-8")
    ask = (run.dir / "ask.json").read_text(encoding="utf-8")
    lk = (run.dir / "lookups.json").read_text(encoding="utf-8") if (run.dir / "lookups.json").exists() else "[]"
    pack = json.loads((run.dir / "pack.json").read_text(encoding="utf-8"))
    cm = ""
    if (run.dir / "peers.md").exists():
        cm += "\n\n# 同業對照（程式算好；引用標記 `[p:peers]`）\n\n" + (run.dir / "peers.md").read_text(encoding="utf-8")
    if (run.dir / "compute.json").exists():
        cm += "\n\n# 程式算好的比較（compute.json；引用標記 `[c:編號]`）\n\n```json\n" + (run.dir / "compute.json").read_text(encoding="utf-8") + "\n```"
    cm += "\n\n# 歷史倍數\n\n" + hist_summary(run)
    prompt = (run.pack_md + "\n\n---\n\n" + card + "\n\n---\n\n# 你上一通定的題目（ask.json）\n\n```json\n" + ask + "\n```\n\n# 查證結果（lookups.json）\n\n```json\n" + lk + "\n```" + cm
              + JUDGE_FOOT.format(today=dt.date.today().isoformat(), pxd=pack.get("price_chart", {}).get("last_date")))
    r = _cap(run, "judge", "opus", prompt, "judge")
    text = _need(r)
    (run.dir / "judge_raw.md").write_text(text, encoding="utf-8")
    obj, err = sp.strip_json(text)
    if err or not isinstance(obj, dict) or "sections" not in obj:
        raise SystemExit("judge JSON 解析失敗（不重試）：" + str(err))
    (run.dir / "brief.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    if isinstance(obj.get("machine"), dict):
        (run.dir / "machine.json").write_text(json.dumps(obj["machine"], ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        raise SystemExit("judge 沒有 machine 欄位")
    print("[judge] brief.json {0} 字元、{1} 節、{2} 個算式".format(len(json.dumps(obj, ensure_ascii=False)), len(obj["sections"]), len(obj.get("calcs", []))))


CRITIC_BRIEF_PROMPT = """你是獨立的冷讀檢查員，沒有參與寫作。下面是一份個股研究的「底稿」（JSON：結論、算式 calcs、各節 sections、機器欄位 machine），之後會有人照底稿寫成文章。你還看得到資料包裡的財務摘要與上一份報告的結論。你看不到原始資料包的其他部分，不要要求更多資料，也不要自己上網。

只檢查五件事：
1. 結論跟各節證據一致嗎。
2. 最強的反方意見有沒有被正面回答（而不是只列風險清單）。
3. 有沒有把一次性、會消失或口徑不同的項目，當成經常性獲利。
4. 機器欄位（獲利三檔的數字與對應情況、追蹤條件、會讓結論翻面的事）跟各節講的一樣嗎。這份報告刻意不給情境機率、目標價、合理倍數、觀望或進場的裁決，沒有這些不算問題，不要因此亮燈；底稿若出現這些，反而要亮黃燈。
5. calcs 的每條算式自己重算一遍（輸入以算式內標的出處為準，可對照資料包摘錄），結果跟 result 對不上的亮紅燈，並在 reason 寫出你算的結果。

燈號：紅＝會讓讀者做出錯誤判斷、必須修；黃＝該改但不致誤導；綠＝沒問題。每件事至少一筆，有多個問題可多筆。where 填節的 id（如 "q2"、"valuation"、"conclusion"）、算式用 "calcs:k3"、機器欄位用 "machine"，多處用逗號。reason 要具體，指出哪句話、哪個數字，一到三句。
只輸出 JSON 陣列，前後不要其他文字：
[{{"item": "1 結論與證據|2 反方|3 一次性|4 情境一致|5 算式重算", "light": "紅|黃|綠", "where": "q2", "reason": "..."}}]

# 底稿

```json
{brief}
```

# 資料包摘錄（財務摘要與上一份結論）

{pack}
"""


def step_critic_brief(run):
    brief = (run.dir / "brief.json").read_text(encoding="utf-8")
    prompt = CRITIC_BRIEF_PROMPT.format(brief=brief, pack=pack_summary(run.pack_md))
    r = run.oneshot("critic_brief", "sonnet", prompt, "critic_brief")
    obj, err = sp.strip_json(_need(r))
    if err or not isinstance(obj, list):
        raise SystemExit("critic_brief JSON 解析失敗：" + str(err))
    (run.dir / "critic.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    cnt = {k: sum(1 for x in obj if x.get("light") == k) for k in ("紅", "黃", "綠")}
    print("[critic_brief]", cnt)
    return cnt


PATCH_PROMPT = """你是這份個股研究底稿的作者。有人冷讀後給了紅燈與黃燈（非綠燈項），請修補。

# 規矩

- 只改非綠燈項指到的地方，以及因此必須一起改的地方。改了一個數字或論點，所有引用它的節、conclusion、machine 都要一起改到一致（包含各節的「什麼情況下會改看法」門檻要跟 machine 的追蹤與翻面條件一致）。
- 不加情境機率、目標價、合理倍數、觀望或進場的裁決。
- 不補新數字：資料包摘錄、查證答案、算式輸入裡沒有的數字不能出現。新算式放進 calcs，寫出算式、輸入帶出處標記。
- 要改的節整節完整重寫（含 id、heading、answer、points、tables、change_my_mind、placeholders），不要只給片段。

# 輸出

只輸出 JSON 物件，前後不要其他文字，沒要改的欄位省略：
{{"sections": [完整的節物件，id 要與底稿相同],
  "calcs": [完整的算式物件，id 相同的取代、新 id 的新增],
  "conclusion": ["…"],
  "machine_patch": {{"欄位": "新值；陣列欄位（earnings_cases、tracking、change_my_mind、vs_prior）給完整陣列"}}}}

# 要處理的燈號

{lights}

# 現在的底稿（brief.json）

```json
{brief}
```

# 查證結果

```json
{lookups}
```

# 資料包摘錄

{pack}
"""


def step_patch_brief(run):
    crit = json.loads((run.dir / "critic.json").read_text(encoding="utf-8"))
    bad = [x for x in crit if x.get("light") in ("紅", "黃")]
    if not bad:
        print("[patch_brief] 沒有紅或黃，略過")
        return False
    brief_txt = (run.dir / "brief.json").read_text(encoding="utf-8")
    lk = (run.dir / "lookups.json").read_text(encoding="utf-8") if (run.dir / "lookups.json").exists() else "[]"
    prompt = PATCH_PROMPT.format(lights=json.dumps(bad, ensure_ascii=False, indent=1), brief=brief_txt, lookups=lk, pack=pack_summary(run.pack_md))
    r = run.oneshot("patch_brief", "opus", prompt, "patch_brief")
    obj, err = sp.strip_json(_need(r))
    if err or not isinstance(obj, dict):
        raise SystemExit("patch_brief JSON 解析失敗：" + str(err))
    brief = json.loads(brief_txt)
    (run.dir / "brief_before_patch.json").write_text(brief_txt, encoding="utf-8")
    changed = {"sections": [], "calcs": [], "conclusion": False, "machine": []}
    secs = brief["sections"]
    for s in obj.get("sections") or []:
        for i, o in enumerate(secs):
            if o.get("id") == s.get("id"):
                secs[i] = s
                break
        else:
            secs.append(s)
        changed["sections"].append(s.get("id"))
    calcs = brief.setdefault("calcs", [])
    for c in obj.get("calcs") or []:
        for i, o in enumerate(calcs):
            if o.get("id") == c.get("id"):
                calcs[i] = c
                break
        else:
            calcs.append(c)
        changed["calcs"].append(c.get("id"))
    if obj.get("conclusion"):
        brief["conclusion"] = obj["conclusion"]
        changed["conclusion"] = True
    mp_ = obj.get("machine_patch") or {}
    for k, v in mp_.items():
        brief.setdefault("machine", {})[k] = v
        changed["machine"].append(k)
    (run.dir / "brief.json").write_text(json.dumps(brief, ensure_ascii=False, indent=1), encoding="utf-8")
    (run.dir / "machine.json").write_text(json.dumps(brief["machine"], ensure_ascii=False, indent=1), encoding="utf-8")
    run.mf["patch_brief_changed"] = changed
    print("[patch_brief] 改動", json.dumps(changed, ensure_ascii=False))
    return True


PROSE_FOOT = """

---

# 補充說明

- 今天是 {today}。
- 下面「例行檢查有事的項目」要併進相關的節，用一兩句交代。
- 不要呼叫任何工具，不要載入或讀取任何 skill 或檔案，所需資料都在上面。只輸出文章 Markdown，第一行是 `# 標題`。
"""


def step_prose(run):
    card = (CARDS / "prose_card.md").read_text(encoding="utf-8")
    brief = json.loads((run.dir / "brief.json").read_text(encoding="utf-8"))
    brief_nm = {k: v for k, v in brief.items() if k != "machine"}
    ask = json.loads((run.dir / "ask.json").read_text(encoding="utf-8"))
    issues = [r for r in ask.get("routine", []) if not str(r.get("status", "")).startswith("無")]
    prompt = (card + "\n\n---\n\n# 底稿（brief）\n\n```json\n" + json.dumps(brief_nm, ensure_ascii=False, indent=1) + "\n```\n\n# 例行檢查有事的項目\n\n```json\n"
              + json.dumps(issues, ensure_ascii=False, indent=1) + "\n```" + PROSE_FOOT.format(today=dt.date.today().isoformat()))
    r = _cap(run, "prose", "opus", prompt, "prose")
    text = _need(r).strip()
    text = re.sub(r"^```(?:markdown|md)?\s*\n|\n```\s*$", "", text)
    (run.dir / "article_raw_prose.md").write_text(text, encoding="utf-8")
    m = re.search(r"(?m)^# [^\n]+$", text)  # 模型偶爾先吐一堆假的工具呼叫（想載入 skill），只留第一個 # 標題起的正文
    if m and m.start() > 0:
        print("[prose] 去掉標題前 {0} 字元的非正文（假工具呼叫）".format(m.start()))
        text = text[m.start():].strip()
    (run.dir / "article.md").write_text(text + "\n", encoding="utf-8")
    print("[prose] article.md {0} 字元".format(len(re.sub(r"\s+", "", text))))
