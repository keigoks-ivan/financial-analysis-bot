# _droplog_gate.md｜gate_card.md 濃縮時丟掉的段落

來源標記：GC=gate_contract.md、GT=gate.md.tmpl、CG=critic-gates.md、CM=CLAUDE.md（DD 層 writer↔critic 對調節）

1. **[GC] 開頭「取代對象」「為什麼要換」兩段**——v15→v17 沿革、critic-gates.md 與 gate_contract.md 的定位說明。理由：歷史沿革，v20 閘卡不需要知道自己取代了什麼。
2. **[GC] 「checklist 條目 → gate_view／judgment 欄位對照表」的表格與「(a)–(g) 對照 `dd_bundle.py::_gate_view_section`」實作註**——理由：v17 專屬 bundle 產生機制，v20 沒有 gate_view，表格內容已併入 checklist 各條一行敘述，表格形式與實作註本身丟棄。
3. **[GC] ⑤ 條文末「（2026-09-10 WP-E：口徑從「次數<2」改…)」、⑧ 條文末「（2026-09-10 WP-E：口徑從「每欄獨立條目」…)」**——版本間口徑變更 changelog。理由：只留最終口徑，不留演變過程。
4. **[GC] ⑥(iii) 「2026-09-11：v19 的 IRR／EV／asym…舊格式若手填結果，仍核對…」**——v19 過渡期新舊格式相容說明。理由：v20 是新契約，沒有舊格式包袱。
5. **[GC] 末段「🔴／🟡／🟢 口徑…此處僅重申不得脫鉤…本檔不重複展開」**——指向 gate.md.tmpl 的 meta 轉介文字，非規則本身。理由：口徑已在卡片內直接照抄 gate.md.tmpl 原文，不需要轉介句。
6. **[GT] 「讀（bundle 全文附於本訊息之後…)」整節**，含「完整來源」「scenario_meta：程式計算結果」「gate_contract.md 全文」三個 bullet——bundle 組裝與 Read 工具操作說明。理由：v20 輸入直接是 judgment.json + facts.json，不需要 bundle 組裝敘述。
7. **[GT] 「禁」節裡「禁跑任何腳本（validate_judgment.py／dd_decision.py／dd_scenario.py 已在判斷端跑過…)」**——點名 v17 專屬腳本檔名。理由：v20 由「算」步驟取代這些腳本，卡片已用「禁改 judgment.json、只出稽核清單」涵蓋核心禁令，腳本檔名屬過時實作細節。
8. **[GT] 「輸出（一次 Write 到 `{audit_path}`…)」整節**，含 `## AUDIT: 判斷級🔴 = N` 表頭、Markdown 表格輸出格式（`| # | 軸 | 燈 | 依據 | 指向欄位 | 建議改法 |`）、`{max_turns}` 輪次上限——v17 舊輸出格式與 Write 工具操作說明。理由：v20 設計稿 §4.3 明定輸出為單一 JSON 陣列，舊表格整段換成任務給的 JSON schema，Write 相關文字一併丟棄（v20 閘無工具）。
9. **[GT] 「回報（≤100 字）」節**——舊鏈閘另外回報文字摘要給呼叫端。理由：v20 的 JSON 輸出本身即回報，不需要額外回報段落。
10. **[GT] 尾端兩個 `<!-- 2026-09-11 -->` 註腳**（「獨立審核須區分定位存在與內容正確…修補後重審仍讀完整來源」「完整性與判斷燈號分開…`## COMPLETENESS: PASS/FAIL`…meta.contract 為 v19」）——前者談「修補後重審」屬閘後修補迴圈的產物；後者的 COMPLETENESS 旗標綁定 v19 contract 版本號、且需求額外一行輸出，與 v20 固定 JSON 陣列輸出格式衝突。理由：兩段都預設「閘後還有修補迴圈」，與 v20「紅燈就停不修」矛盾，整段丟棄。
11. **[CG] 全文**（QC-41／QC-48／QC-50／QC-51 spawn 範例、WebSearch 查證預算 ≤10／14 輪、`## FINDINGS` 表格輸出格式、QC-54 白話呈現核、合併載具條款、fail-safe 方向）——理由：這是「寫稿後」散文層 critic 協議（讀 HTML 全文＋WebSearch 查證），與判斷層閘（單輪、無工具、只讀 judgment.json）是不同流程階段的不同協議，gate_contract.md 開頭已明言兩者不可混用；卡片只留①–⑦原始出處引註，正文不收。
12. **[CM] TSM／PLTR A/B 對質實測敘事、篇幅比較數字、三條 kill condition**——理由：這些是「為什麼(a)(b)兩項職責不能拿掉」的證據與退場條件，屬決策脈絡，不是閘要執行的規則；卡片只取結論「(a)(b) 兩項不得因精簡拿掉」。
