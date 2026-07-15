# 首頁「市場脈動」每日生成規格（home-pulse）— routine 每交易日照此跑

**定位**：首頁整合摘要，把兩個**日更**源收斂成「過去 1–3 個月趨勢 × 當日交互 → 趨勢有沒有反轉」。與 monitor editorial 同家族的描述器紀律（禁擇時結論、禁買賣指令），但視角不同：monitor editorial 是當日跨資產快照；home-pulse 是**趨勢反轉偵測**。

**只用日更源**（週更的 crowding／rotation RRG 一律不納入）：
1. `docs/monitor/data/latest.json`（as_of；每條 series 的 val/pctile/p20/p60/z）＋ `docs/monitor/data/alerts.json`（近 ~15 交易日留痕）。
2. `docs/rotation/data/radar.json`（cross_asset 宇宙、120 日框架；每檔 members[].frames["120"].trail[] 有 ~30 個交易日的每日 {d, r=RS-Ratio, m=RS-Momentum}）。

## 最高原則：不硬找反轉，順勢就順勢（2026-07-15 持有人拍板）

**多數交易日市場是延續的，不是反轉的。** 「趨勢延續、無重大變化」是**第一級合法輸出**，不是次等結果——headline 該說延續就大方說延續，不要每天硬擠一條反轉出來充數。低變化日照實寫低變化，`reversal_flags` 空陣列完全正常。

**反轉的材料性門檻（達不到就不是反轉，只是雜訊）**：
- radar 象限跨界：RS-Momentum 剛好貼著 100 線、幅度 <0.5 的單日擺動**不算反轉**——那是 RRG 在中軸的正常抖動。要算反轉，需 (a) 跨界後**持續 ≥3 個交易日**未回，且 (b) 位移幅度夠大（近端 r 或 m 至少移動 ~1 以上，不是 100.1↔99.8 的來回）。達不到門檻的，寫進 line.text 當「動能轉軟／轉強」的**次要觀察**，**不進 reversal_flags、不上 headline**。
- monitor 三點分位：軌跡翻折要夠深（折返幅度 ~20–30 分位點以上）才算反轉；小幅回檔是續勢中的正常波動。
- headline 預設用**延續語言**；只有存在真正過門檻的反轉時才以反轉為主句。若當日只有邊際擺動，headline＝「趨勢延續＋（可選）某軸動能邊際轉軟」，不誇大成反轉。

## 趨勢反轉的判定方法（核心）

**monitor 端**——用現成三點軌跡 p60（約 3 月前分位）→ p20（約 1 月前分位）→今分位：
- 續勢：三點單調同向（例 real10y 50.8→97.2→100＝一路衝頂並釘住）。
- 反轉：方向翻折（例某軸 p60 高、p20 崩、今回升＝V 型底反轉；或 p60 低、p20 高、今回落＝頂部反轉）。
- 每個判讀句必附三點分位數字，讓「反轉」可檢驗。alerts.json 用來佐證當日動作是延續還是打斷既有 streak。

**radar 端**——對 cross_asset/120d 每個資產，比較 trail 的**近端斜率翻折**與**象限跨界**：
- 象限：r≥100 & m≥100 領先／r≥100 & m<100 轉弱／r<100 & m≥100 改善／r<100 & m<100 落後。
- 反轉訊號＝最近 ~5–10 個交易日內跨象限（領先→轉弱＝動能見頂滾落；落後→改善＝落後股回神）。用 trail 倒數兩段的 r、m 變化量判斷，不是只看最後一天位置。
- 至少點出「哪個資產剛翻面」與「誰仍在延續」。

## 輸出：`docs/home/pulse.json`（schema=home-pulse-v1）

```json
{
  "schema": "home-pulse-v1",
  "monitor_as_of": "YYYY-MM-DD",   // = monitor latest.json as_of
  "radar_as_of": "YYYY-MM-DD",     // = radar.json as_of（可與 monitor 差一交易日）
  "written_at": "ISO8601",
  "headline": "一句話：當前哪條趨勢正在／剛反轉（趨勢語言，非漲跌快照）",
  "monitor_line": {
    "text": "2-3 句：貼現率／胃納／流動性主軸的趨勢與今日是延續或反轉，每句帶三點分位",
    "trend": "extending|reversing|mixed"
  },
  "radar_line": {
    "text": "2-3 句：cross_asset 120d 領先／落後結構，誰剛翻面誰仍延續",
    "trend": "extending|reversing|mixed"
  },
  "reversal_flags": [
    {"axis": "如 實質利率 / 新興市場股 / 高收益債", "from": "舊態", "to": "新態", "evidence": "三點分位或象限跨界＋當日錨"}
  ]
}
```

- `reversal_flags` 空陣列合法（沒有反轉就誠實空著，headline 改寫成「趨勢延續、無反轉」）。
- 不硬湊反轉；沒反轉時價值在「確認趨勢仍完整」。

## 硬規則
- 描述器紀律：禁「即將反轉／見頂／該買該賣」作結論；「反轉」只描述已發生的軌跡翻折，不預測未來轉折時點。
- 每個判讀句錨定機械層數字（分位／z／RS-M／象限）；無錨形容詞禁用。
- 軌跡句嚴格 p60→p20→今 時間順序（p20＝1 月前、p60＝3 月前，寫反＝全錯）。
- 中文全形標點；機構研究語調；無鷹架語言。
- monitor 與 radar 各自 as_of 可差一交易日，分別標注，不強制同日。
- 只覆寫 `docs/home/pulse.json` 單檔，不動 index.html（首頁靠 JS 讀此檔渲染，帶過期防呆）。

## routine 每日流程
1. 讀上述兩源原始檔（親自核對每個數字）。
2. 依趨勢反轉方法產出 pulse.json。
3. `python3 -c "import json;json.load(open('docs/home/pulse.json'))"` 驗證。
4. commit（訊息 `home-pulse: 每日市場脈動 YYYY-MM-DD`）→ rebase-retry push（比照 repo canonical push 迴圈）。

## 品質防線（無 critic gate，但自檢四題）
1. 反轉題：今天有沒有**過門檻**的趨勢翻折（持續 ≥3 日＋幅度夠大）？沒有就大方說沒有，不硬湊；貼著 100 線的邊際擺動一律不算。
2. 續勢題：哪條趨勢仍完整、明說延續。若當日主軸就是延續，headline 就用延續語言，不要為了「有東西講」而升級雜訊為反轉。
3. 軌跡題：≥3 句 p60→p20→今，逐句自證方向沒寫反。
4. 誠實題：反轉是「已發生且過門檻的軌跡翻折」還是「我在預測／在放大雜訊」？後兩者一律刪。
