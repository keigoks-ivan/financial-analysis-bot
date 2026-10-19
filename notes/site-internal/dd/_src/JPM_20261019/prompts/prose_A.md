你是 stock-analyst v20 的**散文層（prose）agent**，標的 JPM（2026-10-19）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JPM_20261019/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：JPM　日期：2026-10-19　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1335B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（396B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（491B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1375B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（799B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（674B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（687B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1872B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3366B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2284B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1335           3965-5665      5 條（2–6 內）  
s3                  8000         396           5323-7604      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2665          8634-12335      5 條（2–6 內）  
s6                 11000         674          7228-10326      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         687           1969-2813      5 條（2–6 內）  
s10                 5000        1872           2190-3128      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2284           2000-2716      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3996B；至少需散文≈41.00KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45%
−45
−30
0%
0
0.45
0.93
1
01
1.5%
1.5
1.65
1.81
2
2%
2.26
2.39
2.4
2.5%
3%
3
3.2%
3.5%
3.8%
4
4%
4.5%
4.55
5
5%
5.2%
5.2
5.57
5.75
5.85
5.9%
6%
6
6.58
7%
7
7.1%
7.7%
7.7
7.9
8%
8
09
9
9%
9.2%
9.5
9.8%
10
10%
10.5%
10.53
11.4
11.5
11.5%
12%
12
12.5
12.5%
12.9%
13
13.3
13.32
13.9%
14
14%
14.1
14.11
14.5
15%
15.3%
15.7%
16
16.2%
16.6
17
17%
18
18%
18.5
19
20
20%
20.02
20.5
21.5
23
24
24.07
24.5
25
25.5
26%
26
26.6
26.8
27
27.43
28.7
28.8
30%
30
30.4
31
32.2
33.3
35%
35.8
36%
40%
40
42
44
45%
46%
49%
49
50
52
54%
56
57
65%
65
69
70
82
83
90
92
100
100%
150%
153
160
180
200
212
227
228.77
250
255
272.95
275
280
293
300
339.72
340
366.5
501.72
509
510
2008
2020
2025
2026
2027
2028
20261019
1,040
1,062
1,070
1,075
1,086
1,140
1,160
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
{"meta":{"ticker":"JPM","date":"2026-10-19","schema":"v15.0","contract":"v19","company_name":"JPMorgan Chase & Co."},"oneliner":"存款利差、卡片、投行與資產管理同時處在週期高點，ROTCE 20% 高於管理層自訂的跨循環 17%；現價約 14 倍前瞻盈餘，等於把高點報酬當成常態，要等價格或信用數據給出空間再動","thesis":{"H":[{"id":"H1","text":"2027 年不含市場 NII 約 1,070 億美元，增量主要來自放款與存款成長，而不是利率","2y":"2027 年度不含市場 NII 不低於 1,040 億","5y":null,"10y":null,"threshold":"不低於 1,040 億美元（中心情境 1,070 億下修 3% 以內）","source":"季報與法說的 NII 指引","drift_rule":"季度不含市場 NII 年化值連 2 季低於中心情境 5% 為削弱，連 3 季低 10% 為反轉"},{"id":"H2","text":"跨信用循環 ROTCE 守住 17%","2y":null,"5y":"含信用正常化年度在內，四季滾動 ROTCE 不低於 15%","10y":null,"threshold":"四季滾動 ROTCE 不低於 15%","source":"季報新聞稿 ROTCE","drift_rule":"連 4 季低於 17% 達 5% 以上（低於 16.2%）為削弱，連 6 季低 10% 以上（低於 15.3%）為反轉"},{"id":"H3","text":"消費存款引擎持續：零售存款市占維持第一，並朝 15% 推進","2y":null,"5y":"分行擴張後消費存款持續正成長","10y":null,"threshold":"消費與社區銀行平均存款年增不低於 0%，單季淨新增支票帳戶不低於 40 萬","source":"季報、法說、FDIC 存款資料","drift_rule":"存款年增率連 4 季低於 0% 或支票帳戶淨增連 4 季低於 40 萬為削弱，連 6 季為反轉"}],"R":[{"id":"R1","text":"資本市場收入回落：投行在九月下旬放緩，固收年減 4%，前季承認有提前認列","h_ref":"H2","clock":"⚡","threshold":"市場加投行營收連 2 季年減超過 10%","evidence_refs":["capital_markets_pricing#1"]},{"id":"R2","text":"信用循環轉折：產業處於循環後段，信用條件變鬆，實質利率偏高","h_ref":"H2","clock":"🔥","threshold":"卡片淨沖銷率連 2 季高於 3.8%","evidence_refs":["financial_capital_credit_cycle#4"]},{"id":"R3","text":"Basel III 與 G-SIB 規則提高 JPM 資本要求，吃掉多餘資本與回購空間","h_ref":"H2","clock":"🐢","threshold":"最終規則下所需標準法 CET1 高於 12.5%","evidence_refs":["regulatory_antitrust#1","financial_regulatory_capital_rules#2"]},{"id":"R4","text":"生息穩定幣、代幣化存款與 AI 代理繞過中介，蠶食低成本存款與支付","h_ref":"H3","clock":"🐢","threshold":"消費與社區銀行平均存款連 2 季年減","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#2"]},{"id":"R5","text":"費用連續上調，快過營收，營運槓桿轉負","h_ref":"H2","clock":"🔥","threshold":"2027 年調整後費用指引高於 1,160 億美元","evidence_refs":["capital_markets_pricing#2"]},{"id":"R6","text":"第三方系統、雲端集中與地緣政治（中東、中國）造成營運中斷或資產損失","h_ref":"H2","clock":"🐢","threshold":"單一事件損失超過 10 億美元，或核心支付中斷超過 24 小時","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]}],"single_thing":{"description":"美國轉入衰退，卡片淨沖銷率年化突破 4.5%（目前指引約 3.2%）","why_fatal":"卡片是盈餘對景氣最敏感的一塊。沖銷上升會和準備提列、資本市場收入回落同時出現，EPS 走悲觀路徑，倍數也一起壓縮。卡片放款餘額事實表未涵蓋，無法精算每個百分點的金額","if_happens":"EPS 走悲觀路徑（2028 年約 20.5 美元），本益比壓到約 9.5 倍，股價約 200 美元以下","how_monitor":"每季財報的卡片淨沖銷率與拖欠率、管理層的沖銷率指引、失業率","probability":"20%"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":13.32,"peg_fy2":2.26,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":20.02,"FY2026E":24.07,"FY2027E":25.5,"FY2028E":null},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；2028 年共識事實表未涵蓋（只有兩年共識）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JPM_20261019/scenario.json","archetype":{"primary":"金融","secondary":null,"confidence":"高","fingerprint":"全能銀行：低成本消費存款加卡片利差，再加投行、市場與資產管理費收"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性，將會反轉。第三季法說管理層說全業務同時創紀錄不是歷史常態，Dimon 說信用條款變鬆（PIK、弱契約），財務長說實質利率長期偏高會傷害消費者信用","bargaining":{"up":"資金來源端：消費存款 beta 低於模型，議價力弱；批發存款競爭激烈，財務長說邊際上更競爭","down":"借款人端：大型企業與 AI 基建融資需求旺，同業放寬條件，JPM 表示正在收緊","geo":"全球業務。Dimon 股東信點名烏克蘭、中東衝突與對中國緊張，公司無法置身事外"},"profit_pool_dir":"利潤池往資本市場、資產管理與私人信貸擴散，AI 基建融資有一部分由非銀行資本承接","tam_table":{"expanded":false,"reason":"銀行成長看放款、存款、資產管理規模與費收市占，不是市場滲透率；這些項目已寫在成長題的分部表"}},"moat":{"mechanism":"全美最大的零售存款規模加上分行密度與信任，形成低成本資金；在此基礎上用卡片、投行、支付與資產管理交叉變現的全能銀行網絡","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"存款面在擴大：零售存款市占第一，單季淨新增支票帳戶約 65 萬，消費存款年增 4%。投行面略降：錢包份額從第一季 9.8% 降到年初至今 9.2%，仍排第一。兩邊相抵，判為持平","peer_na_reason":"同業 ROTCE 事實表未涵蓋。同業表只有 FCF 利潤率，銀行的 FCF 受放款與交易資產變動主導（JPM 為負值），不能拿來比護城河","threats":[{"level":"🔴","text":"生息穩定幣與代幣化存款可能繞過銀行中介，直接攻擊最便宜的消費存款與支付費收。JPM 以 Kinexys 與存款代幣自建對應產品，但多數專案沒有確定上線日","p":30,"evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"個人 AI 代理替客戶比價搬錢，會加速收益型資金流出。管理層目前封鎖外部代理直接轉帳，並以主要往來銀行策略應對","p":20,"evidence_refs":["substitute_technology#3"]},{"level":"🟡","text":"Stripe、PayPal、Block、Chime 等金融科技點對點爭奪支付與年輕客群（前季法說 Dimon 點名）","p":25,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"存款、卡片、轉帳、受保存款與分行屬必需服務（第三季法說 Dimon）。使用者、決策者、付款者三個角色都成立，消費支出年增 10%"},{"item":"決策層級","level":"🟡","text":"主要往來帳戶綁薪轉與帳單，轉換成本高。但收益型資金本來就會流動，批發存款更競爭，AI 代理可能在帳戶層壓低搬錢摩擦"},{"item":"價值鏈分配","level":"🟡","text":"JPM 靠閒置存款的利差賺錢。Dimon 承認如果這條路被擋，會改收訂閱費，也認為 AI 效益最後會讓給客戶，利差的分配有被重劃的可能"},{"item":"社會容忍度","level":"🟡","text":"規模本身招來資本懲罰：G-SIB 附加費草案預計由 4.5% 升到 5.2%，約多需 200 億美元資本；卡片利率與費用也長期受政治檢視"}],"roiic":17,"reinvest_rate":0.45,"endo_ceiling":7.7,"formula_note":"增量報酬取管理層資本部署目標 17%（前季與本季法說 Dimon）。保留率取本季（股利每季 1.65 美元×約 26.6 億股，約 44 億，加回購 10 億，占淨利 153 億約 35%，保留 65%）與過去約 70 億回購節奏（保留約 26%）的中間值約 45%。內生成長上限＝17%×0.45≈7.7%"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"FCF 利潤率","JPM":-83.39,"BAC":73.37,"WFC":22.09,"C":-26.88,"GS":-62.71,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"BAC","fcf_margin":73.37,"strategy_note":"存款與市場業務結構最接近的對手。前季法說財務長指出 G-SIB 短期批發融資新算法對 JPM 和美國銀行負擔最重","period":"TTM ending 2026-06-30（4季加總）"},{"name":"WFC","fcf_margin":22.09,"strategy_note":"消費存款與卡片的直接競爭者；同業報酬率事實表未涵蓋，無法量化差距","period":"TTM ending 2026-06-30（4季加總）"},{"name":"C","fcf_margin":-26.88,"strategy_note":"跨國企業支付與財資服務的主要對手；同業數據事實表未涵蓋","period":"TTM ending 2026-06-30（4季加總）"},{"name":"GS","fcf_margin":-62.71,"strategy_note":"投行與權益交易主要對手，前季法說 Dimon 點名為競爭者；JPM 全球投行費用份額第一，本季權益交易年增 49%","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（放款、存款、資產管理規模），利率次之，費收看週期；淨回購暫降","runway_years":"零售存款市占朝 15% 推進，目前市占事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬 17%×保留率約 45%≈7.7%；共識 2025 到 2027 年化 12.9% 超出部分歸因於週期性資本市場收入","segments":[{"item":"消費與社區銀行","value":"第三季營收 212 億美元、年增 9%，淨利 57 億；卡片與汽車營收年增 15% 至 83 億"},{"item":"企業與投資銀行","value":"營收 227 億、年增 14%，淨利 82 億；投行費用年增 14%，權益交易年增 49%，固收年減 4%，支付營收年增 14% 至 56 億"},{"item":"資產與財富管理","value":"營收 69 億、年增 14%，淨利 18 億，稅前利益率 36%；長期淨流入 510 億，管理資產 5.2 兆"},{"item":"Corporate","value":"營收約 0.93 億，淨損 4.55 億，含 6.58 億證券損失"}],"decay_signals":[{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"2026 共識 EPS 年增約 20%，共識營收比 2025 年度營收高約 14%，差距超過 5pp；兩者營收口徑可能不同，視為弱訊號"},{"item":"毛利率連 2 季下滑","lit":false,"note":"銀行不適用；改看效率比約 54%"},{"item":"核心市占縮減","lit":false,"note":"投行份額略降但仍第一，零售存款市占第一"},{"item":"產業估值倍數系統性下移","lit":false,"note":"P/S 位於年度端點 92 分位，方向相反"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐；股利、回購節奏與資本部署已寫在判斷句，現金去向四分事實表未涵蓋"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表沒有近期具規模併購資料","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"前瞻盈餘殖利率約 7.1%（24.07÷339.72）；10 年期公債殖利率事實表未涵蓋，無法比對門檻","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"股權報酬費用與歷年股數事實表未涵蓋","grade":"不過"}]},"valuation":{"basis":"本益比加上 P/TBV 對 ROTCE 的合理倍數","tier":"美國大型全能銀行","peers":{"expanded":false,"reason":"同業 P/E、P/TBV、ROTCE 事實表未涵蓋；同業表只有對銀行無意義的 FCF 利潤率"},"fwd_pe":14.11,"peg":2.39,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 14.1 倍÷2026 到 2027 共識 EPS 成長 5.9%，PEG 約 2.4；以 17% 跨循環 ROTCE 換算正常化本益比約 16.6 倍；P/TBV 約 3 倍，高於合理約 2.4 倍；P/S 位於 4 個年度端點 92 分位（不是五年分位，五年分位事實表未涵蓋）。四項都指向偏貴","upside_short_pct":7.9,"upside_mid_pct":18.5},"trap_analysis":{"verdict":"🟡","label":"週期高點盈餘被當成常態"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"產業研究把 2026 年描述為信用循環後段，信用卡拖欠在 6 月上升；第三季法說 Dimon 說信用條款變鬆，財務長說實質利率長期偏高會帶來失業上升與消費信用轉弱","assumption":"基準情境假設失業率溫和、卡片沖銷率維持約 3.2%","consequence":"衰退加資本市場收入回落時，EPS 可能跌到 20 美元左右、本益比壓到約 9 倍，股價約 180 至 200 美元，五年後虧損接近一半","ruling":"採納。悲觀情境機率給 30%，並把卡片淨沖銷率定為唯一致命數字","watch":"卡片淨沖銷率；批發準備提列的原因是否從新業務轉為降評","evidence_refs":["financial_capital_credit_cycle#4"],"fact_refs":["f_kpi5_provision_for_credit_los","f_kpi6_rotce"]},{"view":"論點失敗","evidence":"10-K 風險因子、財務長與 Dimon 都點名生息穩定幣與代幣化可以繞過銀行中介，衝擊支付與存款","assumption":"低成本消費存款不會被大規模搬走","consequence":"存款成本上升，NII 結構性下修，利差模式被迫改成訂閱收費","ruling":"部分採納。這是十年尺度的風險，近兩年有封鎖外部代理與自建存款代幣緩衝，不改變近期情境，列入長期威脅與觸發器","watch":"消費與社區銀行存款年增率；生息穩定幣相關立法","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"回購從約 70 億美元節奏降到 10 億，多餘資本改投有機成長，目標報酬 17%；資本新規草案可能多需約 200 億；費用年增 12%，快過營收","assumption":"保留下來的資本能賺到 17% 以上，且資本規則不會再吃掉多餘資本","consequence":"業務即使續強，ROTCE 也會從 20% 被稀釋往 17% 走，每股盈餘成長慢於盈餘總額，淨回購殖利率下降","ruling":"採納。基準情境淨回購殖利率只給 1.5%，ROTCE 向 17% 收斂","watch":"季度回購金額、CET1 走勢、四季滾動 ROTCE","evidence_refs":["regulatory_antitrust#1","financial_regulatory_capital_rules#2","capital_markets_pricing#2"],"fact_refs":["f_kpi7_cet1_ratio_standardized","f_kpi3_noninterest_expense"]},{"view":"價格已反映太多","evidence":"前瞻本益比 14.1 倍，P/S 位於 4 個年度端點的 92 分位，P/TBV 約 3 倍；第三季 EPS 不及共識後，股價盤前跌 3% 隨即收復","assumption":"市場把 20% ROTCE 當成常態","consequence":"報酬回到 17% 時合理 P/TBV 約 2.4 倍，倍數下修約兩成","ruling":"採納。基準情境終端本益比用 12.5 倍，低於現值","watch":"前瞻本益比與四季滾動 ROTCE","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_pe_current","f_ps_percentile","f_consensus_eps_fy1"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 339.72","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=339.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"財報不及預期與指引上調並存","cause":null,"side_a":"第三季 EPS 5.57 美元，低於共識約 5.85；排除證券損失後 5.75，仍低約 3%","side_b":"全年 NII 指引上調到約 1,062 億，2027 年不含市場 NII 中心情境約 1,070 億","ruling":"可調和。落差來自證券損失與費用年增 12%，不是利差業務轉弱；費用快於營收是要追的訊號，列入費用風險","evidence_level":"一手財報加二手共識","settle_metric":"第四季費用約 275 億、不含市場 NII 約 255 億是否達成","if_then":["若第四季費用超過 280 億且不含市場 NII 低於 250 億，費用風險升為減碼理由","若兩者都達標，本季落差只當一次性，結論不變"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"利率方向","cause":null,"side_a":"有分析認為聯準會降息快於預期會壓低 NII","side_b":"財務長在第三季法說說遠期曲線含 12 月一次、明年上半年兩次升息，公司仍屬資產敏感","ruling":"兩邊方向相反，但對應不同時點。近一年升息情境占優；降息壓 NII 的路徑併入衰退的悲觀情境，不單獨作為減碼理由","evidence_level":"一手法說對二手分析","settle_metric":"聯準會實際利率路徑與季度不含市場 NII","if_then":["若聯準會轉向降息且季度不含市場 NII 年減，悲觀情境機率由 30% 上調到 40%","若升息落地且存款成本沒有明顯上升，情境機率不變"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"多餘資本與新資本規則","cause":null,"side_a":"Dimon 說約有 300 億美元多餘資本，回購排最後，優先投入有機成長","side_b":"公司自估 Basel III 草案會讓所需 CET1 增加約 4% 到 6%，兩案合計約多需 200 億；監管機關則估計大型銀行要求下降約 5%","ruling":"可調和。300 億足以吸收 200 億，但吸收後可回購空間大幅縮小。年底最終規則公布前無法裁決","evidence_level":"一手 10-Q 與法說","settle_metric":"最終規則下 JPM 所需標準法 CET1 比率","if_then":["若最終規則讓所需 CET1 超過 12.5%，淨回購殖利率假設降到 0 並重算情境","若最終規則讓所需 CET1 低於 11.5%，淨回購殖利率假設上調到 3%"],"evidence_refs":["regulatory_antitrust#1","financial_regulatory_capital_rules#2"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"現在就買的最強論證：ROTCE 20%，前瞻盈餘殖利率約 7%，2027 年 NII 再增 50 億，單季淨新增支票帳戶約 65 萬，存款引擎還在加速","side_b":"管理層自己說全業務同時創紀錄不是常態、跨循環目標 17%；正常化本益比約 16.6 倍，P/TBV 約 3 倍高於合理的約 2.4 倍","ruling":"選觀望。買方論證全部建立在 ROTCE 長期守住 20%，和管理層自己的跨循環目標方向相反。依據是第三季法說的 17% 目標與信用條件變鬆的描述","evidence_level":"一手法說","settle_metric":"信用正常化後四季滾動 ROTCE 是否仍不低於 18%","if_then":["若股價跌到 293 美元以下且卡片淨沖銷率不高於 3.5%，重跑判斷，通過後小部位首倉","若四季滾動 ROTCE 跌破 15%，價格到位也不進場"],"evidence_refs":[]},{"axis":"前季承諾兌現","cause":null,"side_a":"七月法說：全年費用約 1,075 億，卡片沖銷約 3.2%，消費存款低個位數成長，Smart Cash 年內推出","side_b":"十月：費用指引再升到約 1,086 億（二手報導），沖銷率維持 3.2%，消費與社區銀行存款年增 4%，Smart Cash 已上線試點","ruling":"大致兌現，唯一走偏的是費用連兩季上調。管理層歸因於業務量相關費用，目前未證實，持續監測：若 2027 年預算定案後費用超過共識 1,140 億 2% 以上，這個歸因就不成立","evidence_level":"一手法說加二手指引","settle_metric":"2027 年調整後費用指引","if_then":["若 2027 年費用指引超過 1,160 億，基準情境 EPS 下修並停止加碼","若費用指引落在 1,140 億以內，費用風險降級"],"evidence_refs":["capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"2027 年不含市場 NII 中心情境能否守住","type":"假設驗證","maps_to":"H1","metric":"季度不含市場 NII","threshold":"第四季不低於 250 億美元（指引約 255 億）","action":"低於門檻且 2027 年中心情境下修超過 3%：論點削弱，不加碼","source_freq":"季報與法說，每季","date":"2027-01","evidence_refs":["supply_demand_durability#2"]},{"n":2,"text":"消費信用轉弱","type":"風險","maps_to":"R2","metric":"卡片淨沖銷率","threshold":"連 2 季高於 3.8%（指引約 3.2%）","action":"減碼到觀察倉，悲觀情境機率上調到 40%","source_freq":"季報，每季","date":null,"evidence_refs":["financial_capital_credit_cycle#4"]},{"n":3,"text":"衰退讓卡片沖銷失控","type":"Single Thing","maps_to":"single_thing","metric":"卡片淨沖銷率（年化）","threshold":"高於 4.5%","action":"清倉觀察倉，估值改用悲觀情境","source_freq":"季報，每季","date":null,"evidence_refs":["financial_capital_credit_cycle#4"]},{"n":4,"text":"Basel III 與 G-SIB 最終規則","type":"風險","maps_to":"R3","metric":"最終規則下所需標準法 CET1","threshold":"高於 12.5%（現行 11.5%）","action":"淨回購殖利率假設降到 0，重算情境","source_freq":"監管公告與 10-Q","date":"2026-12","evidence_refs":["regulatory_antitrust#1","financial_regulatory_capital_rules#2"]},{"n":5,"text":"存款被穩定幣或 AI 代理搬走","type":"風險","maps_to":"R4","metric":"消費與社區銀行平均存款年增率","threshold":"連 2 季低於 0%","action":"護城河方向改判下降，重跑判斷","source_freq":"季報，每季","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#2"]},{"n":6,"text":"費用失控","type":"風險","maps_to":"R5","metric":"2027 年調整後費用指引","threshold":"高於 1,160 億美元（共識約 1,140 億）","action":"停止加碼，基準情境 EPS 下修","source_freq":"一月法說","date":"2027-01","evidence_refs":["capital_markets_pricing#2"]},{"n":7,"text":"營運、第三方系統或地緣事件","type":"風險","maps_to":"R6","metric":"單一營運或資安事件損失","threshold":"損失超過 10 億美元，或核心支付中斷超過 24 小時","action":"減碼並重跑判斷","source_freq":"8-K 與新聞，事件驅動","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":8,"text":"價格與信用同時給出空間","type":"估值rearm","maps_to":"rearm_trigger","metric":"股價與卡片淨沖銷率","threshold":"股價不高於 293 美元，且卡片淨沖銷率不高於 3.5%","action":"重跑判斷，通過後小部位首倉","source_freq":"日線收盤與季報","date":null,"evidence_refs":[]},{"n":9,"text":"第四季財報複審","type":"複審日期","maps_to":null,"metric":"2027 年 NII 與費用指引","threshold":"指引公布","action":"重跑判斷","source_freq":"一月法說","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"卡片淨沖銷率（年化）","bear_threshold":"高於 4.5%","window":"單季","source":"JPM 季報新聞稿","last_status":"ok"},{"metric":"四季滾動 ROTCE","bear_threshold":"低於 15%","window":"連 2 季","source":"JPM 季報新聞稿","last_status":"ok"},{"metric":"標準法 CET1 比率","bear_threshold":"低於 12.5%（要求 11.5% 加 1pp 緩衝）","window":"單季","source":"JPM 季報新聞稿與 10-Q","last_status":"ok"},{"metric":"消費與社區銀行平均存款年增率","bear_threshold":"低於 0%","window":"連 2 季","source":"JPM 季報與法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=10.53, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價不高於 293 美元（約 2027 年共識 EPS 11.5 倍），且卡片淨沖銷率不高於 3.5%，兩條同時成立才重跑判斷","exec_line":"目前不進場。觸價且信用數據過關後重跑判斷，首倉小部位；信用或資本規則觸發時停止加碼"},"reasoning":{"industry":"第三季法說（2026-10-13，財務長 Barnum）的分部數字：消費與社區銀行營收 212 億美元，淨利 57 億；企業與投資銀行營收 227 億，淨利 82 億；資產與財富管理營收 69 億，淨利 18 億。法說的營收 509 億是管理口徑，新聞稿報告口徑為 501.72 億，兩者口徑不同。最新一季效率比約 54%（費用 272.95 億÷淨收入 501.72 億），撥備前利潤約 228.77 億，ROTCE 20%，CET1 13.9%。本季含 6.58 億美元證券損失。供需持久性：週期性，將會反轉。管理層自己說每個業務同時創紀錄並非歷史常態，信用條件已經變鬆，升息循環也重啟。產業態勢屬雙向拉鋸。競爭面，穩定幣、代幣化與個人 AI 代理被 10-K 和管理層點名為新威脅。結構面，2026 年要新開 160 家以上分行，目標零售存款市占 15%，淨新增支票帳戶單季約 65 萬。法規面，Basel III 與 G-SIB 草案可能讓 JPM 多需約 200 億美元資本，監管機關卻估計大型銀行整體要求下降，兩邊方向相反。單點依賴方面沒有客戶集中問題，護城河證據是 FDIC 零售存款市占第一，全球投行費用份額也是第一。","moat":"機制：全美零售存款市占第一（FDIC），分行密度加上數十年累積的信任，形成低成本、低 beta 的消費存款，再用卡片、投行與資產管理交叉變現。執行面：第三季全業務年增，資產管理長期淨流入 510 億美元，淨新增支票帳戶約 65 萬，執行評 9。定價面：存款 beta 低於模型，消費存款年增 4%，議價力強；但批發存款更競爭，穩定幣與個人 AI 代理正在壓低搬錢門檻，定價評 8，已反映一項生態型威脅。同業 ROTCE 對照事實表未涵蓋，表中的 FCF 利潤率對銀行沒有意義，所以無法證明報酬率差距在擴大，評級停在 B。","growth":"成長組成：量（平均放款年增 10%、平均存款年增 8%）加利率（2027 年不含市場 NII 約 50 億增量中約四分之一來自殖利率曲線）加費收（資產管理、投行），回購貢獻暫時下降。共識 EPS 從 2025 年 20.02 到 2027 年 25.5，兩年年化約 12.9%；但 2026 到 2027 只有約 5.9%。內生上限約 7.7%，超出的部分歸因於 2026 年週期性資本市場收入帶來的利潤率擴張（前季法說：上半年資本市場營收超出預期 65 億美元），這部分不可外推。第三年共識事實表未涵蓋。","governance":"資本順序是股利、有機成長、最後才回購（第三季法說 Dimon）。前季已把股利調到每季 1.65 美元。CET1 從約 15.7% 降到 13.9%，期間內部部署與回購並行。風險在於把資本留在大約 3 倍帳面價值的位置，投入週期高點的放款，目標報酬 17% 低於目前的 20%。","valuation":"前瞻本益比約 14.1 倍（339.72÷24.07），2027 年約 13.3 倍。以 17% 跨循環 ROTCE 換算，正常化 EPS 約 20.5（24.07×17/20），正常化本益比約 16.6 倍。P/TBV 約 3 倍（前季分析師提問口徑，精確值事實表未涵蓋）；以 ROTCE 17%、成長 5%、資金成本 10% 推算，合理 P/TBV 約 2.4 倍。賣方目標價共識約 366.5 美元（13 位），Benzinga 16 位平均約 340，兩邊對本次判斷一個略偏支持、一個中性。","premortem":"管理層在第三季法說說全業務同時創紀錄不典型，信用條件已經變鬆，前季也承認投行有提前認列。最新一季提列 27.43 億美元，批發準備增加來自新業務而非降評，信用目前還穩。依據見反證紀錄的論點失敗與價格已反映太多兩條。26 週漲約 10.5%，RSI 約 52，動能沒有過熱。"},"plain":{"six":{"how_it_makes_money":"賺的是存款戶與借款人之間的利差（2026 年 NII 指引約 1,062 億美元，約占共識營收一半），加上企業與投資人的服務費。錢卡在低成本消費存款這個節點。產業處在週期過熱段","moat":"護城河方向持平。低成本存款規模與全能銀行交叉銷售仍然領先，但投行費用份額從第一季的 9.8% 降到年初至今 9.2%，不能判為擴大","growth":"後五年跑道中等。放款年增約一成、存款年增 8%，主要來自週期與分行擴張；零售存款市占已是第一，正朝 15% 目標推進，沒有可量化的第二條成長曲線","capital":"資本配置紀律好：股價愈高回購愈少，本季回購約 10 億美元（過去節奏約 70 億），約 300 億多餘資本轉投有機成長。三項計分的量化輸入事實表大多未涵蓋","valuation":"現價要求 ROTCE 長期守在 20% 左右、盈餘每年再長 6% 以上才划算。管理層自己說目前環境不典型，跨循環目標是 17%，我不相信高點報酬能當常態，結論是偏貴","how_wrong":"最可能看錯的地方是把週期高點當常態：信用循環轉折與資本市場收入回落同時發生"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價不高於 293 美元，且卡片淨沖銷率不高於 3.5%","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"金融","price_at_dd":339.72,"week26_return_pct":10.53,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"2026 年 EPS 含週期高點的市場與投行收入，ROTCE 20% 高於管理層跨循環目標 17%；用正常化 EPS 約 20.5 計算，本益比是 16.6 倍不是 14.1 倍，便宜的說法不成立"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"Basel III 與 G-SIB 最終規則預計年底定案","impact":"高","watch":"JPM 所需 CET1 比率與多餘資本"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報，細化 2027 年 NII 與費用指引","impact":"高","watch":"不含市場 NII 中心情境、費用指引、卡片沖銷率"},{"date":"2026-12","date_precision":"month","type":"macro","event":"聯準會 12 月利率決策（遠期曲線含一次升息）","impact":"中","watch":"存款成本與存款移轉"},{"date":"2027-09","date_precision":"quarter","type":"regulatory","event":"壓力資本緩衝 2.5% 到期，以修訂後壓力測試模型重算","impact":"中","watch":"新的壓力資本緩衝數值"}],"_projected_from":"v19"}
```
