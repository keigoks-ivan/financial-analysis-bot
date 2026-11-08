你是 stock-analyst v20 的**散文層（prose）agent**，標的 ALAB（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：ALAB　日期：2026-11-08　archetype：None　前份裁決：2026-10-13　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1413B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（525B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1001B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1459B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1048B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（742B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（690B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2429B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3517B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2097B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（278B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1413           3911-5587      5 條（2–6 內）  
s3                  8000         525           5232-7475      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3508          8044-11492      5 條（2–6 內）  
s6                 11000         742          7181-10258      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         690           1967-2810      5 條（2–6 內）  
s10                 5000        2429           1800-2571      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2097           2000-2903      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         278            855-1222      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5036B；至少需散文≈39.96KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70%
−65%
−65
−63%
−45%
−45
−38.3%
−4.54
0
0%
0.2
0.69
0.75
0.80
0.87
0.92
1
1.09
1.1%
1.16
1.21
1.22
1.29
1.3
1.32
1.38
1.44
1.5%
1.6
1.62
1.64
1.66
1.7%
2
02
2%
3
03
4
4%
04
4.39
4.4%
4.63
4.70
4.7
5
05
5%
5.3
5.30
5.4
5.9
5.90
06
6%
6
6.39
6.94
7
7.00
8.00
8
08
8.61
8.8
8.80
8.9%
9
09
10%
10
10.1%
10.1
10.3
10.7
11
11.4
12.0%
12
12.5
12.7%
12.8
13%
14
14.0%
14%
14.8
15
15%
15.8
16
16.3%
18
18.5
20%
20
21%
21.4
22
22.1
23
24
25
25%
25.5%
26
27%
27.48
27.5
27.6%
28
29
29.2
29.2%
30
30%
31
31.7%
33.8%
35
36
36%
38%
38.3%
40%
40
40.0%
41%
42%
42
43.4
43.44
44%
44.7%
45%
45
48.5%
49
49%
52.2%
58%
60%
65%
65
65.2%
67.1%
68.5
68.8%
69.8
70%
70
71%
72%
72.4%
73.7%
73.9%
74%
74.7%
75%
75
75.69%
76.4%
78%
80
82.5%
84%
85
86%
100%
100
106
106.2
120
125.3
134.2
142
142.82
150%
150
154%
156
160
162
162.3
179.2
185
187
190.71
194
200
205
210
219.1
243.4
246
260
281.8
307
308.85
320
326
400
540
560
584.9
660
665
730
740
750
800
2025
2026
2027
2028
2030
2031
2033
20261108
1,000
2,000
2,960
3,350
3,354
8,000
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
{"meta":{"ticker":"ALAB","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Astera Labs"},"oneliner":"第三季營收 584.9M、第四季指引中點 740M，基本面仍在加速；股價較前份判斷跌 38% 後回到合理區，但 2027 年 EPS 站不站得住，要看最大客戶第一代平台放緩後新客戶能否接上。","thesis":{"H":[{"id":"H1","text":"Scorpio X 在最大客戶之外放量，第一代平台放緩後營收不出現斷層。","2y":"FY2027 營收達共識水準，且最大客戶外至少 2 家量產。","5y":null,"10y":null,"threshold":"FY2027 營收≥3,350M，最大客戶外 Scorpio X 量產客戶≥2 家。","source":"季度財報與法說、10-K 終端客戶揭露。","drift_rule":"TTM 偏離連 2 季≥5% 削弱，連 3 季≥10% 反轉。"},{"id":"H2","text":"每顆加速器內容價值逐代倍增，營益率守住 40% 以上。","2y":null,"5y":"FY2031 營收約 80 億美元、non-GAAP 營益率約 41%。","10y":null,"threshold":"下一代每顆加速器內容價值≥2,000 美元；FY2031 營收≥8,000M、non-GAAP 營益率≥40%。","source":"法說揭露的內容價值、季度財報。","drift_rule":"TTM 偏離連 4 季≥5% 削弱，連 6 季≥10% 反轉。"},{"id":"H3","text":"協定從 PCIe 轉向 UALink、銅轉向光之後，ALAB 仍保住 scale-up 插槽並拿到光學新市場。","2y":null,"5y":null,"10y":"scale-up 光學成為第二條主要營收線。","threshold":"2030 年 scale-up 光學營收≥20 億美元，約為管理層 400 億美元市場估計的 5%。","source":"法說產品線揭露、產業研究機構數據。","drift_rule":"跨 2 個年度低於進度削弱，跨 3 個年度反轉。"}],"R":[{"id":"R1","text":"最大客戶第一代平台放緩後，新平台與新客戶接不上，2027 年營收出現斷層。","h_ref":"H1","clock":"⚡","threshold":"第一季財測中點季減超過 20%，或連 2 季季減合計超過 15%。","evidence_refs":["capital_markets_pricing#3","customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R2","text":"毛利率與費用同時走差，營收達標但利潤率回落。","h_ref":"H2","clock":"🔥","threshold":"non-GAAP 毛利率連 2 季低於 70%，或營業費用率高於 30% 而營收年增低於 30%。","evidence_refs":["capital_markets_pricing#4"]},{"id":"R3","text":"Broadcom、NVLink 生態與多協定轉換吃掉 scale-up 插槽，銅轉光後重定時器被取代。","h_ref":"H3","clock":"🐢","threshold":"下一代每顆加速器內容價值未達 2,000 美元，或公開設計中 ALAB 插槽減少。","evidence_refs":["end_markets#3","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1","competitive_share_entrants#3"]},{"id":"R4","text":"製造與經銷集中台灣，晶圓供應或地緣事件中斷出貨。","h_ref":"H1","clock":"🐢","threshold":"10-Q 揭露晶圓不足造成出貨遞延，或台灣事件中斷出貨達一季。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#4"]},{"id":"R5","text":"出口管制與關稅影響需求或成本。","h_ref":"H2","clock":"🔥","threshold":"法說揭露出口許可或關稅影響當季營收 5% 以上，或毛利率因此下降 200bp 以上。","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3"]}],"single_thing":{"description":"最大終端客戶下一代加速器平台的 scale-up 交換器，多數插槽改由 Broadcom、NVLink 方案或自研承接。","why_fatal":"2025 年單一終端客戶占營收逾七成，第三季成長主力又是領先客戶的 X 系列量產；這是情境樹裡對 FY2028 EPS 影響最大的單一變數，Base 8.80 對 Bear 4.70。","if_happens":"FY2028 EPS 落向 4.70，股價按 16–18 倍看 75–85 美元，清倉。","how_monitor":"每季法說對下一代平台的表述、2026 年 10-K 終端客戶占比、Amazon 認股權證歸屬進度、最大客戶公開的新平台設計。","probability":"25%（12–24 個月），主觀估計：第二家客戶試產與多平台設計導入壓低機率，但管理層未揭露下一代插槽已拿到。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":27.48,"peg_fy2":0.69,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.22,"FY2026E":4.39,"FY2027E":6.94,"FY2028E":8.61},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識，EPS 家數事實表未涵蓋（營收共識 20–23 位分析師），與公司 non-GAAP 季度數字對得上（第二季 0.80、第三季 1.32、第四季指引中點 1.64）。FY2025A 1.22 是 GAAP 稀釋，事實表沒有 non-GAAP 年度值，口徑不同，不拿來算三年複合；共識成長用 FY2026E 到 FY2028E 兩年複合 40.0%。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"毛利率 73.9%、幾乎無負債、營收年增三位數，但單一終端客戶占比高，複利特徵要等第二家客戶量產才算驗證。"},"industry":{"clock_phase":"II","sd_verdict_source":"供需持久性：偏結構但帶週期性。Gartner、ASML、Wolfe 都指向吃緊延續到 2027–28，但這些證據講的是整體半導體與記憶體，不是 scale-up 交換器本身；管理層稱晶圓、電力、記憶體仍受限（2026-11-03）。","bargaining":{"up":"晶圓依賴台積電，10-K 列為單點風險，替代產能難以合理條件取得。","down":"最大終端客戶 2025 年逾七成營收，又以認股權證（最多 326 萬股、履約價 142.82 美元，對應最多 65 億美元採購，至 2033 年）綁定採購，議價權在客戶端。平均每年約 9 億美元，不到 FY2027 共識營收三成，是誘因不是採購承諾。","geo":"製造與主要經銷商在台灣；中國營收維持個位數占比（2026-08-04，Jitendra Mohan）。"},"profit_pool_dir":"五年利潤池占比事實表未涵蓋。方向上利潤往加速器與 scale-up 網路集中，ALAB 毛利率高於多數連線同業。","tam_table":[{"item":"scale-up 光學互連（2030）","value":"400 億美元，管理層估計，滲透率事實表未涵蓋"},{"item":"Taurus 市場（2030）","value":"超過 40 億美元，管理層 2026-08-04"},{"item":"Scorpio X 於 AWS 部署機會（2026–29）","value":"約 25 億美元，BofA 2026-05；第三季 Scorpio 年化已逾 10 億美元，此估計可能偏舊"},{"item":"五年營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"量產驗證過的交換器與重定時器組合加 COSMOS 軟體，讓客戶換供應商要重做系統驗證；Hypercast 與網內運算讓產品直接參與 AI 工作負載。","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"第三季 X 系列已出貨兩家客戶，第四季另有多家客戶排單，P 系列在兩家美國超大型雲端業者放量（2026-11-03 法說）；本包沒有來源顯示最大客戶份額下滑。第二家客戶仍在試產，方向只有部分驗證。","peer_na_reason":"同業與 ALAB 的投入資本事實表未涵蓋，無法算 ROIC 差距，改用毛利率、營益率與內容價值方向對照。","threats":[{"level":"🔴","text":"NVLink 生態與 Broadcom Scale-Up Ethernet 爭奪 scale-up 交換插槽，對手可能較易取得設計導入，CXL、UALink 仍在早期。","p":35,"evidence_refs":["end_markets#3","substitute_technology#1","competitive_share_entrants#1"]},{"level":"🟡","text":"Credo 在光學 DSP 持續拿份額，壓縮 ALAB 在主動電纜與光學的空間。","p":30,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"銅轉光與產品價格隨時間下降，2028 年後機櫃內重定時器可能被光學架構取代；管理層稱光學內容價值更高，尚無營收驗證。","p":25,"evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（僅方向判斷：上半年資本支出約 28M、占營收 4%；投入資本事實表未涵蓋，周轉率未算）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"客戶要解決的問題是加速器之間的高頻寬低延遲連線，付款者與決策者都是超大型雲端業者，需求明確；但目前的解法由 PCIe 走向 UALink 與其他協定，問題持久不代表 ALAB 現有解法持久。"},{"item":"決策層級","level":"🟡","text":"替代性在每一代平台的插槽層級決定。同一代內換供應商要重做系統驗證，轉換成本高；跨世代會重新比稿，最大客戶下一代的選擇尚未揭露。"},{"item":"價值鏈分配","level":"🟡","text":"毛利率 72% 以上顯示目前分得到價值，但買方極度集中且以認股權證換採購，NVIDIA 掌握關鍵互補品，最大客戶也有自研能力。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的零組件，沒有消費者或政治上的漲價天花板；監管面主要是出口管制與關稅，列在風險項處理。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"需要資本支出、折舊、營運資金變動與投入資本。事實表只有上半年營業現金流 162.3M 與自由現金流 134.2M，差額約 28M 為資本支出，不足以算增量報酬。真正的再投資走研發費用，過去 12 個月占營收 33.8%，帳面口徑的內生上界會失真。情境輸入把成長標為超過內生上界，是算不出上界時取保守一側的假設，不是算出來的結果。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","ALAB":73.89,"NVDA":74.67,"AVGO":68.77,"CRDO":67.07,"MRVL":52.21,"unit":"%"},{"metric":"營業利益率","ALAB":25.52,"NVDA":65.21,"AVGO":48.52,"CRDO":31.74,"MRVL":16.81,"unit":"%"},{"metric":"FCF 利潤率","ALAB":22.15,"NVDA":41.92,"AVGO":44.22,"CRDO":27.57,"MRVL":18.23,"unit":"%"},{"metric":"研發密度","ALAB":33.82,"NVDA":7.79,"AVGO":13.28,"CRDO":21.46,"MRVL":25.84,"unit":"%"}],"competitors":[{"name":"NVDA","gm":74.67,"om":65.21,"fcf_margin":41.92,"rd_intensity":7.79,"strategy_note":"NVLink Fusion 既是合作也是封閉生態的延伸，營益率 65.2%，資本量級遠大於 ALAB，是最難防的生態競爭者。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"strategy_note":"Scale-Up Ethernet 交換器與 PCIe Gen 6 重定時器直接重疊，營益率 48.5%，可用規模與客製晶片關係綁售。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"CRDO","gm":67.07,"om":31.74,"fcf_margin":27.57,"rd_intensity":21.46,"strategy_note":"在光學 DSP 與主動電纜拿份額，FCF 利潤率 27.6% 高於 ALAB，主要重疊在 Taurus 線。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"MRVL","gm":52.21,"om":16.81,"fcf_margin":18.23,"rd_intensity":25.84,"strategy_note":"毛利率 52.2% 較低，但與 Lumentum 的合併若成局，矽光整合會直接對準 ALAB 的光學新線。","period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"量價齊揚，量靠機櫃與叢集擴大，價靠世代升級與內容價值增加，沒有併購或回購貢獻。","runway_years":"事實表未涵蓋滲透率，無法算到 30% 的年數","runway_post_y5":"🟢","endo_ceiling_basis":"投入資本、折舊與營運資金變動事實表未涵蓋，內生上界算不出來，情境樹按超過上界的保守一側處理。","segments":[{"item":"Scorpio（AI 交換）","value":"第三季最大產品線，年化逾 10 億美元，X 系列超過 P 系列；第四季 P 系列預期維持雙位數季增"},{"item":"Aries（重定時器）","value":"第三季創紀錄，每升一代單價約升 20–30%，Gen 7 已發表"},{"item":"Taurus（主動電纜）","value":"800G 第三季開始量產，2030 市場逾 40 億美元（管理層）"},{"item":"Leo（記憶體控制器）","value":"Leo 2 已出試產量，2027 年中放量"},{"item":"光學、客製、Orion","value":"光學 2027 下半年、客製 2027 年底首批 2028 放量、Orion 2027 起；單機櫃內容逾 10 萬美元"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":true,"text":"第一季 76.4%、第二季 73.7%、第三季 72.4%、第四季指引約 72%，季季走低，都低於 2025 全年 75.69%；同季年比事實表未涵蓋。"},{"item":"核心市占近 12 個月縮減","lit":false,"text":"本包沒有份額下滑的來源。"},{"item":"EPS 成長高於營收成長逾 5 個百分點","lit":false,"text":"FY2027E EPS 增 58%，營收增 65%；FY2028 共識營收事實表未涵蓋。"},{"item":"FCF 對淨利低於 0.75 連 2 年","lit":false,"text":"FY2025 為 1.29 倍；FY2024 淨利為負，不適用。"},{"item":"SBC 占營收逾 5% 且逐年上升","lit":false,"text":"第二季 16.3%，遠高於 5%；逐年方向事實表未涵蓋，未亮燈但列監測。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，公司未回購也未配息，現金累積到 1.38B，沒有資本回饋可展開。"},"sbc":{"note":"第二季 SBC 占營收 16.3%；Amazon 認股權證最多 326 萬股，約為第四季稀釋股數的 1.7%。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"aiXscale 收購條款未揭露，尚無營收，無法計算已實現報酬。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"本包未見回購紀錄。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數 185M 到 187M，一季增 1.1%，年化約 4.4%，高於每年 1.5%；SBC 占營收 16.3%（第二季）。","grade":"不過"}]},"valuation":{"basis":"Forward P/E 與 PEG。12 個月上檔用 FY2027E Base 7.00 乘 30 倍得 210 美元，約 +10.1%；中期用 FY2028E Base 8.80 乘 28 倍得 246 美元，約 +29.2%。","tier":"高成長 AI 連線半導體","peers":{"expanded":false,"reason":"事實表同業表只有利潤率，沒有同業前瞻本益比，無法做倍數對照。"},"fwd_pe":43.44,"peg":1.09,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"相對前份 308.85 美元，價格降 38%、FY2027E 共識上升，估值由偏貴回到合理；但分母有爭議，便宜的說法不成立，只到合理。五年分位事實表未涵蓋（上市未滿三年，年度端點只有 1–4 點），不計算。","upside_short_pct":10.1,"upside_mid_pct":29.2},"trap_analysis":{"verdict":"🟡","label":"毛利率季季走低，其他衰退信號未亮"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2025 年單一終端客戶逾七成營收；CFO 說初始 Scorpio X 平台已完成大部分初始部署（2026-11-03），第二家超大型客戶仍在試產。","assumption":"最大客戶下一代平台的 scale-up 插槽仍由 Astera 拿到，或新客戶能補上缺口。","consequence":"FY2028 EPS 落向 4.70，五年價格約 106 美元，較現價跌 44%。這與唯一致命點是同一件事，兩處對帳一致。","ruling":"採納，列為最大風險，Bear 機率給 30%。","watch":"第一季財測、2026 年 10-K 終端客戶占比、最大客戶新平台公開設計。","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1","capital_markets_pricing#3"],"fact_refs":["f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"論點成功但股東經濟變差","evidence":"第四季營業費用指引 194–200M，較第三季 162M 再增約 21%，員工一年翻倍；毛利率由 76.4% 降到約 72%；管理層長期營業費用率約 30%；SBC 占營收 16.3%；Amazon 認股權證以股權換採購。","assumption":"營收成長能維持營業槓桿，新產品線不會稀釋利潤率，股數增幅放緩。","consequence":"營收達標但營益率回落到 40% 上下，稀釋年化約 4%，non-GAAP EPS 達標而每股實質價值落後。","ruling":"部分採納。Base 營益率只給 41%，低於第四季指引 45%；Orion 機櫃平台管理層稱會提高毛利，尚無數字，不採信。","watch":"non-GAAP 毛利率、營業費用率、稀釋股數季增幅。","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_kpi4_sbc","f_kpi7_q3_fy2026"]},{"view":"價格已反映太多","evidence":"下跌後過去 12 個月 P/S 仍 21.4 倍、FY2026E 本益比 43.4 倍，接近 GAAP 的 FY2027E 本益比約 36 倍。","assumption":"FY2028E 共識 8.61 大致成立，且終端倍數能守住 24 倍。","consequence":"若 2031 年 EPS 只到 Bear 5.90，即使倍數 24 倍也只有 142 美元，仍低於現價。","ruling":"反駁為主因：FY2028E 22.1 倍、要求的 2028 年後成長約 14%，價格不算透支；但前提是共識成立，故只給合理，不給便宜。","watch":"FY2028E 共識 EPS 是否跌破 8.00。","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_ps_current","f_fwd_pe_latest"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 308.85 → 本次 190.71（-38.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=308.85","side_b":"本次 price_at_dd=190.71","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 308.85 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 308.85 美元：Bull 價 665、Bear 價 120，五年期望值 +14.0%，基準年化 1.5%，不對稱比 1.6","side_b":"本次情境、股價仍用 308.85 美元：Bull 價 660、Bear 價 106.2，五年期望值 +12.7%，基準年化 1.7%，不對稱比 1.44","ruling":"先換情境、股價不動：五年期望值少 1.3 個百分點，基準年化多 0.2 個百分點。不對稱比由 1.6 變為 1.44。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 308.85 美元：五年期望值 +12.7%，基準年化 1.7%，不對稱比 1.44","side_b":"本次情境、股價 190.71 美元：五年期望值 +82.5%，基準年化 12.0%，不對稱比 4.63","ruling":"再換股價、情境不動：起點價下跌 38.3%，五年期望值多 69.8 個百分點，基準年化多 10.3 個百分點，不對稱比由 1.44 升到 4.63。合計五年期望值比前份多 68.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價下跌後的估值與部位結論","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份 308.85 美元，估值偏貴，結論為等待。","side_b":"本次 190.71 美元，估值回到合理；FY2027E 共識 6.94 高於前份門檻 6.39。","ruling":"估值結論改善來自價格。Bull 25%、Bear 30% 維持前份，第三季正反證據大致抵銷；Max DD 區間 −65% 至 −45%，比前份 −70% 淺，因為起點已低 38%。","evidence_level":"事實表價格與共識","settle_metric":"股價與 FY2027E、FY2028E 共識 EPS","if_then":["若股價續跌而第一季財測不低於第四季實績，分批反買","若股價先反彈超過 260 美元而第一季財測未出，不追"]},{"axis":"基本面欄位複核","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：訊號等級 B、陷阱風險中等、護城河向上、五年後跑道寬、品質複利成長、中循環。","side_b":"本次六欄都不變。第三季法說帶來正面證據（X 系列出貨兩家客戶、多家第四季排單、營收超過指引上緣），也帶來負面證據（初始平台部署大致完成、營業費用超指引、毛利率續降）。","ruling":"新證據沒有推翻任何一欄。分母爭議使訊號等級不因價格下跌而升級。","evidence_level":"2026-11-03 法說原話","settle_metric":"第一季財測與最大客戶外量產家數","if_then":["若 2027 年底最大客戶外仍無量產客戶，護城河方向下修為穩定，第三筆取消"]},{"axis":"首倉與加碼的重新評估條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價≤200美元且FY2027E共識EPS≥6.39；或最大客戶外≥2家Scorpio X量產且股價≤260美元；任一成立重跑判斷再定首倉","side_b":"第一季財測中點不低於第四季實績；或股價≤150 美元且 FY2028E 共識 EPS≥8.00；任一成立重跑判斷定下一筆","ruling":"前份第一支條件已成立（股價 190.71 不高於 200、FY2027E 共識 6.94 不低於 6.39），本次就是那次重跑。重跑結果是價格條件達成，但 FY2027、FY2028 EPS 仍有爭議，本次不建首倉，維持追蹤。首倉改綁第一季財測，因為決定性數據已經不是價格。","evidence_level":"事實表價格與共識","settle_metric":"第一季營收財測中點對第四季實績","if_then":["若第一季財測中點不低於第四季實績，重跑判斷定首筆，部位上限總資產 4%","若未達標，不建倉，續列追蹤"]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未留存清倉或減碼門檻。","side_b":"最大客戶外量產家數 2027 年底仍為 0、季營收連 2 季合計跌逾 15%、non-GAAP 毛利率連 2 季低於 70%、FY2028E 共識 EPS 跌破 7.00。","ruling":"前份摘要這一欄為空，本次新設清倉與減碼門檻，全部對應情境樹的 Bear 路徑。","evidence_level":"判斷設定","settle_metric":"四項門檻逐季對照","if_then":["毛利率連 2 季低於 70%，減碼到 2%","量產家數與營收兩項同時觸發，清倉"]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未留存唯一致命點。","side_b":"最大終端客戶下一代加速器平台的 scale-up 交換器，多數插槽改由 Broadcom、NVLink 方案或自研承接。","ruling":"Single Thing 本次新設，選它是因為它對 FY2028 EPS 的敏感度最大（Base 8.80 對 Bear 4.70）。","evidence_level":"法說與年報摘要，無客戶端確認","settle_metric":"最大客戶下一代平台供應商","if_then":["若證實多數插槽由他家或自研承接，清倉"],"evidence_refs":["customer_second_source#0"]},{"axis":"2027 上半年營收形狀","cause":null,"side_a":"管理層：初始 Scorpio X 平台已完成大部分初始部署，之後維持規模貢獻，新平台與新客戶在 2027 年陸續疊加（2026-11-03，Desmond Lynch）。","side_b":"賣方提問：最大客戶本世代建置 2027 年第一季見頂，下一代要到接近 2028（Barclays），Morgan Stanley 也問是否進入高原期；CFO 拒談客戶量。FY2027 共識營收僅比第四季年化高 13%。","ruling":"可調和，屬程度差異：第一代放緩與新平台接力可以同時成立，差別在缺口多大、多久。決勝數據是 2027 年 2 月的第一季財測，今天還不存在，風險未解，到那時才能裁決。","evidence_level":"管理層原話與賣方提問，無客戶端數據","settle_metric":"第一季營收財測中點對第四季實績","if_then":["若財測中點不低於第四季實績，加碼到總資產 4%","若季減超過 10%，停止加碼，等第二季財測","若季減超過 20% 且管理層未點名接力平台，減碼一半","若訊號證實放緩只是一季，第二季財測恢復季增，把第二筆補回"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"客戶集中度口徑","cause":null,"side_a":"10-K 客戶表：五家各占 10% 以上，最大 20%，合計約 84%。","side_b":"年報風險揭露與第三方彙整：單一終端客戶逾 2025 年營收 70%，前三大約 86%。","ruling":"可調和：合理解讀是前者為下單的直接客戶與經銷商，後者為實際用貨的終端客戶，投資判斷用終端口徑。兩份都是搜尋摘要轉述，未讀原文。第三季法說稱客戶更分散但沒給數字，而第三季成長主力是領先客戶的 X 系列，集中度可能不降反升。","evidence_level":"二手摘要","settle_metric":"2026 年 10-K 最大終端客戶占比","if_then":["若占比低於 60%，第二家客戶的論點算得到驗證","若高於 75%，取消第三筆加碼"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#0","geo_supply_chain#4"]},{"axis":"長期毛利率目標","cause":null,"side_a":"2026-08-04 法說摘錄：毛利率長期目標 78%（Desmond Lynch）。","side_b":"2026-11-03 法說 Susquehanna 提問用長期目標 70%，管理層未更正；實績由第一季 76.4% 走到第四季指引約 72%。","ruling":"兩個數字對不上，本包無法查原文，不採信 78%。情境樹用約 71%，配長期營業費用率約 30%，長期營益率約 41%，低於第四季指引 45%。","evidence_level":"法說摘錄與賣方提問","settle_metric":"下一次管理層對長期毛利率的明確表述","if_then":["若 non-GAAP 毛利率連 2 季低於 70%，減碼到 2%"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"管理層承諾對照","cause":null,"side_a":"2026-08-04：客製方案首批 2027、NPO 目標 2027 量產、Leo 2027 對兩家超大型客戶量產、UALink 版 Scorpio X 2027 交付；第三季營收指引 540–560M、營業費用 156–160M。","side_b":"2026-11-03：客製收窄為 2027 年底首批、2028 放量；NPO 營收 2027 下半年；Leo 放量 2027 年中；UALink 只說變化不大，未重申交付時點；第三季營收 584.9M 超過上緣，營業費用 162M 也超過上緣。","ruling":"短期財務指引守信，新產品時程尚未失約，但客製放量已後移。UALink 時點未重申，標為未證、監測。問答中另有未正面回答：2026-08-04 CFO 未回應 Amazon 認股權證對毛利率的影響，也未給當時每顆內容價值的具體數字；2026-11-03 CFO 拒談 2027 客戶量。","evidence_level":"兩場法說原話對照","settle_metric":"UALink 版 Scorpio X 的交付時點與客戶","if_then":["若連兩季未重申 2027 交付，內容價值倍增的 Base 假設下修，取消第三筆加碼"]},{"axis":"產業態勢三軸","cause":null,"side_a":"競爭：Broadcom、NVIDIA、Credo、Marvell 都在加碼，Marvell 與 Lumentum 整合矽光（2026-11-03 問答）。","side_b":"結構：AI 半導體短缺預期延續到 2027，ASML 產能賣到 2027，scale-up 走向多協定；其他結構變數是 2028 年後銅轉光與最大客戶自研能力。","ruling":"雙向拉鋸：需求面結構轉好，競爭同步變強，銅轉光是下一個結構變動點。","evidence_level":"第三方研究與賣方摘要","settle_metric":"下一代平台設計導入與 2028 年光學出貨","if_then":["若 2028 年光學營收占比仍低於 5%，H3 下修"],"evidence_refs":["end_markets#3","substitute_technology#1"]},{"axis":"現在就買與現在就賣的最強論證","cause":null,"side_a":"買：FY2028E 22.1 倍，第四季營收指引再季增 27%，FY1 共識三個月上修 8.9%，前份設定的價格與共識條件都已達成；10% 年報酬只需 2031 年 EPS 約 12.8 美元。","side_b":"賣：第一代平台放緩是 CFO 親口說的，逾七成終端營收集中一家，下一代插槽未定；股價跌 38% 而事實表沒有下跌原因，可能有本包未涵蓋的資訊。","ruling":"現在不買，維持追蹤：賠率夠但 FY2027、FY2028 EPS 未定，第一季財測才驗得出來。首筆綁第一季財測，後續部位綁第二家客戶量產。","evidence_level":"事實表與法說","settle_metric":"第一季財測","if_then":["若第四季財報前股價跌破 150 美元且 FY2028E 共識仍不低於 8.00，重跑判斷定首筆","若 FY2028E 共識跌破 7.00，取消首筆計畫，重跑判斷"]}],"triggers":[{"n":1,"text":"第一季財測驗證第一代平台放緩的幅度","type":"假設驗證","maps_to":"H1","metric":"第一季營收財測中點相對第四季實績","threshold":"不低於 0%","action":"加碼到總資產 4%","source_freq":"季度財報","date":"2027-02","evidence_refs":["capital_markets_pricing#3"]},{"n":2,"text":"最大客戶以外的 Scorpio X 客戶進入量產","type":"加碼","maps_to":"H1","metric":"最大客戶外 Scorpio X 量產客戶數","threshold":"至少 1 家","action":"加碼到總資產 6%","source_freq":"季度法說","date":"2027-08","evidence_refs":[]},{"n":3,"text":"第一季財測大幅季減且說不出接力平台","type":"減碼","maps_to":"R1","metric":"第一季營收財測中點相對第四季實績","threshold":"季減超過 20% 且未點名接力平台","action":"減碼一半，停止加碼","source_freq":"季度財報","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":4,"text":"最大客戶下一代平台插槽流失","type":"Single Thing","maps_to":"Single Thing","metric":"最大客戶下一代平台 scale-up 交換器供應商","threshold":"證實多數插槽由他家或自研承接","action":"清倉","source_freq":"事件驅動，法說與 10-K","date":"2027-12","evidence_refs":["customer_second_source#0"]},{"n":5,"text":"毛利率跌破管理層口中的長期區間","type":"風險","maps_to":"R2","metric":"non-GAAP 毛利率","threshold":"連 2 季低於 70%","action":"減碼到總資產 2%","source_freq":"季度財報","date":"2027-05","evidence_refs":["capital_markets_pricing#4"]},{"n":6,"text":"價格跌到 Bear 倍數附近而共識未破","type":"估值rearm","maps_to":"H1","metric":"股價與 FY2028E 共識 EPS","threshold":"股價≤150 美元且共識≥8.00","action":"分批反買","source_freq":"每日股價、月度共識","date":null,"evidence_refs":[]},{"n":7,"text":"第二家客戶沒有出現且營收下滑","type":"清倉","maps_to":"H1","metric":"最大客戶外量產家數與季營收","threshold":"2027 年底仍為 0 家且季營收連 2 季合計跌逾 15%","action":"清倉","source_freq":"季度財報","date":"2028-02","evidence_refs":[]},{"n":8,"text":"第四季財報後全面複審","type":"複審日期","maps_to":"H1","metric":"全套判斷","threshold":"第四季財報發布","action":"重跑判斷","source_freq":"季度","date":"2027-02","evidence_refs":[]},{"n":9,"text":"年報揭露的終端客戶集中度","type":"風險","maps_to":"R1","metric":"2026 年 10-K 最大終端客戶占比","threshold":"高於 75%","action":"取消第三筆加碼","source_freq":"年度 10-K","date":"2027-02","evidence_refs":["customer_concentration_credit#1"]}],"kill_metrics":[{"metric":"最大客戶外 Scorpio X 量產客戶數","bear_threshold":"2027 年底仍為 0 家","window":"至 2027-12-31","source":"季度法說","last_status":"ok"},{"metric":"季營收","bear_threshold":"連 2 季季減合計超過 15%","window":"2027 全年","source":"季度財報","last_status":"ok"},{"metric":"non-GAAP 毛利率","bear_threshold":"連 2 季低於 70%","window":"滾動 2 季","source":"季度財報","last_status":"warning"},{"metric":"FY2028E 共識 EPS","bear_threshold":"跌破 7.00","window":"未來 12 個月","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[{"ref":"supply_demand_durability#1","reason":"這則談 NAND 位元供需，ALAB 不賣 NAND，證據對象與公司產品不同，無法推導 scale-up 連線的需求。"},{"ref":"supply_demand_durability#5","reason":"這則只給晶圓產能增速，沒有需求或稼動率對照，單獨無法支持供過於求的結論。"}],"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把第一代平台放緩當成整條成長線見頂：第二家超大型客戶已在試產，第四季另有多家客戶排單，FY2027 共識只要求每季平均增約 5%。這是判斷不是證實，股價下跌的真正原因事實表未涵蓋，第一季財測才驗得出來。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='↑', week26=-4.54, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望","rearm_trigger":"第一季財測中點不低於第四季實績；或股價≤150 美元且 FY2028E 共識 EPS≥8.00；任一成立重跑判斷定下一筆","exec_line":"現價不建倉，維持追蹤：FY2027、FY2028 EPS 未定，等 2027 年 2 月第一季財測。財測中點不低於第四季實績，或股價≤150 美元且 FY2028E 共識 EPS≥8.00，才重跑判斷定首筆；財測未出前續漲不追。本文的 2%、4%、6% 是重跑後轉為可進場時的部位上限，不是現在的動作。"},"reasoning":{"industry":"公司只有一個報告部門，按產品線看：Scorpio 交換器第三季成為最大產品線，年化營收超過 10 億美元，X 系列已超過 P 系列；Aries 重定時器靠 PCIe Gen 6 續創新高；Taurus 800G 開始量產；Leo 記憶體控制器 2027 年中才放量（2026-11-03 法說，Jitendra Mohan、Desmond Lynch）。第三季營收 584.9M、季增 49%、年增 154%，non-GAAP 毛利率 72.4%、營益率 44.7%、EPS 1.32，營收與 EPS 都高於 8 月指引（540–560M、1.16–1.21）；第四季指引營收 730–750M、毛利率約 72%、營益率約 45%、EPS 1.62–1.66。單點依賴：2025 年單一終端客戶逾七成、前三大約 86%（年報摘要轉述，未讀原文），這同時是量產驗證的來源和最大的集中度風險。事實表的最新一季 KPI 停在第二季，第三季數字取自逐字稿。","moat":"優勢有兩層。一層是量產經驗：Scorpio X 有業界最大的 320 lane 配置，第三季出貨兩家客戶、多個平台。另一層是 COSMOS 軟體，從元件診斷擴到機櫃與網路管理，客戶換供應商要重做系統驗證。同業對照：過去 12 個月毛利率 73.9%，高於 AVGO 68.8%、CRDO 67.1%、MRVL 52.2%，接近 NVDA 74.7%；GAAP 營益率 25.5% 低於 CRDO 31.7%，因為研發占營收 33.8%，高於四家同業。ROIC 差距取不到，改看內容價值與毛利率：每顆加速器內容價值已超過 1,000 美元，下一代僅交換器就要再加 1,000 美元以上；毛利率卻從第一季 76.4% 降到第四季指引約 72%，部分來自 Amazon 認股權證的非現金影響，部分來自模組組合。所以執行面在擴大，定價力只算穩定。反例：若 2027 年底仍只有最大客戶量產，向上的方向就站不住。","growth":"成長來自量與價，沒有併購或回購撐。量：機櫃與叢集變大，附掛率提高；價：資料速率每升一代單價約升 20–30%（2026-11-03，Jitendra Mohan）。共識 EPS FY2026E 4.39、FY2027E 6.94、FY2028E 8.61，兩年複合 40.0%；FY2025 只有 GAAP 1.22，口徑不同，不算三年複合。FY2027 共識營收 3,354M 只比第四季指引中點年化 2,960M 高 13%，相當於每季平均增約 5%，共識已部分反映放緩。內生上界因投入資本與再投資數字事實表未涵蓋而算不出來，共識與內生上界的缺口無法歸因，因此加註依賴 re-rate，長期信心上限為中；但 Base 情境本益比由 43.4 倍收縮到 24 倍，五年報酬實際靠 EPS 複利。光學、記憶體、客製、機櫃平台四條線都有時程，全部還沒有營收，2027 年下半年才開始驗證。","governance":"第三季末現金及有價證券 1.38B，季增 125.3M，營業現金流 179.2M 創高，總債務 45M。FY2025 自由現金流 281.8M 對 GAAP 淨利 219.1M，轉換率 1.29 倍；第三季營業現金流只有 non-GAAP 淨利 243.4M 的 74%，放量期營運資金在吃現金。近三年現金去向四分事實表未涵蓋。SBC 第二季占營收 16.3%，稀釋股數由第三季指引 185M 升到第四季指引 187M，年化約 4.4%。管理層 2026-11-03 說員工一年翻倍，長期營業費用率約 30%。","valuation":"現價 190.71 對應 FY2026E 43.4 倍、FY2027E 27.5 倍、FY2028E 22.1 倍，EV 對 FY2026E 營收 15.8 倍。要有 10% 年報酬，五年後需 307 美元，以 24 倍算 FY2031 EPS 約 12.8 美元。這個推論建立在 FY2027、FY2028 共識成立之上，而這正是爭點。PEG 用 FY2026E 本益比 43.4 除以兩年複合 40.0% 得 1.09，FY2027E 口徑為 0.69。non-GAAP 排除的費用約占四分之一：第三季指引 GAAP EPS 0.87–0.92 對 non-GAAP 1.16–1.21，換算接近 GAAP 的 FY2027E 本益比約 36 倍。同業前瞻本益比事實表未涵蓋，只能以自身倍數對照。","premortem":"最可能看錯三處。第一，第一代平台放緩其實是下一代插槽流失的前兆，這是唯一致命點。第二，新產品線時程滑動，客製案已從 2027 收窄到年底並把放量放到 2028。第三，股價在兩次判斷之間跌 38%，事實表沒有下跌原因，可能存在本包未涵蓋的負面資訊。本包沒有訴訟、SEC 調查或重編紀錄。衰退信號只有毛利率一項亮燈，陷阱風險中等。歷史最大回撤事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺超大型雲端業者 AI 機櫃內連線的錢，錢卡在加速器之間的 scale-up 交換與訊號調節節點，量目前主要靠單一終端客戶撐住。","moat":"護城河在擴大，靠的是量產經驗與 COSMOS 軟體，定價力只算穩定；第二家客戶量產前，這個方向只有一家大客戶的驗證。","growth":"跑道寬，第二條 S 曲線有來源但還沒有營收，五年後的成長要靠 2027 下半年起的新客戶與新產品接力。","capital":"現金留在帳上投研發，沒有回購也沒有配息，稀釋偏高。","valuation":"現價要求 2031 年 EPS 約 12.8 美元才有 10% 年報酬，相當於 FY2028E 共識之後每年再長 14%，這個要求不高；問題是 FY2028E 共識本身還沒有定論。","how_wrong":"最可能看錯的是把最大客戶第一代平台放緩當成短暫停頓，結果下一代插槽丟失。"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把第一代平台放緩當成整條成長線見頂：第二家超大型客戶已在試產，第四季另有多家客戶排單，FY2027 共識只要求每季平均增約 5%。這是判斷不是證實，股價下跌的真正原因事實表未涵蓋，第一季財測才驗得出來。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":190.71,"week26_return_pct":-4.54,"consensus_rev_3m_pct":8.93,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2027、FY2028 EPS 取決於最大客戶第一代平台放緩的幅度和第二家客戶接力的速度：FY2027 Bull 8.00、Base 7.00、Bear 5.30，差距大到本益比便宜的論證不能用，判斷改看 FY2031 的 EPS 區間。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與第一季財測，管理層也承諾補充 Orion 對損益的影響","impact":"高","watch":"第一季營收財測中點對第四季實績"},{"date":"2027-06","date_precision":"month","type":"product","event":"Leo 2 量產放量（管理層稱 2027 年中）","impact":"中","watch":"兩家超大型客戶是否如期出貨"},{"date":"2027-09","date_precision":"month","type":"product","event":"NPO 光學元件與多家 Scorpio X 客戶開始貢獻營收（2027 下半年）","impact":"高","watch":"最大客戶外量產家數"},{"date":"2027-12","date_precision":"month","type":"product","event":"客製方案首批出貨（管理層稱 2027 年底）","impact":"中","watch":"是否再往後延"}],"_projected_from":"v19"}
```
