你是 stock-analyst v20 的**散文層（prose）agent**，標的 ARM（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ARM　日期：2026-11-08　archetype：None　前份裁決：2026-07-30　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1814B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（996B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（997B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1423B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1024B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（751B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（731B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2227B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3975B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2432B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1814           3630-5186      5 條（2–6 內）  
s3                  8000         996           4903-7004      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3444          8089-11556      5 條（2–6 內）  
s6                 11000         751          7174-10249      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         731           1938-2769      5 條（2–6 內）  
s10                 5000        2227           1941-2773      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2432           2000-2568      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5452B；至少需散文≈39.55KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70
−70%
−66%
−45%
−45
−43%
−36.5%
−28%
−26.4%
−22.4%
−18.12
−18.12%
−8.2%
−5.4%
−5.3
−5.3%
−2.1
−0.4%
0
0.0%
0.14%
0.18
0.20
0.42
0.75
0.82
0.85
1
1.0
1%
01
1.05
1.10
1.2%
1.23
1.24
1.5
1.5%
1.64
1.7
2
02
2.09
2.13%
2.23
2.25
2.5
2.65
2.7
2.8
2.85
2.95
3
03
3%
3.06
3.09
3.3
3.5%
3.55
04
4
4.05
4.25
4.35
4.4
4.7
4.9
05
5%
5
5.2
06
6
6.1
6.10
6.20
6.4
6.65
6.70
07
7%
7
7.73
8%
08
8
8.31
8.5
8.5%
9%
9
9.08
9.37
10
10%
10.1
10.26
10.4%
10.64
10.8
11
11.4
11.5
12%
12
13%
13.6%
13.9%
14
14.43
14.5%
15%
15
16%
17
17.02%
18%
19.0
20
20%
21.2
22%
22.4%
24
25%
25
26
26.7
27%
28
28.19
29%
29
29.5%
30
30%
30.2
31
31.08
31.2
31.21
33%
34
34.8%
34.9
35%
35
36
37.2%
37.6%
38
39
40
40%
40.07
42
42%
43%
43
43.1
44.2%
45%
45
46%
48
49
49%
49.20
50%
52
54%
56
57%
57.07
57.1
57.28%
59%
60
60%
63%
63.7
64.0
66
66.6%
70
75
75%
76.3%
78
78.3
85.9%
88
89.9%
90
90%
$92
92
97%
97.44%
97.5%
99%
100
100%
104
$108
110
122
125
138
150
150%
155
160
171
174.4
174.62
200.71
209.64
213
224.89
245
272
288
367.2
393
428
500
520
2024
2025
2026
2027
2028
2030
20261108
1,000
2,000
2,200
2,600
5,000
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
{"meta":{"ticker":"ARM","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Arm Holdings plc"},"oneliner":"授權大增與 AGI CPU 上修都是真的，但權利金只年增 8%，比 7 月指引少 5 個百分點；股價跌到 174.62 美元後，基準五年報酬仍接近零，等約 110 美元再重做研究。","thesis":{"H":[{"id":"H1","text":"資料中心權利金繼續翻倍、手機費率往上，帶動全公司權利金在 FY2028 回到年增 20% 以上","2y":"FY2028 權利金年增 ≥20%","5y":"FY2032 權利金約 66 億美元，五年年增約 18%","10y":null,"threshold":"單季權利金年增：FQ4 FY27 ≥12%，FY2028 各季 ≥20%；資料中心權利金年增 ≥100%","source":"Arm 季度股東信與法說；第三方份額看 Mercury Research、TrendForce","drift_rule":"單季年增低於 20% 路徑 5 個百分點以上連 2 季算削弱，低於 10 個百分點以上連 3 季算反轉"},{"id":"H2","text":"AGI CPU 按時放量，授權客戶沒有因此大規模轉向","2y":"FY27＋FY28 累計營收 ≥15 億美元，首代毛利率 ≥30%","5y":"FY2032 矽業務約 75 億美元，毛利率約 45%","10y":null,"threshold":"累計營收 ≥15 億美元；活躍 ATA 不低於 60 家；前五大授權客戶沒有公開把資料中心 CPU 轉到 RISC-V","source":"Arm 季度法說、矽業務獨立列示後的財報、客戶公告","drift_rule":"累計營收展望低於路徑 5% 以上連 2 季算削弱，低於 10% 以上連 3 季算反轉"},{"id":"H3","text":"矽業務拉低毛利率之後，營業利益率還守得住，股份薪酬占比也降下來，才配得上 28 倍終端本益比","2y":"FY2028 非 GAAP 營業利益率 ≥42%","5y":"FY2032 非 GAAP 營業利益率 ≥40%，股份薪酬含雇主稅占營收 ≤20%","10y":null,"threshold":"非 GAAP 營業利益率 ≥40%；股份薪酬含雇主稅占營收逐年下降","source":"Arm 季度股東信的非 GAAP 調節表","drift_rule":"營業利益率低於路徑 5% 以上連 4 季算削弱，低於 10% 以上連 6 季算反轉"}],"R":[{"id":"R1","text":"權利金重新加速落空。2026-07-29 Jason Child 指引 Q2 年增 13%，實際 8%，FQ3 指引低個位數；半導體庫存修正也可能拖累。","h_ref":"H1","clock":"🔥","threshold":"FQ4 FY27 權利金年增 <12%，或 FY2028 前兩季平均 <15%","evidence_refs":["end_markets#4","supply_demand_durability#5"]},{"id":"R2","text":"反壟斷與 Qualcomm 訴訟打的是費率階梯本身。FTC 已在調查，Qualcomm 案預計 2026 年第四季開庭，受影響營收約 4.4 億美元；證券求償目前只到律所調查階段。","h_ref":"H1","clock":"🔥","threshold":"FTC 起訴、歐盟發出異議聲明，或法院限制 CSS 與授權條款，任一成立","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#1","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1","customer_concentration_credit#2"]},{"id":"R3","text":"矽業務成功反而壓低估值倍數。首代毛利率 30～40%，3 奈米產能靠台積電，公司也開始承擔供應鏈中斷風險。","h_ref":"H3","clock":"🔥","threshold":"合併毛利率單季 <90% 且非 GAAP 營業利益率 <40%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"自家晶片與授權客戶形成通路衝突，客戶可能縮減合作或保留路線圖資訊。","h_ref":"H2","clock":"🐢","threshold":"活躍 ATA 連 2 季下降，或前五大客戶公開縮減 Arm 路線圖合作","evidence_refs":["competitive_share_entrants#3","customer_second_source#1","channel_business_model_shift#1"]},{"id":"R5","text":"RISC-V、客戶自建核心與加速器分流，長期壓縮 CPU 權利金基礎。","h_ref":"H1","clock":"🐢","threshold":"RISC-V 進入任一大型雲端業者的主力伺服器 CPU，或旗艦手機 SoC 改用 RISC-V","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"id":"R6","text":"中國自給與出口管制。Arm China 占 FY2026 營收約 16%，Arm 不控制其營運，高階 Neoverse 許可難取得。","h_ref":"H1","clock":"🐢","threshold":"Arm China 占營收單年下降 4 個百分點以上，或出口管制擴及更低階核心","evidence_refs":["customer_second_source#2","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2"]},{"id":"R7","text":"對 SoftBank 與少數大客戶的依賴。SoftBank 持股約 90%，授權及設計服務每季約 2 億美元，S&P 展望負面；前五大客戶占 57%。","h_ref":"H3","clock":"🔥","threshold":"SoftBank 單季授權 <1.5 億美元，或評等降到 BB 以下，或公告減持 Arm","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","customer_concentration_credit#4"]}],"single_thing":{"description":"FY2028 全年權利金年增率低於 15%（2028 年 5 月前後公布）","why_fatal":"權利金毛利率最高，也是授權大增能否變現的驗證。本輪自估：五年權利金年增由 18% 降到 8%，FY2032 EPS 少約 1.7 美元（約 −28%），終端倍數也會由 28 倍往 20 倍掉，合計跌幅約 49%，大於矽業務落空的影響。","if_happens":"共識 FY2029 EPS 4.05 美元失去基礎，五年目標由約 171 美元降到約 88 美元。持有者清倉，未持有者取消重啟條件，直到權利金連 2 季回到 20% 以上。","how_monitor":"看每季股東信的權利金總額與三段增速，先看 FQ3 FY27，再看基期轉易後的 FQ4 FY27，後者應回到 12% 以上。","probability":"約 35%，12～24 個月，主觀估計。Q2 落後指引 5 個百分點、Q3 指引更低；但基期 2027 年初轉易，資料中心翻倍也提供支撐。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":57.07,"peg_fy2":1.64,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":0.85,"FY2027E":2.23,"FY2028E":3.06,"FY2029E":4.05},"fy_end_month":3,"eps_basis":"基期為 GAAP 稀釋 EPS，非 GAAP 全年基期事實表未涵蓋；共識三年為 Koyfin 非 GAAP。兩者口徑不同，成長率以 FY2027E→FY2029E 兩年複合 34.8% 為準。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ARM_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"97% 毛利的指令集授權，靠費率階梯和資料中心份額成長，正在加上 30～40% 毛利的自有晶片"},"industry":{"clock_phase":"III","sd_verdict_source":"WSTS 預估 2026 年全球半導體成長 89.9%，主要靠記憶體，屬過熱段；手機段卻因記憶體漲價而量縮。供需持久性：資料中心 CPU 需求結構性持久，供給可逆性中等，CFO 在 2026-07-29 說供應鏈要到日曆 2028～29 才放寬，之後定價順風可能反轉。","bargaining":{"up":"矽業務對台積電、記憶體、載板與測試機議價力弱，CEO 承認這是第一顆產品，規模不如 AMD。IP 業務沒有這個問題。","down":"前五大客戶占 57%，三家合計 42%；客戶無獨家與最低採購義務，但換架構成本高。","geo":"中國約占營收 18%，經由 Arm 不控制營運的 Arm China；高階 Neoverse 受美英出口管制。"},"profit_pool_dir":"機櫃裡的利潤往加速器與記憶體集中。Arm 用 AGI CPU 往下游多拿美元，但毛利率低得多。OI 池五年前後占比事實表未涵蓋。","tam_table":[{"item":"資料中心 CPU 晶片 TAM","value":"2026-03 Rene Haas 稱 2030 年約 1,000 億美元；2026-07-29 Jason Child 引最新估計 2,200 億美元；2026-11-04 Rene Haas 稱 2,000 億美元以上合理"},{"item":"AI 資料中心權利金 TAM","value":"2026-03 Rene Haas 稱當時約 30 億美元"},{"item":"伺服器 CPU 份額（第三方）","value":"Mercury 估 2026 Q2 出貨 13.6%；TrendForce 估 2026 年超過 20%，2027 年約 30%"},{"item":"頂級超大規模業者份額（管理層）","value":"2024 年 15%，2025 年 50% 以上，2026 年底預期超過 60%"},{"item":"PC 份額","value":"管理層稱占全球出貨 20%"},{"item":"手機份額","value":"約 99%（Morningstar）"},{"item":"RISC-V 滲透率","value":"SHD 估 2024 年 10.4%，市場 520 億美元，2030 年可能超過 2,600 億美元"},{"item":"OI 池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"指令集與軟體生態帶來的轉換成本，加上 v9／CSS 費率階梯","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力擴大：管理層稱頂級超大規模業者的 Arm 伺服器份額由 2024 年 15% 升到 2025 年 50% 以上，第三方數字較低但方向相同。定價力穩定：費率階梯仍在，但 v9 採用過半、順風轉弱，反壟斷調查限制 CSS 往上推的空間。兩者合併判穩定。","peer_na_reason":"同業 ROIC 差距事實表未涵蓋，只有毛利率、營益率、FCF 率與研發密度，改用份額方向當可比軸。","threats":[{"level":"🔴","text":"RISC-V 屬生態攻擊。免費開源，Arm 許多客戶同時是主要支持者，客戶沒有獨家或最低採購義務；SHD 估 2024 年滲透率 10.4%。","p":"30%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"客戶自建核心與 AI 加速器分流。Qualcomm Oryon 仍依賴 Arm 指令集；加速器若吃掉 CPU 工作負載，市場會變小，但目前 agentic 工作負載反而增加 CPU 需求。","p":"30%","evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"level":"🟡","text":"AGI CPU 與授權客戶直接競爭。20-F 已寫明客戶可能終止或縮減合作、改用替代架構；目前尚未看到實際流失。","p":"35%","evidence_refs":["competitive_share_entrants#3","customer_second_source#1","channel_business_model_shift#1"]},{"level":"🟡","text":"中國自給政策與出口管制限制高階 Neoverse 在中國的銷售，陸系客戶可能自研或改用對手技術。","p":"40%","evidence_refs":["customer_second_source#2","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（定性判斷，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都成立：本季夥伴出貨超過 100 億顆 Arm 晶片。資料中心受電力限制，每瓦效能是需要而不是想要；手機換機可以延後，所以邊緣 AI 權利金約零成長。"},{"item":"決策層級","level":"🟡","text":"決策單位是 SoC 設計案，換指令集成本高，但客戶無獨家與最低採購義務，Qualcomm 已證明高階核心可以自己做。實際續約率事實表未涵蓋，代理讀數是活躍 ATA 超過 60 家。"},{"item":"價值鏈分配","level":"🟡","text":"機櫃價值主要流向加速器與記憶體，2026-03 管理層估 AI 資料中心權利金 TAM 只有約 30 億美元，遠小於晶片 TAM，這也是 Arm 下場賣晶片的原因。矽業務上游由台積電與記憶體廠掌握，首代毛利率只有 30～40%。"},{"item":"社會容忍度","level":"🔴","text":"FTC 調查 Arm 授權行為是否企圖壟斷，前份另記歐盟與南韓也在查。Arm 同時賣晶片給授權客戶的對手，等於替投訴方加了論據，CSS 費率的實際上限可能低於經濟上限。尚無正式指控。"}],"roiic":"事實表未涵蓋投入資本，無法計算。替代讀數：FY2025→FY2026 GAAP 增量營業利益率約 8.5%（營業利益由約 8.31 億增至約 9.08 億美元，營收由 40.07 億增至 49.20 億美元）。","reinvest_rate":"事實表未涵蓋資本支出明細、折舊、營運資金變動與稅後營業利益，無法計算。研發密度 57.28% 是實質再投資，會計上走費用。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。投入資本缺資料，本輪不算上界，也不用替代讀數充當上界。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","ARM":97.44,"SNPS":72.38,"CDNS":85.68,"AVGO":68.77,"QCOM":53.1,"unit":"%"},{"metric":"營業利益率","ARM":17.02,"SNPS":11.03,"CDNS":29.64,"AVGO":48.52,"QCOM":20.08,"unit":"%"},{"metric":"FCF 利潤率","ARM":21.5,"SNPS":29.18,"CDNS":28.65,"AVGO":44.22,"QCOM":20.06,"unit":"%"},{"metric":"研發密度","ARM":57.28,"SNPS":30.6,"CDNS":33.3,"AVGO":13.28,"QCOM":23.67,"unit":"%"}],"competitors":[{"name":"SNPS","gm":72.38,"om":11.03,"fcf_margin":29.18,"rd_intensity":30.6,"strategy_note":"同屬設計工具與 IP，研發密度約為 Arm 的一半，顯示 Arm 目前的研發負擔偏重。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"CDNS","gm":85.68,"om":29.64,"fcf_margin":28.65,"rd_intensity":33.3,"strategy_note":"純 IP／軟體型的倍數上錨，Arm 的矽業務比重一升，就離這個參照越遠。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"strategy_note":"矽業務成熟後的參照，靠規模把營業利益率做高，是 Arm 混合毛利率下滑後的倍數下錨。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"QCOM","gm":53.1,"om":20.08,"fcf_margin":20.06,"rd_intensity":23.67,"strategy_note":"既是占 FY2026 營收 9% 的客戶，也是最直接的對手，自研 Oryon 核心繞開 Arm 的設計費，只留指令集關係。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（資料中心份額、矽業務出貨），價為輔（v9／CSS 費率），併購與回購接近零。","runway_years":"伺服器出貨份額約 1～2 年到 30%（TrendForce 估 2027 年約 30%），按短跑道給倍數；份額以外還有核心數增加與矽業務。","runway_post_y5":"🟢","endo_ceiling_basis":"本輪算不出內生上界，投入資本、折舊與營運資金變動事實表未涵蓋。共識兩年複合 34.8% 按超過上界處理。","segments":[{"item":"權利金","value":"6.70 億美元，年增 8%，占營收 46%；FQ3 指引季增低十幾%、年增低個位數"},{"item":"授權及其他","value":"7.73 億美元，年增 50%，占營收 54%；含 SoftBank 2.09 億美元；ACV 年增 12%"},{"item":"資料中心權利金","value":"年增翻倍，四大客戶為 Amazon、Google、Microsoft、NVIDIA；占權利金比重未揭露"},{"item":"實體 AI 權利金","value":"年增 50%"},{"item":"邊緣 AI 權利金","value":"約零成長，手機量縮被費率抵銷"},{"item":"AGI CPU","value":"尚無營收，FQ4 FY27 開始出貨；FY27＋FY28 最多 20 億美元；首代毛利率 30～40%"}],"decay_signals":["股份薪酬占營收偏高：含雇主稅 29.5%，逐年是否上升事實表未涵蓋，保守算亮燈","毛利率：TTM 97.44%，季度年比事實表未涵蓋，未亮；矽業務出貨後預期下滑","FCF／淨利：FY2025 為 0.20，FY2026 為 1.05，未連 2 年低於 0.75，未亮","EPS 與營收：FY2027→FY2028 共識 EPS 年增 37.2%，營收 37.6%，差距小於 5 個百分點，未亮","其餘六項（市占、提價後銷量、TAM、產業倍數、維護性資本支出、停止投資）：未見證據或事實表未涵蓋"],"trap_rating":"價值陷阱風險🟡（亮 1 項）；長期成長性🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，最大一筆 DreamBig 約市值 0.14%；近三年現金去向事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"唯一近期併購 DreamBig 於 2026-07-01 完成，約 2.65 億美元，約市值 0.14%，尚無已實現報酬資料。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購金額與均價事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"由 financial_history 淨利÷稀釋 EPS 自算，FY2023 到 FY2026 稀釋股數年增約 1.2%，低於 1.5%。","grade":"過"}]},"valuation":{"basis":"非 GAAP Forward P/E，以 FY2027E 為當前財年，FY2028E 為輔","tier":"高毛利 IP 型，正往半導體設計公司過渡","peers":[{"item":"CDNS Forward P/E","value":"34.9 倍，毛利率 85.9%（前份摘要 2026-07-30 讀數，本輪事實表未涵蓋新值）"},{"item":"AVGO Forward P/E","value":"19.0 倍，毛利率 76.3%（前份摘要 2026-07-30 讀數）"},{"item":"半導體中位 Forward P/E","value":"28.19 倍（前份摘要 2026-07-30 讀數）"},{"item":"ARM Forward P/E","value":"78.3 倍（2026-11-07 快照）"}],"fwd_pe":78.3,"peg":2.25,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2027E 78.3 倍除以 FY2027E→FY2029E EPS 年複合 34.8%，PEG 2.25；FY2028E 口徑 1.64。基準五年年化約 −0.4%，低於 8% 的弱門檻，所以維持偏貴。五年分位事實表未涵蓋，只有 4 個年度端點（本益比 26.7、P/S 64.0、EV／S 63.7），不當五年分位用。","upside_short_pct":-2.1,"upside_mid_pct":-5.3},"trap_analysis":{"verdict":"🟡","label":"亮燈一項：股份薪酬占營收 29.5%，矽業務上線後毛利率也將下滑"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FQ2 權利金年增 8%，FQ3 指引低個位數；手機約占營收 40～45%；RISC-V 和客戶自建持續推進。","assumption":"費率階梯還有空間，手機回穩後權利金回到 20% 以上。","consequence":"五年後虧 50% 最可能的路徑：權利金年增卡在 10% 以下，FY2029 共識落空，本益比由 78 倍壓到 20 倍，股價約 60 美元。","ruling":"採納。這條與 Single Thing 是同一件事，不另立門檻，機率放進空方 35%。","watch":"FQ4 FY27 起的單季權利金年增，以及 FY2028 全年數字。","evidence_refs":["end_markets#4","substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"],"fact_refs":["f_consensus_eps_fy3","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"FTC 調查 Arm 授權是否企圖壟斷，Bloomberg 報導後股價單日跌 8.5%。Qualcomm 案預計 2026 年第四季開庭，屬民事個案，Qualcomm 占 FY2026 營收 9%，約 4.4 億美元。原告律所僅宣布調查，未見已提起的集體訴訟。","assumption":"調查不會限制 CSS 定價，也不會強制中立授權。","consequence":"CSS 約 10% 的費率失去依據，費率階梯斷掉。社會容忍度本輪判紅，是經濟上限之外的第二個天花板。","ruling":"採納但不放進基準。FTC 尚未起訴，現有證據的時間窗蓋不到裁決日，風險未解，2026 年第四季開庭前不可裁決。","watch":"Qualcomm 案判決、FTC 起訴與否、歐盟異議聲明。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#1","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1","customer_concentration_credit#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"首代 AGI CPU 毛利率 30～40%；FY2031 目標 150 億美元矽業務會把混合毛利率由 97.5% 壓向 63%（前份論點）；公司已簽供應合約；Q2 非 GAAP 自由現金流只有 1.10 億美元。","assumption":"營業利益率守得住，市場不把公司改用半導體倍數。","consequence":"矽業務愈成功，倍數愈低。CDNS 34.9 倍到 AVGO 19.0 倍（2026-07-30）之間，代工與記憶體漲價也可能吃掉毛利。","ruling":"採納，基準終端 28 倍就是這個結果。","watch":"合併毛利率、非 GAAP 營業利益率、存貨與供應預付。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"],"fact_refs":["f_kpi1_non_gaap_operating_incom","f_kpi3_non_gaap_free_cash_flow"]},{"view":"論點成功但股東經濟變差","evidence":"股份薪酬加雇主稅 4.25 億美元，占非 GAAP 營業利益 66.6%。SoftBank 持股約 90%，S&P 在 2026-03 將其展望降為負面，授權及設計服務每季約 2 億美元；前五大客戶占 57%。","assumption":"股份薪酬占比隨規模下降，控股股東與小股東利益一致。","consequence":"非 GAAP EPS 高估股東實拿；SoftBank 若需要現金，減持賣壓與關聯方收入回落都會傷害小股東。","ruling":"部分採納。股份薪酬放進 H3 門檻；SoftBank 目前只是評等壓力，沒有減持證據，列為風險監測。","watch":"股份薪酬占營收、SoftBank 評等與持股變動、SoftBank 季度授權金額。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","customer_concentration_credit#4"],"fact_refs":["f_kpi4_sbc_non_gaap"]},{"view":"價格已反映太多","evidence":"FY2027E 本益比 78.3 倍，FY2028E 57.1 倍，前瞻 EV／S 30.2 倍。賣方平均目標價 213～272 美元都早於 11-04 財報。","assumption":"高點回落 59% 代表便宜。","consequence":"已跌多少不是安全邊際。現價要年化 10%，EPS 要年複合約 33%，基準只有約 22%。","ruling":"採納。價格是目前唯一卡住的條件。","watch":"FY2028 共識 EPS 本益比。","evidence_refs":[],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_ev_s_fwd","f_consensus_eps_fy2"]}],"max_dd":{"lo":-70,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 224.89 → 本次 174.62（-22.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=224.89","side_b":"本次 price_at_dd=174.62","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 224.89 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 224.89 美元：Bull 價 288、Bear 價 56，五年期望值 −36.5%，基準年化 −8.2%，不對稱比 0.18","side_b":"本次情境、股價仍用 224.89 美元：Bull 價 367.2、Bear 價 60，五年期望值 −26.4%，基準年化 −5.4%，不對稱比 0.42","ruling":"先換情境、股價不動：五年期望值多 10.1 個百分點，基準年化多 2.8 個百分點。不對稱比由 0.18 變為 0.42。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 224.89 美元：五年期望值 −26.4%，基準年化 −5.4%，不對稱比 0.42","side_b":"本次情境、股價 174.62 美元：五年期望值 −5.3%，基準年化 −0.4%，不對稱比 0.82","ruling":"再換股價、情境不動：起點價下跌 22.4%，五年期望值多 21.2 個百分點，基準年化多 4.9 個百分點，不對稱比由 0.42 升到 0.82。合計五年期望值比前份多 31.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"跌 22% 之後該不該買（現在就買的最強論證）","cause":"價格變動","prior_field":["signal","val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"現在就買的最強論證：股價由高點 428 美元跌到 174.62 美元，跌 59%；RSI 31；AGI CPU 能見度由 10 億美元以上提高到最多 20 億美元；授權年增 50%，12～24 個月後轉成權利金；手機基期 2027 年初轉易；FY2029E 本益比只剩 43 倍。","side_b":"現價要有年化 10%，在 30 倍終端本益比下，EPS 五年複合要約 33%。基準只有約 22%，五年目標約 171 美元，等於不賺。","ruling":"不買，卡住的只有價格。股價由 224.89 美元跌到 174.62 美元，只是從明顯過高回到仍偏貴，結論與偏貴判斷不變。機率維持多 17、中 48、空 35：AGI 上修與權利金落空方向相反，強度相抵。最大回撤區間隨股價下移。","evidence_level":"自算加一手法說","settle_metric":"FY2028 共識 EPS 本益比與 FQ4 FY27 權利金年增","if_then":["如果股價先漲過 52 週均線 209.64 美元而權利金年增仍低於 12%，不追。","如果股價跌到 110 美元以下且權利金年增沒有低於 8%，重跑研究後分批反買，上限 3%。","反向條件：FQ4 FY27 權利金年增 ≥20% 且矽業務確認達 20 億美元，重啟價位上調到 FY2028 共識 EPS 的 45 倍（約 138 美元），建倉上限 3%。"],"evidence_refs":[]},{"axis":"權利金落空與授權大增，護城河與跑道的判斷有沒有變","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"權利金年增 8%，FQ3 指引低個位數；ACV 年增 12%；v9 順風轉弱。","side_b":"資料中心權利金翻倍，主要客戶首次簽 ATA，AGI CPU 訂單延伸到日曆 2027 年，第三方份額持續上升。","ruling":"三項判斷都不改。權利金落空主要來自手機量縮，還沒有證據顯示份額或費率受損；基期轉易後若仍不回升，再下調。","evidence_level":"一手法說、20-F、第三方份額","settle_metric":"基期轉易後兩季的邊緣 AI 權利金年增","if_then":["如果 FQ4 FY27 與 FQ1 FY28 邊緣 AI 權利金連 2 季沒有轉正，護城河方向改為縮減，停止加碼。","反向條件：如果資料中心權利金連 2 季維持翻倍且總權利金年增 ≥20%，定價面改判擴大，重啟價位上調到 45 倍。"],"evidence_refs":["end_markets#4"]},{"axis":"公司類型沿用","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份歸為品質複利成長，未標循環位置。","side_b":"矽業務即將出貨，權利金也受手機週期影響。","ruling":"本輪方法沿用，歸類不變。截至 FQ2 FY27 矽業務營收仍為零，毛利率 97%。2026-07-29 Jason Child 承諾矽業務營收占比到 10% 時獨立列示，屆時改看半導體設計公司的倍數。","evidence_level":"一手法說","settle_metric":"矽業務占營收比重","if_then":["如果矽業務占營收達 10%，基準終端倍數上限由 28 倍降到 25 倍，不追。","反向條件：如果矽業務占比達 10% 而合併營業利益率仍 ≥45%，倍數維持 28 倍。"],"evidence_refs":[]},{"axis":"估值重啟門檻調整（重跑研究與建倉條件）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"FY+2 forward PE ≤ 35x（約 $108）→ 重跑完整 DD；≤ 30x（約 $92）Base 5Y IRR 才過 9%/yr。重啟後角色上限衛星 starter、倉位帽 3%","side_b":"FY2028 共識 EPS 本益比 ≤36 倍（約 110 美元，基準五年年化約 9%）→重跑完整研究；重啟後倉位上限 3%","ruling":"AGI CPU 能見度上修後，基準五年目標由約 155 美元升到約 171 美元，基準年化 9% 對應的價位由約 92 美元升到約 110 美元，兩段門檻併成一段。重跑研究與建倉上限 3% 不變。","evidence_level":"自算加一手法說","settle_metric":"FY2028 共識 EPS 本益比","if_then":["如果本益比 ≤36 倍，重跑完整研究，通過後分批反買。","反向條件：如果 FQ3 FY27 下修矽業務展望到 15 億美元以下，門檻降回 30 倍。"],"evidence_refs":[]},{"axis":"Single Thing 由空白改為 FY2028 權利金年增率","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空值。","side_b":"FY2028 全年權利金年增率低於 15%（2028 年 5 月前後公布）","ruling":"本輪依敏感度選定。權利金落空同時打擊 EPS 與終端倍數，影響大於矽業務落空，也大於單一訴訟事件。","evidence_level":"自算","settle_metric":"FY2028 全年權利金年增","if_then":["如果低於 15%，清倉；未持有者不建倉。","反向條件：如果 ≥20%，重啟價位上調到 45 倍。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空值。","side_b":"本次設六條門檻，含 FY2028 權利金低於 15% 清倉，FTC 起訴或歐盟異議聲明減碼。","ruling":"前份只有風險敘述，沒有結構化門檻；本次把前份合併毛利率跌破 90% 的條件保留下來，其餘新設。","evidence_level":"方法調整","settle_metric":"各門檻首次讀數","if_then":["如果任一清倉條件成立，清倉。","反向條件：如果兩季內所有門檻都未觸發且權利金年增 ≥20%，取消減碼預案。"],"evidence_refs":[]},{"axis":"權利金財測與實際","cause":"新證據","prior_field":null,"side_a":"2026-07-29 Jason Child：Q2 權利金年增 13%，全年接近高十幾%，FY2028、FY2029 的 20% 以上成長不變。","side_b":"2026-11-04 實際 Q2 年增 8%，FQ3 指引低個位數。Jason Child 未再重申 20%，只對手機相關業務說明年至少兩位數。","ruling":"採信實際數字，不採信路徑不變的說法。管理層把落空歸因記憶體漲價，這個歸因標未證，要用基期轉易後的數字檢驗。基準 FY2028 EPS 因此低於共識 7%。","evidence_level":"兩場法說逐字稿","settle_metric":"FQ4 FY27、FQ1 FY28 邊緣 AI 權利金年增","if_then":["如果基期轉易後連 2 季邊緣 AI 權利金沒有轉正，記憶體歸因證偽，基準 EPS 下修 10%，不追。","反向條件：如果 FQ4 FY27 總權利金年增 ≥20%，基準 FY2028 EPS 上調到共識 3.06 美元。"],"evidence_refs":["end_markets#4"]},{"axis":"三段權利金描述和總額對不上","cause":"新證據","prior_field":null,"side_a":"管理層描述：資料中心翻倍，實體 AI 年增 50%，邊緣 AI 約零成長；CFO 又說資料中心去年接近權利金的 20%。","side_b":"自算：權利金由約 6.20 億增至 6.70 億美元，只多約 5,000 萬美元。資料中心若占去年 20%，翻倍增量約 1.24 億美元，邊緣 AI 至少要衰退約 15%，不可能約零成長；若邊緣真的約零成長，資料中心去年不到權利金的 8%。","ruling":"不可裁決至 FQ3 FY27 財報。兩種讀法都偏空：要嘛資料中心比講的小，要嘛手機比講的差。裁決前採保守讀法，資料中心占權利金低於 15%，FY2028 翻倍也只貢獻約 15 個百分點。","evidence_level":"法說數字自算，公司未揭露絕對金額","settle_metric":"資料中心權利金絕對金額或占比","if_then":["如果揭露占比 ≥25%，代表邊緣 AI 實際明顯衰退，下修手機段假設，不追。","如果揭露占比 ≤15%，FY2028 基準權利金年增由 20% 下修到 16%，不追。","反向條件：如果占比 ≥25% 且 FQ4 FY27 邊緣 AI 年增轉正，FY2028 基準權利金年增上修到 25%。"],"evidence_refs":["end_markets#4"]},{"axis":"授權年增 50% 與 ACV 年增 12%","cause":"新證據","prior_field":null,"side_a":"2026-11-04 Rene Haas：授權年增 50% 是未來權利金的領先指標；授權比預期多約 1 億美元。","side_b":"同場 Jason Child：單季授權受時點與會計影響，ACV 才是底層趨勢；ACV 年增 12%，Q1 為 13%。","ruling":"看 ACV。授權大增有真實需求，但單季 50% 不能外推，基準授權 FY2032 只給約 39 億美元。","evidence_level":"一手法說","settle_metric":"ACV 年增","if_then":["如果 ACV 年增連 2 季 ≥15%，授權視為結構性上修，FY2028 基準 EPS 上調到 3.06 美元。","反向條件：如果 ACV 年增連 2 季 <8%，授權按時點性收入處理，不追。"],"evidence_refs":[]},{"axis":"AGI CPU 毛利率與營收措辭","cause":"新證據","prior_field":null,"side_a":"2026-07-29 Jason Child：首代毛利率高 30% 到低 40%；營收「超過 10 億美元」的信心上升。","side_b":"2026-11-04 Jason Child：先重複高 30% 到低 40%，接著說首代可能再低一點，建議用 30% 到 40%；營收改說「最多 20 億美元」。Rene Haas 同場說不擔心毛利。","ruling":"採 30～40%。金額上修是真的，但「最多」是上限不是下限，基準 FY27＋FY28 累計用約 15 億美元。","evidence_level":"兩場法說逐字稿","settle_metric":"FQ4 FY27 首次出貨毛利率；FQ3 FY27 更新的累計營收","if_then":["如果首代毛利率低於 30%，基準矽業務毛利率由 45% 下修到 40%，不追。","反向條件：如果首代毛利率 ≥40% 且累計確認 20 億美元，基準矽業務 FY2032 上修到 100 億美元。"],"evidence_refs":["geo_supply_chain#1"]},{"axis":"伺服器份額口徑","cause":"新證據","prior_field":null,"side_a":"管理層：頂級超大規模業者份額 2025 年 50% 以上，2026 年底超過 60%。","side_b":"Mercury：2026 Q2 出貨份額 13.6%；TrendForce：2026 年超過 20%；Mercury 也認為 AGI CPU 賣到 20 億美元，整體份額仍是低個位數。","ruling":"可調和，分母不同。方向採管理層，規模與 TAM 計算採第三方。","evidence_level":"管理層與第三方研究","settle_metric":"Mercury 與 TrendForce 下一期份額","if_then":["如果第三方份額兩期內沒有增加，下修資料中心權利金路徑，不追。","反向條件：如果 2027 年第三方份額超過 30%，基準資料中心權利金上修。"],"evidence_refs":[]},{"axis":"雙引擎互相強化，還是自家晶片疏離客戶","cause":"新證據","prior_field":null,"side_a":"2026-11-04 Rene Haas 以 OCI 為例，同時提供 NVIDIA Vera 與 AGI CPU 實例，兩項業務互相強化；本季有主要客戶首次簽 ATA。","side_b":"20-F 寫明授權客戶可能縮減合作或轉向替代架構；前份記 Qualcomm 的 Oryon 伺服器晶片首發部署客戶是 Meta，而 Meta 也是 AGI CPU 的主要客戶。","ruling":"目前採 A 側。尚無客戶實際流失的證據；衝突是慢變數，用 ATA 數量與客戶路線圖追蹤。","evidence_level":"法說與 20-F，缺實際流失資料","settle_metric":"活躍 ATA 家數、前五大客戶公開路線圖","if_then":["如果活躍 ATA 連 2 季下降，或前五大客戶公開轉向 RISC-V，減碼一半。","反向條件：如果矽業務占比升到 10% 時 ATA 仍持續增加，把這條風險降級。"],"evidence_refs":["customer_second_source#1","channel_business_model_shift#1"]},{"axis":"共識修正讀數是否可信","cause":null,"prior_field":null,"side_a":"Koyfin 兩份快照 FY1、FY2、FY3 修正全為 0.0%，90 天間距也是 2.23 美元對 2.23 美元。","side_b":"Chartmill 在 2026-10-17 顯示 FY2027 EPS 2.25 美元，近 3 個月上修約 2.13%；11-04 財報後的權利金落空也不可能完全沒反映。","ruling":"視為資料缺口，不當成沒有修正的證據。11-04 的利空推定還沒進賣方模型，下一份快照前凍結任何加碼判斷。","evidence_level":"資料品質問題","settle_metric":"11-04 後 30 天的共識快照","if_then":["如果 30 天後 FY2028 共識下修超過 5%，不追，重啟價位依新共識重算。","反向條件：如果共識上修，維持本輪基準，不因上修提前建倉。"],"evidence_refs":[]},{"axis":"賣方目標價與本輪基準","cause":null,"prior_field":null,"side_a":"賣方平均目標價約 213～272 美元，區間 125～500 美元，多數評等買進。","side_b":"本輪基準五年目標約 171 美元，12 個月約 171 美元。","ruling":"比共識悲觀，理由是市場把 FY2029 EPS 建立在權利金回到 20% 以上，並用 IP 倍數看待 30～40% 毛利的矽業務。賣方全距 4 倍，且多數早於財報，參考價值低，本輪信心也因此只給中。","evidence_level":"聚合站資料，日期不一","settle_metric":"財報後新目標價與權利金實績","if_then":["如果 FQ4 FY27 權利金年增 ≥20%，承認共識較對，基準 EPS 上調。","反向條件：如果權利金年增仍低於 12%，共識下修，不追。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：AMD 上調伺服器 CPU 業務，TrendForce 估 2026 年份額約 27%；Qualcomm 進入資料中心 CPU。","side_b":"結構：x86 頭節點轉向 Arm，Google、NVIDIA 已有實例；其他結構變數是三法域反壟斷與出口管制。","ruling":"雙向拉鋸。需求結構轉好，同時競爭加劇、監管收緊；依據是 11-04 法說與 TrendForce、Bloomberg 報導。","evidence_level":"法說與第三方","settle_metric":"第三方伺服器份額、反壟斷進度","if_then":["如果 FTC 正式起訴，減碼一半。","反向條件：如果 FTC 結案且份額持續上升，定價面改判擴大。"],"evidence_refs":["regulatory_antitrust#1"]}],"triggers":[{"n":1,"text":"股價進入重啟區","type":"估值rearm","maps_to":"價格","metric":"FY2028 共識 EPS 本益比","threshold":"≤36 倍（約 110 美元）","action":"重跑完整研究，通過後分批反買，上限 3%","source_freq":"每日收盤","date":null},{"n":2,"text":"FY2028 權利金年增低於 15%","type":"Single Thing","maps_to":"Single Thing","metric":"FY2028 全年權利金年增","threshold":"<15%","action":"清倉；未持有者不建倉","source_freq":"季度股東信","date":"2028-05"},{"n":3,"text":"FQ3 FY27 財報檢查權利金與資料中心占比","type":"假設驗證","maps_to":"H1","metric":"FQ3 FY27 權利金年增","threshold":"<1%","action":"不追，基準 EPS 下修 5%","source_freq":"季度股東信","date":"2027-02"},{"n":4,"text":"基期轉易後第一個讀數","type":"假設驗證","maps_to":"H1","metric":"FQ4 FY27 權利金年增","threshold":"<12% 為失敗，≥20% 為超標","action":"<12% 不追並下修基準 EPS 10%；≥20% 重啟價位上調到 45 倍","source_freq":"季度股東信","date":"2027-05"},{"n":5,"text":"矽業務累計營收更新","type":"假設驗證","maps_to":"H2","metric":"FY27＋FY28 矽業務累計營收展望","threshold":"低於 15 億美元","action":"不追，重啟門檻降回 30 倍","source_freq":"季度法說","date":"2027-02"},{"n":6,"text":"Qualcomm 案與反壟斷里程碑","type":"風險","maps_to":"R2","metric":"判決或正式指控","threshold":"法院限制 CSS 或授權條款、FTC 起訴、歐盟發出異議聲明，任一成立","action":"減碼一半；未持有者不追，重啟門檻降到 30 倍","source_freq":"法院文件、FTC 公告、6-K","date":"2026-Q4","evidence_refs":["major_events#1","regulatory_antitrust#1"]},{"n":7,"text":"矽業務稀釋開始顯影","type":"風險","maps_to":"R3","metric":"合併毛利率與非 GAAP 營業利益率","threshold":"毛利率 <90% 且營業利益率 <40%","action":"減碼一半","source_freq":"季度股東信","date":"2027-05","evidence_refs":["geo_supply_chain#1"]},{"n":8,"text":"授權客戶開始轉向","type":"風險","maps_to":"R4","metric":"活躍 ATA 家數與前五大客戶路線圖","threshold":"ATA 連 2 季下降，或前五大客戶公開轉向 RISC-V","action":"減碼一半","source_freq":"季度法說、客戶公告","date":null,"evidence_refs":["customer_second_source#1"]},{"n":9,"text":"控股股東壓力","type":"風險","maps_to":"R7","metric":"SoftBank 評等與持股","threshold":"S&P 降到 BB 以下，或公告減持 Arm","action":"不追","source_freq":"評等公告、6-K","date":null,"evidence_refs":["customer_concentration_credit#3"]},{"n":10,"text":"下次財報後複審","type":"複審日期","maps_to":"全部假設","metric":"日期","threshold":"FQ3 FY27 財報公布後","action":"更新情境樹與重啟價位","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"FY2028 全年權利金年增","bear_threshold":"<15%","window":"2028-05 公布","source":"Arm 季度股東信","last_status":"warning"},{"metric":"FY27＋FY28 矽業務累計營收","bear_threshold":"<10 億美元","window":"至 2028-03","source":"Arm 季度法說","last_status":"ok"},{"metric":"合併毛利率與非 GAAP 營業利益率","bear_threshold":"毛利率 <90% 且營業利益率 <40%","window":"FQ4 FY27 起逐季","source":"Arm 季度股東信","last_status":"ok"},{"metric":"ACV 年增","bear_threshold":"連 2 季 <8%","window":"逐季","source":"Arm 季度股東信","last_status":"ok"},{"metric":"FTC 起訴或歐盟異議聲明","bear_threshold":"任一發生","window":"未來 24 個月","source":"FTC、歐盟執委會公告","last_status":"unknown"},{"metric":"股份薪酬含雇主稅占營收","bear_threshold":"連 4 季 >30%","window":"逐季","source":"Arm 季度股東信","last_status":"warning"}],"evidence_dismissed":[{"ref":"capital_markets_pricing#5","reason":"這則 245 美元均值對應的是 2026-06-05 股價 393 美元；股價已跌到 174.62 美元，目標價低於股價的前提不再成立，資料已過期。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"重啟後上限 3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方把 FY2029 EPS 4.05 美元建立在權利金回到 20% 以上，並用 IP 公司的倍數看待矽業務；本季權利金年增 8%，矽業務毛利率 30～40%，兩點都還沒被證實。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=-18.12, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 情境缺少從出貨量與單價推到 EPS 的算式，成長跑道判綠也撐不住：資料中心的份額已經很高，AGI CPU 尚無營收，所以這條爆發候選的 Bull 依據不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"FY2028 共識 EPS 本益比 ≤36 倍（約 110 美元，基準五年年化約 9%）→重跑完整研究；重啟後倉位上限 3%","exec_line":"未持有者現價不建倉。已持有者不加碼，等 FQ4 FY27 權利金讀數；FY2028 權利金年增低於 15% 就清倉。"},"reasoning":{"industry":"Q2 FY27 營收 14.43 億美元，年增 27%。授權及其他 7.73 億美元（占 54%，年增 50%，比公司預期多約 1 億美元），權利金 6.70 億美元（占 46%，年增 8%）。權利金內部：資料中心翻倍，實體 AI 年增 50%，邊緣 AI 約零成長。毛利率 97.44%（TTM），非 GAAP 營益率 44.2%，GAAP 只有 13.9%，差額幾乎都是股份薪酬。單點依賴：前五大客戶占 FY2026 營收約 57%，最大客戶 Arm China 約 16%；SoftBank 本季貢獻 2.09 億美元，占營收 14.5%，同時是持股約 90% 的控股股東；矽業務的 3 奈米產能靠台積電，首要客戶是 Meta。AGI CPU 尚無營收，首批商業出貨在 FQ4 FY27。","moat":"客戶換架構要重寫軟體、重新驗證，生態有三千萬開發者。方向證據用份額軸，因為同業 ROIC 差距事實表未涵蓋。本季新簽 3 份 ATA、4 份 CSS，其中一家主要客戶首次簽 ATA。扣分項只有 RISC-V 屬於生態攻擊；Qualcomm 自研核心仍用 Arm 指令集，算點對點競爭。當期 ROIC 只能定性：高毛利、輕資產，但投入資本事實表未涵蓋，GAAP 營益率 17.02% 與非 GAAP 44.2% 的落差全在股份薪酬。再投資主要走研發費用，研發密度 57.28%，矽業務之後會多出存貨與供應預付。","growth":"成長來自量（資料中心、矽業務）與價（v9／CSS 費率），併購與回購幾乎沒有貢獻。共識 FY2027E 到 FY2029E 非 GAAP EPS 由 2.23 美元到 4.05 美元，兩年複合 34.8%。基期 FY2026 只有 GAAP 0.85 美元，和非 GAAP 共識口徑不同，不拿來算三年 CAGR。內生上界算不出來，缺口無法歸因，這段成長依賴 re-rate，長期信心上限為中。FY2027 全年權利金展望在 2026-07-29 還是接近高十幾%，FQ2 實際 8%、FQ3 指引低個位數，代表高成長是往後遞延，不是已經發生。","governance":"淨現金約 31.21 億美元。FCF／淨利：FY2023 為 1.23，FY2024 為 3.09，FY2025 為 0.20，FY2026 為 1.05，波動很大。Q2 非 GAAP 自由現金流只有 1.10 億美元，Q1 為 6.65 億美元，落差原因事實表未涵蓋。股份薪酬加雇主稅 4.25 億美元，占營收 29.5%，占非 GAAP 營業利益 66.6%。稀釋股數由 FY2023 約 10.26 億升到 FY2026 約 10.64 億，年增約 1.2%，還在 1.5% 以內，但股價下跌會讓同樣金額的薪酬換出更多股。近三年現金去向四分、回購紀錄事實表未涵蓋。","valuation":"要年化 10%，在 30 倍終端本益比下，FY2032 非 GAAP EPS 要到約 9.37 美元。我的基準是 6.10 美元。倍數：FY2027E 78.3 倍，FY2028E 57.1 倍，FY2029E 43.1 倍，前瞻 EV／S 30.2 倍。敏感度（本輪自估）：FY2032 權利金由約 66 億美元降到約 43 億美元，EPS 少約 1.7 美元；矽業務由約 75 億美元降到約 30 億美元，EPS 少約 1.0 美元；終端倍數由 28 倍降到 20 倍，股價少 29%。成長熄火測試：FY2029 之後成長率降到 15%、10%、5%，對應 30、20、15 倍，股價約 122、78、56 美元，三種都低於現價。短期上檔用 FY2028 基準 EPS 2.85 美元×60 倍，中期用 FY2030 基準 EPS 4.35 美元×38 倍。","premortem":"26 週報酬 −18.12%，RSI 31.08，動能沒有過熱，股價貼著 104 週均線 174.4 美元。賣方目標價區間 125～500 美元，高低差 4 倍，且多數早於 11-04 財報，我的基準比賣方平均悲觀。反證、矛盾裁定與觸發條件集中在反證紀錄，這裡不重寫。"},"plain":{"six":{"how_it_makes_money":"賺晶片設計公司的錢：設計開始時收授權費，晶片出貨時收權利金。錢卡在指令集與軟體生態這一節。本季成長靠授權，權利金只年增 8%。","moat":"護城河方向穩定（→）。機制是指令集加軟體生態的轉換成本；份額還在往上，定價工具卻同時受反壟斷挑戰。","growth":"五年後跑道仍寬（🟢）：伺服器出貨份額仍低於 35%，AGI CPU 是有訂單的第二條曲線。近兩年共識 EPS 年複合 34.8%，比我相信的快。","capital":"現金充足，併購風險小，但股份薪酬吃掉非 GAAP 營業利益的三分之二。","valuation":"現價要求非 GAAP EPS 五年複合約 33%。我不信到那個程度，基準約 22%，五年報酬接近零。","how_wrong":"看空可能錯在權利金基期轉易後直接回到 20% 以上；看多可能錯在權利金連 15% 都到不了。"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方把 FY2029 EPS 4.05 美元建立在權利金回到 20% 以上，並用 IP 公司的倍數看待矽業務；本季權利金年增 8%，矽業務毛利率 30～40%，兩點都還沒被證實。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 FY2028 共識 EPS 本益比降到 36 倍以下（約 110 美元），再重跑完整研究。","qc48_result":"fail","qc48_note":"Bull 情境缺少從出貨量與單價推到 EPS 的算式，成長跑道判綠也撐不住：資料中心的份額已經很高，AGI CPU 尚無營收，所以這條爆發候選的 Bull 依據不成立。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":174.62,"week26_return_pct":-18.12,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"共識 EPS 是非 GAAP，排除占非 GAAP 營業利益 66.6% 的股份薪酬與雇主稅；GAAP 本益比 200.71 倍。分母本身就是爭點，78 倍不能當便宜的論據。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"regulatory","event":"Qualcomm／Nuvia 案預計開庭","impact":"高","watch":"法院是否限制 Arm 的授權條款或 CSS 安排"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FQ3 FY27 財報，公司承諾更新 AGI CPU 展望","impact":"高","watch":"權利金年增、資料中心占比、矽業務累計營收"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"AGI CPU 首批商業出貨（FQ4 FY27）","impact":"高","watch":"出貨是否如期、客戶是否超出 Meta"},{"date":"2027-Q2","date_precision":"quarter","type":"guidance","event":"下一次 Arm Everywhere 活動，CFO 稱約在 2027 年上半年更新長期目標","impact":"中","watch":"FY2029 之後的矽業務目標與毛利率路徑"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FQ4 FY27 財報，手機基期轉易後第一個完整讀數","impact":"高","watch":"權利金年增是否 ≥12%，合併毛利率是否跌破 90%"}],"_projected_from":"v19"}
```
