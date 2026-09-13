# 市況資料接入與自動更新：實作驗收

2026-09-13。這份記錄實際執行結果，候選來源清單不能當成已完成接入。

已登錄 51 條序列：43 條正常、2 條部分歷史、6 條待免費金鑰或聯絡設定。共保存 51,356 筆觀測，含不同序列重複追蹤同一概念，不能當成獨立證據數。歷史與修訂存在 `data/market_sources/series/`，沒有使用測試資料填補缺口。

## 尚未完成

- TWSE 指數與成交金額已保存 2016-01 至 2019-08 的 44 個月檔，各 896 筆。後續請求回傳 HTTP 428，降至每五秒一個月檔仍未恢復。狀態為 partial_history，日更會從進度續傳，未宣稱完整十年。當前加權指數另外由 OpenAPI 取得，日期 2026-09-11。
- 缺 FRED_API_KEY（兩條 ALFRED 修訂序列）、BEA_API_KEY、EIA_API_KEY，以及 SEC_USER_AGENT（真實聯絡識別，兩條公司資本支出）。接入程式與離線測試已完成，尚無真實 API 驗收。填入根目錄 `.env.market_sources`，可參照 `market_sources.env.example`；私人檔已 gitignore。
- TPEx 的憑證鏈驗證失敗，未關閉 TLS 驗證。generic adapter 已測試，但尚無正式啟用序列。PBOC／NBS 官方直連未接入，BIS 中國信貸不能代替中國所有總經指標。
- 盈餘共識、完整選擇權曲面與可靠資金流仍有缺口。本輪保留既有新聞故事線與預測結算，沒有宣稱情境機率已校準，也沒有重寫公開投資結論。

## 自動更新

Codex 本機 heartbeat 已建立並核對為 ACTIVE：`市況與情報每日更新`，每天台北 17:15，id 為 `automation`。需電腦及 App 運行，關機不保證執行。第一輪完整訂閱分析尚未執行，建立排程不等於研究驗收成功。

任務走 collect → 私人 state → prepare → 按 snapshot_id 決定是否寫第二意見草稿。來源失敗保留舊資料並揭露缺口，同批草稿完成後跳過。模型不使用 Claude／OpenAI API key，額度耗盡停止，不自行開啟額外付費；帳戶額外用量設定尚未核實。

GitHub Actions 的零模型資料接入與版本保存已改好，尚未提交／發布，因此遠端仍跑原版。Claude 雲端 routine 仍需重新登入。依 AGENTS.md，Codex 沒有放行權，本輪不 commit／push。

## 檔案與操作

| 檔案 | 用途 |
|---|---|
| `data/market_source_registry.json` | 序列、單位、頻率、地區、研究類別與更新間隔 |
| `scripts/market_sources.py` | 接入、歷史與修訂、增量回補、來源狀態、期間比較 |
| `scripts/market_sources_us.py` | FRED／ALFRED、OFR、Cboe、CFTC、NY Fed |
| `scripts/market_sources_economy.py` | BLS、BEA、EIA、SEC、Fiscal Data |
| `scripts/market_sources_global.py` | ECB、BIS、BOJ、TWSE、TPEx、TAIFEX |
| `scripts/build_market_state.py` | source:* 證據與來源缺口合成 |
| `scripts/market_refresh.py` | 固定證據、期間比較、冷讀與帳簿核對、發布包 |
| `docs/market/index.html` | 日期分層、來源狀態、類別及期間篩選、前期判讀與情境 |
| `scripts/intel/render.py` | 情報今日頁顯示官方資料日期與缺口，封存不混入目前值 |

```bash
python3 scripts/market_sources.py collect --write
python3 scripts/market_sources.py collect --env-file .env.market_sources --write
python3 scripts/market_sources.py collect --only fred_cpi --backfill --write
python3 scripts/build_market_state.py --out .market_sources/state.json
python3 scripts/market_refresh.py prepare --state .market_sources/state.json
```

collect 不呼叫模型、不提交、不推送；沒有 --write 就不保存。首次從 2016-01-01 回補，平日重疊增量，每月首日完整複查。實際可得歷史可能較短：高收益利差公開 CSV 約三年，SOFR 自 2018 年，期交所公開資料為有限期間。

原始回應與收據放 `.market_sources/raw/`，金鑰去除後保存 SHA256。本機可查原始檔；Actions runner 的 raw 是暫存，沒有永久雲端歸檔。整理後的觀測值與修訂為研究底稿，發布層只讀摘要。「當時已知值」只能用有版本日期的 ALFRED／申報或開始保存後的快照，不能拿最新修訂歷史代替。

## 審查與驗證

WRESBAL／WTREGEN 已核對為百萬美元。OFR REPO-DVP_AR_G30-P 是 DVP 超過 30 日附買回成交加權利率初值。BIS CG_DTYPE A 是信貸／GDP，B 是趨勢，C 是差額，只接完整 C key。CFTC TFF 欄位與分項 COT 不同，已依真實 JSON 修正。Cboe VVIX／OVX／GVZ 真實 CSV 使用各自名稱作欄名，未採納第二意見中一律改 CLOSE 的建議。

專項測試涵蓋失敗保留、A→B→A 修訂、日期與單位、ALFRED 版本、SEC 期間、官方分頁、BIS 混序列、BOJ 陣列、TWSE 續傳、原始雜湊，以及訂閱額度停止與證據驗收。79 項專項測試通過。瀏覽器已驗證來源連結、類別與一年期篩選，並修正來源名稱欄寬及歷史起點顯示。

全套 scripts/tests 在既有 scripts/site_nav.py:206 的 Python 3.9 f-string 語法錯誤處中止收集。本輪沒有改該檔，也沒有宣稱全套通過。

## Actual series coverage

| Series | Status | First | Latest | N |
|---|---|---|---|---:|
| fred_cpi | ok | 2016-01-01 | 2026-08-01 | 127 |
| fred_core_cpi | ok | 2016-01-01 | 2026-08-01 | 127 |
| fred_pce | ok | 2016-01-01 | 2026-07-01 | 127 |
| fred_core_pce | ok | 2016-01-01 | 2026-07-01 | 127 |
| fred_payrolls | ok | 2016-01-01 | 2026-08-01 | 128 |
| fred_unemployment | ok | 2016-01-01 | 2026-08-01 | 127 |
| fred_claims | ok | 2016-01-02 | 2026-09-05 | 558 |
| fred_real_gdp | ok | 2016-01-01 | 2026-04-01 | 42 |
| fred_industrial_production | ok | 2016-01-01 | 2026-07-01 | 127 |
| fred_retail_sales | ok | 2016-01-01 | 2026-07-01 | 127 |
| fred_treasury_2y | ok | 2016-01-04 | 2026-09-10 | 2673 |
| fred_treasury_10y | ok | 2016-01-04 | 2026-09-10 | 2673 |
| fred_breakeven_10y | ok | 2016-01-04 | 2026-09-11 | 2674 |
| fred_hy_spread | ok | 2023-09-12 | 2026-09-10 | 787 |
| fred_fed_assets | ok | 2016-01-06 | 2026-09-09 | 558 |
| fred_bank_reserves | ok | 2016-01-06 | 2026-09-09 | 558 |
| fred_treasury_account | ok | 2016-01-06 | 2026-09-09 | 558 |
| fred_reverse_repo | ok | 2016-01-04 | 2026-09-11 | 2666 |
| fred_dollar | ok | 2016-01-04 | 2026-09-04 | 2663 |
| fred_oil | ok | 2016-01-04 | 2026-09-09 | 2673 |
| cboe_vix | ok | 2016-01-04 | 2026-09-11 | 2721 |
| cboe_vvix | ok | 2016-01-04 | 2026-09-11 | 2688 |
| cboe_ovx | ok | 2016-01-04 | 2026-09-11 | 2686 |
| cboe_gvz | ok | 2016-01-04 | 2026-09-11 | 2686 |
| nyfed_sofr | ok | 2018-04-02 | 2026-09-10 | 2109 |
| ofr_repo_g30 | ok | 2018-05-08 | 2026-09-10 | 1951 |
| cftc_spx_lev_long | ok | 2016-01-05 | 2026-09-08 | 558 |
| cftc_spx_lev_short | ok | 2016-01-05 | 2026-09-08 | 558 |
| cftc_wti_mm_long | ok | 2016-01-05 | 2026-09-08 | 558 |
| cftc_wti_mm_short | ok | 2016-01-05 | 2026-09-08 | 558 |
| ecb_eurusd | ok | 2016-01-04 | 2026-09-11 | 2738 |
| ecb_deposit_rate | ok | 2016-01-01 | 2026-09-13 | 3909 |
| twse_taiex | ok | 2026-09-11 | 2026-09-11 | 1 |
| taifex_putcall_oi | ok | 2026-08-12 | 2026-09-11 | 23 |
| taifex_putcall_volume | ok | 2026-08-12 | 2026-09-11 | 23 |
| bls_cpi | ok | 2016-01-01 | 2026-08-01 | 127 |
| bea_real_gdp_growth | blocked_credentials | None | None | 0 |
| eia_crude_stocks | blocked_credentials | None | None | 0 |
| sec_msft_capex | blocked_credentials | None | None | 0 |
| sec_amzn_capex | blocked_credentials | None | None | 0 |
| boj_tankan_manufacturing | ok | 2016-01-01 | 2026-04-01 | 42 |
| fiscal_public_debt | ok | 2016-01-04 | 2026-09-10 | 2684 |
| fiscal_total_debt | ok | 2016-01-04 | 2026-09-10 | 2684 |
| bis_credit_gap_cn | ok | 2016-01-01 | 2025-10-01 | 40 |
| bis_credit_gap_us | ok | 2016-01-01 | 2025-10-01 | 40 |
| bis_credit_gap_jp | ok | 2016-01-01 | 2025-10-01 | 40 |
| bis_credit_gap_hk | ok | 2016-01-01 | 2025-10-01 | 40 |
| alfred_cpiaucsl | blocked_credentials | None | None | 0 |
| alfred_payems | blocked_credentials | None | None | 0 |
| twse_taiex_history | partial_history | 2016-01-04 | 2019-08-30 | 896 |
| twse_turnover_history | partial_history | 2016-01-04 | 2019-08-30 | 896 |

## 交付核對

Python AST、內嵌 JavaScript 語法、工作流 YAML 與改動空白檢查均通過。QC 掃描 19 檔，0 errors／0 warnings。79 項專項測試通過，另有既有 LibreSSL 相容性警告。市場頁已以真實資料包在本機瀏覽器核對；情報來源區塊已做轉義與日期呈現測試，未執行完整情報發布流程。

主要新增或更動函式：

- `market_sources.py`：`HttpClient`、`load_credentials`、`validate_registry`、`merge_observations`、`current_observations`、`summarize_series`、`collect`；三個 adapter 模組負責官方回應解析。
- `market_refresh.py`：`make_snapshot`、`quality`、`prepare`、`validate_candidate`、`make_release`、`publish`、`locked_publish`。
- `build_market_state.py`：`attach_source_evidence`、`print_evidence_pack`、`main`。
- `intel/llm.py`：`_is_quota_exhausted`、`Ledger.record_failure`、`Ledger.trip_quota`、`run_claude`；`intel/run_daily.py`：`_llm_status`、`build_output`。
- `intel/render.py`：`render_official_sources`、`build_day_body`；市場頁新增來源覆蓋、日期分層、期間比較、情境及一致版本載入。

以下是本任務七個既有檔案的 git diff --stat。新增程式、測試、來源註冊表、實際歷史資料和交接文件仍為 untracked，不包含在這個統計內。`knowledge/rule_ledger.md` 有其他 session 的修改，本輪僅追加市況證據驗收規則與撤銷條件，不能整檔視為本輪產物。

```text
 .github/workflows/market-state-daily.yml |  27 +-
 .gitignore                               |   4 +
 docs/market/index.html                   | 554 +++++++++++++++++++++++++++----
 scripts/build_market_state.py            |  41 ++-
 scripts/intel/llm.py                     |  80 ++++-
 scripts/intel/render.py                  |  31 ++
 scripts/intel/run_daily.py               |  15 +-
 7 files changed, 667 insertions(+), 85 deletions(-)

```

Claude 主 session 接手時，先審這份清單與專項 diff，提供缺少的免費資料設定，再完成第一輪訂閱研究、獨立冷讀與發布驗收。既有市場上游停更項目仍須恢復；重建 state 不會更新那些上游數字。未經這些步驟，不應宣稱網站已全面自動更新或研究機率已驗證。

## 2026-09-13 驗收與首次發布（Claude 主 session）

接手審查後實際完成的事，逐項對應前文「尚未完成」：

- **資料層修正三處**（審查 agent 發現，已補測試）：BEA 季／年觀測日改為期間首日（原用季底，與 FRED 同季不同日）；`current_observations` 對 `latest_revised` 且兩版都帶發布日的序列（EIA）改依發布日取新版，不再靠附加順序；分位摘要新增 `percentile_from`（分位樣本實際起點）與無觀測時的明示 null，短歷史（高收益利差三年、台指期權一個月）不再被讀成十年分位。專項測試 79 → 81 項通過。
- **TWSE 歷史回補完成**：兩條 FMTQIK 序列以既有續傳＋五秒限速從 2019-09 接到 2026-09-11，各 2,606 筆，未再遇 428；51 條中 45 條正常、6 條待金鑰。
- **停更上游根因**：`intel-2-daily.yml` 的週日段用起跑當下的 UTC 星期判斷，排程自 08-24 起連續被延到週一 00:0x UTC 起跑，`IS_SUNDAY` 永遠 false，crowding／regime／catalyst／kill-watch 停更四週。本輪手動 dispatch `crossasset-weekly.yml` 補回 COT（9/8）與 regime；並把週日段判斷改為「UTC 週日，或週一 06:00 UTC 前起跑」（另一 commit）。
- **來源分歧一例**：站內 `internals:cpi_yoy` 3.71% 是 13 個月變化（334.131／322.169），官方序列 12 個月年增 3.35%；判讀改以官方序列為錨，機械層那欄不引用（`build_monitor_internals.yoy_series` 的 12 期回看在序列缺月時會錯位，屬另一 owner，未修）。
- **首輪研究**：固定證據 snapshot `632d83e4…`（state 合成日 2026-09-12、主要行情 2026-09-11、情報 2026-09-12）；判讀 as_of 2026-09-13，判讀者 Fable，獨立冷讀 Opus 四輪（2 🔴＋16 🟡 → 7 🟡 → 3 🟡 → 0），機械 critic 10 PASS／0 WARN，八張命題落帳 `fc_20260913_ed_01`–`08`（含哨兵），accept 狀態 `degraded`（九條缺口已揭露），發布包 `releases/4145a02d…`。
- **未做**：判讀快照無前期可比（第一份），7／30／90／365 天比較全部來自官方序列；六條待金鑰序列本機與 GitHub Secrets 皆未設定；`docs/market/data/state.json` 的估值緩衝磚仍顯示上期 22.7 倍（state 在 accept 前建成，下一班次自動改用 22.5）。
- **測試**：`scripts/site_nav.py` 兩處 f-string 反斜線改為先算好片段（Python 3.9 相容、輸出逐字相同，另一 commit）後，全套 `python3 -m pytest scripts/tests` 在 3.9 下 557 項通過；`test_build_live_scoreboard_combined_twd.py` 仍因 `scripts/update_long_track_w52_adaptive.py:994` 的執行期 `type | None` 於 3.9 無法收集，不在本任務範圍、未修。
