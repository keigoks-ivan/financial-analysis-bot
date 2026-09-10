# DD 管線 2026-09-10 改動交接（給 Codex 複審）

規格書：`notes/site-internal/dd/_codex_rule_scope_audit_20260910.md`（Codex 第一輪審查）。本檔列出實際落地的 commit、每項怎麼做、驗收數字、以及刻意沒做或與規格書不同的地方。**尚未用真實 Fable 跑過任何一份 DD**，所有驗收都是靜態或 mock。

## Commit 清單（main，已 push）

| commit | 內容 |
|---|---|
| `b08b9fc9d` | P0：判斷包改讀最新一季逐字稿（原取 `recent_four_quarters[0]`＝最舊季且路徑重拼，14 份全漏）；gate prompt 第 5 行同步 |
| `c5edb729d` | WP-B：逐字稿摘要內容雜湊永久快取（`.dd_build/digest_cache/`）、coverage 沿用改 `COVERAGE_REUSE_POLICY` 按軸失效、用量帳改報 input／output／cost |
| `fb369e4df` | test_ddreport_finish 斷言同步 commit subject 新格式 |
| `beff7380f` | WP-A：閘輸入改機械 `gate_view`＋`scripts/dd_prompts/gate_contract.md`（14 檔 bundle −30.6%）、prose 白名單只留 judgment、`dd_headless` 一律傳 `--tools` |
| `af69121ba` | WP-C：複審 delta 路由接進 `ddreport.py::_do_judge`（`_judge_delta_route`、`judge_delta.md.tmpl`、`--no-delta`） |
| `a7f8b24d8` | WP-D：判斷規則精簡（A1–A4＋撤配額六項＋B1–B9 條件式） |
| `44bcba9ca` | notes：Codex 規格書入庫 |

## WP-D 逐項

**A1 反證合併**：canonical＝`premortem.blind_spots[]`（既有欄位）。每條選填 `view`（論點失敗／論點成功但股東經濟變差／價格已反映太多）／`evidence`／`assumption`／`consequence`／`ruling`／`watch`。`premortem.required` 降為 `blind_spots`＋`max_dd`；`trap_analysis.required` 只剩 `verdict`（與 `decision_inputs.trap` 同源，不能動）。`dd_brief.render_premortem` 按三視角分組；`render_fears` 在 `plain.fears` 缺時讀 view＝論點失敗。舊形狀全保留 fallback。

**A2 ROIIC 一次推導**：`moat.roic_durability` 為唯一推導處；§6.D／§10 改直引。schema 本無重複數字欄，只改規則文字。

**A3 結論收斂**：`plain` 必填頂層鍵 7→3（`growth_funding`／`prior_compare_reason`／`evidence_quality`）；`bets`／`fears`／`change_my_mind` 撤「長度＝3」；`reasoning` 撤 ≥3 行地板。

**A4 漂移按原因分組**：`contradictions[].prior_field` 放寬為 `string | array`，新增 `cause` enum。`validate_judgment._prior_fields_of()` 單一權威，`dd_delta.py::cmd_check` 同 import。規則＝每個 DRIFT_WATCH 變動欄必須映射到一個原因條目，漏一欄仍 FAIL（有測試）。

**撤配額**：digest「每篇 ≥12 條」→ 撤（`validate_digest` 只在 topic 數 <2 時 FAIL，其餘 WARN；14 個 run 的 digest 掃過 0 檔失敗）；reasoning 行數地板→撤；§9 Pattern match「不得說無可比」→撤；`max_dd.trigger_time` 移出 required（`lo` 仍必填，dd-meta 直讀）；QC-53 32 條→問題字典，撤逐條作文。

**B1–B9 條件式**：`industry.tam_table`／`growth.segments`／`governance.capital_returns`／`valuation.peers` 四個 schema 區塊接受 `{"expanded": false, "reason": "..."}` 標記物件。**key 仍必填**（與規格書「改 optional」不同，理由：整個省略就不會留下理由，kill condition 驗不了）。`thesis.H` 的 `2y`／`5y`／`10y` 移出 required（B6）。B4 的 `peg`／`percentile_5y`／`val_light` 仍必填（估值燈與 screener 直讀）。B8 保留 12 軸全掃，`validate_evidence` 的 `queries_run` 門檻 ≥2→≥1。B9 最新季全文親讀不變。`dd_brief` 加「未展開區塊」列；`gen_dd_tables` E3／E8／E10 遇標記物件渲染一行「未展開：理由」。

**帳本**：`knowledge/rule_ledger.md` 末列「DD 規則精簡（2026-09-10）」，kill condition＝同一證據快照盲審發現因被取消的必做項導致關鍵反證漏失／口徑錯置／應展開未展開 ≥1 例 → 該項恢復必做。

## 驗收數字

| 項目 | 結果 |
|---|---|
| `validate_judgment` 對 `notes/site-internal/dd/_src/` 19 份＋`.dd_build/runs/` 14 份 | 32 PASS；BE_20260905 FAIL 但**改動前即 FAIL**（J1 負向證據未處置，該 run 本身未完成） |
| `dd_brief` 14 份重渲染 vs 改動前 | 逐 byte 相同（0 行差異） |
| pytest（DD 相關五檔） | 160 passed；全套 234 passed（含 13 條新契約測試，既有測試零修改） |
| `judgment-rules.md` | 41,292 → 45,316 bytes（**+4KB**，條件式規則要寫觸發條件） |
| schema required 條目 | 196 → 184 |
| judge bundle（TXN 重組） | 262,936 → 267,845 bytes（+1.9%） |
| gate bundle（WP-A，14 檔合計） | 2,433,581 → 1,688,424 bytes（−30.6%） |

## 成本實況（新用量帳，13 個 v17 run）

總 $210.14：Fable 判斷段 $131.95（63%）、sonnet 收證據 $42.06、opus 閘 $26.08。Fable 每檔 output 5–18 萬 token，但 judgment.json 只約 37KB（≈12K token）——錢在思考與「首輪 ok=False 後整包重寫」（TXN／WDC 各一次）。**WP-D 省的是輸出端（反證只寫一份、四張表條件式、配額撤除），輸入端反而 +1.9%，淨效果未實跑驗證。**

## 刻意沒做／與規格書不同

1. B 類四個 schema key 保留必填（見上）。
2. `gate.md.tmpl` 未動（Stage 1G 閘不准動）；其 ⑤ 仍問「queries_run <2」而機械閘已降 ≥1，刻意留給閘自行判讀。
3. B9「optional 逐字稿由待解問題選」未實作——plan 階段零 LLM，沒有「待解問題」訊號；只撤條數配額。
4. 規格書 §五 item 5「以 byte 下限證明分析完整」未動（屬篇幅預算治理段，v17 快速版本就不適用）。
5. B10（倉位方案／PM 邊界）、Bear 機率地板、row 8a／8b、`dd_decision.py`、decision_inputs 欄位集合全部未動。
6. Codex 第一輪第 6 項「judgment 拆重複輸出：decision_out 不應要求 Fable 輸出」——查證後 `decision_out` 本來就由 `dd_decision.py run` 回填，Fable 只在最終回報引用；無需改。
7. 順手修一個既有 bug：`render_premortem` 對 dict 形態 `blind_spots` 原會渲染 Python dict repr（14 份中 13 份是 dict，之前因都有 `plain.how_to_lose` 未走到）。

## 建議 Codex 複審重點

- `judgment-rules.md` §0.5 兩個共用約定與各節「觸發條件」措辭是否會讓 Fable 系統性選「不展開」（觸發條件太鬆或太嚴）。
- `validate_judgment._prior_fields_of` 與 `dd_delta.cmd_check` 的映射規則是否有漏洞（多欄共用 cause 時能否掩蓋方法變動）。
- `_judge_delta_route` 的升級條件（`EVENTS_MAJOR_CATEGORIES`＝ma_merger／sec_investigation_restatement／clinical_fda；trigger 比對標 not_mechanizable）是否足夠保守。
- 第一次真實 Fable 跑（全套與 delta 各一）的觀察清單：Fable output token、judge check 重試次數、未展開區塊的理由品質。
