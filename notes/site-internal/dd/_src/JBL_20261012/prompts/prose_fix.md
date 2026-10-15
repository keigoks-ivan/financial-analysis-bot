你是 stock-analyst v20 的**散文層（prose）agent**，標的 JBL（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JBL_20261012/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：JBL　日期：2026-10-12　archetype：None　前份裁決：2026-07-03　觀望｜條件式衛星持倉　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1702B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（436B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（855B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（784B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1249B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（1044B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1276B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2342B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3336B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2865B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1702           3709-5298      5 條（2–6 內）  
s3                  8000         436           5295-7564      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2888          8478-12112      5 條（2–6 內）  
s6                 11000        1044           6969-9956      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1276           1557-2224      3 條（2–6 內）  
s10                 5000        2342           1861-2658      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2865           2000-2135      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4629B；至少需散文≈40.37KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−58
−58%
−56%
−50%
−44%
−39%
−38
−38%
−16.8%
−15%
−10.3%
−2%
0
0.1
0.1%
0.27
0.3
0.4%
0.5
0.54
0.68
0.75
0.87
0.89
0.96
01
1
1%
1.04
1.3%
1.3
1.34
1.4
1.5
1.5%
1.56
1.6
1.61
1.69
1.78
1.92
2%
02
2
2.03%
2.03
2.31
2.5
2.6
2.7
2.9%
3
3%
03
3.2%
3.23%
3.4%
3.6
3.68%
3.7
3.80
3.8
3.8%
3.93%
4%
4
4.20
4.3%
4.59%
4.6%
4.66%
4.7
4.8%
4.82%
4.98%
5.0%
5%
5
05
5.03%
5.2%
5.29%
5.4%
5.41
5.49%
5.6%
5.65%
5.7%
5.8%
5.92
06
6%
6
6.1%
6.22
6.3
6.4%
6.5%
6.57
6.75
6.8%
7
7%
07
7.1%
7.25
7.33
7.8%
8
8%
08
8.8
8.8%
8.85%
9%
09
9
9.2%
9.23%
9.75
10%
10
10.5
11
11%
11.4
11.72
11.8%
11.95%
12
12%
12.5
12.70
12.76
13.10
13.1
13.5
13.8
13.81
14
14.5
15%
15
15.32
15.5
16%
16
16.06%
16.1
16.5
16.6
16.7
16.88
16.92
17
17.3
17.31
17.55
17.69
18
18.5
19.2%
19.7%
20%
20
20.2
20.57
20.69
21
21%
21.5
22%
22
22.17
22.2%
23
23.38
23.4
24%
24
24.5
25%
25
25.4
25.4%
25.6%
25.93
26
26.5
27
28
28%
28.5
29
29%
29.8%
30
30%
30.3%
31
31%
31.41
33
34
34%
35%
36%
37
38.6%
39
39.5%
40
40%
42
43%
45
45%
49
49%
50%
50
52%
53
54%
55
56
56%
58
58%
59%
60
60%
61
62
64
68
70
72
72%
74
75%
78
80%
82%
82
84
85
86%
90
90%
100%
100
106
106.16
110
110%
114
120
135
136
144
150%
170
170.5
175
186
200
221
230
240
243
256
289
298
298.02
300
306
306.28
319
333
340
341.3
347
359
375
377
380
384
400
427.5
430
440
441
445
482
640
740
2024
2025
2026
2027
20261012
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
{"meta":{"ticker":"JBL","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Jabil Inc."},"oneliner":"AI 機櫃、資料中心電源與液冷帶動 FY27 營收 +24%、core EPS +34%，資本支出低、回購穩定；但薄利代工的盈餘與倍數同綁 AI 資本開支循環，現價五年 Base 年化約 7%，等 240 美元以下或下半年利潤率兌現","thesis":{"H":[{"id":"H1","text":"AI 帶動的 FY27 成長能轉成利潤：營收約 445 億（+24%）、core 營業利益率 6.1%、core EPS 17.55","2y":"FY27 兌現指引，FY28 營收仍雙位數成長","5y":null,"10y":null,"threshold":"FY27 core EPS ≥16.7 美元（指引減 5%）且 II 部門營收 ≥243 億（指引減 5%）","source":"2026-09-30 Q4 FY26 法說 FY27 指引（CEO Dastoor、CFO Hebard）；每季 8-K 財報新聞稿","drift_rule":"季度實績對指引軌跡偏離連 2 季 ≥5% 削弱；連 3 季 ≥10% 反轉"},{"id":"H2","text":"資本輕與現金轉換在高成長下維持：淨資本支出 1.5–2% 營收、FCF 不低於 core 淨利、80% 以上回饋股東","2y":null,"5y":"FY2031 前淨資本支出 ≤2% 營收、股數每年淨減約 3%","10y":null,"threshold":"淨資本支出 ≤2% 營收、調整後 FCF 對 core 淨利 ≥90%、淨存貨天數回到 55–60 天","source":"年度 10-K 與 Q4 法說（FY26 淨資本支出 1.3%、調整後 FCF 15.32 億、轉換約 110%）","drift_rule":"TTM 指標連 4 季偏離門檻 ≥5% 削弱；連 6 季 ≥10% 反轉"},{"id":"H3","text":"工程主導的多元組合讓 JBL 成為結構性較高利潤的代工：core 營業利益率由 FY20 3.2% 升至 FY26 5.8%，下一個循環低點仍守得住","2y":null,"5y":null,"10y":"跨一個完整循環，core 營業利益率低點 ≥5%、高點 ≥6.5%","threshold":"營收衰退年度 core 營益率 ≥5.0%；FY2031 前出現 ≥6.5% 的年度","source":"2026-09-30 Q4 法說 CFO Hebard（FY20 3.2%→FY26 5.8%）；年度 10-K","drift_rule":"跨 2 個年度未達削弱；跨 3 個年度反轉"}],"R":[{"id":"R1","text":"記憶體與單一來源零件短缺拖慢 FY27 下半年產能爬坡，營收與利潤率低於指引","h_ref":"H1","clock":"⚡","threshold":"連 2 季營收或 core 營業利益低於指引下緣且歸因零組件→減碼","evidence_refs":["end_markets#4","geo_supply_chain#0"]},{"id":"R2","text":"客戶集中與自製化：前五大約 36%、單一客戶集中度高於同業（穆迪），第二家超大規模客戶 FY27 預期 ≥10%，客戶在評估自製","h_ref":"H1","clock":"🔥","threshold":"10-K 前五大 ≥45% 或單一客戶 ≥25%，或任一 ≥10% 客戶公開移轉專案","evidence_refs":["customer_second_source#1","customer_second_source#2","customer_concentration_credit#2"]},{"id":"R3","text":"FY28 後 AI 資本開支消化，約 400 萬平方呎新產能稼動率下滑","h_ref":"H3","clock":"🐢","threshold":"II 部門營收連 2 季年增 <+10%（發生機率 ≥50% 才大幅減碼）","evidence_refs":["ems_utilization_capex_cycle#1"]},{"id":"R4","text":"成長靠應付帳款與客戶預付款支撐，付款條件正常化時營運資金反向吸走現金","h_ref":"H2","clock":"🔥","threshold":"淨存貨天數連 2 季 >64 天，或 FY27 調整後 FCF <12 億美元","evidence_refs":["ems_roic_asset_turnover_benchmark#4"]},{"id":"R5","text":"中國據點、貿易爭端與在地化擴廠推高成本","h_ref":"H3","clock":"🐢","threshold":"core 營業利益率年減 ≥30 個基點且歸因關稅或在地化成本","evidence_refs":["reg_tariff_export#2","geo_supply_chain#2"]},{"id":"R6","text":"FDA 警告函（2026-08-27）升級，傷及製藥服務與醫療客戶信任","h_ref":"H3","clock":"⚡","threshold":"進口警示、同意令，或醫療與包裝指引下修 ≥5%","evidence_refs":["major_events#1","clinical_fda#0","product_recall_warning#0"]}],"single_thing":{"description":"任一 10% 以上營收客戶（最大資料中心客戶，或 FY27 預期成為 10% 客戶的第二家超大規模客戶）宣布把機櫃或儲存專案移轉自製或他廠，公司因此下修當年營收指引 20 億美元以上","why_fatal":"前五大客戶約 36%、AI 相關營收約五成，新產能又是為已承諾專案而建；少一個 10% 級專案，等於營收少約一成、新產能閒置、固定成本吸收惡化，EPS 跌幅估計是營收跌幅的 1.5–2 倍，倍數同時往代工常態回落","if_happens":"清倉，不等下一季確認","how_monitor":"每季法說的客戶與部門營收說法、年度 10-K 客戶集中度揭露、8-K 指引變動、超大規模客戶的自製或供應商轉移公告","probability":"12–24 個月約 10%"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.81,"peg_fy2":0.54,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":13.1,"FY2027E":17.69,"FY2028E":22.17,"FY2029E":25.93},"fy_end_month":8,"eps_basis":"core（non-GAAP）稀釋 EPS；FY2026A 由 FY27 指引 17.55 美元與 +34% 推回約 13.10；FY2027E–FY2029E 為 Koyfin 2026-10-08 共識，分析師家數事實表未涵蓋（Benzinga 目標價約 9 位）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JBL_20261012/scenario.json","archetype":{"primary":"EMS/ODM","secondary":null,"confidence":"高","fingerprint":"毛利率約 9%、營益率 5–6%、資產周轉約 1.6 倍、淨資本支出 1.5–2% 營收、前五大客戶 36%，盈餘隨終端資本支出循環"},"industry":{"clock_phase":"II","sd_verdict_source":"2026-09-30 Q4 法說：已承諾客戶需求填滿新增產能、需求能見度 12–24 個月（Matt Crowley）；Evertiq 2026-09：未找到 FY27 以後的需求預測。結論：週期性、反轉時點未定","bargaining":{"up":"記憶體與單一來源零件在短缺中由供應商主導分配，JBL 靠約 120 家策略供應商關係與客戶共同採購爭取配額","down":"超大規模客戶與大型車廠、醫療器材廠議價力強，存貨預付款與付款條件由客戶主導；穆迪稱單一客戶集中度高於同業","geo":"中國、墨西哥、印度、越南與美國 40 餘個據點；在地化貼近客戶但推高成本，關稅與中國資金匯出限制屬持續風險"},"profit_pool_dir":"AI 基建利潤池集中在晶片與雲端業者；代工環節份額小，但 JBL 往電源、液冷、部署服務移動，core 營益率六年升 2.6 個百分點","tam_table":{"expanded":false,"reason":"事實表未涵蓋可引用的 TAM、滲透率與利潤池占比數字，只有超大規模業者 AI 投資超過全球 EMS 年營收的定性描述，展開只會變成推估"}},"moat":{"mechanism":"專案層切換成本：設計階段介入＋受監管產業長認證＋液冷、電源、測試能力組合；不是產品定價權","execution":8,"pricing":4,"grade":"C","trend":"→","trend_evidence":"執行面擴大（core 營益率六年升 2.6 個百分點、資本支出強度減半）；定價面持平（毛利率約 9%，Celestica 營益率高 3.8 個百分點）；份額面 FQ3 縮減（追蹤同業組占比 22.2%→19.7%），但 Q4 隨產能上線、II 部門 +56% 追回。三者合併判持平","peer_na_reason":"同業 ROIC 只有聚合站讀數且定義不一，算不出可靠的報酬利差；改以營業利益率與資產周轉代替","threats":[{"level":"🟡","text":"Celestica 等同業在 AI 增量上成長較快，JBL 在追蹤同業組的營收占比一年內由 22.2% 降至 19.7%（點對點競爭，不涉架構替代）","p":"40%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"客戶評估自製與外包，加上單一客戶集中度高於同業（穆迪）；自製報導未具日期且摘要截斷，證據力弱","p":"20%","evidence_refs":["customer_second_source#2","customer_concentration_credit#2","customer_second_source#1"]},{"level":"🟡","text":"自動化工廠業者可能直接替超大規模業者營運產能（Bright Machines），目前只是可能性","p":"10%","evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端、車廠與醫療器材廠的產品與工程團隊，決策者與付款者是同一客戶的採購端，三個角色都成立；AI 推論帶動的儲存、網通、電源與冷卻是需要而非想要，FY27 有已承諾訂單填滿新產能（2026-09-30 Matt Crowley）。但急迫不等於持久：FY27 之後無外部需求預測，且外包或自製由客戶決定"},{"item":"決策層級","level":"🟡","text":"替代性要在單一專案層看：受監管產業認證週期長、專案常跑十年以上（Steve Borges），換廠需重新認證，切換成本高；資料中心端 6 個最大案中 4 個始於設計合作，但超大規模業者通常多家供應，且有評估自製的報導（未具日期、摘要截斷，證據力弱）"},{"item":"價值鏈分配","level":"🟡","text":"AI 基建價值鏈的利潤集中在晶片與雲端業者，JBL 毛利率約 9%、營益率 5–6%；記憶體與單一來源零件在短缺時由供應商主導分配（Frank McKay 稱分配跟著信任走）。正面是組合往電源、液冷、部署服務移動，core 營益率六年升 2.6 個百分點；負面是同環節的 Celestica 營益率高 3.8 個百分點"},{"item":"社會容忍度","level":"🟢","text":"JBL 賣的是代工與整合服務，不是終端必需品，價格不面對社會或政治上限；唯一相關的是資料中心用電與期中選舉後的法規走向，管理層稱 FY27–28 未見重大影響（Matt Crowley），列為監測"}],"roiic":31,"reinvest_rate":72,"endo_ceiling":22,"formula_note":"FY26 core 營業利益 20.69 億美元；FY25 約 16.1 億（營收 298.02 億×core 營益率 5.4%，後者由 FY26 5.8% 減 CEO 所稱 40 個基點推回）。增量稅後營業利益≈（20.69−16.1）×80%（core 稅率 20%）≈3.7 億。投入≈淨資本支出 4.7 億＋Hanley 收購 7.25 億＋營運資金增量（FCF 轉換約 110%，視為近零）≈12 億；D&A 事實表未涵蓋，把全部淨資本支出當成長投資，增量報酬約 31% 屬下限。稅後營業利益≈20.69×80%≈16.6 億，再投資率≈12÷16.6≈72%。內生上界≈31%×72%≈22%。這是單一上行年度，含稼動率回升的循環槓桿，持續性要打折。當期 ROIC 聚合站讀數 16%–30%、管理層 core ROIC 59%（公司口徑），定義不一，不作承重"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","JBL":9.23,"CLS":11.95,"FLEX":9.35,"SANM":9.01,"unit":"%"},{"metric":"營業利益率","JBL":5.03,"CLS":8.85,"FLEX":5.29,"SANM":5.49,"unit":"%"},{"metric":"FCF 利潤率","JBL":3.89,"CLS":3.33,"FLEX":3.68,"SANM":4.66,"unit":"%"},{"metric":"研發密度","JBL":0.08,"CLS":0.99,"FLEX":null,"SANM":0.26,"unit":"%"}],"competitors":[{"name":"CLS","gm":11.95,"om":8.85,"fcf_margin":3.33,"rd_intensity":0.99,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"FLEX","gm":9.35,"om":5.29,"fcf_margin":3.68,"rd_intensity":null,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"SANM","gm":9.01,"om":5.49,"fcf_margin":4.66,"rd_intensity":0.26,"period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（AI 機櫃、電源、液冷、半導體設備子系統）＋組合改善推升利潤率＋回購每年約 3%；併購為輔（Hanley 7.25 億）","runway_years":"事實表未涵蓋滲透率，算不出到 30% 滲透的年數；以已承諾訂單與 12–24 個月能見度計，高確信期約 2 年","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段：增量報酬約 31%×再投資率約 72%≈22%（FY26 單一上行年度，含循環槓桿）；共識三年 EPS 年化約 25.6%，超出約 3.6 個百分點，歸因淨回購","segments":[{"item":"Regulated Industries","value":"FY27 指引約 136 億美元（+7%）：車用與運輸約 50 億（+9%）、醫療與包裝約 56 億（+6%）、再生能源與能源基建約 30 億（+7%）；Q4 營收 34 億、core 營益率 5.8%"},{"item":"Intelligent Infrastructure","value":"FY27 指引約 256 億美元（+43%）：雲端與資料中心 175 億（+52%）、資本設備 42 億（+40%）、網通與通訊 39 億（+15%，其中網通約 +45–50%）；Q4 營收約 58 億、core 營益率 6.5%"},{"item":"Intelligent Devices & Robotics","value":"FY27 指引約 53 億美元（−2%）：Digital Commerce & Robotics 約 30 億（+11%）、Connected Living 約 23 億（−15%，主動退出低利潤專案）；Q4 舊分部營收約 14 億、core 營益率 7.1%"},{"item":"AI 相關營收","value":"FY26 約 144 億美元→FY27 指引約 221 億（+54%），占營收約 40%→50%；FY27 預期 5 家 AI 客戶年營收超過 10 億"}],"decay_signals":["核心市占近 12 個月縮減：亮——追蹤同業組營收占比 22.2%→19.7%（CSI Market，2026-06-30）","EPS 成長顯著高於營收成長：亮——FY27 指引 core EPS +34% 對營收 +24%","毛利率連 2 季年減：未亮——TTM 毛利率 9.23%，CEO 稱 FY26 毛利率 9.2% 較 FY20 升逾 200 個基點","FCF 對淨利低於 0.75 連 2 年：未亮——FY25 FCF 11.72 億對淨利 6.57 億，FY26 轉換約 110%","SBC 占營收超過 5% 且逐年上升：未亮——FY26 SBC 約 1.4 億，約占營收 0.4%","TAM 萎縮或被替代：未亮（Connected Living −15% 為主動退出）","產業倍數近 3 年系統性下移：未亮——P/S 與 EV/S 居自身四個年度端點最高","維護性資本支出占 FCF 超過 60%：事實表未涵蓋","停止投資新產能且營收 3 年內下滑：未亮","主力產品提價後銷量下滑：不適用（代工無自有定價）"],"trap_rating":"🟡（亮 2 條）"},"quality":{"three_year":[{"item":"營收","value":"FY23 347 億→FY24 289 億（−16.8%，含行動裝置業務出售）→FY25 298 億（+3.2%）→FY26 約 359 億（+21%）"},{"item":"GAAP 營業利益率","value":"FY23 4.59%→FY24 4.98%→FY25 4.82%"},{"item":"FCF 利潤率","value":"FY23 2.03%→FY24 3.23%→FY25 3.93%"}],"dupont":[{"item":"稅後營業利益率","value":"core 營益率 5.8%×（1−20% core 稅率）≈4.6%（FY26）"},{"item":"資產周轉","value":"約 1.6 倍（聚合站 2026-03-31；TipRanks 1.61、Value Research 1.56）"}],"ccc":[{"item":"現金循環天數（FQ3 FY26）","value":"5 天（前季 21、去年同期 24），應付天數 135、存貨天數 84"},{"item":"淨存貨天數（Q4 FY26）","value":"64 天（含存貨預付款），目標 55–60 天；毛存貨約 82 天"}],"financial_note":"成長資金主要來自應付帳款與客戶預付款，付款條件一旦正常化，營運資金會反向吸走現金","latest_quarter_note":"Q4 FY26 營業現金流 7.33 億、淨資本支出 1.92 億、調整後 FCF 5.41 億、回購 1.69 億、淨利息費用 0.87 億"},"governance":{"capital_returns":[{"item":"營業現金流（FY26）","value":"約 20 億美元（Q4 法說 CFO）"},{"item":"淨資本支出","value":"4.7 億美元，占營收 1.3%；FY27 指引 1.5–2%"},{"item":"併購","value":"Hanley Energy 約 7.25 億美元現金（2026-01-02 完成）"},{"item":"回購","value":"FY26 約 11 億美元；自 FY13 股數約 2.03 億→1.04 億，平均回購價 58 美元"},{"item":"股息","value":"殖利率約 0.1%，金額小"},{"item":"資產負債表","value":"負債約 34 億、現金約 17 億、負債對 core EBITDA 1.3 倍、總流動性約 61 億"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Hanley 7.25 億美元（2026-01-02 完成）；管理層稱雙位數利潤率並推升 II 部門 core 營益率，已實現增量報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"以現價計 core 追蹤盈餘殖利率約 4.3%（13.10÷306.28）、前瞻約 5.8%（17.69÷306.28）；10 年期殖利率事實表未涵蓋，只要高於約 3.8% 即不過，保守判未過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY26 SBC 約 1.4 億美元，約占市值 0.4%；股數自 FY13 約 2.03 億降至約 1.04 億，淨稀釋為負","grade":"過"}]},"valuation":{"basis":"core（non-GAAP）前瞻本益比為主、PEG 為輔；GAAP 追蹤本益比受非現金與一次性費用扭曲，不作主尺","tier":"大型 EMS（與 Celestica、Flex、Sanmina 同層）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比或 EV 倍數；終端倍數改以自身前瞻 17.3 倍與四個年度端點分位對照"},"fwd_pe":17.31,"peg":0.68,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 17.3 倍、FY28 13.8 倍、PEG 約 0.68 偏便宜；但 P/S 與 EV/S 都在自身四個年度端點最高、GAAP 追蹤本益比 85 分位，代表市場已計入 AI 組合改善，且 PEG 分母可能是循環高點；兩邊相抵判合理。比前份的偏貴改善，原因是股價跌約 10%、同期 FY27 與 FY28 共識上修 5–8%","upside_short_pct":8.8,"upside_mid_pct":25.4},"trap_analysis":{"verdict":"🟡","label":"循環高點分母風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"管理層為 FY27 新增約 400 萬平方呎產能；Evertiq 2026-09 未找到 FY27 以後的需求預測；FY24 營收曾 −16.8%（含業務出售）","assumption":"超大規模業者 AI 資本開支在 FY28–29 延續","consequence":"5 年後虧損 50% 最可能的故事：FY28–29 進入消化期，II 部門營收連季衰退、新產能閒置，core EPS 回到約 13.5 美元，倍數由前瞻 17 倍回到 10–11 倍，股價約 135–170 美元","ruling":"採納為 Bear 主路徑，機率 30%；不作為 Base，因為管理層稱新產能綁已預訂專案、II 部門資本支出約占營收 1%，閒置產能的固定成本負擔比重資產代工小。與唯一致命點部分重疊：客戶專案移轉是同一故事的單一公司版本","watch":"II 部門營收年增率（連 2 季低於 +10% 即減碼）、管理層對稼動率的說法","evidence_refs":["ems_utilization_capex_cycle#1","supply_demand_durability#3"],"fact_refs":["f_kpi9_guidance_fy2027"]},{"view":"論點失敗","evidence":"FDA 2026-08-27 對旗下 Pharmaceutics International（馬里蘭州 Cockeysville）發出 cGMP 警告函，涉調查不明差異、批次失敗與矯正措施不足；搜尋未見召回","assumption":"醫療與製藥是分散 AI 循環的穩定支柱","consequence":"若升級為進口警示或同意令，製藥服務受阻，並傷及醫療客戶對 JBL 品質系統的信任，醫療與包裝 FY27 指引約 56 億美元的 +6% 落空","ruling":"反駁為主：警告函限於單一製藥廠區，未見召回；但受影響營收金額與改善期限事實表未涵蓋，屬資料缺口。利空不足一季、是否已進賣方模型不明，影響揭露前凍結加碼","watch":"FDA 後續處分、10-Q 醫療營收揭露、Croatia 製藥廠進度","evidence_refs":["major_events#1","clinical_fda#0","product_recall_warning#0"],"fact_refs":[]},{"view":"論點失敗","evidence":"FY25 10-K 風險因素：與中國的貿易爭端已造成並可能造成不利影響；第三方摘要稱中國營運受資金匯出限制，2025 年 2 月起關稅墊高零件成本","assumption":"關稅與地緣成本可以轉嫁給客戶","consequence":"若無法轉嫁，core 營業利益率年減，FY27 的 6.1% 落空","ruling":"部分反駁：最高法院推翻 IEEPA 關稅，公司已開始收到退款並稱無重大影響（10-Q 2026-05-31）。不預測關稅走向，改以損益設閘：core 營業利益率年減 30 個基點以上且管理層歸因關稅或在地化成本，即停止加碼","watch":"季度 core 營業利益率年變化與管理層歸因","evidence_refs":["reg_tariff_export#2","geo_supply_chain#2","reg_tariff_export#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"FQ3 FY26 應付款 +82% 至 144 億、存貨 +58% 至 74 億，同期營收僅 +21%；現金循環縮短主要靠應付天數升到 135 天；Celestica TTM 營益率 8.85% 對 JBL 5.03%","assumption":"AI 營收照指引成長，同時現金轉換維持 100% 以上","consequence":"營收與 EPS 照計畫，但付款條件或客戶預付款正常化時，營運資金反向吸走現金，FCF 低於 core 淨利；同時要靠價格守份額，利潤率停在 6% 附近，增量報酬下滑","ruling":"部分採納：FY27 FCF 指引約 16 億美元已含營運資金增加，Q4 淨存貨天數降 4 天，目前不支持惡化；但存貨回歸期限已由 Q4 延到 FY27 內，列入出場指標","watch":"淨存貨天數、應付天數、FY27 調整後 FCF（低於 12 億即減碼）","evidence_refs":["ems_roic_asset_turnover_benchmark#4","ems_roic_asset_turnover_benchmark#3","competitive_share_entrants#0"],"fact_refs":["f_kpi6_adjusted_free_cash_flow","f_peer_cls_operating_margin_pct","f_peer_jbl_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"FY26 回購約 11 億、Hanley 收購 7.25 億、淨資本支出 4.7 億，合計超過營業現金流約 20 億；過去回購均價 58 美元，現價 306 美元","assumption":"回購持續創造每股價值","consequence":"以 core 追蹤盈餘殖利率約 4.3% 回購，對每股價值的增益遠小於過去；若同時舉債支應，循環下行時資產負債表彈性下降","ruling":"部分採納：負債對 core EBITDA 1.3 倍、總流動性約 61 億，短期無壓力；回購對每股盈餘的貢獻（約每年 3%）已計入 Base，不另給加分","watch":"淨負債變化、回購金額對 FCF 比例（連 2 年超過 100% 即警示）","evidence_refs":["ma_merger#0"],"fact_refs":["f_kpi6_adjusted_free_cash_flow","f_price_at_dd"]},{"view":"價格已反映太多","evidence":"P/S 0.89 倍、EV/S 0.96 倍都在自身四個年度端點最高，GAAP 追蹤本益比 31.41 倍居 85 分位；賣方目標價分歧（Goldman 482→375、UBS 430、Simply Wall St 6 月平均 441、Benzinga 9 月平均 377）","assumption":"市場會持續用 AI 受惠者而非代工常態給倍數","consequence":"若 FY28 後成長回到代工常態，倍數回落吃掉盈餘成長，五年報酬接近零","ruling":"部分採納：前瞻 17.3 倍、FY28 共識 13.8 倍並不極端，股價自 7 月跌約 10%、同期共識上修，估值壓力已部分釋放；但 Base 終端只給 15 倍、五年年化約 7%，不足以支持現在進場","watch":"前瞻 core 本益比；股價在 240 美元以下才重跑進場判斷","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_pe_current","f_fwd_pe_latest"]}],"max_dd":{"lo":-58,"hi":-38,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 341.3 → 本次 306.28（-10.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=341.3","side_b":"本次 price_at_dd=306.28","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式衛星持倉 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與報酬指標","cause":"價格變動","prior_field":["val","asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份（2026-07-03）：股價 341.3 美元，估值偏貴，Base 五年年化 5.2%、五年期望報酬 28%、上下檔比 2.7","side_b":"本次：股價 306.28 美元（−10.3%），估值改判合理；報酬指標由腳本依新情境重算（粗估 Base 年化約 7%）","ruling":"主因是股價下跌：以 FY27 共識計，前瞻倍數由約 20.2 倍（341.3÷16.88）降到 17.3 倍；同財年共識上修 5–8% 是次因，已歸入新證據條目","evidence_level":"事實表股價與共識快照","settle_metric":"前瞻 core 本益比","if_then":["若股價回到 340 美元以上而 FY27 指引未上修→估值結論回到偏貴，不追"],"evidence_refs":[]},{"axis":"情境與基本面判斷","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct"],"side_a":"前份：時機訊號 B、陷阱風險中、護城河方向持平、五年後跑道中；Bull 五年價 640 美元、Bear 230 美元；機率 Bull 30%、Bear 30%","side_b":"本次：時機訊號、陷阱風險、護城河方向、五年後跑道四項不變；Bull 終端約 740 美元（37×20 倍）、Bear 約 170.5 美元（15.5×11 倍）；機率 Bull 25%、Base 45%、Bear 30%","ruling":"新證據是 Q4 FY26 超指引與 FY27 指引（營收 445 億、core EPS 17.55，高於共識 16.92），把三條 EPS 路徑都墊高。Bull 機率降 5 個百分點，因為 Bull 需要 FY28–29 AI 再高成長，而 FY27 之後無外部需求預測、同業份額流失證據新出現；Bear 終端價下移，因為本次 Bear 明確寫入 FY28–29 盈餘回落與 11 倍，而不只是壓倍數","evidence_level":"一手（Q4 法說逐字稿、8-K）＋第三方（CSI Market）","settle_metric":"FY28 指引（2027-09）","if_then":["若 FY28 指引營收年增 ≥15% 且第三家超大規模客戶達 10 億級→Bull 機率回到 30%","若 FY28 指引營收年增 <5%→Bear 機率上調至 40%"],"evidence_refs":["competitive_share_entrants#0","capital_markets_pricing#0","supply_demand_durability#3"]},{"axis":"分類與方法","cause":"方法變動","prior_field":["archetype","cycle_position","max_dd_pct"],"side_a":"前份：公司類型與循環位置未判；最大回撤單點 −50%；裁決觀望、角色為條件式持倉","side_b":"本次：歸類電子製造代工，需求量循環位置判中循環；最大回撤改為區間 −38% 至 −58%；裁決與角色由決策矩陣依本輪輸入重算","ruling":"本輪流程要求代工類公司走需求量循環讀數，且回撤必須給區間；下緣加深是因為 Bear 情境納入盈餘回落，不是新增負面事件","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件（null）","side_b":"股價≤240美元（Base五年年化約12%）且FY27 core EPS指引不低於17美元時，重跑判斷後分批建立首倉","ruling":"觀望的約束是價格，所以重新進場條件就是價格約束的否定；附加指引條件只為防止在基本面轉壞時拿價格當理由進場；價格先漲而證據未到則不追","evidence_level":"本輪情境樹","settle_metric":"股價與 FY27 指引","if_then":["若股價≤240美元且指引維持→重跑判斷後分批建立首倉（≤3%）","若股價先漲破 380 美元但上半年利潤率未見年增→不追"],"evidence_refs":[]},{"axis":"出場指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設出場指標（null）；前份假設中的反轉門檻為 II 段連 2 季年增 <+10% 或 core 營益率連 4 季不升、前瞻本益比跌破 14 倍","side_b":"II 部門營收連 2 季年增 <+10%、FY27 core 營益率 <5.6%、淨存貨天數 >70 天或連 2 季 >64 天、前五大 ≥45% 或單一客戶 ≥25%、FY27 調整後 FCF <12 億、FDA 處分升級→減碼；唯一致命點發生→清倉","ruling":"沿用前份 II 段 <+10% 門檻，新增利潤率、存貨、集中度、現金流與 FDA 五條；前份前瞻本益比 14 倍門檻退休，改由情境樹 Bear 的 11 倍追蹤倍數承接，因為倍數是結果，不是基本面出場理由","evidence_level":"一手（Q4 法說、10-Q）","settle_metric":null,"if_then":["任一出場指標觸發→減碼一半","唯一致命點發生→清倉"],"evidence_refs":["ems_roic_asset_turnover_benchmark#4"]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"任一 10% 以上營收客戶（最大資料中心客戶，或 FY27 預期成為 10% 客戶的第二家超大規模客戶）宣布把機櫃或儲存專案移轉自製或他廠，公司因此下修當年營收指引 20 億美元以上","ruling":"Single Thing 選客戶專案移轉而非 AI 資本開支下修：後者是連續變數，已在 Bear 情境定價；前者是離散事件，在前五大客戶 36%、新產能綁專案的結構下是數學上最大的單一敏感度項，發生即清倉","evidence_level":"一手（10-Q 客戶集中度）＋第三方（穆迪）","settle_metric":"指引變動與客戶揭露","if_then":["若發生→清倉","若 FY26 10-K 單一客戶占比 ≥20%→Single Thing 機率上調至 15%"],"evidence_refs":["customer_concentration_credit#2","customer_second_source#1"]},{"axis":"假設門檻","cause":"新證據","prior_field":["thesis.H"],"side_a":"前份：H1 AI 營收每年 +40%，削弱＝AI 營收成長連 2 季 <+25%；H2 四大雲端資本開支每年 +20%，削弱＝2027 指引年增 <+15%；H3 前瞻本益比維持 18–23 倍，削弱＝跌破 16 倍、反轉＝跌破 14 倍","side_b":"本次：H1 FY27 core EPS ≥16.7 美元且 II 部門營收 ≥243 億；H2 淨資本支出 ≤2% 營收、FCF 對 core 淨利 ≥90%、淨存貨天數回到 55–60 天；H3 營收衰退年度 core 營益率 ≥5%、FY2031 前出現 ≥6.5% 的年度","ruling":"FY27 已有公司指引，門檻改用指引減 5% 直接驗證；雲端資本開支不在事實表、無法驗證，改由 II 部門營收承接；倍數門檻退休（理由見出場指標條目）。前份 H1 的 AI 營收成長門檻仍成立：FY27 指引 +54% 遠高於 +25%","evidence_level":"一手（Q4 法說 FY27 指引）","settle_metric":"FY27 季度實績","if_then":["若 FY27 Q1–Q2 累計 core EPS 低於指引軌跡 5% 以上→H1 削弱，停止加碼"],"evidence_refs":["end_markets#0","end_markets#1"]},{"axis":"存貨天數回歸期限","cause":null,"prior_field":null,"side_a":"2026-06-17 Q3 法說 CFO Hebard：扣除客戶預付款後存貨約 68 天，高於 55–60 天目標，歸因出貨時點，預期 Q4 回歸正常","side_b":"2026-09-30 Q4 法說 CFO Hebard：淨存貨 64 天仍高於目標，改稱在 FY27 期間逐步回到區間；毛存貨約 82 天，另有商品漲價與雲端資料中心存貨權重較高；Frank McKay 稱前提是客戶持續給存貨預付款","ruling":"可調和（程度差異：方向對、期限延後約一年）。不採信也不否定，列為未證：若 FY27 Q2 淨存貨天數仍高於 62 天，視為出貨時點歸因證偽","evidence_level":"一手（兩季法說逐字稿）","settle_metric":"淨存貨天數（含存貨預付款）","if_then":["若 FY27 Q2 淨存貨天數 ≤60 天→存貨疑慮解除，不再影響進場條件","若連 2 季高於 64 天或客戶減少存貨預付款→停止加碼，Bear 機率上調至 35%"],"evidence_refs":["ems_roic_asset_turnover_benchmark#4","ems_roic_asset_turnover_benchmark#3"]},{"axis":"份額流失與絕對成長","cause":null,"prior_field":null,"side_a":"CSI Market：JBL 在追蹤同業組的營收占比 22.2%→19.7%，FQ3 營收年增 11.8% 對同業 30.3%","side_b":"Q4 FY26：營收 +29%、II 部門 +56% 並超出 6 月指引約 9 億；CFO 稱本年度多數時間產能受限，Q4 產能提前上線；FY27 II 部門指引 +43%","ruling":"可調和（程度差異）：FQ3 落後有產能受限的具體原因，Q4 已追回；但 Celestica 營益率高 3.8 個百分點，代表同環節對手拿得更多，所以護城河方向判持平而非擴大","evidence_level":"第三方（單一資料商、同業範圍未揭露）對一手","settle_metric":"JBL 營收年增率對追蹤同業平均的差距","if_then":["若 FY27 連 2 季營收年增落後追蹤同業平均 10 個百分點以上→護城河方向下調為縮減，停止加碼"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"共識上修幅度的口徑","cause":null,"prior_field":null,"side_a":"事實表：FY1 共識近三個月上修 38.6%（12.76→17.69）","side_b":"舊快照的 FY1 是 FY26（Q3 法說指引約 12.70），新快照的 FY1 是 FY27（指引 17.55）；同財年比較，FY27 由 16.88 升至 17.69（約 +4.8%），FY28 由 20.57 升至 22.17（約 +7.8%）","ruling":"採 B 側：38.6% 是財年滾動造成的數字，實際上修動能是溫和的 5–8%；本判斷不以 38.6% 作為盈餘動能證據","evidence_level":"事實表兩份快照＋法說指引","settle_metric":"同財年共識 EPS","if_then":["若下一份快照 FY28 共識再上修 ≥5%→上修動能成立，Bull 機率可回到 30%"],"evidence_refs":[]},{"axis":"第三家超大規模客戶的說法","cause":null,"prior_field":null,"side_a":"2026-06-17 Q3 法說 CEO Dastoor：第三家超大規模客戶 FY27 約數億美元，FY28 快速擴大到 10 億以上","side_b":"2026-09-30 Q4 法說 CEO Dastoor：FY27 貢獻不大、之後機會更大，未重申 FY28 的 10 億","ruling":"可調和（措辭轉保守，並非否認）；不計入 Base 的 FY28 路徑，只計入 Bull","evidence_level":"一手（兩季法說逐字稿）","settle_metric":"FY28 指引中該客戶的規模說法","if_then":["若 2027-09 法說未把該客戶列為 10 億級→Bull 機率由 25% 降至 20%"],"evidence_refs":["customer_concentration_credit#4"]},{"axis":"現在就買的最強論證對觀望","cause":null,"prior_field":null,"side_a":"現在就買：FY27 指引高於共識（EPS 17.55 對 16.92），股價卻自 7 月跌約 10%、法說後盤前再跌約 4%；前瞻 17.3 倍、FY28 共識 13.8 倍；FY26 已有 4 家 AI 客戶年營收超過 10 億、FY27 預期 5 家，產能綁已承諾訂單；資本支出低、回購每年縮股約 3%；賣方平均目標價約 377 美元","side_b":"觀望：Base 終端價約 427.5 美元（FY31 core EPS 28.5×15 倍追蹤），對現價五年年化約 7%；倍數由追蹤 23.4 倍回到 15 倍，吃掉近一半盈餘成長；FY27 之後無外部需求預測，Bear 30% 機率對應約 −44%","ruling":"不可調和（買與不買方向相反），選 B 側。依據：約束是價格——要拿到約 12% 的 Base 年化，價格需在 240 美元以下；賣方目標價約等於 FY28 共識的 17 倍，本判斷不認為成長放緩後的代工能維持這個倍數。硬數據點：FY27 Q1 core 營業利益是否 ≥5.92 億，以及淨存貨天數","evidence_level":"一手指引＋本輪情境樹","settle_metric":"股價對 240 美元、FY27 上半年 core 營業利益率年增幅","if_then":["若股價≤240美元且 FY27 core EPS 指引 ≥17 美元→重跑判斷後分批建立首倉（≤3%）","若股價先漲破 380 美元但 FY27 上半年利潤率未見年增→不追","反向條件：若 FY27 Q2 起 core 營業利益率連 2 季年增 ≥40 個基點且 FY28 指引營收年增 ≥15%→Base 終端倍數上調至 17 倍，於 300 美元附近重跑判斷後分批建立首倉"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","capital_markets_pricing#3"]},{"axis":"Adani 合作的資本需求","cause":null,"prior_field":null,"side_a":"2026-06-17 Q3 法說 CEO Dastoor：被問合資或出資結構時未回答，稱尚無定案架構，FY28 才是有意義貢獻的起點","side_b":"2026-09-30 Q4 法說 CEO Dastoor：對與 Adani 的印度資料中心建置極度看好，仍未揭露結構；同場稱資本支出會接近營收的 1.5%","ruling":"可調和但未證：結構揭露前，不計入任何情境的盈餘，也不採信它與資本輕模式相容","evidence_level":"一手（兩季法說逐字稿）","settle_metric":"合作結構與出資揭露","if_then":["若揭露的出資使淨資本支出超過營收 2%→H2 削弱，停止加碼"],"evidence_refs":[]},{"axis":"FY27 利潤率承諾與全年形狀","cause":null,"prior_field":null,"side_a":"2026-06-17 Q3 法說 CEO Dastoor：對 FY27 core 營業利益率 6% 以上很有信心，同時承認新產能爬坡有影響","side_b":"2026-09-30 Q4 法說：FY27 指引 6.1%（+30 個基點）；Q1 指引中點約 5.65%（6.22 億÷110 億），營收上下半年約 45／55、利潤率後段加權；Q1 營收年化已約 440 億","ruling":"可調和：承諾在指引層兌現，但幅度只剛好過 6%，全年成果押在下半年爬坡，所以 H1 的驗證點落在 FY27 Q2–Q3","evidence_level":"一手（兩季法說逐字稿）","settle_metric":"FY27 上半年 core 營業利益率年增幅","if_then":["若 FY27 上半年 core 營業利益率年增不到 10 個基點→FY27 core EPS 路徑下修至 16.5 美元，H1 削弱、停止加碼"],"evidence_refs":["end_markets#4"]},{"axis":"醫療業務的一次性歸因","cause":null,"prior_field":null,"side_a":"2026-06-17 Q3 法說 CEO Dastoor：FY26 醫療預期下修 1 億美元，稱不重大","side_b":"2026-09-30 Q4 法說 CFO Hebard：醫療與包裝低於預期，歸因自動化設備延誤與客戶專案時點；分析師問 Croatia 是否延誤，Steve Borges 稱照計畫、FY28 全面量產；同期 FDA 對旗下製藥廠發出警告函","ruling":"管理層連續兩季把醫療落後歸為時點因素，不採信也不否定，列為未證；FY27 指引 +6% 是驗證點","evidence_level":"一手（兩季法說）＋FDA 公開警告函","settle_metric":"醫療與包裝營收年增率","if_then":["若 FY27 上半年醫療與包裝營收年增 <3%→時點歸因證偽，下修 Regulated Industries 成長假設並停止加碼"],"evidence_refs":["major_events#1"]}],"triggers":[{"n":1,"text":"FY27 Q1 財報檢驗利潤率爬坡起點","type":"假設驗證","maps_to":"H1","metric":"Q1 FY27 core 營業利益與營收","threshold":"core 營業利益 ≥5.92 億美元且營收 ≥106 億（指引下緣）","action":"未達→H1 削弱、停止加碼；達標屬預期內，不構成追價理由","source_freq":"每季 8-K 財報新聞稿","date":"2026-12","evidence_refs":[]},{"n":2,"text":"FY27 Q2 淨存貨天數回到目標區間","type":"假設驗證","maps_to":"H2","metric":"淨存貨天數（含存貨預付款）","threshold":"≤60 天","action":"連 2 季高於 64 天→停止加碼，Bear 機率上調至 35%","source_freq":"每季法說 CFO 揭露","date":"2027-03","evidence_refs":["ems_roic_asset_turnover_benchmark#4"]},{"n":3,"text":"10% 級客戶專案移轉並下修營收指引","type":"Single Thing","maps_to":"Single Thing","metric":"客戶專案移轉公告與營收指引變動","threshold":"任一 ≥10% 營收客戶移轉專案，且當年營收指引下修 ≥20 億美元","action":"清倉","source_freq":"事件驅動（8-K、法說、客戶公告）","date":null,"evidence_refs":["customer_second_source#2","customer_concentration_credit#2","customer_second_source#1"]},{"n":4,"text":"價格回到 Base 年化約 12% 的位置","type":"估值rearm","maps_to":"重新進場條件","metric":"股價與 FY27 core EPS 指引","threshold":"股價 ≤240 美元且指引 ≥17 美元","action":"重跑判斷後分批建立首倉（≤3%），不直接建倉","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":5,"text":"AI 資本開支消化訊號","type":"風險","maps_to":"R3","metric":"II 部門營收年增率","threshold":"連 2 季 <+10%","action":"減碼；取消進場條件","source_freq":"每季 8-K","date":null,"evidence_refs":["ems_utilization_capex_cycle#1"]},{"n":6,"text":"FDA 警告函升級","type":"風險","maps_to":"R6","metric":"FDA 對旗下製藥廠的後續處分","threshold":"進口警示、同意令，或醫療與包裝營收指引下修 ≥5%","action":"減碼；影響揭露前凍結加碼","source_freq":"事件驅動（FDA 網站、10-Q）","date":null,"evidence_refs":["major_events#1","clinical_fda#0","product_recall_warning#0"]},{"n":7,"text":"零組件短缺拖累交付","type":"風險","maps_to":"R1","metric":"季度營收與 core 營業利益對指引下緣","threshold":"連 2 季低於指引下緣且管理層歸因零組件","action":"減碼","source_freq":"每季 8-K 與法說","date":null,"evidence_refs":["end_markets#4","geo_supply_chain#0"]},{"n":8,"text":"FY26 年報客戶集中度","type":"風險","maps_to":"R2","metric":"前五大與單一最大客戶營收占比","threshold":"前五大 ≥45% 或單一客戶 ≥25%","action":"停止加碼，唯一致命點機率上調至 15%","source_freq":"每年 10-K","date":"2026-10","evidence_refs":["customer_concentration_credit#2","customer_second_source#1"]},{"n":9,"text":"關稅或在地化成本吞噬利潤率","type":"風險","maps_to":"R5","metric":"core 營業利益率年變化與管理層歸因","threshold":"年減 ≥30 個基點且歸因關稅或在地化成本","action":"停止加碼","source_freq":"每季法說","date":null,"evidence_refs":["reg_tariff_export#2","geo_supply_chain#2"]},{"n":10,"text":"成長落後同業擴大","type":"風險","maps_to":"護城河方向","metric":"JBL 營收年增率對追蹤同業平均的差距","threshold":"連 2 季落後 ≥10 個百分點","action":"護城河方向下調為縮減，停止加碼","source_freq":"每季（CSI Market 等第三方）","date":null,"evidence_refs":["competitive_share_entrants#0"]},{"n":11,"text":"FY27 Q1 財報後複審","type":"複審日期","maps_to":"全案","metric":null,"threshold":null,"action":"重跑判斷，檢查 H1、存貨與價格條件","source_freq":"一次","date":"2026-12-31","evidence_refs":[]}],"kill_metrics":[{"metric":"Intelligent Infrastructure 部門營收年增率","bear_threshold":"連 2 季 <+10%","window":"FY27 Q1 起每季","source":"公司季度 8-K 財報新聞稿","last_status":"ok"},{"metric":"FY27 全年 core 營業利益率","bear_threshold":"<5.6%（指引 6.1% 減 0.5 個百分點）","window":"FY2027（至 2027-08-31）","source":"公司 8-K 與法說","last_status":"unknown"},{"metric":"淨存貨天數（含存貨預付款）","bear_threshold":">70 天，或連 2 季高於 64 天","window":"每季","source":"季度法說 CFO 揭露","last_status":"warning"},{"metric":"前五大客戶與單一最大客戶營收占比","bear_threshold":"前五大 ≥45% 或單一客戶 ≥25%","window":"每年 10-K","source":"Jabil 10-K、10-Q 客戶集中度揭露","last_status":"ok"},{"metric":"FY27 調整後自由現金流","bear_threshold":"<12 億美元（指引約 16 億）","window":"FY2027","source":"公司 8-K","last_status":"unknown"},{"metric":"FDA 對旗下製藥廠警告函的後續處分","bear_threshold":"進口警示、同意令，或醫療與包裝指引下修 ≥5%","window":"2026-08 起 12 個月","source":"FDA 警告函資料庫、公司 10-Q","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=2.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價≤240美元（Base五年年化約12%）且FY27 core EPS指引不低於17美元時，重跑判斷後分批建立首倉","exec_line":"現在不追；價格條件成立→重跑判斷後分批建立首倉（上限 3%）；股價先漲但 FY27 上半年 core 營業利益率未見年增→不追；唯一致命點發生→清倉"},"reasoning":{"industry":"營收結構（2026-09-30 Q4 FY26 法說）：Regulated Industries 約 34 億（+9%，core 營益率 5.8%）、Intelligent Infrastructure 約 58 億（+56%，6.5%）、Connected Living & Digital Commerce 約 14 億（持平，7.1%）。FY27 指引：Intelligent Infrastructure 256 億（+43%，約占營收 58%；其中雲端與資料中心 175 億、資本設備 42 億、網通與通訊 39 億）、Regulated Industries 136 億（+7%）、Intelligent Devices & Robotics 53 億（−2%）。AI 相關營收 FY26 約 144 億（約四成）→FY27 約 221 億（約五成）。最新一季營收 106.16 億、core 營業利益 6.75 億（6.4%）、GAAP 營益率 5.7%，TTM 毛利率 9.23%。單點依賴：前五大客戶約 36%、78 家約 90%（10-Q 至 2026-05-31），未點名最大客戶；第三方彙整 FY25 單一客戶約 16% 營收、24% 應收（未對照原文）；CEO 預期第二家超大規模客戶 FY27 成為 10% 以上客戶；Apple 占比 FY21 22%→FY24 11% 已降。供需持久性：AI 基建需求在 FY27 有已承諾訂單填滿約 400 萬平方呎新產能，但 FY27 之後沒有外部需求預測，屬週期性、反轉時點未定的需求。景氣位置判擴張期：營收 FY26 +21%、FY27 指引 +24%，稼動率由約 75% 回升到約 80%，仍低於正常的 85–86%，尚未滿載過熱。產業態勢判雙向拉鋸：競爭面 Celestica 在 AI 增量上成長較快，JBL 在追蹤同業組的營收占比降 2.5 個百分點；結構面 AI 基建需求與客戶分散度改善；其他結構變數是 IEEPA 關稅遭推翻並開始退款、記憶體產能轉向 AI 造成其他終端市場零件吃緊。","moat":"機制：設計階段介入（6 個最大資料中心案中 4 個始於設計合作）＋受監管產業長認證週期（專案常跑十年以上）＋液冷、電源、測試能力組合，形成專案層的切換成本，而不是產品層的定價權。方向證據：正向是 core 營業利益率 FY20 3.2%→FY26 5.8%、淨資本支出占營收 2.9%→1.3%（Q4 法說 CFO）；負向是追蹤同業組營收占比一年內 22.2%→19.7%、FQ3 營收年增 11.8% 對同業 30.3%（CSI Market，同業範圍未揭露）。同業利差：TTM 營業利益率 JBL 5.03% 對 Celestica 8.85%（落後 3.8 個百分點）、Flex 5.29%、Sanmina 5.49%；同業 ROIC 只有聚合站讀數且定義不一（OpenCapital JBL 29.8%、Celestica 39.5%、Flex 19.2%；TipRanks JBL 16.06%），不作承重。利潤率創高要拆開看：結構性部分來自出售行動裝置業務與組合改善，週期性部分來自稼動率回升，殘差是 Hanley 雙位數利潤率的服務收入。評分：執行 8（連續超指引、產能提前上線），定價權 4（毛利率 9% 級、存貨預付與付款條件由客戶定）。當期報酬屬低利益率×高周轉：營益率約 6%、資產周轉約 1.6 倍，現金循環只有 5 天，靠應付天數 135 天撐起（10-Q 2026-05-31）。增量報酬與內生上界推導見持續期欄位。","growth":"成長組成以量為主（AI 機櫃、資料中心電源與液冷、半導體測試與設備子系統），組合往高利潤服務移動推升利潤率，回購每年約縮股 3%（FY26 回購約 11 億美元÷市值約 319 億）；併購只有 Hanley 7.25 億一筆。共識三年 core EPS：FY26 約 13.10 美元（FY27 指引 17.55 與 +34% 推回）→FY29 共識 25.93，年化約 25.6%（Koyfin 2026-10-08，家數事實表未涵蓋）。內生上界約 22%（見護城河段），缺口約 3.6 個百分點，可由淨回購約 3.4% 解釋，不需依賴重新評價。FY27 core EPS +34% 對營收 +24%，EPS 成長高出營收 10 個百分點，靠利潤率與回購，屬衰退訊號之一；另一條是追蹤同業組份額縮減，共 2 條亮燈。跑道：FY27 高確信（訂單已承諾）；FY28 管理層只說出場產能較高、看好，未給數字（2026-09-30 CEO），第三家超大規模客戶 FY28 達 10 億的說法在 Q4 未重申；Croatia 製藥廠 FY28 才全面量產；實體 AI 由 CEO 自稱目前部署可忽略。","governance":"FCF 對淨利：FY25 FCF 11.72 億對 GAAP 淨利 6.57 億（1.78 倍），FY26 調整後 FCF 對 core 淨利約 110%（CEO）；FY22 只有 0.27 倍，轉換率隨存貨與付款條件大幅擺動。SBC：FY26 約 1.4 億美元，約占營收 0.4%、core 營業利益 6.8%，股數淨減，沒有稀釋問題。FY26 現金去向：營業現金流約 20 億→淨資本支出 4.7 億、Hanley 收購 7.25 億、回購約 11 億、股息約 0.3 億；合計約 23 億，高於營業現金流，差額由資產負債表支應（期末負債約 34 億、現金約 17 億、負債對 core EBITDA 1.3 倍、總流動性約 61 億）。長期框架是 80% 以上調整後 FCF 回饋股東；FY27 指引 FCF 約 16 億，7 月新授權 15 億回購尚餘約 14 億。併購已實現報酬事實表未涵蓋，但 Hanley 為雙位數利潤率，被列為 II 部門 core 營益率 +60 個基點的來源之一。","valuation":"主尺用 core 前瞻本益比：17.31 倍（306.28÷FY27 共識 17.69）；FY28 共識 22.17 對應 13.8 倍。GAAP 追蹤本益比 31.41 倍被攤銷、股權報酬與重組費用拉高（GAAP 追蹤 EPS 約 9.75 對 core 約 13.10），不作主尺。歷史位置：P/S 0.89 倍、EV/S 0.96 倍都是自身四個年度端點最高，GAAP 追蹤本益比居 85 分位；事實表只有四個年度端點、不是五年連續序列，故不填五年分位。PEG：17.31÷三年共識 EPS 年化 25.6%≈0.68，帳面便宜，但分母建立在 AI 資本開支延續的上行年度。上檔：12 個月以 Base FY28 EPS 21.5×前瞻 15.5 倍≈333 美元（+8.8%）；3 年以 Base FY30 EPS 26.5×前瞻 14.5 倍≈384 美元（+25.4%）。賣方平均目標價約 377 美元（約 9 位，Benzinga），約等於 FY28 共識的 17 倍，與本判斷的差異在終端倍數而非盈餘。共識動能：事實表的近三月上修 38.6% 是財年滾動造成，同財年實際上修 FY27 約 +4.8%、FY28 約 +7.8%。同業倍數事實表未涵蓋，無法跨同業錨定。","premortem":"三個最強反駁點已併入反證紀錄：一、FY28 後 AI 資本開支消化、約 400 萬平方呎新產能閒置；二、成長靠應付帳款與預付款撐，Celestica 以較高利潤率拿走增量；三、P/S 與 EV/S 已在自身最高。衰退訊號亮 2 條，陷阱風險中等。"},"plain":{"six":{"how_it_makes_money":"賺的是複雜製造、供應鏈整合與工程服務的加工利差：FY26 營收約 359 億美元、core 營業利益率 5.8%；錢卡在客戶端——超大規模雲端、車廠與醫療器材廠握有議價權，JBL 靠周轉、規模與認證黏著拿約 6% 的營業利益","moat":"護城河方向持平：工程早期介入與受監管產業認證讓執行面持續改善，但 AI 增量上成長落後 Celestica、利潤率也低於對方，定價權仍弱","growth":"五年後跑道中等：FY27 有承諾訂單與約 400 萬平方呎新產能撐住 +24% 營收，但 AI 基建滲透率與 FY28 以後需求都沒有可引用數字；實體 AI、共封裝光學、印度資料中心仍屬早期、未量化","capital":"資本配置紀律良好但邊際效益下降：FY26 調整後自由現金流 15.32 億美元、回購約 11 億，自 FY13 股數減少 49%；如今回購價位在 300 美元附近，盈餘殖利率約 4–6%，遠不如過去均價 58 美元的年代","valuation":"現價 306.28 美元等於 FY27 共識 core EPS 的 17.3 倍、FY28 共識的 13.8 倍；要划算，得 AI 營收在 FY28–29 再成長、利潤率站穩 6% 以上，且市場在成長放緩後仍給 15 倍以上——第一項我大致相信，最後一項不確定，所以判合理、不便宜","how_wrong":"最可能錯在把上行年度當常態：AI 資本開支一旦消化，薄利代工的盈餘與倍數會同時下修；次要風險是營運資金反轉與客戶集中"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤240美元（Base五年年化約12%），且FY27 core EPS指引不低於17美元","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"EMS/ODM","price_at_dd":306.28,"week26_return_pct":2.31,"consensus_rev_3m_pct":38.64,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY28–29 共識 EPS（22.17、25.93）建立在 AI 資本開支延續之上，可能是循環高點分母，PEG 0.68 的便宜論證不成立；另事實表 FY1 共識近三月上修 38.6% 是財年滾動（舊 FY1 為 FY26 的 12.76、新 FY1 為 FY27 的 17.69），同財年實際上修僅 FY27 約 +4.8%、FY28 約 +7.8%"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"other","event":"FY26 年報 10-K 公布（客戶集中度與單一客戶占比）","impact":"中","watch":"前五大與單一最大客戶的營收及應收占比"},{"date":"2026-11","date_precision":"month","type":"regulatory","event":"美國期中選舉後資料中心相關法規走向（Q4 法說 Matt Crowley 點名）","impact":"低","watch":"是否出現影響 FY28 資料中心建置的法規"},{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q1 FY27 財報（指引營收 106–114 億、core EPS 3.80–4.20）","impact":"高","watch":"core 營業利益是否 ≥5.92 億、淨存貨天數是否續降"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"Q2 FY27 財報（季節性低點、利潤率爬坡起點）","impact":"高","watch":"core 營業利益率年增幅、淨存貨天數是否 ≤60 天、醫療與包裝成長"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"約 400 萬平方呎新增產能在 FY27 下半年進入較佳稼動","impact":"中","watch":"管理層對稼動率與下半年利潤率的說法"},{"date":"2027-09","date_precision":"month","type":"guidance","event":"Q4 FY27 財報與年度投資人說明（FY28 指引）","impact":"高","watch":"FY28 營收年增是否 ≥15%、第三家超大規模客戶是否達 10 億級"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,328B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JBL_20261012/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期（§5.R／§5.F）</h2>
<p class="lead">護城河來自專案層切換成本，不是定價權，評為 C 級、方向持平。</p>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
<ul class="pts">
<li>護城河機制是設計階段介入、受監管產業的長認證，以及液冷、電源與測試能力的組合。這些形成專案層的切換成本，而不是產品層的定價權。執行面給 8 分（連續超指引、產能提前上線），定價權只給 4 分，因為毛利率停在約 9%，存貨預付與付款條件由客戶決定。</li>
<li>方向證據一正一負。正面是 core 營業利益率由 FY20 的 3.2% 升到 FY26 的 5.8%，淨資本支出占營收由 2.9% 降到 1.3%。負面是追蹤同業組的營收占比一年內由 22.2% 降到 19.7%，FQ3 營收年增 11.8%，同業則是 30.3%（CSI Market，同業範圍未揭露）。</li>
<li>份額縮減有具體的解釋。管理層稱 FY26 多數時間產能受限，Q4 產能提前上線，Intelligent Infrastructure 部門營收 +56%，超出 6 月指引約 9 億美元。三面合併後判持平，不判擴大，因為 Celestica 的營業利益率比 JBL 高 3.8 個百分點。</li>
<li>同業利差用營業利益率代替 ROIC。TTM 營業利益率 JBL 5.03%，Celestica 8.85%，Flex 5.29%，Sanmina 5.49%。同業 ROIC 只有聚合站讀數且定義不一（OpenCapital 對 JBL 是 29.8%，Celestica 是 39.5%，Flex 是 19.2%），所以不作承重。</li>
<li>報酬持續期要打折。FY26 增量報酬約 31%，再投資率約 72%，推出內生上界約 22%。這是單一上行年度，含稼動率回升的循環槓桿。投入只計淨資本支出、Hanley 收購與近零的營運資金增量，所以 31% 是下限，但持續性仍須打折。</li>
<li>當期報酬屬低利益率乘高周轉。營業利益率約 6%，資產周轉約 1.6 倍，現金循環只有 5 天，卻靠應付天數 135 天撐起。管理層口徑的 core ROIC 為 59%，定義與聚合站不同，不作承重。</li>
<li>威脅清單有三項，都是黃燈。Celestica 等同業搶 AI 增量，機率 40%。客戶自製與集中度高於同業，機率 20%。自動化工廠業者如 Bright Machines 直接替超大規模業者營運產能，機率 10%，目前只是可能性。</li>
</ul></section>

```