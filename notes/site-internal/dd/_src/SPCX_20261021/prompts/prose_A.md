你是 stock-analyst v20 的**散文層（prose）agent**，標的 SPCX（2026-10-21）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPCX_20261021/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：SPCX　日期：2026-10-21　archetype：None　前份裁決：2026-08-05　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1785B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（626B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1010B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1686B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1449B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（711B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1100B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2895B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3970B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1994B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1785           3650-5215      5 條（2–6 內）  
s3                  8000         626           5162-7374      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4145          7598-10855      5 條（2–6 內）  
s6                 11000         711          7202-10289      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1100           1680-2400      3 條（2–6 內）  
s10                 5000        2895           1474-2105      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1994           2000-3006      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5743B；至少需散文≈39.26KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−410.3%
−410%
−350
−159
−157.5%
−85
−85%
−80%
−75.6%
−70%
−55
−55%
−29.1%
−27.2%
−13.6%
−13.4
−13%
−8.07
−7
−7%
−3.0%
−2.8%
−0.51
−0.3%
−0.09
0
0.20
0.35
0.4%
0.75
01
1
1.1
1.2
1.3
1.5%
1.7%
1.7
1.73
1.89
1.93
2
2.05
2.2
2.33
2.5
3%
3
03
3.3
3.4
3.89
04
4.0%
4
4.31
4.48
4.5
5.0%
5%
05
5
5.35%
6
6%
06
$6.0
6.08
6.65%
7%
7
07
8
08
8.5%
8.7%
9
10
10%
10.4%
11
11%
11.4
11.4%
11.7
12%
12
12.17
13%
13
13.5
14
15%
15
15.4
16
16%
16.1
16.2%
17.7
17.9%
18%
18
19.1%
20.0
20%
20
20.9%
21
21.6%
23.63
23.7
23.8%
24
24.13
25
25%
25.2%
26
27
27%
27.9
28
29.68
30%
30
31.4%
31.7
32.6%
35%
35
36%
37.6
38
40%
41.2%
41.65
41.7
42
43.0%
44
45%
45
47%
48
48.79
49
49.4%
50%
50
51.0%
52%
52.5
55%
55.4%
58.64
60
60%
60.4%
66%
66
68
69
69%
069
70
75
75.6
76.6
77
81.9
$82
82
84.5
84.7%
85
88
90
91%
$95
95
097
97
100%
100
$110
110
125
$125
125.33
128
131
132%
135
138
140
143
146
147.79
150%
152
155
158
159%
159.5
160
161%
164
165
174
175
184
192%
196
202
221.2
225
230
232
250
260.7
300
322
330
340
350
370
392.86
397
400
420
453
481
500
600
603
630
800
857
2023
2024
2025
2026
2027
2028
2029
2031
2035
14000
14300
15500
45329.43
100000
115000
120000
123000
130000
140000
150000
160000
170000
210000
230000
255000
295000
330000
400000
520000
620000
700000
20261021
1,000
1,175
1,360
1,400
1,500
1,600
1,700
15,000
2,000
2,100
2,540
3,300
4,620
4,680
5,000
6,000
6,120
7,000
7,400
7,500
−1,506%
−2,000
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
{"meta":{"ticker":"SPCX","date":"2026-10-21","schema":"v15.2","contract":"v19","company_name":"Space Exploration Technologies Corp."},"oneliner":"Q3 營收年增 161%，AI 算力租賃讓公司單季獲利，但現價已高於 Base 情境五年價值（約 128 美元）；Q4 資本支出翻倍到 350–400 億美元，算力合約多為半年期現貨價，Q1 2027 營收兌現前不追。","thesis":{"H":[{"id":"H1","text":"Starlink 用用戶量彌補單價，Connectivity 分部營收維持年增 40% 以上、分部營業利益率 40% 以上（Q3 年增 69%、利益率約 45%）","2y":null,"5y":"Starlink 寬頻加 Mobile 成為全公司最穩的現金來源，FY2031 分部營收至少是 FY2026 的三倍","10y":null,"threshold":"分部營收年增 ≥40%，營業利益率 ≥40%","source":"每季 8-K 分部表","drift_rule":"5 年論點：連 4 季偏離 ≥5% 視為削弱，連 6 季偏離 ≥10% 視為反轉"},{"id":"H2","text":"算力租賃把新增瓦數變成營收：雲服務續約每瓦單價不低於現價，Q1 2027 營收落在 330–370 億指引內，SI 調整後 EBITDA 利潤率維持 55% 以上（Q3 約 66%）","2y":"2027 年底名牌算力 ≥8 GW，且全部有租約或自用，FY2027 營收 ≥1,600 億美元","5y":null,"10y":null,"threshold":"續約單價不降，Q1 2027 營收 ≥330 億，SI 調整後 EBITDA 利潤率 ≥55%","source":"每季 8-K、CFO 在法說揭露的續約定價方向","drift_rule":"2 年論點：連 2 季偏離 ≥5% 視為削弱，連 3 季偏離 ≥10% 視為反轉"},{"id":"H3","text":"2027 年的算力資本支出（從 Q4 2026 單季 350–400 億美元起跳）能靠營運現金流與投資級債務完成，三家評等維持投資級，非併購股數年增 ≤3%","2y":"FY2027 結束時評等不變，淨負債不超過年度調整後 EBITDA 的 2 倍","5y":null,"10y":null,"threshold":"評等不低於 BBB−，非併購股數年增 ≤3%，淨負債／EBITDA ≤2 倍","source":"評等公告、10-Q 加權股數與資產負債表","drift_rule":"2 年論點：連 2 季偏離 ≥5% 視為削弱，連 3 季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"算力租金下跌：全產業 2027 年同步擴產，半年期現貨合約到期時重新定價，SI 營收兩季內下修","h_ref":"H2","clock":"⚡","threshold":"續約每瓦單價比前次降 ≥10%，或季營收低於指引下緣"},{"id":"R2","text":"融資與稀釋：S&P 預期 FCF 至少負到 2029 年，大摩估 2035 年前沒有 FCF 為正的年度；Q2 自由現金流約 −159 億，Q4 資本支出再翻倍，缺口靠發債與發股補，SBC 占營收 16%","h_ref":"H3","clock":"🔥","threshold":"評等展望轉負，或非併購股數年增 >5%，或淨負債／EBITDA >2.5 倍","evidence_refs":["unprofitable_path_to_profitability#0","unprofitable_path_to_profitability#2","capital_markets_pricing#4","unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#2","unprofitable_dilution_trajectory#4"]},{"id":"R3","text":"發射與寬頻出現第二供應商：國安發射名單擴到七家，New Glenn 拿到國安合約，Neutron 以約 5,000 萬美元對標 Falcon 9，Amazon Leo 部署中；最大客戶的採購份額可能逐步流出","h_ref":"H1","clock":"🐢","threshold":"國安任務年度分配中 SpaceX 占比低於一半，或 Amazon Leo 開始商用後 Starlink 消費者季增低於 100 萬","evidence_refs":["customer_second_source#0","customer_second_source#2","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"id":"R4","text":"治理與監管：與 Tesla 的合併正由雙方特別委員會討論（Tesla 端需全體股份過半同意）；公司章程以德州法院與強制仲裁排除集體訴訟；澳洲 ACCC 審查 Cursor 收購，國會議員要求嚴查 EchoStar 頻譜交易","h_ref":"H3","clock":"🔥","threshold":"雙方特別委員會達成協議並公布換股比例，或監管機關對頻譜交易啟動正式調查","evidence_refs":["major_events#3","regulatory_antitrust#0","regulatory_antitrust#1"]},{"id":"R5","text":"供應鏈單點：AI 算力只採 NVIDIA，記憶體是限制因素；Starlink 終端產線曾依賴中國製設備（曾申請關稅豁免）；關鍵礦物與鑄鍛件是航太產能瓶頸","h_ref":"H2","clock":"🔥","threshold":"單季新增名牌算力低於公司指引 20% 以上，或 Starlink 終端缺貨導致消費者季增低於 100 萬","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]}],"single_thing":{"description":"Q1 2027 營收低於公司指引下緣 330 億美元（這會是算力合約續約價或續約率轉弱的第一個硬數字）","why_fatal":"SI 占 Q3 營收 52%，且多為半年期現貨價合約，每瓦租金是每股價值最大的單一敏感因子。指引落空代表 2027 年 Base 路徑（1,600 億）站不住，而資本支出已承諾在每季 350–400 億的水準，淨負債與股數會一起惡化","if_happens":"不建倉；已持有者減碼一半；Bull 機率降到 15%，重啟價位下修到 ≤70 美元","how_monitor":"每季 8-K 營收、法說揭露的續約每瓦單價方向、12 月年化營收是否達 1,000 億","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":76.6,"peg_fy2":null,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":-0.51,"FY2026E":-0.09,"FY2027E":1.93,"FY2028E":4.48},"fy_end_month":12,"eps_basis":"Koyfin 共識 EPS（2026-10-08 快照，早於 Q3 財報），未標明是 GAAP 還是調整後；基期取年度財報稀釋 EPS −0.51；歷年股數口徑不一，跨年比較只作方向參考"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPCX_20261021/scenario.json","archetype":{"primary":"未獲利高成長","secondary":"循環/商品","confidence":"中","fingerprint":"FY2026 共識 EPS 仍為負（−0.09），但 Q3 已單季獲利；過半營收是按現貨價續約的 GPU 算力租賃，帶有商品循環性質"},"industry":{"clock_phase":"III","sd_verdict_source":"兩塊業務分開看。Starlink 寬頻需求屬結構性、可持久：消費者季增 160 萬，航空已簽約約 1.2 萬架。AI 算力租賃屬週期性，會反轉：回收期不到一年的報酬正吸引全產業加倍擴產，公司也計畫 2027 年新增 10 GW；供給一旦追上，半年期合約會最先反映降價。","bargaining":{"up":"供應商議價力強。AI 算力只採 NVIDIA（2026-08-04 法說 Musk），記憶體是限制因素。渦輪葉片鑄件比整機晚 12–18 個月交貨（2026-10-20 法說 Musk），公司用自有鑄造能力補位。","down":"客戶議價力目前弱：管理層稱 hyperscaler 排隊租算力，續約每瓦單價上升。但合約短，客戶到期就能轉租他處。最大客戶占 2025 年營收 20.9%，比 2023 年的 25.2% 低。","geo":"2024 年曾要求台灣供應商把產線移往泰國、越南；曾為中國製的終端產線設備申請關稅豁免；Section 232 航太調查 2026-07 結束、未加稅，但摘要被截斷，細節未證實。"},"profit_pool_dir":"利潤池往算力上游（晶片）與下游（模型應用）集中，中段租賃的報酬取決於供需缺口。公司用 Terafab 自製晶片（目標 2028 Q3 量產，管理層自稱極激進）和 Grok／Cursor 往兩端延伸。","tam_table":[{"item":"全球太空經濟規模（2026）","value":"約 4,620–4,680 億美元，長期年複合成長 7%–8.7%；GlobalData 估僅 4.0%"},{"item":"美國三大電信年營收（Starlink Mobile 目標市場）","value":"約 6,000 億美元（Q2 法說引述）；自有頻譜服務 2028 年初才開通"},{"item":"AI 算力租賃市場規模與公司份額","value":"事實表未涵蓋；只有公司名牌算力 1.7 GW 與 2027 年底 13 GW 目標"},{"item":"營業利益池占比（五年前→現在）","value":"事實表未涵蓋"}]},"moat":{"mechanism":"可重複使用火箭帶來每公斤發射成本與頻次的優勢，讓自家星座部署成本最低、容量領先（Starship 單次已部署 26 Tbps，相當於 10 次 Falcon 9），Starlink 因此能用用戶量彌補單價。AI 算力段的優勢只有供電與建置速度；管理層稱自有鑄件可把渦輪交期縮短 12–18 個月，未經證實。","execution":9,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力在擴大：Q3 發射 35 次，Starship 首次入軌並部署 V3 衛星，名牌算力 1.7 GW 依進度。定價力持平：Falcon 9 牌價由 6,120 萬漲到約 7,400 萬美元，但國安發射名單 2026-07 新增 Impulse Space 與 Relativity 兩家，最大客戶開始分散供應商，所以方向不能標為上升。消費者 ARPU 由一年前 85 美元降到 Q2 的 66、Q3 回到 69 美元，是用用戶量彌補單價。","peer_na_reason":"事實表未涵蓋同業 ROIC 與投入資本，改以利潤率對照","threats":[{"level":"🟡","text":"國安發射供應商名單擴到七家（新增 Impulse Space、Relativity Federal），最大客戶的發射採購開始分散","p":"40%","evidence_refs":["customer_second_source#0","customer_second_source#2"]},{"level":"🟡","text":"Blue Origin New Glenn（低軌 45 噸、國安合約 24 億美元）與 Rocket Lab Neutron（單次約 5,000 萬美元）在中重型發射市場正面比價","p":"35%","evidence_refs":["substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"Amazon Leo 部署中、尚未商用，商用後會搶 Starlink 的企業、政府與新興市場訂戶","p":"30%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率、低周轉。過去四季營業利益率 −13.6%、FCF 利潤率 −157.5%。Q3 單季營業利益率升到 19.1%，但單季資本支出 196 億已超過單季營收 146 億，投入資本周轉率偏低（投入資本金額事實表未涵蓋）。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"Starlink 的使用者就是付款者，屬於剛需而非可有可無（消費者季增 160 萬、航空約 1.2 萬架已簽約）。算力的使用者是模型公司，公司自己用掉約一半算力；外租部分按現貨價、半年期出租。客戶要解決的問題（訓練與推論算力）會長期存在，但向誰租可以每半年重選。"},{"item":"決策層級","level":"🟡","text":"發射：國安客戶按任務招標，並在擴大供應商名單。寬頻：企業客戶黏著度高（Q2 法說稱從未流失企業客戶）。算力：半年期合約到期就能轉租，替換成本低，管理層刻意選短約，押注租金上升。"},{"item":"價值鏈分配","level":"🔴","text":"AI 算力鏈的利潤多被晶片端拿走。公司只採 NVIDIA，記憶體是限制因素，算力租賃位在價值鏈中段。SI 占 Q3 營收 52%，Q3 資本支出 196 億中有 164 億投在這段，但它不是最難取代的環節。發射與衛星端則垂直整合，利潤留在自己手上。"},{"item":"社會容忍度","level":"🟡","text":"寬頻與手機直連依賴 FCC 授權。2026-01 核准再發射 7,500 顆 Gen2，但附帶須遵守日後規則的條件；近期又核准 15,000 顆 Mobile V2。國會議員曾致函 DOJ 與 FCC，要求嚴查 EchoStar 頻譜交易。營收有 20.9% 來自單一大客戶，政策轉向會直接衝擊。"}],"roiic":"約 20%（粗估）。SI 分部調整後 EBITDA 季增 38 億美元、年化約 152 億，對應 Q2 約 158 億加 Q3 164 億、合計約 322 億的算力資本支出，稅前 EBITDA 報酬約 47%；扣掉五年折舊後稅前約 27%，稅後約 20%。只算 SI 分部，用的是管理層口徑，事實表未收投入資本。","reinvest_rate":"遠大於 100%。前九個月 PP&E 購置 481 億美元，營業現金流只有 131 億，自由現金流 −350 億；差額由 IPO 淨募資約 857 億與 2026-06 發債 250 億支應。","endo_ceiling":16,"formula_note":"內生成長＝增量報酬約 20%×自籌再投資率上限 100%＝約 20%/年；資本配置三項評分無一通過，再打八折，約 16%/年。共識 FY2026→FY2027 營收 +159%，超出的部分全靠外部資金。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","SPCX":50.95,"RKLB":37.26,"ASTS":39.17,"PL":55.42,"IRDM":71.85,"unit":"%"},{"metric":"營業利益率","SPCX":-13.63,"RKLB":-29.06,"ASTS":-410.26,"PL":-27.16,"IRDM":23.76,"unit":"%"},{"metric":"FCF 利潤率","SPCX":-157.52,"RKLB":-48.25,"ASTS":-1506.12,"PL":4.96,"IRDM":32.61,"unit":"%"},{"metric":"研發密度","SPCX":51.23,"RKLB":40.62,"ASTS":249.67,"PL":33.86,"IRDM":2.46,"unit":"%"}],"competitors":[{"name":"RKLB","gm":37.26,"om":-29.06,"fcf_margin":-48.25,"rd_intensity":40.62,"strategy_note":"Neutron 約 13 噸低軌運力、單次約 5,000 萬美元，直接對標 Falcon 9，首飛延到 2026 Q4；過去四季營業利益率 −29.1%，規模差兩個數量級，短期只是單一產品線的正面競爭","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ASTS","gm":39.17,"om":-410.26,"fcf_margin":-1506.12,"rd_intensity":249.67,"strategy_note":"手機直連衛星的對手，過去四季營業利益率 −410%、FCF 利潤率 −1,506%，仍在燒錢建網；和 Starlink Mobile 搶同一批電信夥伴","period":"TTM ending 2026-06-30（4季加總）"},{"name":"PL","gm":55.42,"om":-27.16,"fcf_margin":4.96,"rd_intensity":33.86,"strategy_note":"做地球觀測，不直接競爭；毛利率 55.4%、FCF 已轉正（+5.0%），說明小型衛星營運商也能自給，但規模無法比","period":"TTM ending 2026-07-31（4季加總）"},{"name":"IRDM","gm":71.85,"om":23.76,"fcf_margin":32.61,"rd_intensity":2.46,"strategy_note":"唯一獲利的衛星同業（營業利益率 +23.8%、FCF 利潤率 +32.6%），可當 Starlink 成熟後利潤結構的參照；SpaceX 正促請 FCC 檢視 IRDM 對競爭業者的行為","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"以量為主（算力瓦數、Starlink 訂戶與航空裝機），價格為輔（算力每瓦租金上升、ARPU 69 美元），併購小幅（Cursor Q3 貢獻 6.08 億），回購為負（股數淨增加）","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段：增量報酬約 20%×自籌再投資率 100%，打八折約 16%/年。共識營收 FY2026→FY2027 +159%，缺口來自外部融資（IPO 淨募資約 857 億、2026-06 發債 250 億）、全股票收購 Cursor（600 億）與利潤率擴張（過去四季營業利益率 −13.6%→Q3 19.1%），不是內生成長","segments":[{"item":"SI（算力租賃＋Grok＋Cursor＋X 廣告）","value":"Q3 營收 75.6 億美元（季增 50 億），營業利益 4.31 億（扣 Cursor 相關 SBC 12.17 億前約 16 億），調整後 EBITDA 50 億；資本支出 164 億"},{"item":"Connectivity（Starlink 寬頻／Mobile／Starshield）","value":"Q3 營收 52.5 億（年增 69%），營業利益 23.7 億（利益率約 45%）；企業與政府營收年增 91%；資本支出 15.4 億"},{"item":"Space（發射、Dragon、Starship）","value":"Q3 營收約 17.7 億（年增 6%）；Q2 調整後 EBITDA 虧損 2.05 億（Starship 研發）；資本支出 16.1 億"}],"decay_signals":[{"item":"SBC 占營收 >5% 且逐年上升","lit":true,"evidence":"Q3 SBC 23.63 億、占營收 16.2%；2025 年約 10.4%（兩個聚合站數字相除）；Cursor 收購另有 230 億將在約三年內認列"},{"item":"毛利率連 2 季年減","lit":false,"evidence":"年度毛利率 41.2%→43.0%→49.4%，過去四季 51.0%；但 Q3 含約 3 個百分點的關稅退款，公司預告 Q4 毛利率回到 Q2 水準"},{"item":"主力產品漲價後銷量下滑","lit":false,"evidence":"2026-05 Starlink 方案漲價最多 10 美元／月，Q3 消費者仍季增 160 萬"},{"item":"核心市占縮減","lit":false,"evidence":"國安發射名單擴大，但事實表未涵蓋份額數字，暫不亮燈，列入觀察"},{"item":"FCF/NI <0.75 連 2 年","lit":false,"evidence":"虧損年度比值沒有意義，改看 FCF 利潤率：2025 年 −75.6%、過去四季 −157.5%，屬投資期，不是獲利品質崩壞"},{"item":"其餘五類（EPS 與營收成長背離、TAM 萎縮、產業倍數下移、維護性資本支出占 FCF >60%、停止擴產）","lit":false,"evidence":"都不成立，或事實表未涵蓋"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自自建算力（SI 營收扣掉 Cursor 6.08 億後，季增仍達 192%），併購不是成長支柱；公司不配息也不回購，沒有股東回饋可展開"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Cursor 以 600 億美元全股票收購（2026-08-14 完成），其中 230 億列為留任與替換獎酬，約三年認列為 SBC；Q3 貢獻營收 6.08 億，但 Cursor 相關 SBC 12.17 億讓 SI 分部營業利益只剩 4.31 億，已實現報酬未達資金成本","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"沒有回購計畫；Q1 向 xAI 員工回購 2,540 萬股、24.13 億美元，屬合併交割，不算股東回饋","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 占營收 16.2%；Cursor 換股 3.89 億股，約占目前股數 3%；10-Q 加權股數由上半年 48.79 億升到 Q2 的 58.64 億（含 IPO），淨稀釋遠超每年 1.5%","grade":"不過"}]},"valuation":{"basis":"EV/S（尚未獲利的高成長股以前瞻 EV/S 為主要估值尺，轉為穩定獲利後改用前瞻本益比）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業 EV/S 現值；本檔同時做發射、寬頻與 AI 算力，沒有可直接比的同業。終端倍數改以自身前瞻與歷史倍數，以及唯一獲利衛星同業 IRDM 的利潤結構作對照"},"peg":null,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"前瞻 EV/S 41.7 倍，過去 12 個月 81.9 倍。機率加權五年價值約 165 美元，Base 約 128 美元，Base 低於現價；Bear 終點約 30 美元（−80%），因此偏貴。上市未滿五年，沒有五年分位可用（3 個年度端點分位 1.7% 不是五年口徑）。","upside_short_pct":-7,"upside_mid_pct":-13.4},"trap_analysis":{"verdict":"🟡","label":"成長是真的，但每股經濟可能被稀釋與資本支出吃掉"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"管理層明言算力按現貨價、用短約出租，不簽長約；Q4 資本支出 350–400 億美元，2027 年目標新增 10 GW（最多 20 GW）；Q3 SI 營收 75.6 億，占全公司 52%","assumption":"每瓦算力的價值隨模型進步只升不降（Musk 以 H100 舊卡租金上漲為例）","consequence":"全產業同步擴產，2027–28 年供給追上需求時，半年期合約兩季內就會重新定價；SI 營收與 EBITDA 一起下修，已投入的算力資產靠債務撐著，淨負債升到約 1,700 億，對應 Bear 終點約 30 美元","ruling":"採納為主要下行情境（Bear 機率 30%）。管理層只有個別例子（舊卡租金、續約價上升），沒有供給端的數字。此情境與 Single Thing 是同一個檢驗（Q1 2027 營收），不另立一條","watch":"每季法說的續約每瓦單價方向；Q1 2027 營收對比 330–370 億指引","fact_refs":["f_kpi11_si","f_kpi4_pp_e","f_kpi10_nameplate_compute"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 SBC 23.63 億，占營收 16.2%、占 GAAP 營業利益 84.7%；Cursor 600 億收購價中有 230 億約三年攤為 SBC；股數口徑混亂，基本與稀釋股數相同（潛在稀釋證券因反稀釋被排除）；S&P 預期 FCF 負到 2029 年，大摩估 2035 年前沒有 FCF 為正的年度；公司章程以德州法院與強制仲裁排除集體訴訟；與 Tesla 的合併已由雙方特別委員會討論","assumption":"營收目標達成，就等於每股價值上升","consequence":"即使 2027 年營收照 Bull 走，持續發股融資、SBC 與可能的 Tesla 換股會吃掉一截每股成長。Base 已假設 2031 年股數 143 億（+8.5%）；若每年稀釋 3% 以上，Base 每股價值會再少約 6%","ruling":"採納：Base 與 Bear 都提高終端股數；Tesla 合併條款公布前不建倉","watch":"10-Q 加權股數、SBC 占營收比、Tesla 特別委員會進度","evidence_refs":["unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#2","unprofitable_dilution_trajectory#4","unprofitable_path_to_profitability#0","major_events#3"],"fact_refs":["f_kpi7_sbc","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"EV 約 1.89 兆美元，前瞻 EV/S 41.7 倍；Base 情境（2031 年營收 3,300 億×6 倍）每股約 128 美元，低於現價；賣方共識目標價被下修（225→202），GLJ 指 Q2 自由現金流燒掉 159.5 億、銷售倍數約 77 倍","assumption":"Q1 2027 年化約 1,400 億營收可以直接當基期，EV/S 只剩約 13.5 倍","consequence":"現價已經把 Base 兌現算進去，剩下的報酬只來自 Bull 情境；一旦季度營收落在指引下緣，倍數與營收會一起往下","ruling":"採納：估值偏貴，不追。但不據此放空，因為管理層連兩季超預期、算力建置也按時","watch":"股價與 Base 五年價值的距離（≤95 美元才有安全邊際）","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_ev_m","f_ev_s_fwd","f_price_at_dd"]}],"max_dd":{"lo":-85,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 125.33 → 本次 147.79（+17.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=125.33","side_b":"本次 price_at_dd=147.79","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 125.33 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 125.33 美元：Bull 價 260.7、Bear 價 37.6，五年期望值 −0.3%，基準年化 −3.0%，不對稱比 1.3","side_b":"本次情境、股價仍用 125.33 美元：Bull 價 392.86、Bear 價 29.68，五年期望值 +31.4%，基準年化 0.4%，不對稱比 2.33","ruling":"先換情境、股價不動：五年期望值多 31.7 個百分點，基準年化多 3.4 個百分點。不對稱比由 1.3 變為 2.33。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 125.33 美元：五年期望值 +31.4%，基準年化 0.4%，不對稱比 2.33","side_b":"本次情境、股價 147.79 美元：五年期望值 +11.4%，基準年化 −2.8%，不對稱比 1.73","ruling":"再換股價、情境不動：起點價上漲 17.9%，五年期望值少 20.0 個百分點，基準年化少 3.3 個百分點，不對稱比由 2.33 降到 1.73。合計五年期望值比前份多 11.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"Q1 2027 年化營收能否當基期（不可調和）","cause":"新證據","prior_field":null,"side_a":"多方：Q3 營收 146 億、年增 161%，Q1 2027 指引 330–370 億，年化約 1,400 億，EV/S 只剩約 13.5 倍；調整後 EBITDA 利潤率 60%，在手訂單 630 億（一年內認列約 420 億）；管理層稱客戶排隊租算力、續約單價上升、回收期不到一年。這是現在就買的最強論證","side_b":"空方：算力合約多為半年期、按現貨價，管理層刻意不簽長約；Q4 資本支出 350–400 億，全產業同步擴產；S&P 預期 FCF 負到 2029 年。年化值能維持多久取決於整體供需缺口，不是公司能控制的","ruling":"選空方，暫不追。兩方方向相反，決定勝負的數據（2027 上半年續約價與 Q1 營收）要到 2027-05 才出現，今天的證據涵蓋不到 2027–28 年的供給風險期。真正卡住的是估值：現價高於 Base 五年價值。解除條件是股價回到 ≤95 美元，或 Q1 2027 證明年化營收可延續（屆時 Base 上修，≤125 美元即可）。多方的營收證據是一手資料、且連兩季兌現，所以不放空、不迴避，只等價格或數據","evidence_level":"一手（公司 8-K、Q3 法說 CFO 與 Musk 發言）","settle_metric":"Q1 2027 營收對比 330–370 億指引、續約每瓦單價方向","if_then":["若 Q1 2027 營收 ≥350 億、續約每瓦單價不降，且 Q4 資本支出 ≤400 億，則在 ≤125 美元建首倉（小倉位），Bull 機率上調到 30%","若 Q1 2027 營收 <330 億，或管理層揭露續約單價下降，則不建倉，Bull 機率降到 15%，重啟價位下修到 ≤70 美元","若股價先跌到 ≤95 美元而基本面數據未惡化，則分批建首倉，不等 Q1 2027","若股價續漲但上述數據還沒出來，則不追"]},{"axis":"管理層前一季承諾對照（Starship、Mobile、算力）","cause":"新證據","prior_field":null,"side_a":"2026-08-04 Q2 法說：Musk 稱約一年後 Starship 每天至少飛一次，下一次飛行（8 月底）會試塔架接船，V3 衛星需約 1,000 顆、2027 年第二季達到；Shotwell 稱 Starlink Mobile 2027 年底開始服務；Musk 稱 2027 年底算力約 10 GW","side_b":"2026-10-20 Q3 法說：Musk 改為 2027 上半年每週一飛、下半年每週兩飛，接船延到 Flight 15（11 月）；Shotwell 稱 V3 只要「幾百顆」、2027 年中達到，Mobile 改為 2028 年初開通；算力則上調為 2027 年底約 13 GW，且 10 月底已達約 2.2 GW","ruling":"可調和，屬程度差異。太空與 Mobile 時程系統性延後（Mobile 至少延一季），V3 的門檻被改寫降低；算力建置是唯一按時、甚至超前的一塊。所以 Mobile 與 Starship 營收不放進任何情境的 2027 年，Base 只靠算力與寬頻","evidence_level":"一手（兩季法說原話）","settle_metric":"2027 上半年 Starship 實際每月飛行次數、Mobile V2 首批發射時點","if_then":["若 2027-06 前 Starship 未達每月至少兩飛，則下修 Bull 路徑的 Starlink 容量假設","若 Mobile V2 首批發射延到 2027 下半年以後，則所有情境的 Mobile 營收都延後到 2029 年"]},{"axis":"資本支出與算力自用比例改口","cause":"新證據","prior_field":null,"side_a":"2026-08-04 Q2 法說：CFO 稱未來兩季資本支出與 Q2（約 184 億美元）相近；Musk 預期內部 Grok 訓練只占約一成算力；Musk 宣布 AI 算力只採 NVIDIA","side_b":"2026-10-20 Q3 法說：Q3 資本支出 196 億大致符合，但 Q4 指引升到 350–400 億，約為原說法的兩倍；Musk 改稱目標是自用與外租各半（可在六四之間浮動），並採現貨短約；另宣布 Terafab 自製晶片，2028 Q3 量產是內部目標，管理層自稱極激進","ruling":"改口方向對股東不利，採納新說法。自用比例由一成升到五成，代表每 GW 的對外營收少四成以上（若 Q2 說的一成只指訓練、不含自家推論，落差會小一些）；同時資本支出翻倍，還多了一座晶片廠的資金需求。Base 以自用與外租各半估算每 GW 對外營收，並上調淨負債終點","evidence_level":"一手（兩季法說原話）","settle_metric":"Q4 2026 實際資本支出、SI 對外雲服務營收占比","if_then":["若 Q4 實際資本支出 >400 億，且 SI 對外營收占比低於一半，則 Base 淨負債終點上調到 2,000 億、Bull 機率降到 20%","若 Q4 資本支出 ≤350 億，且對外營收占比回升到六成以上，則 Base 淨負債終點下調到 1,000 億"]},{"axis":"Q3 獲利品質","cause":"新證據","prior_field":null,"side_a":"Q3 GAAP 營業利益 27.9 億（利益率 19.1%），淨利 44 億，調整後 EBITDA 88 億（60.4%），公司稱營運槓桿顯現","side_b":"Connectivity 毛利率 55% 含約 3 個百分點的關稅退款一次性收益，CFO 預告 Q4 全公司毛利率回到 Q2 水準；淨利高於營業利益，差額來自營業外，事實表未拆分；SBC 占 GAAP 營業利益 84.7%","ruling":"可調和，屬程度差異。獲利轉正是真的（SI 新產能開始賺錢），但 Q3 的利益率高估了常態；情境樹不用 Q3 利益率外推","evidence_level":"一手（8-K、Q3 法說 CFO）","settle_metric":"Q4 2026 毛利率是否回到 Q2 水準、Connectivity 扣除一次性收益後的利益率","if_then":["若 Q4 毛利率比 Q2 水準低 3 個百分點以上，則 Base 終端 EV/S 下調到 5 倍"]},{"axis":"賣方目標價分歧","cause":"新證據","prior_field":null,"side_a":"MarketBeat：42 位分析師平均目標價 221.2 美元（27 買／8 持有／7 賣），較現價高約 50%","side_b":"StockHub 報導共識目標價由 225 降到 202；目標價區間 75–800 美元，最高與最低相差逾 10 倍","ruling":"不拿來當支撐。區間寬到無法當錨，反映賣方對終端倍數沒有共識。本次結論比平均目標價悲觀，因為市場把年化營收當基期，沒有為合約期限打折","evidence_level":"二手（聚合站）","settle_metric":"Q1 2027 財報後目標價中位數的方向","if_then":["若 Q1 2027 財報後平均目標價下修超過 15%，即確認空方對年化營收打折的看法"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"前份風險項處置","cause":"新證據","prior_field":null,"side_a":"前份三項風險：鎖定股解禁的供給壓力（2026-12-08 全面解禁）；AI 客戶集中加上 90 天終止條款與租價下跌；多個星座同時進入 Starlink 的擴張市場","side_b":"本包對解禁時程與客戶名單沒有新證據；Q3 法說改稱客戶眾多、採現貨短約；Amazon Leo 約 300 顆、尚未商用","ruling":"不刪門檻。解禁保留在最大回撤的依據內，繼續觀察；客戶集中與終止條款因本包未涵蓋客戶名單與條款內容，併入本次第一項風險（短約重新定價），以續約單價下降 ≥10% 為門檻；多星座競爭保留為本次第三項風險","evidence_level":"前份判斷＋本包一手法說","settle_metric":"2026 年 10-K 的客戶集中度附註、2026-12-08 解禁後的成交量與股價","if_then":["若 10-K 顯示單一算力客戶占營收超過 20%，則把客戶集中改回獨立風險項，Bear 機率上調到 35%"]},{"axis":"前份漂移：價格與裁決","cause":"價格變動","prior_field":["signal","val","p_bull_pct","p_bear_pct"],"side_a":"前份（2026-08-05）股價 125.33 美元：觀望，估值偏貴，訊號 B，Bull 25%／Bear 30%","side_b":"本次股價 147.79 美元（+18%）：估值仍偏貴，訊號 B 不變；Bull／Bear 機率維持 25%／30%。Q3 營收大幅超預期，原本應上調 Bull，但被 Q4 資本支出翻倍與算力自用比例升到五成抵銷","ruling":"股價上漲，Base 每股價值也因營收路徑上調而同步上修，估值結論與裁決方向不變","evidence_level":"一手（股價、8-K）","settle_metric":"股價與 Base 五年價值 128 美元的距離","if_then":["若股價 ≤95 美元，則分批建首倉"]},{"axis":"前份漂移：基本面欄位","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份：價值陷阱風險中等，護城河持平，五年後成長空間寬，屬未獲利高成長","side_b":"本次四欄都不變，但依據換新：陷阱風險中等，改由 SBC 占營收 16.2% 亮燈支撐；護城河持平，因國安發射名單擴到七家，方向不能標為上升；成長空間寬，因 FCC 核准 15,000 顆 Mobile V2 且公司收購了低頻頻譜；仍歸未獲利高成長，因 FY2026 共識 EPS −0.09，Q3 雖單季獲利，全年尚未轉正","ruling":"結論不變，證據更新","evidence_level":"一手＋二手","settle_metric":"FY2026 全年 GAAP EPS 是否轉正（2027-01 財報）","if_then":["若 FY2026 全年 GAAP EPS 轉正且 FY2027 共識上修，則改用前瞻本益比作為主要估值尺"],"evidence_refs":["customer_second_source#0"]},{"axis":"前份漂移：回撤與循環位置","cause":"方法變動","prior_field":["max_dd_pct","cycle_position"],"side_a":"前份最大回撤取單點 −70%；循環位置未填","side_b":"本次改填範圍 −85%～−55%，因為 Bear 終點約 −80%，回撤下緣必須涵蓋；循環位置仍不填，因為主要分類不是循環股，算力租賃的循環性改寫進 Single Thing 與 Bear 情境","ruling":"屬方法變動，不是新看法：範圍中點 −70% 與前份一致","evidence_level":"判斷","settle_metric":null,"if_then":[]},{"axis":"重啟條件變動（建首倉價位）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤$82（隱含 AI 分部 ≤35x FY27E EBITDA）且 H1/H2 監測未惡化；或 Q3 AI 分部營收 ≥$6.0B ＋ Google/Anthropic 合約展期，則 ≤$110 可建 starter","side_b":"股價 ≤$95 建首倉；或 Q1 2027 營收 ≥350 億美元且續約每瓦單價不降，≤$125 建首倉","ruling":"前份條件中「Q3 AI 分部營收 ≥60 億美元」已達成（實際 75.6 億），但 ≤110 美元的價格條件沒到，合約展期在本包也沒有證據，所以前份重啟條件沒有完整觸發。新證據讓 Base 營收路徑上調（Q1 2027 指引 330–370 億），Base 每股價值隨之升高，純價格門檻由 82 上移到 95 美元；事件門檻改用下一個硬數字，也就是 Q1 2027 營收","evidence_level":"一手（8-K、Q3 法說）","settle_metric":"Q1 2027 營收、股價","if_then":["若兩個條件任一成立，則建首倉（小倉位），並重跑一次判斷確認"]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"Q1 2027 營收低於指引下緣 330 億美元（這會是算力合約續約價或續約率轉弱的第一個硬數字）","ruling":"Q3 法說首次揭露算力採現貨短約，並給出 Q1 2027 營收指引，Single Thing 因此有了可檢驗的二元事件。選它是因為 SI 占營收過半，每瓦租金是每股價值最大的單一敏感因子","evidence_level":"一手（Q3 法說）","settle_metric":"Q1 2027 營收","if_then":["若 Q1 2027 營收 <330 億，則不建倉，已持有者減碼一半"]},{"axis":"新設退出指標（減碼／清倉門檻）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設退出指標（null）","side_b":"新設五條：Q1 2027 營收 <330 億；續約每瓦單價比前次降 ≥10%；任一家評等降到 BBB− 以下或展望轉負；Connectivity 營收年增連 2 季 <40%；非併購股數年增 >5%","ruling":"前份只有重啟條件，沒有退出門檻，本次補上：任兩條觸發即減碼一半，評等跌破投資級即清倉","evidence_level":"判斷","settle_metric":null,"if_then":["若任兩條觸發，則減碼一半","若評等跌破投資級，則清倉"]}],"triggers":[{"n":1,"text":"Q1 2027 營收對比公司指引 330–370 億美元","type":"Single Thing","maps_to":"H2","metric":"季營收","threshold":"<330 億美元","action":"不建倉；已持有者減碼一半","source_freq":"每季 8-K","date":"2027-05"},{"n":2,"text":"Q1 2027 營收 ≥350 億，且續約每瓦單價不降","type":"假設驗證","maps_to":"H2","metric":"季營收＋續約單價方向","threshold":"≥350 億美元，且單價持平或上升","action":"股價 ≤125 美元時建首倉（小倉位）","source_freq":"每季 8-K＋法說","date":"2027-05"},{"n":3,"text":"股價跌到 Base 五年價值的七五折以下","type":"估值rearm","maps_to":null,"metric":"股價","threshold":"≤95 美元","action":"在基本面未惡化的前提下，分批建首倉（小倉位）","source_freq":"每日","date":null},{"n":4,"text":"長期信用評等跌破投資級","type":"清倉","maps_to":"H3","metric":"Moody's／S&P／Fitch 評等","threshold":"任一家降到 BBB− 以下","action":"清倉","source_freq":"即時","date":null},{"n":5,"text":"Q4 2026 實際資本支出與 12 月年化營收","type":"複審日期","maps_to":"H3","metric":"Q4 資本支出、12 月年化營收","threshold":"資本支出 >400 億，或 12 月年化營收 <1,000 億","action":"任一成立就把 Bull 機率降到 20% 並重算情境；兩者都達標則維持","source_freq":"Q4 財報","date":"2027-01"},{"n":6,"text":"Starlink 寬頻成長放緩","type":"風險","maps_to":"H1","metric":"Connectivity 分部營收年增率","threshold":"連 2 季 <40%","action":"停止加碼；連 3 季則減碼一半","source_freq":"每季 8-K","date":null},{"n":7,"text":"與 Tesla 的合併條款公布","type":"風險","maps_to":"R4","metric":"特別委員會協議與換股比例","threshold":"雙方特別委員會達成協議","action":"條款公布前不建倉；公布後重跑判斷","source_freq":"8-K／新聞稿","date":null},{"n":8,"text":"非併購股數膨脹","type":"減碼","maps_to":"R2","metric":"10-Q 加權稀釋股數年增率（扣除併購換股）","threshold":">5%／年","action":"減碼一半","source_freq":"每季 10-Q","date":null,"evidence_refs":["unprofitable_dilution_trajectory#0"]}],"kill_metrics":[{"metric":"季營收對比公司指引下緣","bear_threshold":"Q1 2027 營收 <330 億美元","window":"Q1 2027 財報（約 2027-05）","source":"公司 8-K 新聞稿","last_status":"unknown"},{"metric":"雲服務合約續約每瓦單價","bear_threshold":"比前次續約下降 ≥10%（管理層口徑轉為下降）","window":"每季法說","source":"法說會管理層揭露","last_status":"ok"},{"metric":"長期信用評等","bear_threshold":"任一家降到 BBB− 以下，或展望轉負","window":"即時","source":"Moody's／S&P／Fitch 公告","last_status":"ok"},{"metric":"Connectivity 分部營收年增率","bear_threshold":"連 2 季 <40%","window":"每季","source":"8-K 分部表","last_status":"ok"},{"metric":"非併購股數年增率","bear_threshold":">5%／年","window":"每季","source":"10-Q 加權稀釋股數","last_status":"unknown"}],"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Q1 2027 年化約 1,400 億美元營收當成可延續的基期，但這批營收多半來自約半年期、按現貨價續約的算力合約，而 Q4 資本支出已升到 350–400 億美元；市場沒有為年化值能維持多久打折"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='→', week26=-8.07, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 情境缺少「瓦數 × 每瓦租金 → 營收 → EPS」的算術，歷史上高估值高成長的可比案例（Cisco）報酬遠低於 Bull 隱含的年化 21.6%，五年成長跑道的「滲透率低」與 FCC 核准也沒有可回溯的來源，因此 Bull 依據目前不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='未獲利高成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"verdict":"觀望","rearm_trigger":"股價 ≤$95 建首倉；或 Q1 2027 營收 ≥350 億美元且續約每瓦單價不降，≤$125 建首倉","exec_line":"不追。股價 ≤95 美元時分批建首倉（小倉位）；Q1 2027 驗證通過後，≤125 美元建首倉；Tesla 合併條款公布前不建倉；已持有者遇 Single Thing 觸發減碼一半，評等跌破投資級則清倉"},"reasoning":{"industry":"營收分部（Q3）：SI 75.6 億（52%），Connectivity 52.5 億（36%），Space 約 17.7 億（12%）。全公司 GAAP 營業利益率 19.1%，調整後 EBITDA 利潤率 60.4%，淨利 44 億，稀釋 EPS 0.35 美元。過去四季（至 2026-06）毛利率 51.0%，營業利益率 −13.6%。定價權在哪：算力段的定價權在晶片供應商與現貨市場，公司只是中段的租賃方；寬頻段由公司自己掌握，因為自有火箭讓部署成本最低。單點依賴：供應端，AI 算力只採 NVIDIA（2026-08-04 法說 Musk），記憶體是目前的限制因素；需求端，最大客戶占 2025 年營收 20.9%（申報檔未具名，媒體解讀為美國政府），比重由 2023 年 25.2% 逐年下降，屬集中度風險，不是護城河證據。產業時鐘 III：算力回收期不到一年、續約價上升，超額報酬正吸引全產業加倍擴產，公司自己 Q4 資本支出指引 350–400 億、2027 年目標新增 10 GW；寬頻段仍在擴張期。產業態勢是雙向拉鋸。惡化的一面：國安發射名單擴到七家，New Glenn 拿到國安合約，Amazon Leo 仍在部署。轉好的一面：FCC 再核准 7,500 顆 Gen2 與 15,000 顆 Mobile V2，公司買入 EchoStar 與低頻頻譜、轉向自營電信，Section 232 航太調查也未加關稅。","moat":"執行力 9 分：2025 年 Falcon 9 發射 165 次；Q3 共 35 次，含 2 次 Starship、6 次國安任務；Starship Flight 14 首次入軌並部署 V3 衛星。Musk 稱公司占全球入軌質量近九成，這是管理層說法，未獨立核實。算力建置按進度：Q3 末 1.7 GW，10 月底約 2.2 GW。定價力 6 分：發射端，Falcon 9 牌價由 6,120 萬漲到約 7,400 萬美元，仍遠低於 Vulcan、Ariane 6 的約 1.1 億；寬頻端，消費者 ARPU 由一年前 85 美元降到 Q2 的 66 美元，Q3 因客群組合回到 69 美元，等於用用戶量彌補單價下滑；算力端價格由市場決定，公司只能跟著現貨價。同業對照：事實表未收投入資本，算不出報酬率差距。改看過去四季營業利益率：SPCX −13.6%，低於唯一獲利的 IRDM（+23.8%），高於 RKLB（−29.1%）、PL（−27.2%）、ASTS（−410.3%）。因此合併分不到 8 分，評 B。報酬持續期：當期屬低利益率、低周轉；四個檢查點中價值鏈分配為紅（算力租賃排在晶片之後），其餘為黃。增量報酬粗估約 20%，但再投資率遠大於 100%，成長靠外部資金。","growth":"成長以量為主：名牌算力由 Q3 末 1.7 GW 擴到年底 2.5–3 GW，2027 年底目標 13 GW（管理層說法）；Starlink 消費者季增 160 萬、達 1,360 萬，航空已簽約約 1.2 萬架。價格是輔助：算力每瓦租金略高於 30–50 美元區間上緣，續約價上升；ARPU 69 美元。併購：Cursor 在 Q3 約半季貢獻 6.08 億。回購：沒有，股數反而淨增加。共識三年 EPS：基期 FY2025 為 −0.51、FY2026 共識 −0.09，算不出複合成長率；FY2027 1.93→FY2028 4.48（+132%），這兩年的共識近期各上修約 11%。共識營收 FY2026 453 億→FY2027 1,175 億（+159%），但 Q1 2027 指引 330–370 億，已讓 FY2027 共識顯得過時。內生上限約 16%（見護城河段）。缺口來自外部融資、全股票收購與利潤率擴張，來源說得清楚，不是單靠估值倍數上調。成長年限：全球可服務家戶與算力市場規模事實表未涵蓋，年數是判斷值；滲透率低，第二條曲線（Mobile 自有頻譜）已有 FCC 核准與頻譜收購為證，評為寬。衰退信號只亮一個（SBC 占營收 16.2% 且在上升），長期成長性與價值陷阱風險都屬中等。","governance":"現金轉換：前九個月營業現金流 131 億，PP&E 購置 481 億，自由現金流 −350 億。Q3 淨利 44 億高於 GAAP 營業利益 27.9 億，差額來自營業外項目，事實表未拆分，因此轉換率沒有參考價值。SBC：Q3 23.63 億，占營收 16.2%、占 GAAP 營業利益 84.7%。現金去向四分：資本支出（Q3 196 億，其中 SI 164 億、Connectivity 15.4 億、Space 16.1 億）遠大於併購（Cursor 全股票 600 億、發行 3.89 億股；Q1 xAI 合併時回購員工股 24.13 億）；股息與回購都是 0。資金來源：IPO 淨募資約 857 億，2026-06 發行 250 億優先無擔保債（票面利率 5.35%–6.65%）；目前總債務 397 億、現金 1,000 億。往後看：Q4 資本支出指引 350–400 億，而 Q2 法說時曾說未來兩季會和 Q2 的 184 億相近；S&P 預期 FCF 負到 2029 年。CFO 稱會靠營運現金流、債市與供應鏈夥伴融資，並維持投資級。","valuation":"前瞻 EV/S 41.7 倍（EV 1.89 兆÷FY2026 共識營收 453 億）；過去 12 個月 EV/S 81.9 倍、P/S 84.5 倍。若用 Q1 2027 指引年化約 1,400 億計算，EV/S 約 13.5 倍，但這正是分母的爭點。本益比沒有意義：FY2026 共識 EPS −0.09；用 FY2027 的 1.93 算，前瞻本益比約 77 倍。五年分位：2026-06 才上市，事實表只有 3 個年度端點，不算五年分位。PEG：基期 EPS 為負，無法計算。12 個月：以 FY2028 Base 營收 2,100 億×9 倍 EV/S、淨負債約 300 億、股數約 135 億推算，約 138 美元，約 −7%；五年 Base 約 128 美元，約 −13%。賣方：MarketBeat 平均目標價 221.2 美元（區間 75–800，最高與最低相差逾 10 倍），StockHub 報導共識由 225 降到 202；區間太寬，不拿來當支撐。","premortem":"壓力測試：假設 2029 年後營收年增降到 15%／10%／5%，EV/S 同步壓到 6／5／4 倍，淨負債 1,500 億、股數 143 億，推出每股約 131／97／68 美元，三個都低於現價，0／3 通過；10% 情境的 97 美元可當 Bear 倍數的對照錨。空方最強的數字：GLJ 指出 Q2 自由現金流燒掉約 159.5 億、銷售倍數約 77 倍；S&P 預期 FCF 負到 2029 年；大摩估 2035 年前沒有自由現金流為正的年度。FY2026 共識 EPS 近三個月由 0.20 下修到 −0.09，發生在 Q3 財報前；Q3 單季 0.35 美元可能讓下修反轉，待確認。管理層承諾的兌現紀錄：算力建置按時（Q2 說年底超過 2 GW，10 月底已約 2.2 GW），營收連兩季超預期；但 Starship 時程（Q2 說一年內每天一飛，Q3 改為 2027 上半年每週一飛）與 Starlink Mobile 開通時間（Q2 說 2027 年底，Q3 改為 2028 年初）都延後。法說迴避的問題：Q2 迴避 Mobile 資本支出數字與 10 GW 把握度；Q3 改說有把握新增 10 GW，但拒談供電計畫細節（稱高度專有）與晶片突破。歷史最大回撤：2026-06 才上市，事實表未涵蓋完整的回撤序列。"},"plain":{"six":{"how_it_makes_money":"公司賺三份錢。第一份是 AI 算力租賃與 Grok／Cursor 軟體（SI），Q3 營收 75.6 億美元，占 52%。第二份是 Starlink 訂閱（Connectivity），營收 52.5 億、營業利益 23.7 億，是全公司最穩的利潤來源。第三份是發射（Space），約 17.7 億。關鍵在算力的每瓦租金：SI 營收大多來自半年期、按現貨價續約的合約，公司是排在晶片供應商下游的租賃方。","moat":"護城河方向持平（→）。發射成本與頻次的領先仍在擴大，但最大客戶美國國防部已把國安發射名單擴到七家，New Glenn 也拿到國安合約，定價力只能算穩定。AI 算力段沒有結構性護城河，只有建置速度。","growth":"五年後成長空間仍寬（🟢）。Starlink 消費者 1,360 萬戶、進入 174 個市場，滲透率仍低。第二、三條成長曲線已有具體證據：FCC 核准 15,000 顆 Mobile V2，公司也買入低頻頻譜（2028 年初開通）；名牌算力由 1.7 GW 往 2027 年底 13 GW 擴（管理層目標）。但這是外部資金堆出來的成長：增速遠超自籌內生上限約 16%，差額全靠外部融資。","capital":"資本配置偏弱。前九個月自由現金流 −350 億美元，Q3 SBC 占營收 16.2%，三項評分（併購報酬、回購收益率、SBC 稀釋）無一通過。好的一面是手上淨現金約 603 億，三家評等機構都給投資級。","valuation":"現價需要比 Base 情境再好一點：Base 假設 2031 年營收約 3,300 億美元、給 6 倍 EV/S，推出每股約 128 美元，仍低於現價 147.79 美元。我相信營收方向向上，但不相信半年期現貨合約撐得起這個倍數，估值偏貴。","how_wrong":"最可能看錯的方向是太保守：如果算力租金真如管理層所說只升不降，2027 年底 13 GW 全數變現，營收會遠超 Bull 路徑。反方向的錯誤是低估了供給追上時，半年期合約重新定價的速度。價值陷阱風險中等（🟡）。"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Q1 2027 年化約 1,400 億美元營收當成可延續的基期，但這批營收多半來自約半年期、按現貨價續約的算力合約，而 Q4 資本支出已升到 350–400 億美元；市場沒有為年化值能維持多久打折","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"股價 ≤95 美元；或 Q1 2027 營收 ≥350 億且續約每瓦單價不降後，股價 ≤125 美元；Tesla 合併條款公布前不建倉","qc48_result":"fail","qc48_note":"Bull 情境缺少「瓦數 × 每瓦租金 → 營收 → EPS」的算術，歷史上高估值高成長的可比案例（Cisco）報酬遠低於 Bull 隱含的年化 21.6%，五年成長跑道的「滲透率低」與 FCC 核准也沒有可回溯的來源，因此 Bull 依據目前不成立。","trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"未獲利高成長","price_at_dd":147.79,"week26_return_pct":-8.07,"consensus_rev_3m_pct":-145.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"前瞻營收這個分母本身就是爭點。FY2026 共識 453 億美元是在 Q3 財報前擬定的；Q1 2027 指引 330–370 億，年化約 1,400 億，會讓 EV/S 降到約 13.5 倍。但這批營收大多來自約半年期、按現貨價續約的雲服務合約，年化值能否延續正是多空分歧所在，所以不拿年化營收來論證便宜。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Starship Flight 15 嘗試讓一、二級都由塔架回收","impact":"中","watch":"成功的話，2027 上半年每週一飛的時程可信度上升；失敗只會延後 Starlink V3 部署，不影響算力營收"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報：12 月年化營收是否達 1,000 億、Q4 資本支出是否落在 350–400 億","impact":"高","watch":"資本支出超過 400 億，或年化營收不到 1,000 億，就下調 Bull 機率"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"Q1 2027 財報：營收對比 330–370 億指引","impact":"高","watch":"這是 Single Thing 的檢驗點；營收 ≥350 億且續約價不降，才考慮建首倉"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"V3 衛星達數百顆，使用者感受到速度提升（Shotwell 說法）","impact":"中","watch":"Q2 法說原本說需要約 1,000 顆，門檻已被改低；要看實際速度與 ARPU"},{"date":"2028-03","date_precision":"quarter","type":"product","event":"Starlink Mobile 以自有頻譜開通服務","impact":"中","watch":"已由 2027 年底延到 2028 年初；若再延，Mobile 營收就移出五年情境"},{"date":null,"date_precision":null,"type":"other","event":"SpaceX 與 Tesla 的特別委員會是否就合併條款達成協議","impact":"高","watch":"條款公布前不建倉；換股比例決定每股被稀釋多少"}],"_projected_from":"v19"}
```
