# check_id.py 報告 — ID_HBM_Supercycle_20260904.html

| 檢查項 | 結果 | 數值 | 說明 |
|---|---|---|---|
| 1. 檔名格式 | PASS | ID_HBM_Supercycle_20260904.html | OK |
| 2. id-meta 驗證 | PASS | exit 0 | exit 0 |
| 3. 八段錨點 | PASS | 8/8 | OK |
| 4. 表格數與列數 | PASS | 12 張表 | OK |
| 5. 分歧卡 | PASS | 4 張（威脅 1） | OK |
| 6. PM 行動框 | PASS | 1 | OK |
| 7. kill 表 | PASS | 5 列 / v4 / kill_metrics 5 條 | OK |
| 8. 燈號五格 | PASS | 5/5 標記 | OK |
| 9. 資料窗 | PASS | 2026-09-04 | OK |
| 10. T1 占比 | PASS | 65.2%（floor 45%，共 23 條） | OK |
| 11. 推導行 | PASS | mechanics=4, valuation=3, risks=1, stocks=1 | OK |
| 12. 附錄歷史錨點 | PASS | 2/2 段含年份+量化 | OK |
| 13. 情境權重 | PASS | 2 張含權重欄的表 | OK |
| 14. 流程劇場外漏 | PASS | 0 處 | OK |
| 15. 篇幅 | WARN | 15448 可見字 / 80845 bytes | 主閱讀線可見字 15448 不在 11,000–14,000；HTML 80845 bytes > 上限 55000（外掛 CSS） |
| 16. 重複掃描 | PASS | 2.8%（410/14523 windows） | 「InvestMQuestResearch&nbs」x4 @ appendix, mechanics, summary；「nvestMQuestResearch&nbsp」x3 @ appendix, summary；「vestMQuestResearch&nbsp;」x3 @ appendix, summary；「estMQuestResearch&nbsp;&」x3 @ appendix, summary；「stMQuestResearch&nbsp;&n」x3 @ appendix, summary |
| 17. 全形標點(qc.py) | PASS | exit 0 | OK |

## T1 floor 覆蓋說明（writer 填，2026-09-04）

本檔以 `--t1-floor 45` 執行（mega=semi 常規門檻為 60%）。實際一手來源占比 **65.2%（23 條計入）**，已高於 60%，覆蓋旗僅為保險；但仍記錄降階理由，因為下列**兩類數字無法取得一手源**：

1. **價格數列**——DRAM／NAND／HBM 的逐月合約價絕對值需付費訂閱資料庫，本次僅能取得研究機構公開發布的**季度百分比變動**（列 #13／#14／#15／#16，皆 T2）。全文一律以季度季增幅表述，未以任何方式補造月度數字；投資時鐘的信心格因此只給「中」。
2. **韓國兩家的部分附註**——SK hynix 與 Samsung 的設備折舊年限附註、Samsung 每股淨值，公開檢索無法取得一手；Samsung 淨值倍數因此只給 3.5–4 倍區間（列 #22，T3），不給精確值。

承重數字（三家獲利、資本支出、折舊、存貨、股東權益、股數、HBM4 產品時程、出口管制）**全部為一手**：Micron FQ3 2026 財報與 FY2025／FY2020 年報、SK hynix Form F-1/A 與官方業績、Samsung 官方業績、NVIDIA 8-K、Google Cloud 官方文件、BIS 與聯邦公報。資本週期比值（capex ÷ 折舊）、存貨天數、淨值倍數、股東報酬率皆由上述一手報表自算，算式寫在正文推導行內。

同一句理由亦寫在報告 §1 的折疊層（本報告以 thesis 段折疊承接，template 未在 summary 段設折疊位）。
