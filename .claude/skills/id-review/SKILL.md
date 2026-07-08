---
name: id-review
description: 對既有產業報告（Industry DD / ID 或 Industry Discourse / DS）跑 cold-review critic 並 patch 大錯。觸發：用戶要求「改 / review / audit / patch / 驗證」某份既存 ID / DS 報告，或詢問「這份 ID 還活著嗎 / 哪裡有大錯 / 要改什麼」。本 skill 把「critic 跑 + 大錯/cosmetic 分類 + user-in-the-loop patch + commit & push」這個工作流固化下來。**不寫新 ID 或 DS**（那是 industry-analyst skill；industry-ds 已 deprecated 併入 industry-analyst v2.0）；**也被 industry-analyst Step 8.7 強制呼叫**做新報告寫稿後的 mandatory critic gate。v1.5（搭配 industry-analyst v2.0）：**讀目標 HTML id-meta `skill_version` 自動判別模式** — `v2.x` → v2 checklist（cornerstone 6 條 + thesis box sync + V2-1~V2-15 共 15 條——含 3 條 v2 模組抽查（三角對帳/資本週期/priced-in）＋ v1.6 新增 4 條：V2-12 機器欄↔內文同步（sd_verdict/clock_phase/priced_in 等六欄，下游直讀機器欄故矛盾比散文錯更危險）/ V2-13 熱產業時鐘施壓（校準教訓：shortage×Phase II 唯一系統性失效格，勝率 7/25）/ V2-14 kill 套套邏輯與口徑防呆 / V2-15 v2.7 情境手冊實答抽查）；`v1.x` → 現行 ID checklist（legacy 不動）；`--mode ds` → DS-mode 8 條（8 份 legacy DS 仍可 review）。v1.4.1：DS-mode 檢查清單 8 條（DS-1 表格比 / DS-2 因果閉合 / DS-3 供需平衡 / DS-4 §6 三情境 / DS-5 §10 雙路徑 / DS-6 §11 一致性 / DS-8 §6 推導抽查 / DS-9 §1 雙錨點）。
version: v1.6
date: 2026-07-08
---

# id-review skill v1.5

## 【角色定位】

`id-review` 不寫稿、不做 PM 決策。它做兩件事：
1. **獨立修現有 ID**：用戶說「改 ID_X」/「驗證 ID_X 哪裡要改」→ 跑 critic、分類大錯/cosmetic、patch、push
2. **被 industry-analyst 呼叫做 publish gate**：industry-analyst Step 8.7 強制 spawn `id-review` 的 critic phase；若找到 ≥1 🔴 CHANGES_CONCLUSION → blocking publish

`industry-thesis-critic` 是 sub-agent（位於 `~/.claude/agents/industry-thesis-critic.md`），是 `id-review` 的工具，不是 skill。

---

## 【Mode Dispatch — ID v1 / ID v2 / DS】（v1.5：加 v2 自動判別）

本 skill 自 v1.3 起支援多模式。**判別順序（v1.5 起）**：

1. **檔名前綴 = `DS_*.html`** → `--mode ds`（8 份 legacy DS，不讀 id-meta）。
2. **檔名前綴 = `ID_*.html`** → 進一步**讀目標 HTML 的 `<script id="id-meta">` JSON 取 `skill_version`**：
   - `skill_version` 以 `v2`（v2.0、v2.x）開頭 → **ID v2 mode**（套用本檔末「【ID v2 Mode 檢查清單】」段，cornerstone 6 條 + thesis box sync + V2-1~V2-15）。
   - `skill_version` 以 `v1`（或缺欄位 / 解析失敗）開頭 → **ID v1 mode（legacy，現行流程不動）**。
3. `--mode {id|ds}` 顯式參數**覆寫**檔名/skill_version 判別；但 `--mode id` 不強迫 v1 — 仍走 skill_version 子判別（v2 報告即使被傳 `--mode id` 也套 v2 checklist）。若要強制 legacy v1 行為，傳 `--mode id-v1`。

| Mode | 對象 | id-meta | 檢查清單 |
|:---|:---|:---|:---|
| **ID v1**（legacy，預設於舊 ID） | `docs/id/ID_*.html`，`skill_version` v1.x | id-meta | 現行 ID checklist（§12 / §13 / §10.5 / cornerstone fact / thesis box / mega-sub_group）— **legacy 不動** |
| **ID v2**（新格式） | `docs/id/ID_*.html`，`skill_version` v2.x | id-meta | **cornerstone 6 條 + thesis box sync（保留）+ V2-1~V2-15（15 條）**，見本檔末「【ID v2 Mode 檢查清單】」 |
| **DS**（legacy） | `docs/ds/DS_*.html` | ds-meta | DS 8 條，見本檔末「【DS Mode 檢查清單】」 |

**skill_version 讀法**（Step 1 定位檔案後立即執行）：

```bash
python3 - "$ID_PATH" << 'PY'
import sys, re, json
html = open(sys.argv[1]).read()
m = re.search(r'<script id="id-meta"[^>]*>(.*?)</script>', html, re.DOTALL)
sv = "v1.0"  # 缺欄位 / 解析失敗 → fallback legacy v1
if m:
    try:
        sv = json.loads(m.group(1)).get("skill_version", "v1.0")
    except Exception:
        pass
print("MODE=" + ("id-v2" if re.match(r'^v2', sv) else "id-v1"), "skill_version=" + sv)
PY
```

**自動 dispatch**（user 沒傳 `--mode`）：
- `DS_*.html` → mode ds
- `ID_*.html` → 讀 skill_version → id-v2 或 id-v1（上方腳本）

**Spawn 時明確指定**：被 industry-analyst Step 8.7 強制呼叫時，spawn prompt 含 `The skill auto-detects v2 from id-meta skill_version >= v2.0 and applies the v2 checklist`（v2.0 主稿 Step 8.7 已如此寫），critic agent 自行讀 skill_version dispatch；不需在 prompt 硬寫 mode。

**ID v2 mode 與 v1 的差異**：
- v2 沒有 §10/§11/§12/§13/§14 舊編號 — 改 §0-§9 九章。cornerstone fact 與 thesis box sync 改 remap 到 v2 章節（cornerstone 在 §7 Non-Consensus、thesis box 在 §0；§13 falsification 移到 §8 證偽表、§10.5 catalyst 移到 §8 catalyst timeline、§11 ranking 移到 §9 ticker 表）。
- 額外套 V2-1~V2-15（從 DS 搬 8 條 remap + 3 條 v2 模組抽查 + v1.6 4 條:機器欄同步/熱產業時鐘施壓/kill 防呆/手冊實答）。
- 仍讀 id-meta（v2 沿用 id-meta schema 零改動），仍用 `validate_id_meta.py`。

DS 模式下：
- 不檢查 §12 / §13 / §10.5（DS 沒有這些章節）
- 不檢查 ID 銘文（DS 是 ds-meta 不是 id-meta）
- 改檢查 **DS 8 條**（v1.4.1：v1.4 9 條移除 DS-7，因 industry-ds v1.2 把 source-tag 從 inline 移至 §末 aside，Gate 12 已涵蓋結構檢查 + T1 占比；DS-7 ~80% 與 Gate 12 重疊）：DS-1 表格比 / DS-2 因果閉合（升級）/ DS-3 供需平衡 / DS-4 §6 三情境 / DS-5 §10 雙路徑 / DS-6 §11 一致性 / ~~DS-7~~（已移除）/ **DS-8 推導抽查** / **DS-9 §1 雙錨點**
- Banner 寫到 §0 但格式略不同（見 DS Mode 段）
- critic report 路徑：`notes/site-internal/ds/_critic_{Theme}_{YYYYMMDD}.md`（不是 `notes/site-internal/id/_critic_*`）

> **legacy DS 仍可 review**：industry-ds 已 deprecated 併入 industry-analyst v2.0，但 8 份既存 DS 報告凍結保留，`--mode ds` 分支不動，仍可對它們跑 critic + patch。

---

## 【觸發】

使用者表達以下任一意圖時觸發：
- **修正意圖**：「改 ID_X」/「patch ID_X」/「修 ID_X 的錯」/ 「改 DS_X」/「patch DS_X」
- **驗證意圖**：「review ID_X」/「audit ID_X」/「驗證這份 ID」/ 「review DS_X」/「驗證這份 DS」
- **健康度查詢**：「ID_X 還活著嗎」/「哪裡有大錯」/「要改什麼」/「DS_X 還活著嗎」
- **明確 invocation**：`/id-review {file or theme}`（自動 dispatch 模式）
- **被 skill 強制呼叫**：industry-analyst Step 8.7（v2 報告由 id-meta `skill_version` 自動判別 → ID v2 mode；legacy ID 仍走 ID v1 mode）。industry-ds 已 deprecated，無獨立 Step 8.7。

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
| **C** — existing-report | 用戶說「我已經有 critic report 在 notes/site-internal/id/_critic_X.md，直接用它」 | 不 spawn，直接讀現有 report，跳到 Step 4 |

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

{若 ID v2 mode（id-meta skill_version v2.x）→ 在 prompt 內附下列 v2 章節對映 + V2 checklist：}
This is a v2.0 ID（敘事為骨表格為窗，§0-§9 九章）. Apply the 7 cornerstone items with this chapter mapping:
  - cornerstone fact / Non-Consensus → §7（not §12）
  - falsification metric table → §8（not §13）
  - catalyst timeline → §8（not §10.5）
  - ticker ranking / conviction tier → §9（not §11）
  - thesis box / PM Implication 綠卡 → §0
Additionally run the V2-1~V2-15 checklist (see id-review SKILL.md 「【ID v2 Mode 檢查清單】」):
表格比≥55%/表≤10 / 因果閉合 §1→§3·§4 / §5 供需裁決三選一 / §5 三視野×三情境 trigger 可量化 /
§8 catalyst 雙路徑 / §9 ticker 與 §3·§4 一致 / §5 cell 推導回溯 §3·§4 / §1 雙錨點 /
§4 三角對帳兩邊數字真實+回溯來源（差>20% 有解釋）/ §5 資本週期 ≥2 指標且方向與裁決一致 /
§7 每條分歧 priced-in 分位有來源.

Save report to /Users/ivanchang/financial-analysis-bot/notes/site-internal/id/_critic_{Theme}_{YYYYMMDD}.md.

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
- 用 Read 工具讀 `notes/site-internal/id/_critic_{Theme}_{date}.md`（user 指定路徑）
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
/Users/ivanchang/financial-analysis-bot/notes/site-internal/id/_critic_{Theme}_{date}.md.

Hunt for ADDITIONAL conclusion-changing errors Pass 1 might have missed
（章號為 legacy ID；ID v2 mode 用括號內 v2 對映）:
1. §0 thesis cornerstone numbers (key magnitudes) — v2: §0 thesis box
2. §6 player ranking facts (誰 > 誰 的支撐) — v2: §3 玩家矩陣 + §9 ticker 表
3. §14 portfolio actionable claims — v2: §0 PM Implication 綠卡
4. Cross-ID consistency with recent critic findings (check sister IDs)
5. §9.5 Kill scenarios — real steel-man or strawman? — v2: §7 steel-man 反方
6. §13 falsification metrics — any close to crossing? — v2: §8 證偽表
7. Under-rated tickers (中等 tier 但事實顯示應升 🔴) — v2: §9 ticker 表
{ID v2 mode 額外：抽查 V2-9 §4 三角對帳 / V2-10 §5 資本週期 / V2-11 §7 priced-in 是否裝飾性;v2.5+ 另跑 V2-12 機器欄同步 / V2-13 熱產業時鐘施壓（shortage×PhaseII）/ V2-14 kill 套套邏輯;v2.7+ 加 V2-15 手冊實答抽查。}

Save to /Users/ivanchang/financial-analysis-bot/notes/site-internal/id/_critic_pass2_{Theme}_{date}.md.

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

  完整 critic 報告（存 repo 內部 notes/site-internal/id/，不進 published 樹）：_critic_{Theme}_{date}.md（Pass 1）＋ _critic_pass2_{Theme}_{date}.md（Pass 2）
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

#### Step 6.5d — PM Implication §0.7 re-assessment（v1.2 加 — mandatory before commit）

**為什麼 mandatory**：critic patch 在 §11（conviction tier 變動）、§8（de-rating window 更新）、§13（新 falsification metric 加入）的任何修改，都直接影響 PM 的行動結論。若只更新這三個深層章節而不同步 §0.7，讀者看到的 PM Implication 是基於 patch 前狀態的 stale 結論 — audit trail 不完整。這是 6.5a thesis box sync 原則在 PM 層的延伸：寫稿者（analyst）與行動結論（PM 讀的 §0.7）必須同步。

**執行時機**：6.5a（thesis box sync）+ 6.5b（body sweep）+ 6.5c（conversational framework promotion）全部完成後，進 Step 7 commit 之前。

**Step 6.5d 完整流程**：

**D-0：§0.7 存在性檢查**

```
grep -n "§0.7" docs/id/ID_X.html
```
- 找到 → 進 D-1（re-assessment）
- 找不到 → 進 D-5（back-fill scenario）

**D-1：讀取現有 §0.7 + 逐 bullet 對照 Step 5 patch list**

讀取 `<section id="s0-7">` 整段，對照本次 id-review 所有 patch 條目：

| bullet | 需重新評估的 trigger |
|:---|:---|
| **thesis 方向**（保持 / 強化 / 降級）| 6.5a thesis box sync 改了 thesis 主軸？critic verdict = BROKEN 或 AT_RISK？|
| **個股 conviction tier 變化** | Step 5 patch 了 §11 的任何 🔴🟡🟢 tier？有 cross-ID sync 被更新？|
| **關鍵新監測點** | Step 5 patch 新增了 §13 F-N row？或 §10.5 catalyst 新增了條目？|
| **multiple / 估值 / 週期定位風險** | Step 5 patch 了 §8 de-rating window？或 §10 Phase 判斷改變？|
| **Entry 時機** | Step 5 patch 了任何 cross-ID entry posture 相關的 §11.5 / §12 framing？|

**D-2：更新 §0.7 各 bullet**

對每條需更新的 bullet：

1. thesis 方向 bullet：
   - critic verdict = INTACT → 「保持」；verdict = AT_RISK → 「降級，xxx 風險上升」；verdict = BROKEN → 「降級至保守，建議縮減曝險」
   - 若 6.5a 改了 thesis box 主軸 → 同步更新此行

2. conviction tier 變化 bullet：
   - 列出所有在本次 patch session 中 tier 有變動的 ticker（從 §11 改動倒推）
   - 格式：「TICKER 從 🔴 → 🟡（critic YYYY-MM-DD：{一行原因}）」
   - 若有 cross-ID sync → 加 `（cross-ID sync: ID_X）`

3. 關鍵新監測點 bullet：
   - 若 Step 5 patch 新增了 §13 row（e.g., F-8）→ 把新 metric + 閾值摘要加入此 bullet
   - 若 §10.5 catalyst 有新增 → 選 1-2 條最重要的加入

4. multiple/估值/週期風險 bullet：
   - 若 §8 新增了 de-rating window 判斷卡 → 更新此 bullet（引用 §8 新卡的結論）
   - 若 §10 Phase 有改動 → 更新 Phase 位置與下個轉換訊號

5. Entry 時機 bullet：
   - 若 thesis 降級 → 改「等 §13 falsification 條件排除後再 re-enter」
   - 若 cross-ID entry posture 改變（§11.5 或 §12 framing 更新）→ 同步說明

**D-3：更新 j-logic 行動 ①②③④**

若以上任一 bullet 有更新 → j-logic 行動也必須同步重新撰寫：
- 行動 ① 通常是「largest 🔴 ticker 的 sizing 指令」
- 行動 ② 通常是「at-risk 或 thesis 變化最大的 ticker 的應對」
- 行動 ③ 通常是「最重要的 new monitoring point 的觸發動作」
- 行動 ④ 通常是「entry timing 或 waiting 的具體條件」

**D-4：更新 conviction pill**

根據 patch 後的整體 thesis 健康度重新評定：
- `high`：critic verdict = INTACT AND §11 ≥ 2 個 🔴 维持
- `mid`：verdict = AT_RISK 或有 ≥ 1 條新 §9.5 kill scenario 加入
- `low`：verdict = BROKEN 或 thesis 主軸已需降級

**D-5：Back-fill scenario（§0.7 missing — 舊 ID 沒有此段）**

舊 ID（v1.0-v1.12 格式）若完全沒有 §0.7，本次 id-review 必須創建：
1. 讀取 §11 conviction tier、§8 現有 de-rating 判斷卡、§13 falsification 條目
2. 依 Step 7.5 template（`templates/html_template.md`）填入五 bullet + j-logic
3. 插入位置：**`<div class="insight">💡 3 條核心 insight</div>` 之後、`<h2>§1 產業定義與邊界</h2>` 之前**；若找不到 insight div，則插在 `<h2>§1` 之前
4. 在 commit message 中標注「§0.7 PM Implication backfilled（old ID did not have this section）」
5. 此 back-fill 算作本次 patch session 的一部分（不需另開 commit）

**6.5d 不需更新的反例**：
- Step 5 所有 patch 都是 §2/§3/§4 等數據層（技術演進、TAM 等），沒有碰 §11/§8/§13/§10 → 跳過 D-2/D-3/D-4，只確認 §0.7 存在
- 若用戶說「skip §0.7 update」→ 在 commit message 標注 `§0.7 re-assessment skipped per user request`，不省略記錄

**為什麼 6.5a + 6.5b + 6.5c + 6.5d 構成完整 sync 流程**：
- 6.5a：thesis box（讀者第一眼看的結論段）← 同步分析師結論
- 6.5b：body sections（§3/§5/§6 等 inline 重複處）← 同步數字一致性
- 6.5c：conversational frameworks（對話中 emerge 的 nuance）← 同步進 HTML
- **6.5d：§0.7 PM Implication（PM 直接讀的行動結論）← 同步投資行動**

四者缺一，ID 的修正都是不完整的 audit trail。

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
- notes/site-internal/id/_critic_{Theme}_{date}.md (Pass 1)
- notes/site-internal/id/_critic_pass2_{Theme}_{date}.md (Pass 2)

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
  - notes/site-internal/id/_critic_{Theme}_{date}.md
  - notes/site-internal/id/_critic_pass2_{Theme}_{date}.md（若有）

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

- v1.1（2026-05-02）：加 Step 2 input mode dispatch (A/B/C) + Step 0/C1-C6 consolidation phase + Step 6 banner 寫法明確化（append vs rewrite）。觸發來源：2026-05-02 ID_AIInferenceEconomics 手動 patch 暴露 3 個 gap + 1 個缺漏概念（banner 累積 / consolidation）
- v1.2（2026-05-03）：加 Step 6.5d PM Implication §0.7 re-assessment（5 bullet / j-logic 4 action / conviction pill sync + back-fill scenario 舊 ID）。觸發：ID_AIDataCenter v1.1 patch（commit f1c450b）— user 把臨時 PM block 升格為所有 ID 標準段落。
- v1.3（2026-05-12）：加 `--mode ds` 分支支援 industry-ds skill 產出的 DS 報告。新增「DS Mode 檢查清單」（DS-1 到 DS-6：表格比 / history-future causality / supply-demand 平衡 / §6 三情境 / §10 雙路徑 / §11 一致性）+「DS Mode Banner 格式」。觸發：industry-ds skill v1.0 上線，需要 mandatory critic gate。
- v1.4（2026-05-13）：DS-mode 檢查清單從 6 條擴為 9 條。DS-2 升級為「因果閉合在 §3 或 §5，不可延後到 §8」；新增 DS-7（source-tag 抽查 + T1 占比 + 黑名單）、DS-8（§6 base/bull/bear 推導抽查）、DS-9（§1 雙錨點 — 日期 + 量化）。觸發：industry-ds v1.1 上線，DS_AIAcceleratorDemand v1.0 暴露 5 個系統性弱點（無 footnote、無推導、§1 口語錨點、§11 forward-looking 閾值無時間標、§3 因果延後到 §8），需要對應 critic 鎖點。
- v1.4.1（2026-05-13）：移除 DS-7（source-tag 抽查）。觸發：industry-ds v1.2 把 inline `<span class="source-tag">` 移至每節末 `<aside class="ds-refs">`，pre-publish Gate 12 已更新為 aside 結構檢查 + T1 占比。DS-7 原本三個功能（URL 可達性抽查 / tier mis-tag 偵測 / ≥15 sources 底線）與 Gate 12 重疊度 ~80%，剩 20% 為低頻 redundancy；保留會誤 fail v1.2 報告（aside 內無 inline tag）。DS-8/DS-9 編號保留不動。
- v1.6（current，2026-07-08）：**校準教訓武器化＋機器欄時代同步**。V2 checklist 11→15 條：V2-12 機器欄↔內文同步（v2.5 五欄＋v2.6 priced_in，下游 QC-52/獵場鍵/monitor 直讀機器欄，矛盾比散文錯更危險）；V2-13 熱產業時鐘施壓（calibration_id_20260707：shortage×Phase II 唯一系統性失效格 7/25，critic 是時鐘樂觀偏誤的最後防線）；V2-14 kill 套套邏輯與口徑防呆（閾值抄自家 guidance＝永真/口徑不唯一/全表公司自報數）；V2-15 v2.7 情境手冊實答抽查（防 Gate 14 宣告式通過）。版本適用門檻：V2-12~14 需 ≥v2.5、V2-15 需 ≥v2.7，舊 v2.0-v2.4 報告跳過不失敗。
- v1.5（2026-06-11）：**加 v2 自動判別分支**，搭配 industry-analyst v2.0（合併 industry-ds、改 §0-§9 九章敘事骨架）。① Mode Dispatch 改三層判別：`DS_*` → ds mode；`ID_*` → 讀 id-meta `skill_version`，`v2.x` → ID v2 mode、`v1.x`/缺欄位 → ID v1 mode（legacy 現行流程不動）。② 新增「【ID v2 Mode 檢查清單】」= 現行 ID cornerstone 6 條 + thesis box sync（保留、remap 到 §0/§7/§8/§9）+ 從 DS 搬 8 條 remap 到 v2 章節（V2-1 文字比≥55%/表≤10 / V2-2 因果閉合 §3 或 §4 / V2-3 §5 供需裁決三選一 / V2-4 §5 三視野×三情境 trigger 可量化 / V2-5 §8 catalyst 雙路徑 / V2-6 §9 ticker 與 §3/§4 一致 / V2-7 §5 cell 推導抽查回溯 §3/§4 / V2-8 §1 雙錨點）+ 3 條 v2 新模組抽查（V2-9 §4 三角對帳 / V2-10 §5 資本週期證據 / V2-11 §7 priced-in 分位）。共 11 條 V2 + cornerstone 6 + thesis box sync。③ Step 8.7 spawn prompt 由 skill_version 自動 dispatch（v2.0 主稿已對齊）。DS-mode 8 條與現行 ID v1 checklist 文字不動（legacy 報告續用）。
- v1.3：跑熟後降為 mode (b) auto-patch 大錯
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

---

## 【ID v2 Mode 檢查清單】（v1.5 新增）

當 id-meta `skill_version` 以 `v2` 開頭（industry-analyst v2.0 產出的「敘事為骨表格為窗」§0-§9 九章報告），跑 Step 1-7 patch flow，但**檢查清單 = cornerstone 6 條 + thesis box sync（保留）+ 以下 V2-1~V2-15（15 條;V2-12~14 僅 skill_version ≥ v2.5、V2-15 僅 ≥ v2.7 適用，對舊 v2.0-v2.4 報告跳過不失敗）**。

v2 報告的章節與 legacy ID 對映（critic 與 patch 都用 v2 章號）：

| legacy ID 概念 | v2 章節 |
|:---|:---|
| §0 thesis box（一句 Thesis）| §0 決策摘要層 thesis box |
| §12 Non-Consensus（cornerstone fact + priced-in）| §7 Non-Consensus + Priced-in + Kill |
| §13 Falsification metric table | §8 證偽表 |
| §10.5 Catalyst Timeline | §8 Catalyst Timeline |
| §11 ticker ranking / conviction tier | §9 關聯個股 🔴🟡🟢 表 |
| §0.7 PM Implication 綠卡 | §0 PM Implication 綠卡 |

### 保留：cornerstone 6 條 + thesis box sync（remap 到 v2 章節）

industry-thesis-critic agent 的 7-item 冷讀（Item 1-6 cornerstone + Item 7 thesis box sync）**全部保留**，spawn 時在 prompt 內告知 v2 章節對映：

- **Item 1 鮮度**：讀 id-meta `sections_refreshed`（v2 沿用 technical / market / judgment 三桶，mapping：technical→§1-§2、market→§3-§5、judgment→§6-§9）。
- **Item 2 cornerstone fact 重驗**：cornerstone fact 從 **§7 Non-Consensus 三條分歧**萃取（不再是 §12）。「獨家 / 唯一 / 首家」類 claim 仍跑 ecosystem search。
- **Item 3 falsification 越線**：讀 **§8 證偽表**（不再是 §13）。
- **Item 4 catalyst 自 publish 後狀況**：讀 **§8 Catalyst Timeline**（不再是 §10.5）。
- **Item 5 / 6**：cross-ID 一致 + ticker tier 合理性，讀 **§9 ticker 表**。
- **Item 7 thesis box sync**：對映 **§0 thesis box + §0 PM Implication 綠卡**（Step 6.5a / 6.5d 流程不變，章號改 v2）。

> Step 6.5（thesis box sync / body sweep / framework promotion / §0.7 PM re-assessment）全部沿用，僅把 §11/§8/§13/§10/§0.7 章號替換為 v2 對映（§9/§8/§8/§5/§0 PM 綠卡）。grep body sweep 的「常見重複位置」改掃 v2 章節（§3 利潤池 / §5 三情境 / §9 ticker 表）。

### V2-1：表格比例 + 數量硬限制（原 DS-1 門檻改）

industry-analyst v2.0 是「敘事為骨表格為窗」，門檻**比 DS 寬**（DS 是 ≥80% 文字 / ≤4 表；v2 是 ≥55% 文字 / ≤10 表）：

| 項目 | Pass | Fail |
|:---|:---|:---|
| 文字字元比例 | ≥ 55% | < 55% |
| 表格數量 | ≤ 10 張 | > 10 張 |
| 單表行數 | 每張 ≤ 8 行（§9 例外 ≤16）| 任一非 §9 表 > 8 行 |

**檢查方式**（同 Pre-Publish Gate 6）：

```bash
python3 << 'PY'
import re
html = open("docs/id/ID_X.html").read()
clean = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)
tables = re.findall(r'<table[^>]*>.*?</table>', clean, flags=re.DOTALL)
text_total = len(re.sub(r'\s+','',re.sub(r'<[^>]+>','',clean)))
table_text = sum(len(re.sub(r'\s+','',re.sub(r'<[^>]+>','',t))) for t in tables)
print(f"tables: {len(tables)}, text ratio: {1-table_text/text_total:.1%}")
PY
```

**Fail 處置**：表格 > 10 張或文字 < 53% → 🔴。53-55% → 🟡（補敘述）。

### V2-2：§1 → §3 / §4 因果閉合（原 DS-2，remap 到 v2）

**Why**：v2 §1 提出的結構變數（某代際技術 / 護城河 / 製程獨家性）必須在 **§3（供給）或 §4（需求）**至少一段（≥50 字符）直接回應「該變數未來 3-5 年是否仍 binding」。v2.0 明文規定「不准推到判斷層（§7 Non-Consensus 不算閉合點）」。

**檢查方式**：
1. 人工讀 §1 提煉 2-3 個關鍵結構變數 / inflection。
2. 對每個變數，在 §3 + §4 grep 是否有顯式回應段（≥50 字符）。
3. 若答案只出現在 §5/§6/§7/§8/§9 → 仍 fail（破壞「歷史→未來」spine）。

**Fail 處置**：🔴（§5 推估完全脫離 §1，無 trace）/ 🟡（答案延後到 §7 等判斷層，要求前置到 §3 或 §4）/ 🟢（部分連結不顯式，補橋段）。

### V2-3：§5 供需裁決三選一明確（原 DS-3，remap 到 §5）

**Why**：v2 §5 開頭必須給「未來 X 年產業供需狀態是 **過剩 / 平衡 / 短缺**，因為 [具體原因]」，三選一不准騎牆。

**檢查方式**：在 §5 開頭尋找裁決句，確認出現過剩 / 平衡 / 短缺三選一（surplus / balance / shortage）。允許分時間段（「短期 X 中長期 Y」）但每段必須明確；禁「可能 X 也可能 Y」。

**Fail 處置**：🔴 — 缺明確裁決或騎牆 → 阻擋發布。

### V2-4：§5 三視野 × 三情境 + trigger 可量化（原 DS-4，remap 到 §5）

**檢查項**：
- 三視野：12M / 3Y / 5Y+
- 三情境：base / bull / bear
- Trigger 欄非空，且每個 trigger 是**可量化 metric**（禁「demand booms」「inference takes off」這類模糊詞；要像「NVDA inference run-rate ≥ $80B annualized」）。
- 表外有 ≥3 段敘述展開三視野邏輯。

**Fail 處置**：🔴（缺視野 / 三情境 / trigger 全模糊）/ 🟡（trigger 部分模糊或敘述太薄）。

### V2-5：§8 catalyst 雙路徑齊備（原 DS-5，remap 到 §8）

**Why**：§8 Catalyst Timeline 每個節點必須寫「若達成→ X」「若落空→ Y」雙路徑，否則退化成單純時間表，喪失 falsification 價值。

**檢查方式**：grep §8 catalyst 每個節點（`<time>` / 日期標記）後 30 字內是否含「若達成 / 若落空」「if hit / if miss」「達成 / 落空」字眼。

**Fail 處置**：🔴（全部單路徑）/ 🟡（部分節點單路徑）。

### V2-6：§9 ticker depth 與 §3 / §4 敘事一致（原 DS-6，remap 到 §9）

**Why**：§9 是 stock-analyst hook。若 §3 寫供給過剩、§9 把所有供應商標 🔴 beneficiary，邏輯不通。

**檢查方式**：
- 找 §9 標 beneficiary=true 的 🔴 ticker，確認 §3（供給）或 §4（需求）有敘述支持「為何受益」。
- 對 beneficiary=false 的 ticker，確認有敘述支持「為何受害」。

**Fail 處置**：🔴（系統性矛盾）/ 🟡（個別 ticker 缺對應）。

### V2-7：§4 / §5 推導抽查 — inputs 可回溯（原 DS-8，remap 到 v2）

**Why**：v2 §5 三視野×三情境 cell 與 §4 TAM 三情境必須附 input → calc → implication 推導；bull/bear 偏離 base 必須由「某 input 假設改變」推出，不准黑盒 ±20%。

**檢查方式**：
1. 從 §5 三情境表**隨機抽 base / bull / bear 各一格**（共 2 個 cell 起跳）。
2. 對每個抽到的 cell：
   - 表外緊鄰段落（同 horizon 敘述展開段）是否有「推導：」字串或等效推導行（「→」「換算」「計算」開頭短行）。
   - 推導行提到的 input 數字（如「hyperscaler capex $600B」「workload mix 35%」），是否能回溯到 **§3（供給）/ §4（需求）/ §2** 找到對應出處（不是憑空假設）。
   - bull / bear 偏離 base 是否由「某 input 假設改變」推出。

**Fail 處置**：🔴（§5 完全無推導行，所有 cell 黑盒）/ 🟡（部分 cell 有推導但 input 無法追到 §3/§4）/ 🟢（推導存在但不夠精確）。

### V2-8：§1 雙錨點（日期 + 量化）（原 DS-9，章號不變）

**Why**：v2 §1 每個 inflection 段必含具體日期（YYYY 或 YYYY-MM）+ 至少一個量化錨點，禁「過去幾年」「最近」這類模糊表述。

**檢查方式**：對 §1 每個 inflection 段正則檢查：

```python
import re
s1 = re.search(r'<h2[^>]*>§1[^<]*</h2>(.*?)(?=<h2|\Z)', html, re.DOTALL).group(1)
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', s1, re.DOTALL)
for i, p in enumerate(paragraphs):
    text = re.sub(r'<[^>]+>', '', p)
    has_date = bool(re.search(r'\b(19|20)\d{2}(-\d{2})?\b', text))
    has_number = bool(re.search(r'\d+\s*%|\$\s?\d+|\d+\s?(GW|TFLOPS|GB|MAU|B|M)|\d+x|\d+\s?倍', text))
    if not (has_date and has_number):
        print(f"§1 段 {i+1}: 缺 {'日期' if not has_date else ''} {'量化錨點' if not has_number else ''}")
```

**Fail 處置**：🔴（§1 全無日期錨點）/ 🟡（部分段有日期無量化或反之）/ 🟢（精度太低只到 decade）。

---

### V2 新模組抽查（v2 獨有 3 條，DS 沒有）

industry-analyst v2.0 新增 7 個分析模組，其中三個對 thesis 結論最 load-bearing — critic 必須抽查它們是「真有做」還是「裝飾」。

### V2-9：§4 需求三角對帳（QC-M2 對應）

**Why**：v2 §4 要求 top-down TAM 與 bottom-up（下游客戶 capex/採購 guidance 加總 vs 上游廠商營收 consensus 加總）對帳；**兩邊差 >20% 必須解釋缺口在哪**。critic 抽查這對帳是否真實存在。

**檢查方式**：
1. 在 §4 找 top-down TAM 數字 + bottom-up 加總數字（兩邊都要有具體 $ 數）。
2. **兩邊數字真實存在且可回溯來源**（節末 aside 有對應條目，不是憑空寫一個 bottom-up 數字湊對帳）。
3. 若兩邊差 >20% → 確認章內有解釋缺口（重複計算 / 樂觀滲透率 / 口徑不同）+ 寫明採信哪邊。

**Fail 處置**：🔴（只有 top-down，完全沒 bottom-up 對帳 / 兩邊差 >20% 但無解釋）/ 🟡（對帳存在但某一邊數字無來源）/ 🟢（對帳完整但結論採信邏輯薄弱）。

### V2-10：§5 資本週期證據真實引用（QC-M1 對應）

**Why**：v2 §5 供需裁決必須引資本週期三指標（① capex/折舊比趨勢、② ROIC vs WACC、③ 新產能 lead time）中**至少 2 項**作量化依據。critic 抽查是否「真引用」且「非裝飾性」。

**檢查方式**：
1. 在 §5 裁決段找資本週期指標，確認**至少 2 項**有具體數字（不只提名詞）。
2. **非裝飾性檢查**：裁決方向必須與指標方向**邏輯一致** — e.g. 裁決「未來過剩」但 capex/折舊比下降、ROIC < WACC、lead time 縮短（三者都指向產能收縮）→ 矛盾，指標是裝飾。反之裁決「短缺」配 lead time 拉長 + ROIC > WACC + capex/折舊比攀升 → 一致。

**Fail 處置**：🔴（裁決只靠敘事，0-1 項指標 / 指標方向與裁決方向矛盾）/ 🟡（湊到 2 項但其一無數字或來源）/ 🟢（指標齊但與裁決連結不夠顯式）。

### V2-11：§7 priced-in 分位有來源（QC-M3 對應）

**Why**：v2 §7 每條 non-consensus 分歧必須附 priced-in 檢驗 — ① sector 估值歷史分位（現在 EV/Sales 或 Fwd P/E 在過去兩輪 cycle band 的 percentile）+ ② 現價隱含成長假設。**分歧對但已 priced → 標「不可操作」**。critic 抽查每條分歧的 priced-in 是否齊備、分位數字是否有來源。

**檢查方式**：
1. 對 §7 每條分歧（通常 3 條），確認旁邊有 priced-in 段。
2. 每個 priced-in 段含：① 估值分位（具體 percentile 或 band 位置）+ ② 現價隱含假設。
3. **分位數字有來源**：節末 aside 有對應 valuation band 來源（券商 T3-A valuation band 圖、或自算但註明資料窗口）；隱含成長假設有推導行。
4. 若某分歧「對但已被 price」→ 確認章內標明「不可操作」。

**Fail 處置**：🔴（≥1 條分歧完全沒 priced-in / 分位數字憑空無來源）/ 🟡（priced-in 存在但隱含假設無推導 / 部分分歧缺）/ 🟢（齊備但「可操作性」結論未明示）。

### V2-12：機器欄 ↔ 內文同步（v1.6 新增；skill_version ≥ v2.5 適用）

**Why**：v2.5 起 id-meta 有五個機器裁決欄（`sd_verdict`/`clock_phase`/`conviction`/`kill_metrics`/`demand_5y_multiple`）、v2.6 加 `priced_in`——下游（stock-analyst QC-52 對帳、獵場篩選鍵、position-thesis-monitor）**直接讀機器欄不讀散文**。機器欄與內文矛盾＝下游拿到一份與報告本體不同的裁決，比散文錯更危險。

**檢查方式**：id-meta 六欄逐項對內文——`sd_verdict` ↔ §5 供需裁決、`clock_phase` ↔ §0 6-box 投資時鐘、`conviction` ↔ §0 PM 綠卡 pill、`kill_metrics[]` ↔ §8 證偽表（metric 名＋bear 閾值逐條）、`priced_in` ↔ §7 各分歧 priced-in 檢驗的整體讀數、`demand_5y_multiple` ↔ §4 base 5Y TAM ÷ 現 TAM。
**Fail 處置**：🔴（任一欄與內文方向矛盾，如散文寫「多數利多已 priced」而機器欄 `priced_in: low`）/ 🟡（數字級不一致或口徑漂移）/ 🟢（一致）。

### V2-13：熱產業時鐘施壓（v1.6 新增；校準教訓武器化）

**Why**：ID 層裁決校準（knowledge/calibration_id_20260707.md）：**shortage × Phase II 是唯一系統性失效格**（n=25、勝率 7/25、清一色 AI 硬體）——時鐘對「正熱的產業」系統性樂觀，對走過半場的產業（III/IV 21/21 全勝）標得準。critic 是這個偏誤的最後防線。

**檢查方式**：`sd_verdict = shortage ∧ clock_phase = II` 的報告，強制三問——① Phase II 判定依據是產業基本面週期證據（capex/庫存/訂單）還是被順風敘事拉著走？② 該族群 26 週漲幅/擁擠度證據（crowding monitor、位置錶）是否指向更晚的相位？③ `priced_in` 是否誠實——短缺＋超漲族群標 `low` 是紅旗，須逐分歧核對。
**Fail 處置**：🔴（Phase II 無基本面週期證據支撐、或 priced_in 與族群漲幅明顯矛盾）/ 🟡（有證據但未處理擁擠度反證）/ 🟢（三問皆有答）。

### V2-14：kill 套套邏輯與口徑防呆（v1.6 新增）

**Why**：證偽表最常見的隱形失效——閾值抄公司自發 guidance（永真）、口徑不唯一（不可裁決）、全部指標皆公司自報數（可被管理層美化）。這三項本是寫作端手冊條目（judgment-playbook #2/#17），critic 端對稱抽查。

**檢查方式**：對 id-meta `kill_metrics[]` 每條——① 閾值是否與公司自發 guidance 同源（是 → 應為 meet/miss 監測而非獨立門檻）；② 口徑是否唯一可裁決（範圍、含不含哪些段）；③ 整表至少一條為市場撮合價/實測價（租價、現貨價、depletions）而非公司自報。
**Fail 處置**：🔴（≥1 條套套邏輯 / 全表皆公司自報數）/ 🟡（口徑歧義 ≥1 條）/ 🟢（過）。

### V2-15：情境手冊實答抽查（v1.6 新增；skill_version ≥ v2.7 適用）

**Why**：v2.7 Gate 14 要求命中情境的 judgment-playbook 條目逐條實答——寫作端 gate 只能自證，critic 端抽查防「宣告已答」。

**檢查方式**：讀 `industry-analyst/references/judgment-playbook.md` 觸發索引，判斷本報告命中哪些情境（如單價下跌 → P×Q 拆解；持續讓利 → 四判準），抽 2 條驗證章節內有**實際答案**（具體數字/判定，非泛泛帶過）。
**Fail 處置**：🔴（命中明顯情境但完全未答，如記憶體 ID 無 P×Q 拆解）/ 🟡（答了但無數字支撐）/ 🟢（實答）。

---

## 【ID v2 Mode Banner 格式】（v1.5 新增）

v2 報告 banner 沿用**現行 ID banner 格式**（§0 頂部紅底 block，見 Step 6「Banner 標準格式」），不採 DS 的 `<details>` 摺疊式 — 因為 v2 是 id-meta + §0 決策層結構，與 legacy ID 同源。累積上限（≥5 patch / >2000 字 / id_version ≥v1.5）與 consolidation flow（Step 0 → C1-C6）完全沿用。critic report 路徑 `notes/site-internal/id/_critic_{Theme}_{YYYYMMDD}.md`（與 legacy ID 同目錄）。validator 用 `scripts/validate_id_meta.py`。

---

## 【DS Mode 檢查清單】（v1.3 新增）

當 `--mode ds`，跑 Step 1-7 patch flow 但 **檢查清單改用以下 6 條**（取代 ID 模式的 §12/§13/cornerstone/thesis-box 檢查）。

DS 沒有 §12 Non-Consensus（DS 有 §8 Non-Consensus 但敘述形式不是 tag 體系）、沒有 §13 Falsification metric table、沒有 §10.5 catalyst table（DS 的 catalyst 是 §10 敘述形式），所以原本 ID critic 的核心鎖點全部不適用。DS 改驗以下「敘述結構正確性」鎖點。

### DS-1：表格比例硬限制

| 項目 | Pass | Fail |
|:---|:---|:---|
| 表格數量 | ≤ 4 張 | > 4 張 |
| 單表行數 | 每張 ≤ 8 行（不含表頭）| 任一張 > 8 行 |
| 文字字元比例 | ≥ 80% | < 80% |

**檢查方式**：
```bash
python3 << 'PY'
import re
html = open("docs/ds/DS_X.html").read()
clean = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)
tables = re.findall(r'<table[^>]*>.*?</table>', clean, flags=re.DOTALL)
text_total = len(re.sub(r'\s+','',re.sub(r'<[^>]+>','',clean)))
table_text = sum(len(re.sub(r'\s+','',re.sub(r'<[^>]+>','',t))) for t in tables)
print(f"tables: {len(tables)}, ratio: {1-table_text/text_total:.1%}")
PY
```

**Fail 處置**：🔴 CHANGES_CONCLUSION。表格 > 4 張或文字 < 78% → 大錯。78-80% → 🟡 PARTIAL（補敘述）。

### DS-2：§1 → §3 / §5 / §6 因果鏈（v1.4 升級：必須閉合在 §3 或 §5）

**Why**：DS 核心是因果敘事。§1 歷史寫完後，必須在 §3（未來供給）或 §5（未來需求）中有顯式回應 — 「歷史告訴我們 X，所以未來 Y」。**v1.4 升級**：v1.3 critic 只抓「§1 是否被 §3/§5/§6 引用」，但 AI Accelerator DS v1.0 暴露漏網之魚 — CUDA 護城河答案延後到 §8 Non-Consensus（不是 §3 或 §5），破壞了「歷史 → 未來」因果 spine。v1.4 改為「§1 inflection 必須在 §3 或 §5 找到對應回答段（≥ 50 字符）；若答案出現在 §6/§7/§8/§9 → 仍 fail」。

**檢查方式**：
1. 人工讀 §1 提煉 2-3 個關鍵 inflection point（歷史事件 / 技術代際 / 護城河形成節點）
2. 對每個 inflection，在 §3（未來供給）+ §5（未來需求）中 grep 是否有顯式回應段（≥ 50 字符）
3. 若 §3/§5 均無回應、但 §6/§7/§8/§9 有回答 → 標 PARTIAL_ERROR（破壞 spine 但非完全脫節）

**範例 fail**：§1 寫「2012 年 CUDA 把 NVDA 變平台公司」→ §3 / §5 完全沒回應「CUDA 在 inference 階段是否仍是 binding moat」，卻把答案放在 §8 Non-Consensus（「市場認為 CUDA 不可動搖、我們認為 ROCm 已縮短差距」）→ 🟡 PARTIAL_ERROR：要求把 §8 內容前置一部分到 §3。

**Fail 處置**：
- 🔴 CHANGES_CONCLUSION：§6 推估完全脫離 §1 歷史（無任何 trace）
- 🟡 PARTIAL_ERROR（v1.4 新）：§1 → §3/§5 不閉合但 §8/§9 有回應 → 要求把答案前置到 §3 或 §5
- 🟢 COSMETIC：部分連結但不顯式 → 補敘述橋段

### DS-3：§3 + §5 → 供需平衡明確結論

**Why**：DS 最大價值 — 把供需兩端合在一起、給出明確結論。模稜兩可 → §6 推估缺基礎。

**檢查方式**：在 §5 結尾或 §6 開頭尋找 `.ds-bridge` 段落（或等價 prose 段落），確認出現以下三選一：
- 「過剩 / surplus / oversupply」
- 「平衡 / balance」
- 「短缺 / shortage / undersupply」

允許分時間段（「短期 X 中長期 Y」），但每段必須明確。

**Fail 處置**：🔴 — 缺結論 → 阻擋發布。

### DS-4：§6 三 horizon × 三情境 + trigger 完整

**檢查項**：
- 表格三列：12M / 3Y / 5Y+
- 表格三欄：base / bull / bear
- Trigger 欄非空（每 horizon 一個可量化 metric）
- 表外有 ≥ 3 段敘述展開三個 horizon 的邏輯

**Fail 處置**：🔴（缺 horizon 或 trigger）/ 🟡（敘述太薄）

### DS-5：§10 Catalyst 雙路徑

**Why**：catalyst 不只是列日期。每個節點必須寫「若達成 → X」「若落空 → Y」雙路徑，否則 catalyst 變單純時間表，喪失 falsification 價值。

**檢查方式**：grep `<time>` 或 `class="ds-time"` 標記後 30 字內是否含「若達成 / 若落空」「if hit / if miss」「達成 / 落空」字眼。

**Fail 處置**：🟡（部分節點有單路徑）/ 🔴（全部單路徑）

### DS-6：§11 ticker 與 §3 / §5 敘述一致

**Why**：§11 是 stock-analyst hook。若 §3 寫供給過剩、§11 把所有供應商標 🔴 beneficiary，邏輯不通。

**檢查方式**：
- 找 §11 標 🔴 beneficiary=true 的 ticker
- 對每個這樣的 ticker，確認 §3（未來供給）或 §5（未來需求）有敘述支持「為何此 ticker 受益」
- 同理對 🔴 beneficiary=false 的 ticker，確認有敘述支持「為何受害」

**Fail 處置**：🟡（個別 ticker 缺對應）/ 🔴（系統性矛盾）

### DS-7：已移除（v1.4.1，2026-05-13）

原 v1.4 source-tag 抽查 + T1 占比 + 黑名單檢查。industry-ds v1.2 把 inline source-tag 改為 §末 `<aside class="ds-refs">`，pre-publish Gate 12 已更新為 aside 結構檢查 + T1 占比，DS-7 與 Gate 12 重疊度 ~80%，剩 20% 為 redundancy → 移除。編號保留 gap，不 renumber DS-8/DS-9（git 歷史看得出 DS-7 曾存在）。

### DS-8（v1.4 新）：§6 推導可追溯性抽查

**Why**：DS v1.0 §5/§6 bull/bear case 給絕對數字但不寫推導 — PM 無法獨立判斷 bull case +20% 來自哪個 input 變動。v1.1 從 stock-analyst v12.2 移植「推導可追溯性原則」 — §6 三 case 必須附 input → calc → implication 推導。

**檢查方式**：
1. 從 §6 表格中**隨機抽 base / bull / bear 各一格**
2. 對每個抽到的 cell：
   - 表外緊鄰段落（同 horizon 的敘述展開段）是否有「推導：」字串或等效推導行（「→」「換算」「計算」開頭的短行）
   - 推導行中提到的 input 數字（如「hyperscaler capex $600B」「workload mix 35%」「accelerator ratio 1.33」），是否能在 §2/§3/§4/§5 找到對應出處（不是憑空假設）
   - bull / bear 偏離 base 的程度是否由「某個 input 假設改變」推出（不是無理由的 ±20%）

**範例 fail**：
- 表格寫「base case 2028 NVDA share 60-65%」、「bull 70-75%」、「bear 45-50%」
- 表外段落只寫「base 假設 ASIC 滲透率穩定、bull 假設 CUDA inference 護城河持續、bear 假設 ASIC 加速」
- 但沒寫「ASIC 滲透率 30% → NVDA 62% / 20% → NVDA 72% / 45% → NVDA 47%」這種具體映射
- → 🟡 PARTIAL_ERROR：要求把每個 case 對應的 input 數字寫出來

**Fail 處置**：
- 🔴：§6 完全沒有推導行（所有 cell 都是黑盒）
- 🟡：部分 cell 有推導但 input 數字無法追到 §2-§5
- 🟢：推導存在但不夠精確

### DS-9（v1.4 新）：§1 雙錨點（日期 + 量化）

**Why**：DS v1.0 §1 只要求「2-3 個歷史轉折點」但沒規定錨點精度。AI Accelerator DS v1.0 出現「ChatGPT-Hopper 配給」這種口語式錨點 — 沒有 H100 launch 具體日期（2023-03）、沒有 ChatGPT MAU 100M 達成時間（2023-01-31）、沒有當時的 lead time 數字。v1.1 強制每個 inflection 段必含具體日期 + 量化錨點。

**檢查方式**：對 §1 每個 inflection point 段落（通常 2-4 段）正則檢查：
```python
import re
# 抓 §1 全文
s1 = re.search(r'<h2[^>]*>§1[^<]*</h2>(.*?)(?=<h2|\Z)', html, re.DOTALL).group(1)
# 拆段落
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', s1, re.DOTALL)
for i, p in enumerate(paragraphs):
    text = re.sub(r'<[^>]+>', '', p)
    has_date = bool(re.search(r'\b(19|20)\d{2}(-\d{2})?\b', text))
    has_number = bool(re.search(r'\d+\s*%|\$\s?\d+|\d+\s?(GW|TFLOPS|GB|MAU|B|M)|\d+x|\d+\s?倍', text))
    if not (has_date and has_number):
        print(f"§1 段 {i+1}: 缺 {'日期' if not has_date else ''} {'量化錨點' if not has_number else ''}")
```

**範例 fail**：
- ❌「過去幾年 AI 加速器需求快速成長」← 無日期、無量化
- ❌「ChatGPT 興起後，H100 變稀缺品」← 有事件但無日期 + 無量化
- ✅「**2022-11-30 ChatGPT 發布**，兩個月內 **MAU 衝破 1 億**；**2023-03 H100 launch** 時 hyperscaler 已開始大量採購；**2023-Q3 NVDA DC 營收同比 +279%**，第一次出現 **12+ 個月 lead time 配給**」

**Fail 處置**：
- 🔴：§1 完全無日期錨點（所有段都是「過去」「最近」這類模糊表述）
- 🟡：部分段有日期但無量化錨點（或反之）
- 🟢：有日期但精度太低（只到 decade）

---

## 【DS Mode Banner 格式】（v1.3 新增，v1.3.1 微調）

DS 模式下 banner 寫到 **§0 末尾**（不放 thesis box 之上，避免把 thesis 推到下方），且用 `<details>` 預設摺疊，讓讀者先看 thesis 不被 editorial note 干擾。格式：

```html
<details style="margin:18px 0 6px;font-size:12.5px;color:#6B7280">
  <summary style="cursor:pointer;color:#7C3AED;font-weight:600;list-style:none">📌 編輯記錄（v{N} critic patch）— 點開展開</summary>
  <div style="margin-top:8px;padding:10px 14px;background:#FEF9C3;border-left:3px solid #F59E0B;border-radius:3px;color:#78350F;line-height:1.65">
    <strong>v{N}（{YYYY-MM-DD}）</strong>：🔴 / 🟡 / 🟢 — {patch summary} → 影響章節：§{X}。critic report：_critic_{Theme}_{YYYYMMDD}.md（存 repo 內部 notes/site-internal/id/，非 published）
  </div>
</details>
```

**位置規則**：在 §0 內，必填順序為 thesis box → ds-crosslink callout（若有 related_ids） → intro paragraph → 編輯記錄 details（若有 patch）。Banner 一律 collapse-by-default。

**累積上限與 ID 相同**：≥ 5 patch / > 2000 字 / ds_version ≥ v1.5 → consolidation flow（每個 patch 進到對應章節，§0 details 內留單行 "v{N} consolidated" marker）。

**路徑**：DS critic report 路徑 `notes/site-internal/ds/_critic_{Theme}_{YYYYMMDD}.md`（不放 `notes/site-internal/id/_critic_*`）。

DS 模式不檢查 `<script id="id-meta">` 而是 `<script id="ds-meta">`；validator 用 `scripts/validate_ds_meta.py`。
