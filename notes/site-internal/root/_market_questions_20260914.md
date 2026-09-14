# 市況待驗證問題板

2026-09-14。使用者要求把競爭解釋、反證與下一驗證點放上主控台，並明確要求這次由 Codex 完成，Claude 本週額度已用完。沒有呼叫 Claude、沒有改訂閱排程或開付費 API fallback。

## 研究邊界

三題：利率上升原因、短期廣度與長期趨勢分歧、弱端信用是否擴散。11 個引用綁定 b2388d0c8c14679eb39f900a67925119670b1622d42fc218821c7046d55ba9c1。FRED 檢查通膨補償與高收益利差口徑，聯準會官方日程確認九月會議。沒有政策期貨會前定價紀錄，明列未知，不把舊文的升息機率沿用成已核實事實。

作者 GPT-6-astra；GPT-5.6-sol 做獨立冷讀與程式子任務。首輪指出短期／長期廣度混用、微幅跨線過度推論、信用指標重疊及實質利率措辭，已逐項修正。門檻沿用既有判讀，明列尚未校準；相關 kill condition 在 rule_ledger 登記。舊 read.json／預測帳簿不改。

## 自動更新與人工核對

questions.json 是有日期及固定引用的研究產物，market_questions.py 檢查正文 hash、異模型冷讀及原快照；record 將它與現況一併放入不可變發布包。新引用變動或期限到期只標重評，未引用資訊變化不偽造某題結論已失效。

下一次訂閱執行先跑 market_refresh.py prepare，讀 question_board_guidance／analysis_scope；questions_only 時只更新問題板，full_read 時照原流程處理機率判讀並另外核對問題板。可呼叫任一可用訂閱模型完成研究與另一模型冷讀；額度不足保留舊研究日期及待重評狀態，不呼叫 API fallback。

候選程序：複製 questions.json 為非公開工作草稿，更新 as_of／snapshot_id／研究正文及恰好全部引用的 evidence_snapshot.quotes。獨立冷讀通過後 editorial_review 填真實 model／verdict／content_hash。執行 `python3 scripts/market_questions.py validate --candidate <草稿> --data-dir docs/market/data`，通過才將已核准 JSON 放回 questions.json，然後 `python3 scripts/market_refresh.py record --write`。record 保留舊發布包，避免覆寫歷史。

## 驗證

完整可收集測試 572 項通過；排除既有 Python 3.9 不相容的 test_build_live_scoreboard_combined_twd.py，其匯入 update_long_track_w52_adaptive.py:994 失敗，本次未動該檔。UI 最後修正再跑 7 項通過。Python AST、頁面 JavaScript 語法、候選板 CLI 驗證、diff 檢查通過。QC 零錯誤；rule_ledger 原有第 43、44、47 行三項半形標點警告，新增段落無警告。

桌面與 390×844 手機瀏覽器驗收通過；手機內容寬與 scrollWidth 均為 375，三張卡完整，展開支持／反對證據可見保存日期。修正問題板導覽被頂部選單遮住及 percent 原始單位。發布 record 重跑保留相同 bundle／generated_at，沒有假新版本。

主要函式：新增 validate_board、board_hash、derive_review、load_question_board、驗證 CLI；refresh 的 prepare、make_release、publish 接入問題板；UI 的 renderQuestionBoard、questionEvidenceList、questionQuoteValue、quoteHasChanged 顯示分層證據。
