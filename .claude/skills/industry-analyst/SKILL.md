---
name: industry-analyst
description: 建立「產業深度報告（Industry Deep Report / ID）」— 一份跨多檔個股共用、白話深入淺出又決策嚴謹的產業研究文件。輸入產業主題（如「玻璃基板封裝」「HBM 供需循環」「GLP-1 治療藍圖」「全球航運週期」），輸出八段錨點 sell-side HTML（summary/thesis/debates/mechanics/valuation/risks/stocks/appendix），品質由必交決策物 D1-D13 把關而非字數。v4.0（2026-09-03）：規則層瘦身、研究引擎降為旗艦專用、機械閘收斂為 scripts/check_id.py、正文全白話而分析師紀律收進折疊層。觸發：使用者提到「產業研究 / sector DD / 產業報告 / 產業藍圖 / industry landscape」「{主題} ds」「ds {主題}」「{產業} 敘述報告」「分析 {產業} 的供需循環」「{產業} 歷史與未來」「discourse {industry}」或具體產業主題（玻璃基板、HBM、CoWoS、AI ASIC、GLP-1、核融合、航運週期等）且尚未要求做個股 DD。不觸發：「{ticker} DD」「{ticker} 定見」「該不該進場 {ticker}」等個股請求，一律改走 stock-analyst。
version: v4.0
date: 2026-09-03
---

# industry-analyst skill v4.0 — 必交決策物取代字數

> **版號單一真相＝frontmatter `version:`**。歷史沿革與升版理由一律進 `references/changelog.md`；本檔只留現行規格，不留舊版本 WHY。

## 【定位】

- ID＝跨多檔個股共用的產業判斷，一份 ID 要能餵多檔 DD 的產業背景與供需裁決，不是單檔報告的附屬品。
- 北極星：一份 ID 只需誠實回答三題——①產業供需現在在哪一格（過剩/平衡/短缺）？②市場哪裡看錯（分歧＋已定價多少）？③現在貴不貴、我怎麼知道我錯了？
- 白話深入淺出是**表達層**，決策嚴謹是**論證層**，兩者不能互換：正文可以完全不出現行話與內部欄位名，但不能少一個承重數字、一張三情境表、一條可證偽的 kill 指標。
- **品質＝【必交決策物 D1-D13】每件是否真算、真有來源，不是字數**。舊字數地板已廢，篇幅只設上界警告。
- v3.0 教訓（詳見 `references/changelog.md`）：研究引擎把一份 ID 的成本推到 DD 的 20-40 倍、上線六週僅產出一份；字數地板獎勵填充，而 critic 抓到的錯全部落在沒算的量化模組；白話目標被 template 內建英文標籤與正文 claim tag 直接打架。v4.0 處方：規則層瘦身、必交物取代字數、研究分級、機械閘收斂一支 script、閱讀線全白話。

## 【路徑】

Skill 目錄：

```
~/.claude/skills/industry-analyst/
  SKILL.md                    # 本檔（現行版本見 frontmatter）
  templates/
    report_template.md        # 八段架構＋設計 token CSS（視覺唯一權威）
  references/
    sources.md                 # 來源紀律：T1 優先與 floor 分型／中文來源／spurious specificity／詞彙機率／Claim Taxonomy／freshness／禁推估／利潤池降定性
    research-queries.md        # Axis A-E 查詢模板，只給採集 agent 讀
    judgment-playbook.md       # 20 條情境判斷手冊（觸發索引式，內容不變）
    id-meta-schema.md          # id-meta JSON schema（validator 是權威，不變）
    changelog.md                # 版本沿革
```

Repo 層級：

```
scripts/check_id.py            # 機械閘：錨點／id-meta／表數／kill 同步／T1 占比／威脅卡／唯一敘述重複掃描／推導行
docs/assets/id-v4.css          # v4 家族共用外掛 CSS（省每檔 inline 一份）
docs/id/
  INDEX.md
  index.html
  ID_{Theme}_{YYYYMMDD}.html   # 唯一輸出
  cat-{mega}.html
```

`pre_publish_check.md`、`templates/schema_fields.md` 已於 v4.0 刪除（機械閘進 `scripts/check_id.py`，判斷閘進 id-review J1–J10）。存量 188 檔不遷移，隨改版自然汰換。

## 【開跑前】

1. **主題夠具體**：太籠統（「半導體」）→ 縮到有供需錨的層級（「AI ASIC 設計服務」「DRAM 超循環」）。
2. **查既有同主題 ID**：`ls docs/id/ID_*{Theme}*.html`。有 → 判定本次是「措辭級 refresh」（裁決不動）還是「裁決級 refresh」（走標準流程），summary 加一行前版連結；前版只讀 id-meta＋kill 表＋分歧卡標題（見【Token 紀律】）。
3. **分類**：從 `docs/id/taxonomy.md` 白名單選 `mega`＋`sub_group`（`mega` 同時決定 T1 floor 分型）。
4. **等級**：預設標準級；持有人明說「旗艦」才開旗艦引擎（見【研究流程分級】）。

## 【報告骨架】

八段錨點固定順序，不可重排。**唯一敘述規則**：核心判斷只在 thesis 段完整出現一次，之後全文只准寫「見核心判斷段」；裁決只在 summary 一句＋mechanics 3.4 完整推導；PM 行動只住 summary。**資料窗唯一**：整份報告一個資料窗日期，寫在 summary；refresh 若只更新部分章節，仍須把 summary 與 kill 表現值一併更到同一窗。

| 段 | 錨點 | 白話主標題 | 這段唯一的工作 | 可見字目標 |
|---|---|---|---|---:|
| 第一頁 | summary | 一頁看完 | 決策卡：一句 KEY CALL＋五格燈號（供需／時鐘／信心／已定價／5 年需求倍數，全白話）＋三句話（現在／未來／怎麼做）＋三條帶現值的 kill＋PM 行動，只住這裡 | 700–1,000 |
| 1 | thesis | 核心判斷 | thesis 完整講一次（含唯一一張承重表）；之後全文禁止復述 | 1,200–1,800 |
| 2 | debates | 市場哪裡看錯 | 3–4 張分歧卡（市場最強版本帶數字→我們認為→已定價多少→判別訊號→什麼發生就錯），含 ≥1 張替代威脅卡，steel-man 住卡內 | 2,000–2,800 |
| 3 | mechanics | 機制與供需 | 3.1 需求（TAM 三情境＋對帳）／3.2 供給（玩家矩陣＋利潤池＋成本曲線）／3.3 為什麼是現在／3.4 裁決（資本週期＋三視野表＋投資時鐘雙閘） | 4,000–5,500 |
| 4 | valuation | 現在貴不貴 | unit economics＋估值傳導＋priced-in 位置節（核心 🔴 檔現行倍數 vs 歷史帶＋估值分位＋26 週漲幅交叉＋現價隱含成長→收斂 low/mid/high） | 1,200–1,800 |
| 5 | risks | 我怎麼知道我錯了 | 一張表：kill ≥3 條（現值＋來源＋查核頻率＋領先幾季＋可否操縱＋破線姿態，≥1 條市場撮合價）＋催化劑雙路徑 | 900–1,300 |
| 6 | stocks | 誰受影響 | 🔴🟡🟢 表（純度推導行）＋非顯而易見受益者＋營運槓桿最大者＋「特徵非推薦」句 | 800–1,200 |
| 附錄 | appendix | 背景、歷史、來源 | 白話定義＋歷史轉折（日期＋量化錨）＋類比先例＋來源總表（單一，附 T 級）＋claim 標記說明，全部折疊 | 1,200–2,000 |

主閱讀線 **11,000–14,000 可見字，無地板**；超過只警告，地板改由必交物承擔。分析表 **≤12 張**（不含附錄來源總表；每張 ≤8 列、個股表 ≤16 列），超過 check_id.py 擋。HTML 目標：CSS 外掛 `docs/assets/id-v4.css` 時 ≤55KB，inline CSS 時 ≤70KB；超過只警告不擋。

## 【必交決策物 D1-D13】

這張表取代舊 QC／機械閘編號體系；`scripts/check_id.py` 驗「機器可驗」欄，id-review critic 抽查「真做的判準」欄。

| # | 必交物 | 真做的判準（critic 抽查） | 機器可驗 |
|---|---|---|---|
| D1 | 三句話＋最重要的判斷 | 行動句允許「都不買／等回調」；KEY CALL 不重述裁決 | now_state／future_state／action 落 id-meta |
| D2 | 供需裁決 | 資本週期三指標至少 2 個有數字（capex/折舊、ROIC vs WACC、lead time）；三選一或 split＋detail | sd_verdict／sd_verdict_detail |
| D3 | 投資時鐘 | Phase＋換相「必要∩充分」雙閘，充分須兩個獨立訊號 | clock_phase |
| D4 | TAM 三情境＋對帳 | top-down vs bottom-up 兩條路徑都有數字，差 >20% 說明缺口；bull/bear 由「改了哪個假設」推出；表末 5 年倍數 | demand_5y_multiple |
| D5 | 玩家矩陣＋利潤池 | 三時間欄；利潤池是總額占比非毛利率；無 source 的 % 改定性 | — |
| D6 | 成本曲線 | 週期型必做；結構成長型一句省略理由 | — |
| D7 | 分歧卡 3–4 張 | 每卡引 ≥1 共識來源；≥1 張替代威脅卡；每卡有可量化判別訊號＋證偽句 | 威脅卡標記 |
| D8 | 現在貴不貴（priced-in 位置節） | 核心 🔴 檔現行倍數（Fwd P/E 或 EV/S）vs 自身歷史帶＋估值分位＋26 週漲幅／擁擠度交叉＋現價隱含成長；收斂為 low/mid/high。零估值數字＝未交 | priced_in |
| D9 | kill 表 ≥3 條 | 每條附現值＋as-of＋查核來源與頻率；≥1 條市場撮合價；每條標領先幾季、可否被操縱、破線姿態；閾值不得與公司 guidance 同源；不可觀測指標不得上表 | kill_metrics[] 逐條對齊 |
| D10 | 催化劑 ≥5 | 日期（季度可）＋指標＋達成／落空雙路徑 | — |
| D11 | 個股表 | 純度每檔一行推導；🔴 附 mcap_bucket；「特徵非推薦」句 | related_tickers[]（purity_pct／mcap_bucket） |
| D12 | 歷史錨點 | 每個轉折 YYYY 或 YYYY-MM＋一個量化錨；≥2 輪 cycle 的產業附統計表 | 附錄 regex |
| D13 | 唯一敘述 | 核心判斷、裁決、PM 行動各只完整出現一次；分歧卡「市場認為」須是最強版本帶數字，不得是媒體標語 | 12-gram 重複掃描 |

## 【白話與禁流程劇場】

- 每段主標題中文白話，英文 sell-side 名降小字（「市場哪裡看錯 · Key Debates」）。
- 五格燈號白話對照：供需＝短缺／平衡／過剩／分裂；時鐘＝相位白話（如「擴張中段」）；已定價＝還沒反映／部分反映／大多反映；信心＝高／中／低；5 年需求倍數＝×__。
- 正文禁止出現：claim tag（[F:]/[I:]/[X:]/[A:]）、T 級標記、內部欄位名（如 sub_group 值）、方法論標籤（Deductive Inference）、版本戳散文、NC# 一類內部編號——這些是 critic 與機器的資產，一律收進 `evidence-fold` 或 data-attribute。
- 術語首現括號給一句白話，句式照 `notes/site-internal/root/_plainlang_styleguide.md`；新造術語先查該對照表，表上沒有就照該檔鐵律讀機制查證、定白話名並回寫對照表。
- 固定樣板塊大砍：「怎麼讀」只在表格需要判讀時寫一句（表格右欄已寫方向就不寫）；「對投資的意義」每段最多出現一次且不得復述核心判斷段；逐節來源收斂為附錄單一來源總表。圖只在有數據時畫，零數據的示意圖不畫。

## 【保留紀律（摘要）】

以下細節全文在 `references/sources.md`（寫 mechanics 段前必讀）：

- **T1 優先與 floor 分型**：核心承重數字（TAM／裁決／玩家矩陣）優先 T1；T1（含 T1-zh）占比 floor 依 id-meta `mega` 分型——`macro`／`cloud`／`space` 45%，其餘 60%。主題屬時事快變型但分類落在 60% 組（如 semi 底下的 AI 推論經濟學）時，可用 `check_id.py --t1-floor 45` 覆蓋，但**不得低於 45%**，且須在 `--report` 產出的 check 報告與 summary 折疊內各寫一句理由。
- **spurious specificity 禁令**：估算數字禁精準值，唯一例外——三情境表與三視野表允許 5 點步進的主觀權重（如 55／25／20，標明「主觀」且加總 100），此為判斷類規則例外，已登記 `knowledge/rule_ledger.md`，不外推到其他判斷。
- **詞彙級機率**：散文事件機率一律用「很可能／可能／不太可能」，禁精準百分比。
- **玩家矩陣禁 Q×4 推估**：不得用單季數字乘四推年度；已公告四季則加總，僅一季須註明「年化推估，actual 待 FY 公告」。
- **利潤池／議價權 % 無 source 降定性**：無來源的百分比一律改「主導／均勢／次要」，不留精準無源數字。
- **Freshness**：事件型 14 天／結構型 60 天，混合取嚴；`sections_refreshed` 三桶——technical（定義／歷史／技術成熟度）365 天、market（供給／需求／裁決）90 天、judgment（估值／分歧／證偽／個股）60 天。
- **T1 衝突明列**：兩個 T1 給不同數字須明列衝突＋差異原因＋採值邏輯，禁止偷偷擇一不說。

## 【研究流程分級】

| 級別 | 觸發 | 流程 | 估算成本 |
|---|---|---|---|
| **標準（預設）** | 一般新 ID、裁決級 refresh | ① writer（opus）定 thesis sketch＋列必答封閉問題（含 Axis E 五條機械查詢）→ ② spawn **一個** sonnet 採集 agent 回結構化證據包 → ③ writer 自做判斷性搜尋（分歧／priced-in／時鐘）並寫稿 → ④ completeness critic（sonnet）→ ⑤ `check_id.py` → ⑥ id-review critic（sonnet，餵摘錄）→ 修 → 發布 | 約 1.5–2.5M tokens |
| **旗艦** | 持有人明說「旗艦」或母題級新主題 | 標準流程＋五軸 fan-out（Axis A–E 各一獨立 agent，互不知彼此結果）＋承重數字 3-skeptic 對抗查證。**僅持有人明說「旗艦」時開啟，預設不跑**；規格全文見 `references/changelog.md`（v3.0 條目） | 12–24M，每次須持有人開啟 |
| **措辭級 refresh** | 裁決不動，只更新數字 | 不跑採集 agent、不跑 completeness；只 `check_id.py`＋critic 摘錄 | <0.5M |

理由：id-review critic 本來就對承重數字做獨立查證，3-skeptic 層與之重疊；completeness critic 便宜且不可替代（獨立腦抓缺席變數），故標準流程只保留它。

**① 採集 agent（sonnet，一次派工，封閉式問題清單）**：

```
Agent({
  description: "Collect structured evidence for {Theme} ID",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "對產業主題「{Theme}」，依 references/research-queries.md 的 Axis A-E 查詢模板逐項查證（每軸至少一題，Axis E 五條機械查詢不得因『顯然無關』跳過）。
  每項證據回傳結構化格式：{數字}｜{來源 URL}｜{as-of 日期}｜{T1/T2/T3-A/T3-B/T3-C/T4}。
  查不到就回報「查不到」，不得用訓練知識推估或以合理猜測代替。
  承重數字（capex／指引／RPO／折舊／發債／TAM）直讀 10-Q／8-K／官方新聞稿，不得只抓財經彙整站。
  彙整成一份證據包，按 Axis A-E 分節。"
})
```

**② completeness critic（sonnet，只知主題不讀論證）**：

```
Agent({
  description: "Completeness critic for {Theme} ID",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "你只知道產業主題「{Theme}」，尚未讀過任何草稿。
  第一步：獨立列出本主題『應有的一階變數』清單（競爭替代／地緣供給／需求方自供／監管／相鄰棧顛覆等，依主題調整）。
  第二步：讀草稿 {path}，逐項對照你的清單，找出草稿完全沒提到的變數。
  缺席的一階變數必須列為必補研究項，或指出草稿是否已在分歧卡明文『考慮過、排除，因為…』。
  回傳：缺席變數清單＋每項建議去哪個段落補。"
})
```

**③ id-review critic（sonnet，跨模型冷讀，只餵摘錄）**：

```
Agent({
  description: "Pre-publish critic gate on {Theme}",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "You are operating as the id-review sub-agent. Read spec at /Users/ivanchang/.claude/skills/id-review/SKILL.md.
  ID file: docs/id/ID_{Theme}_{YYYYMMDD}.html。
  先跑 `python3 scripts/check_id.py docs/id/ID_{Theme}_{YYYYMMDD}.html --excerpt /tmp/_excerpt_{Theme}.md --report /tmp/_check_{Theme}.md`，只讀這兩個檔，不讀整份 HTML；需要脈絡時用 grep -n／sed -n 只取指定段。
  依 D1-D13 必交決策物逐項抽查『真做的判準』欄，回報 🔴 CHANGES_CONCLUSION / 🟡 PARTIAL_IMPACT / 🟢 COSMETIC 分級與計數。"
})
```

## 【寫稿順序】

thesis sketch＋id-meta 草稿 → appendix → mechanics → valuation → debates → risks → stocks → thesis 定稿 → summary 最後定稿（PM 行動框須在 debates／risks／stocks 完成後才寫，因為那是把三段壓縮成「今天能做什麼決定」的橋接段）。

寫 mechanics 3.4／valuation／risks 動筆前 **Read `references/judgment-playbook.md`**，掃觸發索引，命中情境的條目逐條實際作答，答案融入章節敘事，不渲染手冊編號。寫 id-meta 前 **Read `references/id-meta-schema.md`**；`scripts/validate_id_meta.py` 是最終權威。

## 【Token 紀律】

- **自驗一律 `check_id.py` 或單行 python／grep；禁止 Read 回自己寫的整份輸出 HTML**。定位改用 grep 取行號，修改改用針對性 Edit。
- **前一版 ID 只讀 id-meta＋kill 表＋分歧卡標題，不讀全文**（防錨定亦省 token）。
- **critic 餵摘錄**（`check_id.py --excerpt`），不餵 mechanics 全文與附錄；critic 需要更多內容時自己 grep 指定段。
- **一次寫到帶內，禁止「寫完再壓縮重寫」**——重寫等於同一份報告的 output token 付兩次。
- **writer 超過約 60 輪或遇 API 500 後的修補一律換乾淨 patch agent，不再續用同一 writer。**
- **同一資料只抓一次**，抓齊後建表，不回頭補抓。
- **機械輪次批次化三條**：①定位先於動手——動手改檔前先用一輪複合 grep 把所有目標行號一次取齊；②同一檔案的機械性修改（措辭替換、數字更新，不需逐處判斷者）≥5 處時禁止逐個修補，改一次讀相關區段、一次重寫該段；③驗證性查詢一律併成單條複合指令，**驗證輪次 ≤3 輪**。
- **最終回報 ≤300 字＋INDEX 行**：只給路徑／KB／可見字／五格燈號／check 狀態／critic 🔴🟡 數／INDEX 行，不複述報告內容。

## 【發布流程】

1. `python3 scripts/check_id.py docs/id/ID_{Theme}_{YYYYMMDD}.html`，exit 0 才可往下；非 0 用 `--report notes/site-internal/id/_check_{Theme}_{YYYYMMDD}.md` 存機器報告並回頭修。
2. id-review critic（見上模板③，只餵摘錄）。
3. 修：🔴 必修；旗艦級 0 🔴 才放行，標準級 ≥1 🔴 交持有人選 ship 或 fix。
4. `docs/id/INDEX.md` append 一行（欄位格式沿用既有）：

   ```
   | YYYY-MM-DD | 主題 | 涵蓋 ticker 數 | 核心 🔴 / 次要 🟡 / 邊緣 🟢 | 投資時鐘 Phase | 🟡 比例 | 鮮度 | 檔名 | 備註 |
   ```

   鮮度欄位格式：`tech:YYYY-MM-DD 🟢 ｜ market:YYYY-MM-DD 🟢 ｜ judgment:YYYY-MM-DD 🟢`（超半衰期依序轉 🟡/🟠/🔴）。「🟡 比例」欄為 legacy 欄位，v4 報告一律填「—」。
5. `docs/id/index.html` 插卡片：找對應 `<!-- subgroup-anchor: {mega}.{sub_group} -->`，卡片加 `v4` badge pill。
6. `python3 scripts/build_id_category_pages.py`。
7. `python3 scripts/id_dd_mapping.py`、`python3 scripts/retrofit_dd_id_banner.py`（若腳本存在）。
8. `python3 scripts/check_tier_matrix.py --inject-html`；若回報「🆕 N 檔新 ticker」提示是否評估加入 Tier Matrix。
9. `python3 scripts/inject_report_primer.py --family id`。
10. `python3 scripts/qc.py`。
11. **預設停下複審，持有人說 push 才 commit**（同一 commit 涵蓋 ID＋索引；commit 前 `git status` 確認沒掃到別的 session 留下的檔）。

**Terminal 摘要格式**（精簡，不複述報告內容）：

```
✅ 產業深度報告完成：{主題}
📄 檔案：docs/id/ID_XXX.html（{KB}KB，可見字 {N}）
🚦 五格燈號：供需 {X} ｜ 時鐘 {X} ｜ 信心 {X} ｜ 已定價 {X} ｜ 5Y 需求倍數 ×{X}
🔧 check_id.py：{PASS/FAIL 摘要}
🧑‍⚖️ id-review critic：🔴{a} 🟡{b} 🟢{c}
🔗 INDEX 行已 append ｜ 索引卡片：[✅/❌]
```

## 【整合點：stock-analyst 讀取 ID（不變）】

stock-analyst 執行 DD 時，在護城河／競爭格局／產業演進章節前先：

```
1. 讀 docs/id/INDEX.md
2. 用 sector / theme 比對當前 ticker
3. 命中 → 讀該 ID 的 stocks 段找本 ticker 影響深度 + mechanics 段產業背景
4. 公司 DD：產業背景引用 ID_XXX（一句話 + <a href>）+ 本公司差異化 3-5 條量化 bullet；不重複產業通論
5. 未命中 → 照原流程，HTML 頁尾提示「未發現相關產業 DD，建議建立 ID_XXX」
```

下游消費者一律讀 id-meta `related_tickers` array，無需手動維護。

## 【觸發／不觸發】

**ID（dashboard／研究）觸發語**：
- 「研究 XXX 產業」/「sector 分析」/「industry landscape」/「產業報告」/「產業藍圖」
- 「玻璃基板／CoWoS／HBM／先進封裝／GLP-1／AI ASIC／EUV／核融合」等具體主題，且未帶股票 ticker 的量化分析要求。
- portfolio 決策時說「這個主題」「這個產業」而非「這檔股票」。

**DS（敘事／供需循環）觸發語（已吸收，一律轉向本 skill）**：
- 「{主題} ds」/「ds {主題}」/「{產業} 敘述報告」/「discourse {industry}」
- 「分析 {產業} 的供需循環」/「{產業} 歷史與未來」/「{產業} 短中長期推估」

**不觸發**（走其他 skill）：
- 「{ticker} DD」/「{ticker} 深度分析」/「{ticker} 定見」/「該不該進場 {ticker}」→ stock-analyst
- 純政策事件追蹤 → geopolitics-dd

若同時要求「先做產業＋再做這檔」，先跑 industry-analyst，再跑 stock-analyst（後者自動讀新產出的 ID）。

## 【條件載入路由表】

| 檔案 | 何時 Read |
|---|---|
| `references/sources.md` | 寫 mechanics 段（供給／需求／估值涉及來源判斷）之前 |
| `references/research-queries.md` | 只在 spawn 採集 agent 時附給該 agent；writer 本身不需通讀 |
| `references/judgment-playbook.md` | 寫 mechanics 3.4／valuation／risks 動筆前 |
| `references/id-meta-schema.md` | 寫 id-meta 之前 |
| `references/changelog.md` | 修改本 skill 規則之前 |

## 【版本歷史】

v1.0→v3.0 歷版摘要全文 → `references/changelog.md`。**寫報告時不需載入**；修改本 skill 規則前必讀，判斷類規則增刪必同步 `knowledge/rule_ledger.md`（見 repo CLAUDE.md 規則治理條款）。
