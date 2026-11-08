你是 stock-analyst v20 的**散文層（prose）agent**，標的 ETN（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ETN_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：ETN　日期：2026-11-08　archetype：None　前份裁決：2026-09-05　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1476B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（431B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（991B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1367B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1024B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（586B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1018B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2288B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3433B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2614B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（285B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1476           3867-5524      5 條（2–6 內）  
s3                  8000         431           5298-7569      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3382          8133-11618      5 條（2–6 內）  
s6                 11000         586          7290-10414      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1018           1737-2482      5 條（2–6 內）  
s10                 5000        2288           1898-2712      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2614           2000-2386      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         285            850-1215      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4660B；至少需散文≈40.34KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45
−45%
−39%
−30
−30%
−26%
−16.8%
−14.68%
−14.68
−1.7%
−1
0
0.25
0.75
0.8%
0.87
0.93
0.97
0.97%
1
1.0
1%
1.1
1.18%
1.2
1.3
1.35
1.54
1.61
1.9
02
2
2.3
2.46
2.9%
2.97
03
3
3.31
3.6
3.75
3.91
4.0
4
4.01
5
5%
05
5.21
6%
06
6
7.0%
7
07
7.2%
7.5
8.0
8
08
8.1
8.75
8.9
8.9%
09
9%
9
9.6
9.8%
10%
10
10.34
10.39
10.49
11
11%
11.0%
11.1%
11.4
11.8%
11.87%
12%
12
12.06
12.4
12.8%
13
13.55
13.67
13.70
13.75
14
14%
14.8
15
15%
15.2
15.4
15.5
$15.5
16.0
16
16.07
16.2%
16.2
16.28
16.4
16.8%
17%
17
17.2%
17.32%
17.5
$17.7
18
18.2
18.5
18.75
18.94
19
19%
19.1%
19.3%
19.4%
20
20%
20.5
20.9
20.99
21.0
21%
21.1%
22%
22
22.6
22.63
23
23%
23.74%
23.9
24%
24
24.1%
24.5%
24.5
24.9%
25.0
25
25%
25.3%
25.6%
26
27%
27
27.1
28%
28.8
29%
29.8%
30
30%
31%
31
31.8%
32%
32.3%
33%
33
34.1%
34.14
35%
35
35.05%
35.53
36.99
37.59%
38
39%
40.87
41%
41.72
42
43.0%
43%
44%
45
46%
49
50%
50
50.1%
51%
52
54%
55%
55
56
58%
61.2%
65%
68.7
70
85%
89.47
95.5
100
100%
101%
104
140
150%
170
200
201
201.04
207
230
240%
250
252
259
259.2
277.2
289
300
$300
307
321
340
341.72
355
$355
360
366
384
410
410.85
425.5
431.88
440
485.47
492
526
575
703
800
858
875
887.6
2022
2023
2025
2026
2027
2028
2029
2030
2036
2301
2308
20261108
1,328
3,500
33,685
37,420
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
{"meta":{"ticker":"ETN","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Eaton Corporation plc"},"oneliner":"第三季再上修，電氣訂單年增 43%，股價卻從 9 月的 410.85 美元跌到 341.72 美元；現價只要 EPS 年增約 12% 就有約 10% 年報酬，但現金轉換與 2028 年後資料中心需求仍未驗證。","thesis":{"H":[{"id":"H1","text":"在手訂單與新產能轉換支撐 FY27 調整後 EPS 約 16 美元、FY28 約 18.5 美元。","2y":"FY27 ≥15.5 美元，FY28 ≥17.5 美元","5y":null,"10y":null,"threshold":"FY27 首次指引中點 ≥15.5 美元；電氣滾動 12 個月 book-to-bill ≥1.1","source":"Eaton 季度新聞稿與法說，季更；2027 年 2 月首次給 FY27 指引","drift_rule":"TTM 調整後 EPS 連 2 季低於路徑 5% 為削弱，連 3 季低於路徑 10% 為反轉"},{"id":"H2","text":"電氣美洲利潤率兌現 2030 年 32% 承諾，新廠投產不再拖累；2026-07-31 法說摘錄未明講分部，按上下文解讀為電氣美洲。","2y":null,"5y":"2030 年 ≥32%","10y":null,"threshold":"FY27 全年 ≥30%，2030 年 ≥32%","source":"Eaton 季度新聞稿分部利潤率，季更","drift_rule":"TTM 利潤率連 4 季低於路徑 5% 為削弱，連 6 季低於路徑 10% 為反轉"},{"id":"H3","text":"800V 直流遷移後，Eaton 每 MW 內容價值不低於現行約 340 萬美元，固態變壓器由試點轉量產。","2y":null,"5y":null,"10y":"2036 年前直流架構下內容價值與份額不低於交流時代","threshold":"2027 年底前揭露量產訂單；每 MW 內容價值 ≥340 萬美元","source":"法說與投資人日，半年更；第三方份額事實表未涵蓋","drift_rule":"跨 2 個年度未達為削弱，跨 3 個年度未達為反轉"}],"R":[{"id":"R1","text":"資料中心開工延遲或資本支出消化，訂單成長快速降溫。","h_ref":"H1","clock":"🔥","threshold":"資料中心滾動訂單連 2 季 <30%","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"開關設備與斷路器供給轉鬆，多座新廠同時開出，新進入者壓低定價。","h_ref":"H2","clock":"🔥","threshold":"電氣美洲在手訂單連 2 季 <10% 且利潤率年減 ≥100bp","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#1"]},{"id":"R3","text":"關稅與原物料成本再度超過價格傳導。","h_ref":"H2","clock":"⚡","threshold":"價格成本連 2 季轉負且電氣美洲利潤率環比下滑","evidence_refs":["reg_tariff_export#0"]},{"id":"R4","text":"800V 直流架構加速，對手在固態變壓器取得大案，現有交流設備內容價值縮水。","h_ref":"H3","clock":"🐢","threshold":"2027 年底前未揭露量產訂單且對手取得具名大案","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R5","text":"10-Q 列示的反壟斷與貿易管制事項惡化；受影響營收與和解時程事實表未涵蓋。","h_ref":"H1","clock":"🐢","threshold":"揭露應計或金額 ≥1.9 億美元，或進入刑事程序","evidence_refs":["regulatory_antitrust#1"]},{"id":"R6","text":"Boyd 約 95.5 億美元併購占市值逾 5%，整合或增長不如預期，高槓桿下壓縮資本彈性；Mobility 出表也增加 FY27 比較難度。","h_ref":"H1","clock":"🔥","threshold":"Boyd FY27 營收 <27 億美元","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"超大型雲端資本支出進入消化期，使電氣滾動 12 個月 book-to-bill 連 2 季跌破 1.0。","why_fatal":"這是情境樹最大的敏感度：Base 與 Bear 的 FY31 EPS 差 35%（25.0 對 16.2 美元），倍數再差 30%（23 對 16 倍），終端股價差 55%（575 對 259 美元）。","if_happens":"清倉，等訂單連 2 季回升後重新研究。","how_monitor":"每季新聞稿的滾動 12 個月訂單與 book-to-bill，法說的資料中心訂單與談判管線。","probability":"未來 12 至 24 個月約 20%；FY27 訂單有在手訂單與 11% 終端市場框架支撐，但 2027 年規劃容量超過六成尚未開工。"}},"appendix_a":{"growth_durability":7,"quality_score":7.5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.99,"peg_fy2":1.3,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":12.06,"FY2026E":13.67,"FY2027E":16.28,"FY2028E":18.94},"fy_end_month":12,"eps_basis":"調整後 EPS（Non-GAAP），Koyfin 2026-11-07 快照，分析師家數事實表未涵蓋；FY2025A 由 FY26 指引中點 13.75 美元與管理層所稱年增 14% 反推，FY1 共識 13.67 美元略低於指引下緣 13.70 美元。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ETN_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"多年訂單與利潤率上行，但約三分之一營收所在的強勢市場帶有資本支出週期性，且 2026 年成長含 8 個百分點併購。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性需求、週期性交付：訂單加速且大型變壓器交期仍長於 12 至 24 個月，屬擴張期；但新產能 2027 起陸續開出，2027 年規劃容量超過六成尚未開工，供給可逆性中等。來源為 2026-11-03 法說、Rystad 與 JPMorgan 轉述，依據不含股價。","bargaining":{"up":"銅等原物料與關稅成本靠價格傳導，Q3 價格成本金額轉正。","down":"超大型雲端與託管客戶逐案議價，CFO 稱 10 月與 2 家大客戶談定，第四季還有數家要談。","geo":"利潤主要在美洲；歐亞靠跟隨全球客戶與 COL、NordicEPOD 補產品。"},"profit_pool_dir":"利潤池往能提供完整電力鏈的供應商集中，但 5 年營業利益池占比事實表未涵蓋，方向僅為定性判斷。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與滲透率；可引用的只有美國資料中心已公告案量 366GW 對已裝機 50GW，屬管理層追蹤數，不是可服務市場。"}},"moat":{"mechanism":"自製關鍵電力設備加系統整合，形成單一供應商、認證與交期的轉換成本；液冷與直流產品把範圍延伸到晶片端。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面穩定：電氣美洲利潤率逐季回升，但年比仍下滑，25 個擴產案完成 18 個後才剛轉成產出。定價面穩定：Q3 價格成本轉正，大客戶仍逐案議價。份額沒有第三方證據，所以不標擴大。","peer_na_reason":"事實表未涵蓋各家投入資本，ROIC 差距無法計算，只能比利潤率。","threats":[{"level":"🟡","text":"固態變壓器與 800V 直流架構吸引 Siemens、Reinhausen、Sungrow 進入；Eaton 有 UL 認證先行與 10 個試點，屬單點競爭，但遷移時點公司也說無法掌握。","p":35,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"新進入者與模組整合商爭奪預製電力市場，10-K 也承認漲價可能損及份額；事實表沒有具名搶單案例。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"斷路器與開關設備可能轉向供給過剩，交期優勢消失後定價力才會受到真正測試。","p":30,"evidence_refs":["supply_demand_durability#2"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，無法定象限；利益率面屬中高。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"電力設備是剛需，管理層預期 2027 年沒有終端市場衰退；但資料中心的急迫性不等於持久性，2027 年規劃容量超過六成尚未開工。"},{"item":"決策層級","level":"🟡","text":"決策單位是整條電力鏈，單一保固與認證有黏性；但大客戶可在多家合格供應商間選擇，目前靠交期與供應確定性撐住，漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"Eaton 每 MW 約 340 萬美元內容價值有議價基礎，且無單一客戶超過 10%；但架構由晶片與雲端業者決定，大客戶逐案議價，Vertiv 的現金轉換也較好。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業與公用事業，尚無社會價格上限的跡象；10-Q 列有反壟斷與貿易管制事項，金額事實表未涵蓋，已列入風險監測。"}],"roiic":"資料缺口：事實表沒有投入資本。僅能做假設性推算，若 Boyd 利潤率接近公司 Q3 分部利潤率 25.3%，FY27 營收 27 億美元對 95.5 億美元收購價的稅前報酬約 7.2%，Boyd 實際利潤率未揭露。","reinvest_rate":"資料缺口：折舊、營運資金與稅率事實表未涵蓋。FY26 僅 Boyd 一筆約 95.5 億美元，約為 FY2025 淨利 40.87 億美元的 2.3 倍，屬一次性高峰。","endo_ceiling":null,"formula_note":"內生成長率應為增量 ROIC 乘再投資率；兩項輸入都缺，所以不給數字。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","ETN":35.05,"2308.TW":35.27,"VRT":38.12,"SU.PA":null,"2301.TW":23.4,"unit":"%"},{"metric":"營業利益率","ETN":17.32,"2308.TW":16.98,"VRT":20.35,"SU.PA":null,"2301.TW":11.41,"unit":"%"},{"metric":"FCF 利潤率","ETN":11.87,"2308.TW":9.46,"VRT":23.74,"SU.PA":null,"2301.TW":-6.21,"unit":"%"},{"metric":"研發密度","ETN":2.75,"2308.TW":8.39,"VRT":null,"SU.PA":null,"2301.TW":5.3,"unit":"%"}],"competitors":[{"name":"2308.TW","gm":35.27,"om":16.98,"fcf_margin":9.46,"rd_intensity":8.39,"strategy_note":"毛利率與營業利益率幾乎相同，研發密度明顯較高，是電源端與直流架構的主要對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"VRT","gm":38.12,"om":20.35,"fcf_margin":23.74,"rd_intensity":null,"strategy_note":"毛利率、營業利益率與 FCF 利潤率都高於 Eaton，是純資料中心標的中現金轉換最強的對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"SU.PA","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表無財務資料，無法比較；仍是全球配電與資料中心電力的主要競爭者。"},{"name":"2301.TW","gm":23.4,"om":11.41,"fcf_margin":-6.21,"rd_intensity":5.3,"strategy_note":"利潤率低一個層級且 FCF 為負，不宜作為 Eaton 的定價對照。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主、價次之，併購墊高 2026 年約 8 個百分點，回購貢獻小。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊、營運資金與稅率事實表都未涵蓋，內生上界無法推導；無法證明共識成長落在上界內，情境樹保守視為超過。","segments":[{"item":"電氣美洲","value":"Q3 營收 41.72 億美元、有機 +22%、利潤率 29.8%、資料中心 +54%、滾動訂單 +39%"},{"item":"電氣全球","value":"Q3 營收約 27 億美元、總成長 +58%、有機 +27%、利潤率 21.1%、滾動訂單 +51%"},{"item":"航太","value":"Q3 營收約 12 億美元、有機 +6%、利潤率 24.9%、在手訂單 56 億美元"},{"item":"Mobility","value":"Q3 營收反推約 8.75 億美元、有機 +9%、利潤率 17.2%，FY27 僅貢獻約 8 億美元"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":true,"note":"TTM 毛利率 35.05%，低於 FY2025 的 37.59%；季度年比事實表未涵蓋，以 TTM 代理。"},{"name":"EPS 成長顯著高於營收成長","lit":true,"note":"FY2022 至 FY2025 GAAP EPS 年複合 19.4%，營收 9.8%，差 9.6 個百分點。"},{"name":"FCF／淨利低於 0.75 連 2 年","lit":false,"note":"FY2024 為 0.93，FY2025 為 0.87。"},{"name":"核心市占、SBC 占比、維護性資本支出、產業倍數下移","lit":null,"note":"事實表未涵蓋。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"累計併購","value":"約 140 億美元（2026-11-03 法說）"},{"item":"Boyd Thermal","value":"約 95.5 億美元，2026-03-12 交割；FY26 營收指引 19 億美元，FY27 至少 27 億美元"},{"item":"COL Group","value":"8.1 億歐元，2026-09-25 同意收購"},{"item":"Mobility 分拆","value":"與 Dana 進行 Reverse Morris Trust，Eaton 股東持 50.1%，另收約 11 億美元現金，預計 2027 年第一季完成"},{"item":"股息","value":"TTM 殖利率約 0.97%"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Boyd 與其他併購的實際利潤與投入資本事實表未涵蓋；管理層稱各案達到或超過預期，但屬自述。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購均價與 10 年期殖利率事實表未涵蓋。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"推得稀釋股數 2022 年約 4.01 億、2025 年約 3.91 億，年減約 0.8%，沒有淨稀釋。","grade":"過"}]},"valuation":{"basis":"FY26 前瞻本益比（調整後 EPS 13.67 美元），並以 GAAP 本益比與 FCF 殖利率對照。","tier":"電力設備與資料中心基礎設施","peers":{"expanded":false,"reason":"事實表未涵蓋同業倍數，只有同業利潤率，無法做同層級對照。"},"fwd_pe":25.0,"peg":1.54,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY26 前瞻 25.0 倍、FY27 21.0 倍，PEG 1.54（25.0÷16.2）落在合理帶；但 GAAP 本益比 34.14 倍，FCF 殖利率約 2.9%（TTM FCF 約 38 億÷市值 1,328 億美元），所以結論是合理而非便宜。5 年分位事實表只有 4 個年度端點，無法計算，留空。上行空間：12 個月以 FY27 Base 16.0×24 倍＝384 美元；24 個月以 FY28 Base 18.5×23 倍＝425.5 美元。","upside_short_pct":12.4,"upside_mid_pct":24.5},"trap_analysis":{"verdict":"🟡","label":"成長靠利潤率與併購放大，尚未到陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"JPMorgan 經 Nasdaq 引述，2027 年規劃資料中心容量超過六成尚未開工；電氣美洲資料中心營收成長由 Q2 約 65% 降到 Q3 的 54%，電氣美洲在手訂單成長由 Q1 的 44% 降到 33%。","assumption":"366GW 已公告案量能如期轉成 Eaton 訂單；CEO 於 2026-07-31 表示只有約 20% 近期轉換。","consequence":"五年後虧 50% 最可能的路徑：2028 年資本支出消化，新廠同時開出，EPS 跌回 13 美元以下、本益比 13 倍，股價約 170 美元。","ruling":"部分採納：Bear 機率給 30%，與唯一致命事件同一條路徑；不採納到 Base，因為 Q3 滾動 12 個月資料中心訂單仍 +101%，非資料中心訂單也在增加。","watch":"資料中心滾動 12 個月訂單、電氣 book-to-bill、2027 年初雲端資本支出指引。","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_kpi4_backlog_book_to_bill"]},{"view":"論點成功但股東經濟變差","evidence":"FY26 GAAP 與調整後 EPS 差距 3.31 美元，FY2025 約 1.61 美元；Eaton 的 TTM FCF 利潤率 11.87%，Vertiv 為 23.74%；CFO 稱大客戶逐案議價。","assumption":"需求成真時，利潤會留在 Eaton，而不是流向大客戶或被併購溢價吃掉。","consequence":"營收達標但每股 FCF 成長落後調整後 EPS，終端倍數應往 Base 下緣走。","ruling":"採納：結論不給便宜，併購報酬項不計通過；FCF／GAAP 淨利連 2 年低於 0.75 就減碼。","watch":"FCF／GAAP 淨利、Boyd 利潤率揭露、大客戶合約的原物料調整條款。","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"],"fact_refs":["f_peer_etn_fcf_margin_pct","f_peer_vrt_fcf_margin_pct","f_kpi5"]},{"view":"價格已反映太多","evidence":"UBS 降評至中立，目標價由 440 降到 360 美元，僅比現價高約 5%，理由是估值偏高與近期盈餘上行有限，發布日未載明；GAAP 本益比 34.14 倍，FCF 殖利率約 2.9%。","assumption":"調整後 25.0 倍是合適的定價口徑。","consequence":"若市場改看 GAAP 或 FCF，合理的結論不成立，倍數可能再壓縮。","ruling":"部分反駁：股價自前份已跌約 17%，FY27 前瞻 21.0 倍，Base 假設倍數降到 23 倍，報酬不靠重估；但質疑保留，所以首批上限為目標部位 1/3。","watch":"2027 年 2 月指引是否使 FY27 共識 16.28 美元下修。","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_pe_current","f_fwd_pe_latest"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 410.85 → 本次 341.72（-16.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=410.85","side_b":"本次 price_at_dd=341.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 410.85 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 410.85 美元：Bull 價 887.6、Bear 價 277.2，五年期望值 +43.0%，基準年化 8.9%，不對稱比 2.97","side_b":"本次情境、股價仍用 410.85 美元：Bull 價 858、Bear 價 259.2，五年期望值 +34.1%，基準年化 7.0%，不對稱比 2.46","ruling":"先換情境、股價不動：五年期望值少 8.9 個百分點，基準年化少 1.9 個百分點。不對稱比由 2.97 變為 2.46。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 410.85 美元：五年期望值 +34.1%，基準年化 7.0%，不對稱比 2.46","side_b":"本次情境、股價 341.72 美元：五年期望值 +61.2%，基準年化 11.0%，不對稱比 5.21","ruling":"再換股價、情境不動：起點價下跌 16.8%，五年期望值多 27.1 個百分點，基準年化多 4.0 個百分點，不對稱比由 2.46 升到 5.21。合計五年期望值比前份多 18.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與機率（股價下跌）","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-09-05 股價 410.85 美元，估值偏貴、觀望，Bull／Bear 機率 25／30，最大回撤 −45%。","side_b":"本次股價 341.72 美元，FY26 前瞻 25.0 倍、FY27 21.0 倍，估值改判合理；機率與回撤下緣維持。","ruling":"變動主因是股價下跌約 17%，共識近 3 個月只上修 1.18%，不是基本面翻新；機率不因股價下跌而放寬。","evidence_level":"高：股價與共識皆有快照","settle_metric":"FY27 首次指引中點","if_then":["若股價續跌但 FY27 指引中點 ≥15.5 美元，分批反買","若股價先漲回 410 美元以上而指引未出，不追"],"evidence_refs":[]},{"axis":"基本面判斷維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5"],"side_a":"前份訊號等級 B、陷阱風險中等、護城河方向穩定、五年後跑道中等。","side_b":"本次四項維持。Q3 訂單與利潤率轉強，但固態變壓器對手進入，TTM 毛利率下滑。","ruling":"新證據正負相抵，不足以改判；跑道不上調，因為液冷與固態變壓器仍押同一個資料中心資本支出；護城河不上調，因為份額只有管理層自述。","evidence_level":"中：訂單與利潤率為官方數字，份額無第三方","settle_metric":"第三方份額資料與固態變壓器量產訂單","if_then":["若 2027 年底前揭露固態變壓器量產訂單且資料中心以外訂單維持 ≥20%，跑道上調並加碼第二批","若份額證據轉負，停止加碼"],"evidence_refs":["substitute_technology#1"]},{"axis":"公司分類","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份分類為品質複利成長，未標循環位置。","side_b":"本次主分類不變，循環位置仍不標，第二分類標循環商品。","ruling":"判斷方法未改主分類；資料中心的週期性放在 Bear 機率 30% 與第二分類處理。","evidence_level":"中","settle_metric":"資料中心訂單是否出現負成長","if_then":["若資料中心訂單轉為年減，改用循環股框架並減碼 1/3"],"evidence_refs":[]},{"axis":"進場條件（加碼門檻變更，前份條件已發動）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤$355（FY26E 13.55×26x 或 FY27E 16.07×22x），或 FY27 共識 EPS 上修 ≥10%（≥$17.7）且股價未同步上漲 → 重跑 DD、衛星首倉 1/3","side_b":"第二批加碼須 FY27 首次指引 EPS 中點 ≥$15.5 且電氣滾動 12 個月訂單年增 ≥25%；股價 ≤$300 且基本面未破則分批反買。","ruling":"前份股價條件已於 2026-11-06 收盤發動（341.72 美元低於 355 美元），另一個共識條件未發動；所以本次改寫下一批的條件，改由基本面資料點決定。","evidence_level":"高：收盤價可驗證","settle_metric":"2027 年 2 月 FY27 指引","if_then":["若兩項條件都達到，加碼第二批 1/3","若 FY27 指引中點低於 14.8 美元，減碼 1/3"],"evidence_refs":[]},{"axis":"Single Thing 建立","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空，沒有前份唯一致命點原文。","side_b":"超大型雲端資本支出進入消化期，使電氣滾動 12 個月 book-to-bill 連 2 季跌破 1.0。","ruling":"Single Thing 選情境樹最大敏感度，而不是最戲劇性的技術替代事件；發生即清倉。","evidence_level":"中","settle_metric":"電氣滾動 12 個月 book-to-bill","if_then":["若連 2 季低於 1.0，清倉","若維持 ≥1.1，不動作"],"evidence_refs":[]},{"axis":"監控指標建立（清倉與減碼門檻）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空，沒有前份門檻原文。","side_b":"book-to-bill 低於 1.0 連 2 季清倉；資料中心滾動訂單低於 30% 連 2 季減碼；電氣美洲 FY27 利潤率低於 29% 減碼；FCF／GAAP 淨利連 2 年低於 0.75 減碼。","ruling":"改用每季可驗證的官方數字作為清倉與減碼依據。","evidence_level":"高：皆為公司季報揭露項目","settle_metric":"每季新聞稿與法說","if_then":["任一減碼門檻觸發，減碼 1/3","單一致命門檻觸發，清倉"],"evidence_refs":[]},{"axis":"管理層承諾對帳：電氣美洲利潤率","cause":"新證據","side_a":"2026-07-31 法說 CFO：Q2 到 Q3 改善 250bp，Q3 到 Q4 再改善 200 至 250bp，年比下滑歸因於暫時性負價格成本。","side_b":"2026-11-03 法說：Q3 實際 +230bp 到 29.8%，略低於路徑；CEO 提醒不要把 Q4 乘以 4；年比下滑改稱暫時性原物料。","ruling":"屬程度差異，可調和；暫時性歸因標為未證、監測。Q2 路徑隱含 Q4 約 31.8% 至 32.3%，門檻留緩衝設在 31%。","evidence_level":"高：同一管理層前後兩場法說","settle_metric":"Q4 電氣美洲利潤率","if_then":["若 Q4 <31%，停止加碼","若到 2027 年第二季利潤率年比仍下滑，暫時性歸因證偽並減碼 1/3"],"evidence_refs":[]},{"axis":"資料中心需求持久性","cause":"新證據","side_a":"CEO 2026-11-03：已公告案量由 307GW 增至 366GW，滾動訂單 +101%，跑道延伸到 2028、2029 年以後。","side_b":"JPMorgan 轉述 2027 年規劃容量超過六成未開工；另有摘要稱資料中心訂單成長由 Q1 的 240% 降到 Q2 的 85%，口徑與 Q3 的 +101% 不一定相同，來源品質混雜。","ruling":"可調和：案量不是訂單，開工延遲影響時點，尚未看到訂單反轉；證據時間窗只到 2027 年，不能宣稱 2028 年後風險已解。","evidence_level":"中：官方訂單對照轉述資料","settle_metric":"資料中心滾動 12 個月訂單年增與電氣 book-to-bill","if_then":["若資料中心訂單連 2 季低於 30%，減碼 1/3","若股價先跌但訂單維持，分批反買"],"evidence_refs":["supply_demand_durability#3","supply_demand_durability#2"]},{"axis":"上修但現金與 GAAP 未跟上","cause":"新證據","side_a":"全年調整後 EPS 中點上修 0.25 美元到 13.75 美元，第三次上修。","side_b":"全年分部利潤率 24.1% 至 24.5% 不動，現金流預期只重申；GAAP EPS 僅 10.39 至 10.49 美元。","ruling":"可調和：上修來自銷量與 Q3 超標，併購攤提壓低 GAAP；但在 FCF 跟上前，不用調整後 EPS 主張便宜。","evidence_level":"高：官方指引","settle_metric":"FY26 全年 FCF 與 FY27 現金流指引","if_then":["若 FY27 FCF／GAAP 淨利低於 0.75，停止加碼","若連 2 年低於 0.75，減碼 1/3"],"evidence_refs":[]},{"axis":"份額：管理層自述對第三方","cause":"新證據","side_a":"CEO 稱在歐洲與亞洲持續贏得份額；2026-07-31 法說稱電氣全球資料中心營收 +65%、底層市場 +23%。","side_b":"第三方只有五家合計 41% 至 43%，沒有 Eaton 單獨份額與消長；Vertiv 利潤率與現金轉換都更高。","ruling":"管理層證據支持方向但不足以上調護城河，判斷維持穩定。","evidence_level":"低：單一來源自述","settle_metric":"第三方份額報告或大客戶揭露","if_then":["若第三方資料顯示 Eaton 份額下降，停止加碼"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":"新證據","side_a":"連續三次上修、訂單創高，EPS 只需約 12% 年複合即有約 10% 年報酬。","side_b":"好消息之下股價仍跌，代表市場在折現 2028 年後的斷層；現金流預期未上修，調整項擴大到 3.31 美元，FCF 殖利率約 2.9%，週線低於 52 週與 104 週均線，UBS 目標價僅高於現價約 5%。","ruling":"不採納不進場，但採納不一次滿倉：首批上限為目標部位 1/3，其餘等基本面資料點。若賣方論點成立，第一個可見證據會是 FY27 指引或訂單轉弱。","evidence_level":"中","settle_metric":"FY27 指引與電氣訂單","if_then":["若 FY27 指引中點低於 14.8 美元，減碼 1/3","若指引 ≥15.5 美元且訂單 ≥25%，加碼第二批 1/3","若股價反彈但兩項資料未出，不追"],"evidence_refs":["capital_markets_pricing#4"]}],"triggers":[{"n":1,"text":"FY27 首次指引達標且電氣訂單未轉弱，加碼第二批。","type":"加碼","maps_to":"H1","metric":"FY27 調整後 EPS 指引中點；電氣滾動 12 個月訂單年增","threshold":"≥15.5 美元且 ≥25%","action":"加碼第二批 1/3","source_freq":"第四季新聞稿，年度一次","date":"2027-02"},{"n":2,"text":"第四季電氣美洲利潤率驗證擴產已轉為獲利。","type":"假設驗證","maps_to":"H2","metric":"電氣美洲第四季分部利潤率","threshold":"≥31%","action":"未達則停止加碼","source_freq":"季報","date":"2027-02"},{"n":3,"text":"資料中心訂單成長明顯降溫。","type":"風險","maps_to":"R1","metric":"資料中心滾動 12 個月訂單年增","threshold":"連 2 季 <30%","action":"減碼 1/3","source_freq":"法說，季更","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"電氣訂單低於出貨，需求反轉成立。","type":"Single Thing","maps_to":"Single Thing","metric":"電氣滾動 12 個月 book-to-bill","threshold":"連 2 季 <1.0","action":"清倉","source_freq":"季報","date":null},{"n":5,"text":"股價大跌但基本面未破時分批反買。","type":"估值rearm","maps_to":"H1","metric":"收盤價；H1 門檻是否仍成立","threshold":"≤300 美元（約 FY27 Base 18.75 倍）且 book-to-bill ≥1.1","action":"分批反買第三批 1/3","source_freq":"日收盤與季報","date":null},{"n":6,"text":"關稅或原物料吸收失敗。","type":"減碼","maps_to":"R3","metric":"電氣美洲價格成本與環比利潤率","threshold":"價格成本連 2 季轉負且利潤率環比下滑","action":"減碼 1/3","source_freq":"法說，季更","date":null,"evidence_refs":["reg_tariff_export#0"]},{"n":7,"text":"新產能開出後開關設備供給轉鬆。","type":"風險","maps_to":"R2","metric":"電氣美洲在手訂單年增與利潤率年變動","threshold":"在手訂單連 2 季 <10% 且利潤率年減 ≥100bp","action":"停止加碼","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#2","competitive_share_entrants#1"]},{"n":8,"text":"固態變壓器未能由試點轉量產。","type":"風險","maps_to":"R4","metric":"量產訂單揭露與對手具名大案","threshold":"2027 年底前未揭露量產訂單，且對手取得具名大案","action":"減碼 1/3","source_freq":"法說，季更","date":"2027-12-31","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":9,"text":"反壟斷或貿易管制事項出現金額。","type":"風險","maps_to":"R5","metric":"10-Q 應計或揭露金額；程序性質","threshold":"≥1.9 億美元（TTM FCF 約 5%），或進入刑事程序","action":"達金額門檻減碼 1/3；刑事介入清倉","source_freq":"10-Q，季更","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":10,"text":"Boyd 未達管理層 FY27 下限。","type":"風險","maps_to":"R6","metric":"Boyd FY27 營收","threshold":"<27 億美元","action":"停止加碼","source_freq":"法說，季更","date":"2028-02"},{"n":11,"text":"第四季財報與 FY27 指引後複審。","type":"複審日期","maps_to":"H1","metric":"指引、訂單、現金流","threshold":"財報公布後一週內完成","action":"依前述門檻執行","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"電氣滾動 12 個月 book-to-bill","bear_threshold":"<1.0（現值 1.2）","window":"連 2 季","source":"Eaton 季度新聞稿","last_status":"ok"},{"metric":"資料中心滾動 12 個月訂單年增","bear_threshold":"<30%（現值 101%）","window":"連 2 季","source":"Eaton 法說","last_status":"ok"},{"metric":"電氣美洲全年利潤率","bear_threshold":"FY27 <29%（Q3 為 29.8%）","window":"FY27 全年","source":"Eaton 季度新聞稿","last_status":"unknown"},{"metric":"FCF／GAAP 淨利","bear_threshold":"<0.75（FY2025 為 0.87）","window":"連 2 個年度","source":"年報現金流量表","last_status":"ok"},{"metric":"固態變壓器量產訂單","bear_threshold":"未揭露量產訂單","window":"至 2027-12-31","source":"Eaton 法說","last_status":"unknown"}],"evidence_dismissed":[{"ref":"geo_supply_chain#0","reason":"證據本身是一般性風險揭露，原文未列特定國家、金額或已發生事件，無法形成可驗證門檻；關稅的損益影響已另列為風險。"},{"ref":"major_events#3","reason":"證據僅為約 289 輛車用差速器召回，沒有金額，也與電氣及航太論點無關，且與另一筆召回紀錄是同一通報。"},{"ref":"product_recall_warning#0","reason":"與前一筆是同一 NHTSA 通報的重複收錄，規模約 289 輛，來源未提供財務影響。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場在定價 2028 年後的資料中心斷層，但最新一季滾動訂單仍 +101%，資料中心以外的公用事業、住宅與機械 OEM 訂單也在成長；現價只要求約 12% 的 EPS 年複合成長，尚無實證支持需求反轉。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-14.68, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"第二批須 FY27 首次指引 EPS 中點 ≥$15.5 且電氣滾動 12 個月訂單年增 ≥25%；股價 ≤$300 且基本面未破則分批反買","exec_line":"前份股價條件已發動，首批上限為目標部位 1/3；週線仍低於 52 週與 104 週均線，加碼一律等基本面資料點，反彈不追價。"},"reasoning":{"industry":"Q3 營收 89.47 億美元，年增 28%，其中有機 19%、併購 8 個百分點；分部利潤率 25.3%。分部方面，電氣美洲營收 41.72 億美元、利潤率 29.8%；電氣全球約 27 億美元、21.1%；航太約 12 億美元、24.9%；Mobility 由總額反推約 8.75 億美元、17.2%，預計 2027 年第一季併入 Dana。四段營收乘利潤率合計約 22.6 億美元，與公布的 22.63 億美元相符，電氣美洲占約 55%。最新季毛利率事實表未涵蓋，TTM 毛利率 35.05%、營業利益率 17.32%。單點依賴：2023 至 2025 年沒有單一客戶超過淨銷售 10%，客戶集中度不是風險；但資料中心與商用航太合計約占三分之一營收，資料中心這一塊押的是同一條 AI 資本支出。366GW 是產業已公告案量，不是 Eaton 的訂單。產業態勢：競爭面有 Siemens 等進入固態變壓器，結構面訂單與在手訂單加速，其他結構變數是 800V 直流架構遷移，裁決為雙向拉鋸。","moat":"機制是從變壓器、開關設備、斷路器到 UPS 自製，再加模組整合與液冷，客戶得到單一供應商、單一保固與較短交期；CEO 於 2026-11-03 舉 Fibrebond 由 3.75 億美元成長到 6 億美元為例。ROIC 差距事實表未涵蓋，改比利潤率：Eaton 的 TTM 毛利率、營業利益率與 FCF 利潤率接近台達電，三項都低於 Vertiv。份額只有管理層自述，第三方僅有五家合計 41% 至 43%，無 Eaton 單獨份額。執行力給 8 分，電氣美洲利潤率由 Q1 約 25.6% 回到 Q3 的 29.8%，但前一段擴產確實拖累過利潤率。定價力給 7 分，Q3 價格成本轉正、1 月 2 日再調價，但大客戶逐案談，交期緊張解除後才算真正測試。","growth":"共識三年 EPS 年複合約 16.2%：FY2025 調整後 EPS 由指引中點 13.75 美元與管理層所稱年增 14% 反推約 12.06 美元，到 FY28E 18.94 美元。FY27 共識營收年增 11.1%，EPS 年增 19.1%，差 8.0 個百分點，主要靠利潤率與併購綜效。Mobility 出表後，FY27 同範圍營收需年增約 21%，算式為（37,420－800）÷（33,685－3,500）－1，其中 3,500 是 Q3 Mobility 約 875 百萬美元的四倍；這高於管理層終端市場至少 11% 的框架，是我的 Base 低於共識的原因。缺口歸因為利潤率擴張與併購，內生上界無法計算，長期信心上限為中。公司正式的 2026 至 2030 年有機目標仍是 6% 至 9%。","governance":"FY2025 FCF／淨利 0.87（35.53 億÷40.87 億美元），FY2024 為 0.93，Q3 FCF 10.34 億美元。SBC 占營收、現金去向四分、債務到期與加權利率事實表未涵蓋。併購累計投入約 140 億美元，淨負債 201.04 億美元，約為 TTM 營業利益 55 億美元的 3.6 倍。CEO 於 2026-11-03 表明未來 12 個月不做 Boyd 規模併購，接下來以整合為優先。由淨利÷稀釋 EPS 推得股數，2022 年約 4.01 億股、2025 年約 3.91 億股，年減約 0.8%。","valuation":"反推：10% 總報酬扣約 1% 股息，股價年增 9%，五年後約 526 美元，除以 22 倍需 FY31 EPS 23.9 美元，由 13.67 美元起算年複合 11.8%。Base 年報酬約 12%，來自 EPS 複利約 12.8%、倍數收縮約 −1.7%、股息約 1%，報酬不靠重估。成長熄火壓力測試：FY28 後成長降到 15%、10%、5%，搭配 25、20、15 倍，FY31 股價約 703、492、321 美元，三種情境兩種高於現價。賣方平均目標價 431.88 至 485.47 美元，現價低於這些均值 21% 至 30%，但多數早於這波下跌；UBS 的 360 美元是較新的反方看法。全距約 1.35 倍，未到需要因分歧調降信心的程度。","premortem":"最大回撤與空方論證放在情境樹與反證紀錄。週線目前低於 52 週與 104 週均線，RSI 36.99，26 週報酬 −14.68%，代表市場不認同連續上修；我把這視為未解的反方訊號，所以分批且不追價。亮燈的衰退信號有兩項，毛利率下滑與 EPS 成長高於營收，屬中等陷阱風險。歷史最大回撤與法律案件金額事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"Eaton 賺的是資料中心、電網與工商建築的配電與電力轉換設備錢，利潤卡在電氣美洲這一節：Q3 約 55% 的分部利潤來自這個分部。","moat":"護城河方向穩定：端到端電力鏈與供應確定性是真的，但份額與報酬差距都沒有獨立證據支持變寬。","growth":"五年後跑道中等：需求案量充足，但看得到的第二條曲線仍押同一個資料中心資本支出。","capital":"資本配置能驗證的只有股數紀律，大型併購的報酬還要等 Boyd 的利潤數字。","valuation":"現價只要求 EPS 年複合約 12% 搭配 22 倍退出，就有約 10% 年報酬；這接近公司自訂下限，我信得過，但不算便宜。","how_wrong":"最可能看錯的地方，是把 2028 年前已排定的需求當成 2028 年後也存在。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場在定價 2028 年後的資料中心斷層，但最新一季滾動訂單仍 +101%，資料中心以外的公用事業、住宅與機械 OEM 訂單也在成長；現價只要求約 12% 的 EPS 年複合成長，尚無實證支持需求反轉。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":341.72,"week26_return_pct":-14.68,"consensus_rev_3m_pct":1.18,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY26 調整後與 GAAP EPS 指引相差 3.31 美元，占調整後 EPS 的 24%，FY2025 差約 1.61 美元，差距在 Boyd 後擴大。另外 FY27 共識是否完整扣除 Mobility 出表，事實表無法驗證。兩者都使 25 倍不能當成便宜的論據。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 FY27 首次完整指引","impact":"高","watch":"EPS 中點是否 ≥15.5 美元、Mobility 出表口徑、現金流指引"},{"date":"2027-Q1","date_precision":"quarter","type":"other","event":"Mobility 與 Dana 的 Reverse Morris Trust 預計完成","impact":"中","watch":"實收現金約 11 億美元與 FY27 EPS 稀釋幅度"},{"date":"2027-03","date_precision":"month","type":"other","event":"Boyd 開始計入有機成長","impact":"中","watch":"Boyd FY27 至少 27 億美元的進度與利潤率揭露"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"南卡羅來納三相變壓器廠投產爬坡","impact":"中","watch":"電氣美洲利潤率是否再度受拖累"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"固態變壓器由試點轉量產","impact":"中","watch":"量產訂單揭露與對手具名案件"}],"_projected_from":"v19"}
```
