# 【已退役 — 2026-07-20 · v3.0 起由 report_template.md 取代】

**本檔（完整考證版 `_full.html` template）已停用。** v3.0 廢除 dual-output 兩份制——不再產 `_full.html` companion，每次跑 `industry-analyst` 只產**一份**單檔 sell-side 八段報告。

- **現行 template**：`templates/report_template.md`（含 §0-§9 舊資產 → 新八段映射表；本檔的 §0-§9 內容模組全數映射進新架構，考證層收 `evidence-fold` 折疊、§1 背景降級為附錄）。
- **退役原因**：dual-output 廢除——「9 章完整版無 id-meta＋精煉版帶 id-meta」的雙檔協議不再存在，id-meta 單檔 SSOT 直接放新報告 head 內。
- **既有 `_full.html` 檔**：凍結不動、站上保留；validator 對其 skip 行為不變。
- 原完整內容（§0-§9 骨架＋暖紙編輯風 CSS＋模組表格速查）可從 git history 取回：`git log --follow -- .claude/skills/industry-analyst/templates/html_template.md`。
