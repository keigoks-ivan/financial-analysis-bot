你是 stock-analyst v20 的**散文層（prose）agent**，標的 2383.TW（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2383.TW_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：2383.TW　日期：2026-11-02　archetype：None　前份裁決：2026-10-20　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1660B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（471B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（874B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（788B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1035B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（736B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（849B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2343B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3328B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2697B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1660           3738-5340      5 條（2–6 內）  
s3                  8000         471           5270-7529      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2697          8612-12303      5 條（2–6 內）  
s6                 11000         736          7185-10264      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         849           1856-2651      5 條（2–6 內）  
s10                 5000        2343           1860-2657      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2697           2000-2303      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4165B；至少需散文≈40.84KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−76%
−75
−75%
−70%
−56%
−52%
−50%
−50
−28.4
−13.6
−7.5%
−2.9%
−1
0
0.1
0.14
0.29
0.4
0.5%
0.535%
0.535
0.75
1
1.45%
1.5
1.5%
1.6
1.68
1.7%
1.77
02
2
2.11
2.2%
2.3
2.6
3%
3
03
3.33%
3.33
3.414
3.5%
3.584
3.590
3.9%
4
4.3
5%
5
5.1%
5.8%
6
6%
06
7
7.5%
7.91
8
08
8%
8.94%
9
9.5
9.7
10%
10
10.08
10.1
10.17
10.6
10.95%
11
11.4
12
12%
13
13.5
14%
14
14.4
15%
15
15.5%
15.82%
17
17.1
18
19.94%
20
20%
20.28%
20.88%
20.9
21%
21.36%
22%
23.4
23.41%
24
24.5%
24.9%
25%
26
26%
26.94%
27
27.55
28
28%
28.3
29
29.83%
30%
30.2%
31
31.06%
32%
32.5669
33%
33.54%
33.85%
34.6%
34.93
35%
35
36%
38
38%
38.35
39.5%
40
40.0%
40%
40.81
42
45
45%
46.4%
49
50%
50.7
51.8
52%
52
54
56%
57%
60%
62%
65%
65
67.8
70
70%
73
73.13
76%
80%
81
82.3
85
85%
86%
90%
95%
99%
100%
100
103.7%
104
121%
125.6
132%
133.85
146.5
150%
150
152.2
157.4
159%
160
168.9%
170
184%
190
215
215.32
220
230
240
250
260
273
273.24
290
320
380
400
441.28
460
472.75
500
530
560
585
615
640
720
930
945
986
2022
2023
2024
2025
2026
2027
2028
2029
2030
2031
2383
4675.0
5055.0
6213
6274
600183
20261102
1,107
1,412.27
1,525
10,400
12,960
14,400
2,025
2,040
2,252
3,000
3,600
3,725
3,750
3,960
4,300
4,675
4,680
5,000
5,055
6,000
6,070
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
{"meta":{"ticker":"2383.TW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"台光電"},"oneliner":"台光電是 AI 伺服器與交換器高速銅箔基板的全球龍頭，漲價加上滿載，把第四季毛利率指引推到 38% 以上；但 2030 年月產能要擴到現在的 2.6 倍，現價已經用景氣高點的獲利定價，五年基本情境年化約 5–6%，等 3,750 元附近再看。","thesis":{"H":[{"id":"H1","text":"2027 年 AI 伺服器與交換器的需求讓台光電維持滿載、漲價守住，2027 年 EPS 至少 240 元（共識 273 元）","2y":"2027 年單季毛利率維持 ≥33%，產能利用率 ≥95%","5y":null,"10y":null,"threshold":"單季毛利率 ≥33%（2026Q2 33.85%，第四季指引 38–39.5%）；2027 年 EPS ≥240 元","source":"公司季報與法說會（每季）、月營收（每月）","drift_rule":"TTM 營業利益比 Base 路徑連 2 季低 5% 以上為削弱，連 3 季低 10% 以上為反轉"},{"id":"H2","text":"2030 年 1,525 萬張的月產能，在景氣中段仍能大致賣完，營業利益率不跌回 2025 年的 20% 以下","2y":null,"5y":"2028–2030 年產能利用率 ≥85%，年度營業利益率 ≥20%","10y":null,"threshold":"產能利用率 ≥85%；年度營業利益率 ≥20%（2025 年 20.28%）","source":"年報，以及法說會的產能與利用率揭露","drift_rule":"TTM 營業利益比 Base 路徑連 4 季低 5% 以上為削弱，連 6 季低 10% 以上為反轉"},{"id":"H3","text":"台光電在高速材料維持份額領先：M9 2027 年放量，載板材料 2027 年開始出貨，高階材料占比不降","2y":"2027 年 M7 以上占營收 ≥65%，載板材料開始出貨","5y":null,"10y":null,"threshold":"M7 等級以上占營收 ≥65%（2026Q3 為 65–70%）；載板材料 2027 年內出貨","source":"法說會（每季）、Prismark 年度排名","drift_rule":"高階占比連 2 季比 65% 低 5% 以上為削弱；連 3 季低 10% 以上，或載板材料延到 2028 年，為反轉"}],"R":[{"id":"R1","text":"產能洪水：公司與同業同時擴產，上游 2H27 放量，2028 年起高階 CCL 降價，毛利率回到上一輪低點附近","h_ref":"H2","clock":"🔥","threshold":"單季毛利率年減連 2 季，或任一季季減 ≥3 個百分點且管理層提及降價","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"]},{"id":"R2","text":"共同封裝光學（光進銅退）縮短交換器板上的電傳輸距離，削弱 M8／M9 在交換器上的用量","h_ref":"H3","clock":"🐢","threshold":"主要交換器平台量產採用共同封裝光學，且公司揭露的交換器材料營收連 2 季下滑","evidence_refs":["substitute_technology#0","supply_demand_durability#1"]},{"id":"R3","text":"雲端資本支出進入消化期，或平台換代出現空窗，客戶調整庫存，月營收轉弱","h_ref":"H1","clock":"⚡","threshold":"月營收年增率連 2 個月低於 30%，或連 2 個月月減","evidence_refs":["cyclical_inventory_price_position#0"]},{"id":"R4","text":"擴產期現金流持續為負，2027–2030 年約 986 億元的資本支出需要舉債，或發行可轉債、新股，股東經濟被稀釋","h_ref":"H2","clock":"🔥","threshold":"淨負債 >500 億元，或宣布發行新股、海外存託憑證、可轉債","evidence_refs":["cyclical_supply_discipline_capacity#0"]}],"single_thing":{"description":"2027 年底前，台光電或主要同業首次對 M8／M9 等高階 CCL 宣布調降合約價","why_fatal":"毛利率是 EPS 最大的單一敏感項。粗算：2028 年營收約 5,000 億元時，毛利率每降 5 個百分點，稅後淨利少約 190 億元，EPS 少約 54 元（約 Base 2028 年 380 元的 14%）。首次降價代表供需翻轉，價格通常會一路降到產能消化完，EPS 與倍數會同時下修","if_happens":"取消進場條件，Bear 機率上調到 45%，重跑研究；若已持有，先減碼一半，下一季毛利率低於 32% 就清倉","how_monitor":"每季法說會的價格說法；月營收與產能成長的比較；台燿與聯茂的法說會和報價報導；上游玻纖布與銅箔的報價","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.1,"peg_fy2":0.14,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":40.81,"FY2026E":133.85,"FY2027E":273.24,"FY2028E":441.28},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS；共識取 Koyfin 2026-10-31 快照，美元以 32.5669 換算新台幣；EPS 的分析師家數事實表沒有"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2383.TW_20261102/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"產能擴張帶動成長，價格隨供需上下，終端綁雲端與 AI 資本支出；份額領先，但定價力有一部分是景氣給的"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉（時點約 2028 年）。需求面：管理層稱未來兩年 CCL 仍緊張，LTA 訂單超過新增產能；業界稱中高階 CCL 到 2028 年供不應求。供給面：公司 2030 年月產能 1,525 萬張，台燿 2028 年 530 萬張，上游玻纖布 2H27 起放量，供給可逆性高。來源：2026-10-29 第三季法說的媒體整理、優分析產業報導。","bargaining":{"up":"強：HVLP3／HVLP4 銅箔、E 布與低介電玻纖布在下半年最吃緊，T-glass 與低介電新產能 2H27 才投產","down":"弱：客戶接受第二季起 10% 以上的漲價；2025 年兩大客戶各占 14%、12%","geo":"產地分布在台灣、中國（昆山、中山、黃石）、馬來西亞檳城、美國加州 Arlon（2026 年底擴建後營運），可以分散關稅"},"profit_pool_dir":"利潤往高速材料集中：公司毛利率從 2025 年 29.83%，到 2026Q2 33.85%，再到第四季指引 38–39.5%；同業聯茂 TTM 毛利率只有 15.82%。利潤池正流向高階材料龍頭。","tam_table":{"expanded":false,"reason":"事實表沒有 CCL 產業規模、高速材料滲透率與各段成長率，只有份額排名（2025 年全球第一）與利基市場份額多數超過 50% 的質性證據，無法填表；此為資料缺口"}},"moat":{"mechanism":"高速低損耗樹脂配方、平台級材料認證、全球最大產能三者疊加：輝達與雲端客戶每一代平台指定材料等級，認證最早、供得出量的廠商拿走份額。轉換成本只鎖一個平台世代（約一到兩年），下一代重新競爭。","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"Prismark：2025 年營收升為全球 CCL 第一（2024 年第三），超越生益與建滔。外資稱在 Google 需求下對手產能不足，台光電可拿更多份額；法人看好台光電超越斗山，成為輝達最大的 CCL 供應商；HDI、高速材料、AI 伺服器、交換器、低軌衛星等利基市場份額多數超過 50%。沒有最大客戶份額下滑的證據。","peer_na_reason":"台燿的 yfinance 季損益沒有資料；斗山未列入同業表；同業倍數與 ROIC 事實表沒有","threats":[{"level":"🔴","text":"產能洪水：公司 2030 年月產能目標 1,525 萬張（現在約 585 萬張），2027–2030 年資本支出約 986 億元；台燿 2028 年 530 萬張；上游 T-glass 與低介電材料 2H27 投產。2028 年起，高階 CCL 有降價風險","p":"35%","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#2","supply_demand_durability#0"]},{"level":"🔴","text":"共同封裝光學（光進銅退）縮短交換器板上的長距離電傳輸，削弱 M8／M9 在交換器上的用量；伺服器運算板與載板材料不受直接影響","p":"30%","evidence_refs":["substitute_technology#0","supply_demand_durability#1"]},{"level":"🟡","text":"客戶找第二供應商：斗山、台燿在輝達與網通客戶端競爭份額；兩大客戶各占 14%、12%，公司以保密協定為由不評論單一客戶","p":"20%","evidence_refs":["customer_concentration_credit#0","customer_second_source#0","competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"高利益率×周轉率資料缺口","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端與 AI 平台，決策者是輝達與雲端的板材規格設計，付款者是 PCB 廠，三個角色都成立。但需求是雲端資本支出的衍生需求，急迫性高不等於持久。代理讀數：第三季產能利用率 100%，LTA 超過新增產能，能見度約兩年。"},{"item":"決策層級","level":"🟡","text":"替代性要看單一平台的材料指定，不是看 CCL 有幾家供應商。每一代平台都要重新認證，鎖定期約一個世代；斗山、台燿在輝達與網通交換器都是現役競爭者。代理讀數：利基市場份額多數超過 50%，但客戶在保密協定下不揭露架構，續用率無法量化。"},{"item":"價值鏈分配","level":"🟡","text":"台光電分到的比例正在上升（毛利率從 29.83% 升到指引的 38–39.5%）。但上游 HVLP 銅箔、低介電玻纖布與 T-glass 在缺料期也分走價值。2H27 上游放量後，成本可能下降，但同業產能也同時放量；下游的輝達與雲端客戶議價力最強，長期能留下多少不確定。"},{"item":"社會容忍度","level":"🟢","text":"這是企業間的電子材料，終端使用者看不到價格，沒有社會反彈或監管授權的依賴。公平會處分書查無紀錄，反競爭訴訟損失為 0；關稅與出口管制的風險，以美國、馬來西亞產線分散。"}],"roiic":"約 40–60%。代理算法：2025 年淨利增加 50.7 億元，除以 2024 年淨再投資 82.3 億元約 62%，除以 2025 年的 125.6 億元約 40%；淨再投資＝淨利減自由現金流","reinvest_rate":"約 86%：2025 年淨利 146.5 億元減自由現金流 20.9 億元，再除以淨利（2024 年同樣約 86%）；TTM 自由現金流為負，超過 100%","endo_ceiling":40,"formula_note":"內生成長上界＝增量報酬×再投資率，約 40–60%×86%＝35–50%，取 40%。限制：折舊與投入資本事實表沒有；淨利增量含漲價貢獻，不全是新資本帶來的，數字偏高"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","2383.TW":31.06,"6274.TW":null,"6213.TW":15.82,"600183.SS":33.54,"unit":"%"},{"metric":"營業利益率","2383.TW":23.05,"6274.TW":null,"6213.TW":8.94,"600183.SS":23.41,"unit":"%"},{"metric":"FCF 利潤率","2383.TW":-2.9,"6274.TW":null,"6213.TW":-4.92,"600183.SS":10.95,"unit":"%"},{"metric":"研發密度","2383.TW":2.15,"6274.TW":null,"6213.TW":2.31,"600183.SS":4.93,"unit":"%"}],"competitors":[{"name":"6274.TW","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null},{"name":"6213.TW","gm":15.82,"om":8.94,"fcf_margin":-4.92,"rd_intensity":2.31,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"600183.SS","gm":33.54,"om":23.41,"fcf_margin":10.95,"rd_intensity":4.93,"period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"2026 年以價為主（漲價 10% 以上，M7 以上占營收 65–70%）；2027 年起價量並進（產能擴充約五成）；沒有併購，也沒有淨回購（股數三年年均小幅稀釋）","runway_years":"資料缺口（滲透率事實表沒有）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段的報酬持續期：增量報酬約 40–60%×再投資率約 86%，上界約 35–50%，取 40%；共識三年 EPS 年複合約 121%，超出部分歸因於毛利率擴張","segments":[{"item":"基礎設施（AI 伺服器、交換器、低軌衛星）","value":"2025Q4 約 65–70%（其中低軌衛星約一成），公司估 2026 年 70–80%；第四季指引季增約 20%"},{"item":"行動裝置（HDI）","value":"占比事實表沒有；第四季指引持平"},{"item":"車用與工業","value":"占比事實表沒有；第四季指引季減 5–10%"},{"item":"M7 等級以上高階材料","value":"占營收 65–70%（2026Q3 法說）；M9 2026 下半年量產，2027 年放量"},{"item":"載板材料（新產品）","value":"年底完成客戶認證，2027 年出貨，毛利率預期超過 50%；營收規模未揭露"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"毛利率逐季上升，第四季指引 38–39.5%"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"2025 年升為全球第一"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"漲價後產能利用率仍是 100%"},{"signal":"EPS 成長高於營收成長逾 5 個百分點","lit":true,"note":"2022–2025 年 EPS 年複合約 40.0%，營收約 34.6%；共識 2025–2027 年 EPS 年複合約 159%，營收約 99%"},{"signal":"自由現金流對淨利比連 2 年低於 0.75","lit":true,"note":"2024 年約 0.14，2025 年約 0.14，TTM 為負"},{"signal":"SBC 占營收逾 5% 且上升","lit":false,"note":"SBC 事實表沒有；股數三年年均約 +1.7%，來源未明"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"共同封裝光學是潛在威脅，尚無用量下滑的證據，列入監測"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"自身倍數在近四年的高點"},{"signal":"維持性資本支出占自由現金流逾 60%","lit":false,"note":"自由現金流為負，維持性資本支出事實表沒有，無法判讀"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"正在大幅擴產"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自有擴產，不靠併購或回購；股東回報只有殖利率約 0.5% 的現金股息，不是判斷的關鍵"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月重大訊息沒有併購；美國 Arlon 是既有的全資子公司增資擴建，不是收購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表沒有回購紀錄；股東回報只有現金股息，trailing 殖利率 0.535%","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數 2022 年 3.414 億股 → 2025 年 3.590 億股（年度淨利÷稀釋 EPS 推得），年均 +1.7%，高於 1.5%；近一年持平；稀釋來源事實表沒有","grade":"不過"}]},"valuation":{"basis":"以前瞻本益比（FY1、FY2）為主，trailing 本益比與 P/S 為輔。分位只用近四年年度端點加上現值，日頻的五年高低點事實表沒有，實際分位可能略低於 100","tier":"台系高速 CCL 龍頭","peers":{"expanded":false,"reason":"事實表沒有同業本益比、EV/S 與股價淨值比，只有同業利潤率；倍數改用自身對照：trailing 73.13 倍、FY1 34.93 倍、FY2 17.1 倍"},"fwd_pe":34.93,"peg":0.29,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"五年基本情境年化約 5–6%，低於 8% 的弱門檻；trailing 本益比、P/S、EV/S 都在近四年年度端點的最高。但 FY2 本益比 17.1 倍並不極端，貴在景氣高點獲利能否持續，不在當年倍數，所以判偏貴，而不是極貴。","targets":{"short":"12 個月：2027 年基本 EPS 260 元×18 倍（接近目前 FY2 本益比）＝4,680 元","mid":"約兩年：2029 年基本 EPS 400 元×15 倍＝6,000 元"},"upside_short_pct":0.1,"upside_mid_pct":28.3},"trap_analysis":{"verdict":"🟡","label":"景氣高點獲利被當常態"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"公司 2030 年月產能目標 1,525 萬張（現在約 585 萬張），2027–2030 年資本支出約 986 億元；台燿 2028 年產能 530 萬張；上游 T-glass 與低介電材料 2H27 投產。上一輪下行，2023 年首季營收年減 26%，毛利率 21.36%","assumption":"雲端 AI 資本支出到 2028–2030 年，仍能吸收全產業倍增的高階產能","consequence":"2028 年降價，毛利率回到 25% 以下，EPS 腰斬，倍數同步壓縮，股價回到 250 週均線附近（約 −76%）","ruling":"部分採納：已納入 Bear 35% 與回撤下緣 −75%。與唯一致命點重疊（首次降價就是這個故事的起點），不另設事件","watch":"單季毛利率、月營收年增率、同業法說會的價格說法","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"],"fact_refs":["f_kpi1_gaap","f_ma_w250"]},{"view":"論點失敗","evidence":"共同封裝光學「光進銅退」的議題升溫，市場擔心削弱 M8、M9 等高階 CCL 的需求","assumption":"交換器上的長距離電傳輸仍需要高階 CCL","consequence":"交換器材料成長放緩，高階占比與毛利率提前見頂","ruling":"部分採納：交換器只是基礎設施營收的一部分，伺服器運算板與載板材料不受直接影響，且目前沒有用量下滑的數字。列為長期風險，不調整 Base","watch":"主要交換器平台採用共同封裝光學的時程、公司對交換器材料營收的說法","evidence_refs":["substitute_technology#0","supply_demand_durability#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流對淨利比 2024、2025 年都約 0.14，TTM 自由現金流率 −2.9%，2026Q2 自由現金流 −28.4 億元；原物料存貨一年多增加 132%；稀釋股數三年年均 +1.7%","assumption":"擴產的增量報酬維持在 40% 以上，現金流在 2028 年後轉正","consequence":"營收與 EPS 都達標，但新產能在降價期投產，增量報酬掉到資金成本附近，自由現金流長期為負，要靠舉債或增資撐；股東的每股價值成長低於 EPS 成長","ruling":"採納：已反映在資本配置評分偏弱與長期信心「中」；以淨負債與增資列入監測","watch":"自由現金流、淨負債、新股或可轉債的發行","evidence_refs":["cyclical_inventory_price_position#0","cyclical_supply_discipline_capacity#0"],"fact_refs":["f_kpi5","f_peer_2383_tw_fcf_margin_pct","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"trailing 本益比 73.13 倍、P/S 10.08 倍，都在近四年最高；FY1 共識三個月上修 19.94%；3 月時法人目標價 3,000–3,600 元，現價已經遠高於此（最新目標價事實表沒有）","assumption":"市場用 2027–2028 年景氣高點的獲利給倍數","consequence":"就算 2027 年 EPS 達到共識，倍數也會在 2028 年供給增加之前開始收斂，股價橫盤或下跌","ruling":"採納：五年基本情境年化只有約 5–6%，是觀望的主因","watch":"股價對 2027 年基本 EPS 的倍數、共識修正的方向","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_pe_current","f_ps_current","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-75,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 5055.0 → 本次 4675.0（-7.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=5055.0","side_b":"本次 price_at_dd=4675.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 5,055 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 5,055 元：Bull 價 12,960、Bear 價 2,025，五年期望值 +24.9%，基準年化 5.8%，不對稱比 1.5","side_b":"本次情境、股價仍用 5,055 元：Bull 價 14,400、Bear 價 2,040，五年期望值 +24.5%，基準年化 3.5%，不對稱比 1.77","ruling":"先換情境、股價不動：五年期望值少 0.4 個百分點，基準年化少 2.3 個百分點。不對稱比由 1.5 變為 1.77。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 5,055 元：五年期望值 +24.5%，基準年化 3.5%，不對稱比 1.77","side_b":"本次情境、股價 4,675 元：五年期望值 +34.6%，基準年化 5.1%，不對稱比 2.11","ruling":"再換股價、情境不動：起點價下跌 7.5%，五年期望值多 10.1 個百分點，基準年化多 1.6 個百分點，不對稱比由 1.77 升到 2.11。合計五年期望值比前份多 9.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"供需：未來兩年緊張 vs 2.6 倍擴產","cause":null,"prior_field":null,"side_a":"管理層（2026-10-29 第三季法說，媒體轉述）：未來兩年 CCL 市場仍緊張，產能滿載，LTA 訂單已超過新增產能。業界稱中高階 CCL 到 2028 年供不應求","side_b":"公司 2030 年月產能 1,525 萬張（2.6 倍），台燿 2028 年 530 萬張，上游 2H27 放量；2026 年資本支出券商轉述 320 億元，高於 3 月指引上緣的 230 億元","ruling":"可調和，屬程度差異，兩邊說的是不同時間窗。2027 年採信管理層，2028 年以後採信供給增加的風險：Base 的 2027 年貼近共識，2028 年比共識低 14%","evidence_level":"公司法說會的媒體轉述加上產業報導，沒有逐字稿","settle_metric":"2027 年各季毛利率，以及管理層對 2028 年 LTA 價格的說法","if_then":["若 2027 年上半年單季毛利率 ≥38%、管理層表示 2028 年 LTA 價格不降，且股價跌到 3,750 元以下，則重跑研究後分批反買，首倉 ≤3%","若股價先漲回 5,000 元以上，但 2028 年的價格證據還沒出來，則不追","若任一季毛利率季減 ≥3 個百分點且管理層提及降價，則清倉（若持有），並取消進場條件"],"evidence_refs":["supply_demand_durability#3","supply_demand_durability#4","supply_demand_durability#0","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#2"]},{"axis":"替代技術：共同封裝光學 vs M9 與載板材料","cause":null,"prior_field":null,"side_a":"共同封裝光學升溫，市場擔心削弱 M8、M9 在交換器上的需求","side_b":"M9 2026 下半年量產、2027 年放量；載板材料年底認證、2027 年出貨，毛利率預期超過 50%；M7 以上占營收 65–70%","ruling":"可調和：替代風險針對的是交換器的長距離傳輸，載板材料反而可能受惠於封裝演進；目前沒有用量下滑的數字，風險時間在 2028 年以後","evidence_level":"分析文與法說會轉述","settle_metric":"公司對交換器材料營收的說法、載板材料 2027 年的出貨量","if_then":["若主要交換器平台量產共同封裝光學，且公司交換器材料營收連 2 季下滑，則 Bear 機率上調到 40%，停止加碼","若載板材料 2027 年如期出貨且毛利率超過 50%，則五年後跑道上調一檔，但仍不追高"],"evidence_refs":["substitute_technology#0","supply_demand_durability#1","substitute_technology#1","supply_demand_durability#2"]},{"axis":"獲利暴增 vs 現金流為負","cause":null,"prior_field":null,"side_a":"2026Q2 EPS 27.55 元，年增 184%；營業利益率 26.94%","side_b":"同一季自由現金流 −28.4 億元，TTM 自由現金流率 −2.9%；原物料存貨一年多增加 132%","ruling":"可調和：負現金流來自擴產與為新平台備料，是成長期的現象。但如果 2028 年後的降價期仍為負，就變成股東經濟惡化","evidence_level":"財報（yfinance）加上優分析報告","settle_metric":"2027 年全年自由現金流是否轉正","if_then":["若 2027 年自由現金流仍為負，且淨負債超過 500 億元，則下修長期信心，並減碼（若持有）"],"evidence_refs":["cyclical_inventory_price_position#0","cyclical_supply_discipline_capacity#0"]},{"axis":"現在就買的最強論證（觀望方的自我反駁）","cause":null,"prior_field":null,"side_a":"現價只有 2027 年共識 EPS 的 17.1 倍、2028 年的 10.6 倍；LTA 超過新增產能，全球份額第一；前份判斷日（10-20）以來，股價從 5,055 元跌到 4,675 元，RSI 38；第四季毛利率指引 38–39.5%，高於第二季的 33.85%","side_b":"這些都是 2027 年以前的證據。五年報酬取決於 2028–2030 年那 2.6 倍產能能用什麼價格賣出；現價已經用 2027–2028 年的高點獲利定價，五年基本情境年化只有約 5–6%","ruling":"不採信為進場理由：近端證據強，但不足以補償遠端的供給風險；用價格錨等待","evidence_level":"法說會轉述加上共識快照","settle_metric":"股價對 2027 年基本 EPS 的倍數","if_then":["若股價 ≤3,750 元且最近一季毛利率 ≥36%，則重跑研究後分批反買"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","capital_markets_pricing#2"]},{"axis":"前份漂移：價格與結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份 2026-10-20：股價 5,055 元，結論觀望；品質與估值的綜合評級 B，估值偏貴（橘）","side_b":"本次 2026-11-02：股價 4,675 元（跌 7.5%），2027 年共識本益比 17.1 倍，五年基本情境年化約 5–6%；估值仍偏貴，綜合評級維持 B，結論維持觀望","ruling":"這次下跌不足以改變結論：7.5% 的跌幅只讓五年年化報酬多出約 1.6 個百分點，仍低於 8%","evidence_level":"價格資料","settle_metric":"股價對 2027 年基本 EPS 的倍數","if_then":["若股價跌到 3,750 元以下，且最近一季毛利率 ≥36%，則重跑研究後分批反買"],"evidence_refs":[]},{"axis":"前份漂移：護城河、陷阱、跑道、類型、循環位置","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河擴大，價值陷阱風險中等（黃），五年後跑道中等（黃），循環／商品型，中循環","side_b":"第三季法說（2026-10-29）的新資訊：第四季毛利率指引 38–39.5%，產能利用率 100%，LTA 超過新增產能，2030 年月產能 1,525 萬張，載板材料年底認證。份額證據（全球第一、Google、輝達）不變。五欄全部維持","ruling":"新證據是雙向的：近兩年轉好（毛利率指引、LTA），與 2028 年後的供給風險（2.6 倍擴產）同時加重，方向互相抵銷，所以維持原判","evidence_level":"法說會轉述加上產業報導","settle_metric":"第四季毛利率、2027 年產能利用率","if_then":["若第四季毛利率低於 36%，則中循環改判晚循環，不進場"],"evidence_refs":["supply_demand_durability#3","cyclical_supply_discipline_capacity#0","substitute_technology#1"]},{"axis":"前份漂移：機率與最大回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭機率 20%，空頭 35%，最大回撤 −70%（單點）","side_b":"本次：機率維持 20／45／35；最大回撤改用範圍，−50% 到 −75%，由 104 週與 250 週均線的距離，以及 Bear 終點推導","ruling":"機率不動：擴產的新證據加重了空頭，但第四季指引與 LTA 也加重了多頭，兩者相抵。回撤改用範圍是方法上的改動；下緣 −75% 比前份的 −70% 深，因為目前離 250 週均線約 76%","evidence_level":"情境推導","settle_metric":"均線距離與 Bear 終點","if_then":["若股價跌破 104 週均線，則重新檢查空頭機率是否應上調"],"evidence_refs":[]},{"axis":"進場條件門檻變動（進場價與毛利率門檻）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價 ≤4,300 元（約 2027 年基本情境每股盈餘 215 元的 20 倍）且單季毛利率 ≥32%","side_b":"股價 ≤3,750 元（2027 年基本 EPS 260 元約 14.4 倍，貼近 52 週均線）且最近一季毛利率 ≥36%","ruling":"進場門檻從固定 20 倍，改成用五年基本情境年化 ≥10% 反推：Base 2031 年的 6,000 元，以 10% 折回五年約 3,725 元，取 3,750 元。2027 年基本 EPS 從 215 元上修到 260 元，是新證據帶動（第四季毛利率指引、FY2 共識上修）；但 2.6 倍的擴產讓 2027 年 EPS 更像景氣高點，不宜再給 20 倍。毛利率門檻從 32% 上調到 36%：第四季指引已經到 38% 以上，跌回 36% 以下就代表漲價退潮","evidence_level":"情境推導","settle_metric":"股價與最近一季毛利率","if_then":["若兩個條件同時成立，則重跑研究，通過後以首倉 ≤3% 進場","若只有價格條件成立，毛利率卻低於 36%，則不追，視為降價訊號"],"evidence_refs":["cyclical_supply_discipline_capacity#0"]},{"axis":"Single Thing 變動（新設唯一致命點）","cause":"新證據","prior_field":["single_thing"],"side_a":"前份沒有設唯一致命點（空白）","side_b":"2027 年底前，台光電或主要同業首次對 M8／M9 等高階 CCL 宣布調降合約價","ruling":"第三季法說會核准了 2030 年 1,525 萬張的擴產，加上同業泰國廠與上游 2H27 放量，這些新證據讓價格成為數學上最大的單一敏感項，所以新設。發生時減碼一半；毛利率低於 32% 就清倉","evidence_level":"法說會轉述加上產業報導","settle_metric":"每季法說會的價格說法","if_then":["若首次降價發生，則取消進場條件，並減碼（若持有）"],"evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3"]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份沒有設清倉／減碼指標（空白）","side_b":"單季毛利率連 2 季 <32%；月營收年增率連 2 個月 <30%；高階 CCL 降價；產能利用率 <85%；淨負債 >500 億元，或宣布增資","ruling":"前份只有進場條件，沒有退出指標；本次補上，觸發時依各指標減碼或清倉","evidence_level":"方法補強","settle_metric":"各項指標","if_then":["若毛利率連 2 季 <32%，則清倉（若持有）","若月營收年增率連 2 個月 <30%，則減碼三分之一（若持有）"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"第四季毛利率驗證漲價是否延續","type":"假設驗證","maps_to":"H1","metric":"單季毛利率","threshold":"≥38%（指引 38–39.5%）","action":"達標就維持 Base；低於 36%，2027 年 Base EPS 下修到 230 元，Bear 機率上調到 40%","source_freq":"季報與法說會（每季）","date":"2027-03"},{"n":2,"text":"高階材料占比與載板材料出貨","type":"假設驗證","maps_to":"H3","metric":"M7 以上占營收比；載板材料出貨","threshold":"占比 ≥65%；2027 年內開始出貨","action":"未達標，五年後跑道下調一檔","source_freq":"法說會（每季）","date":"2027-08"},{"n":3,"text":"擴產期產能利用率守不守得住","type":"假設驗證","maps_to":"H2","metric":"產能利用率","threshold":"≥85%（第三季 100%）","action":"連 2 季低於 85%，Base 的 2029–2031 年 EPS 下修兩成","source_freq":"法說會（每季）","date":null},{"n":4,"text":"高階 CCL 首次降價","type":"Single Thing","maps_to":"Single Thing","metric":"公司或台燿、聯茂對 M8／M9 合約價的說法","threshold":"任何一家宣布調降","action":"取消進場條件，Bear 機率上調到 45%；若持有，先減碼一半，下一季毛利率 <32% 就清倉","source_freq":"法說會、產業報導（每季）","date":"2027-12","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3"]},{"n":5,"text":"產能洪水壓價","type":"風險","maps_to":"R1","metric":"單季毛利率","threshold":"年減連 2 季，或季減 ≥3 個百分點且提及降價","action":"若持有就減碼一半；沒有持有就不進場","source_freq":"季報（每季）","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"]},{"n":6,"text":"共同封裝光學侵蝕交換器用量","type":"風險","maps_to":"R2","metric":"交換器平台是否採用共同封裝光學；公司交換器材料營收","threshold":"已量產採用，且交換器材料營收連 2 季下滑","action":"Bear 機率上調到 40%，停止加碼","source_freq":"法說會、產業報導（每季）","date":null,"evidence_refs":["substitute_technology#0","supply_demand_durability#1"]},{"n":7,"text":"月營收轉弱","type":"減碼","maps_to":"R3","metric":"月營收年增率","threshold":"連 2 個月 <30%","action":"若持有就減碼三分之一；沒有持有就不追","source_freq":"公開資訊觀測站月營收（每月 10 日前）","date":null},{"n":8,"text":"擴產資金壓力","type":"風險","maps_to":"R4","metric":"淨負債；新股或可轉債發行","threshold":"淨負債 >500 億元，或宣布增資","action":"長期信心降為低，持有者減碼","source_freq":"季報、重大訊息","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#0"]},{"n":9,"text":"股價回到進場區","type":"估值rearm","maps_to":"H1","metric":"股價；最近一季毛利率","threshold":"股價 ≤3,750 元，且毛利率 ≥36%","action":"重跑研究後分批反買，首倉 ≤3%","source_freq":"股價每日、財報每季","date":null},{"n":10,"text":"第四季財報後複審","type":"複審日期","maps_to":null,"metric":"第四季財報與 2027 年展望","threshold":"財報公布","action":"重跑研究","source_freq":"一次","date":"2027-03"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"<32%（2026Q2 為 33.85%，第四季指引 38–39.5%）","window":"連續 2 季","source":"公司季報、法說會","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"<30%（2026 年 9 月為 168.9%）","window":"連續 2 個月","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"高階 CCL（M8／M9）合約價","bear_threshold":"公司或主要同業宣布調降","window":"任一季","source":"法說會、產業報導","last_status":"ok"},{"metric":"產能利用率","bear_threshold":"<85%（第三季 100%）","window":"任一季","source":"法說會","last_status":"ok"},{"metric":"淨負債與股本","bear_threshold":"淨負債 >500 億元（目前 152.2 億元），或宣布發行新股、可轉債","window":"任一季","source":"季報資產負債表、重大訊息","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=3.33, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價 ≤3,750 元（2027 年基本 EPS 260 元約 14.4 倍，貼近 52 週均線）且最近一季毛利率 ≥36%","exec_line":"兩個條件同時成立後重跑研究；通過後分兩批建立：第一批不超過總資產 1.5%，第二批等下一季毛利率仍 ≥36%，合計上限 3%"},"reasoning":{"industry":"最新一季（2026Q2）營收 472.75 億元，毛利率 33.85%，營業利益率 26.94%，EPS 27.55 元。9 月營收 215.32 億元，年增 168.9%；前 9 月累計 1,412.27 億元，年增 103.7%。第三季財報已在 10-28 公布，但事實表沒有第三季損益，本包也沒有逐字稿，只有法說會的媒體轉述：第三季產能利用率 100%，第四季營收指引季增 15–20%，毛利率 38–39.5%。\n\n營收結構：基礎設施（AI 伺服器、交換器、低軌衛星）在 2025Q4 約占 65–70%，公司估 2026 年升到 70–80%；M7 等級以上材料占營收 65–70%；行動裝置與車用工業的占比，事實表沒有。2026 年的成長以漲價為主（第二季起調漲 10% 以上），2027 年起價量齊揚。\n\n產業時鐘判在第二階段（擴張）：需求仍大於供給，LTA 訂單超過新增產能；但 2.6 倍的擴產計畫已經出現，已接近過熱的前段。\n\n議價權：上游的 HVLP 銅箔、低介電玻纖布、T-glass 在 2H27 前都吃緊，上游議價力強；下游客戶接受漲價，兩大客戶各占 14%、12%，沒有到 40% 的集中門檻。單點依賴不在客戶端，而在上游關鍵材料；前三大供應商占比，事實表沒有。\n\n產業態勢三軸：\n- 競爭面：同業台燿 2028 年產能翻倍，上游 2H27 放量，屬惡化中。\n- 結構面：AI 帶動高速材料，LTA 覆蓋新增產能，屬轉好中。\n- 其他變數：替代技術「共同封裝光學」。\n\n裁決為雙向拉鋸：2027 年前結構轉好佔上風，2028 年後競爭與替代技術的風險上升。AI 高速材料的需求是長期的，但價格跟著供需走，所以整體用循環鏡頭看。","moat":"機制是三者疊加：高速低損耗配方、平台級材料認證、最大產能。\n\n投入資本事實表沒有，所以用份額與毛利率代替 ROIC 差距來判方向：\n- 對聯茂：TTM 毛利率高約 15 個百分點（31.06% 對 15.82%），營業利益率高約 14 個百分點。\n- 對生益科技：TTM 毛利率 33.54%、營業利益率 23.41%，與台光電相近；但期間晚一季，又含 PCB 子公司，不能直接比。\n- 台燿：財報在事實表中沒有資料。\n\n執行面給 8 分：產能、認證速度與份額都有證據。定價力給 7 分：第二季漲價 10% 以上，毛利率季增 4.3 個百分點；但這發生在上游缺料、產能滿載的期間，2028 年供給放量後守不守得住，沒有證據。同業 ROIC 差距無法驗證，與生益的利潤率差距接近零，所以整體不給到 8 分以上。\n\n報酬持續期：當期營業利益率 26.94%，稅後淨利率 20.88%，周轉率是資料缺口。四個檢查點中，需求、決策層級、價值鏈三項為黃，社會容忍度為綠。\n\n增量報酬：以淨利增量除以淨再投資（淨利減自由現金流）粗估，約 40–60%；再投資率約 86%；內生成長上界約 35–50%，取 40%。這個代理數字沒有扣掉漲價的貢獻，偏高。","growth":"成長來源：2026 年以價為主；2027 年起價量齊揚，月產能從 2026 年底的 615 萬張增至 2027 年底約 930 萬張。沒有併購，也沒有回購。\n\n三年共識 EPS：2025 年實際 40.81 元 → 2026E 133.85 → 2027E 273.24 → 2028E 441.28，年複合約 121%（(441.28÷40.81)^(1/3)−1）。EPS 的分析師家數事實表沒有；營收的分析師為 13 到 17 家。\n\n內生成長上界約 40%（見護城河段），缺口約 81 個百分點，歸因於毛利率擴張，不是回購或併購：毛利率從 2025 年 29.83% 升到第四季指引 38–39.5%；淨利率從 2025 年 15.5% 升到共識隱含的 2027 年約 26%。\n\n共識近三個月把 FY1 上修 19.94%，但最近兩份快照的 FY3 轉為下修 1.45%。\n\n衰退信號十項中亮兩項：EPS 成長明顯高於營收成長；自由現金流對淨利比連兩年低於 0.75。價值陷阱風險與長期成長性都判為黃。因滲透率資料缺口，跑道年數無法估。","governance":"現金去向（2022–2025 年度財報）：營業現金流大部分流進資本支出與存貨。自由現金流 2022 年 9.5 億元、2023 年 −13.6 億元、2024 年 13.5 億元、2025 年 20.9 億元；2026Q2 為 −28.4 億元（營業現金流 23.4 億元，資本支出 51.8 億元）。\n\n資本支出：2026 年券商轉述約 320 億元，高於公司 3 月指引的 150–230 億元；2027–2030 年約 986 億元。原物料存貨從 2025Q1 的 67.8 億元增到 2026Q2 的 157.4 億元，法人說是為新平台策略性備料。\n\n負債：目前淨負債 152.2 億元，相對市值 1.68 兆元很小。但擴產期若現金流持續為負，舉債或發行可轉債的機率會上升。\n\n現金去向四分：再投資幾乎全部，股息極少，回購零，併購零。\n\n計分卡：\n- 併購：近 12 個月沒有，不適用。\n- 回購：沒有，不適用。\n- 稀釋：以年度淨利除以稀釋 EPS，推得股數 2022 年 3.414 億股、2025 年 3.590 億股，年均 +1.7%，高於 1.5% 的標準；近一年持平（2026Q2 約 3.584 億股）。稀釋來源是員工酬勞還是可轉債轉換，事實表沒有。\n\n營運槓桿：2025 年營收年增 46.4%，營業利益年增約 57%，沒有壓縮。","valuation":"倍數：trailing 本益比 73.13 倍、P/S 10.08 倍、EV/S 10.17 倍，都在近四年年度端點的最高。前瞻本益比：FY1 34.93 倍、FY2 17.1 倍、FY3 約 10.6 倍；前瞻 EV/S 7.91 倍。\n\n前瞻倍數看起來便宜，但分母是漲價後毛利率 38% 以上、產能滿載下的景氣高點獲利，這正是本案的爭點，所以不構成便宜的論證。循環股應優先看股價淨值比，但淨值事實表沒有；同業倍數也沒有，只能用自身倍數對照。PEG 用 FY1 本益比 34.93 除以三年共識 EPS 年複合 121%，約 0.29；對循環股的高點成長沒有參考價值。\n\n情境（機率 20／45／35）：\n- Base：2031 年 EPS 400 元×15 倍＝6,000 元，五年約 +28%。\n- Bull：720 元×20 倍＝14,400 元。\n- Bear：170 元×12 倍＝2,040 元，約 −56%。\n\n成長熄火壓力測試：以 Base 的 2028 年 EPS 380 元為起點，之後三年成長降到 15%／10%／5%，本益比相應壓到 18／12／9 倍，五年後約 10,400／6,070／3,960 元；三種裡有兩種高於現價。\n\n動能：週線多頭排列，股價比 52 週均線高約 26%；RSI 38.35，26 週報酬 3.33%，沒有過熱。","premortem":"最強的三個反駁：\n1. LTA 已超過新增產能，2027 年獲利能見度高，現價只有 FY2 的 17 倍。\n2. 份額第一、認證最早，降價時最後受傷的是龍頭。\n3. 載板材料毛利率超過 50%，2027 年起是第二條曲線。\n\n這三點對 2027 年的部分我都採信，但都沒有回答：2028–2030 年供給增加 2.6 倍時，價格會怎樣。\n\n上一輪下行（2023 年首季）營收年減 26%，毛利率 21.36%；兩個季度後的 2023 年第三季，毛利率 30.2% 就創新高。這顯示龍頭恢復得快，但跌幅是真的。\n\n回撤範圍：回到 104 週均線約 −52%，回到 250 週均線約 −76%，Bear 終點約 −56%，取 −50% 到 −75%。論點本身不脆弱：護城河在擴大、跑道中等、報酬不靠倍數擴張。所以要對深回撤有心理準備，但不因波動本身砍倉。"},"plain":{"six":{"how_it_makes_money":"賺的是 AI 伺服器與交換器電路板用高速銅箔基板的錢。錢卡在兩個節點：平台用哪一級材料，由輝達與雲端客戶在設計時指定；台光電認證最早、產能最大，所以拿到份額，還能漲價。","moat":"護城河在擴大。執行面有份額證據：2025 年升為全球 CCL 第一，Google 與輝達的份額都看增。定價力目前也在擴大，但其中一部分是景氣給的，評 B 級。","growth":"五年後的跑道屬中等。高速材料還在升級（M9 2027 年放量，載板材料 2027 年起出貨）；但滲透率事實表沒有，第二條成長曲線還沒驗證，還有共同封裝光學的替代風險。","capital":"資本配置評分偏弱，原因是幾乎全數回投產能：2024、2025 年自由現金流都只有淨利的 14%，TTM 轉負；股息殖利率 0.5%，沒有回購，股數三年年均稀釋約 1.7%。目前回投報酬高，但 2027–2030 年約 986 億元的擴產，是在景氣高點下注。","valuation":"現價 4,675 元要求兩件事：2027 年 EPS 達到共識的約 273 元；2028 年後產能擴到 2.6 倍時，毛利率不大幅回落。我信前一件，不信後一件。五年基本情境年化約 5–6%，不追，等 3,750 元附近，或擴產期毛利率站穩的證據。","how_wrong":"最可能看錯的地方，是把 2026–2027 年漲價後的毛利率當成常態：2.6 倍的擴產集中在 2028–2030 年，一旦降價，EPS 與倍數會同時下修，回撤可能到 −50% 至 −75%。反方向的錯，是低估 AI 材料升級的速度，讓擴產全數賣完。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"追蹤","wait_for_price":true,"wait_for_price_condition":"股價 ≤3,750 元，且最近一季毛利率 ≥36%；條件成立後重跑研究，再談首倉","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":4675.0,"week26_return_pct":3.33,"consensus_rev_3m_pct":19.94,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"2027–2028 年的共識 EPS，建立在漲價後毛利率 38% 以上與產能滿載上，是景氣高點的獲利；用它算出的 17.1 倍、10.6 倍，不能當成便宜的證據"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"product","event":"載板材料完成客戶認證（公司目標年底）","impact":"中","watch":"認證是否如期，以及 2027 年出貨規模"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"月產能提升到約 615 萬張；美國加州 Arlon 擴建後開始營運","impact":"低","watch":"第四季營收能否達到季增 15–20% 的指引"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"2026 年第四季財報與 2027 年展望法說會","impact":"高","watch":"第四季毛利率是否 ≥38%，2027 年價格與 LTA 的說法，2028 年報價"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"M9 材料放量","impact":"高","watch":"高階占比、毛利率"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"月產能目標約 930–945 萬張；上游玻纖布新產能 2H27 投產，台燿泰國廠擴產","impact":"高","watch":"利用率能否守在 85% 以上，是否出現降價"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,192B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2383.TW_20261102/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期</h2>
<p class="lead">護城河評 B 且向上，但定價力有一部分是景氣給的。</p>
<ul class="pts">
<li>護城河機制是三者疊加：高速低損耗樹脂配方、平台級材料認證、全球最大產能。輝達與雲端客戶每一代平台都指定材料等級，認證最早又供得出量的廠商拿走份額。轉換成本只鎖一個平台世代，約一到兩年，下一代重新競爭。</li>
<li>趨勢向上有具體證據。Prismark 顯示 2025 年台光電營收升為全球 CCL 第一，2024 年是第三，超越生益與建滔。外資稱 Google 需求下對手產能不足，台光電可拿更多份額。沒有最大客戶份額下滑的證據。</li>
<li>打分上，執行面給 8，因為產能、認證速度與份額都有證據。定價力給 7，因為第二季漲價 10% 以上，毛利率季增 4.3 個百分點，但這發生在上游缺料、產能滿載的期間。2028 年供給放量後守不守得住，沒有證據。綜合 7.5，護城河等級 B。</li>
<li>對手比較受限於資料。聯茂 TTM 毛利率 15.82%，台光電高約 15 個百分點。生益科技 TTM 毛利率 33.54%、營業利益率 23.41%，與台光電相近，但期間晚一季又含 PCB 子公司，不能直接比。台燿的季損益沒有資料，斗山未列入同業表。</li>
<li>報酬持續期用代理數字估。2025 年淨利增加 50.7 億元，除以 2024 年淨再投資 82.3 億元約 62%，除以 2025 年的 125.6 億元約 40%。再投資率約 86%，內生成長上界約 35–50%，取 40%。限制是這個增量含漲價貢獻，數字偏高。</li>
<li>威脅有三條。第一，產能洪水，機率 35%，2028 年起高階 CCL 有降價風險。第二，共同封裝光學縮短交換器板上的電傳輸，機率 30%，影響 M8、M9 的交換器用量，伺服器運算板與載板材料不受直接影響。第三，客戶找第二供應商，機率 20%，斗山與台燿都是現役競爭者。</li>
</ul>
<h3>二維評分與 Moat-to-Numbers</h3>
<!-- E5 -->
<h3>§5.F　對手財務深度對照</h3>
<!-- E6 -->
<h3>§5.R　報酬持續期檢核</h3>
<!-- E7 -->
</section>

```