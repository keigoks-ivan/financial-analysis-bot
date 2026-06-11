---
name: industry-ds
description: 【DEPRECATED 2026-06-11】已併入 industry-analyst v2.0 — 所有 DS 觸發語（「{主題} ds」「敘述報告」「供需循環」「discourse」）改觸發 industry-analyst。本檔保留供 legacy DS 報告維護參考。原 DS skill：與 industry-analyst（產業 ID）並列的姊妹 skill，輸入產業主題執行三軸研究，輸出 11 章節、文字 ≥ 80% / 表格 ≤ 20%、以「歷史 → 現供 → 未供 → 現需 → 未需 → 短中長期推估」為敘事骨架的 HTML 報告（docs/ds/DS_*.html）。
version: v1.2
date: 2026-05-13
---

# industry-ds skill v1.2 — 【DEPRECATED 2026-06-11】

> ## ⛔ DEPRECATED — 已併入 industry-analyst v2.0
>
> **狀態**：本 skill 自 2026-06-11 起停用，不再產出新報告。
>
> **為什麼合併**：DS（敘述供需循環，深入淺出好讀）與 ID（表格 dashboard，決策密度高）長期是並列姊妹 skill，但同 theme 常要兩邊各跑一份、內容重疊、維護雙線。industry-analyst v2.0 把兩者合成單一「敘事為骨、表格為窗」的產業深度報告：用 DS 的因果敘事弧當骨架，把 ID 的決策資產（PM 結論、玩家矩陣、利潤池、估值傳導、證偽表）當器官嵌入對應章節，並吸收 DS 的因果閉合、推導鏈、§末 aside 來源系統與可讀性規則層。
>
> **新去處**：所有原 DS 觸發語（「{主題} ds」「ds {主題}」「{產業} 敘述報告」「分析 {產業} 的供需循環」「{產業} 歷史與未來」「discourse {industry}」）一律轉向 `industry-analyst`（v2.0），輸出寫到 `docs/id/`（不再寫 `docs/ds/`）。
>
> **8 份 legacy DS 報告如何維護**：既有 8 份 `docs/ds/DS_*.html` 凍結為 legacy，**檔案不動、不 retrofit、不遷移**。若需要 review / patch / 驗證某份 legacy DS，走 `id-review --mode ds`（DS-mode 檢查清單仍在）；**不要用本 skill 生新 DS**。所有 plumbing（`validate_ds_meta.py` / `build_ds_category_pages.py` / `init_ds_index.py`）僅供 legacy DS 維護參考。
>
> **本檔以下內文全部保留供歷史參考**，描述的是停用前的 v1.2 行為。

## v1.2 變更記錄（inline → aside 遷移）

**背景**：v1.1 為每個量化斷言強制附加 inline `<span class="source-tag">[T1: <a href="URL">長英文來源標題</a>]</span>`，審計性大幅提升，但一份 ~7,500 字中文敘述報告出現 39 條 inline tag，長英文 source title 頻繁中斷中文段落，閱讀流嚴重受損（用戶反饋）。

**設計決策**：保留 source-tag 的所有內容（tier、URL、title、claim summary），但把位置從 inline 移至每節末的 `<aside class="ds-refs">` 參考區塊。讀者能在章節末尾一次查看該章所有來源，不受行文干擾。

**保持不變**：
- `推導：` ds-derive 行（Step 8 的 `<span class="ds-derive">` / `<div class="ds-derive">`）— 這是數學推導可追溯性，與 source-tag 不同，**不移動、不刪除**
- T1 占比 ≥ 50% 規則（改為計算各節 `<aside class="ds-refs">` 的 `[T1]` 條目總數）
- Critic DS-7 source 抽查（改為抽 aside refs，不再抽 inline tags）
- Tier 階層表（T1/T2/T3-A/B/C/T4）完全沿用

**變更項目**：
- 正文與表格內**不再**使用 `<span class="source-tag">` inline tag
- 每個 `<section>` 結尾加 `<aside class="ds-refs">` 列出該節所有引用來源（按 URL 去重）
- Gate 12 / QC-DS13 / DS-7 重寫為檢查 aside 格式
- 字數上限從 7,500 降回 4,000–6,500（移除 inline tag 佔位空間）
- 既存 v1.1 DS 檔案需用 `scripts/retrofit_ds_references.py` 遷移

## 【八大原則】（v1.3：Rule 1 放寬為敘述+bullet hybrid；v1.2：Rule 7 格式從 inline 改為 aside）

1. **敘述為主、條列為輔、表格為錨點**：DS 的核心是「為何今天到這裡 → 未來會去哪裡」的**因果敘事**，不是 dashboard。文字 ≥ 80%（含 bullet 內字數），表格 ≤ 20%。**v1.3 新**：段落 vs bullet 由內容決定 — 因果鏈、漸進推理、論證展開保留段落敘事；3+ 平行同類項目、對稱結構、無因果列舉一律 bullet。詳見【敘述 vs 條列判準】段。如果一章可以全用表格表達 → 它屬於 ID 不屬於 DS。
2. **供需循環骨架（不可動）**：§1 歷史 → §2 現在供給 → §3 未來供給 → §4 現在需求 → §5 未來需求 → §6 短中長期推估，這六章是 DS 的脊椎，章節順序與標題固定，**不可重排、不可刪節**。其他章節（§0、§7-§11）支撐主敘事。
3. **顯式因果鏈（v1.1 強化：閉合在對的章節）**：§1（歷史）每個 inflection point 必須在 §3（未來供給）或 §5（未來需求）中至少有一段直接回答「該變數是否仍 binding / 是否正在轉折」。**§8 Non-Consensus 不算閉合點** — §8 是「市場看法 vs 我們」，不是「歷史 → 未來」的因果橋。例：§1 寫 CUDA 軟體護城河 → §3 必須有「CUDA 在 inference 階段競爭強度評估」段，不能延後到 §8。
4. **供需平衡必須結論**：§3 未來供給 + §5 未來需求合在一起必須給出「平衡 / 過剩 / 短缺」的明確判斷，否則 §6 推估缺基礎。不允許「未來供給可能 X 也可能 Y」這種模稜兩可。
5. **短中長期三 horizon 三情境**：§6 必須拆 12M / 3Y / 5Y+ 三個時間窗，每個窗口給 base / bull / bear 三情境（這是 DS 唯一允許用表格錨點的章節之一）。
6. **與 ID 互補不取代**：DS 不重複 ID 的工作。若同 theme 已有 ID，DS §0 頂部 callout 指回該 ID，DS 內容專注於「ID 表格沒展開的敘事脈絡」。`ds-meta.related_ids[]` 必填指向所有相關 ID。
7. **可審計性（v1.2：改為 §末 aside）**：量化斷言正文中**不再**插入 inline `<span class="source-tag">`。改為每節結尾加 `<aside class="ds-refs">` 區塊，列出該節所有引用來源（按 URL 去重，tier 標示），讀者能在章節末尾查閱完整出處。T1 來源占比 ≥ 50%（計算全文所有 aside 裡的 `[T1]` 條目數 / 所有 aside 條目總數）；單 T3 來源必須 ⚠️ 警示。詳見【來源標籤系統】段。
8. **推導可追溯性（v1.1 新增）**：被當作「結論」的數字（TAM、CAGR、市占、滲透率、目標價、capex 規模），在初次出現的同段或前一段必須附 ≤ 3 行推導：`推導：<input1> + <input2> → <calculation> → <implication>`。讀者能從前文 input 重建結論，拒絕「黑盒數字」。詳見【推導可追溯性原則】段。

---

## 【路徑】

```
~/.claude/skills/industry-ds/
  SKILL.md                         # 本檔
  templates/
    html_template.md               # HTML 視覺 & CSS 規範
    schema_fields.md               # 11 章節必填 / 選填欄位
  pre_publish_check.md             # 預發布 10 道閘門
  references/                      # 案例與 best practice 參考
```

輸出：

```
financial-analysis-bot/
  docs/ds/
    INDEX.md                       # 產業 DS 索引
    index.html                     # DS 列表首頁（由 scripts/init_ds_index.py 初始化、industry-ds 插入新卡片）
    DS_{Theme}_{YYYYMMDD}.html     # 單份 DS 報告
    cat-{mega}.html                # 分類 drilldown 頁（由 scripts/build_ds_category_pages.py 重新生成）
    taxonomy.md → ../id/taxonomy.md  # symlink / pointer，分類體系與 ID 共用
```

驗證腳本：

```
scripts/
  validate_ds_meta.py              # ds-meta JSON 欄位驗證（pre-commit hook 會跑）
  build_ds_category_pages.py       # 從 index.html 重新生成 15 個 cat-*.html
  init_ds_index.py                 # 一次性 bootstrap（從 docs/id/index.html 轉換出 docs/ds/index.html）
```

---

## 【11 章節 Schema】

| § | 標題 | 主要形式 | 表格 | 字數目標 | Insight 必填 |
|:---|:---|:---|:---:|:---|:---|
| **§0** | TL;DR + ds-meta + cross-link callout | 短敘述 + JSON meta block | meta（不計） | 100-200 | 一句話 thesis |
| **§1** | 產業歷史脈絡 | 純敘述 | 0 | 400-700 | 2-3 個歷史轉折點與類比 |
| **§2** | 現在供給結構 | 敘述 + 1 小表（top suppliers / capacity） | 1 | 300-500 | 誰是議價權核心、哪裡是瓶頸 |
| **§3** | 未來供給趨勢 | 純敘述（capex pipeline / 新進入者 / 彈性） | 0 | 400-600 | 12-36M 內供給能否回應需求 |
| **§4** | 現在需求結構 | 純敘述（end-market mix / 地域 / driver） | 0 | 300-500 | 哪一塊需求最不可替代、最有定價權 |
| **§5** | 未來需求趨勢（含 TAM + CAGR） | 敘述 + 1 小表（TAM/CAGR 多情境） | 1 | 400-700 | TAM forecast 史上偏差、需求拐點 |
| **§6** | 短 / 中 / 長期推估 | 敘述 + 1 表（base/bull/bear × 12M / 3Y / 5Y+） | 1 | 500-800 | 三情境各自的 trigger 事件 |
| **§7** | 投資時鐘 + Phase 轉換訊號 | 純敘述（current phase + 下一階段切換點） | 0 | 300-500 | I→II / II→III 必要充分條件 |
| **§8** | Non-Consensus View | 純敘述（3 條 vs 市場共識的具體分歧） | 0 | 400-700 | 共識說 X、本 DS 看 Y、分歧原因 |
| **§9** | 風險與 Kill Scenario | 純敘述（3 條最有力反方論證，每條一段） | 0 | 400-600 | 各條反方的 trigger metric + 時間窗 |
| **§10** | Catalyst Timeline | 敘述為主 + 內聯時間錨點 `<time>` / `<strong>` | 0 | 300-500 | 未來 18M 5-8 個關鍵節點 |
| **§11** | 關聯個股清單 | 表格（**stock-analyst hook，必填**） | 1 | 100-300 | 1-2 檔 non-obvious beneficiary |

**總字數目標**：4,000-6,500 字（v1.2：inline source-tag 移出正文後空間釋放，上限從 7,500 降回 6,500）。表格數量上限 4 張，每張行數上限 8 行（§11 例外可至 16 行）。

### 章節順序硬性規則

§0 → §1 → §2 → §3 → §4 → §5 → §6 → §7 → §8 → §9 → §10 → §11

**不可變動**：§2-§3-§4-§5 必須這個順序（現供 → 未供 → 現需 → 未需），這個四段式是供需平衡推導的脊椎。§6 必須在 §2-§5 之後，因為它依賴前面四章的結論。

### 每章敘述結構建議（不強制，但鼓勵）

每章末尾用一段 **「💡 對投資的意義」**（≥ 1 段，2-4 句），把該章的事實連回投資判斷。這是 DS 的 insight layer 入口。

---

## 【來源標籤系統】（v1.2：從 inline 改為 §末 aside）

### 為什麼這節重要

DS 是敘事報告，但敘事不等於「沒有出處的觀點」。每個量化斷言都必須能被獨立驗證 — 這是 DS 從「個人意見書」升格為「機構級研究」的關鍵。v1.0 無 source 強制；v1.1 引入 inline `<span class="source-tag">` 解決了可審計性問題，但 39 條 inline tag 嚴重破壞中文閱讀流。v1.2 把 source 內容保留（tier、URL、title、claim summary），位置從 inline 移至每節末的 `<aside class="ds-refs">` 參考區塊。

### 格式（v1.2：§末 aside）

每節正文與表格中**不使用 `<span class="source-tag">`**。每節結尾（`</section>` 之前）加：

```html
<aside class="ds-refs">
  <span class="ds-refs-label">本節參考來源</span>
  <ol>
    <li><span class="tier">[T1]</span><a href="https://nvidianews.nvidia.com/.../gtc-2026-keynote">NVIDIA GTC 2026 Keynote slide 47 — H100 配給 lead time 12+ 個月</a></li>
    <li><span class="tier">[T2]</span><a href="https://www.semi.org/report-xxx">SEMI 2025 Advanced Packaging Report — CoWoS capacity 2026-2027</a></li>
    <li><span class="tier">[T3-A]</span><a href="...">Morgan Stanley AI Infra Primer 2026-03-15 p.24 — ASIC capex share forecast</a></li>
    <li><span class="tier">[T1-zh]</span><a href="...">台積電 2026Q1 法說會 slide 14 — CoWoS 配額分配</a></li>
  </ol>
</aside>
```

CSS（HTML 模板已含）：

```css
.ds-refs{margin:28px 0 8px;padding:10px 14px;background:#FAFAF9;border-left:2px solid #D1D5DB;border-radius:3px;font-size:12px;color:#6B7280;line-height:1.7}
.ds-refs .ds-refs-label{color:#4B5563;font-size:10.5px;letter-spacing:.5px;text-transform:uppercase;display:block;margin-bottom:6px;font-weight:700}
.ds-refs ol{margin:0;padding-left:20px}
.ds-refs li{margin:3px 0}
.ds-refs a{color:#475569;text-decoration:none}
.ds-refs a:hover{text-decoration:underline}
.ds-refs .tier{display:inline-block;color:#4B5563;font-weight:600;margin-right:6px;font-size:11px}
.source-warning{background:#FEF3C7;border-left:3px solid #F59E0B;padding:10px 14px;margin:14px 0;font-size:12px;color:#78350F;border-radius:3px}
```

**Aside 編排規則**：
- 同一節內 URL 相同的來源只列一次（取第一次出現的 tier + title）
- `<li>` 按節內首次出現順序排列（T1 優先並不強制重排，保留閱讀順序）
- 每條 `<li>` 格式：`<span class="tier">[TX]</span><a href="URL">Source title — claim/page（可選）</a>`
- 若某節**無任何量化斷言**（如 §7 純敘述 phase 分析），aside 可省略
- §0 TL;DR 若 thesis box 含數字 → 加 aside；若只有敘述 → 可省略

### Tier 階層（完整與 ID 共用）

| Tier | 類別 | 範例 |
|:---|:---|:---|
| **T1 / T1-zh** | 公司 IR / earnings transcript / 10-K / 行業協會 / 政府機構 | NVIDIA GTC、AMD Advancing AI、TSMC Symposium、Apple WWDC、SEMI、SIA、Yole、IEA、USDA、IDC、Gartner、Fed、ECB、BLS、Eurostat、台股 MOPS、台積電 IR |
| **T2 / T2-zh** | 權威三方財經媒體 / 研究機構 | Bloomberg、Reuters、FT、WSJ、Nikkei、Yole Group、IC Insights、TechInsights、JEDEC、IEEE Xplore、ITRI IEK、MIC、TrendForce、CINNO |
| **T3-A** | 賣方產業 primer / 深度 channel check | Morgan Stanley AI Infra Primer、TD Cowen Advanced Packaging Deep-Dive、Goldman Pharmaceuticals 2030、JPM Semi Capex Outlook |
| **T3-B** | 賣方個股報告 / 主流財經媒體 | 賣方個股 target price update、Barron's、Forbes、Fortune |
| **T3-C** | 專業媒體 / 署名 Substack | AnandTech、SemiAnalysis、Tom's Hardware、SemiWiki、Stratechery、DIGITIMES、電子時報；**署名分析師（Dylan Patel、Ben Thompson、Ming-Chi Kuo）可信度升至 T3-A** |
| **T4** | 匿名社群 / wiki | Reddit、Twitter（非官方）、PTT、Mobile01、Wikipedia 數字（歷史時間軸可用） |

### 硬性規則

| 規則 | 細節 |
|:---|:---|
| **T1 占比 ≥ 50%**（QC-DS13）| 全文所有 `<aside class="ds-refs">` 條目中，`[T1]` + `[T1-zh]` 比例 ≥ 50%。低於則返工，補 T1 來源 |
| **量化斷言必在 aside 中有出處**（Gate 12）| 每個含量化斷言的 `<section>` 結尾必須有 `<aside class="ds-refs">` 且至少一條 `<li>`；正文不再要求 inline tag |
| **T4 禁止獨立使用**（QC-DS15）| T4 來源必須有 T1 或 T2 交叉驗證才可列入 aside；單獨用 T4 → 返工換來源 |
| **T3 單獨使用警示**（QC-DS15）| 若某節 aside 全為 T3、無 T1/T2 → 節末加 `<aside class="source-warning">` 警示段 |
| **事件 14 天 / 結構 60 天 freshness**（QC-DS14）| event-triggered claims（earnings、capex 公告、訂單、財報數字）source 必須在 14 天內；structural claims（技術代際、TAM 結構）60 天 |

### 免 aside 例外

以下情況節末 aside 可省略：
- 整節無量化斷言（全為定性敘述或廣為人知歷史事件）
- §0 thesis box 只含定性判斷，無具體數字

以下「數字」可不在 aside 中出現（免計入 T1 占比分母）：
- 純結構性敘述（"NVDA 主導 GPU 市場"、"中國是最大 EV 市場之一"）
- 廣為人知的歷史事件時間點（"ChatGPT 2022-11 發布"、"COVID 2020 爆發"）
- 純定性判斷（"我們認為..."、"似乎指向..."）
- 同節 aside 已列出 source 的同一數字在正文複次引用

### 引用衝突處理

- 同一數字能同時被 T1 + T2 驗證 → 只標較高 tier（T1）
- 中文 T1 與英文 T1 衝突（如 TrendForce vs Yole）→ 在 §5 表格同時列兩數並註明差異
- 賣方 primer T3-A 與公司 T1 IR deck 衝突 → IR deck 為準，T3-A 可作 §8 反方依據

### 設計理念：為什麼是 aside 而不是 inline 或 footnote

- **v1.1 inline `<span class="source-tag">`**：解決了可審計性，但 39 條長英文 source title 嵌在中文敘述裡破壞閱讀流
- **傳統 footnote（`<sup>[n]</sup>` + footer 區塊）**：需要維護 numbering，跨節引用麻煩，且引入第三套 citation 機制
- **v1.2 aside**：每節末一個小盒子，讀者可選擇跳過或查閱；正文完全乾淨；Tier/URL/claim 全部保留；critic 可抽查整個 aside 列表而非逐行掃 inline
- `scripts/validate_source_blacklist.py` 仍可對 aside 中的 URL 一視同仁檢查

---

## 【推導可追溯性原則】（v1.1 新增，從 stock-analyst v12.2 移植）

### 為什麼這節重要

source-tag 解決「**數字來自哪裡**」；推導行解決「**為什麼是這個數字而不是別的**」。

舉例：§5 TAM 表格寫「2026E base case $280-320B / bull $340-380B / bear $230-260B」 — 三個 case 各有 source，但 bull 比 base 高 +20%、bear 比 base 低 -25%。讀者問：「**+20% 從哪個假設變動推出來？**」如果 DS 答不出來，PM 就無法獨立判斷此 thesis 是否成立。

### 規則（硬性）

任何被當作「結論」的數字（TAM、CAGR、market share、滲透率、ASP、產能、capex 規模、bull/bear delta），在初次出現的**同段或前一段**內，必須附 ≤ 3 行推導，格式：

```
推導：<input1> + <input2> + <input3> → <calculation> → <implication>
```

範例：

> 2026E TAM base case 落在 **$280B**。
> 推導：hyperscaler capex $600B（GOOG/MSFT/META/AMZN 三年 CAGR 35%）× AI infrastructure 工作負載 35% × 加速器（GPU + ASIC）占 AI infra 比 1.33 → $280B。
> 此 base 假設 hyperscaler capex 兌現度 100%；若 capex 兌現 75%（衰退衝擊）→ bear case $230B；若兌現 120%（FOMO 加碼）→ bull case $340B。
> （本節末 `<aside class="ds-refs">` 列出 hyperscaler capex $600B 數字的 T1 來源）

### 章節覆蓋（硬性）

| 章節 | 必須推導的數字類型 |
|:---|:---|
| **§5（未來需求）** | TAM 三情境、CAGR、demand inflection 年份預測 |
| **§6（短中長期推估）** | 三 horizon × 三 case 的所有量化 cell；其中 bull/bear 與 base 的偏離必須由「假設改了什麼」推出 |
| **§7（投資時鐘）** | phase 轉換的必要 / 充分條件（量化閾值） |
| **§9（Kill Scenario）** | 三條反方論證的 trigger metric + 時間窗 |
| **§11（ticker depth 閾值）** | depth label（🔴/🟡/🟢）的判定門檻（如「🔴 = AI rev ≥ 40%」），如果是 forward-looking 閾值，必須註明時間基準 + 當前 actual |

### 與 source-tag 的分工

- source-tag 標「**input 數字從哪裡來**」（如 hyperscaler capex $600B 的 T1 來源）
- 推導行標「**input → output 怎麼算出來**」（hyperscaler capex × workload mix × accelerator ratio）

兩者疊加 → PM 可以從 input 來源驗證每個 input，再從推導行驗證 output 計算 → DS 結論完全可審計。

### Anti-pattern（必須避免）

- ❌「我們估 2026E TAM $300B」← 無 input、無推導、節末 aside 無對應來源
- ❌「TAM 約 $300B」← 無推導，節末 aside 也沒有對應 T1/T2 來源 → PM 無法獨立驗證
- ✅「TAM $300B。推導：$600B × 35% × 1.33 → $280-320B base range」+ 節末 `<aside class="ds-refs">` 列 [T1] hyperscaler capex 來源 ← 推導 + aside 都齊全

### 違反處置

`pre_publish_check.md` Gate 13 自動掃 §5/§6/§7/§9/§11 是否有「推導：」或等效標記（如「→」「換算」「計算」開頭的短行），缺一即 fail。

---

## 【§1 歷史錨點規則】（v1.1 新增）

### Why

v1.0 §1 只要求「2-3 個歷史轉折點 + 1-2 個歷史類比」，但沒規定錨點精度。AI Accelerator DS v1.0 出現「ChatGPT-Hopper 配給」這種口語式錨點 — 沒有 H100 launch 具體日期（2023-03）、沒有 ChatGPT MAU 100M 達成時間（2023-01-31）。讀者只能「知道有這事」、無法把錨點當 timeline 用。

### 規則（必須）

§1 中每個 inflection point 段落（通常 2–4 段）必須同時包含：

1. **具體日期或月份**：YYYY 或 YYYY-MM 格式（不允許「過去幾年」「最近」「近期」這類模糊表述）
2. **至少一個量化錨點**：價格、性能指標（TFLOPS / GB / 頻寬）、市占、capacity（GW / wafers）、用戶數、營收

### 範例對比

❌ **v1.0 寫法（口語）**：「ChatGPT 興起後，NVDA H100 變成稀缺品」
✅ **v1.2 寫法**：「**2022-11-30 ChatGPT 發布**，兩個月內 MAU 衝破 1 億；**2023-03 H100 launch** 時 hyperscaler 已開始大量採購；**2023-Q3 NVDA DC 營收同比 +279%**，第一次出現 12+ 個月 lead time 配給」（來源在節末 aside 中列出：ChatGPT MAU source、NVDA 23Q3 earnings T1）

### Critic 檢查（DS-9）

§1 每段正則檢查 `\b(19|20)\d{2}\b` 日期 + 至少一個數字（% / $ / x / GW / TFLOPS / GB / MAU / B / M 等）。違反 → 🟡 PARTIAL_ERROR（不阻擋發布但要求 patch）。

---

## 【§11 ticker depth 時間限定規則】（v1.1 新增）

### Why

v1.0 §11 caption 寫「🔴 = AI rev ≥ 40% of total」但沒指明時間基準，讀者不知道是 current actual 還是 forward-looking。AI Accelerator DS v1.0 把 AMD 標 🔴（forward-looking 2027-2028），但 AMD 當前 AI rev ~8%，造成「現在不到 10% 怎麼標 🔴」的疑惑。

### 規則（必須）

§11 caption 中的閾值定義必須明示時間基準：

- **Current actual**：「🔴 = current AI rev ≥ 40%（as of 2026-Q1）」
- **Forward-looking**：「🔴 = projected AI rev ≥ 40% by 2027-2028」+ 表格每個 ticker 行另列「current YYYY actual」對照欄
- **混合**：兩個閾值並列（current X、projected by Y）

### 範例

✅ **v1.1 寫法（forward-looking 顯示對照）**：

| Ticker | 角色 | Depth | Current AI rev (2026E) | Forward AI rev (2028E) | 對應 DD |
|:---|:---|:---:|:---:|:---:|:---|
| NVDA | primary supplier | 🔴 | 78% | 85% | DD_NVDA_... |
| AMD | secondary supplier | 🔴 | 8% | 45% | — |
| AVGO | ASIC design | 🟡 | 25% | 50% | — |

Caption 註：「🔴 = projected AI rev ≥ 40% by 2028。AMD 雖 current 8%，但 projected 45% → 標 🔴。」

### Critic 檢查（Gate 14）

§11 表格如有「>X%」「≥Y%」「by YYYY」字樣，必須在同 caption 或下方 footnote 註明時間基準。違反 → 🟡 PARTIAL_ERROR。

---

## 【ds-meta JSON Schema】

每份 DS HTML 必須在 `<head>` 內包含這個 block：

```html
<meta name="ds-skill-version" content="v1.2">
<meta name="ds-theme" content="{Theme_CamelCase}">
<meta name="ds-publish-date" content="{YYYY-MM-DD}">
<script id="ds-meta" type="application/json">
{
  "theme": "{Theme 中文或英文敘述句}",
  "skill_version": "v1.2",
  "ds_version": "v1.0",
  "publish_date": "{YYYY-MM-DD}",
  "thesis_type": "structural | event-triggered | mixed",
  "ai_exposure": "🟢 | 🟡 | 🔴",
  "mega": "semi | bio | cloud | ... (15 個白名單，見 docs/id/taxonomy.md)",
  "sub_group": "memory | glp1 | ...（對應 mega 下的白名單）",
  "quality_tier": "Q0 | Q1 | Q2",
  "oneliner": "{≤ 200 字，本 DS 核心 thesis 一句話，不可截斷}",
  "history_window_years": 25,
  "forecast_horizon_years": 5,
  "related_tickers": [
    {"ticker": "NVDA", "role": "primary supplier", "depth": "🔴", "beneficiary": true},
    {"ticker": "AMD",  "role": "secondary supplier", "depth": "🟡", "beneficiary": true}
  ],
  "related_ids": ["ID_AIAcceleratorDemand_20260419"],
  "sections_refreshed": {
    "history": "2026-05-12",
    "supply_demand": "2026-05-12",
    "forecast": "2026-05-12"
  }
}
</script>
```

### 欄位差異 vs id-meta

- `ds_version`（取代 `id_version`）
- `history_window_years`（DS 特有，1-200，標示 §1 回顧多遠）
- `forecast_horizon_years`（DS 特有，1-30，標示 §6 推估到幾年後）
- `related_ids[]`（同 theme ID 列表，用於 §0 callout 與 stock-analyst 整合 dedup）
- `sections_refreshed` buckets 改為 `history / supply_demand / forecast`（ID 是 `technical / market / judgment`）

### 鮮度（freshness）半衰期

- `history`（§1）：730 天（產業歷史變動緩慢）
- `supply_demand`（§2-§5）：180 天（供需結構半年內可能位移）
- `forecast`（§6）：60 天（推估窗口最容易過期，需勤刷新）

逾期 → INDEX.md 鮮度欄位變色（🟡 → 🟠 → 🔴），critic gate 會標 stale。

---

## 【敘述 vs 條列判準】（v1.3 新增）

v1.0-v1.2 硬規「不用 bullet」造成的問題：所有章節被迫寫成大段中文，scan 困難、讀體驗疲勞。但全 bullet 化又會跟 ID 重疊（ID 已經是 scan 型）。v1.3 改為**內容驅動格式**：

### 該 bullet 的徵兆（任一即 bullet）

- **3 個以上平行同類項目**：多個 catalyst、多個 falsification metric、多個情境 trigger、多個玩家比較點
- **對稱結構描述**：每項都是「項目名：屬性 + 數字 + 影響」這種同模板
- **無因果列舉**：top 5 玩家、4 個關鍵假設、3 個短中長期 trigger metric、Kill scenario 三條反方論證

### 該保留敘事的徵兆（任一即敘事）

- **因果鏈 A→B→C**：歷史轉折推理、供需閉合、推導展開
- **漸進論證**：一段話一個結論，下段繼續延伸（如 §1 ChatGPT 引爆 → §3 CUDA inference 護城河 → §6 ASIC 攻擊路徑這種多段推進）
- **解釋「為何」**：解釋一個現象成因 / 機制 / 路徑

### 章節傾向（建議，非硬性）

| 章節 | 預設格式 | 何時切換 |
|---|---|---|
| §0 TL;DR | thesis box + 1 段 narrative | （固定） |
| §1 歷史 | 敘事段落為主 | 若列舉 3+ inflection points 對稱結構 → bullet |
| §2-§5 供需四章 | 敘事為主（因果推導） | 列舉 top suppliers / parallel drivers → bullet 或表格 |
| §6 短中長期 | 表格 + 表外推導敘事 | 表格固定 |
| §7 投資時鐘 | bullet 或表格（本來就是列表型） | 預設 bullet |
| §8 Non-Consensus | bullet（3 條 non-consensus 並列） | 預設 bullet |
| §9 Kill Scenario | bullet（3 條反方論證並列） | 預設 bullet |
| §10 Catalyst | bullet（時間線節點並列） | 預設 bullet |
| §11 ticker | 表格（固定） | （固定） |

### 反 pattern（避免）

- ❌ 把因果鏈寫成 bullet — 「A → B」變成兩個獨立 bullet，邏輯連結消失
- ❌ 把 3 個對稱項目硬塞成段落 — 每個 catalyst 共 30 字、寫成連續 90 字段落，讀者要自己拆
- ❌ Bullet 內又寫長句不分點 — Bullet 是用來 scan 的，每點應在 1-2 行內結束

### Gate 11 配額計算（v1.3 更新）

文字比例 ≥ 80% 計算時，**bullet 內字元算文字**（`<ul>`、`<ol>`、`<li>` tags 排除，內容字元計入）。Gate 11 公式不變，只是計算邊界擴大。

---

## 【文字 80% / 表格 20% 配額機制】

### 量化定義

「文字比例」= 純文字字元數（含段落 + bullet 內容）/ 整篇 HTML 可見字元數（剔除 HTML tags、CSS、JS、注釋）。

**目標**：文字 ≥ 80%，等價於：表格相關字元（含 `<table>`、`<tr>`、`<td>` 等內容）≤ 20%。

**hard cap**：表格數量 ≤ 4 張，每張行數 ≤ 8 行。

### 為何 80/20 不是任意數字

- ID 是 ≤ 30% 敘述（換言之 ≥ 70% 表格）。DS 直接反過來就是 ≥ 80% 敘述。
- 80% 是「敘述真的負責主幹」的最低門檻 — 低於這個比例，文字會被表格切碎、看起來像帶長 caption 的 ID。
- 上限不卡死 100% 因為某些章節（§5 TAM、§6 scenarios、§11 tickers）表格是最有效的呈現方式。

### 自動檢查

`pre_publish_check.md` Gate 11 跑這個檢查：

```bash
python3 scripts/check_ds_text_ratio.py docs/ds/DS_{Theme}_{YYYYMMDD}.html
```

實作於 `pre_publish_check.md` 內（無獨立 script，直接用 inline Python）。

---

## 【寫稿工作流（Step 1-9）】

### Step 1 — Theme 確認 + scope 定義

User 提產業主題，skill 先確認：

1. **Theme 是否夠具體**：太籠統（例：「半導體」）→ 要求 user 縮小（例：「AI ASIC 設計服務」、「DRAM 超循環」）。
2. **Theme 是否屬於 DS 適用範圍**：DS 適合「歷史長、供需循環明顯、敘事比表格重要」的主題。例：
   - ✅ **適合 DS**：AI 加速器需求演進、HBM 超級循環、大宗商品週期（銅 / 鋰 / 油氣）、人口結構驅動（旅遊 / GLP-1）、結構性消費轉移、地緣供應鏈重組
   - ⚠️ **不適合 DS（建議走 ID）**：純估值多空（用 ID 的 §8）、單一公司 catalyst（去 stock-analyst）、純政策事件追蹤（去 geopolitics）
3. **檢查同 theme 是否已有 ID**：
   ```bash
   ls docs/id/ID_*${theme_kebab}*.html
   ```
   若有 → 列入 `related_ids[]`，DS §0 加 callout 連結回去。
4. **mega + sub_group 分類**：從 `docs/id/taxonomy.md` 白名單選一組。

### Step 2 — 三軸 WebSearch / WebFetch

DS 的研究分三軸，每軸最少 3-5 次 search，最多 8 次（避免無限 search）：

- **軸 A：歷史** — 該產業 25 年（或 history_window_years）內的演進、技術代際、轉折點、過去類比
  - Search 關鍵字模板：`{theme} history evolution 1990 2000 2010 2020`、`{theme} technology generations`、`{theme} historical analog [similar industry]`
- **軸 B：供給** — 現在供給結構（top suppliers、capacity、utilization、bottleneck）+ 未來供給（capex pipeline、新進入者、彈性、地緣 / 政策 fragility）
  - Search 關鍵字模板：`{theme} top suppliers 2026 market share`、`{theme} capex pipeline 2026 2027`、`{theme} capacity utilization`、`{theme} new entrants competitive landscape`
- **軸 C：需求** — 現在需求（end-market mix、地域、driver）+ 未來需求（TAM 預估、需求拐點、結構性 shift）
  - Search 關鍵字模板：`{theme} demand drivers 2026 end markets`、`{theme} TAM forecast 2030`、`{theme} customer concentration`、`{theme} demand inflection point`

**T1 來源優先**（v1.2：QC-DS13 強制 T1 占比 ≥ 50%）：公司 IR / earnings transcript、產業協會（SEMI、SIA、IFR、IEA、USDA、Yano、IDC、Gartner）、政府機構（Fed、ECB、BLS、Eurostat）、台股 MOPS。T2：Bloomberg、Reuters、FT、WSJ、Nikkei、Yole、IC Insights、TrendForce。T3-A：賣方 primer（Morgan Stanley、Goldman、TD Cowen 等）。T3-B/C：個股 report、署名 Substack、財經媒體。T4：禁止獨立使用，必須有 T1/T2 交叉。詳見 SKILL.md【來源標籤系統】段。

研究過程中對每個量化斷言記錄其 tier + URL + claim summary；寫稿後，**每節正文不插入 inline tag**，而是在節末 `</section>` 之前插入 `<aside class="ds-refs">` 列出該節使用的所有來源（去重）。Gate 12 檢查每個含量化斷言的 `<section>` 是否有 aside；QC-DS13 計算全文 aside 的 T1 占比；QC-DS14 檢查事件型 claim 14 天內 freshness；QC-DS15 攔 T4 獨立使用 + T3 單獨使用警示。

### Step 3 — 寫 §0 thesis sketch

在開始寫長文之前，先寫 §0：

- 一句話 thesis（≤ 200 字）— 本 DS 整篇要證的核心觀點
- ds-meta JSON block（thesis 確認後填）
- 若同 theme 有 ID → 加 callout：

```html
<div style="background:#F9FAFB;border-left:4px solid #475569;padding:10px 14px;margin:8px 0 14px;border-radius:4px;font-size:13px;color:#1F2937">
  📊 本主題已有 ID 報告：<a href="../id/ID_{Theme}_{YYYYMMDD}.html"><strong>ID_{Theme}_{YYYYMMDD}</strong></a> — 表格 dashboard 視角，建議與本 DS 互補閱讀。
</div>
```

### Step 4 — 寫 §1 歷史脈絡

純敘述。寫 2-3 個歷史轉折點 + 1-2 個歷史類比。這章為後面 §3 / §5 / §6 提供因果起點。

寫作要求：
- 主體用敘事段落（每段 80-150 字）展開因果與時序；當段內列舉 3+ 平行轉折點 / 對稱結構（年份-事件-影響）時可改 bullet（v1.3：見【敘述 vs 條列判準】段）
- **每個 inflection point 段落必須含「具體日期（YYYY 或 YYYY-MM）+ 至少一個量化錨點」**（v1.1 硬性，見【§1 歷史錨點規則】段；DS-9 critic 自動掃）
- 不允許「過去幾年」「最近」「近期」這類模糊表述
- 量化錨點可以是：價格、性能指標（TFLOPS / GB / 頻寬）、市占、capacity、用戶數、營收；來源統一收在節末 `<aside class="ds-refs">` 中
- 結尾段落（💡 對投資的意義）連結到「這段歷史對今天意味著什麼」

### Step 5 — 寫 §2-§5 供需四章

順序嚴格：§2 現供 → §3 未供 → §4 現需 → §5 未需。

**§2 現在供給**：誰供給、capacity 多少、utilization 多少、瓶頸在哪。允許 1 張小表錨點（top 5-8 玩家 × capacity × share）。表格 ≤ 6 行。**v1.1 新增表格欄位規則**：top suppliers 表必須含三個時間點 — **T-2 年（actual）/ 當年（actual or YTD）/ T+1 年（estimate）**，讓讀者看出趨勢方向（加速 / 穩定 / 衰退），不只是 snapshot。若新興供給結構（< 3 年歷史）→ 用 T-1 / 當年 / T+1 並在 footnote 註明數據起始限制。表格數字來源列入節末 aside。

**§3 未來供給**：純敘述。capex pipeline（誰宣布擴 capacity，何時完成）、新進入者（誰準備進入、進入門檻）、地緣 / 政策對供給的影響、供給彈性（價格上漲時多快能擴 capacity）。**v1.1 因果閉合鎖點**：若 §1 提及某代際技術 / 護城河（如 CUDA、CoWoS 製程獨家性），§3 中必須有至少一段（≥ 50 字符）直接回應「該變數在未來 3-5 年是否仍 binding」 — 不可延後到 §8 Non-Consensus。

**§4 現在需求**：純敘述。end-market mix（demand 分佈在哪些下游應用）、地域分布、key drivers（誰在買、為何買）、定價權（哪段需求最 price inelastic）。

**§5 未來需求（含 TAM）**：敘述 + 1 張 TAM / CAGR 多情境表。寫 demand inflection point、TAM forecast（base/bull/bear，多情境）、結構性 shift（哪些需求消失、哪些新增）。**v1.1 推導可追溯性**：bull/bear case 的數字偏離 base 必須在表外段落或表下方註寫推導（如「bull case +20% 來自 hyperscaler capex 兌現 120% × workload mix 不變」），不允許黑盒數字。每個 input（capex、workload mix、accelerator ratio）來源列入節末 aside。**因果閉合鎖點**：若 §1 提及某需求驅動（如生成式 AI、生育率、人口老化），§5 必須回應「該驅動在未來 5-10 年走向 / 是否拐點」。

**章節間因果鎖**：寫完 §5 之後，必須有一段顯式結論：「依本章 §3 與 §5 的推導，未來 X 年產業供需狀態是 **過剩 / 平衡 / 短缺**，因為 [具體原因]」。這是 §6 推估的橋。

### Step 6 — 寫 §6 短中長期推估

敘述 + 1 表（必要）。表格格式：

| Horizon | Base case | Bull case | Bear case | Trigger |
|:---|:---|:---|:---|:---|
| 短期（12M）| {ASP/utilization/sales 數字 + 1 句敘述} | {} | {} | {要看哪個 metric 才知道走 base / bull / bear} |
| 中期（3Y）| {} | {} | {} | {} |
| 長期（5Y+）| {} | {} | {} | {} |

每個 cell 內可加 1-2 句敘述（不用純數字）。表格之外用敘述展開三個 horizon 各自的邏輯。

**v1.1 推導可追溯性（硬性）**：

- 每個 cell 數字的 input 來源統一列入節末 aside
- bull case 與 bear case 必須在表外緊鄰段落內寫「推導：base 假設 X，bull 改為 X' → 結果差 Y%」這種偏離分析
- 例：base 2028 NVDA share 60-65%（推導：§3 ASIC 滲透率 30% × §5 TAM growth 25% CAGR → 維持 ~62%）；bull case 70-75%（推導：§5 ASIC 滲透率改為 20%、CUDA inference moat 持續 → NVDA 多吃 8-10pp）；bear case 45-50%（推導：§3 ASIC 滲透率改為 45% + Google TPU 對外賣 → NVDA 失 12-15pp）
- 三 case 偏離 base 必須能追到 §2/§3/§4/§5 某個 input 變動

**Trigger 欄要求**：每個 horizon 給一個**可量化** trigger metric。禁止「demand booms」「inference takes off」這種模糊詞 — 改寫成「NVDA inference run-rate ≥ $80B annualized（推導：當前 DC rev $130B × 60% inference penetration）」。

### Step 7 — 寫 §7-§11

- **§7 投資時鐘**：當前 Phase（I/II/III/IV）+ 進入下一階段的必要 / 充分條件（純敘述）
- **§8 Non-Consensus View**：3 條 vs 市場共識的具體分歧。每條結構：「共識說 X / 本 DS 看 Y / 分歧原因 Z」。
- **§9 風險與 Kill Scenario**：3 條最有力反方論證。每條一段（80-150 字），含：具體路徑、當前證據、成真時間窗。
- **§10 Catalyst Timeline**：未來 18 個月 5-8 個關鍵節點。寫成連續敘述，每個節點用 `<strong>YYYY-MM</strong>` 或 `<time>YYYY-MM-DD</time>` 標記，CSS 加亮。每節點寫「若達成 / 若落空」雙路徑。
- **§11 關聯個股清單**：1 張表格（**stock-analyst hook，必填**）。欄位：ticker × role × depth × beneficiary × 對應 DD（若已有）。深度標籤同 ID（🔴 核心、🟡 次要、🟢 邊緣）。**v1.1 時間限定（硬性）**：caption 中的閾值定義必須明示「as of YYYY」或「by YYYY (forecast)」。若是 forward-looking 閾值（如「🔴 = projected AI rev ≥ 40% by 2028」），表格每個 ticker 行必須另列「current YYYY actual」對照欄，避免讀者誤判（見【§11 ticker depth 時間限定規則】段）。Gate 14 自動掃。

### Step 8 — 預發布檢查（v1.2：14 道閘門）

按 `pre_publish_check.md` 逐項跑：

1. Gate 1：11 章節完整、順序正確
2. Gate 2：每個事件型 claim < 14 天 refresh
3. Gate 3：ds-meta validator pass
4. Gate 4：mega + sub_group 在白名單
5. Gate 5：related_ids 對應的 ID 真實存在
6. Gate 6：§1 → §3 / §5 / §6 因果鏈可追溯（必須閉合在 §3 或 §5，不能延後到 §8）
7. Gate 7：§3 + §5 → 供需平衡結論明確
8. Gate 8：§6 三情境 + trigger 完整
9. Gate 9：§11 ≥ 3 ticker
10. Gate 10：表格數 ≤ 4、行數 ≤ 8/張
11. **Gate 11**：文字比例 ≥ 80%
12. **Gate 12（v1.2 修訂）**：每個含量化斷言的 `<section>` 末尾必有 `<aside class="ds-refs">`；全文 aside 的 T1 + T1-zh 占比 ≥ 50%（QC-DS13）
13. **Gate 13（v1.1 新，v1.2 不變）**：§5/§6/§7/§9/§11 結論數字必有「推導：」行或等效推導標記
14. **Gate 14（v1.1 新，v1.2 不變）**：§11 ticker depth 閾值必須時間限定（current / forward-looking 明示）；若 forward-looking，必須附 current actual 對照欄

任一 fail → 返工修改該章節，**不可直接 commit**。

### Step 8.7 — MANDATORY critic gate

不可省略。寫稿完成後，必須 spawn id-review skill（`--mode ds`）做 cold review：

```
Agent({
  description: "Cold review DS draft {Theme}",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "You are operating as the id-review sub-agent in DS mode. \
Read spec at /Users/ivanchang/.claude/skills/id-review/SKILL.md. \
Mode: --mode ds. DS file: docs/ds/DS_{Theme}_{YYYYMMDD}.html. \
Save critic report to docs/ds/_critic_{Theme}_{YYYYMMDD}.md."
})
```

Critic 會檢查 DS 特有的 **9 項**（v1.1：原 6 項 + 新增 3 項，見 id-review --mode ds spec）：
1. **DS-1** 表格 > 20% = 違規
2. **DS-2（v1.1 升級）** §1 → §3 / §5 / §6 因果鏈是否成立，且**閉合在 §3 或 §5**（不可延後到 §8）
3. **DS-3** §3 + §5 供需平衡結論是否明確（過剩 / 平衡 / 短缺三選一）
4. **DS-4** §6 三情境 trigger 是否可量化
5. **DS-5** §10 Catalyst「若達成 / 若落空」雙路徑是否完整
6. **DS-6** §11 ticker depth 與 §3 / §5 敘述是否一致
7. **DS-7（v1.2 修訂）** aside 抽樣檢查：抽 2 節，確認其 `.ds-refs` aside 存在、條目與正文量化斷言對應、tier 正確、URL 可達；計算全文所有 aside T1 占比 ≥ 50%
8. **DS-8（v1.1 新）** §6 推導抽樣：抽 base/bull/bear 各一格，驗推導 input 是否可從 §2/§3/§4/§5 找到出處
9. **DS-9（v1.1 新）** §1 雙錨點：每段必有具體日期（YYYY 或 YYYY-MM）+ 至少一個量化錨點（數字）

Critic 結果分三類：
- 🔴 **CHANGES_CONCLUSION**：阻擋發布。必須先 patch 才能 commit。
- 🟡 **PARTIAL_ERROR**：呈現給 user 互動式 patch。
- 🟢 **COSMETIC**：紀錄但不阻擋。

### Step 9 — Commit + 索引同步

1. 在 `docs/ds/index.html` 找對應的 `<!-- subgroup-anchor: {mega}.{sub_group} -->`，插入新 article 卡片。
2. 跑 build script 重新生成分類頁：
   ```bash
   python3 scripts/build_ds_category_pages.py
   ```
3. 更新 `docs/ds/INDEX.md`（手動 append 一列）
4. Commit + push：
   ```
   ds: 首篇 {Theme} DS — {一句話 thesis}
   ```

---

## 【QC 規則】

| 編號 | 規則 | 違反處置 |
|:---|:---|:---|
| QC-DS01 | 章節順序固定（§0 → §1 → ... → §11） | 返工，不可發布 |
| QC-DS02 | 文字比例 ≥ 80% | 返工，刪表格 / 擴敘述 |
| QC-DS03 | 表格 ≤ 4 張、每張 ≤ 8 行 | 返工 |
| QC-DS04 | §1 → §3 / §5 / §6 因果鏈可追溯 | 補敘述橋段 |
| QC-DS05 | §3 + §5 → 供需平衡明確結論（過剩 / 平衡 / 短缺三選一） | 返工 §5 結尾段 |
| QC-DS06 | §6 三 horizon × 三情境 + trigger 完整 | 返工 §6 表格 |
| QC-DS07 | §10 每節點「若達成 / 若落空」雙路徑 | 補雙路徑 |
| QC-DS08 | §11 ≥ 3 ticker，每筆 depth 標籤 + DD 連結（若有） | 補 ticker |
| QC-DS09 | ds-meta `mega` + `sub_group` 必填，在白名單內 | validator 阻擋 commit |
| QC-DS10 | `history_window_years` + `forecast_horizon_years` 必填 | validator 阻擋 |
| QC-DS11 | 每個事件型 claim 14 天內 refresh，結構型 60 天 | critic flag stale |
| QC-DS12 | 若同 theme 有 ID，`related_ids[]` 必填、§0 callout 必填 | critic flag missing link |
| **QC-DS13**（v1.2）| 每個含量化斷言的 `<section>` 末尾必有 `<aside class="ds-refs">`；全文 aside T1 + T1-zh 占比 ≥ 50% | Gate 12 fail / DS-7 critic |
| **QC-DS14**（v1.1）| 事件型 claim source 14 天內、結構型 60 天 | DS-7 critic flag stale |
| **QC-DS15**（v1.1）| T4 禁止獨立使用；T3 單獨使用必加 ⚠️ + `<aside class="source-warning">` | DS-7 critic flag |
| **QC-DS16**（v1.1）| §5/§6/§7/§9/§11 結論數字必有「推導：」行 | Gate 13 fail / DS-8 critic |
| **QC-DS17**（v1.1）| §1 每個 inflection 段含具體日期 + 量化錨點 | DS-9 critic flag |
| **QC-DS18**（v1.1）| §11 ticker depth 閾值必須時間限定（current 或 forward-looking 明示）；若 forward-looking 必附 current actual 對照欄 | Gate 14 fail |
| **QC-DS19**（v1.1）| §1 inflection 必須在 §3 或 §5 找到對應回答段（≥ 50 字符），不能延後到 §8 | DS-2 critic flag |

---

## 【觸發條件】

User 說以下任一，自動觸發本 skill：

- 「{主題} ds」/「ds {主題}」
- 「{產業} 敘述報告」/「discourse {industry}」
- 「分析 {產業} 的供需循環」
- 「{產業} 歷史與未來」
- 「{產業} 短中長期推估」
- 「寫一份 {產業} 的 DS 報告」

**不觸發**（走其他 skill）：
- 「{產業} ID」/「研究 {產業} 產業」→ industry-analyst
- 「{ticker} DD」/「{ticker} 深度分析」→ stock-analyst
- 「{ticker} dca」/「{ticker} 定見」→ deep-conviction-analyst

---

## 【與 ID / DD / DCA 的關係】

| Layer | Skill | Output | 適用情境 |
|:---|:---|:---|:---|
| 產業層（敘事） | **industry-ds** | docs/ds/DS_*.html | 歷史長、供需循環、敘事重於數據 |
| 產業層（dashboard） | industry-analyst | docs/id/ID_*.html | 多維對比、PM 快速決策 |
| 公司層（深度） | stock-analyst | docs/dd/DD_*.html | 單檔公司護城河 / 估值 / 訊號燈 |
| 公司層（決策） | deep-conviction-analyst | docs/dca/DCA_*.html | 單檔買賣定見、PM 行動建議 |

**Cross-link 路徑**：
- DS §11 列 ticker → stock-analyst 讀 §11 → 在 DD §0 / industry context 引用 DS（與 ID 並列）
- DS §0 callout → ID（若同 theme 有）→ user 可一鍵切到 dashboard 視角
- DS `related_ids[]` → validator 確認連結有效 → stock-analyst dedup 機制讀此欄位

---

## 【常見錯誤 anti-pattern】

寫稿時避免以下：

1. **把 ID 章節照抄成敘述**：DS 不是「ID 加長版」。如果你發現自己在寫 §8 估值機制、§9.5 Steel-man 反方表格 → 你應該寫 ID 不是 DS。
2. **敘述堆砌數據卻無因果**：「2020 年 X、2021 年 Y、2022 年 Z」這種流水帳不算敘事。每段必須有「為何」與「所以」。
3. **§3 / §5 各自獨立、不合流**：未來供給與未來需求必須在 §5 結尾合流出供需平衡結論。獨立寫兩章卻不合流是返工 P1 錯誤。
4. **§6 推估數字飄空**：base/bull/bear 三情境的數字必須能追到 §2-§5 的某個事實。例如「bear case ASP -30%」必須有 §3 某段「capex 過剩 X GW」對應。
5. **§10 Catalyst 全寫成「未來會發生」**：必須有具體日期錨點 + 雙路徑判讀。「Q3 26 NVDA earnings」不夠 — 寫「2026-08-27 NVDA earnings：若 inference run-rate ≥ $80B → 確認推論週期延長 → 進入 bull case；若 < $50B → 觸發 §9 thesis #2 反方」。
6. **§11 ticker 與 §3 / §5 敘述不一致**：例如 §3 寫供給過剩、§11 把所有供應商都標 🔴 beneficiary，邏輯不通。
7. **黑盒數字**（v1.1 新增）：§5/§6 bull/bear case 給絕對數字但不寫推導行 — PM 無法驗證 +20%/-25% 從哪個 input 變動推出來。所有結論數字必須能從前文 input 重建（見【推導可追溯性原則】段）。
8. **因果延後到 §8**（v1.1 新增）：§1 提了某 inflection（如 CUDA 護城河），§3/§5 沒回答，把答案延後到 §8 Non-Consensus — 破壞 spine 因果閉合。§8 是「市場看法 vs 我們」，不是「歷史 → 未來」的因果橋。
9. **forward-looking 閾值無時間標**（v1.1 新增）：§11 caption 寫「🔴 = AI rev ≥ 40%」但沒指明是 current actual 還是 2027-2028 forecast，導致 AMD（當前 ~8% AI rev）標 🔴 讓讀者困惑。

---

## 【版本歷史】

- v1.0（2026-05-12）：首版。11 章節、80/20 文字表格比、三軸研究、id-review --mode ds critic gate、與 ID 並存設計。
- v1.1（2026-05-13）：可信度升級。① 移植 ID skill 的 `<span class="source-tag">[T1:]` 設計（避免 codebase 兩套 citation）+ T1 ≥ 50% 強制（QC-DS13）。② 推導可追溯性原則（從 stock-analyst v12.2 移植）— §5/§6/§7/§9/§11 結論數字必附 ≤ 3 行推導（QC-DS16）。③ 因果閉合升級 — §1 inflection 必須在 §3 或 §5 閉合，不能延後到 §8（QC-DS19，DS-2 critic 升級）。④ §1 雙錨點規則 — 每段含具體日期 + 量化錨點（QC-DS17）。⑤ §11 ticker depth 閾值時間限定 — current 或 forward-looking 明示 + 對照欄（QC-DS18）。⑥ §2 表格欄位 — 必須含 T-2 / 當年 / T+1 三時間點。⑦ 字數上限 6,500 → 7,500（給 source-tag + 推導行空間）。⑧ Gate 12-14 + DS-7/8/9 critic 新增。觸發：DS_AIAcceleratorDemand v1.0 暴露 5 個系統性弱點（無 footnote、無推導、§1 口語錨點、§11 閾值無時間標、§3 因果延後到 §8）。
- v1.2（2026-05-13）：閱讀體驗修復。inline `<span class="source-tag">` → §末 `<aside class="ds-refs">` 參考區塊。可審計性規則（tier、T1 占比、T4 禁用、T3 警示、freshness）全部保留，只改位置。推導行（ds-derive）完全不動。字數上限從 7,500 降回 6,500（移除 inline tag 佔位）。Gate 12 / QC-DS13 / DS-7 重寫為 aside 格式。觸發：DS_AIAcceleratorDemand v1.1 有 39 條 inline tag 嚴重破壞中文閱讀流（用戶反饋），且英文 source title 頻繁中斷中文段落。遷移：既存 v1.1 DS 檔案用 `scripts/retrofit_ds_references.py` 批量遷移。
