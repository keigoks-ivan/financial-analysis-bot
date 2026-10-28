---
name: picks-monthly
description: 「本站挑選」（/active-etf/ 與 /etf-dash/ 頁面最上面那一區）的每月月評與每季重挑。每月 1 日替每一筆追蹤中的登記寫一則月評；1、4、7、10 月 1 日另用證據包挑攻守各一檔、做新的一筆事前登記。雲端 routine `picks-monthly-auto` 每月 1 日台北執行並 commit push；使用者說「寫挑選月評」「picks 月評」「本站挑選重挑」時也可手動執行。
---

# picks-monthly：「本站挑選」月評與季度重挑

## 定位

兩個頁面各有一份「本站挑選」事前登記清單：`/active-etf/`（台股主動式 ETF 22 檔，基準 0050.TW）與 `/etf-dash/`（21 檔，基準 SPY）。每一筆登記寫死兩檔（攻、守）、登記日數字、六個查核點與結算日（登記日加一年），之後只由程式每天算含息報酬與查核點。登記只能新增，舊登記不停，各自追蹤到自己的結算日。

機械層（候選數據、登記程式、追蹤程式、頁面）不呼叫模型。本 skill 只補兩件需要寫字的事：

1. **月評**：每月 1 日，替每一筆追蹤中的登記寫 2～4 句話，講目前相對基準的差與查核點狀況。
2. **季度重挑**：1、4、7、10 月 1 日，照下面固定規則從證據包挑攻守各一檔，寫四段說明，交給登記程式產生新的一筆登記。

本 skill 只描述、不預測、不寫買賣。挑選規則是固定的，模型只做「照規則挑、把理由寫成白話」，不自由發揮。中文文字先讀 `~/.claude/skills/zh-analyst-prose/SKILL.md`。

## 輸入

兩個市場各一組，名稱對照如下（下文 `<x>` 指其中一組）：

| kind | 資料目錄 | 頁面資料目錄 | 腳本目錄 | 追蹤程式 | 基準 |
|---|---|---|---|---|---|
| `active-etf` | `data/active_etf/` | `docs/active-etf/data/` | `scripts/active_etf/` | `scripts/active_etf/picks.py` | 0050.TW |
| `etf-dash` | `data/etf_dash/` | `docs/etf-dash/data/` | `scripts/etf_dash/` | `scripts/etf_dash/picks_track.py` | SPY |

1. **候選證據包**：`python3 scripts/<x>/picks_candidates.py --brief`。每檔的報酬、最大回檔、頁面指標、持股重疊。**這是挑選與登記文字唯一可以引用的數字來源**（etf-dash 季度登記另加 `picks_base_rate.py` 的基率檔，見 v1.3）。
2. **追蹤摘要**：步驟 3 用程式從 `docs/<x>/data/picks_track.json` 印出（不含逐日序列），含各登記的含息報酬列、查核點現況、上一則月評。**月評唯一可以引用的數字來源是「證據包＋追蹤摘要」。**
3. `data/<x>/picks.json`：登記清單（只讀）。`data/<x>/picks_reviews.json`：已寫的月評（沒有這個檔視為空清單）。

只讀這兩份。證據包沒有的事不寫，不上網搜尋。

## 輸出

### 月評：append 到 `data/<x>/picks_reviews.json`

```json
{"schema": "picks-reviews-v1",
 "reviews": [
   {"reg_id": "2026-10-28", "as_of": "2026-11-01", "data_as_of": "2026-10-30",
    "status_line": "兩檔各半含息 +X%，0050 +Y%，查核點 0／6 觸發",
    "text": "2～4 句，≤ 220 字。",
    "review": {"model": "claude-sonnet-5", "rounds": 1, "findings": []}}
 ]}
```

- `reg_id`：被評的那一筆登記的 id。`as_of`：寫的日期（台北）。`data_as_of`：該登記在 `picks_track.json` 裡的 `as_of`。
- `status_line`：一行摘要，只放數字與狀態，不放判斷。
- `review`：冷讀結果，最後一輪的 model、rounds、findings。
- 同一個 `reg_id` 在同一個月已有月評就不重寫（重跑冪等）。

### 季度登記：只交 text.json，其餘由程式產生

```json
{"paragraphs": [{"lead": "", "text": ""}, {"lead": "", "text": ""}, {"lead": "", "text": ""}, {"lead": "", "text": ""}],
 "frozen_note": ""}
```

`frozen`、登記日數字表、查核點、title、sub 全部由 `picks_register.py` 產生，模型不寫、不改。

## 月評寫作規則

寫哪些登記：`picks_track.json` 裡 `status` 是 `tracking` 的每一筆。`pending`（登記當天還沒有收盤對照）不寫。`settled` 的登記，若還沒有 `as_of` 不早於 `settle_on` 的月評，補寫一則結算月評，之後不再寫。

結構：

1. 第一句講相對基準的差與方向：把兩檔各半的含息報酬和基準的含息報酬**兩個數字都寫出來**，再說領先或落後。不自己算差距。
2. 第二句講查核點：幾個觸發（抄追蹤摘要的「查核點 N／M 觸發」），哪一個離門檻最近（寫那個查核點講的事，附現值與門檻兩個數字）。
3. 可選的第三句：兩檔持股或評價相對登記日的變化，只寫證據包看得到的。
4. 不預測、不寫買賣、不寫「接下來會」。結算月評第一句寫最終數字。

格式限制（`check_picks_text.py --mode review` 會擋）：全文 ≤ 220 字、2～4 句、數字都要在證據裡、無「——」、「；」最多 1 個、無比喻詞與買賣用語、「不是 A，是 B」最多 1 次。

通用寫作規則（對照 zh-analyst-prose）：

1. 一句一個意思，句號收，一句一個主數字。
2. 數字照證據包原本位數抄，不改寫、不自己加減。
3. 不用比喻，不寫「值得點出」「真正該」「本頁不對」這類自我說明。
4. 英文縮寫第一次出現寫中文加括號；基金代號照寫。
5. 中文與數字之間半形空格，中文標點全形。
6. 每則月評獨立成立，不寫「與上月相比」之外的過程敘述，不寫「第 N 次」。

## 季度重挑規則

只在 1、4、7、10 月 1 日做。**規則固定，模型照做，不得換條件、不得憑印象挑。** 判斷用的數字全部取自證據包。基金清單就是證據包列出的全部檔。

### 攻方

1. 先篩出同時滿足兩條的基金：
   - 近一年含息報酬高於基準同區間。
   - 頁面指標顯示盈餘面在改善。etf-dash：近三個月 EPS 上修高於基準（證據包沒有基準的上修值時，改用「大於 0」），且上修寬度 > 60%。active-etf：20 日命中率 ≥ 50%，且自 2025-07-15 起的含息報酬高於 0050。
2. 在篩出的基金裡挑評價相對最便宜的：etf-dash 看 PEG 最低，active-etf 看遠期本益比最低。數值空白或為負的不參加比較。
3. 沒有任何一檔通過兩條，就沿用上一筆登記的攻方（`picks.json` 最後一筆登記的 `role` 為「攻」的那檔），並在第二段明講「沒有任何一檔同時通過兩項檢查，沿用上一季的攻方」。上一季攻方不在證據包基金清單裡就視為失敗（見失敗處置）。

### 守方

**active-etf 的守方固定是 0050 本身，不挑**：登記指令用 `--defend 0050`。2026-10-28 用 16 個月資料檢驗（`docs/active-etf/analysis-2026-10-28.html`）：22 檔在 0050 的大修正裡沒有一檔跌得比 0050 少，主動報酬平均配對相關 0.69～0.78，守的工作 0050 自己做得比任何一檔主動式好。

**etf-dash 的守方固定是 SPY 本身，不挑**（v1.2，2026-10-28 持有人選定）：登記指令用 `--defend SPY`。十年價格面檢驗（`docs/etf-dash/analysis-2026-10-28.html`）：XLV 六次回檔五次比 SPY 淺，但十年落後 SPY 27.7 個百分點，換成 SPY 當守方，十年累計多 59 個百分點、最大回檔只深 3.6 個百分點。查核點對基準守方只剩 cp1～cp5 且只看攻方。下面 1～4 條是舊做法，留作紀錄，兩個市場都不再用。

1. 排名口徑：有近三年最大回檔的基金不少於 3 檔，就用近三年最大回檔，否則全體改用近一年最大回檔。口徑一律全體同一個，不逐檔混用。
2. 取最大回檔最淺（絕對值最小）的前三檔，扣掉攻方本身。
3. 在這幾檔裡挑與攻方持股重疊（證據包持股重疊矩陣）最低的；重疊相同挑遠期本益比較低的。
4. 重疊超過 50% 的不能當守方：換成排名中的次一檔。前三檔都不合格，就依最大回檔排名往下找第 4、5 檔。找不到合格的守方視為失敗。

### 攻方理由的歷史基率（v1.3）

持有人 2026-10-28 定：每季登記的攻方理由，每一條都要附「歷史上這個條件成立時，之後 52 週贏基準的機率與平均超額」。沒有基率的理由不寫進登記。

**etf-dash**：挑完攻方、寫登記文字之前，先跑

```bash
python3 scripts/etf_dash/picks_base_rate.py --attack <攻方代號> --registered-on <TODAY> --out /tmp/picks/base_rate_etf-dash.json
python3 -c "import json;print(json.load(open('/tmp/picks/base_rate_etf-dash.json'))['brief'])" > /tmp/picks/base_rate_etf-dash.txt
```

程式對攻方規則的三條各算一次，比的都是「條件成立的週」對「所有週」，之後 52 週對 SPY 的含息超額：

| 規則 | 歷史上怎麼量 |
|---|---|
| (a) 近一年贏基準 | 攻方自己的週資料：過去 52 週含息報酬高於 SPY |
| (b) 三個月上修高於基準、寬度 > 60% | 代理指數的隱含預估 EPS（價格 ÷ 預估本益比）13 週變化高於標普 500。寬度沒有歷史，不進條件 |
| (c) PEG 最低 | 代理指數預估本益比在過去十年的分位 ≤ 50。PEG 沒有歷史 |

代理指數：SMH、SMH_UCITS 用費城半導體，QQQ 用那斯達克 100，XLK、XLF、XLY、XLP 用標普 500 的資訊科技、金融、非必需消費、必需消費，RSP 用標普 500。其他檔（XLV、XLE、XLI、XLB、XLC、單一國家）只有 (a)，(b)(c) 是「無基率」。

判定是事先寫死的分類線，不是結論：條件成立的週比所有週多贏 3 個百分點以上、而且統計上站得住（t ≥ 2），才是「有預測力」；條件成立不到 52 週或獨立事件不到 5 次是「無基率」；其餘是「沒有」。

寫進第二段的規矩：

1. 至少引用一條的條件內勝率或條件內平均超額，數字照 `base_rate_etf-dash.txt` 原位數抄，同一句寫出所有週的同一個數字，讓讀者自己比。
2. 判定「沒有」的理由照實寫，例如「上修高於 SPY 的週，之後 52 週超額 +9.7%，所有週 +9.8%」。不得寫成好像這個條件會讓它多贏。
3. 判定「無基率」的理由不寫進第二段。它仍是挑選規則，只記在 pick_log。
4. 三條都是「無基率」時，第二段寫出「無基率」三個字，並講規則怎麼挑出它。

**active-etf**：主動式 ETF 只有 16 個月資料，三條都算不出基率。不跑程式，不硬算；第二段寫明攻方理由「無基率」。

### 四段文字

每段 ≤ 160 字、每句 ≤ 60 字。段與段之間不重複同一個數字。

1. **第一段（lead 留空）**：這一季候選整體，只放一個數字（例如候選裡近一年贏基準的檔數，抄證據包，或持股重疊最高的一組）。
2. **第二段（lead 一句主張）**：攻方為什麼。lead 是一句話的主張，text 放 2～3 個支持數字（近一年含息、盈餘面指標、評價），加上至少一條規則的歷史基率（見「攻方理由的歷史基率」）。若沿用上一季攻方，這裡寫明。
3. **第三段（lead 一句主張）**：守方為什麼。lead 一句，text 放 2～3 個數字（最大回檔、與攻方的重疊、評價）。active-etf：lead 寫「守的那一半放 0050」，text 放攻方的 active share（證據包）與攻方對 0050 的最大回檔比較，不再比較其他基金的回檔。etf-dash：lead 寫「守的那一半放 SPY」，text 放攻方與 SPY 的持股重疊（證據包）與攻方對 SPY 的最大回檔、週 beta 比較。
4. **第四段（lead 留空）**：「會錯在哪」，攻方一句、守方一句（active-etf 守方那句改寫「攻方若貼近指數、active share 掉到多少就不划算」；etf-dash 守方那句改寫攻方在基準回檔時會跌更深的那個數字）。各自對應登記後會變壞的那個數字，不重複六個查核點的文字，不預測。

`frozen_note`：一至兩句，抄證據包的兩檔持股加權重疊與基準，講這筆登記的比較基準是什麼（active-etf 寫「守方是 0050 本身，重疊欄用攻方的 active share 換算」；etf-dash 寫「守方是 SPY 本身，重疊欄是攻方與 SPY 的持股重疊」）。不得與第三段重複同一句話。

格式限制（`check_picks_text.py --mode register` 會擋）：固定 4 段、`frozen_note` 非空，其餘同月評。

## 冷讀 subagent 職責書

寫與審永不同模型（見模型配對）。用 `Agent` 工具開**一個** subagent，一次審這輪寫的所有文字（月評與登記文字），只回報、不改稿。prompt 把下面整段逐字貼進去，並把 `<檔案清單>` 換成這一輪的 text.json 路徑與對應證據檔路徑：

> 你是冷讀者。讀下列文字檔和各自的證據檔：<檔案清單>。月評檔的格式是 {"status_line","text"}，登記文字檔是 {"paragraphs":[{"lead","text"}x4],"frozen_note"}。逐項回報，每項給 🔴（必須改）、🟡（建議）或 🟢：
> (a) 有沒有任何句子等於在叫人買或賣、加或減部位、換檔，即使沒用禁用詞。有沒有預測未來（「會」「將」「接下來」寫成事實）。
> (b) 每個數字在證據檔裡找得到嗎？數字旁邊的標籤對不對（例如把攻方的數字寫成守方的、把含息寫成不含息、把三個月寫成一年）。有沒有把相關當成因果。有沒有自己算出來的差距或加總。
> (c) 月評：第一句是否把兩檔各半與基準兩個數字都寫出來並說明領先或落後？第二句是否講查核點觸發數與最接近門檻的那個？全文是否 2～4 句、≤ 220 字？有沒有講證據包沒有的事？
> (d) 登記文字：第二、三段的 lead 是不是主張（不是數字）？攻守的理由是否對得上規則（攻：近一年贏基準＋盈餘面改善＋評價最便宜；守：兩個市場都固定基準本身，etf-dash 是 SPY、active-etf 是 0050）？若沿用上一季攻方，是否在第二段明講？第二段引用的歷史基率，數字與標籤是否對得上基率檔（條件內對所有週、勝率對超額）？判定「沒有」或「無基率」的理由，有沒有被寫成會讓攻方多贏？active-etf 是否寫明「無基率」？第四段是否攻守各一句「會錯在哪」，而且沒有複述查核點？
> (e) 白話與 AI 痕跡：有沒有比喻、「——」串句、「不是 A，是 B」連用、段尾金句、抽象名詞（機制、結構性、敘事、框架）、英文縮寫沒附中文、每句帶括號排名？有就 🔴。表外你覺得難懂的詞或像金句的句子，給 🟡。
> 🟡 是建議，不擋上站。輸出 JSON：{"model": "...", "verdict": "pass" 或 "fix", "findings": [{"file": "...", "item": "a", "level": "🔴、🟡 或 🟢", "note": "..."}]}

## 步驟

所有暫存檔放 `/tmp/picks/`（不進 repo）。以下的 `<x>` 對每個 kind 各做一次；兩個市場互相獨立，一個失敗不影響另一個。

1. `bash scripts/install_hooks.sh`；`git pull --rebase origin main`；`mkdir -p /tmp/picks`。記下台北今天的日期 `TODAY`（YYYY-MM-DD）與月份。
2. 候選證據包：`python3 scripts/<x>/picks_candidates.py --brief > /tmp/picks/brief_<kind>.txt`。用 `Read` 讀完。接著 `python3 <追蹤程式> --no-fetch`，更新 `docs/<x>/data/picks_track.json`（收盤與配息用前一天 CI 的快取，不抓網路）。
3. 追蹤摘要（把 `<kind>`、`<頁面資料目錄>`、`<資料目錄>` 換成上表的值）：

   ```bash
   python3 - <<'PY' > /tmp/picks/digest_<kind>.txt
   import json, pathlib
   d = json.loads(pathlib.Path("<頁面資料目錄>/picks_track.json").read_text(encoding="utf-8"))
   rp = pathlib.Path("<資料目錄>/picks_reviews.json")
   revs = json.loads(rp.read_text(encoding="utf-8")).get("reviews", []) if rp.exists() else []
   regs = d.get("registrations") or [dict(d, id=d.get("registered_on"))]
   print(f"# 追蹤摘要 {d.get('generated_at')}")
   for r in regs:
       cps = r.get("checkpoints") or []
       n_trig = sum(1 for c in cps if c.get("status") == "triggered")
       picks = "、".join(f"{p['code']} {p.get('role','')}" for p in r.get("picks", []))
       print(f"\n## 登記 {r.get('id')}　狀態 {r.get('status')}　登記日 {r.get('registered_on')}　結算日 {r.get('settle_on')}　資料日 {r.get('as_of')}　基準日 {r.get('base_date')}　{picks}")
       for row in r.get("rows") or []:
           print("  列：" + json.dumps(row, ensure_ascii=False))
       print(f"  查核點 {n_trig}／{len(cps)} 觸發")
       for c in cps:
           print(f"  - {c.get('id')} [{c.get('status')}] {c.get('text')}｜現值：{c.get('current_label')}")
       prev = [v for v in revs if v.get("reg_id") == r.get("id")]
       if prev:
           p = sorted(prev, key=lambda v: v["as_of"])[-1]
           print(f"  上一則月評（{p['as_of']}）：{p.get('status_line')}｜{p.get('text')}")
   PY
   cat /tmp/picks/brief_<kind>.txt /tmp/picks/digest_<kind>.txt > /tmp/picks/ev_<kind>.txt
   ```

   讀 `/tmp/picks/digest_<kind>.txt`。檢查資料新鮮度：要寫月評的登記，`as_of` 距 `TODAY` 超過 5 天就是追蹤資料過期，該市場失敗（stage `資料`）。
4. 寫月評：對每一筆要寫的登記（見月評寫作規則），把 `{"status_line": "...", "text": "..."}` 存成 `/tmp/picks/review_<kind>_<reg_id>.json`。同一個 `reg_id` 本月已有月評的跳過。
5. 機械檢查：`python3 scripts/check_picks_text.py --kind <kind> --mode review --text /tmp/picks/review_<kind>_<reg_id>.json --evidence /tmp/picks/ev_<kind>.txt` 必須 PASS。FAIL 就依原因改稿再跑，最多 3 次，仍 FAIL 進失敗處置（stage `月評檢查`）。
6. 若 `TODAY` 的月份是 1、4、7、10（季度重挑）且 `picks.json` 還沒有 `id` 等於 `TODAY` 的登記：照「季度重挑規則」從 `/tmp/picks/brief_<kind>.txt` 挑攻守各一檔。etf-dash 接著跑「攻方理由的歷史基率」的兩行指令（程式失敗進失敗處置，stage `基率`）。寫 `/tmp/picks/register_<kind>.json`（四段＋`frozen_note`），先跑 `python3 scripts/check_picks_text.py --kind <kind> --mode register --text /tmp/picks/register_<kind>.json --evidence /tmp/picks/brief_<kind>.txt`（etf-dash 加 `--base-rate /tmp/picks/base_rate_etf-dash.json`，會檢查第二段有沒有引用基率），PASS 為止（最多 3 次，stage `登記檢查`）。同時把挑選過程記在 `/tmp/picks/pick_log_<kind>.txt`（每條規則各檔的數字與結果，etf-dash 另抄三條基率的判定），冷讀要看。
7. **冷讀**：用 `Agent` 工具開一個 subagent（`model` 用 `claude-sonnet-5`），貼入「冷讀 subagent 職責書」。檔案清單＝這輪的月評檔與登記文字檔，各自對應的證據檔，`/tmp/picks/pick_log_<kind>.txt`，etf-dash 另加 `/tmp/picks/base_rate_etf-dash.txt`。依 findings 修稿，最多 2 輪；只有 🔴 必須改，🟡 由寫稿者取捨。改過的稿重跑步驟 5、6 的檢查。第 2 輪後仍有 🔴 進失敗處置（stage `冷讀`）。
8. append 月評（用程式寫，不手改 JSON；把 `review` 換成最後一輪冷讀的 model、rounds、findings）：

   ```bash
   python3 - <<'PY'
   import json, pathlib
   p = pathlib.Path("<資料目錄>/picks_reviews.json")
   d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"schema": "picks-reviews-v1", "reviews": []}
   t = json.loads(pathlib.Path("/tmp/picks/review_<kind>_<reg_id>.json").read_text(encoding="utf-8"))
   d["reviews"].append({"reg_id": "<reg_id>", "as_of": "<TODAY>", "data_as_of": "<該登記的 as_of>",
                        "status_line": t["status_line"], "text": t["text"],
                        "review": {"model": "claude-sonnet-5", "rounds": 1, "findings": []}})
   p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
   PY
   ```

9. 季度登記：`python3 scripts/<x>/picks_register.py --attack <攻方代號> --defend <守方代號> --registered-on <TODAY> --text /tmp/picks/register_<kind>.json --dry-run` 先看輸出，沒錯再去掉 `--dry-run` 正式寫入。etf-dash 加 `--base-rate /tmp/picks/base_rate_etf-dash.json`，結果原樣存進該筆登記的 `frozen.base_rates`。程式會自己再跑一次文字檢查；它拒絕就照訊息處理（證據日期過舊、同日已有登記、基率檔的攻方或登記日對不上）。
10. 重跑追蹤程式讓頁面資料帶上新登記與新月評：`python3 <追蹤程式> --no-fetch`。確認 `docs/<x>/data/picks_track.json` 的 `registrations` 有新登記、各登記的 `reviews` 有新月評。
11. 寫 `data/<x>/picks_status.json`：成功寫 `{"as_of": TODAY, "status": "ok"}`。
12. `python3 scripts/qc.py` 必須 PASS。
13. `git status --short` 確認沒有別的檔案夾帶。只 stage 這些檔（兩個市場各自存在的才加）：`data/<x>/picks.json`、`data/<x>/picks_reviews.json`、`data/<x>/picks_candidates.json`、`data/<x>/picks_status.json`、`docs/<x>/data/picks_track.json`。不得 `git add -A`、不得 `--no-verify`。設 `git config user.name "github-actions[bot]"`、`git config user.email "github-actions[bot]@users.noreply.github.com"`。commit 訊息：`picks-monthly {TODAY}：{各市場月評 N 則、新登記 攻代號／守代號 或 無}`，結尾 `Co-Authored-By: Claude <noreply@anthropic.com>`。`git pull --rebase origin main` 後 `git push origin main`，失敗重試 3 次。

## 失敗處置

只影響出問題的那個市場。該市場的 `picks.json`、`picks_reviews.json` 維持步驟開始前的樣子（已經通過檢查並 append 的月評保留；沒完成的季度登記不寫），只寫 `data/<x>/picks_status.json` = `{"as_of": TODAY, "status": "failed", "stage": "<哪一關>", "reasons": [...]}`。`stage` 取值：`資料`（候選或追蹤資料缺、過期）、`月評檢查`、`登記檢查`、`冷讀`、`挑選`（沒有合格守方、上一季攻方不在清單）、`基率`（picks_base_rate.py 失敗）、`登記程式`、`qc`。`reasons` 抄檢查程式或冷讀的原文。另一個市場照常完成，最後同一個 commit 一起 push（失敗的市場只帶 `picks_status.json`）。兩個市場都失敗時，只 commit 兩個 `picks_status.json`。

## 模型配對（寫與審永不同模型）

| 寫文字（routine 的 session model） | 冷讀（Agent subagent） |
|---|---|
| `claude-opus-5-5` | `claude-sonnet-5` |
| 手動由 orchestrator（opus）跑 | `claude-sonnet-5` |

## 硬規則

- 登記清單只能 append。既有登記的任何欄位不改；`frozen`、登記日數字、查核點由 `picks_register.py` 產生，模型不手寫、不手改。
- 不手改 `picks_track.json`、`picks_candidates.json`、頁面 HTML、`picks_candidates.py`、`picks_register.py`、追蹤程式與任何機械層檔案。
- 數字只能抄證據包與追蹤摘要，照原位數，不自己算差距或加總。
- 月評不預測、不寫買賣、不寫換檔建議。查核點觸發了就陳述「某某查核點已觸發」，後果欄的文字由頁面顯示，月評不替它下結論。
- 挑選規則固定：不換條件、不憑印象挑、不因為某檔最近漲得多而破例。
- 不上網搜尋。證據包沒有的事不寫。
- 不改 routine 排程，不改 `.github`。
- 任何檢查或冷讀兩輪仍不合格就停止，不繞過驗證、不 `--no-verify`。

## 版本

- v1.0 2026-10-28：初版。兩個頁面的「本站挑選」改成可累積的登記清單，每月 1 日加一則月評，每季（1、4、7、10 月）重挑一筆。回頭檢討條件：月評連續兩個月因冷讀失敗，或某一季「沒有任何一檔通過攻方篩選」連續兩季（代表篩選條件在目前市況下過嚴）。
- v1.1 2026-10-28：active-etf 守方固定 0050（深度檢驗：22 檔沒有一檔在修正裡比 0050 淺，主動報酬同一個賭注）。登記程式 `--defend 0050`、`--kind revision`、`--extra-evidence`；查核點對基準守方只剩四個，cp4 改看攻方 active share。
- v1.2 2026-10-28：etf-dash 守方固定 SPY（十年檢驗：SMH＋XLV 各半 951% 對 SMH＋SPY 各半 1010%，回檔只差 3.6 個百分點；登記理由「EPS 上修股價跌」在歷史上沒有預測力，攻方理由改寫成長期贏家）。登記程式 `--defend SPY` 走基準守方分支，查核點 cp1～cp5 只看攻方。
- v1.3 2026-10-28：攻方理由附歷史基率（持有人定：沒有基率的理由不寫進登記）。etf-dash 季度登記必跑 `picks_base_rate.py`，登記程式 `--base-rate` 把三條基率凍結進 `frozen.base_rates`，文字檢查要求第二段引用其中一條的勝率或超額；active-etf 資料太短，寫「無基率」。SMH 回頭檢查三條都是「沒有」，評價那條反向（本益比分位 ≤ 50 的週之後 52 週超額 +4.7%，所有週 +12.4%）。
