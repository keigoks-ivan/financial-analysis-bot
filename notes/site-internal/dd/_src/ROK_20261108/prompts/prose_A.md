你是 stock-analyst v20 的**散文層（prose）agent**，標的 ROK（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROK_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ROK　日期：2026-11-08　archetype：None　前份裁決：2026-06-20　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1679B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（388B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1120B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1411B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1161B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（634B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（975B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2296B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4396B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3241B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1679           3725-5321      5 條（2–6 內）  
s3                  8000         388           5328-7612      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3692          7916-11308      5 條（2–6 內）  
s6                 11000         634          7256-10366      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         975           1768-2525      5 條（2–6 內）  
s10                 5000        2296           1893-2704      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3241           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4975B；至少需散文≈40.02KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45%
−45
−33%
−31%
−30
−30%
−20.7%
−17%
−16.68
−9%
−8.77%
−6%
−3.0%
0
0.11
0.20
0.5
0.75
0.8
0.97
1
1.1
1.12
1.3
1.4%
1.47
1.5
1.5%
1.6
1.72
1.97%
02
2%
2
2.24
2.5
2.6%
2.96
3%
3
3.8
3.97%
4%
04
4
4.5
4.5%
4.8
4.8%
4.95%
05
5
5%
5.3
6
6%
06
6.2%
6.5%
6.75
7%
07
7
7.5%
7.7%
7.8
8%
08
8
8.28
8.5%
9
9%
9.6%
10%
10
11%
11
11.25%
11.4
11.45%
11.6%
11.95
12%
12
12.69%
12.8
12.86%
13%
13
13.22
13.24
13.42
13.6
13.90
14
14.2
14.50
14.8
14.9
14.92
15.00
15%
15.5
16
16.4
16.4%
16.51%
16.67
17
18%
18
18.0
18.48
19
19.6%
19.6
19.74%
20%
20
20.4%
20.7%
20.8
21
21.2
21.5%
21.6%
21.9%
22%
22
22.2%
22.55
22.6
22.7%
22.8
23%
23.5%
23.7
24
24%
24.5%
25%
25
25.19
25.6
26%
26
26.6
27.2
27.3
28
28.0
28.01
28.86
30%
30
31%
31.4
32%
32
32.2%
33.8%
34%
35
42%
42
44%
45
46%
49
49.35%
50%
51
53.61%
65%
70
85
90
98.5
100%
100
107%
110.4
111.27
112
113%
120
139%
150%
156%
215
218
232
250
256
270
272
300
330
340
375.86
383
406.67
407
420
421
473.79
477
508.8
536
588
602
744.8
2026
2027
2028
20261108
1,752
10,132
2,071
2,818
3,119
4,185
8,989
9,074
9,575
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
{"meta":{"ticker":"ROK","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Rockwell Automation"},"oneliner":"ROK 的控制平台與利潤率兌現良好，但現價約 25 倍 FY2027 EPS，共識三年路徑沒有下行年，基準情境年化不到 8%，等 340 美元以下再進場。","thesis":{"H":[{"id":"H1","text":"工業自動化需求延續，FY2027 剔除關稅退款後的核心有機成長站穩中高個位數。","2y":"FY2027 核心有機成長 ≥ 6.5%，FY2028 ≥ 5%","5y":null,"10y":null,"threshold":"FY2027 核心有機成長 ≥ 6.5%；FY2028 ≥ 5%；資料中心加半導體 FY2027 達中十位數成長","source":"2026-11-05 法說（Moret、Rothe）與公司季報；口徑為報告有機成長扣掉 1 個百分點的客戶關稅退款基期效應","drift_rule":"TTM 連 2 季偏離門檻 ≥ 5% 為削弱，連 3 季偏離 ≥ 10% 為反轉"},{"id":"H2","text":"利潤率擴張來自生產力與產品組合，FY2031 Enterprise 營業利益率站上 24%。","2y":null,"5y":"FY2031 Enterprise 營業利益率 ≥ 24%","10y":null,"threshold":"FY2027 ≥ 23%（指引）；FY2029 ≥ 23.5%；FY2031 ≥ 24%；price/cost 全年為正","source":"公司季報與法說；投資人日將更新長期目標","drift_rule":"TTM 連 4 季偏離門檻 ≥ 5% 為削弱，連 6 季偏離 ≥ 10% 為反轉"},{"id":"H3","text":"Logix 的工廠控制標準地位十年內不被架構替代，軟體與 ARR 補上較穩定的收入。","2y":null,"5y":null,"10y":"Software & Control 利益率維持 30% 以上，Logix 仍是主要客戶的控制標準","threshold":"FY2027 有機 ARR 成長 ≥ 7%（指引）；Software & Control 利益率 ≥ 32%；有機成長不低於 Intelligent Devices","source":"公司季報、法說、年度 10-K 競爭段落；第三方份額事實表未涵蓋","drift_rule":"跨 2 個年度低於門檻為削弱，跨 3 個年度低於門檻為反轉"}],"R":[{"id":"R1","text":"工業資本支出循環回落或專案繼續延後，核心有機成長熄火。","h_ref":"H1","clock":"🔥","threshold":"核心有機成長連 2 季低於 5%","evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"id":"R2","text":"記憶體與 PCB 等電子料通膨，加上缺料，吃掉約 3 個百分點的漲價。","h_ref":"H2","clock":"⚡","threshold":"price/cost 連 2 季轉負，或剔除關稅退款後 Enterprise 營業利益率連 2 季低於 22%","evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"]},{"id":"R3","text":"Siemens／NVIDIA 工業 AI 作業系統與開放式自動化削弱 Logix 鎖定。","h_ref":"H3","clock":"🐢","threshold":"Software & Control 有機成長連 2 季低於 Intelligent Devices 且毛利率同比下滑","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"ARR 連續不及預期，軟體與服務的穩定收入沒有出現。","h_ref":"H3","clock":"🔥","threshold":"有機 ARR 成長連 2 季低於 5%","evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"id":"R5","text":"Section 232 機器人與工業機械關稅落地，轉嫁受競爭與合約限制。","h_ref":"H2","clock":"🔥","threshold":"關稅落地且當季 price/cost 轉負","evidence_refs":["reg_tariff_export#3","reg_tariff_export#1"]},{"id":"R6","text":"資料中心與半導體投資降溫，約 10% 營收的成長主題退潮。","h_ref":"H1","clock":"🔥","threshold":"合併垂直 FY2027 成長低於 10%","evidence_refs":[]}],"single_thing":{"description":"FY2028 之前出現連續兩季有機營收同比轉負的循環下行。","why_fatal":"這是數學上最大的單一敏感項。共識三年路徑沒有下行年；一旦發生，FY2028 EPS 由共識 16.67 美元落到約 12.8 美元，倍數同時降到 17 至 20 倍，股價約 218 至 256 美元。","if_happens":"第一季轉負先停止加碼，第二季確認後減碼至半倉，到 17 至 20 倍區間再分批買回；控制平台未受損就不清倉。","how_monitor":"每季有機成長、Lifecycle Services 訂單出貨比、管理層對機器製造商訂單的說法。","probability":"12 至 24 個月約 25%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":22.55,"peg_fy2":2.0,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":13.42,"FY2027E":14.92,"FY2028E":16.67,"FY2029E":18.48},"fy_end_month":9,"eps_basis":"Non-GAAP Adjusted EPS。FY2026A 為公司實際值，含 0.11 美元關稅退款淨利益；三年共識來自 2026-11-07 Koyfin 快照，EPS 家數事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROK_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利控制平台，獲利隨工業資本支出循環波動，FY2024 營收 −8.77%。"},"industry":{"clock_phase":"II","sd_verdict_source":"偏週期、結構為輔：資料中心與半導體約占營收 10%、FY2027 指引中十位數成長，屬結構性；其餘多數垂直仍看資本支出循環，事實表也沒有能區分再工業化結構性與週期性的 2027 至 2028 預測。","bargaining":{"up":"記憶體與 PCB 供應商議價力上升，Rothe 2026-11-05 說通膨未消退、PCB 供應偏緊。","down":"下游分散，但約 65% 經獨立經銷商，前兩大約占 20%。","geo":"北美是最快成長區，美國 FY2026 有機成長逾 12%；對墨西哥、加拿大、中國的進口受關稅政策影響。"},"profit_pool_dir":"公司內部利潤向控制器與軟體集中；產業層級的利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池占比，無法展開；這項缺口限制了跑道判斷，不代表不重要。"}},"moat":{"mechanism":"工廠與機器製造商把控制系統標準化在 Logix 與其軟體工具上，轉換成本來自重寫程式、重新認證與重訓人員，再由約 65% 銷售所經的獨立經銷網放大。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力擴大，定價權穩定，合併為方向穩定。沒有出現最大客戶份額下滑的具名證據，也沒有第三方份額佐證上升。","peer_na_reason":"同業 ROIC 事實表未涵蓋，改用毛利率與營業利益率比較，無法證明報酬差距擴大。","threats":[{"level":"🔴","text":"Siemens 與 NVIDIA 的工業 AI 作業系統試圖把決策層移到控制器之上，屬生態攻擊；ROK 也與 NVIDIA 合作，但主導權不在自己手上，AI 淨增量 ARR 也未揭露。攻擊者投入資本量級事實表未涵蓋。","p":"30%","evidence_refs":["competitive_share_entrants#3","substitute_technology#0"]},{"level":"🟡","text":"開放式自動化把軟體與硬體脫鉤；來源是 Schneider 自家專欄，採用率事實表未涵蓋，ROK 已把 Logix 放上開放運算平台應對。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"10-K 預期競爭維持高強度，可能限制份額與獲利，屬點對點競爭常態。","p":"常態存在","evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是控制工程師，決策者是廠方與機器製造商的標準制定者，付款者是資本支出預算。工廠提升生產力與韌性的問題長期存在，但購買可以延後：2026-11-05 Moret 說採礦等產業專案被延後而非取消，FY2024 營收 −8.77%。"},{"item":"決策層級","level":"🟢","text":"替代要以整座工廠或整個機型的控制標準為單位衡量，不是單顆控制器。QTS、Stryker、Vale 都是平台標準化案，換掉要重寫程式、重新認證與重訓。代理讀數只有 Logix 第四季 +25% 與管理層稱續約強勁，續約率與流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"約 65% 銷售經獨立經銷商，前兩大約占 20%，下游分潤穩定。上游的記憶體與 PCB 正在多拿：Rothe 2026-11-05 說通膨未消退、第一季最難，PCB 供應偏緊。AI 層若由運算平台主導，長期也會分走價值。"},{"item":"社會容忍度","level":"🟢","text":"產品賣給企業，不是民生必需品，也不靠監管授權，沒有政治定價上限。關稅退款後公司主動提列 85 百萬美元退給客戶，屬客戶關係管理，不是社會壓力。"}],"roiic":"20.4%（以 TTM ROIC 代理；投入資本逐年值事實表未涵蓋，真實增量報酬無法計算）","reinvest_rate":"≤21.9%（FY2027 資本支出約 383 百萬美元 ÷ NOPAT 約 1,752 百萬美元；折舊與營運資金事實表未涵蓋）","endo_ceiling":4.5,"formula_note":"單位為百分比。資本支出＝共識營收 9,575 百萬美元×指引 4%；NOPAT＝15.00 美元×110.4 百萬股＋利息 120 百萬美元×（1−20%）。內生上限＝20.4%×21.9%≈4.5%。把全部資本支出當成長性投入是刻意取高，FY2027 指引 FCF 轉換率 100% 也顯示淨再投資很少。可能看錯的方向：若增量報酬高於平均（Software & Control 增量利益率逾 50% 暗示有此可能），上限會被低估。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","ROK":49.35,"HON":38.04,"EMR":53.61,"PH":37.74,"ETN":35.05,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","ROK":19.74,"HON":16.2,"EMR":20.85,"PH":21.4,"ETN":17.32,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","ROK":16.51,"HON":4.95,"EMR":19.0,"PH":17.2,"ETN":11.87,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","ROK":7.89,"HON":5.37,"EMR":null,"PH":null,"ETN":2.75,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"HON","gm":38.04,"om":16.2,"fcf_margin":4.95,"rd_intensity":5.37,"strategy_note":"毛利率與營業利益率都低於 ROK，FCF 利潤率 4.95% 偏低，原因事實表未涵蓋，不宜直接比較現金品質。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"EMR","gm":53.61,"om":20.85,"fcf_margin":19.0,"rd_intensity":null,"strategy_note":"最接近的利潤率對照，毛利率與營業利益率都略高於 ROK，說明 ROK 的毛利優勢並非同業第一。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PH","gm":37.74,"om":21.4,"fcf_margin":17.2,"rd_intensity":null,"strategy_note":"毛利率低很多但營業利益率高於 ROK，營運效率是值得對照的標竿。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ETN","gm":35.05,"om":17.32,"fcf_margin":11.87,"rd_intensity":2.75,"strategy_note":"毛利率明顯低於 ROK，產品重疊主要在電力，直接競爭控制平台的證據事實表未涵蓋。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"FY2027 有機 6% 至 9%：價格約 3 個百分點，關稅退款基期 1 個百分點，其餘為量；無併購，回購貢獻 EPS 0.20 美元。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"沿用報酬持續期欄位：TTM ROIC 20.4%×再投資率上限 21.9%≈4.5%，是取高的上限。","segments":[{"item":"Intelligent Devices","value":"FY2026 營收 4,185 百萬美元，+11%；全年利益率 20%；FY2027 指引中個位數成長，利益率約 +100 個基點。"},{"item":"Software & Control","value":"FY2026 營收 2,818 百萬美元，+18%；全年利益率 33.8%；FY2027 指引高個位數成長，利益率小幅上升。"},{"item":"Lifecycle Services","value":"FY2026 營收 2,071 百萬美元，−6%，主因 Sensia；第四季有機 +2%、訂單出貨比 0.97；FY2027 指引有機低個位數成長，利益率約 +100 個基點。"}],"decay_signals":["亮燈：EPS CAGR 高於營收 CAGR 超過 5 個百分點（FY2026 至 FY2028 約 11.45% 對 6.2%）。","未亮：FCF／淨利連 2 年低於 0.75（FY2025 約 156%，FY2026 公司口徑 113%）。","資料缺口：毛利率季度同比、市占、SBC、維護性資本支出、產業倍數三年變化，事實表未涵蓋。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，且現金去向四分事實表未涵蓋，主要數字已寫在本題理由。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 沒有併購完成項目；歷史併購投入與回報事實表未涵蓋，無法計算。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"以現價算 FY2027 盈餘殖利率 3.97%（14.92÷375.86）；10Y 殖利率與回購均價事實表未涵蓋，但只有 10Y 低於 1.97% 才會過關，故判不過。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 金額事實表未涵蓋；目前股數 111.27 百萬股，FY2027 回購 6 億美元按現價約減 1.6 百萬股，年均約 0.8 百萬，與指引平均稀釋股數 110.4 百萬股相符，隱含淨發行接近零，低於 1.5%。","grade":"過"}]},"valuation":{"basis":"前瞻本益比與 PEG，Non-GAAP EPS 口徑","tier":"高品質工業自動化","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數；前份記載 EMR／Siemens 約 20 倍（2026-06-20）已過時，不足以展開。"},"fwd_pe":25.19,"peg":2.24,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 25.19 倍、PEG 2.24 偏貴，但基準情境已假設倍數由 28.0 倍降到 24 倍，仍有約 7.7% 年化，多空不對稱約 3 倍，結論為合理偏貴。五年分位事實表未涵蓋，不用年度端點代替。","upside_short_pct":7.8,"upside_mid_pct":22.6},"trap_analysis":{"verdict":"🟡","label":"成長靠漲價、利潤率與回購，再投資貢獻小"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY2024 營收 −8.77%、GAAP 稀釋 EPS 由 11.95 降到 8.28 美元；FY2027 指引明說未假設資本支出全面回升，Lifecycle Services 第四季有機僅 +2%、訂單出貨比 0.97。","assumption":"共識 FY2027 至 FY2029 每年 EPS 成長 10% 以上，沒有下行年。","consequence":"FY2028 EPS 落到約 12.8 美元、倍數降到 17 至 20 倍，股價約 218 至 256 美元，較現價跌 32% 至 42%；若同時發生架構替代，五年虧 50% 才會成立。","ruling":"採納為最大風險，與唯一致命點同源，不另設第二個致命點；機率放進空頭情境 30%。FY2024 下行時公司仍賺錢且 FCF 為正，屬可守的循環，採波動保護紀律。","watch":"每季核心有機成長、Lifecycle Services 訂單出貨比。","evidence_refs":["supply_demand_durability#1","end_markets#2"],"fact_refs":["f_price_at_dd"]},{"view":"論點失敗","evidence":"Siemens／NVIDIA 工業 AI 作業系統被視為較具威脅的問題，10-K 也把 AI 採用列為需求風險，Schneider 專欄主張以開放標準脫鉤軟硬體。","assumption":"控制層仍是工廠自動化的價值匯集點。","consequence":"若決策與編排層移到控制器之上，Software & Control 34% 的利益率會先受壓，影響最大的是終端倍數。","ruling":"部分採納。FactoryTalk Conductor 長在自有工具鏈，Logix 也能在開放運算平台上跑，屬強化型回應；但 AI 淨增量 ARR 未揭露，無法證明攻守已分，分界年暫訂 2028。","watch":"Software & Control 相對 Intelligent Devices 的有機成長差、毛利率。","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"],"fact_refs":["f_peer_rok_gross_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"FY2027 資本支出升到營收約 4%（FY2026 約 3%），新廠最大投資 FY2027 結束後才投入使用；回購由 FY2026 估算約 13 億美元降到 6 億美元；Software & Control 利益率 FY2027 只小幅上升，Rothe 2026-08-04 已說單靠漲價難擴張利潤率。","assumption":"新廠與資料中心訂單的報酬不低於目前 20.4% 的 ROIC。","consequence":"營收與 Logix 論點都成立，但折舊從 FY2028 起墊高、回購托底減少，EPS 成長低於簡單外推；基準 FY2029 EPS 因此低於共識約 2.6%。","ruling":"採納。基準情境 FY2028 起低於共識，不給新廠額外報酬。","watch":"FY2028 折舊與 ROIC；公司口徑 ROIC 低於 18% 即視為再投資報酬變差。","evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"],"fact_refs":["f_rev_consensus_fy1_m","f_consensus_eps_fy3"]},{"view":"價格已反映太多","evidence":"前瞻本益比 25.19 倍、PEG 2.24；帳面共識上修實為財年換年；賣方目標價 407 至 421 美元都早於這次財報，全距 215 至 536 美元接近 2.5 倍。","assumption":"市場願意為一段沒有下行年的路徑付 25 倍。","consequence":"基準情境即使 EPS 年增約 10%，年化也只有約 7.7%。","ruling":"採納，結論是現價不追。較前份下跌 20.7% 主要是倍數修正，不等於安全邊際。","watch":"前瞻本益比與同財年共識 EPS。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_rev_fy1_pct","f_price_at_dd"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 473.79 → 本次 375.86（-20.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=473.79","side_b":"本次 price_at_dd=375.86","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 473.79 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 473.79 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 473.79 美元：Bull 價 744.8、Bear 價 272，五年期望值 +4.8%，基準年化 1.4%，不對稱比 1.12","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.12。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 473.79 美元：五年期望值 +4.8%，基準年化 1.4%，不對稱比 1.12","side_b":"本次情境、股價 375.86 美元：五年期望值 +32.2%，基準年化 6.2%，不對稱比 2.96","ruling":"再換股價、情境不動：起點價下跌 20.7%，五年期望值多 27.3 個百分點，基準年化多 4.8 個百分點，不對稱比由 1.12 升到 2.96。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值區間假設","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 473.79 美元，假設市場維持 28 到 35 倍前瞻本益比，估值結論偏貴。","side_b":"本次股價 375.86 美元、前瞻本益比 25.19 倍，估值結論降一級到合理偏貴。","ruling":"前份對倍數的假設已失效，本次不再把倍數維持當論點，基準情境改用倍數下降計算。跌幅不等於安全邊際，PEG 仍有 2.24。","evidence_level":"高","settle_metric":"前瞻本益比與基準年化報酬","if_then":[],"evidence_refs":[]},{"axis":"品質評級與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評級 B，價值陷阱風險中等。","side_b":"本次兩者不變，但依據換成 FY2026 利潤率達標、ARR 連兩季不及預期，以及 EPS 成長明顯快於營收。","ruling":"維持原結論。利潤率兌現是正面新證據，ARR 落後與成長品質是負面新證據，兩者相抵。","evidence_level":"中","settle_metric":"FY2027 上半年 ARR 與 Enterprise 營業利益率","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"本次首次給值的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位為空。","side_b":"本次依新格式首次給值：護城河方向穩定、跑道中等、品質複利型兼具循環性、循環位置中段、機率 25／45／30、最大回撤 −30% 至 −45%。","ruling":"不是判斷轉向，沒有可比較的前值。","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份無重新進場條件（原文為空）。","side_b":"收盤價 ≤ 340 美元（約 22.8 倍 FY2027 共識 EPS），且 FY2027 共識 EPS 不低於 14.50 美元。","ruling":"唯一約束是價格。共識下限只用來確認分母沒壞，不是第二個等待理由。340 美元對應基準年化約 10%。","evidence_level":"中","settle_metric":"收盤價與 FY2027 共識 EPS","if_then":["若收盤價 ≤ 340 美元且共識不低於 14.50 美元，重跑研究後分批反買。","若共識跌破 14.50 美元，即使價格到位也不買，改看唯一致命點是否發生。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"organic 連 2 季 < +5%；OM 連 2 季 < 20%；連 1-2 季 FPE 漂移至 < 25x；前份未列獨立的清倉清單。","side_b":"核心有機成長連 2 季低於 5% 減碼三分之一；剔除關稅退款的 Enterprise 營業利益率連 2 季低於 22% 減碼三分之一；有機 ARR 連 2 季低於 5% 停止加碼；Software & Control 有機成長連 4 季為負且毛利率連 2 季同比下滑則清倉。","ruling":"成長門檻數字不變，但改用剔除關稅退款的口徑。利潤率門檻由 20% 升到 22%，因 FY2026 已達 22.2%。前瞻本益比低於 25 倍不再是減碼理由，因為現價已接近 25 倍且本次基準已假設倍數下降。","evidence_level":"中","settle_metric":"每季核心有機成長與 Enterprise 營業利益率","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份無唯一致命點（原文為空）。","side_b":"FY2028 之前出現連續兩季有機營收同比轉負的循環下行。","ruling":"新增，因為這是 EPS 與倍數同時受影響的最大單一敏感項。","evidence_level":"中","settle_metric":"每季有機營收同比","if_then":[],"evidence_refs":[]},{"axis":"共識上修是否真實","cause":null,"prior_field":null,"side_a":"事實表顯示 FY1 共識上修 12.69%、近 3 個月上修 12.86%。","side_b":"舊值 13.24／14.92／16.67 與新值 14.92／16.67／18.48 恰好平移一年，是財年換年，同一財年 FY2027 前後都是 14.92 美元。","ruling":"採後者，不把這些數字當上修動能。同財年修正約為零，FY2026 實際 13.42 美元高於三個月前共識 13.22 美元才是真正的超越。可能看錯之處：2026-07 Zacks 的 FY2027 估值為 13.90 美元，表示不同來源的舊值不一致。","evidence_level":"高","settle_metric":"同一財年的共識 EPS 逐週比較","if_then":["若投資人日後 FY2027 共識 EPS 高於 15.00 美元，才算真上修。","若跌破 14.50 美元，停止加碼。"],"evidence_refs":[]},{"axis":"FY2027 有機成長品質","cause":null,"prior_field":null,"side_a":"指引有機成長 6% 至 9%，中值 7.5%。","side_b":"中值含 1 個百分點客戶關稅退款的基期效應，真實成長 6.5%，低於 FY2026 核心 9% 與第四季核心 7%。","ruling":"採後者。Moret 說指引有保留，但目前只能確認成長放緩；若資本支出全面回升才會走向區間上緣。","evidence_level":"高","settle_metric":"FY2027 上半年核心有機成長","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"ARR 指引可信度","cause":null,"prior_field":null,"side_a":"Moret 2026-11-05：FY2027 ARR 成長 7%，軟體與服務都會改善。","side_b":"Moret 2026-08-04：第三季 ARR 成長 6% 低於預期；2026-11-05：第四季 5% 仍低於預期。Lifecycle Services 第四季報告 −9% 主要是 Sensia，有機 +2%。","ruling":"管理層把落後歸因於專案延後與 IT 設備漲價，未證，先監測。基準情境假設 ARR 約 6%。若 FY2027 上半年連兩季低於 6%，視為歸因證偽。","evidence_level":"中","settle_metric":"FY2027 第一、二季有機 ARR 成長","if_then":["若連兩季低於 6%，下修軟體第二曲線的權重，停止加碼。","若連兩季達到 7% 以上，跑道判斷重新檢視。"],"evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"axis":"Logix 是真需求還是提前拉貨","cause":null,"prior_field":null,"side_a":"Moret 2026-11-05：Logix 第四季 +25%，沒有補庫存或提前購買。","side_b":"FY2027 指引 Software & Control 降到高個位數，Logix 相近；PCB 供應偏緊，缺料期常見重複下單。通路庫存事實表未涵蓋。","ruling":"不可裁決至 FY2027 第二季財報。決勝數據未揭露，不採信也不否定管理層說法。","evidence_level":"低","settle_metric":"Software & Control 第一季指引 10% 的達成情況與第二季增速","if_then":["若第二季 Software & Control 有機成長低於 5%，視為有拉貨成分，下修 FY2028 EPS 假設。","若維持 10% 以上，上修基準情境。"],"evidence_refs":[]},{"axis":"通膨說法改變","cause":null,"prior_field":null,"side_a":"Rothe 2026-08-04：通膨在升高，不預期短期穩定。","side_b":"Rothe 2026-11-05：變化速度放緩、供應商調價通知減少，但第一季更難，PCB 供應偏緊。","ruling":"語氣轉好，尚未證實。第一季增量利益率指引 30% 中段，低於全年 30% 高段。損益層的吸收失敗以 price/cost 連兩季轉負為準。","evidence_level":"中","settle_metric":"price/cost 與第一季增量利益率","if_then":["若 price/cost 連兩季轉負，減碼三分之一。"],"evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：資料中心與半導體約占營收 10%，美國新產能投資創新高，Logix 獲超大規模資料中心採用。","side_b":"競爭與其他結構變數：Siemens／NVIDIA 工業 AI、開放式自動化，以及 Section 232 機器人與工業機械調查。","ruling":"雙向拉鋸。正面已反映在營收，負面尚未反映在數字，故護城河方向維持穩定。","evidence_level":"中","settle_metric":"Software & Control 有機成長差與 Section 232 結果","if_then":[],"evidence_refs":["competitive_share_entrants#3","reg_tariff_export#3","substitute_technology#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"RSI 28.86，股價較前份低 20.7%，FY2026 EPS 比最初指引中值高 1.72 美元，投資人日將更新長期利潤率目標，多頭情境年化逾 15%。","side_b":"基準年化不到 8%，共識沒有下行年，ARR 未達預期，前瞻本益比仍有 25 倍。","ruling":"不買。超賣與財報表現都是事實，但基準報酬不足以補償循環風險；代價是投資人日若大幅上修目標，可能買不到 340 美元。","evidence_level":"中","settle_metric":"收盤價、投資人日長期目標、同財年共識","if_then":["若股價先反彈到 420 美元以上而同財年共識沒有上修，不追。","若股價跌到 340 美元以下且基本面無損，分批反買。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2027 剔除關稅退款的核心有機成長要達到指引中值。","type":"假設驗證","maps_to":"H1","metric":"核心有機成長（剔除關稅退款與 Sensia）","threshold":"全年 ≥ 6.5%，第一季 ≥ 4%","action":"未達不加碼","source_freq":"季報與法說，每季","date":"2027-02","evidence_refs":[]},{"n":2,"text":"Enterprise 營業利益率要達到 FY2027 指引。","type":"假設驗證","maps_to":"H2","metric":"Enterprise 營業利益率（剔除關稅退款）","threshold":"FY2027 ≥ 23%","action":"未達不加碼","source_freq":"季報與法說，每季","date":"2027-11","evidence_refs":[]},{"n":3,"text":"有機 ARR 成長要由 5% 回升到指引 7%。","type":"假設驗證","maps_to":"H3","metric":"有機 ARR 成長","threshold":"FY2027 ≥ 7%，上半年任一季 ≥ 6%","action":"上半年連兩季低於 6% 停止加碼","source_freq":"季報與法說，每季","date":"2027-05","evidence_refs":["supply_demand_durability#1"]},{"n":4,"text":"工業資本支出循環回落，核心有機成長熄火。","type":"風險","maps_to":"R1","metric":"核心有機成長","threshold":"連 2 季低於 5%","action":"減碼三分之一","source_freq":"季報，每季","date":null,"evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"n":5,"text":"電子料通膨吃掉漲價。","type":"風險","maps_to":"R2","metric":"price/cost、Enterprise 營業利益率（剔除關稅退款）","threshold":"price/cost 連 2 季轉負，或營業利益率連 2 季低於 22%","action":"減碼三分之一","source_freq":"季報與法說，每季","date":null,"evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"]},{"n":6,"text":"Section 232 關稅落地且無法轉嫁。","type":"風險","maps_to":"R5","metric":"Section 232 結果與當季 price/cost","threshold":"關稅落地且當季 price/cost 轉負","action":"停止加碼","source_freq":"政府公告與季報","date":null,"evidence_refs":["reg_tariff_export#3"]},{"n":7,"text":"控制平台優勢被 AI 作業系統或開放式架構削弱。","type":"風險","maps_to":"R3","metric":"Software & Control 減 Intelligent Devices 的有機成長差、毛利率","threshold":"成長差連 2 季為負且毛利率同比下滑","action":"減碼一半","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"]},{"n":8,"text":"循環下行成真。","type":"Single Thing","maps_to":"Single Thing","metric":"有機營收同比","threshold":"連 2 季轉負","action":"第一季轉負停止加碼，第二季確認後減碼至半倉","source_freq":"季報，每季","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":9,"text":"價格回到足以補償循環風險的水準。","type":"估值rearm","maps_to":"現價","metric":"收盤價、FY2027 共識 EPS","threshold":"收盤價 ≤ 340 美元且共識 ≥ 14.50 美元","action":"重跑研究後分兩批建倉","source_freq":"每日股價、每週共識","date":null,"evidence_refs":[]},{"n":10,"text":"跌到 250 週均線附近且基本面無損。","type":"加碼","maps_to":"現價","metric":"收盤價、FY2027 共識 EPS","threshold":"收盤價 ≤ 300 美元且共識 ≥ 14.50 美元","action":"分批反買","source_freq":"每日股價、每週共識","date":null,"evidence_refs":[]},{"n":11,"text":"估值回到前份偏貴區間。","type":"減碼","maps_to":"現價","metric":"前瞻本益比","threshold":"≥ 32 倍（以 14.92 美元計約 477 美元）","action":"減碼三分之一","source_freq":"每日股價、每週共識","date":null,"evidence_refs":[]},{"n":12,"text":"控制平台地位出現實質流失。","type":"清倉","maps_to":"R3","metric":"Software & Control 有機成長、毛利率","threshold":"有機成長連 4 季為負且毛利率連 2 季同比下滑","action":"清倉","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":13,"text":"投資人日後複審長期目標與同財年共識。","type":"複審日期","maps_to":"H2","metric":"長期利潤率目標、FY2027 共識 EPS","threshold":"投資人日結束後一週內","action":"更新情境，不因目標上修直接追價","source_freq":"一次性","date":"2026-11","evidence_refs":[]}],"kill_metrics":[{"metric":"核心有機成長（剔除關稅退款與 Sensia）","bear_threshold":"連 2 季低於 5%","window":"連 2 季","source":"公司季報與法說","last_status":"ok"},{"metric":"Enterprise 營業利益率（剔除關稅退款）","bear_threshold":"連 2 季低於 22%","window":"連 2 季","source":"公司季報與法說","last_status":"ok"},{"metric":"有機 ARR 成長","bear_threshold":"連 2 季低於 5%","window":"連 2 季","source":"公司季報與法說","last_status":"warning"},{"metric":"Software & Control 減 Intelligent Devices 的有機成長差","bear_threshold":"連 2 季為負","window":"連 2 季","source":"公司季報","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-16.68, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等收盤價 ≤ 340 美元（約 22.8 倍 FY2027 共識 EPS，基準年化約 10%），且 FY2027 共識 EPS 不低於 14.50 美元。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"收盤價 ≤ 340 美元（約 22.8 倍 FY2027 共識 EPS），且 FY2027 共識 EPS 不低於 14.50 美元","exec_line":"現價不追。收盤價 ≤ 340 美元且 FY2027 共識 EPS 不低於 14.50 美元時，重跑研究後分兩批建倉；投資人日若上修長期利潤率目標，只更新情境，不因此追價。"},"reasoning":{"industry":"FY2026 部門營收：Intelligent Devices 4,185 百萬美元（約 46%，+11%）、Software & Control 2,818 百萬美元（約 31%，+18%）、Lifecycle Services 2,071 百萬美元（約 23%，−6%，主要因 Sensia 合資解散）。第四季部門利益率依序為 21.6%、34%、16.4%，三部門盈餘 588 百萬美元，Software & Control 約 256 百萬美元。TTM 毛利率 49.35%。第四季 Enterprise 營業利益率 24.5%，其中 1.3 個百分點來自關稅退款、0.5 個百分點來自 Sensia，剔除後約 22.7%，不能拿 24.5% 當常態。產業位於擴張期：第四季核心成長 7%、離散產業 +20%、美國新產能投資創新高，但管理層明說指引沒有假設資本支出全面回升，採礦專案仍在延後，食品飲料資本支出偏弱。單點依賴在通路：約 65% 銷售經獨立經銷商，前兩大經銷商約占 20%（FY2025 10-K），這既是觸及客戶的優勢，也是集中度風險；單一終端客戶占比事實表未涵蓋。","moat":"機制是工廠、機器製造商與工程人員把控制系統標準化在 Logix 與其軟體工具上，換系統要重寫程式、重新認證、重訓人員。可證方向：QTS、Stryker 的標準化案，Logix 第四季 +25%，控制器出貨量已高於疫情前（2026-11-05，Moret）；2026-08-04 Moret 也說在控制器取得份額。反向證據是這些都來自管理層，事實表沒有第三方份額。執行力判擴大：FY2026 Enterprise 營業利益率 +330 個基點，其中營運改善 270 個基點。定價權判穩定：FY2027 規劃約 3 個百分點價格，但 Rothe 2026-08-04 說單靠漲價難擴張利潤率，第三季 price/cost 也一度為負。同業比較：ROK TTM 毛利率 49.35%，高於 HON、PH、ETN，低於 EMR 的 53.61%；營業利益率 19.74%，低於 EMR 與 PH。ROIC 20.4%（CFO，TTM），同業 ROIC 事實表未涵蓋，所以評等不上到 A。當期報酬屬高利益率×低周轉，用 FY2026 Enterprise 營業利益率 22.2%、稅率 19.6% 倒推周轉約 1.1 倍。","growth":"三年共識 EPS CAGR 11.25%（13.42 到 18.48 美元，2026-11-07 Koyfin 快照，家數事實表未涵蓋）；基期剔除 0.11 美元關稅退款後為 11.6%。內生上限 4.5%，缺口約 6.75 個百分點。歸因：FY2026 營收約 8,989 百萬美元（部門合計 9,074 減客戶退款 85）到 FY2028 共識 10,132 百萬美元，CAGR 約 6.2%，高於內生上限的部分主要是約 3 個百分點的漲價，不需資本；同期 EPS CAGR 約 11.45%，與營收差約 5.3 個百分點，其中淨回購約 1.5 個百分點，其餘約 3.8 個百分點來自利潤率擴張。缺口可歸因於利潤率與淨回購，不依賴倍數重估，但表示成長品質低於靠再投資複利的公司。FY2027 有機指引 6% 至 9% 含 1 個百分點關稅退款基期效應，中值的真實成長是 6.5%，低於 FY2026 核心 9%。美國新產能 Moret 形容約在第四局，屬管理層自述。","governance":"FY2026 FCF 轉換率 113%，含關稅退款 6 個百分點，剔除後約 107%；第四季 FCF 602 百萬美元，轉換率 139%，退款貢獻約 21 個百分點；FY2027 指引回到 100%。全年回饋股東約 19 億美元，以股息約 6 億美元估算回購約 13 億美元，FY2027 只規劃約 6 億美元。資本支出由營收約 3% 升到約 4%，用於美國綠地新廠與數位基礎設施。淨負債 3,119 百萬美元，信評 A-／A3／A。近 12 個月沒有併購。資料差異：公司口徑全年 FCF 按 13.42 美元×約 112 百萬股×113% 約 17 億美元，yfinance TTM FCF 利潤率 16.51% 換算約 14.8 億美元，差異原因事實表未涵蓋，本輪不以 FCF 絕對額做承重判斷。現金去向四分與債務到期結構事實表未涵蓋。","valuation":"現價 375.86 美元，FY2027 共識 EPS 14.92 美元，前瞻本益比 25.19 倍；三年 CAGR 11.25%，PEG 2.24，屬偏貴。基準情境 FY2031 EPS 21.2 美元乘 24 倍得 508.8 美元，價格年化約 6.2%，加股息約 7.7%，其中 EPS 複利約 9.6%、倍數下降約 −3.0%、股息約 1.5%，沒有靠倍數重估。敏感度：FY2031 EPS 少 10%，目標價少約 51 美元；終端倍數少 2 倍，少約 42 美元；FY2031 利潤率少 1 個百分點，少約 22 美元。成長熄火對照：三年後成長降到 15%／10%／5%，前瞻本益比約 26／21／17 倍，較現值 +3%／−17%／−33%。市場可能錯的只有一點，就是共識沒有循環，這對現價是壞事不是好事，所以本次比共識保守，不主張市場低估。賣方目標價 406.67 美元（2026-04-07）與約 421 美元（無日期）都早於這次財報，只作弱參考。五年分位無資料：事實表只有 3 個年度端點，trailing P/E 分位 31.4、P/S 分位 98.5，兩者方向相反，是利潤率上升造成的。","premortem":"衰退信號亮一項，價值陷阱風險中等，依據見反證紀錄。反方向也可能看錯：若投資人日上修長期利潤率目標，且美國新產能真的還在早中段，本次 FY2028 起低於共識的基準情境會偏保守，340 美元可能等不到。歷史最大回撤事實表未涵蓋，回撤範圍改由空頭情境推導。2026-08-04 法說有三題未正面回答：Rothe 未量化第三季 price/cost 逆風、未給 2027 年 Software & Control 利潤率、未給通膨改善時間表。2026-11-05 已部分回答，Software & Control 利潤率小幅上升、通膨變化速度放緩，但 price/cost 金額仍未量化。"},"plain":{"six":{"how_it_makes_money":"ROK 賺的是工廠把控制標準定在 Logix 之後的持續採購，錢卡在控制器與軟體這一節點。Software & Control 占 FY2026 部門營收約 31%，第四季貢獻約 44% 的部門盈餘。","moat":"護城河方向穩定。Logix 控制平台的標準地位仍在賺錢，但份額上升只有管理層自述，外部份額與同業 ROIC 都沒有資料，不足以判定擴大。","growth":"五年後的跑道中等：資料中心與半導體約占營收 10%、FY2027 指引中十位數成長，但 TAM 與滲透率事實表未涵蓋，不足以確認第二條成長曲線。","capital":"資本配置尚可：股數確實在減、槓桿低於 2 倍，但以現價回購的盈餘殖利率只有約 4%，回購不算便宜。","valuation":"現價要求 FY2031 EPS 約 21 美元、終端仍有 24 倍，才有年化約 7.7%。這個假設我相信，但報酬不夠厚，跌到 340 美元以下才有約 10% 年化。","how_wrong":"最可能看錯在循環：共識三年路徑沒有下行年，而 FY2024 才剛出現營收 −8.77%、GAAP 稀釋 EPS 約 −31%。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等收盤價 ≤ 340 美元（約 22.8 倍 FY2027 共識 EPS，基準年化約 10%），且 FY2027 共識 EPS 不低於 14.50 美元。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":375.86,"week26_return_pct":-16.68,"consensus_rev_3m_pct":12.86,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2027 共識 14.92 美元不含關稅退款淨利益，分母可用；FY2026 的 13.42 美元含 0.11 美元退款。上行幅度以基準 EPS 乘 trailing 倍數計算，倍數由 28.0 倍線性降到 24 倍，一年後 14.9×27.2，三年後 18.0×25.6。帳面共識上修 12% 至 13% 是財年換年，同一財年 FY2027 前後都是 14.92 美元，不能當上修證據。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"投資人日更新長期利潤率目標","impact":"高","watch":"Enterprise 營業利益率目標是否高於 FY2027 的 23%，以及 ARR 目標。"},{"date":"2026-11","date_precision":"month","type":"product","event":"Automation Fair 展示軟體定義 Logix 與 FactoryTalk Conductor","impact":"中","watch":"客戶採用案例與 AI 收入是否有量化揭露。"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"FY2027 第一季財報","impact":"高","watch":"有機成長是否達中個位數、EPS 約 3 美元、Software & Control 成長 10%、ARR 是否回升。"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"美國綠地新廠的主要投資開始投入使用","impact":"中","watch":"折舊增幅與 ROIC 是否低於 18%。"}],"_projected_from":"v19"}
```
