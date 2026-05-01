---
name: id-review
description: 對既有產業 DD（Industry DD / ID）跑 cold-review critic 並 patch 大錯。觸發：用戶要求「改 / review / audit / patch / 驗證」某份既存 ID 報告，或詢問「這份 ID 還活著嗎 / 哪裡有大錯 / 要改什麼」。本 skill 把「critic 跑 + 大錯/cosmetic 分類 + user-in-the-loop patch + commit & push」這個工作流固化下來。**不寫新 ID**（那是 industry-analyst skill）；**也被 industry-analyst Step 8.7 強制呼叫**做新 ID 寫稿後的 mandatory critic gate。
version: v1.0
date: 2026-05-01
---

# id-review skill v1.0

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

### Step 1：定位 ID 檔案

從用戶輸入辨識 target ID：
- 直接給檔名：`ID_AIInferenceEconomics_20260430.html` → 直接用
- 給主題名：「AI Inference Economics」/「先進封裝」 → grep `docs/id/INDEX.md` 找最新一份
- 給 URL：`https://research.investmquest.com/id/ID_X.html` → 抽出檔名映射本地路徑

若找到多份（同主題不同日期）→ 用最新一份；若找不到 → 告訴用戶「沒找到」並列 `docs/id/` 中相近主題候選。

### Step 2：跑 critic Pass 1

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

Run all 6 items + Item 6.5 CONCLUSION_IMPACT triage.
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

所有 patch 完成後，在 ID 文件頂部插入或更新 critic banner（標準格式）：

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

- v1.1：跑熟後降為 mode (b) auto-patch 大錯
- v1.2：加 cron 排程模式（weekly 自動跑所有 Q0 ID 的 critic，產 alert 但不 patch）
- v1.3：跨 ID 一致性 reconcile（critic 找到 cross-ID 數字差異時，自動 patch 兩份 ID 的數字）
- v2.0：擴展為 `dd-review`（同樣模式但對 stock-analyst 的 DD 而非 ID）

---

## 【操作原則】

1. **不寫新內容**：本 skill 不創新、不擴充 thesis；只 patch critic 找到的問題
2. **每條 user-in-the-loop**：mode (a) 是預設，每條 patch 前 ask
3. **critic 是 ground truth**：不質疑 critic 分類；user 若不同意可 skip 該條
4. **Banner 不可省**：所有 patch 完成必須在 ID 頂部寫 critic banner（記錄修正歷程）
5. **commit 訊息要結構化**：列大錯/cosmetic 分類 + portfolio implication
6. **失敗不靜默**：validator fail / critic 找不到章節 / user skip 全部 → 都明確告訴 user
