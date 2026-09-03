# industry-analyst skill 重架構評估（v3.0 → v4 提案）— 2026-09-03

> 目的：持有人要求「最少 token 下達到品質最高的產出、白話、深入淺出、整份報告邏輯要通」。本筆記是評估與提案，**未動任何 skill 檔**；實作待持有人拍板。
> 證據來源：skill 全套檔案（SKILL.md／templates／pre_publish_check／references）、唯一一份 v3.0 產出（`docs/id/ID_AIInferenceEconomics_20260720.html`）、其 critic 與 prepublish 報告、`knowledge/calibration_id_20260707.md`、`knowledge/rule_ledger.md`、冷讀者報告（見 §3）。

---

## 0. 一句話結論

**skill 的問題不在章節順序，在「規則層」與「流程層」**：八段 sell-side 動線本身是對的，但它被三件事拖垮——①規則地層堆疊（九個版本疊在同一檔、兩套章節編號並用、約百條規則）讓 writer 每跑一次先付 ~23 萬字元的指令；②v3.0 研究引擎把一份 ID 的成本推到 DD 的 20–40 倍，結果是 v3.0 上線六週只產出一份；③「16,000–22,000 字、低於 14,000 視為偷懶」的字數地板與「擴展靠文字」八槓桿，把篇幅當深度獎勵，而 critic 抓到的 7 條 🔴 全在**沒算的量化模組**——規則多、字多，但承重的數字是空的。白話目標則被 template 內建的英文 sell-side 標籤與 inline claim 標記直接打架。

處方＝**重架構 skill，微調報告骨架**：砍字數地板改「必交決策物清單」、兩套編號合一、研究引擎分級（引擎降為旗艦專用）、critic 餵摘錄、16 道 gate 收成一支 script、SKILL.md 從 86KB 壓到 ~30KB、閱讀線全白話而把分析師紀律（claim tag／T 級／推導行）移入折疊層。

---

## 1. 現況量測

### 1.1 每跑一次 ID，writer 先讀多少指令

| 檔案 | 位元組 | 備註 |
|---|---:|---|
| SKILL.md | 86,277 | 1,060 行；含 v2.0–v3.0 全部沿革與理由 |
| templates/report_template.md | 64,552 | 其中 CSS 約 19KB |
| pre_publish_check.md | 49,194 | 869 行；16 道 gate，多數「人工複核」 |
| templates/schema_fields.md | 13,528 | §0–§9 舊編號字數配額 |
| references/id-meta-schema.md | 12,888 | 寫 id-meta 前必讀（Gate 13'） |
| references/judgment-playbook.md | 7,418 | 20 條，觸發索引式 |
| **寫稿時合計** | **~234KB** | 約 8–10 萬 tokens 量級的指令，尚未開始研究 |
| id-review SKILL.md（critic 端） | 57,066 | critic 再付一次；且目前餵整份 HTML |

對照：stock-analyst v15 走過同樣的路（v14.7 拆 references/、v15 篇幅預算指令＋Token 紀律），ID 這邊只做了 v2.6 的拆分，沒做 v15 那一輪。

### 1.2 規則數量（約百條，大量重疊）

- QC-1～QC-20（20）＋ QC-M1～M6（6）
- Pre-Publish Gate 1／2／2.1／3／4／5／6／7／8／9／10／11／12／13／13'／14／15／16（18）
- 深度擴展八槓桿（8）＋ 新增分析模組（7）＋ 判斷手冊（20）
- id-review 端：cornerstone 6 條＋ V2-1～V2-15
- 同一件事多處重覆：QC-2＝Gate 6；QC-3＝Gate 8；QC-5≈QC-9；QC-12＝Gate 10-3；QC-M3≈Gate 12 priced_in；QC-15 claim tag 又在 template 硬規則再講一次。

### 1.3 兩套章節編號並用

v3.0 把呈現改成八段（summary／thesis／debates／mechanics／valuation／risks／stocks／appendix），但 SKILL.md 其餘 800 行、schema_fields、QC、Gate、判斷手冊、id-review 全部仍用 §0–§9「內容模組編號」，靠一張映射表翻譯（「寫 §5 前讀判斷手冊＝寫 3.4 裁決前讀」）。writer 與 critic 每次都要在腦中做兩套對照；v3.0 首發 prepublish 報告裡就出現藍本用 `id="industry"` 而非 `id="mechanics"`、TOC 連錯的實例。

### 1.4 v3.0 唯一產出的位元組結構

`ID_AIInferenceEconomics_20260720.html`：

| 段 | 位元組 | 可見字元 | 表格 |
|---|---:|---:|---:|
| summary | 7,606 | 2,644 | 1 |
| thesis | 6,298 | 2,591 | 0 |
| debates | 9,515 | 3,364 | 0 |
| mechanics | 32,100 | 12,318 | 6 |
| valuation | 3,822 | 1,206 | 1 |
| risks | 5,575 | 1,823 | 1 |
| stocks | 8,058 | 2,750 | 1 |
| appendix | 8,327 | 2,917 | 1 |
| **全檔** | **113,453** | **30,129** | **11** |

- 讀者看得到的字只占 27%，其餘 73% 是標記與 CSS（head＋CSS＋id-meta JSON 合計約 34KB，占 30%；CSS 本身約 19KB 每檔 inline）。
- 可見字 30K，是自家前身 v2.3 精煉版（54KB／11.1K 可見字）的 **2.7 倍**，也超過 skill 自訂 16–22K 上緣。
- 同一主題兩版裁決一字未變（split／Phase II／mid 是 critic 修回來的），多出來的字沒有換到新結論。

### 1.5 研究引擎成本（v3.0 Gate 15）

- changelog 自述：「聚焦單題 deep-research 實測約 590 萬 tokens，全 ID 引擎估 2–4 倍」→ **一份新 ID 約 1,200–2,400 萬 tokens**。
- prepublish 報告：Kimi K3 一個子題「104 agents 三票制」。
- 對照 DD 全套實測 62–65 萬 tokens／份。**ID ≈ 20–40 份 DD 的成本。**
- 結果：v3.0 於 2026-07-20 上線後，六週內 `docs/id/` 只新增這一份；其餘 62 個 commit 全是 nav／白話工程。skill 實質停擺。

### 1.6 critic 與 gate 在首發實際抓到什麼

id-review（sonnet）7 條 🔴：conviction 機器欄與綠卡矛盾、sd_verdict 該 split 填 shortage、資本週期三指標零數字、熱產業時鐘三問未答、TAM 只有 top-down、priced-in 四條分歧零分位溯源、kill 表套套邏輯且無市場撮合價。**全部落在量化決策模組與機器欄同步**，沒有一條是「字太少」。

16 道 gate 同時有 3 道機械 fail（表格 11>10、T1 占比 36.4%<60%、推導 regex 誤判），prepublish 報告花了大段篇幅解釋「繼承自藍本、如實回報不調門檻」——機械閘產生的是文書工作，不是判斷品質。

### 1.7 校準結果告訴我們品質槓桿在哪

`calibration_id_20260707.md`（77 份可結算）：全部的錯集中 **shortage × Phase II（7/25，超額中位 −7.5%）**，balanced 38/41。結論是 sd_verdict 量物理供需不量可投資性，缺的軸是 priced-in／循環位置／擁擠度。v2.6 補了 `priced_in` 欄位，但 v3.0 首發的 priced-in 仍無估值分位、無 26 週漲幅交叉——**校準點名的那一軸，在報告裡還是最薄的一段**（它被拆成四張 debate 卡各一句話，沒有自己的位置）。

---

## 2. 診斷（七條）

1. **地層堆疊，不是規格**：SKILL.md 是一份「就地 changelog」——v2.0 的合併理由、v2.1 的字數上修、v2.2 三句話、v2.4 純度、v2.5 kill、v2.6 priced_in、v2.7 手冊、v3.0 八段，每層都留著「WHY」與舊 HTML 樣板。寫稿時真正需要的是「現行規格」，理由該在 changelog。
2. **字數地板獎勵填充**：「低於 14,000 視為偷懶」＋「擴展靠文字不靠表格」八槓桿，與 DD 那邊 2026-07-30 被實測推翻的邏輯同款（memory `feedback_render_hygiene_no_process_theater`：floor 不該獎勵填充）。v3.0 產出 30K 字、critic 卻抓到量化模組空白，就是地板失效的證據。
3. **白話目標被 template 打架**：規則層寫「寫給聰明的非專業者、術語首現白話」，template 卻硬編 Key Call／Investment Thesis／Key Debates／Portfolio Implication／Priced-in／Exhibit／Disclosures／Sector View NEUTRAL／Method: Deductive Inference，讀者第一屏看到 `sub_group：compute_demand`、`NC#2 為 AT_RISK`、`Structural Jevons Paradox 反轉這個直覺`。2026-09-01 白話條款只是在可讀性表加了一列，沒改 template。
4. **流程劇場漏到讀者眼前**：inline claim tag（🟢 [F: …]／🔵 [X: base 很可能…]）、T1/T3-A 等級、「NC#」編號、「v3.0 呈現版 · 原始 thesis 建立於」、evidence-fold 裡整段 CLAIM TAXONOMY 說明——這些是給 critic 的，不是給讀者的。全站規則（`_plainlang_styleguide.md` 禁流程劇場）已明文禁止。
5. **研究引擎成本結構錯置**：五軸 fan-out × 3–5 輪＋每個承重數字 3 個 skeptic（10–15 個數字＝30–45 個 agent）＋completeness critic，全部常設。但 id-review critic 本來就會自己 WebSearch 查證承重數字（首發 critic 逐檔核實純度、逐條核實中國模型數字），skeptic 層與 critic 查證重疊。真正不可替代的只有 completeness critic（獨立腦找缺席變數）與 Axis E 機械掃描。
6. **驗證靠人工重讀**：16 道 gate 半數標「人工複核」「spot-check」，writer 得把自己剛寫的 113KB 讀回來好幾次；DD 那邊已立「自驗一律 grep／python 單行、禁 Read 回整份 HTML」，ID 沒有。critic 端 id-review 也還是整檔餵（DD 實測改摘錄省 63%）。
7. **裁決重述四次、priced-in 沒有家**：裁決出現在 rating strip、NOW 一行、thesis 段「供需裁決」段落、3.4 裁決；PM 行動出現在 summary 行動框與 thesis 綠卡兩處；而校準點名最重要的 priced-in／位置軸被切碎塞在四張 debate 卡裡各一句。骨架要動的就這兩處：合併重述、給 priced-in 一個獨立小節。

---

## 3. 冷讀者報告（opus 冷讀，不查事實只看讀者體驗與邏輯流）

對照 v3.0 `ID_AIInferenceEconomics_20260720.html` 與 v2.3 `ID_WaferFabEquipment_20260430.html`。摘要（全文在 session 紀錄）：

**篇幅去向**：正文 26,300 字（v2.3 為 17,317，**多 52%**）。增量 58% 落在 3.3 中國 open-weight 一節（5,211 字，等於 3.1＋3.2＋3.4＋4 四節相加），其餘是 **24 塊固定樣板**（10 個「怎麼讀」＋6 個「對投資的意義」＋8 個「本節參考來源」）與 Debates 前置後各段的復述。

**同一判斷講了 13 次**：「毛利分層／不是同一多頭」出現在 lede、Key Points 兩點、NEXT 磚、ACTION 磚、Key Call、thesis box、PM 行動、Debate 2、3.2 怎麼讀、估值傳導正文與折疊、個股估值面總結、implication、The One Line。兩處幾乎逐字重複（「盯便不便宜的人問錯問題……」在 §1 與 Key Points 各一次）。3.2 一張三層表的內容被正文、怎麼讀、因果機制、折疊「死亡螺旋」講了四遍。

**前後矛盾三處**：①第一屏「Sector View NEUTRAL」vs One Line「押 frontier＋垂直整合 ASIC」與 §1「核心押 GOOGL＋AVGO」，NEUTRAL 全篇無一句解釋；②NEXT 磚「毛利 ~48% 待升 70%」vs Debate 3「升 70% 是假設非事實」；③資料時點分裂——主體 2026-04-30 資料窗、3.3 自註 2026-06／07，拼接留給讀者。

**Key Debates 只有 1.5 條是真辯論**：Debate 1、2 的「市場認為」是一句媒體標語（「媒體框 token 崩價＝通縮利空」），無數字無最強版本；真正 steel-man 被搬到 5.3 每條兩行。Debate 4（中國模型）兩造都有數字，是全站最好的辯論段——但四條裡只有一條做到。

**決策有用度（致命缺口）**：
- **全份沒有任何估值數字**——沒有 P/E、沒有倍數區間、沒有「現價 price 了多少」；「未被充分 price」出現 6 次，零量化。v2.3 同一問題有答案（「Street 給 25–30x cyclical 倍數……重估空間 1–1.5 turn」）。
- **情境無權重**：TAM 三情境 $700B／$850B／$450B 沒有機率；全篇唯一機率「~28%」憑空出現在方括號註記裡。v2.3 有 55／22／23＋每情境 5 條確認訊號。
- **證偽表打不了臉**：四條 kill 有兩條不可觀測（Silicon Data 指數無現值無查詢路徑；frontier lab 毛利＝私募不揭露，報告自己免責聲明承認）。v2.3 每條有現值、口徑、來源、頻率（「KLA 營收÷WFE <9%（現 9.7%；分母口徑不同勿混）」）。**v3.0 證偽表比 v2.3 退步。**
- 拿得到的：避開清單非常具體（純 GPU 雲轉售、無差異 API、第三方 open-weight serving 商）；GOOGL 錯價論可檢驗；三檔純度推導做得對。

**流程劇場殘留（原文）**：「（QC-18）」、整段「CLAIM TAXONOMY v1」、「sub_group：compute_demand｜Method：Deductive Inference + Scenario Analysis」、「v3.0 呈現版」與頁尾「industry-analyst v3.0」、「NC#1 INTACT／NC#2 AT_RISK」（NC 全篇未定義，AT_RISK 出現 6 次）、「stock-analyst 自動讀本表 + id-meta related_tickers」、改稿痕跡「須拆為……」、「本表資料時點晚於報告主體資料窗」。

**冷讀者的 60KB 骨架**：Page-1 決策卡（含三條帶現值 kill）→ Key Call 只講一次（之後全文只准「見 §」）→ Debates 兩造都帶數字、steel-man 住這裡 → 需求（三情境帶權重）→ 供給 → **估值與錯價（新增：核心檔現行倍數 vs 命運，回答「現在貴不貴」）** → 風險證偽一張表（現值／來源／頻率／觸發後動作）→ 個股。附錄只留白話定義、先例表、來源總表。正文 ~13,000 字。

**一句話**：v3.0 把一個好判斷講到讀者能背，卻沒回答讀者唯一真正要問的問題（現在這層貴不貴、我怎麼知道我錯了）。

## 4. v4 提案

### 4.1 設計原則（五條）

1. **必交物取代字數**：品質＝一張「必交決策物」清單是否每件都真算、真有來源；篇幅只設上界警告，不設地板。
2. **一套編號**：八段錨點是唯一名字，§0–§9 內容模組編號全數退役（含 schema_fields、QC、Gate、手冊、id-review 全部改寫）。
3. **閱讀線全白話，紀律進折疊**：正文一句不帶 claim tag／T 級／推導行；這三樣是 critic 與機器的資產，收進每節 `evidence-fold` 或 data-attribute。
4. **研究分級**：預設走「單 writer（opus）＋單一封閉式採集 agent（sonnet）＋completeness critic」；五軸 fan-out＋3-skeptic 引擎只給旗艦級新母題，且須持有人逐次開啟。
5. **機械閘一支 script，判斷閘一個 critic**：能用程式驗的（錨點、id-meta、表數、kill 同步、T1 占比、威脅卡、`_full` 禁產、推導行）全進 `scripts/check_id.py`；要判斷的（cornerstone 查證、cross-ID 對帳、量化模組是否真算）全進 id-review 職責書。

### 4.2 報告骨架（八段錨點不改，改「誰只講一次」）

| 段 | 錨點 | 白話標題（主）／英文（小字） | 這段唯一的工作 | 可見字目標 |
|---|---|---|---|---:|
| 第一頁 | `summary` | 一頁看完 | **決策卡，不是摘要**：一句 KEY CALL＋五格燈號（供需／時鐘／信心／已定價／5 年需求倍數，全白話）＋三句話（現在／未來／怎麼做）＋**三條帶現值的 kill**＋四個行動。PM 行動只住這裡 | 700–1,000 |
| 1 | `thesis` | 核心判斷 | thesis **完整講一次**（含唯一一張承重表）；之後全文禁止復述，只准「見 §1」 | 1,200–1,800 |
| 2 | `debates` | 市場哪裡看錯 | 3–4 張分歧卡（含 1 張替代威脅卡）：市場最強版本（帶數字）→我們認為→已定價多少→看什麼訊號分勝負→⚠ 什麼發生就錯。**steel-man 住在卡內**，不另立節 | 2,000–2,800 |
| 3 | `mechanics` | 機制與供需 | 3.1 需求（TAM 三情境＋上下游對帳）／3.2 供給（玩家三欄矩陣＋利潤池＋成本曲線或省略理由）／3.3 為什麼是現在（S 曲線三句＋kingmaker）／3.4 裁決（資本週期 ≥2 數字＋三視野表＋時鐘雙閘）。主題需要時加一節「供給新變數」 | 4,000–5,500 |
| 4 | `valuation` | 現在貴不貴 | unit economics＋估值傳導＋**priced-in 位置節**：核心 🔴 檔現行倍數 vs 歷史帶、估值分位、26 週漲幅／擁擠度交叉、現價隱含成長→收斂 low/mid/high。校準點名的軸集中一處 | 1,200–1,800 |
| 5 | `risks` | 我怎麼知道我錯了 | **一張表**：kill ≥3 條（每條現值＋來源＋查核頻率＋領先幾季＋可否操縱＋破線後姿態；≥1 條市場撮合價）＋催化劑雙路徑。監測點不再另列 | 900–1,300 |
| 6 | `stocks` | 誰受影響 | 🔴🟡🟢 表（純度推導行）＋非顯而易見受益者＋營運槓桿最大者＋「特徵非推薦」句；**不寫估值面總結**（已在 §4） | 800–1,200 |
| 附錄 | `appendix` | 背景、歷史、來源 | 白話定義、歷史轉折（日期＋量化錨）、類比先例表＋cycle 統計、**來源總表（單一，附段落欄與 T 級）**、claim 標記說明 | 1,200–2,000（折疊） |

- 主閱讀線 **11,000–14,000 可見字**；HTML **≤ 70KB**（含 inline CSS）或 **≤ 55KB**（CSS 外掛 `docs/assets/id-v4.css`，站內已有 `docs/assets/imq-base.css`／`supply-chain/assets/engine.css` 先例）。超過只警告不擋。
- **唯一敘述規則**：核心判斷只在 §1 完整出現；裁決只在第一頁一句＋3.4 推導；PM 行動只在第一頁。`check_id.py` 用 12-gram 重複掃描（DD 那邊 2026-07-31 已用同法量測）標出重複段。
- **資料窗唯一**：整份報告一個資料窗日期，寫在第一頁；refresh 若只更新部分章節，仍須把第一頁與 kill 表現值一併更到同一窗。

### 4.3 必交決策物（12 件，取代 QC-1～20／QC-M1～M6／深度八槓桿）

| # | 必交物 | 真做的判準（critic 抽查） | 機器可驗 |
|---|---|---|---|
| D1 | 三句話＋最重要的判斷 | 行動句允許「都不買／等回調」；KEY CALL 不重述裁決 | now_state／future_state／action 落 id-meta |
| D2 | 供需裁決 | 資本週期三指標至少 2 個**有數字**（capex/折舊、ROIC vs WACC、lead time）；三選一或 split＋detail | sd_verdict／sd_verdict_detail |
| D3 | 投資時鐘 | Phase＋換相「必要 ∩ 充分」雙閘，充分須兩個獨立訊號 | clock_phase |
| D4 | TAM 三情境＋對帳 | top-down vs bottom-up 兩條路徑都有數字，差 >20% 說缺口；bull/bear 由「改了哪個假設」推出；表末 5 年倍數 | demand_5y_multiple |
| D5 | 玩家矩陣＋利潤池 | 三時間欄；利潤池是總額占比非毛利率；無 source 的 % 改定性 | — |
| D6 | 成本曲線 | 週期型必做；結構成長型一句省略理由 | — |
| D7 | 分歧卡 3–4 張 | 每卡引 ≥1 共識來源；≥1 張 `data-debate="external-threat"`；每卡有可量化判別訊號＋證偽句 | 威脅卡標記 |
| D8 | 現在貴不貴（priced-in 位置節） | **核心 🔴 檔現行倍數**（Fwd P/E 或 EV/S）vs 自身歷史帶＋估值分位（有來源或自算附窗口）＋26 週漲幅／擁擠度交叉＋現價隱含成長；收斂為 low/mid/high。零估值數字＝未交 | priced_in |
| D9 | kill 表 ≥3 條 | **每條附現值＋as-of＋查核來源與頻率**（比照 macro-analyst v1.1「查不到現值不准上表」）；≥1 條市場撮合價；每條標領先幾季、可否被操縱、破線姿態；閾值不得與公司 guidance 同源；不可觀測的指標不得上表 | kill_metrics[] 逐條對齊 |
| D10 | 催化劑 ≥5 | 日期（季度可）＋指標＋達成／落空雙路徑 | — |
| D11 | 個股表 | 純度每檔一行推導；🔴 附 mcap_bucket；「特徵非推薦」句 | related_tickers[]（purity_pct／mcap_bucket） |
| D12 | 歷史錨點 | 每個轉折 YYYY 或 YYYY-MM＋一個量化錨；≥2 輪 cycle 的產業附統計表 | 附錄 regex |
| D13 | 唯一敘述 | 核心判斷、裁決、PM 行動各只完整出現一次；分歧卡「市場認為」須是最強版本帶數字，不得是媒體標語 | 12-gram 重複掃描 |

保留不變的紀律（搬去 references，不在核心）：來源四級與 T1 優先（floor 改為**依主題型別**：硬體／製造 60%、快速演變或 macro 型 45%，首發已證明一刀切 60% 對時事型主題結構性卡稿）、spurious specificity 禁令、詞彙級機率、Q×4 禁推估、freshness 半衰期。

### 4.4 研究流程分級

| 級別 | 觸發 | 流程 | 估算成本 |
|---|---|---|---|
| **標準（預設）** | 一般新 ID、裁決級 refresh | ①writer（opus）定 thesis sketch＋列「必答封閉問題」（含 Axis E 五條機械查詢）→ ②spawn **一個** sonnet 採集 agent 回結構化證據包（數字＋URL＋as-of；查不到回報查不到）→ ③writer 自做判斷性搜尋（分歧、priced-in、時鐘）並寫稿 → ④completeness critic（sonnet，只知主題不讀論證，列一階變數對照草稿）→ ⑤`check_id.py` → ⑥id-review critic（sonnet，餵摘錄）→ 修 → 發布 | 約 1.5–2.5M tokens（DD 的 2.5–4 倍，合理：ID 一份餵多檔 DD） |
| **旗艦** | 持有人明說「旗艦」或母題級新主題 | 標準流程＋五軸 fan-out＋承重數字 3-skeptic | 維持 12–24M，但每次須持有人開啟 |
| **措辭級 refresh** | 裁決不動、只更新數字 | 不跑採集 agent、不跑 completeness；只 `check_id.py`＋critic 摘錄 | <0.5M |

理由：id-review critic 本來就對承重數字做獨立 WebSearch（首發實證），3-skeptic 層與之重疊；completeness critic 便宜且不可替代（獨立腦）。這是把 Gate 15 由「常設」降為「旗艦專用」——**rule_ledger 該列的 kill condition 寫的是「兩輪校準」**，現在只有一份首發、零校準輪，提前降級須持有人拍板（見 §6 問題 1）。

### 4.5 critic 與自驗的 token 紀律（照抄 DD v15 已驗證的做法）

- id-review 餵摘錄：第一頁＋分歧卡＋2.4 裁決＋priced-in 節＋kill 表＋個股表＋id-meta（約占全檔 45%），不餵 mechanics 全文與附錄；critic 需要時自己 grep 指定段。
- 自驗一律 `check_id.py` 或單行 python；禁 Read 回自己寫的整份 HTML。
- 前一版 ID 只讀 id-meta＋kill 表＋分歧卡標題，不讀全文（防錨定亦省 token）。
- 最終回報 ≤300 字＋INDEX 行；prepublish 報告改為 `check_id.py` 的機器輸出，不再手寫 13KB 文書。

### 4.6 skill 檔案結構與大小目標

| 檔 | 現況 | 目標 | 做法 |
|---|---:|---:|---|
| SKILL.md | 86KB | ~28–32KB | 只留：定位（10 行）、骨架表、12 必交物、白話與流程劇場禁令、研究分級、寫稿順序、發布 9 步、路由表；理由全去 changelog |
| templates/report_template.md | 64KB | ~30KB（CSS 外掛後 ~12KB） | 中文主標題＋英文小字；砍 thesis 段；砍 inline claim tag 佔位；evidence-fold 只留來源清單與推導行 |
| pre_publish_check.md | 49KB | **刪除** | 機械閘→`scripts/check_id.py`；判斷閘→id-review 職責書 3 條 |
| templates/schema_fields.md | 13.5KB | 刪除（併入骨架表） | 舊 §0–§9 配額退役 |
| references/sources.md | — | ~12KB | 來源四級表、中文來源表、券商規則、搜尋捷徑（自 SKILL.md 搬出） |
| references/research-queries.md | — | ~5KB | Axis A–E 查詢模板，只給採集 agent 讀 |
| references/judgment-playbook.md | 7.4KB | 不動 | 已是觸發索引式 |
| references/id-meta-schema.md | 13KB | 不動 | validator 是權威 |
| id-review SKILL.md | 57KB | ~35KB | V2 清單改對八段錨點；加「餵摘錄」與 3 條判斷閘 |

寫稿時載入合計 ~234KB → **~85KB**。

### 4.7 白話層規則（落進 template，不只落進規則表）

- 每段主標題中文白話句，英文 sell-side 名降小字（「市場哪裡看錯 · Key Debates」）。
- rating strip 五格用白話：供需＝「短缺／平衡／過剩／分裂」、時鐘＝「擴張中段」等相位白話、已定價＝「還沒反映／部分反映／大多反映」。
- 正文禁：claim tag、T 級、NC#、內部欄位名（sub_group 值）、方法論標籤（Deductive Inference）、版本戳散文。
- 術語首現括號白話，照 `_plainlang_styleguide.md` 句式 3；新術語先查對照表。
- **固定樣板塊大砍**：「怎麼讀」只在表格需要判讀時寫一句（表格右欄已寫方向就不寫）；「對投資的意義」每段最多一個且不得復述 §1；「本節參考來源」八塊折疊改為附錄**單一來源總表**（去重、附段落欄與 T 級，機器仍可算 T1 占比）。冷讀實測這 24 塊是 v3.0 的主要填充來源。
- 圖只在有數據時畫：零數據的 ASCII 示意圖（「一條上一條下」）不畫。

---

## 5. 不動的東西

- **id-meta 資料契約**：20 支下游 script（picks／detective／kill_watch／rotation／ticker_hubs／q.py／position-thesis-monitor…）讀 `related_tickers`／`sd_verdict`／`clock_phase`／`conviction`／`priced_in`／`kill_metrics`／`demand_5y_multiple`／`now_state`…，schema 零改動，`validate_id_meta.py` 不動。
- **存量 188 檔**不批次遷移（v3.0 既定政策）。
- **模型路由**：writer opus、critic sonnet（CLAUDE.md 路由表「維持不動」）。採集 agent 用 sonnet（證據蒐集非冷讀）。
- **判斷手冊 20 條**與其 rule_ledger 審計制。
- **威脅卡必備席（Gate 16）**：成本最低的 forcing function，保留為 D7 的一部分。

---

## 6. 待持有人拍板的問題

1. **Gate 15 引擎提前降級**：rule_ledger 寫的 kill condition 是「兩輪校準」，現在零輪。提案是降為旗艦專用而非刪除（引擎規格保留在 references/），算「降級」不算「撤回」——可接受嗎？
2. **CSS 外掛**：ID 家族改讀 `docs/assets/id-v4.css` 可省每檔 19KB 與 template 19KB；代價是頁面離線不成立、與其他家族（DD 仍 inline）不一致。要做嗎？
3. **情境權重**：QC-14 禁精準機率（防「60% 機率 Rubin 2027 H2 量產」式假精確），但冷讀者指出 v2.3 的三情境權重（55／22／23）＋確認訊號清單是可決策性的關鍵，v3.0 拿掉後反而退步。提案：只在 TAM 三情境與三視野表允許 **5 點步進的主觀權重**（標明主觀、加總 100），散文事件機率維持詞彙級。這是判斷類規則修改，須登記 rule_ledger——同意嗎？
4. **T1 floor 分型**：60%（硬體製造）／45%（時事快變、macro 型）——分型由 writer 自報還是由 `taxonomy.md` 的 mega 決定？

---

## 7. 實施順序（拍板後）

1. 先寫 `scripts/check_id.py`（把 pre_publish_check 的機械部分程式化），對現有 v3.0 檔跑一次確認等價。
2. 改 template（白話標題、砍 thesis 段、tag 進折疊、CSS 外掛可選）。
3. 重寫 SKILL.md（核心 ~30KB）＋新 references；changelog 補 v4 條目與本筆記連結。
4. 改 id-review（八段錨點、餵摘錄、三條判斷閘）。
5. rule_ledger：Gate 15 降級登記（kill condition 改寫）、字數地板 KILL、加一提刪一（提名 QC-1 🟡 比例 ≤20%——v3.0 debate 卡結構下已無 🟡 bullet 可數，0 命中的閘是裝飾）。
6. 用一份中等規模主題實跑（非 AI 硬體，避開校準失效格），量 token 與可見字，對照本筆記 §1 表。
