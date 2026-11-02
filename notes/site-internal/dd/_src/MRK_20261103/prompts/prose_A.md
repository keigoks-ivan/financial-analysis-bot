你是 stock-analyst v20 的**散文層（prose）agent**，標的 MRK（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MRK　日期：2026-11-03　archetype：None　前份裁決：2026-09-29　迴避｜不持有　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1894B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（779B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（868B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1141B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1239B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（867B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1244B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2068B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1259B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3126B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1894           3574-5106      5 條（2–6 內）  
s3                  8000         779           5055-7221      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3248          8226-11752      5 條（2–6 內）  
s6                 11000         867          7093-10133      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1244           1579-2256      3 條（2–6 內）  
s10                 5000        2068           2052-2932      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3126           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5155B；至少需散文≈39.84KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−48%
−45%
−35%
−35
−13%
−10%
−8.9%
−7.7%
−7.6%
−5.8%
−5.8
−4.1
−4.1%
−2.6%
−1.2%
−1.0%
−0.1%
0%
0.0
0.1%
0.1
0.12
0.2
0.33%
0.5
0.65
0.68
0.75
0.78%
0.8%
0.87%
0.98%
001
1
01
1.01
1.06
1.1
1.2
1.3
1.52
1.79%
1.79
1.84
1.87
02
2%
2
2.29
2.29%
2.31
2.43
2.49
2.5
2.63
2.65
2.66
2.72
2.76
2.77
2.82
2.98
3
03
3%
3.07
3.3%
3.5
3.65
4%
04
4
5
5%
005
5.44
5.5
6%
6
06
6.13
6.2%
6.5
6.94
7
7.1
7.28
7.4
7.6
08
8
8.3
8.5
8.6
8.7
8.8
8.9
8.93
8.95
09
9
9%
9.1
9.14
9.2
9.3
9.5
10.0
10%
10
10.12
10.2
10.4
10.7%
10.8
11
11%
11.5
11.6%
12
12%
12.6
13
13%
13.1
14%
14
14.7
15%
15
16
16.25
16.9
17
17.25%
17.35%
18%
18.7%
18.72%
20%
20
21.5
21.6
22
23
24
25
26
26.72%
28.28%
29
29.19%
30
30%
31
32
33%
33.08%
33.94%
34%
34.01%
35%
35
35.66
36%
38
40
40%
41%
42%
44.77
45%
48%
49
50
53.19%
54%
54.6
57
58%
60%
67
68
70
71.4
74
78
80%
81%
81
81.1%
81.4%
81.4
83.6
84
86
94%
95%
96
100%
119
120
123.6
134.56
140
142.5
148.56
148.69
150
164.0
166.07
181
181.0
182.5
198.4
214
214.2
224
232
250
333
467.7
539.1
637
670.5
700
738.7
2010
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
2033
20261103
2,452.5
3,665
4,132.8
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
{"meta":{"ticker":"MRK","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Merck & Co., Inc."},"oneliner":"Keytruda 專利到期前的換軌期：三期讀數與新藥放量都好，但現價約 FY2027 共識 16 倍、Base 五年年化不到 2%；等 Qlex 與新品放量、且股價落到 FY2027 共識 13 倍以下再重新研究","thesis":{"H":[{"id":"H1","text":"新藥組合在 Keytruda 美國專利到期前放量到足以接棒：Qlex、Winrevair、Capvaxive、Enflonsia、Ohtuvayre、Lipfendra 合計單季營收由 2026Q3 約 21.6 億美元（不含未揭露的 Lipfendra）升到 2027Q4 ≥25 億美元","2y":"2027Q4 新品組合單季 ≥25 億美元（扣除進貨時點效益）","5y":null,"10y":null,"threshold":"2027Q4 單季 ≥25 億美元","source":"公司季度新聞稿與法說的產品營收","drift_rule":"以四季合計對比路徑：連 2 季落後 ≥5% 視為削弱，連 3 季落後 ≥10% 視為反轉"},{"id":"H2","text":"Qlex 皮下劑型守住美國轉換：管理層目標 2027 年底美國採用 30–40%（Q3 法說 Jannie Oosthuizen），以 Qlex 單季 ≥12 億美元為代理門檻（美國占比事實表未涵蓋），且美國無禁制令","2y":"2027Q4 Qlex 單季 ≥12 億美元；美國無不利裁決","5y":null,"10y":null,"threshold":"2027Q4 Qlex 單季 ≥12 億美元","source":"季度新聞稿、法說、8-K 與 10-Q 訴訟附註","drift_rule":"連 2 季低於直線路徑（8.3 億→12 億）≥5% 視為削弱，連 3 季 ≥10% 視為反轉；美國出現禁制令即反轉"},{"id":"H3","text":"專利到期只是淺坑：FY2029 全年營收不低於 2026 年財測中點 670.5 億美元的 95%（約 637 億），FY2031 調整後 EPS 回到 ≥10 美元","2y":null,"5y":"FY2029 營收 ≥637 億美元；FY2031 EPS ≥10 美元","10y":"2030 年代中期營收 ≥700 億美元（CEO 2026-10-29 稱將上修此目標）","threshold":"FY2029 營收 ≥637 億美元","source":"年報 10-K 與年度財測；Koyfin 月度共識","drift_rule":"TTM 營收連 4 季落後路徑 ≥5% 視為削弱、連 6 季 ≥10% 視為反轉；10 年目標跨 2 個年度落後削弱、跨 3 個年度反轉"}],"R":[{"id":"R1","text":"2027 投資年讓 EPS 低於共識：營業費用中高個位數成長、超過 20 億美元學名藥逆風、利息與稅率上升（Q3 法說 CFO），且 CFO 說多數分析師尚未納入","h_ref":"H3","clock":"⚡","threshold":"FY2027 共識 EPS 在 2027-02 財報後降到 8.7 美元以下（較 9.14 低約 5%）","evidence_refs":[]},{"id":"R2","text":"Keytruda 防線被突破：美國核心專利 2028 年 12 月到期、Medicare 議價價格 2028-01 生效，生物相似藥（Cipla／Qilu QL2107）卡位，Qlex 在歐洲 6 國遭禁制令，參議員質詢劑型轉換策略","h_ref":"H2","clock":"🔥","threshold":"Keytruda 家族單季年增率連 2 季 < 0%（2028 年前），或美國出現 Qlex 不利裁決","evidence_refs":["supply_demand_durability#2","end_markets#5","substitute_technology#3","regulatory_antitrust#0"]},{"id":"R3","text":"PD-1×VEGF 雙特異抗體取代 pembrolizumab 成為免疫治療骨幹：ivonescimab 在肺癌頭對頭試驗擊敗 Keytruda，Crescent CR-001 2026 年進臨床；Merck 自有 MK-2010 的三期 2027 上半年才啟動","h_ref":"H3","clock":"🐢","threshold":"任一 PD-1×VEGF 在全球（非僅中國）三期頭對頭勝過 Keytruda 的整體存活","evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"id":"R4","text":"疫苗需求結構性走弱：Gardasil 中國停貨、本土競品十分之一價格、日本需求下滑，美國疫苗猶豫（Capvaxive 美國 −13%）；Q3 Gardasil +14% 含 CDC 採購與 3 億美元時點效益，其中 2.5 億在 2027 年回吐","h_ref":"H3","clock":"🔥","threshold":"Gardasil 美國以外單季營收年增率連 2 季 < −10%","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#0","supply_demand_durability#1","end_markets#1","end_markets#2"]},{"id":"R5","text":"美國藥價與貿易政策壓縮定價：IRA 議價（Januvia／Janumet 已入選，Merck 提告違憲）、MFN 協議與直售病人平價方案、Section 232 專利藥最高 100% 關稅（Merck 以美國投資換三年延後）、德國政策","h_ref":"H3","clock":"🔥","threshold":"全年調整後毛利率 < 80%（2026 財測約 81%），或公司揭露政策造成的年度營收衝擊 > 20 億美元","evidence_refs":["regulatory_antitrust#3","reg_tariff_export#1"]},{"id":"R6","text":"中國來源管線的地緣風險：sac-TMT（Kelun）與 MK-2010（LaNova）皆授權自中國，眾議院中國特別委員會調查 Merck 在中國的 224 項臨床研究（至少 31 項在新疆、40 項在解放軍附屬醫院），CEO 公開警告限制美中交易的後果","h_ref":"H3","clock":"🐢","threshold":"美國立法或行政命令限制使用中國臨床數據申報，或限制中國授權資產","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R7","text":"訴訟與調查：DOJ 依《虛假申報法》調查 Steglatro／Januvia 的 Medicaid 回扣價格申報（2024-06 起）、巴爾的摩市 RotaTeq 反壟斷集體訴訟、Cronin 證券集體訴訟（Gardasil 中國需求陳述）及兩件衍生訴訟","h_ref":null,"clock":"🐢","threshold":"任一案揭露和解或罰款 > 10 億美元，或證券訴訟駁回動議被否決、進入證據開示","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]}],"single_thing":{"description":"美國法院或主管機關對 Keytruda Qlex 的透明質酸酶智財作出不利 Merck 的裁決或禁制令，Qlex 無法在美國續售","why_fatal":"Keytruda 美國專利到期後的留存率是情境樹最大的敏感項，Qlex 是其中唯一可二元判定的節點：它是 2028 年 12 月核心專利到期後不受 IV 生物相似藥直接替代的劑型，管理層目標 2027 年底美國轉換 30–40%。Qlex 若被擋，這部分營收在 2029 年也暴露在生物相似藥下，淺坑假設的主要支柱消失","if_happens":"Base 改走 Bear：FY2031 EPS 由 10.0 降向 7.4 美元，Bear 機率上調到 40%，取消重跑研究條件 12 個月","how_monitor":"荷蘭聽證判決（歐洲 6 國停供，日期事實表未涵蓋）作為先行指標；公司 8-K 與 10-Q 訴訟附註；Qlex 單季營收","probability":"12–24 個月約 10%：管理層稱有自由實施的智財、美國目前無禁制令；但荷蘭已核發暫時禁制令，故不低於 5%"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.25,"peg_fy2":1.52,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":7.28,"FY2026E":2.72,"FY2027E":9.14,"FY2028E":10.12},"fy_end_month":12,"eps_basis":"共識為 Koyfin 調整後 EPS（FY2026E 2.72 含收購研發一次性費用）；FY2025A 用事實表唯一可得的 GAAP 稀釋 EPS 7.28，與調整後口徑不同，三年年複合約 11.6% 因此高估真實成長"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"高毛利專利藥＋單一大藥專利到期前的換軌期"},"industry":{"clock_phase":"III","sd_verdict_source":"需求面結構性持久（PD-1/PD-L1 市場 2026 年約 738.7 億美元、預估年複合 18.7%），但 Merck 能分到多少由專利時程決定，屬時程明確的結構性下行，不是週期","bargaining":{"up":"上游原料與代工不是瓶頸；供應商集中度事實表未涵蓋","down":"美國三大批發商占應收約 54%（2022 年資料）只是物流通路，真正的定價方是 Medicare、商業保險與 PBM；2026-02 與政府的 MFN 協議與直售病人平價方案進一步壓縮定價","geo":"中國：Gardasil 需求崩落、本土 HPV 疫苗以十分之一價格競爭，眾議院調查 Merck 在中國的臨床試驗；美國：Section 232 專利藥關稅以美國投資換三年延後"},"profit_pool_dir":"PD-1 利潤池仍在擴大，但 2028 年後從原廠單抗流向生物相似藥、付款方與 PD-1×VEGF 雙特異抗體新進者","tam_table":[{"item":"PD-1/PD-L1 全球市場","value":"2026E 約 738.7 億美元，預估 2033 年 2,452.5 億美元、年複合 18.7%（Future Market Insights）"},{"item":"Keytruda 家族份額","value":"2026 年上半年 164.0 億＋Q3 86 億美元，年化約 333 億，約占 2026E 市場 45%"},{"item":"主要對手","value":"Opdivo 2026Q1 21.5 億美元（年減 5%）；Imfinzi 2026Q1 16.9 億美元（年增 30%）"},{"item":"利潤池遷移","value":"2028-01 Medicare 議價價格生效、2028-12 美國核心專利到期；雙特異抗體爭奪下一代骨幹"},{"item":"營業利益池 5 年前→現占比","value":"事實表未涵蓋，無法判定是否淨流出 5 個百分點以上"}]},"moat":{"mechanism":"專利保護的生物藥＋腫瘤科商業規模＋以 Keytruda 為骨幹的組合開發能力（sac-TMT、intismeran、calderasib 都設計成與 Keytruda 併用或取代化療組合）","execution":7,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"定價權縮減：Keytruda 2028-01 Medicare 議價價格生效、2028-12 美國核心專利到期；Qlex 遭荷蘭法院禁制令，歐洲 6 國停供；德國政策與美國以外價格逆風（Q3 法說）；Gardasil 中國面對十分之一價格的本土疫苗。執行力穩定：Winrevair 年增 94%、Qlex 單季 8.3 億美元、sac-TMT 與 intismeran 三期正向，但也有撤件與失敗","peer_na_reason":"事實表未涵蓋投入資本，無法算同業 ROIC 差；改用營業利益率與 FCF 利潤率對照，且 MRK TTM 營業利益率 0.87% 被收購研發費用扭曲，以 FY2025 的 34.01% 代替","threats":[{"level":"🔴","text":"PD-1×VEGF 雙特異抗體攻擊 pembrolizumab 的骨幹地位（ivonescimab 頭對頭勝出、Crescent CR-001 進臨床）；Merck 以自有 MK-2010 對沖，所以列為生態攻擊而非架構替代","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"level":"🟡","text":"生物相似藥卡位（Cipla 取得 Qilu QL2107 美國權利）與 2028 年 12 月美國核心專利到期：時程已知的點對點替代，已放進各情境","p":"時程確定","evidence_refs":["substitute_technology#3","supply_demand_durability#2"]},{"level":"🟡","text":"Gardasil 在中國面對十分之一價格的本土 HPV 疫苗","p":"已發生","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"Opdivo 皮下劑型早 9 個月上市、Imfinzi 年增 30%：份額端的點對點競爭","p":40,"evidence_refs":["competitive_share_entrants#3"]}],"roic_durability":{"quadrant":"高利益率×低周轉（投入資本事實表未涵蓋，依 FY2025 營業利益率 34.01% 與大量收購無形資產定性判斷）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是病人、決策者是腫瘤科醫師、付款者是 Medicare 與保險，三角色都成立；癌症治療是需要不是想要，延後的代價是存活。PD-1 市場 2026 年約 738.7 億美元、預估年複合 18.7%。但要解決的問題（免疫治療）會持續，公司目前的解法（pembrolizumab 單抗）不一定"},{"item":"決策層級","level":"🟡","text":"決策最小單位是治療指引與醫院處方集，生物相似藥上市後處方集可整批切換；Qlex 自 2026-04-01 取得永久給付代碼，改變給藥流程形成轉換成本，管理層目標 2027 年底美國轉換 30–40%，但 IV 版本在 2028 年後替代性很高"},{"item":"價值鏈分配","level":"🟡","text":"專利期內價值集中在原廠（調整後毛利率約 81%）；2028 年起 Medicare 議價生效、核心專利到期，價值移向付款方與生物相似藥廠；MFN 協議與直售平價方案再讓一段給付款端。新藥（Winrevair、sac-TMT）各自重建定價空間"},{"item":"社會容忍度","level":"🔴","text":"高必要×高敏感：參議員 Hassan 質詢 Keytruda 專利策略與劑型轉換延遲低價競爭；IRA 議價（Januvia／Janumet 已入選，Merck 提告違憲）；與政府的 MFN 協議與直售平價方案；德國政策逆風。實際定價上限已由政治上限決定"}],"roiic":"無法以實現值計算：投入資本與 2023–2025 收購總額事實表未涵蓋；可見增量為 2022→2025 營業利益增加約 38 億美元。判斷假設取約 10%","reinvest_rate":"約 40%（2026 年單年下限）","endo_ceiling":4.0,"formula_note":"內生成長上界＝增量報酬 × 再投資率＝約 10% × 約 40% ≈ 4%。增量報酬取約 10%：收購資產多數尚未上市、報酬未實現，不給高於資金成本太多的假設；再投資率約 40%：2026 年可見收購與授權至少約 78 億美元（Terns 約 67、TARGAN 約 6.5、SciBrunch 預付 4 億）÷ FY2025 淨利 182.5 億美元，Cidara 金額未涵蓋，實際更高。兩者都是判斷假設，不是已實現數字"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","MRK":71.31,"PFE":73.18,"BMY":69.24,"ABBV":71.48,"unit":"%"},{"metric":"營業利益率","MRK":0.87,"PFE":26.72,"BMY":29.19,"ABBV":33.94,"unit":"%"},{"metric":"FCF 利潤率","MRK":18.72,"PFE":17.25,"BMY":18.56,"ABBV":28.28,"unit":"%"},{"metric":"研發密度","MRK":53.19,"PFE":17.35,"BMY":21.1,"ABBV":15.09,"unit":"%"}],"competitors":[{"name":"PFE","gm":73.18,"om":26.72,"fcf_margin":17.25,"rd_intensity":17.35,"strategy_note":"營業利益率 26.72%、FCF 利潤率 17.25%、研發密度 17.35%；同樣處於專利到期期，不是 PD-1 直接對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BMY","gm":69.24,"om":29.19,"fcf_margin":18.56,"rd_intensity":21.1,"strategy_note":"Opdivo 2026Q1 年減 5%，皮下劑型雖早 9 個月上市仍追不上 Keytruda；營業利益率 29.19%","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ABBV","gm":71.48,"om":33.94,"fcf_margin":28.28,"rd_intensity":15.09,"strategy_note":"營業利益率 33.94%、FCF 利潤率 28.28% 皆為同業最高，現金創造力優於 Merck；不在 PD-1 戰場","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主：新藥放量與併購帶入的管線；價格面受 Medicare 議價、MFN 與美國以外降價壓制；回購每年約 30 億美元、約占市值 0.8%","runway_years":"不適用：Keytruda 已在多個適應症接近滲透高峰；新藥各適應症滲透率事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：內生成長上界約 4%（增量報酬約 10% × 再投資率約 40%）。三年共識 EPS 以 FY2025 GAAP 7.28 美元為基期、到 FY2028E 10.12 美元，年複合約 11.6%，缺口約 7.6 個百分點：①基期是 GAAP、共識是調整後口徑，部分是口徑差而非真成長；②2027 年 Keytruda 權利金到期帶動毛利率上升（利潤率擴張）；③舉債收購帶入的新藥（收購）。剩餘部分無法歸因、依賴重新評價","segments":[{"item":"Keytruda 家族（2026Q3）","value":"86 億美元、年增 6%，約占營收 48%；含 Qlex 8.3 億"},{"item":"Gardasil（2026Q3）","value":"20 億美元、年增 14%（美國 +18% 含 CDC 採購，國際 +6%）；上半年年減 9%"},{"item":"Winrevair（2026Q3）","value":"6.94 億美元、年增 94%（含約 0.5 億進貨時點效益）"},{"item":"Welireg（2026Q3）","value":"3.07 億美元、年增 58%"},{"item":"Capvaxive／Enflonsia／Ohtuvayre（2026Q3）","value":"2.63 億（美國 −13%）／1.87 億／1.84 億美元"},{"item":"動物保健","value":"2026Q3 年增 3%；上半年 35.66 億美元、年增 10%"},{"item":"2027 年專利到期逆風","value":"Bridion、Januvia 家族、Adempas 合計超過 20 億美元（Q3 法說 CFO）"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"note":"Q2 調整後毛利率 81.1%、年減 1.1 個百分點；Q3 81.4%、小幅下降"},{"signal":"核心市占近 12 個月縮減","lit":null,"note":"事實表未涵蓋份額數據；Keytruda 仍成長但 Imfinzi 成長更快"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"未見證據"},{"signal":"EPS 年複合高於營收年複合 5 個百分點以上","lit":null,"note":"FY2025 基期口徑不一、FY2028 共識營收未涵蓋，無法判定"},{"signal":"FCF/NI 連 2 年低於 0.75","lit":false,"note":"FY2024 1.06、FY2025 0.68，只有 1 年"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"1.79%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"note":"PD-1×VEGF 雙特異抗體頭對頭勝過 Keytruda；Gardasil 中國市場萎縮"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"Q2 資本支出 8.93 億美元、FCF 44.77 億"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"在美國增加製造投資；營收 2022–2025 年持續成長"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"股息","value":"殖利率 2.29%，以市值 3,665 億美元換算約 84 億美元／年；管理層承諾逐步調升"},{"item":"回購","value":"2026 年約 30 億美元（Q2、Q3 法說），約占市值 0.8%"},{"item":"收購與授權（2026）","value":"Terns 約 67 億（申報總額 68 億，認列 57 億研發費用）、TARGAN 約 6.5 億、SciBrunch 預付 4 億美元；Cidara 金額事實表未涵蓋"},{"item":"自由現金流","value":"FY2025 123.6 億美元、FY2024 181.0 億；2026Q2 單季 44.77 億"},{"item":"淨負債","value":"467.7 億美元（總債務 539.1 億、現金 71.4 億）"}],"sbc":{"pct_rev":1.79,"note":"2026Q2 單季 2.98 億美元"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2026 年收購 Terns 約 67 億、TARGAN 約 6.5 億、SciBrunch 預付 4 億美元，資產多未上市；2022→2025 營業利益只增加約 38 億美元，收購報酬尚未實現","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"買入收益率約 6.2%（FY2027 共識 9.14 ÷ 148.56）；十年期殖利率事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 單季 2.98 億美元、年化約 12 億，約占市值 0.33%／年，回購抵銷後為淨減少","grade":"過"}]},"valuation":{"basis":"前瞻一年本益比（FY2027 共識 9.14 美元）；FY2026 共識被收購研發費用壓低，trailing 150 倍與 FY2026 前瞻 54.6 倍皆不可用","tier":"大型專利藥廠","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率與研發密度，未涵蓋同業前瞻本益比，無法做倍數對照；終端倍數改以自身前瞻倍數與重新進場價位校準"},"fwd_pe":16.25,"peg":1.52,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 16.25 倍（FY2027）、14.7 倍（FY2028）；P/S 5.44 倍與 EV/S 6.13 倍在可得四個年度端點中最高，真五年分位事實表未涵蓋。PEG 1.52 以 FY2027→FY2028 共識成長 10.7% 計，若改用 Base 路徑約 2% 年成長則遠高於 2。短期（12 個月）以 FY2028E Base 9.5 美元 × 15 倍約 142.5 美元、−4.1%；中期（5 年）Base 140 美元、−5.8%，結論偏貴","upside_short_pct":-4.1,"upside_mid_pct":-5.8},"trap_analysis":{"verdict":"🟡","label":"Keytruda 專利到期前的換軌風險；衰退訊號亮 2 個（毛利率連 2 季年減、替代技術壓縮）"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Keytruda 逾 250 億美元年營收的美國核心專利 2028 年到期、Medicare 議價價格 2028-01 生效；ivonescimab 已在肺癌頭對頭試驗勝過 Keytruda","assumption":"多頭假設 Qlex 轉換加上新藥，能讓營收只出現淺坑","consequence":"若美國 Keytruda 在 2029–2030 年流失過半、Qlex 又被擋，FY2031 EPS 約 7.4 美元、11 倍約 81 美元（−45%）；低谷年倍數壓到 9.5 倍時可見 67 美元","ruling":"採納，列為 Bear 30%。與 Single Thing 部分重疊：美國 Qlex 裁決只是其中一條失敗路徑，雙特異抗體取代與 Medicare 議價不需要任何裁決也會發生，所以保留為獨立反證","watch":"Keytruda 家族單季年增率、Qlex 營收與美國訴訟、全球 PD-1×VEGF 三期讀數","evidence_refs":["supply_demand_durability#2","end_markets#5","substitute_technology#0"],"fact_refs":["f_price_at_dd"]},{"view":"論點成功但股東經濟變差","evidence":"接棒靠舉債併購與授權：2026 年 Terns 約 67 億、TARGAN 約 6.5 億、SciBrunch 預付 4 億美元，淨負債 467.7 億美元；CFO 預告 2027 年營業費用中高個位數成長、利息與稅率上升。社會容忍度偏低：參議員質詢 Keytruda 專利策略，IRA 議價與 MFN 直售平價方案壓定價","assumption":"營收補回來，利潤率與每股盈餘就會跟著回來","consequence":"營收守住但營業利益率從 FY2025 的 34% 往下走、每股盈餘成長落後營收；收購研發費用年年出現，調整後 EPS 高估真實盈餘","ruling":"採納：Base 情境 EPS 比共識低 2–6%（FY2027 8.95 對 9.14、FY2028 9.5 對 10.12）","watch":"調整後營業費用年增率對營收年增率；每年收購研發費用；淨負債變化","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#3"],"fact_refs":["f_net_debt_m","f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"價格已反映太多","evidence":"26 週上漲 33.08%；P/S 5.44 倍、EV/S 6.13 倍在可得四個年度端點中都是最高；FY2027 前瞻本益比 16.25 倍；8 月初賣方平均目標價約 134.56 美元，低於現價約 9%；FY2027／FY2028 共識近期各下修 0.98%／0.78%","assumption":"三期成功等於商業成功，且 2027 共識不再下修","consequence":"即使論點成立，Base 五年年化報酬不到 2%。共識小幅下修時 Bear 錨不依賴共識、暫時平穩；但若 FY2027 共識持續下修，正向不對稱的數字不能當進場依據","ruling":"採納：不追，等股價落到 FY2027 共識 13 倍以下並看到放量","watch":"FY2027 共識 EPS 月度變化；股價 ÷ FY2027 共識","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_ps_current","f_ev_s_current","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 148.69 → 本次 148.56（-0.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=148.69","side_b":"本次 price_at_dd=148.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 148.69 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 148.69 美元：Bull 價 198.4、Bear 價 83.6，五年期望值 −8.9%，基準年化 −1.0%，不對稱比 0.5","side_b":"本次情境、股價仍用 148.69 美元：Bull 價 214.2、Bear 價 81.4，五年期望值 −7.7%，基準年化 −1.2%，不對稱比 0.65","ruling":"先換情境、股價不動：五年期望值多 1.2 個百分點，基準年化少 0.2 個百分點。不對稱比由 0.5 變為 0.65。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 148.69 美元：五年期望值 −7.7%，基準年化 −1.2%，不對稱比 0.65","side_b":"本次情境、股價 148.56 美元：五年期望值 −7.6%，基準年化 −1.2%，不對稱比 0.65","ruling":"再換股價、情境不動：起點價下跌 0.1%，五年期望值多 0.1 個百分點，基準年化多 0.0 個百分點，不對稱比由 0.65 升到 0.65。合計五年期望值比前份多 1.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層淺坑說對上 2027 投資年與專利到期規模","cause":null,"side_a":"CEO（2026-08-04）稱專利到期期間是「小山不是懸崖」、淺幅下滑後快速回到成長；CFO（2026-10-29）稱接近專利到期時盈餘會成長、營收淺坑後很快回升","side_b":"同一場 CFO 也說 2027 年營收只溫和成長、超過 20 億美元學名藥逆風、營業費用中高個位數成長，多數分析師尚未納入；Keytruda 逾 250 億美元年營收 2028 年起受專利與 Medicare 議價夾擊；FY2027／FY2028 共識近期已小幅下修","ruling":"可調和（程度差異）：方向上同意會回到成長，但幅度與時點採較保守的 Base：FY2027 EPS 8.95 美元（共識 9.14）、FY2029 低點 8.9 美元","evidence_level":"管理層陳述＋共識快照（中）","settle_metric":"2027-02 財報給的 2027 年 EPS 財測中點對 9.14 美元","if_then":["若 2027 年 EPS 財測中點 ≥9.1 美元且營業費用成長 ≤5% → Base FY2027 上修到 9.1，重跑情境樹","若財測中點 < 8.8 美元 → 維持不追，Bear 機率上調到 35%","反向條件：若財測高於共識但股價同步漲到 FY2027 的 17 倍以上 → 仍不追"],"evidence_refs":["end_markets#5"]},{"axis":"Q3 上修財測的品質","cause":null,"side_a":"2026 年 EPS 財測由 2.66–2.76 上修到 2.77–2.82 美元，高於當時共識 2.65","side_b":"Q3 營收含約 5.5 億美元美國進貨時點效益：Keytruda 2 億、Winrevair 0.5 億於 Q4 回吐，疫苗 3 億中 2.5 億在 2027 年回吐；全年稅率由 35–36% 降到 32–33% 也有貢獻","ruling":"可調和：上修屬實，但部分來自時點與稅率，不改變 2027 年判斷","evidence_level":"法說與新聞稿（高）","settle_metric":"2026Q4 Keytruda 家族營收扣除 2 億回吐後的年增率","if_then":["若扣除回吐後年增 ≥4% → H2 路徑不變","若 < 2% → R1 升級，Base FY2027 EPS 下修到 8.8 美元"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"ESMO 兩個三期正向（TroFuse-005 降低進展或死亡風險 41%、INTerpath-001 降低復發或死亡風險 42%），sac-TMT PDUFA 2027-06-15；Winrevair 單季 6.94 億美元、年增 94%；CEO 說 700 億美元中期目標將上修；FY2028 共識本益比約 14.7 倍、股息殖利率 2.29%","side_b":"這些成功多數 2028 年後才貢獻，且部分已在 26 週 33% 漲幅中；Base 五年年化不到 2%；Qlex 歐洲禁制令與美國訴訟、Lipfendra 醫保覆蓋要到 2027–2028 年","ruling":"不採納買進。約束條件有兩個：價格（Base 年化不到 2%）與接棒證據（新品組合尚未到 25 億美元），三項重新進場條件需同時成立","evidence_level":"公司發布＋法說（高）","settle_metric":"股價 ÷ FY2027 共識 EPS；新品組合單季營收","if_then":["若股價 ≤119 美元但新品組合未達 25 億 → 不建倉，等放量；分批反買只在重跑研究通過後","若新品組合 ≥25 億且 Qlex ≥12 億但股價仍 ≥140 美元 → 不追（價格先走）"],"evidence_refs":["major_events#2","clinical_fda#0"]},{"axis":"Qlex 智財：管理層說無影響，對上禁制令與國會質詢","cause":null,"side_a":"CEO：有自由實施的智財，荷蘭禁制令只是聽證前的暫時措施；歐洲 6 國停供屬小量市場（Q3 法說）","side_b":"禁制令已生效；分析師直接追問美國是否有風險；參議員 Hassan 質詢 Keytruda 以劑型轉換延遲低價競爭","ruling":"不可裁決至荷蘭聽證結果出爐（日期事實表未涵蓋）；維持把美國 Qlex 裁決設為唯一致命點","evidence_level":"法說陳述（中）","settle_metric":"荷蘭聽證判決；美國是否出現同類禁制令","if_then":["若荷蘭聽證推翻禁制令 → 唯一致命點機率由約 10% 下修到 5%","若美國出現禁制令申請或不利裁決 → Bear 機率上調到 40%，取消重跑研究條件 12 個月"],"evidence_refs":["regulatory_antitrust#0","substitute_technology#3"]},{"axis":"前份至今股價幾乎不動，估值結論、裁決與機率不因價格改變","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-09-29：估值偏貴、迴避、不持有；Bull 20%、Bear 30%","side_b":"本次：股價 148.69→148.56 美元（−0.1%）；估值仍偏貴（FY2027 前瞻 16.25 倍）；機率維持 20／50／30","ruling":"價格沒有帶來新的安全邊際；三期正向讀數（加分）與 2027 投資年訊息（減分）相互抵銷，機率不動","evidence_level":"價格與共識快照（高）","settle_metric":"股價 ÷ FY2027 共識 EPS","if_then":["若股價 ÷ FY2027 共識 ≤13 倍且放量條件成立 → 重跑研究","若股價續漲到 17 倍以上而放量未到 → 不追"]},{"axis":"Q3 財報與 ESMO 讀數檢視後，護城河方向、陷阱風險、五年後跑道與訊號維持","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5","signal"],"side_a":"前份：護城河縮減、陷阱風險中、五年後跑道中、訊號 C","side_b":"本次維持同樣四個結論。加分：TroFuse-005 降低進展或死亡風險 41%、INTerpath-001 降低復發或死亡風險 42%、CEO 稱 700 億美元目標將上修、Winrevair 年增 94%。減分：Qlex 在歐洲 6 國遭禁制令停供、2027 年超過 20 億美元學名藥逆風、德國政策與美國以外價格逆風、I-DXd 撤回加速核准申請","ruling":"正負相抵。700 億美元的 2030 年代中期目標相對 2026 年財測中點 670.5 億只是持平，第二曲線不足以把跑道升為寬；定價權仍在收縮，護城河方向不變","evidence_level":"公司法說與投資人日（高）","settle_metric":"新品組合單季營收、Keytruda 家族年增率","evidence_refs":["clinical_fda#0","major_events#2"]},{"axis":"最大回撤改用範圍推導；型態與循環位置維持","cause":"方法變動","prior_field":["max_dd_pct","archetype","cycle_position"],"side_a":"前份最大回撤 −48%（單點）；型態品質複利成長；循環位置未設","side_b":"本次最大回撤 −35%～−55%，由 Base 與 Bear 路徑低谷年 EPS × 低谷倍數推出；型態維持品質複利成長（副型態轉機／特殊情境）；非循環股，循環位置不適用","ruling":"範圍比單點更能反映專利到期當年的倍數壓縮；型態不變，因為毛利率、現金創造與股息紀錄仍是品質股的樣子，換軌風險放在副型態與反證處理"},{"axis":"重新進場研究門檻：價格條件改為倍數錨，並明列新品組合","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤120 美元（約 FY2027 共識 12.6 倍）","side_b":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤FY2027 共識 EPS 的 13 倍（以 9.14 計約 119 美元）","ruling":"固定 120 美元改為 FY2027 共識 13 倍：CFO 2026-10-29 說多數分析師尚未納入 2027 投資年訊息，共識下修時固定價位等於放寬門檻；前份 120 美元換算 12.6 倍與目前共識 9.14 美元換算的 13.1 倍不一致，改以倍數明定。新品組合明列為 Qlex、Winrevair、Capvaxive、Enflonsia、Ohtuvayre、Lipfendra，2026Q3 約 21.6 億美元（不含未揭露的 Lipfendra）。前份三項皆未成立","settle_metric":"股價 ÷ FY2027 共識 EPS；新品組合單季營收"},{"axis":"Single Thing 首次設定","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"本次 Single Thing：美國法院或主管機關對 Keytruda Qlex 的透明質酸酶智財作出不利 Merck 的裁決或禁制令，Qlex 無法在美國續售","ruling":"Q3 法說揭露荷蘭禁制令已讓歐洲 6 國停供，分析師追問美國風險；Qlex 是 2028–2029 年美國防線的主要工具，屬可監測的單一二元事件","evidence_refs":["substitute_technology#3"]},{"axis":"清倉／減碼門檻首次設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設門檻（null）","side_b":"本次四條：Keytruda 家族連 2 季負成長、Qlex 2027Q4 < 10 億美元或美國禁制令、FY2027 共識 EPS < 8.5 美元、新品組合 2027Q4 < 22 億美元","ruling":"任一觸發即停止重跑研究；若屆時已持有則減碼一半，兩條同時觸發則清倉。前份只有重新進場條件，沒有論點失效的出場線，本次補上"}],"triggers":[{"n":1,"text":"三項重新進場條件同時成立","type":"估值rearm","maps_to":"H1/H2","metric":"Qlex 單季營收；新品組合單季營收；股價 ÷ FY2027 共識 EPS","threshold":"≥12 億美元；≥25 億美元；≤13 倍（約 119 美元），三項同時","action":"重跑研究，通過後才考慮首筆建倉","source_freq":"季度新聞稿＋每日收盤＋月度共識快照","date":"2027-02 起逐季"},{"n":2,"text":"美國 Qlex 智財不利裁決或禁制令","type":"Single Thing","maps_to":"Single Thing","metric":"美國 Qlex 透明質酸酶專利訴訟與禁制令","threshold":"任何不利裁決或禁制令","action":"Bear 機率上調到 40%，取消重跑研究條件 12 個月","source_freq":"8-K、10-Q 訴訟附註、法說；不定期","date":"審理時程事實表未涵蓋","evidence_refs":["substitute_technology#3"]},{"n":3,"text":"2027 年 EPS 財測低於共識","type":"假設驗證","maps_to":"R1","metric":"2027 年調整後 EPS 財測中點","threshold":"< 8.8 美元","action":"Base 路徑下修、Bear 機率上調到 35%，維持不追","source_freq":"Q4 FY2026 財報；一次","date":"2027-02"},{"n":4,"text":"Keytruda 家族轉為負成長","type":"風險","maps_to":"R2","metric":"Keytruda 家族單季營收年增率（扣除進貨時點）","threshold":"連 2 季 < 0%","action":"停止重跑研究；若屆時已持有則減碼一半","source_freq":"季報；每季","date":"2027Q1–2028Q4","evidence_refs":["supply_demand_durability#2","end_markets#5"]},{"n":5,"text":"雙特異抗體在全球三期勝過 Keytruda","type":"風險","maps_to":"R3","metric":"PD-1×VEGF 對 Keytruda 的全球三期頭對頭整體存活","threshold":"統計顯著勝出","action":"威脅升為架構替代，Bear 機率上調到 40%，重跑研究","source_freq":"公司與 Summit／Akeso 公告、ASCO／ESMO；不定期","date":"讀數時程事實表未涵蓋","evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"n":6,"text":"Gardasil 國際需求續弱","type":"風險","maps_to":"R4","metric":"Gardasil 美國以外單季營收年增率","threshold":"連 2 季 < −10%","action":"Base 疫苗營收再下修 10%，Bear 機率加 5 個百分點","source_freq":"季報；每季","date":"逐季","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#1","end_markets#1"]},{"n":7,"text":"政策壓縮毛利率","type":"風險","maps_to":"R5","metric":"全年調整後毛利率","threshold":"< 80%（2026 財測約 81%，2027 預期上升）","action":"Base 終端倍數由 14 降到 13 倍","source_freq":"年度財測與季報","date":"2027-02 起","evidence_refs":["regulatory_antitrust#3","reg_tariff_export#1"]},{"n":8,"text":"中國來源管線受政策限制","type":"風險","maps_to":"R6","metric":"美國對中國臨床數據或授權交易的限制","threshold":"立法或行政命令通過","action":"sac-TMT 與 MK-2010 的上行貢獻歸零，Bull 機率降到 15%","source_freq":"國會與行政部門公告；不定期","date":"不定期","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":9,"text":"訴訟與調查出現重大金額","type":"風險","maps_to":"R7","metric":"DOJ 民事調查、RotaTeq 反壟斷、Cronin 證券訴訟的和解或裁決金額","threshold":"任一 > 10 億美元，或證券訴訟進入證據開示","action":"Bear 情境扣除一次性金額，Bear 機率加 5 個百分點","source_freq":"10-Q／10-K 訴訟附註；每季","date":"逐季","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]},{"n":10,"text":"sac-TMT 子宮內膜癌 PDUFA","type":"複審日期","maps_to":"H3","metric":"FDA 核准與否","threshold":"核准","action":"核准不改變不追；未核准則 Bull 機率降到 15%","source_freq":"FDA／公司公告；一次","date":"2027-06-15"},{"n":11,"text":"Q4 FY2026 財報與 2027 年財測","type":"複審日期","maps_to":"H1/H2/R1","metric":"重新進場三項條件與 2027 年財測","threshold":"見第 1、3 條","action":"逐項對帳後重寫判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"Keytruda 家族單季營收年增率（扣除進貨時點效益）","bear_threshold":"連 2 季 < 0%（2028 年 Medicare 議價生效前）","window":"2027Q1–2027Q4","source":"公司季度新聞稿與法說","last_status":"ok"},{"metric":"Qlex 單季營收","bear_threshold":"2027Q4 < 10 億美元，或美國出現禁制令","window":"至 2027Q4","source":"公司季度新聞稿；8-K 訴訟公告","last_status":"ok"},{"metric":"FY2027 共識調整後 EPS","bear_threshold":"< 8.5 美元","window":"2026-11 至 2027-08","source":"Koyfin 月度共識快照","last_status":"ok"},{"metric":"新品組合單季營收（Qlex、Winrevair、Capvaxive、Enflonsia、Ohtuvayre、Lipfendra）","bear_threshold":"2027Q4 < 22 億美元（較 2026Q3 約 21.6 億無成長）","window":"至 2027Q4","source":"公司季度新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"customer_concentration_credit#0","reason":"證據是 2022 年底的 10-K 數據、距今近四年，且原文自己註明屬產業結構性集中、非新增惡化；沒有附任何呆帳或信用事件，無法連到本次論點"},{"ref":"major_events#3","reason":"來源是第三方召回清單的搜尋摘要，Class II、單一劑型套組（Emend 口服懸液），未附任何營收金額或後續處分"},{"ref":"product_recall_warning#0","reason":"與 Emend 召回為同一事件的重複收錄，同樣來自第三方召回清單摘要，原文寫明未見 2026 年警告信，未附營收衝擊數字"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"3","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='迴避', 矩陣機械輸出='迴避'"}],"pacing":[],"holding_cap":"0%（重跑研究通過前）","requires_critic":[],"rearm_trigger":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤FY2027 共識 EPS 的 13 倍（以 9.14 計約 119 美元）","exec_line":"不持有、不追；三項條件同時成立前不建倉，成立後先重跑研究，通過才考慮首筆建倉"},"reasoning":{"industry":"收錢方式：專利期內的處方藥與疫苗，經美國三大批發商出貨，最後由 Medicare、商業保險與各國政府付款。營收分部（2026Q3 總營收 181 億美元、年增 5%，Q3 法說）：Keytruda 家族 86 億美元（約 48%、年增 6%，含 Qlex 8.3 億）、Gardasil 20 億美元（約 11%、年增 14%，含 CDC 採購與時點效益）、Winrevair 6.94 億、Welireg 3.07 億、動物保健年增 3%。單點依賴：Keytruda 一項約占營收一半，這是集中度風險，不是護城河證據。利潤率：2026Q2 營收 166.07 億美元，GAAP 營業利益率 −2.6%、調整後稅前利益率 3.3%，都被 Terns 收購研發費用壓低；Q3 調整後毛利率 81.4%、營業費用年增 12%。產業時鐘 III：核心 PD-1 單抗在多個已核准適應症接近滲透高峰（CFO 2026-10-29），2028 年起進入 Medicare 議價與專利到期。產業態勢雙向拉鋸：競爭端惡化（雙特異抗體頭對頭勝過 Keytruda、Imfinzi 年增 30%、生物相似藥卡位），其他結構變數同時在動（Medicare 議價、MFN 直售平價方案、Section 232 關稅以美國投資換三年延後），需求端仍在擴張（PD-1 市場預估年複合 18.7%）。","moat":"機制：專利保護的生物藥＋腫瘤科商業規模＋以 Keytruda 為骨幹的組合開發能力。可證方向：投入資本事實表未涵蓋，取不到 ROIC 差，改看利潤率與份額。FY2025 營業利益率 34.01%，與 ABBV TTM 33.94% 相當、高於 BMY 29.19% 與 PFE 26.72%；但 TTM FCF 利潤率 18.72% 低於 ABBV 28.28%，研發密度 53.19%（含收購研發）是同業的 2.5–3.5 倍。份額：Keytruda 家族仍年增 5–6%、Opdivo 年減 5%，領先地位未失，但 Imfinzi 年增 30%、Opdivo 皮下劑型早 9 個月上市。執行力評 7：新藥上市順利、三期接連正向，但 I-DXd 撤回加速核准申請、tulisokibart 在 SSc-ILD 失敗、Capvaxive 美國年減 13%。定價權評 5：Keytruda 2028 年 Medicare 議價、MFN 協議與直售平價方案、德國政策與美國以外價格逆風、Gardasil 中國十分之一價格競爭。方向：執行力穩定、定價權縮減，整體縮減。","growth":"成長來源以量為主：新藥放量（Winrevair 年增 94%、Qlex 單季 8.3 億）與併購帶入的管線（Terns、Cidara、TARGAN）；價格面受壓；回購每年約 30 億美元、約占市值 0.8%。三年共識 EPS：FY2026E 2.72（收購研發費用壓低）、FY2027E 9.14、FY2028E 10.12（Koyfin 快照，家數事實表未涵蓋；營收共識 23 位分析師）。以事實表唯一可得的 FY2025 GAAP 稀釋 EPS 7.28 當基期，三年年複合約 11.6%，但基期與共識口徑不同，高估真實成長。內生成長上界約 4%（見護城河段），缺口歸因見下欄，無法歸因的部分依賴重新評價，長期信心上限為中。五年後跑道：Keytruda 已在多個適應症接近滲透高峰（CFO 2026-10-29），新藥是有三期數據支持的第二條曲線，但管理層 2030 年代中期 700 億美元目標相對 2026 年財測中點 670.5 億只是持平，所以是中等跑道。FY2027／FY2028 共識近期各下修 0.98%／0.78%，CFO 又說多數分析師尚未納入 2027 投資年訊息。","governance":"FCF/NI：FY2022 1.01、FY2024 1.06、FY2025 0.68（FY2023 淨利僅 3.65 億美元，比值失真）。SBC 占營收 1.79%（2026Q2），年化約 12 億美元、約占市值 0.33%。現金去向：股息（殖利率 2.29%，換算約 84 億美元／年）、回購約 30 億美元（2026 年）、收購與授權（Terns 約 67 億、TARGAN 約 6.5 億、SciBrunch 預付 4 億，Cidara 金額未涵蓋）、資本支出（Q2 單季 8.93 億美元）。FY2025 FCF 123.6 億美元大致只夠付股息與回購，收購靠舉債，淨負債 467.7 億美元。收購報酬：多數為上市前資產、研發費用一次認列，報酬尚未實現。回購買入收益率以 FY2027 共識計約 6.2%，十年期公債殖利率事實表未涵蓋，無法判定是否高出 2 個百分點。","valuation":"現價 148.56 美元＝FY2027 共識 9.14 美元的 16.25 倍、FY2028 共識 10.12 美元的 14.7 倍；EV 4,132.8 億美元，trailing EV/S 6.13 倍、P/S 5.44 倍，兩者都在可得四個年度端點的最高位。trailing 本益比 150 倍與 FY2026 前瞻 54.6 倍被收購研發費用扭曲，不可用。現價要求：專利到期只是淺坑、FY2028 起 EPS 維持兩位數美元並在 2030 年代回到成長，且市場願意繼續給 15 倍以上。我們只部分相信：Base 情境 FY2031 EPS 10.0 美元 × 14 倍約 140 美元，價格面五年 −5.8%，加股息後年化不到 2%。賣方 8 月初平均目標價約 134.56 美元，比現價低約 9%（ESMO 讀數前的舊數字），方向上支持不追。同業前瞻倍數事實表未涵蓋。","premortem":"偏空看錯：三期接連成功（TroFuse-005、INTerpath-001）、Winrevair 與 Lipfendra 放量快過預期、2027 年 Keytruda 權利金到期帶動毛利率上升，CFO 明言接近專利到期時盈餘會成長；若 FY2031 EPS 走到 12.6 美元、17 倍，價格約 214 美元。偏多看錯：Keytruda 美國留存率低於預期、Qlex 智財受挫、雙特異抗體取代骨幹，FY2031 EPS 7.4 美元、11 倍約 81 美元。最大回撤範圍 −35%～−55%：Base 路徑 FY2029 低點 8.9 美元 × 約 10.8 倍、Bear 路徑 FY2030 低點 7.1 美元 × 9.5 倍；事實表未涵蓋公司歷史最大回撤，無法用歷史校準。法說迴避：管理層在 Q2 法說與投資人日多次不給專利到期期間的 EPS 數字，也不透露與 FDA 的非比例風險討論。"},"plain":{"six":{"how_it_makes_money":"賺癌症病人與付款方的錢：Keytruda 家族約占營收一半，錢卡在美國專利與 Medicare 議價這一節點，2028–2029 年開始鬆動","moat":"護城河縮減中：執行力穩定，但定價權在收縮","growth":"五年後跑道中等：新藥是有三期數據的第二條曲線，但規模只夠把 Keytruda 的坑填平","capital":"資本配置中等：股息與每年約 30 億美元回購穩定，但新藥接棒靠舉債併購，收購報酬尚未實現","valuation":"現價要求 Keytruda 專利到期只是淺坑、新藥五年內接上逾 250 億美元的缺口，且市場續給 15 倍以上；我們只部分相信，價格偏貴","how_wrong":"最可能看錯在低估新藥接棒速度；反方向的錯則是低估 Keytruda 美國流失速度"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"FY2027 共識尚未完全反映 CFO 2026-10-29 說的 2027 投資年（營業費用中高個位數成長、超過 20 億美元學名藥逆風），且 26 週上漲 33% 已把 sac-TMT 與 intismeran 的三期成功當成商業成功定價","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"迴避","prior_role":"不持有","wait_for_price":true,"wait_for_price_condition":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤FY2027 共識 EPS 的 13 倍（以 9.14 計約 119 美元）","trap":"🟡","val":"🟠","moat":"C","moat_trend":"↓","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":148.56,"week26_return_pct":33.08,"consensus_rev_3m_pct":-0.73,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026 共識 2.72 美元含收購研發一次性費用（Q2 法說 CFO 說 Terns 預付每股 2.31 美元，事實表註記為 2.43，口徑不一；另有 Cidara 與 SciBrunch 費用）。改用 FY2027 共識 9.14 美元當分母，但 CFO 2026-10-29 表示多數分析師尚未納入 2027 投資年訊息，FY2027 分母本身也有下修風險"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 2027 年財測（首次量化投資年）","impact":"高","watch":"EPS 財測中點對共識 9.14 美元、營業費用成長率"},{"date":"2027-06-15","date_precision":null,"type":"regulatory","event":"sac-TMT 子宮內膜癌 PDUFA","impact":"中","watch":"核准與標示範圍"},{"date":"2028-01","date_precision":"month","type":"regulatory","event":"Keytruda Medicare 議價價格生效","impact":"高","watch":"議價折扣幅度與 2028 年財測"},{"date":"2028-12","date_precision":"month","type":"other","event":"Keytruda 美國核心專利到期","impact":"高","watch":"生物相似藥上市時程與 Qlex 轉換率"}],"_projected_from":"v19"}
```
