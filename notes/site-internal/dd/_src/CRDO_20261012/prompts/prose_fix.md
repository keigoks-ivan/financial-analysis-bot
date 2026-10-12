你是 stock-analyst v20 的**散文層（prose）agent**，標的 CRDO（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRDO_20261012/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：CRDO　日期：2026-10-12　archetype：None　前份裁決：2026-09-04　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2284B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（962B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1002B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1591B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1281B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（655B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1069B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1927B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3445B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2980B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（278B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2284           3301-4716      3 條（2–6 內）  
s3                  8000         962           4927-7038      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3874          7788-11126      5 條（2–6 內）  
s6                 11000         655          7241-10345      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1069           1702-2431      3 條（2–6 內）  
s10                 5000        1927           2151-3073      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2980           2000-2020      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         278            855-1222      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5752B；至少需散文≈39.25KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65
−65%
−60%
−53%
−45%
−45
−24%
0
0.073
0.2
0.29
0.37
0.522
0.55
0.56
0.62
0.622
0.65
0.75
0.829
0.85
0.86
0.88
0.902
0.92
0.952
1.00
01
1
1%
1.05
1.17
1.20
1.207
1.5%
1.6
1.75
1.80
1.88
2
2.00
2%
2.306
2.36
2.51
2.8
2.9%
2.9
3
03
3.13
3.131
4
04
4%
4.07
4.08
4.37
4.45
4.5
4.6%
4.65
4.72
4.723
4.733
4.75
4.79
05
5
5%
5.25
5.35
5.6
5.87
06
6
6.0
6.1
6.3
6.31
6.7
6.79
6.8
7%
7
7.2
7.5%
7.5
7.6
7.64
7.643
8
8.5%
09
9%
9
9.2
9.6%
9.69
10
10%
10.8
11
11.3
11.4
12%
12
12.45
12.8
13%
13.35
13.4%
13.6%
14%
14
14.1
14.8
15%
15
16.8%
17
17.4
18
18.1%
18.3
18.4%
20
20%
21.5
22
22.3
22.35
22.8%
24
24.7
25%
25
25.2%
25.6
26
28
30%
30
30.5%
31%
31.7%
31.9%
32%
33%
33.3%
34
34.3
34.32
35%
35
36%
38.1%
40%
40
40.5%
40.5
42
43
43%
45
47.2
48.1%
48.2%
48.5%
49
50%
50.1
52%
52.2%
53%
55%
56.5%
57.7%
61%
63%
64.5%
66
66%
67%
67.1%
68.0%
68%
68
68.8%
69%
70
70%
75.1%
76.8
80%
81%
81.08
84%
85%
88%
95.3%
97.9
98.2%
99.9
100
100%
102
112
114.7%
$120
$135
150%
164.17
175
190
200
205.7%
216
216.55
221
263.6
292
310
602
612.5
800
2024
2025
2026
2027
2028
2029
2030
2035
20261012
2,000
3,000
6,000
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
{"meta":{"ticker":"CRDO","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Credo Technology Group Holding Ltd"},"oneliner":"AI 叢集連接的可靠度專家，AEC 續長、光學第二曲線已出貨；但股價五週漲 32%、前瞻本益比 34 倍、Base 五年年化約 7%，價格走在證據前面，等 175 美元附近或 Q2 FY27 驗證","thesis":{"H":[{"id":"H1","text":"下半年營收依管理層節奏兌現：Q2 季增約 10%、Q3 約 20%、Q4 約 30%，FY27 營收 ≥24 億美元，FY28 初單季朝 10 億美元前進，不是高基期反轉","2y":"FY27 營收 ≥24 億美元（指引 >85%≈24.7 億）；FY28 營收 ≥35 億美元","5y":null,"10y":null,"threshold":"Q2 ≥5.25 億、Q3 ≥6.0 億、Q4 ≥7.6 億美元","source":"公司季報新聞稿與 10-Q（季）；2026-09-01 法說 CFO、2026-09-10 高盛會議 CFO","drift_rule":"2 年期：連 2 季營收落後上述路徑 ≥5% 為削弱，連 3 季 ≥10% 為反轉"},{"id":"H2","text":"光學成為第二支柱且不稀釋毛利：FY27 光學 >6 億美元（DSP、矽光子 PIC、ZeroFlap 各 >1 億），模組占比上升下非 GAAP 毛利率守住 66% 以上","2y":"FY27 光學 ≥6 億美元；FY28 光學 ≥12 億（CEO：光學產能到 FY28 底倍增至三倍）","5y":"光學占營收 ≥40%，NPO／CPX 設計案自 FY28 起量","10y":"系統級光學（ZeroFlap＋PILOT＋NPO）與 AEC 並列，銅光營收趨近各半（CEO 2026-06-01 長期願景）","threshold":"FY27 光學 ≥6 億美元；非 GAAP 毛利率 ≥66%（指引 67%–69%）","source":"法說光學營收口徑（季）、財報新聞稿毛利率","drift_rule":"2 年期：Q3–Q4 FY27 光學未見季度加速或毛利率 <66% 連 2 季為削弱，FY27 光學 <4.5 億為反轉；5 年期：光學占比連 4 季停滯為削弱、連 6 季為反轉"},{"id":"H3","text":"AEC 在 1.6T 世代守住主導：Marvell 等進入者與客戶多源化未壓縮 AEC 量價，銅在機櫃內 1–7 公尺維持主流到大規模 CPO 部署之後","2y":"1.6T AEC 於 FY27 下半年開始貢獻、FY28 放量（CEO）；非 GAAP 毛利率不低於 FY26","5y":"AEC 仍正成長；無 sourced 資料顯示最大客戶的第二供應商份額 ≥30%","10y":null,"threshold":"非 GAAP 毛利率 ≥66%；最大客戶占比季減不超過 10pp 或同季總營收不季減","source":"10-Q 客戶集中附註、法說（季）；第三方份額估計（年）","drift_rule":"5 年期：連 4 季毛利率低於 FY26 水準 ≥5% 為削弱、連 6 季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"客戶拉貨暫停：前四大客戶占 84%、最大 33%，CEO 承認 10% 客戶季間有暴增與暫停；一家暫停就能讓單季營收跌破指引","h_ref":"H1","clock":"⚡","threshold":"任一季營收低於指引下緣，或連 2 季季增 <5%","evidence_refs":["end_markets#2","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R2","text":"AEC 第二來源與價格壓力：Marvell 推 AEC 產品與 Golden Cable 生態讓客戶帶自有 IP，客戶本來就要多源；2026-09-10 被問價格壓力時管理層未回應","h_ref":"H3","clock":"🔥","threshold":"非 GAAP 毛利率 <66% 連 2 季，或最大客戶占比季減 ≥10pp 且總營收季減","evidence_refs":["competitive_share_entrants#1","customer_second_source#2","customer_second_source#3"]},{"id":"R3","text":"架構替代：1.6T 以後 CPO／NPO 可能壓縮 AEC 可服務市場；多數分析認為大規模 CPO 在 2027–2029 之後，Credo 以 NPO／CPX 與 ALC 對沖","h_ref":"H3","clock":"🐢","threshold":"hyperscaler 具名機櫃內大規模 CPO 部署且 AEC 營收年增轉負","evidence_refs":["substitute_technology#0","channel_business_model_shift#1"]},{"id":"R4","text":"供應鏈與關稅：全部晶圓靠 TSMC、無長期產能合約，換代工需 9–12 個月並重新認證；關稅、出口管制與中國子公司資金匯出限制","h_ref":"H1","clock":"🔥","threshold":"管理層歸因供給不足致營收低於指引，或毛利率季減 ≥2pp 且歸因關稅","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#4","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R5","text":"2027 年後雲端資本支出放緩：二手來源認為 2027 為高峰、之後增速 <10%，FY29 共識 12.45 美元的路徑最受影響","h_ref":"H1","clock":"🔥","threshold":"FY28 首次營收指引（約 2027-06）年增 <40%","evidence_refs":["supply_demand_durability#2"]}],"single_thing":{"description":"最大客戶（Q1 FY27 占營收 33%）在 1.6T AEC 世代導入第二供應商並拿走 ≥30% 份額","why_fatal":"一家客戶占營收三分之一，AEC 又是最大事業；份額流失同時打到量與價，FY28 EPS 是情境樹最敏感的單一項，Base 9.2 與 Bear 6.8 的差距大半來自這裡","if_happens":"Base FY28 EPS 下修約 15%–20%、倍數同步壓縮，改走 Bear 路徑；減碼至半倉並凍結加碼","how_monitor":"10-Q 客戶集中附註與法說 10% 客戶名單（季）；最大客戶占比季減 ≥10pp 且總營收季減即視為發生；第三方份額報告（年）","probability":"25%（12–24 個月）：客戶本就要多源、Marvell 生態已上線，但 1.6T AEC 驗證門檻高，目前無具名第二供應商得標證據"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.35,"peg_fy2":0.55,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":2.51,"FY2027E":6.31,"FY2028E":9.69,"FY2029E":12.45},"fy_end_month":4,"eps_basis":"FY2026A 為 GAAP 稀釋 EPS（事實表無 FY26 非 GAAP 年度值）；FY2027E–FY2029E 為 Koyfin 共識非 GAAP 口徑，基期口徑不一致會高估三年成長率，PEG 改用 FY27E→FY29E 年化 40.5%"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRDO_20261012/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"無廠半導體＋系統級產品；毛利率 FY23 57.7%→FY26 68.0% 連升；FY26 FCF 率 30.5%；營收由 AI 資本支出驅動、客戶高度集中"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久但有週期性反轉風險：叢集規模與 1.6T 換代是結構性需求（CEO 引光模組單位數 2026 年 6,000 萬→2030 年 1.75 億），但二手來源認為雲端資本支出 2027 見頂、之後增速降到 10% 以下，2028 無共識","bargaining":{"up":"TSMC 單一晶圓代工、BizLink 組裝，除 BizLink 部分 AEC 協議外無長期供貨合約，換代工需 9–12 個月並重新認證（FY26 10-K）","down":"前四大客戶占 84%、最大 33%；客戶明說要多源，Marvell 生態計畫讓客戶自帶 IP","geo":"製造與封測外包、主要在亞洲；晶圓依賴台灣；中國大陸設研發與銷售，資金匯出受當地法規限制"},"profit_pool_dir":"利潤池由傳統雷射光模組往『可靠度導向』的銅纜與系統級光學移動：800G 世代 AEC 在 GPU 到第一層交換器取代光模組；下一步是模組業者與晶片商在 1.6T 與 NPO 重新分配","tam_table":[{"item":"AEC 市場規模","value":"JPMorgan 估 2028 年約 40 億美元（二手引述）；Lucintel 估 2035 年約 68 億美元、2026–2035 年複合 22.8%（另一版本 35 億，數字不一致，品質存疑）"},{"item":"Credo AEC 份額","value":"約 80%～88%（2025-10 前後估計，未經 Dell'Oro／LightCounting 證實；2026 年無新數）"},{"item":"光模組可插拔市場","value":"單位數 2026 年 6,000 萬→2030 年 1.75 億（CEO 引第三方預測，年化約 31%）；AEC 屬其中 1–7 公尺段"},{"item":"第二、三條曲線","value":"ALC（微發光體線纜，至 30 公尺）與 OmniConnect（記憶體扇出，每顆 GPU 2,000–3,000 美元內容價值）FY28 起營收；CEO 稱各為數十億美元機會（公司自述）"},{"item":"營業利益池占比","value":"5 年前與現在的利潤池占比事實表未涵蓋"}]},"moat":{"mechanism":"系統級整合與驗證：自有 SerDes／DSP＋韌體＋以客戶交換器與網卡實速壓測整條鏈路＋PILOT 遙測，換到的是可靠度溢價與世代內的重新認證成本","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價：非 GAAP 毛利率 Q1 68% 落在指引中點、Q2 指引 67%–69%、FY27 與 FY26 持平，未擴大也未縮；份額：AEC 份額估計 80%–88% 為 2025 年資料，2026 年無新數；最大客戶占比下降屬客戶分散，無 sourced 份額流失；同業 ROIC 差距與兩年趨勢事實表未涵蓋，只能以營益率差代替","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以營益率差代替","threats":[{"level":"🔴生態攻擊","text":"Marvell 推 AEC 產品並以 Golden Cable 生態讓線纜廠與客戶自帶 IP，目標是 Credo 核心市場；資本量級遠大於 Credo，屬破壞性競爭","p":"40%","evidence_refs":["competitive_share_entrants#1","customer_second_source#3"]},{"level":"🟡點對點","text":"客戶本就要多源（2024-12 法說 CEO 承認），Amphenol、Volex 經專利和解取得授權；Credo 以先送樣、先量產應對，至今無具名第二來源得標證據","p":"30%","evidence_refs":["customer_second_source#2"]},{"level":"🟡點對點","text":"CPO 可能在 1.6T 以後壓縮機櫃內 AEC；多數分析認為大規模部署在 2027–2029 之後，Credo 以 NPO／CPX、ALC 與矽光子 PIC 部分對沖，故不按架構替代扣分，但列為長期風險","p":"25%","evidence_refs":["substitute_technology#0","channel_business_model_shift#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（收購後周轉率下降，待驗）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是網路團隊、決策與付款是雲端資本支出；要解決的問題（AI 叢集連線閃斷讓 GPU 閒置）是需要不是想要，但付款端跟著資本支出循環——二手來源認為 2027 為高峰、之後增速降到 10% 以下"},{"item":"決策層級","level":"🟡","text":"替代在『單一叢集世代的連線方案』層級決定：Credo 做全鏈路驗證與韌體強化，世代內切換成本高；但客戶明說要多源，1.6T 換代正是重新評選窗口，切換成本只在世代內有效"},{"item":"價值鏈分配","level":"🟡","text":"上游 TSMC 單一代工且無長期產能合約，下游前四大客戶占 84%；68% 毛利靠可靠度溢價撐住，但兩端議價力都強，Marvell 讓客戶自帶 IP 是把價值往客戶與線纜廠移"},{"item":"社會容忍度","level":"🟢","text":"企業間零組件，價格不涉民生、不依賴監管授權；政策風險來自關稅與出口管制，屬成本與需求面，已列入供應鏈風險，不構成定價上限"}],"roiic":"無法量化（投入資本事實表未涵蓋）。方向：FY25→FY26 GAAP 營業利益由約 0.37 億（4.37 億×8.5%）增至約 4.45 億（13.35 億×33.3%），增約 4.08 億美元，同期自由現金流 4.07 億幾乎等於淨利 4.72 億，有機增量報酬極高；FY27 起新增資本以收購為主，報酬未實現","reinvest_rate":"有機（FY26）：淨利 4.72 億−自由現金流 4.07 億≈0.65 億，約淨利 14%（未含股份報酬加回，偏低估）；FY27 含 DustPhotonics 收購（Q1 現金減 6.79 億）與存貨增 0.62 億，單年再投資接近或超過一年稅後營業利益","endo_ceiling":null,"formula_note":"內生成長＝增量 ROIC×再投資率；事實表無資產負債表（只有 Q1 現金 7.64 億、存貨 3.13 億）與年度資本支出，天花板無法算出，標資料缺口"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","CRDO":67.07,"MRVL":52.21,"ALAB":75.13,"MTSI":56.54,"AVGO":68.77,"unit":"%"},{"metric":"營業利益率","CRDO":31.74,"MRVL":16.81,"ALAB":22.75,"MTSI":18.11,"AVGO":48.52,"unit":"%"},{"metric":"FCF 利潤率","CRDO":27.57,"MRVL":18.23,"ALAB":23.02,"MTSI":10.63,"AVGO":44.22,"unit":"%"},{"metric":"研發密度","CRDO":21.46,"MRVL":25.84,"ALAB":36.13,"MTSI":23.42,"AVGO":13.28,"unit":"%"}],"competitors":[{"name":"MRVL","gm":52.21,"om":16.81,"fcf_margin":18.23,"rd_intensity":25.84,"strategy_note":"直接攻 AEC（Alaska 產品＋Golden Cable 生態讓線纜廠與客戶自帶 IP），自稱 AEC 與 retimer 營收年增一倍以上；營益率 16.8% 但資本量級大，是最實際的第二來源","period":"TTM ending 2026-07-31（4季加總）"},{"name":"ALAB","gm":75.13,"om":22.75,"fcf_margin":23.02,"rd_intensity":36.13,"strategy_note":"retimer 與 scale-up 連接的正面對手，毛利率 75.1% 更高、研發密度 36% 更重，在 PCIe／UALink retimer 與 AEC 都在進攻","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MTSI","gm":56.54,"om":18.11,"fcf_margin":10.63,"rd_intensity":23.42,"strategy_note":"類比與光學驅動元件，毛利 56.5%、營益 18.1%，在主動銅纜與光學前端與 Credo 部分重疊，規模與毛利都落後","period":"TTM ending 2026-06-30（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"strategy_note":"垂直整合巨頭，營益率 48.5% 高於 Credo，DSP 與 CPO 路線都能施壓；是 Credo 光學元件業務最難打的對手","period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"量為主（客戶滲透＋新客戶＋埠數）＋價（800G→1.6T ASP 上移）＋併購（DustPhotonics 光學 PIC）；無回購","runway_years":"AEC 滲透率事實表未涵蓋；以光模組單位數 2026→2030 年化約 31% 與光學第二曲線推估 ≥5 年","runway_post_y5":"🟢","endo_ceiling_basis":"內生天花板無法以事實表算出（缺投入資本）；共識 FY27E→FY29E 非 GAAP EPS 年化 40.5%，缺口歸因於營業費用增速低於營收的利潤率擴張＋收購貢獻光學，兩者可歸因，但 FY29 依賴 2027 年後資本支出續增，保守視為超出","segments":[{"item":"AEC","value":"最大事業；FY24→FY25 翻倍以上、FY25→FY26 三倍以上（CEO）；FY27 新增營收約一半來自銅（AEC 與 retimer），1.6T AEC 於 FY27 下半年開始貢獻、FY28 放量"},{"item":"光學（DSP／PIC／ZeroFlap）","value":"FY27 >6 億美元，三條各 >1 億，下半年加速；DSP 與 PIC 為兩位數美元 ASP、ZeroFlap 為三位數"},{"item":"Retimer","value":"Q1 創紀錄；Screaming Eagle 100G 為主、Blue Heron 200G 開始貢獻"},{"item":"ALC／OmniConnect","value":"FY28 首批營收；目前無營收"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"FY26 GAAP EPS 0.29→2.51，營收年增 205.7%；屬營運槓桿期，往後無法延續"},{"signal":"股份報酬占營收 >5% 且逐年上升","lit":true,"evidence":"Q1 FY27 股份報酬占營收 18.4%；逐年趨勢事實表未涵蓋，以水準保守計亮"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":false,"evidence":"FY25 0.56、FY26 0.86，未連 2 年；Q1 FY27 營業現金流因備料季減，列觀察"},{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q1 非 GAAP 68%，Q2 指引 67%–69%"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"2026 年無份額資料，事實表未涵蓋"},{"signal":"替代技術壓縮可服務市場","lit":false,"evidence":"大規模 CPO 部署多數分析在 2027–2029 之後，尚未發生"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"回購","value":"無（CFO 2026-06-01：無募資或回購計畫）"},{"item":"股息","value":"無"},{"item":"收購","value":"Hyperlume（2025-10）、CoMira（約 2026-03）、DustPhotonics（2026-06，一來源稱 7.5 億美元）；Q1 現金減 6.79 億至 7.643 億"},{"item":"營運資金","value":"Q1 存貨增 0.622 億至 3.131 億（季增約 25%，高於營收季增 9.6%）"},{"item":"資本支出","value":"Q1 0.073 億美元，資本輕"}],"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"DustPhotonics 一來源稱約 7.5 億美元（現金＋股票＋績效獎金），2026-06 完成，Q1 才認列首筆 PIC 營收、FY27 指引 PIC >1 億；已實現報酬尚無法計算","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"無回購；CFO（2026-06-01）表示無募資或回購計畫","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數 FY25 約 1.80 億→FY26 約 1.88 億，年增約 4.6%；Q2 FY27 指引約 2.00 億，遠高於 1.5%","grade":"不過"}]},"valuation":{"basis":"非 GAAP 前瞻本益比（FY1／FY2）＋PEG，以 GAAP 營業利益比例對照","tier":"高成長 AI 連接半導體","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業前瞻本益比；以利潤率當倍數錨會跨口徑，承重的同業倍數列資料缺口"},"fwd_pe":34.32,"peg":0.85,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"非 GAAP 前瞻本益比 34.3 倍、FY2 22.3 倍，PEG 約 0.85 看似便宜；但分母排除占營收 18.4% 的股份報酬，GAAP 對照約 66 倍；P/S 25.6 倍在四個年度端點的 97.9 分位；Base 五年終點約 310 美元、年化約 7%，低於 12% 的進場要求——合理偏貴，不到泡沫；五年分位資料缺口（只有 2–4 個年度端點）","upside_short_pct":2,"upside_mid_pct":43},"trap_analysis":{"verdict":"🟡","label":"成長陷阱風險中等：股份報酬偏高與營運槓桿期兩訊號亮，需求未見反轉，但價格已預支 FY28"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"二手來源認為雲端資本支出 2027 見頂、之後增速 <10%；Marvell 以產品與生態攻 AEC；2026-09-10 管理層未回答 AEC 3–5 年持久性與價格壓力","assumption":"FY28–FY29 共識（9.69、12.45 美元）成立需要資本支出在 2027 後續增、且 AEC 份額與價格不掉","consequence":"FY29 EPS 落到 6 美元上下、倍數壓到 15 倍，股價約 100 美元，五年虧約 50%","ruling":"部分採納：Bear 機率定 30% 不往下壓，下行由資本支出與客戶多源兩個獨立因素驅動；與唯一致命點部分重疊（客戶份額流失），已回補進觸發器與停損指標","watch":"FY28 首次營收指引（約 2027-06）年增是否 ≥40%；最大客戶占比季變化","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#1","customer_second_source#3"],"fact_refs":["f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"論點成功但股東經濟變差","evidence":"Q1 股份報酬 0.88 億美元、占營收 18.4%、占非 GAAP 營益 38.1%；稀釋股數 FY25 約 1.80 億→FY26 約 1.88 億→Q2 FY27 指引約 2.00 億；CEO 表明會持續收購；ZeroFlap 自建模組可能拉低毛利率","assumption":"營收與非 GAAP EPS 達標就等於股東受益","consequence":"每股 GAAP 盈餘長期落後非 GAAP；若毛利率由 68% 滑到 63%，利潤率擴張這段成長缺口的歸因失效","ruling":"採納：估值以 GAAP 對照、非 GAAP 便宜論證不成立；資本配置判偏弱","watch":"稀釋股數每季增幅 >1.5%；GAAP 營益率 <25%；非 GAAP 毛利率 <66%","evidence_refs":[],"fact_refs":["f_kpi5_share_based_compensation","f_kpi3_gaap_operating_income","f_kpi4_gaap_operating_margin"]},{"view":"價格已反映太多","evidence":"26 週漲 81%、距前份五週漲 31.9%；P/S 25.6 倍在四個年度端點的 97.9 分位、EV/S 99.9 分位；前瞻本益比 34.3 倍；Q1 超預期仍跌約 9%","assumption":"市場已把 FY28 初單季 10 億美元營收當成基準","consequence":"Base 五年終點約 310 美元、年化約 7%，低於 12% 的進場要求；任何一季只符合指引就可能財報後下跌","ruling":"採納：不追價，等股價或證據其中之一追上","watch":"股價 ≤175 美元；Q2 FY27 財報營收、光學與毛利率","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_week26_return_pct","f_fwd_pe_latest"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 164.17 → 本次 216.55（+31.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=164.17","side_b":"本次 price_at_dd=216.55","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟢→🟡、均線 🟡→-。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟢→🟡、均線 🟡→-。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 164.17 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 164.17 美元：Bull 價 612.5、Bear 價 112，五年期望值 +98.2%，基準年化 13.4%，不對稱比 7.2","side_b":"本次情境、股價仍用 164.17 美元：Bull 價 602、Bear 價 102，五年期望值 +95.3%，基準年化 13.6%，不對稱比 5.87","ruling":"先換情境、股價不動：五年期望值少 2.9 個百分點，基準年化多 0.2 個百分點。不對稱比由 7.2 變為 5.87。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 164.17 美元：五年期望值 +95.3%，基準年化 13.6%，不對稱比 5.87","side_b":"本次情境、股價 216.55 美元：五年期望值 +48.1%，基準年化 7.5%，不對稱比 2.8","ruling":"再換股價、情境不動：起點價上漲 31.9%，五年期望值少 47.2 個百分點，基準年化少 6.1 個百分點，不對稱比由 5.87 降到 2.8。合計五年期望值比前份少 50.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與裁決（前份漂移）","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-09-04：股價 164.17、前瞻本益比約 26 倍、估值偏便宜、進場分批；機率 Bull 25／Bear 30、最大回撤 −60%","side_b":"本次：股價 216.55（五週 +31.9%）、前瞻本益比 34.3 倍；FY1 共識三個月只上修 2.9%，漲幅幾乎全來自倍數；估值轉為合理偏貴，改為等價格；機率維持 Bull 25／Bear 30，最大回撤改為 −45%～−65% 範圍","ruling":"價格走在證據前面：指引與毛利率和前份一致，變的是價格；裁決由進場改為不追、等價格，機率不因價格調整","evidence_level":"事實表價格與共識","settle_metric":"股價對 Base 五年終點的年化報酬（≥12% 才進場）","if_then":["若股價 ≤175 美元且 Q2 FY27 營收 ≥5.25 億、非 GAAP 毛利率 ≥66%→建首倉 2%","若股價續漲但 Q2 只符合指引下緣→不追","反向：若 Q2 光學季營收未見加速且股價仍 >200 美元→維持不建倉"],"evidence_refs":[]},{"axis":"基本面判斷（前份漂移，未變動欄）","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質評級 B、陷阱風險中、護城河方向持平、五年後跑道寬、品質複利成長型、非循環股","side_b":"本次維持：2026-09-10 高盛會議 CFO 給出 Q3 約季增 20%、Q4 約 30% 與 FY28 初單季 10 億美元目標，毛利率維持 68%；Marvell 競爭、客戶多源、股份報酬偏高等負面證據與前份同一批，未見新的份額流失或毛利率下滑","ruling":"新證據強化營收路徑、不改變護城河與陷阱判斷，各欄維持","evidence_level":"法說與投資人會議一手","settle_metric":"Q2 FY27 營收與非 GAAP 毛利率","if_then":["若 Q2 毛利率 <66%→護城河方向改判縮減並減碼","反向：若 2026 年出現 sourced 份額上升且毛利率擴大→護城河方向改判擴大"],"evidence_refs":["end_markets#0"]},{"axis":"重新進場與加碼條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"第二階：2026-11-30 Q2 FY27 光學季營收 ≥$120M 且非 GAAP 毛利率 ≥66% 且最大客戶 ≤35%；第三階：股價 ≤$135 且四項基本面檢核無損","side_b":"股價 ≤175 美元（Base 五年年化約 12%）且最近一季營收不低於指引下緣、非 GAAP 毛利率 ≥66%","ruling":"前份是已進場後的分階加碼條件；本次唯一約束是價格，改為單一價格條件＋基本面無損檢查，首倉與加碼都以此為準","evidence_level":"情境樹推算","settle_metric":"股價與最近一季營收、毛利率","if_then":["若觸及 175 美元且基本面無損→首倉 2%","反向：若觸及 175 美元但營收低於指引下緣→不買，等下一季"],"evidence_refs":[]},{"axis":"唯一致命點（Single Thing）","cause":"方法變動","prior_field":["single_thing"],"side_a":"null（前份未設定唯一致命點）","side_b":"最大客戶（Q1 FY27 占營收 33%）在 1.6T AEC 世代導入第二供應商並拿走 ≥30% 份額","ruling":"本次補設 Single Thing：客戶集中是情境樹最大的單一敏感度項；發生即減碼至半倉","evidence_level":"10-Q 客戶集中附註＋法說","settle_metric":"最大客戶占比與總營收季變化","if_then":["若最大客戶占比季減 ≥10pp 且總營收季減→減碼至半倉並凍結加碼","反向：若 1.6T 首批量產後最大客戶占比穩定且總營收季增→維持"],"evidence_refs":["customer_second_source#2","customer_concentration_credit#1"]},{"axis":"清倉／減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"null（前份未設停損指標）","side_b":"任一季營收低於指引下緣→減碼；非 GAAP 毛利率 <66% 連 2 季→減碼；最大客戶占比季減 ≥10pp 且總營收季減→減碼至半倉；FY27 光學 <4.5 億美元或 FY28 首次指引年增 <20%→清倉","ruling":"本次補設可量測的減碼與清倉指標，全部取自公司季報與法說","evidence_level":"公司揭露","settle_metric":"季營收、毛利率、客戶占比、光學營收","if_then":["任一指標觸發→依指標動作執行","反向：連續兩季全部正常→維持既定倉位上限"],"evidence_refs":["end_markets#2"]},{"axis":"財報超預期卻下跌","cause":null,"prior_field":null,"side_a":"Q1 營收 4.79 億高於共識 4.733 億、EPS 1.20 高於 1.17，毛利率 68% 在指引中點","side_b":"股價財報後跌約 9%，報導分別歸因光學指引低於期待與毛利率疑慮，兩說不一；Mizuho 稱 Q2 指引偏薄","ruling":"可調和：毛利率疑慮不成立（Q2 指引 67%–69%、FY27 與 FY26 持平），較可信的是市場要求的成長節奏高於指引；這支持本次『價格先於證據』的判讀","evidence_level":"二手報導","settle_metric":"Q2 非 GAAP 毛利率與光學季營收","if_then":["若 Q2 毛利率 <67% 且光學未加速→下調 Base FY28 EPS 並維持不追","反向：若 Q2 營收 ≥5.35 億且全年 >85% 指引上修→上調 Base 路徑、進場價放寬至 190 美元"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"成長品質：獲利對現金","cause":null,"prior_field":null,"side_a":"Q1 非 GAAP 淨利 2.36 億美元、創新高","side_b":"Q1 營業現金流 0.902 億、季減 0.92 億；存貨增 0.622 億至 3.131 億，季增約 25% 高於營收季增 9.6%（CEO 稱為下半年供給提前備料）","ruling":"管理層一次性歸因，不採信也不否定，列為未證、監測；預登記：連 2 季存貨季增率高於營收季增率，或營業現金流低於非 GAAP 淨利一半，視為歸因證偽","evidence_level":"法說一手","settle_metric":"存貨季增率對營收季增率；營業現金流對非 GAAP 淨利","if_then":["若 Q2 存貨季增率仍高於營收季增率→停止加碼","反向：若 Q3 營業現金流回到非 GAAP 淨利 70% 以上→解除"],"evidence_refs":[]},{"axis":"管理層說到做到（前一季承諾對照）","cause":null,"prior_field":null,"side_a":"2026-06-01 法說 CFO：Q1 指引 4.65–4.75 億、上半年季增中個位數、全年營收 >80%、營業費用 +50%","side_b":"2026-09-01：Q1 4.79 億超過上緣、季增 9.6%；全年上調至 >85%；營業費用改 +55%（Q1 費用 0.952 億超過指引上緣）","ruling":"一致偏正：營收兌現且上修；費用上修屬研發加碼，營收仍比費用快約 50%（2026-09-10 CFO）","evidence_level":"法說一手","settle_metric":"Q2 營業費用是否落在 1.00–1.05 億","if_then":["若 Q2 費用再超指引上緣且營收只達下緣→下調 Base 利潤率假設","反向：若 Q2 營收超過指引上緣→維持 Base"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2 本益比 22 倍、FY3 17 倍，FY27→FY29 共識 EPS 年化 40.5%、PEG 約 0.85；JPM 與 Evercore 目標價 310、292 美元；共識三個月上修 2.9%","side_b":"共識為非 GAAP、排除占營收 18.4% 的股份報酬，GAAP 前瞻本益比約 66 倍；FY29 數字依賴 2027 年後資本支出；賣方平均目標價兩來源 216 與 263.6 美元，口徑不一，均值與現價相近","ruling":"⚖反駁：便宜只在非 GAAP 分母下成立；等價格的代價是可能錯過續漲，接受這個代價","evidence_level":"事實表＋二手","settle_metric":"Q2 FY27 營收、光學加速、毛利率","if_then":["若 Q2 財報後股價仍 >200 美元但營收 ≥5.35 億、光學加速、毛利率 ≥67%→以 1% 試單，不等價格","反向：若股價跌到 175 美元以下但 Q2 營收低於 5.25 億→不買，等 Q3"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q2 FY27 營收不低於指引下緣、Q3 指引約季增 20%","type":"假設驗證","maps_to":"H1","metric":"季營收與下季指引","threshold":"Q2 ≥5.25 億美元；Q3 指引中點 ≥6.0 億","action":"達標維持；未達減碼三分之一並下調 Base","source_freq":"財報新聞稿（季）","date":"2026-12","evidence_refs":["end_markets#0"]},{"n":2,"text":"光學季營收逐季加速且毛利率不被模組拉低","type":"假設驗證","maps_to":"H2","metric":"法說光學營收口徑、非 GAAP 毛利率","threshold":"非 GAAP 毛利率 ≥66%；FY27 光學 ≥6 億美元","action":"毛利率 <66% 連 2 季減碼","source_freq":"法說與新聞稿（季）","date":"2026-12","evidence_refs":["end_markets#1"]},{"n":3,"text":"最大客戶導入第二家 AEC 供應商","type":"Single Thing","maps_to":"R2","metric":"最大客戶營收占比與總營收季變化","threshold":"最大客戶占比季減 ≥10pp 且總營收季減","action":"減碼至半倉並凍結加碼","source_freq":"10-Q 客戶集中附註、法說（季）","date":null,"evidence_refs":["customer_second_source#2","competitive_share_entrants#1","customer_concentration_credit#0"]},{"n":4,"text":"客戶拉貨暫停使單季營收跌破指引","type":"風險","maps_to":"R1","metric":"季營收對指引下緣","threshold":"任一季營收低於指引下緣，或連 2 季季增 <5%","action":"減碼三分之一","source_freq":"財報新聞稿（季）","date":null,"evidence_refs":["end_markets#2","customer_concentration_credit#1"]},{"n":5,"text":"供給或關稅吃掉營收與毛利","type":"風險","maps_to":"R4","metric":"管理層對供給不足的歸因、毛利率季變化","threshold":"管理層歸因供給不足致營收低於指引，或毛利率季減 ≥2pp 且歸因關稅","action":"停止加碼","source_freq":"法說（季）","date":null,"evidence_refs":["geo_supply_chain#2","reg_tariff_export#0"]},{"n":6,"text":"股價回到 Base 年化 12% 的價位且基本面無損","type":"估值rearm","maps_to":"H1","metric":"股價、最近一季營收與毛利率","threshold":"股價 ≤175 美元且最近一季營收 ≥指引下緣、非 GAAP 毛利率 ≥66%","action":"建首倉 2%","source_freq":"每日股價＋季報","date":null,"evidence_refs":[]},{"n":7,"text":"Q3 FY27 驗證 1.6T AEC 開始貢獻後加碼","type":"加碼","maps_to":"H3","metric":"Q3 營收、1.6T AEC 營收是否出現","threshold":"已持首倉且 Q3 營收 ≥6.0 億美元、1.6T AEC 開始貢獻、毛利率 ≥66%","action":"加碼至 4%","source_freq":"法說（季）","date":"2027-03","evidence_refs":[]},{"n":8,"text":"FY28 首次展望顯示資本支出高峰後成長斷層","type":"減碼","maps_to":"R5","metric":"FY28 首次營收指引年增","threshold":"年增 <40%","action":"減碼至半倉","source_freq":"Q4 FY27 法說","date":"2027-06","evidence_refs":["supply_demand_durability#2"]},{"n":9,"text":"光學第二曲線失敗或成長斷崖","type":"清倉","maps_to":"H2","metric":"FY27 光學營收、FY28 首次營收指引","threshold":"FY27 光學 <4.5 億美元，或 FY28 首次指引年增 <20%","action":"清倉","source_freq":"Q4 FY27 法說與 10-K","date":"2027-06","evidence_refs":[]},{"n":10,"text":"機櫃內大規模 CPO 部署出現","type":"風險","maps_to":"R3","metric":"hyperscaler 具名 CPO 部署、AEC 營收年增","threshold":"具名機櫃內大規模 CPO 部署且 AEC 營收年增轉負","action":"減碼三分之一","source_freq":"產業新聞、法說（季）","date":null,"evidence_refs":["substitute_technology#0","channel_business_model_shift#1"]},{"n":11,"text":"Q4 FY27 財報與 FY28 展望後全面複審","type":"複審日期","maps_to":"H1","metric":"全部假設與停損指標","threshold":"到期即複審","action":"重跑完整研究","source_freq":"一次","date":"2027-06","evidence_refs":[]}],"kill_metrics":[{"metric":"季營收對公司指引下緣","bear_threshold":"任一季營收低於指引下緣（Q2 FY27 <5.25 億美元）→減碼","window":"逐季至 FY28","source":"公司財報新聞稿","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"<66% 連 2 季→減碼","window":"2026-12 起逐季","source":"公司財報新聞稿","last_status":"ok"},{"metric":"最大客戶營收占比與總營收","bear_threshold":"最大客戶占比季減 ≥10pp 且總營收季減→減碼至半倉","window":"逐季","source":"10-Q 客戶集中附註、法說","last_status":"ok"},{"metric":"FY27 光學營收","bear_threshold":"<4.5 億美元→清倉","window":"FY27 結束（2027-05）","source":"Q4 FY27 法說、10-K","last_status":"unknown"},{"metric":"FY28 首次營收指引年增","bear_threshold":"<20%→清倉；<40%→減碼至半倉","window":"2027-06","source":"Q4 FY27 法說","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=81.08, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但判斷者宣告 wait_for_price：不得把觀望承繼回進場（只往保守方向）","hit":false,"basis":"wait_for_price=True, prior_verdict='進場', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價 ≤175 美元（Base 五年年化約 12%）且最近一季營收不低於指引下緣、非 GAAP 毛利率 ≥66%","exec_line":"現價不追；觸及 175 美元且基本面無損→首倉 2%，Q3 FY27 驗證後加到 4%；已持有者續抱不加碼。回撤 −45%～−65% 屬預期內的深回撤，論點完整時不因跌幅砍倉，只依停損指標動作"},"reasoning":{"industry":"營收來源：AEC（最大）、retimer、光學 DSP／PIC／ZeroFlap，各分部金額公司未揭露（事實表未涵蓋），只知 FY27 光學 >6 億美元、FY27 新增營收約一半來自光學一半來自銅。Q1 FY27 營收 4.79 億美元、年增 114.7%，非 GAAP 毛利率 68%、非 GAAP 營益率 48.2%，GAAP 營益率 25.2%（差距主要是股份報酬）。錢卡在可靠度：同一條連線，Credo 把『連線閃斷造成 GPU 閒置』的成本（CEO 稱利用率損失可達 10%–20%）轉成溢價。單點依賴：前四大客戶占 84%、最大 33%、前兩大 61%；FY26 年底最大客戶占應收 53%；上游全部晶圓靠 TSMC 且無長期產能合約。供需持久性：結構性持久但有週期性反轉風險——叢集變大、速率往 1.6T 走是結構性，付款能力取決於 2027 年後雲端資本支出。產業態勢：雙向拉鋸——競爭惡化（Marvell AEC 產品與 Golden Cable 生態）對上結構轉好（多數分析認為大規模 CPO 部署在 2027–2029 之後，800G 世代銅取代光）。產業時鐘在擴張期：營收連七季三位數年增、Q2 指引續季增約 10%。","moat":"執行力 9：連七季三位數年增、Q1 營收超過指引上緣、五家 hyperscaler 深度合作、光學併購後數月即拿到兩家大廠設計案。定價力 8：非 GAAP 毛利率由 FY23 57.7% 升到 FY26 68.0%，TTM 毛利率 67.1% 高於 MRVL 52.2%、MTSI 56.5%，接近 AVGO 68.8%；營益率 31.7% 高於 MRVL 16.8%、ALAB 22.8%、MTSI 18.1%，低於 AVGO 48.5%。扣 Marvell 生態攻擊 1 分，等級 B。方向判持平：FY27 毛利率指引與 FY26 持平、2026 年無份額數據，不能標擴大；最大客戶占比由 FY25 63% 降到 33% 是客戶分散，不是 Credo 在該客戶份額流失，故不標縮減。2026-09-10 被問到 AEC 價格壓力時管理層未回應，列入觀察。報酬持續期：事實表沒有投入資本，當期 ROIC 與增量 ROIC 無法量化；FY26 自由現金流 4.07 億對淨利 4.72 億（0.86），代表有機成長幾乎不吃資本；FY27 起增量資本主要是收購（DustPhotonics 約 7.5 億）與備料，報酬待驗。","growth":"成長組成以量為主（現有客戶滲透、第五家 hyperscaler 與 NeoCloud、埠數增加），價為輔（800G→1.6T ASP 上移），併購補光學（DustPhotonics 的 PIC 在 Q1 開始認列），無回購。共識 EPS：FY27E 6.31、FY28E 9.69、FY29E 12.45（Koyfin，家數事實表未涵蓋），FY27E→FY29E 年化 40.5%；以 FY26 GAAP 稀釋 EPS 2.51 為基期的三年年化約 70%，但基期與共識口徑不同，會高估。缺口歸因：內生天花板算不出，共識成長可歸因到兩項——營業費用增速低於營收（FY27 費用 +55% 對營收 >85%，CFO 稱 FY28 回到 2:1）的利潤率擴張，以及收購貢獻光學 PIC；保守視為超過可驗證的再投資支撐。跑道：光模組單位數 2026→2030 年化約 31%，AEC 滲透率事實表未涵蓋；有 sourced 第二條曲線（光學 FY27 >6 億美元已在出貨），所以五年後跑道判寬。衰退訊號亮兩個：EPS 成長遠快於營收（營運槓桿期）、股份報酬占營收 18.4%。","governance":"現金轉換：FY26 自由現金流 4.07 億對淨利 4.72 億（0.86），FCF 率 30.5%；Q1 FY27 營業現金流 0.902 億、季減 0.92 億（備料），自由現金流 0.829 億。股份報酬 Q1 0.88 億美元、占營收 18.4%、占非 GAAP 營益 38.1%。稀釋股數 FY25 約 1.80 億（0.522 億÷0.29）→FY26 約 1.88 億（4.723 億÷2.51），年增約 4.6%，Q2 FY27 指引約 2.00 億（含收購股票對價）。現金去向：收購＞營運資金＞資本支出，回購與股息為零；CEO 表明會持續收購工程團隊與互補技術。三項計分：收購報酬尚無法評、回購不適用、稀釋不及格。","valuation":"現價 216.55 美元＝FY1 非 GAAP 本益比 34.3 倍、FY2 22.3 倍（216.55÷9.69）、FY3 17.4 倍（216.55÷12.45）；trailing GAAP 本益比 76.8 倍、P/S 25.6 倍。分母爭議：共識為非 GAAP、排除占營收 18.4% 的股份報酬，Q1 GAAP 營業利益只有非 GAAP 的 52%（1.207÷2.306），粗估 GAAP 前瞻本益比約 66 倍，PEG 0.85（34.3÷40.5）的便宜論證不成立。歷史分位：trailing 本益比只有 2 個年度端點、P/S 與 EV/S 只有 4 個，五年分位事實表未涵蓋；P/S 在四點中 97.9 分位、EV/S 99.9 分位。股價距前份五週漲 31.9%，同期 FY1 共識三個月只上修 2.9%，漲幅幾乎全是倍數。賣方目標價兩來源 216 與 263.6 美元口徑不一，均值與現價相近，不支持也不反對本判斷。短期（12 個月）以 Base FY28E 9.2×24 倍≈221 美元，約 +2%；中期以 Base 五年終點約 310 美元，約 +43%。","premortem":"空方最強數字：前四大客戶 84%、最大 33%；股份報酬占營收 18.4%、稀釋股數年增約 4.6%；P/S 25.6 倍處歷史年度端點頂部；Q1 超預期仍單日跌約 9%。歷史最大回撤事實表未涵蓋。管理層迴避紀錄：2026-09-10 被問 AEC 近期需求、3–5 年持久性與價格壓力，三題都未給量化答案；2026-06-01 未給光學各線金額與 1.6T 時程。陷阱風險中等：衰退訊號亮兩個，核心需求未見反轉。三視角反證見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺超大型雲端 AI 叢集的連線錢：AEC 銅纜系統（最大事業）＋retimer＋光學 DSP／矽光子 PIC／ZeroFlap 光模組；錢卡在『可靠度』這一節點，用自有 SerDes、韌體、全鏈路驗證與遙測換毛利，但前四大客戶占營收 84%","moat":"護城河方向持平：系統級可靠度讓毛利率四年由 57.7% 升到 68%，同業中只次於 AVGO；但 Marvell 以生態攻 AEC、客戶要多源，擴大的證據不足，縮減也未見 sourced 份額流失","growth":"跑道寬：AEC 隨 1.6T 與新客戶續長，光學是已在出貨的第二條曲線，ALC／OmniConnect 為 FY28 第三條；但 FY29 以後的成長率取決於 2027 年後雲端資本支出，共識路徑超出可驗證的再投資支撐","capital":"資本配置偏弱：不回購、不配息，現金拿去收購（DustPhotonics 約 7.5 億美元）與備料；股份報酬占營收 18.4%、稀釋股數年增約 4.6%，收購報酬尚未實現","valuation":"現價要求 FY28 單季營收朝 10 億美元兌現、FY29 EPS 約 12 美元，且五年後市場仍給 20 倍以上；營收路徑我大致信，2027 年後資本支出與客戶多源我不全信，Base 五年年化只剩約 7%，合理偏貴","how_wrong":"最可能看錯在兩處：把 2027 年資本支出高峰後的 FY28–FY29 當成線性延伸，以及低估客戶多源化對 AEC 量價的侵蝕；第三是用非 GAAP 數字看便宜而忽略持續稀釋"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"進場","prior_role":"衛星","wait_for_price":true,"wait_for_price_condition":"等股價 ≤175 美元（Base 五年年化約 12%）且最近一季營收不低於指引下緣、非 GAAP 毛利率 ≥66%；或 Q2 FY27 營收 ≥5.35 億且全年 >85% 指引上修時重新評估","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":216.55,"week26_return_pct":81.08,"consensus_rev_3m_pct":2.94,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"共識 EPS 為非 GAAP，排除占營收 18.4%、占非 GAAP 營益 38.1% 的股份報酬；Q1 GAAP 營業利益僅為非 GAAP 的 52%，以 GAAP 計前瞻本益比約 66 倍，非 GAAP 的便宜論證無效"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"product","event":"OCP 大會展示 ALC（微發光體線纜）","impact":"低","watch":"是否有具名客戶、FY28 量產時程是否維持"},{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q2 FY27 財報與 Q3 指引","impact":"高","watch":"營收 ≥5.25 億、Q3 指引是否約季增 20%、光學季營收、毛利率、最大客戶占比、存貨"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"Q3 FY27 財報","impact":"中","watch":"1.6T AEC 與 1.6T DSP 首批營收、營收 ≥6.0 億"},{"date":"2027-06","date_precision":"month","type":"guidance","event":"Q4 FY27 財報與 FY28 展望","impact":"高","watch":"FY28 營收年增是否 ≥40%；FY27 光學是否 >6 億"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,301B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRDO_20261012/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河等級 B，方向持平，最大威脅是 Marvell 的生態攻擊。</p>
<ul class="pts">
<li>護城河來源是系統級整合與驗證。Credo 有自有 SerDes 與 DSP、韌體，並用客戶實際的交換器與網卡在真實速率下壓測整條鏈路，再加上 PILOT 遙測。客戶換到的是可靠度，換掉它就要在同一世代內重新認證，所以世代內切換成本高。但切換成本只在世代內有效，1.6T 換代正好是重新評選的窗口。</li>
<li>執行力給 9。營收連七季三位數年增，Q1 營收超過指引上緣，與五家 hyperscaler 深度合作，光學併購後數月內就拿到兩家大廠的設計案。這是公司過去幾年最硬的證據，也是管理層可信度的來源。</li>
<li>定價力給 8。非 GAAP 毛利率 TTM 67.1%，高於 MRVL 的 52.2% 與 MTSI 的 56.5%，接近 AVGO 的 68.8%。營益率 31.7% 高於 MRVL 的 16.8%、ALAB 的 22.8%、MTSI 的 18.1%，但低於 AVGO 的 48.5%。扣掉 Marvell 生態攻擊 1 分，綜合分數 8.5，等級 B。</li>
<li>方向判持平。FY27 毛利率指引與 FY26 持平，2026 年沒有份額數據，所以不能標擴大。最大客戶占比由 FY25 的 63% 降到 33%，屬於客戶分散，沒有 sourced 證據顯示在該客戶的份額流失，因此也不標縮減。2026-09-10 被問到 AEC 價格壓力時管理層沒有回應，列入觀察。</li>
<li>最大威脅是 Marvell，機率 40%。Marvell 推 AEC 產品並以 Golden Cable 生態讓線纜廠與客戶自帶 IP，資本量級遠大於 Credo，自稱 AEC 與 retimer 營收年增一倍以上。第二層是客戶多源，機率 30%，Amphenol 與 Volex 經專利和解取得授權，但至今沒有具名第二供應商得標的證據。</li>
<li>架構替代風險 25%，列為長期風險而不扣分。CPO 可能在 1.6T 以後壓縮機櫃內的 AEC，多數分析認為大規模部署在 2027–2029 之後，Credo 以 NPO、CPX、ALC 與矽光子 PIC 部分對沖。報酬持續期的 ROIC 與增量 ROIC 因事實表沒有投入資本而無法量化，只能以 FY26 自由現金流 4.07 億對淨利 4.72 億的 0.86 間接判斷有機成長幾乎不吃資本。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```