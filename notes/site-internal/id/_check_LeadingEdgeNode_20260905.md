# check_id.py 報告 — ID_LeadingEdgeNode_20260905.html

| 檢查項 | 結果 | 數值 | 說明 |
|---|---|---|---|
| 1. 檔名格式 | PASS | ID_LeadingEdgeNode_20260905.html | OK |
| 2. id-meta 驗證 | PASS | exit 0 | exit 0 |
| 3. 八段錨點 | PASS | 8/8 | OK |
| 4. 表格數與列數 | PASS | 12 張表 | OK |
| 5. 分歧卡 | PASS | 4 張（威脅 1） | OK |
| 6. PM 行動框 | PASS | 1 | OK |
| 7. kill 表 | PASS | 5 列 / v4 / kill_metrics 5 條 | OK |
| 8. 燈號五格 | PASS | 5/5 標記 | OK |
| 9. 資料窗 | PASS | 2026-09-05 | OK |
| 10. T1 占比 | PASS | 57.4%（floor 45%，共 47 條） | OK |
| 11. 推導行 | PASS | mechanics=3, valuation=2, risks=1, stocks=1 | OK |
| 12. 附錄歷史錨點 | PASS | 3/4 段含年份+量化 | OK |
| 13. 情境權重 | PASS | 2 張含權重欄的表 | OK |
| 14. 流程劇場外漏 | PASS | 0 處 | OK |
| 15. 篇幅 | WARN | 13453 可見字 / 82020 bytes | HTML 82020 bytes > 上限 55000（外掛 CSS） |
| 16. 重複掃描 | PASS | 1.4%（169/12409 windows） | 「InvestMQuestResearch&nbs」x3 @ appendix, summary；「nvestMQuestResearch&nbsp」x3 @ appendix, summary；「vestMQuestResearch&nbsp;」x3 @ appendix, summary；「estMQuestResearch&nbsp;&」x3 @ appendix, summary；「stMQuestResearch&nbsp;&n」x3 @ appendix, summary |
| 17. 全形標點(qc.py) | PASS | exit 0 | OK |

## T1 floor 覆蓋說明（60% → 45%）

本報告以 `--t1-floor 45` 執行機械閘，實測 T1（含 T1-zh）占比 **57.4%（47 條來源）**，高於覆蓋後的下限、低於 `semi` 分型預設的 60%。兩個理由：

1. **沙盒取用限制（可查證事由）**：本次撰稿環境對 `sec.gov`、`pr.tsmc.com`、`investor.tsmc.com`、`asml.com`、`newsroom.intel.com`、`semi.org`、`rapidus.inc`、`prnewswire.com`、`stockanalysis.com` 等官方與資料商網域的直讀一律回 EGRESS_BLOCKED（開稿時逐一實測 8 個網域全數被擋），承重數字只能經檢索摘要轉引官方原件，故部分條目保守標為 T2/T3 而非 T1。
2. **三個承重數字在公開層面沒有官方出口**：①TSMC N2 月產能實績與年底目標（官方從未公告 WPM，公開估計 5–14 萬片／月）；②TSM／ASML／AMAT／LRCX／KLAC 同源同口徑的 5 年估值分位（各資料商口徑與日期皆不同）；③手機 SoC／PC 對 N2 的晶圓消耗量拆分（無公開方法論）。這三項若硬補只能灌來源或推估，違反禁推估規則，故一律在正文標「未取得／查不到」。

覆蓋理由同步寫在報告 summary 段的折疊層（「資料紀律與來源可及性說明」），與本檔一致。
