# 記憶鏡像（跨 session 專案級背景）

- **鏡像日期**：2026-07-09
- **來源**：`~/.claude/projects/-Users-ivanchang-financial-analysis-bot/memory/MEMORY.md`（單一工具的私有記憶目錄，一行一條索引；每條細節在同目錄的 `{filename}.md`）
- **為何鏡像**：這些跨 session 背景目前只存在某一工具的私有目錄，換 agent 工具就丟。鏡像進 repo 讓任何 agent 讀得到。
- **更新方式**：人工／session 定期重鏡像（來源檔更新後重跑）。此檔是**唯讀鏡像**，真相仍在來源 memory 檔；有分歧以來源為準。
- **範圍**：只搬**專案級結論**（系統架構決策、退役記錄、校準結論、pipeline 現況）＋少數影響產出設計的規範。**排除**純個人偏好／溝通風格／skill 內部補丁類條目（那些留在來源 memory）。
- 每條格式：一行摘要 ` ⟵ `原始 memory 檔名（追溯用）。

## 系統架構與參考

- research.investmquest.com 由四個 repo 共同生成 `docs/`；主 repo 只擁有部分，整站樣板改對應 generator。 ⟵ site_composition.md
- 投資系統母文件（總守則 v2.0）在 Google Drive；改 state-machine 邏輯前必讀；six-state 已對齊純 ETF QQQ+IB01。 ⟵ reference_master_charter.md
- 第二大腦（全文層＋本機 wiki＋vault）2026-07-07 拍板：全本地不上網、衍生物全 gitignore、新內容三道防線自動入腦、涵蓋本機全部 6 個 repo（SIBLING_REPOS registry）。 ⟵ project_second_brain.md
- stock-analyst 版號一號到底；schema 是 8 個下游 pipeline 辨識合併報告的 key，bump 版號必須同步放寬（additive），否則 CI 綠燈但下游悄悄掉報告。 ⟵ dd_skill_version_vs_schema.md
- GRP 排序 mandate：高成長×EPS 上修×股價位置三閘（scripts/engine/grp.py），按上修幅度排序，席位寧缺勿濫；不依賴 5Y IRR，建議一律用 GRP 語言。 ⟵ grp_ranking_mandate.md
- 個股部三軌組合架構（2026-07-03 定案）：核心 5（複利）＋衛星結構（runway🟢 數倍股）＋衛星循環（QC-42 提名），目標 5-10 檔；handoff 見 notes/site-internal/root/_handoff_stock_sleeve_pipeline_20260703.md。 ⟵ project_stock_sleeve_pipeline.md

## 退役／封存記錄

- DCA 已全面退役（2026-07-02 用戶明示）；裁決／moat trend／IRR 權威來源＝v13/v14 dd-meta（dca_* 是舊欄名），v12 過渡期 dual-read fallback 不要拆，用戶可見文案不再出現 DCA。 ⟵ dca_trend_authoritative.md
- 六態機已退役（2026-07-04 用戶明示）；板機層規則變更走 sop-funnel 自身 PREREG；C 型觀察期中勿動門檻。 ⟵ six_state_retired_c_cooling.md
- `/id/theses.html` 與 `/pm/` 已封存（2026-06-11，可逆）；原檔在 _archived/、URL 留 noindex stub、外部 3 repo template 也改了。 ⟵ project_theses_pm_archived.md

## 校準結論（裁決／儀表）

- 裁決函數校準（DD 兩份＋ID 一份）＋v14.6 落地：legacy 60 天倒序 vs v13 回檔段正序；ID 層僅 45% 有機器裁決、錯全集中 shortage×PhaseII（AI 硬體）→ sd_verdict 只當事實錨、Phase II 須交叉驗證、priced_in 待落欄；門檻 PREREG 凍結，2026-10 三份同跑第二輪。 ⟵ project_verdict_calibration_rounds.md
- 首頁風險儀表實證裁決：六訊號儀表＝描述器非擇時、加訊號無效；NFCI/VIX≥40/SKEW/殖利率曲線各自測試結論已記；EPS 上修寬度等資料累積 ≥12 個月再提。 ⟵ project_risk_gauge_verdicts.md
- QC-42 循環鏡頭三樣本驗證完成：ORCL/JBL/MU 定出適用邊界；子型路由位置錶族＋倍數閘＋QC-43 第 7 類已上線；最大遺留＝投降點主動掃描。 ⟵ project_cyclical_trade_lens.md
- 官方 financial-services repo 評審結論：可學集中在事件 T-minus 鏈／確定性驗證／儀表免費訊號三塊（含排序清單）。 ⟵ project_official_finservices_review.md

## Pipeline／專案現況

- 事件 T-minus 鏈全五 phase 上線：催化劑日曆／variance／preview 架構＋人工欄鐵律（cron 永不覆寫 outcome）＋幣別防呆。 ⟵ project_tminus_chain.md
- 2026-07 infra 加固落地：weekly_cache 零 churn 協議／workflow concurrency pattern／scaffolding 新家 notes/site-internal／git 瘦身不做、briefing 確定暫停。 ⟵ project_infra_hardening_202607.md
- industry-analyst v2.5 趨勢欄位全鏈落地：sd_verdict/clock_phase/conviction/kill_metrics 入 id-meta＋79 份 backfill；8 月下旬 79 份同時過期屬預期。 ⟵ project_id_v25_trend_fields.md
- Tier Matrix v3.1 結構凍結×數據活水：快變數據 JS live 讀 screener、Priced 軸自動映射；複審只審 Tier 與證偽觸發。 ⟵ project_tier_matrix_v31_live.md
- 選股駕駛艙＋Momentum-5 對照組：/cockpit/ 純前端聚合零管線；M5＝GRP 的 S&P500 站外對照組（雙窗口、PREREG 凍結、席位人工治理）。 ⟵ project_cockpit_momentum5.md
- 跨資產研究三頁套組上線：/crowding/ 擁擠×/rotation/ 產業輪動（RRG）×/regime/ 大類資產（六軸記分卡）；三頁合一 crossasset-weekly pipeline；描述器非擇時。 ⟵ project_crowding_monitor.md
- 供應鏈瓶頸兩層制上線：curated T0-T2 × 機械層（替代難度×終端封鎖值）；sidecar 兩檔＋cartographer v1.1；首輪提名待複審。 ⟵ project_sc_bottleneck_two_layer.md
- 資產輪動雷達（日線 RRG）上線：/rotation/radar.html 三宇宙×三時框；日更 cron；3 日平滑是視覺關鍵。 ⟵ project_rotation_radar.md
- 2026-07-07 選股頁面大整理完成：聚合層四職能分工定案（cockpit 入口/picks 對外榜/pipeline 流程板機/engine 排序席位）；dd-screener 14→6 頁；復活 screener 須同步還原 update_dd_index 連鎖。 ⟵ project_stock_pages_cleanup_202607.md
- 整站 IA v2 四群導覽定案：nav group key＝pick/research/market/system（quant 已亡）；改 nav 四步 checklist；外部 3 repo literal 重生 byte-identical。 ⟵ project_site_ia_v2_202607.md
- 全站專業化改版落地：機構研究風規範在 _styleguide_v1_20260707.md；/disclosures.html 唯一揭露頁、首頁勿寫回「AI 驅動」。 ⟵ project_site_professional_202607.md
- 半導體 ID v2.3 全面 regen：28→19+9 stub；pilot+B1 已上線；B2-B5 待續。 ⟵ project_id_v23_semi_regen.md
- ID v2.0 deep rewrite 完成：2026-04-27 啟動的 11 份深度重寫全部完成；保留 v2.0 標準＋id-meta CI 限制踩坑供後續參考。 ⟵ id_rewrite_pending.md
- industry-analyst v2.0 pilot 完成（AI 算力資本週期已發布）；遺留 QC-6 T1 60% 對 macro 主題過嚴，建議加例外（floor ~45%+警語）。 ⟵ project_ia_v2_pilot_pending.md
- Pure MA SOP 漏斗定案設計：起漲型 A1 基期≥26週／B 第二班車／T+1 執行；plan 完成待實作。 ⟵ project_sop_funnel_design.md
- Fundamentals cache 待 yfinance 恢復後本機補跑；初版 US 25%／TW 43% success；不主動則 cron 自動修。 ⟵ project_fundamentals_cache_rebuild_pending.md

## 影響產出設計的規範（少數搬入的 feedback）

- 訓練工具禁考記憶回想：SRS/flashcard 已被否決勿再提；只做「新情境＋判斷」型訓練；內部代號不是知識點，勿出現在給用戶的內容裡。 ⟵ feedback_no_recall_drills.md
- 報告資料更新要無痕：對既存 ID/DD 補新數據時自然融入敘事，不留「更新／補齊／changelog」痕跡；review 後沒變就誠實說不用改。 ⟵ feedback_seamless_data_refresh.md
- 別把「自動化好玩」誤當「自動化有用」：對 ID 級深度產出，瓶頸是內容可達性不是索引速度；提 pipeline 前先驗 top 3 來源 friction。 ⟵ feedback_automatable_vs_valuable.md
- 建 DB／cache 先單獨做，consumer 接線是另一個 plan：producer+consumer 一次改動放大風險；zero-consumer-impact cache 可低風險先驗一 cycle 再接。 ⟵ feedback_build_db_before_wire.md
- 評／改 skill 行為前先讀實際產出：skill 是 LLM 判斷＋協議在跑非規則引擎；別只 trace 規則就下結論，反直覺數字先查證。 ⟵ feedback_read_skill_outputs_before_theorizing.md
