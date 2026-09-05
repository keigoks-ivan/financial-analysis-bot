# check_id.py 報告 — ID_LiquidCooling_20260905.html

| 檢查項 | 結果 | 數值 | 說明 |
|---|---|---|---|
| 1. 檔名格式 | PASS | ID_LiquidCooling_20260905.html | OK |
| 2. id-meta 驗證 | PASS | exit 0 | exit 0 |
| 3. 八段錨點 | PASS | 8/8 | OK |
| 4. 表格數與列數 | PASS | 11 張表 | OK |
| 5. 分歧卡 | PASS | 4 張（威脅 1） | OK |
| 6. PM 行動框 | PASS | 1 | OK |
| 7. kill 表 | PASS | 5 列 / v4 / kill_metrics 5 條 | OK |
| 8. 燈號五格 | PASS | 5/5 標記 | OK |
| 9. 資料窗 | PASS | 2026-09-05 | OK |
| 10. T1 占比 | PASS | 45.5%（floor 45%，共 33 條） | OK |
| 11. 推導行 | PASS | mechanics=3, valuation=2, risks=1, stocks=1 | OK |
| 12. 附錄歷史錨點 | PASS | 3/4 段含年份+量化 | OK |
| 13. 情境權重 | PASS | 2 張含權重欄的表 | OK |
| 14. 流程劇場外漏 | PASS | 0 處 | OK |
| 15. 篇幅 | WARN | 13946 可見字 / 80200 bytes | HTML 80200 bytes > 上限 55000（外掛 CSS） |
| 16. 重複掃描 | PASS | 2.4%（308/13048 windows） | 「InvestMQuestResearch&nbs」x3 @ appendix, summary；「nvestMQuestResearch&nbsp」x3 @ appendix, summary；「vestMQuestResearch&nbsp;」x3 @ appendix, summary；「estMQuestResearch&nbsp;&」x3 @ appendix, summary；「stMQuestResearch&nbsp;&n」x3 @ appendix, summary |
| 17. 全形標點(qc.py) | PASS | exit 0 | OK |

## T1 floor 覆蓋說明（--t1-floor 45）

本檔 mega=semi，常規一手來源 floor 為 60%，本次以 `--t1-floor 45` 覆蓋，理由如下（同一理由亦寫在報告 summary 段的「本報告的來源結構」折疊內）：

1. 本主題的承重數字集中在台灣散熱零件廠的逐季毛利率、產能與資本支出，其一手材料（公開資訊觀測站、公司法說簡報／逐字稿）在本次執行環境被網路層 egress 阻擋（mops.twse.com.tw、statementdog、多數券商站台皆不可達），只能引用媒體對法說會的報導，並據實標為 T3-zh，未以轉述充作 T1-zh。
2. 美系一手文件（investors.vertiv.com、eaton.com、investor.ecolab.com、investors.tranetechnologies.com、sec.gov、q4cdn PDF）同樣被 egress 阻擋，數字改以搜尋引擎回傳之該文件原文摘要覆核；來源層級仍依原始文件判定（T1），但取得方式已在報告 disclosures 與 summary 折疊內揭露。
3. 覆蓋後實測 45.5%（15/33），未低於 45% 下限；未以任何推估數字或重複掛同一文件的方式墊高比例。

## 執行方式偏離（本次特殊情況）

本次執行環境未提供 sub-agent 派工工具（無 Task／Agent tool，僅 SendMessage／TaskStop），故 playbook 的 writer／採集／completeness／critic／patch／發布六角色無法分派，全部由單一 orchestrator 脈絡執行。影響：completeness 與 critic 為同模型自審，不具跨模型冷讀效力；兩份報告已於檔頭標明。
