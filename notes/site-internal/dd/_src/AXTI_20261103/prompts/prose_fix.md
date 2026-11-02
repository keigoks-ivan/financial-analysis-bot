你是 stock-analyst v20 的**散文層（prose）agent**，標的 AXTI（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：AXTI　日期：2026-11-03　archetype：None　前份裁決：2026-05-24　B（觀望·thesis 真實但價格徹底透支｜InP 供需週期上行 + AXT 36% 市佔 + 產能 2026/27 各 doubling，但 FY27E EPS $0.75 對應 FwdPE 187x ＋ P/S 95x，5Y Base 目標價 $90-110 vs 現價 $140，等回測 $70-90 或 BB 中軌後再評估）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1896B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（801B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（995B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（763B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1369B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（544B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（731B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2199B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3344B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2252B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1896           3573-5104      5 條（2–6 內）  
s3                  8000         801           5039-7199      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3127          8311-11873      5 條（2–6 內）  
s6                 11000         544          7319-10456      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         731           1938-2769      5 條（2–6 內）  
s10                 5000        2199           1961-2801      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2252           2000-2748      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4733B；至少需散文≈40.27KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−710
−80%
−80
−73%
−62.9%
−60
−60%
−58.1%
−50.6%
−50.59
−46%
−20.1%
−15.6%
−12
−12%
−8%
−8
−6.4%
−3.96
−2.6%
−0.9%
−0.49
0
0.03
0.13%
0.30
0.49
0.56
0.58
0.6
0.64
0.7
0.75
0.8
0.87
0.88
0.9
1
1.0
1.04
1.14
1.17
1.2
1.42
1.5%
1.5
1.6
1.7
1.83
1.89
1.9
02
2
2.23
2.3
2.4
2.5
2.6
2.7
2.75
2.8
2.84
2.85
2.9
2.94
03
3.0
3
3.29
3.6
3.8%
04
4
4.2
4.2%
05
5
5%
5.13
5.45
5.5
5.6
6
06
6.2
6.32
6.85
7
07
7.1
08
8
8.26
9
9.45
9.5
10
10%
11
11.4
12
12%
12.7%
13%
14
15
15%
15.9
16
17
17%
17.5
17.6%
17.8
18%
18
19
20
20%
20.1
21%
22
22.3%
23
23.5
24
25
25%
26
27
28
29
29.8%
30
30%
31
32.2%
34.3
34.4
35
35%
36.2%
36.9%
37%
37.5%
38.7%
40
40%
40.2%
40.3
42
44.9%
45%
45
46
48
49
50%
51%
52
52.31
54%
55
55%
56%
56.0%
57
60%
60
60.1
60.2
62.9%
63%
67.7%
$70
70%
70
70.8
73.4%
74%
76%
80
90
92
94.5%
95
100
100%
110
116%
125
136.4
140.83
150%
150
156%
162%
187
190%
200
232
300
301
340
440
500
800
880
910
970
2019
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
20261103
1,000
1,200
1,660
1,700
2,126
2,140
2,230
2,540
2,570
2,580
3,070
3,350
4,110
4,340
4,350
5,430
6,000
6,557
6,600
7,000
7,100
7,340
7,700
9,000
9,120
−1,790
−1,880
−3,720
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
{"meta":{"ticker":"AXTI","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"AXT, Inc."},"oneliner":"InP 基板缺貨讓 AXT 單季營收一年成長 162%、毛利率升到 56%，但產能全在中國、對手 2028 年後擴產落地；現價約 23 倍 FY2027 共識 EPS，等於把高峰毛利率當常態，等 35 美元以下且毛利率守住再進場","thesis":{"H":[{"id":"H1","text":"InP 缺貨延續到 2027 年底：AXT 擴出的產能全數賣掉、報價不降","2y":"Q4 2027 InP 季營收 ≥1.2 億美元（約 Q4 2026 預估 7,100 萬的 1.7 倍；公司目標 2027 年產能再翻倍）","5y":null,"10y":null,"threshold":"GAAP 毛利率連續 4 季 ≥55%；InP 季營收逐季成長；積壓訂單維持 ≥5 億美元","source":"每季 8-K 業績新聞稿與法說會（CFO 毛利率說明、BD 副總積壓訂單與產能數字）；TrendForce InP 報價","drift_rule":"2 年期：InP 營收或毛利率連 2 季偏離門檻 ≥5% 為削弱、連 3 季 ≥10% 為反轉"},{"id":"H2","text":"2028–2030 競爭產能落地後，AXT 憑 4／6 吋低 EPD 製程守住高端份額，年度毛利率不跌回自身歷史區間","2y":null,"5y":"FY2029–FY2030 年度 GAAP 毛利率 ≥40%（自身年度高點為 2022 年 36.9%）；6 吋占 InP 營收比重逐年上升","10y":null,"threshold":"年度毛利率 ≥40%；InP 營收不連 2 季年減","source":"10-K、每季法說；JX、Sumitomo 擴產公告；TrendForce 中國新案投產進度","drift_rule":"5 年期：連 4 季偏離門檻 ≥5% 為削弱、連 6 季 ≥10% 為反轉"},{"id":"H3","text":"中國製造加出口許可的架構不中斷，擴產融資也不讓 AXTI 股東分到的獲利縮水","2y":"輸美 InP 許可在 2027 年中前核發；Tongmei 融資交割後 AXT 持股 ≥73.4%；香港上市前無母公司層級增資","5y":null,"10y":null,"threshold":"每季實際營收 ≥ 當季已有許可營收；AXT 對 Tongmei 持股 ≥73.4%","source":"8-K、10-Q 出口許可段落、商務部公告；2026-10-27 Tongmei 融資協議 8-K","drift_rule":"2 年期：連 2 季實際營收低於已有許可營收 ≥5% 為削弱、連 3 季 ≥10% 為反轉；持股跌破 70% 直接視為反轉"}],"R":[{"id":"R1","text":"中國收緊 InP 出口許可或擴及原料：所有基板在中國生產，非中國出貨要許可，10-K 自稱出口許可是目前最大挑戰；春季時輸美 InP 許可仍在最後審查、輸美 GaAs 許可未獲批，Q2 10-Q 稱仍有未取得許可的積壓訂單、無法預測審批時點；許可時程不在公司控制內，需求強時也會出現階段性供給衝擊","h_ref":"H3","clock":"⚡","threshold":"單季實際營收低於已有許可營收 10% 以上，或商務部宣布暫停／收緊 InP 出口","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","regulatory_antitrust#2","supply_demand_durability#4"]},{"id":"R2","text":"供給追上後報價反轉：JX 至多 10 倍、Sumitomo 3 倍、浙江新案年產 300 萬片 InP（2029-08 完工）、雲南鍺業與 Vital 擴產，加上 AXT 自身 2027 年底約為 2025 年底 5.5–6 倍；10-K 自承競爭已壓價，中國鎵供應商曾為搶市占降價；2019、2023 兩次下行年度毛利率分別由 36.2% 到 29.8%、由 36.9% 到 17.6%，2019 Q4 單季約 21%，2025 Q1 為 -6.4%","h_ref":"H2","clock":"🔥","threshold":"GAAP 毛利率連 2 季季減各 ≥3 個百分點，或 InP 報價首次調降","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","competitive_share_entrants#3","competitive_share_entrants#4","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","supply_demand_durability#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#4"]},{"id":"R3","text":"AI 光通訊需求降速或訂單取消：積壓訂單以現貨單與 12 個月內短約為主，客戶無最低採購義務、過去曾大量推遲與取消；Q3 首度有單一客戶占營收逾 10%，應收帳款也有一家逾 10% 且不收擔保品；2023 年北美營收曾因 InP 與 GaAs 需求下滑年減 67.7%。前份的超大型雲端資本支出門檻保留為觀察項","h_ref":"H1","clock":"⚡","threshold":"積壓訂單跌破 3 億美元，或揭露大額取消／推遲；觀察項：超大型雲端資本支出年增 <15% 連 2 季（事實表未涵蓋，資料缺口）","evidence_refs":["customer_concentration_credit#3","customer_concentration_credit#2","cyclical_prior_downcycle_behavior#3"]},{"id":"R4","text":"股東經濟外流與訴訟：Tongmei 讓股後 AXT 持股最多降約 12 個百分點到 73.4%，香港上市可能再稀釋；2024-05 起的股東集體訴訟（證券法 10b-5）駁回動議仍待裁定，求償金額未載明","h_ref":"H3","clock":"🐢","threshold":"AXT 對 Tongmei 持股 <70%，或駁回動議被否決","evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"id":"R5","text":"替代技術與差異化流失：Fraunhofer ISE 的 InP-on-GaAs（至 150mm）定位為取代 prime InP 的低成本方案；10-K 自承對手以類似長晶技術生產的基板愈來愈多、已侵蝕差異化","h_ref":"H2","clock":"🐢","threshold":"主要雷射或光偵測器客戶公告以 InP-on-GaAs 量產，或 AXT 4 吋以上出貨占比連 2 季停滯","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"single_thing":{"description":"InP 基板報價首次調降（AXT 法說揭露降價，或產業 2 吋報價較 2026-06 的 880 人民幣高點回落）","why_fatal":"本檔獲利對毛利率最敏感：以 FY2031 Base 營收約 7 億美元計，毛利率每變動 10 個百分點，稅前獲利變動約 7,000 萬，扣稅與少數股權（AXT 持有 Tongmei 約 73.4%）後約 0.6–0.9 美元，占 Base 終端 EPS 2.7 的兩到三成。報價首降代表競爭產能已追上，2019、2023 兩次下行毛利率都在一年內大跌","if_happens":"改走 Bear 路徑（FY2029 EPS 降到 1 美元以下）；已持有清倉，未持有撤回進場條件，等毛利率落底再重跑判斷","how_monitor":"每季法說的報價與毛利率說明；TrendForce、經濟日報轉述的 InP 報價；毛利率連 2 季各降 ≥3 個百分點視同發生","probability":"12–24 個月內約 30%（缺貨預期延續到 2027 年後，但競爭產能 2028 年起投產）"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.5,"peg_fy2":0.49,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-0.49,"FY2026E":0.87,"FY2027E":2.23,"FY2028E":3.29},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；FY2025A 的 -0.49 取自年報，FY2026E–FY2028E 為 Koyfin 2026-10-31 快照共識（口徑未標明 GAAP 或非 GAAP；Chartmill 同期 FY2026 共識 0.88、7 位分析師），FY2026E 的 0.87 早於 Q3 財報，偏舊偏低"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"近四個年度有三年 GAAP 虧損（2023–2025），年度毛利率高低差 24 個百分點（2022 年 36.9%、2025 年 12.7%），當前獲利由報價與產能利用率推動；同時疊加 AI 光通訊的長期需求，這一輪循環幅度可能大於過去"},"industry":{"clock_phase":"II","sd_verdict_source":"2027 年前結構性、2028 年後週期性將反轉：缺口依據為 TrendForce（2026-08，認證 12–18 個月、失衡延續到 2027 年後）、報價三度調漲（經濟日報轉述，2026-08）與 Q3 法說客戶全面配額；反轉依據為 JX 至多 10 倍（TrendForce 2026-06）、Sumitomo 目標 FY2028 為 FY2024 的 3 倍、浙江新案年產 300 萬片 InP（2029-08 完工），以及 2027 年缺口估計分歧（有分析師稱紙面產能約為需求兩倍）","bargaining":{"up":"上游為銦、鎵等原料；AXT 持有中國原料合資股權、子公司晶美已精煉高純銦，原料面掌控力偏強，但 CEO 稱原料價格大漲、會吃掉部分毛利","down":"目前對客戶議價權強：客戶配額、預付款鎖量、報價可調；前五大客戶 35%、一家逾 10%，集中度不高。客戶通常維持至少兩家合格供應商（10-K），供給追上後議價權回到客戶","geo":"所有基板在中國製造，InP 自 2025-02-04 起需商務部出口許可；美國對中國晶圓基板關稅曾升至 70%，IEEPA 部分 2026-02 被最高法院推翻但 232、301 仍有效；中國境內出貨免許可，Q2 中國占營收逾 50%"},"profit_pool_dir":"利潤池目前往基板環節集中（缺貨定價、預付款），2028 年後隨供給追上可能回流到雷射與光模組廠","tam_table":[{"item":"InP 基板市場成長","value":"Yole 預估至 2031 年 CAGR 逾 18%，動能為 AI 資料中心、高速光模組與 CPO（次級來源轉述，低信心）"},{"item":"管理層對市場的說法","value":"未來 3–5 年基板市場擴大 4–6 倍（次級來源轉述）；Q3 法說 CEO 轉述大客戶由 20 倍改口 1,000 倍，屬客戶說法且無推導，不採為依據"},{"item":"AXT InP 季營收","value":"Q2 2026 3,070 萬 → Q3 5,430 萬 → Q4 預估約 7,100 萬美元"},{"item":"AXT InP 產能","value":"2026 年底約為 2025 年底的 2.75–3 倍，2027 年目標再翻倍"},{"item":"TAM 絕對金額、滲透率、各環節營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"低 EPD 長晶製程 know-how＋4／6 吋大尺寸良率學習曲線，加上下游 12–18 個月認證造成的轉換摩擦；屬製程技術型優勢，不是網路效應或法定獨占","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：2026 年 8 月提前達成 InP 產能翻倍、年底約 2025 年底的 2.75–3 倍，6 吋轉入試產、新長晶爐提升產出（Q3 法說）。定價面現階段擴大（報價自 2025Q4 起三度調漲、GAAP 毛利率由去年同期 22.3% 升到 56.0%），但屬供需缺口帶來的週期性定價；10-K 自承對手以類似長晶技術已侵蝕差異化，JX 計畫 InP 產能至多 10 倍、Sumitomo 3 倍、中國多個新案 2029 年前投產。兩者相抵判穩定，不給擴大","peer_na_reason":"同業 ROIC 與倍數事實表未涵蓋；SOI.PA、IQE.L 無財報資料；Sumitomo、JX 為綜合集團，InP 部門數字不單獨揭露","threats":[{"level":"🟡","text":"JX Advanced Metals 至 FY2030 投資至多 1,200 億日圓、InP 產能至多 10 倍；Sumitomo 目標 FY2028 產出為 FY2024 的 3 倍；Lumentum 美國 6 吋 InP 廠 2028 年中量產（事實表未說明是基板或元件）。同技術路線的點對點競爭，但資本量級足以在 2028 年後壓價","p":"40%","evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#2","supply_demand_durability#2"]},{"level":"🟡","text":"中國新進者：雲南鍺業擴到年產 45 萬片、Vital Materials 擴產、浙江新案規劃年產 300 萬片 InP；中國鎵供應商已為搶市占降價，使 AXT 合資企業權益收益由 340 萬降到 80 萬美元，是中國廠進場就打價格戰的前例","p":"35%","evidence_refs":["competitive_share_entrants#4","cyclical_supply_discipline_capacity#3","competitive_share_entrants#2"]},{"level":"🟡","text":"10-K 自承競爭強度過去幾年增加且將持續、已造成降價，對手以類似長晶技術生產的基板愈來愈多、侵蝕技術差異化","p":"30%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"替代技術：Fraunhofer ISE 開發 InP-on-GaAs（至 150mm），定位為取代 prime InP 的低成本方案；仍在研發階段，且 AXT 也是 6／8 吋 GaAs 龍頭，替代發生時可部分轉回自家產品","p":"10%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉（暫定：Q3 GAAP 營益率 38.7%，存貨約 1.04 億美元相對年化營收約 2.94 億；廠房設備事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是超大型雲端業者，決策者是光模組與雷射廠，付款者是基板採購方，三角色都成立：800G／1.6T 與 200G 單通道光偵測器必須用 InP（Q2 法說 CEO），客戶以預付款搶量（Lumentum 4,350 萬、Casela 2,230 萬、Coherent 2,540 萬）。屬需要而非想要，延後購買代價是 AI 叢集無法出貨；但急迫性不等於持久性，需求高度依賴 AI 資本支出"},{"item":"決策層級","level":"🟡","text":"替代性要在客戶的認證層級衡量：新基板通過下游認證需 12–18 個月，高功率雷射要求更低 EPD、合格供應商更少，有轉換摩擦；但 10-K 指出客戶通常維持至少兩家合格供應商，且 AXT 刻意少簽長約，供給充足後客戶換供應商的成本不高"},{"item":"價值鏈分配","level":"🟡","text":"基板只占光模組價值的一小段，目前因缺貨多拿（報價三度調漲、2 吋報價由 500 升到 880 人民幣），但下游客戶規模大、正以長約與預付款鎖量，Sumitomo 有自家光元件需求；供給追上後利潤會回流到元件與模組端"},{"item":"社會容忍度","level":"🔴","text":"價格天花板主要來自政策而非客戶：所有產能在中國，非中國出貨要商務部許可，InP 自 2025-02-04 列管、輸美許可春季時仍在最後審查，10-K 自稱出口許可是目前最大挑戰且無法保證不再加碼；美國 232、301 關稅仍有效。這是依賴政府授權的經營條件，已列入反證紀錄"}],"roiic":"前瞻約 12%–17%（稅前、以現行報價計）；2026 年的歷史增量報酬極高，但主要來自舊產能擠出與漲價，不可外推","reinvest_rate":"超過 100%（Tongmei 擴產資金 6.85–9.45 億美元，對比 Base 情境 FY2027–28 累計歸屬淨利約 3.6 億美元，差額靠外部股權）","endo_ceiling":15,"formula_note":"增量稅前營業利益：InP 季營收由 Q4 2026 約 7,100 萬翻倍到約 1.42 億，年增約 2.84 億 × 營益率 40% ≈ 1.14 億；除以擴產資金 6.85–9.45 億（AXT 增資 4 億＋外部 2.85–5.45 億）≈ 12%–17%。內生成長上界＝增量報酬 × 再投資率（以 100% 封頂，超出部分是外部融資、會稀釋 AXTI 股東）≈ 15%／年。稅率與廠房設備事實表未涵蓋；若毛利率回到 30% 左右，增量報酬降到個位數"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","AXTI":32.18,"SOI.PA":null,"IQE.L":null,"COHR":37.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","AXTI":4.18,"SOI.PA":null,"IQE.L":null,"COHR":12.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","AXTI":-15.59,"SOI.PA":null,"IQE.L":null,"COHR":-14.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","AXTI":8.02,"SOI.PA":null,"IQE.L":null,"COHR":10.16,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"SOI.PA","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null},{"name":"IQE.L","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null},{"name":"COHR","gm":37.5,"om":12.67,"fcf_margin":-14.48,"rd_intensity":10.16,"period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"2026 年：量（InP 產能 2.75–3 倍）＋價（報價三度調漲）＋組合（3 吋轉 4 吋、低 EPD）；2027 年起以量為主（產能再翻倍），價格貢獻縮小；無併購、無回購","runway_years":"事實表未涵蓋滲透率；以需求面估約 5–9 年（Yole 至 2031 年 CAGR 逾 18%，次級來源）","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段的報酬持續期推導：前瞻增量報酬約 12%–17%（稅前、現行報價）× 再投資率以 100% 封頂 ≈ 15%／年；超出部分靠外部募資與 Tongmei 股權，會稀釋 AXTI 股東","segments":[{"item":"InP","value":"Q3 5,430 萬美元（74%），資料中心為主；Q4 增量全數為 InP，預估約 7,100 萬"},{"item":"GaAs","value":"910 萬（12%）；Q4 部分應用季節性走弱，6／8 吋 VCSEL 用於資料中心為潛在新用途"},{"item":"原料（合併子公司）","value":"970 萬（13%）"},{"item":"Ge","value":"34.4 萬"},{"item":"分部毛利率","value":"事實表未涵蓋；管理層稱 InP 毛利高於 GaAs 與原料"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"毛利率逐季上升"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"無第三方份額數據，事實表未涵蓋"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"三度調漲後仍配額"},{"item":"EPS CAGR 顯著高於營收 CAGR","lit":true,"note":"FY2026E 到 FY2027E 的 EPS +156%、營收 +116%"},{"item":"FCF／淨利 <0.75 連 2 年","lit":true,"note":"FY2022–2025 FCF 每年為負，TTM 至 2026-06 FCF 利潤率 -15.6%"},{"item":"SBC／營收 >5% 且逐年上升","lit":false,"note":"Q3 約 1.5%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"InP-on-GaAs 仍在研發階段，列觀察"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"item":"維護性資本支出占 FCF >60%","lit":false,"note":"FCF 為負、資本支出事實表未涵蓋"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"正積極擴產"}],"trap_rating":"價值陷阱風險中等（亮 2 個）；長期成長性中等"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產能擴充與報價，不靠併購；無股息、無回購，資本回饋無可展開項目"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年無併購；Tongmei 增資屬子公司股權融資，不是收購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"無回購；公司處於募資擴產階段","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 股票酬勞 110 萬美元，年化約 440 萬，相對市值約 34.3 億約 0.13%／年，低於 1.5%；增資造成的稀釋另列在現金去向","grade":"過"}]},"valuation":{"basis":"FY2027E（FY2）本益比為主、FY2028E 為輔；FY1 的 0.87 早於 Q3 財報且含 Q1 低基期，只作情境樹起點","tier":"中型化合物半導體基板，同業倍數事實表未涵蓋","peers":{"expanded":false,"reason":"同業倍數事實表未涵蓋：SOI.PA、IQE.L 無財報資料，COHR 只有利潤率；Sumitomo Electric、JX 為綜合集團，InP 無獨立倍數。改以自身歷史端點與情境樹為錨"},"fwd_pe":60.2,"peg":0.64,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"FY1 Fwd PE 60.2 倍（分母 0.87 早於 Q3 財報、含 Q1 低基期，偏高估）；FY2 23.5 倍、FY3 15.9 倍；P/S 20.1 倍、EV/S 17.8 倍，高於自身全部 4 個年度端點（分位 100，只有 4 個年度點、不是真五年）；PEG 0.64（60.2 倍除以 FY2026E 到 FY2028E 兩年 CAGR 94.5%）看似便宜，但分母是高峰毛利率下的獲利，不採為便宜論證 → 偏貴","upside_short_pct":-8,"upside_mid_pct":-12},"trap_analysis":{"verdict":"🟡","label":"價值陷阱風險中等：亮 2 個衰退信號（EPS 成長遠快於營收、FCF 長期為負）"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"JX 至多 10 倍、Sumitomo 3 倍、浙江新案年產 300 萬片 InP、雲南鍺業擴到 45 萬片，AXT 自身 2027 年底約為 2025 年底 5.5–6 倍；有分析師稱紙面基板產能約為需求兩倍；過去兩次下行毛利率都在一年內大跌（2022 到 2023 由 36.9% 到 17.6%）","assumption":"AI 光通訊需求（Yole 至 2031 年 CAGR 逾 18%）吸收得了 2028–2030 的新產能","consequence":"InP 報價回落、毛利率回到 25%–35%，FY2029–2030 EPS 跌到 0.7–0.8 美元，FY2031 以 1.0 × 14 倍計約 14 美元，較現價 -73%","ruling":"採納：列為 Bear 30%，並設為唯一致命點（InP 報價首次調降），兩者是同一件事，不另改寫","watch":"InP 報價、季毛利率、JX／Sumitomo／浙江新案投產進度","evidence_refs":["cyclical_supply_discipline_capacity#3","competitive_share_entrants#3","competitive_share_entrants#4","cyclical_prior_downcycle_behavior#2","supply_demand_durability#2"],"fact_refs":["f_kpi6_gross_margin_gaap"]},{"view":"論點失敗","evidence":"所有基板在中國生產；InP 自 2025-02-04 納入出口管制，10-K 自稱出口許可是目前最大挑戰、無法保證不再加碼；春季說明書時輸美 InP 許可仍在最後審查、輸美 GaAs 許可未獲批；2025 Q1 因許可延遲毛利率 -6.4%","assumption":"中國持續核發許可，且中國境內 AI 光通訊需求（免許可）能填補缺口","consequence":"非中國營收（Q2 約四到五成）中斷 1–2 季，毛利率重演 2025 Q1，股價可能先跌五成以上","ruling":"採納：社會容忍度判紅燈，列為 R1 與清倉條件；機率不高但損失大，不作唯一致命點是因為中國境內出貨免許可、公司已在許可制度下營運近兩年","watch":"每季實際營收 vs 已有許可營收；商務部公告","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1","reg_tariff_export#2","cyclical_prior_downcycle_behavior#4"],"fact_refs":["f_kpi0_revenue_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年增資約 6.32 億美元，股數由約 4,340 萬升到 6,557 萬；Tongmei 對外募 2.85–5.45 億美元，AXT 持股最多降約 12 個百分點到 73.4%，並計畫香港上市；Q2 法說說擴產不需大量資本支出，Q3 卻安排近 9.5 億擴產資金","assumption":"擴產的增量報酬高於讓出的股權成本，且中國子公司的現金能回到母公司","consequence":"合併營收與獲利照計畫成長，但歸屬 AXTI 的 EPS 少一成以上，現金留在中國難以回饋股東","ruling":"採納：Base 的 FY2027 EPS 2.4 只略高於 Q4 2026 年化約 2.3，雖然產能要再翻倍，差額就是預留給少數股權外流與報價放緩；香港上市若再讓股，Base 再下修","watch":"Tongmei 融資最終金額與持股、香港上市條件、母公司層級現金","evidence_refs":["major_events#1","ma_merger#0"],"fact_refs":["f_shares_diluted_m","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"P/S 20.1 倍、EV/S 17.8 倍高於自身所有年度端點；First Principles 以賣出、目標 45 美元首評；B. Riley 中立 55 美元；StockAnalysis 均值 57 美元","assumption":"市場願意對高峰毛利率給 20 倍以上本益比","consequence":"即使 2027–2028 照共識，若市場提早用循環股倍數（10–14 倍）計價，股價可能落到 30–40 美元","ruling":"部分採納：股價已跌 63%，不算極端透支；但以 FY2027 23.5 倍計仍沒有安全邊際，這是本次觀望的主因","watch":"股價對 FY2028 共識 EPS 的倍數","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_ps_current","f_ps_percentile","f_ev_s_current"]}],"max_dd":{"lo":-80,"hi":-60,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 140.83 → 本次 52.31（-62.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=140.83","side_b":"本次 price_at_dd=52.31","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 140.83 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 140.83 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 140.83 美元：Bull 價 136.4、Bear 價 14，五年期望值 −58.1%，基準年化 −20.1%，不對稱比 0.03","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.03。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 140.83 美元：五年期望值 −58.1%，基準年化 −20.1%，不對稱比 0.03","side_b":"本次情境、股價 52.31 美元：五年期望值 +12.7%，基準年化 −2.6%，不對稱比 1.83","ruling":"再換股價、情境不動：起點價下跌 62.9%，五年期望值多 70.8 個百分點，基準年化多 17.5 個百分點，不對稱比由 0.03 升到 1.83。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份觀望後股價跌 63%，仍維持觀望","cause":"價格變動","prior_field":["signal"],"side_a":"前份（2026-05-24）：140.83 美元觀望，理由是 FY2027E EPS 0.75 對應 187 倍，等回測 70–90 美元","side_b":"本次：52.31 美元，已跌破前份等待區間；同期 FY2027 共識 EPS 升到 2.23，現價約 23.5 倍，但分母是高峰毛利率下的獲利","ruling":"結論不變、理由換了：前份是倍數過高，本次是獲利偏循環。股價跌破前份區間反映市場開始折價 2028 年後的供給潮，不算錯殺；Base 五年報酬約 -12%，沒有安全邊際","evidence_level":"中","settle_metric":"2027 年上半年毛利率與 InP 報價方向","if_then":["若股價 ≤35 美元且最近一季毛利率 ≥50%：分批反買首倉","若股價先漲回 70 美元以上而毛利率沒有再升：不追"],"evidence_refs":[]},{"axis":"估值由最貴一級降為偏貴，陷阱風險維持中等","cause":"新證據","prior_field":["val","trap"],"side_a":"前份：FY2027E EPS 0.75、Fwd PE 187 倍、P/S 95 倍，估值最貴一級；陷阱風險中等","side_b":"本次：Q3 營收 7,340 萬、GAAP 毛利率 56.0%、歸屬淨利 2,570 萬，Q4 指引 GAAP EPS 0.56–0.58；FY2027 共識 2.23（23.5 倍）、FY2028 3.29（15.9 倍）；P/S 20.1 倍仍高於自身所有年度端點；衰退信號亮 2 個","ruling":"估值降一級主要是獲利上修造成：若 EPS 仍是 0.75，現價也還有約 70 倍。沒降到合理，是因為分母建立在歷史從未見過的毛利率上。陷阱風險：新證據兩面都有（獲利轉正 vs FCF 仍為負、EPS 成長遠快於營收），維持中等","evidence_level":"高（公司 8-K 與法說）","settle_metric":"2027 年 FCF 是否轉正、毛利率能否守在 50% 以上","if_then":["若 2027 年上半年 FCF 轉正且毛利率 ≥55%：陷阱風險可降一級","若毛利率連 2 季各降 ≥3 個百分點：估值結論回到最貴一級並減碼"],"evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"axis":"新增結構化欄位：循環定位、護城河方向、成長跑道、情境機率與最大回撤","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位皆未填","side_b":"本次：歸類循環/商品、中循環、護城河方向穩定、Y5 後跑道中等，情境機率 Bull 25／Base 45／Bear 30，最大回撤 -60%～-80%；裁決與倉位角色由程式依本次輸入重算","ruling":"屬框架補欄，不是看法翻轉。改用循環鏡頭的依據：近四年三年 GAAP 虧損、年度毛利率高低差 24 個百分點，Q3 單季毛利率已高出自身年度高點約 19 個百分點","evidence_level":"高","settle_metric":"不適用（方法變動）","if_then":[],"evidence_refs":[]},{"axis":"重新進場條件改寫（分批反買首倉）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設結構化條件；結論文字為「等回測 $70-90 或 BB 中軌後再評估」","side_b":"股價 ≤35 美元（約 FY2028 共識 EPS 的 11 倍）且最近一季 GAAP 毛利率仍 ≥50%，才分批反買首倉","ruling":"前份區間已被跌破，且當時用的 EPS 分母（0.75）已失效；新條件綁本次觀望的唯一約束：價格沒有反映跨週期獲利，再加毛利率底線，避免在供給潮開始時接刀","evidence_level":"中","settle_metric":"股價、季毛利率","if_then":["價格先到、毛利率 ≥50%：分批反買首倉","價格先到、毛利率 <50%：不追，等毛利率止跌"],"evidence_refs":[]},{"axis":"出場門檻新設（減碼／清倉）","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設出場門檻","side_b":"毛利率連 2 季季減合計 ≥6 個百分點或單季 <45%：減碼；單季實際營收低於已有許可營收 10% 以上或商務部暫停 InP 出口：清倉；積壓訂單跌破 3 億美元：減碼；2 吋 InP 報價較 880 人民幣高點回落 ≥20%：減碼；AXT 對 Tongmei 持股 <70%：停止加碼","ruling":"本次才有可量化的獲利錨（56% 毛利率、逾 5 億積壓訂單、已有許可營收指引）與 Tongmei 讓股數字，前份沒有這些數字可設門檻","evidence_level":"高","settle_metric":"每季財報","if_then":["任一減碼門檻觸發：減碼一半並重跑判斷","清倉門檻觸發：清倉"],"evidence_refs":["reg_tariff_export#2","geo_supply_chain#1"]},{"axis":"Single Thing 新設：InP 報價首次調降","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"InP 基板報價首次調降（AXT 法說揭露降價，或 2 吋報價較 2026-06 的 880 人民幣高點回落）","ruling":"依數學敏感度選：終端 EPS 對毛利率最敏感，毛利率每 10 個百分點約影響 Base 終端 EPS 兩到三成；報價首降是供給追上的離散訊號。出口許可中斷更戲劇性，但中國境內出貨免許可、公司已在許可制度下營運近兩年，列為風險與清倉條件","evidence_level":"中","settle_metric":"InP 報價、季毛利率","if_then":["若發生：已持有清倉，未持有撤回進場條件","若 2027 年底前未發生且毛利率 ≥55%：維持進場條件"],"evidence_refs":["cyclical_supply_discipline_capacity#3","competitive_share_entrants#3"]},{"axis":"2027 年後 InP 會不會過剩（方向相反，已依時間窗裁決）","cause":"新證據","prior_field":null,"side_a":"管理層（2026-10-29 Q3 法說，Bettles／Young／Fischer）：所有客戶都在配額，2027 年翻倍仍不夠，2027–2028 不擔心過剩，2029 才需要再看","side_b":"供給面：JX 至多 10 倍、Sumitomo 3 倍、浙江新案年產 300 萬片 InP 2029 年完工；有分析師稱紙面基板產能約為需求兩倍；AXT 自身 2027 年底約為 2025 年底 5.5–6 倍","ruling":"⚖ 到 2027 年底選管理層一側（依據：報價三度調漲、正考慮第四次漲逾 10%、交期拉長到 9 個月以上、認證期 12–18 個月）；2028 年起選供給側（依據：競爭產能投產時程集中在 2028–2030，2019 與 2023 兩次下行毛利率都大跌）。決勝數據＝InP 報價方向與毛利率季變化","evidence_level":"中（供給數字多為新聞與搜尋摘要轉述）","settle_metric":"2 吋 InP 報價（880 人民幣高點）與 AXT 毛利率季變化","if_then":["若 2027 年任一時點毛利率連 2 季各降 ≥3 個百分點：減碼至零並撤回進場條件","反向：若 2027 年 Q4 毛利率仍 ≥60% 且積壓訂單 ≥5 億美元：解除觀望，首倉以 FY2028 共識 EPS 14 倍（約 46 美元）為價格上限"],"evidence_refs":["supply_demand_durability#2","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#3","competitive_share_entrants#4"]},{"axis":"管理層對擴產資本需求的說法前後不一","cause":"新證據","prior_field":null,"side_a":"2026-07-30 Q2 法說 BD 副總 Bettles：擴產不需要大量額外資本支出，先前計畫不變","side_b":"2026-10-27 協議與 10-29 Q3 法說 CFO Fischer：Tongmei 對外募 2.85–5.45 億美元，AXT 另以 4 億美元增資 Tongmei，資金用於 InP 與原料擴產，AXT 持股降約 12 個百分點","ruling":"採後者為資本強度的真實訊號：擴產不再只是用舊廠擠產能，增量報酬會低於 2026 年；募資也可能是為香港上市鋪路，暫不判定為浪費，但增量報酬估計下修到 12%–17%（稅前、現行報價）","evidence_level":"高（8-K）","settle_metric":"2027 年資本支出揭露與 Tongmei 融資最終金額","if_then":["若 2027 年資本支出超過 5 億美元而 InP 產能未達再翻倍：增量報酬再下修並維持觀望","若融資取最低額 2.85 億且產能仍翻倍：增量報酬上修"],"evidence_refs":["major_events#1","ma_merger#0"]},{"axis":"積壓訂單五倍成長的品質","cause":"新證據","prior_field":null,"side_a":"Q3 法說：積壓訂單由逾 1 億升到逾 5 億美元，交期 9 個月以上","side_b":"同場 Bettles 與 Fischer：長約占比小、主要是現貨單與 12 個月內短約，公司刻意不簽長約以保留漲價空間；Q2 法說 CFO 稱已不接超出規劃產能的訂單，口徑已變；10-K：客戶可減少、延後或取消訂單；Q3 前五大客戶由 30% 升到 35%、首度有一家逾 10%","ruling":"可調和（程度差異）：需求強是真的，但 5 億美元有一部分來自接單政策放寬，取消風險高於長約；不把積壓訂單當鎖定營收","evidence_level":"中","settle_metric":"積壓訂單金額與取消揭露","if_then":["若積壓訂單跌破 3 億美元或揭露大額取消：減碼","若 2027 年中積壓訂單仍 ≥5 億且長約占比上升：成長能見度上修"],"evidence_refs":["customer_concentration_credit#3","customer_concentration_credit#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：FY2028 共識 EPS 3.29 對應 15.9 倍；現金及投資 8.26 億美元（Q3 法說）扣總債務 1.17 億約 7.1 億、每股約 11 美元；Q4 毛利率可能到 6 字頭；管理層連續兩季財測保守後超標（Q3 指引 6,600 萬、實際 7,340 萬）；股價半年腰斬","side_b":"觀望方：獲利建立在歷史從未見過的毛利率（過去年度高點 36.9%）上，2028–2030 競爭產能密集投產；Base 五年報酬約 -12%","ruling":"反駁買方但保留：買方論證成立的前提是 2028 年毛利率仍 ≥55%，現在沒有證據能裁決，最早要到 2027 年下半年才有決勝數據；在此之前只接受價格補償（35 美元以下）","evidence_level":"中","settle_metric":"2027 年下半年毛利率與 InP 報價","if_then":["若股價 ≤35 美元且毛利率 ≥50%：分批反買首倉","若毛利率未破而股價續漲：不追"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"前份假設與風險門檻改寫","cause":"新證據","prior_field":null,"side_a":"前份：H1 InP 季營收連 2 季 ≥1,700 萬；H2 JX 無擴產公告、Sumitomo 資本支出承諾 ≤5 億美元；H3 FY2027 EPS 共識 ≥0.75、Fwd PE 維持 80 倍以上、股價 80–150 美元；R1 超大型雲端資本支出年增 <15% 連 2 季；R2 毛利率連 2 季季減 3 個百分點加 Sumitomo 提前擴產；R3 商務部反轉加許可拒絕率 >30%","side_b":"本次：H1 改為 Q4 2027 InP 季營收 ≥1.2 億且毛利率連 4 季 ≥55%；H2 改為 FY2029–30 年度毛利率 ≥40%；H3 改為出口許可與 Tongmei 持股；R2 保留毛利率連 2 季季減 3 個百分點並改為減碼條件；R1 改為實際營收低於已有許可營收 10%；超大型雲端資本支出門檻保留為觀察項，本次事實表未涵蓋（資料缺口）","ruling":"前份 H1 已大幅超過（Q3 InP 5,430 萬）而退休、換高門檻；前份 H2 已被 JX 1,200 億日圓、至多 10 倍擴產打破，改測擴產落地後的毛利率；前份 H3 的倍數與股價區間已失效（股價 52 美元、Fwd PE 60 倍）而退休；許可拒絕率無公開數據，改用公司可觀測的已有許可營收","evidence_level":"高","settle_metric":"各新門檻","if_then":["新 H2 毛利率門檻連 4 季偏離 ≥5%：論點削弱、停止加碼","新 R1 觸發：清倉"],"evidence_refs":["competitive_share_entrants#3"]}],"triggers":[{"n":1,"text":"Q4 2026 財報驗證缺貨定價延續","type":"假設驗證","maps_to":"H1","metric":"Q4 營收、GAAP 毛利率、積壓訂單","threshold":"營收 ≥9,000 萬美元、毛利率 ≥56%、積壓訂單 ≥5 億美元","action":"不追（通過只代表論點仍成立，進場仍看價格條件）","source_freq":"每季 8-K 與法說","date":"2027-02","evidence_refs":[]},{"n":2,"text":"中國出口許可收緊或實際營收不及已有許可營收","type":"風險","maps_to":"R1","metric":"實際營收 vs 已有許可營收；商務部公告","threshold":"單季實際營收低於已有許可營收 10% 以上，或宣布暫停／收緊 InP 出口","action":"清倉","source_freq":"每季＋即時公告","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#1","supply_demand_durability#4"]},{"n":3,"text":"毛利率見頂回落","type":"減碼","maps_to":"R2","metric":"GAAP 毛利率季變化","threshold":"連 2 季季減各 ≥3 個百分點，或單季 <45%","action":"減碼","source_freq":"每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#0"]},{"n":4,"text":"InP 報價首次調降","type":"Single Thing","maps_to":"Single Thing","metric":"InP 基板報價","threshold":"AXT 法說揭露降價，或 2 吋報價較 880 人民幣高點回落","action":"清倉；未持有則撤回進場條件","source_freq":"每季法說＋產業報價","date":null,"evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#3"]},{"n":5,"text":"價格到位且毛利率未破","type":"估值rearm","maps_to":"H1","metric":"股價；最近一季 GAAP 毛利率","threshold":"股價 ≤35 美元且毛利率 ≥50%","action":"分批反買首倉","source_freq":"每日股價＋每季財報","date":null,"evidence_refs":[]},{"n":6,"text":"積壓訂單縮水或取消","type":"風險","maps_to":"R3","metric":"積壓訂單金額、取消或推遲揭露","threshold":"跌破 3 億美元，或揭露大額取消／推遲","action":"減碼","source_freq":"每季法說","date":null,"evidence_refs":["customer_concentration_credit#3","customer_concentration_credit#2"]},{"n":7,"text":"競爭產能提前投產","type":"風險","maps_to":"R2","metric":"JX、Sumitomo、浙江新案投產時程","threshold":"任一家宣布 InP 新產能提前到 2027 年內投產","action":"停止加碼","source_freq":"公司公告、TrendForce","date":null,"evidence_refs":["competitive_share_entrants#4","cyclical_supply_discipline_capacity#2"]},{"n":8,"text":"股東經濟外流或訴訟不利","type":"風險","maps_to":"R4","metric":"AXT 對 Tongmei 持股；集體訴訟進度","threshold":"持股 <70%，或駁回動議被否決","action":"停止加碼","source_freq":"8-K、10-Q","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":9,"text":"Q4 財報與 2027 年財測公布後全面複審","type":"複審日期","maps_to":null,"metric":"全部假設與門檻","threshold":"財報公布","action":"重跑判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"GAAP 毛利率","bear_threshold":"連 2 季季減合計 ≥6 個百分點，或單季 <45%","window":"每季，2027–2028","source":"公司 8-K 業績新聞稿","last_status":"ok"},{"metric":"實際營收 vs 已有許可營收；商務部 InP 出口管制","bear_threshold":"單季實際營收低於已有許可營收 10% 以上，或宣布暫停／收緊","window":"每季＋即時","source":"8-K、法說會、商務部公告","last_status":"ok"},{"metric":"積壓訂單","bear_threshold":"由逾 5 億美元跌破 3 億美元，或揭露大額取消／推遲","window":"每季法說","source":"法說會逐字稿","last_status":"ok"},{"metric":"2 吋 InP 基板報價","bear_threshold":"較 2026-06 高點 880 人民幣回落 ≥20%","window":"每季","source":"TrendForce、經濟日報轉述報價","last_status":"unknown"},{"metric":"AXT 對 Tongmei 持股","bear_threshold":"<70%（本次最大額融資後為 73.4%）","window":"至香港上市完成","source":"8-K、10-Q","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=-50.59, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價≤35美元（約FY2028共識EPS的11倍）且最近一季GAAP毛利率仍≥50%，才分批反買首倉","exec_line":"觀望不追。進場只在股價 ≤35 美元且最近一季毛利率 ≥50% 時分批反買首倉；毛利率連 2 季各降 ≥3 個百分點、InP 報價首次調降或出口許可中斷，即撤回進場條件；已持有者依同一組門檻減碼或清倉"},"reasoning":{"industry":"Q3 2026（季末 9-30）營收 7,340 萬美元，季增 54%、年增 162%；分部（2026-10-29 Q3 法說，CFO Fischer）：InP 5,430 萬（74%，以資料中心為主）、GaAs 910 萬（12%）、合併原料子公司 970 萬（13%）、Ge 34.4 萬。GAAP 毛利率 56.0%（Q2 44.9%、去年同期 22.3%），GAAP 營益率 38.7%，非 GAAP 40.2%，歸屬淨利 2,570 萬。增量毛利率約 76%（毛利由約 2,140 萬升到 4,110 萬，除以營收增量 2,580 萬），管理層拆解為量、InP 組合、報價上漲與 3 吋轉 4 吋。管理層兌現度高：Q2 法說給的 Q3 已有許可營收 6,600 萬，實際 7,340 萬；Q2 說 2026 年底 InP 季產能約 6,000 萬，Q4 InP 預估已約 7,100 萬（Q3 的 5,430 萬加上 Q4 指引增量 1,660 萬，BD 副總稱增量全是 InP）；Q2 說毛利率以 5 開頭為目標，Q3 已到 56%。產業時鐘判擴張期：需求仍大於供給、所有客戶都在配額、交期拉長到 9 個月以上、報價自 2025Q4 起三度調漲，供給方正在擴產但尚未落地。供需持久性：2027 年前偏結構性（下游新基板認證 12–18 個月、低 EPD 4 吋以上供給少），2028 年後轉為週期性、供給可逆性高（JX、Sumitomo、中國新案與 AXT 自身擴產集中在 2027–2030 投產）。單點依賴：三處廠區與所有基板都在中國，非中國出貨要商務部許可；客戶面前五大占 35%、首度有一家超過 10%（Q2 時為 30%、無一家超過 10%），集中度上升但仍分散。","moat":"機制：低 EPD（差排密度）長晶 know-how、4／6 吋大尺寸良率學習曲線，加上下游 12–18 個月的認證週期。執行面給 7 分：2026 年 8 月提前達成 InP 產能翻倍、年底約 2.75–3 倍，6 吋轉入試產，新設計長晶爐提升生產力；管理層稱 6 吋除 AXT 外只有一家同級對手、第三家遠落後（Q3 法說 CEO Young），屬公司自述。定價面給 5 分：當下議價力強（報價三度調漲、預付款），但過去年度毛利率在 12.7%–36.9% 擺盪，2019、2023 兩次下行都被動降價，10-K 自承競爭加劇已壓低價格、對手用類似長晶技術已侵蝕差異化。同業對照：TTM 至 2026-06 AXT 毛利率 32.2%、營益率 4.2%，低於 Coherent 的 37.5%、12.7%；但 AXT Q3 單季毛利率已到 56%，TTM 還沒反映這一輪；同業 ROIC 事實表未涵蓋，無法算報酬差距。方向判穩定：執行面擴大、定價面在下一個週期大概率縮減，兩者相抵；沒有客戶份額下滑的證據，也沒有份額上升的第三方數據。當期 ROIC 無法完整計算：營益率可得、稅率與廠房設備未涵蓋，周轉率只能用存貨約 1.04 億美元對年化營收約 2.94 億粗估，屬低周轉。四檢查點與增量報酬見報酬持續期欄。","growth":"成長組成：2026 年是量（InP 產能 2.75–3 倍）＋價（報價三度調漲）＋組合（3 吋轉 4 吋、低 EPD）；2027 年以量為主（產能再翻倍），報價大致不變；無併購、無回購。共識：FY2026E 0.87、FY2027E 2.23、FY2028E 3.29（Koyfin 2026-10-31 快照），FY2025A 為 -0.49，基期虧損無法算三年 CAGR，改用 FY2026E 到 FY2028E 兩年約 94.5%。FY2026E 0.87 早於 Q3 財報，Q2＋Q3 GAAP EPS 已 0.56、Q4 指引 0.56–0.58，實際全年應明顯高於 0.87。內生上界約 15%／年（增量報酬約 12%–17% × 再投資率以 100% 封頂），缺口約 80 個百分點，歸因毛利率擴張（GAAP 毛利率由 FY2025 的 12.7% 到 Q3 的 56.0%）與產能利用率，不是回購或併購；這段缺口無法持續，Base 情境在 2029 年後回落。跑道：滲透率事實表未涵蓋，以 Yole 至 2031 年 CAGR 逾 18% 估需求跑道約 5–9 年；下一條曲線（CPO、6／8 吋 GaAs VCSEL 用於資料中心）只有次級來源與管理層說法，不足以判寬。衰退信號亮 2 個：EPS 成長遠快於營收（FY2026E 到 FY2027E 的 EPS +156%、營收 +116%）、FCF 長期為負（FY2022–2025 每年為負，TTM 至 2026-06 FCF 利潤率 -15.6%）。","governance":"現金流：FY2022–2025 FCF 每年為負（-3,720 萬、-710 萬、-1,790 萬、-1,880 萬美元），TTM 至 2026-06 FCF 利潤率 -15.6%，FCF 對淨利轉換率長期為負。Q3 現金及投資增加 7,700 萬到 8.26 億（Q3 法說），其中 4,350 萬是 Lumentum 預付款、屬負債，扣除後約 3,350 萬，與歸屬淨利 2,570 萬相近；DSO 因預付款降到 49 天。事實表淨負債為 -3.96 億（總債務 1.17 億、現金 5.13 億），與公司口徑的 8.26 億現金及投資差在長期投資，口徑不同。現金去向：資本支出金額事實表未涵蓋；併購、股息、回購皆為零；資金來源是 2026-04 增資約 6.32 億，以及 2026-10-27 Tongmei 對外募 2.85–5.45 億、AXT 另以 4 億增資 Tongmei。SBC：Q3 110 萬美元，占 GAAP 營業利益 3.8%、營收約 1.5%。股數：FY2025 加權股數約 4,340 萬（淨損 2,126 萬除以每股 0.49 推算），目前 6,557 萬，增加約 51%，來自增資而非 SBC。管理層說法落差：Q2 法說（2026-07-30）BD 副總 Bettles 稱擴產不需大量額外資本支出，Q3 卻安排近 9.5 億美元的 Tongmei 擴產資金。","valuation":"現價隱含：FY2027 共識 2.23 對應 23.5 倍、FY2028 共識 3.29 對應 15.9 倍；若用循環股中段 15–17 倍，市場等於要求 FY2028 之後 EPS 長期守在 3 美元以上，也就是毛利率長期高於自身歷史高點。Base 只給 FY2031 EPS 2.7、17 倍，約 46 美元，較現價約 -12%。循環位置判中循環：毛利率已遠高於自身歷史高點、全產業宣布擴產（偏晚），但量價仍齊升、報價還在漲、股價半年跌 51%（偏早）；姿態為持有不加，P/S、EV/S 高於自身所有年度端點，不宜新建立。賣方：目標價由 45 美元（First Principles 賣出）到 125 美元，最高與最低相差 2.8 倍，均值依來源 57–92 美元，多數高於現價；我比賣方保守，分歧在倍數框架：賣方用成長股倍數看 FY2027–28，我用循環股倍數看跨週期獲利，因此下調自身報酬估計的信心。FY1 共識近三個月上修 190%（0.30 到 0.87），FY2 兩次快照之間 -0.9%，上修集中在當年度。RSI 40.3，動能不過熱。","premortem":"產業態勢判雙向拉鋸：競爭惡化（JX 至多 10 倍、Sumitomo 3 倍、中國多個新案，10-K 自承競爭已壓價）對上結構轉好（AI 光通訊需求、認證 12–18 個月使缺口延續到 2027 年後），另有法規軸變動（中國出口許可、美國 232／301 關稅）。最強反駁與處置寫在反證紀錄：供給潮壓價（採納，Bear 30%）、出口許可（採納，清倉條件）、股東經濟外流（採納，Base 已預留）、價格已反映（部分採納，觀望主因）。最大回撤 -60%～-80%：前份判斷日 140.83 美元到現價 52.31 美元五個月跌 63%，26 週報酬 -50.6%，已示範這檔的波動；Bear 情境終點約 -73%；2023 年下行營收 -46%、毛利率 36.9% 到 17.6%，2025 Q1 因出口許可毛利率 -6.4%。屬深回撤標的，論點未破時不因波動砍倉，但只在價格條件到位時才建立。"},"plain":{"six":{"how_it_makes_money":"AXT 賺的是 AI 光通訊雷射與光偵測器廠的 InP 基板錢，錢卡在高品質 InP 長晶這一節點；眼下全球缺貨、客戶配額，量價齊揚撐起 56% 毛利率，但這是一段供需缺口財，製造全部在中國","moat":"護城河方向穩定（→），等級 C：低 EPD 長晶與大尺寸良率是真本事，眼下也正在搶份額，但定價權來自缺貨而非結構，對手擴產與 10-K 自承的差異化流失使優勢撐不過一個完整循環","growth":"Y5 後成長跑道中等（🟡）：需求面有 CPO 與 1.6T 接棒，但 InP 在光通訊雷射已是標準材料、成長靠量不靠滲透，2028–2030 競爭產能落地後 AXT 的獲利成長會明顯低於營收成長","capital":"資本配置偏弱：擴產靠發新股與讓出子公司股權，無股息、無回購；股票酬勞很低，但 2026 年股數已增加約五成","valuation":"現價 52.31 美元要求 2027–2028 年 56%–60% 的毛利率延續，且 2029 年後不跌回自身 12%–37% 的歷史區間才划算；前半段我信，後半段不信，估值偏貴","how_wrong":"最可能看錯的地方是把缺貨毛利率當常態：2028–2030 競爭產能落地、或中國出口許可中斷，都會讓獲利回到循環股的樣子；陷阱風險中等"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價 ≤35 美元且最近一季 GAAP 毛利率 ≥50%；價格先到、基本面未損才分批反買，股價先漲而毛利率證據未到則不追","trap":"🟡","val":"🟠","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":52.31,"week26_return_pct":-50.59,"consensus_rev_3m_pct":190.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母爭點：FY2027–28 EPS 建立在 56%–60% 毛利率上，自身年度高點僅 36.9%（2022），下行期曾到 12.7%（2025）；FY2 的 23.5 倍是循環高峰本益比，不是成長股便宜價。短期上檔以 12 個月後市場看 FY2028，Base 3.0 × 16 倍 ≈ 48 美元（-8%）；中期以 Base 終端 FY2031 EPS 2.7 × 17 倍 ≈ 46 美元（-12%）"},"catalysts":[{"date":"2026-11-27","date_precision":null,"type":"regulatory","event":"前份列出的中國商務部出口管制時點（內容本次事實表未涵蓋）","impact":"高","watch":"到期前核對商務部對 InP 出口許可的公告，有無收緊或延長"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年首季指引","impact":"高","watch":"營收是否達約 9,000 萬、毛利率是否到 6 字頭、積壓訂單是否維持逾 5 億"},{"date":"2027-07","date_precision":"month","type":"capacity","event":"管理層預告年中更新 2027 年產能再翻倍進度","impact":"中","watch":"產能是否超前，新長晶爐與 6 吋良率"},{"date":"2027-Q3","date_precision":"quarter","type":"regulatory","event":"Tongmei 香港上市（2026-07-30 法說稱約需一年）與私募融資交割","impact":"中","watch":"最終募資金額、AXT 持股是否守住 73.4% 以上、上市是否再讓股"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,383B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AXTI_20261103/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">製程型優勢真實，但定價權來自缺貨，等級 C。</p>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
<ul class="pts">
<li>護城河的機制是低 EPD 長晶 know-how、4 吋與 6 吋大尺寸的良率學習曲線，加上下游 12 至 18 個月的認證週期。這屬於製程技術型優勢，不是網路效應，也不是法定獨占。執行面給 7 分，定價面給 5 分，綜合等級 C，方向判穩定。</li>
<li>執行面的證據很扎實。2026 年 8 月提前達成 InP 產能翻倍，年底約為 2025 年底的 2.75 至 3 倍，6 吋轉入試產，新設計長晶爐提升產出。管理層兌現度高：Q2 給的 Q3 已有許可營收 6,600 萬，實際 7,340 萬。Q2 說毛利率以 5 開頭為目標，Q3 已到 56.0%。</li>
<li>定價面是缺貨帶來的週期性定價。GAAP 毛利率由去年同期 22.3% 升到 56.0%，但過去年度毛利率在 12.7% 到 36.9% 之間擺盪。2019 年與 2023 年兩次下行，毛利率分別由 36.2% 降到 29.8%、由 36.9% 降到 17.6%。10-K 自承競爭已壓價，對手以類似長晶技術生產的基板愈來愈多，已侵蝕差異化。</li>
<li>同業對照不完整。TTM 至 2026-06，AXT 毛利率 32.2%、營益率 4.2%，低於 Coherent 的 37.5% 與 12.7%，但 TTM 還沒反映這一輪。SOI.PA 與 IQE.L 沒有財報資料，Sumitomo 與 JX 是綜合集團，InP 部門不單獨揭露，所以同業報酬差距算不出來。</li>
<li>威脅清單裡四項都是黃燈。JX 至 FY2030 投資至多 1,200 億日圓、產能至多 10 倍，機率約 40%。中國新進者雲南鍺業、Vital Materials 與浙江新案，機率約 35%。中國鎵供應商已為搶市占降價，使 AXT 合資企業權益收益由 340 萬降到 80 萬美元，是中國廠進場就打價格戰的前例。</li>
<li>替代技術暫時是小風險。Fraunhofer ISE 的 InP-on-GaAs 做到 150mm，定位為取代 prime InP 的低成本方案，仍在研發階段，機率約 10%。AXT 也是 6 吋與 8 吋 GaAs 龍頭，替代發生時可部分轉回自家產品。</li>
<li>報酬持續期的結論是前瞻增量報酬約 12% 到 17%（稅前，以現行報價計）。若毛利率回到 30% 左右，增量報酬降到個位數。2026 年歷史增量報酬極高，主要來自舊產能擠出與漲價，不可外推。</li>
</ul></section>

```