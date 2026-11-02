你是 stock-analyst v20 的**散文層（prose）agent**，標的 FTNT（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTNT_20261102/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：FTNT　日期：2026-11-02　archetype：None　前份裁決：2026-07-30　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1849B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（585B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（998B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1578B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1200B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（734B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（808B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2229B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3532B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2972B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1849           3606-5151      5 條（2–6 內）  
s3                  8000         585           5190-7415      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3776          7857-11224      5 條（2–6 內）  
s6                 11000         734          7186-10266      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         808           1884-2692      5 條（2–6 內）  
s10                 5000        2229           1940-2771      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2972           2000-2028      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5356B；至少需散文≈39.64KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−53%
−52%
−48%
−47%
−44%
−40
−40%
−19.9%
−15%
−10.5%
−10%
−5%
−2.2%
−1.8
−1.0
−0.9%
0
0%
0.3%
0.5
0.75
0.9
01
1
1%
1.0
1.2
1.20
1.24
1.5%
1.8
02
2
2%
2.1%
2.42
2.6%
2.9%
3%
3
3.2
3.20
3.22
3.3
3.4
3.5
3.5%
3.54
3.56
3.57
3.58
3.6
3.6%
3.80
3.8
3.88
3.9
3.9%
04
4
4.09
4.15
4.2
4.3
4.39
4.5
4.6%
4.8
4.92
5%
5
5.46
5.5
5.6
6
6%
6.00
6.1%
6.25
6.5
7
07
7.05
7.5%
7.65
7.7%
8%
8
08
8.7%
9
10%
10
10.6%
10.9%
11
11%
11.1%
11.5%
11.8%
12
12%
12.2
12.2%
12.7
13%
13
13.1
13.1%
13.5%
14%
14
14.25%
14.5%
15
15%
15.5%
16%
18.0
18.53
19
19%
19.9%
20%
20
20.5%
20.78
21
22
22%
22.2
22.26
23%
23.36
24
25%
25
26%
26
26.6
27
28
28%
29
29%
30%
30
31
31%
31.6
31.7%
32%
32
32.7%
32.8%
33%
33
33.9%
34%
35%
35
35.07
35.1
35.8%
36
37%
38
38.1
38.12
38.2%
40
40%
41
42
42.4
43.9%
44%
44.4
44.5
45%
45
47%
47.99
48
49
50%
51%
51.5
51.7
52%
55%
57.7%
57.7
60%
63%
64
65
67%
70
75%
76
78
78%
79.6%
79.7
80
80%
80.3%
81
81.25
82.15
85
86
88
89
91.15
95%
96
100
100%
115
116
131
$131
136
136.08
140
150%
160
162
169.85
170
$183
183
215
225.6
250
273
742
2024
2025
2026
2027
2030
20261102
2,462
8,200
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
{"meta":{"ticker":"FTNT","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Fortinet, Inc."},"oneliner":"Fortinet 是同業中利潤率最高的整合型網路資安廠。Q3 billings 成長 29%，但服務營收只成長 13%，沒有兌現下半年轉強的說法；股價跌兩成後仍是今年預估盈餘 38 倍，等服務成長回到 15% 或股價到 116 美元附近再進場。","thesis":{"H":[{"id":"H1","text":"服務營收減速是大型合約延後生效造成的時點落差，FY2027 服務營收成長回到 15% 以上","2y":"FY2027 服務營收年增 ≥15%，短期遞延收入年增 ≥14%","5y":null,"10y":null,"threshold":"FY2027 服務營收年增 ≥15%（FY2026 指引約 +13%）","source":"季報新聞稿的服務營收、10-Q 的短期遞延收入、2027 年 1–2 月的 FY2027 財測","drift_rule":"以 TTM 服務營收增速對照 15% 門檻：偏離 ≥5%（低於 14.25%）連 2 季為削弱，偏離 ≥10%（低於 13.5%）連 3 季為反轉；自 2027 Q1 起算"},{"id":"H2","text":"產品營收在換機與漲價高峰後不回吐：AI 資料中心、OT 與內部分段的高階機需求接手，FY2027 產品營收不衰退，非GAAP 營益率守在 34% 以上","2y":"FY2027 產品營收年增 ≥0%，非GAAP 營益率 ≥34%","5y":null,"10y":null,"threshold":"產品營收年增 ≥0%；非GAAP 營益率 ≥34%","source":"季報新聞稿的產品營收與非GAAP 營益率","drift_rule":"TTM 產品營收增速低於門檻 5 個百分點以上（≤−5%）連 2 季為削弱，低於 10 個百分點以上（≤−10%）連 3 季為反轉；營益率低於 34% 連 2 季為削弱"},{"id":"H3","text":"單一 FortiOS 加上自研 ASIC，讓 FTNT 在 SASE、OT、AI 資料中心持續拿份額，同時保住同業最高的 GAAP 營益率","2y":null,"5y":"SASE firewall billings 年增持續高於市場的約 16%，GAAP 營益率 ≥30%","10y":null,"threshold":"SASE firewall billings 年增 ≥16%；GAAP 營益率 ≥30%（PANW 約 6%）","source":"法說的 SASE firewall 與 OT billings 揭露、季報 GAAP 營益率、同業財報","drift_rule":"TTM 偏離門檻 ≥5% 連 4 季為削弱，偏離 ≥10% 連 6 季為反轉"}],"R":[{"id":"R1","text":"服務附加率結構下滑：主權地端方案與網通元件附加率低，漲價後硬體與服務間折扣變大，美國稅務誘因又把採購推向硬體，服務成長卡在 13% 以下","h_ref":"H1","clock":"⚡","threshold":"服務營收年增 ≤12% 連 2 季，或短期遞延收入年增 <12%","evidence_refs":["end_markets#2"]},{"id":"R2","text":"產品雙高峰回吐：漲價（約 10 個百分點）與上半年庫存紅利退場，2027 年到期機台只剩低階機，客戶又已提前購買","h_ref":"H2","clock":"🔥","threshold":"產品營收年增 <0% 連 2 季，或 billings 年增 <10%","evidence_refs":["supply_demand_durability#0"]},{"id":"R3","text":"雲端交付與大廠綑綁侵蝕地端防火牆，替代技術讓單一 FortiOS 平台的附加價值下移","h_ref":"H3","clock":"🐢","threshold":"SASE firewall billings 年增 <16% 連 4 季，或 GAAP 營益率 <28%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"id":"R4","text":"供應鏈與地緣：台灣代工集中、單一來源零件與記憶體成本上升，加上中國禁用令與出口管制","h_ref":"H2","clock":"🔥","threshold":"non-GAAP 總毛利率 <78% 連 2 季，或產品營收連 2 季低於指引中點","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#3"]},{"id":"R5","text":"通路與信用集中：三家經銷商占營收約 55%，六家占應收 67%；最大經銷商若陷入財務困難，會同時打到收款與出貨","h_ref":"H1","clock":"🐢","threshold":"任一前三大經銷商付款延遲或發生信用事件；或六家經銷商占應收 >75%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R6","text":"法律與信任尾部：證券集體訴訟指控誇大換機週期；FortiOS 高風險漏洞通報反覆出現，同一作業系統構成共同故障面","h_ref":"H3","clock":"🐢","threshold":"駁回動議被否決、進入證據開示；或出現遭大規模利用、迫使關閉雲端服務的漏洞事件","evidence_refs":["major_events#0","lawsuit_class_action#0","product_recall_warning#0"]}],"single_thing":{"description":"2027 年 1–2 月公布的 FY2027 初始財測，服務營收成長沒有高於 FY2026 的約 13%","why_fatal":"服務約占營收 63%，是撐住 35 倍倍數的經常性收入。CFO 已在 Q3 口頭承諾 2027 服務成長率高於 2026；若財測沒做到，就是繼下半年轉強之後第二次落空，市場會把服務落後從時點問題改判為附加率結構下滑，終端倍數由 27 倍再降到 20–22 倍。這項的敏感度大於任何單一產品、法律或地緣事件","if_happens":"Base 改用接近空頭的路徑，合理價約 80–100 美元（FY2027E–FY2028E 共識×22 倍）；不進場，已有部位減碼一半，下一季服務營收仍 ≤12% 則清倉","how_monitor":"Q4 2026 財報（2027 年 2 月）的服務營收財測與短期遞延收入年增率；在那之前，先看 BMO、UBS、Barclays 投資人會議上管理層的口徑","probability":"約 20%：短期遞延收入 +14.5%、服務 billings +26% 支持改善，但 Q2 的同一個承諾已經落空一次"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":35.07,"peg_fy2":3.22,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.42,"FY2026E":3.57,"FY2027E":3.88,"FY2028E":4.39},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 非GAAP 共識。FY2025A 只取得年度財報的 GAAP 稀釋 EPS 2.42 美元，非GAAP 年度值事實表未涵蓋；因此以 FY2025A 為基期算出的三年年化約 22% 偏高，含 GAAP／非GAAP 口徑差。可比口徑請用 FY2026E→FY2028E 年化 10.9%"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FTNT_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"毛利率約 80%、GAAP 營益率連兩年 30% 以上、FCF 利潤率四年 31–33%（TTM 44%）、淨現金約 42 億美元；但產品約占營收 37%，帶硬體週期"},"industry":{"clock_phase":"III","sd_verdict_source":"產品端週期性將反轉：管理層 2025-11 稱約 65 萬台防火牆 2026 年底到期，2027 年只剩約 35 萬台低階機，換機延續 4–6 季（Zacks 轉述）；Q3 漲價趨穩、庫存紅利消失。服務與 SASE 端結構性持久：服務 billings +26%、短期遞延收入 +14.5%（Q3 法說）","bargaining":{"up":"上游偏強：ASIC 與部分零件為單一或有限來源，沒有保障產能與價格的長約（10-K），記憶體漲價、交期拉長。FTNT 以採購量與自管製造緩衝，但 Q3 總毛利率仍年減 1.8 個百分點","down":"下游終端客戶分散，但通路集中：三家經銷商占營收約 55%、六家占應收 67%。大型企業與主權客戶議價力上升，要求延後服務生效、合併服務合約","geo":"硬體約 85–95% 在台灣代工（10-K）；中國 2026 年初要求國內企業停用美國與以色列資安產品，FTNT 在列；加密產品受美國出口管制"},"profit_pool_dir":"利潤池往整合平台移動，FTNT 受惠；交付方式往雲端移動，FTNT 以地端為主，屬威脅。淨方向待驗","tam_table":[{"item":"全球資安支出 2026","value":"約 2,462 億美元，年增 12.2%（Gartner，二手部落格轉述）"},{"item":"SASE firewall 市場增速","value":"約 16%（CEO，2026-10-28 法說口述）"},{"item":"FTNT 防火牆出貨台數市占","value":"約 55%（2025 Q4 法說）"},{"item":"FTNT SASE firewall billings 增速","value":"Q3 +31%、Q2 +34%（法說），約為市場兩倍"},{"item":"SAM、營收滲透率、營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"自研 ASIC 的效能成本優勢，加上單一 FortiOS 整合網路與安全；安裝基數帶動服務附加與轉換成本","execution":9,"pricing":7,"combined":8.0,"score":8.0,"grade":"B","trend":"→","trend_evidence":"執行面擴大：FY2026 billings 財測年內三度上調，大額訂單總值 +51%，OT billings 約 +40%，Q3 GAAP 營益率 33.9%。定價面縮減：漲價約貢獻 billings 10 個百分點，但 Q3 起趨穩；Q3 總毛利率年減 1.8 個百分點，產品端成本上升、折扣變大。兩者合成為穩定（→）。台數市占 55% 是管理層口徑，目前未見第三方份額下滑的證據","threats":[{"level":"🔴","text":"雲端交付 SASE（Zscaler、CRWD）與大廠綑綁（MSFT 等）。10-K 自承平台多數仍為地端部署，轉型慢於對手可能流失客戶；較大對手也可能把功能併入既有產品","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"level":"🟡","text":"單一 FortiOS 的漏洞集體曝險：2026 年多國政府發布 Fortinet 產品高風險漏洞通報。同一作業系統的設計是整合優勢，也是共同故障面","p":"20%","evidence_refs":["product_recall_warning#0"]},{"level":"🟡","text":"中國禁用令與加密產品出口管制：北京要求國內企業在 2026 上半年前替換，該市場已關閉；中國營收占比事實表未涵蓋","p":"已發生","evidence_refs":["reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#3"]},{"level":"🟡","text":"台灣代工與單一來源零件：約 85–95% 硬體在台灣代工，ASIC 與部分零件沒有長約。兩岸緊張或記憶體短缺會同時打到交期與毛利","p":"10%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推定）：TTM 營益率 32.7%，客戶預付形成的遞延收入大於應收、存貨與廠房，投入資本極低；確切的投入資本與 ROIC 數值事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（IT／OT 網路）、決策者（資安長與董事會）、付款者（企業與政府）三個角色都成立；延後採購的代價是被攻擊，屬於「需要」而非「想要」。Q3 法說稱 AI 攻擊讓資安升到董事會議題，Gartner 估 2026 資安支出 +12.2%。低階零售客戶有延長使用的現象，屬局部"},{"item":"決策層級","level":"🟡","text":"在單一機櫃、單一網段的層級，換掉 FortiGate 要重寫政策、重訓人員，單一 FortiOS 整合又拉高轉換成本。但新的 SASE 與 AI 安全採購可以直接選雲端交付方案，繞過地端設備。續約率、流失率等代理變數事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"上游 ASIC 與部分零件為單一或有限來源、沒有保障長約，記憶體漲價、交期拉長，Q3 總毛利率年減 1.8 個百分點，代表上游正在多拿；下游三家經銷商占營收約 55%。FTNT 靠自研 ASIC 與自管製造守住約 80% 毛利，仍是價值鏈中最難取代的一環"},{"item":"社會容忍度","level":"🟢","text":"企業資安沒有價格管制，5–20% 的漲價已被吸收；上限來自客戶預算（CFO：漲價有上限），不是政治或監管。主權與合規需求反而加分。中國禁用令屬地緣問題，不是價格容忍問題"}],"roiic":"事實表未涵蓋（缺投入資本、折舊攤銷）","reinvest_rate":"近零或為負：FY2026 基礎設施投資指引 3.9–4.2 億美元，對比推算約 26 億美元的非GAAP 淨利（3.56 美元×約 742 百萬股）偏小；遞延收入增長讓營運資金成為資金來源；收購只有 Virtue AI（公司稱不重大）。折舊攤銷未知，無法算淨值","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。本例的成長由客戶預付推動，兩項都失真，所以不給數字。成長上界改看需求端：資安支出約 +12%、SASE firewall 市場約 +16%"},"spread_table":[{"metric":"毛利率","FTNT":80.04,"PANW":70.36,"CRWD":75.25,"MSFT":67.66,"OKTA":78.13,"unit":"%"},{"metric":"營業利益率","FTNT":32.66,"PANW":6.05,"CRWD":-2.21,"MSFT":47.1,"OKTA":7.68,"unit":"%"},{"metric":"FCF 利潤率","FTNT":43.94,"PANW":35.83,"CRWD":28.22,"MSFT":17.31,"OKTA":31.21,"unit":"%"},{"metric":"研發密度","FTNT":11.1,"PANW":22.23,"CRWD":28.84,"MSFT":10.52,"OKTA":21.18,"unit":"%"}],"competitors":[{"name":"PANW","gm":70.36,"om":6.05,"fcf_margin":35.83,"rd_intensity":22.23,"strategy_note":"以平台化與雲端 SASE 正面對打。TTM 營益率約 6%，研發密度 22% 是 FTNT 的兩倍，等於用投入換份額，獲利結構撐不起長期價格戰","period":"TTM ending 2026-07-31（4季加總）"},{"name":"CRWD","gm":75.25,"om":-2.21,"fcf_margin":28.22,"rd_intensity":28.84,"strategy_note":"端點與雲端交付起家，TTM 營益率為負，是 10-K 點名的雲端交付威脅；與 FTNT 重疊在 SecOps 與 SASE 邊界，不在高效能防火牆","period":"TTM ending 2026-07-31（4季加總）"},{"name":"MSFT","gm":67.66,"om":47.1,"fcf_margin":17.31,"rd_intensity":10.52,"strategy_note":"不是純資安廠，營益率 47%；威脅在於把安全功能綑綁進既有授權，壓縮中小企業單獨採購資安產品的空間","period":"TTM ending 2026-09-30（4季加總）"},{"name":"OKTA","gm":78.13,"om":7.68,"fcf_margin":31.21,"rd_intensity":21.18,"strategy_note":"身分層廠商，毛利率 78%、營益率約 8%，目前多為互補；若 AI 代理身分成為新的控制點，會分走部分價值鏈","period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"FY2026：量（換機、OT、AI 資料中心）＋價（漲價約貢獻 billings 10 個百分點）＋上半年庫存成本紅利。FY2027 起價格與庫存紅利退場，回到量與服務附加，回購貢獻小","runway_years":"事實表未涵蓋（缺營收滲透率）","runway_post_y5":"🟢","endo_ceiling_basis":"需求端上界：資安支出 +12.2%（Gartner 二手轉述）、SASE firewall 市場約 +16%（CEO 口述）。資本面因客戶預付不構成約束，增量 ROIC 無法計算","segments":[{"item":"產品營收（Q3）","value":"7.65 億美元，年增 37%（Q2 年增 52%）；FY2026 推算約 30 億美元（營收財測中點減服務財測中點）"},{"item":"服務營收（Q3）","value":"約 13.1 億美元，年增 13%；FY2026 財測 51.5–51.7 億美元，年增約 13%"},{"item":"服務領先指標（Q3）","value":"服務 billings +26%、總遞延收入 +19%、短期遞延收入 +14.5%（五季最高）"},{"item":"SASE firewall billings","value":"Q3 +31%；Q2 業務規模逾 20 億美元、+34%"},{"item":"OT billings","value":"Q3 約 +40%，Q2 逾 +55%"},{"item":"AI 驅動 SecOps billings","value":"Q3 +15%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"note":"Q3 總毛利率 −1.8 個百分點、前九月 −1.0，上半年合計為負；Q2 單季值未收"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱 SASE firewall 成長約為市場兩倍；未見第三方份額下滑資料"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"Q2 台數與 ASP 同升；低階零售有延長使用，屬局部"},{"signal":"EPS 年化成長高於營收超過 5 個百分點","lit":true,"note":"FY2022–25 GAAP 每股盈餘年化 31.7%、營收 15.5%；前瞻共識兩者已接近"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"FY2025 為 1.20"},{"signal":"SBC／營收超過 5% 且逐年上升","lit":false,"note":"Q3 為 3.9%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"雲端交付替代是風險，尚未反映在數字上"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數序列"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"基礎設施投資約 4 億美元，對比 TTM FCF 約 35 億美元"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"無此情形"}],"trap_rating":"🟡（亮兩項）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；近三年回購金額與現金去向四分事實表未涵蓋，不展開"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"唯一收購 Virtue AI 金額未揭露、公司稱不重大，沒有可算的併購報酬","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"年初至今回購均價約 78 美元，對 FY2026E 3.57 美元的盈餘殖利率約 4.6%；現價約 2.6%。十年期公債殖利率事實表未涵蓋，無法比較","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 年化約 3.3 億美元，占市值約 0.3%，遠低於 1.5%；股數年變化事實表未涵蓋","grade":"過"}]},"valuation":{"basis":"FY1／FY2 非GAAP 共識預估本益比＋PEG","tier":"大型高品質資安平台","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率與研發密度，沒有同業倍數，不自行補數"},"fwd_pe":38.12,"peg":3.5,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 預估本益比 38.1 倍、FY2 35.1 倍；共識 FY2026E→FY2028E 每股盈餘年化 10.9%，PEG 約 3.5，高於 2 屬貴（PEG 用兩年前瞻成長，因 FY2025 非GAAP 基期事實表未收）。本益比 44.5 倍在近四個年度端點的 89 分位，五年分位資料不足。情境估算：12 個月後以 FY2028E 4.39 美元×32 倍＝140 美元，上檔約 3%；五年 Base 終點 162 美元，上檔約 19%。結論是偏貴（🟠）而非極貴：盈餘仍在成長，淨現金 42 億美元，FCF 利潤率 44%","upside_short_pct":3.2,"upside_mid_pct":19.0},"trap_analysis":{"verdict":"🟡","label":"高品質但處在硬體高峰後段，估值仍走在基本面前面"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 產品成長由 Q2 的 52% 降到 37%；漲價約貢獻 billings 10 個百分點且已趨穩，上半年低成本庫存紅利消失。CFO 承認美國客戶因稅務折舊誘因偏向買硬體，同業也曾提前拉貨避漲價；2027 年到期機台只剩約 35 萬台低階機；服務附加率在主權方案與網通元件上本來就較低。","assumption":"換機高峰後，由 AI 資料中心、OT、內部分段的高階機接手，產品不回吐","consequence":"FY2027 產品營收減約 15%、服務只成長 8%、營益率回到 32%，每股盈餘 3.20 美元後年增約 5%，五年後只值 20 倍，股價約 76 美元（−44%）。這條與唯一致命點部分重疊：服務那一半已由唯一致命點涵蓋，產品回吐那一半另列減碼門檻補上","ruling":"採納為空頭主路徑，機率 30%。不加到 35% 以上，因為 billings 仍 +29%、通路庫存占 billings 比率持平或下降（Q3 法說）、遞延收入 +19%，回吐目前沒有直接證據","watch":"Q4 2026 與 Q1 2027 產品營收年增率、通路庫存占 billings 比率、FY2027 初始財測","evidence_refs":["end_markets#2","supply_demand_durability#0"],"fact_refs":["f_kpi2","f_kpi8_q4_2026","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"TTM FCF 利潤率 43.9%，遠高於 FY2022–25 的 31.6–32.8%；多出的部分來自 billings 快於營收的遞延收入累積與上半年庫存去化。記憶體等零件漲價、單一來源、沒有長約，Q3 總毛利率年減 1.8 個百分點。三家經銷商占營收約 55%，六家占應收 67%。","assumption":"營收成長達標時，每股自由現金流同步成長","consequence":"營收照共識成長，但 FCF 利潤率回到 33–35%、毛利率滑向 78%，FY2027–28 每股自由現金流幾乎不成長；以 FCF 計的估值更貴，在 30 倍以上執行的回購報酬偏低","ruling":"部分採納。Base 已用共識 FY2027 每股盈餘只 +8.7%（隱含利潤率收斂），且不以 TTM FCF 利潤率 44% 支撐估值。通路與應收集中目前沒有信用事件（搜尋未見經銷商降評），只列監測","watch":"FCF 利潤率連 2 季低於 35%；non-GAAP 總毛利率連 2 季低於 78%；經銷商付款延遲或應收天數上升","evidence_refs":["geo_supply_chain#0","customer_concentration_credit#0","customer_concentration_credit#1"],"fact_refs":["f_peer_ftnt_fcf_margin_pct","f_kpi6_fcf"]},{"view":"價格已反映太多","evidence":"股價跌約 20% 後，仍是 FY2026E 38.1 倍、FY2027E 35.1 倍；共識 FY2026E→FY2028E 年化只有 10.9%，PEG 約 3.5。P/S 與 EV/S 都在近四個年度端點的最高區，賣方目標價全距約 70–215 美元。","assumption":"高品質加上 AI 資安主題，可以支撐 35 倍以上的倍數到 2030 年代","consequence":"即使盈餘照共識成長，倍數由 35 倍收斂到 27 倍就吃掉大部分報酬，Base 五年年化不到 5%","ruling":"採納，這是本次不追的主因。股價約 116 美元（FY2027E 30 倍）時，Base 年化可回到約 8%","watch":"股價對 FY2027E 共識的倍數；共識 FY2027–28 每股盈餘的修正方向","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_consensus_eps_fy3"]},{"view":"論點失敗","evidence":"10-K 自承平台多數仍為地端部署；CrowdStrike、Zscaler 主打雲端交付，較大的對手可能把安全功能綑綁進既有產品；替代技術也可能讓產品過時。2026 年多國政府發布 Fortinet 產品高風險漏洞通報。","assumption":"網路線上的防火牆在 AI 時代仍是強制執行點（CEO 說法）","consequence":"新的 SASE 與 AI 安全決策繞過地端設備，服務附加的天花板下移，終端倍數落到 20 倍區間","ruling":"部分採納為長期風險。目前 SASE firewall billings +31%、FortiSASE 成長快、主權地端需求反而上升，雲端替代還沒出現在數字上；列為生態攻擊級威脅，機率 30%","watch":"SASE firewall billings 增速是否跌破市場的約 16%；GAAP 營益率是否跌破 30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0","product_recall_warning#0"],"fact_refs":["f_kpi4_gaap"]},{"view":"論點失敗","evidence":"證券集體訴訟指控公司在 2024-11 至 2025-08 期間誇大防火牆換機週期，合併訴狀已於 2026-04-24 提出。中國要求國內企業在 2026 上半年前停用 Fortinet 等產品；約 85–95% 硬體在台灣代工。","assumption":"法律、地緣與供應鏈的尾部事件不會同時發生","consequence":"訴訟進入證據開示並出現不利和解，或台海事件打斷出貨，短期股價可落到空頭區間下緣","ruling":"不採納為主路徑，只當尾部。訴訟金額與受影響營收事實表未涵蓋，程序還在駁回動議前後；中國市場已關閉，損失已反映在數字中；台海屬低機率、高衝擊","watch":"駁回動議的裁定；中國以外地區出現類似禁令；代工交期","evidence_refs":["major_events#0","lawsuit_class_action#0","reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#1"],"fact_refs":[]}],"max_dd":{"lo":-55,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 169.85 → 本次 136.08（-19.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=169.85","side_b":"本次 price_at_dd=136.08","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 169.85 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 169.85 美元：Bull 價 273、Bear 價 88，五年期望值 +7.5%，基準年化 2.9%，不對稱比 1.0","side_b":"本次情境、股價仍用 169.85 美元：Bull 價 225.6、Bear 價 76，五年期望值 −10.5%，基準年化 −0.9%，不對稱比 0.5","ruling":"先換情境、股價不動：五年期望值少 18.0 個百分點，基準年化少 3.8 個百分點。不對稱比由 1.0 變為 0.5。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 169.85 美元：五年期望值 −10.5%，基準年化 −0.9%，不對稱比 0.5","side_b":"本次情境、股價 136.08 美元：五年期望值 +11.8%，基準年化 3.5%，不對稱比 1.24","ruling":"再換股價、情境不動：起點價下跌 19.9%，五年期望值多 22.2 個百分點，基準年化多 4.5 個百分點，不對稱比由 0.5 升到 1.24。合計五年期望值比前份多 4.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：股價下跌後的訊號、估值結論與裁決","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-07-30，169.85 美元）：訊號 B、估值偏貴（🟠）、觀望、追蹤，NTM 本益比 44.4 倍","side_b":"本次（136.08 美元，跌約 20%）：訊號 B、估值偏貴（🟠）；裁決與角色由決策矩陣依本次輸入重算","ruling":"股價跌了兩成，但同期 FY2026E 共識上修 13%，跌幅主要是倍數收斂（NTM 44.4 倍→FY1 38.1 倍）。對 FY2027E 仍有 35 倍，相對 10.9% 的成長仍貴，所以估值結論與訊號不變","evidence_level":"事實表價格與共識、前份摘要","settle_metric":"股價對 FY2027E 共識的倍數","if_then":["若股價跌到 FY2027E 30 倍（約 116 美元）以下，且服務營收沒有惡化：分批首倉","若股價在服務證據到位前反彈到 FY2027E 40 倍以上：不追"],"evidence_refs":[]},{"axis":"前份漂移：情境機率與最大回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 25%、空頭 30%，最大回撤單點 −52%","side_b":"本次：多頭 25%、基準 45%、空頭 30%；最大回撤改為 −40% 至 −55% 區間，空頭終點每股盈餘不高於 FY2027E 共識","ruling":"機率不變：新證據一正一負（billings 強、服務轉強落空），兩者相抵。最大回撤由單點改為區間屬口徑改變，區間中位約 −47%，與前份 −52% 接近","evidence_level":"本次情境推導","settle_metric":"FY2027 初始財測","if_then":["若 FY2027 財測服務營收成長 ≥15%：多頭機率上調到 35%，空頭降到 20%","若服務成長指引 ≤13%：空頭機率上調到 40%，終端倍數以 20 倍以下重算"],"evidence_refs":[]},{"axis":"前份漂移：陷阱風險、護城河方向、成長跑道、公司類型","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份：陷阱風險中等（🟡）、護城河方向穩定（→）、五年後跑道寬（🟢）、品質複利成長","side_b":"本次四項維持：陷阱風險中等、護城河穩定、跑道寬、品質複利成長（類型信心由高降為中）","ruling":"Q3 新證據有兩面。執行面（billings +29%、大額訂單 +51%、OT +40%）支持穩定；定價面（毛利率年減 1.8 個百分點、漲價趨穩）與服務轉強落空偏負。衰退信號仍亮兩項，第二曲線（OT、SASE）仍有來源。產品占比上升，所以類型信心降一級","evidence_level":"Q2、Q3 法說與事實表","settle_metric":"服務營收年增率、non-GAAP 總毛利率、SASE firewall billings 增速","if_then":["若 non-GAAP 總毛利率連 2 季 <78% 且服務成長 ≤12%：護城河方向改判縮減（↓），B 級之下轉為迴避","若 SASE firewall billings 增速連 4 季 <16%：跑道改判中等（🟡）"],"evidence_refs":["geo_supply_chain#0"]},{"axis":"前份漂移：循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"中循環","side_b":"晚循環","ruling":"產品增速由 Q2 的 52% 降到 Q3 的 37%，Q4 營收指引中點只有 +15%；上半年庫存紅利消失、漲價趨穩、零件交期拉長，CFO 也提到美國稅務誘因推動硬體採購。這些都是硬體週期高峰後段的特徵","evidence_level":"Q2、Q3 兩場法說逐字稿","settle_metric":"產品營收年增率","if_then":["若 2027 上半年產品營收年增仍 ≥10%：改回中循環，事件路徑的價格上限放寬到 FY2027E 38 倍","若產品營收年增轉負連 2 季：維持晚循環，不進場"],"evidence_refs":[]},{"axis":"前份漂移：進場首倉條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"價格路徑：FY+2 口徑 32x（約 $131）。事件路徑（不需更低價）：2027-01~02 之 FY2027 初始指引 billings ≥ +15% 且產品營收 ≥ 0%，屆時上限＝當時 FY+2 EPS 的 36x（約 $183，推導見 §14b）。","side_b":"股價≤116 美元（FY2027E 共識 30 倍）；或 FY2027 財測服務營收成長≥15% 且 billings≥15%，價格上限 FY2027E 36 倍（約 140 美元）","ruling":"前份的價格錨是 FY+2 的 32 倍。以 131÷32 回推，分母約 4.09 美元，最接近當時的 FY2028E；依同一定義，現值約 140 美元（4.39×32），現價 136 美元已觸及，本份就是觸及後的重跑判斷。新門檻改為 FY2027E 30 倍（約 116 美元），理由是新證據：FY+2 的上修主要來自已趨穩的漲價與庫存紅利，服務成長也沒有如期改善，分母品質下降。所以改錨在高峰後的第一年，並把倍數訂在 Base 年化約 8% 的位置。事件路徑由「產品營收 ≥0%」改為「服務營收 ≥15%」，因為 Q3 證明服務才是撐住倍數的承重項。事件成立時 Base 上移到 FY2031E 約 6.5 美元、終端 30 倍，以 140 美元進場年化約 8%，因此價格上限由約 183 美元改為約 140 美元。任一條件觸發，都先重跑判斷再進場首倉","evidence_level":"前份摘要、事實表共識、Q3 法說","settle_metric":"股價對 FY2027E 倍數；FY2027 服務營收財測","if_then":["若股價先跌到 116 美元以下且服務數據沒有惡化：重跑判斷後分批首倉","若 2027-02 財測服務成長 ≥15% 且 billings ≥15%：價格在 140 美元以下分批首倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"Single Thing：2027 年 1–2 月公布的 FY2027 初始財測，服務營收成長沒有高於 FY2026 的約 13%","ruling":"前份把風險分散在三條，沒有指定敏感度最大的單一事件。本次以服務成長為唯一致命點：服務約占營收 63%，是倍數的承重項，一旦落空，倍數由 35 倍落到 25 倍以下，衝擊大於任何單一產品、法律或地緣事件。發生即不進場，已有部位減碼一半","evidence_level":"Q3 法說 CFO 對 2027 服務成長的口頭承諾","settle_metric":"FY2027 服務營收財測","if_then":["若財測服務成長 ≤13%：不進場，已有部位減碼一半；下一季仍 ≤12% 則清倉","若財測服務成長 ≥15%：唯一致命點解除，改以產品回吐為主要風險"],"evidence_refs":["end_markets#2"]},{"axis":"減碼與清倉門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼與清倉門檻（空值）","side_b":"服務營收年增 ≤12% 連 2 季減碼一半；產品營收年增 <0% 連 2 季減碼一半；non-GAAP 總毛利率 <78% 連 2 季停止加碼；服務成長指引 ≤10% 且 SASE firewall billings 增速 <16% 清倉","ruling":"前份只有進場條件，沒有出場門檻，本次補上。門檻取 Q3 實際值往下一格：服務 13%→12%，毛利率 79.6%→78%（即 Q4 指引下緣）","evidence_level":"季報新聞稿與法說","settle_metric":"各門檻對應的季報數字","if_then":["若任一減碼門檻觸發：已有部位減碼一半","若清倉門檻觸發：清倉"],"evidence_refs":[]},{"axis":"服務營收：時點落差還是附加率結構下滑","cause":"新證據","prior_field":null,"side_a":"2026-07-29 Q2 法說，CFO 仍預期下半年服務營收成長轉強，並稱 2026 Q1 是服務成長谷底。Q3 管理層把落後解釋成大型新客戶延後啟用服務、合併成企業合約的時點問題","side_b":"2026-10-28 Q3：服務營收 +13%（Q2 +14%），全年服務財測下修到約 +13%；CFO 改口「我沒用過加速一詞，說的是成長率改善」，並把改善延到 2027。同一場 CFO 也承認網通元件與主權方案附加率較低、漲價後硬體與服務間折扣變大、美國稅務誘因推動硬體","ruling":"可調和，屬程度差異。服務 billings +26%、短期遞延收入 +14.5% 支持時點說，但 CFO 自己列出的三項都是結構因素，無法拆出各占多少。裁定時點與結構各半，H1 門檻定在 15%，並列為唯一致命點。管理層的一次性歸因標為未證、持續監測：若 2027 Q1、Q2 服務營收年增仍低於 14%，時點說即證偽","evidence_level":"兩場管理層逐字稿，數字為公司公告","settle_metric":"FY2027 服務營收財測；2027 Q1–Q2 服務營收年增率；短期遞延收入年增率","if_then":["若 FY2027 財測服務營收成長 ≥15% 且 Q4 短期遞延收入年增 ≥14%：時點說成立，價格在 FY2027E 36 倍以下分批首倉","若服務成長指引 ≤13%，或 2027 上半年連 2 季低於 14%：結構說成立，Base 終端倍數降到 25 倍，不進場，已有部位減碼一半"],"evidence_refs":["end_markets#2"]},{"axis":"定價權：維持毛利率的政策對上毛利率下滑","cause":"新證據","prior_field":null,"side_a":"2026-07-29 CEO：調價以維持相同毛利率為公司政策，記憶體價格近幾週趨穩","side_b":"2026-10-28：Q3 總毛利率年減 1.8 個百分點；CFO 稱下半年成本上升、漲價有上限、客戶預算有限；CEO 稱零件交期拉長，價格趨穩但沒有改善","ruling":"可調和。政策是成本上升時跟著漲價，但有時間落後與幅度上限，產品毛利率在成本上升期會被壓；全年 non-GAAP 毛利率仍守在 79.7–80.3%，靠服務毛利抵銷。所以定價力評 7 分，而非 8–9 分","evidence_level":"兩場管理層逐字稿與 10-Q","settle_metric":"non-GAAP 總毛利率（Q4 指引 78–80%）","if_then":["若 non-GAAP 總毛利率連 2 季 <78%：定價力降到 6 分，Base 終端倍數降到 25 倍，已有部位停止加碼","若毛利率回到 80% 以上連 2 季：定價力回到 8 分"],"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"換機需求：沒有拉貨的說法，對上稅務誘因與集體訴訟","cause":"新證據","prior_field":null,"side_a":"2026-07-29 CEO：沒有看到過量庫存或提前拉貨。Q3 CFO：通路庫存占 billings 比率持平或下降，合約年期沒有明顯拉長","side_b":"Q3 CFO：美國客戶因稅務折舊誘因偏向買硬體；2025 Q4 法說 CFO：同業提前拉貨避漲價；集體訴訟指控 2024-11 至 2025-08 期間誇大換機週期，合併訴狀 2026-04-24 提出","ruling":"不可裁決至 2027 上半年。通路庫存數據支持沒有拉貨，但需求端的提前購買（客戶為稅務與避漲價先買）不會出現在通路庫存裡。訴訟金額與受影響營收事實表未涵蓋，程序還在駁回動議階段，因此不定價、只監測","evidence_level":"管理層逐字稿、法院文件公告","settle_metric":"2027 上半年產品營收年增率；駁回動議裁定","if_then":["若 2027 上半年產品營收年增轉負連 2 季：提前購買成立，H2 反轉，不進場，已有部位減碼一半","若駁回動議被否決、進入證據開示：倉位上限降一級；出現不利和解：減碼一半"],"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"RSI 26.6 超賣，股價較前份低 20%。billings +29%，全年 billings 財測三度上調；遞延收入 +19%、服務 billings +26%，服務營收落後只是會計時點，2027 會機械性改善。GAAP 營益率 33.9% 業界最高，淨現金 42 億美元，回購額度 20 億美元；FY2026E 共識三個月上修 13%；管理層稱 2027 營收成長會高於市場","side_b":"領先指標確實強，但產品成長含約 10 個百分點的價格與庫存紅利；共識 FY2027 每股盈餘只 +8.7%。FY2027E 35 倍要求服務改善必須兌現，而 Q2 的同一個承諾剛落空一次","ruling":"不採納現在就買。買方論證的核心（服務會機械改善），三個月後的財測就能驗證，等待成本低。價格先跌到 116 美元，或證據先到，哪個先到就用哪個","evidence_level":"事實表與 Q3 法說","settle_metric":"FY2027 服務營收財測、股價","if_then":["若 2027-02 財測服務成長 ≥15%：當日起以 FY2027E 36 倍為上限分批首倉","若股價在證據到位前反彈到 160 美元以上：不追"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2027 初始財測的服務營收成長達 15% 以上","type":"假設驗證","maps_to":"H1","metric":"FY2027 服務營收成長指引","threshold":"≥15%","action":"達標即 H1 確認，啟動事件路徑的進場評估；落在 13–15% 之間則維持等待","source_freq":"Q4 財報與年度財測（年一次）","date":"2027-02","evidence_refs":["end_markets#2"]},{"n":2,"text":"FY2027 初始財測的服務營收成長沒有高於 FY2026 的約 13%","type":"Single Thing","maps_to":"H1","metric":"FY2027 服務營收成長指引","threshold":"≤13%","action":"不進場；已有部位減碼一半","source_freq":"Q4 財報與年度財測（年一次）","date":"2027-02","evidence_refs":["end_markets#2"]},{"n":3,"text":"股價跌到 FY2027E 共識 30 倍以下","type":"估值rearm","maps_to":null,"metric":"股價÷FY2027E 共識每股盈餘","threshold":"≤30 倍（約 116 美元）","action":"重跑判斷；基本面沒有惡化則分批首倉","source_freq":"每日","date":null},{"n":4,"text":"FY2027 財測服務營收與 billings 成長都達 15% 以上","type":"估值rearm","maps_to":"H1","metric":"FY2027 服務營收與 billings 成長指引","threshold":"兩項皆 ≥15%；價格上限 FY2027E 36 倍（約 140 美元）","action":"重跑判斷後分批首倉","source_freq":"Q4 財報與年度財測（年一次）","date":"2027-02"},{"n":5,"text":"產品營收年增轉負","type":"風險","maps_to":"R2","metric":"產品營收年增率","threshold":"<0% 連 2 季","action":"不進場；已有部位減碼一半","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#0"]},{"n":6,"text":"non-GAAP 總毛利率跌破 Q4 指引下緣","type":"風險","maps_to":"R4","metric":"non-GAAP 總毛利率","threshold":"<78% 連 2 季","action":"定價力下修、Base 終端倍數降到 25 倍；已有部位停止加碼","source_freq":"季報","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":7,"text":"前三大經銷商出現信用事件","type":"風險","maps_to":"R5","metric":"經銷商付款延遲、降評或應收集中度","threshold":"任一前三大經銷商付款延遲或發生信用事件；或六家經銷商占應收 >75%","action":"已有部位減碼一半","source_freq":"季報與年報","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":8,"text":"證券集體訴訟進入證據開示","type":"風險","maps_to":"R6","metric":"駁回動議裁定與和解金額","threshold":"駁回動議被否決","action":"倉位上限降一級；出現不利和解則減碼一半","source_freq":"法院文件（不定期）","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":9,"text":"服務成長與 SASE 份額同時失守","type":"清倉","maps_to":"H3","metric":"FY2027 服務營收成長指引、SASE firewall billings 增速","threshold":"服務指引 ≤10% 且 SASE firewall billings 增速 <16%","action":"清倉","source_freq":"季報與法說","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"n":10,"text":"中國以外出現對美國資安產品的禁用令，或加密產品出口管制擴大","type":"風險","maps_to":"R4","metric":"政府禁用令與出口管制公告","threshold":"任一主要地區（歐洲、亞太）政府發布類似指令","action":"重估受影響營收；已有部位停止加碼","source_freq":"新聞與 10-K 風險因子（不定期）","date":null,"evidence_refs":["reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#3"]},{"n":11,"text":"Q4 2026 財報與 FY2027 財測公布後重跑判斷","type":"複審日期","maps_to":null,"metric":"全份判斷","threshold":"日期到","action":"重跑判斷","source_freq":"一次","date":"2027-02-15"}],"kill_metrics":[{"metric":"服務營收年增率","bear_threshold":"≤12%，連 2 季","window":"2027 Q1–Q2","source":"公司季報新聞稿","last_status":"warning"},{"metric":"產品營收年增率","bear_threshold":"<0%，連 2 季","window":"2027 全年","source":"公司季報新聞稿","last_status":"ok"},{"metric":"non-GAAP 總毛利率","bear_threshold":"<78%，連 2 季","window":"未來 4 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"短期遞延收入年增率","bear_threshold":"<12%","window":"每季","source":"公司季報與 10-Q","last_status":"ok"},{"metric":"證券集體訴訟進度","bear_threshold":"駁回動議被否決、進入證據開示","window":"2027 年","source":"N.D. Cal. 法院文件","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=57.7, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 情境的盈餘路徑靠「服務成長回到 15%」這一個關鍵假設，沒有量價算術，來源只有管理層口頭說法；歷史上同業和本股五年報酬不低於 Bull 隱含的年化 10.6%，所以報酬本身站得住。跑道的第二曲線有法說來源，但滲透率缺數據，且多為管理層口徑，這一項證據偏弱。三項都沒到 🔴，但都有缺口，Bull 依據只算勉強成立。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價 ≤116 美元（FY2027E 共識 30 倍）；或 2027 年 2 月 FY2027 財測服務營收成長 ≥15% 且 billings ≥15%，屆時價格上限為 FY2027E 36 倍（約 140 美元）'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價≤116 美元（FY2027E 共識 30 倍）；或 FY2027 財測服務營收成長≥15% 且 billings≥15%，上限 FY2027E 36 倍（約 140 美元）","exec_line":"任一條件觸發，先重跑判斷再進場。分兩批：首批不超過目標倉位一半，第二批等下一季服務營收年增 ≥14% 確認。價格先跌而服務證據未到時，分批反買、不停損；價格先漲而證據未到時，不追"},"reasoning":{"industry":"最新一季（2026 Q3）營收 20.78 億美元，年增 20.5%。產品營收 7.65 億美元，年增 37%；服務營收約 13.1 億美元，年增 13%（法說）；billings 23.36 億美元，年增 29%。非GAAP 毛利率 79.6%（法說），非GAAP 營益率 38.2%，GAAP 營益率 33.9%。全年財測第三度上調，營收 81.25–82.15 億美元、非GAAP EPS 3.54–3.58 美元；但 Q4 營收指引中點年增約 15%，成長在放慢。產品成長有一塊是價格：IR 會後更正，漲價約貢獻 billings 年增 10 個百分點；上半年又吃到低成本庫存，Q3 起兩者都在退。單點依賴：經銷商 A、B、C 分別占 FY2025 營收 28%、15%、12%，合計約 55%，六家經銷商占應收 67%。它們是通路不是終端需求，但收款與庫存集中在少數對手方；硬體約 85–95% 在台灣代工。產業時鐘判在過熱期（III），依據是硬體層的現象：漲價可轉嫁、零件交期拉長、同業提前拉貨、美國稅務誘因推動硬體採購，與股價無關。供需持久性分兩端：產品端週期性將反轉，服務與 SASE 端結構性持久。產業態勢三軸的裁決是雙向拉鋸：競爭端雲端交付與綑綁在加劇（10-K）；結構端 AI 威脅、OT 與主權需求在轉好；其他結構變數是中國禁用令與加密產品出口管制。","moat":"機制有兩層：自研 ASIC 帶來單位效能的成本優勢；單一 FortiOS 把防火牆、SD-WAN、SASE、OT 整合在同一台設備。安裝基數（台數市占約 55%）再帶動服務附加與轉換成本。方向用同業利潤率差來證：TTM 營益率 FTNT 32.7%，PANW 6.1%、CRWD −2.2%、OKTA 7.7%；FCF 利潤率 43.9%，也高於 PANW 35.8%。反例是這只有單期數字，同業 ROIC 與利差的多年趨勢事實表未涵蓋。執行力 9 分：全年 billings 財測年內第三度上調，100 萬美元以上訂單總值 +51%；研發密度 11.1%，只有 PANW 的一半，產品節奏仍沒落後。定價力 7 分：5–20% 的漲價已轉嫁，約貢獻 billings 10 個百分點；但 Q3 起漲幅趨穩，總毛利率年減 1.8 個百分點，CFO 自承漲價有上限、客戶預算有限，硬體與服務間折扣也變大。兩項合計 8 分，落在 B 級。最強的威脅是雲端交付 SASE 與大廠綑綁，列為生態攻擊，扣 1 分後仍在 B 級。報酬持續期方面，當期屬高利益率×高周轉（遞延收入大於營運資產），四檢查點兩綠兩黃；投入資本與折舊資料缺，增量 ROIC 與再投資率給不出數字。","growth":"FY2026 的成長來自量、價與小幅回購。產品 +37% 中，漲價約貢獻 billings 10 個百分點，另有上半年低成本庫存。FY2027 共識每股盈餘 3.88 美元只成長 8.7%，營收 91.15 億美元成長 11.5%，已反映價格紅利退場與利潤率收斂。共識 FY2026E→FY2028E 非GAAP 每股盈餘年化 10.9%（Koyfin，家數未揭露；FY2027 營收共識為 41 位分析師）。內生上界由需求端決定：資安支出 +12.2%、SASE firewall 市場約 +16%。共識落在上界之內，缺口為負，不需要靠倍數重估。若以 FY2025 GAAP 每股盈餘 2.42 美元為基期，三年年化約 22%；超出的部分來自 FY2026 營益率擴張與 GAAP／非GAAP 口徑差，不是可延續的成長。跑道判寬的依據是有來源的第二條曲線：OT billings Q3 約 +40%、Q2 逾 +55%，FortiSASE billings Q2 翻倍，AI 資料中心與主權方案在擴張。反例是核心防火牆台數市占已約 55%，而且第二曲線的數字多為管理層口徑。衰退信號亮兩項：一是毛利率年減（Q3 −1.8 個百分點、前九月 −1.0，推得上半年也是負的，但 Q2 單季值未收）；二是 FY2022–25 GAAP 每股盈餘年化 31.7%，遠高於營收的 15.5%。因此長期成長性與陷阱風險都判中等。","governance":"FY2025 自由現金流 22.26 億美元，淨利 18.53 億美元，轉換率 1.20。TTM FCF 利潤率 43.9%，高於 FY2022–25 的 31.6–32.8%；多出的部分來自 billings 遠快於營收（遞延收入累積）與上半年庫存去化，不宜外推。Q3 SBC 8,200 萬美元，占營收 3.9%；年化約 3.3 億美元，占市值約 0.3%。淨現金約 42.4 億美元（現金 47.99 億、債務 5.6 億）。董事會加碼回購授權約 12 億美元，剩餘額度 20 億美元。Q2 法說稱年初至今回購均價約 78 美元；在現價 136 美元回購，對 FY2026E 3.57 美元的盈餘殖利率只剩約 2.6%。近三年現金去向四分、債務到期與回購金額事實表未涵蓋。計分三項：併購報酬不適用（唯一收購不重大）；回購盈餘殖利率要對比十年期公債殖利率加 2%，但殖利率事實表未涵蓋，暫時無法判；股權淨稀釋低於 1.5%，通過。","valuation":"股價 136.08 美元，對 FY2026E 非GAAP 共識 3.57 美元是 38.1 倍，對 FY2027E 3.88 美元是 35.1 倍，對 FY2028E 4.39 美元約 31 倍。共識 FY2026E→FY2028E 年化 10.9%，PEG 約 3.5。歷史本益比 44.5 倍落在近四個年度端點的 89 分位，P/S 12.7 倍在 100 分位，EV/S 12.2 倍在 96 分位；但四個點不是五年分位，只能說位在自身區間高檔。Base 情境（FY2031E 每股盈餘 6.00 美元×27 倍＝162 美元）五年只漲約 19%，年化約 3.6%，加 1% 回購仍不到 5%；要到年化 8%，價格需約 116 美元。同業倍數事實表未涵蓋，終端倍數只能對照自身現值（FY2027E 35 倍）。賣方目標價分歧大：聚合站均值 115–160 美元，全距約 70–215 美元，最高對最低超過 3 倍，這壓低了本判斷的信心。","premortem":"三個視角的反證寫在反證紀錄：論點失敗（產品雙高峰回吐，加上服務附加率結構下滑）、論點成功但股東經濟變差（FCF 利潤率由 44% 回到 33%）、價格已反映太多（38 倍對 11% 成長）。五項壓力檢查過三項：淨現金遠大於債務、FCF 對淨利 1.2 倍、SBC 占營收 3.9% 低於 5%，三項皆過；空頭情境五年跌幅約 44% 超過 40%、最大經銷商占營收 28% 超過 25%，兩項不過。技術面：RSI 26.6 屬超賣，但 26 週仍漲 57.7%，代表股價今年 5 月前後約 86 美元、7 月底約 170 美元，波動極大；股價仍在 250 週均線上方，但長均線 13 週斜率只有 2.1%。歷史最大回撤與訴訟金額事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"FTNT 賺的是企業與政府的網路安全預算。先賣自研 ASIC 的 FortiGate 硬體（Q3 占營收約 37%），再按硬體價收 FortiCare 與 FortiGuard 服務費（約 63%）。錢卡在「裝在網路線上的那台防火牆」這個節點，服務附加率決定一台設備能收幾年錢。","moat":"護城河方向穩定（→）：執行面仍在擴大，定價面開始收斂，兩者相抵。","growth":"五年後跑道仍寬（🟢），但 FY2027 起成長會由 20% 降到約 10%：價格紅利退場，回到量與服務附加。","capital":"資本配置紀律好：自由現金流長期高於淨利、股權稀釋低、淨現金厚，回購授權再加 12 億美元；疑點在現價回購的報酬已遠低於年初。","valuation":"現價要求三件事：服務營收 2027 年起回到 15% 左右、產品不回吐、五年後仍值 30 倍以上。第一項我只信一半，所以判偏貴，不追。","how_wrong":"最可能看錯在太保守：若遞延收入與服務 billings 如期在 2027 年轉成營收，現價不算貴。另一面的錯誤是產品高峰回吐得比共識更深。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"股價 ≤116 美元（FY2027E 共識 30 倍）；或 2027 年 2 月 FY2027 財測服務營收成長 ≥15% 且 billings ≥15%，屆時價格上限為 FY2027E 36 倍（約 140 美元）","qc48_result":"pass","qc48_note":"Bull 情境的盈餘路徑靠「服務成長回到 15%」這一個關鍵假設，沒有量價算術，來源只有管理層口頭說法；歷史上同業和本股五年報酬不低於 Bull 隱含的年化 10.6%，所以報酬本身站得住。跑道的第二曲線有法說來源，但滲透率缺數據，且多為管理層口徑，這一項證據偏弱。三項都沒到 🔴，但都有缺口，Bull 依據只算勉強成立。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":136.08,"week26_return_pct":57.7,"consensus_rev_3m_pct":12.97,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 盈餘含上半年低成本庫存與漲價紅利，屬部分一次性；改以 FY2027E 3.88 美元前瞻錨定（35.1 倍），結論不變"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 初始財測","impact":"高","watch":"服務營收成長指引是否高於 13%、短期遞延收入年增率、產品營收指引"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"BMO、UBS、Barclays 投資人會議爐邊談話","impact":"低","watch":"管理層對 2027 服務成長與零件成本的口徑是否改變"}],"_projected_from":"v19"}
```
