你是 stock-analyst v20 的**散文層（prose）agent**，標的 GLXY（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：GLXY　日期：2026-11-03　archetype：None　前份裁決：2026-05-25　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2187B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（501B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（904B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1274B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1160B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（719B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（887B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（3011B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3241B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2605B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2187           3369-4813      3 條（2–6 內）  
s3                  8000         501           5249-7499      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3338          8163-11662      5 條（2–6 內）  
s6                 11000         719          7197-10281      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         887           1829-2613      5 條（2–6 內）  
s10                 5000        3011           1392-1989      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2605           2000-2395      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4819B；至少需散文≈40.18KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−332%
−86%
−85
−85%
−72%
−55
−55%
−54%
−48.13
−47.2%
−28.5%
−15.1
−7.4%
−2.64
−2.41
−0.61
−0.51
−0.50
−0.45%
−0.28%
−0.11
−0.10
−0.07
0
0.13
0.27
0.374
0.414
0.5
0.51
0.517
0.7%
0.75
0.83
0.94
1%
1
1.2
1.25
1.5
1.6
1.96
2
2%
2.1
2.29
2.3
2.4
2.6
2.8%
3%
3
03
3.23
3.47
04
4
4.09
4.16
4.19
4.3
4.45
4.48
4.55
4.99
5
05
5%
5.2%
5.69
5.75
06
6
6.5
6.6
7
7%
7.57
8
08
8.5
9
09
9%
9.875%
10%
10
11%
11
12
12%
12.5
12.6
13
13.9
14
15
15%
15.14
16
16.2
16.9
17
18
19
19.5
20%
20
20.5
21
23
24
25
25%
26
27
27%
28.65
28.8
29%
29
30
30%
31
35
35.07
35.2%
37
37%
40%
41
42
46%
47%
47.2%
47.36
48%
48
49
50
50%
52
53
53%
57
58%
60
60%
63.8
64
68
68%
70
71%
75%
80%
80
80.6
85%
86%
86.9
89
90
90%
100%
100
104
133
137
145
150%
179
190
200
224
260
300
400
518
575
600
650
800
830
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
14500
17900
22400
44000
45000
46000
50000
51771.63
58900
61800
64000
64900
68100
71500
72000
80000
88000
96000
20261103
1,590
1,606
1,900
2,000
2,500
5,300
6,000
6,400
6,7
6,900
7,100
7,500
7,900
8,000
−4,200
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
{"meta":{"ticker":"GLXY","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Galaxy Digital Inc."},"oneliner":"Helios 資料中心已開始向 CoreWeave 收租，但價值押在非投資等級的單一承租方與尚未簽約的 Helios II；高槓桿建置下現價大致反映基本情境，等租約與信用事件落地再談","thesis":{"H":[{"id":"H1","text":"Helios I（租給 CoreWeave、約 800MW）依時程交付並如期收租，資料中心成為穩定現金流來源","2y":"2027 年底資料中心年化租賃收入 8–8.5 億美元（管理層 2026-10-27 指引），Phase II 首批資料廳 2027Q2 交付","5y":"Helios I 全部交付、CoreWeave 正常付租，資料中心分部調整後 EBITDA 年化 ≥ 12 億美元","10y":null,"threshold":"2027Q4 單季租賃收入 ≥ 2 億美元；分部調整後 EBITDA 對租賃收入 ≥ 80%（2026Q3 約 86%）","source":"季報資料中心分部揭露、8-K、法說會交付進度","drift_rule":"兩年論點：單季租賃收入或交付進度連 2 季落後指引 ≥5% 為削弱，連 3 季 ≥10% 為反轉"},{"id":"H2","text":"Helios II（約 830MW）在 2027 年底前租給投資等級承租方或有效信用增強的對象，條件不差於 Phase II","2y":"2027-12-31 前公告租約，每 MW 年租金不低於約 190 萬美元（由 2027 年底 8–8.5 億年化指引扣除 Phase I 每季約 8,000 萬推算）","5y":"2031 年前至少一半容量通電收租，且不需發行普通股融資","10y":null,"threshold":"簽約日 ≤ 2027-12-31；承租方或信用增強為投資等級；每 MW 年租金 ≥ 約 190 萬美元","source":"8-K、法說會","drift_rule":"2027-06-30 前無簽約公告為削弱；2027-12-31 前仍無簽約為反轉"},{"id":"H3","text":"數位資產業務在加密量能低迷下仍取得市占，並把收入往經常性收費（資管、質押、基礎設施）移動，2027 年起穩定獲利","2y":"2027 年數位資產分部調整後 EBITDA 至少連 2 季為正；資管與基礎設施單季調整後毛利 ≥ 2,500 萬美元（2026Q3 為 1,900 萬）","5y":"經常性收費占數位資產調整後毛利 ≥ 40%（2026Q3 約 27%）","10y":null,"threshold":"分部 EBITDA 連 2 季 > 0；交易量季增幅不低於產業","source":"季報分部揭露、法說會交易量對產業比較","drift_rule":"兩年論點：連 2 季分部 EBITDA 為負且交易量落後產業為削弱，連 3 季為反轉"}],"R":[{"id":"R1","text":"CoreWeave 信用惡化：重組、延遲付租或要求重談租約","h_ref":"H1","clock":"⚡","threshold":"CoreWeave 公告重組或破產保護、Galaxy 揭露租金延遲或租約條件變更，任一發生","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R2","text":"德州法規與電力分配：12 月稽核、2027 年 4 月 Batch Zero 分配不利，Helios II 承租方遲遲不簽","h_ref":"H2","clock":"🔥","threshold":"稽核點名 Helios II 需重新審查，或 2027-04 分配未給 Caspian、Selene、Helios III 任何基載容量","evidence_refs":[]},{"id":"R3","text":"建置與融資成本上升：關稅、長交期設備、設備過時；Phase III 與 Helios II 融資利率高於 Phase II 的 9.875%","h_ref":"H1","clock":"🔥","threshold":"Phase III 債務票息 ≥ 10% 或貸款成數 < 75%；Phase II 預算超支 ≥ 10% 或首批交付晚於 2027Q3","evidence_refs":["reg_tariff_export#0","substitute_technology#1"]},{"id":"R4","text":"資管與質押費率壓縮、代幣化被大型傳統金融機構自建吃掉","h_ref":"H3","clock":"🐢","threshold":"資管與基礎設施調整後毛利對管理加質押資產比率連 4 季下滑，或 BNY 等合作 2028 年前仍無收入揭露","evidence_refs":["competitive_share_entrants#0"]},{"id":"R5","text":"LUNA 相關法律責任：安大略集體訴訟獲認證、和解超過已計提數；紐約州檢察長和解 2 億美元分期至 2028 年","h_ref":"H3","clock":"🔥","threshold":"集體訴訟獲認證且和解或判決金額 > 1 億美元，或新增監管和解","evidence_refs":["major_events#0","lawsuit_class_action#0","major_events#1","regulatory_antitrust#0"]},{"id":"R6","text":"AI 資本支出結構性退潮（沿用前份風險三）","h_ref":"H2","clock":"🐢","threshold":"超大型雲端業者資本支出指引連 4 季累計下修 ≥ 15%（來源為各業者財報，事實表未涵蓋）","evidence_refs":[]}],"single_thing":{"description":"CoreWeave 發生信用事件（重組、破產保護或付租違約），導致 Helios I 租約被拒絕或重談降租","why_fatal":"Helios I 是目前唯一有租約的資料中心資產，2026Q3 資料中心調整後毛利 7,900 萬美元全來自 CoreWeave，占營運業務調整後毛利約一半；Phase II 以 85% 貸款成本比、9.875% 擔保債舉債，股權只占約 15%，租金打 25% 折扣就可能抹平資料中心股權，是數學上最大的單一敏感項","if_happens":"清倉；待租約處置結果與替代承租方確定後重跑研究","how_monitor":"CoreWeave 季報現金與融資可得性、債券利差與評等；Galaxy 季報資料中心單季租賃收入是否維持約 8,000 萬美元以上","probability":"12–24 個月約 10%：市場已因 CoreWeave 債務疑慮兩週打掉股價約 30%；但 Helios I 目前負載來自投資等級超大型雲端客戶、德州電力稀缺，破產時租約較可能被承接而非拒絕"}},"appendix_a":{"growth_durability":5,"quality_score":4,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-0.61,"FY2026E":-0.07,"FY2027E":-0.11,"FY2028E":0.94},"fy_end_month":12,"eps_basis":"FY2025 為年度財報稀釋 EPS；FY2026–2028 為 Koyfin 共識（2026-10-31 快照），口徑未註明是否調整後；Q3 調整後 EPS 0.83 美元公布後 FY1 共識仍為 −0.07，可能未完全更新"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLXY_20261103/scenario.json","archetype":{"primary":"金融","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"券商／交易商＋資產管理，疊加以專案債興建、單一承租方的長約資料中心；估值以分部加總為主，不用本益比"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久（供給端）：管理層稱 2028–2030 年可交付電力受限、新併網核准變難，Helios I/II 逾 1.6GW 在批次審查前已核准；但需求集中在超大型雲端、AI 實驗室與 CoreWeave 這類新雲業者，融資收緊時需求可逆（2026-10-27 法說會，Ferraro）","bargaining":{"up":"長交期電力設備供應商：已為 Helios II 預付約 2.3 億美元訂金與採購單；10-K 自述設備可能受關稅影響","down":"Helios I 全部容量租給 CoreWeave（非投資等級），占營運業務調整後毛利約 53%；Galaxy 對 CoreWeave 把哪個終端客戶放進 Helios 沒有控制權，CoreWeave 對客戶合約平均約 5 年，短於 15 年租約","geo":"資料中心全在德州：州長 9 月指令後部分許可暫停；ERCOT 把 Caspian 由基載改列研究負載且申訴被駁回"},"profit_pool_dir":"已核准電力與併網土地分到的利潤池在擴大（稀缺），但 Galaxy 以 9.875% 舉債興建、收益率約 10–11%，多數經濟利益流向承租方與債權人","tam_table":{"expanded":false,"reason":"事實表只有管理層自述美國至 2030 年 80GW 以上供給缺口，沒有獨立的市場規模、滲透率與利潤池資料；論點靠已核准電力的稀缺與承租方信用，不靠滲透率，展開只會堆單一來源數字"}},"moat":{"mechanism":"批次審查前已核准的德州電力（Helios I/II 逾 1.6GW）＋15 年期租約；數位資產端靠資本與機構關係","execution":6,"pricing":5,"grade":"C","trend":"→","trend_evidence":"交易量連續優於產業屬執行面小幅擴大；Helios II 未能如管理層年初所說在夏季簽約、資管進入門檻低，定價面沒有擴大證據，兩者相抵，方向持平","peer_na_reason":"Galaxy 營收是數位資產買賣總額，毛利率與營業利益率近零是會計口徑造成，與 COIN、HOOD 的淨收入口徑不可比；IREN 為 2026-06 止的 TTM，期間也不同。改用交易量相對產業的份額軸","threats":[{"level":"🟡","text":"資管與質押：10-K 自述資管業進入門檻低、競爭者可能大量湧入，費率可能壓縮；Galaxy 資管與基礎設施單季調整後毛利僅 1,900 萬美元","p":"40%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"資料中心競爭者：傳統資料中心、雲端業者與轉型礦工爭奪同一批承租方；Galaxy 的差異只在已核准電力與一期交付紀錄","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"AI 需求與機房規格變化：10-K 自述難預測 AI 資料中心需求與競爭產品進入，設備過時需更換且零件取得可能受阻；機架密度或散熱規格快速改變時，已建資料廳要追加資本支出","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"資料中心屬高利益率×低周轉（分部調整後 EBITDA 率約 86%，年租金約為建置成本的 12%），要看再投資負擔；全公司因總額營收呈現低利益率×高周轉的假象；投入資本口徑事實表未涵蓋，當期 ROIC 無法計算","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是超大型雲端客戶的 AI 負載（Ferraro 稱 Helios I 目前負載來自數兆美元市值的投資等級客戶），決策者是 CoreWeave，付款者是 CoreWeave 母公司；需求端強，但付款環節是非投資等級信用，三角色中這一環偏弱"},{"item":"決策層級","level":"🟡","text":"15 年租約加上電力稀缺，承租方搬遷成本高；但 CoreWeave 對終端客戶合約平均約 5 年，終端負載會換手；數位資產端交易與質押委託轉換成本低，ETF 發行商可隨時改委託"},{"item":"價值鏈分配","level":"🟡","text":"已核准電力是 2028–2030 年的稀缺環節，但 Phase II 推算未槓桿收益率約 10–11%、債息 9.875%，開發商目前只拿到薄利，經濟利益多流向承租方與債權人；Phase II 成本含共用變電站，可能高估每 MW 成本，待 Helios II 租約條件驗證"},{"item":"社會容忍度","level":"🟡","text":"德州政治對資料中心用電敏感：州長 9 月指令後部分許可暫停、Caspian 被改列研究負載；Helios I/II 在批次審查前已核准，管理層稱不受影響，但擴建管線 2.6GW 曝險；加密端 CLARITY 法案未成為法律"}],"roiic":"約 10–11%（Phase II：年化 EBITDA 約 4.3 億 ÷ 總成本約 41 億美元）","reinvest_rate":"遠超 100%：2026 年 Q2、Q3 資本支出合計約 12 億美元（4.48 億＋7.57 億），同期全公司營運獲利近零，靠專案債與現金支應","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；再投資率超過 100% 且以 9.875% 債務支應時，公式不代表可自籌的成長上限，故不給數字；增量報酬只比債息高約 0.5–1 個百分點"},"combined":5.5,"score":5.5,"spread_table":[{"metric":"毛利率","GLXY":-0.45,"COIN":71.01,"HOOD":81.44,"IREN":62.32,"unit":"%"},{"metric":"營業利益率","GLXY":-0.28,"COIN":5.68,"HOOD":45.65,"IREN":-53.57,"unit":"%"},{"metric":"FCF 利潤率","GLXY":-7.17,"COIN":68.4,"HOOD":58.44,"IREN":-332.45,"unit":"%"},{"metric":"研發密度","GLXY":null,"COIN":34.52,"HOOD":19.34,"IREN":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"COIN","gm":71.01,"om":5.68,"fcf_margin":68.4,"rd_intensity":34.52,"strategy_note":"零售與機構交易所加託管，毛利率 71%、FCF 利潤率 68%；與 Galaxy 在機構交易與託管重疊，但收入口徑不同，利潤率不能直接比","period":"TTM ending 2026-09-30（4季加總）"},{"name":"HOOD","gm":81.44,"om":45.65,"fcf_margin":58.44,"rd_intensity":19.34,"strategy_note":"零售券商擴張到加密，營業利益率 46%；與 GalaxyOne 零售通路正面競爭，GalaxyOne 平台資產約 1.25 億美元，規模懸殊","period":"TTM ending 2026-09-30（4季加總）"},{"name":"IREN","gm":62.32,"om":-53.57,"fcf_margin":-332.45,"rd_intensity":null,"strategy_note":"前礦工轉型 AI 資料中心，營業利益率 −54%、FCF 利潤率 −332%，與 Helios 同在重資本建置期，說明這個賽道還沒證明能穩定賺錢","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（資料中心 MW 交付），數位資產端隨加密價格與交易量波動；無併購，回購小","runway_years":"約 5 年（已核准 1.6GW 約在 2030–2031 年建完，之後取決於 2027-04 電力分配）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段增量報酬率約 10–11%；再投資率超過 100% 由債務支應，內生上限不適用；共識 EPS 基期為負，成長缺口無法歸因，依賴資料中心收入兌現與估值重評","segments":[{"item":"資料中心","value":"2026Q3 調整後毛利 7,900 萬美元（Q2 2,000 萬）、分部調整後 EBITDA 6,900 萬；已交付 133MW；管理層預估 2027 年底年化租賃收入 8–8.5 億美元"},{"item":"數位資產","value":"2026Q3 調整後毛利 7,100 萬美元（Global Markets 5,300 萬、資管與基礎設施 1,900 萬），分部 EBITDA 仍為負；平均放款 18 億美元、管理加質押資產 104 億美元"},{"item":"財務與公司","value":"2026Q3 調整後毛利 4.19 億美元（Q2 為 −4,200 萬），來自持倉與私募投資增值，不可重複；季末淨數位資產與投資約 17 億美元"}],"decay_signals":[{"signal":"毛利率連 2 季同比下滑","lit":false,"note":"總額營收口徑毛利率無意義，調整後毛利無同比資料"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"Q1 交易量持平對產業大跌、Q3 +12% 對產業持平"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"不適用"},{"signal":"EPS 成長顯著高於營收成長","lit":false,"note":"EPS 基期為負無法計算"},{"signal":"FCF/NI 低於 0.75 連 2 年","lit":true,"note":"2023、2024 年淨利為正但自由現金流為負，2025 年自由現金流 −15.1 億美元"},{"signal":"SBC/營收高於 5% 且上升","lit":false,"note":"Q3 SBC 約占調整後毛利 2.8%"},{"signal":"TAM 萎縮或被替代","lit":false,"note":"AI 電力需求上升；加密量能低迷屬週期"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"只有 3 個年度端點，無法判斷"},{"signal":"維修性資本支出占 FCF 高於 60%","lit":false,"note":"FCF 為負，不適用"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"仍在擴產"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，資本去向以資料中心建置為主；回購年初至今約 2 億美元、約占市值 2%，不承重"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"無重大併購；2026 年購入三處德州站點屬資產購置、以里程碑付款，尚無已實現報酬可算","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"年初至今回購約 2 億美元，回購期間 FY1 共識 EPS 為負，買入時盈餘殖利率為負，低於 10 年期公債殖利率加 2 個百分點","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 1,606 萬美元，年化約 6,400 萬、約占市值 0.7%；管理層稱回購已超過抵銷，年初至今流通股淨減少","grade":"過"}]},"valuation":{"basis":"分部加總：資料中心 EV/EBITDA＋數位資產業務＋投資部位－淨負債；情境樹因虧損改用總額營收 EV/S 換算","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率、沒有同業估值倍數；本公司營收為數位資產買賣總額，與同業營收口徑不可比，倍數對照會失真"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"分部加總：基本情境每股約 19.5 美元，較現價高約 29%，五年年化約 5%；資料中心給 10 倍約 11 美元。現價介於 10–12.5 倍之間，判為合理。12 個月：Helios II 簽約機率約 40%、簽約後約 21 美元，未簽約約 13 美元，加權約 16.2 美元，較現價高約 7%。上市未滿五年、只有 3 個年度端點，五年分位不適用；P/S 與 EV/S 在端點內居最高，但分母為總額營收，不採用","upside_short_pct":7,"upside_mid_pct":28.8},"trap_analysis":{"verdict":"🟡","label":"資本密集擴張、自由現金流連年為負；便宜與否取決於資料中心倍數與承租方信用"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Helios I 133MW 全租給 CoreWeave（15 年租約），10 月因 CoreWeave 債務疑慮股價兩週跌約 30%；Phase II 以 85% 貸款成本比、9.875% 擔保債融資","assumption":"CoreWeave 在 2031 年前不重組、不降租，Helios I 租金如期入帳","consequence":"5 年後虧 50% 以上最可能的故事：CoreWeave 在 AI 融資收緊中重組，Helios 租約被拒絕或降租，Helios II 同時沒租出去，專案債吃掉資料中心股權，只剩數位資產業務與投資部位，每股 4 美元以下","ruling":"採納：與唯一致命點相同，機率約 10%；空頭情境給 30%，未來回撤下限放到 −85%","watch":"CoreWeave 季報現金與融資、債券利差；Galaxy 資料中心單季租賃收入是否維持約 8,000 萬美元以上","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"],"fact_refs":["f_kpi6_data_centers_adjusted_gr","f_kpi7_data_centers_critical_it"]},{"view":"論點成功但股東經濟變差","evidence":"Phase II 推算未槓桿收益率約 10–11%，債息 9.875%；2026-05 簽 5 億美元 ATM；Helios II 約 830MW 若比照 Phase II 每 MW 約 1,590 萬美元，需再投入逾百億美元；35.07 億美元票據 2031 年到期","assumption":"資料中心收入成長會等比例變成每股價值","consequence":"Helios 全部建成、租金都收到，但增量報酬只比資金成本高約 0.5–1 個百分點，加上增資與 2031 年再融資，每股價值成長遠慢於 EBITDA；基本情境資料中心 EBITDA 成長約 7 倍，每股價值只增約 29%","ruling":"採納：基本情境淨負債 179 億美元、股數 6 億股已反映；這是不建倉的主因之一","watch":"Phase III 債務票息與貸款成數、ATM 實際使用量、每股帳面淨值","evidence_refs":["major_events#3"],"fact_refs":["f_net_debt_m","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"市值約 89 億美元，約為帳面權益 30 億美元的 3 倍；2025 年淨利 −2.41 億美元；賣方目標價多在 7 月、CoreWeave 疑慮之前訂定","assumption":"市場仍在用 Helios II 順利簽約、資料中心約 12 倍 EBITDA 定價","consequence":"若市場改用接近高收益債利率的 10 倍對資料中心定價，基本情境每股約 11 美元，比現價低約 27%","ruling":"部分採納：股價已跌 48%，但跌幅不是安全邊際；現價只落在合理區、沒有折價，所以不建倉，但也不到放空的程度","watch":"Helios II 租約條件、Phase III 融資利率、CoreWeave 債券利差","evidence_refs":[],"fact_refs":["f_ev_m","f_week26_return_pct"]}],"max_dd":{"lo":-85,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 28.65 → 本次 15.14（-47.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=28.65","side_b":"本次 price_at_dd=15.14","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 28.65 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 28.65 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 28.65 美元：Bull 價 47.36、Bear 價 4.16，五年期望值 −28.5%，基準年化 −7.4%，不對稱比 0.51","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.51。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 28.65 美元：五年期望值 −28.5%，基準年化 −7.4%，不對稱比 0.51","side_b":"本次情境、股價 15.14 美元：五年期望值 +35.2%，基準年化 5.2%，不對稱比 1.96","ruling":"再換股價、情境不動：起點價下跌 47.2%，五年期望值多 63.8 個百分點，基準年化多 12.6 個百分點，不對稱比由 0.51 升到 1.96。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層承諾與兌現（一致）","cause":null,"prior_field":null,"side_a":"Q2 法說會（2026-08-05，Paquette）：Q3 是 Phase I 第一個完整季，租賃收入約 8,000 萬美元、專案層級調整後 EBITDA 率高於 90%；完成 CoreWeave 專案不需再募股權","side_b":"Q3 法說會（2026-10-27）：每季約 8,000 萬美元租賃收入、資料中心調整後毛利 7,900 萬、分部調整後 EBITDA 6,900 萬（分部層級含管銷，約 86%）；Ferraro 重申 Phase III 股權資金已備妥、只待 2027 上半年舉債","ruling":"一致：資料中心執行面承諾有兌現，執行分數據此給 6 分","evidence_level":"新聞稿＋前後兩季逐字稿","settle_metric":"2027Q2 Phase II 首批資料廳交付","if_then":["若 Phase II 首批交付晚於 2027Q3 → 停止加碼，執行分降一級"],"evidence_refs":[]},{"axis":"Helios II 為何沒簽（不可調和）","cause":null,"prior_field":null,"side_a":"管理層（2026-10-27，Novogratz、Ferraro）：夏季談到可簽的條件，但市場轉向、2028 年後電力更稀缺、超大型雲端開始搶 2028 年電力，主動不簽，Helios II 更值錢","side_b":"Novogratz 年初曾說夏季可能達成協議，2 月曾提 12 個月內簽約（Compass Point 引述）；Q2 法說會被問租戶漏斗時沒給進度；同期融資市場收緊、德州許可暫停，部分承租方要等 12 月稽核與 2027 年 4 月分配才簽","ruling":"方向相反、目前無法裁決，至簽約公告前採較保守的一側：不給管理層說法溢價，基本情境假設 Helios II 延到 2027 下半年才簽、2031 年只交付約一半","evidence_level":"管理層自述對照前後說法","settle_metric":"Helios II 租約公告：承租方信用等級、每 MW 年租金、是否需發普通股","if_then":["若 2027-06-30 前與投資等級承租方簽約且每 MW 年租金不低於約 190 萬美元 → 重跑研究，小額首倉","若 2027-12-31 前仍未簽約 → 第二論點反轉，不建倉；已持有者減碼","反向：簽約對象非投資等級且無有效信用增強 → 視同未簽，不追"],"evidence_refs":[]},{"axis":"Q3 獲利品質","cause":null,"prior_field":null,"side_a":"第三方報導：Q3 調整後 EPS 0.83 美元，遠高於共識 0.13 美元；淨利 3.23 億美元","side_b":"新聞稿與法說會：調整後 EBITDA 4.55 億中營運業務只有約 6,000 萬，財務與公司部門 4.19 億來自持倉與私募投資增值；Citi 追問時數位資產分部 EBITDA 仍為負","ruling":"可調和，屬程度差異：本季超預期主要是一次性增值，不改變經常性獲利判斷；估值不使用本季 EPS","evidence_level":"新聞稿＋逐字稿","settle_metric":"營運業務合計調整後 EBITDA","if_then":["若 2026Q4 營運業務調整後 EBITDA ≥ 1 億美元且數位資產分部轉正 → 第三論點加分，仍不追","反向：營運業務 EBITDA 回到接近零 → 停止加碼"],"evidence_refs":[]},{"axis":"管理層一次性歸因","cause":null,"prior_field":null,"side_a":"Paquette：若非一次性會計調整，數位資產分部本季已獲利；Phase II 年均收入假設下調只是租賃會計認列的澄清，實質不變","side_b":"兩項說法本季都無法驗證；Q2 法說會被問 BNY 與 GalaxyOne 貢獻時只給敘事、沒給數字","ruling":"不採信也不否定，標記未證、監測：2026Q4 與 2027Q1 數位資產分部調整後 EBITDA 仍為負，則一次性說法證偽；Phase II 收入以首個完整季實際入帳數核對","evidence_level":"逐字稿","settle_metric":"數位資產分部調整後 EBITDA；Phase II 首個完整季租賃收入","if_then":["兩季仍為負 → 第三論點削弱，停止加碼","Phase II 首個完整季租賃收入低於 1.2 億美元 → 第一論點削弱，減碼"],"evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-05-25，股價 28.65 美元）：估值偏貴","side_b":"本次（股價 15.14 美元，26 週跌 48%）：估值合理、沒有足夠折價","ruling":"變動主因是股價下跌約 47%；同期新證據（Helios II 未簽、CoreWeave 疑慮、9.875% 融資成本）也讓價值下修，所以只由偏貴降到合理，沒有變便宜","evidence_level":"價格資料＋分部加總","settle_metric":"分部加總每股價值對現價","if_then":["股價跌破 11 美元（資料中心 10 倍價值）且 CoreWeave 未出事 → 分批反買前提成立，先重跑研究","股價回到 20 美元以上而 Helios II 仍未簽 → 不追"],"evidence_refs":[]},{"axis":"品質訊號與陷阱判斷","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：品質訊號 B、陷阱中度（以估值偏貴為主要依據）","side_b":"本次：品質訊號降為 C、陷阱維持中度，依據改為資本密集擴張、自由現金流連年為負、單一非投資等級承租方","ruling":"降級理由是新證據：10 月 CoreWeave 債務疑慮使股價兩週跌約 30%；Helios II 夏季交易沒有成交；Phase II 9.875% 融資成本揭露增量報酬只略高於資金成本；德州許可暫停、Caspian 被改列研究負載；前份 2026 年底交付 300MW 的門檻落空","evidence_level":"8-K、10-Q、逐字稿、新聞","settle_metric":"Helios II 租約與 CoreWeave 信用","if_then":["Helios II 與投資等級承租方簽約且 Phase III 融資票息低於 9% → 品質訊號回到 B，重跑研究","反向：CoreWeave 信用事件 → 清倉"],"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"新增評估欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份為舊格式：未產出定期定額裁決與角色、護城河方向、五年後跑道、公司分類、循環位置、未來回撤範圍與情境機率","side_b":"本次首次給值：護城河方向持平、五年後跑道中等、金融為主兼具轉機特性、中循環；虧損改用營收倍數情境樹，多頭 20%、空頭 30%，未來回撤 −55% 至 −85%","ruling":"屬方法變動，不代表基本面變化，不拿來與前份比較","evidence_level":"格式變更","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件","side_b":"Helios II 與投資等級承租方（或有效信用增強）簽約，且 CoreWeave 付租正常、無重組公告","ruling":"首倉與加碼改用事件條件而非價格：卡住的是 Helios II 租約與 CoreWeave 信用兩件事，價格再跌也替代不了；觸發後先重跑研究，首倉只用小額","evidence_level":"逐字稿＋新聞","settle_metric":"Helios II 租約公告","if_then":["條件成立 → 重跑研究後小額首倉","條件成立但股價已過 25 美元 → 不追，等回落"],"evidence_refs":[]},{"axis":"Single Thing 變更","cause":"新證據","prior_field":null,"side_a":"前份未設唯一致命點；前份風險一為 CoreWeave 財務問題，CoreWeave 現金與融資可得性連 2 季減少才警戒、正式重組公告才重評","side_b":"本次 Single Thing：CoreWeave 發生重組、破產保護或付租違約，導致 Helios I 租約被拒絕或降租；任一公告即清倉","ruling":"由新證據觸發：10-19 起市場因 CoreWeave 債務疑慮兩週內把股價打掉約 30%，且 Phase II 以 85% 貸款成本比舉債、股權層薄，承租方信用成為數學上最大的單一敏感項；動作由重評改為清倉","evidence_level":"10-Q＋新聞","settle_metric":"CoreWeave 信用事件","if_then":["CoreWeave 公告重組或付租延遲 → 清倉","反向：CoreWeave 完成大額股權融資或評等上調 → 移出唯一致命點，重跑研究"],"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"論點與停損門檻變更","cause":"新證據","prior_field":["thesis.H","thesis.R","kill_metrics"],"side_a":"前份：第一論點 2026 年底交付 ≥300MW、2028 上半年 800MW 全交付；第二論點交易年化收入 ≥5 億美元；第三論點 2028 年底前第二客戶 ≥300MW；資本支出超預算 20% 且里程碑延後才減碼；未設停損指標","side_b":"本次：第一論點改為 2027Q4 單季租賃收入 ≥2 億美元；第二論點改為 Helios II 2027 年底前與投資等級承租方簽約；第三論點改為數位資產分部 2027 年連 2 季 EBITDA 為正；建置融資票息 ≥10% 或超支 ≥10% 即減碼；新增五項停損指標，CoreWeave 信用事件即清倉","ruling":"改門檻是新證據驅動：截至 2026Q3 只交付 133MW、Phase II 2027Q2 才開始交付，前份 2026 年底 300MW 確定落空（依前份規則屬削弱）；交易業務單季調整後毛利 5,300 萬、年化約 2.1 億，遠低於前份 5 億門檻（前份未定義口徑，總額營收不可用）；Helios II 夏季未簽、融資成本 9.875%，第二客戶的時間壓力與融資成本都比前份假設高，門檻因此提前、收緊；前份 AI 資本支出退潮門檻沿用為風險六","evidence_level":"新聞稿、逐字稿、8-K","settle_metric":"各論點門檻","if_then":["任一停損指標觸發 → 減碼一半；CoreWeave 信用事件 → 清倉"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價 26 週跌 48%、RSI 37；Phase I 準時收租、Phase II 已全額融資且按預算施工；電力稀缺讓 Helios II 更搶手；現金、穩定幣與公債 49 億美元；賣方最低目標價 24 美元仍比現價高約 58%；回購已超過抵銷稀釋","side_b":"目標價多是 7 月、CoreWeave 疑慮之前的數字；扣掉建置所需淨負債後，現價大約已反映 Helios I 全額付租＋Helios II 部分交付、12 倍左右的資料中心倍數；剩下的上行要靠兩個還沒發生的事件；CoreWeave 利空出現不到一季，FY2 共識只下修約 10%，可能尚未完全進入賣方模型","ruling":"不採：跌幅不是安全邊際；在 2026Q4 財報這個首個確認數據點之前凍結建倉","evidence_level":"價格資料、賣方目標價彙整、逐字稿","settle_metric":"Helios II 租約、2026Q4 財報","if_then":["Helios II 投資等級租約公告 → 重跑研究、小額首倉","價格續漲而事件未到 → 不追"],"evidence_refs":["geo_supply_chain#1"]}],"triggers":[{"n":1,"text":"CoreWeave 發生重組、破產保護或付租違約","type":"Single Thing","maps_to":"R1","metric":"CoreWeave 信用事件","threshold":"任一公告","action":"清倉；待租約處置與替代承租方確定後重跑研究","source_freq":"事件驅動（8-K、新聞）","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":2,"text":"Helios II 與投資等級承租方簽約","type":"假設驗證","maps_to":"H2","metric":"Helios II 租約公告","threshold":"承租方或信用增強為投資等級、每 MW 年租金 ≥ 約 190 萬美元、無需發行普通股","action":"重跑研究，條件符合則小額首倉","source_freq":"事件驅動","date":"2027-12-31"},{"n":3,"text":"德州資料中心稽核結果","type":"風險","maps_to":"R2","metric":"稽核結果是否影響 Helios II","threshold":"Helios II 須重新審查或延後通電","action":"不建倉；已持有者減碼一半","source_freq":"一次性","date":"2026-12"},{"n":4,"text":"ERCOT Batch Zero 研究負載分配","type":"風險","maps_to":"R2","metric":"Caspian、Selene、Helios III 合計 2.6GW 分到的基載容量與通電時程","threshold":"零分配或通電延到 2030 年後","action":"五年後跑道下調為窄，停止加碼","source_freq":"一次性","date":"2027-04"},{"n":5,"text":"Phase II 首批資料廳交付","type":"假設驗證","maps_to":"H1","metric":"交付時點與預算","threshold":"晚於 2027Q3 或超支 ≥10%","action":"停止加碼；與第 3 條同時發生則減碼","source_freq":"每季","date":"2027-09-30"},{"n":6,"text":"數位資產分部是否轉正","type":"假設驗證","maps_to":"H3","metric":"數位資產分部調整後 EBITDA","threshold":"2026Q4 與 2027Q1 仍為負","action":"一次性會計說法證偽，第三論點削弱，停止加碼","source_freq":"每季","date":"2027-05"},{"n":7,"text":"Phase III 債務融資條件","type":"風險","maps_to":"R3","metric":"票息與貸款成數","threshold":"票息 ≥ 10% 或需發普通股補足","action":"減碼一半，重算基本情境淨負債","source_freq":"事件驅動","date":"2027-06-30","evidence_refs":["reg_tariff_export#0"]},{"n":8,"text":"重新進場條件","type":"估值rearm","maps_to":"H2","metric":"Helios II 租約＋CoreWeave 信用","threshold":"Helios II 與投資等級承租方簽約，且 CoreWeave 付租正常、無重組公告","action":"重跑研究後小額首倉，不追價","source_freq":"事件驅動","date":null},{"n":9,"text":"LUNA 安大略集體訴訟認證與和解（2026-06 聽證結果事實表未涵蓋）","type":"風險","maps_to":"R5","metric":"認證結果與和解金額","threshold":"獲認證且和解或判決金額 > 1 億美元","action":"減碼一半","source_freq":"事件驅動","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":10,"text":"下次複審：2026 年第四季財報","type":"複審日期","maps_to":null,"metric":"資料中心租賃收入、數位資產分部 EBITDA、Helios II 進度","threshold":"無","action":"重跑判斷","source_freq":"每季","date":"2027-Q1"}],"kill_metrics":[{"metric":"資料中心分部單季租賃收入（Helios I）","bear_threshold":"連 2 季低於 7,500 萬美元，或 CoreWeave 延遲付租","window":"每季","source":"Galaxy 季報分部揭露","last_status":"ok"},{"metric":"Helios II 租約簽署","bear_threshold":"2027-12-31 前未與投資等級（或有效信用增強）承租方簽約","window":"至 2027-12-31","source":"8-K、法說會","last_status":"warning"},{"metric":"數位資產分部調整後 EBITDA","bear_threshold":"2027 上半年仍連 2 季為負","window":"2026Q4–2027Q2","source":"季報分部揭露","last_status":"warning"},{"metric":"Phase III 債務融資條件","bear_threshold":"票息 ≥ 10% 或需發普通股補足","window":"2027 上半年","source":"8-K","last_status":"unknown"},{"metric":"現金、穩定幣與美國公債","bear_threshold":"扣除 12 月 4.45 億美元可交換債後低於 25 億美元","window":"每季","source":"季報、新聞稿","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6,7a","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":true,"basis":"valuation_dependent=True, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟡', moat_trend='→', week26=-48.13, valuation_dependent=True"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6', '7a']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"Helios II 與投資等級承租方（或有效信用增強）簽約，且 CoreWeave 付租正常、無重組公告","exec_line":"條件成立後先重跑研究，首倉不超過總資產 1%，不追價；在此之前不建倉；已持有者遇 CoreWeave 信用事件即清倉"},"reasoning":{"industry":"2026Q3 新聞稿：GAAP 營收 80.6 億美元是數位資產買賣總額，TTM 毛利率 −0.45%、營業利益率 −0.28%，不能拿來看獲利；第三方報導寫 86.9 億，與新聞稿不符，以新聞稿為準。改看調整後毛利 5.69 億美元：資料中心 7,900 萬、數位資產 7,100 萬（Global Markets 5,300 萬、資管與基礎設施 1,900 萬）、財務與公司部門 4.19 億（持倉與私募投資增值，含 Etched、Forward Industries）。調整後 EBITDA 4.55 億中營運業務只有約 6,000 萬，淨利 3.23 億與 GAAP 營業利益 4.09 億主要靠一次性增值。可重複的錢是資料中心租金與數位資產業務，合計約 1.5 億／季。單點依賴：資料中心 133MW 全租給 CoreWeave，占營運業務調整後毛利約 53%（7,900 萬 ÷ 約 1.5 億）；Galaxy 面對的是 CoreWeave 母公司整體信用，看不到終端客戶合約（Ferraro，2026-10-27）。產業時鐘以資料中心為主：需求大於可交付電力，屬擴張期，但融資端已轉嚴（Phase II 以 9.875% 擔保債融資、市場出現 CoreWeave 債務疑慮）。供需持久性：供給約束偏結構性，需求集中在少數超大型雲端、AI 實驗室與新雲業者，融資收緊時可逆。","moat":"機制：一是 Helios I/II 逾 1.6GW 在德州批次審查前已核准，管理層稱 2028–2030 年可交付電力受限，屬稀缺資產；二是數位資產端以資產負債表、牌照與機構關係（BNY、摩根士丹利財富管理、貝萊德質押基金）取得委託。執行面 6 分：Q2 法說會說 Q3 是 Phase I 第一個完整季、租賃收入約 8,000 萬美元，Q3 如數做到；Phase II 已全額融資、按時程與預算施工；交易量 Q1 持平對產業大跌、Q3 +12% 對產業持平，份額小幅提升；但前份預期 2026 年底交付 300MW 落空，Helios II 原本夏季可能簽約也沒簽。定價面 5 分：Helios II 不簽的理由是條件可以更好，尚未被成交驗證；Phase II 推算收益率只略高於 9.875% 債息，看不到開發商議價優勢；10-K 自述資管業進入門檻低、費率可能壓縮。同業報酬率差距算不出來，改用交易份額軸，方向持平。","growth":"成長主要靠量：資料中心交付 MW（Phase I 133MW 已收租，Phase II 260MW 2027Q2 起交付，管理層預估 2027 年底年化租賃收入 8–8.5 億美元），數位資產端跟著加密價格與交易量起伏；無併購，回購規模小。共識 EPS 由 FY2025 −0.61 美元到 FY2028 0.94 美元，基期為負，算不出三年 CAGR；內生上限因再投資率超過 100% 而不適用，成長缺口無法歸因，等於依賴資料中心收入兌現與估值重評，信心上限為中。跑道：Helios I 約 800MW 預計 2028 年建完，Helios II 約 830MW 2028 年起通電，順利的話約 2030–2031 年用完已核准電力；之後看 Caspian、Selene、Helios III 合計 2.6GW 研究負載能否分到電（Caspian 申請基載被駁回）。代幣化：Novogratz 說還沒看到整體移轉，BNY 合作 12 個月內不會主導收入。衰退信號亮 1 個（自由現金流連年低於淨利），長期成長性與陷阱風險都屬中度。","governance":"自由現金流對淨利：2023 年 −0.50 億對 2.29 億、2024 年 −2.64 億對 3.47 億、2025 年 −15.1 億對 −2.41 億，三年都轉換不了，主因是資料中心資本支出（2026 年 Q2 4.48 億、Q3 7.57 億，2027 上半年更高）。SBC：Q3 1,606 萬美元，占調整後毛利約 2.8%，年化約占市值 0.7%。現金去向：一是資料中心建置（Phase II 已全額融資，35.07 億美元 9.875% 擔保債 2031 年到期）；二是回購，年初至今約 2 億美元，10 月用完首期授權，再加 2 億；三是償債，12 月到期 4.45 億可交換債，管理層稱以現金償還；四是放款，平均餘額 18 億美元、季增約 25%。另 5 月簽 5 億美元 ATM，使用量未揭露。季末現金、穩定幣與公債 49 億美元，帳面權益約 30 億，資料中心分部資產 68 億、負債 53 億。","valuation":"市場現價要求的是 Helios I 800MW 全數建成、CoreWeave 付滿租約，資料中心拿到約 12 倍 EBITDA。推導：市值約 89 億美元、目前淨負債 48 億、EV 137 億；把 Phase II 餘款、Phase III 與 Helios II 一半容量的建置成本加上後，2031 年淨負債約 179 億，資料中心 EBITDA 約 20.5 億，加數位資產業務 23 億、投資部位 17 億，12.5 倍時每股約 19.5 美元、10 倍時約 11 美元，現價 15.14 美元落在兩者之間。我信 Helios I 會建成，但不信市場會在 Helios II 簽約前給到 14 倍以上，所以是合理、不便宜。金融業尺：市值約為帳面權益（約 30 億美元）的 3 倍、2025 年淨利為負，以帳面報酬率看偏貴；但 Helios 以成本入帳，這把尺低估資料中心，只作參考。賣方目標價 24–57 美元（最高最低比 2.4 倍）多在 7 月、CoreWeave 疑慮之前，不採為錨。共識修正：FY1 近三月顯示 −86%，實際是虧損由 −0.51 縮小到 −0.07 美元，方向是上修；FY2 由 −0.10 到 −0.11 小幅下修。","premortem":"反證集中三處，詳見反證紀錄：CoreWeave 信用、Helios II 條件、增量報酬貼近資金成本。壓力測試 5 項過 3 項：加密寒冬（數位資產業務大致自籌資金、流動性 49 億美元）、德州法規擴大（Helios I/II 已核准）、Helios II 延到 2029 年（現金足以償還 12 月 4.45 億可交換債）撐得住；CoreWeave 違約與融資利率再升兩項撐不住。股價 26 週跌 48%、RSI 37，低於 52 週均線約 37%，沒有過熱。"},"plain":{"six":{"how_it_makes_money":"賺三種錢：向 CoreWeave 收 15 年期資料中心租金（2026Q3 起每季約 8,000 萬美元）、數位資產交易／放款／資管與質押收費、自營部位與創投增值；錢卡在 Helios 已核准的電力與承租方信用這一節","moat":"護城河 C 級、方向持平：資料中心的優勢是批次審查前已核准的電力，數位資產端靠資本、牌照與機構關係並小幅拿到交易份額，兩邊都還沒有定價權證據","growth":"五年後跑道中等：Helios I/II 約 1.6GW 已核准，之後的 2.6GW 要等 2027 年 4 月 ERCOT 分配；代幣化是管理層說的第二條曲線，但他們自己也說還沒看到大規模轉移","capital":"資本配置中等：回購已超過抵銷股權報酬稀釋，但回購期間公司仍虧損；資料中心以 9.875% 舉債擴張，增量報酬貼近資金成本","valuation":"現價大致等於基本情境：Helios I 建成且 CoreWeave 付滿租約、資料中心約 12 倍 EBITDA；要更高需要 Helios II 簽到投資等級租約、市場給 14 倍以上，一年內我不信","how_wrong":"最可能看錯的是 CoreWeave 的信用與 Helios II 的條件，兩者都會在 12–18 個月內見分曉；增量報酬只略高於 9.875% 的資金成本，看對了每股價值也長得慢"}},"decision_inputs":{"signal":"C","ma":"-","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":true,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不追價，等 Helios II 與投資等級承租方簽約且 CoreWeave 付租正常；2026-12 德州稽核或 2027-04 電力分配結果不利則再延後","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"金融","price_at_dd":15.14,"week26_return_pct":-48.13,"consensus_rev_3m_pct":-86.27,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"營收為數位資產買賣總額（FY2026 共識約 518 億美元），資料中心租金目前不到 1%，EV/S 與 P/S 分母不反映獲利來源；情境樹的 EV/S 只是把分部加總結果換算成腳本形狀，倍數上升主要來自舉債建置的資產沒有反映在總額營收，不等於估值重評"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"德州資料中心稽核結果公布，涵蓋 Helios II","impact":"高","watch":"Helios II 是否被要求重新審查或延後通電"},{"date":"2026-12","date_precision":"month","type":"other","event":"4.45 億美元可交換債到期","impact":"中","watch":"以現金償還或改發新債、票息水準"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"2026 年第四季財報","impact":"中","watch":"數位資產分部 EBITDA 是否轉正、Helios II 進度"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"ERCOT Batch Zero 研究負載電力分配","impact":"高","watch":"Caspian、Selene、Helios III 合計 2.6GW 分到多少基載與通電時程"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"Helios Phase II 首批資料廳交付","impact":"高","watch":"是否準時、是否超支"},{"date":"2027-Q2","date_precision":"quarter","type":"other","event":"Phase III 債務融資","impact":"中","watch":"票息與貸款成數是否高於 Phase II 的 9.875%"}],"_projected_from":"v19"}
```
