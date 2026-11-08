你是 stock-analyst v20 的**散文層（prose）agent**，標的 PLTR（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLTR_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：PLTR　日期：2026-11-08　archetype：None　前份裁決：2026-08-05　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1958B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（378B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（997B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1329B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（865B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（348B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（731B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2093B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4117B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2647B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1958           3529-5042      5 條（2–6 內）  
s3                  8000         378           5335-7622      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3191          8266-11809      5 條（2–6 內）  
s6                 11000         348          7456-10652      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         731           1938-2769      5 條（2–6 內）  
s10                 5000        2093           2035-2907      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2647           2000-2353      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4178B；至少需散文≈40.82KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−72
−72%
−65%
−50%
−50
−49%
−32%
−22.76%
−15%
−1.4%
0
0.3
0.4%
0.6%
0.63
0.8
1%
1
1.24
1.26
1.3
1.4%
1.45
1.5%
1.53
1.66
1.7
1.70
1.8
1.83
2
2%
02
$2.09
2.15
2.2
2.24
2.29
2.3%
2.3
2.35
2.4
2.45
2.49
$2.49
2.5
2.55
2.66
2.7
2.70
2.74
2.75
2.79
2.8
2.9
3
03
3.0
3%
$3.43
3.43
3.55
$3.559
3.8
4%
4
4.35
4.55
5
05
5%
5.3%
5.55
6%
$6.0
6
6.05
6.6
7
07
08
8%
8
8.0%
8.15
8.3%
$8.530
8.534
9%
9.0%
09
9
$9.2
9.3%
9.4%
9.68%
9.83%
10
10%
$10
$10.3
$10.4
10.5
11
11%
11.4
12
13
$13.0
$13.11
$13.4
13.8%
14
15%
$15
16%
16.39
17.6%
17.6
18%
18
19%
20%
20
$20
21
21%
21.52%
22%
24
25%
25
26
27%
28
28%
29%
29.4%
$30
30%
30
30.5%
30.5
31%
32
35%
35
$36
38
40
41%
41.2%
42
42.0%
42.04%
42.5%
44
45%
$45
45
45.64%
46%
46
47%
47
49
49%
50%
52
53%
$54
54.4%
55
55.2%
56
56%
57.4%
58%
58.8
$59
60
60%
62%
62
63%
64
64.4
64.41
65%
67
68
$70
70
71.2%
72%
75.9%
76%
77.8
80
$80
$82
84%
84.74%
85%
86%
88%
90
94
94.34
$95
96%
98.8%
100%
100
104
108%
$109
129%
$130
130%
$136.5
140
140%
$146
148%
150%
154
157%
160.38
$160.38
$162.66
162.66
$165
165%
$184
$189
$192
$199
$209
220
$265
$307
446
472.5
686
$826
$953
$984
2022
2026
2027
2028
20261108
$1,128
$1,216
$1,463
$2,132
$2,313
$2,918
2,328
2,409.5
2,429
2,535
2,564
2,579
2,593
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
{"meta":{"ticker":"PLTR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Palantir Technologies Inc."},"oneliner":"Palantir 靠 Ontology 把 AI 接進企業與軍方流程，Q3 營收年增 96%、淨留存升到 165%，但合約總額只年增 6%；現價為 FY1 本益比 94 倍，基本情境年化約 9%，下一步看 Q4 接單能否回升。","thesis":{"H":[{"id":"H1","text":"Ontology 加 AIP 是企業把模型接進營運流程的必要層，模型越便宜、開放權重越多，這一層越值錢。","2y":"FY2027 美國商業營收 ≥ $6.0B，淨留存全程 ≥ 140%","5y":"FY2031 美國商業營收 ≥ $20B","10y":"前十大商業客戶無一遷出，AIP 仍是企業營運 AI 的預設流程層","threshold":"Q3 實績：美國商業 $984M、年增 148%，淨留存 165%，FY2026 美國商業指引 > $3.559B","source":"公司季度新聞稿與法說（2026-11-02）","drift_rule":"淨留存連 2 季低於 140% 達 5% 以上為削弱，連 3 季低於門檻 10% 以上為反轉"},{"id":"H2","text":"需求大於交付能力，合約變短只是過渡，營收可在高基期維持高速。","2y":"FY2027 營收 ≥ $13.0B，2027 年第一季起美國商業 TCV 年增回到 ≥ 30%","5y":"FY2031 營收 ≥ $30B，調整後營益率 ≥ 58%","10y":"國際段占比回升到 25% 以上，或出現年營收超過 $10B 的第二條曲線","threshold":"FY2026 指引 $8.530–8.534B、FY2027 共識 $13.11B；總剩餘合約對年化營收 1.45 年，低於 1.3 年視為惡化","source":"公司指引與新聞稿、yfinance 共識營收（2026-11-08）","drift_rule":"FY2027 營收進度低於門檻 5% 連 2 季為削弱，低於 10% 連 3 季為反轉"},{"id":"H3","text":"EPS 複利快過倍數壓縮，五年後仍有正報酬。","2y":"一年後前瞻本益比 ≥ 45 倍，FY2028 共識不低於 $3.43","5y":"FY2031 EPS ≥ $6.0，本益比 ≥ 35 倍","10y":"十年累積報酬 ≥ 2.5 倍","threshold":"FY1 本益比 94.34 倍、FY2 本益比 64.4 倍；共識 EPS 1.70／2.49／3.43","source":"Koyfin 共識快照（2026-11-07）","drift_rule":"FY2028 共識連 4 季低於 3.43 達 5% 以上為削弱，連 6 季低於 10% 以上為反轉"}],"R":[{"id":"R1","text":"美國商業由加速轉為高速但減速；Q3 接單已先放緩，若合約變短的解釋不成立，營收會在 2–4 季後跟上。","h_ref":"H2","clock":"⚡","threshold":"美國商業季增連 2 季 < +15%，或 TCV 對營收比連 2 季 < 1.8 倍（Q3 為 1.26 倍，已算第一季）","evidence_refs":["end_markets#2"]},{"id":"R2","text":"歐洲主權 AI 由個案變成系統性排除，壓低國際段；Q3 國際商業只季增 1%，國際政府季增 6%。","h_ref":"H2","clock":"🔥","threshold":"國際段任一季季增轉負，或英國動用解約條款","evidence_refs":["geo_supply_chain#2"]},{"id":"R3","text":"前沿實驗室複製資料整合與前線部署，資本量級遠大於 Palantir；Q3 法說引述約半數 Anthropic 客戶直接與其合作。","h_ref":"H1","clock":"🐢","threshold":"任一前十大商業客戶遷出，或淨留存因價格競爭跌破 130%","evidence_refs":["substitute_technology#1","competitive_share_entrants#2","end_markets#3"]},{"id":"R4","text":"美國國防生態被分食：Alphabet 簽下機密協議，Anduril 取得陸軍 NGC2 資料層主導權（前份紀錄）。","h_ref":"H2","clock":"🔥","threshold":"美國政府營收連 2 季季增 < 5%","evidence_refs":["competitive_share_entrants#3"]}],"single_thing":{"description":"到 2027 年第一季財報為止，美國商業 TCV 連兩季年增都低於 20%，且淨留存跌破 150%。","why_fatal":"現價為 FY2 本益比 64 倍，FY2027 共識營收要再長 53%，主要靠美國商業。若接單放緩其實是需求問題，EPS 下修和倍數壓縮會同時發生：FY2028 EPS 由 3.43 降到 2.70、倍數落到 35 倍，股價約 $95，跌 41%。","if_happens":"減碼一半，停止加碼，下修基本情境後重跑報告；只有 TCV 弱而淨留存守住 150% 時，僅停止加碼。","how_monitor":"每季新聞稿與法說的美國商業 TCV 年增率、淨留存、剩餘合約季增率。","probability":"25–30%（未來 12–24 個月）"}},"appendix_a":{"growth_durability":8,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":64.41,"peg_fy2":1.53,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":0.63,"FY2026E":1.7,"FY2027E":2.49,"FY2028E":3.43},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS（yfinance 年度財報）；FY2026E–FY2028E 為 Koyfin 共識（2026-11-07），事實表未註明 GAAP 或調整後口徑。基期與共識可能不同口徑，三年 CAGR 75.9% 偏高，FY2026E→FY2028E 兩年 CAGR 42.0% 較可靠。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLTR_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"TTM 毛利率 85%、營業利益率 46%、FCF 利潤率 56%，營收年增 96%，淨現金 $10.3B；成長速度遠高於一般複利股，歸類信心因此只到中等。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久，但速度帶週期性：管理層稱需求超過交付能力（2026-11-02 法說），同季淨留存升到 165%；合約總額年增僅 6% 是反向訊號。IDC 與 Creative Strategies 的算力短缺看法屬產業層資訊，不是軟體專屬證據。","bargaining":{"up":"模型可多來源，含開放權重，對單一模型商議價力高；部分客戶跑在 AWS、Microsoft 基礎設施上，公司無法控制對方設施。","down":"客戶分散，前三大占 16%，前三大平均合作 10 年；Customer I 占應收帳款 27%（2026-09-30），名稱未揭露。","geo":"美國占 84% 營收；歐洲主權疑慮壓抑國際段，CEO 在 2026-08-03 法說承認歐洲業務成長很差。"},"profit_pool_dir":"管理層主張價值從模型層移向應用與流程層，事實表沒有利潤池數字可驗證。","tam_table":[{"item":"美國國防部 TTM 營收占五角大廈預算","value":"低於 25 個基點（2026-08-03 法說 CTO）"},{"item":"美國商業客戶數","value":"686 家，年增 29%、季增 5%（Q3 FY2026）"},{"item":"TAM、SAM、滲透率、段 CAGR、利潤池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"Ontology 加 AIP 把客戶的資料、邏輯與動作綁在同一層，模型可替換而流程不用換，營運資料持續累積成後訓練素材，轉換成本隨使用加深。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：淨留存 157%→165%，美國商業季增 29%，Rule of 40 連 13 季改善。定價面穩定：TTM 毛利率 84.74%，但沒有單獨調價資料，Q3 調整後毛利率 85% 低於 Q2 的 86%。合併判持平。可能看錯之處：若毛留存與客單價資料顯示定價在升，方向應上調。","peer_na_reason":"同業 ROIC 事實表未涵蓋，以利潤率差距代替。","threats":[{"level":"🔴","text":"前沿模型實驗室把資料整合與前線部署產品化，直接爭企業流程層，屬生態攻擊。","p":"35%","evidence_refs":["substitute_technology#1","substitute_technology#0","competitive_share_entrants#2","end_markets#3"]},{"level":"🟡","text":"大型對手以搭售或低毛利競爭，Alphabet 進入美國國防機密領域。","p":"30%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3"]},{"level":"🟡","text":"歐洲主權替代，法國與西班牙已有轉向或排除的報導，來源為二手媒體。","p":"50%","evidence_refs":["geo_supply_chain#2"]},{"level":"🟡","text":"部分客戶跑在 AWS、Microsoft 基礎設施上，雲端商既是通路也可能成為斷點。","p":"15%","evidence_refs":["geo_supply_chain#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"政府端屬需要，Maven 使用者超過 10 萬；商業端很多是公司過去沒做的新工作，延後的代價較低。代理讀數：淨留存 165%，美國商業 TCV 年增只有 11%。"},{"item":"決策層級","level":"🟢","text":"替代單位是整條流程，不是單一模型。代理讀數：前三大客戶平均合作 10 年，淨留存 165%。合約變短會降低契約上的轉換障礙，毛留存率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"公司毛利率 85%，後訓練模型本身被管理層稱為商品，價值留在流程與資料管線。風險在模型商也要這一段，開放權重供應若收斂到少數夥伴也會削弱議價力。"},{"item":"社會容忍度","level":"🔴","text":"政治上限已經低於經濟上限：法國與西班牙有轉向或排除報導，英國監理機關的試用引發資料疑慮。國際政府 Q3 仍季增 6%，數字尚未受損，已列入反證。"}],"roiic":"公式值事實表未涵蓋；代理值為每多花 1 美元調整後費用多賺約 2.7 美元調整後營業利益（Q3 年比）","reinvest_rate":"事實表未涵蓋（缺 D&A、營運資金、遞延收入明細）","endo_ceiling":null,"formula_note":"內生成長公式要用投入資本與營運資金變動，事實表沒有這些明細；輕資產公司的再投資多走損益表，即使算出比率也缺乏經濟意義，因此不自行外推。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","PLTR":84.74,"SNOW":67.03,"NOW":73.08,"CRM":77.28,"DDOG":79.58,"unit":"%"},{"metric":"營業利益率","PLTR":45.64,"SNOW":-22.76,"NOW":9.68,"CRM":21.52,"DDOG":2.3,"unit":"%"},{"metric":"FCF 利潤率","PLTR":55.62,"SNOW":21.96,"NOW":30.78,"CRM":34.49,"DDOG":25.93,"unit":"%"},{"metric":"研發密度","PLTR":9.83,"SNOW":38.78,"NOW":22.47,"CRM":14.49,"DDOG":42.61,"unit":"%"}],"competitors":[{"name":"SNOW","gm":67.03,"om":-22.76,"fcf_margin":21.96,"rd_intensity":38.78,"strategy_note":"資料平台層對手，營業利益率仍為負，打價格戰的本錢有限。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"NOW","gm":73.08,"om":9.68,"fcf_margin":30.78,"rd_intensity":22.47,"strategy_note":"同屬企業流程軟體，毛利率與 FCF 都低於 Palantir，是在既有裝機上爭 AI 預算的對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CRM","gm":77.28,"om":21.52,"fcf_margin":34.49,"rd_intensity":14.49,"strategy_note":"利潤結構成熟，客戶基礎大，威脅在搭售而不是單點產品。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"DDOG","gm":79.58,"om":2.3,"fcf_margin":25.93,"rd_intensity":42.61,"strategy_note":"監控工具層，與 Palantir 直接重疊小，主要作為利潤率比較基準。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量與既有客戶擴張為主，新客為輔，價格無獨立證據，併購與回購貢獻為零。","runway_years":"定性約 10 年（事實表未涵蓋滲透率，只有國防預算占比一項代理）","runway_post_y5":"🟢","endo_ceiling_basis":"事實表沒有投入資本與營運資金明細，天花板未算。成長資金來自內部現金，Q3 調整後 FCF $1,216M，淨現金 $10.3B；共識 CAGR 是否超過天花板無法判定。","segments":[{"item":"美國商業","value":"$984M，年增 148%，季增 29%"},{"item":"美國政府","value":"$953M，年增 96%，季增 18%"},{"item":"國際政府","value":"$192M，年增 31%，季增 6%"},{"item":"國際商業","value":"$184M，年增 21%，季增 1%"}],"decay_signals":["EPS CAGR 高於營收 CAGR 超過 5 個百分點：FY2025A→FY2027E EPS 98.8% 對營收 71.2%，基期口徑可能不同；FY2027E 單年已反轉為 EPS 年增 46%、營收年增 53%。"]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，資本回饋目前不影響論點；回購明細事實表未涵蓋。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月未見併購，8-K 也沒有相關重大事項。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購金額與均價；Q3 現金增加約等於 FCF，當季回購不明顯。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數 FY2023→FY2025 年化增加約 5.3%，超過每年 1.5%；最新一季大致持平，待 FY2026 年報確認。","grade":"不過"}]},"valuation":{"basis":"FY1 共識 EPS 的前瞻本益比，對照 FY2 本益比與前瞻 EV/S。","tier":"高成長軟體頂層","peers":{"expanded":false,"reason":"事實表只收同業利潤率，沒有同業估值倍數，無法做跨公司倍數比較；終端倍數改以本身 FY2 本益比與 PEG 對照。"},"fwd_pe":94.34,"peg":2.24,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 94.34 倍 ÷ FY2026E→FY2028E CAGR 42.04%＝2.24，偏貴；FY2 本益比 64.41 倍 ÷ 同一 CAGR＝1.53，落在合理區間。以 FY2025 GAAP 0.63 為基期算出 1.24，基期口徑不一致，不採用。基本情境年化約 9%，屬中段。合併判為中性偏貴，FY2 共識上修而價格未動，所以沒有再往昂貴移動。","upside_short_pct":17.6,"upside_mid_pct":30.5},"trap_analysis":{"verdict":"🟡","label":"經營面沒有陷阱跡象，風險在高倍數加上接單放緩"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 總 TCV $2,918M 只年增 6%，Q2 年增 49%；美國商業 TCV $1,463M，年增 11%，低於 Q2 的 $2,132M；總剩餘合約季增 2%、RPO 季持平，營收卻季增 20%。OpenAI 與 Anthropic 正往資料整合與前線部署走。2026-08-03 法說被問模型下架能否更換時，CEO 未給客戶數或量化資訊。","assumption":"假設 CFO 所說八位數合約年限變短屬過渡，短約到期後會以更大金額續約。","consequence":"假設若錯，營收在 2–4 季後減速，FY2028 EPS 由 3.43 落到約 2.70，倍數落到 35 倍，股價約 $95。五年後虧 50% 最可能就是這條路：需求被實驗室與開放權重分走，Palantir 從必要層退成選項之一。","ruling":"部分採納，與唯一致命點重疊，不另開事件。淨留存 165% 與客戶年增 29% 反駁需求見頂；但 CFO 只用一句話解釋，法說三個提問也沒人追問，歸因列為未證。","watch":"Q4 與 2027 Q1 的美國商業 TCV 年增率、淨留存、剩餘合約季增率。","evidence_refs":["end_markets#2","substitute_technology#1","competitive_share_entrants#2","end_markets#3"],"fact_refs":["f_kpi6_total_contract_value_tcv","f_kpi7_u_s_commercial_remaining"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 調整後費用季增 20%，與營收季增相同；CEO 說要重新調配公司資源才服務得了需求。稀釋股數 FY2023 至 FY2025 年化增加約 5.3%，現金 $10.4B 持續累積。","assumption":"假設調整後營益率維持 60% 左右，稀釋放緩。","consequence":"若短約需要更多前線工程師才能交付，利潤率會回落；基本情境 FY2031 調整後營益率每低 5 個百分點，EPS 約少 8%。","ruling":"採納為次要風險，基本情境已用 60%，低於目前的 62%，不再單獨調整機率。","watch":"調整後費用增速與營收增速之差、SBC 占營收、稀釋股數。","evidence_refs":[],"fact_refs":["f_kpi1_non_gaap_adjusted_operat","f_kpi4_sbc_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"英國監理機關試用 Palantir 引發資料疑慮，各國正考慮進一步規範 AI；法國與西班牙已有轉向或排除報導；CEO 在 Q3 法說談到歐洲時說應該避免多談。","assumption":"假設政治上限只影響國際段，目前占營收 16%。","consequence":"若美國政治風向或輿論轉變，占營收 41% 的美國政府業務也會受限，公司實際可賺的上限由政治決定。","ruling":"採納，這是四項持續期檢查中唯一判紅的項目；目前數字未受影響，國際政府 Q3 仍季增 6%。","watch":"國際段季增率、德國決標結果、英國合約解約條款。","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#3","geo_supply_chain#2"],"fact_refs":["f_kpi0_revenue_gaap"]},{"view":"價格已反映太多","evidence":"FY1 本益比 94.34 倍、前瞻 EV/S 44 倍。Q4 指引高於共識約 8%，盤後仍跌約 3%；賣方目標價 $70 到 $265，高低相差 3.8 倍。","assumption":"假設 FY2031 仍值 38 倍。","consequence":"終端倍數改 25 倍，基本情境只剩 $165，五年年化約 0.6%。","ruling":"採納。賣方分歧過大，下調對自身報酬預估的信心，第一筆只建部分倉位。","watch":"FY2 本益比與 FY2 共識修正方向。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_ev_s_fwd","f_consensus_eps_fy2"]}],"max_dd":{"lo":-72,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 162.66 → 本次 160.38（-1.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=162.66","side_b":"本次 price_at_dd=160.38","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 162.66 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 162.66 美元：Bull 價 446、Bear 價 60，五年期望值 +54.4%，基準年化 9.3%，不對稱比 2.7","side_b":"本次情境、股價仍用 162.66 美元：Bull 價 472.5、Bear 價 58.8，五年期望值 +55.2%，基準年化 9.0%，不對稱比 2.66","ruling":"先換情境、股價不動：五年期望值多 0.8 個百分點，基準年化少 0.3 個百分點。不對稱比由 2.7 變為 2.66。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 162.66 美元：五年期望值 +55.2%，基準年化 9.0%，不對稱比 2.66","side_b":"本次情境、股價 160.38 美元：五年期望值 +57.4%，基準年化 9.4%，不對稱比 2.74","ruling":"再換股價、情境不動：起點價下跌 1.4%，五年期望值多 2.2 個百分點，基準年化多 0.3 個百分點，不對稱比由 2.66 升到 2.74。合計五年期望值比前份多 3.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"接單放緩與留存加速","cause":"新證據","prior_field":["signal"],"side_a":"Q3 總 TCV 年增 6%，TCV 對營收比 1.26 倍，Q2 為 2.79 倍；美國商業剩餘合約季增 4%。","side_b":"Q3 淨留存由 157% 升到 165%，營收季增 20%，美國商業季增 29%，高於前份設定的 18%。","ruling":"可調和，屬程度差異：短約會讓 TCV 低估年化合約金額。維持原有評等與進場結論。這個利空不到一季，FY2 共識在兩份快照間只動 0.4%，尚未反映，因此第一筆只建部分倉位，加碼凍結到 Q4 財報。","evidence_level":"公司揭露，單季，歸因未證","settle_metric":"美國商業 TCV 年增率與淨留存，看 2027-02 與 2027-05 兩次財報","if_then":["若 Q4 美國商業 TCV 年增 ≥30% 且淨留存不降，加碼至目標倉位","若連兩季美國商業 TCV 年增 <20% 且淨留存 <150%，減碼一半","若股價先漲過約 $199（FY2 本益比 80 倍）而接單未確認，不追","若股價跌到 $130–140 而淨留存與美國商業季增都未惡化，分批反買"],"evidence_refs":["end_markets#2"]},{"axis":"估值結論","cause":"新證據","prior_field":["val"],"side_a":"前份：現價 $162.66，FY2027 共識 $2.09，FY2 本益比 77.8 倍，中性偏貴。","side_b":"本次：現價 $160.38，FY2027 共識 $2.49，FY2 本益比 64.4 倍，仍中性偏貴。","ruling":"結論不變。倍數下降來自共識上修，不是股價下跌；FY1 本益比 94 倍與前瞻 PEG 2.24 仍不支持判成便宜。兩次共識來源不同，上修幅度為近似值。","evidence_level":"共識快照，跨來源","settle_metric":"FY2 共識修正方向","if_then":["若 FY2 共識連兩季下修且 FY2 本益比仍高於 60 倍，停止加碼"],"evidence_refs":[]},{"axis":"陷阱與護城河方向","cause":"新證據","prior_field":["trap","moat_trend"],"side_a":"前份：陷阱風險中性，護城河方向持平。","side_b":"本次：淨留存上升、利潤率差距擴大，但搭售與 Alphabet 進入國防的競爭證據增加。","ruling":"兩項結論不變。正面證據主要反映市場擴大，CEO 自己也這樣解釋；負面證據尚未進入數字。","evidence_level":"公司揭露加二手報導","settle_metric":"淨留存、毛利率、美國政府季增率","if_then":["若毛利率連兩季年比下滑且淨留存同時下降，護城河方向下調並減碼一半"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3"]},{"axis":"成長空間、生意類型與景氣位置","cause":"新證據","prior_field":["runway_post_y5","archetype","cycle_position"],"side_a":"前份：後段跑道寬，歸類品質複利成長，不適用景氣循環位置。","side_b":"本次：美國商業首度超過美國政府，FY2026 指引再上調，歸類與跑道都不變。","ruling":"三項不變。滲透率仍無數字，因此跑道結論的信心只到中等。","evidence_level":"公司揭露，缺滲透率","settle_metric":"美國國防預算占比與國際段占比","if_then":["若 FY2027 營收成長低於 30% 且無第二曲線，跑道下調並停止加碼"],"evidence_refs":[]},{"axis":"情境機率與最大回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 27%、Bear 28%，最大回撤 −65% 單點。","side_b":"本次 Bull 25%、Base 47%、Bear 28%，最大回撤區間 −72% 至 −50%。","ruling":"Bull 的 FY2031 EPS 門檻提高到 10.5，機率下調 2 點；留存走強與接單放緩互相抵銷，Bear 維持 28%。最大回撤改填區間，由情境倍數推算。","evidence_level":"判斷假設","settle_metric":"FY2027 營收與 EPS 對 Base 路徑的偏離","if_then":["若 FY2027 EPS 低於 2.15，機率移向 Bear 並減碼一半"],"evidence_refs":[]},{"axis":"加碼條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"回檔 $130-140（NTM ~68x、布林中軌）或 Q3 US 商業 QoQ ≥ +18% 且 NDR 未下滑","side_b":"回檔 $130–140（FY2 本益比約 52–56x、貼近 104 週線）或 Q4 美國商業 TCV 年增 ≥ 30% 且淨留存未下滑","ruling":"舊加碼條件的基本面分支已在 Q3 達成，美國商業季增 29%、淨留存升到 165%，因此換成 Q4 接單條件。價位不變，對應 FY2 本益比由 62–67 倍降為 52–56 倍。","evidence_level":"公司揭露","settle_metric":"Q4 美國商業 TCV 年增率","if_then":["若 Q4 達成條件，加碼至目標倉位"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點變動","cause":"新證據","prior_field":["single_thing"],"side_a":"前份摘要的唯一致命點欄位為空；前份第三項風險門檻寫明：任一 top-10 商業客戶遷出。","side_b":"到 2027 年第一季財報為止，美國商業 TCV 連兩季年增都低於 20%，且淨留存跌破 150%。","ruling":"改用敏感度最大的項目。客戶遷出較戲劇化，但只影響單一客戶；接單持續放緩會同時打到 FY2028 EPS 與倍數。前十大客戶遷出保留在長期風險與清倉條件。","evidence_level":"公司揭露","settle_metric":"美國商業 TCV 年增率與淨留存","if_then":["若事件發生，減碼一半並下修基本情境"],"evidence_refs":["end_markets#2"]},{"axis":"短期風險門檻與減碼條件","cause":"新證據","prior_field":["R1.threshold"],"side_a":"QoQ 連 2 季 < +15%，或 TCV/營收比 < 1.8x","side_b":"美國商業季增連 2 季 < +15%，或 TCV 對營收比連 2 季 < 1.8 倍","ruling":"舊門檻在 Q3 已觸發一次，TCV 對營收比 1.26 倍。1.8 倍不動，TCV 這條改成連兩季才減碼，因單季波動大（Q2 2.79 倍、Q3 1.26 倍），短期風險的規則也是連兩季才動作。Q3 算第一季。","evidence_level":"公司揭露","settle_metric":"Q4 的 TCV 對營收比","if_then":["若 Q4 再低於 1.8 倍，減碼三分之一"],"evidence_refs":["end_markets#2"]},{"axis":"清倉與減碼指標新增","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未列清倉與減碼指標，欄位為空。","side_b":"本次新增：TCV 年增連兩季 <20% 且淨留存 <150% 則減碼一半；前十大商業客戶遷出且淨留存 <130% 則清倉。","ruling":"把前份散在風險項的條件集中成可執行指標，並補上動作。","evidence_level":"方法調整","settle_metric":"每季公司揭露","if_then":["若清倉條件成立，清倉並重跑報告"],"evidence_refs":[]},{"axis":"管理層成長承諾對帳","cause":null,"prior_field":null,"side_a":"2026-08-03 法說 CEO：要讓整體業務在未來 18 個月追上美國商業的成長率。","side_b":"Q3 整體年增 96%，美國商業 148%，相差 52 個百分點；Q2 約相差 56 個百分點。","ruling":"尚未到期，差距只小幅收斂，不計入基本情境。","evidence_level":"法說原話摘錄","settle_metric":"2028-02 前整體與美國商業年增差距","if_then":["若 2028 年初差距仍大於 30 個百分點，CEO 的成長預告不再用於上修情境，並停止加碼"],"evidence_refs":[]},{"axis":"大單筆數揭露","cause":null,"prior_field":null,"side_a":"2026-08-03 法說 CRO 報百萬美元以上大單 220 筆，創新高。","side_b":"2026-11-02 法說沒有報這個數字，只說簽了多筆年限較短的八位數合約。新聞稿全文不在本包，無法確認是否另有揭露。","ruling":"未證，暫不作為負面證據，列入下季追蹤。","evidence_level":"逐字稿比對，缺新聞稿全文","settle_metric":"Q4 是否揭露大單筆數","if_then":["若 Q4 仍未揭露且美國商業 TCV 年增 <30%，停止加碼"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"FY1 本益比 94 倍、接單放緩、指引超預期仍下跌，可能是高基期減速前的最後一段。","side_b":"FY2 共識上修、淨留存上升、淨現金 $10.3B，週線仍為多頭排列。","ruling":"賣出論點要成立，前提是接單放緩來自需求，目前證據不足以判定，因此分批進場而非放棄。","evidence_level":"公司揭露加判斷","settle_metric":"Q4 與 2027 Q1 接單","if_then":["若唯一致命點成立，減碼一半"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"淨留存連兩季低於 140%，第一項假設削弱。","type":"假設驗證","maps_to":"H1","metric":"淨金額留存率","threshold":"連兩季 <140%","action":"停止加碼","source_freq":"公司季度財報","date":"2027-02 起每季"},{"n":2,"text":"美國商業接單連兩季沒有回升，且淨留存同步走弱。","type":"Single Thing","maps_to":"Single Thing","metric":"美國商業 TCV 年增率與淨留存","threshold":"連兩季 TCV 年增 <20% 且淨留存 <150%","action":"減碼一半並下修基本情境","source_freq":"公司季度財報","date":"2027-05","evidence_refs":["end_markets#2"]},{"n":3,"text":"股價回到 $130–140 而基本面無損。","type":"估值rearm","maps_to":"H3","metric":"股價與 FY2 共識","threshold":"$130–140 且 FY2 共識未下修","action":"分批反買","source_freq":"每日收盤與共識快照","date":null},{"n":4,"text":"Q4 接單回升，合約變短的解釋得到支持。","type":"加碼","maps_to":"H2","metric":"美國商業 TCV 年增率與淨留存","threshold":"TCV 年增 ≥30% 且淨留存未下滑","action":"加碼至目標倉位","source_freq":"公司季度財報","date":"2027-02"},{"n":5,"text":"短期風險連兩季成立。","type":"減碼","maps_to":"R1","metric":"美國商業季增率、TCV 對營收比","threshold":"季增連兩季 <15%，或比值連兩季 <1.8 倍","action":"減碼三分之一","source_freq":"公司季度財報","date":"2027-02","evidence_refs":["end_markets#2"]},{"n":6,"text":"前沿實驗室實際搶走大客戶，且留存因此明顯下滑。","type":"清倉","maps_to":"R3","metric":"前十大商業客戶遷出與淨留存","threshold":"任一客戶遷出且淨留存 <130%","action":"清倉並重跑報告","source_freq":"法說與公開報導","date":null,"evidence_refs":["substitute_technology#1"]},{"n":7,"text":"歐洲排除由個案變成數字。","type":"風險","maps_to":"R2","metric":"國際段季增率、英國解約條款","threshold":"任一季季增轉負，或英國動用解約條款","action":"停止加碼","source_freq":"公司季度財報與新聞","date":"2027-02 起每季","evidence_refs":["geo_supply_chain#2"]},{"n":8,"text":"美國國防業務被分食。","type":"風險","maps_to":"R4","metric":"美國政府營收季增率","threshold":"連兩季 <5%","action":"停止加碼","source_freq":"公司季度財報","date":"2027-02 起每季","evidence_refs":["competitive_share_entrants#3"]},{"n":9,"text":"2022 年證券集體訴訟仍在第十巡迴法院上訴，若撤銷駁回會重回一審；求償金額事實表未涵蓋，屬民事集體案件。","type":"風險","maps_to":null,"metric":"上訴裁決與集體認證","threshold":"撤銷駁回並發回","action":"停止加碼；進入集體認證且和解不利時減碼一半","source_freq":"法院文件與季報","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":10,"text":"Q4 FY2026 財報後重跑本報告，確認接單與指引。","type":"複審日期","maps_to":"H2","metric":"報告複審","threshold":"財報公布後一週內","action":"重跑報告","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"美國商業 TCV 年增率與淨留存","bear_threshold":"TCV 年增連兩季 <20% 且淨留存 <150%","window":"至 2027 年第一季財報","source":"公司季度新聞稿與法說","last_status":"warning"},{"metric":"TCV 對當季營收比","bear_threshold":"連兩季 <1.8 倍","window":"Q3 FY2026 起連續兩季","source":"公司季度新聞稿","last_status":"warning"},{"metric":"美國商業營收季增率","bear_threshold":"連兩季 <15%","window":"任兩季連續","source":"公司季度新聞稿","last_status":"ok"},{"metric":"前十大商業客戶遷出與淨留存","bear_threshold":"任一客戶遷出且淨留存 <130%","window":"未來 24 個月","source":"法說與公開報導","last_status":"ok"}],"evidence_dismissed":[{"ref":"reg_tariff_export#1","reason":"這是 10-K 的總體風險條列，關稅只是括號內一項，沒有金額、客戶或產品對應，無法轉成指標。"},{"ref":"geo_supply_chain#1","reason":"來自 FY2024 10-K 的通用風險語句，未指出任何實際事件或金額，也未涉及具體供應鏈節點。"},{"ref":"geo_supply_chain#3","reason":"唯一來源是第三方網站轉述，未說明 Palantir 在當地有何設施或營收，無法評估暴險。"},{"ref":"customer_second_source#1","reason":"來源是掛在大學網域下的聚合頁面，轉述 BBC 卻沒有原文，系統範圍與金額都無法核實。"},{"ref":"major_events#3","reason":"內容是律師事務所招攬投資人的公告，不是監管或法院行動，同一筆資料也說明未見 SEC 調查或重編財報。"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把單季 TCV 年增 6% 讀成需求見頂，FY2 共識約上修 19% 而股價沒動；我認為 TCV 被短約壓低，淨留存升到 165% 是反證，這個判斷下兩季可以檢驗。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=16.39, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"回檔 $130–140（FY2 本益比約 52–56x、貼近 104 週線）或 Q4 美國商業 TCV 年增 ≥ 30% 且淨留存未下滑","exec_line":"現價先建第一批，Q4 財報確認接單後才補；股價跌到 $130–140 而淨留存與美國商業季增都未惡化時分批反買；股價漲過約 $199（FY2 本益比 80 倍）而接單未確認則不追。深回撤區間可到 −72%，論點未破不因波動砍倉。"},"reasoning":{"industry":"Q3 FY2026 營收 $2,313M，年增 96%、季增 20%。分部取自 2026-11-02 法說 CFO：美國商業 $984M（占 42.5%，年增 148%）、美國政府 $953M（41.2%，年增 96%）、國際政府 $192M（8.3%，年增 31%）、國際商業 $184M（8.0%，年增 21%）。調整後毛利率 85%，GAAP 營業利益率 47%，調整後營業利益率 62%。前三大客戶占 FY2025 營收 16%，無單一客戶超過 10%，客戶端沒有單點依賴；單點依賴在地區，美國占 84%。產業判為擴張期：客戶從試點到大單的時間明顯縮短，管理層稱需求超過交付能力，也還沒有供給過剩或價格戰的已實現數字；合約變短是第一個要盯的過熱跡象。可能看錯之處：需求描述多來自管理層自述，價量拆分與毛留存率事實表未涵蓋。","moat":"機制是 Ontology：客戶把營運資料、邏輯與動作放進同一層之後，模型可以換，流程不必換，營運資料還能持續餵給後訓練。可證方向：淨留存由 Q2 的 157% 升到 165%，前 20 大客戶 TTM 平均營收年增 76%。TTM 營業利益率 45.64%，高於 CRM 21.52%、NOW 9.68%、DDOG 2.3%、SNOW −22.76%，毛利率也是五家最高，研發密度 9.83% 是五家最低。同業 ROIC 事實表未涵蓋，以利潤率差距代替，差距有一部分來自成長階段，不能全算成護城河。不判加寬有三個理由：CEO 在 Q3 法說自己偏向「市場在周圍爆發」這個解釋；價格與份額資料事實表沒有；前沿實驗室與 Alphabet 的攻擊正在增加，Anduril 也在 2026 年 6 月取得陸軍 NGC2 資料層主導權（前份紀錄）。當期 ROIC：投入資本事實表未涵蓋，輕資產加淨現金 $10.3B，歸為高利益率、高周轉，這項分類未經數字驗證。新增資本報酬用代理值看：Q3 調整後費用年增約 $307M，調整後營業利益年增約 $826M，每多花 1 美元多賺約 2.7 美元；這是高成長期的單點，不能外推。","growth":"成長幾乎全來自量與客戶擴張：淨留存 165%、美國商業客戶年增 29%、每客戶營收年增 88%；價格沒有獨立資料，沒有併購，也沒有淨回購貢獻。Koyfin 共識 EPS 為 FY2026E 1.70、FY2027E 2.49、FY2028E 3.43，兩年 CAGR 42.0%；以 FY2025 GAAP 0.63 為基期的三年 CAGR 為 75.9%，基期與共識可能不同口徑。FY2027 共識營收 $13.11B，年增 53%。內生上界算不出來，缺口無法歸因，結論依賴倍數維持，信心上限為中；資本不是限制，因為成長靠內部現金支應。能見度在下降：總剩餘合約 $13.4B 對年化當季營收為 1.45 年，一年前約 1.83 年；美國商業由約 2.29 年降到 1.66 年，由揭露的年增率反推。衰退信號亮一項，SBC 占營收 13.8% 高於 5%，但事實表只有單季，無法判斷是否逐年上升。","governance":"FCF 對淨利：FY2025 為 129%，Q3 為 108%（調整後 FCF $1,216M ÷ GAAP 淨利 $1,128M）。SBC 占 Q3 營收 13.8%、占 GAAP 營業利益 29.4%。現金與短期美債由 Q2 的 $9.2B 增到 $10.4B，增幅約等於當季 FCF，顯示 Q3 沒有明顯回購或併購。現金去向四分事實表未涵蓋。股數由淨利除以稀釋 EPS 反推：FY2023 約 2,328M、FY2024 約 2,429M、FY2025 約 2,579M，兩年年化增加約 5.3%；Q3 FY2026 約 2,564M（EPS 四捨五入，範圍 2,535M–2,593M），大致持平。目前流通股 2,409.5M，與稀釋股數仍差約 154M 股，屬尚未轉換的稀釋來源。","valuation":"現價 $160.38，FY1 本益比 94.34 倍，FY2 本益比 64.4 倍，前瞻 EV/S 44 倍。FY2027 共識由前份紀錄的 $2.09 升到 $2.49，約上修 19%（前者為 stockanalysis／MarketBeat，後者為 Koyfin，不同源，僅供近似），股價由 $162.66 到 $160.38，FY2 本益比由 77.8 倍降到 64.4 倍。Q4 指引高於共識約 8%，盤後仍跌約 3%，代表好消息已被預期。賣方目標價 $70–$265，高低相差 3.8 倍，參考價值低。短期目標：一年後 FY2028 共識 3.43 × 55 倍＝$189，上檔 17.6%。中期目標：基本情境 FY2029 EPS 4.55 × 46 倍＝$209，上檔 30.5%。真五年分位與同業倍數事實表未涵蓋，年度端點分位樣本太少，不拿來判斷。","premortem":"經營面衰退信號只亮一項，主要風險在高倍數加上接單放緩。成長熄火測試以基本情境 FY2029 EPS 4.55 計：成長降到 15% 給 30 倍為 $136.5（−15%）；降到 10% 給 24 倍為 $109（−32%）；降到 5% 給 18 倍為 $82（−49%）。跌幅 30% 以內算過，三項過一項。產業態勢：競爭在惡化（實驗室與 Alphabet 進場），結構也在轉好（企業 AI 需求擴大、開放權重降低模型依賴），歐洲主權是另一個結構變數，裁決為雙向拉鋸。歷史最大回撤與空方最強數字事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺大型企業與美國政府把 AI 接進實際營運流程的錢，錢卡在 Ontology 加 AIP 這一層；美國占營收 84%。","moat":"護城河方向持平：執行力仍在擴大，定價力沒有獨立證據，競爭者的攻擊變多，還不足以判為加寬。","growth":"五年後仍有寬跑道：國防預算占比低於 25 個基點，主權 AI 是已開始收錢的新曲線；滲透率沒有數字，這個判斷的信心只到中等。","capital":"資本配置還沒有被考驗：現金持續累積，沒有併購，回購資料缺，歷史股數稀釋偏高。","valuation":"現價要求 FY2031 EPS 約 6.6 美元、屆時仍值 38 倍，基本情境才有約 9% 年化報酬；我相信 EPS 路徑，對倍數只有中等信心。","how_wrong":"最可能看錯在把合約變短當成過渡；若其實是需求放緩，EPS 下修和倍數壓縮會一起來。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把單季 TCV 年增 6% 讀成需求見頂，FY2 共識約上修 19% 而股價沒動；我認為 TCV 被短約壓低，淨留存升到 165% 是反證，這個判斷下兩季可以檢驗。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":160.38,"week26_return_pct":16.39,"consensus_rev_3m_pct":6.25,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"2026-08-03 法說 CFO 拆出 SpaceX 持股未實現利益對 GAAP 與調整後 EPS 的貢獻，金額事實表未涵蓋；本次以前瞻 EPS 為主，不拿 TTM 本益比論便宜。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 FY2027 全年指引","impact":"高","watch":"美國商業 TCV 年增率、淨留存、FY2027 營收指引對共識 $13.11B；公司尚未公告日期，依前幾季財報時點估計。"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報","impact":"高","watch":"唯一致命點的第二次檢驗；公司尚未公告日期。"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"德國聯邦國防軍替代方案決標（前份紀錄稱年底前）","impact":"中","watch":"Palantir 是否被排除，歐洲其他國家是否跟進。"}],"_projected_from":"v19"}
```
