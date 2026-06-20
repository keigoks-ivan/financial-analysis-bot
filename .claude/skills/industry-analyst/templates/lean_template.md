# 精煉版（決策卡）Template — canonical 入口 · v2.3

每次跑 `industry-analyst` 產**兩份**（dual-output）：

| 檔名 | 內容 | id-meta | 角色 |
|---|---|---|---|
| `ID_{Theme}_{YYYYMMDD}.html` | **精煉版決策卡**（~7 PARTS、≈45-55KB） | **有**（SSOT，索引/screener 認這份） | **canonical 入口** — 一點進來就是決策卡 |
| `ID_{Theme}_{YYYYMMDD}_full.html` | 完整考證版（9 章 + 一手 source、~170KB+） | **無**（validator 自動 skip、不重複列索引） | companion，由 canonical 連過去 |

> **canonical = 精煉版**。完整版搬到 `_full.html`。兩份**雙向連結**：canonical 底部 xlinks「完整考證版 →」連 `_full.html`；`_full.html` 頂部「⚡ 趕時間？→ 2 頁精煉版決策卡」連回 canonical。完整版的 `<head>` 拿掉 id-meta（`<meta name="id-*">` + `<script id="id-meta">` 都不放），精煉版帶 id-meta。

## Golden reference（複製這份的 CSS 與骨架，勿憑空重寫）

`docs/id/ID_AIComputeCapexCycle_20260611.html`（canonical 精煉版）為 golden reference。新主題複製其 `<head>`（Google Fonts link + id-meta + 第一個 `<style>` 編輯風 CSS）與 body 元件骨架，只換內容。

## `<head>` 必備

```html
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Serif+TC:wght@400;500;600;700&display=swap" rel="stylesheet">
```
+ `<meta name="id-*">` 三標 + `<script id="id-meta">`（含 `now_state` / `future_state` / `action`，v2.x 必填）。site nav header 沿用 canonical 站頭（`scripts/site_nav.py full_nav_block('research','id')`）。

## 視覺系統（`:root`）

`--ink:#1c1916 · --ink-soft:#3d3833 · --paper:#faf7f2 · --paper-deep:#f0ebe1 · --paper-card:#f5f1e8 · --accent:#7a3d1c · --accent-deep:#4a2410 · --gold:#b08840 · --gold-soft:#d4b572 · --muted:#6e665a · --green:#2a5040 · --red:#8a3424 · --amber:#8a6420`。body Noto Serif TC/Crimson Pro 襯線、標籤 IBM Plex Mono。

## Body 骨架 — 7 PARTS（**不含 system-integration 部分**）

`.container`（max-width 980，paper 底）包：

1. **`.masthead`**：`.pub-info`（logo + 日期/地點）→ `.headline`（大襯線標題，`<em>` 鏽金強調關鍵詞）→ `.deck`（斜體一句副標：本份是把 N 字母題濃縮成決策卡）→ `.byline`（method line）。
2. **`.stat-grid`**（8 格）：capex / 變現缺口 / 供需裁決 / 投資時鐘 / CAGR / Conviction / 核心特徵 / 代表案例（mono key + 襯線 value + `<small>` 註）。
3. **`.abstract`**（ABSTRACT 角標）：3 段 — 現狀裁決、真正脆弱點、本報告的判斷立場。
4. **`.toc`**（Contents，羅馬數字）+ **`.xlinks`**（母題/子題 + **完整版 →** 連結）。
5. **PART I `.chapter` 決策摘要層**：`.dsum`（3 欄 NOW/NEXT/ACTION，綠/金/紅 mono tag）→ `.keycall`（深墨金字「The Key Call」）→ 三道裂縫敘述 → `.monitor`（PM 級監測點，編號 1-N，任一轉弱降一級 conviction）→ `.caveat`（來源結構說明）。
6. **PART II 歷史類比**：1-2 個對照（框住 bear 天花板 + 傳導時滯錨）+ `.data-display` 表。
7. **PART III 供給側**：瓶頸 + `.inference`（含 `.deduction-chain` 前提鏈 + **可證偽條件**）+ `.data-display` 利潤池表。
8. **PART IV 需求側**：缺口 + 三角驗證表 + `.inference` + token 經濟學 + `.caveat`（多空為何都對）。
9. **PART V 裁決與情境**：`.scenario-set`（base/bull/bear + 主觀機率 + 觸發確認訊號）+ `.timeline`（Phase 三段）。
10. **PART VI 個股特徵與 conviction tier**：`.tier-list`（CORE/EDGE badge），**只輸出「特徵 + 分類」，提及公司＝「該特徵的代表案例」、非買入推薦**；估值面總結一段。
11. 收尾：`.keystone`（The One Line，置中深墨金字一句）→ `.epilogue`（「這份報告刻意不做的三件事」）→ `.footnotes`（Selected Sources，[T1]/[T3] tier）→ `.colophon`。

## 硬規則（critic 會抓）

- **PART 數＝7（PART I-VII 內容，但不含舊草稿的「System Integration / Pure MA」那節）** — 賣出訊號併入 PART I `.monitor`，不另開系統整合章。
- **個股非推薦**：PART VI + epilogue 必含「特徵/分類、買賣由個股 DD + 系統決定、非買入推薦」字句。
- **決策層完整、證據層濃縮**：精煉版保留所有判斷（裁決 / KEY CALL / 三裂縫 / 三情境 / conviction tier / 監測點），砍的是考證厚度（逐條 source 推導留給 `_full.html`）。
- **scenario 三情境必附主觀機率 + 觸發確認訊號**；inference 必附 `.deduction-chain` + 可證偽條件。
- 中文全形標點；數字 range / ~xxx；機率用「很可能/可能/不太可能」非百分比。
