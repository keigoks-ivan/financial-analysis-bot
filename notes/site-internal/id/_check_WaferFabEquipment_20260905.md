# check_id.py 報告 — ID_WaferFabEquipment_20260905.html

| 檢查項 | 結果 | 數值 | 說明 |
|---|---|---|---|
| 1. 檔名格式 | PASS | ID_WaferFabEquipment_20260905.html | OK |
| 2. id-meta 驗證 | PASS | exit 0 | exit 0 |
| 3. 八段錨點 | PASS | 8/8 | OK |
| 4. 表格數與列數 | PASS | 11 張表 | OK |
| 5. 分歧卡 | PASS | 4 張（威脅 1） | OK |
| 6. PM 行動框 | PASS | 1 | OK |
| 7. kill 表 | PASS | 5 列 / v4 / kill_metrics 5 條 | OK |
| 8. 燈號五格 | PASS | 5/5 標記 | OK |
| 9. 資料窗 | PASS | 2026-09-05 | OK |
| 10. T1 占比 | PASS | 65.7%（floor 60%，共 35 條） | OK |
| 11. 推導行 | PASS | mechanics=4, valuation=2, risks=1, stocks=1 | OK |
| 12. 附錄歷史錨點 | PASS | 2/2 段含年份+量化 | OK |
| 13. 情境權重 | PASS | 2 張含權重欄的表 | OK |
| 14. 流程劇場外漏 | PASS | 0 處 | OK |
| 15. 篇幅 | WARN | 13619 可見字 / 80866 bytes | HTML 80866 bytes > 上限 55000（外掛 CSS） |
| 16. 重複掃描 | PASS | 0.6%（74/12754 windows） | 「InvestMQuestResearch&nbs」x3 @ appendix, summary；「nvestMQuestResearch&nbsp」x3 @ appendix, summary；「vestMQuestResearch&nbsp;」x3 @ appendix, summary；「estMQuestResearch&nbsp;&」x3 @ appendix, summary；「stMQuestResearch&nbsp;&n」x3 @ appendix, summary |
| 17. 全形標點(qc.py) | PASS | exit 0 | OK |
## T1 floor 說明

- 本報告 `mega = semi`，T1（含 T1-zh）floor ＝ **60%**，**未申請 `--t1-floor 45` 覆蓋**；patch 後實測 65.7%（35 條來源中 23 條 T1／T1-zh，新增 #35 為 T2 故比例較初稿 67.6% 略降，仍高於 floor）。
- 沙盒環境下多數投資人關係網站與監理申報頁（investors.micron.com、www.semi.org、www.seaj.or.jp、automation-news.jp）WebFetch 被 egress proxy 直接擋，公司官方數字改以 WebSearch 取得官方新聞稿／法說原文摘要，原始網址與官方發布日已逐條列於附錄來源總表；此為取得路徑差異，非來源層級降格。
- 篇幅 WARN（patch 後 80,866 bytes / 13,619 可見字，> 55,000 bytes 上限）屬 v4 家族常態（Agentic 75.7KB／算力 capex 77.7KB／HBM 80.9KB），非機械 FAIL；可見字仍在硬上界 14,000 內。

## 採集端未解缺口（已於正文誠實標示，未推估補數）

1. 六檔同一資料源、同一取數日的 Forward P/E 與 5 年歷史分位——查無單一同口徑來源，§4 改以「追蹤倍數 vs 5 年均值倍率」＋「遠期倍數 vs 類股中位數」兩個可查證替代指標作結論，並在表內標註各檔取數日不同。
2. DDR5 16Gb 合約價 2025-01 起逐月序列——僅得季度合約價季增幅（3Q26 +13–18%）與單點現貨值，kill 表第 1 條改以季度合約價季增幅為指標。
3. 各設備商 investor day 對 2028／2030 SAM 的官方逐項數字（含頁碼）——查不到，TAM 三情境改以 SEMI 官方預測（2026-07-14）為基準錨、投行展望為 bull 錨。
4. Hitachi High-Tech 半導體設備絕對營收——查不到，6501.T 純度欄留「查不到」、維持 🟢 邊緣分級。
5. 前四輪 WFE 高峰 vs 五寡占股價高峰的領先落後季數——查不到現成統計，遵守禁自行推算股價規則，附錄類比表不含此欄。
6. 荷蘭、日本 2026 年對半導體設備的出口許可政策官方公告原文——查不到，正文僅以美方 T1 公告論述管制的雙向性，未引用二手政策彙整。
