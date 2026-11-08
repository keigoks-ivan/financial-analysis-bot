你是 stock-analyst v20 的**散文層（prose）agent**，標的 HIMX（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：HIMX　日期：2026-11-08　archetype：None　前份裁決：2026-07-03　觀望｜候選/追蹤池　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1629B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（395B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（999B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1422B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1066B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（841B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（840B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2099B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3223B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3130B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1629           3760-5371      5 條（2–6 內）  
s3                  8000         395           5324-7605      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3487          8059-11513      5 條（2–6 內）  
s6                 11000         841          7111-10159      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         840           1862-2660      5 條（2–6 內）  
s10                 5000        2099           2031-2901      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3130           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4984B；至少需散文≈40.02KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65
−65%
−58%
−55%
−51.44
−40
−40%
−35.4%
−6.1%
−1.9%
0%
0
0.046
0.055
0.06
0.07
0.107
0.11
0.114
0.16
0.2
0.21
0.221
0.25
0.252
0.28
0.3
0.30
0.32
0.40
0.47
0.48
0.504
0.59
0.6
0.70
0.72
0.75
0.80
0.8
0.82
0.83
0.9%
0.9
0.92
1
01
1.2
1.29
1.3
1.30
1.5%
1.5
1.6%
1.69
1.75
1.90
1.9
2
2%
02
2.09
2.34
2.45
2.47
2.56
2.72
2.97
3%
3.0
03
3
3.25%
3.5%
3.6
3.9
4
4%
4.94%
5
5%
05
5.1
5.2%
5.3%
5.5%
6
06
6.53
07
7
7.1
7.1%
7.58
7.7%
08
8%
8
8.0%
8.49
8.8
9.0
09
9
9.1
9.2%
10
10%
10.5
11
11.8
11.9
12
13
13%
13.15
13.3
14
14.0%
14.09
14.4
15
15%
15.4
16.3%
17.4
17.7
18.06
19.0
19
19.03%
19.88%
20%
20
20.0
20.7%
21.4%
21.7%
22%
22.4%
23%
23
24
24.0%
25%
26%
26
26.4%
27%
27
27.9%
28.0%
28.5
28.68
28.7%
28.8%
30.0%
30
30%
30.2
31%
31.07%
31.2%
33%
33.1%
33.3
33.5%
34.2%
35
35%
35.4%
36%
36.1
39.10%
40%
40.43
40.5%
42%
42
43
43.9
43.937
44
44%
45
45.4%
49
50
50%
50.6
51%
51.0
51.44%
51.5
52
57.8
60%
65.8%
69%
70
71.3%
71.6%
73.8%
79.8
80
87
90
93
100
100%
102.8
104
113%
119
119.5
129.3
150
150%
159.8
174.43
174.5
175
176.8
182.6
187.6
190
192.5
199
205
207
213
225
227.5
246.8
250
280
285.3
285.32
351.51
369
400
460
636.83
832
850
861
877
900
947
949.39
970
2022
2023
2025
2026
2027
2028
3034
20261108
1,201
1,230.6
1,300
1,400
1,480.88
1,832.39
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
{"meta":{"ticker":"HIMX","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Himax Technologies, Inc."},"oneliner":"車用顯示驅動龍頭遇上庫存急修正，Q4 營收指引季減兩成多；現價大致只付了本業，CPO 仍待量產驗證，等 2027 年初的訂單與出貨資料再談進場。","thesis":{"H":[{"id":"H1","text":"車用驅動 IC 這次修正是客戶庫存調整，不是需求斷層或份額流失，2027 年營收恢復雙位數成長。","2y":"FY2027 營收至少 947m 美元，Q1 2027 至少 190m，Q2 2027 至少 225m。","5y":null,"10y":null,"threshold":"FY2027 營收與車用 IC 年增都至少 10%","source":"公司季度新聞稿與法說，20-F 客戶揭露","drift_rule":"TTM 營收連 2 季低於路徑至少 5% 視為削弱，連 3 季低於至少 10% 視為反轉"},{"id":"H2","text":"非驅動 IC 占比升到接近 30%，足以抵消 2027 年代工與封測漲價，毛利率守在 33% 以上。","2y":"FY2027 毛利率至少 33%，非驅動 IC 占比至少 27%。","5y":"FY2031 毛利率中樞約 36%，營益率至少 13%。","10y":null,"threshold":"FY2027 毛利率至少 33%，非驅動 IC 占比至少 27%","source":"公司季度新聞稿與法說","drift_rule":"TTM 毛利率連 2 季低於路徑至少 5% 視為削弱，連 3 季低於至少 10% 視為反轉"},{"id":"H3","text":"CPO 的 FAU 光學元件 2027 年進入量產，2028 年成為有份量的第二條成長線。","2y":"2027 全年 CPO 占營收至少 5%，約 50m 美元。","5y":"FY2031 CPO 占營收約 10% 以上，毛利率高於公司平均，第二來源出現後仍守住主要份額。","10y":null,"threshold":"2027 全年至少 5%，2028 全年至少 10%","source":"公司法說、FOCI 公告","drift_rule":"連 4 季低於路徑至少 5% 視為削弱，連 6 季低於至少 10% 或 2027 年底仍未量產視為反轉"}],"R":[{"id":"R1","text":"車用庫存修正超過一季，Q1 2027 續弱；這次中國出口與面板廠拉貨反轉，能見度低。","h_ref":"H1","clock":"⚡","threshold":"Q1 2027 營收低於 175m，或 Q2 2027 低於 205m","evidence_refs":["capital_markets_pricing#0","supply_demand_durability#4"]},{"id":"R2","text":"代工與封測漲價吃掉毛利，台積電縮減成熟製程產能使供給更緊。2023 年全年毛利率 27.9% 是參考底線。","h_ref":"H2","clock":"🔥","threshold":"連 2 季毛利率低於 30%","evidence_refs":["supply_demand_durability#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_inventory_price_position#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#3"]},{"id":"R3","text":"中國本土替代與面板自研，加上客戶與應收集中，主力驅動 IC 的客戶基礎被侵蝕。","h_ref":"H1","clock":"🐢","threshold":"客戶 A 占比不高於 20%，或 FY2027 車用 DDIC 年減","evidence_refs":["competitive_share_entrants#0","customer_second_source#1","substitute_technology#0","substitute_technology#1","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R4","text":"CPO 量產延後，或第二來源攤薄毛利。量產時間由終端客戶決定。","h_ref":"H3","clock":"🔥","threshold":"2027 年底未量產，或 2028 年占比低於 5%","evidence_refs":["substitute_technology#2"]},{"id":"R5","text":"關稅與出口管制衝擊中國客戶與供應鏈，FY2025 大尺寸與中小尺寸驅動 IC 已受關稅不確定性影響。","h_ref":"H1","clock":"🔥","threshold":"主要客戶或供應商列入實體清單，或毛利率季減至少 2 個百分點且公司歸因於關稅","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R6","text":"晶圓代工集中台灣，部分產品單一晶圓廠，更換要數季驗證。來源為 FY2019 與 FY2017 的 20-F，年代較舊，公司 2025 年稱已擴展到中國、韓國與新加坡。","h_ref":"H1","clock":"🐢","threshold":"任一主要代工或封測廠斷供達 1 季","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R7","text":"半導體族群系統性下跌，股價在基本面確認前再受壓。2022 年費半自高點跌約 36%。","h_ref":"H1","clock":"⚡","threshold":"費半自高點回落至少 30%","evidence_refs":["cyclical_prior_downcycle_behavior#1"]}],"single_thing":{"description":"最大客戶（含關係企業，2025 年占營收 24.0%）把主力驅動 IC 大幅轉給本土供應商或自研，全年採購砍半以上。","why_fatal":"這是單一最大敏感度。客戶 A 約 207m 營收（861m 乘 24.0%），砍半少約 104m，以 33.5% 毛利率與 0.82 稅後比推算，每 ADS 少約 0.16 美元，約為基本情境 FY2027 的三分之一；CPO 完全落空在 FY2027 約少 0.07 美元（假設 50% 毛利率）。2025 年底對其應收 57.8m，占 28.8%，也會同時打擊現金。","if_happens":"改用悲觀情境並清倉，不因股價已低而加碼。","how_monitor":"每年 3 月 20-F 的客戶占比與應收集中度，每季法說的車用 DDIC 與 TDDI 季增率，面板廠是否公開導入本土 IC。","probability":"12 至 24 個月約 15%"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":6.53,"peg_fy2":0.06,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":0.252,"FY2026E":0.47,"FY2027E":1.3,"FY2028E":2.45},"fy_end_month":12,"eps_basis":"每 ADS，IFRS 稀釋。FY2025A 由事實表 financial_history.years[3] 淨利 43.937m 除以 174.43m ADS 得 0.252 美元；同列 diluted_eps 0.504 與淨利不符，未採用。FY2026E 至 FY2028E 取 Koyfin 2026-11-07 快照，未隨 Q4 指引調整，分析師家數未載明。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HIMX_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"需求量循環：營收由 FY2022 的 1,201m 連三年降到 FY2025 的 832m，年度毛利率在 27.9% 到 40.5% 之間擺動；不符合商品型的兩項以上條件。CPO 是另外一條未驗證的成長線，不隨循環判讀。"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉：管理層 2026-11-05 稱面板廠在中國十一長假後急砍 Q4 預測；中汽協資料顯示前九月內銷年減 22.4%、出口年增 65.8%，歐盟貿易壁壘與新能源車退稅下調使出口轉弱。","bargaining":{"up":"對晶圓代工與封測弱勢：2027 年漲價已公告，公司把確保產能列為第一優先。","down":"對面板廠議價中等：前十大客戶占 71.3%，部分面板廠可自研；成本由雙方分攤，2026 Q2 起部分調價生效。","geo":"中國總部客戶占 73.8%，供應鏈以台灣為主，同時受出口管制與關稅影響。"},"profit_pool_dir":"事實表未涵蓋五年利潤池序列；方向上車用時序控制與區域調光的利潤占比上升，消費性驅動 IC 下降。","tam_table":{"expanded":false,"reason":"事實表沒有 TAM、SAM、滲透率與利潤池序列。CPO 屬新品類本應展開，但證據包未涵蓋，標為資料缺口。"}},"moat":{"mechanism":"車規認證與長設計週期形成的轉換成本，加上車用時序控制、區域調光與 HUD 去畸變的功能整合；換供應商要在下一個車款重走驗證。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"擴大面：車用時序控制 2026 年預估成長逾 40%，Q4 再季增低雙位數，2026-08-06 Jordan Wu 稱 LTDI 為目前市場獨家供應。縮減面：客戶 A 占比由 28.7%、26.4% 降到 24.0%，FY2025 大尺寸驅動 IC 年減 28.0%、中小尺寸年減 8.0%，20-F 指中國面板廠導入本土 IC 已構成重大挑戰。執行力穩定，定價力穩定偏弱，合併判穩定。","threats":[{"level":"🔴","text":"中國面板廠扶植本土驅動 IC，隸屬面板客戶的對手能更早拿到產品藍圖。2025 年 73.8% 營收來自中國總部客戶，曝險最大。","p":"35%","evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#2"]},{"level":"🟡","text":"數家面板廠具自行設計能力，成功自研就會減少或停止採購。","p":"20%","evidence_refs":["customer_second_source#1","substitute_technology#0"]},{"level":"🟡","text":"產業長期平均售價下滑，前兩大客戶合計逾三成，對客戶 A 的應收占 28.8%，公司曾延長付款條件。","p":"50%","evidence_refs":["substitute_technology#1","customer_concentration_credit#0","customer_concentration_credit#1"]},{"level":"🟡","text":"CPO 光學元件已有對手正面競爭，二手評論指 Largan 切入、FOCI 長期不排除第二來源，管理層也承認長期不會有人獨占。","p":"40%","evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"低利益率×高周轉（投入資本事實表未涵蓋，周轉方向依無晶圓廠模式推定）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"車主用車、車廠與一階供應商定規格、面板廠付款，三環節都成立。每車顯示器與 IC 含量上升較確定，但整車需求正在轉弱，中國內銷前九月年減 22.4%。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一車款的設計案衡量：量產中車款換供應商要重新驗證，轉換成本高；下一車款就可重選，本土供應商有機會切入。重新認證週期的數字事實表未涵蓋。"},{"item":"價值鏈分配","level":"🔴","text":"上游代工與封測已公告 2027 年漲價，台積電也在縮減成熟製程產能；下游前十大客戶占 71.3%，部分具自研能力。Himax 夾在中間，TTM 營益率只有 4.94%，成本只能與客戶分攤。"},{"item":"社會容忍度","level":"🟢","text":"驅動 IC 占整車成本比重低，不是民生必需品定價，沒有社會或監管對漲價的限制；出口管制另列為風險項。"}],"roiic":"FY2022 至 FY2025 營收減少約 369m，營業利益減少約 213m，增量報酬為負，不具外推意義；投入資本明細事實表未涵蓋。","reinvest_rate":"FY2023 至 FY2025 自由現金流（129.3m、102.8m、119.5m）都高於淨利（50.6m、79.8m、43.9m），有形再投資率為負；成長靠費用化研發，折舊與營運資金明細事實表未涵蓋。","endo_ceiling":null,"formula_note":"內生成長率等於增量報酬乘以再投資率；兩項輸入都缺，故不給數字，只判定共識成長遠超任何由歷史再投資能支撐的水準。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","HIMX":31.07,"3034.TW":39.1,"SIMO":50.54,"AMBA":58.52,"LSCC":68.62,"unit":"%"},{"metric":"營業利益率","HIMX":4.94,"3034.TW":19.03,"SIMO":21.3,"AMBA":-14.9,"LSCC":13.05,"unit":"%"},{"metric":"FCF 利潤率","HIMX":3.25,"3034.TW":14.97,"SIMO":-24.9,"AMBA":2.33,"LSCC":24.71,"unit":"%"},{"metric":"研發密度","HIMX":19.88,"3034.TW":17.07,"SIMO":23.7,"AMBA":54.74,"LSCC":30.76,"unit":"%"}],"competitors":[{"name":"3034.TW","gm":39.1,"om":19.03,"fcf_margin":14.97,"rd_intensity":17.07,"strategy_note":"聯詠是最直接的驅動 IC 對手，TTM 營益率高出約 14 個百分點，也正在加壓車用市場。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SIMO","gm":50.54,"om":21.3,"fcf_margin":-24.9,"rd_intensity":23.7,"strategy_note":"儲存控制晶片業者，業務不同，只當無晶圓廠獲利結構參考，不是份額對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"AMBA","gm":58.52,"om":-14.9,"fcf_margin":2.33,"rd_intensity":54.74,"strategy_note":"邊緣 AI 視覺晶片與 WiseEye 部分重疊，高毛利仍虧損，說明邊緣 AI 要有規模才撐得起研發。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"LSCC","gm":68.62,"om":13.05,"fcf_margin":24.71,"rd_intensity":30.76,"strategy_note":"低功耗 FPGA，毛利率與現金流都高，是小型利基晶片的利潤結構參考，不是直接對手。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主，來自車用顯示顆數與單車 IC 含量；價的部分是與客戶分攤代工漲價；併購與回購沒有貢獻。","runway_years":"車用時序控制與 LTDI 的滲透率事實表未涵蓋，不給年數。","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界無法給數字：增量報酬過去四年為負，有形再投資率為負，投入資本與折舊明細事實表未涵蓋。共識成長即使用較高基期 0.504 美元計算也約 69%，判定超過上界。","segments":[{"item":"大尺寸驅動 IC","value":"Q3 19.0m，占 7.7%；Q4 指引季增低雙位數，來自電視與顯示器舊產品出貨。"},{"item":"中小尺寸驅動 IC","value":"Q3 176.8m，占 71.6%；Q4 指引雙位數季減，車用、平板、手機都下滑。"},{"item":"非驅動 IC","value":"Q3 51.0m，占 20.7%；Q4 持平至略降；管理層目標 2027 年占比接近 30%，不含 CPO。"},{"item":"車用時序控制","value":"Tcon 占營收逾 10%，其中車用過半；2026 年預估成長逾 40%，Q4 季增低雙位數。"},{"item":"LTDI","value":"Q4 預期占營收逾 5%，季增個位數。"},{"item":"CPO","value":"工程量產爬坡中，2026 年貢獻有限；管理層稱 2027 年起有實質貢獻，但不給數字。"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 為 33.1% 對去年同期 31.2%，Q3 再升到 34.2%。"},{"item":"核心市占近 12 個月縮減","lit":null,"note":"事實表沒有份額時間序列，客戶 A 占比下滑不等於市占下滑。"},{"item":"提價後銷量下滑","lit":null,"note":"部分調價 Q2 生效，Q4 量縮主因客戶庫存，無法拆分。"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"共識三年 EPS 成長遠高於營收成長，差距超過 5 個百分點。"},{"item":"自由現金流對淨利連 2 年低於 0.75","lit":false,"note":"FY2023 至 FY2025 約為 2.56、1.29、2.72 倍。"},{"item":"員工股權費用占營收高於 5% 且上升","lit":false,"note":"2026 年獎金授予 13.3m，約占全年推算營收 1.5%。"},{"item":"市場萎縮或被替代技術壓縮","lit":false,"note":"車用顯示 IC 含量仍上升；面板廠自研是風險，尚未見營收侵蝕數字。"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數序列。"},{"item":"維持性資本支出占自由現金流高於 60%","lit":false,"note":"Q3 資本支出 3.9m，自由現金流約 20.0m。"},{"item":"停止投資且營收 3 年內下滑","lit":true,"note":"FY2023 至 FY2025 營收連三年下滑；無晶圓廠不適用新產能這一半，保守算亮燈。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"過去 12 個月沒有併購，成長也不靠併購；現金回饋只有年度股利，近三年現金去向明細事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"過去 12 個月沒有併購，唯一重大交易是以約 80m 美元出售約 31% 權益法持股，屬處分。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q3 流通 ADS 174.5m，與上季幾乎相同；近年回購金額與均價事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"2026 年員工獎金授予 13.3m，其中 11.8m 立即既得，約當市值 1,480.88m 的 0.9%，低於每年 1.5%；ADS 數量近季未增。","grade":"過"}]},"valuation":{"basis":"循環修正中的當年度與次年度本益比，並以 FY2022 至 FY2025 平均每 ADS 盈餘約 0.59 美元對照。","tier":"小型無晶圓廠顯示 IC","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或 EV/S；終端倍數本應附同業現值對照，證據包未涵蓋，標為資料缺口。"},"fwd_pe":18.06,"peg":0.16,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"五年分位無法計算，資料只有 4 個年度端點；P/E、P/S、EV/S 都在這 4 點的最高位，但分母偏低，只作為不便宜的提醒。現價約為平均盈餘的 14.4 倍、FY2027 基本情境的 17.7 倍。PEG 0.16 來自偏低基期與未更新的共識，不能當便宜證據；以基本情境三年成長約 15% 計算約 1.2。12 個月機率加權約 8.8 美元（+4%），3 年約 10.5 美元（+23%）。結論為合理。","upside_short_pct":4,"upside_mid_pct":23},"trap_analysis":{"verdict":"🟡","label":"價值陷阱風險中等：衰退訊號亮 2 項，修正深度仍未知。"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY2022 至 FY2025 營收由 1,201m 降到 832m，營益率由 21.4% 降到 5.3%；2025 年 73.8% 營收來自中國總部客戶；20-F 指中國面板廠導入本土 IC 已構成重大挑戰。","assumption":"車用是避風港，份額與毛利守得住。","consequence":"若車用走上消費性驅動 IC 的路，FY2031 每 ADS 盈餘約 0.30 美元，股價約 3.6 美元，虧損近六成。","ruling":"部分採納，悲觀情境機率提高到 35%。這個故事與唯一致命點重疊，最大客戶轉單是第一張骨牌。","watch":"FY2026 20-F 的客戶 A 占比與車用份額，每季車用 DDIC 與 TDDI 季增率。","evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#2","customer_second_source#1","reg_tariff_export#2"]},{"view":"論點成功但股東經濟變差","evidence":"CPO 由 FOCI 出資約 100m 美元擴產，Himax 只供特定光學元件；管理層承認已有對手正面競爭，長期不會有人獨占；代工與封測 2027 年漲價。","assumption":"光學元件的高毛利可持續，本業成本可轉嫁。","consequence":"營收達標但毛利被攤薄，價值由模組廠或客戶取走；代工漲價也吃掉非驅動 IC 占比提升的好處。","ruling":"採納，這是基本情境只給 CPO 小幅貢獻的原因。","watch":"CPO 開始貢獻後全公司毛利率能否站上 35%，第二來源何時出現。","evidence_refs":["substitute_technology#2","cyclical_supply_discipline_capacity#0","cyclical_inventory_price_position#2"]},{"view":"價格已反映太多","evidence":"股價 26 週跌 51.44%，但 TTM 本益比 40.43 倍，P/S 1.69、EV/S 2.09 都在 4 個年度端點的最高位；現價約為 FY2027 基本情境的 17.7 倍。","assumption":"跌深就是便宜。","consequence":"若 FY2027 每 ADS 低於 0.40 美元，現價仍不便宜，還有下跌空間。","ruling":"部分採納，估值結論只給合理，不給便宜；股價下跌不算安全邊際。","watch":"Q4 財報後賣方 FY2027 共識下修的落點。","evidence_refs":["capital_markets_pricing#0","cyclical_prior_downcycle_behavior#1"]}],"max_dd":{"lo":-65,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 13.15 → 本次 8.49（-35.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=13.15","side_b":"本次 price_at_dd=8.49","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 候選/追蹤池 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=候選/追蹤池","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 B→C、估值 🟠→🟡、均線 ✅→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 13.15 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 13.15 美元：Bull 價 27、Bear 價 6，五年期望值 +30.0%，基準年化 5.2%，不對稱比 1.9","side_b":"本次情境、股價仍用 13.15 美元：Bull 價 28.5、Bear 價 3.6，五年期望值 −6.1%，基準年化 −1.9%，不對稱比 0.92","ruling":"先換情境、股價不動：五年期望值少 36.1 個百分點，基準年化少 7.1 個百分點。不對稱比由 1.9 變為 0.92。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 13.15 美元：五年期望值 −6.1%，基準年化 −1.9%，不對稱比 0.92","side_b":"本次情境、股價 8.49 美元：五年期望值 +45.4%，基準年化 7.1%，不對稱比 2.34","ruling":"再換股價、情境不動：起點價下跌 35.4%，五年期望值多 51.5 個百分點，基準年化多 9.0 個百分點，不對稱比由 0.92 升到 2.34。合計五年期望值比前份多 15.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訊號評級與結論","cause":"新證據","prior_field":["signal"],"side_a":"前份訊號評級 B，結論觀望，列在候選名單。","side_b":"本次訊號評級降到 C，結論傾向維持觀望。","ruling":"Q4 營收指引季減 22% 至 26%，車用訂單急修正，短線基本面比前份差；等待條件改成事件，不是價位。","evidence_level":"一手：公司 2026-11-05 新聞稿與法說","settle_metric":"2027 Q1 營收指引","if_then":["若 Q1 指引季增或持平，且車用止跌或 CPO 開始量產出貨：重做研究，首筆不超過 2%","若 Q1 營收低於 175m 且車用續跌：不追，持有者減碼一半"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 13.15 美元，估值偏貴。","side_b":"本次股價 8.49 美元，下跌約 35.4%，估值合理。","ruling":"變動來自股價，不是盈餘上修；基本情境的盈餘路徑其實比賣方低很多。","evidence_level":"事實表股價","settle_metric":"FY2027 共識下修後的本益比","if_then":["若共識下修後 FY2027 本益比高於 20 倍：估值結論轉回偏貴，不追"],"evidence_refs":[]},{"axis":"陷阱風險、護城河方向、成長空間","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"前份陷阱風險中等，護城河方向穩定，五年後成長空間中等。","side_b":"本次三項結論不變，但證據更新：車用時序控制更強、CPO 擴產更具體，同時車用急修正、代工漲價。","ruling":"正反證據相抵，結論不動。","evidence_level":"一手法說與 20-F","settle_metric":"FY2026 20-F 客戶占比與車用份額","if_then":["若車用份額確認下滑：護城河方向改為縮減，不追，持有者清倉"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"研究框架與機率","cause":"方法變動","prior_field":["archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這兩項分類空白，樂觀與悲觀機率各 25%，最大回撤 −55%。","side_b":"本次按需求量循環解讀，判晚循環；樂觀 20%、悲觀 35%，最大回撤範圍 −40% 至 −65%。","ruling":"共識成長超過內生上界，悲觀機率不得低於 30%；車用急修正再支持上調。循環位置按五項訊號多數決，三項偏賣、一項偏買、一項因分母偏低不明；訊號仍有矛盾，所以不給建立部位的姿態。","evidence_level":"方法約束加一手資料","settle_metric":"Q1、Q2 2027 營收與存貨","if_then":["若 Q1、Q2 2027 營收回到 190m、225m 以上：循環位置改判早循環，分批反買"],"evidence_refs":[]},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未載明重啟條件（空值）。","side_b":"2027 年 2 月公布的 Q1 營收指引季增或持平為必要條件，另需車用驅動 IC 止跌或 CPO 量產出貨其一。","ruling":"重啟條件綁事件，因為約束來自論點未決，不是估值。","evidence_level":"判斷","settle_metric":"2027 Q1 營收指引","if_then":["若條件成立：重跑完整研究再建立部位"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未載明減碼與清倉門檻（空值）。","side_b":"毛利率連 2 季低於 30% 就減碼一半；2027 年營收年增低於 5% 且年底 CPO 未量產就清倉。","ruling":"新設門檻，對應本次車用修正、代工漲價與 CPO 三個主要風險。","evidence_level":"判斷","settle_metric":"季度毛利率、年度營收、CPO 量產公告","if_then":["若門檻成立：依表減碼或清倉，不等下一次研究"],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未載唯一致命點（空值）。","side_b":"最大客戶（含關係企業，2025 年占營收 24.0%）把主力驅動 IC 大幅轉給本土供應商或自研，全年採購砍半以上。","ruling":"按每 ADS 盈餘敏感度排序，這項大於 CPO 落空，所以列為唯一致命點。","evidence_level":"20-F 客戶揭露加推算","settle_metric":"FY2026 20-F 客戶 A 占比","if_then":["若發生：改用悲觀情境並清倉"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"三項論點的門檻","cause":"新證據","prior_field":["H1","H2","H3"],"side_a":"前份：FY2026 車用 IC 高於 460m、FY2027 毛利率至少 33%；2026 年光學與 CPO 占比至少 3%，2H26 AR 眼鏡量產或 CPO 進入主要客戶供應鏈；正常化毛利率 31% 至 33%。","side_b":"本次：FY2027 營收至少 947m；FY2027 毛利率至少 33% 且非驅動 IC 至少 27%；2027 年 CPO 占比至少 5%。","ruling":"全年車用約 +10%，僅勉強碰到前份門檻。LCoS 已被 2026-08-06 Jordan Wu 排除在明年量產題材之外，CPO 2026 年貢獻也有限，所以光學路徑改寫成只看 CPO。毛利率已高於前份區間，但 2027 年代工漲價，門檻維持 33%。","evidence_level":"一手法說","settle_metric":"FY2027 營收、毛利率、CPO 占比","if_then":["若三項中兩項未達：基本情境下修，停止加碼"],"evidence_refs":[]},{"axis":"管理層 2027 成長說法與 Q4 跌幅","cause":null,"prior_field":null,"side_a":"2026-11-05 Jordan Wu：Q4 是短期修正，2027 年營收雙位數成長，不含 CPO，前提是全球車輛出貨持平。","side_b":"同場承認訂單能見度受限，客戶急煞車也讓公司意外；要達到 +10%，FY2027 平均季營收要比 Q4 中點高約 26%。","ruling":"可調和，屬程度差異。一次性歸因不採信也不否定，標為未證。基本情境本業只取 +8% 至 +10%。若 Q1、Q2 2027 分別低於 190m、225m，短期修正的說法視為證偽。","evidence_level":"一手法說，未來說法尚未驗證","settle_metric":"Q1、Q2 2027 營收","if_then":["若兩季都達標：H1 維持，分批反買","若兩季都未達：H1 削弱，下修基本情境，停止加碼"],"evidence_refs":["capital_markets_pricing#0","supply_demand_durability#4"]},{"axis":"賣方共識與指引","cause":null,"prior_field":null,"side_a":"賣方 FY2027 每 ADS 1.30 美元、營收 1,230.6m；3 位分析師目標價平均 30.2 美元，低 17.4、高 43。","side_b":"指引推算 FY2026 營收約 861m；不含 CPO 的 2027 年 +10% 約 947m，要到賣方數字 CPO 需貢獻約 280m。","ruling":"採後者。比共識悲觀的原因是成長基準已過時：FY2026 營收共識高於指引約 10%，三年 EPS 近期修正都是 0。利空還沒進模型，所以凍結加碼到第一個確認資料點；目標價高低差 2.47 倍，家數又少，不作依據。","evidence_level":"一手指引對二手彙整","settle_metric":"2027 年 2 月後的共識修正","if_then":["若下修後 FY2027 EPS 仍高於 0.80 美元：上調基本情境，分批反買","若下修到 0.40 美元以下：不追"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-08-06 Jordan Wu：毛利率改善趨勢明年可能延續；Q3 平板 IC 下滑原因是產能限制；CPO 在最保守情境下 2027 年也有實質貢獻。","side_b":"2026-11-05 Karen Tiao 把平板下滑歸因於上半年提前拉貨；Jordan Wu 改說毛利率相對穩定或略為改善，CPO 從明年某個時點開始，量產時間由終端客戶決定。","ruling":"語氣下修，不是方向翻轉。兩次平板歸因可能同時成立，但說明管理層的歸因不穩定，H2 與 H3 只用實際數字驗證。","evidence_level":"逐字稿對照","settle_metric":"FY2027 毛利率與 CPO 量產公告","if_then":["若 2027 年上半年毛利率低於 33%：H2 削弱，停止加碼"],"evidence_refs":["cyclical_supply_discipline_capacity#1"]},{"axis":"CPO 領先與未量產","cause":null,"prior_field":null,"side_a":"管理層稱處於最先進驗證階段，FOCI 通過新台幣 33.3 億元擴產，晶圓級光學路線獨特。","side_b":"尚未正式量產，仍在改善良率，不給營收數字，對手已正面競爭，目前只與 FOCI 合作。","ruling":"可調和。基本情境只放 2027 年約 30m，到 FY2031 約 150m；大幅成功只放在樂觀情境。","evidence_level":"一手說法，二手競爭資訊","settle_metric":"2027 全年 CPO 占營收比重","if_then":["若 2027 年占比至少 5%：樂觀機率上調至 30%，分批反買","若 2027 年底未量產：樂觀機率降到 10%，不追"],"evidence_refs":["substitute_technology#2"]},{"axis":"份額是否流失","cause":null,"prior_field":null,"side_a":"2026-11-05 Jordan Wu：車用成長贏過全球汽車出貨，證明未失份額。","side_b":"20-F 稱本土替代已構成重大挑戰，客戶 A 占比連降，聯詠與新進者加壓車用。","ruling":"不可裁決至 FY2026 20-F 公布。管理層的比較沒有對照同業；客戶 A 下滑也可能來自消費性產品。暫不判份額流失，也不接受份額無虞。","evidence_level":"公司自述對風險揭露，缺份額序列","settle_metric":"FY2026 20-F 車用 DDIC 與 TDDI 份額","if_then":["若車用 DDIC 份額低於 35%：護城河方向改為縮減，不追，持有者清倉"],"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0","customer_second_source#1"]},{"axis":"存貨與應收","cause":null,"prior_field":null,"side_a":"管理層稱存貨健康，理由是產業交期拉長，也需要確保 2027 年產能。","side_b":"存貨 159.8m，季增 5.5%、年增 16.3%，Q4 營收卻要季減約兩成多；粗估存貨天數由約 90 天升到約 119 天。DSO 93 天，一年前 87 天。","ruling":"部分採信，車用客戶確實要求供應穩定，但急修正期存貨有跌價風險，應收又集中在客戶 A。以存貨季增率與營收季增率的差距當領先指標。","evidence_level":"一手數字加推算","settle_metric":"Q4 2026、Q1 2027 存貨與 DSO","if_then":["若兩季差距都大於 10 個百分點：停止加碼"],"evidence_refs":["customer_concentration_credit#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價半年跌 51%，現價大致只付本業；CPO 工程量產中且 FOCI 擴產；車用時序控制 +40%；股息約 3%；約 80m 處分款入帳；賣方最低目標價 17.4 美元。","side_b":"利空不到一週，訂單能見度低，賣方模型還沒改；現價約 FY2027 基本情境的 17.7 倍，週線跌破 52 週與 104 週均線。","ruling":"暫不買。等待成本有限，下一個驗證點在 2027 年 2 月；若論點正確，錯過的幅度可接受，論點錯誤則還有四成以上下跌。","evidence_level":"一手資料加判斷","settle_metric":"2027 Q1 營收指引","if_then":["若股價先漲、Q1 指引未出：不追","若股價跌破 250 週均線 7.58 美元，但 Q1 指引確認止跌：分批反買，首筆不超過 2%","若 Q1 營收低於 175m 且車用續跌：不追"],"evidence_refs":["major_events#0"]},{"axis":"淨負債口徑","cause":null,"prior_field":null,"side_a":"法說只揭露現金及其他金融資產 285.3m。","side_b":"事實表總債務 636.83m（含租賃），淨負債 351.51m，企業價值 1,832.39m。","ruling":"EV 採事實表，但受限資金與債務條件未涵蓋，所以 EV 倍數只作參考，本次估值以本益比為主。","evidence_level":"事實表，明細缺口","settle_metric":"FY2026 20-F 債務與受限資金附註","if_then":["若受限資金能抵銷大部分借款：EV 倍數下修，估值結論不變"],"evidence_refs":[]},{"axis":"每股盈餘資料不一致","cause":null,"prior_field":null,"side_a":"事實表 financial_history.years[3] 的 FY2025 稀釋 EPS 為 0.504 美元。","side_b":"同列淨利 43.937m 除以 174.43m ADS 約 0.252 美元，前三年 EPS 都與淨利除以 ADS 相符。","ruling":"採 0.252 美元，0.504 美元與淨利不符；TTM 本益比 40.43 倍隱含 0.21 美元，也低於最近兩季合計 0.221 美元，因此不作依據。","evidence_level":"事實表內部對照","settle_metric":"20-F 的每 ADS 盈餘","if_then":["若 20-F 確認 0.504 美元：共識成長率改為約 69%，結論不變"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：中國本土替代與面板廠自研加劇，聯詠與新進者加壓車用。","side_b":"結構：車用顯示含量上升，時序控制與 LTDI 領先；其他變數是成熟製程漲價、關稅與出口管制。","ruling":"雙向拉鋸：20-F 指本土替代已是重大挑戰，法說顯示車用時序控制 2026 年成長逾 40%，兩邊都有一手證據。","evidence_level":"一手","settle_metric":"FY2027 車用營收與毛利率","if_then":["若車用成長且毛利率至少 33%：改判結構性轉好中，分批反買","若車用年減且毛利率低於 30%：改判競爭惡化中，清倉"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","reg_tariff_export#0"]}],"triggers":[{"n":1,"text":"Q1 指引與車用或 CPO 同時轉好，才重新研究進場。","type":"估值rearm","maps_to":"H1","metric":"2027 Q1 營收指引季增率","threshold":"不低於 0%，另需車用驅動 IC 止跌或 CPO 量產出貨其一","action":"重跑完整研究，首筆不超過 2%","source_freq":"公司法說，每季","date":"2027-02","evidence_refs":["capital_markets_pricing#0"]},{"n":2,"text":"2027 全年營收驗證短期修正的說法。","type":"假設驗證","maps_to":"H1","metric":"FY2027 營收","threshold":"至少 947m 美元","action":"未達標則下修基本情境，樂觀機率減 5 點，停止加碼","source_freq":"季度新聞稿","date":"2028-02","evidence_refs":["supply_demand_durability#4"]},{"n":3,"text":"毛利率與產品組合驗證能否抵消漲價。","type":"假設驗證","maps_to":"H2","metric":"FY2027 毛利率與非驅動 IC 占比","threshold":"毛利率至少 33%，非驅動 IC 至少 27%","action":"未達標則停止加碼","source_freq":"季度新聞稿","date":"2028-02","evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"CPO 是否真的量產。","type":"假設驗證","maps_to":"H3","metric":"2027 全年 CPO 占營收比重","threshold":"至少 5%，約 50m 美元","action":"達標則樂觀機率上調至 30%；年底未量產則降到 10%","source_freq":"法說與 FOCI 公告","date":"2028-02","evidence_refs":["substitute_technology#2"]},{"n":5,"text":"存貨成長超前營收。","type":"風險","maps_to":"R1","metric":"存貨季增率減營收季增率","threshold":"連 2 季大於 10 個百分點","action":"停止加碼","source_freq":"季度新聞稿","date":"2027-05","evidence_refs":["customer_concentration_credit#1"]},{"n":6,"text":"最大客戶大幅轉單。","type":"Single Thing","maps_to":"R3","metric":"客戶 A 占營收比重與車用 DDIC 年增率","threshold":"FY2026 20-F 客戶 A 不高於 20%，且車用 DDIC 年減","action":"清倉","source_freq":"20-F，每年","date":"2027-03","evidence_refs":["customer_concentration_credit#0","customer_second_source#1","substitute_technology#0"]},{"n":7,"text":"代工漲價轉嫁失敗。","type":"減碼","maps_to":"R2","metric":"GAAP 毛利率","threshold":"連 2 季低於 30%；2023 年 Q2 的 21.7% 含終止代工合約的一次性影響，以全年 27.9% 作底線","action":"減碼一半","source_freq":"季度新聞稿","date":"2027-08","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_inventory_price_position#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#3"]},{"n":8,"text":"本業與 CPO 同時失敗。","type":"清倉","maps_to":"H1","metric":"FY2027 營收年增率與 CPO 量產狀態","threshold":"年增低於 5% 且年底 CPO 未量產","action":"清倉","source_freq":"季度新聞稿與法說","date":"2028-02","evidence_refs":["substitute_technology#2"]},{"n":9,"text":"關稅或出口管制衝擊未能吸收。","type":"風險","maps_to":"R5","metric":"毛利率季變動與管制名單","threshold":"主要客戶或供應商列入實體清單，或毛利率季減至少 2 個百分點且公司歸因於關稅","action":"減碼一半","source_freq":"BIS 公告、法說","date":"2027-05","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"n":10,"text":"連續兩季過關才加到上限。","type":"加碼","maps_to":"H1","metric":"Q2 2027 營收與毛利率","threshold":"營收至少 225m，毛利率至少 33%","action":"分批加到 3% 上限","source_freq":"季度新聞稿","date":"2027-08","evidence_refs":[]},{"n":11,"text":"Q4 財報與 Q1 指引公布後全文複審。","type":"複審日期","maps_to":"H1","metric":"複審","threshold":"2027 年 2 月財報日","action":"依重啟條件決定是否進場","source_freq":"一次性","date":"2027-02","evidence_refs":[]},{"n":12,"text":"半導體族群系統性下跌與供應集中事件。","type":"風險","maps_to":"R6","metric":"費半回檔幅度、主要代工或封測斷供","threshold":"費半自高點回落至少 30%，或斷供達 1 季","action":"停止加碼","source_freq":"市場資料與公司公告","date":"2027-05","evidence_refs":["cyclical_prior_downcycle_behavior#1","geo_supply_chain#0","geo_supply_chain#1"]}],"kill_metrics":[{"metric":"季營收","bear_threshold":"Q1 2027 低於 175m 美元，或 Q2 2027 低於 205m 美元","window":"2027-08 前","source":"公司季度新聞稿","last_status":"warning"},{"metric":"GAAP 毛利率","bear_threshold":"連 2 季低於 30%","window":"未來 4 季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"FY2027 車用 IC 營收年增率","bear_threshold":"低於 +5%","window":"2028-02 前","source":"公司法說","last_status":"unknown"},{"metric":"CPO 占營收比重","bear_threshold":"2027 全年低於 3%，或年底仍未量產","window":"2028-02 前","source":"公司法說與 FOCI 公告","last_status":"unknown"},{"metric":"客戶 A 占營收比重","bear_threshold":"FY2026 不高於 20%，且車用 DDIC 年減","window":"2027-03 的 20-F","source":"20-F Item 4","last_status":"warning"},{"metric":"存貨季增率減營收季增率","bear_threshold":"連 2 季大於 10 個百分點","window":"Q4 2026 與 Q1 2027","source":"公司季度新聞稿","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":"3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟡', moat_trend='→', week26=-51.44, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"2027 年 2 月公布的 Q1 營收指引季增或持平為必要條件，另需車用驅動 IC 止跌或 CPO 量產出貨其一。","exec_line":"條件成立後先重跑完整研究，首筆不超過 2%；Q2 2027 營收至少 225m 且毛利率至少 33% 才加到 3%。股價先漲而資料未到時不追。"},"reasoning":{"industry":"2026 Q3 營收 246.8m 美元：中小尺寸驅動 IC 176.8m（71.6%），非驅動 IC 51.0m（20.7%），大尺寸驅動 IC 19.0m（7.7%）。營益率 9.2% 被 Q3 認列的員工獎金 11.9m 壓低，加回約 14.0%。Q4 指引約 182.6m 至 192.5m，主因面板廠急砍車用驅動 IC 訂單。全年營收推算約 861m（Q1 199m、Q2 約 227.5m、Q3 246.8m、Q4 中點約 187.6m），比 FY2025 的 832m 多約 3.5%。單點依賴屬集中度風險，不是護城河證據：客戶 A 占 2025 年營收 24.0%，前十大 71.3%，中國總部客戶 73.8%。供需耐久性判為週期性將反轉：Q2、Q3 的車用拉貨已經反轉；成熟製程吃緊較持久，但對 Himax 是成本壓力，不是需求順風。產業時鐘判收縮，依據是 10 月車用訂單急修正與中國內銷前九月年減 22.4%，不是股價。","moat":"機制是車規認證週期長，加上面板廠、車廠與一階供應商的雙層關係，換供應商要重走驗證。20-F 稱車用 DDIC 約 40%、TDDI 過半、區域調光 Tcon 更高。同業落差明顯：TTM 毛利率 31.07% 對聯詠 39.10%，營益率 4.94% 對 19.03%，低 14.09 個百分點；事實表只有單期 TTM，無法判斷落差是否收窄。最大客戶占比由 28.7% 降到 24.0%，不能判為擴大。管理層用車用成長贏過全球汽車出貨來論證未失份額，這個比較沒有對照同業，且 Q2、Q3 含客戶超額拉貨，不足以證明份額。CPO 的領先只在工程驗證階段，尚無量產營收。當期 ROIC 無法計算，投入資本明細事實表未涵蓋。","growth":"共識三年 EPS 成長率以 FY2025 每 ADS 0.252 美元為基期、到 FY2028 的 2.45 美元，約 113%；這個數字不能用。基期是低點，FY2026 共識營收 949.39m 比已報三季加 Q4 指引中點約 861m 高約 10%，而三個年度的 EPS 共識近期修正都是 0，代表 Q4 利空尚未反映。缺口主要來自毛利率擴張與 CPO 貢獻，不是歷史再投資能支撐的成長。管理層稱 2027 年雙位數成長且不含 CPO，但要達到 +10%（約 947m），全年平均季營收要比 Q4 指引中點高約 26%。滲透率數字事實表未涵蓋，因此不給年數。","governance":"FY2025 自由現金流 119.5m，淨利 43.9m，2026 年發放股利 44m，約等於 FY2025 全年淨利。TTM 自由現金流利潤率只有 3.25%，以約 877m 營收粗估不到 30m，低於股利所需，因存貨與應收增加；Q3 自由現金流約 20.0m。Q4 預計收到約 80m 的處分款可補足。事實表淨負債 351.51m（總債務 636.83m 含租賃，現金 285.32m），債務到期結構、利率與受限資金事實表未涵蓋，法說只談現金。近三年現金去向四分事實表也未涵蓋。","valuation":"表面 Fwd P/E 18.06 倍的分母有爭議：FY2026 共識 0.47 美元未隨 Q4 指引調整，且公司 Q4 指引不含約 0.11 美元的處分利益。以 Q1 營益率粗估約 0.046 美元，加 Q2 0.114、Q3 0.107、Q4 指引中點 0.055，全年扣除處分利益約 0.32 美元，對應約 26 倍。用基本情境 FY2027 的 0.48 美元計算約 17.7 倍。賣方 FY2027 共識 1.30 美元對應 6.53 倍，但需要 1,230.6m 營收，不採信。TTM 本益比 40.43 倍隱含每 ADS 0.21 美元，低於 Q2、Q3 兩季合計 0.221 美元，顯示分母落後，也不採用。","premortem":"這次利空不到一週，賣方共識還沒動，Q1 2027 才有第一個驗證點。股價 26 週跌 51.44%、RSI 28.68，反映悲觀，但過去的 2022 年費半跌約 36%，本股已跌更深不等於見底。AI 不會取代這些實體晶片，它的影響是搶走成熟製程產能並推高成本。空方最強數字、歷史最大回撤與訴訟金額事實表未涵蓋；20-F 無重大訴訟。"},"plain":{"six":{"how_it_makes_money":"賺面板廠與車用一階供應商的錢，產品是顯示驅動與時序控制晶片，利潤卡在晶圓代工漲價與面板廠議價之間。Q3 毛利率 34.2%、營益率 9.2%，Q4 營收指引季減 22% 至 26%。","moat":"護城河方向穩定，等級偏低：車用時序控制與區域調光的領先在擴大，消費性驅動 IC 與本土替代在侵蝕，兩者相抵。","growth":"五年後成長空間中等：車用時序控制與 LTDI 仍在滲透，CPO 是未經量產驗證的第二曲線，尚不足以判為寬。","capital":"資本配置穩健但沒有創造額外價值：FY2023 至 FY2025 自由現金流都高於淨利，股利幾乎發光全年淨利，稀釋低，沒有併購與明顯回購。","valuation":"現價要求 FY2031 每 ADS 盈餘約 0.9 美元、以 13 倍計價才有年化約一成的報酬，這接近基本情境，價格合理但沒有安全邊際。CPO 若完全落空，本業約 0.70 美元乘 13 倍約 9.1 美元，大致等於現價。","how_wrong":"最可能看錯三處：車用修正持續超過一季、最大客戶轉單、CPO 量產延後或毛利被第二來源攤薄。反方向的錯誤是修正真的只有一季，而 CPO 比預期更快放量。"}},"decision_inputs":{"signal":"C","ma":"🟠","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不等價位，等 2027 年 2 月財報：Q1 營收指引季增或持平，另加車用驅動 IC 止跌或 CPO 量產出貨其一。","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":8.49,"week26_return_pct":-51.44,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026 共識 0.47 美元未隨 Q4 指引調整，可能含也可能不含約 0.11 美元的一次性處分利益；同年度共識營收 949.39m 比指引推算約 861m 高約 10%。便宜論證不採用這個分母。"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"other","event":"出售權益法持股交割，現金約 80m，稅後利益約 19m 至 20m。","impact":"中","watch":"是否如期取得主管機關核准，以及 2027 年股利政策。"},{"date":"2027-01","date_precision":"month","type":"capacity","event":"代工與封測 2027 年漲價生效。","impact":"中","watch":"Q1 毛利率指引與客戶分攤比例。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 Q1 2027 指引。","impact":"高","watch":"Q1 營收指引、車用驅動 IC 訂單、存貨。"},{"date":"2027-03","date_precision":"month","type":"other","event":"FY2026 20-F 公布客戶占比與車用份額。","impact":"中","watch":"客戶 A 占比、應收集中度、車用 DDIC 與 TDDI 份額。"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"CPO FAU 預期進入量產，時間由終端客戶決定。","impact":"高","watch":"量產公告、FOCI 擴產進度、第二來源消息。"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"車用 OLED 預期自下半年放量，智慧眼鏡專案量產。","impact":"中","watch":"非驅動 IC 占比是否接近 30%。"}],"_projected_from":"v19"}
```
