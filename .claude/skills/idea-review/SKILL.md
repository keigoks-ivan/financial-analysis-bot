---
name: idea-review
description: 投資想法頁（docs/ideas/*.html）的每月全面檢視（雲端 routine `idea-review-auto`，每月 1 日 06:30 台北，排在 idea-watch 05:15 之後）。每頁重答五題（主張還對不對、什麼事實變了、反方多強、對錢的意義、下個月看什麼），給判定與處置，有主觀機率的頁重打機率，追加一筆到 docs/ideas/data/review.json，寫一份 review_YYYY-MM.md 給持有人讀，commit push。不改想法頁、不改 ideas.json。使用者說「跑想法月檢視」「idea review」「想法頁全面檢視」時也可手動執行。
---

# idea-review：投資想法頁每月全面檢視

## 定位

`/ideas/` 有三層追蹤，各管一段時間：

- 早報（每天 06:15）：新聞關鍵字比對，結果在 `docs/briefing/data/idea_hits.json`。
- idea-watch（每天 05:15）：每個查核點現在是支持、動搖還是推翻，結果在 `docs/ideas/data/research.json`。
- **本 skill（每月 1 日 06:30 台北）**：整頁看一次。查核點只管單一事件，本 skill 回答「這篇想法整體還站不站得住、頁面要不要改」。

全面檢視不是只核對數字。每頁要重答五題，再給處置：

| 檢視五題 | 寫進哪一欄 | 對應頁面上的哪一題（idea-writing 五必答） |
|---|---|---|
| 主張還對不對 | `verdict`＋`thesis` | 主張 |
| 什麼事實變了 | `facts` | 查核點 |
| 反方多強 | `counter` | 反方 |
| 對錢的意義 | `money` | 對錢的意義、收回條件 |
| 下個月看什麼 | `watch` | 查核點的到期事件 |
| 處置 | `action` | 不動／改幾句／整頁重寫 |
| 主觀機率重打 | `scenarios` | 三種情境（只限本來就有主觀機率的頁） |

結果追加到 `docs/ideas/data/review.json`（不覆蓋歷史），由 `docs/ideas/data/review.js` 顯示在每頁主張方框下方，索引頁讀同一份檔出標籤。

不做的事：不改任何想法頁 HTML、不改 `ideas.json`、不改 `research.json`、不自行改寫頁面。判「改幾句」或「整頁重寫」只是處置建議，由持有人決定後另開 session 照 `idea-writing` 改。股價表由另一支每日腳本重算，不在檢視範圍；檢視可以引用頁面現在的數字。

這份是檢視紀律，不是裁決閘，不登記 rule_ledger。

## 時間與證據窗

- 檢視日 D：台北時間今天（`YYYY-MM-DD`）。檢視月：D 的年月，檔名與 commit 都用它（12 月 1 日跑的叫 `2026-12`，內容涵蓋 11 月）。
- 每頁的證據窗：該頁上一筆檢視的 `date` 隔天到 D。沒有上一筆就從 D 的前一個月 1 日起算；頁面建立日（`ideas.json` 的 `created`）比起點晚，就從建立日起算。
- 同一頁在檢視月已有一筆（例如手動先跑過）就跳過，不重寫、不覆蓋。全部都已有就直接結束，不 commit。

## 輸入（讀什麼）

1. `docs/ideas/ideas.json`：`status` 為 `active` 的每個 `id`，各查核點的 `label`、`companies`、`company_names`、`keystone`、`due`。
2. 每頁正文 `docs/ideas/<id>.html`（先去掉 `<script>` 與標籤再讀）。要找到的段落：主張方框（`<div class="thesis">`）、一頁摘要最後一條（撐住結論的視角）、三種情境與主觀機率、反方意見、收回條件（標題含「收回」的那一節）、還沒查到的。
3. 同一頁 `CPS` 陣列的中文 `yes`／`no` 條件。
4. `docs/ideas/data/research.json`：`status` 裡該頁每個查核點檢視當天的狀態；`entries`、`changes` 裡 `date` 在證據窗內、`idea` 等於該頁的紀錄。用 Python 篩出來讀，不要整檔讀進來。
5. `docs/briefing/data/idea_hits.json`：證據窗內該頁的 `supports`／`refutes`／`shaky`（`neutral` 只計數）。
6. `docs/earnings/earnings_YYYY-MM-DD.html`：日期在證據窗內的全部。每份約 100KB，先用該頁查核點的 `companies` 與 `company_names` 搜尋，只讀命中的段落。當天若已有 `docs/earnings/synthesis_<D>.html`（月度財報統整）也讀；沒有不等。
7. 週報：`docs/weekly/` 下日期在證據窗內的檔，有才讀（2026-06-21 之後沒有新檔）。
8. 對錢的意義要用的兩個檔：
   - `docs/long-track-w52-adaptive/state.json`：`tickers.QQQ／SMH／0050／2330.executed_pct`（占指數部 %，水位＝乘以 2，用整數算）、`overlay.ief`／`overlay.gld` 的 `n`（週線三條件過幾條）與 `target_pct`、`last_change_desc`。
   - `docs/engine/roster_notify_state.json`：美股看板（`us`）、台股（`tw`）、精選榜十倍組（`tb`）三套席位的 `seats`。
9. 下個月看什麼要用的日曆：`ideas.json` 的 `due`、`docs/catalyst/calendar.json`（財報日，`type: earnings`）、總經類頁加 `docs/monitor/data/macro_calendar.json`。
10. 上網：可以 WebSearch／WebFetch 查原始財報、10-Q／8-K、公司新聞稿、央行與政府數據。一手來源優先，媒體只在一手讀不到時用。

## 步驟

1. `bash scripts/install_hooks.sh`；`git pull --rebase origin main`。
2. 讀 `docs/ideas/data/review.json`。檔案不存在就從 `{"schema":"idea-review-v1","updated":"<D>","reviews":[]}` 開始。照上一節決定哪些頁要做。
3. 看 `research.json` 的 `run`：`run.date` 不是 D 或 `run.status` 不是 `ok`，照常檢視，但在 md 末尾寫「idea-watch 今天未完成，查核點狀態取到 <run.date>」。
4. 逐頁檢視（順序：證據窗內有關鍵查核點 refutes／shaky 的頁先做，再做有到期事件的頁，最後其他頁）：
   1. 讀上一節第 2～7 項。
   2. 上網核對：每頁 2～4 組查詢，搜到的重要結果用 WebFetch 讀原文，不能只靠搜尋摘要。優先查三件事：收回條件裡的數字現在多少、關鍵查核點的到期事件結果、頁面主張依賴的那個數字有沒有變。頁數多時可以每頁派一個 sonnet subagent 只做上網核對，回傳「日期、數字、原文網址」清單；判斷與寫字由 routine 本身做。
   3. 依下一節判 `verdict`、`action`，寫各欄。
5. 判「被推翻」的頁要冷讀：用 `Agent` 工具開一個 sonnet subagent（寫者 opus、審者 sonnet，模型不同），只給頁面路徑、收回條件原文、你認定成立的事實與原文連結，要它回報「同意／不同意＋一句理由」。不同意就改判「動搖」，理由寫進 md 該頁第二行。只冷讀一輪，不來回。
6. 寫 `review.json`：每頁一筆追加到 `reviews` 陣列末尾，`updated` 改成 D。既有的筆一個字都不動。
7. 寫 `docs/ideas/data/review_<檢視月>.md`（格式見後）。
8. 跑「機械檢查」一節的指令，必須印出 `OK`；`python3 -c 'import json;json.load(open("docs/ideas/data/review.json"))'`；`python3 scripts/qc.py --escalate docs/ideas/data/review_<檢視月>.md` 必須通過。
9. commit 與 push：
   - 只 `git add docs/ideas/data/review.json docs/ideas/data/review_<檢視月>.md`。
   - commit 訊息第一行：`idea-review YYYY-MM：N 頁，成立 a／動搖 b／被推翻 c，重寫 d`（N＝本次寫入的頁數，d＝`action` 為整頁重寫的頁數）。有整頁重寫或被推翻的頁，第二行起列出：`整頁重寫：id、id`、`被推翻：id`，沒有就不寫那行。
   - `git pull --rebase origin main`，`git push origin main`，失敗重試 3 次。rebase 在 `review.json` 衝突時，以遠端版本為底，把本次的幾筆重新追加，再跑一次步驟 8。
10. 中途失敗、只做完部分頁：做完的頁照寫，不寫空殼；沒做的頁在 md 列「本月未檢視：<id>，原因」；commit 訊息第一行尾加「（未完成 k 頁）」，照步驟 9 推上去。一頁都沒做完就只寫 md 說明原因，單獨 commit push。

## 每頁怎麼判

### verdict（三選一）

- **成立**：關鍵查核點（`ideas.json` 裡 `keystone: true`）都沒有 refutes，而且收回條件一條都沒碰到。
- **動搖**：關鍵查核點有任一個是 refutes 或 shaky，或收回條件有一條碰到邊。
- **被推翻**：收回條件任一條成立。

名詞定義：

- 關鍵查核點「有 refutes／shaky」：看 `research.json` 的 `status` 在檢視當天的狀態。狀態是 supports，但證據窗內的 entries 或 idea_hits 有 refutes、而且之後沒有一手資料翻回來，也算。非關鍵查核點的 refutes 不單獨改變 verdict，但要寫進 `facts` 或 `counter`。
- 收回條件「碰到邊」：條件寫的事已經部分發生，字面門檻還沒到。兩種情形：數字已走到門檻的九成以上（例：30 天走寬 72bp，警戒線 75bp）；或條件寫的是未來某年，同樣的事已在更早的季度出現（例：條件寫 2027 年兩家自由現金流轉負，本季已有三家為負）。
- 收回條件「成立」：條件字面上的事已發生，有一手來源或兩個互相獨立的來源。只有二手來源時判「碰到邊」，`facts` 的 `source` 寫出是哪個二手來源。
- 沒有查核點的頁（目前是 ai-chip-design）只看收回條件。

### action（三選一）

- **不動**：頁面上沒有句子被證據窗內的事實推翻。股價與報價自然變動不算（股價表每日自動重算）。
- **改幾句**：主張與撐住結論的視角都沒變，但有句子跟事實對不上：到期事件結果沒寫、判斷句被新數字推翻、收回條件字面跟現況對不上、或要補一節證據窗內才出現的事。要改的地方集中在三節以內。
- **整頁重寫**：撐住結論的那個視角（一頁摘要最後一條寫的）被事實推翻、主情境的觸發條件被事實排除、或要改的地方散在一半以上的節。判「被推翻」的頁一律整頁重寫，要不要收掉這篇由持有人決定，寫在 md。

### 對錢的意義（money）

- 對照實單與席位講受惠、受壓：實單是 QQQ／SMH 各半（美股指數部）、0050／2330 各半（台股指數部）、IEF／GLD 各最多 20% 的債金腿；席位是三套名單的 `seats`。寫成「SMH 水位 80%、台積電在台股席位，主張若對兩者受壓」這種具體句。
- 同一欄要交代收回條件現在離成立多遠。
- 實單只照 W52 規則與執行層調整，想法頁不改部位。不寫加碼、減碼、買進、賣出建議。和實單、席位都沒有直接部位時直說「實單與席位沒有直接部位」，再講影響哪類公司。

### 下個月看什麼（watch）

- 只放 D 到下個月 1 日之間的事件：該頁查核點的 `due`、`docs/catalyst/calendar.json` 裡該頁查核點公司的財報日、總經類頁的 `macro_calendar.json`。
- 1～4 條，照日期排；只放會改變 verdict 或機率的事。寫「看哪個數字」，不只寫事件名。`approx: true` 或日曆標推估的日期，句尾加「（推估）」。

### 情境機率（scenarios）

- 只給頁面上寫了「主觀機率」的頁，以頁面現況為準。升息機率、Kalshi 這類市場報價不算主觀機率。沒有的頁不寫 `scenarios` 這個欄位。
- `name` 用頁面上的情境名稱。`prob` 用整數，各情境加總 100（壓力情境頁面沒給機率就不列）。
- `prev`：上一筆檢視同名情境的 `prob`。沒有上一筆，或頁面改寫後情境換了名字，就填頁面現在寫的值；頁面也沒寫就填 `null`。
- 機率只因證據窗內的事實移動，每個變動都要能在 `facts` 或 `counter` 找到對應的那一條；找不到就 `prob` 等於 `prev`。月內價格漲跌本身不是觸發條件，不能只因價格走勢調機率。

## review.json 格式（schema `idea-review-v1`）

```json
{"schema":"idea-review-v1","updated":"2026-12-01",
 "reviews":[
  {"idea":"ai-scissors","date":"2026-12-01","verdict":"成立|動搖|被推翻","action":"不動|改幾句|整頁重寫",
   "thesis":"一句：主張還對不對、為什麼（≤60 字）",
   "facts":[{"date":"2026-11-19","text":"事實一句（≤50 字）","source":"來源短名"}],
   "counter":"反方現在多強，哪條變強變弱（≤80 字）",
   "money":"對錢的意義有沒有變：受惠／受壓、收回條件有沒有碰到（≤80 字）",
   "watch":[{"date":"2026-12-09","text":"看什麼（≤30 字）"}],
   "scenarios":[{"name":"消化期","prob":55,"prev":55}],
   "by":"opus"}
 ]}
```

- 每頁每月一筆。同一頁多筆時，頁面顯示 `date` 最新的一筆，其餘收進「歷次檢視」。
- `facts` 2～5 條，`date` 是事件發生日，不是查到的日子；`source` 寫短名（公司 10-Q、新聞稿、FRED、TrendForce）。
- `by`：routine 與手動都寫 `opus`。
- 頁面上沒有 `id="review"` 容器的頁照寫，在 md 末尾列出「未掛檢視區塊：<id>」，由持有人決定要不要補。

## 文字規格

照 `zh-analyst-prose`。

| 欄位 | 字數上限（Python `len()`） | 寫什麼 |
|---|---|---|
| `thesis` | 60 | 結論先行：主張還對不對，加一個理由 |
| `facts[].text` | 50 | 一件事、一個數字 |
| `counter` | 80 | 頁面反方哪一條變強、哪一條變弱，附數字 |
| `money` | 80 | 受惠／受壓的實單部位與席位，收回條件離成立多遠 |
| `watch[].text` | 30 | 看哪個數字 |

- 白話、結論先行、每條一個數字。
- 中文後一律全形標點（，。：；「」（）），中文與數字、英文之間半形空格。
- 不用比喻（zh-analyst-prose 第 13 條的詞都不用），不寫「之前」「舊版」「上次說」，直述現在的事實。
- 不寫過程自我對話（「本次檢視發現」「重新查核後」），不寫套話（「值得注意的是」）。
- 一筆檢視最多一個「不是……是……」句。
- 英文縮寫第一次出現寫中文，例如「自由現金流（FCF）」。
- 數字找不到就不寫那一條，不捏造、不拿上個月的數字填。
- 無法上網（WebSearch／WebFetch 失敗）時只用 repo 內資料，每頁 `thesis` 句尾加「（本月未上網核對）」，這幾個字不算進 60 字。

## review_YYYY-MM.md 格式

每月都寫，給持有人讀。整頁重寫與被推翻的頁放最前面，每頁兩行，頁名用 `ideas.json` 的 `short`：

```markdown
# 投資想法月檢視 2026-12（檢視日 2026-12-01）

12 頁：成立 a／動搖 b／被推翻 c；整頁重寫 d、改幾句 e、不動 f。

## 要你決定的

- AI 硬體循環（ai-hardware-cycle）：動搖｜整頁重寫。<thesis>
  要重寫的原因一句；被推翻的頁另寫「重寫或收掉這篇，請持有人決定」。

## 其他各頁

- AI 剪刀差（ai-scissors）：成立｜不動。<thesis>
  <money 一句，或要改哪幾句>

## 附註

- 本月未檢視、未掛檢視區塊、idea-watch 未完成、未上網核對，有才寫。
```

## 機械檢查

寫完 `review.json` 後在 repo 根目錄跑，必須印出 `OK`：

```bash
python3 - <<'EOF'
import json, re, subprocess, sys
from datetime import datetime, timedelta, timezone
D = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
P = "docs/ideas/data/review.json"
d = json.load(open(P, encoding="utf-8"))
ideas = {i["id"]: i for i in json.load(open("docs/ideas/ideas.json", encoding="utf-8"))["ideas"]}
CJK = re.compile(r"[一-鿿][,.:;!?()]")
err = []
if d.get("schema") != "idea-review-v1": err.append("schema 不是 idea-review-v1")
if d.get("updated") != D: err.append("updated 不是今天")
month = {}
for r in d["reviews"]:
    month.setdefault((r.get("idea"), str(r.get("date"))[:7]), []).append(r)
for (i, m), rs in month.items():
    if len(rs) > 1: err.append(f"{i} {m}：同月 {len(rs)} 筆")
new = [r for r in d["reviews"] if r.get("date") == D]
for r in new:
    t = r.get("idea")
    if ideas.get(t, {}).get("status") != "active": err.append(f"{t}：不是 active 想法")
    if r.get("verdict") not in ("成立", "動搖", "被推翻"): err.append(f"{t}：verdict")
    if r.get("action") not in ("不動", "改幾句", "整頁重寫"): err.append(f"{t}：action")
    if r.get("verdict") == "被推翻" and r.get("action") != "整頁重寫": err.append(f"{t}：被推翻要整頁重寫")
    if not r.get("by"): err.append(f"{t}：缺 by")
    th = r.get("thesis", "").replace("（本月未上網核對）", "")
    for k, s, n in (("thesis", th, 60), ("counter", r.get("counter", ""), 80), ("money", r.get("money", ""), 80)):
        if not s: err.append(f"{t}：{k} 空白")
        if len(s) > n: err.append(f"{t}：{k} {len(s)} 字，上限 {n}")
    texts = [th, r.get("counter", ""), r.get("money", "")]
    for f in r.get("facts", []):
        if len(f.get("text", "")) > 50: err.append(f"{t}：fact {len(f['text'])} 字")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(f.get("date", ""))): err.append(f"{t}：fact 日期格式")
        texts.append(f.get("text", ""))
    for w in r.get("watch", []):
        if len(w.get("text", "")) > 30: err.append(f"{t}：watch {len(w['text'])} 字")
        texts.append(w.get("text", ""))
    sc = r.get("scenarios")
    if sc:
        if any(not isinstance(s.get("prob"), int) for s in sc): err.append(f"{t}：prob 要整數")
        elif sum(s["prob"] for s in sc) != 100: err.append(f"{t}：機率加總 {sum(s['prob'] for s in sc)}")
        if any(s.get("prev") is not None and not isinstance(s["prev"], int) for s in sc): err.append(f"{t}：prev 要整數或 null")
    for s in texts:
        if CJK.search(s): err.append(f"{t}：中文後半形標點「{s[:20]}」")
try:
    old = json.loads(subprocess.run(["git", "show", f"HEAD:{P}"], capture_output=True, text=True, check=True).stdout)
    cur = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in d["reviews"]}
    for x in old.get("reviews", []):
        if json.dumps(x, sort_keys=True, ensure_ascii=False) not in cur:
            err.append(f"舊筆被改動或刪除：{x.get('idea')} {x.get('date')}")
except subprocess.CalledProcessError:
    pass
print("\n".join(err) if err else f"OK：今天 {len(new)} 筆")
sys.exit(1 if err else 0)
EOF
```

## 硬規則

- 描述器紀律：不寫買賣建議、目標價、部位建議。
- 不改任何想法頁 HTML、`ideas.json`、`research.json`、`idea_hits.json`、早報與財報任何檔、routine 排程本身。判要改的頁只寫處置，不自行改寫。
- `review.json` 只追加，既有的筆不改、不刪、不重排。
- 只 add `review.json` 與當月 md。不得 `git add -A`，不得 `--no-verify`，不得 `--amend`。
- 數字只能來自讀到的原文或 repo 內的檔；找不到留空，不捏造。
- 付費牆讀不到全文時只用標題與摘要，該條 `facts` 的 `source` 寫「（只讀到摘要）」。
- 無法上網時用 repo 內資料，`thesis` 註明「本月未上網核對」。

## routine prompt

給 `/schedule` 建 `idea-review-auto` 用，排每月 1 日 06:30 台北，模型 opus：

```
照 .claude/skills/idea-review/SKILL.md 跑本月想法頁檢視。只追加 review.json、寫當月 md，只 add 這兩檔；不改想法頁與 ideas.json；不寫買賣建議；數字找不到留空；禁 git add -A、--no-verify、--amend。
```

## 版本

- v1.0 2026-11-01：初版。同日持有人拍板每月檢視一次（五題＋處置＋重打主觀機率留軌跡），第一份由人工檢視寫成（日期 2026-11-01），routine 從 2026-12-01 起跑。
