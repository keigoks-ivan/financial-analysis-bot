# stock-analyst v16 — retire-candidates.md（退役提名表，WP2）

> **本檔只提名，不刪除、不裁定。** 裁定權在 2026-10 校準輪（`knowledge/rule_ledger.md` 既有節奏）。提名理由分三類：
> ① **已被 validator/architecture 完全取代**——v16 三段式（evidence.json → judgment.json → prose）讓條文原本要防的失誤模式，在新架構下已無路徑發生，條文本身變成「解釋一個不會再發生的錯誤」；
> ② **零救援實績**——沿用既有 `rule_ledger.md` 定義，登記在案但兩輪校準查無觸發或查無被攔下案例；
> ③ **與他條重複**——語意已完全內含於另一條，維持兩條並存只增加維護成本。
> 本表**不新增任何判斷類規則**，也不改動任何條文的門檻與語意——只是把「這條還有沒有存在必要」的問題攤開列出。

| 編號 | 條文一句話 | 理由類型 | 建議處置 |
|---|---|---|---|
| QC-7／QC-14／QC-36 | 頁首儀表板／§13／附錄 A／dd-meta 的 Fwd PE・PEG・R:R・5Y 目標價須人工核對三/四處同源一致 | ①已被architecture完全取代——v16下頁首/decision/dd-meta/附錄A皆由`gen_dd_tables.py`從同一份`judgment.json`機械生成，不存在「抄三次、可能抄歪」的動作路徑，人工核對同源的失效模式已不可能發生 | 三條合併降級為`gen_dd_tables.py`的一句實作說明（「單一數字居所」已是judgment.json本身，非事後核對規則），正式QC條文提名退役；2026-10校準若發現`gen_dd_tables.py`本身有bug造成不同源，則證明retirement誤判，應恢復人工核對條款 |
| QC-17／QC-18 | 前份DD只能grep/sed擷取三區塊，嚴禁整檔Read較早版本 | ①已被architecture完全取代——`dd_prior.py`（零LLM）是Stage 1取得前份資訊的唯一管道，輸出已是擷取後的`evidence.json.prior_dd`三區塊；Stage 1本身被明文禁止Read `docs/dd/`，沒有工具權限可以違反本條，警語對象已不存在 | 條文降級為`dd_prior.py`契約引用（見judgment-rules.md §11／§20已如此處理），SKILL.md本體不再需要重複「禁止整檔Read」的自律警語；退役後若查到判斷層仍嘗試繞過禁令（如透過WebSearch重新搜到前份報告內容），視為新失效模式，需另立規則而非恢復本條 |
| QC-2／QC-10／QC-24／QC-25 | MA104w／Bollinger／intraday／Beta雙源，「讀採集數字包第5節旗標，禁自算」 | ①部分被architecture取代——v16下Stage 1被明文禁WebSearch/WebFetch且無Bash執行權，物理上無法「自算」，唯一數字來源是`evidence.json.numbers`；「禁自算」這句警語對象在Stage 1手上已不可能發生 | 保留門檻數字本身（>30%差異取較高值等，屬judgment-rules.md已收錄的判斷部分），但「讀採集數字包第5節旗標」這句操作性指令可簡化為「讀`evidence.json.numbers`對應欄」，不需要「禁自算」的重複警語；若Stage 0b evidence-pack子agent反而被查到有自算旗標的情形，禁令對象轉移到Stage 0b spawn prompt，需在`evidence-pack.md`補一句而非在judgment-rules.md重申 |
| QC-8 | 執行不中斷，LLM按所有QC規則自動跑完所有章節 | ①已被architecture完全取代（v15設計稿已提名，v16延續）——三段式拆分後每段本身就是一次性、有限範圍的Write+驗證迴圈（≤3輪），「中途中斷」的失效模式已被工具級禁令（禁Read整份輸出、驗證輪次上限）結構性排除，不需要再靠agent自律「不中斷」 | 維持v15.2設計稿的既有提名，2026-10校準輪一併審計；若Stage 0/1/2任一段仍發生「因confuse而提前停止」的案例，恢復本條為顯性判斷規則 |
| QC-29（已退役，v15沿用） | 附錄A R:R降為base+bear 2情境，dd-meta `stress`記2/2 | ①已被validator完全取代——`dd_scenario.py`的輸出形狀本身只產base+bear兩案，不存在「輸出4情境」的路徑；`validate_dd_meta.py`驗`stress.{pass,total}`型別 | 狀態不變（v15已退役，本表僅確認v16下retirement依據更穩固——原本是流程紀律，現在是腳本輸出形狀的物理限制），無需進一步動作 |
| QC-12（併入QC-39，v14.7沿用） | 近90天產業/競爭掃描獨立條文 | ③與他條重複——語意已完全併入QC-39三軸裁決（見judgment-rules.md §10「QC-12（併入本條）」段），獨立編號只剩歷史指向作用 | 狀態不變（沿用既有併入決定），本表僅確認v16下`coverage-axes.md`的`major_events`軸與QC-39/QC-12的搜尋query模板一致，未發現新分歧 |
| 附錄A基本面評級六步表中純機械部分（final_signal步驟1-2的布林判定） | quality×估值燈×MA×trap組合的if-else判定 | ①已被validator部分取代——`dd_decision.py`已機械化決策矩陣rows 1-10（含Hard/Soft Veto的if-else），但**附錄A的`final_signal`六步表本身（timing-appendix.md §B/H）尚未被`dd_decision.py`吸收**，兩者是平行的兩套if-else（一套算`signal`，一套算`dca_verdict`），有潛在的「規則兩地維護」風險 | **不提名退役，改提名WP3待辦**：建議WP3評估是否把`timing-appendix.md`的`final_signal`六步表也腳本化進`dd_decision.py`或新增`gen_final_signal.py`，讓`signal`（thesis-level品質分類）與`dca_verdict`（現時裁決）共用同一套機械路由基礎設施；本表列出僅為記錄WP2過程中發現的結構性重複，非成熟的退役提名 |

---

## 未提名但WP2過程中發現的規則衝突／重複（僅記錄，見主回報「規則衝突」欄）

以下不算退役候選（門檻/語意不重複，只是條文散落多處），但登記在此供rule_ledger.md下次規則治理時參考：

- `judgment-to-ddmeta.md`已文件化`kill_metrics[]`與`triggers[]`存在「雙居所+優先序」的既成事實（非WP2新增，WP1c已如此判斷）——E12「唯一居所」條文（QC-37/E12同源規則）與此existing dual-storage事實有輕微語意落差，但該檔已解釋此為「回溯反推 vs 新報告」的差異，不算真衝突，僅提醒judgment-rules.md §14的「唯一居所」措辭對回溯轉譯場景不完全適用。
