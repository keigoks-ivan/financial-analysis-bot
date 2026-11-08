你是 stock-analyst v20 的**散文層（prose）agent**，標的 ON（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ON　日期：2026-11-08　archetype：None　前份裁決：2026-06-20　B 衛星候選/觀望（深度週期股剛Q1'26 inflect +5%YoY，股價自52W低$44.56已近3倍且跑過分析師均標$106；SiC#2+CIS#1+FCF韌性真實，但EV放緩是SiC結構逆風+Sony CIS競爭+估值🟠+MA🟡觀察池後谷底火箭極伸展；機率加權合理價$71/-42%下行不對稱；等大幅回檔$70-85+SiC/EV復甦確認，長期信心僅中）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1467B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（409B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（995B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1473B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1055B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（679B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1110B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2314B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3592B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3034B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1467           3873-5533      5 條（2–6 內）  
s3                  8000         409           5314-7591      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3523          8034-11477      5 條（2–6 內）  
s6                 11000         679          7225-10321      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1110           1673-2390      3 條（2–6 內）  
s10                 5000        2314           1880-2686      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3034           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4872B；至少需散文≈40.13KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−82%
−69%
−55
−55%
−51%
−47.9%
−38.65
−30
−30%
−25%
−4.9%
0
0.13
0.24
0.29
0.46
0.5%
0.53
0.6%
0.7
0.78
0.85
0.90
1
1%
01
1.01
1.19
1.5%
1.5
1.56
1.6%
1.75
1.80
2%
2
02
2.2%
2.3
2.35
2.5%
2.99
03
3
3%
3.14
3.2
3.22%
3.28
3.32
3.4
3.5
3.7
3.80
3.8
3.87
3.9
3.92
3.96
4
4.15
4.4
4.45
4.5
4.67
4.71
4.8
4.886
4.9
4.95
05
5%
5
5.02
5.3%
5.5%
5.55
5.97
6
06
6%
6.08
6.2
6.4
6.6%
6.7
7
07
7.15
7.4
7.5
7.77
7.80
7.8
08
8
8.1
8.7%
8.90
09
9%
9
9.4
9.8%
9.9
10%
10
10.5
10.9
11
11%
11.4
11.5
11.8
12%
12
12.4
13.0
13.4
13.44
14
14.0
14.5%
14.9%
15
15%
16%
16
16.23%
17%
17
17.2%
17.22
17.8
19
19.12%
19.3
19.5
20
20%
21.5
21.6
22.0%
23.2%
24
24.16%
25
25%
25.38%
26
26%
27%
27.6
28%
28
28.55%
30%
30
31
31.04
33%
33
33.1%
33.84%
34.16
35%
36.1
36.1%
37.02
37.6%
38.65%
38.68%
39%
40%
40
40.3
41%
41.12%
41.2%
41.6%
42%
42
42.5%
43%
43.5%
44.5%
44.56
45%
45
45.6
47
47.9%
48%
49.0%
49
50%
52
53%
53
54%
55%
55
56.43%
60.0
60%
60
60.19%
60.24%
63.31
65
65%
66.07
66.1
69
69.17
70
71%
71
74
75.94
76
79
79%
80%
82.8%
83%
83.3
85
87.6
89
90
91
92%
93%
100%
100
104
108.09
110
113
121.62
140%
150%
170
175%
176%
186
200
210
232
250
300
450
500
800
2004
2023
2025
2026
2027
2028
2029
2030
20261108
2,000
3,700
9,000
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
{"meta":{"ticker":"ON","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"onsemi"},"oneliner":"功率半導體復甦加上 AI 資料中心放量，現價以 16 倍計只要求 FY27 EPS 約 3.96 美元，比共識低 16%；但約 70 億美元的 Synaptics 併購財務條款未明，車用又連兩季讓路，先等併購槓桿的答案，不追價。","thesis":{"H":[{"id":"H1","text":"AI 資料中心電源成為第二引擎，靠完整電源產品線和 800V 架構擴大份額。","2y":"2027 年營收約翻倍到 12 億美元以上","5y":"2030 年有機不低於 25 億美元，含 Ferric 不低於 30 億美元","10y":null,"threshold":"2027 全年不低於 11 億美元","source":"季報與 10-Q 新增的 AI 資料中心分部","drift_rule":"近四季累計低於路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"},{"id":"H2","text":"稼動率、Fab Right 和新品組合把毛利率帶回高 40%。","2y":"2027 全年非 GAAP 毛利率不低於 43.5%，2027 Q4 不低於 45%","5y":"FY31 約 50%，低於管理層 2030 年 53%","10y":null,"threshold":"2027 全年不低於 43.5%","source":"季報與法說的稼動率揭露","drift_rule":"近四季毛利率低於路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"},{"id":"H3","text":"車用下滑只是供給調配，2027 年回到長期成長，含量增加抵銷 SAAR 持平。","2y":"2027 Q1 車用不低於 7.8 億美元，全年約增 9%","5y":"2030 年車用仍是最大市場，年化約 9%","10y":null,"threshold":"2027 Q1 車用不低於 7.8 億美元，FY27 總營收不低於 74 億美元","source":"季報與法說","drift_rule":"近四季車用營收低於路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"}],"R":[{"id":"R1","text":"約 70 億美元的 Synaptics 併購：條款已修訂，中國審查可能嚴格，完成後去槓桿取代回購。","h_ref":"H2","clock":"🔥","threshold":"淨負債高於近四季自由現金流 4 倍，或新發股數高於 15%，或 2027 年底前仍未取得中國審批","evidence_refs":["regulatory_antitrust#1"]},{"id":"R2","text":"車用讓路造成份額或補庫存訂單流失。","h_ref":"H3","clock":"⚡","threshold":"2027 Q1 車用低於 7.4 億美元","evidence_refs":["end_markets#0"]},{"id":"R3","text":"中國反傾銷、樂山封測廠與出口管制；中國約占營收 30%（二手來源）。","h_ref":"H3","clock":"🔥","threshold":"對 onsemi 課稅不低於 20% 且毛利率季減不低於 100 基點","evidence_refs":["regulatory_antitrust#2","reg_tariff_export#0","geo_supply_chain#3"]},{"id":"R4","text":"循環反轉：AI 資本支出放緩或補庫存退潮，上輪股價跌 71%。","h_ref":"H1","clock":"🔥","threshold":"通路庫存高於 11 週，或存貨增速連 2 季高於營收增速","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R5","text":"SiC 證券集體訴訟未結，減損與重組反覆出現，非 GAAP 獲利可能高估真實盈餘。","h_ref":"H2","clock":"🐢","threshold":"集體認證通過且和解金高於約 4.9 億美元，或再核准 2 億美元以上減損","evidence_refs":["lawsuit_class_action#0","major_events#2","major_events#3"]}],"single_thing":{"description":"Synaptics 併購以高槓桿完成：合併文件或完成後首份財報顯示淨負債高於近四季自由現金流 4 倍，或新發股數超過現有流通股 15%。","why_fatal":"這是最大的單一敏感度：毛利率少 500 基點約減 FY31 EPS 1.19 美元、終端價 19 美元；高槓桿同時帶來利息（新債 60 億美元按假設利率 6% 約減 EPS 0.78 美元）和倍數下修（16 倍降到 12 倍），Base 終端價合計少約 40 美元。現有淨負債僅 3.4 億美元，若約 70 億全數現金，淨負債升到約 79 億，是近四季 FCF 的 4.9 倍，此時再遇循環下行，回購支撐也沒有了。","if_happens":"Bear 機率上調到 40% 以上並重做 EPS 路徑；未持有者不進場，已持有者減碼一半，車用同時失守則清倉。","how_monitor":"2026-10-01 的 8-K 與合併文件中的現金股票比例、融資安排；中國審批進度；完成後首份 10-Q 的淨負債。","probability":"約 35%（12～24 個月）。修訂條款未收錄於事實表，這是粗估，讀到條款後應立即改成接近 0 或接近 100。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.44,"peg_fy2":0.46,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":0.29,"FY2026E":3.28,"FY2027E":4.71,"FY2028E":6.08},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識（2026-11-07），判斷為 non-GAAP，依據是 Q3 non-GAAP 0.90 加 Q4 指引中點約 1.01 與 3.28 相符。基期 FY2025A 0.29 為 GAAP 稀釋 EPS，含減損與加速折舊；事實表沒有 FY2025 non-GAAP，因此成長率只看 FY2026E 到 FY2028E。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"FY22 到 FY25 營收由 83.3 億跌到 60.0 億美元，毛利率由 49.0% 跌到 33.1%，沒有虧損年，資本支出僅占營收 2%～5%，屬需求量循環而非商品價格循環；AI 資料中心另算結構成長。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性偏緊、將會反轉：Wolfe 的 Chris Caso 認為 2028 前難見全面過剩（2026-07-30，泛半導體），8 吋代工 2026 上半年漲 5%～15%；反方是 SiC 上游稼動率約 50%，中國成熟製程新產能可能使部分品類交期正常化。","bargaining":{"up":"8 吋代工與投入成本上漲，約 65% 產品外部製造（2026-09-16 投資人日），上游目前較強。","down":"車用 OEM 與超大型雲端客戶議價力強；客戶約 9,000 家但經銷占 54%，漲價目前只用來抵銷投入成本。","geo":"中國約占營收 30%（二手來源），樂山封測廠持股 80%，商務部反傾銷調查未結。"},"profit_pool_dir":"利潤池由車用 SiC 往 AI 電源移動；五年占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表只有管理層口徑的 2030 年 TAM 與 SiC 單點滲透率，沒有五年前基期和利潤池占比，展開只會轉抄公司說法。"}},"moat":{"mechanism":"車規認證與長設計週期，加上從高壓到低壓的完整電源產品線；AI 資料中心再以系統級方案和功率密度競爭。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：2026 年 AI 資料中心約 6.2 億美元，年增 140%，非 GAAP 毛利率連升五季，Google 等平台開始量產出貨。定價力在 SiC 縮減、矽與類比穩定，漲價僅抵銷成本。車用份額沒有第三方正反證據。","peer_na_reason":"事實表只有同業利潤率，沒有投入資本，算不出 ROIC 差距，改用毛利率、營益率與 FCF 率差距。","threats":[{"level":"🔴","text":"中國低價 SiC 與產能過剩壓低價格，onsemi 捷克廠 2025 年裁約 170 人後，2026-06 再傳裁 200～300 人。","p":45,"evidence_refs":["competitive_share_entrants#3","geo_supply_chain#2","geo_supply_chain#4","substitute_technology#2","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"]},{"level":"🟡","text":"AI 電源份額未必如預期，管理層也承認 Vcore 進場較晚；每代架構都會重開插槽。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"對手取得政府補貼，中國成熟製程新產能可能使部分品類交期正常化。","p":30,"evidence_refs":["competitive_share_entrants#2","supply_demand_durability#2"]},{"level":"🟡","text":"10-K 的技術替代與產品過時風險屬通用揭露；目前 800V 牽引逆變器仍全用 SiC，垂直 GaN 則是 onsemi 自有路線。","p":20,"evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"暫判低利益率×低周轉：TTM GAAP 營益率 19.12%，存貨約 186 天；投入資本事實表未涵蓋，周轉率無法計算。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"客戶要解決的是功率密度和電氣化，AI 機櫃的 onsemi 內容由約 1.5 萬美元升到 11.5 萬美元以上（2026-09-16 投資人日，公司說法），延後代價高。公司解法能否勝出放在下一項判斷。"},{"item":"決策層級","level":"🟡","text":"替代性要看單一插槽：車規設計案認證長，2026-08-03 法說稱部分客戶下單到 2028；但 AI 電源每代架構都重開插槽。漲價後流失率與重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"最難取代的環節是 GPU 與雲端平台，onsemi 在零件層。漲價目前只抵銷投入成本，管理層也表示要與客戶分享創造的價值，毛利率低於類比同業約 20 個百分點。"},{"item":"社會容忍度","level":"🟡","text":"終端消費者不直接面對這筆成本，限制來自政策：中國反傾銷調查、美中出口管制與各國補貼；onsemi 捷克項目本身也獲歐盟核准 4.5 億歐元補助。"}],"roiic":"事實表未涵蓋投入資本，算不出數字。FY22 到 FY25 營業利益由約 27.6 億降到約 7.5 億美元，歷史增量報酬為負，但這段跨下行循環且含減損，不能外推。","reinvest_rate":"折舊與營運資金事實表未涵蓋，只能算收購項：Ferric 與 Synaptics 合計約 76 億美元，約為近四季稅後營業利益 10 億美元的 7.5 倍。","endo_ceiling":null,"formula_note":"內生成長率需要增量 ROIC 與完整再投資率，兩者輸入不足，留空，不用推估值代替。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","ON":38.68,"TXN":60.24,"NXPI":56.43,"MCHP":60.19,"STM":33.84,"unit":"%"},{"metric":"營業利益率","ON":19.12,"TXN":41.12,"NXPI":28.55,"MCHP":16.23,"STM":6.64,"unit":"%"},{"metric":"FCF 利潤率","ON":25.38,"TXN":35.24,"NXPI":24.16,"MCHP":21.69,"STM":3.22,"unit":"%"},{"metric":"研發密度","ON":8.85,"TXN":10.09,"NXPI":17.92,"MCHP":22.24,"STM":14.56,"unit":"%"}],"competitors":[{"name":"TXN","gm":60.24,"om":41.12,"fcf_margin":35.24,"rd_intensity":10.09,"strategy_note":"毛利率 60.24%、營益率 41.12%，是類比獲利標竿；2026 資本支出降到 20～30 億美元，供給紀律有利同業定價。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"NXPI","gm":56.43,"om":28.55,"fcf_margin":24.16,"rd_intensity":17.92,"strategy_note":"毛利率 56.43%，車用與工業競爭者；FCF 率 24.16%，略低於 onsemi，表示 onsemi 的現金轉換不輸，但毛利率差距大。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"MCHP","gm":60.19,"om":16.23,"fcf_margin":21.69,"rd_intensity":22.24,"strategy_note":"毛利率 60.19%、營益率僅 16.23%，資料截至 2026-06；稱庫存去化接近尾聲，是循環回升的旁證。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"STM","gm":33.84,"om":6.64,"fcf_margin":3.22,"rd_intensity":14.56,"strategy_note":"毛利率 33.84%、FCF 率 3.22%，是 SiC 與車用直接對手，獲利明顯弱於 onsemi。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主；價格抵銷成本；毛利率擴張貢獻 EPS 的大部分增幅；併購外加且未納入公司長期模型；回購在併購完成後讓位給去槓桿。","runway_years":"SiC 目前約占電動車牽引逆變器 17.2%（2026 Q1），年增速事實表未涵蓋，無法推算到 30% 所需年數。","runway_post_y5":"🟢","endo_ceiling_basis":"內生上限算不出：投入資本、折舊與營運資金事實表未涵蓋。2027 年資本支出約占營收 5%，管理層稱預測期間不再增加 brownfield，有機再投資很低，共識年化 36.1% 的主要來源是毛利率擴張，歸因明確。情境樹按超過內生上限處理。","segments":[{"item":"車用","value":"Q3 7.77 億美元，季減 1%、年減 1%；Q4 指引減高個位數；管理層 2027 年回到約 9% 成長。"},{"item":"工業","value":"Q3 4.67 億美元，季增 10%、年增 9%；Q4 指引增低雙位數，主因電網與能源基建。"},{"item":"AI 資料中心","value":"Q3 1.80 億美元，季增 39%、年增 175%；2026 年約 6.2 億，2027 年預期翻倍；2030 年目標 30 億以上，其中 5 億來自 Ferric。"},{"item":"其他","value":"Q3 2.99 億美元，Q4 增高十位數來自外部製造的大客戶專案，2027 年不延續此增速。"}],"decay_signals":["EPS 成長高於營收成長：FY26 到 FY28 EPS 年化 36.1%，FY27 營收增 14.9%，差距超過 5 個百分點；成立，來自谷底回升。","停止擴產且營收三年內下滑：FY23 到 FY25 營收連三年下滑，2026 資本支出約占營收 2%；成立，但營收已轉正。","產業估值倍數三年趨勢：事實表未涵蓋，不計入。","核心市占：管理層稱未流失，第三方份額資料事實表未涵蓋，不計入。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"2023～2026 回購","value":"42 億美元，占 FCF 92%，股數減 12%；剩餘授權 53 億美元（2026-09-16 投資人日）。"},{"item":"2026 Q2 回購","value":"3.32 億美元。"},{"item":"2026 Q3 回購","value":"2,000 萬美元，受 Synaptics 交易限制。"},{"item":"併購後順位","value":"先投資業務，再快速去槓桿，回購改為伺機（2026-11-02 法說，Thad Trent）。"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Synaptics、Ferric 尚未完成，沒有已實現報酬；歷史併購報酬事實表未涵蓋。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2023～2026 回購 42 億美元、股數淨減 12%，推得均價上限約 79 美元；近四季每股 FCF 約 4.15 美元，收益率至少約 5.3%。10 年期公債殖利率事實表未涵蓋，無法比較。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 占 GAAP 營業利益 9.8%，約 3,700 萬美元，年化約 1.5 億美元，約占市值 0.6%，低於 1.5%；2023～2026 股數淨減 12%。","grade":"過"}]},"valuation":{"basis":"Fwd P/E 與 PEG，分母為 FY2026E 共識 EPS，並對照 FY2027E。同業現值倍數事實表未涵蓋，終端倍數以自身 FY1 19.3 倍與 FY2 13.4 倍對照。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比，無法做倍數對照；同業判讀放在護城河題。"},"fwd_pe":19.3,"peg":0.53,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"63.31÷3.28＝19.3 倍；63.31÷4.71＝13.4 倍；PEG＝19.3÷36.1＝0.53。數字偏低，但銷售倍數在年度端點 65～69 百分位，且 FY27 毛利率和併購後股數都是爭點，因此只判合理，不判便宜。","upside_short_pct":19.5,"upside_mid_pct":40.3},"trap_analysis":{"verdict":"🟡","label":"循環復甦進行中，不是價值陷阱；但便宜程度取決於併購後的每股分母"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"上輪下行股價由 108.09 跌到 31.04，降價與低稼動使單季非 GAAP 毛利率落到 37.6%；SOX 歷次回落最深 −82%；Synaptics 約占現市值 28%，且可能面臨中國嚴格審查。","assumption":"假設 2027 年起需求續強，併購不會把資本結構壓垮。","consequence":"五年後虧 50% 的最可能路徑：高槓桿完成併購後循環在 2028～2029 反轉，AI 資本支出放緩，SiC 價格戰延續，EPS 停在 3 美元附近，配 10～12 倍，股價 30～40 美元。","ruling":"採納，併入 Bear 33%。與 Single Thing 部分重疊：併購是起點，循環反轉是放大器，所以另設庫存與通路條件。","watch":"併購後淨負債、通路庫存週數、存貨與營收增速差、AI 資料中心季增率。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","regulatory_antitrust#1"],"fact_refs":["f_net_debt_m","f_ev_m","f_week26_return_pct"]},{"view":"論點成功但股東經濟變差","evidence":"AI 資料中心 2027 年預期翻倍，但 Ferric 付現 6 億美元加最多 1.75 億業績獎金，Synaptics 約 70 億；Q3 回購降到 2,000 萬美元，2025-11 又核准 2～3 億美元減損與加速折舊；2030 目標上調的 5 億全來自收購。","assumption":"假設營收與毛利率成功會等比例轉成每股自由現金流。","consequence":"營收與毛利率達標，每股價值卻被併購溢價、利息和新股吃掉；投資人日的 100% 自由現金流回饋在併購後不成立。","ruling":"部分採納。有機部分的資本效率仍佳，資本支出僅 5%；但在併購報酬出現前，不把管理層 30%～35% 的 FCF 目標算進每股價值。","watch":"每股自由現金流、GAAP 與 non-GAAP EPS 差距、併購後回購金額。","evidence_refs":["major_events#3","major_events#0","major_events#1"],"fact_refs":["f_kpi5_fcf","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"股價大跌後，P/S 3.87 倍、EV/S 3.92 倍仍在四個年度端點的 69、65 百分位；Trailing P/E 37.02 倍；FY27 共識隱含毛利率約 44.5%～45%。","assumption":"低本益比的結論依賴 FY27 EPS 4.71 能達成。","consequence":"若共識高估，現在看到的 13.4 倍其實不便宜。","ruling":"反駁。即使 FY27 毛利率只有 43%，EPS 仍約 4.4 美元，現價約 14 倍；銷售倍數高是因毛利率仍在谷底回升。真正要防的是併購改變分母，不是營運預期太滿。","watch":"2027 Q1、Q2 非 GAAP 毛利率與共識 FY27 EPS 修正。","evidence_refs":[],"fact_refs":["f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_pe_current","f_consensus_eps_fy2"]}],"max_dd":{"lo":-55,"hi":-30,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 121.62 → 本次 63.31（-47.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=121.62","side_b":"本次 price_at_dd=63.31","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 121.62 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 121.62 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 121.62 美元：Bull 價 210、Bear 價 45.6，五年期望值 −4.9%，基準年化 0.5%，不對稱比 0.7","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.7。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 121.62 美元：五年期望值 −4.9%，基準年化 0.5%，不對稱比 0.7","side_b":"本次情境、股價 63.31 美元：五年期望值 +82.8%，基準年化 14.5%，不對稱比 5.02","ruling":"再換股價、情境不動：起點價下跌 47.9%，五年期望值多 87.6 個百分點，基準年化多 14.0 個百分點，不對稱比由 0.7 升到 5.02。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 121.62，估值偏貴（🟠），機率加權合理價 71 美元。","side_b":"本次：股價 63.31，FY1 19.3 倍、FY2 13.4 倍，估值轉為合理（🟡），但分母有爭議。","ruling":"改變主要來自股價下跌 48%，FY1 共識近三個月僅上修 2.5%。","evidence_level":"事實表","settle_metric":"FY27 共識 EPS 與併購後股數","if_then":[],"evidence_refs":[]},{"axis":"評級與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：評級 B、陷阱風險 🟡，理由是估值過高，要等回檔到 70～85 美元且 SiC／EV 復甦確認。","side_b":"本次：評級 B、陷阱風險 🟡，價格條件已過，新限制是前份之後才簽的 Synaptics 併購。","ruling":"結果相同但理由換了：貴的問題解除，資本結構的問題出現。","evidence_level":"一手文件（8-K）","settle_metric":"合併文件揭露的融資結構","if_then":[],"evidence_refs":["major_events#0"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這幾欄為空，沒有護城河方向、五年後成長空間、公司類型、循環位置、情境機率與最大回撤。","side_b":"本次補上：護城河方向 →、五年後成長空間 🟢、循環／商品類、早循環、機率 20／47／33、最大回撤 −30%～−55%。","ruling":"這是欄位補齊，不代表基本面由無到有的變化。","evidence_level":"判斷","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 由無到有","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點，Single Thing 欄為空。","side_b":"Synaptics 併購以高槓桿完成：合併文件或完成後首份財報顯示淨負債高於近四季自由現金流 4 倍，或新發股數超過現有流通股 15%。","ruling":"協議在 2026-06-25 簽訂，晚於前份的 06-20，因此新增。","evidence_level":"一手文件（8-K）加二手估值","settle_metric":"淨負債÷近四季自由現金流；新發股數÷流通股","if_then":["若兩項都未超標或交易終止，重跑完整研究；若超標，已持有者減碼一半，未持有者不進場。"],"evidence_refs":["major_events#0","regulatory_antitrust#1"]},{"axis":"重新進場、減碼與清倉門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件，也沒有清倉或減碼的數字清單；只寫等回檔到 70～85 美元且 SiC／EV 復甦確認。","side_b":"本次：合併文件顯示完成後淨負債不高於近四季自由現金流 4 倍且新發股數低於 15%才重跑研究；車用 2027 Q1 低於 7.4 億美元減碼一半；併購槓桿與車用同時失守則清倉。","ruling":"價格條件已過，等待對象改為併購條款，因此改用事件條件。","evidence_level":"一手文件與法說","settle_metric":"合併文件融資結構；2027 Q1 車用營收","if_then":["若併購槓桿與車用同時失守，清倉。"],"evidence_refs":["major_events#0","end_markets#0"]},{"axis":"前份假設與風險門檻對帳","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：FY27 營收高於 70 億美元；2026 資料中心高於 5 億美元；FY27 非 GAAP 毛利率不低於 42%；SiC 連 2 季年減加 PSG 季減則減倉；ISG 連 2 季衰退加份額流失則重評；股價高於均標 20% 加動能轉弱則等回檔。","side_b":"本次：FY27 營收不低於 74 億美元；2027 AI 資料中心不低於 11 億美元；FY27 毛利率不低於 43.5%；SiC／PSG 與 ISG 兩項保留；股價高於均標 20% 一項退休。","ruling":"2026 資料中心預期已達 6.2 億美元，Q4 毛利率指引中點 42.5%，舊門檻已過或將過，所以上調。現價低於各家均標 41%～79%，高於均標的條件不成立，退休。SiC 全年營收與份額事實表未涵蓋，標資料缺口。","evidence_level":"法說與事實表","settle_metric":"各假設對應的季報數字","if_then":[],"evidence_refs":[]},{"axis":"車用下滑是供給調配還是份額流失","cause":null,"prior_field":null,"side_a":"Hassane El-Khoury（2026-11-02）：短期、供給驅動，沒有流失份額，終端需求全數支援，2027 Q1 恢復，全年回到長期目標。","side_b":"Thad Trent（2026-08-03）原本指引 Q3 車用小增，實際季減 1%、年減 1%，Q4 再減高個位數；被延後的正是 OEM 為防缺貨而下的補庫存單。","ruling":"可調和，程度差異。暫採管理層說法但標為未證，預設期限：2027 Q1 車用低於 7.4 億美元，暫時性歸因即告失效。","evidence_level":"管理層說法，無第三方份額","settle_metric":"2027 Q1 車用營收","if_then":["若 2027 Q1 車用不低於 7.8 億美元，維持 H3。","若低於 7.4 億美元，已持有者減碼一半，未持有者不進場。"],"evidence_refs":["end_markets#0"]},{"axis":"2027 毛利率節奏","cause":null,"prior_field":null,"side_a":"Thad Trent（2026-11-02）：2027 年全年毛利率持續擴張。","side_b":"同一場法說：稼動率落後兩季反映，Q3、Q4 都是 83%，代表 2027 上半年損益沒有稼動率推升，只能靠新品組合、漲價和 Fab Right，後兩項效益多在 2027 年後段與 2028 年。","ruling":"可調和。方向採管理層，節奏採保守，所以 Base 的 FY27 低於共識 5.5%。","evidence_level":"法說原文推導","settle_metric":"2027 Q1、Q2 非 GAAP 毛利率","if_then":["若 2027 Q2 毛利率不低於 43%，Base 上調至共識。","若連 2 季低於 42%，已持有者減碼一半。"],"evidence_refs":[]},{"axis":"2030 年 AI 資料中心目標","cause":null,"prior_field":null,"side_a":"管理層把 2030 年目標上調到 30 億美元以上。","side_b":"Hassane El-Khoury 答 Wells Fargo 時說上調的 5 億全來自收購。2026 基期已由 5 億升到 6.2 億，2027 年翻倍約 12.4 億，有機 25 億隱含 2027～2030 年化僅 26%；投資人日被 BofA 問是否保守時也未正面回答。","ruling":"不可裁決至 2028 年。可能是保守，也可能反映 800V 時程和競爭；Base 用 2030 年約 28 億美元。","evidence_level":"法說原文","settle_metric":"2027、2028 年 AI 資料中心營收","if_then":["若 2027 全年高於 14 億美元，Bull 機率上調到 25%。","若低於 10 億美元，停止加碼。"],"evidence_refs":["competitive_share_entrants#4","end_markets#1"]},{"axis":"自由現金流用途","cause":null,"prior_field":null,"side_a":"Thad Trent（2026-09-16 投資人日）：扣除其他投資後 100% 自由現金流回饋股東，模型不含 Synaptics。","side_b":"Thad Trent（2026-11-02）：Synaptics 完成後去槓桿是首要任務，回購伺機；Q3 回購僅 2,000 萬美元。","ruling":"不算改口，但獨立模型不是股東實際會拿到的結果，應以併購後框架為準。","evidence_level":"法說原文","settle_metric":"併購後季度回購金額與淨負債","if_then":[],"evidence_refs":["ma_merger#0"]},{"axis":"客戶集中度口徑","cause":null,"prior_field":null,"side_a":"投資人日：沒有 10% 客戶，前 20 大占 35%。","side_b":"10-K：一家經銷商占 FY25 營收約 11%。","ruling":"可調和，前者應為終端客戶口徑，後者為經銷商；本包沒有原文證實。","evidence_level":"公司文件","settle_metric":"下一份 10-K 客戶揭露","if_then":[],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY27 僅 13.4 倍，FCF 殖利率約 6.6%，Q3 與 Q4 指引優於季節性，FY1 共識三個月上修 2.5%，賣方均標高於現價 41%～79%，價格也低於前份設定的 70～85 美元。","side_b":"併購條款未讀到，股價低於 250 週均線 69.17 美元，車用暫時性尚未驗證；Ferric 與修訂協議都不到一季，是否進入賣方模型未知。","ruling":"觀望，唯一限制是併購財務條款。條款已在 2026-10-01 的 8-K，只是本包未收錄，補讀後可立刻裁決，不必等到完成日。","evidence_level":"事實表與資料缺口","settle_metric":"合併文件的現金股票比例與融資安排","if_then":["若股價先站回 69.17 美元但併購條款未確認，不追。","若條款達標且 Q4 毛利率不低於 42%，股價卻跌破 55 美元，分批反買到 1.5%，2027 Q1 車用確認後加到 3%。","反向條件：若淨負債高於近四季自由現金流 4 倍，已持有者減碼一半；若車用同時低於 7.4 億美元，清倉。"],"evidence_refs":["major_events#0","capital_markets_pricing#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：中國低價 SiC 與上游過剩；結構轉好：AI 電源需求，IDM 資本支出 2026 年再降 9%，TI 資本支出下降。","side_b":"其他結構變數：中國反傾銷調查未結，Section 232 關稅範圍狹窄，併購改變公司結構，經銷占比升到 54%。","ruling":"雙向拉鋸：矽功率與類比轉好，SiC 惡化，中國政策未定。","evidence_level":"一手文件與產業媒體","settle_metric":"SiC 定價、AI 資料中心營收、反傾銷裁定","if_then":[],"evidence_refs":["cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#0","reg_tariff_export#2"]}],"triggers":[{"n":1,"text":"併購高槓桿完成","type":"Single Thing","maps_to":"R1","metric":"淨負債÷近四季自由現金流；新發股數÷流通股","threshold":"高於 4 倍，或新發股數高於 15%","action":"已持有者減碼一半，未持有者不進場","source_freq":"8-K、合併文件、10-Q，事件驅動","date":"2027-06","evidence_refs":["regulatory_antitrust#1"]},{"n":2,"text":"併購條款達標後才重跑研究","type":"估值rearm","maps_to":"R1","metric":"同上","threshold":"不高於 4 倍且低於 15%，或交易終止","action":"重跑完整研究，通過後首筆 1.5%","source_freq":"合併文件，事件驅動","date":"2026-12","evidence_refs":["major_events#0"]},{"n":3,"text":"車用暫時性驗證","type":"假設驗證","maps_to":"H3","metric":"車用季營收","threshold":"不低於 7.8 億美元為確認，低於 7.4 億美元為否證","action":"確認則加到 3%；否證則減碼一半","source_freq":"季報","date":"2027-05","evidence_refs":["end_markets#0"]},{"n":4,"text":"毛利率節奏驗證","type":"假設驗證","maps_to":"H2","metric":"非 GAAP 毛利率","threshold":"2027 Q2 不低於 43%","action":"未達則停止加碼","source_freq":"季報","date":"2027-08","evidence_refs":[]},{"n":5,"text":"AI 資料中心放量驗證","type":"假設驗證","maps_to":"H1","metric":"AI 資料中心營收","threshold":"2027 Q1 不低於 2.3 億美元，全年不低於 11 億美元","action":"未達則停止加碼","source_freq":"季報新分部","date":"2027-05","evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"中國政策吸收失敗","type":"風險","maps_to":"R3","metric":"反傾銷稅率與非 GAAP 毛利率季變化","threshold":"對 onsemi 課稅不低於 20% 且毛利率季減不低於 100 基點","action":"減碼三分之一","source_freq":"中國商務部公告、季報","date":null,"evidence_refs":["regulatory_antitrust#2","reg_tariff_export#0"]},{"n":7,"text":"循環反轉領先指標","type":"風險","maps_to":"R4","metric":"通路庫存週數；存貨與營收增速差","threshold":"高於 11 週，或存貨增速連 2 季高於營收增速","action":"停止加碼","source_freq":"法說，每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"n":8,"text":"SiC 與 PSG 走弱（前份保留，SiC 全年數字為資料缺口）","type":"風險","maps_to":"H3","metric":"SiC 營收年增率、PSG 季增率","threshold":"SiC 連 2 季年減且 PSG 季減","action":"減碼三分之一","source_freq":"季報與法說","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#3"]},{"n":9,"text":"影像感測走弱（前份保留，份額為資料缺口）","type":"風險","maps_to":"H3","metric":"ISG 季營收與車用影像份額","threshold":"連 2 季衰退且第三方資料顯示份額流失","action":"停止加碼","source_freq":"季報與產業報告","date":null,"evidence_refs":[]},{"n":10,"text":"多項核心假設同時失敗","type":"清倉","maps_to":"H2","metric":"併購槓桿、車用、毛利率、AI 營收","threshold":"槓桿超標且車用低於 7.4 億美元；或毛利率連 2 季低於 42% 且 AI 全年低於 10 億美元","action":"清倉","source_freq":"季報","date":"2027-08","evidence_refs":[]},{"n":11,"text":"SiC 證券集體訴訟","type":"風險","maps_to":"R5","metric":"訴訟程序與和解金額（金額事實表未涵蓋）","threshold":"集體認證通過且和解金高於一季 FCF，約 4.9 億美元","action":"減碼一半；若有刑事介入則清倉","source_freq":"10-Q 法律事項","date":null,"evidence_refs":["lawsuit_class_action#0","major_events#2"]},{"n":12,"text":"Q4 財報複審","type":"複審日期","maps_to":"H2","metric":"Q4 毛利率、2027 Q1 車用指引","threshold":"毛利率不低於 42%，車用指引回到 7.8 億美元附近","action":"未達則不進場","source_freq":"財報","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"車用季營收","bear_threshold":"低於 7.4 億美元","window":"2027 Q1 財報","source":"季報與法說","last_status":"warning"},{"metric":"非 GAAP 毛利率","bear_threshold":"連 2 季低於 42%","window":"2027 Q1 起","source":"季報","last_status":"ok"},{"metric":"AI 資料中心年營收","bear_threshold":"2027 全年低於 10 億美元","window":"FY2027","source":"季報新分部","last_status":"ok"},{"metric":"併購後淨負債÷近四季自由現金流","bear_threshold":"高於 4 倍","window":"合併文件至完成後首份財報","source":"8-K、合併文件、10-Q","last_status":"unknown"},{"metric":"新發股數÷現有流通股","bear_threshold":"高於 15%","window":"合併文件至完成日","source":"8-K、合併文件","last_status":"unknown"},{"metric":"通路庫存週數","bear_threshold":"高於 11 週","window":"每季","source":"法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#1","reason":"這是 2025-02 的新聞標題，只有地緣不確定一語，沒有地區、金額或業務別，也早於本輪復甦，指不到可監測的數字；地緣風險已有中國反傾銷與樂山廠兩項較具體的證據。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"不高於 3%，循環股且併購未決","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-38.65, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='早循環', moat='C', moat_trend='→', cycle_gates_pass=None","input_gap":["cycle_gates_pass"]},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"Synaptics 合併文件顯示完成後淨負債不高於近四季自由現金流 4 倍且新發股數低於流通股 15%，或交易終止；達成後重跑研究","exec_line":"未持有不建倉；條件達成後重跑完整研究，首筆 1.5%，2027 Q1 車用達標後加到上限 3%。"},"reasoning":{"industry":"Q3 營收 17.22 億美元：車用 7.77 億（45%）、工業 4.67 億（27%）、其他 2.99 億（17%）、AI 資料中心 1.80 億（10%）；事業群為 PSG 8.90 億、AMG 5.97 億、ISG 2.35 億。Q3 非 GAAP 營益率 23.2%，GAAP 22.0%。產業時鐘判在擴張早段：2026-08-03 法說稱訂單出貨比明顯高於 1、交期拉長，漲價開始少量進損益；onsemi 自身稼動率 83%，仍低於 92%～93% 的滿載線，FY26 共識營收 66.1 億美元也低於 FY22 的 83.3 億。供需判為週期性偏緊、將會反轉：緊在部分矽製程產線與 AI 排擠，SiC 上游反而過剩。單點依賴：2026-09-16 投資人日 Thad Trent 稱沒有 10% 客戶、前 20 大占 35%；10-K 另揭露一家經銷商占 FY25 營收約 11%，經銷通路占 54%。分部毛利率事實表未涵蓋。","moat":"機制是車規認證與長生命週期設計案，加上低壓到高壓的完整電源產品線，AI 資料中心再加系統級方案。ROIC 差距因投入資本缺資料算不出，改用同業利潤率差距。TTM GAAP 毛利率 38.68%，比 TXN 低 21.6 個百分點、比 NXPI 低 17.8、比 MCHP 低 21.5、比 STM 高 4.8；營益率 19.12%，低於 TXN 的 41.12% 與 NXPI 的 28.55%，高於 MCHP 與 STM；FCF 率 25.38%，僅低於 TXN。SiC 份額 55%～60% 是公司自述，沒有第三方驗證。可能看錯的地方：若車用讓路實際造成份額流失，方向應改為 ↓。","growth":"成長來源：2027 年以量為主，價格只抵銷成本，併購外加，回購暫停。共識營收 FY26 到 FY27 增 14.9%（66.07 億到 75.94 億美元，28 位分析師）；共識 EPS FY26 到 FY28 年化 36.1%（3.28 到 6.08）。以 FY25 GAAP 0.29 為基期的三年 CAGR 約 176%，基期含減損，沒有參考價值。管理層 2027 年框架（AI 翻倍約增 6.2 億、車用 9%、工業 10%，後兩項以 Q3 年化估）合計約增 10.9 億，略高於共識的 9.9 億，所以營收不是爭點，毛利率才是。FY27 共識隱含毛利率約 44.5%～45%（4.71×3.92 億股÷0.85，扣其他收益約 1 億，營業費用假設 13.0～13.4 億）；Q4 指引中點 42.5%，且 Q3、Q4 稼動率都是 83%，按落後兩季計 2027 上半年沒有稼動率推升。因此 Base 的 FY27、FY28 EPS 為 4.45、5.55，各低於共識 5.5%、8.7%。反例：若新品組合與漲價提前進損益，共識就站得住。","governance":"Q3 自由現金流 4.886 億美元，占營收 28%，對 GAAP 淨利 3.14 億的轉換率 1.56 倍；TTM FCF 率 25.38%。Q3 資本支出只占營收 1.6%，2027 年回到約 5%，同樣條件下 FCF 率約少 3.4 個百分點。淨負債 3.4 億美元，Ferric 付現 6 億後約 9.4 億；若 Synaptics 約 70 億全數現金，淨負債約 79 億，是近四季 FCF 約 16 億的 4.9 倍，修訂條款事實表未涵蓋。SBC 約占營收 2.2%。近三年現金去向四分與債務到期結構事實表未涵蓋。","valuation":"以 16 倍反推，現價 63.31 只要求 FY27 EPS 約 3.96 美元，比共識 4.71 低 16%。Q3、Q4 指引都高於季節性，即使 FY27 毛利率只到 43%，EPS 仍約 4.4 美元。不確定的是分母：賣方是否納入 Synaptics 事實表未涵蓋，公司長期模型明確不含。各倍數分歧：Trailing P/E 37.02 倍（分母含減損費用）、FY1 19.3 倍、FY2 13.4 倍；P/S 3.87 倍與 EV/S 3.92 倍位於四個年度端點的 69 與 65 百分位。賣方均標 89～113 美元，比現價高 41%～79%，但三個來源日期不一且早於 11-02 財報，只作對照。真正的五年分位事實表未涵蓋，留空。","premortem":"以 FY31 Base EPS 7.80 計，毛利率每 100 基點約 0.24 美元（110 億美元×1%×0.85÷3.92 億股），對應終端價約 3.8 美元；新債每 10 億美元按假設利率 6% 約減 0.13 美元；若高槓桿使終端倍數由 16 倍降到 12 倍，終端價少約 31 美元。股價低於 52、104、250 週均線，RSI 34.16，26 週跌 38.65%；下跌原因事實表沒有拆解，時間上與 6 月 25 日簽約重疊，但沒有事件日股價，不能歸因。循環位置判早循環：訂單出貨比大於 1、通路庫存 9.9 週且下降、情緒悲觀偏向買，倍數訊號分歧，AI 資本支出位置事實表未直接涵蓋。P/B 事實表未涵蓋，反動能五項檢查無法全數確認。AI 資料中心屬結構成長，不隨循環賣。管理層有四題未正面回答：AI 營收拆分、與對手比較稼動率、2027 投入成本與定價幅度、AI 目標是否保守。"},"plain":{"six":{"how_it_makes_money":"賺汽車、工業和 AI 資料中心的電源與感測零件錢，利潤卡在稼動率和產品組合：Q3 非 GAAP 毛利率 41.2%，離 53% 目標還有 11.8 個百分點。","moat":"護城河方向穩定：AI 電源在擴大，SiC 定價在縮減，毛利率仍比類比同業低約 20 個百分點。","growth":"五年後仍有成長空間：AI 電源是第二條曲線，SiC 滲透率約 17%；但共識成長主要靠毛利率回升，不是靠再投資。","capital":"現金創造強，但資金用途正從回購轉向舉債併購，資本配置成績要等 Synaptics 與 Ferric 的實際報酬。","valuation":"現價只要求 FY27 EPS 約 3.96 美元配 16 倍，我相信營運面做得到，但併購後的每股分母還不能確認，便宜的說法暫時不成立。","how_wrong":"最可能看錯的不是營運，而是併購把資本結構改掉；其次是車用暫時下滑的說法與循環反轉。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等事件不等價位：先讀 2026-10-01 修訂合併協議的現金股票比例與融資安排（本包未收錄），確認完成後淨負債不高於近四季自由現金流 4 倍、新發股數低於流通股 15%；2027 Q1 車用營收達 7.8 億美元以上才補足倉位。","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":63.31,"week26_return_pct":-38.65,"consensus_rev_3m_pct":2.5,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"短期上檔＝FY27 Base EPS 4.45×17 倍，中期上檔＝FY28 Base EPS 5.55×16 倍。FY27 共識隱含毛利率約 44.5%～45%，高於 Q4 指引中點 42.5%；Synaptics 的舉債與發股也可能改變每股分母，修訂條款未收錄。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"Ferric 併購完成（6 億美元現金，另有最多 1.75 億美元業績獎金）","impact":"低","watch":"付現後現金與 2030 目標的有機拆分"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 Q1 指引","impact":"高","watch":"車用指引是否回到 7.8 億美元附近，毛利率是否達 42.5%"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"2027 Q1 財報","impact":"高","watch":"車用營收、AI 資料中心營收與上半年毛利率節奏"},{"date":"2027-Q2","date_precision":"quarter","type":"regulatory","event":"Synaptics 併購預計年中完成，須通過中國市場監管審查","impact":"高","watch":"審批進度、融資條款與完成後淨負債"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"800V 資料中心機櫃開始放量","impact":"中","watch":"AI 資料中心季增率與垂直 GaN 營收"}],"_projected_from":"v19"}
```
