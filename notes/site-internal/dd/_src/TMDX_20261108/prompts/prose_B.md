你是 stock-analyst v20 的**散文層（prose）agent**，標的 TMDX（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：TMDX　日期：2026-11-08　archetype：None　前份裁決：2026-05-25　B 衛星候選等修復 — thesis 完整但 Q1 EPS miss 引發 trap 🟡 + MA ❌→🟠 雙減半；等 Q2 26 EPS recovery + W250 站回 ~$80 連 4 週後可升 A｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1875B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（760B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（993B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1380B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（898B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（619B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（809B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2210B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3655B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2647B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1875           3587-5125      5 條（2–6 內）  
s3                  8000         760           5068-7240      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3271          8210-11729      5 條（2–6 內）  
s6                 11000         619          7267-10381      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         809           1884-2691      5 條（2–6 內）  
s10                 5000        2210           1953-2790      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2647           2000-2353      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4911B；至少需散文≈40.09KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−60
−57%
−55%
−40%
−40
0
0.44
0.50
0.51
0.70
0.75
0.83
1%
1
1.086
1.134
1.22
1.336
1.5%
1.5
1.51
1.6%
1.7
1.9
1.903
1.93
1.98
2%
02
2
2.03
2.1
2.2
2.20
2.25
2.3
2.5
2.7
3
03
3%
3.21%
3.30
3.3
3.31
3.42
3.74
04
4%
4
4.2
4.3
4.47
4.87
4.93
5
5%
05
5.3
5.30
5.68
5.7
5.8
6%
6
6.0%
6.22
6.3
7
07
7.27
7.6
7.64
7.74
8
08
8.67
8.95
9
9.6
10
10%
10.4
11
11.4
11.82%
12
12%
12.1%
12.21%
12.3%
12.5%
13%
13
13.9%
14%
14
14.2%
15%
16
16%
16.4%
18%
18.0%
18
19%
20%
20
21%
22
22%
23%
24%
24
24.04
25
25%
26
26%
27
28.0%
28%
28
29%
30%
30
30.07
30.65
31
32.2%
33
35
35%
36%
38
38.6%
39.2
39.22
39.6
40
41%
42
43%
44%
45
48%
49
49.1
50%
53
55%
57
58
58.44
58.5%
60%
61.1%
62
62%
68.94
70
75%
75
75.4%
79.2%
$80
81%
82%
86%
88.24
90
91%
100%
100
109
120
124.45
124.5%
134
142
143
150%
178
200
230
250
260
288
300
510
660
940
2023
2025
2026
2027
2028
2030
20261108
1,050
1,210
1,400
1,540
10,000
2,000
2,200
2,900
21,000
3,300
3,473
3,500
4,080
4,100
4,300
4,400
4,840
5,139
7,000
8,500
8,960
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
{"meta":{"ticker":"TMDX","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"TransMedics Group, Inc."},"oneliner":"Q3 營收年增 41%，不含 PAD 毛利率 61.1%，成長與利潤都比五月好；但股價已從 68.94 美元漲到 88.24 美元，十月航班轉弱，2027 年利潤率也沒給方向，先等 2 月全年指引再決定進場。","thesis":{"H":[{"id":"H1","text":"2026 年利潤率下修是公司主動加碼研發的選擇，毛利結構沒有變差，2027 年起營業槓桿會回來。","2y":"FY2028 調整後營業利益率至少 19%","5y":"FY2031 調整後營業利益率至少 23%","10y":null,"threshold":"FY2027 至少 14%；FY2028 至少 19%；不含 PAD 毛利率至少 60%","source":"公司 8-K 與法說，每季","drift_rule":"TTM 調整後營業利益率對照路徑，連 2 季偏離至少 5% 為削弱，連 3 季偏離至少 10% 為反轉。"},{"id":"H2","text":"現有心肝肺平台靠份額與服務滲透，即使全美捐贈者下滑，案量仍能維持高成長。","2y":"FY2028 美國案量至少 8,500 例，營收至少 10.4 億美元","5y":"FY2031 營收至少 16 億美元","10y":null,"threshold":"FY2026 營收至少 7.64 億美元；FY2027 至少 8.95 億美元；FY2028 至少 10.4 億美元","source":"公司 8-K 與法說，OPTN 月度資料","drift_rule":"TTM 營收對照路徑，連 2 季偏離至少 5% 為削弱，連 3 季偏離至少 10% 為反轉。"},{"id":"H3","text":"Part B、DENOVO、腎臟與歐洲會成為第二條成長曲線，讓成長延續到五年以後。","2y":"兩試驗 2027-03-31 前開始收案，2027 年底累計至少 300 例，CHOPS 510(k) 於 2027 年底前取得","5y":"FY2031 心、肺、腎與國際合計占營收至少 35%","10y":"腎臟占營收至少 25%","threshold":"合計 1,050 例收案，18 個月內完成一半以上；OCS Kidney 於 2027 下半年完成首例人體","source":"公司法說與 FDA 公告；試驗登記資料事實表未涵蓋","drift_rule":"里程碑延誤一季為削弱，延誤兩季以上為反轉；占營收比連 4 季偏離至少 5% 為削弱，連 6 季偏離至少 10% 為反轉。"}],"R":[{"id":"R1","text":"2027 年全年指引給不出利潤率擴張。財務長不給方向，研發至少維持幾季，Part B 與 DENOVO 費用還沒完全進來，賣方卻模型化擴張。","h_ref":"H1","clock":"⚡","threshold":"FY2027 調整後營業利益率指引中點低於 14%","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"第四季量能不如指引隱含。管理層承認十月航班下降，不含 PAD 第四季隱含營收約 1.98 億美元。","h_ref":"H2","clock":"⚡","threshold":"第四季不含 PAD 營收低於 1.93 億美元","evidence_refs":[]},{"id":"R3","text":"肝臟競爭加劇，移植中心逐例改用其他保存方式，大客戶的使用量也可能下降。","h_ref":"H2","clock":"🔥","threshold":"美國肝臟營收連 2 季季減","evidence_refs":["customer_concentration_credit#1"]},{"id":"R4","text":"試驗與核准時程繼續往後。CHOPS 510(k) 已由 2027 上半年延到下半年，Part B 催化已由第四季延到 2027 年第一季。","h_ref":"H3","clock":"🔥","threshold":"2027-03-31 前任一試驗未開始收案，或 2027 年底前 CHOPS 510(k) 未取得","evidence_refs":[]},{"id":"R5","text":"管理層與揭露可信度。CFO 在 2026-08-04 與 2026-11-05 兩次法說之間由 Gerardo Hernandez 換成 Fernando Araujo，原因本包未涵蓋；Q2 法說對乾跑與義大利補償都曾改口；證券集體訴訟駁回聲請待裁，訴訟金額事實表未涵蓋。","h_ref":"H1","clock":"🔥","threshold":"CEO 或 CFO 再異動；駁回聲請遭否且獲集體認證；出現刑事或 SEC 調查","evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"id":"R6","text":"供應單點與關稅。部分零件與灌注液單一來源，Andover 單一廠區，第三方滅菌與飛機網路都有依賴；關稅已小幅墊高成本。","h_ref":"H1","clock":"🔥","threshold":"產品毛利率連 2 季低於 75%，或單一供應中斷造成停產超過 30 天","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R7","text":"OPO 制度改革造成交接混亂，全美捐贈量持續下滑，Q3 已年減 6%。","h_ref":"H2","clock":"🐢","threshold":"全美已故捐贈者量連 4 季年減","evidence_refs":[]}],"single_thing":{"description":"美國肝臟營收（Q3 約 1.5 億美元）連兩季季減，同時全美肝移植量沒有同步下降。","why_fatal":"肝臟占美國移植營收約 81%，研發與試驗資金幾乎都靠它；肝臟失速後，營收與營業槓桿會同時失去，FY2028 共識 EPS 3.31 美元站不住。","if_happens":"清倉，等肝臟營收連兩季回穩才重跑研究。","how_monitor":"每季法說揭露的器官別營收；OPTN 每月移植與航班資料作領先指標。","probability":"12 到 24 個月約 20%，依據是 Terumo／OrganOx 在肝臟正面競爭，份額只有管理層口述，Q3 美國移植營收季增僅 1%。"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":39.22,"peg_fy2":0.83,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":4.87,"FY2026E":1.51,"FY2027E":2.25,"FY2028E":3.31},"fy_end_month":12,"eps_basis":"共識取自 2026-11-07 Koyfin 快照，會計口徑事實表未標明；FY2025A 4.87 美元為 GAAP 稀釋 EPS，含非營業項目，淨利 1.903 億美元高於營業利益約 1.086 億美元，差額事實表未拆解，不適合當成長基期。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"未獲利高成長","confidence":"中","fingerprint":"每例收費的耗材加服務，已轉盈但仍在投資期，FY2025 才首度產生正 FCF。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：全球可移植器官長期短缺，美國等候名單超過 10.4 萬人（Transplant International 2026 綜述）；短期量受 Q3 全美捐贈者年減 6% 影響。","bargaining":{"up":"Fresenius Kabi 是 OCS 心肺灌注液單一來源，部分零件為單一來源，換廠可能需要 FDA 核准。","down":"沒有客戶超過營收 10%，議價分散，但移植中心可以逐例選擇保存方式。","geo":"歐洲靠逐區標案進入，義大利只取得預算，德國目前沒有補償。"},"profit_pool_dir":"五年營業利益池資料事實表未涵蓋；公司同時拿器材、服務與物流三段，服務占比上升正在拉低整體毛利率。","tam_table":[{"item":"美國心肺肝移植滲透率（2025）","value":"OCS 5,139 例，約占 26%；肝臟 36%"},{"item":"短保存 DBD 心臟（ENHANCE Part B 目標）","value":"2025 年約 2,200 例，尚無適應症"},{"item":"美國肺移植（DENOVO 目標）","value":"每年約 3,500 例，多數未用機器灌注"},{"item":"美國腎移植（OCS Kidney 目標）","value":"每年約 21,000 顆已移植，另約 9,000 顆未使用；2027 下半年才首例人體"},{"item":"歐洲","value":"管理層稱與美國規模相當；2027 上半年進義大利、荷蘭、比利時"},{"item":"分段年複合成長率與營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"FDA 核准的可攜式多器官溫灌注裝置，加上臨床取器服務與自有機隊，形成每例收費的整合服務。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"擴大的證據是 Q3 肝心份額增加，但只有管理層口述；縮減的證據是 Terumo 收購 OrganOx 與 XVIVO 申請核准，尚未反映在營收。兩邊都沒有獨立份額數字，故判持平。","peer_na_reason":"對照表四家都不是器官保存的直接對手，直接對手 XVIVO 與 OrganOx 的財務事實表未涵蓋，投入資本報酬差距無法計算。","threats":[{"level":"🔴","text":"Terumo 買下 OrganOx，在肝臟這個核心市場放大對手的銷售與資本。肝臟占美國移植營收約 81%，屬生態層級的攻擊。","p":"35%","evidence_refs":["supply_demand_durability#5"]},{"level":"🟡","text":"XVIVO 心臟冷灌注若獲 FDA 核准，將直接競爭 ENHANCE Part B 的短保存 DBD 心臟區塊，屬單點競爭。","p":"50%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"常溫區域灌流與冷藏是移植中心可以逐例選擇的替代方案；RE-UP 目前據管理層說只有一家中心使用。","p":"30%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"10-K 承認他方可能做出更好或更便宜的技術，公司也要持續向外科醫師與支付方證明 OCS 優於冷藏；目前沒有具體替代產品上市紀錄。","p":"30%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，象限不下結論。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是外科醫師，決策者是移植中心，付款端已有既定補償路徑；器官短缺屬結構性，等候名單超過 10.4 萬人。Q3 捐贈者年減 6% 是供給波動，不是需求消失。"},{"item":"決策層級","level":"🟡","text":"替代性發生在每一顆器官與每位外科醫師的選擇上。Q2 法說管理層說有對手的大客戶轉過來，代表客戶換得動，反向也成立；合約年限與流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"公司同時拿耗材、服務、物流，產品毛利率 79.2%，服務 32.2%；上游器官由 OPO 掌握，灌注液單一來源，毛利最高的一段又面臨冷藏低價方案。"},{"item":"社會容忍度","level":"🟡","text":"器官移植屬高必要、高敏感領域，CMS 10 月 30 日定案 OPO 認證新規，也更重視運送事件；目前對公司偏中性，但優勢部分依賴監管框架，新 OPO 進入路徑還要再立法程序。"}],"roiic":"事實表未涵蓋（投入資本與折舊攤銷都沒有），不計算。","reinvest_rate":"事實表未涵蓋，不計算。","endo_ceiling":null,"formula_note":"內生成長率等於增量報酬乘再投資率，兩項輸入都缺，不輸出上界。TTM FCF 利潤率 11.82% 接近營業利益率 12.21%，現階段成長投資多走研發費用，資本再投資率本身也難代表成長投入。情境樹保守視為超出上界，熊市機率給 30%。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","TMDX":58.69,"ABT":56.67,"MDT":65.01,"GKOS":64.78,"PODD":71.88,"unit":"%"},{"metric":"營業利益率","TMDX":12.21,"ABT":13.9,"MDT":19.04,"GKOS":-25.3,"PODD":18.44,"unit":"%"},{"metric":"FCF 利潤率","TMDX":11.82,"ABT":13.37,"MDT":16.33,"GKOS":2.81,"PODD":7.29,"unit":"%"},{"metric":"研發密度","TMDX":13.83,"ABT":6.8,"MDT":7.77,"GKOS":27.12,"PODD":11.3,"unit":"%"}],"competitors":[{"name":"ABT","gm":56.67,"om":13.9,"fcf_margin":13.37,"rd_intensity":6.8,"strategy_note":"大型多元醫材公司，不在器官保存正面競爭，只作成熟醫材的利潤率參照。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"MDT","gm":65.01,"om":19.04,"fcf_margin":16.33,"rd_intensity":7.77,"strategy_note":"成熟醫材規模參照；營業利益率較高反映規模，與移植領域的競爭無關。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"GKOS","gm":64.78,"om":-25.3,"fcf_margin":2.81,"rd_intensity":27.12,"strategy_note":"成長型醫材參照；研發密度更高且仍為營業虧損，公司在這類成長股裡已先轉盈。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PODD","gm":71.88,"om":18.44,"fcf_margin":7.29,"rd_intensity":11.3,"strategy_note":"耗材型經常性收入的參照；毛利率較高，對照出公司的服務與航空占比拉低毛利。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主，Q3 案量新高、產品年增 29%；價格次之，服務調價轉嫁油價；併購小，PAD 全年約 1,400 萬美元；沒有回購。","runway_years":"現有三器官平台約 1 到 2 年就到 30% 滲透；加上腎臟與歐洲後超過 10 年，但後者尚無營收證據。","runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本與折舊攤銷，增量報酬無法計算；共識成長的缺口歸因於利潤率擴張，保守視為超過內生上界。","segments":[{"item":"產品（Q3）","value":"1.134 億美元，年增 29%，毛利率 79.2%"},{"item":"服務（Q3，含 PAD 940 萬美元）","value":"8,960 萬美元，年增 60%，毛利率 32.2%"},{"item":"物流（Q3，服務內）","value":"約 4,100 萬美元，年增約 50%"},{"item":"美國肝臟（Q3）","value":"約 1.5 億美元"},{"item":"美國心臟（Q3）","value":"約 3,300 萬美元"},{"item":"美國肺臟（Q3）","value":"約 200 萬美元"},{"item":"國際（Q3）","value":"660 萬美元，年增 82%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","status":"未亮","note":"Q3 年減 40 基點，Q2 年比事實表未涵蓋；不含 PAD 為 61.1%，年增 230 基點。"},{"signal":"核心市占近 12 個月縮減","status":"未亮","note":"管理層稱肝心份額增加，沒有獨立數字。"},{"signal":"主力產品提價後銷量下滑","status":"未亮","note":"本包沒有此類證據。"},{"signal":"EPS CAGR 顯著高於營收 CAGR","status":"亮","note":"FY2026 至 FY2028 共識 EPS 年化約 48%，FY2027 營收增 16.4%。"},{"signal":"FCF／淨利連 2 年低於 0.75","status":"亮","note":"FY2024 為負，FY2025 為 0.70；FY2025 淨利含非營業項目，訊號偏機械。"},{"signal":"SBC／營收超過 5% 且逐年上升","status":"資料缺口","note":"Q3 為 6.0%，歷年趨勢事實表未涵蓋。"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"未亮","note":"Q3 捐贈者年減 6% 只有一季。"},{"signal":"產業估值倍數近 3 年系統性下移","status":"資料缺口","note":"事實表未涵蓋。"},{"signal":"維護性資本支出占 FCF 超過 60%","status":"資料缺口","note":"事實表未涵蓋。"},{"signal":"停止投資新產能且收入 3 年內下滑","status":"未亮","note":"公司仍在擴張，營收持續成長。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，公司也沒有配息或回購紀錄；現金優先投入研發與臨床，三年現金去向事實表未涵蓋。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"PAD Aviation 才併入一季，投入金額事實表未涵蓋，沒有已實現報酬可驗。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"本包未見回購紀錄，管理層的資本配置優先序也沒有回購。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 1,210 萬美元，年化約 4,840 萬美元，除以市值 30.65 億美元約 1.6%／年，略高於 1.5%，且沒有回購抵銷。","grade":"不過"}]},"valuation":{"basis":"以 EPS 乘本益比為主。FY1 本益比 58.44 倍，FY2 39.2 倍，trailing 24.04 倍不採用。","tier":"已獲利、仍在投資期的高成長醫材","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，也沒有 XVIVO 與 OrganOx 的財務；終端倍數改由自身前瞻倍數與成長放緩推算，列為資料缺口。"},"fwd_pe":58.44,"peg":1.22,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 58.44 倍的分母被 2026 年研發高峰壓低，換 FY2 為 39.2 倍。以 FY2026 至 FY2028 共識 EPS 年化 48% 計算，PEG 為 1.22，落在 1 到 2 的合理區，但基期偏低，PEG 偏好看。前瞻 EV／S 為 4.47 倍。五年分位無法計算，事實表只有 2 到 4 個年度端點，現值在端點最低，不能當便宜的證據。","upside_short_pct":24,"upside_mid_pct":62},"trap_analysis":{"verdict":"🟡","label":"中度風險：EPS 增速遠高於營收，FCF 對淨利轉換偏低"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"肝臟占美國移植營收約 81%，Terumo 已買下 OrganOx，執行長也說市場非常擁擠；份額增加只有管理層口述。","assumption":"整合服務足以抵擋大公司用價格與通路攻打肝臟。","consequence":"肝臟失速，FY2031 EPS 約 2.2 美元、18 倍，股價約 40 美元，五年虧約 55%。","ruling":"採納，熊市機率給 30%，與唯一致命條件同一條。","watch":"美國肝臟營收季增率，OPTN 月度移植量。","not_applicable_reason":null,"evidence_refs":["supply_demand_durability#5","competitive_share_entrants#2"]},{"view":"論點成功但股東經濟變差","evidence":"服務占營收升到 44%，毛利率 32.2%；PAD 拉低毛利率 260 基點；CHOPS 定位是不同價位的第二選項；Q3 調整後研發年增 91%；8 月才把全年營業利益率展望由約 16% 下修到 12.5% 至 14%。","assumption":"案量達標後，利潤率會回到管理層的 30% 目標。","consequence":"移植量達標，但 FY2031 營業利益率只有 18%，EPS 約比基本情境少 22%。","ruling":"部分採納，基本情境只用 23%，不採信 30%。產品毛利率 79.2% 部分來自報廢減少，能否持續未證。","watch":"不含 PAD 毛利率、產品毛利率、服務毛利率。","not_applicable_reason":null,"evidence_refs":["supply_demand_durability#3"]},{"view":"價格已反映太多","evidence":"FY1 本益比 58.44 倍，26 週上漲 30%；Q2 後 Piper Sandler 把目標價由 120 美元降到 100 美元；9 月資料顯示 Zacks Rank 5、放空比例約 38.6%；賣方目標價最高與最低約 2.5 倍。","assumption":"FY2028 EPS 3.31 美元會實現，倍數壓縮慢於盈餘成長。","consequence":"若 2 月指引讓 FY2027 EPS 下修 15%，以 30 倍計算約 57 美元，跌約 35%。","ruling":"部分採納。58 倍的分母被壓低，FY2 39.2 倍不算離譜，但賣方分歧大，因此等 2 月指引。","watch":"FY2027 共識 EPS 是否低於 2.25 美元，放空比例變化。","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#4"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 68.94 → 本次 88.24（+28.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=68.94","side_b":"本次 price_at_dd=88.24","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 68.94 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 68.94 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 68.94 美元：Bull 價 288、Bear 價 39.6，五年期望值 +124.5%，基準年化 18.0%，不對稱比 6.22","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 6.22。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 68.94 美元：五年期望值 +124.5%，基準年化 18.0%，不對稱比 6.22","side_b":"本次情境、股價 88.24 美元：五年期望值 +75.4%，基準年化 12.3%，不對稱比 3.42","ruling":"再換股價、情境不動：起點價上漲 28.0%，五年期望值少 49.1 個百分點，基準年化少 5.7 個百分點，不對稱比由 6.22 降到 3.42。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份判擴大：五年內 XVIVO 不會進入美國心肝市場，22 架機隊構成物流護城河。","side_b":"本次判持平：Q3 份額仍增加，但 Terumo 買下 OrganOx，XVIVO 心臟產品爭取 FDA 核准，執行長自稱市場非常擁擠。","ruling":"採持平。份額增加只有管理層口述，對手加碼有外部來源，證據不足以支持擴大。可調和，屬程度差異。","evidence_level":"中：對手面有低品質來源，份額面沒有獨立數字。","settle_metric":"美國肝臟營收季增率；OPTN 肝移植 OCS 使用比例（事實表未涵蓋）。","if_then":["若美國肝臟營收連兩季季增至少 3% 且 XVIVO 心臟未獲核准，方向上修為擴大，部位加碼至 4%。","若美國肝臟營收連兩季季減，清倉。"],"evidence_refs":["supply_demand_durability#5","competitive_share_entrants#2"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 68.94 美元，估值判便宜（🟢）。","side_b":"本次股價 88.24 美元，FY1 本益比 58.44 倍，FY2 39.2 倍，估值判合理（🟡）。","ruling":"主因是股價上漲 28%；同期 FY1 共識近三個月反而下修 3.21%，盈餘預期沒有跟著變好。","evidence_level":"高：價格與共識都是實際數字。","settle_metric":"FY2027 共識 EPS 與股價的相對變動。","if_then":["若股價在 2 月指引前漲過 100 美元，不追。","若股價跌到 75 美元以下且第四季不含 PAD 營收不低於 1.93 億美元，分批反買。"],"evidence_refs":[]},{"axis":"評級與價值陷阱","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評級 B、價值陷阱中度，理由是 Q1 EPS 不如預期；升級條件為 Q2 EPS 回升，且股價站回 250 週均線連 4 週。","side_b":"本次維持 B 與中度，理由換成 EPS 增速遠高於營收、FCF 對淨利轉換偏低。Q2 調整後 EPS 0.44 美元低於 0.50 美元共識，Q3 回到 0.51 美元。","ruling":"不升級。Q2 沒有達到前份條件，Q3 轉好只有一季，股價現在高於 250 週均線，但連續週數事實表未涵蓋。","evidence_level":"中","settle_metric":"FY2027 全年調整後營業利益率指引。","if_then":["若指引中點至少 14%，建首倉 2%。","若指引中點低於 12.5%，停止加碼，等試驗收案資料。"],"evidence_refs":[]},{"axis":"前份假設驗證","cause":"新證據","prior_field":null,"side_a":"前份要求 Q3 營業利益率至少 12%，FY2026 至少 15%，FY2026 營收至少 7.27 億美元。","side_b":"Q3 調整後 14.2% 達標，營收指引 7.64 億至 7.74 億美元達標；FY2026 利潤率指引 12.5% 至 14%，低於 15%。","ruling":"利潤率假設部分落空。前份把壓力歸因於機隊擴張的時點，本次改為主動加碼腎臟與試驗投資，並重寫成新的利潤率論點。","evidence_level":"高：公司財報與指引。","settle_metric":"FY2027 調整後營業利益率。","if_then":["若 FY2027 低於 13%，減碼一半。"],"evidence_refs":[]},{"axis":"未填欄位補齊","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位都是空值。","side_b":"本次依現行框架補齊：五年後空間判寬，類型為品質複利成長且信心中等，循環位置不適用，機率與回撤區間見情境樹。","ruling":"屬舊版沒有輸出，不代表看法改變。","evidence_level":"不適用","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 與前份對照","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（空值）。","side_b":"美國肝臟營收連兩季季減，同時全美肝移植量沒有同步下降。","ruling":"本次新設 Single Thing。肝臟占美國移植營收約 81%，是數學上最大的單一敏感項。","evidence_level":"中","settle_metric":"每季法說揭露的器官別營收。","if_then":["條件成立即清倉。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻對照","cause":"方法變動","prior_field":["kill_metrics","rearm_trigger"],"side_a":"前份未設 kill_metrics 與 rearm_trigger（空值），結論只寫「等 Q2 26 EPS recovery + W250 站回 ~$80 連 4 週後可升 A」。","side_b":"美國肝臟營收連 2 季季減即清倉；TTM 調整後營業利益率低於 12% 連 2 季即減碼一半；重新進場條件為 2027 年全年調整後營業利益率指引中點至少 14%。","ruling":"舊條件以股價與單季 EPS 為主，新條件改看肝臟與利潤率，因為論點的敏感度集中在這兩項。","evidence_level":"中","settle_metric":"美國肝臟營收；調整後營業利益率。","if_then":["條件未觸發前，不因股價波動減碼。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：有機成長 35%，不含 PAD 毛利率 61.1%，FY2 本益比 39.2 倍，放空比例高，試驗 2027 年第一季啟動；等到 2 月可能錯過重估。","side_b":"等 2 月：十月航班下降是管理層親口承認，第四季隱含營收要季增，FY2027 利潤率沒有方向，也是新財務長第一份全年指引。","ruling":"選等。基本情境年化約 12%，多等三個月的成本小；十月疲軟的消息未滿一季，且 11-07 共識快照沒有變動，尚不能確定已進賣方模型。可調和，屬時點差異。","evidence_level":"中","settle_metric":"2027 年 2 月財報的全年利潤率指引。","if_then":["若股價先漲過 100 美元而指引未出，不追。","若股價跌到 75 美元以下而第四季不含 PAD 營收不低於 1.93 億美元，分批反買。","若指引中點至少 14%，即使股價已上漲，也重跑研究後建首倉 2%。"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"2028 年目標可信度","cause":null,"prior_field":null,"side_a":"管理層在 Q2 重申，2028 年約 10,000 例、營收 12 億美元、營業利益率 30%。","side_b":"共識 FY2028 EPS 只有 3.31 美元；Q3 法說沒有重申這組數字，財務長也不給 2027 年利潤率方向。","ruling":"站共識這邊。2026 年指引只有 12.5% 至 14%，要兩年翻倍以上，沒有數據支持。基本情境 FY2028 EPS 用 3.30 美元。可調和，屬程度差異。","evidence_level":"中","settle_metric":"FY2027 調整後營業利益率。","if_then":["若 FY2027 至少 18%，上調基本情境並加碼至 4%。","若 FY2027 低於 13%，下修基本情境並減碼一半。"],"evidence_refs":[]},{"axis":"服務增速與案量的落差","cause":null,"prior_field":null,"side_a":"服務營收不含 PAD 年增約 43%，管理層歸因於 NOP 採用、份額與調價。","side_b":"產品年增 29%、季增 2%，美國移植營收季增 1%；2026-08-04 法說，執行長先否認乾跑增加，後來又說差距可能來自乾跑。","ruling":"未證、監測。預登記：不含 PAD 的服務增速連 3 季高於產品增速 10 個百分點以上，且公司未拆解案量與價格，就判定服務成長品質不足。","evidence_level":"低：公司未揭露案量與乾跑。","settle_metric":"不含 PAD 服務增速減產品增速；年度案量。","if_then":["條件成立時，FY2027 基本情境營收下修 5%，停止加碼。"],"evidence_refs":[]},{"axis":"試驗與核准時程滑動","cause":null,"prior_field":null,"side_a":"2026-08-04 法說，Waleed Hassanein：CHOPS 510(k) 現實時程是 2027 上半年，心臟預期第四季起隨 Part B 解鎖而加速。","side_b":"2026-11-05 法說，Waleed Hassanein：510(k) 目標改為 2027 下半年，Part B 與 DENOVO 催化延到 2027 年第一季，第四季指引不計入。","ruling":"管理層時程要打折，基本情境不放早於 2027 下半年的試驗增量營收。試驗讀數今天不存在，收案起算 12 到 18 個月，不可裁決至 2028 年。","evidence_level":"高：兩次法說原話。","settle_metric":"2027-03-31 前兩試驗是否開始收案；2027 年底前 510(k) 是否取得。","if_then":["若任一試驗到 2027-03-31 仍未收案，停止加碼。","若兩項里程碑都達成，維持原路徑。"],"evidence_refs":[]},{"axis":"第四季量能","cause":null,"prior_field":null,"side_a":"執行長：十月只是幾週疲軟，第四季後半通常明顯回升，車輛運送也在增加。","side_b":"Stifel 分析師：十月航班加上 11 至 12 月的季節性，案量可能季減，而不含 PAD 第四季隱含營收約 1.98 億美元。","ruling":"不可裁決至 2 月，凍結建倉到第四季財報。指引區間寬度隱含下緣約 1.93 億美元。","evidence_level":"中","settle_metric":"第四季不含 PAD 營收。","if_then":["若低於 1.93 億美元，不追，延到 2027 年 5 月財報再判斷。"],"evidence_refs":[]},{"axis":"PAD 毛利率稀釋","cause":null,"prior_field":null,"side_a":"財務長：PAD 拉低毛利率 260 基點，整合後會改善。","side_b":"PAD 併入才一季，改善沒有資料；Q3 服務毛利率 32.2% 已低於 Q2 的 35%，財務長也預告第四季回落。","ruling":"未證、監測。預登記：連 3 季 PAD 稀釋仍至少 200 基點，整合改善的說法視為不成立。","evidence_level":"低","settle_metric":"含與不含 PAD 的毛利率差距。","if_then":["條件成立時，基本情境毛利率假設下修 1 個百分點，停止加碼。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：Terumo 買下 OrganOx，XVIVO 爭取心臟核准，管理層也稱市場擁擠。","side_b":"結構轉好：器官短缺屬結構性，HHS 腎臟計畫要多做約 2,000 顆腎移植，CMS 更重視運送事件，對垂直整合有利。","ruling":"雙向拉鋸。其他結構變數是 10 月 30 日定案的 OPO 認證規則，短期交接對捐贈量的影響尚未量化。","evidence_level":"中","settle_metric":"全美已故捐贈者量；美國肝臟營收。","if_then":["若全美已故捐贈者量連 4 季年減，停止加碼。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2 月全年利潤率指引達標才開始建倉","type":"估值rearm","maps_to":"H1","metric":"FY2027 調整後營業利益率指引中點","threshold":"至少 14%","action":"重跑研究後建首倉 2%","source_freq":"8-K 與法說，每季","date":"2027-02","evidence_refs":["supply_demand_durability#3"]},{"n":2,"text":"第四季量能低於指引下緣","type":"風險","maps_to":"R2","metric":"第四季不含 PAD 營收","threshold":"低於 1.93 億美元","action":"不追，延到 2027 年 5 月財報判斷","source_freq":"8-K，每季","date":"2027-02","evidence_refs":[]},{"n":3,"text":"兩項試驗要在第一季底前開始收案","type":"假設驗證","maps_to":"H3","metric":"ENHANCE Part B 與 DENOVO 收案狀態","threshold":"2027-03-31 前兩項都開始收案","action":"未達成則停止加碼","source_freq":"法說，每季","date":"2027-03","evidence_refs":[]},{"n":4,"text":"肝臟營收失速","type":"Single Thing","maps_to":"Single Thing","metric":"美國肝臟營收","threshold":"連 2 季季減，且全美肝移植量未同步下降","action":"清倉","source_freq":"法說，每季；OPTN 每月","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":5,"text":"XVIVO 心臟產品取得 FDA 核准","type":"風險","maps_to":"R3","metric":"FDA 核准公告","threshold":"取得核准","action":"停止加碼，直到兩季心臟營收確認未受影響","source_freq":"FDA 公告，不定期","date":"2026-Q4","evidence_refs":["competitive_share_entrants#2"]},{"n":6,"text":"利潤率與收案同時達標","type":"加碼","maps_to":"H1","metric":"TTM 調整後營業利益率；兩試驗累計收案","threshold":"至少 16%，且累計收案至少 300 例","action":"加碼至 4%","source_freq":"8-K 與法說，每季","date":"2027-12","evidence_refs":[]},{"n":7,"text":"利潤率持續低於門檻","type":"減碼","maps_to":"R1","metric":"TTM 調整後營業利益率","threshold":"低於 12% 連 2 季","action":"減碼一半","source_freq":"8-K，每季","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":8,"text":"集體訴訟不利進展","type":"減碼","maps_to":"R5","metric":"證券集體訴訟程序","threshold":"獲集體認證且出現不利和解","action":"減碼一半","source_freq":"10-Q 與 10-K，每季","date":null,"evidence_refs":["lawsuit_class_action#0","major_events#0"]},{"n":9,"text":"刑事介入或核心產品被迫停售","type":"清倉","maps_to":"R5","metric":"刑事調查；FDA 對 OCS Liver 的停售措施","threshold":"任一發生","action":"清倉","source_freq":"8-K 與 FDA 公告，不定期","date":null,"evidence_refs":["lawsuit_class_action#0"]},{"n":10,"text":"供應或關稅壓力侵蝕產品毛利率","type":"風險","maps_to":"R6","metric":"產品毛利率","threshold":"低於 75% 連 2 季","action":"停止加碼","source_freq":"法說，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":11,"text":"捐贈者量持續下滑","type":"風險","maps_to":"R7","metric":"全美已故捐贈者量","threshold":"連 4 季年減","action":"停止加碼","source_freq":"OPTN，每月","date":null,"evidence_refs":[]},{"n":12,"text":"第四季財報後複審","type":"複審日期","maps_to":"H1","metric":"全年指引與第四季實績","threshold":"財報公布後一週內","action":"依重新進場條件決定建倉或繼續不追","source_freq":"一次性","date":"2027-02-28","evidence_refs":[]}],"kill_metrics":[{"metric":"美國肝臟營收","bear_threshold":"連 2 季季減，且全美肝移植量未同步下降","window":"2 季","source":"公司法說的器官別營收","last_status":"ok"},{"metric":"TTM 調整後營業利益率","bear_threshold":"低於 12% 連 2 季","window":"2 季","source":"公司 8-K","last_status":"warning"},{"metric":"產品毛利率","bear_threshold":"低於 75% 連 2 季","window":"2 季","source":"公司法說","last_status":"ok"},{"metric":"ENHANCE Part B 與 DENOVO 開始收案","bear_threshold":"2027-03-31 前任一未開始","window":"至 2027-03-31","source":"公司法說","last_status":"warning"},{"metric":"全美已故捐贈者量","bear_threshold":"連 4 季年減","window":"4 季","source":"OPTN 月度資料","last_status":"warning"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#1","reason":"該段是 10-K 的一般性產業語句，沒有指向公司的調查、金額或時點，也無法建立可監測的門檻。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用十月航班與被研發壓低的 2026 年利潤率定價，沒有反映不含 PAD 毛利率 61.1% 與 2027 年第一季啟動的兩項試驗；但這個落差要等全年指引與實際收案才會收斂。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=30.07, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"2027 年 2 月公布的全年調整後營業利益率指引中點至少 14%","exec_line":"現價不追；2 月財報後條件達成，重跑研究並建首倉 2%；利潤率與試驗收案都達標再加到 4%。"},"reasoning":{"industry":"Q3 營收 2.03 億美元，年增 41%，有機成長 35%。產品 1.134 億美元，年增 29%，毛利率 79.2%；服務 8,960 萬美元，年增 60%，不含 PAD 年增約 43%，毛利率 32.2%，其中物流約 4,100 萬美元。器官別為肝約 1.5 億美元、心約 3,300 萬美元、肺約 200 萬美元，國際 660 萬美元。整體毛利率 58.5%，調整後營業利益率 14.2%，GAAP 13.9%。產業處在擴張期，依據是美國等候名單超過 10.4 萬人、每年約 7,000 人等不到器官，與股價無關。供需持久性判為結構性持久，但 Q3 全美已故捐贈者年減 6%，短期量會跟著捐贈數字波動。單點依賴有三個：肝臟、Fresenius Kabi 單一供應的灌注液、Andover 單一廠區。2023 至 2025 年沒有單一客戶超過營收 10%，集中度不在客戶端。","moat":"執行面，Q3 在全美捐贈者年減 6% 下，肝與心案量仍創新高，86% 需空運的任務由自有機隊完成。定價面，服務以調價轉嫁油價，產品毛利率 79.2%，定價力還在；但公司自己推出不同價位的 CHOPS 進入 DBD 心臟與肺。份額方向只有管理層口述，獨立份額數字事實表未涵蓋。對手端，Terumo 買下 OrganOx，XVIVO 心臟產品預期爭取 FDA 核准，執行長在 Q3 法說也說現在是非常擁擠的市場。與直接對手的投入資本報酬差距無法計算，所以方向證據最多支持持平，不標擴大。這個判斷可能錯在肝臟份額實際上比外部證據顯示的更穩。","growth":"成長以量為主，價格次之，併購很小，沒有回購。共識 FY2026 至 FY2028 EPS 年化約 48%，由 1.51 美元到 3.31 美元；FY2027 共識營收只增 16.4%，差距幾乎全靠利潤率擴張。以 FY2025 稀釋 EPS 4.87 美元為基期的三年 CAGR 是負 12.1%，但基期含非營業項目，不能用。EPS 分析師家數事實表未涵蓋，營收 FY1 為 9 家、FY2 為 12 家。內生上界無法計算，缺口歸因於利潤率擴張。滲透率低於 35% 且有 Part B、DENOVO、腎臟三條具名曲線，所以五年後空間判寬；反例是占美國移植營收約 81% 的肝臟 2025 年滲透率已達 36%，新曲線若落空，空間會明顯變窄。","governance":"FY2025 FCF 1.336 億美元，FCF／淨利 0.70，但淨利含非營業項目；TTM FCF 利潤率 11.82%。Q3 SBC 1,210 萬美元，占營收 6.0%，占 GAAP 營業利益 43%。現金 4.93 億美元，含租賃總債務 8.67 億美元，淨負債 3.74 億美元；2026 年利息支出約 2,900 萬美元，其中新總部融資租賃 1,540 萬美元。本包未見回購或配息，錢主要投 OCS Kidney、次世代 OCS、ENHANCE 與 DENOVO，Q3 調整後研發年增 91%。近三年現金去向四分事實表未涵蓋。稀釋均股 4,080 萬股明顯高於流通股 3,473 萬股，差額的組成事實表未涵蓋。","valuation":"88.24 美元以 10% 年化滾五年是 142 美元，除以 25 倍得 EPS 5.68 美元，約等於 16 億美元營收加 21% 營業利益率。這個條件我部分相信，因為不含 PAD 毛利率已達 61.1%，但 2027 年利潤率沒有方向。短期上檔：FY2028 共識 EPS 3.31 美元乘 33 倍約 109 美元，約 +24%。三年上檔：FY2030 基本情境 EPS 5.30 美元乘 27 倍約 143 美元，約 +62%。賣方目標價在 6 月平均 134 美元，後續約 124.45 美元但日期不一，全距約 70 到 178 美元，最高與最低約 2.5 倍，分歧大，因此下調對報酬不對稱的信心。賣方目標價多數早於 Q3，現價低於均值的幅度只作參考，不作買進理由。","premortem":"份額增加只有管理層口述，Q3 美國移植營收季增僅 1%。管理層紀錄有落差：Q2 法說執行長對乾跑先否認後又承認可能，對歐洲補償也當場更正；CHOPS 510(k) 從 2027 上半年延到下半年，Part B 的催化從第四季延到 2027 年第一季。財務長在兩次法說之間換人，新任不對 2027 年利潤率給方向。歷史最大回撤、訴訟金額事實表未涵蓋。價值陷阱判中度，依據是兩項衰退信號亮燈，其中一項受 FY2025 非營業項目影響，另有三項資料缺口。"},"plain":{"six":{"how_it_makes_money":"賺的是每一例移植的耗材費與服務費，錢卡在 OCS 一次性耗材這一節；肝臟占美國移植營收約 81%，是最大的單點依賴。","moat":"機制是 OCS 裝置、NOP 取器服務與自有機隊綁成一條服務線；目前仍在拿份額，但對手資本變大，方向判持平。","growth":"2025 年三器官滲透率約 26%，加上腎臟與歐洲，五年後仍有成長空間，但第二曲線目前還沒有營收。","capital":"資本配置偏弱：沒有回購，SBC 稀釋略超標，資金全壓在研發與臨床，回報要到 2027 年後才看得到。","valuation":"現價要賺 10% 年化，FY2031 EPS 要到約 5.7 美元、終端 25 倍；這接近我的基本情境，判合理，不算便宜。","how_wrong":"最可能看錯三件事：肝臟份額不如管理層講的穩、2027 年利潤率再次讓位給投資、試驗時程繼續往後。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用十月航班與被研發壓低的 2026 年利潤率定價，沒有反映不含 PAD 毛利率 61.1% 與 2027 年第一季啟動的兩項試驗；但這個落差要等全年指引與實際收案才會收斂。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月第四季財報與全年指引，調整後營業利益率指引中點至少 14% 才建倉；現價不追。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":88.24,"week26_return_pct":30.07,"consensus_rev_3m_pct":-3.21,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2025 稀釋 EPS 4.87 美元含非營業項目，淨利 1.903 億美元高於營業利益約 1.086 億美元，差額事實表未拆解，所以 trailing 24 倍不能當便宜證據。改用 FY1 與 FY2 前瞻錨定；FY1 分母被研發壓低，2026-11-07 共識快照也未顯示 Q3 後的修正。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"regulatory","event":"XVIVO 心臟冷灌注 FDA 核准進度","impact":"中","watch":"是否取得核准，以及是否影響 Part B 收案。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年全年指引，新財務長第一份全年指引","impact":"高","watch":"調整後營業利益率指引中點是否至少 14%，第四季不含 PAD 營收是否至少 1.93 億美元。"},{"date":"2027-Q1","date_precision":"quarter","type":"regulatory","event":"ENHANCE Part B 與 DENOVO 開始收案","impact":"高","watch":"2027-03-31 前兩項是否都開始收案。"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"上半年在義大利、荷蘭、比利時推出 OCS 與 NOP","impact":"中","watch":"標案數量與國際營收成長。"},{"date":"2027-Q4","date_precision":"quarter","type":"regulatory","event":"下半年目標取得 CHOPS 510(k)","impact":"中","watch":"時程是否再延後，以及定價。"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"下半年 OCS Kidney 首例人體使用","impact":"高","watch":"是否如期完成，以及試驗設計與對照組。"}],"_projected_from":"v19"}
```
