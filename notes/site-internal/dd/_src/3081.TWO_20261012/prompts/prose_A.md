你是 stock-analyst v20 的**散文層（prose）agent**，標的 3081.TWO（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261012/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：3081.TWO　日期：2026-10-12　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1315B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（414B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1006B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（851B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（898B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（227B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（625B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1955B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3385B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1514B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1315           3979-5685      5 條（2–6 內）  
s3                  8000         414           5310-7586      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2755          8572-12245      5 條（2–6 內）  
s6                 11000         227          7541-10773      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         625           2012-2875      5 條（2–6 內）  
s10                 5000        1955           2132-3045      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1514           2000-3486      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3657B；至少需散文≈41.34KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−479.3
−85
−85%
−55%
−55
−54%
−53.7
−26.53%
−2.46%
−2.10
0
0.099%
0.099
0.7%
0.75
0.76
1
1.46
1.53
1.6
1.6%
2
2%
2.5
3%
3
3.2
3.7%
3.7
4%
4
4.18
4.209
4.21
4.62
5
5%
6
7
8
8%
8.37
9
10
10%
11
12
13%
13.08%
14
15%
17.79%
18
19.61
20
20%
21%
21.72%
22
22.7
24
25%
25
26
28
30%
30
31.88%
32
35
35%
37%
37
37.27%
39.39
40%
40
40.5
41.67%
41.72%
42
42.7%
43.67
44
45
45%
46
46.9%
49
50%
50
54%
54.53%
55%
55.65%
56
57%
57.45%
60
68
70
71%
74%
76.8
80
80%
83.89
84%
84.28
85%
90
92
98.2
100%
100
100.9%
150%
154
154.3
176.54%
200%
206%
268.6
306.8
428.4
468.5
469
572.6
626.8
748.0
800
900
948
2023
2024
2025
2026
2027
2028
2029
2030
2031
2455
3025.0
3081
20261012
1,221.2
1,380
1,400
2,400
3,025
3,136
3,345
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
{"meta":{"ticker":"3081.TWO","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"聯亞光電"},"oneliner":"賣 InP 磊晶片與 CW 雷射給矽光模組廠，缺貨讓毛利率衝上 57%；現價是 FY2027 共識 EPS 的 76.8 倍，已預支缺貨延續與新產能全數賣光，不追，等報價與估值同時回到合理區。","thesis":{"H":[{"id":"H1","text":"矽光需求吸收 2027 年 2.5 倍產能：2027 年營收至少為 2026 年的 2 倍","2y":"2027 年營收 ≥ 2026 年 2 倍","5y":null,"10y":null,"threshold":"2027 年月營收年增率維持 ≥50%，全年營收 ≥2026 年 2 倍","source":"公開資訊觀測站月營收、季報、法說會","drift_rule":"營收連 2 季低於上述路徑 ≥5% 判削弱，連 3 季 ≥10% 判反轉"},{"id":"H2","text":"基板漲價下毛利率仍守 50% 以上，代表報價權在缺貨期留在磊晶環節","2y":"2027 年各季毛利率 ≥50%","5y":null,"10y":null,"threshold":"單季毛利率 ≥50%（Q2 2026 為 57.45%）","source":"季報、法說會","drift_rule":"毛利率連 2 季較基準低 ≥5% 判削弱，連 3 季低 ≥10% 判反轉"},{"id":"H3","text":"開放式 InP 磊晶市占與客戶基礎在同業擴產與 IDM 自製下守住","2y":null,"5y":"2031 年客戶數仍 ≥10 家、前三大客戶無一轉自製","10y":null,"threshold":"客戶數 ≥10 家；開放式 InP 磊晶市占 ≥50%","source":"年報客戶揭露、產業報導","drift_rule":"任一前三大客戶公開轉自製或連 4 季營收年增落後同業 ≥5% 判削弱；兩家轉自製或連 6 季落後 ≥10% 判反轉"}],"R":[{"id":"R1","text":"InP 基板供應受中國出口管制與基板廠漲價擠壓，出貨與毛利同時受限","h_ref":"H2","clock":"⚡","threshold":"單季營收季減且公司歸因缺料，或單季毛利率 < 50%","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2","geo_supply_chain#2"]},{"id":"R2","text":"2027–2028 同業倍增產能與 IDM 自製帶來報價反轉，重演 2023 年毛利率崩落","h_ref":"H2","clock":"🔥","threshold":"磊晶片報價首次調降，或毛利率連 2 季年減","evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R3","text":"客戶與地區集中：三家客戶占應收 74%、2025 年銷售 71% 在中國","h_ref":"H3","clock":"🔥","threshold":"任一前三大客戶宣布自製或第二來源，或單季營收季減 ≥15%","evidence_refs":["customer_concentration_credit#0"]},{"id":"R4","text":"擴產靠外部資金，自由現金流長期為負並稀釋股本","h_ref":"H1","clock":"🐢","threshold":"2028 年自由現金流仍為負，或股本較 2025 年底增加 >8%","evidence_refs":[]}],"single_thing":{"description":"磊晶片或 CW 雷射報價由漲轉跌（首次出現降價報導）","why_fatal":"EPS 路徑建立在缺貨期報價上；2023 年報價與稼動率一退，毛利率由 31.88% 掉到 13.08% 並轉虧。擴產 2.5 倍後固定成本更高，報價下跌對毛利率的槓桿比上一輪更大，是 EPS 最大的單一敏感項。","if_happens":"持有者清倉，未持有者不碰；Bear 機率上調並重跑研究。","how_monitor":"每季毛利率、月營收與產能的落差、產業媒體與 TrendForce 報價報導、同業產線上線時點","probability":"12–24 個月約 35%"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":76.8,"peg_fy2":0.76,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":4.21,"FY2026E":19.61,"FY2027E":39.39,"FY2028E":null},"fy_end_month":12,"eps_basis":"新台幣稀釋 EPS；FY2025A 為年度財報稀釋 EPS 4.209，FY2026E／FY2027E 為 yfinance 分析師共識平均，FY2028E 共識事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261012/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"近四個年度有兩年虧損（2023、2024），毛利率由 13.08% 擺到 57.45%，擺幅逾 40pp；擴產期資本支出大於營業現金流。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：Lumentum 稱缺口逾三成、TrendForce 預期失衡延續到 2027 之後（皆二手轉述）；但 Coherent 兩度倍增 InP 產線、Lumentum 美國新廠、聯亞 2027 產能 2.5 倍，新供給 2026–2028 上線，供給可逆性高。","bargaining":{"up":"上游 InP 基板強勢：2025Q4 起已漲三次、Q4 評估再漲逾一成；聯亞以住友電工 2026–2030 長約與安全庫存緩衝。","down":"客戶由 7–8 家增至 10 家以上，但三家客戶占應收帳款 74%，且主要客戶本身有自建 InP 能力。","geo":"2025 年銷售 71% 在中國；基板受中國出口管制影響，已推動日本與歐洲供應商認證。"},"profit_pool_dir":"缺貨期利潤池往雷射與磊晶環節移動，能否留住取決於 2027–2028 新產能上線後的報價。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率或利潤池占比；只有 800G 以上出貨由 2,400 萬增至 6,300 萬的二手引述，不足以建滲透率表。"}},"moat":{"mechanism":"磊晶製程經驗＋客戶雷射重新認證週期＋InP 基板長約；替代性的決策單位是客戶每一代模組的雷射認證，不是磊晶片這個商品。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大（客戶 7–8 家增至 10 家以上、1.6T 量產、開放式 InP 磊晶市占逾六成）；定價面僅穩定（漲價來自全產業缺貨，同業倍增產能與 IDM 自製在 2027–2028 壓回），合判持平。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能以毛利率與營益率對比；IQE.L 財報資料缺。","threats":[{"level":"🔴","text":"IDM 自行供應磊晶加上 Coherent、Lumentum 自建 InP 產能，2027–2028 削弱外購磊晶需求與報價。","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#3"]},{"level":"🟡","text":"InP 基板受中國出口管制，限制延續且無新增來源時中長期供應受限；已有長約與安全庫存緩衝。","p":"20%","evidence_refs":["supply_demand_durability#3","geo_supply_chain#2"]},{"level":"🟡","text":"全新等開放式磊晶同業擴產搶單，屬點對點競爭。","p":"25%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋，擴產期資本密集度上升，推測偏低周轉）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是雲端資料中心、決策者是光模組廠、付款者是模組廠；AI 叢集光互連是需要不是想要，800G 以上出貨由 2,400 萬增至 6,300 萬（二手引述）。急迫性不等於持久性，需求強度已反映在報價。"},{"level":"🟡","item":"決策層級","text":"替代性要在客戶每一代雷射認證衡量：換磊晶來源需重驗，黏性存在；但 Lumentum、Coherent 有能力自製，IDM 自行供應已被賣方點名，重新認證週期隨 3.2T 換代可能成為轉單窗口。"},{"item":"價值鏈分配","level":"🟡","text":"缺貨期利潤往雷射與磊晶環節移動，但上游基板已漲三次、Q4 再評估漲逾一成，下游客戶集中（三家占應收 74%）且可自建，聯亞夾在兩個強勢環節之間，需求存在不等於這一環能長期多拿。"},{"item":"社會容忍度","level":"🟢","text":"企業間零組件，無監管定價或社會漲價天花板；唯一政策面是基板出口管制，屬供應風險而非價格上限。"}],"roiic":"事實表未涵蓋（無投入資本序列，無法算增量 ROIC）","reinvest_rate":"約 200%（Q2 2026：淨利 468.5 百萬元 − 自由現金流 −479.3 百萬元 ＝ 再投資約 948 百萬元，以淨利代稅後營業利益）","endo_ceiling":null,"formula_note":"再投資＝淨利−自由現金流＝資本支出−折舊＋營運資金增加；單季數字，擴產高峰期偏高。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","3081.TWO":54.53,"2455.TW":37.27,"IQE.L":null,"LITE":41.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","3081.TWO":41.72,"2455.TW":21.72,"IQE.L":null,"LITE":17.79,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","3081.TWO":-2.46,"2455.TW":7.31,"IQE.L":null,"LITE":9.96,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","3081.TWO":6.31,"2455.TW":10.55,"IQE.L":null,"LITE":11.83,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"2455.TW","gm":37.27,"om":21.72,"fcf_margin":7.31,"rd_intensity":10.55,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"IQE.L","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表無財務資料，無法比較；屬開放式磊晶同業。"},{"name":"LITE","gm":41.67,"om":17.79,"fcf_margin":9.96,"rd_intensity":11.83,"period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（2027 產能 2.5 倍）＋價為輔（基板與磊晶片多次漲價）；無併購、無回購。","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 無法從事實表推導；再投資率約 200% 且靠私募（上限 4,500 張）與 12 億元可轉債補資金，共識 FY2025→FY2027 EPS 年化約 206% 遠超內部資金可支撐速度，缺口歸因毛利率擴張與漲價。","segments":[{"item":"DataCom（矽光為主）","value":"占營收 80–85%"},{"item":"電信","value":"占營收 5–10%"},{"item":"其他","value":"約 5%"}],"seven_questions":[],"decay_signals":["EPS 成長顯著高於營收成長（毛利率由 42.7% 擴張至 57.45% 推動）：亮","自由現金流／淨利 < 0.75：2026 年轉負但只一年，未達連兩年：未亮","毛利率連兩季年減：未亮","TAM 被替代技術壓縮：公司稱 EML 與 CW 雷射各有應用，未見替代報導：未亮"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，現金去向集中在擴產資本支出；近三年現金去向四分事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"無併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"無回購；反向有私募普通股上限 4,500 張與 12 億元有擔保可轉債","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"股票酬勞占營收 0.7%、占營業利益 1.6%（Q2 2026）","grade":"過"}]},"valuation":{"basis":"Fwd P/E（FY2027E 共識 EPS）＋P/S 年度端點對照","tier":"AI 光通訊上游元件（磊晶與雷射）","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比或 EV 倍數，無法建同層級倍數錨。"},"fwd_pe":154.3,"peg":1.53,"percentile_5y":100,"val_light":"🔴","val_light_derivation":"FY2 本益比 76.8 倍，對一家四年內兩年虧損、毛利率擺幅逾 40pp 的公司過高；P/S 以四個年度端點計現值高於所有端點（分位 100，非連續五年分位）；判紅。","upside_short_pct":3.7,"upside_mid_pct":-53.7},"trap_analysis":{"verdict":"🟡","label":"循環高點盈餘陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"上一輪下行 2023 年營收年減 55.65%、毛利率 13.08%、EPS −2.10；Coherent 兩度倍增 InP 產線、Lumentum 美國新廠、高盛點名 IDM 自行供應磊晶。","assumption":"本份假設 2027 年前缺貨不退。","consequence":"2028 年新產能到位、報價轉跌，毛利率回到 25–30%，EPS 腰斬、倍數由成長股壓到循環股，五年後虧損逾 80%。","ruling":"採納：Bear 機率給 30%，與唯一致命點部分重疊（報價轉跌是同一事件的觸發點），終端倍數與 EPS 路徑已反映。","watch":"單季毛利率、磊晶片報價方向、同業擴產進度","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_supply_discipline_capacity#3"],"fact_refs":["f_kpi1"]},{"view":"論點失敗","evidence":"2025 年底三家客戶占應收帳款 74%，2025 年銷售 71% 在中國；基板受中國出口管制。","assumption":"客戶擴到 10 家以上已分散風險。","consequence":"單一大客戶轉自製或中國客戶縮單，單季營收可能季減逾一成五。","ruling":"採納為中期風險，列入假設風險清單；客戶營收占比事實表未涵蓋，無法量化。","watch":"年報客戶揭露、月營收季減幅度","evidence_refs":["customer_concentration_credit#0","geo_supply_chain#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Q2 自由現金流 −479.3 百萬元；近三季資本支出近 60 億元，靠私募（上限 4,500 張）與 12 億元可轉債補錢；基板 Q4 再漲逾一成。","assumption":"需求兌現就等於股東賺錢。","consequence":"需求兌現但新產能報酬率低於舊產能、股本擴張約 4–5%，每股盈餘成長落後營收成長。","ruling":"部分採納：股本稀釋規模有限，但擴產報酬率無法驗證，資本配置不給加分。","watch":"自由現金流轉正時點、私募完成價格與股數","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2"],"fact_refs":["f_kpi4"]},{"view":"價格已反映太多","evidence":"FY1 本益比 154.3 倍、FY2 76.8 倍、P/S 84.28 倍；賣方均值目標價約 3,136 元與現價相近；美系外資 3 月即以評價已反映利多降評。","assumption":"市場會持續用成長股倍數看待 2027 年盈餘。","consequence":"即使 Bull 路徑五年報酬約 +37%，Base 約 −54%，期望值為負。","ruling":"採納：這是本份不追的主要約束。","watch":"股價對 FY2027 共識 EPS 倍數","evidence_refs":[],"fact_refs":["f_pe_current","f_ps_current","f_consensus_eps_fy2"]}],"max_dd":{"lo":-85,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 3025.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=3025.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"供需持久度","cause":null,"prior_field":null,"side_a":"業界預期 InP 供需失衡延續到 2027 之後，Lumentum 稱產能訂滿到 2028、缺口逾三成（二手轉述）。","side_b":"Coherent 兩度倍增 Sherman InP 產線、Lumentum 美國新建廠、聯亞 2027 產能 2.5 倍，新供給 2026–2028 陸續上線；賣方點名 IDM 自行供應磊晶。","ruling":"不可調和（對 2028 年報價方向相反）。裁決偏向供給追上：供給增量是已公告的實體擴產，需求面多為二手引述且只看到 2028。決定性數字是 2027 下半年磊晶片報價方向。","evidence_level":"中（多為二手報導）","settle_metric":"磊晶片與 CW 雷射報價方向、單季毛利率","if_then":["若 2027 上半年磊晶片報價仍上調且單季毛利率 ≥55%，股價回到 FY2027 共識 EPS 35 倍以下時建立首倉 2%","若出現首次降價報導，未持有者不碰，持有者清倉"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#5","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"7 月營收年增 176.54%、Q3 財測季增約 20%、2027 產能 2.5 倍、客戶擴到 10 家以上，FY2027 共識 EPS 較 FY2026 翻倍；若 2028 仍缺貨，EPS 再上一層，倍數可被成長消化。","side_b":"即使 Bull 路徑（2031 年 EPS 92 元、45 倍）五年總報酬也只約 +37%，Base 約 −54%；現價已定價最好情境。","ruling":"可調和（程度差異）：生意好與價格貴同時成立，裁決不追。","evidence_level":"中","settle_metric":"單季毛利率與月營收年增率","if_then":["若 2027 年前兩季毛利率 ≥55% 且月營收年增 ≥80%，上修 Base 終端 EPS 並重跑研究","若股價先漲而報價證據未到，不追"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#2"]},{"axis":"賣方共識與本份分歧","cause":null,"prior_field":null,"side_a":"賣方 10 位均值目標價約 3,136 元，8 買 1 持有 1 賣，Macquarie 目標價 3,345 元。","side_b":"本份 Base 五年終值約 1,400 元，期望報酬為負。","ruling":"分歧屬框架層：賣方以 12 個月內 FY2027 盈餘乘倍數，本份以五年內含一次報價下行的盈餘定價；市場錯在把缺貨期毛利率當常態。全距最高最低相差 5 倍，本份對 Base 路徑的信心也下調。","evidence_level":"中","settle_metric":"2027 下半年單季毛利率","if_then":["若 2027 下半年毛利率仍 ≥55% 且無降價報導，本份框架錯，上修 Base 機率並重跑研究","若毛利率跌破 50%，維持不碰"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"擴產吸收驗證：2027 年起月營收年增率","type":"假設驗證","maps_to":"H1","metric":"月營收年增率","threshold":"連續 3 個月 < 30%","action":"持有者減碼一半；未持有者維持不追","source_freq":"公開資訊觀測站，每月","date":null},{"n":2,"text":"磊晶片或 CW 雷射報價首次調降","type":"Single Thing","maps_to":"Single Thing","metric":"磊晶片報價方向","threshold":"首次出現降價報導","action":"清倉","source_freq":"產業報導、法說會，每季","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#3"]},{"n":3,"text":"毛利率跌破缺貨期水準","type":"風險","maps_to":"R1","metric":"單季毛利率","threshold":"< 50%","action":"減碼一半","source_freq":"季報，每季","date":null,"evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2"]},{"n":4,"text":"大客戶轉自製或導入第二來源","type":"風險","maps_to":"R3","metric":"前三大客戶採購動向","threshold":"任一宣布自製或第二來源","action":"減碼一半","source_freq":"產業報導、年報，不定期","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":5,"text":"估值回到可進場區且毛利率未破","type":"估值rearm","maps_to":"H2","metric":"股價對 FY2027 共識 EPS 倍數","threshold":"≤ 35 倍（約 1,380 元）且單季毛利率 ≥50%","action":"重跑研究後首倉 ≤2%","source_freq":"每日股價、每季毛利率","date":null},{"n":6,"text":"Q3 2026 財報與法說複審","type":"複審日期","maps_to":"H1","metric":"Q3 營收季增率與毛利率","threshold":"季增 ≥20%、毛利率 ≥55%","action":"未達則下修 Base 路徑","source_freq":"季報","date":"2026-11"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"連兩季 < 45%","window":"2027Q1–2028Q4","source":"公司季報","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連三個月轉負","window":"2027–2028","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"磊晶片報價方向","bear_threshold":"首次降價報導","window":"未來 12–24 個月","source":"產業報導（經濟日報、TrendForce）與法說會","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把缺貨期 57% 毛利率與 2.5 倍產能全數售出當成常態，忽略 2027–2028 同業 InP 產線倍增、IDM 自製與 2023 年毛利率 13% 的先例。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=43.67, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"3%","requires_critic":[],"rearm_trigger":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,380 元）且單季毛利率仍 ≥50%","exec_line":"不追；未持有者等上述價位並重跑研究，首倉 ≤2%；已持有者毛利率跌破 50% 減碼一半，報價轉跌清倉。"},"reasoning":{"industry":"Q2 2026 營收 1,221.2 百萬元，毛利率 57.45%，營業利益 572.6 百萬元（營益率 46.9%），稅後淨利 468.5 百萬元；EPS 口徑不一（法說自結約 4.62、yfinance 稀釋 4.18），本份以 yfinance 口徑為準。產品組合：DataCom 占 80–85%（矽光最大），電信 5–10%，其他約 5%；1.6T 已量產、3.2T 與客戶開發中。管理層未給數字財測，只說矽光需求非常強勁、2027 年產能約為 2026 年的 2.5 倍；媒體轉述 Q3 營收季增約 20% 的財測。產業時鐘判在擴張期：7 月營收年增 176.54%、基板與磊晶片 2025Q4 起多次漲價、全產業擴產。供需持久度：週期性將反轉——缺口目前逾三成且業界預期延續到 2027 之後，但同業新產能 2026 至 2028 陸續上線、公司自身 2027 產能 2.5 倍，供給可逆性高。產業態勢判雙向拉鋸：結構轉好軸（InP 雷射缺貨、客戶由 7–8 家增至 10 家以上）對上競爭惡化軸（同業兩度倍增 InP 產線、高盛點名 IDM 自行供應磊晶）。單點依賴：上游 InP 基板（中國出口管制、住友電工五年長約）與下游集中（2025 年底三家客戶占應收帳款 74%、2025 年銷售 71% 在中國）；單一客戶營收占比事實表未涵蓋。","moat":"機制是磊晶製程經驗加上客戶的雷射重新認證週期：模組廠換磊晶來源要重驗，這給了黏性；住友電工 2026–2030 基板長約鎖住核心材料。利潤率對比：TTM 毛利率 54.53%、營益率 41.72%，高於全新（37.27%／21.72%）與 Lumentum（41.67%／17.79%），但同業 ROIC 事實表未涵蓋，只能比利潤率，且對比落在缺貨高峰。執行力給 8 分（1.6T 量產、3.2T 送驗、客戶擴到 10 家以上），定價力給 6 分（2023 年營收年減 55.65%、毛利率 13.08%、全年虧損，缺貨一退報價就守不住）。方向判持平而非擴大：執行面在擴大，但定價面受三股力量夾擊——基板廠 Q4 再漲逾一成吃掉利潤、Coherent 與 Lumentum 自建 InP 產線、IDM 自行供應磊晶。ROIC 只能拆一半：稅後營業利益率高，投入資本周轉率事實表未涵蓋；再投資率約 200%（Q2 稅後淨利 468.5 百萬元減自由現金流 −479.3 百萬元，得再投資約 948 百萬元，以淨利代稅後營業利益），增量 ROIC 無法推導。","growth":"成長來源以量為主（2027 產能 2.5 倍、客戶擴到 10 家以上），價為輔（基板與磊晶片 2025Q4 起多次漲價），無併購、無回購。共識 EPS：FY2025 實際 4.21 元、FY2026E 19.61 元、FY2027E 39.39 元，兩年年化約 206%；FY2028E 共識事實表未涵蓋，無法算三年 CAGR。內生上界：增量 ROIC 推不出，再投資率約 200% 且已靠私募與可轉債補資金，共識成長顯然超過內部資金可支撐的速度。缺口歸因毛利率擴張（2025 年 42.7% → Q2 2026 57.45%）與漲價，不是回購或併購；這部分會隨供需反轉回吐。第二曲線有線索（3.2T、延伸到 EML 與接收端 PD，公司稱與 CW 雷射並非互相取代），但沒有量化依據，故不給寬燈。衰退信號亮一盞：EPS 成長遠快於營收成長（差距來自毛利率擴張）；自由現金流轉負但只一年，未達連兩年門檻。","governance":"FCF／淨利：2025 年 626.8／428.4 百萬元約 1.46 倍，轉換良好；2026 起擴產，Q2 營業現金流 268.6 百萬元、資本支出 748.0 百萬元，自由現金流 −479.3 百萬元，TTM FCF 利潤率 −2.46%；營業現金流低於淨利，反映在製品與基板安全庫存堆高。近三季已公告資本支出近 60 億元，董事會另通過不超過 22.7 億元設備、向 Aixtron 購置約 8.37 億元設備；資金來源包括 2026 年 1 月通過的私募（上限 4,500 張，以 900 元計約 40.5 億元，約占現有股本 4%）與 6 月通過的 12 億元有擔保可轉債，是否完成與實際價格事實表未涵蓋。股票酬勞占營收 0.7%、占營業利益 1.6%，很低。股息殖利率 0.099%，無回購。","valuation":"FY1 本益比 154.3 倍、FY2 76.8 倍（3,025 元分別除以 19.61、39.39），P/S 84.28 倍、EV/S 83.89 倍，trailing 本益比 306.8 倍，各自都在可得年度端點的最高位。賣方均值目標價約 3,136 元（10 位、資料日期未明），只比現價高約 3.7%，區間 900–4,500 元，最高最低相差 5 倍，共識本身分歧大；另一來源 469 元疑為過期快照，不採用。PEG 以 FY1 本益比除以 FY2026→FY2027 共識成長 100.9% 得 1.53；若用 FY2025 起算的兩年年化約 206% 會得到更低的數字，但基期是虧損後復甦年，便宜論證不成立。同業現值本益比事實表未涵蓋，終端倍數無法附同業對照。分母爭點：FY2027 共識 EPS 隱含缺貨報價與新產能全數售出，屬循環高點盈餘。","premortem":"反證集中在三件事：上一輪下行實績（2023 年營收年減 55.65%、毛利率 13.08%、EPS −2.10，股價 2023 年 10 月低見 98.2 元）、2027–2028 同業新產能與 IDM 自製、基板受中國出口管制。衰退信號亮一盞（EPS 成長遠快於營收），自由現金流轉負只一年。反方向也可能看錯：若 3.2T 與 CPO 讓缺貨延續到 2029，本份的 Base 過於保守。細節見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺 AI 資料中心光模組廠的錢：營收八成以上來自矽光用 CW 雷射與 InP 磊晶片，錢卡在 InP 基板供應與磊晶產能兩個節點；Q2 毛利率 57.45%、營益率 46.9%，是公司史上最高。","moat":"護城河 B 級、方向持平：開放式 InP 磊晶市占逾六成與客戶擴張是真的，但現在的定價力主要來自缺貨，2023 年毛利率曾掉到 13%，證明它不是結構性定價權。","growth":"成長跑道中等：矽光與 1.6T／3.2T 世代切換讓量至少成長到 2027，但滲透率事實表未涵蓋，且 2028 年起同業新產能湧入，五年後成長取決於報價能否守住。","capital":"資本配置屬擴產期：自由現金流轉負、靠私募與可轉債補錢，沒有回購，股東稀釋風險大於員工酬勞稀釋。","valuation":"現價要求缺貨報價延續到 2028 年以後、2.5 倍產能全數以現價賣光、毛利率守在 55% 以上，而且市場繼續給高成長倍數；四件事同時成立的機率我不信。","how_wrong":"最可能看錯的地方是把缺貨期毛利率當成新常態；陷阱風險中等。"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把缺貨期 57% 毛利率與 2.5 倍產能全數售出當成常態，忽略 2027–2028 同業 InP 產線倍增、IDM 自製與 2023 年毛利率 13% 的先例。","momentum_overheated":false,"cycle_gates_pass":false,"wait_for_price":true,"wait_for_price_condition":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,380 元）且單季毛利率仍 ≥50%","trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":3025.0,"week26_return_pct":43.67,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2027E 共識 EPS 39.39 元隱含缺貨期報價與 2.5 倍產能全數售出，是循環高點盈餘；以它算出的倍數與 PEG 低估真實價格，便宜論證不成立。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026 財報與法說，驗證季增約 20% 財測","impact":"高","watch":"單季毛利率是否 ≥55%、Q4 展望與追加資本支出"},{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"InP 基板廠評估 Q4 再漲價逾一成","impact":"中","watch":"磊晶片是否同步第三次漲價、毛利率是否被吃掉"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"2027 年 2.5 倍產能上線節奏","impact":"高","watch":"月營收能否隨產能放大"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"Coherent Sherman InP 產線第二次倍增目標時點","impact":"高","watch":"磊晶片報價方向"}],"_projected_from":"v19"}
```
