你是 stock-analyst v20 的**散文層（prose）agent**，標的 HWM（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HWM_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：HWM　日期：2026-11-03　archetype：None　前份裁決：2026-07-10　觀望｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2515B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（861B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1017B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1514B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1720B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（877B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1293B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2244B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3561B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3160B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2515           3140-4485      3 條（2–6 內）  
s3                  8000         861           4997-7139      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4251          7524-10749      5 條（2–6 內）  
s6                 11000         877          7086-10123      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1293           1545-2207      3 條（2–6 內）  
s10                 5000        2244           1929-2756      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3160           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=6250B；至少需散文≈38.75KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−58%
−55
−55%
−54%
−41%
−35%
−35
−22.8%
−11.73
−11.7%
0.14
0.24
0.5%
0.5
0.6%
0.75
0.8%
0.85
0.89
0.9
0.95
01
1
1%
1.1%
1.1
1.2
1.2%
1.3
1.37
1.42
1.5
1.6
1.7
1.8
02
2.0
2
2.13
2.2%
2.5
2.6%
2.95
3
03
3.27
3.4%
3.5
3.71
3.9
3.95
3.995
4%
04
4
4.45
4.5
5%
5
5.1
5.3
5.4
5.42
5.50
5.5%
5.6
5.62
5.7
5.7%
5.8
06
6%
6
6.2
6.30
6.5
6.55
6.6%
6.6
6.8
7.0
7%
7
07
7.1
7.1%
7.55
7.6
7.68
8
8%
08
8.2
8.4%
8.5
9
09
9%
9.06
9.45
9.7
10
10%
10.4
10.6
10.7%
11%
11
11.2
12
12%
12.2
12.8
13%
13.4%
13.9%
14
14%
14.4%
14.51
15
15%
15.08
15.5%
16%
16.5%
17%
17
17.2%
17.5%
18
18%
19%
19.0%
19.8%
20
20%
20.8%
21%
21.3
21.5
22
22%
22.5%
22.8%
23%
23.4%
23.7%
24
25%
25
26
26.3%
27.03
27.4%
27.5
28
28.0%
28%
28.7%
29%
29
29.1%
29.4%
29.8
30%
30
31%
31
31.0%
32
32%
32.3
32.5%
33
33%
34
35%
35
36%
36.6%
37.7
39%
39
39.0
39.01
39.1%
40%
41%
41
41.5
43%
44%
45%
45
46.5%
48
49
49.5%
50
50%
52
54%
60%
70
72%
77%
85%
90
91
98
98%
100%
100
103
104
112
115
116.8
117.5
118
120
124
140
148
150%
175
$175
180
185
195
197
211
211.44
232
240
251
265
273.77
290
291
297
313
350
435.2
456
520
580
737
787
2018
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
2032
20261103
1,686
1,860
2,000
2,250
8,000
8,600
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
{"meta":{"ticker":"HWM","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Howmet Aerospace Inc."},"oneliner":"引擎熱段葉片的供給瓶頸商，航太備品與燃氣渦輪兩條線都在成長、現金流強；但現價仍是 FY2026 盈餘的 39 倍，2027 營收展望放緩到 +12%，最大客戶 GE 又併購了鑄件對手，Base 年化報酬只有個位數，等 NTM 本益比 ≤29 倍再分批","thesis":{"H":[{"id":"H1","text":"商用航太 OE 爬坡加上引擎備品，帶動 Engine Products 2027 至 2028 年營收年增 ≥12%，備品占總營收維持 ≥20%","2y":"Engine Products 季營收年增 ≥12%（Q3 2026 為 +33%）；737、A320、787、A350 產量續升；LEAP-1B 新葉片在 2027Q1 切換","5y":"備品占營收 ≥20%（Q3 2026 約 21%）；新一代葉片的內容價值提升，反映在 Engine 營收上","10y":"LEAP 與 GTF 機隊在 2030 年代進入入廠維修高峰；交機量約 2032 年見頂（Aviation Week 估約 2,250 架）","threshold":"地板：Engine Products 季營收年增 ≥10%；備品占營收 ≥18%","source":"公司季報新聞稿分部表與法說；Boeing、Airbus 產量公告；Aviation Week 交機預測","drift_rule":"以 TTM 年增率計：連 2 季偏離門檻 5% 以上視為削弱，連 3 季偏離 10% 以上視為反轉"},{"id":"H2","text":"燃氣渦輪營收從 2025 年約 10 億美元的基期起，3 年內翻倍，2030 年前到約 25 億美元；成長靠市占提升與客戶長約產能，且不增加負債","2y":"2027 年燃氣渦輪營收年增 ≥25%（Q3 2026 為 +45%）；新產能如期投產","5y":"2030 年燃氣渦輪營收約 25 億美元；主要客戶的產能仍訂到 5 年後","10y":"2025 至 2030 年新增的渦輪機隊，帶動 2030 年代 IGT 備品放量","threshold":"地板：燃氣渦輪營收年增 2027 年 ≥20%、2028 年 ≥15%","source":"公司季報法說的燃氣渦輪成長率；GE Vernova 等客戶的訂單、積壓與產能訂滿年份","drift_rule":"連 4 季偏離門檻 5% 以上視為削弱，連 6 季偏離 10% 以上視為反轉；主要客戶首次下修燃氣渦輪展望時，立即重估"},{"id":"H3","text":"在擴產與回購同時進行下，調整後 EBITDA 利潤率守住 ≥32%、Engine Products ≥36%，自由現金流 ≥營收的 18%，淨負債對 EBITDA ≤1.5 倍","2y":"2027 年調整後 EBITDA 利潤率 ≥32.5%；CAM 綜效開始兌現，Fastening 利潤率回到 ≥30%（Q3 2026 為 29.4%）","5y":"資本支出高峰（2027 至 2028 年）過後，FCF 率 ≥20%","10y":null,"threshold":"地板：調整後 EBITDA 利潤率 ≥31%；Engine Products EBITDA 利潤率 ≥36%；FCF 對淨利 ≥85%","source":"公司季報新聞稿與分部表","drift_rule":"連 2 季偏離門檻 5% 以上視為削弱，連 3 季偏離 10% 以上視為反轉"}],"R":[{"id":"R1","text":"客戶垂直整合：GE 併 CPP（117.5 億美元，預計 2027 下半年完成）、P&W 自建鑄造廠、多家大客戶有自有高溫合金爐，可能把一級高壓渦輪葉片或結構鑄件移出 HWM","h_ref":"H1","clock":"🐢","threshold":"任一主要窄體引擎的一級葉片改由客戶自製或 CPP 供應；或 GE 占營收由約 11% 降到 9% 以下（10-K 年度揭露）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","customer_second_source#0","customer_second_source#1","customer_second_source#2","customer_concentration_credit#1","supply_demand_durability#4","end_markets#3"]},{"id":"R2","text":"燃氣渦輪熱潮反轉：資料中心電力需求不如預期；SpaceX 自鑄葉片、新創改裝舊航空引擎分流需求；HWM 與同業同時擴產，造成產能過剩（HWM 已有 7 座新廠，另考慮再蓋 3 座）","h_ref":"H2","clock":"🔥","threshold":"燃氣渦輪營收年增連 2 季低於 15%；或主要燃氣渦輪客戶首次下修訂單或交機展望","evidence_refs":["substitute_technology#0","competitive_share_entrants#1"]},{"id":"R3","text":"短期外部衝擊：航油高漲使航空公司從冬季到 2027 年減班；關稅與出口限制；海綿鈦與特殊合金屬有限來源；墨西哥、中國、歐洲的營運與戰爭風險","h_ref":"H3","clock":"⚡","threshold":"調整後 EBITDA 利潤率連 2 季年減超過 100bp；或商用航太營收年增連 2 季低於 8%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"成長換檔引發倍數下修：2027 營收展望 +12%，不到 2026 年內生成長的一半，市場質疑 2026 年之後的成長","h_ref":"H1","clock":"🔥","threshold":"2027-02 法說把 2027 營收展望下修到 112 億美元以下（約 +9%）；或 NTM 本益比跌破 25 倍而 EPS 沒有下修（代表倍數 regime 下移）","evidence_refs":["capital_markets_pricing#4"]}],"single_thing":{"description":"主要燃氣渦輪客戶（GE Vernova、Siemens、三菱等）首次下修燃氣渦輪訂單或交機展望，或 HWM 燃氣渦輪營收年增連 2 季跌破 15%，代表資料中心與電力帶動的燃氣渦輪熱潮已經見頂","why_fatal":"IGT 是增量成長與五年後跑道的主要來源：Q3 年增 45%，執行長目標 2030 年約 25 億美元；它也是溢價倍數的理由。HWM 正在蓋 7 座新廠、考慮再蓋 3 座，資本支出高檔延續到 2028 年。熱潮反轉會同時打到 EPS 路徑（2028 至 2030 年成長降到個位數）、倍數（壓到約 20 倍）與新產能的報酬。數學上這是最大的單一敏感項：IGT 由 10 億成長到 25 億美元，以 Engine 分部利潤率粗算，約對應 2030 年 EPS 1 美元，比失去一個窄體引擎一級葉片更大（執行長自己也這樣比較）","if_happens":"減碼一半；若 HWM 同時縮減擴產計畫或下修 IGT 路徑，清倉；未持有則放棄建倉計畫","how_monitor":"每季 HWM 法說的燃氣渦輪營收成長率與產能訂滿年份；GE Vernova 等客戶季報的訂單與積壓；HWM 的資本支出指引","probability":"12 到 24 個月內約 15%。客戶稱 2031 年產能已訂滿、2032 年也接近訂滿，短期反轉的機率低；但 SpaceX 自鑄葉片、新創改裝舊引擎，顯示需求方正在找替代"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":32.3,"peg_fy2":1.7,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":3.71,"FY2026E":5.42,"FY2027E":6.55,"FY2028E":7.68},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS（年度財報，3.71）；FY2026E 到 FY2028E 為 Koyfin 10-31 共識，與公司調整後 EPS 同口徑。兩者口徑差距小（Q3 GAAP 營業利益率 28.7%，調整後 29.1%）；財年於 12 月底結束"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HWM_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"製造瓶頸＋售後備品年金＋客戶長約，ROIC 高，FCF 轉換約九成；但營收綁在航空交機與燃氣渦輪的資本週期上，帶有循環成分"},"industry":{"clock_phase":"II","sd_verdict_source":"航太屬結構性持久：2026 年交機量 1,686 架仍低於 2018 年，2032 年約 2,250 架才見高峰（Aviation Week）；GE Aerospace 稱到 2027 年的限制在供給，不在需求。IGT 能見度長，客戶稱 2031 年產能已訂滿，2032 年也會在一兩季內訂滿；但它屬資本財週期，供給可逆性中等（GE 併 CPP、SpaceX 自鑄葉片、新創改裝舊引擎）","bargaining":{"up":"上游海綿鈦與特殊合金屬有限或單一來源，認證要求讓替代來源不易取得（FY2024 10-K）；多數採年度或長約採購","down":"下游集中：GE Aerospace 與 RTX 各約占 2025 年第三方銷售 11%，前兩大合計約 22%；多家最大客戶有自有高溫合金爐。目前 HWM 因為是供給瓶頸而占上風，漲價幅度高於成本轉嫁","geo":"2025 年出貨地北美 72%、歐洲 22%；營運據點包含墨西哥、中國、日本"},"profit_pool_dir":"短期流向 HWM：葉片是瓶頸，Engine 利潤率 39.1%。中期有回流 OEM 的壓力：GE 透過併購 CPP、P&W 透過自建鑄造廠，想把利潤池拉回自家","tam_table":[{"item":"TAM 總額","value":"事實表未涵蓋"},{"item":"IGT 葉片全球市占","value":"逾 50%（執行長，2026-08-06 法說）；Q3 IGT 營收 +45%，快於產業，市占仍在上升"},{"item":"IGT 營收路徑","value":"2025 年基期約 10 億美元（由執行長「2.5 倍約 25 億美元」回推）；3 年內翻倍，2030 年約 25 億美元"},{"item":"商用航空交機量","value":"2026 年 1,686 架，2027 年 1,860 架，2028 年約 2,000 架，2032 年高峰約 2,250 架（Aviation Week）"},{"item":"備品占營收","value":"2019 年 11%，2025 年 21%，Q1 2026 23%，Q3 2026 約 21%"},{"item":"營業利益池占比 5 年變化","value":"產業利益池事實表未涵蓋；HWM 自身營業利益率由 2022 年 17.2% 升到 TTM 28.0%"}]},"moat":{"mechanism":"熱段單晶渦輪葉片的量產良率，加上逐料號認證（執行長稱累積了數十年）；航太與燃氣渦輪共用同一套鑄造能力，形成規模與學習曲線。葉片是這兩條供應鏈的共同瓶頸","execution":9,"pricing":8,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：IGT 營收 Q3 年增 45%，明顯快於產業，執行長稱市占持續增加（全球葉片市占逾 50%）；Engine Products EBITDA 利潤率 39.1%，一年擴大 580bp。定價面擴大但有上限：2025 年漲價幅度高於材料與通膨轉嫁，但最大客戶有自有爐，並以併購建立替代來源。GE 併 CPP 的負面記在威脅等級，不在趨勢上重複扣分。最大客戶份額下滑目前沒有 sourced 證據","peer_na_reason":"同業 ROIC 與利潤率歷史事實表未涵蓋，只能用 TTM 利潤率差距比較；SAF.PA 沒有季度損益資料","threats":[{"level":"🔴","text":"客戶生態攻擊：GE Aerospace（約占營收 11%）以 117.5 億美元買下鑄件對手 CPP，金額約為 HWM 市值的 14%，預計 2027 下半年完成。執行長評 CPP 強項在結構件鑄造，並說下一座結構鑄件廠的規模與地點可能因此調整。估計五年內實質分走 HWM 在 GE 的葉片或結構件份額的機率約 30%","p":30,"evidence_refs":["competitive_share_entrants#2","customer_second_source#2","supply_demand_durability#4","end_markets#3"]},{"level":"🟡","text":"點對點：多家最大客戶有自有高溫合金爐，自製翼型鑄件；P&W 自建先進鑄造廠；10-K 自承客戶整併後可能換掉 HWM","p":20,"evidence_refs":["competitive_share_entrants#0","customer_second_source#0","customer_second_source#1","customer_concentration_credit#1"]},{"level":"🟡","text":"點對點：新進者與新技術（10-K 一般性風險因子）。SpaceX 計畫自鑄燃氣渦輪葉片，接受降載運轉換取供電；新創改裝退役航空引擎發電。執行長認為新產能上線後，這些替代方案會變得不必要","p":15,"evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率（TTM 營業利益率 28.0%）× 投入資本周轉率事實表未涵蓋。從持續高檔的資本支出與 7 座新廠來看，判讀接近高利益率×低周轉，需要看再投資負擔","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（航空公司、電廠與資料中心）、決策者（引擎與燃氣渦輪 OEM）、付款者（OEM；備品由航空公司與維修廠付）三個角色都成立。葉片是「需要」不是「想要」：缺葉片的代價是引擎停飛或渦輪無法發電。執行長在 Q3 提到，SpaceX 甚至接受沒有葉片的渦輪交貨，自行補上葉片後降載運轉。代理讀數：備品 Q3 年增 30%，占營收約 21%；GE Aerospace 稱 2027 年前的限制在供給、不在需求"},{"item":"決策層級","level":"🟡","text":"替代性要在「單一引擎型號的單一級葉片」這個層級衡量：每個料號都要客戶重新認證，執行長稱這種能力花了數十年。但 10-K 顯示最大客戶已有自有高溫合金爐，GE 買下 CPP，P&W 自建鑄造廠，客戶的自製能力正在擴大。代理讀數：重新認證週期，以及 GE 營收占比約 11%；漲價後的客戶流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的超額利潤主要落在引擎 OEM 的售後服務。HWM 現在因為是供給瓶頸，能讓漲價幅度高於成本轉嫁（2025 年報），Engine 利潤率 39.1%。但買方集中（GE、RTX 各約 11%），又有自建能力；2028 年後新產能陸續投產、產能一旦鬆動，利潤可能流回 OEM。長期需求存在，不等於 HWM 能一直拿到現在的份額"},{"item":"社會容忍度","level":"🟢","text":"B2B 零件，終端消費者看不到，社會對漲價的敏感度低。執行長刻意「不占客戶便宜」，沒有把價格推到經濟上限，等於留下緩衝。國防件可能受政府成本審查；關稅方面，Section 232 未課稅但保留選項，屬政策風險。國防定價審查案例事實表未涵蓋"}],"roiic":"約 33%（2026 年粗估，淨利口徑）","reinvest_rate":"常態約 30%（2026 年含併購約 98%）","endo_ceiling":10,"formula_note":"單位為百分比。增量 ROIC 約等於 2026 年淨利增量除以新增投入資本。淨利由 FY2025 的 15.08 億美元（GAAP）增加到 FY2026 約 22 億（調整後，指引 EPS 5.50 × 約 4 億股），增量約 7.1 億；兩年口徑不同，略有落差。新增資本約 21.5 億：兩件併購約 20 億，加資本支出約 5 億，減折舊攤銷約 3.5 億（以 Q3 EBITDA 利潤率 32.5% 減調整後營業利益率 29.1%，推得約占營收 3.4%）。兩者相除約 33%；營運資金變動事實表未涵蓋，未計入。這 33% 混合了兩種報酬：有機部分極高，併購部分目前偏低。常態再投資率：資本支出淨額約 1.5 到 3 億，加上假設平均每年併購約 7 億，除以 FY2027 稅後利益約 26 億（共識 EPS 6.55 × 約 3.95 億股），約 15% 到 40%，取 30%。內生成長上限約 33% × 30%，約 10%。2026 年的有機成長多來自既有設備良率提升與定價，不需要新資本，這部分不能外推"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","HWM":36.63,"ATI":24.46,"CRS":31.21,"TDG":59.57,"SAF.PA":null,"unit":"%"},{"metric":"營業利益率","HWM":28.01,"ATI":16.52,"CRS":23.36,"TDG":46.47,"SAF.PA":null,"unit":"%"},{"metric":"FCF 利潤率","HWM":19.83,"ATI":8.4,"CRS":10.69,"TDG":19.26,"SAF.PA":null,"unit":"%"},{"metric":"研發密度","HWM":0.39,"ATI":null,"CRS":null,"TDG":null,"SAF.PA":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"ATI","gm":24.46,"om":16.52,"fcf_margin":8.4,"rd_intensity":null,"strategy_note":"特殊合金與鍛件，TTM 營業利益率 16.5%、FCF 率 8.4%，遠低於 HWM；它同時是鍛件對手與鈦材上游。利潤差距顯示 HWM 站在價值鏈中較難取代的熱段環節","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CRS","gm":31.21,"om":23.36,"fcf_margin":10.69,"rd_intensity":null,"strategy_note":"高溫合金材料商，營業利益率 23.4%、FCF 率 10.7%；材料環節也在漲價，價值鏈的利潤不是只流向 HWM","period":"TTM ending 2026-09-30（4季加總）"},{"name":"TDG","gm":59.57,"om":46.47,"fcf_margin":19.26,"rd_intensity":null,"strategy_note":"售後專利件模式，營業利益率 46.5%；自有設計、售後定價，與按客戶圖面生產的 HWM 屬不同層級，不拿來當倍數錨","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SAF.PA","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表無財務資料；它是 LEAP 引擎的合資方，也是 HWM 客戶，議價位置在下游端"}]},"growth":{"driver_mix":"2026 年以量為主（商用航太 OE、備品、IGT），價為輔（漲價高於成本轉嫁、鋁價轉嫁）；併購約 4pp（CAM、Brunner），回購每年約增厚 EPS 1%。2027 年展望 +12% 不含新併購","runway_years":"滲透率口徑不適用。以需求能見度計約 6 到 8 年：IGT 客戶產能訂到 2031 至 2032 年，交機量 2032 年見高峰","runway_post_y5":"🟢","endo_ceiling_basis":"引用報酬持續期欄：增量 ROIC 約 33% × 常態再投資率約 30%，約 10%。Base 情境 EPS 五年年增約 13.9%，超出上限，差額靠利潤率擴張與回購補足，因此 Bear 機率取 30%","segments":[{"item":"Engine Products","value":"Q3 2026 營收 14.51 億美元，年增 33%（商用航太 +39%、燃氣渦輪 +44%）；EBITDA 利潤率 39.1%，年增 580bp；占營收約 54%"},{"item":"Fastening Systems","value":"6.30 億美元，年增 41%，扣除 CAM 與 Brunner 併購後 +10%；EBITDA 利潤率 29.4%，年減 140bp，受 CAM 稀釋"},{"item":"Engineered Structures","value":"2.95 億美元，年減 4%，扣除出售的 Savannah 後 +8%；EBITDA 利潤率 23.7%，年增 290bp"},{"item":"Forged Wheels","value":"3.27 億美元，年增 32%（量增加上鋁價轉嫁）；EBITDA 8,600 萬美元，利潤率約 26.3%，被鋁價轉嫁稀釋"},{"item":"備品（跨分部）","value":"Q3 約 5.7 億美元，年增 30%，占營收約 21%；Q1 2026 為 23%，2019 年為 11%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"reading":"TTM 毛利率 36.6%，2022 到 2025 年逐年上升"},{"signal":"核心市占近 12 個月縮減","lit":false,"reading":"IGT 市占續升；航太葉片未見有出處的份額流失"},{"signal":"主力產品提價後銷量下滑","lit":false,"reading":"量價齊升"},{"signal":"EPS 成長顯著高於營收（差距大於 5pp）","lit":true,"reading":"2022 到 2025 年 EPS 年增約 49.5%，營收約 13.4%；FY2027 共識 EPS +20.8%，公司營收展望 +12%"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"reading":"2024 年 0.85，2025 年 0.95"},{"signal":"SBC／營收大於 5% 且逐年上升","lit":false,"reading":"約 1.1%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"reading":"SpaceX 自鑄葉片、改裝舊引擎屬邊際替代，列入監測"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"reading":"同業倍數歷史事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 大於 60%","lit":false,"reading":"資本支出約 5 億，FCF 約 20 億"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"reading":"7 座新廠，另考慮再蓋 3 座"}],"trap_rating":"長期成長性 🟡（十類衰退信號亮 1 項）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"2026 年營收成長 29%，其中內生占 25 個百分點，併購只貢獻約 4 個百分點，成長不靠併購撐；資本去向的四項分配已寫在理由段"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"CAM 18 億美元（2026-04 完成）加 Brunner。Q3 併購帶來的營收約 1.37 億美元（Fastening 年增 41%，扣除內生 10%）；以 CAM 約 20% 的利潤率粗算，年 EBITDA 約 1.1 億，對價約 20 億，稅前 EBITDA 報酬約 5.5%，低於資本成本。綜效多數在 2027 年，2026 年對 EPS 約持平","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2026 年初至今回購 11 億美元，均價 251 美元（Q3 均價 265）。以 FY2026 指引 EPS 5.50 計算，盈餘收益率 2.2%；以 FY2027 共識 6.55 計算為 2.6%。10 年期公債殖利率事實表未涵蓋，但除非殖利率低於約 0.6%，否則達不到「殖利率加 2 個百分點」的門檻","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 前三季 8,000 萬美元，約占營收 1.1%；稀釋股數 Q3 末 3.995 億股，8 年減少逾 1 億股，淨稀釋為負","grade":"過"}]},"valuation":{"basis":"以 Fwd P/E（FY2026 共識 EPS）為主，PEG 為輔","tier":"航太引擎熱段零組件，按客戶圖面生產、有長約；TDG 屬售後專利件，層級不同；ATI、CRS 屬材料上游","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比或 EV/S 現值，無法做倍數對照；終端倍數改以自身年度端點分位與成長熄火情境定錨"},"fwd_pe":39.01,"peg":1.42,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"偏貴一級。FY2027 本益比 32 倍；PEG 1.42（FY2026 本益比 39.0 除以 FY2025A 到 FY2028E 共識 EPS 年增 27.4%；改用 FY2026 到 FY2028 的 19.0%，則約 2.0，偏貴）；Base 年化約 7%，低於一成；EV/S 在近 4 個年度端點的 77% 分位。前份在股價 273.77 美元時判最貴一級，這次股價跌 22.8%、EPS 又上修，所以降一級。五年分位事實表未涵蓋","upside_short_pct":7.6,"upside_mid_pct":37.7},"trap_analysis":{"verdict":"🟡","label":"低到中。十類衰退信號只亮「EPS 成長快於營收逾 5pp」一項，屬利潤率擴張帶動；利潤率見頂後，成長會向營收靠攏。判斷依據見反證紀錄"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"HWM 已在蓋 7 座新廠、考慮再蓋 3 座，資本支出高檔延續到 2028 年；GE 以 117.5 億美元買下 CPP；SpaceX 計畫自鑄燃氣渦輪葉片，新創改裝舊航空引擎發電；10-K 承認大客戶有自有高溫合金爐","assumption":"IGT 需求是結構性的，HWM 的單晶葉片良率別人短期內學不來","consequence":"五年後虧 50% 最可能的故事：2028 年起 IGT 熱潮退燒，同一時間 GE 在 CPP 併購完成後把部分葉片移回自家，EPS 卡在 6 美元附近，倍數壓到 20 倍，股價約 120 美元","ruling":"部分採納：以 30% 的 Bear 機率計入。這條與唯一致命點（IGT 反轉）部分重疊；客戶垂直整合另列為威脅","watch":"燃氣渦輪營收年增率、GE 占營收比、資本支出指引","evidence_refs":["customer_second_source#0","customer_second_source#2","substitute_technology#0","supply_demand_durability#4","competitive_share_entrants#2"],"fact_refs":["f_consensus_eps_fy1"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年回購 11 億美元，均價 251 美元，盈餘收益率約 2.2%，Q3 均價 265 美元；CAM 18 億美元買在約 20% 的利潤率，綜效要到 2027 年才出現；2027 至 2028 年資本支出還要再上升","assumption":"成長兌現，每股價值就會同步成長","consequence":"營收照計畫成長，但高價回購與低報酬併購把增量 ROIC 拉低到 15% 到 20%，FCF 對淨利掉到 85% 以下，每股內含價值的成長落後營收","ruling":"部分採納：資本配置三項只過一項（SBC 稀釋低），列入觀察，不改 Base 路徑","watch":"FCF／淨利、回購均價、CAM 綜效金額、資本支出占營收比","evidence_refs":[],"fact_refs":["f_kpi4_free_cash_flow","f_kpi5_stock_based_compensation"]},{"view":"價格已反映太多","evidence":"FY2026 本益比 39.0 倍、FY2027 32.3 倍；EV/S 在近 4 個年度端點的 77% 分位；2027 營收展望 +12%，不到 2026 年內生成長的一半","assumption":"市場會繼續給高峰成長期的倍數","consequence":"即使 EPS 照共識成長，倍數向 28 倍收斂就會吃掉一半以上的 EPS 複利，Base 年化只有個位數","ruling":"採納：這是本次選擇等價格的主因","watch":"NTM 本益比是否到 29 倍；2027-02 法說的展望修訂","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_fwd_pe_latest","f_ev_s_current","f_ev_s_percentile"]},{"view":"論點失敗","evidence":"10-K 列出關稅、出口限制、海綿鈦等有限來源原料，以及墨西哥、中國、歐洲營運與戰爭風險；執行長稱航油高漲可能讓冬季到 2027 年的部分航班減少","assumption":"短期外部衝擊不會傷到備品與利潤率","consequence":"利潤率連續被關稅與原料吃掉，H3 失守，倍數提前下修","ruling":"以反駁為主：Section 232 航太調查沒有課新稅，執行長預期備品不受影響。改用利潤率年變動判斷吸收是否失敗（連 2 季年減超過 100bp）","watch":"調整後 EBITDA 利潤率年變動、Forged Wheels 鋁價轉嫁稀釋","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"],"fact_refs":["f_kpi3_adjusted_ebitda_margin"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 273.77 → 本次 211.44（-22.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=273.77","side_b":"本次 price_at_dd=211.44","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟠、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 273.77 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 273.77 美元：Bull 價 456、Bear 價 148，五年期望值 +22.5%，基準年化 5.7%，不對稱比 1.6","side_b":"本次情境、股價仍用 273.77 美元：Bull 價 435.2、Bear 價 124，五年期望值 +1.2%，基準年化 1.2%，不對稱比 0.9","ruling":"先換情境、股價不動：五年期望值少 21.3 個百分點，基準年化少 4.5 個百分點。不對稱比由 1.6 變為 0.9。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 273.77 美元：五年期望值 +1.2%，基準年化 1.2%，不對稱比 0.9","side_b":"本次情境、股價 211.44 美元：五年期望值 +31.0%，基準年化 6.6%，不對稱比 2.13","ruling":"再換股價、情境不動：起點價下跌 22.8%，五年期望值多 29.8 個百分點，基準年化多 5.4 個百分點，不對稱比由 0.9 升到 2.13。合計五年期望值比前份多 8.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移（價格變動）：估值、回撤範圍、結論與角色","cause":"價格變動","prior_field":["val","max_dd_pct"],"side_a":"前份（2026-07-10，股價 273.77 美元）：估值判最貴一級，最大回撤估 −58%，結論觀望","side_b":"本次（211.44 美元，跌 22.8%）：FY2026 本益比 39.0 倍、FY2027 32.3 倍、NTM 約 33 倍，估值降為偏貴一級；回撤以較低的起點與倍數重算為 −35% 到 −55%；結論與角色依本次輸入重新路由","ruling":"三欄變動的主因是股價下跌，次因是 FY1 共識三個月上修 7.1%。估值仍偏貴，結論方向不變，仍是等價格","evidence_level":"高","settle_metric":"NTM 本益比","if_then":["若 NTM 本益比降到 29 倍以下，且 Engine Products 利潤率 ≥36% → 重跑判斷，通過後分批首筆建倉","若股價反彈到 52 週均線（約 240 美元）以上，而 2027 展望沒有上修 → 不追"],"evidence_refs":[]},{"axis":"前份漂移（新證據）：價值陷阱風險、情境機率、綜合訊號","cause":"新證據","prior_field":["trap","p_bull_pct","p_bear_pct","signal"],"side_a":"前份：價值陷阱風險最低一級；Bull、Bear 機率各 25%；綜合訊號 B 級","side_b":"本次：10-29 首度給出 2027 營收展望 +12%，對比 FY2027 共識 EPS +20.8%，EPS 成長快於營收逾 5pp，價值陷阱風險升一級（十類中只亮這一項）。GE 併 CPP 是新出現的客戶垂直整合，加上 Base 路徑超出內生成長上限，Bear 機率由 25% 調到 30%；Bull 維持 25%；綜合訊號維持 B 級","ruling":"陷阱風險上升是成長換檔的提醒，不代表論點失敗；Bear 機率上調，反映客戶垂直整合與內生上限被超過","evidence_level":"中","settle_metric":"2027 年 EPS 與營收的成長差距；GE 占營收比","if_then":["若 2027-02 法說把營收展望上修到 118 億美元以上，且 EPS 與營收成長差距縮到 5pp 以內 → 價值陷阱風險回到最低一級","若 GE 宣布葉片移轉 → Bear 機率升到 35%，並減碼三分之一"],"evidence_refs":["capital_markets_pricing#4","customer_second_source#2"]},{"axis":"前份漂移（以新證據重驗後不變）：護城河趨勢、五年後跑道、公司類型、循環位置","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河趨勢向上，五年後跑道寬，品質複利成長型，未設循環位置","side_b":"本次四欄不變，但依據更新。趨勢仍向上：IGT 市占續升，Engine 利潤率年增 580bp；GE 併 CPP 記在威脅等級，不在趨勢上重複扣分。跑道仍寬，而且更有據：客戶產能訂到 2031 至 2032 年，IGT 翻倍時程縮短到 3 年。公司類型不變。屬非循環型，仍不設循環位置","ruling":"維持。若 GE 實際移轉了葉片份額，趨勢改判穩定，並重估等級","evidence_level":"中","settle_metric":"燃氣渦輪營收成長、GE 占營收比","if_then":["若主要窄體引擎的一級葉片移轉 → 趨勢改判穩定，等級重估","若燃氣渦輪營收年增連 2 季低於 15% → 跑道降為中等"],"evidence_refs":["end_markets#3","competitive_share_entrants#2"]},{"axis":"重啟條件變更（建倉與加碼條件）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"NTM Fwd P/E 回落 ≤ 35x（約 $175-195）或航太類股回檔 20%+；或售後/IGT 加速使共識 FY27 EPS 上修 >15% 重錨倍數","side_b":"NTM 本益比 ≤29 倍（以現行共識約 185 美元），且 Engine Products EBITDA 利潤率 ≥36%；觸發後重跑判斷，通過才分批建倉，之後才談加碼","ruling":"前份條件已觸發：NTM 本益比約 33 倍，低於 35 倍；主因是 EPS 上修，股價仍高於 175 到 195 美元的區間。依紀律，觸發後是重跑判斷，而不是直接建倉。重跑發現 2027 營收展望只有 +12%，成長在換檔，合理退場倍數下修到 28 倍，Base 年化只有個位數。所以門檻由 35 倍改為 29 倍，並加上利潤率護欄，避免在基本面轉壞時接刀","evidence_level":"中","settle_metric":"NTM 本益比","if_then":["若 NTM 本益比 ≤29 倍且護欄成立 → 首筆建倉三分之一","若價格先跌，但跌的原因是 IGT 客戶下修或葉片移轉 → 不買"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"主要燃氣渦輪客戶首次下修訂單或交機展望，或 HWM 燃氣渦輪營收年增連 2 季跌破 15%，代表資料中心與電力帶動的燃氣渦輪熱潮已經見頂","ruling":"本次依規定補設 Single Thing。數學上最大的單一敏感項是 IGT 熱潮反轉：這段增量約對應 2030 年 EPS 1 美元，也是溢價倍數的支撐，比失去單一窄體引擎一級葉片更大。發生時減碼一半；若公司同時縮減擴產，則清倉","evidence_level":"中","settle_metric":"燃氣渦輪營收年增率、客戶訂單展望","if_then":["若發生 → 減碼一半","若 HWM 同時縮減擴產或下修 IGT 路徑 → 清倉"],"evidence_refs":["substitute_technology#0"]},{"axis":"kill_metrics 新設（減碼與清倉門檻）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）","side_b":"Engine Products 季營收年增連 2 季低於 10% → 停止加碼（連 3 季低於 5% 則減碼三分之一）；燃氣渦輪營收年增連 2 季低於 15% → 減碼一半；調整後 EBITDA 利潤率連 2 季低於 30% → 減碼三分之一，若同時燃氣渦輪年增低於 10% → 清倉；主要窄體引擎一級葉片移轉 → 減碼三分之一","ruling":"本次補上可以量化的減碼與清倉門檻，分別對應三條假設與最大的威脅","evidence_level":"高","settle_metric":"公司季報分部數字","if_then":["任一門檻觸發 → 依上列動作執行，並在兩週內重跑判斷"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"GE 併 CPP：客戶垂直整合，對照執行長稱正為 GE 擴產","cause":"新證據","prior_field":null,"side_a":"空方：GE（約占營收 11%）以 117.5 億美元買下鑄件對手 CPP，消息出來時股價跌近 11%；10-K 自承多家最大客戶有自有高溫合金爐，客戶整併後可能換掉 HWM；P&W 也自建鑄造廠","side_b":"多方：執行長（2026-10-29）說 CPP 強項在結構件鑄造，HWM 正在為 GE 新增一批要兩年才能裝好的大型產能；他也說，即使失去最大窄體引擎的一級葉片，2031 年單一年度的 IGT 備品增量就能補上","ruling":"可調和，屬程度差異。2027 年前不影響葉片份額；結構鑄件的擴廠規模可能縮小，執行長自己說可能影響下一座廠的規模與地點。長期以 30% 機率列為生態威脅並計入 Bear，不改趨勢","evidence_level":"中（公司 10-K 與法說，另有二手報導）","settle_metric":"GE 占 HWM 營收比；HWM 是否揭露葉片計畫移轉","if_then":["若 GE 或 CPP 承接任一主要窄體引擎的一級高壓渦輪葉片 → 減碼三分之一，並重估護城河等級","若 HWM 為 GE 新增的產能投產並簽下長約 → 威脅機率降到 20%"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_second_source#1","customer_second_source#2","customer_concentration_credit#1","supply_demand_durability#4","end_markets#3"]},{"axis":"2027 成長換檔：+12% 展望，對照慣常偏保守的初步指引","cause":"新證據","prior_field":null,"side_a":"空方：2027 營收展望 +12%±0.5%，不到 2026 年內生成長 22% 到 25% 的一半；有報導稱股價較 8 月水位低約 35%，投資人質疑 2026 年之後的成長","side_b":"多方：2026 年 2 月的初步指引是營收 91 億、EPS 4.45，最後上修到 103 億、5.50；IGT 翻倍時程由 3 到 5 年縮短到 3 年；國防補庫存與飛彈增產尚未計入；共識 FY2027 營收 116.8 億，已高於公司的約 115 億","ruling":"可調和。初步展望偏保守是慣例，但 2026 年有一次性順風（既有設備良率提升、鋁價轉嫁、併購約 4pp），2027 年實際成長較可能落在 13% 到 16%。這不構成論點失敗，但支持較低的退場倍數。這項利空已反映在賣方模型中：10-31 快照的 FY2 共識仍小幅上修 0.8%","evidence_level":"中","settle_metric":"2027-02 法說的 2027 營收展望","if_then":["若展望上修到 118 億美元以上，且 FY2027 共識 EPS ≥7.0 → NTM 本益比會自然接近重啟門檻，重跑判斷","若展望下修到 112 億美元以下 → Bear 機率升到 35%，停止建倉計畫"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"管理層的槓桿說法改口","cause":"新證據","prior_field":null,"side_a":"2026-08-06 Q2 法說，John Plant：年底淨負債對 EBITDA 約 1 倍","side_b":"2026-10-29 Q3 法說，John Plant：2026 年底的槓桿會與 2025 年底相近；Q3 實際約 1.3 倍，當季回購 5 億美元","ruling":"可調和。差異來自加速回購（年初至今 11 億，比 2025 全年多 4 億），以及 CAM 的商業本票還剩 3.9 億；不是現金流轉弱，Q3 FCF 5.62 億，全年指引上調到 20 億。這次承諾數字有改動，記一筆，看年底實際值","evidence_level":"高","settle_metric":"2026 年底淨負債對 EBITDA","if_then":["若 2027 年資本支出上升期間槓桿升破 1.8 倍，而回購沒有減少 → 資本配置降級，並停止加碼","若年底在 1.2 倍以下 → 結案"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭惡化：GE 併 CPP、P&W 自建鑄造廠、SpaceX 自鑄燃氣渦輪葉片、新創改裝退役航空引擎發電；10-K 也列了新進者與新技術風險","side_b":"結構轉好且持久：2026 年交機量仍低於 2018 年，2032 年才見高峰；GE Aerospace 稱限制在供給、不在需求；IGT 客戶產能訂到 2031 至 2032 年。其他結構變數：Section 232 航太調查沒有課新稅，但保留 180 天談判期與日後課稅的選項；10-K 列了關稅、出口限制，以及海綿鈦的有限來源","ruling":"雙向拉鋸。結構轉好目前強過競爭惡化，但競爭惡化是 2026 年才出現的趨勢，攻擊者的資本量級很大。關稅屬中性偏負，用利潤率年變動來判斷是否吸收失敗","evidence_level":"中","settle_metric":"燃氣渦輪與商用航太成長率；調整後 EBITDA 利潤率年變動","if_then":["若利潤率連 2 季年減超過 100bp，且公司歸因於關稅 → 停止加碼","若主要客戶公告自製葉片量產 → 減碼三分之一"],"evidence_refs":["supply_demand_durability#4","substitute_technology#0","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"axis":"現在就買的最強論證，對照等價格","cause":"價格變動","prior_field":null,"side_a":"現在就買：股價較前份跌 22.8%，較 8 月高點約 −35%；NTM 本益比約 33 倍，已低於前份的重啟線；FY1 共識三個月上修 7.1%，2026 年內全年指引連續上調四次；IGT 翻倍時程提前；新增 50 億美元回購，約占市值 6%；RSI 48，不過熱","side_b":"等價格：Base 情境（EPS 五年年增約 14%、退場 28 倍）年化只有個位數；FY2026 本益比 39 倍，要 2031 年仍有 30 倍以上才划算；成長換檔與 GE 垂直整合都是新增的不確定","ruling":"選等價格。決勝的數字是 Base 年化報酬：要到一成，股價要到約 185 美元，或 EPS 路徑再上修約 15%","evidence_level":"中","settle_metric":"NTM 本益比；2027-02 法說展望","if_then":["若 NTM 本益比 ≤29 倍，且 Engine Products 利潤率 ≥36% → 重跑判斷後，首筆建倉三分之一","若股價先漲回 240 美元以上，而展望沒有上修 → 不追","反向條件：若股價跌破 185 美元是因為 IGT 客戶下修或葉片移轉 → 不買，改依觸發器處理"],"evidence_refs":[]},{"axis":"賣方目標價，對照本次判斷","cause":"新證據","prior_field":null,"side_a":"賣方（Q3 前）：平均目標價約 297 到 313 美元（約 20 位分析師，絕大多數買進），JP Morgan 350 美元；隱含 FY2027 共識約 45 到 48 倍","side_b":"本次：2031 年 Base 價值約 291 美元，與賣方的 12 個月目標相近；本次判斷比共識悲觀","ruling":"分歧在框架層：賣方把高峰成長期的倍數延伸到成長換檔之後（倍數 regime），事實層（EPS 路徑）的差異不大。Q3 後的目標價更新值事實表未涵蓋","evidence_level":"低（彙整網站，Q3 前資料）","settle_metric":"Q3 後的賣方目標價與倍數假設","if_then":["若賣方普遍把目標倍數降到 35 倍以下，而股價沒有跌 → 代表市場接受用較低倍數換較高 EPS，重跑判斷"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Engine Products 營收成長是否守住","type":"假設驗證","maps_to":"H1","metric":"Engine Products 季營收年增率（TTM）","threshold":"≥10%；連 2 季低於 10% 視為削弱","action":"削弱時停止加碼；連 3 季低於 5% 時減碼三分之一","source_freq":"公司季報新聞稿分部表，每季","date":"2027-02","evidence_refs":[]},{"n":2,"text":"燃氣渦輪翻倍路徑是否守住","type":"假設驗證","maps_to":"H2","metric":"燃氣渦輪營收年增率","threshold":"2027 年 ≥20%，2028 年 ≥15%","action":"連 2 季低於門檻時停止加碼，並重估 IGT 路徑","source_freq":"公司季報法說，每季","date":"2027-02","evidence_refs":[]},{"n":3,"text":"擴產期間利潤率是否守住","type":"假設驗證","maps_to":"H3","metric":"調整後 EBITDA 利潤率；Engine Products EBITDA 利潤率","threshold":"調整後 ≥31%，Engine Products ≥36%","action":"連 2 季跌破時停止加碼","source_freq":"公司季報新聞稿，每季","date":"2027-02","evidence_refs":[]},{"n":4,"text":"客戶垂直整合是否開始搶走葉片","type":"風險","maps_to":"R1","metric":"主要窄體引擎一級高壓渦輪葉片的供應來源；GE 占營收比","threshold":"出現任一移轉公告；或 GE 占營收降到 9% 以下","action":"減碼三分之一，並重估護城河","source_freq":"HWM 與 GE 的公告、法說、10-K，事件驅動","date":"2027-09","evidence_refs":["competitive_share_entrants#2","customer_second_source#2","customer_second_source#1"]},{"n":5,"text":"短期外部衝擊是否吃進利潤率","type":"風險","maps_to":"R3","metric":"商用航太營收年增率；調整後 EBITDA 利潤率年變動","threshold":"商用航太年增連 2 季低於 8%，或利潤率連 2 季年減超過 100bp","action":"停止加碼；若同時 Engine 利潤率低於 36%，減碼三分之一","source_freq":"公司季報，每季","date":"2027-02","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"n":6,"text":"燃氣渦輪熱潮見頂","type":"Single Thing","maps_to":"Single Thing","metric":"主要燃氣渦輪客戶的訂單與交機展望；HWM 燃氣渦輪營收年增率","threshold":"客戶首次下修展望，或 HWM 燃氣渦輪營收年增連 2 季低於 15%","action":"減碼一半；若 HWM 同時縮減擴產計畫，清倉","source_freq":"GE Vernova、Siemens、三菱的季報，以及 HWM 法說，每季","date":"2027-02","evidence_refs":["substitute_technology#0"]},{"n":7,"text":"估值重啟條件","type":"估值rearm","maps_to":"rearm","metric":"NTM 本益比，加上 Engine Products EBITDA 利潤率護欄","threshold":"≤29 倍（以現行共識約 185 美元），且 Engine Products 利潤率 ≥36%","action":"重跑判斷，通過後分批首筆建倉三分之一","source_freq":"每日股價與共識 EPS，每週檢查","date":null,"evidence_refs":[]},{"n":8,"text":"Q4 法說後複審","type":"複審日期","maps_to":"H1、H2、H3","metric":"2027 營收展望修訂、Q4 實績、資本支出指引","threshold":"2027 營收展望維持 115 億美元以上","action":"法說後兩週內重跑判斷","source_freq":"公司 Q4 法說","date":"2027-02","evidence_refs":[]},{"n":9,"text":"利潤率失守時減碼","type":"減碼","maps_to":"H3","metric":"調整後 EBITDA 利潤率","threshold":"連 2 季低於 30%","action":"減碼三分之一","source_freq":"公司季報，每季","date":null,"evidence_refs":[]},{"n":10,"text":"利潤率與燃氣渦輪同時失守時清倉","type":"清倉","maps_to":"H2、H3","metric":"調整後 EBITDA 利潤率；燃氣渦輪營收年增率","threshold":"利潤率連 2 季低於 30%，且燃氣渦輪年增低於 10%","action":"清倉","source_freq":"公司季報，每季","date":null,"evidence_refs":[]},{"n":11,"text":"2027 展望下修引發倍數下修","type":"風險","maps_to":"R4","metric":"2027 營收展望","threshold":"2027-02 法說下修到 112 億美元以下","action":"Bear 機率升到 35%，停止建倉計畫","source_freq":"公司 Q4 法說","date":"2027-02","evidence_refs":["capital_markets_pricing#4"]}],"kill_metrics":[{"metric":"Engine Products 季營收年增率","bear_threshold":"連 2 季低於 10%（Q3 2026 為 +33%）","window":"2027Q1–2028Q4","source":"公司季報新聞稿分部表","last_status":"ok"},{"metric":"燃氣渦輪營收年增率","bear_threshold":"連 2 季低於 15%（Q3 2026 為 +45%）","window":"2027Q1–2028Q4","source":"公司季報法說","last_status":"ok"},{"metric":"調整後 EBITDA 利潤率","bear_threshold":"連 2 季低於 30%（Q3 2026 為 32.5%）","window":"2027Q1–2028Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"主要窄體引擎一級高壓渦輪葉片是否移轉給客戶自製或 CPP","bear_threshold":"任一公告即觸發","window":"2027–2029（GE 併 CPP 完成後）","source":"HWM 與 GE 公告、法說、10-K 客戶占比","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=-11.73, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 情境有部分營收骨架，也有具名的燃氣渦輪來源，但 2030 年 25 億美元的目標和客戶產能訂到 2031 至 2032 年的原文沒核實到，歷史上可比案例的 5 年報酬也不足以佐證 +15.5% 年化，所以這個 Bull 依據只能算部分站得住。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='NTM 本益比 ≤29 倍（以現行共識約 185 美元，對應 Base 五年年化約一成），且 Engine Products EBITDA 利潤率 ≥36%；若下跌是 IGT 客戶下修或葉片移轉造成的，不算達成'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"NTM 本益比 ≤29 倍（以現行共識約 185 美元），且 Engine Products EBITDA 利潤率 ≥36%；觸發後先重跑判斷，再分批","exec_line":"未持有：等 NTM 本益比 ≤29 倍、且 Engine Products 利潤率 ≥36% 時重跑判斷，通過後分三筆建倉，每筆間隔至少一季財報。已持有：不加碼，也不因波動減碼，只依觸發器動作"},"reasoning":{"industry":"Q3 2026 營收 27.03 億美元，年增 29%，內生 25%。調整後營業利益率 29.1%，GAAP 28.7%，調整後 EBITDA 利潤率 32.5%；TTM 毛利率 36.6%。四個分部：Engine Products 14.51 億，約占 54%，年增 33%，EBITDA 利潤率 39.1%；Fastening Systems 6.30 億，約占 23%，含 CAM 與 Brunner 併購，扣除後年增 10%；Engineered Structures 2.95 億，約占 11%，扣除出售的 Savannah 後年增 8%；Forged Wheels 3.27 億，約占 12%，成長來自量增與鋁價轉嫁。終端市場：商用航太 +32%、國防 +10%、燃氣渦輪 +45%、商用運輸 +28%；備品約 5.7 億，占營收約 21%。收錢方式有三種：OEM 長約供貨、備品（航空公司與維修廠經 OEM 下單）、IGT 客戶的長約產能。產業時鐘判第 II 段擴張：2026 年交機量 1,686 架仍低於 2018 年，Aviation Week 預測 2032 年約 2,250 架才見高峰，飛機訂單積壓龐大；IGT 段已有過熱跡象，客戶產能訂到 2031 到 2032 年，新創也在搶進。供需持久性：航太屬結構性持久；IGT 能見度長，但供給可逆性中等。議價：下游集中，GE 與 RTX 各約占 2025 年第三方銷售 11%（FY2025 10-K）；上游的海綿鈦與特殊合金屬有限或單一來源。沒有單一客戶超過 11%，單點依賴在上游原料，不在客戶。全年指引營收約 103 億美元，Q4 約 27.5 億。","moat":"機制：引擎熱段葉片要在更高溫、更高壓下運轉，每個料號都要經過客戶認證，執行長說這種能力花了數十年才建立；目前葉片是航太與燃氣渦輪的共同瓶頸。同業對照（TTM）：HWM 營業利益率 28.0%、FCF 率 19.8%，高於 CRS 的 23.4% 與 10.7%，也高於 ATI 的 16.5% 與 8.4%；TDG 的 46.5% 屬售後專利件模式，層級不同。同業 ROIC 及其歷史趨勢事實表未涵蓋，只能拿利潤率差距代替，無法證明差距仍在擴大，所以合併分不給到 8 分以上。執行面給 9 分：內生成長 25%、增量利潤率 43%，單季吸收約 520 名新員工仍能擴大利潤率。定價面給 8 分：2025 年漲價幅度高於材料與通膨轉嫁；但執行長自述不趁供給緊張占客戶便宜，大客戶也有自有爐，並透過併購建立替代來源。威脅：GE 併 CPP 屬客戶的生態攻擊，攻擊者動用的資本約為 HWM 市值的 14%，扣 1 分，機率 30%；其餘的自有爐、新進者與替代技術屬點對點威脅。趨勢判 ↑：執行面在擴大（IGT 市占提升），定價面也在擴大但有上限；GE 併 CPP 的負面只記在威脅等級，不在趨勢上重複扣分。當期 ROIC 因投入資本與稅率事實表未涵蓋而無法計算；增量 ROIC 粗估約 33%，常態再投資率約 30%，內生成長上限約 10%，推導寫在報酬持續期欄。","growth":"2026 年的成長組成：以量為主（商用航太 OE 加備品、IGT），價為輔（漲價高於成本轉嫁、鋁價轉嫁），併購約貢獻 4pp（CAM、Brunner），回購每年約增厚 EPS 1%。三年共識 EPS：FY2025 實際 3.71（GAAP 稀釋），FY2026E 5.42，FY2027E 6.55，FY2028E 7.68（Koyfin 10-31 快照；營收共識有 18 位分析師），三年年化約 27.4%，其中 FY2026 到 2028 約 19.0%。內生成長上限約 10%，等於增量 ROIC 約 33% 乘以常態再投資率約 30%。缺口約 17pp，來源可以拆開：利潤率擴張（2026 年增量利潤率 43%，既有設備良率提升不需要新資本）、2026 年的併購、淨回購。這段缺口不靠重新評價。往後兩年的缺口（19% 對 10%）主要靠利潤率續升與 CAM 綜效；利潤率見頂之後，EPS 成長會向營收成長靠攏。十類衰退信號只亮 1 項：EPS 成長快於營收逾 5pp。","governance":"FCF 對淨利的比率：2023 年 0.89、2024 年 0.85、2025 年 0.95（年度財報，見事實表財務歷史欄）；2026 年 FCF 指引約 20 億美元（±0.5 億），約占營收 19%。SBC 前三季 8,000 萬美元，約占同期營收 1.1%；稀釋股數 Q3 末降到 3.995 億股，8 年減少逾 1 億股。2026 年現金去向：併購約 20 億（CAM 18 億加 Brunner）、資本支出逾 5 億、回購 11 億（年初至今）、股利每季 0.14 美元（Q3 調升 17%）。淨負債約 41 億美元，Q3 淨負債對 EBITDA 約 1.3 倍，商業本票還有 3.9 億未還。董事會再加 50 億美元回購授權，約為市值的 6%。計分卡：併購報酬未過，CAM 併購前利潤率約 20%，綜效多數在 2027 年，前三季對 EPS 約持平；回購收益率未過，均價 251 美元對 FY2026 指引 EPS 5.50 只有 2.2%，改用 FY2027 共識也只有 2.6%；SBC 淨稀釋過，股數淨減少。營運槓桿：2026 年營收年增約 25%，EBITDA 增幅更快，沒有壓縮。","valuation":"現價 211.44 美元，是 FY2026 共識 EPS 的 39.0 倍、FY2027 的 32.3 倍、FY2028 的 27.5 倍，NTM 約 33 倍。trailing 本益比 41.5 倍落在近 4 個年度端點的 44% 分位，EV/S 9.06 倍在 77% 分位（只有 4 個年度端點，不是五年分位）。反推：要五年拿到一成年化，若 2031 年退場倍數 28 倍，FY2031 EPS 須約 12.2 美元，年增約 17.5%；若退場 32 倍，須約 10.6 美元，年增約 14.4%。Base 路徑 EPS 年增約 13.9%、退場 28 倍，年化約 7%；倍數從 39 倍收斂到 28 倍，每年吃掉約 6.6pp。我相信 EPS 能複利 13% 到 14%，但不相信 2031 年成長回到一成左右時，市場還會給 30 倍以上。同業倍數事實表未涵蓋，終端倍數以自身的年度端點與成長熄火情境定錨。","premortem":"反證與盲點的完整推演寫在反證紀錄，這裡只交結論。價值陷阱風險低到中：十類衰退信號只亮「EPS 成長快於營收」一項。最大的單一敏感項是 IGT 熱潮反轉。回撤範圍估 −35% 到 −55%：2026 年 8 月以來，在基本面沒有受損的情況下已跌約三成五，26 週報酬 −11.7%；股價 211 美元，低於 52 週均線 240 美元，高於 104 週均線 197 美元。訴訟、監管、召回方面查無新事件，反壟斷只有一般性條文。"},"plain":{"six":{"how_it_makes_money":"HWM 賺的是引擎與燃氣渦輪 OEM 的錢，錢卡在熱段單晶渦輪葉片這一節。量產良率加上數十年累積的認證，讓 HWM 成為航太與電力兩條供應鏈的共同瓶頸。Engine Products 占營收約 54%，EBITDA 利潤率 39.1%","moat":"護城河趨勢向上，等級 B。機制是熱段單晶葉片的量產良率與認證門檻：IGT 葉片全球市占逾 50% 且仍在上升，Engine 利潤率一年擴大 580bp。扣分處在最大客戶 GE 以 117.5 億美元買下鑄件對手 CPP，客戶自製能力限制了定價上限","growth":"五年後的跑道仍寬。IGT 是已有具名客戶背書的第二條成長曲線：客戶產能訂到 2031 至 2032 年，執行長目標 2030 年約 25 億美元；航太交機量也要到 2032 年才見高峰。但 2027 年營收展望只有 +12%，成長率從 2026 年的 25% 換檔下來","capital":"資本配置中上。現金流強到可以同時擴產、併購、回購而不加槓桿，SBC 稀釋極低。扣分在兩處：回購價位偏高（2026 年均價 251 美元，盈餘收益率約 2.2%），以及 CAM 併購的報酬還沒兌現","valuation":"現價要成立，HWM 未來五年 EPS 須年增約 14% 到 18%，而且 2031 年還要維持 28 到 32 倍，才拿得到一成年化。EPS 複利這部分我大致相信，倍數維持這部分我不信。估值判偏貴一級","how_wrong":"最可能看錯的是倍數與 IGT 熱潮能持續多久，而不是航太本業。如果 2028 年後燃氣渦輪需求反轉，又碰上 GE 收回部分葉片，EPS 與倍數會一起下修。反過來說，如果 2027 年展望像 2026 年那樣一路上修，等價格就可能錯過"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"NTM 本益比 ≤29 倍（以現行共識約 185 美元，對應 Base 五年年化約一成），且 Engine Products EBITDA 利潤率 ≥36%；若下跌是 IGT 客戶下修或葉片移轉造成的，不算達成","qc48_result":"pass","qc48_note":"Bull 情境有部分營收骨架，也有具名的燃氣渦輪來源，但 2030 年 25 億美元的目標和客戶產能訂到 2031 至 2032 年的原文沒核實到，歷史上可比案例的 5 年報酬也不足以佐證 +15.5% 年化，所以這個 Bull 依據只能算部分站得住。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":211.44,"week26_return_pct":-11.73,"consensus_rev_3m_pct":7.11,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母為 FY2026 共識 EPS 5.42（公司指引 5.50），前三季已實現；CAM 併購對 EPS 約持平，沒有一次性項目的爭議"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"macro","event":"期中選舉後，國會處理 2027 國防預算，取代持續決議；這會決定飛彈零件增產與補庫存能否定案","impact":"中","watch":"國防預算通過時間；飛彈多年期合約是否定案"},{"date":"2027-01","date_precision":"month","type":"regulatory","event":"Section 232 航太調查的 180 天談判期約在 2027 年 1 月到期，屆時可能決定是否課稅","impact":"中","watch":"是否對航太零件課新關稅；HWM 能否轉嫁"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 法說：細化 2027 營收展望（初步約 115 億美元、+12%）與各機型產量假設","impact":"高","watch":"2027 營收展望是否上修；燃氣渦輪成長率；資本支出指引"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"LEAP-1B 新一代熱段葉片預計在 2027 年第一季切換","impact":"中","watch":"切換時點是否延後；單機價值提升幅度"},{"date":"2027-09","date_precision":"quarter","type":"other","event":"GE Aerospace 併購 CPP，預計 2027 下半年完成","impact":"高","watch":"完成後 GE 是否移轉葉片或結構鑄件訂單"}],"_projected_from":"v19"}
```
