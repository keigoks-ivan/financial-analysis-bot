你是 stock-analyst v20 的**散文層（prose）agent**，標的 AAPL（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：AAPL　日期：2026-11-08　archetype：None　前份裁決：2026-07-31　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1857B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（501B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1130B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1399B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1075B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（532B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（813B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2200B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3574B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2760B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1857           3600-5143      5 條（2–6 內）  
s3                  8000         501           5249-7499      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3604          7977-11396      5 條（2–6 內）  
s6                 11000         532          7328-10468      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         813           1881-2687      5 條（2–6 內）  
s10                 5000        2200           1960-2800      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2760           2000-2240      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4898B；至少需散文≈40.10KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−57
−50%
−50
−49%
−45%
−39%
−36%
−35%
−35
−6.4%
−2.8
0%
0.04%
0.05
0.10
0.2
0.27
0.28%
0.31
0.5
0.7
0.75
0.8%
0.88
01
1
1.03
1.2
1.25
1.4%
1.7
1.8%
1.8
1.9%
1.93
2%
02
2
2.1
2.8%
2.9%
3
3%
3.35
3.75
4.0%
4
4.2%
5
5%
05
5.2%
5.4%
5.9
06
6
6%
7
07
7%
7.3%
7.5%
7.7%
7.95%
8
08
8%
8.5%
8.7%
8.7
8.8
8.9
8.98
9.0
9%
9
9.04
9.3
9.4%
9.5%
9.5
9.6
9.6%
9.67
9.8
10
10%
10.4
10.49
10.65
10.7%
11
11%
11.3
11.3%
11.4
11.5
11.55
11.7
11.8%
11.82
12
12%
12.7
12.9%
13%
13.1
13.6%
13.9
14
14.6%
15
15%
15.1%
15.7%
15.8%
16%
16.7%
16.9%
16.93
17
17%
17.3%
17.8%
18%
18
18.8%
18.9%
19.0%
19%
20
20%
20.1%
22
22%
24
24%
25
25%
26
27
27.6%
28
28%
28.4%
30%
30
31
31.1%
32
32.15
33.0%
33%
36
36.04
37.2%
38.13
39
40%
42
43.6%
44%
44.5%
45
45%
45.5%
46%
46.9%
47%
47.1%
47.9%
48%
48.1%
48.79%
49
50%
50.3%
52
60%
62
70
73%
75%
76%
83
90
100
100%
108
137.9
144
150%
174
180
191
192
194
200
208
208.88
210
218
229
240
250
$257
257
260
261
$261
280
309.21
315.73
327
330
331
333
342.37
347
363
375
377.6
378
400
458
479
503
512
544
548.3
567.2
570
575.83
581
800
829
944.8
2025
2026
2027
2028
20261108
1,144.77
1,321.8
1,360.6
1,370
1,470
2,336
2,406
2,480
4,776.9
4,788.3
5,267
5,690
5,692.7
5,693
6,000
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
{"meta":{"ticker":"AAPL","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Apple Inc."},"oneliner":"iPhone 與 Mac 在縮水的市場裡搶到份額，但現價要 36 倍 FY27 EPS，記憶體成本還在漲；好公司太貴，等約 257 美元且毛利率守住 45% 再談。","thesis":{"H":[{"id":"H1","text":"iPhone 與 Mac 在記憶體短缺時搶到份額，FY27 營收能靠單價與新機組合再成長兩位數。","2y":"FY27 營收年增至少 10%，2027 年第三季全球手機份額至少 20%","5y":null,"10y":null,"threshold":"FY27 營收至少 5,267 億美元；2027 年第三季份額至少 20%","source":"每季財報與 10-Q；Counterpoint、IDC 季度出貨","drift_rule":"TTM 營收偏離路徑連 2 季達 5% 算削弱，連 3 季達 10% 算反轉"},{"id":"H2","text":"漲價與產品組合補得回記憶體成本：毛利率會下滑，但毛利額繼續成長。","2y":"FY27 毛利額年增至少 3%，單季毛利率不連兩季低於 44%","5y":null,"10y":null,"threshold":"FY27 毛利額至少 2,406 億美元；公司毛利率至少 44%","source":"每季 8-K 營收與毛利率；法說對記憶體與結轉庫存的說明","drift_rule":"TTM 毛利額偏離路徑連 2 季達 5% 算削弱，連 3 季達 10% 算反轉"},{"id":"H3","text":"Services 撐過監管與授權壓力，FY28 回到雙位數成長並守住高毛利。","2y":null,"5y":"FY28～FY31 年增至少 10%，毛利率至少 75%","10y":null,"threshold":"FY28 Services 年增至少 10%，毛利率至少 75%","source":"每季 8-K；最高法院、歐盟執委會、Google 案進度","drift_rule":"自十二月季指引起算，連 4 季偏離 5% 算削弱，連 6 季偏離 10% 算反轉"},{"id":"H4","text":"AI 時代 iPhone 仍是個人脈絡的主要入口。","2y":null,"5y":null,"10y":"活躍裝置與付費帳戶持續創高，App Store 維持年增","threshold":"活躍裝置至少 25 億台且持續成長；付費訂閱至少 15 億","source":"每季法說揭露的活躍裝置、付費帳戶、App Store 說法","drift_rule":"跨 2 個年度未創高算削弱，跨 3 個年度算反轉"}],"R":[{"id":"R1","text":"記憶體高價延續，結轉庫存效益遞減，漲價補不回成本；2026-11-02 法說 Ternus 說十二月季之後採購價仍在上升。","h_ref":"H2","clock":"🔥","threshold":"公司毛利率連 2 季低於 44%，或毛利額連 2 季年減","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","supply_demand_durability#4"]},{"id":"R2","text":"Services 被監管與司法切割，受影響基礎為九月季 315.73 億美元的 Services 營收，App Store 占比未揭露；DOJ 屬民事訴訟，定案時間事實表未涵蓋。","h_ref":"H3","clock":"🔥","threshold":"Services 年增連 2 季低於 7%，或毛利率低於 73%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","channel_business_model_shift#1","major_events#2","lawsuit_class_action#1"]},{"id":"R3","text":"Agent 形態繞過 App 與 Safari 入口，或新型 AI 裝置成為新入口。2026-07-30 法說 Ternus 未正面回應 OpenAI 裝置與 SpaceX AI 手機。","h_ref":"H4","clock":"🐢","threshold":"App Store 連 2 季年減，或付費訂閱低於 15 億","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"id":"R4","text":"系統晶片單一供應、製造集中亞洲，地緣或貿易事件直接限制出貨與毛利。","h_ref":"H1","clock":"⚡","threshold":"營收指引連 2 季年增低於 5%，或新關稅使毛利率連 2 季低於 44%","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R5","text":"FY26 是換機高點，漲價後需求轉弱，對手以低價奪回份額。","h_ref":"H1","clock":"🔥","threshold":"iPhone 營收連 2 季年減，或第三季全球份額低於 20%","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#3"]},{"id":"R6","text":"CEO 交接與訴訟風險同時存在：2026-07-30 法說 Cook 宣布交棒，Ternus 2026-11-02 首次主持；Siri AI 與 Epic 合規的證券集體訴訟未有駁回裁定。","h_ref":"H4","clock":"🔥","threshold":"駁回聲請遭否且集體認證通過；或 CFO、COO 於 12 個月內異動","evidence_refs":["major_events#1","lawsuit_class_action#0"]}],"single_thing":{"description":"剔除關稅退款後，公司毛利額連續兩季年減。","why_fatal":"FY27 共識 EPS 9.5 在費用年增 12%、稅率 17%、平均股數約 144 億下，需要毛利額約 2,480 億美元，較 FY26 的 2,336 億多約 6%。毛利率每 1 個百分點約等於 0.27 美元 EPS，約占 FY27 共識 2.9%，是模型裡最大的單一敏感項。毛利額年減代表漲價沒有補回記憶體成本，EPS 成長與高倍數同時失去依據。","if_happens":"不建首倉，Bear 機率由 30% 上調到至少 40%，Base FY27 EPS 下修到 9.0 以下；已持有者減碼一半。","how_monitor":"每季 8-K 的營收乘毛利率，扣掉法說揭露的關稅退款；同時看法說對記憶體採購價與結轉庫存的說法。","probability":"約 25%（12～24 個月）。管理層已說記憶體續漲且結轉庫存效益遞減，但漲價剛開始反映，Android 缺料也有利於份額。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":32.15,"peg_fy2":3.35,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":8.98,"FY2027E":9.5,"FY2028E":10.65,"FY2029E":11.82},"fy_end_month":9,"eps_basis":"GAAP 稀釋 EPS；FY2026A 含關稅退款，九月季 0.05 美元；FY2027E 起為 Koyfin 共識 FY1～FY3"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AAPL_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"高毛利平台、低資本密度、持續回購"},"industry":{"clock_phase":"IV","sd_verdict_source":"依據 IDC 2026-08-26 預測：手機出貨年減 16.7%、平均售價年增 27.6%。供需屬週期性將反轉，Samsung 2026-07-31 稱短缺延續到 2028。","bargaining":{"up":"上游最強的是 DRAM 三家供應商與台積電。2026-07-30 法說 Cook 稱記憶體定價是百年一遇洪水，2026-11-02 法說 Ternus 稱前所未見，製造採購承諾由六月到九月增加 330 億美元。","down":"下游電信與經銷分散，間接通路約六成，定價權仍在 Apple 手上。","geo":"製造集中在中國大陸、印度、日本、南韓、台灣、越南；印度約占 iPhone 產量四分之一，大中華區 FY26 營收年增 28%。"},"profit_pool_dir":"短期利潤由手機品牌流向記憶體供應商；五年營業利益池占比事實表未涵蓋，不做降檔判斷。","tam_table":[{"item":"全球手機出貨 2026","value":"IDC 8 月預測年減 16.7%"},{"item":"手機平均售價 2026","value":"IDC 預測 581 美元，年增 27.6%"},{"item":"Apple 全球手機份額 2026Q3","value":"Counterpoint 22%，去年同期 18%"},{"item":"全球 PC 2026Q3","value":"IDC 年減 20.1%；Mac 份額 9.5%，去年同期 8.5%"},{"item":"營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"iOS 與自研晶片綁住超過 25 億台裝置，換機與服務都在自家平台結算；換邊要同時放棄資料、App 與跨裝置連動。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力穩定、定價權穩定。份額三項都上升，但 App Store 九月季與去年相近，十二月季 Services 指引降到 8%～9%，CFO 說漲價彈性現在判斷還太早。","peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，改以份額方向與 FCF 利潤率對照。","threats":[{"level":"🔴","text":"監管與司法切割 Services：歐盟 DMA、美國 DOJ 訴訟、外部連結裁決、Google 搜尋授權。","p":"40%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#2","lawsuit_class_action#1","channel_business_model_shift#1"]},{"level":"🔴","text":"AI agent 繞過 App 與 Safari 入口，分發租金鬆動。目前沒有收入受損證據，所以還不列為架構替代。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"對手可接近零利潤甚至虧損銷售；但本輪短缺中 Android 受傷更深，Apple 份額反而上升。","p":"20%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"系統晶片由台積電單一供應，製造集中亞洲，關稅與地緣事件會直接影響出貨。","p":"15%","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉率事實表未涵蓋，依淨再投資接近零推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多半是同一人；活躍裝置超過 25 億台，九月季升級人數與付費帳戶都創紀錄。"},{"item":"決策層級","level":"🟡","text":"替代要在整個生態系層級衡量，換機成本高；但最關鍵的代理變數是漲價後流失率，CFO 2026-11-02 說現在判斷彈性還太早。"},{"item":"價值鏈分配","level":"🟡","text":"DRAM 三家供應商正在多拿，剔關稅退款毛利率由六月季 48.1% 降到九月季 46.9%，十二月季指引中點 45.5%。若高價延續到 2028 應改判紅。"},{"item":"社會容忍度","level":"🔴","text":"App Store 抽成已碰到政治上限：歐盟罰款 5 億歐元並下令停止限制導流，美國外部連結裁決執行中，DOJ 訴訟進行中。"}],"roiic":"無法計算：FY24～FY26 淨利減 FCF 累計 −57 億美元，淨再投資接近零，分母不成立；投入資本事實表未涵蓋（financial_history.years，yfinance 年報）。","reinvest_rate":"約 7.5%（代理口徑：FY26 淨利減去 FCF 扣 SBC 後的金額，再除以淨利；資本支出與折舊事實表未涵蓋）","endo_ceiling":null,"formula_note":"增量報酬乘再投資率對 Apple 失效，分母接近零時結果沒有意義。成長來自定價、mix 與回購，不是新投入資本。採購承諾與 AI 算力若持續放大，再投資率會上升，需要重算。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","AAPL":48.79,"MSFT":67.66,"GOOGL":60.86,"AMZN":51.08,"SONY":33.03,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","AAPL":33.01,"MSFT":47.1,"GOOGL":33.32,"AMZN":12.89,"SONY":14.6,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","AAPL":28.41,"MSFT":17.31,"GOOGL":4.19,"AMZN":-6.38,"SONY":12.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","AAPL":9.56,"MSFT":10.52,"GOOGL":15.81,"AMZN":null,"SONY":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"MSFT","gm":67.66,"om":47.1,"fcf_margin":17.31,"rd_intensity":10.52,"strategy_note":"營益率 47.1% 高於 Apple，FCF 利潤率 17.3%，資本壓在 AI 基礎建設；消費端入口不是直接對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"GOOGL","gm":60.86,"om":33.32,"fcf_margin":4.19,"rd_intensity":15.81,"strategy_note":"同時是 Android 陣營與搜尋授權付款方，FCF 利潤率只剩 4.2%；對 Apple 既帶收入也帶依賴。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"AMZN","gm":51.08,"om":12.89,"fcf_margin":-6.38,"rd_intensity":null,"strategy_note":"營益率 12.9%、FCF 利潤率 −6.4%，資本投入雲端；與 Apple 重疊在內容與裝置，威脅低。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"SONY","gm":33.03,"om":14.6,"fcf_margin":12.4,"rd_intensity":null,"strategy_note":"毛利率 33.0%、營益率 14.6%，消費電子同業中定價力明顯低於 Apple。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"FY26 量價併進，回購貢獻約 2 個百分點；FY27 以單價與 mix 為主，量受供給限制。","runway_years":"不給年數：高階客群滲透率事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬乘再投資率對 Apple 失效，FY24～FY26 淨利減 FCF 累計 −57 億美元，淨再投資接近零；上界留空，保守當作共識 9.6% 已超出。","segments":[{"item":"iPhone 九月季","value":"575.83 億美元，年增 17%"},{"item":"Services 九月季","value":"315.73 億美元，年增 10%，毛利率 76%"},{"item":"Mac 九月季","value":"108 億美元，年增 24%"},{"item":"穿戴與家庭九月季","value":"83 億美元，年減 8%"},{"item":"iPad 九月季","value":"62 億美元，年減 10%"},{"item":"產品合計九月季","value":"829 億美元，年增 12%，毛利率 37.2%"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"接近成立：剔退款後連兩季季減，去年同季毛利率事實表未涵蓋"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"手機與 Mac 份額都上升"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"iPhone 9 月才漲價；Mac 出貨 IDC 年減 11.3%，但受供給限制"},{"item":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"note":"FY23～FY26 為 13.6% 對 7.7%，差 5.9 個百分點"},{"item":"FCF 對淨利低於 0.75 連 2 年","lit":false,"note":"FY26 為 1.03，FY25 為 0.88"},{"item":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"FY26 為 2.9%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"出貨量萎縮，但金額因單價上升而擴大"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"item":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"事實表未涵蓋"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"未發生"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，Q.ai 金額僅占市值約 0.04%，現金去向四分資料事實表也未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"FY26 唯一具規模的收購是 Q.ai，約 20 億美元，占市值約 0.04%，尚無已實現報酬可量。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"以現價計盈餘收益率約 2.8%（1÷36.04）；回購均價與 10 年期殖利率事實表未涵蓋，只要 10 年期高於 0.8% 就不過。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY26 SBC 137.9 億美元，占市值約 0.28%；FY26 平均稀釋股數較 FY25 減少約 2%。","grade":"過"}]},"valuation":{"basis":"FY27 共識前瞻本益比與 PEG","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋，事實表只有同業利潤率，無法做倍數對照。"},"fwd_pe":36.04,"peg":3.75,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"36.04 倍 FY27 共識 EPS，PEG 3.75（36.04 除以三年 CAGR 9.6），高於 2 倍的昂貴線；五年基準價約 375 美元，年化約 2%，低於 8%。五年分位事實表未涵蓋，四個年度端點分位 100 不當五年分位。結論為過高。","upside_short_pct":-2.8,"upside_mid_pct":1.2},"trap_analysis":{"verdict":"🟡","label":"高基期加成本上行，估值沒有留緩衝"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Samsung 預期短缺延續到 2028；Counterpoint 預期 2027 年手機再減 1.4%；2026-11-02 法說 Ternus 說記憶體採購價繼續上升、結轉庫存效益遞減；IDC 提示 2027 年庫存堆積風險。","assumption":"漲價補得回成本，需求不因單價上升而縮。","consequence":"五年虧 50% 最可能的故事：毛利額連續下滑，FY31 EPS 只有約 10 美元，市場當低成長硬體股給 18 倍，股價約 180 美元，虧約 47%。","ruling":"採納，列為 Bear 路徑。這與 Single Thing 指向同一件事，不另立事件。","watch":"每季毛利額年增率、製造採購承諾、存貨變化","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","supply_demand_durability#4"],"fact_refs":["f_kpi3_gaap","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"2025-05 Eddy Cue 稱 AI 可能約十年內取代 iPhone；10-K 自述技術變化快。2026-11-02 法說 Daryanani 問客戶關係是否會由裝置轉到 agent，Ternus 只答 iPhone 是個人中樞，並說 Siri 目前仍以請求為主。","assumption":"Agent 必須經過 iOS 才拿得到個人脈絡。","consequence":"入口租金鬆動，Services 與換機同時受傷。","ruling":"部分採納。風險真實但時間窗在 2028 之後，近兩年資料無法裁決，不當作現價的主要否決理由。","watch":"App Store 年增方向、每週造訪人數、付費訂閱數","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"view":"論點成功但股東經濟變差","evidence":"DMA 罰款 5 億歐元與停止令，第 6(4) 條若最終認定可罰至全球年淨銷售 10%，以 FY26 計約 479 億美元；DOJ 尋求衡平救濟；外部連結裁決執行中；Google 上訴若翻案可能禁止商業條件。十二月季指引列第三方授權為逆風，Siri AI 雲端成本進 Services 銷貨成本。","assumption":"Services 76% 毛利率可持續。","consequence":"裝置賣得再好，最肥的利潤仍會變薄。Services 占九月季毛利約 44%，抽成下修會直接打在倍數上。","ruling":"採納。社會容忍度判紅，Base 的 Services 成長只放 8%～10%。","watch":"Services 年增率與毛利率、最高法院裁決、DMA 最終認定","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","channel_business_model_shift#1","major_events#2","lawsuit_class_action#1"],"fact_refs":["f_kpi8_services"]},{"view":"價格已反映太多","evidence":"36.04 倍前瞻本益比、PEG 3.75；26 週上漲 16.9%；股價高於 52 週均線 16.9%。","assumption":"倍數維持 30 倍以上，且 FY27 營收年增約 19%。","consequence":"即使 EPS 達到共識，五年年化也只有個位數低段。","ruling":"採納，這是目前的主要約束。","watch":"FY27 共識前瞻本益比","fact_refs":["f_fwd_pe_latest","f_week26_return_pct","f_ma_w52"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 309.21 → 本次 342.37（+10.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=309.21","side_b":"本次 price_at_dd=342.37","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 309.21 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 309.21 美元：Bull 價 512、Bear 價 210，五年期望值 +19.0%，基準年化 4.2%，不對稱比 1.8","side_b":"本次情境、股價仍用 309.21 美元：Bull 價 544、Bear 價 208，五年期望值 +18.8%，基準年化 4.0%，不對稱比 1.93","ruling":"先換情境、股價不動：五年期望值少 0.2 個百分點，基準年化少 0.2 個百分點。不對稱比由 1.8 變為 1.93。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 309.21 美元：五年期望值 +18.8%，基準年化 4.0%，不對稱比 1.93","side_b":"本次情境、股價 342.37 美元：五年期望值 +7.3%，基準年化 1.9%，不對稱比 1.25","ruling":"再換股價、情境不動：起點價上漲 10.7%，五年期望值少 11.5 個百分點，基準年化少 2.1 個百分點，不對稱比由 1.93 降到 1.25。合計五年期望值比前份少 11.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與等待結論","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份股價 309.21 美元，FY27 前瞻本益比約 32 倍，估值偏貴，結論是等待。","side_b":"現價 342.37 美元，較前份高 10.7%，前瞻本益比 36.04 倍，估值改判過高，品質評級不變。","ruling":"採 B 側，等待結論不變。變動主要來自股價上漲，基本面沒有提供更高倍數的理由。","evidence_level":"高","settle_metric":"FY27 共識前瞻本益比","if_then":["若股價續漲而 FY27 共識未上修，不追","若股價跌到 27 倍附近且基本面無損，分批反買"],"evidence_refs":[]},{"axis":"品質判斷複核","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"前份：陷阱風險中等、護城河穩定、五年後跑道中等。","side_b":"本次三項不變。新證據兩邊都有：份額擴大、中國回升；另一邊剔退款毛利率兩季降約 260 個基點，Services 指引降到 8%～9%。","ruling":"三項維持。硬體端的好消息與 Services 端的壞消息方向相反，幅度還不足以改判。","evidence_level":"中","settle_metric":"手機份額、Services 年增率、毛利額年增率","if_then":["若 Services 連 2 季年增低於 7%，減碼一半","若份額續升且 Services 回到 10% 以上，仍不追，等估值條件"],"evidence_refs":[]},{"axis":"公司分類與週期位置","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份：品質複利成長，週期位置未填。","side_b":"本次相同。","ruling":"未變動。Apple 不按循環股處理，記憶體週期放在毛利情境中反映。","evidence_level":"高","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 25%、Bear 28%、最大回撤 −45%。","side_b":"本次 Bull 25%、Bear 30%、最大回撤範圍 −50%～−35%。","ruling":"內生上界算不出，保守當作共識已超出，Bear 機率提高到 30%；回撤改用範圍表達。","evidence_level":"中","settle_metric":"毛利額年增率","if_then":[],"evidence_refs":[]},{"axis":"重新進場門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE（FY27 共識）≤ 27x（約 $261）且剔關稅毛利率連 2 季 ≥ 46%——雙條件 AND，缺一不進場","side_b":"FY27 共識前瞻本益比 ≤ 27 倍（約 $257）且公司毛利率連 2 季 ≥ 45%，兩項同時成立才重跑研究","ruling":"進場價由 261 美元改 257 美元，因為 FY27 共識由約 9.67 降到 9.5。毛利率由 46% 改 45%，因為十二月季指引 45%～46% 已反映更高的記憶體成本，且多數關稅退款已收回。放寬毛利率的代價是可能太早進場，價格條件不放寬。主要約束是估值，毛利率只用來確認跌價不是論點失敗。","evidence_level":"中","settle_metric":"FY27 共識前瞻本益比、公司毛利率","if_then":["若兩項同時成立，重跑研究，通過後分批反買","若股價到位但毛利率低於 45%，不追"],"evidence_refs":[]},{"axis":"清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標","side_b":"毛利額連 2 季年減；毛利率連 2 季低於 44%；Services 連 2 季低於 7%；第三季手機份額低於 20%；FY27 共識 EPS 低於 9.0","ruling":"新增減碼與清倉指標，讓結論可以被數字否定。門檻取自本次情境：44% 與 9.0 是 Bear 路徑的邊界。","evidence_level":"中","settle_metric":"各季 8-K 與共識快照","if_then":["若毛利額連 2 季年減，減碼一半","若毛利額連 4 季年減且 FY28 共識 EPS 低於 9.5，清倉"],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"剔除關稅退款後，公司毛利額連續兩季年減。","ruling":"新設 Single Thing。選毛利額而不是毛利率，因為成本全額轉嫁時毛利率也會下滑，百分比會誇大傷害。","evidence_level":"中","settle_metric":"每季營收乘毛利率","if_then":["若發生，不建倉，已持有者減碼一半"],"evidence_refs":[]},{"axis":"共識上修是否真實","cause":null,"prior_field":null,"side_a":"資料顯示 FY1 共識近 3 個月上修 7.95%，由 8.8 升到 9.5。","side_b":"8 月的 8.8 較像 FY26 數字：10-17 的 FY26 共識為 9.04；前份進場價隱含 FY27 共識約 9.67（261 除以 27）。同口徑看 FY27 共識約下修 1.8%。","ruling":"採 B 側，把 7.95% 視為財年切換造成。性質：可調和，屬財年口徑差異。可能看錯的地方是前份隱含值與 Koyfin 來源不同，要有同財年歷史快照才能定案。","evidence_level":"中","settle_metric":"FY2027 共識 EPS 的同財年歷史快照","if_then":["若同財年資料證實 3 個月下修超過 3%，不追，Base EPS 再下修","若同財年資料證實上修至少 3%，仍不追，Base EPS 上調到共識"],"evidence_refs":[]},{"axis":"換機高峰或結構升級","cause":null,"prior_field":null,"side_a":"Wedbush 認為週期仍有動能；升級人數創紀錄；2026-07-30 法說 Cook 說資料看不出拉貨。","side_b":"另有報導認為創紀錄季度可能是週期高點；Counterpoint 預期 2027 年手機再減；iPhone 18 標準版未在九月推出，營收認列時點不易比較。","ruling":"不可裁決至 2027 年九月季財報。現有資料涵蓋不到高基期的比較窗，不能說風險已解。本次結論不靠裁決此事，兩種情況下現價都偏貴。","evidence_level":"低","settle_metric":"iPhone 營收對 FY26 高基期的年增率","if_then":["若 iPhone 營收連 2 季年減，減碼一半","若高基期下仍年增 10% 以上，仍不追，上調 Bull 機率"],"evidence_refs":["supply_demand_durability#3","supply_demand_durability#2"]},{"axis":"毛利率與毛利額","cause":null,"prior_field":null,"side_a":"毛利率下滑會被解讀為成本轉嫁失敗。","side_b":"成本全額轉嫁時毛利額不變，毛利率仍會因營收變大而下滑。","ruling":"採 B 側，致命指標用毛利額，毛利率作輔助。性質：可調和。","evidence_level":"高","settle_metric":"毛利額年增率","if_then":["若毛利率下滑但毛利額年增至少 5%，不減碼","若毛利額年減，減碼一半"],"evidence_refs":[]},{"axis":"營收共識的財年標籤","cause":null,"prior_field":null,"side_a":"事實表把 4,776.9 億美元標為與 FY1 EPS 同一財年。","side_b":"FY26 實績 4,788.3 億美元，兩者幾乎相等；十二月季指引年增 7%～10%，這筆不可能是 FY27。5,692.7 億美元才像 FY27，等於年增 18.9%。","ruling":"採 B 側，前瞻 EV/S 10.49 倍的分母很可能晚一年，不引用。本次採 EPS 路徑，不受影響。性質：可調和，屬資料標籤問題。","evidence_level":"中","settle_metric":"營收預估對應的財年","if_then":["若 FY27 共識確為 5,693 億美元，十二月季後其餘三季需年增約兩成以上，低於此節奏就不追"],"evidence_refs":[]},{"axis":"淨負債口徑","cause":null,"prior_field":null,"side_a":"事實表淨負債 377.6 億美元，總債務 944.8 億含租賃，現金 567.2 億。","side_b":"2026-11-02 法說 CFO Parekh：現金與有價證券 1,370 億、總債務 800 億，淨現金約 570 億。","ruling":"看償債能力採 B 側。差額約占企業價值 1.9%，情境樹走 EPS，不受影響。性質：可調和。","evidence_level":"高","settle_metric":"10-K 資產負債表","if_then":[],"evidence_refs":[]},{"axis":"Services 放緩的歸因","cause":null,"prior_field":null,"side_a":"2026-11-02 法說 CFO Parekh 主要歸因匯率：三月到九月季約 4 個百分點，十二月季再 0.5。","side_b":"同場十二月季指引把第三方授權列為主要逆風之一，App Store 九月季與去年相近，手遊疲弱延續，外部連結裁決仍在執行。2026-07-30 法說已提手遊疲弱。","ruling":"匯率歸因未證，持續監測。先登記期限：匯率逆風小於 1 個百分點的季度，Services 年增仍連 2 季低於 9%，匯率歸因就不成立。第三方授權的內容管理層未說明。","evidence_level":"中","settle_metric":"Services 年增率與 CFO 揭露的匯率影響","if_then":["若歸因不成立，下修 Base 的 Services 成長，不追","若匯率消退後回到 10% 以上，仍不追，H3 維持"],"evidence_refs":["channel_business_model_shift#1","regulatory_antitrust#2"]},{"axis":"供給限制的說法變化","cause":null,"prior_field":null,"side_a":"2026-07-30 法說 Cook 說九月季限制主因是系統晶片先進製程，並稱根因不是一般供給問題。","side_b":"2026-11-02 法說 Khan 說先進製程限制正在緩解，十二月季 Mac、iPad 受限主因轉為記憶體。Sankar 與 Mohan 問記憶體採購安排，只得到採購承諾增加 330 億美元的回答。","ruling":"限制已由晶片移到記憶體，問題由產能變成成本與可得性。是否簽長約、鎖價多少未回答，列為資料缺口。性質：可調和。","evidence_level":"中","settle_metric":"10-K 採購承諾、法說對記憶體成本的說法","if_then":["若採購承諾再季增至少 200 億美元且營收指引年增低於 5%，停止加碼"],"evidence_refs":["geo_supply_chain#2","supply_demand_durability#0"]},{"axis":"上季指引對帳","cause":null,"prior_field":null,"side_a":"2026-07-30 CFO Parekh 指引九月季營收年增 9%～11%、iPhone 中十位數、毛利率 47%～48%、營業費用 191～194 億美元。","side_b":"實績為年增 12%、iPhone 年增 17%、毛利率 47.9%、營業費用 192 億美元。","ruling":"管理層指引偏保守，這是看多的真實證據，所以 Base 的 FY27 EPS 只比共識低約 2%，不放更低。","evidence_level":"高","settle_metric":"十二月季實績對指引","if_then":["若十二月季毛利率高於 46%，仍不追，上調 Base EPS"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"裝置超過 25 億台，份額在最差的市場裡擴大，大中華區全年年增 28%，Duo 供不應求；AI 對手燒錢而 Apple FCF 利潤率 28.4%。優質資產少有便宜價，等 257 美元可能等不到。","side_b":"現價要賺 8%，EPS 五年要年增 15.7%（27 倍）或 11.8%（32 倍），共識只有 9.6%；十二月季毛利率指引還低於九月季。","ruling":"採 B 側，不追。等不到的機會成本是真實的，所以保留上移條件：毛利額連 4 季年增至少 8% 且 FY28 共識 EPS 至少 11.5 時重跑情境樹，價格門檻隨 EPS 上移。","evidence_level":"中","settle_metric":"毛利額年增率、FY28 共識 EPS","if_then":["若股價續漲而毛利額證據未到，不追","若股價下跌但基本面無損且條件成立，分批反買"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭面轉好：IDC 8 月預測 Android 年減 20%、iOS 年減 5.2%，Apple 份額擴大。對手仍可接近零利潤銷售。","side_b":"其他結構變數惡化：DOJ 與 DMA 切割 Services，AI 入口未定，記憶體價值鏈移轉。","ruling":"雙向拉鋸。競爭面結構性轉好，法規與價值鏈分配變差。","evidence_level":"中","settle_metric":"手機份額、Services 年增率","if_then":[],"evidence_refs":["competitive_share_entrants#1","regulatory_antitrust#1"]}],"triggers":[{"n":1,"text":"毛利額連兩季年減","type":"Single Thing","maps_to":"H2","metric":"公司毛利額年增率（剔關稅退款）","threshold":"連 2 季低於 0%","action":"不建倉；已持有者減碼一半","source_freq":"每季 8-K","date":"2027-01","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1"]},{"n":2,"text":"估值與毛利率同時達標才重新研究","type":"估值rearm","maps_to":"估值","metric":"FY27 共識前瞻本益比與公司毛利率","threshold":"≤ 27 倍（約 $257）且毛利率連 2 季 ≥ 45%","action":"重跑研究，通過後小倉分批反買","source_freq":"每日股價、每季財報","date":null,"evidence_refs":[]},{"n":3,"text":"FY27 營收檢查","type":"假設驗證","maps_to":"H1","metric":"FY27 營收年增率","threshold":"低於 10%","action":"下修 Base 營收，不追","source_freq":"每季 8-K","date":"2027-11","evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"Services 成長跌破底線","type":"風險","maps_to":"R2","metric":"Services 年增率","threshold":"連 2 季低於 7%","action":"減碼一半，未持有則不追","source_freq":"每季 8-K","date":"2027-01","evidence_refs":["channel_business_model_shift#1"]},{"n":5,"text":"監管或司法出現不利定案","type":"風險","maps_to":"R2","metric":"最高法院外部連結裁決、Google 上訴、DMA 第 6(4) 條認定","threshold":"任一項不利，且 Google 商業條件被禁或公司揭露 Services 受重大影響","action":"減碼一半","source_freq":"事件驅動","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#2","lawsuit_class_action#1"]},{"n":6,"text":"AI 入口開始侵蝕平台","type":"風險","maps_to":"R3","metric":"App Store 年增方向與付費訂閱數","threshold":"App Store 連 2 季年減，或付費訂閱低於 15 億","action":"減碼一半","source_freq":"每季法說","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"n":7,"text":"採購承諾放大而需求轉弱","type":"風險","maps_to":"R1","metric":"製造採購承諾季增額與下季營收指引","threshold":"再季增至少 200 億美元且指引年增低於 5%","action":"停止加碼","source_freq":"每季 10-Q、法說","date":"2027-01","evidence_refs":["supply_demand_durability#4"]},{"n":8,"text":"毛利額持續衰退","type":"清倉","maps_to":"R1","metric":"毛利額年增率與 FY28 共識 EPS","threshold":"毛利額連 4 季年減且 FY28 共識 EPS 低於 9.5","action":"清倉","source_freq":"每季 8-K、共識快照","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":9,"text":"供應鏈或關稅吸收失敗","type":"風險","maps_to":"R4","metric":"營收指引年增率與公司毛利率","threshold":"指引連 2 季低於 5%，或新關稅使毛利率連 2 季低於 44%","action":"減碼一半","source_freq":"每季法說","date":null,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"n":10,"text":"手機份額回吐","type":"風險","maps_to":"R5","metric":"第三季全球手機份額","threshold":"低於 20%","action":"減碼一半，未持有則不追","source_freq":"Counterpoint、IDC 每季","date":"2027-10","evidence_refs":["competitive_share_entrants#1"]},{"n":11,"text":"證券集體訴訟進入不利階段","type":"風險","maps_to":"R6","metric":"Siri AI 與 Epic 合規集體訴訟程序","threshold":"集體認證通過且出現不利和解；刑事介入則清倉","action":"減碼至半倉","source_freq":"事件驅動","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":12,"text":"十二月季財報後複審","type":"複審日期","maps_to":"H2","metric":"十二月季毛利額與毛利率","threshold":"毛利率是否落在 45%～46%","action":"更新情境路徑","source_freq":"每季 8-K","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"公司毛利額年增率（剔關稅退款）","bear_threshold":"連 2 季低於 0%","window":"FY27 各季","source":"每季 8-K 營收與毛利率","last_status":"unknown"},{"metric":"公司毛利率","bear_threshold":"連 2 季低於 44%","window":"FY27 至 FY28","source":"每季 8-K","last_status":"warning"},{"metric":"Services 年增率","bear_threshold":"連 2 季低於 7%","window":"FY27 至 FY28","source":"每季 8-K","last_status":"ok"},{"metric":"第三季全球手機份額","bear_threshold":"低於 20%","window":"2027 年第三季","source":"Counterpoint、IDC","last_status":"ok"},{"metric":"FY27 共識 EPS","bear_threshold":"低於 9.0","window":"未來 12 個月","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場同時相信 FY27 營收年增約 19% 和 36 倍本益比；十二月季指引只有 7%～10%、毛利率還在降，五年要賺 8% 需要 EPS 年增約 16%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🔴', moat_trend='→', week26=16.93, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"FY27 共識前瞻本益比 ≤ 27 倍（約 $257）且公司毛利率連 2 季 ≥ 45%，兩項同時成立才重跑研究","exec_line":"不追，現價 342.37 美元不建首倉。條件成立後重跑研究，首筆只用小倉。"},"reasoning":{"industry":"九月季營收 1,144.77 億美元，iPhone 占 50.3%、Services 27.6%、Mac 9.4%、穿戴 7.3%、iPad 5.4%（Mac、iPad、穿戴金額取自 2026-11-02 法說 CFO Parekh 口述）。公司毛利率 47.9%、營益率 31.1%。Services 營收不到三成，毛利卻占約 44%（315.73 億美元乘 76%，除以總毛利 548.3 億美元，76% 取自同場法說）。單點依賴有兩個：iPhone 占一半營收；系統晶片只靠台積電，DRAM 只有三家供應商。間接通路占淨銷售約 60%，電信業者占應收帳款 33%，單一客戶 13%，這是信用集中，不是需求集中。產業位置判在收縮期，IDC 8 月預測 2026 年手機出貨年減 16.7%、平均售價年增 27.6%，短缺壓量抬價。供需判斷是週期性將反轉，但時間偏晚：Samsung 預期短缺延續到 2028，Counterpoint 預期 2027 年手機再減 1.4%。","moat":"機制是 iOS、自研晶片與服務綁在同一個裝置基礎上，活躍裝置超過 25 億台。方向看份額：Counterpoint 2026 年第三季全球手機 22%（去年同期 18%），IDC 的 Mac 份額 9.5%（8.5%），中國手機 17.8%（15.8%）。同業 ROIC 無資料，改看 FCF 利潤率：Apple 28.4%，MSFT 17.3%、GOOGL 4.2%、AMZN −6.4%，對手正把現金投進 AI 基礎建設。反向證據在 Services：九月季 App Store 與去年相近，十二月季指引 8%～9%，監管與第三方授權都在壓。AI 淨增量尚未出現，Siri AI 目前只看到雲端成本進 Services 銷貨成本、硬體遞延增加，付費升級還沒定價；AI 長在自有作業系統上屬強化，agent 若從 App 層繞過入口就是替代，分界年看 2028。兩項評分 8 已含生態攻擊的扣分。FY26 毛利率 48.79% 是四年高點，約 0.7 個百分點來自關稅退款（九月季約 11 億、六月季約 22 億美元，粗估），記憶體結轉庫存也屬短期因素，這些不當結構性。可能看錯的地方：份額上升有一部分來自 Android 缺料，短缺結束後可能回吐。","growth":"成長靠價、mix 和回購，量受供給限制。FY26 營收年增 15.1%、EPS 年增 20%；FY23～FY26 營收 CAGR 7.7%、EPS CAGR 13.6%（financial_history.years，yfinance 年報）。三年共識 EPS CAGR 9.6%（8.98 到 11.82，Koyfin 2026-11-07，分析師家數事實表未涵蓋）。內生上界算不出，保守當作共識已超出。缺口歸因：淨回購每年約 1.7 個百分點，其餘來自定價與 mix，不依賴倍數上升。共識內部有一個待驗的組合：FY27 EPS 9.5 在費用年增 12%、稅率 17%、平均股數約 144 億下，需要毛利額約 2,480 億美元；若營收 5,693 億美元，毛利率約 43.6%，若營收只增 10%，毛利率要 47.1%，高於十二月季指引 45%～46%。跑道判中等：22% 是出貨份額，不是高階客群滲透率，後者事實表未涵蓋，所以不按份額直接給寬；Duo、Siri AI 付費、健康與家庭都還沒有營收證據，不算第二條曲線。","governance":"FY26 FCF 1,360.6 億美元對淨利 1,321.8 億美元，轉換率 1.03；SBC 137.9 億美元，占營收 2.9%、占營業利益 8.7%。九月季回饋股東 280 億美元（回購 240 億、股利 39 億），現金與有價證券由六月季 1,470 億降到 1,370 億，總債務 800 億（2026-07-30、2026-11-02 法說 CFO Parekh）。公司已取消淨現金歸零目標，CFO 只說保留彈性，沒有新目標。現金需求正在變大：製造採購承諾季增 330 億美元，美國四年 6,000 億美元承諾，AI 算力需求管理層說還在很早期。以現價回購的盈餘收益率約 2.8%。近三年現金去向四分、回購均價與債務到期結構事實表未涵蓋。事實表淨負債 378 億美元與 CFO 口徑淨現金約 570 億美元的差異，應來自長期有價證券與租賃，看償債能力採 CFO 口徑。","valuation":"現價 342.37 美元等於 36.04 倍 FY27 共識 EPS、38.13 倍 FY26 EPS。五年要賺 8%，終端股價要 503 美元：終端 27 倍需要 EPS 年增約 15.7%，32 倍需要約 11.8%，共識三年 CAGR 只有 9.6%。基準情境五年後約 375 美元，年化約 2%，倍數收斂吃掉大部分 EPS 成長。12 個月目標用 32 倍乘 FY28 Base EPS 10.4，約 333 美元；24 個月用 30 倍乘 FY29 Base EPS 11.55，約 347 美元。賣方平均目標價 327～331 美元低於現價，但資料日是 6 月與 8 月，已舊；高低 400 與 200 美元相差 2 倍，分歧不算極端，小幅支持不追。同業前瞻倍數事實表未涵蓋，終端倍數無法做同業現值對照，以本股現值與 27 倍進場門檻為錨。近 3 個月 FY1 上修 7.95% 應是財年切換造成，不當上修動能。","premortem":"最可能看錯三處。一，Base EPS 比共識低約 2%，但上一季指引偏保守，九月季營收與 iPhone 都超過區間，看錯就是錯過上漲。二，倍數可能長期維持 30 倍以上，Apple 的 FCF 利潤率遠高於投入 AI 的同業，市場可能繼續給稀缺溢價。三，記憶體短缺若在 2027 年中緩解，毛利率回升會快過我的路徑。衰退信號成立一項（FY23～FY26 EPS CAGR 高於營收 CAGR 5.9 個百分點），毛利率年減接近成立但去年同季資料事實表未涵蓋，價值陷阱風險判中等。壓力測試三組：FY29 後成長率降到 15%、10%、5%，終端倍數 30、26、18 倍，五年後股價約 458、363、229 美元，兩組不虧。法說迴避項：2026-07-30 Cook 未回答是否拓寬矽供應商，Ternus 未談 OpenAI 裝置與 SpaceX AI 手機；2026-11-02 Khan 兩次被問記憶體採購安排都只回採購承諾，Ternus 未解釋 iPhone 18 標準版缺席。歷史最大回撤事實表未涵蓋。RSI 標示不可用，不引用。"},"plain":{"six":{"how_it_makes_money":"賺的是 25 億台裝置持有人的換機錢和過路費，眼下利潤被卡在記憶體這一節。","moat":"護城河穩定：硬體端擴大，Services 端縮減，兩邊相抵。","growth":"五年後跑道中等：手機份額還有空間，第二條成長曲線尚未被財報證明。","capital":"資本配置穩健，但在 36 倍回購的報酬偏低。","valuation":"現價要求 EPS 五年年增約 16% 才賺得到 8%，我不相信。","how_wrong":"最可能看錯的是低估管理層保守度與 Apple 的稀缺溢價。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場同時相信 FY27 營收年增約 19% 和 36 倍本益比；十二月季指引只有 7%～10%、毛利率還在降，五年要賺 8% 需要 EPS 年增約 16%。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 FY27 共識前瞻本益比回到 27 倍（約 $257）以下，且公司毛利率連 2 季 ≥ 45%。","trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":342.37,"week26_return_pct":16.93,"consensus_rev_3m_pct":7.95,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"trailing 分母 8.98 含關稅退款（九月季 0.05 美元；六月季金額未揭露，按毛利率約 2 個百分點粗估約 0.10 美元）。前瞻分母 9.5 的爭點是記憶體成本。兩個分母都不支持便宜論證。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"十二月季財報與三月季指引","impact":"高","watch":"毛利額年增率、毛利率是否落在 45%～46%、記憶體結轉庫存說法；實際日期待公司公告"},{"date":"2027-06","date_precision":"quarter","type":"macro","event":"IDC 預期記憶體價格 2027 年中趨穩","impact":"高","watch":"公司毛利率指引是否止跌"},{"date":null,"date_precision":null,"type":"regulatory","event":"最高法院審理外部連結裁決上訴","impact":"高","watch":"App Store 抽成能否恢復；開庭與判決日事實表未涵蓋"},{"date":null,"date_precision":null,"type":"regulatory","event":"歐盟 DMA 第 6(4) 條最終認定","impact":"中","watch":"罰款金額與互通性義務"},{"date":null,"date_precision":null,"type":"product","event":"Siri AI 伺服器用量超額付費上線","impact":"中","watch":"定價與 iCloud+ 附著率"}],"_projected_from":"v19"}
```
