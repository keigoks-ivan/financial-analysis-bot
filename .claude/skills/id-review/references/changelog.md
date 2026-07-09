# id-review v1.6.1 — changelog.md（條件載入 reference）

> 本檔為 SKILL.md 的拆分模組（2026-07-09 v1.6.1 結構拆分，內容自 v1.6 原文搬移、語意零變更）。必讀時點見 SKILL.md 條件載入路由表。修改規則請同步 SKILL.md stub 與 references/changelog.md。

## 【後續升級】

- v1.1（2026-05-02）：加 Step 2 input mode dispatch (A/B/C) + Step 0/C1-C6 consolidation phase + Step 6 banner 寫法明確化（append vs rewrite）。觸發來源：2026-05-02 ID_AIInferenceEconomics 手動 patch 暴露 3 個 gap + 1 個缺漏概念（banner 累積 / consolidation）
- v1.2（2026-05-03）：加 Step 6.5d PM Implication §0.7 re-assessment（5 bullet / j-logic 4 action / conviction pill sync + back-fill scenario 舊 ID）。觸發：ID_AIDataCenter v1.1 patch（commit f1c450b）— user 把臨時 PM block 升格為所有 ID 標準段落。
- v1.3（2026-05-12）：加 `--mode ds` 分支支援 industry-ds skill 產出的 DS 報告。新增「DS Mode 檢查清單」（DS-1 到 DS-6：表格比 / history-future causality / supply-demand 平衡 / §6 三情境 / §10 雙路徑 / §11 一致性）+「DS Mode Banner 格式」。觸發：industry-ds skill v1.0 上線，需要 mandatory critic gate。
- v1.4（2026-05-13）：DS-mode 檢查清單從 6 條擴為 9 條。DS-2 升級為「因果閉合在 §3 或 §5，不可延後到 §8」；新增 DS-7（source-tag 抽查 + T1 占比 + 黑名單）、DS-8（§6 base/bull/bear 推導抽查）、DS-9（§1 雙錨點 — 日期 + 量化）。觸發：industry-ds v1.1 上線，DS_AIAcceleratorDemand v1.0 暴露 5 個系統性弱點（無 footnote、無推導、§1 口語錨點、§11 forward-looking 閾值無時間標、§3 因果延後到 §8），需要對應 critic 鎖點。
- v1.4.1（2026-05-13）：移除 DS-7（source-tag 抽查）。觸發：industry-ds v1.2 把 inline `<span class="source-tag">` 移至每節末 `<aside class="ds-refs">`，pre-publish Gate 12 已更新為 aside 結構檢查 + T1 占比。DS-7 原本三個功能（URL 可達性抽查 / tier mis-tag 偵測 / ≥15 sources 底線）與 Gate 12 重疊度 ~80%，剩 20% 為低頻 redundancy；保留會誤 fail v1.2 報告（aside 內無 inline tag）。DS-8/DS-9 編號保留不動。
- v1.6.1（current，2026-07-09）：**結構拆分**。SKILL.md（~64KB）拆為核心 + 條件載入 references/：【DS Mode 檢查清單】全文（8 條，僅服務 legacy DS）搬至 `references/ds-mode-checklist.md`、版本歷史（本檔）搬至 `references/changelog.md`，核心各留 stub + 必讀時點，並在 Mode Dispatch 段加條件載入路由表。內容逐字搬移、語意零變更（Python 腳本移動 + char-count 對帳）。ID v2 Mode 檢查清單（V2-1~V2-15，現役主力）與所有 banner 格式、Step 1-7 patch flow 留在核心。ID v1 legacy checklist 未拆出——它與共用 Step 1-7 flow 交織、無獨立小節可乾淨切出。
- v1.6（2026-07-08）：**校準教訓武器化＋機器欄時代同步**。V2 checklist 11→15 條：V2-12 機器欄↔內文同步（v2.5 五欄＋v2.6 priced_in，下游 QC-52/獵場鍵/monitor 直讀機器欄，矛盾比散文錯更危險）；V2-13 熱產業時鐘施壓（calibration_id_20260707：shortage×Phase II 唯一系統性失效格 7/25，critic 是時鐘樂觀偏誤的最後防線）；V2-14 kill 套套邏輯與口徑防呆（閾值抄自家 guidance＝永真/口徑不唯一/全表公司自報數）；V2-15 v2.7 情境手冊實答抽查（防 Gate 14 宣告式通過）。版本適用門檻：V2-12~14 需 ≥v2.5、V2-15 需 ≥v2.7，舊 v2.0-v2.4 報告跳過不失敗。
- v1.5（2026-06-11）：**加 v2 自動判別分支**，搭配 industry-analyst v2.0（合併 industry-ds、改 §0-§9 九章敘事骨架）。① Mode Dispatch 改三層判別：`DS_*` → ds mode；`ID_*` → 讀 id-meta `skill_version`，`v2.x` → ID v2 mode、`v1.x`/缺欄位 → ID v1 mode（legacy 現行流程不動）。② 新增「【ID v2 Mode 檢查清單】」= 現行 ID cornerstone 6 條 + thesis box sync（保留、remap 到 §0/§7/§8/§9）+ 從 DS 搬 8 條 remap 到 v2 章節（V2-1 文字比≥55%/表≤10 / V2-2 因果閉合 §3 或 §4 / V2-3 §5 供需裁決三選一 / V2-4 §5 三視野×三情境 trigger 可量化 / V2-5 §8 catalyst 雙路徑 / V2-6 §9 ticker 與 §3/§4 一致 / V2-7 §5 cell 推導抽查回溯 §3/§4 / V2-8 §1 雙錨點）+ 3 條 v2 新模組抽查（V2-9 §4 三角對帳 / V2-10 §5 資本週期證據 / V2-11 §7 priced-in 分位）。共 11 條 V2 + cornerstone 6 + thesis box sync。③ Step 8.7 spawn prompt 由 skill_version 自動 dispatch（v2.0 主稿已對齊）。DS-mode 8 條與現行 ID v1 checklist 文字不動（legacy 報告續用）。
- v1.3：跑熟後降為 mode (b) auto-patch 大錯
- v1.3：加 cron 排程模式（weekly 自動跑所有 Q0 ID 的 critic，產 alert 但不 patch）
- v1.4：跨 ID 一致性 reconcile（critic 找到 cross-ID 數字差異時，自動 patch 兩份 ID 的數字）
- v2.0：擴展為 `dd-review`（同樣模式但對 stock-analyst 的 DD 而非 ID）
