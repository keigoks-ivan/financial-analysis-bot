你是 stock-analyst v20 的**散文層（prose）agent**，標的 3081.TWO（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

每章 3–6 條，每條 100–200 字；s10（估值與三種未來）與 s12（最可能怎麼賠）至少 1,500 bytes，把情境輸入、終端倍數、反證三視角的裁定鋪開。

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

標的：3081.TWO　日期：2026-11-08　archetype：None　前份裁決：2026-10-12　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1361B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（416B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（869B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1153B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1180B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（219B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（651B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2265B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3194B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2643B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1361           3947-5639      5 條（2–6 內）  
s3                  8000         416           5309-7584      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3202          8259-11798      5 條（2–6 內）  
s6                 11000         219          7547-10781      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         651           1994-2849      5 條（2–6 內）  
s10                 5000        2265           1914-2735      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2643           2000-2357      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4098B；至少需散文≈40.90KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−85
−85%
−84%
−77%
−66%
−65%
−65
−43.1%
−42.1%
−40.2%
−26.4
−24.8
−15.0%
−14.3
−14.3%
−5.1%
−5%
−4.79
−2.1
−1.6%
0
0.02%
0.09
0.1
0.171
0.171%
0.29
0.4
0.7
0.75
0.87
1
01
1.4
1.46
1.5%
1.5
1.6
1.6%
2
2%
2.2
2.5
2.9
03
3
3%
3.2
3.45%
3.94
4
4.21
4.28
4.62
5%
5
06
6
6.27
6.6
6.8
7
8
08
09
9
9.8
10%
10
10.9%
11
12
12%
12.21
13%
13.08%
13.9
14
15
15%
15.8
16
17%
17.5
18
20
20.6
21%
21
21.26
21.72%
22.1%
22.5
22.5%
22.7
23%
23.35%
24
25
25%
26
28
28.0
28.01
29.16
30%
30
31
31.7
32
33.7
34%
35%
35
37
37.27%
37.39
38.6
39.4
40.72
41.5
42%
42
42.1%
42.98
43
43.3
44
44%
45
45%
45.91%
46.3
46.9%
47
49
49.2
50%
50
52
54.9
55%
55
55.99%
56
57.45%
60
60%
61%
70
71%
74%
77
80%
80
82.4
82.7
84.95
85
85%
88
90%
90
92.5
92.52
97
97.7%
100
100%
101.2
101.4
103
104
111.54
114%
122
150%
165
188
211%
288
400
468
468.5
469
484
600
800
900
906
1750.0
2023
2024
2025
2026
2027
2028
2030
2455
3025.0
3081
20261108
1,316
1,344
1,380
1,425
1,500
1,619
1,720
1,750
2,000
2,400
2,440
3,025
3,136
3,600
3,904
4,140
4,500
6,300
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
{"meta":{"ticker":"3081.TWO","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"聯亞光電"},"oneliner":"資料中心矽光帶動的 InP 磊晶缺貨股。一個月跌 42% 後，現價約等於機率加權價值，仍要 FY2027 獲利翻倍且 2028 年後毛利率不崩才站得住。等約 1,425 元且單季毛利率守住 50% 再談進場。","thesis":{"H":[{"id":"H1","text":"2027 年產能放大能兌現成獲利，FY2027 營收與 EPS 接近共識。","2y":"FY2027 營收 ≥90 億元、EPS ≥35 元","5y":null,"10y":null,"threshold":"FY2027 營收 ≥90 億元且 EPS ≥35 元（共識 101.2 億元、40.72 元）","source":"公開資訊觀測站月營收與季報，法說的產能進度","drift_rule":"TTM 營收對本路徑連 2 季偏離 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"},{"id":"H2","text":"新產能到位後毛利率守得住，證明不是單純的缺貨行情。","2y":null,"5y":"FY2029 至 FY2031 年度毛利率 ≥45%","10y":null,"threshold":"年度毛利率 ≥45%（Q2 2026 為 57.45%，2023 年為 13.08%）","source":"季報與年報","drift_rule":"連 4 季低於門檻 5 個百分點以上為削弱，連 6 季低於 10 個百分點以上為反轉"},{"id":"H3","text":"開放式 InP 磊晶片龍頭地位與客戶廣度維持，3.2T 順利接棒。","2y":null,"5y":"開放式磊晶份額 ≥50%，客戶 ≥10 家，3.2T 進入量產","10y":null,"threshold":"份額 ≥50%（目前單一報告稱逾 60%）且客戶 ≥10 家","source":"Digitimes 等產業報告、公司法說","drift_rule":"連 4 季未見 3.2T 量產或客戶數下降為削弱，連 6 季份額資料低於 50% 為反轉"}],"R":[{"id":"R1","text":"InP 基板斷料：中國出口管制延續，庫存緩衝原本只看到 2026 年第三季。","h_ref":"H1","clock":"⚡","threshold":"單季營收季減 ≥10% 且公司歸因基板，或單季毛利率 <50%","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2","geo_supply_chain#2"]},{"id":"R2","text":"新產能與自製同時到位：同業擴產、IDM 自行供應磊晶，矽光滲透慢於預期。","h_ref":"H2","clock":"🔥","threshold":"磊晶片報價轉跌，或單季毛利率連 2 季年減","evidence_refs":["cyclical_supply_discipline_capacity#3"]},{"id":"R3","text":"上一輪下行重演：中國電信客戶幾乎消失時，月營收年減 74%，毛利率落到 13%，連兩年虧損。","h_ref":"H2","clock":"🔥","threshold":"月營收連 3 個月年增低於 30%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R4","text":"客戶與地區集中：2025 年底三家客戶占應收帳款 74%，銷售市場中國占 71%。","h_ref":"H3","clock":"🔥","threshold":"前三大客戶占應收 ≥80%，或出現主要客戶轉第二來源的報導","evidence_refs":["customer_concentration_credit#0"]},{"id":"R5","text":"擴產資金壓力：Q2 自由現金流 −4.79 億元，設備預算約 82.7 億元，高於帳上現金 49.2 億元。","h_ref":"H1","clock":"🔥","threshold":"淨現金轉為淨負債，或股本年增 ≥5%","evidence_refs":[]}],"single_thing":{"description":"任一季毛利率跌破 45%，而當季營收仍年增，代表是價格鬆動，不是需求消失。","why_fatal":"終端 EPS 對毛利率最敏感：FY2031 Base 營收約 165 億元，毛利率每少 5 個百分點，稅後少約 6.8 億元，EPS 少約 6.6 元，約占 12%。同時市場會改用循環股倍數，Base 的 24 倍往 Bear 的 18 倍靠。","if_happens":"已持有者清倉；未持有者取消進場條件，等毛利率連兩季回升再重做研究。","how_monitor":"每季財報毛利率、每月營收、基板與磊晶片報價的產業報導。","probability":"12–24 個月內約 25%"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":42.98,"peg_fy2":3.94,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":4.21,"FY2026E":20.6,"FY2027E":40.72,"FY2028E":null},"fy_end_month":12,"eps_basis":"FY2025A 為 yfinance 稀釋 EPS，FY2026E、FY2027E 為 yfinance 分析師共識平均；FY2028 共識事實表未涵蓋，留空，不自行推估。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"2023、2024 連兩年虧損；毛利率由 13.08% 到 57.45%，擺幅約 44 個百分點；Q2 資本支出占營收 61%。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉，約在 2028 年前後。依據 TrendForce 的新產能時程與公司法說的 2027 年產能指引。","bargaining":{"up":"上游 InP 基板吃緊，已漲三次，第四季考慮再漲逾一成。住友電工 2026–2030 年長約降低斷料風險，是否鎖價事實表未涵蓋。","down":"缺貨期由聯亞議價，磊晶片已漲兩次。客戶增至 10 家以上，但 2025 年底三家客戶占應收帳款 74%。","geo":"2025 年銷售市場中國占 71%、美國 21%。基板受中國出口管制影響，美系雲端直接訂單是分散的方向。"},"profit_pool_dir":"缺貨期利潤往 InP 磊晶與雷射環節集中，五年利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"TAM、SAM、滲透率與利潤池占比事實表都未涵蓋，只有 800G 以上出貨量由 2,400 萬增至 6,300 萬一筆二手資料，組不成表。"}},"moat":{"mechanism":"開放式 InP 磊晶片的量產規模與客戶驗證週期。單一市場報告稱開放式市場份額逾 60%，未經第二來源確認。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定：1.6T 已量產、3.2T 驗證中，客戶由 7–8 家增至 10 家以上，住友基板長約到位。定價權穩定：現在能漲價，但 2023 年毛利率 13.08%，看不出跨週期定價權。TTM 毛利率領先 LITE 約 10 個百分點、營業利益率領先約 21 個百分點；同業 ROIC 差距與歷史趨勢事實表未涵蓋，所以不標擴大。","peer_na_reason":"IQE.L 無季度財報資料，Coherent 不在同業表內。","threats":[{"level":"🟡","text":"IDM 自行供應磊晶，加上同業擴產，壓縮開放式磊晶的份額與價格。目前只有賣方提示，沒有具體客戶轉自製的報導。","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"InP 基板受中國出口管制影響，庫存緩衝原本只看到 2026 年第三季。","p":"25%","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2","geo_supply_chain#2"]},{"level":"🟡","text":"客戶與地區集中，三家客戶占應收帳款 74%，銷售 71% 在中國，少數客戶改單就會直接影響營收。","p":"25%","evidence_refs":["customer_concentration_credit#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"需求真實，Lumentum 稱出貨短缺客戶需求逾 30%，800G 以上出貨量大增。付款者集中在雲端資本支出，少數決策點就能延後採購。"},{"item":"決策層級","level":"🟡","text":"1.6T 已量產、3.2T 驗證中，換供應商要重新驗證，有黏著度。合約年限、重新認證週期與漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"缺貨期聯亞拿到高分配，毛利率 55.99% 高過 LITE 的 45.91%。上游基板連續漲價，下游有擴產與自製能力，這個分配不穩固。"},{"item":"社會容忍度","level":"🟢","text":"企業間零組件，沒有消費者定價壓力；公平會處分 0 筆，反競爭訴訟損失為 0。出口管制另列為供應風險。"}],"roiic":25,"reinvest_rate":90,"endo_ceiling":22.5,"formula_note":"單位為百分比，皆為估算。投入資本與折舊事實表未涵蓋，象限由 Q2 資本支出占營收 61%、自由現金流為負推定。增量 ROIC：設備預算約 82.7 億元（近三季公告近 60 億元加上限 22.7 億元）。低案用共識 FY2027 較 FY2026 新增營收 46.3 億元×稅後 30%＝13.9 億元，得 17%；高案用產能 2.5 倍滿載新增 82.4 億元×稅後 34%＝28.0 億元，得 34%，取中間約 25%。再投資率：TTM 營收以市值 1,619 億元÷P/S 37.39 反推約 43.3 億元，自由現金流約 1.5 億元，稅後營業利益約 15.8 億元，1−0.09≈90%。內生上界＝25%×90%＝22.5%。90% 的再投資率難維持五年，此上界偏樂觀。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","3081.TWO":55.99,"2455.TW":37.27,"IQE.L":null,"LITE":45.91,"unit":"%"},{"metric":"營業利益率","3081.TWO":44.48,"2455.TW":21.72,"IQE.L":null,"LITE":23.35,"unit":"%"},{"metric":"FCF 利潤率","3081.TWO":3.45,"2455.TW":7.31,"IQE.L":null,"LITE":9.52,"unit":"%"},{"metric":"研發密度","3081.TWO":5.34,"2455.TW":10.55,"IQE.L":null,"LITE":12.47,"unit":"%"}],"competitors":[{"name":"2455.TW","gm":37.27,"om":21.72,"fcf_margin":7.31,"rd_intensity":10.55,"strategy_note":"TTM 截至 2026-06，毛利率 37.27%、營業利益率 21.72%，獲利能力差聯亞一截。期間比聯亞早一季，比較略偏向聯亞有利。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"IQE.L","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表沒有財務數字，無法比較。"},{"name":"LITE","gm":45.91,"om":23.35,"fcf_margin":9.52,"rd_intensity":12.47,"strategy_note":"雷射同業，TTM 毛利率 45.91%、營業利益率 23.35%，都低於聯亞。雷射產能據稱訂到 2028 年，短期印證需求，長期是擴產與自製的對手。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主、價為輔，無併購與回購貢獻。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 25%×再投資率 90%＝22.5%，推導見護城河段；缺口歸因為利潤率擴張。","segments":[{"item":"DataCom（矽光為大宗）","value":"約 80–85%"},{"item":"Telecom","value":"約 5–10%"},{"item":"其他","value":"約 5%"}],"decay_signals":[{"item":"EPS 成長顯著高於營收成長","value":"亮燈：共識 FY2025–FY2027 EPS 年化 211%，營收年化 114%，差 97 個百分點。"},{"item":"自由現金流對淨利低於 0.75 倍連兩年","value":"未亮但要盯：FY2025 為 1.46 倍，TTM 約 0.1 倍，再一個年度低於門檻就亮燈。"},{"item":"其餘八類","value":"未亮或事實表未涵蓋，市占變化、維護性資本支出與產業倍數趨勢都查無資料。"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，回購資料查無，股息殖利率 0.171% 不影響估值結論。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月重大訊息未見併購事件，沒有可評估的併購報酬。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購紀錄事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q2 SBC 906 萬元，年化約 3,600 萬元，約占市值 0.02%，低於每年 1.5% 的上限。","grade":"過"}]},"valuation":{"basis":"FY2027 共識本益比。循環股的股價淨值比與同業倍數事實表未涵蓋。","tier":"高成長循環零組件","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，不能用不同口徑的數字當錨。"},"fwd_pe":42.98,"peg":3.94,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價約為 FY2027 共識 EPS 的 43 倍，機率加權五年價值約 1,720 元，沒有安全邊際，所以仍偏貴；相較上份約 77 倍已明顯回落，降一檔。五年分位事實表未涵蓋，只有年度端點。PEG 用 FY2027 本益比 42.98 倍除以 Base FY2027–FY2031 年化 10.9%。若用共識 FY2026 到 FY2027 成長 97.7% 計算 PEG 為 0.87，那是產能爆發的一次性跳升，不採用。短期目標 1,500 元＝FY2028 Base EPS 50 元×30 倍；中期目標 1,316 元＝FY2029 Base EPS 47 元×28 倍。","upside_short_pct":-14.3,"upside_mid_pct":-24.8},"trap_analysis":{"verdict":"🟡","label":"成長是真的，價格用的是缺貨期利潤率"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2023 年毛利率 13.08%、EPS −2.1 元，2024 年續虧；賣方提示 IDM 自行供應磊晶與矽光滲透慢於預期。","assumption":"新產能到位後毛利率仍守在 45% 以上。","consequence":"五年後虧損過半最可能的路徑是 2028 年起價格鬆動，毛利率往 30% 走，EPS 16–26 元、18 倍，股價約 468 元。與唯一致命點同一件事。","ruling":"採納，列 30% 機率。上一輪是中國電信客戶消失，這一輪換成雲端客戶，型態不同，但少數客戶決定營收的結構相同。","watch":"單季毛利率、磊晶片報價、月營收年增率。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_supply_discipline_capacity#3"],"fact_refs":["f_kpi1"]},{"view":"論點失敗","evidence":"股價 10-12 到 11-06 由 3,025 元跌到 1,750 元，期間有 10-28 第三季財報。基板庫存原本只看到 2026 年第三季。","assumption":"FY2027 共識 EPS 未下修，由前份門檻換算約 39.4 元升至 40.72 元，所以跌的是倍數。共識快照可能落後實際。","consequence":"若實際原因是基板斷料或毛利率下滑，本次所有路徑都偏高。","ruling":"不可裁決，要到補讀第三季財報與法說才能定。補讀前不做任何進場動作。","watch":"第三季單季毛利率、10 月至 12 月營收、公司對基板供應的說明。","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2","geo_supply_chain#2"],"fact_refs":["f_earnings_recency","f_price_at_dd","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Q2 自由現金流 −4.79 億元，設備預算約 82.7 億元，現金 49.2 億元、債務 31.7 億元。基板再漲逾一成。","assumption":"擴產資金來自營業現金流，股本不擴大。","consequence":"營收照預期翻倍，股東仍可能因增資或可轉債稀釋而少賺；每股路徑還受股數口徑 92.5 到 101.4 百萬股的影響。","ruling":"採納部分。Base 股數已用約 103 百萬股，若再對外籌資，每股路徑要下修。","watch":"淨現金、股本變動、籌資公告。","evidence_refs":["end_markets#3","cyclical_supply_discipline_capacity#0"],"fact_refs":["f_kpi4","f_net_debt_m","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"現價約為 FY2027 共識 EPS 的 43 倍、trailing 111.54 倍，P/S 37.39 倍在 4 個年底端點中最高。","assumption":"一個月跌 42% 已提供足夠保護。","consequence":"機率加權五年價值約 1,720 元，低於現價，Base 年化約 −5%，跌幅沒有轉成安全邊際。","ruling":"採納。跌幅只修正了上份的過高定價，還沒補償 30% 的 Bear 路徑。","watch":"股價對 FY2027 共識 EPS 的倍數。","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_pe_current","f_ps_current","f_ps_percentile","f_consensus_eps_fy2"]}],"max_dd":{"lo":-85,"hi":-65,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 3025.0 → 本次 1750.0（-42.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=3025.0","side_b":"本次 price_at_dd=1750.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 3,025 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 3,025 元：Bull 價 4,140、Bear 價 484，五年期望值 −40.2%，基準年化 −14.3%，不對稱比 0.4","side_b":"本次情境、股價仍用 3,025 元：Bull 價 3,904、Bear 價 468，五年期望值 −43.1%，基準年化 −15.0%，不對稱比 0.29","ruling":"先換情境、股價不動：五年期望值少 2.9 個百分點，基準年化少 0.7 個百分點。不對稱比由 0.4 變為 0.29。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 3,025 元：五年期望值 −43.1%，基準年化 −15.0%，不對稱比 0.29","side_b":"本次情境、股價 1,750 元：五年期望值 −1.6%，基準年化 −5.1%，不對稱比 1.4","ruling":"再換股價、情境不動：起點價下跌 42.1%，五年期望值多 41.5 個百分點，基準年化多 9.8 個百分點，不對稱比由 0.29 升到 1.4。合計五年期望值比前份多 38.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"缺貨延續與循環晚期的時間窗","cause":null,"prior_field":null,"side_a":"TrendForce 等來源稱 InP 短缺延續到 2027 年之後，Lumentum 據稱雷射產能訂到 2028 年。","side_b":"毛利率 57.45% 為事實表四個年度內最高，Coherent 將兩度倍增產線，聯亞 2027 年產能放大 2.5 倍，2023 年毛利率曾落到 13.08%。","ruling":"可調和，屬時間窗差異。2027 年以前採信缺貨，2028 年以後採信供給回補，所以 Base 在 FY2029 回落，Bear 機率維持 30%。","evidence_level":"中，缺貨多為二手轉述，歷史財務為一手資料。","settle_metric":"單季毛利率與磊晶片報價。","if_then":["若 2027 年底前單季毛利率仍 ≥55% 且磊晶片續漲，Bear 機率下調至 25%","若任一季毛利率跌破 45%，已持有者清倉，未持有者取消進場條件"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#5","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"一個月跌 42%，RSI 28.01，股價貼著 52 週線且在 104 週線之上。FY2027 共識本益比由約 77 倍降到約 43 倍，共識 EPS 沒有下修。Bull 五年 3,904 元，約為現價 2.2 倍。","side_b":"現價略高於機率加權價值約 1,720 元，Base 年化約 −5%。下跌原因與 10-28 財報內容都不在手上，不能把跌幅當安全邊際。","ruling":"選等價位。超賣只說明賣壓，不說明價值。本判斷比賣方悲觀，但認為目前股價大致合理，不主張市場看錯。","evidence_level":"中，第三季資料缺口未補。","settle_metric":"第三季單季毛利率與 FY2027 共識 EPS。","if_then":["價格先走、證據未到：股價回到 2,000 元以上而第三季毛利率仍未確認，不追","跌到約 1,425 元以下且單季毛利率 ≥50%，重做研究後分批反買，首倉不超過 3%","反向條件：股價未跌到 1,425 元，但 FY2027 共識 EPS 上修至 55 元以上且毛利率 ≥55%，重做情境樹，進場價按 35 倍上移"],"evidence_refs":["capital_markets_pricing#2","end_markets#4"]},{"axis":"賣方目標價與本判斷","cause":null,"prior_field":null,"side_a":"Investing.com 10 位分析師平均目標價 3,136 元，最高 4,500 元、最低 900 元，最新評等動作在 8 月。","side_b":"本判斷 Base 五年 1,344 元，機率加權約 1,720 元。","ruling":"分歧在框架層。平均目標價約等於 FY2027 共識 EPS 的 77 倍，等於把缺貨期利潤率當常態，再給成長股倍數。高低目標價相差 5 倍，快照也早於這波下跌，不拿來當支撐。","evidence_level":"低，快照日期不明，TradingView 另一組 469 元疑為過期資料。","settle_metric":"FY2027 共識 EPS 與實際毛利率。","if_then":["若賣方在第三季財報後下修 FY2027 EPS 逾 10%，Base 路徑同步下移，進場價按 35 倍重算"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：IDM 自製與 Coherent、Lumentum 擴產，壓力在 2027 年後上升。","side_b":"結構：資料中心矽光需求推動 InP 短缺，客戶數增至 10 家以上。其他：基板出口管制與報價上漲。","ruling":"雙向拉鋸。需求結構轉好與未來供給增加同時成立，目前證據不足以判哪邊先到。","evidence_level":"中。","settle_metric":"客戶數、磊晶片報價、自製相關報導。","if_then":["若 2027 年客戶數低於 10 家或傳出主要客戶自製，改判競爭惡化中，Bull 機率降到 15%"],"evidence_refs":["cyclical_supply_discipline_capacity#3","competitive_share_entrants#0","supply_demand_durability#3"]},{"axis":"估值結論因股價下跌而改善","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：3,025 元，約 FY2027 共識 EPS 77 倍，估值最貴一檔，Bull 25%、Bear 30%、最大回撤 −85%。","side_b":"本次：1,750 元，約 43 倍，估值降一檔到偏貴，Bull 25%、Bear 30% 不變，最大回撤範圍 −85%～−65%。","ruling":"改善全部來自價格，基本面假設沒有變，所以機率不動。","evidence_level":"高，價格與共識為事實表數字。","settle_metric":"股價對 FY2027 共識 EPS 的倍數。","if_then":["若股價回到 FY2027 共識 EPS 60 倍以上（約 2,440 元），估值回到最貴一檔，已持有者減碼一半"],"evidence_refs":[]},{"axis":"基本面判斷維持不變","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：觀望，循環晚期，護城河穩定，五年後空間中等，陷阱風險中等。","side_b":"本次資料：Q2 毛利率 57.45%，FY2027 共識 EPS 由約 39.4 元升至 40.72 元，客戶數增至 10 家以上，2027 年產能 2.5 倍；同時 Q2 自由現金流為負，第三季內容缺漏。","ruling":"新證據方向互抵，沒有一項足以改判，這八欄全部維持。循環位置看毛利率與供給，不看股價，所以跌 42% 不會讓位置提前。","evidence_level":"中。","settle_metric":"第三季毛利率與 2027 年產能進度。","if_then":["若第三季毛利率低於 50%，陷阱風險升到最高一檔並重做研究"],"evidence_refs":["competitive_share_entrants#0","cyclical_supply_discipline_capacity#0"]},{"axis":"重新進場門檻（首倉進場）更新","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,380 元）且單季毛利率仍 ≥50%","side_b":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,425 元）且單季毛利率仍 ≥50%","ruling":"倍數與毛利率條件不變，只因 FY2027 共識 EPS 上升，換算進場價上移約 45 元。前份門檻至今未觸發，現價 1,750 元仍高出新門檻約 23%。","evidence_level":"高。","settle_metric":"收盤價、FY2027 共識 EPS、單季毛利率。","if_then":["達到新門檻時先重做研究再分批進場，不直接建倉"],"evidence_refs":[]},{"axis":"Single Thing 與清倉指標首次明列","cause":"方法變動","prior_field":["single_thing","kill_metrics"],"side_a":"前份摘要此欄為 null，無原文。","side_b":"任一季毛利率跌破 45%，而當季營收仍年增。","ruling":"前份摘要沒有這兩欄可比，本次新訂，無法判斷是否比前份放寬。","evidence_level":"不適用。","settle_metric":"單季毛利率。","if_then":["發生時已持有者清倉，未持有者取消進場條件"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"補讀 10-28 的第三季財報與法說，確認毛利率、基板供應與這波下跌的原因。","type":"假設驗證","maps_to":"H1","metric":"2026 年第三季單季毛利率","threshold":"≥50% 維持現有判斷，<50% 重做研究","action":"補齊資料前不做任何進場動作","source_freq":"公開資訊觀測站季報，一次性","date":"2026-11-30","evidence_refs":["cyclical_inventory_price_position#2"]},{"n":2,"text":"股價回到 FY2027 共識 EPS 35 倍以下，且單季毛利率仍在 50% 以上。","type":"估值rearm","maps_to":"H2","metric":"股價÷FY2027 共識 EPS；單季毛利率","threshold":"≤35 倍（約 1,425 元）且毛利率 ≥50%","action":"重做研究後分批反買，首倉不超過 3%","source_freq":"收盤價每日，毛利率每季","date":null},{"n":3,"text":"下半年營收要達到全年共識所需的水準。","type":"假設驗證","maps_to":"H1","metric":"2026 下半年累計營收","threshold":"≥33.7 億元（全年共識 54.9 億元減上半年 21.26 億元）","action":"低於門檻則下調 FY2027 Base EPS 並重算進場價","source_freq":"月營收，每月","date":"2027-01-10"},{"n":4,"text":"任一季毛利率跌破 45%，而當季營收仍年增。","type":"Single Thing","maps_to":"Single Thing","metric":"單季毛利率","threshold":"<45% 且當季營收年增","action":"已持有者清倉，未持有者取消進場條件","source_freq":"季報，每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"n":5,"text":"基板斷料影響出貨。","type":"風險","maps_to":"R1","metric":"單季營收季增率與公司對基板的說明","threshold":"季減 ≥10% 且公司歸因基板","action":"已持有者減碼一半，未持有者不進場","source_freq":"月營收與法說","date":null,"evidence_refs":["supply_demand_durability#3","geo_supply_chain#2"]},{"n":6,"text":"擴產資金轉為對外籌資或淨現金轉負。","type":"風險","maps_to":"R5","metric":"淨現金與股本變動","threshold":"淨現金 <0，或股本年增 ≥5%","action":"每股路徑按新股本下修，已持有者停止加碼","source_freq":"季報與重大訊息","date":null},{"n":7,"text":"股價回升到過高倍數而毛利率沒有再上行。","type":"減碼","maps_to":"H2","metric":"股價÷FY2027 共識 EPS；單季毛利率","threshold":"≥60 倍（約 2,440 元）且毛利率未創新高","action":"已持有者減碼一半","source_freq":"收盤價每日，毛利率每季","date":null},{"n":8,"text":"3.2T 量產與客戶廣度驗證。","type":"假設驗證","maps_to":"H3","metric":"3.2T 量產進度與客戶家數","threshold":"2027 年底前未量產，或客戶低於 10 家","action":"Bull 機率由 25% 降到 15%","source_freq":"法說，每季","date":"2027-12-31"},{"n":9,"text":"FY2026 年報與第四季法說後複審。","type":"複審日期","maps_to":"H1","metric":"全份判斷","threshold":"屆期必做","action":"重跑情境樹並更新進場價","source_freq":"年報","date":"2027-03-31"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"<45%","window":"任一季","source":"公開資訊觀測站季報與法說","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"<35 元","window":"3 個月內","source":"yfinance 分析師共識","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連 3 個月 <30%","window":"連續 3 個月","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"淨現金","bear_threshold":"<0","window":"連 2 季","source":"季報資產負債表","last_status":"ok"},{"metric":"2027 年產能倍數","bear_threshold":"<2 倍（指引 2.5 倍）","window":"2027 年底前","source":"公司法說","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":"首倉不超過 3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=-26.4, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,425 元）且單季毛利率仍 ≥50%","exec_line":"未持有：不追，等約 1,425 元且單季毛利率 ≥50%，重做研究後分三批進場。已持有：不加碼，反彈到約 2,440 元減碼一半，單季毛利率跌破 45% 清倉。"},"reasoning":{"industry":"Q2 2026 營收 12.21 億元，毛利率 57.45%，營業利益率 46.9%。DataCom 占 80–85%，以矽光為大宗，電信 5–10%。供需判斷是週期性將反轉，時間點約在 2028 年前後：短缺目前是真的，但 Coherent 報導將兩度倍增 InP 產線，聯亞自己 2027 年產能也放大 2.5 倍，供給回得來。產業位置判第三階段（過熱），依據是毛利率為事實表四個年度內最高，上下游同時漲價與擴產。單點依賴屬於風險：矽光是最大產品，2025 年銷售 71% 在中國，三家客戶占應收帳款 74%。單一客戶營收占比事實表未涵蓋。10-28 公布的第三季財報內容也未涵蓋，單季數字最新只到 Q2。","moat":"當期 ROIC 算不出，因為投入資本與折舊事實表未涵蓋。持續期四項檢查是三項中等、一項良好：需求真實但付款者集中，客戶驗證有黏著但合約年限未知，聯亞毛利率高過客戶級同業，反而提高對方自製的誘因。新增資本報酬估約 25%，再投資率約 90%，內生成長上界約 22.5%。毛利率領先 LITE 約 10 個百分點，但這是缺貨期的讀數，同業 ROIC 差距與歷史趨勢都查無，所以不標擴大。反例是 2023 年毛利率 13.08%，當時需求一消失，定價能力也跟著消失。","growth":"現階段成長是量為主、價格助攻，沒有併購與回購。共識 FY2025 到 FY2027 EPS 年化 211%，營收年化 114%，差 97 個百分點來自利潤率擴張與低基期。第三年共識事實表未涵蓋，三年年化算不出。內生上界 22.5%，共識兩年年化與上界相差約 188 個百分點，歸因為利潤率擴張與產能利用率回升，不是再投資複利，不能外推。Base 路徑 FY2026E 到 FY2031E 年化 22.1%，在上界以內。滲透率事實表未涵蓋；3.2T 與 CPO 是下一段需求的來源，但沒有量化時程，不足以判寬。","governance":"FY2025 自由現金流 6.27 億元，是淨利 4.28 億元的 1.46 倍。TTM 截至 2026-09 的自由現金流利潤率只剩 3.45%，對淨利約 0.1 倍；Q2 單季為 −4.79 億元。SBC 占營業利益 1.6%，年化約占市值 0.02%，不是問題。淨現金 17.5 億元（現金 49.2 億元、債務 31.7 億元），對約 82.7 億元設備預算不夠，差額要靠未來營業現金流或對外籌資。近三年現金去向、債務到期結構與回購紀錄事實表未涵蓋。","valuation":"現價對 FY2026 共識 EPS 約 85 倍，對 FY2027 約 43 倍，trailing 111.54 倍，前瞻 EV/S 29.16 倍。P/S 與 EV/S 在 4 個年底端點中都是最高。情境樹 Bull 3,904 元、Base 1,344 元、Bear 468 元，機率加權約 1,720 元，比現價低約 2%。上份 3,025 元時約 77 倍，估值改善全部來自股價下跌。循環股本應看股價淨值比，但事實表未涵蓋；同業倍數也未涵蓋。","premortem":"偏多看錯的路徑：2028 年新產能與自製同時到位，毛利率往 2023 年的方向走。偏空看錯的路徑：3.2T 與 CPO 放量早於預期，缺貨延長，毛利率維持 55% 以上，Bull 的 3,904 元約為現價 2.2 倍，此時等 1,425 元會買不到。最大的資料缺口是 10-12 到 11-06 跌 42% 的原因，期間包含 10-28 的第三季財報，內容事實表未涵蓋。歷史最大回撤序列與放空方數字也未涵蓋。"},"plain":{"six":{"how_it_makes_money":"聯亞賺資料中心光模組與雲端業者的錢，錢卡在 InP 磊晶片與 CW 雷射的產能這一節。","moat":"護城河穩定，評 B 級，來自開放式 InP 磊晶的份額與客戶驗證，看不出跨週期的定價權。","growth":"五年後仍有成長，但空間只能判中等：份額已高，下一段需求要靠 CPO，時程沒有數字。","capital":"資金全押在擴產，回饋股東不是重點，風險在設備預算大於帳上現金。","valuation":"現價 1,750 元要求 FY2027 獲利翻倍，而且 2028 年後毛利率不崩。前半我相信，後半現在不值得先付錢。","how_wrong":"成長是真的，風險在價格用的是缺貨期的利潤率，而這波大跌的原因我手上沒有。"}},"decision_inputs":{"signal":"C","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"追蹤","wait_for_price":true,"wait_for_price_condition":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,425 元）且單季毛利率 ≥50%；達到後先重做研究再分批。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":1750.0,"week26_return_pct":-26.4,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2027 EPS 40.72 元建立在缺貨期利潤率與產能 2.5 倍上，用它得出 43 倍不能當便宜的論據。股數也有疑義：事實表 92.52 百萬股，由 Q2 淨利 468.5 百萬元÷EPS 4.62 元反推約 101.4 百萬股，差約一成，市值與 EV/S 可能低估約一成，本益比不受影響。"},"catalysts":[{"date":"2026-11-10","date_precision":"month","type":"other","event":"10 月營收公告，為第四季第一個數據點","impact":"中","watch":"年增率與月增率，對照下半年 33.7 億元的需求"},{"date":"2026-12-31","date_precision":"quarter","type":"other","event":"InP 基板第四季是否再漲逾一成，磊晶片是否第三度漲價","impact":"中","watch":"漲價能否完全轉嫁，毛利率方向"},{"date":"2027-03-31","date_precision":"quarter","type":"guidance","event":"FY2026 年報與第四季法說","impact":"高","watch":"毛利率、2027 年產能進度、資本支出與籌資安排"},{"date":"2027-12-31","date_precision":"quarter","type":"capacity","event":"2027 年產能達 2026 年 2.5 倍的指引驗收","impact":"高","watch":"實際產能倍數、產能利用率、報價是否鬆動"},{"date":null,"date_precision":null,"type":"product","event":"3.2T 進入量產，公司未給時程","impact":"中","watch":"法說揭露的客戶驗證進度"}],"_projected_from":"v19"}
```
