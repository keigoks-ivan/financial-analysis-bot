# Pre-Publish Report — ID_AIInferenceEconomics_20260720.html

industry-analyst v3.0 首發 pilot（sell-side 呈現升版）。標的：AI Inference Economics 推論經濟學母題。藍本＝`id_sellside_sample.html`（八段架構＋中國 open-weight 節已含）；本輪任務＝融入 Kimi K3 deep-research 結果、id-meta 升 v3.0、發布落檔＋索引同步。裁決不變：`sd_verdict=shortage` / `clock_phase=II` / `conviction=high`。

發布日：2026-07-20。查核日（本報告所有 spot-check）：2026-07-20。

---

## Gate 表 pass/fail 總覽

| Gate | 性質 | 結果 | 備註 |
|:---|:---|:---|:---|
| Gate 1 | 阻斷 | ✅ PASS（spot-check） | 🔴 核心 GOOGL/AVGO/NVDA 財報引用季度（GOOGL 2026Q1 10-Q、AVGO FY26 Q2、NVDA FY27 Q1）均為 2026-05～07 揭露，< 60 天 |
| Gate 2 | 阻斷 | ✅ PASS（spot-check） | 新增事件性數字（K3 發布/定價、DRAM 漲幅）全部為 2026-07 查核，< 14 天 |
| Gate 2.1 | 阻斷 | ⚠ N/A（本輪未新增「獨家/唯一」類 cornerstone claim） | K3 相關敘述未使用獨家/唯一措辭；沿用既有分歧卡措辭不變 |
| Gate 3 | 阻斷 | ✅ PASS | 單一 ID 發布，無同批次 cross-ID 共用數字待 reconcile |
| Gate 4 | 阻斷 | ✅ **PASS（機器驗證）** | `python3 scripts/validate_id_meta.py docs/id/ID_AIInferenceEconomics_20260720.html` → exit 0 |
| Gate 5 | 阻斷 | ✅ PASS | §0 PM 綠卡（Portfolio Implication judgment-card）五 bullet ＋ j-logic 齊備；conviction=high 與 §6 3🔴 一致，未改動 |
| Gate 6 | 阻斷 | Part A ✅ PASS／Part B ❌ **FAIL（繼承自藍本）** | Part A 文字比 91.2%（≥55%）。Part B：表格數 **11 張（cap 10）**——藍本原始樣稿即為 11 張（本輪未新增 `<table>`，僅在既有 Exhibit 補欄位），非本次整合引入 |
| Gate 7 | 阻斷 | ❌ **FAIL（heuristic 誤判為主，繼承自藍本結構）** | mechanics/stocks 段落有推導行；`valuation`／`debates` 段量化數字多但推導語彙用「怎麼讀」「因果機制」段落敘事而非逐句「推導：」/「→」，觸發此 regex heuristic；此為藍本既有寫法，未在本輪新增內容中復現同類問題（新增段落已含明確推導語句） |
| Gate 8 | 阻斷 | Part A ❌ **FAIL（36.4%＜60%，繼承自藍本＋小幅改善）** ／ Part B ✅ PASS | T1+T1-zh 占比 36.4%（原藍本 33.3%，本輪新增 Moonshot 官方／Epoch AI 兩條 T1 使其小升）；此主題屬快速演變之產業時事類（Kimi K3、中國模型定價），第三方研究/媒體（T3-A/T3）天然占比高，類似 macro 主題的 T1 floor 例外情境，但本 ID 未走該例外流程——如實回報未調整門檻 |
| Gate 9 | 阻斷 | ✅ PASS | 附錄 §1 三次轉折均含具體年月＋量化錨點（2022-11 / 2023-2025 / 2026），未改動 |
| Gate 10 | warning | ✅ PASS | 供需裁決明確（SHORTAGE）；§6 ticker depth 有時間限定（current 2026 區間）；catalyst 雙路徑齊備（§5.1 event-line 皆有 path-pos/path-neg） |
| Gate 11 | 阻斷 | ✅ **PASS（機器驗證，修正後）** | 唯一輸出 `ID_AIInferenceEconomics_20260720.html`；八段機器錨點 summary/thesis/debates/mechanics/valuation/risks/stocks/appendix 全數存在（**發現藍本原用 `id="industry"` 非 `id="mechanics"`、`<header>` 缺 `id="summary"`，本輪已修正**）；appendix 含 2 個 `.evidence-fold`；`_full.html` 不存在；`<script id="id-meta">` 存在 |
| Gate 12 | 阻斷 | ✅ PASS | `kill_metrics[]` 4 條與 §5.2 證偽表 4 列一一對應（metric 名＋bear 閾值一致，未改動）；`sd_verdict/clock_phase/conviction` 與 §0 rating-strip、§3.5 裁決敘事一致；**`priced_in=mid`** 與 Key Debates implication 段落讀數一致（見下方 priced_in 說明） |
| Gate 13' | 阻斷 | ✅ PASS | 寫 id-meta 前已 Read `references/id-meta-schema.md`；`validate_id_meta.py` 全綠 |
| Gate 14 | 阻斷 | ⚠ N/A（本輪定位為呈現升版 refresh，非新裁決） | 未觸發新判斷分岔；裁決值原封不動 |
| Gate 15 | 阻斷 | **partial** | 承重數字對抗查證已由 deep-research workflow 對 Kimi K3 案例執行（104 agents 三票制，主線提供）；completeness critic 已以「中國模型供給衝擊」補洞形式於既有藍本執行；本輪另發現並修正一處來源錯誤（見下方「查證記錄」arXiv 2507.20534 不實引用）；五軸 fan-out N/A（本次為呈現升版 refresh 非裁決級新研究） |
| Gate 16 | 阻斷 | ✅ **PASS（機器驗證）** | debate-card 總數 4（≥3）；`data-debate="external-threat"` 標記 1 張（Debate 4，中國 open-weight 卡）；判別訊號文字存在（5 條，含新增第 5 條記憶體門檻訊號） |
| Gate 13（purity） | warning | ✅ PASS | §6 Exhibit「關聯個股」表新增「純度%」欄；GOOGL/AVGO/NVDA 三檔 tier-list 各附一行 segment 營收 ÷ 總營收推導（見下方摘要） |

**阻斷 Gate 未過**：Gate 6 Part B（表格數 11/10）、Gate 7（valuation/debates 推導 heuristic）、Gate 8 Part A（T1 占比 36.4%/60%）。三項**均為藍本既有結構性特徵，非本輪整合新增**（已用原始 `id_sellside_sample.html` 逐一比對驗證：藍本原始表格數同為 11、T1 占比原為 33.3%、debates/valuation 段落原本就未逐句用「推導：」語彙）。按治理慣例（v3.0 為首發 pilot，非既有生產線批次）如實回報，不強行湊數/灌水/砍表格結構破壞藍本設計，交由主線裁決是否納入 v3.0 pre_publish_check.md 下一輪校準的例外處置（例如仿 macro-analyst 的 T1 floor 例外條款）。

---

## priced_in：mid（新增機器欄）

推導依據（收斂 Key Debates 四卡的 priced-in 檢驗，傾向保守）：
- Debate 1（Jevons 總支出翻倍）：**部分已 price**（hyperscaler capex 估值已反映支出上升）。
- Debate 2（毛利三層分裂）：**未 price**（市場仍把推論鏈當同一多頭）——最大 optionality，拉低整體 priced_in。
- Debate 3（frontier lab 毛利升 70%）：**已 price**（私募估值假設 70% margin 路徑兌現）——若不達即重定價，拉高整體 priced_in（風險已被定價但脆弱）。
- Debate 4（中國 open-weight）：**部分已 price**（7–34× 價差、OpenRouter 61% 滲透已廣泛報導），但 K3 牌價逆勢上漲 3 倍顯示市場尚未完全「清算」commodity 層地板持續探底的假設。

四卡有兩卡「未/部分 price」、一卡「已 price 且脆弱」、一卡「部分 price 但有反向新訊號」——不騎牆但也不誇大 optionality，收斂為 **mid**（不選 low，因 Debate 3 的私募估值假設已充分定價；不選 high，因 Debate 2 仍是可操作的錯誤定價）。

---

## 🔴 純度三檔推導摘要

| Ticker | 推導 | 來源 | as-of |
|:---|:---|:---|:---|
| GOOGL | Google Cloud $20.03B ÷ Alphabet 總營收 $109.9B → **~18%** | Alphabet 2026Q1 10-Q / Yahoo Finance 財報報導 | 2026Q1（2026-04 公告） |
| AVGO | AI 半導體營收 $10.8B ÷ 總營收 $22.2B → **~49%** | Broadcom FY2026 Q2 財報公告 | FY26 Q2（2026-06 公告） |
| NVDA | Data Center 營收 $75.2B ÷ 總營收 $81.6B → **~92%** | NVIDIA FY2027 Q1 8-K | FY27 Q1（2026-05 公告） |

三檔均為 mega-cap 綜合體，purity 用**最貼近的揭露段別**（Cloud／AI 半導體／Data Center）作代理，非純 inference 拆分——已在報告內以括號註明限制（GOOGL 純度未計入 TPU 自用效益、實際曝險更高；NVDA 純度含訓練與推論混合、為保守上界）。查不到可靠拆分時本應降 🟡，但三檔均有可靠 segment 揭露，維持 🔴。

---

## Step 1 內容整合摘要

融入位置：Debate 4 證據鏈（我們認為／判別訊號兩格延伸＋evidence-fold 新增 1 條來源）、§3.3「中國模型供給衝擊」小節（新增 2 段：Kimi K3 技術根＋serving 記憶體門檻／牌價反轉，evidence-fold 新增 7 條來源）、§5 風險與證偽 implication callout（新增第 ③ 條記憶體／HBM 監測點一句）、Key Points 第 6 條與 rating-strip Priced-in 格（輕度延伸）。裁決值（SHORTAGE／Phase II／HIGH conviction）全程未動。

**查證記錄（重要）**：任務簡報原列來源含「arXiv 2507.20534」作為 Kimi K3 一手技術報告（48 稀疏度省 1.69× FLOPs／64 對 128 attention heads 省 83% FLOPs 等具體數字）。獨立 WebSearch 查核發現 **arXiv 2507.20534 實際是《Kimi K2: Open Agentic Intelligence》論文**（2025-07 submission，K2 非 K3；K3 於 2026-07-16 發布，時序上不可能被一篇 2025-07 的論文描述）。判定為來源誤植，**未採用**該 arXiv 引用與其附帶的specific 數字（48/1.69×/64v128/83%），改用可獨立驗證的公開數字替代：
- K3 規格：2.8T 總參數、896 expert／16 啟動（≈1.8% 稀疏度）、KDA＋Gated MLA、IndexShare 稀疏索引器（1M context 下 FLOPs 降約 2.9×、解碼加速 6.3×）——來源 Moonshot 官方 blog（kimi.com/blog/kimi-k3）＋MarkTechPost 2026-07-16。
- K2.x serving 硬體門檻（959GB 權重／1,347GB 閒置 vRAM／8×B200 或 16×H100）——來源 Lambda 官方部署指南（lambda.ai/blog/how-to-serve-kimi-k2-instruct-on-lambda-with-vllm，獨立查核）。
- B200 NVFP4 serving 成本 $0.14/M tokens——來源 SemiAnalysis InferenceX（inferencex.semianalysis.com，獨立查核，與任務簡報數字一致）。
- Epoch AI「GPT ~50% 毛利／Kimi 近成本價 serving」——獨立查核確認（epoch.ai/gradient-updates/is-a-compute-crunch-coming），與任務簡報論點一致。
- K3 官方牌價 $3／$15（cache-miss）較 K2.6（$0.95／$4.00）漲幅 ~3.1–3.75×——獨立查核確認「~3 倍」措辭成立。
- DRAM 合約價 2026Q1 QoQ +90~95%（TrendForce）、SK hynix 短缺展望至 2030——獨立查核均確認。

其餘任務簡報數字（DRAM 漲幅、記憶體 BOM 佔比、750B FP8 記憶體門檻概算等）因效力/時間預算未逐一覆核，但與已驗證數字量級一致、無矛盾跡象。

---

## Step 2 — id-meta 變更摘要

- `skill_version`: v2.3 → **v3.0**；`id_version`: v2.0 → **v3.0**；`publish_date`: 2026-04-30 → **2026-07-20**
- 新增 `priced_in: "mid"`（見上）
- `related_tickers[]`：GOOGL/AVGO/NVDA（僅 🔴 depth）新增 `purity_pct`（18/49/92）；🟡🟢 檔位依 schema 選填未動
- `sections_refreshed.market` / `.judgment`：2026-06-20 → **2026-07-20**；`.technical` 保留 2026-06-20（技術根章節本輪未實質改動）
- `now_state`/`future_state`/`action`：**檢視後判定無需更動**——裁決不變、既有措辭仍準確涵蓋毛利分層結構性判斷，新證據（K3）屬於強化既有機制而非改變方向

**Gate 11 連帶修正**：藍本原用 `id="industry"`（非 v3.0 規格的 `id="mechanics"`）且 `<header class="masthead">` 缺 `id="summary"`——不符 `templates/report_template.md` 定義的八段機器錨點。已修正為 `id="summary"`（header）與 `id="mechanics"`（§3），並同步更新 sticky TOC 連結 `#industry`→`#mechanics`。此為技術性修正，不影響任何裁決或敘事內容。

---

## Step 3 — 落檔與索引同步結果

| 動作 | 結果 |
|:---|:---|
| `docs/id/ID_AIInferenceEconomics_20260720.html` | 新建，112,613 bytes |
| `docs/id/INDEX.md` | 已 append 一行（2026-07-20） |
| `docs/id/index.html` topic-card | 連結改指新檔／badge 改「v3 敘事版」／data-search 補「kimi k3 deepseek 中國模型」 |
| `scripts/build_id_category_pages.py` | ✅ exit 0，14 個 cat-*.html 重生 |
| `scripts/id_dd_mapping.py` | ✅ exit 0，`portfolio/id_dd_map.json` 重建（92 IDs／236 DD tickers／118 overlap） |
| `scripts/retrofit_dd_id_banner.py` | ✅ exit 0，342 份 DD banner 更新（含 GOOGL/AVGO/NVDA 等舊 20260430 連結旁新增 20260720 連結）、239 份無對應 ID 跳過 |
| `scripts/check_tier_matrix.py` | ✅ exit 0，僅既有提示（未涵蓋 ticker 建議、ASML/NET 近期 DD 更新提示），與本次發布無關 |
| `scripts/qc.py`（changed-files 模式） | ✅ exit 0，385 檔掃描，0 errors，1703 warnings（**新檔與兩份索引檔零警告**；warnings 全數來自本輪未觸碰的其他既有檔案，屬並行工作樹既有狀態） |

**注意（供主線 commit 範圍判斷）**：`retrofit_dd_id_banner.py`／`id_dd_mapping.py`／`build_id_category_pages.py` 為全庫掃描型腳本，運行後 `git status` 顯示 358 份 `docs/dd/DD_*.html`＋14 份 `docs/id/cat-*.html`＋`portfolio/id_dd_map.json` 一併變動（banner 重新定位＋ID 清單刷新，皆為既有腳本冪等行為，非本次新增邏輯）。另外，working tree 本身已有一批與本任務無關的 uncommitted 變更（`.claude/skills/industry-analyst/*`、`knowledge/rule_ledger.md`、`scripts/validate_id_meta.py` 等——判斷為主線同時進行的 v3.0 skill 基礎設施建置，非本 agent 產生）。commit 範圍請主線自行核實界定，本 agent 未做任何 git 操作。

---

## 硬規則自查

- 中文全形標點：新增內容已用全形（，。：；「」）；`qc.py` 對本次新增/編輯的三個檔案（新 HTML／INDEX.md／index.html）零警告。
- Changelog 語氣：正文未出現「本次補上」「新增於」等詞；masthead byline／report-colophon 使用「v3.0 呈現版 · 原始 thesis 建立於 2026-04-30」屬 sell-side 報告慣用 metadata 措辭（非 changelog 散文），與既有站內慣例（如 v2.3 版本已用「v2.3 改版」字樣）一致。
- 未動 scratchpad 原始 sample、未動 `docs/id/` 其他檔案（僅新檔＋INDEX.md＋index.html 該卡片區塊）、未做任何 git add/commit/push 操作。
