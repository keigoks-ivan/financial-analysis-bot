你是 stock-analyst v20 的**散文層（prose）agent**，標的 6669.TW（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261012/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：6669.TW　日期：2026-10-12　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1261B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（469B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1005B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1154B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1015B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（331B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（722B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2125B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3450B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2260B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1261           4017-5739      5 條（2–6 內）  
s3                  8000         469           5272-7531      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3174          8278-11826      5 條（2–6 內）  
s6                 11000         331          7468-10669      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         722           1945-2778      5 條（2–6 內）  
s10                 5000        2125           2012-2875      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2260           2000-2740      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4235B；至少需散文≈40.77KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−251
−146
−60
−60%
−58%
−40%
−40
−24%
−17.85%
−8.93%
−5.84%
−0.5
0%
0
0.39
0.58
0.75
1
1.14
1.2
1.21
1.32
1.4
1.52
2
2%
2.1
2.13%
2.13
2.8
2.9
3%
3
3.3
3.34%
3.8%
4
5%
5
5.5%
5.54%
5.8
5.8%
5.85%
6
6%
6.62%
7%
7.0%
7
7.09%
7.3%
7.6%
7.8%
8
8%
8.2%
8.25%
9
09
9.3%
9.42
10
10%
10.37%
10.82%
11
11.4
12
12%
12.6
12.64
13
14
15
15%
16
17.4%
18.5
18.52
18.8
18.81
20%
23%
23.2
24%
24
25
25%
26
26%
26.0%
28%
30
30%
31.912
32.2%
32.2
34%
34.3%
34.3
35
35%
38%
40%
40
42
43%
45
49
49%
50.2%
52%
59%
68%
70%
70
80.43
86%
90
91.56
91.56%
98.06
100%
100
105
115
120
120.95
125
128%
149.69
150%
150
157
162
172
179.98
195
200
205
210%
220
226.58
228
232
235
250
265.54
283
285
315
345
348.72
479
511
657
667.97
945
2023
2024
2025
2026
2027
2028
2029
2031
2275.0
2382
3231
6669
20261012
1,080
1,800
2,275
2,292
2,408
2,781.53
3,000
3,055
3,382
4,000
4,326
6,600
7,568
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
{"meta":{"ticker":"6669.TW","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"緯穎科技 Wiwynn"},"oneliner":"緯穎是直供 hyperscaler 的 ASIC 機櫃龍頭 ODM，營業利益率高於台系同業；但前兩大客戶占營收八成以上、自由現金流連年為負，倍數也在自身高檔、循環偏晚段。結論是不追，等股價回落或擴張轉成現金再談。","thesis":{"H":[{"id":"H1","text":"AI 機櫃出貨與 ASIC 份額撐住，2027 年 EPS 達到共識附近","2y":"FY2027 EPS 不低於 162 元（共識 179.98 元下修一成以內）","5y":null,"10y":null,"threshold":"FY2027 共識或實際 EPS ≥ 162 元","source":"公司季度財報新聞稿、Koyfin 共識月快照","drift_rule":"近十二個月 EPS 落後基本情境路徑連 2 季 ≥ 5% 為削弱，連 3 季 ≥ 10% 為反轉"},{"id":"H2","text":"營業利益率持續高於台系同業：近十二個月 6.62%，對廣達 3.34%、緯創 3.8%","2y":null,"5y":"營業利益率 ≥ 5.5%，且對廣達、緯創的差距 ≥ 2 個百分點","10y":null,"threshold":"營益率 ≥ 5.5% 且同業差距 ≥ 2 個百分點","source":"各公司季報","drift_rule":"差距低於 2 個百分點連 4 季為削弱，連 6 季為反轉"},{"id":"H3","text":"擴張轉成現金：自由現金流率由近十二個月 −5.84% 轉正","2y":null,"5y":"2028 年全年自由現金流率 ≥ +2%","10y":null,"threshold":"年度自由現金流率 ≥ +2%","source":"公司年報與季度現金流量表","drift_rule":"近十二個月自由現金流率連 4 季低於 0% 為削弱，連 6 季為反轉"}],"R":[{"id":"R1","text":"毛利率被零組件成本與同業擠壓；Q2 的 9.3% 含一次性 NRE 與代採購的會計效果","h_ref":"H2","clock":"⚡","threshold":"季毛利率低於 7.0%，連兩季","evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"id":"R2","text":"客戶集中：2024 年 Meta 占 52%、Microsoft 占 34%，合計 86%；另有財報摘要把客戶集中與訴訟列為風險，訴訟內容事實表未涵蓋","h_ref":"H1","clock":"🔥","threshold":"任一大客戶下一代專案改由其他 ODM 主供","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#3"]},{"id":"R3","text":"hyperscaler capex 2028 年放緩，融資壓力浮現","h_ref":"H1","clock":"🔥","threshold":"Meta、Microsoft、Amazon 任一家次年 capex 指引年減逾 10%","evidence_refs":["supply_demand_durability#5"]},{"id":"R4","text":"產能七成集中在墨西哥，關稅待遇與客戶出貨地要求可能改變","h_ref":"H2","clock":"🐢","threshold":"USMCA 待遇取消，或客戶再次要求停止自墨西哥出貨","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]},{"id":"R5","text":"資本風險轉到緯穎：德州據點投資放大到 16 億美元以上，Q1 存貨季增 68%，總資產由 3,382 億增到 4,326 億元","h_ref":"H3","clock":"🔥","threshold":"存貨季增率比營收季增率高 10 個百分點以上，連兩季","evidence_refs":["ems_utilization_capex_cycle#0","ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1"]}],"single_thing":{"description":"Meta、Microsoft 或 AWS 任一家，在下一代 AI 機櫃專案把主供改給其他 ODM，緯穎份額掉到三成以下","why_fatal":"前兩大客戶 2024 年合計占營收 86%。一家主供專案轉走，等於三到五成營收消失，而德州廠折舊與利息照算；對 EPS 的衝擊大於任何利潤率或關稅情境","if_happens":"不建倉；已持有則清倉並重跑研究","how_monitor":"季報的客戶占比、外資對 AWS 份額的追蹤（高盛估 2026 年約七成）、月營收連兩月年減","probability":"約 15%（12–24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.64,"peg_fy2":0.39,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":98.06,"FY2026E":120.95,"FY2027E":179.98,"FY2028E":226.58},"fy_end_month":12,"eps_basis":"Koyfin 共識（美元依 2026-10-09 匯率 31.912 換成台幣），與判斷日股價同一口徑。基期 98.06 元由判斷日股價 2,275 元 ÷ trailing 本益比 23.2 反推，屬近十二個月口徑，代用 FY2025 實際值；公司年報稀釋 EPS 265.54 元是另一套每股口徑，不混用"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261012/scenario.json","archetype":{"primary":"EMS/ODM","secondary":null,"confidence":"高","fingerprint":"直供 hyperscaler 的機櫃級 ODM：毛利率個位數，營運資金與產能都吃資本，營收跟著少數客戶的 capex 週期走"},"industry":{"clock_phase":"II","sd_verdict_source":"屬週期性。TrendForce 估記憶體 2027 下半年才緩解；Goldman 估供需最早 2027 下半年平衡，2028 年 capex 成長放緩到 12%；Morgan Stanley 估 2028 年 capex 上看 1.4 兆美元。","bargaining":{"up":"上游 GPU、記憶體、先進封裝都是賣方市場，緯穎是價格接受者，只能與客戶協商成本轉嫁","down":"客戶是少數 hyperscaler，2024 年前兩大客戶合計 86%，議價權在客戶手上","geo":"產能墨西哥七成、馬來西亞兩成、歐洲一成；德州第二棟廠 2027 年量產後，美國產能約占兩成"},"profit_pool_dir":"利潤池往晶片、記憶體與封裝端集中。客戶透過直購與代採購把帳面營收移出 ODM，整合費比重小，資本負擔卻往 ODM 移。","tam_table":{"expanded":false,"reason":"事實表只有產業層級的出貨量與 capex 數字，沒有緯穎可服務市場規模與份額的五年序列，無法組出五年前到現在的對照表；份額證據只有單一客戶的外資推估"}},"moat":{"mechanism":"直供 hyperscaler 的 ASIC 機櫃設計與整合能力，加上提前鎖定的高功率廠房電力容量；換供應商要多走一個平台世代的驗證","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"對台系同業的營業利益率差距約 3 個百分點仍在，但自身營益率由 2024 年 7.8% 降到 6.62%，ROCE 也由 38% 降到 23%；最大客戶份額沒有下滑的來源證據。執行力判穩定，定價權判穩定偏弱，合判持平","peer_na_reason":null,"threats":[{"level":"🔴","text":"客戶把價值鏈往自己拉：部分記憶體改為客戶直購；德州據點投資放大到 16 億美元以上，報導未說明 Amazon 是否出資，ODM 只拿整合費卻要扛資本風險","p":35,"evidence_refs":["ems_utilization_capex_cycle#0","end_markets#4"]},{"level":"🟡","text":"同業擠壓：台系 AI 伺服器 ODM 營收增速普遍高於毛利增速，緯穎 Q1 營收在五大裡排第四，廣達、鴻海的 GPU 機櫃規模更大","p":40,"evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"大客戶第二供應來源：日系外資提到緯創可能作為 L10 配額備援，目前不是明確的第二供應商認定","p":25,"evidence_refs":["customer_second_source#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是 hyperscaler 本身，三個角色一致。需求急迫，但急迫不等於持久：Goldman 估 2027 年五大 capex 約 1.2 兆美元、2028 年成長放緩到 12%，而且每年要約 3,000 億美元 AI 營收才能打平"},{"item":"決策層級","level":"🟡","text":"替代性要在每一代機櫃專案的主供決定上衡量，不是看市場上有幾家 ODM。每代平台都要重新認證，客戶有能力切換，換供應商的代價是一個平台週期的驗證時間。讀數：外資估 AWS 相關份額約七成；續約率與合約年限事實表未涵蓋"},{"item":"價值鏈分配","level":"🔴","text":"整條鏈的利潤集中在晶片、記憶體與先進封裝，ODM 毛利率在 8% 上下。客戶自 2026 年 4 月起把部分記憶體改為直購，德州據點投資卻由緯穎承擔。讀數：近十二個月毛利率 8.2%、自由現金流率 −5.84%"},{"item":"社會容忍度","level":"🟡","text":"伺服器整合價格沒有民生敏感度，社會不會限制定價；風險在政策面。美國 232 條款對先進晶片衍生品課 25%（美國資料中心用途可豁免），鋁鋼銅關稅擴大，墨西哥產出又依賴 USMCA 待遇"}],"roiic":"約 24%，且在下滑。2024→2025 年淨利增加 283 億元，對應前一年再投資 479 億元約 59%、當年再投資 657 億元約 43%；以 2026 年共識淨利 667.97 億元計，增量淨利 157 億 ÷ 2025 年再投資 657 億 ≈ 24%","reinvest_rate":"2025 年約 128%（再投資 657 億 ÷ 淨利 511 億），2024 年約 210%；再投資以淨利減自由現金流計，用淨利代替稅後營業利益","endo_ceiling":24,"formula_note":"內生成長上限 = 增量報酬約 24% × 再投資率（封頂 100%）≈ 24%。超過 100% 的再投資靠可轉債與聯貸支應，不算內生"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","6669.TW":8.2,"2382.TW":5.54,"3231.TW":5.85,"SMCI":10.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","6669.TW":6.62,"2382.TW":3.34,"3231.TW":3.8,"SMCI":7.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","6669.TW":-5.84,"2382.TW":-1.2,"3231.TW":-8.93,"SMCI":-17.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","6669.TW":1.09,"2382.TW":1.29,"3231.TW":1.15,"SMCI":1.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"2382.TW 廣達","gm":5.54,"om":3.34,"fcf_margin":-1.2,"rd_intensity":1.29,"strategy_note":"營業利益率 3.34%，約為緯穎一半，靠 GPU 機櫃規模取勝，利潤結構較薄","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3231.TW 緯創","gm":5.85,"om":3.8,"fcf_margin":-8.93,"rd_intensity":1.15,"strategy_note":"營業利益率 3.8%，自由現金流率 −8.93% 比緯穎更吃資本；外資提到它可能是緯穎的組裝備援","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SMCI","gm":10.82,"om":7.09,"fcf_margin":-17.85,"rd_intensity":1.97,"strategy_note":"毛利率 10.82%、營益率 7.09% 略高於緯穎，但自由現金流率 −17.85% 最差；走品牌與通路，不是直供 ODM","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（機櫃出貨與單機內容），價多為零組件轉嫁；無併購、無回購","runway_years":5,"runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 24% × 再投資率封頂 100%；共識三年 CAGR 約 32.2% 超出天花板約 8 個百分點，靠外部融資補足","segments":[{"item":"AI 伺服器","value":"2025 年約占營收一半，其中 ASIC 約九成；管理層預期 2026 年過半"},{"item":"通用伺服器","value":"2025 年約占一半；Nomura 預期 2026 年出貨年增 20%–30%，管理層稱各季出貨年增"}],"decay_signals":["自由現金流對淨利連兩年低於 0.75：2024、2025 年自由現金流都是負值（亮燈）","毛利率年度下滑：2024 年 10.37% 降到 2025 年 8.25%；季度年比連兩季的資料事實表未涵蓋（半亮）","其餘八類事實表未見亮燈：核心市占、提價後銷量、EPS 與營收增速差、員工股票酬勞、TAM 被替代、產業倍數下移、維護性資本支出、停止投資，均無資料或不成立"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；事實表只有股息殖利率 2.13%，沒有股息與回購的歷年明細，無法展開"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事件軸查無重大收購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購紀錄；公司正以可轉債與聯貸籌資，方向與回購相反","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"員工酬勞股數事實表未涵蓋；上限 150 億元可轉債若轉換會有稀釋，但市值與轉換價未列，無法精算","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（Koyfin FY1 共識，與判斷日股價同口徑），輔以 PEG","tier":null,"peers":{"expanded":false,"reason":"事實表只有同業的利潤率，沒有同業本益比，無法組成同層級的倍數對照"},"fwd_pe":18.52,"peg":0.58,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 18.5 倍與 12.6 倍、PEG 0.58，若共識兌現不算貴；但 trailing 各倍數都在自身四個年度端點的最高位，獲利處在客戶 capex 高峰，每股口徑也有爭議，便宜的論證不成立，結論是合理偏滿。五年分位事實表未涵蓋，四個年度端點中位於最高","upside_short_pct":5.8,"upside_mid_pct":34.3},"trap_analysis":{"verdict":"🟡","label":"高成長但現金轉換為負的循環高點"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Goldman 估五大 hyperscaler 每年需約 3,000 億美元 AI 營收才能打平，2027 年要靠約 4,000 億美元投資級債支應建置，2028 年 capex 成長放緩到 12%","assumption":"客戶 capex 到 2028 年後仍維持高檔","consequence":"2028–2029 年 EPS 回落到 105–120 元、倍數壓到 9 倍，股價約 945–1,080 元，五年虧損過半","ruling":"採納，作為空頭情境主軸，機率 30%。這條與唯一致命點（大客戶轉單）是不同事件，分開計算","watch":"hyperscaler 次年 capex 指引、投資級債發行量、月營收年增率","evidence_refs":["supply_demand_durability#5"],"fact_refs":["f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"論點成功但股東經濟變差","evidence":"德州據點投資由 1.52 億美元放大到 16 億美元以上，報導未說明 Amazon 是否出資；Q1 存貨約 2,292 億元，季增 68%；總資產由 3,382 億增到 4,326 億元；自由現金流 2024、2025 年與近十二個月都是負的；董事會核准 150 億元可轉債與 15 億美元聯貸","assumption":"營收成長會帶來對應的現金","consequence":"EPS 成長，但每股自由現金流與資本報酬下滑，可轉債稀釋吃掉部分 EPS 成長","ruling":"採納，這是本次不追的主因之一，用第三條假設（2028 年自由現金流率轉正）驗證","watch":"營業現金流、存貨季增率對營收季增率、可轉債轉換價","evidence_refs":["ems_utilization_capex_cycle#0","ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1"],"fact_refs":["f_peer_6669_tw_fcf_margin_pct","f_kpi5"]},{"view":"價格已反映太多","evidence":"26 週漲 91.56%；trailing 本益比 23.2 倍、市銷率 1.14、EV/S 1.21，三者都在自身四個年度端點的最高位","assumption":"高峰獲利的倍數不會收斂","consequence":"就算 2027 年 EPS 達標，倍數從 18.8 倍收斂到 13 倍也會吃掉大部分報酬","ruling":"部分採納。2027 年前瞻 12.6 倍不算貴，但基本情境已假設倍數收斂，五年約 +34%、年化約 6% 加股息，不足以補償循環風險","watch":"股價對 2027 年共識 EPS 的倍數","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_fwd_pe_latest"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 2275.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=2275.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"每股口徑","cause":null,"prior_field":null,"side_a":"公司新聞稿 Q2 EPS 80.43 元、FactSet 2026 EPS 中位數 348.72 元、外資目標價 6,600–7,568 元","side_b":"判斷日股價 2,275 元、Koyfin FY1 共識 120.95 元、trailing 本益比 23.2 倍、股息殖利率 2.13%，兩套每股數字相差約 2.9 倍","ruling":"可調和，屬口徑差異。估值與情境全程只用判斷日股價這一套；外資目標價與新聞稿每股數字不拿來和現價比較","evidence_level":"多源交叉，口徑差異的成因事實表未涵蓋","settle_metric":"公司公告的流通股數或面額變更","if_then":["若查明為股數變動，將外資目標價除以同一比例後再比較","若查明 Koyfin 共識換算有誤，重跑情境樹"],"evidence_refs":[]},{"axis":"毛利率方向","cause":null,"prior_field":null,"side_a":"Q2 毛利率升到 9.3%，公司歸因於記憶體改代採購與新產品 NRE 收入","side_b":"Q1 為 7.6%；台系 ODM 營收增速普遍高於毛利增速，緯穎 Q1 營收在五大裡排第四","ruling":"可調和，屬程度差異。管理層歸因不採信也不否定：代採購只是把營收移出、讓百分比變好看，NRE 屬一次性。標為未證、監測；若 2027 年第一季前連兩季毛利率低於 8%，視為歸因證偽","evidence_level":"公司新聞稿與二手產業報導","settle_metric":"季毛利率與毛利金額年增率","if_then":["若連兩季毛利率低於 8%，下修營益率假設並取消進場條件","若毛利金額年增率連兩季高於營收年增率，承認利潤率改善屬結構性"],"evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"axis":"需求持久度與融資","cause":null,"prior_field":null,"side_a":"記憶體、CoWoS 到 2027 年都供不應求，2027 年五大 capex 約 1.2 兆美元","side_b":"Goldman 估 2027 年要靠約 4,000 億美元債券支應，2028 年成長放緩到 12%","ruling":"可調和，屬時間差。2027 年以前需求有支撐，風險集中在 2028 年，所以基本情境 2029 年 EPS 持平","evidence_level":"賣方研究，多家一致","settle_metric":"五大 hyperscaler 2028 年 capex 指引","if_then":["若 2028 年 capex 指引年增仍高於 20%，空頭機率下修到 25%","若任一家年減逾 10%，取消進場條件"],"evidence_refs":["supply_demand_durability#5"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"2027 年前瞻本益比 12.6 倍、PEG 約 0.58；高盛估 AWS 相關份額約七成，AMD Helios 機櫃可拿三到四成；電力容量已鎖到 2028 年；分析師共識 2027 年營收約 2.1 兆元","side_b":"循環偏晚段，trailing 倍數在自身最高；自由現金流為負，擴張靠外部融資；前兩大客戶占 86%","ruling":"不可調和（買與不買方向相反），選 B 側：不追。依據是增量報酬已由 43%–59% 降到約 24%，新投入資本的報酬在下滑，而 2028 年 capex 成長預估只剩 12%","evidence_level":"財報推算加賣方研究","settle_metric":"股價對 2027 年共識 EPS 的倍數、2027 年共識修正、季營業現金流","if_then":["若股價續漲，但第三季毛利率與存貨沒有改善，則不追","若股價回落到 1,800 元以下，且 2027 年共識 EPS 未下修逾一成，重跑研究後分批反買","若連兩季營業現金流轉正、存貨增速低於營收增速，代表不追的判斷錯了：即使價格未回落，也在 2027 年第二季財報後重跑研究，考慮分批建立","若任一大客戶下修次年 capex 逾一成，取消進場條件，改為迴避"],"evidence_refs":["ems_utilization_capex_cycle#0"]}],"triggers":[{"n":1,"text":"2027 年 EPS 共識守住","type":"假設驗證","maps_to":"H1","metric":"FY2027 共識 EPS","threshold":"較 179.98 元下修逾 10%（低於 162 元）","action":"撤回進場條件，改為迴避並重跑研究","source_freq":"Koyfin 共識快照，每月","date":null},{"n":2,"text":"毛利率被擠壓","type":"風險","maps_to":"R1","metric":"季毛利率","threshold":"低於 7.0%，連兩季","action":"不建倉；已持有則減碼一半","source_freq":"公司季報，每季","date":null,"evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"n":3,"text":"存貨堆積領先營收","type":"風險","maps_to":"R5","metric":"存貨季增率減營收季增率","threshold":"高於 10 個百分點，連兩季","action":"停止加碼；已持有則減碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1"]},{"n":4,"text":"大客戶下一代專案主供轉給其他 ODM","type":"Single Thing","maps_to":"single_thing","metric":"單一客戶份額或月營收","threshold":"任一大客戶份額掉到三成以下，或月營收連兩月年減","action":"清倉並重跑研究","source_freq":"外資報告、月營收，每月","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":5,"text":"客戶 capex 轉向","type":"風險","maps_to":"R3","metric":"Meta、Microsoft、Amazon 次年 capex 指引","threshold":"任一家年減逾 10%","action":"不追；已持有則減碼","source_freq":"客戶季報，每季","date":null,"evidence_refs":["supply_demand_durability#5"]},{"n":6,"text":"墨西哥產能與關稅","type":"風險","maps_to":"R4","metric":"USMCA 待遇與客戶出貨地要求","threshold":"USMCA 待遇取消，或客戶再次要求停止自墨西哥出貨","action":"停止加碼並重估毛利率","source_freq":"政策公告與公司說明，事件型","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]},{"n":7,"text":"價格回落到可進場區","type":"估值rearm","maps_to":"H1","metric":"股價與 FY2027 共識 EPS","threshold":"股價 1,800 元以下，且 FY2027 共識 EPS 不低於 162 元","action":"重跑研究後小部位分兩批建立","source_freq":"每日股價、每月共識","date":null},{"n":8,"text":"擴張轉成現金","type":"假設驗證","maps_to":"H3","metric":"年度自由現金流率","threshold":"2028 年全年 ≥ +2%","action":"未達則不升級持有","source_freq":"公司年報，每年","date":null},{"n":9,"text":"第三季財報複審","type":"複審日期","maps_to":"H2","metric":"毛利率、存貨、營業現金流","threshold":"毛利率 ≥ 8% 且存貨增速不高於營收增速","action":"未達則維持不追","source_freq":"公司季報","date":"2026-11-15"}],"kill_metrics":[{"metric":"季毛利率","bear_threshold":"低於 7.0% 連兩季","window":"2026 年第三季到 2027 年第二季","source":"緯穎季度財報新聞稿","last_status":"ok"},{"metric":"存貨季增率減營收季增率","bear_threshold":"高於 10 個百分點，連兩季","window":"每季滾動","source":"緯穎法說簡報與資產負債表","last_status":"warning"},{"metric":"FY2027 共識 EPS","bear_threshold":"較 179.98 元下修逾 10%","window":"至 2027 年底","source":"Koyfin 共識快照","last_status":"unknown"},{"metric":"大客戶次年 capex 指引","bear_threshold":"Meta、Microsoft、Amazon 任一家年減逾 10%","window":"2027–2028 年","source":"各客戶季度財報","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=91.56, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價回落到 1,800 元以下（約 2027 年共識 EPS 的 10 倍），且 2027 年共識 EPS 未較 179.98 元下修超過 10%","exec_line":"兩條件同時成立才重跑研究，研究通過後首筆小部位、分兩批進場；期間任一大客戶下修 capex 逾一成即取消"},"reasoning":{"industry":"最新一季（2026 年第二季）營收 2,781.53 億元，年增 26.0%；毛利率 9.3%，營業利益率 7.3%，稅後淨利 149.69 億元。公司沒有給量化財測。營收結構方面，2025 年 AI 伺服器與通用伺服器各占約一半，AI 伺服器裡 ASIC 約占九成；管理層預期 2026 年 AI 占比過半。Q2 的年增率看起來放緩，有一部分是會計口徑造成：4 月起部分客戶的記憶體改由緯穎代採購，金額不再計入營收與成本。單點依賴是本案的核心風險而不是護城河。2024 年資料顯示 Meta 占 52%、Microsoft 占 34%，合計 86%；另有外資估計 AWS 相關 ASIC 份額約七成。產業時鐘判在擴張期（II）：TrendForce 估 2026 年 AI 伺服器出貨年增逾 28%，北美前五大 CSP capex 年增約 40%，記憶體與 CoWoS 都仍供不應求。供需持久度屬週期性，供不應求可延續到 2027 下半年至 2028 上半年；Goldman 預估 2028 年 capex 成長放緩到 12%，之後有反轉風險。","moat":"機制：緯穎直接替 hyperscaler 設計並整合 ASIC 機櫃，電力容量已鎖到 2028 年，在客戶下一代平台的導入速度有優勢。可證方向用利潤率差距衡量：近十二個月營業利益率 6.62%，對廣達 3.34%、緯創 3.8% 高約 3 個百分點；毛利率 8.2%，對兩家的 5.54%、5.85% 也較高；只略低於 SMCI 的 7.09%。不給向上的理由：自身營業利益率由 2024 年 7.8% 降到 6.62%，ROCE 由五年前 38% 降到 23%（2024 年資料）。不給向下的理由：最大客戶份額沒有下滑的來源證據，外資仍估 AWS 相關份額約七成。子評分：執行力 7、定價權 5。當期 ROIC 事實表未涵蓋（缺廠房設備與投入資本口徑）。產業態勢判為雙向拉鋸：競爭面，台系 ODM 營收增速普遍高於毛利增速，緯穎 Q1 營收在五大 AI 伺服器 ODM 裡排第四；結構面，供不應求延續到 2027 下半年；其他結構變數是客戶改直購記憶體，以及德州據點擴大投資由緯穎承擔。","growth":"成長來源以量為主：機櫃出貨量，加上 GPU、ASIC 內容增加帶動的單機價值；價格面多半是零組件轉嫁，不是議價。共識 EPS 三年路徑為 FY2026 120.95、FY2027 179.98、FY2028 226.58 元。基期取判斷日股價 2,275 元 ÷ trailing 本益比 23.2 ≈ 98.06 元，三年 CAGR 約 32.2%。內生天花板約 24%，缺口約 8 個百分點，無法歸因於利潤率擴張、淨回購或收購，實際是靠可轉債與聯貸撐起超過內生資金的再投資，屬依賴re-rate，長期信心上限為中。跑道方面，IDC 估 ODM 直供已占 Q1 伺服器營收約 50.2%，落在 35%–70% 區間；AMD Helios 是新客戶，不是新曲線，所以判中等，約五年。","governance":"自由現金流轉換率為負：2024 年自由現金流 −251 億元、淨利 228 億元；2025 年自由現金流 −146 億元、淨利 511 億元；近十二個月自由現金流率 −5.84%。2026 下半年資本支出預算 9.42 億美元，用於電力、設備、土地與廠房；同時核准上限 150 億元國內無擔保可轉債與 15 億美元聯貸。股息殖利率 2.13%。三項計分：近年沒有重大收購，收購報酬不適用；回購紀錄事實表未涵蓋，而且籌資方向與回購相反；員工酬勞股數事實表未涵蓋，可轉債將來有稀釋。現金去向四分與債務到期結構事實表未涵蓋。流動比率約 1.32 倍，短期償債沒有壓力。","valuation":"同一每股口徑下，前瞻本益比 FY2026 為 18.5 倍、FY2027 為 12.6 倍，PEG 約 0.58（18.52 ÷ 三年 CAGR 32.2）。若共識兌現，這個價位不算貴。不過 trailing 本益比 23.2 倍、市銷率 1.14、EV/S 1.21，三者都在自身四個年度端點的最高位；26 週已漲 91.56%。真正的五年分位事實表未涵蓋。上檔推算如下。短期：2027 年基本情境 EPS 172 元 × 14 倍 = 2,408 元，約 +5.8%。五年：2031 年基本情境 EPS 235 元 × 13 倍 = 3,055 元，約 +34.3%，年化約 6% 加股息。外資目標價 6,600–7,568 元是另一套每股口徑，不能直接拿來和現價比較。","premortem":"空頭路徑寫在反證紀錄的論點失敗那一條。最大回撤推算：過去四年唯一的下行年是 2023 年，營收年減 17.4%；空頭情境 2029 年 EPS 105 元 × 9 倍 = 945 元，較現價約 −58%；26 週漲 91.56% 若回吐一半，約 −24%。歷史最大回撤序列事實表未涵蓋。價值陷阱判黃燈：自由現金流連兩年為負屬亮燈，毛利率年度下滑為半亮。"},"plain":{"six":{"how_it_makes_money":"賺的是 hyperscaler 自建 AI 與通用伺服器的機櫃設計整合費，錢卡在兩個節點：客戶的 capex 決策，以及上游 GPU、ASIC、記憶體的供應。","moat":"護城河方向持平，等級 C。執行力領先台系同業，定價權有限，價值鏈分配正往客戶端移動。","growth":"Y5 之後的成長跑道屬中等：ODM 直供模式已占伺服器營收約一半，看不到 AI 機櫃以外的第二條曲線。","capital":"資本配置偏弱：擴張速度超過內生現金，靠可轉債與聯貸支應。","valuation":"現價要成立，需要 2027 年 EPS 照共識成長約 49%、2028 年再成長約 26%，而且市場仍給 12 倍以上。前半段我信，後半段不信。","how_wrong":"最可能看錯在 2028 年：客戶 capex 放緩時，現在堆起來的存貨、德州廠與可轉債會同時變成負擔。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不追，等股價回落到 1,800 元以下，且 2027 年共識 EPS 未下修超過一成","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"EMS/ODM","price_at_dd":2275.0,"week26_return_pct":91.56,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母有兩層爭議。第一是每股口徑：公司新聞稿 Q2 EPS 80.43 元、FactSet 2026 EPS 348.72 元，與判斷日股價 2,275 元、Koyfin FY1 120.95 元相差約 2.9 倍；本判斷只用後者這一套。第二是 2026–2027 年 EPS 落在 hyperscaler capex 高峰，高峰獲利配上低倍數不等於便宜"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"2026 年第三季財報","impact":"高","watch":"毛利率是否守在 8% 以上、存貨是否續增、營業現金流"},{"date":"2027-Q1","date_precision":"quarter","type":"macro","event":"Meta、Microsoft、Amazon 公布 2027 年 capex 指引","impact":"高","watch":"是否仍高於 2026 年"},{"date":"2027","date_precision":null,"type":"capacity","event":"德州第二棟廠量產，美國產能占比升到約兩成","impact":"中","watch":"折舊增加對毛利率的影響"},{"date":null,"date_precision":null,"type":"other","event":"上限 150 億元國內可轉債發行與 15 億美元聯貸動用","impact":"中","watch":"轉換價與稀釋幅度"}],"_projected_from":"v19"}
```
