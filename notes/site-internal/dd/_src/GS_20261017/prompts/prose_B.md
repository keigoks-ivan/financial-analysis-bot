你是 stock-analyst v20 的**散文層（prose）agent**，標的 GS（2026-10-17）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GS_20261017/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：GS　日期：2026-10-17　archetype：None　前份裁決：2026-06-15　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1793B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（441B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（492B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1515B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（878B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（609B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（925B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2111B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3366B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2226B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1793           3645-5207      5 條（2–6 內）  
s3                  8000         441           5291-7559      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2885          8480-12115      5 條（2–6 內）  
s6                 11000         609          7274-10391      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         925           1802-2575      5 條（2–6 內）  
s10                 5000        2111           2022-2889      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2226           2000-2774      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4196B；至少需散文≈40.80KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−83.4%
−62.7%
−50
−50%
−28%
−28
−27%
−18.6%
−15%
−5.5%
−3.94
−0.5%
0
0.66
0.75
0.85
0.91
1
01
1%
1.5
1.7
1.72
2
2.0
2%
2.04
2.04%
2.8
2.8%
3
3.3%
3.3
3.68
3.7%
3.9%
4%
4
04
4.1
4.2
4.5%
4.7%
5%
5
5.4%
6%
06
6
6.4%
6.5%
6.65
07
7
7%
7.5
7.5%
8
8%
08
8.04
8.5%
8.9%
9
10
10%
10.5
11
11%
11.4
11.5
12
12.13
12.4%
12.5
12.67
12.9%
13
13%
13.0
13.02
13.2
14
14%
14.3%
14.9
15
15%
16.1%
17
17.01
17.2
18
18.6%
18.7%
18.7
19%
19.8%
19.8
20%
20
20.7%
21.6
22
22%
23%
23.5%
24
25%
26%
26
26.6%
27
27%
27.4%
29
30%
30
32%
34
34.7
35
35%
36
37.5%
38%
40
40%
40.54
41%
42
44.9
45%
46
48%
49%
49
50
50.5
51.32
52.94
55%
55
58
59.4%
60
64.4
67.78
68
70
71.67
72%
72.67
73
73.4%
75
76
76.5
76.73
80.5
81%
82
84.5
85%
88
90
95
96%
100
100%
101
102
127
128
134.6
140
146
150%
150
160
186.8
200
270
460
500
583
600
630
640
763
881
881.26
910
1082.57
2016
2018
2022
2023
2025
2026
2027
2028
2032
20261017
1,000
1,048.73
1,049
1,056
1,082
1,082.57
1,500
1,530
18,679
2,760
4,300
4,910
7,003
9,930
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
{"meta":{"ticker":"GS","date":"2026-10-17","schema":"v15.2","contract":"v19","company_name":"The Goldman Sachs Group, Inc."},"oneliner":"高盛是資本市場裡最強的顧問與做市平台之一，耐久型收入已占近半；但 2026 年的獲利處在週期高處，13 倍本益比談不上便宜。先等兩季財報證明谷底已經抬高，再考慮進場。","thesis":{"H":[{"id":"H1","text":"資本市場從前十分位回到前四分位，是降溫而不是崩落：全公司季淨營收守在 150 億美元以上，M&A 宣布量維持第一","2y":"FY2027 全年淨營收 ≥600 億美元（FY2025 為 583 億）","5y":null,"10y":null,"threshold":"季淨營收 ≥150 億美元；年初至今 M&A 宣布量排名第一","source":"每季 8-K 財報稿與法說；全球 M&A 宣布量排行","drift_rule":"兩年期：TTM 淨營收低於 600 億美元，連 2 季偏離 ≥5% 視為削弱，連 3 季偏離 ≥10% 視為反轉"},{"id":"H2","text":"耐久型收入（管理費、融資收入）持續上升，把獲利谷底抬高","2y":"管理及其他費用季年增 ≥8%","5y":"管理及其他費用年化 ≥200 億美元；融資收入占 FICC 加股票營收跨週期維持 ≥40%","10y":null,"threshold":"3Q26 管理及其他費用 36 億美元，年增 22%；前三季融資收入 127 億美元，占比逾 40%；長期淨流入連續 35 季","source":"每季 8-K 與法說（Coleman，2026-10-13）","drift_rule":"五年期：管理費年增低於 8%，連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"},{"id":"H3","text":"管理層守住資本紀律：跨週期 ROE ≥15%，多出來的資本退回股東，而不是再買進低回報的業務","2y":null,"5y":"五年平均 ROE ≥15%（2025 年為 15%，前三季 20.7%）","10y":null,"threshold":"滾動四季 ROE ≥15%；CET1 高於要求 50–100bp；單筆收購小於市值 5%","source":"每季 8-K；股東會（2026-04-29，Solomon）；10-Q","drift_rule":"五年期：滾動 ROE 低於 15%，連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"資本市場活動從前四分位繼續下滑：M&A 量已季減 41%，聯準會升息，IPO 動能在夏季後轉弱","h_ref":"H1","clock":"⚡","threshold":"全公司季淨營收連 2 季年減 >15% 則減碼","evidence_refs":["end_markets#5"]},{"id":"R2","text":"資本配置偏離：為了衝資產管理規模付出高價收購，或再度進入低回報業務；Platform Solutions 3Q26 仍在認列 Apple Card 減值，是前一輪擴張失誤的尾巴","h_ref":"H3","clock":"🔥","threshold":"單筆收購超過市值 5%，或 AWM 稅前利益率連 4 季低於 25%","evidence_refs":["end_markets#3"]},{"id":"R3","text":"股票融資與 AI 基建融資把資產負債表推大：一旦對沖基金去槓桿或大型融資案出問題，所謂的耐久收入會跟著週期一起下滑，信用損失也同時上升","h_ref":"H2","clock":"🔥","threshold":"單季撥備超過 7.5 億美元，或融資收入季減超過 15%","evidence_refs":[]},{"id":"R4","text":"法律與監管：1MDB 證券集體訴訟已認證集體（購買期間 2016-12-22 至 2018-11-08），CDS 結算價反壟斷案仍在進行，另有一件私人反壟斷訴訟與未具名的監管調查；金額與結案時點都在事實表未涵蓋","h_ref":"H3","clock":"🐢","threshold":"和解或判決金額超過 50 億美元，或政府機關新立案則減碼；刑事介入則清倉檢討","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#0"]}],"single_thing":{"description":"某一季全公司淨營收跌破 140 億美元（低於 2025 年季均約 146 億），代表資本市場從前四分位跌到中位數以下","why_fatal":"淨營收約七成來自投行與交易，費用又有剛性；營收回到 2025 年以下時，EPS 會從 68 美元掉到 46–50 美元，市場同時把倍數壓到約 10 倍，股價約 460–500 美元，比現價低約 45%。這是情境樹裡最大的單一敏感項","if_happens":"持有則減碼至半倉並重跑研究；未持有則延後任何進場，直到營收連兩季止跌","how_monitor":"每季 8-K 的淨營收；每月全球 M&A 宣布量與美國 IPO 件數；財報稿對投行積壓方向的描述","probability":"約 20%（12–24 個月）：M&A 量已季減 41%、聯準會升息、積壓從高點回落；但耐久收入約 45%，加上 3Q26 營收仍有 186.8 億美元，離門檻還有距離"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.13,"peg_fy2":0.85,"stress":{"pass":6,"total":7}},"eps_meta":{"base_eps_path":{"FY2025A":51.32,"FY2026E":67.78,"FY2027E":72.67,"FY2028E":76.73},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識取自 Koyfin 2026-10-08 快照，分析師家數事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GS_20261017/scenario.json","archetype":{"primary":"金融","secondary":"循環/商品","confidence":"高","fingerprint":"約七成收入來自投行與交易，隨資本市場週期擺動；近三成來自資產與財富管理費；資本受監管比率約束的資產負債表業者"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：Solomon 在 2026-10-13 法說稱活動從前十分位降到前四分位；3Q26 全球 M&A 宣布量季減 41% 至 9,930 億美元；8-K 載明投行積壓較 2Q26 末下降、較 2025 年底略降；耐久收入約 45% 只能減緩回落","bargaining":{"up":"上游是人才：Coleman 稱頂尖業務與工程人才的爭奪更激烈；薪酬比降到 30% 是業務組合偏向融資的結果，並不代表人才議價力下降","down":"下游企業可以在多家投行之間挑顧問，但最大型交易集中在前兩名；股票融資需求超過產業供給，高盛握有定價權並可挑客戶","geo":"亞洲股票融資是新的增量來源；中東衝突帶來的能源與利率波動，是交易延後的主要外部風險"},"profit_pool_dir":"利潤池正往融資（動用資產負債表）與另類資產（管理費）移動，純顧問與承銷的占比下降；高盛在兩邊都有位置，是少數同時具備顧問、承銷、分銷與自有資金池的業者","tam_table":{"expanded":false,"reason":"投行與交易是成熟市場，成長取決於活動週期與份額，不是滲透率；另類資產與財富管理的市場規模與滲透率在事實表未涵蓋，無法展開"}},"moat":{"mechanism":"董事會層級顧問關係＋做市與融資的資產負債表規模＋自有公私募資金池，三者互相加乘：顧問帶出融資與承銷，融資與承銷的部位再分配進資產管理","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力穩定：M&A 宣布量年初至今第一且領先差距創紀錄，股票營收三家最高。定價力擴大：主經紀融資供不應求。份額略受擠壓：EMEA 對 JPMorgan 的領先縮小，2025 年投行費用總額落後 JPMorgan。三者合計判為穩定","peer_na_reason":"同業對照只有 FCF 利潤率，而銀行與券商的自由現金流被交易資產與放款變動主導（高盛 −62.7%、JPMorgan −83.4%、美銀 +73.4%），不能代表 ROIC；同業 ROE／ROTCE 事實表未涵蓋","threats":[{"level":"🟡","text":"JPMorgan 在投行費用總額領先，並在 EMEA 縮小 M&A 份額差距；屬點對點的份額競爭，尚未動搖第一名地位","p":"30%","evidence_refs":["competitive_share_entrants#0","end_markets#6","competitive_share_entrants#1"]},{"level":"🟡","text":"代幣化、預測市場與代理式交易可能侵蝕做市價差；Solomon 稱目前規模很小，高盛已參與 DTCC 代幣化服務並自建 GS DAP，屬可吸收的技術變化","p":"15%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"公開債市承銷往私募信貸移轉，可能壓低承銷費率；高盛同時擁有私募 IG 與另類資產平台，兩邊都接得住，風險在費率而非份額","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"企業併購與融資需求真實存在（AI 資料中心建設估計到 2032 年需逾 10 兆美元），但可以延後：Solomon 坦言 9 月有幾檔 IPO 因估值比預期低 10–15% 而暫緩，私募贊助商也選擇用延續基金延後退場"},{"item":"決策層級","level":"🟢","text":"顧問的選擇權在董事會與執行長手上，看的是關係與聯盟排名，不看報價；年初至今 M&A 宣布量領先第二名約 4,300 億美元，顯示最大型交易的替代性很低"},{"item":"價值鏈分配","level":"🟡","text":"融資端定價權在高盛（股票融資需求超過產業供給）；顧問與承銷端，大型交易常由多家共同顧問分費，私募信貸也在分走債務承銷的利潤，整條價值鏈的分配並非單向有利"},{"item":"社會容忍度","level":"🟡","text":"超額報酬依賴監管資本規則：Basel III 終局與 G-SIB 重提案目前往放寬方向走，CFO 希望年底前定案，但期中選舉後政策可能轉向；1MDB 證券集體訴訟已認證集體，CDS 反壟斷案仍在進行，屬政策與法律容忍度風險"}],"roiic":18.7,"reinvest_rate":15,"endo_ceiling":2.8,"formula_note":"銀行不適用資本支出公式，改用保留盈餘率代替再投資率。3Q26 淨利 52.94 億美元，扣普通股股利 14.9 億與回購 30 億，保留 8.04 億，保留率約 15%（未扣優先股股利）。增量報酬以 3Q26 年化 ROE 18.7% 代替，因為增量值事實表未涵蓋。內生成長上界＝18.7%×15%≈2.8%；加上回購年化約 4.7% 的減股效果，每股上界約 7.5%"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"FCF 利潤率","GS":-62.71,"JPM":-83.39,"MS":-25.44,"BAC":73.37,"WFC":22.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"JPM","fcf_margin":-83.39,"strategy_note":"2025 年投行費用總額第一（101 億美元，高盛 82 億），EMEA M&A 份額差距正在縮小，是最直接的份額威脅；3Q26 股票營收約 50 億美元，年增 49%","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MS","fcf_margin":-25.44,"strategy_note":"3Q26 股票營收 58 億美元，年增 41%，低於高盛的 64.4 億；財富管理規模更大，是資產與財富管理端的主要對照","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BAC","fcf_margin":73.37,"strategy_note":"全能型銀行，靠存款成本支撐融資，在大型顧問案上不是主戰場對手；表內 FCF 利潤率為正，反映的是存放款結構，與競爭力無關","period":"TTM ending 2026-06-30（4季加總）"},{"name":"WFC","fcf_margin":22.09,"strategy_note":"以商業銀行業務為主，投行份額小，對高盛的顧問與做市核心幾乎不構成威脅","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（交易量、融資餘額、AUS 淨流入）為主，價（主經紀定價）次之，回購每年減股約 4–5%，資產管理收購的貢獻小","runway_years":"事實表未涵蓋滲透率，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界 2.8%＝增量報酬 18.7%（以 3Q26 年化 ROE 代替）×保留率 15%；加上回購約 4.7% 後，每股上界約 7.5%","segments":[{"item":"Global Banking & Markets","value":"3Q26 淨營收 134.6 億美元，年增 32%、季減 13%；前三季 segment ROE 23.5%；週期敏感"},{"item":"Asset & Wealth Management","value":"3Q26 淨營收 50.5 億美元，年增 14%；管理及其他費用 36 億美元，年增 22%；另類 AUS 4,910 億美元，年增 26%；全年募資預期約 1,500 億美元"},{"item":"Platform Solutions","value":"3Q26 淨營收 1.7 億美元，年減 72%，主因 Apple Card 貸款組合減值；消費金融持續縮減中"}],"decay_signals":[{"item":"EPS 成長顯著高於營收成長（差距大於 5pp）","lit":true,"text":"2025 年 EPS 年增 26.6%（40.54→51.32），營收年增 8.9%"},{"item":"FCF/NI 連兩年低於 0.75","lit":false,"text":"數字上連三年為負，但銀行的自由現金流被交易資產與放款變動主導，這個訊號不適用"},{"item":"核心市占近 12 個月縮減","lit":false,"text":"M&A 宣布量領先差距創紀錄；只有 EMEA 對 JPMorgan 的領先縮小，屬部分訊號"},{"item":"產業估值倍數近三年系統性下移","lit":null,"text":"事實表未涵蓋"},{"item":"SBC/營收大於 5% 且逐年上升","lit":null,"text":"事實表未涵蓋"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主體是內生的交易、融資與管理費；已知金額的收購合計約 27 億美元，約占市值 1%，不承重"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近期資產管理收購（Industry Ventures、Innovator、NEOS、LCN）尚無已實現報酬揭露；前一輪消費金融擴張以退場收場，Platform Solutions 3Q26 營收年減 72%；已實現 ROIIC 事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"3Q26 回購均價 1,048.73 美元，FY2026 共識 EPS 67.78，盈餘收益率約 6.5%；10 年期公債約 5%（Solomon 2026-10-13 法說口述）加 2% 為 7%，未過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 金額與授予股數事實表未涵蓋","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY2026 共識 EPS），輔以 trailing 本益比的年度端點分位；同業本益比與有形淨值倍數事實表未涵蓋","tier":"大型投行與券商（與 MS、JPM 投行部門同一層級）","peers":{"expanded":false,"reason":"事實表的同業對照只有 FCF 利潤率，對銀行沒有估值意義；同業本益比與 P/TBV 事實表未涵蓋"},"fwd_pe":13.0,"peg":0.91,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 13.0 倍、trailing 12.67 倍，四個年度端點分位 30%（五年分位事實表未涵蓋）；以 2025 年 EPS 計為 17.2 倍。PEG 0.91 被週期跳升墊高，以 2026→2028 成長率計約 2.0。便宜與否取決於分母，結論中性 🟡","upside_short_pct":3.3,"upside_mid_pct":19.8},"trap_analysis":{"verdict":"🟡","label":"週期高處的獲利被誤當常態"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"3Q26 全球 M&A 量季減 41%；投行積壓較 2Q 末下降；聯準會 9 月升息、市場預期再緊縮約 75bp；10 年期公債一季上升約 75bp","assumption":"活動只是從前十分位降到前四分位，不會跌破中位數","consequence":"若 2027–2028 年像 2022–2023 年一樣收縮，EPS 會從 68 美元掉到 46–50 美元，倍數壓到 10 倍，股價約 460–500 美元；從現價算虧約 45%，若加上之前從 1,082 美元的跌幅，接近虧一半。這個故事與唯一致命點相同","ruling":"採納：Bear 機率定為 30%，並把唯一致命點設在單季營收跌破 140 億美元","watch":"每季淨營收與投行積壓方向；每月全球 M&A 宣布量","evidence_refs":["end_markets#5","supply_demand_durability#0","supply_demand_durability#3"],"fact_refs":["f_kpi0_net_revenues_gaap","f_kpi11_management_guidance"]},{"view":"論點成功但股東經濟變差","evidence":"融資收入占 FICC＋股票營收逾 40%；放款組合季增 6% 至 2,760 億美元；3Q26 撥備 3.68 億美元含個別減值；CET1 緩衝從 150bp 縮到 100bp；CFO 稱 SLR 的大幅延展已經完成","assumption":"耐久收入的增加不需要更多槓桿，也不會帶來更多信用損失","consequence":"即使耐久收入占比真的升到五成，它也是靠資產負債表換來的；去槓桿時融資收入、撥備與資本緩衝會同時惡化，ROE 的谷底未必如管理層所說那麼高。過去的消費金融擴張也是成長了、股東卻賠錢的例子","ruling":"部分採納：Poonawala 在法說上提出同樣的質疑，Solomon 只回答要看 3–5 年，沒有給出下行時的數字；列為 R3 並設撥備門檻","watch":"單季撥備是否超過 7.5 億美元；CET1 緩衝是否低於 50bp；融資收入季減幅度","evidence_refs":["end_markets#3"],"fact_refs":["f_kpi6_provision_for_credit_los","f_kpi8_cet1_ratio_standardized_"]},{"view":"價格已反映太多","evidence":"前瞻本益比 13 倍是用週期高處的分母算的，以 2025 年 EPS 計為 17.2 倍；財報前 30 天 EPS 預估 17 次下修、0 次上修；FY1 共識三個月下修 5.4%；分析師稱股價約為有形淨值 3 倍","assumption":"市場會用今年的 EPS 給倍數","consequence":"如果市場改用跨週期 EPS 定價，就算 EPS 不跌，倍數也會被壓縮","ruling":"採納：便宜的論證不成立，不追價，改等事件證據","watch":"財報後的共識快照是否回補；股價對有形淨值的倍數（資料缺口）","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_pe_current","f_fwd_pe_latest"]}],"max_dd":{"lo":-50,"hi":-28,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1082.57 → 本次 881.26（-18.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1082.57","side_b":"本次 price_at_dd=881.26","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,082.57 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,082.57 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 1,082.57 美元：Bull 價 1,530、Bear 價 630，五年期望值 −5.5%，基準年化 −0.5%，不對稱比 0.66","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.66。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,082.57 美元：五年期望值 −5.5%，基準年化 −0.5%，不對稱比 0.66","side_b":"本次情境、股價 881.26 美元：五年期望值 +16.1%，基準年化 3.7%，不對稱比 1.72","ruling":"再換股價、情境不動：起點價下跌 18.6%，五年期望值多 21.6 個百分點，基準年化多 4.2 個百分點，不對稱比由 0.66 升到 1.72。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與綜合訊號，前份對本份","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份（2026-06-15，股價 1,082.57 美元）估值結論 🔴，綜合訊號 B","side_b":"本份股價 881.26 美元，FY2026 共識本益比約 13 倍；估值結論改為 🟡，綜合訊號維持 B","ruling":"估值轉為中性，完全來自股價下跌約 19%；基本面沒有變好到值得升級，也沒有壞到需要降級。分母有爭議，所以價格下跌不轉成加分","evidence_level":"硬數據","settle_metric":"4Q26 與 1Q27 季淨營收","if_then":["若兩季淨營收各 ≥160 億美元，則估值結論可往偏便宜方向重評","若單季淨營收跌破 140 億美元，則以 2025 年 EPS 為分母重算，估值結論回到偏貴"],"evidence_refs":[]},{"axis":"前份未產出的欄位改由本份方法填入","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","rearm_trigger","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位皆為空值（舊格式未產出）","side_b":"本份：護城河方向 →、五年後成長空間 🟡、類型為金融、循環位置為晚循環、重新進場條件為事件錨；情境機率 20／50／30 與最大回撤 −28% 至 −50% 由本份情境樹產生；定期投入的裁決與角色由程式產出","ruling":"不是判斷改變，而是前份沒有這些欄位；本份是首次給值，下一份起才能比較漂移","evidence_level":"方法說明","settle_metric":null,"if_then":["若下一份任一欄與本份不同，則逐欄歸因到價格、新證據或方法"],"evidence_refs":[]},{"axis":"價值陷阱風險由 🟢 改為 🟡","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱風險 🟢","side_b":"本份 🟡：2025 年 EPS 成長 26.6%，遠高於營收的 8.9%；財報前 EPS 預估 17 次下修、0 次上修；3Q26 全球 M&A 量季減 41%；投行積壓已從五年高點回落","ruling":"採 🟡：一個衰退信號亮燈，加上活動轉弱的新證據；還不到 🔴，因為 3Q26 EPS 17.01 美元遠高於共識，管理費仍年增 22%","evidence_level":"硬數據","settle_metric":"FY2027 共識 EPS 在財報後是否續降","if_then":["若財報後共識再下修超過 5%，則改判 🔴，並把 Bear 機率調到 35%","若財報後共識回補到 70 美元以上，則維持 🟡"],"evidence_refs":["capital_markets_pricing#2","end_markets#5"]},{"axis":"Single Thing 由空白改為單季營收門檻","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"某一季全公司淨營收跌破 140 億美元（低於 2025 年季均約 146 億）","ruling":"Single Thing 新設：情境樹裡最大的單一敏感項是營收週期，所以用季營收的水位做二元事件；發生時減碼至半倉並重跑研究","evidence_level":"方法說明","settle_metric":"每季 8-K 淨營收","if_then":["若單季淨營收跌破 140 億美元，則減碼至半倉並重跑研究","若連兩季 ≥160 億美元，則依重新進場條件處理"],"evidence_refs":[]},{"axis":"減碼與清倉門檻、重新進場條件的變動","cause":"方法變動","prior_field":["kill_metrics","rearm_trigger"],"side_a":"前份風險一的警戒：GBM 季度淨收入連 2 季 YoY < −15% → 減倉；風險二：年度募資 < 600 億美元連 2 年；風險三：P/TBV 跌破 1.5 倍；前份未設正式減碼門檻與重新進場條件","side_b":"全公司季淨營收連 2 季年減 >15% → 減碼；單季跌破 140 億美元 → 減碼至半倉；管理費年增 < 5% 連 2 季、年度募資 < 600 億美元連 2 年、P/TBV 跌破 1.5 倍三條沿用前份；新增撥備 > 7.5 億美元與 CET1 緩衝 < 50bp。重新進場改為：4Q26 與 1Q27 季淨營收各 ≥160 億美元且積壓不再下降","ruling":"把 GBM 口徑改成全公司口徑，因為全公司數字已含耐久收入的緩衝，更能反映股東實際承受的波動；前份三條門檻全部保留，其中 P/TBV 因事實表未涵蓋有形淨值，標為資料缺口而不退休；清倉只保留給訴訟出現刑事介入","evidence_level":"方法說明","settle_metric":"每季 8-K","if_then":["若連 2 季全公司營收年減 >15%，則減碼","若出現刑事介入或和解金額超過 50 億美元，則清倉檢討"],"evidence_refs":[]},{"axis":"投行積壓的說法：管理層對財報稿","cause":"新證據","prior_field":null,"side_a":"Q2 法說（2026-07-14，Solomon）：投行積壓升到五年最高；Q3 法說（2026-10-13，Solomon、Coleman）：積壓仍非常強勁，顧問的高額認列大致被股權承銷的補充抵銷","side_b":"3Q26 8-K：投行費用積壓較 2Q26 末下降，也較 2025 年底略降","ruling":"可調和，屬程度差異：以申報文件為準，積壓已從高點回落，管理層的用語偏樂觀。結論是 2027 年投行費用的年增會明顯放慢","evidence_level":"硬數據","settle_metric":"4Q26 投行費用與財報稿的積壓描述","if_then":["若 4Q26 財報稿稱積壓再降，則 Bear 機率調到 35%","若稱積壓回升，則維持現有機率"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"共識下修與財報大幅超預期","cause":"新證據","prior_field":null,"side_a":"財報前 30 天 EPS 預估 17 次下修、0 次上修；FY1 共識三個月內從 71.67 降到 67.78","side_b":"3Q26 EPS 17.01 美元，遠高於 LSEG 共識 13.02 美元；扣除慈善捐款前約 18 美元","ruling":"可調和：共識快照停在財報前的 10-08，尚未反映財報後的回補；但超預期部分包含偏高的績效費（管理層預期 4Q 仍偏高），可持續性未證。不採信也不否定，記為監測","evidence_level":"硬數據","settle_metric":"財報後下一份共識快照的 FY2026 與 FY2027 EPS","if_then":["若下一份快照的 FY2027 EPS 低於 70 美元，則確認下修趨勢，價值陷阱改判 🔴","若回到 73 美元以上，則撤回下修疑慮"],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#0"]},{"axis":"Platform Solutions 指引落空","cause":"新證據","prior_field":null,"side_a":"Q2 法說（2026-07-14，Coleman）：Platform Solutions 下半年各季營收與 Q2 大致相當","side_b":"3Q26 Platform Solutions 營收 1.7 億美元，年減 72%，主因 Apple Card 貸款組合減值","ruling":"管理層的指引落空，但金額不到全公司營收 1%；記為前一輪資本配置失誤的尾巴，納入資本紀律風險的監測，不改變論點","evidence_level":"硬數據","settle_metric":"Apple Card 轉移完成與後續減值","if_then":["若 4Q26 再認列減值且金額超過 5 億美元，則資本配置評語下修","若轉移完成且無新減值，則結案"],"evidence_refs":["end_markets#3"]},{"axis":"觀望，或現在就買","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：3Q26 EPS 17.01 美元對共識 13.02 美元；耐久收入約 45%；M&A 領先差距創紀錄；贊助商 M&A 仍低於歷史均值，是尚未兌現的上行；全年募資上修到約 1,500 億美元；股價已從 6 月的 1,082 美元跌 19%，RSI 34","side_b":"等待的理由：分母處在週期高處，以 2025 年 EPS 計為 17.2 倍；投行積壓與全球 M&A 量已在回落；聯準會升息；Base 五年報酬年化只有約 5–6%，上下檔不對稱比率不到 2","ruling":"不可調和，選擇觀望。關鍵限制是不知道今年的獲利是不是週期頂點，而這要靠兩季財報的營收水位來解，不是靠價格","evidence_level":"硬數據","settle_metric":"4Q26 與 1Q27 季淨營收與投行積壓方向","if_then":["若 4Q26 與 1Q27 季淨營收各 ≥160 億美元且積壓不再下降，則重跑研究並建立首倉","若股價先漲回 1,000 美元以上而營收條件未到，則不追","若股價跌破約 763 美元（FY2027 共識 EPS 的 10.5 倍），而季營收仍 ≥150 億美元且撥備 ≤7.5 億美元，則分批反買","若季營收連 2 季年減 >15%，則不進場，並把 Bear 機率調到 35%"],"evidence_refs":["end_markets#5","capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"季淨營收守在 150 億美元以上，驗證這是降溫而不是崩落","type":"假設驗證","maps_to":"H1","metric":"全公司季淨營收","threshold":"≥150 億美元","action":"維持觀望，等重新進場條件","source_freq":"每季 8-K","date":"2027-01"},{"n":2,"text":"資本市場回落轉為收縮","type":"風險","maps_to":"R1","metric":"全公司季淨營收年增率","threshold":"連 2 季 < −15%","action":"減碼；未持有則不進場","source_freq":"每季 8-K","date":null,"evidence_refs":["end_markets#5"]},{"n":3,"text":"單季營收跌回 2025 年季均以下","type":"Single Thing","maps_to":"Single Thing","metric":"全公司季淨營收","threshold":"單季 < 140 億美元","action":"減碼至半倉並重跑研究","source_freq":"每季 8-K","date":null,"evidence_refs":["end_markets#5"]},{"n":4,"text":"兩季財報證明谷底已經抬高","type":"估值rearm","maps_to":"H1","metric":"季淨營收與投行積壓方向","threshold":"4Q26 與 1Q27 各 ≥160 億美元，且積壓不再下降","action":"重跑研究後建立首倉","source_freq":"每季 8-K 與法說","date":"2027-04"},{"n":5,"text":"融資與放款的信用成本上升","type":"風險","maps_to":"R3","metric":"信用損失撥備","threshold":"單季 > 7.5 億美元","action":"停止加碼","source_freq":"每季 8-K","date":null},{"n":6,"text":"1MDB 證券集體訴訟或 CDS 反壟斷案出現不利和解或判決","type":"風險","maps_to":"R4","metric":"和解或判決金額","threshold":"> 50 億美元，或政府機關新立案","action":"減碼；若有刑事介入則清倉檢討","source_freq":"10-Q 法律程序揭露","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0","regulatory_antitrust#0","regulatory_antitrust#1"]},{"n":7,"text":"資本紀律失守：大型收購或資本緩衝過薄","type":"風險","maps_to":"R2","metric":"單筆收購對價、CET1 高於要求的緩衝","threshold":"單筆 > 市值 5%（約 128 億美元），或緩衝 < 50bp","action":"停止加碼","source_freq":"8-K 與季報","date":null,"evidence_refs":["end_markets#3"]},{"n":8,"text":"價格先跌、基本面未壞時分批反買","type":"加碼","maps_to":"H1","metric":"股價與季淨營收、撥備","threshold":"股價 < 約 763 美元，且季營收 ≥150 億美元、撥備 ≤7.5 億美元","action":"分批反買","source_freq":"每日股價、每季 8-K","date":null},{"n":9,"text":"4Q26 財報後複審","type":"複審日期","maps_to":null,"metric":"全年財報與投行積壓","threshold":"財報公布","action":"重跑研究","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"全公司季淨營收","bear_threshold":"單季 < 140 億美元（低於 2025 年季均約 146 億）","window":"單季","source":"每季 8-K 財報稿","last_status":"ok"},{"metric":"全公司季淨營收年增率","bear_threshold":"連 2 季 < −15%","window":"2 季","source":"每季 8-K 財報稿","last_status":"ok"},{"metric":"管理及其他費用年增率","bear_threshold":"< +5% 連 2 季（沿用前份）","window":"2 季","source":"每季 8-K 財報稿","last_status":"ok"},{"metric":"CET1 高於監管要求的緩衝","bear_threshold":"< 50bp","window":"單季","source":"每季 8-K 與法說","last_status":"ok"},{"metric":"信用損失撥備","bear_threshold":"單季 > 7.5 億美元","window":"單季","source":"每季 8-K 財報稿","last_status":"ok"},{"metric":"另類資產年度募資","bear_threshold":"< 600 億美元連 2 年（沿用前份）","window":"2 年","source":"法說與 8-K","last_status":"ok"},{"metric":"股價對有形淨值倍數","bear_threshold":"跌破 1.5 倍連 2 季（沿用前份）","window":"2 季","source":"資料缺口：事實表未涵蓋有形淨值","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-3.94, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"4Q26 與 1Q27 季淨營收各 ≥160 億美元，且財報稿稱投行積壓不再下降","exec_line":"觀望：證據到齊後重跑研究，首倉不超過標準倉位的三分之一；價格先漲而證據未到則不追"},"reasoning":{"industry":"3Q26 淨營收 186.8 億美元，年增 23%、季減 8%。分部約 72% 為 Global Banking & Markets（134.6 億，年增 32%），其中股票 64.4 億（年增 72%）、FICC 34.7 億（年增率接近零）、顧問 17 億創單季紀錄；約 27% 為 Asset & Wealth Management（50.5 億，年增 14%）；Platform Solutions 只剩 1.7 億，年減 72%。銀行沒有毛利率口徑，以稅前利益率代營業利益率：7,003÷18,679＝37.5%；前三季效率比 59.4%，扣撥備後薪酬比 30%。依管理層口徑，耐久型收入（管理費、融資、私人銀行）約占年初至今營收 45%，融資收入占 FICC＋股票營收逾 40%。產業時鐘判在 III：CEO 自己說活動從 5–6 月的前十分位降到前四分位，3Q26 全球 M&A 量季減 41%，聯準會 9 月升息，投行積壓較 Q2 末下降；營收仍在高位，但動能已轉弱。供需持久性：週期性將反轉，耐久收入只能緩衝回落幅度，無法抵銷。單點依賴：沒有單一客戶營收集中度揭露（10-K 只揭露放款組合約 81% 在美洲）；真正的單點是資本市場活動本身。公司未提供營收或獲利指引。","moat":"機制是三件事互相加乘：董事會層級的顧問關係（年初至今 M&A 宣布量領先第二名約 4,300 億美元，管理層稱是史上最大差距）、做市與融資的資產負債表規模（股票融資營收年增 96% 創紀錄，Coleman 稱需求超過產業供給）、以及能把交易分配給自有公私募資金池的資產管理平台（AUS 4.1 兆美元，長期淨流入連續 35 季）。可證方向：份額軸偏正，2026 上半年 EMEA M&A 份額為 2018 年以來同期最高、全球 M&A 份額 38%，3Q26 股票營收也高於大摩與小摩；偏負的是 2025 年 LSEG 投行費用總額排第二（82 億對 JPMorgan 101 億），且 EMEA 對 JPMorgan 的領先比 2025 上半年的 11 個百分點更窄。執行力評 8、定價力評 7，等級 B：銀行業允許綜合評分，但同業 ROIC spread 取不到，不給到 8 分以上。報酬持續期：3Q26 年化 ROE 18.7%、前三季 20.7%，屬高利益率×低周轉，主要靠槓桿撐起；再投資空間有限，內生成長上界約 2.8%，多數盈餘以股利與回購退回股東。","growth":"成長來源以量為主（交易量、融資餘額、AUS），價為次（主經紀定價），再加上小規模的資產管理收購與回購減股。三年共識 EPS CAGR 為 14.3%（FY2025A 51.32 → FY2028E 76.73，Koyfin 2026-10-08 快照；分析師家數事實表未涵蓋），但其中多數來自 2026 年單年 +32% 的週期跳升；2026→2028 只有約 6.4%/年。內生上界 2.8%，缺口約 11.5pp，可以歸因：回購約 4–5pp，其餘來自利潤率擴張與週期性營收上揚（效率比改善 270bp、薪酬比降到 30%）。2026 年之後的共識 6.4%，大致落在每股上界約 7.5% 以內。Solomon 在 3Q 法說自己說，不認為未來五年營收還能維持 2022 年以來 11% 的年複合成長。衰退信號亮一個：2025 年 EPS 年增 26.6%、營收只增 8.9%，差距大於 5pp。長期成長性與價值陷阱風險都判 🟡。","governance":"3Q26 普通股股利 14.9 億美元加回購 30 億，合計 44.9 億，約占淨利 52.94 億的 85%。回購從 Q2 的 40 億放慢到 30 億，CET1 從 12.9% 降到 12.4%，高於要求的緩衝從 150bp 縮到 100bp，仍在管理層承諾的 50–100bp 區間上緣。季股利 5 美元，年增 25%。法說上有分析師直接質疑公司在約 3 倍有形淨值的價位大量回購。資產管理收購（Industry Ventures 6.65 億美元另加至多 3 億或有對價、Innovator 約 20 億，NEOS 與 LCN 金額未揭露）已知合計約占市值 1%，不承重。前一輪消費金融擴張以出售 Apple Card、GM 卡收場，Platform Solutions 3Q26 仍在認列減值。銀行的 FCF/NI 沒有意義；SBC 金額事實表未涵蓋。","valuation":"前瞻本益比 13.0 倍（881.26÷67.78），trailing 12.67 倍，在四個年度端點中分位 30%；EV/S 對銀行沒有意義。分母本身就是爭點：若獲利回到 2025 年的 51.32 美元，現價本益比是 17.2 倍，不是 13 倍。以三年共識 CAGR 14.3% 計算的 PEG 為 0.91，看似便宜，但 14.3% 是被 2026 單年的週期跳升墊高的；改用 2026→2028 的 6.4%，PEG 約 2.0。股息殖利率 2.04%。同業本益比與 P/TBV 事實表未涵蓋。本研究的 Base 情境：一年後 70 美元×13 倍＝910 美元（+3.3%），五年後 84.5 美元×12.5 倍＝1,056 美元（+19.8%）。估值結論中性。","premortem":"三個方向見反證紀錄：一是資本市場收縮讓 EPS 掉回 46–50 美元、倍數同步壓縮；二是耐久收入靠資產負債表撐起，去槓桿時融資收入、信用損失與資本緩衝會同時惡化；三是 13 倍看似便宜，但分母有爭議，共識在財報前三個月已下修 5.4%。股價 26 週跌 3.9%，RSI 34，沒有過熱，但也還沒有出現投降式賣壓。訴訟方面，1MDB 證券集體訴訟已認證集體、CDS 反壟斷案仍在進行，金額與時點都在事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺三種人的錢：企業付顧問與承銷費，機構與對沖基金付交易價差與融資利息，富人與機構付管理費。錢卡在頂級顧問關係和資產負債表交會的那一個節點，而這個節點本身隨資本市場週期大幅擺動。","moat":"護城河方向穩定（→）：顧問關係網與做市規模仍居第一梯隊，主經紀定價權在擴大；但投行費用總額落後 JPMorgan，EMEA 領先差距也在縮小，兩邊相互抵銷。","growth":"五年後的成長空間中等（🟡）：交易與投行是成熟市場，長期跟著 GDP 與股市市值走；第二曲線是另類資產與財富管理，但已是規模化業務，不是新的 S 曲線。","capital":"資本配置中等偏弱：股利與回購用掉約 85% 的季淨利，但回購均價 1,049 美元對應的盈餘收益率約 6.5%，低於 7% 的門檻；收購規模小，報酬未揭露。","valuation":"現價要求 2026 年約 68 美元的 EPS 是新的常態，之後每年再成長約 6%。這只有一半可信：耐久收入確實抬高了谷底，但今年的獲利有相當部分來自前十分位的市場活動。","how_wrong":"最可能看錯的地方，是把 2026 年的週期高處獲利當成常態；其次是把融資業務當作耐久收入，實際上它放大了週期與信用風險。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 4Q26 與 1Q27 財報：季淨營收各 ≥160 億美元，且投行積壓不再下降，證明 2026 年的獲利不是週期頂點","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"金融","price_at_dd":881.26,"week26_return_pct":-3.94,"consensus_rev_3m_pct":-5.43,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026 共識 EPS 67.78 包含上半年前十分位的資本市場活動，以及 3Q 偏高的績效費；若回到 FY2025 的 51.32，現價本益比是 17.2 倍而非 13 倍，因此不採用便宜的論證"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉","impact":"中","watch":"選後監管與併購審查態度是否轉向；Solomon 稱客戶並未因選舉觀望"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"Basel III 終局與 G-SIB 重提案是否在年底前定案","impact":"中","watch":"資本要求下降的幅度，以及回購空間是否擴大"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"4Q26 財報與法說","impact":"高","watch":"季淨營收是否 ≥160 億美元、投行積壓方向、績效費與第二筆慈善捐款"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"1Q27 財報與法說","impact":"高","watch":"重新進場條件的第二季驗證；贊助商 M&A 是否開始回升"}],"_projected_from":"v19"}
```
