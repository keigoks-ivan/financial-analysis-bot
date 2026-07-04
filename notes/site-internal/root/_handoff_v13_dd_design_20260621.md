# v13 DD 整併設計 handoff（2026-06-21）

把 DD（`stock-analyst` v12.7）與 DCA（`deep-conviction-analyst` v1.5）整併成單一 **v13 DD**
skill，著重深度個股基本面，並把 DCA 真正加值的決策層疊在基本面之上。本文件是專案的
authoritative spec — 跨 session 續做先讀這份。

## 0. 已定案決策（用戶 2026-06-21 確認）

1. **`stock-analyst` 直接升級成 v13**（不另開新 skill）；輸出仍是 `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`。
2. **單一報告檔**，內含「深度基本面 ＋ 決策層」；不再產獨立 `DCA_*.html`。
3. **統一裁決**：人面對的結論只有一個 — 進場 / 觀望 / 迴避（+ 倉位角色）。
   原 DD 訊號燈 **A+/A/B/C/X 降為 metadata-only 的基本面評級**（餵 screener，不再是並列 headline）。
4. **短期擇時降級**：Pure MA 六態機、短期 R:R 收進報告末段「擇時附錄」，資訊性、不主導裁決。
5. **篇幅 floor ~110KB**（hard）/ ~125KB（soft warn），added-only。
6. **DCA 退役**：`deep-conviction-analyst` 轉成 deprecation stub，觸發語（dca / 定見）改觸發 v13。
7. **遷移順序：先 plumbing（P1-P2）後 skill（P3）**，每階段獨立可驗。
8. **460+343 份 legacy 全凍結**：靠下游 dual-read 繼續活在站上，零資料遷移。

## 1. v13 報告章節骨架（三層）

來源標籤：`[DD §X]` 現行 DD ／ `[DCA]` 現行 DCA ／ `[合一]` 融合 ／ `[降級]` ／ `[砍]`。

### 頁首 — 結論儀表板（不編號）
合併 `DD §1 dashboard` + `DCA Status Bar` + `DCA §2 一句話` + `DCA §7 裁決 headline`：
一句話 thesis（≤50 字）｜統一裁決 進場/觀望/迴避｜倉位角色｜護城河趨勢 ↑→↓｜Y5 後跑道 🟢🟡🔴｜
Max DD −__%｜品質/護城河/估值燈｜持有年限｜opportunity cost 一行｜5Y 機率加權 EV／IRR。

### Part I — 基本面深度（骨幹，≈70%）
- **§1 投資結論詳述** `[DD §1]` — trap 四問 + 最關鍵監測指標表。
- **§2 序章：第一性原理 × 逆向** `[DD §4]`。
- **§3 投資論點錨定** `[DD §5 + DCA §5 合一]` — 持有期 / 三假設 / 12M對照 / 三風險 / 邊際 /
  決策主線 / **3.F Single Thing（DD §5.F 與 DCA §5 統一成「一個」binary trigger）**。
- **§4 即時財報情報** `[DD §6 + §6.5]`。
- **§5 核心門檻檢核（Munger）** `[DD §7]`。
- **§6 長期成長性** `[DD §8 + DCA A2 吸收]` — 七問儀表板 / Runway / 驅動 / ROIIC / 壓測 /
  AI 風險 / **Y5 後跑道 🟢🟡🔴** / 分部前瞻。
- **§7 護城河（核心）** `[DD §9 + DCA A1 升權威]` — 二維拆解 / Moat-to-Numbers / 市佔表 /
  定價事件帳 / **護城河趨勢 ↑→↓（DCA 12M sourced 證據成為權威趨勢線）** / 威脅三級 / 對手 P&L。
- **§8 財務品質監測** `[DD §10]`。
- **§9 產業格局** `[DD §11 + DCA A2 利潤池吸收]`。
- **§10 治理與資本配置** `[DD §12]`。
- **§11 估值與報酬（最大融合點）** `[DD §13 + DCA §4 合一]` — Fwd PE 分位 / PEG / 同業 /
  **Bull/Base/Bear 5Y + IRR 三分量拆解 + Pattern match** / 內生天花板 sanity check。

### Part II — 決策層（疊在基本面上，不重搜，≈22%）
- **§12 矛盾辨識與強制裁決** `[DCA Phase B]`。
- **§13 Pre-mortem 與 Max DD** `[DCA §6]` — 失敗故事三段倒推（故事→校驗 §3.F→修正）+ Max DD 範圍。
- **§14 決策** `[DCA §7]` — 統一裁決 + 決策矩陣 Hard/Soft Veto + 倉位 + opportunity cost +
  加減碼 + 持有年限。
- **§15 複審觸發與保質期** `[DCA §8]`。

### 附錄 A — 擇時（降級，≈3%）
`[DD §2 殘留]` Pure MA 六態機 + 短期 R:R + 估值燈。純資訊，不主導 §14。

### 砍／改去處
`[砍]` DD §3 三方辯論；`[改]` DCA Phase A1/A2/A3 獨立搜尋 → 不重搜，料落 §6/§7/§9；
`[降級]` A+/A/B/C/X headline → 只進 dd-meta；`[上移]` DCA Status Bar/§2 thesis → 頁首儀表板。

## 2. 統一 metadata：dd-meta v13

保留現行 22 必填欄（screener 不斷線），`schema` 改 `v13.0`。新增（schema=v13 才必填）：

| 欄位 | 值 / 型別 | 取代原本 |
|---|---|---|
| `dca_verdict` | 進場 / 觀望 / 迴避 | DCA `<!-- dca-verdict -->` marker |
| `dca_role` | 7 類 enum（見下）| DCA §7a 角色表 regex（aggregate_dca_stats `_categorize`）|
| `moat_trend` | ↑ / → / ↓（升必填、權威）| DCA `<!-- dca-moat-trend -->` + ~150 行 EV/trend regex |
| `runway_post_y5` | 🟢 / 🟡 / 🔴 | DCA Phase A2 |
| `ev5y_pct` | number | DCA §4「機率加權期望值」regex |
| `irr_base_pct` | number（選填）| DCA §4 |
| `max_dd_pct` | number（選填）| DCA §6c |

`dca_role` enum（對齊 `aggregate_dca_stats.py` CATEGORY_ORDER，去掉 fallback「缺資料」）：
`核心持倉 / 條件式核心持倉 / 衛星持倉 / 條件式衛星持倉 / 投機部位 / 不持有/迴避 / 候選/追蹤池`。

`signal`/`verdict`（A+/A/B/C/X）保留為基本面評級。

## 3. 遷移計畫（dual-read，零 legacy 遷移）

核心策略：聚合器**優先讀 v13 dd-meta 的 dca 欄位；讀不到 fall back 現行 legacy 路徑**。
P1-P2 改完、尚無 v13 報告時，跑一輪結果應與現狀逐字相同（全走 fallback）→ 即驗證點。

| 檔案 | 改法 |
|---|---|
| `validate_dd_meta.py` | schema regex `^v1[23]\.\d+$`；version 接受 v13；v13 才驗新欄位 |
| `update_dd_index.py` | v13 直接讀 meta（繞過 EV/trend regex）；定見欄 → `/dd/DD_X.html#decision`；legacy 仍連 `/dca/` |
| `dd_screener_dd_loader.py` | 優先 meta 的 dca 欄位，否則 `_find_latest_dca` |
| `aggregate_dca_stats.py` | 同掃 v13 DD（讀 meta）＋ legacy DCA，按 ticker 去重取最新 |
| `pre-commit` | DCA gate → v13 單檔 floor 110KB |
| skills | deep-conviction-analyst → stub；ddreport → v13→update_dd_index；multi-stock-comparator → 讀單檔（legacy fall back 雙檔）；portfolio-manager → 重指決策段 |
| 頁面 | how-to.html / dd-screener/index.html 文字；research 頁由 script 重生 |
| CLAUDE.md | DCA workflow / ddreport / size floor 表 / 標準 pipeline 句 |

**不動**：460+343 legacy 報告、`get_eps_for_ticker.py`/Excel pipeline、dd-screener build_* 子頁與
alpha-ranker（修 loader 即涵蓋）、ID/earnings/supply-chain/QGM、~15 份 comparison 靜態檔。

## 4. 執行階段（每階段獨立可驗）

- **P1 metadata 契約**：dd-meta v13 + schema-aware validator。驗：全 476 legacy DD strict 仍綠。
- **P2 下游 dual-read**：3 聚合器 + pre-commit。驗：跑 update_dd_index.py，research/screener 與現狀逐字相同。
- **P3 寫 v13 stock-analyst SKILL.md**（內容主工）。
- **P4 pilot 1-2 檔**：端到端驗（research/screener/錨點/size gate）+ critic 冷讀。
- **P5 收尾其他 skills + 頁面 + CLAUDE.md + DCA 退役 stub。**

## 4.5 進度（live）

- **P0 ✅** 本設計文件。
- **P1 ✅** `validate_dd_meta.py` schema-aware（`^v1[23]\.\d+$`、v13 才驗 `V13_REQUIRED_FIELDS`/
  `V13_ENUM_FIELDS`，v12 零變動）；`dd_meta.md` 補 v13 欄位。驗：476 legacy strict 全綠、
  v13 正負例煙霧測試全過。
- **P2 ✅** dual-read：`update_dd_index.py` 加 `_v13_dca_overlay()`（lru_cache 掃 DD_DIR v13 meta），
  三個 `collect_dca_*` 改為 legacy 掃描後 overlay v13（v13 wins）；`collect_v12_entries` 收 v13；
  `dd_screener_dd_loader.py` v13 → `dca_path = /dd/..#decision`；`aggregate_dca_stats.py` 加掃 DD v13
  meta（`_ticker_link` 對 `DD_*` 走 /dd/#decision）；pre-commit DD floor schema-aware（v13 110/125KB）。
  驗：`_v13_dca_overlay()==0` 證明 all-v12 corpus 下全 no-op（research/screener 逐字不變）。
  **未 commit**（避免並行 session 衝突，留給用戶 review）。
- **P3 ✅** v13 `stock-analyst/SKILL.md`（1981 行 / ~147KB；原 v12.7 備份在 /tmp + git）。三層骨架
  （頁首儀表板 + §1-§11 Part I + §12-§15 Part II + 附錄 A 擇時）；DD §4-§13 −2 位移、子節字母全保留；
  DCA 決策層折入 §12-§15、Single Thing 統一 §3.F、§11 估值×報酬融合（DCA §4 IRR/Bull-Base-Bear/
  pattern match）；A+/A/B/C/X 降 metadata-only；emit dd-meta v13（schema v13.0 + 5 必填 + 2 選填）；
  §14 `id="decision"` 錨點。驗：QC-32 canonical dd-meta 例過 real validator 0 error；結構/機器
  （yfinance 協議/HTML emission/QC-1..38/深度量化模組）全在；無 dangling ref。**未 commit。**
- **P4 ✅** pilot = TSM（`DD_TSM_20260622.html`）。端到端 plumbing **全綠**：dd-meta v13 validator pass、5 必填欄齊、
  `id="decision"` 錨點、三處裁決一致（觀望）、`_v13_dca_overlay` 撿到 TSM、三個 collect 函式把 TSM 路由到
  `/dd/..#decision`（v13 勝 legacy DCA）、`aggregate_dca_stats` 從 dd-meta 讀到（觀望/條件式核心持倉）。
  **已知限制**：pilot 73.7KB < 110KB v13 floor（結構完整、數字自算、接線正確，但深度未達 production；
  commit 用 `--no-verify`）。critic 冷讀依用戶「直接到 P5」指示略過。
- **P5 ✅** 收尾：`deep-conviction-analyst`→deprecation stub（dca/定見 轉 stock-analyst）；`ddreport` v2.0
  （砍 DCA step，鏈 = v13 DD→update_dd_index→commit）；`multi-stock-comparator` 加 v13 註記（讀 DD 即得決策層）；
  `CLAUDE.md`（DCA workflow 整段改寫、標準 pipeline 句、size floor 表加 v13 110KB row、sync 段 stale 引用）；
  `how-to.html`（DCA card 改 v13 整併、skill list）。portfolio-manager 無 DCA 引用免改；dd-screener JS functional
  （v13 dca_path 已指 /dd/..#decision）。
- **未跑 update_dd_index.py**：避免重建 research/index.html + 觸發 yfinance screener 撞並行 session
  （這兩個 shared 檔此刻被其他 session 改著）。dual-read 已驗，下次任一 session 跑 update_dd_index 會自動撿 TSM/AVGO。

## 6. 已 commit + push（2026-06-22）

- commit `44869bf3`：v13 系統（P1-P3 plumbing + skills + docs + TSM pilot）。
- commit `3fad73c7`：AVGO v13 pilot（進場）+ TSM/AVGO INDEX.md 列 + docs/dd/CLAUDE.md rule 18。
- 兩份 pilot 示範 v13 差異化裁決：**TSM 觀望**（貼 ATH/站上布林上軌/動能過熱）vs **AVGO 進場**
  （PEG 0.44/回檔 17%/布林上軌下方/未過熱）；基本面評級皆 A（metadata），人面對裁決由 §14
  決策矩陣（時機）區分 — 正是 v13 統一裁決設計的核心價值。
- 兩份皆 --no-verify（68-74KB < 110KB floor，用戶 review 認可的 lean pilot）。

## 7. 後續可選（非阻塞）

- v13 報告要達 110KB production 深度需完整研究 run（每深度模組 6-8 次 web 深搜 + segment-level
  sourced TAM + 完整對手 P&L 實數）；目前 pilot 走精簡。若要量產 v13，建議排一次「TSM/AVGO 全深度重跑」。
- INDEX.md 維護規則小節（docs/dd/CLAUDE.md）仍寫「7 欄」，實際已 8 欄（裁決欄 v13 = 統一裁決）；
  pre-existing drift，未在此次 scope 修。
- 跑一次 update_dd_index.py（待並行 session 靜止時）讓 research 頁/screener 正式反映 v13 兩檔。

## 5. 風險與守則
- 兩種「裁決」混淆 → 已用「A+/A/B/C/X 只進 metadata、人面對單一裁決」化解。
- 主風險在 P3 skill 重寫品質 → P4 pilot + critic 冷讀把關。
- 並行 session git 衛生：commit 前四步自檢、只 add 本次檔（見 CLAUDE.md / memory）。
- moat trend 權威性：v13 dd-meta.moat_trend = 決策層趨勢，對齊 memory `dca_trend_authoritative`。
