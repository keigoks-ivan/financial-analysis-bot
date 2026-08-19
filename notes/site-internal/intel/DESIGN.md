# 情報收件匣 `/intel/` 設計 v0（2026-08-19）

持有人目標：把主站打造成投資用的資訊搜集平台。**先整合資訊，整合好再跟持股連結，一步一步來。** 外部資訊要盡量收（產業動態、市場異常、經濟情勢、地緣政治），每天自動更新，**走 Claude Code 月租額度**，**用最省資源的方式**。

## 0. 已有、不重做

| 已有 | 路徑 | 在新架構裡的角色 |
|---|---|---|
| 個股樞紐 251 檔 | `/t/`（`scripts/build_ticker_hubs.py`） | 第 2 層的個股頁，加「最新動態」區塊即可 |
| 全站搜尋 | `/search.html`＋`assets/search-index.json` | Phase 4 擴到 intel 卡片 |
| 每日簡報 | `/briefing/`（06:15 TPE） | 平行存在；未來可引用當日 intel 卡 |
| 市場監測／偵測警報 | `/monitor/`、`/detective/` | **當成 intel 的來源之一**（市場異常類） |
| 持倉週掃、thesis monitor | `/pm/`、`position-thesis-monitor` agent | 第 3 層接這裡 |
| 產業 ID、供應鏈 | `/id/`、`/supply-chain/` | 第 2 層主題頁的骨幹 |

缺的：**外部資訊收件匣**（最大的洞）、**主題頁**、搜尋只蓋六成頁面。

## 1. 三層架構（一步一步疊）

```
第 3 層  /my/            持股 → 只看相關情報 ＋ thesis 警示          （Phase 3）
第 2 層  /t/ /theme/     個股頁加動態；新建主題頁；總經／地緣頁      （Phase 2）
第 1 層  /intel/         每天自動抓外部資訊 → 卡片 → 按 ticker／主題歸檔（Phase 1，先做）
```

## 2. 最省資源五原則（設計約束，不是建議）

1. **機械層做 90% 的事，零 token**：抓取、去重、關鍵字預過濾、渲染頁面全部是 Python，跑在 GitHub Actions（免費）。
2. **LLM 只做四件事**：一句話摘要、為什麼重要、打標（ticker／主題／類別）、重要度。輸入只給「標題＋來源摘要（≤300 字）＋URL」，**不餵全文**。
3. **一天一批、分兩道**：關鍵字預過濾後 ≤200 條給 haiku 分類，haiku 留下的 ≤60 條給 sonnet 摘要。超過上限按來源權重截斷並在頁面標示「今日略過 N 條」。
4. **永不重送**：`seen.jsonl` 記 URL hash；標題 Jaccard 相似度 >0.8 視為同一則只送一次。
5. **JSON 是唯一真相**：`docs/intel/data/YYYY-MM-DD.json` 落地後，所有頁面由 template 靜態渲染，改版面不需要重跑 LLM。

6. **模型分工（持有人指示：用不同模型搭配）**——每一步用「剛好夠」的那一檔，最貴的只碰真正需要判斷的地方：

| 步驟 | 模型 | 為什麼 | 頻率 |
|---|---|---|---|
| 抓取／去重／關鍵字預過濾／渲染 | **無**（Python） | 不需要理解語意 | 每天 |
| 第一道分類：這條跟投資有沒有關、屬哪一類、命中哪些 ticker／主題 | **haiku** | 便宜、快；分類題 haiku 夠；把 200 條砍到 60 條 | 每天 |
| 摘要＋「為什麼重要」＋重要度 | **sonnet** | 要一點判斷力，但不需要深推理 | 每天，只跑 haiku 留下來的 |
| 每週回顧：這週哪些卡合起來改變了某主題／某檔的判斷 | **opus** | 跨卡片、跨天的綜合判斷，真正需要推理 | 每週一次，只讀 importance≥2 的卡 |
| Phase 3 持股警示：importance=3 命中持股 → 對照 thesis kill metric | **opus** | 決策級，錯不得 | 事件觸發，很少 |

**額度估算（月租）**：haiku 200 條 × ~120 tok ≈ 2.4 萬／天；sonnet 60 條 × ~230 tok ≈ 1.4 萬／天；opus 每週一次 ~5 萬。**一個月合計 ~150 萬 token，其中 opus 只佔 ~20 萬**。對 Max 方案是零頭。

## 3. 資料流（每天）

```
06:00 TPE  GitHub Actions  intel-fetch.yml（免費）
           scripts/intel/fetch.py
             ├─ 抓 RSS／EDGAR／FRED／公開資訊觀測站 → raw/YYYY-MM-DD.jsonl
             ├─ 去重（URL hash ＋ 標題相似度）
             ├─ 關鍵字預過濾：命中 ticker 清單（/t/ 的 251 檔＋別名）或主題關鍵字才留
             └─ 輸出 pending/YYYY-MM-DD.json（≤80 條，含 title/source/url/snippet/matched_tags）
           commit → push（觸發 pages 沒關係，只是 JSON）

06:30 TPE  Claude Code 排程（月租額度）
           claude -p "$(cat scripts/intel/PROMPT_classify.md)" --model haiku
             ├─ 讀 pending/今天.json（≤200 條）
             └─ 每條判：relevant?／category／tickers／themes → 留下 ≤60 條
           claude -p "$(cat scripts/intel/PROMPT_summarize.md)" --model sonnet
             ├─ 讀 haiku 留下的 ≤60 條
             └─ 每條產出 {summary_zh, why_zh, importance} → docs/intel/data/YYYY-MM-DD.json
           （每週日另跑一次 opus：weekly-review，讀本週 importance≥2 的卡 → docs/intel/weekly/YYYY-Www.html）
           python3 scripts/intel/render.py   ← 零 token
             ├─ docs/intel/index.html（今日＋近 7 天）
             ├─ docs/intel/t/{TICKER}.html 或直接注入 /t/{TICKER}.html 的「最新動態」區塊
             ├─ docs/intel/theme/{slug}.html
             └─ 更新 search-index（Phase 4）
           git commit --only docs/intel/ → push（用 worktree 隔離，避免踩並行 session）
```

**排程跑在哪（Phase 1 第 0 步要驗）**：
- 預設：**本機 launchd** 跑 `claude -p`（確定走月租）。Mac 要醒著；用 `pmset repeat wakeorpoweron MTWRFSU 06:25:00` 叫醒。
- 備選：GitHub Actions 用 `claude setup-token` 產的長效 token（**先查目前條款是否允許 CI 用月租 token**，允許才用；優點是不靠 Mac）。
- 兩者的 prompt／腳本完全相同，只差觸發點。

## 4. 卡片 schema（`docs/intel/data/YYYY-MM-DD.json`）

```json
{
  "date": "2026-08-19",
  "generated_at": "2026-08-19T06:41:00+08:00",
  "model": "sonnet",
  "skipped": 12,
  "cards": [
    {
      "id": "sha1(url)[:12]",
      "title": "原標題",
      "source": "Reuters",
      "url": "https://…",
      "published": "2026-08-18T22:10:00Z",
      "category": "company | industry | market | macro | geo",
      "tags": {"tickers": ["NVDA","2330.TW"], "themes": ["ai-datacenter"]},
      "importance": 3,
      "source_tier": "T2",
      "summary_zh": "一句話。",
      "why_zh": "為什麼跟投資有關（1–2 句，不重複摘要）。"
    }
  ]
}
```
`importance`：3＝會改變某檔 thesis 或某主題判斷；2＝值得記進脈絡；1＝背景。頁面預設只展開 3 與 2。

## 5. Phase 1 來源清單（聚焦版）

**公司層（只收 /t/ 的 251 檔＋持股）**
- SEC EDGAR full-text search API（8-K、10-Q、13D）— 免費、按 ticker 查
- 公開資訊觀測站重大訊息（台股）— MOPS 有 RSS／可爬
- 公司 IR RSS（先做持股，其餘 Phase 2 補）

**產業動態（5 個主題）**
- 主題：`ai-datacenter`、`semis`、`power-grid`、`macro-rates`、`taiwan-geo`
- 來源：TechNews、DigiTimes、SemiAnalysis、Tom's Hardware、EE Times、Utility Dive
- 每個主題一組關鍵字清單（`scripts/intel/themes.yml`），預過濾用

**市場異常**
- 站內 `docs/monitor/data/alerts.json`、`docs/detective/` 輸出 — 直接讀，零抓取成本

**經濟情勢**
- FRED 更新 RSS（CPI、NFP、FOMC 相關 series）、Fed 新聞稿 RSS、BLS 日曆

**地緣政治**
- Reuters World、AP Top News、CFR、國防部即時軍事動態、陸委會新聞稿
- 只留命中 `taiwan-geo` 或提到 251 檔任一的

## 5b. 小道消息（持有人 2026-08-19 確認要收）

**收，但分等級、標清楚、追蹤命中率。** 卡片 schema 加 `source_tier`：

| tier | 定義 | 例 |
|---|---|---|
| T1 官方 | 公司自述、監管申報 | SEC 8-K、MOPS、法說會逐字稿 |
| T2 主流媒體 | 有編輯把關 | Reuters、Bloomberg、工商時報 |
| T3 專業圈 | 具名、有可查紀錄的分析師／產業媒體 | 郭明錤、SemiAnalysis、DigiTimes 供應鏈消息 |
| T4 小道 | 匿名、論壇、社群 | PTT Stock 板、Reddit、X 爆料帳號 |

規則：
1. T3／T4 卡掛「傳聞」badge，頁面上與事實分區。
2. **單靠 T4 不得 importance=3**；需 T3 以上或 ≥2 個獨立來源才可升。
3. 傳聞每日上限 20 條。
4. **命中率追蹤**：`docs/intel/data/rumors.jsonl` 存每則傳聞（來源帳號／板、日期、主張）；每週 opus 回顧比對是否被 T1／T2 證實 → 維護 `rumor_sources.json` 的 hit-rate，預過濾權重據此自動調整。這是這條線最有價值的產出。
5. 抓取可行性：PTT／Reddit／Substack 可機械抓；X 官方 API 付費、免費管道不穩，Phase 1 跳過，之後以「持有人手動貼連結進 inbox」補。
6. **不抓** Telegram／LINE／付費群組；**只收公開傳聞，不收任何內線資訊**。

## 6. 頁面（Phase 1 只做前兩個）

1. `/intel/` — 今日情報：按重要度分組，每張卡＝標題＋一句摘要＋為什麼重要＋標籤 chip（點 chip 進個股頁／主題頁）；下方近 7 天摺疊。
2. `/t/{TICKER}` 加「最新動態」區塊 — 該 ticker 最近 30 天的卡（由 render.py 注入既有 hub 頁的固定標記區）。
3. `/intel/theme/{slug}` — Phase 2。
4. 首頁「最近發布」feed 加 intel 一種 kind — Phase 2。

## 7. 後續階段

- **Phase 2 主題頁**：`/theme/{slug}` ＝ 該主題的 ID＋供應鏈＋intel 卡＋相關 ticker；總經／地緣專區。
- **Phase 3 持股連結**：`/my/` 或 cockpit 加「持股相關情報」；importance=3 且命中持股 → 觸發 `position-thesis-monitor` 或 email。
- **Phase 4 搜尋擴充**：search-index 納入 intel／learn／briefing；tag 從 ticker 擴到 theme。

## 8. 不做的事（省資源）

- 不抓全文、不存全文（只存 URL＋snippet）
- 不用 opus 跑日常分類與摘要（opus 只做每週回顧與持股警示）
- 不做即時／盤中更新，一天一批
- 不做向量搜尋，關鍵字＋tag 就夠
