# DS Critic Report — DS_AIASICDesignService_20260514.html
**Mode**: --mode ds (industry-ds v1.2, id-review v1.4.1)
**Date**: 2026-05-14
**Quality tier**: Q0 (Flagship)
**Overall verdict**: AT_RISK (1 🔴, 2 🟡, 2 🟢)

---

## Executive Summary

The DS is structurally sound — all 11 chapters present, ds-meta valid, related_ids exist, ds-bridge with explicit 3-phase supply-demand conclusion, §6 3×3 table with quantifiable triggers, §1 dual-anchor anchors comprehensive, §3 causal closure explicitly labeled. One hard 🔴 per the spec's literal rule (DS-1: §11 table 11 rows > 8 limit), two 🟡 requiring interactive patch, two 🟢 cosmetic. The 🔴 is structural but arguably a spec edge case for the required ticker registry.

---

## 🔴 CHANGES_CONCLUSION (1 條)

### 🔴-1 DS-1 違規：§11 表 11.1 有 11 data rows，超出每張 ≤ 8 行硬限制

**位置**: Line ~510–525, `<table class="ds-tickers">`

**發現**:
- DS spec 硬規則："單表行數 | 每張 ≤ 8 行（不含表頭）| 任一張 > 8 行" → FAIL → 🔴
- 表 11.1 有 11 data rows（AVGO / MRVL / 3661.TW / 2454.TW / 3443.TW / NVDA / GOOGL / AMZN / MSFT / META / AAPL）
- 其他三張表均合規：表 2.1 = 7 rows、表 5.1 = 3 rows、表 6.1 = 3 rows
- 文字比例 90.4%（合規，≥80%）、表格數量 4 張（合規，≤4 張）

**為何標 🔴 而非豁免**:
  按 DS spec 字面規則，任一張 > 8 行即觸發 🔴 CHANGES_CONCLUSION，無例外條款。
  §11 是 stock-analyst hook 的 required section，包含 11 家公司（5 design service providers + 6 hyperscaler/LLM lab customers），原則上不能任意刪減，但可以拆分。

**修正建議 — 拆成兩張表**:

把表 11.1 拆成「11a 設計服務供應端（5 家）」+「11b 需求端 hyperscaler / LLM lab（6 家）」，各表 ≤ 8 rows：

```html
<!-- 表 11a：設計服務供應端（5 家） -->
<table class="ds-tickers">
<caption>表 11a：AI ASIC 設計服務供應端（5 家）... </caption>
<thead>...</thead>
<tbody>
  <!-- AVGO, MRVL, 3661.TW, 2454.TW, 3443.TW — 5 rows -->
</tbody>
</table>

<!-- 表 11b：需求端 hyperscaler / LLM lab（6 家） -->
<table class="ds-tickers">
<caption>表 11b：AI ASIC 需求端客戶（6 家）... </caption>
<thead>...</thead>
<tbody>
  <!-- NVDA, GOOGL, AMZN, MSFT, META, AAPL — 6 rows -->
</tbody>
</table>
```

注意：table count 從 4 張升到 5 張，超出「≤ 4 張」的另一個 DS-1 限制。**因此建議同時把表 2.1（7 rows）改為 prose list（因為 §2 已有大量 prose 敘述，表 2.1 的 share/GM 數字可以移進文中）**，把表格數量從 5 張降回 4 張。

**另一個替代方案**（若 user 偏好保留表格形式）: 把表 11.1 濃縮至最關鍵的 8 家，把 AAPL（邊緣客戶 ~5%）和 AMZN 或 MSFT 的其中一家移入 §11 prose，僅保留 8 行。

**Portfolio implication**: 修正後分析結論不變（AVBO 峰值、Alchip 跳級、MediaTek step function），但格式合規後 stock-analyst hook 可以更清晰讀取。

---

## 🟡 PARTIAL_ERROR (2 條)

### 🟡-1 DS-8：§6 中期（3Y）/ 短期（12M bear）推導 bull/bear 無具體 input→output 映射

**位置**: Line ~360-375（表 6.1 短期 bear cell）、Line ~375-376（中期 §6 derive 段）

**發現**:
DS-8 spec 要求「bull / bear 偏離 base 的程度是否由『某個 input 假設改變』推出（不是無理由的 ±20%）」。

逐一抽查：
1. **短期 12M base derive** ✅：明確計算 AVGO AI rev $42B × 50% = $21B + 各玩家加總 = $24B（input 可追）
2. **短期 12M bull** 🟡：「AVGO $50B AI rev + Alchip Trainium 3 yield 超預期 + MediaTek 加速 → $30B+」——有 input assumption change（AVGO 從 $42B 升至 $50B），但沒有 explicit calc（$50B × 50% + $1.6B + $2.5B = ~$30.1B，近似推出但未寫出）
3. **短期 12M bear** 🟡：「OpenAI 融資繼續卡 $18B + Trainium 3 yield 問題 + AVGO 1-2 個 XPU 客戶延後 → $16-19B」——沒有具體 calc，無法從輸入假設推出 $16-19B range
4. **中期 3Y bull** 🟡：「Google TPU 8i unit 兌現 + MTIA 二供化 + 第 3-4 個 merchant LLM lab 加入 → $75B+」——relative to base $55B, +$20B (+36%) 但無具體推導
5. **中期 3Y bear** 🟡：「二供化激進但整體 TAM 增速慢 + AVGO GM 顯著壓縮 → $35B」——無具體 input→output calc
6. **長期 5Y+ base** ✅：$2029 $55B × 2年 24% CAGR = $85B（traceable）
7. **長期 5Y+ bull** 🟡：「NVDA 推論 share 跌至 18% + merchant LLM lab 全面投入 + CAGR 維持 30%+ → $115B」——2029 base $55B × 1.30^2 = $93B ≠ $115B，差額 $22B 未說明來源
8. **長期 5Y+ bear** ✅：「2029 bear $35B × 1.32^2 ≈ $61B ≈ $62B」——logic traceable

**修正建議** — 在現有 §6 derive 段中，補充 bull/bear 的具體映射行：

_短期 bull case 補充（插入 `→ $30B+` 之前）_:
```
（推導：AVGO $50B × 50% = $25B + Alchip $1.6B + MediaTek $2.5B + MRVL $2B + GUC $1.5B = $32.6B，
  重疊調整後 ≈ $30B+）
```

_短期 bear case 補充（插入 `→ $16-19B` 之前）_:
```
（推導：AVGO bear $35B × 50% = $17.5B + Alchip <$0.9B + MediaTek $1.5B + MRVL $1.5B + GUC $1.0B ≈ $22.4B，
  重疊調整後 ≈ $18-19B；若 OpenAI 合約大幅延後 AVGO Q3-Q4 rev 下修 → 低端 $16B）
```

_中期 bull case 補充（插入 `→ $75B+` 之前）_:
```
（推導：2026 $24B × 3Y 41% CAGR = $67B base-bull；加 merchant LLM lab ≥ 3 家額外 NRE pool +$8-10B ≈ $75-78B）
```

_中期 bear case 補充（插入 `→ $35B` 之前）_:
```
（推導：2026 $24B × 3Y 13% CAGR = $35B；驅動因：AVGO IP royalty GM 68% → 60% 等於 -12% 收入效果，
  加 design 工作部分內化 → 整體 TAM 增速壓至 13% CAGR）
```

_長期 bull case 補充（插入 `→ $115B` 之前）_:
```
（推導：2029 bull $75B × 1.24^2 = $115B；merchant LLM lab 新增 NRE pool 2030 $12-15B 已含於 $75B 2029 bull base）
```

**Portfolio implication**: §6 推估不因此改變方向；但 PM 讀 §6 數字時需要看到 input mapping，否則 $30B vs $16B 看起來是隨意的。

---

### 🟡-2 DS-6：MRVL 在 §11 標 beneficiary=true + depth=🔴，但 §2 明確稱「2026 結構性受損」，§3/§5 無支持「MRVL 是淨受益方」的主動敘述

**位置**: ds-meta line ~26（MRVL beneficiary=true）、§11 表 11.1 MRVL row、§2 prose

**發現**:
- ds-meta: `"beneficiary": true, "depth": "🔴"`
- §2 明確敘述：「Marvell 是 2026 結構性受損 — 而非單一專案損失」「XPU growth 僅 20%」
- §3: MRVL 只在 「目前 Maia 300 是 Marvell 獨家共同設計」語境下出現（一次、附帶）
- §5: MRVL 在 §5 derive 中只作為「估算 source」（「Marvell 2025 投資人日 custom XPU $40.8B 估算」），不作為受益主角
- §11 table MRVL role: 「丟 Trainium 3/4 給 Alchip、保住 Maia 300 + Apple Baltra networking；2026 XPU growth 僅 20%」

**矛盾核心**: DS spec DS-6 要求「§11 標 🔴 beneficiary=true 的 ticker，確認 §3 或 §5 有敘述支持『為何此 ticker 受益』」。§2 §3 §5 的主要 MRVL 敘述都是「受損」「苦撐」「失去 socket」而非「受益」。雖然 MRVL 的 depth=🔴 在技術上可以解釋為「AI revenue exposure ≥ 40%」（不代表方向），但 `beneficiary=true` 欄位和 `depth=🔴` 合併使用會誤導 stock-analyst 自動讀取。

**修正建議** — 兩個選項：

選項 A（最小修改）: 將 ds-meta MRVL `beneficiary` 改為 `false` 或 `"mixed"` 以反映「AI exposure high but net loser in 2026-2027」，並在 §11 prose 增加一句說明：「MRVL 雖高 AI exposure（🔴）但在本 DS 敘述框架下為『相對受損方』— 與 §2 結構性受損描述一致」：

```json
{"ticker": "MRVL", "beneficiary": false, "depth": "🔴", ...}
```

選項 B（不改 ds-meta）: 在 §3 或 §5 補一段主動支持 MRVL beneficiary 的敘述（≥50 字），例如：「雖然 MRVL 在 2026 結構性受損，但其 Maia 300 與 Celestial AI scale-up 整合形成 2027 recovery story — §5 長期需求中 MSFT Maia 400 可能擴大 MRVL 角色」，使 §11 的 beneficiary=true 有正向敘述支撐。

**Portfolio implication**: 若 stock-analyst 讀到 MRVL beneficiary=true 且 depth=🔴，可能過度樂觀設定初始 conviction。修正後信號更準確。

---

## 🟢 COSMETIC (2 條)

### 🟢-1 DS-6：NVDA depth=🟡 與 §11 caption 公式不一致（88% AI exposure 應按公式 → 🔴）

**位置**: §11 表 11.1 NVDA row、表格 caption

**發現**:
- §11 caption 定義：`🔴 = projected AI / 設計服務 rev exposure ≥ 40% by 2028E`
- NVDA row 數字：Current ~92%, Projected ~88% → 兩個值均 >> 40%，按公式應是 🔴
- 實際標記：depth-yellow 🟡
- ds-meta 也是 `"depth": "🟡"`

**原因**: NVDA 是「受害方」（beneficiary=false），作者用 🟡 暗示「負面曝險」而非「正面受益」，這是合理的 editorial 決策，但 caption 的公式定義沒有說明「beneficiary=false 時 depth 的含義不同」。

**修正建議**: 在 §11 caption 推導行補一句：
```
「受害方（beneficiary=false）ticker 之 depth 表示 ASIC 擴張對其市占的負面威脅程度；
🟡 = 中等威脅（推論 share 受壓但絕對美元仍增）；🔴 = 高威脅（兩個維度同時受壓）。」
```
或直接在 NVDA row 加一個 footnote indicator `*` + caption footnote 說明。

**不改變結論**: 這是閱讀體驗問題，不影響 NVDA 的投資方向判斷（§8 #3 已明確說明 NVDA 絕對美元仍強）。

---

### 🟢-2 DS-4 微觀：§6 各 horizon 展開段的「敘述 vs derive」比例偏 derive-heavy

**位置**: §6 三個 horizon 展開段（line ~370-380）

**發現**:
- §6 結構：1 intro para + 1 table + 3 horizon expand paras（每個 para 都含 derive block）
- DS-4 spec：「表外有 ≥ 3 段敘述展開三個 horizon 的邏輯」— 三段確實存在 ✅
- 但每個 horizon 段的 derive block 佔段落約 60-70%，prose narrative 較薄（每個 horizon 只有 2-3 句非 derive 散文）
- 「短期 12M 本 horizon 最大 binary risk」這一段 prose 分析是好的（~80 字）
- 但 §6 整段的「歷史類比」（§1 類比一 fabless 革命在 §6 para 3/4 被引用）是有用的敘事補充

**修正建議（optional）**: 對中期（3Y）展開段補一句 forward-looking 散文，說明「3Y 段最重要的 non-linear risk 是 AVGO 60% → 45-55% derate 的速度不確定性」（目前只在 derive 中提）。若 user 認為現有 prose 已足夠，可跳過。

---

## Gates 1-14 狀態

| Gate | 項目 | 狀態 |
|:-----|:-----|:-----|
| Gate 1 | 11 章節完整（§0-§11） | ✅ |
| Gate 2 | ds-meta JSON valid + 所有必填欄位 | ✅ |
| Gate 3 | related_ids 3 個本地存在（ID_AIASICDesignService, ID_AIAcceleratorDemand, ID_AIInferenceEconomics） | ✅ |
| Gate 4 | quality_tier = Q0 設定 | ✅ |
| Gate 5 | §0 ds-thesis block 存在 | ✅ |
| Gate 6 | ds-bridge 供需平衡結論（三時間段：平衡偏緊 / 平衡偏寬鬆 / 過剩於設計層） | ✅ |
| Gate 7 | §6 三 horizon × 三情境表（9 cells + Trigger col） | ✅ |
| Gate 8 | §9 三條 Kill scenario | ✅ |
| Gate 9 | §8 三條 Non-consensus view | ✅ |
| Gate 10 | §10 ≥5 個 catalyst nodes（實際 7 個，全部有雙路徑） | ✅ |
| Gate 11 | Footer 存在 | ✅ |
| Gate 12 | 所有 11 節均有 `<aside class="ds-refs">` | ✅ |
| Gate 13 | ds-meta tickers (11) = §11 table data rows (11) | ✅ |
| Gate 14 | 無黑名單 source；T1 占比 51%（≥40% 合規） | ✅ |

---

## DS-specific 8 checks 狀態

| Check | 結果 | 分類 |
|:------|:-----|:-----|
| DS-1 表格比例（90.4% 文字，4 張表） | ✅ 比例合規；但表 11.1 有 11 data rows > 8 行上限 | 🔴 |
| DS-2 §1 → §3/§5 因果閉合 | ✅ §3 有「因果閉合 §1 inflection #4-5」顯式標籤 + 實質段落 | ✅ PASS |
| DS-3 §3+§5 供需平衡明確結論 | ✅ ds-bridge 三時間段明確結論 | ✅ PASS |
| DS-4 §6 三 horizon × 三情境 + trigger 完整 | ✅ 3×3 table + trigger 量化 + 3 narrative paras | ✅ PASS |
| DS-5 §10 catalyst 雙路徑 | ✅ 7 個節點全部有 ds-path-positive + ds-path-negative | ✅ PASS |
| DS-6 §11 ticker 與 §3/§5 一致 | ⚠️ MRVL beneficiary=true vs §2 結構性受損敘述矛盾 | 🟡 |
| DS-8 §6 推導抽查 | ⚠️ 短期 bear / 中期 bull/bear / 長期 bull 缺具體 input→output calc | 🟡 |
| DS-9 §1 雙錨點 | ✅ §1 全部 9 段均有具體日期 + 量化錨點 | ✅ PASS |

---

## 操作建議（按優先序）

1. **🔴-1 DS-1 §11 表格行數**（需 user 決策方向後 patch）：
   - Option A（推薦）: 拆 §11 表 → 11a（供應端 5 家）+ 11b（需求端 6 家），同時把表 2.1 改為 prose；最終 4 張表合規
   - Option B: 刪去 AAPL + AMZN 其中一家（AAPL 深度最淺），§11 prose 補一句說明非關鍵 ticker 未列入表

2. **🟡-2 DS-6 MRVL beneficiary**：ds-meta `"beneficiary": false`（最小修改、最不誤導）

3. **🟡-1 DS-8 bull/bear calc**：在 §6 三個 horizon 的 derive 段尾部補 4-5 行 input→output mapping（見上方具體補充文字）

4. **🟢-1 §11 NVDA depth 說明**：caption 補一句 beneficiary=false ticker 的 depth 含義

---

## 自動檢查數字摘要

- **文字比例**: 90.4%（合規，≥80%）
- **表格數量**: 4 張（合規，≤4 張）
- **表格最大 rows**: 11 行（違規，>8）
- **T1 source 占比**: 51%（合規，通常要求 ≥40%）
- **§1 雙錨點段數**: 9/9 通過
- **§6 Trigger 量化**: ✅
- **§10 catalyst 雙路徑**: 7/7 通過
- **related_ids 存在**: 3/3 通過

---

*Critic generated by id-review skill v1.4.1 (DS mode) · 2026-05-14*
*Q0 report — both Pass 1 findings apply; no Pass 2 spawned (Pass 2 mandatory for Q0 but operating as sub-agent with single-pass constraint)*
