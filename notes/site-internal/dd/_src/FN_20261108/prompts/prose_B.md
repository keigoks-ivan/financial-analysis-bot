你是 stock-analyst v20 的**散文層（prose）agent**，標的 FN（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：FN　日期：2026-11-08　archetype：None　前份裁決：2026-09-05　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1552B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（427B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（989B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1530B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（825B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（390B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（851B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2104B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3397B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3212B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1552           3814-5448      5 條（2–6 內）  
s3                  8000         427           5301-7573      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3344          8159-11656      5 條（2–6 內）  
s6                 11000         390          7427-10610      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         851           1854-2649      5 條（2–6 內）  
s10                 5000        2104           2027-2896      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3212           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4422B；至少需散文≈40.58KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−52.6%
−47.35
−45%
−37.6%
−35%
−35
−23.28%
−19.7%
−1.374
0
0.01
0.38%
0.4
0.4%
0.6
0.62
0.7
0.73
0.75
0.76%
0.97%
1
01
1.026
1.3%
1.5%
1.56%
1.587
1.6
1.67
1.78
1.782
1.8
02
2
2.5
2.53
2.8
2.99%
3%
3
03
3.51
4
4%
4.1
4.10
4.2
4.25
4.34
4.44
4.5%
4.6%
4.7
4.73
5
5%
05
5.11%
5.2%
5.48
5.6
5.8%
06
6
6.5
6.77
7
7.1
7.57
7.575
7.6
7.7
7.77
8%
8
08
8.1
8.29%
8.8%
9
09
9.23%
9.3%
10
10%
10.04%
10.1
10.5%
10.7%
10.8%
11
11.3%
11.4
11.46%
11.5%
11.95%
11.99%
12%
12
12.09%
12.1%
12.35%
12.7%
12.71%
13
13.05
13.57
13.75
13.81
14
14%
14.25
14.74
14.745
15
15%
15.5
16
16%
16.3%
16.59
16.6
17
17%
17.23
17.4
17.4%
18
19
19.7%
19.72
19.9
19.9%
20%
20
20.5
20.7
20.8
21
22.8%
23.1
23.3%
23.35%
23.5%
23.5
23.7%
24.0
24
24.11
24.69
25%
25
26
27.5
28%
28.0
28
28.4
28.4%
29
29.1%
29.4%
29.74
30%
30
30.2
30.53%
31
31.6%
32.5%
32.5
34
34.2%
34.5
35%
35
35.1%
36%
37.6%
38.16%
39.5%
41
42
42.8%
43%
45
45.91%
46.4%
47
47.35%
49
51%
52
52.6%
53%
53.5%
57.4%
60
65%
68.8%
69%
70
72.3%
72.3
76.7
77.3%
78%
80
80%
80.7
80.72
91%
95%
96%
100%
100
104
115
125
130
140
150
150%
155
160
204
227.5
249.7
250
304
327.13
350
$350
380
384
385
388.86
407.4
420
624.33
800
846
2026
2027
2028
20261108
1,012
1,120
1,600
2,000
2,100
2,130
3,240
4,490
5,740
7,500
7,700
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
{"meta":{"ticker":"FN","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Fabrinet"},"oneliner":"Fabrinet 營收年增 51%，營益率守住 10.8%，股價卻跌掉近一半，預估本益比剩 16.6 倍；但自由現金流轉負、補足稅沒算進 EPS，現價合理，還稱不上便宜。","thesis":{"H":[{"id":"H1","text":"資料中心需求把營收帶到 FY2028 約 80 億美元，Building 10 的新產能能被填滿。","2y":"FY2028 營收≥76.7 億美元（共識 80.72 億的 95%）","5y":null,"10y":null,"threshold":"FY2028 營收≥76.7 億美元；Q2 FY27 資料中心 QoQ≥8%","source":"季報營收分類與法說；共識來自 Koyfin 與 yfinance 快照","drift_rule":"TTM 營收落後路徑連 2 季≥5% 為削弱，連 3 季≥10% 為反轉"},{"id":"H2","text":"客戶與產品持續分散：NVIDIA 下滑由 Cisco、Amazon、Nokia 與新收發器客戶補上，OCS、NPO、CPO 成為下一條曲線。","2y":null,"5y":"FY2030 前 OCS、NPO、CPO 合計年營收≥10 億美元，且單一客戶占比≤25%","10y":null,"threshold":"管理層或 10-K 揭露的新案營收≥10 億美元；單一客戶≤25%","source":"10-K 重要客戶表與法說","drift_rule":"連 4 季偏離路徑≥5% 為削弱，連 6 季≥10% 為反轉；若新案營收始終未揭露，視為無法驗證並下修跑道判斷"},{"id":"H3","text":"擴產不稀釋資本報酬：ROIC 維持 25% 以上，Building 10 後自由現金流轉正。","2y":"FY2028 FCF 利潤率≥3%，non-GAAP 營益率≥10.5%","5y":"同一口徑 ROIC≥25%","10y":null,"threshold":"FY2028 FCF 利潤率≥3%；non-GAAP 營益率≥10.5%","source":"10-K 現金流量表、季度法說、第三方 ROIC 資料","drift_rule":"TTM 偏離連 2 季≥5% 為削弱，連 3 季≥10% 為反轉"}],"R":[{"id":"R1","text":"擴產走在需求前面：2027-01 產能約 100 億美元，Building 11 動工，客戶預測卻不是訂單。","h_ref":"H1","clock":"🔥","threshold":"Building 10 完工後連 4 季，年化營收÷總產能低於 65%","evidence_refs":["ems_utilization_capex_cycle#1","ems_utilization_capex_cycle#2"]},{"id":"R2","text":"零組件短缺壓住出貨，雷射、記憶體、ASIC 偏緊，為特定客戶採購的料也難轉用。","h_ref":"H1","clock":"⚡","threshold":"季營收低於指引下緣，且管理層歸因供應","evidence_refs":["supply_demand_durability#0","geo_supply_chain#2"]},{"id":"R3","text":"客戶自製、第二供應商或 CPO 把製造環節拿走。","h_ref":"H2","clock":"🐢","threshold":"任一前四大客戶營收金額年減≥25%；或 FY2029 前 NPO 與 CPO 營收仍接近零","evidence_refs":["customer_second_source#0","customer_second_source#1","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"泰國集中與貿易限制：出口管制可能延伸到泰國，關稅再升級時成本未必能轉嫁，中國營運也要承擔當地風險。","h_ref":"H3","clock":"🔥","threshold":"non-GAAP 毛利率連 2 季低於 11.5%，且管理層歸因關稅或貿易限制","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R5","text":"Pillar 2 補足稅落地：泰國抵減若未實施，non-GAAP EPS 約高估 12.7%。","h_ref":"H3","clock":"🔥","threshold":"FY2027 底未實施抵減，且單季補足稅≥non-GAAP 淨利 10%","evidence_refs":[]}],"single_thing":{"description":"資料中心營收連兩季環比下滑（2028 年中前）。","why_fatal":"資料中心占營收 53%，貢獻最新一季年增金額的 69%；一旦反轉，Bear 的 FY2031 EPS 17 美元只有 Base 34 美元的一半，而 Building 11 已開工，資本收不回來，是模型中最大的單一敏感項。","if_happens":"第一季環比下滑就停止加碼；連兩季下滑則清倉，不等 Building 11 完工。","how_monitor":"每季法說的營收分類，比較資料中心營收對上季，同時看年化營收÷產能。","probability":"約 25%（12–24 個月，判斷值，假設 Bear 機率 30% 中多數落在 FY2028–29，沒有統計基礎）"}},"appendix_a":{"growth_durability":7,"quality_score":6.5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.57,"peg_fy2":0.6,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":13.05,"FY2027E":19.72,"FY2028E":24.11,"FY2029E":29.74},"fy_end_month":6,"eps_basis":"FY2026A 為 GAAP 稀釋 EPS 13.05，事實表未涵蓋 FY2026 non-GAAP EPS；FY2027E 到 FY2029E 為 Koyfin 共識，由上半年 EPS 與指引推斷為 non-GAAP，家數事實表未涵蓋（營收共識為 7 位分析師）。財年於 6 月底結束。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/scenario.json","archetype":{"primary":"EMS/ODM","secondary":"品質複利成長","confidence":"中","fingerprint":"約 12% 毛利、代工收費、客戶集中、需求跟著 AI 資本支出，但資本報酬高於一般代工。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性需求疊加週期斜率：資料中心光互連需求持久，但付款者是 AI 資本支出，客戶預測不是訂單；FN 新增產能在 2027-01 達約 100 億美元，廠房建成後不可逆。來源為 2026-11-02 與 2026-08-17 法說。","bargaining":{"up":"雷射、記憶體、ASIC 偏緊，上游較強；管理層 2026-11-02 稱拿到公平甚至超額的配額。","down":"前四大客戶占 57.4%，對代工議價強，毛利率四年由 12.71% 降到 11.99%。","geo":"多數資產與製造在泰國，北美以外出貨占 77.3%，並受出口管制外溢影響。"},"profit_pool_dir":"利潤留在元件與設計端，LITE 與 COHR 毛利率 45.91%、38.16%，FN 為 11.95%；未見利潤往代工端移動，五年利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM、滲透率與利潤池占比，無可引用來源；成長判斷改以客戶、產能與分部數字為依據，屬已知資料缺口。"}},"moat":{"mechanism":"精密光電的量產製程與良率知識，加上新案重新驗證的轉換成本。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定：Q1 FY27 營收高於指引，Nokia、Amazon 升為一成以上客戶，多家收發器新客戶爬坡。定價面穩定：毛利率四年略降，營益率回升。反向證據是 NVIDIA 金額兩年約減 25%，管理層 2026-08-17 對此與 1.6T 時程未正面回答，所以不標擴大。","threats":[{"level":"🟡","text":"客戶自製或導入第二供應商：10-K 揭露客戶整併後曾因自製而減少需求，少數客戶流失會造成重大影響；具名的第二供應商報導未找到。","p":30,"evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"level":"🟡","text":"CPO 與全電短距連結可能改變組裝製程，封測廠也可能進入；證據來自第三方與風險因子，FN 已有 NPO 與 CPO 案但尚無營收。若量產案流向封測廠，升級為架構替代。","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"level":"🟡","text":"其他代工與 ODM 進入目標市場，或產業整併產生更大對手，可能帶來降價與份額流失。","p":25,"evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心與電信網路，決策者是設備 OEM 與雲端業者，付款者是它們的資本支出。連接需求是真的，資料中心營收年增 78%；但客戶預測不是訂單，需求持久，金額節奏不持久。"},{"item":"決策層級","level":"🟡","text":"替代要看單一產品案：10-K 稱許多產品 FN 是唯一外包製造商，新案又要重新驗證，短期難換。但 NVIDIA 金額兩年約減 25%，顯示份額可能在產品世代切換時移走，原因事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的利潤留在元件與設計端：LITE 毛利率 45.91%、COHR 38.16%，FN 11.95%。前四大客戶占 57.4%，部分有自製能力。FN 毛利率四年約降 0.7 個百分點，沒有多分到，也沒有被明顯擠壓。"},{"item":"社會容忍度","level":"🟢","text":"FN 是企業間製造服務，不面對消費者定價，沒有社會定價上限；政策風險在出口管制與關稅，已列入風險。"}],"roiic":32.5,"reinvest_rate":72.3,"endo_ceiling":23.5,"formula_note":"事實表缺折舊與營運資金變動，再投資以 NOPAT 減 FCF 近似。NOPAT＝營業利益×(1−4%)；FY2025 與 FY2026 再投資 5.48 億÷NOPAT 合計 7.575 億＝72.3%；增量 ROIC＝FY2024 到 FY2026 NOPAT 增加 1.782 億÷5.48 億＝32.5%。若稅率改 15%，增量 ROIC 約 34.2%，再投資率約 68.8%，內生上界仍為 23.5%。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","FN":11.95,"CLS":11.46,"JBL":9.23,"LITE":45.91,"COHR":38.16,"unit":"%"},{"metric":"營業利益率","FN":10.04,"CLS":8.29,"JBL":5.11,"LITE":23.35,"COHR":14.11,"unit":"%"},{"metric":"FCF 利潤率","FN":-3.73,"CLS":2.99,"JBL":3.82,"LITE":9.52,"COHR":-23.28,"unit":"%"},{"metric":"研發密度","FN":null,"CLS":0.93,"JBL":0.08,"LITE":12.47,"COHR":10.18,"unit":"%"}],"competitors":[{"name":"CLS","gm":11.46,"om":8.29,"fcf_margin":2.99,"rd_intensity":0.93,"strategy_note":"毛利率與 FN 接近，FCF 利潤率 2.99%；同一資料站 ROIC 39.5%，是最強的代工對照，也被 10-K 列為光學製造對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"JBL","gm":9.23,"om":5.11,"fcf_margin":3.82,"rd_intensity":0.08,"strategy_note":"毛利率 9.23%、營益率 5.11%，被 10-K 列為對手，威脅在爭取新案，現有案轉移的證據事實表未涵蓋。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"LITE","gm":45.91,"om":23.35,"fcf_margin":9.52,"rd_intensity":12.47,"strategy_note":"既是長期客戶也是上游，毛利率 45.91%；2026-11-02 傳出與 Marvell 的併購後，委外比例可能改變，需要觀察。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"COHR","gm":38.16,"om":14.11,"fcf_margin":-23.28,"rd_intensity":10.18,"strategy_note":"毛利率 38.16%、FCF 利潤率 −23.28%，上游同樣大舉投資，顯示擴產不只 FN 一家；與 FN 的直接重疊程度事實表未涵蓋。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主：客戶新案與產能爬坡；價格貢獻事實表未涵蓋；併購與回購貢獻可忽略。","runway_years":"事實表未涵蓋 TAM，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段的增量 ROIC 32.5%×再投資率 72.3%＝23.5%，不另算。","segments":[{"item":"資料中心（Q1 FY27）","value":"7.77 億美元，占 53%，年增 78%，季增 16%"},{"item":"通訊基礎設施（Q1 FY27）","value":"4.44 億美元，占 30%，年增 35%，季增 8%"},{"item":"車用、工業與其他（Q1 FY27）","value":"2.53 億美元，占 17%，年增 20%，季增 8%"}],"decay_signals":["亮：毛利率年度連續下滑，12.71%、12.35%、12.09%、11.99%，Q1 FY27 年減 20 個基點。","亮：FCF 對淨利連兩年低於 0.75，FY2025 為 0.62，FY2026 為 0.01。","未亮：FY2023 到 FY2026 EPS 與營收 CAGR 差 4.1 個百分點，低於 5。","未亮：SBC 占營收 0.76%。","未亮：仍在擴產，沒有停止投資。","未定：CPO 是否壓縮可服務市場，證據只有第三方分析。","無資料：核心市占、維修性資本支出、產業倍數三年走勢事實表未涵蓋。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能與新案，不靠併購支撐；併購與回購金額都小，展開也不改變判斷。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"沒有大型併購；Raytek 16% 股權約 3,240 萬美元，Q1 FY27 認列 2,100 萬美元未實現損失，規模不足以計算已實現報酬。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q1 FY27 均價約 380 美元，以 FY2027E EPS 19.72 計買入收益率 5.2%，計入補足稅約 4.5%；事實表未涵蓋 10 年期公債殖利率，無法比較。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 年化約 4,490 萬美元，占市值約 0.38%，低於 1.5%。","grade":"過"}]},"valuation":{"basis":"以 FY2027E non-GAAP EPS 的 Forward P/E 為主，計入 Pillar 2 補足稅後的倍數作對照；同業 Fwd P/E 事實表未涵蓋。","tier":"光通訊代工（低毛利、高資本報酬）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業 Fwd P/E，無法當估值錨；估值改用自身現值與情境路徑。"},"fwd_pe":16.59,"peg":0.73,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"名目 16.59 倍看起來便宜，但分母排除了經常性的補足稅，計入後約 19 倍，用 Q2 指引 GAAP 與 non-GAAP 差距換算約 20.7 倍；FCF 為負，PEG 0.73 只在 FY2029 共識成立時有效。真正五年分位無法計算，只有四個年度端點的 29.4%。綜合為合理，不到便宜。","upside_short_pct":17.4,"upside_mid_pct":28.4},"trap_analysis":{"verdict":"🟡","label":"現金轉換與毛利率兩項訊號亮起，尚未到陷阱。"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"AI 資本支出是占營收 53% 的資料中心業務的共同來源；Building 11 動工，總產能規劃上修到 160 億美元。第三方分析另指 CPO 與全電短距連結可能縮小可服務市場，客戶整併也曾帶來自製。","assumption":"管理層看到的客戶預測能轉成訂單，且架構改變時 FN 仍是製造方。","consequence":"FY2029 起營收回到約 60 億美元，FY2031 EPS 17 美元×12 倍＝204 美元，比現價低 37.6%；谷底給 10 倍時約低 52.6%。","ruling":"採納為 Bear 情境，機率 30%，與 Single Thing 是同一個故事。CPO 替代部分反駁：證據只來自第三方網站，FN 已有 NPO 與 CPO 案，但尚無營收，無法排除。","watch":"資料中心營收 QoQ、年化營收÷產能、10-K 重要客戶表。","evidence_refs":["ems_utilization_capex_cycle#1","customer_second_source#0","substitute_technology#0","substitute_technology#1"],"fact_refs":["f_week26_return_pct","f_ma_w250"]},{"view":"論點成功但股東經濟變差","evidence":"FY2026 營收增 36%，FCF 只有 304 萬美元；Q1 FY27 FCF −1.374 億，營運現金流 2,130 萬對去年同期 1.026 億，公司歸因應收帳款增加。客戶集中也使應收集中。Non-GAAP EPS 又未計補足稅。","assumption":"Building 10 完工後資本支出回落，營運資金增速放緩，現金轉換恢復。","consequence":"Building 11、12 與新址接續投入，營收達標但現金長期被吃掉，EPS 複利無法變成股東現金，合理倍數應低於名目 EPS 所示。","ruling":"採納：這是目前最接近事實的風險。Base 給 15 倍而非現行倍數，並把 FY2028 全年 FCF 為負列為減碼條件。反駁部分：淨現金 6.77 億，短期沒有資金壓力。","watch":"單季 FCF、營運現金流對淨利、應收帳款增速對營收增速、單季補足稅金額。","evidence_refs":["ems_utilization_capex_cycle#2","ems_roic_asset_turnover_benchmark#2","customer_concentration_credit#2"],"fact_refs":["f_kpi3_non_gaap_fcf","f_peer_fn_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"股價跌 47.35% 後名目本益比 16.59 倍，但計入補足稅約 19 倍，用 Q2 指引 GAAP 差距換算約 20.7 倍；trailing 24.69 倍。","assumption":"一般直覺認為跌近一半就便宜。","consequence":"用 15 倍與 Base 路徑，年化回報約 10%，只算中等；要更好的回報必須相信共識 FY2029 EPS 29.74 能實現，而這段超過內生上界。","ruling":"部分採納：價格沒有貴到反映過度，但跌幅本身不是安全邊際，只支持分批，不支持一次買足。","watch":"股價÷當年度共識 EPS，以及補足稅抵減是否實施。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_current"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 407.4 → 本次 327.13（-19.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=407.4","side_b":"本次 price_at_dd=327.13","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 407.4 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 407.4 美元：Bull 價 1,012、Bear 價 227.5，五年期望值 +46.4%，基準年化 8.8%，不對稱比 2.8","side_b":"本次情境、股價仍用 407.4 美元：Bull 價 846、Bear 價 204，五年期望值 +23.3%，基準年化 4.6%，不對稱比 1.8","ruling":"先換情境、股價不動：五年期望值少 23.1 個百分點，基準年化少 4.2 個百分點。不對稱比由 2.8 變為 1.8。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 407.4 美元：五年期望值 +23.3%，基準年化 4.6%，不對稱比 1.8","side_b":"本次情境、股價 327.13 美元：五年期望值 +53.5%，基準年化 9.3%，不對稱比 3.51","ruling":"再換股價、情境不動：起點價下跌 19.7%，五年期望值多 30.2 個百分點，基準年化多 4.7 個百分點，不對稱比由 1.8 升到 3.51。合計五年期望值比前份多 7.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"基本面結論五項未變的原因","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5"],"side_a":"前份：評級 B、估值中性、陷阱中度、護城河持平、五年後跑道寬，股價 407.4 美元。","side_b":"本次：五項結論不變，股價 327.13 美元。新證據包括 Q1 FY27 超出指引、Building 11 上修、FCF −1.374 億、補足稅持續。","ruling":"好消息與壞消息互相抵銷。營收與產能證據改善，現金轉換與 EPS 品質轉差，所以五項都不動。估值倍數雖降，但分母有爭議，不升為便宜。","evidence_level":"一手財報與法說","settle_metric":"Q2 FY27 的資料中心 QoQ 與營運現金流","if_then":["若 Q2 FY27 營收≥1,600M 且營運現金流轉正，則加碼第二筆。","若毛利率連 2 季低於 11.5%，則減碼三分之一。"],"evidence_refs":["ems_utilization_capex_cycle#2"]},{"axis":"公司分類與循環位置","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份分類為品質複利成長，循環位置未填。","side_b":"本次主分類改為 EMS/ODM，次分類為品質複利成長，循環位置為中循環。","ruling":"改分類是因為本輪明確採代工視角，生意本身沒變。倍數與情緒偏買，需求與擴產不在低點，訊號矛盾，判為中循環、未觸發循環買點。循環讀數只作平行參考，不改長期判斷。","evidence_level":"財報結構與法說","settle_metric":"客戶庫存資料，目前事實表未涵蓋","if_then":["若資料中心營收連兩季環比下滑，循環位置改判晚循環以後，清倉。","若需求回落後股價跌破 249.7 美元且 ROIC 維持 25% 以上，再分批反買。"],"evidence_refs":[]},{"axis":"裁決、機率與回撤區間","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：觀望，機率 25／45／30，最大回撤 −45%，股價 407.4 美元。","side_b":"本次：機率維持 25／45／30，回撤區間 −35% 到 −55%，股價 327.13 美元，下跌 19.7%；裁決與角色由本次輸入重新產生。","ruling":"股價下跌改變進場條件，不改變情境機率。Bear 30% 是共識超過內生上界後的下限，新證據正負相抵，不調整。","evidence_level":"價格資料與判斷","settle_metric":"Q2 FY27 財報","if_then":["若股價續漲而財報未驗證，則不追。","若股價下跌而基本面無損，則分批反買。"],"evidence_refs":[]},{"axis":"重新進場與加碼門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"11 月 Q1 FY27 財報總資料中心 QoQ >0 且 datacom QoQ ≥0；或回檔至 ≤$350（FY2027 本益比約 19x）且 H1-H3 檢核無損","side_b":"Q2 FY27 營收≥1,600M、資料中心 QoQ≥8% 且營運現金流轉正；或週收盤站回 104 週均線 388.86 且營收條件成立","ruling":"舊門檻已發火：股價 327.13 低於 350，資料中心 QoQ +16%。datacom 自 FY2026 第四季起不再單獨揭露，只有管理層質化說法。舊條件已用完，新門檻改看現金流，因為這是目前尚未驗證的環節，前份裁決不沿用。","evidence_level":"一手財報與法說","settle_metric":"Q2 FY27 財報","if_then":["若新門檻全部成立，則加碼第二筆。","若營收低於 1,600M，則停止加碼。"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要未提供（null）。","side_b":"資料中心營收連兩季環比下滑則清倉；FY2028 全年 FCF 利潤率為負或毛利率連 2 季低於 11.5% 則減碼。","ruling":"前份門檻在摘要中缺失，無法比對，本次重新設定，理由是資料中心占營收 53%，且現金轉換是目前最弱的一環。","evidence_level":"判斷","settle_metric":"每季財報","if_then":["若資料中心營收連兩季環比下滑，則清倉。"],"evidence_refs":[]},{"axis":"Single Thing 變更","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未提供（null）。","side_b":"資料中心營收連兩季環比下滑（2028 年中前）。","ruling":"前份內容缺失，無法比對。本次選最大敏感項：資料中心占營收 53%，並貢獻最新一季年增金額的 69%。","evidence_level":"判斷","settle_metric":"資料中心營收 QoQ","if_then":["若事件發生，第一季停止加碼，第二季清倉。"],"evidence_refs":[]},{"axis":"客戶整併對 FN 是利多還是利空","cause":"新證據","prior_field":null,"side_a":"執行長 Grady 2026-11-02：過去整併（Lumentum 併 NeoPhotonics、Infinera 併 Coriant、Nokia 併 Infinera）事後都讓 FN 業務成長。","side_b":"10-K FY2026：部分情況下客戶整併後取得自製產能，FN 需求下降。","ruling":"可調和，兩者描述不同案例。Lumentum 與 Marvell 的影響未知，管理層也說尚未與雙方談過；賣方模型應未反映，第一個驗證點是後續兩季法說。","evidence_level":"管理層原話對 10-K 風險因子","settle_metric":"10-K 重要客戶表與法說對 Lumentum 的說法","if_then":["若合併後宣布把 FN 現有案轉自製，則停止加碼。","若合併公司占比升破 10%，則維持原計畫，不因此減碼。"],"evidence_refs":["customer_second_source#0"]},{"axis":"需求能見度與訂單約束力","cause":"新證據","prior_field":null,"side_a":"執行長 Grady 2026-11-02：客戶讓 FN 看到的需求遠到看不見盡頭，成長看來可持續。","side_b":"財務長 Sverha 2026-08-17：客戶預測不是訂單承諾。","ruling":"可調和：能見度高，約束力低。FN 擴產依據的是沒有約束力的預測，這段風險落在股東身上，所以 Bear 取 30%。","evidence_level":"管理層原話","settle_metric":"年化營收÷總產能","if_then":["若 Building 10 完工後連 4 季低於 65%，則減碼一半。","若比率升破 80% 且現金流轉正，則加碼。"],"evidence_refs":["ems_utilization_capex_cycle#1"]},{"axis":"資產輕的說法與現金流","cause":"新證據","prior_field":null,"side_a":"執行長 Grady 2026-11-02：資產輕、固定成本低，即使景氣反轉也沒有增加重大固定成本。","side_b":"FY2026 FCF 幾乎為零，連兩季 FCF 為負，Building 10、11 共 350 萬平方呎屬自有廠房。","ruling":"可調和：損益面成立，固定成本約占成本 5%；現金面不成立，資本已經投下去。評價上採用現金面。","evidence_level":"法說與財報","settle_metric":"FY2028 FCF 利潤率","if_then":["若 FY2028 FCF 利潤率低於 0，則減碼三分之一。","若連 2 季 FCF 為正，則加碼。"],"evidence_refs":["ems_utilization_capex_cycle#2"]},{"axis":"EPS 分母的品質","cause":"新證據","prior_field":null,"side_a":"Non-GAAP EPS 4.34，有效稅率 4%，FY2027E 本益比 16.59 倍。","side_b":"Q1 FY27 另有 2,000 萬美元補足稅被排除，約占 EPS 12.7%；財務長稱泰國抵減尚未實施，FY2026 也有 5,740 萬美元。","ruling":"管理層的排除未證、需監測。若 FY2027 底仍未實施，且單季補足稅仍達 non-GAAP 淨利 10% 以上，排除的說法即視為不成立，改用含稅 EPS。","evidence_level":"法說原話","settle_metric":"泰國抵減實施與否、單季補足稅金額","if_then":["若 FY2027 底仍未實施，則停止加碼，估值改用含稅 EPS。","若抵減實施且單季補足稅低於淨利 5%，則恢復使用 non-GAAP 倍數。"],"evidence_refs":[]},{"axis":"三個月共識上修是否真實","cause":"方法變動","prior_field":null,"side_a":"共識 FY1 三個月上修 42.8%，由 13.81 到 19.72。","side_b":"最新一次修正只有 +0.97%。8 月 13 日的 13.81 比 Northland 2026-05 對 FY2027 的 17.23 低約 20%，當時 FY2026 尚未公布，應是財年切換所致。","ruling":"不把 42.8% 當真實上修。真實方向是小幅上修，FY1 +0.97%、FY2 +1.56%、FY3 持平。無法從事實表直接確認快照對應財年，這是推論。","evidence_level":"快照資料與推論","settle_metric":"以同一財年比對快照","if_then":["若同財年比對仍顯示大幅上修，則上調 Base 路徑前兩年。"],"evidence_refs":[]},{"axis":"現在買與現在賣的最強論證","cause":"新證據","prior_field":null,"side_a":"買：營收加速到 51%，Q2 指引年增 43%，名目 16.59 倍，淨現金占市值 5.8%，固定成本低，前份進場門檻已到。","side_b":"賣：股價在 52 週與 104 週均線之下，FCF 連兩季為負，EPS 未計補足稅，AI 資本支出週期未知，此刻大幅擴產正是週期後段常見的動作。","ruling":"可調和：基本面支持小量建立，價格與現金流證據不支持一次買足。","evidence_level":"財報與價格資料","settle_metric":"Q2 FY27 財報與週收盤對 104 週均線","if_then":["若 Q2 FY27 營收≥1,600M 且資料中心 QoQ≥8%，則加碼第二筆。","若股價續漲但財報未驗證，則不追。","若股價跌破 249.7 美元而論點無損，則分批反買。","若資料中心營收連兩季環比下滑，則清倉。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭與替代：10-K 提醒代工、ODM、封測可能進入，第三方指 CPO 改變價值鏈，NVIDIA 金額縮小。","side_b":"結構轉好：資料中心年增 78%，OCS 與 NPO 開始，雷射客戶轉向委外。其他結構變數：Lumentum 與 Marvell 併購、Pillar 2、關稅。","ruling":"雙向拉鋸：需求結構轉好，競爭與客戶結構的不確定同時上升。","evidence_level":"10-K、法說、第三方","settle_metric":"客戶占比與新案營收揭露","if_then":["若前四大客戶任一營收金額年減≥25%，則減碼三分之一。"],"evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"axis":"管理層上季承諾對帳","cause":"新證據","prior_field":null,"side_a":"2026-08-17 財務長 Sverha 指引 FQ1 營收 13.75–14.25 億美元、EPS 4.10–4.25；執行長 Grady 稱總產能規劃 125–140 億美元、Building 11 為 21 億美元。","side_b":"2026-11-02 實際營收 14.74 億、EPS 4.34，均高於指引；執行長把總產能改為 160 億美元，Building 11 改為 30 億美元。","ruling":"財測兌現，可信度加分。但產能目標 11 週內上修 14% 到 28%，部分來自每平方呎營收上升，上修速度快於可驗證的訂單。","evidence_level":"逐字稿","settle_metric":"Building 10 完工後年化營收÷產能","if_then":["若下季再度上修產能而資料中心 QoQ 低於 8%，則停止加碼。"],"evidence_refs":["ems_utilization_capex_cycle#1"]}],"triggers":[{"n":1,"text":"Q2 FY27 營收與資料中心成長驗證第一個論點。","type":"假設驗證","maps_to":"H1","metric":"Q2 FY27 營收；資料中心 QoQ","threshold":"營收≥1,600M 且資料中心 QoQ≥8%","action":"達標則加碼第二筆；營收低於 1,600M 則停止加碼","source_freq":"季報，每季","date":"2027-02"},{"n":2,"text":"資料中心營收連兩季環比下滑。","type":"Single Thing","maps_to":"Single Thing","metric":"資料中心營收 QoQ","threshold":"連 2 季低於 0","action":"第一季停止加碼；第二季清倉","source_freq":"季報，每季","date":"2028-06 前"},{"n":3,"text":"新產能沒有被填滿。","type":"風險","maps_to":"R1","metric":"年化營收÷總產能","threshold":"Building 10 完工後連 4 季低於 65%","action":"減碼一半","source_freq":"季報與法說，每季","date":"2027-03 起","evidence_refs":["ems_utilization_capex_cycle#1","ems_utilization_capex_cycle#2"]},{"n":4,"text":"零組件短缺導致營收落空。","type":"風險","maps_to":"R2","metric":"季營收對指引下緣","threshold":"低於下緣且管理層歸因供應","action":"停止加碼一季，供應改善才恢復","source_freq":"季報，每季","date":"每季","evidence_refs":["supply_demand_durability#0"]},{"n":5,"text":"關稅成本轉嫁失敗。","type":"風險","maps_to":"R4","metric":"non-GAAP 毛利率","threshold":"連 2 季低於 11.5% 且管理層歸因關稅或貿易限制","action":"減碼三分之一","source_freq":"季報，每季","date":"每季","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]},{"n":6,"text":"美國把出口管制延伸到泰國。","type":"風險","maps_to":"R4","metric":"出口管制適用範圍","threshold":"正式延伸到泰國且涵蓋 FN 主力產品","action":"清倉","source_freq":"美國商務部公告與 10-K，事件驅動","date":"未定","evidence_refs":["reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"n":7,"text":"Pillar 2 補足稅抵減沒有落地。","type":"風險","maps_to":"R5","metric":"泰國抵減實施與否；單季補足稅÷non-GAAP 淨利","threshold":"FY2027 底未實施且比率≥10%","action":"停止加碼，估值改用含稅 EPS","source_freq":"季報，每季","date":"2027-08"},{"n":8,"text":"子公司 Casix 的中國不當得利案（民事、個案）由最高院再審，求償 RMB 4 億，受影響營收事實表未涵蓋。","type":"風險","maps_to":"R4","metric":"再審判決","threshold":"判決 Casix 須賠償且金額≥RMB 2 億","action":"計入一次性損失重算淨現金；若同時引發中國業務限制則減碼三分之一","source_freq":"10-K、10-Q，每季","date":"判決日未定","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0"]},{"n":9,"text":"重新進場條件。","type":"估值rearm","maps_to":"H1","metric":"Q2 FY27 營收、資料中心 QoQ、營運現金流；週收盤對 104 週均線","threshold":"營收≥1,600M、QoQ≥8%、營運現金流>0；或站回 388.86 且營收條件成立","action":"重跑研究後建首筆，不直接買足","source_freq":"季報與週線，每季","date":"2027-02"},{"n":10,"text":"現金流證實擴產回本。","type":"加碼","maps_to":"H3","metric":"單季 FCF；non-GAAP 營益率","threshold":"FCF 連 2 季為正且營益率≥10.5%","action":"加碼到計畫部位上限","source_freq":"季報，每季","date":"2027-08 起"},{"n":11,"text":"倍數回到透支水準而現金流未改善。","type":"減碼","maps_to":"H3","metric":"股價÷當年度共識 EPS；FCF","threshold":"≥25 倍且 TTM FCF 仍為負","action":"減碼三分之一","source_freq":"每日價格與季報","date":"持續"},{"n":12,"text":"Q2 FY27 財報後全面複審。","type":"複審日期","maps_to":"H1","metric":"H1 到 H3 檢核","threshold":"財報公布","action":"依檢核結果執行加碼或停止加碼","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"資料中心營收環比","bear_threshold":"連 2 季低於 0","window":"2028-06 前每季","source":"季報營收分類","last_status":"ok"},{"metric":"年化營收÷總產能","bear_threshold":"Building 10 完工後連 4 季低於 65%","window":"2027-03 起 4 季","source":"法說揭露的產能與季度營收","last_status":"unknown"},{"metric":"自由現金流利潤率","bear_threshold":"FY2028 全年低於 0","window":"FY2028","source":"10-K 現金流量表","last_status":"warning"},{"metric":"non-GAAP 毛利率","bear_threshold":"連 2 季低於 11.5%","window":"每季","source":"季度法說","last_status":"ok"},{"metric":"前四大客戶營收金額","bear_threshold":"任一客戶年減≥25%","window":"FY2027 與 FY2028","source":"10-K 重要客戶表","last_status":"warning"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 CPO 當成對 FN 的替代，但 FN 同時承接 pluggable、NPO 與 CPO 案，架構改變換的是產品，不一定換掉製造商；週期高點的疑慮反駁不了，已放進 Bear 情境。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-47.35, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"Q2 FY27 營收≥1,600M、資料中心 QoQ≥8% 且營運現金流轉正；或週收盤站回 104 週均線 388.86 且營收條件成立","exec_line":"2027-02 財報前最多建首筆（計畫部位三分之一）；股價續漲而財報未驗證則不追，跌破 250 週均線 249.7 美元但論點無損則分批反買。"},"reasoning":{"industry":"最新一季（季末 2026-09-25）營收 14.745 億美元，年增 51%。依 2026-11-02 法說，三個分部都超過一成：資料中心 7.77 億（占 53%，年增 78%）、通訊基礎設施 4.44 億（年增 35%）、車用工業與其他 2.53 億（年增 20%）。non-GAAP 毛利率 12.1%，營益率 10.8%。產業處於擴張期，依據是連續 14 季成長、零組件全面偏緊，尚未看到砍單或庫存反轉。客戶集中是單點依賴：10-K FY2026 前四大客戶合計 57.4%（Cisco 19.9%、NVIDIA 16.3%、Nokia 10.7%、Amazon 10.5%）。NVIDIA 占比兩年由 35.1% 降到 16.3%，以總營收換算，金額約由 10.1 億美元降到 7.6 億美元。AI 熱潮中金額反而縮小，是本輪最需要解釋的數字，管理層 2026-08-17 法說沒有正面回答。","moat":"機制是精密光電的量產知識：10-K 稱許多產品 FN 是客戶唯一的外包製造商，新案重新驗證時間長，管理層也稱已在概念階段參與設計。定價權只到製造費：毛利率 11.95%、營益率 10.04%，高於 CLS 的 11.46%／8.29% 與 JBL 的 9.23%／5.11%，但遠低於 LITE 的 45.91%／23.35%。ROIC 來源不一致：opencapital 23.7%、stockanalysis 30.53%，管理層稱 30% 以上；事實表沒有投入資本，無法自算。CLS 同一來源為 39.5%，期間不同，因此看不到對最強同業的正向差距。增量報酬用營業利益×96%（Q1 FY27 non-GAAP 稅率 4%）估 NOPAT，FY2024 到 FY2026 增加 1.78 億美元，同期再投資以 NOPAT 減 FCF 近似為 5.48 億，增量 ROIC 約 32.5%，再投資率約 72.3%，內生成長上界約 23.5%。Building 10 的資本已投入但營收尚未完全反映，這個數字會受落後效應影響。可能看錯之處：若 Building 10 未滿載，下一段增量 ROIC 會明顯低於此值。","growth":"成長以量為主，價格貢獻事實表未涵蓋，回購與併購可忽略。共識三年 EPS 由 FY2026 的 13.05（GAAP）到 FY2029E 的 29.74，CAGR 31.6%；基期是 GAAP、共識是 non-GAAP，若用 2026-08-13 快照 13.81 推估 non-GAAP 基期則為 29.1%。FY2027E 到 FY2029E 兩年 CAGR 22.8%。內生上界 23.5%，缺口 8.1 個百分點：約 2.5 個是基期口徑，其餘約 5.6 個來自 Building 10 已投入資本的釋放與營益率擴張，兩者無法再拆，視為無法完全歸因；共識路徑依賴這段缺口，Base 路徑不採用。產能規劃為 2027-01 約 100 億、Building 11 後 130 億、含 Building 12 為 160 億美元，FY2028 共識營收 80.7 億只用到 2027-01 產能的八成。TAM 與滲透率事實表未涵蓋，跑道判斷只靠下一條曲線有管理層來源這一項；若 FY2030 前 OCS、NPO、CPO 沒有達到管理層說的數億美元規模，下修為中等。","governance":"FY2026 FCF 304 萬美元，對淨利 4.73 億幾乎為零。Q1 FY27 營運現金流 2,130 萬、資本支出 1.587 億，其中 7,700 萬是 Santa Clara 園區，FCF −1.374 億。現金及短投 7.57 億，淨現金約 6.77 億，占市值 5.8%。SBC 單季 1,120 萬，占營收 0.76%，年化約占市值 0.4%。回購 7.7 萬股、均價約 380 美元，比現價高 16%；董事會把額度增至 2 億美元，財務長明說優先序是先投資成長。管理層說擴產用自有資金，同季在泰國借入約 7,500 萬美元，財務長解釋為當地借款比動用美國投資便宜，金額不大，不視為資金壓力。Building 11 與潛在新廠將把資本支出推高。近三年現金去向四分與債務到期結構事實表未涵蓋。","valuation":"現價 327.13 美元，FY2027E 本益比 16.59 倍，FY2028E 13.57 倍，預估 EV/S 1.67 倍。要年化 10%，FY2031 EPS 需約 35 美元配 15 倍；Base 路徑 34 美元，幾乎剛好，所以回報只算合理。PEG 0.73 用 FY2027E 到 FY2029E 兩年 CAGR 22.8%，三年口徑缺 non-GAAP 基期。一年上檔用 FY2028E Base EPS 24.0×16 倍＝384 美元（+17.4%），三年用 FY2029E 28.0×15 倍＝420 美元（+28.4%）。真正的五年分位算不出來，事實表只有四個年度端點，trailing 本益比落在 29.4%。同業 Fwd P/E 事實表未涵蓋，無法做同業倍數對照。賣方平均目標價 624.33 美元比現價高 91%，全距 385–800 美元，來源日期不一，只視為賣方尚未下修，不當估值依據。共識 FY1 三個月上修 42.8% 很可能是財年切換造成，最新一次修正只有 +0.97%。","premortem":"衰退訊號亮兩項：毛利率連續下滑、FCF 對淨利連兩年低於 0.75，價值陷阱風險屬中度。三個假設的量化衝擊：補足稅若照 Q1 FY27 計，EPS 約少 12.7%；Cisco 若流失，營收少 19.9%；資料中心需求反轉，FY2031 EPS 由 Base 34 美元降到 Bear 17 美元。股價 26 週跌 47.35%，原因事實表未涵蓋，法說只看到投資人擔心 CPO 蠶食，不能把跌幅當安全邊際。2026-08-17 法說有四題管理層沒有正面回答：NVIDIA 下滑與競爭、1.6T 時程、雷射供應承諾、datacom 單季下滑原因，都視為資料缺口。"},"plain":{"six":{"how_it_makes_money":"賺的是精密光電的量產代工費：客戶掌握設計與品牌，FN 拿製造環節約 12% 毛利，錢主要卡在元件與設計端。","moat":"護城河持平：製程與量產良率的優勢還在，客戶分散抵銷了最大資料中心客戶金額縮小的負面，還不能說擴大。","growth":"五年後仍有跑道：資料中心光互連加上尚未出貨的 OCS、NPO 與 CPO 構成下一條成長曲線，但證據目前只有管理層說法與案件數量。","capital":"現金優先投產能，短期現金轉換很差；SBC 低，回購規模小，且買在比現價高的位置。","valuation":"現價要靠 FY2031 EPS 約 35 美元配 15 倍才有年化 10%，這個要求我相信，但回報只算合理，算不上便宜。","how_wrong":"最可能看錯在把 AI 建置高峰的 EPS 當成常態；目前還不是價值陷阱，但兩項衰退訊號已亮。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 CPO 當成對 FN 的替代，但 FN 同時承接 pluggable、NPO 與 CPO 案，架構改變換的是產品，不一定換掉製造商；週期高點的疑慮反駁不了，已放進 Bear 情境。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"EMS/ODM","price_at_dd":327.13,"week26_return_pct":-47.35,"consensus_rev_3m_pct":42.8,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"non-GAAP EPS 排除 Pillar 2 補足稅，Q1 FY27 為 2,000 萬美元，約占 non-GAAP EPS 12.7%，泰國抵減尚未實施。市場同時質疑 FY2028–29 EPS 能否實現，所以不採用 16.59 倍的便宜論證。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"capacity","event":"Building 10 完工，Building 11 動工，總產能約 100 億美元","impact":"中","watch":"完工後第一個完整季的年化營收÷產能"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q2 FY27 財報與 Q3 指引","impact":"高","watch":"資料中心 QoQ、營運現金流、毛利率是否如指引改善"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"泰國 Pillar 2 抵減是否實施（管理層未給時點，以 FY2027 底為觀察點）","impact":"中","watch":"單季補足稅金額"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"NPO 與 CPO 案開始貢獻營收","impact":"中","watch":"管理層是否量化 OCS、NPO、CPO 營收"},{"date":"2028-06","date_precision":"quarter","type":"capacity","event":"Building 11 預計完工，新增約 30 億美元產能","impact":"中","watch":"完工時年化營收是否已超過 100 億美元產能的八成"}],"_projected_from":"v19"}
```
