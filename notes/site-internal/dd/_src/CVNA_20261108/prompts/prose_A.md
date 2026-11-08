你是 stock-analyst v20 的**散文層（prose）agent**，標的 CVNA（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：CVNA　日期：2026-11-08　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1200B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（582B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（810B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1314B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1026B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（405B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（764B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2376B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3724B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2579B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1200           4060-5800      5 條（2–6 內）  
s3                  8000         582           5193-7418      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3150          8295-11850      5 條（2–6 內）  
s6                 11000         405          7416-10595      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         764           1915-2736      5 條（2–6 內）  
s10                 5000        2376           1837-2624      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2579           2000-2421      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4398B；至少需散文≈40.60KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70%
−70
−61%
−54%
−45%
−45
−18.36
−11.06%
−5.61
−0.7%
0
0.09%
0.3%
0.39
0.47
0.48
0.75
0.79
0.8
0.95
01
1
1.02
1.35
1.40
1.42
1.45
1.5%
1.52
1.55
1.6
1.60
1.6%
1.69
1.70
1.75
1.9
2.0
2.00
2
02
2.05
2.08
2.12
2.3
2.3%
2.30
2.60
2.6
2.73
3%
03
3
3.05
3.2
3.30
3.4
3.55
3.75
4
4%
4.00
4.05%
4.15
4.3%
4.83
05
5.0
5%
5
5.2
5.61%
5.9
5.94
06
6
6%
6.2
6.9
07
7
7%
7.4%
7.5%
7.5
7.8%
8%
8
08
8.74%
8.9%
9
9%
9.5%
10
10%
10.7
11
11%
11.5%
12
12%
12.5%
13
13.5%
14
14.2%
14.8%
15
15%
15.2
16.2%
16.6
17.3%
18%
18
19%
19.04%
20
20%
20.63%
21%
21.9%
22
22%
23
23%
24%
24
25%
25
26
26%
27%
28
28.80
29%
29
30%
30
32
33
33.90
34.0%
34%
34.7
35%
35.37
36%
38
39%
40
40%
42%
46%
48
48.4
49
50
50%
54%
59
61%
62.82
63%
70
73.57
74%
75
76%
76.4%
77.9
80.4
84.14
85
85.8
86
87
87.4
90
90.4
100
100%
104
118%
120
122
130
150%
185
196
200
220
250
260
299
300
310
394%
400
410
455
594
598
705
889
2022
2025
2026
2027
2028
2029
2031
2036
20261108
1,000
1,097.6
1,302
1,487
1,882
2,030
2,040
2,200
2,500
2,733
3,200
3,284
3,625
3,680
3,830
4,500
4,620
49,000
5,300
6,144
7,093
8,040
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
{"meta":{"ticker":"CVNA","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Carvana Co."},"oneliner":"Carvana 在持平的二手車市場繳出 39% 的台數成長，營益率約為傳統車商兩倍。但現價是 FY2026E 的 48.4 倍，基本情境五年年化只有約 7%，其他收入又相當於 EBITDA 的 74%，等 59 美元以下再談。","thesis":{"H":[{"id":"H1","text":"產能擴張撐得住台數成長，FY2027 年增約 26%，FY2028 約 21%。","2y":"FY2028 零售台數約 122 萬台","5y":null,"10y":null,"threshold":"FY2027 年增不低於 25%，FY2028 不低於 20%","source":"公司季報零售台數；法說會的整備產量與上架庫存說明","drift_rule":"TTM 台數偏離路徑 5% 以上連兩季為削弱，10% 以上連三季為反轉"},{"id":"H2","text":"費用槓桿讓每台獲利恢復成長，GAAP 營益率逐年上升。","2y":null,"5y":"FY2031 GAAP 營益率 11.5%","10y":null,"threshold":"FY2028 不低於 10%，FY2031 不低於 11.5%","source":"公司季報 GAAP 營業利益與營收","drift_rule":"TTM 營益率偏離路徑 5% 以上連四季為削弱，10% 以上連六季為反轉"},{"id":"H3","text":"規模優勢延續，公司走到年賣 300 萬台。","2y":null,"5y":null,"10y":"2036 年前年賣 300 萬台，約占全美二手車總量 8%","threshold":"FY2031 年賣不少於 185 萬台","source":"公司年報台數；Cox Automotive 產業總量","drift_rule":"跨兩個年度落後路徑為削弱，跨三個年度為反轉"}],"R":[{"id":"R1","text":"利率、信用或貸款買方需求轉差，壓低融資收益。","h_ref":"H2","clock":"⚡","threshold":"每台其他收入低於 2,200 美元連兩季","evidence_refs":[]},{"id":"R2","text":"整備與人力擴張跟不上，新場站成本偏高，成長放慢或費用上升。","h_ref":"H1","clock":"🔥","threshold":"上架庫存成長低於銷量成長連四季，或台數年增低於 20% 連兩季","evidence_refs":[]},{"id":"R3","text":"批發車價處高點、供給偏緊，加上油價與關稅，車源與運輸成本吸收不了。Cox 與公司都以環境穩定為前提。","h_ref":"H2","clock":"🔥","threshold":"零售 GPU 低於 3,200 美元連兩季","evidence_refs":["supply_demand_durability#3","reg_tariff_export#0"]},{"id":"R4","text":"空方報告衍生的法律風險與 2022 年集體訴訟，金額與時程未知。","h_ref":"H3","clock":"🐢","threshold":"集體認證通過且和解超過 5 億美元，或刑事介入","evidence_refs":["major_events#2","major_events#3","lawsuit_class_action#0"]}],"single_thing":{"description":"貸款銷售管道中斷：ABS 市場或整批貸款買方在一季內拒買，或要求的價差使利得接近歸零。","why_fatal":"Q3 其他收入 5.94 億美元，相當於調整後 EBITDA 的 74%。每台少 1,000 美元，FY2031 基本 EPS 約少 0.95 美元，約 24%；相比之下營益率每 1 個百分點約 9%，倍數每 1 倍約 4%。它是最大的單一敏感度。","if_happens":"貸款留在帳上，營運資金吸走現金，0.8 倍淨負債比快速惡化，成長被迫放慢。FY2022 的 FCF −18.36 億美元、營益率 −11.06% 是前例。此時應清倉，不等下一季確認。","how_monitor":"每季其他收入÷零售台數；每月 ABS 發行規模與是否縮量；法說會揭露的貸款買方變動。","probability":"12 至 24 個月約 10%，判斷值；貸款買方集中度事實表未涵蓋，可能低估。"}},"appendix_a":{"growth_durability":8,"quality_score":7.5,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":34.7,"peg_fy2":1.02,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.69,"FY2026E":1.52,"FY2027E":2.12,"FY2028E":2.73},"fy_end_month":12,"eps_basis":"FY2025A 為 yfinance 稀釋 EPS；FY2026E 至 FY2028E 為 Koyfin 共識，GAAP 或調整後未標明，EPS 家數未載明。FY2025A 含不會重複的成分，成長判斷改以 FY2026E 為基期。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVNA_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"已獲利、高成長、低滲透率的線上零售，獲利對利率與消費信貸敏感"},"industry":{"clock_phase":"IV","sd_verdict_source":"需求結構性持久，量的壓力屬週期性。Cox 預估 2026 年零售二手車 −0.7%，CFO 稱 Q2 產業年減約 4 點，批發價卻在近三年高點，屬供給偏緊造成的量縮，不是需求崩塌。2027 年租賃退場車回升（次級來源轉述 Manheim）會緩解供給。","bargaining":{"up":"車源來自消費者、拍賣與市集夥伴，分散；各來源占比事實表未涵蓋。","down":"購車人極度分散，真正有議價權的下游是貸款買方與 ABS 投資人。","geo":"主要在美國單一市場。"},"profit_pool_dir":"CEO 稱車商淨利率 25 至 30 年大致持平。利潤往規模化線上業者移動的證據是 CVNA 營益率約為 AN、LAD 的兩倍以上，五年利潤池占比事實表未涵蓋。","tam_table":[{"item":"全美二手車總量（Cox 2026）","value":"3,830 萬台"},{"item":"全美零售二手車（Cox 2026）","value":"2,030 萬至 2,040 萬台"},{"item":"CVNA 年化台數（Q3）","value":"87 萬台"},{"item":"滲透率","value":"占總量 2.3%，占零售二手 4.3%。管理層說的兩個百分點出頭，分母是總量"},{"item":"300 萬台目標占比","value":"占總量 7.8%，占零售二手 14.8%"},{"item":"營業利益池五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"垂直整合的整備與物流網路加上單一庫存池，規模帶來更多選車、更快到貨與更低資金成本。","execution":9,"pricing":6,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：連續 11 季台數成長與 EBITDA 利潤率業界第一，NPS 兩年升 9 點，到貨快 2 天。定價面穩定：每台總毛利年減 410 美元，主因是讓利給客戶與利率上升，零售 GPU 反而年增 85 美元。可能看錯的地方：讓利結束後每台獲利若仍不回升，定價面要改判縮減。","peer_na_reason":"同業 ROIC 事實表未涵蓋，以份額與營益率差替代。","threats":[{"level":"🟡","text":"新進者持續進場：Amazon、Costco、車廠直售列在 10-K，Hertz 2025 年推線上二手車，目前都還沒有規模證據。","p":"30%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#3"]},{"level":"🟡","text":"AI 代理比價對零售端透明度有利，但會提高貸款提前清償與利率比價。CEO 在 2026-10-28 也承認提前清償可能上升；產業人士預測 2029 年常態化，屬預測。","p":"30%","evidence_refs":["substitute_technology#2"]},{"level":"🟡","text":"公司依賴第三方生成式 AI 平台，表現不如預期時會影響轉換率與客服，屬營運風險，不是替代威脅。","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者與付款者多為同一人，買車需求可延後但不會消失。美國零售二手車約 2,030 萬台，新車均價逾 49,000 美元，推動需求轉向二手。"},{"item":"決策層級","level":"🟡","text":"每次購車都是單筆決策，沒有轉換成本，也沒有回購率資料。替代性靠當地選車量與到貨速度維持，CEO 稱多數大都會庫存已超過當地車商總和，此為公司說法。"},{"item":"價值鏈分配","level":"🟡","text":"其他收入相當於 EBITDA 的 74%，獲利有很大一段要經過貸款買方與 ABS 投資人。公司又主動把利率讓給客戶，這段價值的分配權不完全在公司手上。"},{"item":"社會容忍度","level":"🟡","text":"車貸受 CFPB、FTC 與各州監管，獲利若過度依賴貸款會招致政策與輿論壓力。FTC 費用揭露方向目前對公司有利，SEC 調查已結案且不建議執法。"}],"roiic":50,"reinvest_rate":40,"endo_ceiling":20,"formula_note":"再投資率以 FY2025（稅後營業利益−FCF）÷稅後營業利益代理：營業利益 1,882 百萬美元×0.79＝1,487 百萬美元，減 FCF 889 百萬美元，得 40%；未加回利息，會高估再投資。實現增量報酬＝兩年稅後營業利益差 705 百萬美元÷598 百萬美元＝118%，受既有產能填滿推高。平均資本報酬約 23%。前瞻 50% 為判斷值。內生上界＝50%×40%＝20%，單位為百分比。稅率 21% 為假設；折舊、營運資金與收購淨額事實表未涵蓋，所以無法用標準公式。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","CVNA":19.04,"KMX":10.31,"AN":17.73,"LAD":15.14,"ACVA":50.98,"unit":"%"},{"metric":"營業利益率","CVNA":8.74,"KMX":-1.4,"AN":4.28,"LAD":3.59,"ACVA":-7.09,"unit":"%"},{"metric":"FCF 利潤率","CVNA":4.05,"KMX":4.15,"AN":0.8,"LAD":-1.12,"ACVA":-0.87,"unit":"%"}],"competitors":[{"name":"KMX","gm":10.31,"om":-1.4,"fcf_margin":4.15,"strategy_note":"規模最接近的二手車對手，線上化追趕尚未轉成獲利，CEO 表示看不出對 CVNA 有明顯影響。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"AN","gm":17.73,"om":4.28,"fcf_margin":0.8,"strategy_note":"特許經銷模式毛利率接近 CVNA，但費用結構重，營益率約只有一半。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"LAD","gm":15.14,"om":3.59,"fcf_margin":-1.12,"strategy_note":"靠併購擴張，自由現金流為負，資本路徑與 CVNA 相反。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ACVA","gm":50.98,"om":-7.09,"fcf_margin":-0.87,"strategy_note":"批發拍賣平台，只在批發端部分重疊，對零售端不構成直接威脅。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量約 76%，價格與組合約 24%，併購與回購幾乎沒有貢獻。","runway_years":"5.9（維持 39% 成長）至 10.7（平均 20% 成長）","runway_post_y5":"🟢","endo_ceiling_basis":"沿用護城河段推導：前瞻增量報酬 50%×再投資率 40%＝20%。","segments":[{"item":"零售","value":"Q3 占營收 76.4%，年增 54%"},{"item":"批發","value":"Q3 占營收 16.2%，年增 11%"},{"item":"其他","value":"Q3 占營收 7.4%，年增 25%，相當於調整後 EBITDA 的 74%"},{"item":"新車","value":"收購 Stellantis 經銷店，CEO 稱目前獲利，占比事實表未涵蓋"}],"decay_signals":["毛利率連兩季年減：亮燈。Q2 每台毛利年減 455 美元，Q3 年減 410 美元，TTM 毛利率 19.04% 低於 FY2025 的 20.63%。","EPS 成長高於營收成長超過 5 個百分點：亮燈。FY2026E 到 FY2027E 的 EPS 增 39%，營收增 26%。","FCF／淨利連兩年低於 0.75：未亮，但接近。FY2025 為 63%，FY2024 為 394%，FY2026 尚未結束。","核心市占縮減、提價後銷量下滑、SBC 偏高、停止投資新產能：未亮。","TAM 萎縮或被替代：未亮。Cox 預估 2026 年零售二手車 −0.7%，屬持平。","產業倍數下移、維護性資本支出占比：事實表未涵蓋。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能與份額，不靠併購或回購，且近三年現金去向細項事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月只有七家 Stellantis 經銷店的小型收購，金額事實表未涵蓋，無法計算已實現報酬。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"公司沒有回購，CFO 表示現金優先投資業務。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 年化約 1 億美元，除以市值 1,097.6 億美元，約 0.09%，低於 1.5%。逐年股數事實表未涵蓋。","grade":"過"}]},"valuation":{"basis":"Forward P/E，分母為 FY2026E 共識 EPS 1.52 美元","tier":"高成長線上零售，事實表沒有同層同業倍數","peers":{"expanded":false,"reason":"事實表的同業表只有毛利率、營益率與 FCF 利潤率，沒有同業倍數，無法做跨公司估值對照，這是資料缺口。"},"fwd_pe":48.4,"peg":1.42,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"偏貴。Forward P/E 48.4 倍÷FY2026E 到 FY2028E 年化 34.0%，PEG 1.42；改用基本情境五年年化約 21%，PEG 約 2.3，低 PEG 來自近兩年的成長高峰。五年分位事實表未涵蓋，只有年度端點分位：P/S 90.4、EV/S 87.4。基本情境五年年化約 7%，上下行比約 1.9。","upside_short_pct":5.9,"upside_mid_pct":16.6},"trap_analysis":{"verdict":"🟡","label":"貴的好公司：兩項衰退信號亮燈，還不是價值陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 其他收入 5.94 億美元，相當於調整後 EBITDA 的 74%；利率今年持續上升，每台其他毛利年減 299 美元。FY2022 曾出現 FCF −18.36 億美元、營益率 −11.06%。","assumption":"多頭假設信用轉差時融資管道仍然暢通，貸款買方持續接手。","consequence":"管道收緊時貸款留在帳上，現金轉負，成長被迫放慢。五年虧 50% 最可能就是這條路：約 130 萬台，EPS 1.60 美元，18 倍。","ruling":"採納，悲觀機率給 30%。這和唯一致命事件是同一條因果鏈，兩處一致。Gotham 報告的指控內容事實表未涵蓋，無法判斷是否指向同一處。","watch":"每台其他收入低於 2,200 美元連兩季、ABS 發行是否縮量、淨負債比。","evidence_refs":["major_events#3"],"fact_refs":["f_kpi2_ebitda_non_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 在 2026-10-28 表示寧可讓價值表現在台數上；2025 年底起把利率讓給客戶，2026-07-29 也承認庫存吃緊時讓利「probably didn't get fully paid」。CEO 同時承認 AI 代理可能提高提前清償。FY2025 FCF 只有淨利的 63%。","assumption":"多頭假設規模帶來的好處會留給股東。","consequence":"台數照基本情境，但營益率停在 9.5%，FY2031 EPS 約 3.30 美元，26 倍值 86 美元，五年年化約 3%。","ruling":"部分採納。基本情境營益率 11.5%，已低於管理層目標 1 個百分點。","watch":"每台 GAAP 營業利益、每台 SG&A、FCF 與淨利的比率。","evidence_refs":["substitute_technology#2"],"fact_refs":["f_kpi3_gaap","f_kpi1"]},{"view":"價格已反映太多","evidence":"Forward P/E 48.4 倍，EV/S 在四個年度端點的 87.4 分位。賺 12% 年報酬要 FY2031 EPS 約 5.0 美元，等於約 220 萬台、12% 營益率。","assumption":"現價假設成長放慢前倍數撐得住，或 FY2031 結果接近樂觀情境。","consequence":"基本情境終點 104 美元，五年年化約 7%；三情境機率加權五年約 +36%，年化約 6%，上下行比約 1.9。","ruling":"採納，本輪不追價，等 59 美元以下。","watch":"股價、FY2027E 共識 EPS。","fact_refs":["f_fwd_pe_latest","f_ev_s_percentile"]}],"max_dd":{"lo":-70,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 73.57","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=73.57","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"單位獲利走向與管理層的路徑說法","cause":null,"prior_field":null,"side_a":"2026-10-28 CEO 說到 13.5% EBITDA 利潤率的路徑「extremely clear」，單靠費用槓桿就足以到 12.5% 營益率。","side_b":"Q3 每台費用持平，每台總毛利年減 410 美元，營收年增 42% 而營業利益只增 29%。2026-07-29 被問每台 EBITDA 何時回升時 CEO 沒給時間點，2026-10-28 再被問仍只談長期目標。","ruling":"程度差異，可調和。方向採信管理層，時點不採信。要到 12.5%，每台營業利益要從 3,284 美元升到約 4,620 美元，若全靠費用，每台費用要再降約四成，所以基本情境只算到 11.5%。","evidence_level":"高，財報數字與逐字稿","settle_metric":"每台 GAAP 營業利益年增率，看 2027 上半年兩季","if_then":["若 2027 上半年兩季每台 GAAP 營業利益轉為年增，但股價仍高於 59 美元，不追","若每台 GAAP 營業利益連兩季年減超過 300 美元，停止加碼","反向：股價先跌到 59 美元以下且每台 GAAP 營業利益未惡化，分批反買"]},{"axis":"庫存追上銷售的承諾","cause":null,"prior_field":null,"side_a":"2026-07-29 CEO 表示有信心庫存成長會追上並可能超過銷售。","side_b":"2026-10-28 CFO 說上架可立即購買的車輛，成長率仍遠低於銷售；分析師估庫存約增 30%，銷量增 39%。Q3 產量略高於銷量。","ruling":"承諾尚未兌現，方向正確。CEO 稱成長主要受限於供應鏈，這條決定第一個假設能否成立。","evidence_level":"中，庫存年增率為分析師說法","settle_metric":"上架庫存年增率減零售台數年增率","if_then":["若連四季庫存成長仍低於銷量成長，停止加碼","若 2027 上半年庫存成長超過銷量成長，但股價高於 59 美元，不追"]},{"axis":"高價車組合是否為結構性轉變","cause":null,"prior_field":null,"side_a":"2026-07-29 CEO 說偏向較新較貴車款「definitely not structural」，計畫回到較傳統的車齡里程組合。","side_b":"2026-10-28 CEO 說 prime 客群占比明顯上升，Q3 零售營收成長比台數高 15 個百分點，CFO 把 EBITDA 利潤率下滑部分歸因於高價車組合。","ruling":"管理層的一次性歸因未獲證實，也未被否定，列入監測。若到 2027 年 Q2 每台零售收入仍年增超過 5%，視為歸因證偽，利潤率目標要用每台金額重新檢視。","evidence_level":"中","settle_metric":"零售營收÷零售台數的年增率","if_then":["若 2027 年 Q2 每台零售收入仍年增超過 5% 且每台獲利未增，停止加碼"]},{"axis":"SEC 調查","cause":null,"prior_field":null,"side_a":"2025 年 6 月公司收到 SEC 傳票，主要涉及空方報告的指控。","side_b":"2026 年 9 月 SEC 告知已結束調查，不擬建議執法，未見財報重編。","ruling":"此風險退場。結案只代表沒有執法行動，不等於空方的所有指控都不成立。","evidence_level":"高，10-K 與 10-Q 原文","settle_metric":"已結案，不再需要判定","if_then":["若主管機關重啟調查或財報重編，清倉"],"evidence_refs":["regulatory_antitrust#0","major_events#0","major_events#1","sec_investigation_restatement#0"]},{"axis":"空方報告與證券集體訴訟","cause":null,"prior_field":null,"side_a":"2022 年證券集體訴訟仍在進行；2026-01-28 Gotham 報告後股價單日跌約 14.2%，多家律所宣布調查。","side_b":"搜尋未見 2026 年新案起訴，SEC 已結案，公司財報數字持續改善。","ruling":"不可裁決至集體認證或和解出現為止。求償金額、涉及營收與開庭日期事實表未涵蓋，這段證據不足以說風險已解除。","evidence_level":"低，缺金額與時程","settle_metric":"集體認證結果與和解金額","if_then":["若集體認證通過且和解金額超過 5 億美元，減碼一半","若出現刑事介入，清倉"],"evidence_refs":["major_events#2","major_events#3","lawsuit_class_action#0"]},{"axis":"停止給指引與追蹤可見度","cause":null,"prior_field":null,"side_a":"CFO 說轉向 GAAP 是公司成熟的自然演進。","side_b":"公司從 Q4 財報起不再提供展望，調整後 EBITDA 的重要性也會下降，而每台獲利正在下滑。","ruling":"轉向 GAAP 本身是好事，但外部監測變難。本報告的每台獲利關卡一律改用 GAAP 營業利益，避免口徑消失。","evidence_level":"中","settle_metric":"Q4 財報是否仍揭露每台毛利與費用拆解","if_then":["若公司同時取消每台毛利與費用拆解，停止加碼"]},{"axis":"Q3 獲利不如預期與共識未修正","cause":null,"prior_field":null,"side_a":"Q3 EPS 約 0.39 美元，低於共識 0.47 至 0.48 美元，含 5,300 萬美元一次性費用。","side_b":"兩份快照的 FY1、FY2、FY3 共識都沒有變動，FY1 仍是 1.52 美元。","ruling":"利空出現不到一季，共識可能還沒反映。Q4 財報出來之前凍結任何加碼。","evidence_level":"中，快照時點不明","settle_metric":"Q4 財報後 FY2027E 共識 EPS 是否低於 2.00 美元","if_then":["若 Q4 財報後 FY2027E 共識低於 2.00 美元且股價未跌，不追"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"結構轉好：FTC 要求揭露費用，對不收文件費的業者有利；CEO 認為 AI 代理放大實體摩擦的差異，線上化持續。","side_b":"競爭與融資壓力：10-K 預期新舊競爭者持續進入，Hertz 已進場；利率上升壓低每台融資收益，批發價處近三年高點。","ruling":"雙向拉鋸。零售端結構轉好，融資端面臨壓力，靠 Q3 份額續增與每台其他毛利年減 299 美元同時成立來支持這個判斷。","evidence_level":"中","settle_metric":"份額與每台其他收入","if_then":["若份額增速放慢且每台其他收入連兩季下滑，減碼"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"連續 11 季業界最快成長，資產負債表創紀錄，SEC 結案，股價 26 週跌 5.61%。若 FY2027 走樂觀路徑 2.30 美元，且倍數維持 38 倍，一年後約 87 美元，再等可能錯過。","side_b":"同一情境只給 19% 空間，而悲觀路徑五年虧 61%，上下行比約 1.9，基本情境年化約 7%。","ruling":"不採納現在進場。公司好不等於價格好，綁定約束只有價格，到 59 美元以下基本情境年化回到 12%。若訊號證實我錯，即 2027 上半年每台 GAAP 營業利益轉正成長且台數增 30% 以上，就把基本情境上修再重算進場價。","evidence_level":"中","settle_metric":"股價與 2027 上半年每台 GAAP 營業利益","if_then":["若股價先漲但每台獲利未回升，不追","若股價跌到 59 美元以下且基本面未受損，分批反買"]},{"axis":"估值分母","cause":null,"prior_field":null,"side_a":"Trailing P/E 35.37 倍，年度端點分位 0，看起來便宜。","side_b":"Forward P/E 48.4 倍，FY2026E 低於 FY2025A，營收卻預期成長 46%。","ruling":"採 Forward。Trailing 分母含不會重複或口徑不同的成分，不能用來說便宜。Q3 EPS 0.39 美元乘全部股數高於淨利 4.83 億美元，每股口徑也需要在原始財報上核對，本包無法查證。","evidence_level":"中","settle_metric":"10-K 的 FY2026 稀釋股數與稅率揭露","if_then":["若 FY2026 財報顯示正常化 EPS 低於 1.40 美元，不追"]}],"triggers":[{"n":1,"text":"貸款銷售管道中斷，或每台其他收入連兩季低於 2,200 美元。","type":"Single Thing","maps_to":"Single Thing","metric":"其他收入÷零售台數","threshold":"低於 2,200 美元連兩季，Q3 為 2,733 美元；或公告暫停主要貸款銷售管道","action":"清倉；未持有則不建倉","source_freq":"季報；ABS 發行文件每月","date":null},{"n":2,"text":"股價回到基本情境年化 12% 的價位。","type":"估值rearm","maps_to":"估值","metric":"收盤價","threshold":"不高於 59 美元","action":"重跑研究，基本面關卡未觸發才分批建倉","source_freq":"每日","date":null},{"n":3,"text":"台數成長是否維持基本情境路徑。","type":"假設驗證","maps_to":"H1","metric":"零售台數年增率","threshold":"連兩季低於 25% 視為偏離","action":"下修基本情境，價位未到不動作","source_freq":"每季","date":"2027-02"},{"n":4,"text":"每台獲利是否恢復成長。","type":"假設驗證","maps_to":"H2","metric":"GAAP 營業利益÷零售台數","threshold":"2027 上半年連兩季年增","action":"上修基本情境並重算進場價","source_freq":"每季","date":"2027-08"},{"n":5,"text":"每台獲利持續惡化。","type":"減碼","maps_to":"R1","metric":"每台 GAAP 營業利益年變動","threshold":"連兩季年減超過 300 美元，Q3 年減約 250 美元","action":"減碼一半；未持有則延後進場","source_freq":"每季","date":"2027-02"},{"n":6,"text":"整備產能跟不上銷售。","type":"風險","maps_to":"R2","metric":"上架庫存年增率減零售台數年增率","threshold":"連四季為負","action":"停止加碼","source_freq":"每季，法說會","date":"2027-08"},{"n":7,"text":"外部成本吸收失敗，包含油價、關稅與批發車價。","type":"風險","maps_to":"R3","metric":"零售 GPU","threshold":"低於 3,200 美元連兩季，Q3 為 3,625 美元","action":"停止加碼","source_freq":"每季","date":"2027-02","evidence_refs":["reg_tariff_export#0","supply_demand_durability#3"]},{"n":8,"text":"證券訴訟出現不利進展。","type":"風險","maps_to":"R4","metric":"集體認證與和解金額","threshold":"集體認證通過且和解超過 5 億美元；或刑事介入","action":"前者減碼一半，後者清倉","source_freq":"10-K、10-Q 法律事項","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":9,"text":"建倉後基本面連續驗證才加碼。","type":"加碼","maps_to":"H2","metric":"每台 GAAP 營業利益與淨負債比","threshold":"連兩季年增且淨負債比低於 1 倍","action":"分批加碼至目標倉位","source_freq":"每季","date":null},{"n":10,"text":"Q4 財報後複審，含共識是否下修與指引取消後的揭露內容。","type":"複審日期","maps_to":"全部","metric":"Q4 2026 財報","threshold":"財報發布後一週內","action":"重跑研究","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"每台其他收入（其他收入÷零售台數）","bear_threshold":"低於 2,200 美元連兩季","window":"兩季","source":"公司季報","last_status":"ok"},{"metric":"每台 GAAP 營業利益年變動","bear_threshold":"年減超過 300 美元連兩季","window":"兩季","source":"公司季報","last_status":"warning"},{"metric":"零售台數年增率","bear_threshold":"低於 20% 連兩季","window":"兩季","source":"公司季報","last_status":"ok"},{"metric":"淨負債對 TTM EBITDA","bear_threshold":"高於 2.0 倍","window":"單季","source":"公司季報，指標停揭時用 GAAP 數字自算","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 FY2026E 到 FY2028E 年化 34% 的 EPS 定價，等於假設每台獲利止跌回升；但 Q3 每台 EBITDA 年減約 400 美元，費用沒有槓桿，營業利益增速低於營收 13 個百分點。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=-5.61, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 路徑是用台數、每台收入、營益率和股數推出來的算術，不是題材敘事，管理層 300 萬台目標也查得到;但本次沒有找到可比案例的五年報酬數字，Bull 隱含年化 21.9% 是否合理無法驗證，只能算有條件成立。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價收在 59 美元以下，此時基本情境五年年化回到 12%；到價後重跑研究。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價收在 59 美元以下，基本情境五年年化回到 12%；觸發後重跑研究，不直接建倉","exec_line":"現價不追。股價到 59 美元以下且每台 GAAP 營業利益年減未擴大，重跑研究後先建首筆；Q4 財報前凍結任何加碼。"},"reasoning":{"industry":"Q3 營收 80.4 億美元，零售占 76.4%，批發 16.2%，其他 7.4%。TTM 毛利率 19.04%，GAAP 營益率 8.74%，Q3 單季營益率 8.9%。其他收入只占營收 7.4%，但 5.94 億美元相當於調整後 EBITDA 的 74%，每台 2,733 美元，是全公司最依賴外部資金市場的一段；其他毛利事實表未單列，此數為上限。每台總毛利 7,093 美元，年減 410 美元，每台費用持平，所以每台調整後 EBITDA 約 3,680 美元，年減約 400 美元，CEO 歸因約 200 美元來自油價與利率。單點依賴在貸款買方與 ABS 市場，買方名單與集中度事實表未涵蓋。可能看錯的地方：若其他收入有相當部分來自保固與服務合約，對資金市場的敏感度會低於這裡的估計。","moat":"機制是整備、物流與單一庫存池的垂直整合：規模越大，選車越多、到貨越快、資金成本越低。可驗證的方向是份額，從 10-K 的 1.6% 升到 Q3 的兩個百分點出頭，產業同期持平；營益率高於 KMX、AN、LAD。稅後 ROIC 約 23%：2026-07-29 CFO 給的 TTM 營業利益約 22 億美元、淨營運資產約 75 億美元，稅前約 29%，再以 21% 假設稅率換算，隱含周轉約 3.4 倍。這是低利益率、高周轉的零售模式。FY2025 實現的增量報酬約 118%，主因是填滿既有產能，不能外推，前瞻取 50%。反例是 Q3 每台費用沒有槓桿，新場站初期成本也較高，增量報酬可能比 50% 更低。同業 ROIC 事實表未涵蓋。","growth":"成長以量為主：Q3 零售營收年增 54%，台數 39%，其餘約一成是高價車組合，量約占 76%。共識 EPS 從 FY2025A 1.69 到 FY2028E 2.73，年化 17.3%；但 FY2026E 1.52 低於 FY2025A，營收卻增 46%，基期含不會重複的成分，細項事實表未涵蓋。改用 FY2026E 為基期，兩年年化 34.0%，高於內生上界 20%，缺口 14 個百分點歸因於營益率擴張，主要是費用槓桿，不是回購或併購。Koyfin 的 EPS 家數未載明。按 39% 成長率，5.9 年即達零售二手市場的 30%，這不現實；用平均 20% 成長則為 10.7 年。反例：CEO 說成長受限於供應鏈，產能一旦跟不上，跑道再長也兌現不了。","governance":"FY2025 FCF 為淨利的 63%，TTM FCF 利潤率 4.05%。SBC 每季 2,500 萬美元，占營收 0.3%。Q3 淨負債對 TTM 調整後 EBITDA 0.8 倍，利息保障 6.9 倍，都是公司紀錄。2026 年 8 月以 16.6 億美元定期貸款再融資，每年省息約 4,500 萬美元，Q3 認列一次性費用 5,300 萬美元。CFO 在 2026-07-29 表示現金首要用途是投資業務。營運槓桿在 Q3 轉弱：營收年增 42%，GAAP 營業利益年增 29%，差 13 個百分點。近三年現金去向四分、債務到期結構與逐年股數事實表未涵蓋。","valuation":"現價 73.57 美元，Forward P/E 48.4 倍。要賺 12% 年報酬，五年後股價要 130 美元，以 26 倍計 FY2031 EPS 要約 5.0 美元，等於約 220 萬台、12% 營益率。我的基本情境是 185 萬台、11.5%、EPS 4.00 美元，終點 104 美元，年化約 7%。短期目標：FY2027E 2.05 美元×38 倍＝77.9 美元；中期：FY2028E 2.60 美元×33 倍＝85.8 美元，兩個倍數都是判斷值。賣方目標均值 84.14 美元，區間 48 至 120 美元，是 2026-08-05 的舊資料，早於 Q3，不支持追價。Q3 EPS 約 0.39 美元，低於共識 0.47 至 0.48 美元，但兩份快照的 FY1 共識都是 1.52 美元，可能尚未更新。RSI 62.82 未過熱，4 週漂移事實表未涵蓋。","premortem":"悲觀路徑是利率與信用同時轉差，其他收入下滑，台數停在 130 萬台左右。FY2022 的 FCF −18.36 億美元、營益率 −11.06% 是這家公司真實發生過的下行。我也可能看錯在另一邊：若每台獲利在 2027 年回升，同時台數維持 30% 以上成長，等 59 美元可能永遠等不到。未涵蓋且會影響判斷的資料有：貸款買方集中度、其他收入細項、歷史最大回撤、Gotham 報告的指控內容、集體訴訟金額、同業倍數。2026-07-29 的法說會上，管理層多次避開下半年獲利與每台獲利回升時點的提問。"},"plain":{"six":{"how_it_makes_money":"Carvana 賺買車人的車差和貸款的錢，錢卡在貸款能不能順利賣出去。","moat":"護城河在變寬，來自規模帶動的選車、到貨速度與資金成本，定價面大致穩定。","growth":"成長跑道寬，五年後仍有空間，滲透率遠低於 35%。","capital":"現金優先投回業務和降債，沒有回購，股本稀釋很低。","valuation":"現價要求 FY2031 EPS 接近 5 美元才有 12% 年報酬，我只信到 4 美元，所以偏貴。","how_wrong":"最可能看錯的是融資收益的韌性，其次是現價已先付了未來幾年的成長。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2026E 到 FY2028E 年化 34% 的 EPS 定價，等於假設每台獲利止跌回升；但 Q3 每台 EBITDA 年減約 400 美元，費用沒有槓桿，營業利益增速低於營收 13 個百分點。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價收在 59 美元以下，此時基本情境五年年化回到 12%；到價後重跑研究。","qc48_result":"pass","qc48_note":"Bull 路徑是用台數、每台收入、營益率和股數推出來的算術，不是題材敘事，管理層 300 萬台目標也查得到;但本次沒有找到可比案例的五年報酬數字，Bull 隱含年化 21.9% 是否合理無法驗證，只能算有條件成立。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":73.57,"week26_return_pct":-5.61,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"Trailing P/E 35.37 倍低於 Forward 48.4 倍，反推 trailing EPS 約 2.08 美元，高於 FY2025A 的 1.69 美元與 FY2026E 的 1.52 美元，而營收預期成長 46%。分母含不會重複或口徑不同的項目，細項事實表未涵蓋，P/E 端點分位 0 不能當便宜的證據。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報（日期未公告，依往例推估），公司自此不再提供展望，2027 年起以 GAAP 為主","impact":"高","watch":"每台 GAAP 營業利益、零售台數、每台毛利與費用拆解是否續揭露"},{"date":"2027-03","date_precision":"quarter","type":"macro","event":"租賃退場車回升，次級來源轉述 Manheim 預估 2027 年 310 萬台","impact":"中","watch":"批發與零售價差、零售 GPU"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"完整轉換的 ADESA 場站陸續上線，時點為推估，新場站初期成本偏高","impact":"中","watch":"每台營運費用、整備產量相對銷量"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"新車經銷據點是否擴展到 Stellantis 以外的車廠，時點未揭露","impact":"低","watch":"新車業務揭露與車廠合作"}],"_projected_from":"v19"}
```
