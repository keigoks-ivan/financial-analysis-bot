你是 stock-analyst v20 的**散文層（prose）agent**，標的 CMI（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：CMI　日期：2026-11-08　archetype：None　前份裁決：2026-05-18　衛星候選 / 觀望 — Power Systems data center super-cycle + EPA 2027 prebuy thesis 真實但估值已透支；建議等 Fwd PE 分位回 60% 區（~$580-620 區）或 NA Class 8 prebuy 真實流入 FY27 EPS 共識上修後再進場｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2325B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（436B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1128B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（971B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1110B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（828B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1144B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2170B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3363B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3197B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2325           3272-4675      3 條（2–6 內）  
s3                  8000         436           5295-7564      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3209          8254-11791      5 條（2–6 內）  
s6                 11000         828          7120-10172      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1144           1649-2356      3 條（2–6 內）  
s10                 5000        2170           1981-2830      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3197           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4734B；至少需散文≈40.27KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−50
−41%
−35.4%
−33.31
−30%
−30
−27%
−16%
−15%
−7.1%
−5%
−0.7%
−0.24%
0.07
0.5
0.54
0.68
0.75
0.77
0.84
0.88
1%
1
01
1.03
1.3
1.32
1.371
1.387
1.423
1.72
1.75
1.79
1.81
1.82
1.82%
1.99
2
02
2%
2.25
2.4
2.5
2.6
2.9
3%
3
3.03
3.1
3.59
3.9%
4
4%
04
4.1
5
5%
05
6
6%
6.6%
6.9%
7
7%
07
7.71
8
8%
08
8.2%
8.25
8.28
8.3%
9%
9
9.1%
9.1
9.2%
9.4
9.5%
9.66%
9.9
10%
10
10.2%
10.37%
10.75%
11%
11
11.02
11.4
11.6
11.79%
12
12%
12.25
12.5
12.75%
12.85
12.9
12.93
13%
13
13.2
13.2%
13.25
13.5
13.5%
13.75%
13.9%
14
14.05
14.3%
14.5
15%
15
15.2
15.21
15.3%
15.5%
16
16%
16.5%
16.81
17
17.3%
17.4%
17.5
18%
18
18.2%
18.33%
18.4
18.5%
18.88%
18.9%
19
19%
20
20%
20.5
21
21%
21.06
22%
22
22.4
22.5%
23
23%
23.81
24
24%
24.5%
25%
25
25.1
25.4%
25.6%
25.7%
26%
26
26.1%
26.4%
26.5
27.7%
28%
28.5
29
29.5%
29.59
30
30%
31
32
33
33%
33.34
33.5
34.7
34.81
35%
35.4%
36
36.5
38
39.46
40
40%
40.69
41
42
43
43.8%
45
47%
47.6
48
49
50%
50
50.9
54.18
55%
55
56
60%
60
62
65
67
70
72%
75.24
90
94.38
94.4
95%
98.7
100%
100
104
130
150%
220
225
250
264
313.5
327.19
400
411
413
450
450.07
465
500
502
551
$580
580
620
667
696.53
745
757
894
2008
2019
2022
2024
2025
2026
2027
2028
2029
2030
20261108
1,085
15,000
25,000
320,000
39,052
5,600
7,500
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
{"meta":{"ticker":"CMI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Cummins Inc."},"oneliner":"康明斯跌到 450 美元，只有今年 EPS 的 15.2 倍，資料中心發電訂單排到 2028 下半年，生意沒壞；但現價仍要 2030 目標大致達成才有約一成年報酬，2027 年獲利基礎要等 2 月財測，先不接。","thesis":{"H":[{"id":"H1","text":"資料中心備援電力需求撐住 Power Systems 與 Distribution，資料中心營收由約 50 億美元成長到 2030 年 90 億美元以上，Power Systems EBITDA 率守在 25% 以上。","2y":"FY2027 Power Systems 營收年增≥10%，EBITDA 率≥25%；大型機組訂單排程維持到 2028 下半年之後。","5y":"2030 年資料中心營收≥90 億美元，高馬力產能 55GW 投產後 Power Systems EBITDA 率仍≥25%。","10y":null,"threshold":"2026 年發電營收 +15–25%，Power Systems 營收 +15–18%、EBITDA 率 25.1–25.6%；2030 年資料中心營收 90 億美元以上。","source":"康明斯 8-K 分部表、2026-11-05 法說、2026-05-21 投資人日。","drift_rule":"連 2 季 Power Systems 年增<+10% 或 EBITDA 率<25% 削弱；連 4 季年增<+5% 反轉。"},{"id":"H2","text":"北美卡車由週期低點回升，EPA 2027 分階段切換沒有造成斷層，NCP 轉嫁給客戶，Engine 段利潤率守住。","2y":"2027 年北美重卡產量與 2026 年大致持平（24–25 萬輛）；Engine 段 EBITDA 率≥12%；NCP 全額轉嫁。","5y":"2028 後段新平台脫離約 18 個月的保固提列期後，Engine 段 EBITDA 率高於 FY2026 指引上緣 12.75%；X10 帶動重卡份額上升。","10y":null,"threshold":"FY2026 Engine 段 EBITDA 率指引 12.25–12.75%；北美重卡 24–25 萬輛；中型 12.5–13 萬輛。","source":"康明斯 8-K、季度法說、EPA 定案公告、ACT Research 月度訂單。","drift_rule":"2027 H1 月訂單<15,000 輛削弱；連 2 季新平台上量出問題反轉。"},{"id":"H3","text":"全公司 EBITDA 率由 FY2026 約 18.2% 升到 2030 年 20% 以上，增量利潤率 25% 以上，反映發電組合與營運紀律，不是景氣高點的暫時現象。","2y":"FY2027 EBITDA 率≥18.5%，FY2028≥19%。","5y":"FY2030 EBITDA 率≥20%，營收 450–500 億美元。","10y":null,"threshold":"2030 年 EBITDA 率>20%、營收 450–500 億美元、增量利潤率 25% 以上。","source":"2026-05-21 投資人日、每季 8-K。","drift_rule":"連 2 季全公司 EBITDA 率<16.5% 或 Power Systems<24% 削弱；連 4 季全公司<15% 或 Power Systems<22% 反轉。"}],"R":[{"id":"R1","text":"Q3 延後的出貨在 Q4 補不回來，全年指引再下修。Q4 指引隱含營收年增 15%、Distribution 季增約 23%。","h_ref":"H1","clock":"⚡","threshold":"Q4 Distribution<38 億美元或全年成長<9.5%，供應鏈的一次性歸因就不成立。","evidence_refs":["end_markets#1","capital_markets_pricing#0"]},{"id":"R2","text":"資料中心資本支出暫停，或同業擴產壓縮訂單與定價。","h_ref":"H1","clock":"🔥","threshold":"連 2 季 Power Systems 年增<+10% 或 EBITDA 率<25% 削弱；連 4 季年增<+5% 反轉。","evidence_refs":["supply_demand_durability#3","substitute_technology#2"]},{"id":"R3","text":"電動卡車與其他替代技術壓縮內燃機市場，中國已見影響。","h_ref":"H2","clock":"🐢","threshold":"北美 Class 8 電動滲透率>10%（3–5 年內，事實表未涵蓋現值，資料缺口），且判斷機率≥50% 才砍倉。","evidence_refs":["competitive_share_entrants#1"]},{"id":"R4","text":"PACCAR 提高自製引擎比重，或其他客戶改採自製、他廠。","h_ref":"H2","clock":"🐢","threshold":"PACCAR 占合併銷售<11% 且北美重卡產量年增。","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0"]},{"id":"R5","text":"EPA 2027 切換造成需求斷層，或預購後回吐。公司 5 月曾說明年第一季會有量的停頓。","h_ref":"H2","clock":"🔥","threshold":"2026 H2 月訂單<25,000 輛警示（事實表只到 2026 年 5 月，資料缺口）；2027 H1 月訂單<15,000 輛削弱；Engine 段 EBITDA 率連 2 季<8% 減碼。","evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"id":"R6","text":"新平台上市與召回推高保固。L9 燃油管召回約 39,052 件，PD7000 軟體召回約 411–413 台，金額未揭露。","h_ref":"H3","clock":"🔥","threshold":"保固費用占營收連 2 季>3%（目前約低 2%）。","evidence_refs":["major_events#1","major_events#2","product_recall_warning#0","product_recall_warning#1"]},{"id":"R7","text":"關稅、貨運與單一來源零件推高成本。CFO 說下半年價格減成本略為負值。","h_ref":"H3","clock":"🔥","threshold":"毛利率連 2 季年減，視為吸收失敗。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R8","text":"排放案的後續監管與證券集體訴訟 Baker v. Cummins，現況未核實，受影響金額與和解日期事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"單筆新增應計≥2.5 億美元，或集體認證且和解不利則減碼一半；刑事介入則清倉。","evidence_refs":["regulatory_antitrust#0","major_events#3","lawsuit_class_action#0"]},{"id":"R9","text":"Hydrogenics 電解槽停用建議的財務影響尚在評估，未計入指引。","h_ref":"H3","clock":"⚡","threshold":"單次費用>1 億美元或轉為召回。"}],"single_thing":{"description":"超大規模客戶對大型發電機組出現實質訂單取消或遞延，公司揭露排程由 2028 下半年往前縮短，或多年協議被改約。","why_fatal":"這是五年路徑裡最大的單一變數。資料中心營收增量 40 億美元，用 Power Systems 25.4% 的 EBITDA 率、23% 稅率、1.3 億股粗算，每股約 6 美元，占 Base 五年 EPS 增量 18.4 美元的三分之一；Distribution 的安裝利潤還沒算，本益比也會同步由 14 倍往 11 倍掉。卡車下行幅度也大，但屬已知週期，已在 Bear 路徑內。","if_happens":"持有就清倉，未持有就取消重啟條件；Base 下移到 Bear 路徑，重跑研究。","how_monitor":"每季法說的大型機組訂單排程月份與多年協議揭露，再對照主要雲端業者的資本支出指引（事實表未涵蓋數字）。","probability":"12–24 個月內約 20%。訂單排到 2028 下半年且部分合約更長，短期取消機率低；但美國資料中心的能源與環保爭議已被法說問及，積壓又集中在少數客戶。"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.93,"peg_fy2":0.77,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":20.5,"FY2026E":29.59,"FY2027E":34.81,"FY2028E":40.69},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；FY2025A 含 Accelera 相關費用，共識來自 2026-11-07 Koyfin 快照，尚未反映 Q3 財測收斂，EPS 家數事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"不是商品價格接受者，是需求量循環：卡車段由低點回升，發電段訂單滿載但新增產能 2028 年才大量到位。"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高。訂單排到 2028 下半年是真的，但緊俏來自產能不足，康明斯自己要把高馬力產能加到 55GW，Caterpillar、Generac 也在擴，2028 年供給大增後定價能否守住沒有證據。時鐘落在擴張期的依據是營收年增由 Q1 3%、Q2 9% 升到 Q3 13%，Q4 指引隱含 15%。","bargaining":{"up":"供應鏈偏緊，Q3 一家供應商出問題就延後約 2 億美元營收，多項關鍵零件單一來源。","down":"大型機組供應商少，對資料中心客戶有定價空間；對 PACCAR 等大型 OEM 議價較弱，供應協議不保證數量。","geo":"中國含合資 Q3 營收 19 億美元，出口管制可能影響收款與現金調回；資料中心訂單國際已與美國持平。"},"profit_pool_dir":"利潤池往 Power Systems 與 Distribution 移動，2025 年合計占 EBITDA 60%；五年前占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率。資料中心只有公司自述由約 50 億美元到 2030 年 90 億美元以上，算不出利潤池五年變化，這是已知缺口。"}},"moat":{"mechanism":"全球引擎規模、售後服務網路，加上發電機組到安裝的一體化供應。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"發電端定價與利潤率擴大；卡車端最大客戶占比由 16% 降到 13%，中國銷量跌幅比產業多 10 個百分點。資料中心份額增減沒有一手數據。","peer_na_reason":"同業 ROIC 事實表未涵蓋，改用 TTM 營業利益率比較。","threats":[{"level":"🟡","text":"Caterpillar 發電銷售成長 72%，Generac 資料中心積壓約 16 億美元，同業擴得比康明斯快。Power Systems Q3 只增 15%，部分受自身產能與供應限制。","p":"35%","evidence_refs":["substitute_technology#2","supply_demand_durability#3"]},{"level":"🔴","text":"PACCAR 擴自製引擎，10-K 也寫明客戶可能自行開發或改向他廠採購；占營收由 16% 降到 13%，週期與自製各占多少事實表無法拆。","p":"40%","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0"]},{"level":"🟡","text":"電動與其他替代技術。中國電動卡車已影響銷量，但只限當地公路車；北美重卡滲透率事實表未涵蓋，資料中心本十年仍以柴油備援為主。","p":"30%","evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"資料缺口：事實表未涵蓋投入資本，無法算周轉率與象限；稅後營益率約 9.1%（TTM 營益率 11.79%×（1−23%））。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是資料中心營運者與車隊，決策者與付款者是超大規模客戶、OEM 與車隊，三環都成立。備援電力延後的代價是停機風險，屬需要不是想要，目前 95% 是備援用途。需求量的波動放在風險段處理。"},{"item":"決策層級","level":"🟡","text":"大型機組供應商少，超大規模客戶簽多年協議，替代性低。卡車端逐台選配，PACCAR 可改用自製引擎，替代性存在。漲價流失率與續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"Power Systems EBITDA 率 25.4%，錢目前留在這一節。但買方高度集中，供應鏈限制出貨，CFO 說成本在爬；2028 年全產業擴產後分配可能反轉。"},{"item":"社會容忍度","level":"🟡","text":"分析師已在法說問美國資料中心的能源與環保爭議，CEO 承認有討論。排放端有前科，2024 年付 19 億美元和解；EPA 2027 的 NCP 金額預計 12 月定案。限制備援機組的法案證據事實表未涵蓋。"}],"roiic":"約 47%（代理值，非實測）","reinvest_rate":"約 28%（代理值，非實測）","endo_ceiling":13.2,"formula_note":"投入資本與折舊不在事實表，改用代理：FY2023–25 累計淨利 75.24 億美元減累計 FCF 54.18 億美元，得 21.06 億當淨再投資，占淨利 28%；FY2022→FY2025 營業利益增 12.85 億，稅後（23%）9.9 億，除以 21.06 億得 47%；47%×28%＝13.2%。此數可能高估，因為 2022 年 Meritor 併購款不在分母，金額事實表未列；FY2024 淨利 39.46 億明顯高於前後年，一次性項目也未拆。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","CMI":25.88,"CAT":32.92,"PCAR":16.85,"ALSN":33.95,"GNRC":39.92,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","CMI":11.79,"CAT":18.33,"PCAR":10.75,"ALSN":18.88,"GNRC":10.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","CMI":9.66,"CAT":12.36,"PCAR":7.44,"ALSN":15.85,"GNRC":8.97,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","CMI":4.17,"CAT":2.97,"PCAR":1.51,"ALSN":4.06,"GNRC":5.48,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"CAT","gm":32.92,"om":18.33,"fcf_margin":12.36,"rd_intensity":2.97,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"PCAR","gm":16.85,"om":10.75,"fcf_margin":7.44,"rd_intensity":1.51,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"ALSN","gm":33.95,"om":18.88,"fcf_margin":15.85,"rd_intensity":4.06,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"GNRC","gm":39.92,"om":10.37,"fcf_margin":8.97,"rd_intensity":5.48,"period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主，發電有漲價，淨回購每年約 1 個百分點，併購為零；利潤率擴張對 EPS 的貢獻大於營收。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"沿用護城河段的代理值 13.2%（淨再投資率 28%×增量報酬 47%）；投入資本與折舊事實表未涵蓋。","segments":[{"item":"Power Systems","value":"Q3 營收 23 億美元、+15%、EBITDA 率 25.4%；FY2026 指引 +15–18%、25.1–25.6%。新產能 2027 年開始增加，2028 年增幅較大。"},{"item":"Distribution","value":"Q3 營收 33 億美元、+4%、EBITDA 率 13.9%；FY2026 指引 +10–13%，Q4 指引中點隱含季增 23%。"},{"item":"Engine","value":"Q3 營收 31 億美元、+20%、EBITDA 率 13.5%；FY2026 指引下修到 +8–11%、12.25–12.75%。"},{"item":"Components","value":"Q3 營收 29 億美元、+23%、EBITDA 率 14.3%；FY2026 指引 +8–11%、13.25–13.75%。"},{"item":"Accelera","value":"Q3 營收 1.03 億美元；FY2026 EBITDA 虧損指引 2.6–2.9 億美元，Hydrogenics 停用建議的影響未計入。"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q2 26.1% 對 26.4% 年減，Q3 27.7% 對 25.6% 年增。"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"中國卡車銷量 −15%，產業 −5%；PACCAR 占比下降。北美與資料中心份額無一手數據。"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"皮卡 −16%，公司歸因於柴油價格與利率，不是提價。"},{"signal":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"evidence":"共識 EPS 年增 25.7%，營收兩年年增約 10%，部分是低基期。"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"FY2024 0.07（含 19 億美元和解款），FY2025 0.84。"},{"signal":"SBC／營收大於 5% 且上升","lit":null,"evidence":"事實表未涵蓋。"},{"signal":"TAM 萎縮或被替代","lit":false,"evidence":"中國公路車有替代，集團層面尚未看到；TAM 數字事實表未涵蓋。"},{"signal":"產業倍數近 3 年系統性下移","lit":null,"evidence":"事實表未涵蓋產業倍數序列。"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"evidence":"總資本支出指引 13.5–14.5 億美元，TTM FCF 約 34.7 億美元；維持性比例未揭露。"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"仍在加 20GW 產能，FY2026 營收約 +10%。"}],"trap_rating":"價值陷阱風險中等（亮 2 個），長期成長性中等。"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購：近 12 個月無併購類重大申報，CEO 在投資人日說管線沒有大型項目；回饋節奏已寫在本題判斷中。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Meritor（2022）的已實現報酬事實表未涵蓋。可驗證的是零排放：2025 Q3 Accelera 減損與存貨費用 2.4 億美元，2026 Q1 淨付 1.75 億美元賣掉低壓燃料電池，FY2026 仍預期 EBITDA 虧損 2.6–2.9 億美元，Hydrogenics 電解槽又發出停用建議。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"Q2 回購 2.25 億、Q3 3.59 億美元；回購均價與 10 年期殖利率事實表未涵蓋，無法判定。現價盈餘殖利率 6.6%（29.59÷450.07）只供參考。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 金額事實表未涵蓋。改看股數：稀釋股數由 FY2022 約 1.423 億（淨利÷EPS）降到 FY2025 約 1.387 億，目前流通 1.371 億，淨稀釋為負。","grade":"過"}]},"valuation":{"basis":"Forward P/E（FY2026E 共識 EPS），循環股輔以銷售倍數對照。","tier":"工業動力設備","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比；終端倍數因此沒有同業現值對照，只用康明斯自身 15.21 倍為錨，這是已知缺口。"},"fwd_pe":15.21,"peg":0.88,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"本益比面偏便宜：今年 15.21 倍、明年 12.93 倍，PEG 0.88（15.21÷FY2026E 到 FY2028E 年增 17.3%）。銷售面不便宜：P/S 1.72 倍在 4 個年度端點的 65 百分位，EV/S 1.81 倍在 60 百分位。五年分位算不出來，事實表只有 4 個年度端點。Base 年報酬約 10%，屬中段。分母有爭議，便宜的論證不算數，所以評中性。短期上檔＝FY2027 Base EPS 33.5 美元×15 倍＝502 美元；中期＝FY2028 Base EPS 38 美元×14.5 倍＝551 美元。","upside_short_pct":11.6,"upside_mid_pct":22.4},"trap_analysis":{"verdict":"🟡","label":"價值陷阱風險中等：便宜建立在高點利潤率上，衰退信號亮 2 個。"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2008 年第四季 EBIT 率由 9.2% 跌到 3.9%，2019 年 Class 8 產量九個月跌 55%；Caterpillar、Generac 同步擴資料中心產能，康明斯 20GW 新產能 2028 年才大量到位。","assumption":"資料中心需求與卡車週期不會同時轉弱，2028 年新增產能仍被消化。","consequence":"五年後虧 50% 最可能的故事：2028 年供給大增時超大規模客戶放緩，卡車同時下行，FY2029 EPS 跌到 24 美元，本益比 9–10 倍，股價約 225 美元。","ruling":"採納，已放進 Bear 機率 30% 與最大跌幅下緣 −50%。這條和唯一致命事件部分重疊，差別在這裡是供需慢慢反轉，唯一致命事件是訂單被取消。","watch":"每季大型機組訂單排程月份、Power Systems 營收年增與 EBITDA 率、ACT 月度卡車訂單。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#2","supply_demand_durability#3"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 Distribution EBITDA 率由 15.5% 降到 13.9%，CEO 說發電專案利潤率低於售後零件；CFO 說下半年價格減成本略為負值；Q4 Power Systems 隱含約 22.5%；客戶改訂小排量機組，儲能案也在增加。","assumption":"資料中心營收到 2030 年 90 億美元時，增量利潤率維持 25% 以上。","consequence":"營收達標但組合變差，EBITDA 率停在 18–19%，FY2031 EPS 約 40 美元，以 14 倍計年報酬由約 10% 降到約 6%。","ruling":"部分採納。Base 已低於共識，但沒有扣到這麼低，因為 Q3 毛利率創新高，組合惡化還沒出現在全公司數字上。","watch":"Distribution EBITDA 率、Power Systems 增量利潤率，每季看。","evidence_refs":["reg_tariff_export#2"]},{"view":"價格已反映太多","evidence":"跌 33% 後仍要 FY2031 EPS 47.6 美元才有 10% 年報酬，接近 2030 目標換算 41–48 美元的上緣；P/S 仍在 4 個年度端點的 65 百分位。","assumption":"跌這麼多就算便宜。","consequence":"FY2031 EPS 只有 43 美元時，年報酬約 8%，不足以補償循環股的回撤。","ruling":"採納。已跌不是安全邊際，要有 2027 年獲利基礎的確認才算。","watch":"2 月財測後的共識 FY2027 EPS。","evidence_refs":["capital_markets_pricing#0"]}],"max_dd":{"lo":-50,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 696.53 → 本次 450.07（-35.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=696.53","side_b":"本次 price_at_dd=450.07","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 696.53 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 696.53 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 696.53 美元：Bull 價 1,085、Bear 價 313.5，五年期望值 −7.1%，基準年化 −0.7%，不對稱比 0.68","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.68。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 696.53 美元：五年期望值 −7.1%，基準年化 −0.7%，不對稱比 0.68","side_b":"本次情境、股價 450.07 美元：五年期望值 +43.8%，基準年化 8.3%，不對稱比 3.1","ruling":"再換股價、情境不動：起點價下跌 35.4%，五年期望值多 50.9 個百分點，基準年化多 9.1 個百分點，不對稱比由 0.68 升到 3.1。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論變動","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 696.53 美元時評為最貴一級，要等 580–620 美元。","side_b":"本次 450.07 美元、今年 EPS 的 15.2 倍，評為中性。","ruling":"改變的主因是股價跌 35%，FY2026E 共識三個月只修 −0.24%。不升到最便宜一級，因為銷售倍數仍在年度端點的 60–65 百分位，便宜只在本益比上成立，而分母正是爭點。","evidence_level":"事實表數字","settle_metric":"2 月財測後的共識 FY2027 EPS","if_then":["若共識 FY2027 EPS 維持 33 美元以上且財測達標，重跑研究後建首筆，不超過 2%","若共識 FY2027 EPS 低於 33 美元，不建倉"]},{"axis":"前份空白欄位首次填入","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位都是空值：配置結論與角色、護城河方向、成長跑道、公司類型、循環位置、情境機率、最大跌幅。","side_b":"本次首次填入：護城河持平、成長跑道中等、循環股兼品質成長、循環中段、牛 20／基 50／熊 30、最大跌幅 −30%～−50%；配置結論與角色由程式算。","ruling":"這些是新填，不是看法反轉。循環位置判中段：訂單與情緒偏買，存貨與倍數中性，資料中心資本支出偏晚；P/B 事實表未涵蓋，訊號又互相矛盾，反動能檢查沒有全過。","evidence_level":"格式變動","settle_metric":"無","if_then":["若卡車與發電訊號在 2 月後一致偏買，循環位置改判早循環並重跑研究","若 Power Systems 接單放緩，循環位置改判晚循環，不建倉"]},{"axis":"綜合評等與價值陷阱理由更換","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份綜合評等 B、價值陷阱中等，依據是題材真實但估值透支。","side_b":"本次同為 B、價值陷阱中等，依據換成估值已回落，但 Q3 實質低於預期、獲利基礎未確認。","ruling":"評等沒變，理由換了。估值壓力減輕，換成分母風險，兩者互抵。","evidence_level":"公司申報與法說","settle_metric":"FY2027 財測","if_then":["若 2 月財測三項全中，重跑研究後建首筆，不超過 2%","若有一項未達，不建倉，重啟條件順延一季"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"進場重啟條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 Fwd PE 分位回 60% 區（~$580-620 區）或 NA Class 8 prebuy 真實流入 FY27 EPS 共識上修後再進場","side_b":"2027 年 2 月財測：FY2027 營收成長中點≥7%、EBITDA 率中點≥18.5%，且財測後共識 FY2027 EPS≥33 美元，三項全中才重跑研究","ruling":"舊的價格條件已被跌破，卻沒有對應的基本面確認；管理層 11 月 5 日也說預購有限，舊的事件條件失去依據。進場改看獲利基礎，這是目前唯一的卡點。","evidence_level":"公司法說","settle_metric":"2 月財測三項","if_then":["三項全中，重跑研究後進場，首筆不超過 2%","有一項未達，不進場"]},{"axis":"Single Thing 由空白改為資料中心訂單取消","cause":"方法變動","prior_field":null,"side_a":"前份唯一致命點為空值，未設定。","side_b":"超大規模客戶對大型發電機組出現實質訂單取消或遞延，公司揭露排程由 2028 下半年往前縮短，或多年協議被改約。","ruling":"五年路徑裡敏感度最大的單項是資料中心增量，所以定在這裡，不是定在較戲劇性的法規或訴訟事件。","evidence_level":"估算，輸入來自公司目標","settle_metric":"每季訂單排程月份","if_then":["若事件發生，持有就清倉，未持有就取消重啟條件","若排程延伸到 2029 年以後，Bull 機率上調 5 個百分點並重跑研究"]},{"axis":"減碼與清倉門檻整理","cause":"方法變動","prior_field":null,"side_a":"前份未設砍倉指標；門檻散在風險列：Engine 段 EBITDA margin 連 2 季 < 8% 觸發減倉；連 4 季 Power Systems YoY < +5% → thesis 反轉，估值倍數 reset 至 17-18x。","side_b":"Engine 段 EBITDA 率連 2 季<8% 減碼；Power Systems 年增連 4 季<+5% 或 EBITDA 率連 4 季<22% 清倉；大型機組排程縮短到 2027 年內清倉；保固費用率連 2 季>3% 減碼。","ruling":"原門檻全部保留。只退休 17–18 倍的倍數重設，因為現價已是 15.2 倍。新增項目針對這次才浮現的訂單與新平台保固風險。","evidence_level":"前份紀錄與公司法說","settle_metric":"分部 EBITDA 率與年增率","if_then":["若 Engine 段連 2 季低於 8%，減碼一半","若 Power Systems 連 4 季年增低於 5%，清倉"]},{"axis":"前份卡車與發電門檻修訂","cause":"新證據","prior_field":null,"side_a":"2026 NA Class 8 production ≥ 320,000 units；Power Systems FY26-FY27 EBITDA margin 平均 ≥ 26%。","side_b":"公司預測 2026 年北美重卡 24–25 萬輛、中型 12.5–13 萬輛；FY2026 Power Systems EBITDA 率指引 25.1–25.6%。","ruling":"32 萬輛單看重卡沒達到，含中型是 36.5–38 萬輛，舊口徑本來就不清楚，退休，改成 2027 年重卡產量持平。26% 在全年指引下也達不到，改成 25% 以上，並保留連 2 季低於 25% 就削弱的規則。","evidence_level":"公司法說","settle_metric":"FY2027 重卡產量、Power Systems EBITDA 率","if_then":["若 2027 年重卡產量低於 22 萬輛，Base 的 FY2027 EPS 下調到 32 美元，不建倉","若連 2 季 Power Systems EBITDA 率低於 25%，停止加碼"]},{"axis":"管理層對預購的說法改變","cause":"新證據","prior_field":null,"side_a":"2026-08-04 Rumsey：some prebuy is coming in，中型車財測納入略高的預購；2026-05-21 Engine 總裁：明年第一季會有量的停頓。","side_b":"2026-11-05 Rumsey：pretty limited prebuy，需求是週期低點的真實回升；中型車預測下修到 12.5–13 萬輛，客戶在等 NCP。","ruling":"數字上接受預購有限，中型車下修、客戶在等，確實不像大規模預購。需求回升還沒證實，5 月講過的第一季停頓 11 月也沒有撤回。可調和，是時間差與程度差。","evidence_level":"法說逐字稿","settle_metric":"2027 Q1 北美重卡產量與 Engine 段 EBITDA 率","if_then":["若 2027 Q1 北美重卡產量季減超過 15%，不建倉","若產量持平且 Engine 段 EBITDA 率≥12%，H2 視為成立，可按重啟條件進場"]},{"axis":"Power Systems 利潤率走勢","cause":"新證據","prior_field":null,"side_a":"CFO（2026-11-05）：Q4 約 22.5% 不是往後的水準，軌跡沒有根本改變。","side_b":"前份記 Q1 29.5%，之後 Q2 24.5%、Q3 25.4%、Q4 隱含約 22.5%；小機組需求、儲能案與新產能投入都可能拉低組合。","ruling":"管理層的歸因不採信也不否定，標為未證。預先登記：2027 Q1、Q2 連續低於 24%，就算歸因不成立。","evidence_level":"法說逐字稿，部分為隱含計算","settle_metric":"2027 Q1、Q2 Power Systems EBITDA 率","if_then":["若連續兩季低於 24%，停止加碼並下調 Base 的 2030 年 EBITDA 率假設","若兩季都在 25% 以上，H1 維持"]},{"axis":"Q3 表面達標與實質品質","cause":"新證據","prior_field":null,"side_a":"Q3 EPS 8.25 美元，接近共識 8.28 美元。","side_b":"8.25 美元含每股 0.54 美元離散稅項利多，扣掉是 7.71 美元，低於共識 6.9%；營收 94.4 億美元也低於約 98.7 億美元預期。","ruling":"採後者。Q3 實質上營收和獲利都低於預期，只有利潤率好。共識數字來自聚合摘要，未逐字核對，但方向不受影響。11-07 快照沒反映，FY2027 的 34.81 美元還沒被重新檢驗。","evidence_level":"法說逐字稿＋聚合摘要","settle_metric":"2 月財測後的共識 FY2027 EPS","if_then":["若共識下修到 33 美元以下，不建倉並下調 Base","若共識維持 33 美元以上且財測達標，重跑研究後建首筆"],"evidence_refs":["capital_markets_pricing#0","end_markets#1"]},{"axis":"股價與共識背離、現在就買的最強論證","cause":"價格變動","prior_field":null,"side_a":"現在就買的最強論證：Q3 利潤率創高，接單超預期，排程到 2028 下半年，超大規模客戶有超過訂單期的合約承諾；資料中心訂單國際已與美國持平，可緩衝美國政治風險；股價半年跌 33%，只有今年 EPS 15.2 倍、明年 12.9 倍。","side_b":"不買的理由：跌幅原因事實表未涵蓋；共識還沒反映 Q3；現價要 FY2031 EPS 47.6 美元才有一成年報酬；2027 指引 2 月才出，EPA 規則 12 月才定。","ruling":"先不買。股價先跌、共識後跟是時間差，可調和。等三個月的代價是可能買貴，買錯的代價是在 −30% 到 −50% 的路徑上持有；兩者比較，等待划算。若市場對、共識錯，FY2027 共識會在 2 月下修。","evidence_level":"事實表、法說","settle_metric":"2 月財測三項","if_then":["股價回到 104 週均線 465 美元以上而 2 月財測未出：不追","股價跌到 400 美元以下、12 月 EPA 定案 NCP 可轉嫁、沒有訂單取消：分批反買，首筆不超過 1%","反向條件：2 月財測有一項未達，不建倉，重啟條件順延一季"]},{"axis":"產業態勢","cause":"新證據","prior_field":null,"side_a":"競爭惡化：Caterpillar 發電銷售 +72%，Generac 資料中心積壓約 16 億美元，PACCAR 擴自製引擎。","side_b":"結構轉好：訂單排到 2028 下半年，大型引擎供應商少，EPA 2027 讓每台卡車成本增加約 1 萬美元，多在動力系統。","ruling":"雙向拉鋸。第三軸是法規與替代技術：EPA 2027 即將定案，中國電動卡車正在替代柴油。兩邊都有出處，份額方向沒有一手數據，不能裁成單邊。","evidence_level":"公司申報、媒體與搜尋摘要","settle_metric":"資料中心份額、PACCAR 占比","if_then":["若 PACCAR 占比低於 11% 且北美重卡產量年增，停止加碼","若 X10 帶動重卡份額上升有數據，定價力加回 1 分"],"evidence_refs":["substitute_technology#2","supply_demand_durability#3","customer_second_source#0"]}],"triggers":[{"n":1,"text":"2 月財測確認 2027 年獲利基礎","type":"估值rearm","maps_to":"H3","metric":"FY2027 營收成長與 EBITDA 率指引中點，財測後共識 FY2027 EPS","threshold":"營收成長≥7%、EBITDA 率≥18.5%、共識 EPS≥33 美元，三項全中","action":"重跑研究，通過才建首筆，不超過 2%","source_freq":"Q4 財報與法說，一年一次","date":"2027-02"},{"n":2,"text":"資料中心大型機組訂單被取消或遞延","type":"Single Thing","maps_to":"H1","metric":"大型機組訂單排程與多年協議","threshold":"排程縮短到 2027 年內，或揭露協議取消、遞延","action":"清倉","source_freq":"每季法說","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"Power Systems 成長或利潤率轉弱","type":"假設驗證","maps_to":"H1","metric":"Power Systems 營收年增與 EBITDA 率","threshold":"連 2 季年增<+10% 或 EBITDA 率<25%","action":"停止加碼","source_freq":"每季 8-K 分部表","date":"2027-02"},{"n":4,"text":"Q4 補出貨沒有兌現，供應鏈的一次性歸因就不成立","type":"風險","maps_to":"R1","metric":"Q4 Distribution 營收、全年營收成長","threshold":"Distribution<38 億美元或全年成長<9.5%","action":"不追","source_freq":"Q4 財報","date":"2027-02","evidence_refs":["end_markets#1","capital_markets_pricing#0"]},{"n":5,"text":"EPA 定案不利","type":"風險","maps_to":"R5","metric":"NCP 金額與過渡安排","threshold":"NCP 無法全額轉嫁，或定案延到 2027 年","action":"不追","source_freq":"EPA 公告","date":"2026-12"},{"n":6,"text":"Engine 段利潤率跌破底線","type":"減碼","maps_to":"R5","metric":"Engine 段 EBITDA 率","threshold":"連 2 季<8%","action":"減碼","source_freq":"每季 8-K 分部表","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"n":7,"text":"發電論點反轉","type":"清倉","maps_to":"H1","metric":"Power Systems 營收年增與 EBITDA 率","threshold":"連 4 季年增<+5% 或 EBITDA 率<22%","action":"清倉","source_freq":"每季 8-K 分部表","date":null},{"n":8,"text":"新平台保固失控","type":"風險","maps_to":"R6","metric":"保固費用占營收","threshold":"連 2 季>3%（目前約低 2%）","action":"減碼","source_freq":"每季 10-Q","date":null,"evidence_refs":["product_recall_warning#0","product_recall_warning#1","major_events#1","major_events#2"]},{"n":9,"text":"Hydrogenics 電解槽費用超出預期","type":"風險","maps_to":"R9","metric":"停用建議的財務影響","threshold":"單次費用>1 億美元或轉為召回","action":"不追","source_freq":"每季 10-Q","date":"2027-02"},{"n":10,"text":"成本與關稅吸收失敗","type":"風險","maps_to":"R7","metric":"毛利率年增減，CFO 對價格減成本的說法","threshold":"毛利率連 2 季年減","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1"]},{"n":11,"text":"排放訴訟出現新費用或程序升級","type":"風險","maps_to":"R8","metric":"新增應計、集體認證、刑事程序","threshold":"單筆應計≥2.5 億美元或集體認證且和解不利減碼一半；刑事介入則清倉","action":"減碼","source_freq":"10-Q 訴訟附註","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#3","lawsuit_class_action#0"]},{"n":12,"text":"PACCAR 占比續降","type":"風險","maps_to":"R4","metric":"PACCAR 占合併銷售比","threshold":"<11% 且北美重卡產量年增","action":"停止加碼","source_freq":"10-K，一年一次","date":"2027-02","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0"]},{"n":13,"text":"股價先跌、基本面未損時的試單","type":"加碼","maps_to":"H1","metric":"股價、EPA 定案、訂單排程","threshold":"股價≤400 美元，NCP 可轉嫁，無訂單取消","action":"分批反買，首筆不超過 1%，2 月財測前不再加","source_freq":"每日股價、事件","date":null},{"n":14,"text":"2 月財測後複審","type":"複審日期","maps_to":"H1","metric":"三項假設與全部風險列","threshold":"Q4 財報公布","action":"重跑研究","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"Power Systems 營收年增","bear_threshold":"連 4 季<+5%","window":"4 季","source":"8-K 分部表","last_status":"ok"},{"metric":"Power Systems EBITDA 率","bear_threshold":"連 2 季<25% 削弱，連 4 季<22% 清倉","window":"2–4 季","source":"8-K 分部表","last_status":"warning"},{"metric":"Engine 段 EBITDA 率","bear_threshold":"連 2 季<8%","window":"2 季","source":"8-K 分部表","last_status":"ok"},{"metric":"全公司 EBITDA 率","bear_threshold":"連 2 季<16.5% 削弱，連 4 季<15% 反轉","window":"2–4 季","source":"8-K","last_status":"ok"},{"metric":"大型機組訂單排程","bear_threshold":"由 2028 下半年縮短到 2027 年內","window":"每季","source":"法說","last_status":"ok"},{"metric":"北美 Class 8 月訂單","bear_threshold":"2027 H1 月訂單<15,000 輛","window":"2027 H1","source":"ACT Research（事實表只到 2026 年 5 月）","last_status":"unknown"},{"metric":"北美 Class 8 電動滲透率","bear_threshold":">10%","window":"3–5 年","source":"事實表未涵蓋，資料缺口","last_status":"unknown"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-33.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"2027 年 2 月財測：FY2027 營收成長中點≥7%、EBITDA 率中點≥18.5%，且財測後共識 FY2027 EPS≥33 美元，三項全中才重跑研究","exec_line":"未持有先不動。三項全中後重跑研究，通過才建首筆，不超過 2%；股價跌到 400 美元以下、12 月 EPA 定案 NCP 可轉嫁且無訂單取消，可先試 1%。"},"reasoning":{"industry":"Q3 營收 94.38 億美元，年增 13%，毛利率 27.7%，GAAP 營益率 15.3%，EBITDA 率 18.9%。分部含內部銷售，加總高於合併數：Engine 31 億美元（+20%，EBITDA 率 13.5%）、Components 29 億（+23%，14.3%）、Distribution 33 億（+4%，13.9%）、Power Systems 23 億（+15%，25.4%）、Accelera 1.03 億（虧損 5,600 萬）。CFO 在 2026-05-21 投資人日說，2025 年 Power Systems 加 Distribution 占 EBITDA 60%，2030 年不低於 50%。單點依賴有兩個：PACCAR 占 2025 年營收 13%（2024 年 16%），是唯一超過 10% 的客戶；資料中心積壓集中在大型超大規模客戶，金額事實表未涵蓋。Q3 EPS 8.25 美元含 7,500 萬美元離散稅項利多（每股 0.54 美元），扣掉後是 7.71 美元。全年指引由營收 +10–13% 收斂到約 +10%，主因是北美皮卡。","moat":"機制是引擎規模、售後網路與發電機組到安裝的一體化。管理層稱年產約 130 萬具引擎，超過最近對手兩倍；北美活躍公路引擎至少 220 萬具。方向證據：Power Systems EBITDA 率 Q3 升 250 個基點到 25.4%，定價為正，Q3 接單高於公司預期。反面是 PACCAR 占營收由 16% 降到 13%，最大客戶份額下滑就不能判擴大；中國卡車銷量 −15%、產業 −5%，公司歸因於電動卡車。TTM 營業利益率 11.79%，低於 Caterpillar 18.33%、Allison 18.88%，高於 PACCAR 10.75%、Generac 10.37%。執行力 8 分；定價力本來 8 分，扣客戶自製威脅 1 分得 7 分。","growth":"成長以量為主，發電有漲價，併購為零，淨回購每年約 1 個百分點。公司目標是 2030 年營收 450–500 億美元（年增 6–9%）、EBITDA 率超過 20%。三年共識 EPS CAGR 由 FY2025A 20.5 美元起算是 25.7%，由 FY2026E 29.59 美元到 FY2028E 40.69 美元是 17.3%；內生上界 13.2%。缺口 12.5 個百分點（FY2026E 起算為 4.1），來源依序是 FY2025 含 Accelera 費用的低基期、利潤率由 17.4% 往 20% 以上擴張、淨回購，沒有收購。Base 五年 EPS 年增 10.2%，在上界內。反例：若增量報酬的代理值高估，上界會更低，Base 也會變吃力。","governance":"FCF／淨利 FY2025 為 0.84，FY2024 為 0.07，後者含 19 億美元和解付款；TTM FCF 利潤率 9.66%。Q3 營業現金流 14.05 億美元、資本支出 3.03 億、FCF 11.02 億，回購 3.59 億加股息 3 億，約 47% 的營業現金流回給股東；今年累計 16.81 億美元。資本支出指引 13.5–14.5 億美元，併購為零，債務到期結構事實表未涵蓋。淨負債 33.34 億美元，約 FY2026 指引 EBITDA 67 億美元的 0.5 倍。SBC 金額事實表未涵蓋，改用股數判斷。","valuation":"現價 450.07 美元，要 10% 年報酬（股息 1.82%，股價年增 8.2%），五年後要 667 美元；用 14 倍終端本益比，等於 FY2031 EPS 47.6 美元，年增 10%。公司 2030 目標（營收 450–500 億美元、EBITDA 率 20–21%）換算約 41–48 美元，換算用 FY2026E 淨利÷EBITDA 約 60%、2030 年 1.32 億股。市場沒有定價崩盤，定價的是目標大致達成；而共識 FY2028E 40.69 美元已貼近這個區間下緣，比公司目標早兩年。賣方目標價 745–757 美元都是 Q3 前資料，區間 500–894 美元，高低比 1.79 倍，對本次結論沒有參考力。反例：若 2030 目標偏保守，現價其實便宜。","premortem":"第一種錯法是太保守：Q3 接單高於公司預期，排程到 2028 下半年，股價可能在 2 月財測前就反彈，等待會買貴。第二種是還不夠保守：Bear 的 FY2029 EPS 24 美元只比 FY2026E 低 19%，而 2008 年第四季 EBIT 率曾由 9.2% 降到 3.9%，2019 年 Class 8 產量九個月跌 55%；資料中心和卡車同時下行時，跌幅可能超過 −50%。半年跌 33% 的原因事實表未涵蓋，法說只看到分析師問選舉消息與資料中心能源爭議，不能當成已知原因。RSI 23.81 代表賣壓重，不代表到底。歷史最大回撤與空方論點事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺的是卡車廠、車隊和資料中心的動力設備與售後錢，獲利正從卡車引擎往發電與經銷移動，錢卡在大型發電機組的產能和全球服務網路這一節。","moat":"護城河持平（→）：發電端在加寬，卡車端被 PACCAR 自製和中國電動卡車削掉一塊，兩邊相抵。","growth":"成長跑道中等（🟡）：卡車引擎已成熟，第二條曲線是資料中心與主電力天然氣，但 130 公升機組還沒收正式訂單，2029 年才有像樣營收。","capital":"現金生成改善，回饋紀律清楚，但零排放的併購和投資交了學費，回購價位也還算不出來。","valuation":"現價要的是 2030 目標大致兌現，我信大半，所以算合理價，不算便宜。","how_wrong":"最可能看錯的是 2027 年獲利基礎：Q3 實質低於預期，共識還沒動，便宜的本益比可能建立在高點獲利上。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月 Q4 財報的 FY2027 指引：營收成長中點≥7%、EBITDA 率中點≥18.5%，且財測後共識 FY2027 EPS≥33 美元。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":450.07,"week26_return_pct":-33.31,"consensus_rev_3m_pct":-0.24,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母是 FY2026E 共識 29.59 美元，利潤率在歷史高位，含 Q1 的 1.99 億美元出售損失與 Q3 每股 0.54 美元稅項利多；11-07 快照未反映 Q3 財測收斂。股價半年跌 33%，FY1 共識三個月只修 −0.24%，爭點就是這個分母守不守得住。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"EPA 2027 最終規則預計公布，NCP 金額是主要未知數。","impact":"高","watch":"NCP 能否全額轉嫁，過渡安排是否改變。"},{"date":"2027-01","date_precision":"month","type":"product","event":"X10 與 X15 新平台開始限量生產。","impact":"中","watch":"上量品質、保固提列。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 FY2027 財測。","impact":"高","watch":"營收成長、EBITDA 率、Power Systems 指引、Q4 補出貨。"},{"date":"2027-Q3","date_precision":"quarter","type":"product","event":"X10 全面量產，X15 第四季接續。","impact":"中","watch":"新舊平台切換是否造成訂單斷層。"},{"date":"2028-Q1","date_precision":"quarter","type":"capacity","event":"20GW 新增產能進入較大幅度的上線期，7 公升新引擎 1 月上市。","impact":"高","watch":"新增供給是否被訂單消化，Power Systems 定價。"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,213B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河 B 級持平，發電加寬，卡車被削。</p>
<ul class="pts">
<li>護城河機制是全球引擎規模、售後服務網路，加上發電機組到安裝的一體化供應。管理層稱年產約 130 萬具引擎，超過最近對手兩倍，北美活躍公路引擎至少 220 萬具。這個規模讓售後零件與服務有穩定基礎。</li>
<li>執行力給 8 分。Power Systems EBITDA 率 Q3 升 250 個基點到 25.4%，Q3 接單高於公司預期。定價力本來 8 分，扣客戶自製威脅 1 分得 7 分。綜合分數 7.5，等級 B。</li>
<li>方向判持平（→）。正面證據是發電端定價與利潤率擴大。反面是 PACCAR 占營收由 16% 降到 13%，最大客戶份額下滑就不能判擴大，中國銷量跌幅比產業多 10 個百分點。資料中心份額增減沒有一手數據，所以不判擴大。</li>
<li>TTM 營業利益率 11.79%，低於 Caterpillar 18.33% 與 Allison 18.88%，高於 PACCAR 10.75% 與 Generac 10.37%。毛利率 25.88% 在五家中偏低，研發密度 4.17% 則高於 Caterpillar 的 2.97%。同業 ROIC 事實表沒有，所以用利潤率比較。</li>
<li>最高的威脅是 PACCAR 擴自製引擎，機率 40%，燈號紅。10-K 也寫明客戶可能自行開發或改向他廠採購。占營收由 16% 降到 13%，但週期與自製各占多少，事實表拆不出來。</li>
<li>同業擴產是第二個威脅，機率 35%。Caterpillar 發電銷售成長 72%，Generac 資料中心積壓約 16 億美元，都擴得比康明斯快。Power Systems Q3 只增 15%，部分受自身產能與供應限制。</li>
<li>替代技術機率 30%。中國電動卡車已影響銷量，但只限當地公路車。北美重卡電動滲透率事實表沒有現值，這是資料缺口，資料中心本十年仍以柴油備援為主。</li>
<li>報酬持續期的代理值是 ROIIC 約 47%、再投資率約 28%，相乘得內生上界 13.2%。這是代理值，非實測，可能高估，因為 2022 年 Meritor 併購款不在分母。FY2024 淨利 39.46 億美元明顯偏高，一次性項目也未拆。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```