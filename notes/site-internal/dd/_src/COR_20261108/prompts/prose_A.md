你是 stock-analyst v20 的**散文層（prose）agent**，標的 COR（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：COR　日期：2026-11-08　archetype：None　前份裁決：2026-05-25　B 觀望偏進場｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1911B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（417B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（805B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（773B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（898B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（764B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1486B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2295B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4400B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3731B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1911           3562-5089      5 條（2–6 內）  
s3                  8000         417           5308-7583      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2476          8767-12524      5 條（2–6 內）  
s6                 11000         764          7165-10236      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1486           1410-2014      3 條（2–6 內）  
s10                 5000        2295           1893-2705      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3731           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3918B；至少需散文≈41.08KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−40%
−40
−35%
−25%
−25
−22.7%
−5
0
0.1%
0.35
0.47%
0.6%
0.72
0.72%
0.9
01
1
1.01
1.10%
1.15%
1.4%
1.4
1.41%
1.44
1.5%
1.5
1.52
1.61
1.8%
1.90
1.94
02
2%
2
2.59
2.71
3
03
3%
3.6%
3.6
3.7%
4
04
4%
4.04%
4.2
4.55
4.6%
4.66
5
05
5%
5.5%
5.9
06
6%
6
6.7%
7%
07
7
7.239
7.96
8
08
8%
8.5
9
09
9%
9.1
9.10
9.28%
9.98
10
10%
10.3%
10.5%
10.54%
10.9%
11%
11
11.4
12
12%
12.5
12.6%
12.9%
13%
13.88
14
14%
15
15%
15.21
15.4
16
16.9
16.93
17
17.3%
17.80
17.85
17.86
17.95
17.97
18%
18
18.4
18.58
19
19.40
19.5
19.575
19.70
19.7
19.75
20.00
20
20%
20.1
20.2
20.35
20.9
21%
21.3%
21.5
21.6
21.93
22
22.9
23%
23
23.9
24
24.27
25%
26
26.2
26.2%
26.3
27.7
28
28%
28.3%
28.3
28.8
29.4
29.9%
30%
30
32.5
33
34%
34.9
35
35%
37.2
38%
38.08
38.81
40%
41%
42
45%
47.90
49
50
50%
52%
57
57.6%
63.9
66%
70
78
80%
90%
90
94%
100%
100
104
109%
150%
216
220
240
258
268
274.91
296
298.89
314
333.56
340
345.6
349
350
366
373
420.8
460.8
520
627
636.5
783
884
2025
2026
2027
2028
2030
20261108
2,000
4,000
9,330
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
{"meta":{"ticker":"COR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Cencora, Inc."},"oneliner":"Cencora 把藥品配送的現金轉進專科藥與醫師管理平台，FY2027 指引撐得住約 10% 的 EPS 成長。但 333.56 美元的基本情境年報酬只有約 7%，Walgreens 占營收 25%、應收 38% 是最大斷點，現價不追，296 美元以下再談。","thesis":{"H":[{"id":"H1","text":"專科藥與醫師服務分部是成長引擎，營業利益維持中雙位數成長，占比逐年上升。","2y":"FY2027 分部營業利益成長 18–21%，FY2028 ≥ 13%","5y":"FY2031 占扣除 Other 後營業利益 ≥ 50%（FY2026 由指引反推約 41%）","10y":null,"threshold":"FY2027 低於 15%，或 FY2028 起任兩季低於 10%","source":"Cencora 季報新分部（FY2027 Q1 起）、2026-11-04 法說指引、分部重編 8-K","drift_rule":"2 年論點連 2 季偏離 ≥ 5% 算削弱，連 3 季偏離 ≥ 10% 算反轉；5 年論點連 4 季偏離 ≥ 5% 算削弱，連 6 季偏離 ≥ 10% 算反轉。"},{"id":"H2","text":"藥品配送與服務是現金底盤，扣掉客戶移量與匯率後仍能維持中個位數營業利益成長。","2y":"FY2027 分部營業利益成長 ≥ 2%，FY2028 ≥ 4%","5y":"FY2027–FY2031 平均年增 ≥ 4%","10y":null,"threshold":"FY2027 低於 2%，或 FY2028 低於 3%","source":"Cencora 季報新分部、2026-11-04 法說指引","drift_rule":"2 年論點連 2 季偏離 ≥ 5% 算削弱，連 3 季偏離 ≥ 10% 算反轉；5 年論點連 4 季偏離 ≥ 5% 算削弱，連 6 季偏離 ≥ 10% 算反轉。"},{"id":"H3","text":"調整後 EPS 有現金支撐，併購賺得回資本成本。","2y":"FY2027 調整後 FCF ≥ 35 億美元，約為調整後淨利 ≥ 90%","5y":"五年累計 FCF ÷ 調整後淨利 ≥ 90%，MSO 併購沒有大額減損","10y":null,"threshold":"FY2027 調整後 FCF 低於 30 億美元，或單筆商譽減損 ≥ 5 億美元","source":"季報現金流量表、年報商譽附註、法說資本配置段","drift_rule":"2 年論點連 2 季偏離 ≥ 5% 算削弱，連 3 季偏離 ≥ 10% 算反轉；5 年論點連 4 季偏離 ≥ 5% 算削弱，連 6 季偏離 ≥ 10% 算反轉。"}],"R":[{"id":"R1","text":"Walgreens 與 Boots 繼續移出量體，或財務惡化。私有化後評等撤銷，外界只能看公司揭露。","h_ref":"H2","clock":"⚡","threshold":"主協議終止或破產 → 清倉；再揭露移量、FY2027 10-K 占營收低於 20%，或占應收高於 45% → 減碼三分之一","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#3"]},{"id":"R2","text":"Evernorth（占營收約 13%）量體流失：Cigna 新設批發配送，法說未點名的大型郵購客戶連三季下滑。","h_ref":"H2","clock":"🔥","threshold":"10-K 占營收由 13% 降到 9% 以下，或公司確認協議縮減 → 減碼三分之一","evidence_refs":["customer_second_source#0"]},{"id":"R3","text":"Part B 給付、ASP 規則與 340B 改變專科經濟，管理層尚未量化。","h_ref":"H1","clock":"🐢","threshold":"規則定案後公司量化的分部營業利益衝擊 ≥ 5%，或專科分部毛利率連 2 季年減 → 減碼三分之一","evidence_refs":["regulatory_antitrust#0"]},{"id":"R4","text":"併購賺不回資本成本。OneOncology 首年 EPS 中性，PharmaLex 已減損 7.239 億美元，後面還有兩筆交易。","h_ref":"H3","clock":"🔥","threshold":"OneOncology 滿 24 個月（2028-02）仍無正 EPS 貢獻，或單筆商譽減損 ≥ 5 億美元 → 停止加碼","evidence_refs":[]},{"id":"R5","text":"關稅、學名藥通縮與供應鏈法規成本吸收不了。","h_ref":"H2","clock":"🐢","threshold":"配送分部營收成長減營業利益成長連 4 季大於 3 個百分點，且管理層歸因成本 → 減碼三分之一","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#0"]}],"single_thing":{"description":"Walgreens 主供應商協議終止，或 Walgreens 申請破產。","why_fatal":"Walgreens 與 Boots 合計約占 FY2025 營收 25%、應收帳款 38%，是最大的單一營收與信用敞口。協議終止會同時砍營收並拖累配送規模效益，破產還要加上應收減損。應收金額與該客戶利潤占比事實表未涵蓋，衝擊只能按比例粗估。","if_happens":"清倉，等應收損失金額和替代量體確定後再重做研究。參考跌幅是 Max DD 深端 −40%，加上應收減損可到 −50%。","how_monitor":"8-K 客戶揭露、FY2026 與 FY2027 10-K 的營收與應收占比、法說對移量的說法。私有化後 Walgreens 沒有公開季報，這是監測盲區。","probability":"12 至 24 個月約 8%。這是判斷值，沒有評等或違約資料可以校準。"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.21,"peg_fy2":1.44,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":17.97,"FY2027E":19.7,"FY2028E":21.93,"FY2029E":24.27},"fy_end_month":9,"eps_basis":"調整後稀釋 EPS，財年 9 月底；FY2026A 來自 2026-11-04 法說，FY2027–FY2029 為 Koyfin 2026-11-07 共識快照，分析師家數事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"千分之十幾的營業利益率，靠規模與周轉賺錢，EPS 成長靠專科組合、併購與回購疊加。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：藥品需求不能延後，到 2030 年有 100 多項新腫瘤藥（2026-11-04 法說，管理層口徑）；三大批發商 2026 年配銷營收預估 9,330 億美元（Drug Channels），新進者難以複製。","bargaining":{"up":"對製造商有配送與商業化服務的議價，但製造商也在試直送病患，上游優勢只算中等。","down":"下游偏弱：前十大客戶占營收 66%，Walgreens 已部分移量。專科診所端較強，因為 MSO 直接持股。","geo":"以美國為主，國際約占 Q4 營收 9%；歐洲配送受美元影響，FY2027 約 2,000 萬美元逆風。"},"profit_pool_dir":"由傳統配送往專科與 MSO 移動。五年利潤池占比事實表未涵蓋，只能由指引反推 FY2026 專科約占 41%。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與五年利潤池占比，分部重編 8-K 也不在本次資料內，展開只能靠管理層口徑，不足以填表。"}},"moat":{"mechanism":"全國配送、冷鏈與專科物流的規模，加上 MSO 把專科醫師綁進平台；三家寡占下靠周轉率賺錢。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：排除兩筆 MSO 併購與失去腫瘤客戶後，FY2026 美國核心營業利益成長約 13%。定價面縮減：毛利率上升主要來自併購，Walgreens 2026-07-01 起部分量體移出，大型郵購客戶連三季下滑。兩者抵銷，判穩定；最大客戶份額下滑，不能判擴大。","peer_na_reason":"事實表只有同業利潤率，沒有投入資本與 ROIC，無法計算報酬差距，改看利潤率與最大客戶份額方向。","threats":[{"level":"🟡","text":"製造商、藥局、醫療提供者與保險人持續整併，壓低議價力或造成客戶流失。","p":"40%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"大客戶把部分量體移走或自建配送與專科業務。目前是個別客戶行為，尚未變成全行業轉向。","p":"35%","evidence_refs":["customer_second_source#0","competitive_share_entrants#3"]},{"level":"🟡","text":"製造商直送病患由試點變成策略項目，可能繞過批發通路。只有單篇產業報導，尚無量體數字；三大批發商的配銷規模與 MSO 持股是反面證據。","p":"30%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"病患使用、醫師或 PBM 決定、保險付款，三個角色都成立；藥品不能延後。FY2026 在製造商降價下營收仍增 5%。"},{"item":"決策層級","level":"🟡","text":"替代發生在主供應商合約與品項層級。Walgreens 主協議不變但部分量體已移出，證明客戶能拆單；MSO 診所端黏著度較高。"},{"item":"價值鏈分配","level":"🟡","text":"配送環節只拿約 1.4% 營業利益率，前十大客戶占 66%，毛利率上升靠併購。MSO 是往價值鏈高處走，能否多拿利潤還沒證明。"},{"item":"社會容忍度","level":"🟡","text":"專科經濟依賴 Part B 給付、ASP 規則與 340B，2026-08-05 法說管理層拒絕量化。事實表未見立法直接針對配送商，故不判紅燈。"}],"roiic":"事實表未涵蓋收購對價與投入資本，無法計算。方向代理：OneOncology 12 個月扣融資後 EPS 中性（2026-08-05 法說 Eva Boratto），首年約等於稅後融資成本。","reinvest_rate":"事實表未涵蓋折舊、營運資金變動與收購淨額，無法計算；可得數字只有 FY2026 資本支出 9.1 億美元、FY2027 約 10 億美元。","endo_ceiling":null,"formula_note":"公式＝增量 ROIC × 再投資率，輸入都缺，不用替代數字硬算。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","COR":4.12,"CAH":3.9,"MCK":3.67,"HSIC":31.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","COR":1.44,"CAH":1.26,"MCK":1.67,"HSIC":5.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","COR":0.47,"CAH":1.9,"MCK":1.64,"HSIC":3.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"CAH","gm":3.9,"om":1.26,"fcf_margin":1.9,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"MCK","gm":3.67,"om":1.67,"fcf_margin":1.64,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"HSIC","gm":31.59,"om":5.79,"fcf_margin":3.64,"period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量（專科與 GLP-1）為主，併購次之，回購每年約 2%，價格為負。","runway_years":"事實表未涵蓋專科藥與 MSO 滲透率，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"事實表缺收購對價、投入資本、折舊與營運資金變動，內生上界無法推導。情境上按保守處理，Bear 機率取 30%。","segments":[{"item":"專科藥與醫師服務","value":"FY2027 營收增 9–14%，營業利益增 18–21%（含 OneOncology 前四個月延續），長期中雙位數；FY2026 約占扣除 Other 營業利益 41%（由指引反推）"},{"item":"藥品配送與服務","value":"FY2027 營收增 4–6%，營業利益增 2–4%（含客戶移量延續與約 1 個百分點匯率），長期中個位數"},{"item":"Other（待處分）","value":"FY2027 營收約 35 億美元、營業利益約 2 億美元，對集團營業利益成長約 −5 個百分點"},{"item":"MSO","value":"約占 FY2026 集團營業利益 10%，EyeSouth 視網膜業務與 American Oncology Network 未計入指引"}],"decay_signals":["核心市占近 12 個月縮減：Walgreens 部分移量、大型郵購客戶連三季下滑、FY2025 失去腫瘤客戶","EPS CAGR 顯著高於營收 CAGR：共識 EPS 10.5% 對營收約 4.6%"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"FY2026 股東回報","value":"約 15 億美元，含回購約 10 億（均價 268 美元）與股息"},{"item":"FY2027 回購計畫","value":"12.5 億美元"},{"item":"股息","value":"季配息調升 10%，連續第 22 次"},{"item":"債務","value":"RCA 定期貸款 8 億美元已還清；FY2027 年底償還 OneOncology 定期貸款 10 億美元"},{"item":"資本支出","value":"FY2026 9.1 億美元，FY2027 約 10 億美元"},{"item":"併購","value":"OneOncology 2026-02 完成；EyeSouth 視網膜業務與 American Oncology Network 待交割；對價事實表未涵蓋"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2026-08-05 法說 Eva Boratto：OneOncology 12 個月扣融資後調整後 EPS 中性，首年約等於稅後融資成本；Q4 FY2025 PharmaLex 商譽減損 7.239 億美元，該業務已列入待處分。對價與投入資本事實表未涵蓋。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"FY2026 回購 10 億美元、均價 268 美元，以 FY2026 調整後 EPS 17.97 美元計買入收益率 6.7%。10 年期公債殖利率事實表未涵蓋，無法判定是否高出 2 個百分點。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 金額事實表未涵蓋，改用股數反推：Q4 稀釋股數年減 1.8%（約 350 萬股），10 億美元 ÷ 268 美元約回購 373 萬股，扣掉回購後股本年增約 0.1%，低於 1.5%。","grade":"過"}]},"valuation":{"basis":"FY2027E 共識 EPS 的 Forward P/E，FCF 殖利率對照。","tier":"藥品配送三大寡占","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有 Forward P/E 或 EV/EBITDA，同業估值比較無法展開，補不到就不寫數字。"},"fwd_pe":16.93,"peg":1.61,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"16.93 倍 ÷ 三年共識 EPS 複合 10.54%＝PEG 1.61，落在合理區間；FY2027 調整後 FCF 約 35 億美元 ÷ 市值 636.5 億美元＝殖利率約 5.5%；基本情境年報酬約 7%。事實表沒有五年序列，五年分位留空。1 年上檔：FY2028E 21.6 美元 × 16 倍＝345.6 美元，+3.6%；3 年上檔：FY2030E 26.3 美元 × 16 倍＝420.8 美元，+26.2%。","upside_short_pct":3.6,"upside_mid_pct":26.2},"trap_analysis":{"verdict":"🟡","label":"生意沒壞，但客戶集中度高、併購報酬未證"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Walgreens 與 Boots 合計占 FY2025 營收約 25%、應收約 38%，私有化後評等已撤銷，2026-07-01 起部分量體移出。","assumption":"主供應商協議繼續有效，新股東不會進一步拆分採購。","consequence":"協議終止時 EPS 停在 20 美元上下，倍數 11 至 12 倍，股價約 220 至 240 美元，比現價跌 28% 至 34%；再加應收減損可到 −50%。","ruling":"採納為最大風險，與唯一致命點相同。協議未變不等於風險解除，因為私有化後外界看不到對方財務。","watch":"FY2026 10-K 的客戶與應收占比，以及任何揭露移量的 8-K。","evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#3"],"fact_refs":[]},{"view":"論點失敗","evidence":"2026-08-05 法說 Robert Mauch 拒絕量化 340B 與 ASP 規則影響；2026-11-04 法說回答給付問題時只談政策倡議。","assumption":"給付變動不傷專科診所經濟，2028 年 IRA 延伸到 Part B 後醫師給付不受負面影響。","consequence":"專科成長由中雙位數降到個位數，EPS 路徑掉向 Bear，MSO 併購的資本回不來。","ruling":"部分採納。現有證據的時間窗蓋不到 2028 年風險窗，不能說風險已解，裁定為不可裁決至規則定案。","watch":"CMS 年度給付規則、專科分部毛利率、管理層是否開始量化。","evidence_refs":["regulatory_antitrust#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"OneOncology 首年 EPS 中性；資本支出升到約 10 億美元；Q4 GAAP EPS 2.71 美元對調整後 4.66 美元；EyeSouth 與 American Oncology Network 還要再花錢。","assumption":"MSO 併購之後靠臨床試驗與服務疊加拉高報酬。","consequence":"專科占比上升、調整後 EPS 達標，但增量資本報酬低於資本成本，每股 FCF 成長落後 EPS，倍數不會升。","ruling":"部分採納。基本情境倍數由 16.93 降到 16，不給專科化溢價。","watch":"FY2027 調整後 FCF、OneOncology 滿 24 個月的 EPS 貢獻、商譽減損。","evidence_refs":[],"fact_refs":["f_kpi1_gaap_operating_income_ma","f_kpi3_adjusted_diluted_eps_q4","f_kpi4_free_cash_flow_fy2026_op"]},{"view":"價格已反映太多","evidence":"26 週漲 28.3%，比前份 274.91 美元高 21.3%；FY2027 共識已在指引上緣；基本情境年報酬約 7%。","assumption":"市場會繼續用約 17 倍買 10% 成長，不回到 5 月的約 15 倍。","consequence":"回到 15 倍就是 296 美元，跌 11%，基本面不必變差。","ruling":"採納，這是本次不追的唯一約束。","watch":"FY2027E 共識本益比與財報後賣方目標價更新。","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_consensus_eps_fy1","f_price_at_dd"]}],"max_dd":{"lo":-40,"hi":-25,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 274.91 → 本次 333.56（+21.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=274.91","side_b":"本次 price_at_dd=333.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 274.91 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 274.91 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 274.91 美元：Bull 價 627、Bear 價 258，五年期望值 +57.6%，基準年化 10.9%，不對稱比 13.88","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 13.88。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 274.91 美元：五年期望值 +57.6%，基準年化 10.9%，不對稱比 13.88","side_b":"本次情境、股價 333.56 美元：五年期望值 +29.9%，基準年化 6.7%，不對稱比 2.59","ruling":"再換股價、情境不動：起點價上漲 21.3%，五年期望值少 27.7 個百分點，基準年化少 4.2 個百分點，不對稱比由 13.88 降到 2.59。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"共識上修是真的嗎","cause":null,"prior_field":null,"side_a":"FY1 共識三個月上修 10.3%（17.86 → 19.70 美元）。","side_b":"8 月的 FY1 是 FY2026，11 月的 FY1 已換成 FY2027，這是財年換算。同財年比較：FY2026 實際 17.97 美元只比 8 月共識多 0.6%；FY2027 在 2026-08-05 法說上 JPMorgan 分析師說市場約增 14%，以指引中點 17.85 美元換算約 20.35 美元，現在 19.70 美元，少約 3%，其中 MWI 的 0.35 美元在 8 月已提示。","ruling":"採 B 側，性質是方向相反但屬資料口徑，可調和。上修 10.3% 不能當動能證據，同財年實際方向是小幅下修。決策若引用此數字應人工覆核。","evidence_level":"程式快照加逐字稿；14% 為分析師口述，不是正式共識。","settle_metric":"FY2027 共識相對 19.70 美元的變化","if_then":["如果 2027-02 財報後 FY2027 共識高於 20.00 美元，上調基本情境 EPS 並重算進場價。","反向：如果共識跌破 19.40 美元，停止加碼。"],"evidence_refs":[]},{"axis":"管理層對客戶續約的說法","cause":null,"prior_field":null,"side_a":"2026-08-05 法說 Robert Mauch 說續約沒有需要特別提的。","side_b":"2026-08-12 8-K 揭露 2026-07-01 起部分 Walgreens 量體移出；2026-11-04 法說 Eva Boratto 把客戶移量列為 FY2027 配送分部的延續壓力。","ruling":"可調和但扣分。主協議未變，字面上不算續約，不過移量在法說當下已生效，依摘錄法說沒有主動提。此後客戶議題只看 8-K、10-K 數字。規模不大：配送指引 2–4% 比中個位數目標少約 2 個百分點，匯率占 1 個，移量約 1 個。","evidence_level":"一手 8-K 加逐字稿摘錄","settle_metric":"FY2026 與 FY2027 10-K 的 Walgreens 營收占比","if_then":["如果 FY2027 10-K 占營收低於 20%，減碼三分之一。","反向：如果占比維持 23% 以上且無新揭露，解除客戶揭露扣分。"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"現在就買還是等價位","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：16.9 倍買 EPS 目標 10–14% 的公司；FY2027 排除 MWI 後 EPS 增 10–12%；FCF 殖利率約 5.5%；股息連續 22 次調升；賣方目標價都高於現價。","side_b":"現價已比前份高 21%，基本情境年報酬約 7%，FY2027 共識在指引上緣，新分部要到 2027-02 才有第一季實績。","ruling":"採 B 側。卡點只有價格，基本面沒有破；不是逢高賣出的理由，只是現在買的報酬不夠。可能看錯的地方是管理層一貫超標，FY2027 若超過指引上緣，等待會錯過一段。","evidence_level":"公司指引與程式估值資料","settle_metric":"股價相對 296 美元，以及專科分部前兩季營業利益成長","if_then":["如果股價收在 296 美元以下，且 Walgreens、Evernorth 沒有新增移量，分批反買，分三批。","如果股價續漲超過 366 美元而專科分部還沒有一季實績，不追。","反向：如果 FY2027 Q1、Q2 專科分部成長都 ≥ 18%，基本情境倍數由 16 倍提到 17 倍，進場價上移到約 314 美元。"],"evidence_refs":[]},{"axis":"估值結論由便宜轉合理","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 274.91 美元，以當時 FY2026 指引中點 17.80 美元計約 15.4 倍，結論為便宜。","side_b":"現價 333.56 美元，FY2027E 共識 16.93 倍，結論轉為合理。","ruling":"主因是股價漲 21.3%，EPS 基礎換到下一財年只吸收一部分，倍數升約 1.5 倍。","evidence_level":"程式價格與共識","settle_metric":"FY2027E 共識本益比","if_then":["如果本益比回到 15 倍（約 296 美元），分批反買。","反向：如果本益比升到 19 倍以上而 EPS 未上修，不追。"],"evidence_refs":[]},{"axis":"綜合評等與陷阱風險維持不變","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份綜合評等 B，陷阱風險中等。","side_b":"本次仍為 B 與中等，依據換成新分部指引、Walgreens 移量與 OneOncology 併表。","ruling":"結論不變，理由更新。專科成長證據變強，客戶集中證據變差，兩者抵銷。","evidence_level":"一手財報、8-K 與逐字稿","settle_metric":"專科分部營業利益成長與 Walgreens 占比","if_then":["如果兩項同時惡化，減碼三分之一。","反向：如果專科連兩季 ≥ 18% 且客戶占比穩定，把價格門檻上移重算。"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"前份空白欄位首次填寫","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位沒有值。","side_b":"本次第一次填：護城河穩定、成長空間中等、商業類型為品質複利、非循環股不判循環位置、機率 20／50／30、Max DD −25% 至 −40%；定期定額結論與角色由程式產生。","ruling":"沒有舊值可比，不算結論改變。","evidence_level":"格式差異","settle_metric":"下一份報告對照本次值","if_then":["如果下一份這些欄位有變，按原因逐欄歸因。"],"evidence_refs":[]},{"axis":"Single Thing 由空白改為 Walgreens 主供應商協議","cause":"方法變動","prior_field":null,"side_a":"前份唯一致命點欄位為空。","side_b":"Walgreens 主供應商協議終止，或 Walgreens 申請破產。","ruling":"前份把 Walgreens 放在第一項風險，這次升為 Single Thing，因為 25% 營收、38% 應收是最大單一敏感度，發生時清倉。","evidence_level":"一手 10-K 與 8-K","settle_metric":"協議狀態與破產申請","if_then":["如果任一成立，清倉。","反向：如果 FY2027 10-K 占比仍在 23% 以上且主協議延續，下調事件機率。"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"清倉與減碼門檻更新","cause":"新證據","prior_field":null,"side_a":"WBA 公告 Chapter 11／出售／>20% store closure → 立即清倉；連 4 季 OI margin ≤ 1.10% → 結構性破壞，減倉 1/2；連 4 季 OI margin 15% → 減倉 1/3。","side_b":"主供應商協議終止或破產 → 清倉；再揭露移量或 FY2027 10-K 占營收低於 20% → 減碼三分之一；配送分部 FY2027 營業利益成長低於 2% → 停止加碼；專科分部 FY2027 低於 15% → 停止加碼。","ruling":"「出售」一項退休：Sycamore 私有化已於 2025-08-28 完成，主協議未變，前份寫談判中是過時資訊。店數改看公司揭露的營收占比，因為私有化後 Walgreens 不再公開季報。配送利益率 1.10% 與 RCA 利益率因新分部重編與未單獨揭露取不到值，保留在賣出指標並標資料缺口。","evidence_level":"一手 8-K、逐字稿；重編 8-K 不在本次資料內","settle_metric":"新分部第一季揭露","if_then":["如果新分部揭露配送利益率，恢復 1.10% 門檻並減碼一半。"],"evidence_refs":["customer_concentration_credit#3"]},{"axis":"重新進場條件新增","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份沒有重新進場條件。","side_b":"股價收盤 ≤ 296 美元（約 FY2027E 共識 15 倍），且 Walgreens、Evernorth 沒有新增移量，分批反買。","ruling":"296 美元由基本情境 460.8 美元、10% 年報酬倒推，與 FY2027E 共識 15 倍和 104 週均線 298.89 美元接近。","evidence_level":"情境推算與程式均線","settle_metric":"收盤價與大客戶揭露","if_then":["如果條件成立，分批反買，分三批。","反向：如果跌到 296 美元以下是因為大客戶移量，不買，先重做研究。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Walgreens 主供應商協議終止，或 Walgreens 申請破產，立即清倉。","type":"Single Thing","maps_to":"Single Thing","metric":"主供應商協議狀態、破產申請","threshold":"協議終止或破產申請任一成立","action":"清倉","source_freq":"8-K，事件發生時","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#3"]},{"n":2,"text":"Walgreens 再揭露移量或占比跌破門檻，減碼三分之一。","type":"減碼","maps_to":"R1","metric":"Walgreens 與 Boots 占營收與應收比例","threshold":"再有 8-K 揭露移量，或 FY2027 10-K 占營收低於 20%，或占應收高於 45%","action":"減碼三分之一","source_freq":"8-K 即時，10-K 每年","date":"2027-11","evidence_refs":["customer_concentration_credit#2"]},{"n":3,"text":"Cigna 批發配送是一季內的新利空，管理層不評論，賣方模型是否納入事實表未涵蓋。第一個確認數據出來前不加碼，Evernorth 占比跌破門檻就減碼。Evernorth 與 Cigna 的關聯事實表未載明，本次按同一風險處理。","type":"減碼","maps_to":"R2","metric":"Evernorth 占營收比例","threshold":"由約 13% 降到 9% 以下，或公司確認協議縮減","action":"減碼三分之一","source_freq":"10-K 每年，法說每季","date":"2027-02","evidence_refs":["customer_second_source#0"]},{"n":4,"text":"專科分部成長不到門檻就停止加碼。","type":"假設驗證","maps_to":"H1","metric":"專科藥與醫師服務分部營業利益年增率","threshold":"FY2027 低於 15%，或 FY2028 起任兩季低於 10%","action":"停止加碼","source_freq":"季報，每季","date":"2027-02","evidence_refs":[]},{"n":5,"text":"配送分部成長不到門檻就停止加碼。","type":"假設驗證","maps_to":"H2","metric":"藥品配送與服務分部營業利益年增率","threshold":"FY2027 低於 2%，或 FY2028 低於 3%","action":"停止加碼","source_freq":"季報，每季","date":"2027-02","evidence_refs":[]},{"n":6,"text":"管理層把 FY2026 現金流超標歸因於量、組合與時點。FY2027 調整後 FCF 若低於門檻，視為歸因不成立。","type":"假設驗證","maps_to":"H3","metric":"調整後自由現金流","threshold":"FY2027 低於 30 億美元","action":"減碼三分之一","source_freq":"財報新聞稿，每年","date":"2027-11","evidence_refs":[]},{"n":7,"text":"關稅、學名藥通縮與供應鏈法規不做預測，只看公司有沒有吸收掉。","type":"風險","maps_to":"R5","metric":"配送分部營收成長減營業利益成長","threshold":"差距連 4 季大於 3 個百分點，且管理層歸因成本或學名藥通縮","action":"減碼三分之一","source_freq":"季報，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#0"]},{"n":8,"text":"FTC 於 2026-05-20 對 MWI 與 Covetrus 合併發出補件要求，FY2027 指引假設年中完成，影響約營業利益 1.5 億美元、EPS 0.35 美元。","type":"風險","maps_to":"H3","metric":"MWI 與 Covetrus 交割時點","threshold":"2027-09-30 前未完成，或 FTC 提起訴訟","action":"停止加碼","source_freq":"8-K、季報","date":"2027-09","evidence_refs":["regulatory_antitrust#2"]},{"n":9,"text":"2026-05 股價下跌後多家律所宣布調查，目前只是調查公告，尚未提告，本身不動作。民事集體訴訟通過認證才減碼。","type":"風險","maps_to":"治理風險","metric":"證券集體訴訟進度","threshold":"正式提告且通過集體認證","action":"減碼一半","source_freq":"法院文件、10-Q","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":10,"text":"若 SEC 或司法部就財測揭露介入，清倉。","type":"清倉","maps_to":"治理風險","metric":"SEC 或司法部調查","threshold":"公司揭露正式調查或刑事介入","action":"清倉","source_freq":"8-K、10-Q","date":null,"evidence_refs":["major_events#1"]},{"n":11,"text":"估值回到基本情境 10% 年報酬的價位，分批反買。","type":"估值rearm","maps_to":"H1","metric":"收盤價與大客戶揭露","threshold":"收盤 ≤ 296 美元，且 Walgreens、Evernorth 沒有新增移量","action":"分批反買","source_freq":"每日收盤，8-K","date":null,"evidence_refs":[]},{"n":12,"text":"FY2027 Q1 財報複審，對照 Q1 調整後 EPS 約 4.55 美元與新分部第一次實績。","type":"複審日期","maps_to":"H1","metric":"Q1 調整後 EPS、分部營業利益","threshold":"EPS 低於 4.55 美元，或專科分部成長低於 18%","action":"停止加碼","source_freq":"季報","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"Walgreens 與 Boots 主供應商協議及占營收比例","bear_threshold":"協議終止或破產；FY2027 10-K 占營收低於 20%","window":"每份 8-K、10-K，至 FY2027 10-K","source":"SEC 8-K、10-K 客戶集中揭露","last_status":"warning"},{"metric":"Evernorth 占營收比例","bear_threshold":"由約 13% 降到 9% 以下","window":"FY2026、FY2027 10-K","source":"SEC 10-K","last_status":"unknown"},{"metric":"專科藥與醫師服務分部營業利益年增率","bear_threshold":"FY2027 低於 15%，或 FY2028 起任兩季低於 10%","window":"FY2027 Q1 起逐季","source":"Cencora 季報新分部","last_status":"unknown"},{"metric":"藥品配送與服務分部營業利益年增率","bear_threshold":"FY2027 低於 2%，或 FY2028 低於 3%","window":"FY2027 Q1 起逐季","source":"Cencora 季報新分部","last_status":"unknown"},{"metric":"調整後自由現金流","bear_threshold":"FY2027 低於 30 億美元","window":"FY2027 全年","source":"Cencora 財報新聞稿","last_status":"unknown"},{"metric":"配送分部營業利益率（前份門檻，資料缺口）","bear_threshold":"連 4 季 ≤ 1.10%，新分部基期待重編資料確認","window":"FY2027 Q1 起逐季","source":"季報；分部重編 8-K 不在本次資料內","last_status":"unknown"},{"metric":"RCA 營業利益率（前份門檻，資料缺口）","bear_threshold":"前份文字為連 4 季 15%，方向不明；公司未單獨揭露","window":"待公司揭露","source":"事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[{"ref":"competitive_share_entrants#2","reason":"聚合網站數字，同業群組成與計算方法都沒揭露；0.9 個百分點的差距也混入製造商降價與 GLP-1 組合差異，無法判定市占方向。客戶流失改用 10-K 與 8-K 一手證據判斷。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=28.3, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價收盤回到 296 美元以下（約 FY2027E 共識 15 倍），且 Walgreens、Evernorth 沒有新增移量。卡點是價格，基本面沒有破。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價收盤 ≤ 296 美元（約 FY2027E 共識 15 倍），且 Walgreens、Evernorth 沒有新增移量","exec_line":"現價不追。跌到 296 美元以下且基本面未破，分三批反買；續漲而專科分部尚無實績，不追。"},"reasoning":{"industry":"收錢方式有三種：向製造商收配送與服務費、向藥局和醫院賺採購價差、透過 MSO 分享專科診所利潤。Q4 FY2026 營收 884 億美元，舊分部美國 783 億、營業利益 9.98 億；國際 78 億、1.52 億；Other 23 億、1.01 億。調整後毛利率 4.04%，調整後營業利益率 1.41%，毛利率多出的 57 個基點主要來自併購 OneOncology，不是原有業務漲價。2026-11-04 起改成專科藥與醫師服務、藥品配送與服務兩大分部，MSO 約占 FY2026 營業利益 10%。單點依賴是集中度風險，不是護城河證據：Walgreens 加 Boots 約占 FY2025 營收 25%，Evernorth 約 13%，前十大 66%。產業時鐘判擴張期，依據是 FY2026 營收增 5%、GLP-1 單季多 28 億美元、專科藥占美國藥品支出過半，不是股價。產業態勢判雙向拉鋸：競爭面有客戶轉單與整併壓議價（10-K、2026-08-12 8-K）；結構面專科藥五年增 80%（2026-11-04 法說，管理層口徑）；其他結構變數是製造商降價（Q4 少 28 億美元營收）與 Part B 給付規則。","moat":"機制是全國配送網路、冷鏈與專科物流的規模，加上 MSO 把醫師端綁在平台上。事實表沒有投入資本，算不出對同業的 ROIC 差距，改看利潤率與最大客戶份額：COR 毛利率高於 McKesson 與 Cardinal，但營業利益率低於 McKesson，毛利率優勢主要來自併表 MSO 的業務組合，不能當成定價力提升。當期報酬屬低利益率、高周轉，營運資金天數事實表未涵蓋，只能定性。增量報酬看 OneOncology：2026-08-05 法說 Eva Boratto 稱 12 個月扣融資後 EPS 中性，首年報酬約等於稅後融資成本。可能看錯的地方：RCA 與 OneOncology 的臨床試驗和服務疊加尚未計入，管理層稱 OneOncology 仍在早期，若兩年後報酬明顯上升，這個判斷要改。","growth":"成長來自量、併購與回購，價格是負貢獻：Q4 GLP-1 多 28 億美元，製造商降價少 28 億美元。共識 EPS 由 FY2026 實際 17.97 美元到 FY2029 的 24.27 美元，三年複合 10.5%；共識營收 FY2027 到 FY2028 只增 4.6%。由指引反推專科權重：扣除 Other 的營業利益成長 8.5–11%，配送 2–4%，專科 18–21%，低中高三組都解出專科約占 FY2026 扣除 Other 營業利益的 41%。若專科年增 15%、配送 5%，FY2031 專科占比約 52%。CFO 說專科中雙位數目標包含小型併購，所以不能全當內生。回購每年約 2%（12.5 億美元 ÷ 636.5 億美元市值）。內生上界因 ROIIC 與再投資率都缺，無法計算，共識與上界的缺口無法量化，長期信心上限定為中。衰退信號亮兩個：最大客戶份額縮減；EPS 複合比營收複合高約 5.9 個百分點，其中部分是製造商降價和處分業務壓低營收。","governance":"FY2026 FCF 38.81 億美元（營運現金流 47.90 億減資本支出 9.10 億），調整後 38.08 億，超過原指引約 30 億，管理層歸因於量、組合與時點，時點部分可能回吐；FY2027 指引約 35 億。對調整後淨利：FY2026 以 17.97 美元 × 約 1.94 億股計約 34.9 億，轉換率約 109%；FY2027 以指引中點 19.575 美元 × 1.90 億股計約 37.2 億，約 94%。資料衝突：同業表 COR 的 TTM FCF 利潤率 0.47% 與公司公告換算的 1.15% 對不上，本次採公司公告。淨負債 63.9 億美元，FY2027 年底償還 OneOncology 定期貸款 10 億。SBC 金額與近三年現金四分去向事實表未涵蓋。營運槓桿沒有壓縮：FY2027 營收增 3–5%、營業利益增 4–6%。","valuation":"FY2027E 共識 19.70 美元對應 16.93 倍，已在指引 19.40–19.75 美元上緣。要達 10% 年報酬，扣 0.72% 股息後股價需年增 9.28%，五年後約 520 美元；16 倍下要 EPS 32.5 美元（由 17.97 美元複合 12.6%），基本情境 28.8 美元下要 18 倍。資料限制：trailing 本益比 18.58 倍在 3 個年度端點的分位為 0，但 18.58 倍隱含 EPS 約 17.95 美元，是調整後口徑，FY2025 GAAP EPS 只有 7.96 美元，歷史端點若用 GAAP 就不可比，事實表未列端點值，無法確認，所以不拿 0 分位當便宜證據；P/S 與 EV/S 同時在最高分位。賣方目標價 349–366 美元都在 2026-11-04 財報前，只比現價高 5–10%，支持不追。同業 Forward P/E 事實表未涵蓋。","premortem":"陷阱風險中等，衰退信號亮兩個。反證與裁定都在反證紀錄，共四條：Walgreens 斷點、專科給付規則、併購報酬、價格已反映。事實表沒有歷史最大回撤序列，路徑風險以 2026-05-06 單日跌 17.3% 與 Bear 倍數推估。"},"plain":{"six":{"how_it_makes_money":"賺的是藥廠和藥局之間的配送與服務錢，每 100 美元營收只留約 1.4 美元營業利益，利潤節點正從一般配送移到專科藥與醫師管理平台。","moat":"護城河穩定，評 B：規模與專科網路難以複製，但最大客戶份額在下滑，定價力沒有變強。","growth":"成長空間中等：傳統配送已飽和，專科藥與 MSO 是真實的第二曲線，但多半靠併購取得，滲透率事實表未涵蓋。","capital":"資本配置中等：回購時點好、股本稀釋低，但併購報酬還沒證明。","valuation":"現價合理偏滿。要賺 10% 年化，得靠 EPS 五年複合 12.6%，或倍數升到 18 倍，我只信 EPS 複合約 10%。","how_wrong":"最可能看錯的是客戶集中，不是專科成長；其次是併購報酬與給付規則。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等股價收盤回到 296 美元以下（約 FY2027E 共識 15 倍），且 Walgreens、Evernorth 沒有新增移量。卡點是價格，基本面沒有破。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":333.56,"week26_return_pct":28.3,"consensus_rev_3m_pct":10.3,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"Q4 GAAP EPS 2.71 美元與調整後 4.66 美元差距大，但 FY2027 調整後 FCF 每股約 18.4 美元，約為指引中點的 94%，調整後 EPS 有現金支撐，分母不是本次爭點。FY2027 含約 4,000 萬美元與 MWI 交易相關的營業外收益，是否持續事實表未涵蓋。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"FY2026 10-K 申報","impact":"高","watch":"Walgreens、Boots 與 Evernorth 的營收和應收占比"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"Profarma 股權出售預計於 FY2027 第一季完成","impact":"低","watch":"營收減少幅度是否符合指引"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2027 Q1 財報，新分部第一次實績","impact":"高","watch":"Q1 調整後 EPS 對約 4.55 美元，專科分部營業利益成長"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"MWI 與 Covetrus 合併假設於 FY2027 年中交割，FTC 審查中","impact":"中","watch":"FTC 結果與交割時點，EPS 影響約 0.35 美元"},{"date":"2028-01","date_precision":"quarter","type":"regulatory","event":"2028 年 IRA 延伸到 Part B（2026-08-05 法說提及）","impact":"高","watch":"專科診所給付與管理層是否量化影響"}],"_projected_from":"v19"}
```
