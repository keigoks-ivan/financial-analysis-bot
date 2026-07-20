# 【已退役 — 2026-07-20 · v3.0 起由 report_template.md 取代】

**本檔（精煉版決策卡 template）已停用。** v3.0 廢除 dual-output 兩份制——不再分「精煉版（canonical）＋完整考證版（_full.html）」，每次跑 `industry-analyst` 只產**一份**單檔 sell-side 八段報告。

- **現行 template**：`templates/report_template.md`（Page-1 摘要層 → Thesis → Key Debates → 機制與供需 → 估值 → 風險證偽 → 個股 → 附錄折疊；id-meta 單檔 SSOT 放 head 內）。
- **退役原因**：dual-output 廢除——精煉版的決策資產（rating strip／NOW-NEXT-ACTION／KEY CALL／tier-list）與完整版的考證層（逐節來源／深機制段）在 v3.0 合併為單檔，證據層改收 `evidence-fold` 折疊。
- **既有 v2.x 精煉版 ID 檔**：凍結不動，review 走 `id-review`（自動判版）。
- 原完整內容（6 PARTS 骨架＋編輯風 CSS＋硬規則）可從 git history 取回：`git log --follow -- .claude/skills/industry-analyst/templates/lean_template.md`。
