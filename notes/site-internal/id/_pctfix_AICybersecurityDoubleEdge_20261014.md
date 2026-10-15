# AICybersecurityDoubleEdge 現價分位標為估算（2026-10-14）

備份：judgment.pre_pct.json、ID_*.pre_pct.html。已重取 priced_inputs。judgment.json 與頁面（含 id-meta）同步修改。

## 修改（judgment 與頁面同）
- oneliner／why_now：「PANW 估值分位已到 5 年最高」→「PANW 估值已高於 DD 日估算區間」
- now_state：「PANW 估值分位 100」→「PANW 估算已高於 DD 日區間上緣（DD 日 2026-09-04 分位 100）」
- action：「PANW、FTNT 以現價估算的 5 年分位都到 100」→「…倍數都已高於 DD 日區間上緣（DD 日分位分別為 100、69）」；「它的分位也升到 71.7」→「它的估算分位…」
- deck：「PANW 估值分位已到 100」→「PANW 估算已高於 DD 日區間上緣（DD 日 2026-09-04 分位 100）」
- priced_in_note、gate_leading、market_view（P/E 95.9 倍句）、第一屏 key point（P/E 95.9 倍、5 年分位 100）：同上改寫
- debates point「PANW 估值分位已在 5 年頂」→「PANW 現價估算已高於 DD 日區間上緣」；priced_in「高度反映，估值分位已在 5 年頂」→「高度反映，現價估算已高於 DD 日區間上緣」
- passthrough：「PANW、FTNT 的 5 年分位都是 100，CRWD 也是 100」→「…估算都已高於 DD 日區間上緣（DD 日分位 100、69），CRWD 也一樣（DD 日 2026-08-31 分位 92）」；「MSFT 分位升到 71.7」→「MSFT 估算分位…」
- sensitivity：「FTNT 本身也在 5 年分位 100」→「FTNT 估算也已高於 DD 日區間上緣，DD 日 2026-07-30 分位 69」
- MSFT 句「5 年分位 71.7」→「估算分位 71.7」
- valuation lede：judgment「倍數與 5 年分位一律用現價估算…」→「倍數用現價估算…，分位為推估值」；頁面說明句「5 年分位是目前倍數在過去 5 年排第幾百分位，100 代表最高」→「分位為依 DD 日分位推估的估算值，不是實際 5 年分位；估算超出 DD 日區間者不給數字」
- priced_rows.pctl（表格與 JSON）：CRWD 100→估算已高於區間上緣（DD 日 2026-08-31 分位 92）；PANW 100→（DD 日 2026-09-04 分位 100）；FTNT 100→（DD 日 2026-07-30 分位 69）；NET 88.3→估算 88.3；MSFT 71.7→估算 71.7；CSCO 81.0→估算 81.0

## 略過
- DD 日明示的分位未動；「估值從高位消化」等不綁特定推估分位的句子未動。

## 交持有人
- id_meta.priced_in（高度反映）與 priced_in_note 的理由主要靠 PANW 推估分位 100（只代表倍數已超出 DD 日區間，不是真實分位）。未更動欄位值。

檢查：mech_checks 無 red、stub_validate ok、check 階段 PASS。
註：頁面由 check 階段從 judgment.json＋prose_A/B.html 重組，故頁面文字改動同步套用於 prose_A.html／prose_B.html（已備份 *.pre_pct.html）。
