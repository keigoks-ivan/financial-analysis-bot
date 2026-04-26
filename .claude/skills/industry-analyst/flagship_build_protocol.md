# Flagship Build Protocol（v1.4 新增）

**用途**：建立新產業 flagship 頁（如生技 / 能源 / 雲端）的 SOP。

---

## 一、何時該建 Flagship？

| 條件 | 決定 |
|:---|:---|
| 單一 ID 能解釋全部 | ❌ 不建，直接用該 ID |
| 2-3 份相關 ID | ⚠️ 累積到 5 份再建 |
| **5+ 份 ID 且有 cross-cutting insight** | ✅ 建 flagship |
| 5+ ID 但各自獨立、無共通 thesis | ❌ 改做 summary 頁（不叫 flagship）|
| 8+ ID 已成完整產業鏈 | ✅ 建 + 可考慮升級為 flagship v2（layered）|

**cross-cutting insight 定義**：一條 thesis 同時影響多份 ID 的結論（如 AI Infra 的「TSMC HBM base die」同時在 AP / HBM / LEN 三份 ID 出現）。

---

## 二、Flagship 架構（7 個強制段）

```
1. Flagship Library Selector  （位於頁面頂部）
   - 顯示本 flagship 屬於哪個產業
   - 列出其他產業 flagship（含 grey placeholder）

2. Status Bar                  （自動 staleness）
   - Version / Last refresh / Days since / Next B refresh / 狀態燈
   - JS 計算 < 60 / 60-90 / 90-120 / > 120 天

3. Hero + Lead                 （一段 < 150 字的主論述）
   - Badge: 「Flagship · Cross-ID Synthesis · 20XX 版」
   - H1: 「{產業} 投資的 N 個非共識（20XX 版）」
   - 一段說明該 flagship 的系統性視角

4. TOC                         （目錄）
   - N 條 thesis 錨點連結

5. Layer 分類章節              （產業客製）
   - AI 基建範例：需求 → 運算 → IO → 基建（4 層）
   - 生技範例：需求 → 技術 → 臨床 → 政策（4 層）
   - 能源範例：發電 → 儲能 → 電網 → 終端（4 層）
   - 消費範例：品牌 → 通路 → 供應鏈（3 層）
   - 每條 thesis 必含 consensus / ours / evidence + tag

6. Synthesis 合論               （四個層次的因果鏈）
   - 層次連動表（需求→技術→基建 等）
   - 組合曝險暗示

7. Portfolio Implications       （long/short map）
   - Super Winners（受 ≥ 2 條 thesis 受益）
   - Super Losers（受 ≥ 2 條 thesis 受害）
   - Indirect Risk
   - 殭屍贏家警示

8. Update Protocol 提醒塊        （A/B/C/D 四種觸發）
```

---

## 三、Non-Consensus Thesis 篩選標準

每條 thesis 必須同時滿足：

1. **挑戰主流**：有明確的共識對比（T3 券商 / 媒體引用）
2. **有事實支撐**：≥ 2 個獨立 data point，且有至少 1 個 T1 來源
3. **附證偽條件**：§13 落地到具體 metric + 閾值
4. **跨至少 1 份 ID**：不能是單 ID 內的 insight（那只需放該 ID）

---

## 四、每條 thesis 的標準格式

```html
<div class="thesis" id="t{N}">
  <div class="thesis-head">
    <div class="thesis-num">{N}</div>
    <div class="thesis-title">{一句話 thesis}</div>
    <a class="thesis-source" href="/id/ID_{Topic}_{date}.html">ID_{Topic} →</a>
  </div>
  <div class="thesis-body">
    <div class="consensus"><span class="label c">共識</span>{主流觀點 + T3 source}</div>
    <div class="ours"><span class="label o">本 ID</span>{本 ID 不同看法}</div>
    <div class="evidence"><span class="label e">事實基礎</span>{具體 data + T1/T2 source}</div>
    <div class="thesis-tags">
      <span class="thesis-tag type-{structural|event}">{類型}</span>
      <span class="thesis-tag layer">{Layer 編號}</span>
    </div>
  </div>
</div>
```

---

## 五、Flagship Library 更新步驟

當新 flagship 建好：

1. **建新檔**：`/id/theses-{category}.html`（如 `theses-biotech.html`）
2. **回 theses.html 啟用對應 tab**：
   ```html
   <!-- 從 -->
   <a href="#" onclick="return false" style="background:#F3F4F6;color:#9CA3AF...cursor:not-allowed">🧬 生技 / GLP-1（未建）</a>

   <!-- 改成 -->
   <a href="/id/theses-biotech.html" style="background:#7C3AED;color:#fff...">🧬 生技 / GLP-1 ✓</a>
   ```
3. **Flagship Library 計數更新**：`1 / 5 個領域 flagship` → `2 / 5`
4. **新 flagship 內部也要有 Library selector**（同一份複製過去，當前 tab 反白為該類）
5. **research/ 首頁 nav** 若該 flagship 重要 → 也加到主導覽列

---

## 六、Update Protocol（四種觸發）

同一套 A/B/C/D 規則適用所有 flagship：

| 觸發 | 條件 | 指令範例 |
|:---|:---|:---|
| A 事件補丁 | 核心 ticker 事件 / 重大新聞 | 「更新生技 flagship 第 3 條（Novo Q1 最新 GLP-1 銷售）」 |
| B 季度 refresh | 每 90 天 | 「季度 refresh 生技 flagship」 |
| C 擴充新條 | 新 ID 有 cross-cutting insight | 「生技 flagship 加第 6 條（CGM 主題）」 |
| D 整版重寫 | 每 18-24 月或 A 補丁 > 2/月 | 「生技 flagship v2.0 重寫」 |

---

## 七、QC 檢查（flagship 建置前跑）

類比 Industry DD 的 Gates，flagship 發布前必檢：

- **FG-1** Hero + Lead 是否明確 thesis map（非只是介紹）
- **FG-2** 每條 thesis 有 consensus / ours / evidence 三段
- **FG-3** 至少 3 條 thesis 出現在 ≥ 2 份 ID（cross-cutting）
- **FG-4** Synthesis 段有 layered 因果鏈說明
- **FG-5** Portfolio Implications 有 winners + losers + 殭屍
- **FG-6** Status bar JS 正確載入
- **FG-7** Update Protocol 塊完整

---

## 版本歷史
- 2026-04-19 v1.0：初版。基於 AI Infra flagship v1.0.1 的實作經驗整理。
