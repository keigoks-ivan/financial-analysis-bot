你是 stock-analyst v20 的**散文層（prose）agent**，標的 ARW（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARW_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ARW　日期：2026-11-08　archetype：None　前份裁決：2026-05-23　B（衛星觀望·thesis 完整 AI 半導體 duopoly + ECS 結構成長，但 cycle peak 估值已透支、Pure MA 🟡 + BB 上軌突破，等回測 4W 均 $201 以下或 BB 中軌 $156 分批進場）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1799B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（405B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（805B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1367B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（814B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（453B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（801B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2252B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3233B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2675B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1799           3641-5201      5 條（2–6 內）  
s3                  8000         405           5316-7595      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2986          8410-12014      5 條（2–6 內）  
s6                 11000         453          7383-10547      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         801           1889-2699      5 條（2–6 內）  
s10                 5000        2252           1924-2748      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2675           2000-2325      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4105B；至少需散文≈40.90KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−35%
−35
−20%
−16.7%
−8%
−7.11
−7%
−4.68
−4.41
−1.28%
0
0.0%
0.11%
0.21
0.24
0.39
0.5%
0.69
0.75
01
1
1.0
1.11
1.4%
1.5%
1.75
1.9
2
02
2%
2.11
2.5
2.6
2.71%
2.8%
2.9%
3.0%
3
3%
3.11%
3.26%
3.6%
3.8
3.92
4.0%
4.0
4%
4
4.02%
4.03%
4.1%
4.15%
4.3%
4.6
4.7%
4.83
4.9
5.0%
5%
5
05
5.03
5.1%
5.2%
5.61%
5.77
5.81
6
6%
06
6.22
6.4
7
7.00
7.03%
7.20
7.29
7.5
7.57
7.8
7.9%
8
8%
8.0
08
8.1%
8.1
8.3
8.37
8.4
8.6
8.82
9
9%
9.5
10
10%
10.2
10.4
10.43%
10.5%
10.8%
10.82%
10.93
11
11.2%
11.24%
11.43%
11.5
11.7%
11.9%
12
12.1%
13
13.03%
14
14%
14.49%
15%
15
15.1%
15.11
15.66%
16.7%
17%
17
17.4
17.5
18%
19%
19
19.1
20
20%
21
21.0%
21.0
21.30
21.5%
21.64
21.80
22
23%
23.7%
23.93
24%
24
24.5
25%
26
26.0%
26.5
27.2
27.20
27.4
28
28.4
29
29%
30%
30
30.73
32.94
33
33.5
34%
34
35
35%
35.5%
36
37
39.5
40%
42
43
43%
44%
44.5
45%
45
45.5
46%
47
48%
48
49%
49
50
50%
50.56
50.82
51.6
52
54%
54
56%
59
62.3%
67%
69%
70
73
73.9%
79
81.5
85.5
90
91.55
92
100
100%
110
117
120
130
132
150
150%
$156
176.54
181.09
190
199
$201
201
212
215
217.33
250
265%
334
400
407
441
460
550
2025
2026
2027
2028
2029
2036
20261108
1,160
1,600
10,717.7
2,690
4,300
4,640
9,300
9,900
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
{"meta":{"ticker":"ARW","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Arrow Electronics"},"oneliner":"第三季創紀錄，但成長多靠漲價，8.4倍本益比的分母接近上輪高點21.80美元；五年基本情境年化約5%，現價不追，等150美元以下再重跑研究。","thesis":{"H":[{"id":"H1","text":"本輪元件上行至少走到2027年底，第三季以漲價為主的成長，從第四季起改由出貨量接手，Components營益率守住5%。","2y":"FY2027 EPS不低於24美元；Components全年營益率不低於5.0%。","5y":null,"10y":null,"threshold":"第四季Components營收不低於81.5億美元且營益率不低於5.0%；FY2027 EPS不低於共識23.93美元。","source":"公司季度新聞稿與法說；共識來自Koyfin快照。","drift_rule":"TTM EPS較路徑偏離連兩季達5%為削弱，連三季達10%為反轉。"},{"id":"H2","text":"加值服務與ECS能墊高下一輪谷底，週期中段營益率不低於FY2022至FY2025的平均4.15%，谷底年EPS不再跌回7.29美元。","2y":null,"5y":"FY2027至FY2031平均營益率不低於4.0%；谷底年EPS不低於12美元；股數降到45.5百萬股以下。","10y":null,"threshold":"谷底年營益率不低於3.0%，EPS不低於12美元；ECS帳單金額年增不低於10%。","source":"10-K分部資料、季度帳單金額、CFO對加值服務占營業利益比重的揭露。","drift_rule":"平均營益率較門檻偏離連四季達5%為削弱，連六季達10%為反轉。"},{"id":"H3","text":"通路角色十年內不被繞過：多數中小客戶要的交期和數量，原廠直接供應並不划算，Arrow維持規模與產品線優勢。","2y":null,"5y":null,"10y":"2036年前毛利率不跌破10.5%，投入資本報酬率十年平均不低於10%。","threshold":"TTM毛利率不低於10.5%；沒有主要原廠大規模收回經銷授權。","source":"10-K供應商集中度與競爭章節、原廠通路調整報導。","drift_rule":"跨兩個年度低於門檻為削弱，跨三個年度為反轉。"}],"R":[{"id":"R1","text":"週期提前反轉，補庫存回吐；上一輪營收連兩年下滑，營益率由5.61%跌到3.26%。","h_ref":"H1","clock":"⚡","threshold":"Components營益率連兩季低於4.7%，或訂單出貨比跌破1。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R2","text":"營運資金吃掉現金：第三季營運現金流−4.41億美元，存貨季增14億美元，其中約6億美元是待出貨的AIS訂單。","h_ref":"H1","clock":"⚡","threshold":"存貨增速連兩季快過Components營收增速，或營運現金流連兩季為負。","evidence_refs":["supply_demand_durability#3"]},{"id":"R3","text":"加值服務占比被稀釋：2025年約占營業利益30%，今年下降；ECS成長靠硬體毛額認列，AIS毛利率未揭露。","h_ref":"H2","clock":"🔥","threshold":"ECS帳單金額連兩季年增低於10%，或帳單基礎毛利率年減。"},{"id":"R4","text":"接班與資本配置風險：仍為代理CEO，ECS總裁年底退休，證券化額度已加入重大併購時提高槓桿上限的條款。","h_ref":"H2","clock":"🔥","threshold":"併購超過約4.6億美元，或調整後槓桿超過2.5倍。","evidence_refs":["major_events#0"]},{"id":"R5","text":"關稅與出口管制吸收失敗：2025年10月三家中國子公司曾被列入實體清單，IEEPA關稅訴訟結果也有不確定性。","h_ref":"H1","clock":"🔥","threshold":"Components營益率季減不少於50個基點，且管理層歸因於關稅或出口管制。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","regulatory_antitrust#1","geo_supply_chain#0"]},{"id":"R6","text":"通路被繞過：原廠直銷、電商與物流業者切入中小客戶。","h_ref":"H3","clock":"🐢","threshold":"TTM毛利率跌破10.5%，或累積證據顯示被繞過的機率達50%以上。","evidence_refs":["channel_business_model_shift#1","competitive_share_entrants#0","substitute_technology#0"]}],"single_thing":{"description":"Global Components訂單出貨比跌破1，同時積壓訂單首次季減。","why_fatal":"Components營益率每降100個基點，以年化營收約334億美元、稅率24%、51.6百萬股計算，EPS約少4.9美元，是基本路徑FY2027 EPS 26美元的19%；上一輪EPS兩年內跌67%。","if_happens":"取消進場條件；若持有則清倉；空頭機率由35%上調到50%以上。","how_monitor":"每季法說的訂單出貨比描述、積壓訂單延伸月份與交期變化；公司未揭露具體數字，只能看文字變化，這是資料缺口。","probability":"12至24個月內約45%；積壓訂單只看到2027年中，基本情境假設週期在2028年見頂。"}},"appendix_a":{"growth_durability":4,"quality_score":5,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":7.57,"peg_fy2":0.21,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":10.93,"FY2026E":21.64,"FY2027E":23.93,"FY2028E":27.2},"fy_end_month":12,"eps_basis":"FY2025A為GAAP稀釋EPS（事實表年度財務史）；FY2026E起為Koyfin共識，FY1對應FY2026。基期與預估口徑不一致且基期接近谷底，三年CAGR 35.5%偏高。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARW_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"年度財報FY2022至FY2024，EPS由21.80美元跌到7.29美元，營收連兩年下滑10.82%與15.66%，但沒有虧損年；屬需求量循環，不是商品價格接受者。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉。目前處於擴張期：積壓訂單看到2027年中，交期拉長但低於疫情高峰，中小客戶才剛回來（2026-11-05法說）；記憶體缺貨可能延續到2027（Altium/Octopart引述Samsung、SK Hynix）。但客戶已開始加回緩衝庫存（2026-08-06 Components總裁），上一輪兩年內EPS跌67%。","bargaining":{"up":"單一供應商不超過8%，但原廠掌握配額、授權與直銷選擇權，上游較強。","down":"單一客戶不超過2%，下游分散；大客戶可比價或走直銷。","geo":"美中關稅與出口管制直接影響亞太業務，2025年10月曾有三家中國子公司被列入實體清單，同年11月移除。"},"profit_pool_dir":"事實表未涵蓋","tam_table":{"expanded":false,"reason":"事實表沒有TAM、滲透率與利潤池資料，市占只有聚合網站推算的14.49%；本次論點靠週期與週轉，不靠滲透率。"}},"moat":{"mechanism":"產品線廣度、全球物流與信用額度形成規模優勢，服務原廠不願直接服務的大量中小客戶。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：費用占毛利比降到62.3%，領先AVT。定價力縮減：毛利率連四年下滑，缺貨期間也沒有回升。ECS新增HPE Juniper與IBM七國代理，但2026年8月結束一項約7億美元的供應商關係。兩邊相抵判持平。","peer_na_reason":"事實表只有同業利潤率，沒有同業ROIC，無法計算報酬率差距。","threats":[{"level":"🟡","text":"原廠調整通路：10-K明言公司也與供應商搶客戶；TI增加直銷，TE把部分車用銷售轉入經銷，ADI亞太整合有利Arrow，方向混合。","p":"25%","evidence_refs":["substitute_technology#0","channel_business_model_shift#1","channel_business_model_shift#2"]},{"level":"🟡","text":"供應商整併可能把Arrow排除在外；2026年8月CEO證實一項約7億美元的供應商關係結束，ECS主管稱對營收與獲利無影響，未證。","p":"15%","evidence_refs":["geo_supply_chain#1"]},{"level":"🟡","text":"物流、電子目錄與電商業者切入中小客戶，正是Arrow毛利較好的客群。","p":"30%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"數位平台與AI工具若跟不上，客戶留存會受影響；目前只見風險因子描述，沒有流失數據。","p":"20%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者與付款者清楚，多數客戶需要通路提供的交期與數量。但客戶已在加回緩衝庫存，部分需求是補庫存，不是實際消耗。"},{"item":"決策層級","level":"🟡","text":"同一料號可在不同通路比價，替代性高；設計導入與供應鏈服務的轉換成本較高。漲價後流失率與續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"原廠拿走多數利潤，通路毛利約一成一；毛利率連四年下滑，這輪缺貨也沒改善，但約56%存貨受供應商條款保護，風險分攤仍有利通路。"},{"item":"社會容忍度","level":"🟢","text":"通路加價不是社會議題，也不依賴監管授權；實際限制來自關稅與出口管制。"}],"roiic":15,"reinvest_rate":54,"endo_ceiling":8.1,"formula_note":"單位為百分比。增量資本報酬：週期中段營益率約3.6%至4%，稅率24%，營運資金占營收18%，約15%至17%，取15%。再投資率：FY2022至FY2025累計FCF 15.11億美元除以淨利32.94億美元得46%，1減46%為54%，因事實表缺折舊與併購淨額，以此代替標準公式。內生上限：15%×54%＝8.1%。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","ARW":11.43,"AVT":10.43,"SNX":6.89,"CDW":21.0,"WCC":21.5,"unit":"%"},{"metric":"營業利益率","ARW":4.02,"AVT":3.11,"SNX":2.71,"CDW":7.03,"WCC":5.57,"unit":"%"},{"metric":"FCF 利潤率","ARW":4.03,"AVT":-1.28,"SNX":-1.08,"CDW":3.81,"WCC":1.6,"unit":"%"}],"competitors":[{"name":"AVT","gm":10.43,"om":3.11,"fcf_margin":-1.28,"strategy_note":"最直接的元件對手，三項利潤率都低於ARW，FCF利潤率為−1.28%；期間較早，差距有部分來自時點。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SNX","gm":6.89,"om":2.71,"fcf_margin":-1.08,"strategy_note":"以IT通路為主，營益率2.71%，適合對照ECS，不是元件對手。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"CDW","gm":21.0,"om":7.03,"fcf_margin":3.81,"strategy_note":"直接面對企業客戶的加值經銷，毛利率21.0%、營益率7.03%，說明越靠近終端客戶定價力越好。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"WCC","gm":21.5,"om":5.57,"fcf_margin":1.6,"strategy_note":"電氣與通訊通路，毛利率21.5%，商業模式不同，只作通路毛利上限的參考。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"第三季價為主，第四季財測量為主；無併購；回購小幅。","runway_post_y5":"🟡","endo_ceiling_basis":"增量資本報酬15%×再投資率54%＝8.1%，推導見護城河段。","segments":[{"item":"Global Components","value":"第三季營收約79億美元，年增43%，季增8%；營益率5.2%，季減20個基點；第四季財測81.5至85.5億美元。"},{"item":"Global ECS","value":"第三季營收約28億美元，年增29%；帳單金額59億美元，年增14%；營益率3.6%；第四季財測34至36億美元，營益率低於歷年第四季的6%以上。"}],"decay_signals":[{"name":"毛利率連兩季年減","lit":false,"note":"第三季持平，但年度毛利率連四年下滑。"},{"name":"核心市占縮減","lit":false,"note":"沒有可靠的一手數據。"},{"name":"提價後銷量下滑","lit":false,"note":"管理層稱未見需求被破壞。"},{"name":"EPS成長遠高於營收成長","lit":true,"note":"FY2025到FY2027 EPS年化約48%，營收約23%，差距來自週期回升。"},{"name":"FCF對淨利連兩年低於0.75","lit":false,"note":"FY2025為負，FY2024為2.6倍；2026年待全年數字。"},{"name":"SBC占營收超過5%且上升","lit":false,"note":"第三季約0.11%。"},{"name":"TAM萎縮或被替代","lit":false,"note":"未見證據。"},{"name":"產業倍數系統性下移","lit":false,"note":"事實表未涵蓋。"},{"name":"維護性資本支出占FCF過高","lit":false,"note":"第三季資本支出僅2,690萬美元。"},{"name":"停止投資且收入下滑","lit":false,"note":"不適用。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，回購金額只有第二、三季的資料，現金去向四分事實表未涵蓋，無法可靠展開。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近12個月沒有重大併購，過往併購的實際報酬事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價與10年期公債殖利率事實表未涵蓋，無法判定。現價前瞻盈餘殖利率11.9%，但分母有爭議。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"第三季SBC 1,160萬美元，年化4,640萬美元，約占市值91.55億美元的0.5%，低於1.5%。","grade":"過"}]},"valuation":{"basis":"以FY2026E共識EPS的前瞻本益比為起點，再用目前股數調整的五年平均盈餘校正。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比；本次錨定公司自身的盈餘週期，同業倍數不承重，但也因此少一項對照。"},"fwd_pe":8.37,"peg":0.24,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"不便宜也不貴。FY2026E本益比8.37倍，但分母接近上輪高點；用調整後平均EPS約17.4美元計算約10.4倍，略高於前份記錄的五年中位約10倍。五年分位無法計算，事實表只有四個年度端點（Trailing本益比分位39.5）。基本情境五年年化約5%，低於8%。","upside_short_pct":17,"upside_mid_pct":10},"trap_analysis":{"verdict":"🟡","label":"低本益比可能是週期高點的假便宜"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY2022到FY2024，EPS由21.80美元跌到7.29美元，營收連兩年下滑。本輪積壓訂單到2027年中，客戶已在加回緩衝庫存，Arrow存貨73億美元，較2025年底50.82億美元增加44%。","assumption":"目前訂單反映真實消耗，不含重複下單。","consequence":"五年後虧五成最可能的故事：2028年訂單回吐，存貨跌價與去化同時發生，EPS回到8至9美元，股價約90至110美元。","ruling":"採納，列為機率35%的空頭情境；約56%存貨受供應商條款保護，降低減損幅度，但擋不住營收與費用槓桿反轉。與唯一致命點是同一件事，不另立。","watch":"訂單出貨比、積壓訂單延伸月份、存貨增速對營收增速。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","supply_demand_durability#3","substitute_technology#2"],"fact_refs":["f_kpi3_441_4_26_9","f_kpi6_backlog_book_to_bill"]},{"view":"論點成功但股東經濟變差","evidence":"第三季Components邊際營益率2.8%；ECS營收年增29%但帳單只增14%；應收與應付天數年增約100天；約6億美元存貨放在AIS資料中心業務，毛利率未揭露。","assumption":"成長能以目前的資本效率轉成現金。","consequence":"營收和訂單都達標，但資金被鎖在存貨與應收，ROIC自15.1%回落，EPS成長換不到自由現金流。","ruling":"部分採納。管理層稱AIS存貨下季出貨，未證，先監測；若到2027年第一季財報存貨仍不低於73億美元，這個說法不成立。","watch":"存貨季增率對Components營收季增率、季度營運現金流、ROIC。","evidence_refs":["supply_demand_durability#3","end_markets#2"],"fact_refs":["f_kpi3_441_4_26_9"]},{"view":"論點成功但股東經濟變差","evidence":"公司仍由代理CEO領導，ECS總裁年底退休；2026年9月應收帳款證券化額度增至17.5億美元，並加入重大併購時臨時提高槓桿上限的條款。","assumption":"新任CEO維持目前的回購與投資等級紀律。","consequence":"週期高點動用資金做大型併購，等於在盈餘最好的時候用高價買資產。","ruling":"未證，列為風險。條款只代表保留彈性，沒有併購計畫的證據。","watch":"CEO正式人選、超過市值5%的併購、調整後槓桿。","evidence_refs":["major_events#0"]},{"view":"價格已反映太多","evidence":"用目前股數調整的平均EPS約17.4美元，現價約10.4倍；反推週期中段EPS要約19美元。","assumption":"股數減少與營收基數提高足以把中段盈餘墊高到19美元以上。","consequence":"基本情境年化只有約5%，多數報酬還要靠本益比由8.37倍回到9.5倍。","ruling":"採納。現價沒有透支，但也沒有給週期風險留下折價，所以不追。","watch":"股價是否到150美元以下，以及FY2027共識更新後的水準。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_shares_diluted_m"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 217.33 → 本次 181.09（-16.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=217.33","side_b":"本次 price_at_dd=181.09","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 217.33 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 217.33 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 217.33 美元：Bull 價 407、Bear 價 120，五年期望值 +5.0%，基準年化 1.4%，不對稱比 1.11","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.11。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 217.33 美元：五年期望值 +5.0%，基準年化 1.4%，不對稱比 1.11","side_b":"本次情境、股價 181.09 美元：五年期望值 +26.0%，基準年化 5.1%，不對稱比 2.11","ruling":"再換股價、情境不動：起點價下跌 16.7%，五年期望值多 21.0 個百分點，基準年化多 3.8 個百分點，不對稱比由 1.11 升到 2.11。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份未計算的欄位，本次首次給值","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位都是空值。","side_b":"本次：護城河持平，五年後成長空間中等，歸類循環股，位於中循環，空頭機率35%，最大回撤區間−35%至−50%。","ruling":"前份沒有計算，無從比較，不視為判斷改變。","evidence_level":"方法差異","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"估值結論未變，但價格與分母都變了","cause":"價格變動","prior_field":["val"],"side_a":"前份估值中性，股價217.33美元，FY2027共識EPS 21.30美元，約10.2倍。","side_b":"本次估值中性，股價181.09美元，FY2027共識EPS 23.93美元，7.57倍。","ruling":"股價跌16.7%且分母上修，數字上更便宜；但分母接近週期高點，便宜論證不成立，結論維持中性。","evidence_level":"高，公司財報與收盤價","settle_metric":"下一份共識快照與第四季財報","if_then":["如果股價跌到150美元以下且訂單出貨比仍高於1，則分批反買，首筆不超過3%"],"evidence_refs":[]},{"axis":"訊號與陷阱判斷未變","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份訊號為B，陷阱風險中等。","side_b":"本次訊號不變，陷阱風險中等；十項衰退訊號亮一項，即EPS成長遠高於營收成長。","ruling":"第三季基本面強於前份預期，但增量主要來自價格與週期，不足以上調。","evidence_level":"中","settle_metric":"第四季Components營益率與營運現金流","if_then":["如果第四季Components營益率不低於5.0%且營運現金流轉正，則維持現有條件，不追"],"evidence_refs":["cyclical_prior_downcycle_behavior#1"]},{"axis":"進場條件由技術位改為回報率價位，前份分批進場條件不沿用","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等回測 4W 均 $201 以下或 BB 中軌 $156 分批進場","side_b":"收盤價不高於150美元（用目前股數調整的五年平均EPS約8.6倍，基本情境年化約9%）才重跑研究","ruling":"前份201美元的條件已經達到，本次仍不進場：那是技術位，基本情境在現價年化只有約5%。新條件直接對應限制本次進場的因素，即盈餘分母接近高點。","evidence_level":"中，情境為判斷值","settle_metric":"收盤價與訂單出貨比","if_then":["如果股價未經驗證續漲超過212美元，則不追","如果股價跌到150美元以下且基本面無損，則分批反買"],"evidence_refs":[]},{"axis":"Single Thing由空值改為訂單出貨比跌破1","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）。","side_b":"Global Components訂單出貨比跌破1，同時積壓訂單首次季減。","ruling":"Components營益率每降100個基點，EPS約少4.9美元，是最大的單一敏感項；訂單出貨比是它最早的離散訊號。","evidence_level":"中，公司未揭露具體數字","settle_metric":"每季法說的訂單出貨比描述與積壓訂單月份","if_then":["如果訂單出貨比跌破1且積壓訂單季減，則取消進場條件，若持有就清倉"],"evidence_refs":["cyclical_prior_downcycle_behavior#1"]},{"axis":"減碼與清倉門檻改寫","cause":"新證據","prior_field":["kill_metrics"],"side_a":"連 2 季觸發即減倉 50%；spot price > -20% QoQ 立即減倉至 0","side_b":"Components營益率連兩季低於4.7%則減碼一半；訂單出貨比跌破1且積壓訂單季減則清倉；DRAM現貨連兩季季減超過10%保留為警示。","ruling":"記憶體只占Components營收低雙位數（2026-08-06 CFO），單靠現貨價清倉過於敏感；改以公司自身的營益率與訂單作為動作依據，現貨價降為警示。","evidence_level":"高，法說原話","settle_metric":"Components非GAAP營益率","if_then":["如果Components營益率連兩季低於4.7%，則減碼一半","如果DRAM現貨連兩季季減超過10%，則停止加碼"],"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"axis":"前份其他門檻的去留","cause":"新證據","prior_field":["H_thresholds","R_thresholds"],"side_a":"第四季毛利率不低於11.7%；ECS每季營業利益2億美元；ArrowSphere活躍客戶數；前瞻本益比持續高於11倍；平均目標價250美元；市占18%跌至12至14%。","side_b":"保留TTM毛利率連兩季不高於11.2%（目前11.43%）與ECS成長監測（改看帳單金額）。其餘退休。","ruling":"第三季非GAAP毛利率10.8%且第四季硬體占比更高，11.7%不切實際；ECS第三季營業利益9,900萬美元，2億美元目標過高；ArrowSphere客戶數與市占沒有可取得的一手資料；市場目前給8.37倍，已低於前份9倍的警戒，但只有單點，本次不再假設重估到11倍以上。","evidence_level":"高，公司財報；客戶數與市占為資料缺口","settle_metric":"TTM毛利率與ECS帳單金額年增","if_then":["如果TTM毛利率連兩季不高於11.2%，則護城河改判下降，若持有就清倉"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"低本益比是便宜還是週期高點","cause":null,"prior_field":null,"side_a":"FY2026E 8.37倍、FY2027E 7.57倍，第四季財測年化EPS 28.4美元，約6.4倍。","side_b":"FY2026E EPS 21.64美元接近FY2022高點21.80美元，當時兩年內跌到7.29美元；用目前股數調整的平均EPS約17.4美元，現價約10.4倍。","ruling":"採後者，便宜論證不成立。雙方都同意盈餘現在很高，差別是能撐多久，屬程度差異；到2027年第二季財報之前無法定案。","evidence_level":"高，年度財報與公司財測","settle_metric":"2027年第二季財報的積壓訂單是否延伸到2028年","if_then":["如果積壓訂單延伸到2028年且Components營益率不低於5%，則把基本情境FY2028 EPS上調到30美元，維持不追","如果積壓訂單開始縮短且Components營益率低於4.7%，則空頭機率上調到50%並停止加碼"],"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"axis":"管理層對漲價貢獻的說法","cause":"新證據","prior_field":null,"side_a":"2026-08-06 CFO：漲價約貢獻Components季增營收的三分之一；2026-11-05準備稿強調出貨量需求有韌性。","side_b":"2026-11-05 CFO問答：「Most of our revenue growth in the components business was driven by price increases in the third quarter」。","ruling":"採後者，第三季成長主要來自價格。第四季財測說會以出貨量為主，尚待驗證。","evidence_level":"高，法說原話","settle_metric":"第四季Components營收與管理層對量價的拆分","if_then":["如果第四季Components營收低於81.5億美元，則空頭機率上調到40%並不追"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"ECS第四季營益率的前後說法","cause":"新證據","prior_field":null,"side_a":"2026-08-06 CFO：預期第四季ECS仍有很高的營益率。","side_b":"2026-11-05 CFO：歷年第四季以淨銷售計高於6%，今年隱含低於此；帳單基礎大致持平。Q3營收財測年增約2%，實際29%。","ruling":"管理層確實改口，但主因是硬體按毛額認列，帳單基礎未見惡化；同時顯示ECS財測的能見度很低。第二季預告的下半年費用，第三季未量化，標未證。","evidence_level":"高，法說原話","settle_metric":"第四季ECS帳單基礎營益率與合約費用金額","if_then":["如果ECS帳單金額連兩季年增低於10%，則第二假設判定削弱並停止加碼"],"evidence_refs":[]},{"axis":"共識修正0.0%與大幅超標互相矛盾","cause":"新證據","prior_field":null,"side_a":"FY1至FY3共識修正皆為0.0%，三個月修正也是0.0%。","side_b":"第三季EPS 6.22美元，高於財測4.83至5.03美元；第四季財測7.00至7.20美元。","ruling":"快照未更新，不能解讀為市場沒有上修。基本情境FY2027 EPS 26美元高於共識23.93美元就是因此。","evidence_level":"高，公司財測對比快照","settle_metric":"下一份共識快照","if_then":["如果FY2027共識上修到26美元以上而股價仍高於150美元，則不追"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"第四季財測年化EPS 28.4美元，約6.4倍；積壓訂單到2027年中；共識看來還沒更新；RSI 30.73，股價略高於52週均線176.54美元；第三季回購9,300萬美元，調整後槓桿1.9倍；12個月上行約17%。","side_b":"五年基本情境年化約5%，空頭情境120美元，跌34%；第三季成長多靠漲價，存貨季增14億美元，營運現金流−4.41億美元；這份利空只有兩個交易日，賣方模型可能還沒反映。","ruling":"不追。短線上行是真的，但賺的是週期還沒到頂的錢，不是長期回報；限制進場的是盈餘分母接近高點。這個判斷若錯，會錯在週期比上一輪長，代價是少賺一段。","evidence_level":"中","settle_metric":"第四季財報的量價拆分、營運現金流與積壓訂單","if_then":["如果股價未經驗證續漲超過212美元，則不追","如果股價跌到150美元以下且訂單出貨比仍高於1，則分批反買，首筆不超過3%","如果訂單出貨比跌破1，則取消進場條件，若持有就清倉"],"evidence_refs":["supply_demand_durability#3"]}],"triggers":[{"n":1,"text":"訂單出貨比跌破1，同時積壓訂單首次季減。","type":"Single Thing","maps_to":"R1","metric":"Global Components訂單出貨比與積壓訂單","threshold":"訂單出貨比低於1.0且積壓訂單季減","action":"未持有則取消進場條件；若持有則清倉","source_freq":"每季法說","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#1"]},{"n":2,"text":"第四季Components要由出貨量接手成長並守住營益率。","type":"假設驗證","maps_to":"H1","metric":"Components營收與非GAAP營益率","threshold":"營收不低於81.5億美元，營益率不低於5.0%","action":"未達標則不追，空頭機率上調到40%","source_freq":"2027年2月財報","date":"2027-02"},{"n":3,"text":"存貨增速連兩季快過Components營收增速；第三季存貨季增23.7%，營收季增7.9%，已亮第一季。","type":"風險","maps_to":"R2","metric":"存貨季增率減Components營收季增率","threshold":"連兩季為正，或2027年第一季財報存貨仍不低於73億美元","action":"未持有則不追；若持有則減碼一半","source_freq":"每季財報","date":"2027-02","evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"股價回到150美元以下才重跑研究。","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"不高於150美元","action":"重跑研究，通過後分批反買，首筆不超過3%","source_freq":"每日","date":null},{"n":5,"text":"Components營益率連兩季低於4.7%。","type":"減碼","maps_to":"R1","metric":"Components非GAAP營益率","threshold":"連兩季低於4.7%，第三季為5.2%","action":"若持有則減碼一半，未持有則取消進場條件","source_freq":"每季財報","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"n":6,"text":"TTM毛利率連兩季不高於11.2%，代表缺貨期間定價力仍在流失。","type":"清倉","maps_to":"R6","metric":"TTM毛利率","threshold":"連兩季不高於11.2%，目前11.43%","action":"護城河改判下降；若持有則清倉","source_freq":"每季財報","date":null,"evidence_refs":["channel_business_model_shift#1","competitive_share_entrants#0"]},{"n":7,"text":"關稅或出口管制吸收失敗，以損益表現為準，不預測政策。","type":"風險","maps_to":"R5","metric":"Components營益率季變動與管理層歸因","threshold":"季減不少於50個基點，且管理層歸因於關稅或出口管制","action":"未持有則不追；若持有則減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","regulatory_antitrust#1","geo_supply_chain#0"]},{"n":8,"text":"週期高點的大型併購或槓桿上升。","type":"風險","maps_to":"R4","metric":"併購金額與調整後槓桿","threshold":"併購超過約4.6億美元（市值5%），或調整後槓桿超過2.5倍","action":"停止加碼，揭露併購條件與資金來源前不進場","source_freq":"8-K與每季財報","date":null,"evidence_refs":["major_events#0"]},{"n":9,"text":"第四季財報後複審全部假設與情境。","type":"複審日期","maps_to":"H1","metric":"全部假設與風險指標","threshold":"到期即複審","action":"更新EPS路徑與機率","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"Global Components訂單出貨比與積壓訂單","bear_threshold":"訂單出貨比低於1.0且積壓訂單季減","window":"任一季","source":"公司法說，文字描述，未揭露具體數字","last_status":"ok"},{"metric":"Components非GAAP營益率","bear_threshold":"連兩季低於4.7%","window":"連兩季","source":"公司新聞稿與法說","last_status":"ok"},{"metric":"TTM毛利率","bear_threshold":"連兩季不高於11.2%","window":"連兩季","source":"季度財報","last_status":"ok"},{"metric":"存貨季增率減Components營收季增率","bear_threshold":"連兩季為正","window":"連兩季","source":"季度財報","last_status":"warning"},{"metric":"季度營運現金流","bear_threshold":"連兩季為負","window":"連兩季","source":"季度財報","last_status":"warning"},{"metric":"ECS帳單金額年增率","bear_threshold":"連兩季低於10%","window":"連兩季","source":"公司法說","last_status":"ok"},{"metric":"DRAM現貨價季變動","bear_threshold":"連兩季季減超過10%","window":"連兩季","source":"資料缺口，事實表未提供序列","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"7a","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":true,"basis":"valuation_dependent=True, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-7.11, valuation_dependent=True"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['7a']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"收盤價不高於150美元（用目前股數調整的五年平均EPS約8.6倍，基本情境年化約9%）才重跑研究","exec_line":"現價不追；跌到150美元以下且訂單出貨比仍高於1，重跑研究，通過後分批反買，首筆不超過3%；訂單出貨比跌破1則取消。"},"reasoning":{"industry":"第三季營收10,717.7百萬美元，非GAAP營益率4.1%。Global Components營收約79億美元、營益率5.2%；Global ECS營收約28億美元、營益率3.6%（2026-11-05法說）。2025年沒有單一客戶超過合併營收2%，單一供應商不超過8%，沒有集中度問題，單點依賴是元件週期本身。第三季非GAAP毛利率10.8%，與去年持平，營益率年增130個基點全部來自費用槓桿，費用占毛利比由73.9%降到62.3%。營運資金約占營收18%，第三季增加約9億美元，資金壓在存貨與應收。加值服務2025年約占營業利益30%，今年比重會下降（2026-11-05 CFO）。供需判斷為週期性將反轉，依據見產業欄。","moat":"機制是產品線廣度、全球物流與信用額度：10-K指出多數客戶要的交期或數量，原廠通常不直接提供。同業對照上，ARW的TTM毛利率11.43%、營益率4.02%都高於AVT的10.43%、3.11%，但AVT的期間只到2026年6月，少了一個景氣最好的季度，差距被放大；事實表沒有同業ROIC。定價力的反證較強：年度毛利率由FY2022的13.03%連降到FY2025的11.24%（事實表年度財務史，yfinance），這輪缺貨中第三季非GAAP毛利率仍是10.8%。公司揭露的非GAAP ROIC為15.1%，年增7.8個百分點，推算投入資本大致持平，報酬提升來自週期回升，不是新資本賺得更多。這個判斷的反例：毛利率下滑部分來自硬體與低毛利品項的組合變化，若拆開後核心毛利率其實上升，定價力應上調，但事實表沒有拆分資料。","growth":"第三季成長以漲價為主，第四季財測以出貨量為主，近12個月沒有重大併購，回購小幅。共識EPS由FY2025的10.93美元到FY2028E的27.20美元，三年CAGR 35.5%，但基期是GAAP且接近週期低點；FY2026E到FY2028E只有12.1%。內生上限8.1%，缺口27.4個百分點（兩年口徑為4.0個百分點），主要歸因營益率隨週期回升，其次是回購，不是可持續的再投資報酬。EPS預估家數事實表未涵蓋。市占只有聚合網站的14.49%，不足以用滲透率推算成長年限。","governance":"FY2022至FY2025的FCF對淨利比分別為−8%、69%、265%、−7%，四年累計46%（事實表年度財務史，yfinance）。TTM FCF利潤率4.03%，推算主要靠2025年第四季的流入，2026年第三季FCF已是−4.68億美元。SBC占營收約0.11%，年化約占市值0.5%。第二季回購4,300萬美元、第三季9,300萬美元，兩季年化約占市值3.0%；不配息。總債務季增5.81億美元到28億美元，調整後槓桿由第二季1.75倍升到1.9倍。近三年現金去向四分、回購均價、債務到期結構事實表未涵蓋。","valuation":"現價181.09美元，以9.5倍週期中段本益比反推，市場要求中段EPS約19.1美元。FY2022至FY2026E的平均淨利約8.82億美元，除以目前50.56百萬股，約17.4美元，現價約10.4倍；要求水準比這個平均高約9%。12個月看FY2028E EPS 26.5美元×8.0倍＝212美元，上行17%；24個月因市場開始預期下行，用7.5倍，199美元，上行10%。賣方目標價190至215美元都早於第三季財報，參考性低，全距132至250美元未超過2.5倍。同業本益比事實表未涵蓋。","premortem":"循環位置用需求量循環五項訊號判斷：訂單出貨比遠高於1但未量化，偏中性；客戶開始加回緩衝庫存、Arrow存貨今年增加44%，亞太通路庫存卻據分析師引述處於低點，偏賣；本益比位於年度端點中段，偏買；終端資本支出週期事實表未涵蓋，中小客戶才剛回來，中性；RSI 30.73、賣方多為持有，偏買。結論是中循環，姿態為持有不加。P/B事實表未涵蓋，反動能檢查無法全部完成。衰退訊號亮一項，陷阱風險中等。產業態勢：競爭面原廠直銷與電商切入持續，結構面缺貨與加值服務有利，其他變數是關稅與出口管制，裁決為雙向拉鋸。歷史最大回撤與空方具體數字事實表未涵蓋，回撤區間由盈餘推估。"},"plain":{"six":{"how_it_makes_money":"賺的是原廠與大量中小客戶之間的備貨、撮合與加值服務價差，毛利約一成一，錢卡在營運資金週轉，獲利高低由元件週期決定。","moat":"護城河持平：規模與產品線廣度的優勢還在，執行面變好，定價力卻沒有因缺貨而提升。","growth":"五年後的成長空間中等：通路本身成熟，加值服務是部分第二曲線，尚未被證明能撐起獨立成長。","capital":"現金流上行期被存貨吃掉、下行期回流，SBC稀釋很低；併購與回購的實際報酬無法從現有資料驗證。","valuation":"現價要求週期中段EPS約19美元才划算，達得到但沒有折價；8.4倍的低本益比不能當作便宜的證據。","how_wrong":"最可能的錯誤是把週期高點當成新常態；反方向的錯誤是太早放棄一段還沒走完的上行。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":true,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等收盤價不高於150美元，且訂單出貨比仍高於1。","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":181.09,"week26_return_pct":-7.11,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026E EPS 21.64美元接近FY2022的21.80美元，上一輪兩年內跌到7.29美元；第三季EPS還含約0.39美元的稅務和解效果（按24%稅率換算）。PEG 0.24的基期是GAAP且接近谷底，不能當便宜證據；改用FY2026E到FY2028E的12.1%，PEG為0.69。三個年度共識修正皆為0.0%，與第三季大幅超標矛盾，判定快照未更新。"},"catalysts":[{"date":"2027-01-01","date_precision":null,"type":"other","event":"Rodney Clark接任ECS總裁。","impact":"中","watch":"ECS供應商關係與帳單成長是否延續。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與2027年第一季財測。","impact":"高","watch":"Components量價拆分與營益率、存貨、營運現金流、ECS帳單基礎營益率。"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"2027年第一季財報。","impact":"高","watch":"積壓訂單是否延伸到2027年底以後，AIS存貨是否轉成出貨。"}],"_projected_from":"v19"}
```
