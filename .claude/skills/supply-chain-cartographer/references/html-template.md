# Thin HTML template（Step 2 全文）

> 條件載入：Step 2 寫 `docs/supply-chain/{topic}.html` 時載入。核心 SKILL.md 的 Step 2 只保留「複製 cowos.html 改 3 處」的骨架，本檔為完整可貼上的 thin template。內容自 v1.1 原文零語意變更搬移。

## Step 2：寫 thin `docs/supply-chain/{topic}.html`（複製 cowos.html / cpo.html 改 3 處）

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{Topic 完整標題} — InvestMQuest Research</title>
<meta name="description" content="{1-2 句描述 nodes 數 + 單點數 + 核心 thesis}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/engine.css">
</head>
<body data-topic="{topic-id}">

<header class="site">...</header>  <!-- 從 cowos.html 複製，無改動 -->

<main class="shell">
  <div class="crumb"><a href="/">首頁</a> / <a href="/research/">研究</a> / <a href="/supply-chain/">供應鏈地圖</a> / {Topic 完整標題}</div>
  <div class="sc-head">
    <h1 class="sc-title" id="topicTitle"><span class="spark"></span>{Topic 完整標題}</h1>
    <p class="sc-sub" id="topicSub"></p>
  </div>
  <div class="topic-tabs" id="topicTabs"></div>
  <div class="sc-toolbar">
    <div class="legend" id="legend"></div>
    <label class="sc-search">
      <input id="sc-search-input" type="text" placeholder="搜尋節點 / 公司 / 代號…" autocomplete="off">
    </label>
  </div>
  <div class="stats-row" id="statsRow"></div>
  <div class="map-wrap">
    <div class="map-canvas" id="mapCanvas">
      <svg class="edges-svg" id="edges"></svg>
      <div class="grid" id="grid"></div>
    </div>
  </div>
  <div class="def-block" id="defBlock"></div>
</main>

<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-hidden="true">...</aside>  <!-- 從 cowos.html 複製 -->

<footer class="site">...</footer>

<script src="assets/engine.js"></script>
</body>
</html>
```

→ **3 處修改點**：`<title>`、`<meta description>`、`<body data-topic="...">`、`<crumb>` 與 `<h1>` 的 topic 名 — 其他完全 copy-paste from cowos.html。
