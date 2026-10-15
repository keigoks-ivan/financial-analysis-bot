# TokenEconomics 20261014：閘紅燈局部修正紀錄

範圍：只修 gate_2 的紅燈與屬於事實或算術錯的黃燈。這次不動估值輸入（Part 1 跳過，priced_in、plan.json 都沒改）。sd_verdict、clock_phase、conviction、*_boundary、base_rate.action 全部不動。
備份：judgment.pre_local.json、evidence.pre_local.json、plan.pre_local.json。逐欄變更清單：scratchpad `te_fix.log.json`。
重跑結果：gate PASS（紅 0，黃 9），prose PASS，check PASS（check_id rc=0，validate rc=0，81KB）。交界句「短缺／分裂交界」仍在頁面上。

## 一、紅燈

### 紅 1：id_meta.future_state 超過字數上限（J5／meta）
- 前：「…還會往下收斂；持平線依降價速度落在 1.6 到 2.9 倍之間，用量增速一旦跌破，總支出就縮。…」，共 252 字。
- 後：「…還會往下收斂，跌破 1.6–2.9 倍的持平線，總支出就縮。…」，共 235 字。
- 數字與裁決不變。

### 紅 2：capex／折舊寫成「≥1.6 倍」下限（D2）
- 查證：MSFT FY2026 10-K 的不動產與設備折舊費用是 $34.3B，FY2025 是 $22.0B（SEC XBRL us-gaap:Depreciation，accn 0001193125-26-323660，T1）。新增證據 **X1**，填補 NF-D「沒有公司一手折舊數字」的缺口。
- 算式：115.9 ÷ 34.3 ≈ 3.38，約 3.4 倍。FY25 是 64.551 ÷ 22.0 ≈ 2.93，約 2.9 倍。閘的重跑已獨立驗過 3.38 與 2.94。
- **方向和委託書的前提相反**。委託書與 gate_2 認為推算式低估折舊，所以 1.6 倍是上限。揭露數字顯示推算式反而把折舊高估了一倍多：推算值約 $73.9B，揭露值 $34.3B。原因有兩個。第一，推算式把 FY25 的 capex 當成前 4.5 年每一年的值，但更早年度的 capex 小很多。第二，推算式把全部 capex 都按 5.5 年攤，建物實際攤 15–25 年。所以 1.57 其實是下限，實際值是 3.4 倍。這次的修法是直接換成揭露數字，不再用推算值，也不再寫「≥」或「至少」。
- 改動欄位：
  - mechanics.verdict.capital_cycle[0].name：「capex／折舊（MSFT，推算下限）」→「capex／折舊（MSFT FY26，公司揭露）」。
  - capital_cycle[0].value：「≥1.6 倍：115.9 ÷ [(115.9 ＋ 64.6 × 4.5) ÷ 5.5]」→「約 3.4 倍：capex $115.9B ÷ 折舊 $34.3B；FY25 為 64.6 ÷ 22.0 ≈ 2.9 倍」。cite 改成 D5、B4、X1。
  - mechanics.verdict.synthesis：「capex 至少是折舊的 1.6 倍，交期長，租價仍在漲…」→「MSFT capex 是折舊的 3.4 倍（10-K 揭露），通路交期 36–52 週，輝達 Q3 指引仍季增約 12%，週期仍處擴張段。H100 租價各指數讀數落在 $2.53–3.39，看不出方向，只當輔證。…」
- 對結論的影響：擴張段的讀法更強，clock_phase 維持 II。
- 未查證：capex（D5 現金口徑）與折舊是否同樣含融資租賃資產。這點已寫進 X1 的 note。

### 紅 3：H100 租價被寫成仍在上漲（J2／D3）
- 證據：姊妹篇 AIComputeCapexCycle 用的是隨用隨租中位價，$3.39（2026-09-03）。B18 的另一追蹤站在 9/6 報 $3.06。本篇 D9 的 Silicon Data 指數是 $2.85（10/13），同頁另有一筆 $2.53。SemiAnalysis 的現貨合約價在 2026-02 是 $2.83（B18）。這幾個數字來自不同指數，價差不能讀成下跌，也不能讀成上漲。同一指數的 26 週序列查不到：搜尋過一次，沒有找到 Silicon Data 在 4 月有日期的讀數。唯一的變動數據是 D9 的 7 日 +7.1%。
- 改動欄位：
  - thesis.sister_reconcile[0].reason：原文是「與本篇的算力半邊一致（H100 週增 7.1%，D9）」。改寫為：算力短缺的錨改成輝達 Q3 指引季增約 12%（B2）與通路交期 36–52 週（D17）；並列出三個指數的口徑與讀數，寫明這組價差看不出方向。
  - mechanics.verdict.gate_necessary：「H100 租賃指數的 26 週變化轉為負值（目前仍在上漲）」→「Silicon Data H100 租賃指數以 2026-10-13 的 $2.85 起算，26 週變化轉為負值（目前只有 7 日讀數，趨勢未定）」。
  - 同一個「週增 7.1%＝算力仍緊」的寫法還出現在其他欄位，一起改掉。算力短缺一律改用 B2 與 D17 當錨，H100 降為輔證：
    - id_meta.now_state：「算力撮合價反而走強，H100 每小時 $2.85、週增 7.1%…」→「算力層仍緊：輝達 Q3 指引季增約 12%，通路交期 36–52 週；H100 每小時 $2.85，租價方向未定。」
    - id_meta.sd_verdict_detail：「H100 租價週增 7.1%」→「通路交期 36–52 週」。sd_verdict 本身不動。
    - thesis.points[2]、thesis.sd_points[0]、thesis.exhibit.rows[3]（讀法由「算力仍緊」改為「各指數讀數不一，方向未定」）。
    - base_rate.differences[1].point：引用由 D9、B2 改為 B2、D17。base_rate.action 不動。
    - mechanics.supply.h3：「瓶頸在算力：租價還在漲，存貨開始堆積」→「瓶頸在算力：指引仍季增 12%，存貨開始堆積」。
    - mechanics.verdict.capital_cycle[3].value：補上「只有 7 日變動 +7.1%，26 週起點查不到」。
    - risks.kill_table[0].now 補同一段說明。kill_table[0].manipulable 補一句：$3.39 是隨用隨租中位價，屬不同指數，不能直接比。
- thesis.cite 補上 D17、B18。

### 紅 4（gate_1）：base 價格因子 0.64 與 K2 持平線 1.6 倍（D4）
- 目前的 judgment.json 已經處理過，這次不改：base 在 2027 年用 D11 的 0.35，2028 年以後才回到 A12 的 0.64，並寫明「屬判斷，不是實測」；K2 已改成多個降價速度下的持平線（1.6／1.9／2.9 倍）；future_state 與 kill_metrics 也同步改了。gate_2 沒有再把它列成紅燈。

## 二、gate_2 黃燈裡屬於事實或算術錯的部分（已修）

- **J9**，mechanics.verdict.horizons[1].bull：「用量年增維持 3 倍，2028 年約 $240B」→「用量年增依序 4、3 倍，2028 年約 $240B」。驗算：90 × 4 × 3 × 0.35 × 0.64 ≈ $242B，和 TAM 表的 bull 路徑一致。
- **D3**，MSFT「屬會計口徑」的歸因，mechanics.verdict.bear_narrative：原文把 MSFT 曆年 capex 指引由約 $190B 降到 $175B 寫成「屬會計口徑」並當作前例。改寫為：這個說法只見於次級摘要，原因未確認，另有 FY27 約 $255–260B 的未證實說法，暫不當前例（B5、C11）。verdict.cite 補上 C11、B2、X1。
- **D3**，「客製矽占比 15.8%」的分子含網通：
  - 指標統一改名為「博通 AI 營收占比」，涉及 thesis.derivation、debates[1] 的 our_view／signal_pos／signal_neg／falsifier、mechanics.supply.read、horizons[2].trigger。
  - 加註只算 XPU 的值：16.7 × 0.73 ≈ 12.2，12.2 ÷（89.0 + 12.2）≈ 12.0%（B13）。也加註分母沒有納入 Trainium、MTIA 與 TPU 自用。
  - 20% 與 25% 兩個門檻沒有改，只把量的是什麼寫清楚。
- **D11**，AMD 用了不同季的分母，stocks.rows[5].derivation：改寫為「Q2 資料中心 $6.7B；同季總營收不在證據包，Q3 總營收指引約 $13B 屬不同季，只能看量級」。purity 30 不變。
- **D9**，summary.kill_brief[1].now：補上「估算」兩字。

## 三、跳過（屬判斷，或無法查證）

- gate_2 的 D4 黃燈：$90B 基期取幾何平均、2025 年基期 $45B 沒有來源、demand_5y_multiple 2.8 偏軟。這是情境假設的判斷，證據包裡沒有 2025 年的對外 token 支出。重跑後的閘仍列為黃燈。
- gate_2 的 D9 黃燈：K2 一年只能觀測一次，需要改用季頻的替代量測。這要重新設計 kill 線，屬判斷，這次只補了「估算」標記。
- gate_2 的 D11 黃燈：GOOGL、AMZN、MSFT、META、NET 的純度沒有分母。這需要補合併營收的證據，查詢次數不夠，跳過。
- gate_1 的黃燈（gate_2 沒有重提）：Trainium 列寫「晶片年化營收逾 $25B」，C15 原文是 Chips 事業；以及上緣 $730B 只採 MSFT $175B。不在本次範圍。
- 重跑後閘新列的黃燈：讓利四判準站不穩、K1 的 $2.40 閾值太敏感、買方自由現金流證據只有單季。都屬判斷，沒有修。

## 四、交持有人

1. **紅 2 的方向**：委託書要求把 1.6 倍改寫成上限。一手 10-K 的數字顯示 1.6 倍其實是下限，實際值是 3.4 倍。這次照一手數字改，請確認接受。
2. **sd_verdict 的措辭（重跑後 gate J9 黃燈）**：閘認為「裁決錨在算力層」等於 shortage，與 split 不一致。sd_verdict 本身已經是交界（短缺／分裂），動它要持有人決定。這次只把錨換成 B2 與 D17，沒有動裁決。
3. **META 估值輸入可能異常（重跑後 gate D8 黃燈）**：META 現價 Fwd P/E 24.5，DD 日是 17.1，分位由 33 跳到 100，26 週卻只漲 8.1%，很可能是 FY2 EPS 預估資料異常。這屬於 Part 1 的程式輸入，這次沒動。如果是資料錯，「買方溢價」的論據與 priced_in 都要重看。

## 五、查詢紀錄（7 次，上限 8 次）

1. SEC 8-K Ex.99.1 現金流量表：「Depreciation, amortization, and other」FY26 $38.5B。這一行含其他項目，不採用。
2. 同一頁重抓一次確認，數字相同。
3. 搜尋 MSFT 10-K 折舊費用：摘要寫 $34.3B，當線索用。
4. 10-K 全文第一段：附註被截斷，讀不到。
5. 10-K 全文第二段：同樣讀不到。
6. SEC XBRL companyconcept us-gaap:Depreciation：確認 FY26 $34.3B、FY25 $22.0B、FY24 $15.2B，採用為 X1。
7. 搜尋 Silicon Data H100 指數 4 月的讀數：查不到有日期的值。
