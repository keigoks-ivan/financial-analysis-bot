# Cold-review：ID_AINetworking_20261014（ID v4 mode，J1–J10）

審稿範圍：check_excerpt.md、check_report.md；evidence.json 與 votes／gate_1／gate_2／priced_block 僅用於追數字來源。查證 4 輪網搜（資本支出、EML 交期、NVDA Q2 FY27、Dell'Oro），其餘列「未及查證」。

## 結論

**Verdict：THESIS_INTACT（可上站，需先做下列 🟡 小修）。** 🔴 0 條、🟡 9 條、🟢 4 條（J1、J4、J8，J10 基本通過）。沒有一條會翻轉「需求仍擴張、供給偏緊、雷射最緊、pure-play 估值貴」的主結論，但有三處是 gate 已點名、成稿仍保留的瑕疵，另有兩處過期數字。

## 對「閘改回短缺」的判斷（J6，本案重點）

**程序上站得住，但理由寫得比證據強；我的看法是「可辯護，不是已證明」。**

支持改回的證據：
- 三票 split 的換格依據，是把交換層標為「balanced」，而這一點只靠 Broadcom「2027 年供給已確保」單一 Benzinga 自動轉錄稿（evidence C10，T3-B，note 自註「承重引用前須以官方逐字稿核對」）。該句說的是博通自家供給，不是交換層整體供需。
- 同一證據包內有三份反向材料：Arista 稱供應鏈緊、元件成本上升約兩年、可能到 2028（C12，T3-A，Motley Fool 逐字稿）；Dell'Oro 2026-09-03 新聞稿標題段落稱 2Q26 供給限制壓抑市場（B22／C2，T2；我另以網搜看到 Dell'Oro 原稿同句 supply constraints weighed on the market）；Lumentum 缺口逾 30%（B16）。換格要推翻前版判斷，舉證責任在換的一方，單一轉錄稿確實不夠。
- 前版（2026-04-19）同為 shortage／II，換格需要新證據，沒有就不動，這是合理的保守規則。

不夠紮實之處：
1. 反方證據用的標準不對稱。閘排除博通自動轉錄稿（T3-B），卻接受「Dell'Oro 摘要稱市場受供給限制（未逐字讀到）」（C2 note 明寫只見搜尋摘要）。兩邊都是未直讀的二手，頁面卻只對一邊說「未逐字讀到」且仍當緊的佐證。
2. 「交換層沒有證據顯示平衡」是缺證據，不是有證據顯示緊。Arista 說的是零組件成本上升，成本漲價與缺貨是兩件事。
3. 三票 split 的真實根據其實不只交換層：頁面自己的稀缺分層表（thesis）六層裡，只有雷射「短缺」，交換晶片「偏緊、有競爭」，光模組「中國廠分食」，retimer／AEC「無缺貨證據」，連接器「訂單強」。這張表本身就是分層結果，單值「短缺」把它壓平。見下 J5。
4. 回到的格子（shortage×Phase II）歷史勝率 7/24、均報酬 −7.5%（base_rate）。改回短缺等於把本篇放進已知最弱的格子；conviction 下調為 low 是誠實的補償，這點處理對。

我的建議：不推翻閘的結果，但（a）在頁面把「換格證據不足」的理由寫成「博通自述不足以證明交換層平衡」，不要寫成交換層供給緊已被證實；（b）sd_verdict_detail 已列 retimer／AEC 無缺貨，建議在 summary 供需格明講「僅雷射層短缺，其餘分層偏緊至無證據」，避免讀者把 shortage 讀成全鏈。這是第一個「閘推翻三票一致」的案例，建議在 rule_ledger 記一筆：改回的證據門檻應同時套用在正反兩邊（含 Dell'Oro 未直讀）。

## 🟡 逐條

### 🟡 1　J6／J3　Phase II 後段的兩項佐證是套套邏輯或與網路無關（gate_1、gate_2 已點名，成稿未改）
- 錯的原文（mechanics §3.4）：「2026 年 capex 約 $690B，為其年折舊負擔 $115–140B 的 5–6 倍…capex 為折舊負擔的 5–6 倍，承諾一季翻倍有餘，屬 Phase II 後段。」
- 問題：$115–140B 是證據包 D15 以 5 年壽命把 $690B 除以 5 估的（690/5≈138），不是實際折舊，比值本來就約 5。evidence NF-D 明列 capex／折舊比一手查不到。
- 正確做法：改標「假設壽命 5 年下的推算，不作獨立證據」，Phase II 後段只留 lead time（D13）與供給承諾（D3）。
- 同段另一句（thesis 供需怎麼判）：「資本被 InP 擋住後改道：NVDA 供給承諾一季由 $119B 增至 $279B，存貨較年初 +47.5%。」evidence B2／C6（NVIDIA 10-Q Note 10，https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000075/nvda-20260726.htm，2026-07-26）寫明承諾主要是記憶體與製造設施，與 InP 或網路無關。應刪「InP 擋住後改道」的因果句，改為「NVDA 整體資本鎖定」。
- 另：存貨 +47.5% 的基期是 2026-01-25（跨兩季），而姊妹 AIAcceleratorDemand 的存貨 kill 用季增；頁面卻說「與本篇存貨較年初 +47.5% 的判讀一致」，基期不同，不能寫「一致」。
- 欄位：mechanics.verdict.capital_cycle[0]、thesis.sd_points[2]、thesis.sister_reconcile[1]、mechanics.verdict.gate_leading。

### 🟡 2　J3／J7　hyperscaler 資本支出現值是 4 月資料，7 月財報季已更新
- 錯的原文：kill 表「2026 年約 $670–725B，年增約 77%（2026-04-30）」；§3.1「Microsoft 約 $190B 中有約 $25B 是元件漲價」；§3.4「2026 年 capex 約 $690B」。
- 7 月財報後的值（網搜，各源口徑不一，需回頭讀公司一手）：Alphabet 全年上調至 $195–205B（原 $180–190B）、Amazon 約 $220B（原約 $200B，原因含記憶體漲價）、Meta 收斂為 $130–145B、Microsoft 以曆年計約 $175B（會計處理改變後，原 $190B）；四家合計約 $710–745B。來源：https://www.cnbc.com/2026/07/28/hyperscalers-face-higher-capex-scrutiny-after-alphabet-report-panned.html（2026-07-28）、https://effectstory.com/en/articles/hyperscaler-ai-capex-q2-2026-microsoft-alphabet-meta-amazon、https://www.yieldtheory.app/research/hyperscaler-ai-capex-tracker-2026。
- 影響：+77% 與「需求仍擴張」方向不變，但 Microsoft $190B／$25B 漲價拆解已非最新；證據包 D11 note 自稱「Q3 財報尚未公布，故為最新可得」，漏看了 7 月 Q2 財報季。另外 CNBC 稱 Alphabet 財報後股價下挫、市場對 capex 轉趨挑剔，這是對本篇 II→III 預警有用的新資訊，頁面沒有提。
- 同列另有口徑問題：欄位名為「2027 年 capex 指引年增」，現值卻填 2026 年增 77%，不是 2027 指引，讀者看不出離熊線（<+20%）還差多少。建議現值改為「2027 指引尚未公布（下次 2026-10 下旬）；2026 年增約 77%（7 月更新值）」。
- 欄位：risks.kill_table[1]、id_meta.kill_metrics[1]、mechanics.verdict.capital_cycle。

### 🟡 3　J3　EML 交期現值過期，且 Dell'Oro 年增現值停在 Q1
- 錯的原文：kill 表「第三方 EML 雷射交期：延至 2027 年後，10 月無更新（2026-04-20）」；「Dell'Oro Ethernet AI back-end 交換器年增逾 2 倍 2026 Q1（2026-06-02）」。
- 事實：TrendForce 原始發布為 2025-12-08（https://www.trendforce.com/presscenter/news/20251208-12823.html，Nvidia 預先配給使 lead time 延至 2027 年後），2026-04-20 是 TelecomTV 轉述的 AI 光模組報告。Lumentum 5 月法說稱缺口逾 30%，7 月重申（B16），產能到 2028 年中才加。方向未變，但「現值」其實是六至十個月前的轉述，整個「雷射最緊」的第一層證據都建在這上面，且為二手。
- Dell'Oro 2Q26 稿已在 2026-09-03 發布（https://www.delloro.com/news/ai-back-end-networks-switch-sales-surpass-front-end-networks-for-the-first-time-in-2q2026/），kill 表現值卻仍填 Q1 數字；證據包有 B22 但沒有 Q2 年增數字。應標「Q2 年增未取得（付費報告）」而不是沿用 Q1。
- 建議：EML 現值註明「最新一手為 Lumentum 2026-05 法說；TrendForce 無 10 月更新」，並把 lead time 欄改為雷射商自述＋第三方各一列分開。
- 欄位：risks.kill_table[0]、[2]；id_meta.kill_metrics[2]。

### 🟡 4　J9／J7　kill 表第 5 條「0 家」與分歧卡 3 矛盾，且「量產」未定義
- 錯的原文：kill 表「開放 scale-up…量產部署家數：0 家；UALink 首批產品 2026 年底至 2027 年初」；分歧卡 3「Tomahawk Ultra 本季已開始部署」。
- 問題：證據只是「查不到確認」（NF-D、NF-E），不等於 0 家；而 B8（DatacenterDynamics 轉述博通）說 Tomahawk Ultra 已開始部署，與「0 家」衝突。熊線「2027-06 前仍為 0 家」因此無法裁決。
- 修正：現值改「無確認公告（查不到）」，並寫明「量產」＝公開出貨或客戶揭露；說清 Tomahawk Ultra 部署是否計入。
- 欄位：risks.kill_table[4]、id_meta.kill_metrics[4]。

### 🟡 5　J5　單值「短缺」與頁面自己的分層結論不對稱
- 錯的原文：summary 供需格「短缺…供給偏緊，雷射最緊」，id-meta sd_verdict＝shortage；但稀缺分層表六層中只有雷射標「短缺」，retimer／AEC「無缺貨證據」，光模組「中國廠分食」。
- 判準上這不到 🔴，因為頁面把分層寫得很清楚、detail 欄也有交代；但下游（INDEX、picks）只讀 sd_verdict 單值，會把整個網路讀成短缺。
- 建議：維持 shortage，但 sd_verdict_detail 第一句直接寫「僅雷射層短缺」，並在 summary 燈號副標加「其餘層偏緊或無缺貨證據」。

### 🟡 6　J3／J10　估值倍數口徑未標，讀者會誤讀 NVDA、AVGO 便宜程度
- 錯的原文（valuation 表與全文）：「NVDA 16.67」「AVGO 18.51」「ANET 42.1」「本益比（股價除以每股盈餘）」「前瞻本益比 5 年分位」。
- 問題：priced_block.md 寫的是 Fwd P/E(FY2)，即用兩個財年後的共識 EPS，頁面只說「本益比」「前瞻本益比」。證據包 D16（sentisense，2026-09-06，T3-C）給 NVDA 前瞻 P/E 約 24 倍、AVGO 約 31 倍，與頁面 16.67／18.51 差很多。兩者口徑不同都說得通，但「NVDA、AVGO 是免費選擇權」這句行動建議的依據正是這個低倍數，必須讓讀者知道是 FY2 口徑。
- 修正：valuation 表欄名改「FY2 前瞻本益比」，並在註腳寫明 NVDA 以 NTM 計約 24 倍（D16，二手）。分位是否為同口徑歷史序列，頁面也未說明，列為未及查證。
- 欄位：valuation.priced_rows、summary.pm_actions、id_meta.action。

### 🟡 7　J3　ALAB、CRDO 無 5Y 分位卻仍被歸類並寫進行動句（gate 已點名，未改）
- 錯的原文：「ALAB 48 倍」進 pm_actions①與 id_meta.action（「ALAB 48 倍」）；valuation 收斂「high：…ALAB 48.33 倍」「mid：…CRDO 22.35 倍（無分位）」。priced_block 明標「⚠ 無 5Y 分位，不得當承重證據」。
- 另外 summary 稱「pure-play 已在 5 年頂部」，實際只有 ANET、MRVL 兩檔有 100 分位，MRVL 純度才 40%。
- 修正：措辭改為「ANET、MRVL 在 100 分位；ALAB、CRDO 無分位可判」，pm_actions① 的 ALAB 改為旁註。
- 欄位：summary.key_call、valuation.high／mid、id_meta.action。

### 🟡 8　J3　TAM 倍數 4.5 建立在無來源的 2025 基期
- 錯的原文：§3.1 推導「2025 年基期≈100÷1.8≈$55B（Q1 Ethernet 年增逾 2 倍；全年取較低倍數）；5 年倍數 250÷55≈4.5，CAGR≈35%」；top-down 回推「以年增 30%」（base 卻用 25%）。
- 問題：1.8 倍沒有來源（A6 只說 Q1 Ethernet 逾 2 倍，且那是 Ethernet 單項，不含 InfiniBand 與網卡）；前版基期隱含約 $29B，3.4→4.5 的跳升（+32%）沒有交代。30% 與 25% 為何不同也沒說。
- 修正：id-meta demand_5y_multiple 改區間（約 3.5–4.5）或標「基期為推算」；或引 Dell'Oro 2025 全年實值（付費報告，查不到就明說）。
- 欄位：mechanics.demand.tam.derivation、id_meta.demand_5y_multiple。

### 🟡 9　J1／J3　NVDA 網路金額與純度三處疊在二手數字上
- 錯的原文：「Q2 法說季增 18%」「NVDA 網路 FQ2≈$14.8B×1.18≈$17.5B，÷總營收 $96.2B≈18%」。
- 問題：Q1 $14.8B 只來自 globaldatacenterhub（T3-B／T4，一手 CFO Commentary 未直讀）；Q2「網路季增 18%」來自 Webull 轉載的 Motley Fool 摘要。巧合的是 NVDA 同季 Data Center 營收季增也是 18%（NVIDIA 8-K Ex.99，https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm，2026-08-26：總營收 $96.2B、Data Center $89.0B、季增 18%），我無法排除摘要把 Data Center 的增幅誤植到網路。頁面已標「二手」，tier 處理誠實，但「NVDA 為最大網路營收池」「purity 18%」「玩家矩陣：網路季增 18%」都建在這個數字上。
- 修正：把「網路季增 18%」加註「與 Data Center 季增同為 18%，一手未驗」；purity_pct 18 保留但在 stocks 推導行標「±不確定」。
- 欄位：stocks.rows[NVDA]、mechanics.supply.player_matrix[NVDA]。

## 其他未列 🟡 但建議順手處理

- 旭創 1.6T 市占「35–40%」（E13，Nomura 預估，as-of 約 2026-01，T3-B）在稀缺分層與玩家矩陣中未標日期與「預估」性質；它是預測值，不是實績。
- AVGO「2027 年供給已確保、AI 營收倍增至約 $115B」只有單一自動轉錄稿（C10）；頁面在三處聲明不當承重證據，但 12M Bull 情境仍寫「AVGO FY27 AI 約 $115B 獲確認」當觸發。這是以弱證據設觸發，不致命，但與自己宣稱的證據紀律不一致。證據包 B7 還記有另一報導稱 FY27 網路 $115B／FY28 $230B 與他處衝突，應維持不採用。
- check_id.py 的重複掃描命中「AI back-end 交換器 Q2 首度超越 front-end」在 8 處出現，經核屬跨段復述，方向一致（J9 🟡 級，可接受）。

## J1–J10 逐項

| # | 結果 | 備註 |
|---|---|---|
| J1 cornerstone | 🟢（附 🟡 9） | 「EML 售罄／交期延至 2027 年後」「Ethernet 在 AI back-end 超越 InfiniBand」皆有 T2／T3 來源；「Celestica 第一」為 Dell'Oro 稿直述；「旭創 35–40%」見上。 |
| J2 cross-ID | 🟡 | 7 份姊妹皆已對帳（含 gate_2 點名的 AIInferenceEconomics、CUDARocmMoat）。存貨基期與姊妹不一致（🟡 1）；與前版 ID_AINetworking_20260419（shortage／II、TAM $100B、3.4 倍）口徑差異頁面有交代「本版納入 scale-up」，但 3.4→4.5 的基期變動未交代（🟡 8）。 |
| J3 量化模組 | 🟡 | D2 資本週期兩個真數字（lead time、供給承諾）但佐證含套套邏輯；D4 三角對帳有算且差距 50% 有解釋；D8 倍數有來源但口徑未標；D9 現值多條過期。 |
| J4 分歧真辯論 | 🟢 | 四張卡市場最強版本皆帶數字，威脅卡有判別訊號與日期。分歧 1 的「錯殺型」缺 AVGO 中國營收占比，已用 falsifier 補強，信心標「低」合理。 |
| J5 機器欄↔內文 | 🟡 | 見 🟡 5。conviction low、priced_in mid、clock II 與內文一致；summary 寫「II／III 交界」而 id-meta clock_phase 為 II，可接受。 |
| J6 熱產業時鐘施壓 | 🟡 | 三問：(1) Phase 判定的基本面證據有但部分是套套邏輯（🟡 1）；(2) pure-play 26 週 +28–90%、ANET／MRVL 100 分位，頁面已寫「II／III 交界」並在 priced_in 取 mid，擁擠度有處理；(3) priced_in 誠實，結論一致。conviction 因 7/24 下調為 low 正確。 |
| J7 kill 套套 | 🟡 | 5 條中有 3 條為第三方或市場撮合價（Dell'Oro、TrendForce、本益比分位），無套套邏輯；但現值多條過期或口徑含糊（🟡 2、3、4）。前版兩條 kill（NVDA 網路金額、AVGO 網路占比）撤下並說明原因，處理得當。 |
| J8 判斷手冊 | 🟢 | 命中「shortage×II」「熱產業擁擠度」，頁面實答有具體數字（5–6 倍雖為套套邏輯，仍屬實答，問題歸 J3）。未逐條重驗 playbook 全部索引。 |
| J9 唯一敘述 | 🟡 | 重複掃描 4.6%，皆為方向一致的復述；kill 表與分歧卡 3 的矛盾見 🟡 4。 |
| J10 白話 | 🟢 | 抽五句皆有括號白話或定義（本益比、分位、pure-play 都有解釋）；FY2 口徑除外（歸 🟡 6）。 |

## 未及查證（不臆測）

- Dell'Oro 2Q26 原稿正文數字（付費報告；只確認標題與「supply constraints」句）。
- Lumentum FQ4 FY26 與 Coherent FY26 一手 8-K 數字（B13、B15 證據包自註取自搜尋摘要）。
- ANET 毛利 63.4%、LITE 50.4%、COHR 39.4%、APH book-to-bill 1.23 未獨立重驗（證據包有 T1 來源，僅核對來源存在）。
- NVDA Q2 網路是否真為季增 18%（見 🟡 9）。
- 估值分位是否為同口徑（FY2）歷史序列。

## 處置（2026-10-14，持有人授權：不改結論的錯直接修）

只改 judgment.json、evidence.json，另依協調者指示重算 plan.json 的 priced 與 priced_block.md；改前備份為 `*.pre_critic.json`／`priced_block.pre_critic.md`。sd_verdict（shortage）、clock_phase（II）、conviction（low）、priced_in（mid）、sd_verdict_gate_reverted（split/split/split）、base_rate.action（downgraded）與 action 方向（都不追高）全部未動。頁面仍寫「三次判斷皆判分裂，換格證據不足，維持原判短缺」。mech_checks 無紅燈，prose 與 check 重跑結果 PASS，T1 占比 60.0%（65 條，下限 60%）。

查證用了 5 次網路查詢，新增兩筆證據：
- X1（T2）：Dell'Oro 2Q26 新聞稿直讀（2026-09-03）。原文寫 “We expect the market to remain supply-constrained, rather than demand-constrained, for at least the next one-to-two years.” 新聞稿沒有列出 2Q26 年增率。
- X2（T1）：Meta Q2 2026 財報新聞稿（2026-07-29）。2026 年資本支出指引 $130–145B，由 $125–145B 收窄。

### 已修
1. **供需說明（J6、🟡5）**
   - sd_verdict_detail：「供給偏緊，雷射層最緊…」→「僅雷射層確認短缺…交換層偏緊…但沒有缺貨證據；retimer／AEC 亦無。維持短缺是因換格證據不足。」（132 字）
   - summary.sd_note：→「僅雷射層短缺，其餘偏緊或無缺貨證據」
   - thesis.sd_points[0]：改為換格依據只有 Broadcom 單一自動轉錄稿，不足以換格，交換層缺貨並未被證實。
   - thesis.sd_points[1]：「Dell'Oro 摘要…（C2，未逐字讀到）」→ 改引 X1 直讀原句，並註明兩者都沒有交期或停線數字。這樣正反兩邊的證據用同一個標準。
   - 同一說法一併改：base_rate.downgrade_note（刪掉誤引的 D3）、base_rate.differences[0]、thesis.derivation、sister_reconcile[5]。
2. **Phase II 後段的套套邏輯佐證（🟡1）**
   - capital_cycle[0]：改標「推算，不作證據」，並寫明 5–6 倍來自 5 年壽命假設（D15、NF-D）。
   - verdict.synthesis：只留交期與 NVDA 整體供給承諾兩項佐證。
   - thesis.sd_points[2]：「資本被 InP 擋住後改道」→「上游資本鎖定加深，但不限於網路…主要是記憶體與製造設施（D3）」。
   - capital_cycle[2]、gate_leading、base_rate.differences[1]：同步補上「整體」「非網路專屬」。
   - 存貨基期：各處改寫為「較 2026-01-25、跨兩季」（31,575÷21,403−1＝47.5%，D4）。sister_reconcile[1] 的「判讀一致」改為「方向一致，增幅不宜與單季營收增幅直接比較」。
3. **資本支出口徑（🟡2，部分修）**
   - kill_table[1]：「2026 年約 $670–725B，年增約 77%」→「2027 年指引尚未公布；2026 年約 $670–725B、年增約 77%（4 月指引）；7 月 Meta 收窄至 $130–145B（X2），其餘三家未以一手核對」。kill_brief[0] 同步改。
   - demand.current_points[2]、bear_narrative、sister_reconcile[3]：標明是 4 月指引，Microsoft 的 $25B 改寫為「4 月稱」。
4. **EML 交期與 Dell'Oro 年增（🟡3，部分修）**
   - kill_table[0]：「年增逾 2 倍（2026 Q1）」→「1Q26 年增逾 2 倍；2Q26 新聞稿（2026-09-03）未列年增，付費報告未取得」（X1／B21）。
   - kill_table[2]、kill_brief[1]、capital_cycle[1]：標明是第三方轉述、2026-04 之後沒有更新，並並列雷射商自述（Lumentum 2026-05 法說、7 月重申，B16）。
5. **kill 第 5 條（🟡4）**
   - 現值：「0 家」→「無確認公告（查不到）；博通稱 Tomahawk Ultra 已開始部署，客戶未揭露，不計入」。
   - 量產定義：寫成「公開出貨或客戶揭露」。
   - 熊線改為「2027-06 前仍無 hyperscaler 揭露量產部署」，id_meta.kill_metrics[4] 與 debates[2].signal_neg 同步改。
   - debates[2].our_view：補「客戶與規模未揭露」。
6. **倍數口徑與 NVDA 倍數（🟡6，連同協調者追加的程式輸入修正）**
   - plan 原本誤用 DD 日快照，改以 `priced_inputs` 重算為現價 FY2 估算：
     - NVDA 16.67→14.22 倍，分位 10→0
     - AVGO 18.51→18.29，分位 24.4→22.4
     - CRDO 22.35→19.89（無分位）
     - MRVL 37.97→36.51，分位 100→93.6
     - ALAB 48.33→49.98（無分位）
     - ANET 42.1→38.79，分位 100→86.9
     - COHR 19.92→20.3，分位 0→3.2
   - APH 程式值 14.48 倍、0 分位，跟 DD 日的 25.7 倍差了 44%。latest.json 的 price_at_dd 150.31 對上週線收盤 86.19，pe_drift −43.7%，method 是 drift，看起來是股價口徑沒有對齊。無法確認，所以頁面寫「現值待核」。
   - valuation.lede 註明「FY2 前瞻本益比（現價除以兩個財年後的共識每股盈餘），以 2026-10-14 現價估算」。kill_metrics[3]、kill_brief[2] 的欄名加上 FY2。
   - 所有引用舊倍數或舊分位的句子都已改成新值，共 15 個欄位。debates[3].falsifier 的「維持 90 分位以上」改為「兩檔皆在 90 分位以上」，因為 ANET 現在是 86.9。
   - 新值沒有改變方向：ANET、MRVL 仍然高，NVDA、AVGO、COHR 仍然低，priced_in 維持 mid，「都不追高」也不變。
7. **ALAB、CRDO 無分位（🟡7）**
   - id_meta.action：「ALAB 48 倍」→「ALAB 無分位可判」。
   - summary.key_call、oneliner：「pure-play 已在 5 年頂部」→「ANET、MRVL 本益比已在 5 年 86.9／93.6 分位」或「5 年高檔」。
   - pm_actions[0]：ALAB 改為旁註。valuation.high 與 valuation.mid 改為「無分位，不歸類」。
8. **TAM 基期（🟡8）**
   - tam.derivation 寫明以下幾點：
     - 2025 基期約 $55B 是推算，1.8 倍沒有來源，A6 只是 Q1 的 Ethernet 單項。
     - 敏感度：全年增幅若為 1.6 倍或 1.4 倍，倍數分別約 4.0、3.5。
     - 前版隱含基期約 $29B（100÷3.4）。
     - top-down 用 30% 是為了讓五年累計對上 Dell'Oro 的 $1 兆，base 用 25% 等於打兩成折（820÷1,000）。
   - summary.multiple_scope 加註「2025 基期為推算」。
9. **NVDA 網路季增 18%（🟡9）**：在 thesis.points[5]、now_state、player_matrix、stocks.rows[NVDA]、debates_extra 標註「與 Data Center 季增同為 18%，一手未驗」（A1：Data Center 季增 18%），並寫明純度有不確定。
10. **其他建議**
    - 旭創市占加註「Nomura 預估，2026-01」（E13），共三處。
    - 12M Bull 的 AVGO $115B 改為「在財報正式確認（目前只見單一轉錄稿）」。

### 跳過（含部分）
- 🟡2：Alphabet、Microsoft、Amazon 的 7 月指引沒有改。找到的 Alphabet 8-K 是 Q1 指引（$180–190B），其餘只有二手來源，而且彼此不一致，查證上限內無法用一手確認。CNBC「市場對 capex 轉趨挑剔」是二手、未讀原文，沒有加入。
- 🟡3：EML 交期沒有拆成「雷射商自述」「第三方」兩列。這是結構改動，會連動 kill_metrics，所以改在同一格並列兩者。
- 🟡6：沒有加 D16 的 NTM 約 24 倍註腳。FY2 現值已由程式輸入解決，再加一筆 T3-C 引用會使 T1 占比跌破 60%。5 年分位是否為同口徑歷史序列未查證。
- 🟡8：id_meta.demand_5y_multiple 維持 4.5。這個欄位是數字，區間寫在推導行裡。
- 重複掃描 4.8%：屬方向一致的復述，接受不改。
- 「未及查證」清單中的 Lumentum、Coherent 一手 8-K，以及 ANET、LITE、COHR 毛利與 APH book-to-bill 重驗，本輪沒有處理。

### 交持有人
- 會改變結論的項目：無。
- 範圍外待決（不影響本篇結論）：
  - 審稿員建議在 rule_ledger 記一筆：閘改回前版時，換格證據門檻要同時套用在正反兩邊。
  - 姊妹 ID_AIAcceleratorDemand_20260905 的存貨 kill 把 +47.5% 標成「一季」，實際跨兩季（基期 2026-01-25）。該篇「已亮一季」的狀態可能要重看。
  - dd-screener 的 APH live_fpe_est（14.48，drift 法）疑似股價口徑錯誤，需要修資料管線。
