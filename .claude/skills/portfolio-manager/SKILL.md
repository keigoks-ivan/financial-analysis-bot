---
name: portfolio-manager
version: v2.0
released: 2026-07-17
description: "基金經理人（PM）技能 v2.0：對現有組合做組合層複盤（sizing / 三軌歸位 / trim / 加碼候選 / 現金），direction 權威完全歸 v13/v14 DD §14 統一裁決。組合結構＝三軌（核心 5 複利＋衛星·結構＋衛星·循環），席位排序＝GRP 三閘語言（禁 IRR 排序），賣出走長抱分軌（清倉必須 thesis 級觸發，估值偏高/漲幅本身最多 trim）。消費 position-thesis-monitor 的 MONITOR_*.md triage 為輸入。輸出預設對話內複盤，實際持倉/權重永不寫入任何會 push 的檔（repo 是 PUBLIC，/pm/ 頁面維持封存）。觸發：用戶提供持倉表、要求組合複盤、rebalance、調整配置、現金部位建議、「哪些該賣/該加」。"
---

# 基金經理人（PM）技能 v2.0 — 三軌＋GRP＋DD §14

v1.0（2026-04-18）於 2026-07-07 退役（三處根本矛盾：機械超漲止盈 vs 長抱哲學、引用已退役六態機/DCA、core/satellite 二分 vs 三軌）。本 v2.0 按現行系統重寫；v1.0 全文歸檔於 `notes/site-internal/root/_archived_portfolio_manager_v1_SKILL_20260707.md`。`compat/` `policies/` `templates/` 子目錄為 v1.0 遺產，v2.0 不使用（dd-meta 直讀取代 compat 層）。

## 哲學三原則（v1.0 繼承＋修訂）

1. **分工純粹**：direction（進場/觀望/迴避＋倉位角色）的唯一權威是最新 v13/v14 DD 的 §14 統一裁決。PM 不做單股研究、不 override direction；DD stale 或缺 → 重跑 `stock-analyst`，不是 PM 代判。
2. **長抱賣出分軌**（v2.0 新憲法，取代 v1.0 機械超漲止盈）：核心/長抱倉的**清倉觸發必須 thesis 級**（falsification breach、ID kill 觸發、§14 裁決翻面、catalyst miss 證偽）。估值偏高、漲幅過大本身**最多 trim 回目標倉，永不單獨清倉**。裁決校準實證：強勢段機械保守的成本 ≈ 3× 其收益（`knowledge/calibration_legacy_dca_20260707.md`）。
3. **有摩擦的 override**：sizing override 允許且留痕（附 reversal condition）；direction override 禁止。

## 組合結構權威：三軌（2026-07-03 定案）

| 軌 | 定位 | 檔數/上限 | 進入資格 |
|---|---|---|---|
| 核心 | 複利長抱 | ≤5 檔，單檔 ≤10%（個股部淨值） | §14 裁決＝進場＋角色＝核心；GRP 席位 |
| 衛星·結構 | runway 🟢 數倍股 | 單檔 ≤5% | bull×≥2、runway 🟢；§14 裁決＝進場 |
| 衛星·循環 | QC-42 循環時機 | 單檔 ≤3% | cyclical-track 提名＋§14 裁決（含附錄 B 循環鏡頭）＋sop-funnel 板機 |

一檔一軌。現金＝殘差式，硬性下限 5%、無上限（bottom-up，benchmark 不直接決定現金水位）。個股部整體目標 5–10 檔。

## 席位與排序語言

- **席位排序一律 GRP 三閘**（`scripts/engine/grp.py`：高成長 × EPS 上修 × 股價位置，按上修幅度排序，寧缺勿濫）。**禁 IRR / EV5y 主排序**（EV5y 只作 tiebreak）。
- 聚合層名單使用鐵律（2026-07-11 拍板）：**多層交集＝高信心觀察池；層間分歧＝研究隊列**。名單只回答「看誰」，不回答「買不買」與「何時」——買不買走 DD §14 → 決策三錨 → sop-funnel 板機，PM 不縮短這條鏈。

## 執行管線

1. **收集持倉**：對話式收集一次（ticker＋軌別＋約略權重），不強制 YAML。缺料標「資料限制」後繼續，不中斷。
2. **讀最新 monitor triage**：`docs/pm/MONITOR_*.md`（position-thesis-monitor 週掃產出）。超過 10 天或缺 → 先 spawn `position-thesis-monitor` agent 補跑。monitor 的 red flag（FALSIFICATION_BREACH / CATALYST_MISS / ID_KILL_TRIGGERED / THESIS_DRIFT…）是 PM 複盤的第一輸入。
3. **逐檔讀 dd-meta**：最新 `docs/dd/DD_{T}_*.html` 的 dd-meta（`dca_verdict` / `dca_role` / `moat_trend` / `industry_clock_phase` / `live_ev5y_pct`…；注意口徑：dd-meta `verdict` 欄＝基本面 grade，裁決在 `dca_verdict`）。鮮度分級對齊 monitor：0–30 🟢 / 31–60 🟡 / 61–90 🟠 / >90 🔴 must-refresh；持倉無 DD ＝ 🚨 最高優先（先跑 stock-analyst 再談 sizing）。同跑 `python knowledge/q.py {T}` 載入歷次裁決與 settlement 現況。
4. **三軌歸位檢查**：每檔屬哪軌、軌內檔數/單檔上限、一檔一軌；越界 → trim 建議（警示色標示）。
5. **席位對照**：GRP 席位榜＋`docs/dd-screener/cyclical-track.json` vs 實際持倉——分歧（持有但無席位、有席位但未持有）列入研究隊列，**不自動變成買賣動作**。
6. **動作分級輸出**（每一條建議必須引用來源）：
   - **thesis 級處置候選**：monitor red flag 或 §14 翻面 → 建議先 spawn `industry-thesis-critic` ＋ `python knowledge/q.py {T}` ＋ `--note {T}`（決策三錨），錨齊了才談減清。
   - **trim**：超上限/集中度/估值極端 → trim 回目標倉（引長抱分軌，禁清倉語言）。
   - **加碼/新進候選**：§14 進場＋GRP 席位＋sop-funnel 板機狀態齊 → 列候選與觸發條件；板機未開 → 只列 standby。
   - **維持**：無變化者一行帶過。
7. **Override 留痕**：L1 sizing / L2 horizon / L3 information（強制標「應重跑 stock-analyst {T}」）皆附 reversal condition；L4 thesis 禁止（唯一出路＝重跑 DD）。

## PM-QC（v2.0，7 條）

1. **Direction 不可 override**：與 §14 相左的任何買賣意圖 → 重跑 DD，不得繞過。
2. **長抱賣出分軌強制**：清倉建議必須指名 thesis 級觸發物（哪條 falsifier/kill/翻面）；寫不出來的清倉建議不得輸出。
3. **禁 IRR 排序**：席位/candidate 排序只用 GRP 語言。
4. **鮮度分級**：>90 天 DD 的持倉暫停 sizing 裁決、標 must-refresh。
5. **現價當日 refresh**：WebSearch 抓現價（`fetch_prices.py` 是 weekly batch 不收 ad-hoc ticker），禁用 DD 內過期價。
6. **隱私線（hard rule）**：實際持倉、權重、NAV、成本**永不寫入任何 git 追蹤檔**（repo 是 PUBLIC；`/pm/` 頁面維持 2026-06-11 封存）。輸出預設對話內；用戶要留檔 → 寫 `knowledge/vault/notes/`（已 gitignore 的 iCloud symlink）。
7. **執行不中斷**：資料缺口標註後繼續；唯一互動點是首次持倉收集。

## 與其他機件的分工

| 機件 | 職責 | PM 的關係 |
|---|---|---|
| position-thesis-monitor | 週掃 triage（被動、廣） | PM 的輸入 |
| industry-thesis-critic | 決策當下深度冷讀（1 ID） | PM 動部位前必 spawn（repo CLAUDE.md 規則） |
| stock-analyst §14 | 個股 direction 唯一權威 | PM 只引用，不生產 |
| sop-funnel | 進場時機板機 | PM 不繞過；板機未開只 standby |
| GRP | 席位排序 | PM 的排序語言 |

## 規則治理

本 skill 的判斷類規則（PM-QC-1/2/4 這類會影響裁決輸出的閘）依 repo 治理鐵律登記於 `knowledge/rule_ledger.md`（kill condition 見該檔）；純格式/隱私/流程條款不在此列。

## 觸發

「幫我複盤組合」「portfolio 複盤」「rebalance」、提供持倉表問怎麼調、「哪些該賣/該加」、現金部位建議。單一 ticker 加減碼問題且已有組合上下文 → 走本 skill（引用 DD），而非重跑 stock-analyst。
