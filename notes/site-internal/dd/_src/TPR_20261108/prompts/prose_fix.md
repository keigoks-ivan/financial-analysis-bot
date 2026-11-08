你是 stock-analyst v20 的**散文層（prose）agent**，標的 TPR（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：TPR　日期：2026-11-08　archetype：None　前份裁決：2026-10-05　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1531B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（374B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（799B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1282B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1020B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（373B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（968B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2122B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3906B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2509B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1531           3828-5469      5 條（2–6 內）  
s3                  8000         374           5338-7626      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3101          8329-11899      5 條（2–6 內）  
s6                 11000         373          7439-10627      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         968           1772-2532      5 條（2–6 內）  
s10                 5000        2122           2015-2878      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2509           2000-2491      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4109B；至少需散文≈40.89KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−55%
−54%
−50%
−42%
−40
−40%
0
0%
0.06
0.12
0.15%
0.15
0.27
0.35
0.45
0.5%
0.75
0.82
1
1.02
1.1
1.19
1.2
1.3
1.32
1.39
1.4
1.6
1.68
1.7
1.74
1.75
1.8%
1.8
1.81
1.85
1.9
2
2.0
02
2%
2.10
2.1
2.3
2.4
2.5
2.62
03
3
3%
3.02
3.05
3.5
4
4%
5
05
5%
5.7%
6
6%
6.25%
6.4
6.5%
6.6
6.7
6.8%
6.99
7
07
7.0
7%
7.06
7.27
7.5
7.6
7.7%
7.80
7.82
7.90
7.9%
7.96
8%
08
8
8.25
8.30
8.3
8.35
8.6
8.89
9
9.2
9.3%
9.3
9.5
9.9
10%
10
10.08
10.2
10.3
10.3%
10.7
11
11.25
11.4
12
12%
12.3
12.4%
12.5
12.6%
13
13.1
13.88%
14
14.9
14.94
15
15.0
15%
15.28
15.3
16.0
16%
16
16.6
16.68
16.97
17
17%
17.6%
17.7%
18
18%
18.1
19
19%
20%
20
22
22%
23%
23
23.2%
24%
24
24.2%
25
25%
26
26.5%
27
28.9%
30
30%
34.36%
34.7
35.6%
36%
40
40%
42
44.9%
45
45%
49
50%
52
53
58%
60%
61
65.77
69.1
70
70.4
70.47
70.8%
73
73.3%
74
75%
75.8%
76
76%
77
77.9%
78%
78.3%
78.6%
78.7%
80.0
80
85.5
86%
87%
88
90
100%
100
110
115
118.12
120
130
132.8
150
150%
165
166
170
174
200
211
220
241.2
250
260
268.2
500
525
1100
2024
2025
2026
2027
5600
20261108
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
{"meta":{"ticker":"TPR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Tapestry, Inc."},"oneliner":"Coach 一個品牌撐起全部獲利：Q1 固定匯率成長 16%，全年 EPS 財測上調到 8.25–8.35 美元；現價約 16 倍，基準情境年報酬約 8%，關鍵在北美中個位數成長與 78% 毛利率能否守住。","thesis":{"H":[{"id":"H1","text":"Coach 在 FY26 年增 24% 的高基期上，仍能維持高個位數以上成長，而且單價與件數同時成長。","2y":"FY28 Coach 營收 ≥ 80 億美元","5y":"FY31 Coach 營收 ≥ 100 億美元","10y":null,"threshold":"Coach 固定匯率年增 ≥ +7%，手袋件數年增 ≥ 0","source":"每季法說與新聞稿、10-K 分部營收","drift_rule":"兩年維度：低於門檻 5% 以上連 2 季算削弱，低於 10% 以上連 3 季算反轉；五年維度：連 4 季偏離 5% 算削弱，連 6 季偏離 10% 算反轉。"},{"id":"H2","text":"過去三年的利益率提升大部分是結構性的，來自促銷減少、單價提升與國際組合，不會退回 FY23 到 FY25 的水準。","2y":null,"5y":"FY31 毛利率 ≥ 76%，營業利益率 ≥ 23%","10y":null,"threshold":"毛利率 ≥ 76%，營業利益率 ≥ 23%","source":"10-Q 與 10-K、法說毛利率拆解","drift_rule":"連 4 季偏離 5% 算削弱，連 6 季偏離 10% 算反轉。"},{"id":"H3","text":"自由現金流持續轉成每股價值，回購不需要靠持續舉債，也不被大型併購打斷。","2y":null,"5y":"FY27 到 FY31 累計 FCF ≥ 90 億美元，稀釋股數降到 1.75 億股以下，總槓桿低於 2.5 倍","10y":null,"threshold":"年度 FCF ≥ 16 億美元，總槓桿 ≤ 2.0 倍","source":"現金流量表與每季法說","drift_rule":"連 4 季偏離 5% 算削弱，連 6 季偏離 10% 算反轉。"}],"R":[{"id":"R1","text":"Coach 北美在高基期下降溫，FY27 財測已假設中個位數，一旦低於這個水準，上調的財測就站不住。","h_ref":"H1","clock":"⚡","threshold":"北美 Coach 固定匯率年增 < +3% 連 2 季","evidence_refs":["competitive_share_entrants#2"]},{"id":"R2","text":"毛利率順風反轉：Q1 擴張 220 個基點裡有 70 個來自關稅，手袋生產集中越南、柬埔寨、菲律賓約七成，FY26 關稅成本曾估約 1.6 億美元，國際業務約占 40% 並受美中關係影響。","h_ref":"H2","clock":"🔥","threshold":"毛利率年減 ≥ 100 個基點連 2 季","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R3","text":"Kate Spade 續跌且虧損擴大，消耗管理層與資本；全年財測隱含下半年收斂，尚未驗證。","h_ref":"H1","clock":"🔥","threshold":"FY27 年減超過 10%，或 FY28 上半年仍年減","evidence_refs":["end_markets#1"]},{"id":"R4","text":"重回併購路線：FTC 擋下 Capri 後，同層級整合受限，未來交易可能轉向較不熟悉的領域，傷害資本報酬。","h_ref":"H3","clock":"🐢","threshold":"宣布總價超過市值 5% 的併購，且 Kate Spade 尚未恢復成長","evidence_refs":["regulatory_antitrust#1"]},{"id":"R5","text":"回購長期超過自由現金流，EPS 成長靠舉債支撐。","h_ref":"H3","clock":"🐢","threshold":"股東回饋 ÷ 調整後 FCF 連 2 年 > 1.2 倍，或總槓桿 > 2.0 倍","evidence_refs":[]},{"id":"R6","text":"Capri 併購終止相關的兩宗證券集體訴訟仍未決，金額事實表未涵蓋，不涉及核心業務。","h_ref":null,"clock":"🐢","threshold":"集體認證獲准且和解金額超過約 1.7 億美元","evidence_refs":["major_events#0","lawsuit_class_action#0"]}],"single_thing":{"description":"Coach 北美固定匯率營收連續兩季年減。","why_fatal":"北美是最大獲利來源，這件事同時打到營收與毛利率。以 FY27 營收中點 85.5 億美元、18% 稅率、2 億股算，毛利率每少 1 個百分點，EPS 少約 0.35 美元；由財測約 78.6% 退回 FY24 的 73.3%，約少 1.9 美元，相當於 FY27 EPS 的 22%。","if_happens":"清倉。空頭路徑改為基準情境，五年目標約 70 美元，完成重新判斷前不買回。","how_monitor":"每季法說的北美 Coach 固定匯率年增、促銷天數與手袋件數；Q1 為 +7%，Q2 財測中個位數。","probability":"12–24 個月約 20%，依據是 FY26 的高基期與北美只有中個位數財測；Coach 品牌執行長 2026-11-05 說 23 季有 22 季成長，是反向證據。"}},"appendix_a":{"growth_durability":6,"quality_score":7.5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.94,"peg_fy2":1.19,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":7.06,"FY2027E":7.96,"FY2028E":8.89,"FY2029E":10.08},"fy_end_month":6,"eps_basis":"Non-GAAP，會計年度 6 月底結束。基期由 FY27 財測 8.25–8.35 美元對應年增 17–18% 反推約 7.06 美元；FY2027E 到 FY2029E 為 2026-11-07 共識快照，仍是財測上調前數字。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高毛利、直營為主、自由現金流大多拿去回購"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高：Coach 品牌執行長 2026-08-13 說這行沒有進入門檻，財務長同場說規模門檻在升高；需求靠品牌熱度，降溫時會反轉。","bargaining":{"up":"手袋代工集中在越南、柬埔寨、菲律賓約七成，事實表沒有單一供應商占比。","down":"直營約 87%，批發約 12%，沒有單一客戶超過 10%，下游議價力低。","geo":"美國進口關稅與美中關係是主要外部變數，國際業務約占淨銷售 40%。"},"profit_pool_dir":"五年營業利益池流向事實表未涵蓋，只有二手報導稱 Tapestry 從歐洲品牌手中取得份額。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與滲透率，管理層只說市場很大而未給數字，本次不自行估算。"}},"moat":{"mechanism":"200–500 美元價位帶的品牌熱度，加上直營約 87% 的價格控制與約 10 億美元行銷量體。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"定價力擴大：AUR 與件數同時成長，北美促銷減少。執行力持平：Coach 獲客強，但 Kate Spade 續跌 10%，2026-08-13 執行長也承認其知名度未改善。兩者合併為持平，且 CFO 說未來定價是通膨再加一點，目前 AUR 增速不宜外推。","peer_na_reason":"同業表不能用於利差判斷：MC 毛利率與 CFR 缺毛利率都不像精品公司，疑似代號對到同名美股，本包無法核實；RMS、KER 無資料，也沒有 ROIC 欄。","threats":[{"level":"🟡","text":"Michael Kors 仍是主要對手，Polene、Jacquemus 靠社群與稀缺性吸引年輕客；來源為彙整文章，沒有一手份額。","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"二手精品成長約為一手三倍，Gen Z 手袋二手比例高；數字來自聚合文章，未回溯原始報告，但方向與年輕客群重疊。","p":"25%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"AI 購物助理可能改變數位探索與比價，10-K 已列風險因素；門店 Q1 成長低雙位數，高於數位中個位數，附著點仍在自有門店。","p":"15%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"Bernstein 分析師 2026-11-05 問到歐洲品牌下探單價、縮小價差；Coach 品牌執行長回答價差仍大，但沒有給量化數字。","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率，周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"手袋是想要而非需要，延後購買代價低；正面代理是 FY26 新客 1100 萬人，且 2026-08-13 執行長說新客留存率位居客戶檔案最高之列。"},{"item":"決策層級","level":"🟡","text":"替代發生在單一款式的購買決定，轉換成本接近零；提價後件數仍成長是目前最好的反證，但 200 美元以下是刻意縮減。"},{"item":"價值鏈分配","level":"🟢","text":"直營約 87%、沒有單一客戶超過 10%、毛利率 78% 以上，品牌端拿走鏈上大部分利潤，代工端分散在多國。"},{"item":"社會容忍度","level":"🟢","text":"非必需品，沒有社會對漲價的天花板，也不依賴監管授權；關稅屬成本面政策風險，放在風險項處理。"}],"roiic":"下限約 58%：FY27 稅後營業利益增量約 1.74 億美元 ÷ 資本支出與雲端費用約 3 億美元","reinvest_rate":"上限約 18%：3 億美元 ÷ FY27 稅後營業利益約 16.97 億美元，未扣折舊，也未含營運資金","endo_ceiling":10.3,"formula_note":"FY27 營收中點 85.5 億美元 × 營益率約 24.2% × （1−18%）得約 16.97 億；FY26 營益率以財測增幅約 100 個基點回推約 23.2%。58% × 17.7% 約 10.3%。折舊事實表未涵蓋，所以增量報酬是下限、再投資率是上限，兩者相乘等於 FY27 稅後營業利益成長率。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","TPR":78.31,"RMS":null,"MC":34.36,"CFR":null,"KER":null,"unit":"%"},{"metric":"營業利益率","TPR":24.53,"RMS":null,"MC":18.4,"CFR":null,"KER":null,"unit":"%"},{"metric":"FCF 利潤率","TPR":22.95,"RMS":null,"MC":27.54,"CFR":24.77,"KER":null,"unit":"%"}],"competitors":[{"name":"RMS","gm":null,"om":null,"fcf_margin":null,"strategy_note":"事實表無財務資料，策略也未涵蓋，只能歸在管理層所說價差明顯的歐洲精品一側。"},{"name":"MC","gm":34.36,"om":18.4,"fcf_margin":27.54,"strategy_note":"表內毛利率 34.36% 不像精品集團，疑似代號對錯，不採用；二手報導只稱 LVMH 時尚皮件表現分歧。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CFR","gm":null,"om":null,"fcf_margin":24.77,"strategy_note":"表內只有 FCF 利潤率、沒有毛利率，疑似代號對錯，不作同業比較。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"KER","gm":null,"om":null,"fcf_margin":null,"strategy_note":"事實表無財務資料，無法判讀。"}]},"growth":{"driver_mix":"FY27 價與量都有，AUR 貢獻大於件數；EPS 另靠回購與利益率擴張，沒有併購。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 10.3%，來自 FY27 財測推算的增量報酬下限 58% 乘再投資率上限約 18%；共識約 12.6% 高出約 2.3 個百分點，歸因淨回購與利益率擴張。","segments":[{"item":"Coach","value":"FY26 營收 69.1 億美元，年增 24%；Q1 FY27 固定匯率 +16%；FY27 財測高個位數成長，營益率約 36%。"},{"item":"Kate Spade","value":"FY26 營收 10.7 億美元，年減 10%；Q1 FY27 年減 10%；FY27 財測高個位數衰退並小額營業虧損。"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"Q1 毛利率年增 220 個基點。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"沒有縮減證據，但第三方份額數字缺。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"Q1 件數低個位數成長；200 美元以下是刻意縮減。"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY27 財測 EPS 年增 17–18%，營收固定匯率 6–7%；三年共識也高出約 6 個百分點。"},{"signal":"FCF 對淨利低於 0.75 連兩年","lit":false,"note":"FY26 為 1.19 倍，FY27 財測推算約 1.02 倍。"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"推算不到營收 2%。"},{"signal":"TAM 萎縮或被替代","lit":false,"note":"二手市場成長快，列為威脅，沒有 TAM 萎縮證據。"},{"signal":"產業估值倍數系統性下移","lit":null,"note":"事實表未涵蓋。"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"總資本支出與雲端費用約 3 億美元，只占 FCF 約 18%。"},{"signal":"停止投資且營收下滑","lit":false,"note":"FY27 資本支出增加，營收成長。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月沒有併購類重大申報；近三年現金去向分項事實表未涵蓋，無法展開。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月沒有併購，Capri 案 2024-11 終止；過往收購投入金額與增量報酬事實表未涵蓋，Kate Spade 轉為營業虧損是負面旁證，但算不出報酬率。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"以財測中點算盈餘殖利率約 6.25%（8.30 ÷ 132.8）；10 年期公債殖利率與回購均價事實表未涵蓋，無法判定。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數由 FY26 約 2.10 億（淨利 15.28 億 ÷ EPS 7.27）降到 FY27 財測約 2 億，淨稀釋為負；SBC 約 1.3 億美元，約占市值 0.5%。","grade":"過"}]},"valuation":{"basis":"前瞻本益比，以 FY27 公司財測中點 8.30 美元為分母，共識快照 7.96 美元為對照。","tier":"輕奢品牌，同業現值倍數事實表未涵蓋","peers":{"expanded":false,"reason":"同業表的 MC、CFR 數字不像精品公司，RMS、KER 無資料，且沒有倍數欄，不能當估值錨。"},"fwd_pe":16.68,"peg":1.32,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 16.0 到 16.68 倍、PEG 1.32 落在合理帶，基準年報酬約 8% 屬中段偏低。股價較前份高 12.4%，財測中點高 5.7%，差額由倍數吸收，結論維持中性。","upside_short_pct":11,"upside_mid_pct":19},"trap_analysis":{"verdict":"🟡","label":"品牌熱度退潮與高點利益率"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Coach 成長由 FY26 的 24% 放緩到 Q2 財測高個位數，手袋 AUR 成長由中十位數降到低雙位數；Coach 品牌執行長自己說這行沒有進入門檻；Kate Spade 在同一平台上續跌 10%。","assumption":"Coach 的年輕客群熱度能延續到 FY31，而不是一段流行週期。","consequence":"五年後虧 50% 最可能的故事：北美轉負，促銷回來，毛利率退回 73–75%，營益率回到 19%，EPS 約 6.4 美元，11 倍約 70 美元。","ruling":"採納，空頭機率維持 30%，與唯一致命點重疊，監測同一指標。反面證據是 23 季有 22 季成長，所以不把機率再往上加。","watch":"北美 Coach 固定匯率年增、手袋件數與 AUR、促銷天數。","evidence_refs":["competitive_share_entrants#2","end_markets#1"],"fact_refs":["f_peer_tpr_gross_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"FY27 股東回饋 20 億美元高於 FCF 接近 17 億美元，差額靠現金與商業本票；EPS 財測上調 0.45 美元，FCF 財測沒有動；行銷占比持續上升，Q2 SG&A 預計增加約 120 個基點。FTC 勝訴也可能限制同層級併購，未來併購只能往較差的選項走。","assumption":"每股盈餘成長會等比例轉成每股自由現金流。","consequence":"Coach 繼續成長，但 EPS 靠縮股與高點利益率撐住，每股現金沒有同步成長，終端倍數會低於 15 倍。","ruling":"部分採納。總槓桿 1.1 倍還有空間，FY27 的超額回饋不算問題；連兩年超過 1.2 倍才算資本配置轉差。","watch":"股東回饋 ÷ 調整後 FCF、總槓桿、行銷占營收比。","evidence_refs":["regulatory_antitrust#1"],"fact_refs":["f_kpi3","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"現在就賣的最強論證：毛利率由 FY23 的 70.8% 升到 78% 以上，營業利益率由 17.6% 升到 24% 以上，P/S 與 EV/S 都在年度端點約 76–78% 分位；股價一個月漲 12.4%，RSI 70.47；下半年營收只剩中個位數成長。","assumption":"16 倍本益比適用於尚未見頂的利益率。","consequence":"基本面沒破，只要本益比回到 FY28 EPS 的 12–13 倍，股價就在 110–120 美元，跌 10–17%。","ruling":"部分採納。26 週報酬僅 0.15%、股價貼近 52 週均線，稱不上整段過熱；但基準年報酬只有約 8%，容錯空間薄，所以分批而不是一次加足。","watch":"前瞻本益比是否超過 FY28 EPS 的 18 倍、毛利率年變動。","evidence_refs":[],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_rsi14","f_week26_return_pct"]}],"max_dd":{"lo":-55,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 118.12 → 本次 132.8（+12.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=118.12","side_b":"本次 price_at_dd=132.8","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 118.12 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 118.12 美元：Bull 價 241.2、Bear 價 74，五年期望值 +35.6%，基準年化 7.9%，不對稱比 2.3","side_b":"本次情境、股價仍用 118.12 美元：Bull 價 268.2、Bear 價 70.4，五年期望值 +44.9%，基準年化 9.3%，不對稱比 2.62","ruling":"先換情境、股價不動：五年期望值多 9.3 個百分點，基準年化多 1.4 個百分點。不對稱比由 2.3 變為 2.62。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 118.12 美元：五年期望值 +44.9%，基準年化 9.3%，不對稱比 2.62","side_b":"本次情境、股價 132.8 美元：五年期望值 +28.9%，基準年化 6.8%，不對稱比 1.81","ruling":"再換股價、情境不動：起點價上漲 12.4%，五年期望值少 16.0 個百分點，基準年化少 2.5 個百分點，不對稱比由 2.62 降到 1.81。合計五年期望值比前份少 6.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"評級與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份股價 118.12 美元，評級 B，估值中性。","side_b":"本次股價 132.8 美元，評級 B，估值中性。","ruling":"股價漲 12.4%，財測中點漲 5.7%，差額由本益比從約 15.0 倍升到 16.0 倍吸收，兩項結論都不變。","evidence_level":"事實表與法說","settle_metric":"前瞻本益比","if_then":[],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"情境機率與回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份多頭 25%、空頭 30%，最大回撤 −55%。","side_b":"本次多頭 25%、基準 45%、空頭 30%，最大回撤 −40% 到 −55%。","ruling":"機率不變。股價較高使同一空頭價位的跌幅擴大，EPS 財測上調則抵銷一部分，回撤改用範圍表達。","evidence_level":"情境推算","settle_metric":"空頭路徑的 EPS 與本益比","if_then":[],"evidence_refs":[]},{"axis":"護城河、跑道與陷阱風險","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap"],"side_a":"前份：護城河方向持平，五年後跑道中等，價值陷阱風險中等。","side_b":"本次：三項都不變。","ruling":"Q1 的新證據偏正面，Coach 固定匯率 +16%、件數與 AUR 同增，但一季不足以把品牌熱度升格為護城河擴大，滲透率與第三方份額仍缺。","evidence_level":"法說","settle_metric":"第三方份額與滲透率，事實表未涵蓋","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"公司類型與循環位置","cause":"新證據","prior_field":["archetype","cycle_position"],"side_a":"前份：品質複利成長，未標循環位置。","side_b":"本次相同。","ruling":"Q1 逐字稿沒有改變公司類型的證據；品牌熱度的週期性放在空頭情境處理，不改標循環股。","evidence_level":"法說","settle_metric":"毛利率與北美成長是否同步轉弱","if_then":[],"evidence_refs":[]},{"axis":"裁決與角色","cause":"新證據","prior_field":[],"side_a":"前份裁決進場，角色衛星。","side_b":"本次基本面輸入沒有轉弱，裁決與角色以本次輸入算出的結果為準。","ruling":"Q1 超越財測且前份加碼條件成立，沒有下修裁決的基本面理由。","evidence_level":"法說","settle_metric":"Q2 FY27 Coach 成長","if_then":[],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"加碼條件更新","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼條件：Q1 FY27 法說（約 2026-11）Coach 固定匯率成長 ≥ +10% 且手袋件數年增 ≥ 0，兩者同時成立","side_b":"加碼條件：Q2 FY27 法說（約 2027-02）Coach 固定匯率成長 ≥ +10% 且北美 Coach ≥ +5%，兩者同時成立","ruling":"前份加碼條件已於 2026-11-05 法說成立：Coach 固定匯率 +16%，手袋件數低個位數成長。舊條件已用掉；新條件加上北美，因為北美是最大獲利來源，且 Q2 財測 Coach 只有高個位數。","evidence_level":"法說原話","settle_metric":"Coach 固定匯率年增與北美年增","if_then":["若 Q2 兩項達標，則加碼剩下一半；","若 Coach 達標但北美低於 +5%，則停止加碼，等 Q3 法說。"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"Single Thing 與清倉、減碼門檻首次建立","cause":"方法變動","prior_field":["single_thing","kill_metrics"],"side_a":"前份摘要此欄為空，無原文可引。","side_b":"Coach 北美固定匯率營收連續兩季年減。","ruling":"前份摘要沒有留存唯一致命點與清倉指標，本次依敏感度重新建立；北美同時影響營收與毛利率，是最大單一敏感項，連兩季年減即清倉，毛利率連兩季年減 100 個基點以上則減碼。","evidence_level":"情境推算","settle_metric":"北美 Coach 固定匯率年增","if_then":[],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：Michael Kors 仍是主要對手，Polene、Jacquemus 搶年輕客，二手平台成長快，歐洲品牌可能下探。","side_b":"結構：Coach 在 18–27 歲品牌偏好排名第一，直營約 87%；關稅假設由中 20% 降到低至中 20%。","ruling":"雙向拉鋸。品牌與通路結構在轉好，但競爭證據多為二手彙整，關稅屬政策變數，沒有一軸足以單向定調。","evidence_level":"二手彙整與法說","settle_metric":"第三方手袋份額，事實表未涵蓋","if_then":[],"evidence_refs":["competitive_share_entrants#2","end_markets#3","substitute_technology#1"]},{"axis":"財測上調的品質","cause":null,"prior_field":null,"side_a":"2026-11-05 財務長：全年 EPS 由 7.80–7.90 美元上調到 8.25–8.35 美元。","side_b":"同場拆解：中點上調 0.45 美元，0.27 是 Q1 已實現，0.12 來自線下項目，主要是多回購，只剩約 0.06 美元是後三季營運上修；Q2 財測 3.05 美元僅略高於共識 3.02 美元。","ruling":"可調和。上調是真的，但對後三季的新資訊很少，不能外推成成長加速，基準情境的 FY27 只取財測上緣。","evidence_level":"法說原話","settle_metric":"Q2 FY27 EPS 與營收","if_then":[],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"EPS 上調但現金流財測不動","cause":null,"prior_field":null,"side_a":"2026-08-13 財務長：FY27 調整後 FCF 接近 17 億美元。","side_b":"2026-11-05 財務長：EPS 上調、回購多 3.5 億美元，FCF 仍接近 17 億美元，Q1 僅 5600 萬美元。","ruling":"可調和，但未證。可能是保守或存貨投資，暫不扣分；若全年 FCF 低於 16 億美元且管理層歸因一次性，視為解釋不成立。","evidence_level":"法說原話","settle_metric":"FY27 調整後 FCF","if_then":["若 FY27 FCF 低於 16 億美元，則停止加碼。"],"evidence_refs":[]},{"axis":"毛利率擴張的來源","cause":null,"prior_field":null,"side_a":"2026-11-05 財務長：Q1 毛利率年增 220 個基點，營運 130、關稅 70、匯率 20。","side_b":"2026-08-13 財務長原估全年只增約 30 個基點，關稅假設中 20%；11-05 上調到約 80 個基點，關稅假設降為低至中 20%。","ruling":"約六成來自營運，較持久；三成多是關稅，一成是匯率，屬外部順風。外部順風部分放進空頭情境，空頭營益率回到 19%。","evidence_level":"法說原話","settle_metric":"扣除關稅與匯率後的毛利率年變動","if_then":[],"evidence_refs":["reg_tariff_export#0"]},{"axis":"進入門檻的說法","cause":null,"prior_field":null,"side_a":"2026-08-13 Coach 品牌執行長：這行沒有進入門檻。","side_b":"2026-08-13 財務長：規模門檻正在提高。","ruling":"可調和。門檻不在進入而在放大，護城河給中上評等，不給最高等級；被問最擔心哪個對手時未點名，競爭證據只能靠外部。","evidence_level":"法說原話","settle_metric":"行銷占營收比與新客數","if_then":[],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"Kate Spade 的回升假設","cause":null,"prior_field":null,"side_a":"2026-08-13 執行長：營收進展比計畫慢，整體知名度未改善，全年財測高個位數衰退。","side_b":"2026-11-05 財務長：Q1 年減 10%，Q2 財測低雙位數衰退，全年仍維持高個位數衰退，等於下半年要明顯收斂。","ruling":"未證，監測。品牌已小額虧損，對獲利影響有限；但全年財測隱含下半年回升，若 Q3 仍年減 10% 以上，這項假設視為被推翻。","evidence_level":"法說原話","settle_metric":"Q3 FY27 Kate Spade 年增率","if_then":["若 Q3 年減 10% 以上，則停止加碼。"],"evidence_refs":["end_markets#1"]},{"axis":"共識上修幅度","cause":null,"prior_field":null,"side_a":"事實表：FY1 共識近三個月上修 13.88%，由 6.99 美元到 7.96 美元。","side_b":"RTTNews 記錄 2026-08-13 的 FY27 共識為 7.82 美元；6.99 美元差距太大，不像同一財年，很可能是尚未換年的 FY26 共識，同一財年實際上修約 1.8%。","ruling":"採用同一財年口徑，13.88% 不作為動能依據。換年時點無法在本包核實。財測上調後共識快照仍低於財測下緣，後續應會上修。","evidence_level":"跨來源比對","settle_metric":"下一份共識快照的 FY27 EPS","if_then":[],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#0"]},{"axis":"現價是否加碼","cause":null,"prior_field":null,"side_a":"前份加碼條件已成立，基本面超過財測。","side_b":"RSI 70.47，股價一個月漲 12.4%，基準年報酬約 8%。","ruling":"先加計畫量的一半，原因是短線動能過熱；另一半綁 Q2 法說。Q4 件數持平曾被歸因於促銷天數減少，Q1 件數回到成長，這項解釋初步成立，再看一季。","evidence_level":"事實表與法說","settle_metric":"Q2 FY27 Coach 成長、RSI","if_then":["若股價在 Q2 法說前漲過 150 美元而證據未更新，則不追；","若股價跌到 115 美元以下且北美 Coach 仍 ≥ +3%，則分批反買。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q2 FY27 法說驗證 Coach 成長與北美動能，達標才加碼剩下一半。","type":"加碼","maps_to":"H1","metric":"Coach 固定匯率年增、北美 Coach 年增","threshold":"Coach ≥ +10% 且北美 ≥ +5%","action":"加碼","source_freq":"每季法說","date":"2027-02"},{"n":2,"text":"Coach 北美固定匯率營收連續兩季年減。","type":"Single Thing","maps_to":"Single Thing","metric":"北美 Coach 固定匯率年增","threshold":"連 2 季 < 0%","action":"清倉","source_freq":"每季法說","date":null},{"n":3,"text":"毛利率連兩季明顯年減，且管理層歸因關稅或促銷，視為吸收失敗。","type":"減碼","maps_to":"R2","metric":"毛利率年變動","threshold":"連 2 季年減 ≥ 100 個基點","action":"減碼","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"n":4,"text":"Kate Spade 的下半年回升沒有出現。","type":"風險","maps_to":"R3","metric":"Kate Spade 營收年增","threshold":"FY27 全年年減超過 10%，或 FY28 上半年仍年減","action":"停止加碼","source_freq":"每季法說","date":"2027-08","evidence_refs":["end_markets#1"]},{"n":5,"text":"Capri 併購相關的兩宗證券集體訴訟屬民事，不涉及營運收入，求償金額事實表未涵蓋，和解時點未知；公司 2025-07-14 聲請駁回，尚待裁定。","type":"風險","maps_to":"R6","metric":"法院裁定與和解金額","threshold":"集體認證獲准且和解金額超過約 1.7 億美元（一年 FCF 的 10%）","action":"減碼","source_freq":"10-Q 與 10-K 訴訟附註","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":6,"text":"股東回饋持續高於自由現金流，靠借債支撐回購。","type":"風險","maps_to":"R5","metric":"股東回饋 ÷ 調整後 FCF、總債務 ÷ 調整後 EBITDA","threshold":"連 2 年 > 1.2 倍，或槓桿 > 2.0 倍","action":"停止加碼","source_freq":"年度財報與法說","date":"2027-08"},{"n":7,"text":"股價回落但基本面無損，分批反買。","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤ 115 美元（約 FY28 EPS 9.2 美元的 12.5 倍）且北美 Coach ≥ +3%","action":"分批反買","source_freq":"每日收盤與每季法說","date":null},{"n":8,"text":"股價上漲而盈餘沒有同步上修，先減三分之一。","type":"減碼","maps_to":"H2","metric":"股價對 FY28 EPS 倍數","threshold":"≥ 18 倍（以 9.2 美元算約 166 美元）","action":"減碼","source_freq":"每日收盤與共識更新","date":null},{"n":9,"text":"Q2 FY27 法說後重看 Coach 基期效應與 Kate Spade 下半年回升假設。","type":"複審日期","maps_to":"H1","metric":"法說揭露","threshold":"Q2 法說公布","action":"停止加碼直到完成複審","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"北美 Coach 固定匯率年增","bear_threshold":"連 2 季 < 0%","window":"2 季","source":"每季法說","last_status":"ok"},{"metric":"毛利率年變動","bear_threshold":"連 2 季年減 ≥ 100 個基點","window":"2 季","source":"每季財報","last_status":"ok"},{"metric":"Coach 手袋件數與 AUR","bear_threshold":"同一季兩者都年減","window":"1 季","source":"每季法說","last_status":"ok"},{"metric":"存貨年增減營收年增","bear_threshold":"連 2 季高於 5 個百分點","window":"2 季","source":"每季財報與法說","last_status":"ok"},{"metric":"股東回饋 ÷ 調整後 FCF","bear_threshold":"連 2 年 > 1.2 倍","window":"2 年","source":"年度財報與法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=0.15, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"requires_critic":[],"rearm_trigger":"加碼條件：Q2 FY27 法說（約 2027-02）Coach 固定匯率成長 ≥ +10% 且北美 Coach ≥ +5%，兩者同時成立","exec_line":"前份加碼條件已成立，現價先加計畫量的一半，原因是短線動能過熱；另一半等 Q2 法說達標。Q2 前漲過 150 美元不追，跌到 115 美元以下且基本面無損才分批反買。"},"reasoning":{"industry":"FY26 營收 80.0 億美元，Coach 69.1 億占 86%、年增 24%，Kate Spade 10.7 億、年減 10%。約 87% 經由自營門店與數位賣出，批發約 12%，沒有單一客戶超過 10%。2026-11-05 法說的最新一季毛利率 78.7%，營業利益率超過 23%；事實表的最新一季指標仍停在 Q4 FY26，Q1 FY27 數字取自逐字稿。單點依賴就是 Coach：FY27 財測 Coach 營益率約 36%，Kate Spade 小額虧損，獲利幾乎全來自一個品牌。產業在擴張期，依據是二手彙整的全球精品 2026 年成長 3–5%、美國 4–6%，以及管理層引述美國假期季中個位數成長的產業預測。供需屬供給可逆性高，所以空頭機率不壓低。","moat":"機制是 200–500 美元價位帶的品牌熱度，加上約 87% 直營帶來的價格控制，以及約 10 億美元行銷量體形成的規模門檻。可比軸用單價與毛利：FY26 手袋 AUR 中十位數、件數低雙位數成長，Q1 AUR 低雙位數、件數低個位數；毛利率由 FY23 的 70.8% 升到最新 TTM 的 78.3%。定價力評擴大，執行力評持平，因為 Kate Spade 在同一平台上續跌 10%，代表優勢長在 Coach 品牌，不在集團平台。同業表不可用，第三方份額也缺，所以方向不上調。當期 ROIC 需要投入資本，事實表未涵蓋，下方只給增量推算。","growth":"FY27 成長拆解：價是手袋 AUR 低雙位數，量是件數低個位數與 Q1 新客 260 萬，回購使全年稀釋股數約 2 億股，較 FY26 約 2.1 億少約 5%，沒有併購。三年共識 EPS 年複合約 12.6%（基期 FY26 約 7.06 美元到 FY29 10.08 美元），分析師家數事實表未涵蓋。內生上界約 10.3%，超出的約 2.3 個百分點主要來自淨回購與 FY27 約 100 個基點的利益率擴張，不靠收購。Coach 要從 69.1 億美元到 100 億，五年需年增約 7.7%，可達，但北美財測只有中個位數，要靠國際。鞋類只貢獻 Q1 成長約 6%，還不算第二曲線。","governance":"FY26 自由現金流 18.1 億美元，是淨利 15.3 億的 1.19 倍；FY27 財測接近 17 億，較 FY26 下滑，以 EPS 財測中點乘 2 億股算淨利約 16.6 億，轉換率約 1.02 倍。FY27 回饋約 20 億美元，含回購 17 億與每股股利 1.85 美元，超出部分靠現金下降與商業本票。總槓桿 1.1 倍，遠低於 2.5 倍目標，目前不構成問題。SBC 在 Q4 占營業利益 7%，若全年比例相近約 1.3 億美元。管理層承諾 Coach 維持強勁且 Kate Spade 恢復成長前不併購。淨負債有兩個口徑：事實表含租賃約 34.7 億美元，管理層只算借款為 18 億美元；本次用本益比估值，不受影響。回購均價與近三年現金去向分項事實表未涵蓋。","valuation":"FY27 財測中點 8.30 美元算前瞻本益比 16.0 倍，共識快照 7.96 美元算 16.68 倍，共識仍是上調前數字。PEG 以共識三年年複合約 12.6% 算為 1.32，屬合理帶。Trailing 本益比在四個年度端點的 7% 分位不能當便宜證據，因為 FY25 GAAP EPS 只有 0.82 美元，把歷史端點墊高；P/S 在 75.8% 分位、EV/S 在 77.9% 分位，反映利潤率已在高位。五年分位資料不足，留空。賣方目標價平均 165–174 美元，全距 88–211 美元約 2.4 倍，方向支持進場，但多為 8 月前數字，不作依據。同業現值倍數事實表未涵蓋。短線 RSI 70.47，但 26 週報酬僅 0.15%，股價貼近 52 週均線，過熱只來自財報後跳漲。","premortem":"三個看錯方向的完整推演在反證紀錄。資料面有三處要打折：同業表疑似代號對錯，不能用來證明利差；共識近三個月上修 13.88% 很可能混到財年換算；歷史最大回撤與空方最強數字事實表未涵蓋。2026-08-13 法說管理層沒有正面回答促銷時點影響、逐季毛利率路徑與最擔心的競爭對手；前兩項在 Q1 結果中部分得到驗證，競爭對手仍無答案。"},"plain":{"six":{"how_it_makes_money":"賺的是全球年輕客群買 200–500 美元手袋的錢，利潤卡在 Coach 品牌這一節，Kate Spade 目前沒有貢獻獲利。","moat":"護城河方向持平：定價力在擴大，但證據只到 Coach 一個品牌，第三方份額數字缺，Kate Spade 也說明平台優勢不能複製。","growth":"五年後的跑道中等：Coach 到 100 億美元算得出來，但北美只有中個位數，滲透率無數字，第二條成長曲線尚未成形。","capital":"現金創造強、回購積極，但 FY27 股東回饋高於自由現金流，有一部分靠舉債支應。","valuation":"現價要求 EPS 五年約 10% 複利、倍數由 16 倍略降到 15 倍，才有約 8% 年報酬；基本面我信，賠率只算中等。","how_wrong":"最可能看錯的是把一段品牌熱度當成結構性優勢，其次是把回購撐出來的 EPS 當成營運成長。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":132.8,"week26_return_pct":0.15,"consensus_rev_3m_pct":13.88,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"共識快照落後財測，兩個分母只差約 4%，不改變結論。FY27 含第 53 週與小額關稅順風，影響不大到足以改變判斷；利益率是否處於高點已放進空頭情境，不靠本益比便宜來論證。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"假期檔期，Coach 改打限量與配色，促銷更少","impact":"高","watch":"促銷天數與北美直營成長"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q2 FY27 法說","impact":"高","watch":"Coach 固定匯率成長、北美年增、毛利率是否年增約 170 個基點"},{"date":"2027-03","date_precision":"month","type":"product","event":"Chelsea 40 上市，定價 525 美元","impact":"低","watch":"500 美元以上的接受度與 AUR"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"Q3 FY27 法說","impact":"中","watch":"下半年中個位數營收假設、Kate Spade 是否收斂"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,454B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河來自品牌熱度與直營定價，等級 B，方向持平。</p>
<ul class="pts">
<li>護城河的機制有三層。一是 200 到 500 美元價位帶的品牌熱度，二是約 87% 直營帶來的價格控制，三是約 10 億美元行銷量體形成的規模門檻。三層都建立在 Coach 一個品牌上。執行力評 8，定價力評 7，合併等級為 B，趨勢持平。</li>
<li>定價力的證據最強。FY26 手袋單價中十位數成長、件數低雙位數成長，Q1 單價低雙位數、件數低個位數。提價後件數仍然成長，是目前最好的反證。北美促銷天數也在減少。毛利率由 FY23 的 70.8% 升到最新 TTM 的 78.3%。</li>
<li>執行力只能評持平。Coach 獲客能力強，FY26 新客 1100 萬人，Q1 新客 260 萬人，執行長也說新客留存率位居客戶檔案最高之列。但 Kate Spade 在同一平台上續跌 10%，2026-08-13 執行長承認其知名度未改善。優勢長在 Coach 品牌，不在集團平台。</li>
<li>進入門檻的說法互相矛盾。Coach 品牌執行長 2026-08-13 說這行沒有進入門檻，財務長同場說規模門檻正在提高。兩者可以調和：門檻不在進入而在放大，所以護城河給中上評等，不給最高等級。被問到最擔心哪個對手時，管理層沒有點名。</li>
<li>競爭威脅有四項，都評為中等。Michael Kors 仍是主要對手，Polene、Jacquemus 靠社群與稀缺性吸引年輕客，機率約 30%。二手精品成長約為一手三倍，機率約 25%。歐洲品牌下探單價，機率約 20%。AI 購物助理，機率約 15%。這些數字多來自彙整文章，沒有一手份額。</li>
<li>同業比較在這份報告裡不能用。表內 MC 的毛利率 34.36% 不像精品公司，CFR 缺毛利率，疑似代號對到同名美股。RMS 與 KER 沒有資料，也沒有投入資本報酬欄。所以利差判斷不上調，第三方份額缺口是護城河評等的最大限制。</li>
<li>報酬持續性的四個檢查點，兩項偏正面、兩項中性。價值鏈分配與社會容忍度為綠，品牌端拿走大部分利潤，漲價沒有社會天花板。需求基礎與決策層級為黃，手袋是想要而非需要，替代只發生在單一款式的購買決定，轉換成本接近零。內生報酬上界約 10.3%。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```