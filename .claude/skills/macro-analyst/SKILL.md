# macro-analyst skill v1.2 — 總經深度報告（macro ID）

**v1.2（2026-07-10）**：八份實跑＋七輪 critic 的完整校準（素材：`notes/site-internal/macro/_v12_calibration_notes.md`）。新增八條 sourcing 紀律（見【數據紀律】一節）：非美／無官方統計主題的 T1 條款、T3 現值取捨、觸及紀錄強制查證、證據新鮮度標籤、carry-forward 數字二次查證、無 sourced base rate 出口、衝突數字割捨協議、數據窗標準動作；critic spawn 歸屬明文化。累計錯誤型態譜系（全部「真數字錯上下文」、幻覺 0）：①過時數字 ②錯標系列/口徑 ③時間標籤錯 ④引信無現值 ⑤站內引用美化 ⑥舊證據當新引信 ⑦當局行動漏記。stance 鑑別力議題（八份全中性）不動條文，forward 對帳日 2027-01。

**v1.1（2026-07-09）**：首跑四份 critic 實證驅動——①證偽表每條必附現值＋as-of；②站內引用忠實性。均為 sourcing／格式紀律，非判斷類規則，不入 rule_ledger。

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
- 證偽表摘要（top 2-3 kill metrics）——**每條必附現值＋as-of**，讓「引信與門檻的距離」在 §0 就可讀；＋ refresh_due（預設 +3 個月）

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
未來 6-12 個月的資料發布／政策節點（接催化劑日曆語言）；證偽表＝每條 kill metric 帶門檻、查核頻率、資料源、**現值＋as-of**——**說不出證偽條件的判斷不准寫進 §0；查不到現值的 kill metric 不准上表**（現值缺席＝無法判斷引信距離門檻多遠，甚至可能已半觸發而不自知——v1.1 教訓）。該指標若近 12 個月內曾瞬時觸及或逼近門檻，必須明文記載該次事件。

### §8 對本站組合的 read-through
三軌／GRP／regime 語言；明文連結 `/regime/`、`/crowding/`、相關 `docs/id/` 報告（連出不複製）；結尾固定一句描述器定位聲明。

## 【硬規則】

1. **描述器紀律**（見憲法）——self-review 時 grep 掃描禁語（「將大跌」「轉折將至」「建議賣出」「立即減倉」類）。
2. **中文全形標點**；賣方研究口吻；無鷹架語言（「本版補齊」等）。
3. **來源紀律**：沿用 industry-analyst 來源階層（T1-T4 定義、QC-7 衝突處理）；T1 占比 floor **45%**（macro 例外檔，比照 QC-6 macro 例外先例）＋警語標註。
4. **Claim taxonomy／🟡 判斷 ≤20%／機率詞彙級／§末 aside 來源系統**：沿用 industry-analyst 對應規則，不重抄（見該 skill SKILL.md）。
5. **篇幅**：目標 60-90KB；文字 ≥60%、表格 ≤8 張；深度來自傳導鏈與 base rate 統計，不是灌指標。
6. **站內引用忠實性**：引用站內姊妹報告（macro／ID／DD／regime／crowding）的結論時，必須忠於原文的裁決語氣與保留——**原文標為「分歧／未解／低信心」的論點，不得轉述為「一致／已確認」**；引用時保留原文的限定詞。違反＝大錯（會讓站內文件互相洗白，比外部錯引更危險）。
7. **macro-meta JSON**（嵌報告 `<script type="application/json" id="macro-meta">`）：
   ```json
   {"schema":"macro-v1","topic":"...","slug":"...","date":"YYYY-MM-DD",
    "horizon_months":N,"stance_risk_assets":"順風|中性|逆風",
    "kill_metrics":[{"metric":"...","threshold":"...","freq":"...","source":"..."}],
    "related_ids":[],"refresh_due":"YYYY-MM-DD"}
   ```
   Validator 後補（建 DB 先單獨做、consumer 接線另案——先手動保證欄位齊）。

## 【數據紀律（v1.2，八份實跑校準）】

錯誤型態譜系（八份累計，幻覺 0）：全部是「**真數字、錯上下文**」——過時／錯標系列／時間標籤錯／舊證據當新引信／當局行動漏記。以下八條全部針對這個譜系：

1. **非美／轉引 T1 條款**：T1 以**口徑**為準（官方數字＝T1），取得路徑若為轉引（官方頁不可達、經媒體轉發）須在來源標註；權威性與可驗證性分離者（如準官方序列只有轉載可查）保守降 T3。
2. **結構性 T1 天花板聲明**：主題天然無官方統計者（FX 部位、AI capex、私人流動性指數類），floor 仍 45%，但須在來源總表明文「本主題 T1 結構性天花板」＋逐項標註，區別於偷懶。
3. **T3 現值取捨**：kill metric 現值只有 T3 源時——若該指標是裁決變數，仍上表但標源級＋aside 註明「現值監控依賴轉引源」；非裁決變數則換代理指標或下表。
4. **觸及紀錄強制查證**：「近 12 個月是否觸及門檻」不得憑寫稿記憶；**「政策當局行動」型 kill metric（干預／會議決策／監管變更）必須查一次官方 release**（YenCarry 教訓：MoF 創紀錄干預 ¥11.73 兆漏記，原稿誤寫「無干預」）。
5. **證據新鮮度標籤**：觸及紀錄必附事件日期；「既存 tell（已亮燈 N 個月）」與「新事件」分開標，**不得把舊證據寫成新引信**（AICapexMacro 教訓：17 個月前的折舊年限縮短被標成近期觸發）。
6. **Carry-forward 數字強制二次查證**：政策利率／利差／官方預測 vintage（IMF WEO、SEP 類）——這幾類「極易從記憶帶舊值」的數字，self-review 時強制 WebSearch 確認 current vintage（DollarCycle 教訓：IMF 增長差用了兩天前已被取代的舊 vintage；YenCarry 教訓：政策利差 325bp 過時）。
7. **無 sourced base rate 的正式出口**：主題無量化文獻時允許質性合成（如「托底 5/5、再通脹 1.5/5」），但必須明文標註「非 sourced 統計」＋列出合成所依個案（ChinaEconomy 先例轉正）。
8. **衝突數字割捨協議**：多源分歧顯著且未解（如三源差 150bp）→ 降格為區間或加權替代口徑並標註，不押單一數字；序列斷檔／口徑改版一律進「標籤精確聲明」段（報告 footer 標配）。

## 【研究流程（四軸，零素材啟動）】

- **Step 0**：主題確認＋邊界判定（industry vs macro，見上）＋讀 `docs/regime/` 最新一期與 `docs/crowding/` 最新一期當現況底料（站內先讀，不重做）。
- **Axis A — 歷史與 base rate**（3-5 輪 WebSearch/WebFetch）：同類週期的歷史統計。
- **Axis B — 政策與流動性**（3-5 輪）：央行／財政的官方文本與數據（T1 優先）。
- **Axis C — 實體與盈餘傳導**（3-5 輪）：對 GDP／企業盈餘／各資產類的傳導證據。
- **Axis D — 市場定價與 positioning**（3-5 輪）：期貨曲線、共識、COT（可引 crowding 資料層）。
- **寫稿順序**：§3 → §4 → §2 → §5 → §6 → §7 → §8 → §1 → §0（數據錨先立，決策層最後收斂）。

## 【發稿流程】

1. 寫稿完成 → **self-review gate**：數字皆有來源與 as-of／全形標點／禁語掃描／§0-§8 齊／macro-meta 欄位齊／**證偽表每條現值齊**（缺現值的 metric 補查或下表）／**站內引用逐條回對原文**（開原檔比對裁決語氣，分歧不得寫成一致）／**carry-forward 數字二次查證**（政策利率／利差／預測 vintage，數據紀律第 6 條）／**當局行動型 kill metric 查官方 release**（數據紀律第 4 條）。
2. **強制 cold-review critic**（比照 industry-analyst Step 8.7）：**必須是獨立 agent**——由主 session 或 writer spawn 皆可（實跑兩型皆有效），但 writer 不得自任 critic、critic 用不同 model tier（sonnet）、結果與修復記錄一律存檔。checklist 7 條——①§0 stance 與 §5 情境樹一致；②傳導鏈每環有來源；③base rate 統計非 cherry-pick；④證偽表可操作（門檻＋頻率＋源＋**現值**；並查該指標近 12 個月是否曾觸及門檻而報告未載）；⑤描述器紀律無違反；⑥priced-in 分歧真非共識；⑦與 regime/crowding 現況無未解釋矛盾＋**站內引用忠實抽查 ≥2 處**（開被引原檔逐字比對）。另固定用 WebSearch 抽查 5-6 個關鍵數字（首跑實證：主要錯誤型態是「真數字但過時／錯標系列」，非幻覺）。報告存 `notes/site-internal/macro/_critic_{Slug}_{YYYYMMDD}.md`。大錯必修，cosmetic 記錄即可。
3. index.html insert 卡片（比照 push-earnings 模式，skill-appended）。
4. **預設停下複審**——用戶說 push 才 commit（報告＋index＋critic md 三檔一 commit），push 前 `git pull --rebase`。

## 【治理登記】

- 判斷類規則已登記 `knowledge/rule_ledger.md`：①§0 stance 三選一反騎牆＋證偽表強制；②tool-level kill condition（90 天無任何決策引用→降級）。
- 審計節奏：隨裁決校準輪（下輪 2026-10）。
- **stance 鑑別力 forward 對帳（2027-01）**：首八份 stance 全為中性——若六個月後八份對應的資產路徑截然不同，代表 stance 無資訊量、真正載資訊的是證偽表，屆時裁決是否把 stance 降格、「引信距離」升格（素材與方法見 `notes/site-internal/macro/_v12_calibration_notes.md`）。
- 產出頻率預期：於需求觸發，估每月 0-2 份；**不做週期性自動產出**（描述器三頁已覆蓋高頻資料層，本 skill 是低頻深度層）。
