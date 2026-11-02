你是 stock-analyst v20 的**散文層（prose）agent**，標的 NOW（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：NOW　日期：2026-11-02　archetype：None　前份裁決：2026-07-23　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1885B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（1050B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（995B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1752B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1175B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（495B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1782B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2218B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4914B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3967B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1885           3580-5115      5 條（2–6 內）  
s3                  8000        1050           4865-6950      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3922          7755-11078      5 條（2–6 內）  
s6                 11000         495          7353-10505      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1782           1203-1718      3 條（2–6 內）  
s10                 5000        2218           1947-2782      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3967           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5728B；至少需散文≈39.27KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45
−45%
−40%
−31.5%
−30
−30%
−6.33
−3.4%
0
0.2%
0.43%
0.75
0.98
1%
1.00
1
01
1.1
1.2
1.25
1.5
1.67
1.8
02
2
2.1
2.15%
2.2
2.46%
2.5
2.6
03
3
3%
3.1
3.3%
3.4
3.4%
3.7
3.8%
3.85
3.9%
3.97
4%
04
4
4.2
4.35
4.5
4.60
4.62
4.72
4.75
4.80
4.8
4.83
4.95
5.0
5%
05
5
5.4%
5.7
5.70
5.92
6
6.15
6.33
6.49
6.7
7
07
7.5
7.75
08
8%
8
8.06
8.22
8.85
9
9.4%
9.68%
10
10%
10.1%
10.4
10.5
10.7
11
11%
11.2%
11.4
12
12%
12.1%
12.6
12.7%
13%
13
13.0%
13.1%
13.38
13.9%
14
14%
14.3%
15
15%
15.2%
15.31
15.4%
16%
16.25%
16.8
17
17.4%
17.48
17.5%
17.8%
18%
18.5%
18.7%
19%
19
19.75%
20%
20
20.5
21%
21
21.52%
21.76
21.8
22%
22
22.1%
22.5%
23
24
24.7
24.7%
25
25%
26
26.48
26.5
26.86
28%
28
28.5
30%
30
31
31.5%
32%
32.5%
32.6%
33
35%
36%
38
38.08
39.88
40%
40
41.06
42
42.8%
43.69%
45
45%
45.33
46.07
47.1%
49
50
50%
53.5
54.55%
57.6
58
60
60%
65%
66.3%
68
70
70.5%
72
73.08%
75
75.6
77.5
77.53%
78%
80%
81%
83.1%
84.15
90
95
95%
95.46
97%
98%
100
100%
105.12
118.75
123
131.1
136.5
140
150%
158
162.3
162.34
164
$164
192.68
248
265
278.2
297
300
320
500%
500
658
680
900
2023
2025
2026
2027
2028
2029
2030
2031
20261102
1,091
1,500
4,963
8,126
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
{"meta":{"ticker":"NOW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"ServiceNow, Inc."},"oneliner":"ServiceNow 向大企業收工作流平台訂閱費，續約率 98%，AI 合約價值目標一年內兩度上調；現價約 21.8 倍明年共識 EPS，估值合理但不便宜，成敗看 2027 年 1 月的財測能否守住 18% 訂閱成長。","thesis":{"H":[{"id":"H1","text":"工作流系統記錄層（CMDB、工作流資料、代理治理）讓大企業留下來：AI 代理要在企業裡動手，仍得經過 ServiceNow，續約與大客戶擴張不會退","2y":null,"5y":"2031 年前續約率維持 97% 以上，年 ACV 逾 500 萬美元的客戶數每年增加 8% 以上（2026 第三季 680 家、第二季 658 家）","10y":null,"threshold":"續約率 ≥97%；大客戶數年增 ≥8%","source":"公司季度新聞稿與法說（續約率、大客戶數）","drift_rule":"五年期：門檻偏離連 4 季 ≥5% 判削弱，連 6 季 ≥10% 判反轉"},{"id":"H2","text":"AI 與用量計價是淨增量：AI ACV 的成長補得上座位制放緩，Armis 滿一年後，訂閱營收固定匯率成長仍守在 18% 以上","2y":null,"5y":"2030 年 AI 占 ACV 約 30%（CFO 2026-05-04 設定的目標），訂閱營收朝 300 億美元以上前進","10y":null,"threshold":"2026 年底 AI ACV ≥17 億美元；2027 年第二季起訂閱營收固定匯率 ≥18%","source":"第四季財報與每季法說（AI ACV、訂閱營收固定匯率成長）","drift_rule":"五年期：門檻偏離連 4 季 ≥5% 判削弱，連 6 季 ≥10% 判反轉"},{"id":"H3","text":"股東經濟同步改善：利潤率照承諾擴張、股票薪酬占比下降，EPS 複利不需要倍數回升","2y":"2027 年非 GAAP 營益率較 2026 年的 31.5% 擴張至少 100bp（CFO 2026-05-04 承諾），股票薪酬占營收降到 14% 以下（2026 第三季為 15.4%），FY2027 EPS 不低於 4.60","5y":null,"10y":null,"threshold":"營益率擴張 ≥100bp；股票薪酬占營收 ≤14%；FY2027 EPS ≥4.60","source":"第四季財報的年度財測、每季新聞稿、Koyfin 共識","drift_rule":"兩年期：連 2 季偏離 ≥5% 判削弱，連 3 季 ≥10% 判反轉"}],"R":[{"id":"R1","text":"成長減速與共識下修循環：第四季 cRPO 財測 18.5%，低於前三季；三年共識 EPS 三個月內各降 2–3%，看起來便宜，有一部分是因為分母在降","h_ref":"H2","clock":"🔥","threshold":"cRPO 固定匯率 <17.5% 連 2 季；FY2027 共識 EPS <4.60","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"]},{"id":"R2","text":"AI 代理與競爭重劃預算：Salesforce Agentforce IT 服務管理、微軟捆綁銷售、企業用 AI 工具自建，加上座位制轉用量計價，可能把應用軟體利潤率壓縮 100–900bp（彭博行業研究）；要到 2027–28 年續約潮才看得到結果","h_ref":"H1","clock":"🐢","threshold":"續約率 <97% 連 2 季，或非 GAAP 訂閱毛利率 <78% 連 2 季","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","substitute_technology#2","substitute_technology#3","supply_demand_durability#2"]},{"id":"R3","text":"聯邦與事件風險：單一聯邦通路夥伴占營收升到 13%（2025 年 11%）；DOJ 調查政府合約合規問題，公司已通報陸軍停權除名辦公室，無法預測結果；中東衝突曾讓 2026 年第一季大型地端交易延後，拖累訂閱成長約 75bp","h_ref":"H1","clock":"⚡","threshold":"遭起訴或收到停權通知；該夥伴占營收 >15%","evidence_refs":["customer_concentration_credit#2","regulatory_antitrust#0","major_events#3","geo_supply_chain#0"]},{"id":"R4","text":"舉債併購的報酬未驗證：Armis 約 77.5 億美元現金收購，部分以 40 億美元定期貸款支應，淨負債 38 億美元；12 個月內完成三筆收購","h_ref":"H3","clock":"🔥","threshold":"2027 年營益率擴張 <50bp，或再宣布單筆 >50 億美元收購","evidence_refs":["ma_merger#1"]}],"single_thing":{"description":"2027 年 1 月下旬第四季財報給出的 2027 年訂閱營收財測，固定匯率成長低於 18%","why_fatal":"基礎情境 2027–2028 年 EPS 年增約 20%，靠的是約 19–20% 的訂閱營收成長加上利潤率擴張。財測低於 18%，等於公司自己承認 AI 沒能補上座位制的放緩。營收成長率是 EPS 路徑裡敏感度最大的一項，倍數也會跟著往空頭的 15 倍靠攏。","if_happens":"減碼至半倉並重跑研究；空頭機率由 30% 上調到 40% 以上，停止一切加碼，直到 Armis 滿一年後的 cRPO 證明成長守住 17.5%","how_monitor":"看第四季財報新聞稿與法說中的年度財測。事前先看兩件事：第四季 cRPO 實際值是否高於財測的 18.5%，以及 FY2027 共識營收（目前 192.68 億美元，隱含約 18.7% 成長）有沒有變動","probability":"約 25%（12–24 個月內）。管理層 2026 年兩次都只把一半超標傳遞到全年，財測偏保守；但第四季 cRPO 財測已經降到 18.5%"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":21.76,"peg_fy2":0.98,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":3.97,"FY2027E":4.83,"FY2028E":5.92},"fy_end_month":12,"eps_basis":"non-GAAP 稀釋 EPS（Koyfin 共識，與 2026 第三季非 GAAP 稀釋 EPS 1.00 同口徑）；分析師家數事實表未涵蓋。FY2025 非 GAAP 實際值事實表未涵蓋；GAAP 的 1.67 口徑不同，不代入"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"訂閱占營收 97%、續約率 98%、訂閱成長約 20%（固定匯率）、全年非 GAAP 營益率 31.5%、自由現金流利潤率 36%、股票薪酬占營收約 15%"},"industry":{"clock_phase":"II","sd_verdict_source":"需求屬結構性持久。企業 AI 從試驗走向上線，治理與流程執行是必要支出，RPO 年增 22.5% 且合約年期在拉長（CFO 2026-10-28）。不過定價模式正由座位轉向用量，利潤怎麼分配還在變動；彭博行業研究估計應用軟體利潤率可能因此壓縮 100–900bp。","bargaining":{"up":"上游是超大型雲端與模型商。公司轉向超大型雲端，短期壓低了毛利率（CFO 2026-05-04、2026-07-22）；管理層稱模型已商品化、可以改用較便宜的模型（Zavery 2026-07-22）。上游議價力判為中等。","down":"下游是大型企業與政府。年 ACV 逾 500 萬美元的客戶 680 家，續約率 98%；單一聯邦通路夥伴占營收 13%，但這家夥伴背後是多個聯邦機關。","geo":"中東衝突曾讓 2026 年第一季的大型地端交易延後；公司與 Aramco Digital 簽有橫跨 50 多國的協議；出口管制與關稅屬制式風險揭露。"},"profit_pool_dir":"利潤池正往 AI 模型與算力層移動，公司想當代理的受治理執行層來接住這部分。目前的證據是外部代理經 Action Fabric 呼叫公司平台時仍按次計費，但利潤池往哪邊走尚未定案。","tam_table":[{"item":"企業應用軟體支出 2026 年","value":"4,963 億美元，年增 13.9%（美元）、12.7%（固定匯率）；Gartner 2026 第三季預測，經第三方部落格轉述"},{"item":"企業應用軟體支出 2030 年","value":"8,126 億美元；2026–2030 年隱含年複合成長約 13.1%（8,126÷4,963 開四次方）"},{"item":"公司滲透率（營收÷支出）","value":"2026 年約 3.3%（今年共識營收 162.3 億÷4,963 億）；若 2030 年達到公司訂閱目標 300–320 億美元，約 3.7–3.9%"},{"item":"SAM 與分段成長率","value":"事實表未涵蓋（IT 服務管理、資安、CRM 各段的市場規模都未收錄）"},{"item":"營業利益池占比（5 年前到現在）","value":"事實表未涵蓋，無法判斷利益池是否淨流出 5 個百分點以上"},{"item":"預測下修訊號","value":"Gartner 把 2027 年總額較上一季預測下修 25 億美元，相對 4,963 億美元的規模不到 1%"}]},"moat":{"mechanism":"工作流系統記錄層的轉換成本（CMDB、工作流資料、代理治理），再加上多產品綁定","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力在擴大：連續超過財測，吸收併購稀釋後營益率仍擴張 50bp。定價權穩定偏弱：AI 方案漲價 20–30%，但毛利率下滑，又以導入服務讓利。兩者合計判持平。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只有毛利率、營益率、自由現金流利潤率與研發密度","threats":[{"level":"🔴","text":"生態攻擊：Salesforce 推出 Agentforce IT 服務管理，切入公司本業；微軟以 Copilot 與代理平台捆綁銷售。10-K 自述，系統記錄廠商可能阻擋整合，或以捆綁降價施壓。公司在投資人日稱競爭名單裡看不到這些對手（2026-05-04），但沒有提供贏率數字；第三季前 20 大交易中，IT 服務管理仍占 11 筆。","p":30,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"點對點替代：AI 原生的點解決方案，以及企業用 AI 寫程式工具自建流程；10-K 自述公司正與替代做法競爭。本次沒有列為架構替代，理由是外部代理（ChatGPT、Gemini）經 Action Fabric 呼叫時，工作仍在公司平台內執行並按次計費，附著點長在公司的 CMDB 與工作流上。升級條件：若 Action Fabric 用量停止揭露，或訂閱毛利率連 2 季低於 78%，就升為架構替代並重評論點。","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#2","substitute_technology#3"]},{"level":"🟡","text":"定價模式轉換：座位制改為用量或成果計價。彭博行業研究估計應用軟體利潤率可能壓縮 100–900bp；CFO 稱客戶完全沒有要求成果計價（2026-10-28），但一半新增 ACV 已經不是座位計價。這項風險已反映在定價權評分，不另扣分。","p":40,"evidence_refs":["supply_demand_durability#2"]}],"roic_durability":{"quadrant":"推定為高利益率×高周轉：非 GAAP 營益率約 32%，訂閱預收款讓營運資金為負。投入資本事實表未涵蓋；計入併購商譽後，周轉率會下降。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（員工與 IT 人員）、決策者（CIO、CEO）、付款者（企業預算）三方一致。IT 服務、資安與 AI 代理治理是營運必要支出，延後購買的代價是停機與資安事件。代理變數：續約率 98%、RPO 年增 22.5%。"},{"item":"決策層級","level":"🟡","text":"替代與否在企業平台層決定。搬遷要移走 CMDB、重建流程、重新訓練員工，合約年期也拉長到 5 年（Experian、Maybank，2026-07-22）。但 AI 導入代理讓搬遷變快：公司自稱用 Sweep 把 CRM 導入縮短到 30–60 天，同樣的工具對手也能拿來搬走公司的客戶。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈上游是模型商與超大型雲端，前端是 ChatGPT、Gemini 等介面。公司以 Action Fabric 讓外部代理在平台內執行並按次計費，目前拿得到錢；但 TTM GAAP 毛利率由 77.53% 降到 73.08%，顯示成本端分走了一部分。CFO 稱 AI 推論成本不到服務成本的 10%（2026-05-04）。"},{"item":"社會容忍度","level":"🟢","text":"屬企業對企業軟體，沒有監管授權形成的價格上限。敏感點在政府採購：DOJ 正在調查政府合約合規問題，單一聯邦通路夥伴占營收 13%；這屬於事件風險，不構成定價天花板。"}],"roiic":"事實表未涵蓋投入資本與收購後營業利益，無法計算增量 ROIC","reinvest_rate":"2026 年被併購墊高：Armis 約 77.5 億美元現金對價，已超過第三季非 GAAP 營業利益的年化值約 53.5 億美元（13.38 億×4，未稅）。資本支出、折舊與營運資金變動事實表未涵蓋。","endo_ceiling":20,"formula_note":"內生成長率＝增量 ROIC×再投資率，兩項數字都缺，改以有機訂閱成長作為上界代理。2026 年全年訂閱成長約 21%（固定匯率），扣除 Armis 提前併入的約 1.25 個百分點後約 19.75%，取整為 20%。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","NOW":73.08,"PLTR":84.8,"CRM":77.28,"MSFT":67.66,"DDOG":79.51,"unit":"%"},{"metric":"營業利益率","NOW":9.68,"PLTR":42.8,"CRM":21.52,"MSFT":47.1,"DDOG":0.43,"unit":"%"},{"metric":"FCF 利潤率","NOW":30.78,"PLTR":54.55,"CRM":34.49,"MSFT":17.31,"DDOG":27.04,"unit":"%"},{"metric":"研發密度","NOW":22.47,"PLTR":10.42,"CRM":14.49,"MSFT":10.52,"DDOG":43.69,"unit":"%"}],"competitors":[{"name":"PLTR","gm":84.8,"om":42.8,"fcf_margin":54.55,"rd_intensity":10.42,"strategy_note":"爭奪企業 AI 營運層的預算，營益率 42.8%、自由現金流利潤率 54.55%，都遠高於公司；和公司流程系統記錄層的重疊有限，屬預算競爭，不是直接替換。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CRM","gm":77.28,"om":21.52,"fcf_margin":34.49,"rd_intensity":14.49,"strategy_note":"以 Agentforce 推 IT 服務管理，正面切入公司本業，還能和既有 CRM 捆綁銷售；GAAP 營益率 21.52%，高於公司，打價格戰的承受力較強。公司則反向用 Sweep 把 CRM 導入縮短到 30–60 天，去搶對方客戶。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"MSFT","gm":67.66,"om":47.1,"fcf_margin":17.31,"rd_intensity":10.52,"strategy_note":"把 Copilot 與代理平台捆綁進既有企業授權，是最大的捆綁威脅；但同時也是合作方，公司的 Control Tower 可以通知 Azure AI Foundry 切斷代理權限。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"DDOG","gm":79.51,"om":0.43,"fcf_margin":27.04,"rd_intensity":43.69,"strategy_note":"可觀測性領域與公司的 ITOM、AIOps 重疊；研發密度 43.69%、營益率 0.43%，仍在投入期，對公司屬點對點競爭。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主：既有大客戶的多產品擴張（前 20 大交易有 19 筆含 6 項以上產品）與 AI 新方案。價次之：AI 原生方案平均漲價 20–30%。併購約 1.25 個百分點（Armis）。回購只抵銷稀釋，不貢獻每股成長。","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"沿用護城河段的內生上界 20%（以有機訂閱成長為代理，增量 ROIC 無法計算）。共識 EPS 2026→2028 年年複合約 22.1%（5.92÷3.97 開根號）；三年期算法需要 2025 年非 GAAP 實際值，事實表未涵蓋。缺口約 2.1 個百分點，歸因於利潤率擴張：CFO 承諾 2027 年非 GAAP 營益率擴張 100bp（2026-05-04），淨回購為零（稀釋中性）。共識營收 2026→2027 年約年增 18.7%（192.68÷162.34）。","segments":{"expanded":false,"reason":"公司只分訂閱與專業服務兩類，訂閱占第三季營收 97%。產品線（IT、資安、CRM、AI）的營收拆分事實表未涵蓋，只有 ACV 與交易數，無法做分部三年成長。利潤由訂閱毛利決定，不取決於產品組合。"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"evidence":"TTM GAAP 毛利率 73.08%，低於 2025 年的 77.53%；第三季非 GAAP 訂閱毛利率 80%，低於全年財測 81%；CFO 在 2026-07-22 承認轉向超大型雲端與 AI 用量帶來短期壓力"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"沒有來源可證份額流失；IT 服務管理仍出現在前 20 大交易中的 11 筆；競爭者份額數字事實表未涵蓋"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"AI 原生方案漲價 20–30%，CEO 稱活躍使用者沒有下降（2026-05-04），續約率 98%"},{"signal":"EPS 成長率比營收成長率高 5 個百分點以上","lit":false,"evidence":"共識 EPS 2026→2028 年約年增 22.1%，營收 2026→2027 年約年增 18.7%，差距約 3.4 個百分點"},{"signal":"自由現金流÷淨利低於 0.75 連 2 年","lit":false,"evidence":"2025 年自由現金流 45.33 億美元÷淨利 17.48 億美元，約 2.6 倍，由股票薪酬與預收款墊高"},{"signal":"股票薪酬占營收超過 5% 且逐年上升","lit":false,"evidence":"第三季占營收 15.4%，遠高於 5%；但逐年趨勢事實表未涵蓋，公司目標是 2029 年降到 10% 以下。暫不計為亮燈，列入監測"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"企業應用軟體支出 2026 年年增 13.9%；替代技術壓縮市場的說法只有評論，沒有數字"},{"signal":"產業估值倍數近 3 年系統性下移","lit":true,"evidence":"公司本益比、股價營收比、EV/S 都落在四個年度端點中的最低點；市場以「SaaS 末日」形容整個類股。產業整體倍數事實表未涵蓋"},{"signal":"維持性資本支出占自由現金流超過 60%","lit":false,"evidence":"CFO 稱資本支出下降，自由現金流利潤率上調到 36%"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"營收 2023–2025 年每年成長 20% 以上"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"收購現金","value":"Armis 約 77.5 億美元（2026-04-20 完成，部分以 40 億美元定期貸款支應）；Moveworks 約 28.5 億美元（2025-12-15 完成）；Veza（2026-03-02 完成，金額事實表未涵蓋）"},{"item":"回購","value":"2026 年第一季 20 億美元加速回購，剩餘授權 42 億美元；目標 2026 年稀釋中性"},{"item":"股票薪酬","value":"第三季 6.33 億美元，占營收 15.4%；公司目標 2029 年降到 10% 以下"},{"item":"淨負債","value":"38.08 億美元（總債務 84.15 億美元、現金 46.07 億美元，含租賃負債）"},{"item":"股息","value":"事實表未涵蓋，未見股息資料"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"12 個月內完成 Moveworks（約 28.5 億美元）、Veza、Armis（約 77.5 億美元現金，其中 40 億美元為定期貸款）三筆收購；收購後的營收與利潤貢獻事實表未涵蓋，Armis 到 2026-04-20 才完成，已實現報酬還無法計算","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2026 年第一季 20 億美元加速回購，尚餘 42 億美元授權；回購均價事實表未涵蓋。以現價推算，今年共識 EPS 收益率約 3.8%（1÷26.48），自由現金流收益率約 5.4%（36%×162.3 億÷1,091 億市值）；十年期公債殖利率只要高於 3.4%，就達不到「殖利率加 2 個百分點」的門檻。回購主要是在抵銷股票薪酬","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"CFO 在 2026-05-04 稱 2026 年淨稀釋為中性；全年 GAAP 稀釋加權股數財測 10.4 億股，第四季 10.5 億股。代價是第三季股票薪酬 6.33 億美元、占營收 15.4%，要靠現金回購抵銷","grade":"過"}]},"valuation":{"basis":"以 FY2026E 與 FY2027E 共識 non-GAAP EPS 計算的前瞻本益比搭配 PEG 為主尺，扣除股票薪酬後的自由現金流收益率作交叉檢查","tier":"大型企業軟體平台（訂閱成長約 20%）","peers":{"expanded":false,"reason":"事實表的同業表只有利潤率，沒有同業前瞻本益比，無法做倍數對照；改用公司自身的四個年度端點與 PEG"},"fwd_pe":26.48,"peg":1.2,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"今年共識 non-GAAP EPS 3.97，前瞻 26.5 倍；明年 4.83，21.8 倍。FY2026→FY2028 共識 EPS 年複合約 22.1%（5.92÷3.97 開根號），PEG 約 1.2（以明年計約 0.98），落在合理區間。公司本益比、股價營收比、EV/S 都在四個年度端點中的最低點；這不是五年分位，五年分位事實表未涵蓋。扣除股票薪酬後的自由現金流收益率約 3%：36%×162.3 億−6.33 億×4，約 33 億美元，再除以 1,091 億美元市值。結論：合理，不便宜。","upside_short_pct":13.0,"upside_mid_pct":24.7},"trap_analysis":{"verdict":"🟡","label":"中等：十項衰退信號亮兩項（GAAP 毛利率下滑、自身倍數下移），股票薪酬偏高列入監測"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2026-05-04 投資人日，CFO 設定 2030 年 AI 占 ACV 30% 的目標；分析師追問這是否隱含非 AI 部分年增不到 10%，CFO 只說這樣想是錯的，沒有給數字。二手評論指出，AI 寫程式工具讓企業能自建流程，代理取代人力也會減少座位。本季訂閱成長連續三季停在 20.5–21%（固定匯率），AI 加速沒有帶動總成長。","assumption":"AI 增量足以抵銷既有產品的放緩，總訂閱成長守在 18% 以上","consequence":"五年後虧損 50% 最可能的劇本：2027–28 年續約潮出現座位縮減，前端模型商拿走使用者介面，公司淪為按次計費的後端；成長掉到個位數，利潤率被用量計價壓縮，倍數落到 12–15 倍（空頭路徑 4.80×12 倍約 58 美元）","ruling":"部分採納。空頭機率維持 30%，但不放進基礎情境，因為續約率 98%、RPO 年增 22.5% 且合約年期拉長，未來一年內看不到需求流失。不過非 AI 部分的成長數字至今沒有揭露，這是論點最大的缺口。此劇本與 Single Thing 部分重疊：2027 年財測就是它的第一個驗證數字。","watch":"2027 年訂閱營收財測、Armis 滿一年後的 cRPO 固定匯率成長、續約率","evidence_refs":["substitute_technology#0","substitute_technology#2","substitute_technology#3"],"fact_refs":["f_kpi1_subscription_revenues_ga","f_kpi9_rpo","f_kpi8_crpo"]},{"view":"論點失敗","evidence":"單一聯邦通路夥伴占 2026 上半年營收 13%（2025 年 11%）。DOJ 針對政府合約合規問題（前陸軍資訊長聘用案）展開調查，公司已通報陸軍停權除名辦公室，並表示無法預測結果。","assumption":"聯邦業務不受調查影響；CFO 稱第四季聯邦淨新增 ACV 還會再加速（2026-10-28）","consequence":"若公司遭停權，經這家夥伴的 13% 營收與其他聯邦合約都會受威脅，營收與 EPS 可能一次下移一成以上","ruling":"反駁，判為低機率事件，12–24 個月內約 5%。10-K 稱訴訟合計不會造成重大不利影響，與這家通路夥伴之間也沒有收款異常。但這屬事件風險，不能用機率平均掉，因此另設清倉條件。","watch":"10-Q 與 8-K 中的調查進度、該夥伴的營收與應收帳款占比","evidence_refs":["regulatory_antitrust#0","major_events#3","customer_concentration_credit#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"第三季股票薪酬 6.33 億美元，占營收 15.4%。12 個月內完成三筆收購，Armis 77.5 億美元現金對價中有 40 億美元靠定期貸款，淨負債 38 億美元。TTM GAAP 毛利率 73.08%（2025 年 77.53%）。第三季起為大單免費附上導入服務，把部分價值從訂閱移到專業服務。自由現金流扣除股票薪酬後，只剩營收的約 15–21%。","assumption":"利潤率照承諾每年擴張 100bp，股票薪酬在 2029 年降到營收 10% 以下，之後不再做大型收購","consequence":"AI 成功了，但錢流向股票薪酬、利息與收購溢價，每股盈餘年增落在 15% 以下，基礎情境的 IRR 掉到個位數","ruling":"採納為監測項。目前利潤率承諾有在兌現：全年營益率財測維持 31.5%，自由現金流利潤率上調到 36%，人數略降。但併購報酬還沒驗證；若再宣布逾 50 億美元的收購，就下修資本配置結論。","watch":"2027 年營益率財測、股票薪酬占營收比、收購公告","evidence_refs":["ma_merger#1"],"fact_refs":["f_kpi5_sbc","f_net_debt_m","f_peer_now_gross_margin_pct","f_peer_now_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"股價由前份的 95.46 美元升到 105.12 美元（+10.1%），同期明年共識 EPS 由 5.0 降到 4.83（−3.4%），前瞻倍數上升約 14%。2026 年春季 Goldman、BTIG、Citi 都下修了目標價；賣方目標價區間 72–248 美元，高低差 3.4 倍。","assumption":"基礎情境 EPS 已放在共識下方（2027 年 4.75、2028 年 5.70），終端 21 倍也低於現值 26.5 倍","consequence":"共識若再下修 5%，今年口徑的倍數會由 26.5 倍變成約 28 倍，估值由合理轉為偏貴，上檔空間被吃掉","ruling":"大致反駁。基礎情境不需要倍數回升，報酬來自 EPS 複利。但在共識連續下修期間，空頭錨會跟著往下移，所以報酬不對稱比不作為加碼依據。","watch":"FY2027 共識 EPS 是否跌破 4.60","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_rev_fy2_pct","f_consensus_eps_fy2"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 95.46 → 本次 105.12（+10.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=95.46","side_b":"本次 price_at_dd=105.12","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 衛星","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 95.46 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 95.46 美元：Bull 價 265、Bear 價 68，五年期望值 +70.5%，基準年化 11.2%，不對稱比 5.7","side_b":"本次情境、股價仍用 95.46 美元：Bull 價 278.2、Bear 價 72，五年期望值 +83.1%，基準年化 14.3%，不對稱比 6.49","ruling":"先換情境、股價不動：五年期望值多 12.6 個百分點，基準年化多 3.1 個百分點。不對稱比由 5.7 變為 6.49。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 95.46 美元：五年期望值 +83.1%，基準年化 14.3%，不對稱比 6.49","side_b":"本次情境、股價 105.12 美元：五年期望值 +66.3%，基準年化 12.1%，不對稱比 4.35","ruling":"再換股價、情境不動：起點價上漲 10.1%，五年期望值少 16.8 個百分點，基準年化少 2.2 個百分點，不對稱比由 6.49 降到 4.35。合計五年期望值比前份少 4.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論由偏便宜轉為合理","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-07-23）：股價 95.46 美元、明年共識 EPS 5.0，約 19 倍，判為偏便宜","side_b":"本次：股價 105.12 美元（+10.1%）、明年共識 EPS 4.83（−3.4%），約 21.8 倍；今年口徑 26.5 倍、PEG 約 1.2，判為合理","ruling":"估值結論降一級。倍數上升約 14%，其中約四分之三來自股價上漲，約四分之一來自共識下修。進場結論與部位角色依本次輸入重新推出。","evidence_level":"事實表數字","settle_metric":"明年共識 EPS 與股價","if_then":["若股價回到 95 美元以下，且明年共識 EPS 守在 4.60 以上→估值回到偏便宜，分批加碼","若明年共識 EPS 跌破 4.60 而股價沒跌→估值轉貴，停止加碼"],"evidence_refs":[]},{"axis":"基本面欄位經本季證據檢驗後維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、價值陷阱 🟡、護城河方向持平、五年後成長空間 🟢、屬品質複利成長、景氣位置不適用","side_b":"本次維持同值：綜合訊號 B；價值陷阱 🟡（亮兩項：GAAP 毛利率下滑、自身倍數下移）；護城河持平（續約率 98%、AI 漲價抵銷座位壓力，但毛利率下滑抵消了擴大的可能）；成長空間 🟢（只占企業應用軟體支出約 3.3%）；仍屬品質複利成長；非景氣循環股","ruling":"用新證據檢驗後不改。可能看錯的地方：毛利率若再連 2 季下降，價值陷阱升為 🔴，護城河方向改為下降。","evidence_level":"公司公布數字＋法說","settle_metric":"非 GAAP 訂閱毛利率、續約率","if_then":["若非 GAAP 訂閱毛利率連 2 季低於 78%→護城河方向改為下降並重評論點","若續約率維持 98% 且 AI ACV 達 17 億美元→維持"],"evidence_refs":[]},{"axis":"機率與回撤口徑","cause":"方法變動","prior_field":["max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：最大回撤填單點 −40%；多頭機率 28%、空頭 30%","side_b":"本次：最大回撤改填區間 −45%～−30%；多頭 25%、基礎 45%、空頭 30%","ruling":"回撤改填區間（寬 15 個百分點），下緣由空頭 EPS 配 12 倍推得。多頭機率降 3 個百分點，反映三個月內共識 EPS 下修 2–3%，以及第四季 cRPO 財測降速。空頭 30% 不變：共識 EPS 成長已超過有機營收上界，空頭機率不得低於 30%。","evidence_level":"情境假設","settle_metric":"2027 年訂閱營收財測","if_then":["若 2027 年財測 ≥18% 且共識止跌→多頭機率回調到 28%","若財測 <18%→空頭機率上調到 40% 以上"],"evidence_refs":[]},{"axis":"加碼與減碼門檻改寫","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"加碼＝站回 W104($164) 或有機 cRPO cc ≥18% 連 2 季；減碼＝有機 cRPO <16%（UBS 路徑）連 2 季或 AI ACV 淨增轉負","side_b":"加碼＝週收站回 W104（現約 158）或 2027 年第二季起 cRPO 固定匯率 ≥18% 連 2 季；減碼＝cRPO 固定匯率 <17.5% 連 2 季或 AI ACV 淨增轉負","ruling":"加碼的價格條件不變，仍是週收站回 W104，只是均線本身由 164 移到約 158。有機 cRPO 改用公司直接公布的 cRPO 固定匯率成長，因為公司沒有揭露有機拆分，前份用的是券商估算。Armis 在 2027 年第二季滿一年之前，公布值含約 1.25 個百分點的無機貢獻，所以加碼只看滿一年後的 18%，與舊門檻相同。減碼門檻 17.5%：滿一年前約等於有機 16.25%，滿一年後就是 17.5%，兩段都比舊的 16% 嚴格。AI ACV 淨增轉負的減碼條件保留。","evidence_level":"方法說明","settle_metric":"cRPO 固定匯率年增","if_then":["若 2027 年第二季起 cRPO 固定匯率 ≥18% 連 2 季→加碼一級","若 cRPO 固定匯率 <17.5% 連 2 季→減碼至半倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"Single Thing：2027 年 1 月第四季財報給出的 2027 年訂閱營收財測，固定匯率成長低於 18%；一旦發生即減碼至半倉","ruling":"前份留空。本次依敏感度挑選營收成長財測：它是 EPS 路徑裡敏感度最大的一項，而且三個月內就會有答案。","evidence_level":"方法說明","settle_metric":"2027 年訂閱營收財測","if_then":["若財測 <18%→減碼至半倉並重跑研究","若財測 ≥18%→補第二批"],"evidence_refs":[]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標（空值），門檻散在加碼、減碼條件裡","side_b":"cRPO 固定匯率 <17.5% 連 2 季→減碼；FY2027 共識 EPS <4.60→停止加碼；續約率 <97% 連 2 季→停止加碼；2027 年訂閱營收財測 <18%→減碼至半倉；非 GAAP 訂閱毛利率 <78% 連 2 季→重評；遭起訴或收到停權通知→減碼，停權確定→清倉","ruling":"本次把停損指標獨立成表，數字都取公司或共識資料直接公布的值，不用推估的有機拆分。","evidence_level":"方法說明","settle_metric":"各指標每季更新","if_then":["任一減碼門檻觸發→減碼至半倉","停權確定→清倉"],"evidence_refs":[]},{"axis":"代理繞過威脅的分級","cause":"新證據","prior_field":null,"side_a":"前份把「代理在架構上繞過工作流層」列為最高級威脅（架構替代）","side_b":"本次降為點對點觀察項：外部代理經 Action Fabric 在公司平台內執行並按次計費，Assist 用量不到 30 天成長 500%（CEO 2026-10-28）；與 OpenAI、Google 的合作也把執行環節留在公司平台","ruling":"附著點的證據目前站在「強化」這一側，但來源全是管理層。設升級條件：訂閱毛利率連 2 季低於 78%，或 Action Fabric 用量停止揭露，就升回最高級並重評論點。","evidence_level":"管理層說法（未經第三方驗證）","settle_metric":"非 GAAP 訂閱毛利率、Action Fabric 用量揭露","if_then":["若訂閱毛利率連 2 季低於 78%→升回架構替代，停止加碼","若 2027 年仍持續揭露代理用量且毛利率守住 80%→維持點對點分級"],"evidence_refs":["substitute_technology#2"]},{"axis":"AI 加速與 cRPO 降速","cause":"新證據","prior_field":null,"side_a":"管理層（2026-10-28 法說，CFO Mastantuono）說明第四季 cRPO 財測 18.5% 的原因：提前續約移到第三季（約占第三季 100bp 超標的一半）、聯邦地端比重上升（約 25bp）、T4C 條款排除約 50bp、導入服務小幅影響。CEO McDermott 稱 2027 年才會看到真正的加速。","side_b":"數字面：AI 淨新增 ACV 年增 65%、AI 消耗量成長 13 倍，但訂閱營收連續三季停在 20.5–21%（固定匯率）；cRPO 成長由第一季約 22.5% 降到第三季 21%，第四季財測 18.5%。第二季（2026-07-22）CFO 也用聯邦地端提前認列解釋超標，一次性說明一再出現。","ruling":"可調和，屬程度差異，不是方向相反。AI ACV 是增量，總成長持平代表 AI 正在補既有產品的放緩，與 H2 一致，但還沒有看到加速。對管理層的會計說明不採信也不否定，標為「未證、監測」。","evidence_level":"公司公布數字＋管理層說法","settle_metric":"2027 年第一、二季 cRPO 固定匯率成長","if_then":["若 2027 年第一、二季 cRPO 固定匯率成長都沒有回到 19% 以上→認定一次性說明不成立，停止加碼","若 Armis 滿一年後 cRPO 固定匯率 ≥18% 連 2 季→加碼一級","反向：若 cRPO 固定匯率 <17.5% 連 2 季→減碼至半倉"],"evidence_refs":[]},{"axis":"管理層承諾與兌現（對照舊逐字稿）","cause":"新證據","prior_field":null,"side_a":"承諾：CFO Mastantuono 在 2026-05-04 投資人日承諾，2027 年非 GAAP 營益率與自由現金流利潤率各擴張 100bp，2029 年股票薪酬占營收降到 10% 以下，2026 年稀釋中性。CEO McDermott 在 2026-05-04 與 2026-07-22 兩度表示年底人數會回到收購前水準。2026 年 AI ACV 目標 15 億美元。","side_b":"兌現：第三季 AI ACV 目標再上調到 17 億美元，全年營益率財測維持 31.5%，自由現金流利潤率財測由 35% 上調到 36%，CEO 稱總人數略降（2026-10-28）。新變數是第三季起為大單附上導入服務，第三季約 25bp、第四季約 50bp 的訂閱營收移到專業服務，會壓到 2027 年的毛利結構。另外，第二、三季的全年訂閱營收都只上調 1,500 萬美元，只傳遞了一半超標。","ruling":"目前言行一致，承諾沒有改口。風險在導入服務會不會變成常態（CFO 稱不會長期做），用 2027 年財測驗證。","evidence_level":"逐字稿原話","settle_metric":"2027 年非 GAAP 營益率財測","if_then":["若 2027 年營益率財測擴張 ≥100bp 且導入服務的影響沒有擴大→維持部位並補第二批","若營益率擴張 <50bp，或導入服務延伸到 2027 年下半年→停止加碼，並上調股東經濟變差情境的空頭機率"],"evidence_refs":[]},{"axis":"公司超標上調與共識下修","cause":"新證據","prior_field":null,"side_a":"公司：第三季營收、cRPO、營益率、自由現金流全數超過財測上緣，並上調全年訂閱營收與自由現金流利潤率","side_b":"賣方：2026-07-30 到 2026-10-31，FY2026、FY2027、FY2028 共識 EPS 分別下修 2.46%、3.4%、2.15%；2026 年春季 Goldman、BTIG、Citi 下修目標價；目標價區間 72–248 美元，高低差 3.4 倍","ruling":"分歧在事實層。下修原因事實表未涵蓋（可能是利息、併購稀釋，或導入服務改變了利潤結構），不能假設賣方是錯的，所以基礎情境 EPS 放在共識下方 2–4%。目標價分歧超過 2.5 倍，降低對報酬不對稱比的信心；共識連續下修期間，不對稱比不作為加碼依據。","evidence_level":"Koyfin 共識快照與賣方報告摘要（各目標價聚合站的數字彼此不一致，未驗證）","settle_metric":"FY2027 共識 EPS","if_then":["若 FY2027 共識 EPS 跌破 4.60→停止加碼","若跌破 4.35→減碼","若第四季財報後共識止跌回升→補第二批"],"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"]},{"axis":"現在就賣的最強論證","cause":"新證據","prior_field":null,"side_a":"賣方論證：同一季全面超標、AI 目標再上調，股價盤後仍下跌（Zukin 在 2026-10-28 法說提問時點出），共識 EPS 三個月連續下修；股價跌破 W52、W104、W250 三條週線均線，W250 的 13 週斜率只剩 0.2%；一次性說明連續三季出現（第二季聯邦地端提前、第三季提前續約、第四季 T4C 與導入服務），全年上調也都只傳遞一半超標","side_b":"持有論證：基礎情境不需要倍數回升（終端 21 倍低於現值 26.5 倍）；續約率 98%，RPO 297 億美元、年增 22.5%；AI ACV 一年內兩度上調，本季淨增 65%；自由現金流利潤率財測上調到 36%","ruling":"持有，第二批等財測再補。賣方最強的一點是一次性說明連續出現，這要用 2027 年第一、二季 cRPO 驗證；以現在的數字，還推不翻論點。","evidence_level":"公司公布數字＋逐字稿","settle_metric":"2027 年訂閱營收財測與 2027 年第一、二季 cRPO","if_then":["若 2027 年財測訂閱營收固定匯率成長 ≥18%，且營益率擴張 ≥100bp→補第二批","若財測 <18%→減碼至半倉","若股價先漲回 W52（約 123 美元）但財測還沒公布→不追","若股價再跌 15%，而續約率與 cRPO 都沒有受損→分批反買"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"續約率與大客戶擴張守住","type":"假設驗證","maps_to":"H1","metric":"季度續約率；年 ACV 逾 500 萬美元客戶數","threshold":"續約率 ≥97%；大客戶數年增 ≥8%（2026 第三季 680 家）","action":"任一項連 2 季未達→停止加碼並重跑研究","source_freq":"公司季報新聞稿與法說，每季","date":"2027-01"},{"n":2,"text":"AI 合約價值達標，且總成長不掉","type":"假設驗證","maps_to":"H2","metric":"AI ACV 年底值；訂閱營收固定匯率年增","threshold":"2026 年底 AI ACV ≥17 億美元；2027 年第二季起訂閱營收固定匯率 ≥18%","action":"AI ACV 未達標→停止加碼；兩項都達標→補第二批","source_freq":"第四季財報與之後每季法說","date":"2027-01"},{"n":3,"text":"利潤率承諾兌現、股票薪酬下降","type":"假設驗證","maps_to":"H3","metric":"2027 年非 GAAP 營業利益率財測；股票薪酬÷營收","threshold":"營益率財測較 2026 年 31.5% 擴張 ≥100bp；股票薪酬占營收 ≤14%","action":"營益率擴張 <50bp→停止加碼","source_freq":"第四季財報（年度財測）與每季新聞稿","date":"2027-01"},{"n":4,"text":"2027 年訂閱營收財測","type":"Single Thing","maps_to":"Single Thing","metric":"2027 年訂閱營收財測的固定匯率成長","threshold":"<18%","action":"減碼至半倉並重跑研究","source_freq":"2026 年第四季財報，一次性","date":"2027-01"},{"n":5,"text":"明年共識 EPS 持續下修","type":"風險","maps_to":"R1","metric":"FY2027 共識 non-GAAP 稀釋 EPS","threshold":"<4.60（2026-10-31 為 4.83）；<4.35 再升一級","action":"<4.60→停止加碼；<4.35→減碼","source_freq":"Koyfin 共識快照，每月","date":null,"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"]},{"n":6,"text":"DOJ 政府合約調查升級","type":"風險","maps_to":"R3","metric":"10-Q、8-K 中的調查揭露","threshold":"公司遭起訴，或收到停權、除名通知","action":"遭起訴或收到停權通知→減碼至半倉；停權確定→清倉","source_freq":"10-Q 每季、8-K 即時","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#3"]},{"n":7,"text":"聯邦通路夥伴集中度上升","type":"風險","maps_to":"R3","metric":"單一聯邦通路夥伴占營收與應收帳款的比重","threshold":"占營收 >15%，或揭露收款問題","action":"停止加碼","source_freq":"10-Q、10-K，每季","date":null,"evidence_refs":["customer_concentration_credit#2"]},{"n":8,"text":"原告律所調查轉為正式集體訴訟","type":"風險","maps_to":"R3","metric":"證券集體訴訟進度","threshold":"正式提起並獲集體認證，且出現不利和解","action":"減碼至半倉","source_freq":"10-Q 法律程序段，每季","date":null,"evidence_refs":["lawsuit_class_action#1"]},{"n":9,"text":"訂閱毛利率續降，價值被前端與雲端分走","type":"風險","maps_to":"R2","metric":"非 GAAP 訂閱毛利率","threshold":"<78% 連 2 季（第三季 80%、全年財測 81%）","action":"停止加碼，並把代理繞過威脅升為最高級後重評","source_freq":"公司季報新聞稿，每季","date":null,"evidence_refs":["supply_demand_durability#2","substitute_technology#3"]},{"n":10,"text":"再做大型收購","type":"風險","maps_to":"R4","metric":"收購公告金額","threshold":"單筆 >50 億美元","action":"停止加碼，並下修資本配置結論","source_freq":"8-K，即時","date":null,"evidence_refs":["ma_merger#1"]},{"n":11,"text":"價格或成長確認後加碼","type":"加碼","maps_to":"H2","metric":"週收盤相對 W104；cRPO 固定匯率年增","threshold":"週收站回 W104（現約 158），或 2027 年第二季起 cRPO 固定匯率 ≥18% 連 2 季","action":"加碼一級","source_freq":"週線、每季","date":null},{"n":12,"text":"成長跌破下限","type":"減碼","maps_to":"R1","metric":"cRPO 固定匯率年增；AI ACV 季度淨增","threshold":"cRPO 固定匯率 <17.5% 連 2 季，或 AI ACV 淨增轉負","action":"減碼至半倉","source_freq":"公司季報，每季","date":null},{"n":13,"text":"留存崩壞","type":"清倉","maps_to":"R2","metric":"續約率；訂閱營收固定匯率年增","threshold":"續約率 <95% 連 2 季，或訂閱營收固定匯率 <12%","action":"清倉","source_freq":"公司季報，每季","date":null,"evidence_refs":["competitive_share_entrants#2"]},{"n":14,"text":"第四季財報後重跑研究","type":"複審日期","maps_to":null,"metric":"2027 年財測與第四季實績","threshold":"財報公布","action":"重跑研究，決定第二批是否補進","source_freq":"一次性","date":"2027-01"},{"n":15,"text":"Armis 滿一年後的第一個乾淨 cRPO","type":"複審日期","maps_to":"H2","metric":"cRPO 固定匯率年增","threshold":"2027 年第二季財報公布","action":"重跑研究，檢驗一次性說明是否成立","source_freq":"一次性","date":"2027-07"}],"kill_metrics":[{"metric":"cRPO 固定匯率年增（公司公布值）","bear_threshold":"<17.5% 連 2 季","window":"2026 第四季至 2027 第四季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"FY2027 共識 non-GAAP 稀釋 EPS","bear_threshold":"<4.60（2026-10-31 為 4.83，近 3 個月 −3.4%）","window":"至 2027 年第二季財報","source":"Koyfin 共識快照","last_status":"warning"},{"metric":"季度續約率","bear_threshold":"<97% 連 2 季","window":"每季","source":"公司法說","last_status":"ok"},{"metric":"2027 年訂閱營收財測的固定匯率成長","bear_threshold":"<18%","window":"2027 年 1 月第四季財報","source":"公司財測","last_status":"unknown"},{"metric":"非 GAAP 訂閱毛利率","bear_threshold":"<78% 連 2 季","window":"每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"DOJ 政府合約調查","bear_threshold":"遭起訴或收到停權通知","window":"持續","source":"10-Q、8-K","last_status":"unknown"}],"evidence_dismissed":[{"ref":"reg_tariff_export#0","reason":"這是 10-K 的制式風險揭露，沒有金額、受影響營收或時點；同一份 10-K 的 MD&A 寫明未因總體事件影響流動性與營運。公司 97% 營收是訂閱軟體，關稅只涉及營運相關的進口，這筆證據本身對應不到任何損益數字。"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9（MA❌例外）","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 ServiceNow 當成會被 AI 代理吃掉的座位制軟體來定價，公司自身倍數落在四個年度端點的最低點。但本季數字指向相反方向：續約率 98%，RPO 297 億美元、年增 22.5% 且合約年期拉長，一半新增 ACV 已不是座位計價，外部代理經 Action Fabric 呼叫仍按次計費。市場錯在把定價模式轉換當成需求流失。若 Armis 滿一年後 cRPO 固定匯率成長連 2 季低於 17.5%，這個理由就被證偽。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=15.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"MA=❌ 但 signal≥B 且 val≤🟡 且無 Veto：依「baseline rows 9/9b/10 的 MA 條件字面不含 ❌ 時，該組合不落空、不降觀望——按對應 val 燈 baseline row 裁決，MA❌ 僅作 row4 節奏調節」推論，verdict=進場（row4 pacing 已疊加，見上）"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"單檔上限 5%；共識持續下修期間不超過 4%","requires_critic":[],"rearm_trigger":"加碼＝週收站回W104（現約158）或2027Q2起cRPO固定匯率≥18%連2季；減碼＝cRPO固定匯率<17.5%連2季或AI ACV淨增轉負","exec_line":"分兩批進場：現價先建一半。另一半等 2027 年 1 月第四季財報：2027 年訂閱營收財測固定匯率成長 ≥18%，且 FY2027 共識 EPS ≥4.60，才補進；若財測 <18%，不補，並減碼至半倉。"},"reasoning":{"industry":"2026 年第三季總營收 41.06 億美元，其中訂閱 39.88 億美元，占 97%。非 GAAP 營業利益 13.38 億美元（約 32.6%），GAAP 營業利益 3.85 億美元（約 9.4%），兩者的差距主要是股票薪酬 6.33 億美元；非 GAAP 訂閱毛利率 80%。收費方式是多年期訂閱，部分 AI 與資料方案在超出點數後按用量計價。RPO 297 億美元、cRPO 136.5 億美元，續約率 98%，年 ACV 逾 500 萬美元的客戶有 680 家。公司沒有揭露超過營收 10% 的產品分部。單點依賴落在客戶端：一家美國聯邦通路夥伴兼系統整合商占 2026 上半年營收 13%（2025 年為 11%），直銷占營收 78%。產業時鐘在擴張期，依據是企業應用軟體支出 2026 年年增 13.9%，2030 年估 8,126 億美元（Gartner，經第三方轉述）。產業態勢分三面看：競爭面，Salesforce 與微軟以 AI 代理切入 IT 服務管理，屬惡化；結構面，企業 AI 從試驗走到上線，需要治理與執行層，屬轉好，公司 AI ACV 年底目標已兩度上調到 17 億美元；其他面，座位制轉用量計價與企業自建都在變動。綜合裁決為雙向拉鋸。","moat":"機制：CMDB、工作流資料加上 20 多年的營運脈絡，讓客戶把 IT、資安、HR 流程跑在同一個平台上；第三季前 20 大交易中有 19 筆包含 6 項以上產品，要換供應商就得搬資料、重建流程並重新訓練員工。方向的證據：同業 ROIC 事實表未涵蓋，改看留存與價格兩條軸。續約率在 2026 年第二、三季都是 98%；年 ACV 逾 500 萬美元的客戶由第二季 658 家增到第三季 680 家；AI 原生方案平均漲價 20–30%（CFO 2026-05-04、2026-07-22）。反向證據：TTM GAAP 毛利率 73.08%，低於 2025 年的 77.53%；GAAP 營益率 9.68%，在同業中只高於 DDOG（CRM 21.52%、MSFT 47.1%、PLTR 42.8%）；第三季起公司為大單附上導入服務，這是讓利，不是漲價。評分：執行力 9 分，第二、三季的營收、cRPO、營益率全數超過財測上緣，做完三筆收購後人數不增反減；定價權 7 分，漲價成立，但成本端被雲端與推論分走一部分。扣掉一項生態攻擊後評為 B。報酬持續期：投入資本事實表未涵蓋，當期 ROIC 無法計算。四個檢查點兩綠兩黃，黃燈在決策層級（AI 導入代理讓搬遷時間縮短）與價值鏈分配（前端模型商與雲端拿走一部分）。","growth":"成長來源以量為主、價為輔，併購約貢獻 1.25 個百分點。跑道：公司營收約占 2026 年企業應用軟體支出的 3.3%，而這塊支出 2026–2030 年本身約年增 13%；以目前約 20% 的成長速度，要幾十年才會碰到 30% 滲透率，跑道在 10 年以上。第二條 S 曲線有來源可證：AI ACV 年底目標由 10 億、15 億一路上調到 17 億美元，第三季淨增 65%；資產管理 ACV 突破 10 億美元；CEO 稱已有 6 個事業的年化營收超過 10 億美元。AI 是否真的是淨增量：AI ACV 只計增量（CFO 2026-05-04），但被蠶食的座位收入沒有揭露。投資人日有分析師指出，2030 年 AI 占 ACV 30% 隱含非 AI 部分年增不到 10%，CFO 沒有給數字。所以淨增量只能用總訂閱成長來驗證，分界年是 2027 年（Armis 滿一年後）。附著點：外部代理經 Action Fabric 在公司資產上執行並計費，屬於強化，分界年是 2028 年（座位續約潮）。十年延伸：基礎情境第 6–10 年 EPS 年增 10%，多頭 15%。十項衰退信號亮兩項（GAAP 毛利率下滑、自身倍數下移），長期成長性評為中等。","governance":"自由現金流÷淨利：2025 年約 2.6 倍（45.33÷17.48 億美元）。轉換能力強，但主因是股票薪酬與預收款，不是利潤本身。股票薪酬第三季 6.33 億美元，占營收 15.4%；CFO 承諾 2029 年降到 10% 以下（2026-05-04）。現金去向只能列出 2026 年已知部分，三年四分法事實表未涵蓋：收購 Armis 約 77.5 億美元現金，另有 Veza（金額未知），2025 年底收購 Moveworks 約 28.5 億美元；2026 年第一季 20 億美元加速回購，尚餘 42 億美元授權；股息沒有資料；淨負債 38.08 億美元，含 40 億美元定期貸款與租賃負債。CEO 稱長期目標不含大型併購（2026-05-04），CFO 同日也把開拓新 TAM 的小型收購列為資本配置第二順位；Armis 已屬大型收購，之後若再做單筆逾 50 億美元的收購，就與這套說法衝突。營運槓桿：全年營益率財測 31.5%，較去年擴張 50bp，吸收併購稀釋後仍在擴張。","valuation":"現價 105.12 美元。今年（FY2026）共識 non-GAAP EPS 3.97，對應 26.5 倍；明年 4.83，對應 21.8 倍。GAAP 本益比 75.6 倍，差距來自股票薪酬。反推市場要求：若要五年拿到 10% 年報酬，且五年後市場給 21 倍，2031 年 EPS 需要約 8.06，年增約 15.2%（105.12×1.1 的 5 次方÷21）。基礎情境是 8.85，年增約 17.4%。我相信這個量級：前兩年有 RPO 297 億美元與 98% 續約率撐住，後面靠利潤率承諾。我不相信的是倍數會回到前幾年的水準：公司三種倍數雖然都在四個年度端點中的最低點，但整個產業正在降評，這不能當成便宜的理由。賣方方面，2026-08 聚合站的平均目標價約 140 美元，區間 72–248 美元（未驗證），高低差 3.4 倍，本次不採用賣方目標價。上檔推算：短期一年，2027 年基礎 EPS 4.75×25 倍約 118.75 美元，約 +13.0%；中期兩年，2028 年 5.70×23 倍約 131.1 美元，約 +24.7%（倍數由 26.5 倍線性降向終端的 21 倍）。","premortem":"空方最強的數字有三個：TTM GAAP 毛利率 73.08%（2025 年 77.53%）；三年共識 EPS 三個月內分別下修 2.2–3.4%；第四季 cRPO 財測 18.5%，低於第三季的 21%。管理層每季都有一次性說明：第二季是聯邦地端提前認列，第三季是提前續約（約占 cRPO 超標的一半），第四季是 T4C 條款約 50bp 加上導入服務。對這類一次性歸因，不採信也不否定，標為「未證、監測」，並事先登記驗證條件：2027 年第一、二季 cRPO 固定匯率成長若都沒有回到 19% 以上，就認定這套說明不成立。訴訟與監管：DOJ 政府合約調查的金額與時點都未揭露；原告律所在 2026-10 發出投資人調查通告，但還沒有正式提起訴訟。動能：RSI 26.86，股價低於 W52、W104、W250，屬超賣，不是過熱。歷史最大回撤數字事實表未涵蓋，回撤區間由空頭路徑推得。"},"plain":{"six":{"how_it_makes_money":"賺大型企業 IT、資安與員工服務流程的訂閱錢，訂閱占營收 97%；錢卡在企業工作流的系統記錄層，AI 代理要在企業裡動手做事，多半得經過這一層。","moat":"護城河持平。工作流系統記錄層的轉換成本還在：續約率 98%、合約年期拉長、大客戶數持續增加，AI 新方案漲價 20–30% 也抵銷了座位壓力。但 GAAP 毛利率下滑，加上 Salesforce 與微軟以捆綁方式進攻，定價權沒有擴大。","growth":"五年後的成長空間仍寬：公司營收只占 2026 年企業應用軟體支出約 3.3%，AI、資安、CRM 三條第二曲線都已有營收規模。但共識 EPS 年增約 22%，比有機營收成長多出約 2 個百分點，這段要靠利潤率擴張來補。","capital":"資本配置中等。回購只夠抵銷股票薪酬帶來的稀釋，2026 年靠舉債完成大型收購，報酬尚未驗證；自由現金流轉換能力強。","valuation":"現價要求未來五年 EPS 年增約 15% 以上，而且倍數不再大幅下降。今年共識 26.5 倍、明年 21.8 倍，PEG 約 1.2。我相信基礎情境的 EPS 複利，但共識還在下修，所以估值判為合理、不便宜。","how_wrong":"最可能看錯的地方：AI 代理把座位制改成用量計價後，營收照樣成長，但毛利與定價權被前端模型商與雲端分走。價值陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 ServiceNow 當成會被 AI 代理吃掉的座位制軟體來定價，公司自身倍數落在四個年度端點的最低點。但本季數字指向相反方向：續約率 98%，RPO 297 億美元、年增 22.5% 且合約年期拉長，一半新增 ACV 已不是座位計價，外部代理經 Action Fabric 呼叫仍按次計費。市場錯在把定價模式轉換當成需求流失。若 Armis 滿一年後 cRPO 固定匯率成長連 2 季低於 17.5%，這個理由就被證偽。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":105.12,"week26_return_pct":15.31,"consensus_rev_3m_pct":-2.46,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"判斷便宜與否用的是 non-GAAP EPS，沒有扣除股票薪酬（占營收約 15%）。股票薪酬是經常性成本，不是一次性項目，所以不改用前瞻錨定，而是用扣除股票薪酬後約 3% 的自由現金流收益率交叉檢查，結論同樣是合理、不便宜。"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"product","event":"AIOps、HRSD、CRM 的 AI 專員預計在第四季全面上市","impact":"中","watch":"上市後是否揭露用量與 Assist 消耗"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"2026 年第四季財報與 2027 年全年財測","impact":"高","watch":"2027 年訂閱營收固定匯率成長是否 ≥18%、營益率擴張是否 ≥100bp、AI ACV 年底是否 ≥17 億美元"},{"date":"2027-07","date_precision":"quarter","type":"other","event":"2027 年第二季財報：Armis 滿一年後第一個不含無機貢獻的 cRPO","impact":"高","watch":"cRPO 固定匯率成長是否 ≥18%"},{"date":null,"date_precision":null,"type":"regulatory","event":"DOJ 政府合約合規調查","impact":"中","watch":"10-Q、8-K 是否揭露起訴、和解或停權通知"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,894B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2><p class="lead">護城河評 B 且持平，執行力強，定價權偏弱。</p><ul class="pts">
<li>護城河來自工作流系統記錄層的轉換成本。設備清單、工作流資料加上 20 多年營運脈絡，讓客戶把 IT、資安、人資流程跑在同一個平台。第三季前 20 大交易中有 19 筆含 6 項以上產品，要換供應商得搬資料、重建流程並重新訓練員工。</li>
<li>方向的正面證據有三條。續約率在第二、三季都是 98%。年 ACV 逾 500 萬美元的客戶由 658 家增到 680 家。AI 原生方案平均漲價 20–30%，CEO 稱活躍使用者沒有下降。這些讓護城河至少沒有變窄。</li>
<li>反向證據同樣具體。TTM GAAP 毛利率 73.08%，低於 2025 年的 77.53%。GAAP 營益率 9.68%，在同業中只高於 DDOG 的 0.43%，CRM 為 21.52%，MSFT 為 47.1%，PLTR 為 42.8%。第三季起為大單附上導入服務，這是讓利，不是漲價。</li>
<li>評分上，執行力給 9 分。第二、三季的營收、cRPO、營益率全數超過財測上緣，做完三筆收購後人數不增反減，營益率仍擴張 50bp。定價權給 7 分，漲價成立，但雲端與推論成本分走一部分。扣掉一項生態攻擊後評為 B，方向持平。</li>
<li>最大威脅是生態攻擊，發生機率約 30%。Salesforce 推出 Agentforce IT 服務管理，直接切入本業，還能和既有 CRM 捆綁。微軟把 Copilot 與代理平台捆進企業授權。公司稱競爭名單裡看不到這些對手，但沒有給贏率，第三季前 20 大交易中 IT 服務管理仍占 11 筆。</li>
<li>點對點替代列為觀察項。AI 原生點解決方案和企業用 AI 寫程式工具自建流程，都在 10-K 自述的競爭範圍內。前份把代理繞過列為最高級威脅，本次降級，理由是外部代理經 Action Fabric 呼叫時，工作仍在公司平台內執行並計費。</li>
<li>降級的證據都來自管理層，所以設了升級條件。非 GAAP 訂閱毛利率連 2 季低於 78%，或 Action Fabric 用量停止揭露，就升回架構替代並重評論點。第三季該毛利率為 80%，全年財測 81%，目前仍有緩衝。</li>
<li>定價模式轉換是第三項威脅，機率約 40%。彭博行業研究估計應用軟體利潤率可能壓縮 100 至 900bp。CFO 稱客戶沒有要求成果計價，但一半新增 ACV 已不是座位計價。這項已反映在定價權評分，不另扣分。</li>
<li>報酬持續期無法精算。投入資本事實表未涵蓋，增量 ROIC 算不出來，只能推定為高利益率搭配高周轉，預收款讓營運資金為負。四個檢查點兩綠兩黃，黃燈在決策層級與價值鏈分配。AI 導入代理讓搬遷縮短到 30 至 60 天，對手也能拿來搬走公司客戶。</li>
</ul><!-- E5 --><!-- E6 --><!-- E7 --></section>

```