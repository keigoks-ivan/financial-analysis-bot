> 2026-09-13 更新：使用者已明確要求 Codex 直接完成發布，以下交接狀態已被取代。已發布 commit 8f71f2234；正式部署 34756993051 成功，零模型更新 34757053471 與自動部署 34757080170 均成功。正式網址 https://research.investmquest.com/regime/ 已完成瀏覽器驗收。

# 大類資產更新交接，2026-09-13

本機修改與驗收完成，尚未 commit／push／遠端發布。依 AGENTS.md 由 Claude 主 session 決定放行。原 working tree 的其他修改均保留；請勿 reset 或廣域提交。

## 原因與最後行為

線上 build_regime 已於 9/13 執行，COT 到 9/8，比率週線標記到 9/7，但六軸、0.63 綜合分數、觸發條件仍為 7/6 硬編碼。重跑舊 builder 不會更新這些判讀。

現在頁面前方有每日六軸觀測，直接讀取市場頁 refresh.json 指向的同一份不可變 release；顯示觀測日、判讀日、缺漏／待重評狀態。綜合判讀與情境全文共用該包已通過審查的 read，不另跑模型、不生成新分數或新投資裁決。這裡保留市場包的原文，未重新審核或改寫它的金融結論。

COT 與三比率沿用既有週更排程。每筆 COT 有自己的觀測日、四週變化和樣本數；價格比標公式、週線標記、歷史百分位及 52 週變化。週線日期可能為週初或週末，不改稱確定收盤日。銅金比改保留八位小數，避免原四位捨入失真。缺漏、過期、無可用判讀或抓不到發布包都有明示。

7/6 評分與創刊號移入歷史區。REGIME_20260706.html 原檔未修改。

## 資料契約與相容性

latest.json 新增 schema `regime-observations-v2`。`historical_editorial` 保存舊 composite／axes／triggers 與日期；原頂層三欄分別為空字典、空列表、空列表。這是刻意阻止既有 intel fetch／summarize／detective 繼續把 7 月判讀當現況，不應把舊值補回。detective 不再產生舊定性分數的變動訊號；真正市場判讀與證偽命題仍由市場頁既有研究流程維護。

`meta.data_as_of` 取完整 COT 與三比率的最舊日期；不完整時為 null。`meta.publish_date`／`editorial_as_of` 保持歷史日期，絕不改成執行日。市場頁 regime 環境卡、freshness 與情報週更區已改用觀測欄位。其他消費者的舊 composite 讀取會安全降級，不會得到新冒充的定性分數。

兩層都失敗時，builder 在寫檔之前以非零退出，保留前次 JSON／HTML。無資料變化的重跑沿用原 generated_at，不製造假版本。`--skip-fetch` 現在不寫價格快取。新增 `--out-dir`／`--cot-history`／`--price-cache` 供隔離驗收。

## 本次檔案與函式

- `scripts/build_regime.py`：cot_compute、build_price_cache、ratio_compute、render_dashboard、inject_dashboard、main。
- `scripts/build_market_state.py`：build_environment、build_components、build_freshness、main 中的 regime 日期候選。此檔還有其他 session 的修改。
- `scripts/intel/render.py`：load_status_snapshot 的 regime_label、render_weekly_regime。此檔還有其他 session 的修改。
- `docs/regime/index.html`、`docs/regime/current.js`、`docs/regime/data/latest.json`。
- `scripts/tests/test_regime_refresh.py`。

同目錄 `_regime_update_20260913.patch` 只含本輪差異，以開始修改前的本機檔案為基線；它供審查與移植用，不要盲目重複套用到已包含修改的 working tree。未追蹤的新 JS 與測試需要明確加入發布提交。

## 驗收證據

- Python 3.9 AST、JavaScript 語法檢查通過；QC 7 檔，0 errors／0 warnings。
- 專項 7 passed：歷史判讀隔離、日期逐筆保留、部分來源缺漏、銅金比精度、同日冪等、全失敗保留、兩頁消費者與前端缺值／未來日期／審查狀態／跳脫。
- 完整 scripts/tests 被既有 `scripts/update_long_track_w52_adaptive.py:994` 的 `str | None` Python 3.9 相容問題擋住收集。只排除 `test_build_live_scoreboard_combined_twd.py` 後，565 passed。未修改該他人檔案。
- 獨立低成本模型唯讀複查：無新增阻斷問題。
- 瀏覽器以實際線上市場 release 加目前 main 的兩份價格／COT 快取驗收；6 張卡、18 個觀測、判讀 9/13、COT 9/8、比率週線 9/7 均顯示。手機內容寬與 viewport 同為 375px，無水平溢出。
- 情報週更區以本次真實 JSON 渲染通過。市場 state 僅輸出至 /tmp 驗收，未覆寫已發布市場證據。

## Claude 發布前要核對

在最新 main 的隔離 checkout 移植本輪差異，保留其他工作。核對建置與消費者一起發布，避免舊 builder 覆蓋新 schema。用那個 checkout 的最新快取重新跑 build_regime；不要將目前本機其他過期上游重建後覆蓋遠端市場或情報。

不必新增模型排程：每日觀測跟隨既有市場 Actions 的 release，判讀跟隨原 Claude 訂閱 routine；COT／比率由原 intel 週日流程更新。確認部署包含 current.js，且線上 /market/data/refresh.json 與指定 releases/<sha>.json 可讀。缺檔回退已測，但應在正式發布後再開 /regime/ 驗證載入。

最後用最新上游重建市場 state／record 與情報頁，確保所有頁面改讀觀測欄位，再依既有權限發布與驗收。Codex 未執行遠端放行。

本機預覽：http://127.0.0.1:8768/regime/，內容來自 /tmp/regime-preview，只供此次驗收。

本輪結束時 `git diff --stat`（5 個已追蹤檔，包含兩個混合修改檔的既有差異）：437 insertions(+), 262 deletions(-)。另有新增 JS、測試與本交接檔；實際本輪差異以隨附 patch 為準。
