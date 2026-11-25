#!/usr/bin/env python3
"""dd5 管線：pack → ask(opus) → lookups(sonnet 平行) → write(opus) → render → critic(sonnet) → fix(opus，最多一次) → render
→ lint(零 LLM) → recheck(sonnet 再冷讀) → fix2(opus，有紅燈或 lint block 才跑) → render → lint → gate(零 LLM，判定能否發布)。

用法：python3 scripts/dd5/run.py TICKER --date YYYYMMDD [--steps ask,lookups,write,render,critic,fix,render,lint,recheck,fix2,render,lint,gate]
累計花費（~/dd5-pilot/runs/*/manifest.json 全部加總）超過 HARD_STOP 就不再呼叫 LLM。
"""
from __future__ import annotations

import argparse
import concurrent.futures
import copy
import datetime as dt
import glob
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
for p in (str(SCRIPTS), str(SCRIPTS / "dd2"), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import spawn as sp  # noqa: E402  (scripts/dd2/spawn.py)
import render as rd  # noqa: E402

PILOT = Path.home() / "dd5-pilot"
CARDS = HERE / "cards"
HARD_STOP = 20.0
import os
THINK_CAP = int(os.environ.get("DD5_THINK_CAP", "32000"))  # opus 思考 token 上限（第一通 TXN ask 沒設，花 3.9 美元、思考約 13 萬 token）
SKILL = Path.home() / ".claude/skills/zh-analyst-prose/SKILL.md"


EFFORT = {"ask": "medium", "write": "medium", "fix": "low", "fix2": "low", "lintfix": "low", "base": "medium", "critic": None, "recheck": "medium", "judge": "medium", "patch_brief": "low", "prose": "low", "peers_pick": None}
TIMEOUT = {"ask": 300, "write": int(os.environ.get("DD5_WRITE_TIMEOUT", "600")), "fix": 300, "critic": 480, "recheck": 480, "fix2": 300, "lintfix": 300, "base": 300, "judge": 420, "patch_brief": 300, "prose": 420, "critic_brief": 300, "peers_pick": 120}  # 牆鐘上限（秒），超過殺掉改 --effort low 重試一次


def spawn_effort(prompt_path, model, out_json, cwd, effort):
    """dd5 自己包一層：不改 scripts/dd2/spawn.py，用 CLI --effort 控制思考量。"""
    import dd_headless
    extra = ["--effort", effort] if effort else None
    r = dd_headless.spawn(prompt_path=prompt_path, model=model, allowed_tools=None, max_turns=1, out_json=out_json,
                          cwd=cwd, extra_args=extra)
    return sp._augment_with_raw_usage(r, out_json)


def total_spent():
    t = 0.0
    for f in glob.glob(str(PILOT / "runs/*/manifest.json")):
        try:
            for c in json.loads(Path(f).read_text(encoding="utf-8")).get("calls", []):
                t += c.get("cost_usd") or 0
        except Exception:
            pass
    return t


class Run:
    def __init__(self, ticker, date):
        self.t, self.date = ticker, date
        self.dir = PILOT / "runs" / "{0}_{1}".format(ticker, date)
        self.mf_path = self.dir / "manifest.json"
        self.mf = json.loads(self.mf_path.read_text(encoding="utf-8")) if self.mf_path.exists() else {"ticker": ticker, "date": date, "calls": []}
        self.pack_md = (self.dir / "pack.md").read_text(encoding="utf-8")

    def save(self):
        self.mf["total_cost_usd"] = round(sum(c.get("cost_usd") or 0 for c in self.mf["calls"]), 4)
        self.mf_path.write_text(json.dumps(self.mf, ensure_ascii=False, indent=1), encoding="utf-8")

    def record(self, step, cid, model, r, t0, note=""):
        u = sum((v.get("inputTokens") or 0) for v in (r.get("by_model") or {}).values())
        c = {"step": step, "id": cid, "model": model, "ok": r.get("ok"), "cost_usd": r.get("cost_usd"),
             "input_tokens_uncached": u, "cache_read": r.get("cache_read"), "cache_creation": r.get("cache_creation"),
             "output_tokens": r.get("output_tokens"), "thinking_tokens": r.get("thinking_tokens"), "effort": r.get("effort"), "num_turns": r.get("num_turns"),
             "duration_s": round((r.get("duration_ms") or (time.time() - t0) * 1000) / 1000, 1), "at": dt.datetime.now().isoformat(timespec="seconds"), "note": note}
        self.mf["calls"].append(c)
        self.save()
        return c

    def guard(self):
        if os.environ.get("DD5_RUN_LIMIT"):  # 單檔上限模式：只算這一檔 manifest 的累計
            lim = float(os.environ["DD5_RUN_LIMIT"])
            s = sum(c.get("cost_usd") or 0 for c in self.mf["calls"])
            if s >= lim:
                raise SystemExit("本檔累計 {0:.2f} 美元已達上限 {1}，停止".format(s, lim))
            return
        s = total_spent()
        if s > HARD_STOP:
            raise SystemExit("累計花費 {0:.2f} 美元超過 {1} 美元，停止".format(s, HARD_STOP))

    def oneshot(self, step, model, prompt, out_name, cid=None):
        import llm
        self.guard()
        pp = self.dir / "prompt_{0}.md".format(out_name)
        pp.write_text(prompt, encoding="utf-8")
        t0 = time.time()
        eff = EFFORT.get(step) if model == "opus" else None

        def killed(info):
            c = {"step": step, "id": (cid or out_name) + "_killed", "model": model, "ok": False, "cost_usd": info["est_cost_usd"],
                 "cost_is_estimate": True, "effort": info["effort"], "duration_s": info["seconds"],
                 "at": dt.datetime.now().isoformat(timespec="seconds"), "note": "牆鐘超過 {0} 秒被殺，花費為估算".format(info["timeout_s"])}
            self.mf["calls"].append(c)
            self.save()
            print("[{0}] 超時被殺（{1} 秒），估算 ${2}".format(step, info["timeout_s"], info["est_cost_usd"]))
        r, kills = llm.call(str(pp), model, str(self.dir / "raw_{0}.json".format(out_name)), str(self.dir), eff,
                            TIMEOUT.get(step, 300), on_timeout=killed)
        c = self.record(step, cid or out_name, model, r, t0, note="超時後改 low 重試" if kills else "")
        print("[{0}] {1} ok={2} ${3} {4}s out_tok={5} cache_read={6}".format(step, model, r.get("ok"), c["cost_usd"], c["duration_s"], c["output_tokens"], c["cache_read"]))
        return r


def need_text(r):
    txt = r.get("result_text")
    if not r.get("ok") or not txt:
        raise SystemExit("LLM 通失敗：" + json.dumps({k: r.get(k) for k in ("ok", "num_turns")}) + " " + str(txt)[:300])
    return txt


# ---------------------------------------------------------------- 各步
def step_ask(run, name="ask"):
    card = (CARDS / "ask_card.md").read_text(encoding="utf-8")
    prompt = run.pack_md + "\n\n---\n\n" + card
    r = run.oneshot("ask", "opus", prompt, name)
    obj, err = sp.strip_json(need_text(r))
    if err:
        raise SystemExit("ask JSON 解析失敗：" + err)
    (run.dir / (name + ".json")).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


LOOKUP_PROMPT = """你是查證員。公司：{t}（美股）。今天是 {today}。只回答下面這一個問題，用 WebSearch 與 WebFetch 查，最多 8 輪（搜尋加抓頁總共不超過 8 次工具呼叫，超過就用已有的證據回答，沒找到就 not_found）。

規則：
- 優先公司文件、監管文件、產業統計；媒體轉述其次。
- answer 不超過 400 字，每個數字都要有 quotes 裡的原文支撐。quotes 的 text 是原文片段（不是你的改寫），url 是真實開過的頁面，date 是該頁發布日期。
- 查到的頁面上若出現比問題更新、而且直接改變問題前提的公司公告（例如人事異動、調查結果、併購、重編、指引更新），要點開讀內文，把日期與重點寫進 answer，不能只報標題。
- 找不到就 not_found 設 true，answer 寫「沒找到」與你查了什麼，不要編、不要用記憶補。
- 資料日期要標清楚；超過一年的資料要在 answer 裡說明。

問題編號：{id}
問題：{q}
這題服務的子題：{for_q}
建議來源：{src}

只輸出一個 JSON 物件，前後不要其他文字：
{{"id": "{id}", "answer": "...", "quotes": [{{"text": "...", "url": "...", "date": "YYYY-MM-DD"}}], "confidence": "高|中|低", "not_found": false}}
"""


def step_lookups(run):
    ask = json.loads((run.dir / "ask.json").read_text(encoding="utf-8"))
    items = ask.get("lookups") or []
    run.guard()

    def one(it):
        pp = run.dir / "prompt_lookup_{0}.md".format(it["id"])
        pp.write_text(LOOKUP_PROMPT.format(t=run.t, today=dt.date.today().isoformat(), id=it["id"], q=it.get("question", ""),
                                            for_q=it.get("for", ""), src=it.get("preferred_source", "")), encoding="utf-8")
        t0 = time.time()
        # 工作目錄改到家目錄以外的空資料夾（理由見 llm._once）；--setting-sources project 蓋掉 dd_headless 的 user
        # （後出現的同名旗標生效，做法同 llm._once）。路徑一律絕對，換 cwd 後才不會找不到。
        import dd_headless
        import llm
        llm.NEUTRAL_CWD.mkdir(parents=True, exist_ok=True)
        out_json = str((run.dir / "raw_lookup_{0}.json".format(it["id"])).resolve())
        r = dd_headless.spawn(prompt_path=str(pp.resolve()), model="sonnet", allowed_tools=["WebSearch", "WebFetch"], max_turns=8,
                              out_json=out_json, cwd=llm.NEUTRAL_CWD, extra_args=["--setting-sources", "project"])
        r = sp._augment_with_raw_usage(r, out_json)
        return it, r, t0

    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for it, r, t0 in [f.result() for f in [ex.submit(one, i) for i in items]]:
            c = run.record("lookup", it["id"], "sonnet", r, t0)
            obj, err = sp.strip_json(r.get("result_text") or "")
            if err or not isinstance(obj, dict):
                obj = {"id": it["id"], "answer": "（查證通沒有回出可解析的 JSON：{0}）".format(err), "quotes": [], "confidence": "低", "not_found": True}
            obj["id"] = it["id"]
            obj["question"] = it.get("question", "")
            res.append(obj)
            print("[lookup] {0} ok={1} ${2} {3}s turns={4} not_found={5}".format(it["id"], r.get("ok"), c["cost_usd"], c["duration_s"], c["num_turns"], obj.get("not_found")))
    (run.dir / "lookups.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


def step_compute(run):
    sys.path.insert(0, str(Path.home() / "v7-backtest"))
    from src.price_store import get_prices
    import pandas as pd
    ask = json.loads((run.dir / "ask.json").read_text(encoding="utf-8"))
    out = []
    for c in ask.get("compute") or []:
        tk = list(dict.fromkeys([run.t] + [str(x).upper() for x in c.get("tickers", [])]))
        rows = []
        try:
            cl = get_prices(tk, start=str(pd.Timestamp(c["from"]) - pd.Timedelta(days=7)), end=c["to"], field="close")
            ad = get_prices(tk, start=str(pd.Timestamp(c["from"]) - pd.Timedelta(days=7)), end=c["to"], field="adj_close")
        except Exception as e:
            cl = ad = None
            rows = [{"ticker": t, "error": str(e)[:100], "price_chg_pct": None, "total_ret_pct": None} for t in tk]
        if cl is not None:
            for t in tk:
                s0 = cl[t].dropna()
                a0 = ad[t].dropna()
                s0f = s0[s0.index >= pd.Timestamp(c["from"])]
                if s0f.empty:
                    rows.append({"ticker": t, "error": "無資料", "price_chg_pct": None, "total_ret_pct": None})
                    continue
                d0, d1 = s0f.index[0], s0f.index[-1]
                rows.append({"ticker": t, "start_date": str(d0.date()), "start_px": round(float(s0f.iloc[0]), 2), "end_date": str(d1.date()),
                             "end_px": round(float(s0f.iloc[-1]), 2), "price_chg_pct": round((float(s0f.iloc[-1]) / float(s0f.iloc[0]) - 1) * 100, 1),
                             "total_ret_pct": round((float(a0.loc[d1]) / float(a0.loc[d0]) - 1) * 100, 1)})
        out.append({"id": c["id"], "from": c["from"], "to": c["to"], "why": c.get("why", ""), "rows": rows})
    (run.dir / "compute.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[compute]", len(out), "組")


BASE_PROMPT = """

---

# 補寫任務：公司底稿

上面是資料包。再下面是你（同一位作者）已經寫好的正文，它缺「公司底稿」這一節。請只補這一節，其他都不要動，不要重寫正文。

規則（來自寫作卡）：
{rule}

格式：
- 輸出 Markdown，第一行 `## 公司底稿`，用 `###` 分三小節：生意怎麼賺錢、護城河、成長跑道。文字規則同正文（白話、全形標點、數字帶 [p:標籤] 或 [l:編號] 出處、一段一件事、不用比喻）。
- 只能用資料包與正文已有的查證數字，不要補新數字、不要上網。
- 最後輸出 json 區塊，只有 moat 欄位：
```json
{{"moat": {{"source": "一句話", "trend": "變強|持平|變弱", "evidence": "一句話帶數字"}}}}
```
- 如果你的護城河判斷跟正文估值節給的倍數理由不一致，不要改正文，在 json 區塊多放一個 "conflict" 欄位，用一兩句講清楚哪裡不一致；一致就不要放。

# 現有正文（article.md）

{article}
"""


def step_base(run):
    card = (CARDS / "write_card.md").read_text(encoding="utf-8")
    a = card.index("- 結論之後、子題之前，寫「公司底稿」")
    b = card.index("- 中間照子題一節一節寫")
    rule = card[a:b].strip()
    art = (run.dir / "article.md").read_text(encoding="utf-8")
    prompt = run.pack_md + BASE_PROMPT.format(rule=rule, article=art)
    r = run.oneshot("base", "opus", prompt, "base")
    text = need_text(r)
    body, obj, err = extract_machine(text)
    if obj is None:
        raise SystemExit("base JSON 解析失敗：" + str(err))
    (run.dir / "base.md").write_text(body.strip() + "\n", encoding="utf-8")
    mach = json.loads((run.dir / "machine.json").read_text(encoding="utf-8"))
    mach["moat"] = obj.get("moat")
    if obj.get("conflict"):
        mach["moat_conflict_note"] = obj["conflict"]
    (run.dir / "machine.json").write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")


def pick_peers(run, pe, n=5):
    """沒有人工名單時：先請 haiku 點名、程式驗代號；驗過不足 3 家用 auto_peers 補，點名失敗整個退回 auto_peers。
    回傳 (名單, 寫進 gaps 的說明)。點名結果與驗證紀錄存 run 目錄的 peers_pick.json。"""
    rec = {"ticker": run.t, "picks": [], "verify": []}
    good = []
    try:
        r = run.oneshot("peers_pick", "haiku", pe.pick_prompt(run.t), "peers_pick")
        obj, err = sp.strip_json(r.get("result_text") or "") if r.get("ok") else (None, "呼叫失敗")
        picks = obj.get("peers") if isinstance(obj, dict) else None
        if err or not isinstance(picks, list) or not picks:
            raise ValueError(err or "沒有 peers 清單")
        rec["picks"] = [x for x in picks if isinstance(x, dict)]
        good, rec["verify"] = pe.verify_picks(run.t, rec["picks"], n)
    except Exception as e:  # 含超時；LLM 失敗不擋流程，退回 auto_peers
        rec["error"] = str(e)[:200]
    notes = []
    if good:
        notes.append("同業名單由模型點名、程式驗過代號（yfinance 查得到且有年度營收）；模型點名 {0} 家、驗過 {1} 家，未經人看過".format(len(rec["picks"]), len(good)))
    if len(good) < 3:
        auto, auto_notes = pe.auto_peers(run.t, n=n)
        fill = [x for x in auto if x not in good][:n - len(good)]
        if good:
            notes.append("模型點名驗過只有 {0} 家，另有 {1} 家由程式自動補（yfinance 同產業、市值相近，產業分類很粗）".format(len(good), len(fill)))
        else:
            notes += ["模型點名失敗或全數驗證不過（{0}），整份名單退回程式自動產生".format(rec.get("error") or "驗證全丟")]
            good = []
        notes += auto_notes if not good or not fill else []
        good = good + fill
        rec["auto_filled"] = fill
    rec["final"] = good
    (run.dir / "peers_pick.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[peers] 點名後同業：", good, "（丟掉：{0}）".format([v["code"] for v in rec["verify"] if not v["kept"]]))
    return good, notes


def step_peers(run, override=None):
    import peers as pe
    ap_ = run.dir / "ask.json"
    ask = json.loads(ap_.read_text(encoding="utf-8")) if ap_.exists() else {}
    plist = override or ask.get("peers") or []  # 優先順序：--peers、ask.json 的人工名單、程式自動產生
    auto_notes = []
    if not plist:
        plist, auto_notes = pick_peers(run, pe)
    md, data, gaps = pe.build(run.t, plist, extra_gaps=auto_notes)
    (run.dir / "peers.md").write_text(md, encoding="utf-8")
    (run.dir / "peers.json").write_text(json.dumps({"data": data, "gaps": gaps}, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    pj = json.loads((run.dir / "pack.json").read_text(encoding="utf-8"))
    pj["tags"]["peers"] = {"title": "同業對照表（程式用 yfinance 自算）", "source": "yfinance", "url": "", "asof": run.date}
    pj.setdefault("gaps", [])
    for g in gaps:
        if g not in pj["gaps"]:
            pj["gaps"].append(g)
    (run.dir / "pack.json").write_text(json.dumps(pj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("[peers]", len(data), "家；缺口", gaps)


def extract_machine(text):
    ms = list(re.finditer(r"```json\s*\n(.*?)\n```", text, re.S))
    if not ms:
        return text, None, "沒有 json 區塊"
    m = ms[-1]
    obj, err = sp.strip_json(m.group(1))
    return text[:m.start()].rstrip() + "\n", obj, err


WRITE_FOOT = """

---

# 補充說明（給寫的人）

- 今天是 {today}。資料包裡的現價是 {pxd} 收盤價。
- 查證答案的引用標記用 `[l:編號]`，編號就是上面查證結果裡的 id（例如 `[l:l1]`）。資料包用 `[p:標籤]`，標籤見資料包各段標題。
- 一個標記一個方括號，多個來源就連寫多個，例如 `[p:price][l:l2]`。
- 請直接輸出正文與結尾的 json 區塊，不要在前面加說明。
"""


def step_write(run, fix_note=None):
    card = (CARDS / "write_card.md").read_text(encoding="utf-8")
    prose = ""
    if SKILL.exists() and SKILL.stat().st_size <= 8192:
        prose = "\n\n---\n\n# 附：中文文字規範（zh-analyst-prose）\n\n" + SKILL.read_text(encoding="utf-8")
        run.mf["prose_skill_attached"] = True
    else:
        run.mf["prose_skill_attached"] = False
        run.mf["prose_skill_bytes"] = SKILL.stat().st_size if SKILL.exists() else None
    ask = (run.dir / "ask.json").read_text(encoding="utf-8")
    lk = (run.dir / "lookups.json").read_text(encoding="utf-8") if (run.dir / "lookups.json").exists() else "[]"
    pack = json.loads((run.dir / "pack.json").read_text(encoding="utf-8"))
    cm_txt = ""
    if (run.dir / "peers.md").exists():
        cm_txt += "\n\n# 同業對照（程式算好；引用標記 `[p:peers]`）\n\n" + (run.dir / "peers.md").read_text(encoding="utf-8")
    if (run.dir / "compute.json").exists():
        cm_txt += "\n\n# 程式算好的比較（compute.json；引用標記 `[c:編號]`）\n\n```json\n" + (run.dir / "compute.json").read_text(encoding="utf-8") + "\n```"
    prompt = (run.pack_md + "\n\n---\n\n" + card + prose + "\n\n---\n\n# 你上一通定的題目（ask.json）\n\n```json\n" + ask + "\n```\n\n# 查證結果（lookups.json）\n\n```json\n" + lk + "\n```" + cm_txt
              + WRITE_FOOT.format(today=dt.date.today().isoformat(), pxd=pack.get("price_chart", {}).get("last_date")))
    r = run.oneshot("write", "opus", prompt, "write")
    text = need_text(r)
    (run.dir / "write_raw.md").write_text(text, encoding="utf-8")
    art, machine, err = extract_machine(text)
    if machine is None:
        raise SystemExit("write 機器欄位解析失敗：" + str(err))
    (run.dir / "article.md").write_text(art, encoding="utf-8")
    (run.dir / "machine.json").write_text(json.dumps(machine, ensure_ascii=False, indent=1), encoding="utf-8")


CRITIC_PROMPT = """你是獨立的冷讀檢查員，沒有參與寫作。下面是一份個股研究正文（段落已加編號 P1、P2…）、機器欄位，以及資料包裡的財務摘要與上一份報告的結論。你看不到原始資料包的其他部分，不要要求更多資料，也不要自己上網。

只檢查四件事：
1. 結論跟正文證據一致嗎。
2. 最強的反方意見有沒有被正面回答（而不是只列風險清單）。
3. 有沒有把一次性、會消失或口徑不同的項目，當成經常性獲利。
4. 機器欄位（獲利三檔的數字與對應情況、追蹤條件、會讓結論翻面的事）跟正文講的一樣嗎。這份報告刻意不給情境機率、目標價、合理倍數、觀望或進場的裁決，沒有這些不算問題，不要因此亮燈；正文若出現這些，反而要亮黃燈。

燈號：紅＝會讓讀者做出錯誤判斷、必須修；黃＝該改但不致誤導；綠＝沒問題。每件事至少一筆，有多個問題可多筆。where 填段落編號（如 "P7"，多段用逗號）或 "machine"。reason 要具體，指出哪句話、哪個數字，一到三句。
只輸出 JSON 陣列，前後不要其他文字：
[{{"item": "1 結論與證據|2 反方|3 一次性|4 情境一致", "light": "紅|黃|綠", "where": "P7", "reason": "..."}}]

# 正文

{article}

# 機器欄位

```json
{machine}
```

# 資料包摘錄（財務摘要與上一份結論）

{pack}
"""


def lite_prompt(run, pack):
    """組精簡版提示詞（不呼叫 LLM）：資料包＋同業對照＋規則卡＋日期；規則卡後附低品質來源網域（source_domains.json）。"""
    import domains
    card = (CARDS / "lite_card.md").read_text(encoding="utf-8")
    extra_txt = ""
    if (run.dir / "peers.md").exists():
        extra_txt += "\n\n# 同業對照（程式算好；引用標記 `[p:peers]`）\n\n" + (run.dir / "peers.md").read_text(encoding="utf-8")
    dom = domains.prompt_line()
    return (run.pack_md + extra_txt + "\n\n---\n\n" + card + ("\n\n" + dom if dom else "")
            + "\n\n---\n\n今天是 {0}。資料包裡的現價是 {1} 收盤價。".format(dt.date.today().isoformat(), pack.get("price_chart", {}).get("last_date")))


def step_lite(run):
    """精簡版：一通寫完，寫的人自己上網查（不經 ask、lookups、critic、fix）。"""
    import dd_headless
    import llm
    run.guard()
    pack = json.loads((run.dir / "pack.json").read_text(encoding="utf-8"))
    prompt = lite_prompt(run, pack)
    pp = run.dir / "prompt_lite.md"
    pp.write_text(prompt, encoding="utf-8")
    llm.NEUTRAL_CWD.mkdir(parents=True, exist_ok=True)
    out_json = str((run.dir / "raw_lite.json").resolve())
    t0 = time.time()
    r = dd_headless.spawn(prompt_path=str(pp.resolve()), model="opus", allowed_tools=["WebSearch", "WebFetch"], max_turns=16,
                          out_json=out_json, cwd=llm.NEUTRAL_CWD,
                          extra_args=["--setting-sources", "project", "--effort", "medium",
                                      "--max-budget-usd", os.environ.get("DD5_LITE_BUDGET", "4")])
    r = sp._augment_with_raw_usage(r, out_json)
    c = run.record("lite", "lite", "opus", r, t0)
    run.save()
    print("[lite] opus ok={0} ${1} {2}s turns={3} out_tok={4}".format(r.get("ok"), c["cost_usd"], c["duration_s"], c["num_turns"], c["output_tokens"]))
    text = need_text(r)
    (run.dir / "write_raw.md").write_text(text, encoding="utf-8")
    art, machine, err = extract_machine(text)
    if machine is None:
        raise SystemExit("lite 機器欄位解析失敗：" + str(err))
    m = re.search(r"^# ", art, flags=re.M)  # 帶工具的呼叫常在正文前多寫一句開場白，標題之前的一律丟掉
    if m:
        art = art[m.start():]
    (run.dir / "article.md").write_text(art, encoding="utf-8")
    (run.dir / "machine.json").write_text(json.dumps(machine, ensure_ascii=False, indent=1), encoding="utf-8")


def numbered(article):
    paras = re.split(r"\n\s*\n", article.strip())
    return paras, "\n\n".join("[P{0}] {1}".format(i + 1, p) for i, p in enumerate(paras))


def pack_summary(pack_md):
    keep = ("prior", "price", "consensus", "capital", "val_hist", "fin_annual", "fin_quarter", "routine_fin")
    parts = re.split(r"(?m)^(?=## \[p:)", pack_md)
    return "\n".join(p for p in parts if any(p.startswith("## [p:{0}]".format(k)) for k in keep))


def step_critic(run):
    art = (run.dir / "article.md").read_text(encoding="utf-8")
    _, num = numbered(art)
    prompt = CRITIC_PROMPT.format(article=num, machine=(run.dir / "machine.json").read_text(encoding="utf-8"), pack=pack_summary(run.pack_md))
    r = run.oneshot("critic", "sonnet", prompt, "critic")
    obj, err = sp.strip_json(need_text(r))
    if err or not isinstance(obj, list):
        raise SystemExit("critic JSON 解析失敗：" + str(err))
    (run.dir / "critic.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    cnt = {k: sum(1 for x in obj if x.get("light") == k) for k in ("紅", "黃", "綠")}
    print("[critic]", cnt)
    return cnt


FIX_PROMPT = """你是這份個股研究的作者，有人冷讀後給了紅燈與黃燈（非綠燈項）。請針對下面列的每一項修補，其他一律不動。

規則：
- 只輸出要替換的段落。每個替換段要完整重寫該段（可以拆成多段，用空行分開），沿用原本的標記格式（[p:標籤]、[l:編號]）與文字規則（白話、全形標點、數字帶出處、一段一件事）。
- 如果問題是「機器欄位跟正文不一致」，判斷哪一邊對，改錯的那一邊：改正文就替換段落，改機器欄位就在 machine_patch 裡只放要改的欄位（巢狀欄位照原結構）。
- 問題若涉及全文多處同一個口徑，每一處都要改到同口徑；改完如果獲利檔位、結論或「現價預設了什麼」的推理因此站不住，照實改機器欄位（machine_patch）與相關段落，不要為了保住原結論硬撐。
- 這份報告刻意不給情境機率、目標價、加權報酬、合理倍數，修補時不要加進正文或機器欄位。
- 段落編號（P7 這種）只是給你對位置用的，正文裡不能出現；要指向別處就寫節的名稱。
- 論點或數字改了之後，下面附的各節標題與開頭結論段若還在講舊的說法，一併替換到一致（標題也用 replacements 換）。
- machine_patch 裡的陣列欄位（追蹤條件、獲利三檔等）會整個取代原本的陣列：要改其中一筆，就給完整陣列，沒被點名的項目原樣保留。
- 修補以改寫原段為主，不要為了回應一條意見新增整段；改完的篇幅不要明顯變長。
- 不能補進資料包與查證結果之外的新數字。拿不到證據的地方，改寫成「這裡缺什麼、會怎麼影響判斷」的一句話。
只輸出 JSON，前後不要其他文字：
{{"replacements": [{{"para": "P7", "text": "新的段落內容（Markdown）"}}], "machine_patch": {{}}}}

# 非綠燈項（紅與黃）

{reds}

# 相關段落

{paras}

# 目前的機器欄位

```json
{machine}
```

# 可引用的資料：查證結果

```json
{lookups}
```

# 資料包摘錄

{pack}
"""


def step_fix(run):
    crit = json.loads((run.dir / "critic.json").read_text(encoding="utf-8"))
    reds = [x for x in crit if x.get("light") in ("紅", "黃")]
    if not reds:
        print("[fix] 沒有紅燈或黃燈，略過")
        return False
    return _apply_fix(run, reds, "fix", "")


def _apply_fix(run, reds, step, tag, prompt_tpl=None, drop_empty=False):
    """fix 與 fix2 共用：照 reds 呼叫一次 opus、套用替換與 machine_patch。
    tag 是備份檔名尾碼（fix 為空字串，維持原檔名 article_before_fix.md 等）。"""
    art = (run.dir / "article.md").read_text(encoding="utf-8")
    paras, _ = numbered(art)
    want = set()
    for x in reds:
        for m in re.findall(r"P(\d+)", str(x.get("where", ""))):
            want.add(int(m))
    for i, p in enumerate(paras, 1):  # 紅燈若是口徑問題，同一個數字會出現在很多段：把含該數字的段落全部帶上
        if re.search(os.environ.get("DD5_FIX_GREP", r"$^"), p):
            want.add(i)
    seen_h2 = 0
    for i, p in enumerate(paras, 1):  # 標題與開頭結論段一律帶上：論點改了，標題與結論才能同步
        if p.lstrip().startswith("#"):
            want.add(i)
            if p.lstrip().startswith("## "):
                seen_h2 += 1
        elif seen_h2 <= 1:
            want.add(i)
    ctx = "\n\n".join("[P{0}] {1}".format(i, paras[i - 1]) for i in sorted(want) if 1 <= i <= len(paras)) or "（紅燈沒有指到具體段落，請從機器欄位或整體處理）"
    prompt = (prompt_tpl or FIX_PROMPT).format(reds=json.dumps(reds, ensure_ascii=False, indent=1), paras=ctx,
                               machine=(run.dir / "machine.json").read_text(encoding="utf-8"),
                               lookups=(run.dir / "lookups.json").read_text(encoding="utf-8"), pack=pack_summary(run.pack_md))
    r = run.oneshot(step, "opus", prompt, step)
    obj, err = sp.strip_json(need_text(r))
    if err or not isinstance(obj, dict):
        raise SystemExit("{0} JSON 解析失敗：".format(step) + str(err))
    (run.dir / "article_before_fix{0}.md".format(tag)).write_text(art, encoding="utf-8")
    if not tag:
        (run.dir / "article_prefix.md").write_text(art, encoding="utf-8")
    for rep in obj.get("replacements", []):
        m = re.match(r"P(\d+)", str(rep.get("para", "")))
        if m and 1 <= int(m.group(1)) <= len(paras):
            paras[int(m.group(1)) - 1] = rep.get("text", "").strip()
    if drop_empty:  # fix2 允許用空字串刪掉整段（例如文末重複的一節）
        paras = [x for x in paras if x.strip()]
    (run.dir / "article.md").write_text("\n\n".join(paras) + "\n", encoding="utf-8")
    mp = obj.get("machine_patch") or {}
    if mp:
        mach = json.loads((run.dir / "machine.json").read_text(encoding="utf-8"))
        (run.dir / "machine_before_fix{0}.json".format(tag)).write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")

        def merge(a, b):
            for k, v in b.items():
                if isinstance(v, dict) and isinstance(a.get(k), dict):
                    merge(a[k], v)
                else:
                    a[k] = v
        merge(mach, mp)
        (run.dir / "machine.json").write_text(json.dumps(mach, ensure_ascii=False, indent=1), encoding="utf-8")
    return True


# ---------------------------------------------------------------- 發布前品質關卡：lint → recheck → fix2 → gate
def step_lint(run):
    import lint
    out = lint.lint_run(run.dir)
    nb = sum(1 for h in out["hits"] if h["severity"] == "block")
    print("[lint] ok={0} block={1} warn={2}".format(out["ok"], nb, len(out["hits"]) - nb))
    for h in out["hits"]:
        print("  [{0}] {1} L{2}: {3}".format(h["severity"], h["rule"], h["line"], h["text"]))
    return out


def step_recheck(run):
    """修補後再冷讀一次：同 step_critic 的 prompt 與呼叫方式（sonnet），輸出 critic2.json、raw_recheck.json。"""
    art = (run.dir / "article.md").read_text(encoding="utf-8")
    _, num = numbered(art)
    prompt = CRITIC_PROMPT.format(article=num, machine=(run.dir / "machine.json").read_text(encoding="utf-8"), pack=pack_summary(run.pack_md))
    r = run.oneshot("recheck", "sonnet", prompt, "recheck")
    obj, err = sp.strip_json(need_text(r))
    if err or not isinstance(obj, list):
        raise SystemExit("recheck JSON 解析失敗：" + str(err))
    (run.dir / "critic2.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    cnt = {k: sum(1 for x in obj if x.get("light") == k) for k in ("紅", "黃", "綠")}
    print("[recheck]", cnt)
    return cnt


def step_gate(run):
    """零 LLM：讀 lint.json 與 critic2.json（沒有就退回 critic.json），紅燈 0 且 lint block 0 才 PASS。"""
    lint_p = run.dir / "lint.json"
    if not lint_p.exists():
        raise SystemExit("gate 需要 lint.json，請先跑 lint 步驟")
    lint_o = json.loads(lint_p.read_text(encoding="utf-8"))
    reasons = []
    if (run.dir / "critic2.json").exists():
        crit, src = json.loads((run.dir / "critic2.json").read_text(encoding="utf-8")), "critic2.json"
    elif (run.dir / "critic.json").exists():
        crit, src = json.loads((run.dir / "critic.json").read_text(encoding="utf-8")), "critic.json"
        reasons.append("修補後未再冷讀（燈號來自 critic.json）")
    else:
        raise SystemExit("gate 需要 critic2.json 或 critic.json")
    red = sum(1 for x in crit if x.get("light") == "紅")
    yellow = sum(1 for x in crit if x.get("light") == "黃")
    lb = sum(1 for h in lint_o.get("hits", []) if h.get("severity") == "block")
    lw = sum(1 for h in lint_o.get("hits", []) if h.get("severity") == "warn")
    if red:
        reasons.append("冷讀仍有 {0} 個紅燈（{1}）".format(red, src))
    if lb:
        reasons.append("lint 有 {0} 筆 block：{1}".format(lb, "、".join(sorted({h["rule"] for h in lint_o["hits"] if h.get("severity") == "block"}))))
    ok = red == 0 and lb == 0
    out = {"pass": ok, "reasons": reasons, "red": red, "yellow": yellow, "lint_block": lb, "lint_warn": lw, "critic_source": src}
    (run.dir / "gate.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    run.mf["gate"] = {"pass": ok, "reasons": reasons}
    run.save()
    print("[gate] PASS" if ok else "[gate] FAIL: " + "；".join(reasons))
    return out


FIX2_EXTRA = """- 有些項目是機械檢查抓到的格式問題（內部用語、內部段落編號、重複的節）：照項目說明改，改成讀者看得懂的白話，不要新增內容。
- 項目要求「刪掉」某段時，那一段的 text 給空字串 ""。
"""

LINT_REASON = {
    "internal_para_no": "正文出現內部段落編號「{t}」，改成指向節的名稱，或直接拿掉這個指向",
    "internal_term": "正文出現內部用語「{t}」，改寫成讀者看得懂的說法（例如改成公開資料沒有、這份報告沒有，不要提資料包、底稿這類製作過程）",
    "forbidden_content": "正文出現這份報告刻意不給的內容（{t}），刪掉或改寫成不給裁決的說法",
    "fake_tool_call": "正文夾帶工具呼叫殘留字串，整段重寫成正常文字",
    "title_missing": "第一行必須是「# 標題」，補上以問句為題的標題",
}


def _lint_reds(art, hits):
    """把 lint 的 block hits 轉成給 fix 的紅燈項目；回傳 (項目 list, 只能用程式處理不必叫 LLM 的規則 set)。"""
    spans, pos = [], 0
    for m in re.finditer(r"\n\s*\n", art.strip()):
        spans.append((pos, m.start()))
        pos = m.end()
    spans.append((pos, len(art.strip())))
    body = art.strip()

    def para_of_line(ln):  # lint 的行號對的是原檔；用去頭尾空白後的字元位置換算段號
        off = len(art) - len(art.lstrip())
        char = sum(len(x) + 1 for x in art.split("\n")[:ln - 1]) - off
        for i, (a, b) in enumerate(spans, 1):
            if a <= max(char, 0) <= b:
                return i
        return len(spans)
    items, seen = [], set()
    for h in hits:
        if h.get("severity") != "block" or h["rule"] == "blank_run":
            continue
        if h["rule"] == "duplicate_h2":
            name = re.match(r"「## (.+?)」", h["text"]).group(1)
            first = [i for i, p in enumerate(re.split(r"\n\s*\n", body), 1) if p.lstrip().startswith("## " + name)]
            if len(first) < 2:
                continue
            paras = re.split(r"\n\s*\n", body)
            end = len(paras)
            for j in range(first[-1], len(paras)):
                if j > first[-1] - 1 and paras[j].lstrip().startswith("## "):
                    end = j
                    break
            where = ",".join("P{0}".format(i) for i in range(first[-1], end + 1))
            items.append({"item": "lint", "light": "紅", "where": where,
                          "reason": "文末重複的「{0}」一節刪掉（整節每一段的 text 都給空字串），內容已在開頭".format(name)})
            continue
        tpl = LINT_REASON.get(h["rule"], "機械檢查（{0}）未過：{{t}}".format(h["rule"]))
        pat = r"P\d{1,3}" if h["rule"] == "internal_para_no" else r"資料包|底稿|上一通|這一通|題目的前提|查證結果|規則卡|機器欄位|主軸沒有被|k\d+|machine"
        m = re.search(pat, h["text"]) if h["rule"] in ("internal_para_no", "internal_term") else None
        t = m.group(0) if m else h["text"]
        key = (para_of_line(h["line"]), h["rule"], t)
        if key in seen:
            continue
        seen.add(key)
        items.append({"item": "lint", "light": "紅", "where": "P{0}".format(key[0]), "reason": tpl.format(t=t) + "（原句：{0}）".format(h["text"])})
    return items


def step_fix2(run):
    """critic2 有紅燈或 lint 有 block 才叫一次 opus；兩者都乾淨就跳過、不花錢。blank_run 這類純排版問題不叫 LLM
    （fix 重寫時本來就會把段落用單一空行接回）。"""
    c2p, lp = run.dir / "critic2.json", run.dir / "lint.json"
    crit2 = json.loads(c2p.read_text(encoding="utf-8")) if c2p.exists() else []
    lint_o = json.loads(lp.read_text(encoding="utf-8")) if lp.exists() else {"hits": []}
    art = (run.dir / "article.md").read_text(encoding="utf-8")
    # 第二次冷讀的黃燈也一起修（2026-11-24 持有人同意）：修完不再讀第三次，gate 仍只看紅燈與 lint
    reds = [x for x in crit2 if x.get("light") in ("紅", "黃")] + _lint_reds(art, lint_o.get("hits", []))
    if not reds:
        blank = [h for h in lint_o.get("hits", []) if h["rule"] == "blank_run" and h["severity"] == "block"]
        if blank:
            (run.dir / "article_before_fix2.md").write_text(art, encoding="utf-8")
            (run.dir / "article.md").write_text(re.sub(r"\n\s*\n(?:\s*\n)+", "\n\n", art), encoding="utf-8")
            print("[fix2] 只有連續空行，已用程式整理，不叫 LLM")
            return True
        print("[fix2] critic2 沒有紅燈、lint 沒有 block，不需要，略過")
        return False
    tpl = FIX_PROMPT.replace("只輸出 JSON，前後不要其他文字：", FIX2_EXTRA + "只輸出 JSON，前後不要其他文字：")
    return _apply_fix(run, reds, "fix2", "2", prompt_tpl=tpl, drop_empty=True)


def step_lintfix(run):
    """最後一次 lint 還有 block 才叫一次 opus，只改被點到的那幾段；沒有就跳過、不花錢。
    修完由後面的 render,lint,gate 再判一次，仍不過就停下交人。"""
    lp = run.dir / "lint.json"
    lint_o = json.loads(lp.read_text(encoding="utf-8")) if lp.exists() else {"hits": []}
    art = (run.dir / "article.md").read_text(encoding="utf-8")
    reds = _lint_reds(art, lint_o.get("hits", []))
    if not reds:
        print("[lintfix] lint 沒有 block，不需要，略過")
        return False
    tpl = FIX_PROMPT.replace("只輸出 JSON，前後不要其他文字：", FIX2_EXTRA + "- 這一輪只處理列出的項目，其他段落一個字都不要動。\n只輸出 JSON，前後不要其他文字：")
    return _apply_fix(run, reds, "lintfix", "3", prompt_tpl=tpl, drop_empty=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--date", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--steps", default="ask,lookups,write,render,critic,fix,render")
    ap.add_argument("--peers", default=None, help="同業代號，逗號分隔；有給就蓋過 ask.json 與自動名單")
    a = ap.parse_args()
    run = Run(a.ticker.upper(), a.date)
    for s in a.steps.split(","):
        if s == "ask":
            step_ask(run)
        elif s == "ask_medium":
            step_ask(run, "ask_medium")
        elif s == "base":
            step_base(run)
        elif s == "peers":
            step_peers(run, override=[x.strip().upper() for x in a.peers.split(",") if x.strip()] if a.peers else None)
        elif s == "compute":
            step_compute(run)
        elif s == "lookups":
            step_lookups(run)
        elif s == "write":
            step_write(run)
        elif s == "critic":
            step_critic(run)
        elif s in ("judge", "critic_brief", "patch_brief", "prose"):
            import steps3
            getattr(steps3, "step_" + s)(run)
        elif s == "fix":
            if step_fix(run):
                run.mf["fixed_once"] = True
                run.save()
        elif s == "lint":
            step_lint(run)
        elif s == "lite":
            step_lite(run)
        elif s == "lintfix":
            step_lintfix(run)
        elif s == "recheck":
            step_recheck(run)
        elif s == "fix2":
            if step_fix2(run):
                run.mf["fixed_twice"] = True
                run.save()
        elif s == "gate":
            step_gate(run)
        elif s == "render":
            import render_pretty as rp  # noqa: E402  新版面
            print(json.dumps(rp.render(run.dir, out=a.out), ensure_ascii=False))
        run.save()
    print("本檔合計 ${0}；全部試跑累計 ${1:.2f}".format(run.mf.get("total_cost_usd"), total_spent()))


if __name__ == "__main__":
    main()
