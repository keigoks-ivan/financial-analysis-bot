# Handoff：個股部 25% 投資流程落地（四項工程）

日期：2026-07-03 ｜ 交付對象：Opus 實作 session ｜ 設計定案：本文件為準，偏離先問持有人

## 0. 背景一頁

個股部目標：**5～10 檔最有上漲潛力的組合**（總資產 25%，總守則 v3.0 草案；單檔上限 10%／衛星 5%，分母＝個股部淨值）。流程＝單一漏斗：`發現 → 資格閘 → 裁決 → 潛力排序 → 板機(sop-funnel) → 倉位 → 監控 → 出場 → 複盤`。

2026-07-03 對過去 12M／24M 做了發現力驗屍（用 `data/weekly_cache` 週線 × `docs/dd-screener/latest.json` × sop-funnel ledger × git DD 入庫日），結論：

- **前 12M（2024-07→2025-06）成長年**：贏家（SEZL/RKLB/PLTR/APP/CLS/CRS/STRL/FIX）多為「多年基期 ATH 突破」＝ A1 同型，板機層無結構缺陷；當年抓不到是因為 DD 宇宙／漏斗 2026 年才建成。
- **後 12M（2025-07→2026-06）循環年**：贏家（SNDK +3744%/AXTI/BE/WDC/MU/LITE/STX/台鏈）全滅於五條件的 trailing fcf/roic ＝ QC-42 已診斷的 mandate gap。
- **Top25 贏家今天只有 4 檔過現行閘**（WDC/CRDO/STRL/FIX）；`de`（D/E≤0.7）是實作私加的條件（**持有人 2026-06-11 拍板的五條件沒有 D/E**），在贏家樣本誤殺 AVGO/LLY/APP/SEZL/STX。
- 對照組（現行規則 8 檔進場票）24M 等權 +165%、後 12M +80% —— 系統在自己 mandate 內及格，缺的是循環鏡頭與板凳深度。
- 發現層「入庫後仍有肉」：MU 入庫後 +176%、STX +141%、ALAB +102% —— 規則放行比發現速度更關鍵。

修正後三軌（已用 2026-07-02 資料驗證可跑出名單）：
- **核心軌可執行 5**：NVDA/TSM/AVGO/GOOGL/LLY（後三檔為 D/E、FCF 冤案平反）
- **衛星·結構 3**：PLTR/COHR/APH（bull×≥2、runway 🟢）
- **衛星·循環 0 檔可執行、18 檔候選**：低熱＋上修組 ORCL/JBL/SOFI/HOOD/HUBB/NET/GHM；🔥已熱組 MU/FORM/2327.TW/CIEN/VICR/2368.TW（反動能閘擋、等回踩）

---

## Task 1：D/E 退出 pass_count（小改、高影響、先做）

**改哪**：`scripts/build_dd_screener.py`（criteria 定義處，latest.json 的 `criteria[]` 現含 fcf/roic/eps2y/peg/de 五項）。

**Spec**：
1. `de` 從 pass_count 計算中移除（criteria 陣列拿掉或標 `advisory: true` 不計分）；**欄位照算照顯示**，前端改成警示 badge（D/E>0.7 顯示 ⚠，不擋）。
2. 五條件的第五條回歸持有人拍板版：**護城河 grade∉{C,X} 且 trend≠↓**。若 moat veto 已在別處實作（sop-funnel `moat_excluded`），pass_count 維持四條件即可，但 UI 文案要寫清楚「4 條件＋護城河 veto」。
3. **下游影響必查**：`sop-funnel` 母體（`quality_pass` 現 25 → 預期 ~41）、`targets.html` 六燈之「進場」燈不受影響（走 dca_verdict）、`pipeline` 頁（Task 4）。sop-funnel 母體變大屬 PREREG 事項——**記入 ledger meta（gate 變更日 2026-07-0X），回測與記分板分段標示，不重算歷史**。
4. 驗收：AVGO/LLY/STX/WDC pass；SNDK 仍被 moat veto（C↓）；`python3 scripts/sop_funnel/test_engine.py` 全過；pass 分布約 25→41（±3 容忍）。

## Task 2：衛星·循環軌正式化（新 JSON 層＋掛 weekly workflow）

**產出**：`docs/dd-screener/cyclical-track.json` ＋ `cyclical-track.html`（或併入 Task 4 pipeline 頁一節）＋ `cyclical-track-snapshots/`（沿用其他層的 snapshot 慣例）。

**資格規則（QC-42 代理版 v0，已回測形狀，門檻如下不要自行調參）**：
- 循環特徵：`fail_criteria ∩ {fcf, roic} ≠ ∅`（trailing 難看）
- 上修動能（單月，baseline 見 `eps_revision_baseline_date`）：`eps2y_revision_pp ≥ +3` **或** `eps_fy_next_revision_pct ≥ +5` **或** `eps_fy_curr_revision_pct ≥ +3`
- 護城河底線：`moat_grade ≠ X` 且非（`C` 且 trend `↓`）
- 排除已過品質閘者（歸核心/結構軌，一檔一軌）
- **熱度閘（反動能）**：12M 報酬 >+250%（用 weekly_cache 算）→ 標 🔥「等回踩」，名單保留但排序沉底、明文不可追
- 排序：`eps2y_revision_pp + eps_fy_next_revision_pct` 降冪；低熱組置頂

**硬規則**：本軌輸出是**研究提名清單，不是進場清單**——每檔要進場仍須 (a) v14 DD 裁決＝進場（含 QC-42 循環鏡頭附錄 B）(b) sop-funnel 板機。頁面上這句話要顯性。單檔上限 3%（個股部淨值），寫進說明。

## Task 3：循環候選 DD 隊列（判斷密集，品質閘照舊）

順序：**ORCL → JBL → MU（裁決複審）**，之後 SOFI/HOOD/HUBB/NET/GHM 視前三檔結果。全走 `stock-analyst` v14 skill：
- ORCL/JBL 是新 DD；MU 是既有 DD 的裁決複審（有 v13 報告，走複審不重寫）。
- **QC-42 附錄 B（循環鏡頭）目前 spec v0.1 未定稿**（見 memory `project_cyclical_trade_lens`：平行投機軌、5 檔循環位置、反動能硬閘、不碰 §14/dd-meta）。這三檔就是持有人要的手跑原型——**每檔附錄 B 產出後停下來給持有人看**，通過兩檔以上再把 spec 轉正。
- ORCL 特別提示：12M -40% ＋ FY2 單月上修 +36% 是本次篩選頭牌，但「跌有跌的理由」＝ value trap 假設必須在 DD 裡正面處理（AI 訂單 vs 資本開支/債務結構）。
- 常規閘照舊：v14 size floor（110KB hard）、跑完 `python scripts/update_dd_index.py`、dd-meta validator、產業態勢 critic（QC-41）。

## Task 4：`docs/dd-screener/pipeline.html`（漏斗總覽頁）

單頁呈現整條漏斗的活數字，weekly workflow 自動更新（掛在形狀掃描/標的頁更新之後，同一 workflow step，含 fail-safe 慣例）：
1. **宇宙**：universe_size、待研究隊列（六燈盲區 ＋ 動能盲區）
2. **資格閘**：修正後通過數＋名單（含 D/E ⚠ badge）
3. **三軌射擊名單**：核心（EV5y×確定性排序）／結構衛星（runway 🟢、bull×）／循環衛星（Task 2 輸出）——每檔連 DD `#decision` 錨點，無裁決者標「待補 DD」
4. **板機現況**：sop-funnel today_signals / open_trades / standby / 態②否決計數
5. **回看鏡（發現力稽核）**：12M/24M 報酬 top 30 ×（無 DD 或 DD>90 天）→ 動能盲區研究隊列；本次驗屍腳本邏輯直接移植（週線報酬計算見下方附錄）
6. **隱私線**：只呈現研究層，**實際持倉/權重不上頁**（/pm/ 封存同一原則）

Nav 掛法照 `scripts/site_nav.py` 慣例；資料全部來自既有 JSON，**不新增採集**。

## 驗收與紀律（每個 Task 通用）

- 動引擎必跑 `scripts/sop_funnel/test_engine.py`（39 斷言回放錨＝regression 防線）；ledger append-only 不手改。
- DD 相關改動後必跑 `python scripts/update_dd_index.py`，research 頁/screener JSON 與新檔**同一 commit**。
- Commit 前四步自檢（CLAUDE.md「Parallel-session git hygiene」）：cwd、`git status` 的 `??` 區、不盲 `git add -A`、fixture 進 /tmp。
- 中文產出全形標點；報告數字必 sourced。
- 每完成一個 Task 停下來回報，不連跑。

## 附錄：驗屍用的計算慣例（回看鏡移植用）

- 12M 報酬：`weekly_bars[-1].close / weekly_bars[-53].close - 1`；24M 用 `[-105]`；bars 不足即跳過。
- DD 入庫日：`git log --diff-filter=A --format=%as -- 'docs/dd/DD_{T}_*.html' | tail -1`。
- EV5y 取值：`live_ev5y_pct` 優先，缺則 `ev5y_pct`；bull 倍數＝`bull_5y_price / price_at_dd`。
- 本次驗屍原型腳本在 session scratchpad（shooting_list.py），邏輯以本文件文字為準。
