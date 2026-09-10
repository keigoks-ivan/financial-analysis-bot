# DD v18 設計稿：從「填滿模板」倒過來成「解關鍵疑點」

2026-09-10。供持有人與 Codex 冷讀，**不是給模型執行的 prompt**。本輪未改任何 skill／prompt／schema／程式，未跑模型、未跑 DD。

## 〇、持有人拍板的方向（原文）

> - 每檔固定回答核心問題：怎麼賺錢、競爭優勢、成長、現金與資本配置、估值、可能看錯在哪。
> - 深入研究由關鍵疑點觸發：哪個未知會改變買不買的判斷，就往哪裡查；不是每個模組都一樣深。
> - 查證與計算不能省，重複作文可以省：資料來源、重要反證、數字一致性保留；同一結論不用換五個地方再寫。
> - 證據已足以支持判斷時就停；缺關鍵證據就明說不確定，而不是繼續堆篇幅。

另一句：「事情不要搞得太複雜。」本稿以此驗收——**v18 只改三件事：查多少、何時查、寫幾遍。不新增系統、不新增閘、不新增模型。**

## 一、六個核心問題的最小交付物

**結論：每題交「一組數字＋一句判斷＋來源」，不交表格模板。**表格是需要時的產物，不是入場費。

1. **怎麼賺錢**——>10% 營收段占比、最新一季毛利／營益率（法說親讀＋10-K／10-Q）；判斷句＝賺誰的錢、錢卡在哪一節點。**不預設 TAM／SAM／滲透率表。**
2. **競爭優勢**——一條機制（不是清單）＋一個可證方向：對最強同業的 ROIC spread 或最大客戶份額方向，附 12 個月內 sourced data point；判斷句＝`moat.trend`。同業財務對照只在該方向是爭點時展開。
3. **成長**——量、價、併購還是回購；三年共識 EPS CAGR（標家數與來源）＋內生上界（ROIIC × 再投資率，**全份唯一推導處**）＋缺口歸因一句；判斷句＝`runway_post_y5`。
4. **現金與資本配置**——FCF／NI 轉換率、SBC／營收、近三年現金去向四分、債務到期與利率；判斷句＝`capalloc_grade`。十年併購全史只在連續收購型或本期有重大交易時展開。
5. **估值**——`peg`／`percentile_5y`（估值燈與 screener 直讀）＋情境樹三支的 EPS 路徑、終端倍數、機率；判斷句＝現價要求未來 X 才划算，我信不信。IRR／EV5Y／AR／Max DD 機械算。
6. **可能看錯在哪**——`premortem.blind_spots[]` 三視角各一條以上（論點失敗／論點成功但股東經濟變差／價格已反映太多），每條帶 `evidence`／`assumption`／`consequence`／`ruling`／`watch`。**全份唯一反證居所**；steelman、trap 依據、`plain.fears` 引用不重寫（WP-D A1）。

## 二、疑點觸發機制：用決策敏感度定義，不靠作者自陳

**結論：「該往哪深挖」機械算出來，不由判斷 agent 自我宣告。**三訊號取聯集，上限 4 條：

- **(a) 矩陣邊界距離（主）**——`dd_decision.py` 是純函數。對 `decision_inputs` 22 欄**逐欄單獨擾動**（bool 翻面、enum 上下一檔、數值 ±20%）重跑矩陣，記下**哪幾欄單獨翻動就改變 verdict**＝承重欄，其餘不是。
- **(b) 證據等級最低者**——每題支撐 finding 取最低等級（L1 已實現／L2 sourced 前瞻／L3 敘事）並讀該軸 `status`；承重欄靠 L3 或 `status="none"` 撐者優先。
- **(c) 前份漂移最大欄**——`drift_watch` 20 欄中變動幅度最大、且 `cause` ≠「價格變動」者。

輸出 `open_questions[]`（2–4 條，新增 optional 欄位），每條四格：`field`（承重欄位路徑）｜`if_x_then`（未知若往 X 走）｜`verdict_shift`（裁決從 A 變 B）｜`how_to_settle`（要什麼證據才能定）。**深挖只對這幾條做**；清單外的軸維持輕掃結果，不加深、也不因為淺就標不適用。

## 三、流程形狀：兩個變體與推薦

### 甲｜三段不變，stage 0 輕掃全軸、疑點在草判之後深查

- **Stage 0（sonnet）**：12 軸全掃**不變**，每軸 1 輪，批次 2 軸／批放寬到 4–6 軸／批 → coverage spawn 6→2–3；數字 1；逐字稿摘要多數命中永久快取 → 0–2。**spawn 8–12 → 4–6。**
- **Judge 一（Fable 短模式）**：只交 `decision_inputs` 草值＋`scenario.json`＋提名的疑點，**不交完整 schema**。
- **Probe（零 LLM ＋ sonnet）**：機械敏感度得 (a)，合併 (b)(c) 與 Fable 提名成 `open_questions[]`；對其中 2–4 條 spawn **1–2 個 sonnet 深查 agent**，產物**併回 `evidence.json`**（不併回等於繞過 J1）。**防錨定**：深查 agent 只收到 `if_x_then` 與 `how_to_settle` 兩格問句，不收到草判 verdict。
- **Judge 二（Fable）**：輕掃包＋深查增量＋草值，一次寫定 `judgment.json`。**Stage 1G（opus）與快速版渲染完全不變。**

深查放在**判斷之後**——之前不知道哪裡承重。估計：spawn 5–7／檔；Fable 2 輪（首輪短，output 1–2 萬 token）；**成本 $11–13／檔**（現 $16.2：Fable $10→$6–8、sonnet $3.2→$2.5–3、opus $2 不動）。品質風險＝草判錨定（以問句隔離對沖）與輕掃漏軸（Stage 1G ⑤ 仍逐軸點名）。相容性**高**——三段結構、`gate_view` 抽取面、三支 validator 全不動。

### 乙｜單一 agent 帶搜尋工具，邊判斷邊查

spawn 1（＋opus 閘 1），Fable 多輪工具迴圈。每輪 `cache_read ≈ 當前 context`，20–40 個 tool call 下單調膨脹，而 Fable 是最貴那段——**成本很可能不降反升，$15–25／檔**且變異大。品質風險二，第二個致命：①採集紀律退化（`source`／`as_of`／`queries_run`／`direction` 是 sonnet 專職採集時被 validator 逼出來的）；②**J1 失去外部證據面**——負向證據能硬擋是因為證據包由別人給、每條 `dir=-` 必須交代；自己查自己判時，沒查到的負面證據不會出現在任何清單上。相容性**低**——沒有結構化 `evidence.json`，Stage 1G ①⑤⑦ 同時失去對照面。

### 推薦

**選甲。**理由：乙把「查證的人」與「下判斷的人」合成同一個，J1 與跨模型閘賴以成立的外部證據面消失，省的錢遠小於失去可稽核性的代價。

## 四、不能省的清單，各自放哪

**結論：以下七項全部原位保留，一項都不移進條件式。**

- **來源與 as-of**——留在 coverage finding 契約、`validate_evidence.py` 硬擋；輕掃降輪數不降舉證標準。
- **負向證據處置（J1）**——`validate_judgment.py` 不動。**新增一條接線**：深查產物必須併回 `evidence.json` 的 coverage，否則新查到的負面證據落在 J1 掃描面外。
- **數字一致性**——`dd_scenario`／`dd_decision`／`validate_judgment`＋`verify_dd_math`（已含 `BRIEF_*.html`）不動；改路徑或預設產物時逐一點名這四道加 pre-commit。
- **跨模型閘 Stage 1G**——位置、模型、嚴格度不動；只做 Codex #5 的**契約同步**：閘問的與機械層驗的須同一件事（漂移逐欄「有原因映射」而非「獨立條目」；搜尋問「切題充分」而非「湊兩條」）。需持有人批准動 gate 文案。
- **`decision_inputs` 22 欄與決策矩陣**——**完全不動**；它同時是 §二 (a) 的輸入面，瘦身會破壞疑點機制。
- **dd-meta 下游欄位**——`dca_role`／`max_dd_pct`／`ev5y_pct`／`irr_base_pct` 機械產生；`peg`／`percentile_5y`／`val_light` 判斷 agent 必交，**永不進條件式**。
- **特殊公司換尺**——archetype 路由與 gate-set 不動；金融／未獲利／循環／轉機不套一般模板。

## 五、停止規則

**結論：停止條件綁在 `open_questions[]` 上，不綁篇幅、不綁表格數。**三條全成立才停：①清單每條已擇一結案（拿到能改變答案的證據並落進 judgment，或明寫「取不到，維持不確定」附缺什麼）；②重跑敏感度後沒有新的「單欄翻動即改裁決」欄位跑出清單之外；③三支機械驗證與 J1 全過。上限＝**深查最多 2 輪**；仍有承重疑點未結案 → 走「尚不能裁決」。

**「尚不能裁決」的出口**：verdict enum 現為 進場／觀望／迴避（＋兩個進場·條件式），下游 screener／engine／picks／PM 直讀。**建議不新增 enum**：`dca_verdict` 落「觀望」，另加 dd-meta 選填 `undecidable=true`＋`undecidable_reason`，`rearm_trigger` 填缺的那條證據，brief 頁首顯示「尚不能裁決（暫記觀望）」。research 頁照渲染觀望、dd-screener 派生的「進場」欄本就不含觀望、engine 只用「迴避」做 veto，三處皆不受影響。**待持有人拍板**：要不要真加第四個 enum；**預設＝不加**——為每年少數幾份動五個消費端不划算，旗標可證偽也可事後升級。

## 六、schema 瘦身：184 → 約 110–120

**結論：刪的是「固定表格的子欄」與「同一結論的第二份抄本」，不刪下游契約與判斷輸入。**

**必須留（約 100–110 條）**三類：①決策鏈（`decision_inputs` 22＋`decision_out` 7＋`premortem`／`max_dd` 5＋`archetype.primary`，約 35）；②下游直讀（`triggers[]`、`thesis` 三組供 monitor、`valuation` 六欄供估值燈與 screener，約 40）；③判斷權威欄（`moat` 四欄、`runway_post_y5`、`capalloc_grade`、`meta`，約 25）。

**可整批降 optional 或刪（約 65–75 條）**：

- **(a) 固定表格的逐欄子項（25–30 條）**——`moat.competitors[]` 8 欄、`quality` 五張表、`industry` 兩欄。改法同 WP-D B 類：key 保留、可填未展開標記（`expanded:false`＋非空 `reason`），只在該區塊承重時必展開。
- **(b) `appendix_a` 與 dd-meta 重複的投影欄（8–10 條）**——`signal`／`val`／`ma`／`verdict`／兩個 upside 改由 `gen_dd_tables.py` 從權威欄機械投影，不由 Fable 再填一次；A3「同一結論不寫五處」的 schema 版，直接砍掉一段 output。
- **(c) `reasoning` 十模組全必填（3–5 條）**——改「承重數字模組必填」，機械判定＝該模組有數字流進 `decision_inputs`／`scenario`／dd-meta 者必填，其餘 optional。

數量是估計，實作時逐條對帳。**前提**：Codex WP-D 複審第 2、3 點（空標記可過、新反證來源可全空）須先修好，否則降 optional 只是放大漏洞。

## 七、遷移與驗證

**結論：不另建平行系統。**v18 是 v17 同一條管線的參數與寫作量調整——入口仍 `ddreport.py run`，stage 名稱不變，新增的只有 `judged` 內的 probe 子步驟；無 `--v18` 旗標、無 lite 版本，舊行為以 `--no-probe` 留退路。

**舊 `judgment.json` 相容**：新欄位全 optional；被降 optional 的欄位在舊檔仍存在，validator **只放寬不收緊**，19 份存查與 14 個 run 應維持現有 PASS／FAIL 不變（沿用 WP-D 驗收慣例：`dd_brief` 14 份重渲染逐 byte 相同）。舊檔不重跑、不回頭改。

**驗證＝同一份證據快照的成對比較**，不是拿歷史不同證據的 token 相減：①取 2 檔（一乾淨、一爭議），`DD_REPLAY_FROM` 固定證據與模型設定；②新舊各跑一次全套，比六項——總耗時／input／output／cost／`judge check` 重試次數／Stage 1G 🔴 數；③人工盲讀新版 `blind_spots[]` 對該 run 的負向 finding 清單，看有無**重要反證消失**；④delta 另設一例已知實質變動，驗「應改有改」。一次成對測試只能判斷有沒有效，**不能證明普遍不降品質**。

**kill condition（登記 `knowledge/rule_ledger.md` 的措辭）**：

> **v18 疑點觸發式深查**（2026-09-1x）。生日理由：v17 判斷段佔成本 63%、Fable 每檔 output 5–18 萬 token 而 `judgment.json` 僅 37KB，錢在重複作文與整包重寫。任一觸發即撤回該部分：(a) 連續 5 份中 Stage 1G 出現「證據包已有而判斷未接」或「覆蓋面缺軸」類判斷級 🔴 ≥2 例 → 撤回輕掃、恢復全軸標準深度；(b) 同一證據快照盲審發現因未列入 `open_questions[]` 而漏掉的承重反證 ≥1 例 → 該類疑點改強制展開並修正判準；(c) 成對比較顯示總成本未降 ≥20% 或 Fable output token 未降 ≥30% → 精簡無效，撤回全部新增複雜度、回 v17。加一提刪一候選：QC-51 同形狀 peer 對帳。

## 八、明確不做

**B10 倉位方案／PM 邊界**（屬決策方法與下游契約，要連 `dca_role` 與 PM 消費端一起處理）、**Bear 機率地板**（有 ledger 登記與 kill condition，不以「流程優化」名義撤）、**row 8a／8b**（100%／150% 門檻 PREREG 凍結至 2026-10 校準，本稿只提審計需求）、**拿掉 opus 閘**（Stage 1G 是兩度命中判斷級 🔴 才建立，降級條件「連續 6 份首輪 🔴＝0」未滿足）、**換掉 Fable 判斷層**（2026-09-06 已用 A／B 拍板：opus 思考 89K 對 Fable 22K、31 分對 13 分、成本相當且寫壞 JSON）、**新增任何 LLM 閘**（v18 的省法是少寫，不是再請一個模型看；§二刻意做成零 LLM 敏感度分析就是為了不違反這條）。

---

**最需要持有人拍板的三題**（預設見對應章節）：①「尚不能裁決」用旗標還是新 enum（預設：旗標）；②是否批准同步 gate 文案，讓閘驗的與機械層驗的是同一件事（預設：批准，只同步契約不降嚴格度）；③成對驗證用哪兩檔、由誰執行（預設：一乾淨一爭議，Claude 指揮、不發布）。
