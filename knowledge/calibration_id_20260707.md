# ID 層裁決校準 — 第一輪（2026-07-07）

**目的**：在把 stock-analyst 接上 ID（DD 動筆前先讀 canonical ID 的 sd_verdict／clock_phase）之前，先對 ID 層的機器裁決對答案——GIGO 防線。方法與 DD 層驗屍同構（`calibration_v13_20260707.md`）：每份 ID 取 id-meta `related_tickers` 中 depth 🔴 且 beneficiary 的成分股做等權籃子，從裁決 as-of 日（`sections_refreshed.judgment`）結算至 2026-07-06，對 QQQ 算超額。腳本：session scratchpad `id_autopsy.py`（一次性；第二輪建議固化進 knowledge/）。

## 覆蓋率盤點（比報酬數字更持久的發現）

- 188 份 ID 中**只有 86 份有可解析的 id-meta、80 份有 `sd_verdict`**——102 份 legacy（v2.4 以下未 backfill）沒有機器裁決。**DD↔ID 接線的機器可讀覆蓋率只有 ~45%**，其餘只能讀散文。
- 80 份的裁決 as-of **幾乎全部是 2026-06-21**（v2.5 backfill 日）——ID 層沒有裁決歷史，本輪視窗中位僅 16 天。從現在起裁決才開始自然老化，2026-10 第二輪才有真窗口。
- sd_verdict 分布：balanced 42 / shortage 31 / split 6 / **surplus 僅 1**——「過剩」幾乎不存在，本身就是結構性偏多的訊號（或 universe 選題偏好順風產業）。
- kill_metrics ≥3 條：80 份達標（機器化程度好）；本輪未對 kill_metrics 做命中率結算（觸線是基本面門檻非價格，need position-thesis-monitor 歷史對照），列為第二輪缺口。

## 第一輪結果（77 份可結算，視窗中位 16 天）

| sd_verdict | n | 超額中位（vs QQQ） | 勝率 |
|---|---|---|---|
| shortage | 30 | **−5.4%** | 12/30 |
| balanced | 41 | +7.0% | 38/41 |
| split | 6 | +0.2% | 3/6 |

**交叉表把全部的錯定位在一格**：

| | 超額中位 | 勝率 |
|---|---|---|
| **shortage × Phase II** | **−7.5%** | **7/25** |
| shortage × Phase III/IV | +2.9~+9.8% | 5/5 |
| balanced × 全部 phase | +5.0~+8.5% | 38/41 |

shortage×II 的最差名單＝Memory Supercycle、AI Storage、HBM Supercycle、AI Networking、Liquid Cooling、WFE、Hybrid Bonding、Nuclear、Leading Edge——**清一色 AI 硬體/半導體**，正是 6 月底至今回檔的族群。

## 判讀（誠實版）

1. **這一輪不能證明 sd_verdict 錯**。記憶體短缺物理上是真的（合約價在漲）；16 天視窗量到的是「AI 硬體回檔 + 資金輪出」這一個 rotation 事件，shortage×II ≈ AI 半導體的 sector dummy。
2. **但它暴露一個接線層面的語意風險，這與視窗長短無關**：`sd_verdict` 量的是**物理供需**，不是**可投資性**。「短缺」在爆發尾端恰恰是最危險的買點（priced-in）。同一週（6/20-22），DD 層對 MU 判觀望、SNDK 判迴避——**可投資性判斷活在 DD 層而且判對了；ID 層的機器欄位裡沒有 priced-in / 擁擠度這一軸**（ID 散文有 priced-in 模組，但沒有落 id-meta，機器讀不到）。
3. **clock_phase 的失效集中在最重要的一群**：AI 硬體全標 Phase II（擴張中段），而 crowding monitor 同期把 AI 交易標為高度擁擠。Phase III/IV 標籤的籃子全數跑贏（8/8、13/13）——時鐘對「已經走過半場的產業」標得準，對「正熱的產業」系統性樂觀。這與 DD 層驗屍的結論（26 週漲幅位置才是分割線）互相印證。

## 對 DD↔ID 接線的直接指令（GIGO 防線設計）

1. **`sd_verdict` 以「物理狀態證據」身分被消費，禁止當方向訊號**——DD 引用時的標準句式是「產業物理供需＝短缺（ID:{theme}，as-of {date}）」，可投資性（priced-in、循環位置、擁擠度）仍由 DD §14 自判。這使接線的 GIGO 風險大幅下降：事實錨比方向錨難錯。
2. **`clock_phase` 消費時對 Phase II 打折**：Phase II＝本輪校準中唯一失效的標籤格，DD 引用 Phase II 時必須用自己的位置閘（26 週漲幅錨／QC-42 位置錶）交叉驗證；Phase III/IV 可直接引用。
3. **id-meta 缺一個 `priced_in` 機器欄**（散文有、機器無）——industry-analyst 下次版本應把 priced-in 模組的結論落欄（如 `priced_in: low/mid/high`），這是 ID 層對「shortage 陷阱」的自我保護。
4. 102 份無機器裁決的 legacy ID：接線時只作散文參考、不入機器對帳；是否 backfill 由 ID regen 專案排程決定。

## 下一輪

2026-10 與 legacy DCA／v13 兩份校準同步跑（屆時 ID 裁決視窗 ~3.5 個月、跨財報季）：重跑 sd_verdict×phase 交叉表、補 kill_metrics 命中率（對照 position-thesis-monitor 歷史）、驗 Phase II 打折規則是否仍需要。腳本固化進 `knowledge/`。
