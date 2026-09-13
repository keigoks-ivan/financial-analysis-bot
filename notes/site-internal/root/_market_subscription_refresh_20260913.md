# 市況與情報自動更新：訂閱版第一階段

2026-09-13。後續已啟用 Codex 本機每天 17:15 的更新與第二意見草稿排程，需要電腦及 App 運行；Claude 雲端排程仍未配置。新增來源的實測與待完成事項見 [_market_source_implementation_20260913.md](_market_source_implementation_20260913.md)。本輪沒有呼叫研究模型、修改線上資料、提交或推送，尚未核實帳戶額外用量設定。

持有人後續已授權重新選擇資料來源。本文「沿用既有來源」只描述第一階段程式現況，後續資料範圍改以 [`_market_source_expansion_20260913.md`](_market_source_expansion_20260913.md) 為準；可新增或替換來源、回補歷史並調整資料架構。

## 這一版解決什麼

`/intel/` 保存事件與情報；`/market/` 用同批證據解釋市況、比較前期並列出情境與反證。Python 保存和核對資料，訂閱模型負責推理。保留既有 market-read-v1、預測帳簿與後續結算，不另造評分系統。

目前來源並不涵蓋金融市場的所有訊號，也沒有完整的歷史判讀快照。這一版先修正日期混用、更新失敗仍顯示成功，以及無法重現歷次分析的問題。現存舊判讀不會被補上當時未保存的數字。

資料流程：官方來源增量接入＋既有上游資料 → build_market_state → market_refresh record → 固定證據快照與發布包 → Claude 訂閱排程 prepare → 新判讀與獨立冷讀 → 機械驗證 → 命題落帳 → accept → 由具放行權的 Claude 流程發布。

## 執行與費用

- GitHub Actions 只新增零模型的版本保存步驟。既有情報流程的 Haiku 分類、Sonnet 摘要及其排程仍沿用，這輪沒有重複增設情報模型任務。
- 市況綜合判讀交給 Claude Code cloud routine，建議台北每日 17:15 檢查一次。`prepare` 在證據版本相同時回傳 `run_analysis=false`；不同時才進研究。週一 `mode=weekly`，重查前期假設與跨資產矛盾。這版沒有常駐即時新聞監控。
- 較便宜的模型處理抽取、分類、格式和單元測試。主判讀保留足以處理跨資產因果的模型；冷讀必須是不同模型、獨立上下文。省額度靠增量更新，不以刪掉反證或縮短來源補足。
- 使用帳戶的訂閱登入，關閉額外用量／額外付費，不設 API key 備援。程式的 `billing=subscription_only` 是流程聲明，不能代替帳戶計費設定的核實。耗盡額度即停止模型批次，保留待重評狀態，下一班恢復後續工作。
- 不額外購買金融數據不等於所有數據免費或即時。沿用來源的授權、頻率與缺值限制；Actions 與網站託管也有各自用量。
- 如果改用 ChatGPT 訂閱中的 Codex 本機 automation，資料與合約可原樣使用，但電腦及 App 必須保持運行。不得將本機自動化寫成關機也保證執行。

能力依據：[Claude routines](https://code.claude.com/docs/en/routines)、[Codex automations](https://learn.chatgpt.com/docs/automations?surface=app)、[Codex pricing](https://learn.chatgpt.com/docs/pricing)。啟用時需再確認當下方案與帳戶權限。

## 儲存合約

| 位置 | 用途 |
|---|---|
| `docs/market/data/snapshots/<snapshot_id>.json` | 固定證據，包含 state 和當日情報摘要；歷史版本不覆寫 |
| `.dd_build/market-refresh/<snapshot_id>/evidence.json` | 模型本次唯一市況證據包；prepare 不改發布目錄 |
| 同目錄 `request.json` | 上次判讀、前版雜湊、資料缺口、期間變化與 daily／weekly 模式 |
| 同目錄 `candidate.json` | 新判讀草稿，尚未驗收不得寫入 read.json |
| `docs/market/data/releases/<release_id>.json` | 同批 state、read、refresh、判讀歷史與期間比較 |
| `docs/market/data/refresh.json` | 最後才切換的發布指標；頁面由此載入一包內容 |

`snapshot_id` 依資料內容生成，排除生成時間與舊判讀標題。`record` 保留舊判讀，狀態標示 `needs_review`；`accept` 通過後才存新判讀及其 `evidence_snapshot`。來源有缺口時即使通過也顯示 `degraded`。不會因為存檔成功就宣稱研究完整。

期間比較提供 7、30、90、365 天，從目標日之前最多七個曆日的已保存快照選基準，畫面顯示實際基準日。找不到就顯示資料不足。這是資料比較，不是回填歷史預測，也不替代後續的長期時間序列研究。

主要行情日以 `monitor:sp500` 的來源日期核對，不能只看 state 的合成日。來源缺失、日期超前或行情超過四個曆日會阻止新版本發布；長假誤擋的調整條件已登記 rule ledger。次要來源偏舊則揭露缺口，不能拿當日日期覆蓋。

## 可貼入 Claude routine 的任務

> 在 financial-analysis-bot 的最新主分支執行市況增量研究。遵守 AGENTS.md、market-read 既有分析合約及本文件的版本流程。只用本帳戶訂閱額度，沒有 API 或額外用量備援。額度耗盡、輸入缺失、數字不一致或審核未通過就停止，不要換 API、不改舊判讀日期、不繞過驗證。
>
> 先確認資料工作目錄乾淨且沒有另一個市況研究正在發布，先執行 `python3 scripts/market_sources.py collect --write`（金鑰檔存在時加 `--env-file .env.market_sources`），再執行 `python3 scripts/build_market_state.py --out .market_sources/state.json`，接著執行 `python3 scripts/market_refresh.py prepare --state .market_sources/state.json`。讀 stdout 指出的 run_dir 內 evidence.json 和 request.json。run_analysis=false 就結束本輪；errors 非空就回報來源失敗，不研究。沒有歷史基準時，只列目前證據，明確表示不能做完整期間比較。
>
> 以這一包證據、用戶筆記和預測帳簿為依據研究。按照 AGENTS 的先讀後裁協議查詢相關知識，不覆寫用戶筆記。便宜模型可抽取或整理，最終判讀者自己閱讀關鍵原文及反證。若額外搜尋提供了新數字，先透過正常資料來源補入新批證據並重新 prepare；不可把未保存的數字塞進觀察值冒充已驗證。
>
> 在 run_dir 寫 candidate.json，沿用 market-read-v1 全部必要欄位，並加入下節欄位。明確交代相較前期哪些證據改變、哪些結論未變，以及基準、偏強、偏弱情境的條件、反證與跨資產影響。weekly 模式重讀假設、來源缺口和已結算結果。不能以多個同源指標當成多份獨立證據；沒有可校準依據的情境機率不要編數字。
>
> 對定稿計算 fingerprint，交不同模型在獨立上下文冷讀 evidence.json 和 candidate.json。審核結果存到 review，包含模型、snapshot_id、content_hash、verdict 與 findings。任何數字口徑疑慮都 blocking=true。正文修改後重新計算指紋並重審，最多修補一次；仍不合格交回 Claude 主 session。
>
> 依下列驗收順序執行。全部通過後，依 AGENTS 的放行權限決定是否提交指定產物。推送前若資料或判讀已被更新，重新準備與驗證，不覆蓋較新成果。不得廣域 git add。回報本批版本、來源日、判讀日、缺口、模型用量、命題數及實際發布結果。

## 草稿新增欄位

```json
{
  "snapshot_id": "取自 request.json",
  "billing": "subscription_only",
  "vs_prior_zh": "哪些證據或推論相較前期改變；第一份需說明無可比快照。",
  "data_gaps_zh": "資料缺口與對結論的限制。",
  "observations": [
    {"ref": "monitor:sp500", "field": "num", "value": 100, "as_of": "2026-09-13"}
  ],
  "scenarios": [
    {"name_zh": "基準", "horizon": "3m", "conditions_zh": "成立條件。", "falsifiers_zh": "會推翻的證據。", "asset_implications_zh": "股、債、匯與商品的影響。", "refs": ["monitor:sp500"]}
  ],
  "review": {
    "model": "實際冷讀模型",
    "snapshot_id": "同一批版本",
    "content_hash": "fingerprint 輸出",
    "verdict": "pass",
    "findings": []
  }
}
```

上例是欄位示意，不是市場數據或完整合格草稿。每個被引用的數字都要在 observations 帶相同欄位值與來源日，允許 num、pctile、chg30_pct、z。程式核對結構化數字，不保證能偵測正文所有算術與因果錯誤，這是獨立冷讀的責任。模型名稱與審核聲明本身不是身分驗證，需保留真正的分開執行紀錄。

## 驗收順序

以下 `<run_dir>` 必須替換成 prepare 輸出的實際路徑。執行環境設台北時區，避免既有 ledger CLI 的當地日期與排程日期不同。

```bash
python3 scripts/market_refresh.py fingerprint --candidate <run_dir>/candidate.json
python3 scripts/market_refresh.py validate --candidate <run_dir>/candidate.json
TZ=Asia/Taipei python3 scripts/ledger_from_editorial.py --source market-read --file <run_dir>/candidate.json
TZ=Asia/Taipei python3 scripts/ledger_from_editorial.py --source market-read --file <run_dir>/candidate.json --write
python3 scripts/market_refresh.py accept --candidate <run_dir>/candidate.json
python3 scripts/market_refresh.py accept --candidate <run_dir>/candidate.json --write
```

先補上真正的冷讀結果才執行 validate。ledger 乾跑有拒絕就停止，不能略過；正式落帳後核對 `claim_ids`，按既有合約附上 horizon／falsifier 連結。accept 會重新核對帳簿的命題、機率、期限和結算條件，不允許畫面與帳簿機率不同。舊 ledger 的 30 天文字查重仍保留：真正的新日期／到期日要寫清楚；同日完全相同且已落帳的命題可核對後沿用原 id，不用改寫句子逃過查重。若命題有改變但無法正常落帳就交回處理。

accept 乾跑不改資料，`--write` 才保存新判讀及發布包。命題帳簿與網站不是跨系統交易：落帳後若 accept 失敗，保留落帳的稽核軌跡和草稿，重跑時核對原 id，不刪帳洗掉失敗。

## 啟用前的最後交接

1. Claude 主 session 審閱本輪 diff 與檢查結果，保留其他 session 的修改。依目前 repo 規則，Codex 不具放行權。
2. 在已登入的 Claude Code cloud 確認訂閱、額外用量關閉、repo 權限與環境可執行所需腳本。找到既有 market-read routine 並更新其任務，不另建重複排程；原本「同日一律跳過」的舊 trigger 改以本文件 prepare 的版本判斷為準。
3. 核准並發布本輪精確檔案。上游 Actions 完成後會保存證據版本，17:15 routine 消費新版本。保留原上游頻率，待量測用量後再合併重複情報 cron，這輪不盲停其他研究任務。
4. 在隔離目錄先做一次真正的訂閱研究驗收，核對帳戶用量、引用、冷讀與預測帳簿。通過後才授權 routine 的正式發布步驟。排程下次成功執行並在網站看見新版本，才算啟用完成。

目前尚未完成的研究改造：歷史價格序列回補、事件故事線的分群／拆線、完整來源覆蓋矩陣、跨資產情境的校準與例外事件喚醒。這些需要獨立驗收；本輪不宣稱已完成「全市場所有訊號」或已證明預測有效。

## 本輪程式與驗證交接

- 新增 `scripts/market_refresh.py`：make_snapshot／history_rows 保存證據，prepare／period_comparisons 做版本及期間比較，quality 核對來源日，candidate_hash／validate_candidate 核對冷讀與帳簿，publish／locked_publish 同批切換並防止舊程序覆寫新判讀。
- `scripts/intel/llm.py`：run_claude 的額度失敗辨識及 Ledger 的整批停止；`scripts/intel/run_daily.py`：_llm_status／build_output 改以實際失敗標示 degraded。
- `docs/market/index.html`：不可變發布包讀取、時間分層、資料缺口、期間比較、情境與前期差異；最新數值不再帶入舊判讀日的引用說明。
- `.github/workflows/market-state-daily.yml`：上游成功後觸發零模型版本保存，只提交指定產物；未在本輪實際執行。
- `knowledge/rule_ledger.md`：只追加 2026-09-13 區段；同檔已有其他 session 的修改，提交時不得整檔一併放行。
- 新增兩份測試：test_market_refresh.py、test_intel_subscription_status.py，涵蓋錯批證據、過時行情、正文改動後舊審核、到期日／帳簿不一致、歷史不足、並行覆寫，以及額度耗盡與正常文本誤判。

驗證：兩份新增測試合計 26 項；Python 3.9 AST、YAML 解析、前端 JS 解析及頁面離線 mock 通過。本機瀏覽器已使用真實舊判讀與目前資料的暫存發布包確認時間分層及歷史不足。QC 為零 errors；rule_ledger.md 第 43、44、47 行有三項既有半形標點 warning，本輪新增段落沒有警告。

全套 `python3 -m pytest scripts/tests -q` 在改動前後都於收集階段失敗：test_build_live_scoreboard_combined_twd 匯入既有 site_nav.py 第 206 行時，Python 3.9 不接受 f-string expression 內的反斜線。這不是本輪引入；未擴大修改其他 session 的程式。Python 3.12 環境未裝 pytest，本輪未安裝依賴或聲稱全套通過。

已追蹤且由本輪單獨修改的四檔，`git diff --stat` 如下。另新增 market_refresh.py、兩份測試與本文件；rule ledger 只追加上述 2026-09-13 區段，不能將它其他未提交變更算成本輪成果。

```text
 .github/workflows/market-state-daily.yml |  14 +-
 docs/market/index.html                   | 353 +++++++++++++++++++++++++------
 scripts/intel/llm.py                     |  80 ++++++-
 scripts/intel/run_daily.py               |  15 +-
 4 files changed, 389 insertions(+), 73 deletions(-)
```
