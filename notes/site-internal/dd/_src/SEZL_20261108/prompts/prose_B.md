你是 stock-analyst v20 的**散文層（prose）agent**，標的 SEZL（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：SEZL　日期：2026-11-08　archetype：None　前份裁決：2026-10-05　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1910B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（739B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（772B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（615B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1105B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（404B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（704B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2141B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3354B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3224B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1910           3563-5090      5 條（2–6 內）  
s3                  8000         739           5083-7261      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2492          8756-12508      5 條（2–6 內）  
s6                 11000         404          7417-10596      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         704           1957-2796      5 條（2–6 內）  
s10                 5000        2141           2001-2859      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3224           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3896B；至少需散文≈41.10KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70
−70%
−58.5%
−50
−50%
0%
0
0.1
0.13%
0.4
0.5
0.7
0.75
0.78
0.8
0.9
0.99
1
1.04
1.05
1.086
1.18
1.2%
1.226
1.32
1.5
1.665
1.80
02
2
2%
2.1
2.18
2.2
2.3
2.39
2.4
2.5
2.5%
2.7
2.7%
2.777
3
3%
03
3.12
3.159
3.2%
3.4
3.5%
3.6%
3.72
4.0%
4
04
4.2%
4.2
4.3
4.35
4.4
4.5
4.56
5
05
5%
5.2
5.26
5.4
5.45
5.475
5.50
5.81
6
6.0%
06
6.2
6.4
6.5
6.65
07
7%
7
7.1%
7.20
7.30
7.3
7.5
7.60
7.7
7.8
7.9
7.95
8%
08
8
8.3%
8.9
9%
9
9.8
10
10%
10.1
10.3
10.30
10.5
11
11.4
11.5
11.9%
11.9
12
12.4
12.5%
12.5
13%
13
13.6%
14
14.7%
15%
15.2
16
16.7
18%
18
20%
20.8
21
22
22.1%
22.47
22.7%
23%
24
24.1
25
26
27.29
27.3
28.1%
28.41
28.7%
28.8%
28.8
30
30%
31
31%
32%
33.0%
33.7%
34.8%
34.9%
35%
35.9%
36%
37
39
39.68%
40.2%
41
42
42.1%
42.5%
42.6%
43.0
45
47%
47
47.3
49
50%
50.48
52
54
55%
55.11
55.11%
58%
58.5%
60
60%
62
62.5%
63.18
64.7%
65.06%
68.1%
70
70%
72%
78%
78
82
83.2%
95
97.4%
100%
100
101.5
103
105
110.85
125
137
139
149.43
150%
157
160.6
165
168
185.4
240
250
276
310
340
370
378
680
2022
2024
2025
2026
2027
2028
2029
2031
20261108
1,116
1,248
1,567
1,590
1,940
2,110
2,800
4,780
7,010
8,460
955,000
−1,400
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
{"meta":{"ticker":"SEZL","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Sezzle Inc."},"oneliner":"訂閱與短天期放款把獲利推到新高，第三季也達到前份的進場條件，但股價五週漲 34.8%，FY2027 財測本益比升到 20.8 倍，基準五年年化約 6–7%，信用週期又未驗證，等 125 美元以下再買。","thesis":{"H":[{"id":"H1","text":"訂閱把一次性分期變成經常性關係，帶動頻率與每用戶營收同步上升。","2y":"2027 年底活躍訂閱 ≥125 萬人，每季單位變現用戶營收 ≥45 美元","5y":"2031 年底活躍訂閱 ≥250 萬人","10y":null,"threshold":"2027 年底訂閱低於 125 萬人，或每季單位變現用戶營收連 2 季低於 41 美元","source":"公司每季新聞稿與法說","drift_rule":"2 年期連 2 季偏離 ≥5% 視為削弱，連 3 季偏離 ≥10% 視為反轉；5 年期連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"},{"id":"H2","text":"短天期放款的定價與風控撐得住，淨交易利潤率留在目標區間，提列不超過 TTV 3%。","2y":"FY2027 淨交易利潤率 ≥58%，全年提列占 TTV ≤3%","5y":"經歷一次消費信貸下行，單年淨交易利潤率不低於 50%","10y":null,"threshold":"淨交易利潤率連 2 季 <55%，或全年提列占 TTV ≥3.5%","source":"公司每季新聞稿與法說","drift_rule":"2 年期連 2 季偏離 ≥5% 視為削弱，連 3 季偏離 ≥10% 視為反轉；5 年期連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"},{"id":"H3","text":"銀行執照與非購物產品打開第二條成長曲線，擴大消費者錢包份額。","2y":"2028-04 前取得國家銀行執照，SezzleCash 與 Send 占 TTV ≥10%","5y":"FY2031 每股盈餘 ≥12.5 美元","10y":null,"threshold":"2028-04 前遭否決或撤件，或 FY2028 非購物 TTV 占比 <5%","source":"監管機關公告、8-K、每季法說；公司若不拆非購物 TTV 則標資料缺口","drift_rule":"2 年期連 2 季偏離 ≥5% 視為削弱，連 3 季偏離 ≥10% 視為反轉；5 年期連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"消費信貸轉壞，新用戶與較長天期同時放大損失；關稅與失業等總經因素會透過消費者還款能力傳導。","h_ref":"H2","clock":"🔥","threshold":"全年提列占 TTV ≥3.5%，或應收帳款年增率高於 TTV 年增率 30 個百分點以上連 2 季且提列率年增","evidence_refs":["reg_tariff_export#0"]},{"id":"R2","text":"SezzleCash 與 Send 利潤率較低，初期損失較高，規模放大後稀釋淨交易利潤率。","h_ref":"H2","clock":"⚡","threshold":"扣除 Visa 效益後的淨交易利潤率連 2 季 <58%","evidence_refs":[]},{"id":"R3","text":"訂閱費與預借現金被監管或法院視為利息，或消費者訴訟擴大；目前僅有律所調查公告。","h_ref":"H3","clock":"🐢","threshold":"聯邦或州機關正式執法，或消費者集體訴訟通過駁回動議","evidence_refs":["regulatory_antitrust#2"]},{"id":"R4","text":"大型商家與平台集中，商家費率被壓，獨家權被競爭對手拿走。","h_ref":"H1","clock":"🔥","threshold":"Target 或大型平台終止合作，或公司揭露單一商家流失影響 TTV ≥5%","evidence_refs":["customer_second_source#0","geo_supply_chain#2","supply_demand_durability#2"]},{"id":"R5","text":"銀行夥伴協議非獨家且可在特定事件終止，取得銀行執照前存在單點依賴。","h_ref":"H3","clock":"⚡","threshold":"WebBank 發出終止通知且 6 個月內無替代方案","evidence_refs":["geo_supply_chain#0"]},{"id":"R6","text":"治理與財報可信度：2024 年現金流量表重編、董事 Karen Webster 請辭並表達分歧、多家律所公告證券調查。","h_ref":"H2","clock":"⚡","threshold":"第二次不可依賴公告涉及損益，或證券集體訴訟正式提起並通過駁回動議，或 SEC 正式調查","evidence_refs":["major_events#0","sec_investigation_restatement#0","major_events#4","regulatory_antitrust#3","lawsuit_class_action#1"]}],"single_thing":{"description":"FY2027 全年信用損失提列占 TTV 達 4.0% 以上，FY2026 指引約 2.5%。","why_fatal":"以 FY2027 TTV 約 70 億美元（本輪假設）計，多 1.5 個百分點稅前少約 1.05 億美元，每股少約 2.4 美元，占 7.20 美元財測三分之一；同時市場會把公司從成長股改用放款股定價。其他單項較小，淨交易利潤率少 5 個百分點每股約少 0.9 美元。","if_happens":"清倉，不逢低補；情境改走 Bear 路徑，要重跑完整研究才可能再進場。","how_monitor":"每季新聞稿與法說的提列占 TTV，領先指標是應收帳款年增率減 TTV 年增率的差距；2022 年以前的提列率事實表未涵蓋。","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":22.47,"peg_fy2":0.78,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":3.72,"FY2026E":5.26,"FY2027E":6.65,"FY2028E":7.95},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS；FY2026E–FY2028E 為 Koyfin 2026-11-07 共識快照，未反映 2026-11-04 公司財測 5.45–5.50 美元與 FY2027 初步財測 7.20 美元"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SEZL_20261108/scenario.json","archetype":{"primary":"金融","secondary":"品質複利成長","confidence":"中","fingerprint":"短天期無擔保消費信貸加訂閱費，提列占營收 22.7%，10 月遞交國家銀行執照"},"industry":{"clock_phase":"II","sd_verdict_source":"擴張期：美國 BNPL 2026 年預估年增 14.7%、2027 年 11.9%，成長放緩但未收縮（eMarketer 彙整），第三季提列年減顯示信用環境仍順。供需持久性：需求結構性持久，供給可逆性高，銀行與科技公司隨時能加入，信用轉壞時供給也會快速收縮。","bargaining":{"up":"對 Visa 有談判成果，第三季獨家安排帶來 370 萬美元效益；對銀行夥伴 WebBank 仍是依賴方，協議非獨家且可在特定事件終止。","down":"對企業級商家議價弱，商家正從獨家轉向多家 BNPL；對消費者有訂閱定價權，但取消容易。","geo":"業務集中在美國與加拿大，地緣風險低，關稅只透過消費支出間接影響。"},"profit_pool_dir":"利潤池五年變化事實表未涵蓋；管理層稱份額來自區域銀行與信用合作社（2026-06 報導），屬公司說法。","tam_table":[{"item":"美國 BNPL 市場 2026 年預估","value":"1,116 億美元，年增 14.7%（eMarketer 彙整）"},{"item":"美國 BNPL 市場 2027 年預估","value":"1,248 億美元，年增 11.9%（eMarketer 彙整）"},{"item":"六大業者 2025 年發放信貸","value":"1,567 億美元（Fed 資料經彙整站轉述，口徑與上兩列不同）"},{"item":"Sezzle 2025 年份額","value":"39 億美元，約占六大業者 2.5%"},{"item":"訂閱占活躍消費者","value":"約 31%（第三季訂閱 955,000 人對第一季活躍消費者 310 萬人，期間不同）"},{"item":"營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"重複交易累積的放款資料加上短天期快速調額度的風控循環，再由訂閱與 Anywhere 虛擬卡把消費者留在自家 App，降低對單一商家結帳按鈕的依賴。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：訂閱年增 68.1%、頻率 6.5 次升到 7.8 次、營收收益率年增 60 個基點、Pay-in-5 已占核心 BNPL 約 70%。定價面穩定：商家端費率承壓，公司靠消費者付費方案爭取商家，訂閱又容易取消。兩者合成穩定，留存未揭露前不上調。","peer_na_reason":"事實表只有同業利潤率，沒有投入資本，無法計算對最強同業的 ROIC 差距，改用留存與頻率軸，而留存又未揭露。","threats":[{"level":"🟡","text":"銀行信用卡轉分期，以及 Apple、PayPal 等整合先買後付；目前未見具名的 2026 新進入者，來源多為二手彙整，所以只算點對點競爭。","p":"30%","evidence_refs":["competitive_share_entrants#4","substitute_technology#0"]},{"level":"🟡","text":"企業級商家費率壓力與獨家權重分配，公司改用隨選付費方案把費用轉給消費者來爭取商家。","p":"35%","evidence_refs":["supply_demand_durability#2"]},{"level":"🟡","text":"Target 在融資協議的集中上限最高，這是額度上限而非實際占比；少數大型電商平台轉向會不成比例衝擊，但 FY2025 無單一對象占營收 10% 以上。","p":"15%","evidence_refs":["customer_second_source#0","geo_supply_chain#2"]},{"level":"🟡","text":"代理式購物可能繞過結帳按鈕；執行長 2026-11-04 說 Anywhere 虛擬卡可載入購物助理，附著點在自有資產上，AI 帶來的淨增量事實表未涵蓋，分界年估 2028。","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者與決策者都是消費者，訂閱費也由消費者付，短期流動性對信用受限族群是需要而非想要；第三季重複交易占 97.4%，頻率年增到 7.8 次。"},{"item":"決策層級","level":"🟡","text":"消費者可在結帳時改用其他 BNPL，商家也從獨家走向多家；財務長 2026-11-04 說訂閱很容易取消，流失率與獲客成本都未揭露，替代性只能間接判斷。"},{"item":"價值鏈分配","level":"🟡","text":"Visa 獨家安排顯示公司拿到部分網路端讓利，但商家費率承壓，WebBank 協議可在特定事件終止；公司多拿的部分主要來自消費者付費。"},{"item":"社會容忍度","level":"🟡","text":"第三季年化營收約為應收帳款 2.1 倍，客群信用受限，又新增預借現金；CFPB 壓力暫緩，但銀行執照審查與律所調查會提高能見度，政治上限低於經濟上限。"}],"roiic":78,"reinvest_rate":60,"endo_ceiling":47,"formula_note":"單位皆為百分比。稅後營業利益＝TTM 營收約 5.81 億美元×營業利益率 39.68%×（1－第三季稅率 22.1%）≈1.80 億美元；投入資本＝權益 2.777 億＋借款 1.04 億－現金 7,010 萬≈3.12 億美元，當期 ROIC 約 58%。增量：第三季淨利年增 2,110 萬美元，年化約 8,460 萬；投入資本增加約 1.086 億（權益＋1.226 億、借款－1,400 萬，一年前現金事實表未涵蓋），ROIIC 約 78%；再投資率 1.086÷1.80≈60%；內生上界 78%×60%≈47%。放款公司的營運資金增加以投入資本變動代替公式中的各項。ROIIC 砍半時上界約 23%。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","SEZL":74.33,"AFRM":68.07,"PYPL":45.76,"unit":"%"},{"metric":"營業利益率","SEZL":39.68,"AFRM":20.44,"PYPL":18.52,"unit":"%"},{"metric":"FCF 利潤率","SEZL":65.06,"AFRM":23.3,"PYPL":18.37,"unit":"%"},{"metric":"研發密度","SEZL":null,"AFRM":null,"PYPL":9.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"AFRM","gm":68.07,"om":20.44,"fcf_margin":23.3,"rd_intensity":null,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"PYPL","gm":45.76,"om":18.52,"fcf_margin":18.37,"rd_intensity":9.56,"period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主：TTV 年增 34.9%；價為輔：營收占 TTV 年增 60 個基點；無併購，回購影響小。","runway_years":"份額口徑約 18 年（TTV 年增 30%、市場年增 13% 的機械推算，高估）；訂閱滲透口徑約 1 年內超過 35%","runway_post_y5":"🟡","endo_ceiling_basis":"沿用護城河段的再投資推導：上界約 47%，壓力版約 23%。三年共識 EPS 年複合 28.8% 在上界內但高於壓力版，基準情境年複合約 18% 兩版都在上界內。","segments":{"expanded":false,"reason":"證據包沒有第三季 10-Q 的收入拆分，訂閱、商家費、利息與預借現金的金額事實表未涵蓋，只有法說的綜合收益率，無法展開。"},"decay_signals":[{"name":"毛利率連 2 季年減","lit":false,"note":"第三季淨交易利潤率年增 10.5 個百分點"},{"name":"核心市占 12 個月縮減","lit":false,"note":"TTV 年增 34.9%，高於市場預估 14.7%"},{"name":"主力產品提價後銷量下滑","lit":false,"note":"證據包未見提價後量縮"},{"name":"EPS 成長顯著高於營收成長","lit":false,"note":"共識 FY2025–2027 EPS 年複合 33.7%、營收 33.0%，差 0.7 個百分點"},{"name":"FCF／淨利低於 0.75 連 2 年","lit":false,"note":"約 2.1 倍，但現金流分類使 FCF 偏高，不當作品質證據"},{"name":"SBC 占營收大於 5% 且上升","lit":false,"note":"年化約 1.2%"},{"name":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"市場成長放緩但仍為正"},{"name":"產業倍數三年系統性下移","lit":false,"note":"事實表未涵蓋，未計入"},{"name":"維護性資本支出占 FCF 大於 60%","lit":false,"note":"輕資產模式不適用"},{"name":"停止投資新產能且收入下滑","lit":false,"note":"新產品持續上線，收入成長"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長是有機的，未見併購；現金去向四分與回購均價事實表未涵蓋，無法展開成表。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 未見併購項目，無併購報酬可評","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"今年前三季回購 2,800 萬美元；回購均價與 10 年期殖利率事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"上半年 SBC 340 萬美元，年化約 680 萬，對市值 50.48 億美元約 0.13%","grade":"過"}]},"valuation":{"basis":"放款公司以 P/E 為主，採當年度 EPS 同口徑，並用 FY2027 公司初步財測交叉檢查。","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有 AFRM、PYPL、Klarna 的前瞻倍數，無法做同業倍數對照。"},"fwd_pe":28.41,"peg":0.99,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"PEG＝28.41÷28.8≈0.99，屬合理。但 FY2027 本益比由前份 16.7 倍（110.85÷6.65）升到 20.8 倍（149.43÷7.20），EPS 錨只上修 8.3%，其餘都是倍數擴張；基準五年年化約 6–7%，機率加權五年約＋36%，低於 8% 的及格線。真實五年分位事實表未涵蓋，年度端點分位 100 只有 3–4 個點，僅看方向。結論偏貴。","upside_short_pct":7.5,"upside_mid_pct":24.1},"trap_analysis":{"verdict":"🟢","label":"衰退信號未出現，風險在信用週期"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"提列 2.7% 是沒有經歷信用下行的數字；應收帳款年增 72%，快於 TTV 年增 34.9%，應收天數由約 16 天拉長到約 21 天，Pay-in-5 已占核心 BNPL 約 70%。","assumption":"短天期能讓公司在損失上升前快速收額度。","consequence":"提列多 1.5 個百分點，FY2027 每股約少 2.4 美元，倍數同時下移，五年終值約 62 美元，跌 58.5%。","ruling":"採納。這與唯一致命點是同一件事，已反映在 Bear 機率 30% 與進場價。","watch":"每季提列占 TTV，以及應收帳款年增率減 TTV 年增率的差距。","evidence_refs":["reg_tariff_export#0"]},{"view":"論點失敗","evidence":"第三季年化營收約為應收帳款 2.1 倍，客群信用受限，又推預借現金；律所已公告調查費用揭露，銀行執照結果公司自己也說不確定。","assumption":"監管維持目前的寬鬆態度，訂閱費不被視為利息。","consequence":"訂閱與預借現金的費率受限，第二條曲線關閉，成長回到 BNPL 市場增速。","ruling":"部分採納。目前沒有政府機關行動，律所公告證據力低，列為長期風險，不提高短期機率。","watch":"聯邦或州機關正式行動、銀行執照審查結果。","evidence_refs":["regulatory_antitrust#2"]},{"view":"論點成功但股東經濟變差","evidence":"訂閱淨增由 14 萬降到 10.1 萬，行銷由 1,940 萬降到 1,590 萬美元，每淨增一人行銷約由 139 美元升到 157 美元；財務長 2026-11-04 說 Cash 與 Send 利潤率較低，初期損失較高；執行長說執照期間傾向多留現金。","assumption":"訂閱增加會同步帶來相同的單位獲利，現金會配回股東。","consequence":"用戶與營收都達標，但淨交易利潤率回到區間中段，ROE 被資本要求稀釋，每股成長低於用戶成長。","ruling":"採納。基準情境已假設淨交易利潤率回到約 60%，銀行資本要求的金額事實表未涵蓋。","watch":"扣除 Visa 效益後的淨交易利潤率、每淨增一人的行銷費用、執照核准條件。"},{"view":"價格已反映太多","evidence":"26 週漲 55.11%，自前份以來漲 34.8%；FY2027 本益比 20.8 倍高於前份 16.7 倍；賣方目標價 137–168 美元多在第三季前，現價已接近其均值。","assumption":"市場會繼續按財測上修幅度給高倍數。","consequence":"就算 FY2027 達標，倍數回到 18 倍以下，一年持有報酬也接近零。","ruling":"採納。價格是目前唯一卡住進場的因素。","watch":"股價是否回到 125 美元以下，賣方在第三季後的目標價更新。"}],"max_dd":{"lo":-70,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 110.85 → 本次 149.43（+34.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=110.85","side_b":"本次 price_at_dd=149.43","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 110.85 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 110.85 美元：Bull 價 276、Bear 價 54，五年期望值 +40.2%，基準年化 7.1%，不對稱比 2.4","side_b":"本次情境、股價仍用 110.85 美元：Bull 價 378、Bear 價 62，五年期望值 +83.2%，基準年化 12.5%，不對稱比 4.56","ruling":"先換情境、股價不動：五年期望值多 43.0 個百分點，基準年化多 5.4 個百分點。不對稱比由 2.4 變為 4.56。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 110.85 美元：五年期望值 +83.2%，基準年化 12.5%，不對稱比 4.56","side_b":"本次情境、股價 149.43 美元：五年期望值 +35.9%，基準年化 6.0%，不對稱比 2.18","ruling":"再換股價、情境不動：起點價上漲 34.8%，五年期望值少 47.3 個百分點，基準年化少 6.5 個百分點，不對稱比由 4.56 降到 2.18。合計五年期望值比前份少 4.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份觀望後股價大漲，進場首倉條件已經成立","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-10-05 於 110.85 美元觀望，條件是第三季提列守在 2.5–3%、淨交易利潤率 ≥55% 就進場首倉。第三季提列占 TTV 2.7%、淨交易利潤率 64.7%，條件已發火，分母由 GMV 改 TTV，差異小。","side_b":"股價到 149.43 美元，漲 34.8%。FY2027 EPS 錨只由 6.65 美元上修到 7.20 美元，多 8.3%，差額幾乎都是倍數擴張，估值結論由合理轉為偏貴。","ruling":"不翻多，維持觀望，機率維持 25／45／30，最大回撤下緣維持 −70%。前份的錯在進場條件沒寫價格上限，也低估下半年成長，這段漲幅確實錯過；但條件成立時價格已先走，追價的基準年化只有約 6–7%。","evidence_level":"公司揭露與市場價格","settle_metric":"股價相對 125 美元，以及第四季提列占 TTV","if_then":["若股價回到 125 美元以下且信用未惡化，則進場首倉 2%","若股價續漲而第四季信用尚未驗證，則不追","反向條件：若第四季提列占 TTV 高於 3.6%，則價格到位也不進場，順延一季"],"evidence_refs":[]},{"axis":"進場首倉條件改成價格錨","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"第三季財報提列／GMV 守在全年 2.5–3% 指引內且淨交易利潤率 ≥55% 即進場首倉；股價先跌破 95 美元而信用未惡化則分批反買","side_b":"股價≤125 美元，最近一季提列占 TTV 不高於去年同季且淨交易利潤率≥55% 即進場首倉；股價≤105 美元而信用未惡化則分批反買","ruling":"舊條件的基本面部分已達成，留著沒有約束力。新條件把唯一卡住的價格寫成進場首倉門檻，125 美元對應基準年化約 10%；分批反買由 95 美元上移到 105 美元，因為 FY2027 財測高於舊共識 8.3%，52 週均線也已升到 101.5 美元。","evidence_level":"公司揭露","settle_metric":"股價與每季提列占 TTV","if_then":["若股價≤125 美元且第四季提列不高於去年同季，則進場首倉 2%","若股價≤105 美元而信用未惡化，則分批反買至 3%"],"evidence_refs":[]},{"axis":"Single Thing 由缺值補上","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要沒有保留唯一致命點（欄位為空）","side_b":"FY2027 全年信用損失提列占 TTV 達 4.0% 以上","ruling":"Single Thing 依數學敏感度選定：提列多 1.5 個百分點每股約少 2.4 美元，淨交易利潤率少 5 個百分點約少 0.9 美元，前者最大。","evidence_level":"本輪依公司揭露推算","settle_metric":"FY2027 全年提列占 TTV","if_then":["若全年提列占 TTV ≥4.0%，則清倉"],"evidence_refs":[]},{"axis":"清倉與減碼門檻由缺值補上","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要沒有保留清倉與減碼門檻（欄位為空）","side_b":"全年提列占 TTV ≥3.5% 減碼一半、≥4.0% 清倉；淨交易利潤率連 2 季 <55% 減碼一半","ruling":"補上可量化門檻，資料都來自每季新聞稿，減碼與清倉分兩段，避免季節性單季波動誤觸。","evidence_level":"公司揭露","settle_metric":"每季與全年提列占 TTV、淨交易利潤率","if_then":["若全年提列占 TTV ≥3.5%，則減碼一半","若淨交易利潤率連 2 季 <55%，則減碼一半"],"evidence_refs":[]},{"axis":"品質訊號與價值陷阱判斷","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份訊號 B、價值陷阱風險 🟡。","side_b":"第三季營收年增 42.6%、淨交易利潤率年增 10.5 個百分點，十類衰退信號都未出現，其中產業倍數一項事實表未涵蓋。","ruling":"價值陷阱風險降為 🟢，訊號維持 B。陷阱風險轉好不代表信用風險消失，後者已放進 Bear 機率。","evidence_level":"公司揭露","settle_metric":"毛利與淨交易利潤率年變化","if_then":["若淨交易利潤率連 2 季年減，則價值陷阱風險回到 🟡 並停止加碼"],"evidence_refs":[]},{"axis":"護城河方向與五年後成長空間","cause":"新證據","prior_field":["moat_trend","runway_post_y5"],"side_a":"訂閱年增 68.1%、頻率 7.8 次、單位變現用戶營收年增 28.1%，銀行執照已遞件，看來應上調。","side_b":"留存與獲客成本未揭露，信用週期未驗證，銀行執照結果未定，SezzleCash 與 Send 量仍很小。","ruling":"方向維持 →，成長空間維持 🟡。新證據偏正，但都是順風期的結果指標，還不足以證明持續性。","evidence_level":"公司揭露","settle_metric":"留存率揭露、銀行執照核准、信用下行期的淨交易利潤率","if_then":["若公司揭露訂閱留存且逐年改善，或信用下行期淨交易利潤率仍 ≥55%，則方向上調為擴大並重算情境","若銀行執照遭否決，則成長空間降為 🔴 並停止加碼"],"evidence_refs":[]},{"axis":"公司類型由品質複利改列金融","cause":"新證據","prior_field":["archetype"],"side_a":"前份列品質複利成長。","side_b":"2026-10 遞交國家銀行執照，2026-06 推出預借現金，第三季提列約占營收 22.7%，獲利對信用高度敏感。","ruling":"改列金融，第二類型保留品質複利。獲利要用走過信用週期的標準看，終端倍數因此低於現值。","evidence_level":"公司揭露","settle_metric":"銀行執照進度與提列占營收","if_then":["若銀行執照遭否決且放款占比下降，則重新檢討公司類型"],"evidence_refs":[]},{"axis":"週期位置不適用","cause":"方法變動","prior_field":["cycle_position"],"side_a":"前份未填週期位置。","side_b":"本次仍不填，公司不屬循環或商品股。","ruling":"信用週期風險放在情境機率與提列門檻，不另填週期位置。","evidence_level":"判斷","settle_metric":"全年提列占 TTV","if_then":["若提列占 TTV 連 2 季年增，則把信用下行機率由 30% 上調並重算"],"evidence_refs":[]},{"axis":"下半年減速指引與實際落差，以及財測保守度","cause":"新證據","prior_field":null,"side_a":"2026-08-06 第二季法說，財務長 Lee Brading 指引下半年營收約年增 30%，並說財測不含 Sezzle Send，執行長 Charles Youakim 說未假設 SezzleCash 有重大上行；消息公布後股價盤前跌 23%。","side_b":"2026-11-04 第三季法說，營收年增 42.6%，全年上修到約 42.5%；財務長 Lee Brading 說 FY2027 的 7.20 美元包含已上線產品。","ruling":"8 月的減速警告被第三季否定，指引保守這點成立。但 FY2027 財測已納入已上線產品，保守度低於 2026 年，7.20 美元不能照 2026 年從 4.35 美元上修的幅度外推，基準只放 7.30 美元。","evidence_level":"法說逐字稿","settle_metric":"2027-02 正式財測","if_then":["若正式財測每股 ≥7.60 美元，則基準路徑上調一檔並重算進場價","若 7.20 美元被下修，則取消進場條件"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"淨交易利潤率 64.7% 是結構性還是順風","cause":"新證據","prior_field":null,"side_a":"年增 10.5 個百分點中，Visa 效益 2.2、資金成本約 1.5、交易費用約 0.8，合計約 4.5 偏結構性；收益率上升約 2.3，受訂閱組合帶動。","side_b":"提列下降約 3.4 個百分點偏週期性且未驗證；執行長 2026-08-06 說新用戶損失率較高，財務長 2026-11-04 說新產品利潤率較低，應收天數又在拉長。","ruling":"屬程度差異，可調和。基準情境讓淨交易利潤率回到約 60%，提列這部分放進 Bear 機率。Visa 效益是否經常性未證，持續監測。","evidence_level":"法說逐字稿，拆解為本輪推算","settle_metric":"扣除 Visa 效益後的淨交易利潤率、提列占 TTV","if_then":["若 2027 年第一季財報前未再出現同類 Visa 效益，則視為一次性，FY2027 每股預期下修約 0.1 美元","若扣除 Visa 效益後連 2 季 <58%，則停止加碼"],"evidence_refs":[]},{"axis":"自由現金流是否等於股東可拿的錢","cause":"新證據","prior_field":null,"side_a":"TTM FCF 利潤率 65.06%，遠高於 AFRM 與 PYPL。","side_b":"2026-02-25 不可依賴公告後，票據購入與還款列投資活動，放款成長不經過營業現金流；應收帳款一年增加約 1.32 億美元，FCF 約為淨利 2.1 倍。","ruling":"估值用淨利與 EPS，不用 FCF。這次重編只涉現金流分類，未動損益與資產負債表，屬內控瑕疵，不是獲利造假的證據。","evidence_level":"SEC 8-K","settle_metric":"10-K 內控結論、是否再有不可依賴公告","if_then":["若再出現不可依賴公告且涉及損益，則清倉","反向條件：若 FY2026 10-K 內控無重大缺失，則此項不再影響倉位"],"evidence_refs":["major_events#0","sec_investigation_restatement#0"]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭：Klarna 2025-03 取代 Affirm 成為 Walmart 獨家，商家費率承壓，銀行與科技公司持續加入。","side_b":"結構：訂閱與虛擬卡降低商家端依賴，TTV 成長高於市場；其他變數方面，CFPB 壓力緩和，銀行執照已遞件，但美國 BNPL 成長預估降到 11.9%。","ruling":"裁決為雙向拉鋸。商家端競爭在惡化，消費者端結構在轉好，淨效果要看留存與提列。","evidence_level":"二手彙整與公司揭露","settle_metric":"TTV 成長相對市場、企業商家新增與流失","if_then":["若 TTV 年增率低於市場增速連 2 季，則改判競爭惡化中並減碼一半"],"evidence_refs":["supply_demand_durability#2","competitive_share_entrants#4"]},{"axis":"現在就買的最強論證","cause":"價格變動","prior_field":null,"side_a":"FY2027 財測 20.8 倍對應 31–32% 成長，2026 年財測由 4.35 美元上修到 5.45–5.50 美元，放款成長靠自籌，總負債只有調整後 EBITDA 的 0.4 倍。","side_b":"同一組數字建立在順風的信用與區間上緣的利潤率上，倍數五週內已擴張，基準年化約 6–7%。","ruling":"不採納。若信用真的走過下行，現在不買會少賺，這個代價可以接受；因為看錯時的跌幅約 58.5%，大於少賺的部分。","evidence_level":"法說逐字稿與事實表","settle_metric":"第四季提列與 FY2027 正式財測","if_then":["若第四季提列 ≤3.2% 且正式財測每股 ≥7.60 美元，則重算基準，進場價可上移","若股價續漲而兩項都未驗證，則不追"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 125 美元以下且信用未惡化時進場首倉。","type":"估值rearm","maps_to":"H2","metric":"股價、最近一季提列占 TTV、淨交易利潤率","threshold":"股價≤125 美元；提列不高於去年同季；淨交易利潤率≥55%","action":"進場首倉 2%","source_freq":"每日收盤與每季新聞稿","date":null,"evidence_refs":[]},{"n":2,"text":"唯一致命點：FY2027 全年提列占 TTV 達 4.0% 以上。","type":"Single Thing","maps_to":"Single Thing","metric":"全年信用損失提列占 TTV","threshold":"≥4.0%","action":"清倉","source_freq":"年度財報","date":"2028-02","evidence_refs":[]},{"n":3,"text":"第四季提列高於全年指引隱含水準。全年約 2.5% 隱含第四季約 3.2%，第一季 TTV 事實表未涵蓋，以 11 億美元估算。","type":"風險","maps_to":"R1","metric":"第四季提列占 TTV","threshold":">3.6%","action":"不追，進場條件順延一季","source_freq":"每季新聞稿","date":"2027-02","evidence_refs":["reg_tariff_export#0"]},{"n":4,"text":"應收帳款成長持續快於交易量，且提列率開始年增。","type":"風險","maps_to":"R1","metric":"應收帳款年增率減 TTV 年增率","threshold":"差距 >30 個百分點連 2 季，且提列占 TTV 年增；第三季差距 37 個百分點","action":"停止加碼","source_freq":"每季新聞稿與法說","date":null,"evidence_refs":[]},{"n":5,"text":"全年提列超過 3.5%。","type":"減碼","maps_to":"R1","metric":"全年信用損失提列占 TTV","threshold":"≥3.5%","action":"減碼一半","source_freq":"年度財報","date":"2027-02","evidence_refs":[]},{"n":6,"text":"新產品或信用把淨交易利潤率壓到目標區間下緣以下。","type":"減碼","maps_to":"R2","metric":"淨交易利潤率（扣除 Visa 效益）","threshold":"連 2 季 <55%","action":"減碼一半","source_freq":"每季新聞稿","date":null,"evidence_refs":[]},{"n":7,"text":"驗證訂閱引擎：2027 年底活躍訂閱至少 125 萬人。","type":"假設驗證","maps_to":"H1","metric":"活躍訂閱人數","threshold":"2027 年底 ≥125 萬，或季淨增連 2 季 <4 萬即判落後","action":"未達則停止加碼","source_freq":"每季新聞稿","date":"2028-02","evidence_refs":[]},{"n":8,"text":"證券訴訟與治理：目前只有律所徵求投資人公告，受影響金額事實表未涵蓋，也未見已提起的集體訴訟。","type":"風險","maps_to":"R6","metric":"訴訟程序階段","threshold":"集體認證且不利和解則減碼一半；刑事或 SEC 正式調查則清倉","action":"依里程碑減碼一半或清倉","source_freq":"8-K 與法院公告，事件驅動","date":null,"evidence_refs":["regulatory_antitrust#3","lawsuit_class_action#1","major_events#4"]},{"n":9,"text":"銀行夥伴協議終止且沒有銀行執照或替代夥伴接手。","type":"清倉","maps_to":"R5","metric":"WebBank 計畫狀態","threshold":"終止通知且 6 個月內無替代方案","action":"清倉","source_freq":"8-K，事件驅動","date":null,"evidence_refs":["geo_supply_chain#0"]},{"n":10,"text":"Target 或大型平台流失。","type":"減碼","maps_to":"R4","metric":"單一商家流失對 TTV 的影響","threshold":"公司揭露影響 TTV ≥5%","action":"減碼一半","source_freq":"法說與 8-K","date":null,"evidence_refs":["customer_second_source#0","geo_supply_chain#2"]},{"n":11,"text":"首倉後信用連續驗證，才放大到上限。","type":"加碼","maps_to":"H2","metric":"提列占 TTV、訂閱季淨增","threshold":"連 2 季提列年減且訂閱季淨增 ≥8 萬","action":"加碼至 3%","source_freq":"每季新聞稿","date":null,"evidence_refs":[]},{"n":12,"text":"第四季財報與 FY2027 正式財測公布後重跑完整研究。","type":"複審日期","maps_to":"H3","metric":"FY2027 正式財測、提列指引","threshold":"財報公布即複審","action":"重跑完整研究","source_freq":"每季財報","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"全年信用損失提列占 TTV","bear_threshold":"≥3.5% 減碼一半，≥4.0% 清倉","window":"FY2026 至 FY2027 年度結果","source":"公司每季新聞稿與法說","last_status":"ok"},{"metric":"淨交易利潤率（扣除 Visa 效益）","bear_threshold":"連 2 季 <55% 減碼一半","window":"逐季至 FY2027","source":"公司每季新聞稿與法說","last_status":"ok"},{"metric":"應收帳款年增率減 TTV 年增率","bear_threshold":"差距 >30 個百分點連 2 季，且提列占 TTV 年增","window":"逐季至 FY2027","source":"公司每季新聞稿與法說","last_status":"warning"},{"metric":"活躍訂閱季淨增","bear_threshold":"連 2 季低於 4 萬人","window":"逐季至 FY2027","source":"公司每季新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#1","reason":"這是 10-K 的通用揭露，沒有供應商名稱、實際中斷紀錄或受影響交易金額，無法形成可監測的門檻；證據包也沒有任何服務中斷事件。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"上限 3%，深回撤區間 −50% 到 −70%，信用週期未驗證前不放大","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=55.11, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價≤125 美元，最近一季提列占 TTV 不高於去年同季且淨交易利潤率≥55% 即進場首倉；股價≤105 美元而信用未惡化則分批反買","exec_line":"現價不追。股價≤125 美元且信用未惡化時建首倉 2%；連 2 季提列年減且訂閱季淨增 ≥8 萬才加到 3%；股價≤105 美元而信用未惡化則分批反買；全年提列 ≥3.5% 減碼一半，≥4.0% 清倉。"},"reasoning":{"industry":"2026-11-04 第三季法說：營收 1.665 億美元，年增 42.6%；TTV 14 億美元，年增 34.9%；營收占 TTV 11.9%；交易相關成本占 TTV 4.2%；淨交易利潤率 64.7%，扣除 Visa 效益約 62.5%；淨利 4,780 萬美元，淨利率 28.7%；調整後 EBITDA 利潤率 42.1%；活躍訂閱 955,000 人，年增 68.1%。事實表的季度指標停在第二季，第三季數字取自逐字稿。收入分部金額事實表未涵蓋。單點依賴屬集中度風險，不是護城河證據：2026-05 融資協議對 Target 的集中上限 35%，其他商家 15%；WebBank 是銀行計畫夥伴；不過 FY2025 沒有單一對象占營收 10% 以上。","moat":"機制是重複交易累積的放款資料加上短天期調額度，訂閱與虛擬卡再降低對商家結帳按鈕的依賴。TTM 營業利益率 39.68%，高於 AFRM 與 PYPL，但兩邊資金結構與期間不同，事實表也沒有同業投入資本，算不出 ROIC 差距。第三季重複交易占 97.4%、頻率 7.8 次，都是正面訊號；財務長 2026-11-04 拒絕揭露獲客成本，留存因此無法驗證。當期 ROIC 約 58%，增量 ROIC 約 78%，都是信用順風下的讀數。","growth":"成長以量為主，TTV 年增 34.9%，收益率再加 60 個基點，沒有併購，回購影響小。三年共識 EPS 年複合 28.8%（FY2025A 3.72 美元到 FY2028E 7.95 美元，Koyfin 快照，早於第三季財測上調）。內生上界約 47%，壓力版約 23%，共識沒有超過上界，缺口為負。整體份額只有約 2.5%，但訂閱約占活躍消費者 31%，而訂閱年增 68.1%，遠快於第一季活躍消費者的 13.6%。下一條曲線要靠銀行執照與非購物產品：執行長 2026-11-04 說 SezzleCash 與 Send 量仍很小，執照結果也未定。美國 BNPL 成長預估降到 2027 年 11.9%。","governance":"TTM FCF 約為淨利 2.1 倍，但 2026-02 重編後票據購入與還款列投資活動，這個倍數不能當現金品質證據。SBC 上半年 340 萬美元，年化約占營收 1.2%、占市值 0.13%。今年前三季回購 2,800 萬美元，額度 1 億美元；回購均價與 10 年期殖利率事實表未涵蓋，回購報酬無法判定。應收帳款年增 72% 到 3.159 億美元，借款反由 1.18 億降到 1.04 億，流動性約 2.39 億美元。執行長 2026-11-04 說銀行執照期間傾向多留現金。現金去向四分事實表未涵蓋。","valuation":"現價 149.43 美元。事實表前瞻本益比 28.41 倍用的是 5.26 美元，這份 2026-11-07 快照低於 2026-11-04 的新財測 5.45–5.50 美元，共識近三個月修正 0% 是沒更新，不是沒上修。以財測中點算 27.3 倍，以 FY2027 初步財測 7.20 美元算 20.8 倍。短期目標按 FY2027 EPS 7.30 美元×22 倍約 160.6 美元；中期按 FY2029 EPS 10.30 美元×18 倍約 185.4 美元。賣方目標價 137–168 美元多停在第三季前，現價接近其均值，只能弱支持不追。真實五年分位事實表未涵蓋。","premortem":"十類衰退信號都未出現，價值陷阱風險低，真正風險是信用週期。成長熄火壓力以 FY2029 EPS 10.30 美元計：成長降到 15%、給 16 倍約 165 美元；降到 10%、給 10 倍約 103 美元；降到 5%、給 8 倍約 82 美元，跌幅小於 30% 的只有第一檔。歷史最大回撤事實表未涵蓋，可見的路徑波動是 2026-08 財報優於預期仍盤前跌 23%。股價高於 52 週均線 47%，RSI 63.18 未過熱，四週漂移事實表未涵蓋。第三季 Q&A 未迴避核心問題，但獲客成本與流失率仍拒絕揭露。"},"plain":{"six":{"how_it_makes_money":"Sezzle 賺的是信用受限消費者的訂閱費、分期與預借現金費用，加上商家手續費，錢卡在風控這一節：短天期放款的損失能不能壓在 TTV 的 2–3%。","moat":"護城河方向穩定（→）：執行面在擴大，定價面只能算穩定，留存與信用下行兩項證據還沒有。","growth":"五年後成長空間中等（🟡）：現在這台訂閱引擎的滲透率一年內會過 35%，第二條曲線還沒證明。","capital":"資本配置偏保守：股權稀釋很低，回購規模小，現金優先留給放款成長與銀行執照；三項評分只有稀釋一項能確認過關。","valuation":"現價要求 FY2031 每股盈餘到 12.5 美元，也只換來約 6–7% 年化；我相信這條基準路徑，但這個價不夠補償未驗證的信用週期。","how_wrong":"最可能看錯在信用：若短天期模型在下行期也守得住，現在不買就是再錯一次；若守不住，現價離合理價很遠。"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等股價回到 125 美元以下，且最近一季提列占 TTV 不高於去年同季、淨交易利潤率 ≥55%","trap":"🟢","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"金融","price_at_dd":149.43,"week26_return_pct":55.11,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母有三個版本：共識 5.26 美元未更新、財測 5.45–5.50 美元、FY2027 初步財測 7.20 美元。獲利又建立在目標區間上緣的淨交易利潤率、370 萬美元 Visa 效益與順風的提列上，因此不主張便宜。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 FY2027 正式財測","impact":"高","watch":"第四季提列占 TTV 是否高於 3.6%，每股財測是否 ≥7.60 美元"},{"date":"2027-Q4","date_precision":"quarter","type":"regulatory","event":"國家銀行執照審查，公司預期總時程 12–18 個月","impact":"高","watch":"核准、附條件或撤件，以及附帶的資本要求"},{"date":"2027-Q4","date_precision":"quarter","type":"other","event":"Shopify 反壟斷案證據開示預計延續至 2027 年","impact":"低","watch":"公司為原告，未計入任何情境；第三季兩項專案費用合計 240 萬美元"}],"_projected_from":"v19"}
```
