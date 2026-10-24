你是 stock-analyst v20 的**散文層（prose）agent**，標的 CRS（2026-10-25）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：CRS　日期：2026-10-25　archetype：None　前份裁決：2026-09-01　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1641B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（393B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1120B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1466B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（962B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（498B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（826B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2128B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4100B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2635B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1641           3751-5359      5 條（2–6 內）  
s3                  8000         393           5325-7607      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3548          8016-11452      5 條（2–6 內）  
s6                 11000         498          7351-10502      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         826           1872-2674      5 條（2–6 內）  
s10                 5000        2128           2010-2872      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2635           2000-2365      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4700B；至少需散文≈40.30KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−68%
−62
−62%
−56%
−45%
−42
−42%
−40.3%
−33.32
−33%
−24.8
−17.9%
−2.2%
−0.6%
0
0%
0.28
0.4%
0.41
0.6
0.63
0.68
0.75
0.76
0.8%
0.84
0.96
1
01
1.0
1.14
1.5
1.5%
1.7
1.91
2
2%
2.6
2.8
2.8%
3%
3
03
3.25
3.3%
4
4%
4.7%
4.8
5
5%
5.2%
6
06
6.4%
6.4
7
07
7%
7.3
7.8%
8
8.4%
9
09
9.4
9.5
10
10%
10.5%
10.5
10.52
10.58
10.6
10.76
11%
11
11.4
12
12.6
12.8
13.2%
13.3
13.38
14%
14
14.1
14.8
15%
15
15.2%
15.5%
15.6
15.96
16%
17
17.2
17.8
17.84
18%
18
18.6
19
19.20
19.2
19.6%
20
20%
20.6
21
21%
21.28
21.3
22%
22
22.4
22.5%
23%
24
24.6%
25%
25
26
26.5%
27
27.3%
28%
30%
30
30.6%
30.9%
31
32%
33%
34.7%
35%
35
36
36%
37%
37.5%
37.7%
39
39%
39.5
40%
40.3%
42
45%
45
49
49%
50
50%
52
52.6
52.8
55.3
65%
70
77.7
83.0
98
99%
100
100%
104
126
133.9
150%
150
168
187.5
195
196.4
200
214
216.3
218
222
250
284.66
317
335
362.3
400
418
426
430
465.80
476
476.42
520.92
521
539.8
540
555
573.5
625.88
648
650
700
702
798.2
850
880
2019
2026
2027
2028
2034
20261025
1,056
1,100
1,200
1,300
1,400
1,500
16,000
2,100
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
{"meta":{"ticker":"CRS","date":"2026-10-25","schema":"v15.0","contract":"v19","company_name":"Carpenter Technology"},"oneliner":"航太鎳基超合金供不應求，長約續約持續漲價，FY27 營業利益指引 850–880 百萬美元維持不變；股價半年跌 33%，前瞻本益比降到約 21 倍，基本面未見破損。利益率處於歷史高點，週期回落風險以 Bear 三成機率計價。","thesis":{"H":[{"id":"H1","text":"擴產上線前，SAO 調整後營益率（不含附加費）維持 35% 以上，代表定價來自供給缺口與長約重訂，而不是單季產品組合。","2y":"FY27–FY28 各季≥35%（Q1 FY27 為 37.7%）","5y":"FY31 擴產全數貢獻後≥32%","10y":null,"threshold":"連 2 季低於 35% 為削弱；連 4 季低於 32% 為反轉","source":"季報新聞稿與每季法說（SAO 部門數字）","drift_rule":"連 2 季低於 35%"},{"id":"H2","text":"商用航太下單仍在加速：結構件、通路與引擎訂單持續年增，客戶下單量還沒跟上主機廠產率。","2y":"FY27–FY28 商用航太訂單每季年增（Q1 FY27 年增 25%，結構件與通路 +49%、引擎 +22%）","5y":"FY31 航太國防仍占營收約六成以上，訂單未轉負","10y":null,"threshold":"商用航太訂單年增率連 2 季轉負為削弱；連 3 季轉負為反轉","source":"每季法說口述（公司不揭露絕對金額，且已停止揭露出貨量）","drift_rule":"連 2 季年減"},{"id":"H3","text":"FY27 營業利益 850–880 百萬美元與 FY29 1,200–1,300 百萬美元目標可達，擴產案於 FY28 初如期完工。","2y":"FY27 實際≥850；FY28 初擴產開機","5y":"FY29 營業利益≥1,200；FY30 擴產帶來增量營業利益約 150","10y":null,"threshold":"FY27 指引下緣下修為削弱；FY29 目標下修至 1,100 以下為反轉；擴產延後逾 6 個月為削弱","source":"季報新聞稿與每季法說","drift_rule":"指引下緣下修或擴產延後"}],"R":[{"id":"R1","text":"SAO 營業利益連續低於指引：Q1 已低於 Q4 FY26 法說給的 218–222 下緣，Q2 指引 214–218 也沒有季增。","h_ref":"H1","clock":"⚡","threshold":"連 2 季低於當季指引下緣","evidence_refs":[]},{"id":"R2","text":"ATI 等同業新產能加上本公司擴產，2028 年後產業提價紀律鬆動，長約續約漲幅縮小。","h_ref":"H1","clock":"🔥","threshold":"續約漲幅連 2 次降到個位數為削弱；出現持平或折價續約為反轉","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"航太週期反轉：主機廠訂單淨額轉弱，積壓訂單相對交付的年數下降，與擴產上線時點撞在一起。","h_ref":"H2","clock":"🐢","threshold":"積壓÷年交付由約 10 年降到 6 年以下開始減碼；降到 4 年以下大幅減碼","evidence_refs":[]},{"id":"R4","text":"關鍵原料部分來自政經不穩國家且可能沒有替代來源，關稅與出口管制變動導致附加費轉嫁失效。","h_ref":"H1","clock":"🔥","threshold":"SAO 營益率年減 3 個百分點以上，且公司歸因於原料或關稅","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#1"]},{"id":"R5","text":"國防撥款遲滯拖過期中選舉，國防量持續偏少，影響產線調度與產品組合。","h_ref":"H2","clock":"⚡","threshold":"至 2027 年 6 月國防訂單仍年減","evidence_refs":[]}],"single_thing":{"description":"主要航太長約續約（法說稱一份已達原則協議、另有兩份大型合約談判中）出現價格持平或下調。","why_fatal":"情境樹最大的單一敏感度在價格：產能滿載下量的成長受限於擴產約 7%，FY29 目標的利益率擴張幾乎全靠價格；長約占航太業務多數，一份大型長約不漲價，就代表供需缺口論點失效。","if_happens":"減碼至半倉，並把 Base 情境終端本益比由 19 倍降到 15 倍重算。","how_monitor":"每季法說的長約續約描述，以及 SAO 營益率","probability":"約 10%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.84,"peg_fy2":0.84,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":10.76,"FY2027E":13.38,"FY2028E":15.96,"FY2029E":19.2},"fy_end_month":6,"eps_basis":"調整後（non-GAAP）EPS，財年結束於 6 月。基期 FY2026A 10.76 取自 FY26 年度結果報導；GAAP 稀釋 EPS 為 10.52。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"產能滿載、長約重訂價、附加費轉嫁的特殊合金廠；FY23 營益率僅 5.2%，循環性並未消失。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性偏持久。Q2 FY26 簡報稱 2019 年以來無實質新增產能、合格供應商少；Q1 FY27 法說 CEO 稱除本公司擴產與少數幾家外沒有新產能上線。反向因素是本公司與 ATI 同步擴產。","bargaining":{"up":"鎳、鈷、鈦等原料部分來自政經不穩國家，供應商漲價時可能沒有替代來源，目前以附加費轉嫁吸收。","down":"客戶最在意保證供貨。長約續約價格大幅上調，客戶都要求更多材料；無單一客戶超過營收 10%。","geo":"關稅經附加費轉嫁，管理層判斷目前無重大影響。國防撥款遲滯壓低國防訂單。"},"profit_pool_dir":"利潤池往材料端移動：本公司營益率 FY23 5.2%，FY26 升到 22.5%。下游鍛造與緊固件商 HWM 營益率仍高於本公司（27.3%）。","tam_table":{"expanded":false,"reason":"不屬低滲透或新品類題材，成長來自既有航太產率爬升與價格；事實表未涵蓋市場規模與份額數據。"}},"moat":{"mechanism":"材料認證轉換成本，加上合格熔煉產能稀缺與多年長約","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"Q1 FY27 法說：長約份額大致不變、沒有搶份額；價格續漲但來自供需缺口；本公司擴產約 9,000 噸與 ATI 擴產同步進行。營益率較 ATI 高 7.3 個百分點、較 HWM 低 4.8 個百分點；同業利差歷史序列事實表未涵蓋。","threats":[{"level":"🟡","text":"ATI 等同業擴產，加上本公司 FY28 初擴產約 9,000 噸，2028 年後供需缺口可能收斂，長約續約漲幅隨之縮小。","p":"25%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"10-K 揭露部分產品可被替代，低價替代材料可得時客戶可能轉用。航太認證件替代難度高，衝擊集中在工業與消費等不需認證的品項。","p":"10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是航空公司，決策者與付款者是引擎與機體供應鏈。沒有合格合金就造不出引擎，屬「需要」而非「想要」。主機廠積壓逾 16,000 架，第三季空中交通量季增 14%，引擎首次大修潮來臨。"},{"item":"決策層級","level":"🟢","text":"替代性要看料號層級的認證：換供應商須重新認證，第三方稱需 18–36 個月；航太業務多數在長約下，長約續約時客戶都要更多量。"},{"item":"價值鏈分配","level":"🟡","text":"材料端分到的利潤正在變多（營益率 FY23 5.2%→FY26 22.5%），但下游 HWM 營益率仍高 4.8 個百分點。上游原料部分來自不穩國家，供應商議價力未知；新產能 2028 年後上線可能把分配推回下游。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業與國防供應鏈，沒有消費者端的政治漲價上限。國防採購價格審查是潛在上限，但本包證據未見相關討論。"}],"roiic":"約 30%（擴產案：增量營業利益約 150 百萬美元×(1−21%)÷投入約 400 百萬美元）","reinvest_rate":"約 35%（代理值：1−FY26 自由現金流 362.3÷稅後營業利益約 555；折舊與營運資金明細事實表未涵蓋）","endo_ceiling":10.5,"formula_note":"內生成長＝30%×35%≈10.5%。擴產投入約 4 億取自前份判斷引用的 Q4 FY26 法說；1.5 億增量營業利益取自 2026-07-30 Q4 FY26 法說 CFO 原話；稅率 21% 取公司指引區間 20–22% 中值。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","CRS":30.58,"HWM":36.03,"ATI":23.36,"MTRN":16.01,"RS":28.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","CRS":22.47,"HWM":27.31,"ATI":15.19,"MTRN":6.35,"RS":7.76,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","CRS":11.6,"HWM":19.64,"ATI":11.16,"MTRN":1.55,"RS":3.41,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","CRS":null,"HWM":0.41,"ATI":null,"MTRN":1.23,"RS":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"HWM","gm":36.03,"om":27.31,"fcf_margin":19.64,"rd_intensity":0.41,"strategy_note":"下游鍛造與緊固件龍頭，部分是本公司客戶。營益率 27.3%、自由現金流利潤率 19.6%，都高於本公司，代表價值鏈下游仍分走較多利潤。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ATI","gm":23.36,"om":15.19,"fcf_margin":11.16,"rd_intensity":null,"strategy_note":"最接近的熔煉同業，營益率 15.2%，正在擴產。新產能上線時點是本公司長約漲幅能否延續的主要變數。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MTRN","gm":16.01,"om":6.35,"fcf_margin":1.55,"rd_intensity":1.23,"strategy_note":"鈹與先進材料利基，營益率 6.4%，與本公司航太超合金重疊有限，不作定價錨。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"RS","gm":28.21,"om":7.76,"fcf_margin":3.41,"rd_intensity":null,"strategy_note":"金屬通路與加工中心，營益率 7.8%，屬通路角色而非熔煉產能持有者。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"價為主、量為輔（擴產約 +7%），再加淨回購","runway_years":7,"runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 30%×再投資率約 35%≈10.5%；共識三年 EPS 年化約 21%，缺口由利益率擴張與淨回購解釋","segments":[{"item":"SAO（Q1 FY27，不含附加費）","value":"營收 573.5 百萬美元，年增 7%；調整後營益率 37.7%；營業利益 216.3"},{"item":"PEP（Q1 FY27，不含附加費）","value":"營收 83.0 百萬美元，年減 5%；營業利益 7.3（去年同期 9.4），鈦醫療走弱"},{"item":"航太國防終端（FY26）","value":"約占營收 65%，年增 15%；醫療年減約 21%、運輸年減約 11%"}],"decay_signals":["EPS 成長遠高於營收成長：亮燈（FY23→FY26 營收年化約 7%，EPS 由 1.14 升至 10.52）","FCF÷淨利：FY26 0.68、FY25 0.76，只有一年低於 0.75，未達連兩年，列觀察","毛利率連 2 季年減：未亮（年度毛利率 13.2%→30.6% 逐年上升）","SBC 占營收：未亮（0.8%）","核心市占縮減：未亮（管理層稱份額持平）","提價後銷量下滑：無法判斷（公司已停止揭露出貨量）","產業估值倍數系統性下移：事實表未涵蓋"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；現金去向以擴產與回購為主，已在判斷理由中交代。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年沒有併購；Q4 FY26 法說 CEO 表示併購不排除，但優先序低。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q1 回購 133.9 百萬美元，期間股價約 476–521，對 FY27 共識 EPS 13.38 的買入收益率約 2.6–2.8%，低於公債殖利率加 2% 的門檻。實際回購均價事實表未涵蓋。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營收 0.8%、占 GAAP 營業利益 3.3%；回購使股數淨減少，淨稀釋率為負。","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY1＝FY2027E 調整後 EPS）與 PEG，P/S 年度端點分位作輔助","tier":"特殊合金／航太材料","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業本益比，不跨層級借用。"},"fwd_pe":21.28,"peg":1.0,"percentile_5y":39.5,"val_light":"🟡","val_light_derivation":"PEG 約 1.0（21.3 倍÷三年 EPS 年化約 21%），落在合理區下緣。但分母是歷史最高利益率下的盈餘，FY23 營益率只有 5.2%，加上週期折價後結論停在中性。分位採 P/S 年度端點的 39.5（不是五年日頻）；本益比分位 0 因 FY23 盈餘低谷失真，不採用。","upside_short_pct":18,"upside_mid_pct":50},"trap_analysis":{"verdict":"🟡","label":"利益率高檔的週期風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"上一輪谷底 FY23 營益率 5.2%、EPS 1.14；同業 ATI 擴產，本公司擴產也在 FY28 初上線。","assumption":"長約漲價與 37% 以上的 SAO 營益率能延續到 FY30 以後。","consequence":"若 FY29–30 航太去庫存疊加新產能上線，長約不再漲價，EPS 回落到 10–11，本益比壓到 12 倍，股價約 126，較現價 −56%。","ruling":"部分採納，已放進 Bear 30%。但 Q1 法說稱除本公司與少數幾家外沒有新產能，積壓訂單逾 16,000 架，週期反轉最快也在 FY29 之後；不採納「一兩年內就反轉」的說法。","watch":"長約續約價格、商用航太訂單年增率、ATI 新產能投產時點","evidence_refs":["competitive_share_entrants#1"],"fact_refs":["f_kpi7_sao_segment_operating_ma","f_peer_ati_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流÷淨利從 FY24 0.96 降到 FY26 0.68；Q1 自由現金流 −24.8；Q1 回購 133.9 落在 476–521 價位區間；本季起停止揭露出貨量。","assumption":"營業利益成長會等比例轉成每股現金。","consequence":"營業利益達標，但擴產與營運資金吃掉現金，高價回購折損價值，每股自由現金流成長落後 EPS。","ruling":"部分採納。FY27 自由現金流指引 400–430 若達成，對 FY27 淨利約 650（共識 EPS×現股數推估），轉換率約 0.63，仍然偏低。擴產完工後 FY28 起資本支出應回落，轉換率能否回升是可以驗證的。","watch":"FY27 自由現金流是否達 400；FY28 資本支出是否回落","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc","f_consensus_eps_fy1","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"8 月初一家聚合站的賣方共識目標價 465.80，低於當時股價 520.92 約 16%；各聚合站共識數字不一致，另一來源為 625.88、區間 540–700。","assumption":"高本益比可以延續。","consequence":"倍數向下修正。","ruling":"反駁。這條證據描述的是 8 月初的狀況，當時以現行 FY27 共識計約 39 倍前瞻本益比；現價 284.66 已比該最低共識目標價再低約 39%，前瞻本益比 21.3 倍，「反映太多」的風險在本輪下殺中已大致釋放。保留的部分：聚合站口徑不一，目標價不作為依據。","watch":"FY2 共識是否開始下修","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_week26_return_pct"]}],"max_dd":{"lo":-62,"hi":-42,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 476.42 → 本次 284.66（-40.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=476.42","side_b":"本次 price_at_dd=284.66","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 衛星","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份角色：均線 ✅→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 476.42 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 476.42 美元：Bull 價 1,056、Bear 價 187.5，五年期望值 +34.7%，基準年化 8.4%，不對稱比 1.7","side_b":"本次情境、股價仍用 476.42 美元：Bull 價 648、Bear 價 126，五年期望值 −17.9%，基準年化 −2.2%，不對稱比 0.41","ruling":"先換情境、股價不動：五年期望值少 52.6 個百分點，基準年化少 10.6 個百分點。不對稱比由 1.7 變為 0.41。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 476.42 美元：五年期望值 −17.9%，基準年化 −2.2%，不對稱比 0.41","side_b":"本次情境、股價 284.66 美元：五年期望值 +37.5%，基準年化 8.4%，不對稱比 1.91","ruling":"再換股價、情境不動：起點價下跌 40.3%，五年期望值多 55.3 個百分點，基準年化多 10.6 個百分點，不對稱比由 0.41 升到 1.91。合計五年期望值比前份多 2.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份裁決、訊號與估值結論","cause":"價格變動","prior_field":["signal","val","p_bull_pct","p_bear_pct","max_dd_pct","cycle_position"],"side_a":"前份（2026-09-01，股價 476.42）：進場、核心；訊號 A；估值中性；Bull 25%／Bear 30%；最大回撤 −68%；未設循環位置。","side_b":"本次（股價 284.66）：訊號 A 不變；估值結論仍為中性，但前瞻本益比從約 35 倍降到約 21 倍；Bull 25%／Base 45%／Bear 30% 不變；回撤區間改以現價起算 −42% 至 −62%；循環位置仍不設；裁決與部位大小在均線轉弱後重新決定。","ruling":"股價下跌約 40%，但營業利益指引與訂單都沒有轉弱，基本面結論沿用。前份在約 35 倍給中性，本次在 21 倍仍給中性，是因為把利益率位於歷史高點的週期折價納入。回撤改以現價為基準：前份估的 −68%，自 8 月引用價起算已實現約 −45%。","evidence_level":"價格為已實現資料；指引來自公司新聞稿","settle_metric":"Q2 FY27 SAO 營業利益與商用航太訂單","if_then":["若 Q2 FY27 SAO 營業利益≥214 且商用航太訂單續年增，加第二批","若 Q2 FY27 SAO 營業利益<214，停止加碼並把 Bear 機率上調至 35%"],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：擴大（↑）","side_b":"本次：穩定（→）","ruling":"Q1 FY27 法說 CEO 明言長約份額大致不變、沒有搶份額；價格上漲主要來自供需缺口，屬可逆來源；本公司與 ATI 都在擴產。進入門檻（認證、合格供應商少）沒有改變，所以判穩定，而不是縮減。","evidence_level":"法說原話與同業擴產報導","settle_metric":"長約續約價格與同業營益率差距","if_then":["若下一份大型長約續約價格再上調且 ATI 營益率差距維持 7 個百分點以上，可回到擴大","若長約續約價格持平，改判縮減並減碼至半倉"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"價值陷阱、跑道與類別","cause":"方法變動","prior_field":["trap","runway_post_y5","archetype"],"side_a":"前份：陷阱風險低（🟢）、五年後跑道寬（🟢）、品質複利成長","side_b":"本次：陷阱風險中（🟡）、五年後跑道中（🟡）；主類別仍為品質複利成長，另加註循環性為副類別","ruling":"本次逐項套用衰退信號。EPS 成長遠高於營收成長一項亮燈：FY23→FY26 營收年化約 7%，EPS 由 1.14 升到 10.52；FY26 自由現金流÷淨利 0.68 低於 0.75，但只有一年，列觀察。跑道方面，以目標產率 2,100 架計，16,000 架積壓約 7–8 年，FY31 後的成長取決於新訂單與第二曲線，目前沒有量化證據。","evidence_level":"年度財報序列與法說口述","settle_metric":"FY27 自由現金流÷淨利、主機廠新訂單","if_then":["若 FY27 自由現金流÷淨利再低於 0.75，陷阱風險維持中並停止加碼","若國防或燃氣渦輪營收占比出現可量化的雙位數成長，跑道可回到寬"],"evidence_refs":[]},{"axis":"唯一致命點（Single Thing）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定（null）","side_b":"主要航太長約續約價格持平或下調","ruling":"前份把風險分散在三條風險項中；本次依最大單一敏感度的原則，指定價格為唯一致命點。產能滿載下量的成長只有擴產約 7%，利益率擴張幾乎全靠價格。一旦發生即減碼至半倉。","evidence_level":"法說：一份長約已達原則協議、另有兩份談判中","settle_metric":"每季法說的長約續約描述","if_then":["若續約價格持平或下調，減碼至半倉","若三份續約全部上調，維持部位"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標（null）","side_b":"新設五條：SAO 營益率連 4 季低於 32%、商用航太訂單連 3 季年減、FY27 營業利益低於 850、長約續約不漲價、擴產延後逾 6 個月；前兩條同時發生即清倉，其餘任一發生即減碼。","ruling":"前份只有假設與風險的警戒值，沒有可執行的出場線；本次補上，讓減碼與清倉綁定可觀察的數字。","evidence_level":"公司新聞稿與法說","settle_metric":"SAO 營益率與商用航太訂單","if_then":["SAO 營益率連 4 季低於 32% 且訂單連 3 季年減，清倉","FY27 營業利益低於 850，減碼至半倉"],"evidence_refs":[]},{"axis":"加碼重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"已進場核心角色，無rearm觸發；加碼觸發見§13b","side_b":"Q2 FY27 財報（2027-01 下旬）SAO 營業利益≥214 且商用航太訂單續年增，或週收盤站回 104 週均線（約 317），任一成立即恢復正常加碼","ruling":"股價跌破 104 週均線，加碼節奏需要明確的重啟條件；以首個基本面驗證點或趨勢修復二擇一。","evidence_level":"均線與指引為已揭露數字","settle_metric":"Q2 FY27 SAO 營業利益、週收盤價","if_then":["任一條件成立，恢復加碼至目標部位","兩者皆未成立，維持分批節奏，不追價"],"evidence_refs":[]},{"axis":"管理層前季財測與本季實績","cause":"新證據","prior_field":null,"side_a":"2026-07-30 Q4 FY26 法說 CFO：Q1 總營業利益 195–200 百萬美元、SAO 218–222","side_b":"Q1 實績總營業利益 196.4（區間下半）、SAO 216.3（低於區間下緣）；Q2 SAO 指引 214–218，與 Q1 持平；CEO 稱達成 98–99%","ruling":"可調和，屬程度差異：總數達標，SAO 小幅未達。但 Q2 SAO 指引沒有季增，與 CEO「量價皆更強」的說法有落差，列為短期驗證點。","evidence_level":"公司新聞稿與法說原話","settle_metric":"Q2 FY27 SAO 營業利益","if_then":["若 Q2 SAO 營業利益≥218，維持加碼節奏","若 Q2 SAO 營業利益<214，停止加碼"],"evidence_refs":[]},{"axis":"結構件客戶下單","cause":"新證據","prior_field":null,"side_a":"2026-07-30 Q4 FY26 法說 CEO：結構件客戶下單仍謹慎，低於預期需求","side_b":"2026-10-22 Q1 FY27 法說 CEO：結構件與通路訂單季增 23%、年增 49%，客戶庫存下降","ruling":"一致：前季點名的保留項本季轉強，屬兌現而非改口。","evidence_level":"法說口述百分比，未給絕對數","settle_metric":"結構件與通路訂單年增率","if_then":["若 Q2 結構件與通路訂單續年增，維持 H2","若轉為年減，H2 降為削弱並停止加碼"],"evidence_refs":[]},{"axis":"國防需求與國防訂單","cause":"新證據","prior_field":null,"side_a":"CEO：國防終端需求大，與國防部的直接接觸增加，F/A-XX 有實質材料內容","side_b":"國防訂單季減且年減，直接客戶缺撥款無法下單；國防量偏少使產線調度受影響","ruling":"可調和，但時點不確定：需求存在，撥款時點未知。決勝數據要到期中選舉後預算明朗才會出現，在 2027 年上半之前無法裁決。","evidence_level":"法說口述","settle_metric":"國防訂單年增率","if_then":["若 2027 年 3 月前預算明朗且國防訂單轉為年增，維持 Bull 25%","若至 2027 年 6 月國防訂單仍年減，把國防補單從 Bull 假設中移除，Bull 機率降至 20%"],"evidence_refs":[]},{"axis":"量價揭露","cause":"新證據","prior_field":null,"side_a":"管理層稱量、價與需求展望都比上季更強","side_b":"本季起停止揭露出貨量，量價拆分無法從外部驗證（Q1 FY27 法說 CEO 自述）","ruling":"列為未證、持續監測。揭露減少本身是負面訊號；在恢復揭露出貨量或 SAO 營益率連續創高之前，不採信「量也在增」的說法，只採信營業利益。","evidence_level":"法說原話","settle_metric":"SAO 營業利益與營益率","if_then":["若 SAO 營益率連 2 季低於 36% 且仍不揭露出貨量，停止加碼","若恢復揭露且出貨量年增，維持現判"],"evidence_refs":[]},{"axis":"醫療終端","cause":"新證據","prior_field":null,"side_a":"2026-07-30 Q4 FY26 法說 CEO：醫療終端本財年首度季增","side_b":"Q1 FY27 PEP 營收年減 5%，營業利益 7.3（去年同期 9.4），主因鈦醫療銷售下滑；Q2 FY26 時鈦醫療經銷需求已疲弱","ruling":"可調和：醫療占比小，PEP 營業利益不到全公司 4%，不影響主論點；但前季「醫療轉好」的說法本季沒有延續。","evidence_level":"公司新聞稿與法說","settle_metric":"PEP 季營業利益","if_then":["若 PEP 季營業利益連 2 季低於 5 百萬，把醫療從第二曲線清單移除","若 PEP 回到 9 百萬以上，維持現判"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"共識上修訊號","cause":"方法變動","prior_field":null,"side_a":"近三月 FY1 共識上修 26.5%（10.58→13.38）","side_b":"7 月底快照的 FY1 很可能仍是 FY26（10.58 接近 FY26 調整後 EPS 10.76），10 月快照已切換為 FY27；最近兩份快照 FY1 −0.6%、FY2 0%、FY3 +0.4%","ruling":"採 B 側：26.5% 視為財年切換，不當作上修證據；共識實際修正約持平。","evidence_level":"兩份共識快照","settle_metric":"下一次快照的 FY2 共識修正","if_then":["若 FY2 共識下修超過 3%，視為賣方開始下修，停止加碼","若 FY2 上修超過 3%，作為上調 Bull 機率的依據"],"evidence_refs":[]},{"axis":"股價與基本面背離","cause":"價格變動","prior_field":null,"side_a":"市場面：26 週股價 −33%，自 8/1 引用價約 −45%，跌破 52 週與 104 週均線","side_b":"公司面：FY27 指引維持，商用航太訂單年增 25%，CEO 稱需求與價格展望都比上季更強","ruling":"不可調和，需要裁決。現在就賣的最強論證：市場可能先看到航太週期見頂或國防預算遞延的跡象，而本公司訂單資料只有口述百分比，出貨量也停止揭露，外部無法驗證；下殺原因事實表也未涵蓋。裁決：偏向公司資料，但不重押，以分批取代一次建足，並以 Q2 FY27 財報作為第一個決勝點。","evidence_level":"價格為已實現資料；基本面為公司口述","settle_metric":"Q2 FY27 商用航太訂單與 SAO 營業利益","if_then":["若 Q2 訂單續年增且 SAO 營業利益≥214，加第二批","若 Q2 訂單轉為年減或 SAO 營業利益<214，停止加碼並減碼至三分之二","若股價續跌但 Q2 數據完好，按計畫分批反買，不停損"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"SAO 調整後營益率守住 35%","type":"假設驗證","maps_to":"H1","metric":"SAO 調整後營業利益率（不含附加費）","threshold":"連 2 季低於 35%","action":"停止加碼","source_freq":"季報新聞稿，每季","date":"2027-01"},{"n":2,"text":"商用航太訂單維持年增","type":"假設驗證","maps_to":"H2","metric":"商用航太訂單年增率（法說口述）","threshold":"連 2 季年減","action":"停止加碼","source_freq":"法說，每季","date":"2027-01"},{"n":3,"text":"FY27 營業利益指引下緣不下修、擴產如期","type":"假設驗證","maps_to":"H3","metric":"FY27 營業利益指引、擴產進度","threshold":"指引下緣低於 850 或擴產延後逾 6 個月","action":"減碼至三分之二","source_freq":"季報新聞稿，每季","date":"2027-01"},{"n":4,"text":"SAO 營業利益未達指引下緣","type":"風險","maps_to":"R1","metric":"SAO 季營業利益對比當季指引","threshold":"Q2 FY27 低於 214（Q1 已低於原指引下緣 218）","action":"停止加碼","source_freq":"季報新聞稿，每季","date":"2027-01"},{"n":5,"text":"原料或關稅成本轉嫁失效","type":"風險","maps_to":"R4","metric":"SAO 調整後營益率年變動，且公司歸因於原料或關稅","threshold":"年減 3 個百分點以上","action":"減碼至三分之二","source_freq":"季報新聞稿與法說，每季","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#1"]},{"n":6,"text":"主要航太長約續約價格持平或下調","type":"Single Thing","maps_to":"single_thing","metric":"長約續約價格方向","threshold":"任一大型長約持平或下調","action":"減碼至半倉","source_freq":"法說，每季","date":null},{"n":7,"text":"Q2 FY27 財報確認後加第二批","type":"加碼","maps_to":"H1","metric":"SAO 營業利益與商用航太訂單","threshold":"SAO 營業利益≥214 且商用航太訂單續年增","action":"加第二批（目標部位三分之一）","source_freq":"季報新聞稿，每季","date":"2027-01"},{"n":8,"text":"恢復正常加碼節奏","type":"估值rearm","maps_to":"H2","metric":"Q2 FY27 SAO 營業利益與訂單，或週收盤價","threshold":"SAO≥214 且訂單續年增，或週收盤站回 104 週均線（約 317）","action":"恢復加碼至目標部位","source_freq":"季報與週線","date":"2027-01"},{"n":9,"text":"利益率與訂單同時反轉","type":"清倉","maps_to":"H1","metric":"SAO 營益率與商用航太訂單","threshold":"SAO 營益率連 4 季低於 32% 且商用航太訂單連 3 季年減","action":"清倉","source_freq":"季報新聞稿與法說，每季","date":null},{"n":10,"text":"FY27 實際營業利益未達指引下緣","type":"減碼","maps_to":"H3","metric":"FY27 全年營業利益","threshold":"低於 850 百萬美元","action":"減碼至半倉","source_freq":"年度新聞稿","date":"2027-07"},{"n":11,"text":"Q2 FY27 財報後複審","type":"複審日期","maps_to":"H1","metric":"整體論點","threshold":"財報公布後兩週內","action":"重跑判斷","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"SAO 調整後營業利益率（不含附加費）","bear_threshold":"連 4 季低於 32%","window":"FY27–FY29 每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"商用航太訂單年增率（法說口述）","bear_threshold":"連 3 季年減","window":"FY27–FY29 每季","source":"每季法說逐字稿","last_status":"ok"},{"metric":"FY27 全年營業利益","bear_threshold":"低於 850 百萬美元","window":"FY27（約 2027-07 下旬公布）","source":"公司年度新聞稿","last_status":"ok"},{"metric":"主要航太長約續約價格","bear_threshold":"出現持平或下調的續約","window":"2026-10 至 2028-06","source":"每季法說逐字稿","last_status":"ok"},{"metric":"擴產案完工時點","bear_threshold":"延後至 FY28 開始後逾 6 個月","window":"2027-07 至 2028-01","source":"公司新聞稿與法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"channel_business_model_shift#1","reason":"此事件是 FY2024 第三季 Latrobe 經銷單位 14.1 百萬美元商譽全額減損，距今逾兩年半，金額約為 FY26 營業利益的 2%；證據本身也註明不是 2026 年的通路轉型，10-K 同章節描述現行通路沒有結構變動。"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=8–10 月股價下跌約 45%，同期 FY27 營業利益指引維持，商用航太訂單年增 25%、結構件與通路年增 49%，空中交通量季增 14%，管理層對量價與 FY29 目標的信心上升。市場若擔心燃油價格壓抑航空需求，目前訂單資料並不支持；但市場下殺的完整原因事實表未涵蓋。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟡', val='🟡', moat_trend='→', week26=-33.32, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"Q2 FY27 財報（2027-01 下旬）SAO 營業利益≥214 且商用航太訂單續年增，或週收盤站回 104 週均線（約 317），任一成立即恢復正常加碼","exec_line":"既有持股續抱，不因回撤停損。新資金分三批：現價區先建三分之一；Q2 FY27 財報確認 SAO 營業利益≥214 後加第二批；週收盤站回 104 週均線後加第三批。Single Thing 發生即減碼至半倉。"},"reasoning":{"industry":"最新一季（Q1 FY27，季末 2026-09-30）營收 798.2 百萬美元（含附加費），GAAP 營業利益 196.4，營益率 24.6%；不含附加費的調整後營益率 30.9%。SAO 部門調整後營益率 37.7%，與上季紀錄持平。分部方面，SAO 營收（不含附加費）573.5、PEP 83.0，SAO 約占九成且貢獻幾乎全部利潤。終端以航太國防為主，FY26 約占營收 65%、年增 15%；醫療 FY26 年減約 21%，運輸年減約 11%。原料成本以附加費轉嫁給客戶。FY24–FY26 無單一客戶占營收或應收帳款 10% 以上。單點依賴在上游：部分關鍵原料來自政經不穩國家，且可能沒有替代來源。產業時鐘在擴張期：主機廠產率由 2026 年約 1,400–1,500 架往 2,100 架以上爬升，積壓訂單逾 16,000 架，客戶下單量仍低於現行產率，尚未過熱。供需持久性屬結構性偏持久：2019 年以來除生產力提升外無實質新增產能，合格鎳基超合金廠很少。反向因素是本公司擴產約 9,000 噸將於 FY28 初上線，ATI 也在加產能，2028 年後供給可逆性屬中等。另外，Q1 有效稅率 15.5% 含一次性股權獎勵稅務利益，單季 EPS 3.25 略被墊高。","moat":"護城河機制：鎳基超合金需逐一料號通過客戶認證，第三方稱新供應商需 18–36 個月（單一廠商報告，未經獨立驗證）；10-K 稱高價值產品的主要競爭者不到十家；航太業務多數在長約下。方向證據：Q1 FY27 法說 CEO 表示長約續約量增，但份額大致不變，沒有搶份額。價格力確實擴大，但來源是 2019 年以來無新增產能的供需缺口，屬可逆來源；本公司擴產約 9,000 噸將於 FY28 初上線，ATI 亦在擴產。同業利潤對照（TTM 至 2026-06）：營益率本公司 22.5%、ATI 15.2%、HWM 27.3%，對最接近的熔煉同業 ATI 高 7.3 個百分點。同業利差的歷史序列事實表未涵蓋，無法判斷擴大或收窄，因此不給擴大。產業態勢分三軸看：競爭面，ATI 與本公司同步加產能，埋下供給轉鬆的種子；結構面，航太積壓逾 16,000 架、產率目標再提高約 50%，結構轉好；其他面，關稅經附加費轉嫁，低價替代材料的風險則常態存在。整體裁決為雙向拉鋸。報酬持續期：當期稅後營業利益約 555 百萬美元（FY26 營業利益 702×(1−21%)）；投入資本事實表未涵蓋，ROIC 無法精算。增量報酬以擴產案估算：約 4 億美元投入換得 FY30 增量營業利益約 1.5 億，稅後約 30%；再投資率代理值約 35%；內生成長上界約 10.5%。","growth":"成長組成以價格為主，包括長約重訂與非長約價格續升；量受產能滿載限制，FY28 初擴產約 9,000 噸（約 2019 年出貨量的 7%）帶來加量，另有淨回購。三年共識 EPS 為 FY27 13.38、FY28 15.96、FY29 19.20，自 FY26 調整後 EPS 10.76 起算年化約 21%；共識家數事實表未涵蓋，營收共識來自 6 位分析師。內生上界約 10.5%（見護城河段），缺口約 11 個百分點。缺口歸因：利益率擴張約 8 個百分點（FY29 營業利益目標 1,200–1,300，對比 FY26 的 702，增幅遠高於營收共識的年增約 10%），淨回購約 3 個百分點。缺口可以歸因，但前提是價格續漲。跑道：以目標產率 2,100 架計，16,000 架積壓約可支撐 7–8 年。FY31 後能否續長，取決於新訂單、國防新平台，以及燃氣渦輪、半導體等第二曲線；目前只有管理層口述，沒有量化證據，因此給中。衰退信號亮一項（EPS 成長遠高於營收成長），FCF 轉換率有一年低於 0.75，列為觀察。","governance":"自由現金流÷淨利：FY24 0.96、FY25 0.76、FY26 0.68（年度財報序列），轉換率隨擴產資本支出下滑。Q1 FY27 營運現金流 52.8、資本支出 77.7，自由現金流 −24.8；CFO 說明是存貨季節性累積，下半年會回收，全年自由現金流指引 400–430 維持不變。SBC 6.4，占營收 0.8%。現金去向依序為擴產、回購（Q1 回購 133.9，用完舊的 4 億額度並啟用新的 10 億額度）、股息，最後才是併購（管理層稱優先序低）。淨負債 539.8，淨負債÷EBITDA 0.6 倍，2034 年前沒有債務到期。回購時點方面，Q1 期間股價至少有一段落在 476–521 區間（9/1 前份判斷價與 8/1 引用價），實際均價事實表未涵蓋。以 FY27 共識 EPS 計，買入收益率約 2.6–2.8%，要 10 年期公債殖利率低於約 0.8% 才算過關，因此判不過；若以現價 284.66 回購，收益率升到約 4.7%。","valuation":"現價 284.66，對 FY27 共識 13.38 的前瞻本益比 21.3 倍，對 FY28 為 17.8 倍、對 FY29 為 14.8 倍；PEG 約 1.0（三年共識 EPS 年化約 21%）。我相信前半，因為指引維持、訂單加速；不完全相信後半，因為 FY23 營益率只有 5.2%。近三個月 FY1 上修 26.5% 很可能是財年切換造成：7 月底快照的 FY1 仍是 FY26，10.58 與 FY26 調整後 EPS 10.76 相近，因此不當作上修證據；最近兩份快照之間，FY1 −0.6%、FY2 0%、FY3 +0.4%，共識實際上約持平。歷史分位：P/S 位於 4 個年度端點的 39.5 分位；本益比分位為 0，是因 FY23 盈餘低谷讓早年本益比失真，不採用。短期上檔：FY28 共識 15.96 乘現行前瞻 21 倍約 335，約 +18%。中期上檔：Base 終端約 426，約 +50%。成長熄火測試三案（FY29 後成長降到 15%、10%、5%，終端本益比分別 17、15、12 倍）中，兩案終端價高於現價，一案低於現價。","premortem":"最強的三個反證詳見反證紀錄。第一，航太週期反轉，疊加本公司與 ATI 的新產能在 FY29–30 上線，長約不再漲價，EPS 退回 FY26 水準。第二，獲利成長，但現金轉換率下滑，回購又在高價區執行。第三，市場半年下殺 33% 的原因事實表未涵蓋，可能有本包看不到的負面資訊。股價已跌破 52 週與 104 週均線（418、317），仍在 250 週均線 168 之上；RSI 11 屬極度超賣，但不構成進場理由。"},"plain":{"six":{"how_it_makes_money":"賺的是航太引擎、緊固件與結構件供應鏈的錢。錢卡在合格的真空熔煉產能與多年材料認證；產能已滿載，利潤擴大靠長約重訂價。","moat":"→ 穩定：認證門檻與合格供應商稀少的格局未變。目前價格力強，但主要來自供需缺口；份額持平，同業也在同步擴產。","growth":"🟡 中：五年內成長以價格為主、擴產加量約 7% 為輔；Y5 後的跑道取決於新訂單與第二曲線。","capital":"現金有一段被擴產吃掉，回購多在高價區執行；資產負債表穩健。","valuation":"中性。現價要求 FY29 營業利益接近管理層目標下緣，且之後利益率不大幅回落；前半我相信，後半只信一半。","how_wrong":"🟡：最可能看錯的地方，是把週期高點的價格力當成結構性的。"}},"decision_inputs":{"signal":"A","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"8–10 月股價下跌約 45%，同期 FY27 營業利益指引維持，商用航太訂單年增 25%、結構件與通路年增 49%，空中交通量季增 14%，管理層對量價與 FY29 目標的信心上升。市場若擔心燃油價格壓抑航空需求，目前訂單資料並不支持；但市場下殺的完整原因事實表未涵蓋。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"進場","prior_role":"核心","wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":284.66,"week26_return_pct":-33.32,"consensus_rev_3m_pct":26.47,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY1 分母落在公司指引區間內，不是一次性盈餘；利益率高檔的風險已放進 Bear 情境，不當作分母爭點。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉後國防預算明朗化","impact":"中","watch":"國防訂單是否轉為年增"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q2 FY27 財報與法說","impact":"高","watch":"SAO 營業利益是否≥214、商用航太訂單是否年增、長約續約價格"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"大型航太長約續約（一份已達原則協議、兩份談判中）","impact":"高","watch":"續約價格是否再上調"},{"date":"2027-07","date_precision":"month","type":"capacity","event":"擴產案完工，FY28 初開機","impact":"高","watch":"是否如期、在預算內"},{"date":"2027-07","date_precision":"month","type":"guidance","event":"FY27 全年結果與 FY28 指引","impact":"高","watch":"FY27 營業利益是否≥850、自由現金流是否達 400"}],"_projected_from":"v19"}
```
