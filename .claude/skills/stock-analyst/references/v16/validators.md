# stock-analyst v16 — validators.md（判斷機器 → 機械腳本接管清單）

> v16-draft（WP2）。本檔是 QC-1～QC-54（＋決策矩陣／E12／critic 觸發機械化部分）中「可由檔案機械判定」那一支的權威索引——語意搬自 SKILL.md／references，門檻數字不動，只換「誰檢查」。判斷類條文留在 `judgment-rules.md`；呈現類條文留在 `render-rules.md`。FAIL 一律擋 commit／組裝；WARN 只提示不擋。

| QC/規則 | 原一句話 | 接管腳本與檢查名 | FAIL/WARN |
|---|---|---|---|
| QC-2 | W52/W104/W250 讀採集數字包，禁自算 | `dd_evidence.py`／採集 agent 產出 `evidence.json.numbers`；`validate_evidence.py` 驗欄位存在 | WARN（缺欄） |
| QC-3 | Bear PE／Bear EPS／Bear 股價推導公式 | `dd_scenario.py`（EV/IRR/AR 算術）＋`verify_dd_math.py` 檢查 A（EV5y／IRR_base／AR／\|max_dd\|恆等式，tol 見腳本） | FAIL |
| QC-4 | Fwd P/E 5Y 分位公式＝(當前−5Y低)/(5Y高−5Y低)×100% | 無獨立腳本重算分位本身（見末段缺口①）；`validate_judgment.py` 只驗 `valuation.percentile_5y` 型別存在 | WARN（型別） |
| QC-7／QC-14／QC-36／QC-37 | 頁首／§13／dd-meta 數字須三處同源、5Y 目標價四處一致 | **結構性消除**：v16 下頁首/decision/dd-meta 皆由 `gen_dd_tables.py` 從同一份 `judgment.json` 生成，不存在「抄三次」的動作，故不再需要事後比對 | — |
| QC-9 | 品質分＝min(底分+體質veto,10)，5 項 veto 降級制 | `validate_judgment.py` 驗 `appendix_a.quality_score` 型別＋範圍 1-10；veto 加減本身仍是判斷（見 judgment-rules.md §8） | WARN |
| QC-15 | 引用產業/市場數據須標發布日期，>180 天加註 | `validate_evidence.py`：`coverage.<axis>.findings[].as_of` 必填，>180 天標記 | WARN |
| v16.1 新增 | 估值歷史/動能/共識修正/同業財務/客戶集中度五欄＋最新一季 KPI 須存在且≥4 項有 as_of/source | `dd_numbers_extra.py`（零 LLM 算五欄＋KPI 佔位符）＋`validate_evidence.py::check_numbers_extra`（`numbers.valuation_history`／`momentum_26w`／`consensus_revision`／`peer_financials`／`edgar_concentrations` 存在性、`peer_financials`≥2 對手、`latest_quarter_kpis.items`≥4 項＋quarter 與最新季標籤 token 一致） | WARN（預設）／FAIL（`--strict`，讓舊 evidence 檔仍可跑） |
| QC-17／QC-18 | 先前報告只讀三區塊，嚴禁整檔 Read | `dd_prior.py`（零 LLM 擷取 revlog／H1-H3+R1-R3／E12 表，寫入 `evidence.json.prior_dd`），從不把整份舊 HTML 交給任何 agent | 結構性（無 FAIL/WARN，機制本身防呆） |
| QC-19 | 重大事件 5 組強制搜尋 | `coverage-axes.md` `major_events` 軸（5 條 query 模板）＋`validate_evidence.py` 驗 `queries_run`≥2 | FAIL（缺軸） |
| QC-21 | R:R 數學假象防禦（<5% 下行失效，改極端 Bear） | `dd_scenario.py` 算術本體＋`verify_dd_math.py` 檢查 A；「是否套用極端 Bear」仍是 judgment-rules.md §9 的判斷 | FAIL（算術部分） |
| QC-22 | 股價漂移>10%/20% 標警語 | 無腳本（見末段缺口②） | — |
| QC-27 | Revenue YoY−OI YoY divergence 分級 | 無腳本重算 divergence（見末段缺口③） | — |
| QC-29 | 附錄 A R:R 降為 base+bear 2 情境，`stress` 記 2/2 | `dd_scenario.py` 輸出形狀本身只產 base+bear 兩案；`validate_dd_meta.py` 驗 `stress.{pass,total}` 型別 | WARN |
| QC-32 | dd-meta JSON 硬性 schema（22+5 必填+20 選填，enum 白名單） | `validate_dd_meta.py --report`（唯一權威） | FAIL |
| QC-33 | 承重結論數字須附≤3行推導 | `judgment.schema.json` 要求 `reasoning.<module>` 必填非空；`validate_prose.py` 反向擋呈現層新增數字（見下） | FAIL（欄位缺）／FAIL（prose 數字溢出） |
| QC-34 | 漂移/分位/護城河判定禁單季 snapshot，須 TTM/年度 | 無腳本區分季度口徑（見末段缺口④） | — |
| QC-35 | H1/H2/H3 漂移分級門檻（2Y 連2季5%/連3季10%；5Y 連4季5%/連6季10%；10Y 跨2年/跨3年） | 門檻數字本身留 judgment-rules.md §14（agent 判斷「是否達到」）；`validate_judgment.py` 只驗 `thesis.H[].drift_rule` 欄位存在 | WARN |
| QC-38 | 篇幅 75–105KB＋分章節 byte 預算＋七表五模組 | `dd_sections.py bytes FILE`（逐段 canonical id 比對預算表，`--strict` 時 exit 1）；`verify_dd_math.py` 檢查 C（五模組存在性：0 次 FAIL、1 次 WARN） | FAIL（模組缺）／WARN（bytes 超標，非 strict） |
| QC-39 ①（強制搜尋） | A/B/C 三軸各≥3 query | `coverage-axes.md`＋`dd_evidence.py axes`＋`validate_evidence.py`（每軸 `status` 必填，`found` 需≥1 條 sourced finding，`none` 需≥2 條 `queries_run`） | FAIL |
| QC-40 | 輸出潔淨，六類機制詞不得渲染進 HTML | `dd_sections.py leaks FILE`（`LEAK_PATTERNS` 唯一權威詞表）＋`_UNESCAPED_LT_RE`（未跳脫 `<`） | FAIL（新增檔＋已過 render_dd 標記時）／WARN（其餘情況） |
| QC-40（呈現層新規） | 呈現層不得新增判斷物沒有的數字 | `validate_prose.py PROSE_DIR --judgment judgment.json`（容忍規則見 render-rules.md §3） | FAIL |
| 決策矩陣 rows 1–10 | Hard Veto／節奏調節／Soft Veto／Baseline，max-severity wins | `dd_decision.py run`（機械路由，翻譯自 `decision-layer.md`，非修訂）；`dd_decision.py check-all --infer-from-html` 可回溯核對既有 30 份 v15 DD | FAIL（欄位缺型別）／裁決本身不設 FAIL，只有輸入缺值時記 input_gap |
| QC-49 | 90 天內翻面須引前次觸發器已發火，否則承繼 | `dd_decision.py`（`qc49_inherit_prior`/`prior_verdict`/`prior_role` 覆寫層，見 `decision_inputs.md` §2.4）；`validate_judgment.py` 只驗 `thesis.R[].h_ref` 等交叉引用可解析 | WARN（引用缺）／裁決覆寫依輸入值機械執行 |
| E12 同源 | `kill_metrics[]`/`rearm_trigger`/`catalysts[]` 與 `triggers[]` 同源 | `gen_dd_tables.py`（`judgment-to-ddmeta.md` §四同源轉譯規則，見該檔「kill_metrics 兩種居所」）；`validate_judgment.py` 驗至少一列 `triggers[].date` 非空 | WARN |
| 財報時效閘 | 財報後≤3 交易日跑 DD 須用財報後價格 | `data-collection.md` 採集腳本第 1.5 節（`earnings_recency` 計算＋警語注入），非獨立驗證腳本，屬採集端機械計算 | 結構性（無 FAIL/WARN，數字直接由腳本算出） |
| Bull 退化 | 情境樹 Bull EPS 不得幾乎等於 Base（僅靠終端倍數） | 目前僅 critic ⑥ 人工抽查（見 `critic-gates.md`），**無機械腳本**（見末段缺口⑤） | — |
| 未跳脫 `<` | 正文比較符須 `&lt;`/`&gt;` | `dd_sections.py leaks` 的 `_UNESCAPED_LT_RE` | FAIL（同 leaks 規則） |
| `id="decision"` 錨點 | §13 段落須帶錨點供定見欄連結 | `qc.py check_decision_anchor`（v13/v14 強制）＋`render_dd.py --assemble` 對 `decision` 段的固定處理 | FAIL |
| dead link | 內部相對連結不得指向不存在檔案 | `qc.py check_dead_links` | WARN（changed-files 模式一般為 WARN，見 qc.py severity model） |
| CJK 標點 | 全形字後不得接半形 , . : | `qc.py check_cjk_punct`（.md／.html 皆掃） | WARN（除非該行是新增行且觸發 escalate 條件） |
| 回溯一致性 | judgment.json → 生成 HTML 的 dd-meta 須與判斷物一致 | `verify_dd_math.py` 檢查 D（版本戳）＋E（`scenario_tree` 六欄 tol 對比）；judgment↔生成 HTML 全欄一致尚無逐欄腳本（見缺口⑥） | FAIL（D／E 覆蓋範圍）／— |

---

## 判為 validator 類但尚無腳本的缺口

以下條文性質上屬於「有唯一正確答案、機械可判定」，但截至 WP2 尚未有對應腳本，目前仍**完全倚賴 agent 自律或 critic 抽查**——列出供 WP1 後續補或 2026-10 校準輪評估是否值得建腳本：

1. **QC-4 分位公式重算**：`(當前−5Y低)/(5Y高−5Y低)×100%` 本身無腳本從 `evidence.json.numbers`（5Y 高低）與現價重算比對 `valuation.percentile_5y`——目前只驗型別存在，不驗數值正確性。
2. **QC-22 股價漂移檢查**：首搜日 vs 報告日價格漂移 >10%/20% 的警語觸發，無腳本比對 `evidence.json` 採集時價格與 `decision_inputs.price_at_dd`。
3. **QC-27 Revenue-OI divergence 分級**：`>3%`／`>7%` 兩級警示的除法運算，無腳本從 `judgment.quality` 或 `growth` 相關欄位重算並比對敘事結論。
4. **QC-34 季節性口徑判定**：無法機械分辨「TTM／年度」vs「單季 snapshot」——這類口徑錯誤只能靠 evidence.json 的 `as_of`／`window` 欄位間接稽核，未成閘。
5. **Bull 退化偵測**（EPS CAGR 貢獻 vs re-rate 貢獻比例）：`dd_scenario.py` 已算出三分量拆解數字，理論上可加一條「Bull 情境 EPS 貢獻 < X% 則 WARN」的機械閘，但 WP2 尚未加；目前唯一把關是 QC-41/48 critic 的人工冷讀⑥項。
6. **judgment.json ↔ 生成 HTML 逐欄回溯一致性**：`verify_dd_math.py` 只驗版本戳與 `scenario_tree` 六欄，不是把 `dd-meta.html` 全部欄位與 `judgment.json` 逐一比對——理論上 `gen_dd_tables.py` 是唯一生成路徑應該天然一致，但目前無回歸測試鎖定這個假設。
7. **採集端旗標來源紀律**（QC-2/10/24/25：MA104w／Bollinger／intraday／Beta 雙源禁自算）：只能檢查 `evidence.json.numbers` 欄位是否存在，無法機械偵測 Stage 1 是否老實引用而非自己重算後覆蓋。
8. **QC-6 治理四項覆蓋完整性**：`validate_judgment.py` 只驗 `governance` 頂層 key 存在，不驗其下①股權結構②資本配置③薪酬④內部人交易四個子項是否真的都填了（或誠實標「數據限制」）。
