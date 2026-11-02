你是 stock-analyst v20 的**散文層（prose）agent**，標的 HLT（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HLT_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：HLT　日期：2026-11-03　archetype：None　前份裁決：2026-07-03　觀望｜條件式核心持倉　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2177B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（833B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（809B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1737B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（956B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（563B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（901B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2333B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3927B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3146B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2177           3376-4823      3 條（2–6 內）  
s3                  8000         833           5017-7167      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3502          8049-11498      5 條（2–6 內）  
s6                 11000         563          7306-10437      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         901           1819-2599      5 條（2–6 內）  
s10                 5000        2333           1867-2667      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3146           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5159B；至少需散文≈39.84KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−60
−55%
−50
−40
−40%
−38%
−5.6%
−5.4%
−5%
−2%
−1.5
−0.8%
0%
0
0.15
0.165
0.3%
0.4%
0.5%
0.6%
0.7
0.75
1%
1
1.1%
1.1
1.18
1.2
1.26
1.3
1.33
1.49
1.6%
1.6
1.7
1.72
1.8%
1.9
2
2%
02
2.1%
2.28
2.3
2.32
2.34
2.38
2.39
2.4
2.42
2.43
2.45
2.5%
2.5
2.7
2.73
2.9
3
03
3%
3.2
3.3
3.5
3.5%
3.9
4%
4
4.0
4.2%
4.4%
4.5%
4.5
4.6
5
5%
05
5.3
5.5%
5.6%
5.8%
5.9%
06
6
6.0%
6%
6.12
6.4%
07
7
7%
7.1%
7.2%
7.3
7.4
7.5%
7.7%
7.8
8
08
8%
8.1
8.2%
8.3
8.3%
8.4%
8.6
8.6%
8.89
9%
9.0%
09
9.0
9
9.01
9.07
9.09
9.13
9.5%
9.5
9.76
10.0
10%
10
10.2
10.3
10.45
10.58
10.7
11%
11
11.8%
12
12.0
12%
12.2%
12.5
13.4
13.8%
14
14.3
14.5%
14.6%
14.6
14.8
15
15%
15.6
15.7%
16.1
16.2%
16.2
16.4%
16.8
17.1%
17.13
18
18.94
19.44
19.5
20
20%
22
22.4%
23
23%
23.2%
23.4
23.9%
24.0%
24
25
25%
25.1%
25.1
25.5%
26
27
27%
27.3%
27.4%
28
28.2%
29
30
30%
30.1%
30.6%
31
31.0%
31.6
32.7%
33.25
33.7
34
34.8
34.85
35%
35
36%
36
36.4%
37%
38%
38
39.89
39.9
40%
40
40.7
45
45%
46
48
49
49.2
50
50%
52.7
54
54.3
57%
60%
60
70
75
87.7
90
100%
100
120.4
129.9
131.98
141.1
150%
156
187
216
226.6
227
234
300
330
338.12
342.3
356
364
364.18
397
400
456
585
648
668
810.3
824
2025
2026
2027
2028
2029
2031
20261103
1,000
2,000
2,500
3,000
3,400
5,900
543,100
6,000
7,000
8,200
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
{"meta":{"ticker":"HLT","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Hilton Worldwide Holdings Inc."},"oneliner":"輕資產收費模式加上業界最快的展店速度，生意本身好；但 40 倍預估本益比連部分靠舉債回購撐出的 EPS 成長也一起定價，基準情境五年年化約 6%，等股價回到 330 美元以下再談。","thesis":{"H":[{"id":"H1","text":"淨單位成長每年維持 6–7%：管線 54 萬間，2027 年開業約八成已在手，轉換案與國際低滲透補足新建的不足。","2y":"2027、2028 年 NUG 都在 6% 以上，管線不低於 50 萬間。","5y":null,"10y":null,"threshold":"NUG ≥6%（Q3 2026 為 6.0%）；管線 ≥50 萬間（2026-09-30 為 543,100 間）","source":"公司季報新聞稿與法說（NUG、管線、新建開工）；Lodging Econometrics 美國管線季報","drift_rule":"NUG 連 2 季低於 5% 為削弱，連 3 季低於 5% 為反轉；管線連 2 季季減，也列為削弱。"},{"id":"H2","text":"品牌 RevPAR 溢價加上 Honors 會員網路，讓業主願意付費、旅客願意直訂：費用收入每年成長 7% 以上，讓利後仍守得住。","2y":null,"5y":"2031 年前管理及特許費年複合成長 ≥7%，費用年增與 RevPAR 加 NUG 加總的差距不擴大到 3pp 以上。","10y":null,"threshold":"管理及特許費年增 ≥7%（Q3 2026 為 9.5%，CFO 法說）；與 RevPAR 加 NUG 加總的差距 ≤3pp（Q3 為 11.8% 對 9.5%，差 2.3pp）","source":"公司季報（管理及特許費、系統 RevPAR、NUG）；10-K 直訂通路與 Honors 揭露；RISE 2 方案公布（預計 2027 Q1）","drift_rule":"費用年增連 4 季低於 4% 為削弱（沿用前份）；差距連 4 季大於 3pp 也列為削弱，連 6 季為反轉。"},{"id":"H3","text":"資本回饋加內生成長，讓 EPS 維持雙位數複利：每年約 35 億美元回饋，股數每年淨減 3% 以上，槓桿守在 3.5 倍以內。","2y":null,"5y":null,"10y":"十年 EPS 年複合成長 ≥10%，其中淨回購貢獻約 3–4pp，內生約 7–9pp。","threshold":"年資本回饋 ≥30 億美元（2026 指引約 35 億）；淨負債÷調整後 EBITDA ≤3.5 倍（131.98 億 ÷ 2026 指引中點 40.7 億，約 3.2 倍）","source":"公司季報與 10-Q（回購金額、債務、EBITDA 指引）","drift_rule":"淨負債÷EBITDA 超過 4 倍，或回購年減逾 30%，即削弱（沿用前份）；跨 2 個年度成立為削弱，跨 3 個年度為反轉。"}],"R":[{"id":"R1","text":"美國景氣轉弱、非住宅投資循環反轉，RevPAR 轉負，40 倍倍數與 EPS 同時下修；中東、中國已是負成長，關稅與地緣衝突會加速這個過程。","h_ref":"H1／H3","clock":"⚡","threshold":"美國 RevPAR（CoStar 月度）連 2 個月年減 → 減碼評估（沿用前份）；系統可比 RevPAR 連 2 季年減 → 減碼至半倉","evidence_refs":["end_markets#1","geo_supply_chain#1","reg_tariff_export#0"]},{"id":"R2","text":"倍數溢價收斂：市場把預估本益比由 40 倍壓回 30 倍以下，是與基本面無關的純倍數風險；估值高的時候，管理層一貫的保守指引也可能被讀成成長放緩。","h_ref":"H2","clock":"🔥","threshold":"預估本益比跌破 30 倍而 FY+1 共識沒下修 → 屬倍數回歸，不減碼，列入分批買點；共識同時下修 ≥5% → 減碼至半倉","evidence_refs":["capital_markets_pricing#1"]},{"id":"R3","text":"利率高檔、回購靠舉債：每年約 15 億美元的回饋缺口靠 5.5% 新債補，利率高於 2.5% 的盈餘殖利率，回購推升 EPS 的效果會隨利息上升而縮小。","h_ref":"H3","clock":"🐢","threshold":"淨負債÷EBITDA >4 倍或利息覆蓋 <5 倍（沿用前份），需 ≥50% 機率成立才砍倉","evidence_refs":[]},{"id":"R4","text":"AI 代理成為新的訂房入口，導向 OTA 或另收通路費；直訂優勢被稀釋，業主分銷成本上升，Hilton 被迫再讓利。","h_ref":"H2","clock":"🔥","threshold":"公司揭露直訂占比下降，或 RISE 2 讓利超過 RISE（業主利潤率 75–100bp）→ 護城河降一級，重跑研究","evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"id":"R5","text":"營建成本與融資成本墊高，開發商擱置案子，NUG 只能靠轉換案撐，而轉換案比重本身已在高檔（Q3 為 37%，長期平均約 30%）。","h_ref":"H1","clock":"🔥","threshold":"新建開工年增轉負連 2 季，或簽約年減連 2 季 → H1 削弱","evidence_refs":["reg_tariff_export#1"]},{"id":"R6","text":"監管與制裁：英國 CMA 調查連鎖飯店是否透過 STR 資料共享價格資訊（尚無結論，未讀到原頁）；OFAC 制裁讓 Frankfurt City Centre 的租約於 2026-10-31 終止。兩者目前都未量化。","h_ref":"H2","clock":"🐢","threshold":"CMA 由初步調查轉為正式指控，或公布罰款 → 重估；因制裁終止的飯店合約累計 ≥3 家 → 風險升級","evidence_refs":["regulatory_antitrust#1","major_events#2"]}],"single_thing":{"description":"美國景氣衰退，讓 Hilton 系統可比 RevPAR 在 2027 或 2028 任一完整年度轉為年減。","why_fatal":"費用收入大致等於客房營收乘上抽成率。RevPAR 轉負會同時打斷「NUG＋RevPAR＋回購」這套成長算式：為了保住槓桿，回購會減速，EPS 從 9 美元以上掉到 8 美元以下，40 倍的倍數也會回到 20 倍出頭。這是情境樹中單一變數影響最大的一項：Bear 終點 −38%，谷底 −50～−60%。","if_happens":"已持有者減碼至三分之一；未持有者不接，等預估本益比回到 25 倍以下、RevPAR 年減幅收斂後再重跑研究。","how_monitor":"CoStar 美國週度與月度 RevPAR；公司季報的系統可比 RevPAR 與次年指引；美國非住宅固定投資季增率。","probability":"約 20%：CoStar 2026-08 預測 2027 年美國 RevPAR +2.1%，公司口頭給 2027 年全球 3–4%，兩者都是正數，但緩衝只有 2–4pp；中東與中國已是負成長。"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":34.85,"peg_fy2":2.39,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":9.13,"FY2027E":10.45,"FY2028E":12.0},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（扣特殊項目），與公司指引同口徑。共識取 Koyfin 2026-10-31 快照，未列家數（Chartmill 同期 FY2026 為 31 位）。FY2025A 調整後實際值事實表未涵蓋；年度表的 6.12 是 GAAP 稀釋 EPS，口徑不同，不填。三年共識只能算 FY2026→FY2028 兩年年化 14.6%。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HLT_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"輕資產收費平台：收入是抽成型費用，業主出資展店，自由現金流大量用於回購；需求面隨 RevPAR 景氣波動，所以信心給中。"},"industry":{"clock_phase":"II","sd_verdict_source":"供給面偏結構性持久，需求面屬週期性。供給：美國 2026 年 0.4%、2027 年 0.6%，在建量為 12 年低點（CoStar 2026-08），Lodging Econometrics 把 2027 年美國開業數由 824 家下修到 668 家。需求：靠商務差旅與非住宅投資，CoStar 預測 2027 年美國 RevPAR 只剩 +2.1%。供給低撐得住價格，撐不住需求反轉。","bargaining":{"up":"業主分散，沒有單一集中（10-K）；但業主利潤率多年被壓。Hilton 以 RISE 降費換取業主續建意願：忠誠度費用降 30bp，達品質門檻再降 50bp，約一半系統拿到。議價力小幅往業主移動。","down":"旅客與通路：Hilton Honors 2.43 億會員有會員價與點數折抵，用來導向直訂；B2B 端與 Navan 直連。但 OTA 占比十年大致不變（Skift 2026-05）。AI 代理目前占比可忽略（CEO），但可能改寫訂房入口。","geo":"美國以外客房約占 36%（2025）。中東非洲 2026 全年 RevPAR 預期低雙位數下滑，中國低個位數下滑；地緣衝突與 OFAC 制裁已讓 Frankfurt 一家租賃飯店退出。"},"profit_pool_dir":"往大品牌輕資產平台集中：Hilton 占全球供給約 5.6%，卻占在建客房近 20%；歐洲約 60% 是獨立飯店，轉換案是份額來源。營業利益池的歷史占比事實表未涵蓋。","tam_table":[{"item":"Hilton 占全球客房供給","value":"約 5.6%（Q3 法說 CEO；另一處說法為不到 6%）"},{"item":"Hilton 占全球在建客房","value":"近 20%，約為現有占比的 3.5 倍（Q3 法說）"},{"item":"開發管線","value":"543,100 間（2026-09-30，年增 5%），近一半已動工"},{"item":"歐洲獨立飯店占供給","value":"約 60%；Hilton 約占歐洲供給 2%（Q3 法說 CEO）"},{"item":"美國高品質客房占比","value":"約 25%（CEO 自估，未經第三方驗證）"},{"item":"段成長率","value":"美國產業供給 2026 年 0.4%、2027 年 0.6%（CoStar 2026-08）；Hilton NUG 指引每年 6–7%"},{"item":"營業利益池占比（5 年前→現在）","value":"事實表未涵蓋"}]},"moat":{"mechanism":"品牌帶來的 RevPAR 溢價＋Honors 2.43 億會員＋規模帶來的融資與分銷優勢，讓業主願意付費掛牌；系統越大，會員價值越高，再吸引更多業主，形成雙邊網路。","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行力擴大：NUG 6.0% 高於 Marriott 指引 4.5–5%；在建占全球近 20%，為現有占比的 3.5 倍；Q3 新建開工年增逾 40%；12 個月內從近 60 個品牌轉入。定價力穩定：CEO 稱品牌 RevPAR 溢價在 Q2 再擴大，但對業主以 RISE 讓利，key money 比例小升；Q3 費用年增 9.5%，比 RevPAR 加 NUG 的加總低 2.3pp。執行力擴大、定價力穩定，合併判為向上。","peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，以營業利益率與 FCF 利潤率差距代替；同業期間也不一致（Marriott、Choice 為截至 2026-06 的 TTM）。","threats":[{"level":"🔴","text":"AI 代理與對話式平台成為新的訂房入口，可能把直訂導回 OTA 或另收通路費，稀釋 Honors 的直訂優勢、墊高業主分銷成本。CEO 稱目前占比可忽略，且已與各平台直連；但 OTA 占比十年沒被搶回，說明通路權不在飯店手上。屬生態層攻擊，5 年內成形的機率約 30%。","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"對手以更優的管理與特許條件（含 key money）搶案，另有共享住宿替代。Hilton 在建客房中有 key money 的比例由約 9–10% 升到 11%，屬點對點競爭。","p":20,"evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（輕資產；投入資本口徑事實表未涵蓋，象限依商業模式與 14.5% 的 FCF 利潤率判讀）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是旅客，付款者是旅客或企業，Hilton 真正的付費客戶則是業主。業主要的是 RevPAR 溢價與訂房量，這個需求在 Q3 由商務散客 +8.3%、團體 +8.2% 撐住。但住宿是可延後的支出，休閒只成長 1.6%，需求又與非住宅投資循環高度連動（CEO）。急迫性高不等於持久性高，給黃燈。"},{"item":"決策層級","level":"🟢","text":"決策單位是每一家飯店的業主。12 個月內有近 60 個品牌的飯店轉進 Hilton，轉換案占 Q3 開業 37%，在建占全球近 20%，顯示在單一飯店層級，業主選 Hilton 的比例在上升。合約年限與解約條款事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈裡，業主出資本與營運成本，OTA 抽佣，Hilton 收費。CEO 承認業主多年利潤率受壓；Hilton 用 RISE 讓出約 75–100bp 的業主利潤率（Q2 法說），RISE 2 還要再讓，key money 比例也小升。Hilton 目前拿得多，但為了維持展店，未來每單位收費可能被慢慢擠壓。"},{"item":"社會容忍度","level":"🟡","text":"Hilton 收的是業主的費用，不是民生必需品的價格，社會容忍度問題主要落在房價與附加費上。FTC 垃圾費用規則與紐約市隱藏費用禁令屬全產業規範；英國 CMA 2026-03 調查連鎖飯店是否透過 STR 資料共享價格資訊，尚無結論（未讀到原頁）。目前不構成定價天花板，但監管方向在收緊，給黃燈。"}],"roiic":45,"reinvest_rate":23,"endo_ceiling":10,"formula_note":"內生成長＝增量報酬 × 再投資率。再投資只計資本支出加合約取得成本（含 key money），未扣折舊，營運資金變動事實表未涵蓋。分子分母同用毛額，兩者相乘等於稅後盈餘增量除以稅後營業利益，也就是用已實現的盈餘增速當上界，而且其中含業主出資帶來的成長，只能當量級參考。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","HLT":30.13,"MAR":19.81,"H":20.11,"CHH":50.59,"WH":null,"unit":"%"},{"metric":"營業利益率","HLT":24.01,"MAR":15.73,"H":7.21,"CHH":25.52,"WH":36.38,"unit":"%"},{"metric":"FCF 利潤率","HLT":14.49,"MAR":11.64,"H":6.35,"CHH":7.09,"WH":30.57,"unit":"%"}],"competitors":[{"name":"MAR","gm":19.81,"om":15.73,"fcf_margin":11.64,"strategy_note":"最大的直接對手。2026 淨客房成長指引 4.5–5%，低於 Hilton 的 6–7%；營業利益率 15.7% 較低，但兩家營收都含成本代墊，差距不能全算成護城河差距。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"H","gm":20.11,"om":7.21,"fcf_margin":6.35,"strategy_note":"偏高端與生活風格，資產較重，營業利益率 7.2%、FCF 利潤率 6.4%。Hilton 的奢華與生活風格是成長最快的兩塊（12 個月單位成長 11% 與 20%），雙方正面交鋒會加重 key money 競爭。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CHH","gm":50.59,"om":25.52,"fcf_margin":7.09,"strategy_note":"中低價位純特許，營業利益率 25.5% 與 Hilton 相近，但 FCF 利潤率 7.1% 只有 Hilton 一半；在中檔轉換案上，是 Hilton 的 Spark、Tempo 爭取業主時的對手。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"WH","gm":null,"om":36.38,"fcf_margin":30.57,"strategy_note":"經濟型純特許，營業利益率 36.4%、FCF 利潤率 30.6%，同業最高，主因是營收不含大量成本代墊；與 Hilton 客群重疊有限，不作主要對照。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主、價為輔，回購放大：NUG 6–7% 加 RevPAR 3–4%，構成約 9–10% 的費用成長；淨回購再為 EPS 加約 4pp；沒有併購。","runway_years":"≥29（以產業供給零成長計的下限）","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段的推導：增量報酬約 45% × 再投資率約 23%，約 10%；這個數字等同 Q3 實際稅後盈餘增速，只當量級參考。","segments":{"expanded":false,"reason":"分部營收與利潤事實表未涵蓋（需要 10-Q 分部表）。本次承重的成長來源是 NUG 與 RevPAR，已在成長驅動與情境路徑處理。自有與租賃飯店約 46 家且在大修（Q2 法說 CFO），分時度假授權費 Q3 低於預期，兩者都是拖累項目，已列入一次性歸因的監測。"},"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"季度序列事實表未涵蓋；年度 FY2024 27.4%、FY2025 28.2%，TTM 30.1%，未見下滑"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"NUG 6.0% 高於 Marriott 指引 4.5–5%，在建占全球近 20%"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"Q3 房價與住房率同步上升"},{"item":"EPS 成長顯著高於營收成長（差 >5pp）","lit":true,"note":"FY2027 共識 EPS 年增 14.5%，營收年增 8.6%，差約 6pp，主要來自回購"},{"item":"FCF÷淨利 <0.75 連 2 年","lit":false,"note":"FY2024 為 1.18 倍，FY2025 為 1.33 倍"},{"item":"SBC÷營收 >5% 且逐年上升","lit":false,"note":"Q3 約 1.8%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"需求面沒有萎縮；AI 代理屬通路威脅，已記在威脅清單，不重複計"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"本身倍數在四個年度端點中最高；同業歷史倍數事實表未涵蓋"},{"item":"維持性資本支出占 FCF >60%","lit":false,"note":"資本支出加合約取得成本年化約 5.3 億美元，約為 FY2025 FCF 19.44 億的 27%，且多屬成長性支出"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"營收由 FY2022 的 87.7 億增至 FY2025 的 120.4 億美元，管線創新高"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購：近 12 個月 8-K 無併購項目，資本回饋以回購為主，金額與資金來源已在本題推導寫明。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 無併購項目，事實表沒有併購事件","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購買入的盈餘殖利率＝1 ÷ 預估本益比 39.89，約 2.5%；門檻是 10 年期公債殖利率加 2%，10 年期事實表未涵蓋，但只有在 10 年期 ≤0.5% 時才會過；且部分回購由 5.5% 新債支應，判不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 5,900 萬美元，年化約 2.4 億，約占市值 0.3%；回購約占市值 4.2%，股數淨減少","grade":"過"}]},"valuation":{"basis":"預估本益比（FY2026 共識調整後 EPS）＋PEG","tier":"大型多品牌飯店集團，與 Marriott、IHG 同層；Choice、Wyndham 屬中低價位純特許，Hyatt 資產較重，不跨層當錨","peers":{"expanded":false,"reason":"同業現值倍數事實表未涵蓋；只能引用前份判斷記載的 7 月舊值（Marriott 約 30 倍、IHG 約 20 倍），不作承重錨。"},"fwd_pe":39.89,"peg":2.73,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"輸入：預估本益比 39.9 倍、PEG 2.7、trailing 本益比在四個年度端點中最高、股價高於賣方目標價均值；基準情境（終端 30 倍、FY2031 EPS 16.2）五年年化約 6%，機率加權約 4%，都低於 8%。五年高低點事實表未涵蓋，五年分位不計。結論：很貴。短期與中期上檔用基準路徑，倍數每年線性降 2 倍：一年後 38 倍 × FY2027 的 10.45，約 397 美元（+9.0%）；三年後 34 倍 × FY2029 的 13.4，約 456 美元（+25.1%）。一年看起來有 9%，是 EPS 年增 14.5% 抵掉倍數收斂的結果；拉長到五年，倍數拖累變大。","upside_short_pct":9.0,"upside_mid_pct":25.1},"trap_analysis":{"verdict":"🟡","label":"回購放大 EPS：EPS 成長比營收快約 6pp，估值卻按內生複利給到 40 倍"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"CEO 把需求連到非住宅固定投資循環，並稱未來兩年「擋不住」；但 CoStar 預測 2027 年美國 RevPAR 只剩 +2.1%。中東非洲 Q3 −5.6%、中國 −5.4%，10-K 與 10-Q 都把關稅與地緣衝突列為需求風險。","assumption":"需求循環不會在 2027–28 年反轉，RevPAR 維持正成長。","consequence":"RevPAR 轉負會同時打到 EPS 與倍數：EPS 谷底 7.8、倍數 22 倍，五年後股價約 227 美元，較現價 −38%，谷底 −50～−60%。這也是本次的 Single Thing。","ruling":"採納：Bear 機率維持 30%，不壓低。但不據此減碼，因為目前沒有任何需求轉弱的已實現數據（Q3 RevPAR +5.8%，FY2026 指引上修）。","watch":"CoStar 美國月度 RevPAR、公司季度 RevPAR 與次年指引、美國非住宅固定投資季增率","evidence_refs":["end_markets#1","geo_supply_chain#1","reg_tariff_export#0"],"fact_refs":["f_kpi4_system_wide_comparable_r","f_fwd_pe_latest"]},{"view":"論點成功但股東經濟變差","evidence":"NUG 6–7% 兌現，但 Q3 管理及特許費年增 9.5%，低於 RevPAR 加 NUG 的加總 11.8%。RISE 已讓出業主利潤率 75–100bp，RISE 2 將在 2027 Q1 再談，key money 比例小升；AI 平台可能把直訂導回 OTA（Skift、10-K）。同時回購在 40 倍下進行：FY2025 FCF 19.44 億，2026 回饋 35 億，缺口靠 5.5% 新債。","assumption":"展店帶來的費用增量不會被讓利吃掉，回購每花一塊錢仍能增加每股價值。","consequence":"若每間房收費持續被擠，費用成長會由 9–10% 降到 7–8%。在 2.5% 盈餘殖利率下回購、借 5.5% 的錢，回購越多，每股價值增幅越小；EPS 成長可能維持，股東報酬率卻下降。","ruling":"部分採納：回購買入殖利率不過，資本配置打折。費率讓利的證據還不夠，因為差距含中東獎勵費與分時度假授權費，列入監測，不改護城河等級。","watch":"每季管理及特許費年增與 RevPAR 加 NUG 的差距；RISE 2 讓利幅度；回購均價與新債發行","evidence_refs":["competitive_share_entrants#1","substitute_technology#1"],"fact_refs":["f_kpi5_net_unit_growth_yoy","f_net_debt_m","f_fwd_pe_latest"]},{"view":"價格已反映太多","evidence":"預估本益比 39.9 倍，trailing 49.2 倍在四個年度端點中最高；26 週漲 17.1%，FY1 共識同期只上修 1.1%；股價高於賣方目標價均值；10 月宣布轉上 Nasdaq、強調科技定位，敘事在推高倍數。","assumption":"市場願意長期用 40 倍買一家內生成長約 10%、其餘靠回購的收費公司。","consequence":"倍數回到 30 倍時，即使 EPS 照基準走，五年年化也只有約 6%；回到 25 倍，年化只剩約 2%。","ruling":"採納：估值很貴，不追價，等 330 美元以下。","watch":"預估本益比相對 FY+1 共識的變化；賣方目標價均值；FY+1 共識修正方向","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_week26_return_pct","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 338.12 → 本次 364.18（+7.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=338.12","side_b":"本次 price_at_dd=364.18","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式核心持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式核心持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🔴、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 338.12 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 338.12 美元：Bull 價 585、Bear 價 216，五年期望值 +31.0%，基準年化 8.2%，不對稱比 1.9","side_b":"本次情境、股價仍用 338.12 美元：Bull 價 648、Bear 價 226.6，五年期望值 +32.7%，基準年化 7.5%，不對稱比 2.32","ruling":"先換情境、股價不動：五年期望值多 1.7 個百分點，基準年化少 0.7 個百分點。不對稱比由 1.9 變為 2.32。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 338.12 美元：五年期望值 +32.7%，基準年化 7.5%，不對稱比 2.32","side_b":"本次情境、股價 364.18 美元：五年期望值 +23.2%，基準年化 5.9%，不對稱比 1.72","ruling":"再換股價、情境不動：起點價上漲 7.7%，五年期望值少 9.5 個百分點，基準年化少 1.6 個百分點，不對稱比由 2.32 降到 1.72。合計五年期望值比前份少 7.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"產業態勢三軸（一致判斷）","cause":null,"prior_field":null,"side_a":"結構轉好：美國供給 2026 年 0.4%、2027 年 0.6%，在建量為 12 年低點；Lodging Econometrics 下修 2027 年開業數；Hilton 管線 54.3 萬間，在建占全球近 20%。","side_b":"其他結構變數：AI 代理改寫訂房入口（10-K、Skift）、英國 CMA 調查價格資訊共享、FTC 與紐約市附加費規範。競爭面：10-K 提到對手可能給更好條件、key money 小升，但 Marriott NUG 指引 4.5–5% 低於 Hilton，看不到競爭惡化。","ruling":"雙向拉鋸：供給面結構性轉好，通路軸（AI 代理）正在變動，競爭面靜態且偏有利。兩者可調和：供給面撐住 2027–28 年的價格，通路軸是 5 年以上的變數。","evidence_level":"供給面為 CoStar、Lodging Econometrics 預測加公司實際數據；通路面為風險揭露與產業媒體","settle_metric":"美國年度供給成長；公司直訂占比（事實表未涵蓋）","if_then":["若公司揭露直訂占比下降或分銷成本率上升，通路軸改判為競爭惡化中，護城河降一級並重跑研究","反向：若有數據顯示 AI 代理直連讓直訂占比上升，定價力加一分"],"evidence_refs":["substitute_technology#0","regulatory_antitrust#1","competitive_share_entrants#1"]},{"axis":"供需預測分歧","cause":null,"prior_field":null,"side_a":"CoStar／Tourism Economics 2026-08：美國供給 2026 年 0.4%，RevPAR +4.4%；Hilton Q3 美國 RevPAR 實際 +7%。","side_b":"PwC 2025-12：2026 年供給成長將快於需求（少數意見）。","ruling":"採 A：PwC 是 2025 年底的事前預測，已被 2026 年實際 RevPAR 與 CoStar 8 月的供給數字推翻。屬時間差造成的程度差異，可調和。","evidence_level":"實際數據＋較新預測，對照舊預測","settle_metric":"CoStar 美國年度需求成長減供給成長","if_then":["若 CoStar 下一版把 2027 年美國需求成長預測降到低於供給成長，Bear 機率由 30% 提高到 35%","反向：若 2027 上半年美國 RevPAR 維持 +3% 以上，維持現行機率"],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#0"]},{"axis":"管理層指引與共識","cause":null,"prior_field":null,"side_a":"Q2 法說（2026-07-28）：Q3 EPS 指引 2.28–2.34，低於共識 2.42；分析師追問 Q2 超標為何沒有全額反映到全年，CFO 未量化。","side_b":"Q3 實際調整後 EPS 2.45，高於指引上緣與當時共識；全年 EPS 指引由 8.89–9.01 上調到 9.07–9.13。但 CEO（2026-10-27）說全年 EBITDA 原本可以上修 3,000 萬，實際只上修 1,000 萬，差額由中東與分時度假授權費各吃一半。","ruling":"可調和：管理層指引偏保守的慣性成立，Q4 指引 2.32–2.38 也這樣解讀。但「超標沒有全額流到全年」已連兩季出現，拖累項目在變多，這一點併入一次性歸因條目監測。","evidence_level":"公司指引與實際財報","settle_metric":"Q4 2026 實際調整後 EPS 對照指引 2.32–2.38","if_then":["若 Q4 實際低於 2.32，代表保守指引的慣性失效，Base 2027 EPS 下修 3%","反向：若 Q4 落在 2.38 以上，且 2027 指引 EPS 下緣 ≥10.3，維持 Base"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#0"]},{"axis":"管理層一次性歸因","cause":null,"prior_field":null,"side_a":"CEO（Q3 法說 2026-10-27）：中東、墨西哥、自有飯店翻修、HGV 授權費合計 6,000–7,000 萬美元以上的拖累屬一次性、非結構性，明年會正常化。","side_b":"拖累在擴大，不是收斂：Q2 法說時中東全年預期「高個位數到低雙位數下滑」，Q3 改為低雙位數下滑；中國由 Q2 說的「再降約兩個百分點」變成 Q3 單季 −5.4%；HGV 授權費到 Q3 才首次列為拖累；自有飯店部分，CEO 自己說要 2–3 年。","ruling":"不採信也不否定，標為未證、持續監測，並預先登記檢驗條件：若 2027 上半年兩季調整後 EBITDA 年增都低於 8%，且中東或 HGV 仍被列為拖累，一次性說法即證偽。屬程度差異，可調和。","evidence_level":"管理層說法，對照前後兩季法說","settle_metric":"2027 Q1、Q2 調整後 EBITDA 年增","if_then":["若證偽，Base 2027 EPS 由 10.45 下修到 10.0；重算後五年年化低於 5%，已持有者減碼至半倉","反向：若 2027 上半年 EBITDA 年增 ≥10%，Bull 機率由 25% 提高到 30%"],"evidence_refs":["end_markets#1","geo_supply_chain#1"]},{"axis":"2027 年需求口徑","cause":null,"prior_field":null,"side_a":"公司：CEO 稱美國底層成長由 Q2 估的約 2.5% 上調到約 4%，全球約 3.5%，2027 年全球 RevPAR 3–4%；大型團體飯店 2027 年預訂為中個位數成長。","side_b":"產業：CoStar 預測 2027 年美國 RevPAR +2.1%（需求 +1.1%、ADR +1.6%），且 2027 年 6 月受世足賽高基期影響為 −0.8%。","ruling":"可調和：公司講的是 Hilton 系統（偏商務與中檔、含國際），產業講的是美國全體，公司高 1–2pp 合理，但這是公司自估。Base 2027 用共識 EPS 10.45，我判斷隱含 RevPAR 約 3%，介於兩者之間。管理層一季內把底層成長從 2.5% 改口成 4%，方向向上但幅度大，打折採信。","evidence_level":"公司口頭展望，對照第三方預測","settle_metric":"2027 Q1 系統可比 RevPAR","if_then":["若 2027 Q1 系統 RevPAR 低於 +2%，Base 2027 EPS 下修到 10.2","反向：若 2027 Q1 ≥4%，Bull 機率提高 5pp"],"evidence_refs":["end_markets#2","end_markets#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：全球占比只有 5.6%，在建占 20%，NUG 6–7% 可延續多年；2027 年開業八成已在手；RevPAR 處擴張期，供給為 12 年低點；EPS 兩年年增 14.6%，FCF 轉換 1.2–1.3 倍。這種品質的收費公司過去少有便宜價，等 330 可能等不到。","side_b":"觀望方：40 倍已把 14.6% 的 EPS 成長全額定價，其中約 4pp 靠部分舉債的回購；基準五年年化約 6%，機率加權約 4%；股價在賣方目標價之上。","ruling":"選觀望方。好生意優先於好價格，但在現價下，最好的結果（Bull 年化約 12%）也只是中等，壞的結果（Bear −38%）機率 30%，不對稱比不到 2。等不到 330 的代價是錯過一段年化 6% 左右的報酬，可以接受。","evidence_level":"情境樹推導","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若股價跌到 330 美元以下且 NUG 指引 ≥6%，重跑研究後建首倉","反向：若股價續漲到 400 美元以上而 FY+1 共識上修未達 3%，維持不追"],"evidence_refs":[]},{"axis":"前份漂移：估值與裁決","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct"],"side_a":"前份（2026-07-03）：股價 338.12 美元，估值偏貴，綜合訊號 B，裁決觀望，機率 25／45／30。","side_b":"本次：股價 364.18（+7.7%），預估本益比 39.9 倍；FY1 共識近 3 個月只上修 1.1%，漲幅來自倍數。估值轉為很貴，綜合訊號維持 B，機率維持 25／45／30；裁決與角色由矩陣依本次輸入重算。","ruling":"估值結論轉嚴是價格造成的。基本面輸入（NUG、RevPAR、共識 EPS）比前份略好，但不足以抵銷倍數上升；機率不因價格調整。","evidence_level":"事實表的價格與共識快照","settle_metric":"預估本益比","if_then":["若股價回到 330 美元以下，估值結論回到偏貴，重跑研究","反向：若 FY2027 共識上修 ≥5% 而股價不動，估值結論同樣回到偏貴"],"evidence_refs":[]},{"axis":"前份漂移：分類與陷阱判讀","cause":"方法變動","prior_field":["trap","archetype","cycle_position","max_dd_pct"],"side_a":"前份：價值陷阱綠燈，未給公司類型與循環位置，最大回撤為單點 −55%。","side_b":"本次：逐條核對十類衰退信號，回購造成的 EPS 成長比營收快約 6pp 亮一燈，陷阱改為黃燈；公司類型定為品質複利成長（信心中）；循環位置仍不給，因為不屬循環類型，產業時鐘另記為擴張期；最大回撤改為 −40%～−60% 的範圍，由 Bear 谷底 EPS 與倍數推出。","ruling":"屬方法變動，不是基本面變差：EPS 與營收的差距前份就存在，本次才計入；用範圍表示回撤比單點更誠實。","evidence_level":"方法說明","settle_metric":"FY2027 EPS 年增減營收年增的差距","if_then":["若回購縮減讓兩者差距收斂到 5pp 以內，陷阱回到綠燈","反向：若再亮第二燈（例如季度毛利率連兩季年減），陷阱維持黃燈，並下修長期信心"],"evidence_refs":[]},{"axis":"前份漂移：護城河方向與跑道","cause":"新證據","prior_field":["moat_trend","runway_post_y5"],"side_a":"前份：護城河向上，五年後跑道寬。","side_b":"本次維持：Q3 管線 54.3 萬間（前份引用的是 Q1 的 52.7 萬），Q3 開業 2.7 萬間創紀錄，在建占全球近 20%，全球占比 5.6%。新增的負面證據（AI 通路、RISE 讓利）記在威脅與反證，不重複扣方向。","ruling":"新證據強化原判斷，值不變。","evidence_level":"公司季報與法說","settle_metric":"NUG 與管線","if_then":["若 NUG 連 2 季低於 5%，或管線連 2 季季減，護城河方向改為持平，跑道降為中","反向：若在建占比升破 25%，維持向上"],"evidence_refs":[]},{"axis":"前份漂移：重新進場條件（建首倉）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設（null）。","side_b":"股價 ≤330 美元（約 FY2027 共識 EPS 的 31.6 倍）且 NUG 指引維持 ≥6%：重跑研究後建首倉；≤300 美元且基本面無損：分批加碼第二筆。","ruling":"前份裁決觀望，但沒寫解除條件。本次把綁住進場的估值約束寫成可檢查的價位：在 330 美元，基準情境五年年化回到約 8%。","evidence_level":"情境樹推導","settle_metric":"股價；NUG 指引","if_then":["若觸發，重跑研究後建首倉，起始不超過目標部位三分之一","反向：若觸發時 NUG 指引已低於 6%，不建倉，改等下一季"],"evidence_refs":[]},{"axis":"前份漂移：減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份 kill_metrics 未設（null）。風險門檻原文：「system RevPAR 連 2 月轉負 → 減碼評估」；「溢價無新基本面支撐而持續 → 列為估值下行情境」；「net debt/EBITDA >4x 或利息覆蓋 <5x → 需 ≥50% 機率才砍倉」。","side_b":"本次新設：NUG 連 2 季 <5% 停止加碼，連 3 季減碼至半倉；系統 RevPAR 連 2 季年減，減碼至半倉；管理及特許費年增連 4 季 <4%，減碼至半倉；淨負債÷EBITDA >4 倍，停止加碼；NUG 指引下緣 <5% 且 RevPAR 連 2 季年減，清倉。倍數風險改為具體數字：預估本益比跌破 30 倍而共識沒下修，屬倍數回歸，不減碼；共識同時下修 ≥5% 才減碼。","ruling":"方法變動：前份只有方向性的風險描述，本次把減碼、清倉條件寫成數字；原本的 RevPAR 與槓桿門檻保留。","evidence_level":"方法說明","settle_metric":"公司季報","if_then":["任一減碼條件成立，依該條動作執行，不等複審","反向：條件全部未觸發，維持觀望，等價格條件"],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設（null）。","side_b":"Single Thing：美國景氣衰退，讓 Hilton 系統可比 RevPAR 在 2027 或 2028 任一完整年度年減；一旦發生，減碼至三分之一。","ruling":"前份沒有指定唯一致命點。本次選情境樹中單一變數影響最大的一項，因為它同時打到 EPS 與倍數。","evidence_level":"情境樹敏感度","settle_metric":"系統可比 RevPAR 全年年增","if_then":["若 2027 全年 RevPAR 指引下緣 <1%，Single Thing 機率由約 20% 上調到 30%，Bear 機率同步提高到 35%","反向：若 2027 上半年 RevPAR ≥3%，機率下調到 15%，Bear 維持 30%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 330 美元以下，NUG 指引仍 ≥6%：重跑研究後建首倉","type":"估值rearm","maps_to":"H1","metric":"股價；NUG 年度指引","threshold":"股價 ≤330 美元（約 FY2027 共識 EPS 的 31.6 倍），且 NUG 指引下緣 ≥6%","action":"重跑研究後建首倉，起始不超過目標部位三分之一","source_freq":"每日收盤價；季報","date":null,"evidence_refs":[]},{"n":2,"text":"價格續漲、證據沒跟上：不追","type":"估值rearm","maps_to":"R2","metric":"股價；FY+1 共識 EPS 修正","threshold":"股價 ≥400 美元，而 FY+1 共識三個月上修 <3%","action":"不追","source_freq":"每日收盤價；共識月度快照","date":null,"evidence_refs":[]},{"n":3,"text":"價格先跌、基本面沒壞：分批反買第二筆","type":"加碼","maps_to":"H1","metric":"股價；系統可比 RevPAR；NUG","threshold":"股價 ≤300 美元，且最近一季 RevPAR 年增 >0、NUG ≥6%","action":"分批反買第二筆","source_freq":"每日收盤價；季報","date":null,"evidence_refs":[]},{"n":4,"text":"展店放慢：NUG 跌破 5%","type":"假設驗證","maps_to":"H1","metric":"NUG 年增","threshold":"連 2 季 <5%（連 3 季為反轉）","action":"連 2 季停止加碼；連 3 季減碼至半倉","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#1"]},{"n":5,"text":"收費被擠：費用成長落後","type":"假設驗證","maps_to":"H2","metric":"管理及特許費年增；與 RevPAR 加 NUG 加總的差距","threshold":"費用年增連 4 季 <4%，或差距連 4 季 >3pp","action":"減碼至半倉","source_freq":"季報","date":null,"evidence_refs":["substitute_technology#1"]},{"n":6,"text":"美國需求轉弱","type":"風險","maps_to":"R1","metric":"美國 RevPAR（CoStar 月度）年增","threshold":"連 2 個月年減","action":"減碼至半倉","source_freq":"CoStar 月報","date":null,"evidence_refs":["end_markets#1"]},{"n":7,"text":"Single Thing：系統 RevPAR 全年轉負","type":"Single Thing","maps_to":"Single Thing","metric":"系統可比 RevPAR 全年年增","threshold":"2027 或 2028 任一完整年度 <0%，或年度指引下緣 <0%","action":"減碼至三分之一，預估本益比回到 25 倍以下再重跑研究","source_freq":"季報與年度指引","date":"2027-02","evidence_refs":["geo_supply_chain#1"]},{"n":8,"text":"槓桿上升","type":"風險","maps_to":"R3","metric":"淨負債÷調整後 EBITDA","threshold":">4.0 倍","action":"停止加碼","source_freq":"10-Q，每季","date":null,"evidence_refs":[]},{"n":9,"text":"AI 通路吃掉直訂","type":"風險","maps_to":"R4","metric":"直訂占比；RISE 2 讓利幅度","threshold":"直訂占比下降，或 RISE 2 讓利超過 RISE（業主利潤率 75–100bp）","action":"護城河降一級，重跑研究，停止加碼","source_freq":"10-K、法說","date":"2027-03","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":10,"text":"一次性拖累的說法被證偽","type":"假設驗證","maps_to":"H3","metric":"調整後 EBITDA 年增","threshold":"2027 上半年兩季都 <8%，且中東或分時度假授權費仍被列為拖累","action":"Base 2027 EPS 下修到 10.0；重算後五年年化 <5%，減碼至半倉","source_freq":"季報","date":"2027-07","evidence_refs":["end_markets#1"]},{"n":11,"text":"展店與需求雙雙破底","type":"清倉","maps_to":"H1","metric":"NUG 年度指引；系統可比 RevPAR","threshold":"NUG 指引下緣 <5%，且系統 RevPAR 連 2 季年減","action":"清倉","source_freq":"季報","date":null,"evidence_refs":[]},{"n":12,"text":"Q4 財報與 2027 指引複審","type":"複審日期","maps_to":null,"metric":"2027 年 RevPAR、NUG、EBITDA 指引與資本回饋金額","threshold":"RevPAR 指引下緣 <2% 或 NUG 下緣 <6%，即重跑研究","action":"重跑研究","source_freq":"年度","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"淨單位成長（NUG，年增）","bear_threshold":"連 2 季 <5%","window":"2 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"系統可比 RevPAR（幣別中性，年增）","bear_threshold":"連 2 季 <0%","window":"2 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"管理及特許費年增","bear_threshold":"連 4 季 <4%","window":"4 季","source":"公司季報與法說","last_status":"ok"},{"metric":"淨負債÷調整後 EBITDA","bear_threshold":">4.0 倍","window":"1 季","source":"10-Q 資產負債表與公司 EBITDA","last_status":"ok"},{"metric":"FY+1 共識 EPS 三個月修正","bear_threshold":"≤−5%","window":"3 個月","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把約 14.6% 的 EPS 成長當成內生複利，給到 40 倍；但內生上界約 10%，其餘約 4pp 來自回購，而回購有一部分用 5.5% 新債支應、買到的盈餘殖利率只有 2.5%；需求又處擴張期後段（2027 年美國 RevPAR 預測 +2.1%）。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='↑', week26=17.13, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Hilton 的 Bull 情境有展店量乘 RevPAR 加回購的骨架，12.2% 的年化隱含報酬也不高於 Hilton 過去的實現報酬，沒有明顯站不住。但缺口仍在：Bull 後段 RevPAR 假設缺來源，且與產業預測相反。我也找不到可比案例，全球占比與在建占比的口徑無法回溯到法說原文，所以 Bull 依據只算部分成立。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 330 美元以下（約 FY2027 共識 EPS 的 31.6 倍，基準五年年化回到約 8%），且 NUG 指引維持 6% 以上'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價 ≤330 美元（約 FY2027 共識 EPS 的 31.6 倍）且 NUG 指引維持 ≥6%","exec_line":"不追價。股價 ≤330 美元且 NUG 指引 ≥6%：重跑研究後建首倉；≤300 美元且最近一季 RevPAR 年增為正：分批加碼第二筆；續漲但共識沒跟上：不追。已持有者：美國 RevPAR 連 2 個月年減，減碼至半倉；系統 RevPAR 全年轉負，減碼至三分之一。"},"reasoning":{"industry":"收入結構：Q3 2026 營收 33.25 億美元，GAAP 營業利益 9.09 億（營業利益率 27.3%），調整後 EBITDA 10.58 億；TTM 毛利率 30.1%，營業利益率 24.0%。營收含大量代業主支付、再向業主收回的成本，所以帳面利潤率低估了收費本業。分部營收與占比事實表未涵蓋，法說可得的拆分如下：管理及特許費 Q3 年增 9.5%（CFO）；自有與租賃飯店剩約 46 家，正在大修，拖累 2,000–2,500 萬美元（Q2 法說 CFO）；分時度假（HGV）授權費 Q3 低於預期。量與價：Q3 系統可比 RevPAR +5.8%，其中商務散客 +8.3%、團體 +8.2%、休閒 +1.6%，NUG 6.0%；分區看，美國 +7%，中東非洲 −5.6%，中國 −5.4%。單點依賴：10-K 稱業主與加盟商沒有單一集中。真正的集中在美國（美國以外客房約占 36%）與商務差旅，CEO 自己把需求連到非住宅固定投資循環，這是景氣曝險，不是客戶集中。產業時鐘在擴張期：美國 RevPAR 由 2025 年約 −1.5～−2%（CEO）翻到 2026 年 Q3 的 +7%，供給成長 0.4%，在建量為 12 年低點；但 CoStar 預測 2027 年美國 RevPAR 降到 +2.1%，已在擴張期後段。議價：上游是業主，分散，但利潤率多年受壓，Hilton 自 2025 年起以 RISE 降費讓利；下游是旅客與通路，OTA 占比十年沒被直訂搶回，AI 代理是新變數。","moat":"機制：品牌帶來的 RevPAR 溢價，加上 Honors 會員網路，再加上規模帶來的融資與分銷優勢，讓業主願意付費掛牌；系統越大，會員價值越高，又吸引更多業主。執行力 9 分：Q3 開業 2.7 萬間，創單季紀錄；NUG 6.0%，高於 Marriott 2026 指引 4.5–5%；在建客房占全球近 20%，為現有占比的 3.5 倍；Q3 新建開工年增逾 40%；轉換案占開業 37%，12 個月內從近 60 個其他品牌轉入。定價力 7 分：CEO 稱 Q2 品牌 RevPAR 溢價再擴大，但對業主在讓利：RISE 已降費，RISE 2 預計 2027 Q1 推出，key money 比例小升。Q3 管理及特許費年增 9.5%，低於 RevPAR（+5.8%）加 NUG（6.0%）的簡單加總 11.8%，差 2.3pp；差距一部分來自中東獎勵費下滑與分時度假授權費，一部分可能是費率讓利，事實表無法拆開。同業對照：投入資本口徑缺，ROIC 差距算不出來，改用利潤率。HLT 營業利益率 24.0%，高於 Marriott 15.7%、Hyatt 7.2%；FCF 利潤率 14.5%，高於 Marriott、Hyatt、Choice，低於 Wyndham 30.6%（經濟型純特許，營收結構不同）。各家營收都含成本代墊，利潤率比較只能看方向。報酬持續期：屬高利益率×高周轉的輕資產模式；四個檢查點一綠三黃，主要隱憂在價值鏈分配，業主與 OTA 都在要錢。增量報酬與再投資：Q3 資本支出加合約取得成本 1.33 億美元，年化約 5.3 億。Q3 調整後 EBITDA 年增 8.4%，推回前一年同季約 9.76 億，單季增量約 8,200 萬，年化約 3.3 億；稅後增量約 2.5 億（稅率假設 25%，實際稅率事實表未涵蓋），增量報酬約 45%。稅後營業利益以 TTM 營業利益率 24.0% × FY2026 共識營收 129.9 億 × 0.75 估算，約 23.4 億，再投資率約 23%（未扣折舊，偏高）。內生成長上界約為 45% × 23%，即 10% 左右。EBITDA 增量有一部分來自既有飯店的 RevPAR 上升，那部分資本是業主出的，所以增量報酬偏高估；但 Q3 EBITDA 實際年增 8.4%，與 10% 上界的量級相符。","growth":"成長組成：量是 NUG 6–7%，價是 RevPAR（2026 年 4–4.5%，2027 年公司口頭給 3–4%），合起來費用收入成長約 9–10%；沒有併購；回購每年減少約 4% 股數。共識 EPS：FY2026 9.13、FY2027 10.45、FY2028 12.0，兩年年化 14.6%。FY2025 調整後實際值事實表未涵蓋，算不出三年；年度表 FY2025 GAAP 稀釋 EPS 6.12 與調整後口徑不同，不混用。同期營收共識：FY2026 129.9 億、FY2027 141.1 億，年增 8.6%，EPS 比營收快約 6pp。內生上界約 10%（推導見護城河段的增量報酬）。缺口是 14.6% 減 10%，約 4.6pp，可完整歸因：淨回購約 3.9pp（年回饋約 35 億美元，扣掉股息約 1.3 億，回購約 33.7 億，除以市值 810.3 億約 4.2%，再扣 SBC 年化約 2.4 億，約 0.3%），營業槓桿約 0.7pp。缺口不靠倍數重估。跑道：全球占比 5.6%，即使產業供給零成長、Hilton 以 6% 擴張，也要 29 年才到 30%；產業供給成長越快，年數越長，10 年以上屬高確信。2027 年開業約八成已在手（CEO），新建開工年增逾 40%。衰退信號十類只亮一個：EPS 成長比營收快 5pp 以上，原因是回購；其餘九項未亮，其中季度毛利率序列事實表未涵蓋。","governance":"FCF 與淨利：FY2022–FY2025 的 FCF ÷ 淨利依序為 1.26、1.49、1.18、1.33 倍；TTM FCF 利潤率 14.5%（FY2025 為 16.2%）。SBC：Q3 為 5,900 萬美元，占營收 1.8%。現金去向：2026 指引資本回饋約 35 億美元（股息每季 0.15 美元，Q3 共 3,400 萬），但 FY2025 FCF 只有 19.44 億，缺口約 15.6 億靠新債補：2025-12 與 2026-05 各發行 10 億美元、利率 5.5% 的票據。淨負債 131.98 億（含租賃負債），除以全年調整後 EBITDA 指引中點 40.7 億，約 3.2 倍；循環信用額度未動用，可用 18.94 億。營運槓桿：FY2025 營收年增 7.7%，營業利益年增約 13.8%，沒有壓縮。近 12 個月無併購。三項計分：併購報酬不適用。回購買入的盈餘殖利率＝1 ÷ 預估本益比 39.9，約 2.5%，低於新債利率 5.5%；10 年期公債殖利率事實表未涵蓋，但除非 10 年期在 0.5% 以下，否則都不過，判不過。SBC 淨稀釋：SBC 年化約占市值 0.3%，回購約占 4.2%，股數淨減少，判過。現金四分（營運再投資、併購、股東回饋、還債）的完整數字事實表未涵蓋。","valuation":"現價 364.18 美元，以 FY2026 共識 9.13 計，預估本益比 39.9 倍；以 FY2027 計為 34.8 倍；trailing 49.2 倍，在四個年度端點中最高（不是五年分位）；EV 為 FY1 營收的 7.3 倍。PEG＝39.9 ÷ 14.6（FY2026→FY2028 兩年年化，不是三年），約 2.7，大於 2 屬貴。反推：終端 30 倍下要賺 10% 年化，FY2031 EPS 要到 19.5 美元（364.18 × 1.1^5 ÷ 30），也就是五年年化 16.4%；倍數若維持 40 倍，基準 EPS 路徑可給約 12% 年化。所以買在現價，等於押倍數一直維持高檔。共識：近 3 個月 FY1 只上修 1.1%，股價 26 週卻漲 17.1%，漲幅主要來自倍數擴張。賣方目標價均值（Tickflow 8 月 342.3、Barchart 約 356、最高 400）低於現價，最高與最低之比約 1.3 倍，分歧不大，方向不支持追價。同業現值倍數事實表未涵蓋，終端 30 倍只能參考前份判斷記載的 7 月 Marriott 約 30 倍。","premortem":"價值陷阱風險為黃燈：十類衰退信號亮一個，即回購讓 EPS 成長比營收快約 6pp。這不是生意變差，而是 EPS 成長有一塊不是內生的；三個視角的反證寫在反證紀錄。最大回撤推導：Bear 谷底 FY2028 EPS 7.8 × 20–24 倍，約 156–187 美元，較現價跌 49–57%；較淺的衰退（EPS 9.0 × 26 倍，約 234）跌 36%；取 −40%～−60%。歷史最大回撤事實表未涵蓋。主要空方數字：預估本益比 39.9 倍、2027 年美國 RevPAR 預測 +2.1%、淨負債 131.98 億、每年約 15.6 億的回饋缺口靠新債補。"},"plain":{"six":{"how_it_makes_money":"賺的是業主的錢：旅館業主為了品牌、訂房系統與 Honors 會員帶來的客房營收溢價，按營收付管理費與特許費。錢卡在「品牌＋會員網路」這一節點，量靠展店，價靠 RevPAR。","moat":"護城河 B 級，方向向上：展店與轉換的份額持續擴大，對業主的定價力持平、略有讓利；最大的新威脅是 AI 代理改寫訂房入口。","growth":"成長跑道寬：Hilton 只占全球供給約 5.6%，NUG 6–7% 可延續多年。但 EPS 共識年增約 14.6%，其中約 4pp 靠回購，內生上界約 10%。","capital":"現金轉換好、SBC 低，但在 40 倍本益比下用部分新債回購，每塊錢回購買到的盈餘殖利率只有約 2.5%，資本配置要打折。","valuation":"現價要求倍數幾乎不收斂：五年後若回到 30 倍，要賺 10% 年化需要 EPS 每年成長 16.4%，高於樂觀情境。我不信，估值很貴。","how_wrong":"最可能看錯的地方有三處：景氣在 2027–28 年轉弱，讓 40 倍倍數與 EPS 一起下修；展店成功，但每間房的收費被讓利與 AI 通路吃掉；回購用新債在高倍數買，股東經濟變差。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把約 14.6% 的 EPS 成長當成內生複利，給到 40 倍；但內生上界約 10%，其餘約 4pp 來自回購，而回購有一部分用 5.5% 新債支應、買到的盈餘殖利率只有 2.5%；需求又處擴張期後段（2027 年美國 RevPAR 預測 +2.1%）。","momentum_overheated":null,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 330 美元以下（約 FY2027 共識 EPS 的 31.6 倍，基準五年年化回到約 8%），且 NUG 指引維持 6% 以上","qc48_result":"pass","qc48_note":"Hilton 的 Bull 情境有展店量乘 RevPAR 加回購的骨架，12.2% 的年化隱含報酬也不高於 Hilton 過去的實現報酬，沒有明顯站不住。但缺口仍在：Bull 後段 RevPAR 假設缺來源，且與產業預測相反。我也找不到可比案例，全球占比與在建占比的口徑無法回溯到法說原文，所以 Bull 依據只算部分成立。","trap":"🟡","val":"🔴","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":364.18,"week26_return_pct":17.13,"consensus_rev_3m_pct":1.11,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母是調整後 EPS（扣特殊項目），與 GAAP 差距不小：trailing 49.2 倍對應的 GAAP EPS 約 7.4 美元，FY2026 調整後指引為 9.07–9.13。特殊項目內容事實表未涵蓋，但共識與公司指引同口徑，市場也用這個口徑，分母不是爭點。"},"catalysts":[{"date":"2026-11-05","date_precision":null,"type":"other","event":"主要上市地由 NYSE 轉到 Nasdaq，代號不變","impact":"低","watch":"指數成分與被動資金的變化；不影響基本面"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 全年指引（RevPAR、NUG、EBITDA、資本回饋）","impact":"高","watch":"RevPAR 指引下緣是否 ≥3%，NUG 是否維持 6–7%，回饋金額多少"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"RISE 2 業主降費方案預計公布","impact":"中","watch":"讓利幅度是否超過 RISE（業主利潤率 75–100bp）"},{"date":"2027-06","date_precision":"month","type":"macro","event":"世足賽高基期：CoStar 預測 2027 年 6 月美國 RevPAR −0.8%","impact":"中","watch":"Q2 2027 RevPAR 年增是否轉負；這是基期效應，不應誤讀為需求反轉"}],"_projected_from":"v19"}
```
