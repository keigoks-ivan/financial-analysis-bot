你是 stock-analyst v20 的**散文層（prose）agent**，標的 CAMT（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：CAMT　日期：2026-11-08　archetype：None　前份裁決：2026-09-06　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1437B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（666B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（870B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1222B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（751B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（674B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（795B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2195B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3670B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2725B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1437           3894-5563      5 條（2–6 內）  
s3                  8000         666           5134-7334      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2843          8510-12157      5 條（2–6 內）  
s6                 11000         674          7228-10326      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         795           1893-2705      5 條（2–6 內）  
s10                 5000        2195           1963-2805      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2725           2000-2275      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4444B；至少需散文≈40.56KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−55%
−52.78
−37%
−35%
−35
−33.4%
−20%
0
0.33
0.50%
0.55%
0.62
0.7
0.78
0.8
0.90
0.94
0.96
0.97
0.99
1
1.04
1.08
1.17
1.39
1.4
1.5
1.5%
1.58
1.613
1.72%
1.9
2%
2
02
2.51
2.59
2.6
2.6%
2.75
2.8%
3
3.1
3.10
3.21
3.5%
3.5
3.60
3.6
3.63
04
4%
4
4.1
4.15
4.3
4.43
4.95
4.96
5
05
5%
5.09
5.4
5.9
5.92
6%
6
6.07
6.1
6.6
6.89
6.90
6.9
7
7%
7.2
7.35
7.5
08
8
8.12
8.2
8.30
8.3
8.33
8.5
8.55
8.7%
8.7
8.77
8.771
09
9
9.34
9.5
10
10%
11
11%
11.3%
11.4
11.44
12
12%
12.2
12.2%
13.0%
13
14%
14
15
15%
16.3%
17
17.5
17.5%
18
18.7%
19%
19
19.07
20%
20
20.74%
22
23.15%
23.3
24%
24
25
25%
25.5
26
26.74
26.9
27.7%
28%
29.5%
29.8
30
30%
30.21
31%
32%
33%
33.4%
34%
34.8%
35%
36%
36.48
40%
40.2%
41%
41.5
42%
42
42.2
42.2%
42.8%
44.2
45%
45
45.35
46.5
46.81%
48%
49
49%
50%
50.0%
50.03%
50.46%
51%
51.1%
51.6
52
52%
52.5%
52.78%
53%
54%
55%
55.8
56%
56.7
57%
59.7
60
61.5
63
69.7%
70
74
77.86
78
$78
80
80%
85%
86.4
95%
97.05
100%
100
$100
104
108.9
115.43
125
$125
138
145.72
150%
$158
$165
171
187.58
220
250
286
330
365
570
$720
$800
2026
2027
2028
2029
2030
20261108
1,150
2,280
2,810
4,000
4,100
5,150
6,130
7,110
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
{"meta":{"ticker":"CAMT","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Camtek Ltd."},"oneliner":"股價半年跌 53%、共識沒動，FY2027 本益比 19 倍買的是 8 億美元展望能否兌現；管理層不拆在手訂單，毛利率也沒做到 8 月的說法，下一個驗證點是 2026 Q4 財報。","thesis":{"H":[{"id":"H1","text":"FY2027 營收達到管理層 8 億美元以上展望，非 GAAP 營益率回到 31% 以上。","2y":"FY2027 營收 ≥ 8 億美元、非 GAAP 營益率 ≥ 31%、非 GAAP EPS ≥ 4.95 美元","5y":null,"10y":null,"threshold":"營收 ≥ 8 億美元且非 GAAP 營益率 ≥ 31%","source":"公司季度新聞稿與法說","drift_rule":"TTM 營收或 EPS 較路徑偏離連 2 季 ≥ 5% 視為削弱，連 3 季 ≥ 10% 視為反轉"},{"id":"H2","text":"先進封裝 2D 檢測與 3D 凸塊量測的份額守住，毛利率走向 54% 以上。","2y":null,"5y":"FY2029 非 GAAP 毛利率 ≥ 54%，OSAT 仍占訂單 45% 以上","10y":null,"threshold":"OSAT 占訂單 ≥ 45%、台灣 OSAT 份額 ≥ 50%、FY2029 非 GAAP 毛利率 ≥ 54%","source":"法說訂單拆分、Yole 年度報告、季度毛利率","drift_rule":"連 4 季偏離 ≥ 5% 視為削弱，連 6 季偏離 ≥ 10% 視為反轉"},{"id":"H3","text":"封裝複雜度讓檢測步驟持續增加，軟體與服務、混合鍵合、光子成為第二條曲線。","2y":null,"5y":null,"10y":"軟體、服務與新製程合計占營收 ≥ 25%","threshold":"FY2029 軟體加服務 ≥ 1.4 億美元；FY2030 混合鍵合加光子占訂單 ≥ 10%","source":"投資人日、法說、年報","drift_rule":"跨 2 個年度低於路徑視為削弱，跨 3 個年度視為反轉"}],"R":[{"id":"R1","text":"毛利率回升落空：零組件與匯率壓力延續，調價轉嫁不足。","h_ref":"H1","clock":"⚡","threshold":"2027 Q1 與 Q2 非 GAAP 毛利率連 2 季低於 51%","evidence_refs":[]},{"id":"R2","text":"2027 檔期訂單遞延或重複下單，AI 資本支出進入消化期；少數 HPC 與 HBM 客戶減少支出時衝擊集中。","h_ref":"H1","clock":"🔥","threshold":"2027 展望低於 7.2 億美元，或存貨成長率高於營收成長率 10 個百分點連 2 季","evidence_refs":["supply_demand_durability#2"]},{"id":"R3","text":"大型同業進入 OSAT 2D 檢測，本土業者攻低階，份額與價格同時受壓。","h_ref":"H2","clock":"🔥","threshold":"OSAT 占訂單低於 45%，或管理層不再重申台灣 OSAT 份額至少 50%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"id":"R4","text":"中國約占營收 45%，出口管制或本土替代造成需求下滑。","h_ref":"H1","clock":"🔥","threshold":"中國營收年減逾 20%，或美方新規直接涵蓋檢測量測機台","evidence_refs":["customer_concentration_credit#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R5","text":"X-ray 等非光學路線在混合鍵合取得主要地位，第二條曲線被截斷。","h_ref":"H3","clock":"🐢","threshold":"主要客戶以非光學方案作為混合鍵合主要檢測，或 FY2030 混合鍵合加光子占訂單低於 10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R6","text":"關鍵零組件短缺超過管理層估的 3～6 個月，影響交期。","h_ref":"H1","clock":"⚡","threshold":"2027 年 5 月財報仍提短缺，或任一季錯過交期","evidence_refs":["geo_supply_chain#1"]}],"single_thing":{"description":"FY2027 營收展望被下修到 7.2 億美元以下（較 8 億美元少 10%）。","why_fatal":"這是盈餘最敏感的一項：營收少 10%，毛利約少 4,100 萬美元，費用不動時 EPS 約少 0.7 美元，約 14%；毛利率少 1 個百分點只影響約 2.8%。下修同時證明檔期訂單不夠硬，12 億美元目標與目前本益比都會被一起重估。","if_happens":"清倉，等訂單拆分與需求重新驗證後再重做判斷。","how_monitor":"每季財報與法說的 2027 展望、預收款與合約負債、存貨與營收成長率差、主要客戶資本支出。","probability":"20%（12～24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":19.07,"peg_fy2":1.17,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.04,"FY2026E":3.63,"FY2027E":5.09,"FY2028E":5.92},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin 共識，依季度非 GAAP 稀釋 EPS（Q2 0.78、Q3 0.99 美元）判斷為非 GAAP；FY2025A 1.04 美元是 GAAP，事實表沒有非 GAAP 值，兩者口徑不同，不可直接計算成長率。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAMT_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"FY2022～FY2025 營收 3.21 億增至 4.96 億美元，只有 FY2023 小跌 1.72%，毛利率 46.81%～50.46%；盈利能力穩，但 2027 成長高度綁 AI 封裝資本支出，帶循環性。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久，但 2027 檔期搶訂帶週期成分：SEMI 2026 年中預測設備銷售到 2028 年仍成長，CFO 在 2026-10-14 投資人日也提醒可能進入資本支出消化期；這是 Bear 機率取 30% 的依據之一。","bargaining":{"up":"通用零組件（記憶體、CPU、搬運機構件）短缺漲價，Q3 已壓到毛利率；COO 說多數有雙來源，單一來源比例事實表未涵蓋。","down":"客戶分散，FY2025 最大客戶 11%；COO 說客戶已理解因零組件調價，幅度未揭露，能否轉嫁要看 2027 毛利率。","geo":"亞洲占 Q3 營收 95%，中國約 45%；製造與研發集中在以色列，歐洲擴產作對沖。"},"profit_pool_dir":"利潤往 AI 先進封裝移動；5 年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"可服務市場（2027）","value":"20 億美元以上，較目前增約 5 億美元（二手摘要，管理層口徑）"},{"item":"可服務市場（2030）","value":"約 60 億美元（2026-10-14 投資人日，COO），未經第三方驗證"},{"item":"CAMT 滲透率（2027）","value":"8 億÷20 億＝約 40%"},{"item":"CAMT 滲透率（目標口徑）","value":"12 億（約 2029 年）÷60 億（2030 年）＝約 20%，年份不完全對齊，且前提是新增市場都打得進去"},{"item":"營業利益池 5 年占比變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"先進封裝專用檢測與量測機台＋約 4,000 台裝機基礎＋放量期的認證黏著度","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力穩定：Q3 營收高於指引，Hawk 與 Eagle G5 占系統營收升到約 57%，過去 17 次指引調整有 13 次上調。定價力穩定但未獲證實：調價才開始，Q3 毛利率 51.1% 還低於預期。競爭屬客群範圍開始被多家供應，不是方向受損；沒有來源指出最大客戶份額下滑。","peer_na_reason":"事實表同業對照只有利潤率與研發密度，沒有 ROIC 與投入資本，改用毛利率與營業利益率比較。","threats":[{"level":"🟡","text":"大型同業切入 OSAT 的 2D 檢測。2D 占 2026 年出貨約 85%，對手已在同一客戶拿到訂單；目前是單點競爭，若第二家主要 OSAT 也開始多家採購，升為生態攻擊。","p":"40%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"中國本土業者以低價攻低階市場。2026-10-14 CEO 說本地競爭增加，2026-11-04 管理層說看不到威脅，並稱中國 2027 訂單至少持平。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"X-ray CT 等路線切入混合鍵合檢測，加上技術快速變動可能造成存貨沖銷。證據只有一份會議摘要，混合鍵合 2028 後才有規模，目前不構成架構替代。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"無法判定：事實表未涵蓋投入資本","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是封裝產線工程師，決策者是良率與製程主管，付款者是 OSAT 與晶片廠的資本支出預算。良率損失代價高，屬於需要而非想要，但機台可以延後買：COO 2026-11-04 說有些客戶提前下單只是為了確保檔期。需求持久，時點會波動。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一製程步驟衡量。COO 2026-11-04 說部分客戶在快速放量時不願換機重新認證，這是轉換成本的證據；但同一 OSAT 已向對手下單，代表新增步驟可以多家供應。重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"毛利率 50.03% 低於 NVMI 與 KLAC，上游零組件漲價先吃到毛利，調價要到 2027 才見效。客戶以大型 OSAT 為主，能否多拿價值取決於新機種帶來的新功能。"},{"item":"社會容忍度","level":"🟢","text":"這是企業資本財，沒有社會定價壓力；政治限制來自出口管制，已列入中國風險處理。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。缺投入資本、折舊與營運資金變動，不自行推估；Q3 營業現金流 7,110 萬美元，現金季增 6,130 萬美元，顯示資本需求低，但不足以算出上界。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","CAMT":50.03,"ONTO":50.36,"NVMI":57.38,"KLAC":61.47,"unit":"%"},{"metric":"營業利益率","CAMT":23.15,"ONTO":13.81,"NVMI":30.04,"KLAC":42.64,"unit":"%"},{"metric":"FCF 利潤率","CAMT":null,"ONTO":22.54,"NVMI":25.44,"KLAC":27.83,"unit":"%"},{"metric":"研發密度","CAMT":11.39,"ONTO":12.73,"NVMI":15.64,"KLAC":10.8,"unit":"%"}],"competitors":[{"name":"ONTO","gm":50.36,"om":13.81,"fcf_margin":22.54,"rd_intensity":12.73,"strategy_note":"毛利率與 CAMT 幾乎相同，營益率低 9 個百分點，是量測與檢測的直接對手；是否為投資人日提到的 OSAT 得標者，事實表未涵蓋。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"NVMI","gm":57.38,"om":30.04,"fcf_margin":25.44,"rd_intensity":15.64,"strategy_note":"毛利率與營益率都高於 CAMT，顯示製程控制有更好的定價空間，CAMT 的 55%～56% 目標並非行業天花板。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"KLAC","gm":61.47,"om":42.64,"fcf_margin":27.83,"rd_intensity":10.8,"strategy_note":"規模與利潤率遠高於 CAMT，COO 承認大型對手正進入 2D 檢測；關鍵在能否把前段關係帶進 OSAT。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主；新機種組合與 2027 起的調價為輔，併購與回購幾乎沒有貢獻。","runway_years":"已過 30%：FY2027 展望 8 億美元對可服務市場 20 億美元以上，約 40%","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋投入資本、折舊與營運資金，無法推算；情境樹按超出內生上界處理，Bear 機率取 30%。","segments":[{"item":"先進封裝（Q3 營收占比）","value":"約 80%，多數由 AI 需求帶動"},{"item":"一般封裝（手機等）","value":"平均每季約 15%，COO 2026-11-04 說未見走弱"},{"item":"HBM","value":"占 6 億美元訂單逾 20%（2026-08-10 COO）；兩家客戶 2026～2027 合計逾 2.6 億美元"},{"item":"光子","value":"約占訂單 5%，主要放量在 2028 後"},{"item":"服務","value":"2026 年約 4,000 萬美元，年增 35%～40%"},{"item":"軟體","value":"目前接近零，2027 預期達雙位數百萬美元，3 年目標約 4,000 萬美元"}],"decay_signals":["EPS 成長高於營收成長逾 5 個百分點：FY2027 共識 EPS 年增 40.2%、營收年增 34.8%，差 5.4 個百分點；原因是營業槓桿，若毛利率沒回升，這段差距會先消失。"]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"近 365 天無配息，回購與現金去向四分事實表未涵蓋，目前成長也不靠併購支撐，無資料可展開。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Visual Layer 金額未揭露，2027 才有軟體營收，已實現報酬無從計算。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購紀錄；近 365 天無配息。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 570 萬美元，年化 2,280 萬美元，對市值 45.35 億美元約 0.50%，低於 1.5%；以 SBC 金額代替淨稀釋股數，股數變動事實表未涵蓋。","grade":"過"}]},"valuation":{"basis":"Fwd P/E 為主，用 FY2026E 與 FY2027E 共識 EPS；事實表未涵蓋同業倍數。","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率與研發密度，沒有本益比或 EV/S，無法做倍數比較，需補資料。"},"fwd_pe":26.74,"peg":0.97,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2026E 本益比 26.74 倍、FY2027E 19.07 倍，PEG 0.97 數字上便宜；FY2027E 本益比對 FY2028E 成長 16.3% 的 PEG 則是 1.17。P/S 仍在 4 個年度端點的 59.7 分位，便宜只出現在盈餘口徑，而盈餘分母正是爭點，所以評為中性，不給便宜。五年分位事實表未涵蓋，留空。","upside_short_pct":12.2,"upside_mid_pct":42.2},"trap_analysis":{"verdict":"🟡","label":"一項衰退信號亮燈，FY2027 盈餘分母待驗證"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"COO 2026-11-04 說部分客戶提前一年下單，並非現在就需要機台，只是要確保檔期；投資人日未把 8 億美元拆成預測、訂單與預付；CFO 提過資本支出消化期；Needham 分析師點出 HBM 封裝的 TCB 延遲。","assumption":"2027 的檔期訂單大多是確定需求，不會遞延或重複下單。","consequence":"若訂單遞延，FY2027 營收低於 7.5 億美元，FY2029 EPS 谷底約 3.10 美元，五年後股價約 61.5 美元，約 −37%；若再疊加中國受限，虧損接近 50%。","ruling":"採納。與唯一致命數字同源，Bear 機率 30%，首倉只放 1/3。","watch":"預收款與合約負債、存貨成長率減營收成長率、FY2027 展望","evidence_refs":["supply_demand_durability#2"]},{"view":"論點失敗","evidence":"中國 FY2025 占營收 49%、2026 約 45%，COO 說 2027 至少持平；20-F 提醒出口管制即使不直接適用也可能壓低需求；CEO 2026-10-14 承認本地競爭增加。","assumption":"中國需求與份額 2027 不掉。","consequence":"中國營收少 30%，以 FY2027 約 3.6 億美元估算少 1.08 億美元，EPS 約少 0.96 美元，約 19%。","ruling":"採納為 Bear 的成分，不設為唯一致命數字：這需要一次政策轉折，FY2027 展望下修的傳導更直接。","watch":"中國營收占比與絕對金額、美國商務部新規","evidence_refs":["customer_concentration_credit#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"view":"論點失敗","evidence":"26 週跌 52.78%，FY1 共識近 3 個月卻上修 0.55%，背離原因與同業同期股價事實表都未涵蓋。","assumption":"這波下跌主要是週期恐懼，不是市場掌握了尚未反映在共識的壞消息。","consequence":"若賣壓來自未公開的訂單遞延或份額流失，FY2027 共識會補跌，現價不是底部。","ruling":"採納。不可裁決至 2027 年 2 月財報，在此之前只放首倉，不因低價加碼。","watch":"Q4 財報後的共識修正、賣方目標價更新"},{"view":"論點成功但股東經濟變差","evidence":"Q3 毛利率 51.1% 低於 CFO 8 月給的年底 52.5%～53% 路徑，CFO 歸因零組件與謝克爾升值；管理層另有 8 億美元以上現金用於成長與併購，過去 1.5 年看過逾百件。","assumption":"營收達 12 億美元時毛利率能到 55%～56%，現金不會買貴。","consequence":"毛利率少 4 個百分點，12 億美元營收下 EPS 約少 0.8 美元，約一成；一筆高價併購會再傷報酬。","ruling":"部分採納。Base 營益率只給 33%～34%，低於目標 34%～36%。","watch":"季度非 GAAP 毛利率、單筆併購是否超過市值 5%","evidence_refs":["geo_supply_chain#1"]},{"view":"價格已反映太多","evidence":"股價砍半後 P/S 8.33 倍仍在 4 個年度端點的 59.7 分位，EV/S 約在中位；FY2026E 本益比 26.74 倍還高於我給的終端 20 倍。","assumption":"高成長期間本益比能守住 20 倍以上。","consequence":"若市場繼續用週期頂部盈餘定價，FY2027E 4.95 美元×15 倍＝74 美元，還有約 24% 下檔。","ruling":"部分採納。估值結論只給中性，不給便宜；Base 已假設本益比由 26.74 倍降到 20 倍。","watch":"FY2027E 本益比、Q4 財報後的共識修正"}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 145.72 → 本次 97.05（-33.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=145.72","side_b":"本次 price_at_dd=97.05","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 145.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 145.72 美元：Bull 價 330、Bear 價 86.4，五年期望值 +42.8%，基準年化 8.7%，不對稱比 2.59","side_b":"本次情境、股價仍用 145.72 美元：Bull 價 286、Bear 價 61.5，五年期望值 +13.0%，基準年化 2.6%，不對稱比 1.39","ruling":"先換情境、股價不動：五年期望值少 29.8 個百分點，基準年化少 6.1 個百分點。不對稱比由 2.59 變為 1.39。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 145.72 美元：五年期望值 +13.0%，基準年化 2.6%，不對稱比 1.39","side_b":"本次情境、股價 97.05 美元：五年期望值 +69.7%，基準年化 11.3%，不對稱比 4.43","ruling":"再換股價、情境不動：起點價下跌 33.4%，五年期望值多 56.7 個百分點，基準年化多 8.7 個百分點，不對稱比由 1.39 升到 4.43。合計五年期望值比前份多 26.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前次進場條件已達成，重訂首倉門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤ $125（FY2027E 本益比約 25.5 倍、Base 五年年化 ≥ 12%）且 Q3 營收 ≥ $158M 兌現→首倉 1/3；或 FY2027 共識 EPS 上修 ≥ 10% 且股價未過 $165→重跑","side_b":"股價 ≤ $100 且 2027 營收展望 ≥ $800M→首倉 1/3；2026 Q4 毛利率 ≥ 51% 且展望不降→加至 2/3；股價 > $125 而財報未驗證不追","ruling":"前次首倉條件的兩項都已發生：股價 97.05 美元低於 125 美元，Q3 營收 1.613 億美元高於 1.58 億美元，所以本次重做判斷。Q3 已兌現，下一個未驗證的是 8 億美元展望與毛利率，首倉與加碼門檻改掛這兩項。","evidence_level":"公司新聞稿（一手）","settle_metric":"FY2027 營收展望、2026 Q4 非 GAAP 毛利率","if_then":["若 2026 Q4 毛利率 ≥ 51% 且展望 ≥ 8 億美元，加碼至計畫倉位 2/3","若股價先漲過 125 美元而財報還沒出，不追"]},{"axis":"毛利率說法改口","cause":"新證據","prior_field":null,"side_a":"2026-08-10 CFO：年底毛利率 52.5%～53%、營益率 30%～32%。","side_b":"2026-11-04 CFO：Q3 毛利率 51.1%，低於預期，改說 2027 Q1 起逐步改善，沒有給 Q4 數字。","ruling":"可調和，屬時間延後。零組件與匯率的一次性歸因不採信也不否定，標為未證；若 2027 年 8 月財報毛利率仍低於 52%，這個歸因就不成立。匯率不做預測，只看毛利率有沒有吸收掉。","evidence_level":"公司法說（一手）","settle_metric":"2027 Q1、Q2 非 GAAP 毛利率","if_then":["若 2027 Q1 毛利率 ≥ 52%，加碼至滿倉","若 2027 Q1 與 Q2 都低於 51%，減碼一半，定價力評分下調 1 分"]},{"axis":"供應鏈說法前後不一","cause":"新證據","prior_field":null,"side_a":"2026-08-10 COO：討論產能時看不到問題或障礙；2026-10-14 CEO：營運基礎能供應更多。","side_b":"2026-11-04 COO：部分供應商產能不足，要 3～6 個月解決，但自己說只是感覺、不確定。","ruling":"可調和：自家產能沒問題，卡在外部零組件。但三個月內說法轉向，管理層的時程只當參考，以 2027 年 5 月財報是否仍提短缺為準。","evidence_level":"公司法說（一手）","settle_metric":"2027 年 5 月財報的短缺說法與交期","if_then":["若 2027 年 5 月仍提短缺或錯過交期，停止加碼","若短缺解除且毛利率回升，維持原加碼節奏"],"evidence_refs":["geo_supply_chain#1"]},{"axis":"OSAT 主導地位與對手得標","cause":"新證據","prior_field":null,"side_a":"2026-11-04 COO：在 OSAT 居主導地位，大型對手很難進入。","side_b":"2026-10-14 COO：對手宣布 OSAT 訂單，公司只稱也拿到大單；台灣 OSAT 份額預期至少 50%；大型對手進 2D 要努力應對，而 2D 占 2026 年出貨約 85%。","ruling":"可調和，屬程度差異。市場變大時客戶開始多家採購，方向維持穩定；份額全是公司自述，所以不給溢價。","evidence_level":"公司法說（一手，自述）","settle_metric":"OSAT 占訂單比重、Yole 年度份額","if_then":["若 OSAT 占訂單低於 45%，減碼一半並重做競爭判斷","若 2028 年份額如 COO 所說變大，定價力評分上調 1 分"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"股價與訂單方向相反","cause":"新證據","prior_field":null,"side_a":"股價 26 週跌 52.78%，週線跌破 52 週與 104 週均線。","side_b":"年初至今訂單逾 8 億美元，檔期排到 2027 下半年，FY1 共識近 3 個月上修 0.55%。","ruling":"性質是市場與公司資料方向相反，但不是論點內部的矛盾。裁定偏向訂單，但證據不足以下重注：Q3 高於指引與 2027 展望是公司明文，下跌原因事實表未涵蓋。決勝數據今天不存在，最早 2027 年 2 月才有，在此之前只放首倉。現在就賣的最強論證：訂單未拆分、毛利率已失約一次、競爭者已進門，股價仍是當年盈餘的 26.74 倍，跌 53% 不等於安全邊際。","evidence_level":"訂單為管理層自述，未拆分；股價為市場事實","settle_metric":"FY2027 展望、預收款與訂單拆分","if_then":["若 FY2027 展望下修到 7.2 億美元以下，清倉","若展望上修到 8.5 億美元以上且股價仍低於 125 美元，加碼至滿倉","若股價先漲過 125 美元而財報未驗證，不追","若股價跌破 78 美元而展望未降，分批反買，不停損"]},{"axis":"估值結論與裁決的變動","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 145.72 美元，估值結論為最貴一級，觀望。","side_b":"本次股價 97.05 美元，跌 33%，FY2027E 本益比 19.07 倍，估值結論降到中性。","ruling":"前次觀望的主因是估值偏高，這個理由已隨股價消失，討論轉為小倉位試單；基本面只小幅變化，不是公司變好。"},{"axis":"價值陷阱風險上升","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱風險為低。","side_b":"本次為中等：EPS 成長高於營收成長 5.4 個百分點，毛利率低於管理層說法。","ruling":"只亮一項信號，列中等；毛利率逐季同比與份額是資料缺口，補上後可能再升。"},{"axis":"看過新證據後維持的欄位","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份評級 B、護城河穩定、後段成長中等、品質複利成長、中循環。","side_b":"本次相同。","ruling":"12 億美元目標與 2027 展望偏正面，毛利率、競爭與混合鍵合延後偏負面，兩邊相抵，不足以改變評級。搶檔期與零組件短缺已是後段特徵，若 2027 訂單放緩就改列晚循環。"},{"axis":"機率與最大回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"Bull 25%、Bear 30%、最大回撤 −55%。","side_b":"Bull 25%、Bear 30%、最大回撤 −55%～−35%。","ruling":"機率不變，因為訂單上修與毛利率失約互相抵銷。回撤改成範圍，並以現價 97.05 美元為起點重算，同樣的 −55% 對應的價位已低很多。"},{"axis":"Single Thing 與清倉指標前份無紀錄","cause":"方法變動","prior_field":["single_thing","kill_metrics"],"side_a":"前份摘要的唯一致命點與清倉指標均為 null。","side_b":"FY2027 營收展望被下修到 7.2 億美元以下（較 8 億美元少 10%）。","ruling":"前份摘要沒有保留這兩欄，無從比較；本次首次留下 Single Thing 與清倉門檻。"}],"triggers":[{"n":1,"text":"股價不高於 100 美元且 2027 營收展望維持 8 億美元以上，建立首倉","type":"估值rearm","maps_to":"H1","metric":"股價、2027 營收展望","threshold":"股價 ≤ $100 且展望 ≥ $800M","action":"首倉 1/3","source_freq":"每日股價，每季財報","date":"2026-11-09 起"},{"n":2,"text":"2026 Q4 非 GAAP 毛利率不低於 51% 且 2027 展望不降，加到計畫倉位 2/3","type":"加碼","maps_to":"H1","metric":"非 GAAP 毛利率、2027 營收展望","threshold":"≥ 51% 且展望 ≥ $800M","action":"加碼至 2/3","source_freq":"每季財報","date":"2027-02"},{"n":3,"text":"2027 Q1 非 GAAP 毛利率達 52% 以上，加到計畫倉位上限","type":"加碼","maps_to":"H2","metric":"非 GAAP 毛利率","threshold":"≥ 52%","action":"加碼至滿倉","source_freq":"每季財報","date":"2027-05"},{"n":4,"text":"股價跌破 250 週均線附近而 2027 展望未降，分批反買，不停損","type":"加碼","maps_to":"H1","metric":"股價、2027 營收展望","threshold":"股價 < $78 且展望 ≥ $800M","action":"分批反買","source_freq":"每週收盤，每季財報","date":"持續"},{"n":5,"text":"股價先漲過 125 美元而財報還沒驗證，不追","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"> $125 且財報未驗證","action":"不追","source_freq":"每日","date":"2027-02 前"},{"n":6,"text":"2027 連兩季毛利率低於 51%，減碼一半","type":"減碼","maps_to":"R1","metric":"非 GAAP 毛利率","threshold":"連 2 季 < 51%","action":"減碼一半","source_freq":"每季財報","date":"2027-08"},{"n":7,"text":"2027 營收展望下修到 7.2 億美元以下，清倉","type":"Single Thing","maps_to":"Single Thing","metric":"FY2027 營收展望","threshold":"< $720M","action":"清倉","source_freq":"每季財報","date":"2027-12 前每季","evidence_refs":["supply_demand_durability#2"]},{"n":8,"text":"OSAT 占訂單低於 45%，或管理層不再重申台灣 OSAT 份額至少 50%，減碼一半","type":"風險","maps_to":"R3","metric":"OSAT 占訂單比重","threshold":"< 45%","action":"減碼一半","source_freq":"法說揭露時","date":"持續","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"n":9,"text":"中國營收年減逾 20%，或美方新規直接涵蓋檢測量測機台，減碼一半","type":"風險","maps_to":"R4","metric":"中國營收、美國出口管制規則","threshold":"年減 > 20% 或新規涵蓋","action":"減碼一半","source_freq":"每季財報，規則公告時","date":"持續","evidence_refs":["customer_concentration_credit#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":10,"text":"2027 年 5 月財報仍提零組件短缺，或任一季錯過交期，停止加碼","type":"風險","maps_to":"R6","metric":"短缺說法、交期","threshold":"2027-05 仍短缺或錯過交期","action":"停止加碼","source_freq":"每季法說","date":"2027-05","evidence_refs":["geo_supply_chain#1"]},{"n":11,"text":"2026 Q4 財報後重做判斷","type":"複審日期","maps_to":"H1","metric":"毛利率、2027 展望、下跌原因資料","threshold":"財報公告後","action":"重做判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"FY2027 營收展望","bear_threshold":"低於 7.2 億美元","window":"2026 Q4 至 2027 Q3 每季財報","source":"公司新聞稿與法說","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"2027 連 2 季低於 51%","window":"2027 Q1 起每季","source":"公司新聞稿","last_status":"warning"},{"metric":"OSAT 占訂單比重","bear_threshold":"低於 45%","window":"管理層每次揭露","source":"法說與投資人日","last_status":"ok"},{"metric":"中國營收","bear_threshold":"年減逾 20%，或美方新規直接涵蓋檢測量測機台","window":"每季；規則公告時即時","source":"公司新聞稿、20-F、美國商務部公告","last_status":"ok"},{"metric":"存貨成長率減營收成長率","bear_threshold":"連 2 季高於 10 個百分點","window":"每季資產負債表","source":"6-K 財報","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"Q4 財報驗證前不超過總資產 2%，通過後不超過 4%；要有再跌 35%～55% 的心理準備。","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 FY2027 盈餘當週期頂點定價：26 週股價跌 52.78%，FY1 共識近 3 個月卻上修 0.55%，FY2027 本益比只剩 19 倍。但管理層給了 8 億美元以上展望，檔期已排到 2027 下半年，單季毛利率落空不等於週期結束。下跌的確切原因事實表未涵蓋，此判斷待 2026 Q4 財報驗證。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-52.78, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價 ≤ $100 且 2027 營收展望 ≥ $800M→首倉 1/3；2026 Q4 毛利率 ≥ 51% 且展望不降→加至 2/3；股價 > $125 而財報未驗證不追","exec_line":"分三批：第一批不超過計畫倉位 1/3；第二批等 2026 Q4 財報（預計 2027 年 2 月）；第三批等 2027 Q1 毛利率達 52%。"},"reasoning":{"industry":"Q3 營收 1.613 億美元，年增 28%，GAAP 毛利率 50.0%，非 GAAP 毛利率 51.1%、營益率 29.5%；Q2 到 Q3 增量營益率約 41%（營業利益多 1,150 萬美元，營收多 2,810 萬美元）。先進封裝約占八成，其中手機等一般封裝平均每季約 15%；OSAT 占訂單略高於五成。單點依賴不在單一客戶，FY2025 最大客戶僅 11%，而在 AI 資本支出與中國：亞洲占 Q3 營收 95%，中國 2026 年約 45%。產業時鐘在擴張期：年初至 10 月中訂單逾 8 億美元，對前三季營收約 4.15 億美元，訂單出貨比約 1.9 倍（期間不完全對齊），客戶把檔期排到 2027，零組件短缺與調價同時出現，已有擴張後段的特徵。可能看錯之處：訂單金額是管理層自述，且沒有拆出確定訂單與預測。","moat":"機制是專為先進封裝客製的 2D 檢測與 3D 凸塊量測，加上約 4,000 台裝機與放量期不願換機的認證成本。可比軸用利潤率，因為事實表沒有 ROIC：毛利率 50.03%，低 NVMI 7.35 個百分點、低 KLAC 11.44 個百分點、與 ONTO 差 0.33 個百分點；GAAP 營益率 23.15%，高 ONTO 9.34 個百分點、低 NVMI 6.89 個百分點（ONTO 為截至 6 月的資料）。份額數字全部是公司自述，不足以支持溢價。2026-10-14 COO 預期台灣 OSAT 份額至少 50%，同時承認對手在同一客戶拿到訂單，這是客群開始多家供應，還不是份額下滑的證據；若之後 OSAT 占訂單跌破 45%，我的方向判斷就錯了。產業態勢裁決為雙向拉鋸：競爭者變多，需求與檢測步驟也在增加。AI 軟體長在自家機台上，屬強化而非替代，2027 才有營收，尚無法算淨增量。","growth":"成長以量為主，Hawk 與 Eagle G5 組合與 2027 開始的調價是第二層，併購與回購幾乎沒有貢獻。FY2026E 到 FY2028E 共識 EPS 兩年年化 27.7%（3.63 到 5.92 美元）；FY2025 只有 GAAP 1.04 美元，當年營業利益率沒降、淨利卻減半，判斷受非營業項目壓低（事實表未拆），不能當基期，所以三年年化不採用。FY2027 共識營收年增 34.8%、EPS 年增 40.2%，差距來自營業槓桿。內生上界因事實表未涵蓋投入資本而算不出，缺口無法歸因，長期信心上限取中。第二條曲線目前都還不夠硬：混合鍵合 2027 貢獻有限、2028 起才有意義，投資人日也承認比預期慢；光子約占訂單 5%，主要放量在 2028 後；軟體與服務目標 3 年 1.4 億美元，其中軟體 4,000 萬美元是估計值。衰退信號只亮一項，逐季毛利率同比與份額屬資料缺口，沒有計入；TTM 毛利率 50.03% 低於 FY2025 的 50.46%，值得盯。","governance":"FCF 對淨利轉換率 FY2022 至 FY2025 依序 0.62、0.90、0.94、2.51 倍，FY2025 偏高是因淨利被壓低，不是現金變好。Q3 SBC 570 萬美元，占營收 3.5%，年化約 2,280 萬美元，對市值 45.35 億美元約 0.50%。現金 8.771 億美元，以稀釋股數 5,150 萬股算每股約 17 美元，占股價約 17.5%。事實表的現金 6.07 億美元沒有包含公司口徑的全部存款與有價證券，用公司口徑算 EV 約 41.5 億美元，比表上 44.2 億美元低約 6%。可轉債條款與現金去向四分事實表未涵蓋，轉換價若高於現價，這筆債要還現金而不是轉股，所以現金不能全部算成安全邊際。併購看過逾百件，Visual Layer 金額未揭露、整合已完成，報酬還要等 2027 軟體營收。","valuation":"要年化 12%，五年後股價要到約 171 美元；用 20 倍終端本益比，FY2031 EPS 要約 8.55 美元，從 FY2026E 3.63 美元算是年化 18.7%。我的 Base 是 8.30 美元，略差一點。FY2026E 本益比 26.74 倍、FY2027E 19.07 倍，兩年年化 27.7% 下 PEG 0.97。Trailing 本益比 36.48 倍在 4 個年度端點的 23.3 分位，但 P/S 8.33 倍在 59.7 分位、EV/S 8.12 倍在 51.6 分位，股價砍半後按營收看並不便宜，便宜只出現在盈餘口徑。五年歷史分位事實表未涵蓋。賣方目標價多在 8 月以前（均值約 187.58 美元，現價低於均值 48%），早於這波下跌，不拿來支持裁決；各來源最高 220 美元對最低 80 美元，全距約 2.75 倍，信心相應下調。12 個月上檔用 FY2027E 4.95 美元×22 倍＝108.9 美元，約 +12.2%；3 年用 FY2029E 6.90 美元×20 倍＝138 美元，約 +42.2%。","premortem":"衰退信號亮一項，價值陷阱風險列中等。週線收在 104 週均線下、250 週均線上（97.05 對 115.43 與 77.86），26 週跌 52.78%，RSI 30.21，動能沒有過熱，也沒有止跌訊號。事實表沒有解釋這波下跌的原因，也沒有同業同期股價，這是本次最大的資料缺口。核心可守：FY2023 下行時營收只跌 1.72%、GAAP 營益率仍有 20.74%，但樣本只有一次，當時的 AI 封裝占比事實表未涵蓋。波動按深回撤準備，不因波動本身砍倉。法說上 TCB 延遲的提問，COO 只說沒看到變化，沒有正面解釋。"},"plain":{"six":{"how_it_makes_money":"賺先進封裝客戶為守良率付的檢測與量測錢，利潤卡在專用機台與約 4,000 台裝機基礎；Q3 約八成營收來自先進封裝，多數由 AI 需求帶動。","moat":"穩定：裝機基礎與專用機台還守得住，但大型同業已在 OSAT 拿到訂單，漲價能力要到 2027 才看得出來。","growth":"中等：以 2027 年 8 億美元對 20 億美元以上的可服務市場算，滲透率已約 40%，後面要靠管理層口徑的新市場，混合鍵合又比預期慢。","capital":"現金多、紀律待驗：8.77 億美元現金主要留給成長與併購，近一年沒有配息，SBC 稀釋輕。","valuation":"現價要 FY2027 約 5 美元的盈餘站得住，FY2031 還要做到約 8.5 美元才有年化 12%；我相信前者，後者要看毛利率與 12 億美元目標。","how_wrong":"最可能看錯的地方，是把 2027 搶檔期的訂單當成真實需求。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 FY2027 盈餘當週期頂點定價：26 週股價跌 52.78%，FY1 共識近 3 個月卻上修 0.55%，FY2027 本益比只剩 19 倍。但管理層給了 8 億美元以上展望，檔期已排到 2027 下半年，單季毛利率落空不等於週期結束。下跌的確切原因事實表未涵蓋，此判斷待 2026 Q4 財報驗證。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":97.05,"week26_return_pct":-52.78,"consensus_rev_3m_pct":0.55,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2025 GAAP EPS 1.04 美元被壓低，不能當基期，已改用前瞻口徑。FY2027E 5.09 美元依賴 8 億美元展望，這是展望不是財測，管理層也沒拆在手訂單；市場砍半股價而共識未動，分母本身就是爭點，便宜的論證不成立。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 Q4 財報與 2027 展望更新（日期依去年 2 月 18 日公告推估）","impact":"高","watch":"非 GAAP 毛利率是否 ≥ 51%、8 億美元展望是否維持、訂單有無拆分"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"2027 Q1 財報","impact":"高","watch":"非 GAAP 毛利率是否 ≥ 52%、調價效果"},{"date":"2027-05","date_precision":"month","type":"capacity","event":"零組件短缺解除的最晚時點（COO 估 3～6 個月）","impact":"中","watch":"是否仍提短缺、有無錯過交期"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"AI 軟體產品開始貢獻營收","impact":"中","watch":"2027 全年是否達雙位數百萬美元、認列為訂閱或一次性授權"}],"_projected_from":"v19"}
```
