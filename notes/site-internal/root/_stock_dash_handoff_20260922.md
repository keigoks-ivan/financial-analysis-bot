# stock-dash 護城河三題制（SKILL v2.0）交接 — 2026-09-22

主 session 要關閉，中途叫停。**目前系統是一致的**：production 端（build_stock_dash.py、
docs/stock-dash 頁面、四檔 moat/{T}.json）仍是完整的舊版（moat-v2，score/width/trend
判斷制），互相吻合、可以正常跑；只有 pipeline 的兩支腳本已改完新版但**還沒執行過**，
沒有任何半改的檔案。

## ① 各檔案狀態

| 檔案 | 狀態 | 說明 |
|---|---|---|
| `.claude/skills/moat-review/SKILL.md` | **v2.0 已定案**（唯讀，我沒有動它） | 開頭「# moat-review v2.0（2026-09-22 定案：三個關鍵問題）」，120 行；三問四樣東西＋示範（NVDA 三題＋錯的出題法）＋流程表（4 步：蒐證／查證＋出題(sonnet)／檢查(opus 唯讀)／把關(程式)）＋moat-v3 schema，都在檔案裡，本檔是唯一權威來源。 |
| `scripts/moat_pipeline.py` | **已照 v2.0 全部重寫**，語法已驗證（`ast.parse` 過），**還沒實際跑過一次** | 三步 LLM 改成：sonnet 查證＋出題（一通、帶 WebSearch/WebFetch、`--json-schema`，prompt 附 SKILL「示範」整節）→ opus 只讀檢查（四題 q_specific_ok/why_mechanism_ok/lean_consistent_ok/watch_observable_ok，任一 false 帶 notes 重出一次，再 false 不落檔記 `_failures.json`）→ 程式把關（`check_moat_review.py`）。已刪掉 judge／write／score 相關函式與 `--judge-model` 旗標。輸出 `moat-v3` schema。保留 `--out-dir`（測試用，非正式指令不需要）。CLI 用法見檔頭 docstring：`python3 scripts/moat_pipeline.py NVDA,TSM,AMD,MSCI --mode init --concurrency 2`。 |
| `scripts/check_moat_review.py` | **已照 v2.0 全部重寫**，語法已驗證，邏輯未經真實資料測試 | 驗 `moat-v3`：schema／status(初出\|已重出)／one_liner_zh 非空／questions 恰 3 題且四樣東西齊／每條 evidence 要有 date 或文字含「未能確認」／lean∈{撐住,鬆動,不明}／每題 watch≥1 且 metric_key 或 manual＝true／禁買賣語／正文禁「DD」與對手 ticker／全形標點（僅警告）。**沒有測過任何真實 pose JSON**，第一次真的跑 moat_pipeline.py 時才會知道欄位對不對得起來（例如 sonnet 出的 JSON 鍵名跟 check 預期是否完全一致）。 |
| `scripts/build_stock_dash.py` | **尚未開始改，仍是舊版（moat-v2）** | `MOAT_HURDLE_RATE_PCT`／`METRIC_KEY_RESOLVERS`（約行 2777-2938）、`update_moat_conditions`、`compute_review_due_v2`、`build_moat_changes_table`、`build_moat_rival_comparison`、`build_card_moat` 都還在讀 `current.q3_review.conditions`／`current.score`／`current.width`／`current.trend`／`current.judgment_date`，這些欄位在新的 `moat-v3` 文件裡**不存在**（新結構是 `current.questions[].watch[]`、`current.date`、沒有 score/width/trend）。`compute_version_snapshot`（約行 2998-3030）與 `check_version_triggers`（約行 3033 起，T3 那組 key）也還在讀 `moat_score`/`moat_width`/`moat_trend`。**這支腳本目前完全沒碰**，還能正常跑（因為 moat/{T}.json 也還是舊版），但只要 moat_pipeline.py 一旦被拿去對正式檔跑一次，這裡就會全部讀不到欄位、`build_card_moat` 會整段炸掉或吐 None。**下一步必須先改這支才能碰任何一檔正式資料。** |
| `docs/stock-dash/` 頁面（scratch 片段＋assemble） | **尚未開始改，仍是舊版一畫面** | 片段檔在舊 session 的 scratchpad：`/private/tmp/claude-501/-Users-ivanchang/7e202424-1296-458d-a9b2-07a1fa5a4666/scratchpad/`（`_idx_moat_body.txt`／`_idx_moat_js.txt`／`_shared_js2.txt`／`_appendix_js2.txt`／`_idx_css.txt`／`assemble_prod.py`）。現況是 v1.0 設計：分數卡＋三段 prose＋條件表＋收合證據區，都在讀 `moatCurrent.score/width/trend`、`q1_shape.prose_zh` 等舊欄位。**還沒有任何新版三題卡片的 HTML/CSS/JS**，一行都沒動。`docs/stock-dash/index.html`／`full.html` 本身（78KB／6KB，mtime 09-22 15:05）也是照舊版產物，跟目前的 moat/{T}.json（舊版）一致，可以正常瀏覽，沒有壞。 |
| `docs/stock-dash/data/moat/{NVDA,TSM,AMD,MSCI}.json` | **全部還是 `schema: moat-v2`**（判斷制，非三題制），`date`（欄位其實叫 `judgment_date`）都是 `2026-09-22` | 這是**上一輪**（sonnet 判斷＋opus 把關的 v1.1 判斷制）留下的正式檔，**完全沒被本輪動過**。`_failures.json` 目前不存在／空。 |

## ② 四檔 schema 版本（明確回答）

`NVDA.json`／`TSM.json`／`AMD.json`／`MSCI.json` 四檔**都是 `"schema": "moat-v2"`**（score/width/trend 判斷制），沒有任何一檔是 `moat-v3`。三題制目前只存在於程式碼裡，**還沒有任何一檔資料被跑過新 pipeline**。

## ③ 已知 bug／未完成項

1. **`check_moat_review.py` 完全沒跑過真實資料**——`moat_pipeline.py` 產出的 JSON 鍵名（如 `q_zh`/`why_zh`/`text_zh`/`desc_zh`）跟 check 腳本預期的鍵名是我同一次重寫時手動對齊的，理論上一致，但沒有拿真的 sonnet 輸出驗證過，第一次跑 `--dry-run` 之後、**跑一次真的 `--mode init`（單一檔，不用 concurrency）先看 check 結果**再batch。
2. **`build_stock_dash.py` 完全沒改**——這是最大的斷點。只要 `moat_pipeline.py` 寫出一份 `moat-v3` 檔到正式 `docs/stock-dash/data/moat/`，下一次 `build_stock_dash.py {T}` 就會在 `update_moat_conditions`／`compute_version_snapshot` 這些函式讀不到 `q3_review`/`score` 等舊欄位而出錯或吐錯的值。**順序務必是：先改完 build_stock_dash.py 的 moat 相關函式（見上表列的函式與行號），再跑 moat_pipeline.py 覆蓋正式檔，最後才 rebuild。**
3. **頁面完全沒改**——就算資料與 build 腳本都改完，頁面 JS 還是照舊版欄位渲染，會整章空白或 JS 報錯（`moatCurrent.score` 是 `undefined`）。順序上頁面可以跟 build_stock_dash.py 平行改，但都要在正式資料被覆蓋、要 rebuild 之前完成，否則會有一段時間頁面是壞的。
4. **`--out-dir` 旗標保留但這次沒被要求用**——與舊 A/B 架構（`--judge-model`/`--reuse-evidence`）已一併刪除，因為新架構查證＋出題是同一通，沒有「只換判斷模型」或「重用查證」的概念了。
5. **dd-screener FunnelRank 護城河層**——SKILL v2.0「下游」段明講「不再有護城河層」，但 FunnelRank 的產生腳本不在本任務允許碰的檔案清單裡（只能動 `moat_pipeline.py`／`check_moat_review.py`／`build_stock_dash.py`／`docs/stock-dash/`），**這件事完全沒有處理，需要另外排一個任務**去改 FunnelRank 那條線（很可能是 `scripts/build_dd_screener.py` 或類似檔案，本次沒有去確認確切位置）。
6. 上一輪（A/B 比較，已於更早的暫停指令中止）留下的殘檔：`_build/moat_ab_opus/NVDA.json`（完整）＋`_build/moat_pipeline_agents/{AMD,NVDA,TSM}_judge.json`／`{NVDA,TSM}_write_1.json`（半成）——這些是舊判斷制 A/B 的殘留，跟本輪三題制無關，沒有清掉（指示是「已跑完的保留檔案不刪」），之後若要清理可以直接刪 `_build/moat_ab_opus/`。

## ④ 重跑指令（下一個 session 接手時，建議順序）

```bash
# 0. 先把 build_stock_dash.py 的 moat 相關函式改完（見②表格列的函式名／行號），
#    否則下面第 2 步一 rebuild 就會炸。頁面片段（scratchpad 那幾個 _idx_moat_*.txt）
#    也建議在這時候一起改完。

# 1. 單檔 dry-run 看 prompt 組得對不對（不花錢）
python3.12 scripts/moat_pipeline.py NVDA --mode init --dry-run

# 2. 單檔真的跑一次，先看 check_moat_review 過不過、gate 有沒有正常重試
python3.12 scripts/moat_pipeline.py NVDA --mode init

# 3. 確認 docs/stock-dash/data/moat/NVDA.json 變成 schema=moat-v3、check 通過後，
#    再一次跑其餘三檔（可 concurrency）
python3.12 scripts/moat_pipeline.py TSM,AMD,MSCI --mode init --concurrency 2

# 4. rebuild 四檔頁面（此時 build_stock_dash.py 必須已經改完，見③-2）
python3.12 scripts/build_stock_dash.py NVDA
python3.12 scripts/build_stock_dash.py TSM
python3.12 scripts/build_stock_dash.py AMD
python3.12 scripts/build_stock_dash.py MSCI

# 5. 照舊流程重組頁面（assemble_prod.py → site_nav → qc.py → node --check →
#    瀏覽器驗證桌面＋390px手機＋console乾淨），驗完立刻關 server／分頁
#    （機器記憶體吃緊，這是整個任務從頭到尾的鐵律）。
```

**不要用 `--all-dd` 或大 concurrency 直接對全站跑**——先用 NVDA 一檔把 pipeline／check／build_stock_dash／頁面四段全部串起來驗證過一次，再處理其餘三檔，避免同一個結構性 bug 複製四遍還要重花四次 LLM 費用。
