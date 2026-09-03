# stock-analyst v16 — rule-migration-map.md（QC-1～QC-54 ＋ 各 reference 檔去向，WP2）

> 每條 QC 與每個既有 reference 檔在 v16 下的去向。**去向欄位五選一**：`judgment`＝留在 `references/v16/judgment-rules.md`；`render`＝留在 `references/v16/render-rules.md`；`validator`＝機械腳本接管，見 `references/v16/validators.md`；`retire`＝提名退役，見 `references/v16/retire-candidates.md`；`reference不變`＝保留原 v15.2 reference 檔，條件載入路由不變。多數條文横跨兩類（判準留判斷層、機械部分交腳本），**多重去向皆列出**，不強迫單一分類。門檻數字與語意搬遷過程一字未動。

## 一、QC-1～QC-53（含 QC-7b）逐條去向

| QC | 一句話 | 去向 | 新檔位置 |
|---|---|---|---|
| QC-1 | 業務權重須引用§3，禁自行估算 | judgment | judgment-rules.md §5 |
| QC-2 | MA104w讀採集數字包第5節旗標，禁自算 | validator＋retire候選 | validators.md（evidence.json.numbers）；retire-candidates.md（"禁自算"警語對象已被架構排除） |
| QC-3 | Bear PE/EPS/股價推導公式 | judgment＋validator | judgment-rules.md §9；validators.md（dd_scenario.py／verify_dd_math.py檢查A） |
| QC-4 | Fwd P/E 5Y分位公式 | judgment＋validator缺口 | judgment-rules.md §8；validators.md缺口①（分位重算尚無腳本） |
| QC-5 | §7同業比較須與§10.4同組 | judgment | judgment-rules.md §6 |
| QC-6 | §9治理須涵蓋四項 | judgment＋validator缺口 | judgment-rules.md §7；validators.md缺口⑧（四子項覆蓋完整性尚無腳本） |
| QC-7 | 頁首/章節核心數字須一致 | retire候選 | retire-candidates.md（structurally eliminated by gen_dd_tables.py單一來源） |
| QC-7b | §1/頁首禁技術面語言作進場理由 | render＋structural | render-rules.md §4（QC-54白話呈現精神涵蓋）；技術面輸入僅餵`dd_decision.py` row4/5 pacing、從不進verdict，屬架構性排除，非逐字搬遷（見下方「未逐字搬遷」附註） |
| QC-8 | 執行不中斷 | judgment（保留提名）＋retire候選 | judgment-rules.md §1（QC-47永不修剪清單內）；retire-candidates.md（v15設計稿既有提名延續） |
| QC-9 | 品質分強制計算，5項veto降級制 | judgment | judgment-rules.md §8 |
| QC-10 | Bollinger位置讀採集旗標，禁自算 | validator＋retire候選 | 同QC-2 |
| QC-11 | 倉位角色框架，不輸出組合% | judgment | judgment-rules.md §0、§14 |
| QC-12 | 已退役，併入QC-39 | judgment（已併） | judgment-rules.md §10；retire-candidates.md記錄狀態確認 |
| QC-13 | 自我攻擊裁決 | judgment | judgment-rules.md §18 |
| QC-14 | 核心數據交叉一致性 | retire候選 | retire-candidates.md（與QC-7/36合併提名） |
| QC-15 | 時效性檢查，>180天標註 | validator | validators.md（validate_evidence.py `as_of`） |
| QC-16 | 關鍵時程具體化 | judgment | judgment-rules.md §5 |
| QC-17 | 先前報告只讀三區塊，禁整檔Read | retire候選 | retire-candidates.md（dd_prior.py架構性排除） |
| QC-18 | 只讀最近一份，嚴禁合併比較 | retire候選 | retire-candidates.md（與QC-17合併提名） |
| QC-19 | 重大事件五組強制搜尋＋深查 | validator＋judgment（隱含） | validators.md（coverage-axes.md `major_events`軸）；深查／定性判斷部分未獨立標號承接，隱含於judgment-rules.md對`evidence.coverage`/`triggers[]`的一般建構義務內（見下方「未逐字搬遷」附註①） |
| QC-20 | 催化劑實現檢查 | judgment | judgment-rules.md §5 |
| QC-21 | R:R數學假象防禦 | judgment＋validator | judgment-rules.md §9；validators.md（dd_scenario.py／verify_dd_math.py檢查A） |
| QC-22 | 股價漂移>10%/20%標警語 | validator缺口 | validators.md缺口②（尚無腳本；v16下Stage0/1/2分段執行，原「長session單次搜尋vs最終寫檔」漂移場景本身架構已變，見下方附註②） |
| QC-23 | 競爭威脅三級分類 | judgment | judgment-rules.md §4 |
| QC-24 | Intraday訊號讀採集旗標，禁自算 | validator＋retire候選 | 同QC-2 |
| QC-25 | Beta雙來源驗證 | validator＋retire候選 | 同QC-2 |
| QC-26 | Margin結構性測試 | judgment | judgment-rules.md §4（護城河閘二） |
| QC-27 | Revenue-OI divergence分級 | judgment＋validator缺口 | judgment-rules.md §6；validators.md缺口③ |
| QC-28 | 絕對vs相對成長對照 | judgment | judgment-rules.md §4（護城河閘三） |
| QC-29 | 已退役，附錄A降為base+bear 2情境 | validator＋retire（已確認） | validators.md；retire-candidates.md狀態確認 |
| QC-30 | 同業溢價收斂壓測 | judgment | judgment-rules.md §8 |
| QC-31 | signal對映強制表 | judgment | judgment-rules.md §8 |
| QC-32 | dd-meta JSON硬性schema | validator | validators.md（validate_dd_meta.py）；欄位對映權威見`judgment-to-ddmeta.md`（WP1c既有交付物） |
| QC-33 | 推導可追溯性 | judgment＋render＋validator | judgment-rules.md §19（reasoning每模組必填）；render-rules.md §3（呈現層不得新增數字，validate_prose.py執行）；schema必填見judgment.schema.json |
| QC-34 | 季節性過濾，禁單季snapshot | judgment＋validator缺口 | judgment-rules.md §14；validators.md缺口④ |
| QC-35 | 漂移分級門檻（2Y/5Y/10Y） | judgment＋validator | judgment-rules.md §14；validators.md（validate_judgment.py驗`drift_rule`欄位存在，WARN） |
| QC-36 | 5Y目標價一致性四處 | retire候選 | retire-candidates.md（與QC-7/14合併提名） |
| QC-37 | 裁決單一居所 | render | render-rules.md §6 |
| QC-38 | 篇幅預算與深度標準 | judgment＋render＋validator | 五模組七表必交（judgment-rules.md各對應章節內建要求＋validators.md verify_dd_math.py檢查C）；篇幅目標/省法三條/byte預算表（render-rules.md §7）；bytes機械閘（validators.md dd_sections.py bytes） |
| QC-39 | 產業態勢雙向掃描三軸裁決 | judgment＋validator | judgment-rules.md §10（評估與裁決）；validators.md／evidence-pack.md＋coverage-axes.md（搜尋機械化） |
| QC-40 | 輸出潔淨六類禁渲染 | render＋validator | render-rules.md §5；validators.md（dd_sections.py leaks） |
| QC-41 | 產業態勢獨立critic | judgment（觸發標記）＋reference不變 | judgment-rules.md §16；critic-gates.md（spawn prompt／checklist全文，WP3待更新輸入格式） |
| QC-42 | 循環交易鏡頭 | judgment（路由指標）＋reference不變 | judgment-rules.md §1條件載入表；cyclical-lens.md不變 |
| QC-43 | archetype分類器+gate-set路由 | judgment | judgment-rules.md §1 |
| QC-44/45/46 | 非複利archetype gate-sets（金融/未獲利/轉機·公用） | judgment（路由指標）＋reference不變 | judgment-rules.md §1條件載入表；archetype-gatesets.md不變 |
| QC-47 | archetype×QC適用矩陣 | judgment | judgment-rules.md §1 |
| QC-48 | 爆發候選Bull冷讀 | judgment（觸發標記）＋reference不變 | judgment-rules.md §16；critic-gates.md不變 |
| QC-49 | 裁決hysteresis | judgment＋validator | judgment-rules.md §15；validators.md（dd_decision.py覆寫層機械執行） |
| QC-50 | 錯過成本反向critic | judgment（觸發標記）＋reference不變 | judgment-rules.md §16；critic-gates.md不變 |
| QC-51 | 同形狀peer裁決對帳 | judgment＋reference不變 | judgment-rules.md §12；critic-gates.md（完整對帳句式與執行細則） |
| QC-52 | DD↔ID對帳 | judgment | judgment-rules.md §11（全文保留，屬Stage1證據讀取核心紀律） |
| QC-53 | 情境判斷手冊（32條觸發式） | judgment（路由指標）＋reference不變 | judgment-rules.md §17；judgment-playbook.md不變 |

**未逐字搬遷附註**（誠實揭露，非隱藏遺漏）：
① QC-19「深查」的判斷部分（M&A/訴訟/FDA/CEO異動的定性影響）在v16下沒有獨立編號段落承接——它被吸收進judgment-rules.md對`contradictions[]`／`triggers[]`／`decision_inputs.bear`等欄位「須從evidence.coverage的sourced findings建構」的一般性義務中，但沒有像QC-20/QC-23那樣的專屬小節。若2026-10校準發現重大事件判讀品質下滑，應優先檢查這裡是否需要补一個顯性小節。
② QC-22股價漂移的原始情境（單一長session writer，首次搜尋價格到最終寫HTML間可能經過數小時到數天）在v16三段式架構下場景本身改變——Stage 0b evidence.json一次性produce、Stage 1/2各自短生命週期執行，理論上漂移窗口大幅縮短，但**尚未證明歸零**（Stage 2若延後很久才跑，仍可能用到過期價格）。本表誠實列為「validator缺口」而非「已解決」。

## 二、既有 reference 檔（v15.2）在 v16 下的角色

| reference檔 | v16下角色 | 去向細節 |
|---|---|---|
| `archetype-gatesets.md` | reference不變 | QC-44/45/46全文條件載入不變，judgment-rules.md §1只留路由指標 |
| `cyclical-lens.md` | reference不變 | QC-42全文＋附錄B規格條件載入不變 |
| `roic-durability.md` | reference不變 | §5.R判準字典，judgment-rules.md §4已內嵌精簡表＋指向本檔補完整推理 |
| `judgment-playbook.md` | reference不變 | QC-53觸發索引32條，judgment-rules.md §17只留路由指標 |
| `timing-appendix.md` | reference不變（角色略調整） | 附錄A擇時全節（品質分veto/final_signal六步/估值燈/週線六態），judgment-rules.md §8已內嵌核心門檻，本檔仍是填`appendix_a`四欄前的必讀來源；**retire-candidates.md已提名**評估`final_signal`六步表是否也該被`dd_decision.py`吸收（非本輪裁定，留WP3待辦） |
| `data-collection.md` | reference不變＋部分被新檔補充 | Stage 0a採集agent spawn模板沿用不變；Stage 0b（覆蓋矩陣搜尋）新增能力由`references/v16/evidence-pack.md`＋`references/v16/coverage-axes.md`承接（WP1a既有交付物，非本輪WP2產出）；狀態判定Python實作沿用不變（機械採集腳本本體，非judgment/render/validator類條文） |
| `decision-layer.md` | reference不變（讀者轉移） | rows 1-10矩陣→`scripts/dd_decision.py`機械翻譯（"翻譯不是修訂"，見`decision_inputs.md`）；§11/§12/§13a-c判斷句式與門檻→已內嵌judgment-rules.md §12/§13/§14；本檔仍是`dd_decision.py`維護者的權威源文字，Stage 1/2 agent不再需要直接讀它（judgment-rules.md §14已聲明"你不手算裁決"） |
| `html-output.md` | reference不變（v15.2 legacy）＋新檔取代 | BODY組裝契約/dashboard模板/dd-meta JSON段/顯示順序等→`references/v16/render-rules.md`（v16版，Stage 2讀這份不讀html-output.md）；html-output.md本身保留供v15.2單體writer pipeline（`render_dd.py`無`--assemble`旗標時的舊模式）沿用，退場時點屬WP3範圍 |
| `critic-gates.md` | reference不變（輸入格式待WP3更新） | QC-41/48/50/51觸發條件與fail-safe方向→judgment-rules.md §16（Stage1只標記，不spawn）；spawn prompt全文/七軸checklist/查證預算/合併載具條款→保留本檔不變；**已知落差**：本檔現行文字仍寫「讀`dd_sections.py text`全文」，v16設計稿§5.3改為「讀evidence.json+judgment.json」——此更新屬WP3（agent契約）範圍，WP2不得動這份reference檔內容 |
| `delta-refresh.md` | 未變動，待WP3/v16.1 | v16下delta複審模式尚未設計（design spec §8待決4：「delta複審是否納入本輪或留v16.1」），本檔完全未受WP2影響，SKILL.v16.draft.md的路由表會標註此為已知缺口 |
| `dd-meta-schema.md` | reference不變（角色轉移） | QC-32 schema本體權威已轉移給`scripts/dd_schema/judgment.schema.json`＋`judgment-to-ddmeta.md`（WP1c交付物）；本檔對v16 Stage1/2 agent已非必讀，但仍是`gen_dd_tables.py`維護者與dd-meta下游消費者（research頁/dd-screener等）的欄位語意權威文件，不建議退役 |
| `changelog.md` | 未變動 | 沿革記錄，v16亦適用「改規則前必讀」慣例，不屬本次三分法範圍 |

## 三、決策矩陣／E12／dd-meta 契約等非QC編號條文去向

| 條文 | 去向 | 新檔位置 |
|---|---|---|
| 決策矩陣rows 1-10（Hard Veto/節奏調節/Soft Veto/Baseline） | validator | `scripts/dd_decision.py`（翻譯自decision-layer.md，非修訂）；judgment-rules.md §14只列decision_inputs七個判斷密集欄與row 8a/8b資格條件 |
| E12監測與觸發器表（唯一居所） | judgment | judgment-rules.md §14（`triggers[]`規格）；同源轉譯規則見`judgment-to-ddmeta.md`§四 |
| dd-meta JSON schema v15.0（22+5必填+20選填） | validator | validators.md（validate_dd_meta.py）；欄位對映`judgment-to-ddmeta.md` |
| Token紀律（機械輪次批次化三條） | judgment＋render（各自複述一次） | judgment-rules.md §20；render-rules.md（隱含於§10輸出流程，未獨立成節——SKILL.v16.draft.md的Token紀律v16版一節統一收口） |
