---
name: deep-conviction-analyst
version: v2.0-deprecated
released: 2026-06-22
description: "【已退役 — 2026-06-22 併入 stock-analyst v13】舊 DCA（Deep Conviction Analysis，獨立 docs/dca/DCA_*.html 決策層報告）已整併進 stock-analyst v13 的單一報告（docs/dd/DD_*.html）：基本面 Part I + 決策層 Part II（§12 矛盾裁決 / §13 pre-mortem+Max DD / §14 統一裁決 / §15 複審）收斂為一個人面對裁決（進場/觀望/迴避）。原 DCA 觸發語『{ticker} dca』『{ticker} 定見』『conviction analysis {ticker}』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』現在一律改觸發 stock-analyst（v13）。本 skill 僅作為 deprecation 重導向，不再產獨立 DCA 檔。"
---

# 深度定見分析師（Deep Conviction Analyst）— 已退役 ⛔

**2026-06-22 起，本 skill 併入 `stock-analyst` v13。**

舊架構是「DD（基本面）+ DCA（決策層）兩份報告」。v13 把兩者整併成**單一報告 `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`**：

```
Part I  基本面深度（§1-§11，骨幹 ≥60%）
Part II 決策層（§12 矛盾裁決 / §13 pre-mortem+Max DD / §14 統一裁決 / §15 複審）
```

讀者面對的結論收斂為**一個統一裁決：進場 / 觀望 / 迴避**（+ 倉位角色），不再有「訊號燈 A+ vs 裁決進場」兩個並列頭銜。原 DCA 真正加值的決策模組（一句話 thesis、Single Thing、pre-mortem、Max DD、IRR 三分量拆解、opportunity cost、護城河趨勢 ↑→↓）全部保留在 v13 的對應章節；重複的基本面搜尋（舊 Phase A1/A2/A3）已砍除，基本面在 Part I 做一次。

## 收到 DCA / 定見類觸發語時怎麼做

當用戶說「幫我跑 {ticker} dca」「{ticker} 定見」「conviction analysis {ticker}」「最終判斷 {ticker}」「該不該進場 {ticker}」「買不買 {ticker}」——

**直接改觸發 `stock-analyst`（v13）**，產出單一 v13 報告。不要再產獨立 `docs/dca/DCA_*.html`。

```
Skill(stock-analyst, args="{ticker}")
```

## 既有 docs/dca/DCA_*.html（legacy）

343 份 legacy DCA 報告**凍結保留**、仍在站上，下游聚合器（`update_dd_index.py` / `dd_screener_dd_loader.py` / `aggregate_dca_stats.py`）以 dual-read 繼續支援——v13 DD 的 dd-meta 決策層欄位優先，讀不到才 fall back legacy DCA 檔。不需遷移、不要 retrofit。

詳見 `docs/_handoff_v13_dd_design_20260621.md`。
