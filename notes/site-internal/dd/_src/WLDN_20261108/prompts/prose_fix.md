你是 stock-analyst v20 的**散文層（prose）agent**，標的 WLDN（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：WLDN　日期：2026-11-08　archetype：None　前份裁決：2026-07-03　進場｜衛星持倉　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1883B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（403B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（809B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1161B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（916B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（500B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1148B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2331B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3596B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2693B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1883           3582-5117      5 條（2–6 內）  
s3                  8000         403           5318-7597      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2886          8480-12114      5 條（2–6 內）  
s6                 11000         500          7350-10500      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1148           1646-2352      3 條（2–6 內）  
s10                 5000        2331           1868-2669      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2693           2000-2307      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4050B；至少需散文≈40.95KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−45%
−43%
−40%
−40
−31%
−25.08
−13.2%
0
0%
0.14
0.15
0.2%
0.2
0.21
0.3
0.62
0.67
0.75
0.76
0.80
0.90
1
1.0
1.02
1.1
1.10
1.122
1.20
1.2
1.21
1.25
1.32%
1.32
1.34
1.40
1.4
1.45
1.46
1.5
1.5%
1.50
1.54
1.56
1.57
1.8
1.8%
02
2
2.0
2.145
2.3
2.3%
2.5
2.85
2.9
2.92
2.93
3%
3
03
3.1
3.2
3.32
3.4
3.41
3.49
3.7
3.8
4
4%
4.06
4.1
4.18
4.20
4.2
4.35
4.4
4.4%
4.40
4.53%
4.55
4.57%
4.65%
4.8
4.9
4.91
5%
05
5
5.0
5.03
5.07
5.1%
5.20
5.2%
5.4
5.40
5.42
5.5%
5.5
5.68%
5.75
5.8
5.87
6.0
6%
6
06
6.25
6.3
6.9%
07
7
7%
7.05%
7.1%
7.15
7.23
7.4%
7.6%
7.7
7.96
08
8
8.4
8.4%
8.65
8.83
9%
9
9.3
9.3%
9.4
9.5%
9.6
9.7%
10%
10
10.28
10.58
10.81%
10.9
11
11%
11.3
11.3%
11.4
11.73%
11.78
12%
12
12.22
12.3
12.8%
13
13.06
13.1
13.2%
13.5
13.5%
13.7%
13.7
14
14.2
15%
16%
16
16.07
16.3
17
17%
18%
19%
20%
20
22
22%
22.9
23%
23.2%
24
24%
24.3%
25%
25.2%
25.6%
26
27%
28%
29%
29.3
30
30%
30.5%
32
33
35%
37.5%
37.79%
38
38%
38.4%
40.2
41%
42
43
45.8
48
49
50
50%
50.7%
51.2
52
58%
63%
65%
66.22
66.5%
70%
70
73.7%
75.6
76.3
80.0%
80%
85
85%
90%
90
100
100%
104
112.67
121
150%
150
179
198
200
200.26
250
497
2024
2026
2027
2029
20261108
1,300
1,366
1,400
1,590
1,730
2,000
2,020
2,278
2,300
2,400
2,500
2,625
2,780
2,800
3,000
3,290
3,670
3,720
4,010
4,220
4,470
4,660
5,000
5,600
6,000
6,050
6,500
7,000
7,500
9,800
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
{"meta":{"ticker":"WLDN","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Willdan Group, Inc."},"oneliner":"能源顧問需求與併購把 EBITDA 推向 1.4 億美元，但稅率回正與舉債併購讓每股盈餘幾乎不動；現價約 12 倍 FY27 調整後盈餘，勝負在 2 月公布的現金流與有機成長。","thesis":{"H":[{"id":"H1","text":"成長不是只靠併購撐出來：FY27 有機淨營收維持低雙位數。","2y":"FY27 有機淨營收成長 ≥10%（Q3 FY26 為 12%，Energy 為 17%）","5y":"FY31 淨營收 ≥7.7 億美元（不含 FY27 後新併購）","10y":null,"threshold":"FY27 有機淨營收 ≥10%；FY31 淨營收 ≥7.7 億美元","source":"新聞稿與每季法說的有機成長揭露；2027 年 2 月法說首度拆分 FY27 有機與併購","drift_rule":"TTM 有機成長連 2 季低於 9.5% 為削弱，連 3 季低於 9% 為反轉"},{"id":"H2","text":"併購後 Adj EBITDA 利潤率站上 27% 以上，Mantis 的 35% 利潤率成立。","2y":"FY27 Adj EBITDA ≥1.40 億美元，占淨營收 ≥27%","5y":"FY31 Adj EBITDA 占淨營收 ≥28%","10y":null,"threshold":"FY27 Adj EBITDA ≥1.40 億美元且利潤率 ≥27%；FY31 利潤率 ≥28%","source":"2026-11-05 CFO 長期目標為高 20% 區間；FY26 指引中點 1.10 億／4.40 億美元為 25%","drift_rule":"自 Q2 FY27 起，TTM 利潤率連 2 季低於 25.6% 為削弱，連 3 季低於 24.3% 為反轉"},{"id":"H3","text":"現金跟得上 EBITDA：FCF 達 Adj EBITDA 七成，淨槓桿實際下降。","2y":"FY26 FCF ≥7,000 萬美元；FY27 FCF ≥9,800 萬美元；Q3 FY27 淨槓桿 ≤1.8 倍","5y":"FY31 FCF ≥1.5 億美元，累計 FCF 高於同期併購支出","10y":null,"threshold":"FCF／Adj EBITDA ≥70%；Q3 FY27 淨槓桿 ≤1.8 倍（公司目標低於 2.0 倍太鬆，以 1.4 億 EBITDA 計只需再少約 1,300 萬美元淨負債）","source":"新聞稿現金流量表與法說資本結構頁","drift_rule":"TTM FCF／Adj EBITDA 連 2 季低於 66.5% 為削弱，連 3 季低於 63% 為反轉（目前 65%）；前份門檻保留：TTM OCF／淨利連 2 季低於 1.0 為削弱"}],"R":[{"id":"R1","text":"9 月營運資金落差沒有在 Q4 回補，現金轉換承諾落空。","h_ref":"H3","clock":"⚡","threshold":"FY26 全年 FCF 低於 6,500 萬美元，即 Q4 低於約 3,720 萬美元","evidence_refs":[]},{"id":"R2","text":"資料中心許可與併網遭政治反彈，APG 與 Mantis 的資料中心客戶延案。","h_ref":"H1","clock":"🔥","threshold":"FY27 APG 低於 1.1 億美元（前份門檻保留，單季未揭露，標資料缺口），或管理層撤回管線看到 2029 年以後的說法","evidence_refs":[]},{"id":"R3","text":"電費負擔壓力讓能效與電網規劃預算被砍，主要公用事業客戶信用轉弱或流失。","h_ref":"H1","clock":"🔥","threshold":"公用事業能效資金連 2 季年增低於 5%（前份門檻保留，標資料缺口）；SCE 降至投機級；兩大客戶任一流失","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"id":"R4","text":"競標壓價，且多家得標合約不保證工作量。","h_ref":"H2","clock":"🔥","threshold":"單季 Adj EBITDA 占淨營收連 2 季低於 24%，或 NYPA 年工作量低於 5,000 萬美元","evidence_refs":["competitive_share_entrants#1"]},{"id":"R5","text":"併購過多或 Mantis 整合失敗，舉債收購的報酬低於資金成本。","h_ref":"H2、H3","clock":"🔥","threshold":"Mantis FY27 Adj EBITDA 低於 2,400 萬美元；FY27 全年 OCF／淨利低於 1.0，或 Burton 淨營收低於 3,000 萬美元（後兩項前份保留）","evidence_refs":[]},{"id":"R6","text":"人才與分包成本侵蝕利潤；Q3 薪資福利年增 24%，高於淨營收年增 18%。","h_ref":"H2","clock":"⚡","threshold":"薪資福利年增高於淨營收年增 ≥5 個百分點，且 Adj EBITDA 利潤率年減，連 2 季","evidence_refs":["geo_supply_chain#0"]},{"id":"R7","text":"FY27 稅率高於 22%，每股盈餘再被壓低。","h_ref":"H2","clock":"⚡","threshold":"2 月指引 FY27 有效稅率 ≥25%，每高 3 個百分點約少 0.21 美元 Adj EPS","evidence_refs":[]}],"single_thing":{"description":"2027 年 2 月正式指引或 FY27 實績把 Adj EBITDA 壓到 1.40 億美元以下。","why_fatal":"達標只需在備考約 1.32 億美元上成長約 6%；做不到代表核心業務沒有成長。槓桿 2.3 倍下，EBITDA 每少 10% 約少 0.67 美元 Adj EPS，是最大單一敏感項。","if_happens":"清倉，股價可能落到 Bear 路徑的 38 到 48 美元。","how_monitor":"2 月正式指引、每季 Adj EBITDA、有機成長與併購拆分、Mantis 貢獻。","probability":"約 15% 到 20%（12 到 24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":12.22,"peg_fy2":1.46,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":4.91,"FY2026E":5.07,"FY2027E":5.42,"FY2028E":null},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS。FY2025A 4.91 美元由逐字稿推算（前九個月 4.18 美元年增 25%，TTM 5.75 美元）；FY2026E 與 FY2027E 為 Koyfin 共識快照，未反映本次財報與 Mantis；FY2028E 共識事實表未涵蓋，留空。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"輕資產能源服務，靠重複客戶與併購擴張，EBITDA 成長快，但每股盈餘受稅率、利息與稀釋拖累"},"industry":{"clock_phase":"II","sd_verdict_source":"雙向拉鋸：競爭未見惡化（10-K 稱市場分散，Q3 NYPA 續標成功）；結構性轉好（負載成長，美國投資者所有公用事業 2026 年資本支出估 2,278 億美元，2024 年約 1,730 億，來源為招募業者部落格，品質偏低）；其他結構變數是電費負擔與資料中心許可的政治反彈。擴張期的依據是公用事業資本支出與新約，不是股價。","bargaining":{"up":"上游主要是工程人才與分包商；CEO 在 2026-08-06 稱人才市場偏緊、資深人員薪資上升。","down":"下游是受監管公用事業與政府，靠競標與預算決定；FY25 前十大客戶占 50.7%，兩大客戶占 23.2%。","geo":"過去集中在加州與紐約，納入併購後工作涵蓋 50 州，地域集中度下降。"},"profit_pool_dir":"利潤往電網規劃、能源採購與商業工業客戶移動，事實表未涵蓋量化的利潤池資料。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與分段利潤池，只有同業群營收份額約 0.2% 這個代理值，展開等於自行編造數字。"}},"moat":{"mechanism":"監管型能效專案與電網規劃的長年經驗，加上跨公用事業、政府、商業三類客戶的重複委託，換手要付出專案知識與重新採購的成本。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大（NYPA 續標、Con Ed 擴約、Adj EBITDA 利潤率上升）；定價權穩定（競標為主，毛利率變動主要來自組合）。兩者合併為穩定，同業 ROIC 差距事實表未涵蓋。","peer_na_reason":"事實表只有同業三項利潤率，未涵蓋同業 ROIC 與份額變化，無法計算報酬差距。","threats":[{"level":"🟡","text":"競標為主，輸標可能失去該市場多年，得標也可能壓價；NYPA 續標成功顯示目前守得住，但多家得標合約不保證工作量。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"自動化工具可能壓縮工程與顧問工時；目前只有社群文章的觀點，沒有數據，公司則把 AI 列為效率來源，先監測不扣分。","p":"30%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"大型全國工程公司可能切入能源專案與電網規劃；10-K 已提示，本包未見實際案例。","p":"20%","evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉（方向判斷；事實表未涵蓋投入資本，Mantis 入帳後周轉率會下降）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是電力用戶與建物業主，決策者是公用事業與政府，付款來自費率與預算；電網受限是必須解決的問題，超過 80% 工作來自重複客戶。資料中心那一段的急迫性高，持久性較難判斷。"},{"item":"決策層級","level":"🟡","text":"單一專案的替代性由競標決定，10-K 明示輸標會失去多年機會；NYPA 續標與 Con Ed 第 17 年說明現有客戶黏著，但事實表沒有續約率與漲價後流失率。"},{"item":"價值鏈分配","level":"🟡","text":"合約營收約一半轉手給分包與材料，公司留下淨營收；營益率 7.05% 低於 TTEK 的 11.73%，買方是受監管大型機構，議價力不弱。"},{"item":"社會容忍度","level":"🟡","text":"CEO 稱電費負擔已成客戶最重要的考量，部分地區電價年增超過 30%；這有利能效方案的論述，也會壓縮由費率支付的預算，資料中心許可的政治反彈已經出現。"}],"roiic":13.7,"reinvest_rate":50,"endo_ceiling":5.5,"formula_note":"FY25 到 FY27 指引 Adj EBITDA 增 6,050 萬美元，以 23% 稅率計稅後約 4,660 萬，除以 FY26 併購投入 3.41 億美元得 13.7%，其中含幾乎不用資本的有機成長；單看 Mantis 約 7.1%。再投資率 50% 是本次判斷，假設現金先還債再做小型併購。13.7%×50% 得 6.9%，資本配置未過關打八折後為 5.5%。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","WLDN":37.79,"TTEK":18.78,"ACM":5.68,"J":22.07,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","WLDN":7.05,"TTEK":11.73,"ACM":4.65,"J":4.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","WLDN":8.4,"TTEK":10.81,"ACM":1.32,"J":4.53,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"TTEK","gm":18.78,"om":11.73,"fcf_margin":10.81,"strategy_note":"營益率 11.73%、FCF 利潤率 10.81%，都高於 WLDN 的 7.05% 與 8.4%，是目前利潤結構的上限對照；事實表沒有業務重疊度。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ACM","gm":5.68,"om":4.65,"fcf_margin":1.32,"strategy_note":"營益率 4.65%、FCF 利潤率 1.32%，低於 WLDN；毛利率 5.68% 的成本口徑與 WLDN 不同，不能直接比。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"J","gm":22.07,"om":4.57,"fcf_margin":4.53,"strategy_note":"營益率 4.57%、FCF 利潤率 4.53%，低於 WLDN；屬於 10-K 提示可能跨入的大型工程公司類型。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"FY26 Q3 淨營收成長 18%，有機 12%、併購 6%；FY27 合約營收成長約 19%，併購約 12 個百分點以上，指引下限隱含有機約 6%。成長來自量與併購，回購沒有貢獻。","runway_years":"超過 10 年（份額代理值約 0.2%，TAM 事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"內生上界 5.5%（推導見護城河報酬持續期）。共識兩年年化 5.1% 未超過，Base 路徑 11.3% 超過，缺口可歸因於利息下降與利潤率擴張；情境已按超出處理，空頭機率 30%。","segments":[{"item":"Energy","value":"約占營收 85%，FY27 將超過 90%；Q3 有機淨營收成長 17%"},{"item":"Engineering","value":"約占營收 15%，FY27 降到 10% 左右"},{"item":"客群","value":"含併購全年化後，公用事業、州與地方政府、商業各約三分之一"},{"item":"資料中心（APG）","value":"FY26 約 7,500 萬美元，約占隱含合約營收 8.4 億的 9%；Q3 未更新數字"}],"decay_signals":["EPS 成長顯著高於營收成長：FY23 到 FY25 GAAP EPS 由 0.80 升到 3.49 美元，營收年增 11% 到 20%，已亮燈，且部分來自低稅率","毛利率連兩季年減：未亮燈，Q2 減 150 個基點、Q3 增 150 個基點","FCF／淨利低於 0.75 連兩年：未亮燈，FY25 為 1.34；FY26 前九個月 0.62 需看 Q4","SBC 占營收超過 5% 且上升：未亮燈，Q3 占合約營收 2.3%，但年增 58%","產業估值倍數系統性下移：事實表未涵蓋"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"FY26 併購現金支出","value":"約 3.41 億美元（前九個月 5,600 萬＋Mantis 2.85 億）"},{"item":"債務","value":"Mantis 完成後總債務 3.32 億美元、淨負債 2.93 億美元，淨槓桿約 2.3 倍，可動用流動性 1.54 億美元"},{"item":"回購與股利","value":"事實表未涵蓋，法說未提"},{"item":"優先序","value":"多數自由現金流還債，同時尋找小型併購"}],"sbc":{"note":"Q3 SBC 497 萬美元，年增 58%，占 GAAP 營業利益 30.5%、占淨營收 4.4%。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Mantis 以 2.85 億美元換約 2,625 萬 Adj EBITDA（7,500 萬×35%），約 10.9 倍；稅後約 2,020 萬，報酬約 7.1%，低於 9% 到 10% 的資金成本假設，且尚未實現。Burton 與 Compass 未揭露單獨獲利。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"法說未提回購，現金優先還債；事實表未涵蓋回購紀錄。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數由 FY23 約 1,366 萬（淨利÷稀釋 EPS）增到 FY26 指引 1,590 萬，年增約 5.2%，高於每年 1.5% 上限；部分來自股價上升造成的計算效果。","grade":"不過"}]},"valuation":{"basis":"FY27E 調整後 EPS，以約 22% 稅率計，輔以納入 Mantis 淨負債後的 EV／EBITDA 與 FCF 殖利率","tier":"小型能源服務與工程顧問","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業現值本益比或 EV／EBITDA；同業倍數承重但無資料，標為缺口，改用公司自身現值與情境推導。"},"fwd_pe":13.06,"peg":1.56,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY27 調整後本益比 12.3 倍與 FCF 殖利率 7.4% 到 9.3% 偏低，但分母受稅率影響，GAAP 本益比約 20 到 22 倍，且槓桿剛升到 2.3 倍，結論為合理。PEG 以 FY25 實績 4.91 到 FY28 Base 6.25 美元年化 8.4% 計算，第三年並非共識。五年分位留空，因事實表只有 3 到 4 個年度端點（本益比 0、P/S 43、EV/S 40.2），不是五年序列。","upside_short_pct":14.2,"upside_mid_pct":51.2},"trap_analysis":{"verdict":"🟡","label":"EBITDA 高成長掩蓋每股盈餘停滯，便宜感部分來自 0% 稅率"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"公用事業與政府客戶靠費率和預算付款，CEO 自己說電費負擔已是最重要的考量；FY25 兩大客戶占合約營收 23.2%，其中 SCE 所屬集團已被 S&P 降到 BBB-；資料中心許可出現政治反彈。","assumption":"能效與電網規劃預算不會因電費壓力被砍，資料中心案照進度走。","consequence":"五年虧 50%（約 33 美元）最可能的路徑是 FY27 跌破 1.4 億美元指引，有機成長轉負，FY31 EPS 約 4.1 美元、8 倍。","ruling":"部分採納。Bear 機率定 30%，FY27 EBITDA 列為唯一致命數字；反駁一次崩潰的說法，NYPA 10 年合約續標與 Con Ed 第 17 年顯示核心客戶仍穩。","watch":"2 月有機成長揭露、公用事業客群年增率、SCE 評等","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"],"fact_refs":["f_kpi7_fy2026"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 Adj EBITDA 年增 22%，Adj EPS 1.20 美元對 1.21 美元；GAAP EPS 0.76 對 0.90。指引隱含 Q4 Adj EPS 約 1.02 美元，去年同季 1.57 美元。FY26 全年 Adj EBITDA 增 38%，Adj EPS 僅增約 6%。稀釋股數 FY23 到 FY26 年增約 5.2%。","assumption":"EBITDA 成長會轉成每股成長。","consequence":"FY27 EBITDA 增逾 27%，Base Adj EPS 只增約 4%；若繼續以約 7% 報酬舉債併購，營收漂亮但每股價值不動。","ruling":"採納。Base 路徑按 22% 以上稅率、約 2,000 萬美元利息與持續稀釋建立，資本配置判定未過關。","watch":"FY27 Adj EPS 低於 5.0 美元，或年度稀釋股數增幅高於 3%","fact_refs":["f_kpi4_gaap_eps","f_kpi6_sbc","f_kpi7_fy2026"]},{"view":"價格已反映太多","evidence":"股價 26 週跌 25%，表面 13 倍，但分母用 0% 稅率；納入 Mantis 後 EV 約 13.1 億到 13.5 億美元，不是 10.58 億；FY27 GAAP 本益比估約 20 到 22 倍。","assumption":"市場會繼續用加回 SBC 與攤銷的調整後 EPS 定價。","consequence":"若市場改看 GAAP 或扣 SBC 後的 FCF，便宜感消失，倍數上修空間有限。","ruling":"採納一半。估值結論由偏便宜降為合理，Base 倍數 14 倍低於稅率還原後的 16 倍；但 FCF 若達標，扣 SBC 後殖利率仍約 7.4%。","watch":"FY27 扣 SBC 後 FCF 殖利率低於 6%","fact_refs":["f_fwd_pe_latest","f_pe_current","f_ev_m","f_net_debt_m"]}],"max_dd":{"lo":-55,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 76.3 → 本次 66.22（-13.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=76.3","side_b":"本次 price_at_dd=66.22","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟢→🟡、均線 🟡→🟠、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟢→🟡、均線 🟡→🟠、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 76.3 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 76.3 美元：Bull 價 198、Bear 價 52，五年期望值 +80.0%，基準年化 13.5%，不對稱比 6.0","side_b":"本次情境、股價仍用 76.3 美元：Bull 價 200.26、Bear 價 48，五年期望值 +50.7%，基準年化 9.7%，不對稱比 2.92","ruling":"先換情境、股價不動：五年期望值少 29.3 個百分點，基準年化少 3.8 個百分點。不對稱比由 6.0 變為 2.92。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 76.3 美元：五年期望值 +50.7%，基準年化 9.7%，不對稱比 2.92","side_b":"本次情境、股價 66.22 美元：五年期望值 +73.7%，基準年化 12.8%，不對稱比 4.9","ruling":"再換股價、情境不動：起點價下跌 13.2%，五年期望值多 22.9 個百分點，基準年化多 3.2 個百分點，不對稱比由 2.92 升到 4.9。合計五年期望值比前份少 6.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"FY27 成長是自己長的還是買來的","cause":null,"prior_field":null,"side_a":"2026-11-05 CEO：FY27 合約營收 10 億美元、年增約 19%，EBITDA 超過 1.4 億、增逾 25%，有機成長維持低雙位數。","side_b":"Mantis 全年化後，FY26 備考合約營收約 9.4 億、淨營收約 5.03 億、Adj EBITDA 約 1.32 億；指引對備考僅增 6%、接近零、增 6%，Burton 1 到 4 月尚未計入。","ruling":"可調和：指引應視為下限，不是低雙位數有機成長的預測。Base 取 FY27 Adj EBITDA 約 1.46 億，高於下限但低於備考加 11% 有機。","evidence_level":"法說原話與本次換算；Burton 備考未揭露","settle_metric":"2027 年 2 月法說的有機與併購拆分","if_then":["若正式指引 Adj EBITDA ≥1.45 億美元且有機成長 ≥10%，加碼第二筆","若正式指引仍停在 1.40 億且有機成長低於 7%，停止加碼並下修 Base FY27 EPS 約 0.3 美元"],"evidence_refs":[]},{"axis":"EBITDA 與每股盈餘背離","cause":null,"prior_field":null,"side_a":"2026-11-05 CFO：獲利成長快於營收，TTM Adj EBITDA 增 29%、Adj EPS 5.75 美元增 41%。","side_b":"Q3 Adj EPS 持平，GAAP EPS 減 16%；FY26 指引隱含 Q4 Adj EPS 年減約 35%。TTM 41% 含低稅率效果。","ruling":"可調和：差異來自稅率回正、利息與稀釋。估值以稅率還原後的每股盈餘為準，FY26 的 13 倍不作便宜依據。","evidence_level":"法說與新聞稿","settle_metric":"FY27 有效稅率與 Adj EPS 指引","if_then":["若 FY27 稅率指引 ≥25%，Base FY27 EPS 下修約 0.2 美元並停止加碼","若 FY27 稅率指引 ≤20%，Base FY27 EPS 上修約 0.15 美元"],"evidence_refs":[]},{"axis":"Mantis 淨營收由 1.2 億改為 7,500 萬美元","cause":null,"prior_field":null,"side_a":"2026-11-05 CEO：會計師重新檢視淨營收組成，Mantis 利潤率因此是 35%，對公司有增益。","side_b":"收購公告後兩個月內，同一項目的淨營收少了 37.5%；2.85 億美元買價約 10.9 倍 EBITDA，高於 WLDN 目前約 9.3 到 9.6 倍。","ruling":"未證、監測。淨營收改變不一定改變 EBITDA，但本包沒有獨立驗證。預登記：FY27 Mantis Adj EBITDA 低於 2,400 萬美元，即視為管理層說法證偽。","evidence_level":"管理層單方說明","settle_metric":"FY27 Mantis Adj EBITDA 與淨營收","if_then":["若 Mantis FY27 Adj EBITDA 低於 2,400 萬美元，減碼一半","若 Mantis 達 2,800 萬美元以上且交叉銷售有具體案例，併購報酬項目重新評估"],"evidence_refs":[]},{"axis":"現金轉換","cause":null,"prior_field":null,"side_a":"2026-11-05 CFO：9 月營運資金是暫時落差，Q4 回補；長期 FCF 超過 Adj EBITDA 七成，FY27 約 9,800 萬美元。","side_b":"前九個月營業現金流 3,290 萬，低於去年 4,010 萬；FCF／Adj EBITDA 前九個月 35%、TTM 65%，都低於七成承諾。","ruling":"未證、監測。FY26 達 7,000 萬美元需要 Q4 FCF 約 4,220 萬，去年同季約 3,670 萬；預登記 FY26 低於 6,500 萬即視為暫時落差的說法證偽。","evidence_level":"新聞稿現金流量表與法說","settle_metric":"FY26 全年 FCF","if_then":["若 FY26 FCF 低於 6,500 萬美元，減碼一半","若 FY26 FCF ≥7,000 萬美元且 FY27 指引過關，加碼第二筆"],"evidence_refs":[]},{"axis":"毛利率與稅率的說法前後對照","cause":null,"prior_field":null,"side_a":"2026-08-06 CFO：Q2 毛利率減 150 個基點，歸因組合轉向績效工程與商業專案；下半年稅率約 15% 到 20%。","side_b":"2026-11-05 CFO：Q3 毛利率增 150 個基點至 38.4%，歸因有利組合、激勵收入與 LADWP；Q3 稅率實際 23%。","ruling":"同一個組合說法解釋相反方向，毛利率不能當結構性改善，改看 Adj EBITDA 占淨營收。稅率已高於上季說法，Base 不採 FY26 的低稅率。","evidence_level":"兩季法說原話","settle_metric":"連續四季 Adj EBITDA 占淨營收與 FY27 稅率","if_then":["若 FY27 單季 Adj EBITDA 占淨營收連 2 季低於 24%，停止加碼","若連 4 季高於 27%，利潤率假設上修"],"evidence_refs":[]},{"axis":"資料中心曝險能否裁決","cause":null,"prior_field":null,"side_a":"2026-11-05 CEO：資料中心需求沒有動搖，管線看到 2029 年以後，併網通常在流程末端，不會擋住前期工作。","side_b":"分析師直接問 FY27 含多少資料中心、APG 是否再翻倍，CEO 沒有給數字；電池儲能占比也只是估計 5% 以下。","ruling":"不可裁決至 2027 年 2 月。APG 約 7,500 萬美元僅占合約營收約 9%，所以這不是最大敏感項，但 Mantis 的資料中心占比未揭露，曝險上限未知。","evidence_level":"法說問答，未量化","settle_metric":"FY27 APG 與 Mantis 的資料中心收入揭露","if_then":["若 FY27 APG 指引低於 1.1 億美元，停止加碼","若管理層撤回管線看到 2029 年以後的說法，減碼一半"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣：槓桿剛升到 2.3 倍，併購報酬約 7%，現金轉換落後承諾，每股盈餘不成長，股價仍在 52 與 104 週均線下方，2 月前沒有明確的向上催化。","side_b":"持有：淨營收有機成長 12%，核心續約成功，指引下限保守，FCF 若達標扣 SBC 後殖利率約 7.4%，Base IRR 約 12.8%。","ruling":"不賣但不追：首筆限半倉，因本週的新負面資訊尚未進入賣方模型，2 月前凍結加碼。","evidence_level":"綜合判斷","settle_metric":"2027 年 2 月 FY26 現金流與 FY27 正式指引","if_then":["若股價先漲到 85 美元以上而 2 月數據未到，不追","若股價跌破 52 美元且有機成長仍 ≥10%，分批反買","若 FY27 Adj EBITDA 指引低於 1.40 億美元，清倉"],"evidence_refs":[]},{"axis":"基本面結論相對前份下修","cause":"新證據","prior_field":["signal","val","trap","moat_trend"],"side_a":"前份（2026-07-03，股價 76.3 美元）：進場、評級 A、估值偏便宜、價值陷阱風險低、護城河擴大。","side_b":"本次：評級 B、估值合理、價值陷阱風險中等、護城河穩定；裁決與角色依本次輸入重算。","ruling":"股價跌了但結論下修，原因是 7 月後三項新事實：Mantis 把淨負債由 2,300 萬拉到 2.93 億美元；179D 到期後 Q3 稅率 23%；Adj EBITDA 成長沒有轉成每股成長。護城河由擴大改穩定，因為客群擴張主要靠併購，定價權與同業報酬差距沒有擴大的證據。","evidence_level":"公司法說與新聞稿","settle_metric":"FY26 現金流、FY27 稅率與有機成長","if_then":["若 FY26 FCF ≥7,000 萬美元且有機成長 ≥10%，估值結論可回到偏便宜並加碼第二筆","若 FY27 有機成長低於 7%，停止加碼並重評護城河方向"],"evidence_refs":[]},{"axis":"情境機率、跑道與公司分類","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭機率 30%、空頭 25%、最大回撤 −45%、五年後跑道寬，未標公司類型與循環位置。","side_b":"本次：多頭 20%、基準 50%、空頭 30%，最大回撤 −40% 到 −55%；跑道仍寬，類型為品質複利成長，不按循環股處理。","ruling":"Base 路徑高於內生成長上界，空頭機率拉到 30%；回撤改成區間，下緣反映 2.3 倍槓桿。跑道結論未變。","evidence_level":"本次情境推導","settle_metric":"FY27 有機成長與淨槓桿","if_then":["若 Q3 FY27 淨槓桿 ≤1.8 倍且有機成長 ≥10%，下次複審把空頭機率降回 25%","若淨槓桿 ≥2.0 倍，減碼一半"],"evidence_refs":[]},{"axis":"加碼條件新設","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設（null）","side_b":"FY26 FCF≥7,000 萬美元且 2 月指引 Adj EBITDA≥1.45 億美元；或股價<52 美元且有機成長≥10%","ruling":"前份沒有明確的加碼條件；本次把加碼綁在現金流與正式指引，股價下跌時也要有機成長過關才分批反買，避免機械式攤平。","evidence_level":"方法補強","settle_metric":"FY26 FCF 與 FY27 正式指引","if_then":["條件成立才加碼第二筆","條件未成立則停止加碼"],"evidence_refs":[]},{"axis":"減碼與清倉門檻新設","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（null）；前份風險門檻為 APG 連 2 季年增低於 50%、公用事業能效資金連 2 季年增低於 5%、FY27 OCF／淨利低於 1.0 或 Burton 淨營收低於 3,000 萬美元。","side_b":"FY27 Adj EBITDA 低於 1.40 億美元清倉；FY26 FCF 低於 6,500 萬美元減碼；Q3 FY27 淨槓桿 ≥2.0 倍減碼；有機成長連 2 季低於 9.5% 停止加碼。","ruling":"Mantis 舉債後最敏感的數字改為 EBITDA 與現金，因此新設清倉與減碼門檻。前份後兩條保留在風險欄，能效資金與 Burton 目前標資料缺口。APG 年增率門檻退休，因 FY26 基期已接近三倍，年增率失去鑑別力，改用 FY27 絕對金額 1.1 億美元。","evidence_level":"法說與前份紀錄","settle_metric":"各門檻對應的季度揭露","if_then":["任一清倉條件成立即清倉","減碼條件成立即減碼一半"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設（null）","side_b":"2027 年 2 月正式指引或 FY27 實績把 Adj EBITDA 壓到 1.40 億美元以下。","ruling":"Single Thing 選 EBITDA，因為它是數學上最大的敏感項：少 10% 約少 0.67 美元 Adj EPS，遠大於稅率與利率的影響。達標只需備考基礎上成長約 6%，若連這都做不到，代表核心業務沒有成長，應清倉。","evidence_level":"本次敏感度推導","settle_metric":"FY27 Adj EBITDA","if_then":["若低於 1.40 億美元，清倉","若高於 1.45 億美元，加碼第二筆"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY26 現金流與 FY27 正式指引同時過關，才加第二筆。","type":"加碼","maps_to":"H3","metric":"FY26 FCF 與 FY27 Adj EBITDA 指引","threshold":"FCF≥7,000 萬美元且 Adj EBITDA 指引≥1.45 億美元","action":"加碼第二筆","source_freq":"新聞稿與法說，每季","date":"2027-02"},{"n":2,"text":"FY27 Adj EBITDA 跌破指引下限。","type":"Single Thing","maps_to":"H2","metric":"FY27 Adj EBITDA","threshold":"低於 1.40 億美元","action":"清倉","source_freq":"新聞稿，每季","date":"2027-02"},{"n":3,"text":"Q4 營運資金沒有回補。","type":"減碼","maps_to":"R1","metric":"FY26 全年 FCF","threshold":"低於 6,500 萬美元","action":"減碼一半","source_freq":"新聞稿現金流量表，每季","date":"2027-02"},{"n":4,"text":"去槓桿沒有達標；公司目標門檻很鬆，未達代表現金流或併購紀律出問題。","type":"減碼","maps_to":"H3","metric":"季末淨槓桿","threshold":"Q3 FY27 季末 ≥2.0 倍","action":"減碼一半","source_freq":"法說資本結構頁，每季","date":"2027-11"},{"n":5,"text":"有機成長低於假設。","type":"假設驗證","maps_to":"H1","metric":"有機淨營收成長","threshold":"連 2 季低於 9.5%","action":"停止加碼","source_freq":"法說，每季","date":null},{"n":6,"text":"資料中心延案或管理層改口。","type":"風險","maps_to":"R2","metric":"FY27 APG 收入與資料中心管線說法","threshold":"FY27 APG 低於 1.1 億美元，或撤回管線看到 2029 年以後的說法","action":"減碼一半","source_freq":"法說，每季；單季 APG 目前未揭露","date":null},{"n":7,"text":"主要公用事業客戶信用轉弱或流失。","type":"風險","maps_to":"R3","metric":"SCE 信評與兩大客戶合約","threshold":"SCE 降至投機級，或兩大客戶任一流失","action":"停止加碼","source_freq":"信評公告與 10-K，事件驅動","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":8,"text":"競標壓價或人才分包成本侵蝕利潤。","type":"風險","maps_to":"R4、R6","metric":"Adj EBITDA 占淨營收；薪資福利年增減淨營收年增","threshold":"利潤率連 2 季低於 24%，或成本差距 ≥5 個百分點且利潤率年減連 2 季","action":"停止加碼","source_freq":"新聞稿與法說，每季","date":null,"evidence_refs":["competitive_share_entrants#1","geo_supply_chain#0"]},{"n":9,"text":"股價先跌而基本面未破時分批反買；股價先漲而數據未到時不追。","type":"估值rearm","maps_to":"H1","metric":"股價與有機成長","threshold":"低於 52 美元且有機成長 ≥10%；高於 85 美元且 2 月數據未到","action":"分批反買；不追","source_freq":"每日股價與每季法說","date":null},{"n":10,"text":"FY26 全年財報與 FY27 正式指引公布後重新研究。","type":"複審日期","maps_to":"H1、H2、H3","metric":"有機成長、稅率、FCF、Adj EBITDA 指引","threshold":"公布即複審","action":"重跑完整研究","source_freq":"2027 年 2 月下旬法說","date":"2027-02"}],"kill_metrics":[{"metric":"FY27 Adj EBITDA","bear_threshold":"低於 1.40 億美元即清倉","window":"2027-02 指引起至 FY27 實績","source":"公司新聞稿 8-K","last_status":"ok"},{"metric":"FY26 全年 FCF","bear_threshold":"低於 6,500 萬美元即減碼一半","window":"2027-02 公告","source":"新聞稿現金流量表","last_status":"warning"},{"metric":"季末淨槓桿","bear_threshold":"Q3 FY27 季末 ≥2.0 倍即減碼一半","window":"至 2027-11 公告","source":"法說資本結構頁","last_status":"ok"},{"metric":"有機淨營收成長","bear_threshold":"連 2 季低於 9.5% 即停止加碼","window":"FY27 逐季","source":"每季法說","last_status":"ok"},{"metric":"Adj EBITDA 占淨營收","bear_threshold":"單季連 2 季低於 24% 即停止加碼","window":"FY27 逐季","source":"新聞稿","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把資料中心政治風向當成全公司風險，但 APG 約 7,500 萬美元只占 FY26 隱含合約營收約 9%，主體是 NYPA、Con Ed 等公用事業與政府工作；FY27 指引下限也只要求備考基礎上成長約 6%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-25.08, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"FY26 FCF≥7,000 萬美元且 2 月指引 Adj EBITDA≥1.45 億美元；或股價<52 美元且有機成長≥10%","exec_line":"現價先建計畫部位一半，2 月法說前不加碼；FY26 現金流與 FY27 正式指引過關才加第二筆。"},"reasoning":{"industry":"Q3 合約營收 2.145 億美元，扣掉分包與材料轉手後的淨營收 1.122 億才是自己賺的；毛利率 38.4%，GAAP 營業利益占合約營收 7.6%，Adj EBITDA 占淨營收 25.2%。分部上 Energy 約 85%、Engineering 約 15%，FY27 Energy 會超過 90%。超過 80% 的工作來自重複客戶，NYPA 10 年多家得標合約（總額約 33 億美元）續標成功，Con Ed 合作進入第 17 年。單點依賴在付款來源：公用事業的能效預算最終由電費支付，FY25 兩大客戶占合約營收 23.2%；管理層稱納入 Mantis 後沒有客戶超過 10%。供需判斷為結構性持久：負載成長與老舊電網不是單一年度現象，但資料中心這一段的政治風險正在升高。","moat":"可證的方向是最大客戶關係：NYPA 續標成功，年工作量 5,000 萬到 6,000 萬美元；Con Ed 與 National Grid 合併成每年 2,500 萬美元的方案。反面是客群擴張主要靠併購，事實表沒有同業 ROIC，只有利潤率：WLDN 營益率 7.05%，低於 TTEK 的 11.73%，高於 ACM 與 J；毛利率 37.79% 與同業口徑不同，不能當優勢。Q2 毛利率下滑與 Q3 上升都歸因組合，定價權無法由此證明。Mantis 單筆稅後報酬約 7.1%，再投資品質低於整體增量報酬。投入資本事實表未涵蓋，當期 ROIC 只能判方向。","growth":"FY27 合約營收約 19% 的成長中，Mantis 增量約 12 個百分點，指引下限隱含的有機成長僅約 6%，低於管理層口頭的低雙位數。共識只有兩年：FY25 實績 4.91 美元（由逐字稿推算）到 FY27E 5.42 美元，年化 5.1%，且快照早於本次財報，第三年共識事實表未涵蓋。內生上界 5.5%；Base 路徑 FY26 到 FY31 年化 11.3%，超出 5.8 個百分點，主要來自債務還清省下利息（約 2.5 個百分點）、利潤率擴張與輕資本的有機成長，不靠回購與倍數。份額代理值僅約 0.2%，低於 35% 的寬跑道標準，但 TAM 未涵蓋。","governance":"FY25 FCF／淨利 1.34，FY26 前九個月 FCF 2,780 萬美元、對淨利 4,470 萬只有 0.62，對 Adj EBITDA 只有 35%，靠 Q4 回補。FY26 併購投入約 3.41 億美元，淨槓桿由 Q3 的 0.2 倍升到 2.3 倍。公司目標 Q3 FY27 淨槓桿低於 2.0 倍，以 1.4 億 EBITDA 計只需少約 1,300 萬美元淨負債，門檻很鬆，本次用 1.8 倍檢驗。SBC 單季 497 萬美元，占 GAAP 營業利益 30.5%。債務到期結構、新貸款利率與近三年現金去向事實表未涵蓋；以 Q3 利息推估利率約 6% 到 7%，FY27 利息約 2,000 萬美元。","valuation":"表面 Forward P/E 13.06 倍，但 FY26 指引假設 0% 稅率，用 22% 還原後約 16.3 倍。事實表的 EV 10.58 億美元仍用舊淨負債，納入 Mantis 後 EV 約 13.1 億到 13.5 億，對 FY27 Adj EBITDA 下限約 9.3 到 9.6 倍。FY27 Base EPS 5.40 美元對應 12.3 倍；若扣回 SBC 與攤銷，GAAP EPS 估約 3.1 到 3.4 美元，約 20 到 22 倍。管理層 FCF 約 9,800 萬美元的目標等於市值 9.3%，扣 SBC 後約 7.4%。12 個月目標 75.6 美元（5.40×14），三年約 100 美元。賣方 7 月底共識目標 112.67 美元早於本次財報，隱含倍數未計稅率回正；共識 EPS 三個月零修正也是快照未更新，不代表市場沒有反應。","premortem":"敏感度：FY27 Adj EBITDA 少 10%（1,400 萬美元）約少 0.67 美元 Adj EPS，是最大單一項；稅率高 3 個百分點少 0.21 美元；利率高 1 個百分點少約 0.14 美元。對 FY31 目標價（Base 121 美元）的衝擊：稅率高 3 個百分點約少 4.8 美元，FY28 起有機成長每年少 2 個百分點約少 9.4 美元，利潤率低 200 個基點約少 9.4 美元，終端倍數少 1 倍少 8.65 美元。價值陷阱風險中等，反證寫在反證紀錄。歷史最大回撤、債務條款與訴訟金額事實表未涵蓋；10-K 只列一般專業疏失索賠。"},"plain":{"six":{"how_it_makes_money":"賺公用事業、州與地方政府、商業客戶的能效與電網規劃服務費，錢卡在電網受限地區的規劃與方案設計這一節；併購已把三類客戶拉成各約三分之一。","moat":"護城河穩定、等級 B：優勢來自長年公用事業專案經驗與重複客戶，執行力在擴大，定價權沒有擴大的證據。","growth":"五年後跑道仍寬，但 FY27 帳面成長大半是併購，有機成長的下限要到 2027 年 2 月才看得清楚。","capital":"資本配置目前不及格：舉債併購的報酬尚未證明，股數每年增約 5%；還債是接下來一年的正確優先序。","valuation":"現價要求 FY27 調整後 EPS 約 5.4 美元、之後獲利年增約 10%，不需要倍數上修；我相信 EBITDA 兌現，對每股現金只信一半，所以估值算合理，不算便宜。","how_wrong":"最可能看錯的是把 EBITDA 成長當成每股價值成長；真正致命的是 FY27 Adj EBITDA 跌破 1.4 億美元。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把資料中心政治風向當成全公司風險，但 APG 約 7,500 萬美元只占 FY26 隱含合約營收約 9%，主體是 NYPA、Con Ed 等公用事業與政府工作；FY27 指引下限也只要求備考基礎上成長約 6%。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":66.22,"week26_return_pct":-25.08,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY26 調整後 EPS 5.20 美元建立在全年 0% 稅率上；179D 已於 2026 年 6 月底到期，Q3 稅率 23%。以 22% 粗估還原約 4.06 美元，對應 16.3 倍而非 13 倍，FY27 的稅率公司尚未揭露。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY26 財報與 FY27 正式指引，首度拆分有機與併購","impact":"高","watch":"FY26 FCF、FY27 Adj EBITDA、有機成長、稅率"},{"date":"2027-Q2","date_precision":"quarter","type":"guidance","event":"Q1 FY27 財報，現金流季節性偏弱的第一次檢驗","impact":"中","watch":"淨槓桿與 Mantis 整合進度"},{"date":"2027-Q4","date_precision":"quarter","type":"guidance","event":"Q3 FY27 財報，檢驗淨槓桿承諾","impact":"高","watch":"淨槓桿是否 ≤1.8 倍"},{"date":"2027-Q1","date_precision":"quarter","type":"other","event":"LADWP 太陽能路燈專案放量，CEO 稱 2027 年可能成為最大客戶","impact":"中","watch":"放量速度與客戶集中度"},{"date":null,"type":"regulatory","event":"各州資料中心許可與併網限制的政策進展","impact":"中","watch":"德州、俄亥俄州的政策與 APG 管線說法"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,389B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WLDN_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期</h2><p class="lead">護城河等級 B、方向持平，執行力強但定價權沒有證據。</p><ul class="pts">
<li>護城河來自長年的監管型能效專案與電網規劃經驗，加上三類客戶的重複委託。客戶換手要付出專案知識與重新採購的成本。執行力給 8 分，因為 NYPA 續標、Con Ed 擴約、利潤率上升都有證據。定價權給 6 分，因為競標為主，毛利率變動主要來自組合。</li>
<li>同業對照只能看利潤率。WLDN 營益率 7.05%，低於 TTEK 的 11.73%，高於 ACM 的 4.65% 與 J 的 4.57%。FCF 利潤率 8.4% 同樣低於 TTEK 的 10.81%。毛利率 37.79% 與同業成本口徑不同，不能當優勢。同業 ROIC 與份額變化事實表沒有涵蓋，無法計算報酬差距。</li>
<li>報酬持續期以 FY25 到 FY27 指引 Adj EBITDA 增加 6,050 萬美元估算，以 23% 稅率計稅後約 4,660 萬美元，除以 FY26 併購投入 3.41 億美元，得 ROIIC 13.7%。這個數字含幾乎不用資本的有機成長，單看 Mantis 只有約 7.1%。再投資率取 50%，因為假設現金先還債再做小型併購。</li>
<li>內生成長上界因此是 13.7% 乘 50% 得 6.9%，資本配置未過關打八折後為 5.5%。共識兩年年化 5.1% 沒有超過這個上界，但我們的 Base 路徑 FY26 到 FY31 年化 11.3%，超出 5.8 個百分點。缺口可歸因於還債省下的利息約 2.5 個百分點、利潤率擴張與輕資本的有機成長，所以空頭機率拉到 30%。</li>
<li>四個報酬持續期檢查點中，需求基礎值是綠燈，其餘三項是黃燈。需求來自電網受限這種必須解決的問題。決策層級由競標決定，沒有續約率與漲價後流失率。價值鏈上買方是受監管的大型機構，議價力不弱。社會容忍度則因電費負擔與資料中心許可而不確定。</li>
<li>護城河的三個威脅都是黃燈。競標壓價機率 30%，自動化壓縮工程工時機率 30%，大型全國工程公司切入機率 20%。自動化目前只有社群文章的觀點，沒有數據，公司反而把 AI 列為效率來源，先監測不扣分。大型工程公司 10-K 已提示，本次資料未見實際案例。</li>
</ul>
<h3>§5.F 對手財務深度對照</h3>
<!-- E5 -->
<!-- E6 -->
<h3>§5.R 報酬持續期檢核</h3>
<!-- E7 -->
</section>

```