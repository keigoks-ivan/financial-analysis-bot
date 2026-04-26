# Sub-Topic ID Value-Add Matrix（QC-I7 實作）

**用途**：子題 ID（如 Liquid Cooling vs 母題 AI DC）發布前必須填寫本矩陣，證明獨立 value-add。

---

## 填寫範本

每發布一份子題 ID，需在 `pre_publish_report.md` 的 Gate 7 段落填：

```markdown
## Gate 7: Sub-Topic Value-Add Matrix

子題 ID: {子題名稱}
母題 ID: {母題名稱}

| 面向 | 母題 ID 涵蓋度 | 子題 ID 新增深度 | 判斷 |
|:---|:---|:---|:---|
| 技術 | {母題寫了什麼} | {子題比母題深在哪} | ✅/⚠/❌ |
| TAM | {母題的數字} | {子題的拆分 / 更新} | ✅/⚠/❌ |
| 玩家 | {母題列哪些 ticker} | {子題加哪些 non-obvious} | ✅/⚠/❌ |
| Thesis | {母題的 thesis} | {子題獨立的 thesis} | ✅/⚠/❌ |
| 歷史類比 | {母題有沒有} | {子題是否不同類比} | ✅/⚠/❌ |
| Kill scenario | {母題有沒有} | {子題是否新角度} | ✅/⚠/❌ |

判斷標準：
- ✅ 至少 4 欄為「子題有獨立深度」
- ⚠ 2-3 欄有深度
- ❌ < 2 欄有深度 → 建議合併回母題
```

---

## 實際案例：Liquid Cooling ID vs AI DC ID

| 面向 | AI DC ID 涵蓋 | Liquid Cooling ID 新增 | 判斷 |
|:---|:---|:---|:---|
| 技術 | 只一段介紹液冷 | ✅ 8 個子技術 deep dive（DTC/CDU/immersion single/two-phase 等）| ✅ |
| TAM | ~$4-5B（合併提） | ⚠ $5-6.4B（拆單 phase vs two phase）**但與母題不 reconcile** | ⚠ |
| 玩家 | 列 VRT/ETN/GEV 主 | ✅ 加 Asetek / Submer / GRC / Trane / Nidec / Chemours | ✅ |
| Thesis | VRT pure play + GEV + ETN 三條 | ✅ CDU kingmaker / Immersion 2028+ / Asetek 三條（不同焦點） | ✅ |
| 歷史類比 | 光纖 / smart grid / cloud DC | ⚠ PC 水冷 + 雲端 + 加密礦機（部分重複） | ⚠ |
| Kill scenario | AI capex 減 + SMR | ✅ PFAS 監管 + Trane 衝擊 + immersion 失敗（新角度） | ✅ |

**總評**：4 欄 ✅ + 2 欄 ⚠ + 0 欄 ❌ → **✅ 通過 Gate 7**，子題有獨立 value-add。

⚠ 欄需後續 reconcile（特別是 TAM 與母題不一致的問題，跨 Gate 3 也已記錄）。

---

## 常見 fail 情境

### 情境 1：純廣度擴充無深度
子題 ID 加了 5 檔 non-obvious ticker 但技術深度沒變。
→ 判斷 ❌，應把 ticker 補進母題 §11，不需獨立 ID。

### 情境 2：重寫母題 thesis
子題 thesis 與母題 thesis 重複或同質（如母題 thesis 1 和子題 thesis 1 是同一論點）。
→ 判斷 ❌，應修母題而非開新 ID。

### 情境 3：技術 deep dive 但無獨立投資結論
子題深入技術細節但不給新投資啟示。
→ 判斷 ⚠，應加獨立 §12 + §13。

### 情境 4：有新玩家但無新投資角度
加了化學端玩家（如 Chemours）但沒分析對整體 thesis 的影響。
→ 判斷 ⚠，需補「這個新 segment 對組合的意義」。

---

## 版本歷史
- 2026-04-19 v1.0：初版，以 Liquid Cooling vs AI DC 為範例
