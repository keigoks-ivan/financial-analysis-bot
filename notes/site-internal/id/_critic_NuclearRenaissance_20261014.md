# 冷讀報告：ID_NuclearRenaissance_20261014（industry-analyst v4.1）

審稿日 2026-10-14。依 id-review ID v4 模式 J1–J10，只讀 check_excerpt／check_report，必要處 grep evidence.json 與 playbook，查證 6 輪。

## 總判定

結論站得住，但標籤要寫得更誠實：**shortage（窄範圍）可以保留，不必退成 split**。🔴 0 條、🟡 7 條、🟢 4 條。

shortage 對 split 的壓力測試（J6）結果：

- 既有機組電量這一層，短缺證據比頁面寫的還硬。PJM 2028/29 容量拍賣結清在價格上限 $325，連續第三次貼上限；不設上限的模擬價是 $554.72，供給比可靠度要求少 6,831 MW，只有約 525 MW 新供給得標（來源見下）。頁面只把 $325 當成「容量價」，沒說它是上限，也沒引用缺口。
- 鈾這一層撐不起「短缺」。頁面自己的分層表把長約寫「偏緊」、現貨寫「平衡」，哈薩克上半年增產 8.6%，現貨 $89.63 低於長約 $96.50。三次判決 shortage／split／shortage，分歧就出在這一層。
- 所以「shortage 在既有機組電量、鈾僅偏緊」是證據支持的說法；把鈾長約也併入「短缺範圍」是頁面內最弱的一環（見 J9）。
- 7/24 勝率的反證論述（新建 14–15 年、短缺已合約化）成立，但 priced_in 這欄標 mid 缺乏證據（J6 第三問）。

## 🟡 清單

### 🟡 1（J7／J2）PJM $325 是價格上限，頁面誤以為上限數值不在證據包

- 原文錯誤：「兩篇都用 PJM 容量價 $325 作否證指標，本篇門檻設為 <$260，不採該篇的價格上限口徑，因為上限數值不在本次證據包」（thesis 與姊妹報告差異段）。
- 正確：$325/MW-日**就是**2028/29 拍賣的價格上限，且為連續第三次貼上限（前一次上限 $333.44）。姊妹報告 AIDataCenter 的熊線正是「結清價落在價格上限以下且缺口收斂至 3,000 MW 以內」，兩篇的口徑其實可以對齊，不是「不採上限口徑」。
- 影響：本頁熊線 <$260 等於「上限仍在，但價格掉到上限的 80% 以下」，實務上只有供給大幅補上才會發生；另一個更近的風險是上限規則本身。來源互相矛盾：有的說上限與下限延長到 2029/30 拍賣，有的說最後一場授權拍賣是 2026-12，之後上限回到 Net CONE（約 $550）。頁面「可否操縱」欄已提「上限規則可能被監管修改」，但沒有把這件事列進催化劑，也沒有寫缺口 6.8 GW。
- 建議修法：thesis 差異段改寫為「PJM $325 即為價格上限，連續三次貼限，缺口 6,831 MW」；kill 表現值欄補「（上限價）」；risks 催化劑加一條「2026-12 拍賣與上限規則」。
- 來源：https://www.opis.com/resources/energy-market-news-from-opis/pjms-2028-2029-capacity-auction-clears-at-price-cap-for-third-time/ ；https://www.rtoinsider.com/136577-pjm-capacity-auction-clears-325-cap-short-reliability-requirement/ ；as-of 2026-07-14。
- JSON 欄位：`kill_metrics[1].bear_threshold`、`sd_verdict_detail` 不需改，主要是 thesis 文字與 kill 表現值。

### 🟡 2（J7）新簽 PPA 現值與季別口徑：Amazon 日期與容量、Q3 基期缺

- 原文：「9 月底後再簽 Google 890 MW 增容……與 Amazon 190 MW」「現值 9 月底後至少 1.08 GW（2026-10-06）」「連兩季合計 <500 MW」。
- 問題 A（日期）：evidence 把 Amazon 標題日期記為 2026-09-30，但多家報導把宣布時間寫成 2026 年 10 月初。Google 890 MW 為 2026-10-06（evidence 已確認）。兩筆多半都落在 Q4 曆季，不是 Q3。
- 問題 B（容量口徑）：Amazon 協議是 20 年 PPA，涵蓋 Calvert Cliffs 約 690 MW 電力，其中含 190 MW 增容，預計 2030–2032 上線、約 $30 億投資。evidence 已自註「690 對 190 口徑不同，未讀到全文」，頁面只用 190 MW，沒有在頁面揭露這個口徑選擇。同日 Google 協議另含 15 年 2,700 MW 既有機組供電，頁面只在 kill 表括號寫「另有 2,700 MW 電源別待核」。
- 問題 C（基期）：熊線是「連兩季合計 <500 MW」，頁面給了 Q2（920 MW），Q3 曆季（7–9 月）的新簽數字沒給，催化劑段又寫「Q3 財報……季內新簽合計 ≥500 MW」。讀者無法判斷第一季是否已經低於線。若 Q3 曆季本身 <500 MW，熊線已走了一半，頁面現值欄「至少 1.08 GW」會讓人誤以為已大幅過線。
- 建議修法：現值欄分列「Q2：920 MW（含 Dresden 30 MW）／Q3 曆季：待查／10 月至今：Google 890 MW 增容＋Amazon PPA 約 690 MW（含 190 MW 增容）」，並把 Google 2,700 MW 15 年既有機組協議列為正面證據，寫進 thesis 的「現在」。
- 來源：https://world-nuclear-news.org/articles/constellation-amazon-agree-nuclear-focused-power-purchase-deal ；https://www.ans.org/news/article-8452/amazon-constellation-partner-for-calvert-cliffs-uprate/ ；https://www.powermag.com/google-deal-backs-890-mw-of-constellation-nuclear-uprates-at-11-pjm-reactors/ ；as-of 2026-10-06。
- JSON 欄位：`kill_metrics[2]` 現值欄、`now_state`。

### 🟡 3（J9）短缺範圍與分層表自相矛盾：鈾長約被列入短缺，卻在表內只寫「偏緊」

- 原文：summary「短缺只在既有機組與鈾長約」，`sd_verdict_detail`「短缺範圍只限既有機組電量與鈾長約兩層」；分層表「鈾（長約）偏緊」「鈾（現貨）平衡」；thesis「鈾層偏緊但不是全面短缺」。
- 問題：同一頁對鈾長約有兩個強度。依頁面自己的表，只有「既有機組電量」與「容量市場」兩列寫「短缺」。
- 影響：不改方向，但這是三次判決會分歧的根源，標籤字面超過了內文證據。
- 建議修法：把 `sd_verdict_detail` 改為「短缺只在既有機組電量與容量市場；鈾長約偏緊但現貨平衡，列為邊界層」，summary 同步。`sd_verdict_boundary: shortage/split` 保留，並在頁首燈號說明邊界來自鈾層。

### 🟡 4（J6）priced_in 標「中」缺證據，且證據包漏掉可得的 IPP 價格資料

- 原文：燈號「已定價 中｜燃料鏈已去評價，IPP 查不到」；估值章「12 檔中有 9 檔沒有倍數」「IPP 與 SMR 沒有本地資料，無法判斷擁擠度」。
- 問題：核心短缺範圍的名字（CEG、VST、CCJ）恰好是沒有價格或倍數資料的那幾檔，卻給出 mid 的結論欄。依 J6 第二問（26 週漲幅擁擠度），該格沒有被回答。
- 公開資料可補：Zacks 系分析稱 CEG 近六個月 −15.5%、VST −13.8%（另一表列 CEG 三個月 +19.5%，兩者矛盾，且 10 月 6 日 Google 協議當天 CEG 漲約 12%、VST 約 8%、TLN 約 7%）。方向上顯示 IPP 並未擁擠，這對「shortage×II 勝率只有 7/24」的反證有利，但頁面沒有用上。這些是二手來源，我不建議直接寫進數字，只建議頁面承認「IPP 價格走勢是可補的缺口」並把 priced_in 改為「查不到（不下判斷）」，或下次刷新時補 CEG／VST／CCJ 的 26 週報酬。
- 來源：https://finance.yahoo.com/markets/stocks/articles/ceg-stock-trails-industry-6-165500041.html ；https://247wallst.com/investing/2026/10/06/constellation-energy-soars-12-on-google-nuclear-deal-for-890-mw-vistra-jumps-8-talen-energy-climbs-7/ ；as-of 2026-10-06 前後，未能核對一手報價。
- JSON 欄位：`priced_in`。

### 🟡 5（J8／J3）資本週期結論用了自己宣告「不可比」的數字

- 原文：3.4「capex／折舊（CEG 上半年）：約 2.8 倍（含 Calpine，基期不可比）」，同段結論卻寫「資本支出在上升（CEG 上半年 capex 約為折舊 2.8 倍，含 Calpine）」；VST capex「口徑未對齊，不算比值」。
- 問題：重新框架成「capex 上升但容量少且慢」時，兩個量化支點（2.8 倍、VST 超過全年指引）都被自己標為不可比。真正撐得住這個框架的只有 2.2 GW 的增容清單與 CEG 負債 2.6 倍，後者也含 Calpine 併購。playbook 條目 1（短缺但資本大量湧入）要求具體數字作答，這裡的答案是定性。
- 建議修法：結論句刪掉 2.8 倍，改用 Google 890 MW 對應 $43 億（約 $480 萬／MW）、Amazon 約 $30 億、Crane 重啟的實際投資額作為「錢換到多少容量」的比值。這些數字已在證據包或可由證據包推得。
- 另一個小的內部不一致：2,188 MW 清單（Google 890＋Crane 835＋VST 433＋Dresden 30）沒有納入同頁引用的 Amazon 190 MW 增容，若納入為 2,378 MW，約占 97 GW 的 2.5%。頁面寫「約 2.2 GW」「2.3%」不錯，但清單不完整。

### 🟡 6（J4）分歧 3 的「無威脅」判別訊號偏弱

- 原文：「已反映：無法量化（沒有擁擠度資料）」，判別訊號用「非核協議單季累計 >1 GW」。
- 問題：訊號有數字，過關。但「市場最強版本」只引用地熱 150 MW 級協議，最強反方其實是燃氣：頁面自己寫「已有 hyperscaler 申請現場燃氣發電許可」卻沒給燃氣 MW。最強版本應該是燃氣規模，地熱是弱版本，與頁面結論「規模不對等」的立論有稻草人風險。
- 建議修法：補一個燃氣現場發電的 hyperscaler 容量數字，或明寫「查不到」。

### 🟡 7（J10）白話抽查

- 命中：「E −25% 且倍數再降兩成」（E 未解釋為獲利）；「alpha 來源」「風險控制線」「去評價」「錯殺候選」；3.3 的「S 曲線起點」。這些在 `_plainlang_styleguide.md` 屬於偏業內用語，主閱讀線建議換成「獲利下滑 25%」「超額報酬來源」「估值倍數下降」。不影響結論。

## 🟢 通過項目

- **J1**：Vogtle 14–15 年（2009 動工、2023–24 商轉）、Westinghouse EBITDA −54%（3.52 億降到 1.63 億，算式 −53.7%）、CEG 長期債 2.6 倍（191÷72.5＝2.63）皆可回溯；「LEU 美國唯一 HALEU 濃縮商」可接受但屬 T3 層級，建議個股 DD 再核。
- **J3**：TAM 算術全部驗過。每 GWe 約 170 tU；2030 裝機 457 GWe 對應 77,800 tU、約 2.02 億磅；×$96.5＝195 億美元，Bull ×$136＝275 億，Bear ×$80＝160 億，2027 同理，皆吻合。CAGR 6%（量 2.5%、價 3.8%）正確。上下路徑差 18% 有推導。長約年化簽量 6,600 萬磅對消耗約 37% 正確。
- **J5**：燈號五格與 thesis 文字一致（shortage／II／mid／mid）。
- **J8**：playbook 命中條目 1、7、14、18、19 皆有作答；條目 18 的換相雙閘有具體數字（長約月增率、3,300 萬磅對 2,700 萬磅）。

## 鈾價與長約數字是否為最新

核對結果：**目前頁面數字沒有過期**。

- 長約 $96.50（2026-08 與 2026-09 月底，Cameco 轉載 UxC／TradeTech）、現貨 $89.63（2026-09-30）。Sprott 稱長約八月創歷史新高約 $96，另有來源稱現貨 10 月中約 $89.5–89.75。Cameco 的長約 7 月底均價 $95.50 與頁面一致。
- 2026-10 月底價格要到 2026-10-31 才會公布，Cameco、Kazatomprom 的 Q3 數據與 BWXT、CEG 的 Q3 財報都在 10 月底到 11 月，**證據日之後沒有已發布的新數據會改動頁面數字**。
- 來源：https://www.nucnet.org/news/long-term-uranium-price-hit-all-time-high-in-august-says-sprott-10-4-2026 ；https://carboncredits.com/uranium-prices-today/ ；as-of 2026-10-12 前後。

## 未及查證

- 「近 26 週 TLN +3.9%、BWXT −40.5%、LEU −33.6%」與各檔倍數分位為程式輸出，依指示未重算。
- Oklo 現金約 $30 億、增資 $19 億，以及 Centrus 在手訂單 $45 億（evidence 為 T1，我只確認數字存在於證據包）。
- Westinghouse 產業分層表的「EPC 承壓」判斷、「BAM 5% 純度」、「OKLO 市值級距 large」的歸類。
- 1979–1988 取消 67 座（T4，Wikipedia 轉述 EIA）。
- UxC 上半年長約簽量 3,300 萬磅對 2,700 萬磅：證據為 Cameco MD&A 轉述，未讀到 UxC 原文。

## 處置（2026-10-14，局部修，不重判）

只改 🟡 指到的欄位，sd_verdict、clock_phase、conviction、sd_verdict_boundary、base_rate.action 都沒動。新增證據三條：X1（Yahoo Finance 日線還原價，T1）、X2（APPA 轉述 PJM 2026-07-14 新聞稿，T2；pjm.com 本機無法連線）、X3（Constellation 2026-09-30 新聞稿，T1）。查證用了 8 次。

### 已修

| 🟡 | 欄位 | 改前 → 改後 | 來源 |
|---|---|---|---|
| 1 | thesis.sister_reconcile[1].reason | 「不採該篇的價格上限口徑，因為上限數值不在本次證據包」→「$325/MW-日就是 2028/29 拍賣的價格上限，已連續第三次結清在上限，缺口 6,831 MW；本篇 <$260＝跌到上限八成以下，與該篇看的是同一件事，口徑可以對齊」 | X2 |
| 1 | risks.kill_table[1].now／manipulable | 「$325/MW-日（2028/29 交割年）」→ 補「即價格上限；缺口 6,831 MW」；可否操縱補「價格上下限只設定到 2026-12 這一場，之後規則未定」 | X2 |
| 1 | summary.kill_brief[1].now、id_meta.now_state、分層表「容量市場」列 | 補「上限價」與缺口 6,831 MW | X2 |
| 1 | risks.catalysts | 新增「2026-12 PJM 2029/30 容量拍賣（價格上下限的最後一場）」：仍在上限→維持；<$260 或上下限延長並調低上限→計入 kill 第 2 條 | X2 |
| 2 | id_meta.now_state、thesis.points[1]、thesis.derivation | 「9 月底後再簽…Amazon 190 MW」→「9 月 30 日與 Amazon 簽 20 年 690 MW（含 190 MW 增容），10 月 6 日再簽 Google 890 MW 增容」 | X3、S3 |
| 2 | risks.kill_table[2].now | 「9 月底後至少 1.08 GW」→「Q2 920 MW（CEG）；Q3 至少 690 MW（CEG–Amazon，VST／TLN 未查）；10 月 890 MW（Google 增容，另有 2,700 MW 15 年協議電源別待核）」 | B9、X3、S3 |
| 2 | summary.kill_brief[2].now、分層表「既有機組電量」列、risks.derivation、catalysts[0].pos | 「≥1.08 GW」→「Q2 920、Q3 ≥690、10 月 890 MW」「9 月底起再簽 1.58 GW」；推導補「Q2、Q3 已知 920＋690＝1,610 MW，在線上方」 | X3 |
| 3 | id_meta.sd_verdict_detail | 「短缺範圍只限既有機組電量與鈾長約兩層」→「短缺只在既有機組電量與容量市場兩層；鈾長約偏緊、現貨平衡，是短缺／分裂交界的來源」 | 頁面分層表 |
| 3 | summary.sd_note、thesis.lede、base_rate.downgrade_note | 同步拿掉「鈾長約＝短缺」，改為鈾層偏緊／交界層 | 同上 |
| 4 | valuation.priced_rows（CEG／VST／CCJ ret26w）、momentum、mid、derivations、debates[1].priced_in／our_view、base_rate.differences[2]、summary.priced_in_note | 「無本地週線」「CEG／VST 沒有資料」→ CEG 0.0%、VST −0.7%、CCJ −25.8%（日線，2026-04-14 至 10-13），倍數仍查不到 | X1 |
| 5 | base_rate.differences[0].point、mechanics.verdict.synthesis | 刪掉「CEG capex 約為折舊 2.8 倍」；改用 Google 增容每 MW 約 483 萬美元以上、Amazon 逾 $30 億換 190 MW 增容與 20 年延役 | S3、X3 |
| 5 | mechanics.verdict.capital_cycle[1].value | 「約 2.8 倍（含 Calpine，基期不可比）」→ 加「不作結論依據」 | D4 |
| 5 | 增容清單（thesis.derivation、base_rate 兩處、synthesis） | 2,188 MW、2.3%、約 2.2 GW → 納入 Amazon 190 MW：2,378 MW、2.5%、約 2.4 GW | X3 |
| 6 | debates[2].our_view | 補「最強的反方是燃氣，已有 hyperscaler 申請現場燃氣許可，但證據包查不到容量數字；規模不對等只對地熱成立」 | E3 |
| 7 | debates[1]／[3].our_view、mechanics.why_now.s_curve[2]、valuation | 「E −25%」→「獲利下滑 25%」；「alpha 來源」→「超額報酬來源」；「去評價」→「倍數下降」；「S 曲線起點」→「起步階段」 | — |
| 連帶 | id_meta.oneliner、summary.key_call | 「燃料鏈股跌三到四成」→「兩成半到四成」（補入 CCJ −25.8% 後原句說過頭） | X1 |

**priced_in：mid → mid（不變）。** CEG、VST 26 週持平、CCJ −25.8%，核心籃沒有追高，不符 high；CEG／VST／CCJ 仍沒有倍數，TLN 分位 71.8 高於中位，不符 low 的「核心籃倍數在歷史中位以下」。依頁面自己的 low／mid／high 定義維持 mid，但理由由「查不到」換成有價格資料。id_meta.action 不動。

**更正審稿意見一處**：Amazon 協議的宣布日是 2026-09-30（Constellation 新聞稿 dateline「LUSBY, MD – SEPT. 30, 2026」），審稿說的「10 月初」是 World Nuclear News 的報導日（10-01）。原證據 C2 的 9-30 正確，所以這筆屬曆年 Q3，不是 Q4。

### 略過

- Part 1 a)–b)：本篇已用現價估值輸入，不重做。
- Google 2,700 MW 15 年協議列為正面證據：電源別仍未查證，維持「待核」。
- 燃氣現場發電的 MW：查不到，頁面已寫明。
- PJM 上下限到期後的規則（延長或回到 Net CONE）：來源互相矛盾，未查證。頁面只寫「之後規則未定」。「12 月為第四場也是最後一場」由 APPA 的「第三場」與「共四場」推得。
- VST、TLN 的 Q3 曆季新簽：未查，頁面已寫明。
- 「風險控制線」「錯殺候選」兩個詞保留：前者是 playbook 條目 16 的角色標籤，後者在 action 與 pm_actions 多處使用，改了要動結論文字。
- 閘的黃燈（未處理，供參考）：D13 有 CEG Fwd P/E 21.93 對五年均值 23.94，但屬 T4、頁面沒有日期，不當承重證據，所以沒有拿來改 priced_in。PPA 熊線 500 MW 沒有外部錨點，Crane 一條取自公司目標。

### 交持有人

無。所有修改都不需要動 sd_verdict、clock_phase、conviction 或交界欄位。

### 重跑結果

gate PASS（紅 0、黃 7）→ prose 兩半皆交 → check PASS（check_id rc=0、validate rc=0、80KB）。頁面「短缺／分裂交界」字樣出現 3 處，新數字與改寫句已在 HTML 中逐條確認。
