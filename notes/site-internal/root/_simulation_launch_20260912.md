# 模擬交易上線（2026-09-12）

使用者明確要求將已完成的盤感 LAB 放到 research.investmquest.com，並在系統下方新增模擬區塊。本次沿用 GitHub Pages 的 docs/ 發布流程。

- `/simulation/`：完整靜態交易室，從 v7-backtest/market-replay 已驗證版本複製；來源 SHA 見 simulation/release.json。
- 首頁在系統卡下方新增模擬區塊，頁首在系統之後增加模擬連結。canonical site_nav.py 同步入口，首頁、系統主控台與模擬頁使用新導覽；其他既有頁隨原生成流程更新，不重寫研究報告。
- 資料與成交引擎沿用原版本；所有行情從同站相對路徑載入，不依賴私人 Sites 網址或第三方登入。
- 紀錄保存在瀏覽器；新網域無法直接讀取舊 Sites 網域的 localStorage。
- 來源專案的 56 項引擎與互動測試已通過；整合後以同一套測試在此站路徑再次驗證。

維護時從來源 dist 複製公開資產，保留此站 canonical link，再使用 site_nav.process 注入 simulation/index.html 導覽。不要複製 .openai、原始來源封存或測試 fixture 到 docs。

導覽原檔有兩處 f-string 跳脫引號，Python 3.9 無法解析；本次把屬性字串移至區域變數，輸出逐位元不變。全站測試另有原有模組使用 Python 3.10 型別語法，因此完整測試沿用既有 Python 3.12 環境；未修改其他模組。

最終驗證：搬移後交易室 56 項測試通過；研究站 scripts/tests 442 項通過；QC 為 0 errors／0 warnings；同站資產與導航順序已檢查。
