你是 stock-analyst v20 的**散文層（prose）agent**，標的 MAR（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MAR_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MAR　日期：2026-11-08　archetype：None　前份裁決：2026-07-10　觀望｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1957B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（445B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（906B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1339B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（999B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（612B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（985B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2289B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4367B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2477B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1957           3530-5043      5 條（2–6 內）  
s3                  8000         445           5288-7555      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3244          8229-11756      5 條（2–6 內）  
s6                 11000         612          7272-10388      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         985           1760-2515      5 條（2–6 內）  
s10                 5000        2289           1898-2711      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2477           2000-2523      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4562B；至少需散文≈40.44KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−35
−35%
−5%
−4.2
−4.2%
−1
0%
0
0.4%
0.6%
0.67
0.75
0.84
0.86
0.88
1.00
1
1%
1.035
1.0475
1.10
1.15
1.25
1.44%
1.5%
1.69
1.7
1.81
02
2%
2
2.1%
2.14
2.3
2.40
2.4
2.5%
2.6
2.62
2.735
2.82
2.85
2.851
2.87%
2.88
3%
3
03
3.02
3.028
3.09
3.257
3.44%
3.5%
3.8
3.8%
4%
4
4.1%
4.1
4.45
4.5%
4.6%
4.75%
5
5%
05
5.4%
5.5%
5.9%
06
6.0
6%
6
6.2%
6.5%
7%
7.0%
7
7.2
7.5
7.8%
08
8%
8
8.4%
8.5%
8.5
9
9.51
10%
10
10.02
10.9%
11.00
11
11.3%
11.3
11.4
11.64
11.7
11.8
11.8%
11.81
11.96
12
12%
12.5
12.6
12.7
12.70
12.71%
12.72
12.9
13%
13.3
13.30
13.39
13.5
13.75
14%
14
14.4
14.4%
14.5
14.5%
14.9
15%
15.04
15.22
15.75
15.93%
16%
16
16.42
16.55
18
18%
18.05
18.25
18.39
19
19.87%
20%
20
20.05
20.6
21
21%
21.6%
21.7%
22%
22
23.4
24%
24
24.2%
25
26
27
28
29
30%
30
31
31%
31.1
32
34.8
34.82
35%
35.5
36
36.0%
36%
40%
41.4
42
42%
45%
45
48
49
50%
50
52
52%
60
63
65%
70
70.05
75%
90%
90
100%
100
150%
172.25
198
200
240
252.7
266
267
$310
310
347.51
348
372.47
385
391
399
416
416.47
446
463
482
600
670
748.8
2025
2026
2027
2028
2030
2500
2900
5500
6500
20261108
3,000
634,000
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
{"meta":{"ticker":"MAR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Marriott International"},"oneliner":"萬豪的費用、淨房數與回購都在運轉，但 416 美元已是 FY2026 預估本益比 34.8 倍，基準情境五年年化約 6%，不追，等回到約 348 美元再重新評估。","thesis":{"H":[{"id":"H1","text":"全球旅宿需求維持正成長：2027 全球 RevPAR 落在管理層初步區間，穿越一次景氣循環後仍有 2.5% 以上的年化成長。","2y":"FY2027 全球 RevPAR 增 3.5%～4.5%，FY2028 不低於 2.5%","5y":"含一次衰退，五年年化不低於 2.5%","10y":null,"threshold":"全球 RevPAR 年增 ≥2.5%；美加 ≥2%；2027 正式指引下緣 ≥3%","source":"公司季度新聞稿與法說；CoStar／Tourism Economics 美國預測","drift_rule":"兩年期驗證：與門檻偏離 ≥5% 連兩季為削弱，偏離 ≥10% 連三季為反轉。"},{"id":"H2","text":"輕資產系統持續擴張：淨房數維持中個位數成長，管線能轉成開業，費用隨系統成長。","2y":"FY2026 淨房數約 4.5%，FY2027 不低於 4.5%，管線不低於 63 萬間","5y":"至 FY2031 淨房數年化不低於 4.5%","10y":"系統規模再擴四成以上，國際比重提高","threshold":"淨房數年增 ≥4%；管線 ≥60 萬間；施工中客房 ≥26 萬間；轉換案占開業 ≥30%","source":"公司季度新聞稿與法說","drift_rule":"兩年期驗證：與門檻偏離 ≥5% 連兩季為削弱，偏離 ≥10% 連三季為反轉；五年期驗證用連四季與連六季。"},{"id":"H3","text":"業主讓利可控、費用率不被壓縮，EPS 能靠費用成長與回購維持雙位數複合。","2y":"FY2028 調整後 EPS 不低於 14.5 美元","5y":"FY2031 調整後 EPS 不低於 19 美元","10y":null,"threshold":"FY2028 共識 EPS ≥14.5 美元；特許與基本費增速與 RevPAR 加淨房數的落差不超過 2 個百分點；key money ≤投資支出 45%；維持投資等級","source":"Koyfin 共識快照；公司財報與法說；信用評等公告","drift_rule":"兩年期驗證：與門檻偏離 ≥5% 連兩季為削弱，偏離 ≥10% 連三季為反轉。"}],"R":[{"id":"R1","text":"全球衰退使 RevPAR 轉負，費用下滑，高倍數同時下修。","h_ref":"H1","clock":"🔥","threshold":"全球 RevPAR 連兩季低於 0%","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"業主要求更多回饋，key money、費率讓利或聯名卡費分享侵蝕股東經濟。","h_ref":"H3","clock":"🔥","threshold":"key money 超過 7 億美元或占投資支出逾 50%；返還超過客房收入 50 個基點；公司同意分享聯名卡費","evidence_refs":["channel_business_model_shift#2"]},{"id":"R3","text":"新供給、建造成本與同業競爭壓低淨房數與管線轉化。","h_ref":"H2","clock":"🔥","threshold":"淨房數低於 4%；施工中客房低於 26 萬間；與希爾頓淨房數差距 ≥3 個百分點連兩個半年，同業數字目前是資料缺口","evidence_refs":["competitive_share_entrants#1","reg_tariff_export#2"]},{"id":"R4","text":"AI 代理式訂房與 OTA 分流削弱 Bonvoy 直訂優勢。","h_ref":"H3","clock":"🐢","threshold":"Bonvoy 會員房晚占比連兩個半年下滑；公司未在本包揭露，目前是資料缺口","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"id":"R5","text":"Starwood 資料外洩訴訟與英國 CMA 資訊交換調查帶來賠償、裁罰與合規成本。第四巡迴已推翻集體認證，部分原告改為個別提告，調解仍在進行。","h_ref":"H3","clock":"🐢","threshold":"和解或裁罰合計超過市值 1%，約 11 億美元；出現不利集體認證或 CMA 違法認定","evidence_refs":["lawsuit_class_action#0","regulatory_antitrust#0"]},{"id":"R6","text":"中東衝突使 2026 第四季與 2027 上半年 RevPAR 持續承壓，並拖慢管線。","h_ref":"H1","clock":"⚡","threshold":"2027 第一季中東 RevPAR 仍年減逾 20%，或管線流失超出正常水準","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"全球 RevPAR 連續兩季年減。","why_fatal":"這是最大的單一敏感度：RevPAR 每 1 個百分點對應 5500 萬～6500 萬美元費用，由 +4% 轉為 −5% 約少 5 億～6 億美元，每股稅前約 2 美元。現價含 31.1 倍 FY+2 本益比，需求轉負時 EPS 與倍數會一起下修；聯名卡新約對 2028 年的 1 億～1.25 億美元影響小得多。","if_happens":"這是估值重置，不等於生意毀損。未持有者等 FY+2 本益比 22 倍以下，重跑研究後分批反買；已持有者若當時倍數仍高於 26 倍就減碼三分之一，低於 26 倍不因波動賣出。","how_monitor":"每季財報的全球 RevPAR 年增率；領先指標看團體訂房進度與訂房窗口，第三季全球訂房窗口約 21 天，年比大致持平。","probability":"12～24 個月約 15%～20%，屬主觀估計，事實表沒有衰退機率資料。"}},"appendix_a":{"growth_durability":7,"quality_score":7.5,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":31.1,"peg_fy2":2.14,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":10.02,"FY2026E":11.96,"FY2027E":13.39,"FY2028E":15.04},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin 共識調整後 EPS。FY2025A 調整後 EPS 事實表未涵蓋，由 2026-08-03 全年指引 11.64～11.81 美元與年增 16%～18% 反推約 10.02 美元；GAAP 稀釋 EPS 為 9.51 美元，口徑不同，未用於成長率計算。三年複合 14.5%。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MAR_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"旅宿需求循環","confidence":"中","fingerprint":"輕資產收費，靠回購放大每股盈餘，需求隨景氣波動"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉，但供給緩衝厚：CoStar 預估美國 2026、2027 供給僅增約 0.4%、0.6%，在建量為 12 年低點；需求端 2027 面對世足賽高基期，CoStar 預估美國 RevPAR 放緩至 2.1%。","bargaining":{"up":"上游是業主。公司已把忠誠度費率下調約 5%，並自費提供最高 50 個基點的返還，議價空間變窄。","down":"下游是旅客與發卡銀行。Bonvoy 約 3.09 億會員支撐直訂與卡費，但業界分析認為 OTA 占比十年未明顯下降。","geo":"中東占開業客房 3%、管線 6%、2025 總費用 3%；大中華 RevPAR 約持平。"},"profit_pool_dir":"費用端有一部分回吐給業主，卡費則往品牌方集中，淨方向要等 2027 指引確認。","tam_table":{"expanded":false,"reason":"證據包沒有全球客房總量、品牌滲透率與利潤池歷史序列，無法填 TAM、滲透率或五年利潤池變化；本次論點也不建立在低滲透或新品類上。"}},"moat":{"mechanism":"Bonvoy 會員與全球訂房系統形成的雙邊網路，業主付費換取直訂與品牌溢價。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"管線年增逾 6% 至 634,000 間、淨房數 4.6%，代表執行力仍強；費率下調、最高 50 個基點返還與 key money 上升，代表定價權受壓。","peer_na_reason":"事實表只有同業毛利率、營業利益率與自由現金流利潤率，沒有投入資本與 ROIC，無法計算報酬差距；IHG 財務資料也缺。","threats":[{"level":"🟡","text":"AI 目前主要改變旅遊探索，訂房端較慢。附著點是 Bonvoy 帳號與直訂流量；若 2030 年前代理式訂房繞過 Bonvoy，威脅應升級。外部長期預測不是實測。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"訂房、物業管理與忠誠度系統多年改造已遷移逾 3,000 家飯店，較複雜的全服務與豪華飯店還在後面，延誤或中斷會直接傷害業主信任。","p":"20%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"轉換案競爭推高 key money，同業用資本搶業主，壓低新增合約報酬。","p":"40%","evidence_refs":["channel_business_model_shift#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"第三季休閒、團體、商務 RevPAR 分別增 7%、6%、4%，需求廣泛；但旅遊可以延後，訂房窗口約 21 天，能見度短。"},{"item":"決策層級","level":"🟡","text":"決策單位是個別業主。前九個月簽約創新高，代表品牌仍受青睞；轉換案比重高也代表業主可以換牌，合約年限與違約條款事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"業主集體反映成本，公司以降費率、返還與 key money 回應，同時聯名卡費集中在品牌方，分配爭議尚未解決。"},{"item":"社會容忍度","level":"🟢","text":"沒有看到房價管制或費率上限的證據。英國 CMA 調查的是資訊交換，屬合規風險，不是價格天花板。"}],"roiic":"事實表未涵蓋，無法用定義式計算","reinvest_rate":"定義式事實表未涵蓋；粗略參考為 2026 投資支出 12.5～13.5 億美元，約等於 FY2025 營業利益 41.4 億美元的 31%，屬稅前且未扣折舊。","endo_ceiling":8.5,"formula_note":"增量報酬的定義式需要投入資本、折舊與營運資金變動，事實表未涵蓋。內生天花板改用輕資產代理式：淨房數 4.75% 與 RevPAR 3.5% 相乘，(1.0475×1.035)−1≈8.4%，取 8.5%，不含淨回購與利潤率擴張。可能高估的地方是沒有扣除 key money 的資本成本。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","MAR":19.87,"HLT":30.13,"H":20.58,"IHG":null,"CHH":50.18,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","MAR":15.93,"HLT":24.01,"H":8.38,"IHG":null,"CHH":25.1,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","MAR":12.71,"HLT":14.49,"H":2.45,"IHG":null,"CHH":6.8,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"HLT","gm":30.13,"om":24.01,"fcf_margin":14.49,"strategy_note":"利潤率表面高於萬豪，但代墊成本比重未拆開，不能直接當護城河差距；前份追蹤的淨房數差距本次事實表未涵蓋。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"H","gm":20.58,"om":8.38,"fcf_margin":2.45,"strategy_note":"營業利益率與自由現金流利潤率都明顯低於萬豪，事實表沒有足以比較品牌力的數字。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"IHG","gm":null,"om":null,"fcf_margin":null,"strategy_note":"事實表無財務資料，無法判讀。"},{"name":"CHH","gm":50.18,"om":25.1,"fcf_margin":6.8,"strategy_note":"利潤率高於萬豪；萬豪在中階市場已接近 600 家飯店，雙方競爭可能升高。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量（淨房數 4.6%）＋價（RevPAR 6.5%）＋聯名卡與住宅品牌費＋回購；近 12 個月沒有併購。","runway_years":"滲透率事實表未涵蓋，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板 8.5%，共識三年複合 14.5%，差 6.0 個百分點，歸因於淨回購與利潤率擴張。","segments":[{"item":"總費用收入（第三季）","value":"15.22 億美元，年增 14%"},{"item":"獎勵管理費（第三季）","value":"1.81 億美元，年增 22%；第四季預估約持平"},{"item":"聯名卡費（2026 全年）","value":"預估增加高 30% 區間；新約對 2028 全年影響 1 億～1.25 億美元"},{"item":"住宅品牌費（2026 全年）","value":"預估增逾 90%；第三季因交屋時點年減 35%"},{"item":"分時度假費（2026 全年）","value":"1.10 億～1.15 億美元，大致持平"}],"decay_signals":[{"signal":"毛利率連兩季年減","status":"資料缺口","note":"事實表沒有季度毛利率，年度數字又受代墊成本影響。"},{"signal":"核心市占縮減","status":"資料缺口","note":"同業淨房數與份額事實表未涵蓋。"},{"signal":"提價後銷量下滑","status":"未亮","note":"法說稱多數市場房晚與房價並進，沒有相反數據。"},{"signal":"EPS 成長顯著高於營收成長","status":"亮","note":"三年 EPS 複合 14.5%，FY2026 至 FY2027 共識營收約增 5.9%，差距超過 5 個百分點。"},{"signal":"自由現金流對淨利連兩年低於 0.75","status":"未亮","note":"FY2022 至 FY2025 分別約 0.86、0.88、0.84、1.00。"},{"signal":"SBC 占營收高且上升","status":"資料缺口","note":"SBC 金額事實表未涵蓋。"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"未亮","note":"AI 目前主要影響探索，尚無訂房份額移轉數據。"},{"signal":"產業倍數系統性下移","status":"資料缺口","note":"同業歷史倍數事實表未涵蓋。"},{"signal":"維持性資本支出占自由現金流過高","status":"資料缺口","note":"維持性支出未拆分。"},{"signal":"停止投資且收入下滑","status":"未亮","note":"管線創新高，FY2022 至 FY2025 營收逐年成長。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；近三年現金去向與債務到期結構事實表未涵蓋，只有 2026 全年股東回饋至少 48 億美元的指引。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 沒有併購協議，無已實現併購報酬可評分。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價事實表未涵蓋。以 52 週均線 347.51 美元與 FY1 EPS 11.96 美元代入，盈餘殖利率約 3.44%，現價約 2.87%；要過關，十年期公債殖利率需低於約 1.44%。十年期殖利率事實表未涵蓋。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"由淨利除以稀釋 EPS 反推稀釋均股：3.257、3.028、2.851、2.735 億股，每年淨減 4.1%～7.0%。SBC 金額事實表未涵蓋，毛稀釋率無法計算。","grade":"過"}]},"valuation":{"basis":"FY2026E 共識調整後 EPS 的預估本益比，並以 FY+2 本益比對照前份區間","tier":"高品質輕資產飯店品牌","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業預估本益比，無法做跨公司倍數對照。"},"fwd_pe":34.82,"peg":2.4,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"FY+2 本益比 31.1 倍高於前份區間上緣，PEG 2.40 高於 2，四個年度端點中位於最高，基準情境五年年化約 6%，低於 8%。五年分位缺資料，結論不依賴它。","upside_short_pct":-4.2,"upside_mid_pct":11.3},"trap_analysis":{"verdict":"🟡","label":"生意不差，但每股成長高度依賴回購與費率以外的步階收入"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"RevPAR 每少 1 個百分點，相關費用少 5500 萬～6500 萬美元；現價 FY+2 本益比 31.1 倍，淨負債約為第三季年化 EBITDA 的 2.85 倍。","assumption":"需求持續正成長，倍數維持 30 倍上下。","consequence":"RevPAR 由 +4% 轉為 −5%，費用約少 5 億～6 億美元，每股稅前約少 2 美元；倍數壓回 18～20 倍時，股價可能到 200～240 美元，跌 42%～52%。","ruling":"採納。這是五年虧損五成最可能的路徑，也就是唯一致命點，因此不另立第二個故事。","watch":"全球 RevPAR 年增率、團體訂房進度、訂房窗口。","evidence_refs":["supply_demand_durability#3","end_markets#3"],"fact_refs":["f_kpi6_worldwide_revpar_growth","f_net_debt_m","f_shares_diluted_m"]},{"view":"論點成功但股東經濟變差","evidence":"公司下調忠誠度費率約 5%，自費提供最高 50 個基點返還；key money 約 5 億～6 億美元且預期續增；全球新建案開工前三季減約 24%，資料品質受管理層保留。","assumption":"淨房數與 RevPAR 達標，費用就會等比例流到股東。","consequence":"系統越做越大，但新增房間的取得成本上升，費用成長落後系統成長，EPS 更依賴舉債回購。","ruling":"部分採納。目前讓利規模仍小於費用增量，但放進基準情境的 EPS 略低於共識，並設定 key money 與費用落差的監測門檻。","watch":"key money 金額與占比、特許與基本費增速減 RevPAR 與淨房數的落差。","evidence_refs":["channel_business_model_shift#2","competitive_share_entrants#1","reg_tariff_export#2"],"fact_refs":["f_kpi5_gross_fee_revenues","f_kpi9_net_rooms_pipeline"]},{"view":"價格已反映太多","evidence":"FY1 預估本益比 34.82 倍，PEG 約 2.40，四個年度端點中位於最高；七月賣方目標價平均低於現價。","assumption":"市場會繼續為回購驅動的雙位數 EPS 付 30 倍以上。","consequence":"即使 EPS 年化 10.9%，倍數回到 27 倍後，股價年化僅約 5.4%，加股息約 6%。","ruling":"採納，這是目前不進場的唯一綁定原因。","watch":"FY+2 預估本益比；賣方第三季後更新的目標價。","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_consensus_eps_fy2"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 372.47 → 本次 416.47（+11.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=372.47","side_b":"本次 price_at_dd=416.47","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🔴、均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 372.47 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 372.47 美元：Bull 價 670、Bear 價 266，五年期望值 +24.2%，基準年化 5.5%，不對稱比 2.3","side_b":"本次情境、股價仍用 372.47 美元：Bull 價 748.8、Bear 價 252.7，五年期望值 +36.0%，基準年化 7.8%，不對稱比 2.62","ruling":"先換情境、股價不動：五年期望值多 11.8 個百分點，基準年化多 2.3 個百分點。不對稱比由 2.3 變為 2.62。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 372.47 美元：五年期望值 +36.0%，基準年化 7.8%，不對稱比 2.62","side_b":"本次情境、股價 416.47 美元：五年期望值 +21.6%，基準年化 5.4%，不對稱比 1.69","ruling":"再換股價、情境不動：起點價上漲 11.8%，五年期望值少 14.4 個百分點，基準年化少 2.4 個百分點，不對稱比由 2.62 降到 1.69。合計五年期望值比前份少 2.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與裁決","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 372.47 美元，FY+2 本益比約 29 倍，估值偏貴，裁決觀望。","side_b":"本次股價 416.47 美元，FY+2 本益比 31.1 倍，高於前份區間上緣，估值轉為昂貴；情境機率維持 25／45／30，最大回撤區間 −55%～−35%。","ruling":"變化主要來自股價上漲 11.8%，FY+2 EPS 由約 12.9 美元升至 13.39 美元只抵銷一部分，因此仍是不追。","evidence_level":"事實表價格與共識數字；前份 EPS 由 24 倍對 310 美元反推","settle_metric":"FY+2 預估本益比","if_then":["若 FY+2 本益比降到 26 倍以下，重跑研究後分批反買。","若股價續漲但 2027 指引未高於 4.5%，不追。"],"evidence_refs":[]},{"axis":"品質判斷未改","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份總評 B、價值陷阱中度、護城河方向穩定、五年後跑道中等，屬品質複利成長，循環位置未填。","side_b":"本季 RevPAR 與管線更強，但業主讓利、key money 與費用品質的疑慮也更明確。","ruling":"正負證據相抵，上述判斷都不變。公司按品質複利成長看待，循環位置本次同樣不填。","evidence_level":"2026-08-03 與 2026-11-02 法說、公司新聞稿","settle_metric":"2027 年 2 月的費用與淨房數指引","if_then":["若特許與基本費增速連兩季落後 RevPAR 加淨房數超過 2 個百分點，護城河方向改為縮減並停止加碼。","若落差收斂且管線持續成長，維持原判。"],"evidence_refs":["end_markets#0","channel_business_model_shift#2"]},{"axis":"進場條件改以報酬反解","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"Fwd PE(FY+2) 回落至 ~24x（~$310）或全球 RevPAR 連 2 季轉負（衰退重置）；或 Fwd PE 連 6 月 <22x 且分析師目標中位下修","side_b":"FY+2 預估本益比回到 26 倍以下（約 348 美元）；觸發後重跑研究再定首倉，不直接進場","ruling":"舊條件以歷史倍數為錨，本次改成基準情境五年年化約 10% 反解的進場價。衰退分支移到唯一致命點處理，避免把價格與事件兩個條件混在一起。","evidence_level":"情境樹算術","settle_metric":"FY+2 預估本益比","if_then":["價格達標後先重跑研究，通過才以小額首倉進場。","若 EPS 共識下修超過 5%，進場價同步下移，不沿用 348 美元。"],"evidence_refs":[]},{"axis":"Single Thing 由未設改為全球 RevPAR 連兩季年減","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設（原欄位為空）","side_b":"全球 RevPAR 連續兩季年減","ruling":"需求轉負是數學上最大的單一敏感度，同時打擊 EPS 與倍數，其規模大於聯名卡新約或業主讓利。","evidence_level":"2026-11-02 財務長敏感度","settle_metric":"季度全球 RevPAR 年增率","if_then":["發生時，未持有者等 FY+2 本益比 22 倍以下，重跑研究後分批反買。","發生時，已持有者若倍數仍高於 26 倍就減碼三分之一。"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"新增量化減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（原欄位為空）","side_b":"全球 RevPAR 連兩季年減就檢視減碼；淨房數低於 4% 連兩季停止加碼；key money 超過 7 億美元或占投資支出逾 50% 停止加碼；同時出現淨房數低於 3% 與費用落差超過 4 個百分點才清倉。","ruling":"本次把前份風險表的觀察項改成可執行門檻，前份的淨房數、集體訴訟與會員房晚指標都保留在風險清單，取不到的值標資料缺口。","evidence_level":"判斷者設定，依據公司指引與敏感度","settle_metric":"季度財報","if_then":["達到單一門檻時先停止加碼或減碼，不直接清倉。","兩項結構性門檻同時成立才清倉。"],"evidence_refs":[]},{"axis":"假設門檻上調與改寫","cause":"新證據","prior_field":["H1.threshold","H3.threshold"],"side_a":"全球 RevPAR 年增 ≥1.5%；Fwd PE(FY+2) 24-31x","side_b":"全球 RevPAR 年增 ≥2.5%；第三項假設改看 EPS、費用落差與 key money","ruling":"2027 初步區間已到 3.5%～4.5%，舊底線太低。現價已高於舊倍數區間上緣，倍數改由進場條件處理，第三項假設改驗證業主讓利下的每股經濟。","evidence_level":"2026-11-02 法說","settle_metric":"2027 年 2 月正式指引","if_then":["若正式指引下緣低於 3%，第一項假設判為削弱並不追。","若 2028 共識 EPS 跌破 14.5 美元，停止加碼。"],"evidence_refs":["supply_demand_durability#0","end_markets#2"]},{"axis":"2027 需求展望","cause":null,"side_a":"管理層初步看全球 RevPAR 3.5%～4.5%，世足賽高基期可由 EMEA 低基期抵銷。","side_b":"CoStar／Tourism Economics 預估 2027 美國 RevPAR 僅增 2.1%，且房價成長低於通膨。","ruling":"可調和，兩者地區範圍不同，管理層 2026 年也持續上修。基準情境取 3.5%～4%，不採上緣；這項要到正式預算才能裁定。","evidence_level":"公司前瞻與第三方預測，都不是實績","settle_metric":"2027 年 2 月全球與美加 RevPAR 指引","if_then":["若美加指引低於 2.5%，下修基準 EPS 並不追。","若全球指引高於 4.5%，基準 EPS 上修後重算進場價。"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#3","end_markets#2","end_markets#3"]},{"axis":"費用成長品質","cause":null,"side_a":"2026-11-02 財務長表示特許與基本費權利金率沒有壓縮。","side_b":"同場 Rothschild 分析師指出，扣除聯名卡與住宅費後，費用成長落後 RevPAR 與淨房數；全年總費用增約 13%，高於 4.75% 與 4.6% 的簡單加總。","ruling":"可調和但未證實。管理層沒有提供扣除後數字，本次不採信也不否定；先預登記，若 2027 年前兩季落差仍超過 2 個百分點，就視為費率受壓。","evidence_level":"法說問答，缺分項資料","settle_metric":"特許與基本費增速減 RevPAR 與淨房數增速","if_then":["連兩季落差超過 2 個百分點就停止加碼。","連四季落差超過 4 個百分點就減碼。"],"evidence_refs":["channel_business_model_shift#2"]},{"axis":"業主關係與 key money","cause":null,"side_a":"2026-08-03 CEO 說談判用的 key money 比部分同業少，2026-11-02 又說討論透明、合作、具建設性，不會有重大宣布。","side_b":"同一位 CEO 也稱 key money 是競爭中的常用武器，財務長預期合約取得成本續增；CEO 拒絕正式回應業主公開信，也未拆分轉嫁與自行吸收金額。key money 案件每房價值溢價 65%～75% 是公司自算，缺成本端。","ruling":"可調和：新業主仍願意簽約，既有業主仍在爭取分配。CEO 對同業的比較自述為軼事，不採為證據。方向判定維持穩定，但列為第一順位監測。","evidence_level":"法說管理層陳述，缺獨立數據","settle_metric":"key money 金額與占投資支出比重","if_then":["key money 超過 7 億美元或占比逾 50% 就停止加碼。","若公司同意分享聯名卡費，重算 EPS 後再決定是否減碼。"],"evidence_refs":["channel_business_model_shift#1","channel_business_model_shift#2"]},{"axis":"中東復甦說法","cause":null,"side_a":"2026-08-03 CEO 指 2027 EMEA 可望隨中東復甦強勁成長；外部報導列中東占房量 4%、管線 7%、費用 4%。","side_b":"2026-11-02 CEO 改為假設旅遊干擾持續、2027 逐步改善，並列中東占開業客房 3%、管線 6%、2025 總費用 3%。","ruling":"口徑較前一季保守，暴露比例採公司最新說法。沙烏地活動取消使第四季年減幅擴大，但 3% 費用占比不足以單獨改變論點。","evidence_level":"法說一手說法與二手報導","settle_metric":"2027 第一季中東 RevPAR 與管線流失","if_then":["若 2027 第一季中東 RevPAR 仍年減逾 20%，把 2027 RevPAR 假設降到區間下緣並不追。","若管線流失超出正常水準，淨房數假設下修並停止加碼。"],"evidence_refs":["geo_supply_chain#0"]},{"axis":"產業態勢三軸","cause":null,"side_a":"競爭端惡化：轉換案競爭推高 key money，業主要求更多回饋。","side_b":"結構端轉好：美國新供給處於 12 年低點，公司轉換案占開業逾 40%；其他結構變數是 AI 改變旅遊探索與英國 CMA 調查。","ruling":"雙向拉鋸。供給緩衝支持費用，取得新合約的成本卻在上升，兩者方向相反但都還不足以改變護城河方向。","evidence_level":"法說、CoStar、CMA 案件頁","settle_metric":"key money、淨房數與美國供給成長","if_then":["若美國新建開工持續增加 20% 且供給預估高於 2%，下修 RevPAR 假設並不追。","若 key money 回落且淨房數高於 5%，上修基準情境。"],"evidence_refs":["supply_demand_durability#2","competitive_share_entrants#1","regulatory_antitrust#0"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"指引不斷上修，2026 RevPAR 由 1.5%～2.5% 升到 4.5%～5%；EPS 增 20%～21%；管線與會員都創新高；美國供給低，2027 仍有 3.5%～4.5% 的初步看法。好公司很少跌到便宜價，觀望可能錯過多年複利。","side_b":"即使基準 EPS 年化 10.9%，倍數由 34.8 倍回到 27 倍，股價年化只有約 5.4%；空方機率 30%，上下檔比約 1.7，新資金的安全邊際不足。","ruling":"選擇不追。這不是對公司品質的否定，而是現價已預付多年成長。市場若持續給 30 倍以上，這個判斷會錯，但錯的代價是少賺，買在高位遇到衰退的代價是跌五成。","evidence_level":"情境樹與法說","settle_metric":"FY+2 預估本益比與 2027 指引","if_then":["若股價續漲但指引未再上修，不追。","若股價跌但費用與淨房數門檻未破，到 348 美元附近重跑研究後分批反買。","若 2027 指引高於 4.5% 且 FY2028 EPS 共識升到 16 美元以上，重算進場價；否則維持不追。"],"evidence_refs":["end_markets#1","capital_markets_pricing#4"]}],"triggers":[{"n":1,"text":"股價回到基準報酬約 10% 的區間，重跑研究再決定首倉。","type":"估值rearm","maps_to":"進場條件","metric":"FY+2 預估本益比","threshold":"≤26 倍（約 348 美元）","action":"重跑研究，通過後分批反買","source_freq":"每週，收盤價與最新共識","date":null},{"n":2,"text":"全球需求進入衰退，EPS 與倍數同時下修。","type":"Single Thing","maps_to":"R1","metric":"全球 RevPAR 年增率","threshold":"連兩季 <0%","action":"未持有者等 22 倍以下分批反買；持有且倍數高於 26 倍則減碼三分之一","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"2027 正式指引驗證需求假設。","type":"假設驗證","maps_to":"H1","metric":"2027 全球 RevPAR 指引下緣","threshold":"≥3%","action":"低於門檻就不追並下修基準 EPS","source_freq":"第四季財報","date":"2027-02"},{"n":4,"text":"系統成長與管線轉化。","type":"假設驗證","maps_to":"H2","metric":"淨房數年增、管線、施工中客房","threshold":"淨房數 ≥4%；管線 ≥60 萬間；施工中 ≥26 萬間","action":"連兩季低於門檻就停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["competitive_share_entrants#1","reg_tariff_export#2"]},{"n":5,"text":"業主讓利與新增合約成本升高。","type":"風險","maps_to":"R2","metric":"key money 金額與占投資支出比重；費用增速落差","threshold":"key money >7 億美元或占比 >50%；落差連兩季 >2 個百分點","action":"停止加碼","source_freq":"每季財報與法說","date":null,"evidence_refs":["channel_business_model_shift#2"]},{"n":6,"text":"中東干擾拖累 RevPAR 與管線。","type":"風險","maps_to":"R6","metric":"中東 RevPAR 年增率與管線流失","threshold":"2027 第一季年減逾 20% 或管線流失超出正常水準","action":"下修 2027 假設並不追","source_freq":"每季法說","date":"2027-05","evidence_refs":["geo_supply_chain#0"]},{"n":7,"text":"資料外洩訴訟與英國競爭法調查出現不利結果。民事和解由財務影響決定動作，若出現刑事介入則重新評估治理並可清倉。","type":"風險","maps_to":"R5","metric":"和解或裁罰金額、調查結論","threshold":"合計超過市值 1%（約 11 億美元）","action":"減碼三分之一；刑事介入則清倉","source_freq":"10-K、10-Q、CMA 案件頁","date":null,"evidence_refs":["lawsuit_class_action#0","regulatory_antitrust#0"]},{"n":8,"text":"持有者的估值上限。","type":"減碼","maps_to":"R1","metric":"FY+2 預估本益比","threshold":"≥36 倍（約 482 美元）","action":"減碼三分之一","source_freq":"每週","date":null},{"n":9,"text":"第四季財報與 2027 正式指引後複審。","type":"複審日期","maps_to":"H1","metric":"RevPAR、費用、淨房數、key money 指引","threshold":"完整更新","action":"重算情境與進場價","source_freq":"第四季財報","date":"2027-02"}],"kill_metrics":[{"metric":"全球 RevPAR 年增率","bear_threshold":"連兩季低於 0%","window":"2 季","source":"公司季度財報","last_status":"ok"},{"metric":"淨房數年增率","bear_threshold":"低於 4% 連兩季；低於 3% 為結構性破位","window":"2 季","source":"公司季度財報","last_status":"ok"},{"metric":"key money 金額與占投資支出比重","bear_threshold":"超過 7 億美元或占比逾 50%","window":"1 個會計年度","source":"公司法說與新聞稿","last_status":"ok"},{"metric":"特許與基本費增速減 RevPAR 與淨房數增速","bear_threshold":"連兩季落後超過 2 個百分點；連四季超過 4 個百分點","window":"2～4 季","source":"公司財報；分項資料目前是缺口","last_status":"unknown"},{"metric":"FY2027 共識 EPS","bear_threshold":"低於 12.72 美元，即較 13.39 美元下修 5%","window":"2027 年 6 月前","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[{"ref":"capital_markets_pricing#1","reason":"這是 2026-08-03 對第三季的指引，已被實績取代：第三季調整後 EPS 3.02 美元，高於指引上緣 2.82 美元，也高於當時共識 2.88 美元。"},{"ref":"major_events#1","reason":"與同份 10-K 的另一條 EPA 紀錄是同一事件，重複收錄且方向標記不一致；內容只涉及一家受管飯店，未揭露金額，也沒有指向費用或合約的傳導路徑。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2026 年的步階式成長當成常態：全年總費用增約 13%，高於 RevPAR 4.75% 加淨房數 4.6%，差額主要來自聯名卡新約與住宅品牌費，這些增速不會重演；同時以 34.8 倍為部分靠回購驅動的 EPS 定價。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🔴', moat_trend='→', week26=18.39, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🔴'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"FY+2 預估本益比回到 26 倍以下（約 348 美元）；觸發後重跑研究再定首倉，不直接進場","exec_line":"現價不建倉、不追；回到約 348 美元先重跑研究，通過後以小額首倉分批進場；已持有者續抱，FY+2 本益比達 36 倍（約 482 美元）時減碼三分之一。"},"reasoning":{"industry":"第三季總營收 70.05 億美元，總費用收入 15.22 億美元，占 21.7%，其餘分項金額事實表未涵蓋。TTM 毛利率 19.87%、營業利益率 15.93%，分母含代墊成本，不能直接當獲利能力看。第三季費用成長來自 RevPAR 6.5%、淨房數 4.6% 與聯名卡費。管理層預估 2026 全年聯名卡費增加高 30% 區間，住宅品牌費增逾 90%，這兩項的增速不會年年重演。單點依賴方面，Host 的客戶資料停在 FY2021，不足以判斷現況；目前看得到的集中點是聯名卡合約，金額與合作方占比事實表未涵蓋。產業處於擴張期，依據是第三季全球 RevPAR 增 6.5%，美加不含世足賽仍增 6.2%。反例是大中華約持平、中東年減 12%，擴張並非全面。","moat":"機制是雙邊網路：Bonvoy 約 3.09 億會員帶來直訂，吸引業主加入，634,000 間管線再擴大會員可用的飯店。執行面在變強，前九個月有機簽約創新高，轉換案占開業逾 40%。定價面在變弱，公司下調忠誠度費率約 5%，自費提供最高 50 個基點返還，CEO 也說 key money 是競爭中的常用武器。兩者相抵判為穩定。可能看錯的地方是同業 ROIC 差距與份額事實表未涵蓋；若希爾頓的淨房數領先持續擴大，方向就應改為縮減。TTM 利潤率低於希爾頓不能當證據，因為兩家代墊成本比重未拆開。","growth":"調整後 EPS 基期約 10.02 美元，由 2026-08-03 指引 11.64～11.81 美元與年增 16%～18% 反推；到 FY2028E 15.04 美元，三年複合 14.5%。內生天花板 8.5%，缺口 6.0 個百分點。其中淨回購約 3.8～4.1 個百分點：2026 股東回饋至少 48 億美元，扣股息約 7.2 億美元後占市值 3.8%，FY2025 稀釋均股減 4.1%。其餘約 2 個百分點來自費用增速高於 G&A 的利潤率擴張。缺口可以歸因，不必靠倍數上修，但每股盈餘成長約四分之一來自回購。反例是淨房數若由轉換案與中階品牌加速，內生天花板會高於 8.5%。","governance":"FY2022 至 FY2025 自由現金流對淨利約 0.86、0.88、0.84、1.00，現金轉換良好。以 TTM 自由現金流利潤率 12.71% 乘 FY2026 共識營收，自由現金流約 35.5 億美元，低於 48 億美元的股東回饋。淨負債 172.25 億美元，含租賃，約為第三季年化 EBITDA 的 2.85 倍，季節性未調整；管理層承諾維持投資等級，循環信貸也由 45 億美元增至 50 億美元。SBC 占營收、四類現金去向、債務到期結構與回購均價事實表未涵蓋。可能看錯的地方是回購紀律：股價越高，同樣金額買回的股數越少，EPS 增厚效果會下降。","valuation":"現價 416.47 美元，FY1 預估本益比 34.82 倍，FY+2 為 31.1 倍，高於前份 24～31 倍區間上緣。PEG 以 34.82 倍除以三年複合 14.5%，約 2.40，屬偏貴。五年分位事實表未涵蓋，只有四個年度端點，現值位於最高。短期目標以 FY2027E 13.30 美元乘 30 倍得 399 美元，較現價 −4.2%；中期以 FY2029E 16.55 美元乘 28 倍得 463 美元，較現價 +11.3%。30 倍來自前份 FY+2 五年均值 26～27 倍，乘共識 FY2027 與 FY2026 EPS 比值後換算。賣方目標價平均約 385～391 美元，最高 446 美元，但多為七月資料，第三季上修後可能偏舊，只作低權重參考。反例是 EPS 指引持續上修，2026 成長指引已由 16%～18% 升到 20%～21%，連續超預期時市場可能繼續給高倍數。","premortem":"2026 全球 RevPAR 指引由 1.5%～2.5% 一路升到 4.5%～5%，管理層指引明顯保守，因此觀望可能錯過續漲。另一方面，第二季法說管理層不正式回應業主公開信，也未拆分轉嫁與自行吸收的金額；第三季被問到扣除卡費與住宅費後的費用成長時，只回答權利金率沒有壓縮，未給數字。歷史最大回撤、訴訟金額事實表未涵蓋。價值陷阱風險中度，唯一亮起的衰退信號是 EPS 成長遠高於營收成長。"},"plain":{"six":{"how_it_makes_money":"萬豪賺的是飯店業主與發卡銀行付的品牌費，錢卡在 Bonvoy 會員與全球訂房系統這一節點，最新一季總費用收入 15.22 億美元，年增 14%。","moat":"護城河方向穩定：規模與管線仍在擴大，但維持這個位置要付更多 key money 與業主讓利。","growth":"五年後跑道中等：淨房數仍有中個位數成長，但滲透率事實表未涵蓋，也沒有足以單獨撐起成長的第二曲線。","capital":"資本配置穩定而偏積極：2026 股東回饋至少 48 億美元，高於自由現金流，差額需要舉債支應。","valuation":"現價要求未來五年 EPS 年增超過一成，而且本益比續守 30 倍上下；需求與回購我相信，倍數我不信。","how_wrong":"最可能看錯的是低估連續超預期的力量；對股東最大的傷害則來自需求轉負時 EPS 與倍數一起下修。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2026 年的步階式成長當成常態：全年總費用增約 13%，高於 RevPAR 4.75% 加淨房數 4.6%，差額主要來自聯名卡新約與住宅品牌費，這些增速不會重演；同時以 34.8 倍為部分靠回購驅動的 EPS 定價。","momentum_overheated":null,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等 FY+2 預估本益比回到 26 倍以下，約 348 美元，再重跑研究。","trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":416.47,"week26_return_pct":18.39,"consensus_rev_3m_pct":2.4,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"世足賽約 45 個基點 RevPAR，換算費用約 2500 萬～2900 萬美元，不足以改變倍數判讀；住宅品牌費的絕對金額事實表未涵蓋。EV/S 有 16.42 與 4.45 兩個數字，分母口徑明顯不同，本案不用 EV/S 定價。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉","impact":"低","watch":"第四季美加 RevPAR 是否只受小幅影響"},{"date":"2026-12","date_precision":"month","type":"other","event":"紐約分析師交流會","impact":"低","watch":"是否提前透露 2027 費用、key money 或業主方案"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 正式指引","impact":"高","watch":"RevPAR、特許與基本費、聯名卡費、key money、淨房數"},{"date":"2027-06","date_precision":"month","type":"macro","event":"開始面對世足賽高基期","impact":"中","watch":"美加 RevPAR 扣除賽事基期後的成長"},{"date":"2027-12","date_precision":"month","type":"product","event":"全服務與豪華飯店科技系統遷移波次延續至年底","impact":"中","watch":"系統中斷、業主投訴與導入進度"},{"date":null,"date_precision":null,"type":"regulatory","event":"英國 CMA 飯店資訊交換調查進度","impact":"中","watch":"是否出現違法認定、裁罰金額或資料服務調整"}],"_projected_from":"v19"}
```
