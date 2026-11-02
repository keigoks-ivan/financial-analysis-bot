你是 stock-analyst v20 的**散文層（prose）agent**，標的 GILD（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GILD_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：GILD　日期：2026-11-03　archetype：None　前份裁決：2026-05-25　A+ 核心候選滿格訊號 — 五維齊全｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2502B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（724B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（996B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1576B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1339B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（1012B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1520B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2657B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4412B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3024B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2502           3149-4498      3 條（2–6 內）  
s3                  8000         724           5093-7276      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3911          7762-11089      5 條（2–6 內）  
s6                 11000        1012           6992-9988      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1520           1386-1980      3 條（2–6 內）  
s10                 5000        2657           1640-2343      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3024           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5908B；至少需散文≈39.09KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−55%
−53%
−40%
−35
−35%
−29%
−18%
−15
−1.9%
−1.9
−1.5%
−1.20
−0.85
−0.75
−0.45
0.3%
0.30
0.4
0.5%
0.7%
0.75
0.8%
0.8
0.9%
1%
1
$1
01
1.11
1.31
1.5%
1.77
1.85
1.9%
1.92
1.92%
$2
2%
2
02
2.03
2.37
2.4
2.5
2.6%
3%
03
3
3.05
3.4
3.55
3.64
3.7
3.9%
3.9
4.0
4
4%
04
4.5%
4.5
4.6
4.8
05
5
5%
5.06
5.3%
5.6%
5.8
6%
6
6.78
6.8
07
7.0
7
7.2%
7.3
7.4
7.5%
8
08
8%
8.75
8.9
8.925
9
09
9.10
9.27
9.6
9.6%
9.91
10
10%
10.73
11%
11
11.4
12%
12
12.40
12.55
12.6
13%
13
13.6
14%
14
15
15.5
15.8
16%
16
16.5%
16.5
17
17.1
18%
18
20
20%
20.7
21%
23
24%
24
24.3%
25
25%
25.7
26
26%
26.1%
29
29%
29.2%
29.26
30%
30.0%
30
31
31%
34.62
35%
035
36.2%
38%
38.0%
39.6%
39.7%
40
40%
40.2%
41
41.68
42
42%
44%
45
45%
45.92
47.98
49%
49
50%
50
50.35
52
53%
60%
62
67
70%
70
74%
77
79.5%
80
80%
80.16
82.89
83
85%
85.10
86%
88%
88.6
90
93%
94.56
100%
100
104
110
115
117
119.56
120
129
134.36
135
136.21
140
150%
157.93
159.28
166
169.44
176
180
183
205
225
230
232
237
250
$250
254.77
262
272.8
294.4
301
310
312.9
313
320
335.5
340
$350
365
753
1205
1215
1240
1720
2015
2020
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
2036
3107
4182
8000
8527
14000
23000
30600
31200
31289.15
31300
31500
32200
33400
34300
34400
36000
36400
37700
39200
39300
42200
45000
20261103
2,102
2,600
23,000
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
{"meta":{"ticker":"GILD","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Gilead Sciences, Inc."},"oneliner":"GILD 的 HIV 處方地位與長效 PrEP 仍在擴大，但 2028 年起 Medicare 議價壓縮 Biktarvy 定價權；股價半年漲 29%、倍數在四年高點，論點未破、估值已走在前面，等 135 美元以下再加碼。","thesis":{"H":[{"id":"H1","text":"長效 PrEP 成為第二根 HIV 支柱：Yeztugo 半年一針，加上 2027 年的週口服與 2028 年的年針，讓 GILD 的 PrEP 份額維持在 50% 以上。","2y":"FY2026 Yeztugo 約 10 億美元；FY2027 ≥16 億美元；週口服 lenacapavir PrEP 於 2027-02 前後獲核准","5y":null,"10y":null,"threshold":"FY2027 Yeztugo ≥16 億美元；GILD PrEP 市占 ≥50%；再注射率 ≥70%","source":"公司季報新聞稿與法說會（2026-10-29 Johanna Mercier：Yeztugo Q3 3.05 億、PrEP 市占 50%、再注射率超過 70%）","drift_rule":"Yeztugo 季銷售對照 FY2027 的 16 億路徑（每季約 3.4 億遞增到 4.6 億）：連 2 季偏離 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉。"},{"id":"H2","text":"HIV 治療護城河撐過政府議價：Biktarvy 處方地位不動，PrEP 與新方案（Bixlenvo、IS/LEN）補上 2028 年的價格缺口，2028 年 HIV 營收仍高於 2027 年。","2y":"2027 年 HIV 營收年增 ≥5%（庫存回吐後）","5y":"2028 年 HIV 營收不低於 2027 年；2030 年 Biktarvy 美國治療市占 ≥50%；2026–2030 年 HIV 營收年複合成長 ≥3%","10y":null,"threshold":"2028 年 HIV 營收不低於 2027 年；Biktarvy 美國市占 ≥50%","source":"2028 年初正式財測、季報與法說（2026-10-29 Andrew Dickinson：預期 2028 年 HIV 總營收、總產品銷售與 EPS 都會成長）","drift_rule":"HIV 營收 TTM 對照每年成長 3% 的路徑：連 4 季偏離 ≥5% 為削弱，連 6 季偏離 ≥10% 為反轉。"},{"id":"H3","text":"多角化降低 HIV 集中度：Trodelvy 一線、Livdelzi、anito-cel 與發炎管線，讓非 HIV 營收占比由約 25% 升到 35% 以上。","2y":"2027 年 Trodelvy ≥23 億美元；anito-cel 於 2026-12-23 獲核准","5y":"2031 年非 HIV 營收占產品銷售 ≥35%；Trodelvy ≥30 億美元","10y":"2036 年 Biktarvy 專利到期時，非 HIV 占比 ≥45%，發炎領域至少有一項上市產品","threshold":"2027 年 Trodelvy ≥23 億美元；anito-cel 獲核准；emvistegrast 於 2027 年進入三期","source":"季報與法說（2026-10-29：Trodelvy 年化約 20 億、HIV 約占七成、發炎 13 項臨床計畫）","drift_rule":"5 年期：非 HIV 營收 TTM 對照路徑，連 4 季偏離 ≥5% 為削弱、連 6 季偏離 ≥10% 為反轉；10 年期：跨 2 個年度偏離為削弱，跨 3 個年度為反轉。"}],"R":[{"id":"R1","text":"Yeztugo 放量在第二年失速：受保險覆蓋、Apretude 與 Merck 月服口服 PrEP 競爭影響，PrEP 長期共識已由 77 億下修到 67 億。","h_ref":"H1","clock":"🔥","threshold":"FY2027 Yeztugo 低於 16 億美元，或排除第四季後連 2 季季增低於 5%","evidence_refs":["supply_demand_durability#2","substitute_technology#1"]},{"id":"R2","text":"政府定價外溢超出預期：Biktarvy 2028 年 Medicare 價格比牌價低約 38%，並外溢到 Medicaid、340B；另有 Medicaid MFN；政府價格計算方法可能被挑戰並重編；病人援助計畫受加強審查。","h_ref":"H2","clock":"🔥","threshold":"公司揭露的 2028 年淨影響超過 20 億美元，或下一輪議價名單再納入 HIV 主力產品","evidence_refs":["end_markets#3","regulatory_antitrust#0","regulatory_antitrust#1"]},{"id":"R3","text":"關稅、供應鏈與通路的單點風險：Section 301 於 2026-07 生效，品牌藥最高 100% 關稅且豁免不保證；Section 232 暫停只到 2028 年底；原料有相當比例來自美國以外，部分只有單一供應商，另有 BIOSECURE；加州設施有天災風險；三大批發商占總毛銷售 74%。","h_ref":"H2","clock":"🐢","threshold":"非 GAAP 產品毛利率連 2 季低於 86%，或任一大批發商信評降到投資級以下","evidence_refs":["reg_tariff_export#1","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#4","regulatory_antitrust#3","customer_concentration_credit#0"]},{"id":"R4","text":"訴訟：TDF（Viread／Truvada）產品責任約 23,000 名原告，2027-03 首場 bellwether；HIV 反壟斷私人訴訟（Aetna 州法院案）續行。","h_ref":"H2","clock":"⚡","threshold":"原告勝訴且含懲罰性賠償，或訴訟準備超過 20 億美元","evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#2"]},{"id":"R5","text":"多角化執行風險：2026 年約 129 億美元併購（約為市值 6%）的回報未證；細胞治療 Q3 年減 18%；KITE-753 遭部分臨床暫停、月服口服 3107 遭臨床暫停，2025 年 GS-1720／GS-4182 也曾被暫停；in vivo CAR-T 威脅既有細胞治療。","h_ref":"H3","clock":"🐢","threshold":"anito-cel 未獲核准，或 2027 年 Trodelvy 低於 23 億美元，或 2027 年再有一項關鍵臨床遭暫停","evidence_refs":["major_events#3","substitute_technology#2"]}],"single_thing":{"description":"2028 年初公司的正式財測顯示 2028 年 HIV 營收低於 2027 年，推翻 2026-10-29 管理層「HIV、總營收與 EPS 在 2028 年仍成長」的說法。","why_fatal":"HIV 約占產品銷售七成五，Biktarvy 約占一半。這個數字是政府議價、PrEP 放量、新方案替換三股力量的淨結果，也是本檔估值中敏感度最大的單一數字。一旦 HIV 轉為年減，市場會把 GILD 從成長股重新歸類為專利懸崖前的成熟藥廠，倍數往下回落。","if_happens":"減碼至半倉；若同時 Biktarvy 美國市占跌破 50%，清倉。上調空頭機率，並重跑判斷。","how_monitor":"每季的 HIV 年增率與 Yeztugo 季銷售；公司對 2028 年 Biktarvy 淨影響的更新（目前約 15 億美元）；2028 年初的正式財測。","probability":"12–24 個月內約 25%：管理層過去兩年吸收 Part D 改制約 11 億、ACA 等政策 5 億以上衝擊，說法有紀錄支撐；但 15 億只是初步估計，外溢拆分也沒給。"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.1,"peg_fy2":1.77,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":6.78,"FY2026E":-0.45,"FY2027E":9.91,"FY2028E":10.73},"fy_end_month":12,"eps_basis":"FY2025A 是 GAAP 稀釋 EPS 6.78 美元（事實表 financial_history，yfinance 年度財報）；FY2026E–FY2028E 是 Koyfin 共識（2026-10-31 快照），應為非 GAAP 且含 acquired IPR&D，FY2026E 因一次性費用而為負。基期與共識口徑不一致，三年 CAGR 不宜機械計算。判斷改用乾淨口徑：2026 年排除一次性的中點 8.925 美元到 FY2028E 的 10.73 美元，年增約 9.6%。財年止於 12 月。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GILD_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"高毛利、高自由現金流；2022–2025 年營收年增僅約 2.6%，2026 年轉為雙位數；單一產品約占半數營收；價格受政府議價管制。"},"industry":{"clock_phase":"II","sd_verdict_source":"2026-10-29 法說（基礎業務年增 16%、Biktarvy 美國市占 53%、美國 PrEP 市場年增 14%）與 2026-09-30 10-Q","bargaining":{"up":"原料與中間體有相當比例來自美國以外，部分只有單一供應商。供應商議價權低，風險在供貨中斷，不在價格。","down":"美國銷售經三大批發商：Cardinal 29%、McKesson 24%、Cencora 21%（2025 年合計 74%）。批發商只配送、不定價；真正的議價者是 Medicare、Medicaid、340B 與保險，議價權正往付款端移動。","geo":"Section 232 關稅依 2025-12 協議暫停三年；Section 301 全球關稅 2026-07 生效，公司稱即使目前符合豁免，也不保證未來不適用。"},"profit_pool_dir":"HIV 利潤池正由每日口服往長效劑型（治療與預防）移動，GILD 兩端都握在手上；但池中被政府取走的部分在擴大（2028 年 Biktarvy 淨影響約 15 億美元）。","tam_table":[{"item":"美國 PrEP 市場成長","value":"2026 Q3 年增 14%；長效針劑需求年增一倍"},{"item":"GILD PrEP 份額與規模","value":"約 50%（Yeztugo 加 Descovy for PrEP），年化約 40 億美元"},{"item":"PrEP 劑型結構","value":"每日口服約占 80%～85%（2026-08-04 法說），長效仍屬低滲透"},{"item":"HIV 治療","value":"Biktarvy 美國市占 53%；治療市場尚未回到 2%～3% 常態成長，已見止穩"},{"item":"全球感染者","value":"逾 4,000 萬人，44% 尚未達到病毒抑制"},{"item":"TAM 金額、各段 CAGR 與營業利益池五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"HIV 處方慣性與換藥風險：病毒已抑制的患者換藥有病毒反彈風險，醫師傾向不動，所以 Biktarvy 份額在學名藥與兩藥療法並存下仍升到 53%。加上自有的 lenacapavir 長效平台同時覆蓋治療（Bixlenvo、IS/LEN）與預防（Yeztugo 半年針、週口服、年針），下一代劑型也留在自家手上。專利與學名藥和解後指向 2036-04。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Biktarvy 美國市占 53% 創新高，PrEP 份額 50%，Yeztugo 成為長效針劑預防第一（2026-10-29 法說）。定價面縮減：CMS 定出 Biktarvy 每 30 天 2,600 美元，Medicare 通路比牌價低約 38%，2028 年淨影響約 15 億美元；另有 2025-12 協議下的 Medicaid MFN。兩者相抵為穩定。前份判加深，本次因議價價格定案而下修一級。","peer_na_reason":"事實表的同業資料只有利潤率與研發密度，沒有 ROIC、投入資本與估值倍數，所以利差方向與終端倍數的同業對照無法建立。","threats":[{"level":"🟡","text":"學名藥：舊一代 HIV 方案已有學名藥搶份額（10-K 風險因子）；Biktarvy 與學名藥商和解後專利指向 2036-04，五年內主力產品不受影響。","p":"10%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"兩藥療法：Merck Idvynso 2026-04 獲 FDA 核准，但不適用初治患者；ViiV Dovato 對 Biktarvy 影響被 RBC 評為微小。這條證據引用的報導是 2020 年舊文，2026 年的實際份額影響以 Biktarvy 市占 53% 創新高為準。","p":"10%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"Merck 月服口服 PrEP（MK-8527）兩項療效試驗預估 2027 年完成，與 Yeztugo 半年針及 GILD 自家週口服直接競爭；屬點對點競爭，GILD 有週口服與年針兩種對應方案。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"in vivo CAR-T 免除細胞採集與製造，對 Yescarta 與 anito-cel 這類 ex vivo 產品構成架構性壓力；但細胞治療只占產品銷售約 4%，GILD 也已在中國啟動 in vivo BCMA CAR-T 試驗，以公司層級看屬點對點。","p":"30%","evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率，周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"HIV 治療是終身用藥，屬需要而非想要；全球逾 4,000 萬感染者、44% 尚未達到病毒抑制（2026-10-29 Dietmar Berger）。使用者是患者、決策者是醫師、付款者是保險與政府，三個角色清楚。付款端有摩擦（ACA 變動、Florida ADAP 調整），但沒有讓 Biktarvy 份額下滑。PrEP 屬預防，延後的代價低、對給付更敏感，是需求面較弱的一段。"},{"item":"決策層級","level":"🟢","text":"替代性要看醫師對單一病毒已抑制患者的換藥決策：換藥有病毒反彈風險，Biktarvy 份額在學名藥與兩藥療法並存下仍升到 53%，RBC 也評 Dovato 對 Biktarvy 影響微小。Yeztugo 再注射率超過 70%，長效針的留存同樣高。"},{"item":"價值鏈分配","level":"🟡","text":"三大批發商占總毛銷售 74%，但它們只配送、不定價。真正分走價值的是付款端：通路組合只要移動 1%，季度實現價格就會大幅波動（2026-10-29 Johanna Mercier）；340B、Medicaid best price 與 2028 年 Medicare 議價把更多價值移給政府與保險。藥廠在價值鏈中仍最難被取代，但分配比例在往付款端移。"},{"item":"社會容忍度","level":"🔴","text":"實際定價上限已由政治上限決定。CMS 定出 Biktarvy 每 30 天 2,600 美元，Medicare 通路比牌價低約 38%，2028 年淨影響約 15 億美元。2025-12 協議接受 Medicaid MFN、Epclusa 直接對患者價，以及海外漲價須回饋美國。10-Q 另揭露政府價格計算方法可能被挑戰並重編、病人援助計畫受加強審查。CEO 公開稱這是 pill penalty。此項已列入反證紀錄。"}],"roiic":"約 5%～10%（推估，無法驗證）","reinvest_rate":"約 60%","endo_ceiling":4.5,"formula_note":"當期 ROIC：稅後營業利益率約 29%（TTM 營益率 36.2% 乘以 1 減 20% 稅率）乘以投入資本周轉率，周轉率事實表未涵蓋，所以算不出。增量報酬：2022→2025 年 GAAP 營業利益由約 110 億（272.8 億×40.2%）到約 117 億（294.4 億×39.7%），三年只增約 7 億，同期做了多次大型併購與授權（事實表 financial_history，yfinance 年度財報）；2026 年 Trodelvy、Livdelzi 等併購資產開始放量，故取 5%～10% 推估。再投資率：2026 年前三季公司把約四成自由現金流回饋股東，其餘約六成用於併購與降債。內生成長上界約 7.5%×60%，約 4.5%（單位 %）。研發是費用化，這條公式會低估由內部研發推動的成長，lenacapavir 就是自有研發。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","GILD":79.51,"AMGN":69.52,"BMY":69.24,"VRTX":86.0,"MRK":71.31,"unit":"%"},{"metric":"營業利益率","GILD":36.23,"AMGN":29.99,"BMY":29.19,"VRTX":37.95,"MRK":0.87,"unit":"%"},{"metric":"FCF 利潤率","GILD":39.59,"AMGN":26.71,"BMY":18.56,"VRTX":30.16,"MRK":18.72,"unit":"%"},{"metric":"研發密度","GILD":20.8,"AMGN":20.03,"BMY":21.1,"VRTX":32.09,"MRK":53.19,"unit":"%"}],"competitors":[{"name":"AMGN","gm":69.52,"om":29.99,"fcf_margin":26.71,"rd_intensity":20.03,"strategy_note":"營益率與研發密度接近 GILD，自由現金流率低一截；同為大型成熟生技，是終端倍數的同類參照，倍數事實表未涵蓋。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BMY","gm":69.24,"om":29.19,"fcf_margin":18.56,"rd_intensity":21.1,"strategy_note":"營益率與自由現金流率都明顯低於 GILD，顯示 GILD 的現金產生力在同業前段。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"VRTX","gm":86.0,"om":37.95,"fcf_margin":30.16,"rd_intensity":32.09,"strategy_note":"利潤率結構最接近（毛利率 86%、營益率 38%），不在 HIV 正面競爭，可作為高利潤生技的估值上緣參照；倍數事實表未涵蓋。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MRK","gm":71.31,"om":0.87,"fcf_margin":18.72,"rd_intensity":53.19,"strategy_note":"TTM 營益率僅 0.9%，應含大額一次性費用，事實表未拆。在 HIV 是直接對手：Idvynso 兩藥療法已上市，月服口服 PrEP 預估 2027 年完成療效試驗。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主、價為輔、併購補管線：2026 年 HIV 成長來自需求、通路組合帶來的價格與庫存；PrEP 市場年增 14%；Trodelvy +42%、Livdelzi +93% 都是量；2028 年起價格轉負（Medicare 議價）；淨回購每年約 0.3%～0.5%，貢獻小。","runway_years":"5～9 年（HIV 治療份額已過半，PrEP 長效仍低滲透；Biktarvy 專利到 2036）","runway_post_y5":"🟡","endo_ceiling_basis":"報酬持續期檢核：增量報酬約 5%～10%（推估）乘再投資率約 60%，約每年 4.5%","segments":[{"item":"HIV（治療加預防）","value":"2026 Q3 62 億美元，年增 18%（價格、需求、庫存）；全年預期年增約 12%；約占產品銷售七成五"},{"item":"Biktarvy","value":"Q3 41 億美元，年增 10%；美國治療市占 53%；2028 年 Medicare 議價淨影響約 −15 億美元"},{"item":"PrEP（Descovy 加 Yeztugo）","value":"Descovy 10 億美元（+49%，約八成為 PrEP）；Yeztugo 3.05 億（季增 31%，全年約 10 億）；PrEP 合計年化約 40 億、份額 50%"},{"item":"肝病","value":"9.27 億美元，年增 13%；Livdelzi 2.03 億（+93%）"},{"item":"Trodelvy","value":"5.06 億美元，年增 42%，年化約 20 億；一線三陰性乳癌已在美歐核准"},{"item":"細胞治療","value":"3.55 億美元，年減 18%，全年預期年減中雙位數；anito-cel FDA 決定日為 2026-12-23"},{"item":"Veklury","value":"全年約 3 億美元，持續下滑"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"非 GAAP 產品毛利率 88%，去年同期 86%"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"Biktarvy 美國市占 53% 創新高；PrEP 份額 50%"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"Q3 價格與需求同時為正"},{"signal":"EPS 成長顯著高於營收成長（差距超過 5pp）","lit":false,"note":"乾淨口徑 EPS 2026→2028 年增約 9.6%，營收 2026→2027 共識 +7.2%，差約 2.4pp；GAAP 口徑因 2025 年基期失真，不採用"},{"signal":"FCF/NI 連 2 年低於 0.75","lit":false,"note":"2025 年 1.11、2023 年 1.31；2024 年受 IPR&D 費用扭曲"},{"signal":"SBC/營收超過 5% 且逐年上升","lit":null,"note":"事實表未涵蓋 SBC"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"HIV 治療市場尚未回到 2%～3% 常態成長，但已止穩；PrEP 市場年增 14%；列為觀察"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"Q3 資本支出 2.37 億，對比 FCF 47.98 億"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"至 2030 年在美國投資 320 億美元；2026 年 Foster City 新廠動土"}],"trap_rating":"🟢"},"quality":{},"governance":{"capital_returns":[{"item":"2026 Q3 股東回饋","value":"約 14 億美元，含回購 3.7 億"},{"item":"2026 年前三季回饋占自由現金流","value":"約 40%（上半年約 49%）"},{"item":"股息","value":"殖利率約 1.9%，每年約 40 億美元"},{"item":"2026 年 acquired IPR&D","value":"約 129 億美元（Arcellx、Tubulis、Ouro，含第四季 PepStar 與 Vir 約 14 億前期付款）"},{"item":"淨負債","value":"約 183 億美元（總債務 262 億減現金 80 億）"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2022→2025 年營業利益只增約 7 億美元，同期做了多次大型併購；細胞治療 2026 Q3 年減 18%。Trodelvy 年化約 20 億、Livdelzi 年增 93% 已轉好，但併購對價事實表未涵蓋，已實現回報看不出超過資金成本；2026 年再花約 129 億 acquired IPR&D，尚無營收。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購規模小（Q3 3.7 億美元，年化約 15 億，約為市值 0.7%）。以 2026 年排除一次性 EPS 中點 8.925 美元對股價 169.44 美元，盈餘殖利率約 5.3%；10 年期公債殖利率事實表未涵蓋，無法判定是否過門檻。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數由 2022 年約 12.6 億股（淨利 45.92 億除以 EPS 3.64）降到 2025 年約 12.55 億股（85.10 億除以 6.78），目前流通約 12.40 億股；股數淨減少，淨稀釋率低於每年 1.5%。","grade":"過"}]},"valuation":{"basis":"以 FY2027 共識前瞻本益比為主、PEG 為輔；情境樹用營收乘終端 EV/S，因為 FY2026 共識 EPS 受一次性費用影響而為負","tier":"大型成熟生技","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或 EV/S 現值，無法建倍數對照；改以 GILD 自身四個年度端點與 52／104／250 週均線作錨。"},"fwd_pe":17.1,"peg":1.77,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"FY2027 本益比 17.1 倍（169.44 除以 9.91）。PEG 1.77（17.1 除以 9.6，成長率取 2026 年排除一次性 8.925 到 FY2028 共識 10.73 的年增率），落在 1～2 的合理區。但 P/S、EV/S 都在四個年度端點之上；情境樹基本情境五年價格報酬約 3.9%，機率加權約 −1.5%，加上股息年化約 3%。合理的 PEG 配上自身歷史最高的倍數與偏弱的期望報酬，判偏貴（🟠）。短期上行：FY2028 共識 10.73 乘 15.5 倍，約 166 美元（−1.9%）；中期：基本情境 2031 年終端價約 176 美元（+3.9%）。","upside_short_pct":-1.9,"upside_mid_pct":3.9},"trap_analysis":{"verdict":"🟢","label":"衰退信號零亮燈；風險在估值與政府定價，不在生意衰退"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2026-10-29 CMS 定出 Biktarvy 每 30 天 2,600 美元（Medicare 比牌價低約 38%），公司估 2028 年淨影響約 15 億美元，並外溢到 Medicaid、340B。分析師質疑 Yeztugo 的持久性，PrEP 長期共識由 77 億下修到 67 億。Merck 月服口服 PrEP 2027 年完成療效試驗。","assumption":"管理層所說 2028 年 HIV、總產品銷售與 EPS 仍高於 2027 年成立。","consequence":"如果外溢大於預期、PrEP 又在第二年失速，2028 年 HIV 年減，市場會把 GILD 重新歸類為專利懸崖前的成熟藥廠，倍數回落，對應空頭情境約 −53%。","ruling":"部分採納。公司吸收 2025 年 Part D 改制約 11 億、2026 年 ACA 等政策 5 億以上衝擊的紀錄可信；但 15 億只是初步估計，外溢拆分也沒給。空頭機率給 30%。這個視角與 Single Thing 是同一命題（2028 年 HIV 是否仍成長），已對帳，不另設。","watch":"2027 年各季 HIV 年增率、Yeztugo 季銷售、2028 年初正式財測","evidence_refs":["end_markets#3","supply_demand_durability#2","substitute_technology#1"],"fact_refs":["f_kpi6_fy2026"]},{"view":"論點成功但股東經濟變差","evidence":"份額與營收照計畫成長，價值卻被付款端與併購分走。2025-12 協議接受 Medicaid MFN、Epclusa 直接對患者價，以及海外漲價須回饋美國；10-Q 揭露政府價格計算方法可能被挑戰並重編，病人援助計畫受加強審查；2026 年 acquired IPR&D 約 129 億美元，約為市值 6%。社會容忍度是持續期四個檢查點中唯一的紅燈。","assumption":"排除 IPR&D 的營益率維持在 45%～50%，且併購資產在 2028 年後產生營收。","consequence":"營收成長，但每股盈餘成長低於營收；自由現金流被持續的併購吃掉，股東報酬只剩股息。","ruling":"採納為主要結構風險。基本情境已讓終端 EV/S 由 7.3 倍降到 5.8 倍，反映政治定價上限；若 2027 年併購金額仍超過 50 億美元、又沒有對應的上市時程，停止加碼。","watch":"排除 IPR&D 的非 GAAP 營益率（現為 49%）、年度 acquired IPR&D 金額、下一輪 Medicare 議價名單","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"],"fact_refs":["f_kpi2_non_gaap","f_ev_m"]},{"view":"價格已反映太多","evidence":"股價 169.44 美元，26 週漲 29%，高於 52 週均線約 24%；P/S 6.8 倍、EV/S 7.4 倍都高於過去四個年度端點；FY2027 本益比 17.1 倍。","assumption":"市場假設 2026 年的成長速度與利潤率可以延續到 2030 年代。","consequence":"即使基本面照基本情境走，五年價格報酬也只有約 4%，加上股息年化不到 3%；成長回到中個位數時，倍數還會往下。","ruling":"採納。這是本次不追價的唯一綁定約束，論點本身未破。","watch":"股價對 FY2027 共識 EPS 的倍數；回到約 13.6 倍（135 美元）以下才有安全邊際","evidence_refs":[],"fact_refs":["f_price_at_dd","f_week26_return_pct","f_ma_w52","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"TDF 產品責任訴訟約 23,000 名原告，聯邦首場 bellwether 2027-03 開審；HIV 反壟斷私人訴訟（Aetna 案）可在州法院續行；品牌藥最高 100% 關稅，Section 301 已於 2026-07 生效且豁免不保證；部分產品與物料只有單一供應商或單一設施。","assumption":"訴訟與關稅只造成一次性的現金或成本衝擊，不動搖處方地位。","consequence":"如果 bellwether 判決不利並帶出大額和解，或關稅讓產品毛利率掉回 86% 以下，EPS 路徑下移，倍數再受壓。","ruling":"反駁為非致命。金額事實表未涵蓋，但性質是民事訴訟與成本項，不改變 Biktarvy 與 PrEP 的需求。保留觸發器，不放進情境主路徑。","watch":"2027-03 bellwether 判決；非 GAAP 產品毛利率","evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#2","reg_tariff_export#1","reg_tariff_export#3","geo_supply_chain#1"],"fact_refs":[]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 134.36 → 本次 169.44（+26.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=134.36","side_b":"本次 price_at_dd=169.44","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 134.36 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 134.36 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 134.36 美元：Bull 價 254.77、Bear 價 80.16，五年期望值 +24.3%，基準年化 5.6%，不對稱比 1.85","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.85。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 134.36 美元：五年期望值 +24.3%，基準年化 5.6%，不對稱比 1.85","side_b":"本次情境、股價 169.44 美元：五年期望值 −1.5%，基準年化 0.8%，不對稱比 0.8","ruling":"再換股價、情境不動：起點價上漲 26.1%，五年期望值少 25.7 個百分點，基準年化少 4.8 個百分點，不對稱比由 1.85 降到 0.8。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷","cause":null,"side_a":"多空雙方都同意：Biktarvy 處方地位仍在加強（市占 53%），自由現金流強（TTM 自由現金流率 39.6%），2026 年財測多次上調（基礎業務較年初中位數 +16.5 億美元）。","side_b":"爭點只有兩處：2028 年後政府定價的累積幅度，以及現價是否已經計入。","ruling":"一致的部分不再重辯，判斷集中在定價與估值。","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"估值與整體評級（前份到本次）","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-05-25，股價 134.36 美元）：估值判為便宜，整體 A+；機率與最大回撤未給。","side_b":"本次（股價 169.44 美元，+26%）：估值判偏貴，整體降為 B；本輪首次給出機率（多頭 25%、基本 45%、空頭 30%）與最大回撤 −35%～−55%。","ruling":"價格是主因。股價由 134.36 美元漲到 169.44 美元，以本次 FY2027 共識 9.91 美元換算，倍數由約 13.6 倍升到 17.1 倍。基本面的新證據（Medicare 議價）只讓整體降一級；若股價沒漲，估值結論會停在合理偏低。空頭 30% 反映估值已在四年高點，且共識成長超過內生成長上界。","evidence_level":"高","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若股價回到 135 美元以下且 HIV 季年增仍 ≥3%，分批反買","反向：若股價續漲到 205 美元以上而 2028 年展望未上修，減碼三分之一"],"evidence_refs":[]},{"axis":"護城河方向與價值陷阱（前份到本次）","cause":"新證據","prior_field":["moat_trend","trap"],"side_a":"前份：護城河加深；價值陷阱風險低。","side_b":"本次：護城河穩定（執行擴大、定價縮減，兩者相抵）；價值陷阱風險仍低。","ruling":"2026-10-29 CMS 定出 Biktarvy 每 30 天 2,600 美元（Medicare 比牌價低約 38%），公司估 2028 年淨影響約 15 億美元。前份風險三寫的「IRA 把 Biktarvy 列入→削弱 H2」已經發火。定價權因此降一級，護城河方向由加深改為穩定。衰退信號仍零亮燈，價值陷阱判斷不變。","evidence_level":"高","settle_metric":"Biktarvy 美國治療市占（現為 53%），以及 2028 年 HIV 營收是否高於 2027 年","if_then":["若 2028 年 HIV 營收財測低於 2027 年，減碼至半倉","反向：若 2027 年 Biktarvy 市占維持 53% 以上，且公司把 2028 年淨影響下修到 10 億以下，護城河方向可回到擴大"],"evidence_refs":["end_markets#3"]},{"axis":"本輪新增欄位（前份未填）","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position"],"side_a":"前份：舊格式，以上欄位皆未填。","side_b":"本次：五年後成長空間判中等；公司類型判品質複利成長（次類為受監管公用），信心中；屬非循環股，不填循環位置；裁決與角色由程式依本次輸入重算。","ruling":"前份是舊格式，未要求這些欄位，本輪依新格式補齊。這不是價格或基本面造成的變動。","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"行動門檻與 Single Thing（前份到本次）","cause":"方法變動","prior_field":["rearm_trigger","kill_metrics","single_thing"],"side_a":"前份：Single Thing、kill_metrics、重啟條件皆未設定（空值）。","side_b":"本次 Single Thing：2028 年初正式財測若顯示 2028 年 HIV 營收低於 2027 年，減碼至半倉；若同時 Biktarvy 美國市占低於 50%，清倉。重啟條件：股價 ≤135 美元，且最近一季 HIV 年增 ≥3%。kill_metrics 五條：Yeztugo 年銷售、HIV 季年增率、2028 年財測、Biktarvy 市占、產品毛利率。","ruling":"前份格式未要求，本輪新設。觀望的綁定約束是估值，所以重啟條件是對價格的否定。Single Thing 選 2028 年 HIV 是否成長，因為它是政府議價、PrEP 放量、新方案替換三股力量的淨結果，數學上敏感度最大。","evidence_level":"中","settle_metric":"2028 年 HIV 營收對比 2027 年","if_then":["若股價 ≤135 美元且 HIV 季年增 ≥3%，分批反買","若 Single Thing 發生，減碼至半倉；若同時 Biktarvy 市占低於 50%，清倉"],"evidence_refs":["end_markets#3"]},{"axis":"Yeztugo 門檻（前份到本次）","cause":"方法變動","prior_field":["thesis.H1","thesis.R1"],"side_a":"前份 R1：「Q3 26 Yeztugo < $250M 或 Q4 < $350M → 全年 $1B guide 風險；連 2 季 QoQ < 30% growth → R1 觸發」；前份 H1：「FY27 ≥ $2B」。","side_b":"本次：FY2027 Yeztugo 低於 16 億美元，或排除第四季季節性後連 2 季季增低於 5%，即停止加碼。","ruling":"季增 30% 的門檻只適用上市第一年。Q3 實際 3.05 億、季增 31%，已過前份 2.5 億的門檻；但前三季合計約 7.0 億、全年指引約 10 億，代表第四季幾乎持平（公司稱是假期季節性），照舊門檻第四季必然誤觸。因此改用年度絕對額。FY2027 門檻由 20 億下修到 16 億，因為賣方已把 PrEP 長期共識由 77 億下修到 67 億、第四季季增也在放緩；這是新證據帶動的方法調整。","evidence_level":"高","settle_metric":"FY2027 Yeztugo 年銷售","if_then":["若 FY2027 Yeztugo 低於 16 億美元，停止加碼","反向：若 2027 年上半年合計 ≥8 億美元，H1 確認，維持持有"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"管理層說法與做法：併購節制","cause":null,"side_a":"2026-08-04 CFO Andrew Dickinson：今年不預期再做大型併購，近期重心是整合 Arcellx、Tubulis、Ouro。","side_b":"2026-10-29：同意收購 PepStar 的口服 IL-23R 計畫並簽下 Vir 合作，第四季前期付款約 14 億美元；全年 acquired IPR&D 由 115 億上修到 129 億。","ruling":"可調和，屬程度差異。14 億美元不到市值 1%，符合當時留下的『機會主義』但書；但全年已花約 129 億、約為市值 6%，併購回報尚未證明。這不改變論點，列入資本配置監測。","evidence_level":"高","settle_metric":"2027 年 acquired IPR&D 金額，以及 2026 年收購資產的臨床里程碑","if_then":["若 2027 年 acquired IPR&D 超過 50 億美元且沒有對應的上市時程，停止加碼","反向：若 anito-cel 在 2027 年取得第四線以上領先，且 emvistegrast 進入三期，維持持有"],"evidence_refs":[]},{"axis":"Q3 HIV 成長的品質","cause":null,"side_a":"需求面：Biktarvy 美國市占 53% 創新高，PrEP 市場年增 14%，HIV 年增 18%。","side_b":"Q3 含高於往常的庫存建置，以及通路組合帶來的價格（Johanna Mercier：庫存年底前正常化，第四季庫存建置會小於往常）。2026-08-04 法說預期治療市場回到 2%～3% 成長，2026-10-29 改口為「尚未回到、僅見止穩」。","ruling":"可調和。需求是真的，但 18% 不是可以外推的速度，2027 年 HIV 成長應回到中個位數；基本情境把 2027 年營收放在略低於共識，就是反映這一點。","evidence_level":"中","settle_metric":"2027 年第一季 HIV 營收年增率（庫存回吐後）","if_then":["若 2027 Q1 HIV 年增低於 3%（庫存回吐超過預期），停止加碼並下修基本情境","反向：若 ≥8%，H2 加分，維持持有"],"evidence_refs":[]},{"axis":"賣方共識修正方向的讀法","cause":null,"side_a":"事實表把 FY2026 共識近 3 個月修正記為 −40%，看起來是大幅下修。","side_b":"實際是由 −0.75 美元上修到 −0.45 美元（虧損縮小 0.30 美元），負數分母讓百分比的符號顛倒。另外，−0.45 高於公司指引的 −1.20～−0.85，快照可能還沒計入第四季約 14 億美元的前期付款。FY2027、FY2028 共識在兩次快照間持平。","ruling":"裁定為上修，不是下修。FY2028 共識在 2028 年 IRA 影響揭露後沒動，可能是快照未更新，也可能早已計入，現有證據無法分辨。新利空還無法確認是否已進入賣方模型，因此凍結加碼到下一份快照為止，不據此加減分。","evidence_level":"中","settle_metric":"下一份共識快照的 FY2028 EPS","if_then":["若 FY2028 共識下修超過 5%，表示 IRA 影響原先未計入；維持基本情境，但重新檢查 2028 年營收路徑"],"evidence_refs":[]},{"axis":"現在就賣與現在就買的最強論證","cause":null,"side_a":"賣：26 週漲 29%，P/S 與 EV/S 都在四個年度端點的最高位，2028 年 Biktarvy 少 15 億，我們的基本情境五年價格報酬只有約 4%。","side_b":"買：基礎業務年增 16% 是十年來最快；管理層公開承諾 2028 年總營收與 EPS 仍成長；lenacapavir 平台涵蓋半年針、週口服、年針三種 PrEP；FY2027 本益比 17 倍，對應約 10% 的 EPS 成長。","ruling":"不賣也不追。論點未破，但估值已走在前面：持有者續抱，空手者等價格。","evidence_level":"中","settle_metric":"股價對 FY2027 共識 EPS 的倍數，以及 2027 年 HIV 季年增率","if_then":["若股價 ≤135 美元且 HIV 季年增仍 ≥3%，分批反買","若股價 ≥205 美元且 2028 年展望未上修，減碼三分之一"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Yeztugo 第二年放量是否達標","type":"假設驗證","maps_to":"H1","metric":"Yeztugo 年銷售與季增率","threshold":"FY2027 低於 16 億美元，或排除第四季季節性後連 2 季季增低於 5%","action":"停止加碼","source_freq":"公司季報新聞稿／每季","date":"2027-02","evidence_refs":["supply_demand_durability#2"]},{"n":2,"text":"2028 年 HIV 營收是否仍高於 2027 年","type":"Single Thing","maps_to":"Single Thing","metric":"2028 年正式財測的 HIV 營收對比 2027 年實際","threshold":"財測低於 2027 年實際","action":"減碼至半倉；若同時 Biktarvy 美國市占低於 50%，清倉","source_freq":"Q4 2027 財報與 2028 年財測／每年","date":"2028-02","evidence_refs":["end_markets#3"]},{"n":3,"text":"政府定價外溢擴大","type":"風險","maps_to":"R2","metric":"公司揭露的 2028 年 Biktarvy 淨影響；下一輪 Medicare 議價名單","threshold":"淨影響上修到 20 億美元以上，或名單再納入一個 HIV 主力產品","action":"停止加碼","source_freq":"季報法說／CMS 每年 2 月名單","date":"2027-02","evidence_refs":["end_markets#3","regulatory_antitrust#0","regulatory_antitrust#1"]},{"n":4,"text":"關稅與供應鏈成本吸收失敗","type":"風險","maps_to":"R3","metric":"非 GAAP 產品毛利率","threshold":"連 2 季低於 86%（現為 88%）","action":"停止加碼","source_freq":"季報法說／每季","date":null,"evidence_refs":["reg_tariff_export#3","geo_supply_chain#0"]},{"n":5,"text":"TDF 產品責任首場 bellwether","type":"風險","maps_to":"R4","metric":"判決結果與公司訴訟準備","threshold":"原告勝訴且含懲罰性賠償，或訴訟準備超過 20 億美元","action":"停止加碼","source_freq":"法院判決／10-Q","date":"2027-03","evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":6,"text":"anito-cel FDA 決定","type":"假設驗證","maps_to":"H3","metric":"FDA 決定","threshold":"未獲核准（收到完整回覆函）","action":"停止加碼","source_freq":"公司公告／一次性","date":"2026-12-23","evidence_refs":[]},{"n":7,"text":"Merck 月服口服 PrEP 療效讀數","type":"風險","maps_to":"R1","metric":"MK-8527 兩項療效試驗結果","threshold":"療效不劣於每日口服，且安全性乾淨","action":"停止加碼","source_freq":"Merck 公告／一次性","date":"2027","evidence_refs":["substitute_technology#1"]},{"n":8,"text":"估值回到安全邊際","type":"估值rearm","maps_to":null,"metric":"股價對 FY2027 共識 EPS 的倍數","threshold":"股價 ≤135 美元（約 13.6 倍），且最近一季 HIV 營收年增 ≥3%","action":"分批反買：分三批加回目標倉位","source_freq":"每日股價／每季財報","date":null,"evidence_refs":[]},{"n":9,"text":"深度回檔加碼","type":"加碼","maps_to":"H2","metric":"股價與 H1、H2 狀態","threshold":"股價 ≤120 美元（104 週均線附近），且 H1、H2 未削弱","action":"加碼至目標倉位上限","source_freq":"每日股價／每季財報","date":null,"evidence_refs":[]},{"n":10,"text":"估值過度延伸","type":"減碼","maps_to":null,"metric":"股價對 FY2027 共識 EPS 的倍數","threshold":"股價 ≥205 美元（約 20.7 倍），且 2028 年展望未上修","action":"減碼三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":11,"text":"HIV 護城河反轉","type":"清倉","maps_to":"H2","metric":"2028 年 HIV 營收與 Biktarvy 美國市占","threshold":"2028 年 HIV 營收年減，且 Biktarvy 美國市占低於 50%","action":"清倉","source_freq":"季報法說","date":"2028-02","evidence_refs":[]},{"n":12,"text":"複審：Q4 財報、2027 年財測、週口服 PrEP 的 FDA 決定","type":"複審日期","maps_to":null,"metric":"2027 年財測與 HIV 成長","threshold":null,"action":"重跑完整判斷","source_freq":"一次性","date":"2027-02-15","evidence_refs":[]}],"kill_metrics":[{"metric":"Yeztugo 年銷售","bear_threshold":"FY2027 低於 16 億美元","window":"FY2027（每季追蹤路徑 3.4 到 4.6 億）","source":"公司季報新聞稿","last_status":"ok"},{"metric":"HIV 營收季年增率","bear_threshold":"連 2 季低於 3%","window":"2027 Q1 至 2027 Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"2028 年 HIV 營收財測對比 2027 年實際","bear_threshold":"財測低於 2027 年實際","window":"2028 年初","source":"Q4 2027 財報與 2028 年財測","last_status":"unknown"},{"metric":"Biktarvy 美國治療市占","bear_threshold":"低於 50%（現為 53%）","window":"每季","source":"公司法說會","last_status":"ok"},{"metric":"非 GAAP 產品毛利率","bear_threshold":"連 2 季低於 86%（現為 88%）","window":"每季","source":"公司法說會非 GAAP 損益","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場拿 2026 年 Q3 外推成長（HIV 年增 18%，其中含庫存建置與通路價格的加分），並把 2028 年 Medicare 議價當成一次性缺口。我們認為政府定價是持續的壓力，且在 2036 年專利到期前終端倍數會回落；基本情境五年價格報酬只有約 4%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=29.26, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價回到 135 美元以下（約 FY2027 共識 EPS 的 13.6 倍），且最近一季 HIV 營收年增仍 ≥3%","exec_line":"持有者續抱、不追價。股價 ≤135 美元且 HIV 季年增 ≥3% 時，分三批加回；≥205 美元且 2028 年展望未上修時，減碼三分之一。Single Thing 發生就減碼至半倉，若 Biktarvy 市占再跌破 50% 則清倉。最大回撤可能到 −35%～−55%，論點未破時不因波動砍倉。"},"reasoning":{"industry":"營收分部（2026 Q3，總營收 83 億美元、產品銷售 82.89 億）：HIV 62 億（年增 18%；Biktarvy 41 億、Descovy 10 億、Yeztugo 3.05 億）、肝病 9.27 億（+13%；Livdelzi 2.03 億）、Trodelvy 5.06 億（+42%）、細胞治療 3.55 億（−18%）；Veklury 全年約 3 億。利潤率：GAAP 營業利益 34.62 億（約 42%），非 GAAP 營業利益 41.68 億（約 50%）；TTM 毛利率 79.5%、營益率 36.2%、自由現金流率 39.6%。單點依賴：Biktarvy 約占 Q3 產品銷售五成、HIV 合計約七成五，這既是護城河證據，也是集中度風險；美國通路的三大批發商合計 74%，最大一家 29%。供需持久性屬結構性：HIV 是終身用藥，Biktarvy 美國市占 53% 創新高，PrEP 市場年增 14%。持久的是量，價格由政策決定，2028 年 Medicare 通路價格比牌價低約 38%。產業態勢是雙向拉鋸：需求結構轉好（長效 PrEP 需求年增一倍、GILD PrEP 份額 50%），法規軸惡化（Medicare 議價、Medicaid MFN、Section 301 關稅），競爭軸大致靜態（兩藥療法對 Biktarvy 影響微小）。產業時鐘判 II（擴張），依據是 2026 年基礎業務年增 16%、為 2015 年以來最快，PrEP 市場也是雙位數成長；唯一保留是 HIV 治療市場還沒回到 2%～3% 的常態成長。財測方面，FY2026 產品銷售上調到 310～313 億美元。全年非 GAAP EPS −1.20～−0.85 美元，負值來自約 129 億美元 acquired IPR&D 一次性費用，排除後為 8.75～9.10 美元（2026-10-29 Andrew Dickinson）。","moat":"可證方向有兩條。第一是份額：Biktarvy 美國治療市占 53%，為歷史新高；兩藥療法（ViiV Dovato、Merck Idvynso）沒有動搖它。第二是對同業的利潤率：TTM 營益率 36.2%，低於 VRTX 的 38.0%，高於 AMGN 的 30.0% 與 BMY 的 29.2%；自由現金流率 39.6% 是五家最高。MRK 營益率 0.9% 應含一次性費用，不拿來比較。事實表缺同業 ROIC 與歷年資料，利差方向無法判斷，所以綜合分不給到 8。評分：執行 8，商業執行強，但細胞治療年減 18%，KITE-753 遭部分臨床暫停、月服口服 3107 遭臨床暫停；定價權 7，產品毛利率 88%、Biktarvy 專利到 2036，但價格上限已由政治決定。兩項合為 B。威脅四項皆屬點對點，不扣分。報酬持續期：需求基礎值與決策層級為綠，價值鏈分配黃，社會容忍度紅；增量報酬偏低，內生成長上界約每年 4.5%。","growth":"成長拆解：2026 年以量為主（PrEP、Biktarvy 份額、Trodelvy、Livdelzi），價格也是正貢獻（通路組合、PrEP 定價），但 2028 年起價格轉負；回購每年淨減股約 0.3%～0.5%，貢獻小；併購補的是 2028 年後的管線，目前尚無營收。共識：FY2026 營收 312.9 億到 FY2027 335.5 億（+7.2%，24 位分析師）；EPS 為 FY2027 9.91、FY2028 10.73 美元（Koyfin，家數事實表未涵蓋）。GAAP 口徑三年 CAGR（2025 年 6.78 到 2028 年 10.73）約 16.5%，但基期是 GAAP、共識是非 GAAP，口徑不一致，不採用。乾淨口徑是從 2026 年排除一次性的中點 8.925 美元到 FY2028 的 10.73 美元，年增約 9.6%。內生上界約每年 4.5%，缺口約 5pp，主要來自利潤率擴張：TAF 權利金到期使產品毛利率 +2pp，費用槓桿把營益率推到 49%。這部分可以歸因，但 2027 年後不會重複；淨回購很小，收購尚無營收貢獻。成長空間方面，Biktarvy 美國市占 53%（落在 35%～70% 區間），專利到 2036。PrEP 長效是已上市的第二條曲線，每日口服仍占 80%～85%。真正要在 2031 年後接住 Biktarvy 的腫瘤與發炎尚未證明：發炎 13 項臨床計畫多在二期，emvistegrast 2027 年才進三期。因此判為中等。衰退信號十項零亮燈，另有兩項資料缺口（SBC、產業倍數歷史）。","governance":"自由現金流轉換：2025 年 FCF 94.56 億除以淨利 85.10 億為 1.11，2023 年為 1.31（事實表 financial_history，yfinance 年度財報）；2026 Q3 FCF 47.98 億（營業現金流 50.35 億減資本支出 2.37 億）。SBC 占營收事實表未涵蓋。現金去向：股息每年約 40 億（殖利率 1.92% 乘市值約 2,102 億），回購年化約 15 億，2026 年併購與授權約 129 億，資本支出很小；前三季約四成 FCF 回饋股東（上半年約 49%），淨負債約 183 億。三項計分如下。併購已實現的增量報酬未過：2022→2025 年營業利益只增約 7 億，細胞治療年減 18%；Trodelvy 與 Livdelzi 已轉好，但併購對價事實表未涵蓋。回購收益率無法判定：缺 10 年期公債殖利率，以排除一次性 EPS 計算的盈餘殖利率約 5.3%。股數淨稀釋這項通過：稀釋股數由 2022 年約 12.6 億降到 2025 年約 12.55 億。管理層 2026-08-04 說今年不再做大型併購，10-29 又加了約 14 億的前期付款；金額不到市值 1%，但併購仍是這家公司資本配置的最大變數。","valuation":"現價 169.44 美元，對 FY2027 共識 EPS 9.91 美元為 17.1 倍、對 FY2028 的 10.73 美元為 15.8 倍；前瞻 EV/S 7.3 倍、P/S 6.8 倍，都高於過去四個年度端點（分位 100；只有四個點，不是真正的五年分位）。現價隱含什麼：要有 8% 年報酬（股息約 2%），2031 年股價需約 225 美元；以 15 倍計，EPS 需約 15 美元，等於從 2026 年排除一次性的 8.9 美元起每年成長約 11%，還要穿過 2028 年 IRA 缺口。這只有多頭情境做得到。基本情境下 2031 年 EPS 約 12 美元、本益比約 15 倍，價格報酬約 4%。賣方目標價（2026-04 約 157.93 美元、2026-07 約 159.28 美元，區間 120～180）都早於最近兩次財測上調，已過時；但現價高於兩者，方向上不支持追價。同業倍數事實表未涵蓋，終端倍數只能用自身歷史端點與均線作錨。","premortem":"最可能看錯的地方有三個。第一，Q3 HIV 年增 18% 含庫存與通路價格的加分，管理層已說年底前會正常化。第二，2028 年 Biktarvy 約 15 億的淨影響只是初步估計，外溢拆分未給：Akash Tewari 追問時，Johanna Mercier 拒絕拆分。第三，多角化接棒：細胞治療年減、兩個管線遭臨床暫停，2026 年約 129 億的併購尚無營收。看錯的代價主要是估值回落：股價高於 52 週均線約 24%，回到 104 週均線 119.56 美元約 −29%；空頭終點約 80 美元，約 −53%。衰退信號零亮燈，價值陷阱風險低。法說迴避紀錄：HIV 營收占比連兩季都沒給數字，ISL/LEN 的淨經濟性未回應，Descovy 價格只說可維持『到某個程度』。"},"plain":{"six":{"how_it_makes_money":"賺的是美國 HIV 患者與高風險族群的終身用藥錢（HIV 約占產品銷售七成五、Biktarvy 約五成）。處方權在醫師與患者手上，GILD 握得很牢；淨價卻卡在付款端，由 Medicare 議價、Medicaid、340B 與通路組合決定，政府正把一部分定價權收回。","moat":"護城河方向穩定：執行面在擴大，定價面在縮減。機制是 HIV 每日單錠的處方慣性加上 lenacapavir 長效平台，病毒已抑制的患者很少換藥；但 2028 年起 Medicare 議價把 Biktarvy 價格壓低約 38%，價格上限改由政府決定。","growth":"五年後成長空間中等：HIV 治療份額已過半、2036 年專利到期；長效 PrEP 是已上市的第二條曲線，但腫瘤與發炎能否在 2031 年後接棒，目前還沒有證據。","capital":"資本配置中等：現金產生力強、配息穩定、股數沒有被稀釋；但約六成自由現金流投入併購與授權，增量報酬還沒有證明。","valuation":"偏貴。現價要求 2031 年 EPS 約 15 美元、並維持 15 倍以上本益比，才有 8% 年報酬，等於要穿過 2028 年 IRA 缺口仍年增約 11%。只有多頭情境做得到，我們不相信現價有安全邊際。","how_wrong":"最可能看錯的是把 2026 年的高點當常態。生意衰退的風險低，看錯的代價是估值回落。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場拿 2026 年 Q3 外推成長（HIV 年增 18%，其中含庫存建置與通路價格的加分），並把 2028 年 Medicare 議價當成一次性缺口。我們認為政府定價是持續的壓力，且在 2036 年專利到期前終端倍數會回落；基本情境五年價格報酬只有約 4%。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 135 美元以下（約 FY2027 共識 EPS 的 13.6 倍），且最近一季 HIV 營收年增仍 ≥3%","trap":"🟢","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":169.44,"week26_return_pct":29.26,"consensus_rev_3m_pct":-40.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 共識 EPS（−0.45 美元）為負，來自約 129 億美元 acquired IPR&D 一次性費用；公司給的排除口徑是 8.75～9.10 美元。估值分母改用 FY2027 共識 9.91 美元，分母本身不是爭點。另外，GILD 的非 GAAP 不排除 acquired IPR&D，未來每一筆授權都會直接壓低當年的非 GAAP EPS。"},"catalysts":[{"date":"2026-11-08","date_precision":null,"type":"product","event":"ACR 年會公布 IRAK4 抑制劑 edecesertib 二期 COSMIC 數據（皮膚紅斑性狼瘡）","impact":"低","watch":"發炎管線第一個概念驗證是否乾淨"},{"date":"2026-11","date_precision":"month","type":"product","event":"AASLD 公布 Livdelzi 三期 IDEAL 完整數據","impact":"低","watch":"能否把適用族群擴到約一半的二線患者，以及 2027 年的標籤更新"},{"date":"2026-12-23","date_precision":null,"type":"regulatory","event":"anito-cel 用於第四線以上多發性骨髓瘤的 FDA 決定日","impact":"中","watch":"是否核准、標籤的安全性內容；以及公司 18 個月內取得第四線以上領先的目標"},{"date":"2026-12","date_precision":"month","type":"product","event":"Trodelvy 三期 ASCENT-GYN（子宮內膜癌）結果更新","impact":"中","watch":"結果是否正向，決定 Trodelvy 能否拿到第三個適應症"},{"date":"2027-02","date_precision":"month","type":"regulatory","event":"每週口服 lenacapavir PrEP 的 FDA 決定（預期 2027-02 初）","impact":"中","watch":"是否核准，以及能否沿用 Yeztugo 約七成的藥品給付覆蓋"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年財測","impact":"高","watch":"HIV 成長是否回到中個位數、Yeztugo 2027 年目標、acquired IPR&D 預算"},{"date":"2027-03","date_precision":"month","type":"other","event":"TDF 產品責任訴訟聯邦首場 bellwether 審判","impact":"中","watch":"判決方向與是否含懲罰性賠償"},{"date":"2027","date_precision":null,"type":"product","event":"PURPOSE-365 年針 PrEP 三期更新（目標 2028 年上市）","impact":"高","watch":"療效與注射部位反應；結果決定 2028 年後的 PrEP 成長"},{"date":"2027","date_precision":null,"type":"regulatory","event":"IS/LEN 每週口服治療方案的 FDA 決定","impact":"中","watch":"核准時程與淨價；2026-08 法說未回應是否稀釋 Biktarvy 的經濟性"},{"date":"2027","date_precision":null,"type":"other","event":"Merck 月服口服 PrEP（MK-8527）兩項療效試驗預估完成","impact":"中","watch":"療效是否不劣於每日口服"},{"date":"2028-01-01","date_precision":null,"type":"regulatory","event":"Biktarvy Medicare 議價價格生效（每 30 天 2,600 美元）","impact":"高","watch":"外溢到 Medicaid、340B 的實際幅度"},{"date":"2028-02","date_precision":"month","type":"guidance","event":"2028 年正式財測","impact":"高","watch":"HIV 營收是否高於 2027 年（Single Thing）"}],"_projected_from":"v19"}
```
