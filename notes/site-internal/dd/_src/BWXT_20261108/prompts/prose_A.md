你是 stock-analyst v20 的**散文層（prose）agent**，標的 BWXT（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：BWXT　日期：2026-11-08　archetype：None　前份裁決：2026-09-05　進場·條件式（爆發候選）｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1561B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（441B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1121B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1379B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1058B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（626B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1206B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2161B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3937B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2410B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1561           3807-5439      5 條（2–6 內）  
s3                  8000         441           5291-7559      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3558          8009-11442      5 條（2–6 內）  
s6                 11000         626          7262-10374      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1206           1606-2294      3 條（2–6 內）  
s10                 5000        2161           1987-2839      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2410           2000-2590      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4886B；至少需散文≈40.11KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−46
−46%
−41.62
−30
−30%
−24.2%
−0.51%
0
0.19%
0.21%
0.23
0.34
0.36%
0.41
0.5
0.56
0.75
0.887
0.887%
0.90
0.908
1
1%
1.1
1.26
1.3
1.321
1.44
1.497
1.5%
1.5
1.54
1.7
2
02
2.09
2.1
2.27
2.79
3
03
3.1
3.1%
3.142
3.5%
3.5
3.58
3.6%
3.64
4%
4
04
4.28
4.3
4.72
4.74
4.75
4.77
4.95
5%
5
05
5.0
5.05
5.1
5.15
5.17
5.25
5.35
5.75
5.8
5.86
5.9
6%
06
6
6.192
6.2%
6.3
6.391
$6.40
6.5
6.50
7
7%
7.25
7.5
7.62
7.625
7.7
7.7%
08
8
8%
8.0
8.2
8.5%
8.567
8.8%
8.9
9
9.0%
09
9.53
9.83%
10%
10
10.37%
10.5
10.6
10.6%
11%
11
11.07
11.07%
11.3%
11.4
11.5
11.73%
11.78%
12
12.4%
12.5
12.5%
12.7%
13
13.2%
13.9%
14%
14
14.5
14.7%
15
15%
15.5
15.7%
16
17
17.2%
17.5%
17.9%
19%
20
20%
20.2
20.5%
21%
21.10%
22.5
22.6%
22.61%
22.91%
23
23.12
23.5
24
24%
24.2%
24.23%
24.86%
25%
25
25.16
26%
26
26.9
27
27.8
27.8%
28
29
30
30%
31
32.6%
33
33%
35%
35
35.8
38%
40%
41.6%
42
45
45%
48.1%
49
50
50%
52
55
55%
60
60%
64
65%
67%
68%
70
72.3%
76%
78%
80
80.6
84
85.6
87
87.55
88
90
95%
100%
100
104
107
$107
107.29
109.5
119.52
128.8
$130
130
150
150%
152.8
157.59
158.59
193
250
294
307.2
2024
2025
2026
2027
2028
2029
2030
2034
2036
14372
20261108
2,990
4,000
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
{"meta":{"ticker":"BWXT","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"BWX Technologies, Inc."},"oneliner":"美國海軍核反應爐的主要供應商，股價半年跌 41.6%、共識幾乎沒動；基本情境年報酬約一成，勝負看海軍新定價與首張新建訂單。","thesis":{"H":[{"id":"H1","text":"舊定價消化完後，政府部門靠特殊材料放量維持高個位數以上成長，利潤率守住 20%。","2y":"2027 全年政府部門營收年增 ≥8%，調整後 EBITDA 利潤率 ≥20%","5y":null,"10y":null,"threshold":"2027 年政府部門營收年增 ≥8% 且利潤率 ≥20%","source":"BWXT 季報與法說（2026-11-02 CFO 的 2027 初步展望）","drift_rule":"TTM 連兩季偏離 ≥5% 算削弱，連三季 ≥10% 算反轉"},{"id":"H2","text":"商業部門把新建機組需求轉成確定訂單，2030 年達管理層目標下緣。","2y":null,"5y":"FY2030 營收 ≥55 億美元、調整後 EBITDA ≥11 億美元、商業部門利潤率 ≥15%","10y":null,"threshold":"FY2030 營收 ≥55 億美元，調整後 EBITDA ≥11 億美元，商業部門利潤率 ≥15%","source":"BWXT 年報、季報與 2026-09-29 投資人日目標","drift_rule":"連四季偏離 ≥5% 算削弱，連六季 ≥10% 算反轉"},{"id":"H3","text":"先進核能與濃縮長成第二條獲利曲線，降低對海軍單一計畫的依賴。","2y":null,"5y":null,"10y":"2036 年前濃縮與先進核能合計占營收 ≥20%，微反應爐至少 3 座商業機組交付","threshold":"濃縮與先進核能合計占營收 ≥20%（現值事實表未涵蓋），商業微反應爐交付 ≥3 座","source":"BWXT 年報分部揭露、DOE／NNSA 公告、Janus 里程碑","drift_rule":"跨兩個年度未達階段里程碑算削弱，跨三個年度算反轉"}],"R":[{"id":"R1","text":"第四季獲利要跳一階。2026-08-03 CFO 說下半年約 55% 獲利落在第四季，以 3Q26 調整後 EPS 1.26 美元反推第四季約 1.54 美元；全年商業部門約 45% 成長也靠第四季。2026-11-02 CFO 說沒有特殊項目。","h_ref":"H1","clock":"⚡","threshold":"FY2026 調整後 EPS 低於 4.72 美元或自由現金流低於 3.5 億美元"},{"id":"R2","text":"美國政府占 FY2025 營收約 68%，下一份海軍多年期定價是最大的單一談判，新約若讓利會直接打到獲利核心。","h_ref":"H1","clock":"🔥","threshold":"政府部門利潤率連兩季低於 19%","evidence_refs":["customer_concentration_credit#0"]},{"id":"R3","text":"有機在手訂單連兩季下滑，新建訂單時程三場說法依序後移，2030 目標的後段因此更集中。","h_ref":"H2","clock":"🔥","threshold":"2027-06-30 前無美國新建訂單，或在手訂單連兩季低於 80 億美元"},{"id":"R4","text":"EO 14372 可能限制關鍵國防承包商的股息、回購、高管加薪與部分激勵指標，預期以新 DFARS 條款實施，會直接限制資本回饋。","h_ref":"H2","clock":"🔥","threshold":"DFARS 最終條款適用 BWXT 且股息或回購受限","evidence_refs":["regulatory_antitrust#1"]},{"id":"R5","text":"加拿大廠的重型零組件可能賣回美國，新增關稅會壓毛利，最終影響要看合約條款。這裡不預測關稅，只看商業部門利潤率是否吸收得住。","h_ref":"H2","clock":"🔥","threshold":"商業部門利潤率連兩季低於 12.5%","evidence_refs":["reg_tariff_export#0"]},{"id":"R6","text":"加拿大競爭局調查 Kinectrics 收購對核醫競爭的影響，2025-11 法院核准擴大調查令並納入 Novartis，2026 年未見結案。受影響範圍主要是年化營收約 1.3 億美元的醫療事業，出售完成後曝險縮小，但出售案本身可能受影響，結案日事實表未涵蓋。","h_ref":"H2","clock":"🐢","threshold":"競爭局提出挑戰，或醫療事業出售延到 2027-03-31 之後","evidence_refs":["regulatory_antitrust#0"]},{"id":"R7","text":"資本先於訂單。美國新廠不看確定訂單也要蓋（2026-11-02，CEO），金額未揭露，2027 自由現金流持平到小增。","h_ref":"H2","clock":"🔥","threshold":"資本支出超過營收 7% 且美國新建訂單仍為零"}],"single_thing":{"description":"下一份海軍多年期定價協議的利潤率低於舊約換新後水準，使政府部門調整後 EBITDA 利潤率跌破 19%。","why_fatal":"政府部門占 3Q26 分部調整後 EBITDA 78%，海軍占比事實表未涵蓋。以政府年營收約 26 億美元、稅率約兩成粗算，利潤率每少 1 個百分點，EPS 少約 0.23 美元，約 FY2026E 的 5%。由全年約 20.5% 跌破 19%，EPS 至少少 0.34 美元，倍數也會同步往下。新建訂單落空的影響分散在多張單與 2028 年後，不是最大單一敏感度。","if_happens":"減碼至半倉；若首張新建訂單也落空則清倉。","how_monitor":"海軍定價協議公告與金額（8-K、法說），每季政府部門調整後 EBITDA 利潤率。","probability":"12～24 個月約 15%"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.12,"peg_fy2":2.09,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":3.58,"FY2026E":4.75,"FY2027E":5.17,"FY2028E":5.86},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識，對應公司調整後 EPS 指引 4.72～4.77 美元；FY2025A 只有 GAAP 稀釋 EPS 3.58 美元，non-GAAP 基期事實表未涵蓋，所以三年年複合 17.9% 混口徑不採用，改用 FY2026E→FY2028E 的 11.07%。EPS 預估家數事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWXT_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"單一買方長約、核級資格、政府出資設施，加上尚未兌現的新建機組選擇權"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：CEO 說全球這類零組件產能仍不足（2026-11-02），Deloitte 與 Bain 指國防航太供應鏈緊張延續到 2027，但後兩者不是核能專屬資料。","bargaining":{"up":"上游目前無瓶頸，鋯管與大型鍛件取得順利，加拿大鋼鐵工人略缺（2026-08-03，CEO）。","down":"海軍是單一買方，新定價還在談；商業端由 Westinghouse 決定零組件分配，Doosan、IHI 會競爭（2026-11-02，CEO）。","geo":"加拿大 Cambridge 廠的產品可能賣回美國，受關稅影響；波蘭投資要有確定訂單才做。"},"profit_pool_dir":"事實表未涵蓋利潤池占比。方向上，政府段由舊定價轉向新定價與特殊材料，商業段仍在投入期。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM、滲透率與利潤池占比；逐字稿只有單機可觸及金額（CANDU 3.5～7 億美元、SMR 0.5～1 億美元），不足以組成市場表。"}},"moat":{"mechanism":"核級製造資格、政府授權設施與長期海軍合約。換供應商要重建設施與資格，實際轉換時間事實表未涵蓋。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：3Q26 政府部門利潤率 22.6%，Cambridge 產能增約 50%。定價面穩定：舊定價 2026 年底消化完，新多年期定價仍在談。兩者合併判穩定。客戶份額未見下滑，美國政府占營收由 76% 降到 68% 是商業段變大，不是份額流失。","peer_na_reason":"事實表只給同業利潤率，沒有 ROIC 與投入資本，無法算對最強同業的報酬差距，改看毛利率差與客戶份額。","threats":[{"level":"🟡","text":"TRISO-X 的 Oak Ridge TX-1 於 2026-02-13 取得 NRC 許可，DOE 也把 TRISO-X 與 Valar 納入燃料試點。攻擊範圍限於 TRISO，不碰海軍核心。BWXT 的 Lynchburg 線年產約兩百公斤，可至少擴到四倍（2026-11-02，CEO）。攻擊者資本量級事實表未涵蓋。","p":"40%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"AP1000 零組件要跟 Doosan、IHI 競爭，CEO 同時說全球產能不夠分。影響在價格，不在資格。","p":"60%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"10-K 提到現有技術可能被顛覆，醫用同位素也有替代技術。這是通用揭露，沒有具體對手；醫療事業出售後只留 20%，曝險變小。","p":"30%","evidence_refs":["competitive_share_entrants#2","substitute_technology#0"]}],"roic_durability":{"quadrant":"暫列低利益率×高周轉。營益率約 10%～14%，部分設施由政府出資；投入資本事實表未涵蓋，當期 ROIC 無法計算。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"海軍使用、NNSA 決策、國會付款，三個角色都成立，且屬既定計畫，預算延宕時約可拿前一年 95%（2026-11-02，CEO）。商業新建段的風險分配還沒談定，只算黃燈。"},{"item":"決策層級","level":"🟢","text":"海軍的替代性要看反應爐資格層，沒有第二來源揭露。商業端替代性高得多，Westinghouse 可在 BWXT、Doosan、IHI 之間分配。"},{"item":"價值鏈分配","level":"🟡","text":"舊定價換新讓政府利潤率由年初 19% 升到約 20.5%，但下一份多年期協議還沒簽。單一買方對固定成本結構很清楚，分配結果要看這次談判。"},{"item":"社會容忍度","level":"🟡","text":"獲利依賴聯邦預算與法規授權。EO 14372 可能限制關鍵國防承包商的股息、回購與高管薪酬指標，顯示政治上限已經出現；核能支持目前跨黨派。"}],"roiic":"約 14.7%（FY2022→FY2025 實現，含 Kinectrics）；管理層 2030 目標隱含超過 50%，不採用","reinvest_rate":"約 72.3%（同口徑含併購）；不含併購約 11%","endo_ceiling":10.6,"formula_note":"淨利增 0.908 億美元；投入＝FY2023～FY2025 淨利 8.567 億－FCF 7.625 億＋Kinectrics 5.25 億＝6.192 億美元。以淨利代 NOPAT，PCG 與其他併購未計，Kinectrics 併入時點事實表未涵蓋。2030 目標隱含值被政府出資與預收款墊高，所以只用已實現數字。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","BWXT":22.61,"LMT":11.73,"RTX":21.1,"NOC":20.02,"GD":15.42,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","BWXT":9.83,"LMT":11.78,"RTX":11.77,"NOC":10.61,"GD":10.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","BWXT":10.34,"LMT":10.59,"RTX":9.51,"NOC":8.78,"GD":10.22,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","BWXT":0.44,"LMT":null,"RTX":2.97,"NOC":null,"GD":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"LMT","gm":11.73,"om":11.78,"fcf_margin":10.59,"rd_intensity":null,"strategy_note":"毛利率約為 BWXT 一半，營益率較高，屬系統整合商，未列在 10-K 摘要的核部件對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"RTX","gm":21.1,"om":11.77,"fcf_margin":9.51,"rd_intensity":2.97,"strategy_note":"毛利率 21.10% 最接近 BWXT，研發密度高於 BWXT，業務重疊有限，只作國防利潤率參考。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"NOC","gm":20.02,"om":10.61,"fcf_margin":8.78,"rd_intensity":null,"strategy_note":"10-K 列為政府核部件對手，營益率略高於 BWXT，沒有證據顯示切入海軍反應爐。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"GD","gm":15.42,"om":10.37,"fcf_margin":10.22,"rd_intensity":null,"strategy_note":"未列在 10-K 摘要的核部件對手，FCF 利潤率與 BWXT 接近，只作現金轉換參考。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（特殊材料、海軍、商業零組件），定價次之（海軍舊約換新），併購第三（2024 年以來 15% 年複合裡有機 8.5%），回購不計。","runway_years":"滲透率事實表未涵蓋；海軍合約能見度據稱 6～8 年","runway_post_y5":"🟢","endo_ceiling_basis":"沿用護城河段的 14.7% × 72.3%＝10.6%。共識 FY2026E→FY2028E 年增 11.07% 略高於上限，缺口可歸因利潤率擴張。FY2025A 只有 GAAP 基期，混口徑的 17.9% 不採用。","segments":[{"item":"政府部門 3Q26","value":"營收 6.391 億美元，年增 3.6%；調整後 EBITDA 利潤率 22.6%"},{"item":"商業部門 3Q26","value":"營收 3.142 億美元，年增 25%，有機 15%；調整後 EBITDA 利潤率 13.2%"},{"item":"2027 初步展望","value":"政府營收與 EBITDA 高個位數至低雙位數；商業有機高個位數、報告數低個位數，利潤率增 50～100 基點"},{"item":"2030 架構","value":"營收 55～60 億美元，調整後 EBITDA 11～12 億美元，自由現金流 5.25～5.75 億美元"}],"decay_signals":[{"item":"毛利率連兩季年減","status":"亮","note":"季度資料事實表未涵蓋；年度 24.86%→24.23%→22.91%，TTM 22.61%，以年度趨勢計入。"},{"item":"核心市占縮減","status":"未亮","note":"海軍沒有第二來源揭露。"},{"item":"提價後銷量下滑","status":"未亮","note":"無此類資料。"},{"item":"EPS 年增高於營收逾 5 個百分點","status":"未亮","note":"FY2022～FY2025 EPS 11.3%、營收 12.7%。"},{"item":"FCF／淨利連兩年低於 0.75","status":"未亮","note":"FY2024 與 FY2025 皆約 0.90。"},{"item":"SBC／營收超過 5% 且上升","status":"未亮","note":"年化約 1%。"},{"item":"TAM 萎縮或被替代","status":"未亮","note":"有 TRISO 競爭，未見市場萎縮。"},{"item":"產業倍數三年系統性下移","status":"未亮","note":"同業倍數事實表未涵蓋，無法判定。"},{"item":"維護性資本支出占 FCF 超過 60%","status":"未亮","note":"營收 3.5%～4% 約 1.3～1.5 億美元，占 FCF 約四成。"},{"item":"停止投資新產能且收入下滑","status":"未亮","note":"仍在擴產。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"FY2023～FY2025 自由現金流合計","value":"7.62 億美元"},{"item":"2024 年以來營收年複合成長","value":"15%，其中有機 8.5%（2026-09-29，CEO）"},{"item":"Kinectrics 收購","value":"5.25 億美元"},{"item":"醫療事業出售","value":"對價 7.5 億美元，最高 8 億美元，保留 20%"},{"item":"到 2030 年可動用資金","value":"約 55 億美元，扣資本支出與股利後約 35 億美元"},{"item":"股息","value":"TTM 殖利率 0.887%，管理層稱維持並增加"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Kinectrics 與 PCG 各自的投入與獲利未揭露，單案已實現報酬事實表未涵蓋。含併購的整體粗估約 14.7%，不能代表單案。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2026 無計畫回購（2026-08-03，CFO），2027 只小幅回購抵銷稀釋（2026-11-02，CFO），回購均價事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 年化約 4,000 萬美元，除以市值 109.5 億美元約 0.36%，低於 1.5%。零息可轉債的潛在稀釋未計，轉換價事實表未涵蓋。","grade":"過"}]},"valuation":{"basis":"FY1 共識 EPS 前瞻本益比","tier":"核能國防核心供應商，事實表沒有同層級同業倍數","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或 EV 倍數，無法做倍數對照。終端倍數因此只錨公司自身現值與成長率。"},"fwd_pe":25.16,"peg":2.27,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 25.16 倍、PEG 2.27（25.16 ÷ 11.07），PEG 偏貴；Trailing P/E 在 4 個年度端點的 26.9 分位，基本情境年報酬約一成且不靠倍數擴張，結論為合理偏高。五年分位事實表未涵蓋。短期：FY2027E 5.15 × 25 倍＝128.8 美元，＋7.7%；三年：FY2029E 6.50 × 23.5 倍＝152.8 美元，＋27.8%。","upside_short_pct":7.7,"upside_mid_pct":27.8},"trap_analysis":{"verdict":"🟡","label":"核心穩，後段成長與利潤率尚未驗證"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"下一份海軍多年期定價協議還在談（2026-11-02，CEO），3Q26 政府部門占分部調整後 EBITDA 78%。","assumption":"新定價至少維持全年約 20.5% 的政府利潤率。","consequence":"五年後虧 50% 最可能的路徑：新定價讓利、新建訂單延到 2028 年後、美國新廠已開工。EPS 停在 4.3 美元、倍數 14 倍，股價約 60 美元。","ruling":"採納。這條與唯一致命點是同一件事，不另立，Bear 機率 30% 已反映。","watch":"新定價協議公告、政府部門季度利潤率","evidence_refs":["customer_concentration_credit#0"],"fact_refs":["f_kpi0_gaap","f_price_at_dd"]},{"view":"論點失敗","evidence":"股價 26 週跌 41.6%，共識幾乎沒動，事實表沒有記錄下跌的直接原因。","assumption":"跌幅主要是主題溢價退潮，不是獲利出事。","consequence":"若市場提前知道海軍或合約的壞消息，目前共識就是落後指標，基本情境會高估。","ruling":"無法反駁，只能用倉位處理。本次只買一個級距，下一筆要等基本面數字。","watch":"賣方下修 FY2027 EPS 的幅度、2026Q4 財報","fact_refs":["f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy3_pct"]},{"view":"論點成功但股東經濟變差","evidence":"2027 自由現金流持平到小增，獲利卻高個位數到低雙位數成長（2026-11-02，CFO）。美國新廠不看確定訂單也要蓋（2026-11-02，CEO），金額未揭露。資本支出說法由可能近 7%（2026-08-03）回到 5～6%（2026-09-29）。約 35 億美元可部署資金，策略長提到轉型型併購。EO 14372 可能限制股息與回購。","assumption":"新投資的增量報酬維持 15% 以上，多餘現金會回到股東手上。","consequence":"2030 目標達成，但股東拿到更多資本、更低報酬率與可轉債稀釋，每股價值成長低於 EBITDA 成長。","ruling":"部分採納。基本情境不計淨回購，終端倍數壓到 23 倍。","watch":"FCF／淨利低於 0.75、資本支出超過營收 7%、單筆併購超過市值 15%","evidence_refs":["regulatory_antitrust#1"],"fact_refs":["f_kpi3_fcf","f_ev_m"]},{"view":"價格已反映太多","evidence":"前瞻本益比 25.16 倍，同口徑 EPS 年增 11.07%，PEG 2.27。賣方平均目標價 193 美元是 7 月底的舊數字，現價已低於它 38%，不能當上檔依據。","assumption":"公司仍配得上較高倍數；同業現值倍數事實表未涵蓋。","consequence":"倍數若向 17 倍靠，就算 FY2027 達共識 5.17 美元，股價約 88 美元，下跌 26%。","ruling":"反駁一半。現價不便宜，但基本情境已用 23 倍終端，結論只到合理偏高。","watch":"前瞻本益比回到 30 倍以上時不追","fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"max_dd":{"lo":-46,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 157.59 → 本次 119.52（-24.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=157.59","side_b":"本次 price_at_dd=119.52","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場·條件式（爆發候選） → 本次 進場","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場·條件式（爆發候選）","side_b":"本次 dca_verdict=進場","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份裁決：估值 🔴→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 157.59 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 157.59 美元：Bull 價 307.2、Bear 價 104，五年期望值 +32.6%，基準年化 6.2%，不對稱比 2.79","side_b":"本次情境、股價仍用 157.59 美元：Bull 價 294、Bear 價 87.55，五年期望值 +12.4%，基準年化 3.1%，不對稱比 1.3","ruling":"先換情境、股價不動：五年期望值少 20.2 個百分點，基準年化少 3.1 個百分點。不對稱比由 2.79 變為 1.3。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 157.59 美元：五年期望值 +12.4%，基準年化 3.1%，不對稱比 1.3","side_b":"本次情境、股價 119.52 美元：五年期望值 +48.1%，基準年化 9.0%，不對稱比 3.64","ruling":"再換股價、情境不動：起點價下跌 24.2%，五年期望值多 35.8 個百分點，基準年化多 5.9 個百分點，不對稱比由 1.3 升到 3.64。合計五年期望值比前份多 15.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與進場結論","cause":"價格變動","prior_field":["val"],"side_a":"2026-09-05：股價 157.59 美元，前瞻本益比約 33 倍，估值偏貴，條件式進場。","side_b":"2026-11-08：股價 119.52 美元，前瞻本益比 25.16 倍，FY1 共識只由 4.74 升到 4.75 美元，估值轉為合理偏高。","ruling":"可調和。變動來自股價，不是獲利數字。下跌已打到前份的價格條件，進場結論維持條件式，不因跌幅放大倉位。","evidence_level":"實測數字","settle_metric":"前瞻本益比與 FY2027 共識 EPS","if_then":["若股價反彈到 150 美元以上而政府部門與訂單都還沒驗證，不追","若股價再跌而 FY2027 共識 EPS 維持 5.0 美元以上，分批反買"]},{"axis":"情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 與 Bear 各 25%，最大回撤 −50%。","side_b":"本次：Bull 20%、Bear 30%，從現價起算最大回撤 −30%～−46%。","ruling":"可調和。本次用已實現數字算內生上限 10.6%，共識與基本情境都略高，Bear 機率拉到 30%。Bull 降到 20%，因為首張新建訂單還沒落地。前份回撤的起算口徑摘要未載，本次明確從現價起算。","evidence_level":"推導","settle_metric":"FY2027 EPS 與政府部門利潤率","if_then":["若 2027 全年 EPS 低於 4.95 美元，Bear 機率上調到 40%，停止加碼","若首張新建訂單落地且政府利潤率 ≥20%，Bull 機率回到 25%，分批加碼"]},{"axis":"品質、陷阱、護城河與跑道結論","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：評等 B、陷阱風險中等、護城河持平、五年後跑道寬、品質複利成長、未標循環位置。","side_b":"本次六項結論不變。新增證據有投資人日 2030 目標、2027 初步展望、Janus 與 Antares 合約，以及有機在手訂單連兩季下滑。","ruling":"可調和。正反證據互抵，結論不動。合約勝利強化第二條曲線，訂單下滑與利潤率未驗證壓住上調空間。","evidence_level":"公司揭露","settle_metric":"海軍新定價與首張新建訂單","if_then":["若海軍新定價使政府利潤率 ≥21%，護城河定價分上調，分批加碼","若海軍新定價使政府利潤率低於 19%，護城河轉為縮減，減碼至半倉"],"evidence_refs":["end_markets#0","channel_business_model_shift#0"]},{"axis":"加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"第二階 1/3：回檔 ≤$130（前瞻本益比 ≤27 倍）或投資人日隱含 FY2028 EPS ≥$6.40／商用利潤率目標 ≥15%；第三階：Q3 政府部門年增 ≥5% 且商用利潤率 ≥12.5%","side_b":"第三階 1/3：4Q26 政府部門年增 ≥8% 且利潤率 ≥20%，或 2027-06-30 前取得首張美國新建訂單；價格條件 ≤$107（前瞻約 22.5 倍）","ruling":"前份加碼第二階已發火：現價 119.52 美元低於 130 美元，前瞻 25.16 倍低於 27 倍，商業利潤率 2030 目標為高十位數也過 15%。第三階沒過：3Q26 政府部門年增 3.6%，低於 5%；商業利潤率 13.2% 過關，但兩項要同時成立。新門檻把政府年增拉到 8%，因為 2027 初步展望由高個位數起跳。","evidence_level":"實測數字","settle_metric":"2026Q4 政府部門年增與利潤率","if_then":["若 2026Q4 條件成立，加碼第三個 1/3","若 2026Q4 政府部門年增低於 5%，停止加碼到海軍新定價公布"]},{"axis":"Single Thing 前份缺值","cause":"方法變動","prior_field":["single_thing"],"side_a":"null（前份摘要未留存唯一致命點）","side_b":"下一份海軍多年期定價協議的利潤率低於舊約換新後水準，使政府部門調整後 EBITDA 利潤率跌破 19%。","ruling":"前份摘要沒有這一欄，本次依單一敏感度最大項重新選定。","evidence_level":"推導","settle_metric":"海軍新定價協議與政府部門利潤率","if_then":["若政府部門利潤率連兩季低於 19%，減碼至半倉"]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"null（前份摘要未留存停損指標）","side_b":"政府部門利潤率連兩季低於 19% 減碼；在手訂單連兩季低於 80 億美元減碼；海軍引入第二來源清倉。","ruling":"前份摘要沒有這一欄，本次新訂，門檻都能從季報直接驗證。","evidence_level":"推導","settle_metric":"季報揭露的政府部門利潤率與在手訂單","if_then":["若海軍確認引入第二來源，清倉"]},{"axis":"新建機組訂單時程滑動","side_a":"2026-08-03 CEO：年底前有機會拿到至少一張新建設備訂單，並預期下半年會有一張。2026-09-29 MacQuarrie：今年稍晚或 2027 年初。","side_b":"2026-11-02 CEO：年底前仍有可能，但不晚於 2027 年上半年；若落空，2030 目標仍有多條路。","ruling":"可調和，屬時點後移。三場說法依序往後，基本情境採較晚時點。CFO 說新建拐點在 2028～2029 年，晚半年對 FY2027 影響小，對 FY2029 之後影響大。決勝數據今天不存在，2027-06-30 前不可裁決。","evidence_level":"管理層說法","settle_metric":"2027-06-30 前首張美國新建機組零組件訂單","if_then":["若 2027-06-30 前拿到訂單，加碼第三個 1/3","若 2027-06-30 前仍無訂單，停止加碼，Bear 機率上調到 35%"],"evidence_refs":["end_markets#3"]},{"axis":"政府部門利潤率是結構性還是峰值","side_a":"2026-11-02 CFO：海軍業務效率大幅提升，舊定價逐步消化，3Q26 政府部門利潤率 22.6%。","side_b":"全年指引約 20.5%，2027 EBITDA 成長與營收大致同步（2026-11-02，CFO）；原預期 2027 的表現已提前出現（2026-08-03，CFO）。投資人日 CFO 給 2030 年約 20% 合併利潤率，CEO 同場卻說先不下定論（2026-09-29，摘錄無完整上下文）。","ruling":"拆三塊：年初 19% 到 20.5% 是舊定價換新，算結構性；20.5% 到 22.6% 的 2.1 個百分點含權益法收益與專案超額，當殘差，不進基本情境，反映在 Bear 機率。CFO 把政府營收偏低歸因於成本表現好使完工比例法認列較少，這點不採信也不否定，先標未證。","evidence_level":"公司揭露","settle_metric":"2026Q4 與 2027Q1 政府部門營收年增","if_then":["若 2026Q4 與 2027Q1 政府部門營收年增連兩季低於 8%，判定會計歸因不成立，停止加碼","若連兩季利潤率 ≥21% 且營收年增 ≥8%，分批加碼"]},{"axis":"需求湧現與有機在手訂單","side_a":"2026-11-02 CEO：需求環境異常強，正把機會轉成有意義的新訂單，涓流將成洪流。","side_b":"在手訂單 87 億（1Q26）→84 億（2Q26）→85.6 億美元（3Q26）。3Q26 含併購帶進的約 5 億美元，扣掉約 80.6 億美元，有機連兩季下滑；3Q26 接單出貨比 0.56 倍。","ruling":"可調和，但管理層沒有主動講這件事。大型多年期合約本來就不連續，2Q26 底近 12 個月接單出貨比 1.7 倍就是例子。近期訊號採信在手訂單這一側，需求說法要用海軍定價協議與首張新建訂單驗證。","evidence_level":"公司揭露","settle_metric":"期末在手訂單與季度接單出貨比","if_then":["若連兩季在手訂單低於 80 億美元，減碼至半倉","若海軍定價協議入帳使在手訂單回到 90 億美元以上，分批加碼"],"evidence_refs":["end_markets#2","supply_demand_durability#3"]},{"axis":"股價與共識背離（現在就賣的最強論證）","side_a":"股價 26 週跌 41.6%，低於 52 週與 104 週均線。","side_b":"FY1 共識近三個月 ＋0.21%，FY2 ＋0.19%，FY3 −0.51%，2027 初步展望微升，Fitch 給投資等級。","ruling":"可調和，方向相反但差在倍數。現在就賣的最強論證：25 倍前瞻本益比對應約 11% 成長，PEG 2.27 不便宜；FY3 共識已開始下修；事實表沒有下跌原因，市場可能定價了我們沒看到的事。反駁：超過一半成長來自既有核心（2026-09-29，CFO），管理層只計入小幅新建訂單（2026-11-02，CEO）。採基本面這一側，但只買一個級距。","evidence_level":"實測數字＋管理層說法","settle_metric":"週收盤相對 250 週線、政府部門利潤率、FY2027 共識","if_then":["若週收盤跌破 250 週線 107.29 美元且政府部門利潤率低於 20%，趨勢訊號證實為對，停止加碼到 2027-06-30","若跌破 250 週線而政府部門利潤率 ≥20%、共識未下修，分批反買","若未驗證就反彈回 104 週線 158.59 美元，不追"]},{"axis":"產業態勢三軸","side_a":"競爭：海軍核心沒有第二來源揭露；新領域 TRISO-X 已取得 NRC 許可，AP1000 零組件要和 Doosan、IHI 競爭。","side_b":"結構：全球重型零組件產能仍緊（2026-11-02，CEO），主權資金與跨黨派支持。其他：EO 14372、關稅與加拿大競爭審查。","ruling":"裁決：結構性轉好中。依據是已簽的特殊材料合約與 Cambridge 擴產約 50%，競爭惡化只出現在尚未貢獻獲利的新領域。","evidence_level":"公司揭露＋二手資料","settle_metric":"首張新建訂單的價格與利潤率","if_then":["若商業部門利潤率連兩季低於 12.5%，停止加碼"],"evidence_refs":["substitute_technology#1","competitive_share_entrants#0","supply_demand_durability#0"]}],"triggers":[{"n":1,"text":"2026Q4 政府部門營收年增至少 8%、利潤率至少 20%，才買第三個 1/3。","type":"加碼","maps_to":"H1","metric":"政府部門季度營收年增與調整後 EBITDA 利潤率","threshold":"營收年增 ≥8% 且利潤率 ≥20%","action":"加碼第三個 1/3","source_freq":"季報，每季","date":"2027-Q1"},{"n":2,"text":"股價跌到 107 美元以下，但政府利潤率與共識都沒壞，分批反買。","type":"估值rearm","maps_to":"H1","metric":"股價、政府部門利潤率、FY2027 共識 EPS","threshold":"≤107 美元，利潤率 ≥20%，FY2027 共識 ≥5.0 美元","action":"分批反買","source_freq":"每週","date":null},{"n":3,"text":"海軍新定價簽定後，政府部門利潤率連兩季低於 19%。","type":"Single Thing","maps_to":"R2","metric":"政府部門調整後 EBITDA 利潤率","threshold":"連兩季低於 19%","action":"減碼至半倉；若首張新建訂單也落空則清倉","source_freq":"季報與 8-K","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":4,"text":"2027-06-30 前沒有首張美國新建機組零組件訂單。","type":"假設驗證","maps_to":"H2","metric":"美國新建機組訂單","threshold":"2027-06-30 前為零","action":"停止加碼","source_freq":"法說與新聞稿","date":"2027-06-30"},{"n":5,"text":"第四季沒有如期跳升。","type":"風險","maps_to":"R1","metric":"FY2026 調整後 EPS 與自由現金流","threshold":"EPS 低於 4.72 美元或自由現金流低於 3.5 億美元","action":"停止加碼","source_freq":"季報","date":"2027-Q1"},{"n":6,"text":"在手訂單連兩季低於 80 億美元。","type":"減碼","maps_to":"R3","metric":"期末在手訂單","threshold":"連兩季低於 80 億美元","action":"減碼至半倉","source_freq":"季報","date":null},{"n":7,"text":"EO 14372 的 DFARS 條款定案，且適用 BWXT 的合約。","type":"風險","maps_to":"R4","metric":"DFARS 最終條款與公司揭露","threshold":"股息或回購受限","action":"停止加碼","source_freq":"聯邦公報與 10-Q","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":8,"text":"關稅或擴產成本吸收失敗。","type":"風險","maps_to":"R5","metric":"商業部門調整後 EBITDA 利潤率","threshold":"連兩季低於 12.5%","action":"停止加碼","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#0"]},{"n":9,"text":"海軍確認引入第二來源。","type":"清倉","maps_to":"R2","metric":"海軍反應爐供應商結構","threshold":"出現第二來源","action":"清倉","source_freq":"10-K 與 NNSA 公告","date":null},{"n":10,"text":"首張新建訂單期限到期，整份論點重看一次。","type":"複審日期","maps_to":"H2","metric":"訂單、政府利潤率、在手訂單","threshold":"到期日","action":"重跑完整研究","source_freq":"一次性","date":"2027-06-30"}],"kill_metrics":[{"metric":"政府部門調整後 EBITDA 利潤率","bear_threshold":"連兩季低於 19%","window":"2027-03 至 2028-03 各季","source":"BWXT 季報與法說","last_status":"ok"},{"metric":"期末在手訂單","bear_threshold":"連兩季低於 80 億美元","window":"2027 全年各季","source":"BWXT 季報","last_status":"warning"},{"metric":"首張美國新建機組零組件訂單","bear_threshold":"2027-06-30 前仍為零","window":"至 2027-06-30","source":"BWXT 法說與新聞稿","last_status":"warning"},{"metric":"FY2027 調整後 EPS","bear_threshold":"低於 4.95 美元","window":"FY2027","source":"BWXT 年度財報","last_status":"unknown"},{"metric":"商業部門調整後 EBITDA 利潤率","bear_threshold":"連兩季低於 12.5%","window":"2027 全年各季","source":"BWXT 季報","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=FY1 共識近三個月只動 ＋0.21%，2027 初步展望反而微升，跌幅幾乎全來自倍數。市場把新建訂單延後當成 2030 目標落空，但管理層只計入小幅新建訂單，超過一半成長來自既有核心。下跌的直接原因事實表未涵蓋。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-41.62, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"requires_critic":[],"rearm_trigger":"第三階 1/3：4Q26 政府部門年增 ≥8% 且利潤率 ≥20%，或 2027-06-30 前取得首張美國新建訂單；價格條件 ≤$107（前瞻約 22.5 倍）","exec_line":"現價符合前份第二階條件，可買第二個 1/3；第三個 1/3 依上述條件。週收盤跌破 250 週線且政府利潤率低於 20% 時停止加碼。"},"reasoning":{"industry":"3Q26 營收 9.53 億美元，政府部門 6.391 億美元（67%），商業部門 3.142 億美元（33%）；FY2025 美國政府占合併營收約 68%。利潤更集中：3Q26 分部調整後 EBITDA 政府 1.44 億美元、商業 0.41 億美元，政府占 78%。TTM 毛利率 22.61%，3Q26 GAAP 營業利益 1.321 億美元、non-GAAP 1.497 億美元，營益率 13.9%／15.7%。在手訂單 85.6 億美元，其中約 5 億美元是 7 月併入的 PCG。單點依賴：美國政府單一客戶超過 40%，它同時是護城河來源與最大集中風險。產業時鐘在擴張期，依據是全球重型零組件產能仍緊（2026-11-02，CEO）與已簽的特殊材料合約，不是股價。反例：新建機組需求至今沒有變成美國訂單，擴張期的商業段仍是預期。","moat":"海軍反應爐沒有揭露第二來源，法規與資本門檻把競爭者擋在外面。事實表沒有同業投入資本，方向改用客戶份額判斷。毛利率 22.61% 高於四家國防同業（11.73%～21.10%），TTM 營益率 9.83% 卻低於四家（10.37%～11.78%）；3Q26 公司口徑 GAAP 營益率為 13.9%，差距可能來自資料商未把權益法收益計入營業利益，事實表無法確認。執行力給 8 分，依據是 3Q26 政府部門利潤率 22.6%、Cambridge 擴產略低於預算完工。定價力給 7 分，因為買方單一、新定價協議還沒簽，商業端 CEO 也說一定有價格壓力（2026-11-02）。反例：海軍若引入第二來源或新約大幅讓利，這個判斷就錯。","growth":"成長以量為主。共識 EPS 由 FY2026E 4.75 美元到 FY2028E 5.86 美元，年增 11.07%；FY2027 只增 8.8%，部分因年底出售醫療事業。內生上限 10.6%，缺口 0.5 個百分點，歸因利潤率擴張（2026-09-29，CFO 給合併 EBITDA 利潤率 17.5%→約 20%）。第一條曲線是海軍 4～6% 年複合；第二條是特殊材料 24% 年複合，HPDU 16 億美元與濃縮 15 億美元合約已簽；第三條是新建機組、Janus 與 TRISO，還沒變成大額訂單。超過一半成長來自既有核心（2026-09-29，CFO），戰艦未列入預測。反例：特殊材料長期利潤率 Miller 未給數字，若明顯低於政府平均，量長了獲利不一定長。","governance":"FY2024 與 FY2025 的 FCF／淨利都約 0.90。前九個月 SBC 2,990 萬美元，年化約占營收 1%。現金去向四分事實表未涵蓋，只有片段：Kinectrics 5.25 億美元，PCG 金額未見，醫療事業以 7.5～8 億美元出售並保留 20%。2026 無回購計畫，2027 小幅回購只抵銷稀釋（2026-11-02，CFO）。2025-11 發 12.5 億美元零息可轉債，2026-11-04 發 5 億美元 2034 優先債並收購舊票據，目前淨負債約 14.5 億美元。反例：約 35 億美元可部署資金若用在大型併購，這個判斷要重寫。","valuation":"要賺 10% 年報酬，FY2031 EPS 要到約 8.0 美元（年增 11%）。管理層 2030 調整後 EBITDA 中點 11.5 億美元，按 2026 年淨利對 EBITDA 約 65% 換算，FY2030 EPS 約 8.2 美元，現價要求的進度比目標晚一年以上。FY2028 共識 5.86 美元有合約支撐，FY2029 之後要靠海軍定價與新建訂單。同業倍數事實表未涵蓋，這是本次估值最大限制；真正的五年分位也沒有，只有 4 個年度端點分位。反例：倍數若向 17 倍靠，EPS 達標股價仍會跌。","premortem":"管理層迴避的題目集中在單位經濟：Janus 經濟效益（2026-08-03，CEO）、TRISO 每公斤成本（2026-09-29，Miller）、特殊材料長期利潤率（2026-09-29，Miller）、Westinghouse 訂單金額（2026-09-29，CFO）。這四項正是第二條曲線的獲利依據，所以基本情境不計入超額利潤率。歷史最大回撤與空方報告事實表未涵蓋；訴訟、臨床、召回、SEC 調查四項搜尋無結果。"},"plain":{"six":{"how_it_makes_money":"賺的主要是美國政府的錢，錢卡在核級製造資格與設施這一節點。","moat":"護城河穩定：海軍核心地位沒變，新領域的競爭比舊領域多。","growth":"跑道寬，但五年後那段要靠還沒簽的訂單。","capital":"現金轉換好，併購報酬還看不到，回購只抵銷稀釋。","valuation":"現價要求 FY2031 EPS 到約 8.0 美元、終端 23 倍；我信前半，後半要看海軍定價。","how_wrong":"最可能看錯三處：海軍新定價、新建訂單時程、股價下跌的真正原因。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"FY1 共識近三個月只動 ＋0.21%，2027 初步展望反而微升，跌幅幾乎全來自倍數。市場把新建訂單延後當成 2030 目標落空，但管理層只計入小幅新建訂單，超過一半成長來自既有核心。下跌的直接原因事實表未涵蓋。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":119.52,"week26_return_pct":-41.62,"consensus_rev_3m_pct":0.21,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026E EPS 含年底出售的醫療事業，年化營收約 1.3 億美元，占比小，分母不是主要爭點。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"capacity","event":"美國商業重型零組件新廠最終投資決定","impact":"中","watch":"投資金額，是否推高資本支出超過營收 6%"},{"date":"2026-12","date_precision":"month","type":"product","event":"離心機原型機測試","impact":"中","watch":"是否如期運轉，LEU 與 HALEU 是否納入範圍"},{"date":"2026-12","date_precision":"month","type":"other","event":"醫療事業出售完成","impact":"中","watch":"實收金額與資金用途"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"2026Q4 財報與 2027 正式財測","impact":"高","watch":"政府部門年增與利潤率，第四季 EPS 是否達約 1.54 美元"},{"date":"2027-06","date_precision":"month","type":"other","event":"管理層所說首張美國新建機組訂單的最晚窗口","impact":"高","watch":"機組類型與單筆金額"},{"date":"2027-06","date_precision":"month","type":"other","event":"Y-12 鋰處理設施下一階段選商","impact":"低","watch":"是否入選"},{"date":null,"date_precision":null,"type":"other","event":"下一份海軍多年期定價協議","impact":"高","watch":"總金額與政府部門利潤率"}],"_projected_from":"v19"}
```
