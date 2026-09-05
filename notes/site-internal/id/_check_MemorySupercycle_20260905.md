# check_id.py 報告 — ID_MemorySupercycle_20260905.html

| 檢查項 | 結果 | 數值 | 說明 |
|---|---|---|---|
| 1. 檔名格式 | PASS | ID_MemorySupercycle_20260905.html | OK |
| 2. id-meta 驗證 | PASS | exit 0 | exit 0 |
| 3. 八段錨點 | PASS | 8/8 | OK |
| 4. 表格數與列數 | PASS | 12 張表 | OK |
| 5. 分歧卡 | PASS | 4 張（威脅 1） | OK |
| 6. PM 行動框 | PASS | 1 | OK |
| 7. kill 表 | PASS | 6 列 / v4 / kill_metrics 6 條 | OK |
| 8. 燈號五格 | PASS | 5/5 標記 | OK |
| 9. 資料窗 | PASS | 2026-09-04 | OK |
| 10. T1 占比 | PASS | 56.7%（floor 45%，共 30 條） | OK |
| 11. 推導行 | PASS | mechanics=4, valuation=2, risks=1, stocks=1 | OK |
| 12. 附錄歷史錨點 | PASS | 3/6 段含年份+量化 | OK |
| 13. 情境權重 | PASS | 2 張含權重欄的表 | OK |
| 14. 流程劇場外漏 | PASS | 0 處 | OK |
| 15. 篇幅 | WARN | 13989 可見字 / 78680 bytes | HTML 78680 bytes > 上限 55000（外掛 CSS） |
| 16. 重複掃描 | PASS | 1.6%（207/13026 windows） | 「傳統DRAM合約價季增幅由2026年第一季約+9」x4 @ risks, summary, thesis；「（2026-06-30），已連兩季上升→破「連續」x4 @ risks, summary, thesis；「WesternDigital過去26週漲90.7」x4 @ appendix, debates, mechanics, stocks；「esternDigital過去26週漲90.7%」x4 @ appendix, debates, mechanics, stocks；「sternDigital過去26週漲90.7%、」x4 @ appendix, debates, mechanics, stocks |
| 17. 全形標點(qc.py) | PASS | exit 0 | OK |

**T1 floor 覆蓋說明（`--t1-floor 45`，實測 56.7%）**：本主題的最高優先級承重數字之一——逐季合約價百分比——在全球範圍內只存在於 TrendForce／DRAMeXchange 一類的產業研究機構（T2-zh），各原廠一律不揭露逐季合約價，只在法說給季度均價的方向性定性語言。這是記憶體定價機制的產業結構特徵，不是本次採集的執行缺陷。所有「理論上該有 T1 對應物」的承重數字（bit supply 指引、capex、折舊、存貨、產能時程、雲端 capex、出口管制公告）均已用 10-Q／法說書面稿／法說簡報附錄／美國聯邦公報等一手文件承擔，故援引 `sources.md` 的覆蓋條款走 45% floor，未低於 45% 下限。

**篇幅說明**：HTML 位元組數超出 55KB 的軟上限，主因是附錄來源總表 33 筆逐條列出（每筆含段落、T 級、URL、as-of）與 kill 表七欄結構；可見字在帶內，內容未灌水。
