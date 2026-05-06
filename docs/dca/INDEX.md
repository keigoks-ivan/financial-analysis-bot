# DCA 報告索引（Deep Conviction Analysis）

本檔案由 `deep-conviction-analyst` skill 自動維護。每次執行 DCA 後，skill append 一行新記錄。

**定位**：DCA 是 DD 之上的「投資決策層」 — 假設 stock-analyst 的個股 DD 與 industry-analyst 的產業 ID 已存在，DCA 在其上做三軸獨立搜尋 + 矛盾裁決 + 基金經理決策框架。

**欄位說明**：
- **Date**：DCA 報告執行日期（YYYY-MM-DD）
- **Ticker**：正規化代碼（美股 = AVGO，台股 = 2330TW）
- **Thesis**：§2 One-Sentence Thesis，≤50 字
- **Filename**：HTML 檔名（`DCA_{TICKER}_{YYYYMMDD}.html`）
- **DD basis**：本 DCA 引用的 DD 報告檔名（無則「—」）
- **ID basis**：本 DCA 引用的 ID 報告檔名（無則「—」）

---

| Date | Ticker | Thesis | Filename | DD basis | ID basis |
|:---|:---|:---|:---|:---|:---|
| 2026-05-06 | 2330TW | TSMC 是 AI 時代唯一供應頂尖製程的 silicon bottleneck，A16 + CoWoS 雙寡占讓它成為 AI 產業鏈的 toll booth | DCA_2330TW_20260506.html | DD_2330TW_20260504.html | ID_LeadingEdgeNode_20260419.html / ID_HighNAEUV_20260505.html / ID_CoWoSCoPoS_20260501.html / ID_CoPoSFOPLPRace_20260505.html |
