# 大類資產發布完成，2026-09-13

使用者本輪明確授權 Codex 直接完成，取代先前交由 Claude 放行的安排。

程式提交：8f71f22348c7960be44d0ec7efbbf3ee2367d138。由 /tmp/regime-release-20260913 的隔離 clone 發布，原工作目錄的程式與未完成修改未改動。

正式頁：https://research.investmquest.com/regime/。

已驗證正式 HTML、JS、JSON 與情報首頁與發布內容一致。瀏覽器可讀到六軸 18 筆觀測、9/13 已審查判讀、9/8 COT、9/7 比率週線標記。情報週更頁為新版機械觀測；首頁不再冒充使用 7 月評分，封存原文保留。

部署 34756993051 成功。另實跑既有零模型 Market State Daily 34757053471，所有步驟成功，產生 main 提交 8a3f412353e2b6f135c8fa66357991a674a55585，並由新加入的 workflow_run 連動觸發部署 34757080170 成功。最後發布狀態為 degraded，既有待金鑰來源繼續明示缺漏。

專項 8 passed、AST／JS 語法檢查通過、QC 0 errors／0 warnings。隔離遠端版本的全套 Python 3.9 測試執行到 529 passed，仍有先前已知的 update_long_track_w52_adaptive.py:994 型別註記相容問題阻擋一個測試檔收集；最後增加首頁／封存不互相覆寫的專項測試後，專項 8 passed。未將原工作目錄其他未提交測試混入發布。

本次提交 git diff --stat：15 files changed, 599 insertions(+), 245 deletions(-)。除前輪列出的 regime／market／intel 函式外，新增 build_day_body 首頁與封存處理，以及 deploy-pages.yml 的市場更新／週度更新完成觸發。每日資料與已審查判讀共用市場發布包，沒有另跑金融判讀模型或新增付費 API。
