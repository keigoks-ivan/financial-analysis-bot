# v12.3 冷讀 BATCH 8 — Master Report
**涵蓋 Ticker**：CSCO / DDOG / DELL / EBAY / ETN
**審閱日期**：2026-05-17
**審閱者**：Claude Sonnet 4.6 cold-review sub-agent（獨立 read-only，不 edit / commit / push）

---

## 個別 Ticker 快速摘要

| Ticker | 檔案日期 | 大小 | meta tag OK | 6-Check | 主要問題 |
|--------|---------|------|-------------|---------|---------|
| CSCO | 2026-04-27 | 87.7 KB | ✅ `v12.3` | **PASS 6/6** | 無 |
| DDOG | 2026-05-16 | 80.3 KB | ✅ `v12.3` | **PASS 6/6** | 無 |
| DELL | 2026-04-18 | 82.3 KB | ❌ `DD Schema v12.3` | **FAIL（meta）+ WARN** | meta tag 格式錯→CI bypass；§1 stale §13.5 ref |
| EBAY | 2026-05-16 | 108.2 KB | ✅ `v12.3` | **WARN** | §2 B 中 stale §13.5 ref |
| ETN | 2026-05-06 | 95.4 KB | ✅ `v12.3` | **PASS 6/6** | 無 |

**整體通過率**：3/5 完全 PASS，1/5 WARN（EBAY），1/5 FAIL+WARN（DELL）

---

## 詳細 6-Check 結果矩陣

### Check 1｜§8.H — top-1/5/10 + dual-track + source

| Ticker | top-1 | top-5 | top-10 | dual-track | in-house risk | source | 判定 |
|--------|-------|-------|--------|-----------|--------------|--------|------|
| CSCO | ✅ data-gap aside（3-6% est） | ✅ 12-18% est | ✅ 20-28% est | ✅ hyperscaler dual / enterprise sole | ✅ 3-5Y | 10-K + 分析師 | PASS |
| DDOG | ✅ OpenAI ~8-10%，Q1 法說 | ✅ 15-18% est | ✅ 22-25% est | ✅ enterprise sole / AI hyperscaler dual possible | ✅ OpenAI 自建 stack risk | 法說 + 第三方估 | PASS |
| DELL | ✅ xAI ~4.4% est | ✅ AI server 40%+ (子業務) | ✅ 有分層說明 | ✅ neocloud dual / enterprise sole | ✅ ODM 直採 | 分析師估（已標注） | PASS（note） |
| EBAY | ✅ < 1%（10-K無集中度） | ✅ < 5% est | ✅ < 8% est | ✅ multi-homing = second-source 普及 | ✅ multi-platform | 10-K + 邏輯 | PASS |
| ETN | ✅ < 10%（10-K明確） | ✅ data-gap 15-22% est | ✅ data-gap 25-30% est | ✅ hyperscaler dual-track | ✅ 自製 power stack | 10-K + §11 推估 | PASS |

### Check 2｜§9 兩軸 — execution/pricing + evidence + QC-23

| Ticker | exec 分 | pricing 分 | dd-meta sub-scores | 趨勢雙線 | QC-23 三級 | 判定 |
|--------|---------|------------|---------------------|---------|-----------|------|
| CSCO | 7/10（5條） | 6/10（4條） | `exec:7 pricing:6` ✅ | ✅ 穩定 / 緩強化 | ✅ 4行（🟡🔴⛔🔴） | PASS |
| DDOG | 9/10（5條） | 8/10（4條） | `exec:9 pricing:8` ✅ | ✅ 加深 / 加深 | ✅ 5行（🟡🟡🔴🔴⛔） | PASS |
| DELL | 8/10（5條） | 5/10（3條） | `exec:8 pricing:5` ✅ | ✅ 強 / 中低 | ✅ 5行（🟡🟡🔴⛔🔴） | PASS |
| EBAY | 7/10（4條） | 6/10（4條） | `exec:7 pricing:6` ✅ | ✅ 加深 / 穩定承壓 | ✅ 多行三級全覆蓋 | PASS |
| ETN | 8/10（4條） | 7/10（3條） | `exec:8 pricing:7` ✅ | ✅ ↑exec / →pricing | ✅ 3行（⛔🔴🟡） | PASS |

### Check 3｜§11 三段議價權 — 上/下/地緣 各 ≥ 60 字 `<p>`

| Ticker | 對上游 ≥60字 | 對下游 ≥60字 | 地緣曝險 ≥60字 | 判定 |
|--------|------------|------------|--------------|------|
| CSCO | ✅ ~200字 | ✅ ~200字 | ✅ ~150字 | PASS |
| DDOG | ✅ ~150字 | ✅ ~100字 | ✅ ~100字 | PASS |
| DELL | ✅ ~200字 | ✅ ~80字 | ✅ ~70字 | PASS |
| EBAY | ✅ ~200字 | ✅ ~150字 | ✅ ~200字 | PASS |
| ETN | ✅ ~300字 | ✅ ~200字 | ✅ ~150字 | PASS |

### Check 4｜§12 SBC + M&A — FY24/25 % + ex-EPS gap + M&A 5Y

| Ticker | SBC/Rev FY25 | ex-EPS gap | gap > 5pp? | M&A 5Y track | 判定 |
|--------|-------------|-----------|-----------|-------------|------|
| CSCO | 6.42%（⚠️↑） | GAAP/NGAP gap 28% | ⚠️ 已警示 | Splunk $28B + Acacia $4.5B | PASS |
| DDOG | 22%（⚠️持平） | $1.74/share gap | 高位但已記錄 | 無 > $50M 大型 M&A | PASS |
| DELL | ~0.82%（極低✅） | +2.0%（< 5pp，無警示） | ❌ 安全 | 有機為主，EMC legacy | PASS |
| EBAY | 4.7%（緩降✅） | 21% gap（SBC+攤銷） | 已算出 0.8pp EPS CAGR 差 | Depop $1.2B（2021） | PASS |
| ETN | < 0.5%（工業傳統✅） | < 5pp 警示閾值 | ❌ 安全 | Boyd $9.5B（2026）完整揭示 | PASS |

### Check 5｜§1 verdict 鏈一致性

| Ticker | dd-meta signal | §1 dashboard | §2 H | §13 結論 | stale ref | 判定 |
|--------|--------------|-------------|------|---------|---------|------|
| CSCO | B | B | B | 🟠→B | 無 | PASS |
| DDOG | B | B | B | 🔴→B(盲點1) | 無 | PASS |
| DELL | B | B | B | 🟡→B | **§13.5 stale ref（L95）** | WARN |
| EBAY | B | B | B | 🟠→B | **§13.5 stale ref（L243）** | WARN |
| ETN | B | B | B | 🟡→B | 無（L319 是正確說明，非 stale） | PASS |

### Check 6｜v12.3 完整性 — schema marker + §5.F + §8.H + §13 砍

| Ticker | meta tag 格式 | §5.F 存在 | §8.H 存在 | §13.0 已刪 | §13.3 已刪 | §13.5 已刪 | CI bypass? | 判定 |
|--------|-------------|---------|---------|----------|----------|----------|-----------|------|
| CSCO | `v12.3` ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | PASS |
| DDOG | `v12.3` ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | PASS |
| DELL | **`DD Schema v12.3` ❌** | ✅ | ✅ | ✅ | ✅ | ✅ | **⚠️ CI 跳過** | **FAIL** |
| EBAY | `v12.3` ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | PASS |
| ETN | `v12.3` ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | PASS |

---

## Systemic Issues（跨 ticker 共同問題）

### Issue A：stale §13.5 cross-reference（DELL + EBAY — 出現率 2/5 = 40%）

**Pattern**：v12.3 patch 時 §13.5「五角驗證 + 8 因素定錨表 + 便宜理由五問」被砍，但部分段落的 inline reference 未被清理。

| Ticker | 位置 | 原文 | 問題性質 |
|--------|------|------|---------|
| DELL | L95，§1 verdict 說明段 | `§1 = §2 H = §13.5 = B` | verdict 三點一致說明中引用已不存在的 §13.5 作為第三錨點 |
| EBAY | L243，§2 B reasoning div | `B 級對應 §13.5 合理 PE 14-16x` | §2 B 推導中引用已不存在的 §13.5 作為估值 PE 錨 |

**建議修正**：
- DELL L95：改 `§1 = §2 H = §13 結論段 = B`
- EBAY L243：改 `B 級對應 §13.4 peer tier 中位合理 PE 14-16x（mature marketplace comps）`

**根本原因**：v12.3 patch workflow 的 find-and-replace 可能只刪除了 `<h3>13.5</h3>` section body，但未掃描 body 其他位置的 inline §13.5 mentions。建議未來 upgrade 加一個 grep check：`grep -n "§13\.5\|13\.5 =" 檔案.html`。

---

### Issue B：DELL meta tag 格式錯誤導致 CI silent bypass（出現率 1/5 = 20%）

**Pattern**：`<meta name="dd-schema-version" content="DD Schema v12.3">` 應為 `content="v12.3"`。

**影響**：`validate_dd_meta.py` 的判斷邏輯是 `version.startswith("v12")`；DELL 的 content 值以 "DD" 開頭，使 CI 分類為 "non_v12" 並完全跳過，**不觸發任何驗證**。已通過 `python3 scripts/validate_dd_meta.py docs/dd/DD_DELL_20260418.html` 確認回傳 `non-v12 (skipped): 1`。

**建議修正**：將 DD_DELL_20260418.html 第 5 行改為 `<meta name="dd-schema-version" content="v12.3">`。

**根本原因**：v12.3 patch 時 DELL 的 meta tag 寫入了舊 schema_version string 格式（某些早期 DD 在頁首字串和 meta tag 混用）。可能是因為 DELL 的原始 DD 是從 v12.0 升級而非全新生成，升級腳本對此 header 格式有遺漏。

---

## 品質觀察（Sub-tier 特定）

| Ticker | Sub-tier | 特定觀察點 |
|--------|---------|-----------|
| CSCO | networking incumbent | §9 正確辨識 ANET 主導 + CSCO second-source position；pricing power 6/10 符合「hyperscaler 無議價力」現實 |
| DDOG | SaaS observability | §8.H OpenAI single-name ~8-10% 集中度風險已明確標示；SBC 22% Rev 的高位在 dashboard 中有顯著 ⚠️ 說明 |
| DELL | hardware OEM | §9 pricing power 5/10 符合「AI server BOM 90% NVIDIA GPU 無議價力」結構；meta tag 是最大問題 |
| EBAY | e-commerce marketplace | §9 正確使用「dual-dimension default」（marketplace 不適用 single-axis escape）；§11 multi-homing 作為 second-source 的敘述切角合理 |
| ETN | electrical infra | §11 議價權三段是本批最深入（ETN 300字 + 200字 + 150字），供需約束（228GW backlog）作為 pricing power 支撐的論證清楚 |

---

## 修正優先度

| 優先度 | Ticker | 修正項 | 位置 | 是否 CI blocking |
|--------|--------|--------|------|-----------------|
| P1 | DELL | meta tag 格式錯誤 → CI bypass | L5 `content="DD Schema v12.3"` → `content="v12.3"` | **Yes（CI silent bypass）** |
| P2 | DELL | stale §13.5 reference | L95 `§13.5 = B` → `§13 結論段 = B` | No（cosmetic） |
| P3 | EBAY | stale §13.5 reference | L243 `§13.5 合理 PE` → `§13.4 peer tier 合理 PE` | No（cosmetic） |

---

## 冷讀結語

本批 5 檔的 v12.3 patch 整體品質中上。所有 5 檔均正確實施了 §8.H 客戶結構深度（top-1/5/10 + dual-track + in-house risk）、§9 二維護城河（execution + pricing power 分別評分 + dd-meta sub-scores）、§11 議價權三段獨立、§12 SBC 真實稀釋（ex-EPS gap 計算）、§13 瘦身（13.0/13.3/13.5 確認刪除）。

主要 systemic weakness 是 **stale §13.5 cross-reference**（DELL + EBAY）與 **DELL meta tag 格式錯誤**。前者是 patch 流程中 grep 不完整的副作用，後者是 upgrade 腳本的 header 處理遺漏。兩者均有明確的修正路徑，修正成本低。

CSCO / DDOG / ETN 達到完全 PASS，可作為 v12.3 patch 品質基準範例。
