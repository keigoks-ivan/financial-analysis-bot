你是 stock-analyst v20 的**散文層（prose）agent**，標的 MCK（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MCK　日期：2026-11-08　archetype：None　前份裁決：2026-05-25　A 核心候選 / 觀望偏進場（pullback 中）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1635B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（390B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（805B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（773B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（905B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（841B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1318B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2294B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4113B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3269B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1635           3755-5365      5 條（2–6 內）  
s3                  8000         390           5327-7610      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2483          8762-12517      5 條（2–6 內）  
s6                 11000         841          7111-10159      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1318           1527-2182      3 條（2–6 內）  
s10                 5000        2294           1894-2706      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3269           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3975B；至少需散文≈41.02KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−47
−28
−4%
0%
0.09%
0.321%
0.321
0.6
0.7
0.75
0.88
0.90
0.93
01
1
1.05
1.14
1.14%
1.23
1.26%
1.4%
1.40
1.44%
1.48
1.5
1.60
1.60%
1.65
1.66%
1.67%
1.80
02
2
2.25
2.5
2.5%
2.85%
2.9%
2.9
3%
3
3.07
3.2
3.5
3.5%
3.61%
3.67%
3.7%
3.9
04
4
4%
4.1%
4.27
4.3%
4.47%
5
05
5%
5.6%
6%
06
6
6.2%
6.5%
6.7
7
7.3%
7.3
8%
8
08
8.6%
8.8%
8.9%
9%
9
10%
10
10.4
10.6
11
11%
11.4
11.7%
12%
12
12.5
13
13%
13.0%
14%
14.0%
14
14.5
15%
15
15.2%
15.9%
16%
16.6
17
17.3
17.7
18%
18
18.5%
18.52
19
19%
19.55
20%
20
20.4
20.5
20.95
21%
21
22%
22.5
23
23%
23.06
23.75
24%
24
25
26%
26
27.36
28%
29.47
30%
30
31
34
34%
38.5%
38.98
39
41%
42
42.2%
44%
44.20
44.4%
44.43
44.66
45
45.5
45.60
46
46.40
46.74
47%
47
48
49%
49
50%
50
50.63
51
52
52%
53.6
54.1
54.5
54.7
55
57.72
58.5
60%
63.5
65
65.5
69
70
72.5
73%
73.5
75%
80
84.5
88%
90%
90
93.5
96%
96.5
97.0%
100%
100
104
114%
116.5
116.7
121%
129%
141
149.8
150%
159%
160
250
340
530
563
621
700
734.5
764
766
766.08
767
800
812
818
860
914
920
999
1060.84
2024
2026
2027
2028
2032
20261108
1,000
1,060.84
1,092
1,109.57
1,199
1,200
1,300
1,600
2,316
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
{"meta":{"ticker":"MCK","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"McKesson Corporation"},"oneliner":"配送三強中營益率最高，專科藥與營運槓桿推動 FY27 調整後 EPS 年增 17–19%；但 26 週股價漲 44%，多數來自倍數由約 17 倍升到 23 倍。現價要賺年化 12%，五年 EPS 需年化約 15%，生意好，價格等回到 920 美元以下再談。","thesis":{"H":[{"id":"H1","text":"北美藥品配送的獲利成長持續快於營收，靠專科藥組合與營運槓桿，不靠藥價。","2y":"FY28 北美藥品營業利益年增 ≥10%（FY27 財測 14–18%）","5y":"到 FY32 營業利益年化 ≥8%","10y":null,"threshold":"單季營業利益年增 ≥10%；營業費用占毛利比率年改善","source":"每季新聞稿與法說逐字稿的分部數字","drift_rule":"TTM 年增偏離門檻 5% 以上連 2 季為削弱；偏離 10% 以上連 3 季為反轉"},{"id":"H2","text":"腫瘤與多專科平台成為第二成長引擎，營業利益占比持續上升。","2y":"FY28 營業利益年增 ≥15%，利益率 ≥2.5%","5y":"FY32 占分部營業利益 ≥30%（現約 21%）","10y":null,"threshold":"單季營收年增 ≥15%；利益率 ≥2.5%","source":"每季財報分部損益；有機成長未揭露，列資料缺口","drift_rule":"TTM 偏離門檻 5% 以上連 2 季為削弱；偏離 10% 以上連 3 季為反轉；利益率低於 2.5% 直接反轉"},{"id":"H3","text":"併購與回購能轉成每股現金成長，調整後 EPS 達長期目標，FCF 跟得上。","2y":"FY28 調整後 EPS ≥51 美元，FCF 對調整後淨利 ≥90%","5y":"FY32 調整後 EPS ≥80 美元；PMG 第三年底增益 ≥1.60 美元","10y":null,"threshold":"FCF 對調整後淨利 ≥90%；PMG 第三年底增益 ≥1.60 美元","source":"新聞稿 FCF 與 EPS、併購進度揭露","drift_rule":"TTM 偏離門檻 5% 以上連 2 季為削弱；偏離 10% 以上連 3 季為反轉"}],"R":[{"id":"R1","text":"大客戶集中：前十大占營收約 73%，CVS 已續約到 2032 年，其餘大客戶到期日不明，條件轉差比流失更可能。","h_ref":"H1","clock":"🔥","threshold":"任一前三大客戶流失，或 10-K 揭露前十大占比單年降 3 個百分點以上；OptumRx 合約變動公告立即重評（保留前份門檻）","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R2","text":"藥價政策：IRA、WAC 下降與 340B 回扣制可能改變服務費基礎或客戶行為。兩季實績未傷營業利益，但 2028 年的 IRA 價格與 340B 後的客戶行為都未知。","h_ref":"H1","clock":"🔥","threshold":"管理層改口稱對營業利益有重大影響，或北美藥品營業利益年增連 4 季低於 10%","evidence_refs":["supply_demand_durability#2","end_markets#2"]},{"id":"R3","text":"藥廠直連與自建通路擴大，壓縮配送環節。","h_ref":"H1","clock":"🐢","threshold":"直連占 GLP-1 處方達 30%（保留前份門檻，資料缺口）；專科藥利益率連 4 季下滑超過 50 個基點（保留前份門檻）；GLP-1 配送營收連 2 季環比下滑且產業量未降","evidence_refs":["channel_business_model_shift#2","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"醫材分拆執行失敗、延後，或分拆條件傷害每股價值。","h_ref":"H3","clock":"⚡","threshold":"分拆延後 6 個月以上，或 Apollo 公開退出，或財報重編，立即重評（保留前份門檻）","evidence_refs":[]},{"id":"R5","text":"關稅與上游原料依賴海外造成供應中斷或成本上升。海外業務僅約 4%，曝險在學名藥上游，公司自身曝險未量化。","h_ref":"H1","clock":"🔥","threshold":"合併毛利年增率低於營收年增率連 2 季，且管理層歸因關稅或採購成本","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R6","text":"鴉片相關私人原告訴訟仍有數百件，另有 False Claims Act 案；金額與時點事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"新增和解或準備達 10 億美元減碼，出現刑事程序清倉","evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"id":"R7","text":"PMG 與 Option Care 跨入新領域，整合與報酬未驗證；Option Care 由 CD&R 主導，公司只有少數股權。","h_ref":"H3","clock":"🔥","threshold":"PMG 第三年底增益低於 1.60 美元，或 FY28 再有 20 億美元以上跨入新領域的併購且 PMG 進度落後","evidence_refs":[]}],"single_thing":{"description":"前三大客戶中任一家不續約或大幅降價轉單。CVS（約 24%）已續約到 2032 年 6 月，剩下的是占營收 11% 與 10% 的兩家，名稱與到期日事實表未涵蓋。","why_fatal":"這是單一事件中對 EPS 敏感度最大的一項。以北美藥品平均利益率約 1.14% 粗估，失去 11% 營收的客戶約少 5 億美元營業利益、每股約 3.5 美元，約占 FY27 EPS 的 8%。單客實際利潤率未揭露，可能偏離平均。","if_happens":"EPS 下修約 8%，倍數同步下移，股價先看跌 25–30%。立即減碼至半倉，兩季內未由新客戶補回則清倉。","how_monitor":"8-K、每年 10-K 客戶集中度揭露、法說中的續約與客戶異動說明。","probability":"12–24 個月約 10%，屬主觀估計：CVS 已續約是有力反證，其餘兩家到期日未知。"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.95,"peg_fy2":1.5,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":38.98,"FY2027E":44.66,"FY2028E":50.63,"FY2029E":57.72},"fy_end_month":3,"eps_basis":"調整後稀釋 EPS，財年截至 3 月。FY2026A 事實表未直接收錄，由 FY27 財測 45.60–46.40 美元與年增 17–19% 回推；FY2027E 至 FY2029E 為財報前 Koyfin 共識，FY2027E 已低於新財測下緣。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MCK_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"低毛利、需求跟處方量走，靠營運槓桿與回購把個位數營收成長放大成雙位數 EPS 成長。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：處方量穩定成長，專科新藥推動需求，同店就診人次為近幾季高點（2026-11-04 逐字稿）。GLP-1 單季有波動，配送供給由三家寡占，可逆性低。","bargaining":{"up":"品牌藥以服務費為主，藥廠有直連通路可選，目前規模未見量化。","down":"前十大客戶占營收約 73%，議價權偏客戶；CVS 同時與 Cardinal 延約到 2032 年。","geo":"海外約占營收 4%，風險集中在學名藥上游原料依賴海外與關稅。"},"profit_pool_dir":"公司內部利潤往專科藥、腫瘤網絡與可及性服務移動；產業五年利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表沒有市場規模、滲透率與五年利潤池占比，本輪不補，成長判斷改靠分部實績與公司財測。"}},"moat":{"mechanism":"全國藥品配送規模與服務可靠度，加上社區腫瘤網絡與處方流程連線形成的轉換成本。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"營益率在三強最高，第二季營運槓桿延續；CVS 維持與 Cardinal 雙供應，份額方向無資料，直連通路尚未量化，兩邊都不足以改變方向。","peer_na_reason":"同業 ROIC、市占與投入資本事實表未涵蓋，本輪只能比較利潤率，不判斷報酬率差距。","threats":[{"level":"🟡","text":"藥廠直連病患平台把部分處方移出批發通路。目前只有產業文章，未量化對批發商的影響；同期 GLP-1 配送營收仍年增 26%。","p":"30%","evidence_refs":["channel_business_model_shift#2","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"10-K 自承部分對手與新進者在資料分析與 AI 上經驗更多。受影響的是處方科技段，實體配送不受影響。","p":"20%","evidence_refs":["competitive_share_entrants#1","substitute_technology#1"]},{"level":"🟡","text":"大型連鎖、付款方或藥廠自建供應管理能力，取代部分配送服務。","p":"15%","evidence_refs":["substitute_technology#0","customer_second_source#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"用藥屬必需，使用者、開立者與付款者三方都成立。第二季處方量成長，腫瘤網絡同店就診人次為近幾季高點。"},{"item":"決策層級","level":"🟡","text":"決策單位是連鎖與醫療體系的整約，前十大客戶占營收約 73%。合約長達數年，轉換成本高，但 CVS 同時用兩家供應商，替代性在合約層真實存在。"},{"item":"價值鏈分配","level":"🟡","text":"配送只拿約 3.7% 毛利，品牌藥服務費與 WAC 下降脫鉤的情況已維持兩季。藥廠直連與下游議價是兩端的壓力，專科段拿到的比例較高。"},{"item":"社會容忍度","level":"🟡","text":"藥價、透明度與 340B 仍是國會議題，FTC 與 HHS 2024 年曾就批發商對學名藥短缺的影響徵詢意見，之後無進一步行動。配送營益率僅 1.67%，並非政治焦點的主要利潤池，鴉片訴訟則顯示社會責任成本存在。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"投入資本、折舊與營運資金變動都未收錄，當期 ROIC、增量報酬與內生成長上界無法計算，不估。象限依 1.67% 營益率與配送業性質判斷，周轉率未計算。唯一可見的增量報酬是管理層對 Precision Medicine 的預估：22.5 億美元換第三年底每股增益 1.60–1.80 美元，以 116.5 百萬股計，稅後約 8.8%，含綜效、尚未實現。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","MCK":3.67,"CAH":3.9,"COR":4.12,"HSIC":31.59,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","MCK":1.67,"CAH":1.26,"COR":1.44,"HSIC":5.79,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","MCK":1.64,"CAH":1.9,"COR":0.47,"HSIC":3.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"CAH","gm":3.9,"om":1.26,"fcf_margin":1.9,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"COR","gm":4.12,"om":1.44,"fcf_margin":0.47,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"HSIC","gm":31.59,"om":5.79,"fcf_margin":3.64,"period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"營收成長（量與專科組合）約 7 個百分點，淨回購約 3–4 個百分點，併購約 1 個百分點，營業利益率擴張約 2–3 個百分點。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊與營運資金變動事實表未涵蓋，內生上界無法計算。保守處理為共識成長超出內生上界，因為 EPS 成長中至少 3–4 個百分點來自回購，不屬於營運再投資。","segments":[{"item":"北美藥品","value":"第二季營收 914 億美元，年增 6%；營業利益約 10.4 億美元（回推），年增 22%；FY27 財測營收 +5–9%、營業利益 +14–18%。"},{"item":"腫瘤與多專科","value":"第二季營收 149.8 億美元，年增 24%；營業利益 4.27 億美元，年增 8%，排除去年利得後 23%；FY27 財測營收 +20–24%、營業利益 +18–22%。"},{"item":"處方科技","value":"第二季營收 15 億美元，年增 10%；營業利益 3.07 億美元，年增 18%；FY27 財測營收 +2.5–6.5%、營業利益 +11–15%。"},{"item":"醫材","value":"第二季營收 31 億美元，年增 5%；營業利益 2.25 億美元，年減 10%；FY27 財測營收 +1–6%、營業利益 −4% 到持平。"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"第二季毛利年增 10%，高於營收 8%。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"市占事實表未涵蓋，未見流失證據。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"配送業不適用。"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"差約 6.7 個百分點，主要由回購、利益率與 WAC 下降造成。"},{"signal":"FCF 對淨利連 2 年低於 0.75","lit":false,"note":"FY26 約 1.14，FY27 以調整後淨利估約 0.88。"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"金額事實表未涵蓋，稀釋股數持續下降。"},{"signal":"市場萎縮或被替代技術壓縮","lit":false,"note":"處方量成長，直連影響未量化。"},{"signal":"產業倍數近 3 年系統性下移","lit":false,"note":"自身倍數處於四個年度端點最高位。"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"第二季資本支出 1.23 億美元，FCF 29.47 億美元。"},{"signal":"停止投資且營收下滑","lit":false,"note":"持續投資，營收成長。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"回購","value":"FY27 計畫約 50 億美元，上半年 34 億美元，均價約 818 美元。"},{"item":"併購","value":"Precision Medicine Group 約 22.5 億美元，現金支付，2026 年 11 月完成。"},{"item":"少數股權投資","value":"Option Care Health 49% 約 14 億美元，預計 2027 上半年完成，權益法認列，財測未計入。"},{"item":"股息","value":"殖利率 0.321%，約 3.9 億美元（殖利率乘市值）；2026 年 8 月調升 15%。"},{"item":"外部資金","value":"Apollo 以約 12.5 億美元取得醫材段約 13% 少數股權，FY27 少數股東損益財測 2.9–3.2 億美元。"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"歷年併購的已實現增量報酬事實表未涵蓋；PMG 管理層預估第三年底稅後約 8.8%，含綜效、未實現；資金成本事實表未涵蓋。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"上半年回購均價約 818 美元，以 FY27 財測中點 46 美元計盈餘殖利率約 5.6%；10 年期公債殖利率事實表未涵蓋，無法比較。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"第二季稀釋加權股數 116.7 百萬股，年減 6%，淨股數持續下降；SBC 金額事實表未涵蓋。","grade":"過"}]},"valuation":{"basis":"FY1 前瞻本益比，以公司財測中點 46 美元為分母；同業倍數事實表未涵蓋。","tier":"美國藥品配送三強","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業前瞻本益比，不自行補數；倍數改以自身 26 週前約 16.6 倍與現值 23.06 倍對照。"},"peg":1.65,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 約 23.06 倍，對三年 EPS 年化 14.0% 的 PEG 為 1.65，介於合理區間偏上。基本情境股價年化約 8.6%，加股息約 8.9%。PEG 未破 2 且基本情境仍有正報酬，所以不列最貴一級。短期目標：FY28 基本 EPS 52 美元乘 21 倍，1,092 美元，上行 2.9%。中期目標：FY29 基本 EPS 58.5 美元乘 20.5 倍，1,199 美元，上行 13.0%。","upside_short_pct":2.9,"upside_mid_pct":13.0},"trap_analysis":{"verdict":"🟡","label":"一項衰退訊號亮燈，EPS 成長明顯快於營收，來源可解釋，目前不像價值陷阱。"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"前十大客戶占營收約 73%，WAC 下降與 IRA 定價壓力延續，340B 回扣制可能 2027 年 1 月上路，管理層承認不知道客戶會如何反應。第二季北美藥品獲利成長的來源正好是專科配送、醫療體系與策略客戶。","assumption":"北美藥品獲利成長維持高於長期目標，服務費不隨藥價政策重議。","consequence":"五年後虧 50% 最可能的路徑：政策在 2027–2028 落地，大客戶續約條件轉差，EPS 停在 50 美元，倍數跌到 10.6 倍，股價約 530 美元。情境樹空頭跌 34% 是較可能的版本。","ruling":"部分採納，放進 30% 空頭機率。與唯一致命點在客戶條件上部分重疊，政策路徑另以觸發條件監控。反駁點是 CVS 已續約到 2032 年，WAC 下降兩季未傷營業利益。","watch":"北美藥品營業利益年增率、340B 上路後醫療體系用量、2028 年 1 月 IRA 價格。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","supply_demand_durability#2","end_markets#2"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"FY27 EPS 財測本年度兩次上修，FCF 45–49 億美元沒動。資金轉向 PMG 與 Option Care，現價回購的盈餘殖利率約 4.3%，上半年均價 818 美元時約 5.6%。少數股東損益 FY27 財測 2.9–3.2 億美元。醫材約占分部營業利益 11%，分拆後 EPS 基期會變小。","assumption":"EPS 成長等於股東可拿到的現金成長。","consequence":"EPS 達標，但每股 FCF 只有 EPS 的八到九成，回購買到的股數變少，分拆後的 EPS 基期需要重算；共識是否已反映分拆事實表未涵蓋。","ruling":"採納。基本情境的 EPS 成長逐年降到約 10%，並以 FCF 轉換率作為第三個假設的檢驗。","watch":"FY27 FCF、每股 FCF、分拆條件與換股方式、PMG 增益進度。","evidence_refs":[],"fact_refs":["f_kpi5_free_cash_flow","f_dividend_yield_ttm"]},{"view":"價格已反映太多","evidence":"26 週股價漲 44.4%，FY1 倍數由約 16.6 倍升到 23.06 倍，同期 FY27 EPS 預期上修約 4%。現價高於多數財報前的賣方目標價。","assumption":"23 倍是專科轉型帶來的新倍數，不會回落。","consequence":"倍數回到 16.6 倍，即使 EPS 不變也跌 28%。賺年化 12% 需要五年 EPS 年化約 15.2%，等於要求長期目標上緣維持五年。","ruling":"採納。這是本次唯一的限制條件，價格回到 920 美元以下才重新進場。","watch":"股價對 FY28 基本 EPS 的倍數、FY28 財測區間。","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_price_at_dd","f_fwd_pe_latest","f_ma_w104"]}],"max_dd":{"lo":-47,"hi":-28,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 766.08 → 本次 1060.84（+38.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=766.08","side_b":"本次 price_at_dd=1060.84","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 766.08 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 766.08 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 766.08 美元：Bull 價 2,316、Bear 價 700，五年期望值 +97.0%，基準年化 15.9%，不對稱比 19.55","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 19.55。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 766.08 美元：五年期望值 +97.0%，基準年化 15.9%，不對稱比 19.55","side_b":"本次情境、股價 1,060.84 美元：五年期望值 +42.2%，基準年化 8.6%，不對稱比 2.9","ruling":"再換股價、情境不動：起點價上漲 38.5%，五年期望值少 54.7 個百分點，基準年化少 7.3 個百分點，不對稱比由 19.55 降到 2.9。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與進場訊號","cause":"價格變動","prior_field":["signal","val"],"side_a":"2026-05-25 股價 766.08 美元，估值中性，進場訊號 A，結論觀望偏進場。","side_b":"2026-11-06 股價 1,060.84 美元，FY1 約 23.06 倍，估值偏貴，進場訊號降為 B。","ruling":"前份之後股價漲 38.5%，EPS 預期上修約 4%，其餘是倍數由約 17.3 倍升到 23.06 倍。前份在 766 美元偏向進場事後看是對的，本次不翻成追價：基本面確實變好，但只解釋一小部分漲幅。","evidence_level":"事實表股價與公司財測","settle_metric":"股價對 FY28 基本情境 EPS 的倍數","if_then":["若股價續漲而 EPS 財測未再上修，則不追","若股價達 1,300 美元以上而財測未再上修，則減碼","若股價跌到 920 美元以下且北美藥品營業利益年增仍達 10%，則分批反買"],"evidence_refs":[]},{"axis":"價值陷阱判斷","cause":"新證據","prior_field":["trap"],"side_a":"前份判定無陷阱跡象。","side_b":"本次一項衰退訊號亮燈：共識 EPS 年化約 14.0%，營收年化約 7.3%，差約 6.7 個百分點。","ruling":"差距可解釋：第二季北美藥品營收受 WAC 下降拖累約 4 個百分點，其餘來自回購與利益率，所以只列輕度警示。前份摘要沒有逐項清點，無法確認當時是否已計入。","evidence_level":"事實表共識與逐字稿","settle_metric":"EPS 與營收成長差、FCF 轉換率","if_then":["若 FCF 對調整後淨利連 2 年低於 75%，則停止加碼","若成長差回到 5 個百分點內且 FCF 轉換率達 90%，則解除停止加碼"],"evidence_refs":[]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位為空。","side_b":"本次填入護城河方向持平、五年後跑道中等、公司類型為品質複利成長；本檔非循環股，循環位置留空；機率與最大回撤由情境樹產生。","ruling":"前份沒有留下數值，無從比較方向變化，不把本次數值視為基本面變動。","evidence_level":"無前值可比","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場門檻。","side_b":"股價 ≤920 美元（約 FY28 基本情境 EPS 17.7 倍，基本情境年化約 12%）。","ruling":"本次卡住的只有價格，重新進場條件因此是價格錨。門檻依基本情境 FY32 股價 1,600 美元回推。","evidence_level":"情境假設","settle_metric":"股價","if_then":["若股價 ≤920 美元且基本面未破，則分批反買","若 FY28 財測中點年增達 16%，則進場價上調到 1,000 美元"],"evidence_refs":[]},{"axis":"清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標。","side_b":"本次設五項：北美藥品營業利益年增連 3 季低於 5%、腫瘤段營收年增連 2 季低於 10%、前三大客戶流失、FCF 轉換率連 2 年低於 75%、直連占 GLP-1 處方達 30%。","ruling":"前份只有風險閾值，本次把會改變持股的條件寫成明確的清倉指標，保留前份直連 30% 的門檻。","evidence_level":"判斷設定","settle_metric":"五項指標","if_then":["若任兩項同時成立，則清倉","若僅一項成立，則減碼"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"前三大客戶中任一家不續約或大幅降價轉單。","ruling":"客戶事件是單一事件中 EPS 敏感度最大的一項；終端倍數敏感度更大，但不是單一事件，放在反證處理。","evidence_level":"10-K 客戶集中度與回推","settle_metric":"8-K 與 10-K 客戶揭露","if_then":["若事件發生，則減碼至半倉","若兩季內未由新客戶補回，則清倉"],"evidence_refs":["customer_second_source#0"]},{"axis":"北美藥品假設門檻","cause":"新證據","prior_field":["thesis.H1"],"side_a":"季 Rev YoY ≥ 10%；季 Pharma OI margin ≥ 1.4%；連 2 季 Pharma Rev YoY < 8% 削弱。","side_b":"單季營業利益年增 ≥10%，營業費用占毛利比率年改善。","ruling":"WAC 下降使北美藥品營收成長少約 4 個百分點，第二季營收年增 6%，按舊門檻已削弱，同季營業利益卻年增 22%，營收不再是合適指標。舊的 1.4% 利益率與回推的 1.14% 差距大，前份分部範圍可能不同，無法核對。","evidence_level":"2026-11-04 逐字稿","settle_metric":"北美藥品營業利益年增率","if_then":["若 TTM 年增連 3 季低於 5%，則清倉","若單季年增低於 10%，則停止加碼"],"evidence_refs":["end_markets#2"]},{"axis":"腫瘤段假設門檻","cause":"新證據","prior_field":["thesis.H2"],"side_a":"季 Oncology YoY ≥ 20%；OP margin ≥ 3%；連 2 季 YoY < 15% 削弱；OP margin < 2.5% 反轉。","side_b":"單季營收年增 ≥15%；利益率 ≥2.5%；FY28 營業利益年增 ≥15%。","ruling":"第二季營收年增 24%，利益率 2.85%，低於舊的 3% 但高於 2.5% 反轉線。專科配送放量會壓低利益率，所以門檻改看營業利益成長，反轉線保留。","evidence_level":"10-Q 與逐字稿","settle_metric":"腫瘤段營業利益年增率與利益率","if_then":["若利益率低於 2.5%，則減碼","若營收年增連 2 季低於 10%，則清倉"],"evidence_refs":[]},{"axis":"第三個假設改寫","cause":"方法變動","prior_field":["thesis.H3"],"side_a":"MedSurg 分拆 2027 完成，2027-06 前完成 spin；分拆延後 6+ 個月警戒，放棄則反轉。","side_b":"併購與回購轉成每股現金成長，FCF 對調整後淨利 ≥90%；分拆移到風險項，保留舊門檻。","ruling":"分拆進度正常，2027 年 1 月將以 Wellverse 名稱營運，對股東價值的主要爭點已轉到資本配置與現金轉換。","evidence_level":"2026-08-05 逐字稿","settle_metric":"分拆公告與 FCF 轉換率","if_then":["若分拆延後 6 個月以上，則停止加碼"],"evidence_refs":[]},{"axis":"EPS 上修而 FCF 未上修","cause":null,"prior_field":null,"side_a":"2026-08-05 Kenny Cheung 說營運資金改善有機會優於財測，並把 say-do ratio 當作標準。","side_b":"2026-11-04 EPS 財測再上調，FCF 財測 45–49 億美元不變，低於 FY26 的 54.1 億美元。","ruling":"性質：可調和，時間性差異未證、監測。先認定為季底日期與營運資金時點，預先設定連 2 個財年 FCF 低於調整後淨利 90%，時間性的說法即不成立。","evidence_level":"逐字稿與財報","settle_metric":"FY27 與 FY28 的 FCF 對調整後淨利","if_then":["若 FY27 FCF 低於 45 億美元，則停止加碼","若 FY27 FCF 達 55 億美元以上，則解除停止加碼"],"evidence_refs":[]},{"axis":"併購節奏","cause":null,"prior_field":null,"side_a":"2026-08-05 Brian Tyler 稱不預期 FCS 規模的併購，Kenny Cheung 稱會有一些小型併購。","side_b":"2026-08-25 宣布 22.5 億美元買 Precision Medicine，10 月再簽約以 14 億美元買 Option Care 49%；Brian Tyler 2026-11-04 表示 CRO 部分對公司是新業務。","ruling":"性質：可調和但要記一筆。摘錄只有片段，原話可能只針對診所類併購，無法判定改口。PMG 預估稅後約 8.8%，高於現價回購約 4.3%，但含綜效。Option Care 由 CD&R 經營，公司是少數股東，分析師提到的買下其餘股權選擇權管理層未正面回應。","evidence_level":"逐字稿摘錄","settle_metric":"PMG 第三年底每股增益","if_then":["若 FY28 再有 20 億美元以上跨入新領域的併購且 PMG 進度落後，則停止加碼","若 PMG 增益按進度且 FCF 達標，則維持 920 美元的進場價"],"evidence_refs":[]},{"axis":"長期目標與實際成長","cause":null,"prior_field":null,"side_a":"Kenny Cheung 2026-11-04 重申 EPS 長期目標 13–16%。","side_b":"FY27 排除一次項的 EPS 成長 19–21%，分析師直指長期目標過低，管理層未回答要怎樣才會回到目標內。","ruling":"性質：可調和。長期目標偏保守有依據，也可能只是壓低預期。基本情境取年化約 11.7%，低於長期目標；多頭 16% 等於上緣。","evidence_level":"2026-11-04 逐字稿","settle_metric":"FY28 財測 EPS 成長區間（約 2027 年 5 月）","if_then":["若 FY28 財測中點年增達 16%，則進場價上調到 1,000 美元並分批反買","若 FY28 財測中點年增低於 10%，則停止加碼並把進場價下修到 800 美元"],"evidence_refs":[]},{"axis":"WAC 與 IRA 對獲利的影響","cause":null,"prior_field":null,"side_a":"Kenny Cheung 2026-08-05 與 11-04 都說 WAC 下降只影響營收，品牌藥九成五以上是服務費。","side_b":"10-Q 與媒體指定價逆風延續；IRA 價格水準未知（2026-08-05 Brian Tyler），2028 年 1 月才生效。","ruling":"性質：程度差異。兩季實績支持管理層，但證據的時間窗沒有涵蓋 2028 年，不能說風險已解，裁定為不可判斷，要等 IRA 價格公布。","evidence_level":"10-Q 與逐字稿","settle_metric":"IRA 價格公布後北美藥品營業利益年增率","if_then":["若管理層改口稱對營業利益有重大影響，則減碼","若 2028 年兩季內營業利益年增仍達 10%，則解除此項警示"],"evidence_refs":["end_markets#2","supply_demand_durability#2"]},{"axis":"下半年北美藥品路徑","cause":null,"prior_field":null,"side_a":"2026-08-05 Brian Tyler 說學名藥有利因素提前，會犧牲後面季度。","side_b":"2026-11-04 北美藥品全年營業利益財測上調到 14–18%，第二季年增 22%，下半年加速投資。","ruling":"性質：可調和。財測已隱含下半年減速，第二季的強勁不能外推，這也是基本情境 FY28 只放 13% 的原因之一。","evidence_level":"逐字稿","settle_metric":"第三、四季北美藥品營業利益年增率","if_then":["若下半年年增低於 10%，則停止加碼","若下半年年增達 18%，則進場價上調到 1,000 美元"],"evidence_refs":[]},{"axis":"共識資料時點","cause":null,"prior_field":null,"side_a":"事實表 FY1 共識 44.66 美元，近 3 個月修正 0.09%，最近兩份快照修正 0%。","side_b":"2026-11-04 公司把 FY27 財測上調到 45.60–46.40 美元，共識已低於新區間下緣。","ruling":"快照早於財報反映，修正 0% 不代表賣方沒動作。情境樹起點改用財測中點，三年共識仍列舊值並註明過時；舊分母使前瞻本益比高估約 0.7 倍。","evidence_level":"事實表與新聞稿","settle_metric":"下一份快照 FY1 是否達 45.60 美元","if_then":["若下一份快照 FY1 仍低於 45.60 美元，則不追，先確認資料來源"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：三強格局未變，新進者與藥廠直連是慢變數，未見量化傷害。結構轉好：專科藥與社區照護需求持續，醫療體系與專科量帶動獲利。","side_b":"其他結構變數：340B 回扣制、IRA 2028、藥品關稅、Medicare GLP-1 Bridge 計畫都在變動。","ruling":"雙向拉鋸：需求結構轉好，政策軸變動中，競爭軸靜態。依據是 2026-11-04 逐字稿與 FY2026 10-K。","evidence_level":"公司揭露","settle_metric":"北美藥品營業利益年增率與 340B 上路後用量","if_then":["若 340B 上路後北美藥品營業利益年增連 2 季低於 10%，則停止加碼"],"evidence_refs":["channel_business_model_shift#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"EPS 連續上修，長期目標明顯保守，現價對 FY28 基本 EPS 約 20.4 倍；若 EPS 維持年增 18%，一年後倍數自然消化，前份 766 美元的經驗顯示等回檔可能等不到。","side_b":"現價要求五年 EPS 年化約 15.2% 才賺 12%，公司自己上半年的回購均價是 818 美元。","ruling":"不追。等待的代價是股價不回來就錯過，這個代價可以接受。為避免用過時 EPS 錨定，FY28 財測若夠強，進場價會上調。","evidence_level":"情境推算","settle_metric":"FY28 財測與股價","if_then":["若 FY28 財測中點年增達 16%，則進場價上調到 1,000 美元並分批反買","若股價續漲而財測未上修，則不追"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 920 美元以下，重新評估首筆進場","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤920 美元","action":"分批反買","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"北美藥品營業利益成長低於財測或假設門檻","type":"假設驗證","maps_to":"H1","metric":"北美藥品營業利益年增率","threshold":"FY27 全年低於 14% 或單季低於 10%","action":"停止加碼","source_freq":"每季財報","date":"2027-02","evidence_refs":["end_markets#2"]},{"n":3,"text":"腫瘤與多專科成長或利益率跌破門檻","type":"假設驗證","maps_to":"H2","metric":"腫瘤段營收年增率與利益率","threshold":"營收年增低於 15% 或利益率低於 2.5%","action":"利益率破線減碼，營收低於 15% 停止加碼","source_freq":"每季財報","date":"2027-02","evidence_refs":[]},{"n":4,"text":"FCF 持續落後 EPS","type":"假設驗證","maps_to":"H3","metric":"FCF 對調整後淨利","threshold":"低於 90% 連 2 個財年","action":"停止加碼","source_freq":"每年財報","date":"2027-05","evidence_refs":[]},{"n":5,"text":"340B 回扣制上路後醫療體系與專科用量轉弱","type":"風險","maps_to":"R2","metric":"北美藥品營業利益年增率","threshold":"上路後連 2 季低於 10%","action":"停止加碼","source_freq":"每季財報、政策公告","date":"2027-01","evidence_refs":["supply_demand_durability#2","end_markets#2"]},{"n":6,"text":"前三大客戶任一家不續約或大幅降價轉單","type":"Single Thing","maps_to":"R1","metric":"客戶揭露與營收占比","threshold":"任一前三大客戶流失，或 10-K 揭露占比單年降 3 個百分點以上","action":"減碼至半倉，兩季未補回則清倉","source_freq":"8-K、每年 10-K","date":null,"evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":7,"text":"再度發生嚴重藥品召回或 FDA 警告信，表示配送品質出問題","type":"風險","maps_to":"R1","metric":"Class I 召回或 FDA 警告信件數","throughput":null,"threshold":"12 個月內再有 1 件 Class I 召回或 1 封警告信","action":"停止加碼","source_freq":"FDA 公告","date":null,"evidence_refs":["major_events#3","product_recall_warning#0"]},{"n":8,"text":"鴉片相關訴訟出現大額新增準備或刑事程序","type":"風險","maps_to":"R6","metric":"新增和解或準備金額","threshold":"達 10 億美元減碼，出現刑事程序清倉","action":"減碼或清倉","source_freq":"10-Q 與 10-K 附註","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":9,"text":"關稅或供應中斷的成本未能轉嫁","type":"風險","maps_to":"R5","metric":"合併毛利年增率減營收年增率","threshold":"連 2 季為負，且管理層歸因關稅或採購成本","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"n":10,"text":"股價跌到 52 週線附近且假設未破，持有者可增加部位","type":"加碼","maps_to":"H1","metric":"股價與北美藥品營業利益年增率","threshold":"股價 ≤860 美元，且單季年增達 10%","action":"分批反買","source_freq":"每日收盤、每季財報","date":null,"evidence_refs":[]},{"n":11,"text":"股價繼續上行但財測未跟上","type":"減碼","maps_to":"H1","metric":"股價對 FY28 基本 EPS 倍數","threshold":"股價 ≥1,300 美元（25 倍），且 FY28 基本 EPS 未上修","action":"減碼","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":12,"text":"兩項以上清倉指標同時成立","type":"清倉","maps_to":"H1","metric":"清倉指標成立數","threshold":"五項中任兩項成立","action":"清倉","source_freq":"每季財報","date":null,"evidence_refs":[]},{"n":13,"text":"FY28 財測公布時複審情境與進場價","type":"複審日期","maps_to":"H3","metric":"FY28 EPS、FCF 與分部財測","threshold":"財測公布","action":"依財測中點年增調整進場價：達 16% 上調到 1,000 美元，低於 10% 下修到 800 美元","source_freq":"年度財報","date":"2027-05","evidence_refs":[]}],"kill_metrics":[{"metric":"北美藥品營業利益 TTM 年增率","bear_threshold":"低於 5%","window":"連 3 季","source":"每季財報分部數字","last_status":"ok"},{"metric":"腫瘤與多專科營收年增率","bear_threshold":"低於 10%","window":"連 2 季","source":"每季財報分部數字","last_status":"ok"},{"metric":"前三大客戶續約狀況","bear_threshold":"任一家流失或不續約","window":"事件發生即成立","source":"8-K、10-K 客戶集中度揭露","last_status":"unknown"},{"metric":"FCF 對調整後淨利","bear_threshold":"低於 75%","window":"連 2 個財年","source":"新聞稿 FCF 與調整後 EPS","last_status":"warning"},{"metric":"藥廠直連通路占 GLP-1 處方比例","bear_threshold":"達 30%（保留前份門檻）","window":"滾動 12 個月","source":"藥廠揭露；目前為資料缺口","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=44.43, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價 ≤920 美元（約 FY28 基本情境 EPS 17.7 倍，基本情境年化約 12%）","exec_line":"未持有者不追；股價 920 美元以下且基本面未破，分批建立首筆。已持有者續抱、停止加碼；股價 1,300 美元以上且財測未再上修則減碼。"},"reasoning":{"industry":"FY27 第二季營收 1,109.57 億美元，調整後營業利益 18.52 億美元，營益率 1.67%，毛利約 39 億美元，毛利率約 3.5%。北美藥品營收 914 億美元，營業利益由合併數回推約 10.4 億美元，利益率約 1.14%，占分部營業利益約 52%。腫瘤與多專科營收 149.8 億美元、營業利益 4.27 億美元，利益率 2.85%，占約 21%。處方科技營收 15 億美元、營業利益 3.07 億美元，占營收 1.4%，卻占分部營業利益約 15%。醫材營收 31 億美元、營業利益 2.25 億美元，占約 11%。錢卡在兩個節點：品牌藥九成五以上按服務費收取（2026-08-05 Kenny Cheung），所以 2026 年 1 月 WAC 下降使北美藥品營收成長少約 4 個百分點，營業利益沒有重大影響；專科藥通路與診所網絡的利益率則高於基礎配送。⚑單點依賴：CVS 占營收約 24%，次兩大客戶占 11% 與 10%，前十大約 73%。CVS 續約到 2032 年 6 月，管理層 2026-11-04 確認已計入財測，短期續約風險解除，集中度本身沒有變。","moat":"機制是全國配送網的規模成本，加上腫瘤網絡與嵌入開立處方流程的連線，支付方網絡涵蓋美國 96% 處方量。可證方向：MCK 營益率 1.67%，高於 Cencora 1.44% 與 Cardinal 1.26%；毛利率 3.67% 卻是三家最低，優勢來自費用效率，定價沒有優勢。第二季北美藥品營業利益年增 22%，營收年增 6%。同業 ROIC 與市占事實表未涵蓋，無法驗證差距是否擴大，所以不標擴大。反方向的可能：若三家的利益率差距只是專科組合的時間差，優勢可能比數字看起來窄。","growth":"FY26 調整後 EPS 約 38.98 美元，由 FY27 財測 45.60–46.40 美元與年增 17–19% 回推；到 FY29 共識 57.72 美元，三年年化約 14.0%。這組共識是財報前快照，FY1 的 44.66 美元已低於新財測下緣。共識營收 FY26 到 FY28 年化約 7.3%，EPS 比營收快約 6.7 個百分點。落差歸因：淨回購每年約 3–4 個百分點（第二季稀釋股數年減 6%，FY27 回購約 50 億美元，約占市值 4.1%）；PMG 第三年底 1.60–1.80 美元的增益，折合每年約 1 個百分點；其餘約 2–3 個百分點來自營業利益率擴張。現價回購每一美元買到的股數，比上半年均價 818 美元時少約 23%，這部分成長會降速。FY27 腫瘤段財測由營收 14.5–18.5% 上調到 20–24%，其中 PMG 貢獻未揭露。","governance":"FCF 對淨利的轉換率 FY23 到 FY26 分別為 129%、121%、159%、114%。FY27 財測 FCF 45–49 億美元沒有隨 EPS 上修，以調整後淨利約 53.6 億美元估算，轉換率約 88%。FY27 資金需求：回購約 50 億美元、PMG 22.5 億美元、Option Care 14 億美元、股息約 3.9 億美元，合計約 90 億美元；來源是 FCF 約 47 億美元與 Apollo 約 12.5 億美元，缺口約 31 億美元，若 Option Care 落到 FY28 則缺口約 17 億美元，靠現金與新債支應。季末現金 65 億美元是 PMG 付款前的數字，事實表淨負債 46.74 億美元要調高到約 69 億美元才反映現況。SBC 金額事實表未涵蓋。","valuation":"股價 1,060.84 美元，對 FY27 財測中點 46 美元是 23.06 倍；事實表的 23.75 倍用的是財報前共識 44.66 美元，分母已過時。26 週前股價約 734.5 美元，對當時財測中點 44.20 美元約 16.6 倍。這 26 週股價漲 44.4%，FY27 EPS 預期只上修約 4%，其餘都是倍數擴張。Trailing 本益比 27.36 倍位於四個年度端點的最高位，五年分位事實表未涵蓋。現價高於 FN2 目標價共識約 999 美元 6.2%，方向支持不追，但多數目標價早於本次財報，證據力有限；已知目標價區間 812–1,200 美元，高低比 1.48，分歧不大。反方向的可能：若 FY28 財測再度明顯高於共識，23 倍會比看起來便宜。","premortem":"推翻論點的路徑是 340B 回扣制與 IRA 價格落地後客戶行為改變，北美藥品成長回到低個位數，倍數回到 14–17 倍。法說迴避點：上一季 FCF 何時加速沒給時點；下半年北美藥品路徑沒給季度數字；340B 當時沒給數字，本季說不預期重大影響但也說不知道客戶會怎麼做；腫瘤段成長率 50% 與 15% 的不一致在原稿未更正。本季分析師問北美藥品要怎樣才會回到長期目標，管理層只重申目標。歷史最大回撤、鴉片訴訟金額與開庭時點事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"McKesson 賺的是藥廠與下游藥局之間的配送服務費，以及專科藥附加服務的錢。營收八成在北美藥品配送，獲利增量愈來愈靠專科藥、腫瘤網絡與藥品可及性服務。","moat":"護城河方向持平，等級 B：規模與服務可靠度鎖住三強地位，定價權受大客戶集中限制。","growth":"五年後跑道中等：核心配送成熟，腫瘤與專科是看得到的第二曲線，但有機成長未拆出，也沒有滲透率資料。","capital":"資本配置偏好但未驗證：回購紀律佳，今年重點轉向兩筆新領域投資，報酬要到 FY29–FY30 才看得出來。","valuation":"現價要賺年化 12%，以 20 倍終端倍數計，FY2032 EPS 要到約 93.5 美元，五年年化約 15.2%，接近管理層長期目標 13–16% 的上緣。未來兩年我相信做得到，五年都維持我不相信，估值偏貴。","how_wrong":"最可能看錯三處：把目前 14–22% 的北美藥品獲利成長當常態、低估政策落地的時間點、把 23 倍當新常態。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 920 美元以下；基本面沒有需要等的事件，卡住的是價格。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":1060.84,"week26_return_pct":44.43,"consensus_rev_3m_pct":0.09,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"第二季含淨稅務利益 1.05 億美元，約每股 0.90 美元，幾乎等於本季超出預期的 0.93 美元，是否已在共識內事實表未涵蓋。全年營業利益財測上調 3 個百分點，約可解釋全年 EPS 財測中點上調 1.40 美元，分母沒有爭議。稅率每升 1 個百分點，FY27 EPS 約少 0.6 美元。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"regulatory","event":"340B 回扣制可能上路","impact":"高","watch":"醫療體系與專科用量、客戶是否轉換通路"},{"date":"2027-01","date_precision":"month","type":"other","event":"醫材事業預計以 Wellverse 名稱營運，推進分拆","impact":"中","watch":"分拆方式、時程、對 EPS 基期的影響"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第三季財報（時間為預估）","impact":"中","watch":"北美藥品營業利益是否如預期減速、下半年投資幅度"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 第四季財報與 FY28 財測（時間為預估）","impact":"高","watch":"EPS 成長區間、FCF 財測、PMG 進度"},{"date":"2027-06","date_precision":"quarter","type":"other","event":"Option Care Health 49% 股權預計於 2027 上半年完成","impact":"中","watch":"股東與監管核准、權益法收益"},{"date":"2028-01","date_precision":"month","type":"regulatory","event":"IRA 相關價格生效","impact":"高","watch":"價格水準、管理層對營業利益影響的說法"}],"_projected_from":"v19"}
```
