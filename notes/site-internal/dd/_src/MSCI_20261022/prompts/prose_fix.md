你是 stock-analyst v20 的**散文層（prose）agent**，標的 MSCI（2026-10-22）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MSCI　日期：2026-10-22　archetype：None　前份裁決：2026-09-29　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1176B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（372B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（896B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1246B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1313B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（697B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（982B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2040B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4567B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1931B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1176           4077-5824      5 條（2–6 內）  
s3                  8000         372           5340-7628      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3455          8081-11545      5 條（2–6 內）  
s6                 11000         697          7212-10303      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         982           1763-2518      5 條（2–6 內）  
s10                 5000        2040           2072-2960      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1931           2000-3069      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4785B；至少需散文≈40.22KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45
−45%
−42%
−34%
−30
−30%
0
0.13%
0.13
0.3%
0.75
0.76%
0.9
01
1
1.2
1.21
1.3
1.3%
1.5
1.5%
1.6
1.65
1.7
1.94
2
02
2%
2.2
2.22
2.4
2.9%
2.9
3%
03
3
3.26
3.34
3.5%
3.8
4
5
5%
5.1
5.2
5.385
5.6
5.7
5.85
6
6%
6.27
6.6%
07
7
7.5%
7.9%
8
8%
8.67
8.7%
8.9%
09
9
9%
9.5%
9.6
9.8%
10%
10
10.2%
10.7
10.8%
11%
11
11.1%
11.4
11.4%
11.7%
12%
12
12.1
12.4%
13.2
14
14%
14.0%
14.0
14.5%
14.6
14.85
15
15.0
15%
15.45
15.69
15.9
17.1
17.4%
18
18.7%
19
19%
19.5
19.52
20%
20
20.3
20.8
21
21.4
21.5
22
22.1
22.35
22.6
23
24
24.8%
25%
25
25.35
26%
26
26.6%
27
27.0
27.05
28
29
29.1%
29.6%
30
30%
30.97
31
31.3
32
33.0
34
34.5
34.6%
35%
36
36%
36.4%
39.5
39.9%
41.6%
42
44
44.8%
45
45.1%
46%
46.1%
46.2
49
52
53.5%
54.8%
55.7%
55.8%
56.2%
58%
59%
61.9
62.1%
63%
69.5
70
74%
82.4%
83.0%
83%
93%
94.4%
94.5%
95%
95.3%
96.5%
97%
98%
100
100%
104
150%
250
351
400
401.4
439
440
474
536
542.72
562
604
604.46
692
700
722
742
746
760
800
805
884
2024
2026
2027
2035
20261022
1,000
1,185
1,264
1,500
2,000
3,010
5,000
7,310
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
{"meta":{"ticker":"MSCI","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"MSCI Inc."},"oneliner":"全球股票基準與投資分析的標準制定者，Q3 淨新銷售創紀錄、留存回升；但 FY1 本益比 31 倍，管理層明言不擴張利潤率，五年基準年化約 9%。生意好，價格只算合理，等 536 美元以下再加碼。","thesis":{"H":[{"id":"H1","text":"Index 訂閱是主引擎，有機訂閱 run rate 維持兩位數成長","2y":null,"5y":"年增 ≥10%","10y":null,"threshold":"Index 有機訂閱 run rate 年增 ≥10%（Q3 為 11.7%）","source":"MSCI 季報新聞稿與法說","drift_rule":"連 4 季低於 9.5% 為削弱，連 6 季低於 9% 為反轉"},{"id":"H2","text":"客戶黏著不被 AI 與自建侵蝕：總留存率守住、訂閱整體穩定成長","2y":null,"5y":"總留存率 ≥94.5%，訂閱 run rate 年增 ≥8%","10y":null,"threshold":"總留存率 ≥94.5%（Q3 約 95%）；訂閱 run rate 年增 ≥8%（Q3 為 9%）","source":"MSCI 季報新聞稿","drift_rule":"連 4 季偏離門檻 ≥5% 為削弱，連 6 季偏離 ≥10% 為反轉"},{"id":"H3","text":"經營槓桿不被再投資全部吃光，每股獲利維持雙位數成長","2y":"調整後 EPS 年增 ≥12%","5y":null,"10y":null,"threshold":"FY2026、FY2027 調整後 EPS 年增 ≥12%（Q3 為 14%）","source":"MSCI 季報新聞稿與年度指引","drift_rule":"連 2 季偏離門檻 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"}],"R":[{"id":"R1","text":"BlackRock 集中度上升且擁有議價權：占合併營收由 FY2023 的 9.8% 升至 FY2025 的 10.8%，占 Index 分部 18.7%，同時是競爭者；修約後部分大型產品底價降低（2026-07-21 CFO）","h_ref":"H2","clock":"🐢","threshold":"BlackRock 占 Index 分部營收升破 20%，同時掛鉤 ETF 平均基點年降逾 10%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_second_source#0","competitive_share_entrants#2"]},{"id":"R2","text":"AI 讓對手低價替代、客戶自建指數與分析，ESG 評等首當其衝","h_ref":"H2","clock":"🔥","threshold":"總留存率＜93% 連 2 季","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"id":"R3","text":"費用指引連續上修，管理層明言不擴張利潤率，EPS 成長可能低於共識","h_ref":"H3","clock":"⚡","threshold":"調整後 EBITDA 利潤率＜58% 連 2 季","evidence_refs":["capital_markets_pricing#1"]},{"id":"R4","text":"資產費是股市 beta：股市空頭、主動 ETF 分流、新興市場地緣與關稅衝擊，會同時壓資產規模與基點","h_ref":"H3","clock":"🔥","threshold":"資產費 run rate 年增連 2 季轉負","evidence_refs":["end_markets#4","geo_supply_chain#0","reg_tariff_export#0"]},{"id":"R5","text":"永續與氣候分部需求下行，加上 EU ESG 評等新規的授權與合規成本","h_ref":"H2","clock":"🐢","threshold":"永續與氣候分部淨新銷售連 2 季為負","evidence_refs":["regulatory_antitrust#1"]}],"single_thing":{"description":"BlackRock 宣布把掛鉤 MSCI 指數的主要 ETF 改用他家或自家指數，或要求大幅降低資產費","why_fatal":"BlackRock 占 FY2025 營收 10.8%、Index 分部 18.7%，其中 96.5% 是資產費，幾乎全數落到利潤；其他發行商也會跟著議價，基準不可替代的敘事被打破，倍數同步下修","if_happens":"清倉並重跑研究；EPS 約少一成，倍數往 20 倍靠攏","how_monitor":"SEC 8-K 重大合約項目、BlackRock 產品公告、10-K 最大客戶占比","probability":"約 3%（ETF 授權合約 2026-01 已延至 2035-03-31）"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟡","long_term_confidence":"高","fpe_fy2":27.05,"peg_fy2":1.94,"stress":{"pass":4,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":15.69,"FY2026E":19.52,"FY2027E":22.35,"FY2028E":25.35},"fy_end_month":12,"eps_basis":"共識為調整後 EPS（Koyfin 快照）；FY2025A 只有年報 GAAP 稀釋 EPS 15.69，與共識口徑不同，以此為基期算的三年成長會被高估；可比的共識成長以 FY2026→FY2028 年增約 14.0% 為準"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"高留存訂閱加資產費，毛利率 83%，FCF 對淨利轉換率約 1.2 倍"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久（訂閱端）：留存率 95.3%（前一年 94.4%），Index 留存逾 97%；資產費端屬週期性，隨股市反轉（Q2 新聞稿、2026-10-20 CFO）","bargaining":{"up":"上游是資料與雲端供應商，可替代，議價權在 MSCI","down":"下游大型資產管理商可壓資產費基點：H1 掛鉤 ETF 平均基點下滑，BlackRock 修約後部分大型產品底價降低（2026-07-21 CFO）","geo":"營收跨三大區；Q3 淨新銷售 EMEA +74%、亞太 +36%、美洲 +26%"},"profit_pool_dir":"利潤池往客製指數、交易生態（避險基金、券商、做市商）與私募資料移動，MSCI 有跟上：客製指數訂閱 run rate +26%、私募資本方案 +19%","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率；利潤池遷移改用分部 run rate 成長代理，見成長題分部表"}},"moat":{"mechanism":"全球股票基準標準：基金合約、公開說明書與績效考核綁定 MSCI 指數，資產費與訂閱兩頭收；避險基金、券商的交易生態圍繞指數建立，掛鉤產品越多越難換","execution":9,"pricing":8,"grade":"A","trend":"→","trend_evidence":"留存率 95.3%（前一年 94.4%），Q3 約 95%、年增 30bp，Index 留存逾 97%；但掛鉤 ETF 平均基點下滑（H1 新聞稿），BlackRock 修約後部分產品底價降低（2026-07-21 CFO）","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以營益率與 FCF 利潤率差替代","threats":[{"level":"🟡","text":"AI 讓對手以低價推出替代品，客戶也可能自建客製指數與風險分析；ESG 評等最容易被 AI 複製。目前留存率仍在上升，客戶偏好透過 MSCI 自家應用直連（2026-10-20 Munari），屬點對點威脅","p":30,"evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"BlackRock 同時是最大客戶、股東與競爭者，可壓資產費，或把產品換到自家／他家指數；合約延至 2035 年，短期機率低","p":15,"evidence_refs":["competitive_share_entrants#2","customer_concentration_credit#1"]},{"level":"🟡","text":"主動型 ETF 數量已超過被動型，資金若持續由被動轉主動，資產費成長會變慢；但主動 ETF 也在採用 MSCI 的主動 ETF 授權與投組工具","p":25,"evidence_refs":["end_markets#4"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（投資組合經理、風控）、決策者（投資長、產品委員會）、付款者（資產管理商、ETF 發行商）三方一致：基準是募資與績效考核的必需品，延後購買的代價高；對標資產近 23 兆，留存率 95.3%"},{"item":"決策層級","level":"🟢","text":"替代性要在基金合約層衡量：換基準要改公開說明書，並經董事會與投資人揭露；Index 留存逾 97%、資產管理客戶 98%（2026-10-20 CFO），BlackRock 合約延至 2035-03-31"},{"item":"價值鏈分配","level":"🟡","text":"ETF 發行商自身面臨費率壓縮，會向上游壓指數費：掛鉤 ETF 平均基點下滑，BlackRock 修約後部分產品底價降低；最大客戶同時是競爭者，有自建能力"},{"item":"社會容忍度","level":"🟡","text":"歐美監管者與媒體高度關注指數業；MSCI Limited 為英國 FCA 授權的基準管理機構，EU ESG 評等規範自 2026-07-02 起要求 ESMA 授權。資產費若推到經濟上限容易招來監管，實際做法是讓基點逐步下滑來換規模"}],"roiic":"事實表未涵蓋投入資本與折舊攤銷，無法照公式精算。替代讀數：FY2022→FY2025 營業利益由約 12.1 億增至約 17.1 億（營收×營益率），增加約 5.1 億；同期資本支出年約 1.6–1.7 億（FY2026 指引）加小型收購，增量報酬極高但不可精算","reinvest_rate":"低：成長投資多以營業費用列帳，而非資本化。FY2026 資本支出指引中值 1.65 億，對 FY2025 自由現金流 14.6 億約 11%，其餘現金用於股利與回購","endo_ceiling":11,"formula_note":"「增量報酬×再投資率」在此不適用：成長投資多走營業費用（CEO 2026-10-20 表示，AI 在既有業務省下的費用全數再投入新產品），資本化投入資本很小。改以「營收有機成長×利潤率持平」作內生上界，約 11%：FY2022–FY2025 營收年複合 11.7%，取略低值，反映資產費正處週期高點"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","MSCI":82.97,"SPGI":70.9,"MCO":74.98,"FDS":51.38,"unit":"%"},{"metric":"營業利益率","MSCI":55.66,"SPGI":41.56,"MCO":46.1,"FDS":29.55,"unit":"%"},{"metric":"FCF 利潤率","MSCI":44.77,"SPGI":34.57,"MCO":36.36,"FDS":29.05,"unit":"%"},{"metric":"研發密度","MSCI":5.45,"SPGI":null,"MCO":null,"FDS":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"SPGI","gm":70.9,"om":41.56,"fcf_margin":34.57,"rd_intensity":null,"strategy_note":"S&P 道瓊指數是美國基準的主要對手；SPGI 營益率 41.6%，比 MSCI 低約 14pp，但指數業務未拆分，無法逐業務線比較","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MCO","gm":74.98,"om":46.1,"fcf_margin":36.36,"rd_intensity":null,"strategy_note":"主力是信評與風險分析，與 MSCI 在私募信用、風險資料有交集；營益率 46.1%，是利潤率最接近的同業","period":"TTM ending 2026-06-30（4季加總）"},{"name":"FDS","gm":51.38,"om":29.55,"fcf_margin":29.05,"rd_intensity":null,"strategy_note":"在投組分析上與 MSCI Analytics 正面競爭（10-K 列名）；營益率 29.6%，利潤率差距說明 MSCI 分析產品依附在指數與因子模型上，而不是單賣工具","period":"TTM ending 2026-05-31（4季加總）"}]},"growth":{"driver_mix":"量為主（ETF 資產規模、避險基金與資產擁有者等新客群），價為輔（年度調價貢獻穩定），EPS 另靠回購減股約 2–3pp","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"營收有機成長約 11%，在利潤率持平下直接轉為營業利益成長（FY2022–FY2025 營收年複合 11.7%）；成長投資多費用化，公式值不適用，詳見護城河題的報酬持續期段","segments":[{"item":"Index 有機訂閱 run rate 年增（Q3）","value":"11.7%（Q2 11.1%，逐季加速）"},{"item":"資產費 run rate（Q3）","value":"近 10 億美元，創紀錄；H1 資產費營收 +26.6%，但平均基點下滑"},{"item":"Analytics 有機訂閱 run rate 年增（Q3）","value":"7.5%（Q2 6.6%）"},{"item":"私募資本方案訂閱 run rate 年增（Q3）","value":"19%"},{"item":"Real Assets 有機訂閱 run rate 年增（Q3）","value":"2%"},{"item":"Climate run rate 年增（Q3，不含 First Street）","value":"8%；永續取消偏高，Q4 淨新銷售預期持平到小幅正"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差＞5pp）","lit":true,"evidence":"共識 FY2027 EPS +14.5%，營收 +8.9%，差 5.6pp"},{"signal":"產業估值倍數近 3 年系統性下移","lit":true,"evidence":"trailing 本益比、P/S、EV/S 皆落在近四個年度端點最低；同業倍數事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"永續評等需求受壓、AI 替代風險存在，但只限單一分部，且 Climate run rate 仍 +8%，未亮"},{"signal":"毛利率連 2 季年減","lit":false,"evidence":"TTM 毛利率 83.0%，高於 FY2025 的 82.4%"},{"signal":"FCF／淨利＜0.75 連 2 年","lit":false,"evidence":"FY2025 約 1.21 倍"},{"signal":"SBC／營收＞5% 且逐年上升","lit":false,"evidence":"Q2 推算約 2.9%"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自有機訂閱與資產費，2026 年三筆收購屬小型補強，不承重；回購影響已寫在現金去向與 EPS 缺口歸因"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2026 年三筆收購（Compass Financial、ApeVue、First Street 現金 1.2 億美元）皆遠小於市值 5%，已實現增量報酬事實表未涵蓋，不計分","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q3 回購均價 562 美元，對 FY2026 共識 EPS 19.52 美元，盈餘殖利率約 3.5%；10 年期公債殖利率事實表未涵蓋，但 10 年期要低於 1.5% 才會過門檻，判不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"上半年 SBC 7,310 萬美元，年化約 1.5 億，對市值約 439 億，毛稀釋約 0.3%／年；回購使股數淨減","grade":"過"}]},"valuation":{"basis":"前瞻本益比與 PEG（品質複利型）","tier":"高品質金融資料與指數商","peers":{"expanded":false,"reason":"事實表的同業資料只有利潤率，沒有同業前瞻本益比，無法用倍數跨公司定錨"},"fwd_pe":30.97,"peg":2.22,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 31 倍、PEG 約 2.2，偏貴；但 trailing 本益比為近四個年度端點最低，五年基準年化約 9%，落在中段，兩者相抵判黃。五年分位：事實表只有四個年度端點，不外推","upside_short_pct":2.4,"upside_mid_pct":46.2},"trap_analysis":{"verdict":"🟡","label":"倍數下移與 EPS 跑贏營收兩項亮燈"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"資產費隨股市市值與 ETF 資金流起落：H1 掛鉤股票 ETF 資產 +34.6%，但平均基點下滑；主動 ETF 三年資產年複合 59%；新興市場指數台灣權重 24.8%，地緣與關稅可能抑制資金配置與客戶預算","assumption":"股市長期上行、被動化持續，基點下滑被資產成長抵消","consequence":"股市空頭一年、資產規模縮水 25–30%，再加 BlackRock 壓費：資產費營收下滑，EPS 回到 19–20 美元，倍數同時壓到 20 倍，股價約 400–440 美元","ruling":"部分採納：資產費的市場風險已放進 Bear 情境（30% 機率、終端 20 倍）。結構性部分反駁：主動 ETF 轉型反而在採用 MSCI 的主動 ETF 專用授權與投組工具（2026-07-21 CFO、2026-10-20 Munari），Index 訂閱仍在加速","watch":"資產費 run rate 年增是否轉負；掛鉤 ETF 平均基點費率年降幅","evidence_refs":["end_markets#4","geo_supply_chain#0","reg_tariff_export#0","customer_concentration_credit#1"],"fact_refs":["f_kpi6_index_analytics_organic_"]},{"view":"論點失敗","evidence":"AI 讓對手低價推出替代品、客戶自建分析；ESG 評等可被 AI 複製；EU ESG 評等規範自 2026-07-02 起要求 ESMA 授權，增加合規成本；Q3 永續出現一筆大額縮單","assumption":"MSCI 的資料、模型與基準地位無法被 AI 低成本複製","consequence":"總留存率跌破 93%，調價能力失效，倍數下修","ruling":"多數反駁：Q3 留存約 95%、年增 30bp，Index 逾 97%；客戶透過 MSCI 自家應用使用內容的比例高於第三方連接器（2026-10-20 Munari）。風險集中在永續分部，已放進 Bear","watch":"總留存率；永續與氣候分部淨新銷售","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","regulatory_antitrust#1"],"fact_refs":["f_kpi5_retention_rate"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 2026-10-20 明言不擴張利潤率，增量經營槓桿全數再投資；2026 費用指引在 Q2 上修，Q3 再說會落在上緣；利息費用指引上調，因為循環信貸增加以支應回購；回購均價 562 美元，約 FY1 的 29 倍；Q3 超預期，自由現金流指引卻未上調","assumption":"再投資報酬如 CEO 所說很高，回購價格合理","consequence":"營收照長，但 EPS 成長降到 8–10%；以高倍數加槓桿回購會消耗股東資本","ruling":"採納為監測：Base 第一年 EPS 已低於共識，並設全年調整後 EPS 年增＜8% 為停止加碼條件","watch":"調整後 EPS 年增；淨負債對 EBITDA 倍數；FY2027 費用指引","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_kpi7_fy2026_guidance_q2","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY1 本益比 31 倍、PEG 約 2.2；股價自前份 542.72 漲到 604.46 美元（+11%），RSI 69.5，價格在 52／104／250 週均線之上；Q2 後賣方下修目標價（JPM 742→700、Evercore 746→722）；共識 FY1 EPS 近期下修 0.76%","assumption":"市場會持續給品質溢價","consequence":"若 EPS 只符合共識、倍數回到 26 倍，五年年化約 9%，一年報酬接近零","ruling":"採納：不追價，等 536 美元以下（FY2027 共識 24 倍）","watch":"FY2 本益比；共識修正方向","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_rsi14","f_consensus_rev_fy1_pct","f_price_at_dd"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 542.72 → 本次 604.46（+11.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=542.72","side_b":"本次 price_at_dd=604.46","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 542.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 542.72 美元：Bull 價 1,185、Bear 價 401.4，五年期望值 +45.1%，基準年化 8.7%，不對稱比 3.8","side_b":"本次情境、股價仍用 542.72 美元：Bull 價 1,264、Bear 價 440，五年期望值 +55.8%，基準年化 10.2%，不對稱比 5.85","ruling":"先換情境、股價不動：五年期望值多 10.7 個百分點，基準年化多 1.5 個百分點。不對稱比由 3.8 變為 5.85。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 542.72 美元：五年期望值 +55.8%，基準年化 10.2%，不對稱比 5.85","side_b":"本次情境、股價 604.46 美元：五年期望值 +39.9%，基準年化 7.9%，不對稱比 3.34","ruling":"再換股價、情境不動：起點價上漲 11.4%，五年期望值少 15.9 個百分點，基準年化少 2.4 個百分點，不對稱比由 5.85 降到 3.34。合計五年期望值比前份少 5.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份基本面結論欄","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、估值黃燈、陷阱黃燈、護城河方向穩定、Y5 後跑道寬、品質複利成長、非循環股","side_b":"本次全數維持","ruling":"Q3 新證據（Index 訂閱加速至 11.7%、三條產品線淨新銷售創紀錄、留存年增 30bp）強化護城河與跑道判斷，但同時出現永續大額縮單、費用上修，正反相抵，結論不變","evidence_level":"公司新聞稿與法說原話","settle_metric":"Q4 Index 有機訂閱 run rate 年增","if_then":["若 Q4 Index 有機訂閱 run rate 年增 ≥11% 且總留存率 ≥95%，護城河方向轉 ↑ 的執行面條件成立，再看資產費基點是否止跌","若 Index 有機訂閱 run rate 年增跌破 10%，跑道改評中等、停止加碼"],"evidence_refs":[]},{"axis":"前份裁決、角色、情境機率與回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：股價 542.72 美元時進場；Bull／Bear 機率 25%／30%；最大回撤 −45%","side_b":"本次：股價 604.46 美元（+11%），基本面未變而價格先走，改為不追、等 536 美元以下；Bull／Bear 機率維持 25%／30%；最大回撤改為 −30%～−45% 的範圍","ruling":"漲幅來自價格而非證據（共識 EPS 反而小幅下修），依「價格先走、證據未到就不追」處理","evidence_level":"價格與共識快照","settle_metric":"FY2 本益比","if_then":["若股價回到 536 美元以下且 Index 有機訂閱 run rate 年增 ≥10%，分批加碼首筆三分之一","若股價續漲到 700 美元以上而共識 EPS 未上修，不追，持有者不加碼"],"evidence_refs":[]},{"axis":"估值重啟加碼門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價回到 474 美元以下（FY1 本益比 24 倍），且 Index 有機訂閱 run rate 年增仍在 10% 以上","side_b":"股價回到 536 美元以下（FY2027 共識 EPS 24 倍），且 Index 有機訂閱 run rate 年增仍 ≥10%","ruling":"加碼門檻的分母由 FY2026 滾動到 FY2027：FY2026 已過三季，前瞻一年改用 FY2027 共識 22.35 美元；倍數 24 倍不變，價位由 474 升至 536 美元","evidence_level":"共識快照","settle_metric":"股價對 FY2027 共識 EPS 倍數","if_then":["若股價 ≤536 美元且 Index 有機訂閱 run rate 年增 ≥10%，分批加碼"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼指標","side_b":"本次設四條：Index 有機訂閱 run rate 年增＜8% 連 2 季則減碼；總留存率＜93% 連 2 季則減碼；BlackRock 旗艦產品改用他家指數則清倉重評；全年調整後 EPS 年增＜8% 則停止加碼","ruling":"前份缺門檻屬方法缺漏，本次補上；門檻取 Q2–Q3 實際值往下留緩衝","evidence_level":"公司新聞稿","settle_metric":"各季新聞稿營運指標","if_then":["若任一減碼條件成立，減碼一半","若 BlackRock 轉換指數成立，清倉並重跑研究"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing","side_b":"BlackRock 把掛鉤 MSCI 指數的主要 ETF 改用他家或自家指數，或要求大幅降低資產費","ruling":"這是數學上最大的單一離散敏感項：BlackRock 占營收 10.8%，其中 96.5% 是高利潤的資產費；合約延至 2035 年，機率低，但發生即清倉重評","evidence_level":"10-K 與 8-K","settle_metric":"SEC 申報中的 BlackRock 合約與營收占比","if_then":["若 BlackRock 宣布主要產品轉換指數，清倉並重跑研究"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"不擴張利潤率對上共識 EPS 跑贏營收","cause":"新證據","prior_field":null,"side_a":"CEO 2026-10-20：不擴張利潤率，經營槓桿全數再投資；2026 費用落在指引上緣","side_b":"共識 FY2027 EPS +14.5%、營收 +8.9%，隱含利潤率擴張或大幅減股","ruling":"可調和（程度差異）：FY2026 一次性遣散、績效股票應計與收購費用在基期回落，加上回購減股，可解釋約 3–4pp；其餘要靠利潤率上升，與 CEO 說法衝突，所以 Base 第一年 EPS 取 22.1 美元，略低於共識","evidence_level":"法說原話與共識","settle_metric":"FY2027 費用指引（2027-01 Q4 法說）","if_then":["若 FY2027 調整後 EBITDA 費用指引年增 ≥ 營收共識增速，下修 Base EPS 並停止加碼","若費用指引年增 ≤6%，共識 EPS 可信，維持 Base"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"管理層前後說法：永續與 Analytics","cause":"新證據","prior_field":null,"side_a":"2026-07-21 CFO：永續與氣候未來兩季淨新銷售約零到小幅負；CEO：Analytics 偏弱「都是不規則」","side_b":"2026-10-20：Q3 永續取消偏高，有一筆大額縮單，Q4 改說持平到小幅正；Analytics 淨新銷售年增 63%，創紀錄","ruling":"Analytics 的不規則歸因已獲驗證；永續的說法有兌現，但仍在下行，加上 EU ESG 評等新規增加合規成本，暫時採信、不加分","evidence_level":"兩季法說原話","settle_metric":"Q4 永續與氣候淨新銷售","if_then":["若 Q4 永續與氣候淨新銷售轉負，管理層的永續說法證偽，Bear 機率上調至 35%","若 Q4 轉正且 Climate run rate 含 First Street 後 ≥12%，永續拖累見底"],"evidence_refs":["regulatory_antitrust#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"不追：FY1 本益比 31 倍、PEG 2.2、RSI 69.5，價格比前份高 11%","side_b":"現在買：trailing 本益比為近四個年度端點最低；Q3 是基本面最強的一季（淨新銷售創紀錄、留存回升）；CEO 個人 2024 年以來買進 3,010 萬美元，公司以 562 美元回購 6.27 億；等價可能等不到","ruling":"不可調和（方向相反），選等價。依據：基準年化約 9%，落在中段；價格漲幅大於證據增強幅度。硬數據點是 FY2 本益比 27 倍","evidence_level":"價格、共識與法說","settle_metric":"FY2 本益比與 Q4 Index 訂閱成長","if_then":["若股價 ≤536 美元，分批加碼首筆三分之一","若 Q4 財報 Index 有機訂閱 run rate ≥12% 且 FY2027 共識 EPS 上修 ≥3%，不等價，以現價分批加碼首筆三分之一","反向：若股價續漲但共識下修，不加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"驗證 Index 訂閱主引擎","type":"假設驗證","maps_to":"H1","metric":"Index 有機訂閱 run rate 年增","threshold":"≥10%；連 2 季＜8% 則減碼","action":"連 2 季＜8% 減碼一半","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":[]},{"n":2,"text":"BlackRock 主要 ETF 改用他家或自家指數","type":"Single Thing","maps_to":"single_thing","metric":"BlackRock 掛鉤 MSCI 指數的主要產品","threshold":"任一旗艦產品宣布轉換指數或重議資產費","action":"清倉並重跑研究","source_freq":"SEC 8-K、BlackRock 公告／事件","date":null,"evidence_refs":["customer_concentration_credit#0","competitive_share_entrants#2"]},{"n":3,"text":"AI 替代是否侵蝕客戶黏著","type":"風險","maps_to":"R2","metric":"總留存率","threshold":"＜93% 連 2 季","action":"減碼一半","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"n":4,"text":"費用上修吃掉獲利成長","type":"風險","maps_to":"R3","metric":"調整後 EBITDA 利潤率；全年調整後 EPS 年增","threshold":"利潤率＜58% 連 2 季，或全年 EPS 年增＜8%","action":"停止加碼","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":["capital_markets_pricing#1"]},{"n":5,"text":"資產費隨股市轉弱","type":"風險","maps_to":"R4","metric":"資產費 run rate 年增","threshold":"連 2 季轉負","action":"若留存與訂閱成長守住，視為市場波動，分批加碼；若訂閱同步轉弱，減碼","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["end_markets#4","geo_supply_chain#0"]},{"n":6,"text":"價格回到合理區","type":"估值rearm","maps_to":null,"metric":"股價對 FY2027 共識 EPS 倍數","threshold":"股價 ≤536 美元（24 倍）且 Index 有機訂閱 run rate 年增 ≥10%","action":"分批加碼首筆三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":7,"text":"倍數過熱","type":"減碼","maps_to":null,"metric":"股價對 FY2027 共識 EPS 倍數","threshold":"＞36 倍（約 805 美元）","action":"減碼三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":8,"text":"Q4 財報與 FY2027 指引後複審","type":"複審日期","maps_to":null,"metric":"FY2027 費用指引、Q4 淨新銷售","threshold":"財報公布","action":"重跑研究","source_freq":"一次","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"Index 有機訂閱 run rate 年增","bear_threshold":"＜8% 連 2 季","window":"2 季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"總留存率","bear_threshold":"＜93% 連 2 季","window":"2 季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"BlackRock 主要 ETF 是否改用他家指數","bear_threshold":"任一旗艦產品宣布轉換","window":"12 個月","source":"SEC 8-K、BlackRock 公告","last_status":"ok"},{"metric":"全年調整後 EPS 年增","bear_threshold":"＜8%","window":"1 個會計年度","source":"MSCI Q4 新聞稿與年報","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場以 AI 替代與永續下滑為由壓低倍數（trailing 本益比為近四個年度端點最低），但 Q3 Index 訂閱加速到 11.7%、留存率升到約 95%，替代效應還沒出現在留存數字上"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=0.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價回到 536 美元以下（FY2027 共識 EPS 24 倍），且 Index 有機訂閱 run rate 年增仍 ≥10%'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但判斷者宣告 wait_for_price：不得把觀望承繼回進場（只往保守方向）","hit":false,"basis":"wait_for_price=True, prior_verdict='進場', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價回到 536 美元以下（FY2027 共識 EPS 24 倍），且 Index 有機訂閱 run rate 年增仍 ≥10%","exec_line":"已持有者續抱、不加碼；新資金等 536 美元以下分三筆買，每筆間隔至少一季財報；若 Q4 Index 訂閱 ≥12% 且 FY2027 共識上修 ≥3%，可不等價先買首筆"},"reasoning":{"industry":"Q2 FY2026 營收 8.67 億美元，調整後 EBITDA 利潤率 62.1%，GAAP 營益率 56.2%，季自由現金流 3.26 億。年度財報：FY2025 營收 31.3 億，FY2022–FY2025 年複合約 11.7%，營益率維持在 53.5%～54.8%。Q3 法說（2026-10-20 CEO）：總營收 +12.4%，資產費營收 +25%，訂閱營收 +8%，調整後 EPS +14%。分部為 Index、Analytics、Sustainability and Climate、All Other–Private Assets，各分部營收占比事實表未涵蓋。單點依賴：BlackRock 占 FY2025 合併營收 10.8%、Index 分部 18.7%（FY2022 為 17.4%），其中 96.5% 是資產費。這既是集中度風險，也是護城河證據：2026-01 修約，期限延至 2035-03-31。產業時鐘判 II（擴張）：被動化與 ETF 資金流仍在擴張，Q3 股票 ETF 淨流入 760 億美元，對標資產近 23 兆。供需耐久性：訂閱端屬結構性持久，留存率 95.3%，年增 0.9pp；資產費端隨股市週期起落，股市反轉時會先掉。","moat":"機制是基準標準加轉換成本：基金合約、績效考核與交易生態都綁在 MSCI 指數上，掛鉤的產品越多越難換。對同業的利潤率差：營益率 55.7%，對 MCO 46.1%、SPGI 41.6%、FDS 29.6%，最強同業差 9.6pp；FCF 利潤率 44.8%，對 36.4%／34.6%／29.1%。同業 ROIC 與歷史趨勢事實表未涵蓋，只能用單期利潤率差替代，無法判斷差距在擴大還是收窄。評分：執行力 9（留存升、淨新銷售創紀錄、員工數持平下完成四筆收購）；定價權 8（年度調價貢獻穩定，但最大客戶拿到較低底價、資產費基點下滑）。屬訂閱型資料業，以綜合分加敘述評 A，依據是轉換成本落在決策最小單位（基金合約層）。三項威脅都屬點對點，不扣分。","growth":"成長來源以量為主（ETF 資產規模、新客群），價為輔：調價對新銷售的貢獻近幾季穩定（2026-07-21 CFO）。EPS 另有回購減股加成。共識 EPS FY2026→FY2028 由 19.52 升至 25.35 美元，年增約 14.0%（事實表無分析師家數）；共識營收 FY2027 +8.9%。內生上界約 11%，缺口約 3pp，歸因兩項：一是淨回購，Q3 回購 6.27 億美元，2024 年以來累計 44 億、近 800 萬股；二是 FY2026 一次性費用的基期效應，包括遣散費多 1,000–1,500 萬、績效股票應計多 1,500–2,000 萬、收購費用約 2,000 萬（2026-10-20 CFO）。缺口不是靠倍數重評。滲透率事實表未涵蓋；跑道判斷依據是：對標資產 23 兆中只有約 8 兆是被動管理，做市商尚未滲透、還沒進數字（2026-10-20 CEO），私募與財富管理正在放量。","governance":"現金去向：FY2026 自由現金流指引 14.85–15.45 億、資本支出 1.6–1.7 億，股息殖利率約 1.3%，回購是最大去向（2026-07-01 至 10-19 回購 6.27 億）。淨負債 61.9 億，以 Q2 調整後 EBITDA 5.385 億年化約 21.5 億計算，約 2.9 倍；Q3 法說上調利息費用指引，原因是循環信貸餘額增加以支應回購，Q3 現金利息多付 5,000 萬美元以上。CEO 個人 2024 年以來買進 5.7 萬股、3,010 萬美元，利益與股東一致。收購都是小型補強。","valuation":"FY1 本益比 30.97 倍；FY2 約 27.0 倍（604.46÷22.35）。PEG＝30.97÷14.0≈2.2，屬偏貴。trailing 本益比 33.0 倍、P/S 13.2 倍、EV/S 15.0 倍，都是近四個年度端點中最低，顯示市場已在折價 AI 替代與永續風險；但只有四個點，不是五年分位。基準情境：五年 EPS 34 美元×26 倍＝884 美元，較現價 +46%，年化約 8%，加股息約 9%。Bull 1,264 美元，Bear 440 美元。賣方平均目標約 692 美元（2026-09 彙整），高於現價，方向上支持持有，不支持追價；Q2 後 JPM、Evercore 已下修目標價。同業前瞻倍數事實表未涵蓋，終端倍數無法用同業現值校準，只能以自身倍數區間定錨。","premortem":"最可能看錯的三處都寫在反證紀錄：資產費的市場風險、再投資吃掉經營槓桿、價格已先走。動能面：RSI 69.5，接近但未過 70；26 週報酬只有 +0.13%，四週漂移事實表未涵蓋，不判過熱。共識 FY1 EPS 近期小幅下修 0.76%，與 Q3 數字超預期方向相反，原因是費用上修。"},"plain":{"six":{"how_it_makes_money":"向資產管理商、ETF 發行商、避險基金與資產擁有者收錢：訂閱占大宗，另按掛鉤 MSCI 指數的資產規模抽基點費（Q3 資產費 run rate 近 10 億美元，創紀錄）。錢卡在「投資標竿」這一節點：基金合約與公開說明書寫死比較基準，換掉要改文件、重新對投資人揭露。","moat":"→：執行力在擴大（留存率回升，Q3 Index、Analytics、私募資本方案淨新銷售創紀錄），定價權穩中略鬆（資產費基點下滑、BlackRock 底價調降），兩者相抵，判為穩定。","growth":"🟢：Index 訂閱加速（Q3 有機 11.7%），私募資本方案 +19%，客製指數 +26%；避險基金、資產擁有者、財富管理與做市商等新客群構成第二、三條曲線，Y5 之後跑道寬。","capital":"現金轉換極佳，但回購價格偏高、且靠舉債支撐：FY2025 自由現金流對淨利約 1.21 倍，SBC 約占營收 2.9%；Q3 回購均價 562 美元，換算盈餘殖利率只有約 3.5%，資金部分來自循環信貸。","valuation":"現價 604 美元要求未來五年調整後 EPS 年增約 11–12%，終端還要守住 26 倍以上，才換得年化約 9%。EPS 部分我相信，倍數擴張我不信，結論是合理偏貴，不追價。","how_wrong":"🟡：兩項衰退信號亮燈（共識 EPS 跑贏營收逾 5pp、自身倍數下移）；不構成陷阱，但看錯的路徑很清楚：股市空頭打資產費，同時倍數壓縮。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場以 AI 替代與永續下滑為由壓低倍數（trailing 本益比為近四個年度端點最低），但 Q3 Index 訂閱加速到 11.7%、留存率升到約 95%，替代效應還沒出現在留存數字上","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"進場","prior_role":"衛星","wait_for_price":true,"wait_for_price_condition":"等股價回到 536 美元以下（FY2027 共識 EPS 24 倍），且 Index 有機訂閱 run rate 年增仍 ≥10%","trap":"🟡","val":"🟡","moat":"A","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":604.46,"week26_return_pct":0.13,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"共識 EPS 為調整後口徑，與 FY2025 GAAP 稀釋 EPS 15.69 美元口徑不同；本益比分母一律用共識前瞻值，不影響結論"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 費用、資本支出指引","impact":"高","watch":"FY2027 調整後 EBITDA 費用年增對營收共識 +8.9%；Q4 淨新銷售與永續分部"},{"date":"2027-02","date_precision":"month","type":"other","event":"FY2026 年報揭露 BlackRock 營收占比與資產費結構","impact":"中","watch":"BlackRock 占合併與 Index 分部營收比是否續升"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,837B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河</h2>
<p class="lead">護城河評 A，方向持平，轉換成本落在基金合約層。</p>
<ul class="pts">
<li>機制是基準標準加轉換成本。基金合約、公開說明書與績效考核都綁在 MSCI 指數上，掛鉤的產品越多越難換。換基準要改公開說明書，並經董事會與投資人揭露，決策層級高。Index 留存逾 97%，資產管理客戶留存 98%（2026-10-20 CFO）。這是 A 級評等的核心依據。</li>
<li>利潤率差距證明定價權。MSCI 營業利益率 55.7%，同業 MCO 為 46.1%、SPGI 為 41.6%、FDS 為 29.6%，對最強同業仍差 9.6pp。FCF 利潤率 44.8%，對 36.4%、34.6%、29.1%。同業 ROIC 與歷史趨勢事實表未涵蓋，只能用單期差距替代，無法判斷差距是擴大還是收窄。</li>
<li>執行力評 9，定價權評 8。執行力的證據是留存回升、Q3 Index、Analytics 與私募資本方案淨新銷售創紀錄，員工數持平下完成四筆收購。定價權略鬆，因為年度調價貢獻雖穩定，但掛鉤 ETF 平均基點下滑，BlackRock 修約後部分產品底價降低。兩者相抵，方向判為持平。</li>
<li>第一項威脅是 AI 低價替代與客戶自建，機率 30%。ESG 評等最容易被 AI 複製，Q3 永續出現一筆大額縮單。但客戶偏好透過 MSCI 自家應用使用內容（2026-10-20 Munari），留存率仍在上升。這屬點對點威脅，不扣分。</li>
<li>第二項威脅是 BlackRock，機率 15%。BlackRock 占 FY2023 合併營收 9.8%，升至 FY2025 的 10.8%，占 Index 分部 18.7%（FY2022 為 17.4%），其中 96.5% 是資產費。它同時是客戶、股東與競爭者，有自建能力。ETF 授權合約 2026-01 已延至 2035 年 3 月 31 日，短期機率低。</li>
<li>第三項威脅是主動 ETF 分流，機率 25%。主動型 ETF 數量已超過被動型，資金若由被動轉主動，資產費成長會變慢。反過來看，主動 ETF 也在採用 MSCI 的主動 ETF 授權與投組工具（2026-07-21 CFO）。這項威脅有對沖，不是單向風險。</li>
</ul>
<h3>二維評分與 Moat-to-Numbers</h3>
<!-- E5 -->
<h3>§5.F 對手財務深度對照</h3>
<!-- E6 -->
<p>SPGI 的道瓊指數是美國基準的主要對手，營業利益率比 MSCI 低約 14pp，但指數業務未拆分。MCO 與 MSCI 在私募信用、風險資料有交集，利潤率最接近。FDS 在投組分析上與 MSCI Analytics 正面競爭，利潤率差距說明 MSCI 的分析產品依附在指數與因子模型上。</p>
<h3>§5.R 報酬持續期檢核</h3>
<!-- E7 -->
<p>四個檢核點中，需求基礎與決策層級都是綠燈，價值鏈分配與社會容忍度為黃燈。內生成長上界約 11%，成長投資多走營業費用，公式上的增量報酬乘再投資率不適用。</p>
</section>

```