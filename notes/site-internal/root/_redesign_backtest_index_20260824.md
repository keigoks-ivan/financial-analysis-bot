# 改版記錄：`/backtest/` 總覽頁排列與配色（2026-08-24）

呈現層改版——內容（裁決、數字、狀態文字、連結）不動，只改排列與配色。

## 產線確認

`docs/backtest/index.html` 是**產生檔**，由 `_build_index.py`（資料層：`GROUPS`/`RET`/`TAG`/`DOM`/`YEARLY_COLS`）匯入 `_index_layout.py`（渲染層：`render()` + `TEMPLATE` 字串代換）產出，`_build_index.py.main()` 呼叫寫檔。原始檔內有一段標記「DEAD CODE」的舊 `render()`/`TEMPLATE`，非實際使用，未動。**改版全部做進兩個 `.py` 原始檔，`index.html` 只是重新 build 的輸出**，未手改 HTML 本身。

`/backtest/` 深頁樹（v7-backtest 外部 repo 產出）完全未動；`scripts/site_nav.py` 的 `EXTERNAL_TREES` 排除 `backtest`，內嵌 `imq-nav-root` nav 區塊由 `_index_layout.py` 直接呼叫 `full_nav_block()` 產生（繞過排除清單，這是既有機制、非本次改動），因此重新 build 會拿到當下最新的全站 nav——這造成 nav 區塊 byte 上有異動，但**內容與結構未被本次改版手動更動**，屬 build 流程既有副作用，非紅線違反（詳見下方「附帶事項」）。

## 現況問題（改版前）

- 配色為獨立灰白 generic 系統，未接全站 `imq-base.css` 色系
- 首屏無總覽，要滾到第二屏才看得到目前有幾套實單/候補/實驗/否決
- 美股 tab 的 `.acard` 貼死 CAGR +14.31% 等舊快照，且執行層文字「10pp 門檻＋5% 取整」已被 2026-07-22 升格的「20pp/10% 取整＋clamp 150%」取代，屬過期資訊
- 每個 tab 開頭一大坨 `.dir` 頁面連結 pill，把排名表/研究筆記往下擠
- 表格左色帶與狀態 tag 顏色未依語意分四檔統一
- 六個 tab 排列順序不一致

## 六點規格與實作

1. **色系**：`_index_layout.py` 的 `TEMPLATE` 加入 `<link rel="stylesheet" href="/assets/imq-base.css">`；`:root` 改用 `--paper/--ink/--card/--line/--accent/--gold*/--pos/--neg/--warn` 別名，`_build_index.py` 內 `TAG`/`DOM` 字典與零星 inline tag 一併改用新 token。Chart.js 兩張圖（growth line、risk/return scatter）的線色/格線色同步換色系。`<h1>` 沿用全站襯線標題慣例。
2. **狀態總覽**：tabs 下方新增 4 張狀態卡：實單 1（連 `/long-track/#live`）／合格候補 6／實驗·研究 54／否決·歸檔 15。n 值以一次性腳本機械點算 `GROUPS` 標題分類＋`DIRECTORY` pill 狀態、依 href 去重後得出，寫死於模板，不建資料鏈。
3. **實單卡改引導卡**：美股 `.acard` 移除全部績效數字與執行層參數字串，改為一句定位＋`/long-track/#live` 連結；`acard-note`（候補清單）不動。**發現**：台股 tab（原 line 326 附近）沒有對等 `.acard`，只有一張純連結出去的 `.cta` 卡，本點該分項不適用，已如實回報而非硬套。
4. **藥丸目錄降級**：`_dir()` 新增 `collapsed` 參數，包成 `<details><summary>本分類全部頁面索引</summary>...`；美股/台股/多資產/槓桿疊加 4 個 tab 的 `%X_DIR%` 從 tab 開頭移到最底部並收合。href 對帳見下。
5. **四檔語意色**：色帶/tag 統一為 實單=金、採用/候補=綠、實驗·研究=藍(--accent)、否決·歸檔=紅、基準=灰；修正一個既有 bug——舊 `lane()` 先比對「採用」子字串，會誤判標題「🔬 實驗(未採用)」（因為「未採用」裡含「採用」）為綠色；新版改為先判否決/實驗，再判候補/採用，六組標題逐一手動核對分類正確。細部狀態 tag 文字全部照留，只換色。
6. **六 tab 節奏**：美股/台股/多資產/槓桿疊加統一為 ①結論卡 ②排名表(實驗/否決收合) ③研究筆記 ④頁面索引(收合)。

## 自行裁量：總經／國家掃描的目錄不收合

規格第 4 點寫「每個 tab」目錄降級收合，第 6 點又說總經／國家掃描這種純連結清單 tab「把清單卡片化排整齊即可，不硬造排名表」——兩點對這兩個 tab 有張力：它們的 `.dir` 清單本身就是整個 tab 的全部內容，不是「次要目錄」。判斷後決定：**總經／國家掃描的 `.dir` 區塊保持可見、不收合**（`_dir(..., collapsed=False)`），僅美股/台股/多資產/槓桿疊加 4 個有排名表的 tab 才把目錄移底收合。這是我的解讀，非規格明文指定，特此標注供覆核。

## 驗證結果

**Href 完整性**：改版前用 `git show HEAD:docs/backtest/index.html` 存底，改版後以 nav 區塊（`<div class="page-hdr">` 之前，本就不動因此排除）與 body 分開 diff，用 Counter 做 multiset 比對。Body 內 href 集合零遺失，唯二差異為規格授權的變更：`.acard` 引導卡的 `/long-track-w52-adaptive/` → `/long-track/#live`（第 3 點指名）、以及狀態總覽卡新增的同一個 `/long-track/#live`（第 2 點新增元素）。

**六 tab 功能驗證**（本機 `python3 -m http.server` + 瀏覽器）：
- 美股/台股/多資產/槓桿疊加：tab 切換正常、結論卡/CTA 卡、排名表色帶與 tag 色正確、實驗與否決區預設收合、底部新增收合式「頁面索引」正常展開/收合
- 總經／國家掃描：內容卡片化整齊、`.dir` 目錄維持可見（依上方裁量）
- 兩張 Chart.js 圖（growth line + risk/return scatter）換色後正常渲染，無 canvas/script 結構性破壞
- Hash 直達：以獨立網址（`?t=N#tab`）觸發真正的頁面重新載入，逐一驗證 `#us/#tw/#multi/#lev/#macro/#scan` 皆能在載入時直接顯示正確 tab（注意：同頁換 hash 的瀏覽器行為本來就不會重跑 IIFE 路由，這是正常瀏覽器行為非頁面 bug，測試時改用獨立網址觸發完整載入排除此干擾）
- Console：僅一則與頁面無關的 Chrome extension 訊息通道例外（"A listener indicated an asynchronous response..."），非本頁 JS 產生的錯誤
- 手機版：以注入媒體查詢對應規則＋強制窄版 viewport 模擬（環境的 `resize_window` 工具未能真正改變瀏覽器可視寬度），確認 `@media(max-width:820px)` 內新增的 `.stat-row{grid-template-columns:repeat(2,1fr)}` 與既有 `.live-wrap/.grid2/.dir-row` 等規則一起生效，nav/tabs/狀態卡皆正確收窄換行、無橫向溢出

**`scripts/site_nav.py`**：全站掃描結果為 `no-body 8 / skip 30 / skip-external 570 / unchanged 1701`，無「changed」分類，確認 `docs/backtest/index.html` 落在 `skip-external`（`EXTERNAL_TREES` 排除清單）——0 changes to backtest tree。

**`scripts/qc.py`**：`docs/backtest/index.html` 本身 0 warning／0 error。全站掃描回報 1 個 gate error，位於 `notes/site-internal/root/_consolidation_system_20260823.md`（另一個 session 的既有檔案，與本次改版無關，未動它）；另有多筆半形標點 warning 分散在既有的 `docs/dd/`、`docs/id/`、`docs/earnings/` 等檔，同樣是既有問題非本次引入。`docs/backtest/criteria/index.html`、`docs/backtest/turtle_adopt/index.html`（v7-backtest 深頁）各有一筆既有 warning，屬深頁樹範圍，未動。

## 附帶事項：nav 區塊的 byte 差異

`_index_layout.py` 的 `render()` 在 build 時直接呼叫 `scripts/site_nav.py` 的 `full_nav_block()`，取得的是「當下」全站 nav 標記，與 `EXTERNAL_TREES` 排除清單（阻擋的是 site_nav.py 的批次改寫掃描，不是這條 build-time 呼叫）是兩條獨立機制。本次改版之前，最後一次 build 早於同日一筆全站 nav 更新（commit `aa8b41d8f`），因此重新 build 後 nav 區塊會多出這筆追平差異——這不是本次改版手動改動 nav 內容，是既有 build 流程的正常行為，內容/結構本身未被更動。
