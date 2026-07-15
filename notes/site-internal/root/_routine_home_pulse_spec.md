# 首頁「市場脈動」生成規格（home-pulse）— 純機械引擎

**引擎（2026-07-15 定案）**：`scripts/build_home_pulse.py`——**純 Python、零 LLM、確定性**。由 GitHub Actions `home-pulse-daily.yml`（`workflow_run` 事件驅動：monitor 或 radar 日更 workflow 跑完就重生；cron `0 1 * * 2-6` fallback）自動跑並 push main，zero-churn 寫入。
**為何機械而非 LLM**：內容是「只陳述事實＋機械偵測轉折」（見下），不需要判斷；且雲端 LLM routine 有 push-to-main 403 bug（#58141）推不上 main，而站上「會自動更新的一律是機械層、LLM 分析一律手動」是既定模式。原雲端 routine `trig_01JcweZyEd74QKZeFq4ri6UC` 已停用（enabled=false）。本檔＝腳本行為的權威文件（演算法＋哲學）。

**定位**：首頁整合摘要，把兩個**日更**源收斂成簡短的市場現況陳述。

**內容哲學（持有人 2026-07-15 拍板）＝陳述事實、不做判斷分析，但有可能轉折時要提醒**：
- **只陳述市場事實**：數字、分位、軌跡、象限狀態。不寫判讀語、不下結論、不做投資判斷（禁「屬正常波動」「未見翻折」「估值偏貴」這類分析框架語；禁擇時；禁買賣指令）。
- **轉折要提醒**：當某條指標出現可能的趨勢轉折（象限跨界、動能翻向、分位軌跡翻折），寫進 `reversal_flags` 並在首頁以醒目「⚠ 轉折提醒」呈現。**已確認的轉折**（持穩 ≥3 日）與**接近中的轉折**（貼線微幅、未站穩）都值得提醒，但用字要如實區分（「持穩 6 日」vs「未站穩、接近轉弱」），不誇大。
- headline＝一句事實陳述（當前主要指標狀態＋若有轉折點出）；points＝純事實 bullet；reversal_flags＝轉折提醒。

**只用日更源**（週更的 crowding／rotation RRG 一律不納入）：
1. `docs/monitor/data/latest.json`（as_of；每條 series 的 val/pctile/p20/p60/z）＋ `docs/monitor/data/alerts.json`（近 ~15 交易日留痕）。
2. `docs/rotation/data/radar.json`（cross_asset 宇宙、120 日框架；每檔 members[].frames["120"].trail[] 有 ~30 個交易日的每日 {d, r=RS-Ratio, m=RS-Momentum}）。

## 最高原則：不硬找反轉、陳述事實（2026-07-15 持有人拍板）

**多數交易日市場是延續的。** 沒有轉折就照實陳述現況，`reversal_flags` 空陣列完全正常，不硬擠轉折充數。轉折提醒是「有才提」，不是每天要湊一條。

**轉折的分級（都可提醒，但用字如實區分）**：
- **已確認轉折**：radar 象限跨界後**持續 ≥3 個交易日**未回、且近端 r/m 位移 ~1 以上（非貼線抖動）；或 monitor 三點分位翻折 ~20–30 分位點以上。evidence 寫「持穩 N 日、位移多少」。
- **接近中的轉折**：貼 100 線微幅跨界、未站穩（<3 日或位移 <0.5）。**仍值得提醒**（持有人要「有可能轉折」就提），但 evidence 必須如實寫「未站穩／接近／微幅」，不誇大成已完成的反轉。
- 兩級都進 `reversal_flags`；沒有任何一級就空陣列。

## 趨勢反轉的判定方法（核心）

**monitor 端**——用現成三點軌跡 p60（約 3 月前分位）→ p20（約 1 月前分位）→今分位：
- 續勢：三點單調同向（例 real10y 50.8→97.2→100＝一路衝頂並釘住）。
- 反轉：方向翻折（例某軸 p60 高、p20 崩、今回升＝V 型底反轉；或 p60 低、p20 高、今回落＝頂部反轉）。
- 每個判讀句必附三點分位數字，讓「反轉」可檢驗。alerts.json 用來佐證當日動作是延續還是打斷既有 streak。

**radar 端**——對 cross_asset/120d 每個資產，比較 trail 的**近端斜率翻折**與**象限跨界**：
- 象限：r≥100 & m≥100 領先／r≥100 & m<100 轉弱／r<100 & m≥100 改善／r<100 & m<100 落後。
- 反轉訊號＝最近 ~5–10 個交易日內跨象限（領先→轉弱＝動能見頂滾落；落後→改善＝落後股回神）。用 trail 倒數兩段的 r、m 變化量判斷，不是只看最後一天位置。
- 至少點出「哪個資產剛翻面」與「誰仍在延續」。

## 輸出：`docs/home/pulse.json`（schema=home-pulse-v2）— 事實陳述＋轉折提醒

**呈現＝首頁一次顯示完，不折疊**：headline 一句事實 ＋ 監測／輪動各 2-3 條**純事實** bullet ＋（若有轉折）醒目「⚠ 轉折提醒」。bullet 陳述數字/分位/軌跡/象限狀態，**不寫判讀語、不下結論**。

```json
{
  "schema": "home-pulse-v2",
  "monitor_as_of": "YYYY-MM-DD",   // = monitor latest.json as_of
  "radar_as_of": "YYYY-MM-DD",     // = radar.json as_of（可與 monitor 差一交易日）
  "written_at": "ISO8601",
  "headline": "一句事實陳述（≤ ~44 字）：當前主要指標狀態；若有轉折點出，不下投資結論",
  "monitor": {
    "points": ["2-3 條純事實 bullet：分位/z/三點軌跡/絕對值，陳述狀態不做判讀（如『實質利率分位 100（50.8→97.2→100）』）"]
  },
  "radar": {
    "points": ["2-3 條純事實 bullet：象限狀態＋RS-M（如『美股 SPY 在領先象限、新興市場在轉弱象限（連 14 日）』）"]
  },
  "reversal_flags": [
    {"axis": "如 黃金 GLD、比特幣 IBIT 動能", "from": "舊象限/態", "to": "新象限/態", "evidence": "轉折交易日＋持穩天數/位移；接近中的寫『未站穩、接近』"}
  ]
}
```

- 無 `trend`、無 `detail` 欄——首頁不折疊、不放判斷標籤，只陳述事實。
- `reversal_flags` 首頁以「⚠ 轉折提醒」醒目呈現（已確認＋接近中都提）；空陣列合法（無轉折就不顯示該區）。

- **精簡鐵律**：headline ≤ ~44 字；每 block 2-3 條事實 bullet、每條 ≤ ~28 字一個數字錨；寧可少一條也不要塞長句。
- 轉折若有寫進 `reversal_flags`（首頁醒目呈現）；沒轉折就空陣列、不硬湊。

## 硬規則
- **只陳述事實、不判斷分析**：寫數字/分位/軌跡/象限狀態，禁判讀語（「屬正常波動」「未見翻折」「估值偏貴」「延續為主」這類分析框架）、禁投資結論、禁擇時、禁買賣指令。轉折提醒只描述已發生或接近中的軌跡翻折，不預測轉折時點、不建議動作。
- 每條 bullet 錨定機械層數字（分位／z／RS-M／象限／絕對值）；無錨形容詞禁用。
- 軌跡若寫嚴格 p60→p20→今 時間順序（p20＝1 月前、p60＝3 月前，寫反＝全錯）。
- 中文全形標點；無鷹架語言。
- monitor 與 radar 各自 as_of 可差一交易日，分別標注，不強制同日。
- 只覆寫 `docs/home/pulse.json` 單檔，不動 index.html（首頁靠 JS 讀此檔渲染，帶過期防呆）。

## 引擎與自動化（機械，確定性）
- **生成**：`python scripts/build_home_pulse.py`——讀 monitor `latest.json`（含 status／fear_greed）＋ radar `radar.json`（cross_asset 120d），套事實模板產 points、跑象限跨界演算法產 reversal_flags，zero-churn 寫 `docs/home/pulse.json`。無資料變動＝空 diff、不 commit。
- **轉折演算法（腳本內建，權威）**：偵測近 8 交易日內 RS-M 穿越 100 → `held`（跨界後交易日數）、`disp`=|m−100|；`confirmed = held≥5 或（held≥3 且 disp≥0.5）`，否則 `approaching`（evidence 標「未站穩、接近」）；`disp<0.15 且 held<2` 視雜訊濾除。同 from→to／同級的成員合併成一條 flag。
- **發布**：GitHub Actions `home-pulse-daily.yml`（`workflow_run` 監聽 Daily Market Monitor／Daily Asset Rotation Radar 完成 + cron fallback），rebase-retry push main（比照 monitor-daily）。
- **確定性保證**（取代 LLM 的自檢——腳本天生做到）：只輸出模板化事實、絕不生成判讀語；轉折分級由門檻決定不靠判斷；軌跡永遠照 p60→p20→今 欄位順序印出，不會寫反。要改行為＝改腳本＋本檔同步。
