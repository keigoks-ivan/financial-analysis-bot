你是 stock-analyst v20 的**散文層（prose）agent**，標的 HUBS（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：HUBS　日期：2026-11-08　archetype：None　前份裁決：2026-05-22　B 觀望（thesis 偏 observation；估值 5Y 分位 3% 極便宜但 Pure MA ❌ 盲點 2 救援失敗 + 4 家券商 5/8 同步降評；等 Q2 FY26 8/6 Customer Agent ARR 揭露）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1788B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（488B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（994B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1395B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（723B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（319B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（855B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2220B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1421B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2353B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1788           3648-5212      5 條（2–6 內）  
s3                  8000         488           5258-7512      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3112          8322-11888      5 條（2–6 內）  
s6                 11000         319          7477-10681      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         855           1851-2645      5 條（2–6 內）  
s10                 5000        2220           1946-2780      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2353           2000-2647      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4180B；至少需散文≈40.82KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−35
−35%
−32%
0
0%
0.04
0.16%
0.3
0.43
0.5
0.54
0.75
0.86
1
1%
1.1%
1.271
1.67
1.9
02
2
2%
2.1
2.2%
2.37
2.5
2.8
3
3%
3.49
3.63
3.81
4%
04
4
5
5%
05
5.08
5.2%
5.45%
6%
6
06
6.6%
07
7
7%
7.2
7.5
7.5%
7.6%
8
8%
08
8.5%
09
9%
9
9.46
9.476
9.60
9.71
10%
10
10.7
11
11.93
12
12%
12.1
12.6
12.7%
13.0%
13
13.3
13.4%
13.59
13.61
14
14%
14.5%
14.8
14.9
15%
15
15.08
15.1%
15.1
15.2
16%
16.8
16.82
17
17%
17.8
18%
18.89%
19%
19.6
20
20%
20.21
21
21.52%
21.56%
21.6
22
22.4
22.6%
23
23%
23.5%
24
24%
25%
25.4
25.9
27
27%
27.7%
28.1
30%
30.78%
31.3
31.6%
33%
34.49%
35%
35
36
37%
38%
40%
40
45%
45
48.46
49%
49
49.74%
50%
50
$50
52
55%
55.7
60%
62%
65%
68.8%
70
70.7%
73.08%
78%
80%
83.02%
83.76%
84.83%
85%
85.03%
85.4%
87.24
88%
88.74%
90
95%
98%
100%
100
101%
102%
104%
130
135
136.8
137
190
198.37
200.61
250
256.6
273.96
291
336
445.12
450
720
2024
2025
2026
2027
2028
2029
2030
2031
20261108
1,160
1,730
1,910
10,000
12,038
2,200
2,300
311,704
4,000
4,890
4,963
5,000
5,040
5,300
6,000
7,000
8,126
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
{"meta":{"ticker":"HUBS","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"HubSpot, Inc."},"oneliner":"客戶金額留存還穩，但淨留存、淨新增客戶與淨新增 ARR 一起轉弱，公司同時在降價；15 倍 non-GAAP 本益比扣掉股權報酬後並不便宜，等 2027 年 2 月的年度指引與 EMEA 試點結果再說。","thesis":{"H":[{"id":"H1","text":"安裝基礎止血：客戶金額留存守住高 80%，淨留存回到 102% 以上，淨新增 ARR 年增轉正。","2y":"2027 年淨留存 ≥102%，淨新增 ARR 年增轉正。","5y":null,"10y":null,"threshold":"FY2027 淨留存 ≥102%，客戶金額留存維持高 80%。","source":"季度財報電話會。","drift_rule":"連 2 季低於門檻為削弱，連 3 季低於 100% 為反轉；留存率波動小，5%／10% 的偏離過寬，改用絕對點數。"},{"id":"H2","text":"獲利品質改善：non-GAAP 營益率照承諾上升，同時 SBC 占營收下降。","2y":"FY2027 non-GAAP 營益率 23–24%，SBC 占營收 ≤12%。","5y":"FY2030 non-GAAP 30%、GAAP 20%、SBC 10%（公司目標，基準情境打折到 FY2031 的 27%）。","10y":null,"threshold":"FY2027 non-GAAP 營益率 ≥23%，SBC 占營收 ≤12%。","source":"2026-09-17 投資人日 CFO 與季度財報。","drift_rule":"2 年門檻：TTM 連 2 季偏離 ≥5% 為削弱，連 3 季 ≥10% 為反轉。5 年門檻：連 4 季偏離 ≥5% 為削弱，連 6 季 ≥10% 為反轉。"},{"id":"H3","text":"席位加 credit 的新定價帶來淨增量收入，而不是把舊收入重新切分。","2y":"2027 年底前揭露付費 credit 收入，試點區新 ARR 高於未試點區。","5y":"FY2031 營收成長 ≥7.5%。","10y":null,"threshold":"付費 credit 收入占訂閱營收 ≥3%，單客訂閱營收固定匯率年增 ≥3%。","source":"季度財報電話會與 EMEA 試點揭露（預計 2027 年 2 月）。","drift_rule":"2 年門檻：TTM 連 2 季偏離 ≥5% 為削弱，連 3 季 ≥10% 為反轉。到 2027 年底仍未揭露付費 credit 收入，視為削弱。"}],"R":[{"id":"R1","text":"2027 年指引低於市場：Q4 指引中位數已低於 Q3 實績，管理層說逆風延續到 2027 年。","h_ref":"H1","clock":"⚡","threshold":"FY2027 營收指引中位數年增 <9%，或單季淨新增客戶連 2 季 <4,000。","evidence_refs":["end_markets#2","capital_markets_pricing#0","supply_demand_durability#1"]},{"id":"R2","text":"定價改革把既有收入重新訂價：試點 ASP 較低，一旦推到既有客戶，影響約 36 億美元的訂閱收入。","h_ref":"H3","clock":"🔥","threshold":"單客訂閱營收固定匯率年增連 2 季 <1%，或宣布強制遷移既有客戶。","evidence_refs":["channel_business_model_shift#1"]},{"id":"R3","text":"通用 LLM 與 AI 原生 CRM 從低階客戶開始替代。","h_ref":"H1","clock":"🐢","threshold":"客戶金額留存低於 85% 或管理層不再稱高 80%。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0"]},{"id":"R4","text":"夥伴通路占營收約 49%，AI 壓縮夥伴的服務收入；公司同時要靠夥伴協助試用轉付費，自家專業服務收入卻在下滑。","h_ref":"H1","clock":"🔥","threshold":"夥伴及轉介客戶占營收低於 45%。","evidence_refs":["customer_concentration_credit#0","end_markets#0"]},{"id":"R5","text":"主要基礎設施集中在第三方雲端，FY2021 10-K 已揭露，2025-10-20 AWS us-east-1 中斷也證實這個風險仍在。","h_ref":"H1","clock":"🐢","threshold":"單次中斷影響主要區域超過 24 小時，且造成可量化的客戶補償。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R6","text":"法律與法規：律所調查尚未成案，CIPA 追蹤器訴訟有前例，州級 AI 法規各自為政。","h_ref":"H2","clock":"🐢","threshold":"證券集體訴訟獲認證，或單一州法規迫使主要 AI 功能停用。","evidence_refs":["regulatory_antitrust#2","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1"]},{"id":"R7","text":"AI 成本與股權報酬拖累獲利品質，營益率靠人力節省撐住。","h_ref":"H2","clock":"🔥","threshold":"TTM 毛利率 <80%，或 SBC 占營收回升到 14% 以上。","evidence_refs":["major_events#1"]}],"single_thing":{"description":"淨留存單季跌破 100%，代表既有客戶整體開始縮水。目前為 101%，全年看法已改為降約 2 點。","why_fatal":"這是基準情境最大的單一敏感度。每年少 1 點淨留存，五年後約少 5% 營收，FY2031 約 2.8 億美元，以 80% 流量換算每股約少 4 美元，占基準 EPS 約 15%；同年 1 點營益率只值約 1 美元。跌破 100% 後成長只能靠新客，而新客已在放慢，倍數也會跟著壓縮。","if_happens":"結論轉為不持有，已持有者清倉；重啟至少等連兩季回到 102%。","how_monitor":"每季財報電話會揭露的淨留存，下一次在 2027 年 2 月；同時看客戶金額留存與加購拖累的說法。","probability":"12–24 個月約 40%"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🔴","long_term_confidence":"低","fpe_fy2":11.93,"peg_fy2":0.43,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":9.71,"FY2026E":13.3,"FY2027E":16.82,"FY2028E":20.21},"fy_end_month":12,"eps_basis":"Non-GAAP 稀釋 EPS。FY2025A 由公司 FY2026 指引 13.59–13.61 美元與電話會所稱年增 40% 回推，約 9.71 美元，因年增率四捨五入約有 ±0.04 美元誤差；GAAP 0.86 美元為不同口徑。FY2026E 到 FY2028E 為 2026-11-07 Koyfin 共識快照，分析師家數事實表未涵蓋；FY2026E 13.3 美元低於公司新指引，快照應未更新 Q3。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"低","fingerprint":"營收成長仍有 17%、FCF 利潤率約 19%，但 GAAP 營益率僅 5.45%，成長正往 12% 換檔，定價與產品同時轉型。"},"industry":{"clock_phase":"IV","sd_verdict_source":"結構性持久為主：AI 改變買方找軟體的方式，入站獲客受壓屬結構性；預算排擠偏週期，但管理層 2026-08-05 與 2026-09-17 都說不出緩解時點。判 IV 的依據是淨新增 ARR 年減與客戶更在意價格，不是股價。","bargaining":{"up":"上游是模型與雲端。模型中立降低單一供應商風險，但 CFO 說 2027 年 COGS 成長快於營收。","down":"客戶分散，沒有單一大客戶；下市場對價格敏感，上市場決策層級提高，議價力往客戶移。","geo":"國際營收占 49%，地緣議價證據事實表未涵蓋。"},"profit_pool_dir":"有往模型層流出的跡象，毛利率 85.03%→83.76%→83.02%；五年利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表沒有 CRM 與 SMB 行銷軟體的份額和滲透率，只有 Gartner 二手的企業應用軟體總額（2026 年 4,963 億美元、2030 年 8,126 億美元），無法拆成 TAM、SAM、滲透率與利潤池占比。"}},"moat":{"mechanism":"CRM 資料與多產品整合的轉換成本（客戶金額留存高 80%），搭配入站獲客與占營收約 49% 的夥伴通路。","execution":7,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"淨留存 102%→101%，全年改為降約 2 點；淨新增客戶 7,000→5,300→低於 5,000；12 萬美元以上大單年增 38%→19%；2026 年淨新增 ARR 年減。","peer_na_reason":"事實表只有同業利潤率，沒有投入資本，無法計算 ROIC 差距。","threats":[{"level":"🔴","text":"通用 LLM、AI 原生 CRM 與 vibe coding 自建：10-K FY2025 新增列入競爭來源，部分新創已不用 HubSpot。目前沒有量化搶單或留存下滑的證據，屬生態攻擊，還不到架構替代。","p":35,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0"]},{"level":"🟡","text":"席位轉用量或成果計價：Gartner 轉述 2030 年前逾 40% 企業 SaaS 支出脫離純席位，Ramp 資料則顯示目前仍以席位為主。公司正主動遷移，風險在收入重訂價。","p":40,"evidence_refs":["supply_demand_durability#2","channel_business_model_shift#1"]}],"roic_durability":{"quadrant":"無法判定：GAAP 營益率 5.45% 屬低利益率，投入資本周轉率事實表未涵蓋。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是行銷與銷售團隊，決策者在上市場已升到 CEO、CTO 與董事會，付款者在下市場變得更省。需要 CRM 的問題還在，高 80% 的客戶金額留存是證據；加購和版本升級可以延後，Q3 已轉成拖累。"},{"item":"決策層級","level":"🟡","text":"最小決策單位是每年續約時的席位與版本。Starter 約 15 萬家，約占客戶數一半，轉換成本低；Pro+ 較黏，62% 新 Pro+ 客戶一開始就買多個產品。多數合約一年以內，降級在續約時就會反映。"},{"item":"價值鏈分配","level":"🟡","text":"模型與雲端拿走的份額在增加：CFO 說 2027 年 COGS 成長快於營收，毛利率兩年降 2 點。連接器把介面交給 ChatGPT 與 Claude，目前工作仍寫回 HubSpot，Q3 建立 2,200 萬筆物件。毛利率若低於 80% 就轉紅。"},{"item":"社會容忍度","level":"🟢","text":"企業軟體沒有社會定價上限問題，定價限制來自客戶預算。州級 AI 法規與隱私執法屬合規成本，事實表未見針對 HubSpot 的調查。"}],"roiic":"事實表未涵蓋投入資本，無法計算","reinvest_rate":"事實表未涵蓋折舊與營運資金變動，無法計算","endo_ceiling":null,"formula_note":"當期 ROIC、增量 ROIC 與再投資率都缺輸入數字，不以估算代替。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","HUBS":83.02,"CRM":77.28,"NOW":73.08,"TEAM":84.83,"MNDY":88.74,"unit":"%"},{"metric":"營業利益率","HUBS":5.45,"CRM":21.52,"NOW":9.68,"TEAM":0.16,"MNDY":2.9,"unit":"%"},{"metric":"FCF 利潤率","HUBS":18.89,"CRM":34.49,"NOW":30.78,"TEAM":20.07,"MNDY":21.56,"unit":"%"},{"metric":"研發密度","HUBS":25.2,"CRM":14.49,"NOW":22.47,"TEAM":49.74,"MNDY":26.03,"unit":"%"}],"competitors":[{"name":"CRM","gm":77.28,"om":21.52,"fcf_margin":34.49,"rd_intensity":14.49,"strategy_note":"營益率 21.52%、FCF 利潤率 34.49%，獲利能力高於 HubSpot，靠收購補 agent，是上市場最直接的對手。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"NOW","gm":73.08,"om":9.68,"fcf_margin":30.78,"rd_intensity":22.47,"strategy_note":"毛利率 73.08% 低於 HubSpot，FCF 利潤率 30.78%，與 SMB 客群的重疊程度事實表未涵蓋。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"TEAM","gm":84.83,"om":0.16,"fcf_margin":20.07,"rd_intensity":49.74,"strategy_note":"毛利率 84.83% 相近，營益率僅 0.16%，研發密度 49.74%，GAAP 獲利接近零。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MNDY","gm":88.74,"om":2.9,"fcf_margin":21.56,"rd_intensity":26.03,"strategy_note":"毛利率 88.74%、FCF 利潤率 21.56%，與 HubSpot 的客戶重疊與份額事實表未涵蓋。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（客戶 +12%），價為輔（單客訂閱營收 +4%），併購可忽略；EPS 另受營益率擴張與回購推升。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋投入資本與再投資率，內生上界無法推導，情境以保守方式視為已超過。共識 EPS 與營收的差距可歸因於營益率擴張和回購。","segments":[{"item":"訂閱營收 Q3 年增","value":"18%"},{"item":"專業服務及其他 Q3","value":"1,730 萬美元，年減 3%"},{"item":"國內營收 Q3 年增","value":"16%"},{"item":"國際營收 Q3 年增","value":"18%，占營收 49%"}],"decay_signals":[{"item":"毛利率連兩季年減","lit":true,"evidence":"年度與 TTM 毛利率 85.03%→83.76%→83.02%，CFO 預告 2027 年 COGS 成長快於營收；單季序列事實表未涵蓋，以年度趨勢判定。"},{"item":"核心市占近 12 個月縮減","lit":false,"evidence":"事實表未涵蓋份額資料。"},{"item":"主力產品提價後銷量下滑","lit":false,"evidence":"公司是在降價，不是提價。"},{"item":"EPS CAGR 高於營收 CAGR 逾 5 點","lit":true,"evidence":"2025 至 2027 年相差 17 點。"},{"item":"FCF／淨利連兩年低於 0.75","lit":false,"evidence":"FCF 遠高於 GAAP 淨利，其中部分來自 SBC。"},{"item":"SBC 占營收逾 5% 且逐年上升","lit":false,"evidence":"Q3 為 13.4%，但占比年減逾 3 點，條件不成立。"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"Gartner 二手資料估計代理式 AI 到 2030 年侵蝕傳統應用軟體 1,160 億美元，但企業應用軟體總額仍成長，列入觀察。"},{"item":"產業估值倍數近三年系統性下移","lit":false,"evidence":"同業倍數事實表未涵蓋，只能看到本公司 P/S 為四個年度端點最低。"},{"item":"維持性資本支出占 FCF 逾 60%","lit":false,"evidence":"資本支出占營收 5–6%，約 2 億美元，不到 FCF 7.2 億美元的 30%。"},{"item":"停止投資新產能且收入三年內下滑","lit":false,"evidence":"不適用，收入仍在成長。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，事實表僅見一筆 1,910 萬美元收購；三年現金去向事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2026-04 收購 Futurepedia 僅 1,910 萬美元，沒有回報資料，其他收購事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"2026 年累計回購近 10 億美元；回購均價與 10 年期公債殖利率事實表未涵蓋，無法計算買入收益率。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"全年稀釋股數假設 5,040 萬，Q4 假設 4,890 萬，股數淨減。前提是回購大於 SBC；只看 SBC，年化約 5.08 億美元，約市值 5.2%。","grade":"過"}]},"valuation":{"basis":"non-GAAP Fwd P/E 為主，同時對照 GAAP trailing P/E 與 FCF 扣 SBC 後的收益率。","tier":"SMB 應用軟體，成長換檔中","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法做同級比較。"},"fwd_pe":15.08,"peg":0.54,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"PEG 0.54（15.08 倍除以 FY2025A 到 FY2028E 的 EPS CAGR 27.7%）與 15.08 倍看來便宜，但分母沒有扣 SBC，GAAP trailing P/E 為 48.46 倍。分母正是爭點，便宜論證不成立，結論只給中性。五年分位事實表未提供。","upside_short_pct":9,"upside_mid_pct":45},"trap_analysis":{"verdict":"🟡","label":"成長換檔中的中度陷阱風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"入站獲客受壓，淨留存連降，淨新增 ARR 年減；10-K 新增 AI 原生 CRM 與通用 LLM 為競爭來源，部分新創已不用 HubSpot。","assumption":"基準情境假設客戶金額留存維持高 80%，流失只發生在邊際客戶。","consequence":"5 年後虧 50% 最可能的路徑：Starter 與 Pro 客戶改用 LLM 加輕量資料庫，淨留存掉到 95% 附近，營收成長低個位數，倍數壓到 7–9 倍。","ruling":"採納。這條與唯一致命數字（淨留存跌破 100%）部分重疊，門檻已寫進觸發條件。目前沒有份額流失的量化證據，所以 Bear 機率放 35%，沒有更高。","watch":"客戶金額留存是否仍稱高 80%、Starter 客戶數、淨新增客戶。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","supply_demand_durability#1"],"fact_refs":["f_kpi7"]},{"view":"論點成功但股東經濟變差","evidence":"CFO 在 2026-09-17 說 2027 年 COGS 成長快於營收；試點 ASP 較低；毛利率 85.03%→83.76%→83.02%；2026 年 10 月裁員約 7%，省下的錢有相當部分再投入留才與 AI。","assumption":"credit 定價高於模型成本，且付費用量夠大。付費與內含比例管理層在 2026-08-05 沒回答。","consequence":"agent 用得很好，但毛利率掉到 78% 左右。FY2031 營收 55.7 億美元下，5 點毛利率約少 2.8 億美元營業利益、每股約 5 美元，約占基準 EPS 18%。","ruling":"部分採納。管理層重申 2027 年營益率 23–24%，短期可靠人力成本抵銷，長期不能一直裁員，所以基準情境只給到 27%。","watch":"毛利率、SBC 占營收、付費 credit 是否揭露。","evidence_refs":["major_events#1","channel_business_model_shift#1"],"fact_refs":["f_peer_hubs_gross_margin_pct","f_kpi6_sbc"]},{"view":"價格已反映太多","evidence":"15.08 倍 non-GAAP 看似已反映壞消息，但 GAAP trailing P/E 48.46 倍，FCF 扣年化 SBC 後收益率約 2.2%。賣方 8 月目標價均值 273.96 美元定於 Q3 之前，EPS 快照近兩份沒有修正。","assumption":"市場繼續用 non-GAAP 倍數看這家公司，且 FY2027 EPS 共識 16.82 美元不再下修。","consequence":"分母改成扣 SBC 後，市場給的並不是低價；共識下修時地板跟著往下。","ruling":"採納。現在就買的最強論證：EV／FCF 約 12 倍、淨現金 10.7 億美元，2027 年營益率已被重申，試點有效，逆風有一部分是公司自己選的，留存一旦止跌，倍數有機會回到 20 倍。本次不採納這個論證，因為決勝數據 2027 年 2 月才到，Q3 利空還沒進 EPS 模型，先等第一個確認數據點。","watch":"賣方 EPS 與目標價更新、2027 年 2 月指引。","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_consensus_rev_fy1_pct","f_kpi6_sbc"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 198.37 → 本次 200.61（+1.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=198.37","side_b":"本次 price_at_dd=200.61","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 198.37 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 198.37 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 198.37 美元：Bull 價 720、Bear 價 136.8，五年期望值 +70.7%，基準年化 13.0%，不對稱比 3.63","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.63。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 198.37 美元：五年期望值 +70.7%，基準年化 13.0%，不對稱比 3.63","side_b":"本次情境、股價 200.61 美元：五年期望值 +68.8%，基準年化 12.7%，不對稱比 3.49","ruling":"再換股價、情境不動：起點價上漲 1.1%，五年期望值少 1.9 個百分點，基準年化少 0.3 個百分點，不對稱比由 3.63 降到 3.49。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：短期獲利防線","cause":null,"prior_field":null,"side_a":"2026-08-05 CEO 說 2027 年營益率擴張 2–3 點，2026-09-17 CFO 給 23–24%，2026-11-04 CFO 再次確認。","side_b":"Q3 營益率 22.6%，Q4 指引約 23%，裁員約 7%。","ruling":"兩邊一致，屬可調和。2027 年目標接近 Q4 退出水準，達成難度不高；短期 EPS 下修風險主要來自營收。","evidence_level":"高，公司財報與電話會。","settle_metric":"FY2027 non-GAAP 營益率。","if_then":[],"evidence_refs":[]},{"axis":"不可調和：AI 是增量還是替代","cause":"新證據","prior_field":null,"side_a":"管理層：月 credit 用量年初至今增近 2.5 倍，連接器客戶留存高 13 點、席位升級 3 倍，headless 對 HubSpot 是加分。","side_b":"收入指標相反：淨留存降到 101%，2026 年淨新增 ARR 年減，入站獲客受壓，加購轉為拖累。","ruling":"不可裁決至 2027 年 2 月，暫採收入指標這一邊。依據是使用量可能來自內含額度，付費比例沒有揭露，連接器留存又有自選偏誤。硬數據點是淨留存、淨新增 ARR 與付費 credit 收入。","evidence_level":"中，使用量由管理層自述，收入指標為財報揭露。","settle_metric":"淨留存連兩季 ≥102%，單季淨新增 ARR 年增轉正，付費 credit 收入揭露。","if_then":["若連兩季淨留存 ≥102%、客戶金額留存仍為高 80%、淨新增 ARR 年增轉正，則重跑完整判斷，通過後首筆不超過 2%。","若淨留存單季跌破 100%，則不建倉，已持有者清倉。","若股價先站上 52 週線 256.6 美元而留存未改善，則不追。","若股價續跌但重啟條件未成立，則不分批反買，維持不建倉。"],"evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"axis":"管理層口徑七週內改變","cause":"新證據","prior_field":null,"side_a":"2026-08-05 CFO：全年淨留存大致持平，淨新增 ARR 成長低於固定匯率營收成長，FCF 約 7.5 億美元；2026-09-17 CFO 仍說淨留存大致持平，FCF 7.5 億美元，大單年增 38%。","side_b":"2026-11-04 CFO：全年淨留存降約 2 點，淨新增 ARR 年減，FCF 約 7.2 億美元；CEO 說大單年增 19%。","ruling":"採信新數字，投資人日的說法在七週內失效，管理層對 2027 年的樂觀描述要打折。Q4 指引仍可能偏保守，兩者不互斥。","evidence_level":"高，電話會原話。","settle_metric":"2027 年 2 月實績與指引。","if_then":["若 Q4 營收低於 9.60 億美元，則視為指引不再保守，維持不建倉。"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"管理層歸因：刻意取捨的短期代價","cause":"新證據","prior_field":null,"side_a":"管理層把試用與定價改革列為刻意取捨，短期拖累、長期有利，並以 2024 年席位降價後留存改善為例。","side_b":"壓力自 Q2 起連兩季加重，2026-08-05 CEO 說不出緩解時點，2026-09-17 CEO 也說 2027 年還太早判斷；試用延長採購週期只能解釋一部分。","ruling":"不採信也不否定，標記為未證、監測。預登記：到 2027 年 Q2 財報（約 2027-08），淨留存仍 ≤101% 且單季淨新增客戶 ≤5,000，這項歸因視為不成立。","evidence_level":"中。","settle_metric":"2027-08 前的淨留存與淨新增客戶。","if_then":["若到 2027-08 兩項都未改善，則判定歸因不成立，維持不建倉，已持有者減碼一半。"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"賣方共識與本次判斷","cause":"新證據","prior_field":null,"side_a":"8 月目標價均值 273.96 美元、中位 250 美元、區間 190–450 美元，最高最低比 2.37 倍；均值高於現價 37%，方向上反對本次結論。","side_b":"本次不進場，因 Q3 後的逆風尚未反映在 EPS 快照，快照 13.3 美元甚至低於公司新指引。","ruling":"分歧在框架。目標價隱含倍數回到約 20 倍，本次認為淨留存止跌前沒有理由回到 20 倍。不主張市場現在的低倍數是錯的。","evidence_level":"中，目標價資料停在 2026 年 8 月。","settle_metric":"Q3 後賣方 EPS 與目標價更新。","if_then":["若 FY2027 EPS 共識更新後仍 ≥16.8 美元且 2 月營收指引 ≥10%，則保留重啟機會。","若共識下修超過 5%，則同步下移 Bear 錨，維持不追。"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭：10-K 新增 AI 原生 CRM 與通用 LLM，目前缺量化搶單資料。結構轉好：Gartner 估 2026 年全球軟體支出年增 15.1%，Ramp 資料顯示席位侵蝕慢於言論。","side_b":"其他結構變數：商業模式由席位轉席位加 credit，買方發現軟體的通路改由 AI 中介。","ruling":"其他結構變動中，指商業模式與通路兩項；競爭惡化尚無量化證據。依據是 Q3 電話會對入站需求與定價的說明。","evidence_level":"中。","settle_metric":"付費 credit 收入與入站以外的獲客占比。","if_then":[],"evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2"]},{"axis":"基本面判斷變動","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5"],"side_a":"2026-05-22：訊號 B、觀望、陷阱中度，護城河方向與跑道未評。","side_b":"2026-11-08：訊號 C，護城河收窄，跑道中等，陷阱中度；股價幾乎沒動（198.37→200.61 美元）。","ruling":"變動來自兩次財報，不是股價。前份假設 ARR 年增 ≥18% 已被 Q3 billings 年增 15% 與 Q4 營收年增 12% 否定，前份的淨新增門檻也已觸發。","evidence_level":"高。","settle_metric":"2027 年 2 月財報。","if_then":[],"evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"axis":"估值方法與情境欄位","cause":"方法變動","prior_field":["val","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份以五年估值分位 3% 判偏便宜，公司類型、循環位置、情境機率與回撤範圍未填。","side_b":"本次把 SBC 納入分母比較，便宜論證不成立，結論改中性；公司類型定為品質複利成長（低信心），循環位置不適用，情境機率與回撤範圍首次填入。","ruling":"屬方法變動。股價與前份幾乎相同，估值結論下修不是因為變貴，而是分母的爭點被納入。","evidence_level":"中。","settle_metric":"SBC 占營收與 GAAP 營益率。","if_then":[],"evidence_refs":[]},{"axis":"重啟與加碼門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重啟門檻，只寫等 2026-08-06 Customer Agent ARR 揭露。","side_b":"三項同時成立才重跑判斷：淨留存連兩季 ≥102%，客戶金額留存仍為高 80%，單季淨新增 ARR 年增轉正。","ruling":"舊等待事件沒有帶來揭露，所以改用公司確實會揭露的留存指標；重啟後也只是重跑判斷，不會直接加碼。","evidence_level":"高。","settle_metric":"季度留存指標。","if_then":[],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"連 2 季 net add < 10,000；NRR 連 2 季 < 100%；Gross retention < 88%","side_b":"單季淨新增客戶連 2 季 <4,000；淨留存單季 <100%；客戶金額留存低於 85% 或管理層不再稱高 80%。","ruling":"舊的淨新增門檻已觸發（Q2 7,000、Q3 5,300），這個觸發不撤銷，是本次不進場的理由之一。新門檻用於下一階段的減碼與清倉判斷。淨留存改為單季觸發，比舊門檻更嚴。客戶金額留存公司只揭露區間，88% 無法核對，所以改用可觀察的說法。","evidence_level":"高。","settle_metric":"季度財報電話會。","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"淨留存單季跌破 100%。","ruling":"本次依敏感度選定：每年少 1 點淨留存，FY2031 EPS 約少 4 美元；同年 1 點營益率約 1 美元。","evidence_level":"中，敏感度為本次推算。","settle_metric":"季度淨留存。","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"前份假設門檻更換","cause":"新證據","prior_field":["H1","H3"],"side_a":"H1：FY26 全年 ARR ≥ +18% YoY；FY27 guide ≥ +15%。H3：Q4 FY26 Customer Agent ARR 揭露 ≥ $50M。","side_b":"H1：FY2027 淨留存 ≥102%，客戶金額留存維持高 80%。H3：付費 credit 收入占訂閱營收 ≥3%，單客訂閱營收固定匯率年增 ≥3%。","ruling":"舊 H1 已被實績否定。舊 H3 的 ARR 公司沒有揭露，無法驗證，改用公司的新定價架構與可揭露指標。","evidence_level":"高。","settle_metric":"2027 年季度揭露。","if_then":[],"evidence_refs":["end_markets#2"]}],"triggers":[{"n":1,"text":"Q4 財報與 2027 年首次年度指引","type":"複審日期","maps_to":"H1","metric":"FY2027 營收指引中位數年增、營益率指引、淨留存","threshold":"營收 ≥10%，營益率 ≥23%，淨留存 ≥101%","action":"三項達標才開始累計重啟條件，任一未達則不追","source_freq":"公司財報，季度","date":"2027-02","evidence_refs":["end_markets#2","capital_markets_pricing#0"]},{"n":2,"text":"淨留存跌破 100%","type":"Single Thing","maps_to":"Single Thing","metric":"淨留存","threshold":"單季 <100%","action":"不建倉，已持有者清倉","source_freq":"財報電話會，季度","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":3,"text":"重啟條件三項同時成立","type":"估值rearm","maps_to":"H1","metric":"淨留存、客戶金額留存、單季淨新增 ARR","threshold":"連兩季淨留存 ≥102%，客戶金額留存仍為高 80%，淨新增 ARR 年增轉正","action":"重跑完整判斷，不直接建倉，通過後首筆不超過 2%","source_freq":"財報電話會，季度","date":null,"evidence_refs":[]},{"n":4,"text":"客戶金額留存轉弱","type":"清倉","maps_to":"R3","metric":"客戶金額留存","threshold":"管理層不再稱高 80%，或低於 85%","action":"已持有者清倉，重啟條件歸零","source_freq":"財報電話會，季度","date":null,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"n":5,"text":"獲利承諾未兌現","type":"假設驗證","maps_to":"H2","metric":"FY2027 non-GAAP 營益率、SBC 占營收","threshold":"營益率 ≥23%，SBC ≤12%","action":"任一未達，已持有者減碼一半","source_freq":"公司財報，年度","date":"2028-02","evidence_refs":[]},{"n":6,"text":"EMEA 試點結果與推行時程","type":"假設驗證","maps_to":"H3","metric":"試點區新 ARR、既有客戶遷移安排","threshold":"試點區新 ARR 高於未試點區，且沒有強制遷移既有客戶","action":"未達則不追","source_freq":"財報電話會","date":"2027-02","evidence_refs":["channel_business_model_shift#1"]},{"n":7,"text":"證券訴訟從律所調查變成正式案件","type":"風險","maps_to":"R6","metric":"已提起訴訟、法院認證、和解金額","threshold":"集體認證加不利和解；或刑事介入","action":"集體認證加不利和解則減碼一半；刑事介入則清倉","source_freq":"SEC 文件與法院紀錄，事件","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0","lawsuit_class_action#1"]},{"n":8,"text":"夥伴通路占比下降","type":"風險","maps_to":"R4","metric":"夥伴及轉介客戶占營收","threshold":"FY2026 10-K 低於 45%","action":"已持有者減碼一半","source_freq":"10-K，年度","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":9,"text":"價格先走、證據未到","type":"風險","maps_to":"R1","metric":"週收盤價相對 52 週線","threshold":"站上 256.6 美元而重啟條件未成立","action":"不追","source_freq":"週線","date":null,"evidence_refs":[]}],"kill_metrics":[{"metric":"淨留存（NRR）","bear_threshold":"單季低於 100%","window":"單季","source":"季度財報電話會","last_status":"warning"},{"metric":"客戶金額留存","bear_threshold":"低於 85% 或管理層不再稱高 80%","window":"單季","source":"季度財報電話會","last_status":"ok"},{"metric":"單季淨新增客戶","bear_threshold":"低於 4,000 家","window":"連 2 季","source":"公司財報","last_status":"warning"},{"metric":"FY2027 營收指引中位數年增","bear_threshold":"低於 9%","window":"2027 年 2 月","source":"公司財報","last_status":"unknown"},{"metric":"FY2027 non-GAAP 營益率","bear_threshold":"低於 23%","window":"FY2027","source":"公司財報","last_status":"unknown"},{"metric":"TTM 毛利率","bear_threshold":"低於 80%","window":"TTM","source":"公司財報","last_status":"warning"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"三項同時成立才重跑判斷：淨留存連兩季≥102%，客戶金額留存仍為高80%，單季淨新增ARR年增轉正","exec_line":"目前不建倉，不設進場價，等 2027 年 2 月財報；已持有者停止加碼，淨留存跌破 100% 就清倉。"},"reasoning":{"industry":"最新一季營收 9.476 億美元，年增 17%，其中訂閱年增 18%，專業服務及其他 1,730 萬美元、年減 3%。訂閱占營收 98%，多數合約一年以內。non-GAAP 營益率 22.6%，GAAP 僅 7.6%，訂閱毛利率 85.4%。客戶 311,704 家、年增 12%，新增主要來自低價 Starter，單客訂閱營收 12,038 美元、年增 4%。Q4 指引中位數 9.46 億美元，低於 Q3 實績，年增率降到 12%，管理層明講逆風延續到 2027 年。單點依賴有兩個：Solutions Partners 及其轉介客戶占 2025 年營收約 49%，既是護城河也是集中度風險；主要基礎設施放在 AWS us-east-1，2025 年 10 月已出過事。可能看錯：Q3 實績高於指引上限約 2,300 萬美元，若 Q4 也如此，年增率約 15%，12% 的退出成長率就言過其實。","moat":"機制是 CRM 資料加多產品整合形成的轉換成本，再加入站獲客與夥伴通路。執行力穩定（7 分）：Q3 non-GAAP 營益率年增 3 點，20% 的 Pro+ 客戶使用 agent，但 2026 年留存與 ARR 看法兩度下修。定價力縮減（5 分）：淨留存由 Q2 的 102% 降到 101%，全年看法由大致持平改成降約 2 點；加購、聯絡人級距與版本升級已抵銷席位升級；agent 由每對話 1 美元改成每解決 0.5 美元，新客 Starter 與 credit 折扣 65%，試點區 ASP 較低。毛利率 85.03%→83.76%→83.02%。AI 新進者的威脅另記在威脅等級，不在趨勢重複扣分。同業 ROIC 差距取不到，改用留存與 ASP 當比較軸；FCF 利潤率 18.89%，低於 CRM 的 34.49% 與 NOW 的 30.78%。AI 曝險看兩點：淨增量的分界點是 2027 年底，屆時付費 credit 收入要大於定價改革讓出的收入；附著點的分界點是 2029 年，看工作是否仍寫回 HubSpot 的資料。反例：客戶金額留存穩在高 80%，使用連接器的客戶留存高 13 點，但這群客戶本來就較活躍，有自選偏誤；若 2027 年留存與加購止跌，趨勢應改回穩定。","growth":"成長以量為主：客戶年增 12%，單客訂閱營收年增 4%，併購可忽略。共識 EPS 由 FY2025A 約 9.71 美元到 FY2028E 20.21 美元，三年 CAGR 27.7%。FY2025A 到 FY2027E 的 EPS CAGR 31.6%，同期營收 CAGR 14.5%，差 17 點，來自營益率上升與股數下降，可以歸因，但不是營收帶來的。跑道無法用滲透率算，事實表只有企業應用軟體總額。第二曲線是 credit：月用量年初至今增近 2.5 倍，但付費與內含比例沒有揭露，2026 年淨新增 ARR 還在年減，不能算已證實。也沒有證據顯示市場已飽和，所以判中等。可能看錯：EMEA 試點的 Pro+ 客戶量和 credit 用量若能在全球複製，跑道應升一級。","governance":"2026 年累計回購近 10 億美元，高於全年 FCF 指引約 7.2 億美元，現金及有價證券為 13 億美元。FCF 指引由 7.5 億美元下修到 7.2 億美元，管理層沒有說明原因，同期有 6,000–7,000 萬美元遣散費。Q3 SBC 1.271 億美元，占營收 13.4%，年減逾 3 點；年化約 5.08 億美元，約占 FCF 七成，扣掉後 FCF 約 2.1 億美元。稀釋股數由全年假設 5,040 萬降到 Q4 假設 4,890 萬。2026 年 8 月新授權是 24 個月 10 億美元，每年約 5 億美元，差不多只抵銷 SBC。FY2025 FCF／GAAP 淨利 12.6 倍沒有參考價值，因為淨利太小。三年現金去向、債務到期與回購均價事實表未涵蓋。2030 年 SBC 占營收 10% 的目標是檢驗點。","valuation":"現價 200.61 美元等於 FY1 共識 15.08 倍、FY2 11.93 倍、EV／FCF 約 12.1 倍（EV 87.24 億美元、FCF 約 7.2 億美元）。同一家公司的 GAAP trailing P/E 是 48.46 倍，FCF 扣掉年化 SBC 後收益率約 2.2%。便宜與否取決於 SBC 算不算成本，這正是爭點，所以不把便宜當進場理由。Base 用 13 倍，低於現值，報酬全部來自 EPS 成長。五年分位事實表沒有，年度端點的 0% 只有 2 到 4 個點，不算五年分位。EPS 快照 13.3 美元低於公司新指引 13.59–13.61 美元，近兩份快照修正幅度為 0，Q3 的利空應該還沒進模型。護城河收窄時 Bear 錨不穩定，每次下修地板就下移，上下檔比只供參考，不作進場依據。可能看錯：Q4 指引若如過去一樣保守，年增率約 15%，現價就確實偏低。","premortem":"衰退信號亮兩個，毛利率下滑與 EPS 成長高於營收成長，對應中度陷阱風險。淨留存在降，但客戶金額留存仍穩，兩條留存線沒有同時下滑，所以沒有升到高風險；客戶金額留存轉弱就要升級。成長熄火測試以 FY2029 EPS 計：成長降到 15%，22.4 美元乘 15 倍得 336 美元；降到 10%，乘 13 倍得 291 美元；降到 5%，約 15 美元乘 9 倍得 135 美元，跌 33%。三項過兩項。付費 credit 比例管理層至今沒回答，是最大的資訊缺口。歷史最大回撤事實表未涵蓋，只知道現價比 250 週線 445.12 美元低 55%。"},"plain":{"six":{"how_it_makes_money":"賺中小企業行銷、銷售與客服團隊的訂閱費，錢卡在 CRM 資料加多產品整合這一節點；新客與加購兩個入口正在變窄。","moat":"護城河收窄（↓）：客戶黏著還在，定價力與新客入口退步。","growth":"Y5 之後跑道中等（🟡）：滲透率資料缺，第二曲線 credit 還沒證明能賺錢。","capital":"資本配置中等：今年回購大於 FCF，股數下降，但往後的授權額度大約只夠抵銷股權報酬。","valuation":"現價要求 FY2031 non-GAAP EPS 約 27 美元（屆時 13 倍）才有年化 12%；算得到，但前提是淨留存先止跌，這點目前信不過。","how_wrong":"最容易看錯的是降速的性質：是轉型期還是護城河收窄，要到 2027 年 2 月才分得清。"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等事件，不等價位：連兩季淨留存 ≥102%，客戶金額留存仍為高 80%，單季淨新增 ARR 年增轉正；第一個檢查點是 2027 年 2 月財報。","trap":"🟡","val":"🟡","moat":"C","moat_trend":"↓","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":200.61,"week26_return_pct":1.66,"consensus_rev_3m_pct":0.15,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"non-GAAP EPS 排除占營收 13.4% 的 SBC。Q3 non-GAAP EPS 3.81 美元，GAAP 1.67 美元；FCF 扣年化 SBC 後對市值收益率約 2.2%，遠低於 FY1 本益比隱含的 6.6%。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年首次年度指引","impact":"高","watch":"營收成長、營益率指引、淨留存與淨新增客戶"},{"date":"2027-02","date_precision":"month","type":"product","event":"EMEA 席位加 credit 試點結果與後續推行時程","impact":"高","watch":"試點區新 ARR、ASP、既有客戶是否遷移"}],"_projected_from":"v19"}
```
