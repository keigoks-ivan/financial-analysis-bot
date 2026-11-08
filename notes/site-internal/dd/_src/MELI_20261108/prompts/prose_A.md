你是 stock-analyst v20 的**散文層（prose）agent**，標的 MELI（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MELI_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MELI　日期：2026-11-08　archetype：None　前份裁決：2026-08-07　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1820B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（673B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（985B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1411B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1002B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（544B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（735B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2293B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3494B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3686B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1820           3626-5180      5 條（2–6 內）  
s3                  8000         673           5129-7327      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3398          8121-11602      5 條（2–6 內）  
s6                 11000         544          7319-10456      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         735           1935-2765      5 條（2–6 內）  
s10                 5000        2293           1895-2707      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3686           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4876B；至少需散文≈40.12KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−60
−59%
−50%
−36%
−35%
−35
−34%
−17.5%
−7.5
0
0.2%
0.66
0.75
0.9
1
1.04
1.5
1.52
1.71
02
2
2.05
2.14
2.52%
2.7%
2.84
2.85
3%
3
3.4%
3.57
4%
04
4
4.4
4.41
4.900%
4.93
5%
5
05
5.03
5.14
5.850%
6
6%
6.0%
6.3%
6.5%
6.6%
7%
07
7
7.42%
7.5
7.7
7.9%
8.0%
08
8%
8
8.24%
8.83
09
9.0%
9
9.2%
9.27
9.53
9.8%
10
10%
10.4%
11
11%
11.08%
11.3%
11.4
11.5%
11.8%
12
12.7%
13
14
14%
15
15%
15.6%
16%
17
17.5%
17.7
18
18.7%
19
19.0%
19.22
20
20%
20.1%
20.7
21%
21
22
24
25%
25.9%
26
27
27.02
28
29%
29.5%
30
30%
30.92
31.81%
32
33.5%
34.2
34.4
35%
36%
38
38.26
39.4
39.47
40%
40
40.6%
41%
41
42%
42
42.02%
42.5%
44
44.5%
45
45%
46%
46.09
46.09%
46.1%
46.1
47.2%
47.5
49
50%
50
50.24%
50.3
50.6
50.7
51.8
53.8
53.8%
54
55.89
58%
58
60%
61.2%
61.4
61.41
62%
66
67%
69%
70
70%
76.4
78.56
79
84
86
87.8
87.86
90%
90
95.3%
100%
100
100.4
104
107.5
108
113.0%
116
130
150%
154
180
190
196
228.2
250
300
312
482
497
620
800
913
972
993
1510
1510.0
1830.0
1830
2025
2026
2027
2028
2029
2033
2036
20261108
1,050
1,069
1,086
1,200
1,250
1,510
1,580
1,596
1,600
1,830
1,997
10,780
2,153
2,166
2,209
2,259
2,322
2,854
2,878
28,893
3,201
38,469
5,488
6,420
7,000
9,300
9,400
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
{"meta":{"ticker":"MELI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"MercadoLibre, Inc."},"oneliner":"營收仍年增 45%，營益率卻跌到 6.3%，讓利是自願還是被競爭逼的還沒分曉；FY27 共識隱含約 8% 營益率，證據到位前不追。","thesis":{"H":[{"id":"H1","text":"飛輪繼續放大，領先地位守得住。Q3 巴西 GMV 年增 36%、每買家件數年增 16%，兩項通過，抽成缺當季值。","2y":"巴西 FX 中性 GMV 年增維持 25% 以上","5y":"拉美線上滲透持續上升，MELI 維持區域第一","10y":null,"threshold":"巴西 FX 中性 GMV 年增≥25% 連 2 季，每買家件數年增為正，3P 抽成不低於 Q2 2026 減 50bp（Q3 抽成值事實表未涵蓋）","source":"公司季報與電話會議；第三方份額是資料缺口","drift_rule":"連 2 季偏離門檻 5% 算削弱，連 3 季偏離 10% 算反轉"},{"id":"H2","text":"6% 至 7% 的營益率是投資期低點，FY27 開始回升。Q3 6.3%，距破壞線 6.0% 只差 30bp。","2y":"FY27 營益率≥8.0% 算驗證，≥10% 才算收割","5y":"FY31 淨利率約 6.3%，接近 FY2023 的 6.5%","10y":null,"threshold":"FY27 全年 GAAP 營益率≥8.0%；任一季低於 6.0% 或連 4 季不升算破壞","source":"公司 8-K 季報；共識隱含 8% 由 FY27 EPS、營收與 Q3 淨利對營業利益比換算","drift_rule":"連 2 季偏離門檻 5% 算削弱，連 3 季偏離 10% 算反轉"},{"id":"H3","text":"信貸能在高速成長下維持風險調整後利差。Q3 NIMAL 20.1%、15 至 90 天逾期率 7%，兩項通過，90 天以上缺當季值。","2y":"信貸組合高速成長時 NIMAL 維持 20% 以上","5y":"信貸走過一次完整信用週期，NIMAL 仍為正且可持續","10y":null,"threshold":"NIMAL≥20% 連 2 季，15 至 90 天逾期率≤8.0%，90 天以上逾期率不連 3 季上升（Q3 值事實表未涵蓋）","source":"公司 8-K 與 10-Q","drift_rule":"連 2 季偏離門檻 5% 算削弱，連 3 季偏離 10% 算反轉"}],"R":[{"id":"R1","text":"低價平台把巴西與墨西哥的低客單區變成價格戰，讓利收不回來。","h_ref":"H1","clock":"🔥","threshold":"巴西 FX 中性 GMV 年增連 2 季低於 25%，且營益率低於 7%","evidence_refs":["competitive_share_entrants#0","end_markets#2"]},{"id":"R2","text":"信用週期在快速放款時反轉；Q1 貸款期限拉長已引來律所徵求，目前沒有正式訴訟。","h_ref":"H3","clock":"⚡","threshold":"15 至 90 天逾期率連 2 季高於 8.0%，或提列年增率高於組合年增率連 2 季（提列資料事實表未涵蓋）","evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"id":"R3","text":"投資期沒有盡頭：運費、聯盟行銷、1P 與巴西工時改革持續吃掉利潤率。","h_ref":"H2","clock":"🔥","threshold":"連 4 季營益率不升，或 Q4 2026 與 Q1 2027 連 2 季低於 6.3%","evidence_refs":["end_markets#1","capital_markets_pricing#1","channel_business_model_shift#2"]},{"id":"R4","text":"拉美監管、消費者保護與匯率政策累積成本；布宜諾斯艾利斯省調查與智利裁罰都還在早期或覆議階段。","h_ref":"H2","clock":"🐢","threshold":"美元營收成長低於 FX 中性成長 10 個百分點以上連 2 季，且營益率同步下滑","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","major_events#2","product_recall_warning#0"]}],"single_thing":{"description":"FY2027 全年 GAAP 營業利益率沒有回到 8.0% 以上。","why_fatal":"終端淨利率每差 1 個百分點，FY31 EPS 差約 20.7 美元，目標價差約 16%，大於營收差 10%（約 10%）與終端倍數差 1 倍（約 4%）。FY27 共識 EPS 隱含營益率約 8%，沒到就代表低利潤率是常態，FY2、FY3 共識都要重算。","if_happens":"FY2 共識下修，基本情境改向悲觀情境靠攏；放棄建倉，持有者減碼至半倉。","how_monitor":"每季 8-K 的 GAAP 營業利益率，搭配 FY2 共識 EPS 月度快照；全年結果在 FY2027 財報確認。","probability":"12 至 24 個月內約 40%"}},"appendix_a":{"growth_durability":8,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":27.02,"peg_fy2":1.04,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":39.4,"FY2026E":38.26,"FY2027E":55.89,"FY2028E":78.56},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS；FY2026E 至 FY2028E 為 Koyfin 2026-11-07 共識快照，FY1＝FY2026，12 月底財年；EPS 家數事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MELI_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"金融","confidence":"中","fingerprint":"電商平台＋支付＋信貸飛輪，利潤率處於自願投資低點，信貸占比持續上升"},"industry":{"clock_phase":"II","sd_verdict_source":"週期位置為擴張期，依據是巴西件數年增 45%、Q3 履約面積季增近 20%。供需持久性：需求面結構性持久，拉美電商成長約為全球 1.5 倍（次級來源）；供給端有亞洲平台持續加碼，利潤分配比需求本身更不穩。","bargaining":{"up":"上游應用商店抽 15% 至 30%，POS 設備受記憶體漲價影響，公司議價力弱。","down":"賣家分散，但公司本季仍調降部分抽成換取供給，定價空間受限。","geo":"巴西是主戰場；阿根廷利潤率較高，CEO 未回答是否會向區域平均收斂。"},"profit_pool_dir":"短期由平台流向消費者與賣家（免運門檻下調、抽成調降、PIX 折扣）；營業利潤池五年變化事實表未涵蓋。","tam_table":[{"item":"拉美電商市場 2026","value":"2,153 億美元（Endeavor／MercadoLibre，次級轉述，各來源定義差異大）"},{"item":"線上滲透率","value":"許多次區域僅低雙位數，美國約 16%（次級來源，分母未核）"},{"item":"公司 GMV 年化","value":"Q3 228.2 億美元×4，約 913 億美元；與上列市場規模口徑不一致，不可直接算市占"},{"item":"巴西份額","value":"Shopee 約 20%，Amazon 約 10%（會議摘要）；MELI 份額數字事實表未涵蓋"},{"item":"營業利潤池五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"商務流量、自建物流、Mercado Pago 與信貸互相強化：市集交易資料先於放款，生態系用戶 GMV 多 70%、TPV 多 90%（CFO，2026-08-05）。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大：巴西每件成本年減 5%、每買家件數年增 16%。定價力縮減：毛利率連四期下滑，Q3 營益率 6.3%，抽成下調。改為↓的條件：巴西 FX 中性 GMV 年增連 2 季低於 25% 且營益率仍低於 7%。","peer_na_reason":"同業投入資本報酬率事實表未涵蓋，用毛利率、營益率與份額替代；FCF 利潤率受金融業務現金流扭曲，不作比較。","threats":[{"level":"🔴","text":"Shopee、Temu 與社交平台用低價、跨境與短影音攻低客單區，MELI 以下調免運門檻與聯盟行銷回應。目前看是低客單範圍受攻擊，整體成長沒有放緩。攻擊者資本量級：Shopee 所屬集團近四季營益率 8.24%，能持久。","p":"40%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","end_markets#2"]},{"level":"🟡","text":"外部購物代理若成為入口，會繞過 MELI 的 app 與廣告；公司決定暫不把商品開放給外部平台。AI 的附著點目前在自有物流、信貸與資料，屬強化；搜尋 LLM 成本已被增量收入涵蓋，但沒有金額。分界年抓 2029，屆時外部代理占巴西線上流量超過 10% 就升級為架構替代。應用商店抽成與對手更快採用 AI 屬同類壓力。","p":"20%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"POS 商家常有多台設備，可以切換供應商；收單 take rate 因往大商家移動而下滑，目前收單仍年增 42%。","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率，周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多為同一消費者，賣家端由需求帶動。購物頻次在上升：巴西每買家件數年增 16%。代理讀數：Q3 活躍買家 9,400 萬、金融月活 9,300 萬。"},{"item":"決策層級","level":"🟡","text":"買家每次下單都可比價，低單價商品替代性高，社交平台也集中在低客單；高單價、分期與會員免運的黏著度較強。POS 商家可多機切換（Fintech 主管，2026-11-04）。漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"利益目前由平台往消費者與賣家移動：免運門檻下調、部分抽成調降、PIX 折扣。平台仍保住廣告（年增 58%）與收單（年增 42%）。上游應用商店抽 15% 至 30%，POS 設備的晶片成本 CFO 稱是長期現象。"},{"item":"社會容忍度","level":"🟡","text":"墨西哥反壟斷案 2025 年 8 月結案沒有矯正措施，但點名 Buy Box 與物流整合；布宜諾斯艾利斯省有消費者保護調查，智利有商品安全裁罰。NIMAL 約 20% 的消費信貸在政治上敏感，巴西債務重整方案已經存在，目前對公司影響小。"}],"roiic":"事實表未涵蓋：缺投入資本與折舊","reinvest_rate":"事實表未涵蓋：缺折舊與營運資本變動；已知 Q3 資本支出 5.03 億美元、Q2 信貸投入約 21 億美元","endo_ceiling":null,"formula_note":"當期 ROIC 與增量 ROIC 都算不出來。替代讀數：FY2022 到 FY2025 增量營業利益÷增量營收約 11.8%（1,069→3,201 百萬美元；營收 10,780→28,893 百萬美元）。FY2025 到近四季：營業利益約 3,201→2,854 百萬美元（近四季營收由市值÷P/S 推得約 38,469 百萬美元，乘 7.42%），增量為負。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","MELI":42.02,"NU":null,"SE":44.34,"AMZN":51.08,"CPNG":27.37,"unit":"%"},{"metric":"營業利益率","MELI":7.42,"NU":null,"SE":8.24,"AMZN":12.89,"CPNG":-3.43,"unit":"%"},{"metric":"FCF 利潤率","MELI":31.81,"NU":-12.68,"SE":16.92,"AMZN":-6.38,"CPNG":-1.14,"unit":"%"},{"metric":"研發密度","MELI":7.16,"NU":null,"SE":4.24,"AMZN":null,"CPNG":null,"unit":"%"}],"competitors":[{"name":"NU","gm":null,"om":null,"fcf_margin":-12.68,"rd_intensity":null,"strategy_note":"列為金融同業；事實表只有 FCF 利潤率，銀行現金流不可比，競爭強度事實表未涵蓋。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SE","gm":44.34,"om":8.24,"fcf_margin":16.92,"rd_intensity":4.24,"strategy_note":"Shopee 是最直接的攻擊者，巴西份額約 20%；集團近四季營益率略高於 MELI，不是靠賠錢搶市，撐得住長期競爭。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"AMZN","gm":51.08,"om":12.89,"fcf_margin":-6.38,"rd_intensity":null,"strategy_note":"巴西份額約 10%，沒有擴大；資本最雄厚，但事實表沒有顯示它在拉美用補貼主動擴張。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CPNG","gm":27.37,"om":-3.43,"fcf_margin":-1.14,"rd_intensity":null,"strategy_note":"事實表未顯示與 MELI 的市場重疊，僅作自建物流電商的利潤率對照。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主，價為負（免運門檻下調後小籃子變多），併購與回購約為零。","runway_years":"無法精算：只有次級來源的低雙位數滲透率，缺線上與實體零售分母","runway_post_y5":"🟢","endo_ceiling_basis":"事實表沒有投入資本、折舊與營運資本變動，內生上界無法計算，共識 25.9% 是否超出也無法判定；情境樹的悲觀機率仍取 30%。替代讀數見護城河題：FY2022 到 FY2025 增量營業利益率約 11.8%，FY2025 到近四季為負。","segments":[{"item":"商務","value":"Q3 約 61.41 億美元（總營收減金融自算），年增 47.2%；巴西 FX 中性 GMV 年增 36%，墨西哥約 21%（次級來源）"},{"item":"金融","value":"Q3 46.09 億美元，年增 42.5%；月活年增 29%，資產管理規模年增 67%，信貸組合年增 62%"},{"item":"廣告","value":"年增 58%，金額事實表未涵蓋"},{"item":"跨境","value":"GMV 年增約 60%，為 2026-08-05 CEO 說法，Q3 未更新"}],"decay_signals":[{"signal":"毛利率連續下滑","status":"亮","evidence":"FY2023 50.24% 到近四季 42.02%；單季年比資料事實表未涵蓋，以年度與近四季代替"},{"signal":"核心市占縮減","status":"未判定","evidence":"公司稱份額上升，Shopee 巴西約 20%，MELI 份額缺第三方數字"},{"signal":"FCF 對淨利低於 0.75","status":"未判定","evidence":"報表 FCF 未扣信貸投入，不可用；調整後 FCF 只有單季資料"},{"signal":"產業估值倍數系統性下移","status":"未判定","evidence":"事實表只有本公司四個年度端點，沒有同業序列"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近年唯一收購價格未揭露；回購與現金去向四分事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年僅見 Nikos DTVM 一筆，價格未揭露，無法計算已實現報酬","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購紀錄與均價","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"長期留任計畫為現金結算；FY2022 淨利 482÷EPS 9.53 約 50.6 百萬股，FY2025 淨利 1,997÷EPS 39.4 約 50.7 百萬股，三年合計稀釋約 0.2%","grade":"過"}]},"valuation":{"basis":"本益比：FY1 39.47 倍、FY2 27.02 倍、FY3 19.22 倍；EV/S 2.05 倍僅供對照","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法做同級對照，已列為資料缺口"},"fwd_pe":39.47,"peg":1.52,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"三個條件合起來定為合理：一，現價 1510 美元對 FY2 共識 27.02 倍、FY1 39.47 倍；二，FY2 共識要靠營益率回到約 8%，Q3 只有 6.3%，分母正是爭點，便宜論點不成立；三，基本情境五年年化約 15.6%，全部來自 EPS，倍數假設是壓縮。本益比年度端點分位 0 只來自 4 個點，不是五年分位；五年高低事實表未涵蓋，五年分位留空。PEG 以 FY1 本益比除以三年 EPS 年複合 25.9% 計算。","upside_short_pct":6.0,"upside_mid_pct":53.8},"trap_analysis":{"verdict":"🟡","label":"利潤率低點是投資還是新常態，尚未分曉"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"10-K 承認 2025 年亞洲平台以低價與跨境模式在拉美取得顯著份額；Shopee 在巴西約 20%；Q3 營益率 6.3%，毛利率連四期下滑。","assumption":"低價戰會結束，免運與抽成讓利能在份額守住後收回。","consequence":"讓利變成永久成本，FY31 淨利率停在 3% 至 4%，EPS 約 54 美元、18 倍，約 972 美元，五年跌 36%；若同時碰上巴西信用週期，跌幅可達 50% 以上。","ruling":"採納為悲觀情境主線，機率 30%。與唯一致命點部分重疊，重疊在營益率；信用週期獨立，另列信貸門檻補上。","watch":"巴西 FX 中性 GMV 年增、營益率、15 至 90 天逾期率","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#1"]},{"view":"論點失敗","evidence":"Q1 財報揭露貸款期限由約 5 個月拉長到 8 個月並在巴西提列準備，隔天股價跌 12.7%，律所展開徵求；Q2 90 天以上逾期率連兩季上升至 18.7%；Q3 Fintech 主管承認在巴西較謹慎。","assumption":"15 至 90 天逾期率在組合年增 62% 時仍能反映真實品質。","consequence":"逾期率的分母被新放款撐大，一旦放緩，逾期率可能一次跳升，NIMAL 與資金成本同時受壓。","ruling":"採納為監測項。逾期率是落後指標，加上領先門檻：提列年增率高於組合年增率連 2 季即觸發。Q3 提列金額與 90 天以上逾期率事實表未涵蓋，風險不能稱已解除。律所徵求不是訴訟，截至 7 月 10 日沒有案件，受影響金額是資料缺口。","watch":"90 天以上逾期率、提列年增對組合年增","evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"view":"論點成功但股東經濟變差","evidence":"CFO 稱每季都在擴倉；聯盟行銷會持續投資；巴西工時由 44 小時降到 40 小時需要增聘物流人力（CEO，2026-11-04）；1P GMV 年增 69%、毛利率下滑約 300bp（Zacks）；調整後 FCF 只有營收約 2.7%。","assumption":"份額領先會自動轉成利潤率，不需要持續補貼。","consequence":"GMV 與用戶都贏，但利潤被物流、1P 與信貸資本吃掉；FY31 淨利率每低 1 個百分點，EPS 少約 16%。","ruling":"部分採納。每件成本下降與 9 月免運件貢獻轉正是反證，但都是管理層單方說法，標為未證、監測；連 2 季營益率低於 6.3%，暫時性說法視為證偽。","watch":"營益率、毛利率、資本支出占營收、調整後 FCF","evidence_refs":["channel_business_model_shift#2","end_markets#1"]},{"view":"價格已反映太多","evidence":"現價對 FY2 共識 27.02 倍，共識要 FY27 EPS 年增 46.1%。Q3 財報後共識快照沒變，第三方摘要顯示 Q3 EPS 低於共識。賣方目標價仍是財報前數字。","assumption":"共識 FY27、FY28 的利潤率回升會如期發生。","consequence":"FY2 下修 15% 時現價對應約 32 倍；股價較前次 1830 美元跌 17.5%，不等於安全邊際。","ruling":"採納。賣方模型依賴利潤率回升，利空尚未進入模型，下修反映完之前凍結加碼，等第一個確認或否證數據點，也就是 Q4 2026 財報。","watch":"FY2 共識 EPS 月度變化","evidence_refs":["capital_markets_pricing#1"]}],"max_dd":{"lo":-60,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1830.0 → 本次 1510.0（-17.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1830.0","side_b":"本次 price_at_dd=1510.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,830 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,830 美元：Bull 價 6,420、Bear 價 1,086，五年期望值 +113.0%，基準年化 19.0%，不對稱比 5.14","side_b":"本次情境、股價仍用 1,830 美元：Bull 價 5,488、Bear 價 972，五年期望值 +61.2%，基準年化 11.3%，不對稱比 2.84","ruling":"先換情境、股價不動：五年期望值少 51.8 個百分點，基準年化少 7.7 個百分點。不對稱比由 5.14 變為 2.84。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,830 美元：五年期望值 +61.2%，基準年化 11.3%，不對稱比 2.84","side_b":"本次情境、股價 1,510 美元：五年期望值 +95.3%，基準年化 15.6%，不對稱比 4.93","ruling":"再換股價、情境不動：起點價下跌 17.5%，五年期望值多 34.2 個百分點，基準年化多 4.4 個百分點，不對稱比由 2.84 升到 4.93。合計五年期望值比前份少 17.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"利潤率下滑的性質","cause":null,"prior_field":null,"side_a":"管理層：這是刻意投資，運費與聯盟行銷換來頻次，巴西每件成本年減 5%，9 月低價免運件貢獻首度轉正。","side_b":"10-K：亞洲平台以低價取得顯著份額；毛利率連四期下滑，抽成下調，九個月營益率 6.6% 對去年 11.5%。","ruling":"可調和，兩者都成立，比例未知。管理層的暫時性說法不採信也不否定，標為未證、監測。","evidence_level":"中：自願投資的證據多為管理層口徑，競爭壓力有年報與第三方份額。","settle_metric":"單季營業利益率與巴西 FX 中性 GMV 年增的組合","if_then":["若任一季營益率≥8.0% 且巴西 GMV 年增≥25%，投資說法成立，重跑研究後首階 1/3 分批建倉。","若營益率回升但巴西 GMV 年增跌破 25%，代表讓利一停份額就流失，不追。","若 Q4 2026 與 Q1 2027 連 2 季營益率低於 6.3%，暫時性說法證偽，悲觀機率升到 40%，持有者減碼至半倉。"],"evidence_refs":["end_markets#1","competitive_share_entrants#0"]},{"axis":"份額說法","cause":null,"prior_field":null,"side_a":"CEO（2026-11-04）：在每個主要市場的商務與金融都在拿份額。","side_b":"會議摘要：Shopee 在巴西快速拿到約 20%；10-K：亞洲平台取得顯著份額。","ruling":"可調和：被吃的可能是本地零售商，MELI 與 Shopee 可以同時成長。MELI 份額缺第三方數字，不可裁決至取得獨立份額資料。","evidence_level":"低：一邊是公司說法，一邊是會議摘要。","settle_metric":"第三方巴西電商份額（事實表未涵蓋）","if_then":["若第三方資料顯示 MELI 巴西份額連 2 季下滑，護城河方向改為↓，不建倉，持有者清倉。","若份額連 2 季上升且營益率同步回升，悲觀機率降到 25%。"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3"]},{"axis":"管理層前後說法","cause":"新證據","prior_field":null,"side_a":"CFO（2026-08-05）：能源導致物流成本上升，壓縮幅度輕微；POS 補貨是一次性，今年其餘時間補回。","side_b":"CFO（2026-11-04）：能源列為運費壓力四因素之一，預期壓力持續；Fintech 主管確認 POS 補貨效應已消退，但記憶體成本壓力未消失。","ruling":"POS 一次性的說法部分兌現，能源由輕微升為持續壓力，是說法變動。Q3 擴倉成本 CFO 預期部分在 Q4 回補，這一項同樣標為未證、監測。","evidence_level":"高：兩場電話會議原話可對照。","settle_metric":"Q4 2026 運費淨成本占營收變化","if_then":["若 Q4 2026 營益率未高於 Q3 的 6.3%，擴倉暫時性說法削弱，不建倉。","若 Q4 2026 營益率≥8.0%，說法成立，進入建倉條件的第一半。"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"信貸品質","cause":null,"prior_field":null,"side_a":"Q3 15 至 90 天逾期率 7%，與上季及去年同期相同；阿根廷接近歷史低點；NIMAL 20.1%。","side_b":"Q2 90 天以上逾期率連兩季上升至 18.7%；Q1 貸款期限拉長；巴西系統信用轉弱，管理層已對高風險客群收緊。","ruling":"可調和：短天期穩定不代表長天期穩定。Q3 的 90 天以上逾期率事實表未涵蓋，前份第三道門檻今天無法驗證，不可裁決至取得 Q3 10-Q 資料。巴西債務重整方案的影響公司未揭露，說是很小。","evidence_level":"中：短天期數字有一手來源，長天期缺當季值。","settle_metric":"90 天以上逾期率、提列年增對組合年增","if_then":["若 15 至 90 天逾期率連 2 季高於 8.0%，持有者減碼至半倉，未持有者不建倉。","若 15 至 90 天逾期率≥9.0% 且 NIMAL 低於 15%，清倉。"],"evidence_refs":["major_events#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"營收年增 45%、巴西件數年增 45%，股價低於 104 週均線約 25%，RSI 30.92；基本情境五年年化約 15.6%，倍數假設還是壓縮；每件成本下降與免運件貢獻轉正代表投資開始回收。","side_b":"分母還在動，共識尚未消化 Q3，週線在 250 週均線之下，前次設定的進場條件沒有觸發。","ruling":"不買。約束只有一個：營益率未止穩。跌幅本身不是安全邊際。","evidence_level":"中","settle_metric":"Q4 2026 與 Q1 2027 營業利益率、FY2 共識 EPS","if_then":["價格先走、證據未到：股價站回 1,596 美元上方但營益率未達 8.0%，不追。","跌但基本面無損：股價低於 1,200 美元，巴西 GMV 年增≥25%、15 至 90 天逾期率≤8.0%、FY2 共識累計下修不超過 10%，分批反買首階 1/3。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：亞洲平台取得顯著份額，免運與抽成持續下調。","side_b":"結構轉好：拉美電商成長約為全球 1.5 倍，巴西件數連 5 季年增 40% 以上。其他變數：墨西哥快遞稅率升到 33.5%、巴西恢復 50 美元以下免稅，方向相反；巴西工時改革增加物流用工。","ruling":"雙向拉鋸：需求轉好與競爭惡化同時發生，利潤分配是勝負所在。","evidence_level":"中：多為次級來源與公司說法。","settle_metric":"營業利益率與巴西 GMV 年增","if_then":["若競爭壓力下營益率連 2 季低於 6.0%，不建倉，持有者減碼至半倉。","若營益率站上 8.0% 且巴西 GMV 年增仍≥25%，改判結構性轉好中。"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"估值結論變動","cause":"新證據","prior_field":["val"],"side_a":"前份：偏便宜（🟢），股價 1830 美元。","side_b":"本次：合理（🟡），股價 1510 美元。","ruling":"股價跌 17.5%，但分母爭議比前份更實：Q3 沒達到 8.0%，便宜的論點要先等分母驗證。","evidence_level":"高","settle_metric":"FY2 共識 EPS 與營業利益率","if_then":["若 FY2 共識連 2 個月不下修且營益率達 8.0%，估值結論重回偏便宜。","若 FY2 共識累計下修超過 15%，估值結論維持合理並重算悲觀地板。"],"evidence_refs":[]},{"axis":"其他結論未變","cause":"新證據","prior_field":["signal","trap","moat_trend","archetype","cycle_position"],"side_a":"前份：訊號 B、陷阱風險 🟡、護城河方向→、品質複利成長、循環位置空白、裁決觀望、角色未建倉追蹤。","side_b":"本次：訊號、陷阱風險、護城河方向與類型沿用；MELI 不是循環股，循環位置仍留空；裁決與角色交由程式依本次輸入決定。","ruling":"Q3 兩邊都有新證據：成長與單位成本較好，利潤率較差，淨效果不足以改變這些結論。","evidence_level":"中","settle_metric":"Q4 2026 財報","if_then":["若巴西 GMV 年增連 2 季低於 25% 且營益率低於 7%，護城河方向改為↓，持有者清倉。","若營益率≥8.0%，陷阱風險下調一級。"],"evidence_refs":[]},{"axis":"跑道判斷變動","cause":"方法變動","prior_field":["runway_post_y5"],"side_a":"前份：中等（🟡）。","side_b":"本次：寬（🟢）。","ruling":"本輪按滲透率門檻重判：線上滲透低雙位數，低於 35%，信貸與投資帳戶也是有來源的第二條曲線。前份摘要沒有留下定為中等的理由。滲透率來源是次級資料，這是此判斷的弱點。","evidence_level":"低至中","settle_metric":"第三方線上滲透率資料（事實表未涵蓋精確值）","if_then":["若取得一手滲透率且超過 35%，跑道改回中等。"],"evidence_refs":[]},{"axis":"情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：樂觀 25%、悲觀 30%、最大回撤 −50%。","side_b":"本次：樂觀 20%、悲觀 30%、最大回撤 −35% 至 −60%。","ruling":"樂觀機率下調 5 點，因為 Q3 沒看到利潤率拐點且管理層不給目標；悲觀機率維持 30%。最大回撤由單點改成範圍，深端用 FY1 共識打九折推算。","evidence_level":"中","settle_metric":"營業利益率與 FY2 共識 EPS","if_then":["若連 2 季營益率低於 6.3%，悲觀機率升到 40%，不建倉。"],"evidence_refs":[]},{"axis":"建倉門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"分母止穩（雙口徑任一先成立）：Q3 2026 營業利益率 ≥8.0%（領先），或 FY+1 共識 EPS 連 2 個月不再下修（確認）；觸發後首階 1/3 分批建倉","side_b":"Q4 2026 或 Q1 2027 任一季營業利益率≥8.0%，且財報後 FY2 共識 EPS 連 2 個月不下修；觸發後重跑研究，首階 1/3 分批建倉","ruling":"前份建倉條件沒有觸發：Q3 營益率 6.3%，FY1 共識近三個月下修 2.52%。新條件把「或」改成「且」，因為財報後共識快照沒動，單靠沒有下修可能只是賣方還沒更新。","evidence_level":"高","settle_metric":"單季營業利益率與 FY2 共識月度快照","if_then":["兩項都成立，重跑研究後首階 1/3 分批建倉。","只成立一項，不建倉。"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未留存唯一致命點（空值）。","side_b":"FY2027 全年 GAAP 營業利益率沒有回到 8.0% 以上。","ruling":"敏感度試算顯示終端利潤率是最大單一變數，所以把它定成可驗證的二元事件；若發生，持有者減碼至半倉。","evidence_level":"中","settle_metric":"FY2027 全年 GAAP 營業利益率","if_then":["若 FY2027 營益率低於 8.0%，放棄建倉，持有者減碼至半倉。","若達 8.0% 以上，維持首階部位，達 10% 才可加碼。"],"evidence_refs":[]},{"axis":"利潤率門檻（破壞時減碼）","cause":"新證據","prior_field":["thesis.H2"],"side_a":"FY27 營益率 ≥10%；任一季 <6.0% 或連 4 季不升 ＝ 破壞","side_b":"FY27 營益率≥8.0% 算驗證，≥10% 才算收割；任一季低於 6.0% 或連 4 季不升仍算破壞，持有者減碼至半倉","ruling":"舊的 10% 高於共識隱含的約 8%，沿用會把符合共識的結果也判成失敗。破壞線不放寬。這是放寬驗證線，不代表論點變強，8% 到 10% 之間只准維持首階部位，不加碼。","evidence_level":"中：8% 由第三方 EPS 換算。","settle_metric":"FY2027 全年與單季營業利益率","if_then":["若任一季營益率低於 6.0%，持有者減碼至半倉。","若 FY27 營益率≥10%，可加碼至完整部位。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"營益率止穩且共識不再下修，才重新評估建倉","type":"估值rearm","maps_to":"H2","metric":"單季 GAAP 營業利益率＋FY2 共識 EPS","threshold":"Q4 2026 或 Q1 2027 任一季≥8.0%，且財報後 FY2 共識 EPS 連 2 個月不下修","action":"重跑研究後首階 1/3 分批建倉","source_freq":"公司 8-K 每季；Koyfin 快照每月","date":"2027-02","evidence_refs":[]},{"n":2,"text":"巴西飛輪是否繼續放大","type":"假設驗證","maps_to":"H1","metric":"巴西 FX 中性 GMV 年增、每買家件數年增、3P 抽成","threshold":"GMV 年增≥25% 連 2 季，件數為正，抽成不低於 Q2 2026 減 50bp（Q3 抽成值資料缺口）","action":"未達標則不建倉","source_freq":"公司季報與電話會議，每季","date":"2027-02","evidence_refs":[]},{"n":3,"text":"信貸能否維持風險調整後利差","type":"假設驗證","maps_to":"H3","metric":"NIMAL、15 至 90 天逾期率、90 天以上逾期率","threshold":"NIMAL≥20% 連 2 季，15 至 90 天≤8.0%，90 天以上不連 3 季上升（Q3 值資料缺口）","action":"未達標則不建倉","source_freq":"8-K 與 10-Q，每季","date":"2027-02","evidence_refs":[]},{"n":4,"text":"競爭侵蝕成長且利潤未恢復","type":"風險","maps_to":"R1","metric":"巴西 FX 中性 GMV 年增＋營業利益率","threshold":"GMV 年增連 2 季低於 25%，且營益率低於 7%","action":"護城河方向改為↓，不建倉，持有者清倉","source_freq":"公司季報，每季","date":null,"evidence_refs":["competitive_share_entrants#0","end_markets#2"]},{"n":5,"text":"FY2027 營益率沒有回到 8.0%","type":"Single Thing","maps_to":"H2","metric":"FY2027 全年 GAAP 營業利益率","threshold":"低於 8.0%","action":"放棄建倉，持有者減碼至半倉","source_freq":"FY2027 財報，每年","date":"2028-02","evidence_refs":[]},{"n":6,"text":"投資期拖長，暫時性說法失效","type":"減碼","maps_to":"R3","metric":"單季 GAAP 營業利益率","threshold":"Q4 2026 與 Q1 2027 連 2 季低於 6.3%，或任一季低於 6.0%","action":"持有者減碼至半倉，未持有者不建倉","source_freq":"公司 8-K，每季","date":"2027-05","evidence_refs":["end_markets#1","capital_markets_pricing#1","channel_business_model_shift#2"]},{"n":7,"text":"信貸逾期超過容忍線","type":"減碼","maps_to":"R2","metric":"15 至 90 天逾期率","threshold":"連 2 季高於 8.0%","action":"持有者減碼至半倉，未持有者不建倉","source_freq":"8-K，每季","date":null,"evidence_refs":["major_events#1"]},{"n":8,"text":"信貸與利差同時崩壞","type":"清倉","maps_to":"R2","metric":"15 至 90 天逾期率＋NIMAL","threshold":"15 至 90 天≥9.0%，且 NIMAL 低於 15%","action":"清倉","source_freq":"8-K，每季","date":null,"evidence_refs":["major_events#1"]},{"n":9,"text":"股價續跌但基本面沒有受損","type":"加碼","maps_to":"H1","metric":"股價＋三項基本面條件","threshold":"股價低於 1,200 美元，巴西 GMV 年增≥25%，15 至 90 天逾期率≤8.0%，FY2 共識累計下修不超過 10%（不低於 50.3 美元）","action":"分批反買首階 1/3","source_freq":"收盤價每日；基本面每季","date":null,"evidence_refs":[]},{"n":10,"text":"股價先反彈但利潤率證據未到","type":"風險","maps_to":"H2","metric":"股價與營業利益率","threshold":"站回 250 週均線 1,596 美元上方，營益率仍低於 8.0%","action":"不追","source_freq":"週線與每季財報","date":null,"evidence_refs":[]},{"n":11,"text":"匯率與政策衝擊吸收失敗","type":"風險","maps_to":"R4","metric":"美元營收成長與 FX 中性成長差、營業利益率","threshold":"美元成長低於 FX 中性成長 10 個百分點以上連 2 季，且營益率同步下滑","action":"不建倉，持有者減碼至半倉","source_freq":"公司 8-K，每季","date":null,"evidence_refs":["reg_tariff_export#0","regulatory_antitrust#1"]},{"n":12,"text":"證券訴訟進度，目前只有律所徵求","type":"風險","maps_to":"R2","metric":"訴訟程序里程碑","threshold":"正式提告、集體認證且不利和解；或出現刑事介入","action":"集體認證且不利和解則持有者減碼至半倉；刑事介入則清倉","source_freq":"法院文件與公司 10-Q 法律程序揭露，每季","date":null,"evidence_refs":["lawsuit_class_action#0","major_events#1"]},{"n":13,"text":"Q4 2026 財報後重跑研究","type":"複審日期","maps_to":"H2","metric":"全部門檻","threshold":"Q4 2026 財報公布","action":"重跑研究並更新門檻狀態","source_freq":"一次性","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"FY2027 全年 GAAP 營業利益率","bear_threshold":"低於 8.0%；任一單季低於 6.0%","window":"FY2027","source":"公司 8-K","last_status":"warning"},{"metric":"巴西 FX 中性 GMV 年增","bear_threshold":"連 2 季低於 25%","window":"滾動 2 季","source":"公司季報與電話會議","last_status":"ok"},{"metric":"NIMAL","bear_threshold":"連 2 季低於 20%；低於 15% 視為嚴重","window":"滾動 2 季","source":"公司 8-K","last_status":"warning"},{"metric":"15 至 90 天逾期率（全組合）","bear_threshold":"連 2 季高於 8.0%","window":"滾動 2 季","source":"公司 8-K","last_status":"ok"},{"metric":"90 天以上逾期率","bear_threshold":"連 3 季上升","window":"滾動 3 季","source":"公司 10-Q（Q3 值資料缺口）","last_status":"unknown"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"這筆證據只有 FY2024 年報的制式風險揭露，沒有服務中斷事件、合約變動或成本數字，無法形成可檢驗的判斷。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-7.5, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"Q4 2026 或 Q1 2027 任一季營業利益率≥8.0%，且財報後 FY2 共識 EPS 連 2 個月不下修；觸發後重跑研究，首階 1/3 分批建倉","exec_line":"現在不建倉、不加碼，等 Q4 2026 財報。持有者維持現有部位，不因跌價攤平。觸發後首階 1/3，其餘 2/3 綁 FY2027 上半年營益率維持 8.0% 以上才解鎖。"},"reasoning":{"industry":"Q3 營收 107.5 億美元，年增 45%（FX 中性 41%）。商務約 61.4 億美元（總營收減金融自算），年增 47.2%；金融 46.1 億美元，年增 42.5%，兩塊都超過營收一成。廣告年增 58%、信貸組合年增 62%、收單年增 42%，這些業務的獲利被管理層拿去補貼商務。Q3 營益率 6.3%，九個月 6.6%，去年同期 11.5%；調整後 EBITDA 只年增 5%。近四季毛利率 42.02%，FY2023 是 50.24%。單點依賴：巴西是成長最快的市場，信貸風險也集中在巴西與阿根廷；客戶端沒有集中問題，單一客戶占營收都不到 5%。信貸組合在 8-K 口徑是近 180 億美元，電話會議說 190 億美元，差異事實表未核對。公司沒有給數字指引。","moat":"機制是商務、物流、支付、信貸互相餵資料與流量，新對手要同時複製四塊。同業投入資本報酬率事實表未涵蓋，改用份額與利潤率。支持擴大的證據：巴西件數年增 45%、每件成本下降、信貸年增 62% 下 15 至 90 天逾期率穩定在 7%。支持縮減的證據：毛利率 FY2023 50.24%、FY2024 46.09%、FY2025 44.5%、近四季 42.02%，營益率由 FY2025 的 11.08% 降到近四季 7.42%，抽成與免運門檻都往下調。Shopee 所屬集團近四季營益率 8.24%，已略高於 MELI，期間差一季。MELI 自稱在每個主要市場拿份額，這點沒有第三方數字；會議摘要指出退縮的是本地零售商，所以 MELI 與 Shopee 可能同時成長。競爭壓力只記在威脅等級，不再從方向重複扣分。可能看錯的地方：若讓利一停份額就掉，執行力的進步其實是補貼買來的，方向應改為↓。","growth":"成長以量為主：巴西件數年增 45%、每買家件數年增 16%，單價往下走；併購與回購沒有貢獻。共識三年 EPS 年複合 25.9%（FY2025A 39.4 到 FY2028E 78.56，EPS 家數事實表未涵蓋）。內生上界因缺投入資本算不出來，缺口無法量化；已知 FY27 共識營收年增 29.5%、EPS 年增 46.1%，差額要靠利潤率回升。營運槓桿為負：Q3 營收年增 45%，營業利益由次級來源的去年 9.8% 利益率推算約年減 7%，差距遠超 3 個百分點，已列入成長熄火的壓力測試。滲透率證據是次級來源，這是跑道判斷的弱點。","governance":"報表 FCF 利潤率近四季 31.81%，看起來比 Amazon 和 Shopee 都好，但這個數字沒有扣信貸投入，和公司調整後 FCF 差距過大，不能當股東現金。調整後 FCF Q3 為 2.85 億美元，約營收 2.7%；Q2 為 2.14 億美元，已吸收資本支出 4.41 億與信貸投入 21 億美元（CFO，2026-08-05）。Q3 資本支出 5.03 億美元，去年同期 3.57 億。融資端 2025-12 發行 7.5 億美元 4.900% 2033 債，2026-09 發行 10 億美元 5.850% 2036 債。淨負債 87.86 億美元含租賃。長期留任計畫為現金結算，Q3 約 7,000 萬美元，相當於營業利益 10.4%。現金去向四分、債務到期結構與加權利率事實表未涵蓋。","valuation":"FY27 共識 EPS 年增 46.1%，FY28 再增 40.6%。用 Q3 淨利對營業利益比約 0.66 換算（Q3 EPS 8.83 來自第三方摘要），FY27 共識隱含營益率約 8%。基本情境 FY27、FY28 EPS 取 50、66 美元，比共識低約 11% 與 16%，原因是管理層明言投資哲學不變。短期目標：FY27 EPS 50×32 倍＝1,600 美元，上行 6.0%。中期目標：FY29 EPS 86×27 倍＝2,322 美元，上行 53.8%。賣方目標價約 2,166 至 2,259 美元，是 8 月初財報前的數字，今年已由 2,878 美元一路下修，高低比 1.71 倍，不用來支持進場。同業倍數事實表未涵蓋。","premortem":"假設衝擊：FY31 淨利率±1 個百分點，EPS±20.7 美元，目標價±497 美元（16%）；FY31 營收±10%，目標價±312 美元（10%）；終端倍數±1 倍，目標價±130 美元（4%）。利潤率是最大敏感項。成長熄火壓力：FY28 後年增降到 15%、10%、5%，FY31 EPS 約 100.4、87.8、76.4 美元，配 22、18、13 倍，價格約 2,209、1,580、993 美元，對現價 +46%、+5%、−34%，五年不虧本的有兩種。悲觀情境的地板不穩：FY1 共識近三個月下修 2.52%，財報後可能再降，所以正不對稱比率不作進場依據。衰退信號亮 1 項（毛利率），3 項資料不足，亮燈數可能低估。"},"plain":{"six":{"how_it_makes_money":"賺的是拉美賣家抽成、運費、廣告和收單的錢，再加上信貸利差；目前利潤卡在運費與行銷這一節，錢被拿去換買家頻次。","moat":"護城河方向為→：執行力擴大，定價力縮減，淨效果穩定，但兩邊的證據都不乾淨。","growth":"五年後跑道仍寬：線上滲透低雙位數，信貸與投資帳戶是已經在跑的第二條曲線。","capital":"資本配置以內部再投資為主，不發股息，股權幾乎沒有稀釋；真正的問題是資金越來越多流向信貸與倉儲，回報要兩三年後才看得到。","valuation":"現價要求 FY27 EPS 年增 46%，等於營益率回到約 8%；方向可信，時點不信，結論是合理但還不便宜。","how_wrong":"最可能看錯的地方，是把競爭逼出來的讓利當成自願投資，或反過來低估這筆投資的回報。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 Q4 2026 財報（預計 2027 年 2 月）或 Q1 2027 財報：任一季營業利益率≥8.0%，且財報後 FY2 共識 EPS 連 2 個月不下修。股價再跌不構成單獨進場理由，低於 1,200 美元且三項基本面條件都過才分批反買。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":1510.0,"week26_return_pct":-7.5,"consensus_rev_3m_pct":-2.52,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY1 EPS 38.26 被投資壓低，FY2 共識 55.89 又假設回升。Q3 財報後兩份共識快照沒有變動，FY1 近三個月已下修 2.52%，第三方摘要顯示 Q3 EPS 8.83 低於共識 9.27（未對照一手來源），下修可能還沒反映完。FY2 若下修 15% 至約 47.5 美元，現價對應約 32 倍。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報（月份依 FY2025 年報 2 月下旬提交推估）","impact":"高","watch":"營業利益率是否回到 8.0%，擴倉成本是否如 CFO 所說部分回補"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"Q1 2027 財報（月份依今年 5 月 7 日公布推估）","impact":"高","watch":"FY2 共識修正、15 至 90 天逾期率、90 天以上逾期率"},{"date":null,"date_precision":null,"type":"regulatory","event":"巴西工時由 44 小時逐步降到 40 小時，時程事實表未涵蓋","impact":"中","watch":"物流用工與一般管理費占營收比"}],"_projected_from":"v19"}
```
