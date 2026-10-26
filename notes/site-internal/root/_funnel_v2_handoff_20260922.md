# FunnelRank v2 交接檔（2026-09-22，主 session 關閉前）

同邊界任務（dd-screener FunnelRank v2 護城河層演進）進行中，主 session 要關閉，停在以下檔案一致的點。**未 add/commit/push，任何檔案都還沒進 git staging。**

## 1. `scripts/build_dd_screener.py` 現況——FunnelRank v2 是「四層」，護城河層已完全移除

最終定案（持有人拍板）：**FunnelRank 不再有護城河層**。目前程式碼狀態：

- `FUNNEL_V2_LAYER_ORDER = ("quality", "engine", "gap", "price")`——四層，`"moat"` 已不是成員。
- 已刪除：`_load_moat_v2_judgment()`、`_moat_v2_absolute_tier()`、`FUNNEL_V2_MOAT_JUDGMENT_ENABLED`、`FUNNEL_V2_MOAT_STATUS_FOR_SOURCE`、`FUNNEL_V2_MOAT_RUBRIC_MIN_COVERAGE`（連同更早兩版的三來源鏈／覆蓋率守門／絕對分層設計，這次是真的整層拿掉，不是再疊一版）。
- 新增 `_load_moat_v2_display(ticker) -> dict`：純顯示查詢，回傳 `{"moat_questions_url": str|None, "moat_review_due": bool}`。
  - `moat_questions_url` 只有 `docs/stock-dash/data/moat/{T}.json` 存在**且** `schema=="moat-v3"` 才給值（格式 `/stock-dash/?t={T}#moat`）；其他 schema（含現行的 `moat-v2`）一律 `None`。
  - `moat_review_due` 讀 `review_due.due`，**不卡 schema 版本**，任何存在的判斷檔都讀。
  - 這兩個欄位完全不進 `compute_funnel_v2()` 的排序計算，純資訊。
- `compute_funnel_v2()` 內：`funnel_v2_profile`／`funnel_v2_tiers` 現在都是**四個元素**（quality/engine/gap/price 順序），`funnel_v2_median` 是這四層百分位的中位數（無需再排除護城河，因為護城河已經不在陣列裡了）。`funnel_v2_note` 資料不足文案改成 `"資料不足（N/4 層）"`。硬否決（`quality_veto_level=="拒絕"`／`decline_signal_light=="⛔"`／`veto_all_downgrade`）邏輯不變。
- `compute_funnel_v2()` 回傳的 summary／`layer_config` 已無任何 `moat_*` 鍵（`moat_judgment_count`／`moat_missing_count`／`moat_tier_cutoffs`／`moat_judgment_enabled` 全刪，不是留空）。
- `build()` 內 Step 4.8 的 console print 已同步簡化（拿掉舊的「moat 判斷: judgment=...」那行）。
- `python3 -m py_compile scripts/build_dd_screener.py` 通過。

## 2. 頁面／schema.md／ledger／測試現況

- **`docs/dd-screener/index.html`——已同步更新到跟程式碼一致**：
  - 方法論說明框改成「四層側寫逐層排序法」，新增「護城河不進排序（2026-09-22 最終定案）」一條說明。
  - `_thSortable('v2 名次', ...)` 表頭 tooltip 已改四層文案。
  - `_renderFunnelCell()` 已重寫：`FUNNEL_V2_LAYER_LABELS` 剩四個（事業品質/再投資引擎/期望落差/價格）、拿掉舊的 `FUNNEL_V2_BAR_MAX`（四層同量級 0–100，不需要再分護城河/其他兩種滿格基準）；`moat_questions_url` 有值時渲染「護城河三題」小連結，`moat_review_due` 為真時加「·待重看」——皆放在名次格內，tooltip 同步。
  - 舊的 `renderMoatJudgmentStatusNote()`（護城河覆蓋率/開關狀態 banner）已整段刪除，呼叫點也移除，沒有留下對已刪除 DOM id 或已刪除 summary 欄位的殘留引用。
  - 「v2 名次」條列說明（下方 `<li>`）已改四層文案。
  - `node --check` 通過；`python3 scripts/qc.py` 0 錯誤（8 個既有無關 warning，跟本次改動無關）。
- **`scripts/tests/test_funnel_v2.py`——已同步更新，27/27 過**（連同 `test_funnel_caps.py` 等其餘相關測試檔合計 101/101 過）：
  - 舊的護城河 tier／`FUNNEL_V2_MOAT_JUDGMENT_ENABLED`／`_load_moat_v2_judgment`／`_moat_v2_absolute_tier` 測試全部刪除。
  - 新增 `_load_moat_v2_display()` 測試（moat-v3 給連結、舊 schema 不給連結但 review_due 照讀、缺檔／壞檔 fail-safe）。
  - 新增「護城河欄位不影響排序」驗證（`test_moat_never_in_layer_order`、`test_moat_display_fields_populated_but_never_affect_rank`、`test_summary_has_no_moat_fields` 等）。
  - `test_insufficient_data_below_min_layers` 的文案斷言已改成 `"資料不足（1/4 層）"`。
- **`scripts/dd_screener_schema.md`——尚未更新，還是舊版說明（過時）**：目前文字仍描述「moat 層絕對分層＋`FUNNEL_V2_MOAT_JUDGMENT_ENABLED` 過渡開關」那一版設計（本次交接前一輪的中間態），跟現在的程式碼（四層、無護城河層）不一致，需要重寫「FunnelRank v2」整節。
- **`knowledge/rule_ledger.md`——尚未更新**：既有 FunnelRank v2 那一列還停在「單一來源＋絕對分層＋過渡開關」的敘述（同上，中間態），需要再補一段「最終定案：護城河不進排序，改為每檔三個關鍵問題供讀者自判」，比照先前兩次同一列追加段落的寫法（不要整段重寫，接著往下補）。
- **`notes/site-internal/root/_funnel_v2_design_20260922.md`——尚未更新**：§2.1（五層定義的護城河小節）、§3（排序法，仍寫「五個 tier」）、§5（護城河層，仍是三版設計中第二版「單一來源＋絕對分層＋開關」的內容）都需要改寫成「四層、無護城河層、moat_questions_url/moat_review_due 純顯示」。

## 3. 未完成項與重跑指令

**優先順序（若下一個 session 接手）**：

1. **改文件三處**（schema.md／rule_ledger.md／design doc）——這是純文件工作，程式碼與頁面已經一致且測試全過，文件落後不影響任何機械正確性，但會誤導讀者，應盡快補上。改法可比照本次交接前已經做過兩次的模式（rule_ledger 用「追加段落」不覆寫舊段落；design doc 的 §5 可整段替換成最終版，並在段首留一句沿革註記，不假裝一次到位）。

2. **跑一次 build 拿「前 20 名與三檔名次」回報給持有人**（這是本輪任務被交接前尚未完成的最後一步）：
   ```bash
   cd /Users/ivanchang/financial-analysis-bot
   python3 scripts/build_dd_screener.py --include-non-dd --workers 6
   ```
   （用既有 xlsx／快取，不需重抓 Koyfin；全量約需 4–5 分鐘。）跑完後：
   ```bash
   python3 -c "
   import json
   d = json.load(open('docs/dd-screener/latest.json'))
   print('funnel_v2_summary', d.get('funnel_v2_summary'))
   stocks = d['stocks']
   by_t = {s['ticker']: s for s in stocks}
   for t in ['NVDA', 'TSM', 'AMD']:
       s = by_t.get(t)
       print(t, 'rank=', s.get('funnel_v2_rank'), 'tiers=', s.get('funnel_v2_tiers'),
             'moat_questions_url=', s.get('moat_questions_url'), 'moat_review_due=', s.get('moat_review_due'))
   ranked = [s for s in stocks if s.get('funnel_v2_rank') is not None]
   ranked.sort(key=lambda s: s['funnel_v2_rank'])
   print('TOP 20:', ', '.join(s['ticker'] for s in ranked[:20]))
   "
   ```
   注意：因為護城河已完全退出排序，這次的前 20 名應該跟前一輪（僅四層生效但仍留著已強制 -1 的護城河欄位）**理論上完全相同的排序結果**（因為上一輪護城河 tier 已經被開關強制設成 -1、對排序沒有實質影響），但 `funnel_v2_profile`／`funnel_v2_tiers` 現在只有 4 個元素而不是 5 個，欄位形狀不同，下游若有任何程式碼假設 5 元素陣列（目前查過 `build_holdings.py`／`generate_targets.py` 不讀這兩個陣列欄位，只讀 `funnel_v2_rank`，應該不受影響，但沒有重新驗證，建議重新過一次）。

3. **驗證指令**（改完文件、跑完 build 後，提交前的最後檢查）：
   ```bash
   python3 -m pytest scripts/tests/test_funnel_v2.py scripts/tests/test_funnel_caps.py scripts/tests/test_dd_skill_screener.py -q
   python3 scripts/qc.py
   ```

4. **不要動**（同原任務邊界）：`scripts/build_stock_dash.py`、`docs/stock-dash/`、`scripts/check_moat_review.py`、`.claude/skills/`。不要 add/commit/push；git status 裡其他 session 的未提交檔不要碰。

## 4. 這次沒做但可能被問到的事

- 沒有重新跑 build 驗證這次改動後的實際排名結果（見上方第 3 條指令）——本檔寫成時 build 尚未執行。
- `docs/stock-dash/data/moat/` 目前四個真實檔案（AMD／MSCI／NVDA／TSM）皆是 `schema:"moat-v2"`，還沒有任何檔案是 `"moat-v3"`——這是預期中的狀態（另一位 agent 的護城河判斷 skill 仍在演進中），`moat_questions_url` 目前對全母體都會是 `None`，這不是 bug。
