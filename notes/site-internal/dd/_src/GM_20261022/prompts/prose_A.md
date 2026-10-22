你是 stock-analyst v20 的**散文層（prose）agent**，標的 GM（2026-10-22）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：GM　日期：2026-10-22　archetype：None　前份裁決：2026-05-24　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1548B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（412B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（868B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（925B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（879B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（927B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（915B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2057B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3221B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1723B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1548           3816-5452      5 條（2–6 內）  
s3                  8000         412           5312-7588      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2672          8630-12328      5 條（2–6 內）  
s6                 11000         927          7051-10073      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         915           1809-2585      5 條（2–6 內）  
s10                 5000        2057           2060-2943      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1723           2000-3277      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4272B；至少需散文≈40.73KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−55%
−51%
−41%
−38
−38%
−3.4%
−3.25%
−3.25
0.45
0.47
0.5%
0.5
0.66
0.7
0.75
0.9%
0.91
0.92
0.98%
01
1
1.3%
1.6%
1.7%
2%
2
02
2.1%
2.2
2.38
2.5
2.75
3%
3
3.27
3.4%
3.8%
4%
4
4.5%
4.5
4.6
4.61%
4.8%
4.9
5%
5
5.03
5.5%
5.5
5.69
5.7
6
6%
6.0%
6.2
6.8%
7
07
7.5
8
8%
8.2
8.2%
8.66
8.7%
9%
9
9.4
9.5
9.6
10
10%
10.8
11
12
12%
12.2%
12.8
13
13.37
13.5
14
14.6
15
15%
15.1
15.14
15.5
15.6
16
16.0%
16.6
16.65
16.7%
16.82
17%
17.4%
17.6
17.6%
17.7
18
18%
18.85%
19.3
20
20%
20.8
21
22
22.3
23%
23
24
25
25%
26
27
28
29
30%
30
30.0%
34.6%
35
35.5
36%
36
37
40%
40
41
41.1
42%
42
45
46
49
50%
50
52
54
60
60%
61
63
65.36
66
70
74
75
76.11
78.79
79.18
88
88%
90
94
98
99.8
100%
100
101
102.8
104
115
120
125
132
140
145
150%
150
155
167.25
200
232
379.9
414
500
500.2
2019
2022
2024
2025
2026
2027
2028
2029
2031
20261022
1,040
1,450
1,600
1,650
1,820
1,862.7
1,895.0
3,200
4,000
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
{"meta":{"ticker":"GM","date":"2026-10-22","schema":"v15.0","contract":"v19","company_name":"General Motors"},"oneliner":"全尺寸皮卡與大額回購撐住每股盈餘，但美國份額流失、2027 年約 20 億美元原料逆風與循環後段，讓 5.7 倍前瞻本益比不算錯價；等 2027 年 1 月指引確認成本吸收再談進場。","thesis":{"H":[{"id":"H1","text":"回購持續壓低股數，本業持平時每股盈餘仍能成長","2y":"2026–27 年稀釋股數每年減 ≥ 5%；調整後汽車自由現金流每年 ≥ 100 億美元","5y":"五年累計股數再減 ≥ 25%","10y":null,"threshold":"稀釋股數年減 ≥ 5%","source":"季報稀釋股數、回購公告（新授權 200 億美元）","drift_rule":"2 年期：連 2 季偏離 ≥ 5% 視為削弱，連 3 季偏離 ≥ 10% 視為反轉；5 年期：連 4 季偏離 ≥ 5% 視為削弱，連 6 季偏離 ≥ 10% 視為反轉"},{"id":"H2","text":"新一代全尺寸皮卡順利投產並帶動混合比，北美利潤率守住 8–10% 目標區","2y":"2027 年各季北美利潤率 ≥ 8%；2028 年增量產能帶動皮卡份額上升","5y":null,"10y":null,"threshold":"北美利潤率 ≥ 8%","source":"季報北美分部；法說投產進度（Silao、Fort Wayne、Orion）","drift_rule":"2 年期：連 2 季偏離 ≥ 5% 視為削弱，連 3 季偏離 ≥ 10% 視為反轉"},{"id":"H3","text":"保固、EV 虧損與軟體收入的改善，抵銷約 20 億美元原料逆風，2027 EBIT 不低於 2026","2y":"2027 年 EBIT 調整後 ≥ 2026 年實際值（2026 指引 145–155 億美元）","5y":null,"10y":null,"threshold":"2027 指引中值 ≥ 150 億美元","source":"2027 年 1 月全年指引；季報保固與 EV 損益","drift_rule":"2 年期：連 2 季偏離 ≥ 5% 視為削弱，連 3 季偏離 ≥ 10% 視為反轉"}],"R":[{"id":"R1","text":"原料、物流、記憶體與關稅成本吸收失敗：2026 原料逆風約 20 億美元，2027 若按 7 月以來漲幅年化再加 10–15 億美元；10-K 自承關稅可能超出估計，短期緩解無法完全抵銷；中東衝突推高物流與原料成本","h_ref":"H3","clock":"⚡","threshold":"2027 年 1 月指引的 EBIT 調整後中值 < 140 億美元，或北美利潤率連 2 季 < 8%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#3","geo_supply_chain#0"]},{"id":"R2","text":"美國份額慢性流失：2026 年迄今份額 16.7%（去年 17.4%），Q3 美國銷量年減 5.5%，2025 年全球批發量減至 379.9 萬輛；混動區隔缺席","h_ref":"H2","clock":"🔥","threshold":"美國份額連 4 季年減 ≥ 0.5 個百分點，或全年 < 16.0%","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","end_markets#1","supply_demand_durability#1"]},{"id":"R3","text":"新卡車投產品質與保固：NHTSA 對約 99.8 萬輛 L87 6.2L V8 皮卡與 SUV 評估 2025 年召回修復成效；新一代車型同時換上三款新引擎","h_ref":"H2","clock":"⚡","threshold":"調查升級為召回且單一費用 > 10 億美元，或保固年改善轉為惡化","evidence_refs":["major_events#2","product_recall_warning#0"]},{"id":"R4","text":"訴訟與法規罰款：Duramax 柴油排放與 8 速變速箱集體訴訟已發回重審，公司無法估計損失；Ultium TSCA 罰款累計 1,820 萬美元且持續增加。受影響營收與結案時點事實表未涵蓋","h_ref":"H1","clock":"🐢","threshold":"任一集體訴訟重新取得認證並出現不利和解，或單筆和解 > 10 億美元","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0"]},{"id":"R5","text":"EV 政策再翻轉：2026-01 已縮減 EV 產能並出售 Ultium Lansing 權益；若油價推高 EV 需求或法規回頭，可能再投入產能，吃掉回購資金","h_ref":"H1","clock":"🐢","threshold":"再出現 EV 相關重整費用，或 EV 資本支出顯著上調","evidence_refs":["major_events#1"]}],"single_thing":{"description":"美國進入衰退，新車 SAAR 連 3 個月跌破 1,450 萬輛","why_fatal":"北美大車占近九成本業利潤，營運槓桿高；量一掉，利潤率會跌出 8–10% 目標區，回購同時放緩，每股盈餘的兩個引擎一起熄火","if_happens":"清倉；等 SAAR 回升且北美利潤率重回 8% 以上，再重跑判斷","how_monitor":"Cox Automotive 月度 SAAR、GM Financial 違約率、經銷商庫存天數（目標 50–60 天）","probability":"約 25%（12–24 個月）；依據：管理層自己把 2027 成長綁在需求維持，分析師已在問利率上行與消費者體質，但 GM Financial 尚未見違約上升"}},"appendix_a":{"growth_durability":3,"quality_score":5,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":5.03,"peg_fy2":0.45,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":13.37,"FY2027E":15.14,"FY2028E":16.82},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（非 GAAP，Koyfin 共識 10-21 快照）；FY2025A 調整後實際值事實表未涵蓋，年報 GAAP 稀釋 EPS 3.27 美元含 EV 重整費用，不作基期"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"低利潤率高周轉，盈餘隨美國 SAAR 與原料成本擺動，每股盈餘成長主要靠回購"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性。依據：Q3 法說稱 SAAR 在 1,600 萬輛中高段、全年約 1,650 萬輛；鋼與銅較去年均價約高 50%；分析師已在問利率上行與消費者體質，GM Financial 違約率尚未上升。","bargaining":{"up":"供應端議價力弱：鋼、銅、記憶體與物流 7 月以來再漲，2026 原料物流逆風約 20 億美元，GM 仍在找抵銷項","down":"對終端有中等議價力：經銷商獨立，皮卡換代期折扣率比歷次換代低數百基點，北美全年定價僅 +0.5%","geo":"232 鋼鋁關稅仍在，墨西哥與加拿大進口車受 USMCA 檢討影響；2026 毛關稅成本落在 25–35 億美元區間低端"},"profit_pool_dir":"利潤池往北美燃油大車與軟體服務集中，EV 與國際縮小；全球份額往中國車廠移動","tam_table":{"expanded":false,"reason":"美國新車市場已成熟，GM 不屬低滲透或新品類故事；事實表只有 SAAR，沒有分區段 TAM 與利潤池占比，無法誠實展開"}},"moat":{"mechanism":"全尺寸皮卡與 SUV 的規模和品牌忠誠（美國全尺寸皮卡份額逾 42%、皮卡銷量連續七年第一），加上經銷網與自有融資，撐住高配車價與折扣紀律；這套機制在國際市場與小型車上不成立","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：北美利潤率年增 2.5 點，皮卡銷量年增 9%，換代期折扣偏低。定價面縮減：美國整體份額年減約 0.7 點，混動區隔缺席，2027 成本轉嫁未證。兩向抵銷，判為穩定。","peer_na_reason":"事實表沒有同業投入資本與 ROIC，無法算報酬差距；改以份額與折扣率作可比軸","threats":[{"level":"🔴","text":"中國低價車廠進入新興與成熟市場，10-K 自承已對定價、份額與獲利造成顯著負面影響；電池原料加工集中在中國，供應鏈也受制","p":35,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#4","reg_tariff_export#2"]},{"level":"🟡","text":"日系混動在美國拿走份額，GM 在小型、中型轎車與廂型車沒有車；法說稱多個區隔將推混動、不需額外資本支出，但時程未揭露","p":40,"evidence_refs":["end_markets#1"]},{"level":"🟡","text":"軟體定義車走向 AI 定義車，中國車廠速度與成本領先；大型科技公司支持的新進者衝擊直銷與所有權模式。GM 以 Super Cruise 百萬輛保有量與 2028 年高速公路免看路系統應戰","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"買車是可延後的購買，急迫性低；Q3 SAAR 在 1,600 萬輛中高段，GM Financial 違約率未見變化。但管理層把 2027 成長前提明寫為需求維持，消費者信心調查已偏弱"},{"item":"決策層級","level":"🟡","text":"替代決策發生在家庭每次換車，轉換成本低。皮卡買家忠誠度高（份額逾 42%、折扣率低），但混動需求把小型與中型車買家帶向日系"},{"item":"價值鏈分配","level":"🟡","text":"上游鋼、銅、記憶體與物流在 2026 年多拿走約 20 億美元，GM 尚未找到抵銷；經銷商獨立，價值鏈中 GM 只在皮卡與 SUV 有定價空間"},{"item":"社會容忍度","level":"🟡","text":"新車負擔能力已是政策與輿論話題，北美全年定價只 +0.5%。排放法規放寬帶來約 5 億美元節省，屬政策紅利，法規回頭就會消失；關稅也取決於政策"}],"roiic":"事實表未涵蓋；管理層自設新投資報酬門檻 20%（2026-10-20 法說，CEO），沒有實現值驗證","reinvest_rate":"事實表未涵蓋；資本支出落在 100–120 億美元指引下半區，折舊攤提未收","endo_ceiling":3,"formula_note":"增量 ROIC 與再投資率無法從事實表算出，改用代理：共識營收 FY1 約 1,862.7 億美元到 FY2 約 1,895.0 億美元（+1.7%），加上利潤率小幅改善，內生成長上界取約 3%"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","GM":5.74,"TSLA":18.85,"AMZN":50.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","GM":0.98,"TSLA":4.61,"AMZN":11.52,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","GM":0.33,"TSLA":5.55,"AMZN":-0.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","GM":null,"TSLA":7.46,"AMZN":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"TSLA","gm":18.85,"om":4.61,"fcf_margin":5.55,"rd_intensity":7.46,"strategy_note":"近四季營業利益率 4.61%、毛利率 18.85%，高於 GM 的 GAAP 數字，但 GM 含 EV 重整費用；兩家在 EV 與自駕直接對打，GM 的利潤池在燃油大車，與特斯拉重疊有限","period":"TTM ending 2026-06-30（4季加總）"},{"name":"AMZN","gm":50.25,"om":11.52,"fcf_margin":-0.49,"rd_intensity":null,"strategy_note":"同業表列入亞馬遜，但它不是整車廠，利潤率對比沒有意義，不作護城河判讀依據","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量：2027 皮卡產量與 2026 持平，2028 有增量產能；價：北美全年 +0.5%；併購：無；回購：每股盈餘成長的主力","runway_years":"不適用：美國新車市場已成熟，GM 美國份額約 17%，成長靠份額與價格，談不上滲透率","runway_post_y5":"🔴","endo_ceiling_basis":"內生上界約 3%。增量 ROIC 與再投資率事實表未涵蓋，以共識營收 +1.7% 加利潤率小幅改善代理。共識 EPS 兩年複合約 12.2%，缺口約 9 個百分點，主要歸因淨回購，其次是利潤率改善","segments":[{"item":"北美","value":"Q3 營收約 414 億美元，年增 2.1%；EBIT 調整後約 36 億美元，利潤率 8.7%"},{"item":"國際（不含中國權益）","value":"Q3 EBIT 調整後損益兩平，年減 2 億美元，含 Momenta 投資評價損失約 1 億美元"},{"item":"中國權益收入","value":"Q3 3,200 萬美元，連續 8 季獲利，新能源車占 GM 中國銷量逾 60%"},{"item":"GM Financial","value":"Q3 調整後稅前 7 億美元，全年指引 25–30 億美元，季配 2.5 億美元給母公司"},{"item":"軟體與服務","value":"Q3 認列營收逾 8 億美元，年增 15%；年底遞延營收接近 75 億美元，2027 年認列預期雙位數成長"},{"item":"GM Defense","value":"2026 營收約 7 億美元，管理層預期營收年增逾 30%；ISV 潛在合約逾 10 億美元，需國會撥款"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q3 北美調整後利潤率年增 2.5 點；季度 GAAP 毛利率事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"美國份額 16.7%，去年 17.4%"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"全尺寸輕型皮卡銷量年增 9%"},{"signal":"每股盈餘成長高於營收成長逾 5 點","lit":true,"note":"共識 EPS 兩年複合約 12%，營收只增 1.7%，差距來自回購"},{"signal":"自由現金流與淨利比連 2 年低於 0.75","lit":false,"note":"合併口徑 2024 為負、2025 約 0.66，但調整後汽車自由現金流 2026 指引 115–125 億美元；兩口徑差異的拆解事實表未涵蓋，不計入"},{"signal":"股權酬勞占營收超過 5% 且上升","lit":null,"note":"事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"混動與中國低價車屬份額替代，美國總量未萎縮，已計入份額項"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"},{"signal":"維持性資本支出占自由現金流逾 60%","lit":null,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"2025 營收年減 1.3%，但 2027–28 有皮卡、SUV 與回美國生產的產能投資"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"回購","value":"2026 年迄今 63 億美元，含 Q3 25 億、10 月 10 億；新授權 200 億美元多年期"},{"item":"股息","value":"近 12 個月殖利率約 0.9%"},{"item":"資本支出","value":"2026 年落在 100–120 億美元指引下半區"},{"item":"EV 重整現金費用","value":"累計 74 億美元，已付 46 億，Q4 約 10 億，餘額 2027 年付清"}],"capalloc_grade":"A","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月無併購交割，只出售 Ultium Cells Lansing 廠權益給 LG Energy Solution","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"以前瞻本益比 5.69 倍回購，盈餘殖利率約 17.6%；事實表未收 10 年期公債殖利率，但差距大到結論不受影響","grade":"過"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數年減約 9%（Q3 約 8.66 億股），淨稀釋為負","grade":"過"}]},"valuation":{"basis":"前瞻本益比（調整後稀釋 EPS，FY2026E）","tier":"整車廠","peers":{"expanded":false,"reason":"事實表沒有同業前瞻本益比；同業表只有利潤率，且亞馬遜不可比"},"fwd_pe":5.69,"peg":0.47,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比 5.69 倍；以共識兩年 EPS 複合約 12.2% 計，PEG 約 0.47；企業價值營收比在四個年度端點中落在 29 分位。便宜成立，但盈餘處於循環高原、成長主要靠回購，便宜不等於錯價。","upside_short_pct":15.1,"upside_mid_pct":23.0},"trap_analysis":{"verdict":"🟡","label":"循環高原上的低本益比"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"管理層把 2027 成長綁在需求維持與原料回落兩個前提；美國份額正在流失；10-K 自承關稅可能超出估計","assumption":"美國需求維持在 SAAR 1,600 萬輛上下，原料自高點回落","consequence":"若衰退與原料高檔同時發生，EPS 可能在 2–3 年內從 13 美元級回落到 8–9 美元，倍數同時壓到 4.5–5 倍，股價腰斬","ruling":"採納：這是五年虧五成最可能的路徑，已寫成唯一致命點，Bear 機率給 30%","watch":"SAAR 月度數字、GM Financial 違約率、北美利潤率","evidence_refs":["end_markets#1","reg_tariff_export#1","supply_demand_durability#1"],"fact_refs":["f_kpi6_gmna_ebit_adjusted_margi","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"EV 政策已反覆一次：2025–26 年 EV 重整現金費用累計 74 億美元。CFO 說油價可能推高 EV 滲透、要做好準備，2028–29 年 LMR 電池將再推一輪；回購又是在盈餘高原執行","assumption":"回購資金不被 EV 再投資或下一輪政策轉向吃掉","consequence":"皮卡賺的錢再度投入低報酬的 EV 產能，或高價回購遇上循環下行，每股價值不增","ruling":"部分採納：管理層 7 月稱曾拒絕數十億美元的 EV 廠投資，有紀律紀錄；但政策再翻轉的可能存在，列入風險監測","watch":"EV 相關資本支出與重整費用是否再出現；回購均價對盈餘的倍數","evidence_refs":["major_events#1"],"fact_refs":["f_kpi4_adjusted_automotive_free"]},{"view":"價格已反映太多","evidence":"前瞻本益比 5.69 倍；2027 共識 EPS 15.14 美元，近 3 個月 FY1 共識上修 4.5%","assumption":"共識尚未完全扣掉 7 月以來的原料漲價","consequence":"若共識下修約 4–8%，在倍數不變下股價下行有限","ruling":"反駁：倍數已在整車廠低檔，價格沒有反映太多；風險在盈餘分母，不在倍數，已放進論點失敗那條","watch":"1 月指引公布後的 2027 共識 EPS 修正","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-55,"hi":-38,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 78.79 → 本次 76.11（-3.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=78.79","side_b":"本次 price_at_dd=76.11","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 78.79 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 78.79 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 78.79 美元：Bull 價 167.25、Bear 價 54，五年期望值 +30.0%，基準年化 6.0%，不對稱比 2.38","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.38。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 78.79 美元：五年期望值 +30.0%，基準年化 6.0%，不對稱比 2.38","side_b":"本次情境、股價 76.11 美元：五年期望值 +34.6%，基準年化 6.8%，不對稱比 2.75","ruling":"再換股價、情境不動：起點價下跌 3.4%，五年期望值多 4.6 個百分點，基準年化多 0.7 個百分點，不對稱比由 2.38 升到 2.75。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2027 盈餘方向（管理層前後說法）","cause":"新證據","prior_field":null,"side_a":"2026-07-21 CFO：依目前所知，2027 年營收、利潤率、EBIT 與自由現金流都能成長","side_b":"2026-10-20 CFO：要原料價格從現水準回落一些才有信心成長；按 7 月以來漲幅年化，2027 逆風合計約 20 億美元","ruling":"不可調和，採 B 側：Base 路徑 2027 EPS 14.6 美元，比共識 15.14 低約 4%。現在就買的最強論證是：前瞻 5.7 倍、調整後汽車自由現金流約當市值 18%、新回購授權約當市值三成，就算 EBIT 持平，股數每年縮 5% 以上也能推升每股盈餘。不採的理由是這套算術在衰退時同樣反向放大，而 1 月指引這個決勝數據三個月內就到。觀望的約束只有一個：2027 原料成本能否吸收。","evidence_level":"公司法說原話（兩場）","settle_metric":"2027 年 1 月全年指引的 EBIT 調整後中值","if_then":["若中值 ≥ 150 億美元且第四季北美利潤率 ≥ 8%，首倉 2%","若中值 < 140 億美元，不追，並把 Base 2027 EPS 下修到 13.5 美元","價格先走、證據未到：若指引前股價跌到 66 美元以下且第四季數字未惡化，分批反買首倉 2%"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"份額","cause":"新證據","prior_field":null,"side_a":"美國整體份額 16.7%（去年 17.4%），底特律三強 Q3 份額創新低","side_b":"全尺寸皮卡銷量年增 9%、份額逾 42%，燃油車銷量年增；流失集中在 EV 縮減、停產車款與 GM 未參與的混動區隔","ruling":"可調和，屬程度差異：利潤池未失守，但混動缺口是慢性流失，列入風險，不判定護城河下滑","evidence_level":"公司法說與第三方銷量估計","settle_metric":"2027 年美國整體份額與全尺寸皮卡份額","if_then":["若美國份額連 4 季年減 ≥ 0.5 個百分點，停止加碼","若混動車型 2027 年上市且份額止跌，維持現有判斷"],"evidence_refs":["end_markets#1","competitive_share_entrants#3"]},{"axis":"關稅成本估計","cause":"新證據","prior_field":null,"side_a":"10-K（2026-01）：2026 年關稅對 EBIT 調整後衝擊 30–40 億美元","side_b":"Q3 法說：2026 毛關稅成本落在 25–35 億美元低端，年迄今淨額約 18 億美元（含 IEEPA 退款）","ruling":"可調和：差異來自 IEEPA 關稅被推翻後的退款。232 鋼鋁關稅仍在，CFO 自承退款 2027 年不會重複，2027 關稅成本以毛額看","evidence_level":"10-K 與法說原話","settle_metric":"2027 指引中的關稅成本估計","if_then":["若 2027 關稅估計高於 2026 毛額上緣，Base 路徑再下修"],"evidence_refs":["reg_tariff_export#0","geo_supply_chain#3"]},{"axis":"估值結論漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 78.79 美元，估值判為便宜","side_b":"現價 76.11 美元、前瞻本益比 5.69 倍，FY1 共識近 3 個月上修 4.5%","ruling":"估值結論不變：價格小跌、分母上修，倍數更低，但便宜的成因仍是循環高原","evidence_level":"事實表價格與共識快照","settle_metric":"前瞻本益比","if_then":[],"evidence_refs":[]},{"axis":"品質評級、陷阱與護城河方向漂移","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份：整體評級 B、陷阱風險中度、護城河穩定","side_b":"本輪三項不變：北美利潤率回升到 8.7%、皮卡銷量年增 9%，抵銷美國整體份額下滑與原料逆風","ruling":"維持：Q3 證據兩向都有，淨方向未改變","evidence_level":"Q3 季報與法說","settle_metric":"北美利潤率與美國份額","if_then":[],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"跑道、類型、循環位置與情境機率","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未評跑道、類型、循環位置與情境機率（皆為空），倚賴本益比回到 8 倍以上的均值回歸論點","side_b":"跑道窄（美國新車市場成熟、無足量第二曲線）；類型為循環/商品，循環位置為晚循環；情境機率 20／50／30，最大回撤 −38% 至 −55%；Base 終端倍數 6 倍","ruling":"方法變動：本輪改用循環股框架，前份的倍數均值回歸假設只保留在 Bull 路徑（7.5 倍）","evidence_level":"判斷方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設進場重啟條件","side_b":"2027 年 1 月指引的 EBIT 調整後中值 ≥ 150 億美元，且第四季北美利潤率 ≥ 8%","ruling":"新設：觀望的唯一約束是成本吸收，重啟條件即該約束的否定","evidence_level":"判斷方法","settle_metric":"2027 全年指引","if_then":[],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻","side_b":"北美利潤率連 2 季 < 6% 清倉；SAAR 連 3 個月 < 1,450 萬輛清倉；美國份額全年 < 16.0% 減碼；稀釋股數年減 < 3% 減碼","ruling":"新設：依循環股特性，把需求、利潤率、份額與回購四個承重變數各設一條門檻","evidence_level":"判斷方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing","side_b":"Single Thing：美國進入衰退、新車 SAAR 連 3 個月跌破 1,450 萬輛","ruling":"新設：北美大車占近九成本業利潤，需求下滑是數學上最大的單一敏感項","evidence_level":"判斷方法","settle_metric":"SAAR 月度數字","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 全年指引確認原料成本吸收","type":"估值rearm","maps_to":"H3","metric":"2027 年 EBIT 調整後指引中值；第四季北美利潤率","threshold":"中值 ≥ 150 億美元且北美利潤率 ≥ 8%","action":"首倉 2%","source_freq":"第四季財報與全年指引（每年一次）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"北美利潤率跌出目標區","type":"假設驗證","maps_to":"H2","metric":"北美 EBIT 調整後利潤率","threshold":"連 2 季 < 8%","action":"不追；若已持有，停止加碼","source_freq":"季報","date":null,"evidence_refs":[]},{"n":3,"text":"美國進入衰退","type":"Single Thing","maps_to":"Single Thing","metric":"美國新車 SAAR","threshold":"連 3 個月 < 1,450 萬輛","action":"清倉","source_freq":"Cox Automotive 月度","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":4,"text":"美國份額持續流失","type":"風險","maps_to":"R2","metric":"GM 美國市佔年變化","threshold":"連 4 季年減 ≥ 0.5 個百分點","action":"停止加碼","source_freq":"季度銷量公告","date":null,"evidence_refs":["end_markets#1","competitive_share_entrants#3"]},{"n":5,"text":"L87 V8 調查擴大為召回","type":"風險","maps_to":"R3","metric":"NHTSA 工程分析結論與召回費用","threshold":"召回確定且單一費用 > 10 億美元","action":"減碼","source_freq":"NHTSA 公告與 8-K","date":null,"evidence_refs":["product_recall_warning#0","major_events#2"]},{"n":6,"text":"回購放緩","type":"減碼","maps_to":"H1","metric":"稀釋股數年減幅","threshold":"< 3%","action":"減碼","source_freq":"季報","date":null,"evidence_refs":[]},{"n":7,"text":"價格回落而基本面無損","type":"加碼","maps_to":"H1","metric":"股價對 104 週均線；全年指引","threshold":"股價 ≤ 66 美元且指引未下修","action":"分批反買，首倉 2%","source_freq":"每週","date":null,"evidence_refs":[]},{"n":8,"text":"第四季財報後複審","type":"複審日期","maps_to":"H3","metric":"2027 指引與第四季數字","threshold":"財報公布","action":"重跑完整判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"北美 EBIT 調整後利潤率","bear_threshold":"連 2 季 < 6%（清倉）","window":"2027 Q1 至 2028 Q4","source":"GM 季報新聞稿","last_status":"ok"},{"metric":"美國新車 SAAR","bear_threshold":"連 3 個月 < 1,450 萬輛（清倉）","window":"未來 24 個月","source":"Cox Automotive 月度預估","last_status":"ok"},{"metric":"GM 美國市佔","bear_threshold":"全年 < 16.0%（減碼）","window":"2027 全年","source":"Cox Automotive 與 GM 季度銷量","last_status":"warning"},{"metric":"稀釋股數年減幅","bear_threshold":"< 3%（減碼）","window":"每季滾動 4 季","source":"GM 季報","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"7","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":true,"basis":"runway_post_y5='🔴'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🔴', val='🟢', moat_trend='→', week26=-3.25, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['7']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"4%","requires_critic":[],"rearm_trigger":"2027 年 1 月指引的 EBIT 調整後中值 ≥ 150 億美元，且第四季北美利潤率 ≥ 8%","exec_line":"條件成立後首倉 2%；2027 Q1 財報確認新卡車放量、北美利潤率仍 ≥ 8% 再加到 4%；循環股倉位上限 4%"},"reasoning":{"industry":"Q3 營收 500.2 億美元、EBIT 調整後 41.1 億美元（利潤率 8.2%）。北美營收約 414 億美元，EBIT 調整後約 36 億美元，利潤率 8.7%，約占全公司 EBIT 的 88%。國際（不含中國權益）損益兩平，中國權益收入 3,200 萬美元，GM Financial 稅前 7 億美元，OnStar 與 Super Cruise 認列營收逾 8 億美元。單點依賴：北美大車撐起近九成本業利潤，新一代輕型皮卡 Q3 起先在墨西哥 Silao 投產，關稅與投產品質是集中風險。供需持久性屬週期性：美國 SAAR 全年約 1,650 萬輛，處於中段水位，需求靠消費者撐住；原料通膨與利率上行是將反轉的訊號。GM 自稱多數車款產能滿載，供給可逆性中等。產業時鐘判為過熱期：量持平、利潤率在目標區、投入成本 7 月以來再漲 10–15%（較去年均價約 50%），屬獲利面後段，量面並未過熱。產業態勢雙向拉鋸：一邊是競爭惡化（日系混動拿下美國過半份額、中國車廠全球份額上升），一邊是美國需求穩、皮卡折扣紀律好；另有關稅與排放法規放寬兩項結構變數。","moat":"護城河機制只在北美全尺寸皮卡與 SUV 成立。法說稱全尺寸皮卡份額逾 42%，換代期折扣率比歷次換代低數百基點；四品牌 3 月平均成交價年增 3.8%。執行面在擴大：北美利潤率 8.7%，年增 2.5 點，保固年改善約 11 億美元，兩次上調全年指引。定價面在縮減：美國整體份額 16.7%（去年 17.4%），流失集中在 EV 縮減、停產車款，以及 GM 沒有車的混動區隔。2027 原料逆風約 20 億美元能否轉嫁仍未知，CFO 也提醒不要用 2019 換代的漲價幅度推估。兩向抵銷，判為穩定，執行 7 分、定價 5 分。同業比較：事實表只有利潤率。GM 近四季 GAAP 營業利益率 0.98%，低於特斯拉的 4.61%，但這個數字含 EV 重整費用；投入資本缺漏，無法算 ROIC 差距，改看份額與折扣率。報酬持續期：屬低利潤率×高周轉，四檢查點皆為黃燈。增量報酬事實表未涵蓋；管理層自設新投資門檻 20%，沒有實現值驗證。內生成長上界以共識營收成長代理，約 3%。","growth":"共識調整後 EPS 由 FY2026E 13.37 美元升到 FY2028E 16.82 美元，兩年複合約 12.2%。共識營收 FY1 到 FY2 只增 1.7%。內生上界約 3%，缺口約 9 個百分點：主要來自淨回購（稀釋股數年減約 9%），其次是利潤率改善（保固、EV 虧損縮小、軟體），併購為零。法說稱 2027 皮卡產量與 2026 持平，2028 才有增量產能；軟體遞延營收年增 40%，但認列營收占比不到 2%，撐不起第二條成長曲線。美國新車市場已成熟，判跑道窄。衰退訊號十項亮兩項：美國份額縮減，以及每股盈餘成長遠高於營收成長。","governance":"現金去向如下。2026 年迄今回購 63 億美元，完成前次授權；新授權 200 億美元、多年期，約當市值三成。資本支出落在 100–120 億美元下半區。EV 重整現金費用累計 74 億美元，已付 46 億美元（其中 2026 年付 42 億），Q4 再付約 10 億，餘額 2027 年付清。股息殖利率約 0.9%。稀釋股數 Q3 約 8.66 億，年減約 9%。管理層的框架是：新投資要求 20% 報酬、維持投資等級，其餘回饋股東；四家信評皆給投資等級。自由現金流轉換：調整後汽車自由現金流 2026 指引 115–125 億美元，與調整後盈餘約略相當。合併口徑自由現金流 2022–2024 為負、2025 為 17.7 億美元，兩口徑落差的拆解事實表未涵蓋。合併淨負債 1,040 億美元，金融子公司與汽車本業的拆分事實表未涵蓋。股權酬勞占營收事實表未涵蓋。計分方面：近 12 個月無併購；回購以前瞻盈餘殖利率約 17.6% 買入，股數淨減，兩項通過。風險在於回購是在盈餘高原執行，若循環下行，同一筆錢在更低價位能買更多股。","valuation":"現價 76.11 美元、前瞻本益比 5.69 倍，等於市場只願付不到六年的盈餘，隱含盈餘將從高原回落。要讓現價划算，只需要 2027–28 年調整後 EPS 守在 14–16 美元並持續回購；我估守得住的機率約五成，衰退情境約三成。近四季 GAAP 本益比 16.65 倍的分母被 EV 重整費用壓低，不作依據。企業價值營收比 0.92 倍，在四個年度端點中落在 29 分位；事實表沒有真正的五年分位。以共識 FY2026E 到 FY2028E 兩年複合約 12.2% 計，PEG 約 0.47，但成長主要來自回購。12 個月 Base：2027E 14.6 美元乘 6 倍，約 88 美元（+15%）；3 年：2029E 15.6 美元乘 6 倍，約 94 美元（+23%）。賣方年中平均目標價約 98–101 美元，區間 61–132 美元，最高與最低之比約 2.2 倍。我的估值低於賣方，是因為把 2027 原料逆風扣進盈餘。事實表沒有同業前瞻本益比，終端倍數只能對照自身歷史與現價。","premortem":"盈餘停在 EBIT 145–155 億美元的高原，原料、關稅與份額三項逆風同時存在；衰退一來，5.7 倍本益比就會變成陷阱。衰退訊號十項亮兩項，陷阱風險中度。股價 26 週 −3.25%、RSI 35.5，位於 52 週均線 79.18 美元之下、104 週均線 65.36 美元之上，動能不熱。最大回撤推估 −38% 至 −55%（Bear 谷底 EPS 約 8.2 美元乘 4.5–5.5 倍）；歷史回撤事實表未涵蓋。三個反證視角見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺北美燃油大車的錢：利潤卡在全尺寸皮卡與 SUV 的定價和混合比，國際與 EV 不賺錢","moat":"護城河穩定但窄：只在北美全尺寸皮卡與 SUV 成立，整體份額正被混動與中國品牌侵蝕","growth":"成長跑道窄：量持平、價小幅，每股盈餘成長主要靠回購","capital":"資本配置積極且合理：自由現金流大量轉成回購，在低估值下回購效益高","valuation":"現價隱含盈餘將從高原回落；只要 2027 盈餘守住，回購就能推升每股價值，但我不認為市場明顯錯價","how_wrong":"最可能看錯的是循環位置：盈餘在高原，衰退或成本失控會讓低本益比變成陷阱"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 1 月全年指引：EBIT 調整後中值 ≥ 150 億美元，且第四季北美利潤率 ≥ 8%","trap":"🟡","val":"🟢","moat":"C","moat_trend":"→","runway_post_y5":"🔴","capalloc_grade":"A","archetype":"循環/商品","price_at_dd":76.11,"week26_return_pct":-3.25,"consensus_rev_3m_pct":4.53,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"GAAP 近四季本益比 16.65 倍的分母被 EV 重整費用壓低，改用調整後前瞻 EPS 錨定。重整現金費用管理層稱已大致認列，本輪不視為爭點；循環高原的分母風險已放進 Bear 機率 30%。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年指引（董事會 12 月核定預算）","impact":"高","watch":"EBIT 調整後中值是否 ≥ 150 億美元，以及原料逆風估計"},{"date":"2027-01","date_precision":"month","type":"capacity","event":"Fort Wayne 皮卡廠停工 4 週後以新車型復工","impact":"中","watch":"投產節奏與皮卡庫存天數"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"Orion 廠投產新一代輕型皮卡","impact":"中","watch":"2028 年增量產能是否如期"},{"date":null,"date_precision":null,"type":"regulatory","event":"NHTSA 對約 99.8 萬輛 L87 V8 車款的工程分析結論","impact":"中","watch":"是否擴大召回，以及費用規模"}],"_projected_from":"v19"}
```
