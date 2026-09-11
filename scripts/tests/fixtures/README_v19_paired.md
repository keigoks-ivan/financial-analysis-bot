# TSM 成對測試：同一份證據跑 v18 與 v19 判斷（WP-H2-3，2026-09-11）

**一頁講完怎麼跑、產物放哪、比什麼。** 這份是操作說明，不是結論；跑之前沒有人知道答案。

## 為什麼要成對

v19 把「收事實」與「下判斷」拆開：事實表 agent 先把六問的數字收乾淨，判斷 agent 只在五個
關鍵點出手。好處是判斷層不必再從 250KB 原始證據裡挖數字；風險是**分工可能漏資料**——v18
的判斷 agent 看得到的某條反證，v19 的事實表沒抬進來，判斷層就永遠看不到，而且不會有任何
檢查響（事實檢查查不到「沒被抬進來的東西」）。

**同一份證據跑兩次判斷**是唯一能回答這件事的方式：證據相同、規則相同、模型相同，只有契約
不同，差異才歸因得回分工本身。

## 怎麼跑（證據只收一次）

```bash
# 1) Stage 0：收證據＋事實表，只跑一次
python3 scripts/ddreport.py stage0 TSM {DATE}

# 2) v19 判斷（預設契約）
python3 scripts/ddreport.py judge TSM {DATE}

# 3) v18 判斷（同一個 run 目錄、同一份證據）
python3 scripts/ddreport.py judge TSM {DATE} --contract v18
```

`--contract v18` 做三件事，其餘與平常的判斷段完全一樣：

1. 判斷包改走舊契約（`dd_bundle.py judge --contract v18`：證據包緊湊版＋digest 全文＋
   `judgment-rules.md` 的 v18 視圖），寫 `bundles/judge_v18.md`（v19 那份仍是 `bundles/judge.md`）。
2. **一律整份重判**——不走 delta、不走 reuse。走了就會把 v19 那輪的結論帶進來，差異不算數。
3. 跑完把產物快照成帶契約字尾的檔名（見下）。

## 產物放哪

| 檔 | 內容 |
|---|---|
| `{run}/judgment_v19.json`／`judgment_v18.json` | 兩輪各自的判斷物（快照，互不覆蓋） |
| `{run}/scenario_v19.json`／`scenario_v18.json` | 情境樹輸入（v19 由 `scenario_inputs` 機械產生） |
| `{run}/scenario_meta_v19.json`／`scenario_meta_v18.json` | `dd_scenario.py` 算出的 EV／IRR／AR／Max DD |
| `{run}/bundles/judge.md`／`judge_v18.md` | 兩份判斷包全文（比 token 與內容覆蓋用） |
| `{run}/manifest.json` | `judge_contract` 與每輪的 `agent_usage`（時間、token、成本） |

**活檔 `judgment.json` 永遠是最後一次跑出來的那份**——要比較就比兩份快照，不要去猜活檔是誰。
先跑 v19 再跑 v18，最後想回到 v19 就 `cp judgment_v19.json judgment.json` 再往下走。

## 比什麼（逐項對帳，不比篇幅）

1. **六問的結論方向**——逐問比 `answers.q*.verdict`（v18 在 `reasoning.*`／各結構欄）。
   方向級分歧（進場↔迴避、`moat.trend` ↑↔↓、`runway_post_y5` 燈色）是**最重要的一項**，
   有就先停下來找原因，不要先討論成本。
2. **反證覆蓋**——把兩邊 `evidence_dismissed` 以外被引用的負向 finding 列成兩個集合取差集。
   **v18 有而 v19 沒有的那些，逐條回查「這條在事實表裡嗎」**：
   - 在事實表但判斷層沒用 → 判斷層的問題。
   - 不在事實表 → **分工漏資料**，這就是 Codex 複審點名的那個風險，要改事實表 prompt 或
     擴大 `findings_digest` 帶入範圍，不是調判斷 prompt。
3. **數字有沒有漏**——v18 judgment 裡出現、v19 沒有的承重數字（五年高低點、共識家數、
   集中度、對手財務）逐個查事實表有沒有收。
4. **估值與行動條件是否有據**——`decision_inputs` 九欄逐欄對照；`rearm_trigger`、
   `kill_metrics` 的門檻數字兩邊是否指得出同一組依據。
5. **時間與總成本**——`manifest.json` 的 `agent_usage` 逐段加總（事實表、判斷、閘、散文），
   兩輪分開列。**成本是最後一項**：方向與覆蓋沒過關，省下來的錢沒有意義。

## 與 2026-08-08 那份舊報告的關係

`docs/dd/DD_TSM_20260808.html`（v15，sonnet writer）**只列為歷史裁決對帳，不當實驗組**：
證據日期不同、規則版本不同、模型與流程都不同，任何差異歸因不回契約。能用它做的只有一件事
——「本輪裁決與上一次相比變了什麼、理由寫在 `contradictions[]` 了沒有」，那是既有的前份漂移
對帳規則，不是這次的成對測試。

## 零 LLM 的預跑（不花額度，驗管線）

真跑前先用 fixture 把版面與驗收鏈走一遍：

```bash
SP=/tmp/v19check
python3 scripts/gen_dd_tables.py scripts/tests/fixtures/judgment_v19_FIX.json \
    --out $SP/tables --scenario-meta scripts/tests/fixtures/scenario_meta_FIX_20260911.json
python3 scripts/dd_project.py prose-stub scripts/tests/fixtures/judgment_v19_FIX.json \
    --out $SP/prose --facts scripts/tests/fixtures/facts_FIX_20260911.json
python3 scripts/render_dd.py --assemble $SP/prose --tables $SP/tables \
    --judgment scripts/tests/fixtures/judgment_v19_FIX.json --layout v19 \
    --no-postprocess -o $SP/DD_preview.html
python3 scripts/validate_report_v19.py $SP/DD_preview.html \
    --judgment scripts/tests/fixtures/judgment_v19_FIX.json \
    --facts scripts/tests/fixtures/facts_FIX_20260911.json
```

**`prose-stub` 的輸出會 FAIL 結構驗收**，而且應該 FAIL：stub 是骨架（每段只有結論句，沒有
lead、沒有帶 fact id 的條列），不是可發布的散文。要看一份「通得過」的長相，把每段補成
`<p class="lead">` 一句 ＋ `<ul class="pts">` 兩條以上帶 `f_*` id 的條列 ＋ §12 三視角 ＋
§13 三條行動條件再跑一次。真跑時這一段由散文 agent 寫。
