你是 stock-analyst v20 的**散文層（prose）agent**，標的 BE（2026-10-25）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

**s3 到 s7 是整份報告的重心**（商業本質五章）：每章 4–6 條，每條 120–200 字，把 judgment 投影視圖裡對應問題的 reasoning、數字、反方依據全部鋪開，不要一句話帶過；s5 至少 3,000 bytes、s3／s4／s6 至少 1,500 bytes，低於直接 FAIL。

每段前面獨立一行標記 `<!-- SID:sX -->`（`decision` 段寫 `<!-- SID:decision -->`），緊接該段完整外層元素，格式與每段固定三塊（`<h2>`／`<p class="lead">`／`<ul class="pts">`）見散文卡 §6。表格注入標記依散文卡 §3 放在對應位置。

動筆前只列大綱（每章一句主張＋要用的白名單數字），列完就寫，不在腦中預演全文；每章寫完不回頭改。寫壞即交卷不補——這一輪沒有機械閘回饋、沒有第二次機會。

## 呈現硬規則

- 正文承重數字須能在 judgment 投影視圖追溯（原樣或四捨五入到小數點後 1 位），逐字複製數字白名單裡的字串（含 −／%／$ 符號）。
- 不寫 `s14`／`appA`／`appB`／`appC`／`revlog`／頁首儀表板——全部已由機械層生成，你補一句說明也不必要。
- 裁決單一居所：統一裁決只完整陳述於頁首與 `decision` 段，其餘章節提及僅一行「見§13」。
- 比較符 `<` `>` 一律寫 `&lt;` `&gt;`。
- 不渲染流程劇場（「自查發現 X」「我跑了驗證」這類過程對帳），只渲染結論本身。

## 禁

- WebSearch／WebFetch、Read 任何 `docs/dd/`、重讀自己剛寫過的檔。
- 改 `judgment.json` 任何欄位（發現判斷有問題只能在回覆中提一句，不得自行修改判斷）。


===== BUNDLE =====

## ① 任務頭

標的：BE　日期：2026-10-25　archetype：None　前份裁決：2026-09-05　進場·條件式（爆發候選）｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1434B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（900B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1121B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1803B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1058B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（373B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（570B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2011B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4425B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2911B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1434           3896-5566      5 條（2–6 內）  
s3                  8000         900           4970-7100      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3982          7713-11018      5 條（2–6 內）  
s6                 11000         373          7439-10627      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         570           2051-2930      5 條（2–6 內）  
s10                 5000        2011           2092-2989      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2911           2000-2089      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5516B；至少需散文≈39.48KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−181
−88%
−86%
−80%
−80
−75%
−74%
−55
−55%
−32%
−27
−23.6%
−19%
−16.38
−16%
−9.0%
−3.8%
−1.8
−0.37
0
0.6
0.63
0.75
0.78
0.94
0.96
1%
1.0
1
1.01
1.2
1.6%
02
2
2.05
2.5
2.71
3%
3
3.10
3.25
3.40
3.6
3.6%
3.75
3.9
4
04
4.2
4.4
4.4%
4.6
4.7
4.9%
05
5
5%
5.1
5.24
5.4
5.6
5.7%
5.9
6
07
7
7%
7.1
7.2%
7.4
08
8
8%
8.19
8.5%
9
09
9.2
10
10%
10.3
11
11.1%
11.2%
11.4
12%
12
13%
14
14.6
15%
15
17%
17
17.5
18.2%
19.4%
19.9%
20
20%
21%
21.4%
22
23%
23.1%
23.6%
23.6
24
25
25%
26%
26
28
29%
30
30%
31%
32%
32
33
33%
33.4
34%
34.5%
35
35%
35.8
36.9
37
38%
38.4%
40
40%
41%
41.5%
41.5
41.9%
42
43%
45
47%
48
49
50%
50
50.4
50.9
55
56%
58.7%
59%
59.48
59.5
60
60.1
65
67.6
70
73%
75
75%
80%
84.9
87%
90
93
98
99%
100%
100
120
138%
140
150%
175
179%
193.3
197
$197
200
207
210
231
250
252.87
273
274
285.7
350
500%
502.2
544
700
800
2022
2025
2026
2027
2028
2029
2030
2031
2035
20261025
1,070
1,235.8
```

---

## ⑦ C-1 機械段（已由腳本生成，禁止散文 agent 撰寫或覆寫）

已生成：（無，prepare 步驟可能未跑機械段）
`decision` 段仍由你撰寫，但段落內 `<!-- E12 -->` 標記之後會由系統自動接一句機械說明（觸發器見上表、重啟條件），你不需要、也不應該自己寫這句話。

---

## prose_card.md（散文卡）

<!-- source: .claude/skills/stock-analyst/references/v16/render-rules.md sha256:5c3eb1d20588e8d5 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->

# DD v20 散文卡

## 0 任務
你是v20散文agent，標的{ticker}（{date}）。判斷已由judge定案，你不判斷、不改judgment.json，只把thesis/moat/scenario_inputs/counter_evidence/decision_inputs五塊鋪成外資報告白話條列。工具只有Write，上限6輪，無Bash、無補寫輪：一次寫對，寫壞即FAIL。[design§4.4]

## 1 章節順序（＊=機械已生成，禁止重寫）
頁首儀表板＊→s1→s2→s3→s4→s5(§5.R/§5.F)→s6(§6.I)→s7→s8→s85(條件)→s9→s10→s11→s12→decision(§13)→s14＊→appA＊→appB＊(條件·循環)→appC＊(條件)→revlog＊ [render§1][render§2b]
五承重子模組標題字樣固定不可省併：§5.R報酬持續期檢核／§5.F對手財務深度對照／§6.I分部前瞻／§3.F／§9.D。[render§0.1][render§7]
內部下筆順序：archetype→s2→s3→s4→s5→s6→s7→s8→s9→s10→appA→(appB)→s11→s12→decision→s14→s1→頁首（後兩者回頭補）。[render§1]

## 2 篇幅預算（數字原文照抄；**下限是硬閘，寫短直接 FAIL、沒有補寫輪**）
全檔75–105KB(~100KB)，含s85上界115KB，**hard floor 70KB，低於直接FAIL不補寫**[design§4.4]。**散文本體(s1-s12+decision，不含表格)合計≥20KB；s5≥3KB、s3/s4/s6/s12≥1.5KB、s7/s10≥1.2KB**，低於任一即FAIL。**不得心算衍生數字**(季增幾個百分點、差值、比率都算新數字)，只用白名單裡的原數。實測警訊：2026-09-16 TXN 首跑只寫了 21KB 被擋，每條條列要把 judgment 的推導、數字、反方依據都鋪出來，不是一句話帶過。[run.py _gates_v20]Part I≥60%／商業本質(s3-s7)≥45%／估值(s10+appA)≤6.5KB／決策層(s11+s12+decision+s14)≤12KB／decision(s13)下限≥4KB／可見表格≤14張。[render§7][CLAUDE.md篇幅預算]
衝突flag：prose.tmpl(09-11)曾取消整檔bytes硬擋、改純結構驗收；design§4.4(09-16)已恢復floor+FAIL。本卡以design§4.4為準。[prose.tmpl][design§4.4]

## 3 每章寫什麼／judgment欄位／機械段
sid：寫什麼(render§7省法) → 主要欄位
s1：白話開場2-4句(這是什麼生意/為何此裁決/什麼會改變) → thesis
s2：引子一段話，H1-H3表自證(E2標記注入不重寫) → thesis
s3：市場空間+利潤池，E3保留解釋合併 → thesis(§3.F固定標題)
s4：Munger門檻，E4自證 → thesis
s5：核心，承重子模組留解釋餘自證 → moat
s6：只留進裁決子區塊解釋 → moat(§6.I固定標題)
s7：E9收斂為關鍵年+變化率 → moat(§7.E固定標題)
s8：beat/miss+guidance變化 → thesis/counter_evidence
s85：不砍，無上限(條件觸發才寫) → thesis
s9：E10自證 → decision_inputs(§9.D固定標題)
s10：只留裁決用的尺+E11情境樹 → scenario_inputs
s11：矛盾點→裁定表 → counter_evidence
s12：死法top3+MaxDD範圍，三視角(論點失敗／論點成功但股東經濟變差／價格已反映太多)各≥1條 → counter_evidence [prose.tmpl]
decision：chip(進場#166534／觀望#92400E／迴避#991B1B)+角色+執行語+kill_metrics+rearm_trigger+矩陣命中列(E12注入)，新資金／已持有／清倉／放寬四條各自獨立成`<li>` → decision_inputs [render§8][prose.tmpl]
表格注入標記(放對位置，未放則程式退到段尾)：`<!-- E2 -->`→s2「B｜」`<h3>`之後(H1-H3表)｜`<!-- E11 -->`→s10(情境樹合一表)｜`<!-- AUDIT -->`→decision(決策矩陣檢核，須在E12之前)｜`<!-- E12 -->`→decision(監測與觸發器表)｜`<!-- APPA_TABLE -->`→appA。[render§2]
機械禁寫：頁首儀表板(五卡/24格/改變主意三條)、s14、appA、appB、appC、revlog、全部E1-E12表格本體——你只放對應注釋標記，表格內容不寫。[render§2b][prose.tmpl]
欄位對映非精確schema：v20 judgment.json只五塊，比舊版(growth/valuation/contradictions/premortem/decision_out分field)粗，上表為粗配對；找不到對應內容以thesis/moat兜底，不得外推新數字。[design§4.2]

## 4 動筆方式（2026-09-16 改：不預演全文）
動筆前只列一張大綱：每章一句主張、要用到的白名單數字各列出來。列完就寫，**不要在腦中把全文先寫一遍**，每章寫完就交，不回頭改。**Write是唯一寫入動作，禁止先寫短稿再加字湊篇幅、禁止逐輪加字**。某段低於下界先查對應judgment欄位有沒有推導漏寫，不是灌水填充句。表格觸發leaks/標點問題，不得自行改表格檔。[render§0 改寫]
v20無Bash、無check_cmd、無FAIL後重寫一輪的機制——寫完即交卷。篇幅、數字白名單、禁用詞、標點由程式閘驗，不必自我核對。[design§4.4]

## 5 口吻與禁令
外資報告：白話、深入淺出、結論先行、能條列就條列。固定形狀：`<h2>標題`+`<p class="lead">`一句結論(≤40字)+`<ul class="pts"><li>`3-6條(每條一件事，80-200字，句號收尾，**整份不得出現「；」**，一句一個動詞)。**不要寫任何機器代號小字**(signal/val/row/moat 燈號等會被機器語言閘擋下)。[prose.tmpl][zh]

AI痕跡(看到就改)：
1.對比句「不是A是B／這就是」一頁最多一次，其餘直述具體主詞、不用抽象名詞(寫「銀行放款」不寫「主導因子」)。
2.每句一個主數字；括號排名只在是重點時寫成中文；t/p值/n只留計分卡與論點第一條。
3.不括號套括號、不用「——」「；」串子句——一句一動詞一個意思；「詳見」每條最多一個放句尾。
4.刪自我說明句(本頁不對…／值得注意的是)；三段最多一段收結論句，其餘講完事實就停。
5.有幾個講幾個不湊三個一組；一段最多兩個粗體，只給主張裡最重要的數字。
6.英文縮寫第一次中文+原文、第二次只用中文；中文與數字間半形空格，標點全形。
7.不用比喻(吹出/煞車/天花板等)，直述事實，引述原話例外。[zh-analyst-prose§一]

機器語言洩漏(禁渲染六類，render-rules§5)：①自我稽核紀錄(校驗紀錄/Guardrail✓✗)②機械三段顯示過程③skill機制詞(硬接線/(必填)/(防X教訓)/(QC-XX))④dd-meta路由/一致性註記⑤給自己看的提醒⑥章節標題不帶原始編號括注。判準：這句話是寫給讀者理解股票，還是證明我照skill做了？後者不渲染。範例：「row 8a」→「爆發候選路徑」；「row 8b」→「循環衛星進場路徑」。`<``>`比較符一律`&lt;``&gt;`。[render§5][render§8]
裁決單一居所：統一裁決只完整陳述於頁首+decision段，其餘章節提及僅一行「見§13」，禁止重述數字組合。[render§6]

呈現硬規則：正文承重數字須能在judgment.json追溯(原樣或四捨五入到小數點後1位)，§x.y／E1-E12／H1-H3／R1-R3／#n／FYxx／Qx等代號與4位數年份／≤12小整數不算新數字，不得心算外推出新數字。不寫流程對帳句(「自查發現X」「我跑了驗證」)，只渲染結論本身。同一結論性數字只在首次出現處寫全，其餘章節「見§X」引用不重貼。佔位文字(「（略）」「TODO」「待補」整段)一律不算寫完。[render§3][render§7][prose.tmpl]

## 6 輸出格式
每章一片段：獨立一行`<!-- SID:sX -->`，緊接完整外層元素`<section id="sX"><h2>N　標題</h2><p class="lead">…</p><ul class="pts">…</ul><div class="mach">…</div></section>`(decision用`id="decision"`)。只有Write+6輪，比照prose.tmpl分兩批：Write→{prose_a_path}(s1-s7)、Write→{prose_b_path}(s8-s12+decision，s85觸發併入b)。兩次Write完成，不逐段個別開檔。程式讀SID標記切成`prose/{sid}.html`。[prose.tmpl][render§1]


---

## ②c 理由文字禁用詞表（QC-40 機器語言，命中任一＝FAIL；這些是給程式看的代號，不是給讀者的話）

以下為 regex 原文，逐條避開（含變體）：

`row ?\d`　`Hard Veto`　`Soft Veto`　`signal ?[ABCX]\b`　`估值燈`　`val ?[🟢🟡🟠🔴]`　`MA ?[✅❌🟢🟡🟠]`　`Pure MA`　`盲點 ?\d`　`PREREG`　`dd-meta`　`runway_post_y5`　`capalloc`　`QC-\d`　`archetype`　`metadata`　`硬接線`　`接線[:：]`　`Guardrail`　`校驗紀錄`　`判定規則`　`\bgate\b`　`\bF2\b`　`row 8[ab]`　`爆發候選路徑`　`循環衛星進場路徑`

改寫原則：說結論本身，不說「燈號／閘／row／QC／驗算」這類流程代號。例：「估值燈色不變」→「估值結論不變」；「row 8a」→ 直接寫進場條件本身，不用路徑代號。

---

## judgment 投影視圖（dd_project.view_for，緊湊 JSON）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"BE","date":"2026-10-25","schema":"v15.2","contract":"v19","company_name":"Bloom Energy"},"oneliner":"Bloom 以固態氧化物燃料電池吃下電網接不上電的資料中心需求，Q3 營收年增 138%、non-GAAP 營益率 23%；但單季自由現金流 −1.8 億美元、單一客戶占比過高仍未解。現價 FY2 本益比約 37 倍，等 Q4 現金流轉正再加碼","thesis":{"H":[{"id":"H1","text":"AI 資料中心現場供電需求延續，FY2027 EPS 達共識九成以上","2y":"FY2027 non-GAAP EPS ≥4.7 美元、營收年增 ≥30%","5y":null,"10y":null,"threshold":"FY2027 non-GAAP EPS ≥4.7 美元（共識 5.24 美元的九成）","source":"季報新聞稿、2027-02 年度財測","drift_rule":"TTM 營收或 EPS 偏離基本路徑連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"規模化帶來的毛利擴張可以持續，不被加急交付與新產線成本吃掉","2y":"FY2026 全年 non-GAAP 毛利率 ≥34%、FY2027 ≥33%，non-GAAP 營益率 ≥20%","5y":null,"10y":null,"threshold":"non-GAAP 毛利率年度 ≥33%、營益率 ≥20%","source":"季報新聞稿與法說","drift_rule":"TTM 毛利率低於門檻連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H3","text":"客戶與市場多元化：第二曲線（公用事業、工商業、碳捕捉、國際）讓最大客戶占比下降","2y":null,"5y":"最大單一客戶占年營收 ≤35%，且至少一條第二曲線年營收占比 >10%","10y":null,"threshold":"FY2028 前最大客戶占年營收 ≤35%（FY2025 為 43%）","source":"10-K 客戶集中度與營收分類揭露","drift_rule":"最大客戶占比 TTM 偏離目標路徑連 4 季 ≥5pp 視為削弱，連 6 季 ≥10pp 視為反轉"}],"R":[{"id":"R1","text":"現金轉換失靈：營收與利潤成長，營業現金流卻轉負，與上一季 CFO 承諾相反","h_ref":"H2","clock":"⚡","threshold":"Q4 營業現金流 <0 或 FY2026 全年自由現金流 <0","evidence_refs":[]},{"id":"R2","text":"客戶集中與關係人交易：單一客戶占 Q2 營收約 73%、Q1 約 50%，FY2025 最大客戶為 Brookfield 合資關係人","h_ref":"H3","clock":"🔥","threshold":"FY2026 最大客戶占年營收 >50% 或前三大應收 >75%","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#2"]},{"id":"R3","text":"鈧供應與中國出口管制，加上放空報告引發的證券集體訴訟","h_ref":"H2","clock":"⚡","threshold":"揭露鈧短缺或交付延誤；訴訟進入證據開示或 SEC 介入","evidence_refs":["geo_supply_chain#0","geo_supply_chain#3","major_events#0","lawsuit_class_action#0","capital_markets_pricing#4"]},{"id":"R4","text":"地方許可阻力：Santa Clara 燃料限制、新墨西哥 Project Jupiter 空氣許可待定、俄亥俄 Hilliard 挑戰","h_ref":"H1","clock":"🔥","threshold":"兩個以上 100MW 級專案因許可延後 ≥2 季","evidence_refs":["regulatory_antitrust#1"]},{"id":"R5","text":"替代技術與新進者：渦輪產能 2029–30 釋出，FuelCell、Doosan 進入資料中心，電池儲能追上","h_ref":"H2","clock":"🐢","threshold":"產品毛利率連 2 季年減，或競爭者拿下 GW 級資料中心合約","evidence_refs":["supply_demand_durability#2","substitute_technology#0","substitute_technology#2","competitive_share_entrants#1","competitive_share_entrants#2"]},{"id":"R6","text":"關稅與供應鏈集中：鋼鋁銅 50% 關稅、元件主要來自台灣、製造集中在 Fremont","h_ref":"H2","clock":"🔥","threshold":"non-GAAP 毛利率 <32% 且公司歸因關稅或原物料","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"]}],"single_thing":{"description":"最大關係人客戶（經 Brookfield 合資的融資體系）宣布延後或縮減 GW 級部署","why_fatal":"單一客戶占 2026 Q2 營收約 73%，FY2027 共識 EPS 年增約六成大部分仰賴這批交付；產品營收在交付驗收時才認列，延後一季就直接少掉數億美元營收","if_happens":"FY2027 EPS 向空方路徑 4 美元附近靠攏，倍數同步壓縮，股價可能腰斬以上；CFO 稱融資方仍須收貨，但只能緩衝、無法抵銷","how_monitor":"10-Q 客戶占比、2027-02 積壓訂單與年度財測、Oracle 與 Brookfield 公開的資本支出與園區進度","probability":"15–20%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":36.9,"peg_fy2":0.63,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":3.25,"FY2027E":5.24,"FY2028E":8.19},"fy_end_month":12,"eps_basis":"non-GAAP 稀釋 EPS 共識（Koyfin 2026-10-24 快照）；FY2025 non-GAAP 實際值事實表未涵蓋（GAAP 為 −0.37），基期留空"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"低","fingerprint":"高成長、2026 年才轉為 GAAP 獲利、超大客戶集中；若 AI 資本支出轉向，行為會像循環股"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久至 2028 前後：資料中心電網互連瓶頸與渦輪訂單排到 2029–30（二手來源）；供給可逆性中等，渦輪與其他現場發電產能釋出後時間溢價收窄","bargaining":{"up":"鈧（陶瓷電解質）與台灣元件為主要上游瓶頸，鋼鋁銅受 50% 關稅","down":"最大單一客戶 2026 Q2 占營收約 73%，且透過融資方付款，買方議價力強","geo":"第三方估鈧約三分之二源自中國，中國稀土出口管制預計 2026-11-10 恢復；元件主要由台灣供應"},"profit_pool_dir":"資料中心電力利潤池由電網與集中式電廠往現場發電移動，Bloom 目前是最大受益者","tam_table":[{"item":"積壓訂單","value":"約 200 億美元（產品 60 億、服務 140 億），2025-10 報導；Q3 法說稱成長快於營收但未給新數字"},{"item":"部署能見度","value":"公司稱對 25 GW 部署有能見度（2026 Q2 後二手摘要）"},{"item":"資料中心全現場發電占比","value":"公司 2026-04 投資人簡報：開發商預期 2030 年全現場發電資料中心占比逐次上調，約三成以上（簡報數字排版不清）"},{"item":"工商業","value":"公司自辦調查：四分之一工商設施預期 2030 年全現場供電，2035 年 35%（Q3 法說，公司自述）"},{"item":"2027 年新增 AI 資料中心容量","value":"CEO 稱約 30–40 GW 新容量上線（2026-07-28 法說）"},{"item":"利潤池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"不燃燒、許可快、交期以月計的模組化現場發電，加上 GW 級產能帶來的成本曲線領先","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"產品毛利率 38.4%（年增 250bp、季增 120bp）；全年毛利率指引 34%，2025 年為 30%；CFO 稱定價強、降本持續；Nebius 由燃氣改選 Bloom（2026-07-28 法說）；新進者首份資料中心合約僅 75MW","peer_na_reason":"同業 ROIC 事實表未涵蓋，改以毛利率與營益率 spread 代替","threats":[{"level":"🟡","text":"FuelCell 簽首份資料中心容量預留協議（德州 75MW），技術不同、毛利率為負，屬點對點","p":20,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"Doosan 美國子公司 HyAxiom 以磷酸型燃料電池首度進入美國資料中心，屬點對點","p":20,"evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"燃氣渦輪產能 2029–30 釋出，加上電池儲能與其他現場發電技術追上，時間溢價收窄；目前是窗口期而非新攻擊，但屬破壞性競爭，機率取 35%","p":35,"evidence_refs":["supply_demand_durability#2","substitute_technology#0","substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率×周轉未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心營運商，決策者是超大規模業者，付款者多為融資方（Brookfield 承諾擴至 250 億美元）；三角色都成立。需要是真的（CEO 引 NVIDIA：GW 級資料中心延後一季少 100 億美元營收），但急迫性來自電網與渦輪短缺，2029 年後是否持久未證"},{"item":"決策層級","level":"🟡","text":"替代以單一園區、單一區塊為決策單位；新案可改選渦輪或引擎（CEO 也承認各種快速供電技術都有空間），已裝機有服務合約綁定，但設備可轉移，轉換成本只在既有站點"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的價值主要落在算力營收端；Bloom 拿產品毛利 38%，融資方持有資產拿收益，最大客戶占營收七成以上，買方議價力強；上游鈧與台灣元件集中"},{"item":"社會容忍度","level":"🟡","text":"非燃燒、低水耗獲社區與州長背書；但 Santa Clara 限制現場發電燃料、新墨西哥 Project Jupiter 許可兩度被拒、俄亥俄 Hilliard 挑戰亞馬遜燃料電池案，地方許可是實際上限"}],"roiic":"事實表未涵蓋投入資本；方向證據：Q3 non-GAAP 營業利益 285.7 百萬美元（年增逾 500%），前三季資本支出僅 231 百萬美元（法說），增量報酬方向偏高，但營運資金吸收未拆分，無法給數字","reinvest_rate":"事實表未涵蓋 D&A 與營運資金變動；前三季營業現金流約 273 百萬美元（自由現金流 +42 加資本支出 231，由法說數字推得），多數被擴產與營運資金吃掉","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩項輸入皆缺，天花板留空，情境樹按超出處理"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","BE":31.24,"GEV":20.21,"VRT":38.04,"CMI":25.32,"FCEL":-32.39,"PLUG":-18.55,"unit":"%"},{"metric":"營業利益率","BE":11.24,"GEV":4.36,"VRT":19.4,"CMI":11.14,"FCEL":-87.95,"PLUG":-67.5,"unit":"%"},{"metric":"FCF 利潤率","BE":20.07,"GEV":30.07,"VRT":25.47,"CMI":9.7,"FCEL":-73.46,"PLUG":-75.33,"unit":"%"},{"metric":"研發密度","BE":7.08,"GEV":3.17,"VRT":null,"CMI":4.14,"FCEL":18.58,"PLUG":7.25,"unit":"%"}],"competitors":[{"name":"GEV","gm":20.21,"om":4.36,"fcf_margin":30.07,"rd_intensity":3.17,"strategy_note":"燃氣渦輪龍頭，TTM 營益率 4.4% 低於 BE，但 FCF 利潤率 30% 靠預收款；訂單排到 2029–30 是 BE 的時間窗口，產能釋出後是最大對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"VRT","gm":38.04,"om":19.4,"fcf_margin":25.47,"rd_intensity":null,"strategy_note":"資料中心電力與散熱設備，營益率 19.4% 高於 BE 的 TTM；互補多於競爭，800V 直流架構可能是合作或交鋒點","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CMI","gm":25.32,"om":11.14,"fcf_margin":9.7,"rd_intensity":4.14,"strategy_note":"往復式引擎與備用發電，營益率 11.1% 與 BE 相當；燃燒式技術在排放許可上落後","period":"TTM ending 2026-06-30（4季加總）"},{"name":"FCEL","gm":-32.39,"om":-87.95,"fcf_margin":-73.46,"rd_intensity":18.58,"strategy_note":"熔融碳酸鹽燃料電池，毛利率 −32%、營益率 −88%，剛簽首份 75MW 資料中心預留協議，規模與成本差距大","period":"TTM ending 2026-07-31（4季加總）"},{"name":"PLUG","gm":-18.55,"om":-67.5,"fcf_margin":-75.33,"rd_intensity":7.25,"strategy_note":"氫燃料電池，毛利率 −19%、FCF 利潤率 −75%，財務上無力在固定式大型發電與 BE 競爭","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（交付 GW 數），價與降本為輔（產品毛利擴張），無併購、無回購","runway_years":"≥10（現場發電占資料中心與工商業用電比例仍低；精確滲透率事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"投入資本與 D&A 事實表未涵蓋，內生天花板無法算出；共識 FY2026→FY2028 EPS 年化 58.7% 是否在天花板內無法證明，保守視為超出","segments":[{"item":"產品","value":"Q3 營收 1,070 百萬美元（87%），年增 179%，毛利率 38.4%"},{"item":"服務","value":"Q3 營收 67.6 百萬美元，年增 15%，毛利率 21.4%"},{"item":"安裝","value":"Q3 營收 84.9 百萬美元，年增 29%，毛利率未揭露，拖累總毛利"}],"decay_signals":["亮：EPS 成長顯著快於營收（共識 EPS 年化約 59% 對營收約 47%）","亮：FCF/NI 偏低（Q3 自由現金流 −181 百萬美元、前三季 +42 百萬美元，遠低於淨利）","未亮：毛利率仍逐季年增","未亮：SBC 占營收 4.9%，未超過 5% 且非逐年上升","資料缺口：產業估值倍數近三年走勢、核心市占率精確值"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，無回購與股息；資本全數投入擴產與營運資金"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"無回購","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 單季 60.1 百萬美元、占營收 4.9%；股數變化事實表未涵蓋，淨稀釋率無法計算","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY1 與 FY2 non-GAAP EPS）","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋，只有利潤率對照"},"fwd_pe":59.48,"peg":1.01,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 本益比 59.5 倍、FY2 36.9 倍；PEG（FY1）約 1.0、（FY2）約 0.6，便宜的一面被現金轉換與集中度風險抵銷；基本情境五年年化約 7%，低於 8% 門檻；五年分位事實表未涵蓋。結論為偏貴而非極貴","upside_short_pct":7.1,"upside_mid_pct":41.5},"trap_analysis":{"verdict":"🟡","label":"現金轉換與客戶集中待驗"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"燃氣渦輪大廠訂單排到 2029–30，燃料電池短交期是替代方案；新進者（FuelCell 75MW、Doosan HyAxiom）與電池儲能等替代技術在追","assumption":"時間窗口內拿下的客戶會轉成長期服務合約與重複下單（2025 年訂單 80% 來自重複客戶，CEO 說法）","consequence":"若 AI 資本支出放緩或渦輪產能釋出，新訂單出現斷層，EPS 回到 4 美元以下、倍數壓到 14 倍，股價約 50 美元（−74%）","ruling":"採納為空方情境，機率 30%；目前沒有訂單減速的證據，CEO 稱積壓訂單成長快於營收，但拒絕給數字","watch":"2027-02 年度財測與積壓訂單、產品毛利率、競爭者 GW 級合約","evidence_refs":["supply_demand_durability#2","substitute_technology#0","competitive_share_entrants#1","competitive_share_entrants#2"],"fact_refs":["f_kpi5_non_gaap_gross_margin","f_kpi6_management_guidance_fy20"]},{"view":"論點失敗","evidence":"放空報告與集體訴訟指控低報對中國鈧的依賴；第三方估三分之二源自中國；中國稀土出口管制預計 2026-11-10 恢復；製造集中在 Fremont，位於地震帶","assumption":"2026-07-28 CEO 稱鈧可取得量足夠、對應 25 GW 部署、不依賴中國","consequence":"若鈧斷供，交付延誤、毛利率下滑，且訴訟坐實會傷及管理層可信度","ruling":"不可裁決，要等到 FY2026 10-K（2027-02）：公司說法是一手但沒給數字，第三方估計是二手；先列為短期風險","watch":"11-10 之後的交付與毛利率、10-K 對鈧來源的揭露、訴訟駁回動議","evidence_refs":["geo_supply_chain#0","geo_supply_chain#3","geo_supply_chain#1","capital_markets_pricing#4"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營業現金流 −27 百萬美元、自由現金流 −181 百萬美元，存貨、合約資產、應收增加；多數客戶經融資方分期付款；最大客戶為關係人、占 Q2 營收約 73%；SBC 占 non-GAAP 營業利益 21%","assumption":"營收成長會等比例轉成自由現金流，合約資產會隨帳單里程碑周轉","consequence":"EPS 照共識成長，但現金被營運資金與擴產吃掉，SBC 稀釋股東；大客戶議價壓住毛利，每股價值成長低於 EPS 成長","ruling":"部分採納：不追價、倉位上限下修，等 Q4 現金流驗證；年初至今自由現金流仍為正，尚不構成反轉","watch":"Q4 營業現金流、FCF/NI、合約資產周轉、10-K 客戶占比","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#2"],"fact_refs":["f_kpi3_free_cash_flow","f_kpi4_stock_based_compensation"]},{"view":"價格已反映太多","evidence":"FY1 本益比 59.5 倍；FY1 共識三個月內上修近 20%，已把年內三次上調財測反映進去；賣方目標價 10–350 美元，分歧極大","assumption":"FY2028 EPS 達 8.19 美元，之後仍維持雙位數成長","consequence":"基本情境五年年化約 7%，即使論點成立，報酬也只是中等","ruling":"部分採納：FY2 36.9 倍不算極端，但基本報酬不足以支撐在現金未驗證前加碼","watch":"FY2 本益比、共識修正方向","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-80,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 252.87 → 本次 193.3（-23.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=252.87","side_b":"本次 price_at_dd=193.3","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場·條件式（爆發候選） → 本次 觀望","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場·條件式（爆發候選）","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟠、均線 ✅→🟢。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟠、均線 ✅→🟢。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 252.87 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 252.87 美元：Bull 價 502.2、Bear 價 35.8，五年期望值 −9.0%，基準年化 −3.8%，不對稱比 0.96","side_b":"本次情境、股價仍用 252.87 美元：Bull 價 544、Bear 價 50.4，五年期望值 +8.5%，基準年化 1.6%，不對稱比 1.2","ruling":"先換情境、股價不動：五年期望值多 17.5 個百分點，基準年化多 5.4 個百分點。不對稱比由 0.96 變為 1.2。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 252.87 美元：五年期望值 +8.5%，基準年化 1.6%，不對稱比 1.2","side_b":"本次情境、股價 193.3 美元：五年期望值 +41.9%，基準年化 7.2%，不對稱比 2.05","ruling":"再換股價、情境不動：起點價下跌 23.6%，五年期望值多 33.4 個百分點，基準年化多 5.6 個百分點，不對稱比由 1.2 升到 2.05。合計五年期望值比前份多 50.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"現金轉換：上一季承諾與本季實績","cause":null,"prior_field":null,"side_a":"2026-07-28 CFO：營業利益增額 100% 轉為營運現金流，新基準 3.75 億美元以上；Q2 自由現金流 175 百萬美元","side_b":"2026-10-22 CFO：Q3 營業現金流 −27 百萬美元、自由現金流 −181 百萬美元，歸因存貨、合約資產、應收增加，稱「不是趨勢的開始」","ruling":"一次性說法不採信也不否定，先列為未證、持續監測；若 Q4 營業現金流仍為負，視為歸因證偽","evidence_level":"一手（兩季法說逐字稿）","settle_metric":"Q4 2026 單季營業現金流與全年自由現金流","if_then":["若 Q4 營業現金流 >0 且全年自由現金流 >0，執行加碼至 3% 上限","若 Q4 營業現金流 <0，減碼一半，凍結加碼至 FY2027 Q2"],"evidence_refs":[]},{"axis":"鈧供應是否依賴中國（不可調和）","cause":null,"prior_field":null,"side_a":"2026-07-28 CEO：鈧可取得量足夠，已掌握對應 25 GW 部署的能見度，且不依賴中國；但未給用量與庫存數字","side_b":"第三方研究估約三分之二源自中國；2026-07-08 放空報告後股價跌 5.7%，Nevins 集體訴訟指控低報依賴；中國出口管制預計 11-10 恢復","ruling":"暫採公司說法，依據是 10-K 稱至今無重大零件短缺，且公司已在法說公開否認；但訴訟仍在、數字未揭露，風險列為短期，不解除","evidence_level":"一手否認對二手估計","settle_metric":"FY2026 10-K 對鈧來源的揭露與 Q4 non-GAAP 毛利率","if_then":["若 10-K 揭露中國來源 >50%，或 11-10 後出現交付延誤，減碼一半","若 10-K 揭露替代來源且 Q4 non-GAAP 毛利率 ≥34%，解除此風險標記"],"evidence_refs":["geo_supply_chain#0","geo_supply_chain#3","capital_markets_pricing#4","major_events#0","lawsuit_class_action#0"]},{"axis":"客戶集中度","cause":null,"prior_field":null,"side_a":"2026-07-28 CEO：2026 營收財測不依賴任何單一專案；CFO：集中度反映交付時點，不代表積壓訂單組成","side_b":"2026 Q2 單一客戶約占營收 73%、Q1 約 50%、FY2025 43%（關係人）；2025 年底前三大占應收 41%／17%／15%","ruling":"可調和、屬程度差異：積壓訂單可能較分散，但營收與應收實際上高度集中，交付時點的解釋只成立一半","evidence_level":"一手（10-K、10-Q）","settle_metric":"FY2026 10-K 最大客戶占年營收","if_then":["若最大客戶占年營收 >50%，停止加碼","若降到 35% 以下且有第二曲線營收揭露，H3 進度確認"],"evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2 本益比 36.9 倍、FY2→FY3 共識 EPS 成長約 56%；前份加碼價位已到；RSI 33、26 週 −16%；年內三次上調財測全部兌現","side_b":"Q3 現金流轉負，與上一季承諾相反；單一客戶占比過高；基本情境五年年化約 7%","ruling":"暫不加碼，等 Q4 現金流；價格到位但論點有一項未驗證，現有倉位不動","evidence_level":"事實表與法說","settle_metric":"Q4 營業現金流","if_then":["Q4 現金流轉正且股價維持 FY2 本益比 ≤40 倍，加碼","股價續漲但現金流未驗證，不追"],"evidence_refs":[]},{"axis":"估值、裁決、角色與機率漂移","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-09-05：股價 252.87 美元、FY1 本益比約 93 倍（2.71 美元），估值落在最貴一級；裁決為條件式進場，角色衛星；多空機率 25／30","side_b":"本次股價 193.3 美元（−23.6%），FY1 共識上修至 3.25 美元；FY1 本益比 59.5 倍、FY2 36.9 倍，估值下修一級為偏貴；機率維持多 25、基 45、空 30；裁決與角色依新估值與新增的等待條件重新判定","ruling":"倍數下降一半來自股價、一半來自 EPS 上修，以價格變動歸類；機率不動，因為空方情境的依據（渦輪產能、集中度）沒有改變","evidence_level":"事實表","settle_metric":"FY2 本益比","if_then":["FY2 本益比回到 45 倍以上且現金流未驗證，維持不加碼"],"evidence_refs":[]},{"axis":"護城河、跑道、陷阱、訊號、公司類型","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap","signal","archetype"],"side_a":"前份：護城河向上、成長跑道寬、價值陷阱風險中、綜合訊號 B 級、公司類型為品質複利成長","side_b":"本次五項維持：Q3 產品毛利率 38.4%、財測年內第三度上調、碳捕捉與公用事業第二曲線有具名案例；但新進者首度進入資料中心、Q3 現金轉負，公司類型信心降為低","ruling":"新證據同時強化成長與暴露現金風險，方向不變、信心下調","evidence_level":"一手法說與第三方","settle_metric":"Q4 財報","if_then":["若產品毛利率連 2 季年減，護城河方向改判持平"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"axis":"回撤區間與循環位置","cause":"方法變動","prior_field":["max_dd_pct","cycle_position"],"side_a":"前份最大回撤單點 −86%，循環位置未設","side_b":"本次改為區間 −80%～−55%，由空方情境終點與高波動歷史推出；循環位置仍不設（非循環股，AI 資本支出風險放在空方情境）","ruling":"改用區間以符合現行規格，下緣仍覆蓋空方終點跌幅","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"加碼條件改寫（前份觸發器已發火）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"已在場（衛星首階）；加碼雙軌：①回檔至 FY2 前瞻本益比 ≤40x（約 $197）且論點無損；②10-K 明示 FEOC 達標＋年化產能 >2.5GW（不論價位，≤60x）","side_b":"Q4 財報（2027-02）單季營業現金流轉正、FY2026 全年自由現金流為正，且股價維持 FY2 本益比 ≤40 倍（約 210 美元）以內；前份第②軌保留","ruling":"前份第①軌的價格條件已發火（FY2 本益比 36.9 倍、股價 193.3 美元低於 197 美元），但「論點無損」不成立：Q3 現金流與上一季承諾相反，所以加碼暫緩，改把現金流列為必要條件；第②軌外國關注實體規定資料事實表未涵蓋，保留不退休","evidence_level":"事實表與法說","settle_metric":"Q4 營業現金流","if_then":["條件成立，加碼至 3% 上限","Q4 營業現金流為負，減碼一半"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點","side_b":"最大關係人客戶（經 Brookfield 合資的融資體系）宣布延後或縮減 GW 級部署","ruling":"單一客戶占 Q2 營收約 73%，是數學上最大的單一敏感度，故設為唯一致命點","evidence_level":"一手（10-Q）","settle_metric":"10-Q 客戶占比與客戶公告","if_then":["延後 ≥2 季或縮減 ≥30%，清倉"],"evidence_refs":["customer_second_source#1"]},{"axis":"清倉與減碼門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定清倉門檻","side_b":"non-GAAP 毛利率連 2 季 <31% 清倉；全年自由現金流 <0 減碼；FY2027 營收指引年增 <25% 減碼；最大客戶占年營收 >50% 停止加碼","ruling":"補上可監測的數字門檻，取代前份只有加碼條件、沒有退出條件的缺口","evidence_level":"方法","settle_metric":"季報新聞稿與 10-K","if_then":["任一減碼門檻觸發，減碼一半","毛利率門檻觸發，清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2027 財測是否支撐需求延續","type":"假設驗證","maps_to":"H1","metric":"FY2027 營收指引中點年增率","threshold":"≥30%","action":"達標維持；<25% 減碼一半","source_freq":"Q4 財報，年一次","date":"2027-02","evidence_refs":[]},{"n":2,"text":"Q4 現金流驗證上一季承諾","type":"減碼","maps_to":"R1","metric":"Q4 單季營業現金流與 FY2026 全年自由現金流","threshold":"單季營業現金流 <0 或全年自由現金流 <0","action":"減碼一半，凍結加碼至 FY2027 Q2","source_freq":"季報","date":"2027-02","evidence_refs":[]},{"n":3,"text":"最大客戶延後或縮減 GW 級部署","type":"Single Thing","maps_to":"R2","metric":"公司或客戶揭露的部署時程","threshold":"延後 ≥2 季或縮減 ≥30%","action":"清倉","source_freq":"每季 10-Q 與新聞稿","date":null,"evidence_refs":["customer_second_source#1","customer_concentration_credit#2"]},{"n":4,"text":"中國稀土出口管制恢復後的鈧供應","type":"風險","maps_to":"R3","metric":"交付延誤揭露、non-GAAP 毛利率","threshold":"揭露鈧短缺或交付延誤，或毛利率因材料成本降至 32% 以下","action":"減碼一半","source_freq":"季報與公司公告","date":"2026-11-10","evidence_refs":["geo_supply_chain#3","geo_supply_chain#0"]},{"n":5,"text":"現金流轉正後執行加碼","type":"估值rearm","maps_to":"R1","metric":"Q4 營業現金流、FY2026 自由現金流、FY2 本益比","threshold":"單季營業現金流 >0、全年自由現金流 >0，且 FY2 本益比 ≤40 倍（約 210 美元）","action":"加碼至 3% 上限","source_freq":"Q4 財報","date":"2027-02","evidence_refs":[]},{"n":6,"text":"前份第二軌加碼條件保留","type":"加碼","maps_to":"H1","metric":"10-K 外國關注實體規定揭露、年化產能","threshold":"10-K 明示達標，且年化產能 >2.5GW（外國關注實體規定事實表未涵蓋，屬資料缺口）","action":"加碼至 3% 上限，FY2 本益比 ≤60 倍內不論價位","source_freq":"10-K，年一次","date":"2027-02","evidence_refs":[]},{"n":7,"text":"毛利率崩落代表定價力失守","type":"清倉","maps_to":"H2","metric":"non-GAAP 毛利率","threshold":"連 2 季 <31%","action":"清倉","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#2","substitute_technology#0"]},{"n":8,"text":"客戶集中度惡化","type":"風險","maps_to":"R2","metric":"10-K 最大客戶占年營收、前三大占應收","threshold":"最大客戶 >50% 或前三大應收 >75%","action":"停止加碼","source_freq":"10-K，年一次","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","customer_second_source#1"]},{"n":9,"text":"證券集體訴訟進度","type":"風險","maps_to":"R3","metric":"Nevins 案程序","threshold":"駁回動議被否決並進入證據開示，或 SEC 介入","action":"減碼一半；SEC 或刑事調查則清倉","source_freq":"法院文件，不定期","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":10,"text":"地方許可阻力","type":"風險","maps_to":"R4","metric":"100MW 以上專案許可結果","threshold":"兩個以上專案因許可延後 ≥2 季","action":"停止加碼","source_freq":"新聞與公司揭露","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":11,"text":"關稅與台灣供應吸收失敗","type":"風險","maps_to":"R6","metric":"non-GAAP 毛利率與公司歸因","threshold":"毛利率 <32% 且公司歸因關稅或原物料","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"]},{"n":12,"text":"Q4 財報與 FY2027 財測後全面複審","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑完整研究","source_freq":"年一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"non-GAAP 毛利率（季）","bear_threshold":"連 2 季 <31%","window":"FY2027 任兩季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"全年自由現金流","bear_threshold":"FY2026 或 FY2027 全年 <0","window":"2027-02 年報起","source":"公司現金流量表","last_status":"warning"},{"metric":"FY2027 營收指引中點年增率","bear_threshold":"<25%","window":"2027-02 財測","source":"Q4 2026 新聞稿","last_status":"unknown"},{"metric":"最大單一客戶占年營收","bear_threshold":">50%","window":"FY2026 10-K","source":"10-K Item 1","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=-16.38, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bloom 的成長依據有營收實績，但 Bull 路徑沒有量價骨架。第二曲線和滲透率缺少一手來源，同類高估值能源設備股過去 5 年的報酬遠低於 Bull 隱含的每年 23%，而判斷物沒有說明本案為何不同，所以 Bull 依據目前不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟢'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟢'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟢'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"Q4 財報（2027-02）單季營業現金流轉正、FY2026 全年自由現金流為正，且股價維持 FY2 本益比 ≤40 倍（約 210 美元）以內","exec_line":"現有首階持股不動、不加碼；加碼條件成立後加到 3% 上限；全年自由現金流為負減碼一半；毛利率連 2 季 <31% 或最大客戶延後 GW 級部署則清倉"},"reasoning":{"industry":"營收分部（Q3 法說）：產品 1,070 百萬美元（87%，交付驗收即認列，毛利率 38.4%）、服務 67.6 百萬美元（毛利率 21.4%）、安裝 84.9 百萬美元（依進度認列，季間波動大）。Q3 總營收 1,235.8 百萬美元，GAAP 營益率 18.2%。全年財測年內第三度上調，營收 4.4–4.6B、non-GAAP EPS 3.10–3.40；2026-07-28 給的 3.9–4.2B 已兌現並超越，管理層財測可信度高。產業位於擴張期：AI 資料中心用電集中且急迫，燃氣渦輪大廠訂單排到 2029–30，燃料電池 55–90 天交期成為替代方案（二手說法）。供需持久度：2028 年前屬結構性，但供給可逆性中等，渦輪產能釋出後時間優勢會收窄，這一點餵給空方機率。單點依賴必答：2026 Q2 單一客戶約占營收 73%、Q1 約 50%，FY2025 前三大 43%／13%／12%，第一大為經 Brookfield 合資的關係人；多數終端客戶付電費，設備由融資方買斷持有。這是集中度風險，不是護城河證據。議價權：下游最大客戶集中度遠超 40%，上游鈧與台灣元件為瓶頸。","moat":"機制：固態氧化物燃料電池不經燃燒，空氣許可較易取得；模組化可分批上電、交期以月計；Fremont 年產能 2026 年底達 2 GW、廠房可擴至約 5 GW，人力不隨產能等比增加，形成成本曲線領先。可證方向：同業 ROIC 事實表未涵蓋，改用利潤率 spread。BE TTM 營益率 11.2%，高於 GEV 4.4%、CMI 11.1%；FCEL、PLUG 毛利為負，同類燃料電池對手無力抗衡。Q3 產品毛利率 38.4%，全年毛利率指引 34%（2025 年 30%、年初指引 32%）；2026-07-28 CEO 稱資料中心市占率在「90 高段」，Nebius 取消燃氣機組改選 Bloom。執行力擴大、定價力穩定偏擴大，判為向上。產業態勢屬雙向拉鋸：結構轉好（渦輪排到 2029–30、現場發電占比預期上升、維吉尼亞州長點名非燃燒燃料電池）對上競爭者進入（FuelCell、Doosan HyAxiom）與地方許可阻力（Santa Clara、新墨西哥、俄亥俄）。當期 ROIC 無法計算：投入資本與 D&A 事實表未涵蓋。","growth":"成長主要靠量（交付 GW 數），其次是價與成本（產品毛利擴張），沒有併購與回購。共識 non-GAAP EPS FY2026 3.25、FY2027 5.24、FY2028 8.19（Koyfin 2026-10-24 快照，家數未載），FY2026→FY2028 年化約 58.7%。同期營收共識據第三方約 65 億、98 億（單位未載明），營收年化約 47%，EPS 成長比營收快約 12pp。缺口主要歸因營業利益率擴張（GAAP 營益率 FY2025 3.6% → Q3 non-GAAP 23.1%），無回購、無收購。內生天花板因投入資本缺而無法算出，共識是否在天花板內無法證明，保守視為超出。衰退信號亮 2 個：EPS 成長顯著快於營收、FCF/NI 2026 年明顯低於 0.75；長期成長性與價值陷阱風險都落在中間。第三方模型與共識對 2027–28 營收相差約 2 倍，公司未給 2027 指引。","governance":"現金去向：前三季資本支出 231 百萬美元，是 2025 全年的 4 倍，投在 Fremont 與 Newark 機台；營運資金因存貨、合約資產、應收增加而吸收現金；無回購與股息。SBC 單季 60.1 百萬美元，占營收 4.9%、占 non-GAAP 營業利益 21%；股數變化事實表未涵蓋，淨稀釋率無法計算。2026-07-28 CFO 稱營業利益增額 100% 轉為營運現金流、基準 3.75 億美元以上，Q3 營業現金流卻是 −27 百萬美元，承諾與實績落差列入反證。多數客戶經融資方付款，Brookfield 承諾 250 億美元、IDF 26 億美元；專案若延後，融資方仍須收貨（CFO 說法），降低交付風險，但也讓收款節奏取決於融資方。","valuation":"FY1 本益比 59.5 倍（3.25 美元），FY2 36.9 倍（5.24 美元），FY3 23.6 倍（8.19 美元）。PEG 以 FY1 本益比除以 FY2026→FY2028 共識 EPS 年化 58.7%，約 1.0，落在合理區；以 FY2 計約 0.6。FY1 共識近三個月上修 19.9%，股價 26 週 −16%，本益比壓縮主要來自股價下跌加 EPS 上修。基本情境：FY2031E EPS 11.4×24 倍≈274 美元，五年 +41.5%，年化約 7%，低於 8%；機率加權終值約 274 美元，與基本情境接近。12 個月：FY2028E 基本 7.4×28 倍≈207 美元，約 +7%。同業前瞻倍數事實表未涵蓋，終端倍數無法附同業現值對照。賣方目標價全距 10–350 美元，分歧極大，自身報酬信心下調。五年分位事實表未涵蓋。","premortem":"空方最強的三點：Q3 自由現金流 −181 百萬美元，與上一季 CFO 承諾相反；單一客戶占 Q2 營收約 73%；鈧供應被指控依賴中國，有集體訴訟在身，且中國出口管制預計 11-10 恢復。三者都在一年內有數據可驗證（Q4 財報、FY2026 10-K）。股價 26 週 −16%、RSI 33，動能不過熱；高波動歷史意味深回撤要先有心理準備。"},"plain":{"six":{"how_it_makes_money":"賣現場發電設備（產品占 Q3 營收 87%）給資料中心與工商業客戶，賺的是電網接不上電、燃氣渦輪排不到貨的時間差。錢卡在「上電速度＋空氣許可」這一節點；Q3 non-GAAP 毛利率 34.5%、營益率 23.1%","moat":"護城河方向向上：規模化讓產品毛利率持續擴張，定價據 CFO 稱仍強，新進者規模只有數十 MW。但機制建立在電網與渦輪短缺的時間窗口上，持續期是最大問號","growth":"五年後跑道仍寬：資料中心之外已有具名的第二曲線（AEP 為 Google 建 700MW 碳捕捉案、美國陸軍基地、公用事業表前配置），現場發電占整體用電比例仍低","capital":"自籌擴產型：無回購、無股息、無併購，現金全數投入產能與營運資金；Q3 自由現金流 −181 百萬美元，前三季 +42 百萬美元，期末現金 25 億美元","valuation":"現價 193.3 美元要求 EPS 照共識在 FY2028 前成長到 8.19 美元、之後仍有雙位數成長，FY2 本益比 36.9 倍才划算。成長我大致相信，但現金轉換與客戶集中尚未驗證，基本情境五年年化約 7%，偏貴不追","how_wrong":"價值陷阱風險中：最可能看錯在「營收長得出來、現金收不回來」，以及最大客戶一旦延後，單季營收會斷崖"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等 2027-02 Q4 財報確認單季營業現金流轉正、全年自由現金流為正再加碼；價格已到前份加碼區不構成理由","qc48_result":"fail","qc48_note":"Bloom 的成長依據有營收實績，但 Bull 路徑沒有量價骨架。第二曲線和滲透率缺少一手來源，同類高估值能源設備股過去 5 年的報酬遠低於 Bull 隱含的每年 23%，而判斷物沒有說明本案為何不同，所以 Bull 依據目前不成立。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":193.3,"week26_return_pct":-16.38,"consensus_rev_3m_pct":19.93,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母採 non-GAAP EPS；Q3 GAAP EPS 0.78 對 non-GAAP 0.94，GAAP 口徑倍數約高兩成，SBC 屬經常性成本但不是本次爭點"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"中國暫停的稀土出口管制預計 11-10 恢復，牽動鈧供應","impact":"中","watch":"公司是否揭露鈧庫存或替代來源、交付是否延誤"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"Fremont 年產能擴至 2 GW 預計年底完成","impact":"中","watch":"Q4 法說是否確認完工與良率"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報、FY2027 全年財測與積壓訂單數字","impact":"高","watch":"營業現金流、FY2027 營收年增是否 ≥30%、最大客戶占比"},{"date":null,"date_precision":null,"type":"other","event":"Nevins 證券集體訴訟駁回動議裁定","impact":"低","watch":"是否進入證據開示、有無 SEC 介入"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,420B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河方向向上，但建立在電網與渦輪短缺的窗口上。</p>
<ul class="pts">
<li>護城河機制有三層：固態氧化物燃料電池不燃燒，空氣許可較容易取得。模組化設計可分批上電，交期以月計。Fremont 年產能 2026 年底達 2 GW，廠房可擴至約 5 GW，人力不隨產能等比增加，形成成本曲線領先。這三層合起來，構成對燃氣方案的速度與許可優勢。</li>
<li>可證的方向來自利潤率對照。同業投入資本事實表沒有涵蓋，所以改用利潤率比較。BE 的 TTM 營益率 11.2%，高於 GEV 的 4.4%，與 CMI 的 11.1% 相當，低於 VRT 的 19.4%。FCEL 營益率 −88%、PLUG 毛利率 −19%，同類燃料電池對手財務上無力在大型固定式發電與 Bloom 競爭。</li>
<li>執行力與定價力都在擴大。Q3 產品毛利率 38.4%，全年毛利率指引 34%，2025 年為 30%，年初指引只有 32%。CFO 稱定價仍強、降本持續，CEO 稱資料中心市占率在「90 高段」，但這是公司自述，沒有第三方數字。執行力評 8、定價力評 7，等級判為 B，趨勢向上。</li>
<li>威脅清單有三項，都屬點對點，尚未形成面的攻擊。FuelCell 簽下德州首份 75MW 資料中心容量預留協議，技術不同，毛利率為負。Doosan 的美國子公司 HyAxiom 以磷酸型燃料電池首度進入美國資料中心。兩者機率各取 20%。</li>
<li>最大的威脅是時間。燃氣渦輪產能 2029–30 釋出，加上電池儲能與其他現場發電技術追上，時間溢價會收窄。這不是新的攻擊，而是窗口期自然結束，屬破壞性競爭，機率取 35%。CEO 自己也承認各種快速供電技術都有空間。</li>
<li>報酬持續期要看四個檢查點，每個都只給到中間級。需求是真的，但急迫性來自電網與渦輪短缺，2029 年後是否持久未證。替代以單一園區為決策單位，轉換成本只在既有站點。價值鏈分配上，最大客戶占營收七成以上，買方議價力強。社會容忍度上，Santa Clara、新墨西哥 Project Jupiter、俄亥俄 Hilliard 的許可阻力，是實際上限。</li>
</ul>
<h3>§5 二維評分與 Moat-to-Numbers</h3>
<!-- E5 -->
<h3>§5.F 對手財務深度對照</h3>
<!-- E6 -->
<h3>§5.R 報酬持續期檢核</h3>
<!-- E7 -->
</section>

```