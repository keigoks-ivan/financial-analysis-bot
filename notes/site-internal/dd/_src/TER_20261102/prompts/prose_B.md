你是 stock-analyst v20 的**散文層（prose）agent**，標的 TER（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：TER　日期：2026-11-02　archetype：None　前份裁決：2026-06-26　觀望｜條件式衛星持倉　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2146B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（1163B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（998B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1491B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1017B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（593B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1011B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2412B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4811B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2837B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2146           3398-4854      3 條（2–6 內）  
s3                  8000        1163           4786-6837      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3506          8046-11494      5 條（2–6 內）  
s6                 11000         593          7285-10407      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1011           1742-2489      5 條（2–6 內）  
s10                 5000        2412           1812-2588      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2837           2000-2163      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5523B；至少需散文≈39.48KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−57%
−55
−55%
−54%
−41.9%
−40
−40%
−20.51
−18.1%
−13.0%
−6.2%
−4.8%
−3.0%
0
0.19
0.20
0.2%
0.22
0.25%
0.4%
0.5%
0.56
0.6
0.6%
0.68
0.69
0.75
0.81
0.86
0.87
0.95
0.96
0.97
0.99
1
1.00
01
1.07
1.37
1.38
1.4%
1.4
1.667
1.7%
1.8
1.83%
2
02
2.27
3
3.01
3.14
3.21
3.29
3.4%
3.47
04
4%
4
4.5%
5%
5
5.1
5.4%
6%
6
06
6.1%
6.25
6.4%
6.76
6.9
07
7%
7
8
8%
8.06
8.1%
8.43
8.5
8.57
9%
9
9.44
9.5
10%
10
10.3%
10.72
10.8
10.9
11%
11
11.22
11.4
11.6
11.9
12%
12
12.5
12.6
13
13.06
13.29
13.5
13.6%
14
14%
14.5
15
15%
15.92
16%
16
16.8
17
17.2
17.6%
18
18.1%
18.3
19%
19
19.5%
19.5
20
20%
20.3%
20.5%
21.6%
22%
22
22.5
23
23.06
23.1
24
24.6%
25%
25
26
26%
26.6%
26.9%
27
27%
28%
28
28.85
29%
29
29.06
29.9%
30
30%
30.8%
31
31%
31.2%
31.54
31.6%
32%
33.05
33.2%
35%
38%
40%
40.8%
41.9%
42
42%
44%
44
45
45.9%
49
50%
52
53.8
56%
57%
57.5%
58.5%
58.9
59.1%
59.4%
60
60%
64.7%
65.2
65.7%
66%
67%
67.3%
70
75
77%
82%
85%
86
90
99.1
100%
100
104
117
119
120
126
130
140
150%
150
153
160
169.91
170
189
190
200
208
212
215
230
232
235%
240
250%
250
274.37
300
302
313
316
330
348
465
471.96
665.46
676
2023
2025
2026
2027
2028
2029
2030
2031
6857
20261102
1,659
2,295
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
{"meta":{"ticker":"TER","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Teradyne, Inc."},"oneliner":"AI 測試需求把季營收推上 13 億美元平台，股價較 6 月底跌約四成，只剩 FY2027 共識 EPS 的 23 倍；運算放量延到 2027 下半年，2028 年後有產能消化風險，等 1 月展望或 230 美元以下再動。","thesis":{"H":[{"id":"H1","text":"AI 帶動的測試需求讓 2027 年營收繼續成長，季營收脫離 13 億美元平台","2y":"FY2027 營收 60 億美元以上（較 2026 年約 52 億成長至少 15%），且 2027 每季營收不低於前一季（CFO 第三季法說的說法）","5y":"2030 年前 ATE 市場達 200 億美元以上（管理層說法），TER 營收 75 億美元以上","10y":null,"threshold":"FY2027 營收年增至少 15%，第一季營收高於第四季","source":"公司季報新聞稿、Q4 2026 法說的 2027 展望與新版目標模型、SEMI 設備預測","drift_rule":"以 TTM 營收對照 2 年路徑：連 2 季落後 5% 以上視為削弱，連 3 季落後 10% 以上視為反轉"},{"id":"H2","text":"運算 SoC 份額靠客戶的雙供應商策略往上走：merchant GPU 與第二家超大型雲端客戶在 2027 下半年轉成產能採購","2y":"2027 年內第二家超大型雲端客戶下產能單，merchant GPU 營收高於 2026，第三家完成認證；SoC 運算營收 2027 年增至少 30%","5y":"在運算 fast follower 客戶拿到約 30% 份額（Q2 法說管理層描述的上限）","10y":null,"threshold":"2027 第三季財報前出現第二家超大型雲端客戶的產能採購","source":"季度法說的客戶階段說明、SoC 運算營收增幅揭露","drift_rule":"2 年期：客戶時程連 2 季延後視為削弱；連 3 季延後，或客戶退回認證階段，視為反轉"},{"id":"H3","text":"產品組合夠廣，撐得住獲利率，運算訂單時點的波動不至於壓垮獲利","2y":"2027 年每季非 GAAP 毛利率 57% 以上，非 GAAP 營業利益率 28% 以上","5y":"跨週期（含一個下行年）GAAP 營業利益率平均 22% 以上（FY2022–2025 介於 19.5%～26.9%）","10y":null,"threshold":"非 GAAP 營業利益率連 2 季低於 26%，即視為論點受損","source":"季報新聞稿的非 GAAP 對帳表","drift_rule":"2 年期：連 2 季低於門檻 5% 以上視為削弱，連 3 季低於 10% 以上視為反轉；5 年期看 TTM 連 4 季偏離"}],"R":[{"id":"R1","text":"Advantest 守住運算主場，TER 的雙供應商進度卡在認證或小量出貨","h_ref":"H2","clock":"🔥","threshold":"第二家超大型雲端客戶的產能採購延到 2028，或 SoC 運算營收 2027 年增低於 15%","evidence_refs":["competitive_share_entrants#4"]},{"id":"R2","text":"2027–2029 新增產能集中後，AI 資本支出進入消化，測試占半導體資本支出由 8.1% 回落","h_ref":"H1","clock":"⚡","threshold":"半導體測試營收連 2 季季減（第三季已季減 4.5%），且下一季指引中值再低","evidence_refs":["supply_demand_durability#6"]},{"id":"R3","text":"客戶集中：前五大占 44%（2023 年 32%），單一客戶占 19%，兩家客戶分占應收 22% 與 20%，幾乎沒有合約保障","h_ref":"H1","clock":"🔥","threshold":"前五大占比超過 50%，或最大客戶下修、延後訂單","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R4","text":"出口管制、232 關稅與供應鏈（馬來西亞代工、單一來源零件、FPGA 交期拉到 52 週）推高成本或卡住出貨","h_ref":"H3","clock":"🔥","threshold":"非 GAAP 毛利率跌破 57% 且公司歸因零件或關稅，或新出口禁令涵蓋測試機","evidence_refs":["competitive_share_entrants#2","regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3","geo_supply_chain#5","supply_demand_durability#3"]},{"id":"R5","text":"替代技術與新進者：系統級測試等相鄰測試層、新興亞洲廠、客戶自製","h_ref":"H2","clock":"🐢","threshold":"大客戶公開導入自製測試，或亞洲廠拿到高階 SoC 量產機台訂單","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]}],"single_thing":{"description":"2027 年 1 月底的 Q4 法說，2027 年展望給出營收年增低於 10%，或第一季營收指引中值低於 2026 年第四季實際","why_fatal":"2027 年成長是 EPS 路徑上最大的單一敏感項。FY2027 EPS 若由 11.6 降到約 9.5（持平），倍數會同步從 23 倍壓到 18～20 倍，股價落在 170～190 美元，比現價低三成以上，也代表 2026 年就是週期高點","if_happens":"放棄建倉；已持有則清倉，改列循環交易觀察，等半導體測試營收連 2 季季增再重評","how_monitor":"Q4 法說的營收展望、第一季指引與新版目標模型；事前看 UBS 會議與 SEMI 年底預測的口徑","probability":"25%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.06,"peg_fy2":0.68,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":3.47,"FY2026E":9.44,"FY2027E":11.9,"FY2028E":15.92},"fy_end_month":12,"eps_basis":"共識為非 GAAP 稀釋 EPS（Koyfin 快照 2026-10-31）。基期 FY2025A 的 3.47 是 GAAP 稀釋 EPS，因為事實表沒有 FY2025 全年非 GAAP 值；用這個基期算三年 CAGR 會高估，判斷改用 FY2026E→FY2028E 的兩年 CAGR，約 29.9%"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"AI 測試需求驅動的雙寡占測試設備商。營收隨半導體資本支出擺動（FY2023 年減 15%），毛利高、營運槓桿大"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性，2028 年後可能反轉。Wolfe 稱 2028 年前難以供過於求，ASML 稱 2027–28 設備供給不足；但二手評論指出新增產能集中在 2027–2029，CEO 在 Q2 法說也說測試占資本支出的比重 2027 年可能回到 7%","bargaining":{"up":"上游議價力上升。FPGA、CPU、GPU 等零件短缺，測試設備用 FPGA 交期最長拉到 52 週；部分零件單一來源，組裝依賴馬來西亞代工","down":"下游議價力強。前五大客戶占 44%，單一客戶占 19%；客戶刻意採雙供應商，一方面確保產能，一方面保有議價空間","geo":"出口管制與實體清單限制中國業務，232 條款對半導體設備課 25% 關稅，而部分外國對手不受同樣限制"},"profit_pool_dir":"利潤池往 AI 運算、HBM 與資料中心互連測試移動。TER 在 HBM 效能測試份額較高，在運算份額低但正在上升；手機段萎縮","tam_table":[{"item":"測試設備市場（SEMI）","value":"2025 年約 117 億美元（由 2026 年 153 億、年增 31% 回推）→ 2026 年 153 億 → 2028 年 208 億美元"},{"item":"管理層 ATE 市場路徑","value":"舊模型以 120～140 億美元編製，現稱可達或超過 200 億美元，1 月更新"},{"item":"測試占半導體資本支出","value":"2023 年約 4% → 2025 年 6.4% → 2026 前 8 月 8.1%；管理層預期長期落在 7%～9%"},{"item":"TER 半導體測試份額（粗估）","value":"2026 前三季 33.05 億美元，年化約 44 億，對 SEMI 的 153 億約 29%。SEMI 口徑含其他測試設備，只能看方向"},{"item":"運算 SoC 份額","value":"第三方稱 Advantest 的 SoC 份額 CY25 由 56% 升到 66%（未核實）；TER 在 fast follower 客戶的份額預期由 0 增到約 30%"},{"item":"CPO 測試設備","value":"2026 年約 1 億美元 → 2028 年 3～7 億美元（管理層），長期可達 10 億美元以上"},{"item":"營業利益池 5 年變化","value":"事實表未涵蓋產業營業利益池占比"}]},"moat":{"mechanism":"裝機量加測試程式轉換成本（認證 9～12 個月），在運算靠客戶的雙供應商策略切入","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：第二家超大型雲端客戶通過認證、進入 fast follower；merchant GPU 多顆晶片開發中；第三家在認證；HBM 疊層降低，增加 TER 份額較高的效能測試需求。定價面縮減：第四季毛利率指引 57.5%～58.5%，低於第三季 59.1%；零件成本上升，客戶以雙供應商壓價。CEO 也承認運算市場擴大稀釋了整體份額。兩邊相抵，判持平","threats":[{"level":"🟡","text":"Advantest 在運算 SoC 測試的強勢份額與擴產。第三方稱它的 SoC 份額 CY25 由 56% 升到 66%（未核實），TER 只能逐個 socket 搶","p":"40%","evidence_refs":["competitive_share_entrants#4"]},{"level":"🟡","text":"新興亞洲對手與客戶自製測試，且部分對手不受美國出口管制約束","p":"20%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","reg_tariff_export#0"]},{"level":"🟡","text":"韓國記憶體測試廠吃下晶圓測試段的擴產需求（Q3 法說 CEO），TER 在晶圓測試的份額較低","p":"30%","evidence_refs":[]},{"level":"🟡","text":"替代技術：系統級測試等相鄰測試層興起，舊世代機台售價下滑。TER 有 Titan 系統級測試與燒機產品，屬點對點競爭","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推定，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（晶片廠與封測廠）、決策者（晶片設計與測試工程）、付款者（晶片廠資本支出）三方都成立。測試是出貨前必經步驟，屬於「需要」；但購買時點跟著產能擴充走，可以延後。測試占資本支出 8.1%，已在管理層 7%～9% 區間的上半部，CEO 說 2027 年可能回到 7%，當前需求水位偏高"},{"item":"決策層級","level":"🟡","text":"替代性要在單一晶片 socket 層看。已導入的 socket 換供應商要 9～12 個月認證，轉換成本高；但新 socket 由客戶逐階段比較（CEO：每一個都要競爭）。雙供應商策略讓客戶刻意保留替代選項，轉換成本只保護既有裝機，保護不了新訂單的價格"},{"item":"價值鏈分配","level":"🟡","text":"測試只占半導體資本支出 6%～8%，金額小但攸關良率，給 TER 一定的定價空間。可是下游前五大占 44% 且逐年集中，上游 FPGA 等零件短缺把成本往 TER 推，兩頭擠壓。價值鏈的總利益在晶圓廠與 AI 晶片設計者手上，測試環節分多少由客戶決定"},{"item":"社會容忍度","level":"🟡","text":"企業對企業設備，沒有消費者漲價的社會壓力。天花板來自政策：出口管制與實體清單已限制中國銷售，232 條款課 25% 關稅，部分外國對手不受同樣限制。不靠監管授權，但地緣政策會壓縮可服務市場"}],"roiic":"35%（粗估，區間 30%～40%）","reinvest_rate":"35%（粗估，區間 30%～50%）","endo_ceiling":12,"formula_note":"單位為 %。內生成長上界＝增量報酬 35% × 再投資率 35% ≈ 12%。高點對高點：FY2022 營業利益約 8.5 億美元，2026 第三季年化約 16 億，增量為正且高；但 FY2022→FY2025 增量為負，所以取正常化值。再投資包含資本支出（第三季 0.86 億）、收購 1.667 億、存貨半年增約 2 億（一半是備料）；折舊與 NOPAT 事實表未涵蓋，兩項都是粗估，不承重"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","TER":59.41,"6857.T":65.73,"FORM":44.1,"COHU":43.95,"KEYS":64.69,"unit":"%"},{"metric":"營業利益率","TER":33.17,"6857.T":45.86,"FORM":15.95,"COHU":-6.19,"KEYS":20.25,"unit":"%"},{"metric":"FCF 利潤率","TER":21.59,"6857.T":31.21,"FORM":16.67,"COHU":6.68,"KEYS":22.32,"unit":"%"},{"metric":"研發密度","TER":11.78,"6857.T":null,"FORM":13.19,"COHU":18.6,"KEYS":18.13,"unit":"%"}],"competitors":[{"name":"6857.T","gm":65.73,"om":45.86,"fcf_margin":31.21,"rd_intensity":null,"strategy_note":"運算 SoC 測試的領先者，利潤率全面高於 TER（營業利益率 45.9% 對 33.2%），並靠代工夥伴擴產守份額；TER 的份額成長要從它手上拿","period":"TTM ending 2026-06-30（4季加總）"},{"name":"FORM","gm":44.1,"om":15.95,"fcf_margin":16.67,"rd_intensity":13.19,"strategy_note":"探針卡廠，剛與 TER 宣布光學測試合作，TER 第四季完成對它的投資；兩家偏互補，不是直接競爭","period":"TTM ending 2026-09-30（4季加總）"},{"name":"COHU","gm":43.95,"om":-6.19,"fcf_margin":6.68,"rd_intensity":18.6,"strategy_note":"年報點名的半導體測試對手，營業利益率 −6.2%，規模與獲利都威脅不到高階市場","period":"TTM ending 2026-06-30（4季加總）"},{"name":"KEYS","gm":64.69,"om":20.25,"fcf_margin":22.32,"rd_intensity":18.13,"strategy_note":"量測儀器廠，毛利率 64.7%、營業利益率 20.3%，與 TER 產品測試的互連與高速測試部分重疊","period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"量為主（AI 資本支出帶動測試台數），價為輔（新世代儀器），併購與回購貢獻小","runway_years":"5～9","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段的數字：增量報酬 35% × 再投資率 35% ≈ 12%（皆粗估，投入資本與折舊事實表未涵蓋）","segments":[{"item":"半導體測試","value":"第三季 10.72 億美元（82%），年增 77%。SoC 6.76 億（季減約 20%），記憶體 3.01 億（創新高），硬碟測試 0.95 億（創新高）"},{"item":"產品測試","value":"第三季 1.38 億美元（11%），年增 56%，訂單出貨比 1.4，拉高整體毛利率"},{"item":"機器人","value":"第三季 0.96 億美元（7%），年增 28%，首度單季獲利。最大客戶營收 2026 年是 2025 年的三倍；實體 AI 要到約 2028 年才會放量"}],"decay_signals":[{"item":"毛利率連2季年減","lit":false,"text":"第三季年增 60bp，第二季年增 250bp"},{"item":"核心市占近12個月縮減","lit":true,"text":"CEO 說運算市場擴大稀釋了整體份額；第三方稱 Advantest 的 SoC 份額上升（未核實）"},{"item":"主力產品提價後銷量下滑","lit":false,"text":"事實表沒有提價與銷量資料"},{"item":"EPS成長顯著高於營收成長","lit":true,"text":"前 9 月非 GAAP EPS 年增 235%，營收年增 85%，屬週期性營運槓桿"},{"item":"FCF對淨利低於0.75連2年","lit":false,"text":"FY2023–2025 為 0.95、0.87、0.81，逐年下滑但還沒破線"},{"item":"SBC占營收超過5%且逐年上升","lit":false,"text":"約 1.7%"},{"item":"TAM萎縮或被替代","lit":false,"text":"SEMI 上修測試設備市場"},{"item":"產業估值倍數近3年系統性下移","lit":false,"text":"事實表未涵蓋產業倍數序列"},{"item":"維護性資本支出占FCF超過60%","lit":false,"text":"第三季資本支出 0.86 億對 FCF 2.27 億，總資本支出約占 38%"},{"item":"停止投資新產能且收入下滑","lit":false,"text":"正在擴產"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自本業 AI 測試需求，不是併購；2026 年收購合計 1.667 億美元，約市值 0.4%，不承重"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2026 年 4 月 MLTP 合資與 TestInsight 合計 1.667 億美元。產品測試第三季年增 56%、訂單出貨比 1.4，但收購未滿一年，已實現增量報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"第二季回購 0.69 億、第三季 0.99 億美元，回購均價事實表未涵蓋。以現價 forward 本益比 29.06 倍換算，盈餘殖利率約 3.4%；10 年期殖利率只要高於 1.4% 就不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 約為 GAAP 營業利益的 5.4%（第三季約 0.22 億美元，年化約市值 0.2%）。單季回購 0.99 億大於 SBC，淨稀釋為負","grade":"過"}]},"valuation":{"basis":"Forward P/E（FY2026E 非 GAAP 共識）","tier":"雙寡占測試設備","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比，改以自身 forward 本益比、年度端點分位與 PEG 定錨"},"fwd_pe":29.06,"peg":0.97,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"forward 本益比 29.06 倍，FY2027 為 23.1 倍。兩年共識 EPS 年化約 29.9%（基期只有 GAAP 數字，所以不用三年），PEG 約 0.97。trailing 本益比在 4 個年度端點的 26.6% 分位，P/S 在 67.3% 分位，兩者都不是五年分位。從成長看不貴，從週期高檔的獲利看不便宜，結論是合理、偏中性","upside_short_pct":10,"upside_mid_pct":27},"trap_analysis":{"verdict":"🟡","label":"週期高檔獲利與運算份額稀釋"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"二手評論指出新增產能集中在 2027–2029；CEO 在 Q2 法說說測試占資本支出 2027 年可能回到 7%；第三季 SoC 季減約 20%，運算是年內最低；CEO 在 Q3 法說承認對手在運算已建立很強的份額","assumption":"基本情境假設 2029 年只回落約 7%，2030 年就恢復成長","consequence":"若下行與份額停滯同時發生，2029 年 EPS 跌到 7 美元，給 17 倍約 120 美元，5 年後虧損約一半","ruling":"採納，放進熊市情境（機率 30%）。這條與 Single Thing 部分重疊：1 月展望若成長不到 10%，等於提前驗證這條路徑","watch":"半導體測試營收季增減、SEMI 測試設備年增率、第二家超大型雲端客戶的採購時點","evidence_refs":["supply_demand_durability#6","competitive_share_entrants#4"],"fact_refs":["f_kpi0_gaap","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"第四季毛利率指引 57.5%～58.5%，低於第三季 59.1%；CFO 提到成本與通膨壓力，以及 2027 下半年的產能擴充費用；記憶體拉低毛利（Q2 法說 CFO）；2026 年研發加資本支出近 10 億美元，存貨半年增約 2 億美元；FPGA 等零件交期拉長","assumption":"份額提升與營收成長會等比例落到每股盈餘","consequence":"營收照劇本成長，但客戶用雙供應商壓價、零件成本上升、產能與存貨占用資金，營業利益率回到 25% 以下，FCF 轉換率下滑，每股價值的成長落後營收","ruling":"部分採納。第三季營業利益率 31.6%、前 9 月 FCF 8.06 億美元仍強，這條還沒發生；以非 GAAP 營業利益率連 2 季低於 26% 作為減碼門檻","watch":"非 GAAP 毛利率與營業利益率、存貨天數（目前 189 天，CFO 說正常約 200 天）、季度 FCF","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_kpi2_non_gaap","f_kpi5_313_6_86_3_agent"]},{"view":"價格已反映太多","evidence":"forward 本益比 29.06 倍，P/S 8.57 倍位於年度端點 67% 分位；SIG 分析師在 Q3 法說指出共識已高於公司自己的目標模型；週期股在獲利高檔給近 30 倍並不便宜","assumption":"市場會維持 FY2027 23 倍以上的倍數，並相信 FY2028 共識 15.92","consequence":"若市場改用跨週期 EPS 定價，倍數壓到 18～20 倍，即使 FY2027 達標，股價也只在 215～240 美元","ruling":"部分反駁。舊目標模型以 130 億美元的 ATE 市場編製，已經過時（CEO 說明），而且股價已較 6 月底跌 42%，FY2027 只剩 23 倍。但基本情境 5 年年化約 7%，價格不算便宜，所以選擇等價格或等證據","watch":"1 月新版目標模型、FY2027 共識是否下修","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_consensus_eps_fy3"]}],"max_dd":{"lo":-55,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 471.96 → 本次 274.37（-41.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=471.96","side_b":"本次 price_at_dd=274.37","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式衛星持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 471.96 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 471.96 美元：Bull 價 665.46、Bear 價 169.91，五年期望值 −13.0%，基準年化 −3.0%，前份未列不對稱比","side_b":"本次情境、股價仍用 471.96 美元：Bull 價 676、Bear 價 170，五年期望值 −18.1%，基準年化 −4.8%，不對稱比 0.56","ruling":"先換情境、股價不動：五年期望值少 5.1 個百分點，基準年化少 1.8 個百分點。前份未列不對稱比，本次為 0.56。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 471.96 美元：五年期望值 −18.1%，基準年化 −4.8%，不對稱比 0.56","side_b":"本次情境、股價 274.37 美元：五年期望值 +40.8%，基準年化 6.1%，不對稱比 3.21","ruling":"再換股價、情境不動：起點價下跌 41.9%，五年期望值多 58.9 個百分點，基準年化多 10.9 個百分點，不對稱比由 0.56 升到 3.21。合計五年期望值比前份多 53.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"運算份額：TER 說在拿份額，對手說沒有掉","cause":null,"prior_field":null,"side_a":"TER（Q3 法說 CEO）：merchant GPU 進入 fast follower，第二家超大型雲端客戶通過認證，第三家認證中，2026 年在運算份額有顯著進展","side_b":"對手在財報中持續否認掉份額，並增加代工產能；第三方稱 Advantest 的 SoC 份額 CY25 由 56% 升到 66%（未核實）；CEO 也承認運算市場成長稀釋了 TER 的整體份額","ruling":"可調和，屬程度差異。TER 在運算的 socket 數從低基期往上，但運算市場擴大得更快，整體份額可能持平或下滑，2026 年兩邊說法可以同時成立。決勝點在 2027 年 SoC 運算營收增速是否高於市場","evidence_level":"管理層說法加未核實的第三方資料","settle_metric":"2027 年 SoC 運算營收年增率對照 SEMI 測試設備年增率","if_then":["若 2027 年 SoC 運算營收年增比測試設備市場高 10 個百分點以上 → 份額論點成立，牛市機率回到 30%","若低於市場增速 → 份額論點受損，牛市機率降到 20%，停止加碼"],"evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#3","end_markets#3"]},{"axis":"運算放量時點：Q2 說上半年，Q3 改說年中到下半年","cause":null,"prior_field":null,"side_a":"2026-07-29 Q2 法說（Gregory Smith）：運算客戶的下一波高峰預期在 2027 上半年","side_b":"2026-10-28 Q3 法說（Gregory Smith）：第一家超大型雲端客戶下一次大量產在 2027 年中，第二家的產能採購在下半年，ASIC 專案偏下半年；CFO 同時說 2027 每季都會成長，第一季高於第四季","ruling":"可調和。放量往後移一到兩季，但記憶體、汽車工業與產品測試撐住上半年，屬時點風險，論點沒有破。管理層已經延過一次，再延一次就算論點漂移","evidence_level":"兩季法說逐字稿","settle_metric":"2027 第一季營收指引與 SoC 運算季增","if_then":["若 Q4 法說的第一季指引高於第四季實際 → 接受新時程","若第一季指引低於第四季，或第一家量產再延到下半年 → 視同 Single Thing 發生，放棄建倉"],"evidence_refs":[]},{"axis":"測試占半導體資本支出：會回落還是會續擴","cause":null,"prior_field":null,"side_a":"2026-07-29 Q2 法說（Gregory Smith）：比重會落在 7%～9%，2027 年可能回到 7%","side_b":"2026-10-28 Q3 法說（Gregory Smith）：比重由 2025 年 6.4% 升到 2026 前 8 月的 8.1%，條件成熟，ATE 市場會長期擴張","ruling":"可調和。比重由 8.1% 回到 7%，等於少 13.6%，只要半導體資本支出年增約 16% 以上，測試支出就不會縮。SEMI 預測設備銷售 2026→2028 由 1,659 億到 2,295 億美元，年化約 17.6%，剛好在打平線附近。SEMI 的 2027 測試年增 18.1% 數字來源有疑義，不採用。結論是 2027 年測試市場大致持平到小增，不是管理層口中的強勁擴張","evidence_level":"SEMI 預測加兩季法說","settle_metric":"SEMI 年底預測的 2027 測試設備年增率、1 月管理層更新的測試占比","if_then":["若 SEMI 年底預測 2027 測試設備年增 10% 以上 → 維持基本情境","若轉為負成長 → 熊市機率升到 35%，持股減碼一半"],"evidence_refs":["supply_demand_durability#0","end_markets#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價較 6 月底跌 42%，RSI 28.85，26 週落後 20.5%；同期 FY2026 共識 EPS 上修 10.3%，且連續多季優於共識。FY2027 只有 23 倍，FY2028 共識只有 17 倍。能見度由 13 週拉長到兩季，管理層說積壓訂單走強、2027 每季成長。賣方目標價多在 348～465 美元","side_b":"基本情境（2029 年有一次消化）5 年年化只有約 7%；運算放量已延後一次；第四季毛利率指引下滑；共識已高於公司的舊模型","ruling":"選擇觀望、等條件。證據顯示 2027 上半年大概率不差，但便宜的論證建立在 FY2028 共識 15.92 上，這個數字還沒有公司模型背書。1 月 Q4 法說就是決勝點，等兩個月的代價小於追錯週期的代價","evidence_level":"共識快照加法說","settle_metric":"1 月 Q4 法說的 2027 展望與新版目標模型","if_then":["若 1 月展望年增 15% 以上且第一季指引高於第四季 → 建 1/3 首倉，第二季確認後補到 2/3","若 1 月前股價跌到 230 美元以下而共識沒有下修 → 先建 1/3","反向條件：若展望年增低於 10% → 放棄建倉，一季內不再評估"],"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#1"]},{"axis":"估值、熊市機率、最大回撤與裁決隨價格重算","cause":"價格變動","prior_field":["val","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-06-26，股價 471.96 美元，forward 本益比約 49 倍）：估值偏貴，熊市機率 30%，最大回撤 −60%，觀望","side_b":"本次（股價 274.37 美元，forward 本益比 29.06 倍，FY2027 共識 23 倍）：估值回到合理區，熊市機率維持 30%，最大回撤 −40%～−55%","ruling":"股價跌約 42%，同期 FY2026 共識 EPS 上修 10.3%，估值改善全部來自價格。熊市機率不動，因為週期風險沒有變小；最大回撤區間收窄，是因為有一段已經跌完；裁決與角色由新輸入重算","evidence_level":"公司財報與共識快照","settle_metric":"forward 本益比與 FY2027 共識 EPS","if_then":["若股價回到 230 美元以下且 FY2027 共識沒有下修 → 建 1/3 首倉","若 1 月展望公布前股價反彈到 330 美元以上 → 不追"],"evidence_refs":[]},{"axis":"陷阱風險與牛市機率","cause":"新證據","prior_field":["trap","p_bull_pct"],"side_a":"前份：價值陷阱風險低，牛市機率 30%","side_b":"本次：陷阱風險中等，牛市機率 25%","ruling":"陷阱風險上調有兩個新證據：一是前 9 月非 GAAP EPS 年增 235%、營收年增 85%，EPS 成長遠快於營收，屬營運槓桿的週期性放大；二是 CEO 在 Q3 法說說運算市場長太快，稀釋了 TER 的整體份額。牛市機率下調，是因為運算客戶放量時點後移：Q2 法說說下一波在 2027 上半年，Q3 法說改說第一家年中、第二家下半年，ASIC 專案偏下半年","evidence_level":"法說逐字稿與季報","settle_metric":"2027 上半年 SoC 運算營收季增","if_then":["若 2027 第一季 SoC 運算營收季增 20% 以上 → 牛市機率回到 30%","若第二家超大型雲端客戶的採購延到 2028 → 牛市機率降到 20%，熊市升到 35%"],"evidence_refs":["competitive_share_entrants#4"]},{"axis":"品質、護城河方向與長期跑道（結論不變）","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5"],"side_a":"前份：品質中上，護城河持平，5 年後跑道中等","side_b":"本次：三項結論與前份相同","ruling":"正反兩面的新證據相抵。正面：merchant GPU 進入 fast follower，第二家超大型雲端客戶通過認證，第三家認證中，HBM 疊層變低對 TER 有利。負面：對手在運算的強勢份額，第四季毛利率指引下滑，整體份額被稀釋。第二曲線（CPO、實體 AI 機器人）有管理層說法，但規模小、時程在 2028 年後，跑道不升級","evidence_level":"法說逐字稿與同業利潤率","settle_metric":"2027 年 SoC 運算營收增幅對照 Advantest；CPO 測試市場 2028 年是否落在 3～7 億美元","if_then":["若 2027 年 SoC 運算營收年增 30% 以上且毛利率守住 57% → 護城河方向改為擴大","若最大客戶公開導入第三方替代方案 → 護城河方向改為縮減，停止建倉"],"evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#4"]},{"axis":"公司類型與循環位置","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份：未分類（null）","side_b":"本次：循環型設備股，循環位置在中段","ruling":"前份的框架沒有要求分類。本次歸為循環型，因為 FY2023 營收年減 15%，EPS 隨週期大幅擺動；AI 改變的是週期的振幅與時點，沒有消除週期。循環位置判在中段：營收連三季站在 13 億美元平台，管理層預期 2027 每季成長；但測試占資本支出 8.1%，已在管理層 7%～9% 區間的上半部","evidence_level":"年度財報與法說","settle_metric":"2027 上半年營收逐季變化、測試占資本支出比重","if_then":["若 2027 上半年營收逐季成長，且 SEMI 年底預測維持 2027 測試設備兩位數成長 → 維持中段","若測試占比跌回 7% 且半導體測試連 2 季季減 → 改判晚段，熊市機率調到 35%"],"evidence_refs":[]},{"axis":"重啟建倉條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份：未設重啟條件（null）","side_b":"本次：股價 230 美元以下且 FY2027 共識下修不超過 5%，或 1 月 Q4 法說確認 2027 營收年增 15% 以上且第一季指引高於第四季實際 → 首倉建倉 1/3","ruling":"前份判觀望，但沒寫出卡住的條件。本次觀望的約束是價格相對週期風險不夠便宜（基本情境 5 年年化約 7%），重啟條件就是推翻這個約束：要嘛價格便宜到基本情境年化約 10%，要嘛用證據把熊市機率壓下去","evidence_level":"情境樹與法說","settle_metric":"股價與 1 月 Q4 法說展望","if_then":["若兩個條件之一成立 → 首倉建倉 1/3","若股價先到 230 美元，但 1 月展望年增低於 10% → 不建倉，已持有則清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份：未設減碼與清倉門檻（null）","side_b":"本次：半導體測試營收連 2 季季減且下一季指引中值再低 → 減碼一半；2027 營收指引年增低於 10% 或第一季指引低於第四季 → 清倉；非 GAAP 營業利益率連 2 季低於 26% → 減碼一半","ruling":"前份只有監測指標，沒有動作。本次把週期與份額兩條主風險綁到具體動作，門檻取第三季實際值的合理偏離幅度","evidence_level":"季報與法說","settle_metric":"各季財報","if_then":["若任一減碼門檻觸發 → 減碼一半","若清倉門檻觸發 → 清倉，並移出觀察名單一季"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）","side_b":"本次 Single Thing：2027 年 1 月底 Q4 法說給出 2027 營收年增低於 10%，或第一季營收指引中值低於 2026 年第四季實際","ruling":"選 2027 年成長展望，不選單一客戶或出口管制，因為它是 EPS 路徑上數學敏感度最大的一項。發生就清倉，或放棄建倉","evidence_level":"情境樹敏感度","settle_metric":"1 月 Q4 法說","if_then":["若發生 → 清倉，或放棄建倉","若展望年增 15% 以上 → 這個風險解除，改看第二家超大型雲端客戶的時程"],"evidence_refs":[]},{"axis":"營收季減門檻改寫","cause":"新證據","prior_field":["thesis.R"],"side_a":"前份：連 2 季營收環比下滑即警戒；Rubin 認證 TER 出局，或連 2 季 custom-ASIC 份額流失 5pp","side_b":"本次：半導體測試營收連 2 季季減且下一季指引中值再低 → 減碼；第二家超大型雲端客戶的採購延到 2028，或 SoC 運算 2027 年增低於 15% → 份額論點受損","ruling":"第三季總營收 13.06 億美元，較第二季約 13.29 億美元（半導體測試 11.22 億、產品測試 1.07 億、機器人 1.00 億）季減 1.7%；第四季指引中值 13 億美元，再低 0.5%。營收停在高原時，舊門檻會被這種小幅波動觸發，失去區分力，因此改用半導體測試（第三季季減 4.5%）加下一季指引的雙條件。舊門檻提到的具體產品名，在本包證據中無法驗證，改用法說可以追蹤的客戶階段","evidence_level":"季報與法說","settle_metric":"半導體測試季營收與下一季指引","if_then":["若新門檻觸發 → 減碼一半","若第四季實際營收高於 13.06 億美元 → 舊門檻的疑慮解除"],"evidence_refs":["supply_demand_durability#6"]}],"triggers":[{"n":1,"text":"Q4 法說確認 2027 年成長","type":"假設驗證","maps_to":"H1","metric":"2027 營收成長指引、第一季營收指引中值","threshold":"年增 15% 以上，且第一季高於第四季實際","action":"達標則重啟條件成立，建 1/3 首倉","source_freq":"季報（1 月底）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"第二家超大型雲端客戶下產能單","type":"假設驗證","maps_to":"H2","metric":"法說客戶階段說明、SoC 運算營收季增","threshold":"2027 第三季財報前出現產能採購","action":"出現則加碼到 2/3；延到 2028 則牛市機率降到 20%","source_freq":"季報","date":"2027-10","evidence_refs":["competitive_share_entrants#4"]},{"n":3,"text":"產品組合撐住獲利率","type":"假設驗證","maps_to":"H3","metric":"非 GAAP 毛利率、非 GAAP 營業利益率","threshold":"毛利率 57% 以上，營業利益率 28% 以上","action":"守住則維持；跌破見減碼列","source_freq":"季報","date":null,"evidence_refs":[]},{"n":4,"text":"半導體測試連續季減","type":"風險","maps_to":"R2","metric":"半導體測試季營收","threshold":"連 2 季季減，且下一季指引中值再低","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#6"]},{"n":5,"text":"客戶集中度惡化","type":"風險","maps_to":"R3","metric":"前五大客戶營收占比、單一客戶應收占比","threshold":"前五大超過 50%，或單一客戶應收超過 25%","action":"倉位上限降一級，停止加碼","source_freq":"年報","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0"]},{"n":6,"text":"出口管制與零組件成本吃掉毛利","type":"風險","maps_to":"R4","metric":"非 GAAP 毛利率與公司歸因、美國出口規則","threshold":"毛利率跌破 57% 且歸因零件或關稅，或新禁令涵蓋測試機","action":"停止加碼，重估熊市機率","source_freq":"季報與法規公告","date":null,"evidence_refs":["reg_tariff_export#1","supply_demand_durability#3","regulatory_antitrust#1"]},{"n":7,"text":"Single Thing：2027 展望不及","type":"Single Thing","maps_to":"Single Thing","metric":"2027 營收成長指引、第一季指引","threshold":"年增低於 10%，或第一季指引中值低於第四季實際","action":"已持有則清倉，未持有則放棄建倉","source_freq":"Q4 法說","date":"2027-01","evidence_refs":[]},{"n":8,"text":"價格回到重啟區","type":"估值rearm","maps_to":"H1","metric":"股價、FY2027 共識 EPS","threshold":"230 美元以下，且 FY2027 共識下修不超過 5%","action":"建 1/3 首倉","source_freq":"每日","date":null,"evidence_refs":[]},{"n":9,"text":"首倉後加碼","type":"加碼","maps_to":"H2","metric":"2027 第一季營收季增、非 GAAP 毛利率","threshold":"第一季營收季增，且毛利率 57% 以上","action":"加碼到 2/3","source_freq":"季報","date":"2027-04","evidence_refs":[]},{"n":10,"text":"獲利率失守","type":"減碼","maps_to":"H3","metric":"非 GAAP 營業利益率","threshold":"連 2 季低於 26%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":[]},{"n":11,"text":"週期反轉","type":"清倉","maps_to":"R2","metric":"半導體測試營收年增率、第二家超大型雲端客戶時程","threshold":"半導體測試連 2 季年減 20% 以上，或第二家超大型雲端客戶退回認證階段","action":"清倉","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#6"]},{"n":12,"text":"Q4 法說後全份重評","type":"複審日期","maps_to":null,"metric":"整份判斷重跑","threshold":"Q4 法說與新版目標模型公布後","action":"重跑判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"半導體測試季營收連續季減","bear_threshold":"連 2 季季減且下一季指引中值再低 → 減碼一半","window":"2027 年每季財報","source":"公司季報新聞稿 Exhibit 99.1","last_status":"warning"},{"metric":"2027 年營收成長指引與第一季指引","bear_threshold":"年增低於 10% 或第一季指引中值低於 2026 第四季實際 → 清倉或放棄建倉","window":"2027 年 1 月底 Q4 法說","source":"Q4 2026 法說與新版目標模型","last_status":"unknown"},{"metric":"非 GAAP 營業利益率","bear_threshold":"連 2 季低於 26% → 減碼一半","window":"2027 全年各季","source":"季報非 GAAP 對帳表","last_status":"ok"},{"metric":"前五大客戶營收占比、單一客戶應收占比","bear_threshold":"前五大超過 50% 或單一客戶應收超過 25% → 停止加碼","window":"FY2026 年報（2027-02）","source":"10-K Item 1A 與 7A","last_status":"warning"},{"metric":"第二家超大型雲端客戶產能採購","bear_threshold":"2027 第三季財報前仍未出現，或延到 2028 → 牛市機率降到 20%","window":"至 2027-10","source":"季度法說的客戶階段說明","last_status":"unknown"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"這條出自 FY2018 年報的舊敘述（產品與零件越來越多在中國生產），已被之後把半導體製造遷出蘇州的事實取代，現行製造以馬來西亞代工為主。它描述的是七年前的供應鏈結構，不代表目前曝險；目前的供應鏈曝險已由馬來西亞代工與單一來源零件兩條證據承接，列在第四條風險"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把第三季 SoC 季減約 20% 與第四季毛利率指引下滑當成見頂訊號，股價較 6 月底跌 42%。但同期 FY2026 共識 EPS 上修 10.3%，管理層也說積壓訂單走強、2027 每季成長、第一季高於第四季。若 2027 上半年兌現，現價只有 FY2027 EPS 的 23 倍，是過度折價；兌現之前只算部分理由"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-20.51, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027 年 1 月底 Q4 法說確認 2027 營收年增 15% 以上且第一季指引高於第四季實際；或股價回到 230 美元以下（約 FY2027 共識的 19 倍），且共識下修不超過 5%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價≤230美元且FY2027共識下修不超過5%，或1月Q4法說確認2027營收年增≥15%且第一季指引高於第四季實際","exec_line":"條件成立先建 1/3 首倉；2027 第一季營收季增且毛利率在 57% 以上，再補到 2/3；第二家超大型雲端客戶下產能單才建滿。半導體測試連 2 季季減，則停止加碼並減碼一半"},"reasoning":{"industry":"第三季營收 13.06 億美元，分三塊：半導體測試 10.72 億（82%，其中 SoC 6.76 億，記憶體 3.01 億創新高，硬碟測試 0.95 億創新高）；產品測試 1.38 億（11%，訂單出貨比 1.4）；機器人 0.96 億（7%，首度單季獲利）。GAAP 營業利益率 30.8%，非 GAAP 31.6%。第四季營收指引 12.5～13.5 億美元，中值與第三季持平。SoC 由第二季 8.43 億降到 6.76 億，季減約 20%，被記憶體與硬碟測試各約 42% 的季增抵銷；管理層說運算在第三季是年內低點。收錢方式是設備一次性銷售，能見度由過去 13 週拉長到約兩季。單點依賴：前五大直接客戶占 44%（2023 年為 32%），一家半導體測試客戶占 19%，兩家客戶分占應收 22% 與 20%。這是集中度風險，不是護城河證據。產業位置在擴張期，依據有三：SEMI 年中把 2026 測試設備上修到 153 億美元（年增 31%）；測試占半導體資本支出由 6.4% 升到 8.1%；零組件交期拉長。供需持久性屬週期性，2028 年後可能反轉：Wolfe 與 ASML 的持久證據只蓋到 2028，新增產能卻集中在 2027–2029。產業態勢是雙向拉鋸。競爭面，對手在運算強勢且在擴產；結構面，AI 推高測試強度；其他面，出口管制與 232 關稅持續壓縮中國業務。","moat":"機制是裝機量加測試程式的轉換成本。客戶從啟動到量產要 9～12 個月認證（Q2 法說），換供應商就得重寫測試程式、重做 correlation。執行力給 8 分：UltraFLEXplus 產能 18 個月擴 4 倍，並認證第二家代工；推出三款新儀器，補上 2027 世代 AI 晶片的測試空缺；連續多季優於共識。定價力給 6 分：TTM 毛利率 59.4% 對 Advantest 65.7%，營業利益率 33.2% 對 45.9%，FCF 利潤率 21.6% 對 31.2%，三項都落後；第四季毛利率指引下滑，客戶用雙供應商保有議價力。對最強同業的利潤率差為負，但只有單一期間，看不出在擴大還是收窄。方向判持平：執行面擴大（merchant GPU 進入 fast follower，第二家超大型雲端客戶通過認證，第三家認證中）；定價面縮減；運算市場成長太快，稀釋了整體份額（Q3 法說 CEO）。當期報酬方面，事實表沒有投入資本。外包代工、資本支出占營收低，推定為高利益率高周轉。但 FY2022→FY2025 營業利益由約 8.5 億降到 6.9 億美元，增量報酬明顯隨週期擺動。","growth":"成長以量為主：AI 資本支出帶動測試台數，記憶體連四季超過 2 億美元，硬碟測試因近線儲存需求年增約 150%。價格面靠新世代儀器，ASP 資料事實表未涵蓋。併購（2026 年 1.667 億美元）與淨回購（年化約 0.6%）的貢獻都小。共識 FY2026→FY2028 EPS 由 9.44 到 15.92，兩年年化約 29.9%；FY2027 營收共識 65.2 億美元，年增約 24.6%（17 位分析師）。內生上界約 12%（增量報酬 35% × 再投資率 35%，皆粗估），共識高出約 18 個百分點。缺口來自產業資本支出上行帶來的量與營運槓桿，屬週期性外生成長，再投資解釋不了，長期信心上限為中。跑道：管理層說 ATE 市場可達或超過 200 億美元，TER 在運算 fast follower 客戶的份額預期到約 30%，這段約 5～9 年走完，之後成長回到跟著半導體資本支出走。衰退信號亮 2 個（核心份額被稀釋、EPS 成長遠快於營收），長期成長性中等。","governance":"第三季 FCF 2.27 億美元（營業現金流 3.14 億減資本支出 0.86 億），前 9 月 8.06 億，年增近 250%。FCF 對淨利的比率 FY2023–2025 為 0.95、0.87、0.81，逐年下滑，部分是因為擴產期存貨堆高（第三季存貨季增 35%，CFO 說一半是備料、一半對應需求）。SBC 約為 GAAP 營業利益的 5.4%，約營收的 1.7%。現金去向：第一優先是本業，2026 年研發加資本支出近 10 億美元；收購 1.667 億美元（MLTP 合資與 TestInsight）；回購第二季 0.69 億、第三季 0.99 億（第一季事實表未涵蓋）；股利每季 0.20 億。資產負債方面，現金與投資 6.25 億美元，總債務 1.37 億，淨現金約 3.29 億，另有 10 億美元循環額度未動用。三項檢核：收購未滿一年，已實現報酬無法驗證。回購以現價 forward 本益比 29 倍計，盈餘殖利率約 3.4%；10 年期殖利率事實表未涵蓋，但只要高於 1.4%，門檻就會高於 3.4%，這項不過。SBC 淨稀釋為負（回購金額大於 SBC），這項過。","valuation":"現價 274.37 美元，相當於 FY2026 共識 EPS 9.44 的 29.06 倍、FY2027 共識 11.9 的 23.1 倍、FY2028 共識 15.92 的 17.2 倍。兩年共識 EPS 年化約 29.9%，PEG 約 0.97。若終端給 22 倍、要每年賺 8%，FY2031 EPS 要到約 18.3 美元（5 年年化約 14%），等於穿越一次產能消化後仍維持兩位數成長；基本情境只給 16.8，年化約 7%。短期目標：FY2027 EPS 11.6 × 26 倍，約 302 美元（+10%）。中期目標：FY2028 EPS 14.5 × 24 倍，約 348 美元（+27%）。賣方目標價在 8 月時多落在 348～465 美元，資料偏舊；方向上支持上檔，但均值高於本判斷，差別在於有沒有把 2029 年的消化放進來。trailing 本益比 31.54 倍，在 4 個年度端點中位於 26.6% 分位；P/S 8.57 倍與 EV/S 8.5 倍位於約 67% 分位。事實表沒有五年高低點，不計算五年分位；也沒有同業本益比，終端倍數只能對照自身：22 倍低於現值 29 倍，高於 FY2028 共識隱含的 17 倍。","premortem":"反證依據見反證紀錄的三條。陷阱評級中等：十項衰退信號亮 2 項（整體份額被運算成長稀釋、EPS 成長遠快於營收）。價格面：26 週落後大盤 20.5%，RSI 28.85 已超賣，股價低於 52 週均線 316 美元；但仍在 104 週均線 212 美元與 250 週均線 150 美元之上，250 週均線 13 週斜率 +1.83%，長期趨勢未破。共識面：FY2026 共識 EPS 近 3 個月上修 10.3%，但最近兩份快照之間 FY2026 持平、FY2027 只上修 0.25%，第三季優於預期並沒有再推高後面年度。資料缺口：歷史最大回撤、空方數字，以及法說上三題沒有正面回答（記憶體測試成長倍數、長期份額目標、2027 年相對 WFE 的成長），事實表都沒有落成數字。後兩題指向同一件事：管理層不願對運算份額與 2027 成長給出量化承諾。"},"plain":{"six":{"how_it_makes_money":"TER 賺的是晶片廠與 AI 晶片設計者買測試機的錢。每顆高階晶片出廠前都要測，錢卡在測試機台加測試程式這一節。第三季 82% 營收來自半導體測試，毛利率 59.1%，非 GAAP 營業利益率 31.6%。","moat":"護城河持平。測試程式的轉換成本與雙寡占地位穩固，運算份額正在拿；但定價力沒有變強，利潤率仍落後 Advantest。","growth":"5 年後跑道中等。ATE 市場有望在 2030 年前到 200 億美元以上，TER 在運算份額也有空間；但第二曲線（CPO、實體 AI 機器人）規模小、時程在 2028 年後，成長大部分仍綁在半導體資本支出週期。","capital":"資本配置中等。本業再投資優先、帳上淨現金、股權稀釋很低；但回購在高本益比區間執行，收購成效也還沒驗證。","valuation":"現價要求 2027–2028 年照共識成長、2029 年只小幅消化。我只信前半段：2027 有積壓訂單撐，2028 以後沒有。價格合理但不便宜，等 1 月展望或更低價格。","how_wrong":"最可能看錯的地方，是把 2026 年的 13 億美元高原當成新底部。運算放量已經延後一次，2027–2029 年新增產能集中；若 2027 年成長不到 10%，獲利與倍數會一起往下。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把第三季 SoC 季減約 20% 與第四季毛利率指引下滑當成見頂訊號，股價較 6 月底跌 42%。但同期 FY2026 共識 EPS 上修 10.3%，管理層也說積壓訂單走強、2027 每季成長、第一季高於第四季。若 2027 上半年兌現，現價只有 FY2027 EPS 的 23 倍，是過度折價；兌現之前只算部分理由","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 1 月底 Q4 法說確認 2027 營收年增 15% 以上且第一季指引高於第四季實際；或股價回到 230 美元以下（約 FY2027 共識的 19 倍），且共識下修不超過 5%","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":274.37,"week26_return_pct":-20.51,"consensus_rev_3m_pct":10.28,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 EPS 處於週期高檔，但不是一次性獲利。上半年有不會重複的非營運利益（Q2 法說 CFO），金額事實表未涵蓋"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報、新版目標獲利模型（以更大的 ATE 市場重編）與 2027 年展望","impact":"高","watch":"2027 營收成長指引、第一季指引是否高於第四季、新模型的營收與營業利益率目標"},{"date":"2026-12","date_precision":"month","type":"other","event":"UBS 科技投資人會議（管理層出席）","impact":"低","watch":"運算客戶時程與產能計畫的口徑有沒有改變"},{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"完成對 FormFactor 的投資（待主管機關核准）","impact":"中","watch":"投資金額，以及光學測試合作的實際產品"},{"date":"2026-12","date_precision":"month","type":"macro","event":"SEMI 年底設備預測（2027 年測試設備年增率）","impact":"中","watch":"2027 年測試設備是否維持兩位數成長"},{"date":"2027-02","date_precision":"month","type":"other","event":"FY2026 年報揭露前五大客戶占比與應收集中度","impact":"中","watch":"前五大是否超過 50%、單一客戶應收是否超過 25%"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"第二家超大型雲端客戶的產能採購；第一家年中的下一波量產","impact":"高","watch":"SoC 運算營收季增，以及管理層的客戶階段說明"}],"_projected_from":"v19"}
```
