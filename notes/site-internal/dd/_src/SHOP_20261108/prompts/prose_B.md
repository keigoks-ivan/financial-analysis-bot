你是 stock-analyst v20 的**散文層（prose）agent**，標的 SHOP（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：SHOP　日期：2026-11-08　archetype：None　前份裁決：2026-08-08　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2027B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（716B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（990B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1403B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1072B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（599B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（728B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2147B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4572B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3051B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2027           3481-4973      5 條（2–6 內）  
s3                  8000         716           5099-7284      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3465          8074-11535      5 條（2–6 內）  
s6                 11000         599          7281-10401      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         728           1940-2772      5 條（2–6 內）  
s10                 5000        2147           1997-2853      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3051           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5041B；至少需散文≈39.96KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65%
−65
−64.5%
−60%
−58%
−45
−45%
−42%
−41%
−8.5%
−6.38%
−3.1%
−2.3%
−1.8%
−0.63%
−0.53%
−0.41%
0%
0
0.3%
0.4
0.79
0.94
1%
1.0
1
1.22
1.28
1.3
1.5
1.5%
1.63
1.8%
1.88
1.89
1.9
2.0
2
02
2.07
2.15
2.25
2.30
2.32
2.36
2.4
2.40
2.44
2.55
2.6
2.67
3%
3.0%
3
03
3.14
3.14%
3.17
3.2
3.3%
3.3
3.5%
3.5
3.9%
3.95
4
4.00
4.7
4.9
5%
05
5
5.85
6%
6
6.1
6.15
6.5
6.88
6.9%
7%
7
7.1
7.2%
7.375
7.80
7.8
8%
08
8.0
8
8.36
9
10%
10
11
11.4
11.4%
12
12%
12.21
12.49%
12.89%
13
13.4%
13.7
14%
14
14.8%
15
15%
15.2%
15.7
16%
17%
18
18%
18.07%
18.08%
18.1
18.2
19%
19.2%
19.24%
20
20%
20.07
22%
22
22.3%
23%
24%
24
25%
25
25.9%
26
26%
26.05%
26.5%
27%
28%
28
29%
29.06
29.2%
29.5%
30
30%
31.8%
32%
33%
33.66%
34%
34.87
34.87%
35
35%
37%
37.42
38
38.5%
40%
40
42
42.6%
42.76
44
44.96
45
47.27
47.49%
47.6%
48
48.07%
48.9%
49
50%
51
52
52%
52.7
52.8
55%
55.2
60
61.0
61.03
65
66.64%
67
68%
70
$70
71%
74%
76%
77%
77.7%
78%
78.79
79%
79
80
80%
86.4
88
90
$90
92%
100%
100
110
120
140
148.91
149
150
150%
151.57
157.58
158
158.6
174.57
176
195
200
216
231
240
243.8
250
296.4
420
510
2021
2022
2025
2026
2027
20261108
1,191
1,915.76
191,576
2,000
4,766
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
{"meta":{"ticker":"SHOP","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Shopify Inc."},"oneliner":"Shopify 商家拿走美國電商增量近半，GMV 年增 29.5%，護城河仍在變寬；但現價是 FY2026E 的 79 倍，EPS 五年複合 25% 加終端 30 倍也只換來年化約 3%，不追，等 110 美元以下或共識明顯上修。","thesis":{"H":[{"id":"H1","text":"Shopify 商家持續拿到遠高於份額的電商增量，GMV 成長維持在市場三倍以上。","2y":"FY2027–FY2028 固定匯率 GMV 年增不低於 24%。","5y":"FY2031E 美國電商份額達 20% 以上，營收年複合約 22%。","10y":null,"threshold":"固定匯率 GMV 年增連 2 季低於 24%；美國份額年增連 2 季不再上升；B2B GMV 年增低於 40%（後兩項沿用前份）。","source":"季報 8-K、法說、公司引 Census 與 eMarketer 的份額揭露，每季。","drift_rule":"2 年期：TTM 偏離路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉；5 年期：連 4 季達 5% 為削弱，連 6 季達 10% 為反轉。"},{"id":"H2","text":"支付與 Shop Pay 的貨幣化繼續上升，代理式交易不稀釋每筆 GMV 的收入。","2y":"到 FY2028 營收÷GMV 年比持續上升，支付滲透率不低於 71%。","5y":null,"10y":null,"threshold":"營收÷GMV 連 2 季年比不再上升；支付滲透率連 2 季不再上升；揭露向代理平台分潤。","source":"季報 8-K 的營收與 GMV，法說的支付滲透率與代理經濟說明，每季。","drift_rule":"2 年期：TTM 偏離路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"},{"id":"H3","text":"AI 與基礎建設成本被營運槓桿吸收，FCF 利潤率站穩 20%。","2y":"FY2027 FCF 利潤率不低於 19%，FY2028 不低於 20%；毛利金額增速高於營業費用增速至少 5 個百分點。","5y":"FY2031E 淨利率接近 19%。","10y":null,"threshold":"FY2027 FCF 利潤率低於 18%；訂閱毛利率連 4 季低於 77%；毛利金額增速減營業費用增速連 2 季低於 5 個百分點（現約 12 個百分點）。","source":"季報 8-K、現金流量表、法說，每季。","drift_rule":"2 年期：TTM 偏離路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉；5 年期：連 4 季達 5% 為削弱，連 6 季達 10% 為反轉。"}],"R":[{"id":"R1","text":"AI 代理接管買家入口與錢包預設，支付經濟被分走。","h_ref":"H2","clock":"🐢","threshold":"揭露向代理平台分潤，或支付滲透率連 2 季年比下降。","evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"]},{"id":"R2","text":"AI 與代管成本持續上升，訂閱毛利率回不到 80%，毛利金額增速長期落後營收。","h_ref":"H3","clock":"🔥","threshold":"訂閱毛利率連 4 季低於 77%，或毛利金額增速落後營收超過 5 個百分點連 4 季。","evidence_refs":["geo_supply_chain#0"]},{"id":"R3","text":"關稅與消費轉弱打到中小商家，GMV 下行、商家流失與貸款損失上升。","h_ref":"H1","clock":"⚡","threshold":"北美固定匯率 GMV 連 2 季低於 22%，或交易與貸款損失占營收高於 5%（2026 第二季 3.9%）。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R4","text":"Sezzle 反壟斷案與 Briskin 結帳隱私集體訴訟進入實質階段，Shop Pay 綁定或資料蒐集受限。兩案都是民事，受影響營收與結案時點事實表未涵蓋。","h_ref":"H2","clock":"🔥","threshold":"集體認證加不利和解，或判賠與和解超過 8 億美元（約一季 FCF）。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1"]},{"id":"R5","text":"大型對手用更大客群與通路壓價，Plus 與企業客戶擴張變慢。","h_ref":"H1","clock":"🔥","threshold":"Plus MRR 年增連 4 季低於 10%（Q3 為 18%）。","evidence_refs":["competitive_share_entrants#1"]},{"id":"R6","text":"倍數收斂快於 EPS 複利，營運達標時股東報酬仍不足。","h_ref":"H1","clock":"🐢","threshold":"FY2027E 本益比跌破 35 倍且共識同時下修。","evidence_refs":[]}],"single_thing":{"description":"前三大個人代理之一把自家錢包設為預設或向商家收通路抽成，且 Shopify 首次揭露代理式交易的支付附著低於網店。","why_fatal":"在單一事件能改變的變數裡，這項敏感度最大：商家解決方案占營收 78%，營收÷GMV 3.14%，每掉 30 個基點營收約少 10%，五年 EPS 複利與終端倍數會一起下修。","if_happens":"持有者減碼至半倉，未持有者取消進場條件，Bear 機率上調至 40%，重做情境。","how_monitor":"每季看法說對代理經濟的說明、支付滲透率、Shop Pay GMV 年增；事件面看 8-K 與代理平台條款公告。","probability":"12–24 個月約 15%。"}},"appendix_a":{"growth_durability":8,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":61.03,"peg_fy2":2.07,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":0.94,"FY2026E":1.89,"FY2027E":2.44,"FY2028E":3.17},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS，含大額營業外損益；FY2026E–FY2028E 為 Koyfin 共識，口徑事實表未標明，由季度共識量級推斷為調整後。兩者口徑不同，成長率以 FY2026E 為基期。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"固定匯率 GMV 連六季約 30%，TTM FCF 利潤率約 18%，SBC 約占營收 3.9%，淨現金約 45 億美元。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久。全球電商 2026–2027 年增約 7.2%（二手彙整引 EMARKETER），Shopify GMV 增速約為其四倍，擴張來自份額轉移。","bargaining":{"up":"對支付夥伴有議價力，Q3 商家解決方案毛利率年增來自與支付生態夥伴談到的節省（2026-11-03 Hoffmeister）；雲端依賴第三方，集中度事實表未涵蓋。","down":"對中小商家定價有上限，追蹤站記錄 2026-10 年繳牌價上調後隔日回復，此後無持續性漲價。","geo":"固定匯率 GMV 北美年增 28%、歐洲 33%；國際 GMV 年增 32%，國際支付毛利率通常較高（2026-08-05 Hoffmeister）。"},"profit_pool_dir":"利潤池往結帳與支付層集中，AI 代理入口是新的爭奪者；五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"全球電商規模 2026 年","value":"約 6.88 兆美元，年增 7.2%（二手彙整引 EMARKETER，非一手）"},{"item":"全球電商規模 2027 年","value":"約 7.375 兆美元，各來源區間 7.1–8.0 兆"},{"item":"Shopify 占全球電商（粗算）","value":"Q3 GMV 1,191 億美元×4 約 4,766 億美元，約 6.9%；未做季節調整，屬自算"},{"item":"美國電商份額","value":"約 14%（公司自揭，Census 與內部 GMV 估計）"},{"item":"全球零售占比","value":"不到 1%（2026-08-05 Finkelstein）"},{"item":"五年營業利益池占比變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"統一商務作業系統的轉換成本，加上 Shop Pay 與 Shop 買家網路的雙邊效應。","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行面擴大、定價權穩定。美國增量占比由三年前近五分之一升至近半，前份記錄美國份額年增 2 個百分點，Shop Pay GMV 年增 50%。反向證據是代理式交易的分潤尚未定案。","peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，BIGC 財務資料缺失，所以改用份額與利潤率對照。","threats":[{"level":"🔴","text":"AI 代理接管買家入口、代付與錢包預設，Shopify 從買家關係的擁有者退成後台。2026-03 OpenAI 撤下 Instant Checkout 是反例，但代理代購在 Q3 才開始出現。","p":30,"evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"大型對手以更大客群與通路壓價，可能讓 Shopify 流失潛在銷售或被迫降價。目前份額仍在上升，屬點對點壓力。","p":20,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"Sezzle 反壟斷案的壟斷主張進入審理，若 Shop Pay 分期的綁定受限，支付附著率會受影響；目前不是責任認定，受影響營收事實表未涵蓋。","p":15,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2"]}],"roic_durability":{"quadrant":"無法驗算，投入資本事實表未涵蓋；TTM 營益率 18.07%、FCF 利潤率 18.08%，資本輕，方向偏高周轉。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者與付款者都是商家，開店、收款、出貨是營運必需，延後代價高。年 GMV 達 100 萬美元的商家五年留存率 92%（2026-08-05 Hoffmeister），Q3 GMV 年增 29.5%。"},{"item":"決策層級","level":"🟡","text":"換平台要一起動線上店、門市、支付與平均 8 個應用程式，大型商家轉換成本高；小商家遷移容易，AI 建站也會降低門檻。分客群留存與漲價後流失事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"結帳與支付層目前仍在 Shopify 手上，商家解決方案毛利金額年增 37%；但代理平台握有買家入口。2026-11-03 Hoffmeister 只確認導流到商家網站時經濟模型相同，代理代購是否分潤沒有回答。"},{"item":"社會容忍度","level":"🟢","text":"收費約占 GMV 的 3.14%，事實表未見價格監管；搜尋未見 DOJ、FTC 或歐盟調查，目前是 Sezzle 與 Briskin 等民事訴訟。"}],"roiic":"事實表未涵蓋，缺投入資本；替代讀數為 FY2023 到 FY2025 增量營益率約 40%（營業利益增 18.1 億美元÷營收增 44.96 億美元，事實表 financial_history）。","reinvest_rate":"事實表未涵蓋，缺資本支出、折舊、營運資金與併購淨額。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率，兩項輸入都缺，不推估。這家公司的再投資主要走損益表（TTM 研發占營收 12.49%，2026 第二季行銷不到 14%），資產負債表口徑會低估真實再投資。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","SHOP":47.49,"WIX":66.64,"BIGC":null,"AMZN":51.08,"GDDY":63.75,"unit":"%"},{"metric":"營業利益率","SHOP":18.07,"WIX":-8.5,"BIGC":null,"AMZN":12.89,"GDDY":26.05,"unit":"%"},{"metric":"FCF 利潤率","SHOP":18.08,"WIX":19.24,"BIGC":null,"AMZN":-6.38,"GDDY":33.66,"unit":"%"},{"metric":"研發密度","SHOP":12.49,"WIX":34.55,"BIGC":null,"AMZN":null,"GDDY":16.34,"unit":"%"}],"competitors":[{"name":"WIX","gm":66.64,"om":-8.5,"fcf_margin":19.24,"rd_intensity":34.55,"strategy_note":"TTM 毛利率 66.64%，營益率 −8.5%，FCF 利潤率 19.24%；毛利高但營業利益為負，事實表沒有其商務 GMV，無法判斷份額方向。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BIGC","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"財務資料事實表無值，無法對照。"},{"name":"AMZN","gm":51.08,"om":12.89,"fcf_margin":-6.38,"rd_intensity":null,"strategy_note":"TTM 營益率 12.89%，FCF 利潤率 −6.38%；屬 10-K 所述可用更大客群與通路競價的大型對手類型。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"GDDY","gm":63.75,"om":26.05,"fcf_margin":33.66,"rd_intensity":16.34,"strategy_note":"TTM 營益率 26.05%、FCF 利潤率 33.66% 都高於 Shopify，獲利較高，但事實表沒有其成長與商務份額資料。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（GMV），支付附著次之，併購與回購不構成驅動。","runway_years":"美國線上約 6–8 年到 30%；全球零售不到 1%，國際更長","runway_post_y5":"🟢","endo_ceiling_basis":"事實表缺投入資本、資本支出與營運資金，增量 ROIC 與再投資率都算不出，天花板留空；情境樹保守視為共識超過天花板，Bear 機率取 30%。","segments":[{"item":"訂閱解決方案","value":"8.36 億美元，年增 20%，毛利率 79%"},{"item":"商家解決方案","value":"29.06 億美元，年增 35%，自算毛利率 38.5%，毛利金額年增 37%"},{"item":"線下 GMV","value":"年增 30%，累計突破 2,000 億美元"},{"item":"B2B GMV","value":"年增 74%，上季 76%"},{"item":"國際 GMV","value":"年增 32%，上季 37%"},{"item":"代理式交易","value":"AI 流量 2.6 倍、訂單 3.3 倍，量體仍小，公司未揭露占 GMV 比重"}],"decay_signals":[{"signal":"毛利率連 2 季年比下滑","status":"亮燈","note":"Q3 年減約 1.3 個百分點，第四季指引延續；Q2 為 47.6% 左右，去年同期數字事實表未涵蓋，FY2025 48.07% 與 TTM 47.49% 同方向。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠內生，近 12 個月未見大型併購；回購、股利與現金去向事實表未涵蓋，無法展開。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月未見大型併購；shop.com 約 1 億美元，報酬尚不可見。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購資料事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"現金流量表 SBC 140 百萬美元×4÷市值 191,576 百萬美元，約 0.3%／年，低於 1.5%；實際股數變動事實表未涵蓋。","grade":"過"}]},"valuation":{"basis":"前瞻本益比與 PEG 為主，EV／營收對照。","tier":"高成長商務平台","peers":{"expanded":false,"reason":"本包沒有同業倍數，同業表只有利潤率；唯一可用的是前份摘要的 NOW 28 倍，屬 2026-08 舊值，不足以展開。"},"fwd_pe":78.79,"peg":2.67,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"FY2026E 本益比 78.79÷FY2026E–FY2028E 共識 EPS 年複合 29.5%，PEG 2.67；FY2027E 口徑 2.07，都高於 2。基礎情境五年年化約 3%，低於 8%，判最貴一級。短期上行指 12 個月，FY2027E EPS 2.44 美元×65 倍約 158.6 美元；中期指 3 年，FY2029E EPS 4.00 美元×44 倍約 176 美元。","upside_short_pct":6.5,"upside_mid_pct":18.2},"trap_analysis":{"verdict":"🟡","label":"毛利率年比下滑亮燈，來自支付占比上升，需求沒有轉弱。"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"個人代理在 Q3 開始替使用者下單；2026-11-03 Wolfe 問代理是否分潤時，Hoffmeister 只回答導流到商家網站的情況。Baillie Gifford 與 10-K 都點出平台整合與資料限制的風險。","assumption":"Shopify 能守住結帳層，並讓 Shop Pay 成為代理內的常用錢包。","consequence":"代理平台若拿走入口與錢包，支付滲透率 68% 會下滑；營收÷GMV 每掉 30 個基點，營收約少 10%，倍數同時下移，五年虧 50% 以上最可能從這裡來。","ruling":"部分採納。AI 流量 2.6 倍、訂單 3.3 倍，量體仍小，OpenAI 2026-03 撤下 Instant Checkout 表示結帳層不易取代；分潤未定，保留在 30% 的 Bear 機率，與唯一致命點是同一件事。","watch":"代理式訂單的經濟模型揭露、支付滲透率、Shop Pay GMV 年增。","evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"],"fact_refs":["f_kpi0_gaap","f_kpi6_gmv"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營收年增 32%，毛利金額只增 28%，整體毛利率 47.6%，去年同期自算 48.9%；訂閱毛利率 79%，連兩季低於 80% 趨勢線，代管與 Sidekick 成本增加；Q3 FCF 年增大部分屬暫時。第三方雲端依賴也讓成本不全在公司手上。","assumption":"GMV 持續成長，利潤也等比增加。","consequence":"大型商家占比升高，價值更多落在低毛利支付；AI 功能不直接收費；營業費用率下降空間縮小後，EPS 複利會低於預期。","ruling":"部分反駁。商家解決方案毛利率連三季年增，Sidekick 總成本 Q2 到 Q3 下降 18%，支付端沒有侵蝕；訂閱毛利率下滑採納為監測項。","watch":"毛利金額年增與營收年增的落差、訂閱毛利率、營業費用占營收。","evidence_refs":["geo_supply_chain#0"],"fact_refs":["f_kpi0_gaap","f_kpi3_fcf","f_kpi5_q4_fy2026"]},{"view":"價格已反映太多","evidence":"FY2026E 本益比 78.79 倍，PEG 2.67，EV／FY2026E 營收 12.21 倍。","assumption":"市場五年後仍願給 30 倍以上，且 EPS 年複合 25%。","consequence":"基礎情境年化約 3%；EPS 達標時，股東報酬仍可能被倍數收斂吃掉。","ruling":"採納，這是本次不追的主因。要年化 10%，FY2031E EPS 需約 8.0 美元，高於多頭路徑。","watch":"股價是否到 110 美元以下；FY2028E 共識 EPS 是否到 3.95 美元以上。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy3"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 151.57 → 本次 148.91（-1.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=151.57","side_b":"本次 price_at_dd=148.91","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 151.57 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 151.57 美元：Bull 價 243.8、Bear 價 67，五年期望值 −2.3%，基準年化 −3.1%，不對稱比 1.3","side_b":"本次情境、股價仍用 151.57 美元：Bull 價 296.4、Bear 價 52.8，五年期望值 +11.4%，基準年化 3.0%，不對稱比 1.22","ruling":"先換情境、股價不動：五年期望值多 13.7 個百分點，基準年化多 6.1 個百分點。不對稱比由 1.3 變為 1.22。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 151.57 美元：五年期望值 +11.4%，基準年化 3.0%，不對稱比 1.22","side_b":"本次情境、股價 148.91 美元：五年期望值 +13.4%，基準年化 3.3%，不對稱比 1.28","ruling":"再換股價、情境不動：起點價下跌 1.8%，五年期望值多 2.0 個百分點，基準年化多 0.4 個百分點，不對稱比由 1.22 升到 1.28。合計五年期望值比前份多 15.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與裁決維持","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份：股價 151.57 美元，估值最貴一級，訊號 B，觀望，追蹤。","side_b":"本次：股價 148.91 美元，跌約 1.8%，估值仍是最貴一級，訊號 B，結論仍是不追。","ruling":"股價幾乎沒動，EPS 共識也沒有明顯上修，估值結論不變。","evidence_level":"事實表股價與共識快照","settle_metric":"股價與 FY2028E 共識 EPS","if_then":["若股價跌到 110 美元以下且基本面無損，則分批反買，首倉 1/3。","若股價續漲而共識未上修，則不追。"],"evidence_refs":[]},{"axis":"價值陷阱風險上調","cause":"新證據","prior_field":["trap"],"side_a":"前份：風險低（🟢）。","side_b":"本次：風險中等（🟡），毛利率年比下滑亮燈，Q3 47.6% 對去年同期 48.9%，第四季指引毛利金額增速仍低於營收。","ruling":"上調一級但不升到高風險，毛利率下滑來自支付占比，商家解決方案毛利率連三季年增。","evidence_level":"一手，8-K 與法說","settle_metric":"商家解決方案毛利率與毛利金額增速","if_then":["若訂閱毛利率連 4 季低於 77%，則持有者減碼至半倉。","若毛利金額增速連 2 季追上營收增速，則風險回到低。"],"evidence_refs":[]},{"axis":"護城河、跑道與公司類型維持","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河向上，跑道寬，品質複利成長，未標循環位置。","side_b":"本次：相同。新證據是美國增量占比近半、歐洲份額三年翻倍、B2B GMV 年增 74%、線下 GMV 年增 30%。","ruling":"維持。Q3 數字支持份額繼續上升，代理式風險放在威脅與情境機率，不提前下調方向。","evidence_level":"一手為主，份額由公司自揭","settle_metric":"美國增量占比、固定匯率 GMV","if_then":["若美國份額年增連 2 季不再上升，則方向改為穩定並停止加碼。","若第三方資料也確認份額上升，則維持。"],"evidence_refs":[]},{"axis":"情境機率與回撤幅度","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 30%，空頭 25%，最大回撤 −58%。","side_b":"本次：多頭 25%，空頭 30%，最大回撤 −45% 至 −65%。","ruling":"內生天花板缺投入資本無法驗算時採保守處理，空頭定在 30%；回撤由單點改成區間。","evidence_level":"判斷","settle_metric":"投入資本與增量 ROIC 補齊後重算","if_then":["若補齊資料後共識低於內生天花板，則空頭機率可回到 25%。","若高於天花板，則維持 30% 且信心不上調。"],"evidence_refs":[]},{"axis":"進場首倉門檻舊→新（估值 rearm）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價回檔至 $70–90 區間（$70≈PEG 1.0 對應 FY+1 共識成長 29.2%；上緣 $90 保留予國際 take rate 收斂槓桿〔Payments 僅covers~40國〕兌現空間）；或終端倍數假設站上同業現值上緣（NOW 28x）之後仍具正 EV；觸發後首階 1/3 分批建倉","side_b":"股價≤110 美元（基礎情境年化約 10%），或 FY2028E 共識 EPS≥3.95 美元且股價未同步上漲；觸發後重跑研究，首倉上限 1/3","ruling":"進場錨由 PEG 1.0 改成基礎情境年化約 10%，終端年滾到 FY2031E。舊的 70–90 美元等於要求年化 14% 至 20%；110 美元對應 FY2027E 口徑 PEG 約 1.5。前份 FY+2 共識上修≥33%、回檔≥20% 的條件同時改為本次兩個條件。","evidence_level":"判斷，由情境樹反推","settle_metric":"股價、FY2028E 共識 EPS","if_then":["若股價≤110 美元且固定匯率 GMV 仍高於 27%，則重跑研究，通過後首倉 1/3。","若到價但 H1 或 H2 已削弱，則不進場。"],"evidence_refs":[]},{"axis":"減碼與清倉指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設，值為 null。","side_b":"本次新設：固定匯率 GMV 連 2 季低於 24%；營收÷GMV 連 2 季年比不再上升；支付滲透率連 2 季不再上升；訂閱毛利率連 4 季低於 77%；毛利金額增速落後營收超過 5 個百分點連 4 季；揭露代理分潤。","ruling":"前份沒有獨立的減碼與清倉條件，本次補上；前份 H1、H2 的份額、B2B 與貨幣化門檻保留在論點門檻內。","evidence_level":"判斷","settle_metric":"季報與法說","if_then":["若單一指標成立，則持有者減碼至半倉。","若 H1 與 H2 同時反轉，則清倉。"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點舊→新","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設，值為 null。","side_b":"前三大個人代理之一把自家錢包設為預設或向商家收通路抽成，且 Shopify 首次揭露代理式交易的支付附著低於網店。","ruling":"Q3 是代理代購首次出現，分潤問題在法說被問到但沒有回答，所以本次設為唯一致命點。","evidence_level":"一手法說，事件尚未發生","settle_metric":"代理式交易的支付附著與分潤揭露","if_then":["若事件發生，則持有者減碼至半倉，未持有者取消進場條件。","若連 4 季支付滲透率續升且無分潤揭露，則機率下調至 10%。"],"evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"]},{"axis":"貨幣化門檻由季比改年比","cause":"方法變動","prior_field":["thesis.H2.threshold"],"side_a":"Take rate 連 2 季 QoQ 不再上升；或 Payments 滲透率連 2 季不再上升","side_b":"營收÷GMV 連 2 季年比不再上升；支付滲透率連 2 季不再上升；揭露向代理平台分潤。","ruling":"第四季 GMV 季節性放大，季比容易誤觸，所以改年比。沿用季比來看，Q3 3.14% 與前份記錄持平，記一季未升。","evidence_level":"一手，8-K","settle_metric":"營收÷GMV","if_then":["若連 2 季年比不再上升，則 H2 標削弱並停止加碼。","若年比恢復上升，則解除。"],"evidence_refs":[]},{"axis":"成長是否減速","cause":null,"prior_field":null,"side_a":"報表面：GMV 年增 29%，近五季最慢；訂閱營收年增由 22% 降至 20%；國際 GMV 由 37% 降到 32%，線下由 32% 降到 30%。","side_b":"管理層（2026-11-03 Hoffmeister）：固定匯率 30%，連六季相近，北美 28% 持平，第四季指引低 30% 段。","ruling":"可調和，屬程度差異。固定匯率減速幅度小，還不是趨勢反轉。","evidence_level":"一手，8-K 與法說","settle_metric":"固定匯率 GMV 年增率","if_then":["若連 2 季低於 24%，則 H1 標削弱，持有者停止加碼。","若回到 30% 以上，則維持。"],"evidence_refs":[]},{"axis":"代理式交易的經濟歸屬","cause":null,"prior_field":null,"side_a":"2026-08-05 Finkelstein：代理式交易沒有新費用、沒有另外定價。2026-11-03 Finkelstein：代理是新前門，其餘都是 Shopify。","side_b":"2026-11-03 Wolfe 問是否與代理分潤，Hoffmeister 只答導流到商家網站時相同，代理代購沒有回答；Jefferies 問 Shop Pay 與 Meta Pay 的經濟差異也沒有數字。外部評論認為 AI 平台可能接管結帳。","ruling":"方向相反，屬不可調和矛盾。目前選管理層一側，依據是代理式交易接的仍是商家結帳，且 OpenAI 撤下 Instant Checkout；決勝數據今天不存在，不可裁決至 2027 年底。","evidence_level":"一手法說，分潤數據不存在","settle_metric":"代理式訂單支付附著率與分潤揭露","if_then":["若揭露代理平台抽成或代理訂單支付附著低於網店，則持有者減碼至半倉，未持有者取消首倉條件。","若連 4 季代理訂單年增至少 2 倍且支付滲透率持續上升，則多頭機率上調 5 個百分點，但不追價。"],"evidence_refs":["competitive_share_entrants#3","substitute_technology#2"]},{"axis":"訂閱毛利率 80% 趨勢線","cause":null,"prior_field":null,"side_a":"2026-08-05 Hoffmeister：訂閱毛利率略低於 80%，Sidekick 放量下季對季維持相近。","side_b":"2026-11-03：79%，季減，主因代管成本；被問 80% 趨勢線時回答沒有改變，但沒有時間表，第四季還有基礎建設支出。","ruling":"可調和，但管理層說法偏樂觀。Sidekick 總成本季減 18% 屬實，壓力轉到代管。標為未證、監測。","evidence_level":"一手法說","settle_metric":"訂閱毛利率","if_then":["若 2027 上半年沒有回到 79% 以上，則視為結構性成本，Bear 機率不下調。","若連 2 季回到 80%，則解除此項監測。"],"evidence_refs":["geo_supply_chain#0"]},{"axis":"FCF 改善有多少是結構性","cause":null,"prior_field":null,"side_a":"2026-11-03 Hoffmeister：年增約 150 個基點屬結構性；2026-08-05 也說扣除會計變更年增約 1.5 點。","side_b":"第四季指引 FCF 利潤率只與去年相當；Q3 其餘年增來自三項暫時因素；2026-08-05 被問 20% 是否新常態時未正面回答。","ruling":"不採信也不否定，標未證、監測。預先設定：FY2027 前兩季 FCF 利潤率平均年增低於 100 個基點，結構性說法視為不成立。","evidence_level":"一手法說","settle_metric":"FCF 利潤率年增","if_then":["若 FY2027 前兩季平均年增低於 100 個基點，則 H3 標削弱，持有者停止加碼。","若平均年增達 150 個基點以上，則採信結構性說法。"],"evidence_refs":[]},{"axis":"賣方共識與本次看法","cause":null,"prior_field":null,"side_a":"賣方：一源稱 51 位中 38 位正面，平均目標價 157.58 至 174.57 美元，Citi 216、RBC 200、Cantor 158。","side_b":"本次：基礎情境五年年化約 3%，不追。","ruling":"分歧在框架層，事實層沒有爭議。賣方用 12 個月倍數延續，本次用五年終端 30 倍。市場可能錯在倍數體制，把多年 30% 成長當成不會收斂。目標價全距 120 至 231 美元，約 1.9 倍，未大到要再下調信心。","evidence_level":"二手彙整，日期不一","settle_metric":"FY2028E 共識 EPS 上修幅度","if_then":["若 FY2028E 共識 EPS 上修至 3.95 美元以上且股價未同步上漲，則重跑研究。","若股價續漲而共識未上修，則不追。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：加上第四季指引將連七季營收年增低 30 段，美國份額才 14%，費用率還在降；EPS 持續超預期時 79 倍會很快被消化；股價只高於 52 週均線約 10%，RSI 42.76。","side_b":"不買：即使 EPS 年複合 25%，五年年化仍只有約 3%，要年化 10% 須超過多頭路徑。","ruling":"選不買。約束條件是價格，生意本身沒有問題；這個結論在 FY2028E 共識明顯上修時會被推翻。","evidence_level":"事實表與情境樹","settle_metric":"股價、FY2028E 共識 EPS","if_then":["若股價跌到 110 美元以下且固定匯率 GMV 仍高於 27%，則分批反買，首倉 1/3。","若 FY2028E 共識 EPS 達 3.95 美元以上且股價未同步上漲，則重跑研究。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭面：10-K 提到大型對手可能積極定價，平台可能限制資料存取；代理入口是新的競爭層。","side_b":"結構面：Shopify 商家拿走美國增量近半，全球電商仍年增約 7%。其他結構變數：Sezzle 反壟斷案繼續審理，未見 DOJ、FTC 或歐盟調查。","ruling":"雙向拉鋸。份額轉移目前有利 Shopify，代理入口與訴訟是未定的反向力量。","evidence_level":"一手 10-K、法說，訴訟為二手","settle_metric":"美國增量占比、支付滲透率、訴訟里程碑","if_then":["若份額與支付滲透率同時下行，則改判競爭惡化中，持有者減碼至半倉。","若代理訂單放量且支付滲透率續升，則改判結構性轉好中。"],"evidence_refs":["competitive_share_entrants#1","substitute_technology#1","regulatory_antitrust#0"]}],"triggers":[{"n":1,"text":"GMV 成長跌破論點下限","type":"假設驗證","maps_to":"H1","metric":"固定匯率 GMV 年增率","threshold":"連 2 季低於 24%","action":"不追；持有者停止加碼","source_freq":"季報與法說，每季","date":"2027-02"},{"n":2,"text":"貨幣化不再上升","type":"假設驗證","maps_to":"H2","metric":"營收÷GMV、支付滲透率","threshold":"連 2 季年比不再上升，或支付滲透率連 2 季不再上升","action":"停止加碼；持有者標削弱","source_freq":"8-K 與法說，每季","date":"2027-02"},{"n":3,"text":"營運槓桿吸收不了 AI 成本","type":"假設驗證","maps_to":"H3","metric":"FCF 利潤率、毛利金額增速減營業費用增速","threshold":"FY2027 FCF 利潤率低於 18%，或增速差連 2 季低於 5 個百分點","action":"停止加碼；下修基礎情境 EPS 後重算","source_freq":"8-K，每季","date":"2027-05"},{"n":4,"text":"訂閱毛利率持續下滑","type":"風險","maps_to":"R2","metric":"訂閱毛利率","threshold":"連 4 季低於 77%","action":"持有者減碼至半倉","source_freq":"8-K，每季","date":null,"evidence_refs":["geo_supply_chain#0"]},{"n":5,"text":"關稅與消費的衝擊吸收失敗","type":"風險","maps_to":"R3","metric":"北美固定匯率 GMV 年增率、交易與貸款損失占營收","threshold":"北美連 2 季低於 22%，或損失占營收高於 5%","action":"停止加碼；連 4 季成立則減碼至半倉","source_freq":"法說與 10-Q，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":6,"text":"訴訟進入不利階段","type":"風險","maps_to":"R4","metric":"Sezzle 反壟斷案、Briskin 隱私集體訴訟進度","threshold":"集體認證加不利和解，或判賠與和解超過 8 億美元；刑事介入","action":"不利和解則減碼至半倉；刑事介入則清倉","source_freq":"法院文件與 10-Q，事件驅動","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1"]},{"n":7,"text":"代理平台改寫支付經濟","type":"Single Thing","maps_to":"Single Thing","metric":"代理錢包預設、通路抽成、代理訂單支付附著率","threshold":"前三大個人代理之一發生，且 Shopify 揭露支付附著低於網店","action":"持有者減碼至半倉，未持有者取消進場條件","source_freq":"法說、8-K、代理平台條款，事件驅動","date":null,"evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"]},{"n":8,"text":"價格或上修達到進場條件","type":"估值rearm","maps_to":"H1、H2、H3","metric":"股價、FY2028E 共識 EPS","threshold":"股價≤110 美元，或 FY2028E 共識 EPS≥3.95 美元且股價未同步上漲","action":"重跑研究，通過後首倉 1/3","source_freq":"日收盤、共識快照每月","date":null},{"n":9,"text":"股價先漲、證據沒跟上","type":"減碼","maps_to":"估值","metric":"股價÷FY2027E 共識 EPS","threshold":"達 80 倍（約 195 美元）且共識未上修","action":"不追；持有者減碼至半倉","source_freq":"日收盤、共識快照每月","date":null},{"n":10,"text":"成長與貨幣化同時反轉","type":"清倉","maps_to":"H1、H2","metric":"固定匯率 GMV、營收÷GMV","threshold":"GMV 偏離路徑連 3 季達 10%，且營收÷GMV 連 3 季年比下降","action":"清倉","source_freq":"8-K，每季","date":null},{"n":11,"text":"第四季財報複審","type":"複審日期","maps_to":"H3","metric":"FCF 利潤率、毛利金額年增","threshold":"FCF 利潤率與 2025 第四季相當；毛利金額年增高 20% 段","action":"未達則把 150 個基點的結構性說法列為存疑，重跑研究","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"固定匯率 GMV 年增率","bear_threshold":"連 2 季低於 24%","window":"2 季","source":"8-K 與法說","last_status":"ok"},{"metric":"營收÷GMV 年比","bear_threshold":"連 2 季年比不再上升","window":"2 季","source":"8-K，營收與 GMV 自算","last_status":"ok"},{"metric":"支付滲透率","bear_threshold":"連 2 季不再上升","window":"2 季","source":"法說","last_status":"warning"},{"metric":"訂閱毛利率","bear_threshold":"連 4 季低於 77%","window":"4 季","source":"8-K 自算、法說","last_status":"warning"},{"metric":"毛利金額年增減營收年增","bear_threshold":"落後超過 5 個百分點，連 4 季","window":"4 季","source":"8-K 與法說","last_status":"warning"},{"metric":"代理式交易分潤與支付附著","bear_threshold":"揭露向代理平台分潤，或代理訂單支付附著低於網店","window":"12–24 個月","source":"法說、8-K、代理平台條款","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='↑', week26=34.87, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 情境的 EPS 路徑只有總量層級的算術，缺少分部的量乘價，關鍵假設也沒有來源。再看實際報酬：Shopify 自己 2021 年高估值進場後，5 年年化只有約 0%～3.5%，遠低於 Bull 隱含的 +14.8%/年，判斷物沒有交代本案為何不同，所以這個 Bull 依據不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🔴'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價≤110 美元（基礎情境年化約 10%），或 FY2028E 共識 EPS≥3.95 美元且股價未同步上漲；觸發後重跑研究，首倉上限 1/3","exec_line":"目前不追。到價或共識上修後先重跑研究，通過後首倉 1/3，其餘兩段分別等下一季與再下一季財報驗證。"},"reasoning":{"industry":"Q3 FY2026 營收 37.42 億美元，年增 32%。商家解決方案 29.06 億美元，占 77.7%，年增 35%，自算毛利率 38.5%；訂閱解決方案 8.36 億美元，占 22.3%，年增 20%，毛利率 79%（2026-11-03 8-K 與法說）。整體毛利率 47.6%，GAAP 營益率 15.2%，自算非 GAAP 營益率 19.2%。GMV 1,191 億美元，支付滲透率 68%，年增 3 個百分點，所以成長先靠成交量，再靠支付附著。單點依賴有兩處，雲端代管與支付夥伴（FY2025 10-K 風險因子），集中度數字事實表未涵蓋；客戶端沒有集中，沒有單一商家曾超過營收 5%（FY2024 10-K）。供需判斷為結構性持久：Shopify 美國商家線上銷售三年年複合 23%，美國電商整體 8%（2026-11-03 Hoffmeister）。可能看錯的地方是這組數字由公司自行統計，而且商家解決方案會跟著消費循環走。","moat":"機制是統一商務作業系統加 Shop Pay 買家網路：商家換平台要重做線上店、門市、B2B、支付與平均 8 個應用程式的整合，買家端有 4 億名 Shop 與 Shop Pay 使用者。同業 ROIC 事實表未涵蓋，方向改用份額判斷：美國電商份額約 14%，2025 年以來拿走美國增量近半，三年前近五分之一，歐洲份額三年翻倍（2026-11-03 Hoffmeister）。執行面擴大：Lululemon 北美線上店導入 Shop Pay，門店數年增 52%，新導入 POS 的商家有 55% 是 Shopify 新客。定價權穩定：2026-08-05 Finkelstein 說代理式交易沒有新費用，牌價沒有持續上調，訂閱營收年增 20% 低於 GMV。同業利潤率對照不算突出，TTM FCF 利潤率 18.08% 低於 GoDaddy 33.66%。可能看錯的地方是份額數字多為公司自揭，第三方爬蟲資料口徑不一。","growth":"成長以量為主：GMV 年增 29.5%，新商家與同店貢獻各半；價次之，支付滲透率年增 3 個百分點，營收÷GMV 3.14%；併購幾乎沒有，回購事實表未涵蓋。共識 EPS FY2026E 到 FY2028E 年複合 29.5%，營收 FY2027E 年增 26.5%，差距約 3 個百分點來自利潤率擴張。FY2025A 的 0.94 美元是 GAAP，含大額營業外損益，不拿來算三年 CAGR。內生天花板缺投入資本無法驗算，共識與天花板的缺口歸為無法歸因，加註依賴 re-rate，信心上限為中。美國份額由 14% 到 30%，用公司揭露的相對增速（商家 23% 對市場 8%）約 6 年，用前份年增 2 個百分點約 8 年。十項衰退信號只有毛利率年比下滑亮燈：Q3 47.6% 對去年同期自算 48.9%，第四季指引毛利金額增速仍低於營收，來源是支付占比上升，商家解決方案毛利率連三季年增。其餘未亮或無資料：EPS 與營收增速差小於 5 個百分點，FY2025 FCF／淨利 1.63 倍，SBC 占營收 3.9%；產業倍數走勢事實表未涵蓋。反例是 GMV 報表增速為近五季最慢，訂閱營收年增由 22% 降至 20%。","governance":"FY2025 FCF 20.07 億美元，FCF／淨利 1.63 倍，FY2024 為 0.79 倍（事實表 financial_history）；淨利受營業外損益影響，兩年都不適合單獨當轉換率。TTM FCF 利潤率 18.08%。Q3 的 22% 中，CFO 只把約 150 個基點的年增歸為結構性，其餘來自行銷測試、稅款時點與商家預支款會計變更。SBC 及相關稅占營收 3.9%，占 GAAP 營業利益 25.9%。現金流量表 SBC 140 百萬美元年化÷市值 1,915.76 億美元，稀釋約 0.3%／年，實際股數變動事實表未涵蓋。總債務 1.88 億美元，現金 47.27 億美元。現金去向四分、回購均價與債務到期事實表未涵蓋。已知最大的資本動作是 shop.com 約 1 億美元（2026-11-03 RBC 分析師提問所述金額，未見公司揭露），相對現金很小。","valuation":"現價 148.91 美元，FY2026E 本益比 78.79 倍，FY2027E 61.0 倍，EV／FY2026E 營收 12.21 倍。共識 FY2026E 到 FY2028E EPS 年複合 29.5%，PEG 2.67，FY2027E 口徑 2.07，都高於 2。反推：要在現價拿到年化 10%，五年後股價要約 240 美元，以 30 倍算 FY2031E EPS 要 8.0 美元，高於多頭路徑 7.80 美元。連續五年分位事實表未涵蓋，只有年度端點：P/S 分位 55.2，EV/S 分位 52.7；trailing P/E 分位 3.2 只有 3 點，早年獲利極低，不具參考性。共識修正偏平：FY2027E −0.41%，FY2028E −0.63%，FY2026E 近 3 個月 −0.53%。賣方平均目標價 157.58 至 174.57 美元，高於現價 6% 至 17%，全距 120 至 231 美元，來源日期不一，這些是 12 個月倍數延續假設，不反駁五年報酬的計算。動能未過熱：RSI 42.76，26 週報酬 34.87%，4 週漂移事實表未涵蓋。反例：連續超預期時 EPS 可能遠高於共識，FY2028E 上修到 3.95 美元以上，基礎情境年化可回到 8% 左右。","premortem":"價值陷阱風險判中等，依據見反證紀錄：十項衰退信號亮一項。偏多時最可能錯在代理式交易的分潤，偏空時最可能錯在低估 EPS 上修幅度。法說有兩題沒有正面回答：2026-08-05 CIBC 問 FCF 利潤率約 20% 是否新常態，CFO 只指向下季指引；同場 Morgan Stanley 問 Sidekick 對留存與 GMV 的數據，Finkelstein 沒給數字。2026-11-03 只補了開店與轉換指南帶來的 8% 與 3% 提升，留存數字仍缺。歷史最大回撤、空方最強數字事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺商家成交額的抽成：每 100 美元 GMV 收 3.14 美元，78% 營收來自支付等商家解決方案，錢卡在結帳與支付節點。","moat":"護城河仍在變寬（↑）：商家份額持續上升，結帳與 Shop Pay 買家網路把商家和買家綁在同一層，但定價權只算穩定。","growth":"跑道寬（🟢）：美國份額約 14%、全球零售不到 1%，B2B 和線下是已經量化的下一條曲線。","capital":"現金紀律佳但無法完整評分：SBC 稀釋低、淨現金約 45 億美元，回購與併購資料不足。","valuation":"現價要求 EPS 五年年複合 25% 且五年後仍有 30 倍，才換得年化約 3%；我相信生意會成長，不接受這個價格的報酬。","how_wrong":"最可能看錯兩件事：代理式交易把支付經濟分走，以及 79 倍的倍數收斂得比 EPS 複利快。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價≤110 美元，或 FY2028E 共識 EPS 上修到≥3.95 美元且股價未同步上漲。","qc48_result":"fail","qc48_note":"Bull 情境的 EPS 路徑只有總量層級的算術，缺少分部的量乘價，關鍵假設也沒有來源。再看實際報酬：Shopify 自己 2021 年高估值進場後，5 年年化只有約 0%～3.5%，遠低於 Bull 隱含的 +14.8%/年，判斷物沒有交代本案為何不同，所以這個 Bull 依據不成立。","trap":"🟡","val":"🔴","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":148.91,"week26_return_pct":34.87,"consensus_rev_3m_pct":-0.53,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2025 GAAP EPS 受營業外損益扭曲，改用前瞻共識當分母。FY2026E 1.89 美元的口徑事實表未標明，由季度共識量級推斷為調整後；若扣 SBC，倍數更高，不改變結論。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"黑色星期五與網路星期一檔期","impact":"中","watch":"GMV 動能、平台穩定度、Shop Pay 與代理式訂單的揭露。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 FY2027 首季指引，日期未公告","impact":"高","watch":"固定匯率 GMV、毛利金額年增、FCF 利潤率、訂閱毛利率。"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報，日期未公告","impact":"高","watch":"FCF 利潤率年增是否達 100 個基點以上，支付滲透率是否續升。"},{"date":null,"type":"regulatory","event":"Sezzle 反壟斷案與 Briskin 隱私集體訴訟進度，時點事實表未涵蓋","impact":"中","watch":"集體認證、和解金額、對 Shop Pay 綁定的限制。"},{"date":null,"type":"product","event":"個人代理的錢包與分潤條款變動","impact":"高","watch":"代理式訂單的支付附著率，以及是否出現向代理平台分潤。"}],"_projected_from":"v19"}
```
