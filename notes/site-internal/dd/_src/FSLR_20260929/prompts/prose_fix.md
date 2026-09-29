你是 stock-analyst v20 的**散文層（prose）agent**，標的 FSLR（2026-09-29）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20260929/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：FSLR　日期：2026-09-29　archetype：None　前份裁決：2026-06-08　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1840B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（954B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1001B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1222B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（955B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（412B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（783B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2192B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4777B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3675B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1840           3612-5160      5 條（2–6 內）  
s3                  8000         954           4932-7046      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3178          8275-11822      5 條（2–6 內）  
s6                 11000         412          7412-10588      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         783           1902-2717      5 條（2–6 內）  
s10                 5000        2192           1966-2808      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3675           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4805B；至少需散文≈40.20KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−49%
−38.0%
−38%
−35
−35%
−6.7%
−6.35
−4.58
−3.6
−3.06
−3
−0.55%
0
0.10
0.11
0.113
0.19%
0.20
0.26
0.28
0.30
0.34
0.35
0.36
0.37
0.38
0.67%
0.8
1
1.15%
1.2
1.5%
1.8
2
2%
02
2.1
2.67%
2.8
3
3%
03
3.1
3.46
3.5
3.9
4
04
4%
4.2
4.5
4.75%
5
5%
05
5.9
06
6
6.25
6.44
7
7%
07
7.4
7.44
7.6
7.75
08
8%
8
8.72%
09
9
9.82
10
10%
10.56
10.95
11
11.4
12
13
14
15%
15
16
17.0
17
17.41
17.5
17.61
18.2
20
20.5
20.9
22.5
23
23.25
24
24%
25
25%
26
26.5
27
27.89%
28%
28
28.0
28.6%
29
29.13
30
30%
31
33.65%
33.7%
34
35
38%
38
40%
41%
41
42
42.5
42.6%
43.4
44.0%
44
45%
45
45.1
46
46%
47.9
48.6%
49
50
50%
50.1
57%
60%
61%
65.5
70
76.5%
86
90
100
100%
122
136
150%
172.97
175
175.48
176
200
201
221
232
250
252
279.01
290
301
315
370
424
529
624
638
653
706
2022
2024
2025
2026
2027
2028
2029
2030
2031
20260929
1,100
1,908
2,034
3,000
6,000
7,600
8,000
8,900
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
{"meta":{"ticker":"FSLR","date":"2026-09-29","schema":"v15.2","contract":"v19","company_name":"First Solar, Inc."},"oneliner":"美國本土最大的薄膜模組廠，靠 45X 抵免與關稅牆賺美國電廠的錢；現價約 7.4 倍 FY2027 共識，市場把盈餘當成會退坡的補貼在打折，關鍵看 232 底價生效後新約單價補不補得上。","thesis":{"H":[{"id":"H1","text":"已簽合約照價兌現，2026–2027 年的盈餘由 backlog 鎖住","2y":"2026 調整後 EBITDA 落在財測 26–28 億美元；2027 年美國新簽單價不低於每瓦 0.34 美元","5y":null,"10y":null,"threshold":"FY2026 調整後 EBITDA ≥26 億美元；第三季 ≥6.25 億美元；美國新簽單價 ≥0.34 美元／瓦","source":"公司 8-K 新聞稿與季度法說（2026-07-30 重申全年財測，並給第三季指引）","drift_rule":"兩年期：TTM 調整後 EBITDA 對財測偏離，連 2 季 ≥5% 算削弱，連 3 季 ≥10% 算反轉"},{"id":"H2","text":"232 底價生效且沒被豁免掏空，2029–2030 年交貨區間的訂單補得回來","2y":null,"5y":"2027 年底前，滾動四季的新簽÷出貨回到 0.8 以上，新約單價不低於現行","10y":null,"threshold":"滾動四季新簽÷出貨 ≥0.8；232 生效後美國新簽單價 ≥0.36 美元／瓦。起點偏低：第三方報導上半年新簽 2.8 GW 對出貨 7.6 GW，約 0.37","source":"232 公告（2026-08-06 宣布、2026-12-04 生效）、公司季度 backlog 與新簽揭露","drift_rule":"五年期：連 4 季偏離 ≥5% 算削弱，連 6 季 ≥10% 算反轉"},{"id":"H3","text":"45X 退坡後，仍能靠技術溢價賺錢：CuRe 加價入帳、鈣鈦礦走向量產","2y":null,"5y":null,"10y":"2031 年後扣除抵免仍有正毛利；鈣鈦礦或疊層產品成為第二條產品線","threshold":"2028 年前技術加價實現 ≥3 億美元（公司稱最多 6 億）；鈣鈦礦 Series 6 規格試產線 2027 上半年就緒；扣除 45X 後毛利率 >0","source":"季度法說、2026-05-13 投資人說明會、10-K 的 45X 揭露","drift_rule":"十年期：跨 2 個年度未達算削弱，跨 3 個年度算反轉"}],"R":[{"id":"R1","text":"backlog 持續淨減：232 定案後，新單仍補不上出貨","h_ref":"H2","clock":"⚡","threshold":"第三、四季美國新簽合計 <3 GW（對照公司說的已簽加待成交約 6 GW）","evidence_refs":["cyclical_inventory_price_position#3"]},{"id":"R2","text":"關稅牆漏水加上本土矽晶放量，美國新約單價守不住","h_ref":"H2","clock":"🔥","threshold":"232 最終版含豁免或配額；或連 2 季美國新簽單價 <0.30 美元／瓦","evidence_refs":["regulatory_antitrust#0","supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#7","end_markets#7","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"]},{"id":"R3","text":"矽晶效率把 CdTe 甩開，鈣鈦礦商業化落後，抵免退坡後沒有技術溢價","h_ref":"H3","clock":"🐢","threshold":"鈣鈦礦試產線延到 2027 年底之後；或 2028 年前 CuRe 技術加價實現 <3 億美元","evidence_refs":["substitute_technology#0","competitive_share_entrants#5","competitive_share_entrants#2"]},{"id":"R4","text":"碲原料受中國出口管制與少數供應商卡脖子","h_ref":"H1","clock":"🔥","threshold":"10-Q 揭露出口許可被拒，或產量因原料受限而下修","evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]},{"id":"R5","text":"客戶集中與交易對手信用：兩家客戶各占模組營收一成以上，部分新約對手付不出現金擔保","h_ref":"H1","clock":"⚡","threshold":"任一主要客戶終止 ≥1 GW 或擔保違約","evidence_refs":["customer_concentration_credit#0"]},{"id":"R6","text":"成本通膨與運費吃掉毛利（管理層自稱最難降成本的時期之一）","h_ref":"H1","clock":"🔥","threshold":"扣除一次性關稅回收後季毛利率 <40%（第二季粗估約 48.6%、TTM 44.0%）","evidence_refs":[]},{"id":"R7","text":"證券集體訴訟：集體期間 2025-02-26 至 2026-02-24，指控公司對關稅因應與產能轉回美國的陳述不實；求償金額事實表未涵蓋","h_ref":null,"clock":"🐢","threshold":"集體認證通過，且出現不利和解","evidence_refs":["major_events#0","lawsuit_class_action#0"]}],"single_thing":{"description":"45X 製造抵免在 2028 年底前被修法削減，或財政部 FEOC 最終規則讓 FSLR 產品拿不到全額抵免","why_fatal":"45X 在 2025 年認列約 16 億美元（第三方彙整），約等於 2026 調整後 EBITDA 財測中值 27 億美元的六成。它是盈餘裡最大的單一敏感項，比任何單價或出貨量的變動都大","if_happens":"清倉；FY2027–2028 的 EPS 路徑直接改用 Bear，終端倍數降到 8 倍以下","how_monitor":"每季 10-Q 的 45X 認列金額與每瓦抵免；財政部 FEOC 最終規則文本；國會稅改法案條文","probability":"12–24 個月內約 10%。現任政府用 232 與 FCC 規定扶植本土製造，方向對 FSLR 有利；但 FEOC 規則還沒定稿，碲的中國依賴是可能被卡的點（這是推論，規則文本事實表未涵蓋）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":7.44,"peg_fy2":0.26,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":17.61,"FY2027E":23.25,"FY2028E":29.13},"fy_end_month":12,"eps_basis":"Koyfin 快照共識 EPS（2026-09-26），財年止於 12 月；FY2025 實際 EPS 事實表未涵蓋，基期留空，共識年增率改用 FY2026→FY2028 兩年計算（約 28.6%）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20260929/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"太陽能製造業，毛利率谷峰擺動逾 20 個百分點（2022 年 2.67%，2025 年約 41%）；近兩年盈餘被合約與 45X 鎖住，循環風險延後到 2029 年後的補單與抵免退坡"},"industry":{"clock_phase":"IV","sd_verdict_source":"全球是結構性過剩：多晶矽產能約 2,034 GW，對比 2026 年裝機預估 638 GW（第三方）。美國是政策造成的短缺：本土含量合規供給至少短缺到 2027（EIA）。美國這邊的供給可逆性高，關稅條款或豁免一改就會回灌","bargaining":{"up":"上游偏強：碲供應集中，中國約占全球精煉量 76.5%，2025 年起實施出口管制；大宗原料與陸運費也在上漲","down":"下游偏弱：本土一體化產能賣到 2028，新約要求現金擔保；但 2025 年有兩家客戶各占模組營收一成以上","geo":"美國政策是雙面刃：232 與 FEOC 在築牆，但 201 已到期，豁免或配額隨時可能開洞"},"profit_pool_dir":"利潤從全球矽晶製造流向美國合規供給，靠政策維持","tam_table":[{"item":"全球模組需求 2026","value":"529–624 GWdc，十餘年來首次年減（2025 年為 653–706 GWdc）"},{"item":"全球模組產能","value":"約 1,100 GW 以上（另一口徑約 1,908 GW）；多晶矽約 2,034 GW，過剩逾 1.2 TW"},{"item":"美國公用級新增容量 2026","value":"計畫 43.4 GW，年增 60%（EIA）"},{"item":"美國本土模組產能","value":"2025 年底 65.5 GW，比 2024 年底的 42.5 GW 多五成以上；本土電池產能多數要到 2026 年底才放量"},{"item":"FSLR 出貨與份額","value":"2025 年 17.5 GW，約占全球 2%；2026 財測 17.0–18.2 GW；占全球薄膜市場約 45%"},{"item":"利潤池方向","value":"流向美國合規製造：FSLR 淨利高於中國四大廠合計（第三方）；同業 TTM 營益率 CSIQ −0.55%、JKS −6.7%；五年前的對照序列事實表未涵蓋"}]},"moat":{"mechanism":"非多晶矽技術路線＋美國本土規模製造→同時取得本土含量資格與 45X 抵免，並避開矽晶進口面對的關稅與 FEOC 限制；多年期合約附技術加價條款","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"擴大面：新簽單價由 0.34–0.35 升到 0.36 美元／瓦，本土產能賣到 2028，232 新增底價。縮減面：backlog 由 50.1 降到 45.1 GW，美國矽晶電池產能 2026 下半年投產，201 條款到期。兩邊互相抵銷，判穩定","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用 TTM 營業利益率差距當代理；差距是擴大還是收窄需要兩年以上序列，事實表未涵蓋","threats":[{"level":"🔴","text":"關稅牆漏水：201 條款 2026 年 2 月到期；232 若附豁免或配額，全球過剩的矽晶會以每瓦 0.10–0.11 美元回灌美國，新約單價守不住（生態攻擊）","p":25,"evidence_refs":["regulatory_antitrust#0","supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#7","end_markets#7","cyclical_supply_discipline_capacity#1"]},{"level":"🟡","text":"美國本土矽晶電池放量：Qcells 3.5 GW 電池線 2026 第三季滿產，T1 的 2.1 GW 電池廠第四季投產。本土含量不再只有 FSLR 能給；屬點對點競爭，2028 年後補單時開始壓價","p":50,"evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"]},{"level":"🔴","text":"技術差距：矽晶效率上升、成本下降，CdTe 的差距可能大到抵免補不回；FSLR 全球份額約 2%，規模遠小於中國龍頭，鈣鈦礦仍在試產階段","p":30,"evidence_refs":["substitute_technology#0","competitive_share_entrants#5","competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉（TTM 營益率 33.65%；周轉率事實表未涵蓋，依重資產製造推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者三方都成立：開發商決定用誰的模組，電力公司與雲端巨頭透過購電合約付錢；近期約 5 GW 大案中有一半直接綁 Google。EIA 預估 2026 年美國公用級太陽能新增 43.4 GW，年增 60%。電是需要不是想要，延後的代價高"},{"item":"決策層級","level":"🟡","text":"替代性要在單一專案層級看：45 GW backlog 裡約 41 GW 帶本土含量條件，加上 FEOC 與安全港規定讓開發商寧可保守，現在換不掉 FSLR。但 Qcells、T1 美國電池廠 2026 下半年起投產後，本土含量不再只有 FSLR 能給。代理變數：多年期合約、附現金擔保、技術加價條款"},{"item":"價值鏈分配","level":"🟡","text":"全球價值鏈嚴重過剩，矽晶同業普遍虧損（CSIQ 營益率 −0.55%、JKS −6.7%）。FSLR 賺錢是因為關稅與抵免把它放在美國合規供給這個卡口。上游碲原料集中，中國約占全球精煉 76.5%，供應商少、換供應商要長期認證；運費與大宗原料漲價被上游與物流吃走一部分"},{"item":"社會容忍度","level":"🟡","text":"獲利依賴兩個政策授權：45X 抵免（稅法）與關稅牆（行政措施，可加豁免或配額）。Bradley 2026-07-30 自己舉例，201 條款的雙面模組豁免就曾把保護掏空。現任政府方向有利（232、FCC 逆變器規定），但關稅推高電廠成本、抵免由納稅人買單，政治上限低於經濟上限"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋；毛估 2026 資本支出財測 8–10 億美元，約是調整後 EBITDA 財測 26–28 億美元的三成（未扣折舊與營運資金）","endo_ceiling":null,"formula_note":"當期 ROIC＝稅後營益率×投入資本周轉率。投入資本與折舊不在事實表，當期與增量 ROIC 都算不出來，內生成長上界因此留空；情境樹保守處理，一律視為共識成長超出內生上界"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","FSLR":44.02,"CSIQ":16.43,"JKS":4.75,"ENPH":46.95,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","FSLR":33.65,"CSIQ":-0.55,"JKS":-6.7,"ENPH":8.72,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","FSLR":27.89,"CSIQ":-31.42,"JKS":null,"ENPH":11.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","FSLR":5.02,"CSIQ":1.67,"JKS":1.64,"ENPH":13.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"CSIQ","gm":16.43,"om":-0.55,"fcf_margin":-31.42,"rd_intensity":1.67,"strategy_note":"矽晶一體化大廠，TTM 營益率與自由現金流率都是負的；在價格戰裡自顧不暇，短期打不動 FSLR 的合規單價","period":"TTM ending 2026-06-30（4季加總）"},{"name":"JKS","gm":4.75,"om":-6.7,"fcf_margin":null,"rd_intensity":1.64,"strategy_note":"全球出貨龍頭之一（2025 年約 86 GW），TTM 毛利率只剩 4.75%；對 FSLR 的威脅在於關稅牆一漏就能用全球價回灌","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ENPH","gm":46.95,"om":8.72,"fcf_margin":11.49,"rd_intensity":13.85,"strategy_note":"做微型逆變器，不是模組同業；毛利率接近 FSLR，營益率卻只有 8.72%，說明高毛利本身不是護城河，能不能留住才是","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（美國新廠爬坡、南卡後段線）＋價（CuRe 技術加價、232 底價）；無併購、無回購","runway_years":"美國市占與滲透率事實表未涵蓋；以合約可見度計，本土產能已賣到 2028，約 2–3 年高能見度","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板算不出來：增量 ROIC 與再投資率要用的投入資本、折舊、營運資金都不在事實表。共識 FY2026→FY2028 EPS 年增約 28.6%，主要來自 45X 認列量增加、CuRe 技術加價（最多 6 億美元，多數在 2027–2028）與美國產能爬坡，不是再投資報酬","segments":{"expanded":false,"reason":"分部營收與毛利事實表未涵蓋；可得的只有美國與印度新簽單價（0.36 對 0.20 美元／瓦），印度量增會拉低平均單價，已寫進反證紀錄"},"decay_signals":["亮：EPS 成長遠快於營收。第二季營收年減約 4%、淨利年增約 24%；共識 FY2026→FY2028 EPS 年增 28.6%，靠的是抵免與技術加價，不是量","亮：自身估值倍數系統性下移。P/E、P/S、EV/S 都落在自身年底值的最低點","未亮：毛利率沒有連兩季年減，第一季年增約 6 個百分點、第二季年增約 12 個百分點","未亮：SBC 只占營收 0.67%","資料缺口：FCF／淨利連兩年、維護性資本支出占比、美國市占，事實表未涵蓋","觀察中：矽晶效率差距擴大屬長期風險，尚未反映在新簽單價"],"trap_rating":"🟡（亮 2 項）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；法說列的現金用途是營運資金準備、擴產與技術研發，股息與回購紀錄事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年沒有實質併購（Bradley 2026-07-30：過去十年併購做得不多），沒有已實現報酬可算","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"法說列的現金用途不含回購；回購紀錄事實表未涵蓋","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"第二季股權薪酬約占營收 0.67%，以市銷率 3.46 倍換算約占市值 0.19%／年，低於 1.5% 門檻","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY1 共識）加自身 P/S 區間；循環商品子型本應看 P/B，但帳面價值事實表未涵蓋","tier":"低倍數、政策依賴的製造股","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率、沒有倍數；矽晶同業 TTM 營益率為負，本益比沒有意義；終端倍數以自身前瞻 9.82 倍為錨"},"fwd_pe":9.82,"peg":0.34,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比 9.82 倍，FY2027 約 7.4 倍，FY2028 約 5.9 倍。P/E（3 個年底點）、P/S 與 EV/S（4 個年底點）都在自身最低；五年連續分位事實表未涵蓋。PEG 約 0.34。便宜是成立的，但有一部分是補貼盈餘本來就該打的折，所以終端倍數只給 11 倍，不是回到前份設想的 16 倍","upside_short_pct":28,"upside_mid_pct":46},"trap_analysis":{"verdict":"🟡","label":"政策高峰盈餘下的低本益比"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"股價從前份判斷日的 279.01 美元跌到 172.97 美元，約 −38%；同期 FY2026 共識 EPS 反而從 17.41 上修到 17.61。GLJ 在 9 月把目標價從 315 砍到 250。證據包沒有解釋這波殺估值的原因","assumption":"殺估值反映的是市場對 2029 年後補貼退坡的折現，不是某條我們沒看到的具體利空","consequence":"如果市場在定價某條已知的規則草案，Bear 機率就被低估了，7.4 倍的便宜會是陷阱","ruling":"部分採納：Bear 機率取 30%（高於一般的 25%），第三季財報前不建倉；不把「已經跌很多」當成安全邊際。這一條和唯一致命點部分重疊（FEOC 規則），已由清倉條件覆蓋","watch":"財政部 FEOC 最終規則文本、每季 45X 認列額、賣方目標價下修是否擴散","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_price_at_dd","f_consensus_rev_3m_fy1_pct"]},{"view":"論點失敗","evidence":"backlog 從 2025 年底的 50.1 GW 降到 2026 年 6 月底的 45.1 GW。第三方報導上半年新簽約 2.8 GW，取消比新單多。部分交易對手付不出現金擔保。201 條款 2026 年 2 月到期。Qcells 與 T1 的美國電池產能 2026 下半年陸續投產","assumption":"訂單放緩是公司為了等 232 定案而主動挑單","consequence":"如果其實是需求轉向本土矽晶，2029–2030 年的產能會賣不出去，單價也守不住","ruling":"暫時不可裁決，裁決點是第三季財報（2026 年 10 月）。目前偏向公司說法，因為新簽單價從 0.34–0.35 升到 0.36 美元／瓦；需求真的轉弱時，通常會先看到降價","watch":"第三季美國新簽 GW 數、單價、季末 backlog","evidence_refs":["cyclical_inventory_price_position#3","regulatory_antitrust#0","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"],"fact_refs":["f_kpi6_contracted_sales_backlog"]},{"view":"論點失敗","evidence":"矽晶效率持續上升、成本下降，CdTe 的差距可能大到抵免也補不回。FSLR 全球份額約 2%，規模遠小於中國龍頭。鈣鈦礦還在試產線階段","assumption":"CuRe 與鈣鈦礦能維持終身發電量優勢（公司稱 CuRe 終身發電量最多高 8%）","consequence":"45X 退坡後沒有技術溢價，FSLR 回到商品模組的定價","ruling":"採納為長期風險，放進第三個假設與第三個風險；終端倍數不給技術溢價","watch":"鈣鈦礦 Series 6 規格試產線是否在 2027 上半年就緒；CuRe 技術加價實際入帳金額","evidence_refs":["substitute_technology#0","competitive_share_entrants#5","competitive_share_entrants#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"法說承認現在是「最難降成本的時期之一」：鋼、鋁、銅、電價都在漲，陸運到美國西岸的成本已經和從亞洲海運差不多。東南亞產能閒置，每季約 3,000 萬美元。上半年營運現金流 −3.6 億、資本支出 2.8 億。印度新簽只有 0.20 美元／瓦。公司說對科技相關併購更開放；不發股息也不回購","assumption":"美國單價上漲能蓋過成本通膨，現金最後回到股東手上","consequence":"就算 232 和需求都對，每股盈餘成長也會被成本與低價的印度量稀釋，現金被鈣鈦礦與併購吃掉","ruling":"部分採納：Base 情境 FY2027／2028 EPS 比共識低 3%／7%；任何超過市值 5% 的併購列為重大事件，重新判斷","watch":"扣除一次性關稅回收後的毛利率、併購公告、年底淨現金是否落在財測 17–23 億美元","evidence_refs":["end_markets#3"],"fact_refs":["f_kpi3_fcf","f_kpi5_fy2026_guidance_q2"]},{"view":"價格已反映太多","evidence":"前瞻本益比 9.82 倍看起來便宜，但分母裡 45X 抵免粗估約占六成（2025 年認列約 16 億美元，對比 2026 調整後 EBITDA 財測中值 27 億美元）。第二季毛利率 57% 還含約 8,900 萬美元一次性 IEEPA 關稅回收，扣除後約 48.6%","assumption":"45X 至 2029 年仍是全額（依前份判斷記載的階梯，2030 年起遞減；本包未附條文），五年內盈餘大半還在","consequence":"如果改用扣除抵免後的本業盈餘當分母，現價並不便宜","ruling":"部分反駁：五年持有期內盈餘大半落在全額抵免期，前瞻倍數仍可用。但終端倍數只給 11 倍、Bear 給 8 倍，把退坡算進終值","watch":"每季 45X 認列額與每瓦抵免金額","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_kpi1_non_gaap_adjusted_ebitda","f_kpi5_fy2026_guidance_q2"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 279.01 → 本次 172.97（-38.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=279.01","side_b":"本次 price_at_dd=172.97","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷","cause":null,"prior_field":null,"side_a":"公司、EIA 與第三方看法一致：美國本土含量合規模組至少短缺到 2027；公司本土一體化產能已賣到 2028","side_b":null,"ruling":"這是前兩年盈餘的地基，不列為爭點","evidence_level":"公司揭露＋EIA","settle_metric":null,"if_then":[],"evidence_refs":["end_markets#5"]},{"axis":"前份漂移：訊號與估值","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-06-08，279.01 美元）：訊號 B，估值偏便宜，FY2027 本益比約 12 倍","side_b":"本次（172.97 美元）：FY2027 本益比約 7.4 倍、前瞻 9.82 倍，估值仍判便宜；訊號維持 B，因為變得更便宜，被跌破 250 週均線抵銷","ruling":"估值與訊號結論不變。變的是價格，不是基本面：FY2026 共識反而上修 1.15%","evidence_level":"事實表價格與共識快照","settle_metric":"週收盤是否站回 250 週均線（175.48 美元）","if_then":["若第三季財報新簽 ≥2 GW，且週收盤站回 250 週均線→重跑判斷後建首倉","若股價再跌 15%，共識不動、也沒有新利空→分批反買，不停損"],"evidence_refs":[]},{"axis":"前份漂移：新框架補齊的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","asym_ratio","ev5y_pct","irr_base_pct","max_dd_pct","bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct","rearm_trigger"],"side_a":"前份這些欄位都是空的：沒建情境樹，沒判循環位置、護城河方向與公司類型，也沒設重啟條件","side_b":"本次依新框架補齊：護城河方向持平、五年後跑道中等、公司類型歸循環/商品、循環位置中循環、情境機率牛 25／基準 45／熊 30、最大回撤區間 −35%～−55%、重啟條件見行動條件；DCA 欄位本輪不適用","ruling":"這是方法補齊，不代表前份判斷改變","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份陷阱風險 🟡","side_b":"本次仍是 🟡，亮兩項：EPS 成長遠快於營收、自身倍數系統性下移。新的負面證據（backlog 淨減、集體訴訟、碲出口管制）和新的正面證據（232 底價宣布、新簽單價上升）互相抵銷","ruling":"維持 🟡","evidence_level":"公司揭露＋第三方報導","settle_metric":"第三季新簽與 backlog","if_then":[],"evidence_refs":["cyclical_inventory_price_position#3","lawsuit_class_action#0","reg_tariff_export#0"]},{"axis":"行動門檻：減碼與清倉","cause":"方法變動","prior_field":["kill_metrics","triggers"],"side_a":"前份沒設清倉與減碼指標。風險欄有兩條：EPS 共識連 2 季再下修、累計逾 10% → 減倉；連 2 季美國 ASP <0.30 美元／瓦且 backlog 淨流出（需 ≥50% 機率才砍倉）","side_b":"本次：兩條舊門檻都保留，改成明確的減碼條件。FY2027 共識 <20.9 → 減碼一半；連 2 季新簽 <0.30 美元／瓦且 backlog 淨減 → 減碼一半。另新增：backlog <38 GW 且單季新簽 <1 GW → 減碼一半；45X 被削減 → 清倉","ruling":"舊門檻沒有刪，只是把「減倉」落成具體比例；新增的清倉條件對應唯一致命點","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份沒設 Single Thing（空白）；45X 法案存續是放在第一個假設裡當二元事件","side_b":"本次 Single Thing：45X 製造抵免在 2028 年底前被修法削減，或 FEOC 最終規則讓 FSLR 產品拿不到全額抵免；一旦發生就清倉","ruling":"45X 是盈餘裡最大的單一敏感項，所以從假設升格為唯一致命點","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份第三個論點：倍數修復","cause":"價格變動","prior_field":["thesis.H3"],"side_a":"前份：FY2027 本益比從 12 倍修復到 16 倍，中期目標 370 美元；反轉條件是共識下修逾一成或政策利空","side_b":"實際：FY2027 本益比壓到約 7.4 倍，共識卻沒下修（FY2026 上修 1.15%、FY2027 持平）；殺估值的原因證據包未涵蓋","ruling":"前份第三個論點視為反轉並退休，不再拿倍數修復當論點；新論點改看訂單補位與技術溢價","evidence_level":"事實表價格＋共識快照","settle_metric":"共識是否開始下修","if_then":["若之後共識下修逾一成→確認殺估值有基本面根據，減碼一半","若共識持續持平、第三季新簽達標→殺估值屬情緒，依重啟條件建倉"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"前份第三個風險：backlog 淨流出","cause":"新證據","prior_field":["thesis.R3"],"side_a":"前份警戒：連 2 季美國 ASP <0.30 美元／瓦，且 backlog 淨流出","side_b":"backlog 已連兩季淨減（50.1→47.9→45.1 GW），但美國新簽單價升到 0.36 美元／瓦，只滿足一半條件，沒有觸發。前份第二個假設的 47.9 GW 兌現基準，也因正常出貨與新單偏少降到 45.1 GW","ruling":"未觸發；條件保留為減碼門檻","evidence_level":"公司新聞稿＋第三方報導","settle_metric":"第三季美國新簽單價與季末 backlog","if_then":[],"evidence_refs":["cyclical_inventory_price_position#3"]},{"axis":"訂單放緩：主動挑單還是需求轉弱","cause":null,"prior_field":null,"side_a":"公司（2026-07-30 法說，Widmar 與 Bradley）：優先顧價格與合約品質，等 232 定案；7 月單月美國新簽近 2 GW，另有逾 2 GW 等條件成交，還有 2 GW 高機率在年底前成交","side_b":"第三方：上半年新簽 2.8 GW，遠低於出貨，取消比新單多；部分交易對手付不出現金擔保","ruling":"性質是不可調和（方向相反）。選公司這邊，依據是新簽單價從 0.34–0.35 升到 0.36 美元／瓦；需求轉弱時，單價通常會先鬆。但這個裁決只到第三季財報為止","evidence_level":"公司揭露的單價，對上第三方報導（取消量沒有公司原文證實；該報導的單季出貨數字與公司第三季 3.9–4.5 GW 財測量級不合，較可能是上半年合計）","settle_metric":"第三季美國新簽 GW 數與單價、季末 backlog","if_then":["若第三季新簽 ≥2 GW 且單價 ≥0.34 美元／瓦→採公司說法；重啟條件成立後建首倉，上限 3%","反向：若第三、四季美國新簽合計 <3 GW，或單價 <0.30 美元／瓦→採第三方說法；已持有就減碼一半，未持有就放棄建倉"],"evidence_refs":["cyclical_inventory_price_position#3","customer_concentration_credit#0"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"2026-05-13 投資人說明會（Bradley）：南卡後段線照 2026 第四季排程。2026-04-30（Bradley）：財測不假設 122 條款到期後的成品關稅。2026-04-30（Widmar）：對 232 時程不給信心程度","side_b":"2026-07-30（Widmar）：第一期仍在 2026 下半年，第二期延到 2027 年中，理由是提早導入 CuRe。同場（Bradley）：財測改為假設下半年有 301 條款關稅，淨關稅影響 6,000–8,000 萬美元，全年財測不變。同場（Widmar）：仍無法給 232 時程信心程度；232 後來在 8 月 6 日宣布","ruling":"第二期延後有技術理由，只影響 3.5 GW 後段產能的一部分，採信。關稅假設改口屬外部政策變動，財測不變代表已吸收。232 時程兩度不給答案，標為「未證、監測」，不扣護城河分數","evidence_level":"逐字稿（場次日期與講者如上）","settle_metric":"南卡第一期是否在 2026 年底前投產","if_then":["若第一期延到 2027→執行分數扣 1，停止加碼","若如期投產→維持"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買的理由：FY2027 本益比約 7.4 倍、前瞻 9.82 倍，是自身歷年最低；本土一體化產能賣到 2028；232 最低進口價每瓦 0.38 美元，高於公司現行新簽的 0.36 美元，退坡期有漲價空間；淨現金約 17 億美元；KeyBanc 以估值理由升評；FY2026 共識三個月上修 1.15%","side_b":"等的理由：股價剛跌破 250 週均線；232 生效後的新約價格還沒出現；FEOC 最終規則還沒定稿；backlog 仍在淨減","ruling":"等第三季財報與均線，兩個條件都成立再建倉。等的代價是少賺一段；買錯的代價是買進補貼退坡的價值陷阱","evidence_level":"事實表＋公司揭露＋第三方報導","settle_metric":"第三季新簽與 250 週均線","if_then":["若第三季新簽與均線條件都成立→重跑判斷後建首倉","若股價先漲回 200 美元以上，但新簽沒達標→不追"],"evidence_refs":["reg_tariff_export#0"]}],"triggers":[{"n":1,"text":"第三季財報：調整後 EBITDA 對照 6.25–7.75 億美元的財測","type":"假設驗證","maps_to":"H1","metric":"第三季調整後 EBITDA","threshold":"≥6.25 億美元","action":"低於下緣→暫停任何建倉，重新檢查第一個假設","source_freq":"季報（每季）","date":"2026-10"},{"n":2,"text":"訂單補位：第三季美國新簽與季末 backlog","type":"假設驗證","maps_to":"H2","metric":"美國新簽 GW 數與單價、季末 backlog","threshold":"新簽 ≥2 GW、單價 ≥0.34 美元／瓦、backlog ≥44 GW","action":"成立且站回 250 週均線→重跑判斷後建首倉","source_freq":"季報（每季）","date":"2026-10","evidence_refs":["cyclical_inventory_price_position#3"]},{"n":3,"text":"232 最終版本：12 月 4 日生效時有沒有豁免或配額","type":"風險","maps_to":"R2","metric":"232 生效條文","threshold":"出現豁免或配額，涵蓋美國本土電池以外的進口","action":"已持有就減碼一半；未持有就延後建倉一季","source_freq":"聯邦公告（一次性）","date":"2026-12","evidence_refs":["regulatory_antitrust#0"]},{"n":4,"text":"45X 抵免被修法削減，或 FEOC 最終規則讓 FSLR 拿不到全額抵免","type":"Single Thing","maps_to":"single_thing","metric":"45X 條文、FEOC 最終規則、10-Q 的 45X 認列額","threshold":"可領額度確定減少","action":"清倉","source_freq":"聯邦公報與國會法案（隨時）＋每季 10-Q","date":null},{"n":5,"text":"美國新簽單價跌破每瓦 0.30 美元，且 backlog 淨減","type":"減碼","maps_to":"R2","metric":"美國新簽單價、季末 backlog","threshold":"連 2 季同時成立","action":"減碼一半","source_freq":"季報（每季）","date":null,"evidence_refs":["cyclical_inventory_price_position#3"]},{"n":6,"text":"FY2027 共識 EPS 累計下修超過一成","type":"減碼","maps_to":"H1","metric":"FY2027 共識 EPS（現在 23.25）","threshold":"<20.9","action":"減碼一半","source_freq":"共識快照（每月）","date":null,"evidence_refs":["capital_markets_pricing#0"]},{"n":7,"text":"碲供應：中國出口許可被拒，或供應商中斷","type":"風險","maps_to":"R4","metric":"10-Q 風險揭露、產量","threshold":"揭露許可被拒，或產量因原料受限而下修","action":"減碼一半","source_freq":"每季 10-Q","date":null,"evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]},{"n":8,"text":"大客戶與交易對手：占營收一成以上的客戶終止或延後合約","type":"風險","maps_to":"R5","metric":"10-Q 客戶集中與合約終止揭露","threshold":"任一主要客戶終止 ≥1 GW，或擔保違約","action":"停止加碼","source_freq":"每季 10-Q","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":9,"text":"證券集體訴訟的程序進度","type":"風險","maps_to":"R7","metric":"訴訟里程碑與和解金額","threshold":"集體認證通過，且出現不利和解","action":"減碼一半","source_freq":"法院文件與 10-Q","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":10,"text":"成本通膨吃掉毛利","type":"風險","maps_to":"R6","metric":"扣除一次性關稅回收後的季毛利率","threshold":"<40%","action":"停止加碼；連 2 季就減碼","source_freq":"季報（每季）","date":null},{"n":11,"text":"首倉條件：第三季新簽達標，且股價站回 250 週均線","type":"估值rearm","maps_to":"rearm_trigger","metric":"第三季美國新簽、週收盤對 250 週均線","threshold":"新簽 ≥2 GW、單價 ≥0.34 美元／瓦，且週收盤 >250 週均線","action":"重跑判斷後建首倉，上限 3%，分兩批","source_freq":"季報＋週線","date":"2026-10"},{"n":12,"text":"232 生效後第一季的新約價格","type":"加碼","maps_to":"H2","metric":"美國新簽單價與 GW 數","threshold":"單價 ≥0.38 美元／瓦，且新簽 ≥3 GW","action":"加碼第二批，到單檔上限","source_freq":"季報（每季）","date":"2027-02"},{"n":13,"text":"鈣鈦礦 Series 6 規格試產線是否就緒","type":"假設驗證","maps_to":"H3","metric":"法說揭露的進度","threshold":"2027 上半年就緒","action":"延後→第三個假設削弱，終端倍數不再給任何溢價","source_freq":"季報（每季）","date":"2027-06"},{"n":14,"text":"第四季財報與 2027 年財測公布後全面複審","type":"複審日期","maps_to":null,"metric":"2027 年營收與調整後 EBITDA 財測","threshold":"財測中值是否高於 2026","action":"重跑判斷","source_freq":"年報","date":"2027-03"}],"kill_metrics":[{"metric":"美國新簽單價（含技術加價）","bear_threshold":"連 2 季 <0.30 美元／瓦且季末 backlog 淨減→減碼一半","window":"滾動 2 季","source":"公司季度新聞稿與法說","last_status":"warning"},{"metric":"季末合約 backlog 與單季美國新簽","bear_threshold":"backlog <38 GW 且單季美國新簽 <1 GW→減碼一半","window":"2027 年底前逐季","source":"公司 8-K 新聞稿","last_status":"ok"},{"metric":"FY2027 共識 EPS（現在 23.25）","bear_threshold":"累計下修逾 10%（<20.9）→減碼一半","window":"任兩季內","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"45X 製造抵免資格與額度","bear_threshold":"修法或 FEOC 最終規則削減 FSLR 可領額度→清倉","window":"2028 年底前","source":"聯邦公報、國會法案、10-Q 的 45X 認列額","last_status":"unknown"},{"metric":"扣除一次性關稅回收後的季毛利率","bear_threshold":"<40%→停止加碼；連 2 季→減碼","window":"逐季","source":"公司季度新聞稿與法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9（MA❌例外）","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場在 FY2026 共識上修的同時，把 FY2027 本益比從約 12 倍殺到 7.4 倍，等於把盈餘當成 2030 年後會歸零的補貼年金。它沒算進一件事：232 每瓦 0.38 美元的最低進口價，高於公司現行新簽的 0.36 美元，退坡期的新約有漲價空間。這要等 12 月 4 日生效後的新約價格來證實"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=-6.35, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"MA=❌ 但 signal≥B 且 val≤🟡 且無 Veto：依「baseline rows 9/9b/10 的 MA 條件字面不含 ❌ 時，該組合不落空、不降觀望——按對應 val 燈 baseline row 裁決，MA❌ 僅作 row4 節奏調節」推論，verdict=進場（row4 pacing 已疊加，見上）"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"≤3%（循環商品子型、政策依賴）","requires_critic":[],"rearm_trigger":"第三季財報美國新簽 ≥2 GW 且單價 ≥0.34 美元／瓦，且週收盤站回 250 週均線（約 175 美元）之上","exec_line":"兩個條件同時成立，才重跑判斷並建首倉（單檔 ≤3%），分兩批：財報後一批；232 生效（12 月 4 日）後新約單價 ≥0.36 美元再一批。Single Thing 一發生就清倉"},"reasoning":{"industry":"最新一季是 2026 第二季。營收 10.56 億美元，年減約 4%，原因是去年同期有合約終止收入。毛利率約 57%，但含約 8,900 萬美元一次性 IEEPA 關稅回收，扣除後粗估約 48.6%。GAAP 營益率 42.6%，調整後 EBITDA 6.44 億美元（61%）。TTM 毛利率 44.0%、營益率 33.7%。事實表未涵蓋分部營收；看得到的結構是美國為主、印度為輔，兩地新簽單價分別是 0.36 與 0.20 美元／瓦。backlog 45.1 GW，合約值 136 億美元，交貨排到 2030；其中約 41 GW 帶本土含量條件（Widmar，2026-07-30）。單點依賴有兩處。第一是政策：45X 在 2025 年認列約 16 億美元（第三方彙整），約等於 2026 調整後 EBITDA 財測中值 27 億美元的六成。第二是客戶：Silicon Ranch 與 NextEra 各占 2025 年模組營收一成以上。產業時鐘方面，全球處於收縮期：2026 年全球需求是十餘年來首次年減，各環節產能嚴重過剩。FSLR 所在的美國受保護市場則在擴張，2026 年公用級新增 43.4 GW，年增 60%。供需方面，全球是結構性過剩；美國的緊俏是政策造成的，供給可逆性高，關稅一開豁免就會回灌。產業態勢是雙向拉鋸：競爭面在惡化（全球過剩、美國本土矽晶電池放量），結構面在轉好（232 底價、FEOC 收緊、本土合規供給至少短缺到 2027）。","moat":"機制：CdTe 薄膜不走中國主導的多晶矽鏈，加上美國本土規模製造，讓 FSLR 同時吃到本土含量與 45X 抵免，也避開矽晶進口要面對的反傾銷、232 與 FEOC 限制。同業 ROIC 事實表未涵蓋，方向改用兩條可比軸來證。第一條是利潤差距：TTM 營益率 33.65%，對比 CSIQ −0.55%、JKS −6.7%。第二條是單價：美國新簽從 2026 第一季的 0.34–0.35 升到第二季的 0.36 美元／瓦（含技術加價）。執行給 7 分：本土廠高稼動、量創新高，但南卡第二期延後、降成本碰到瓶頸。定價力給 7 分：未扣前是 8 分，因關稅牆可能漏水扣 1 分。等級落 B。判持平而不是擴大，是因為 backlog 在淨減、美國矽晶電池產能開始放量。判持平而不是縮減，是因為新簽單價在升、232 多了一道底價、本土產能賣到 2028。","growth":"成長來源有量有價。量：路易斯安那新廠全年化，南卡後段線 2026 下半年起最多 3.5 GW。價：CuRe 技術加價最多 6 億美元，多數落在 2027–2028；另有 232 底價。沒有併購，也沒有回購。共識 EPS：FY2026 17.61、FY2027 23.25、FY2028 29.13，兩年年增約 28.6%；近三個月 FY2026 上修 1.15%（Koyfin 快照，家數事實表未涵蓋）。內生天花板：投入資本與折舊不在事實表，算不出來。缺口主要歸因於利潤率擴張（45X 認列量增加、技術加價），不是靠再投資報酬，所以信心上限是中。跑道：美國公用級需求撐得住量，EIA 預估發電量從 2025 年 290 BkWh 升到 2027 年 424 BkWh，資料中心用電是主因。但 2030 年後 FSLR 的利潤受 45X 退坡與本土矽晶進場夾擊；鈣鈦礦只到試產線，Series 6 規格預計 2027 上半年就緒，尚未證實。所以判中等。衰退訊號亮 2 項：EPS 成長遠快於營收、自身倍數系統性下移。陷阱風險與長期成長性都判 🟡。AI 取代風險低，AI 資料中心反而是需求來源。","governance":"現金：第二季末淨現金約 17 億美元（2026-07-30 法說），落在公司 15–20 億的目標區，比第一季末的約 20 億少；年底財測是 17–23 億。第二季自由現金流 −3.06 億美元，是用上半年數字反推的。上半年營運現金流 −3.6 億（去年同期 −4.58 億）、資本支出 2.8 億，屬上半年營運資金的季節性；TTM 自由現金流率仍有 27.89%。錢的去向：營運資金準備、擴產（南卡後段線）、技術與研發（鈣鈦礦；第二季研發 7,600 萬美元），另外提前還清了印度 DFC 貸款。Bradley 表示對科技相關併購更開放，列為觀察。SBC 占營收 0.67%，用市銷率換算約占市值 0.19%／年，稀釋很低。營運槓桿：第二季營收年減約 4%、淨利年增約 24%，主因是關稅回收與 45X 占比提高，不是規模效應。三項計分中，併購與回購不適用，只有稀釋一項可評，而且通過。","valuation":"現價 172.97 美元。對 FY2026 共識 17.61 是 9.82 倍，對 FY2027 共識 23.25 約 7.4 倍，對 FY2028 共識 29.13 約 5.9 倍。P/E、P/S、EV/S 都在自身年底值的最低點；五年連續分位事實表未涵蓋。同業多數虧損，沒有可比本益比，所以終端倍數以自身前瞻 9.82 倍為錨。短期上檔：Base 情境 2027 年 EPS 22.5 乘現行 9.82 倍，約 221 美元，約 +28%。中期上檔：Base 2029 年 EPS 28.0 乘 9 倍（退坡在即，倍數再壓一點），約 252 美元，約 +46%。PEG 約 0.34（以 FY2026→FY2028 共識年增 28.6% 計），但對循環與政策盈餘意義有限。循環讀數：六個訊號裡三個偏買（估值在自身最低、量增價穩、情緒接近投降），兩個偏賣（毛利率近峰、美國新產能湧入），一個中性（庫存）。訊號互相矛盾，位置不明、偏中循環，姿態是持有不加。","premortem":"最強的三個反駁。第一，股價四個月跌約 38%，共識卻沒下修，市場可能在定價證據包沒涵蓋的規則風險（FEOC、45X）。第二，backlog 從 50.1 降到 45.1 GW，上半年新簽遠少於出貨。第三，盈餘約六成來自會退坡的抵免，第二季毛利率還含一次性關稅回收。三點都寫進反證紀錄。處置方式：Bear 機率拉到三成、終端倍數只給 11 倍、第三季財報前不建倉。歷史最大回撤與空方最強數字事實表未涵蓋；已知的是前份判斷日至今約 −38%，2022 年毛利率曾掉到 2.67%。陷阱判 🟡：衰退訊號亮 2 項，但最關鍵的兩年盈餘有合約撐。"},"plain":{"six":{"how_it_makes_money":"賺兩筆錢：一筆是美國公用級電廠開發商買本土合規模組的錢，背後付錢的是電力公司與雲端巨頭；另一筆是美國財政部的 45X 製造抵免。錢卡在「本土含量＋非中國供應鏈」這個節點。","moat":"護城河方向持平。靠政策加技術兩條腿，定價力還在，但來源是關稅牆與 45X，不是自己長出來的。","growth":"五年後跑道中等。美國公用級需求還在長，但 FSLR 的利潤跑道受 45X 退坡與本土矽晶進場夾擊，鈣鈦礦這條第二曲線還沒證實。","capital":"資本配置保守。錢回到擴產、技術與營運資金準備，不發股息也不回購；股東拿不到現金回饋，但公司也沒有亂花。","valuation":"現價只要求一件事：盈餘在補貼退坡後別崩。就算 2031 年 EPS 退回 FY2026 的 17.61、只給 10 倍，約 176 美元，也和現價打平。我信一半：前三年有合約撐，後兩年要看 232 底價補不補得上 45X 退坡。","how_wrong":"最可能看錯的地方：把補貼撐起的高峰盈餘當成常態，把 7.4 倍當成便宜。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場在 FY2026 共識上修的同時，把 FY2027 本益比從約 12 倍殺到 7.4 倍，等於把盈餘當成 2030 年後會歸零的補貼年金。它沒算進一件事：232 每瓦 0.38 美元的最低進口價，高於公司現行新簽的 0.36 美元，退坡期的新約有漲價空間。這要等 12 月 4 日生效後的新約價格來證實","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"trap":"🟡","val":"🟢","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":172.97,"week26_return_pct":-6.35,"consensus_rev_3m_pct":1.15,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母 FY2026 共識含 45X 抵免（粗估約占獲利六成），也含第二季約 8,900 萬美元一次性 IEEPA 關稅回收（約為全年調整後 EBITDA 財測的 3%）。五年持有期內抵免大半仍是全額，爭點在終值、不在分母；退坡放在終端倍數與 Bear 路徑處理"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"第三季財報：backlog、美國新簽單價、第四季指引","impact":"高","watch":"新簽 ≥2 GW、單價 ≥0.34 美元／瓦"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"232 太陽能關稅生效：模組每瓦 0.38 美元最低進口價，部分多晶矽衍生品加徵 15% 關稅","impact":"高","watch":"有沒有豁免或配額"},{"date":"2026-Q4","date_precision":"quarter","type":"capacity","event":"南卡羅來納後段線第一期投產","impact":"中","watch":"是否如期在 2026 下半年投產"},{"date":null,"date_precision":null,"type":"regulatory","event":"財政部 FEOC 最終規則","impact":"高","watch":"是否觸及 45X 資格與原料來源"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"第四季財報與 2027 全年財測","impact":"高","watch":"財測是否反映 232 生效後的新約價格"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"鈣鈦礦 Series 6 規格試產線就緒（公司指引 2027 上半年）","impact":"中","watch":"是否延後"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"南卡後段線第二期完工（原排程延到 2027 年中）","impact":"低","watch":"CuRe 導入進度"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s4`：現在 1,426B，下限 1,500B，**目標 ≥ 1,800B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FSLR_20260929/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s4 -->
<section id="s4">
<h2>4　護城河能不能站得住的第一關</h2>
<p class="lead">技術路線加上美國規模製造，同時拿到兩張政策門票。</p>
<ul class="pts">
<li>第一太陽能的核心機制是用碲化鎘薄膜這條非多晶矽的技術路線，搭配美國本土的規模化製造，兩件事疊在一起，同時滿足本土含量規定和 45X 抵免資格，這是別的美國廠不容易同時做到的組合。</li>
<li>矽晶模組如果要進口到美國，得面對反傾銷稅、232 條款和 FEOC 受關注外國實體規定的多重限制，第一太陽能因為原本就是本土一體化製造，直接繞過這些關卡，這是機制上的優勢，不是靠銷售話術。</li>
<li>合約本身也帶技術加價條款，不是單純賣一瓦多少錢，這代表公司有能力把技術優勢轉換成實際的合約單價，而不只是停留在規格書上好看。</li>
<li>這道門檻能不能算真正的護城河，還要看執行力和定價力兩項評分，公司在這兩項都拿到 7 分，最終護城河等級落在 B，算是站得住但不算頂級。</li>
<li>真正的考驗在於這道門檻是不是可逆的，201 條款已經到期，232 條款如果之後被豁免或配額掏空，矽晶模組隨時可能用每瓦 0.10 到 0.11 美元的低價回灌美國市場，把這道護城河的地基抽掉一部分。</li>
</ul>
<div class="mach"></div>
</section>

```