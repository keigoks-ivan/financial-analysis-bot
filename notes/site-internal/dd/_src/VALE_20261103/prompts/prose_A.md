你是 stock-analyst v20 的**散文層（prose）agent**，標的 VALE（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：VALE　日期：2026-11-03　archetype：None　前份裁決：2026-05-25　衛星候選 / 高股息 deep value 觀察｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1617B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（411B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（983B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1126B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1196B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（542B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（880B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2131B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1315B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3118B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1617           3768-5383      5 條（2–6 內）  
s3                  8000         411           5312-7589      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3305          8186-11695      5 條（2–6 內）  
s6                 11000         542          7321-10458      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         880           1834-2620      5 條（2–6 內）  
s10                 5000        2131           2008-2869      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3118           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4519B；至少需散文≈40.48KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−200
−60
−60%
−47%
−40
−40%
−34.1%
−30.3%
−30%
−15.1
−15%
−9.4
−9%
−8.8%
−8%
−5.4%
−2%
−2.0%
−1%
−0.2%
0.17
0.23
0.25
0.29
0.40
0.47
0.55
0.62
0.75
0.8
0.82
0.85
0.91
0.95
01
1%
1
1.07
1.10
1.1
1.16
1.19
1.2
1.3
1.30
1.35
1.483
1.50
1.5
1.60
1.6
1.65
1.75
1.8
1.80
1.88
1.9
1.95
02
2
2%
2.09
2.1
2.2%
2.25
2.3%
2.4
2.8%
03
3
3%
3.05
3.35
3.45
3.6
4%
4.0%
04
4
4.1%
4.4
5
5%
05
5.45
5.5
5.72
06
6
6%
6.04
6.05
6.1
6.11
6.5
6.56
6.6
6.8
7%
7
7.4%
7.5%
7.5
7.6
8
8%
9
9%
9.3%
9.75
9.9
10
10%
10.40
11%
11
11.01
11.48
11.56
12
12%
12.5
14
14.35
15%
15
16
16%
16.48
17
18
18.9%
19.2
20
20%
21%
21
22
23.1
23.5
23.6%
24
25%
25
25.4%
26
27
27%
28%
28
28.7
28.71%
29.17%
29.54%
30%
30
30.3%
31%
31
34
34.5
34.82%
35%
35
35.04%
35.8%
36
38
38.8
40
40%
42%
42.56
44
45%
45
45.19%
47%
48
49
50%
50
51%
52
53%
54
55
55%
56
57
58
60%
60
60.4
61%
62%
62
63
65
66
67%
70%
70
71.8
72%
74
75%
75
78
80
80%
85
85.1
90
100
104
106
137.0
150
160
164
172
180
191.9
200
250
285
490
500
800
900
1985
2011
2013
2015
2016
2022
2023
2024
2025
2026
2027
2028
2029
2030
2035
20261103
15,314
16,898
2,352
2,795
2,919
41,090
41,167
5,000
6,166
7,245
7,983
8,000
8,630
8,840
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
{"meta":{"ticker":"VALE","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Vale S.A."},"oneliner":"Vale 現價 11.48 美元，看似 6.6 倍本益比、9% 殖利率，但第三季盈餘低於預期、Simandou 新供給才開始進場、共識還在下修；長抱不碰，等實現價止穩、共識止跌再重看","thesis":{"H":[{"id":"H1","text":"鐵礦全成本守得住：all-in 成本（未含避險）維持在 2026 指引 58–62 美元/噸內，2027 年指引不高於 62 美元，C1 不高於 23.5 美元","2y":"2027 年 all-in 季值都 ≤62 美元/噸、C1 ≤23.5 美元/噸","5y":null,"10y":null,"threshold":"all-in ≤62 美元/噸（3Q26 為 60.4）；C1 ≤23.5 美元/噸（3Q26 為 23.1）","source":"Vale 季報 6-K、Vale Day 指引","drift_rule":"以 60 美元為基準：連 2 季高 5% 以上（>63）削弱，連 3 季高 10% 以上（>66）反轉"},{"id":"H2","text":"銅成為第二引擎：銅產量由 2026 年 36–38 萬噸走到 2030 年約 50 萬噸，基本金屬占 EBITDA 維持 30% 以上","2y":null,"5y":"2030 年銅產量 ≥45 萬噸；基本金屬占 EBITDA ≥30%","10y":null,"threshold":"年度銅產量逐年成長；基本金屬 EBITDA 占比 ≥30%（3Q26 為 31%）","source":"Vale 季度產銷報告、Vale Day","drift_rule":"銅產量落後目標路徑連 4 季 ≥5% 削弱，連 6 季 ≥10% 反轉"},{"id":"H3","text":"資產負債表撐住配息：擴大淨負債守在 100–200 億美元目標區間，普通配息不靠舉債維持","2y":"2027 年兩次普通配息合計每股 ≥0.8 美元（9 月一次 17 億美元約每股 0.40）","5y":null,"10y":null,"threshold":"擴大淨負債 ≤200 億美元（3Q26 為 164 億）","source":"Vale 季報 6-K、配息公告","drift_rule":"以 164 億為基準：連 2 季高 5% 以上（>172 億）削弱，連 3 季高 10% 以上（>180 億）反轉"}],"R":[{"id":"R1","text":"鐵礦供給過剩：Simandou 爬坡、澳洲巴西增產、中國鋼需下滑，把實現價壓到 all-in 成本加 15 美元以下","h_ref":"H1,H3","clock":"🔥","threshold":"鐵礦粉實現價季均 <75 美元/噸、連 2 季（3Q26 為 85.1）","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#4","end_markets#1","end_markets#2","reg_tariff_export#2"]},{"id":"R2","text":"巴西營運與許可：Serra Norte 洞穴限制與老礦耗竭、Fábrica 與 Viga 停工、ANM 罰單、Carajás 單線鐵路，加上印尼鎳配額","h_ref":"H1","clock":"⚡","threshold":"季度鐵礦產量 <8,000 萬噸（3Q26 為 8,840 萬噸），或全年低於指引下緣 3.35 億噸","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","regulatory_antitrust#3","major_events#3","geo_supply_chain#0","cyclical_inventory_price_position#1"]},{"id":"R3","text":"品質溢價與議價權流失：中國集中採購、低品位直接還原技術、對中國營收占 51% 與關稅貿易壁壘","h_ref":"H1,H2","clock":"🐢","threshold":"all-in 溢價 <2 美元/噸連 4 季（3Q26 約 4.4），或中國對 Vale 實施採購限制","evidence_refs":["customer_second_source#0","reg_tariff_export#0","reg_tariff_export#1","substitute_technology#0","substitute_technology#3","geo_supply_chain#2"]},{"id":"R4","text":"法律與合規成本：Brumadinho 證券集體訴訟、Itabira 市約 55 億美元求償、Southern Bahia 公民訴訟、歐盟航運碳費","h_ref":"H3","clock":"🔥","threshold":"單一年度新增撥備或和解 >10 億美元，或新尾礦壩事故","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0"]}],"single_thing":{"description":"鐵礦粉實現價季均跌破 75 美元/噸（3Q26 為 85.1）","why_fatal":"鐵礦粉與球團占淨銷售約 72%；以第三季粉礦銷量 8,630 萬噸年化約 3.45 億噸，每噸少 10 美元約少 34.5 億美元稅前利潤，接近 FY1 共識淨利約 74 億美元（1.75×42.56 億股）的一半（稅前對稅後，實際衝擊較小）；跌到 75 美元時與 all-in 60.4 美元只剩約 15 美元空間，股息必降","if_happens":"盈餘走 2015 年那種下修路徑（當年調整後 EBITDA 年減 47%）；長抱不碰，持有則清倉，循環交易只在高成本供給退出、港口庫存回落後才評估","how_monitor":"Vale 季報實現價、MB61 等參考價月均、Simandou 月出貨、中國 35 港庫存（SMM 週報）","probability":"35–45%（12–24 個月）：Simandou 2027 年出貨預估 40–50 Mt、中國鋼需 2027 年再降 1%；反方是約 1.6 億噸虧損產能退出會在 75–85 美元之間托底"}},"appendix_a":{"growth_durability":4,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":6.11,"peg_fy2":0.82,"stress":{"pass":5,"total":8},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-11-03）"},"eps_meta":{"base_eps_path":{"FY2025A":0.55,"FY2026E":1.75,"FY2027E":1.88,"FY2028E":null},"fy_end_month":12,"eps_basis":"基期為 GAAP 稀釋 EPS（含非經常損失）；FY2026E 與 FY2027E 為 yfinance 共識平均；FY2028E 事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"鐵礦價格接受者：營收主由鐵礦報價驅動、盈餘隨價格與雷亞爾匯率擺動，近四年毛利率由 45% 降到 35%；銅鎳占 EBITDA 約三成，屬另一個長期部門"},"industry":{"clock_phase":"IV","sd_verdict_source":"worldsteel 2026-10 展望、UBS 2026-01、S&P Global 2026-06 Simandou 出貨估計、SMM 2026-10-16 港口庫存、Vale 3Q26 法說（10-30）","bargaining":{"up":"上游：柴油、船租與巴西人力；約 75% 運量為固定費率長約、2027 年已鎖逾 80%，燃油 2027 年 67% 避險在每桶 78 美元（10-30 法說）","down":"下游：中國鋼廠為主，CMRG 集中採購並稱定價機制不合理，已先與 Rio Tinto 達成協議；十大客戶占鐵礦營收 35.8%，無單一客戶超過 10%","geo":"地理：對中國營收占 51%（20-F FY2025）；北部系統靠 Carajás 到港口約 900 公里單線鐵路"},"profit_pool_dir":"鐵礦利潤池往鋼廠與新進高品位供給移，對 Vale 不利；銅利潤池在擴大，Vale 銅產量計畫 2035 年倍增","tam_table":{"expanded":false,"reason":"成熟大宗商品，不是低滲透、新品類或份額擴張題材；需求用中國與印度鋼產量追蹤，已寫進產業時鐘與供需判斷"}},"moat":{"mechanism":"成本曲線位置加礦石品位：C1 現金成本低、Carajás 與球團有品位溢價；弱點是巴西到中國的運距","execution":6,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"定價力縮減的三個一手證據：IOCJ 低於組合 5% 並改賣中品位、Simandou 與 Carajás 正面競爭（10-30 法說）、CMRG 集中採購並先與 Rio Tinto 達成協議；成本面維持：C1 23.1 美元，運費與燃油避險擋住現貨上漲","peer_na_reason":"同業 RIO、BHP、FMG.AX 的季度損益在事實表全為空值，無法算利潤率或報酬率差距","threats":[{"level":"🟡","text":"Simandou 高品位礦與 Carajás 正面競爭，滿產 1.2 億噸約占海運近 7%（方向已記在護城河趨勢，這裡不重複扣分）","p":"60%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"中國 CMRG 集中採購、稱定價機制不合理，議價權往買方移（已記在趨勢，不重複扣分）","p":"40%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"低品位礦用於直接還原的新製程，削弱高品位溢價（20-F 自述風險）","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#3"]},{"level":"🟡","text":"LFP 已占全球電動車電池逾 55%，壓縮鎳的電池需求，印尼供給成長壓價","p":"50%","evidence_refs":["substitute_technology#1","substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉：近四季營業利益率 28.71%，投入資本周轉率事實表未涵蓋（礦業重資產）；要查的是資產更新負擔，Serra Norte 自 1985 年開採、正在耗竭，得靠 Serra Leste、N3、Capanema 補量","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是鋼廠，鋼是必需品，需求真實；但最大市場中國鋼需 2026 年 −2%、2027 年 −1%，印度 2026 年 +7.4% 只能部分補上"},{"item":"決策層級","level":"🔴","text":"替代發生在每家鋼廠的配礦比例，Vale 粉礦與 Simandou、Pilbara 礦按使用價值互換；與 CMRG 無長約或固定價（CFO 說法），管理層也說多推高品位不一定換得到溢價"},{"item":"價值鏈分配","level":"🔴","text":"CMRG 公開稱礦商與鋼廠價值分配失衡並要處理；中國鋼廠內需疲弱、靠出口約 1.3 億噸鋼撐產量，利潤池往鋼廠回流的壓力大"},{"item":"社會容忍度","level":"🟡","text":"巴西端：洞穴保護限制 Serra Norte 開採、Fábrica 與 Viga 曾遭停工、ANM 罰單；中國端：買方以「不公平」為由壓價，形成政治價格天花板；兩者已反映在目前的量與價上，未見升級"}],"roiic":"事實表未涵蓋：投入資本與折舊攤銷未收；專案層級參考 Bacaba 報酬率由約 50% 升到近 70%（7-31 法說 Usmar），不能代表全公司","reinvest_rate":"事實表未涵蓋：只有 2026 資本支出指引 54–57 億美元與 3Q26 的 12.5 億，折舊與營業資金變動未收","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率，再投資率＝（資本支出－折舊攤銷＋營業資金變動＋收購淨額）÷稅後營業利益；兩項輸入都缺，天花板留空，情境樹不用它放寬機率"},"combined":5.5,"score":5.5,"spread_table":[{"metric":"毛利率","VALE":34.82,"RIO":null,"BHP":null,"FMG.AX":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","VALE":28.71,"RIO":null,"BHP":null,"FMG.AX":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","VALE":8.62,"RIO":null,"BHP":null,"FMG.AX":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","VALE":1.76,"RIO":null,"BHP":null,"FMG.AX":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"RIO","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"Simandou 的開發者之一，Pilbara 之外多一個高品位來源，且已先與 CMRG 達成協議，中國談判籌碼比 Vale 強"},{"name":"BHP","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"WAIO 中期目標每年超過 3.05 億噸、持續擴產；2026 年 3 月曾被中國限制採購，顯示中國集中採購對三大礦商一視同仁"},{"name":"FMG.AX","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"CMRG 正在與其談判（10-30 法說）；利潤率資料事實表未收，無法比較成本位置"}]},"growth":{"driver_mix":"量為主、價被動：鐵礦 2026 年指引 3.35–3.45 億噸、2030 年目標 3.6 億噸，年增不到 2%；銅 2026 年 36–38 萬噸到 2030 年約 50 萬噸、2035 年約 70 萬噸；併購只有小額（Ligga 30%、Minas-Rio 15%）；回購計畫 1 億股約占 2.3%，執行量未知","runway_years":"鐵礦不適用滲透率概念（中國需求已過高峰）；銅成長段到 2035 年約 9 年","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板＝增量報酬×再投資率；事實表沒有投入資本、折舊攤銷與營業資金變動，兩項都算不出，天花板留空。替代參考：Bacaba 專案報酬率約 70%（7-31 法說 Usmar），但那是單一專案，不代表全公司新增資本的報酬","segments":[{"item":"鐵礦粉","value":"占 3Q26 淨銷售 61%；實現價 85.1 美元/噸、年減 10%；鐵礦產量 8,840 萬噸、年減 6%"},{"item":"球團","value":"占 11%；2Q26 實現價 137.0 美元/噸、年增 2.2%；2026 產量指引 30–34 Mt"},{"item":"銅鎳等基本金屬","value":"占 27%；3Q26 EBITDA 11 億美元、年增逾 60%、占全公司 31%；銅實現價 15,314 美元/噸、鎳 16,898 美元/噸；銅產量年減 6%，年初至今增 4%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；年度 2022 到 2025 由 45.19% 降到 35.04%"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"海運市占事實表未涵蓋；第三季產量年減 6%、銷量持平"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"價格接受者，不適用"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"共識 FY1 到 FY2：EPS +7.4%、營收約 −0.2%，差 7.6 個百分點"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":false,"evidence":"2023 年 0.91、2024 年 0.47、2025 年 1.19，只有一年低於"},{"signal":"股權酬勞占營收 >5% 且上升","lit":false,"evidence":"礦業股權酬勞低，金額事實表未涵蓋"},{"signal":"市場萎縮或被替代技術壓縮","lit":true,"evidence":"中國鋼需 2026 −2%、2027 −1%；LFP 逾 55% 壓縮鎳；低品位直接還原製程"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"Vale 自身 P/S、EV/S 在四個年度端點最低，但同業倍數事實表未收，無法確認是產業性下移"},{"signal":"維持性資本支出占 FCF >60%","lit":null,"evidence":"維持性資本支出事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"仍在投資 Capanema、S11D +20、Salobo、Bacaba"}],"trap_rating":"價值陷阱風險中等（亮 2 項），長期成長性中等"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：Ligga 增資約 1.9 億美元，不到約 490 億美元市值的 1%；Minas-Rio 15% 金額事實表未涵蓋；Thompson 是轉出"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"併購規模小（Ligga 30% 增資約 1.9 億美元、Minas-Rio 15%），已實現報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"計畫 1 億股、18 個月（約 2.3% 流通股，7-31 法說）；執行量與均價事實表未涵蓋；以現價與 FY1 共識算的盈餘殖利率約 15%，10 年期殖利率事實表未收","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"股權酬勞金額事實表未涵蓋；目前股數 42.56 億股","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY1、FY2 共識）加股息殖利率；商品循環股原本優先看股價淨值比，事實表沒有帳面價值","tier":"全球海運鐵礦三大之一，與 Rio Tinto、BHP 同一層","peers":{"expanded":false,"reason":"同業 RIO、BHP、FMG.AX 在事實表的損益與倍數全為空值，無法做同一層對照"},"fwd_pe":6.56,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 共識 6.6 倍、FY2 6.1 倍、殖利率 9.3%，表面偏便宜；但以第三季 EPS 0.29 年化約 1.16，本益比約 9.9 倍，落在礦商的中段；分母正是爭點，便宜論證不計，給中性。五年分位：只有四個年度端點，算不出。短期：Base FY2027E EPS 1.30×7.5 倍（盈餘低點給略高倍數）＝9.75，約 −15%；中期：Base FY2031E EPS 1.60×6.5 倍＝10.40，約 −9%，兩者都未含每年約 7.5% 的股息","upside_short_pct":-15.1,"upside_mid_pct":-9.4},"trap_analysis":{"verdict":"🟡","label":"高股息低倍數，但盈餘下行未止、共識仍在下修"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"S&P 估 Simandou 2026 年 15–20 Mt、2027 年 40–50 Mt、2028 年約 70 Mt；BHP WAIO 中期超過 3.05 億噸；UBS 預期澳巴產量每年增約 3%、中國鋼需 3–5 年每年降約 1%；上一輪鐵礦現貨 2011–2015 由約 191.9 跌到 38.8 美元，Vale 2015 年調整後 EBITDA 年減 47%、4Q15 EBITDA 利潤率 23.6%；SMM 港口庫存在累積","assumption":"高成本產能（管理層說約 1.6 億噸虧損）會在 75–85 美元之間退出托底","consequence":"若退出慢於新增，實現價落到 65–70 美元，粉礦每噸空間剩 5–10 美元，EPS 回到 1 美元以下、股息砍半、股價再跌 40–60%","ruling":"採納：這是 Bear 機率 30% 的來源，也是現在不建倉的主因","watch":"鐵礦粉季實現價、Simandou 月出貨、中國港口庫存","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","supply_demand_durability#0","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_inventory_price_position#0"],"fact_refs":["f_kpi6_realized_fines_price","f_kpi7_c1_cash_cost"]},{"view":"論點失敗","evidence":"Carajás 到港口為單線約 900 公里鐵路（第三方說法）；2026-01 Fábrica 與 Viga 因水溢流停工（合計年產約 800 萬噸）；Serra Norte 洞穴限制與老礦耗竭，第三季鐵礦產量年減 6%；Oman 球團廠因中東衝突延後","assumption":"Serra Norte 2027 年持平、2028 年靠 Serra Leste 與 N3 回補","consequence":"單一中斷事件讓季產量跌破 8,000 萬噸，固定成本攤提惡化","ruling":"部分採納：2022 年鐵路停運時靠庫存未影響指引，單次中斷可吸收；耗竭是慢性問題，已放進 Base 量假設","watch":"季產量、Serra Norte 日均產量","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","major_events#3","regulatory_antitrust#2"],"fact_refs":["f_kpi10"]},{"view":"論點成功但股東經濟變差","evidence":"Brumadinho 相關美國證券集體訴訟、Itabira 市求償約 55 億美元、Southern Bahia 公民訴訟無法估算；Fábrica 相關訴訟估計約 6.04 億美元（可能損失）與 ANM 罰單；歐盟 ETS 2026 年起全面適用航運；CMRG 稱定價機制不公、要調整礦商與鋼廠的價值分配；對中國營收占 51%","assumption":"銅成長與成本計畫成功、鐵礦量守住","consequence":"增加的現金被和解、罰款、碳費與對中國讓價吃掉，股息與回購沒跟著增加","ruling":"部分採納：訴訟金額多屬可能損失、時點未定，不放進 Base EPS；CMRG 讓價放進 Bear","watch":"季度撥備、CMRG 協議條款、訴訟進度","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0","regulatory_antitrust#1","customer_second_source#0","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":[]},{"view":"價格已反映太多","evidence":"便宜看的是 FY1 共識 1.75；第三季 EPS 0.29 低於預期、淨利年減 53%，Goldman 7 月降到中立；賣方均價目標 15–17 美元是 9 月以前的數字","assumption":"市場把 6 倍本益比與 9% 殖利率當地板","consequence":"共識一路下修時，每次下修都把地板往下移，低本益比不是保護；以年化 1.16 計，本益比約 9.9 倍","ruling":"採納：Bear 錨還沒穩定，正向不對稱的數字不能當進場依據","watch":"FY2027 共識三個月變化","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#3","end_markets#1"],"fact_refs":["f_kpi2_eps","f_consensus_eps_fy1","f_consensus_eps_fy2"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 16.48 → 本次 11.48（-30.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=16.48","side_b":"本次 price_at_dd=11.48","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 16.48 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 16.48 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 16.48 美元：Bull 價 19.2、Bear 價 6.05，五年期望值 −34.1%，基準年化 −8.8%，不對稱比 0.17","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.17。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 16.48 美元：五年期望值 −34.1%，基準年化 −8.8%，不對稱比 0.17","side_b":"本次情境、股價 11.48 美元：五年期望值 −5.4%，基準年化 −2.0%，不對稱比 0.95","ruling":"再換股價、情境不動：起點價下跌 30.3%，五年期望值多 28.7 個百分點，基準年化多 6.8 個百分點，不對稱比由 0.17 升到 0.95。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：股價下跌後的估值","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-05-25）：股價 16.48 美元，估值中性","side_b":"本次（2026-11-02）：股價 11.48 美元、跌 30%，倍數變低，但第三季 EPS 0.29 年化約 1.16，分母同步下修，估值仍中性","ruling":"估值結論不變：價格跌幅大致被盈餘下修抵銷","evidence_level":"事實表價格與季報數字","settle_metric":"4Q26 EPS 與 FY2027 共識 EPS","if_then":["若 FY2027 共識守在 1.80 以上且 4Q26 EPS ≥0.40：估值改判偏便宜","若 FY2027 共識跌破 1.50：估值改判偏貴，維持不碰"],"evidence_refs":[]},{"axis":"前份漂移：投資評級與價值陷阱判斷","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：評級 B，價值陷阱風險中等","side_b":"本次：評級 C，價值陷阱風險維持中等","ruling":"評級降一級的新證據：第三季 EPS 0.29 低於預期、淨利年減 53%、鐵礦產量年減 6%、粉礦實現價年減 10%；管理層估 Simandou 年化已約 5,000 萬噸，比年初預估快。陷阱判斷不變：衰退信號亮 2 項","evidence_level":"季報與法說一手、媒體轉述","settle_metric":"4Q26 產量與 EPS","if_then":["若 4Q26 與 1Q27 EPS 都回到 0.40 以上：評級回到 B 並重跑研究","若 1Q27 EPS 低於 0.25：衰退信號再亮一項，陷阱風險升為高"],"evidence_refs":["capital_markets_pricing#1","end_markets#1","cyclical_inventory_price_position#1","cyclical_supply_discipline_capacity#0"]},{"axis":"前份漂移：護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：未判護城河方向，風險寫的是 Carajás 溢價收斂","side_b":"本次：判縮減。10-30 法說 Rogério 承認 Simandou 與 Carajás 正面競爭、多推高品位礦不一定換得到溢價；高品位 IOCJ 已低於產品組合 5%、改以中品位為主；CMRG 先與 Rio Tinto 達成協議","ruling":"前份擔心的溢價收斂已有一手證據，定價力縮減、執行力穩定，合併判向下","evidence_level":"法說一手＋20-F 自述","settle_metric":"季報 all-in 溢價與產品組合","if_then":["若 all-in 溢價連 4 季回到 6 美元以上且 IOCJ 占比回升：方向改判持平","若 all-in 溢價跌破 2 美元：維持向下並把 Bear 機率升到 35%"],"evidence_refs":["competitive_share_entrants#2","customer_second_source#0","substitute_technology#0"]},{"axis":"前份漂移：方法補齊的欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","rearm_trigger","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄為空：沒有歸類、沒有循環位置、沒有五年後成長判斷、沒跑情境樹、沒有重新進場條件","side_b":"本次補齊：歸為循環／商品、循環位置中段、五年後成長空間中等、情境機率 20／50／30、最大回撤 −40%～−60%、重新進場須三條件同時成立","ruling":"屬方法補齊，不是看法翻轉；裁決與角色由程式依新欄位重算","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"唯一致命點（Single Thing）由空白改為鐵礦價格門檻","cause":"新證據","prior_field":["single_thing"],"side_a":"前份：未設唯一致命點（欄位為空）","side_b":"本次 Single Thing：鐵礦粉實現價季均跌破 75 美元/噸（3Q26 為 85.1）","ruling":"選價格門檻而不是尾礦壩事故：壩體事故致命但機率低，數學上最大的單一敏感度是鐵礦價格，每噸少 10 美元約少 34.5 億美元稅前利潤；Simandou 爬坡快於預期，讓這個門檻在 12–24 個月內有實際機率","evidence_level":"季報銷量推算＋第三方供給預估","settle_metric":"季實現價","if_then":["若連 2 季低於 75 美元：持有則清倉，長抱研究停止","若連 2 季高於 85 美元且港口庫存下降：Single Thing 機率降到 25%"],"evidence_refs":["supply_demand_durability#1","cyclical_supply_discipline_capacity#4"]},{"axis":"行動門檻變動（減碼／清倉）","cause":"新證據","prior_field":["kill_metrics","triggers"],"side_a":"前份門檻：Vale 鐵礦 EBITDA −30% → 立即減倉；新 dam 事件 → 立即評估清倉；中國鋼產連 2 年 −8% 且 Carajás 溢價連 4 季 <5 美元 → 風險觸發；2026 全年 Brumadinho 費用 >10 億美元；權利金或稅率 +5 個百分點","side_b":"本次門檻：鐵礦粉實現價季均 <75 美元 → 清倉；all-in 成本連 2 季 >63 美元 → 停止加碼、連 3 季 >66 → 減碼；季產量 <8,000 萬噸 → 減碼；淨負債 >200 億美元 → 減碼；集體訴訟不利和解 → 減碼一半；新尾礦壩事故或刑事追訴 → 清倉；權利金或稅率 +5 個百分點保留","ruling":"改用季報直接讀得到的價格、成本、產量。前份減倉門檻以第三季推估已觸發：pro forma EBITDA 35 億美元年減 20%、基本金屬 11 億年增逾 60%，倒推鐵礦及其他約 24 億，年減至少約 35%（含公司費用，屬推估）。中國鋼產 −8% 退休：worldsteel 預估中國 2026 −2%、2027 −1%，這個門檻在價格受損前不會觸發；Carajás 溢價改看公司揭露的 all-in 溢價，4.4 美元已低於前份的 5 美元，但前份要求兩條同時成立，另一條未達","evidence_level":"季報推算","settle_metric":"季報鐵礦分部 EBITDA","if_then":["若 4Q26 鐵礦分部 EBITDA 年減仍超過 30%：確認前份減碼門檻已觸發，維持不碰","若年減收斂到 15% 以內：前份門檻的觸發視為暫時"],"evidence_refs":["cyclical_inventory_price_position#1","end_markets#2"]},{"axis":"前份假設與風險改寫","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份假設：基本金屬 EBITDA 到 FY28 達 50 億美元以上；2026 年配息每股 1.2–1.3 美元；Brumadinho 費用 2027 年後降到每年 3 億美元以下。前份風險：中國鋼需與 Carajás 溢價、巴西權利金與大選、Brumadinho 與壩體","side_b":"本次假設：鐵礦 all-in 守在 62 美元內；銅 2030 年約 50 萬噸、基本金屬占 EBITDA ≥30%；淨負債守 200 億美元內並維持普通配息。本次風險：鐵礦過剩、巴西營運許可、溢價與議價權、法律合規","ruling":"配息假設改寫：CFO 10-30 說今年不太可能發特別股息，TTM 殖利率 9.3% 換算每股約 1.07 美元，前份 1.2–1.3 不成立；基本金屬方向保留，改看銅產量與占比（第三季 11 億、年化約 44 億，FY28 達 50 億仍可能）；Brumadinho 年度費用事實表未涵蓋，併入法律合規風險；巴西大選結果事實表未涵蓋，權利金門檻保留在觀察指標","evidence_level":"法說一手＋事實表","settle_metric":"2027 年 3 月配息、Vale Day","if_then":["若 2027 年 3 月普通配息每股 <0.40：資產負債表與配息假設判削弱","若 FY2026 基本金屬 EBITDA ≥40 億美元：銅引擎假設強化"],"evidence_refs":["major_events#0"]},{"axis":"便宜還是分母在掉","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：FY1 共識本益比 6.6 倍、10-24 快照 5.45 倍、TTM 殖利率 9.3%、P/S 與 EV/S 在四個年度端點最低、RSI 28、股價貼近 250 週均線 11.01、賣方均價目標 15–17 美元；2027 年運費逾 80% 已鎖、燃油 67% 避險在 78 美元、匯率避險 5.72，成本能見度高；基本金屬已占 EBITDA 31%","side_b":"第三季 EPS 0.29 比預期低約 28%，年化約 1.16，換算本益比約 9.9 倍；FY1 共識在 10-24 快照為 2.09、11-03 為 1.75，仍在下修；CFO 說今年不太可能發特別股息；Simandou 2027 年出貨預估 40–50 Mt、港口庫存在累積","ruling":"不可調和（方向相反），選 B 側：便宜論證靠的是還在下修的共識，跌了 30% 本身不是安全邊際；利空出現不到一季，賣方模型只部分反映（FY1 由 2.09 降到 1.75，FY2027 仍 1.88），所以不建倉、凍結任何加碼直到第一個確認數據點","evidence_level":"事實表＋法說逐字稿；共識兩個來源口徑不同","settle_metric":"4Q26 EPS（2027 年 2 月前後）與 Vale Day 2027 成本指引","if_then":["若 4Q26 EPS ≥0.40、FY2027 共識三個月不再下修、鐵礦粉實現價 ≥80 美元：重跑研究，通過才以 1% 試單分批反買","若 FY2027 共識跌破 1.50 或實現價跌破 75 美元：維持不碰，只追循環低點","若股價先漲回 104 週均線以上但上述數據未到：不追"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#3","end_markets#1"]},{"axis":"鐵礦市場平衡與否","cause":null,"prior_field":null,"side_a":"管理層（10-30，Rogério Nogueira）：海運供給持平、中國 9 月累計進口增 4.1%、港口庫存持平在 1.65 億噸、Simandou 年化約 5,000 萬噸仍被吸收；7-31 也說中國比國內指標顯示的平衡","side_b":"第三方：SMM 35 港庫存 1.483 億噸、月增 285 萬噸且預期續增；worldsteel 中國 2026 −2%、2027 −1%；UBS 預期澳巴產量每年增約 3%；Platts 消息稱 2027 起過剩加劇；日本、南韓鋼產 2025 年分別減 4.0%、2.8%","ruling":"不可調和，選 B 側：管理層自己的第三季實現價年減 10%、淨利年減 53%，與「平衡」說法不符；兩家庫存口徑不同（35 港與管理層全口徑），以方向為準","evidence_level":"第三方多為搜尋摘要轉述、未核原文；管理層為一手但有立場","settle_metric":"中國港口庫存月變化、鐵礦粉季實現價","if_then":["若 SMM 港口庫存連 2 個月下降且實現價回到 85 美元以上：Bear 機率由 30% 降到 25% 並重跑研究","若庫存續升破 1.6 億噸：維持不碰，Single Thing 機率上調到 45%"],"evidence_refs":["cyclical_inventory_price_position#0","supply_demand_durability#0","supply_demand_durability#2","reg_tariff_export#2","end_markets#2"]},{"axis":"管理層前一季承諾與本季兌現","cause":null,"prior_field":null,"side_a":"7-31 法說：Bacci 說年底擴大淨負債接近 150 億美元；Pimenta 說對達成所有產量指引有信心；Bacci 說股東回饋看下半年現金流，第三季末或第四季初決定","side_b":"10-30 法說：淨負債 164 億美元，只減約 2 億；鐵礦改說落在指引下緣；Bacci 說今年不太可能發特別股息、要保留現金壓低負債。正面兌現：Salobo 粗顆粒浮選比 7-31 說的 2029 年提前、2028 上半年投產；銅鎳成本優於原指引","ruling":"可調和（程度差異）：產量仍在指引內，但淨負債目標與股東回饋都往保守方向改口；鐵礦端可信度打折，基本金屬端加分","evidence_level":"兩季法說逐字稿","settle_metric":"4Q26 擴大淨負債與 2027 年 3 月配息","if_then":["若年底淨負債高於 160 億美元且 3 月普通配息每股低於 0.40：配息假設判削弱，維持不碰","若年底淨負債降到 150 億美元以下且公布回購執行量：配息假設判守住"],"evidence_refs":[]},{"axis":"Simandou 時程","cause":null,"prior_field":null,"side_a":"RBC（2025-12）：Vale 是 Simandou 延遲的明顯贏家，高品位溢價擴大；RBC 也認為 30 個月爬坡偏樂觀、要 48–60 個月","side_b":"S&P（2026-06）：爬坡快於預期，2026 年 15–20 Mt、2027 年 40–50 Mt；管理層 10-30 估年化已約 5,000 萬噸並承認與 Carajás 競爭","ruling":"不可調和，選 B 側：RBC 的前提（延遲）已過時，最新一手說法是爬坡已在進行","evidence_level":"第三方預估＋管理層一手","settle_metric":"Simandou 月出貨","if_then":["若 Simandou 2027 年實際出貨低於 30 Mt：Bull 機率由 20% 升到 25%","若 2027 年上半年年化已超過 60 Mt：Bear 機率升到 35%，維持不碰"],"evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#4","supply_demand_durability#1"]},{"axis":"基本金屬是長期成長還是價格紅利","cause":null,"prior_field":null,"side_a":"長期成長：Salobo 粗顆粒浮選核准（2028 上半年投產、年增約 3 萬噸銅）、Bacaba 提前、2030 年約 50 萬噸、2035 年約 70 萬噸；鑽探米數 2026 年逾 12 萬米","side_b":"本季 EBITDA 年增逾 60% 主要來自價格：銅產量年減 6%、年初至今僅增 4%；銅實現價 15,314 美元/噸屬高檔；鎳面對 LFP 已占電動車電池逾 55% 與印尼供給，印尼子公司 RKAB 配額初期只獲約 30%","ruling":"可調和：量的成長是真的但 2028 年後才明顯，現在的利潤增幅是價格；分兩套處理，銅的長期部分另計、不隨鐵礦循環賣出，但不足以撐起全公司估值","evidence_level":"法說一手＋第三方","settle_metric":"年度銅產量、基本金屬 EBITDA 占比","if_then":["若 2027 年銅產量年增 ≥8% 且銅價未跌：Bull 機率升到 25%","若銅價回落使基本金屬 EBITDA 占比低於 25%：維持 Base，不追"],"evidence_refs":["substitute_technology#1","substitute_technology#2","regulatory_antitrust#3"]},{"axis":"投資軌與交易軌：是不是循環低點","cause":null,"prior_field":null,"side_a":"像投降：RSI 28、26 週跌 25.4%、股價 11.48 貼近 250 週均線 11.01、P/S 與 EV/S 在四年端點最低、賣方目標高於現價、Goldman 降到中立","side_b":"六項循環訊號只有估值與情緒偏買；量價偏賣（價跌 10%、量持平）、供給紀律偏賣（Simandou、BHP 擴產，管理層只說約 500 萬噸可能調降）、庫存偏賣（港口累積）；毛利率在近四年低端但高於 2015 年谷底（4Q15 EBITDA 利潤率 23.6%）","ruling":"訊號矛盾，位置判中段、標位置不明而觀望；成長靠價格不靠量、TTM 本益比在四年端點最高（分母含非經常損失），兩道反動能限制都不放行","evidence_level":"事實表＋第三方","settle_metric":"主要礦商減產公告、港口庫存月變化","if_then":["若主要礦商宣布減產、港口庫存連 2 個月下降、股價仍在 250 週均線附近：重判為深谷，按循環規則分批反買，上限 3%","若股價先反彈站上 52 週均線 14.35 但供給與庫存沒變：不追"],"evidence_refs":["cyclical_inventory_price_position#0","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"]}],"triggers":[{"n":1,"text":"唯一致命點：鐵礦粉實現價季均跌破 75 美元/噸","type":"Single Thing","maps_to":"Single Thing","metric":"Vale 季報鐵礦粉實現價","threshold":"<75 美元/噸（3Q26 為 85.1）","action":"持有則清倉；長抱不再評估，改用循環低點規則","source_freq":"Vale 季報，每季","date":null,"evidence_refs":["supply_demand_durability#1","cyclical_supply_discipline_capacity#4"]},{"n":2,"text":"鐵礦全成本是否守住指引","type":"假設驗證","maps_to":"H1","metric":"鐵礦 all-in 成本（未含避險）與 C1","threshold":"all-in 連 2 季 >63 美元/噸或 C1 >23.5","action":"停止加碼；連 3 季 >66 美元則減碼","source_freq":"Vale 季報，每季","date":null},{"n":3,"text":"銅第二引擎是否按路徑成長","type":"假設驗證","maps_to":"H2","metric":"年度銅產量、基本金屬 EBITDA 占比","threshold":"2027 年銅產量低於 2026 年實際，或基本金屬占 EBITDA <25%","action":"把銅成長從 Bull 情境移出，Bull 機率降到 15%","source_freq":"Vale 季度產銷報告，每季","date":null},{"n":4,"text":"管理層把第三季 Serra Norte 減產歸因於車隊、降雨與高錳鋁礦段三個一次性因素：未證、監測","type":"假設驗證","maps_to":"R2","metric":"季度鐵礦產量年變化","threshold":"4Q26 與 1Q27 鐵礦產量仍年減 → 一次性歸因證偽","action":"下修 Base 量假設，維持不追","source_freq":"Vale 季度產銷報告，每季","date":"2027-04","evidence_refs":["cyclical_inventory_price_position#1"]},{"n":5,"text":"巴西營運中斷或許可停工","type":"風險","maps_to":"R2","metric":"季度鐵礦產量","threshold":"<8,000 萬噸，或全年低於指引下緣 3.35 億噸","action":"減碼","source_freq":"Vale 季度產銷報告、6-K 重大訊息","date":null,"evidence_refs":["regulatory_antitrust#2","major_events#3","geo_supply_chain#0","regulatory_antitrust#1"]},{"n":6,"text":"中國對 Vale 實施採購限制，或與 CMRG 的協議讓價","type":"風險","maps_to":"R3","metric":"CMRG 協議條款、中國對 Vale 礦的採購限制","threshold":"出現對 Vale 的採購限制，或協議讓價使 all-in 溢價 <2 美元/噸","action":"減碼；限制持續一季以上則清倉","source_freq":"公司公告與新聞，事件驅動","date":null,"evidence_refs":["customer_second_source#0","reg_tariff_export#0"]},{"n":7,"text":"訴訟與尾礦壩事件","type":"風險","maps_to":"R4","metric":"證券集體訴訟進度、新增撥備、壩體安全事件","threshold":"集體訴訟不利和解或判決，或單年撥備 >10 億美元 → 減碼一半；刑事追訴或新尾礦壩事故 → 清倉","action":"減碼一半或清倉","source_freq":"Vale 6-K／20-F 訴訟附註，事件驅動","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":8,"text":"資產負債表與配息","type":"減碼","maps_to":"H3","metric":"擴大淨負債、普通配息每股","threshold":"淨負債 >200 億美元，或 2027 年 3 月普通配息每股 <0.40","action":"減碼","source_freq":"Vale 季報與配息公告","date":"2027-03"},{"n":9,"text":"重新進場：分母止跌","type":"估值rearm","maps_to":"rearm","metric":"鐵礦粉實現價、FY2027 共識 EPS、週收盤對 104 週均線","threshold":"三條同時成立：實現價連 2 季 ≥80 美元、共識三個月不再下修、週收盤 >104 週均線（現 11.56）","action":"重跑研究；通過才以 1% 試單分批起步","source_freq":"季報、共識週更、週線","date":null},{"n":10,"text":"Vale Day 公布 2027 成本與產量指引","type":"複審日期","maps_to":"H1,H2","metric":"2027 all-in 成本指引、鐵礦產量指引","threshold":"all-in 指引上緣 >62 美元/噸則成本假設判削弱","action":"複審全部假設與機率","source_freq":"一次性","date":"2026-12"}],"kill_metrics":[{"metric":"鐵礦粉季實現價","bear_threshold":"<75 美元/噸","window":"任一季，連 2 季確認","source":"Vale 季報 6-K","last_status":"ok"},{"metric":"鐵礦 all-in 成本（未含避險）","bear_threshold":">66 美元/噸","window":"連 3 季","source":"Vale 季報 6-K","last_status":"ok"},{"metric":"季度鐵礦產量","bear_threshold":"<8,000 萬噸","window":"任一季","source":"Vale 季度產銷報告","last_status":"ok"},{"metric":"擴大淨負債","bear_threshold":">200 億美元","window":"任一季","source":"Vale 季報 6-K","last_status":"ok"},{"metric":"中國 35 港鐵礦庫存","bear_threshold":">1.6 億噸且連 3 個月上升","window":"月","source":"SMM 週報","last_status":"warning"},{"metric":"FY2027 共識 EPS","bear_threshold":"<1.50 美元","window":"三個月","source":"yfinance 分析師共識","last_status":"ok"},{"metric":"巴西礦業權利金或企業稅率","bear_threshold":"上調 5 個百分點以上落地","window":"任一時點","source":"巴西國會法案進度（前份門檻保留，資料缺口）","last_status":"unknown"},{"metric":"單一年度新增訴訟撥備或和解","bear_threshold":">10 億美元，或新尾礦壩事故","window":"年度","source":"Vale 6-K 或 20-F 訴訟附註","last_status":"unknown"}],"evidence_dismissed":[{"ref":"supply_demand_durability#4","reason":"這條是 2016 年 6 月的舊預測（摘要標為日期不明，原文日期 2016-06-21），講的是上一輪供給週期；2026 年的過剩判斷已由 UBS、S&P、Platts 與 worldsteel 的當期資料承擔，不能拿十年前的預測重複計分"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","pacing":[],"holding_cap":"長抱不持有；條件成立後上限 3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"三條同時成立才重跑研究：鐵礦粉實現價連 2 季 ≥80 美元、FY2027 共識 EPS 三個月不再下修、週收盤站回 104 週均線","exec_line":"現在不建倉、不追；三條同時成立後先重跑研究，通過才以 1% 試單分批起步；股價先漲但數據未到不追"},"reasoning":{"industry":"3Q26 營收約 106 億美元、年增約 2%；鐵礦粉占淨銷售 61%、球團 11%、銅鎳等 27%（媒體整理的季報數字）。pro forma EBITDA 35 億美元、年減 20%，其中基本金屬 11 億、占 31%（10-30 法說 Bacci）。粉礦實現價 85.1 美元/噸、C1 現金成本 23.1 美元、all-in 成本 60.4 美元（含運費），每噸空間約 25 美元。近四季毛利率 34.82%、營業利益率 28.71%。客戶：對中國營收占 51%（20-F FY2025），十大客戶占鐵礦營收 35.8%，無單一客戶超過 10%，單點依賴是中國這個市場，不是某一家客戶。產業時鐘在收縮期：中國鋼需 2026 年 −2%、2027 年 −1%（worldsteel 10 月），粉礦實現價年減 10%，Simandou 新供給正在進場。供需判斷：過剩偏結構性持久，Simandou 是長壽命低成本新供給、中國需求逐年降；唯一的反向力量是管理層估約 1.6 億噸虧損產能會退出，屬可逆的高成本供給，所以 Bear 給 30%。產業態勢三軸：競爭惡化（Simandou、BHP 擴產）、結構未轉好（中國鋼需降、印度增但體量不足）、其他結構變數（中國集中採購、歐盟航運碳費、低品位直接還原技術），裁決為競爭惡化中。","moat":"機制是成本曲線位置加礦石品位。成本端：C1 23.1 美元/噸仍在低端，但 all-in 一年上升 21% 到 60.4 美元；7-31 法說 Bacci 把 2026 all-in 指引由 52–56 上調到 58–62，約七成來自匯率與柴油；運費長約讓 2026 年比現貨省逾 30 億美元，屬合約期內的暫時保護。品位端：all-in 溢價 4.4 美元/噸與上季持平，粉礦溢價下降、靠球團撐住；高品位 IOCJ 已低於產品組合 5%，主力改成溢價 3–6 美元的中品位（10-30 法說 Rogério）；Rogério 也承認 Simandou 與 Carajás 正面競爭、多推高品位礦不一定換得到溢價。買方端：CMRG 集中採購、已先與 Rio Tinto 達成協議，Vale 仍在談。執行力給 6：Salobo 創第三季紀錄、Sudbury 精煉創 2013 年來新高、銅 all-in −200 美元/噸，但鐵礦產量年減 6%、Serra Norte 耗竭。定價力給 5：價格接受者，只剩小幅溢價。方向：執行穩定、定價力縮減，合併判向下。同業 RIO、BHP、FMG 的利潤率在事實表為空，報酬率差距無法算，方向證據改用溢價與產品組合這條可比軸。","growth":"成長來源是量，價格是被動的。共識 FY1 EPS 1.75 到 FY2 1.88 增 7.4%，同期共識營收 41,167 百萬到 41,090 百萬約持平（幣別標示待核），增幅全靠利潤率改善（成本計畫、運費避險），不是量。三年共識 EPS 年複合成長率算不出：FY2028E 事實表未收，且 FY2025 基期 EPS 0.55 含非經常損失（營業利益率 29.17% 到 29.54% 持平，淨利卻年減約 62%）。缺口歸因為利潤率擴張，這在鐵礦過剩期是最不可靠的一種。五年後：鐵礦在中國已過高峰，印度與東南亞在增但體量不足；銅有一手的產能計畫（Salobo 粗顆粒浮選 2028 上半年投產、年增約 3 萬噸；Alemão 2027 年 FID、2030 年投產），屬已啟動的第二條曲線，但撐不起全公司的寬跑道，所以給中等。","governance":"現金轉換：FCF／淨利 2023 年 0.91、2024 年 0.47、2025 年 1.19（年度財報，FCF＝營業現金流減資本支出；7,245÷7,983、2,919÷6,166、2,795÷2,352）。3Q26 FCF 22 億美元，含營業資金釋出與避險收益（Bacci），資本支出 12.5 億、全年朝 54–57 億指引下緣。擴大淨負債 164 億美元，在 100–200 億目標區間內，但 7-31 法說說年底接近 150 億，本季只減約 2 億。9 月付了 17 億美元股息與資本利息；CFO 10-30 說今年不太可能發特別股息、要多留現金。回購：7-31 開了 1 億股、18 個月計畫（約 2.3%），執行量與均價事實表未涵蓋；Bacci 同意股價便宜、回購有吸引力，但也說可能趁低價做併購。併購規模都小（Ligga 增資約 1.9 億美元、Thompson 轉出後保留 18.9%）。現金去向四分事實表未涵蓋。","valuation":"現價 11.48 美元。FY1 共識 1.75 算 6.6 倍、FY2 1.88 算 6.1 倍；10-24 快照用的 FY1 是 2.09（5.45 倍），兩個來源口徑可能不同，但方向一致指向下修（1.75 比 2.09 低約 16%）。TTM 本益比 71.8 倍是基期含非經常損失，不能用。P/S 0.23、EV/S 0.62 在四個年度端點最低，但只有四個點，不是五年分位。TTM 殖利率 9.3%，換算每股約 1.07 美元；CFO 說今年不太可能發特別股息。賣方均價目標 15–17 美元（9 月以前），高標 21、低標 11–12，高低比約 1.9 倍；方向與我相反，因為賣方模型還沒完全反映第三季的盈餘落差。商品循環股原本優先看股價淨值比，事實表沒有帳面價值，改用前瞻本益比加殖利率。結論：分母在下修，便宜論證暫不成立，估值給中性。","premortem":"我最大的假設是 2027–28 年海運鐵礦轉為明顯過剩。反方：管理層說海運供給持平、中國 9 月累計進口年增 4.1%、約 1.6 億噸虧損產能會退出；RBC 認為 Simandou 爬坡要 48–60 個月；2027 年運費與燃油大多已鎖價。股價 26 週跌 25.4%、RSI 28、站在 250 週均線 11.01 附近，若共識不再下修，市場會先重估。路徑風險：從 11.48 起算，Bear 終點約 −47%；上一輪鐵礦現貨跌約八成、Vale 2015 年調整後 EBITDA 年減 47%，所以最大回撤範圍給 −40%～−60%。陷阱判斷：衰退信號亮 2 項，價值陷阱風險中等，依據見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺中國鋼廠買鐵礦的錢，錢卡在「礦價減掉巴西運到中國的全成本」這一段：粉礦每噸約 25 美元空間，銅鎳是第二個錢包","moat":"護城河縮減、等級 C：成本位置還在，品質溢價與對中國的議價權在流失","growth":"五年後成長空間中等：鐵礦量平、中國需求下滑，第二條曲線是銅（2030 年約 50 萬噸），但銅鎳只占營收約四分之一","capital":"資本配置中等偏守：負債守在目標區間、以配息為主，回購執行未證，管理層還在看低價併購","valuation":"現價要求 2026–27 年 EPS 守在共識 1.75–1.88；以第三季年化約 1.16 看並不便宜，我不信共識守得住","how_wrong":"最可能看錯：鐵礦過剩來得比預期慢、銅價續強，6 倍本益比加 9% 殖利率被重估；看錯的代價是錯過約六到七成的 Bull 漲幅"}},"decision_inputs":{"signal":"C","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":"賣方 FY2027 EPS 1.88 與 15–17 美元目標價仍用偏高的鐵礦價格與成本假設；第三季 EPS 0.29 年化約 1.16，Simandou 2027 年出貨將由 15–20 Mt 增到 40–50 Mt","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等鐵礦粉實現價連 2 季 ≥80 美元且 FY2027 共識 EPS 三個月不再下修","trap":"🟡","val":"🟡","moat":"C","moat_trend":"↓","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":11.48,"week26_return_pct":-25.39,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"TTM 本益比 71.8 倍的分母含非經常損失；FY1 共識 1.75 高於第三季年化約 1.16，且 10-24 快照用的 FY1 為 2.09（不同來源），分母仍在下修，便宜論證暫不計"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"Alemão 銅專案環評公聽會（因大選延後到 11 月），之後取得 LP、2027 年 FID","impact":"中","watch":"公聽會是否再延、LP 時程"},{"date":"2026-12","date_precision":"month","type":"guidance","event":"Vale Day：2027 成本與產量指引、生產力計畫、銅成長與儲量更新","impact":"高","watch":"2027 all-in 指引上緣是否 ≤62 美元/噸；可能調降的約 500 萬噸鐵礦量"},{"date":"2027-Q1","date_precision":"quarter","type":"other","event":"4Q26 財報與 2027 年 3 月配息","impact":"高","watch":"4Q26 鐵礦產量是否年增（管理層承諾）；普通配息每股是否 ≥0.40"},{"date":null,"date_precision":null,"type":"other","event":"與 CMRG 的採購與定價協議","impact":"高","watch":"是否讓價、是否限制 Vale 礦採購"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"Bacaba 銅礦試車（較原定 2028 上半年提前）","impact":"低","watch":"是否如期"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"Simandou 2027 年出貨量（預估 40–50 Mt）","impact":"高","watch":"月出貨是否超過年化 60 Mt"}],"_projected_from":"v19"}
```
