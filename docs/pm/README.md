# docs/pm/ — 出場閉環（Portfolio Monitor）

這一層是「出場閉環」：把選股系統的產出當成**真實組合**來監控與汰換分析。
核心原則（用戶 2026-07-19 拍板）：**系統選出來的組合＝真實組合**——持倉不是手填的
券商部位，而是選股系統自己的產出。監控與汰換分析都針對這個組合。

## 檔案

### `holdings.json` — 系統組合快照（真源）

由 `scripts/build_holdings.py` 產生（掛在 `weekly-engine.yml`，排在引擎鏈之後）。
`source: "system-selected"`。三塊：

- **`index_sleeve`** — 指數部：讀 `docs/long-track-w52-adaptive/state.json` 的
  W52×自適應波動率引擎美台目標曝險與成分（QQQ／SMH／0050／2330，含各自 executed_pct
  與 gate）。這是規則引擎的產出，沒有個股論點，故監控只摘要其目標曝險、不跑論點掃描。
- **`stock_sleeve`** — 個股部：決策引擎**席位擂台的在席者**（`core_seats` 核心＋
  `sat_seats` 衛星），每檔含 seat、上位日期（`seat_since`，由 `docs/engine/arena-ledger.json`
  append-only 帳本推算；`seat_since_at_least` 為真＝帳本起點就已在席、實際更早）、對應
  最新 DD 檔名／`dca_verdict`／`funnel_rank`（查 `docs/dd-screener/latest.json`）。
- **`challengers`** — 擂台當前挑戰者名單（汰換候補）。`beats_seats` 列出該挑戰者引擎
  分數已勝過的在席 ticker（空＝未觸發擂台警報）。

zero-churn：內容不變不重寫（比較排除 volatile 的 `generated_at`）。

### `flags.json` — detective 持倉警報對帳

由 `scripts/build_pm_flags.py` 產生（掛在 `detective-daily.yml`，detective build 之後、
`continue-on-error`）。每日交叉 `holdings.json` 的持倉 ticker 與市場偵探當日產出
（`docs/detective/data/latest.json` 的 signals ＋ `kill_watch.json` 的 kill 指標）：
凡持倉股被任一警報命中即記一筆，**accumulating**（`first_seen`／`last_seen`／`status`：
active＝當日仍命中、cleared＝曾命中今日不再）。detective 多為總體/市場層訊號，單一
持倉股命中通常少見——命中數 0 是誠實結果，機制照樣把帳記著供人眼快查與下次週報對帳。

### `MONITOR_YYYYMMDD.md` — position-thesis-monitor 週報

由 `position-thesis-monitor` sub-agent 產生（`.claude/agents/position-thesis-monitor.md`）。
掃描範疇＝`holdings.json` 的在席者，對每檔跑論點健康掃描（DD 鮮度、證偽指標越線、
催化劑複盤、承保差異等），並新增：

- **席位擂台對比**（Check 13）：挑戰者 vs 在席者，證據面（DD 裁決＋funnel_rank＋動能）
  明顯翻轉時輸出 **SEAT_CHALLENGE「建議換席」**；在席者論點惡化／逼近 kill 邊界輸出
  **SEAT_REVIEW「建議剔除複審」**。
- **detective 持倉警報對帳**（Check 14）：把 `flags.json` 的 active 命中交叉進對應持倉。

**怎麼讀週報**：先看頂部「Triage 摘要」表與「Top 3 立即動作」定調注意力去向；
🔴/🚨 級才需深看，🟢 HEALTHY 一列帶過。所有裁決是**建議**、非指令。

## 換席永遠人工拍板

系統組合＝真實組合，故換掉在席者＝真的換倉。正因如此，**任何換席（含 SEAT_CHALLENGE／
SEAT_REVIEW）永遠由人工拍板**。build 腳本與 monitor agent 只把對戰擺好、把惡化訊號浮上
複審桌，引擎不自動換席、agent 不下換倉指令。
