---
name: deep-conviction-analyst
version: v2.0-deprecated
released: 2026-06-22
description: "【已退役 — 2026-06-22 併入 stock-analyst v13】DCA 決策層已整併進 stock-analyst 單一 DD 報告（docs/dd/DD_*.html 的 Part II）。原 DCA 觸發語『{ticker} dca』『{ticker} 定見』『conviction analysis {ticker}』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』一律改觸發 stock-analyst。本 skill 僅作 deprecation 重導向，不再產獨立 DCA 檔。"
---

# 深度定見分析師（DCA）— 已退役 ⛔

**收到任何 DCA / 定見類觸發語時，直接改觸發 `stock-analyst`**（現 v14.x，單一 DD 報告內含決策層 Part II）：

```
Skill(stock-analyst, args="{ticker}")
```

不要再產獨立 `docs/dca/DCA_*.html`。既有 343 份 legacy DCA 檔凍結保留、下游 dual-read 支援。退役背景與設計細節見 `.claude/notes/deprecated-workflows.md` 與 `docs/_handoff_v13_dd_design_20260621.md`。
