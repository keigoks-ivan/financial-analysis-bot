你是 stock-analyst v20 的**散文層（prose）agent**，標的 EAT（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EAT_20261102/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

每章 3–6 條，每條 100–200 字；s10（估值與三種未來）與 s12（最可能怎麼賠）至少 1,500 bytes，把情境輸入、終端倍數、反證三視角的裁定鋪開。

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

標的：EAT　日期：2026-11-02　archetype：None　前份裁決：2026-07-11　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1955B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（468B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（815B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1635B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1511B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（394B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（890B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2199B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4417B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2723B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1955           3532-5045      5 條（2–6 內）  
s3                  8000         468           5272-7532      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3961          7727-11039      5 條（2–6 內）  
s6                 11000         394          7424-10606      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         890           1827-2610      5 條（2–6 內）  
s10                 5000        2199           1961-2801      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2723           2000-2277      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5084B；至少需散文≈39.92KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−57%
−55
−55%
−49%
−46%
−40%
−39%
−30%
−30
−26%
−16%
−8%
−5.1%
−5%
−3.4%
−3.3%
−1%
0
0%
0.275
0.3%
0.38%
0.4%
0.56%
0.64
0.70
0.75
0.8%
1
01
1.057
1.08
1.14
1.25
1.3%
1.3
1.4
1.43
1.49
1.5%
1.51
1.7
1.7%
1.78
1.9
2%
2
02
2.28
2.39
2.6%
2.65
2.7%
2.7
2.75
2.85
2.85%
2.9
3%
3
3.1
3.22
3.3%
3.5%
3.5
3.7
3.7%
3.75
3.8%
3.831
4%
4
04
4.137
4.28%
4.3
4.4%
4.437
4.87
5
05
5%
5.5%
5.5
5.54
5.575
5.58
5.6%
5.8
5.8%
6
6%
6.1
6.28
6.4%
6.43%
6.5
7%
7
7.0%
07
7.1%
7.4%
7.4
7.5
7.64%
7.86%
08
8%
8
8.25%
9
9%
09
9.1%
9.3%
10%
10
10.1%
10.4%
10.76
10.8
10.82%
10.87
10.99
11
11%
11.11%
11.2
11.4
11.43%
11.50
11.6
11.8
12
12%
12.18%
12.5%
12.6
12.6%
12.9
12.98
13%
13.5
13.55
13.60
13.6
13.65
13.68
13.95
14
14.3
14.5%
14.7
14.70
14.756
14.8
14.8%
14.80
14.95%
15%
15
15.5
15.5%
15.51
15.6
16%
16.30
16.3
16.45
16.5
17
17.68
17.7%
17.7
17.8
18
18.7
18.71
19%
19
19.1
19.1%
19.14%
19.3
19.9
20%
20
21%
22.1
22.2
22.8%
24
24.8
25%
25
26
27%
28
28.9%
30%
30
35%
40%
40
41.3
42
42.5
43
43%
43.23
45
45.71%
45.9
47.6%
49
50
52%
52
53
58.1
59.5
60%
60
62.8
68%
70
75%
80%
84%
90
90.1
90.31
93.6
97%
100%
100
104
105.8
108
120
129.8
130
148
150
150%
157.58
170
179
185
185.26
196
200
210
212
212.18
228
240
243
243.38
250
253
255
300
319
399.6
400
420
500
600
720
830
2022
2026
2027
20261102
2,750
3,300
4,300
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
{"meta":{"ticker":"EAT","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Brinker International, Inc."},"oneliner":"Chili's 靠天天低價套餐加營運改善，連三年雙位數同店、客流連12季贏產業，轉機已到後段；現價約FY2027共識15.5倍，基本情境五年年化約7%，生意變好但價格已反映大半，續抱等回檔再加。","thesis":{"H":[{"id":"H1","text":"Chili's由客流帶動的份額增益，在高基期後仍能延續；新客轉為常客，不是一次性爆紅","2y":"FY27至FY28每季同店不低於+3%、客流不低於0%、領先休閒餐飲產業不低於300bp","5y":null,"10y":null,"threshold":"單季Chili's同店不低於+3%、客流不低於0%、領先產業不低於300bp","source":"公司季報新聞稿與法說（Q1 FY27同店+10.1%、客流+6.4%、領先720bp）；Black Box產業基準","drift_rule":"以近四季同店平均對門檻的偏離計：連2季偏離5%以上為削弱，連3季偏離10%以上為反轉；任一季客流轉負直接觸發唯一致命點"},{"id":"H2","text":"利潤率修復可守並緩步擴張，不因價值策略與加碼人力而回吐","2y":null,"5y":"FY2031餐廳營業利潤率較FY2026累計擴張不少於100bp；穿越一次消費放緩，營業利益率（排除其他損益）仍守在9%以上","10y":null,"threshold":"營業利益率（排除其他損益）不低於10%；餐廳營業利潤率年增不低於20bp（FY27第2季指引約持平，除外）","source":"公司季報（Q1 FY27分別為10.4%、17.7%）；2026-09-17投資人日CFO Mika Ware的長期每年20–40bp說法","drift_rule":"連4季偏離門檻5%以上為削弱，連6季偏離10%以上為反轉"},{"id":"H3","text":"自由現金流轉成每年3–5%減股與2–3%開店，且不拉高槓桿","2y":null,"5y":"FY2031稀釋股數較FY27指引中值42.5百萬股減少不少於15%；FY29起每年開約30家新店","10y":null,"threshold":"年淨減股不低於3%；租賃調整後槓桿低於2倍；FY28開店不少於15家","source":"2026-09-17投資人日（CFO：每年減股3–5%、槓桿目標低於2倍、FY28已核准15家）；Q1 FY27回購1.25億美元","drift_rule":"連4季年化減股低於2.85%為削弱；連6季低於2.7%或槓桿超過2倍為反轉"}],"R":[{"id":"R1","text":"消費放緩加上高基期，使Chili's客流轉負","h_ref":"H1","clock":"⚡","threshold":"任一季客流低於0%＝減碼一半；同店同步低於0%且餐廳利潤率年減＝清倉","evidence_refs":["supply_demand_durability#3","competitive_share_entrants#0"]},{"id":"R2","text":"同業複製社群行銷與價值套餐，價值領先縮小（Black Box已更正人均消費價差，比原先說法窄）","h_ref":"H1","clock":"🔥","threshold":"領先產業幅度連2季低於200bp，或客單組合連2季不高於−1%","evidence_refs":["competitive_share_entrants#2"]},{"id":"R3","text":"商品（含關稅）、運費與時薪通膨吃掉餐廳利潤率，而公司刻意把漲價壓在3%附近","h_ref":"H2","clock":"🔥","threshold":"餐廳營業利潤率連2季年減超過50bp（FY27第2季指引約持平，除外）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"id":"R4","text":"Maggiano's客流持續流失，轉機慢於計畫（2026-08-12 CEO已承認比計畫慢）","h_ref":"H2","clock":"🐢","threshold":"Maggiano's客流連4季不高於−5%（Q1 FY27為−5.1%）","evidence_refs":["supply_demand_durability#2","end_markets#1"]},{"id":"R5","text":"資本支出由約2.75億升至4億美元，改裝目前只打平資金成本，新店報酬未證實，回購在高倍數執行，增量報酬被稀釋","h_ref":"H3","clock":"🐢","threshold":"FY28改裝店營收提升低於3%，或管理層仍未揭露改裝與新店報酬；回購期間前瞻本益比均值超過18倍","evidence_refs":[]}],"single_thing":{"description":"Chili's出現第一季客流年減，客流帶動同店的飛輪斷裂","why_fatal":"這是每股盈餘最大的單一敏感項：客流約占同店三分之二，營業槓桿雙向作用。以約35%遞減利潤率假設估算，同店每少5個百分點，營業利益約少1億美元、每股盈餘約少2美元（約15%），倍數也會同時由15倍往11倍收斂","if_happens":"減碼一半；下一季同店也轉負且餐廳利潤率年減，則清倉","how_monitor":"每季財報的Chili's客流拆分、法說的季中同店口徑、Black Box產業客流","probability":"約30%（12–24個月）：Q2 FY27要對上去年11月的高基期，10月客單組合已轉負，NRA也下修2026實質餐飲成長；但Q2開局仍高個位數，客流仍是同店主力"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.3,"peg_fy2":1.3,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":10.87,"FY2027E":13.68,"FY2028E":14.8,"FY2029E":16.45},"fy_end_month":6,"eps_basis":"FY2026A為GAAP稀釋每股盈餘（財務歷史欄，調整後數字未涵蓋）；FY2027E至FY2029E為Koyfin調整後共識，FY2027含第53週約0.70美元"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EAT_20261102/scenario.json","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"營業利益率由FY23的4.28%回升到FY26的10.82%，租賃調整後槓桿由3.7倍降到1.4倍，8.25%高息債已贖回，資本配置由還債轉向回購與開店；盈餘是否正常化，還要等一次消費下行來檢驗。"},"industry":{"clock_phase":"IV","sd_verdict_source":"休閒餐飲淨店數自2022年−3.3%，同期速食+5.8%、快休閒+15.5%（Black Box，2026-02）；NRA 2026-07中期更新下修2026實質餐飲成長至0.8%；Black Box預估2027銷售小幅成長、客流大致持平。判讀：供給結構性收縮，需求週期性偏弱。","bargaining":{"up":"上游是商品型食材（雞、牛、乳製品、蔬果）、運費與時薪。公司有採購規模，但仍是價格接受者：Q1 FY27商品通膨3.3%、時薪通膨約2.6%，10-K也點名關稅可能推高成本。","down":"下游是分散的個人消費者，轉換成本為零，議價權在消費者手上；公司選擇用低價換客流，而不是靠漲價取利。","geo":"營運集中在美國本土，國際以加盟為主，金額事實表未涵蓋；地緣風險主要經由進口食材關稅傳導。"},"profit_pool_dir":"利潤池由弱勢休閒餐飲業者往執行力強的規模品牌集中；管理層也承認獨立餐廳目前在搶份額。5年前與現在的利潤池占比數字事實表未涵蓋。","tam_table":{"expanded":false,"reason":"成長來自成熟且店數萎縮的品類內搶份額，加上每年2–3%開店，不屬低滲透、新品類或利潤池遷移情境；休閒餐飲市場規模與利潤池占比數字事實表未涵蓋。"}},"moat":{"mechanism":"全國廣告規模＋天天低價菜單架構＋營運簡化與人力配置帶來的相對價值優勢，靠執行維持，沒有轉換成本","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：領先休閒餐飲產業由420bp（Q3 FY26）擴大到720bp（Q1 FY27），客流連12季贏產業。定價面穩定：價格+3.7%未傷客流，但Black Box更正後人均消費價差比原說法窄，10月客單組合轉負。兩者合併判穩定；要升為擴大，須見產業客流轉負期間Chili's仍維持正成長。","peer_na_reason":"同業ROIC與投入資本事實表未涵蓋，以營業利益率與FCF利潤率代理","threats":[{"level":"🟡","text":"同業複製社群爆紅＋價值套餐打法，CEO已點名有競爭者做得成功；若對手營運也到位，Chili's領先產業的幅度會收窄","p":"40%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"level":"🟡","text":"速食重啟價格戰，使休閒餐飲剛追平速食的價值感再度落後","p":"30%","evidence_refs":["supply_demand_durability#4"]},{"level":"🟡","text":"商品（含關稅）、運費與時薪通膨推升成本，而公司刻意把漲價壓在區間低端，價值架構的利潤緩衝變薄","p":"35%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]}],"roic_durability":{"quadrant":"高周轉×中高利益率","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多為同一位用餐客，三個角色一致；但外食屬想要而非需要，延後的代價低。消費承壓下客流仍+6.4%，顯示價值定位在消費降級時受惠；不過10月起酒類與甜點的客單組合轉負，需求韌性只在客流端成立。"},{"item":"決策層級","level":"🟡","text":"替代性要在「今晚吃哪裡」這一層衡量：速食、快休閒、超市熟食、外送都可替代，轉換成本為零。代理讀數方面，價格+3.7%後客流仍+6.4%，沒有漲價流失；新客約占60%，並在9–12個月內行為接近舊客（投資人日）。優勢靠持續執行，不是靠鎖定客戶。"},{"item":"價值鏈分配","level":"🟡","text":"食材、運費與時薪是主要的外部分配者，公司是價格接受者；外送平台分走外送那段約12.5%營收的部分利潤；部分門店自有不動產，降低房東分得的份額。10-K點名關稅可能推高成本，並限制以定價保護利潤率。目前靠銷售槓桿吸收，Q1 FY27餐廳利潤率仍年增150bp。"},{"item":"社會容忍度","level":"🟢","text":"平價外食不依賴任何授權，公司主動把價格壓在低端，沒有逼近社會容忍上限。需留意的是最低工資與小費抵稅（FICA tip credit）等政策變動對人力成本的影響；具體立法進度事實表未涵蓋。"}],"roiic":11,"reinvest_rate":15,"endo_ceiling":1.7,"formula_note":"單位皆為%。當期ROIC粗估約25%：稅後營業利益率＝TTM營業利益率11.43%×（1−19%調整後稅率）≈9.3%；投入資本周轉率＝TTM營收約59.5億美元（企業價值105.8億美元÷企業價值營收比1.78倒推）÷投入資本約22.1億美元（權益4.437億＋淨負債17.68億，後者含租賃負債）≈2.7倍。偏差方向：淨負債含租賃、但營業利益已扣租金，會低估ROIC；權益因多年回購偏低，會高估。增量ROIC約11%：新店每家500–600萬美元、餐廳營業利潤率約17.7%，換算稅前現金報酬約15%上下，扣稅與分攤後約11–12%；改裝CFO稱目前只打平資金成本。再投資率約15%：FY27資本支出中值2.75億美元−折舊攤提約2.39億（3.8%×營收指引中值62.8億）＋加盟店收購約0.275億≈0.64億，除以稅後營業利益約5.8億≈11%；FY28至FY29資本支出升到3.5億、4億後約20%，取中值約15%。營運資金變動事實表未涵蓋，假設為0。內生成長上界≈11%×15%≈1.7%/年。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","EAT":19.14,"MCD":57.38,"TXRH":15.69,"DRI":21.66,"CMG":23.84,"unit":"%"},{"metric":"營業利益率","EAT":11.43,"MCD":45.71,"TXRH":7.86,"DRI":12.18,"CMG":14.95,"unit":"%"},{"metric":"FCF 利潤率","EAT":11.11,"MCD":28.02,"TXRH":6.43,"DRI":7.64,"CMG":11.88,"unit":"%"}],"competitors":[{"name":"MCD","gm":57.38,"om":45.71,"fcf_margin":28.02,"strategy_note":"加盟權利金模式使利潤率（45.71%）不可直接比；它是Chili's廣告直接對比的價值標靶。速食漲價縮小價差讓Chili's受惠，速食若重啟價格戰，則是主要外部威脅。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"TXRH","gm":15.69,"om":7.86,"fcf_margin":6.43,"strategy_note":"牛排館型高客流、重視經理留任的營運標竿；本資料源TTM營業利益率7.86%低於EAT，牛肉成本曝險較高。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"DRI","gm":21.66,"om":12.18,"fcf_margin":7.64,"strategy_note":"多品牌規模採購與管理效率最強的同業，營業利益率12.18%仍略高於EAT，但FCF利潤率7.64%低於EAT的11.11%；EAT在利潤率上正在追近。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"CMG","gm":23.84,"om":14.95,"fcf_margin":11.88,"strategy_note":"快休閒，營業利益率14.95%，與Chili's爭奪年輕客群與外帶；快休閒自2022年淨店數+15.5%，是休閒餐飲流失份額的去處之一。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主：客流約占同店三分之二、價格約三分之一；每股盈餘另加淨回購3–5%與利潤率每年20–40bp；新店FY29起每年貢獻2–3%","runway_years":"份額約5年、新店約10年","runway_post_y5":"🟡","endo_ceiling_basis":"增量ROIC約11%（新店每家500–600萬美元、餐廳營業利潤率約17.7%換算；改裝目前只打平資金成本）×再投資率約15%（FY27至FY29資本支出由2.75億升到4億美元，扣折舊攤提與加盟店收購後，除以稅後營業利益）≈1.7%/年","segments":{"expanded":false,"reason":"分部營收占比事實表未涵蓋；Maggiano's約占獲利3%（投資人日），論點全由Chili's承擔，分部組合不決定利潤走向。"},"decay_signals":[{"item":"毛利率連2季年減","lit":false,"note":"Q1 FY27餐廳利潤率年增150bp"},{"item":"核心市占近12個月縮減","lit":false,"note":"領先產業720bp"},{"item":"提價後銷量下滑","lit":false,"note":"Chili's價格+3.7%、客流+6.4%；Maggiano's價格+2%、客流−5.1%，但只占獲利約3%"},{"item":"每股盈餘成長顯著高於營收成長","lit":true,"note":"FY23→FY26每股盈餘年化約68%、營收約12%；往後共識每股盈餘約12%，對營收4–6%"},{"item":"FCF/淨利連2年低於0.75","lit":false,"note":"FY25 1.08倍、FY26 1.14倍"},{"item":"SBC/營收高於5%且上升","lit":false,"note":"0.56%"},{"item":"TAM萎縮或被替代","lit":true,"note":"休閒餐飲淨店數自2022年−3.3%，客流多年未成長"},{"item":"產業估值倍數近3年系統性下移","lit":null,"note":"事實表未涵蓋"},{"item":"維持性資本支出占FCF高於60%","lit":false,"note":"FY27資本支出2.65–2.85億美元，對FCF約5.5億，維持性部分低於一半"},{"item":"停止新產能且收入3年內下滑","lit":false,"note":"新店FY28加速"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；資本回饋以回購為主（授權7.5億美元、每季1–1.25億美元），不發股利，金額已列在計分卡與理由中"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"唯一收購為12家加盟店，約2,750萬美元（約市值0.3%）；CFO稱對每股盈餘影響約持平，無實現報酬揭露","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"前瞻本益比15.5倍換算回購收益率約6.4%；回購均價與10年期公債殖利率事實表未涵蓋，無法對照門檻","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC年化約3,300萬美元、約市值0.38%，且加權股數指引42–43百萬股持續下降，淨稀釋低於1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2027共識，經第53週校正）為主、PEG為輔；轉機後段看正常化盈餘能力，營收倍數只作參考","peers":{"expanded":false,"reason":"事實表的同業對照只有毛利率、營業利益率、FCF利潤率，未涵蓋同業本益比與目標價，無法同層錨定；改以自身前瞻與歷史倍數為錨"},"fwd_pe":15.51,"peg":1.3,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比15.5倍（去第53週約16.3倍）、PEG約1.3、trailing本益比在4個年度端點的45.9百分位；基本情境五年年化約7%，機率加權後報酬與風險比約1.9。價格合理，但沒有便宜到能補償空方30%的機率。五年分位屬資料缺口，改用年度端點分位代替。","upside_short_pct":7.4,"upside_mid_pct":19.1},"trap_analysis":{"verdict":"🟡","label":"兩項衰退訊號亮燈（每股盈餘成長遠高於營收、品類店數萎縮），屬轉機後段形狀，不是價值陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"10-K指出休閒餐飲多年客流沒有明顯成長，成長只能從同業手上搶；NRA把2026實質餐飲銷售成長由1.3%下修到0.8%；10月起客單組合轉負；Q2要對上去年11月的高基期；Chili's三年累計同店已+52%","assumption":"份額增益是可持續的營運優勢，而不是社群爆紅加價值戰造成的一段高峰","consequence":"若客流轉負，營業槓桿反轉，FY28至FY29每股盈餘可能回到11美元上下，倍數收斂到11倍，股價約120–130美元（約−40%）","ruling":"採納為空方主線，機率30%；與唯一致命點撞上，兩者一致不改動。Q2開局仍高個位數、客流占同店三分之二，一季內發生的機率不高","watch":"Chili's季度客流、領先產業幅度、法說季中同店口徑","evidence_refs":["supply_demand_durability#3","competitive_share_entrants#0"],"fact_refs":["f_kpi7_comparable_restaurant_sa"]},{"view":"論點成功但股東經濟變差","evidence":"FY27資本支出2.65–2.85億美元，投資人日稱之後升到3.5億、4億；CFO說改裝目前只打平資金成本；新店每家500–600萬美元，報酬未揭露；10-K稱關稅與供應鏈可能推高成本，並限制以定價保護利潤率；公司刻意把漲價壓在3–5%區間低端，同時加碼人力","assumption":"客流成長能同時換到利潤率擴張與高增量報酬","consequence":"營收照長、份額照拿，但增量資本報酬掉到接近資金成本，每股盈餘成長主要靠回購；若在高倍數回購，股東實得報酬會低於帳面每股盈餘成長","ruling":"部分採納：再投資規模相對自由現金流（約5.5億美元）仍小，稀釋有限；但這是基本情境年化只有約7%的原因之一","watch":"改裝與新店報酬揭露、餐廳營業利潤率、回購均價","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"],"fact_refs":["f_kpi5_free_cash_flow_non_gaap"]},{"view":"價格已反映太多","evidence":"26週漲43%；股價營收比與企業價值營收比位於近4個年度端點的93.6、90.1百分位；前瞻本益比15.5倍含第53週約0.70美元，去除後約16.3倍；近三月共識+27%是財年換檔造成，實際上修約6%；賣方平均目標價243美元，距現價僅約15%","assumption":"市場仍低估份額增益的持續性","consequence":"就算論點成立，基本情境五年年化約7%，略低於8%的及格線；機率加權後報酬與風險比約1.9","ruling":"採納：續抱不追，等回落到185美元附近（約13.5倍）再加","watch":"股價對FY2027共識的倍數、FY2028共識是否再上修","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_ps_percentile","f_ev_s_percentile","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]},{"view":"論點失敗","evidence":"2026-10-28 Q1法說CEO揭露：Black Box告知產業人均消費基準有誤，Chili's仍較低，但差距比過去引用的3–4美元窄，新數字11月更新","assumption":"天天低價的價值領先幅度夠大，足以在同業複製時守住客流","consequence":"若價差縮到1美元以內，客流領先主要靠營運與行銷，定價面優勢接近消失；同業一旦跟進價值套餐，領先產業的幅度會快速收窄","ruling":"部分採納：定價分維持6不升，護城河方向不升為擴大，等11月資料再定","watch":"Black Box 11月更新、Chili's領先產業幅度","evidence_refs":["competitive_share_entrants#2"],"fact_refs":["f_kpi7_comparable_restaurant_sa"]}],"max_dd":{"lo":-55,"hi":-30,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 185.26 → 本次 212.18（+14.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=185.26","side_b":"本次 price_at_dd=212.18","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 185.26 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 185.26 美元：Bull 價 319、Bear 價 104，五年期望值 +22.8%，基準年化 7.0%，不對稱比 1.4","side_b":"本次情境、股價仍用 185.26 美元：Bull 價 399.6、Bear 價 129.8，五年期望值 +47.6%，基準年化 10.1%，不對稱比 3.22","ruling":"先換情境、股價不動：五年期望值多 24.8 個百分點，基準年化多 3.1 個百分點。不對稱比由 1.4 變為 3.22。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 185.26 美元：五年期望值 +47.6%，基準年化 10.1%，不對稱比 3.22","side_b":"本次情境、股價 212.18 美元：五年期望值 +28.9%，基準年化 7.1%，不對稱比 1.9","ruling":"再換股價、情境不動：起點價上漲 14.5%，五年期望值少 18.7 個百分點，基準年化少 2.9 個百分點，不對稱比由 3.22 降到 1.9。合計五年期望值比前份多 6.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"份額增益是結構性還是高峰","cause":null,"side_a":"管理層（2026-10-28 Q1 FY27法說，CEO Kevin Hochman）：客流連12季贏產業，三年累計同店+52%，新客約60%並轉為常客，Q2開局高個位數，飛輪可持續","side_b":"10-K：休閒餐飲多年客流不長，成長只能靠搶份額；NRA下修2026實質餐飲成長至0.8%；10月客單組合轉負，11月要對上去年高基期；Big Crispy Parm每店每日約2份，低於預期","ruling":"可調和，屬程度差異：份額增益真實，但速度會回到指引的中個位數；基本情境略低於共識，空方30%即為此風險定價","evidence_level":"中（公司自報＋第三方產業資料）","settle_metric":"Chili's Q2 FY27同店與客流（2027年1月公布）","if_then":["若Q2 FY27 Chili's同店不低於+4%且客流為正：維持基本情境，股價不高於185美元時分批加碼","若任一季Chili's客流年減：減碼一半；下一季同店也轉負且餐廳利潤率年減則清倉","若股價先漲、證據未到（Q2財報前漲破240美元）：不追"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","supply_demand_durability#3","end_markets#2"]},{"axis":"近三月共識上修的口徑","cause":null,"side_a":"事實表顯示近三月FY1共識由10.76上修到13.68美元（+27%）","side_b":"7月30日快照時FY2026尚未公告，仍被當成FY1（10.76美元與FY2026實際GAAP每股盈餘10.87美元相近），屬財年換檔；Chartmill 10月17日顯示FY2027共識三個月上修約6%，財報後再由13.65上修至13.68美元","ruling":"採B側：真實上修約6%，盈餘動能不以27%計；這也是不把盈餘動能當加碼理由的原因之一","evidence_level":"高（兩個獨立來源口徑可對上）","settle_metric":"下一份共識快照的FY2027與FY2028數字","if_then":[],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#1"]},{"axis":"管理層利潤率說法前後對照","cause":null,"side_a":"2026-08-12 Q4 FY26法說CFO Mika Ware：FY27餐廳利潤率以52週計改善20–40bp，轉型後利潤率成長會趨緩；2026-09-17投資人日重申長期每年20–40bp","side_b":"2026-10-28 Q1 FY27法說CFO：FY27改善70–90bp（含第53週約30bp），Q2約持平，Q3回到20–40bp，Q4因番茄、生菜基期有上檔","ruling":"可調和：上修來自Q1超預期與商品基期，長期說法沒變；情境樹基本情境採每年20–40bp，不外推FY27的幅度","evidence_level":"高（逐字稿）","settle_metric":"FY27第2季餐廳營業利潤率年變化（指引約持平）","if_then":[],"evidence_refs":[]},{"axis":"價值領先的量化幅度","cause":null,"side_a":"2026-08-12 Q4法說與2026-09-17投資人日，CEO稱Chili's人均消費比競爭者低3–4美元","side_b":"2026-10-28 Q1法說CEO：Black Box告知產業人均消費基準有誤，Chili's仍較低，但差距比原先說法窄，新數字11月更新","ruling":"採B側：定價分維持6不升；若11月更新後差距不到1美元，定價分降到5，合併分降到約6.5，護城河等級可能降為C","evidence_level":"中（尚待更新資料）","settle_metric":"Black Box 2026年11月更新的休閒餐飲人均消費基準","if_then":["若更新後價差不低於2美元：定價面維持穩定","若更新後價差低於1美元：重估護城河等級，暫停加碼，直到下一季客流確認"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"客流連12季領先、指引上修、Q2開局高個位數；管理層財測歷來偏保守（2026-08-12 CEO：每年起始財測都被超越）；前瞻本益比15.5倍低於自身trailing 18.7倍；每年減股3–5%；若同店守住中個位數，FY2029每股盈餘可能高於共識16.45美元，股價可能不再回到185美元","side_b":"26週已漲43%，財報當日漲約13%；基本情境五年年化約7%，低於8%；空方機率30%，報酬與風險比約1.9；共識實際上修只有約6%","ruling":"不採A側為立即加碼理由，但保留證據先到的分支","evidence_level":"中","settle_metric":"Q2、Q3 FY27同店與FY2028共識","if_then":["若股價未回落，而Q2、Q3 FY27同店均不低於+4%且FY2028共識再上修5%以上：以目標倉位1/3小量加回","若股價回落到185美元以下而客流仍為正：分批加碼"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"評等、估值與陷阱判讀的前後對照","cause":"新證據","prior_field":["signal","val","trap"],"side_a":"前份（2026-07-11，股價185.26美元）：綜合評等B級、估值合理、價值陷阱風險中等","side_b":"本次三欄維持同值：Q1 FY27同店+10.1%、指引上修、FY2027共識13.68美元（前份門檻為12美元），盈餘基礎上移；但股價同步上漲約14.5%，前瞻倍數仍約15.5倍；陷阱訊號仍是兩項","ruling":"三欄不變；盈餘上修與股價上漲大致抵銷","evidence_level":"高","settle_metric":"FY2027實際每股盈餘對指引中值13.60美元","if_then":[],"evidence_refs":["supply_demand_durability#1","capital_markets_pricing#0"]},{"axis":"護城河方向、跑道與類型","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河方向穩定、五年後跑道中等、類型為轉機/特殊情境、未標循環位置","side_b":"本次維持四欄。執行面因領先產業由420bp擴大到720bp而轉強，但Black Box人均消費價差被更正變窄，合併仍判穩定；投資人日公布每年2–3%新店與300個商圈，仍不是第二條成長曲線；轉機三件工作已完成，但盈餘正常化未經消費下行檢驗，類型維持；非商品循環股，不標循環位置","ruling":"四欄不變；若產業客流轉負期間Chili's仍維持正成長，護城河方向升為擴大，類型改為品質複利成長","evidence_level":"中","settle_metric":"下一次產業客流轉負季度的Chili's客流","if_then":[],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"axis":"機率與最大回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭25%、空頭30%、最大回撤−46%","side_b":"本次多頭25%、空頭30%不變；最大回撤改為−55%至−30%的範圍。下緣加深，是因為股價由185.26美元漲到212.18美元，與250週均線90.31美元的距離拉大到−57%","ruling":"機率不變，因基本面上修已被價格吸收；回撤下緣隨價格上移而加深","evidence_level":"高","settle_metric":"股價與250週均線距離","if_then":[],"evidence_refs":[]},{"axis":"裁決與角色","cause":"價格變動","prior_field":[],"side_a":"前份：進場、衛星角色","side_b":"本次結論改為續抱不追、等回落到185美元附近再加：股價漲14.5%，基本情境年化仍只有約7%。最終裁決與角色由決策矩陣依本次輸入重算","ruling":"約束來自價格，不是論點；論點比前份更扎實","evidence_level":"高","settle_metric":"股價對FY2027共識倍數","if_then":[],"evidence_refs":[]},{"axis":"加碼條件改寫","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3；帽 3%；加碼＝Q4 FY26 comp ≥ +3% 且 FY27 guide 不下修；撤退＝Chili's 任一季 comp 轉負","side_b":"股價不高於185美元（FY2027共識約13.5倍）且最近一季Chili's客流為正，才恢復分批加碼；客流轉負先減碼一半，同店轉負且利潤率年減才清倉","ruling":"前份加碼條件已兌現（Q4 FY26 Chili's同店+5.6%，FY27指引10月上修），但股價已先漲。現在的約束是價格，所以新加碼條件改為價格錨加客流確認；撤退條件拆成兩段：減碼看客流、清倉看同店與利潤率","evidence_level":"高","settle_metric":"股價、Chili's單季客流","if_then":[],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"Single Thing（唯一致命點）由未設定改為客流轉負","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（null）","side_b":"Chili's出現第一季客流年減，客流帶動同店的飛輪斷裂","ruling":"依敏感度設定：客流占同店三分之二，同店每少5個百分點，每股盈餘約少2美元，是數學上最大的單一敏感項；觸發時減碼一半，確認後清倉","evidence_level":"中","settle_metric":"Chili's單季客流","if_then":[],"evidence_refs":["supply_demand_durability#3"]},{"axis":"清倉與減碼門檻更新","cause":"新證據","prior_field":["kill_metrics","thesis.R","thesis.H"],"side_a":"前份：未設kill metrics；R1任一季同店轉負＝撤退、連2季低於+2%＝減碼；R2價差連3月低於+200bps；R3餐廳層利潤率自高位回落超過200bps；H3以FY27共識連3月低於11.50美元為反轉","side_b":"本次：客流任一季低於0%＝減碼一半；同店低於0%且餐廳利潤率年減＝清倉；領先產業連2季低於200bp＝停止加碼；餐廳利潤率連2季年減超過50bp＝減碼1/3；租賃調整後槓桿超過2倍＝重評回購；H3改為年淨減股不低於3%且槓桿低於2倍","ruling":"門檻改動理由有四：①客流已占同店三分之二，比同店更早反映飛輪斷裂，所以減碼提前到看客流；②月度Black Box資料不在證據包，價差改用季度；③利潤率門檻由200bp收緊到連2季50bp，因公司刻意壓低漲價，緩衝變薄；④FY27共識已是13.68美元，遠高於舊門檻11.50，舊H3門檻退休","evidence_level":"高","settle_metric":"各門檻對應的季度數字","if_then":[],"evidence_refs":["reg_tariff_export#1"]}],"triggers":[{"n":1,"text":"以Chili's季度同店、客流與領先產業幅度驗證份額增益","type":"假設驗證","maps_to":"H1","metric":"Chili's單季同店、客流、領先休閒餐飲產業幅度","threshold":"同店不低於+3%、客流不低於0%、領先不低於300bp","action":"達標則維持；連2季未達則停止加碼","source_freq":"公司季報與法說，每季","date":"2027-01","evidence_refs":["competitive_share_entrants#1"]},{"n":2,"text":"Chili's任一季客流年減","type":"Single Thing","maps_to":"R1","metric":"Chili's單季客流年變化","threshold":"低於0%","action":"減碼一半；下一季同店也低於0%且餐廳利潤率年減則清倉","source_freq":"公司季報，每季","date":"2027-01","evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"成本通膨（含關稅、運費、時薪）壓縮餐廳利潤率","type":"風險","maps_to":"R3","metric":"Brinker餐廳營業利潤率年變化","threshold":"連2季年減超過50bp（FY27第2季指引約持平，不計）","action":"減碼1/3","source_freq":"公司季報，每季","date":"2027-04","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":4,"text":"價格回到合理偏便宜區，且飛輪未斷","type":"估值rearm","maps_to":"H1","metric":"股價、FY2027共識倍數、最近一季Chili's客流","threshold":"股價不高於185美元（約13.5倍）且客流高於0%","action":"分批加碼，每次目標倉位1/3","source_freq":"每日股價＋每季財報","date":null},{"n":5,"text":"倍數超過自身合理上緣，而盈餘未跟上","type":"減碼","maps_to":"H3","metric":"股價÷次一財年共識每股盈餘","threshold":"不低於19倍，且近3個月共識未上修","action":"減碼1/3","source_freq":"每週","date":null},{"n":6,"text":"同店轉負同時利潤率下滑，確認飛輪斷裂","type":"清倉","maps_to":"R1","metric":"Chili's單季同店與餐廳營業利潤率年變化","threshold":"同店低於0%且餐廳利潤率年減","action":"清倉","source_freq":"公司季報，每季","date":null},{"n":7,"text":"Maggiano's客流持續流失","type":"風險","maps_to":"R4","metric":"Maggiano's單季客流","threshold":"連4季不高於−5%","action":"不加碼，並留意減損或出售；不單獨觸發減碼（約占獲利3%）","source_freq":"公司季報，每季","date":"2027-08","evidence_refs":["supply_demand_durability#2","end_markets#1"]},{"n":8,"text":"Black Box人均消費基準更新，以及Q2 FY27財報後複審","type":"複審日期","maps_to":"R2","metric":"更新後Chili's人均消費低於同業的差距、Q2同店","threshold":"差距低於1美元則重估護城河等級","action":"複審","source_freq":"一次性","date":"2027-01"},{"n":9,"text":"回購與開店節奏","type":"假設驗證","maps_to":"H3","metric":"年淨股數縮減、租賃調整後槓桿、FY28開店數","threshold":"減股不低於3%、槓桿低於2倍、FY28開店不少於15家","action":"未達則下調基本情境每股盈餘","source_freq":"年報與投資人日，每年","date":"2027-08"},{"n":10,"text":"利潤率修復能否守住","type":"假設驗證","maps_to":"H2","metric":"營業利益率（排除其他損益）","threshold":"不低於10%","action":"連4季未達則下調基本情境倍數至14倍","source_freq":"公司季報，每季","date":"2027-04"}],"kill_metrics":[{"metric":"Chili's單季客流（年變化）","bear_threshold":"低於0%","window":"任一季","source":"公司季報新聞稿與法說","last_status":"ok"},{"metric":"Chili's單季同店銷售","bear_threshold":"低於0%且同季餐廳營業利潤率年減","window":"任一季","source":"公司季報新聞稿與法說","last_status":"ok"},{"metric":"Chili's同店領先休閒餐飲產業幅度","bear_threshold":"低於200bp","window":"連2季","source":"公司法說引用的Black Box產業資料","last_status":"ok"},{"metric":"Brinker餐廳營業利潤率年變化","bear_threshold":"年減超過50bp","window":"連2季（FY27第2季指引約持平，不計）","source":"公司季報新聞稿","last_status":"ok"},{"metric":"租賃調整後槓桿","bear_threshold":"超過2倍","window":"任一季","source":"公司法說與投資人日","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=43.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件=\"股價回落到185美元以下（FY2027共識約13.5倍，基本情境五年年化約10%），且最近一季Chili's客流仍為正\""},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"單一持股上限3%","requires_critic":[],"rearm_trigger":"股價不高於185美元（FY2027共識約13.5倍）且最近一季Chili's客流為正，才恢復分批加碼","exec_line":"續抱現有部位、不追價；股價不高於185美元且最近一季Chili's客流為正時分批加碼（每次目標倉位1/3）；客流任一季轉負減碼一半；同店轉負且餐廳利潤率年減清倉；股價達次一財年共識19倍以上且共識未上修，減碼1/3"},"reasoning":{"industry":"Q1 FY27 營收14.756億美元、GAAP營業利益1.51億美元、排除其他損益後營業利益率10.4%、餐廳營業利潤率17.7%（年增150bp）。Brinker合併同店+9.1%，其中Chili's +10.1%＝客流6.4%＋價格3.7%＋組合持平；Maggiano's −3.4%（客流−5.1%）。TTM毛利率19.14%、營業利益率11.43%。分部營收占比事實表未涵蓋；投資人日（2026-09-17，CEO Kevin Hochman）稱Maggiano's約占獲利3%，所以Chili's是唯一承重分部，全集團約97%獲利繫於單一品牌。收錢方式以自營門店內用為主，外帶約四分之一（外送、自取各約12.5%，Q1 FY27法說CEO）；Triple Dipper一項占Chili's銷售16%（投資人日CMO George Felix）。單點依賴屬集中度風險，不是護城河證據。產業時鐘判IV收縮：休閒餐飲自2022年淨店數−3.3%，約9%全服務餐廳2026年有倒閉風險，NRA把2026實質餐飲成長由1.3%下修至0.8%。產業正在出清供給，存活的規模業者受惠。供需持久性方面，供給收縮是結構性的，需求則是週期性走弱，兩者相抵：份額可以延續，但總量不長。產業態勢三軸：A競爭面，同業開始複製社群行銷與價值套餐（CEO稱已有競爭者成功）；B結構面，供給出清，速食漲價使休閒餐飲的價值感追平速食，屬轉好；C其他面，關稅、運費與時薪成本上升。裁決為雙向拉鋸。類型仍判轉機/特殊情境（後段），次要類型為品質複利成長。利潤率修復、去槓桿、高息債贖回三件轉機工作已完成，但目前盈餘水準是否已正常化，還沒經過一次消費下行的檢驗。","moat":"機制是全國廣告規模＋天天低價菜單架構（3 for Me約占21%、10.99美元套餐約占帳單9%）＋營運簡化與人力配置，形成相對價值優勢。這種優勢靠執行維持，不是轉換成本或網路效應。\n\n可證方向用份額軸：Chili's同店領先休閒餐飲產業，Q3 FY26為420bp，Q1 FY27擴大到720bp，客流已連12季贏產業（法說CEO）。\n\n同業ROIC事實表未涵蓋，改用利潤率當代理。EAT TTM營業利益率11.43%，DRI 12.18%、TXRH 7.86%、CMG 14.95%；FCF利潤率EAT 11.11%，高於DRI 7.64%、TXRH 6.43%；MCD以加盟權利金為主（營業利益率45.71%），不可直接比。EAT自身營業利益率由FY23 4.28%升到FY26 10.82%（財務歷史欄，年度財報），與DRI的差距在縮小，但DRI歷年數字未涵蓋，只能看單點。\n\n評分：執行8分，依據是客流領先、Google評分創新高4.3、時薪員工離職率降到84%回到產業平均。定價6分：價格+3.7%同時客流+6.4%，代表漲價沒傷到量；但公司刻意把漲價壓在3–5%低端，人均消費優勢經Black Box更正後變窄，10月起酒類與甜點的客單組合也轉負。合併約7分，等級B；未達8分，不需做同業ROIC價差檢驗。三項威脅都屬點對點，不扣分。\n\n當期ROIC粗估約25%（推導見持續期欄），屬高周轉×中高利益率。四檢查點中三項黃燈，報酬持續期取決於執行，不取決於結構。","growth":"成長組成：Q1 FY27 Chili's同店10.1%中，客流6.4%、價格3.7%、組合持平。FY27後三季指引回到中個位數同店、客流為正。投資人日的三年框架為營收年增4–6%（同店2–3%、新店2–3%）、每年減股3–5%、每股盈餘雙位數成長。\n\n三年共識：FY2026A GAAP稀釋每股盈餘10.87美元（財務歷史欄）→FY2029E 16.45美元，CAGR約14.8%。但基期是GAAP、共識是調整後，且FY2027含第53週約0.70美元；去除後FY2027約12.98美元→FY2029E 16.45美元，CAGR約12.6%，以後者為準。\n\n內生成長上界約1.7%/年（增量ROIC約11%×再投資率約15%，推導見持續期欄）。共識與上界的缺口約11pp，歸因如下：利潤率擴張與既有門店同店帶來的營業槓桿約5–6pp、淨回購約4pp、收購0、無法歸因約1–2pp。成長主要靠不需新增資本的同店與回購，屬高ROIC、低再投資空間的形狀，信心上限為中。\n\n跑道：管理層稱門店只用到歷史客流容量約80%，每店每週客數目標4,300人約可再帶來2%同店，份額跑道約5年；新店有300個以上商圈、每年約30家，約可走10年。五年後的跑道無法用滲透率衡量，以無第二曲線、品類不成長判為中等。\n\n衰退訊號亮兩項：每股盈餘成長遠高於營收（FY23→FY26每股盈餘2.28→10.87美元，營收41.3→58.1億美元）、品類店數萎縮。其餘未亮：毛利率連升，FCF/淨利FY25 1.08倍、FY26 1.14倍，SBC占營收0.56%。","governance":"FCF/淨利：FY25 1.08倍（4.137億÷3.831億）、FY26 1.14倍（5.575億÷4.87億）。SBC：Q1 FY27為830萬美元，占營收0.56%、占GAAP營業利益5.5%。\n\n現金去向：FY26全年分項事實表未涵蓋。已知的有：Q4 FY26回購1億美元；Q1 FY27回購1.25億美元，高於當季FCF 1.057億，差額由循環信貸支應（Q1末循環信貸餘額3.75億）；8月董事會加碼授權至7.5億美元；以循環信貸贖回3.5億美元8.25%票據，換成較低利率，屬再融資而非還債；12家加盟店收購約0.275億美元；不發股利（投資人日CFO：現在不做）。\n\n槓桿：租賃調整後由3.7倍降到1.4倍，目標低於2倍；目前淨負債17.68億美元（含租賃）。營運槓桿：FY26營收+7.86%、營業利益約+13%（5.54億→6.28億，以年度營業利益率換算），屬擴張而非壓縮。\n\n計分卡：\n- 併購報酬：不適用，金額約市值0.3%，也沒有實現報酬揭露。\n- 回購收益率：以判斷日前瞻本益比15.5倍換算約6.4%，若10年期殖利率低於約4.4%即通過；殖利率事實表未涵蓋，故不判。\n- SBC淨稀釋：約為市值0.4%/年，且股數淨減，通過。","valuation":"判斷日股價212.18美元。\n\n倍數：前瞻本益比15.51倍（FY2027共識13.68美元）；FY2027含第53週約0.70美元，去除後約16.3倍；FY2028共識14.80美元對應約14.3倍。Trailing本益比18.71倍，位於近4個年度端點的45.9百分位。股價營收比1.49倍、企業價值營收比1.78倍，分居93.6、90.1百分位；營收倍數偏高是因為利潤率由4%修復到11%，不代表貴，盈餘倍數才是主尺。五年分位事實表未涵蓋（只有4個年度端點），不外推。\n\nPEG：去除第53週後，FY2027→FY2029共識CAGR約12.6%，16.3÷12.6≈1.3，落在合理區。同業本益比事實表未涵蓋，無法做同層錨定。\n\n賣方：Jefferies目標價255美元，過去一年更新的平均目標價243.38美元（24家中19家買進），距現價約15%。\n\n共識修正：財報後FY2027共識由13.65上修到13.68美元，Chartmill顯示財報前三個月上修約6%。事實表的近三月+27%，是7月底快照仍以FY2026為FY1造成的財年換檔，不是真實上修。\n\n上檔：12個月以FY2028基本情境每股盈餘14.70美元×15.5倍＝約228美元（+7.4%）；約3年以FY2029的16.30美元×15.5倍＝約253美元（+19.1%）。","premortem":"唯一致命點與空方主線重合（客流轉負），見反證紀錄。\n\n價值陷阱判中度：衰退訊號亮兩項（每股盈餘成長遠高於營收、品類店數萎縮），屬轉機後段的正常形狀，不是盈餘品質惡化。\n\n最大回撤推導：空方情境終點約130美元（−39%）；路徑谷底以FY2029空方每股盈餘10.8美元×10倍≈108美元（−49%）；技術面回到104週均線157.58美元為−26%，回到250週均線90.31美元為−57%；26週漲43%後，回吐空間大。取範圍−55%至−30%。\n\n壓力測試三項（以FY2029兩年期、跌幅不超過5%算通過），通過1/3：\n- 四季同店持平：每股盈餘約14美元×14倍≈196美元（−8%），不過。\n- 餐廳利潤率回吐200bp：16.3−2.75＝13.55美元×15.5倍≈210美元（−1%），通過。\n- 倍數降到11倍、盈餘照基本情境：16.30×11≈179美元（−16%），不過。\n\n訴訟與監管：只有轉租違約訴訟（FY25費用170萬美元、FY26無），無集體訴訟、無SEC調查。法說迴避的問題中，最相關的是改裝報酬，以及North of 6利潤率差距能實現多少，管理層都沒給數字。"},"plain":{"six":{"how_it_makes_money":"賺美國中價位用餐客的錢：Chili's 以10.99美元套餐等天天低價把速食客拉進門，再靠出餐與服務改善留住。錢卡在「客流」這一節點：客流占同店三分之二，撐起營業槓桿，客流一斷利潤率就回吐。","moat":"護城河方向穩定、等級B。執行面在擴大：領先產業幅度由420bp拉到720bp，客流連12季贏產業。定價面只算穩定：人均消費價差被第三方更正為比原說法窄，10月客單組合轉負。合併判穩定。","growth":"五年後跑道中等：在成熟且店數萎縮的品類裡靠搶份額，加上FY29起每年2–3%開店，目前沒有已證實的第二條成長曲線。","capital":"現金流強，用途已轉向回購：FY26自由現金流約5.58億美元、為淨利1.14倍，SBC只占營收0.56%。回購是否買得划算，因回購均價與10年期公債殖利率事實表未涵蓋，無法下定論。","valuation":"現價要求FY2029每股盈餘約16.5美元、倍數守在15倍上下才划算。盈餘路徑我大致相信，但26週漲43%後，基本情境五年年化只剩約7%，價格合理偏滿，不追。","how_wrong":"最可能看錯的是客流飛輪的持續性：若Chili's在高基期與消費承壓下出現一季客流年減，營業槓桿會反轉，每股盈餘與倍數同時下修。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回落到185美元以下（FY2027共識約13.5倍，基本情境五年年化約10%），且最近一季Chili's客流仍為正","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"轉機/特殊情境","price_at_dd":212.18,"week26_return_pct":43.23,"consensus_rev_3m_pct":27.14,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2027共識含第53週約0.70美元（約5%），已改用去除後約12.98美元校正倍數；一次性效應沒有大到成為爭點。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"Black Box更正休閒餐飲人均消費基準","impact":"中","watch":"Chili's低於同業的價差還剩多少"},{"date":"2026-11","date_precision":"month","type":"product","event":"Big Crispy Chicken Parm店內桌卡上架","impact":"低","watch":"每店每日銷量是否由約2份回升"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q2 FY27財報與長期成長更新","impact":"高","watch":"同店是否守住中個位數、客流為正，以及對上去年11月高基期的表現"},{"date":"2027-05","date_precision":"month","type":"product","event":"評估是否更換Big Crispy主打訊息","impact":"中","watch":"廣告帶動的客流增量是否衰退"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27年報（含第53週）與FY28財測","impact":"高","watch":"FY28財測扣除第53週後是否仍雙位數成長，開店是否達15家以上"}],"_projected_from":"v19"}
```
