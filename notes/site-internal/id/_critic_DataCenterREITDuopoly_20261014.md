# Cold review：DataCenterREITDuopoly（2026-10-14，ID v4.1）

**裁決：結論站得住（shortage × Phase II，信心中、續抱不加碼），無 🔴。🟡 6 條、🟢 4 條。**

## 重點一：stock／flow 修補是否正確

CBRE 原文（https://www.cbre.com/press-releases/north-american-data-center-demand-continues-to-outpace-supply-despite-record-construction-activity，2026-08-27）：「Total data center supply … grew 33.7% year-over-year to a record 10.9 megawatts」，同表 Inventory 合計約 10,900 MW。所以 10,903 MW 是存量（inventory），33.7% 是存量增速，頁面「約 8.2→10.9 GW」正確；先前把它當流量的疑慮已排除。吸納 1,456 MW、+11.7% 是半年流量。頁面現在用「一年新增供給約 2.75 GW」對「淨吸納 2.7–2.9 GW」，口徑同為流量，措辭**正確**。「在建半年 +24.8%」也對：CBRE 2025 年底在建 5,994.4 MW（https://www.cbre.com/press-releases/fast-growing-north-american-data-center-market-set-records-in-2025），5,994.4×1.248≈7,481。

## 🟡 清單

**J3／J6-1　吸納區間上緣偏寬，必要條件其實已幾乎觸及**
- 原文：「一年新增供給約 2.75 GW 對淨吸納約 2.7–2.9 GW，吸納跟得上交付」（summary、thesis、3.3、3.4 換相雙閘）。
- 問題：2.9 GW 是 H1 的 1,456×2 年化，假設下半年不低於上半年，沒有依據。用 CBRE 已公布數字算過去 12 個月：2025 全年 2,497.6 MW（同上 2025 年新聞稿）－ H1 2025（1,456.2÷1.117≈1,304）＋ H1 2026 1,456 ≈ **2,650 MW**；佔用量法 2,730 MW。兩者都不高於新增供給 2,748 MW。也就是換相必要條件「新增供給轉為高於淨吸納」按已公布口徑已是持平到略高，頁面卻寫成「吸納略高於供給」。結論（12 個月短缺延續）不變，因為預租與空置率仍撐住，但「現約 2.7–2.9」應改為「約 2.65–2.73（過去 12 個月實際）」，區間上緣刪除。欄位：judgment 的 supply_vs_absorption／thesis 表第三列。

**J6-2　在建 7.5 GW 只是 CBRE 八大主要市場，資本湧入規模被低估**
- 原文：「7.5 GW 在建會陸續交付」「在建 7,481 MW 創高」。
- JLL 2026 年中北美報告：北美在建超過 66 GW（77% 在邊疆市場），空置率 1%（https://www.jll.com/en-us/insights/market-dynamics/north-america-data-centers，2026 年中）。證據包 evidence.json 約 765 行已有此數字，但註記「未直讀、T3」，頁面完全沒用。datacenterHawk 2Q26 報告 H1 北美租賃 13.0 GW（https://media.datacenterdynamics.com/media/documents/2Q_2026_Global_Data_Center_Market_Report.pdf），口徑是簽約而非入住，不能直接比。建議在 3.3 或 risks 補一句：主要市場以外的在建量大一個數量級，空置率 1.4% 只代表八大市場，換相先出現在邊疆市場的可能性要處理。這對「Phase II 後段」是同向補強，不是反證。

**J6-3　「要價分化」證據偏薄，且「小型 +4.3%」是挑最低一檔**
- 原文（debate 3）：「10 MW 以上半年 +6.7%、小型 +4.3%，北維整體上半年持平」，並進入 sd_verdict_detail 與 Key Call。
- CBRE H1 2026：250–500 kW +4.3%，500 kW–3 MW +7.9%，3–10 MW +8.3%，10 MW+ +6.7%（https://www.cbre.com/insights/books/north-america-data-center-trends-h1-2026）。10 MW+ 與 3–10 MW 只差 1.6 個百分點，與 500 kW–3 MW 差 1.2 個百分點，且每一檔都在漲。「小型」若指 250–500 kW，要寫明；否則會讓讀者以為小單漲得更少。北維方面 Data Center Frontier 報導 NoVA 10 MW+ 要價 +1.5%（https://www.datacenterfrontier.com/site-selection/news/55401462/cbre-record-data-center-construction-fails-to-ease-capacity-crunch），不是「持平」；證據包 note 寫「NoVA 整體租金 H1 持平」，來源未附。建議改為「10 MW 以上漲幅略低於中型部署；北維 10 MW+ 僅 +1.5%」，把「分化」降為「放緩」。
- 另：CBRE 新聞稿只說「first six months」，基準期未載明；Data Center Frontier 稱 YoY。「半年變化」與第一條否證指標的「≤0%」假設是半年口徑，應加註。欄位：evidence 租金條目、kill_metrics[0]。

**J7　股價相對表現否證列（X1）：數字對，門檻誠實，但有兩處小瑕疵**
- 數字核對：我以 Yahoo 還原價重算，2026-04-14 → 頁面期末價，DLR 193.17→178.14＝−7.8%，EQIX 1,047.16→1,019.40＝−2.65%，VNQ 92.59→91.14＝−1.57%，平均相對 −3.65pp，頁面寫 −3.6，四捨五入差 0.05，可接受（建議寫 −3.7 或「約 −3.6」）。
- 門檻：「≥15 個百分點（門檻為假設值，未經回測）」已誠實標示，姿態也寫「不自動退出」。滿足 J7「整表至少一條市場撮合價」。
- 瑕疵一：DLR、EQIX 本身是 VNQ 成分股（合計約一成），對 VNQ 的相對值有自我抵銷；15pp 在 26 週對兩檔平均值是什麼量級，頁面未給任何波動度參照。因無回測，建議把「假設值」旁加一句「兩檔 26 週相對 VNQ 的歷史差距分布未算」。
- 瑕疵二：valuation 段寫「核心 REIT 無本地週線，查不到 26 週漲幅」，但 risks 表同一頁給了 DLR −7.8%、EQIX −2.7%。前後矛盾，應在 valuation 段引用 risks 的數字，並據此處理 J6 的擁擠度問題（REIT 26 週落後大盤，與「資本已湧入且擁擠」不一致，反而支持 Phase II 而非更晚相位；EQIX 年初至今約 +34%〔Simply Wall St，2026-10-10〕則顯示 26 週視窗與年度視窗結論不同，宜註明）。

**J5／J9　第一頁「三條要盯的否證指標」一律標「論點作廢」，與 risks 表姿態不符**
- summary 寫三條「破 … 論點作廢」；risks 表中 backlog 破線＝「減碼 DLR」，空置率破線＝「降級、核心倉減半」，要價破線＝「conviction 降 low、停止加碼」，只有兩者同時才退出。另 summary 只列三條，risks 有五條（耐用年限、股價相對兩條未上第一頁）。建議第一頁改為「破線姿態」並註明另有兩條。

## 🟢 通過
- **J1**：「創高」「空置率 1.4%」「在建 7,481.1 MW」「預租 80.4%（去年 74.3%）」「北維 0.2%」皆與 CBRE 原文一致；DLR Q2 backlog 19 億（100% 持分）、14 億（持分）、Core FFO 指引 8.15–8.20 與 8-K 一致（https://www.sec.gov/Archives/edgar/data/0001297996/000110465926086270/dlr-20260723xex99d1.htm）。
- **J2**：四篇姊妹 ID 判斷（短缺、Phase II、信心中）與倍數 2.0x vs 2.2–2.7x 的差異已解釋；前版 TAM 2,000 億不沿用，有說明。
- **J3 其餘**：TAM 三情境加權 1,348 億≈1,350、5 年倍數 2.0x、CAGR 14.9%、bottom-up 22 GW、DLR 每 1 倍 P/FFO≈8.2 美元、持分 backlog 16 億÷營收 69 億＝23% 皆可回算。
- **J4／J8**：四張分歧卡皆附市場最強版本與數字；破局條件可裁決。

## 過時檢查（截至 2026-10-14）
- CBRE H1 2026（2026-08-27 發布）、DLR 2Q26（07-23）仍為最新；DLR 3Q26 於 **10-29** 盤後、EQIX 3Q26 於 **10-28** 盤後（https://www.digitalrealty.com/about/newsroom/press-releases/3373379/digital-realty-schedules-third-quarter-2026-earnings-release-and-conference-call、Nasdaq 媒體通知 2026-10-01），頁面寫「10 月下旬」正確，建議直接寫日期。
- datacenterHawk 本季報告（Q3）尚未發布；最新為 2Q26。頁面未引 datacenterHawk，不構成過時，但見 J6-2 的口徑差。
- 未發現 10 月初新出的月度或財報數字會改動頁面數字。EQIX 與 CPP 完成 atNorth 收購（EQIX newsroom，10 月）頁面未提，對論點無影響。

## 未及查證
- Microsoft 15→25 年耐用年限與 Citi「2027–28 年自由現金流可能轉負」「8,010 億美元」為轉引，未逐條追原文。
- IRM 資料中心營收 +39%、GEV／VRT 數字未查（頁面已標「待核」）。
- Data Center Frontier 文中 10 MW+ 要價出現互相矛盾的 9.7% 與「持平」說法，無法調和，以 CBRE 原頁為準。

## 處置（2026-10-14，局部修，不重判）

只改有問題的欄位，不重跑判斷。sd_verdict、clock_phase、conviction、priced_in、base_rate.action 都沒動。改完重跑閘、散文與檢查：閘 0 紅 10 黃，檢查 PASS（check_id 與 validate_id_meta 皆 exit 0，T1 占比 61.9%）。

### 已修

1. **淨吸納區間（J3／J6-1）**
   - 欄位：id_meta.future_state、thesis.points[1]、thesis.exhibit.rows[2]、thesis.derivation、mechanics.why_now.s_curve[0]
   - 改前：「淨吸納約 2.7–2.9 GW，吸納仍跟得上交付」（上緣是上半年 ×2 年化）
   - 改後：「過去 12 個月淨吸納約 2.65–2.76 GW，與一年新增供給約 2.75 GW 大致相等」
   - 來源：X2（CBRE 2025 全年淨吸納 2,497.6 MW，2026-02-26 新聞稿）、B10、B9、X5
   - 區間上緣用 2.76，不是審稿建議的 2.73。CBRE 新聞稿只寫淨吸納「增近 12%」，沒寫比較基期（X5）。若比的是 2025 上半年，12 個月≈2,650 MW；若比的是 2025 下半年，12 個月≈2,760 MW。占用量變化法得 2,730 MW。三個值都寫進推導。
2. **換相雙閘的現況（同上條）**
   - mechanics.verdict.gate_necessary：「空置率連兩期回升（現 1.4%，已與 2025 年底持平）」→「（未成立：現 1.4%，與 2025 年底持平）」
   - gate_leading：預租率回落加註「未成立：一年前 74.3%，仍在上升」；供給高於吸納加註「推算已大致觸及：新增約 2.75 GW，過去 12 個月淨吸納約 2.65–2.76 GW；CBRE 未寫吸納的比較基期」
   - gate_sufficient[0]、[1]：加註「未成立」（要價現 +8.3%；2027 指引要到 2027 年初才公布，backlog 現 19 億）
   - mechanics.verdict.synthesis 補一句：只有「新增供給不再低於吸納」按推算已大致觸及，空置率沒有回升，兩個充分條件都未成立，所以仍判 Phase II。
   - 名稱要對齊：在本頁的閘門結構裡，「新增供給高於淨吸納」是必要條件底下的領先觀察項；必要條件本身是「空置率連兩期回升」，目前未成立。按頁面自己的規則，不需要換相。
   - 「推算」兩字是閘黃燈 D3 對本次改動的提醒，在閘之後補上，只改措辭，沒改數字。
3. **在建口徑（J6-2）**
   - thesis.points[1]：「在建 7,481 MW 創高」→「主要市場在建 7,481 MW 創高（JLL 估全北美在建逾 66 GW，口徑較廣）」
   - thesis.exhibit.rows[1][0]：「在建容量／預租率」→「主要市場在建容量／預租率」
   - mechanics.supply.read 補三句：JLL 估全北美在建逾 66 GW，其中 77% 在西德州、俄亥俄等新興市場。兩個數字口徑不同，不能相減。空置率 1.4% 只反映主要市場，供給過剩若出現，可能先出現在新興市場；JLL 自己預期空置率到 2028 年仍接近零。
   - 來源：X3（JLL North America Data Center Report, Midyear 2026，2026-08-11，直讀）
4. **要價「分化」（J6-3）**
   - id_meta.now_state：「但要價開始分化」→「要價各級距仍漲，但大單較慢」
   - id_meta.sd_verdict_detail：「要價漲幅已分化，10 MW 以上漲幅低於中型部署」→「要價各級距仍漲，10 MW 以上漲幅略低於中型部署」
   - summary.sd_note：「電力層短缺，要價已分化」→「電力層短缺，大單要價漲幅略低」
   - summary.key_call 與 title.deck：「要價分化」→「要價漲幅」
   - thesis.points[4]：「定價權開始分化」→「要價仍漲，但大單較慢」，並補 500 kW–3 MW 的 +7.9%
   - thesis.exhibit.rows[3][2]：「大單議價力回升」→「各級距仍漲，大單較慢」
   - debates[2].our_view：「小型 +4.3%」改為註明是最小的 250–500 kW 級距，補 500 kW–3 MW 的 +7.9%，「議價力回來了」降為「略有回升」，「很可能收斂」降為「可能收斂」
   - 北維「整體租金上半年持平」保留：CBRE 北維原頁寫「Overall rental rates held steady in H1」，已補出處 X4
   - 半年口徑：CBRE 原文是「first six months of the year」（X5），已在 risks.kill_table[0].src_freq 與 id_meta.kill_metrics[0].source 註明「該半年內變化」
   - 來源：B11、X4、X5
5. **valuation 段與否證表前後矛盾（J7 瑕疵二）**
   - valuation.momentum：「核心 REIT 無本地週線，查不到」→「核心 REIT 26 週落後 REIT 大盤：DLR −7.8%、EQIX −2.7%，VNQ −1.6%（還原收盤價，截至 2026-10-13），價格沒有追高跡象」
   - valuation.priced_rows 的 DLR、EQIX 26 週欄：「查不到（無本地週線）」→ X1 的還原價數字
   - 來源：X1
6. **第一頁「論點作廢」（J5／J9）**
   - summary.kill_brief[0]～[2].bear 加上 kill 表的破線姿態：要價轉負→信心降為低、停止加碼；backlog 破線→減碼 DLR；空置率破線→降為供需平衡、核心倉減半
   - 頁面第一頁不再出現「論點作廢」
   - 散文產出後在 prose_A.html 的 kill-brief 補一行：「要價與空置率同時破線才全數退出；另兩條（超大廠延長耐用年限、DLR／EQIX 相對 REIT 大盤 26 週表現）見『我怎麼知道我錯了』」
   - 這一行不在判斷 JSON 裡，散文若重跑會消失

新增證據 X2～X5，全是 T2，標「審稿補入」。

### 未處理

- J7 瑕疵一（在「假設值」旁註明歷史差距分布未算）：X1 那一列照協調者指示不動。
- 北維 10 MW+ 要價 +1.5%（Data Center Frontier）：CBRE 北維原頁只寫要價升到每 kW 160–185 美元，沒給漲幅；DCF 文中數字自相矛盾，不採用。
- EQIX 年初至今約 +34%（Simply Wall St）：未查證，未加。
- 財報日期：DLR 3Q26 在 10-29 盤後已有公司公告；EQIX 日期公司還沒公告，各家行事曆寫 10-27 到 10-29 都有。頁面寫「下旬」沒錯，不改。
- datacenterHawk H1 北美租賃 13.0 GW：口徑是簽約，與 CBRE 吸納不可比，不加。
- 閘其餘 9 條黃燈都不在本審稿清單裡，也都不是這次改動造成的，未處理：TAM 租用占比口徑、與姊妹報告倍數差的解釋、「9 個月」被寫成建築交期、微軟營業租賃一事正反兩用、其餘三家超大廠的耐用年限未查、2027 capex 指引的口徑、backlog 機械性下滑、純度 95% 沒有推導、紐約 12 GW 對北美吸納口徑不同。
- 檢查第 12 項（附錄歷史錨點）由 PASS 變 WARN（1/2 段）。附錄資料沒改，這是散文重寫的差異。

### 交持有人

- **時鐘相位**：依頁面自己的規則不換相，所以不需要拍板。但持有人要知道：供給與吸納已經大致相等，換相的領先觀察項有一半已觸及。下一個能改變判斷的數字是 2027-03 CBRE 2026 下半年報告的空置率與要價。
- **模板寫死「論點作廢」**：`.claude/skills/industry-analyst/templates/report_template.md` 第 123–125 行，在每條第一頁否證指標後面寫死「論點作廢」。這次是散文作者看到破線欄已有姿態，自己省掉了。其他 ID 會照樣印出來，與 kill 表姿態不一致的問題會在別份報告重現。這是 skill 檔，本次沒動，是否修改請持有人決定。
