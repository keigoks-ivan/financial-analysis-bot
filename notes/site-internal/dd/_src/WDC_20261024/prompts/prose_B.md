你是 stock-analyst v20 的**散文層（prose）agent**，標的 WDC（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261024/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：WDC　日期：2026-10-24　archetype：None　前份裁決：2026-10-13　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1453B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（422B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1132B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1485B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1271B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（287B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（791B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1975B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3352B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2820B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1453           3883-5547      5 條（2–6 內）  
s3                  8000         422           5305-7578      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3888          7778-11112      5 條（2–6 內）  
s6                 11000         287          7499-10713      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         791           1896-2709      5 條（2–6 內）  
s10                 5000        1975           2118-3025      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2820           2000-2180      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4858B；至少需散文≈40.14KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−72%
−70%
−70
−68%
−52%
−50
−50%
−38%
−14.88
−11.2%
0%
0
0.15
0.175
0.19
0.2
0.3
1
01
1.08
1.1%
1.2%
1.3
1.4
1.88
1.93
2
2.1
2.4
3
03
3%
3.2
3.5%
3.80
3.83
4.00
4%
4
4.2
4.3
4.64
5
05
5%
5.3%
5.60
5.80
6
06
6%
7
7%
07
7.2%
8
08
8%
8.76
8.8
8.8%
9
9.4
9.6
9.96
10%
10
10.4%
10.44
11
11.2%
11.4
12
12.81
13%
13.84
13.89
13.9
14
14.88%
15%
15
16%
17%
18%
18
18.7
18.7%
19%
19.37%
20%
20
20.0%
21.3
22%
22
22.5%
23
23.75%
24
24.3%
24.5
24.7
24.84
25%
26%
26
26.92
27.18%
28%
30%
30
31%
32%
33
33.8
34
35%
35
35.6%
35.75
36
36.9%
37.47
39
39.21
40%
40
41
42
43%
44%
44
44.2%
45
45%
46.0
46
49
49.1%
50%
50.71
51
52
54%
54.4%
55%
56%
58
58%
58.1%
60%
61%
62
62%
68%
70
71%
72%
73%
80%
88%
93
100
100%
104
110
110.32
119%
137.5
149%
149.4%
150%
161%
165
200
212.22
232
250
$320
320
340
343.67
344
348
362
374
386.94
392
408
483
500
000660
900
930
2026
2027
2028
2029
2030
2031
005930
20261024
1,050
1,420
4,500
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
{"meta":{"ticker":"WDC","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Western Digital Corporation"},"oneliner":"HDD雙寡頭之一，漲價與高容量換代把毛利率推到58%，但盈餘處在循環高檔，Toshiba擴產與HAMR落後是價格反轉的引信，現價沒有給足安全邊際","thesis":{"H":[{"id":"H1","text":"漲價延續：到FY2028（2028年6月），每TB均價維持年增，毛利率守在55%以上","2y":"FY2028結束時毛利率≥55%，每TB均價年增≥+5%","5y":null,"10y":null,"threshold":"每季每TB均價年增≥+5%，且Non-GAAP毛利率≥55%","source":"每季財報新聞稿與法說會（財務長揭露每TB均價年增）","drift_rule":"毛利率較門檻低5%以上連2季為削弱；低10%以上連3季為反轉"},{"id":"H2","text":"換代補回出貨量：40TB ePMR與HAMR讓EB年增回到25%以上，與Seagate的差距收斂","2y":"FY2028上半年EB年增≥25%","5y":null,"10y":null,"threshold":"2027年3月底前完成兩家超大規模客戶HAMR認證；FY2027第四季起EB年增≥25%","source":"每季法說會的EB出貨數字與HAMR里程碑","drift_rule":"自2027年3月季起計：EB年增連2季低於23.75%為削弱；連3季低於22.5%為反轉"},{"id":"H3","text":"結構改變縮小下行：雙寡頭不增單位產能、長約延伸，下一次下行的營收跌幅小於FY2023的31%","2y":null,"5y":"下一次需求或價格下行時，年營收跌幅<20%，毛利率不低於40%","10y":null,"threshold":"下行年度營收年減<20%，且毛利率≥40%","source":"10-K年度營收與毛利率；同業產能公告","drift_rule":"TTM營收較高點低5%以上連4季為削弱；低10%以上連6季為反轉"}],"R":[{"id":"R1","text":"Toshiba擴產加上低價搶單，2028年後每TB價格成長放緩甚至轉負","h_ref":"H1","clock":"🔥","threshold":"Toshiba正式公告擴產，且每TB均價年增連2季<+10%","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5","cyclical_supply_discipline_capacity#0"]},{"id":"R2","text":"HAMR落後Seagate，EB份額持續流失；HAMR轉換若出現大規模瑕疵，會觸發合約條款","h_ref":"H2","clock":"🔥","threshold":"HAMR認證延後到2027年第二季以後，或EB年增連4季落後同業10個百分點以上","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"id":"R3","text":"客戶集中加上超大規模業者資本支出循環：下行時EB量縮，FY2023曾年減26%","h_ref":"H3","clock":"🐢","threshold":"單一客戶占年營收>20%，或任一季EB季減>15%","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R4","text":"泰國、馬來西亞生產集中，加上關稅與稀土管制，吃進毛利","h_ref":"H1","clock":"⚡","threshold":"關稅或稀土因素使毛利率單季下滑>2個百分點","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#2"]},{"id":"R5","text":"快閃在容量層長期替代硬碟","h_ref":"H3","clock":"🐢","threshold":"HDD與SSD每TB價差縮到3倍以內","evidence_refs":["competitive_share_entrants#4"]}],"single_thing":{"description":"某一季每TB平均售價年增率由正轉負（價格循環反轉）","why_fatal":"毛利率由22%擺到58%，幾乎全由價格驅動，增量毛利率逾80%；價格轉負時，利益率下修的槓桿同樣放大。FY2023曾營收年減31%並轉為營業虧損","if_happens":"基準情境失效，改走Bear路徑（FY2030每股盈餘約12元）；持有者清倉，未持有不碰，等下一輪投降訊號","how_monitor":"每季法說會揭露的每TB均價年增率（2026年6月季18%、9月季28%），並追長約續約價格、Toshiba擴產進度、HAMR放量","probability":"12～24個月內約25%：財務長稱未來3～4季仍有漲價空間、之後放緩；Toshiba擴產目標在2028年3月前"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":8.76,"peg_fy2":0.3,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2026A":9.96,"FY2027E":24.84,"FY2028E":39.21,"FY2029E":50.71},"fy_end_month":6,"eps_basis":"Non-GAAP稀釋每股盈餘（Koyfin共識，6月制財年）。FY2026A用2026-07-30快照的FY1共識9.96元代理：該快照在財年切換前，指的是FY2026。GAAP的26.92元含非營業利得，不能當基期"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261024/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"近五年有兩個GAAP虧損年度（FY2023、FY2024）；毛利率由22%擺到58%，擺幅逾30個百分點；營收主要由每TB價格驅動"},"industry":{"clock_phase":"III","sd_verdict_source":"逐字稿2026-10-22財務長：越遠期越少出貨量受長約價格條款覆蓋。TrendForce（2026-10-07）：雙寡頭轉HAMR後供需逐步趨近平衡。","bargaining":{"up":"高容量平台的磁頭與碟片自製，外購只用在低容量機種；DRAM與NAND投入成本上漲，是近期的成本壓力","down":"前十大客戶占73%，前三大占44%。長約採基準價加基準量，超額量另行議價，買方集中、議價力強","geo":"組裝集中在泰國與馬來西亞，碟片來自日本，受關稅與原產地認定影響"},"profit_pool_dir":"近兩年利潤池從客戶端流向HDD雙寡頭；2028年供給追上後的方向待驗","tam_table":{"expanded":false,"reason":"HDD已承載超大規模資料中心約八成資料，不屬低滲透或新品類情境；需求用EB年增逾25%衡量即可，承重變數是價格而不是TAM"}},"moat":{"mechanism":"自製磁頭與碟片，加上韌體與伺服機構整合，提高面密度。不增加單位產能，靠每顆硬碟的容量增加EB供給，給客戶最低的總持有成本；超大規模客戶每次換代都要重新認證，形成轉換摩擦。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"EB出貨年增22%（2026年9月季），落後同業約10個百分點（法說會UBS提問，管理層未否認）；TrendForce預期Seagate在2028年居首。同期毛利率58.1%創高。執行力穩定，定價力短期擴大但屬供需所賜，合判持平。","peer_na_reason":"事實表同業表沒有Seagate與Toshiba，列出的是快閃記憶體與全快閃陣列廠，ROIC差距不可比，所以改用EB份額方向判讀","threats":[{"level":"🟡","text":"Toshiba擴產加上低價搶單，壓低2028年後的每TB價格。擴產本身尚未經Toshiba證實，但屬破壞性競爭，機率取下限以上。","p":"35%","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5","cyclical_supply_discipline_capacity#0"]},{"level":"🟡","text":"HAMR落後Seagate約一年；首代HAMR轉換若出現大規模瑕疵，可能觸發客戶合約的瑕疵條款並壓縮毛利率。","p":"30%","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"level":"🟡","text":"快閃在容量層長期替代硬碟。目前HDD與SSD每TB價差約5～10倍，五年內架構性替代的機率低。","p":"10%","evidence_refs":["competitive_share_entrants#4"]},{"level":"🟡","text":"客戶集中度由FY2024的55%升到FY2026的73%，單一客戶議價或轉單的衝擊放大。","p":"25%","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]}],"roic_durability":{"quadrant":"高利益率；周轉率待查（事實表未涵蓋投入資本，資本支出約占營收4%～6%，屬輕資產更新）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是超大規模業者，三角色一致。超大規模資料中心約八成資料存在HDD上（2026-08-05執行長），HDD每TB價格只有SSD的五到十分之一。AI推論日誌、檢查點、影片讓保存需求屬於需要而非想要；前七大客戶需求能見度到2030～2031年（2026-10-22執行長）。"},{"item":"決策層級","level":"🟡","text":"替代性要在超大規模客戶的認證層級看。每代平台都要重新認證，換供應商要等一個認證週期，這是摩擦。但市場只有雙寡頭加Toshiba，客戶每次換代都能重新分配份額；長約只鎖基準量，上修量另議。"},{"item":"價值鏈分配","level":"🟡","text":"目前HDD廠拿走的價值偏多：毛利率58%，客戶仍接受每TB均價年增28%。但前十大客戶占73%，買方集中；DRAM與NAND投入成本上漲，正把部分價值移向上游。磁頭獨立供應商只有TDK，這點對自製能力弱的Toshiba約束較大。"},{"item":"社會容忍度","level":"🟢","text":"屬企業對企業的儲存採購，沒有監管價格上限，也沒有授權依賴。10-K只有一般性反壟斷揭露，未點名具體調查。政策風險在關稅與稀土管制，屬成本面，不屬社會對漲價的容忍。"}],"roiic":"事實表未涵蓋投入資本。FY2025到FY2026營業利益由約21.3億美元增到約46.0億美元，增加約24.7億美元，期間淨資本支出每季約1億美元，增量報酬極高，但增量主要來自漲價，不是新增投資。","reinvest_rate":"事實表未涵蓋折舊與營運資金變動，無法算出。已知管理層承諾自由現金流全數回饋股東，五年資本支出平均占營收4%～6%，未來兩年略高，再投資率偏低。","endo_ceiling":null,"formula_note":"內生成長率等於增量ROIC乘以再投資率。本公司的成長來自價格與面密度，不靠新增資本，以再投資率推算的天花板無法量化；共識三年EPS成長遠超任何以再投資支撐的上界，缺口歸因於利益率擴張。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","WDC":48.85,"SNDK":71.47,"000660.KS":76.27,"005930.KS":57.48,"PSTG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","WDC":35.6,"SNDK":61.58,"000660.KS":68.04,"005930.KS":36.88,"PSTG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","WDC":27.18,"SNDK":56.77,"000660.KS":47.8,"005930.KS":28.95,"PSTG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","WDC":8.99,"SNDK":6.56,"000660.KS":4.93,"005930.KS":9.7,"PSTG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"SNDK","gm":71.47,"om":61.58,"fcf_margin":56.77,"rd_intensity":6.56,"strategy_note":"前子公司，做快閃記憶體。TTM毛利率71%、營益率62%，遠高於WDC，反映NAND漲價高峰；長期是容量層的替代者，不是HDD的直接對手。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"000660.KS","gm":76.27,"om":68.04,"fcf_margin":47.8,"rd_intensity":4.93,"strategy_note":"SK海力士。記憶體高峰期營益率68%，和WDC同樣受AI資本支出循環驅動，但產品層不同，不能當HDD的錨。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"005930.KS","gm":57.48,"om":36.88,"fcf_margin":28.95,"rd_intensity":9.7,"strategy_note":"三星。營益率36.9%，和WDC的35.6%相近；同時供應SSD，是快閃替代硬碟的主要來源之一。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"PSTG","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"全快閃儲存陣列廠，事實表沒有財務數字；它的論點是用快閃取代資料中心硬碟。"}]},"growth":{"driver_mix":"價格（每TB均價年增28%）大於量（EB年增22%）；回購次要；無併購","runway_years":"管理層稱EB需求年增逾25%；HDD已承載約八成超大規模資料，滲透率口徑不適用。以價格成長可持續的年數估，約2～3年","runway_post_y5":"🟡","endo_ceiling_basis":"見護城河段的再投資空間：成長主要來自價格與面密度，不靠新增資本；投入資本與折舊事實表未涵蓋，內生天花板無法用再投資率量化","segments":[{"item":"雲端","value":"39億美元，占88%，年增54%（2026年9月季）"},{"item":"Client","value":"3.2億美元，占7%，年增119%"},{"item":"Consumer","value":"1.93億美元，占5%，年增19%"}],"decay_signals":[{"signal":"核心市占近12個月縮減","lit":true,"evidence":"EB出貨年增22%，落後同業約10個百分點；TrendForce預期Seagate在2028年居首"},{"signal":"EPS成長顯著高於營收成長","lit":true,"evidence":"2026年9月季EPS年增161%，營收年增55%，差距來自漲價帶動的利益率擴張"},{"signal":"毛利率連2季年減","lit":false,"evidence":"毛利率58.1%，年增1,420個基點"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"不增單位產能但持續投資磁頭與碟片，營收年增55%"}],"trap_rating":"🟡（亮兩項）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；資本回饋以回購為主，管理層承諾自由現金流全數回饋，2026年9月季回饋11億美元"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年無重大併購；Kioxia合併僅是報導中的洽談，未見最終協議","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"前瞻盈餘殖利率7.2%（1÷13.84）；事實表未涵蓋10年期公債殖利率，無法判定是否過關","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC單季4,500萬美元、占營收1.2%；稀釋股數由3.83億股降到指引的3.80億股，淨稀釋為負","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY1，FY2027E Non-GAAP共識）；循環股本應優先看股價淨值比，但事實表未涵蓋","tier":"HDD雙寡頭（事實表無同tier同業）","peers":{"expanded":false,"reason":"事實表同業表沒有估值倍數，列出的也是快閃記憶體廠，不是HDD可比公司，不能當估值錨"},"fwd_pe":13.84,"peg":0.19,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比13.84倍、FY2028共識8.8倍看似便宜，但分母建在紀錄高毛利率上，屬分母爭議，便宜論證不成立。PEG 0.19是高峰期的成長率造成，不代表便宜。基準情境12個月374元（+8.8%）、五年408元（+18.7%），年化不到4%，判黃色。事實表未涵蓋5年估值分位。","upside_short_pct":8.8,"upside_mid_pct":18.7},"trap_analysis":{"verdict":"🟡","label":"高峰盈餘陷阱風險（價格驅動）"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY2023同一硬碟事業EB年減26%、營收年減31%，毛利率掉到22%並出現營業虧損；Toshiba計畫在2028年3月前讓產能倍增，份額目標30%；雙寡頭的HAMR也在2027～2028年放量","assumption":"本輪不增單位產能與長約延伸，能讓價格在供給追上時不反轉","consequence":"五年後虧五成最可能的路徑：2028年EB供給成長超過需求，長約到期重議，每TB價格年減，毛利率回到40%以下，EPS落到15元以下，倍數同步壓縮","ruling":"採納，用Bear 35%定價。和唯一致命點（每TB均價年增轉負）完全重疊，不另立","watch":"每季每TB均價年增率、Toshiba正式擴產公告、長約續約價格","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","supply_demand_durability#2","cyclical_supply_discipline_capacity#0"],"fact_refs":["f_ma_w250","f_peer_wdc_gross_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"前十大客戶占比由55%升到73%，三家各占16%、15%、13%。第三方彙整的10-K風險因子指出，HAMR轉換可能觸發客戶合約的大規模瑕疵條款。另有報導稱公司與Kioxia洽談以股票支付的合併，規模可能逾200億美元","assumption":"漲價成功時，超額利潤留在股東手上","consequence":"需求與價格都成立，但利潤可能被單一大客戶議價、HAMR瑕疵賠償，或以股票併購NAND廠稀釋，重新引入快閃循環","ruling":"部分採納。客戶集中與HAMR瑕疵列為風險觸發；Kioxia合併在簽約前不定價，簽約就重跑判斷","watch":"單一客戶營收占比、HAMR良率與退貨、Kioxia最終協議","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","substitute_technology#2"],"fact_refs":["f_kpi3_fcf"]},{"view":"價格已反映太多","evidence":"股價由250週均線110元漲到344元；8月財報優於預期，股價仍下跌5%，顯示預期已被墊高","assumption":"市場以FY2028共識39元為基準","consequence":"若FY2028只達基準34元、倍數回到10倍，股價約340元，現價沒有上檔","ruling":"部分採納。FY2028共識8.8倍已含部分循環折價，所以不是貴到要迴避；但以本輪基準看，現價沒有安全邊際","watch":"12月季每TB均價年增與2027年3月季指引","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"長期替代風險是快閃（SanDisk、三星、美光、鎧俠）；硬碟在泰國與馬來西亞組裝，零件來自日本、中國、菲律賓，對這些地區課徵的關稅多次變動","assumption":"HDD與SSD每TB價差維持5～10倍，關稅可以轉嫁","consequence":"若價差縮小或關稅吃進毛利，HDD在容量層的角色會被侵蝕","ruling":"反駁五年內的架構替代，因為價差仍大；關稅列風險觸發，以毛利率是否吸收失敗來判定","watch":"HDD與SSD每TB價差、232條款第二階段的涵蓋品項、單季毛利率","evidence_refs":["competitive_share_entrants#4","reg_tariff_export#3","geo_supply_chain#0"],"fact_refs":["f_kpi5_non_gaap"]}],"max_dd":{"lo":-70,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 386.94 → 本次 343.67（-11.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=386.94","side_b":"本次 price_at_dd=343.67","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 386.94 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 386.94 美元：Bull 價 900、Bear 價 137.5，五年期望值 +20.0%，基準年化 5.3%，不對稱比 1.3","side_b":"本次情境、股價仍用 386.94 美元：Bull 價 930、Bear 價 165，五年期望值 +10.4%，基準年化 1.1%，不對稱比 1.4","ruling":"先換情境、股價不動：五年期望值少 9.6 個百分點，基準年化少 4.2 個百分點。不對稱比由 1.3 變為 1.4。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 386.94 美元：五年期望值 +10.4%，基準年化 1.1%，不對稱比 1.4","side_b":"本次情境、股價 343.67 美元：五年期望值 +24.3%，基準年化 3.5%，不對稱比 1.88","ruling":"再換股價、情境不動：起點價下跌 11.2%，五年期望值多 13.9 個百分點，基準年化多 2.4 個百分點，不對稱比由 1.4 升到 1.88。合計五年期望值比前份多 4.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"結構性需求對循環高檔","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：12月季指引EPS 5.80元，年化約23元，即使停在這個水準，15倍也有348元；FY2028共識只有8.8倍；股價跌破52週均線但仍在104週均線之上，屬回檔區；前七大客戶需求能見度到2030～2031年；雙寡頭不增單位產能，長約延到2027～2028年","side_b":"毛利率58.1%創紀錄並指引升到60%～61%，FY2023曾只有22%；每TB均價年增由高個位數加速到28%；Toshiba擴產指向2028年；財務長說越遠期越少出貨量受長約價格覆蓋","ruling":"不可調和（方向相反），選循環側。依據有三：能見度是量，不是價（2026-10-22財務長）；價格增速還在加速，正是高檔特徵；同一事業FY2023下行時EB年減26%。執行上觀望，等價格或價格證據","evidence_level":"中：一手法說會與10-K歷史；Toshiba擴產為報導，尚未證實","settle_metric":"2028年上半年每TB均價年增率與毛利率","if_then":["若FY2028上半年每TB均價年增仍≥+10%、毛利率≥55%，結構側成立，重跑判斷，可首倉1/3","若任一季每TB均價年增轉負，循環側成立；未持有不碰，持有者清倉","若股價先走、證據未到：反彈回52週均線362元以上但每TB均價年增放緩，不追","若股價跌到320元以下而每TB均價年增仍≥+10%，屬基本面無損的下跌，首倉1/3分批買"],"evidence_refs":["cyclical_prior_downcycle_behavior#1","supply_demand_durability#2","cyclical_supply_discipline_capacity#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：Toshiba計畫在2028年3月前讓產能倍增、份額目標30%；WDC的EB成長落後Seagate約10個百分點，HAMR晚一步","side_b":"結構轉好：雙寡頭不增單位產能，長約加接單生產取代現貨，需求能見度到2030～2031年。其他結構變數：關稅與稀土管制，客戶集中度升到73%","ruling":"雙向拉鋸。結構轉好與競爭惡化同時發生，交會點是每TB價格；2028年前看不出哪邊勝出","evidence_level":"中","settle_metric":"Toshiba正式擴產與2028年長約續約價格","if_then":["若Toshiba正式公告擴產且長約重議價格下調，判競爭惡化中，凍結進場","若Toshiba擴產後兩季每TB均價年增仍≥+10%，判結構性轉好中，重跑判斷"],"evidence_refs":["competitive_share_entrants#0","reg_tariff_export#2","customer_concentration_credit#0"]},{"axis":"每TB成本降幅前後說法","cause":null,"prior_field":null,"side_a":"2026-08-05財務長：6月季每TB成本年減約8%，中長期約年減10%","side_b":"2026-10-22財務長：DRAM與NAND投入成本上漲，近期每TB成本年減低於10%，9月季約4%～5%，靠價值工程逐步抵銷","ruling":"可調和，屬程度差異。長期目標沒改，但近期成本降幅減半，代表毛利率擴張更依賴漲價","evidence_level":"高：一手法說會","settle_metric":"2027年3月季每TB成本年減幅度","if_then":["若連兩季每TB成本年減<5%而漲價放緩，毛利率指引會先轉弱，Bear機率上調到40%"],"evidence_refs":[]},{"axis":"HAMR時程","cause":null,"prior_field":null,"side_a":"2026年7月報導：2026年上半年開始與一家超大規模客戶認證，年底擴到最多三家，2027年上半年量產爬坡","side_b":"2026-10-22執行長：兩家超大規模客戶在2027年第一季完成認證，2027年上半年量產；另兩家在2027年上半年才開始認證；第二代HAMR在2027年下半年開始認證","ruling":"可調和。量產時點沒變，但年底三家改成兩家；Seagate已有兩家量產採購，落後約一年","evidence_level":"高：一手法說會對照二手報導","settle_metric":"2027年3月底是否完成兩家認證","if_then":["若認證延後到2027年第二季以後，Bull機率下調到15%，維持觀望"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"長約漲價條款說法","cause":null,"prior_field":null,"side_a":"2026-08-05：分析師問長約是否逐季調價，執行長說對方過度外推，只講基準價加基準量","side_b":"2026-10-22：執行長說一批長約在進入不同期間時有合約內漲價，週年時依新平台的總持有成本調價","ruling":"新說法較正面，但沒給幅度，也沒給重新定價的比例，不改基準情境","evidence_level":"中：管理層口述，無數字","settle_metric":"長約覆蓋比例與重新定價比例是否揭露","if_then":["若揭露2028年以後長約有鎖價條款且覆蓋過半出貨，Bear機率下調到30%並重跑判斷"],"evidence_refs":[]},{"axis":"共識修正數字的口徑","cause":null,"prior_field":null,"side_a":"事實表列FY1共識近三個月修正+149.4%（9.96元到24.84元）","side_b":"9月季EPS 4.64元加12月季指引5.80元，上半年已達10.44元，所以9.96元不可能是FY2027共識，應是財年切換前的FY2026","ruling":"149%是財年切換造成的假象，不當成上修動能；真正的FY1上修採兩份快照之間的+19.37%","evidence_level":"高：用事實表與逐字稿數字互證","settle_metric":"下一份快照的同財年比較","if_then":["若之後同財年的共識連兩次下修，視為循環轉折的早期訊號，凍結進場"],"evidence_refs":[]},{"axis":"FY2026盈餘基期","cause":null,"prior_field":null,"side_a":"年度財報GAAP稀釋EPS 26.92元、淨利93億美元","side_b":"同年營業利益約46億美元，淨利遠高於營業利益，含非營業利得；Non-GAAP基期約10元","ruling":"成長與估值一律用Non-GAAP口徑，GAAP的26.92元不能當基期，也不用來算自由現金流轉換率","evidence_level":"高","settle_metric":"10-K非營業項目明細（事實表未涵蓋）","if_then":["若非營業利得被證實可重複發生，再改用GAAP口徑重估"],"evidence_refs":[]},{"axis":"前份漂移：股價下跌後的估值與結論","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份：股價386.94元，估值黃色，品質B，觀望追蹤","side_b":"本次：股價343.67元（−11.2%）；FY2028共識由33.8元升到39.21元，倍數降到8.8倍，但分母爭議沒解，估值維持黃色、品質B、結論維持觀望","ruling":"價格下跌加上共識上修都讓倍數變便宜，但便宜來自高峰分母，結論不因價格改變","evidence_level":"高","settle_metric":"每TB均價年增率","if_then":["若股價跌到320元以下而每TB均價年增≥+10%，首倉1/3"],"evidence_refs":[]},{"axis":"前份漂移：基本面判讀","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：陷阱風險黃、護城河持平、跑道黃、循環/商品、晚循環","side_b":"2026-10-22季報：營收、毛利率、EPS全面超過8月指引，每TB均價年增加速到28%，前七大客戶能見度到2030～2031年；但EB年增22%仍落後同業，HAMR認證仍在2027年第一季","ruling":"新證據強化短期盈餘，也讓循環位置更靠高檔（價格加速、毛利率再創高），五欄都維持不變","evidence_level":"高：一手法說會","settle_metric":"12月季每TB均價年增與EB年增","if_then":["若12月季EB年增回到25%以上且HAMR認證如期，護城河方向重評為擴大"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"前份漂移：情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 20%、Bear 32%，最大回撤−72%單點","side_b":"本次：Bull 20%、Base 45%、Bear 35%；最大回撤改為區間−50%到−70%","ruling":"共識三年成長遠超以再投資支撐的天花板，Bear機率下限30%；價格加速屬高檔訊號，Bear再上調3點。回撤改用區間，並以104週、250週均線與FY2023下行幅度定界","evidence_level":"中","settle_metric":"每TB均價年增率","if_then":["若FY2028上半年每TB均價年增仍≥+10%，Bear機率回調到30%"],"evidence_refs":[]},{"axis":"前份漂移：進場重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","side_b":"股價≤$320（約9.4倍基準FY2028每股盈餘34元）且最新一季每TB均價年增≥+10%→首倉1/3；或HAMR量產後連兩季每TB均價年增≥+10%→重跑判斷","ruling":"價格門檻320元不變，但錨改為本輪基準34元的約9.4倍：共識FY2028已升到39.21元，沿用舊錨的10倍會變成392元，等於用上修後的高峰數字放寬門檻。價格條件由年增≥0收緊到≥+10%，因為漲價已加速到28%，掉到10%以下就是循環轉折。第二條改看HAMR量產後的價格，因為法說會表明越遠期長約的價格覆蓋越少，CY2029以後的鎖價揭露不會出現","evidence_level":"高","settle_metric":"股價與每TB均價年增率","if_then":["若兩條都未觸發，維持觀望到2027年1月財報再複審"],"evidence_refs":[]},{"axis":"前份漂移：減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標","side_b":"本次設四項：每TB均價年增連2季<+5%或任一季轉負→清倉；毛利率連2季年減且<50%→減碼一半；EB年增在FY2027下半年仍<20%→不加碼；HAMR認證延後到2027年第二季以後→維持觀望","ruling":"前份只有進場條件，本次補上持有後的減碼與清倉線，讓循環高檔的出場有數字可依","evidence_level":"中","settle_metric":"每季法說會","if_then":["若任一清倉條件觸發，持有者當季清倉"],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設Single Thing（空白）","side_b":"某一季每TB平均售價年增率由正轉負（價格循環反轉）","ruling":"價格是毛利率與EPS在數學上最大的敏感度項（增量毛利率逾80%），比Toshiba擴產或HAMR延誤這類中間變數更直接，所以把Single Thing定在價格","evidence_level":"高","settle_metric":"每季每TB均價年增率","if_then":["若轉負，持有者清倉；未持有不碰"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到320元以下，且最新一季每TB均價年增仍≥+10%：盈餘分母的爭議由價格補償","type":"估值rearm","maps_to":"H1","metric":"股價與每TB均價年增率","threshold":"股價≤$320且每TB均價年增≥+10%","action":"首倉1/3目標倉","source_freq":"每日股價、每季法說會","date":null},{"n":2,"text":"某一季每TB平均售價年增率由正轉負","type":"Single Thing","maps_to":"Single Thing","metric":"每TB均價年增率","threshold":"任一季<0%","action":"未持有不碰；持有者清倉","source_freq":"每季法說會","date":null},{"n":3,"text":"Toshiba正式確認菲律賓擴產，且公司揭露長約重議價格下調","type":"風險","maps_to":"R1","metric":"Toshiba公告與長約價格","threshold":"擴產經正式公告且任一季每TB均價年增<+10%","action":"凍結進場；持有者減碼一半","source_freq":"新聞與每季法說會","date":"2028-03","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5","cyclical_supply_discipline_capacity#0"]},{"n":4,"text":"首代HAMR如期完成兩家超大規模客戶認證，且量產不折價","type":"假設驗證","maps_to":"H2","metric":"HAMR認證與量產時點","threshold":"2027年3月底前完成兩家認證，2027年上半年量產出貨","action":"如期則重跑判斷；延後一季以上則不追，Bull機率降到15%","source_freq":"每季法說會","date":"2027-03","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"n":5,"text":"中國中重稀土出口逐案核准的暫停期到期","type":"風險","maps_to":"R4","metric":"稀土管制與公司供應揭露","threshold":"暫停期未延長，且公司揭露供應中斷或毛利率單季下滑>2個百分點","action":"凍結進場","source_freq":"公告與每季法說會","date":"2026-11-10","evidence_refs":["geo_supply_chain#2"]},{"n":6,"text":"232條款第二階段關稅涵蓋硬碟，或泰國、馬來西亞產地加稅","type":"風險","maps_to":"R4","metric":"關稅範圍與單季毛利率","threshold":"關稅涵蓋硬碟，且毛利率單季下滑>2個百分點","action":"凍結進場；持有者減碼一半","source_freq":"政府公告與每季財報","date":null,"evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0"]},{"n":7,"text":"與Kioxia簽署合併最終協議","type":"風險","maps_to":"H3","metric":"併購協議","threshold":"簽約且交易規模>市值5%","action":"重跑判斷，完成前不建倉","source_freq":"公司公告","date":null},{"n":8,"text":"毛利率連兩季年減且跌破50%","type":"減碼","maps_to":"H1","metric":"Non-GAAP毛利率","threshold":"連2季年減且<50%","action":"持有者減碼一半","source_freq":"每季財報","date":null},{"n":9,"text":"單一客戶占比或前十大客戶占比再升","type":"風險","maps_to":"R3","metric":"10-K客戶集中度","threshold":"單一客戶占年營收>20%，或前十大>80%","action":"Bear機率上調到40%並重跑判斷","source_freq":"每年10-K","date":"2027-08","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"n":10,"text":"2026年12月季財報複審","type":"複審日期","maps_to":"H1","metric":"EPS對指引5.80元、每TB均價年增、EB年增","threshold":"EPS≥5.60元、每TB均價年增≥+20%、EB年增≥22%","action":"重跑判斷","source_freq":"季度","date":"2027-01"}],"kill_metrics":[{"metric":"每TB平均售價年增率","bear_threshold":"連2季<+5%或任一季轉負→清倉","window":"每季財報","source":"公司法說會（財務長揭露）","last_status":"ok"},{"metric":"Non-GAAP毛利率","bear_threshold":"連2季年減且<50%→減碼一半","window":"每季財報","source":"公司財報新聞稿","last_status":"ok"},{"metric":"EB出貨年增率","bear_threshold":"FY2027下半年仍<20%→不加碼","window":"至2027年7月FY2027第四季","source":"公司法說會","last_status":"warning"},{"metric":"首代HAMR兩家超大規模客戶認證","bear_threshold":"延後到2027年第二季以後→維持觀望","window":"2027年3月至6月","source":"公司法說會","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#1","reason":"來源是通路商部落格二手轉引Bloomberg。2026-10-22法說會執行長一手說明：高容量領先平台全用自製磁頭，外購磁頭只用在低容量機種。這項依賴對自製能力最弱的Toshiba約束更大，不構成本公司的供應單點"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-14.88, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"循環股倉位上限3%，首倉1/3","requires_critic":[],"rearm_trigger":"股價≤$320（約9.4倍基準FY2028每股盈餘34元）且最新一季每TB均價年增≥+10%→首倉1/3；或HAMR量產後連兩季每TB均價年增≥+10%→重跑判斷","exec_line":"觀望。卡住的是盈餘分母爭議（高峰或中循環）：等股價到320元以下且價格證據仍在，或等HAMR量產後的價格證據；未持有不追，持有者以每TB均價年增轉負為清倉線"},"reasoning":{"industry":"2026年9月季（逐字稿2026-10-22財務長）營收44億美元，年增55%。雲端39億美元占88%、年增54%；Client 3.2億美元占7%、年增119%；Consumer 1.93億美元占5%、年增19%。毛利率58.1%，營業利益率49.1%。每TB均價年增28%，EB出貨年增22%，增量毛利率逾80%。事實表的最新季數字仍停在2026年6月季：營收37.47億美元、Non-GAAP營益率44.2%、毛利率54.4%。8月給的9月季指引是營收41億美元、毛利率55%～56%、EPS 4.00，三項都超過。產業時鐘判在III過熱，依據不看股價：毛利率創紀錄並指引再升到60%～61%，近線交期拉長到逾52週，第三名Toshiba開始擴產，價格漲幅還在加速。供需耐久度判週期性將反轉。雙寡頭不增單位產能、長約延到2027～2028年屬結構面，但財務長自承越遠期的長約，價格條款覆蓋越少。Toshiba擴產與雙寡頭HAMR放量會在2028年前後讓供給追上，供給可逆性中等。議價權方面，上游的高容量平台磁頭與碟片自製，但DRAM與NAND投入成本上漲，壓縮每TB成本降幅；下游前十大客戶占73%，三家各占16%、15%、13%，買方高度集中。單點依賴：前三大客戶合計44%，任一家調整供應比例就是集中度風險；護城河證據是重新認證週期與長約。","moat":"執行力給8分。9月季營收、毛利率、EPS全數超過8月指引；40TB ePMR是史上最快的一次換代，預計12月季占近線出貨約30%、3月季約50%；首代HAMR預計2027年第一季完成兩家超大規模客戶認證。定價力給6分。眼前每TB均價年增28%，但FY2023同一事業毛利率曾低到22%，說明定價力撐不過整個循環；長約只鎖基準量，越遠期價格覆蓋越少。合計約7分，評B。同業ROIC差距無法呈現：事實表的同業都是快閃記憶體廠，沒有Seagate與Toshiba，所以改用份額軸。2026年9月季EB年增22%，法說會上UBS分析師指出同業約在三成中段，管理層沒有否認，只說會在6～8季內加速；TrendForce預期Seagate在2028年成為最大供應商。執行面判穩定，定價力短期擴大但不能認定可持續，合判持平。威脅三項都是點對點：Toshiba擴產、HAMR落後、快閃長期替代。","growth":"成長拆解是價格大於量：每TB均價年增28%，EB出貨年增22%，回購是次要因素，沒有併購。共識EPS由FY2027的24.84元、FY2028的39.21元到FY2029的50.71元，FY2027到FY2029年化約43%。若以FY2026基期約9.96元計（2026-07-30快照，當時FY1仍指FY2026），三年年化約72%，遠超以再投資支撐的內生上界。缺口歸因於利益率擴張，也就是漲價延續，屬依賴價格的成長。財務長稱未來3～4季每TB均價仍有上漲空間，之後會放緩。衰退訊號亮兩項：核心份額落後同業，EPS成長顯著高於營收成長。高頻寬硬碟仍在送樣、商業定價結構未定，實體AI只有客戶需求的描述，都不能算成已驗證的第二曲線。","governance":"6月季自由現金流12.81億美元（營運現金流13.89億、淨資本支出1.08億）。9月季自由現金流14億美元，回饋股東11億美元；季配息由0.15元調高17%到0.175元。期末淨現金5億美元，2028年到期的可轉債已大幅減少。SBC單季4,500萬美元，占營收1.2%。稀釋股數由3.83億股降到12月季指引的3.80億股。FY2026的GAAP淨利93億美元含非營業利得，自由現金流對淨利的轉換率不具意義；改看TTM自由現金流利潤率27.18%對營業利益率35.6%，轉換正常。風險有兩點：在高峰價位大量回購，若循環反轉，回購的價值會打折；Kioxia合併若以股票支付逾200億美元，約占市值15%，會稀釋股本並重新引入NAND循環。","valuation":"股價343.67元，是FY2027共識24.84元的13.84倍、FY2028共識39.21元的8.8倍。8.8倍要算便宜，前提是這組盈餘屬於中循環；但毛利率創紀錄、還指引再升，分母本身就是爭點，所以便宜的論證不成立。事實表沒有同業估值倍數，5年估值分位也查不到。賣方平均目標價483元，比現價高約40%；主要分布在500～1,050元，最高與最低相差2.1倍，若含疑似過時的250元則達4.2倍，分歧大，因此下調自身信心。12個月基準取FY2028每股盈餘34元乘11倍，得374元，上檔+8.8%。五年基準取FY2031每股盈餘34元乘12倍，得408元，上檔+18.7%，年化不到4%。共識近三個月修正149%是財年切換造成的假象，真正的FY1上修是19.37%。","premortem":"回撤推導如下。現價343.67元，距104週均線212.22元約−38%，距250週均線110.32元約−68%。FY2023同一硬碟事業EB年減26%、營收年減31%，毛利率掉到22%。本輪Bear終點是165元，約−52%。據此把最大回撤區間定在−50%到−70%。股價26週已跌14.88%，RSI 35.75，沒有過熱。8月財報優於預期，股價仍下跌5%，顯示預期已被墊高。8月法說會有四題未正面回答：營收是否見底、長約是否逐季調價、未來12個月多少近線長約要重新定價、指引為何低於競爭對手。10月執行長改口，承認長約有合約內漲價條款，但重新定價的比例仍未揭露。"},"plain":{"six":{"how_it_makes_money":"賺的是超大規模雲端業者與AI資料中心買近線硬碟的錢，雲端占營收88%。利潤卡在磁頭與碟片的面密度節點，目前價和量都在漲，但利潤主要來自漲價。","moat":"護城河方向判持平。自製磁頭碟片帶來的面密度是真機制，但EB出貨成長落後Seagate約10個百分點，HAMR也晚一步；目前的定價力強，主要是供需吃緊帶來的。","growth":"成長跑道中等。EB需求年增逾25%可信，但五年後的成長要靠價格延續，第二曲線（高頻寬硬碟、實體AI）還沒有營收。","capital":"資本配置中上。自由現金流幾乎全數回饋股東，股本緩降，SBC稀釋低；沒有併購可評，回購是否買在循環高檔待驗。","valuation":"現價要FY2028每股盈餘接近共識的39元，而且2029年後不明顯回落才划算。我只信到34元左右，估值合理偏貴。","how_wrong":"最可能看錯的地方，是把高峰盈餘當成中循環。若2028年供給追上後價格循環反轉，股價可能回撤五到七成。"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"追蹤","wait_for_price":true,"wait_for_price_condition":"等股價≤$320且最新一季每TB均價年增≥+10%，或HAMR量產後連兩季每TB均價年增≥+10%","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":343.67,"week26_return_pct":-14.88,"consensus_rev_3m_pct":149.4,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2027與FY2028共識盈餘建立在毛利率58%～61%與每TB均價年增約三成之上，FY2023同一事業毛利率只有22%；分母是高峰還是中循環，正是本檔的核心爭點"},"catalysts":[{"date":"2026-11-10","date_precision":null,"type":"regulatory","event":"中國中重稀土出口逐案核准的暫停期到期","impact":"中","watch":"是否延長；公司是否揭露供應影響"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"2026年12月季財報（指引營收51億美元、EPS 5.80元）","impact":"高","watch":"每TB均價年增、EB年增、2027年3月季指引"},{"date":"2027-03","date_precision":"month","type":"product","event":"首代HAMR完成兩家超大規模客戶認證","impact":"高","watch":"是否如期、是否折價"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"首代HAMR量產出貨（CY2027上半年）","impact":"高","watch":"EB年增是否回到25%以上"},{"date":"2028-03","date_precision":"quarter","type":"capacity","event":"Toshiba菲律賓擴產的目標期限（其FY2027）","impact":"高","watch":"Toshiba正式公告與報價行為"}],"_projected_from":"v19"}
```
