# 市況主控台七項修正與閱讀整理

2026-09-13。持有人要求七項全做、全頁重點化並由 Codex 完成；在獨立 clone 整合，不修改原共享 working tree。三個 GPT-5.6-sol 子任務處理機械層、歷史／跨市場層、版面；主 agent 整合與驗收。

1. CTA 翻轉價在現價上方時，機械讀法明示追價買盤；上下穿越分開。
2. 引信最新值從統一 evidence quotes 對帳；保留 historical 值。資料日期與過期狀態靠近讀數，月季頻率使用適用發布遲滯。
3. Kim–Wright 期限溢價標示、官方 CPI 精確十二個月年增、利率距離 bp、level unit 與 change unit 分離、分位窗口標示。未改原 CPI producer 的十二期公式，只修正 legacy cache 在合成層的引用。
4. 新增 market_history.py，從官方 observation 檔產生真實歷史、7／30／90／365 日比較及實際基準日；月季資料按期別對齊，缺月不假造年增。最新修訂歷史不冒充當時可得歷史。
5. 機率附研究判斷與校準資訊，三框架列截止日；未修改核准判讀的機率或帳簿。
6. 台、美、日、歐區域卡列實際觀測、變化、來源、日期及缺口。新增條件式傳導說明；不宣稱全球覆蓋完整。
7. 判讀／跨市場／情境／證偽優先；追溯、來源與機械附錄折疊。50 段精煉重點與 4 個短標題，原文可展開；手機時間框架直排且無整頁橫向溢出。

## 自動更新

market_sources.summarize_series 使用相同期別比較；market_refresh.prepare 將 history_context 及精煉文案要求傳給訂閱判讀工作。record 發布 history_context，分離資料與判讀成功時間。相同證據、判讀與歷史內容同日重跑不換版本；歷史補齊仍可重新發布。未增加付費 API 或模型 fallback。

本次更正資料後，發布狀態 needs_review 正確。read.json 與預測帳簿保持原核准版本，沒有把新資料倒灌成舊日已知。6 條官方序列仍缺金鑰／聯絡設定，總經時鐘仍為七月。

## 驗收

- Python 3.9：560 passed，排除既有 unrelated test_build_live_scoreboard_combined_twd.py；該檔匯入 update_long_track_w52_adaptive.py:994 的 str | None 在 3.9 失敗，本次未修改。
- 修改 Python AST、HTML inline JS／summary JS 語法通過；QC 0 errors、0 warnings；git diff --check 通過。
- 瀏覽器：桌面 1265／1265、手機 375／375（client／scroll width）；手機 horizon 直排 307px；官方 CPI 月對月／年對年而無假 7 日選項，CPI 3.35%；10 年期距 5% 為 5 bp；VIX9D／NAAIM 有過期標示。
- record 同日重跑 refresh.json 完全一致；prepare 含歷史與短文要求且 run_analysis=true，等待既有訂閱排程處理修正後證據。

主要函式：build_market_state 的 build_fuses／build_evidence_quotes／repair_cpi_yoy_from_official／classify_stale／producer metadata helpers；monitor producers 的 level-unit 與 metadata 輸出；market_history 的 build_history_context／compare_observations；market_sources 的 summarize_series；market_refresh 的 prepare／make_release／record 路徑；頁面的 compactText／quoteDateMeta／quoteChange／renderHistoryContext／renderHorizons／arrangePage。
