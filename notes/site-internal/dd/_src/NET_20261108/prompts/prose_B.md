你是 stock-analyst v20 的**散文層（prose）agent**，標的 NET（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：NET　日期：2026-11-08　archetype：None　前份裁決：2026-08-07　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1559B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（538B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（997B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1491B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1236B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（370B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（624B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2214B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3798B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2211B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1559           3809-5441      5 條（2–6 內）  
s3                  8000         538           5223-7462      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3724          7893-11276      5 條（2–6 內）  
s6                 11000         370          7441-10630      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         624           2013-2876      5 條（2–6 內）  
s10                 5000        2214           1950-2786      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2211           2000-2789      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4893B；至少需散文≈40.11KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−75%
−75
−70%
−54%
−50
−50%
−18.7%
−17.1%
−16.4%
−8.7%
−8.1%
−4.7%
−3.6%
−1.8
−1
−0.29
0
0%
0.1
0.5%
0.59
0.7
0.75
1
1.04
1.1
1.2%
1.2
$1.26
1.26
1.27
1.295
1.3
$1.35
1.35
1.371
1.437
1.46
1.49
1.5
1.5%
1.55
1.57
$1.586
1.66
$1.66
$1.69
1.69
1.741
1.9%
1.9
$1.90
2
02
2.05
2.17
2.27
$2.27
2.5%
2.63
3
3%
3.035
3.28
3.29
3.4
3.4%
3.52
$3.52
3.53
3.58
3.7
3.79
4
4%
4.1
4.14
4.15
4.3
4.5
4.54
4.625
4.65
4.7
5%
05
5
$5.4
5.5
5.6%
06
6%
6
6.1
6.2
6.2%
6.52
7
07
7.6%
7.825
8%
08
8
8.52
$8.7
9
09
10
10%
11
11.4
11.9%
12%
12
12.5%
13
13.7%
14.0%
14%
14
15
15%
15.5%
15.6%
16
16.5%
17.5%
17.6%
18
18.3
18.5%
18.7%
19.0
19%
20
20%
22%
22
22.3%
23.2%
24
25
25%
26%
26
26.3%
28%
28.2%
28.77
29.6
30%
30
30.7%
32%
32.3
32.4%
33%
34%
34
34.2%
35%
35.1
37%
37.03
38.75
39%
40
42
44%
45
48
49
50
51%
52%
$53
57%
57.5%
58
60
60%
61%
62.6%
70%
70
71%
72%
72.4%
73%
73.1%
$74.7
74.7
$75
75
75%
77%
$77
78.7
80%
90
95
100
100%
104
$106
107
116%
118%
119%
120%
122%
122
124
$124.31
125
$136
140
150%
159
$187
$194
$198.95
199
199.07
200
$206
213
213.29
$250
250
$260
$264
$266
$268.75
268.75
$275
290
$305
320
$330
$330.5
330.5
$400
$496.94
509
511.2
760
2019
2021
2024
2025
2026
2027
2028
2029
2031
20261108
1,019
1,400
2,380
2,650
3,800
4,420
4,600
5,000
6,790
7,880
8,210
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
{"meta":{"ticker":"NET","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Cloudflare, Inc."},"oneliner":"Q3 營收年增 39%、非 GAAP 營益率 17.5% 創新高，生意比 8 月更好；但現價約今年指引 EPS 的 199 倍，Base 五年年化只有約 0.5%，等約 $206 再談。","thesis":{"H":[{"id":"H1","text":"代理式工作負載與開發者平台持續放大用量型收入，淨留存維持 120% 以上，營收年增不低於 30%。","2y":"FY27 營收年增 ≥30%，淨留存 ≥120%。","5y":null,"10y":null,"threshold":"FY27 營收年增 ≥30% 且淨留存 ≥120%；Q3 實績 39%、122%。","source":"每季新聞稿與財報電話會議。","drift_rule":"TTM 營收對 Base 路徑連兩季偏離 ≥5% 視為削弱，連三季偏離 ≥10% 視為反轉。"},{"id":"H2","text":"非 GAAP 營益率由 FY26 指引 15.6% 升到 FY31 約 28%，毛利率守住 70% 以上，費用率下降快過毛利率下滑。","2y":null,"5y":"FY31 非 GAAP 營益率約 28%，毛利率 ≥70%。","10y":null,"threshold":"Q4 FY26 ≥18.5%，FY27 ≥20%，毛利率 ≥70%。","source":"每季新聞稿與非 GAAP 調節表。","drift_rule":"TTM 營益率對 Base 路徑連四季偏離 ≥5% 視為削弱，連六季偏離 ≥10% 視為反轉。"},{"id":"H3","text":"Act IV 的按用量收費成為第二條成長曲線，代理要付費才能取用內容與服務，Cloudflare 收取通行費。","2y":null,"5y":null,"10y":"Act IV 成為主要營收來源之一；CEO 2026-11-05 說 10 年後可能是最大業務。","threshold":"2028 年底前揭露 Act IV 年化營收 ≥$250M，約占 Base FY28 營收 5%。","source":"財報電話會議與投資人日揭露。","drift_rule":"跨兩個年度未揭露規模或未達門檻視為削弱，跨三個年度視為反轉。"}],"R":[{"id":"R1","text":"Q3 超預期主要來自用量型收入，CFO 8 月還說這類合約讓逐季預測更難、客戶波動更大；資安急單也可能把需求提前。","h_ref":"H1","clock":"⚡","threshold":"下一季淨留存低於 120%，或營收年增低於 35%。","evidence_refs":[]},{"id":"R2","text":"記憶體、SSD、CPU 缺貨與關稅推高伺服器成本，加上 Workers 毛利較低，毛利率 Q3 再降 70 個基點，與 CFO 6 月、8 月的趨穩說法有落差。","h_ref":"H2","clock":"🔥","threshold":"非 GAAP 毛利率連兩季低於 72% 視為趨穩說法失效，連兩季低於 70% 視為論點受損。","evidence_refs":["geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R3","text":"超大雲綁約、Akamai 推論合約與 AI 新進者帶來降價與份額壓力。","h_ref":"H1","clock":"🔥","threshold":"淨留存連兩季低於 118%，或大客戶季淨增連兩季低於 200 家。","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#2"]},{"id":"R4","text":"模型廠自建託管代理執行環境，把企業代理負載從邊緣網路拉走；CEO 在 2026-06-09 投資人日沒有正面回答這條競合界線。","h_ref":"H3","clock":"🐢","threshold":"前沿模型廠公開把主要代理負載遷出 Cloudflare，且淨留存同時連兩季下滑。","evidence_refs":["substitute_technology#1","substitute_technology#2"]},{"id":"R5","text":"股權酬勞占營收 22.3%，非 GAAP 獲利高估股東實得，股數持續增加。","h_ref":"H2","clock":"🐢","threshold":"FY28 股權酬勞占營收仍高於 20%，或稀釋股數連兩年年增高於 2.5%。","evidence_refs":[]},{"id":"R6","text":"銷售長 Mark Anderson 年底退休，Christian Smith 接任；銷售生產力已連 11 季年增，交接期中斷會影響 FY27。","h_ref":"H1","clock":"⚡","threshold":"管理層不再確認銷售生產力年增，連續紀錄中斷。","evidence_refs":[]},{"id":"R7","text":"出口管制與制裁合規：BIS 關聯企業規則暫停一年到 2026-11-10，2019 年自揭的 OFAC 案仍在審查，金額未揭露。","h_ref":"H1","clock":"🐢","threshold":"BIS 規則復效後公司揭露受影響客戶營收，或 OFAC 案出現罰款或和解金額。","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3"]},{"id":"R8","text":"高成長軟體倍數整體下移，NET 現有倍數失去支撐。","h_ref":"H1","clock":"🔥","threshold":"NET／DDOG Fwd PE 比值連兩季高於 4.5x，或 DDOG Fwd PE 跌破 50x；本次資料缺口。","evidence_refs":[]}],"single_thing":{"description":"2027 年底前，營收年增連兩季跌破 30%，同時淨留存跌回 118% 以下。","why_fatal":"現價約 199 倍今年 EPS，靠的是高成長延續。FY31 營收比 Base 低 15%、終端倍數由 50 倍降到 40 倍，終值由 $275 降到約 $187，比現價低 30%，是情境裡敏感度最大的一項。","if_happens":"不追，取消進場價位並重跑判斷；若屆時已持有，減碼一半。","how_monitor":"每季新聞稿的營收年增率與電話會議的淨留存；Q4 FY26 財報約在 2027 年 2 月。","probability":"約 20%（12 至 24 個月）"}},"appendix_a":{"growth_durability":8,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":159.0,"peg_fy2":4.65,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":-0.29,"FY2026E":1.26,"FY2027E":1.69,"FY2028E":2.27},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為非 GAAP 共識（Koyfin 2026-11-07 快照，財報前數字，公司 FY26 新指引 $1.35）；FY2025A 為 GAAP 稀釋 EPS，非 GAAP 基期事實表未涵蓋，兩者不可直接比較。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NET_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"未獲利高成長","confidence":"中","fingerprint":"非 GAAP 已獲利，自由現金流自 FY23 起連續為正，GAAP 指引 Q4 轉盈。"},"industry":{"clock_phase":"II","sd_verdict_source":"產業處於擴張期，Gartner 預估基礎設施軟體支出 2024 至 2029 年年化約 12%。供需以結構性持久為主：代理流量與開發者數量推高用量；資安急單帶週期性，CEO 自己說這波衝擊約兩年（2026-11-05）。","bargaining":{"up":"伺服器零組件供應商少，記憶體、SSD、CPU 缺貨時議價力在對方。","down":"無單一客戶超過營收 10%，資金池合約讓大客戶擴張更順，議價力偏公司。","geo":"國際營收 FY25 占 51%；Q3 美國占 52%，網路涵蓋 125 國以上。"},"profit_pool_dir":"利潤池往代理式運算與整合式資安平台移動，方向有管理層說法與客戶案例支持；五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"TAM（公司口徑）","value":"2026 年約 2,380 億美元，尚未納入 Act IV（2026-06-09 CFO）"},{"item":"滲透率","value":"FY26 指引營收中點約 29.6 億美元 ÷ 2,380 億 ≈ 1.2%"},{"item":"外部對照","value":"Gartner：基礎設施軟體支出 2024 年 4,420 億美元，2029 年近 7,880 億；IDC：全球邊緣運算支出 2028 年逼近 3,800 億"},{"item":"SAM 與營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"全球網路規模、isolates 運算架構與免費層帶來的流量及威脅情報，形成互相強化的飛輪。","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行面加寬：淨留存一年升 3 個百分點，銷售生產力連 11 季年增，營收連續加速。定價面穩定：毛利率下滑主要歸因產品組合，沒有直接降價證據，也沒有提價證據。","peer_na_reason":"同業 ROIC 事實表未涵蓋，只有利潤率可比，改用留存與份額判斷方向。","threats":[{"level":"🟡","text":"超大雲與新進 AI 業者以綁約與低價爭奪儲存、運算工作負載；Q2 一筆媒體客戶案例提過整合到超大雲的壓力，Q3 案例仍多由 NET 勝出。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"Akamai 以 LLM 推論合約切入（聚合媒體報導，未經官方核實），可能帶來價格或份額壓力。","p":"25%","evidence_refs":["competitive_share_entrants#2","end_markets#2"]},{"level":"🟡","text":"模型廠託管的代理執行環境可能把企業代理負載拉離邊緣網路。目前證據只有一篇部落格解讀與 10-Q 通用風險；若前沿實驗室公開遷出，升為生態攻擊。","p":"30%","evidence_refs":["substitute_technology#1","substitute_technology#2"]}],"roic_durability":{"quadrant":"投入資本事實表未涵蓋，周轉率未知；GAAP 營益率為負，當期 ROIC 為負，非 GAAP 口徑屬低利益率。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是開發者與資安團隊，決策者是 CISO 與 CIO，付款者是企業 IT 預算，三者都成立。讀數：淨留存 122%，大客戶約 5,000 家、年增 25%；反向是 Mark Anderson 2026-06-09 說 IT 預算大致持平。"},{"item":"決策層級","level":"🟡","text":"替代性要看工作負載：代理應用總持有成本低 60% 至 70%，一般成長緩慢的應用跑在 Workers 上反而貴約 15%，舊應用也較難搬上來（2026-06-09）。漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"上游記憶體、SSD、CPU 缺貨會分走利潤，毛利率一年降 290 個基點；下游 AI 實驗室既是客戶也可能自建。Act IV 的收費位置已見首筆營收，金額未揭露。"},{"item":"社會容忍度","level":"🟡","text":"CEO 說公司在代理與內容方之間扮演仲裁者、制定規則（2026-11-05），守門人角色會引來監管注意。目前只見義大利 AGCOM 約 1,400 萬歐元罰款，未見反壟斷調查。"}],"roiic":"非 GAAP 粗估約 30%：FY26 指引營業利益 4.625 億美元對 FY25 約 3.035 億，增量稅後約 1.27 億，除以全額網路資本支出約 4.3 億；折舊未扣，GAAP 口徑無法計算。","reinvest_rate":"約 116%：全額資本支出 4.3 億美元 ÷ 非 GAAP 稅後營業利益 3.7 億；未扣折舊，屬上限。","endo_ceiling":null,"formula_note":"FY25 營益率 14.0% 來自前份摘要。兩個比率相乘只會回到今年非 GAAP 稅後營業利益成長率約 34%，沒有獨立資訊；股權酬勞占營收 22.3% 也沒有計入，所以不給內生上限數字。公司選擇不做融資擴產，資本支出壓在營收 14% 至 15%，用工程效率換成長，代價是短期毛利率下滑。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","NET":72.58,"ZS":76.8,"FSLY":62.64,"AKAM":57.45,"CRWD":75.25,"unit":"%"},{"metric":"營業利益率","NET":-8.11,"ZS":-3.61,"FSLY":-8.85,"AKAM":11.92,"CRWD":-2.21,"unit":"%"},{"metric":"FCF 利潤率","NET":12.53,"ZS":23.24,"FSLY":5.63,"AKAM":14.57,"CRWD":28.22,"unit":"%"},{"metric":"研發密度","NET":22.82,"ZS":26.95,"FSLY":23.42,"AKAM":12.83,"CRWD":28.84,"unit":"%"}],"competitors":[{"name":"ZS","gm":76.8,"om":-3.61,"fcf_margin":23.24,"rd_intensity":26.95,"strategy_note":"第一代 Zero Trust 代表，FCF 利潤率 23.2% 高於 NET；Q3 案例裡第一代廠商多次被替換，但 NET 進場較晚，CEO 也承認。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"FSLY","gm":62.64,"om":-8.85,"fcf_margin":5.63,"rd_intensity":23.42,"strategy_note":"毛利率 62.6%、FCF 利潤率 5.6%，規模與產品廣度都落後，對 NET 壓力有限。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"AKAM","gm":57.45,"om":11.92,"fcf_margin":14.57,"rd_intensity":12.83,"strategy_note":"毛利率 57.5%、GAAP 營益率 11.9%；傳聞的 Anthropic 七年 18 億美元合約未經官方核實，若屬實代表推論負載有替代選擇。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CRWD","gm":75.25,"om":-2.21,"fcf_margin":28.22,"rd_intensity":28.84,"strategy_note":"端點平台整合者，FCF 利潤率 28.2%；目前與 NET 重疊有限，風險在資安預算整合時爭平台位置。","period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"用量與新客為主，價格貢獻無直接證據，併購與回購都不是主因。","runway_years":11,"runway_post_y5":"🟢","endo_ceiling_basis":"內生上限無法可信算出，原因見護城河欄公式註記；保守視為共識成長超出上限，Bear 機率取 30%。","segments":{"expanded":false,"reason":"公司不揭露產品別營收，只有地區與大客戶占比；Workers 營收規模管理層 2026-08-06 未回答，無法拆分。"},"decay_signals":[{"item":"毛利率連兩季年減","status":"亮","note":"Q2 年減 320 個基點，Q3 年減 290 個基點。"},{"item":"核心市占縮減","status":"未亮","note":"管理層與客戶案例顯示份額上升，第三方原始數據未見。"},{"item":"主力產品提價後銷量下滑","status":"資料缺口","note":"事實表未涵蓋。"},{"item":"EPS 年化高於營收年化超過 5 個百分點","status":"亮","note":"Base 路徑 32.4% 對 26.3%，差 6.1 個百分點；共識 FY27 差距 3.4 個百分點。"},{"item":"FCF 對淨利低於 0.75 連兩年","status":"資料缺口","note":"GAAP 淨利為負，比率不適用；Q3 FCF 對非 GAAP 淨利 57%。"},{"item":"股權酬勞占營收高於 5% 且逐年上升","status":"資料缺口","note":"Q3 為 22.3%，水準超標，逐年趨勢事實表未涵蓋。"},{"item":"TAM 萎縮或被替代","status":"未亮","note":"公司與第三方預測都在擴大。"},{"item":"產業倍數近三年系統性下移","status":"資料缺口","note":"事實表未涵蓋同業倍數歷史。"},{"item":"維護性資本支出占 FCF 高於 60%","status":"資料缺口","note":"總網路資本支出約為 FCF 的 1.2 至 1.5 倍，維護性占比未揭露。"},{"item":"停止投資新產能且收入下滑","status":"未亮","note":"資本支出維持營收 14% 至 15%，營收加速。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"沒有配息與回購，成長也不靠併購，資本回饋不影響本次結論。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"併購都是小型補強，Deno 約 2,650 萬美元；已實現增量報酬事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未見回購。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"FY22 至 FY25 加權股數估計年增約 2.5%，高於 1.5%。","grade":"不過"}]},"valuation":{"basis":"非 GAAP Fwd P/E 為主，EV/S 為輔；起點用公司 FY26 指引 EPS $1.35。","tier":"高成長基礎設施軟體","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業前瞻倍數；唯一可用的是前份摘要 2026-08 的 DDOG 78.7 倍，已寫在情境假設。"},"fwd_pe":213.29,"peg":6.2,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"現價對指引 EPS 約 199 倍，對 FY27 共識 159 倍，前瞻 EV/S 32.3 倍，PEG 6.2。Base 五年年化約 0.5%，低於 8% 的最低要求，結論為偏貴。事實表沒有五年分位，只有 4 個年度端點的分位 100。","upside_short_pct":-1.0,"upside_mid_pct":-1.8},"trap_analysis":{"verdict":"🟡","label":"毛利率連降、獲利靠費用率，還不到陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 超額主要來自用量型收入；毛利率一年降 290 個基點；CEO 說資安衝擊約兩年；CEO 未回答與模型廠託管代理的競合界線。","assumption":"代理與資安需求在 2028 年後仍維持高速，Workers 單位經濟如管理層所說超過前兩代產品。","consequence":"營收年化掉到 14%、營益率回到 14%，FY31 EPS 約 $1.66，股價約 $75，五年跌 72%。","ruling":"採納，放進 Bear 並給 30%；與唯一致命事件同一條因果鏈，不另外計算。","watch":"營收年增、淨留存、毛利率，每季檢查。","evidence_refs":["substitute_technology#1","substitute_technology#2"],"fact_refs":["f_kpi7_dollar_based_net_retenti","f_kpi12_non_gaap_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 股權酬勞占營收 22.3%，非 GAAP 與 GAAP 營業利益差 2.05 億美元；股數估計年增約 2.5%；FCF 只有非 GAAP 淨利的 57%。","assumption":"營益率升到 28% 時，股權酬勞占比同步下降。","consequence":"即使營收達 Base，若股權酬勞仍占 15%，FY31 GAAP 淨利約為非 GAAP 的一半，50 倍終端倍數站不住。","ruling":"採納，Base 倍數只給 50 倍，並把股數增加算進 EPS。","watch":"股權酬勞占營收與稀釋股數，每季檢查。","evidence_refs":[],"fact_refs":["f_kpi4_sbc","f_kpi2_gaap_operating_income_lo","f_kpi3_free_cash_flow"]},{"view":"價格已反映太多","evidence":"現價約 199 倍指引 EPS、前瞻 EV/S 32.3 倍；股價跌 19% 後 Base 五年年化仍只有約 0.5%。","assumption":"市場會繼續為這段加速付高倍數。","consequence":"FY27 成長達標但倍數提前壓縮時，短期報酬仍可能為負。","ruling":"採納，這是等待的主因。","watch":"FY27 EPS 共識上修幅度與 Fwd PE FY2。","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_ev_s_fwd","f_price_at_dd"]}],"max_dd":{"lo":-75,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 330.5 → 本次 268.75（-18.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=330.5","side_b":"本次 price_at_dd=268.75","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 330.5 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 330.5 美元：Bull 價 509、Bear 價 107，五年期望值 −16.4%，基準年化 −4.7%，不對稱比 0.7","side_b":"本次情境、股價仍用 330.5 美元：Bull 價 511.2、Bear 價 74.7，五年期望值 −17.1%，基準年化 −3.6%，不對稱比 0.59","ruling":"先換情境、股價不動：五年期望值少 0.7 個百分點，基準年化多 1.1 個百分點。不對稱比由 0.7 變為 0.59。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 330.5 美元：五年期望值 −17.1%，基準年化 −3.6%，不對稱比 0.59","side_b":"本次情境、股價 268.75 美元：五年期望值 +1.9%，基準年化 0.5%，不對稱比 1.04","ruling":"再換股價、情境不動：起點價下跌 18.7%，五年期望值多 19.0 個百分點，基準年化多 4.1 個百分點，不對稱比由 0.59 升到 1.04。合計五年期望值比前份多 18.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與等待結論","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份判斷日股價 $330.5，結論偏貴、等待；Bull 25%、Bear 30%，最大回撤約 −70%。","side_b":"現價 $268.75，跌 18.7%，Base 五年年化由 −4.7% 升到約 0.5%，仍低於 8%；機率不變，回撤範圍改為 −50% 至 −75%。","ruling":"跌價改善了報酬，幅度不足以改變結論，維持偏貴與等待。","evidence_level":"事實表價格與公司財報","settle_metric":"Fwd PE FY2 與 Base 年化報酬","if_then":["若股價跌到 $206 以下且 Q4 基本面未破，分批反買","若股價先漲而 Q4 財報未支持上修路徑，不追"],"evidence_refs":[]},{"axis":"綜合評級、護城河方向與成長跑道","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合評級 B，護城河加寬，跑道寬，屬品質複利成長，非循環股。","side_b":"本次不變：Q3 淨留存 122%、營收加速、Act IV 首次認列營收，支持護城河與跑道；毛利率下滑是反向證據，還不足以改變方向。","ruling":"維持前份判斷。","evidence_level":"公司財報與電話會議","settle_metric":"淨留存與毛利率","if_then":["若淨留存連兩季低於 118%，護城河方向改為穩定，停止加碼"],"evidence_refs":["end_markets#0"]},{"axis":"價值陷阱風險","cause":"方法變動","prior_field":["trap"],"side_a":"前份：價值陷阱風險低。","side_b":"本次：風險中等，逐項計數亮 2 項，分別是毛利率連兩季年減，EPS 年化快過營收 6 個百分點。","ruling":"前份已知毛利率下滑，差別來自本次嚴格逐項計數，基本面沒有因此變差。","evidence_level":"公司財報與本次路徑","settle_metric":"衰退信號項數","if_then":["若亮到 3 項以上，風險升高，不追"],"evidence_refs":[]},{"axis":"進場重啟價位","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE FY2 ≤122x（≈$194；分母固定用共識 FY27 EPS $1.586，對應以自建模型 FY31 終值 $260 折現的 Base IRR +6%/yr）；或 AI／Workers 相關年化 run-rate 首度揭露 ≥$400M 且非 GAAP 毛利率連二季站回 73%+（論點增強，可不等回檔）","side_b":"Fwd PE FY2 ≤122x（≈$206；分母固定用共識 FY27 EPS $1.69，對應 Base 終值 $275 的年化 +6%）","ruling":"倍數 122 倍不變。分母由 $1.586 改為最新共識 $1.69，Base 終值由 $260 升到 $275，進場價位由約 $194 升到約 $206。跌到此價先重跑判斷，再分批建倉。","evidence_level":"Q3 財報與共識快照","settle_metric":"Fwd PE FY2","if_then":["若股價跌到約 $206 且基本面未破，分批反買"],"evidence_refs":[]},{"axis":"進場條件的第二路徑","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"AI／Workers 相關年化 run-rate 首度揭露 ≥$400M 且非 GAAP 毛利率連二季站回 73%+（論點增強，可不等回檔）","side_b":"同一組數字改為重跑條件，達標只上修路徑，不直接進場。","ruling":"即使達標讓 Base 終值上修兩成到約 $330，年化也只有約 4%，低於 6%，不足以免除價格條件。","evidence_level":"情境推算","settle_metric":"AI／Workers 年化營收與毛利率","if_then":["若兩項同時達標，重跑判斷；價格未到仍不追"],"evidence_refs":[]},{"axis":"前份營益率門檻","cause":"新證據","prior_field":null,"side_a":"前份：Q3 非 GAAP 營益率未達 17.6% 即論點失效；FY26 全年不得低於 15.5%。","side_b":"Q3 實際 17.5%，差 0.1 個百分點；營業利益 1.371 億美元高於指引中點 1.295 億，FY26 新指引 15.6%。","ruling":"按字面已觸發，裁定為削弱、未反轉。差距來自營收超預期 6.2%：超出的 4,600 萬美元營收帶來 760 萬美元營業利益，增量利益率只有 16.5%，用量型收入的利潤偏低。門檻改為 Q4 ≥18.5%、FY27 ≥20%。","evidence_level":"公司財報","settle_metric":"Q4 FY26 非 GAAP 營益率","if_then":["若 Q4 營益率低於 18.5%，確認削弱，不追","若 FY27 指引營益率 ≥20%，論點恢復成立，維持路徑"],"evidence_refs":[]},{"axis":"毛利率趨穩說法","cause":"新證據","prior_field":null,"side_a":"CFO 2026-06-09 說毛利率已觸底趨平；2026-08-06 說會穩定在當時水準（Q2 73.1%）。","side_b":"Q3 非 GAAP 毛利率 72.4%，季減 70 個基點，CFO 改談單位經濟毛利，沒有解釋這次下滑。","ruling":"屬程度差異：仍在 70% 至 77% 區間內，CFO 6 月也承認可能再下探。說法尚未證偽，列入監測：Q4 與 FY27 Q1 都低於 72% 就視為證偽。","evidence_level":"逐字稿對照","settle_metric":"非 GAAP 毛利率","if_then":["若連兩季低於 72%，Base 營益率下修 2 個百分點，停止加碼","若回到 73% 以上，視同趨穩，維持路徑"],"evidence_refs":["geo_supply_chain#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：成長連三次加速，FY26 指引三度上調，GAAP 獲利比最晚 2028 年的承諾提前超過一年，股價卻比 8 月低 19%；Q3 營收打敗指引 6%，FY27 共識看來偏低。","side_b":"等待：Base 路徑已高於共識，EPS 年化 32% 才換來約 0.5% 年化報酬；要賺年化 10% 需要接近 Bull 的 EPS。","ruling":"選等待。限制條件只有價格，基本面不需要再證明，報酬空間不夠。","evidence_level":"公司財報與情境推算","settle_metric":"Fwd PE FY2","if_then":["若 FY27 指引營收年增 ≥35% 且營益率 ≥22%，上修 Base 後重跑判斷","若股價先漲而證據未到，不追","若股價跌到約 $206 且基本面未破，分批反買"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"A 競爭：超大雲、Akamai、AI 新進者都在加壓，10-K 也預期降價與份額風險。","side_b":"B 結構：代理流量、資安支出與廠商整合轉好，Q3 多筆案例取代傳統廠商。C 其他：出口管制與 AI 爬蟲收費規則正在變動。","ruling":"雙向拉鋸，目前結構性轉好的力道較強；依據是淨留存 122% 與大客戶年增 25%，競爭壓力還沒反映在留存數字。","evidence_level":"公司財報與 10-K","settle_metric":"淨留存與大客戶淨增","if_then":["若淨留存連兩季低於 118%，改判競爭惡化中，不追"],"evidence_refs":["competitive_share_entrants#1","end_markets#0","channel_business_model_shift#1"]},{"axis":"Single Thing 新增","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未載明唯一致命點。","side_b":"2027 年底前，營收年增連兩季跌破 30%，同時淨留存跌回 118% 以下。","ruling":"本次依敏感度指定：成長失速同時壓低營收路徑與終端倍數，是情境裡影響最大的單一事件。","evidence_level":"情境推算","settle_metric":"營收年增與淨留存","if_then":["若事件發生，取消進場價位並重跑判斷；已持有則減碼一半"],"evidence_refs":[]},{"axis":"前份倍數論點","cause":"方法變動","prior_field":null,"side_a":"前份第三條論點：市場持續給 40x+ EV／營收；NET／DDOG Fwd PE 比連二季 >4.5x，或 DDOG Fwd PE 跌破 50x 則失效。","side_b":"本次第三條論點改為 Act IV 收費層，倍數論點改列風險與減碼指標，門檻保留；本次事實表沒有 DDOG 倍數，屬資料缺口。trailing EV/S 現為 35.1 倍。","ruling":"論點改寫、門檻保留，下次補上 DDOG 倍數再判斷。","evidence_level":"前份摘要與事實表","settle_metric":"NET／DDOG Fwd PE 比值","if_then":["若 DDOG Fwd PE 跌破 50x，下修 Base 終端倍數，已持有則減碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"驗證用量成長是否延續。","type":"假設驗證","maps_to":"H1","metric":"營收年增與淨留存","threshold":"FY27 營收年增 ≥30%；淨留存 ≥120%","action":"未達就下修 Base 路徑，不追","source_freq":"每季財報","date":null},{"n":2,"text":"驗證營益率擴張是否延續。","type":"假設驗證","maps_to":"H2","metric":"Q4 FY26 非 GAAP 營益率","threshold":"≥18.5%","action":"未達就確認論點削弱，不追","source_freq":"Q4 財報","date":"2027-02"},{"n":3,"text":"用量需求退潮的唯一致命事件。","type":"Single Thing","maps_to":"Single Thing","metric":"營收年增與淨留存","threshold":"連兩季年增低於 30% 且淨留存低於 118%","action":"取消進場價位並重跑判斷；已持有則減碼一半","source_freq":"每季財報","date":"2027-12"},{"n":4,"text":"價格回到足以提供合理報酬的位置。","type":"估值rearm","maps_to":"H1","metric":"Fwd PE FY2","threshold":"≤122x（約 $206）","action":"重跑判斷，基本面未破就分批建首倉","source_freq":"每日股價與每月共識快照","date":null},{"n":5,"text":"零組件短缺與關稅是否吃掉毛利率。公司損益上的吸收失敗以毛利率為準。","type":"風險","maps_to":"R2","metric":"非 GAAP 毛利率","threshold":"連兩季低於 70%","action":"不追；已持有則減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#1"]},{"n":6,"text":"BIS 關聯企業規則暫停期到 2026-11-10，觀察是否復效；是否延長事實表未涵蓋。","type":"風險","maps_to":"R7","metric":"BIS 規則狀態與公司揭露","threshold":"復效且公司揭露受影響客戶營收","action":"停止加碼，查下一份 10-K","source_freq":"BIS 公告與 10-K","date":"2026-11-10","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3"]},{"n":7,"text":"第二條曲線得到數字驗證時重新判斷。","type":"假設驗證","maps_to":"H3","metric":"AI／Workers 年化營收與非 GAAP 毛利率","threshold":"年化營收 ≥$400M 且毛利率連兩季 ≥73%","action":"重跑判斷，上修路徑；價格未到仍不追","source_freq":"每季財報","date":null},{"n":8,"text":"Q4 財報與 FY27 指引後重新檢視。","type":"複審日期","maps_to":"H1","metric":"FY27 營收與營益率指引","threshold":"營收年增與營益率指引公布","action":"重跑判斷","source_freq":"Q4 財報","date":"2027-02"}],"kill_metrics":[{"metric":"營收年增率與淨留存","bear_threshold":"連兩季年增低於 30% 且淨留存低於 118%","window":"至 2027 年底","source":"季度新聞稿與財報電話會議","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"連兩季低於 70%","window":"滾動兩季","source":"季度財報電話會議","last_status":"ok"},{"metric":"非 GAAP 營業利益率","bear_threshold":"Q4 FY26 低於 18.5%，或 FY27 低於 20%","window":"2027-02 至 2028-02","source":"季度新聞稿","last_status":"warning"},{"metric":"NET／DDOG Fwd PE 比值；DDOG Fwd PE","bear_threshold":"比值連兩季高於 4.5x，或 DDOG 跌破 50x","window":"滾動兩季","source":"共識快照（本次資料缺口）","last_status":"unknown"},{"metric":"股權酬勞占營收","bear_threshold":"FY28 仍高於 20%","window":"至 FY2028","source":"新聞稿非 GAAP 調節表","last_status":"warning"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#1","reason":"條文是 10-K 的通用風險敘述，沒有具體案件、金額或時點；同一份事實表的一手紀錄與搜尋都未見調查，且列出的併購規模僅數千萬美元。"},{"ref":"geo_supply_chain#0","reason":"來源是投資人簡報前瞻聲明的制式段落，沒有受影響營收、機房或時點，無法轉成可驗證的損益影響。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='↑', week26=37.03, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 的算術只到總營收和營益率，沒有分部的量乘價骨架。NET 2021 年高倍數進場後五年報酬遠低於 13.7%/yr，判斷物也沒有說明這次為何不同，所以 Bull 依據目前站不住。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"Fwd PE FY2 ≤122x（≈$206；分母固定用共識 FY27 EPS $1.69，對應 Base 終值 $275 的年化 +6%）","exec_line":"現價不追。跌到約 $206 且 Q4 基本面未破，重跑判斷後分批建首倉；續漲而證據未到則不追。"},"reasoning":{"industry":"Q3 營收 7.825 億美元，年增 39%；美國占 52%、年增 44%，EMEA 占 26%、年增 32%，APAC 占 14%、年增 32%；年付 10 萬美元以上大客戶約 5,000 家，貢獻 75% 營收。公司未揭露產品別營收。非 GAAP 毛利率 72.4%、營益率 17.5%，GAAP 營業虧損 6,790 萬美元、營益率 −8.7%。Q3 的超額來自用量型收入，CFO 說是長尾客戶提前用完資金池再續約（2026-11-05 CFO）。單點依賴：10-K 揭露 FY23 至 FY25 沒有客戶超過營收 10%，客戶集中度低；供應端依賴少數伺服器零組件商，是毛利率風險。","moat":"機制：全球網路加上 isolates 架構，免費層吸引流量，流量產生威脅情報，情報再吸引付費客戶；CEO 說前沿實驗室和資安公司會先把漏洞通報給 Cloudflare（2026-11-05）。同業 ROIC 差距取不到，改用留存與份額：淨留存一年由 119% 升到 122%，大客戶年增 25%，Q3 案例裡取代了傳統 Zero Trust、DDoS 與 CDN 業者。反向證據：非 GAAP 毛利率年減 290 個基點；截至 2026 年中的 TTM GAAP 營益率 −8.1%，低於 ZS、CRWD、AKAM，FCF 利潤率 12.5% 也落後 ZS 與 CRWD。CEO 所說 7 月以來增加全網約 5% 引用第三方資料，原始數據未見。AI 曝險：新增用量長在自有網路上，屬於強化；AI 年化營收未揭露，淨增量算不出來，2027 年中仍無揭露就視為未證。","growth":"成長以用量和新客為主，價的貢獻沒有直接證據，併購規模小，沒有回購。共識 EPS：FY26 $1.26、FY27 $1.69、FY28 $2.27，FY26 到 FY28 年化 34.2%；這是財報前快照，家數事實表未涵蓋。FY27 共識營收 38.75 億美元，年增約 30.7%。以 2,380 億美元 TAM 算，滲透率 1.2%，年增 30% 至 39% 時約 10 至 12 年達 30% 滲透率。Act IV 在 Q3 首次認列營收，金額未揭露，CEO 說 10 年後可能成為最大業務，第二條曲線已起步、規模未證。缺口歸因：Base 路徑 EPS 年化約 32%、營收年化約 26%，差距來自營益率由 15.6% 升到 28%，不靠回購。","governance":"Q3 股權酬勞含薪資稅 1.741 億美元，占營收 22.3%；非 GAAP 營業利益 1.371 億與 GAAP 營業虧損 6,790 萬之間差 2.05 億美元。由 FY22 到 FY25 的淨損與每股虧損反推，加權股數約由 3.28 億增至 3.53 億，年增約 2.5%，受每股虧損四捨五入影響，只能當概數。Q3 FCF 8,210 萬美元，占非 GAAP 淨利 1.437 億的 57%；網路資本支出占營收 15%。CFO 8 月上修重組現金費用上限至 1.3 億美元，這季 FCF 受多少影響事實表未涵蓋。2026-08 發行 25 億美元 0% 可轉債（2031 到期、轉換價約 $496.94）並償還 13 億美元舊券。近三年現金去向四分與債務到期結構事實表未涵蓋。","valuation":"事實表的 213 倍用財報前共識 $1.26；公司新指引 $1.35，現價約 199 倍。對 FY27 共識 $1.69 為 159 倍，PEG 約 6.2。前瞻 EV/S 32.3 倍、trailing 35.1 倍，都在 4 個年度端點的最高位；這 4 點不是五年分位，五年分位事實表未涵蓋。事實表股數 3.58 億未含完整稀釋，以 Q4 指引的 3.79 億股算，市值約 1,019 億美元，前瞻 EV/S 約 34 倍。股價較前份判斷日 $330.5 跌 18.7%，同期 FY26 營收指引中點上調約 3.4%、EPS 上調約 7.6%，但 Base 五年年化只升到約 0.5%。共識近三月修正 0% 是快照未更新，不能解讀成市場沒有上修。賣方目標價最新只到 6 月，共識 $250、區間 $136 至 $305，僅供參考。短期目標以 FY27 EPS $1.90 乘 140 倍計 $266；中期以 FY29 EPS $3.52 乘 75 倍計 $264。","premortem":"價值陷阱風險中等：衰退信號亮 2 項，分別是毛利率連兩季年減與 EPS 成長快過營收 6 個百分點。成長熄火測試：以 Base FY29 EPS $3.52 為基礎，成長降至 15%、10%、5%，Fwd P/E 壓到 30、22、15 倍，股價約 $106、$77、$53，相對現價跌 61%、71%、80%，三項都低於現價。Q2 與投資人日有 8 條迴避紀錄，最影響判斷的是 Workers 營收規模（2026-08-06 CEO 自承沒有完全回答）和與模型廠託管代理的競合界線（2026-06-09）。歷史最大回撤事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺企業資安與連線預算，再加上開發者與 AI 代理的用量費；錢卡在 Cloudflare 的全球網路，流量進出都要經過這一層。","moat":"護城河在加寬。網路規模、免費用戶帶來的流量與威脅情報互相強化，定價權大致持平。","growth":"成長跑道還長，五年後仍有空間。","capital":"資本配置偏弱：股權酬勞占營收 22.3%，股數持續增加，沒有回購抵銷。","valuation":"現價要 FY31 EPS 達到約 $5.4、屆時還值 50 倍才打平；要賺年化 10%，EPS 要到約 $8.7，接近 Bull 路徑。這個價位報酬空間不夠。","how_wrong":"看錯的方向有兩個：用量與資安需求比預期更持久，等價位會錯過；或這波需求退潮很快，現在的倍數撐不住。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 Fwd PE FY2 ≤122x（約 $206），且 Q4 FY26 財報基本面未破。","qc48_result":"fail","qc48_note":"Bull 的算術只到總營收和營益率，沒有分部的量乘價骨架。NET 2021 年高倍數進場後五年報酬遠低於 13.7%/yr，判斷物也沒有說明這次為何不同，所以 Bull 依據目前站不住。","trap":"🟡","val":"🔴","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":268.75,"week26_return_pct":37.03,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"非 GAAP EPS 未扣占營收 22.3% 的股權酬勞；事實表 FY1 共識 $1.26 是財報前快照，公司新指引 $1.35。兩處都讓分母不乾淨，但無論用哪個都偏貴，結論不變。"},"catalysts":[{"date":"2026-11-10","date_precision":null,"type":"regulatory","event":"BIS 關聯企業規則暫停一年到期","impact":"中","watch":"是否復效或延長，以及公司揭露的受影響客戶。"},{"date":"2026-11-18","date_precision":null,"type":"other","event":"RBC 全球科技、網路、媒體與電信會議","impact":"低","watch":"毛利率與 FY27 用量趨勢的說法。"},{"date":"2026-12-09","date_precision":null,"type":"other","event":"Barclays 全球科技會議","impact":"低","watch":"Workers 單位經濟與銷售交接。"},{"date":"2026-12","date_precision":"month","type":"other","event":"銷售長 Mark Anderson 退休，Christian Smith 接任","impact":"中","watch":"銷售生產力與大客戶淨增。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY26 財報與 FY27 全年指引","impact":"高","watch":"營收年增、Q4 營益率是否 ≥18.5%、毛利率是否守住 72%、GAAP 是否如期轉盈。"}],"_projected_from":"v19"}
```
