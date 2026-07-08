# macro-analyst skill v1.0 — 總經深度報告（macro ID）

## 【定位】

與 `industry-analyst`（產業 ID）平行的**總體經濟深度研究** skill：輸入一個總經主題（「美國財政赤字與利率上限」「美元週期」「AI capex 宏觀傳導」「全球流動性循環」「通膨結構轉變」），執行四軸 web 研究，輸出一份敘事為骨、指標為錨、以「機制 → 歷史 base rate → 現況數據 → 傳導鏈 → 情境樹 → 證偽表 → 組合 read-through」為骨架的 HTML 報告，上站 `docs/macro/`。

**憲法（描述器紀律）— 本 skill 的生日就在「短期轉折預測已判死」的裁決之後（2026-07-08）：**
- 輸出是**環境判讀與情境準備**，不是擇時訊號。禁止「預測轉折時點」「短期大跌將至」類結論；禁止買賣指令句。
- 依據：本站實證——日線 vs 週線 0/96、六訊號儀表＝描述器（出場準但回場遲滯，機械擇時輸 B&H）、SKEW 零資訊、殖利率曲線時滯不可操作、NFCI 只對 2008 有效。macro 變數對市場的可用形態＝**改變左尾分布的描述**與**情境機率**，不是方向擇時。
- 對組合的語言＝三軌／GRP／regime 撥盤（「Off 期間不加新倉」層級），禁 IRR 排序、禁個股指令。

**與 industry-analyst 的邊界**：主題有明確產業供需錨（產能、玩家、利潤池）→ `industry-analyst`；主題是跨資產／政策／利率／匯率／財政／流動性／人口與生產力層級 → 本 skill。灰色地帶（如「AI capex 宏觀傳導」）：若分析單位是 GDP／盈餘總量／資金流而非特定產業鏈 → 本 skill，並在 §8 連結相關 ID 不重做其內容。

## 【觸發語】

「總經研究 {主題}」「macro {topic}」「{主題} 總經報告」「總體經濟分析 {主題}」「宏觀分析 {主題}」「{主題} 宏觀傳導」「macro report {topic}」。純資訊問題（「現在利率多少」）不觸發。

## 【路徑】

- 報告：`docs/macro/MACRO_{Slug}_{YYYYMMDD}.html`（Slug 用 CamelCase 英文，如 `FiscalDominance`、`DollarCycle`）
- 索引：`docs/macro/index.html`（新報告 insert 卡片至列表最上方；首份報告產出後移除 `.empty-state`）
- Critic 報告：`notes/site-internal/macro/_critic_{Slug}_{YYYYMMDD}.md`
- 上站：`https://research.investmquest.com/macro/`

## 【章節骨架：§0 決策層 + §1-§8】

### §0 決策摘要層（thesis box，給掃讀者）
- **一句話判斷**＋ stance 三選一（對風險資產：順風／中性／逆風）——反騎牆，split 情境須在 §5 用情境樹呈現而非騎牆
- 時間尺度（horizon，月為單位）＋機率詞彙級（沿用 industry-analyst 機率詞彙表，不寫偽精確百分比）
- 對三軌組合的 read-through 摘要（2-3 句，描述器語言）
- 證偽表摘要（top 2-3 kill metrics）＋ refresh_due（預設 +3 個月）

### §1 白話定義與機制（深入淺出入口）
這個總經力量是什麼、為何現在重要；歷史雙錨點（沿用 DS-9 規則：一個結構錨＋一個近期錨）。

### §2 歷史框架與 base rate
過去 N 次同類週期的統計（次數、持續期、資產反應的分布不是均值）；歷史類比的失效條件明文。

### §3 現況數據錨（指標面板）
核心指標 ≤8 行表＋敘述；**每個數字帶 T1 來源與 as-of 日期**。T1 for macro＝Fed／FRED／Treasury／BLS／BEA／CBO／IMF／BIS 原始數據與官方文本；賣方宏觀研究列 T3。

### §4 傳導鏈（本報告的脊椎）
總經變數 → 流動性／折現率／企業盈餘 → 資產價格的因果鏈，每一環標傳導時滯與歷史彈性；沿用推導可追溯原則（每個推導可從來源數字重算）。

### §5 情境樹
2-3 情境（base／bull／bear），機率詞彙級；各情境下的資產含義（股／債／美元／商品方向與幅度區間）；反偏差防線：bear 情境不可 <20% 除非明文論證。

### §6 共識對帳與 priced-in
市場現在定價了什麼（期貨曲線、breakeven、共識預測）vs 本報告判斷；分歧點必須可驗證。

### §7 Catalyst 時間表＋證偽表
未來 6-12 個月的資料發布／政策節點（接催化劑日曆語言）；證偽表＝每條 kill metric 帶門檻、查核頻率、資料源——**說不出證偽條件的判斷不准寫進 §0**。

### §8 對本站組合的 read-through
三軌／GRP／regime 語言；明文連結 `/regime/`、`/crowding/`、相關 `docs/id/` 報告（連出不複製）；結尾固定一句描述器定位聲明。

## 【硬規則】

1. **描述器紀律**（見憲法）——self-review 時 grep 掃描禁語（「將大跌」「轉折將至」「建議賣出」「立即減倉」類）。
2. **中文全形標點**；賣方研究口吻；無鷹架語言（「本版補齊」等）。
3. **來源紀律**：沿用 industry-analyst 來源階層（T1-T4 定義、QC-7 衝突處理）；T1 占比 floor **45%**（macro 例外檔，比照 QC-6 macro 例外先例）＋警語標註。
4. **Claim taxonomy／🟡 判斷 ≤20%／機率詞彙級／§末 aside 來源系統**：沿用 industry-analyst 對應規則，不重抄（見該 skill SKILL.md）。
5. **篇幅**：目標 60-90KB；文字 ≥60%、表格 ≤8 張；深度來自傳導鏈與 base rate 統計，不是灌指標。
6. **macro-meta JSON**（嵌報告 `<script type="application/json" id="macro-meta">`）：
   ```json
   {"schema":"macro-v1","topic":"...","slug":"...","date":"YYYY-MM-DD",
    "horizon_months":N,"stance_risk_assets":"順風|中性|逆風",
    "kill_metrics":[{"metric":"...","threshold":"...","freq":"...","source":"..."}],
    "related_ids":[],"refresh_due":"YYYY-MM-DD"}
   ```
   Validator 後補（建 DB 先單獨做、consumer 接線另案——先手動保證欄位齊）。

## 【研究流程（四軸，零素材啟動）】

- **Step 0**：主題確認＋邊界判定（industry vs macro，見上）＋讀 `docs/regime/` 最新一期與 `docs/crowding/` 最新一期當現況底料（站內先讀，不重做）。
- **Axis A — 歷史與 base rate**（3-5 輪 WebSearch/WebFetch）：同類週期的歷史統計。
- **Axis B — 政策與流動性**（3-5 輪）：央行／財政的官方文本與數據（T1 優先）。
- **Axis C — 實體與盈餘傳導**（3-5 輪）：對 GDP／企業盈餘／各資產類的傳導證據。
- **Axis D — 市場定價與 positioning**（3-5 輪）：期貨曲線、共識、COT（可引 crowding 資料層）。
- **寫稿順序**：§3 → §4 → §2 → §5 → §6 → §7 → §8 → §1 → §0（數據錨先立，決策層最後收斂）。

## 【發稿流程】

1. 寫稿完成 → **self-review gate**：數字皆有來源與 as-of／全形標點／禁語掃描／§0-§8 齊／macro-meta 欄位齊。
2. **強制 cold-review critic**（比照 industry-analyst Step 8.7）：spawn general-purpose agent（sonnet），checklist 7 條——①§0 stance 與 §5 情境樹一致；②傳導鏈每環有來源；③base rate 統計非 cherry-pick；④證偽表可操作（門檻＋頻率＋源）；⑤描述器紀律無違反；⑥priced-in 分歧真非共識；⑦與 regime/crowding 現況無未解釋矛盾。報告存 `notes/site-internal/macro/_critic_{Slug}_{YYYYMMDD}.md`。大錯必修，cosmetic 記錄即可。
3. index.html insert 卡片（比照 push-earnings 模式，skill-appended）。
4. **預設停下複審**——用戶說 push 才 commit（報告＋index＋critic md 三檔一 commit），push 前 `git pull --rebase`。

## 【治理登記】

- 判斷類規則已登記 `knowledge/rule_ledger.md`：①§0 stance 三選一反騎牆＋證偽表強制；②tool-level kill condition（90 天無任何決策引用→降級）。
- 審計節奏：隨裁決校準輪（下輪 2026-10）。
- 產出頻率預期：於需求觸發，估每月 0-2 份；**不做週期性自動產出**（描述器三頁已覆蓋高頻資料層，本 skill 是低頻深度層）。
