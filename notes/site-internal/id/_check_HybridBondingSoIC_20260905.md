# check_id.py 報告 — ID_HybridBondingSoIC_20260905.html

| 檢查項 | 結果 | 數值 | 說明 |
|---|---|---|---|
| 1. 檔名格式 | PASS | ID_HybridBondingSoIC_20260905.html | OK |
| 2. id-meta 驗證 | PASS | exit 0 | exit 0 |
| 3. 八段錨點 | PASS | 8/8 | OK |
| 4. 表格數與列數 | PASS | 11 張表 | OK |
| 5. 分歧卡 | PASS | 4 張（威脅 1） | OK |
| 6. PM 行動框 | PASS | 1 | OK |
| 7. kill 表 | PASS | 5 列 / v4 / kill_metrics 5 條 | OK |
| 8. 燈號五格 | PASS | 5/5 標記 | OK |
| 9. 資料窗 | PASS | 2026-09-05 | OK |
| 10. T1 占比 | PASS | 48.6%（floor 45%，共 37 條） | OK |
| 11. 推導行 | PASS | mechanics=3, valuation=2, risks=1, stocks=1 | OK |
| 12. 附錄歷史錨點 | PASS | 2/2 段含年份+量化 | OK |
| 13. 情境權重 | PASS | 2 張含權重欄的表 | OK |
| 14. 流程劇場外漏 | PASS | 0 處 | OK |
| 15. 篇幅 | WARN | 13502 可見字 / 81077 bytes | HTML 81077 bytes > 上限 55000（外掛 CSS） |
| 16. 重複掃描 | PASS | 2.2%（273/12664 windows） | 「InvestMQuestResearch&nbs」x3 @ appendix, summary；「nvestMQuestResearch&nbsp」x3 @ appendix, summary；「vestMQuestResearch&nbsp;」x3 @ appendix, summary；「estMQuestResearch&nbsp;&」x3 @ appendix, summary；「stMQuestResearch&nbsp;&n」x3 @ appendix, summary |
| 17. 全形標點(qc.py) | PASS | exit 0 | OK |

## T1 floor 覆蓋說明（--t1-floor 45）

本檔 `mega=semi`，預設 T1 floor 為 60%，本次以 `--t1-floor 45` 覆蓋，實測 48.6%（37 條來源中 18 條 T1）。兩點理由：

1. **官方出口存在但本次無法直讀**：承重數字的一手文件（Besi 2026 Q2／Q1 業績新聞稿、Adeia 2026 Q2 業績新聞稿、應用材料 FY26 Q3、台積電 2Q26 財報與 6-K、ASMPT 2026 中期業績、Camtek 2026 Q2、Kulicke & Soffa 法說書面說明、SUSS 官方產品頁、三星半導體官方新聞稿）確實存在，但本作業環境對公司 IR 網域、SEC EDGAR 與多數財經站的直連被 egress 阻擋（採集端實測 besi.com／ir.appliedmaterials.com／globenewswire／stocktitan／gurufocus／sec.gov 全擋），只能透過搜尋引擎對官方原件的摘要轉引，故部分官方內容僅能保守標示，無法把 T1 比例推到 60%。
2. **兩個決定性變數在公開層面沒有官方統計**：記憶體端換代時點與混合鍵合專用設備市場規模，公開層面只有 Yole、Research and Markets 與供應鏈推估三家互斥口徑（2027 年 7.3 億美元 vs 2030 年 4.965 億美元），沒有任何協會或政府機構發布過該細分市場的官方數字；為湊比例而灌入與承重無關的官方頁面，只會稀釋來源品質、不會提高判斷可靠度。

同一理由已寫在報告第一頁 `<details class="evidence-fold">`（「資料紀律與來源可及性說明」）第二段。本 run 內同樣因 egress 全阻擋而採用 45% 下限的報告尚有 MemorySupercycle／AIDCPowerElectronics／LiquidCooling／LeadingEdgeNode 四份，處置一致。
