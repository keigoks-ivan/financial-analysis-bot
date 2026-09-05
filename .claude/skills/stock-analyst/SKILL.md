---
name: stock-analyst
version: v15.2-deprecated
released: 2026-09-05
description: "【已退役 — 2026-09-05 併入 ddreport v4.0】v17 起 DD 由無頭三段制生產。原全部觸發語『{ticker} DD』『個股分析 {ticker}』『{ticker} 定見』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』『conviction analysis {ticker}』『{ticker} dca』一律改觸發 ddreport；裸 ticker 與『這檔如何／先篩一下 {ticker}／{ticker} 快篩』仍走 stock-screen-v1。本 skill 僅作重導向，本目錄 `references/` 仍是判斷與呈現規則的權威。"
---

# 個股深度分析師（stock-analyst）— 已退役 ⛔

**收到任何 DD／定見類觸發語時，直接改觸發 `ddreport`**：

```
Skill(ddreport, args="{ticker}")
```

## `references/` 仍是規則權威

v17 三段各自載入本目錄下的規則檔，判斷機器（門檻、矩陣、QC 條文、fail-safe 方向）未隨本 skill 退役：

- `references/v16/judgment-rules.md`（判斷 agent）
- `references/v16/render-rules.md`（散文 agent）
- `references/critic-gates.md`（Stage 1G 閘的①–⑦權威；閘 prompt 模板在 `scripts/dd_prompts/gate.md.tmpl`）
- 其餘條件載入檔（archetype-gatesets／cyclical-lens／roic-durability／judgment-playbook／decision-layer 等）

## 歸檔

v15.2 本體與兩份過渡草稿在 `_archived/skills/stock-analyst-v15.2/`（見其 `README.md`）。tag：`dd-v15.2-final`、`dd-v16.2-final`。回退＝`git checkout dd-v16.2-final -- .claude/skills scripts`。
