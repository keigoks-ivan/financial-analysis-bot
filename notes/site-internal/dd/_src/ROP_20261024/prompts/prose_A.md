你是 stock-analyst v20 的**散文層（prose）agent**，標的 ROP（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ROP　日期：2026-10-24　archetype：None　前份裁決：2026-07-10　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1518B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（547B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1127B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1730B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1491B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（650B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1236B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2068B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4330B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2358B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1518           3837-5482      5 條（2–6 內）  
s3                  8000         547           5217-7453      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4348          7456-10652      5 條（2–6 內）  
s6                 11000         650          7245-10350      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1236           1585-2264      3 條（2–6 內）  
s10                 5000        2068           2052-2932      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2358           2000-2642      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5806B；至少需散文≈39.19KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−42
−42%
−28
−28%
0
0.45%
0.5
0.6
0.74%
0.83
0.831%
0.95
01
1
1.1
1.6
1.639
2%
2
2.05
2.26
2.9
3
03
3.4
3.5
3.76
4%
4
4.309
4.36
4.5
4.88
4.972
5%
5
5.89
6%
06
6
6.4
6.4%
6.5%
7%
07
7
8%
8
8.05
8.4
8.4%
8.69%
8.7%
9
10%
10
10.9%
11%
11.4
11.5%
11.8
12
13%
13
13.86
14
14.20
15%
15
15.14%
16
17
17.5
17.7
17.8
17.83
18
18.822
19.6
19.61
19.91%
20%
21
21%
21.718
21.92%
22
22.34
22.36
23
23%
23.1%
23.2
23.5
23.8
24
24.1
24.4
24.57
24.6
24.6%
24.96%
25%
25
25.9%
26
26%
26.39
27.6
27.97%
28.29%
28.5
28.7%
29
29.05%
30
30%
30.5
30.8
31%
31.7
32
32.8
33%
33.2
33.7
34.3%
35%
35
36%
36.4%
36.4
37
37.2
37.2%
37.26%
39.8%
40
40%
42
43.7%
47%
49
50%
50
52
52.4%
56%
60
62%
65%
68%
68.9%
69.24%
69.53%
69.86%
70
70.0%
75%
79.025
80%
80.65
85%
90%
90
100
100%
104
130
150%
213
213.412
270
$310
317
317.2
340
341
344
350
355.94
360
379.55
380
393
438.14
445.92
459.77
$483
550
694
886
892.8
2025
2026
2027
2028
20261024
2,400
3,540
4,680
5,000
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
{"meta":{"ticker":"ROP","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Roper Technologies"},"oneliner":"美國利基垂直軟體收購平台，Q3有機成長7%、全年EPS指引年內三度上調，AI代理產品已大範圍上市但變現未證；股價半年漲24.6%、前瞻本益比19.6倍，基本面無損但價格先走，等回落再買。","thesis":{"H":[{"id":"H1","text":"垂直軟體工作流鎖定在AI代理普及後仍成立，AI成為公司自己的加值層而非替代品","2y":"企業軟體毛留存維持90%中段、兩軟體部門有機經常性營收≥6%","5y":"毛留存≥90%、核心旗艦未被AI原生對手系統性搶客","10y":null,"threshold":"毛留存≥90%；有機經常性營收≥6%","source":"季度法說（毛留存、有機經常性營收）","drift_rule":"有機經常性營收連2季<5%→削弱；毛留存跌破90%→反轉"},{"id":"H2","text":"AI代理產品在2027–2028年轉成可計量的增量訂閱收入，毛利維持在軟體水準","2y":"至少兩家旗艦AI訂單占比≥25%，TTM毛利率≥68%","5y":null,"10y":null,"threshold":"旗艦AI訂單占比≥25%；TTM毛利率≥68%","source":"季度法說（AI訂單占比）＋季報毛利率","drift_rule":"2027年底仍無AI收入或訂單量化揭露→削弱；TTM毛利率連2季<68%→反轉"},{"id":"H3","text":"自由現金流再部署（收購為主、回購為輔）維持每股自由現金流約兩位數成長，槓桿不失控","2y":null,"5y":"每股自由現金流年增≥8%、淨負債/EBITDA≤3.5倍、無重大商譽減損","10y":null,"threshold":"每股自由現金流年增≥8%；淨負債/EBITDA≤3.5倍","source":"公司法說與年報","drift_rule":"連續兩個年度每股自由現金流增速<6%→削弱；認列重大商譽減損→反轉"}],"R":[{"id":"R1","text":"AI原生垂直方案或通用代理在任務層繞過工作流，旗艦垂直留存或定價受壓，商譽面臨減損","h_ref":"H1","clock":"🔥","threshold":"企業軟體毛留存跌破90%或有機經常性營收連2季<5%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"id":"R2","text":"AI變現延後到2027年後、第三方模型成本吃掉增量毛利","h_ref":"H2","clock":"🔥","threshold":"TTM毛利率<68%或2027年中前仍無AI收入量化","evidence_refs":["supply_demand_durability#1","substitute_technology#1"]},{"id":"R3","text":"循環性業務拖累：Neptune表計組合偏機械式、Deltek政府承包市場不確定、DAT貨量未回","h_ref":"H1","clock":"⚡","threshold":"TEP分部有機成長連2季≤0或EBITDA利潤率<33%","evidence_refs":["end_markets#3"]},{"id":"R4","text":"私募買方回流抬高收購倍數，收購增量報酬向資金成本收斂、槓桿回升","h_ref":"H3","clock":"🐢","threshold":"淨負債/EBITDA>3.5倍，或單年收購逾40億美元且未揭露報酬","evidence_refs":[]}],"single_thing":{"description":"未來12–24個月以高倍數完成單筆逾50億美元、目標有機成長低於ROP母體（約6%）的大型收購","why_fatal":"收購是每股盈餘複利的主要引擎，單筆約相當兩年自由現金流（以營收年增8%、自由現金流約營收30%推算）；高價買進低成長資產會同時壓低增量報酬、推高槓桿並鎖住之後兩三年的部署能力，而且無法逆轉。","if_happens":"宣布當季減碼至半倉；首年每股自由現金流成長仍≥8%且淨負債/EBITDA回到3.5倍以下才回補。","how_monitor":"8-K重大收購公告（成交金額、倍數）；法說揭露的目標成長與綜效；淨負債/EBITDA。","probability":"約15%：管理層稱未來12個月可部署逾60億美元、對2027年收購審慎樂觀，大型交易宣布機率不低；但要同時出現高倍數與低成長目標才算，且管理層重申只買贏家。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":17.83,"peg_fy2":2.05,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":22.34,"FY2027E":24.57,"FY2028E":26.39},"fy_end_month":12,"eps_basis":"公司調整後稀釋EPS（排除收購無形資產攤銷等）；FY2026E–FY2028E為Koyfin共識，家數事實表未涵蓋；FY2025A調整後實際值事實表未涵蓋（年度表只有GAAP 14.20美元，口徑不同不可代入）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROP_20261024/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高毛利經常性軟體收入＋以自由現金流持續收購的資本配置平台，股東報酬取決於下一筆收購的增量報酬"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：企業軟體毛留存連續多季90%中段、有機經常性營收8%（Q3法說）；週期性部分集中在Neptune表計換表週期與DAT貨運需求，兩者合計不是營收主體。","bargaining":{"up":"對上游：AI功能依賴OpenAI、Anthropic、Google、Microsoft等模型供應商，10-K明言漲價未必能轉嫁；Neptune有青銅錠成本通膨（Q2法說）。","down":"對客戶：無單一客戶占營收10%以上，毛留存90%中段，議價力在公司這邊。","geo":"美國以外營收13%，地緣與關稅曝險集中在TEP硬體。"},"profit_pool_dir":"垂直軟體利潤池可能有一部分流向模型供應商，但目前毛利率未見移轉（TTM 69.53%）；方向待2027年AI收費規模揭露後才能判斷。","tam_table":{"expanded":false,"reason":"29家事業分散在數十個利基垂直，事實表未涵蓋任何垂直的TAM、滲透率或利潤池占比；唯一的TAM數字（Vertafore代理AI讓可服務市場約翻倍）是管理層自承的推測，不能承重；成長判斷改以有機經常性營收與毛留存承重。"}},"moat":{"mechanism":"工作流嵌入＋專有資料（例如Strata數十年累積的醫院總帳對照與病患層級成本會計）＋產業合規需求，形成高轉換成本；可證方向用毛留存與對同業的利潤率差距。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力穩定：毛留存連續多季90%中段（Q2、Q3法說）、Q3有機成長7%、有機經常性營收由7%升到8%；定價力穩定：年度毛利率FY2022 69.86%→FY2025 69.24%小幅下移、TTM 69.53%，未見擴大也未破位；兩維皆穩定，方向判為不變。","peer_na_reason":"同業ROIC與投入資本事實表未涵蓋，只能以毛利率、營益率、FCF利潤率比較；同業前瞻本益比也未涵蓋。","threats":[{"level":"🟡","text":"AI原生垂直方案或通用代理在任務層繞過既有工作流，先壓定價再侵蝕留存；目前留存未見受損，若旗艦垂直公開失去大型客戶即升級為生態攻擊。","p":30,"evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"level":"🟡","text":"第三方模型供應商漲價而公司無法轉嫁，AI加值功能的毛利被上游拿走；緩解是每個產品都有模型路由可切換較小或開源模型。","p":25,"evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"私募買方回到收購市場抬高倍數，收購增量報酬向資金成本收斂。","p":25,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是律所會計、保險代理、醫院財務人員，決策者與付款者是同一機構的管理層，三角色都在；工作屬計費、合規、結帳等不能延後的需要而非想要。2025年無客戶占營收10%以上。例外是Neptune水表的換表時點可延後（新冠後換表高峰正在消化）。"},{"item":"決策層級","level":"🟡","text":"以整套系統衡量替代性仍低：企業軟體毛留存連續多季90%中段，Deltek Costpoint地端停止支援反而推動客戶升級上雲。但AI代理把替代的最小單位從整套系統縮到單一任務（例如計費描述、保單處理），對手可在任務層切入，現有留存數字還反映不到這一層。"},{"item":"價值鏈分配","level":"🟡","text":"AI功能依賴少數模型供應商，10-K明言漲價未必能轉嫁；關鍵互補品集中在少數供應商，是價值被上游拿走的典型風險。緩解是每個產品都有模型路由，管理層稱代理工具毛利與軟體毛利相當（Q3法說）。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業與機構，不是消費者必需品，大幅漲價的政治敏感度低；子公司PowerPlan的反壟斷訴訟已於2025年1月以2,400萬美元和解結案，未見現行反壟斷調查。Neptune售予受費率審議的水公用事業，屬間接約束，占比有限。"}],"roiic":"事實表未涵蓋：近年收購金額與被收購事業的獲利貢獻未揭露。可得線索僅有管理層稱Q3三筆小型收購成長快於母體、合併綜效後報酬很有吸引力，屬未量化說法。本次以收購稅後現金報酬約7%–8%作為工作假設（未驗證）。","reinvest_rate":"推估約80%–100%的自由現金流再投入收購或回購：全年自由現金流約營收30%（Q3法說），管理層稱未來12個月可部署資本逾60億美元；比例是推論，非揭露值。","endo_ceiling":10,"formula_note":"內生成長上界約10%＝有機成長約6%（全年指引，幾乎不耗資本：資本支出加資本化軟體約營業現金流4%）＋收購再部署約4點（再投資率約九成×假設增量報酬約7%–8%，換算到每股盈餘再扣利息成本與整合期稀釋，保守取4點）。帳面ROIC下限：FY2025營業利益約22.36億美元（79.025億×28.29%）×（1−21%稅率）≈17.7億；投入資本以總資產上限約344億（商譽213.412億÷62%）計，ROIC約5%，未加回攤銷，屬保守下限。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","ROP":69.53,"CSU.TO":37.26,"TYL":47.21,"JKHY":43.65,"AME":36.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","ROP":27.97,"CSU.TO":17.86,"TYL":15.14,"JKHY":24.96,"AME":25.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","ROP":30.93,"CSU.TO":21.92,"TYL":29.05,"JKHY":19.91,"AME":23.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","ROP":null,"CSU.TO":null,"TYL":9.4,"JKHY":6.93,"AME":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"CSU.TO","gm":37.26,"om":17.86,"fcf_margin":21.92,"rd_intensity":null,"strategy_note":"同為垂直軟體收購平台，毛利率37.26%、FCF利潤率21.92%低於ROP，但兩家成本列報口徑可能不同，利潤率差距不宜全歸因於護城河；它是收購市場上最直接的出價對手。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"TYL","gm":47.21,"om":15.14,"fcf_margin":29.05,"rd_intensity":9.4,"strategy_note":"政府垂直軟體，營益率15.14%遠低於ROP、FCF利潤率29.05%接近，帳面利潤與現金之間的落差比ROP大；客群與Deltek的政府承包業務相近，是政府端上雲與AI節奏的對照。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"JKHY","gm":43.65,"om":24.96,"fcf_margin":19.91,"rd_intensity":6.93,"strategy_note":"銀行核心系統供應商，營益率24.96%、FCF利潤率19.91%，是單一垂直深耕的對照組；ROP本季新收購的c. myers也面向銀行與信用合作社。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"AME","gm":36.36,"om":25.9,"fcf_margin":23.21,"rd_intensity":null,"strategy_note":"工業儀器收購平台，營益率25.9%接近ROP的TEP分部，也是Indicor儀器業務的買家；只用來對照ROP硬體分部，不是軟體護城河的對照。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（有機約6%：經常性營收與模組加購）＋價（AI點數與加購訂閱、Deltek上雲加價）＋併購（今年約1點）＋回購（前八個月約32億美元，Q3暫停）","runway_years":"事實表未涵蓋（各垂直滲透率未揭露）","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段內生上界約10%：有機約6%＋收購再部署約4點；共識FY1到FY3年化約8.7%落在上界內。","segments":[{"item":"應用軟體（Q3）","value":"營收年增7%、有機6%、EBITDA利潤率43.7%（年增30bp）；Q4預期有機中個位數偏上"},{"item":"網路軟體（Q3）","value":"營收年增8%、有機5%、EBITDA利潤率52.4%（年減130bp，核心大致不變）；DAT加速，Q4有機略高於Q3"},{"item":"TEP（Q3）","value":"營收與有機皆年增10%、EBITDA利潤率34.3%（年減90bp）；Neptune機械式表計組合偏高，Q4有機中個位數"},{"item":"Q2營收規模","value":"應用軟體11.8億、網路軟體4.309億、TEP 4.972億美元"}],"decay_signals":["產業估值倍數下移：軟體類股2026年初因AI拋售倍數下移，第三方報導股價一度自高點跌近40%，亮燈","毛利率：年度數字FY2022 69.86%→FY2025 69.24%連三年小幅下移（季度年比資料事實表未涵蓋），接近亮燈","EPS成長高於營收成長：Q3調整後EPS年增15%、營收8%，差距來自回購與利息，屬單季未連續，暫不亮燈","其餘類別（市占縮減、提價後量減、FCF對淨利過低、SBC過高、TAM被壓縮、維護性資本支出過高、停止投資）證據包內未見亮燈"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"回購","value":"八個月累計約32億美元；Q2約12億美元、360萬股、均價約341美元；Q3暫停"},{"item":"收購","value":"上半年兩筆小型約5,000萬美元；Q3三筆（iPipeline、Procare、Strata的補強）共4.36億美元"},{"item":"處分收入","value":"Indicor儀器業務售予AMETEK稅後約12億美元；流量控制業務售予Xylem稅前約6億美元，預計Q4入帳"},{"item":"槓桿","value":"淨負債/EBITDA：Q2末3.4倍→Q3末2.9倍；35億美元循環額度動用13億美元"},{"item":"股息","value":"近12個月殖利率0.831%"},{"item":"可部署資本","value":"未來12個月逾60億美元"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"收購金額與被收購事業獲利未揭露；Q3三筆小型收購管理層稱報酬很有吸引力，未量化","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"Q2回購均價約341美元，對FY1共識EPS 22.34美元的盈餘收益率約6.5%；十年期公債殖利率事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"前九月SBC 1.639億美元，以現價換算約37萬股；Q2單季回購360萬股，淨稀釋為負","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY1調整後EPS）＋PEG","tier":"高品質垂直軟體收購平台","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業前瞻本益比或目標價；終端倍數改以本檔現值19.6倍與前份引用的CSU約17.5倍對照，後者未於本包更新。"},"fwd_pe":19.61,"peg":2.26,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比19.61倍÷共識EPS年化成長8.69%＝PEG 2.26，高於2屬偏貴；倍數已高於前份重定性目標16倍；未判最貴一級，因共識EPS仍在上修（FY1+0.45%、FY2+0.74%）且FCF利潤率約31%，盈餘品質支撐目前倍數。","upside_short_pct":8.4,"upside_mid_pct":36.4},"trap_analysis":{"verdict":"🟡","label":"AI替代與收購報酬未證"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"10-K風險因子明列可能出現新競爭者、產品線可能受包括AI在內的新技術威脅；若替代技術出現，約213億美元、占總資產約62%的商譽可能減損。","assumption":"工作流嵌入與專有資料讓AI成為公司自己的加值層，而不是繞過它的替代品。","consequence":"五年後虧50%最可能的故事：通用代理在計費、保單處理等任務層以低價切入，留存先跌破90%，市場把ROP重新定為衰退中的收購平台，倍數跌到12–13倍、EPS停滯，同時認列商譽減損。","ruling":"反駁但不排除：企業軟體毛留存連續多季90%中段、Q3有機經常性營收8%、21家軟體事業中17到18家已上市代理產品且管理層稱無明顯失敗，現有數字與替代故事方向相反；但留存是落後指標，任務層替代要一到兩年才會反映。","watch":"企業軟體毛留存跌破90%；兩軟體部門有機經常性營收連2季低於5%（季度法說）。","evidence_refs":["substitute_technology#0","competitive_share_entrants#1"]},{"view":"論點成功但股東經濟變差","evidence":"10-K揭露AI產品依賴OpenAI、Anthropic、Google、Microsoft，供應商漲價未必能轉嫁；AI代理產品2026年不構成重大營收，變現是2027年議題，曾有第三方因AI耐久性疑慮將合理價由694下調至550美元（該頁面日期與股價欄位不一致，只採其敘述部分，與Q2法說稱AI今年不會形成實質營收一致）。","assumption":"AI功能能以加購或點數方式收費，毛利維持在軟體水準；收購能在合理倍數成交。","consequence":"AI產品成功上市、留存守住，但收入只是把原有授權費換成點數，模型成本吃掉增量毛利；加上60億美元收購在私募回流後以高倍數成交，每股自由現金流成長掉到5%以下。","ruling":"部分採納：管理層稱代理工具毛利與軟體毛利相當、所有產品都有模型路由可切換，但Q2法說也說AI工具支出年化約為1月的3倍；毛利率是可結算的數字，TTM 69.53%尚未受損，先以門檻監測。","watch":"TTM毛利率跌破68%；2027年指引是否揭露AI收入或訂單占比；大型收購的成交倍數。","evidence_refs":["substitute_technology#1","supply_demand_durability#1"]},{"view":"價格已反映太多","evidence":"26週漲24.6%、RSI 80.65；前瞻本益比19.61倍已高於前份重定性目標16倍；賣方平均目標約445.92美元，與現價相當；2026年初股價曾因AI拋售自高點跌近40%。","assumption":"重定性已大致完成，後續報酬主要靠EPS成長。","consequence":"即使論點全部成立，五年基準報酬約年化7%，低於持有高品質複利股的期望；若AI疑慮再起，倍數回到前份的15–16倍即跌20%以上。","ruling":"採納：現價不追，等價格回到約17倍前瞻本益比附近再分批。","watch":"前瞻本益比回到17倍以下（約380美元），或FY2027共識上修使現價對應倍數下降。","evidence_refs":["substitute_technology#2"]}],"max_dd":{"lo":-42,"hi":-28,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 355.94 → 本次 438.14（+23.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=355.94","side_b":"本次 price_at_dd=438.14","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟡→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟡→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 355.94 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 355.94 美元：Bull 價 886、Bear 價 270，五年期望值 +70.0%，基準年化 11.5%，不對稱比 6.4","side_b":"本次情境、股價仍用 355.94 美元：Bull 價 892.8、Bear 價 317.2，五年期望值 +68.9%，基準年化 10.9%，不對稱比 13.86","ruling":"先換情境、股價不動：五年期望值少 1.1 個百分點，基準年化少 0.6 個百分點。不對稱比由 6.4 變為 13.86。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 355.94 美元：五年期望值 +68.9%，基準年化 10.9%，不對稱比 13.86","side_b":"本次情境、股價 438.14 美元：五年期望值 +37.2%，基準年化 6.4%，不對稱比 3.76","ruling":"再換股價、情境不動：起點價上漲 23.1%，五年期望值少 31.7 個百分點，基準年化少 4.5 個百分點，不對稱比由 13.86 降到 3.76。合計五年期望值比前份少 32.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"AI是擴大市場還是替代威脅","cause":null,"prior_field":null,"side_a":"管理層（2026-10-22 Q3法說，Neil Hunn）：AI建立在領域專長、嵌入工作流、專有資料與客戶信任上，能擴大可服務市場並拿到更多創造的價值；CentralReach約75%、Aderant約25%的訂單與AI相關。","side_b":"10-K風險因子：新競爭者與AI可能削弱產品線價值、AI能力可能快速商品化；第三方因AI耐久性疑慮下調合理價。","ruling":"方向相反，暫採管理層側：依據是可結算的數字（毛留存90%中段、有機經常性營收由7%升到8%、TTM毛利率69.53%）目前都與替代故事相反；但這些是落後指標，裁定有效到2027年第二季，屆時要看到AI訂單擴散到兩家以上旗艦。現在就買的最強論證：全年EPS指引三度上調、每股自由現金流兩位數成長、私募賣方估值鬆動讓60億美元可部署資本有機會以較好價格成交，等回落可能錯過；本檔仍選等，因為這些利多已反映在19.6倍。","evidence_level":"公司法說與10-K（一手）對第三方評論","settle_metric":"企業軟體毛留存；旗艦AI訂單占比","if_then":["若2027年上半年毛留存維持90%以上且兩家以上旗艦揭露AI訂單占比≥25%→即使價格未回落也以三分之一部位分批買進","若毛留存跌破90%或有機經常性營收連2季低於5%→已持有者減碼至半倉並凍結加碼"],"evidence_refs":["competitive_share_entrants#1","supply_demand_durability#1"]},{"axis":"Neptune下半年展望改口","cause":null,"prior_field":null,"side_a":"2026-07-23 Q2法說，Neil Hunn：表計業務預計下半年回到成長。","side_b":"2026-10-22 Q3法說，Neil Hunn：下半年營收改為略低於先前溫和成長的展望，機械式表計組合偏高、可能延續到Q4，稱屬暫時性；Jason Conley稱靜態表計管線仍強，是專案遞延。","ruling":"可調和（程度差異）：出貨數量接近預期，落差在組合與大型專案遞延；暫時性歸因不採信也不否定，標未證、監測；若2027年上半年TEP有機成長仍≤0，歸因證偽，下修TEP成長假設。","evidence_level":"公司法說（一手）","settle_metric":"TEP分部有機成長與EBITDA利潤率","if_then":["若2027年Q1、Q2 TEP有機成長皆≤0→空頭情境機率由25%調到30%並停止加碼"],"evidence_refs":["end_markets#3"]},{"axis":"關稅與供應鏈","cause":null,"prior_field":null,"side_a":"10-K：銷售受出口管制、制裁與新增或報復性關稅影響；第三方彙整另提單一來源供應商與少數雲端平台依賴。","side_b":"10-K：美國以外營收13%；TD Cowen稱關稅風險可忽略（美國曝險約85%）。","ruling":"可調和：風險條款為制式揭露、未附金額，第三方彙整未附申報原文；實際曝險集中在TEP硬體（Q2法說提到Neptune青銅錠投入成本通膨），軟體幾乎不受影響。不預測關稅，改用吸收失敗門檻：TEP EBITDA利潤率跌破33%（Q3 34.3%）視為成本轉嫁失敗。","evidence_level":"10-K（一手）對賣方與第三方彙整","settle_metric":"TEP EBITDA利潤率","if_then":["若TEP EBITDA利潤率連2季低於33%→下調TEP成長與利潤率假設、空頭情境機率加5點"],"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1","reg_tariff_export#1","reg_tariff_export#2"]},{"axis":"產業態勢：競爭／結構／其他","cause":null,"prior_field":null,"side_a":"競爭面：AI原生方案與通用代理可能在任務層切入（10-K風險因子）。","side_b":"結構面：毛留存90%中段、Deltek地端停止支援推動上雲加價、私募賣方估值鬆動改善收購環境（Q2、Q3法說）。","ruling":"雙向拉鋸：競爭惡化尚未出現在數字，結構性轉好有一手證據；其他結構變數中，反壟斷（PowerPlan訴訟已和解）與通路（直銷為主未見轉變）都屬靜態。","evidence_level":"公司法說與10-K（一手）","settle_metric":"毛留存；有機經常性營收","if_then":["若出現旗艦垂直公開失去大型客戶給AI原生對手→改判競爭惡化中，護城河方向下修並停止買進"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"前份漂移：股價帶動的欄位","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份（2026-07-10）：股價355.94美元、估值中性、進場；最大回撤−42%、多空機率各25%。","side_b":"本次：股價438.14美元（約+23%）、前瞻本益比19.61倍、估值偏貴、改為等價格回落；最大回撤範圍−28%到−42%、多空機率維持各25%。","ruling":"基本面在這三個多月轉好（全年EPS指引再上調、有機成長7%），估值結論變貴完全來自股價上漲；機率不動是因為新證據兩面都有（留存與經常性營收轉好、Neptune改口），互相抵銷；回撤下緣不變，上緣改以空頭情境終點推得。","evidence_level":"價格與共識資料","settle_metric":"前瞻本益比","if_then":["若股價回落至約380美元且毛留存未破90%→恢復分批買進"],"evidence_refs":[]},{"axis":"前份漂移：基本面欄位維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質評級B、價值陷阱中等、護城河方向不變、五年後跑道中等、品質複利成長、未列循環位置。","side_b":"本次：六欄皆維持。","ruling":"Q3新證據（有機經常性營收8%、毛留存90%中段、17到18家軟體事業已上市AI代理產品、Neptune改口）正負互抵，不足以改變任何一欄；循環位置仍不適用，主體是經常性軟體收入。","evidence_level":"公司法說（一手）","settle_metric":"毛留存；有機經常性營收","if_then":["若2027年上半年兩家以上旗艦AI訂單占比≥25%→跑道判斷上修一級"],"evidence_refs":[]},{"axis":"加碼觸發條件改寫","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼觸發：站回 W104（~$483）或連 2 季有機成長 ≥5% 且 Deltek/DAT 回穩→加碼；跌至 ~$310 且留存率/毛利未損→逢低加碼。","side_b":"回落至約380美元（約17倍FY1共識）且毛留存維持90%以上→分批買進；或2027年指引≥24.57美元且兩家以上旗艦AI訂單占比≥25%→分批加碼。","ruling":"前份加碼條件中連2季有機成長≥5%已達成（Q2 5%、Q3 7%），但Deltek、DAT回穩管理層仍在觀察；同時股價已漲約23%、本益比超過前份目標，原條件會在偏貴價位觸發加碼，因此改為價格錨加證據錨。站回104週均線一條刪除，現價438.14低於104週均線459.77，在估值偏貴時用均線觸發加碼不合理。","evidence_level":"公司法說與價格資料","settle_metric":"股價；毛留存；2027年指引","if_then":["若2027年指引中點低於24.57美元→加碼條件只保留價格錨並把價位下移至約340美元"],"evidence_refs":[]},{"axis":"減碼與清倉門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼或清倉的數字門檻。","side_b":"本次設定：企業軟體毛留存跌破90%、兩軟體部門有機經常性營收連2季<5%、淨負債/EBITDA>3.5倍、TTM毛利率<68%；任一發生即減碼至半倉，毛留存跌破90%且有機經常性營收連2季<4%即清倉。","ruling":"前份只有假設與風險的漂移條件，沒有落成可執行的減碼、清倉數字，本次補上。","evidence_level":"方法調整","settle_metric":"四項門檻指標","if_then":["若四項中任一項觸發→減碼至半倉並凍結加碼"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）。","side_b":"本次Single Thing：未來12–24個月以高倍數完成單筆逾50億美元、目標有機成長低於ROP母體的大型收購。","ruling":"前份未指定；本次以數學上最大的單一離散事件指定：收購是每股盈餘複利的主要引擎，單筆約相當兩年自由現金流，錯一筆會同時拉低增量報酬並推高槓桿，且無法逆轉。","evidence_level":"方法調整","settle_metric":"8-K重大收購公告的金額與倍數","if_then":["若宣布此類收購→當季減碼至半倉，首年每股自由現金流成長仍≥8%才回補"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"企業軟體毛留存與有機經常性營收是工作流鎖定的結算數字","type":"假設驗證","maps_to":"H1","metric":"企業軟體毛留存；兩軟體部門有機經常性營收年增","threshold":"毛留存≥90%且有機經常性營收≥6%","action":"兩項守住→論點維持；有機經常性營收連2季<5%→減碼至半倉","source_freq":"季度法說","date":null},{"n":2,"text":"AI變現從訂單走進營收","type":"假設驗證","maps_to":"H2","metric":"旗艦AI相關訂單占比；AI收入揭露","threshold":"2027年中前至少兩家旗艦AI訂單占比≥25%","action":"達成→即使價格未回落也以三分之一部位分批買進；2027年底仍無量化揭露→不加碼","source_freq":"季度法說","date":"2027-07"},{"n":3,"text":"模型成本是否被上游拿走","type":"風險","maps_to":"R2","metric":"TTM毛利率","threshold":"<68%（TTM 69.53%）","action":"減碼至半倉並凍結加碼","source_freq":"季報","date":null,"evidence_refs":["substitute_technology#1"]},{"n":4,"text":"Neptune與Deltek等循環性業務拖累","type":"風險","maps_to":"R3","metric":"TEP分部有機成長；TEP EBITDA利潤率","threshold":"有機成長連2季≤0或利潤率<33%","action":"停止加碼，空頭情境機率調至30%","source_freq":"季度法說","date":null,"evidence_refs":["end_markets#3"]},{"n":5,"text":"大型收購的倍數與目標成長","type":"Single Thing","maps_to":"Single Thing","metric":"單筆收購金額、成交倍數、目標有機成長","threshold":"單筆>50億美元且目標有機成長低於母體約6%","action":"宣布當季減碼至半倉；首年每股自由現金流成長仍≥8%才回補","source_freq":"8-K與季度法說","date":null},{"n":6,"text":"價格回落到合理區","type":"估值rearm","maps_to":"H3","metric":"股價；前瞻本益比","threshold":"≤380美元（約17倍FY1共識）且毛留存≥90%","action":"首批三分之一部位","source_freq":"每日股價＋季度法說","date":null},{"n":7,"text":"倍數過度擴張時收割","type":"減碼","maps_to":"H3","metric":"前瞻本益比","threshold":"≥24倍且共識EPS未同步上修","action":"減碼三分之一","source_freq":"每日","date":null},{"n":8,"text":"工作流鎖定失守","type":"清倉","maps_to":"H1","metric":"企業軟體毛留存＋有機經常性營收","threshold":"毛留存<90%且有機經常性營收連2季<4%","action":"清倉","source_freq":"季度法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":9,"text":"Q4財報與2027年指引","type":"複審日期","maps_to":"H1","metric":"2027年調整後EPS指引","threshold":"指引中點≥24.57美元","action":"重跑完整研究","source_freq":"年度","date":"2027-01"}],"kill_metrics":[{"metric":"企業軟體毛留存率","bear_threshold":"跌破90%（目前90%中段）","window":"任一季","source":"季度法說","last_status":"ok"},{"metric":"兩軟體部門有機經常性營收年增","bear_threshold":"連2季<5%（Q3約8%）","window":"連續2季","source":"季度法說","last_status":"ok"},{"metric":"淨負債/EBITDA","bear_threshold":">3.5倍（Q3末2.9倍）","window":"任一季末","source":"季度法說／10-Q","last_status":"ok"},{"metric":"TTM毛利率","bear_threshold":"<68%（TTM 69.53%）","window":"TTM滾動","source":"10-Q／季報","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=24.6, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='❌'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」","row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[],"rearm_trigger":"回落至約380美元（約17倍FY1共識）且毛留存維持90%以上→分批買進；或2027年指引≥24.57美元且兩家以上旗艦AI訂單占比≥25%","exec_line":"現價不追；回落約380美元首批三分之一，340美元以下且毛留存未損再加三分之一，2027年指引不低於24.57美元後補足；毛留存跌破90%即停止買進。"},"reasoning":{"industry":"分部（Q3法說）：應用軟體營收年增7%、有機6%、EBITDA利潤率43.7%；網路軟體年增8%、有機5%、利潤率52.4%；TEP（Neptune水表、NDI量測、Verathon醫材）年增10%、有機10%、利潤率34.3%。Q2三分部營收分別為11.8億、4.309億、4.972億美元，應用軟體約占56%。集中度：2025年無單一客戶占任一分部或公司營收10%以上，美國以外營收13%，沒有單點客戶依賴；上游單點依賴在第三方大型語言模型供應商。產業時鐘判在擴張期（II）：依據是兩軟體部門有機經常性營收由Q2的7%升到Q3的8%、企業核心訂單近12個月中個位數成長，加上私募賣方估值預期鬆動使收購環境轉好，不是看股價。供需耐久性：軟體端屬結構性持久（企業軟體毛留存連續多季在90%中段）；週期性將反轉的部分集中在Neptune表計（新冠後換表高峰的消化期）與DAT貨運（供給面回升、貨量未回）。資本輕：前九月資本支出3,540萬加資本化軟體4,680萬美元，對營業現金流18.822億美元約4%，管理層預估全年自由現金流約營收30%。","moat":"執行力給8分：Q3有機成長7%、全年EPS指引年內三次上調（累計較原始指引高0.95美元）、21家軟體事業中17到18家已有代理式AI產品上市，管理層稱尚無明顯失敗的上市案。定價力給7分：毛利率FY2022 69.86%到FY2025 69.24%小幅下移，TTM 69.53%，沒有擴張證據；Vertafore改用價值點數計價、Strata以加購訂閱賣AI功能，屬試探提價但尚未反映在數字。同業ROIC事實表未涵蓋，只能比利潤率，因此等級壓在B不往上。報酬持續期：高利益率×低周轉，資產負債表約六成是商譽，帳面ROIC偏低，股東報酬主要取決於下一筆收購的增量報酬，而這個數字公司未揭露。四檢查點中需求基礎值與社會容忍度為綠，決策層級與價值鏈分配為黃，黃燈都與AI有關：替代可能先在單一工作流任務出現，模型成本可能被上游拿走。","growth":"成長組成：量與價的有機成長約6%（全年指引，Q3單季7%），併購今年約貢獻1點，回購前八個月約32億美元但Q3暫停、轉向收購。共識調整後EPS：FY2026 22.34、FY2027 24.57、FY2028 26.39美元，FY1到FY3年化約8.7%；FY2025調整後基期事實表未涵蓋，三年CAGR無法依公式算，改用兩年年化。內生上界約10%（見護城河段），共識低於上界，缺口為負，不需依賴倍數擴張。跑道：各垂直滲透率未揭露，年數事實表未涵蓋；Aderant在法律事務所營運軟體的份額由35%升到65%（Q2法說），說明部分旗艦已高滲透，新的成長要靠AI加值與上雲加價，而Vertafore代理AI讓可服務市場約翻倍是管理層自承的推測。衰退信號亮一個、接近亮一個：軟體類股估值倍數在2026年初AI拋售中系統性下移；年度毛利率連三年小幅下移。","governance":"現金：前九月營業現金流18.822億美元，扣資本支出與資本化軟體後自由現金流約18億，管理層預期全年自由現金流約營收30%、每股自由現金流與調整後EPS同步或略好。Q3自由現金流8.05億美元年減4%，原因是2025年發行債券的票息時點與Illumia導入ERP造成收款延遲，部分可能延到2027年第一季（Q3法說），列為未證的一次性歸因，若2027年第一季自由現金流仍年減即證偽。去向：回購（Q3暫停，授權仍有餘額）、收購（Q3三筆共4.36億美元）、股息（殖利率0.831%）、還債（槓桿降0.5倍）。SBC前九月1.639億美元，以現價換算約37萬股，遠小於Q2單季回購的360萬股，淨股數下降。三項計分：收購增量報酬未揭露、無法判定；回購買入收益率以341美元對FY1共識EPS約6.5%，十年期公債殖利率事實表未涵蓋、無法判定；SBC淨稀釋為負，通過。","valuation":"前瞻本益比19.61倍（FY1共識22.34美元），以FY2共識24.57美元計約17.8倍。PEG以FY1到FY3共識年化8.69%計約2.26。26週漲24.6%、RSI 80.65，動能過熱。五年歷史分位所需的估值歷史高低點事實表未涵蓋，分位留空。賣方：16位分析師平均目標約445.92美元（區間約350–550），評等9買9持有2賣（家數與16位不一致，來源本身有誤差），BMO於10月以持有、目標393美元；現價已在賣方均值附近，賣方均值不支持進一步上漲；全距550÷350約1.6倍，未達分歧過大。短期上檔8.4%＝一年後以FY2028共識26.39美元×18倍；中期上檔36.4%＝基準情境五年終端33.2美元×18倍。調整後與GAAP口徑落差大（Q3 GAAP EPS 4.88美元對調整後5.89美元），差額主要是收購無形資產攤銷，本檔與共識、指引皆用調整口徑，不構成爭點。","premortem":"三視角的反證與裁定寫在反證紀錄：AI替代與商譽減損屬論點失敗路徑，目前證據（毛留存90%中段、有機經常性營收8%）反駁但未排除；模型成本與收購倍數屬論點成功但股東經濟變差的路徑，部分採納；股價半年漲24.6%、前瞻本益比19.6倍屬價格已反映太多，採納並據此不追。管理層在Q2法說迴避了AI在2027年的變現金額與指引保守程度，Q3法說也只說2027年規劃下週才開始，AI已進入商業化階段，但訂單、採用、用量都還要證明。Neptune下半年展望由回到成長改為略低於先前展望，是本季唯一的展望改口。"},"plain":{"six":{"how_it_makes_money":"賺的是美國利基產業（律所、保險代理、政府承包商、醫院財務、貨運仲介、藥局、水公用事業）每年續約的軟體訂閱與維護費，錢卡在客戶帳務、計費與合規工作流這一節點；Q3營收21.718億美元、營益率28.7%、調整後EBITDA利潤率39.8%，調整後EPS 5.89美元年增15%。","moat":"護城河方向穩定（→），等級B：機制是工作流嵌入加專有資料造成的轉換成本，可證方向是毛利率69.53%與營益率27.97%對四家同業（毛利率36%–47%、營益率15%–26%）的持續領先，以及企業軟體毛留存連續多季維持90%中段；AI是目前最大的未決威脅。","growth":"五年後成長跑道中等（🟡）：有機成長約6%加收購撐得住8%左右的每股盈餘成長，AI可能是第二條曲線但尚未在營收出現。","capital":"資本配置紀律可信、收購報酬未經外部驗證：今年先大舉回購（前八個月約32億美元、Q2均價約341美元），股價回升後轉向去槓桿與小型收購，淨負債/EBITDA由3.4倍降到2.9倍。","valuation":"現價438.14美元要求未來五年調整後EPS年增約8%，且前瞻本益比守在18倍以上，才有約7%的年化報酬；EPS路徑可信，但倍數已超過前份的重定性目標，再擴張的空間不支撐追價，偏貴。","how_wrong":"最可能看錯在三處：AI在任務層繞過工作流、收購報酬向資金成本收斂、價格已經提前反映重定性；價值陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回落至約380美元（接近52週均線379.55、約17倍FY1共識）且企業軟體毛留存未破90%；或2027年指引不低於共識24.57美元且兩家以上旗艦AI訂單占比≥25%時以較高價分批。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":438.14,"week26_return_pct":24.6,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母為公司調整後EPS，排除收購無形資產攤銷；對連續收購者攤銷是真實成本，GAAP本益比遠高於調整口徑，但本檔的歷史對照、共識與指引全用同一調整口徑，比較一致，不把分母當爭點。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026財報與2027年全年指引","impact":"高","watch":"2027年調整後EPS指引中點對共識24.57美元；是否量化AI訂單或收入"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"Indicor流量控制業務售予Xylem，稅前約6億美元入帳（待監管許可）","impact":"低","watch":"入帳時點與用途（收購或回購）"},{"date":"2027-06","date_precision":"quarter","type":"other","event":"未來12個月逾60億美元可部署資本的收購動向","impact":"高","watch":"單筆金額、成交倍數、目標有機成長"},{"date":"2028-03","date_precision":"quarter","type":"product","event":"Deltek Costpoint地端版停止支援（2028年第一季）","impact":"中","watch":"上雲轉換率與授權收入轉為經常性收入的過渡缺口"}],"_projected_from":"v19"}
```
