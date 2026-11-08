你是 stock-analyst v20 的**散文層（prose）agent**，標的 ANET（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：ANET　日期：2026-11-08　archetype：None　前份裁決：2026-08-05　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1456B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（576B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（992B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1474B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1145B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（420B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（765B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2342B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4143B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2918B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1456           3881-5544      5 條（2–6 內）  
s3                  8000         576           5197-7424      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3611          7972-11389      5 條（2–6 內）  
s6                 11000         420          7406-10580      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         765           1914-2735      5 條（2–6 內）  
s10                 5000        2342           1861-2658      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2918           2000-2082      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4868B；至少需散文≈40.13KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65%
−60%
−60
−50%
−45%
−40%
−40
−36%
−34%
−20
−18.9%
−16%
0
0.26%
0.4
0.7%
1
1.007
1.01
1.09
1.1
1.20
1.21
1.22
1.29
1.38%
1.381
1.44
1.5%
1.6
1.7
1.76
1.9%
1.92
02
2%
2
2.75
3%
3
03
3.33
3.8%
3.9%
4%
04
4
4.14%
4.28
4.3%
4.5
4.6
$4.61
4.61
4.7
5
5%
05
5.1
5.2
5.3
5.4
5.44
5.5
5.64
5.9
6
6%
06
6.4
6.7%
6.99
7
7.2
7.5
08
8
8%
8.179
8.4
8.6
8.8%
8.85%
9
9.5
10%
10
10.4
10.8
11%
11
11.2%
11.4
11.46%
12.0%
12%
12
12.5
12.69
12.78
12.8
12.99
13%
13
13.4%
13.9
14%
14
14.12%
14.6%
15
15%
15.3
16%
16.94
17%
17
17.5%
18%
18
18.15
18.7%
18.9%
19%
20
20%
20.16%
20.4%
20.48
20.48%
20.5%
20.7%
21%
22
23
24
25
25%
25.36%
25.9%
26%
26
26.5%
26.5
27.8%
28%
28.3
29.3
30
30%
30.28
30.3
31.4
32
33
34.6%
34.86%
35
36
36.5%
36.58
36.73%
37.93
38%
39
39.91
40
40%
42%
42
42.2%
42.82%
43.2%
43.2
43.36
43.83%
44%
44.07%
44.1%
45
45%
45.7
45.79
46%
47%
48
49%
49
49.1%
50%
52%
52
55.2%
57
58.5%
59
60%
62%
62.88%
63.4%
63.6%
64%
64.52%
65
65.2%
65.6%
68
68.4
69
69%
70
76.8
77
81
85
85.4%
85.5
90
93.5
95
97
100%
100
103
109
113
114
126
133
143
143.59
144
150%
157.84
$160.55
161
$161
164
170
170.8
180
185
190
195
200
208
210
210.51
216
220
238
289
345
390
421
480
500
710
2025
2026
2027
2028
2030
7800
20261108
2,000
2,250
8,600
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
{"meta":{"ticker":"ANET","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Arista Networks"},"oneliner":"Arista 把 2027 年營收財測抬到約 185 億美元，股價卻比 8 月低 19%，FY2 本益比降到 30 倍；AI 需求與系統層優勢仍在，但份額被 Nvidia 超過、毛利率年減，適合分批，不宜一次買足。","thesis":{"H":[{"id":"H1","text":"AI 後端與跨資料中心網路需求撐住 2027 年財測。","2y":"FY2027 營收 ≥180 億美元，AI fabrics ≥65 億美元。","5y":null,"10y":null,"threshold":"FY2027 營收 ≥180 億美元；AI fabrics ≥65 億美元","source":"公司季報與法說，每季","drift_rule":"累計營收相對 185 億美元路徑，連 2 季偏離 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉。"},{"id":"H2","text":"Nvidia 拿走訓練叢集份額，但 Arista 在跨資料中心骨幹、前端與企業仍靠 EOS 勝出，五年內資料中心乙太網路份額不跌破 15%。","2y":null,"5y":"FY2031 資料中心份額 ≥15%，前兩大客戶維持 10% 以上，或由新客戶補上。","10y":null,"threshold":"IDC 資料中心份額近端 ≥17%，五年 ≥15%","source":"IDC 季度追蹤；10-K 客戶集中度","drift_rule":"份額相對門檻連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉。"},{"id":"H3","text":"園區與企業資料中心形成第二條曲線，AI 消化期時整體營收不會年減。","2y":null,"5y":"FY2030 園區營收 ≥40 億美元。","10y":null,"threshold":"FY2027 園區 ≥20 億美元，FY2030 ≥40 億美元","source":"公司法說與年報；若停止揭露則標資料缺口","drift_rule":"園區營收相對路徑連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉。"}],"R":[{"id":"R1","text":"Nvidia 與白牌路線侵蝕大客戶份額：Spectrum-X 進到 Meta，微軟與 Meta 用 SONiC、FBOSS 保持多供應商。","h_ref":"H2","clock":"🔥","threshold":"IDC 資料中心份額連兩季 <17%，或 10-K 揭露任一大客戶占比跌破 10%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","competitive_share_entrants#3","competitive_share_entrants#4","customer_second_source#0","customer_second_source#1","substitute_technology#0","substitute_technology#2","end_markets#2"]},{"id":"R2","text":"AI 資本支出進入消化期：客戶集中、能見度兩季，採購承諾與存貨在高點時需求反轉。","h_ref":"H1","clock":"⚡","threshold":"FY2028 首版營收成長 <15%，或存貨季增減營收季增連兩季 >10 個百分點","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R3","text":"供應與成本壓縮毛利率：記憶體缺貨、Broadcom 依賴、關稅無法完全轉嫁，製造地也暴露在貿易措施下。","h_ref":"H1","clock":"🔥","threshold":"毛利率連兩季 <62%","evidence_refs":["supply_demand_durability#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R4","text":"產品世代與架構替代：CPO、NPO 與 NVLink 主導的 scale-up；2026-11-03 CEO 稱 CPO 要到 2028～2030 年，scale-up 2028 年量產，交付落後會失去位置。","h_ref":"H2","clock":"🐢","threshold":"2028 年底 scale-up 仍未量產；CPO 滲透率事實表未涵蓋，屆時以法說與第三方追蹤為準","evidence_refs":["substitute_technology#1","competitive_share_entrants#1"]}],"single_thing":{"description":"2027 年 11 月法說給出的 2028 年首版營收成長指引低於 15%（若公司延續今年提前給隔年財測的做法）。","why_fatal":"這個數字同時反映 AI 消化、大客戶移轉與份額流失。FY2028 營收每少 10%，EPS 約少 12%，再疊加本益比由 30 倍降到 20 倍以下，股價可跌 40%～50%；相較之下毛利率每少 1 點，EPS 只少約 2%。","if_happens":"減碼至半倉；若同時有大客戶占比跌破 10% 且營收成長低於 15%，則清倉；不再用 2028 年以後的 scale-up 當續抱理由。","how_monitor":"領先指標看採購承諾（114 億美元）、存貨周轉（1.6）、產品遞延收入、微軟與 Meta 資本支出指引及 IDC 份額；事件日約在 2027 年 11 月第一週。","probability":"25%（12～24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":30.28,"peg_fy2":1.09,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.75,"FY2026E":4.28,"FY2027E":5.64,"FY2028E":6.99},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin 共識快照，事實表未標明 GAAP 或非 GAAP；FY2025A 只有 GAAP 稀釋 EPS 可引用，三年年化 36.5% 可能偏高。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ANET_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"營業利益率近 50%、零負債、股本幾乎不膨脹，但需求綁在 AI 資本支出，營收節奏帶循環性。"},"industry":{"clock_phase":"III","sd_verdict_source":"零組件缺貨、廠商簽多年採購約（Arista 承諾 114 億美元）、S&P 預估 Meta 2026～2028 年自由營運現金流為負，需求強但資金來源開始吃緊，屬過熱期特徵；此判斷不看股價。供需持久性：缺貨到 2027 年屬結構性，需求高度屬週期性。","bargaining":{"up":"偏弱：Broadcom 為主要晶片來源且無保供合約，靠採購承諾換貨。","down":"偏弱：前兩大客戶占 42%，微軟與 Meta 同時採購他廠，並推 SONiC、FBOSS。","geo":"製造外包在馬來西亞、越南、墨西哥等地，關稅成本可能無法完全轉嫁。"},"profit_pool_dir":"利潤池往 AI 後端與跨資料中心骨幹移動；Nvidia 以 GPU 加網路的整套方案分走訓練叢集那一塊。五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"管理層 2030 年可觸及市場","value":"超過 2,000 億美元（2026-11-03 法說，管理層口徑，未經第三方驗證）"},{"item":"FY2026 營收財測占 2030 年市場","value":"約 6.7%（133 億÷2,000 億）"},{"item":"IDC 2Q26 資料中心乙太網路份額","value":"18.7%（1Q26 為 20.7%）"},{"item":"IDC 2Q26 整體乙太網路交換器份額","value":"13.4%"},{"item":"五年前份額、分段 CAGR、營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"單一作業系統 EOS 加 CloudVision，靠品質、低漏洞數、不停機升級與跨資料中心大型系統建立轉換成本；AI 時代再加上對多種加速器的中立性。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Q3 非 GAAP 營業利益率 49.1%，2026 年財測四度上調。定價力穩定：毛利率年減但仍在 62%～64% 區間，2026-08-04 CEO 說漲價效果要到年底或明年才反映。IDC 資料中心份額由 20.7% 降到 18.7%，領先者份額下滑，因此不往上調。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，價差改用營業利益率與 FCF 利潤率。","threats":[{"level":"🔴","text":"Nvidia 以 Spectrum-X 綁 GPU 銷售，已居資料中心乙太網路第一，並進入 Arista 最大客戶之一的多年部署。","p":"40%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","competitive_share_entrants#4","end_markets#2","substitute_technology#2"]},{"level":"🟡","text":"白牌硬體加 SONiC、FBOSS，加上大型系統廠的垂直整合方案，讓大客戶保有多供應商議價力；2026-08-04 CEO 稱白牌是戰術性方案，適用簡單情境。","p":"30%","evidence_refs":["competitive_share_entrants#0","customer_second_source#0","customer_second_source#1","substitute_technology#0"]},{"level":"🟡","text":"下一代架構：CPO、NPO 與 NVLink 主導的 scale-up；管理層稱 CPO 要到 2028～2030 年，scale-up 2028 年才量產，若交付落後會失去位置。","p":"30%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是網路維運、決策者是基建主管、付款者是資本支出預算，三者都成立，AI 叢集不能沒有網路。急迫不等於持久：2026-11-03 CFO 說能見度仍是兩季，S&P 預估 Meta 2027 年資本支出超過 2,250 億美元，同時自由營運現金流為負。"},{"item":"決策層級","level":"🟡","text":"企業客戶以整張網路為決策單位，園區更新週期長，替代性低；大型雲端以網路分層為單位，微軟與 Meta 多供應商採購，替代性高。續約率、漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"稀缺在 GPU、交換晶片與記憶體，Arista 夾在 Broadcom 與大客戶之間，毛利率仍守住 62%～64%。採購承諾由 97 億增到 114 億美元，等於用承諾買供應；若 Nvidia 把網路併入整櫃方案，這段價值會被重新分配。"},{"item":"社會容忍度","level":"🟢","text":"屬企業採購的基礎設施，沒有民生定價壓力；FY2025 10-K 未點名針對 Arista 的反壟斷調查，近十二個月 8-K 也無重大項目。"}],"roiic":"無法計算：投入資本接近零或為負，增量資本的分母沒有意義，事實表也沒有歷年投入資本。","reinvest_rate":"TTM 接近零（FCF 利潤率 42.2% 高於稅後營業利益率約 34.6%）；Q3 單季約 69%（存貨增 7 億、遞延收入減約 1 億、資本支出 1.01 億美元，除以稅後營業利益 12.99 億美元，未計折舊與應收應付變動）。","endo_ceiling":null,"formula_note":"投入資本用 Q3 法說的存貨 32 億美元、DSO 59 天、應付 48 天與遞延收入 68.4 億美元粗算約 −20 億美元，未含固定資產（事實表未涵蓋），ROIC 算術失真。稅後營業利益率 34.6%＝43.83%×（1−21%），投入資本小於 TTM 營收時 ROIC 高於此數。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","ANET":62.88,"CSCO":64.52,"HPE":36.73,"CIEN":44.07,"CLS":11.46,"unit":"%"},{"metric":"營業利益率","ANET":43.83,"CSCO":25.36,"HPE":7.84,"CIEN":14.12,"CLS":8.29,"unit":"%"},{"metric":"FCF 利潤率","ANET":42.2,"CSCO":20.16,"HPE":9.93,"CIEN":13.53,"CLS":2.99,"unit":"%"},{"metric":"研發密度","ANET":12.84,"CSCO":15.1,"HPE":8.85,"CIEN":15.36,"CLS":0.93,"unit":"%"}],"competitors":[{"name":"CSCO","gm":64.52,"om":25.36,"fcf_margin":20.16,"rd_intensity":15.1,"strategy_note":"毛利率與 Arista 接近，營業利益率只有 25.36%，費用結構較重；Arista 在企業與園區搶的是長期主導者的存量。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"HPE","gm":36.73,"om":7.84,"fcf_margin":9.93,"rd_intensity":8.85,"strategy_note":"併入 Juniper 後規模變大，但毛利率 36.73%、研發密度 8.85%，都低於 Arista，短期較難靠研發追趕。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"CIEN","gm":44.07,"om":14.12,"fcf_margin":13.53,"rd_intensity":15.36,"strategy_note":"毛利率 44.07%、營業利益率 14.12%，獲利不在同一級；事實表沒有它與 Arista 直接競爭的證據。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"CLS","gm":11.46,"om":8.29,"fcf_margin":2.99,"rd_intensity":0.93,"strategy_note":"毛利率 11.46%，是代工型利潤結構，可當白牌路線的成本參照，與 Arista 不是同一層競爭。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"以量為主：AI 部署與新客戶；價格尚未反映；併購與回購不是來源。","runway_years":5.3,"runway_post_y5":"🟢","endo_ceiling_basis":"增量 ROIC 乘再投資率的上界無法計算，因投入資本接近零或為負。實際上限是 114 億美元採購承諾能換到的供給、客戶資本支出與份額。","segments":[{"item":"AI fabrics","value":"FY2026 目標 35 億美元，FY2027 約 70 億美元（+100%，基期可能偏低）"},{"item":"園區","value":"FY2026 目標 12.5 億美元，FY2027 約 20 億美元（+60%）"},{"item":"其餘（資料中心前端、服務等）","value":"約 85.5 億美元到約 95 億美元（+11%，由總數倒算）"}],"decay_signals":["毛利率連兩季年減：Q2 63.4% 對 65.6%，Q3 64% 對 65.2%","核心市占縮減：IDC 資料中心份額 1Q26 20.7%、2Q26 18.7%，Nvidia 升至第一"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，近十二個月 8-K 沒有併購項目，這一欄不承重。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近十二個月沒有重大併購；VeloCloud（2025-06-30 完成）的金額與貢獻事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價與十年期公債殖利率事實表未涵蓋，無法判定；Q2 未回購，授權尚餘 8.179 億美元。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數 FY2023 約 12.69 億到 Q3 FY2026 12.78 億，年化約 0.26%，低於 1.5%。","grade":"過"}]},"valuation":{"basis":"FY1 本益比為主，FY2 本益比與 PEG 輔助；終端倍數配終端當年度 EPS，與起點同口徑。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比，無法做倍數對照。"},"fwd_pe":39.91,"peg":1.09,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"由偏貴降到合理偏高：NTM 本益比由前份約 45.7 倍（210.51÷4.61）降到約 31.4 倍。PEG 1.09＝39.91÷36.5%，基期是 GAAP；換成 FY1 到 FY3 的 27.8% 則為 1.44，兩者都在 1～2 的合理區。基準情境五年年化 8.8%，屬中等。沒有到便宜，因為 trailing 本益比仍在 4 個年度端點的 76.8 分位，報酬也沒到 12%。五年分位所需資料事實表未涵蓋，留空。","upside_short_pct":14.0,"upside_mid_pct":26.5},"trap_analysis":{"verdict":"🟡","label":"成長真實但週期風險未消：毛利率連兩季年減、核心份額下滑兩項訊號亮起。"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY2025 前兩大客戶占 42%，前兩大經銷商占應收帳款 52%；S&P 2026-10-30 把 Meta 展望調負，預估 2026～2028 年自由營運現金流赤字 220 億、710 億、390 億美元。","assumption":"假設大型客戶願意繼續舉債擴建，2028 年仍維持高資本支出。","consequence":"五年後虧 50% 最可能的故事：2028 年消化，AI 營收年減，微軟或 Meta 移向 Spectrum-X，採購承諾變損失，本益比由 30 倍降到 17 倍。下行情境終端 93.5 美元，−45%。","ruling":"部分採納，下行機率定 30%。這個故事與唯一致命數字部分重疊，後者是它第一個可量化的訊號。S&P 同時預估 Meta 2027 年資本支出超過 2,250 億美元，近端需求反而支持財測，風險落在 2028 年以後。此信用訊號尚未反映在賣方下修上，因此第一批之後的加碼綁定 IDC 與 Q4 財報。","watch":"微軟與 Meta 資本支出指引；10-K 的 10% 客戶揭露；2028 年首版財測。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 毛利率 64% 低於去年同期 65.2%，FY2027 區間 62%～64%；業界分析認為記憶體缺口 2027 年可能惡化；Broadcom 無保供；關稅可能無法完全轉嫁；研發季增 47%。","assumption":"假設營收翻倍時，毛利率維持 62%～64%、營業利益率維持 49%。","consequence":"AI 贏了，但增量利潤被晶片、記憶體與整櫃夥伴分走。營業利益率每少 1 點，FY2027 EPS 約少 1.9%；降到 44% 約少 10%。","ruling":"採納。基準情境把營業利益率由 49% 逐年降到 45%，不外推當下高點；49% 中有多少屬缺貨期的週期性紅利無法精確拆分，這段不確定性放進下行機率。CFO 把研發跳升連到專案投入，CTO 稱原型費高，列為未證、監測；若研發占營收連兩季高於 11%，這個一次性說法視為不成立。","watch":"毛利率、研發占比、採購承諾與整櫃出貨模式揭露。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","supply_demand_durability#2","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"view":"價格已反映太多","evidence":"FY1 本益比 39.91 倍、trailing 45.79 倍；P/S 18.15 倍、EV/S 16.94 倍，都在 4 個年度端點的 70～77 分位；股價 26 週仍漲 20.48%。","assumption":"假設市場在成長降到 10% 左右時，仍願意給 25 倍。","consequence":"若終端只有 20 倍，基準情境終端 208 美元，五年年化約 4%。","ruling":"部分採納。FY2 本益比 30.3 倍、扣現金 28.3 倍，相對 38%～40% 的財測不算離譜；但基準報酬只有中等，所以只買第一批，不一次買足。","watch":"NTM 本益比 35 倍（約 190 美元）以上不追。","fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_week26_return_pct"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 210.51 → 本次 170.8（-18.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=210.51","side_b":"本次 price_at_dd=170.8","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 觀望 → 本次 進場","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=觀望","side_b":"本次 dca_verdict=進場","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 追蹤 → 本次 衛星","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=追蹤","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 210.51 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 210.51 美元：Bull 價 421、Bear 價 81，五年期望值 +12.0%，基準年化 3.9%，不對稱比 1.1","side_b":"本次情境、股價仍用 210.51 美元：Bull 價 480、Bear 價 93.5，五年期望值 +25.9%，基準年化 4.3%，不對稱比 1.92","ruling":"先換情境、股價不動：五年期望值多 13.9 個百分點，基準年化多 0.4 個百分點。不對稱比由 1.1 變為 1.92。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 210.51 美元：五年期望值 +25.9%，基準年化 4.3%，不對稱比 1.92","side_b":"本次情境、股價 170.8 美元：五年期望值 +55.2%，基準年化 8.8%，不對稱比 3.33","ruling":"再換股價、情境不動：起點價下跌 18.9%，五年期望值多 29.3 個百分點，基準年化多 4.5 個百分點，不對稱比由 1.92 升到 3.33。合計五年期望值比前份多 43.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與裁決隨股價變動","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 210.51 美元，NTM 本益比約 45.7 倍，估值偏貴，結論為觀望。","side_b":"本次：股價 170.8 美元，較前份 −18.9%；NTM 本益比約 31.4 倍，估值合理偏高。","ruling":"變動主要來自股價下跌與共識上修，不是風險消失。裁決與倉位以本次情境重新決定。","evidence_level":"事實表股價與共識。","settle_metric":"NTM 本益比"},{"axis":"價值陷阱評級由綠轉黃","cause":"新證據","prior_field":["trap"],"side_a":"前份：價值陷阱風險低。","side_b":"本次：毛利率連兩季年減，IDC 2Q26 資料中心份額再降到 18.7%，兩項衰退訊號亮起。","ruling":"採納新證據，評級調為黃色。營收、現金流與股本仍健康，尚未到紅色。","evidence_level":"公司法說原話與 IDC 第三方資料。","settle_metric":"毛利率年增減與 IDC 份額","if_then":["若毛利率連兩季低於 62%，則減碼三分之一。","若 3Q26 份額回到 18.7% 以上且毛利率年減幅收斂，則維持分批計畫。"],"evidence_refs":["competitive_share_entrants#3","end_markets#2"]},{"axis":"維持不變的基本面欄位","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合評等為第二級，護城河方向不變，五年後跑道寬，屬品質複利型，未標循環位置。","side_b":"本次全部維持：Q3 財報與 2027 年財測偏正面，IDC 份額與毛利率偏負面，兩邊相抵。","ruling":"估值改善，但護城河仍是 B、長期信心為中、基準報酬只有中等，綜合評等不上調。園區目標 60% 成長與 2028 年 scale-up 支持跑道維持寬。","evidence_level":"法說與事實表。","settle_metric":"IDC 3Q26 份額；FY2026 Q4 財報"},{"axis":"重新進場門檻已達成","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE(NTM) ≤ 35x（以現行 NTM EPS $4.61 計約 $161，隨共識上修同步上移）；週線布林中軌現位 $160.55 同區","side_b":"NTM 本益比 ≤35 倍（現約 31.4 倍，約 190 美元內）可建首批；IDC 3Q26 份額 ≥18.7% 且年底遞延收入年增才加碼。","ruling":"倍數門檻 35 倍不變，舊門檻已達成，價格錨因 NTM EPS 由 4.61 上修到約 5.44 美元而由 161 美元移到約 190 美元。布林中軌資料本次沒有，取消這個錨。新增份額與遞延收入作為加碼條件。","evidence_level":"事實表共識與股價推算。","settle_metric":"NTM 本益比","if_then":["若股價先漲過約 190 美元，而 IDC 與年底遞延收入都還沒驗證，則不追。","若股價跌破 52 週均線 157.84 美元，且基本面門檻都沒觸發，則分批反買。"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份無唯一致命點（欄位為空）。","side_b":"2027 年 11 月法說給出的 2028 年首版營收成長指引低於 15%。","ruling":"本次依新格式首次設定。選這個數字是因為它同時反映 AI 消化、大客戶移轉與份額流失，也是敏感度最大的一項。","evidence_level":"判斷，依情境敏感度推算。","settle_metric":"FY2028 首版營收成長指引"},{"axis":"減碼與清倉門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份無此項門檻（欄位為空）。","side_b":"毛利率連兩季低於 62% 減碼三分之一；2028 年首版成長低於 15% 減碼至半倉；微軟或 Meta 占比跌破 10% 且營收成長低於 15% 清倉。","ruling":"本次依新格式首次設定，以財測下緣與情境敏感度定門檻。","evidence_level":"判斷，門檻來自公司財測區間。","settle_metric":"毛利率、首版財測、10-K 客戶占比"},{"axis":"AI 目標與管理層 8 月說法","cause":"新證據","side_a":"2026-08-04 CEO 稱 AI 目標至少 36 億美元，並說各項數字都會上調。","side_b":"2026-11-03 CFO 回答 AI 仍是 35 億美元、園區 12.5 億美元，全年營收卻由約 126 億上調到 133 億美元；CEO 說實際數字要等年底出貨後才知道。","ruling":"可調和，屬揭露保守，不是需求落差。但 AI 倍增到 70 億美元的基期不可靠：若 2026 年實際 AI 高於 35 億美元，2027 年成長就低於 100%。我只採信總營收 185 億美元，不採信倍增這個說法。","evidence_level":"法說原話，基期待 Q4 揭露。","settle_metric":"FY2026 實際 AI 營收與 2027 年 AI 目標是否同步上修","if_then":["若 FY2026 AI 營收 ≥45 億美元，而 2027 年目標仍是 70 億美元，則停止加碼。","若 FY2026 AI 營收在 35～45 億美元，且 2027 年目標維持或上調，則依計畫加第二批。"]},{"axis":"遞延收入與營收加速","cause":"新證據","side_a":"Q3 營收季增 20.5%，2027 年財測 38%～40%，管理層稱需求是任內最好。","side_b":"遞延收入由約 69 億降到 68.4 億美元，產品遞延收入季減 8,600 萬美元；Bank of America 分析師問兩者是否脫鉤，CEO 未給拆分。","ruling":"可調和。CFO 說流進流出都大，並預期年底餘額高於去年底。這個說法列為未證、監測，不採信也不否定。","evidence_level":"法說原話；2025 年底餘額事實表未涵蓋。","settle_metric":"FY2026 年底遞延收入對 FY2025 年底","if_then":["若年底餘額低於去年底，則停止加碼。","若年底餘額高於去年底，且 Q4 營收達 39 億美元以上，則加第二批。"]},{"axis":"採購承諾與能見度","cause":"新證據","side_a":"2026-11-03 CFO 稱能見度兩季，下半年靠客戶對話與趨勢推估；COO 也說不是每筆訂單都已下。","side_b":"採購承諾 114 億美元（季增 17.5%）、存貨 32 億美元（季增 28%），都快過 Q4 財測季增約 8%，且含多年期記憶體協議。","ruling":"可調和但風險不對稱：缺貨時多訂是理性，消化時就變損失。114 億美元約為 FY2027 推算銷貨成本 68 億美元的 1.7 倍，雖含多年期，仍是最大的表外風險。存貨增速減營收增速，Q3 為 7.5 個百分點。","evidence_level":"法說原話與推算。","settle_metric":"存貨季增率減營收季增率","if_then":["若差距連兩季超過 10 個百分點，則停止加碼。","若 Q4 差距回到 5 個百分點內且營收達標，則維持分批計畫。"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"份額下滑與營收加速","cause":"新證據","side_a":"IDC：Nvidia 自 1Q26 居資料中心乙太網路第一，Arista 份額由 20.7% 降到 18.7%，Meta 與 Nvidia 簽多年合約。","side_b":"Arista：Q3 年增 58.5%，上市以來最快；Etherlink 客戶超過 100 家；7800 跨資料中心平台差異化；企業持續搶份額。","ruling":"可調和：市場擴張且分層。Nvidia 拿 GPU 綁定的訓練叢集，Arista 拿跨資料中心骨幹與企業，份額下降沒有傷到絕對金額。一個季度的變動可能來自出貨時點，所以方向不下調，但列為首要風險。","evidence_level":"第三方季度資料，一季變動。","settle_metric":"IDC 資料中心份額，3Q26 約 2026 年 12 月","if_then":["若 3Q26 與 4Q26 連兩季低於 17%，則停止加碼，護城河方向改為縮減。","若 3Q26 回到 18.7% 以上，則加第二批。"],"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","competitive_share_entrants#4","end_markets#2"]},{"axis":"產業態勢三軸","cause":"新證據","side_a":"競爭惡化：Nvidia 升至第一，白牌與客戶自有作業系統保持壓力。","side_b":"結構轉好：AI 網路由 InfiniBand 轉向乙太網路，加速器變多有利中立供應商，管理層稱 2030 年市場超過 2,000 億美元。","ruling":"雙向拉鋸。其他結構變數中，記憶體缺貨與關稅是主要壓力，反壟斷與通路未見結構變動。","evidence_level":"IDC、10-K、10-Q 與法說。","settle_metric":"IDC 份額與毛利率","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#2","reg_tariff_export#2"]},{"axis":"買賣兩方最強論證","cause":"價格變動","side_a":"現在就買的最強論證：股價比 8 月低 19%，而 2027 年財測高出街頭 10%～15%，FY2 本益比 30 倍已低於前份進場門檻，公司今年四度上調財測。","side_b":"現在就賣的最強論證：這可能是週期高點的獲利。缺貨、長約、漲價與客戶舉債同時出現，兩季能見度卻給了全年財測，份額還在流失。","ruling":"先買三分之一。買方論證有硬數據，賣方論證要到 2028 年才能驗證；但賣方論證無法排除，所以後兩批綁定具名事件。","evidence_level":"事實表與法說，週期判斷不可裁決至 2027 年 11 月。","settle_metric":"FY2028 首版營收成長指引","if_then":["若 2028 年首版成長低於 15%，則減碼至半倉。","若首版成長 ≥20%，且毛利率守住 62%，則維持持股。"]},{"axis":"牛熊機率與最大回撤重新推算","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：牛熊機率 22／32，最大回撤 −65%。","side_b":"本次：牛熊機率 25／30，最大回撤範圍 −40%～−60%。","ruling":"這三欄是情境重建後的判斷，不是股價下跌的機械結果。樂觀機率上調 3 點，依據是 2027 年營收財測約 185 億美元，推得 EPS 約 5.9 美元，比 FY2 共識 5.64 美元高約 5%，差距不大，所以只上調 3 點；下行機率由 32 降到 30，降幅有限，因風險落在 2028 年以後。回撤範圍改由下行情境推算：谷底 FY2028 EPS 4.7 美元配 18～22 倍，約 85～103 美元，對現價 −50%～−40%；若先回到 8 月約 210 美元再跌，約 −60%。對現價的部分會隨起點價下跌而變淺，不代表風險變小。","evidence_level":"機率為判斷，回撤範圍由情境推算；歷史最大回撤事實表未涵蓋。","settle_metric":"FY2028 首版營收成長指引"}],"triggers":[{"n":1,"text":"NTM 本益比在 35 倍以內，先買第一批，目標倉位的三分之一。","type":"估值rearm","maps_to":"H1","metric":"NTM 本益比","threshold":"≤35 倍（現約 31.4 倍，約 190 美元內）","action":"建第一批三分之一","source_freq":"共識與股價，每週","date":"2026-11"},{"n":2,"text":"IDC 3Q26 份額止穩，且 FY2026 年底遞延收入高於 2025 年底，加第二批。","type":"加碼","maps_to":"H2","metric":"IDC 資料中心份額；年底遞延收入","threshold":"份額 ≥18.7% 且遞延收入年增","action":"加第二批至目標倉位三分之二","source_freq":"IDC 每季；公司季報","date":"2027-02"},{"n":3,"text":"股價跌破 52 週均線，但基本面門檻都沒觸發，用最後一批反買。","type":"加碼","maps_to":"R2","metric":"週收盤價","threshold":"<157.84 美元（均線隨時間移動），且第 4、5、6、7 條未觸發","action":"分批反買第三批","source_freq":"週線","date":null},{"n":4,"text":"IDC 份額連兩季低於 17%，不再加碼，護城河方向改為縮減。","type":"風險","maps_to":"R1","metric":"IDC 資料中心乙太網路份額","threshold":"連兩季 <17%","action":"停止加碼","source_freq":"IDC 每季","date":"2027-03","evidence_refs":["competitive_share_entrants#3","end_markets#2"]},{"n":5,"text":"毛利率連兩季低於財測下緣，視為成本轉嫁失敗。","type":"減碼","maps_to":"R3","metric":"非 GAAP 毛利率","threshold":"連兩季 <62%","action":"減碼三分之一","source_freq":"季報","date":"2027-05","evidence_refs":["reg_tariff_export#2","supply_demand_durability#2"]},{"n":6,"text":"存貨成長連兩季明顯快過營收，採購承諾開始變成負擔。","type":"風險","maps_to":"R2","metric":"存貨季增率減營收季增率","threshold":"連兩季 >10 個百分點（Q3 為 7.5）","action":"停止加碼","source_freq":"季報","date":"2027-05"},{"n":7,"text":"2027 年 11 月法說給的 2028 年首版營收成長低於 15%。","type":"Single Thing","maps_to":"Single Thing","metric":"FY2028 首版營收成長指引","threshold":"<15%","action":"減碼至半倉","source_freq":"公司法說","date":"2027-11"},{"n":8,"text":"微軟或 Meta 任一家占營收跌破 10%，同時公司營收成長低於 15%，論點失效。","type":"清倉","maps_to":"H2","metric":"10-K 前兩大客戶占比；營收年增","threshold":"任一家 <10% 且營收年增 <15%","action":"清倉","source_freq":"10-K 每年","date":"2028-02","evidence_refs":["customer_concentration_credit#0"]},{"n":9,"text":"NTM 本益比回到 42 倍以上且獲利預估未同步上修，賣掉部分倉位；前份偏貴時約為 45.7 倍。","type":"減碼","maps_to":"H1","metric":"NTM 本益比","threshold":"≥42 倍","action":"減碼三分之一","source_freq":"共識與股價，每週","date":null},{"n":10,"text":"FY2027 累計營收相對 185 億美元路徑落後 5%，暫停加碼。","type":"假設驗證","maps_to":"H1","metric":"FY2027 累計營收對財測路徑","threshold":"連兩季落後 ≥5%","action":"停止加碼","source_freq":"季報","date":"2027-08"},{"n":11,"text":"FY2026 Q4 財報當週重跑完整判斷。","type":"複審日期","maps_to":"H1","metric":"FY2026 Q4 財報與 2027 年分段財測","threshold":"不適用","action":"重跑完整判斷","source_freq":"法說","date":"2027-02"}],"kill_metrics":[{"metric":"FY2028 首版營收成長指引","bear_threshold":"<15%","window":"2027 年 11 月法說","source":"公司法說","last_status":"unknown"},{"metric":"非 GAAP 毛利率","bear_threshold":"連兩季 <62%","window":"2026 Q4 起逐季","source":"公司季報","last_status":"ok"},{"metric":"IDC 資料中心乙太網路份額","bear_threshold":"連兩季 <17%","window":"每季，約落後一季","source":"IDC 季度追蹤","last_status":"warning"},{"metric":"存貨季增率減營收季增率","bear_threshold":"連兩季 >10 個百分點","window":"每季","source":"公司季報與法說","last_status":"ok"},{"metric":"微軟或 Meta 占營收比重","bear_threshold":"任一家 <10% 且營收年增 <15%","window":"每年 10-K","source":"SEC 10-K","last_status":"ok"}],"decision_out":{"role":"衛星","row_hit":"9","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Nvidia 在訓練叢集的勝利外推到整個資料中心與園區，股價比 8 月低 19%；但 Q3 營收年增 58.5%，份額下降沒有傷到絕對金額，FY2 共識 5.64 美元也低於財測推得的約 5.9 美元，差約 5%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=20.48, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"verdict":"進場","rearm_trigger":"NTM 本益比 ≤35 倍（現約 31.4 倍，約 190 美元內）可建首批；IDC 3Q26 份額 ≥18.7% 且年底遞延收入年增才加碼。","exec_line":"現價附近買目標倉位的三分之一；IDC 3Q26 與 FY2026 Q4 財報都過關再加三分之一；股價跌破 52 週均線且基本面門檻未觸發，用最後三分之一反買；漲過 NTM 35 倍（約 190 美元）不追。"},"reasoning":{"industry":"Q3 FY2026 營收 36.58 億美元，年增 58.5%，GAAP 毛利率 63.6%，非 GAAP 營業利益率 49.1%。正式營收分部事實表未涵蓋；法說給的目標是 2026 年 AI 35 億美元、園區 12.5 億美元，其餘約 85.5 億美元由總數倒算，2027 年三塊約為 70 億、20 億、95 億美元。訂閱型服務與軟體在 Q4 2025 法說占營收約 17%，其餘主要是產品出貨。單點依賴有兩個：FY2025 前兩大客戶占 42%（26%、16%），主力晶片靠 Broadcom 且沒有書面保供。集中度是風險，不是護城河證據；2026-11-03 CEO 預期 10% 以上客戶增加到 3～4 家，方向改善，要等 FY2026 10-K 驗證。供需持久性：缺貨至少延續到 2027 年，屬結構性；需求高度靠客戶擴大資本支出，屬週期性，消化時會反轉。","moat":"機制是一套作業系統從資料中心延伸到園區，品質與不停機升級讓企業客戶換機成本高。可驗證的方向有三個。第一，對 Cisco 的 TTM 營業利益率 43.83% 比 25.36%，FCF 利潤率 42.2% 比 20.16%，毛利率 62.88% 卻略低於 64.52%，領先來自費用效率與規模；同業 ROIC 事實表未涵蓋，只能用利潤率代替。第二，IDC 資料中心份額 1Q26 為 20.7%，2Q26 為 18.7%，Nvidia 2Q26 為 20.4%，領先者份額下滑，方向不能上調。第三，公司 Q3 營收年增 58.5%，明顯加速，但 IDC 3Q26 份額要到 12 月左右才有。Nvidia 的攻擊集中在訓練叢集，屬客群範圍失守，不是整體方向受損；這項負面只記在威脅，不再重複扣方向。三件事分開看：當期屬高利益率、高周轉；四項持續期檢查三黃一綠，超額報酬撐過這輪建置的把握較高，五年後要看份額；增量報酬因投入資本接近零無法計算。反例：若 3Q26 份額繼續下跌，且微軟或 Meta 占比下降，方向就該改成縮減。","growth":"成長以量為主，來自 AI 部署與新客戶；2026-08-04 CFO 說毛利率尚未計入漲價，併購與回購也不是來源。共識 EPS 由 FY2025A 2.75 美元到 FY2028E 6.99 美元，三年年化 36.5%，但基期是 GAAP，共識口徑未標明；FY1 到 FY3 年化 27.8%。EPS 家數事實表未涵蓋，營收共識為 23 位分析師。內生上界無法計算，缺口也就無法量化，長期信心上限為中。可歸因的部分是：FY2025 到 FY2027 共識 EPS 年化 43.2%、營收年化 44.1%，成長來自營收本身，不是利潤率或回購。跑道估算：FY2027 約 185 億美元，以 25% 年增達到 2,000 億美元市場的 30%，約需 5.3 年，屬中等，且市場規模是管理層數字。成長熄火測試：三年後成長率降到 15%、10%、5%，以 FY2029E 8.4 美元配 22、17、13 倍，股價約 185、143、109 美元，對現價 +8%、−16%、−36%。十項衰退訊號亮兩項，另有六項未亮，提價後銷量與產業倍數走勢兩項資料不足。2027 年其餘業務由總數倒算只增約 11%，AI 倍增的基期還不可靠。","governance":"FCF／淨利 FY2024 為 1.29、FY2025 為 1.21，獲利轉現金沒有問題；2026 年前九月 FCF 37.93 億美元。Q3 股權獎勵 1.381 億美元，占營收 3.8%。稀釋股數由 FY2023 約 12.69 億（淨利÷稀釋 EPS 倒算）到 Q3 12.78 億，年化約 0.26%。現金去向：2026-08-04 CFO 說 Q2 未回購，2026-11-03 CFO 說 15 億美元授權尚餘 8.179 億美元；Q3 存貨增至 32 億美元，資本支出 1.007 億美元，採購承諾 114 億美元。三年現金去向四分比例事實表未涵蓋。Q3 營業現金流約 12 億美元，低於非 GAAP 淨利 15.3 億美元，CFO 歸因於刻意備貨。營業利益率由 FY2022 的 34.86% 升到 FY2025 的 42.82%，沒有營業利益成長落後營收的壓縮現象。","valuation":"FY1 本益比 39.91 倍、FY2 30.3 倍；trailing 45.79 倍落在 4 個年度端點的 76.8 分位，不是五年分位。NTM EPS 約 5.44 美元（FY1 權重 14.6%、FY2 權重 85.4%），NTM 本益比約 31.4 倍，低於前份要求的 35 倍。淨現金 143.59 億美元約每股 11.4 美元，扣現金後 FY2 本益比 28.3 倍。財測推得 FY2027 EPS 約 5.9 美元（185 億×49%，加其他收入約 5.5 億，稅率 21%，12.8 億股），比 FY2 共識 5.64 美元高約 5%，我不把這 5% 當便宜的主要論據。FY1 最後一次快照下修 1.38%，與 Q3 大幅優於財測方向相反，較可能是彙整口徑雜訊；近 3 個月仍上修 4.14%。賣方目標價多在財報前：8 月均值約 238 美元、最高 289 美元，聚合站有 185 美元，最高對最低 289÷164 為 1.76 倍，現價低於均值支持分批方向，但資料偏舊。近端推算：12 個月以 FY2027E 5.9 美元配 33 倍為 195 美元，+14%；24 個月以 FY2028E 7.2 美元配 30 倍為 216 美元，+26.5%。同業本益比事實表未涵蓋。","premortem":"壓力測試五項過三項。FY2027 營收少一成，EPS 約 5.1～5.4 美元，仍高於 FY1 的 4.28 美元，過關。毛利率掉到 60%，EPS 約少 6%，過關。最大客戶採購減半，營收約少 13%，仍賺錢，過關。採購承諾一半賣不掉，損失約 57 億美元，接近 FY2027 推算淨利的四分之三，不過關，但這是極端假設，因承諾含多年期合約。FY2 本益比壓到 20 倍，股價 113 美元，−34%，不過關。動能沒有過熱：RSI 43.36，26 週報酬 20.48%；4 週漂移事實表未涵蓋。歷史最大回撤與空方具體數字事實表未涵蓋，2026-08-04 法說有四題管理層未正面回答，都與 AI 組成或 10% 客戶有關，已併入矛盾裁定。"},"plain":{"six":{"how_it_makes_money":"賺雲端巨頭與大型企業的網路預算，錢卡在交換器系統與 EOS 軟體這一節；上游有 Broadcom 與記憶體，下游有微軟與 Meta，兩頭都不弱。","moat":"護城河方向維持不變：EOS 帶來的執行力仍在擴大，定價力穩定，但資料中心份額已被 Nvidia 超過，不能往上調。","growth":"五年後跑道仍寬：份額不到兩成，園區與 scale-up 是有來源的下一條曲線；成長上限是供給與客戶預算，不是 Arista 的資金。","capital":"現金配置中等偏保守：股本幾乎不膨脹、零負債，現金累積到 144 億美元，但回購動作少，併購與回購的報酬拿不到證據。","valuation":"現價要的是 FY2031 EPS 約 10.4 美元、終端 25 倍，五年年化才有 8.8%。FY2027 財測已走完前面一大段，這個要求我相信；想拿 15% 以上就要靠樂觀情境。","how_wrong":"最可能看錯的不是今年的數字，而是 2028 年：AI 建置進入消化期時，114 億美元採購承諾、兩大客戶占四成營收與 30 倍本益比會同時反向。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Nvidia 在訓練叢集的勝利外推到整個資料中心與園區，股價比 8 月低 19%；但 Q3 營收年增 58.5%，份額下降沒有傷到絕對金額，FY2 共識 5.64 美元也低於財測推得的約 5.9 美元，差約 5%。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":170.8,"week26_return_pct":20.48,"consensus_rev_3m_pct":4.14,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母不是爭點。Q3 GAAP EPS 1.22 美元略高於非 GAAP 1.20 美元，差異含股權獎勵的稅務效果，未放大前瞻分母；財測推得 5.9 美元與共識 5.64 美元差約 5%，方向偏保守。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"IDC 公布 3Q26 乙太網路交換器追蹤（依前兩季時點推估）","impact":"高","watch":"Arista 資料中心份額是否回到 18.7% 以上，與 Nvidia 的差距"},{"date":"2026-12","date_precision":"month","type":"product","event":"Arista 年度最大客戶活動","impact":"低","watch":"園區進展與 AVA 定價模式"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 Q4 財報與 10-K","impact":"高","watch":"FY2026 實際 AI 營收、年底遞延收入、10% 以上客戶家數"},{"date":"2027-11","date_precision":"month","type":"guidance","event":"FY2027 Q3 法說，預期給出 2028 年首版財測","impact":"高","watch":"2028 年營收成長是否低於 15%"}],"_projected_from":"v19"}
```
