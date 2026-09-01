# Phase 1.5＋§F＋§G 驗收紀錄（2026-09-01，orchestrator 驗收，全部未 commit 待持有人取捨）

設計依據：`_flowmap_forecast_ledger_design_20260901.md`。五包 sonnet 實作全落地，逐包驗收結果與取捨要點如下。

## 驗收結論（逐件）

| # | 成品 | 驗收 | 關鍵實測 |
|---|---|---|---|
| 1 | 槓桿 ETF 再平衡（flowmap 模組 4） | ✅ | 12/12 AUM；K_NDX=248.12 手驗吻合；NDX +1% 日→尾盤 $2.48bn 同向 |
| 2 | 月末再平衡（模組 5） | ✅ | 8 月分岔 +2.29pp→中桶賣股買債；生效窗判定正確 |
| 3 | §F 自動迴路（週更結算＋成績單＋RV 自動落帳＋季度重估） | ✅ | 成績單三模組 🟡 正確基線；α=0.10 精確二項檢定；COT 類別＝non_commercial（快取僅 legacy 口徑，已揭露）；agent 誤寫 2 筆已回滾驗證 |
| 4 | RV producer | ✅ | 轉移表單調 0.71→0.27（2470 obs）；本月兩筆草案 p=0.65／0.19 待 --write |
| 5 | 趨勢 paper track（TSMOM） | ✅ | 9 檔 8 持有、TLT 現金（12-1=−0.47%）；NAV 三線 100 起跑；簿記 keyed by booked ticker 無錯帳風險 |
| 6 | statlab 相關性 | ✅ | SPY-TLT +0.33（77 分位）；sector 兩兩 0.132（**3 年 1.1 分位**，同步度三年最低） |
| 7 | statlab VIX 期限結構 | ✅（信心中） | slope +2.61 contango、3 年 10 次倒掛；**^VIX3M feed 45 天真空（7/17–8/31）**，缺口防呆＋gaps 誠實 |
| 8 | vix-model producer | ✅ | base rate：21d 回正 96.9%（31/32）、63d SPY 更高 71.9%（23/32）；今日無事件 exit 0 正確；即時性受同一 feed 真空約束 |
| 9 | COT 極端統計＋cot-model | ✅（前提存疑，見下） | 極端燈：NDX 3.2、2Y 100、銅 98.1 分位；今日一筆真事件草案（QQQ >716.76 at_expiry p=0.25）dry-run |

## 兩個實質發現（取捨的核心輸入）

1. **COT「極端反轉」前提在樣本內是反的**：兩套獨立實作交叉確認（statlab 28.2%／39 事件 vs cot_base_rates 25.0%／48 valid，lookahead 口徑不同故數字略異）——2021–2026 權益指數 COT 極端後**延續佔約 72–75%**。cot-model 誠實引用 p=0.25，落帳的實質是延續命題的鏡像。SPX 單市場 n=2 無意義，實作已只用 pooled。
2. **^VIX3M 上游資料真空**（yfinance 源頭，agent 直接查證非本方 bug）：VIX 模組與 vix-model 的即時 onset 偵測目前可能滯後數週，generator 以「用最後可得日＋stale 警告」誠實處理。

## 已知偏差（全部已揭露、待持有人裁）

- §F：α=0.10 為 agent 選值（設計稿未定）；🔴 範圍擴為「未顯著優於擲硬幣」（含顯著更差，超集）。
- trend track：7/9 fail-safe 地板、DBC/PDBC 每輪重評（簿記安全已驗證）、420 日窗。
- cot-model：20 交易日精確索引（與 statlab 的 +28 曆日近鄰法刻意分歧，各自文件化）；多市場同觸發允許部分落帳；lo 樣本門檻 20 為 agent 選值。
- statlab：快取 850 交易日（衍生序列分位的計算前提，非放寬窗長）。

## 待辦（取捨後）

- rule_ledger 補登 5 條 kill（月末模組／rv-model／vix-model／cot-model／trend track）＋加一提刪一提名。
- commit 分組（並行 session 四步自檢）：flowmap 1.5＋§F／statlab／trend-track／producers＋settle 域。
- 六筆 macro harvest 草案 p 值仍待持有人賦值。
- Phase 2 候選持續掛起：dealer gamma、flowmap 掛 detective、指數再構成、crowding 頁改版另案。
