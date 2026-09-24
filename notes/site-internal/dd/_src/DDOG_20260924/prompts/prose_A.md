你是 stock-analyst v20 的**散文層（prose）agent**，標的 DDOG（2026-09-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20260924/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：DDOG　日期：2026-09-24　archetype：None　前份裁決：2026-05-16　觀望（衛星候選 B，thesis 完整但估值🔴 + 4 週 +45% 漂移 + BB 上軌外 14%，等回測 BB 中軌 $131 或 W52 $139 + Fwd PE 修復至 55-60x 再分批）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1739B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（925B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（996B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1366B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1274B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（719B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（814B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2121B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4407B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2149B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1739           3683-5261      5 條（2–6 內）  
s3                  8000         925           4952-7075      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3636          7955-11364      5 條（2–6 內）  
s6                 11000         719          7197-10281      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         814           1880-2686      5 條（2–6 內）  
s10                 5000        2121           2015-2879      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2149           2000-2851      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5541B；至少需散文≈39.46KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70%
−70
−62.5%
−55%
−45
−45%
−31%
−29%
−20%
−16%
−14%
−5.5
−5.5%
−5%
−3%
0
0.2%
0.3
0.3%
0.4
0.43%
0.5%
0.585
0.7
0.75
0.985
1
1%
1.116
1.15
1.3
1.4%
1.5%
1.7
1.8
1.9
1.915
2
2%
02
2.1
2.203
2.5%
2.50
2.53
2.54
2.7
2.787
2.8
2.85
2.9
2.95
2.97
3
3%
3.15
3.38%
3.4
3.40
3.75
3.78
3.9
4
4%
4.05
4.45
4.55%
4.6
5%
5
05
5.05
5.2
5.78%
6
06
6.00
6.2
7
07
7%
7.4
7.4%
7.5
08
8
8%
09
9
10%
10
11%
11
11.21
11.4
11.4%
11.45
12
12%
13%
13
13.5%
14
14.9%
15%
16
16%
17
17%
17.4%
18
18%
19
19%
19.6%
20
20%
20.9%
21.5%
21.7%
21.8
22%
22.5%
22.8
22.9%
23%
24
24%
24.9%
25
25%
26%
26
27%
27.0%
28%
28.6%
29%
30%
30
32
32%
33.5
34%
35%
35.6%
36%
37%
38%
40%
40
40.6
41.0
42
42.8%
43.0
43%
43.4
44%
44.5
44.7
45
46
46.8%
49
50
50%
52%
52
54.6%
55
58%
58.5
60
60%
62
65
70
74
76
77%
78%
79.6%
80%
80
80.9%
84.7
85.7%
90%
90
91%
99
99.4
100
100%
103.98
104%
110%
115%
120%
131
$131
139
$139
142
150%
158
163
177.7
178
185
207.98
212
220.3
238
251.49
270
278.7
285.28
295
300
330
341
405
503
950
2021
2023
2024
2025
2026
2027
2028
2031
2036
20260924
1,000
1,121
32,000
33,400
4,720
7,000
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
{"meta":{"ticker":"DDOG","date":"2026-09-24","schema":"v15.2","contract":"v19","company_name":"Datadog, Inc."},"oneliner":"雲端與AI系統觀測平台龍頭：非AI業務連5季加速、毛留存90%中後段，生意沒變壞；但股價約99倍今年EPS，Base情境五年年化約1%，要等回到185美元附近再談。","thesis":{"H":[{"id":"H1","text":"核心非AI業務維持20%以上成長，總營收在最大客戶減量後仍守住20%以上","2y":"2028年Q2前非AI客戶營收年增每季≥20%；FY2027營收年增≥20%","5y":null,"10y":null,"threshold":"非AI客戶營收年增≥20%（目前20%後段）；FY2027營收年增≥20%（共識22.5%）","source":"公司季報電話會非AI營收年增口徑；FY2027全年指引","drift_rule":"連2季低於門檻5%以上（低於19%）＝削弱；連3季低於門檻10%以上（低於18%）＝反轉"},{"id":"H2","text":"整合平台讓客戶越用越多產品，留存維持高檔、錢包份額持續擴大","2y":null,"5y":"2031年前用6項以上產品的客戶比率從37%升到≥50%，TTM淨營收留存維持≥115%","10y":"2036年觀測性市占由13%–14%升到≥25%","threshold":"TTM淨營收留存≥115%、毛留存維持90%中段以上","source":"公司季報電話會留存與多產品揭露；管理層會議市占陳述","drift_rule":"5年期：留存連4季低於門檻5%以上＝削弱、連6季低於門檻10%以上＝反轉；10年期：市占跨2個年度未升＝削弱、跨3個年度＝反轉"},{"id":"H3","text":"營業槓桿與股權激勵下降，讓營收成長轉成每股盈餘","2y":null,"5y":"FY2028非GAAP營業利益率≥25%、股權激勵占營收≤16%、淨稀釋每年≤3%","10y":null,"threshold":"FY2028非GAAP營業利益率≥25%（長期目標25%以上）且股權激勵占營收≤16%（Q2 FY2026為19.6%）","source":"公司季報新聞稿；2026-02-12投資人日長期目標","drift_rule":"連4季TTM偏離門檻路徑5%以上＝削弱；連6季偏離10%以上＝反轉"}],"R":[{"id":"R1","text":"最大客戶與AI原生客群用量可逆：續約後減量，2024年已有AI原生客戶部分改自建","h_ref":"H1","clock":"⚡","threshold":"再次揭露最大客戶減量，或下季營收指引年增低於20%；連2季即減碼","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#5","end_markets#2"]},{"id":"R2","text":"跨界平台捆綁與計價模式轉變壓低單位收費，留存與毛利率下滑","h_ref":"H2","clock":"🔥","threshold":"TTM淨營收留存連4季低於115%，或非GAAP毛利率連2季低於78%","evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#1","supply_demand_durability#1","supply_demand_durability#7"]},{"id":"R3","text":"自建模型的GPU與token支出加上高股權激勵，吃掉營業槓桿：2026-05-07 CEO說工作負載走營業費用、若資本支出模式改變會告知；2026-09-08 CEO已說token與算力帳單暴增、GPU支出增加且還會更多","h_ref":"H3","clock":"🐢","threshold":"全年非GAAP營業利益率低於22%，或股權激勵占營收連2季高於20%，或資本支出加資本化軟體占營收超過5%","evidence_refs":[]}],"single_thing":{"description":"公司下修全年營收指引，打破一向先保守後上修的模式；最可能的成因是最大客戶或AI原生客群進一步減量","why_fatal":"現價約99倍FY1 EPS，隱含每季持續超出並上修；公司自稱每天看得到逐客戶用量，一旦下修代表需求真的斷了而非保守過頭，倍數會先腰斬（55倍×2.53≈139美元，約−45%）","if_happens":"持有者清倉；未持有者不承接，等下一季數字重跑完整判斷","how_monitor":"每季財報的全年指引中值對比前次；最大客戶相關揭露；FY2026年報客戶集中度","probability":"12–24個月約15%：最大客戶已改為只以承諾額入財測，Q3與Q4有下限，但AI原生客群用量可逆"}},"appendix_a":{"growth_durability":8,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":84.7,"peg_fy2":3.9,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":2.53,"FY2027E":2.97,"FY2028E":3.75},"fy_end_month":12,"eps_basis":"非GAAP稀釋EPS，Koyfin共識2026-09-19快照；FY2025實際EPS事實表未涵蓋，故基期留空"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20260924/scenario.json","archetype":{"primary":"品質複利成長","secondary":"未獲利高成長","confidence":"中","fingerprint":"毛利率約80%、FCF率25–27%、營收年增30%上下，但GAAP獲利被股權激勵吃光，股東經濟介於兩型之間"},"industry":{"clock_phase":"II","sd_verdict_source":"核心雲端遷移需求屬結構性持久（CFO引研究機構估雲端應用占比約高20多到30%，2026-09-10）；AI原生客群用量屬週期性、可逆性高（最大客戶續約後減量，2024年另有AI原生客戶部分改自建）","bargaining":{"up":"上游是公有雲基礎設施，工作負載成本走營業費用而非資本支出（2026-05-07 CEO）；毛利率多年守在80%上下，上游議價有限，但自建模型開始增加GPU與token支出（2026-09-08 CEO）","down":"下游議價力兩極：一般企業多產品整併後轉換成本高；超大客戶與AI實驗室有自建能力與量價折扣籌碼，最大客戶續約後減量即為例證","geo":"約44%員工在美國以外、其中34%在法國（FY2025年報）；美洲是AI活動主場，拉美約占營收5%且成長最快；無實體製造與中國台灣供應鏈依賴"},"profit_pool_dir":"觀測性利潤池向整合平台集中（CFO稱少有公司能有機長出整合平台，2026-09-10），但資料儲存層正被Snowflake、Databricks、ClickHouse分走；公司推聯邦日誌讓資料留在外部，等於讓出部分儲存環節換取留存","tam_table":[{"item":"觀測性市場規模（公司口徑）","value":"300億美元以上；加資安與軟體交付後逾1,000億美元（2026-02-12投資人日CFO）"},{"item":"第三方市場規模估計","value":"2026年33.5億至341億美元，差十倍；CAGR 11%–16%。最低一家低於公司自身年營收，定義過窄不採用"},{"item":"Gartner觀測平台市場","value":"2028年142億美元"},{"item":"公司市占","value":"13%–14%（2026-09-08 CEO），投資人日稱十幾個百分點中段"},{"item":"客戶滲透","value":"約32,000家對目標約50萬家＝7%（2026-02-12投資人日）；Q2 FY2026客戶數33,400"},{"item":"完全滲透客戶的觀測加資安支出","value":"約占其雲端帳單10%–20%（2026-09-08 CEO）"},{"item":"營業利益池占比5年前到現在","value":"事實表未涵蓋"}]},"moat":{"mechanism":"整合平台加資料引力：四大支柱共用同一份資料與同一個承諾額度池，多產品客戶比率逐年升；轉換成本在重建告警、儀表板與跨團隊工作流，不在資料收集（2026-02-12 CEO：收集從來不是護城河）","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大（非AI業務連5季加速、新企業客戶年化訂單年增逾一倍、超大雲端業者AI實驗室改外包給公司）；定價面穩定偏縮（主動推降低帳單的計價、最大客戶續約後減量、Ramp採用率年比持平）","peer_na_reason":"事實表同業對照未含投入資本與ROIC，只能以營業利益率、FCF率替代","threats":[{"level":"🔴","text":"生態攻擊：Palo Alto收Chronosphere、Snowflake收Observe、Cisco整合Splunk，把觀測性綁進資安或資料平台賣，壓縮獨立平台的整併空間","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"計價與架構挑戰：eBPF取代語言代理、資料留在客戶雲內、按基礎設施計價（競品行銷說法）；公司已自推自帶雲接招，但會壓低單位收費","p":"30%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"開發工具廠商把可觀測性做進自家產品；coding agent已能處理部分事後排查（2026-02-12 CEO承認）","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"開源與低價對手：Grafana ARR逾4億美元；Gartner稱逾40家廠商、總持有成本已成標準提問","p":"30%","evidence_refs":["supply_demand_durability#7","supply_demand_durability#1"]},{"level":"🟡","text":"超大客戶自建：2024年一家大型AI原生客戶縮減並部分改用內部工具，造成成長放緩；本輪最大客戶續約後減量","p":"30%","evidence_refs":["customer_second_source#4","customer_second_source#0"]}],"roic_durability":{"quadrant":"非GAAP口徑高利益率×高周轉（輕資產、預收款使營運資金為負）；GAAP口徑因股權激勵占營收19.6%，利益率近零。投入資本事實表未涵蓋，當期ROIC數值不算","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（工程師）、決策者（平台與工程主管）、付款者（財務長）分開看：前兩者的需求是系統掛掉就賠錢的必需品，DASH上工程師高度肯定產品；付款端有帳單抱怨，但毛留存仍在90%中後段，需求轉得成收入。要解決的問題（維運雲端與AI系統）會持續，公司的解法可被替代但替代成本高"},{"item":"決策層級","level":"🟡","text":"替代要在最小決策單位看：單一團隊決定哪些日誌送進來、哪些指標加標籤，可以逐項外移（聯邦日誌、自帶雲、開源收集標準讓收集層無鎖定）；整體換平台則要重建告警、儀表板與跨產品工作流，毛留存90%中後段顯示整體替代少，但最大客戶續約後減量說明局部替代正在發生"},{"item":"價值鏈分配","level":"🟡","text":"完全滲透客戶把雲端帳單10%–20%花在觀測與資安（2026-09-08 CEO），占比高、易被財務盯上；上游雲端與資料平台（Snowflake、Databricks、ClickHouse）同時想分這塊，公司以聯邦日誌讓出部分儲存環節；AI實驗室與超大雲端業者具自建能力，買方集中處議價力偏向客戶"},{"item":"社會容忍度","level":"🟡","text":"無監管授權依賴，FedRAMP屬認證而非獨占；真正的天花板是客戶預算容忍度：公司刻意推無限基數指標等降低帳單的計價、不把價格推到經濟上限，等於付保費換留存，實際定價上限是客戶財務長能接受的帳單占比"}],"roiic":"公式口徑不適用：成長投入費用化（研發約營收30%），資本支出加資本化軟體只占營收4%–5%，營運資金因預收款為負，按公式再投資率趨近零或為負，增量報酬無意義","reinvest_rate":"同上；折舊攤銷與營運資金變動事實表亦未涵蓋","endo_ceiling":25,"formula_note":"改用留存口徑代理：TTM淨營收留存120%出頭，既有客戶約貢獻20個百分點成長；新客戶占年增量約30%（Q2 FY2026），推得營收內生成長約20÷0.7≈28.6%；扣管理層淨稀釋目標2.5%–3%（投資人日）且利益率持平，每股EPS內生上界約25%。資本配置評為最低一級時再打八折＝20%"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","DDOG":79.51,"PLTR":84.8,"CRM":77.28,"NOW":74.77,"MSFT":67.94,"unit":"%"},{"metric":"營業利益率","DDOG":0.43,"PLTR":42.8,"CRM":21.52,"NOW":11.4,"MSFT":46.78,"unit":"%"},{"metric":"FCF 利潤率","DDOG":27.04,"PLTR":54.55,"CRM":34.49,"NOW":31.03,"MSFT":20.19,"unit":"%"},{"metric":"研發密度","DDOG":43.69,"PLTR":10.42,"CRM":14.49,"NOW":22.14,"MSFT":10.72,"unit":"%"}],"competitors":[{"name":"PLTR","gm":84.8,"om":42.8,"fcf_margin":54.55,"rd_intensity":10.42,"strategy_note":"非直接競爭；營業利益率42.8%、FCF率54.6%，示範軟體平台規模化後的利潤上限","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CRM","gm":77.28,"om":21.52,"fcf_margin":34.49,"rd_intensity":14.49,"strategy_note":"非直接競爭；營業利益率21.5%，成熟應用軟體的利潤參照","period":"TTM ending 2026-07-31（4季加總）"},{"name":"NOW","gm":74.77,"om":11.4,"fcf_margin":31.03,"rd_intensity":22.14,"strategy_note":"IT營運流程平台，正往可觀測性延伸（2026-09-08分析師提問），潛在跨界者；營業利益率11.4%","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MSFT","gm":67.94,"om":46.78,"fcf_margin":20.19,"rd_intensity":10.72,"strategy_note":"Azure原生監控是雲端內建替代品，但多雲客戶仍需中立平台；營業利益率46.8%","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（既有客戶用量約占成長七成）加交叉銷售；新客戶占年增量30%；小額併購補技術；無回購、每年淨稀釋2.5%–3%","runway_years":7,"runway_post_y5":"🟢","endo_ceiling_basis":"引護城河題的留存口徑代理：營收內生約28.6%、扣淨稀釋後EPS約25%，資本配置最低一級打八折＝20%；兩年共識CAGR 21.7%高出1.7個百分點，歸因於營業利益率由23%走向25%以上","segments":[{"item":"基礎設施監控ARR","value":"逾16億美元（2025年底）"},{"item":"日誌管理ARR","value":"逾10億美元，年增30%中段（2025年底）"},{"item":"APM ARR","value":"逾10億美元，年增30%中段（2025年底）"},{"item":"RUM ARR","value":"逾2億美元，年增逾50%（Q2 FY2026）"},{"item":"資安產品ARR","value":"逾1億美元（2026-02-12投資人日）；百萬美元客戶中資安僅占其支出2%"},{"item":"Flex Logs ARR","value":"接近1億美元（2026-02-12投資人日）"},{"item":"非AI客戶營收年增","value":"20%後段（Q2 FY2026），Q1為20%中段、一年前18%"}],"decay_signals":[{"signal":"毛利率連2季年比下滑","status":"觀察","note":"Q2 79.6%較一年前80.9%降1.3個百分點；Q1年比事實表未涵蓋，未確認連2季"},{"signal":"核心市占近12個月縮減","status":"未亮","note":"Ramp採用率34%年比持平"},{"signal":"主力產品提價後銷量下滑","status":"未亮","note":"未見提價，反而主動推降低帳單的計價"},{"signal":"EPS CAGR高於營收CAGR逾5個百分點","status":"未亮","note":"FY2027共識EPS年增17.4%低於營收共識年增22.5%"},{"signal":"FCF對淨利低於0.75連2年","status":"未亮","note":"FCF遠高於淨利"},{"signal":"股權激勵占營收高於5%且逐年上升","status":"觀察","note":"19.6%遠高於5%，逐年序列事實表未涵蓋"},{"signal":"TAM萎縮或被替代技術壓縮","status":"未亮","note":"第三方CAGR 11%–16%"},{"signal":"產業估值倍數近3年系統性下移","status":"未亮","note":"公司P/S位於4個年度端點最高"},{"signal":"維持性資本支出占FCF高於60%","status":"未亮","note":"資本支出加資本化軟體僅營收4%–5%"},{"signal":"停止投資新產能且收入3年內下滑","status":"未亮","note":"研發維持約營收30%"}],"trap_rating":"🟢"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：兩個期間的收購各約1.8–1.9億美元、占市值不到0.3%；不配息、未見回購，沒有可展開的股東回饋紀錄"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2026上半年三筆收購合計1.915億美元（10-Q），約占市值0.2%，公司認定不重大，已實現報酬無從量測","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未見回購；管理層只給淨稀釋目標","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"淨稀釋目標每年2.5%–3%（2026-02-12投資人日CFO），高於1.5%；股權激勵占營收19.6%（Q2 FY2026）","grade":"不過"}]},"valuation":{"basis":"非GAAP Fwd P/E（FY1與FY2）加PEG；GAAP盈餘被股權激勵吃掉，不採用","tier":"高成長基礎軟體平台","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率沒有倍數，同業Fwd P/E未涵蓋，不能拿來當倍數錨；終端倍數改以公司自身前份區間（成熟期50–65倍、穩定期40–50倍）與成長率對照"},"fwd_pe":99.4,"peg":4.6,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"FY1 Fwd P/E 99.4倍、FY2 84.7倍；PEG約4.6（高於2為貴）；P/S位於4個年度端點最高；Base情境五年年化約1.4%，低於8%及格線，結論為最貴一級。上行空間：短期＝12個月後FY2027共識EPS 2.97×80倍≈238美元，約−5.5%；中期＝五年Base 270美元，約+7.4%","targets":{"sellside_mean":285.28,"sellside_median":295,"sellside_high":330,"sellside_low":158,"sellside_count":46},"upside_short_pct":-5.5,"upside_mid_pct":7.4},"trap_analysis":{"verdict":"🟢","label":"生意不是陷阱，價格才是風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2024年一家大型AI原生客戶縮減並部分改用內部工具，直接造成當年成長放緩；本輪最大客戶續約後減量，其所屬的AI原生客群2025年Q4貢獻約7個百分點年增；另有報導稱AI原生客群2026年Q1只成長個位數高段","assumption":"非AI業務的加速能長期抵銷AI原生客群的波動，且公司對AI原生曝險遠小於疫情時雲原生客群的約40%","consequence":"若AI原生客群集體優化、同時企業進入新一輪用量優化，成長從30%掉到15%以下，倍數由近百倍壓到30倍上下，五年後虧損五成以上","ruling":"部分採納：這是Bear情境的主軸，機率給30%、最大回撤低點端−70%；不全採，因管理層稱扣掉最大客戶後其餘業務成長率幾乎相同、非AI業務連5季加速、毛留存90%中後段。與唯一致命點部分重疊：唯一致命點是下修全年指引這個離散事件，本條是其背後最可能的成因","watch":"每季非AI營收年增、公司是否再揭露最大客戶減量、FY2026年報是否揭露單一客戶占營收10%以上","evidence_refs":["customer_second_source#4","customer_concentration_credit#5","customer_second_source#1","customer_concentration_credit#0"],"fact_refs":["f_kpi15_ai_yoy","f_kpi11_ai_native_1m_1m_arr_ai"]},{"view":"論點成功但股東經濟變差","evidence":"股權激勵占營收19.6%、占非GAAP營業利益85.7%，扣掉後FCF率只剩約5%；管理層淨稀釋目標每年2.5%–3%；CEO稱內部token與算力帳單暴增、開始在GPU上花更多錢訓練自家模型，且後續支出還會增加（2026-09-08）；公司同時推降低客戶帳單的計價換留存，總持有成本已是客戶標準提問","assumption":"營業利益率能從23%走向25%以上，股權激勵占比逐年下降","consequence":"營收照樣年增20%以上，但每股EPS年增只有十幾%，股東拿到的遠少於營收成長","ruling":"採納：Base情境EPS年增約19%，低於前兩年營收成長，資本配置評為偏弱；股權激勵占營收若連2季高於20%，或全年非GAAP營業利益率跌破22%，視為此路徑成立","watch":"每季股權激勵占營收、稀釋股數年增、非GAAP營業利益率、資本支出加資本化軟體占營收","evidence_refs":["substitute_technology#0","supply_demand_durability#1"],"fact_refs":["f_kpi4_stock_based_compensation","f_kpi2_gaap_operating_income_ma","f_kpi3_free_cash_flow"]},{"view":"價格已反映太多","evidence":"26週漲104%；Fwd P/E 99.4倍（FY1）、P/S位於4個年度端點最高；Q3指引年增28%–29%，低於Q2的36%；Q2財報揭露最大客戶減量後股價曾跌14.9%","assumption":"市場會繼續用Q2的加速外推，並在第五年仍給60倍以上","consequence":"即使生意照Base走，五年年化只有約1%；任何一季成長不及預期都會先殺倍數","ruling":"採納：這是本輪觀望的綁定約束；股價回到185美元以下（FY2027共識EPS約62倍），Base五年年化才到約8%","watch":"FY2 Fwd P/E、每季營收相對指引上緣的超出幅度、FY2027共識EPS修正","evidence_refs":["end_markets#3","capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_ps_percentile","f_kpi5_guidance_q3_fy2026_reven"]}],"max_dd":{"lo":-70,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 207.98 → 本次 251.49（+20.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=207.98","side_b":"本次 price_at_dd=251.49","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"最大客戶的財測方法前後說法","cause":null,"prior_field":null,"side_a":"2026-05-07 Q1法說CFO：對最大客戶與上季一樣採更高程度保守，方法沒有改","side_b":"2026-08-06 Q2法說CEO：這次對最大客戶權重放得不一樣、完全去風險；2026-09-10高盛會議CFO：改成只把合約承諾額放進財測","ruling":"可調和、屬程度差異：方法確實改了，從打折用量變成只算承諾額，原因是該客戶用量已低於過去軌跡。好處是該客戶在財測裡有下限（CFO：不能低於承諾額），Q3與Q4下行有底；壞處是承諾額以上的用量不再算數，代表用量波動比公司過去說的大","evidence_level":"管理層原話（法說與會議逐字稿）","settle_metric":"Q3 FY2026營收相對指引上緣11.45億美元的超出幅度","if_then":["若Q3營收超出指引上緣3%以上且公司未再提最大客戶減量→視為減量已被承諾額兜住，維持觀望、不調機率","若公司再次揭露最大客戶減量或下修全年指引→Bear機率上調到35%，持有者減碼一半"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#0","end_markets#2"]},{"axis":"成長是在加速還是減速","cause":null,"prior_field":null,"side_a":"Q2營收年增35.6%、非AI客戶加速到20%後段、RPO年增43%、cRPO約40%、billings年增38%","side_b":"Q3指引年增28%–29%，FY2027營收共識年增22.5%","ruling":"可調和、屬程度差異：Q2指引29%–31%，實際做到35.6%，公司指引一向保守；Q3指引已計入最大客戶減量。cRPO約40%年增高於指引，支持Q3實際高於指引；但FY2027共識22.5%才是估值該用的成長率","evidence_level":"公司財報與指引","settle_metric":"Q3 FY2026實際營收年增率","if_then":["若Q3年增≥32%且Q4指引年增≥27%→FY2027共識EPS可能上修，重啟價位隨共識上修等比上調","若Q3年增低於30%→保守緩衝變薄，不追、停止加碼"],"evidence_refs":["end_markets#3"]},{"axis":"份額方向","cause":null,"prior_field":null,"side_a":"CFO：與競爭對手相比市占增幅非常大（2026-08-12）；CEO：規模上勝過所有對手並在搶市占（2026-05-07）","side_b":"Ramp：採用觀測性廠商的組織中34%用公司，年比持平；網站偵測占比5.78%排第三","ruling":"可調和、屬口徑差異：Ramp與網站偵測看的是有沒有用，不看花多少；公司靠既有客戶多買產品擴大錢包份額，採用家數持平與營收份額上升可以同時成立。但這也表示新客戶滲透加速沒有外部證據，護城河方向不判擴大","evidence_level":"第三方採購資料對管理層陳述","settle_metric":"Ramp採用率年比變化、新客戶占年增量比例","if_then":["若Ramp採用率年比下滑超過2個百分點→份額縮減列為衰退信號亮燈，護城河方向重評","若新客戶占年增量連2季≥30%→新客戶滲透加速成立"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"跨界整併是否削弱公司地位","cause":null,"prior_field":null,"side_a":"CFO：Snowflake、Palo Alto、Splunk之類的跨界進攻沒有改變競爭態勢，結果是公司地位增強（2026-08-12）","side_b":"第三方評論稱Palo Alto收Chronosphere、Snowflake收Observe形成夾擊；競品稱eBPF、自帶雲、按基礎設施計價是架構轉變；Gartner稱逾40家廠商、總持有成本已成標準提問","ruling":"方向相反、不可調和；裁定採管理層一側，依據是硬數據：非AI業務連5季加速到20%後段、毛留存90%中後段、Q2新企業客戶年化訂單年增逾一倍、多產品滲透一年內明顯加深；若夾擊已生效，這些數字應先轉弱。但定價面已被迫讓利（無限基數、聯邦日誌、自帶雲），所以護城河方向只判穩定不判擴大","evidence_level":"公司財報數據對第三方評論與競品行銷","settle_metric":"TTM淨營收留存率與非GAAP毛利率","if_then":["若淨營收留存連2季降到110%後段以下且非GAAP毛利率低於78%→改判夾擊生效，護城河方向下調為縮減，持有者減碼至一半","反向條件：若淨營收留存維持120%出頭且非AI年增連2季≥25%到2027年Q1→護城河方向可回到擴大"],"evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#1","supply_demand_durability#1","supply_demand_durability#7"]},{"axis":"AI原生客群曝險大小","cause":null,"prior_field":null,"side_a":"CEO：對AI原生客戶的曝險比當年雲原生客戶（高峰約40%）小很多，上行大於下行（2026-09-08）","side_b":"AI原生客群去年底約占營收11%（投資人日），2025年Q4貢獻約7個百分點年增、2026年Q1仍是個位數高段；最大客戶就在這個客群","ruling":"可調和：營收占比確實小，但對成長率的貢獻遠高於占比；它是加速的邊際來源，不是營收主體。估值用的成長率要扣掉這部分的波動","evidence_level":"管理層陳述與年報、季報轉述","settle_metric":"AI原生客群對年增的貢獻百分點","if_then":["若AI原生客群對年增貢獻降到3個百分點以下而總成長仍≥25%→核心自給自足，Bear機率下調5個百分點","若AI原生客群貢獻轉負→停止加碼並檢查Bear情境"],"evidence_refs":["customer_concentration_credit#5","customer_second_source#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"公司指引一向先保守後上修：FY2026營收指引一年內從40.6–41.0億美元上調到43.0–43.4億、再到44.5–44.7億美元；CFO稱每天看得到逐客戶用量、幾近完整資訊（2026-08-12）；cRPO年增約40%、非AI連5季加速、超大雲端業者改外包、FY1共識近3個月上修4.55%。若FY2027 EPS最後做到3.4美元，現價只有74倍","side_b":"就算FY2027做到3.4美元，74倍仍需五年EPS年增20%以上且終端仍給50倍以上才有年化8%；Q3指引已降到28%–29%，最大客戶減量顯示AI原生用量可逆","ruling":"部分採納：上修空間真實存在，所以重啟條件加一條FY2027共識EPS上修到3.40美元以上時門檻同比上調；但在現價，Base五年年化約1.4%，不足以建倉","evidence_level":"公司指引紀錄與管理層原話","settle_metric":"FY2027共識EPS","if_then":["若FY2027共識EPS上修到3.40美元以上而股價漲幅未超過10%→重跑判斷，視為估值落差收斂","若FY2027共識EPS下修→重啟價位同比下調"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"]},{"axis":"綜合評級與估值（前份漂移）","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-16，股價207.98美元）：綜合評級B、估值最貴一級","side_b":"本輪（股價251.49美元，+20.9%）：綜合評級B、估值最貴一級，兩欄都不變；FY1 Fwd P/E 99.4倍、PEG約4.6","ruling":"結論不變但更貴：股價漲20.9%，同期FY1共識EPS近3個月只上修4.55%，漲幅遠大於盈餘上修；生意品質沒有退步，綜合評級仍是B","evidence_level":"事實表價格與共識快照","settle_metric":"FY2 Fwd P/E","if_then":["若FY2 Fwd P/E回到62倍以下→估值結論降一級並重跑判斷","若FY2 Fwd P/E升破100倍→維持觀望、不追"],"evidence_refs":[]},{"axis":"護城河方向與陷阱風險（前份漂移）","cause":"新證據","prior_field":["moat_trend","trap"],"side_a":"前份：護城河方向擴大；價值陷阱風險低","side_b":"本輪：護城河方向穩定；價值陷阱風險低不變","ruling":"方向由擴大調為穩定：2026-08-06揭露最大客戶續約後減量（領先者在最大客戶的份額下滑，不能判擴大）、Ramp採用率年比持平、公司主動推降低帳單的計價換留存；執行面仍在擴大，定價面小幅讓利，淨為穩定。陷阱風險維持低：十類衰退信號無一確認亮起","evidence_level":"公司法說揭露與第三方採購資料","settle_metric":"TTM淨營收留存率、Ramp採用率年比","if_then":["若淨營收留存維持120%出頭且Ramp採用率年比上升≥2個百分點→方向回到擴大","若淨營收留存連2季降到110%後段以下→方向下調為縮減"],"evidence_refs":["customer_second_source#0","customer_concentration_credit#0","competitive_share_entrants#0"]},{"axis":"前份空白欄位補齊（前份漂移）","cause":"方法變動","prior_field":["dca_verdict","dca_role","runway_post_y5","archetype","cycle_position","asym_ratio","ev5y_pct","irr_base_pct","max_dd_pct","bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位全為空白：舊流程把裁決寫成一段文字，沒有落欄，也沒有情境樹機率與最大回撤","side_b":"本輪：五年後跑道判寬、生意型態判品質複利成長；情境樹三支路徑（Bull 60倍、Base 45倍、Bear 32倍）與機率25／45／30、最大回撤−45%至−70%，報酬與不對稱比由程式算出；裁決與角色由決策矩陣算出；循環位置不適用（非循環股）仍留空","ruling":"屬方法變動而非判斷翻面：前份沒有這些欄可比，本輪首次落值，不代表基本面變化","evidence_level":"流程口徑","settle_metric":"無（口徑對齊）","if_then":["下次複審起這些欄位逐欄對帳，任何變動需歸因到價格、新證據或方法"],"evidence_refs":[]},{"axis":"重啟門檻（前份漂移）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"等回測 BB 中軌 $131 或 W52 $139 + Fwd PE 修復至 55-60x 再分批","side_b":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","ruling":"重啟首倉（分批加碼）的門檻從技術位階加倍數區間，改成報酬率錨：以Base情境五年價值270美元反推年化8%的買點。前份131美元與139美元是技術位置，現在52週均線已升到177.7美元，舊門檻失去意義；55–60倍的倍數條件以FY2027共識EPS 2.97換算落在163–178美元，與新門檻185美元相近","evidence_level":"情境樹反推與週線均線","settle_metric":"股價相對185美元","if_then":["若股價≤185美元且最近一季非AI營收年增≥20%→重跑判斷，通過後分批首倉三分之一","若FY2027共識EPS上修到3.40美元以上→門檻同比上調到約212美元"],"evidence_refs":[]},{"axis":"出場指標（前份漂移）","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設出場指標（空白）","side_b":"非AI營收年增連3季低於18%；全年營收指引任一次下修；TTM淨營收留存連2季降到110%後段以下；股權激勵占營收連2季高於20%；非GAAP毛利率連2季低於77%","ruling":"新設理由是2026-08-06揭露的最大客戶減量，讓用量可逆性成為可量測風險：全年指引下修觸發清倉，非AI年增與留存轉弱觸發減碼一半，股權激勵與毛利率觸發停止加碼","evidence_level":"公司法說揭露","settle_metric":"各出場指標每季讀數","if_then":["任一清倉條件觸發→持有者清倉並重跑判斷","兩項減碼條件同時觸發→持有者減碼一半"],"evidence_refs":["end_markets#2"]},{"axis":"Single Thing（前份漂移）","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"公司下修全年營收指引，打破一向先保守後上修的模式；最可能成因是最大客戶或AI原生客群進一步減量","ruling":"Single Thing新設：最大客戶續約後減量（2026-08-06）與財測方法改為只算承諾額（2026-09-10），讓指引下修成為近百倍倍數最敏感的單一離散事件；發生即清倉","evidence_level":"公司法說與會議原話","settle_metric":"每季全年指引中值對比前次","if_then":["若下修→持有者清倉","若連續兩季上修且非AI年增≥25%→機率由15%下調到10%"],"evidence_refs":["customer_concentration_credit#0"]}],"triggers":[{"n":1,"text":"非AI客戶營收年增守住20%","type":"假設驗證","maps_to":"H1","metric":"非AI客戶營收年增率（公司季報口徑）","threshold":"連2季低於19%＝削弱；連3季低於18%＝反轉","action":"削弱→停止加碼；反轉→持有者減碼一半","source_freq":"季報電話會，每季","date":"2026-11（Q3 FY2026財報）"},{"n":2,"text":"最大客戶與AI原生客群用量","type":"風險","maps_to":"R1","metric":"公司是否再揭露最大客戶減量；下季營收指引年增率","threshold":"再次揭露減量，或下季指引年增低於20%","action":"持有者減碼一半；未持有者取消重啟","source_freq":"季報，每季","date":"2026-11（Q3 FY2026財報）","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","end_markets#2","customer_second_source#1"]},{"n":3,"text":"下修全年營收指引","type":"Single Thing","maps_to":null,"metric":"全年營收指引區間中值","threshold":"任何一次低於前次指引中值","action":"持有者清倉；未持有者重跑完整判斷後才考慮","source_freq":"季報新聞稿，每季","date":"2026-11（Q3 FY2026財報）","evidence_refs":["end_markets#3"]},{"n":4,"text":"估值回到可分批區","type":"估值rearm","maps_to":null,"metric":"股價與FY2027共識EPS倍數","threshold":"股價≤185美元（約FY2027共識EPS 62倍）；FY2027共識EPS上修到3.40美元以上時門檻同比上調","action":"重跑判斷，通過後分批首倉三分之一","source_freq":"每日股價、每月共識快照","date":null},{"n":5,"text":"留存與定價力","type":"風險","maps_to":"R2","metric":"TTM淨營收留存率、非GAAP毛利率","threshold":"淨營收留存連2季降到110%後段以下，且非GAAP毛利率低於78%","action":"護城河方向下調為縮減，持有者減碼至一半","source_freq":"季報電話會，每季","date":null,"evidence_refs":["competitive_share_entrants#2","substitute_technology#0","supply_demand_durability#7"]},{"n":6,"text":"股東經濟：股權激勵與利益率","type":"風險","maps_to":"R3","metric":"股權激勵占營收、非GAAP營業利益率","threshold":"股權激勵占營收連2季高於20%，或全年非GAAP營業利益率低於22%","action":"下修Base情境EPS路徑，停止加碼","source_freq":"季報新聞稿，每季","date":null},{"n":7,"text":"年報複審：客戶集中度與FY2027指引","type":"複審日期","maps_to":null,"metric":"年報單一客戶占營收揭露、FY2027營收指引年增","threshold":"單一客戶占營收≥10%，或FY2027指引年增低於20%","action":"重跑完整判斷","source_freq":"年報，每年","date":"2027-02"}],"kill_metrics":[{"metric":"非AI客戶營收年增率","bear_threshold":"連3季低於18%","window":"每季，至2028年Q2","source":"公司季報電話會","last_status":"ok"},{"metric":"全年營收指引","bear_threshold":"任一次下修至低於前次指引中值","window":"每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"TTM淨營收留存率","bear_threshold":"連2季降到110%後段以下","window":"每季","source":"公司季報電話會","last_status":"ok"},{"metric":"股權激勵占營收","bear_threshold":"連2季高於20%","window":"每季","source":"公司季報新聞稿","last_status":"warning"},{"metric":"非GAAP毛利率","bear_threshold":"連2季低於77%","window":"每季","source":"公司季報電話會","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場沿用Q2的36%成長並給近百倍FY1非GAAP盈餘；但Q3指引已降到28%–29%、FY2027營收共識年增22.5%，且非GAAP盈餘排除了占營收19.6%的股權激勵，這個成長率配不上現價倍數"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='→', week26=103.98, valuation_dependent=False","input_gap":["week26_return_pct 落 100-150% 邊界帶，QC-42 反動能閘裁量範圍，本腳本無法自動判定，預設不放行"]},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🔴'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","exec_line":"觀望不建倉。綁定約束是估值：股價≤185美元且最近一季非AI營收年增≥20%，重跑判斷通過後分批首倉三分之一；已持有者遇下修全年指引即清倉，非AI年增連2季低於19%減碼一半，波動本身不砍倉。"},"reasoning":{"industry":"單一營運分部，公司不揭露分部損益，改看產品線ARR：基礎設施監控逾16億美元、日誌與APM各逾10億美元（2025年底口徑，2026-02-12投資人日），RUM逾2億美元且年增逾50%（Q2 FY2026）。最新一季（Q2 FY2026）營收11.21億美元、年增35.6%，高於指引上緣；非GAAP毛利率79.6%、非GAAP營業利益率22.9%，GAAP營業利益率只有0.5%，差額主要是股權激勵（占營收19.6%）。年ARR達10萬美元以上客戶4,720家、貢獻約91%ARR，客戶基礎分散，但單點依賴明確存在：最大客戶是一家AI公司（市場推測為OpenAI，公司未證實），用17項產品、剛續簽九位數合約但Q3起減量；最大客戶所屬的AI原生客群去年底約占營收11%（2026-02-12投資人日CFO），並貢獻2025年Q4約7個百分點的年增。產業時鐘判在擴張期：營收年增從25%（Q1 2025）到32%（Q1 2026）再到36%（Q2 2026），非AI客戶年增從18%升到20%後段，依據是客戶用量與新客戶放量，不是股價。供需耐久性：核心雲端遷移需求屬結構性持久（CFO引研究機構估雲端應用占比僅約高20多到30%，2026-09-10），AI原生客群用量屬週期性、可逆性高，這部分餵給Bear機率。","moat":"機制：四大支柱（指標、追蹤、日誌、數位體驗）共用同一份資料、同一個承諾額度池，客戶跨產品用量可互換（2026-09-08 CEO），多產品滲透一年內明顯加深：用4項以上產品的客戶58%（一年前52%）、6項以上37%（29%）、10項以上13%（7%）。可證方向取留存與份額：TTM淨營收留存120%出頭、毛留存90%中後段，屬高黏著；Ramp統計的採用率34%、年比持平，份額擴大沒有外部證據，管理層的大幅搶市占（2026-08-12 CFO）是以營收增量推論。執行面判擴大：非AI業務連5季加速、Q2季增1.15億美元創紀錄、Gartner觀測平台連6年領導者且執行力軸最高、研發約為最接近同業3倍（投資人日）。定價面判穩定偏縮：財務長層級持續抱怨帳單（2026-08-06法說分析師轉述）、第三方稱企業議價可壓牌價35%–55%，公司主動推無限基數指標、聯邦日誌、自帶雲，降低客戶單位成本換留存（2026-09-10 CFO稱對留存與毛利兩利）；另最大客戶續約後減量，領先者在最大客戶的份額下滑，不能判擴大。執行9分、定價7分，扣一個生態攻擊威脅後落B級。同業對照只給利潤率不給投入資本，無法算報酬率差距：GAAP營業利益率0.43%落後PLTR、CRM、NOW、MSFT全部同業，FCF率27.0%居中（高於MSFT、低於CRM、NOW、PLTR），差距主因是股權激勵。產業態勢判雙向拉鋸：競爭面有資安與資料平台跨界整併（Palo Alto收Chronosphere、Snowflake收Observe），結構面雲端遷移與AI工作負載持續擴大需求，商業模式面則有按基礎設施計價與自帶雲的壓力。","growth":"成長來源：量（既有客戶的雲端與AI工作負載用量，約七成成長來自既有客戶）加交叉銷售（多產品滲透加深）；併購只是小額補技術（2026上半年三筆合計1.915億美元），沒有回購，反而每年淨稀釋2.5%–3%。共識EPS FY2026 2.53、FY2027 2.97、FY2028 3.75，兩年CAGR約21.7%（FY2025實際EPS事實表未涵蓋，三年CAGR無法算）。對照內生上界：留存口徑約25%，資本配置最低一級打八折後20%，共識高出約1.7個百分點，可歸因於利益率擴張：非GAAP營業利益率由FY2026指引23%走向長期目標25%以上（投資人日CFO），兩年約多出2個百分點EPS年增。跑道年數：市占取13.5%，公司年增25%、市場年增12%（第三方CAGR 11%–16%中位）時，市占每年約放大1.116倍，約7年到30%，屬中等折扣；五年後市占約23%，仍低於35%，且有第二曲線，判寬。AI淨增量：AI原生客群與AI觀測產品帶來的新營收目前大於被替代的收入，但Bits AI在財報上還看不出來（2026-09-08 CEO）；附著點長在公司自有的營運資料上屬強化，coding agent繞過平台做事後排查屬替代，分界年約2028年。衰退信號十類無一確認亮起，毛利率年比與股權激勵兩項列觀察。","governance":"最新一季FCF 2.787億美元、FCF率24.9%，但同季股權激勵2.203億美元，扣掉後的自由現金流約0.585億美元、占營收約5%；FCF高於非GAAP淨利，主要來自預收款與現金稅低（FY2026現金稅僅0.3–0.4億美元），不是營運特別省錢。現金去向：帳上現金與有價證券約50億美元（Q2 FY2026），資本支出加資本化軟體占營收4%–5%，2026上半年併購現金淨額0.985億美元，不配息、未見回購；近三年去向四分與債務結構事實表未涵蓋。評分三項：併購報酬：三筆合計1.915億美元，約占市值0.2%（251.49美元×約3.78億股≈950億美元），公司認定不重大，不適用；回購收益率：未見回購，不適用；股權激勵淨稀釋：管理層目標每年2.5%–3%（2026-02-12投資人日CFO），高於1.5%門檻，不過關。營運槓桿：Q2營業費用年增26%，低於營收年增36%，非GAAP營業利益率由20%升到23%，沒有壓縮。","valuation":"口徑用非GAAP Fwd P/E與PEG：GAAP盈餘被股權激勵吃掉（GAAP營業利益率0.5%），trailing P/E約503倍沒有意義。現價251.49美元＝FY2026共識EPS 2.53的99.4倍、FY2027 2.97的84.7倍；兩年EPS CAGR約21.7%，PEG約4.6，屬貴。P/S 22.8倍、EV/S 21.8倍，都在4個年度端點的最高位；連續五年分位事實表未涵蓋。反推：Base情境（FY2031E EPS 6.00、終端45倍）五年價值270美元，年化約1.4%；要年化10%需第五年405美元，等於EPS年增約22%且仍給60倍。賣方46位目標價均值285.28美元、中位數295美元、區間158–330美元（最高除以最低約2.1倍），現價低於均值約12%，方向上支持多頭，本裁決比共識悲觀；差異在框架：賣方沿用Q2的36%成長，我看Q3指引已降到28%–29%、FY2027營收共識年增22.5%，這個成長率配不上近百倍。最大客戶減量的利空已進入指引與賣方模型：FY2026 EPS共識2.53落在指引2.50–2.54之間，近3個月還上修4.55%。","premortem":"價值陷阱風險低：十類衰退信號無一確認亮起，留存、毛利、FCF都穩。三個方向的反證見反證紀錄：論點失敗的故事是AI原生客群退潮加上最大客戶自建，重演2021–2023年優化期；論點成功但股東經濟變差的故事是營收照長、每股盈餘被股權激勵與自建模型的GPU支出稀釋；價格已反映太多的故事是26週漲104%後倍數近百。最大回撤範圍−45%至−70%：起點FY1 Fwd P/E 99.4倍，一次下修指引倍數腰斬到55倍（2.53×55≈139美元，約−45%），成長熄火到10%上下倍數壓到30倍（2.53×30≈76美元，約−70%）；Q2財報揭露最大客戶減量後股價曾跌14.9%，單一事件就能打出雙位數跌幅。論點本身完整，深回撤是價格風險，持有者要有心理準備，不因波動本身砍倉。"},"plain":{"six":{"how_it_makes_money":"賺企業維運雲端與AI系統的錢：年度承諾額打底、超用按量計費；錢卡在「工程師天天用、財務長年年想砍帳單」這一節點，工程端黏著決定續約，財務端的用量優化決定成長斜率。","moat":"護城河方向穩定：執行面擴大、定價面小幅讓利，兩者相抵；機制是整合平台與共用承諾額度池，不是資料收集。","growth":"五年後仍有寬跑道：市占13%–14%、目標客戶滲透7%，資安（ARR逾1億美元）與AI觀測兩條第二曲線已出現；成長以用量與交叉銷售為主。","capital":"資本配置偏弱：現金流厚，但股權激勵每年淨稀釋2.5%–3%，沒有回購抵銷；併購小而分散，報酬無從量測。","valuation":"現價要求五年EPS年增約22%、且第五年市場仍給60倍，才換得年化10%；這接近本輪樂觀情境，我不信。","how_wrong":"最可能看錯的是價格而不是生意：現價已隱含接近樂觀情境；生意面最大的看錯點是AI原生客群與最大客戶的用量波動。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場沿用Q2的36%成長並給近百倍FY1非GAAP盈餘；但Q3指引已降到28%–29%、FY2027營收共識年增22.5%，且非GAAP盈餘排除了占營收19.6%的股權激勵，這個成長率配不上現價倍數","momentum_overheated":false,"cycle_gates_pass":null,"trap":"🟢","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":251.49,"week26_return_pct":103.98,"consensus_rev_3m_pct":4.55,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"非GAAP EPS排除占營收19.6%的股權激勵，若以GAAP計倍數更高；分母口徑不影響偏貴的結論"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 FY2026財報與Q4指引","impact":"高","watch":"營收是否超出指引上緣11.45億美元3%以上；非AI營收年增是否維持20%後段；是否再提最大客戶減量"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026年報與FY2027全年指引","impact":"高","watch":"FY2027營收指引年增是否≥20%；年報是否揭露單一客戶占營收10%以上"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"Bits AI改為AI credits計價的後續說明","impact":"中","watch":"AI credits是否開始在營收或ARR揭露中看得到"}],"_projected_from":"v19"}
```
