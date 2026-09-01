# 設計稿：條件流量地圖（flowmap）＋機率化判讀對帳簿（forecast ledger）

- 日期：2026-09-01｜狀態：**設計稿，未動工**（持有人核准後才開建）
- 出處：「利用市場訊息判別走向」討論收斂——判死的是「指數方向點預測」，不是預測本身。取經機構後選定兩個可誠實預測的物件：**機械行為者的條件流量**（GS flow desk 模式）與**判讀本身的機率記分**（Bridgewater 稽核＋Tetlock 校準模式）。
- 憲法相容性（先講清楚）：
  - 兩層皆**不是收斂面**（2026-07-07 拍板）——不回答買不買、不進 picks／GRP／三軌任何名單。flowmap 輸出條件句（「若觸及 X 則機械賣壓約 Y」），不輸出方向句；ledger 是 meta 層（對判讀記分），不產生判讀。
  - 描述器紀律不變：flowmap 頁面掛與 crowding 同款 disclaimer（描述器非擇時訊號）。
  - 判斷類規則依治理鐵律登記 rule_ledger（kill conditions 見 §A6／§B6）；commit 時履行「加一提刪一」（候刪提名由持有人挑，建議名單見 §C3）。

---

## A. 條件流量地圖（flowmap）

### A1. 目標與非目標

- **回答**：未來 1–10 個交易日，機械型參與者（CTA／vol-control／庫藏股／dealer gamma）在什麼價格與波動條件下，會被迫買或賣、量級多少。
- **為什麼是真預測**：這些參與者按公式行動，流量可事前計算、事後對帳——與 crowding 的差別是 crowding 量「部位存量」（水位），flowmap 量「條件流量」（若 A 則 B 的邊際壓力）。
- **不做**：不預測指數方向、不出買賣指令、不落任何聚合名單、不做個股層。

### A2. 模組拆分（分 phase）

**Phase 1（公開數據可完全重算，信心 hi/med）：**

| # | 模組 | 機制 | 輸出 |
|---|---|---|---|
| 1 | CTA 趨勢觸發位 | 對 SPX／NDX／RTY（＋Phase 1.5 加債券、金、油）重建標準多窗趨勢模型（建議 3 窗：~20／60／120 日動能等權，門檻上線即 PREREG 凍結），反解各窗「翻多／翻空的價格位」 | per-market：當前訊號（+1/0/−1 分窗）、最近翻轉價位與距現價 %、全翻轉時的預估名目流量（AUM 錨 ~$300B CTA，外部研究值，掛 lo 信心） |
| 2 | Vol-control 曝險 | 目標波動策略曝險 ≈ min(cap, σ_target / σ_realized)；用 SPX 日線算 1M/3M blend realized vol，輸出「RV 每 +2 vol 點 → 曝險降 X%、隱含賣壓 $Y」的階梯表（AUM 錨 ~$200–300B，掛 lo） | 當前隱含曝險 %、距下一階梯的 RV 距離、假想 ±2% 日的次日流量 |
| 3 | 庫藏股靜默期日曆 | S&P 500 市值前 ~100 成分的財報日（yfinance earnings calendar）→ 推 blackout 窗口（財報前 ~5 週起）→ 覆蓋率 % 時間線 | 未來 8 週「買回買盤缺席度」曲線＋高峰週標記（純日曆，無判斷） |

**Phase 2（資料有缺口，未解前一律進 gaps 不捏造）：**

| 4 | Dealer gamma | 需要 CBOE/OCC OI 級資料，免費源只有 delayed/粗粒度，SpotGamma 式重建誤差大 | 先以代理（VIX 期限結構斜率＋0DTE 成交占比，若可得）掛 lo，或明列 gaps。**不因為想要這格就用低信心數字充數**——這是 crowding「未取得數值進 gaps」紀律的直接沿用 |

### A3. 資料層（新增最小化）

- **新增 `data/flowmap_prices.json`**：日線 close，先 3 檔（^GSPC／^NDX／^RUT 或 SPY/QQQ/IWM 代理），rolling ~2 年，incremental 增量更新，yfinance→stooq fallback（照抄 `regime_prices.json` 的既有模式；該檔是週線 6 檔，不夠用故另建，不動它）。
- 財報日曆：優先重用 `docs/monitor/data/macro_calendar.json` 既有抓取路徑，不足再補 yfinance。
- COT 對帳用 `data/cot_history.json`（已有，crowding pipeline 維護，唯讀）。

### A4. 輸出 schema（flowmap-v1）與頁面

- `docs/flowmap/data/latest.json`：
  ```json
  { "schema": "flowmap-v1", "as_of": "YYYY-MM-DD", "generated_at": "...",
    "cta": [ { "market": "SPX", "windows": [{"len": 60, "signal": 1, "flip_level": 7420.5, "dist_pct": -3.1}],
               "composite_signal": "+2/3", "est_flow_on_full_flip_usd_bn": [20, 40], "confidence": "lo" } ],
    "vol_control": { "rv_1m": 11.2, "rv_3m": 13.5, "implied_exposure_pct": 87,
                     "ladder": [{"rv": 15, "exposure_pct": 75, "flow_usd_bn": -18}], "confidence": "lo" },
    "buyback": { "blackout_cov_pct_by_week": [...], "peak_week": "YYYY-MM-DD" },
    "gamma": null, "gaps": ["dealer gamma：無 OI 級資料"], "frozen_forecast": { ... 見 A6 } }
  ```
- `docs/flowmap/index.html`：單頁三塊——①條件流量表（條件→行為者→量級→信心→as-of）②觸發位 vs 現價距離條圖 ③blackout 覆蓋率時間線。noindex 先行，站內入口 Phase 1 只掛 detective 頁側連（不動 nav，上 nav 是持有人另拍的事）。
- 更新：新 workflow `flowmap-daily.yml`（cron 跟 detective-daily 同時段），**零 LLM 純機械**。

### A5. 與 detective 的關係（刻意分兩步）

Phase 1 flowmap 獨立產出，不改 detective。Phase 2 若對帳成立，才把「CTA 翻空位距離 < 2%」這類條目掛進 detective signals（那是改判斷系統，另案審）。一次只動一個系統。

### A6. 自我證偽（模組級 kill，登 rule_ledger）

- **每日凍結預測**：latest.json 帶 `frozen_forecast` 欄——「若次日收盤跌破 X，CTA 模型部位變化 ΔY 方向」。歷史逐日 append `docs/flowmap/data/forecast_history.jsonl`（機械產生，不可回改）。
- **對帳路徑**：CTA 模組 vs CFTC COT 週度資產經理／槓桿基金部位變化方向（cot_history 已有）；vol-control 模組 vs 後續 RV 實際路徑下的模型曝險變化。
- **kill conditions**：
  - CTA 模組：連兩季（26 週）COT 方向對帳命中率與擲硬幣無統計差異 → 模組降級為 gaps 或刪除。
  - vol-control 模組：階梯表預測的流量方向連兩季與 SPX 已實現波動—報酬互動不符 → 同上。
  - buyback 日曆為純日曆無判斷，不掛 kill。
  - 門檻數字（3 窗長度、RV blend 權重、AUM 錨）上線即 PREREG 凍結至下一輪校準，期間不因單一案例調參。

---

## B. 機率化判讀對帳簿（forecast ledger）

### B1. 目標

把站內判讀（detective-read／monitor-read editorial、macro stance 證偽表、crowding named-trade unwind 觸發器）升級為**可記分的機率預測**：落款凍結→機械結算→Brier／校準曲線。直接給 rule_ledger 既有條款（「macro stance 與後續 6M 方向連兩輪無相關→降級」）一條可執行的機械路徑。

### B2. 資料模型：`knowledge/forecasts.jsonl`（append-only，鏡像 decisions.jsonl）

```json
{ "id": "fc_20260901_det_01", "ts": "2026-09-01",
  "source": "detective-read",
  "source_ref": "detective editorial as_of 2026-09-01 / theme 2",
  "claim": "90 天內 HY OAS 收盤突破 400bp",
  "p": 0.25, "horizon_days": 90, "resolve_by": "2026-11-30",
  "resolver": { "series": "monitor:hy_oas", "op": ">", "value": 400, "window": "any_close" },
  "status": "open", "resolved_ts": null, "outcome": null, "brier": null }
```

**核心設計裁定：resolver 必須機械可判**。claim 必須綁 monitor／detective 的具體 series＋門檻＋窗口，寫不出 resolver 的敘事句不准落帳。這不是新紀律，是既有「每個判讀句錨定機械層具體數字」的自然延伸——只多要一個 p 和到期日。`series` 域名空間：`monitor:*`／`detective:*`／`price:*`（weekly_cache）三類，結算腳本各有讀法。

### B3. 產生端（誰寫入）

- **Phase 1 不動任何 skill 檔**（skills versioned and stable；進 skill 條文是持有人另行核准的 Phase 2）。落帳方式：
  1. detective-read／monitor-read 跑完後，orchestrator 把 editorial watch 條目中可機械化的 1–3 條擬成 forecast 草案，**問持有人落不落帳**（一句話確認）。
  2. macro 報告的證偽表本來就是「條件＋現值＋as-of」——寫 `scripts/harvest_macro_falsifiers.py` 一次性＋增量搬運成 forecasts（p 由報告 stance 賦值，搬運時人工過目）。
  3. 手動落帳：持有人任何時候可直接 append（q.py 加 `--forecast-add` 互動式引導，防 schema 錯）。
- **量的預期**：每週 2–5 筆。重質不重量——樣本累積靠時間，不靠灌水。

### B4. 結算端：`knowledge/settle_forecasts.py`（鏡像 settle_outcomes.py）

- 對 open forecasts × `docs/monitor/data/latest.json`＋`score_history.json`＋`alerts.json` 留痕＋`data/weekly_cache`，判 resolved_yes／resolved_no／void（series 停更或口徑變更則 void，不硬判）。
- 算 Brier =(p−outcome)²；輸出 `knowledge/forecast_settlement.json`（**衍生物，gitignore，本地重算**——同 settlement.json 待遇）。
- `q.py --forecasts [source]`：open 清單＋到期提醒；resolved ≥20 筆的 source 出校準曲線（10 桶）＋Brier skill score（BSS = 1 − Brier/Brier_climatology，基準＝該 series 歷史無條件 base rate）。
- **樣本誠實條款**：每 source resolved < 20 筆只列 raw 不出 BSS；BSS 置信區間一併印，防小樣本自嗨。

### B5. 消費端

- Phase 1 **不上站**（knowledge/ 本地，比照 decisions.jsonl）。校準結果的用途只有兩個：①執行 rule_ledger 的 macro stance kill 條款；②2026-10 校準輪起，各 read 類 skill 的判讀權重討論有數據可引。
- Phase 2 若要上站走 noindex 頁另案。

### B6. kill condition（登 rule_ledger，tool-level）

- forecast ledger 本體：**180 天內 resolved < 20 筆，或校準結果從未被任何決策討論／校準輪實際引用** → 儀式化認定，降級或砍（automatable ≠ valuable，同 macro-analyst tool-level 條款精神）。

---

## C. 建置順序、成本與治理

### C1. 順序（建議）

1. **B 先建**：零新資料依賴、一支結算腳本＋jsonl＋q.py flag、無 cron 無頁面，一個工作天內可上；且立即讓既有 kill 條款可執行。
2. **A Phase 1**：buyback 日曆（最簡）→ CTA 觸發位 → vol-control。一支 `scripts/build_flowmap.py`＋一個 workflow＋一頁 HTML。
3. **A Phase 2**（gamma、detective 掛線）：等 Phase 1 對帳跑出第一季結果再議。

### C2. 成本

- 兩層日常運轉**零 LLM token**（純機械 cron＋本地結算）。LLM 只出現在 forecast 草案擬定（依附在既有 read skill 的跑次上，邊際成本 ~0）。
- 開發量級：B ≈ 1 腳本＋q.py 改動；A ≈ 1 build 腳本＋1 workflow＋1 頁面＋1 小日線 cache。

### C3. 治理登記（commit 時履行）

- rule_ledger 新增三條：A6 兩條模組 kill＋B6 一條 tool-level kill。
- 「加一提刪一」候刪提名（供持有人挑一）：①crowding 主題熱力圖 64+ 主題分數（是否有 read-through 實績）②detective composites 中生命週期內零轉移的規則 ③monitor fear_greed 合成分數（與判讀引用率對查）。

### C4. 呈現層風格與發包（2026-09-01 持有人補拍板）

- **成品（站上頁面）一律外資券商 sell-side 風格＋白話＋深入淺出**：每個數字先講「這在告訴你什麼」再列數值；術語處置遵循 `_plainlang_styleguide.md`（三鐵律＋四句式＋禁流程劇場＋全形標點），優先沿用 2.5（Monitor+Detective）與 2.8（Crowding）分組既有譯名，不得即興新譯。CTA／vol-control 這類機制要用「誰、在什麼條件下、被迫做什麼、量多大」的白話句式開場，公式與門檻降為小字或折疊。
- **發包模型**：實作（scripts／workflow／頁面樣板）＝ sonnet（路由表「機械層 script／網站樣板」列）；判斷已在本設計稿凍結，sonnet 不得自行改動模型選型、門檻、kill conditions。驗收＝orchestrator（opus 端）對照本設計稿逐項檢查＋白話風格抽查。

### D. 明確不做（本設計稿範圍外）

- 趨勢追蹤 paper track（第三案，另出 PREREG 設計）；nowcast 層（第四案）；regime playbook（組合層，涉 pm 語言另議）。
- 不動既有 skill 檔、不動 nav、不動 crowding／detective／monitor 任何現行管線。
