你是 stock-analyst v20 的**散文層（prose）agent**，標的 STX（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20261102/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：STX　日期：2026-11-02　archetype：None　前份裁決：2026-09-23　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1901B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（523B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1002B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1575B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1528B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（370B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（879B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2216B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3223B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2925B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1901           3569-5099      5 條（2–6 內）  
s3                  8000         523           5234-7477      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4105          7626-10895      5 條（2–6 內）  
s6                 11000         370          7441-10630      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         879           1835-2621      5 條（2–6 內）  
s10                 5000        2216           1949-2784      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2925           2000-2075      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5259B；至少需散文≈39.74KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−75%
−70%
−68
−68%
−45%
−45
−43%
−29.5%
−11.2%
−11.19
−5.8%
−4.8%
−0.6%
0
0.12
0.14%
0.19
0.2
0.20
0.47
0.5%
0.56
0.58
0.7%
0.75
0.76
0.98
01
1
1.05
1.1
1.14
1.5%
1.71
1.75
02
2
2.1%
2.11
2.13
2.64
3.0%
3%
03
3
3.3%
4%
4
4.8
5%
5
5.68
5.69
06
6
6%
6.3%
6.9
07
7
7.30
7.36
7.4
7.5
7.68
7.84
8.0%
8
8%
8.18
9.0
9
09
9.20
9.5%
9.7%
9.9
9.91
10
10%
10.72
11%
11
11.4
12
12.1%
13%
13
13.8
13.90
13.9
14
14%
14.69
15%
15
15.4
15.4%
15.97
16%
16
17
17%
18%
18
19%
19.15
20%
20
21%
21
22
23
24
24%
25
25%
25.6
26
27
28
29%
29.5%
30%
30.3%
31
31.05
31.84
32
33%
33.8
34%
34
34.65%
35%
35
35.78
36.29
36.9%
37%
37.4
38
40%
40
40.35
40.5%
41
42%
42
42.26
42.3
44
45%
45
45.3
47%
47.0%
47
47.8%
48
49
50%
50.4%
50.7%
51%
52
52%
52.7%
53.3%
55%
55
55.7%
56%
57%
57.3
57.8%
58
59.1
60
60%
61%
61.7%
62
63%
65.07
66%
68.0%
70%
70
72
74
74.6%
75%
76
76.3%
78
80.7%
81%
83
84.5%
87.28
90
90%
91
95
95%
97
100%
100
104
112
116%
125
138
150%
195
198
200
203
206
218
220
229
231
233
235
240
250
280
285
300
336
355
367
400%
450
510
$572
606
644
644.58
000660
726
744
806
829
898
914.72
2011
2023
2025
2026
2027
2028
2029
2030
005930
20261102
1,014
1,480
1,620
1,660
1,920
2,070
5,400
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
{"meta":{"ticker":"STX","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Seagate Technology Holdings plc"},"oneliner":"HAMR 與多年長約讓 Seagate 賺到創紀錄的價差，但毛利擴張已改由漲價推動、對手開始擴產；股價回到前份重跑區間，估值轉為中性，等 CY2028 長約定價定案再談建倉。","thesis":{"H":[{"id":"H1","text":"定價延續：長約與 build-to-order 讓每 EB 單價在 CY2027 繼續上升，FY2027 與 FY2028 的獲利大致照共識兌現","2y":"FY2027 非 GAAP EPS ≥38，FY2028 ≥58；FY2027 每季非 GAAP 毛利率不低於前一季","5y":null,"10y":null,"threshold":"FY2027 非 GAAP EPS ≥38（約為共識 40.35 的 95%）；每 EB 營收（營收÷總出貨 EB）年增 ≥15%，維持到 CY2027 底","source":"公司每季財報新聞稿與法說（營收、EB、毛利率、EPS）；Koyfin 共識快照","drift_rule":"2 年期：實際值對門檻連 2 季偏離 ≥5% 視為削弱，連 3 季偏離 ≥10% 視為反轉"},{"id":"H2","text":"量能複利：HAMR 讓 nearline EB 供給年增約 25%，資本支出守在營收 4%～6%","2y":null,"5y":"FY2027–FY2031 總出貨 EB 平均年增 ≥20%；Mozaic 5 在 CY2027 底開始送樣；資本支出不超過營收 6%","10y":null,"threshold":"總出貨 EB 年增 ≥20%（FQ1 FY27 為 21%）；CY2026 底 HAMR 占 nearline EB 出貨約 50%；資本支出÷營收 ≤6%","source":"法說 prepared remarks 中的 EB 與 HAMR 占比；現金流量表的資本支出","drift_rule":"5 年期：連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"},{"id":"H3","text":"長約讓循環變淺：下一輪下行時，毛利率谷底遠高於 FY2023 的 17%～21%","2y":null,"5y":"FY2027–FY2031 任一季非 GAAP 毛利率都不低於 35%；長約配置的能見度維持在未來 2 年以上","10y":null,"threshold":"單季非 GAAP 毛利率 ≥35%；管理層揭露的長約配置期間涵蓋未來 2 年以上","source":"每季財報新聞稿的毛利率；10-K 對主採購協議與取消費用的描述；法說的長約說明","drift_rule":"5 年期：連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"產品轉換卡關：Mozaic 4 認證延後或良率爬坡太慢，12 月季 EB 沒有如管理層承諾明顯跳升，庫存天數繼續上升","h_ref":"H2","clock":"⚡","threshold":"12 月季總出貨 EB 低於 235，或庫存天數連 2 季高於 100 天","evidence_refs":["cyclical_inventory_price_position#1"]},{"id":"R2","text":"供給回應讓漲價見頂：對手 2027 年量產 HAMR、資本支出升向營收約 8%，第三家日本擴產，TDK 擴充磁頭產能，CY2028 以後單價停止上漲。前一輪下行時 FY2023 毛利率掉到 17%～21%，第三方也認為這波漲價可能是暫時的。","h_ref":"H1","clock":"🔥","threshold":"每 EB 營收連 4 季年增低於 5%，或 CY2028 定價低於 CY2027","evidence_refs":["supply_demand_durability#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#3","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","substitute_technology#4"]},{"id":"R3","text":"QLC SSD 替代：缺貨期間超大規模客戶改用功耗低約三成的 QLC SSD，缺口收斂後不再回流 HDD；能源效率需求也可能限縮大容量 HAMR 的上行空間","h_ref":"H2","clock":"🐢","threshold":"STX 資料中心 EB 年增連 4 季低於 15%，且管理層提到客戶改用快閃記憶體","evidence_refs":["substitute_technology#0","substitute_technology#3"]},{"id":"R4","text":"超大規模客戶消化庫存，重演 2023：最大客戶約占營收 14%；2023 年 nearline 採購大減，STX 營收年減 37%、全年虧損，產業 EB 年減約 29%，並產生 1.71 億美元產能閒置費用","h_ref":"H3","clock":"🔥","threshold":"管理層提到換貨、延後拉貨或觸發長約取消費用，或資料中心營收季減","evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5","customer_concentration_credit#0"]},{"id":"R5","text":"貿易、出口管制與供應鏈集中：關稅與出口管制（2023 年 BIS 罰 3 億美元，另附五年暫緩執行的拒絕出口令，至今仍按季付款）；稀土精煉約九成在中國，主軸馬達約八成來自單一日廠，控制晶片由台積電代工，組裝集中在泰國；外購零件漲價已抵掉部分降本，同業也提到半導體關稅可能擴及儲存硬體","h_ref":"H1","clock":"🔥","threshold":"單季非 GAAP 毛利率季減 200bp 以上，且管理層歸因於關稅、出口管制或外購零件","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#5","regulatory_antitrust#1","regulatory_antitrust#2","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#5","geo_supply_chain#6","geo_supply_chain#7","geo_supply_chain#8"]}],"single_thing":{"description":"CY2028 build-to-order 定價定案低於 CY2027，或管理層改為不按年鎖價","why_fatal":"毛利擴張此刻主要靠漲價（CFO 本季原話），每 TB 降本已放緩到個位數中段；FY2028 下半年與 FY2029 全年都落在尚未定價的期間。以 12 月季指引營收 48 億美元計，單價降 10% 約少 4.8 億營收，成本不變，幾乎全部從營業利益扣掉，約為單季營業利益的兩成；EPS 路徑會由 Base 掉到 Bear。","if_happens":"Bear 機率調到 45%，Base 的 FY2029 EPS 下修到 FY2028 水準以下；維持不建倉，若屆時已持有首倉則清倉","how_monitor":"2027 年 1 月底、4 月底、7 月底三次法說中的長約與定價說明；每季每 EB 營收（營收÷EB）的季變化；毛利率季變化","probability":"30%（12–24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":9.91,"peg_fy2":0.12,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":13.9,"FY2027E":40.35,"FY2028E":65.07,"FY2029E":87.28},"fy_end_month":6,"eps_basis":"共識為 Koyfin non-GAAP 稀釋 EPS（快照未列 EPS 分析師家數；營收共識為 21–22 位）。基期 FY2026A 用 GAAP 稀釋 EPS 13.90，因為事實表沒有全年 non-GAAP 數；基期偏低，三年年化成長因此偏高。財年止於 6 月底附近的週五。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20261102/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"FY2023 出現 GAAP 虧損；非 GAAP 毛利率由約 21% 擺到 57.8%，擺幅超過 35 個百分點；單價隨供需缺口大漲。長約拉長了能見度，但價格仍逐年重議。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性、將會反轉：長約配置與 Morgan Stanley 的缺口估計都指向缺貨延續到 2028 年。但 WDC 2027 年量產 HAMR、同業資本支出升向營收約 8%、Toshiba 日本擴產、TDK 磁頭擴產，代表供給可逆，CY2028 以後的價格不能外推。","bargaining":{"up":"上游：主軸馬達約八成出自單一日廠（第三方估計），控制晶片由台積電代工，磁鐵用稀土的精煉集中在中國。STX 自製磁頭與碟片，但外購零件漲價本季只轉嫁了一部分，而且有時間差。","down":"下游：資料中心占營收 81%，最大客戶約 14%。目前供不應求，客戶用多年長約換取供貨保障，議價權暫時在 STX 手上；CY2028 以後的價格仍要重談。","geo":"製造據點分布在中國、馬來西亞、北愛爾蘭、新加坡、泰國、美國，組裝集中在泰國。受美國關稅與出口管制約束，2023 年曾因出貨華為被罰 3 億美元。"},"profit_pool_dir":"利潤池目前流向 HDD 廠：STX 非 GAAP 毛利率由 FY2026 第三季的 47.0% 升到 FQ1 FY27 的 57.8%，外購零件漲價只吃掉一部分。但放在整個儲存利潤池看，MU、000660.KS、285A.T 的 TTM 營益率在 56%～75%，仍高於 STX 的 40.5%。","tam_table":{"expanded":false,"reason":"STX 的成長來自既有大容量儲存市場的量與價，不是低滲透、新品類或份額擴張。事實表只有 Coughlin 估 2026 年 HDD 產業營收超過 300 億美元這一個點，沒有 SAM、滲透率與利潤池占比，展開只會是空表。"}},"moat":{"mechanism":"三家寡占、自製磁頭與碟片、HAMR 面密度領先約一到兩年，再加上超大規模客戶的逐代認證與多年長約","execution":8,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行面擴大：HAMR 占 nearline EB 由約 40% 升到 CY2026 底約 50%，Mozaic 4 正在兩家 CSP 放量，Mozaic 5 進度提前。定價面持平：漲價來自供需缺口，外購零件成本轉嫁有時間差；STX EB 年增目標約 25%，低於產業供給增速估計 30%～35%；WDC 2027 年量產 HAMR，同業資本支出升向營收約 8%。兩面相抵。","peer_na_reason":"事實表同業表只收了記憶體與快閃記憶體廠（替代品供應商），直接的 HDD 對手 WDC 與 Toshiba 沒有財務數字，投入資本也未涵蓋，無法計算 ROIC 差距。","threats":[{"level":"🔴","text":"QLC SSD 生態攻擊：缺貨把 nearline 交期拉長到 52 週以上，快閃記憶體廠用功耗低約三成的大容量 QLC 切入。缺口收斂後，如果客戶的架構不回流，HDD 的 EB 成長會被永久削弱。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#3"]},{"level":"🟡","text":"HDD 對手的供給回應：WDC 40TB UltraSMR 2026 下半年推出、HAMR 2027 年量產、資本支出升向營收約 8%；Toshiba 日本擴產，TDK 擴充磁頭產能。屬點對點競爭，會壓縮 STX 的 HAMR 時間差與 CY2028 以後的定價。","p":"50%","evidence_refs":["substitute_technology#4","cyclical_supply_discipline_capacity#1","competitive_share_entrants#3"]},{"level":"🟡","text":"供應鏈與貿易政策：主軸馬達、控制晶片、稀土來源集中，組裝群聚泰國；關稅與出口管制可能推高成本，或限制可出貨的對象。","p":"20%","evidence_refs":["geo_supply_chain#5","geo_supply_chain#6","geo_supply_chain#7","geo_supply_chain#8","reg_tariff_export#2","reg_tariff_export#3"]}],"roic_durability":{"quadrant":"高利益率×周轉率資料缺口：FY2026 GAAP 營益率 34.65%，FQ1 FY27 非 GAAP 營益率 50.7%；投入資本（廠房、存貨、應收減應付）事實表未涵蓋，算不出周轉率。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端與 AI 應用，決策者是超大規模業者的基礎架構團隊，付款者是同一批業者。資料留存是需要不是想要，客戶已把規劃期拉到 2029–2030 年。但延後購買的代價客戶承受得起：2023 年同一批客戶大砍 nearline 採購，STX 營收年減 37%。急迫性高，持久性還沒經過下行驗證。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一世代硬碟的客戶認證這一層衡量：STX 與 WDC 都通過主要超大規模客戶的認證（WDC 40TB 已在兩家認證），客戶可以在兩家之間移量。10 碟平台讓換代認證比較簡單，長約與部分取消費用拉長了轉換週期，但構不成鎖定。"},{"item":"價值鏈分配","level":"🟡","text":"STX 自製磁頭與碟片，拿到了價差；但主軸馬達約八成出自單一日廠，控制晶片由台積電代工，稀土精煉集中在中國，外購零件漲價本季抵掉了部分降本。快閃記憶體同業的利潤率更高，代表在儲存價值鏈裡，HDD 不是議價力最強的一環。"},{"item":"社會容忍度","level":"🟢","text":"客戶是議價能力強的大型企業，產品不是民生必需品，沒有社會或政治面的漲價天花板，實際上限是經濟面的 QLC SSD 替代。優勢不依賴監管授權；政策風險在出口管制與關稅，2023 年 BIS 罰款已和解，目前按季付款。"}],"roiic":"無法精算（投入資本事實表未涵蓋）。FY2025 到 FY2026，GAAP 營業利益由約 19.15 億美元增到約 42.26 億美元（營收×營益率自算），增量約 23 億；同期資本支出 5.69 億美元。即使把資本支出全部算成新增投入，稅前增量報酬也超過 400%。這是漲價與稼動率回升的結果，不是新投入資本的報酬。","reinvest_rate":"低：FY2026 資本支出 5.69 億美元，約為淨利 31.84 億的 18%，扣掉折舊後更低（折舊與營運資金變動事實表未涵蓋）；管理層維持資本支出占營收 4%～6%。","endo_ceiling":25,"formula_note":"增量 ROIC×再投資率在漲價期會失真，改用實體上界：EB 供給年增約 25%（管理層目標，4%～6% 的資本支出可以支撐）×每 EB 單價持平，得出營收內生上界約 25%。共識 FY2027→FY2029 EPS 年化約 47%，超出的部分來自漲價帶動的毛利擴張與回購。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","STX":50.35,"MU":80.72,"000660.KS":76.27,"005930.KS":57.48,"285A.T":61.72,"unit":"%"},{"metric":"營業利益率","STX":40.49,"MU":74.59,"000660.KS":68.04,"005930.KS":36.88,"285A.T":55.7,"unit":"%"},{"metric":"FCF 利潤率","STX":30.13,"MU":44.27,"000660.KS":47.8,"005930.KS":28.95,"285A.T":30.28,"unit":"%"},{"metric":"研發密度","STX":5.57,"MU":4.24,"000660.KS":4.93,"005930.KS":9.7,"285A.T":null,"unit":"%"}],"competitors":[{"name":"MU","gm":80.72,"om":74.59,"fcf_margin":44.27,"rd_intensity":4.24,"strategy_note":"DRAM 與快閃記憶體廠，TTM 毛利率 80.7%、營益率 74.6%，遠高於 STX 的 50.4% 與 40.5%。在儲存利潤池的分配上拿得比 HDD 多，QLC SSD 是它切入 nearline 的工具。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"000660.KS","gm":76.27,"om":68.04,"fcf_margin":47.8,"rd_intensity":4.93,"strategy_note":"TTM 毛利率 76.3%、營益率 68.0%、FCF 利潤率 47.8%，同樣受益於記憶體缺貨。不是 HDD 對手，而是替代品的供應端。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"005930.KS","gm":57.48,"om":36.88,"fcf_margin":28.95,"rd_intensity":9.7,"strategy_note":"TTM 營益率 36.9%（多角化稀釋），研發密度 9.7% 為表中最高；是記憶體與 SSD 供應者，替代品來源之一。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"285A.T","gm":61.72,"om":55.7,"fcf_margin":30.28,"rd_intensity":null,"strategy_note":"TTM 毛利率 61.7%、營益率 55.7%、FCF 利潤率 30.3%；NAND 專業廠，是大容量 QLC SSD 的直接供給者。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量價並進、以價為主：EB 年增約 21%，每 EB 營收年增約 33%；2027 年起再加上回購。","runway_years":"事實表未涵蓋滲透率；長約能見度到 CY2028–CY2030","runway_post_y5":"🟡","endo_ceiling_basis":"引用報酬持續期段：EB 供給年增約 25%，單價持平下營收內生上界約 25%；資本支出維持營收 4%～6%。","segments":[{"item":"資料中心","value":"FQ1 FY27 營收 34 億美元，占 81%，年增 63%、季增 18%；出貨 198 EB，年增 24%；雲端 nearline 連續 12 季成長，企業 OEM 連續 6 季成長"},{"item":"Edge IoT","value":"FQ1 FY27 營收 7.84 億美元，占 19%，年增 52%、季增 13%"}],"decay_signals":[{"item":"毛利率連兩季年減","lit":false,"note":"非 GAAP 毛利率 57.8%，創新高"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"資料缺口：STX EB 年增 21%，產業同期年增事實表未涵蓋；2025 年 EB 份額約 42%"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"邊緣：每 EB 營收季增約 16%，EB 季增近零（218→220），但年增仍有 21%"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"FY2026→FY2028 共識 EPS 年化約 116%，營收約 51%，差距來自漲價擴毛利"},{"item":"FCF 對淨利連兩年低於 0.75","lit":false,"note":"FY2025 0.56、FY2026 0.98"},{"item":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"約 1.5%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"QLC SSD 威脅尚未反映在 STX 的 EB，持續監測"},{"item":"產業估值倍數近三年系統性下移","lit":false,"note":"倍數近年上移"},{"item":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"FY2026 資本支出 5.69 億美元，約為 FCF 的 18%"},{"item":"停止投資新產能且收入三年內下滑","lit":false,"note":"刻意不增台數，但靠面密度增加 EB，營收上升"}],"trap_rating":"價值陷阱風險 🟡（亮一個）；長期成長性 🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；回購放大的時點與規模已寫在本題判斷，近三年現金去向四分事實表未涵蓋，展開只會是空表。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年沒有重大併購（事件軸查無併購紀錄），不適用","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價與 10 年期公債殖利率事實表未涵蓋，無法對門檻判定；以現價計，FY2027E 前瞻盈餘收益率約 6.3%，trailing 約 3.0%","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY2026 SBC 2.13 億美元，約為現市值 1,480 億的 0.14%，遠低於每年 1.5%；股數小幅上升來自可交換票據交割，不是 SBC","grade":"過"}]},"valuation":{"basis":"以前瞻本益比（FY2027E 共識）為主，用中循環營益率回推的本益比對照","tier":"處於循環高點附近的硬體儲存廠","peers":{"expanded":false,"reason":"事實表同業表只有利潤率，沒有同業本益比或 EV/S；而且列入的是快閃記憶體廠，不是 HDD 對手，商業模式不同，不能當估值錨。改用 STX 自身的前瞻本益比與前份 16–18 倍區間對照。"},"fwd_pe":15.97,"peg":0.19,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"用前瞻獲利看偏便宜：FY2027E 15.97 倍、FY2028E 9.9 倍、FY2029E 7.4 倍。用中循環獲利看偏貴：假設營益率回到 35%，FY2027 共識營收 203 億美元對應 EPS 約 26，本益比約 25 倍；trailing P/S 10.72 倍、前瞻 EV/S 7.36 倍，等於把高點利潤率當常態。trailing 本益比 33.8 倍與 P/S 只落在 3–4 個年度端點的 30% 與 66% 位置，不是五年分位（五年連續分位事實表未涵蓋）。兩邊相抵為 🟡，而且分母本身是爭點，便宜的論證不成立。","upside_short_pct":15.4,"upside_mid_pct":57.3},"trap_analysis":{"verdict":"🟡","label":"衰退信號只亮一個：EPS 成長遠快於營收，而這正是本輪獲利的主要來源"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY2023 營收年減 37%，非 GAAP 毛利率 21%（單季低到 17%），全年虧損；產業 EB 年減約 29%，產能閒置費用 1.71 億美元。Coughlin 認為這波儲存漲價可能是暫時的。","assumption":"長約與 build-to-order 能防止 2023 年那種採購斷崖","consequence":"CY2028 定價下調，加上客戶消化庫存，FY2030 EPS 掉到 16 左右，股價回到 300 美元出頭，5 年虧損約五成","ruling":"採納：列為 Bear 情境（35%）。這條路徑與唯一致命點相同，兩者一致，不改寫。","watch":"每 EB 營收季變化、CY2028 定價、管理層是否提到換貨或延後拉貨","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5","supply_demand_durability#3"],"fact_refs":["f_kpi12_revenue_per_exabyte_asp","f_kpi15_nearline_exabyte_lta_bac"]},{"view":"論點失敗","evidence":"TrendForce：nearline 交期拉長到 52 週以上，QLC SSD 功耗低約三成，2026 年出貨可能爆發。快閃記憶體同業 TTM 毛利率 61%～81%，高於 STX 的 50%。","assumption":"缺口收斂後客戶會回到 HDD","consequence":"HDD 的 EB 成長由約 25% 降到 10% 出頭，量與價同時轉弱","ruling":"部分採納：列為長期風險，並在護城河評分中以生態攻擊扣分。目前 STX 資料中心 EB 仍年增 24%，管理層稱需求沒有被破壞，近兩年內不會是主因。","watch":"STX 資料中心 EB 年增率，以及法說是否提到客戶改用快閃記憶體","evidence_refs":["substitute_technology#0","substitute_technology#3"],"fact_refs":["f_peer_mu_gross_margin_pct","f_peer_285a_t_gross_margin_pct","f_peer_stx_gross_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"本季每 TB 成本降幅由過去約 15% 掉到個位數中段，外購零件比一年前貴；主軸馬達、控制晶片、稀土的供應集中；同業資本支出升向營收 8%；公司 2027 年起把 75% 自由現金流用在回購與股息。","assumption":"需求與漲價都照劇本走","consequence":"量價成長兌現，但零件商分走價差，資本支出被迫上調，回購又集中在循環高檔買進，每股價值的成長慢於獲利成長","ruling":"部分採納：目前零件成本被漲價抵掉還有剩（毛利率季增 510bp），但回購時點是真問題。在 FY2028 本益比約 10 倍、獲利接近高點時大舉回購，如果隨後轉為下行，就等於高價買回。","watch":"資本支出占營收是否超過 6%、每季回購金額與均價、毛利率季變化","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#5","geo_supply_chain#6","geo_supply_chain#7","substitute_technology#3","reg_tariff_export#0"],"fact_refs":["f_kpi1_non_gaap_gross_margin","f_kpi5_free_cash_flow"]},{"view":"價格已反映太多","evidence":"trailing P/S 10.72 倍、前瞻 EV/S 7.36 倍，對一家硬碟廠來說，等於把高點利潤率當常態。假設營益率回到 35%，FY2027 EPS 約 26，本益比約 25 倍。","assumption":"前瞻 16 倍、FY2028 約 10 倍代表便宜","consequence":"就算 FY2028 照共識兌現，市場也會提前為 FY2029 的下行定價，倍數再壓縮，股價橫盤或下跌","ruling":"部分採納：這正是估值給中性而不是便宜、並把分母列為爭點的原因。但股價已由 914.72 跌到 644.58，Base 情境已經不需要倍數擴張，價格反映過頭的程度比前份輕。","watch":"股價÷FY2028E 共識、每季共識修正方向","evidence_refs":[],"fact_refs":["f_ps_current","f_ev_s_fwd","f_fwd_pe_latest","f_price_at_dd"]},{"view":"論點失敗","evidence":"組裝集中在泰國，2011 年洪水曾讓全球近半產能停擺；稀土精煉約九成在中國。2023 年因出貨華為被 BIS 罰 3 億美元，另附五年暫緩執行的拒絕出口令，10-K 仍列出每季付款。","assumption":"多據點生產可以吸收單點中斷","consequence":"STX 自身出貨受阻、成本跳升，或被禁止出貨給特定客戶","ruling":"反駁它是論點殺手，但保留為風險：單點中斷通常讓全產業一起漲價（2011 年硬碟價格約翻倍），而 STX 在六國有製造據點；出口管制罰款已和解並按期付款，事實表未見新的調查。","watch":"BIS 和解付款與稽核進度、關稅清單是否納入硬碟、毛利率季變化","evidence_refs":["geo_supply_chain#3","geo_supply_chain#6","geo_supply_chain#8","regulatory_antitrust#1","regulatory_antitrust#2","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#5"],"fact_refs":["f_kpi1_non_gaap_gross_margin"]}],"max_dd":{"lo":-68,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 914.72 → 本次 644.58（-29.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=914.72","side_b":"本次 price_at_dd=644.58","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 914.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 914.72 美元：Bull 價 1,620、Bear 價 300，五年期望值 −5.8%，基準年化 −4.8%，不對稱比 1.1","side_b":"本次情境、股價仍用 914.72 美元：Bull 價 2,070、Bear 價 336，五年期望值 +8.0%，基準年化 2.1%，不對稱比 1.14","ruling":"先換情境、股價不動：五年期望值多 13.8 個百分點，基準年化多 6.9 個百分點。不對稱比由 1.1 變為 1.14。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 914.72 美元：五年期望值 +8.0%，基準年化 2.1%，不對稱比 1.14","side_b":"本次情境、股價 644.58 美元：五年期望值 +53.3%，基準年化 9.5%，不對稱比 2.64","ruling":"再換股價、情境不動：起點價下跌 29.5%，五年期望值多 45.3 個百分點，基準年化多 7.4 個百分點，不對稱比由 1.14 升到 2.64。合計五年期望值比前份多 59.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與觀望理由","cause":"價格變動","prior_field":["val","signal","max_dd_pct"],"side_a":"前份（2026-09-23，股價 914.72）：估值結論 🔴、總評 B、觀望、追蹤；最大回撤 −75%","side_b":"本次（股價 644.58，−29.5%）：FY2027E 共識由 35.78 升到 40.35，前瞻本益比由約 25.6 倍降到 15.97 倍，估值結論轉為 🟡；總評維持 B；觀望的理由由估值偏貴改為 CY2028 定價未定；最大回撤 −45%～−68%","ruling":"估值結論改變，主因是價格下跌，其次是共識上修。裁決與角色由程式依本次輸入重算，預期仍是不建倉。回撤百分比下修是因為基期改變：本次谷底價約 206–355 美元，與前份 −75% 推出的約 229 美元落在同一區，對下行深度的判斷沒有變。","evidence_level":"高：股價與共識都是事實表數字","settle_metric":"股價÷FY2027E 共識 EPS","if_then":["若股價回到 FY2027E 的 18 倍（約 726 美元）以上，而 CY2028 定價仍未揭露 → 不追","若股價跌破 52 週均線 606 美元，而每 EB 營收仍季增 → 不動作，等待事件"],"evidence_refs":[]},{"axis":"情境機率","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份 Bull 30%、Bear 30%","side_b":"本次 Bull 20%、Base 45%、Bear 35%","ruling":"Bull 路徑因共識上修（FY1 三個月 +12.1%）與部分長約延到 CY2030 而墊高，但機率下修：2026-10-27 法說首次出現同業資本支出升向營收約 8%、第三家日本擴產的具體說法，而 STX 自身 EB 只增約 25%，Bull 所需的漲價延續到 2030 年變得更難。Bear 上調 5 點，反映同一批證據，加上本季 EB 季增近零、庫存天數 83→97、每 TB 降本放緩。Bear 不高於 Base，因為 FY2027 與 FY2028 上半年的價格已經鎖定。","evidence_level":"中：擴產說法出自分析師提問，公司未否認","settle_metric":"CY2028 定價方向與 12 月季 EB","if_then":["若 12 月季 EB ≥240 且 CY2028 定價不低於 CY2027 → Bull 機率回到 25%，Bear 回到 30%","若 CY2028 定價下調 → Bear 機率調到 45%"],"evidence_refs":["supply_demand_durability#3","cyclical_prior_downcycle_behavior#4","cyclical_supply_discipline_capacity#1"]},{"axis":"維持不變的基本面欄位","cause":"新證據","prior_field":["cycle_position","moat_trend","archetype","trap","runway_post_y5"],"side_a":"前份：晚循環、護城河趨勢 →、循環/商品、陷阱風險 🟡、五年後跑道 🟡","side_b":"本次全部同值","ruling":"新一季的證據沒有推翻任何一欄。毛利率再創新高，但擴張改為靠漲價，對手擴產也具體化，維持晚循環與循環/商品。HAMR 領先擴大，與 STX 讓量相抵，護城河趨勢維持 →。衰退信號仍只亮一個，陷阱風險 🟡。沒有已證實的第二成長曲線，跑道 🟡。","evidence_level":"中","settle_metric":"每 EB 營收季變化、總 EB 年增率","if_then":["若每 EB 營收連 2 季季減，而 EB 年增沒有回升 → 陷阱風險升為 🔴，不建倉","若 CY2028 定價續升，且 EB 年增回到 25% 以上 → 循環位置改判中循環，並重看護城河趨勢"],"evidence_refs":["cyclical_prior_downcycle_behavior#0","substitute_technology#4"]},{"axis":"重跑研究條件（不建倉與首倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價回到 $572–644（FY2027E 共識 35.78 的 16–18 倍）即重跑研究；此價位之前不建倉","side_b":"CY2028 長約定價定案不低於 CY2027，且 12 月季總出貨 EB ≥240，兩者都成立才重跑研究；在此之前不建倉，股價先漲也不追","ruling":"前份條件已觸發：收盤 644.58 落在區間上緣（只高 0.58 美元），以最新共識計為 15.97 倍，已低於 16 倍下緣，本次研究就是這次重跑。重跑的結論是估值不再是約束，唯一卡住建倉的是 CY2028 定價能否守住，所以條件由價格錨改為事件錨。事件成立之前不建倉；成立後重跑研究，通過才建首倉。","evidence_level":"高","settle_metric":"CY2028 build-to-order 定價方向","if_then":["事件成立 → 重跑研究，通過後首倉 ≤3%，分兩批建立","事件未到、股價先漲 → 不追"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份沒有設減碼或清倉門檻（null）","side_b":"每 EB 營收連 2 季季減，或年增跌破 10%；非 GAAP 毛利率連 2 季季減，或跌破 55%；總 EB 年增連 2 季低於 15%；庫存天數連 2 季高於 100 天且 EB 未回升；CY2028 定價低於 CY2027","ruling":"前份沒有留門檻，本次補上。持有時，任一條觸發就先減碼一半；每 EB 營收與毛利率同時連 2 季季減，或 CY2028 定價下調，清倉。","evidence_level":"中","settle_metric":"每季財報","if_then":["任一條觸發 → 減碼一半","價格與毛利兩項指標同時觸發 → 清倉"],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份沒有設唯一致命點（null）","side_b":"Single Thing：CY2028 build-to-order 定價定案低於 CY2027，或管理層改為不按年鎖價","ruling":"前份沒有設，本次依最大單一敏感度選定這一項。毛利擴張此刻主要靠漲價，FY2028 下半年與 FY2029 全年都落在尚未定價的期間。以 12 月季指引計，單價降 10% 約少 4.8 億美元營收，幾乎全部從營業利益扣掉，約為單季營業利益的兩成。","evidence_level":"中","settle_metric":"CY2028 定價揭露","if_then":["定價下調 → Bear 機率調到 45%，不建倉；已持有則清倉","定價不低於 CY2027 → 進入重跑研究"],"evidence_refs":[]},{"axis":"供需缺口是結構性還是週期性","cause":"新證據","prior_field":null,"side_a":"結構論：大部分 nearline EB 已用長約配置到 CY2028，部分雲端客戶延到 CY2030；build-to-order 鎖定了 CY2027 的規格與價格。CFO 說供需缺口可能還在擴大，CEO 說沒有換貨或延後拉貨。Morgan Stanley 估缺口延續到 2028 年。","side_b":"週期論：FY2023 營收年減 37%，毛利率掉到 17%～21%，全年虧損，而砍單的正是現在簽長約的超大規模客戶。Coughlin 認為漲價可能是暫時的。WDC 2027 年量產 HAMR，同業資本支出升向營收約 8%，Toshiba 日本擴產，TDK 擴充磁頭。本季 EB 季增近零，庫存天數 83→97，每 TB 降本放緩。","ruling":"不可調和（方向相反）。裁定採週期論，但週期拉長了：長約保證的是量的配置，價格只鎖到 CY2027，而對手的新產能剛好在 2027–2028 年到位。硬數據是 CY2028 定價尚未定案（CEO 本季原話：未來幾季才開始定案）。因此 FY2027 到 FY2028 上半年的獲利可信，FY2029 以後當作循環變數處理，終端倍數不給結構股的溢價（Base 13 倍，低於現值 16 倍）。","evidence_level":"中：長約與擴產說法都出自公司法說，缺口與暫時性的判斷是第三方轉述","settle_metric":"CY2028 build-to-order 定價相對 CY2027 的方向","if_then":["若 CY2028 定價不低於 CY2027，且 12 月季總 EB ≥240 → 重跑研究，通過後首倉 ≤3%，分兩批建立","若 CY2028 定價下調，或出現換貨、延後拉貨 → 不建倉，Bear 機率調到 45%","反向條件：事件未到，股價跌到 450 美元以下，而每 EB 營收與毛利率仍季增 → 提前重跑研究"],"evidence_refs":["supply_demand_durability#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#4","end_markets#5","channel_business_model_shift#3"]},{"axis":"管理層對降本的說法前後對照","cause":"新證據","prior_field":null,"side_a":"2026-07-28 法說：分析師問每 TB 成本年降約 15% 能否持續，CFO 改談定價策略與產品組合，沒有正面回答","side_b":"2026-10-27 法說：分析師指出最近一季每 TB 成本只降個位數中段。CFO 歸因於外購零件比一年前貴，說自製磁頭與碟片的降本照計畫進行，並表示毛利改善此刻主要來自漲價。","ruling":"可調和（程度差異）。降本放緩採納為事實。外購零件的歸因既不採信也不否定，列為未證並持續監測：若到 2027 年 4 月底的法說，每 TB 成本年降仍低於 10%，而毛利率停止季增，就視為歸因不成立，代表 HAMR 轉換本身的成本壓力被低估了。","evidence_level":"中：降幅數字出自分析師，公司未否認","settle_metric":"每 TB 成本年降幅與毛利率季變化","if_then":["每 TB 成本年降回到 10% 以上 → Bull 機率可回到 25%","連 2 季低於 10%，且毛利率停止季增 → Bear 機率調到 45%"],"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2"]},{"axis":"庫存上升與不超建的說法","cause":"新證據","prior_field":null,"side_a":"CEO 2026-10-27：關鍵是不要超建，照需求生產，不讓產品堆在任何地方","side_b":"本季庫存天數由約 83 天升到 97 天（分析師引述），同一季 EB 季增近零","ruling":"可調和（程度差異）。管理層的解釋是替 Mozaic 4 新一輪認證備貨，12 月季 EB 會明顯跳升；這與 2026-07-28 法說說的刻意放慢 Mozaic 4 放量、配合認證週期一致，暫時採信。","evidence_level":"中","settle_metric":"12 月季總 EB 與庫存天數","if_then":["若 12 月季 EB ≥240，且庫存天數回到 90 天以下 → 備貨說法成立","若庫存天數超過 100，且 EB 低於 235 → 視為超建或轉換卡關，重跑研究延後一季"],"evidence_refs":["cyclical_inventory_price_position#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方論點：FY2028 共識本益比 9.9 倍、FY2029 約 7.4 倍；FY2027 價格已鎖，年底轉為淨現金，75% 自由現金流回饋股東；股價已從 914.72 跌 29.5%，RSI 37.4；機率加權的 5 年報酬仍為正，上下檔不對稱偏向上。","side_b":"等待論點：便宜的前提是分母可信，而分母的後半段正是還沒定價的 CY2028；目前處於晚循環，對手擴產已具體化，回撤路徑在 −45%～−68%。","ruling":"不採買方論點。2 到 3 季內就能拿到 CY2028 定價的答案。等待的成本是可能錯過一段漲幅，換來的是不必在價格未證實時承擔深度回撤；事件成立時，就算股價高出一成，FY2029 獲利可信度提高也足以補回。","evidence_level":"中","settle_metric":"CY2028 定價揭露","if_then":["事件成立 → 重跑研究，首倉 ≤3%","事件未到，股價跌到 450 美元以下而基本面沒有受損 → 提前重跑研究"],"evidence_refs":[]},{"axis":"HAMR 占比目標的說法","cause":"新證據","prior_field":null,"side_a":"2026-07-28 法說：分析師問 2027 年 6 月 HAMR 占 nearline EB 70% 的目標，CFO 只確認 40% 的里程碑與進度正常，沒有重申 70%","side_b":"2026-10-27 法說：CFO 說 CY2026 底與 FY2027 的 HAMR 占比目標不變，但仍沒給 FY2027 的數字；CEO 說 Mozaic 5 進度比上季樂觀","ruling":"可調和。CY2026 底約 50% 的目標兩次說法一致；FY2027 的目標兩次都沒講數字，列為未證。不影響本次結論，但若到 2027 年 7 月底仍不揭露，視為目標下修。","evidence_level":"低","settle_metric":"FY2027 年底 HAMR 占 nearline EB 的比例","if_then":["若 FY2027 年底 HAMR 占比低於 60% → H2 削弱","若揭露 ≥70% → H2 確認"],"evidence_refs":["substitute_technology#5"]}],"triggers":[{"n":1,"text":"12 月季財報驗證定價與獲利","type":"假設驗證","maps_to":"H1","metric":"FQ2 FY27 營收、非 GAAP EPS、毛利率","threshold":"營收 ≥47 億美元、EPS ≥9.0、毛利率高於 57.8%","action":"達標：事件錨維持不變；未達標：Base 的 FY2028 EPS 下修 10%，Bear 機率調到 40%，維持不建倉","source_freq":"每季財報","date":"2027-01-31","evidence_refs":[]},{"n":2,"text":"12 月季 EB 是否如承諾跳升","type":"假設驗證","maps_to":"H2","metric":"總出貨 EB 與庫存天數","threshold":"總 EB ≥240，且庫存天數回到 90 天以下","action":"未達標（EB 低於 235，或庫存天數超過 100）：視為產品轉換卡關，重跑研究延後一季","source_freq":"每季法說","date":"2027-01-31","evidence_refs":[]},{"n":3,"text":"Single Thing：CY2028 長約定價定案","type":"Single Thing","maps_to":"Single Thing","metric":"CY2028 build-to-order 單價相對 CY2027","threshold":"低於 CY2027，或改為不鎖價","action":"觸發：Bear 機率調到 45%，維持不建倉；已持有則清倉","source_freq":"每季法說（預計 2027 年上半年揭露）","date":"2027-07-31","evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"重跑研究條件","type":"估值rearm","maps_to":"H1","metric":"CY2028 定價方向，加上 12 月季 EB","threshold":"CY2028 定價不低於 CY2027，且 12 月季總 EB ≥240","action":"重跑研究；通過後首倉 ≤3%，分兩批建立；事件未到而股價先漲，不追","source_freq":"每季法說","date":null,"evidence_refs":[]},{"n":5,"text":"對手的供給回應","type":"風險","maps_to":"R2","metric":"對手 HAMR 量產時程與資本支出、STX 每 EB 營收年增率","threshold":"對手宣布 HAMR 量產提前到 2027 年上半年，或每 EB 營收年增連 2 季低於 10%","action":"Bear 機率調到 40%，不建倉；已持有則減碼一半","source_freq":"同業財報與法說（每季）","date":null,"evidence_refs":["supply_demand_durability#3","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","substitute_technology#4"]},{"n":6,"text":"關稅、出口管制與外購零件成本吸收失敗","type":"風險","maps_to":"R5","metric":"非 GAAP 毛利率季變化與管理層的歸因","threshold":"單季季減 ≥200bp，且歸因於關稅、出口管制或外購零件","action":"已持有則減碼一半；未持有則重跑研究延後一季","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#5","geo_supply_chain#3","regulatory_antitrust#2"]},{"n":7,"text":"證券集體訴訟和解的最終核准聽證","type":"風險","maps_to":"R5","metric":"法院是否核准 1.75 億美元和解（公司已認列 1.05 億美元費用）","threshold":"法院駁回，或和解金額上修","action":"核准：結案，不動作；駁回：重估現金流出，重跑研究延後一季","source_freq":"法院公告與季報","date":"2026-11-17","evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":8,"text":"超大規模客戶消化庫存","type":"風險","maps_to":"R4","metric":"管理層對換貨、延後拉貨、長約取消費用的說明；資料中心營收季變化","threshold":"出現換貨或延後拉貨，或資料中心營收季減","action":"Bear 機率調到 45%；已持有則清倉","source_freq":"每季法說","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5"]},{"n":9,"text":"持有後的清倉條件","type":"清倉","maps_to":"H1","metric":"每 EB 營收與非 GAAP 毛利率","threshold":"兩者同時連 2 季季減","action":"清倉","source_freq":"每季財報","date":null,"evidence_refs":[]},{"n":10,"text":"複審","type":"複審日期","maps_to":null,"metric":"12 月季財報公布後重看全部假設","threshold":null,"action":"重看 H1–H3 與三個情境的機率","source_freq":"一次","date":"2027-02-15","evidence_refs":[]}],"kill_metrics":[{"metric":"每 EB 營收（營收÷總出貨 EB）季變化","bear_threshold":"連 2 季季減，或年增率跌破 10%","window":"每季財報，下次在 2027 年 1 月底","source":"公司財報新聞稿營收與法說揭露的 EB","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"連 2 季季減，或單季跌破 55%","window":"每季","source":"公司財報新聞稿","last_status":"ok"},{"metric":"總出貨 EB 年增率","bear_threshold":"連 2 季低於 15%","window":"每季","source":"法說 prepared remarks","last_status":"ok"},{"metric":"庫存天數（期末庫存÷單季銷貨成本×91）","bear_threshold":"連 2 季高於 100 天，且 EB 季增未回升","window":"每季","source":"財報資產負債表與損益表（自算）","last_status":"warning"},{"metric":"CY2028 build-to-order 定價","bear_threshold":"定案單價低於 CY2027，或管理層改口不再鎖價","window":"2027 年上半年各季法說","source":"法說管理層說明","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-11.19, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"≤3%","requires_critic":[],"rearm_trigger":"CY2028 長約定價定案不低於 CY2027，且 12 月季總出貨 EB ≥240，兩者都成立才重跑研究；在此之前不建倉，股價先漲也不追","exec_line":"現在不建倉。事件成立後重跑研究，通過則首倉 ≤3%，分兩批（財報後一批，下一季確認後一批）。CY2028 定價下調則維持不建倉，並把 Bear 機率調到 45%。若事件未到、股價先跌到 450 美元以下，而每 EB 營收與毛利率仍季增，提前重跑研究。"},"reasoning":{"industry":"收錢方式：把大容量硬碟賣給雲端與企業資料中心。FQ1 FY27 資料中心營收 34 億美元，占 81%，出貨 EB 占 90%；Edge IoT 營收 7.84 億美元，占 19%。FY2026 通路結構為 OEM 81%、經銷 13%、零售 6%，最大客戶約占 14%。最新一季數字取自 2026-10-27 法說（事實表 KPI 只到 FQ4 FY26，該季營收 36.29 億、非 GAAP 毛利率 52.7%）：營收 42.3 億美元，年增 61%、季增 17%；非 GAAP 毛利率 57.8%、營益率 50.7%、EPS 7.68，都高於 2026-07-28 指引的上緣（營收 41 億±1 億、EPS 7.30±0.20）；自由現金流約 15 億美元。12 月季指引為營收 48 億±1 億、EPS 9.20±0.20、營益率 50%～55%。錢卡在面密度：STX 自製磁頭與碟片，靠 HAMR 把每碟容量從 3TB 推到 4TB 以上，刻意不增加硬碟台數。長約把大部分 nearline EB 配置到 CY2028，部分延到 CY2030，但價格只鎖到 CY2027。本季每 EB 營收約 1,920 萬美元，季增約 16%、年增約 33%（自算）；CFO 說毛利改善此刻主要來自漲價。產業時鐘判在 III：單價漲幅超過出貨量，毛利率遠高於任何前高，對手與零件商也開始擴產。供需判斷為週期性、將會反轉：缺貨延續到 2028 年左右，之後供給可逆。單點依賴：上游主軸馬達約八成出自單一日廠，稀土精煉約九成在中國，屬集中風險；下游最大客戶約 14%，未達集中警戒，但 2023 年正是同一批客戶大砍採購。產業態勢是雙向拉鋸：結構轉好的一邊有長約、鎖價、不增台數；另一邊是競爭與替代，包括 WDC 2027 年量產 HAMR、同業資本支出升向營收 8%、Toshiba 日本擴產、QLC SSD。其他結構變數是關稅與出口管制。","moat":"機制：三家寡占（2025 年 EB 份額 WDC 約 47%、STX 約 42%、Toshiba 約 11%），加上自製磁頭與碟片和 HAMR 領先。CEO 說 HAMR 技術無法靠收購取得。Mozaic 3 已在所有主要雲端客戶通過認證；Mozaic 4（最高 44TB）正在兩家 CSP 放量，未來兩個月還有多家完成認證；Mozaic 5 預計 CY2027 底送樣，管理層說進度比上一季樂觀。WDC 的 HAMR 要到 2027 年才量產，時間差約一到兩年。方向證據分兩面。執行面在擴大。定價面持平：漲價由供需缺口推動（CFO 2026-07-28 原話：不是策略改變），外購零件漲價要隔一段時間才轉嫁；STX EB 年增目標約 25%，低於 Morgan Stanley 估的產業供給 30%～35%，等於主動讓量換價。兩面相抵，判為穩定。評分：執行 8、定價 6；QLC SSD 列為生態攻擊扣 1 分，綜合落在 C。同業表只有快閃記憶體與 DRAM 廠，沒有 HDD 對手，算不出 ROIC 差距。只看利潤率，STX TTM 營益率 40.5%，低於 MU 74.6%、000660.KS 68.0%、285A.T 55.7%，在儲存利潤池裡不是最強的一環。報酬持續期：當期報酬高，四個檢查點三黃一綠；增量報酬來自價格，不是新投入的資本。","growth":"成長組成：量的部分，總 EB 年增 21%（FQ4 FY26 為 34%）；價的部分，每 EB 營收年增約 33%。近兩季以價為主，回購從 2027 年 3 月季起放大。共識 EPS 由 FY2026A 13.90（GAAP 稀釋，事實表沒有全年非 GAAP 數）到 FY2027E 40.35、FY2028E 65.07、FY2029E 87.28，三年年化約 84.5%，因基期在循環低檔而偏高；FY2027→FY2029 年化約 47%。內生上界約 25%（EB 供給年增、單價持平）。缺口約 22～60 個百分點，主要歸因於漲價帶動的毛利擴張（CFO 本季原話：毛利改善此刻主要來自漲價），其次是淨回購（以 75% 自由現金流回饋股東的模式推估，每年減股約 4%～5%），沒有收購。管理層 FY2027 只給定性指引：營收成長明顯高於 FY2026 的 34%。共識營收 FY2027 為 203 億美元（年增約 66%），FY2028 為 280 億美元。跑道：管理層稱 EB 需求能見度超過 2030 年，長約配置到 CY2028、部分到 CY2030；HDD 在大容量儲存的滲透率事實表未涵蓋，物理 AI 等新需求管理層自承還沒直接看到，不算第二曲線，因此給中等。十類衰退信號只亮一個：EPS 成長遠快於營收（FY2026→FY2028 EPS 年化約 116%，營收約 51%）。價值陷阱風險 🟡，長期成長性 🟡。","governance":"現金轉換：FY2026 自由現金流 31.05 億美元、淨利 31.84 億，轉換率約 0.98；FY2025 只有 0.56（8.18 億÷14.69 億）。FQ1 FY27 營運現金流 17 億、資本支出 2.11 億（占營收 5%），自由現金流約 15 億，創新高。SBC：FQ4 FY26 為 5,400 萬美元，占營收 1.5%、占非 GAAP 營業利益 3.3%，稀釋很輕。現金去向（近一季，四項中有數字的是前三項）：還債方面，9 月季償還 12 億（含可交換票據與約 10 億高收益債），10 月再還 7.5 億，本金降到約 16 億，淨槓桿 0.2 倍，重回投資等級。回饋股東方面，9 月季 5.68 億，約為 6 月季的兩倍；季股息調升約 3% 到 0.76 美元，剩餘回購授權 44 億。資本支出維持營收 4%～6%。併購：無。近三年完整的四項去向事實表未涵蓋。CEO 說模式是把 75% 自由現金流回饋股東，超出部分看機會加碼。疑慮在時點：大規模回購從 2027 年 3 月季開始，正是獲利接近循環高點、FY2028 本益比約 10 倍的位置；如果 2028 年後轉為下行，等於在高價買回。另外，可交換票據交割讓稀釋股數由 231M 升到 233M（12 月季指引），回購要先抵掉這部分。","valuation":"現價 644.58 美元，對 FY2027E 共識 40.35 為 15.97 倍，對 FY2028E 65.07 為 9.9 倍，對 FY2029E 87.28 為 7.4 倍。FY1 共識近三個月上修 12.1%；最近兩份快照之間 FY1 −0.6%、FY2 +0.7%，修正動能趨平。這個價格不要求共識全數兌現，要求的是 FY2028 以後單價不崩。Base 情境（FY2032E EPS 78×13 倍）約 1,014 美元，5 年 +57%；若 FY2029 停在 FY2028 的水準並給 13 倍，約 806 美元；若 CY2028 單價下調、客戶又開始消化庫存，Bear 情境為 336 美元。我信 FY2027 與 FY2028 上半年（價格已鎖），不信 FY2029 的 87.28：那一整年都落在未定價期間，我給 76。報酬來源拆解：Base 報酬幾乎全部來自 EPS 複利（40.35→78，年化約 14%）加約 0.5% 股息；倍數由 16 倍降到 13 倍是負貢獻，所以不屬於估值依賴型。PEG 0.19（15.97 倍÷GAAP 基期三年 EPS 年化 84.5%）因基期在循環低檔而失真，不當作便宜的證據。賣方共識目標價 829–898 美元是 5 月、7 月的舊值，早於這一輪下跌，不當作支持證據。12 個月短期以 FY2028E Base EPS 62×12 倍計，約 744 美元（+15.4%）。同業本益比事實表未涵蓋。","premortem":"最可能看錯的地方，是把缺貨期的價格當成新常態。壓力測試三項：一、CY2028 單價持平，FY2029 EPS 停在 62，給 13 倍約 806 美元，通過；二、單價兩年內回落約兩成，走 Bear 路徑，終端 336 美元，不通過；三、超大規模客戶消化庫存重演 2023（營收年減 37%），不通過。三項只過一項。最大回撤估 −45%～−68%：前一輪下行時營收年減 37%、全年虧損；這一輪股價在獲利續創新高的情況下，五週內由 914.72 跌到 644.58，26 週報酬 −11.2%，RSI 37.4。循環轉向時，第一站是 104 週均線 367 美元（−43%），極端情況是 250 週均線 195 美元一帶（−70%）。三個反證視角寫在反證紀錄，這裡不重複。陷阱風險 🟡：衰退信號只亮了 EPS 成長遠快於營收這一個，但這一個正是本輪獲利的主要來源。"},"plain":{"six":{"how_it_makes_money":"賺的是雲端資料中心擴充大容量儲存的錢，錢卡在磁頭與碟片的面密度這個節點；這一季多賺的部分主要來自缺貨下的漲價，不是降本。","moat":"護城河趨勢穩定（→）：HAMR 技術領先在擴大，但定價力來自供需缺口而不是客戶鎖定，STX 也主動讓出量的份額；等級 C。","growth":"五年後跑道中等（🟡）：資料留存需求仍在成長，但 HDD 是成熟品類，沒有已證實的第二條成長曲線；共識成長遠超過量能撐得起的上界，差額要靠漲價與回購補。","capital":"資本配置由還債轉向回購，紀律好，但時點有疑慮：債務目標已達成，年底預計轉為淨現金；回購從 2027 年起放大，卻剛好落在循環高檔。","valuation":"估值中性：現價要求 FY2028 前後單價守住、FY2029 以後只溫和回落。前瞻 16 倍、FY2028 約 10 倍看起來便宜，但分母是循環高點附近的獲利，我只信到 FY2028 上半年。","how_wrong":"最可能看錯的地方，是把缺貨期的價格當成新常態；陷阱風險中等（🟡）。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等 CY2028 build-to-order 定價定案（管理層稱在未來幾季內，預計 2027 年上半年法說揭露）且不低於 CY2027，並確認 12 月季總出貨 EB ≥240；事件未到而股價先漲，也不追","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":644.58,"week26_return_pct":-11.19,"consensus_rev_3m_pct":12.08,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母是循環高點附近的獲利：非 GAAP 毛利率 57.8%，遠高於 FY2023 谷底的約 17%～21%，每 EB 營收年增約三成。FY2028 下半年與 FY2029 全年都落在尚未定價的期間，所以 FY2028 約 10 倍、FY2029 約 7 倍不能當作便宜的證據。"},"catalysts":[{"date":"2026-11-17","date_precision":null,"type":"other","event":"證券集體訴訟 1.75 億美元和解的最終核准聽證","impact":"低","watch":"法院是否核准"},{"date":"2027-01","date_precision":"month","type":"product","event":"Mozaic 4 在多家全球 CSP 與 OEM 客戶完成認證（管理層稱在未來兩個月內）","impact":"中","watch":"完成認證的家數與 12 月季 EB"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"FQ2 FY27 財報與 3 月季指引","impact":"高","watch":"EB 是否跳升、毛利率、庫存天數、CY2028 定價進度"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"回購明顯放大（從 3 月季開始）","impact":"中","watch":"回購金額與均價"},{"date":"2027-06","date_precision":"quarter","type":"guidance","event":"CY2028 build-to-order 規格與定價定案（管理層稱在未來幾季內）","impact":"高","watch":"單價相對 CY2027 的方向"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"WDC 預計 2027 年內完成 HAMR 客戶認證並量產","impact":"高","watch":"量產時程與首批容量"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"Mozaic 5（單碟 5TB 以上）開始送客戶驗證","impact":"中","watch":"是否如期或提前"}],"_projected_from":"v19"}
```
