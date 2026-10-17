你是 stock-analyst v20 的**散文層（prose）agent**，標的 IBKR（2026-10-18）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBKR_20261018/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：IBKR　日期：2026-10-18　archetype：None　前份裁決：2026-07-22　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1510B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（413B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（871B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（606B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（922B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（430B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（693B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1916B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3906B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2201B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1510           3843-5490      5 條（2–6 內）  
s3                  8000         413           5311-7587      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2399          8821-12601      5 條（2–6 內）  
s6                 11000         430          7399-10570      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         693           1965-2807      5 條（2–6 內）  
s10                 5000        1916           2159-3084      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2201           2000-2799      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3503B；至少需散文≈41.50KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70
−55
−55%
−47%
−45%
−38%
−35%
−35
−12.4%
−12%
−4%
0
0.0875
0.15
0.5%
0.6
0.60
0.67
0.69
0.73
0.73%
0.75
01
1%
1
1.36
1.39
1.4%
1.4
1.56
1.6
1.64
1.9%
2%
2
2.2
2.22
2.5
2.52
2.59
2.60
2.7
2.70
2.75
2.85
2.9
3.0
3
3%
3.05
3.10
3.20
3.2
3.26
3.35
3.5
3.6
3.62
3.71
3.88%
3.95
4%
4
4.25%
4.36
4.6
4.7%
4.72
5%
5
5.1
5.3
6%
6
06
6.0
6.02
6.2
07
7%
7
7.0%
7.5
08
8%
8
09
9
9%
10
10%
10.2
11%
11
11.4
11.4%
11.54
11.8
12%
12
12.4%
14
15
15%
15.6%
15.8
16
17%
17.04
18%
18
18.7%
18.8%
18.8
19
19%
19.14
20%
20
21
22
23%
23.1%
24
24%
25
25%
25.4
26
27%
27
27.2%
27.6
30
30%
30.6
30.63
31%
31.6
33%
35%
36%
36
37.6
39%
39.0%
41%
42
44
45
46%
47%
49
50
50%
51.2
53%
53.9
55
58
60%
63
$65
70
70%
71%
72
75
78%
80
81%
81.5%
$82
82
82.69
83%
83
85
86.5%
90.2%
94.42
95
100
100%
101
103
110
115
116
142%
142
150
150%
162
175
233
350
427
480
557.6
0875
2020
2025
2026
2027
2028
20261018
1,000
1,052
1,085
1,089
1,100
1,180
1,409
1,800
2,430
2,600
3,000
3,286
3,500
3,800
7,800
8,100
8,300
8,800
9,647
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
{"meta":{"ticker":"IBKR","date":"2026-10-18","schema":"v15.0","contract":"v19","company_name":"Interactive Brokers Group"},"oneliner":"全球低成本券商，帳戶年增 35%、稅前利益率 78%，生意品質一流；但現價對 FY2026 共識為 30.6 倍本益比，已計入三年約 19% 的盈餘成長。交易熱度退潮與利率轉向是主要下行，等 72 美元以下再談。","thesis":{"H":[{"id":"H1","text":"帳戶複利：全球主動投資人與介紹經紀商持續轉入，帳戶與客戶資產維持高成長","2y":"帳戶年增 >25%、客戶權益年增 >20%","5y":null,"10y":null,"threshold":"帳戶年增 >25%／客戶權益年增 >20%","source":"公司月度指標與季報；Q3 帳戶 557.6 萬戶（+35%）、客戶權益 9,647 億美元（+27%）","drift_rule":"帳戶年增連 2 季 <25% 為削弱；連 3 季 <20% 為反轉"},{"id":"H2","text":"淨利息收入由餘額驅動，跨利率週期仍能成長","2y":null,"5y":"淨利息收入年增 ≥10%，降息時由融資與現金餘額增量抵消","10y":null,"threshold":"淨利息收入年增 ≥10%，且季變動不連 2 季為負","source":"Q3 淨利息收入 11.54 億美元（+19%），同期 Fed funds 均值年減 63bp；CFO 揭露美元每 25bp 約 8,300 萬、非美元約 3,500 萬美元","drift_rule":"年增連 4 季 <10% 為削弱；連 6 季年增為負為反轉"},{"id":"H3","text":"盈餘兌現：交易熱度退潮下，共識兩年 EPS 仍能達成","2y":"FY2027 EPS ≥3.2 美元、FY2028 ≥3.6 美元","5y":null,"10y":null,"threshold":"FY2027 EPS ≥3.2 美元／FY2028 ≥3.6 美元","source":"Koyfin 共識 2026-10-08：FY2026 2.70、FY2027 3.26、FY2028 3.71 美元；近 3 個月 FY2026 上修 4.25%","drift_rule":"FY2027 共識連 2 季下修累計 ≥5% 為削弱；連 3 季累計 ≥10% 為反轉"}],"R":[{"id":"R1","text":"交易熱度退潮與定價壓力：DARTs 年增率由 6 月 53% 降至 9 月 6%，每單佣金年減 4%，股票成交量年減 24%；若轉為負成長，佣金走平，EPS 增速降到 10% 以下","h_ref":"H3","clock":"⚡","threshold":"月度 DARTs 年增連 3 個月 <0，或季度 DARTs 再季減 ≥10%","evidence_refs":["substitute_technology#2","competitive_share_entrants#2"]},{"id":"R2","text":"融資與信用週期：融資餘額 1,052 億美元仍高，全市場融資 7 月創紀錄單月降幅，公司信用損失備抵由 1,800 萬升到 2,600 萬美元；急跌時穿倉損失與餘額縮水同時出現","h_ref":"H2","clock":"🔥","threshold":"期末融資餘額季減 ≥15%，或信用損失備抵單季增加 ≥1 億美元","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"id":"R3","text":"利率路徑：淨利息收入約占營收 60%，美元每 25bp 約影響 8,300 萬、非美元約 3,500 萬美元；聯準會 9 月剛升息，降息已成尾部情境，但一旦急轉，敏感度最大","h_ref":"H2","clock":"🔥","threshold":"Fed funds 自 3.88% 累計降 ≥100bp，且淨利息收入連 2 季季減","evidence_refs":["end_markets#4"]},{"id":"R4","text":"跨境監管與法律：OFAC 制裁案 1,180 萬美元和解（2025 年 7 月）、平倉部位集體訴訟和解（聽證結果未查到）、國際營運的地緣與監管風險、日本帳戶遷移仍在與監管溝通","h_ref":"H1","clock":"🐢","threshold":"單一罰款 ≥1 億美元，或主要市場被限制開戶","evidence_refs":["major_events#0","regulatory_antitrust#2","reg_tariff_export#1","major_events#1","lawsuit_class_action#0","geo_supply_chain#0"]}],"single_thing":{"description":"危機型衝擊觸發聯準會急降息，Fed funds 於 12 個月內由 3.88% 降至 2% 以下","why_fatal":"淨利息收入約占淨營收 60%；公司揭露 Fed funds 每 25bp 對年化淨利息收入約 8,300 萬美元（9/30 基準），降至 2% 約少 6.2 億美元。急降息通常伴隨崩盤與融資去槓桿，餘額會同步縮水。這是 EPS 對單一變數最大的敏感度","if_happens":"EPS 回到 FY2025 的 2.2 美元附近，倍數壓縮，價格落入 Bear 區 45–55 美元；持有則減碼至三分之一","how_monitor":"FOMC 決議與 Fed funds 期貨；每季公司利率敏感度表；季度淨利息收入與融資餘額","probability":"約 10%（聯準會 9 月剛升息，12–24 個月內急轉到 2% 以下需要危機型衝擊）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":25.4,"peg_fy2":1.36,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.22,"FY2026E":2.7,"FY2027E":3.26,"FY2028E":3.71},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（A 類股）；共識為 Koyfin 2026-10-08 快照"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBKR_20261018/scenario.json","archetype":{"primary":"金融","secondary":"品質複利成長","confidence":"高","fingerprint":"券商：利差加佣金雙引擎、單一全球平台、高自動化低成本、無長期負債"},"industry":{"clock_phase":"II","sd_verdict_source":"帳戶與客戶資產屬結構性持久；交易量與融資餘額屬週期性，將反轉（FINRA 全市場融資餘額 7 月創紀錄單月降幅）","bargaining":{"up":"交易所與監管費用多數轉嫁客戶，上游無法擠壓利潤","down":"客戶為價格敏感的主動交易者，公司以最低收費定位，議價力來自成本","geo":"約 30% 利率敏感餘額為非美元；各地區營收占比事實表未涵蓋"},"profit_pool_dir":"零售券商利潤往規模化、低成本平台集中；公司營業利益率 86.5%，Robinhood 為 46%","tam_table":{"expanded":false,"reason":"事實表未涵蓋全球線上券商帳戶總數與滲透率，無法建 TAM 表；以帳戶、客戶權益與融資餘額增速代替份額擴張證據"}},"moat":{"mechanism":"單一全球多資產平台加高度自動化，帶來最低成本；介紹經紀商白牌接入後遷移成本高","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：帳戶年增 35%、介紹經紀商管道穩定、Daol 白牌上線。定價面小幅縮減：每單佣金 2.59 美元，年減 4%。兩者相抵為穩定。","peer_na_reason":"事實表無同業 ROIC 與 Schwab 營業利益率，改以 Robinhood 營業利益率與毛利率對照","threats":[{"level":"🟡","text":"零佣金環境的結構性定價壓力，加上 10-K 稱直接市場接取業務競爭將持續加劇；每單佣金已年減 4%","p":"25%","evidence_refs":["substitute_technology#2","competitive_share_entrants#2"]},{"level":"🟡","text":"加密原生平台推代幣化股票，若散戶轉向以代幣化方式持股，可能繞過傳統券商","p":"15%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"系統中斷：2020 年 12 月曾因第三方儲存系統故障多段停擺；全自動平台一旦停擺，客戶信任受損","p":"10%","evidence_refs":["geo_supply_chain#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多為同一個主動投資人；全球投資人想直接持有美國科技股並低成本換匯，屬「需要」而非「想要」。代理讀數：帳戶 557.6 萬戶（+35%）、客戶權益 9,647 億美元（+27%）"},{"item":"決策層級","level":"🟡","text":"在單一客戶層級換券商成本低，零佣金對手隨手可得；但對需要全球多資產接取、保證金與證券借貸的主動交易者難以替代。介紹經紀商整合後遷移成本高。流失率與續約率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟢","text":"交易所與監管費用轉嫁客戶，公司自營清算、託管與融資，拿走利差與佣金；稅前利益率 78% 顯示在價值鏈中分配位置強"},{"item":"社會容忍度","level":"🟡","text":"公司刻意壓低收費，未把價格推到經濟上限；但跨境經營依賴各地監管授權：OFAC 制裁案 1,180 萬美元和解、中國大陸整頓同業、日本帳戶遷移仍在與監管溝通，政策風險屬中等"}],"roiic":"約 23%（年化 Q3 淨利 53.9 億美元 ÷ 帳面權益 233 億美元，以平均報酬近似；增量口徑事實表未涵蓋）","reinvest_rate":"約 81%（年股息 0.60 美元 × 17.04 億股 ≈ 10.2 億美元，約占淨利 19%；無回購、無併購）","endo_ceiling":18.8,"formula_note":"內生上界＝23.1% × 81% ≈ 18.8%。券商盈餘成長主要由客戶餘額與利率驅動，自有資本多為監管緩衝（超額 142 億美元），上界只作參考，不代表資本的實際使用效率"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","IBKR":90.18,"SCHW":null,"HOOD":81.49,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","IBKR":86.5,"SCHW":null,"HOOD":46.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","IBKR":142.84,"SCHW":41.46,"HOOD":3.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","IBKR":null,"SCHW":null,"HOOD":19.59,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"SCHW","gm":null,"om":null,"fcf_margin":41.46,"rd_intensity":null,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"HOOD","gm":81.49,"om":46.03,"fcf_margin":3.61,"rd_intensity":19.59,"period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（帳戶與餘額）為主、利率為輔；無併購、無回購","runway_years":"事實表未涵蓋全球滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 18.8%（年化 ROE 約 23% × 再投資率約 81%）；三年共識 EPS 年複合約 18.7%，落在上界內","segments":{"expanded":false,"reason":"公司不分部揭露；收入由淨利息（約 60%）、佣金（約 31%）、其他費用（約 5%）組成，已寫在怎麼賺錢一題，利潤由利率與餘額決定，而非分部組合"},"decay_signals":["毛利率連兩季年減：未亮（稅前利益率 78%，連八季高於 70%）","核心市占縮減：未亮（帳戶年增 35%）","提價後銷量下滑：不適用（公司未提價）","EPS 成長顯著高於營收成長：未亮（FY2022–2025 EPS 年複合約 33%，營收約 35%）","FCF 對淨利低於 0.75：不適用（券商現金流含客戶餘額變動，FCF 利潤率 142% 無意義）","SBC 占營收高於 5% 且上升：資料缺口（事實表未涵蓋）","TAM 萎縮或被替代：未亮（代幣化屬增量威脅）","產業倍數系統性下移：資料缺口","維護性資本支出占 FCF 過高：不適用","停止投資且營收下滑：未亮"],"trap_rating":"🟢"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，資本回饋只有股息，回購為零，現金去向結構單純"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無重大併購；Q2 法說會稱標的多但無值得追求者","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"無回購計畫，資本回饋只走股息（年 0.60 美元）","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"事實表未涵蓋 SBC 與總股數年增率；A 類股數增加主要來自 LLC 單位轉換，不等於經濟稀釋","grade":"不過"}]},"valuation":{"basis":"Fwd P/E 為主；P/B 對 ROE 為輔（券商）","tier":"優質券商","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，無同業 Fwd P/E 或 P/B；終端倍數改以優質金融 18–22 倍區間與自身歷史端點對照，屬資料缺口"},"fwd_pe":30.6,"peg":1.64,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026 本益比 30.6 倍、FY2027 本益比 25.4 倍；三年 EPS 年複合 18.7%，PEG 約 1.6。trailing 本益比高於四個年度端點全部（只有四點，無法算五年分位，故分位留空）。P/B 約 6.0 倍，高於以 ROE 23%、成長 7% 推出的 5.3 倍。基準情境年化報酬約 5%，未到 8%；一年後以 FY2027 基準 EPS 3.20 美元 × 26 倍計約 83 美元，幾乎無上檔。結論：偏貴，未到泡沫","upside_short_pct":0.6,"upside_mid_pct":5.1},"trap_analysis":{"verdict":"🟢","label":"非價值陷阱：盈餘來自帳戶與餘額的實質成長，衰退信號未亮；風險在倍數與週期，不在生意變質"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"9 月 DARTs 只年增 6%（6 月為 53%）；每戶交易降到近期低點，且全客群皆然；全市場融資 7 月創紀錄單月降幅；公司客戶信用損失備抵由 1,800 萬升到 2,600 萬美元；利率每 25bp 約影響 8,300 萬美元淨利息收入","assumption":"帳戶與餘額的結構性成長足以抵消交易熱度與利率的週期反轉","consequence":"交易退潮、融資去槓桿、降息三者同時發生，佣金與淨利息收入同步下滑，倍數由 30 倍壓到 15–16 倍，五年後虧損接近 50%","ruling":"部分採納。帳戶年增 35%、客戶權益年增 27% 提供緩衝，但倍數壓縮風險真實；Bear 機率維持 25%，回撤區間下限取 −55%。與唯一致命點部分重疊（急降息是共同觸發），本條補上交易與信用兩條路徑","watch":"月度 DARTs 年增率、期末融資餘額季變動、信用損失備抵、Fed funds 路徑","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","end_markets#4"],"fact_refs":["f_kpi10_darts","f_kpi11","f_kpi6_yoy_19"]},{"view":"論點成功但股東經濟變差","evidence":"G&A 增加主因是廣告擴張；Q2 Peterffy 稱行銷報酬率與以往大致相同，Q3 稱 X 合作帶來的新客價值較高但數量較少；每單佣金年減 4%；零佣金環境下定價壓力屬結構性","assumption":"帳戶成長不需要靠持續加碼行銷與降價購買","consequence":"帳戶數照樣成長，但每戶佣金與獲客成本惡化，利益率從 78% 往下滑，股東拿到的每股盈餘成長慢於帳戶成長","ruling":"反駁為主。薪酬比 9%、G&A 僅 7,800 萬美元，廣告增量相對 19 億美元的季營收很小；每單佣金下滑公司歸因於單筆規模變小，屬未證、監測。若連兩季稅前利益率低於 70%，即代表本歸因被證偽","watch":"稅前利益率、每單佣金、G&A 占淨營收比","evidence_refs":["substitute_technology#2","competitive_share_entrants#2"],"fact_refs":["f_kpi3_gaap","f_kpi7_yoy_12"]},{"view":"價格已反映太多","evidence":"FY2026 本益比 30.6 倍；trailing 本益比高於四個年度端點全部；P/B 約 6.0 倍，高於以 ROE 推出的約 5.3 倍；10 月初賣方平均目標價約 80 美元，低於現價","assumption":"市場會持續為 35% 的帳戶成長與 78% 的利益率付 25 倍以上","consequence":"即使 EPS 照共識成長，倍數回到 22 倍也會吃掉大部分報酬，基準年化報酬只剩約 5%","ruling":"採納，這是本次的主要約束。股價雖已較前份下跌 12%，盈餘也上修，仍不足以讓基準報酬達到 8%","watch":"FY2027 共識 EPS 與股價的比值；股價 72 美元","evidence_refs":[],"fact_refs":["f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_price_at_dd"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 94.42 → 本次 82.69（-12.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=94.42","side_b":"本次 price_at_dd=82.69","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 94.42 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 94.42 美元：Bull 價 175、Bear 價 58，五年期望值 +39.0%，基準年化 7.0%，不對稱比 3.0","side_b":"本次情境、股價仍用 94.42 美元：Bull 價 162、Bear 價 51.2，五年期望值 +11.4%，基準年化 1.9%，不對稱比 1.56","ruling":"先換情境、股價不動：五年期望值少 27.6 個百分點，基準年化少 5.1 個百分點。不對稱比由 3.0 變為 1.56。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 94.42 美元：五年期望值 +11.4%，基準年化 1.9%，不對稱比 1.56","side_b":"本次情境、股價 82.69 美元：五年期望值 +27.2%，基準年化 4.7%，不對稱比 2.52","ruling":"再換股價、情境不動：起點價下跌 12.4%，五年期望值多 15.8 個百分點，基準年化多 2.7 個百分點，不對稱比由 1.56 升到 2.52。合計五年期望值比前份少 11.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"帳戶成長對交易熱度","cause":null,"prior_field":null,"side_a":"帳戶年增 35%、客戶權益年增 27%，創新高","side_b":"DARTs 季減 11%，9 月只年增 6%；法說會稱每戶交易降到近期低點且全客群皆然","ruling":"可調和，屬程度差異。帳戶是結構，交易熱度是週期；EPS 對淨利息收入的敏感度大於佣金，因此盈餘受交易退潮的傷害有限，但倍數會受影響","evidence_level":"高（公司季報與月度指標）","settle_metric":"季度 DARTs 季變動與帳戶年增率","if_then":["若 DARTs 季度再降 ≥10% 且帳戶年增仍 ≥25%，則維持論點、不追價","若帳戶年增也跌破 25%，則停止任何加碼計畫"],"evidence_refs":["end_markets#1","end_markets#2"]},{"axis":"融資餘額口徑","cause":null,"prior_field":null,"side_a":"期末融資餘額 1,052 億美元，低於 6 月底約 1,085–1,089 億美元，季減約 3%","side_b":"2026-10-15 法說會 Paul Brody 稱融資餘額年增 47%、季增 8%（應為平均餘額口徑）","ruling":"可調和：平均餘額與期末餘額的差異，表示季中衝高、季末回落，與全市場 7 月去槓桿方向一致。不可據此稱去槓桿已結束","evidence_level":"中（期末為新聞稿，平均為口述）","settle_metric":"Q3 10-Q 的平均與期末融資餘額","if_then":["若 Q4 期末融資餘額再季減 ≥5%，則把融資去槓桿視為進行中，Bear 機率上調至 30%","若回升至 1,100 億美元以上，則維持現有機率"],"evidence_refs":["financial_capital_credit_cycle#2","financial_capital_credit_cycle#1"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭面惡化：10-K 稱直接市場接取業務競爭將持續加劇，零佣金定價壓力屬結構性，每單佣金年減 4%","side_b":"結構面轉好：Fidelity 將對 1 億美元以下 RIA 設門檻，中國大陸整頓 Tiger、Futu 帶來轉戶；其他結構變數方面，利率由降轉升（聯準會 9 月中升息）","ruling":"雙向拉鋸。競爭壓力只壓每單價格，未壓帳戶份額；RIA 與轉戶是可觀察的份額窗口","evidence_level":"中","settle_metric":"帳戶年增率與每單佣金","if_then":["若每單佣金年減擴大到 10% 以上且帳戶增速同步放緩，則把護城河趨勢下修一檔"],"evidence_refs":["competitive_share_entrants#2","substitute_technology#2","supply_demand_durability#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：帳戶年增 35%、稅前利益率 78%、無長期負債；FY2027 本益比 25.4 倍對三年 19% 成長，PEG 約 1.4；聯準會 9 月升息對淨利息收入是順風；Fidelity 的 RIA 門檻提供份額窗口；股價已較前份下跌 12%，RSI 37.6","side_b":"等待方：基準情境終端 22 倍下年化報酬約 5%，未達 8%；倍數高於歷史端點；交易熱度正在退潮","ruling":"選等待方。依據是基準報酬未過 8%，這是價格問題，不是論點問題，兩邊可調和","evidence_level":"中","settle_metric":"股價對 FY2027 共識的倍數","if_then":["若股價 ≤72 美元（約 FY2027 共識 22 倍）且帳戶年增 ≥25%，則建首倉 2%","反向：若 FY2027 共識上修到 ≥3.5 美元而股價仍 ≤85 美元，同樣建首倉 2%","若股價先漲到 95 美元以上而 FY2027 共識未上修，則不追"],"evidence_refs":[]},{"axis":"賣方目標價分歧","cause":null,"prior_field":null,"side_a":"Benzinga 2026-10-07：16 位分析師平均目標價約 80 美元，全距 25–116 美元","side_b":"Benzinga 2026-09：12 位分析師平均約 110 美元；UBS 101 美元、Barclays 115 美元","ruling":"不可裁決，來源未說明差異原因。最高與最低相差逾 2.5 倍，因此本判斷的報酬估計信心下調，不引用共識目標價作進場依據","evidence_level":"低","settle_metric":"下一次賣方目標價彙整","if_then":["若主流券商目標價下修至現價以下且 EPS 共識同時下修，則 Bear 機率上調至 30%"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-07-21 Q2 法說會：Paul Brody 給出美元每 25bp 8,100 萬、非美元 3,800 萬的敏感度；Galik 把 DARTs 強勢部分歸因於環境；Peterffy 稱行銷報酬率與以往相同","side_b":"2026-10-15 Q3 法說會：敏感度改為 8,300 萬與 3,500 萬；Galik 把交易放緩歸因於 IPO 延後，並預期期中選舉帶來波動；Peterffy 稱 X 合作新客數量少","ruling":"說法一致、未改口；敏感度變動來自餘額基準。交易回升歸因於選舉波動屬未證，預登記：若 2026 年 11–12 月月度 DARTs 年增仍低於 10%，即視為此歸因被證偽","evidence_level":"中","settle_metric":"2026 年 11–12 月月度 DARTs 年增率","if_then":["若 11–12 月 DARTs 年增 <10%，則把 FY2027 基準 EPS 由 3.20 美元下修至 3.10 美元重跑"],"evidence_refs":[]},{"axis":"前份漂移：價格變動","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 94.42 美元，FY2026 EPS 約 2.60 美元，本益比約 36 倍，估值偏貴；機率 25/50/25；最大回撤 −45%","side_b":"本次股價 82.69 美元（−12%），FY2026 共識 2.70 美元，本益比 30.6 倍，估值仍偏貴；機率維持 25/50/25；回撤改為區間 −35%～−55%（涵蓋前份 −45%）","ruling":"價格下跌與盈餘上修共同壓低倍數，但未跨過合理門檻；裁決與角色由決策矩陣依本次輸入重算","evidence_level":"高","settle_metric":"FY2026 本益比","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：新證據","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5"],"side_a":"前份：訊號 B、陷阱低、護城河穩定、五年後跑道中等","side_b":"Q3 新資料（帳戶 +35%、稅前利益率 78%、每單佣金 −4%、9 月 DARTs +6%、RIA 稅務感知策略資產 3 億美元）未推翻任何一欄，四欄皆維持","ruling":"維持。新證據兩面都有，執行面擴大與定價面縮減相抵","evidence_level":"高","settle_metric":"帳戶年增率與每單佣金","if_then":[],"evidence_refs":["end_markets#2","substitute_technology#2"]},{"axis":"前份漂移：方法沿用","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份：金融類；循環位置未設","side_b":"本次沿用金融類券商尺（Fwd P/E 為主、P/B 對 ROE 為輔），不套循環股的位置判斷","ruling":"不變。公司盈餘雖受交易週期影響，但核心是餘額與利差，不屬商品循環","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重啟條件變動","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"Fwd PE 回 22-25x（~$65-75）或 NII 經降息週期證明韌性（量增抵消，如 Q2 margin loan +39% 抵 −70bp avg funds）；或回測 Bollinger 中軌 ~$82","side_b":"股價 ≤72 美元（基準年化報酬回到 8%，約 FY2027 共識 22 倍）且帳戶年增 ≥25%；或 FY2027 共識 EPS ≥3.5 美元而股價 ≤85 美元","ruling":"估值rearm 改為單一價格錨並綁定論點驗證。原因：主要約束是價格，觀望錨應為價格錨。移除技術線分支（價格已到 82 美元附近，但基準報酬仍不足）。移除淨利息收入韌性分支（Q3 已證明，不再是約束）。新增盈餘上修分支作為反向的加碼路徑","evidence_level":"中","settle_metric":"股價與 FY2027 共識","if_then":["觸及任一分支，則建首倉 2%，第二批等 Q4 財報確認帳戶年增 ≥25% 再加碼"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"Single Thing：危機型衝擊觸發聯準會急降息，Fed funds 於 12 個月內降至 2% 以下","ruling":"新設。淨利息收入約占營收 60%，利率是 EPS 對單一變數最大的敏感度，大於佣金波動","evidence_level":"高（公司揭露的敏感度）","settle_metric":"Fed funds 有效利率","if_then":["若發生，則減碼至三分之一"],"evidence_refs":["end_markets#4"]},{"axis":"kill 指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill 指標（null）","side_b":"新設五條：帳戶年增連 2 季 <20%、淨利息收入年增轉負且連 2 季季減、Fed funds 12 個月內降至 2% 以下、月度 DARTs 年增連 3 個月 <0、信用損失備抵單季增 ≥1 億美元","ruling":"補上前份缺少的減碼與清倉門檻，持有時以此執行","evidence_level":"中","settle_metric":"各指標","if_then":["帳戶與淨利息收入兩條同時觸發，則清倉；任一條觸發，則減碼至半倉"],"evidence_refs":["financial_capital_credit_cycle#0"]},{"axis":"風險假設改寫","cause":"新證據","prior_field":["thesis.R"],"side_a":"前份 R1：聯準會 2026H2–2027 加速降息 100–150bp，壓淨利息收入","side_b":"Q3 法說會 Paul Brody 稱聯準會 9 月中升息、多國央行 9 月升息，敏感度基準 Fed funds 3.88%；降息風險由主情境降為尾部，改寫為利率路徑風險與唯一致命點","ruling":"利率方向已由降轉升，前份的降息主情境被新證據推翻；風險保留，但門檻改為累計降 ≥100bp 且淨利息收入連 2 季季減","evidence_level":"高","settle_metric":"Fed funds 與季度淨利息收入","if_then":["若 12 個月內累計降息 ≥100bp 且淨利息收入連 2 季季減，則減碼至半倉"],"evidence_refs":["end_markets#4"]},{"axis":"前份觸發器已發火","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份重啟條件中的「淨利息收入經降息證明韌性」分支，以及「回測 82 美元附近」分支","side_b":"Q3 淨利息收入年增 19%，同期 Fed funds 均值年減 63bp，量增已抵消；股價 82.69 美元，落在前份技術線附近。兩分支已發火","ruling":"依前份規則，觸發後要重跑判斷而非直接建倉；本次重跑後基準年化報酬約 5%，仍未達 8%，因此不據此進場","evidence_level":"高","settle_metric":"基準情境年化報酬","if_then":["若股價 ≤72 美元，則建首倉 2%"],"evidence_refs":["end_markets#0"]}],"triggers":[{"n":1,"text":"帳戶年增率跌破 25%，連續 2 季","type":"假設驗證","maps_to":"H1","metric":"客戶帳戶年增率","threshold":"連 2 季 <25%","action":"停止加碼；連 3 季 <20% 則減碼至半倉","source_freq":"公司月度指標／季報","date":null,"evidence_refs":[]},{"n":2,"text":"交易熱度轉為負成長：月度 DARTs 年增率連 3 個月為負","type":"風險","maps_to":"R1","metric":"月度 DARTs 年增率","threshold":"連 3 個月 <0","action":"未持有則不追；持有則減碼至半倉","source_freq":"公司月度指標","date":null,"evidence_refs":["substitute_technology#2","competitive_share_entrants#2"]},{"n":3,"text":"融資去槓桿或信用損失擴大","type":"風險","maps_to":"R2","metric":"期末融資餘額季變動／信用損失備抵","threshold":"融資餘額季減 ≥15% 或備抵單季增加 ≥1 億美元","action":"減碼至半倉","source_freq":"季報與 10-Q","date":null,"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"n":4,"text":"危機型衝擊觸發聯準會急降息，Fed funds 12 個月內降至 2% 以下","type":"Single Thing","maps_to":"R3","metric":"Fed funds 有效利率","threshold":"12 個月內 ≤2%（9/30 為 3.88%）","action":"減碼至三分之一","source_freq":"FOMC 每次會議","date":null,"evidence_refs":["end_markets#4"]},{"n":5,"text":"股價回到基準報酬 8% 的位置，且帳戶成長仍成立","type":"估值rearm","maps_to":"H3","metric":"股價與帳戶年增率","threshold":"股價 ≤72 美元且帳戶年增 ≥25%","action":"建首倉 2%","source_freq":"每日股價／月度指標","date":null,"evidence_refs":[]},{"n":6,"text":"盈餘上修而股價未跟上","type":"加碼","maps_to":"H3","metric":"FY2027 共識 EPS","threshold":"≥3.5 美元且股價 ≤85 美元","action":"建首倉 2%，Q4 財報確認後加碼至 4%","source_freq":"Koyfin 月度快照","date":null,"evidence_refs":[]},{"n":7,"text":"監管或法律事件升級：單一罰款金額大，或主要市場被限制開戶","type":"風險","maps_to":"R4","metric":"監管罰款金額／主要市場開戶限制","threshold":"單一罰款 ≥1 億美元，或日本、中國客戶群被限制開戶","action":"停止加碼；涉及刑事程序則清倉","source_freq":"8-K／10-Q 法律程序段","date":null,"evidence_refs":["major_events#0","regulatory_antitrust#2","reg_tariff_export#1","major_events#1","lawsuit_class_action#0","geo_supply_chain#0"]},{"n":8,"text":"Q4 財報複審：帳戶、淨利息收入、DARTs 與選舉波動歸因驗證","type":"複審日期","maps_to":"H2","metric":"季報","threshold":null,"action":"依觸發器 1–7 執行","source_freq":"季報","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"客戶帳戶年增率","bear_threshold":"連 2 季 <20%","window":"2 季","source":"公司月度指標與季報","last_status":"ok"},{"metric":"季度淨利息收入","bear_threshold":"年增轉負且連 2 季季減","window":"2 季","source":"季報 8-K","last_status":"ok"},{"metric":"Fed funds 有效利率","bear_threshold":"12 個月內降至 2% 以下","window":"12 個月","source":"FOMC 決議","last_status":"ok"},{"metric":"月度 DARTs 年增率","bear_threshold":"連 3 個月 <0","window":"3 個月","source":"公司月度指標","last_status":"warning"},{"metric":"客戶信用損失備抵","bear_threshold":"單季增加 ≥1 億美元","window":"1 季","source":"10-Q","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=1.39, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價 ≤72 美元（基準年化報酬回到 8%，約 FY2027 共識 22 倍）且帳戶年增 ≥25%；或 FY2027 共識 EPS ≥3.5 美元而股價 ≤85 美元","exec_line":"未持有：不追，等重啟條件。觸及後分兩批，首批 2%，第二批等 Q4 財報確認帳戶年增 ≥25% 再加碼至 4%。已持有：不加碼，按 kill 指標執行減碼與清倉"},"reasoning":{"industry":"Q3 GAAP 淨營收 19.14 億美元，年增 15.6%。其中淨利息收入 11.54 億美元（+19%），佣金 6.02 億美元（+12%），其他費用與服務 8,800 萬美元（+33%）。稅前利益率 78%，連續八季高於 70%；薪酬只占調整後淨收入 9%，員工 3,286 人服務 557.6 萬戶。產業時鐘判在 II 擴張：帳戶年增 35%、客戶權益年增 27%、融資餘額年增 36%，仍在擴張；但交易熱度自 2026 年 6 月高點降溫（DARTs 年增率由 6 月 53% 降到 9 月 6%，法說會稱每戶交易降到近期低點且全客群皆然），屬擴張後段。供需持久性分兩層：帳戶與客戶資產屬結構性持久，交易量與融資餘額屬週期性、將隨市場熱度反轉。議價權：上游交易所與監管費用多數轉嫁客戶（Q3 SEC 規費 3,000 萬美元同時推高佣金與成本，不影響利潤）；下游客戶價格敏感，公司的議價力來自最低成本，而不是加價能力。單點依賴：無單一客戶集中（10-K 稱無營業常規以外的重大信用集中），真正的集中風險是利率——每 25bp 對年化淨利息收入約 8,300 萬美元（美元）加 3,500 萬美元（非美元）。","moat":"機制只有一條：單一全球平台加上高度自動化，使每多服務一戶的成本趨近於零，進而能以最低價搶客並維持 78% 稅前利益率。可證方向的同業對照：營業利益率公司 86.5%、Robinhood 46%，毛利率 90.2% 對 81.5%；事實表無同業 ROIC，也無 Schwab 的營業利益率。執行面擴大的證據：帳戶年增 35%；介紹經紀商管道連續數季穩定上線（韓國 Daol 白牌平台 Q3 上線）；夜盤交易量由 350 萬筆增至逾 1,000 萬筆。定價面縮減的證據：每單佣金年減 4%，公司歸因於單筆規模變小；零佣金環境下定價壓力屬結構性。報酬持續期方面，年化 ROE 約 23%，判在高利益率、低周轉象限（資產 2,430 億美元、權益 233 億美元）；四個檢查點兩綠兩黃。再投資方面，股息約占淨利 19%、無回購，再投資率約 81%，內生上界約 18.8%；但超額監管資本 142 億美元遠高於需求 36 億美元，保留盈餘多數並未被業務使用，這個上界高估了實際可用的再投資機會。","growth":"成長來源以量為主：帳戶、客戶資產、融資與現金餘額。利率屬價格因素，為輔；沒有併購，也沒有回購。三年共識 EPS 由 FY2025 實際 2.22 美元到 FY2028 3.71 美元，年複合約 18.7%（Koyfin 2026-10-08 快照），與內生上界約 18.8% 幾乎重合，缺口約為零，不需要靠倍數重估解釋。但這組盈餘對交易熱度與利率高度敏感：Q2 DARTs 480 萬筆、年增 36%，Q3 降到 427 萬筆、年增 18%，9 月只剩年增 6%。管理層把 Q2 的熱度部分歸因於 IPO 與市場環境（2026-07-21 法說會 Galik），Q3 又以期中選舉波動作為回升理由，屬未證歸因。第二通路：Fidelity 2027 年中對小型 RIA 設門檻，公司自認是明顯的承接者；介紹經紀商管道與前兩季相近；預測市場與 AI 自主交易仍在早期。滲透率事實表未涵蓋，跑道年數無法量化。","governance":"季股息由 0.0875 美元調升至 0.15 美元（+71%），年化 0.60 美元，以現價計殖利率約 0.73%。Peterffy 說明股息依市值 0.5%–1% 指引，此前落後所以補上，並稱想像不到會減息的情境（2026-10-15 法說會）。公司權益年增 19% 至 233 億美元，無長期負債。6 月底各營運子公司合計超額監管資本 142 億美元。Q2 法說會稱扣除緩衝後超額資本約 103 億美元，併購標的雖多但無值得追求者。FCF 對淨利的轉換率在券商不具意義：FCF 利潤率 142% 來自客戶餘額流入，不是自由現金。SBC 與股數年增率事實表未涵蓋，稀釋項目無法判定通過與否。","valuation":"現價 82.69 美元，對 FY2026 共識 EPS 2.70 美元為 30.6 倍，對 FY2027 共識 3.26 美元為 25.4 倍；trailing 本益比 31.6 倍，高於事實表四個年度端點的全部（分位 100，非五年分位）。券商尺：帳面權益 233 億美元，市值 1,409 億美元，P/B 約 6.0 倍；年化 ROE 約 23%，以資金成本 10%、長期成長 7% 推出合理 P/B 約 5.3 倍，現價略高；但長期成長若取 8%，合理值升到 7.5 倍，結論對成長假設很敏感。基準情境終端 22 倍下，年化報酬約 5%，未達 8%。賣方目標價分歧大：10 月初 Benzinga 平均約 80 美元（全距 25–116 美元），9 月頁面平均約 110 美元，最高與最低相差逾 2.5 倍，因此本判斷的報酬估計信心下調。近 3 個月 FY2026 共識上修 4.25%，盈餘方向向上，壓力在倍數不在盈餘。","premortem":"主要風險有兩個方向。其一，交易熱度退潮與融資去槓桿同時發生：9 月 DARTs 只年增 6%，股票成交量年減 24%，全市場融資 7 月創紀錄單月降幅，公司客戶信用損失備抵由 1,800 萬升到 2,600 萬美元。其二，聯準會若從 9 月升息急轉為降息，淨利息收入的敏感度會反向放大。管理層迴避紀錄：Q2 被問融資快速成長是否過度承險，只答持續監控、感到安心，未給任何指標；被問帳戶成長能否結構性高於 20%，拒絕承諾；被問區域與韓國貢獻，不拆分。Q3 被問其他國家擴張計畫，拒答。動能面：RSI 37.6，26 週報酬 1.4%，沒有過熱。"},"plain":{"six":{"how_it_makes_money":"賺全球主動投資人與介紹經紀商的錢，錢卡在兩個節點：客戶融資與客戶現金的利差（淨利息收入約占淨營收 60%），以及交易佣金（約 31%）。","moat":"穩定：低成本自動化的規模優勢在執行面仍在擴大，但每單佣金下滑讓定價面小幅縮減，兩者相抵。","growth":"五年後跑道中等：帳戶增速會隨基數放大自然放緩；RIA 與介紹經紀商是看得見的第二通路，但規模仍小（RIA 稅務感知策略資產約 3 億美元），尚不足以判為下一條成長曲線。","capital":"資本配置以保留盈餘擴充資本加股息為主：股息改按市值 0.5%–1% 的指引大幅調升，無回購、無併購、無長期負債。","valuation":"現價要求 FY2026–2028 EPS 年增約 19% 兌現，且倍數守在 25 倍上下；盈餘路徑可信，倍數不可信，結論偏貴。","how_wrong":"最可能看錯的地方：把 2026 年中的交易熱度與融資高峰當成長期基準，而倍數早已按這個基準定價。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"股價 ≤72 美元（約 FY2027 共識 22 倍）且帳戶年增 ≥25%；或 FY2027 共識 EPS 上修至 ≥3.5 美元而股價 ≤85 美元","trap":"🟢","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"金融","price_at_dd":82.69,"week26_return_pct":1.39,"consensus_rev_3m_pct":4.25,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"EPS 分母無一次性爭議（GAAP 0.69 美元與調整後 0.67 美元的差異來自貨幣分散策略損益）。營收倍數分母口徑不一：年度營收含總利息收入，共識為淨營收，P/S 與 EV/S 不作估值錨"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉，管理層預期波動上升帶動交易","impact":"中","watch":"11–12 月月度 DARTs 年增率是否回到 10% 以上"},{"date":"2026-12","date_precision":"month","type":"macro","event":"FOMC 利率決議（9 月升息後的路徑）","impact":"高","watch":"Fed funds 方向與淨利息收入敏感度"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"OCC 全國信託銀行執照（Q2 法說會稱計畫年底前完成上線）","impact":"中","watch":"是否如期取得正式核准"},{"date":"2026-11","date_precision":"month","type":"product","event":"Cboe 單一公司 KPI 二元期權上線，公司接入","impact":"低","watch":"預測市場交易量"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 財報","impact":"高","watch":"帳戶年增、淨利息收入、DARTs、期末融資餘額"},{"date":"2027-06","date_precision":"quarter","type":"other","event":"Fidelity 對 1 億美元以下 RIA 的門檻生效","impact":"中","watch":"RIA 帳戶與資產轉入"}],"_projected_from":"v19"}
```
