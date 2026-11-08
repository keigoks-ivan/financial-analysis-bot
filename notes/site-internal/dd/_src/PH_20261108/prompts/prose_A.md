你是 stock-analyst v20 的**散文層（prose）agent**，標的 PH（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：PH　日期：2026-11-08　archetype：None　前份裁決：2026-05-18　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2152B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（392B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1120B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1401B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1191B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（676B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1209B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2228B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4046B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3222B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2152           3394-4848      3 條（2–6 內）  
s3                  8000         392           5326-7608      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3712          7902-11288      5 條（2–6 內）  
s6                 11000         676          7227-10324      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1209           1604-2291      3 條（2–6 內）  
s10                 5000        2228           1940-2772      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3222           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5041B；至少需散文≈39.96KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−43%
−43
−28
−28%
−1%
−1
−0.5%
0
0.04
0.28%
0.39
0.5
0.63
0.63%
0.7
0.75
0.95
1.0
1
1.07
1.09
1.14
1.3
1.4%
1.5%
1.87
1.97
2%
02
2
2.03
2.10
2.2
2.27
2.32
2.5
2.6
2.7
3
3.0
3.2%
3.3%
3.41
3.5
3.7%
4%
4
4.0%
4.1%
4.28
4.3
4.5%
4.64
4.9
5
5%
05
5.3%
5.3
5.6
6%
6
6.0%
06
6.3
6.4%
6.5%
6.80
7.0
7
07
7%
7.2%
7.2
7.4%
7.5%
08
8
8%
8.0
8.31%
8.82
9
9%
09
9.4%
9.5%
10
10%
10.1
10.5
10.7%
10.7
11
11.4
11.4%
11.5%
11.6%
12
13%
13
13.3%
14
14%
14.8%
15
15%
15.7%
16.13%
17%
17
17.07
17.5%
18
18%
18.16%
18.5
18.5%
20
20%
20.41%
21.1
21.1%
21.4%
21.55%
21.7
22%
22.5%
23
23.08
23.4%
24
24.4%
24.45
24.9
24.91
25
25.5%
25.7
25.79
25.8
26.0%
26%
26
26.9
27
27%
27.0%
27.5%
27.6%
27.7%
27.9%
28.0%
28.2
28.4%
28.48
28.5%
28.6%
29.5%
29.7%
30%
30
30.05
30.5
30.7%
31%
33.0%
34.0%
35
35.0
35.59
35.9
36%
36.45
36.5
36.85
37.2
37.5
37.74%
38
39.05
39.5
39.77
40%
41
41.0
42
42.8%
43
43.5
44.14
45
45.3
47
47%
49
49.3
49.5
50%
50
52.5
53
53.5
54
56
59.92
60%
62
62.5
63
70
73%
73.89
75%
80
84.98
85%
90
92.5
93.6
94%
100
$100
100%
104
107%
120
137
150%
167.67
$220
270
306
318
364
455
525
657
680
711
737
800
862.72
917.79
945
984
2024
2025
2026
2027
2028
20261108
1,039.70
1,087
1,230
1,269
1,438
1,638
4,000
4,600
8,200
8,400
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
{"meta":{"ticker":"PH","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Parker-Hannifin Corporation"},"oneliner":"好公司，但價格已先走一步。工業復甦疊上航太，FY27 EPS 指引三個月上調 6%；現價約 FY27 指引 24.9 倍，Base 五年年化只有 6–7%，到 800 美元以下才值得動手。","thesis":{"H":[{"id":"H1","text":"工業復甦已從訂單走到出貨，加上航太長循環，FY27 有機成長達到指引中點 9%，之後五年平均不低於公司 4–6% 目標的上半段。","2y":"FY27 有機成長不低於 7.5%，FY28 不低於 5%，滾動 12 個月訂單維持正值。","5y":"FY27–FY31 平均有機成長不低於 5%。","10y":null,"threshold":"FY27 有機成長低於 7.5%，或 FY27–FY28 平均低於 5%。","source":"季度新聞稿的有機成長與滾動 12 個月訂單。","drift_rule":"2 年尺度：TTM 偏離路徑 5% 以上連 2 季算削弱，10% 以上連 3 季算反轉。5 年尺度：5% 以上連 4 季算削弱，10% 以上連 6 季算反轉。"},{"id":"H2","text":"部門利潤率的提升大多是結構性的，納入濾材集團後，仍能從 FY27 指引 27.9% 往公司 FY31 目標 30% 走。","2y":"FY28 調整後部門利潤率不低於 28.0%。","5y":"FY31 不低於 29.5%，FCF 利潤率回到 17%。","10y":"下一次工業衰退期間，單年部門利潤率不低於 26%。","threshold":"FY28 低於 27.0% 即論點失效；FY29 低於 28.0% 算削弱。","source":"季度新聞稿與法說。","drift_rule":"5 年尺度：連 4 季偏離路徑 5% 以上算削弱，連 6 季偏離 10% 以上算反轉。10 年尺度：跨 2 個年度算削弱，跨 3 個年度算反轉。"},{"id":"H3","text":"濾材集團與後續併購要把現金做大，不只把調整後 EPS 做大：2.2 億美元綜效兌現，槓桿按計畫回落。","2y":"FY27 綜效達 4,000 萬美元，FY28 結束累計不低於 1 億美元；2028-06 季淨負債對調整後 EBITDA 不高於 2.2 倍。","5y":"2.2 億美元綜效全數兌現，濾材集團 EBITDA 利潤率超過 30%；FY31 FCF 不低於 54 億美元。","10y":null,"threshold":"FY28 結束累計綜效低於 1 億美元，或 2028-06 季槓桿高於 2.5 倍。","source":"法說揭露的綜效累計數，新聞稿的槓桿與 FCF。","drift_rule":"2 年尺度：偏離路徑 5% 以上連 2 季算削弱，10% 以上連 3 季算反轉。"}],"R":[{"id":"R1","text":"復甦只走幾季就回落。亞太有機 +23.4% 靠電子與半導體拉動，管理層被問到 AI 相關占比時沒有給數字；滾動訂單又比單季訂單慢，轉折會晚看到。","h_ref":"H1","clock":"⚡","threshold":"滾動 12 個月訂單連 2 季下滑且低於 +6%，或亞太有機成長低於 +10%。","evidence_refs":[]},{"id":"R2","text":"濾材集團交易約當市值 8%，資金含 52.5 億美元 364 天與 25 億美元三年期貸款。整合若慢於計畫，利息先到、綜效後到；CIRCOR 還沒交割，槓桿可能升到約 3 倍。","h_ref":"H3","clock":"🔥","threshold":"FY27 綜效低於 4,000 萬美元，FY27 結束槓桿高於 3.0 倍，或 FY28 結束累計綜效低於 1 億美元。","evidence_refs":["major_events#1"]},{"id":"R3","text":"非美國銷售地點約占 36%，關稅、對中貿易限制、出口管制範圍變動與中東衝突墊高的物料物流成本，都可能壓縮利潤率。8,400 萬美元關稅退款已在 FY26 Q4 認列，後續退款金額較小。","h_ref":"H2","clock":"🔥","threshold":"吸收失敗判定：部門利潤率連 2 季年減 50 個基點以上，整體毛利率連 2 季年減 1 個百分點以上，或北美工業利潤率低於 25.5%。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#1"]},{"id":"R4","text":"航太 OEM 增產不如預期或售後退潮。航太約占營收三成、利潤率最高；管理層不談客戶機型產量，第三方報導訂單由 +18% 放緩到 +14%。","h_ref":"H1","clock":"🔥","threshold":"航太訂單連 2 季低於 +5%；沿用前份：737 月產量低於 35 架連 2 季，或 A320 在 2027 年到不了 70 架（月產量本輪事實表未涵蓋，屬資料缺口）。","evidence_refs":[]}],"single_thing":{"description":"FY28（2028-06 結束）全年調整後部門營業利益率低於 27.0%。","why_fatal":"這是五年路徑裡最大的單一營運敏感項。以 Base FY31 營收約 318 億美元計，部門利潤率每差 1 個百分點，EPS 差約 1.97 美元，占 Base 終端 EPS 3.7%，按 23 倍約 45 美元股價。低於 27.0% 代表濾材綜效加上量的復甦都撐不住利潤率，FY31 的 30% 目標不成立，本益比也會一起往 17–18 倍掉。","if_happens":"減碼一半，停止任何加碼；若 2028-06 季槓桿同時高於 2.5 倍，清倉。","how_monitor":"每季新聞稿的調整後部門利潤率與法說揭露的累計綜效；2027-08 公布 FY28 指引，中點低於 27.5% 就提前警戒。","probability":"12–24 個月約 15%。FY27 指引已含濾材稀釋仍有 27.9%，要跌 90 個基點以上，需要工業量明顯回落。"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.08,"peg_fy2":2.03,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":28.48,"FY2027E":35.59,"FY2028E":39.77,"FY2029E":44.14},"fy_end_month":6,"eps_basis":"FY2026A 為 GAAP 稀釋 EPS，共識三年為調整後 EPS，兩者口徑不同，由 GAAP 基期算出的三年 CAGR 約 15.7% 會高估。本判斷改用 FY27E 到 FY29E 兩年複合 11.4%。共識來自 Koyfin 2026-11-07 快照，尚未反映 2026-11-05 指引上修，家數事實表未列。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PH_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"營業利益率在營收只增 4.1% 的 FY23–FY25 擴大 4.28 個百分點，FCF 對淨利四年都在 94% 以上，但短循環工業仍決定年度波動。"},"industry":{"clock_phase":"II","sd_verdict_source":"擴張初段：本季是三年多來第一次有機雙位數，滾動 12 個月訂單 +13%，各終端市場全年都指引正成長。供需判斷：工業短循環屬週期性將反轉，時點未知；航太售後屬結構性持久，機隊老化、退役少；美國機械業產能利用率自 2024 年底上升，新產能正在進場。","bargaining":{"up":"原物料與物流仍在漲，公司以定價與供應鏈工具因應，目標是利潤中性。","down":"客戶分散，FY24 單一客戶不超過 4%，中小 OEM 靠經銷商服務；航太仍有部分定價談判在進行。","geo":"非美國銷售地點約占 36%，以在地生產因應關稅與貿易限制。"},"profit_pool_dir":"產業利潤池資料事實表未涵蓋；本季 PH 三個部門的利潤率同創新高。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池資料；公司只揭露併購後濾材年營收約 50 億美元，不足以展開。"}},"moat":{"mechanism":"應用工程師與全球經銷網把多項互連技術設計進客戶設備，替換需求跟著裝機基數走；2/3 營收來自買 4 項以上技術的客戶，85% 產品有智財保護。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：營業利益率由 FY23 的 16.13% 升到 FY26 的 21.55%，大部分發生在營收幾乎不動的期間。定價面穩定：2026-08-06 與 2026-11-05 兩次法說都說工業定價回到正常，財務長說價格對增量利潤率沒有影響。份額、留存與同業時序資料事實表未涵蓋，相對優勢是否擴大無法證明。","peer_na_reason":"事實表同業對照只有 TTM 利潤率單一時點，沒有投入資本與歷史序列，算不出 ROIC 差距與方向。","threats":[{"level":"🟡","text":"電動化以機電系統取代行動設備液壓，時間尺度約 10–15 年，第三方估液壓占工業部門 25–30%。來源是第三方與社群敘事，權威偏低；公司 2025-09 收購 Curtis 補電氣化能力。","p":"30%","evidence_refs":["substitute_technology#1","substitute_technology#2","competitive_share_entrants#3"]},{"level":"🟡","text":"全球與在地對手的降價壓力，以及 10-K 自承的技術快速變動。目前只有風險揭露，沒有份額流失的量化證據。","p":"20%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是設備操作與維修端，決策者是 OEM 工程師與經銷商，付款者是 OEM 與機隊營運商，三者都成立。航太售後占比 47%，機隊老化、退役少，維修需求難以長期延後。"},{"item":"決策層級","level":"🟡","text":"多數營收來自買 4 項以上技術的客戶，決策單位偏系統而非單一零件；但 10-K 自承對手數以百計，漲價後流失率與重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟢","text":"客戶分散，FY24 單一客戶不超過 4%，中小 OEM 透過經銷商採購，買方議價力低；成本上漲可轉嫁，公司目標是利潤中性。"},{"item":"社會容忍度","level":"🟢","text":"未見價格管制或依賴政府授權的證據。併購後濾材規模約 50 億美元，有一般性反壟斷風險，搜尋未見 2026 年政府調查。"}],"roiic":"併購段 5.3–6.5%（上界）：濾材集團年化營收約 21.1 億美元（18.5 億÷10.5×12），乘 30% EBITDA 目標得 6.3 億，扣稅 22.5% 得 4.9 億，除以 92.5 億得 5.3%；營收以 5% 成長四年到 25.7 億，同利潤率得 6.5%。未扣折舊，所以是上界。有機段投入資本事實表未涵蓋。","reinvest_rate":"FY27 單年併購約為 FY26 稅後營業利益的 2.6 倍（92.5 億÷35.9 億）；常態以股利後留存 FCF 約 73% 計（年股利約 10.1 億÷FCF 指引 37.5 億＝27%）。","endo_ceiling":10.7,"formula_note":"內生上界 10.7%＝公司有機目標上緣 6%（資本需求低，FCF 接近或高於淨利）＋併購段報酬 6.5%×留存率 73%。不含利潤率擴張，有機段是目標值，非由投入資本算出。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","PH":37.74,"HON":38.04,"ROK":49.35,"EMR":53.61,"ETN":35.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","PH":21.4,"HON":16.2,"ROK":19.74,"EMR":20.85,"ETN":17.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","PH":17.2,"HON":4.95,"ROK":16.51,"EMR":19.0,"ETN":11.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","PH":null,"HON":5.37,"ROK":7.89,"EMR":null,"ETN":2.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"HON","gm":38.04,"om":16.2,"fcf_margin":4.95,"rd_intensity":5.37,"strategy_note":"毛利率接近 PH，營業利益率與 FCF 利潤率都較低；組合差異大，不是液壓氣動的直接對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ROK","gm":49.35,"om":19.74,"fcf_margin":16.51,"rd_intensity":7.89,"strategy_note":"毛利率明顯較高，營業利益率略低；事實表無分部資料，重疊程度無法判斷。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"EMR","gm":53.61,"om":20.85,"fcf_margin":19.0,"rd_intensity":null,"strategy_note":"毛利率與 FCF 利潤率高於 PH，營業利益率接近，是獲利結構最值得對照的一家。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ETN","gm":35.05,"om":17.32,"fcf_margin":11.87,"rd_intensity":2.75,"strategy_note":"毛利率、營業利益率與 FCF 利潤率都低於 PH；事實表無分部資料，重疊程度無法判斷。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"FY27 報表成長約一半有機、一半併購；有機成長上修來自量，不是價格；EPS 成長再加上利潤率擴張，回購貢獻很小。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"沿用護城河段的 10.7%：有機目標上緣 6% 加併購報酬 6.5% 乘留存率 73%；共識 11.4% 高出 0.7 個百分點，缺口歸因利潤率擴張。","segments":[{"item":"北美工業","value":"Q1 營收 24.45 億美元，有機 +9.4%，利潤率 27.6%；FY27 有機指引中點 8%。"},{"item":"國際工業","value":"Q1 營收 17.07 億美元，有機 +11.6%，亞太 +23.4%，EMEA +4%，拉美 −1%；FY27 有機指引中點 9.5%。"},{"item":"航太","value":"Q1 有機 +14%，利潤率 30.7%，訂單 +14%；FY27 有機指引中點 10%，OE 與售後比重 53／47。"},{"item":"濾材集團","value":"FY27 計入營收 18.5 億美元，約 10.5 個月；歷史中個位數成長；累計成本綜效目標 2.2 億美元，FY27 為 4,000 萬。"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"年度毛利率連三年上升，TTM 37.74%。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"事實表未涵蓋份額資料，未見流失報導。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"本季成長由量帶動。"},{"signal":"EPS 年複合顯著高於營收","lit":true,"note":"FY23–FY26 GAAP EPS 年複合 21.1%，營收 4.1%，差 17 個百分點。"},{"signal":"FCF 對淨利低於 0.75 連 2 年","lit":false,"note":"FY25 為 0.95，FY26 為 1.07。"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"Q1 為 1.4%。"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"電動化屬 10–15 年尺度，列入觀察。"},{"signal":"產業倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋同業倍數歷史。"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"Q1 總資本支出約 1.09 億美元，占 FCF 17%。"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"FY26 營收年增 8.31%，管理層稱靠精實生產增加產能。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"股利","value":"每季 2 美元，連續 306 季；TTM 殖利率 0.63%。"},{"item":"回購","value":"FY26 10 億美元；均價事實表未涵蓋。"},{"item":"併購","value":"濾材集團現金 92.5 億美元，2026-08-13 完成；CIRCOR 航空業務待完成，金額事實表未涵蓋。"},{"item":"債務","value":"淨負債 167.67 億美元，淨負債對調整後 EBITDA 2.7 倍，目標約 6 季回到 2 倍。"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"歷次併購的投入資本與已實現報酬事實表未涵蓋，無法判定。濾材集團未滿一年，事前推算 5.3–6.5%，低於假設的 8% 資金成本，要看 FY29 實績。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"以現價算，盈餘收益率 GAAP 約 3.3%、調整後約 4.0%。10 年期殖利率事實表未涵蓋，但這個報酬連新債約 4.5% 的平均利率都不到，更達不到殖利率加 2%。回購均價未揭露，以現價代用。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q1 SBC 8,200 萬美元，年化占市值約 0.28%，遠低於 1.5%；本季股數減少貢獻 EPS 0.04 美元。","grade":"過"}]},"valuation":{"basis":"調整後 EPS 前瞻本益比，起點用 FY27 指引中點 36.85 美元，並以 GAAP EPS 與 FCF 殖利率校正。","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業前瞻本益比，倍數無法比；判斷改靠自身年度端點與情境樹。"},"fwd_pe":25.79,"peg":2.27,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"偏貴：FY27 指引中點 24.9 倍（財報前共識 25.8 倍），GAAP 指引中點約 30.5 倍；PEG 2.27；FCF 指引對市值殖利率約 3.2%；本益比與 EV 對營收在年度端點分位 80 與 93.6；Base 五年年化約 6–7%。五年高低點事實表未涵蓋，不計五年分位。","upside_short_pct":7.2,"upside_mid_pct":18.5},"trap_analysis":{"verdict":"🟡","label":"EPS 成長主要靠利潤率擴張，營收成長偏低"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"部門利潤率 28.6% 創新高，同時是三年多來第一次有機雙位數；EV 對營收在年度端點的 93.6 分位。","assumption":"假設利潤率的提升能跨過下一次工業衰退。","consequence":"五年虧 50% 最可能的路徑：FY29 前後工業衰退，EPS 跌到約 35 美元，本益比由約 25 倍掉到 13–15 倍，股價落在 455–525 美元，較現價跌 43–50%。","ruling":"部分採納。營業利益率 FY23–FY25 在營收只增 4.1% 時擴大 4.28 個百分點，這段不是量帶出來的；FY26 的 1.14 個百分點中，0.39 來自關稅退款，其餘 0.75 是量與執行混合。保留 Bear 機率 30%，並以 FY28 利潤率低於 27.0% 作為唯一致命點。","watch":"調整後部門利潤率、滾動 12 個月訂單、北美工業利潤率。","evidence_refs":[],"fact_refs":["f_kpi1_adjusted_segment_operati","f_ev_s_percentile"]},{"view":"論點成功但股東經濟變差","evidence":"濾材集團達到 30% EBITDA 目標後，稅後報酬約 5.3–6.5%，低於本判斷假設的 8% 資金成本。FY27 FCF 指引中點 37.5 億美元低於 FY26 的 39.05 億。GAAP EPS 指引中點比調整後低 6.80 美元。收購資金含 52.5 億 364 天與 25 億三年期延遲提款貸款。","assumption":"假設調整後 EPS 成長等於股東實得。","consequence":"整合全部成功、調整後 EPS 照路徑走，但投入資本賺不到資金成本，每股 FCF 跟不上，市場可能改看目前約 3.2% 的 FCF 殖利率。","ruling":"採納。長期信心只給中。管理層說併購管線仍活躍，2027-05 投資人會議還有消息；下一筆大案前，要先看到槓桿回到 2 倍附近。","watch":"每股 FCF、GAAP 與調整後 EPS 差距、槓桿回落速度。","evidence_refs":["major_events#1"],"fact_refs":["f_kpi7_fy2027_guidance_filtrati","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"現價約 FY27 指引中點 24.9 倍，GAAP 口徑約 30.5 倍，PEG 約 2.27；Base 五年年化約 6–7%。","assumption":"假設市場會繼續給 25 倍左右的本益比。","consequence":"基本面照 Base 走，報酬也只是盈餘成長扣掉倍數收斂，沒有安全邊際。","ruling":"採納。現價不追，等 800 美元以下。","watch":"股價相對 FY27 與 FY28 指引的倍數。","evidence_refs":[],"fact_refs":["f_price_at_dd","f_fwd_pe_latest"]}],"max_dd":{"lo":-43,"hi":-28,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 862.72 → 本次 917.79（+6.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=862.72","side_b":"本次 price_at_dd=917.79","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 862.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 862.72 美元：五年期望值 +33.0%，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 862.72 美元：Bull 價 1,638、Bear 價 711，五年期望值 +34.0%，基準年化 7.4%，不對稱比 3.41","ruling":"先換情境、股價不動：五年期望值多 1.0 個百分點。前份未列不對稱比，本次為 3.41。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 862.72 美元：五年期望值 +34.0%，基準年化 7.4%，不對稱比 3.41","side_b":"本次情境、股價 917.79 美元：五年期望值 +26.0%，基準年化 6.0%，不對稱比 2.32","ruling":"再換股價、情境不動：起點價上漲 6.4%，五年期望值少 8.0 個百分點，基準年化少 1.3 個百分點，不對稱比由 3.41 降到 2.32。合計五年期望值比前份少 7.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"利潤率是結構還是週期","cause":null,"prior_field":null,"side_a":"結構：FY23–FY25 營業利益率由 16.13% 升到 20.41%，營收只增 4.1%；國際工業靠過去兩年重組，本季擴大 270 個基點。","side_b":"週期：本季有機 11.5% 帶來 120 個基點擴張，財務長自己說 Q1 特別好；FY26 的 21.55% 含 8,400 萬美元關稅退款；濾材集團起跳利潤率低於舊業務。","ruling":"可調和，屬程度差異。約 4.3 個百分點可視為結構性，0.75 個百分點是量與執行混合，0.39 個百分點是一次性。結構部分含歷次併購的組合變化，無法再拆，這個殘差已放進 Bear 機率 30%。","evidence_level":"中：年報與法說，無法拆開價格、組合與併購。","settle_metric":"FY28 調整後部門利潤率。","if_then":["若 FY28 低於 27.0%，減碼一半。","若 FY28 高於 28.5% 且有機成長回落到 5% 以下，代表結構性成立，股價不高於 945 美元時分批反買。"],"evidence_refs":[]},{"axis":"調整後 EPS 與現金","cause":null,"prior_field":null,"side_a":"FY27 調整後 EPS 指引上調到 36.85 美元，三個月內上調 2.10 美元。","side_b":"同一份指引的 FCF 中點 37.5 億美元，低於 FY26 的 39.05 億；FCF 利潤率約 14.8%，低於公司 17% 的長期目標與 FY26 的 18.16%；Q1 FCF 只占營收 10.7%。","ruling":"可調和。差距來自新增約 3.5 億美元利息、併購帶來的現金影響與下半年現金集中。GAAP EPS 中點 30.05 美元較貼近現金，所以本判斷用 3.2% 的 FCF 殖利率校正 24.9 倍的印象。FY28 是第一個較乾淨的年度。","evidence_level":"高：公司指引與年度財報。","settle_metric":"FY27 FCF 是否不低於 35 億美元；FY28 FCF 利潤率是否回到 17% 附近。","if_then":["若 FY27 FCF 低於 35 億美元，停止加碼。","若 FY28 FCF 利潤率達 17% 以上，這項疑慮解除，股價不高於 945 美元時分批反買。"],"evidence_refs":[]},{"axis":"指引與訂單的落差，以及訂單口徑更換","cause":null,"prior_field":null,"side_a":"2026-08-06 法說，Jeff Sprague 問滾動訂單 9–10% 與工業指引 4–7% 的落差，管理層沒有解釋大小，只說訂單不是精確預測。","side_b":"2026-11-05 有機指引中點由 7% 上調到 9%，Q1 實績 11.5% 高於原本 8% 的指引，證明當時指引偏保守。但 2026-08-06 執行長 Parmentier 宣布工業部門改用滾動 12 個月訂單，理由之一是國際訂單波動大，這個口徑會把轉折平滑掉。","ruling":"可調和。短期偏多的判斷被驗證，但滾動口徑讓下行訊號晚到，不能只看訂單，要搭配亞太有機成長與經銷商訂單。","evidence_level":"中：法說原話，單季訂單已不揭露。","settle_metric":"滾動 12 個月訂單與單季有機成長是否背離。","if_then":["若滾動訂單仍升而單季有機成長連 2 季下滑，停止加碼。","若兩者同升且股價到 800 美元以下，分批反買。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"賣方平均目標價 1,039.70 美元，高於現價 13.3%，區間 680–1,269，且資料在 7 月底，還沒反映 Q1。指引三個月上調 6%，有機成長加速，舊業務增量利潤率指引在高 30% 到低 40%，財報前共識 35.59 美元明顯過時。","side_b":"平均目標價等於 FY27 指引 28.2 倍，需要市場再給更高倍數；Base 五年年化約 6–7%，Bull 約 13%。","ruling":"賣方全距最高除以最低 1.87 倍，分歧不大，目標價方向反對本裁決，但差距來自倍數，不是盈餘：本判斷 FY28 EPS 41.0 美元已高於過時共識 39.77。市場給 25 倍不算錯，只是買在這裡賺的是盈餘成長減倍數收斂。","evidence_level":"中：目標價為二手彙整。","settle_metric":"2027-08 的 FY28 初始指引與當時股價。","if_then":["若股價續漲而 FY28 指引中點未到 43 美元，不追。","若股價跌到 800 美元以下而基本面門檻都沒踩線，分批反買。"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：10-K 列出數以百計對手，沒有第三方份額資料，也未見新進入者或對手勝出報導。結構：航太在手訂單由 73.89 億美元增到 84.98 億，濾材售後比重上升。","side_b":"其他：電動化取代液壓屬 10–15 年尺度，來源權威低；併購後濾材年營收約 50 億美元，有反壟斷曝險，但未見政府調查。","ruling":"裁決＝靜態。競爭面沒有惡化證據，改善主要來自公司組合變化，不是產業本身，依據是 FY26 年報競爭段與 2026-11-05 法說。","evidence_level":"低：缺第三方份額資料。","settle_metric":"第三方份額資料，事實表未涵蓋。","if_then":["若出現對手在主要平台勝出的具名報導，停止加碼。","若 Curtis 電氣化產品在主要行動設備 OEM 勝出且液壓營收未降，電動化威脅機率由 30% 下調到 15%。"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"axis":"前份留空的欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份裁決、角色、跑道、公司類型、循環位置、最大回撤與情境機率皆未填。","side_b":"本次跑道中等，公司類型為品質複利成長，循環位置早循環，最大回撤 −28% 到 −43%，情境機率 20、50、30。","ruling":"屬填欄差異，不代表看法改變。","evidence_level":"低：前份沒有數字可比。","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"評級與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"2026-05-18 評級 B，估值偏貴，股價 862.72 美元。","side_b":"本次評級 B，估值偏貴，股價 917.79 美元，上漲 6.4%。","ruling":"股價上漲與 FY27 指引上調 6% 大致相抵，結論不變。","evidence_level":"高：價格與公司指引。","settle_metric":"股價相對 FY27 指引的倍數。","if_then":["若股價回到 800 美元以下，分批反買。"],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份方向向上。","side_b":"本次穩定：執行面擴大，定價面穩定。","ruling":"2026-08-06 與 2026-11-05 兩次法說都說工業定價回到正常，財務長說價格對增量利潤率沒有影響；也沒有份額或同業時序資料能證明相對優勢擴大，所以改判穩定。","evidence_level":"中：管理層原話，缺第三方資料。","settle_metric":"同業利潤率時序或第三方份額資料。","if_then":["若同業時序顯示 PH 利潤率領先幅度連 4 季擴大，方向改回向上。"],"evidence_refs":[]},{"axis":"價值陷阱評估","cause":"方法變動","prior_field":["trap"],"side_a":"前份無陷阱疑慮。","side_b":"本次一項衰退訊號亮燈：FY23–FY26 GAAP EPS 年複合 21.1%，營收 4.1%。","ruling":"本輪逐項計算十類訊號才抓出來，不是基本面轉差，但提醒過去的 EPS 主要靠利潤率，這條路不能無限延伸。","evidence_level":"高：年度財報。","settle_metric":"EPS 與營收年複合差距。","if_then":["若 FY28 有機成長低於 5% 而利潤率也不再擴張，停止加碼。"],"evidence_refs":[]},{"axis":"重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件。","side_b":"股價收盤回到 800 美元以下（約 FY27 指引中點 21.7 倍，接近 104 週均線）","ruling":"本次把不追的原因限定為價格，到價後先重跑研究，基本面門檻沒踩線才分批加碼。","evidence_level":"中：情境樹推算。","settle_metric":"收盤價。","if_then":["若到價時利潤率或訂單門檻已踩線，不追。"],"evidence_refs":[]},{"axis":"量化出場指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設量化出場指標。","side_b":"FY28 調整後部門利潤率低於 27.0%；滾動 12 個月訂單連 2 季下滑且低於 +6%；2028-06 季槓桿高於 2.5 倍；FY27 FCF 低於 35 億美元；FY28 結束累計綜效低於 1 億美元；北美工業利潤率低於 25.5%；整體毛利率連 2 季年減 1 個百分點；737 月產量低於 35 架連 2 季或 A320 在 2027 年到不了 70 架。","ruling":"新增量化標準。第一條踩到就減碼一半，第一條與第三條同時踩到就清倉，其餘踩到停止加碼或減碼三分之一。","evidence_level":"中：門檻為本判斷設定。","settle_metric":"各指標最新季度值。","if_then":["若第一條踩線，減碼一半。"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing。","side_b":"FY28（2028-06 結束）全年調整後部門營業利益率低於 27.0%。","ruling":"本次新設 Single Thing，選五年路徑裡敏感度最大的一項；濾材整合與訂單反轉最後都會反映到這個數字。","evidence_level":"中：敏感度由 Base 路徑推算。","settle_metric":"FY28 全年調整後部門營業利益率。","if_then":["若踩線，減碼一半。"],"evidence_refs":[]},{"axis":"舊風險門檻：北美工業利潤率","cause":"新證據","prior_field":["R2"],"side_a":"整體 GM 連 2 季 YoY -1pp；Industrial NA segment OI margin 跌破 22%","side_b":"整體毛利率連 2 季年減 1 個百分點（保留）；北美工業利潤率低於 25.5%","ruling":"本季北美工業利潤率已到 27.6%，22% 的舊線離現況 5.6 個百分點，等於不設防。新線上移到 25.5%，踩到就減碼三分之一。","evidence_level":"高：新聞稿數字。","settle_metric":"北美工業調整後利潤率。","if_then":["若低於 25.5%，減碼三分之一。"],"evidence_refs":[]},{"axis":"舊風險門檻：濾材集團交割與綜效","cause":"新證據","prior_field":["R3"],"side_a":"close 延後超過 2027 Q1；首年 synergy < $100M（vs $220M target）","side_b":"FY27 綜效低於 4,000 萬美元；FY28 結束累計低於 1 億美元","ruling":"交割已在 2026-08-13 完成，第一項退休。管理層首次揭露 FY27 只排 4,000 萬美元，換算 12 個月約 4,600 萬，按舊門檻字面已低於 1 億美元，也低於前份首 12 個月達 50% 的驗證點。這是前份假設的時程太前，不是整合出事，但綜效與 EPS 增厚都比前份想的晚。新門檻對齊公司時程，未達就減碼三分之一。","evidence_level":"中：管理層揭露，整合實績還沒出來。","settle_metric":"法說揭露的累計綜效。","if_then":["若 FY28 結束累計低於 1 億美元，減碼三分之一。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY27 有機成長守住指引下緣。","type":"假設驗證","maps_to":"H1","metric":"FY27 有機成長率","threshold":"低於 7.5%","action":"停止加碼","source_freq":"季度新聞稿","date":"2027-08"},{"n":2,"text":"FY28 全年調整後部門營業利益率低於 27.0%。","type":"Single Thing","maps_to":"Single Thing","metric":"調整後部門營業利益率","threshold":"FY28 低於 27.0%","action":"減碼一半","source_freq":"季度新聞稿","date":"2028-08"},{"n":3,"text":"FY28 利潤率踩線，同時還債落後。","type":"清倉","maps_to":"Single Thing","metric":"調整後部門營業利益率與淨負債對調整後 EBITDA","threshold":"FY28 低於 27.0%，且 2028-06 季高於 2.5 倍","action":"清倉","source_freq":"季度新聞稿","date":"2028-08"},{"n":4,"text":"股價回到 800 美元以下。","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"不高於 800 美元","action":"重跑研究，利潤率與訂單門檻都沒踩線才分批反買","source_freq":"每日股價","date":null},{"n":5,"text":"復甦提早回落。","type":"風險","maps_to":"R1","metric":"滾動 12 個月訂單；亞太有機成長","threshold":"訂單連 2 季下滑且低於 +6%，或亞太低於 +10%","action":"停止加碼","source_freq":"季度新聞稿與法說","date":null},{"n":6,"text":"濾材集團綜效或還債落後。","type":"風險","maps_to":"R2","metric":"累計綜效；淨負債對調整後 EBITDA","threshold":"FY27 綜效低於 4,000 萬美元，FY27 結束槓桿高於 3.0 倍，或 FY28 結束累計低於 1 億美元","action":"減碼三分之一","source_freq":"季度法說","date":"2027-08"},{"n":7,"text":"關稅與貿易成本吸收失敗。","type":"風險","maps_to":"R3","metric":"調整後部門利潤率、毛利率、北美工業利潤率","threshold":"部門利潤率連 2 季年減 50 個基點以上，毛利率連 2 季年減 1 個百分點，或北美工業低於 25.5%","action":"減碼三分之一","source_freq":"季度新聞稿","date":null},{"n":8,"text":"Davidson Instruments 私人壟斷訴訟：Parker 已聲請駁回，尚未見裁決；受影響營收與求償金額事實表未涵蓋。","type":"風險","maps_to":"R3","metric":"法院對駁回聲請的裁定；公司揭露的可能損失","threshold":"駁回聲請遭否決，且公司揭露可能有重大影響","action":"減碼三分之一；轉為政府調查或刑事介入則清倉","source_freq":"10-Q 訴訟附註，每季","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":9,"text":"航太增產或售後不如預期。","type":"風險","maps_to":"R4","metric":"航太訂單年增率；737 與 A320 月產量","threshold":"航太訂單連 2 季低於 +5%，或 737 低於 35 架連 2 季，或 A320 在 2027 年到不了 70 架","action":"停止加碼","source_freq":"季度法說；月產量為資料缺口","date":null},{"n":10,"text":"股價提前走到 Base 五年終點。","type":"減碼","maps_to":"H2","metric":"收盤價","threshold":"不低於 1,230 美元，約 FY28 Base EPS 的 30 倍","action":"減碼四分之一","source_freq":"每日股價","date":null},{"n":11,"text":"FY28 指引高於 Base 且價格合理。","type":"加碼","maps_to":"H2","metric":"FY28 初始 EPS 指引中點與股價","threshold":"指引中點不低於 43 美元，且股價不高於 945 美元","action":"重跑研究後分批加碼","source_freq":"2027-08 財報","date":"2027-08"},{"n":12,"text":"2027 投資人會議後複審。","type":"複審日期","maps_to":"H3","metric":"新的長期有機成長、利潤率目標與併購規模","threshold":"會議結束","action":"重跑研究，新目標與併購規模納入情境樹","source_freq":"投資人會議","date":"2027-05-13"}],"kill_metrics":[{"metric":"FY28 全年調整後部門營業利益率","bear_threshold":"低於 27.0%","window":"FY2028（2028-06 結束）","source":"公司季度新聞稿","last_status":"ok"},{"metric":"滾動 12 個月訂單","bear_threshold":"連 2 季下滑且低於 +6%","window":"連續 2 季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"淨負債對調整後 EBITDA","bear_threshold":"2028-06 季高於 2.5 倍","window":"2028-06 季","source":"公司法說","last_status":"ok"},{"metric":"FY27 自由現金流","bear_threshold":"低於 35 億美元","window":"FY2027","source":"公司季度新聞稿","last_status":"unknown"},{"metric":"濾材集團累計成本綜效","bear_threshold":"FY28 結束低於 1 億美元","window":"至 2028-06","source":"公司法說","last_status":"unknown"},{"metric":"北美工業調整後利潤率","bear_threshold":"低於 25.5%","window":"單季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"整體毛利率年變化","bear_threshold":"連 2 季年減 1 個百分點以上","window":"連續 2 季","source":"公司季報","last_status":"ok"},{"metric":"737 與 A320 月產量","bear_threshold":"737 低於 35 架連 2 季；A320 在 2027 年到不了 70 架","window":"至 2027 年底","source":"資料缺口，事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=4.64, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='早循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價收盤回到 800 美元以下（約 FY27 指引中點 21.7 倍，接近 104 週均線）","exec_line":"現價不追。股價到 800 美元以下、利潤率與訂單門檻都沒踩線時，先重跑研究，再分批買進，第一筆不超過預定部位的三分之一。"},"reasoning":{"industry":"Q1 FY27 營收 59.92 億美元：北美工業 24.45 億，有機 +9.4%，利潤率 27.6%；國際工業 17.07 億，有機 +11.6%，利潤率 27.7%；航太有機 +14%，利潤率 30.7%。調整後部門利潤率 28.6%，GAAP 部門利潤率 24.4%；TTM 毛利率 37.74%，營業利益率 21.4%。在手訂單 137 億美元，約 75% 在 12 個月內轉成營收。單點依賴不在客戶：FY24 年報單一客戶不超過 4%，FY26 年報稱無信用集中風險。真正的集中是循環，短循環工業決定年度波動。資料中心約占 1.5%，還不足以左右結果。分部資料取自 2026-11-05 法說與新聞稿。","moat":"機制：應用工程師加全球經銷網，把互連技術設計進客戶設備，之後的替換需求跟著裝機基數走。當期：TTM 營業利益率 21.4% 是對照同業最高，毛利率 37.74% 在五家只排第四，優勢在費用效率與組合，不在單價；投入資本事實表未涵蓋，ROIC 算不出來，象限依併購商譽推斷。持續期：四項檢查中，決策層級因缺流失率資料只給黃燈。增量：濾材集團事前推算報酬 5.3–6.5%，低於本判斷假設的 8% 資金成本，EPS 增厚靠的是 4.5% 左右的舉債。","growth":"FY27 報表成長指引中點 17.5%，其中有機 9%、併購約 9%、匯率 −0.5%。財報前共識 FY27E 到 FY29E 年複合 11.4%；FY2026 只有 GAAP 基期，與調整後共識口徑不同，不拿來算 CAGR。內生上界 10.7%，缺口 0.7 個百分點，歸因利潤率擴張（FY27 指引 27.9%，公司 FY31 目標 30%）。Base 由 FY27 到 FY31 年複合 9.5%，在上界以內。TAM 與滲透率事實表未涵蓋，跑道年數無法換算。資料中心約占 1.5%，雙位數成長，但管理層說還不到獨立的垂直市場；生命科學只是濾材集團內成長較快的一塊。","governance":"FY26 FCF 39.05 億美元，對淨利 107%，FY23–FY26 都在 94% 以上。Q1 SBC 占營收 1.4%。資金去向：Q1 資本支出約 1.09 億；股利每季 2 美元，連續 306 季；FY26 回購 10 億；最大用途是併購，濾材集團付現 92.5 億。Q1 季底淨負債對調整後 EBITDA 2.7 倍，新債平均利率略高於 4.5%；2026-08-06 管理層說峰值約 3 倍、約 6 季回到 2 倍。近三年完整現金去向、債務到期結構與回購均價事實表未涵蓋。","valuation":"五年年化 10% 扣掉 0.63% 殖利率，股價要到約 1,438 美元。Base 的 FY31 EPS 53.5 美元要配 26.9 倍，或者按 23 倍需要 EPS 62.5 美元，已接近 Bull。短期上檔以 FY28 Base EPS 41.0 美元乘 24 倍得 984 美元，+7.2%；中期以 FY29 的 45.3 美元乘 24 倍得 1,087 美元，+18.5%。PEG 用 FY27E 到 FY29E 共識年複合 11.4%，25.79 倍除以 11.4 得 2.27，屬偏貴。共識快照在財報前，FY1 與 FY2 都還沒反映這次上修。","premortem":"三項的證據與裁定寫在反證紀錄。十類衰退訊號只有一項亮燈：FY23–FY26 EPS 年複合比營收高 17 個百分點，代表過去的 EPS 主要靠利潤率。訴訟面只有一件私人壟斷案，10-K 稱訴訟不會有重大不利影響。歷史最大回撤與空方最強數字事實表未涵蓋，最大回撤改由情境樹推算。"},"plain":{"six":{"how_it_makes_money":"賺的是設備製造商與機隊營運商的維修替換錢，利潤卡在應用工程師把多項互連技術設計進設備、經銷網再把售後接走這一節。","moat":"護城河穩定（→）：執行面還在變強，但定價權只是穩定，也拿不出相對同業的方向證據，所以不判擴大。","growth":"成長跑道中等（🟡）：有機目標加併購足以撐五年，第五年以後仍要靠持續併購，第二條成長曲線還不夠格。","capital":"現金流品質好、稀釋很低，但回購報酬不夠，併購報酬還算不出來，資本配置整體中等。","valuation":"917.79 美元要賺到五年年化 10%，FY31 EPS 得到 62.5 美元，或終端倍數維持約 27 倍；這兩項我都不信，所以估值偏貴。","how_wrong":"最可能看錯的是利潤率有多少是結構性的，其次是濾材集團的資本報酬，再來是 25 倍左右的本益比能否維持。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 800 美元以下（約 FY27 指引中點 21.7 倍），Base 年化回報才回到約 9–10%；或 FY28 初始指引中點不低於 43 美元且股價不高於 945 美元。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":917.79,"week26_return_pct":4.64,"consensus_rev_3m_pct":1.66,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母不是翻案點：調整後 24.9 倍與 GAAP 30.5 倍都不便宜。要留意共識 35.59 美元是財報前快照；GAAP 與調整後中點差 6.80 美元，對帳細項事實表未涵蓋；FY26 GAAP 含 8,400 萬美元關稅退款，約每股 0.5 美元。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"CIRCOR 商用與國防航空業務預計完成收購","impact":"中","watch":"交割後槓桿是否接近 3 倍。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 Q2 財報，公司指引營收近 62 億美元、調整後 EPS 8.82 美元、部門利潤率 27.6%","impact":"高","watch":"單季有機成長是否約 10%，濾材集團稀釋幅度。"},{"date":"2027-05-13","date_precision":null,"type":"guidance","event":"2027 投資人會議，公司將說明未來五年規劃","impact":"高","watch":"新的長期目標與下一階段併購規模。"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27 全年財報與 FY28 初始指引","impact":"高","watch":"EPS 指引中點是否達 43 美元，部門利潤率指引是否低於 27.5%。"}],"_projected_from":"v19"}
```
