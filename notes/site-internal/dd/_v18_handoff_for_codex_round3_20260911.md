# v18 第三輪交接（給 Codex）：基準版已實作、TXN 成對驗證已跑

日期：2026-09-11 凌晨。指揮 session 依持有人授權，完成 WP-F 最小實作與一次成對驗證。請複審實作與驗證報告，並對三個待拍板題給意見。

## 讀什麼（依序）

| 檔 | 內容 |
|---|---|
| `notes/site-internal/dd/_v18_impl_notes_20260910.md` | WP-F 實作說明：六問落在哪些欄位、刪了哪些規則段、required 184→137、規則檔 45.4→41.3KB |
| `notes/site-internal/dd/_v18_paired_test_TXN_20260910.md` | 成對驗證報告：13 條反證逐條對帳、22 欄並排、閘三黃燈、成本、事故、三個下一步 |
| commit `2e594765a` | WP-F 本體（13 檔） |
| commit `750dc1312` | 驗證中補的一句規則：條件式區塊展開時必須是陣列列形狀 |
| `.dd_build/runs/TXN_20260907/`／`TXN_20260910/` | 舊／新 judgment.json、scenario_meta.json、gate_audit.md、manifest.json（本機，未追蹤） |

## 驗證結果摘要

同一份 TXN 證據包、`--no-delta`、只跑判斷＋閘、不發布。

| | 舊規則（09-07） | 新規則（09-11） |
|---|---|---|
| Fable 判斷（乾淨一輪） | $9.88 | $5.05 |
| opus 閘 | $3.16 | $1.32 |
| 合計 | $13.04 | $6.37 |
| 牆鐘 | 1,756s | 1,321s（含三輪事故） |
| 裁決／角色 | 進場／核心 | 進場／核心 |
| EV5y／IRR | 44.7／— | 44.7／8.2 |
| 實質反證 13 條 | — | 0 消失、1 弱化、1 門檻消失 |
| 閘 | — | red 0／yellow 3 |

kill condition 未觸發。偏差：舊版當時沒讀到最新季逐字稿（已修的 bug），新版有，所以「新版多了什麼」要打折；報告已分開列。

## 事故（如實）

1. 新版首輪 Fable 把 `governance.capital_returns` 寫成散文字串，patch 後成物件仍 FAIL。根因＝規則沒寫「展開＝陣列」。已補（750dc1312）。
2. 指揮 session 改 validator 訊息時在 f-string 放大括號造成 NameError，一次 resume 作廢。指揮者失誤，已修。

## 請 Codex 看的三題

1. **反證門檻消失**：舊 R3「類比 ASP 連 2 年轉負且 GM <58%」門檻整條消失，論點留在 `moat.threats[2]` 但無指標。報告建議補措辭（降位反證須保留指標門檻或寫刪除理由）而非回退。同意嗎？該門檻的變數證據包本來取不到值，是否該視為 AR≥4 型死閘另案處理？
2. **`trap_analysis.evidence_for` 引成反方向證據**與 **`val_denominator_disputed=false` 無依據**：是規則措辭問題還是 validator 該接？
3. **第二檔**：報告建議跑一檔爭議檔（WDC 或 FIX）才算完成，重點盯閘 ③ 類 J1 缺口。你認為必要嗎？取哪檔？

另有一個小 bug 待修：`scripts/dd_brief.py::_audit_counts` 用 `(\d+)` 抓黃燈數，新版閘寫中文數字「三項」→ 首屏顯示「🟡 —」。

## 未動

B10 倉位、Bear 地板、row 8a／8b、`dd_decision.py`、閘 checklist 結構、自動補查、undecidable 旗標。
