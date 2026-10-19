你是 stock-analyst v20 的**散文層（prose）agent**，標的 3037.TW（2026-10-19）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261019/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：3037.TW　日期：2026-10-19　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1222B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（380B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1005B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1167B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1014B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（472B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（644B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1964B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3478B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1812B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1222           4045-5778      5 條（2–6 內）  
s3                  8000         380           5334-7620      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3186          8270-11814      5 條（2–6 內）  
s6                 11000         472          7370-10528      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         644           1999-2856      5 條（2–6 內）  
s10                 5000        1964           2125-3036      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1812           2000-3188      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4299B；至少需散文≈40.70KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−275
−164
−111
−78%
−78
−70%
−60
−60%
−18
−16
−0.4%
0
0.18
0.38
0.4
0.5%
0.75
1
01
2
3%
3
4
4.34
4.43%
5%
5
5.4
06
6
07
7
7.4
7.7%
08
8
8.45
09
9
9%
10
10%
10.12%
10.24%
11.6
12
12%
12.27%
12.3
13
13.9%
13.94%
14%
14
15
15%
15.5%
16
16.04%
16.4
17.96%
18
19
19.5%
19.85%
20%
20
20.7
21
21%
22
22%
23%
23.26%
24
24%
24.8%
25%
26%
26
28%
28.42%
29
29%
29.3
30%
30
32%
33
35%
35
35.9%
36
38.22
40%
40
42%
42
45
45%
46
46%
48
49
50
50%
51%
52%
52
54
54.1
62.74
63.3
64.7%
65%
65
65.5%
65.53
66
70
70%
73
74%
74.9
76
80
82
85%
88
89
90
100
100%
131
143%
150%
153
330
340
428.9
429
468
537
625.6
686.8
765
803.36
1120.0
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
3037
3189
4062
8046
20261019
1,120
1,200
1,312.4
1,490
1,500
2,711
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
{"meta":{"ticker":"3037.TW","date":"2026-10-19","schema":"v15.2","contract":"v19","company_name":"欣興電子"},"oneliner":"欣興是 AI 高階 ABF 載板龍頭，供需缺口推升報價與毛利率；但現價已按高於2022前高的利潤率定價，又有產地標示刑案與2027年起同業擴產兩道風險，報酬風險比偏差，等回檔。","thesis":{"H":[{"id":"H1","text":"ABF 供需缺口延續到2027年，報價續漲，毛利率守住新高區","2y":"2027年底前單季毛利率維持24%以上","5y":null,"10y":null,"threshold":"單季毛利率≥24%（Q2 2026 為24.8%）","source":"公司季報、法說會","drift_rule":"單季毛利率連2季低於22%為削弱；連3季低於20%為反轉"},{"id":"H2","text":"AI 產品占比提升，讓這一輪循環的谷底利潤率高於上一輪","2y":null,"5y":"2029–2031年年度營益率谷底≥12%（上一輪谷底為2024年的4.43%）","10y":null,"threshold":"年度營益率谷底≥12%；AI 產品營收占比≥65%","source":"年報、法說會 AI 營收占比","drift_rule":"TTM 營益率連4季低於門檻5%以上為削弱；連6季低於門檻10%以上為反轉"},{"id":"H3","text":"537億元擴產能在兩年內回收，轉為正自由現金流","2y":"FY2027 自由現金流轉正，利潤率≥5%","5y":null,"10y":null,"threshold":"FY2027 自由現金流利潤率≥5%（TTM 為−0.4%）","source":"年報與季報現金流量表","drift_rule":"TTM 自由現金流利潤率連2季低於5%為削弱；連3季為負為反轉"}],"R":[{"id":"R1","text":"產地標示刑案升級為起訴、美國海關扣貨或客戶啟動合規條款，高階客戶轉向第二供應商","h_ref":"H1","clock":"⚡","threshold":"起訴公司法人，或任一主要美系客戶公開導入第二供應商","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","major_events#0","lawsuit_class_action#0","competitive_share_entrants#1"]},{"id":"R2","text":"同業與欣興自身的新產能在2027下半年至2029年集中開出，供需反轉，重演2023年的毛利率下滑","h_ref":"H2","clock":"🔥","threshold":"單季毛利率季減3個百分點以上連2季，或報價季減","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","competitive_share_entrants#2","cyclical_supply_discipline_capacity#2"]},{"id":"R3","text":"執行面失誤：AI HDI 良率偏低、折舊上升、工安停工拖累毛利率，重演2024年第二季的情況","h_ref":"H3","clock":"🔥","threshold":"單季毛利率低於24.8%，且公司歸因於良率、停工或折舊","evidence_refs":["capital_markets_pricing#2","major_events#1","cyclical_prior_downcycle_behavior#2"]}],"single_thing":{"description":"高階 ABF 載板報價出現首次季減，宣告這一輪漲價循環結束","why_fatal":"共識 FY2027–2028 EPS 要靠高於2022前高的淨利率；上一輪循環反轉時，營收一年減26%、毛利率掉16個百分點。報價是盈餘最大的單一敏感項，倍數也會跟著壓縮","if_happens":"清倉，等循環位置回到深谷或早循環再重跑研究","how_monitor":"每季法說會的報價說法與毛利率；月營收年增率；景碩、IBIDEN 2027下半年新產能的開出進度","probability":"20%"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":29.3,"peg_fy2":0.4,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":4.34,"FY2026E":20.7,"FY2027E":38.22,"FY2028E":62.74},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識取 Koyfin 美元值，依2026-10-08匯率換算為新台幣"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261019/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"毛利率高低點擺動超過20個百分點（2022年35.9%→2025年13.9%），資本支出占營收結構性高於15%"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：法人估 ABF 缺口2027年約21～25%、2028年約36～42%，但同業新產能2027下半年到2029年陸續開出，供給可逆性高","bargaining":{"up":"上游 T-glass、銅箔、鑽針短缺，材料商議價力上升","down":"賣方市場；客戶簽3～7年長約並預付款","geo":"ABF 產能全部在台灣；PCB 有中國四個廠加泰國新廠，產地標示爭議集中在 PCB"},"profit_pool_dir":"現階段利潤往載板廠移動","tam_table":{"expanded":false,"reason":"事實表未涵蓋 ABF 市場規模與欣興份額時間序列；供需缺口只有第三方估計，已寫在成長題"}},"moat":{"mechanism":"高階 ABF 載板良率加客戶認證週期，配合3～7年長約與預付款鎖量","execution":6,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價力在擴大：2026年多次調漲、下半年再漲，法人估漲幅10～15%，Q2 毛利率由17.96%升到24.8%。執行面在縮減：2026年8月產地標示刑案；法人指客戶可能認證更多供應商；美系外資指 AI HDI 初期良率偏低；10月13日楊梅一廠工安意外部分停工。兩軸相抵，判持平。目前沒有已經發生轉單的證據，所以不判下降。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用毛利率、營益率與自由現金流利潤率對照","threats":[{"level":"🟡","text":"主要客戶因治理疑慮認證第二供應商，可能的對象包括景碩、南電、IBIDEN、SEMCO、Toppan、AT&S；目前仍是市場疑慮，尚未發生轉單","p":"25%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"同業與欣興自身的 ABF 新產能集中在2027下半年至2029年開出，賣方市場可能提前結束","p":"40%","evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"EMIB-T 等先進封裝基板世代轉換，首階良率目標只有50%，良率爬坡不如預期會讓份額讓給對手","p":"20%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低周轉；利益率由低轉中（TTM 營益率10.24%，最新一季15.5%）。投入資本事實表未涵蓋，ROIC 無法精算","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"AI 加速器與伺服器 CPU 都需要 ABF 載板，屬於需要而非想要；載板與 PCB 的 AI 產品占比上半年已超過六成，晶片設計商是決策者也是付款者"},{"item":"決策層級","level":"🟡","text":"替代要經過晶片設計商重新認證，而且有3～7年長約，轉換成本高；但治理疑慮已讓法人提出客戶可能多認證供應商，替代性正在上升"},{"item":"價值鏈分配","level":"🟡","text":"現在載板廠拿到較大份額（漲價、預付款），但上游 T-glass、銅箔短缺也在分走利潤；2023–2024年供過於求時毛利率曾跌到13～14%，分配比例會隨循環擺動"},{"item":"社會容忍度","level":"🟡","text":"屬企業間交易，沒有社會性價格天花板；限制來自地緣與原產地合規，產地標示刑案顯示監管容忍度是實際約束"}],"roiic":"事實表未涵蓋投入資本與折舊，增量 ROIC 無法計算","reinvest_rate":"明顯高於100%：2026年資本支出預算537億元，TTM 營業利益約153億元（營益率10.24%乘以 TTM 營收約1,490億元）","endo_ceiling":null,"formula_note":"TTM 營收的推法：2026上半年803.36億元年增28.42%，回推2025上半年約625.6億元；2025全年1,312.4億元減去上半年，得下半年約686.8億元；兩段相加約1,490億元。投入資本缺值，內生成長上界留空"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","3037.TW":19.85,"3189.TW":23.26,"8046.TW":16.04,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","3037.TW":10.24,"3189.TW":10.12,"8046.TW":12.27,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","3037.TW":-0.4,"3189.TW":7.37,"8046.TW":7.71,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","3037.TW":3.92,"3189.TW":5.59,"8046.TW":null,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3189.TW（景碩）","gm":23.26,"om":10.12,"fcf_margin":7.37,"rd_intensity":5.59,"strategy_note":"楊梅六廠擴產，ABF 產能增加25%到5,000萬顆，2027年陸續開出；TTM 毛利率與自由現金流都優於欣興","period":"TTM ending 2026-06-30（4季加總）"},{"name":"8046.TW（南電）","gm":16.04,"om":12.27,"fcf_margin":7.71,"rd_intensity":null,"strategy_note":"嘉義新廠投資468億元，最快2029上半年才貢獻營收，2027–2028年只靠去瓶頸；營益率略高於欣興","period":"TTM ending 2026-06-30（4季加總）"},{"name":"4062.T（IBIDEN）","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"日系龍頭，新產能多半在2027下半年開出；事實表營收欄缺失，無法比較利潤率","period":"TTM ending 2026-06-30（2季加總）"}]},"growth":{"driver_mix":"量價齊揚：AI 載板出貨量增加，加上2026年多次漲價（法人估漲幅10～15%）；無併購、無回購","runway_years":"約3年（供需缺口估計延續到2028年）","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板無法計算（缺投入資本）；共識三年 EPS 年複合約143%，靠毛利率擴張與漲價，不是靠再投資報酬","segments":[{"item":"ABF 載板","value":"Q2 2026 營收占52%，季增22%、年增51%；2026年資本支出的80～85%投入"},{"item":"HDI","value":"營收占22%，季增14%、年增29%；美系外資指 AI HDI 初期良率偏低"},{"item":"BT 載板","value":"營收占9%；2023年第三季曾因稼動率低而虧損"},{"item":"PCB","value":"營收占9%；產地標示爭議集中在此業務"}],"decay_signals":["自由現金流相對淨利連兩年低於0.75：2024年與2025年自由現金流分別約−164億元與−111億元（亮）","EPS 成長顯著高於營收成長：FY2027 共識 EPS 年增約85%，營收年增約46%（亮）","毛利率連兩季年減：未亮，Q2 2026 毛利率24.8%為近年高點","核心市占縮減：未亮，客戶分散供應目前仍是市場疑慮"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能而非併購；近三年現金去向四分事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無併購；子公司赴港上市屬分拆籌資，不算併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"無回購；2026年6月董事會決議現金增資發行海外存託憑證，方向是發行新股","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占 Q2 營業利益0.5%，金額小","grade":"過"}]},"valuation":{"basis":"Fwd P/E，以 FY2027 共識為主錨（FY2026 含 Q2 業外一次性收益）","tier":"台灣 ABF 載板三雄","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業 Fwd P/E 與目標價"},"fwd_pe":54.1,"peg":0.38,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"現價1,120元，相當於 FY2026 共識54倍、FY2027約29倍、FY2028約18倍。分位用四個年度端點代理，非連續五年序列：本益比、P/S、EV/S 都在端點最高。FY2027 共識淨利率約23%，已高於2022高峰約21%，循環高峰盈餘配這個倍數偏貴；但外資目標價仍高於現價，所以未到極貴。","upside_short_pct":-16,"upside_mid_pct":-18},"trap_analysis":{"verdict":"🟡","label":"循環高點估值，自由現金流連年為負"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2023年營收年減26%，毛利率由35.9%掉到19.5%；2023年第三季 BT 載板因稼動率低而虧損","assumption":"同業與欣興自身在2027下半年至2029年新增的 ABF 產能，碰上 AI 資本支出放緩","consequence":"2029–2030年 EPS 回到20元上下，倍數15倍，五年後約−70%","ruling":"採納：寫進 Bear 情境並給35%機率。與唯一致命點（報價首次季減）部分重疊，致命點就是這段故事的起點","watch":"每季毛利率與 ABF 報價方向；同業擴產時程","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"],"fact_refs":["f_kpi1_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"2026年資本支出537億元；2024–2025年自由現金流合計約−275億元；2026年6月決議發行海外存託憑證","assumption":"需求如預期，但長約把價格鎖住，擴產又吃掉現金並稀釋股本","consequence":"營收翻倍，每股自由現金流仍偏低，股東拿不到漲價紅利","ruling":"部分採納：長約加預付款保護了量，但可能壓低漲價上限，長約價格條款事實表未涵蓋。以 FY2027 自由現金流是否轉正來驗證","watch":"FY2027 自由現金流與股本變動","evidence_refs":["major_events#2"],"fact_refs":["f_kpi4","f_peer_3037_tw_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"現價1,120元，相當於 FY2026 共識54倍、FY2027約29倍；trailing 本益比、P/S、EV/S 都在四個年度端點最高；26週上漲65.5%","assumption":"市場已經把 FY2027 約23%的淨利率（高於2022前高）當成常態","consequence":"利潤率只要回到前高附近，倍數與盈餘就會雙殺","ruling":"採納：Base 情境五年報酬為負，等回檔","watch":"股價相對 FY2027 共識 EPS 是否回到20倍以下","evidence_refs":[],"fact_refs":["f_pe_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy2"]}],"max_dd":{"lo":-78,"hi":-60,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1120.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1120.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"治理疑慮與訂單黏著","cause":null,"prior_field":null,"side_a":"法人指客戶對公司治理疑慮升高，可能認證更多供應商；市場擔心高層涉案觸發美系大廠的供應鏈合規條款，分析指最壞情況是美國海關扣貨、補稅、客戶重新稽核","side_b":"高階 ABF 比重高，訂單移轉不易；ABF 產能全部在台灣，爭議產品是 PCB 而非載板；9月營收年增64.7%，看不到轉單","ruling":"目前偏向後者：月營收沒有轉單跡象，爭議集中在 PCB。但起訴與否、2027年長約續簽要到2026年底至2027年才知道，在那之前不能說風險已解除，所以 Bear 機率維持35%","evidence_level":"中：轉單疑慮是市場推測，營收數字是公司實際公告","settle_metric":"是否起訴公司法人；任一美系客戶是否公告第二供應商；月營收年增率","if_then":["若檢方起訴公司法人，或任一主要美系客戶公開導入第二供應商，持有者清倉，未持有者不建倉","反向條件：若調查只停在個人責任、不擴及載板，且月營收年增維持30%以上直到2027年第一季，此風險移出 Bear 情境加權，Bear 機率調降到30%"],"evidence_refs":["competitive_share_entrants#1","regulatory_antitrust#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","major_events#0","lawsuit_class_action#0"]},{"axis":"共識盈餘路徑與前一循環利潤率上限","cause":null,"prior_field":null,"side_a":"FY2027 共識淨利率約23%，已高於2022高峰約21%；同業與欣興自身2027下半年起擴產；2023年循環反轉時，毛利率一年內掉了16個百分點","side_b":"現在就買的最強論證：法人估 ABF 缺口2027年約21～25%、2028年約36～42%；客戶用3～7年長約加預付款鎖量；現價只有 FY2028 共識的約18倍","ruling":"選前者。缺口估計來自賣方與二手轉述，沒有原報告可驗證；長約的價格條款事實表未涵蓋，無法證明利潤率鎖得住。Base 情境 FY2028 EPS 取52元，低於共識的62.74元","evidence_level":"中：前者是公司實際財報，後者是第三方估計","settle_metric":"2027年各季毛利率是否守在24%以上","if_then":["若2027上半年兩季毛利率都在28%以上，且月營收年增40%以上，Bull 機率由20%調升到30%，價格合理時小倉起步","若任一季毛利率季減3個百分點以上，Bear 機率調升到45%，不建倉"],"evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_supply_discipline_capacity#5","end_markets#5"]}],"triggers":[{"n":1,"text":"單季毛利率連兩季跌破22%，代表漲價循環提前結束","type":"假設驗證","maps_to":"H1","metric":"單季毛利率","threshold":"<22%，連2季","action":"不建倉；已持有者減碼一半","source_freq":"每季財報","date":"2027-01"},{"n":2,"text":"產地標示刑案升級：檢方起訴公司法人，或任一主要美系客戶公開導入第二供應商","type":"風險","maps_to":"R1","metric":"起訴或客戶第二來源公告","threshold":"任一發生","action":"清倉","source_freq":"事件，公開資訊觀測站重大訊息與新聞","date":null,"evidence_refs":["regulatory_antitrust#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","major_events#0","lawsuit_class_action#0","competitive_share_entrants#1"]},{"n":3,"text":"高階 ABF 載板報價出現首次季減","type":"Single Thing","maps_to":"Single Thing","metric":"ABF 報價季變動，依法說會與產業報價","threshold":"首次季減","action":"清倉","source_freq":"每季法說會","date":null},{"n":4,"text":"股價回到約 FY2027 共識 EPS 的20倍以下，而且毛利率沒有破線，就重跑研究","type":"估值rearm","maps_to":null,"metric":"股價相對 FY2027 共識 EPS","threshold":"股價≤765元，且最近一季毛利率≥24%","action":"重跑研究，通過後小倉起步","source_freq":"每日股價與每季財報","date":null},{"n":5,"text":"同業新產能開出後，月營收年增率明顯放緩","type":"風險","maps_to":"R2","metric":"月營收年增率","threshold":"<10%，連3個月","action":"減碼","source_freq":"每月10日前營收公告","date":"2027-07","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"n":6,"text":"良率或停工拖累毛利率","type":"風險","maps_to":"R3","metric":"單季毛利率季變動","threshold":"季減3個百分點以上，且公司歸因於良率或停工","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["capital_markets_pricing#2","major_events#1","cyclical_prior_downcycle_behavior#2"]},{"n":7,"text":"Q3 2026 法說會後複審","type":"複審日期","maps_to":null,"metric":"Q3 毛利率與 Q4 展望","threshold":"毛利率是否優於24.8%","action":"更新情境機率","source_freq":"一次","date":"2026-10"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"<20%，連2季","window":"2027Q1–2028Q4","source":"公司季報","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"<10%，連3個月","window":"2027全年","source":"公開資訊觀測站月營收公告","last_status":"ok"},{"metric":"產地標示刑案進展","bear_threshold":"起訴公司法人，或客戶公告第二來源","window":"2026Q4–2027Q4","source":"檢方發布與公司重大訊息","last_status":"warning"},{"metric":"年度自由現金流","bear_threshold":"FY2027 自由現金流<0","window":"FY2027","source":"年報現金流量表","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 FY2028 共識 EPS 約18倍定價，等於把高於2022前高的淨利率當成常態；2027下半年起同業與欣興自身擴產開出後，載板利潤率歷史上會回落，2023年毛利率一年掉了約16個百分點"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=65.53, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"≤3%","requires_critic":["QC-50"],"rearm_trigger":"股價≤765元（約 FY2027 共識 EPS 20倍），且最近一季毛利率仍≥24%","exec_line":"不追；股價回到765元以下且毛利率未破24%，才重跑研究，首倉以小倉起步"},"reasoning":{"industry":"Q2 2026 營收428.9億元，年增32%；毛利率24.8%，營益率15.5%。分部組成為 ABF 載板52%（年增51%）、HDI 22%（年增29%）、BT 載板9%、PCB 9%。上半年載板與 PCB 的 AI 產品占比都超過六成，公司預期下半年分別升到70%與65～70%。歸屬母公司淨利131億元裡，約89億元是業外收益，來源包括利息、轉投資評價與處分深圳聯能，所以本業獲利品質低於 EPS 8.45元看起來的樣子。產業位置在擴張期，依據有兩項：法人估 ABF 缺口2027年約21～25%、2028年約36～42%；客戶用3～7年長約加預付款鎖量。供需屬週期性、會反轉，供給可逆性高：景碩2027年、IBIDEN 2027下半年、南電2029上半年都有新產能開出，欣興自己2027年光復二廠的 ABF 產能也會增加三成以上。單點依賴方面，據報導欣興在美系 AI ASIC 載板市占超過70%，這是護城河的證據，同時也是集中度風險；客戶別占比事實表未涵蓋。產業態勢屬雙向拉鋸：供需缺口擴大是結構轉好；產地標示刑案帶來客戶合規風險；2027年起同業擴產則是競爭惡化。","moat":"護城河機制是高階 ABF 載板的製程良率加上客戶認證週期。據報導欣興在 AI ASIC 載板的市占超過70%，客戶簽3～7年長約並預付款，可見轉換成本真實存在。同業 ROIC 事實表未涵蓋，改用利潤率比較：TTM 毛利率19.85%，低於3189.TW的23.26%、高於8046.TW的16.04%；營益率10.24%，與3189.TW的10.12%相當、低於8046.TW的12.27%；自由現金流利潤率−0.4%，兩家同業約7.4～7.7%。換句話說，目前的優勢主要表現在定價，資本效率還沒顯現。執行力給6分：刑案搜索、AI HDI 良率偏低、工安部分停工。定價力給8分：多次漲價、長約預付。綜合約7分。","growth":"成長來自量價齊揚，沒有併購，也沒有回購。三年共識 EPS 從 FY2025 實際4.34元到 FY2028 的62.74元，年複合約143%；若以 FY2026 的20.7元為起點，年複合也有約74%。共識與內生能力之間的缺口，主要來自毛利率擴張（2025年13.94%→Q2 2026 24.8%）與漲價，不是再投資報酬。投入資本事實表未涵蓋，內生天花板算不出來；這段成長要靠利潤率回到並超過前高，所以信心上限為中。FY2027 共識淨利率約23%（38.22元×16.4億股÷2,711億元），已經高於2022年高峰約21%。衰退信號亮兩個：自由現金流連兩年為負；EPS 成長遠高於營收成長。","governance":"Q2 2026 營業現金流74.9億元，減去資本支出63.3億元，自由現金流11.6億元，相對歸屬淨利131億元的轉換率不到一成。TTM 自由現金流利潤率−0.4%，同業約7.4～7.7%。2026年資本支出預算由340億元上調到537億元，其中80～85%投入 ABF。SBC 只占營業利益0.5%，不是稀釋來源；但2026年6月董事會決議現金增資發行海外存託憑證，子公司蘇州群策也申請港股上市，股本方向是擴張。淨現金約429億元，資產負債表撐得住擴產。現金去向四分事實表未涵蓋。","valuation":"現價1,120元，相當於 FY2026 共識 EPS 的54倍、FY2027 的約29倍、FY2028 的約18倍。trailing 本益比73倍、P/S 12.3倍、EV/S 12倍，三項都落在四個年度端點的最高處。FY2026 的分母含 Q2 約89億元業外收益，換算約每股5.4元；FY2027–2028 的分母則建立在高於2022前高的淨利率上，所以分母本身就是爭點。用前瞻 PEG 說便宜（以四年低基期算約0.38）不成立。循環股高峰盈餘給18～29倍並不便宜。外資目標價區間1,200～1,500元，高於現價，代表賣方仍採結構性看法，與本判斷方向相反。","premortem":"第一處會讓 Base 情境過度保守，見反證紀錄中的價格與利潤率矛盾。第二處會讓 Bear 情境來得比預期早，見治理矛盾與風險一。衰退信號亮兩個，價值陷阱風險為中。"},"plain":{"six":{"how_it_makes_money":"賺 AI 加速器晶片商的錢：ABF 載板占營收52%，錢卡在高階載板產能這一節點，現在是賣方市場。","moat":"護城河方向持平：定價力正在擴大，治理與執行面卻在侵蝕客戶黏著，兩者相抵。","growth":"成長跑道中等：供需缺口估計撐到2028年，之後同業與自身產能開出，第二條成長曲線還沒有來源佐證。","capital":"資本配置偏弱：重押擴產換成長，自由現金流還沒轉正，而且是發行新股而不是買回股票。","valuation":"現價要求 FY2027–2028 的利潤率站上並長期停在前一循環高點以上才划算，我不相信它能維持到終端年。","how_wrong":"最可能看錯的有兩處：供需缺口比我估的更久，漲價延續到2029年；或者產地標示案升級，導致高階客戶轉單。"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2028 共識 EPS 約18倍定價，等於把高於2022前高的淨利率當成常態；2027下半年起同業與欣興自身擴產開出後，載板利潤率歷史上會回落，2023年毛利率一年掉了約16個百分點","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤765元，且最近一季毛利率≥24%","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":1120.0,"week26_return_pct":65.53,"consensus_rev_3m_pct":31.18,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026 EPS 含 Q2 約89億元業外收益（利息、轉投資評價、處分深圳聯能）；FY2027–2028 EPS 要靠高於前一循環高點的淨利率，以前瞻倍數論證便宜不成立"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"Q3 2026 法說會：毛利率是否優於 Q2 的24.8%，以及2027年資本支出","impact":"高","watch":"毛利率與漲價是否延續"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"光復二廠後續產能於2027年第二季開出","impact":"中","watch":"新產能稼動率與價格"},{"date":"2027-09","date_precision":"quarter","type":"capacity","event":"景碩、IBIDEN 新增 ABF 產能於2027下半年開出","impact":"高","watch":"報價是否轉弱"},{"date":null,"date_precision":null,"type":"regulatory","event":"產地標示刑案偵查結果，是否起訴","impact":"高","watch":"是否擴及公司法人或載板產品"}],"_projected_from":"v19"}
```
