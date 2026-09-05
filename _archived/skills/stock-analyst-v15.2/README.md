# 歸檔：stock-analyst v15.2（含 v16 過渡草稿）

**歸檔日**：2026-09-05

## 為什麼歸檔

v17 把 DD 生產改成**無頭三段制**——`scripts/ddreport.py run {T}` 一支 Python 程式依序無頭呼叫 sonnet（Stage 0／0e 收證據）→ Fable（判斷，產 `judgment.json`）→ opus（Stage 1G 跨模型判斷層閘），再以零 LLM 產快速版；`--full` 才多加一段 sonnet 散文。單體 writer（一個 agent 讀 125.8KB SKILL.md 後一號到底把報告寫完）這個形態被取代，故整份 v15.2 skill 與兩份過渡草稿一併歸檔。

設計稿：`notes/site-internal/dd/_dd_pipeline_redesign_spec_20260905.md`（§3 新流程、§3.8 無頭模式、§7 版本與檔案收斂）。派工單：`notes/site-internal/dd/_wp_spec_v17_batch4_20260905.md` WP6c。

## 檔案來源

| 本目錄檔名 | 原路徑 | 大小 |
|---|---|---|
| `SKILL.md` | `.claude/skills/stock-analyst/SKILL.md`（v15.2） | 125.8KB |
| `SKILL.v16.draft.md` | `.claude/skills/stock-analyst/SKILL.v16.draft.md` | 25.4KB |
| `html-output.md` | `.claude/skills/stock-analyst/references/html-output.md` | 16.5KB |
| `data-collection.md` | `.claude/skills/stock-analyst/references/data-collection.md` | 26.9KB |
| `SKILL.v3.draft.md` | `.claude/skills/ddreport/SKILL.v3.draft.md` | 16.8KB |

## Tag（由 orchestrator 於本批 commit 時打，本檔只登記名稱）

- **`dd-v15.2-final`**＝歸檔前最後一個 commit（v15.2 單體 writer 鏈可運行的最後狀態）。
- **`dd-v16.2-final`**＝v16.2 最後一份上站 DD（CIEN，2026-09-05）當日的 commit。

## 回退方式

要回到 v16.2 那條鏈：`git checkout dd-v16.2-final -- .claude/skills scripts`。要回到 v15.2 單體 writer：`git checkout dd-v15.2-final -- .claude/skills scripts`。

## 仍然有效的部分

判斷機器本身沒有退役——門檻、矩陣、QC 條文、fail-safe 方向留在 `.claude/skills/stock-analyst/references/`（`v16/judgment-rules.md`、`v16/render-rules.md`、`gate-checklist.md` 與各條件載入檔），由 v17 三段的各 agent 分別載入。本目錄的檔案是**史料**，不是現行規則權威，不要當作判斷依據引用。
