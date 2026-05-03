---
name: id-review
description: 對既有產業 DD（Industry DD / ID）跑 cold-review critic 並 patch 大錯。觸發：用戶要求「改 / review / audit / patch / 驗證」某份既存 ID 報告，或詢問「這份 ID 還活著嗎 / 哪裡有大錯 / 要改什麼」。本 skill 把「critic 跑 + 大錯/cosmetic 分類 + user-in-the-loop patch + commit & push」這個工作流固化下來。**不寫新 ID**（那是 industry-analyst skill）；**也被 industry-analyst Step 8.7 強制呼叫**做新 ID 寫稿後的 mandatory critic gate。
version: v1.1
date: 2026-05-02
---

# id-review skill v1.1

## 【角色定位】

`id-review` 不寫稿、不做 PM 決策。它做兩件事：
1. **獨立修現有 ID**：用戶說「改 ID_X」/「驗證 ID_X 哪裡要改」→ 跑 critic、分類大錯/cosmetic、patch、push
2. **被 industry-analyst 呼叫做 publish gate**：industry-analyst Step 8.7 強制 spawn `id-review` 的 critic phase；若找到 ≥1 🔴 CHANGES_CONCLUSION → blocking publish

`industry-thesis-critic` 是 sub-agent（位於 `~/.claude/agents/industry-thesis-critic.md`），是 `id-review` 的工具，不是 skill。

---

## 【觸發】

使用者表達以下任一意圖時觸發：
- **修正意圖**：「改 ID_X」/「patch ID_X」/「修 ID_X 的錯」
- **驗證意圖**：「review ID_X」/「audit ID_X」/「驗證這份 ID」
- **健康度查詢**：「ID_X 還活著嗎」/「哪裡有大錯」/「要改什麼」
- **明確 invocation**：`/id-review {file or theme}`

不觸發：
- 「ID_X 寫了什麼」/「介紹一下 X 產業」（純資訊查詢，直接回答即可）
- 「我考慮加倉 X 產業」（這是 buy-decision 情境，CLAUDE.md 已規定 spawn `industry-thesis-critic` 但不必動 patch）

---

## 【Patch Mode】

預設 **Mode (a) user-in-the-loop** — 每條 patch 前先 ask user 確認。

| Mode | 行為 | 適用 |
|---|---|---|
| **(a) user-in-the-loop**（預設）| 每條 patch 前展示 diff + ask yes/no/skip | 起步 + critic 還沒驗證準度時 |
| (b) auto-patch 大錯 + ask cosmetic | 🔴 自動 patch / 🟢 ask | 跑熟後（critic 誤判率 < 10%）|
| (c) full auto | 全部 auto patch | 不建議（stake 太高）|

升級時機：跑過 5+ 次 mode (a) 後，若觀察到 critic 大錯分類準確 → 用戶可主動說「升級成 mode (b)」。

---

## 【Step-by-Step 流程】

### Step 0：累積上限偵測（v1.1 新增）

每次 skill invocation 開始時，**先**執行本步驟，再決定走 patch flow 或 consolidation flow。

**讀 ID 檔，count：**
- `"🔴 大錯"` 或 `"🔴 Decision-time patch"` 標記數（N_patches）
- `§0 critic banner block` 總字元長度（banner_chars）
- `id-meta.id_version`（例如 v1.3）

**觸發 consolidation 條件（任一即觸發）：**

| 條件 | 閾值 |
|---|---|
| patch 標記累積（N_patches） | ≥ 5 個 |
| banner block 總字元（banner_chars） | > 2000 字 |
| id-meta.id_version | ≥ v1.5 |

**判定邏輯：**
- 全部未滿足 → 正常進 **Step 1**（patch flow）
- 任一條件滿足 → 問 user 確認：

  > 「本 ID 累積 patch 已達 cap（{N_patches} 標記 / {banner_chars} 字 / id_version {V}）。建議先 consolidate v2 再做新 patch。確認進 consolidation flow？(yes / no — no 則繼續疊 patch)」

  - **yes** → 跳到 **Step C1**（consolidation flow），不進 Step 1-7
  - **no** → 繼續 **Step 1-7**（user 接受 banner 變長）

---

### Step C1：列出 banner 內所有 patch 條目給 user 預覽

從 §0 banner 解析出每個 `"🔴 大錯 ①/②/..."` 或 `"🔴 Decision-time patch"` 條目，顯示成 numbered list：

```
目前 banner 累積：
  #1: {Pass 1 大錯 ①} — {one-line summary} → 影響章節：§X
  #2: {Pass 1 大錯 ②} — ... → 影響章節：§Y
  #3: {Pass 2 ...} → ...
  ...
準備併入對應章節，§0 banner 清空為單行 v2 marker。
```

### Step C2：對每條 patch 提議併入位置 + user 確認

對每條 patch：
- 從 patch 內容辨識它影響哪個章節（patch 文字常自帶 `"§6/§11/§14"` 等提示）
- 顯示：

  ```
  Consolidation #{i}/{N}：
    原 banner 文字：{exact text}
    建議併入：§{X} 的 {paragraph hint}
    併入方式：{inline 加入 / 取代 / append}

  確認？(yes / 改成 §Y / skip — 此條留 banner)
  ```

- user 回應對應動作：
  - `yes` → 記錄 merge plan
  - `改成 §Y` → 用 user 指定章節
  - `skip` → 不併入該條（留 banner）

### Step C3：執行 merge

對每條 `yes` / `改成 X` 的條目：
- 用 Edit 工具把 patch 內容寫到目標章節的合適位置（保留 inline mark 如「(post-Pass-3)」作為 audit trail）
- 從 §0 banner 對應條目刪除

### Step C4：§0 banner 清空 + 寫 v2 marker

把 §0 banner 整個 block 替換為單行：

```html
<div style="background:#F0FDF4;border:2px solid #16A34A;border-radius:6px;padding:10px 14px;margin:14px 0;font-size:12.5px">
  <strong style="color:#15803D">✅ v2 consolidated {YYYY-MM-DD}</strong>：過往 Pass 1-{N} patch 已整合進對應章節；修改歷程見 git log。<a href="_consolidation_{date}.md">consolidation manifest</a>
</div>
```

Optional：寫一份 `docs/id/_consolidation_{Theme}_{date}.md` 列出每條 patch 從哪移到哪（audit trail，不上 git，本地保留）。

### Step C5：bump id-meta + 加欄位

更新 ID 內 `<script id="id-meta">` JSON：
- `id_version`: vX.Y → v2.0（or v3.0 if 已是 v2.x）
- 新增 `consolidation_date`: "{YYYY-MM-DD}"
- 新增 `consolidation_count`: incrementing（首次 1）
- `sections_refreshed.judgment`: 今日

### Step C6：validator + commit + push

```bash
python3 scripts/validate_id_meta.py docs/id/ID_X.html
```

validator 通過 → commit message 格式：

```
Consolidate ID_{Theme} v{old} → v2.0 (Pass 1-{N} integrated)

Past patches integrated into native chapters:
- {patch #1} → §X
- {patch #2} → §Y
...

§0 banner cleared to v2 marker. id-meta.id_version bumped.
Audit manifest at docs/id/_consolidation_{Theme}_{date}.md (local only).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

push 到 main（直接 push，不開 PR）。

---

### Step 1：定位 ID 檔案

從用戶輸入辨識 target ID：
- 直接給檔名：`ID_AIInferenceEconomics_20260430.html` → 直接用
- 給主題名：「AI Inference Economics」/「先進封裝」 → grep `docs/id/INDEX.md` 找最新一份
- 給 URL：`https://research.investmquest.com/id/ID_X.html` → 抽出檔名映射本地路徑

若找到多份（同主題不同日期）→ 用最新一份；若找不到 → 告訴用戶「沒找到」並列 `docs/id/` 中相近主題候選。

### Step 2：input mode dispatch + 跑 critic Pass 1

**先判斷 Mode，再 spawn critic（或跳過）：**

| Mode | 觸發條件 | 行為 |
|---|---|---|
| **A** — 預設，full critic spawn | 用戶說「改 ID_X」/「review ID_X」，沒有附具體 feedback | Spawn critic Pass 1，generic prompt（現有行為） |
| **B** — user-feedback-driven | 用戶給了具體意見，如「我覺得 §Y 有 Z 問題」 | Spawn critic Pass 1，framing：validate user's points + find additional blindspots |
| **C** — existing-report | 用戶說「我已經有 critic report 在 docs/id/_critic_X.md，直接用它」 | 不 spawn，直接讀現有 report，跳到 Step 4 |

User 可以混用（如「Mode B + skip Pass 2」—— 若用戶說「feedback 已很完整，不用跑第二輪」可跳過 Step 3）。

#### Mode A（預設）— Full critic spawn

Spawn `industry-thesis-critic` sub-agent（必用 Sonnet 跨模型）：

```
Agent({
  description: "Pass 1 critic on {Theme}",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: """
You are operating as the industry-thesis-critic sub-agent.
Read spec at /Users/ivanchang/.claude/agents/industry-thesis-critic.md.

ID file path: {absolute path to docs/id/ID_X.html}
User's intent: {如「驗證這份 ID 哪些段落需要改」/「考慮加倉前體檢」}

Run all 7 items + Item 6.5 CONCLUSION_IMPACT triage（Item 7 = thesis box sync, agent v1.3 加）.
Save report to /Users/ivanchang/financial-analysis-bot/docs/id/_critic_{Theme}_{YYYYMMDD}.md.

After saving, return brief summary:
1. Verdict (INTACT / AT_RISK / BROKEN)
2. Count of 🔴 CHANGES_CONCLUSION
3. Count of 🟡 PARTIAL_IMPACT
4. Count of 🟢 COSMETIC
5. Top 3 issues by CONCLUSION_IMPACT priority
"""
})
```

時長：~15-20 分鐘。讀回 brief summary。

#### Mode B（NEW）— User-feedback-driven

在 Mode A prompt 基礎上，在 `User's intent` 後插入以下 framing block：

```
User has provided the following peer-review points (already done their analysis):
  1. {point 1 with their reasoning}
  2. ...

Your job: independently validate or refute each point (don't just rubber-stamp).
Then run the standard 7-item checklist + look for ADDITIONAL blindspots user missed.
In your report, structure as:
  - Independent assessment of user's N points (agree/disagree/partial + why)
  - Additional blindspots not caught by user
  - Standard verdict + 7-item findings (含 Item 7 thesis box sync)
```

其餘（save path、brief summary 格式）與 Mode A 完全相同。

#### Mode C（NEW）— 直接使用現有 critic report

- 不 spawn sub-agent
- 用 Read 工具讀 `docs/id/_critic_{Theme}_{date}.md`（user 指定路徑）
- 提取 findings 清單（🔴/🟡/🟢 條目）
- 直接跳到 **Step 4（彙整）**
- 注意：若 Mode C 只提供了 Pass 1 findings，Step 3（Pass 2）tier 規則仍適用 — Q0 仍需補跑 Pass 2，除非 user 明確說「skip Pass 2」

### Step 3：條件性跑 Pass 2（Q0 必跑 / Q1+ 視情況）

讀 ID 的 `id-meta` JSON 找 `quality_tier`（若沒設視為 Q1）。

| Quality Tier | Pass 2 強制？ |
|---|---|
| Q0 Flagship | ✅ 強制（這是 PM 級重大決策依賴的 ID）|
| Q1 Standard | 條件式：Pass 1 verdict = AT_RISK / BROKEN OR ≥1 🔴 found |
| Q2 Quick | ❌ 不跑（pass 1 已足夠）|

Pass 2 prompt 重點是 **focused 大錯掃描**（不是重做 6 項）：

```
Agent({
  description: "Pass 2 focused 大錯 scan on {Theme}",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: """
You are doing a focused second-pass critic. Pass 1 report at: 
/Users/ivanchang/financial-analysis-bot/docs/id/_critic_{Theme}_{date}.md.

Hunt for ADDITIONAL conclusion-changing errors Pass 1 might have missed:
1. §0 thesis cornerstone numbers (key magnitudes)
2. §6 player ranking facts (誰 > 誰 的支撐)
3. §14 portfolio actionable claims
4. Cross-ID consistency with recent critic findings (check sister IDs)
5. §9.5 Kill scenarios — real steel-man or strawman?
6. §13 falsification metrics — any close to crossing?
7. Under-rated tickers (中等 tier 但事實顯示應升 🔴)

Save to /Users/ivanchang/financial-analysis-bot/docs/id/_critic_pass2_{Theme}_{date}.md.

Return: how many ADDITIONAL CHANGES_CONCLUSION errors found + biggest one.
"""
})
```

### Step 4：彙整 + 告訴 user

合併 Pass 1 + Pass 2 findings，分類：

```
🔴 CHANGES_CONCLUSION（會改變投資結論的）：N 條
  1. {one-line title}
  2. ...

🟡 PARTIAL_IMPACT（影響 sizing/magnitude 但不變方向）：M 條
  1. ...

🟢 COSMETIC（事實對齊 / 內部一致性，不變結論）：K 條
  1. ...
```

問用戶：

```
要動哪些？
  A) 全部 (N+M+K) 條
  B) 只 🔴 大錯 (N 條)
  C) 🔴 大錯 + 🟢 cosmetic 順手修（推薦）
  D) 自選編號（如「1, 3, 5」）
  E) 都不動，我自己看 critic report 就好
```

### Step 5：依用戶選擇 patch（mode a — 每條 ask）

對每條要動的 finding：

5.1. **顯示要改什麼**
```
Patch {N}/{total}: {finding title}
位置：{section, e.g. §12 #1 thesis 支撐事實}

--- 原文 ---
{exact existing text}

--- 修正建議 ---
{patched text with FET claim tags if numerical}

理由：{from critic report}
```

5.2. **問用戶**：
```
這條動嗎？
  yes / no / skip / 改成 {自訂版本}
```

5.3. **依回應動作**：
- `yes` → Edit 工具直接 patch
- `no` / `skip` → 跳過，記錄到「未 patch」清單
- `改成 X` → 用用戶的版本 patch
- 用戶沒回覆 → 默認 skip（保守）

### Step 6：寫 critic banner + 更新 id-meta

所有 patch 完成後，在 ID 文件頂部插入或更新 critic banner（標準格式）。

**Banner 寫法規則（v1.1 明確化）：**

| 情境 | 行為 |
|---|---|
| 首次 review（Pass 1） | 新建 banner block |
| 同次 session 內 Pass 2/3 findings | 整合進同一 banner block 的子條（不開新 block） |
| 跨 session 後續 Pass（新的 invocation） | 在現有 banner 內新增子節，如 `🔴 Decision-time patch (Pass N, YYYY-MM-DD)`；不開新 block |
| banner 達到累積上限 | 不再疊新 banner → 見 Step 0（consolidation 觸發條件） |

原則：**同一個 ID 永遠只有一個 §0 banner block，**多次 pass 的 findings 疊加在同一 block 內。何時停止疊加由 Step 0 的 cap 規則控制。

**Banner 標準格式（保持不變）：**

```html
<div style="background:#FEF2F2;border:2px solid #DC2626;border-radius:6px;padding:14px 16px;margin:14px 0;font-size:12.5px;line-height:1.7">
  <strong style="color:#991B1B;font-size:14px">🛡️ Critic Pass {N} + Red Team — {N} 條 CHANGES_CONCLUSION 大錯已 patch（{date}）：</strong><br><br>

  <strong>🔴 大錯 ①：{title}</strong><br>
  事實：{description}<br><br>

  ...

  <strong>🟢 順手修 cosmetic：</strong><br>
  ⑤ {short}<br>
  ⑥ {short}<br><br>

  <strong>📊 修正後 portfolio implication（PM 級）：</strong>{方向不變/變 + conviction 變化}<br><br>

  完整 critic 報告：<a href="_critic_{Theme}_{date}.md">Pass 1</a> + <a href="_critic_pass2_{Theme}_{date}.md">Pass 2</a>
</div>
```

更新 `id-meta` JSON：
- `id_version`: bump（v1.0 → v1.1 → v1.2 ...）
- `sections_refreshed.judgment`: 今日日期
- `sections_refreshed.market`: 今日（若 Pass 2 有更動 market 段）

### Step 6.5：Thesis box alignment + Body repetition sweep（mandatory before commit — v1.2 加 thesis box，v1.3 加 body sweep）

Step 6 的 critic banner 與 id-meta version bump 完成後，做**兩個 sub-step** 才進 Step 7 commit：

#### Step 6.5a — Thesis box sync check

**回頭讀 `<div class="thesis-box">` 整段「本 ID 一句 Thesis（非共識）」**，逐句對照 Step 5 patch list 判斷：

1. thesis 開頭主軸句是否仍對？
2. (1)(2)(3) bullet 的 cornerstone fact 是否被本次 patch falsify 或修正？需加 inline `（critic YYYY-MM-DD 修：...）` 註？
3. thesis 末段 PE / conviction / alpha gap 結論句是否反映了 §11 ranking + §12 / §13 / §8 judgment card 變化？特別注意：
   - **個股 conviction tier 變化**（high → mid 等）— 不能只在 §11 / §8 寫，thesis box 也要點名
   - **PE / multiple 從 uniform → tiered**（如真 monopoly vs 雙寡占分層）— 不能只在 §12 寫
   - **cornerstone consensus framing 過時**（如「共識 $X」是 stale sell-side bear case）— 引述的非共識 gap 數字要改

#### Step 6.5b — Body repetition sweep（v1.3 加 — 2026-05-03 踩坑教訓）

Thesis box 改完後，**grep 全 HTML 找重複 thesis 級數字的 inline 出現**。常見重複位置：

- **§3 S-curve / 技術演進表 + 階段描述**：常 echo thesis 的 PE / margin / share 數字
- **§5 value chain table / 利潤池表 + 對應 insight box**：常重述 thesis 的 margin 預測
- **§6 player table / 個股矩陣**：「最近數據」「conviction」欄常 echo thesis 的數字
- **§4 TAM 註 / §10.5 catalyst 表**：常以 thesis 級數字（如「$100B 合約」）作 anchor
- **§9.5 反方論證 / §9 風險矩陣**：與 thesis 同類的 framing 也要重檢

**Sweep 方法**：用 `grep -nE "(關鍵數字1|關鍵數字2|stale framing 字樣)" docs/id/ID_X.html` 找所有獨立出現位置；每個獨立 stale 出現都需 inline 加修正註（`（critic YYYY-MM-DD 修：...）`）或 strikethrough + replace，**不能只靠 banner 的 narrative explanation cover**。

若任一 sub-step 發現需更新，回 Step 5 patch 工具補一輪。若確認不需更新，commit message 明文標 `thesis box + body sweep reviewed, no update needed` 留 audit trail。

#### Step 6.5c — Conversational Framework Promotion check（v1.4 加 — 2026-05-03 連續 2 次踩坑）

Patch + commit 完成後，**user 常會接著問 methodology / 監控 / 後續觀察問題**（典型例子：「LRCX vs TEL vs AMAT 哪個指標最敏感」「ASIC 生態 vs AMD ROCm 誰先吃 inference share」）。當你的回答構成 **substantive 分析 framework** 時，**必須主動把它 promote 到 HTML**，不能只活在對話層。

**Trigger signals**（任一達成即 promote）：
- 答案構成**新分析結構**：decomposition / taxonomy / bucket 拆分（例 inference TAM 三段式 / value chain 利潤池分層 / kingmaker vs duopoly subsystem 分類）
- 答案含**可測量閾值**：具體百分比、$ 數字、ratio condition（例「ALD YoY > 40% 連 2 季 + TEL 半期 ALD < 25%」「Bedrock per-token cost 降幅 > 30%」「AMD 非 Big-4 hyperscaler ≥ 40%」）
- 答案會**改變 PM 對 thesis 的解讀**（例「AMD 20% inference share 與 ASIC 40-50% 取代不衝突，因為不同 bucket」）

**Promote 到哪**：
- 新分析結構 → 新增 §10.X / §11.X 子節 + insight box
- 可測量閾值 → §13 falsification table 新 F-N row
- thesis interpretation refinement → 對應 §12 NC card 加 caveat（j-infer 或 j-falsify 內標 critic 加註）

**不需 promote 的反例**：純 factual lookup（「BESI 上次法說是哪天」）/ 單點 ticker 建議 / 風格偏好（「結論段要不要分段寫」）

**為什麼 mandatory**：連續 2 天踩同盲點：
- **2026-05-02 WFE v1.1 → v1.2**：user 問 LRCX/TEL/AMAT GAA 板塊推擠驗證指標 → 給 ALD revenue YoY 閾值 framework → user 質問「已經有寫入網頁了嗎」才補 §10.5 LRCX row + §13 F-8 trigger。
- **2026-05-03 CUDA/ROCm v1.1 → v1.2**：user 問 ASIC vs ROCm inference share 競爭 → 給 3-bucket 拆解 framework → user 質問「這個已經有寫入網頁了嗎」才補 §10.6 + §13 F-7/F-8 + §12 NC#1 caveat。

兩次都是同一 pattern：對話 framework 沒進 HTML → user 主動 catch → 補 patch。明文寫成 6.5c 規則才能根除。

**為什麼 6.5a + 6.5b + 6.5c 都是 mandatory**：歷史踩坑：
1. **2026-05-02 WFE v1.1 → v1.2**：內文章節 patch 完但 thesis box 漏掉 ASML conviction 降級 + PE 分層，user 質問才補 → 催生 6.5a。
2. **2026-05-03 ASIC Design Service v1.2 → inline backfill**：thesis box / banner / NC card 都修了，但 §3 S-curve、§5 value chain、§6 player table 6 處 inline stale 字樣漏改，user 質問「已經改完了嗎」才補 → 催生 6.5b。
3. **2026-05-03 CUDA/ROCm v1.1 → v1.2**：對話 methodology framework（3-bucket inference TAM）沒進 HTML，user 質問「這個已經有寫入網頁了嗎」才補 → 催生 6.5c。

Thesis box 是讀者第一眼結論段；body sections 是讀者滾動細節；conversational framework 是 user 與 agent 對話中 emerge 的 nuance — 三者都必須同步進 HTML，否則 ID 留下 incomplete audit trail。Item 7（critic agent 端）+ Step 6.5（skill 端）構成雙層保險；6.5a + 6.5b + 6.5c 構成完整 sync 流程。

### Step 7：驗證 + commit + push

```bash
python3 scripts/validate_id_meta.py docs/id/ID_X.html
python3 scripts/validate_source_blacklist.py docs/id/ID_X.html --report
```

任一失敗 → 告訴用戶 + 暫停 commit。

驗證過 → commit message 標準格式：

```
Patch ID_{Theme}: {N} conclusion-changing errors + cosmetic

Critic 2-pass (Sonnet, agent v1.2 with CONCLUSION_IMPACT) found
{N} 大錯（會改變投資結論的）+ {M} partial + {K} cosmetic.

🔴 CHANGES_CONCLUSION（{N} patched）:
1. {title} — {one line}
2. ...

🟢 COSMETIC (順手修 {K_done}/{K} 條):
{list}

Portfolio implication: {方向不變/變化 + conviction 變化 + 配置調整}

Reports:
- docs/id/_critic_{Theme}_{date}.md (Pass 1)
- docs/id/_critic_pass2_{Theme}_{date}.md (Pass 2)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

push 到 main（直接 push，不開 PR — 與既有 stock-analyst / industry-analyst 一致）。

---

## 【接軌：被 industry-analyst Step 8.7 呼叫】

industry-analyst skill 在 publish 前必須跑 critic gate（Step 8.7，介於 Step 8.5 Pre-Publish Gate 與 Step 9 HTML 產出之間）。

**呼叫方式**（industry-analyst skill 端執行）：

```
1. industry-analyst 寫好 ID HTML 草稿（暫存於 /tmp/ 或 staging）
2. industry-analyst 自己呼叫 critic（不是觸發 id-review skill 全流程）：
   - Spawn industry-thesis-critic sub-agent
   - User intent: 「pre-publish gate check」
   - Pass 1 only（Q1+）或 Pass 1+2（Q0）
3. 讀回 verdict 與 finding count
4. Gate 判定：
   ┌─────────────────────────────────────────────────────────┐
   │ 0 🔴 CHANGES_CONCLUSION    → ✅ Pass，繼續 Step 9 publish │
   │ ≥1 🔴 + Q0 Flagship         → 🔴 BLOCKING，必須先 fix    │
   │ ≥1 🔴 + Q1 Standard         → ⚠ WARNING，user 決定 ship/fix │
   │ ≥1 🔴 + Q2 Quick            → ⚠ WARNING（同 Q1）          │
   └─────────────────────────────────────────────────────────┘
5. BLOCKING → 把 critic findings 給 user 看 + 在 industry-analyst skill 裡修正
              修正完重跑 critic 直到 0 🔴 才放行
6. WARNING → 告訴 user 大錯內容；user 選擇：
   - "ship" → 加 critic banner 後 publish（user 接受帶大錯 ship）
   - "fix" → 進入 id-review patch 流程
```

**為什麼 Q0 強制 / Q1+ 警告**：
- Q0 是母題級重大決策依賴，帶大錯 publish 會 propagate 到子題與 PM 配置
- Q1/Q2 影響面較窄，user 自決可接受

---

## 【tier 判定 default 規則】

若 ID 沒設 `quality_tier` → 依以下默認：
- `mega = "semi"` AND theme 含 "Master" / "母題" / 出現在 INDEX.md 註記為 🔴 母題 → Q0
- 一般子題（INDEX.md 標「子題」/「💎」）→ Q1
- 其他 → Q1（保守）

---

## 【Output Format（給 user 看的最終訊息）】

完成後給 user 一份摘要（不是長文）：

```
✅ id-review 完成：{Theme}

🛡 Critic verdict: {INTACT / AT_RISK / BROKEN}
🔴 大錯：{N} 條（已修 {N_done}）
🟡 Partial: {M} 條（已修 {M_done}）
🟢 Cosmetic: {K} 條（已修 {K_done}）

⏱ 工時：{total minutes}
  - Pass 1 critic: {min}
  - Pass 2 critic: {min}（若跑）
  - Patch + ask 互動: {min}
  - Validate + commit + push: {min}

📊 Portfolio implication: {方向 + conviction 變化}

📝 完整報告：
  - docs/id/_critic_{Theme}_{date}.md
  - docs/id/_critic_pass2_{Theme}_{date}.md（若有）

🔗 Commit: {sha}
🔗 Live: https://research.investmquest.com/id/{filename}
```

---

## 【常見失敗情境】

### ❌ Critic 找不到 ID 的 §12 / §13 / §10.5
→ ID 結構不是標準格式（可能舊版 v1.0 / v1.5 沒有 §12 章節）
→ 告訴 user：「ID 格式較舊，無 §12 Non-Consensus / §13 Falsification — critic 只能跑 partial」
→ 跑能跑的部分 + 標註不可跑項

### ❌ 黑名單 source validator fail
→ ID 引用了內容農場
→ 在 patch 階段加一條：「移除黑名單 source: {url}」+ 替換為合格 source 或標 [unverified]

### ❌ critic Pass 2 與 Pass 1 互相矛盾
→ 罕見但可能（兩次跑 Sonnet 結論不同）
→ 給 user 兩份對照，由 user 判斷哪個準

### ❌ user 一直 skip 所有 patch
→ 完成所有 ask 後若 0 patch → 不寫 banner、不更新 id-meta、不 commit
→ 告訴 user：「無修改，僅產出 critic report 供參考」

---

## 【後續升級】

- v1.1（current，2026-05-02）：加 Step 2 input mode dispatch (A/B/C) + Step 0/C1-C6 consolidation phase + Step 6 banner 寫法明確化（append vs rewrite）。觸發來源：2026-05-02 ID_AIInferenceEconomics 手動 patch 暴露 3 個 gap + 1 個缺漏概念（banner 累積 / consolidation）
- v1.2：原 v1.1 內容 — 跑熟後降為 mode (b) auto-patch 大錯
- v1.3：加 cron 排程模式（weekly 自動跑所有 Q0 ID 的 critic，產 alert 但不 patch）
- v1.4：跨 ID 一致性 reconcile（critic 找到 cross-ID 數字差異時，自動 patch 兩份 ID 的數字）
- v2.0：擴展為 `dd-review`（同樣模式但對 stock-analyst 的 DD 而非 ID）

---

## 【操作原則】

1. **不寫新內容**：本 skill 不創新、不擴充 thesis；只 patch critic 找到的問題
2. **每條 user-in-the-loop**：mode (a) 是預設，每條 patch 前 ask
3. **critic 是 ground truth**：不質疑 critic 分類；user 若不同意可 skip 該條
4. **Banner 不可省**：所有 patch 完成必須在 ID 頂部寫 critic banner（記錄修正歷程）
5. **commit 訊息要結構化**：列大錯/cosmetic 分類 + portfolio implication
6. **失敗不靜默**：validator fail / critic 找不到章節 / user skip 全部 → 都明確告訴 user
7. **Banner 累積上限**：≥5 patch 標記、>2000 字、或 id_version ≥v1.5 → 進 consolidation flow（Step 0 → C1-C6），不再疊新 patch；此規則不可繞過
