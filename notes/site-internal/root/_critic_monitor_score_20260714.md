# Cold-review critic — 跨資產壓力分數（docs/monitor/index.html 新增區塊）

日期：2026-07-14
Scope：`git diff docs/monitor/index.html`（唯一改動檔，CSS + `<section id="sec-score">` + IIFE 末尾 JS，約 299 行新增）；對照 `docs/monitor/data/score_history.json` 的 `method` 區塊（含實際 series 資料抽查）。
Reviewer 未寫任何一行本次新增內容，純冷讀。

## 資料層事實（用於比對，非新增規則）

- `schema: monitor-score-v1`，`window_td: 756`，`min_obs: 252`
- 5 桶／21 成員：vol(5, all rising) / credit(5: baa10y·ccc_oas·hy_oas·ig_oas rising, hyg_lqd falling) / liq(3, all rising) / rates(2, all rising) / app(6, all falling)
- `min_members`：vol/credit/liq/app = 2，rates = 1
- `bucket_rule`："桶需 ≥min_members 成員出分；合成需 ≥3 桶；coverage＝可得成員/21"
- `bands`：calm[0,20] / normal[20,40] / warming[40,60] / tense[60,80] / extreme[80,100]
- `ice_oas_note`：ICE BofA HY/IG/CCC OAS 受 FRED 免費端限縮為約 3 年滾動窗（2023-07 起、~2024 年中暖機後才貢獻）；credit 桶長史錨＝baa10y（1986 起全史），與 hyg_lqd 讓桶自 2008-04 起亮
- `excluded_note`：DXY／黃金／BEI／曲線斜率等雙向語意 series 明文排除
- 實際抽查：`series` 中 credit 首次非 null＝**2008-04-09**（與方法論文字宣稱的「2008-04」精確吻合）；`s`／`spx` 全歷史（7935 筆，1994-12-29～2026-07-13）無 null；21 = 5+5+3+2+6 核對無誤。

## verdict 表

| # | 檢查項 | Verdict |
|---|---|---|
| 1 | 描述器紀律（憲法級） | **FAIL（blocker）** — 見下 |
| 2 | 中文標點全形 | PASS |
| 3 | 方法論忠實性 | **FAIL（cosmetic）** — 見下 |
| 4 | 誠實性（coverage 早年低可被發現） | PASS |
| 5 | 無鷹架語言 | PASS |
| 6 | JS 防禦 | PASS |
| 7 | 一致性（band 命名/顏色） | PASS |

## FAIL 詳情

### 1. 描述器紀律 — FAIL（blocker）

- 免責句本身文字沒問題：`docs/monitor/index.html` 新增行 105（diff 行號，對應 `.score-disclaim`）—「本分數為環境描述器，非擇時訊號——衡量當下跨資產壓力在歷史中的分位位置，不構成進出場指令。與首頁風險儀表同家族。」用詞正確、無買賣/加減倉指令語言（全文掃過「買/賣/加倉/減倉/進場/出場/擇時/建議/應該」等關鍵字，僅這句本身以否定句出現，無其他違規）。
- 問題在**位置**：這句話只出現在 `<details class="method score-details">`（diff 行 99，無 `open` 屬性）內，預設是**折疊**的——使用者必須主動點開「方法論」才看得到。整個 `.score-hero`（44px 大字分數 + 彩色 band chip，diff 行 78-85）與圖表（含分級帶底色，diff 行 86-98）預設可見時，**完全沒有任何免責句在旁**。
- 這與同家族頁面的既有慣例不符：`docs/crowding/index.html` 第 224-226 行把「定位：本監測是描述器（describer），不是擇時訊號」放在 h1/副標題正下方的常駐 `.mandate` div（無需點開任何東西），並在頁尾 disclaimer 區塊（第 274-277 行）重複一次；`docs/regime/index.html` 第 242 行同樣做法。`docs/monitor/index.html` 本頁自己在第 289 行也有一句常駐（非折疊）的頁級描述器聲明，但那句話描述的是「全球指數／…／近 100 條 series 的日更明細…統計規則…標出異常」，是舊有的異常偵測功能，**沒有提到新的「跨資產壓力分數」這個構件**，不能算是這個新區塊專屬的免責揭露。
- 大數字＋色彩分級帶最容易被讀者當「訊號」解讀，恰是憲法級規則要防的情境；把唯一專屬免責句藏進預設折疊區，等於預設狀態下沒有免責聲明。
- **建議修法**（文字建議，不代表本次要改檔）：把 `.score-disclaim` 那句話複製一份到 `.score-hero` 上方或 `<h2>跨資產壓力分數</h2>` 正下方，做成常駐可見的小提示條（比照 crowding/regime 的 `.mandate` 樣式），方法論摺疊區內可以保留原句作為完整版說明，但不能是唯一位置。

### 3. 方法論忠實性 — FAIL（cosmetic）

- 其餘所有可查核宣稱逐字比對 `method` 區塊與實際 series 皆吻合（756 交易日窗、5 桶成員與方向、桶 ≥2/利率 ≥1、合成 ≥3 桶、分級帶 20/40/60/80、coverage÷21=21 個成員、信用桶 2008-04 起亮〔已用實際資料驗證到 2008-04-09〕、ICE OAS 3 年窗限制與 Baa10Y 長史錨的敘述幾乎逐字對應 `ice_oas_note`）。
- 唯一缺漏：`method.min_obs = 252`（滾動視窗最少需要的觀測值數，用來決定 series 何時才開始出分）**在新增文案中完全沒有出現**（全文搜尋「252」/「min_obs」/「最少」/「至少」等關鍵字皆無結果，diff 行 101 的方法論段落只提到「756 個交易日（約 3 年）滾動視窗」這個窗長，沒有另外交代最低觀測值門檻）。這不是矛盾（不影響現有敘述的正確性），是遺漏，故列 cosmetic 而非 blocker。
- **建議修法**：在 diff 行 101 第一段方法論文字補一句，例如「…滾動視窗（每條 series 至少需 252 個交易日觀測值方開始計分）…」。

## 未列為 FAIL 但值得留意

- 誠實性（項 4）：coverage 揭露段（diff 行 104）只點名 credit 桶自 2008-04 起才亮，沒有同樣點名 app 桶（實際資料顯示 app 桶首次非 null 在 1999-12-21，也是部分歷史缺口）。checklist 只要求「方法論或 UI 任一處有交代即可」，credit 桶的說明已滿足最低要求，故判 PASS，但若要更完整可比照 credit 桶的寫法也提一句 app 桶暖機時間。
- JS 防禦（項 6）：確認過 `fetch(...).then(...).then(function(sd){ ...; initScoreSection(sd); }).catch(function(){ 隱藏 section })` 這個鏈式寫法——`initScoreSection` 呼叫在第二個 `.then` 內部，若其內任何一步（`renderScoreHero`/`renderScoreMethod`/`renderScoreChart`）丟出例外，會變成 promise rejection，被最後的 `.catch` 接住並把 `#sec-score` 重新隱藏，是穩健寫法；且 `initScoreSection` 把 `sec.style.display=""` 放在函式最後一行，任何提前拋出的例外都不會執行到「顯示」那一行，屬雙重保險。`renderScoreHero` 對 `last.b[k]` 為 `null`/`undefined` 有明確 guard（bar 留空、數字印 "—"，不會印出 "null"/NaN）。整段 JS 防禦合格，未發現需修的問題。
- 一致性（項 7）：band 命名（calm/normal/warming/tense/extreme → 平靜/常態/升溫/緊張/極端）與顏色（`--pos`/`--accent`/`--warn`/`--tense`/`--neg`）在 CSS class（`.band-chip.b-*`）、JS 顏色函式（`bandColorVar`）、圖表底色映射（`bandFillMap`）、tooltip（經 `bandOfScore`+`BAND_LABELS`）、方法論文字（診斷行 103）之間完全一致，只有一套命名，未發現分歧。
- 中文標點（項 2）：對新增 HTML 與 JS 字串常量做了程式化掃描（正規表示式抓「中文字緊接半形 ,.:;」與中文字緊鄰半形括號），無命中；全形「，。：；「」／＝·（）」使用一致，數字/英文/單位維持半形不變。
- 無鷹架語言（項 5）：新增文案唯一出現的 "v1" 字串是機器 schema key `"monitor-score-v1"`（比對用，非渲染給使用者），非鷹架語言洩漏；「coverage 誠實協議」這類「誠實」措辭與本頁既有第 372 行「資料缺口誠實列出，不以舊值或估值填充」的既定站內慣用語一致，非新洩漏。

## OVERALL = FIXES_REQUIRED
