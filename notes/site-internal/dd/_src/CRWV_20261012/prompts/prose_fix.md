你是 stock-analyst v20 的**散文層（prose）agent**，標的 CRWV（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：CRWV　日期：2026-10-12　archetype：None　前份裁決：2026-05-23　B 衛星候選：Q1'26 Rev $2.08B +112%/adj EBITDA margin 56%/Backlog $99.4B (+49% QoQ) 但 Q2 指引偏低觸發 -10%；Microsoft 67% 客戶集中度極端 + Debt $25-29B D/E 4.5x；EV/Rev FY27 4.3x 同 tier 略折價；MA 🟠 中段消化（從 peak $187 -42%）；等 $90-95 分批進。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1797B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（894B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（876B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1227B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（987B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（479B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（710B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2512B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3219B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2090B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1797           3642-5203      5 條（2–6 內）  
s3                  8000         894           4974-7106      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3090          8337-11910      5 條（2–6 內）  
s6                 11000         479          7365-10521      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         710           1953-2790      5 條（2–6 內）  
s10                 5000        2512           1742-2488      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2090           2000-2910      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4724B；至少需散文≈40.28KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−750
−180%
−100
−100%
−57.4
−55%
−55
−53.6%
−50.5%
−40%
−23.7%
−19.53
−19.5%
−11
−3.94
−3.66
−3.04%
−3.0%
−2.81
−1.9%
−1.81
−1.3%
−0.8%
0
0.3
0.49
0.9
1%
1
1.02
1.1
1.2
1.25
1.28
1.4
1.5
1.5%
1.55
1.65
1.7
1.85
02
2%
2
2.00
2.3
2.5
2.6
3%
3
3.5
3.7
4
4.044
4.2
4.3
4.36
4.5
4.7%
5
5.0
05
5%
5.0%
5.5
5.8
6%
6
6.16
6.26
6.4
6.4%
6.5
6.79
07
7
7.1
7.3
7.7
7.8%
8
8%
08
8.6
9
9.4
10
10%
10.29
11
12
12%
12.0
13%
14
15%
15
17%
20%
20
23
23%
23.7%
24
24.5
25%
25.75
25.8
26
26%
29.3%
30
30%
30.6
31
34.2%
34.5
35%
36
36%
37
40%
40
42
43.7
45%
49
50
50%
56%
58%
59%
60%
62.3%
63%
64.0%
64.22
65%
67%
67.4%
70
70%
71.7%
72%
73
74.3%
75%
76%
80%
82.08
83%
90
94
95
95%
97
100%
100
103
104%
106
107.58
112%
124
128.7
132
140
150%
180
185
187
195
200
220
240
250
260
263
266
270
272.86
300
310
320
350
360
390
453
461
500
550
600
679
700
800
810
900
913
2024
2025
2026
2027
2028
2029
2030
2031
12869.75
21000
24000
25000
26000
27000
28000
34000
42000
43000
50000
55000
56000
68000
78000
80000
110000
160000
20261012
1,000
1,042
1,100
1,239
1,250
1,600
2,500
3,945
6,650
7,530
9,220
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
{"meta":{"ticker":"CRWV","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"CoreWeave, Inc."},"oneliner":"需求與合約都是真的：積壓訂單1,042億美元，Q2營收年增112%。但淨負債約461億美元，Q3利息費用指引約為調整後營業利益的四倍，股東排在債權人之後。現價大致只反映基準情境，要等利息覆蓋率翻轉。","thesis":{"H":[{"id":"H1","text":"合約營收如期兌現：FY2026營收落在指引124億至132億美元之內，FY2027達到240億美元以上（管理層稱2027年底年化營收逾300億，其中逾75%已簽約）","2y":"FY2026營收≥124億；FY2027≥240億","5y":null,"10y":null,"threshold":"FY2026營收<124億美元或FY2027<220億美元即削弱","source":"公司季報新聞稿與法說會（Q1 2026-05-07、Q2 2026-08-11）","drift_rule":"以指引中點為基準，連2季偏離≥5%為削弱，連3季≥10%為反轉"},{"id":"H2","text":"利潤率擴張跑贏利息：Q4 2026調整後營業利益率達十位數低段，2028年調整後營業利益至少等於利息費用","2y":"2027下半年調整後營業利益÷利息費用≥60%","5y":"FY2028調整後營業利益≥利息費用，且淨負債÷調整後EBITDA≤3.5倍","10y":null,"threshold":"Q2 2026比值為20%；2027下半年仍<40%即反轉","source":"季報新聞稿（調整後營業利益、利息費用）、10-Q債務明細","drift_rule":"TTM比值連4季低於路徑5%以上為削弱，連6季低於10%以上為反轉"},{"id":"H3","text":"舊世代GPU合約到期後能以接近原價續約，證明六年折舊與資產殘值站得住（管理層：H100到期以原價約95%續約，A100新約延到2029年）","2y":null,"5y":"2027至2029年到期的Hopper與Ampere叢集續約價≥原約80%，使用率維持","10y":"2030年後Blackwell叢集到期續約價≥原約70%","threshold":"續約價<原約80%，或大量轉入短期現貨並出現閒置，即削弱","source":"法說會續約揭露、10-K折舊政策與減損","drift_rule":"跨2個年度續約價低於門檻為削弱，跨3個年度為反轉"}],"R":[{"id":"R1","text":"客戶集中與交易對手信用：前兩大客戶約占上半年營收63%，10-Q預期集中會持續；OpenAI沒有信用評等、仍在燒現金，並與Broadcom自研10GW加速器","h_ref":"H1","clock":"🔥","threshold":"前兩大客戶合計占比2027年全年≥65%（沿用前份門檻），或任一客戶延後付款、縮減承諾","evidence_refs":["customer_second_source#0","customer_concentration_credit#2","customer_concentration_credit#4","customer_second_source#2"]},{"id":"R2","text":"利息與稀釋吃掉股東經濟：Q2利息6.4億美元是調整後營業利益1.28億的5倍，Q3利息指引8.6億至9.4億；FY2026資本支出兩度上調到350億至390億，公司表示後續可能需要額外債務或股權融資","h_ref":"H2","clock":"⚡","threshold":"Q4 2026調整後營業利益率未達10%，或單季利息費用超過10億而營業利益率沒有同步擴張","evidence_refs":["capital_markets_pricing#2","unprofitable_path_to_profitability#1","unprofitable_path_to_profitability#2","unprofitable_path_to_profitability#3","unprofitable_path_to_profitability#4","unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#1"]},{"id":"R3","text":"替代技術與GPU經濟壽命：客製加速器擴張、GPU供給改善；若舊世代租金崩落，六年折舊與殘值都不成立","h_ref":"H3","clock":"🐢","threshold":"任一主要客戶公開把50%以上推論工作移到自研晶片（沿用前份Microsoft門檻，並擴及全部大客戶），或舊世代續約價<原約80%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","supply_demand_durability#3"]},{"id":"R4","text":"交付與在地阻力：2025年底第三方資料中心延遲曾導致下修指引，並引來證券集體訴訟；供應鏈執行仍被形容為極其困難，地方禁建令在擴散","h_ref":"H1","clock":"⚡","threshold":"任一季因交付延遲而下修全年營收或活躍電力指引","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","regulatory_antitrust#2","major_events#1","major_events#2","lawsuit_class_action#0"]},{"id":"R5","text":"政策與地緣：資料中心用晶片的關稅豁免可能調整，AI法規跨轄區衝突，歐洲關稅威脅衝擊海外據點","h_ref":"H1","clock":"🐢","threshold":"資料中心用半導體的關稅豁免取消，或海外據點遭課稅，使單季毛利率年減超過3個百分點","evidence_refs":["reg_tariff_export#1","regulatory_antitrust#1","geo_supply_chain#0","geo_supply_chain#3"]}],"single_thing":{"description":"前兩大客戶任一縮減、延後或違約已簽的算力承諾","why_fatal":"兩家約占上半年營收63%，資產層級債務以這些合約為擔保。股權只占EV約一半，排在約461億美元淨負債之後；失去一家，營收與融資能力會同時斷裂，是數學上對終端股價最敏感的單一變數。","if_happens":"清倉；未持有者停止追蹤，直到重跑判斷。","how_monitor":"每季10-Q的客戶集中揭露、8-K重大合約變更、OpenAI與Microsoft的融資與資本支出動向、Meta與OpenAI承諾的交付進度","probability":"約10%（12至24個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-2.81,"FY2026E":-3.94,"FY2027E":-1.81,"FY2028E":1.25},"fy_end_month":12,"eps_basis":"GAAP稀釋EPS（Koyfin共識；基期取年度財報稀釋EPS），曆年制；共識口徑事實表未明標，推定為GAAP"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/scenario.json","archetype":{"primary":"未獲利高成長","secondary":"循環/商品","confidence":"中","fingerprint":"重資產算力出租，GAAP虧損，自由現金流深度為負，產能擴張靠債務與增資"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性偏緊，可延續到約2028年。Goldman估計供需在2028年前難以再平衡，電力是綁定約束。但GPU本身的供給已在改善；UBS估計超大規模雲端資本支出增速由2026年的76%降到2027年25%、2028年6%。供給可逆性高，2028年後反轉風險上升。","bargaining":{"up":"上游議價權強：加速器幾乎全數來自NVIDIA這一家供應商，記憶體與零組件漲價需要轉嫁。機殼與電力多由第三方資料中心提供，單一供應商不超過活躍基礎設施的17%（Q1法說）。","down":"下游集中：前兩大客戶約占上半年營收40%與23%。長約與照付不議條款鎖住營收，但大客戶有自建與第二供應商的選項。","geo":"美國以外已簽電力逾1GW（含印尼360MW）。地方禁建令與歐洲關稅威脅，主要影響選址與成本。"},"profit_pool_dir":"利潤池目前集中在NVIDIA，雲端算力這一環的超額報酬靠短缺撐著。短缺緩解後，利潤池有回流上游或流向客戶自建的風險。","tam_table":[{"item":"超大規模雲端前五大2026年資本支出","value":"約7,530億美元（年增83%），2027年約9,220億（KGI，2026-07）"},{"item":"2027年超大規模資本支出情境","value":"Goldman基準約1.1兆、樂觀1.4兆；Morgan Stanley 1.2兆；UBS估增速2027年25%、2028年6%"},{"item":"Neocloud GPU即服務營收（2030）","value":"約2,500億美元，推論占80%（ABI Research）"},{"item":"其他TAM估計","value":"定義不一：AI基礎設施2030年約3,945億（MarketsandMarkets）或約1,239億（Lucintel）；GPU即服務約266億。各家口徑不同，不能直接比較"},{"item":"公司相對位置","value":"FY2026共識營收約128.7億美元，約為ABI 2030年neocloud營收估計的5%；營業利益池占比的五年前與現在對照，事實表未涵蓋"}]},"moat":{"mechanism":"規模化交付速度（電力、液冷、整櫃上線）加上資產層級融資能力與AI軟體層，讓客戶以較低總持有成本取得最新世代算力","execution":8,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行力擴大（Q2新增近500MW，首家上線Vera Rubin），定價力目前偏強但靠短缺支撐；客製加速器與超大規模自建在侵蝕可服務市場，兩者相抵","peer_na_reason":"同業ROIC與投入資本事實表未涵蓋，改用營收規模與利潤率對照","threats":[{"level":"🔴","text":"客製加速器與超大規模自建：Google TPU、AWS Trainium3、Meta MTIA都在擴張，Broadcom稱2027年AI晶片營收能見度逾1,000億美元；OpenAI與Broadcom的10GW自研加速器自2026下半年起部署在其自家資料中心。這直接打到以NVIDIA整櫃為唯一產品的出租模式。","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#1","customer_second_source#2"]},{"level":"🟡","text":"Neocloud價格競爭：Nebius H100按需牌價約低四成，IREN拿下Microsoft合約。小型業者受融資約束可能出清，對公司是雙面影響。","p":"50%","evidence_refs":["end_markets#4"]},{"level":"🟡","text":"GPU經濟壽命可能短於六年折舊年限：若舊世代續約價大幅下滑，折舊與資產殘值都要重估。","p":"30%","evidence_refs":["substitute_technology#2","supply_demand_durability#3"]}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（模型研究員、推論服務）、決策者（實驗室與雲端的基礎設施主管）和付款者（同一法人）三者一致，需求以照付不議長約落地，積壓訂單1,042億美元。問題在付款能力：主要非超大規模客戶OpenAI沒有信用評等，採購承諾約6,650億美元，單季燒現金約37億美元。急迫性高，不代表持久。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一叢集合約的層級衡量。五年期合約、違約條款與SPV債務綁在一起，合約期內轉換成本高；到期時客戶可以自建、改用客製晶片或轉向其他neocloud。在Goldman會議上被問到供需正常化後超大規模客戶是否收回外包，CEO沒有給數字。"},{"item":"價值鏈分配","level":"🔴","text":"價值鏈中最難取代的是NVIDIA（加速器唯一來源）與電網接入。公司TTM毛利率67.4%看似不低，但營業利益率−3.0%，Q2調整後營業利益率只有5%；大部分價值在折舊（付給NVIDIA與零組件商）與利息（付給債權人）階段就被分走了。"},{"item":"社會容忍度","level":"🟡","text":"地方資料中心禁建令增加，紐約州暫停50MW以上新資料中心部分環評核准，最長一年。CEO預期選舉前聲量最大，並稱禁建只會改變建在哪裡，不會減少需求。公司自付電網升級費用以降低政治阻力，等於付了一筆保費。"}],"roiic":"≤0（TTM GAAP營業利益率−3.04%；投入資本口徑事實表未涵蓋，無法算出精確值）","reinvest_rate":">100%（Q2營運現金流6.79億美元對資本支出64.22億；FY2025營運現金流約31億對資本支出約103億）","endo_ceiling":0,"formula_note":"內生成長＝增量報酬×再投資率。增量營業報酬不高於零，所以不靠外部資金的內生成長上界取0，實際成長全部來自債務、客戶預付與增資。當期ROIC＝稅後營業利益率（為負）×投入資本周轉率（事實表未涵蓋），結果為負。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","CRWV":67.42,"NBIS":74.26,"ORCL":63.96,"IREN":62.32,"unit":"%"},{"metric":"營業利益率","CRWV":-3.04,"NBIS":-50.48,"ORCL":34.23,"IREN":-53.57,"unit":"%"},{"metric":"FCF 利潤率","CRWV":-179.92,"NBIS":-434.2,"ORCL":-40.01,"IREN":-332.45,"unit":"%"},{"metric":"研發密度","CRWV":null,"NBIS":26.3,"ORCL":14.19,"IREN":null,"unit":"%"}],"competitors":[{"name":"NBIS","gm":74.26,"om":-50.48,"fcf_margin":-434.2,"rd_intensity":26.3,"strategy_note":"毛利率74.3%高於CRWV，但營業利益率−50.5%，規模約為CRWV四分之一；用低價搶量，是市場的價格錨。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ORCL","gm":63.96,"om":34.23,"fcf_margin":-40.01,"rd_intensity":14.19,"strategy_note":"對照組裡唯一獲利者（營業利益率34.2%），但同樣在重資產擴張，自由現金流利潤率−40%；有既有雲端與資料庫事業可以補貼。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"IREN","gm":62.32,"om":-53.57,"fcf_margin":-332.45,"rd_intensity":null,"strategy_note":"由礦場轉型，強項是電力取得，已拿下Microsoft 97億美元合約；營業利益率−53.6%，仍在燒錢擴張期。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（GW產能）為主，價（合約價上調）其次，加上產品組合轉向推論與軟體；無併購、無回購","runway_years":"約5（以2030年8GW目標換算；滲透率事實表未涵蓋）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：增量報酬不高於零、再投資率超過100%，內生上界取0。共識FY2027營收年增約104%全部超出上界，屬外部融資驅動。","segments":{"expanded":false,"reason":"公司未揭露分部營收。GPU以外的儲存、CPU、網路與軟體ARR逾4億美元，託管推論訂約ARR逾1億，合計不到年底年化營收（185至195億）的3%，目前還不決定利潤；託管推論ARR超過10億時再展開"},"decay_signals":["毛利率下滑：FY2024 74.3%、FY2025 71.7%、TTM 67.4%（年度與TTM口徑；季度年對年連續資料事實表未涵蓋）","替代技術壓縮可服務市場：客製加速器擴張，OpenAI自研10GW","未亮：SBC占營收Q2為6.4%，高於5%，但FY2025約12%降到2026年約6%，並非逐年上升"]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產能擴建，不靠併購撐；無股息、無回購，股東報酬為負（淨發行）"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Weights & Biases約10.29億美元（2025-05完成）等軟體收購，已實現增量報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"無回購，反而持續發行股權與可轉債","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋加權股數2025年增7.8%（4.044億到4.36億股），遠高於每年1.5%","grade":"不過"}]},"valuation":{"basis":"EV/S（前瞻，EV÷FY2026共識營收），終端扣除淨負債","tier":"未獲利重資產算力租賃","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業EV/S或EV/毛利現值，無法做同類倍數錨；終端倍數改以自身EBITDA利潤率換算EV/EBITDA約6倍校準"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"基準情境5年終端價約103美元，對現價82.08美元年化約4.7%，機率加權年化約5%，都低於8%的弱門檻。EV對FY2027營收約3.5倍看似不貴，但股權只占EV一半，淨負債會隨資本支出擴張，倍數便宜不等於股權便宜。TTM EV/S落在上市以來四個年度端點的最低點，但上市未滿兩年，沒有五年分位。","upside_short_pct":-11,"upside_mid_pct":26},"trap_analysis":{"verdict":"🟡","label":"槓桿型成長：營收真實，股東剩餘價值存疑"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"UBS估超大規模資本支出增速2027年25%、2028年6%；GPU供給改善，稀缺轉向電網；客製加速器在擴張；研究機構認為不少小型neocloud撐不過融資與規模門檻。","assumption":"需求在2028年前不降溫，舊世代續約價不崩","consequence":"2028年後新約與續約價格下跌，營收停在260億至300億附近，終端EV/S壓到2.5倍，淨負債約800億美元時股權歸零","ruling":"採納：這是空頭情境的主體，配30%機率，終端價歸零","watch":"超大規模雲端2027年資本支出指引、Hopper續約價、每季新簽承諾金額","evidence_refs":["supply_demand_durability#3","substitute_technology#0","substitute_technology#1","end_markets#4"],"fact_refs":["f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"Q2利息6.4億美元對調整後營業利益1.28億；Q3利息指引8.6億至9.4億，對調整後營業利益2億至2.6億。稀釋股數2025年增7.8%，SBC每季約1.4億至1.65億。曾提出約90億美元全股票收購Core Scientific，被對方股東否決。全年資本支出上調後，公司表示可能需要額外債務或股權融資。","assumption":"營收照管理層路徑在2030年走到8GW","consequence":"營收翻四倍，但淨負債同步擴張到約1,100億、股數增到約8億，每股價值成長被吃掉；基準情境5年年化只有約5%","ruling":"採納：這是本輪下調評級的主因","watch":"調整後營業利益÷利息費用、淨負債÷年化調整後EBITDA、每季股數","evidence_refs":["unprofitable_path_to_profitability#2","unprofitable_path_to_profitability#4","unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#1","major_events#0","ma_merger#0","capital_markets_pricing#2"],"fact_refs":["f_net_debt_m","f_kpi4_sbc","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"EV約913億美元，已是FY2026共識營收的7.1倍；基準情境終端價約103美元，只比現價高26%。賣方平均目標價140美元，隱含的是接近樂觀情境的假設。","assumption":"市場用賣方目標價看待這檔股票","consequence":"想拿到樂觀情境的報酬，必須押注2030年8GW全部到位，而且終端倍數維持4.5倍以上；任何一項落空，報酬就退回基準或更差","ruling":"部分採納：現價不是泡沫，但只付得起基準情境。股價下跌不是安全邊際，因為股權只占EV一半","watch":"利息覆蓋率與淨負債路徑、賣方目標價的下修幅度","evidence_refs":[],"fact_refs":["f_ev_s_fwd","f_ev_m","f_price_at_dd","f_week26_return_pct"]},{"view":"論點失敗","evidence":"管理層在關鍵問題上迴避：Q1法說拒絕拆解上下半年營業利益、拒絕給每季新增兆瓦數；Goldman會議上被問到供需正常化後大客戶收回外包，CEO先說自己前一題答得最政治正確，之後沒有給數字。","assumption":"正常化之後大客戶仍然續約","consequence":"若正常化後大客戶收回外包，2029至2031年到期合約的續約量與價格同時下滑","ruling":"部分採納：Q2實績已兌現上半年承諾，迴避本身不算證據；但正常化情境的數字缺口，正是空頭機率不下調的理由","watch":"2027年起每季揭露的續約量與續約價","evidence_refs":[],"fact_refs":[]}],"max_dd":{"lo":-100,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 107.58 → 本次 82.08（-23.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=107.58","side_b":"本次 price_at_dd=82.08","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 107.58 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 107.58 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 107.58 美元：Bull 價 272.86、Bear 價 0，五年期望值 −1.3%，基準年化 −0.8%，不對稱比 1.02","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.02。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 107.58 美元：五年期望值 −1.3%，基準年化 −0.8%，不對稱比 1.02","side_b":"本次情境、股價 82.08 美元：五年期望值 +29.3%，基準年化 4.7%，不對稱比 1.55","ruling":"再換股價、情境不動：起點價下跌 23.7%，五年期望值多 30.6 個百分點，基準年化多 5.5 個百分點，不對稱比由 1.02 升到 1.55。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：管理層承諾兌現度","cause":null,"prior_field":null,"side_a":"Q1法說（2026-05-07，CFO）：Q2營收24.5億至26億、調整後營業利益0.3億至0.9億、利息6.5億至7.3億；2026年底活躍電力逾1.7GW","side_b":"Q2實際（2026-08-11）：營收25.75億、調整後營業利益1.28億、利息6.4億；年底電力指引上調到逾1.85GW，全年營收指引上調到124億至132億","ruling":"一致：上半年承諾全數兌現或超越，執行面不是爭點","evidence_level":"一手（法說會逐字稿、公司新聞稿）","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"矛盾：資本支出一再上調，營收指引只小幅上調","cause":null,"prior_field":null,"side_a":"Q1法說：全年資本支出310億至350億，下緣因零組件漲價上調","side_b":"Q2法說：全年資本支出上調到350億至390億，中點增加40億；全年營收中點只增加約3億","ruling":"可調和（程度差異）：新增資本支出主要用在2027年交付與新簽大單，Q3初逾250億新承諾可以解釋。但全年資本支出約為年底年化營收的兩倍，股東要等到合約後段才看得到現金。以2027年營收能否跟上為準","evidence_level":"一手","settle_metric":"FY2027營收對240億門檻；2027年資本支出指引","if_then":["若2027年資本支出指引再上調而調整後營業利益率沒有擴張，維持不建倉，空頭機率上調到35%","反向：若2027上半年調整後營業利益÷利息費用連兩季≥60%，重跑判斷並允許小額首倉"],"evidence_refs":["capital_markets_pricing#2","unprofitable_path_to_profitability#1"]},{"axis":"矛盾：利潤率擴張與利息擴張","cause":null,"prior_field":null,"side_a":"管理層：利潤率壓力是時間性而非經濟性（Q1法說，CFO）；新約貢獻利潤率高5至10個百分點，Q4調整後營業利益率可達十位數低段；加權債務成本一年降近300個基點","side_b":"Q2利息6.4億是調整後營業利益1.28億的5倍。Q3指引中點利息9億對調整後營業利益2.3億，比值約26%；Q2到Q3利息增加約2.6億，營業利益只增加約1億","ruling":"可調和（時間差），但數據出來前偏向空方：管理層談的是合約層級的報酬，股權層級要等利潤率增量追上利息增量才成立。執行上不建倉，等比值翻轉","evidence_level":"一手指引數字","settle_metric":"季度調整後營業利益÷利息費用（Q2 2026為20%）","if_then":["若2027上半年連兩季比值≥60%，且全年資本支出未再上調，重跑判斷，允許小額首倉","若2027下半年比值仍<40%，持有者清倉，未持有者停止追蹤","反向：若2026年第四季比值就超過50%，提前重跑判斷"],"evidence_refs":["unprofitable_path_to_profitability#2","unprofitable_path_to_profitability#4"]},{"axis":"矛盾：7月調價約25%與公開牌價未變","cause":null,"prior_field":null,"side_a":"CFO（Q2法說2026-08-11）：7月跨SKU調價約25%，營業利益率的改善還發生在調價之前","side_b":"第三方牌價追蹤：公開按需牌價7月到8月未變，H100每GPU時6.16美元","ruling":"可調和：調價可能落在合約價與新簽約上，不會反映在公開按需牌價；第三方來源是競品部落格。不作為評級依據，以Q3、Q4的每兆瓦營收驗證","evidence_level":"一手對二手","settle_metric":"季度營收÷平均活躍電力","if_then":["若Q4 2026的季營收÷平均活躍電力沒有比Q2提高，視為調價未落地，空頭機率維持30%、不下調"],"evidence_refs":["end_markets#5"]},{"axis":"產業態勢：競爭、結構與其他變數","cause":null,"prior_field":null,"side_a":"結構轉好：電力是綁定約束，Goldman估供需在2028年前難以再平衡，新電網核准要24至36個月；公司已簽電力4.2GW","side_b":"競爭與替代惡化：Nebius牌價低約四成，IREN拿下Microsoft合約，客製加速器在擴張。其他結構變數：地方禁建令擴散，AI法規跨轄區衝突","ruling":"雙向拉鋸：電力稀缺短期內保護既有產能的定價，但客製晶片與自建會在2028年後侵蝕可服務市場。小型業者出清對公司份額有利，同時也提醒融資市場對整個族群的耐心有限","evidence_level":"多為二手預測","settle_metric":"2027年超大規模資本支出實際增速；公司新簽約價","if_then":["若2027年超大規模資本支出增速低於15%，空頭機率上調到35%，維持不建倉"],"evidence_refs":["end_markets#4","supply_demand_durability#3","regulatory_antitrust#1"]},{"axis":"方法：未獲利成長股的現金流門檻","cause":null,"prior_field":null,"side_a":"營收成長加自由現金流利潤率：112%加約−180%，遠低於20，且連兩季成立，照這把尺應直接拒絕","side_b":"重資產長約租賃的自由現金流反映的是產能預建，資本支出對應已簽的照付不議合約；現金跑道由已取得的逾320億美元融資支應（Q2法說），這把尺對這類業務失真","ruling":"不直接拒絕，改給弱評級，並把融資取得失敗列為清倉條件。若這把尺證實為對，判斷依據是：2027年6月前，新一輪資產層級融資的成本明顯高於現行，或出現大額折價增資","evidence_level":"一手","settle_metric":"新債成本相對現行加權成本、單次增資規模","if_then":["若2027年6月前新債成本比現行加權成本高200個基點以上，或單次增資超過流通股10%，清倉並停止追蹤"],"evidence_refs":["unprofitable_path_to_profitability#3"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"積壓訂單1,042億，加上Q3初逾250億新承諾；舊世代以原價約95%續約，A100新約延到2029年；新約貢獻利潤率高5至10個百分點；債務成本一年降近300個基點；股價自高點跌逾一半，EV對FY2027營收約3.5倍","side_b":"以上全是合約層級的好消息；股權層級看，淨負債約461億且隨資本支出擴大，利息增量大於營業利益增量","ruling":"不採納為進場理由，但列入重新評估條件：只要利息覆蓋率翻轉，這些好消息就會直接流到股東","evidence_level":"一手","settle_metric":"季度調整後營業利益÷利息費用","if_then":["若Q4 2026調整後營業利益率≥13%，且利息費用季增不超過10%，提前重跑判斷"],"evidence_refs":[]},{"axis":"客戶集中度的兩種讀法","cause":null,"prior_field":null,"side_a":"10-Q（Q1 2026）：前兩大客戶約占營收65%；Q2 10-Q預期集中度會因長約而持續","side_b":"第三方分析：最大客戶占比由Q1的45%降到Q2的36%；前兩大約占上半年營收40%與23%","ruling":"可調和：最大客戶占比確實在下降（去年同期為72%），但前兩大合計仍約六成。前份「Microsoft占比逐步下降」的方向成立，程度還不夠","evidence_level":"一手對第三方","settle_metric":"10-Q前兩大客戶合計占比","if_then":["若2027年全年前兩大合計占比≥65%，客戶風險升為主要風險，空頭機率上調到35%"],"evidence_refs":["customer_concentration_credit#2","customer_second_source#0"]},{"axis":"前份漂移：評級、陷阱風險、護城河方向","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份（2026-05-23）：評級B、陷阱風險🟡、護城河→","side_b":"本次：評級C、陷阱風險🟡、護城河→","ruling":"評級下調來自新證據：Q2財報後全年資本支出再上調40億，Q3利息指引8.6億至9.4億約為調整後營業利益的四倍，淨負債約461億。陷阱風險維持，衰退信號仍為2項。護城河方向維持，交付優勢擴大與客製晶片侵蝕相抵","evidence_level":"一手","settle_metric":"季度調整後營業利益÷利息費用","if_then":[],"evidence_refs":["capital_markets_pricing#2","unprofitable_path_to_profitability#2"]},{"axis":"前份漂移：估值結論與情境方法","cause":"方法變動","prior_field":["val","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：估值🟡（以FY2027 EV/營收4.3倍、同類略折價判斷）；成長跑道、公司類型、循環位置、情境機率與最大回撤都未填","side_b":"本次：估值🟠（營收路徑×終端EV/S，並扣除終端淨負債）；成長跑道🟡；公司類型為未獲利高成長；非循環股，不判循環位置；機率樂觀20、基準50、空頭30；最大回撤−55%至−100%","ruling":"方法變動：前份沒有扣除淨負債路徑。股價雖從107.58美元跌到82.08美元，但淨負債擴張後股權價值降得更多，估值結論反而轉弱。其餘欄位由空白改為有值，同屬方法補齊","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：假設與風險門檻","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：H2以Microsoft占比67%逐步下降、2027年全年≥65%為反轉；H3以債務/EBITDA在FY2028>3.5倍為反轉；R1為Microsoft自研晶片，R3為OpenAI自研晶片","side_b":"本次：集中度門檻沿用（前兩大合計2027年≥65%），移到風險項；債務/EBITDA門檻原樣保留在清倉條件；兩項自研晶片風險合併為客製加速器風險，並擴及全部大客戶；新增利息覆蓋與舊世代續約兩條假設","ruling":"新證據：最大客戶占比已由去年72%降到約36%至45%，只盯Microsoft已不是最準確的描述；新財報暴露出來的承重變數是利息與續約價","evidence_level":"一手","settle_metric":null,"if_then":[],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"門檻變動：清倉與減碼條件","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份沒有設清倉或減碼門檻，只有警戒閾值「FY27 H1 Debt/EBITDA > 4x → 反轉」","side_b":"本次：淨負債÷年化調整後EBITDA在2027上半年>4倍或2028全年>3.5倍則清倉（前份門檻原樣保留，現值約7.7倍）；調整後營業利益÷利息費用在2027下半年<40%則清倉；FY2026營收<124億則減碼；前兩大客戶縮減承諾則清倉","ruling":"新證據：Q2的利息與資本支出指引讓股權報酬取決於覆蓋率，所以把前份的警戒值升格為清倉門檻，並補上覆蓋率與營收的減碼條件。現值依Q2調整後EBITDA 15億年化計算","evidence_level":"一手","settle_metric":"淨負債÷年化調整後EBITDA；調整後營業利益÷利息費用","if_then":[],"evidence_refs":["unprofitable_path_to_profitability#2"]},{"axis":"門檻變動：重新評估條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新評估條件（裁決文字為等90至95美元分批進）","side_b":"季度調整後營業利益÷利息費用連兩季≥60%（Q2 2026為20%），且全年資本支出指引未再上調","ruling":"由價格條件改為事件條件：股價已跌破90至95美元區間，但本輪的約束是利息覆蓋率而不是價格，價格再低也取代不了覆蓋率翻轉","evidence_level":"一手","settle_metric":"季度調整後營業利益÷利息費用","if_then":[],"evidence_refs":["unprofitable_path_to_profitability#2"]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（Single Thing為空）","side_b":"前兩大客戶任一縮減、延後或違約已簽的算力承諾","ruling":"Single Thing為本次新設：前份沒有填。依對終端股價的敏感度排序，客戶承諾大於任何單一技術或政策事件；一旦發生即清倉","evidence_level":"一手","settle_metric":"8-K重大合約變更、10-Q客戶集中揭露","if_then":[],"evidence_refs":["customer_concentration_credit#4"]}],"triggers":[{"n":1,"text":"Q3 2026財報營收對指引","type":"假設驗證","maps_to":"H1","metric":"Q3 2026營收","threshold":"<34.5億美元（指引下緣）","action":"不追；H1列為削弱，維持不建倉","source_freq":"季報","date":"2026-11","evidence_refs":[]},{"n":2,"text":"利息覆蓋率翻轉（重新評估條件）","type":"估值rearm","maps_to":"H2","metric":"季度調整後營業利益÷利息費用","threshold":"連兩季≥60%，且全年資本支出未再上調（Q2 2026為20%）","action":"重跑判斷；通過後首倉以小額試探倉為上限","source_freq":"季報","date":"2027-05","evidence_refs":["unprofitable_path_to_profitability#2"]},{"n":3,"text":"前兩大客戶縮減或違約","type":"Single Thing","maps_to":"Single Thing","metric":"8-K重大合約變更與10-Q客戶集中揭露","threshold":"任一客戶縮減、延後或違約已簽承諾","action":"清倉","source_freq":"即時（8-K）與季報","date":null,"evidence_refs":["customer_concentration_credit#4","customer_second_source#0"]},{"n":4,"text":"利潤率擴張沒有落地","type":"風險","maps_to":"R2","metric":"Q4 2026調整後營業利益率","threshold":"<10%（管理層承諾為十位數低段）","action":"停止加碼；空頭機率上調到35%","source_freq":"季報","date":"2027-02","evidence_refs":["unprofitable_path_to_profitability#2","capital_markets_pricing#2"]},{"n":5,"text":"交付延遲重演","type":"風險","maps_to":"R4","metric":"全年營收或活躍電力指引","threshold":"任一季因第三方資料中心延遲而下修","action":"減碼","source_freq":"季報","date":null,"evidence_refs":["geo_supply_chain#1","major_events#2"]},{"n":6,"text":"融資條件惡化","type":"清倉","maps_to":"R2","metric":"新債成本與增資規模","threshold":"新債成本比現行加權成本高200個基點以上，或單次增資超過流通股10%","action":"清倉","source_freq":"即時（8-K）","date":null,"evidence_refs":["unprofitable_path_to_profitability#4","unprofitable_dilution_trajectory#0"]},{"n":7,"text":"舊世代GPU續約價","type":"假設驗證","maps_to":"H3","metric":"Hopper與Ampere到期續約價相對原約","threshold":"<80%","action":"減碼","source_freq":"法說會","date":"2027–2029","evidence_refs":["substitute_technology#2"]},{"n":8,"text":"槓桿警戒（前份門檻沿用）","type":"清倉","maps_to":"H2","metric":"淨負債÷年化調整後EBITDA","threshold":"2027上半年>4倍，或2028全年>3.5倍（現值約7.7倍）","action":"清倉","source_freq":"季報","date":"2027-08","evidence_refs":["unprofitable_path_to_profitability#4"]},{"n":9,"text":"財報後複審","type":"複審日期","maps_to":null,"metric":"Q3 2026財報與指引","threshold":"財報公布後","action":"重跑判斷","source_freq":"季報","date":"2026-11","evidence_refs":[]}],"kill_metrics":[{"metric":"淨負債÷年化調整後EBITDA","bear_threshold":"2027上半年>4倍或2028全年>3.5倍（前份門檻沿用，現值約7.7倍）","window":"2027上半年至2028年底","source":"公司季報新聞稿與10-Q","last_status":"warning"},{"metric":"季度調整後營業利益÷利息費用","bear_threshold":"2027下半年仍<40%（Q2 2026為20%）","window":"2027年第3至第4季","source":"公司季報新聞稿","last_status":"warning"},{"metric":"前兩大客戶已簽承諾","bear_threshold":"任一縮減、延後或違約","window":"滾動","source":"10-Q客戶集中揭露與8-K","last_status":"ok"},{"metric":"FY2026營收對指引下緣","bear_threshold":"<124億美元","window":"2027-02財報","source":"公司年報新聞稿","last_status":"ok"},{"metric":"稀釋股數年增率","bear_threshold":">10%","window":"滾動四季","source":"10-Q","last_status":"unknown"},{"metric":"舊世代GPU續約價相對原約","bear_threshold":"<80%","window":"2027至2029年","source":"法說會揭露","last_status":"unknown"}],"evidence_dismissed":[{"ref":"unprofitable_dilution_trajectory#3","reason":"這條證據的前提是Core Scientific全股票併購完成，但同一證據包的重大事件紀錄顯示，該案已在2025-10-30因對方股東否決而終止，所述稀釋不會發生。管理層願意用股票做大額交易的傾向，已另記在股東經濟的反證中"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=-19.53, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='未獲利高成長', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"季度調整後營業利益÷利息費用連兩季≥60%（Q2 2026為20%），且全年資本支出指引未再上調","exec_line":"未持有者不建倉，也不因價格下跌接刀；重新評估條件達成後重跑判斷，首倉以總資產1%試探為上限。持有者遇到清倉條件即全數出清"},"reasoning":{"industry":"收錢方式：客戶簽約五年左右的照付不議合約租用整櫃GPU算力，交付後按合約期直線認列。另有儲存、CPU、網路與軟體（Weights & Biases等）ARR逾4億美元；託管推論的訂約ARR從100萬美元升到逾1億（Q2法說）。最新一季（Q2 2026）營收25.75億美元，年增112%；調整後營業利益1.28億（5.0%），GAAP營業損失0.49億（−1.9%）；TTM毛利率67.4%。積壓訂單1,042億美元，另有Q3初逾250億新承諾尚未計入。活躍電力1.5GW，已簽電力約3.7GW（法說當日為4.2GW）。公司未揭露分部營收。單點依賴：前兩大客戶約占上半年營收40%與23%，加速器幾乎全數來自NVIDIA；兩端都是集中度風險，不是護城河證據。產業時鐘判在過熱期，依據有三：新舊世代GPU售罄並調價、零組件短缺、資本支出年增八成且大量靠債務支應；賣方也已預期2027至2028年增速急降。供需持久度：屬週期性偏緊，電力約束可撐到約2028年，GPU本身的供給可逆性高。","moat":"機制：大規模、快速把NVIDIA新世代整櫃系統上線的能力，加上配套的資產層級融資與軟體層（Mission Control、Weights & Biases）。可證方向改用規模與利潤率對照，因為同業ROIC與投入資本事實表未涵蓋。Q2營收約25.8億美元，Nebius約5.8億、IREN約1.4億；單季新增近500MW活躍電力。TTM毛利率：CRWV 67.4%、NBIS 74.3%、IREN 62.3%、ORCL 64.0%；營業利益率：CRWV −3.0%，NBIS −50.5%，IREN −53.6%，ORCL 34.2%。執行面在擴大：首家驗證Vera Rubin NVL72，ClusterMAX評為Platinum。定價面目前偏強：公開牌價H100每GPU時6.16美元，比Nebius高約六成；管理層稱舊世代以原價約95%續約，A100新約延到2029年。但這份定價權來自短缺，客製加速器擴張後可能鬆動。兩者相抵，方向判持平。當期ROIC為負：稅後營業利益率為負，周轉率事實表未涵蓋。增量報酬不高於零、再投資率超過100%，不靠外部資金的內生成長上界取0。","growth":"成長來源以量為主（活躍電力由1.5GW到年底逾1.85GW，已簽4.2GW，另有約1.5GW土地與意向書選項），價格其次（Blackwell與Vera Rubin定價創新高，CFO稱7月跨SKU調價約25%），再加上產品組合轉向推論與軟體。沒有併購驅動，也沒有回購。共識營收FY2026約128.7億美元、FY2027約263億（年增約104%）。共識EPS由FY2025實際−2.81到FY2028E 1.25，基期為負，三年CAGR無法計算；近三個月FY2026共識EPS從−3.66下修到−3.94。內生上界取0（見護城河段），所以共識成長與內生上界的缺口全部來自外部融資與預期中的利潤率擴張，不能歸因於回購或收購，信心上限為中。跑道：滲透率事實表未涵蓋；以年底年化營收185至195億、對應1.85GW推算，每GW約年營收100億，走到8GW約需5年。2030年後的關鍵是2024至2026年所簽合約的續約價。第二曲線有來源但很小：託管推論目標年底ARR至少2.5億美元，軟體與其他服務ARR逾4億，合計不到年化營收的3%。","governance":"淨利為負，自由現金流對淨利的轉換率沒有意義。Q2自由現金流−57.4億美元（營運現金流6.79億減購置固定資產64.22億；法說口徑的總資本支出為94億）。SBC 1.65億，占營收6.4%。現金去向四分：資本支出壓倒性為主；收購次之（2025年Weights & Biases約10.29億，另有OpenPipe、Monolith、Marimo）；回購為零；股息為零。融資面：Q2透過債務、可轉債與股權募集約180億美元，累計取得逾320億；加權債務成本一年降近300個基點（約每年省11億利息）；Q1法說稱2029年前沒有到期債務（自償合約債與OEM融資除外）。稀釋：稀釋加權股數2024年4.044億股到2025年4.36億股，年增7.8%。營運槓桿為負：Q2營收年增112%，調整後營業利益卻年減36%（2.00億到1.28億），差距遠大於3個百分點，主因是新產能的爬坡成本，列入成長熄火觀察。2025年曾提出約90億美元全股票收購Core Scientific，後被對方股東否決，顯示管理層願意用股票做大額交易。","valuation":"EV約913億美元，由市值約453億加淨負債約461億組成。EV/S的TTM口徑為12.0倍，對FY2026共識營收為7.1倍，對FY2027共識營收約3.5倍（913÷263）。股權只占EV約一半，所以EV每變動10%，股價約變動20%。基準情境：2031年營收550億、EV/S 3.5倍，扣淨負債1,100億，除以8億股，約103美元，比現價82.08美元高26%，年化約4.7%。機率加權約106美元，年化約5%。賣方31家平均目標價140美元（9月初快照），隱含的是接近樂觀情境的假設。PEG不適用：三年EPS基期為負。同業倍數事實表未涵蓋；終端倍數改以自身調整後EBITDA利潤率約58%換算EV/EBITDA約6倍來校準，對照重資產租賃業的常見區間。不主張市場看錯。","premortem":"股價自2026年高點約187美元（前份摘要）跌到現價，回撤約56%；26週報酬−19.5%，RSI 43.7。股權只占EV約一半，回撤會被槓桿放大。已知事件：2025年11月因第三方資料中心延遲下修指引，引來證券集體訴訟（目前是指控，尚未裁決）。管理層在幾個關鍵問題上迴避：拒絕拆解上下半年營業利益、拒絕給每季新增兆瓦數、被問到供需正常化後的情境時沒有給數字。衰退信號亮2項，陷阱風險中等，依據見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"這門生意收的是AI實驗室與超大規模雲端的算力租金：用約五年期的照付不議長約出租NVIDIA整櫃系統。錢卡在電力與機櫃交付這一環，利潤則先被折舊與利息分走。","moat":"護城河方向持平（→），等級C。交付速度與融資能力在擴大，但定價權建立在算力短缺上，客製晶片與大客戶自建正從另一端侵蝕。","growth":"後五年跑道中等（🟡）：2030年8GW目標有電力合約撐腰，但成長幾乎全靠外部資金，第二條曲線（託管推論與軟體）仍然很小。","capital":"資本配置偏弱：沒有回購也沒有股息，股數持續稀釋，資本支出靠債務與增資支應；計分卡三項沒有一項通過。","valuation":"現價要求公司在2031年做到約550億美元營收、終端EV/S約3.5倍，淨負債壓在約1,100億以內，股東才拿得到約年化5%。這就是基準情境本身，沒有安全邊際。我信營收會到，不信股東能分到夠多。","how_wrong":"最可能看錯的地方，是把合約能見度當成股東報酬能見度：營收大概率兌現，但利息、折舊與稀釋可能讓股權長期分不到剩餘價值。反方向的錯，是低估舊世代GPU續約帶來的現金流。"}},"decision_inputs":{"signal":"C","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等的是事件不是價格：季度調整後營業利益÷利息費用連兩季≥60%，且全年資本支出未再上調","trap":"🟡","val":"🟠","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"未獲利高成長","price_at_dd":82.08,"week26_return_pct":-19.53,"consensus_rev_3m_pct":7.65,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"營收口徑沒有一次性項目；真正的爭點在分子端的淨負債路徑，不在分母。一年期推估：FY2027基準營收250億×5.0倍（成長放緩後當年度EV/S由7.1倍收斂）＝1,250億，扣淨負債約810億（資本支出續燒的粗估），除以約6億股，約73美元"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026財報與Q4指引","impact":"高","watch":"利息費用對調整後營業利益的比值，以及2027年資本支出的初步指引"},{"date":"2026-11","date_precision":"month","type":"regulatory","event":"美國期中選舉前後的資料中心議題","impact":"中","watch":"地方禁建令與州級環評暫停是否擴散"},{"date":"2026-Q4","date_precision":"quarter","type":"capacity","event":"首座自建資料中心上線","impact":"中","watch":"自建站點的每兆瓦成本與毛利"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026財報與FY2027指引","impact":"高","watch":"FY2027營收與資本支出指引，年底活躍電力是否超過1.85GW"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,316B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭地位</h2>
<p class="lead">護城河等級 C，方向持平，執行強、定價靠短缺。</p>
<ul class="pts">
<li>護城河的機制是規模化交付速度加上資產層級融資與軟體層。公司能把 NVIDIA 新世代整櫃系統（電力、液冷、整櫃上線）較快上線，讓客戶以較低總持有成本取得最新算力。Q2 單季新增近 500MW 活躍電力，首家驗證 Vera Rubin NVL72，ClusterMAX 評為 Platinum。執行面評 8 分。</li>
<li>定價面目前偏強，評 6 分。公開牌價 H100 每 GPU 時 6.16 美元，比 Nebius 高約六成，管理層稱舊世代以原價約 95% 續約。但這份定價權來自短缺，客製加速器擴張後可能鬆動。所以定價面不能和執行面等量齊觀。</li>
<li>最大的威脅是客製加速器與超大規模自建。Google TPU、AWS Trainium3、Meta MTIA 都在擴張，Broadcom 稱 2027 年 AI 晶片營收能見度逾 1,000 億美元。OpenAI 與 Broadcom 的 10GW 自研加速器自 2026 下半年起部署在自家資料中心。這直接打到以 NVIDIA 整櫃為唯一產品的出租模式，發生機率約 35%。</li>
<li>Neocloud 價格競爭是第二個威脅，機率約 50%。Nebius H100 按需牌價約低四成，IREN 拿下 Microsoft 97 億美元合約。小型業者受融資約束可能出清，對公司是雙面影響：份額有利，但也提醒融資市場對整個族群的耐心有限。</li>
<li>GPU 經濟壽命是第三個威脅，機率約 30%。若舊世代續約價大幅下滑，六年折舊與資產殘值都要重估。這一項要到 2027 至 2029 年大量到期時才能驗證，現在只能看管理層的揭露。</li>
<li>價值鏈分配是最弱的一環。最難取代的是 NVIDIA 與電網接入。TTM 毛利率 67.4% 看似不低，但營業利益率 −3.0%，Q2 調整後營業利益率只有 5%。大部分價值在折舊（付給 NVIDIA 與零組件商）與利息（付給債權人）階段就被分走了。</li>
<li>需求基礎值有問題的是付款能力。主要非超大規模客戶 OpenAI 沒有信用評等，採購承諾約 6,650 億美元，單季燒現金約 37 億美元。前兩大客戶約占上半年營收 63%。急迫性高，不代表持久。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```