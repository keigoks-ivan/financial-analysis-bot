---
name: dd-v12-3-upgrade
description: 對既有 DD 報告做 v12.3 升級的 batch worker。每呼叫一次處理 N 檔（預設 3），用 notes/site-internal/dd/_v12_3_manifest.md claim 協調多 window 並行。對 legacy DD（v12.0/12.1/12.2/pre-v12）做 body patch + dd-meta bump；對已是 v12.3 的 DD 只做 DCA cascade audit。所有 patch 須通過 anti-laziness gate（DD ≥ 80KB / DCA ≥ 50KB / 數字必引 source / 章節 checklist 齊備）。每 5 batch 觸發 cold-review sub-agent 抽查品質。觸發語：「跑 v12.3 升級 N 檔」「v12.3 batch」「升級 DD 到 v12.3」「dd-v12-3-upgrade」「/dd-v12-3-upgrade [N]」。
version: v1.2
---

# DD v12.3 Batch Upgrade Worker

## 0. Mission

把既有 DD（`docs/dd/DD_*.html`）batch upgrade 到 v12.3 schema + body。每個 window 一次處理 N 個 ticker（預設 3），透過共享 manifest 協調多 window 並行。**不寫新 DD**（那是 stock-analyst skill）；**不重跑 DCA**（那是 deep-conviction-analyst skill）；本 skill 只做 patch 與 cascade audit。

**核心原則**：寧可 data-gap 標記也不准瞎填假數字。寧可 batch 退回也不准灌水通過 80KB gate。

**核心 stance：跑完結論可以不一樣** — v12.3 加進來的 §5.F single-thing / §9 二維 moat / §11 三段議價權 / §12 SBC 真實稀釋 是新的證據維度。**不強求 post-v12.3 verdict 與升級前 verdict 相同**，只要求**內部一致**（§1 ↔ §2 ↔ §13 結論三處 verdict 字面同步）。verdict 變了務必留痕（§1 變更紀錄句 + manifest notes + commit log），重大降級（A+/A → C/X）強制觸發 cold review。

—

## 1. 權威來源（執行前必讀其一節）

| 路徑 | 何時讀 |
|---|---|
| `docs/dd/specs/v12.3-spec.md` | Step 2 開始前讀 §3 章節級具體改動清單（決定砍什麼補什麼） |
| `docs/dd/specs/pilot/DD_2330TW_v12.3pilot.html` | Step 2 寫 §5.F / §8.H / §9 兩軸 / §11 三段時當 reference example |
| `docs/dd/CLAUDE.md` | 啟動時讀（git staging 紀律 + Schema 版本與降級規則 #17） |
| `scripts/dd_meta.md` | dd-meta JSON 欄位定義 |

**不要**讀 `.claude/skills/stock-analyst/SKILL.md` 全部 2471 行 — 太大；只用 v12.3-spec.md。

—

## 2. 啟動 prompt 解析

| 用戶輸入 | N |
|---|---|
| `/dd-v12-3-upgrade` | 3 |
| `/dd-v12-3-upgrade 5` | 5 |
| 「跑 v12.3 升級 3 檔」 | 3 |
| 「v12.3 batch」 | 3 |
| 「升級 DD 到 v12.3」 | 3 |

N 上限 5，超過視為 5。

—

## 3. Step 0 — Claim（不可跳過）

### 3.1 Sync + 產 window-id

```bash
cd /Users/ivanchang/financial-analysis-bot
git pull --rebase
```

window-id 格式：`win-<YYYYMMDD-HHMM>-<隨機4字>`，例：`win-20260516-1430-3a7c`。在 Bash 用 `echo "win-$(date +%Y%m%d-%H%M)-$(openssl rand -hex 2)"`。

### 3.2 讀 manifest 挑 N 個

讀 `notes/site-internal/dd/_v12_3_manifest.md`。挑選優先序：
1. **dca_only 優先**（工時短，先把 18 檔清掉）
2. dca_only 清完後再挑 `pending`
3. **legacy_full 內優先序**：v12.2 → v12.1 → v12.0 → pre-v12（pre-v12 工時最長，留最後）
4. 跳過 `in_progress` / `done` / `skip`
5. **跳過 `notes` 含 `pre-v12-heavy` 的 ticker**（除非 pending/dca_only 都沒了；pre-v12 應另外 dedicated batch 處理）

### 3.3 Mark in_progress

對選中的 N 個 ticker，用 Edit 把該 row 的 `status` 從 `pending`/`dca_only` 改成 `in_progress`，`claimed_by` 從 `–` 改成 window-id。

### 3.4 Push claim（**獨立 commit**）

```bash
git add notes/site-internal/dd/_v12_3_manifest.md
git commit -m "claim: v12.3 batch <T1> <T2> <T3> by <window-id>"
git push
```

**若 push 被拒（race）**：
```bash
git pull --rebase
# 讀 manifest 看選中 ticker 是否已被別 window 改成 in_progress
# 若是 → 撤銷自己的 Edit，重新挑 N 個 pending
# 若否 → 重 push
```

最多 retry 3 次；3 次都失敗 → 停下告訴用戶 race 太頻繁，建議減少 window 數。

—

## 4. Step 1 — Per ticker 分流

對每個 claim 到的 ticker（依 manifest 的 schema 欄位）：

- `v12.3` → 跳過 Step 2，**直接做 Step 3 (DCA cascade audit)**
- `v12.0` / `v12.1` / `v12.2` / `pre-v12` → 進 Step 2

—

## 5. Step 2 — DD body patch（legacy → v12.3）

### 5.0 讀檔 + Pre-flight WebSearch（強制）

對該 ticker 跑 **3 次 WebSearch**（最少；可更多）：

1. `<TICKER> customer concentration top customer revenue percent 10-K 2024 2025` — 為 §8.H
2. `<TICKER> stock-based compensation FY2024 FY2025 percent revenue` — 為 §12 SBC
3. `<TICKER> acquisitions M&A 2020 2021 2022 2023 2024 2025` — 為 §12 M&A 5Y

**TW 加搜**：`<TICKER> 公開資訊觀測站` / `<TICKER> 主要客戶 前十大`
**JP 加搜**：`<TICKER> 有価証券報告書` / `site:disclosure2.edinet-fsa.go.jp <TICKER>`

把搜尋結果與關鍵 source URL 記下，patch 後留在 HTML comment：
```html
<!-- v12.3-upgrade source log (window-id, date)
  customer: [URL1, URL2]
  sbc: [URL3]
  m&a: [URL4, URL5]
-->
```

### 5.1 Subtractive（砍）

讀 `docs/dd/specs/v12.3-spec.md` §3 確認當前 DD 哪些章節需要砍。

| 動作 | 操作 |
|---|---|
| §2 9 子節 → 7 子節 | 把 A 體質檢核 5 項 mini-list 收進 §2.B 段首；E 砍 QC-29 4 情境壓力測試表，只留 R:R 三數字 + 1 line Bear anchor（FY+1 EPS × 0.9 × Bear PE） |
| §7 砍「低估值四問」 | 找 「低估值四問」/「低估值 4 問」block 整段刪 |
| §7 砍「便宜理由四問」 | 同上整段刪 |
| §13 砍 13.0 估值體系診斷 | 整 sub-section 刪 |
| §13 砍 13.3 Reverse DCF | 整 sub-section 刪 |
| §13 砍 13.5 五角驗證 / 8 因素定錨 / 便宜理由五問 | 整 sub-section 刪 |
| §13 結尾改 | 加 1 段「結論段」（30-50 字）整合 13.1/13.2/13.4 結論 |

### 5.2 Additive（補，需真研究）

按 v12.3-spec.md §3 的章節定義新增/擴充：

#### §5.F Single Thing（新增）— 必含 4 元素
1. **binary outcome 定義**（成功 / 失敗各長什麼樣）
2. **trigger metric / event**（具體名稱：例「Apple iPhone 17 採用 N3P 良率 ≥ 80%」「FDA Phase 3 readout」）
3. **時間窗**（具體季 / 年；不准寫「未來」）
4. **asymmetric payoff**（成 → +X%，敗 → -Y%；數字非裸估，要引 §13.4 peer 或 §13.2 PEG 推導）

來源優先：對應 ticker 的 DCA §5.F（若存在）→ 否則從現存 DD §5 推導。

#### §5.B 三個假設加 sourced floor
每個假設必須含：
- 可驗證指標**具體數字門檻**（不接受「YoY 增加」這種模糊）
- **信息來源**（公司法說 / sell-side / 產業報告，inline 標註）
- **漂移觸發條件**（連 2 季偏離 X% → 削弱；單季不觸發）

#### §5.C 三個風險加時間尺度分層
每個風險前面加 emoji：
- ⚡ 短期（1-2 季可觸發）
- 🔥 中期（4-6 季）
- 🐢 長期（2+ 年慢變數）

#### §8.B 成長品質
- 定價 vs 量分拆具體 %（最近 1Y + 3Y 趨勢）
- 有機 vs 無機列近 5 年併購清單（年份 + 標的 + 金額）

#### §8.H 客戶結構深度（新增）— 必含 5 元素
1. **top-1 客戶 %**（公開揭露 → 引 source；未公開 → 寫「未公開揭露 — 依 [具體基礎] 推估區間 X-Y%」）
2. **top-5 累計 %**
3. **top-10 累計 %**
4. **dual-track / second-source / sole-source** 標籤 + 1 句 rationale
5. **主客戶議價力或週期性 risk**（具體案例）

#### §9 護城河二維拆解（強制，除 single-axis escape）— 必含 8 元素
1. execution moat score 1-10
2. execution moat 1-2 句 evidence（引 §9 narrative 或外部 source）
3. pricing power moat score 1-10
4. pricing power moat 1-2 句 evidence
5. moat 趨勢雙線標：execution ↑→↓ + pricing ↑→↓
6. 整合 final moat 等級 S/A/B/C/X
7. **QC-23 三級威脅分類表**：threat name × tier（🟡 點對點 / 🔴 生態攻擊 / ⛔ 架構替代）× time-to-impact × probability
8. single-axis escape 案（SaaS / 銀行 / 保險 / 寡占公用事業）：必須先寫「為何符合 escape rule」rationale

#### §10 財務品質
- 三年趨勢表加同業對比欄（從 §13.4 peer 引）
- 「剔除回購後 EPS CAGR」必算
- FCF lumpiness（5Y 滾動均 + 最低谷年份 + lumpy 性質判斷）

#### §11 議價權三段獨立段落 — 每段必含 3 元素
1. 對象明確（vs 上游點名供應商；vs 下游點名客戶或通路；地緣點名國家 / 區域）
2. 議價槓桿（price / volume / terms / 切換成本）
3. 近期具體案例或量化（最近 4 季內）
**每段 ≥ 60 字獨立段落，不准合併為 bullet**。

加：營收三維（業務段 × 地區 × 客戶集中度三表）+ 單位經濟逐業務段（不接受全公司平均 ARPU）。

#### §12 治理擴
- M&A 5Y track 表（年份 / 標的 / 金額 / 整合結果 / 減損註明）
- SBC 真實稀釋強化：「EPS ex-SBC = X」必算；reported EPS vs ex-SBC EPS 差距 > 5pp 必標 ⚠️
- SBC 趨勢 3Y（漲 / 平 / 降）

#### §13.4 強制對的 peer tier
- 點名同 business model tier 的 3-5 家 peer
- 1 句 rationale（為何屬此 tier）
- **避反面例**：3661 不應跟 AVGO/MRVL 比 anchor，應跟 GUC/Faraday 比
- 無 ideal peer → 明寫「無 ideal peer group，本表僅供參考」

### 5.3 Metadata bump

`<head>` 確保有：
```html
<meta name="dd-schema-version" content="v12.3">
```

`<script id="dd-meta" type="application/json">` JSON：
- `"schema": "v12.3"`
- §9 二維拆解後 add：`"moat_execution": <1-10>`, `"moat_pricing_power": <1-10>`
- single-axis escape 案 → 不加二維 sub-scores，但在 `notes` 或 `oneliner` 內含 "single-axis"

頁首字串「DD Schema vX.X」也要更新到 v12.3（如有）。

### 5.4 Anti-laziness + 嚴謹度 gate（**fail-stop**）

**A. Size 地板**：改完 file size **必須 ≥ 80 KB**。`stat -f%z docs/dd/<file>.html` 或 `wc -c < docs/dd/<file>.html`，除以 1024。< 80 KB 不准 commit；回頭加深 §5/§8/§9/§11/§12 narrative。**禁止用空白行 / 加長 disclaimer / 重複 bullet 灌水**。

**B. No-fabricate 鐵律**：任何**數字**寫入 §8.H / §11 / §12 / §10 peer 比較欄 / §13.4 peer tier 都必須附 inline source citation：
- 格式：`87% (10-K FY2024 p.42)` 或 `top-3 客戶占 62% (2026Q1 earnings call transcript)` 或 `(Reuters 2026-04-12)`
- 沒 source 的數字 → reject，不准 commit
- agent「估算 / 推估」**不算 source**；只有 filings / press release / 主流媒體 / 公司官方資料才算
- 找不到資料 → 明寫「未公開揭露 — 依 [具體基礎，例：同業 20-K filings 中位數] 推估區間 X-Y%」**且推估基礎必須具體**

**C. 章節完整度 checklist**：上面 §5.F / §8.H / §9 兩軸 / §11 三段 / §12 SBC + M&A / §13.4 的「必含 N 元素」全部勾完才算過。漏一條就 reject。

**D. 推論邏輯嚴謹（內部一致，不綁定舊結論）**：
- §1 結論 verdict（A+/A/B/C/X）必須能由 §2 + §13 + §9 + §10 + §13.4 五個輸入推導出來。在 §1 末段加 1 句：「signal 推導：[§2 訊號] × [§13 估值燈] × [§9 護城河] × [§10 財務] × [§13.4 peer 相對] = [verdict]」
- §13 結論段必須與 §1 verdict 一致；不一致 → 哪個對哪個錯要明確
- **跑完結論可以不一樣**：post-v12.3 verdict 不需要與升級前 verdict 相同。v12.3 新增的 §5.F single-thing / §9 兩軸 moat / §11 三段議價權 / §12 SBC 真實稀釋 可能合理地推出不同的 verdict（例：v12.0 寫 A，v12.3 §9 二維拆解後 execution 6 / pricing 8 → 整合 B；或 §12 SBC ex-EPS gap 揭露 8pp → A 降 C）
- 只要求**內部一致**（§1 ↔ §2 ↔ §13 結論三處同 verdict 字面），**不要求對齊舊 verdict**

**D.1 Verdict shift 文件化（若 verdict 變了，務必留痕）**：
- 在 §1 末段加 1 句：「verdict 變更紀錄：v12.X → v12.3 由 [A] 改為 [B]，主因：[§9 二維 / §12 SBC / §13.4 peer tier 換 / ...]」（沒變則寫「verdict 不變 [X]」）
- dd-meta JSON 的 `signal` 欄位寫 v12.3 後的新 verdict（不留舊值）
- manifest `notes` 標 `verdict-shift A→B` 或 `verdict-same`
- commit message 必須包一行：「verdict shifts: T1 A→B, T2 same, T3 X→C」（PM 從 git log 一眼掃到 thesis 變動）
- 若 verdict 從 A+/A 掉到 C/X（重大降級）→ manifest `notes` 額外標 `⚠️-major-downgrade`，**cold review 必須對該 ticker 觸發**（不等 5 batch 週期，見 §7.3）

**E. data-gap 處理**：若任何章節「公開資料真的不夠」無法滿 checklist → **不要瞎填湊數**。在該章節結尾加：
```html
<aside class="data-gap">資料缺口：[具體缺什麼] — 待 [何時] 揭露</aside>
```
並在 manifest 該 ticker `notes` 標 `data-gap-§X.Y`。**這比硬填假數字好**。

—

## 6. Step 3 — DCA cascade audit

### 6.1 找該 ticker 的所有 DCA

```bash
ls docs/dca/DCA_<TICKER>_*.html 2>/dev/null
```

無 DCA → manifest 該 ticker `notes` 寫 `no-dca`，跳過 Step 3。

### 6.2 逐檔 Read 全文後決定改法

**禁止 sed-replace / replace_all 暴力替換**。每個 DCA 檔用 Read 完整讀過，**對每個 broken anchor hit 先讀前後 1 段**確認語意，再用 Edit 修改。

掃以下 broken anchor：

| 找到 | 改法（依 context 判斷） |
|---|---|
| `§13.0` 或「估值體系診斷」 | 該段是評價結論引用 → 改指 §13 結論段；該段是分析依據 → 改指 §13.1 / §13.2（看實際引述的內容） |
| `§13.3` 或「Reverse DCF」 | 該段引述 reverse DCF 結論 → 保留結論文字 + 註明「v12.3 已移除該方法但結論引述自 [DD 檔名舊版]」；該段是 deferred「待算」→ 改指 §13.2 PEG/forward PE |
| `§13.5` 或「五角驗證」/「8 因素定錨」 | 同上原則 |
| `QC-29` / 「4 情境壓力測試」 | 引述 4 情境結果 → 保結論 + 註明來源舊版；引述方法 → 改指 §2.E R:R 三數字 |
| §7「低估值四問」/「便宜理由四問」 | 同上原則 |

### 6.3 DCA size floor ≥ 50 KB

若改完 < 50 KB（破壞性編輯）→ 必須補敘述補回。**補的內容不可是廢話**（「綜觀以上分析」「因此本 DCA 維持結論」這類灌水會被 cold review 抓出）。應補：
- (a) 引述對應 DD §13.4 peer 的具體數字
- (b) IRR 重算（用 `update_dd_index.py` 內 `compute_dca_irr`）
- (c) 同類 DD §5.F 對照

### 6.4 DD verdict 變更 → DCA TODO 強制

若該 ticker 升級後 verdict 變了（manifest `notes` 含 `verdict-shift`），在每個對應 DCA 檔尾加：
```html
<!-- TODO: 對應 DD 升級到 v12.3 後 verdict 由 X 改為 Y（[主因簡述，例：§9 二維 execution 6 / pricing 8 → 整合 B]）；本 DCA 的 IRR / 部位建議 / opportunity cost 基於舊 verdict，建議擇期重跑 /<ticker> dca -->
```
**不要在這次 batch 順手重跑 DCA** — 只標 TODO，留給用戶在下個 PM 週期決定是否重跑。

### 6.6 舊版 DCA 標 TODO

若 DCA 是 v1.2 以前的舊版本（無 `dca-meta` 或 verdict 欄位殘缺）→ 在檔尾加：
```html
<!-- TODO: DCA 版本陳舊；建議用戶下次跑 /<TICKER> dca 重新生成 -->
```
**不要在這次 batch 順手重跑 DCA**（會把 batch 撐爆）。

### 6.7 DCA cascade 完整度 checklist
1. 該 ticker 所有 DCA 檔都已掃過（用 `grep -c '<TICKER>' docs/dca/DCA_<TICKER>_*.html` 確認 hit 數）
2. 每處 anchor 替換後語意通順（自檢：把改完段落朗讀一遍）
3. file size ≥ 50 KB
4. 若無 DCA → manifest `notes` 寫 `no-dca`

—

## 7. Step 4 — Validation（三層）

### 7.1 第一層：機械檢核（必過）

```bash
python3 scripts/validate_dd_meta.py --report 2>&1 | grep -E "<T1>|<T2>|<T3>"
```
須無 ERROR。同時逐 ticker 檢：
- DD file size ≥ 80 KB（`stat -f%z docs/dd/DD_<T>_*.html | tail -1`）
- 對應 DCA 全部 ≥ 50 KB
- DD HTML 含 `<meta name="dd-schema-version" content="v12.3">`
- dd-meta JSON 含 `"schema": "v12.3"`
- §5.F / §8.H / §9 兩軸 / §11 三段 / §12 SBC / §13 三子節 anchor 都存在

```bash
# 一次性 grep 驗 v12.3 章節 anchor
grep -E '5\.F|8\.H|moat_execution|議價權.*上游|SBC' docs/dd/DD_<T>_*.html | head -20
```

### 7.2 第二層：no-fabricate 檢核（每章抽 1 數字）

對 patch 的每個 ticker，從 §8.H / §11 / §12 / §13.4 各抽 1 個寫的數字，**目視確認**該數字旁有 source citation（`(10-K FY2024)` / `(2026Q1 earnings call)` / `(Reuters URL)` 等）。沒 citation → patch 退回，補 source 或改寫成有依據的敘述。

### 7.3 第三層：cold review

**觸發條件**（任一即觸發）：
- 每 5 batch 週期（讀 `notes/site-internal/dd/_v12_3_manifest.md` 中 `done` 數，每除 3 為 5 整數倍）
- **major-downgrade 強制**：該 batch 任一 ticker `notes` 標 `⚠️-major-downgrade`（verdict 從 A+/A 掉到 C/X）→ 不等 5 batch 週期，立即對該 ticker 觸發

```
Agent({
  description: "Cold review v12.3 patch quality",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: "你是 v12.3 patch 品質的冷讀 reviewer（與 patch agent 不同 model）。
讀 docs/dd/<latest patched>.html 完整。檢核 6 條：
(1) §8.H 客戶 top-1/5/10 數字是否有 inline source citation（filings / earnings call / 媒體 URL）
(2) §9 兩軸 score 的 evidence 是否真有具體依據還是空話（檢查是否引 §9 narrative 段落或外部資料）
(3) §11 三段議價權每段是否真的「對象明確 + 槓桿 + 近期案例」三元素齊備，且每段 ≥ 60 字獨立段落
(4) §12 SBC % of revenue + EPS ex-SBC + M&A 5Y 表是否真實財報數字（隨機抽 1 數字 cross-verify）
(5) §1 verdict 推導鏈是否**內部一致**（§1 / §2 / §13 結論三處 verdict 字面同步）；**不檢查**是否與舊版 verdict 相同 — 新分析可能合理推出不同結論
(6) 若 §1 verdict 變更紀錄存在（『verdict 變更紀錄：v12.X → v12.3 由 X 改為 Y，主因：...』），理由是否與 §9 / §12 / §13.4 新增或重做的章節呼應（不是隨意改）

輸出格式：PASS / WARN / FAIL + 每條的具體問題（含行號）。
存報告到 notes/site-internal/dd/_critic_v12_3_<ticker>_<YYYYMMDD>.md。"
})
```

- FAIL → 該 batch 退回重做（manifest 該 ticker 改回 `pending`，notes 標 `cold-review-fail-<reason>`）
- WARN → manifest notes 標 `cold-review-warn-<area>`，下批 spot-check 同類問題
- PASS → 繼續

—

## 8. Step 5 — Sync research index + commit

### 8.1 Run sync script

```bash
python3 scripts/update_dd_index.py
```

CLAUDE.md 強制：每次 DD/DCA 動完必跑。會自動同步 `docs/research/index.html` + `docs/dd-screener/latest.json`。

### 8.2 更新 manifest

對 N 個 ticker，把 `status` 從 `in_progress` → `done`。`notes` 加關鍵改動標註，例：
- `§9 single-axis escape: SaaS`
- `data-gap-§8.H: customer % 未揭露`
- `cold-review PASS`（若觸發了）

### 8.3 Commit（**具名 stage，禁用 git add . / -A / ***）

```bash
git add docs/dd/DD_<T1>_*.html docs/dd/DD_<T2>_*.html docs/dd/DD_<T3>_*.html
# 加 DCA 檔（每 ticker 可能有多份 DCA）
git add docs/dca/DCA_<T1>_*.html docs/dca/DCA_<T2>_*.html docs/dca/DCA_<T3>_*.html 2>/dev/null
git add docs/research/index.html
git add docs/dd-screener/latest.json
git add notes/site-internal/dd/_v12_3_manifest.md
# 若觸發 cold review
git add notes/site-internal/dd/_critic_v12_3_*.md 2>/dev/null

git commit -m "$(cat <<'EOF'
DD v12.3 upgrade batch: <T1> + <T2> + <T3> (+ DCA cascade)

verdict shifts: <T1> A→B, <T2> same, <T3> X→C
- <T1>: <main changes — e.g. §9 二維 8/6 → final B; §8.H top-1 87% (10-K)>
- <T2>: <main changes — verdict 不變 A>
- <T3>: ⚠️ major downgrade — <main driver, e.g. §12 SBC ex-EPS gap 12pp → §13 conclusion C>

Window: <window-id>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"

git push
```

**Commit message 規範**：
- 第 2 段必含 `verdict shifts: ...` 行（PM 從 git log 一眼掃到 thesis 變動）
- per-ticker bullet 寫 1-2 個關鍵新發現（§9 二維分數、§8.H 客戶引述、§12 SBC gap、verdict 變更主因）
- major-downgrade ticker 在 bullet 開頭加 ⚠️

**禁止 stage 的東西**（即使顯示 untracked）：
- `docs/id/ID_*.html`（industry-analyst skill 的 in-progress）
- `docs/research/.freshness_cache.json`
- `__pycache__/`
- 任何不在這次 batch scope 的檔

### 8.4 push 失敗處理

```bash
git pull --rebase
# 看是否與別 window 撞 manifest 改動
# 衝突解 manifest 的方式：保留兩邊 done，自己這邊的 notes 不要刪別 window 的
git push
```

—

## 9. Race condition handling

### 9.1 Claim race
- 兩 window 同時 claim 同 ticker：晚到的 push 被拒 → pull → 看 manifest 該 ticker 已被別 window 改 in_progress → 自己換 3 檔重 claim
- Retry 上限 3 次

### 9.2 Commit race
- 兩 window 同時 commit 不同 batch：rebase 解
- 若 rebase 衝突（manifest 同 row 兩邊都改）→ 兩邊都保留 done 狀態，notes 合併

### 9.3 Stale claim
- 某 ticker `in_progress` > 60 min 沒進展 → 視 stale
- 用戶（不是 skill）手動 reset：把該 row 改回 `pending`、`claimed_by` 改 `–`、加 notes `stale-reset YYYYMMDD`

—

## 10. 完工

當 manifest 顯示 `pending` + `in_progress` + `dca_only` 全部歸零（用 `python3 scripts/dd_v12_3_status.py --report` 看），整個 v12.3 升級完成。

最終驗證：
```bash
# 全部過 validator
python3 scripts/validate_dd_meta.py

# 沒有 < 80 KB 的 DD
find docs/dd/ -name "DD_*.html" -size -80k -not -path "*/specs/*"

# 沒有 < 50 KB 的 DCA
find docs/dca/ -name "DCA_*.html" -size -50k

# research index 反映 v12.3 比例
grep -c "v12.3" docs/research/index.html
```

—

## 11. 邊界條件

- **Ticker 別名**（`2330` vs `2330TW`、`2330` vs `TSM`）：manifest 各列為 row，視為兩個獨立 ticker 處理（兩版都升）。**不要自動合併**。
- **JP ticker（6146T / 6857T 等）**：filings 來源是 EDINET / TSE。WebSearch 必須含 `site:disclosure2.edinet-fsa.go.jp` 或「<TICKER> 有価証券報告書」。
- **TW ticker**：filings 看公開資訊觀測站（mops.twse.com.tw）；客戶結構常匿名（「客戶 A」「客戶 B」）→ §8.H 直接照引匿名占比 + 註「公司未具名」。
- **無 DCA 的 ticker**：manifest `notes` 寫 `no-dca`，skip Step 3。
- **DD 多版本**（如 `DD_2383TW_v3.html`、`DD_2383TW_v10_20260415.html`）：只升**最新日期**的，舊版本 / 帶 `vNN` infix 的不動。
- **pre-v12 重檔**：work 量比 v12.0→v12.3 大很多（要從零補 dd-meta JSON 全 24 欄）。預設**跳過**，留最後 dedicated batch 處理。若 pending 全清才會被選中。

—

## 12. 失敗模式（不要做這些）

| 反模式 | 為什麼禁止 |
|---|---|
| 用 `git add .` / `git add -A` | 會帶進 untracked 的 ID HTML / cache，違 CLAUDE.md |
| 數字裸寫無 source | 違 no-fabricate 鐵律 |
| 加空白行 / 重複 bullet 撐到 80 KB | 會被 cold review 抓 |
| sed 暴力替換 DCA anchor | 留半句不通順；違 Step 6.2 |
| 未 pull 直接 commit | manifest race 必爆 |
| 一次 claim > 5 ticker | review 負擔不可控 |
| 批次混 v12.x + pre-v12 | 工時不均，pre-v12 拖死 batch |
| 順手重跑 DCA | 不在本 skill scope，會撐爆 batch |
| 寫「依 industry 通常」當推估基礎 | 違嚴謹度 D；要寫具體 |
| 跳過 Step 5 sync 直接 commit | research index 滯後，違 CLAUDE.md |

### 12.1 已觀察到的真實偷工模式（2026-05-16 cold review 抓到，務必避免）

對首批 ~50 ticker 隨機 cold review 4 檔（MRVL/AAPL/AMZN/LLY），**3/4 有「manifest 寫已做但 body 沒做」的偽完成**。這是 anti-laziness gate 沒擋到的盲區，是 patcher 的偷工高發區。**寫 manifest notes 前，務必對 body 做這些 grep 驗證**：

| 偷工模式 | 真實案例 | grep 驗證指令 |
|---|---|---|
| **§13.4 peer table 是空殼** `<table>` 內無 `<tr>`，manifest 卻寫「點名 3-5 家 peer」 | AAPL §13.4：manifest 寫 mega-cap platform tier (MSFT/GOOGL/META/AMZN)，DD body 的 `<table>` 整個是空（L888-889） | `awk '/§13\.4/,/<\/table>/' docs/dd/DD_<T>_*.html \| grep -c "<tr>"` 應 ≥ 4 |
| **§11 三段用 `<li>` bullet** 違 v12.3 ≥ 60 字獨立段落硬規格 | AMZN §11：用 `<li>` 三條 30-40 字 bullet，違規 | `awk '/§11.*議價權/,/<\/section>/' docs/dd/DD_<T>_*.html \| grep -E "<p>[^<]{60,}.*議價\|<p>[^<]{60,}.*上游"` 應有 3 段獨立 `<p>` |
| **§8.H 整節缺失** dd-meta 標完成但 body 沒寫 top-1/5/10 子節 | LLY §8.H：dd-meta 標 3 wholesaler，body 整個 `<h3>客戶結構深度</h3>` 子節缺失 | `grep -c "top-1\\|top-5\\|top-10\\|客戶結構深度" docs/dd/DD_<T>_*.html` 應 ≥ 3 |
| **§9 manifest 護城河等級 vs dd-meta `moat` 不一致** | AMZN：manifest 寫「composite 9 → S 級」但 dd-meta JSON `"moat": "A"` | `grep -E '"moat":\s*"[SABCX]"' docs/dd/DD_<T>_*.html` vs §9 body 結論段比對 |
| **SBC % 三處數字不一致**（§10 / §12 / 計算值對不上） | AAPL：§10=2.6% / §12=2.88% / 實算=3.09%（$12.863B/$416.16B） | 同一數字若在 ≥ 2 處出現，必須一致；改完用 `grep "SBC" docs/dd/DD_<T>_*.html \| grep -oE "[0-9]+\.[0-9]+%"` 看是否有衝突 |
| **M&A 金額用初報估算值，沒更新到 closing 後條款** | MRVL Celestial AI 用 CNBC 2026-04-20 初報 $2.5B，未更新到 2026-02 closing 後 $3.25B upfront / 最高 $5.5B | 對所有 5Y M&A 用 WebSearch cross-verify 至少 1 個（最新 / 最大金額那筆），優先看公司 8-K 而非媒體初報 |

**心法**：manifest notes 是「自報」，body 是「事實」。Cold review 比對的就是這兩者的 gap。**寫 notes 前先回 DD body 用 grep 驗證每一條，再下筆寫 notes**。

—

## 13. 完成檢查清單（每個 batch 結束自檢）

- [ ] 3 個 DD HTML 都 ≥ 80 KB
- [ ] 對應 DCA 全部 ≥ 50 KB（或標 no-dca）
- [ ] `validate_dd_meta.py` 對 3 ticker 都過
- [ ] dd-meta JSON `schema: v12.3` + `<meta name="dd-schema-version" content="v12.3">`
- [ ] §5.F / §8.H / §9 兩軸 / §11 三段 / §12 SBC + M&A / §13.4 peer tier checklist 全勾
- [ ] **§13.4 peer table 真有 ≥ 3 `<tr>` 行**（不是空 `<table>`；參 §12.1 grep 指令）
- [ ] **§11 三段是獨立 `<p>` 段落 ≥ 60 字**（不是 `<li>` bullet）
- [ ] **§8.H 真有 top-1 / top-5 / top-10 子節**（不只 dd-meta 標完成）
- [ ] **manifest 護城河等級 vs dd-meta `moat` 欄位字面一致**
- [ ] **同一數字（SBC% / 客戶% / 金額）在 DD 多處出現時值一致**
- [ ] **M&A 5Y 表至少 1 個金額已 cross-verify 公司 8-K / 官方公告**（非媒體初報）
- [ ] 所有數字有 inline source（隨機抽 4 個目視確認）
- [ ] §1 verdict 推導鏈句子寫上
- [ ] §1 末段「verdict 變更紀錄」句子寫上（變 → 寫主因；不變 → 寫「verdict 不變 [X]」）
- [ ] 若 verdict 變了：dd-meta `signal` 改新值、manifest notes 標 `verdict-shift A→B`、對應 DCA 加 TODO comment
- [ ] 若 major-downgrade（A+/A → C/X）：manifest notes 標 `⚠️-major-downgrade`，cold review 已對該 ticker 觸發（不等 5 batch 週期）
- [ ] commit message 含 `verdict shifts: ...` 行
- [ ] manifest 3 ticker → done
- [ ] `update_dd_index.py` 跑過
- [ ] commit + push 成功（沒 stage 任何 ID HTML 或 cache）
- [ ] 若 done 數除 3 = 5 整數倍 → cold review 已 spawn

全勾才算 batch 完成。
