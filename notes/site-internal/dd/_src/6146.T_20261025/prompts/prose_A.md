你是 stock-analyst v20 的**散文層（prose）agent**，標的 6146.T（2026-10-25）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6146.T_20261025/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：6146.T　日期：2026-10-25　archetype：None　前份裁決：2026-05-22　A 級核心候選：FY25 actual +11.1% revenue / +10.9% OI / OPM 42.3% 六連年創高；FY26 cumulative shipment ¥438B guide + Q1 FY26 +14% YoY 加速；S 級護城河 10/10、dicing/grinding 65% 近壟斷 + 耗材 40% recurring；估值 PEG 3.07 (cycle base 偏差)盲點 1 救援後 🟡 合理；建議分批進場，等回測 BB 中軌 ¥68,377 或 W52 ¥53,225 後加碼。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1294B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（418B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（259B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（267B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（949B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（380B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（643B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1984B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3349B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1762B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1294           3994-5706      5 條（2–6 內）  
s3                  8000         418           5307-7582      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        1475          9468-13525      5 條（2–6 內）  
s6                 11000         380          7434-10620      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         643           2000-2857      5 條（2–6 內）  
s10                 5000        1984           2111-3016      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1762           2000-3238      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=2534B；至少需散文≈42.47KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−47%
−31.02
−31%
−30
−30%
−27%
−25.2%
−25%
0
0.06%
0.4%
0.43
0.6
0.73
0.75
0.81
0.85
0.87
0.88
0.9
0.97
1%
1
01
1.08
1.14%
1.14
2%
2
2.2%
2.5
3%
3
3.15
3.8
04
4
5%
05
5
6.0
6%
6
6.4%
7
7%
8
9
10%
10
10.8%
10.8
11%
11.4
12
14
14%
14.1%
15%
15.3
15.3%
15.4%
17
17.9%
18
20%
20
21.8%
22
22.56
22.6
25
25%
25.2%
26
28
28.4
28.43
30.5%
30.5
31%
31.8
32%
32.2%
33%
33.5
33.7
34.4
35
35%
36.3
36.3%
36.6%
38%
38.9%
40%
42
42%
42.3%
42.4%
43.9%
44%
45%
45
47%
47.4%
48%
49
50%
52
52%
55%
58%
60
60%
64.9%
70
70%
70.2%
70.6%
90
95
100
100%
104
108.43
108.64
150%
232
250
526
550
569
581
676
750
762.98
828.91
829
1249.84
1300
1450
1550
1650
1733.88
1800
1950
2025
2026
2027
2028
2029
2050
2184.95
2200
2350
2400
2750
3100
3500
6146
49290.0
65860
20261025
1,100
1,106
1,117
1,249.84
1,300
1,324
1,350
1,355
1,355.21
1,428
1,486
1,496
1,550
1,733.88
1,767
1,950
122,500
2,184.95
2,400
2,841
26,000
3,424
3,436
3,895
33,800
35,868
35,900
36,000
4,369
49,290
5,200
5,662
53,225
54,600
65,860
67,200
68,000
68,377
76,600
84,600
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
{"meta":{"ticker":"6146.T","date":"2026-10-25","schema":"v15.0","contract":"v19","company_name":"DISCO Corporation"},"oneliner":"DISCO 切割研磨設備約六到七成份額，最新一季營業利益率 47.4%、出貨額創新高；但股價半年跌 31% 後前瞻本益比仍約 28 倍，1–3 月共識偏高、現金轉換偏弱，等 2027 年 1 月實績確認再動手。","thesis":{"H":[{"id":"H1","text":"AI、HBM 與封測廠擴產讓單季出貨額維持在 1,300 億以上直到 FY2028","2y":"FY2028 前四季滾動出貨額≥5,200 億，年增≥10%","5y":null,"10y":null,"threshold":"四季滾動出貨額≥5,200 億，年增≥10%","source":"DISCO 季度出貨額公告與決算補足說明資料","drift_rule":"四季滾動出貨額連兩季偏離門檻 5% 以上為削弱，連三季偏離 10% 以上為反轉"},{"id":"H2","text":"份額與耗材讓營業利益率在完整循環內守在 40% 以上","2y":null,"5y":"五年滾動年度營業利益率≥40%","10y":null,"threshold":"年度營業利益率≥40%","source":"DISCO 決算短信與年報","drift_rule":"十二個月滾動營業利益率連四季低於門檻 5% 以上為削弱，連六季低於 10% 以上為反轉"},{"id":"H3","text":"切割研磨份額守住六成以上，雷射與電漿由自家吸收，不被本土廠取代","2y":null,"5y":null,"10y":"第三方份額估計≥60%，且中國本土廠未在先進封裝客戶量產","threshold":"份額估計≥60%","source":"第三方產業份額估計、公司地區別營收","drift_rule":"份額估計跨兩個年度下滑為削弱，跨三個年度下滑為反轉"}],"R":[{"id":"R1","text":"設備循環反轉：10–12 月營收與利益已指引季減，營運槓桿向下時利益掉得比營收快","h_ref":"H1","clock":"⚡","threshold":"單季出貨額連兩季年減","evidence_refs":[]},{"id":"R2","text":"中國約占營收 35%，出口管制或需求下修會直接砍掉一截營收","h_ref":"H1","clock":"🔥","threshold":"中國營收連兩季年減且占比下降超過 5pp，或管制公告","evidence_refs":["geo_supply_chain#2"]},{"id":"R3","text":"中國本土設備商在自給政策扶植下取得份額，或新加工技術取代刀輪耗材","h_ref":"H3","clock":"🐢","threshold":"主要客戶公開採用本土設備量產","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"id":"R4","text":"現金轉換偏弱、淨現金閒置，每股價值成長落後淨利","h_ref":"H2","clock":"🔥","threshold":"年度自由現金流÷淨利低於 0.6","evidence_refs":[]}],"single_thing":{"description":"日本或美國公告出口管制，涵蓋 DISCO 切割研磨設備對中國出貨","why_fatal":"中國約占營收 35%（二手資料），營運槓桿又高（邊際利益率近九成），營收少一成五到兩成就可能讓利益少三成以上，同時打破份額與耗材底盤","if_happens":"減碼至半倉並重跑研究；若管制擴及耗材則清倉","how_monitor":"經產省與美國商務部公告、公司公告、季度地區別營收","probability":"15%"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.56,"peg_fy2":0.87,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":1249.84,"FY2027E":1733.88,"FY2028E":2184.95},"fy_end_month":3,"eps_basis":"日本基準稀釋 EPS；共識取 yfinance 平均，FY2029 共識事實表未涵蓋，只有兩年"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6146.T_20261025/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"設備加耗材雙引擎，份額六成以上，營業利益率四成以上，需求隨半導體資本支出循環"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久到 2028 年：Wolfe 稱 2028 年前難見過剩，ASML 稱 2027–2028 年產能不足，SEMI 預估設備支出成長到 2028 年；2028 年後供給可逆性高","bargaining":{"up":"供應商集中度事實表未涵蓋","down":"第一大客戶 TSMC 約占 11%（二手資料），未見單一客戶超過四成；份額六到七成，對客戶議價強","geo":"中國約占營收 35%、產能八成以上在日本（二手資料），出口管制是最大的地緣議價風險"},"profit_pool_dir":"AI 封裝讓後段薄化與切割的工序增加，利潤池往這個節點流入；這是方向判斷，利潤池占比數字事實表未涵蓋","tam_table":{"expanded":false,"reason":"切割研磨設備的市場規模、滲透率與分段成長率事實表都未涵蓋；份額只有 Morningstar 60–70% 一個點估計，無法建時序表"}},"moat":{"mechanism":"份額六到七成加耗材重複購買加製程驗證換線成本","execution":9,"pricing":9,"grade":"A","trend":"→","trend_evidence":"年度營業利益率 FY2025 42.4%、FY2026 42.3%，毛利率 70.6%、70.2%，兩項都持平；份額只有單點估計，同業數字缺，無擴大證據，也無份額流失紀錄","peer_na_reason":"事實表同業財務整張缺，無法算報酬率差距；改用自身利益率軌跡與第三方份額估計判斷方向","threats":[{"level":"🟡","text":"中國自給政策扶植本土切割研磨設備商，可能侵蝕中國份額（約占營收 35%）","p":"20%","evidence_refs":["competitive_share_entrants#0","geo_supply_chain#2"]},{"level":"🟡","text":"雷射、電漿等新加工技術取代鑽石刀輪；公司兩條技術線都在自研，屬自我替代","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率待補（投入資本事實表未涵蓋，只能以營業利益率 42–47% 推定為高報酬）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"每片晶片都要經過薄化與切割，客戶延後購買等於延後量產；生成式 AI 相關出貨額由約 550 億增至約 750 億，最新一季出貨額 1,486 億創高"},{"item":"決策層級","level":"🟢","text":"替代性要在客戶產線的製程驗證層級衡量：設備一旦通過驗證，換廠就得重新認證，耗材也綁住裝機；換約流失率與認證週期的代理數字事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"切割研磨占客戶設備支出比例小但不可少，DISCO 拿到四成以上利益率；但第一大客戶約占 11%，中國約占 35%，本土替代與大客戶壓價會重新分配這段利潤"},{"item":"社會容忍度","level":"🟡","text":"沒有價格管制問題，但半導體設備是出口管制熱點；2026 年 8 月公司已出面否認新管制傳聞，中國商務部也把 20 家日本實體列入關注名單（是否包含 DISCO 未知），政治上限可能比經濟上限先到"}],"roiic":"約 48%（代理值）","reinvest_rate":"約 32%（代理值）","endo_ceiling":15.3,"formula_note":"增量報酬＝(FY2026 淨利 1,355 億−FY2023 淨利 829 億)÷FY2024–FY2026 留存再投資合計（淨利−自由現金流）1,106 億≈48%；再投資率＝1,106÷三年淨利合計 3,436≈32%；內生上界＝48%×32%≈15.3%。以淨利代替稅後營業利益，投入資本缺，所以是代理值，週期上行使它偏高估"},"combined":9.0,"score":9.0},"growth":{"driver_mix":"量為主（AI／HBM／封測廠擴產帶動出貨），價次之，無併購、無回購貢獻","runway_years":"事實表未涵蓋市場規模，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 48%×再投資率約 32%≈15.3%（代理值，週期上行偏高估）；共識兩年 CAGR 32.2% 超出上界，缺口歸因於利益率擴張與週期量能","segments":{"expanded":false,"reason":"設備、耗材、服務的分部營收與地區營收事實表未涵蓋；耗材占比是承重項，但無來源可展開，列為資料缺口"},"decay_signals":["自由現金流÷淨利連兩年低於 0.75（FY2025 0.43、FY2026 0.73）：亮","毛利率連兩季年減：季度毛利率事實表未涵蓋","EPS 年複合高於營收逾 5pp：FY2023–FY2026 為 17.9% 對 15.4%，未亮","替代技術壓縮市場：雷射與電漿由公司自研，未亮"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購（事實表無併購事件）；現金去向四分、股息總額與回購紀錄事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表無併購事件","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"FY2023→FY2026 稀釋股數 108.64→108.43 百萬股，淨回購每年約 0.06%，遠低於門檻","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"三年稀釋股數未增加，淨稀釋率≤0","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY1 共識）","peers":{"expanded":false,"reason":"事實表同業財務整張缺，無法建同 tier 對照；改以自身 trailing 本益比年度端點為錨"},"fwd_pe":28.4,"peg":0.88,"percentile_5y":30.5,"val_light":"🟡","val_light_derivation":"前瞻 28.4 倍、trailing 33.5 倍位於年度端點 30.5% 分位、PEG 0.88；但 FY1 分母隱含 1–3 月營收比 10–12 月指引高 33%，且最新一季利益率在週期高點，便宜論證不成立，判合理","upside_short_pct":10.8,"upside_mid_pct":36.3},"trap_analysis":{"verdict":"🟡","label":"週期高檔利益率加現金轉換偏弱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"中國約占營收 35%、產能八成以上在日本；中國自給政策可能扶植本土設備商；美國 232 關稅涵蓋半導體設備的可能性已被提及","assumption":"中國需求與份額可以維持，出口管制不會涵蓋切割研磨設備","consequence":"五年後虧損 50% 最可能的劇本：2028 年循環反轉，同時中國營收被管制或本土替代砍掉一截，營業利益率跌回三成多，倍數由 28 倍壓到 18 倍","ruling":"部分採納：熊市機率提高到 35%，出口管制列為唯一致命點；但目前沒有任何對手拿單紀錄，管制傳聞已被公司向經產省確認不實，不採為主情境","watch":"地區別營收中國占比、日美出口管制公告、中國本土設備商在先進封裝客戶的驗證消息","evidence_refs":["geo_supply_chain#2","competitive_share_entrants#0"],"fact_refs":["f_kpi0_gaap_jgaap"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流÷淨利 FY2025 0.43、FY2026 0.73；三年股數不變、幾乎不回購；淨現金 3,424 億","assumption":"需求兌現後現金會回到股東手上","consequence":"淨利照論點成長，但擴產吃掉現金、現金堆在帳上，每股自由現金流成長落後淨利，報酬率被現金稀釋","ruling":"採納：資本配置只給中等，長期信心上限設為中","watch":"FY2027 年報自由現金流÷淨利、股東回饋政策是否改變","evidence_refs":[],"fact_refs":["f_kpi4_cf_cf","f_kpi5","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"前瞻 28.4 倍建立在 FY1 共識上，而共識隱含 1–3 月營收約 1,767 億，比 10–12 月指引高 33%；最新一季營業利益率 47.4% 是週期高點","assumption":"共識分母正確，週期高點利益率可以延續","consequence":"FY1 EPS 若只有 1,550，真實前瞻倍數約 31.8 倍；利益率回到 42% 時，現價隱含的成長就要多撐一年以上","ruling":"採納：判定要等 1 月實績確認分母再進場；但股價已跌 31%，不採「價格已大幅高估」","watch":"2027-01 下旬 10–12 月實績與 1–3 月指引、FY1 共識修正幅度","evidence_refs":[],"fact_refs":["f_consensus_eps_fy1","f_rev_consensus_fy1_m","f_kpi7_4_12"]},{"view":"論點失敗","evidence":"公司風險揭露：若出現取代精密鑽石刀輪的新加工技術，業績可能受影響","assumption":"刀輪耗材的重複營收不會被雷射或電漿加工取代","consequence":"耗材底盤縮小，循環下行時沒有緩衝","ruling":"反駁為主：替代技術由 DISCO 自研，屬自我替代，份額未必流失；但耗材組成可能轉向利益率不同的產品，保留觀察","watch":"耗材營收占比與雷射切割設備出貨（事實表未涵蓋，需補）","evidence_refs":["substitute_technology#0"],"fact_refs":[]}],"max_dd":{"lo":-50,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 65860 → 本次 49290.0（-25.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=65860","side_b":"本次 price_at_dd=49290.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 65,860重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 65,860：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 65,860：Bull 價 122,500、Bear 價 36,000，五年期望值 +2.2%，基準年化 0.4%，不對稱比 1.08","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.08。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 65,860：五年期望值 +2.2%，基準年化 0.4%，不對稱比 1.08","side_b":"本次情境、股價 49,290：五年期望值 +36.6%，基準年化 6.4%，不對稱比 3.15","ruling":"再換股價、情境不動：起點價下跌 25.2%，五年期望值多 34.4 個百分點，基準年化多 6.0 個百分點，不對稱比由 1.08 升到 3.15。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：評級、陷阱風險、護城河趨勢","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份（2026-05-22）：評級 A、陷阱風險低、護城河趨勢向上","side_b":"本次：評級 B、陷阱風險中、護城河趨勢持平","ruling":"三項下修都來自新證據：FY2025、FY2026 自由現金流÷淨利連兩年低於 0.75；FY2026 年度毛利率與營業利益率和 FY2025 持平，找不到擴大證據；FY1 共識隱含的 1–3 月營收比公司指引高 33%，分母有爭議","evidence_level":"公司決算與年度財報","settle_metric":"2027-01 下旬公布的 10–12 月實績與 1–3 月指引","if_then":["若 10–12 月出貨額≥1,496 億且 1–3 月營收指引≥1,550 億，評級回到 A 的條件成立","若 FY2027 自由現金流÷淨利回到 0.85 以上，陷阱風險降回低"],"evidence_refs":[]},{"axis":"前份漂移：估值","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 65,860 日圓，估值合理","side_b":"本次股價 49,290 日圓（−25%），估值仍合理","ruling":"股價下跌本來會讓估值轉便宜，但 FY1 分母偏高、利益率處於週期高點，兩者抵銷，估值結論不變","evidence_level":"事實表股價與共識","settle_metric":"FY1 共識修正後的前瞻本益比","if_then":["若 FY1 共識下修後前瞻本益比仍低於 26 倍，估值改判便宜"],"evidence_refs":[]},{"axis":"前份漂移：前份空白欄位補上","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位都是空白","side_b":"本次補上：五年後跑道中等、品質複利成長帶循環屬性、中循環、多頭 20%／熊市 35%、最大回撤 −30%～−50%；定期定額本次未執行，仍空白","ruling":"屬方法補齊，不是基本面變化；熊市機率 35% 是因為共識成長超出內生上界","evidence_level":"方法","settle_metric":"無","if_then":["若下份研究共識成長回到內生上界以內，熊市機率可降到 25%"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"日本或美國公告出口管制，涵蓋 DISCO 切割研磨設備對中國出貨","ruling":"Single Thing 新設：中國約占營收 35%，是單一事件中衝擊最大的一項；2026 年 8 月的管制傳聞雖經公司確認不實，但顯示市場已在交易這個風險。發生時減碼至半倉並重跑研究","evidence_level":"二手地區占比與公司公告","settle_metric":"經產省或美國商務部公告","if_then":["若公告涵蓋切割研磨設備，減碼至半倉並重跑研究","若一年內無管制且中國占比持穩，致命點機率降到 10%"],"evidence_refs":["geo_supply_chain#2"]},{"axis":"行動門檻改寫","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"連 2 季 orders < ¥90B 或 book-to-bill < 0.9 → 預警；GM < 55% 削弱、連 2 季 < 52% 反轉","side_b":"單季出貨額連兩季低於 1,100 億 → 減碼一半；營業利益率連兩季低於 38% → 減碼；出口管制落地 → 減碼至半倉，管制擴大到耗材則清倉","ruling":"公司不公布訂單額與訂單出貨比，改用公司實際公布的出貨額；前份毛利率門檻 52–58% 遠低於實際的 70%，失去警示力，改用營業利益率","evidence_level":"方法","settle_metric":"每季出貨額與營業利益率","if_then":["若出貨額連兩季低於 1,100 億，減碼一半"],"evidence_refs":[]},{"axis":"重啟進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設；只寫等回測 BB 中軌 ¥68,377 或 W52 ¥53,225 後加碼","side_b":"2027-01 下旬實績：10–12 月出貨額≥1,496 億，且 1–3 月營收指引≥1,550 億","ruling":"前份的兩個價格錨都已跌破，但同時出現指引季減與分母爭議，所以改成事件錨，不再用價格錨","evidence_level":"公司指引","settle_metric":"2027-01 下旬決算","if_then":["若兩項同時達標，首筆小倉位 2%"],"evidence_refs":[]},{"axis":"出貨創新高，股價半年跌 31%","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：出貨額 1,486 億創高，10–12 月再指引 1,496 億；2028 年前產業供需偏緊；淨現金 3,424 億；股價已跌 31%，RSI 33.7，前瞻倍數已比 trailing 低 5 倍","side_b":"10–12 月營收與營業利益指引季減 7% 與 14%，利益率由 47.4% 降到 43.9%；FY1 共識隱含 1–3 月營收跳升 33%；營運槓桿向下時同樣大","ruling":"⚖ 不可調和的是時點，方向本身可以調和。選擇等待：硬數據點是 1 月實績能否證明 1–3 月營收真的跳升。股價先走、證據未到，不追","evidence_level":"公司指引與共識","settle_metric":"2027-01 下旬 10–12 月實績、1–3 月指引","if_then":["若 10–12 月出貨額≥1,496 億且 1–3 月營收指引≥1,550 億，首筆小倉位 2%","若股價跌到 250 週均線附近（約 35,900）而出貨額仍≥1,300 億，分批反買","反向：若出貨額連兩季低於 1,300 億，不追，停止任何加碼計畫"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#3"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：Wolfe 與 ASML 都指 2028 年前供給偏緊，SEMI 預估設備支出成長到 2028 年","side_b":"其他結構變數：中國約占 35%，本土替代論述與出口管制關注名單並存；競爭惡化目前只有通用論述，沒有拿單紀錄","ruling":"雙向拉鋸：需求結構轉好與地緣結構風險同時存在，競爭面靜態","evidence_level":"第三方產業預測與二手地區資料","settle_metric":"中國營收占比、管制公告","if_then":["若中國營收連兩季年減且占比下降超過 5pp，停止加碼"],"evidence_refs":["competitive_share_entrants#0","geo_supply_chain#2","supply_demand_durability#2"]},{"axis":"賣方目標價與現價","cause":null,"prior_field":null,"side_a":"賣方平均目標價 76,600–84,600 日圓，最低 68,000，都高於現價","side_b":"這些多是 7 月以前的快照，最高與最低差 3.8 倍","ruling":"目標價方向支持多方，但已過時而且分歧大，不作為進場依據，自身信心也不因此上調","evidence_level":"二手共識頁","settle_metric":"10 月決算後的目標價修正","if_then":["若決算後平均目標價下修超過 15%，熊市機率再加 5pp"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"10–12 月出貨額是否達公司指引","type":"假設驗證","maps_to":"H1","metric":"單季出貨額","threshold":"≥1,496 億日圓","action":"達標維持論點；低於 1,350 億列為削弱","source_freq":"公司季度決算","date":"2027-01","evidence_refs":["supply_demand_durability#3"]},{"n":2,"text":"重啟進場：出貨達標且 1–3 月營收指引證明共識分母成立","type":"估值rearm","maps_to":"H1","metric":"10–12 月出貨額與 1–3 月營收指引","threshold":"出貨額≥1,496 億且營收指引≥1,550 億","action":"首筆小倉位 2%","source_freq":"公司季度決算","date":"2027-01","evidence_refs":[]},{"n":3,"text":"價格先跌、基本面無損時分批反買","type":"加碼","maps_to":"H1","metric":"股價對 250 週均線，以及單季出貨額","threshold":"股價≤36,000 且出貨額≥1,300 億","action":"分批反買，每次 1%，上限 3%","source_freq":"每週","date":null,"evidence_refs":[]},{"n":4,"text":"日本或美國出口管制涵蓋切割研磨設備對中國出貨","type":"Single Thing","maps_to":"R2","metric":"經產省或美國商務部公告","threshold":"公告涵蓋 DISCO 產品","action":"減碼至半倉並重跑研究","source_freq":"事件","date":null,"evidence_refs":["geo_supply_chain#2"]},{"n":5,"text":"中國本土設備商在先進封裝客戶取得切割或研磨量產驗證","type":"風險","maps_to":"R3","metric":"本土設備商量產驗證消息","threshold":"任一主要封測廠或晶圓廠公開採用","action":"停止加碼","source_freq":"事件","date":null,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"n":6,"text":"週期利益率失守","type":"減碼","maps_to":"H2","metric":"單季營業利益率","threshold":"連兩季低於 38%","action":"減碼一半","source_freq":"公司季度決算","date":null,"evidence_refs":[]},{"n":7,"text":"年報複審現金轉換","type":"複審日期","maps_to":"R4","metric":"年度自由現金流÷淨利","threshold":"低於 0.6","action":"資本配置降級並重跑研究","source_freq":"年報","date":"2027-04","evidence_refs":[]}],"kill_metrics":[{"metric":"單季出貨額（公司公布）","bear_threshold":"連兩季低於 1,100 億日圓","window":"2027-01 至 2027-10 各季決算","source":"DISCO 決算短信與補足說明資料","last_status":"ok"},{"metric":"單季營業利益率","bear_threshold":"連兩季低於 38%","window":"未來四季","source":"DISCO 決算短信","last_status":"ok"},{"metric":"年度自由現金流÷淨利","bear_threshold":"FY2027 低於 0.6","window":"FY2027 年報（2027-04）","source":"年度現金流量表","last_status":"warning"},{"metric":"對中國出口管制","bear_threshold":"日本或美國公告涵蓋切割研磨設備","window":"持續","source":"經產省、美國商務部公告","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-31.02, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='A', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"2027-01 下旬實績：10–12 月出貨額≥1,496 億，且 1–3 月營收指引≥1,550 億","exec_line":"等 1 月實績：兩項都達標就建首筆 2%；股價跌到 250 週均線附近且出貨≥1,300 億，分批反買；出貨連兩季低於 1,300 億則不追"},"reasoning":{"industry":"最新一季（2026 年 7–9 月）營收 1,428 億日圓，營業利益 676 億，營業利益率 47.4%，出貨額 1,486 億創單季新高。公司指引 10–12 月營收 1,324 億、營業利益 581 億、利益率 43.9%、出貨額 1,496 億，也就是營收與利益季減，出貨仍創高。營收在客戶驗收後才認列，出貨額才反映客戶的投資意願。年度面（financial_history，FY2023→FY2026）：營收由 2,841 億增至 4,369 億，毛利率由 64.9% 升至 70.2%，營業利益率由 38.9% 升至 42.3%。營運槓桿很高：依指引，10–12 月營收季減 104 億，營業利益季減 95 億，向下時利益掉得比營收快。產業時鐘判在擴張期，依據是出貨額連季創高，以及 SEMI 預估晶圓製造設備 2027 年增 21.8%、2028 年增 14.1%，不是看股價。供需持久度判為結構性持久到 2028 年：Wolfe 與 ASML 都指出新廠房還沒蓋好，2028 年前難見過剩；但這仍是週期性擴張，2028 年後供給可逆性高。設備與耗材的分部占比事實表未涵蓋。單點依賴：第一大客戶 TSMC 約占 FY2026 營收 11%，中國約占 35%，兩者都是二手資料、未對照申報；製造產能八成以上在日本。","moat":"機制有三層：一是切割研磨設備約六到七成份額（Morningstar 2025 年估計）；二是刀片與砂輪耗材隨裝機量重複購買；三是製程經客戶驗證後，換供應商要重新認證。執行面判穩定：FY2025、FY2026 年度營業利益率 42.4%、42.3% 持平，最新一季 47.4% 屬週期高點，不能當成結構性擴大。定價面判穩定：毛利率 FY2025 70.6%、FY2026 70.2% 持平，較 FY2023 的 64.9% 已上一層。同業財務對照整張缺，無法驗證報酬率差距是否擴大，所以不給最高級，給 A，執行與定價各 9 分。威脅：中國自給政策可能扶植本土設備商，屬通用論述，尚無拿單紀錄；雷射與電漿加工可能取代刀輪，但兩者都在 DISCO 自家研發線上，屬點對點威脅，不扣分。再投資報酬用代理值估算：FY2023→FY2026 淨利增 526 億；同期留存再投資（淨利減自由現金流）合計 1,106 億，增量報酬約 48%；三年淨利合計 3,436 億，再投資率約 32%；內生成長上界約 48%×32%≈15.3%。淨利增幅大多來自週期上行與利益率提升，增量報酬偏高估。","growth":"成長以量為主（AI、HBM、封測廠帶動出貨），價格次之；沒有併購，也沒有回購貢獻。共識兩年 EPS 由 FY2026 實際 1,249.84 增至 FY2028E 2,184.95，年複合約 32.2%；FY2029 共識事實表未涵蓋。內生上界約 15.3%（見護城河段），缺口約 17pp，歸因於利益率擴張（營業利益率由 42.3% 升到最新一季 47.4%）加上週期性出貨量放大，不靠回購或收購，也不靠倍數重估。週期回落時這段缺口會反向。衰退信號亮一盞：自由現金流÷淨利 FY2025 0.43、FY2026 0.73，連兩年低於 0.75。其餘：季度毛利率事實表未涵蓋；FY2023–FY2026 EPS 與營收年複合 17.9% 對 15.4%，差 2.5pp，未亮；替代技術由公司自研，未亮。前份提的玻璃切割第二曲線，本包沒有任何證據，不採計。","governance":"稀釋股數由 FY2023 約 108.64 百萬股（淨利 828.91 億÷EPS 762.98）變為 FY2026 約 108.43 百萬股（1,355.21 億÷1,249.84），三年幾乎不變，沒有稀釋，但也等於沒有淨回購。自由現金流÷淨利 FY2023 0.81、FY2024 0.97、FY2025 0.43、FY2026 0.73，後兩年偏低，推測與擴產資本支出有關，但資本支出明細事實表未涵蓋。本年度上半期營運現金流 1,117 億，公司口徑自由現金流 569 億。總債務為零，淨現金 3,424 億，約占市值 6%。股息殖利率 1.14%，現金去向四分與回購均價事實表未涵蓋。","valuation":"前瞻本益比＝股價 49,290÷FY1 共識 1,733.88≈28.4 倍；FY2 為 22.6 倍；trailing 33.5 倍，位於 4 個年度端點的 30.5% 分位（不是五年連續分位）。PEG 以兩年共識年複合 32.2% 計約 0.88，表面便宜，但分母有爭議：FY1 共識營收 5,662 億減公司 4–12 月指引 3,895 億，隱含 1–3 月單季營收約 1,767 億，比 10–12 月指引 1,324 億高 33%。若 FY1 EPS 落在 1,550，前瞻本益比就是 31.8 倍。賣方平均目標價 76,600–84,600 日圓多為 7 月以前的舊快照，最高與最低差 3.8 倍，參考價值低。基準情境：一年後 FY2028E EPS 1,950×28 倍≈54,600（+10.8%）；五年後 FY2031E 2,400×28 倍≈67,200（+36.3%）。同業對照事實表缺，改以自身歷史倍數為錨。","premortem":"陷阱風險中等，依據見反證紀錄：衰退信號亮一盞（自由現金流轉換連兩年偏弱）；FY1 分母有爭議；10–12 月指引營收與利益季減；中國約占營收 35% 且是出口管制熱點。反方向的證據：出貨額仍創新高，2028 年前產業供需偏緊，無份額流失紀錄。"},"plain":{"six":{"how_it_makes_money":"DISCO 賺的是晶圓廠與封測廠「把晶圓磨薄、切開」這一步的錢，收入來自切割、研磨、拋光設備，加上隨用量消耗的刀片與砂輪。錢卡在後段薄化與切割這個節點；AI、HBM 與先進封裝讓這一步工序變多、難度變高。","moat":"護城河趨勢持平：份額與利益率都在高檔，但沒有同業數字能證明領先還在擴大。","growth":"五年後跑道中等：份額已有六到七成，成長要靠市場本身擴大而非滲透，本包內也沒有有來源的第二條成長曲線。","capital":"資本配置中等：股數三年持平沒有稀釋，但幾乎不回購，淨現金約 3,424 億閒置，現金轉換兩年偏弱。","valuation":"現價要求 FY2027、FY2028 兩年每股盈餘照共識各增三成左右，營業利益率守在四成以上。需求面我相信；共識隱含的 1–3 月營收跳升我不全信。估值合理，不便宜。","how_wrong":"最可能看錯的地方，是把週期高點的利益率與共識當成常態。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027-01 下旬實績：10–12 月出貨額≥1,496 億，且 1–3 月營收指引≥1,550 億，證明 FY1 共識分母成立","trap":"🟡","val":"🟡","moat":"A","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":49290.0,"week26_return_pct":-31.02,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY1 共識營收 5,662 億減 4–12 月指引 3,895 億，隱含 1–3 月營收 1,767 億，比 10–12 月指引 1,324 億高 33%；共識可能還沒反映 10 月 22 日的指引，前瞻本益比可能被低估"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"10–12 月決算與 1–3 月指引","impact":"高","watch":"出貨額是否≥1,496 億、1–3 月營收指引是否≥1,550 億"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"FY2027 年度決算與新年度指引","impact":"高","watch":"自由現金流÷淨利、營業利益率、股東回饋政策"},{"date":"2026-12","date_precision":"month","type":"macro","event":"SEMI 年末設備市場預測更新","impact":"中","watch":"2027、2028 年晶圓製造設備成長率是否下修"},{"date":null,"date_precision":null,"type":"regulatory","event":"日美對中國半導體設備出口管制動向","impact":"高","watch":"是否涵蓋切割研磨設備或耗材"}],"_projected_from":"v19"}
```
