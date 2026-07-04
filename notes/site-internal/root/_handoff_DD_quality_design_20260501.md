# Handoff Brief — DD/ID 品質下一階段設計

**From**: 2026-05-01 session（Opus 4.7, 1M context, ~6h 工作）
**To**: 新 window 動手實作

---

## 📍 我們已建的 infrastructure（不要重建）

```
.claude/skills/
  industry-analyst/SKILL.md      v1.9 含 Step 8.7 mandatory critic gate
  stock-analyst/SKILL.md         v12.0
  portfolio-manager/SKILL.md
  id-review/SKILL.md             v1.0 — 修現有 ID + 被 industry-analyst 呼叫

~/.claude/agents/
  industry-thesis-critic.md      v1.2 — 含 CONCLUSION_IMPACT 維度（🔴/🟡/🟢）

scripts/
  validate_id_meta.py            v1.9 加 quality_tier enum (Q0/Q1/Q2)
  validate_source_blacklist.py   M1 黑名單防 SEO 內容農場
  validate_dd_meta.py

docs/id/
  _source_tier_lists.md          黑/白名單集中管理
  _critic_*.md                   既有 critic 報告（HBM4 / AdvancedPackaging / InferenceEcon / GLP1）
  _redteam_*.md                  Pilot fact-checker 紅隊報告（HBM4 / InferenceEcon）
```

CLAUDE.md 已加觸發提示：「討論加倉/減倉/新進 theme 時必先 spawn industry-thesis-critic」。

---

## 🎯 下一階段目標

讓 industry-analyst + stock-analyst 的產出**「基於事實 + 多情境推論未來 + 不能大錯」**。

現有 critic + Step 8.7 解決了「事實對 + 寫稿後查」，但**抓不到的大錯類別**還有：

1. **Spurious specificity**（「78.3% 市佔」實際是 ~75-80% 區間）
2. **共識假裝非共識**（§12 列共識當 thesis）
3. **單一情境被當必然**（「Rubin Ultra 2027 量產」當既定，沒列「if 延後則 X」）
4. **Framing error**（一開始框架錯，所有後續 §12/§13 圍繞錯框架）

---

## 💡 設計提案（待新 window 決定走哪版）

### Option A — 原版（5-class + 精準機率）

```
🟢 [F: source]                     事實（T1/T2 + 日期 + 確切值）
🟡 [I: A→B]                        推論（A 事實 + B 邏輯）
🔵 [X: base 60%/bull 25%/bear 15%] 情境預測（三情境並列 + 機率 sum 1）
⚪ [A: ...]                        假設（顯式列）
⚫ [O: ...]                        意見（無 source 但 flag）
```

### Option B — 精煉版（4-class + 詞彙級機率，我推這個）

```
🟢 [F:]                            事實
🟡 [I:]                            推論（併入意見）
🔵 [X: base 很可能 / bull 可能 / bear 不太可能] 情境（詞彙級）
⚪ [A:]                            假設
```

理由：
- 拿掉 [O:] — 避免「意見」變 hand-wave 借口；強制併入 [I:]
- 機率用詞彙級（很可能 >60% / 可能 30-60% / 不太可能 <30%）— 避免「60%」這種精準數字本身是幻覺

### 兩版共通要做的

1. **強制多情境**：§12 / §13 改成必有 base/bull/bear 三情境（不只 non-consensus 單軸）
2. **Spurious specificity 禁令**（QC rule）：
   - 市佔 → ~70% 或 60-65%，不允許 62.7%
   - 預估 → 2027 H2 或 2027 Q3-Q4，不允許 2027-09-15
   - 例外：T1 source 直接公告的精確數字保留
3. **Skill flywheel**：critic 抓到的大錯自動寫進 SKILL.md Gotchas（長期工程）

---

## 🚧 約束（don't do）

- ❌ **不 retrofit 既有 80 份 ID**（每份 2-3h × 80 = 200h+，不可承受）
- ❌ **不開後門**（[O:] 意見類）
- ❌ **不用精準機率數字**（spurious specificity 高階版）
- ❌ **暫不上 Stop hook**（先用 SKILL.md mandatory call，跑 1-2 週看漏跑率 > 10% 再升級）

---

## 🎬 建議起手式

```
Step 1（30 min）：定 4-class taxonomy 細節（precise spec）
Step 2（30 min）：寫 Spurious Specificity QC rule
Step 3（1h）：升級 id-review skill v1.1 包含新規則
Step 4（1h）：升級 industry-analyst skill 同步要求
Step 5（30 min）：建一份 sample ID 用新格式（test 可讀性）
Step 6（觀察期）：跑 3 份新 ID 看漏跑率 / 可讀性 / token 成本
Step 7（決策）：是否值得升級 stock-analyst skill 用同格式
```

---

## ⚠ 待解決的問題

1. **Option A vs B 二選一**（4 類 vs 5 類，精準機率 vs 詞彙級）
2. **Reader 端可讀性**：高密度 claim 標記是否反而難讀？需做一份 sample 比較
3. **Q0 Flagship 強度 vs Q1/Q2**：要不要 tier-aware（Q0 強制 4-class / Q1 部分要求 / Q2 不要求）
4. **新格式如何跟舊 ID 共存**：純文字 banner 還是強制升 v1.x

---

## 📂 重要檔案閱讀順序（新 window 開工前看）

1. `docs/_handoff_DD_quality_design_20260501.md`（本文件）
2. `.claude/skills/id-review/SKILL.md`（最新 skill，已含 mode (a) user-in-the-loop）
3. `~/.claude/agents/industry-thesis-critic.md`（critic v1.2 含 CONCLUSION_IMPACT）
4. `.claude/skills/industry-analyst/SKILL.md`（Step 8.7 = mandatory critic gate）
5. `docs/id/_critic_AIInferenceEconomics_20260501.md`（critic Pass 1 sample 295 行）
6. `docs/id/_critic_pass2_AIInferenceEconomics_20260501.md`（critic Pass 2 大錯掃描 sample）
7. `docs/id/_pilot_results_20260501.md`（pilot 工作結束報告，含 4 條 SIGNIFICANTLY_WRONG）

---

## 🧠 從 2026-05-01 session 學到的關鍵教訓

1. **Auto-verify ≠ DD 品質**：機械正確性不等於推理品質；critic 機制更有效
2. **跨模型冷讀有效**：Sonnet 紅隊在 18 min 抓到 Opus 寫稿者的 thesis-level 大錯（Rubin Ultra 4-tile / Samsung yield 80% 已破關 etc.）
3. **大錯 vs cosmetic 必須分**：critic 報告每條 finding 標 🔴 CHANGES_CONCLUSION / 🟡 PARTIAL / 🟢 COSMETIC
4. **真正改變結論的錯通常 1-4 條**：兩份 pilot ID 各找到 1-4 條大錯 + 多條 cosmetic
5. **Pilot 經驗：FET 三層標記不夠**：Fact / Estimate / Thesis 三類抓不到「情境預測」（X 類）
6. **80 份 retrofit 是陷阱**：成本不可承受，新格式只應用在新 ID + 大改 ID

---

## 🚀 給新 window 的開場白（複製貼上即可）

> 我要繼續 2026-05-01 session 的工作。先讀 `docs/_handoff_DD_quality_design_20260501.md` 拿到 context。
> 
> 主要決策：選 Option A 還 Option B（4 類 vs 5 類 claim taxonomy）？
> 
> 決定後動手實作 Tier-1（claim 標記 + spurious specificity 禁令 + 多情境強制），不 retrofit 80 份既有 ID。
> 
> 動之前先讀那份 brief 才能確認 context。
