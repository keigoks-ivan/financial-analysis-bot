---
name: idea-watch
description: 投資想法查核點的每日深入查核（雲端 routine `idea-watch-auto`，每天 05:15 台北）。讀 docs/ideas/ideas.json 的查核點，主動搜尋新聞與一手來源、到期事件讀財報新聞稿與法說逐字稿，判斷每個查核點目前是支持、動搖或推翻，寫 docs/ideas/data/research.json 後 commit push。使用者說「跑想法查核」「idea watch」「更新查核點狀態」時也可手動執行。
---

# idea-watch：投資想法查核點每日深入查核

## 定位

`/ideas/` 每篇想法有 6～9 個查核點，定義在 `docs/ideas/ideas.json`。查核分兩層：

- 早報（06:15，GitHub Actions）：新聞關鍵字比對＋Jev 判支持／推翻，便宜的第一道篩選，結果在 `/briefing/data/idea_hits.json`。
- **本 skill（05:15，雲端 routine，月租方案）**：主動搜尋、讀一手來源、到期事件讀財報，給每個查核點一個目前狀態。結果寫 `docs/ideas/data/research.json`，想法頁、想法清單、早報、Email 都讀這份。

本 skill 只回答「查核點現在是支持、動搖還是推翻」，不下買賣結論、不改想法頁內文、不改 `ideas.json`。

## 輸入

1. `docs/ideas/ideas.json`：每個 active 想法的查核點（`label`、`companies`、`company_names`、`keywords`、`supports_if`、`refutes_if`、`keystone`、`due`）。
2. 每篇想法頁 `docs/ideas/<id>.html` 裡 `CPS` 陣列的中文「成立／推翻」條件（`yes`、`no`），這是判斷的主要依據；`supports_if／refutes_if` 是同一件事的英文版。
3. `docs/ideas/data/research.json`：上一次的狀態與累積紀錄（沒有這個檔就視為第一次執行）。
4. `docs/briefing/data/idea_hits.json`（直接讀 repo 裡的檔，不要走網址：雲端環境的網路代理會擋 research.investmquest.com）：早報 Jev 的比對，當線索用，不當結論。這個檔是前一天早報產生的。

## 步驟

1. `bash scripts/install_hooks.sh`；`git pull --rebase origin main`。
2. 讀輸入。今天日期用台北時間。
3. **決定今天查什麼**（前三類每天都要做；第四類只在台北時間週一做）：
   - **到期事件**：`due` 裡日期落在「今天往前 3 天到今天」、且 `research.json` 還沒有同一個 `event` 的 `kind: "earnings"` 紀錄者，讀公司官方新聞稿（IR 網站、SEC 8-K、證交所公告）。`approx: true` 的日期要先確認事件真的已發生。
   - **逐字稿補查**：前 3 天內做過 `kind: "earnings"`、但 `transcript_checked` 是 false 的，找法說逐字稿或官方重點摘要，補查新聞稿沒講的財測用字與供需描述。
   - **主動搜尋**：每個 active 查核點用 2～4 組查詢搜過去 48 小時（第一次執行搜過去 30 天）。搜到的重要結果要用 WebFetch 讀原文，不能只靠搜尋摘要；原文讀不到（對方擋機器人、付費牆）才用摘要，並照硬規則註明。查詢從 `label`、`company_names`、`keywords` 組；台灣公司（台積電、信驊、華城等）加中文查詢。優先找一手或專業來源：公司 IR、SEC、證交所公開資訊觀測站、TrendForce 新聞稿、Cloudflare 部落格與 Radar、主要財經媒體。
   - **週一全面複查**（2026-09-24 使用者要求）：把每個狀態不是 `no_data` 的查核點，拿它目前 `reason` 裡的每個數字與事實，回到原文逐一核對（WebFetch 讀原文；公司新聞稿、SEC、證交所、TrendForce 優先）。數字對不上就改 `reason`；核對後證據不足以支撐原狀態，就照步驟 5 改狀態並寫 `changes`（`reason` 開頭寫「週一複查：」）。每個查核點寫一筆 `kind: "reverify"` 的 entry，`summary` 寫核對結果（例：「週一複查：3 個數字與原文一致」或「週一複查：營收 650 億美元原文是 7 月底年化，已更正」）。同一週已複查過（`entries` 裡本週一已有 `reverify`）就不重做。
4. **逐則判斷**：每則證據對照該查核點的「成立／推翻」條件，給 `verdict`：
   - `supports`：符合成立條件。
   - `refutes`：符合推翻條件。
   - `shaky`：方向不利但還沒到推翻條件，或同時有支持與不利的訊號。
   - `neutral`：相關但不影響判斷（寫進紀錄，不影響狀態）。
   - 無關的不寫。
   判斷原則（2026-09-23 定）：單一數字（一個月營收、一筆報價）沒講到趨勢或財測變化，最多算 `neutral`；舊世代產品降價不算；受景氣影響大的指標（廣告收入）只算公司明講或第三方數據歸因；新 App 上線熱度後的自然回落不算；公司沒公布的數字不能當證據。
5. **更新狀態**（每個查核點一個）：`supports`／`shaky`／`refutes`／`no_data`。
   - 沒有新證據就維持原狀態，只更新 `checked`。
   - 轉成 `refutes` 需要一手來源，或兩個互相獨立的來源。
   - 狀態有變化時寫一筆 `changes`。
6. **關鍵查核點的狀態變化要冷讀**：`keystone: true` 的查核點狀態有任何變化時，用 `Agent` 工具開一個 subagent 冷讀（寫者與審者不同模型：routine 用 opus，冷讀用 sonnet），給它證據原文連結、查核點條件、你的判斷，要它只回報「同意／不同意＋理由」。不同意就維持原狀態，把理由寫進 `changes[].review`。
7. **寫 `docs/ideas/data/research.json`**（格式見下），`python3 -c "import json;json.load(open('docs/ideas/data/research.json'))"` 驗證，`python3 scripts/qc.py docs/ideas/data/research.json` 必須通過。
8. 只 stage `docs/ideas/data/research.json`（**不得 `git add -A`**），commit 訊息「idea-watch YYYY-MM-DD：N 則新證據，M 個狀態變化」，`git pull --rebase origin main`，`git push origin main`，失敗重試 3 次。
9. 任何步驟失敗：不改狀態，只把 `run.status` 設 `failed`、`run.reason` 寫原因，照步驟 8 單獨 commit push（Email 工作流會寄失敗信）。

## research.json 格式（schema `idea-research-v1`）

```json
{
  "schema": "idea-research-v1",
  "run": {"date": "2026-09-24", "started": "2026-09-24T05:15:00+08:00", "finished": "2026-09-24T05:41:00+08:00",
          "model": "opus", "status": "ok", "reason": "", "searched_checkpoints": 17, "new_entries": 4},
  "status": {
    "ai-scissors": {
      "cp1": {"status": "supports", "reason": "一句中文理由（≤ 60 字，含關鍵數字）", "since": "2026-09-24",
              "checked": "2026-09-24", "keystone": true}
    }
  },
  "entries": [
    {"date": "2026-09-24", "idea": "ai-scissors", "checkpoint": "cp2", "verdict": "shaky",
     "summary": "一句中文（≤ 60 字）", "kind": "search",
     "event": "", "transcript_checked": false,
     "sources": [{"title": "原文標題", "url": "https://...", "type": "official"}]}
  ],
  "changes": [
    {"date": "2026-09-24", "idea": "ai-scissors", "checkpoint": "cp2", "keystone": true,
     "from": "supports", "to": "shaky", "reason": "一句中文", "review": "sonnet 同意：……"}
  ]
}
```

- `kind`：`search`（主動搜尋）、`earnings`（到期事件讀新聞稿，`event` 填 `due.label`）、`transcript`（逐字稿補查）、`reverify`（週一全面複查）。
- `sources[].type`：`official`（公司、政府、交易所）、`data`（TrendForce、Cloudflare Radar 等數據）、`media`。`sources[].read`：`full`（讀到原文）或 `snippet`（只讀到搜尋摘要）。
- `entries`、`changes` 新的放最前面，只留最近 365 天。同一個網址不重複寫。
- 每個 active 想法的每個查核點都要出現在 `status` 裡，沒資料就 `no_data`。

## 中文寫法

`summary`、`reason` 照 `zh-analyst-prose`：一句一個主數字，白話，不用比喻，全形標點，中文與數字、英文之間半形空格；寫事實和出處，不寫「值得注意的是」這類套話。

## 硬規則

- 描述器紀律：不寫買賣建議、目標價、部位建議。
- 不改 `ideas.json`、想法頁、早報任何檔、routine 排程本身。
- 不得 `--no-verify`，不得 `git add -A`，不得 `--amend`。
- 數字只能來自讀到的原文；讀不到就寫讀不到，不猜。
- 付費牆讀不到全文時，只用標題與摘要，並在 `summary` 註明「只讀到摘要」。
