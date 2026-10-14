# ID v4 冷讀報告：AI 儲存（ID_AIStorage_20261014）

審查範圍：id-review ID v4 mode，J1–J10。只讀 excerpt、check_id.py 報告，其餘以 grep 與外部查證補足。web 查證共 6 輪（上限 10）。

## 裁決

**THESIS_INTACT（結論站得住），但有 6 項 🟡 需要在發布前或下一版修。**
計數：🔴 0／🟡 7／🟢 3。

核心問題「Phase II 回退是否站得住」：**站得住**，但理由要換。頁面現在的論證（Kioxia 營益率指引仍升）是最弱的一條，另有三條更強的證據（Micron 官方說法、合約價仍為正、營收指引逐季增）沒用上；同時，頁面自己設的「撥到 III」觸發點，被 Micron 9/30 的指引提前踩到了，頁面沒發現。

## J 逐項

| # | 判定 | 摘要 |
|:--|:--|:--|
| J1 | 🟢 | cornerstone 數字（Micron 87.0%／86.25%、$61.5B、FQ4 營收 $54.23B／FY26 $133.19B、存貨 $10.4B）對 Micron 9/30 prepared remarks 查證相符。企業級 SSD 位元占比 48%（Counterpoint 二手）已標二手。 |
| J2 | 🟡 | priced_in 與姊妹篇口徑分歧、NAND kill 門檻比姊妹嚴未交代，見 Y3。 |
| J3 | 🟡 | 資本週期證據過時（Y1）、TAM 基期偏低（Y6）、SNDK 5 年分位無效（Y5）。 |
| J4 | 🟢 | 四張分歧卡皆帶數字與雙路徑，威脅卡（YMTC 14%）附判別訊號。 |
| J5 | 🟡 | 機器欄與內文方向一致（split／II／mid）；PSTG、NTAP 標 beneficiary=true 與內文「NAND 是成本項」矛盾，見 Y7。 |
| J6 | 🟡 | 時鐘回退可辯護；priced_in=mid 未處理擁擠度反證，見 Y3。 |
| J7 | 🟢 | kill 表含市場撮合價（晶圓現貨），閾值非與公司指引同源。 |
| J8 | 🟡 | 判斷手冊 #18（Phase 轉換雙閘須含第二個獨立訊號）實答不合格，見 Y2。 |
| J9 | 🟡 | pm_actions 與 kill 表動作不一致，見 Y4。 |
| J10 | 🟢 | 主閱讀線白話度可，未見內部代號外漏（check_id.py 流程劇場 0 處）。 |

## Phase II 回退是否站得住（J6 重點）

**站得住。證據：**
1. Micron 9/30 prepared remarks：「We anticipate fiscal Q1 to be the floor for gross margins in fiscal 2027… higher gross margins beyond fiscal Q1 for the remainder of fiscal 2027, with a more moderate rate of price increases.」86.25% 的小降是 FQ4 把加碼獎金吃進存貨、在 FQ1 出貨時反映的成本時點效應，不是價格轉弱。頁面把它歸為「雜訊」是對的，但沒引用這句，錯過最強證據。（來源：https://s25.q4cdn.com/621799436/files/doc_financials/2026/q4/Q4-FY26-Prepared-Remarks.pdf，2026-09-30）
2. Micron 稱 FY27 每季營收逐季成長；價格是「漲幅趨緩」而非下跌。III 的定義是價格漲幅收斂「且」毛利下行，目前只滿足前半（預估）。
3. 三輪判 III 一致，不代表證據足夠：三輪看的是同一包證據，票數一致是同源，不是獨立確認。gate 回退符合手冊 #18「單訊號亮燈只算預警」的精神。

**反面：** 頁面對外只說「換格證據不足」，沒說清楚是哪一個閘沒過。見 Y2。

## 🟡 清單

### Y1（J3／J8，影響結論）頁面自設的「撥到 III」資本支出觸發點，已被 Micron 9/30 指引踩到
- 錯誤文字（risks 催化劑 2026-12）：「達標，且 FY27 capex ≤ FQ4 年化 $43B → 維持判斷；毛利未達指引，或 FY27 capex >$43B → 供給回應加速，準備撥到 III。」
- 正確事實：Micron 9/30 prepared remarks 已指引「fiscal Q1 capex around $11.5 billion」「first-half fiscal 2027 capex approximately $25 billion」「capex to be higher in the second half」。上半年 $25B 年化 $50B，下半年更高，FY27 capex 實質上已 >$43B。此外 Micron 稱 FQ4 存貨日數 129 天，較前季 +9 天（管理層預期之後下降）。
- 來源：同上 prepared remarks，2026-09-30。證據包（evidence.json）沒有收這兩句，頁面因此以為這個觸發點還沒發生，屬 stale evidence。
- 影響：頁面「維持 II」的第二個支點（資本回流還在早期）要改寫為「Micron 全公司 capex 已指引 FY27 高於 $43B，但構成以建廠（cleanroom，2028 底後啟用）為主，NAND 專屬產能 2028 底前不增」。這對 Phase II 結論有利（供給晚到），但頁面現在的寫法是觸發點未到，事實不符。
- 附帶：gate 已指出「資本回流」用 Micron 全公司 capex（含 DRAM／HBM）當證據，Micron NAND 只占營收 24%；頁面 thesis 仍寫「資本開始回流：Micron FQ4 capex $10.77B，年化比 FY26 全年高 57%」，範圍未收窄。
- 欄位：mechanics.verdict.capital_cycle、risks.catalysts[2026-12]、thesis.points[5]。

### Y2（J8／J6）換相雙閘的兩個「充分條件」不獨立，且第一條「查不到」被寫成「未達」
- 錯誤文字（mechanics 投資時鐘換相雙閘）：「實績合約價（非預估）季增 ≤5%：查不到。…（未達）」與「原廠實績毛利季降 ≥2pt：未見。…（未達）」。
- 問題：判斷手冊 #18 要求充分條件含「第二個獨立訊號」。合約價與毛利在因果上同源（Sandisk 自稱增量三分之二來自價格），不是獨立訊號。第一條查不到實績，應寫「未驗證」，不是「未達」。gate_1、gate_2 均已提出，定稿未改。
- 更正建議：第二訊號改用獨立變數，例如原廠 NAND 位元出貨季增（debate 2 已用）或存貨天數。證據：Memory 姊妹篇記載三星存貨天數 94.6→102.0→124.5 天連兩季上升（見 ID_MemorySupercycle_20260905 kill_metrics），頁面完全沒回應；Micron DIO 129 天（+9）亦未提。
- 欄位：mechanics.verdict.gate_sufficient。

### Y3（J2／J6）priced_in 與姊妹篇口徑分歧、kill 門檻差異未交代
- 頁面 id-meta：priced_in="mid"。ID_MemorySupercycle_20260905、ID_HBM_Supercycle_20260904、ID_AIComputeCapexCycle_20260903 三篇皆為 "high"。頁面自己寫 MU 26 週 +117.4%、NTAP +130.0% 為最擁擠，卻標 mid，理由是「倍數低」。這恰是手冊 #5 警告的情境（倍數低＝風險換地方藏），頁面有答（風險在 E），但 priced_in 欄的方向仍與姊妹相反，sister 差異段（thesis）沒有交代這一點。
- 頁面 NAND 合約價 kill＝「任一季 ≤0%」，HBM 姊妹與 Memory 姊妹為「連兩季 ≤0」。thesis 的姊妹對照只寫「未觸發」，沒說明為何更嚴（gate 已提）。
- 建議：priced_in 維持 mid 可以，但加一句「與姊妹 high 不同，因為……（本篇以 E 而非倍數判定）」；kill 門檻補一句理由（純 NAND 曝險較高）或對齊。
- 欄位：id_meta.priced_in、thesis.sister_reconcile、id_meta.kill_metrics[1]。

### Y4（J9）PM 行動與 kill 表動作不一致
- 錯誤文字（summary PM Action ①）：「晶圓現貨連 4 週 <16，或合約價任一季 ≤0%，即減碼。」
- kill 表破線後姿態：「與合約價線同時破線→進 IV，SNDK、MU 退出；單獨破線→降級觀察」。同一條線，一處說減碼、一處說降級觀察，合約價單獨破線一處寫「Phase IV，純 NAND 重資產退出」。
- 更正：統一為單條破線＝降級觀察／減碼，雙條破線＝退出，並讓 PM Action 與 kill 表同一措辭。gate_1／gate_2 皆已提，定稿未改。
- 欄位：summary.pm_actions[0]、risks.kill_table[0..1].posture。

### Y5（J3）SNDK 無法有 5 年分位，頁面仍寫「5 年第 15 百分位」
- 錯誤文字（thesis）：「MU、SNDK 倍數在 5 年第 8、15 百分位」；debate 1：「倍數在 5 年第 8–15 百分位」。
- 事實：Sandisk 自 2025-02 才從 WDC 分拆上市，不可能有 5 年分位；valuation 表同列「5 年歷史帶：查不到」卻有分位 15.0，內部自相矛盾。這兩處用來支撐「市場仍用週期尺」。
- 更正：SNDK 改寫為「上市以來分位（樣本不足 2 年）」，並以 MU 單檔作 5 年證據。
- 欄位：thesis.points[4]、debates[0].priced_in、valuation.priced_rows[0]。

### Y6（J3，不重審已標示的 TAM 估計；只報告找到的實測）2025 年產業基期有實測可用，應更新區間而非用 2Q26 份額回推
- 頁面文字：「2025 基期約 60 是粗估… 5 年倍數 330÷60≈5.5、CAGR 約 41%，其中 315÷60≈5.2 倍已在 2026 發生」。
- 我找到的 TrendForce 前五大廠逐季營收（實績）：1Q25 $12.02B（https://www.trendforce.com/presscenter/news/20250529-12600.html）、2Q25 $14.67B（https://www.trendforce.com/presscenter/news/20250828-12688.html）、3Q25 約 $17.1B（https://www.trendforce.com/presscenter/news/20251203-12813.html）、4Q25 $21.17B（https://www.trendforce.com/presscenter/news/20260303-12943.html）。四季合計約 **$64.96B（前五大，不含 YMTC 與長尾）**。
- 全產業年額未見 TrendForce 公布。以頁面自己的覆蓋率（2Q26 前五大 68.87 ÷ 份額回推 78.7＝約 87%）粗估，2025 全產業約 **$70–75B（我的推估，非來源數字）**，落在頁面 50–78 區間的上半部，高於取中值的 60。以 72 為基期，5 年倍數約 4.6 倍（330÷72），2026 年化 315÷72＝約 4.4 倍已發生；CAGR 約 35%。方向不變：倍數多數來自 2026 漲價。建議把「約 60」改為「約 70（前五大實績 65 加長尾）」，倍數改約 4.5。
- 欄位：id_meta.demand_5y_multiple（5.5）、cagr_pct_5y（41）。這是 sensitivity 內的修正，不改結論。

### Y7（J5）PSTG、NTAP 標 beneficiary=true，與內文矛盾
- 內文：PSTG「NAND 為成本項，價格回落時受益」；「儲存系統商目前被元件成本擠壓」。id-meta 卻為 beneficiary:true。NTAP 無任何純度或營收拆分證據，仍列「受益」。
- 更正：兩檔 beneficiary 改 false（或「價格回落時受益」的反向標記），NTAP 無證據改列觀察。
- 欄位：id_meta.related_tickers[PSTG, NTAP].beneficiary。

## 其他未達 🟡 門檻但建議補入的事實（供下一版）

1. **Kioxia 兩季皆低於共識，頁面只引用「營益率升」**：4–6 月營業利益 ¥1.27 兆低於共識 ¥1.37 兆；7–9 月指引 ¥1.89 兆低於 Bloomberg 共識 ¥1.95 兆（來源：https://en.sedaily.com/international/2026/07/31/kioxia-quarterly-operating-profit-tops-1-trillion-yen；https://www.bitget.com/news/detail/12560605591557 等彙整，2026-07-31）。頁面以「營益率 72%→79%」作為否決 III 的承重證據，evidence.json B10 註記「僅讀搜尋摘要」，頁面未標示。方向（營收季增 35%、營益率升）屬實，但漏掉「低於預期」這項反向證據。
2. **SK hynix 3Q NAND 位元出貨**：evidence.json（Nasdaq 法說摘要，T3-B）記載「3Q NAND 位元出貨預期僅低個位數成長」，但後續 S6 註記「釋出稿未載 3Q 出貨%」，屬未證實。頁面 debate 2 用 Q2「十幾 %」支持「位元端溢出」，沒提這個說法。若屬實，則 debate 2 的觸發條件（連兩季 ≥10%）本季不會滿足，偏向「晶圓真的卡死」那條路徑。
3. **MU FY2 口徑**：頁面「現價÷FY2 倍數 6.5≈EPS $152＝下季指引×4（38.15×4＝152.6），市場已假設高峰獲利撐到 2028 年中」。Micron 稱 FY27 逐季成長、FQ1 為毛利率底部，若 FY2 實為 FY2027，則 EPS 152 低於指引軌跡（逐季成長會高於 4×38.15），結論會反轉為「市場已預期下行」。gate 已提 FY2 對應年度未確認，定稿仍寫死 2028。這一項若查實反向，將動到 key_call，目前降級列 🟡 是因證據包無法判定。建議以 dd-screener 的 FY 欄對照確認。

## 驗算確認（🟢 項）
- Micron 存貨 10.37÷8.57＝+21%、營收 54.23÷41.46＝+31%：相符。
- 季 capex 10.77×4＝43.1，較 FY26 27.37 高 57%：相符（Micron remarks：Q4 capex $10.8B）。
- Samsung 23.06÷29.3%＝78.7；Kioxia 10.72÷13.6%＝78.8：相符。
- 三情境 TAM 加權（50/20/30）約 317：相符。

## 未及查證
- Sandisk FQ4 毛利 84.6%、DC 營收 $2.98B：未再重查一手 8-K。
- TrendForce Q3 合約價預估 +10–15% 與 ADATA +35–40%：未開原文。
- DRAMeXchange 512Gb TLC 晶圓現貨 18.833（10/05）：站內無法重現，現值已落後 9 天。
- Counterpoint 企業級 SSD 位元占比 48%（二手）：未查原報告。

## 處置（2026-10-14，持有人授權：不改結論的錯直接修）

機器欄 sd_verdict＝split、clock_phase＝II、conviction＝mid、priced_in＝mid、action 方向、base_rate.action 全部未動；頁面仍顯示「三次判斷皆判第三階段，換格證據不足，維持原判第二階段」。修完重跑 prose＋check：check PASS（check_id rc=0、validate rc=0、75KB；疑似新增數字 5 個皆為章節號與來源代碼）。備份：judgment／evidence／plan 各留 `*.pre_critic.json`，priced_block 留 `priced_block.pre_critic.md`。外部查證 2 次：Micron FQ4 FY26 prepared remarks 原文（PDF 轉文字直讀）、TrendForce 2025 全年 NAND 產業營收搜尋（未找到）。

### 已修

1. **Y1 capex 觸發點已達**（來源：新增 X1＝Micron 2026-09-30 prepared remarks，原文「In fiscal Q1, we project capex of around $11.5 billion and anticipate first-half fiscal 2027 capex to be approximately $25 billion. We project capex to be higher in the second half」；增幅「majority … construction capex … clean room space availability in late calendar 2028 and beyond」，起因是 DRAM 無塵室）。驗算：上半年 $25B 年化 $50B，高於 $43B。
   - risks.catalysts[2]：pos「達標，且 FY27 capex ≤ FQ4 年化 $43B」→「毛利達指引」；neg「毛利未達指引，或 FY27 capex >$43B」→「毛利未達指引」；neg_action「供給回應加速，準備撥到 III」→「準備撥到 III」；event 補「原設的另一條件『FY27 capex >$43B』已達：上半年指引約 $25B、下半年更高；增幅多為 DRAM 無塵室建廠，2028 年底後才可用，本篇改看毛利這一條」。
   - mechanics.verdict.capital_cycle[1].value 補 FY27 指引與「全公司，增幅多為 DRAM 無塵室建廠」，asof 2026-09-03→2026-09-30。
   - thesis.points[5]「Micron FQ4 capex…」→ 註明「全公司（含 DRAM／HBM）」並補 FY27 上半年指引；thesis.exhibit 第 7 列最新值補「FY27 上半年指引約 $25B」，讀法「資本回流」→「全公司回流，多為 DRAM 建廠」。
2. **時鐘維持 II 的理由換成較強證據**（來源：新增 X2＝同一份 remarks「We anticipate fiscal Q1 to be the floor for gross margins in fiscal 2027 … higher gross margins beyond fiscal Q1 … with a more moderate rate of price increases」及「sequential revenue growth each quarter」）。base_rate.differences[1]、mechanics.verdict.gate_sufficient[1]、thesis.sister_reconcile[0] 原以 Kioxia 營益率續升為主要支撐，改為 Micron 這句；summary.clock_note「價格預估放緩；Kioxia 營益率仍升」→「價格預估放緩；Micron 稱 FQ1 為毛利低點」；id_meta.oneliner「Kioxia 營益率仍在升」→「Micron 稱 FQ1 是本財年毛利低點」；thesis.points[1]「屬雜訊」→ 寫明小降來自 FQ4 計入存貨的獎金成本。Kioxia 數字在 now_state、thesis.points[1]、exhibit 仍保留為事實。
3. **Y2（部分）**：gate_sufficient[0]「實績合約價季增 ≤5%：查不到…（未達）」→「（未驗證）」；base_rate.differences[1]「III 的兩個獨立條件…都未達」→「兩個條件中，第一個查不到實績、無法驗證；第二個未達」（拿掉「獨立」，因兩者因果同源）。
4. **Y3（部分）**：thesis.sister_reconcile[1] 補一句「本篇的合約價 kill 用任一季 ≤0%，比該篇的連兩季 ≤0 嚴，因為本篇管的是純 NAND 原廠，SNDK 沒有 DRAM 營收可攤平」（依據：stocks.op_leverage、SNDK 純度 100%）。
5. **Y4 PM 行動與 kill 表**：summary.pm_actions[0]「晶圓現貨連 4 週 <16，或合約價任一季 ≤0%，即減碼」→「晶圓現貨連 4 週 <16，降級觀察；合約價任一季 ≤0%，視為進入 Phase IV，退出」。對齊的是頁面多數處的寫法（kill_table[0]、kill_table[1]、debates[0].neg_read、catalysts[3]），kill 表本身未改。若持有人偏好冷讀建議的「單條減碼、雙條退出」，要改的是 kill_table[1].posture 與 debates[0].neg_read。
6. **Y5 SNDK 無 5 年分位**（A13：2025-02 分拆；本地週線自 2025-02-10 起共 88 週）：thesis.points[4]、debates[0].priced_in、valuation.priced_rows SNDK 分位改「上市以來，未滿 2 年」；valuation.mid「倍數在 5 年低檔」→「倍數在歷史低檔」。
7. **Y7（部分）NTAP**：stocks.rows NTAP 方向「受益」→「中性」，推導補「受益與否沒有證據，只列觀察」；id_meta.related_tickers NTAP beneficiary true→false（depth 🟡，不影響 id_autopsy 籃子）。
8. **倍數改用現價估算**（協調者追加；程式輸入 priced_inputs 已修為 live_fpe_est／live_pct_5y_est，plan.json 的 priced 與 priced_block.md 已重寫）：
   - valuation.priced_rows：MU 6.5／分位 8.0 → 5.35／0；SNDK 7.7／15.0 → 6.77／0（上市以來）；MRVL 37.97／100 → 36.51／93.6；NTAP 18.8 → 21.08；WDC 12.16 不變；倍數欄一律標「現價估算」。
   - 引用處同步：thesis.exhibit 第 9 列「6.5 倍、5 年第 8 百分位」→「5.35 倍（現價估算），5 年區間最低」；thesis.points[4]、debates[0].priced_in 改 5.35／6.77、區間最低；valuation.high「MRVL 37.97 倍、第 100 百分位」→「36.51 倍、第 93.6 百分位」；id_meta.action、related_tickers[MRVL].role、summary.pm_actions[2]「5 年第 100 百分位」→「第 94 百分位」；closing.not_doing[1]「MU 6.5 倍」→「5.35 倍」。
   - 雙殺推導 valuation.derivations[3]：倍數 7.7→6.5、−66% → 6.77→5.35、0.4×5.35÷6.77−1＝−68.4%，寫 −68%。
   - 新倍數只會更便宜（MU、SNDK 分位 8／15 → 0），priced_in 依倍數的那半邊不變；MRVL 仍在高檔，action 不變。
   - 隱含 EPS 推導鏈（thesis.points[2]、thesis.derivation②、valuation.derivations[0–1]）**只標明 6.5、7.7 是 DD 日倍數並附現價估算值，未重算**，理由見交持有人第 1 項。

驗證：R.stub_validate ok；R.mech_checks 無任何紅黃項；被引用來源 T1 占比 63.8%（47 筆，門檻 60%）。HTML 已確認含上述修正文字與「維持原判第二階段」。

### 略過

- **Y6 2025 TAM 基期**：TrendForce 只有前五大逐季數字（搜尋確認 2Q25 $14.67B、4Q25 $21.17B），查不到 2025 全產業年額，依指示不動中值 60 與 demand_5y_multiple 5.5、cagr_pct_5y 41。附註給持有人：冷讀算出前五大四季合計約 $65B，若屬實，全產業基期不會低於 65，現行中值 60 偏低、5.5 倍偏高；方向不變。
- **Y3 priced_in 與姊妹 high 的調和句**：未加。原因是 mid 的依據（隱含 E 約等於下季指引年化）本身有問題，見交持有人第 1 項，先加調和句等於替有疑義的判斷背書。
- **Y7 PSTG**：屬判斷。Everpure 營收 +38%、全年指引上調（C15），以主題受益看 beneficiary=true 有證據；「NAND 回落時受益」是附加條件，不矛盾。
- **附帶 1 Kioxia 兩季低於共識**：未補入；已把 Kioxia 從時鐘理由的主要支撐降為次要（見已修第 2 項）。7–9 月指引低於 Bloomberg 共識一說不在證據包、未查證。
- **附帶 2 SK hynix 3Q NAND 位元出貨僅約 +3%**：C17 為 T3-A，S6 稱原文未載，未證實，不改 debates[1]。

### 交持有人（第 1 項已依持有人更新政策處理，見下節；第 2 項依指示不改）

1. **MU、SNDK 隱含 EPS 推導鏈與 priced_in＝mid**（已處理）。查證結果：FY2 是 FY2027，不是 FY2028（MU DD 2026-07-05 原文「Fwd P/E（FY27，$149.64 共識）= $975.56 / $149.64」；Micron FY27 結束於 2027 年 9 月），所以「撐到 2028 年中」標錯。更大的問題是頁面拿現價除以 DD 日倍數（989.04÷6.5、1487.33÷7.7），兩個日期混用。以 dd-screener 的 Koyfin 共識（2026-10-08）看：MU FY27 EPS $176.15、FY28 $206.33，比下季指引×4（$152.6）高 15%、35%；SNDK FY27 $214.38、FY28 $265.24，比 44–46×4（$176–184）高 17–22%。照頁面自己的分級，「隱含 E 再成長」屬 high，與三篇姊妹一致。核心判斷「低本益比是用高峰獲利算的，風險在 E」方向不反轉，反而更強；但「約等於下季指引×4」這句與 priced_in＝mid 要不要改成 high，需持有人決定。受影響欄位：summary.key_call、summary.priced_in_note、thesis.points[2]、thesis.derivation②、valuation.implied_growth、valuation.mid、valuation.derivations[0–1]、debates[0–1].priced_in、debates_extra、closing.not_doing[1]。
2. **換相雙閘的第二訊號不獨立**（Y2 後半）。合約價與原廠毛利因果同源（B6：Sandisk 季增量三分之二來自價格）。可換成的獨立訊號：存貨天數（Micron DIO 129 天、季增 9 天，管理層稱含節點停產前備貨與獎金計入存貨、預期下降；記憶體姊妹篇記三星存貨天數 94.6→102.0→124.5 連兩季升）或原廠 NAND 位元出貨。改閘的定義可能動到時鐘判斷，所以不直接改。

### 追加處置：priced_in 重判（持有人政策更新：只修錯的那段，priced_in 可依頁面自身分級局部重判）

- **id_meta.priced_in：mid → high。** 理由：頁面分級的 high 是「隱含 E 再成長，或倍數在 5 年高檔」。改用同一時點的價格與倍數重算（dd-screener 2026-10-14 現價估算，FY2＝FY2027）：MU 943.02÷5.35≈176（共識 176.15），比下季指引×4 的 152.6 高約 15%；SNDK 1455.23÷6.77≈215（共識 214.38），比 44–46×4＝176–184 高約 17–22%；FY2028 共識再高 17%（206.33）、24%（265.24）。這屬「隱含 E 再成長」，不再是 mid 的「約等於下季指引年化」。倍數低檔不改變分級，因為 high 的兩個條件是「或」。新分級與三篇姊妹報告（皆 high）一致。
- 驗算：943.02÷5.35＝176.27；1455.23÷6.77＝214.95；176.15÷152.6＝1.154；214.38÷184＝1.165、÷176＝1.218；206.33÷176.15＝1.171；265.24÷214.38＝1.237。
- 同步改寫（舊推導拿現價除以 DD 日倍數，已全部移除）：summary.key_call（「約等於下季指引×4」→「比下季指引×4 還高 15–22%」，結論「風險在 E，不在倍數」不變）、summary.priced_in_note、thesis.points[2]、thesis.derivation②、valuation.implied_growth、valuation.mid（改為目前沒有標的）、valuation.high（列入 MU、SNDK）、valuation.derivations[0–1]、valuation.passthrough、debates[0].our_view／priced_in、debates[1].priced_in、debates_extra.underpriced_risk、closing.not_doing[1]。「撐到 2028 年中」的年度標錯一併移除。
- **id_meta.action**：方向不變（純 NAND 重資產不追），只在句首補「共識 EPS 已算進再成長」。
- 新增證據 X3（dd-screener 現價估算與 Koyfin 共識 FY2027／FY2028 EPS，T2，程式輸入），引用於 thesis、debates[0–1]、valuation。被引用來源 T1 占比 62.5%（48 筆）。
- 未動：sd_verdict、clock_phase、*_boundary、*_gate_reverted、conviction、base_rate.action。重跑 gate→prose→check：gate 紅 0 黃 7，gate 未改動本次編輯；check PASS（76KB）；頁面仍含「維持原判第二階段」，Priced-in 顯示「高」。
- 交持有人第 2 項（換相第二訊號改用存貨天數）依指示視為判斷類改進，不改。
