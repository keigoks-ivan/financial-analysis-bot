你是 stock-analyst v20 的**散文層（prose）agent**，標的 3037.TW（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：3037.TW　日期：2026-11-02　archetype：None　前份裁決：2026-10-19　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1489B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（392B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1011B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（795B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1318B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（497B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（850B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2344B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3463B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2499B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1489           3858-5511      5 條（2–6 內）  
s3                  8000         392           5326-7608      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3124          8313-11876      5 條（2–6 內）  
s6                 11000         497          7352-10503      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         850           1855-2650      5 條（2–6 內）  
s10                 5000        2344           1859-2656      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2499           2000-2501      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4274B；至少需散文≈40.73KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−164
−111
−80
−80%
−78%
−76%
−73%
−67%
−45%
−45
−22.4%
−19.1
−19.1%
−18.2%
−12.1%
−11.7%
−6.5%
−4.2%
−3.9%
−1.7
−1.7%
−0.4%
0
0.2
0.2%
0.36
0.5%
0.59
0.6
0.62
0.75
0.77%
0.85
1
01
1.4
1.5
1.5%
02
2
2.4
2.6
2.88%
3%
3
3.8
4%
4
04
4.2
4.34
4.43%
5
5%
6%
6
6.1
07
7
7.37%
8%
8
8.45
8.8
9
9%
9.03
9.69
10%
10
10.12%
10.24%
10.3
11
11.6
11.7%
11.75
12
12.23
12.27%
13
13.21%
13.94%
14%
14
14.2
15
15%
15.38
15.47
15.5%
15.52
16
16.04%
16.13%
16.43
18
18%
19
19.85%
20
20%
21%
21.01%
21.78%
22
22%
23%
23
23.26%
23.5
24%
24
24.43
24.8%
25%
26%
26
27
27%
27.17%
28%
29%
30%
31%
31
32.01%
34
35%
35
35.9%
36
38
40
40%
40.48
40.5
42%
42
42.01
45
45%
49
50%
50
50.8
51%
52%
54
61%
63.3
64.6
64.7%
65
66.5
66.7
66.8
69%
69.69
70
70%
72%
72
74.9
85
88
89
90
100%
100
111
131.1
140%
150%
152%
164
232
240
250
262.65
286
300
324
330
379
381.7
428.9
468
489
497.8
526.5
537
550
720
765
800
803.36
972
989.0
989
1120.0
2022
2023
2024
2025
2026
2027
2028
2029
2030
2031
3037
3189
4062
8046
20261102
1,010
1,110
1,120
1,200
1,242
1,329.86
1,500
1,599
1,923
1,936
1,980
2,500
2,794
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
{"meta":{"ticker":"3037.TW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"欣興電子"},"oneliner":"AI 讓 ABF 載板漲價、Q2 毛利率回到 24.8%，但 989 元已在付 2028 年循環高點的獲利，產地標示刑案也未決；等股價 765 元以下、毛利率守 24% 且公司未遭起訴再重啟","thesis":{"H":[{"id":"H1","text":"ABF 載板供不應求延續到 2027 年底，漲價讓季毛利率守在 24% 以上並往 28% 走","2y":"2027 年各季毛利率≥24%，全年≥26%","5y":null,"10y":null,"threshold":"季毛利率≥24%（Q2 2026 為 24.8%）","source":"公司季報與法說會（每季）、月營收（每月）","drift_rule":"以近四季毛利率對 26% 路徑的偏離計：連兩季落後 5% 以上視為削弱，連三季落後 10% 以上視為反轉"},{"id":"H2","text":"AI 需求讓營收維持高成長：2027 年營收達 2,500 億元以上（共識 2,794 億元）","2y":"2027 年營收≥2,500 億元；月營收年增≥25% 到 2027 年中","5y":null,"10y":null,"threshold":"2027 年營收≥2,500 億元","source":"公開資訊觀測站月營收、年報","drift_rule":"近四季營收對 2,500 億元路徑的偏離：連兩季落後 5% 以上視為削弱，連三季落後 10% 以上視為反轉"},{"id":"H3","text":"這一輪循環的谷底比上一輪淺：長約與 AI 占比讓 2026～2030 年平均營益率≥15%，下一個谷底年營益率≥8%（2024 年為 4.43%）","2y":null,"5y":"2026～2030 年平均營益率≥15%；谷底年≥8%","10y":null,"threshold":"五年平均營益率≥15%；谷底年≥8%","source":"年報與季報","drift_rule":"以近四季營益率對 15% 的偏離計：連四季落後 5% 以上視為削弱，連六季落後 10% 以上視為反轉"}],"R":[{"id":"R1","text":"產地標示案擴大：檢方起訴公司本身，或美國海關扣貨、客戶重新稽核後公開轉單","h_ref":"H2","clock":"⚡","threshold":"起訴法人或董事長以上；或任一主要客戶公開轉單","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","sec_investigation_restatement#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R2","text":"擴產軍備競賽讓供給在 2027 下半年到 2029 年湧出，報價轉跌、毛利率回落，重演 2023～2024 年","h_ref":"H1","clock":"🔥","threshold":"毛利率連兩季年減，或 ABF 報價首度季減","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R3","text":"執行與工安：HDI 與 AI PCB 良率偏低、楊梅一廠部分停工、537 億元擴產帶來折舊壓力","h_ref":"H1","clock":"⚡","threshold":"營益率季減≥3 個百分點，或停工擴大到影響月營收","evidence_refs":["capital_markets_pricing#2","major_events#1","product_recall_warning#0"]},{"id":"R4","text":"客戶因治理疑慮分散供應商，美系 ASIC 約七成的份額被南電、景碩、日系分走","h_ref":"H3","clock":"🐢","threshold":"法說或客戶揭露份額跌破 50%","evidence_refs":["competitive_share_entrants#1"]}],"single_thing":{"description":"2027 年底前 ABF 載板報價首次出現季減（漲價循環結束）","why_fatal":"情境樹最敏感的是 2028 年後的獲利水準：共識 2027、2028 年 EPS 42.01、69.69 元，隱含利潤率回到 2022 年高點以上；報價一轉跌，2023 年前例是單季毛利率年減 11.75 個百分點，終端 EPS 會從 Base 的 40 元往 Bear 的 18 元移動，下檔約三分之二","if_happens":"未持有：取消重啟，改等循環谷底訊號；已持有：減碼一半，毛利率再連兩季年減則清倉","how_monitor":"每季法說的報價說法（目前稱滾動式調整）、季毛利率年增減、景碩與南電法說的報價口徑、月營收年增率","probability":"約 20%（12～24 個月）：多家預估 2027、2028 年缺口擴大所以不高，但 2027 下半年 Ibiden 與景碩新產能開出是主要風險窗"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.5,"peg_fy2":0.36,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":4.34,"FY2026E":24.43,"FY2027E":42.01,"FY2028E":69.69},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（新台幣）；FY2025A 取年度財報，共識取 Koyfin 2026-10-31 快照，美元值依當日匯率換算；營收共識 FY2026 有 11 位、FY2027 有 20 位分析師"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261102/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"2022→2025 年毛利率 35.9%→13.94%，擺動約 22 個百分點；2026 年資本支出 537 億元約占共識營收 28%；營益率在 4.43%～27.17% 之間擺動"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：ABF 缺口預估 2026 下半年約 10%、2027 年 20～25%、2028 年 36～42%（Counterpoint 二手轉述、高盛、本土法人），2027 年續為賣方市場；但欣興 2026 年資本支出三度上修到 537 億元，景碩、Ibiden 2027 下半年、南電 2029 上半年新產能開出，供給可逆性高","bargaining":{"up":"上游 T-glass、銅箔、鑽針短缺，材料商議價力強；公司已為部分關鍵材料建立替代方案並以漲價轉嫁","down":"下游 AI 晶片客戶為保供應簽 3～7 年長約並預付款，短缺期公司議價力強；但客戶可在新專案加認證第二家，治理疑慮給了理由","geo":"ABF 產能全在台灣；中國有深圳、蘇州、昆山、黃石廠，產地標示案涉中國製 PCB；泰國廠第四季小量出貨；2025 年直接出口美國約 2～3%"},"profit_pool_dir":"利潤池往 AI 用高層數、大尺寸 ABF 集中，BT 與一般 PCB 相對弱；長期分配隨供需擺動","tam_table":{"expanded":false,"reason":"事實表未涵蓋 ABF 市場規模、滲透率與利潤池占比，只有供需缺口預估；不以缺口數字代替市場規模"}},"moat":{"mechanism":"AI 高階 ABF 製程良率與客戶認證，加上 3～7 年長約與預付款形成的轉換成本","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力穩定：美系 ASIC 載板份額約七成、Blackwell 三成以上，客戶簽長約；定價權短期擴大（2026 年多次漲價）但屬循環，上一輪毛利率由 35.9% 跌到 13.94%；負面是治理疑慮可能讓客戶分散，尚未見實際轉單。兩者合計持平","peer_na_reason":"事實表未涵蓋同業投入資本，ROIC 差距以毛利率、營益率、FCF 利潤率代替","threats":[{"level":"🟡","text":"客戶因產地標示案的治理疑慮加認證景碩、南電、Ibiden、SEMCO 等供應商，美系 ASIC 載板約七成份額易降難升","p":"30%","evidence_refs":["competitive_share_entrants#1","geo_supply_chain#1","reg_tariff_export#1"]},{"level":"🟡","text":"同業同步擴產：景碩 2027 年 ABF 產能增 25%、Ibiden 2027 下半年、南電 2029 上半年開出，短缺期定價權在 2028 年後退潮","p":"40%","evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"新世代封裝基板 EMIB-T 2027 年量產、首階良率目標僅 50%，世代轉換中良率落後會讓出份額","p":"20%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"TTM 屬低利益率×低周轉（營益率 10.24%，資產重），2026 下半年往高利益率×低周轉移動；投入資本周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端業者、決策者是 GPU 與 ASIC 設計商、付款者是晶片商或封測廠，三角色都成立；AI 加速器沒有 ABF 以外的量產方案，屬需要而非想要。但急迫性來自 AI 資本支出週期，不等於持久，高盛也點名 PC 需求復甦慢"},{"item":"決策層級","level":"🟡","text":"替代性要看單一晶片專案：新專案要重新認證，合約 3～7 年並有預付款，轉換成本高；但客戶可在下一代專案加認證第二家，治理疑慮正給客戶理由這樣做"},{"item":"價值鏈分配","level":"🟡","text":"AI 晶片價值鏈中載板採購金額占比小，晶片設計與晶圓代工拿走多數；短缺期欣興能漲價 10～15%，但上游 T-glass、銅箔短缺也讓材料商分走一塊；2023～2025 年毛利率跌到 14%，說明分配隨供需擺動"},{"item":"社會容忍度","level":"🟢","text":"工業零組件的企業間交易，沒有社會對漲價的容忍上限；監管風險是產地標示的刑事合規，不是定價授權"}],"roiic":"無法計算：事實表未涵蓋投入資本與折舊。旁證：2022→2025 年營業利益由約 381.7 億元降到約 66.8 億元（營收×營益率），同期自由現金流由正 286 億元轉為負 111 億元，上一輪增量投資在谷底期報酬為負；2026 年回升主要來自報價","reinvest_rate":"扣折舊前約 140%：2026 年資本支出 537 億元÷FY2026 共識淨利約 379 億元（24.43 元×約 15.52 億股）；折舊與營運資金變動事實表未涵蓋，淨再投資率無法精算","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；增量 ROIC 缺投入資本無法計算，天花板留空。共識 FY2026→2028 年 EPS 年複合 69% 幾乎全靠利潤率回升，不是再投資複利，視同超出天花板"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","3037.TW":19.85,"3189.TW":23.26,"8046.TW":16.04,"4062.T":32.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","3037.TW":10.24,"3189.TW":10.12,"8046.TW":12.27,"4062.T":16.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","3037.TW":-0.4,"3189.TW":7.37,"8046.TW":7.71,"4062.T":21.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","3037.TW":3.92,"3189.TW":5.59,"8046.TW":null,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3189.TW","gm":23.26,"om":10.12,"fcf_margin":7.37,"rd_intensity":5.59,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"8046.TW","gm":16.04,"om":12.27,"fcf_margin":7.71,"rd_intensity":null,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"4062.T","gm":32.01,"om":16.13,"fcf_margin":21.01,"rd_intensity":null,"period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"價＋量＋利潤率回升：ABF 漲價、光復廠擴產、AI 占比提高；無併購、無回購","runway_years":3,"runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 缺投入資本與折舊資料無法計算，天花板留空；再投資率扣折舊前約 140%，代表成長靠大量資本投入。共識年複合 69% 的缺口歸因為利潤率回升（毛利率 13.94%→24.8% 並預期續升），屬循環","segments":[{"item":"ABF 載板","value":"Q2 營收占 52%，年增 51%、季增 22%；2026 年資本支出八成以上投入"},{"item":"HDI","value":"占 22%，年增 29%；外資指 AI HDI 初期良率偏低"},{"item":"BT 載板","value":"占 9%；上一輪 2023 年曾因稼動率低而虧損"},{"item":"PCB","value":"占 9%；產地標示調查集中在此"},{"item":"其他","value":"約 8%，事實表未拆分"}],"decay_signals":["亮：EPS 成長遠高於營收成長——FY2027 共識 EPS 年增約 72%，共識營收年增約 45%","亮：自由現金流÷淨利連兩年低於 0.75——2024、2025 年自由現金流為負 164 億、負 111 億元","未亮：毛利率連兩季年減（Q2 2026 毛利率 24.8%，遠高於 2025 年全年 13.94%）","未亮：核心市占縮減（只有市場疑慮，未見實際轉單）","未亮：SBC 占比偏高（SBC 只占營業利益 0.5%）","資料缺口：維護性資本支出占比事實表未涵蓋"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能而非併購，股息殖利率 0.2%、無回購紀錄，資本回饋不承重"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近期無收購，只有處分深圳聯能（人民幣 8.8 億元）與日本子公司意向書，沒有併購報酬可算","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購紀錄；股息殖利率 0.2%","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營業利益 0.5%；淨利÷EPS 推得的加權股數 2022 年約 15.47 億、2025 年約 15.38 億、Q2 2026 約 15.52 億股，年稀釋遠低於 1.5%；市值口徑流通股數 16.43 億股的差距來源未明","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2026～FY2028 共識）為主；循環股優先的股價淨值比事實表未涵蓋","tier":"台系 ABF 三雄（欣興、南電、景碩）與日系 Ibiden 同層","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業本益比與股價淨值比，無法做倍數對照"},"fwd_pe":40.48,"peg":0.59,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價 989 元＝FY2026 共識 40.5 倍、FY2027 共識 23.5 倍、FY2028 共識 14.2 倍；現值本益比 64.6 倍、股價營收比 9.69 倍、EV／營收 9.03 倍都在四個年度端點最高（連續五年分位事實表未涵蓋，五年分位留空）。2027～2028 年共識獲利隱含利潤率高於 2022 年循環高點，高點年份應給低倍數。一年後：FY2028 Base EPS 54 元×18 倍＝972 元（−1.7%）；五年 Base：40 元×20 倍＝800 元（−19.1%）。PEG 0.59＝40.48 倍÷FY2026→2028 共識 EPS 年複合 69%，偏低只因分母從循環低點起算，不代表便宜。判為偏貴","upside_short_pct":-1.7,"upside_mid_pct":-19.1},"trap_analysis":{"verdict":"🟡","label":"循環高檔＋自由現金流為負"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"上一輪高點後，2023 年 Q1 毛利率年減 11.75 個百分點、Q3 BT 載板因稼動率低而虧損，2024 年 Q2 毛利率 13.21%；本輪欣興資本支出三度上修到 537 億元，八成以上投 ABF","assumption":"AI 需求能吸收 2027 下半年到 2029 年全產業的新產能","consequence":"報價 2028 年轉跌、2030 年毛利率回到 15～18%，EPS 約 16～18 元，乘 18 倍約 300 元，五年虧損約三分之二","ruling":"採納，Bear 機率 35%；與唯一致命點（報價首度季減）是同一件事的前後階段，兩者一致","watch":"季毛利率年增減、ABF 報價口徑、同業新廠進度","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_supply_discipline_capacity#3"],"fact_refs":["f_kpi1_gaap","f_kpi6_q3_2026"]},{"view":"論點失敗","evidence":"檢方兩波搜索、14 名主管員工被詢問、PCB 事業部總經理 1,500 萬元交保；法人提醒美國海關扣貨、補稅與客戶重新稽核","assumption":"案件限於 PCB 特定廠房，ABF 產能全在台灣不受影響","consequence":"若起訴公司或客戶啟動合規條款，PCB 與 HDI（合計約 31% 營收）訂單轉出，ABF 新專案也被分散認證","ruling":"部分採納：決勝資料尚不存在，列入重啟條件與風險 R1；營收曝險小於報價轉折，不當唯一致命點","watch":"起訴範圍、美國海關動作、客戶揭露的供應商名單","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","sec_investigation_restatement#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","competitive_share_entrants#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"TTM 自由現金流利潤率 −0.4%，2024、2025 年自由現金流 −164 億、−111 億元；2026 年資本支出 537 億元約為 FY2026 共識淨利的 1.4 倍；Ibiden FCF 利潤率 21.01%","assumption":"這一輪高額擴產的增量報酬高於資金成本","consequence":"AI 需求論點成立，但獲利被折舊與下一輪擴產吃掉，股東拿到的現金有限，股息殖利率只有 0.2%","ruling":"採納：資本配置偏弱，長期信心上限中","watch":"自由現金流÷淨利、2027 年資本支出指引","evidence_refs":["cyclical_supply_discipline_capacity#3"],"fact_refs":["f_peer_3037_tw_fcf_margin_pct","f_peer_4062_t_fcf_margin_pct","f_kpi4","f_dividend_yield_ttm"]},{"view":"論點成功但股東經濟變差","evidence":"楊梅一廠工安死亡、勞檢部分停工、罰鍰未定；美系外資指 AI HDI 與 PCB 初期良率偏低","assumption":"停工不影響營運，良率能在 2027 年拉上來","consequence":"營收成長但營益率落後共識，2027 年 EPS 低於 42.01 元","ruling":"部分採納：Base 2027 年 EPS 取 40 元，略低於共識","watch":"月營收月增率、季營益率","evidence_refs":["major_events#1","product_recall_warning#0","capital_markets_pricing#2"],"fact_refs":["f_kpi2_gaap"]},{"view":"價格已反映太多","evidence":"現價為 FY2027 共識 23.5 倍、FY2028 共識 14.2 倍；現值本益比 64.6 倍、股價營收比 9.69 倍都在四個年度端點最高；股價是 250 週均線 262.65 元的 3.8 倍","assumption":"2028 年共識獲利是常態而非高點","consequence":"即使 2028 年兌現，市場在高點利潤率年份給低倍數，Base 五年終值 800 元低於現價","ruling":"採納：維持觀望、不追價；反方是賣方目標價與共識續上修，已在矛盾裁定處理","watch":"FY2028 共識修正方向、股價對 FY2027 共識倍數","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#4"],"fact_refs":["f_price_at_dd","f_pe_current","f_ps_current","f_ma_w250","f_consensus_eps_fy2","f_consensus_eps_fy3"]}],"max_dd":{"lo":-80,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1120.0 → 本次 989.0（-11.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1120.0","side_b":"本次 price_at_dd=989.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,120 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,120 元：Bull 價 1,936、Bear 價 330，五年期望值 −18.2%，基準年化 −3.9%，不對稱比 0.6","side_b":"本次情境、股價仍用 1,120 元：Bull 價 1,980、Bear 價 324，五年期望值 −22.4%，基準年化 −6.5%，不對稱比 0.62","ruling":"先換情境、股價不動：五年期望值少 4.2 個百分點，基準年化少 2.6 個百分點。不對稱比由 0.6 變為 0.62。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,120 元：五年期望值 −22.4%，基準年化 −6.5%，不對稱比 0.62","side_b":"本次情境、股價 989 元：五年期望值 −12.1%，基準年化 −4.2%，不對稱比 0.85","ruling":"再換股價、情境不動：起點價下跌 11.7%，五年期望值多 10.3 個百分點，基準年化多 2.4 個百分點，不對稱比由 0.62 升到 0.85。合計五年期望值比前份多 6.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：股價下跌後結論未變","cause":"價格變動","prior_field":["signal","val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份（10-19）股價 1,120 元：觀望、整體評級 C、估值偏貴、多空機率 20%／35%、最大回撤 −78%","side_b":"本次股價 989 元（−11.7%）：FY2027 共識 23.5 倍、FY2028 共識 14.2 倍；多空機率維持 20%／35%，最大回撤區間 −80%～−45%","ruling":"跌幅來自價格而非基本面轉弱，Q2 毛利率 24.8% 與 9 月營收年增 64.7% 仍在上行；Base 五年終值 800 元仍低於現價，評級、估值結論、觀望與多空機率都不變，回撤區間改用範圍表達","evidence_level":"高（價格與共識皆為事實表數字）","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若股價跌到 765 元以下且季毛利率≥24%、產地案未起訴公司，重啟研究評估首筆","若股價反彈到 1,200 元以上而 FY2028 共識未上修，維持不追"],"evidence_refs":[]},{"axis":"前份漂移：10-19 之後的新事件","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：陷阱風險中等、護城河持平、五年後成長空間中等、循環股、中循環","side_b":"新事件：楊梅一廠工安死亡、勞檢部分停工（10-13）；處分日本子公司意向書（10-27）；FY2028 共識 EPS 上修 2.88%；10-27 已公布 Q3 財報但事實表未收","ruling":"工安停工公司稱不影響營運、日本子公司處分屬組合瘦身，都不改護城河與循環位置；Q3 財報缺漏是本次最大資料缺口，五欄維持前份結論","evidence_level":"中（Q3 財報缺漏）","settle_metric":"Q3 2026 毛利率與 Q4 展望","if_then":["若 Q3 毛利率低於 24%，循環位置改判晚循環並取消重啟","若 Q3 毛利率≥28% 且 Q4 展望續增，維持中循環判斷"],"evidence_refs":["major_events#1","product_recall_warning#0"]},{"axis":"重啟條件改寫","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價≤765元（約 FY2027 共識 EPS 20倍），且最近一季毛利率仍≥24%","side_b":"股價≤765元（約FY2027共識EPS 18倍）且最近一季毛利率≥24%，且產地標示案未起訴公司本身","ruling":"價格門檻 765 元不變，FY2027 共識已到 42.01 元，765 元改寫為約 18 倍；另加事件條件：刑事程序已開始、客戶可能重新稽核，價格到了但公司被起訴就不重啟研究、不建倉","evidence_level":"中","settle_metric":"股價、季毛利率、起訴範圍","if_then":["三條件全成立：重跑判斷，通過後首筆建倉 1.5%","價格到了但公司被起訴：不建倉，等客戶稽核結果"],"evidence_refs":[]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標（null）","side_b":"本次設四項：季毛利率連兩季低於 20%、月營收年增連三月低於 10%、產地標示案起訴公司、ABF 報價首度季減；觸發即減碼或清倉","ruling":"前份只有重啟條件、沒有持有中的出場規則；本次補上，未持有時作為取消重啟的條件","evidence_level":"中","settle_metric":"四項停損指標","if_then":["任一項觸發且已持有：減碼一半","起訴公司或報價季減後毛利率再連兩季年減：清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未記錄唯一致命點（null）","side_b":"2027 年底前 ABF 載板報價首次出現季減（漲價循環結束）","ruling":"Single Thing 改設為報價轉折：情境樹最敏感的是 2028 年後獲利，報價是它的單一開關；產地標示案影響 PCB 與 HDI（合計約 31% 營收），敏感度較小，列風險 R1","evidence_level":"中","settle_metric":"ABF 報價季變動","if_then":["報價首度季減：取消重啟；若持有減碼一半","2027 年各季報價持續調漲：Bull 機率上調重跑判斷"],"evidence_refs":[]},{"axis":"供需：短缺延續 vs 擴產軍備競賽","cause":null,"side_a":"ABF 缺口 2027 年約 20～25%、2028 年 36～42%（Counterpoint、高盛、本土法人），2027 年續為賣方市場","side_b":"欣興 2026 年資本支出三度上修到 537 億元，景碩 2027 年擴 25%，Ibiden 2027 下半年、南電 2029 上半年新產能開出；上一輪 2023 年 Q1 毛利率年減 11.75 個百分點","ruling":"可調和（時點差異）：2027 年前短缺成立，2028～2029 年供給湧出的風險同樣成立；Base 路徑採 2028 年獲利高點、2029～2030 年回落","evidence_level":"中（缺口預估多為二手轉述，資本支出為公司公告）","settle_metric":"ABF 報價季變動與季毛利率年增減","if_then":["若 2027 年各季毛利率仍季增且景碩、南電擴產延後，Bull 機率由 20% 上調到 30%","若 2027 年任一季報價季減，Bear 機率上調到 45%"],"evidence_refs":["supply_demand_durability#0","end_markets#5","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#1","cyclical_prior_downcycle_behavior#0"]},{"axis":"產地標示案：短期事件 vs 客戶分散供應商","cause":null,"side_a":"花旗：ABF 產能全在台灣，調查若限特定廠房屬短期影響，維持買進、目標價 1,500 元","side_b":"刑事搜索兩波、PCB 事業部總經理交保；市場擔心觸發美系客戶合規條款，客戶可能加認證景碩、南電與日系","ruling":"不可裁決至檢方起訴決定：決勝資料（起訴書、客戶稽核結果）今天不存在，證據時間窗沒有蓋住風險窗；在此之前不稱風險已解，列為重啟條件與風險 R1","evidence_level":"中","settle_metric":"起訴範圍（個人或法人）、美國海關動作、主要客戶揭露的供應商變動","if_then":["若只起訴個人且無海關動作，事件條件解除","若起訴公司或主要客戶公開轉單，持有則清倉，未持有則取消重啟"],"evidence_refs":["geo_supply_chain#0","regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","sec_investigation_restatement#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","competitive_share_entrants#1"]},{"axis":"市場定價 vs 循環歷史","cause":null,"side_a":"法說後賣方目標價 1,010～1,500 元、多家買進；FY1 共識三個月上修 21.78%；現價只要 FY2028 共識的 14.2 倍","side_b":"FY2027 共識隱含淨利率約 23%，已高於 2022 年高點約 21%，FY2028 共識要求更高；過去四年毛利率在 13.94%～35.9% 擺動","ruling":"不可調和（方向相反）。選循環歷史：2022 年營益率 27.17% 之後兩年跌到 4.43%，而本輪全產業同步擴產；硬數據點是季毛利率與 ABF 報價。執行：維持觀望不追價。現在就買的最強論證：股價已從 1,120 元回落 11.7%、RSI 38、FY2028 共識只有 14.2 倍、缺口預估到 2028 年擴大、長約預付款降低下行；它不成立的理由是 14.2 倍的分母是高點獲利。反向條件：2027 下半年毛利率仍季增且 FY2028 共識續上修，承認拉長型循環並重跑判斷","evidence_level":"中","settle_metric":"2027 年各季毛利率與 FY2028 共識 EPS 修正方向","if_then":["若 2027 上半年毛利率≥28% 且 FY2028 共識續上修，重跑判斷、Bull 機率上調到 30%","若股價先漲到 1,200 元以上但毛利率未過 26%，不追","若股價跌到 765 元以下而毛利率仍≥24%、產地案未起訴公司，分批反買首筆 1.5%"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#4","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"axis":"獲利品質：淨利 vs 營業利益","cause":null,"side_a":"Q2 EPS 8.45 元、淨利 131.1 億元","side_b":"Q2 營業利益只有 66.5 億元，業外約 89 億元（利息、評價轉盈、深圳聯能處分利益）；FY2026 共識 EPS 24.43 元含一次性收益","ruling":"可調和（程度差異）：本業仍在改善（營益率 15.5%），但 FY2026 本益比 40.5 倍的分母高估本業，估值改以 FY2027 錨定","evidence_level":"高","settle_metric":"Q3、Q4 業外收益占稅前淨利比","if_then":["若 Q3 業外占稅前淨利仍超過三成，Base 2027 年 EPS 再下修","若業外回到一成以下且營益率≥18%，維持 Base"],"evidence_refs":[]},{"axis":"管理層展望 vs 外資對 HDI 良率疑慮","cause":null,"side_a":"公司稱 Q3 營收與毛利率續季增，AI 占比下半年升到 65～70%","side_b":"一家美系外資指 AI HDI 與 PCB 初期良率偏低，毛利率展望偏弱","ruling":"可調和（分部差異）：載板占 61%（ABF 52%＋BT 9%）主導毛利率，HDI 良率拖累有限；Q3 財報可驗證，但事實表未收","evidence_level":"中","settle_metric":"Q3 毛利率與 HDI 營收季變動","if_then":["若 Q3 毛利率低於 Q2，採信外資疑慮、Base 2027 年 EPS 下修到 36 元","若 Q3 毛利率≥26%，管理層展望成立"],"evidence_refs":["capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"股價跌到 765 元以下、最近一季毛利率仍≥24%，且產地標示案未起訴公司：重啟研究，通過後分批建立首筆","type":"估值rearm","maps_to":"H1","metric":"股價、季毛利率、起訴範圍","threshold":"≤765 元且毛利率≥24% 且未起訴公司","action":"重跑判斷後首筆 1.5%","source_freq":"每日股價；每季財報；重大訊息即時","date":null},{"n":2,"text":"補讀 10-27 已公布的 Q3 2026 財報：毛利率低於 24% 則取消重啟、循環位置改判晚循環","type":"假設驗證","maps_to":"H1","metric":"Q3 2026 毛利率","threshold":"<24%","action":"取消重啟、重跑判斷","source_freq":"一次性（Q3 財報已公布）","date":"2026-11"},{"n":3,"text":"ABF 載板報價首次季減","type":"Single Thing","maps_to":"H1","metric":"ABF 報價季變動","threshold":"首次季減","action":"取消重啟；若持有減碼一半","source_freq":"每季法說、同業法說","date":"2027-12-31 前"},{"n":4,"text":"檢方起訴公司本身，或美國海關扣貨、主要客戶公開轉單","type":"清倉","maps_to":"R1","metric":"起訴範圍與客戶動作","threshold":"起訴法人或董事長以上；或任一主要客戶轉單","action":"持有則清倉，未持有則取消重啟","source_freq":"重大訊息即時","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","sec_investigation_restatement#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]},{"n":5,"text":"季毛利率連兩季年減","type":"減碼","maps_to":"R2","metric":"季毛利率年增減","threshold":"連兩季年減","action":"減碼一半，再一季年減則清倉","source_freq":"每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"n":6,"text":"楊梅一廠停工擴大或 HDI 良率拖累營益率","type":"風險","maps_to":"R3","metric":"季營益率季變動、月營收月增率","threshold":"營益率季減≥3 個百分點，或月營收連兩月月減","action":"凍結重啟一季","source_freq":"每月營收、每季財報","date":null,"evidence_refs":["major_events#1","product_recall_warning#0","capital_markets_pricing#2"]},{"n":7,"text":"月營收年增率維持 25% 以上到 2027 年中","type":"假設驗證","maps_to":"H2","metric":"月營收年增率","threshold":"≥25%","action":"未達則 H2 削弱、Bull 機率下修","source_freq":"每月 10 日前","date":"2027-07"},{"n":8,"text":"美系 ASIC 載板份額跌破五成","type":"風險","maps_to":"R4","metric":"ASIC 載板份額","threshold":"<50%（2025 年底約 70%）","action":"護城河改判下滑，重跑判斷","source_freq":"法說與產業報導，不定期","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":9,"text":"Q4 2026 法說：2027 年資本支出與報價口徑","type":"複審日期","maps_to":"H1","metric":"2027 年資本支出、毛利率展望","threshold":"資本支出再上修且同業同步擴產","action":"重跑判斷","source_freq":"每季","date":"2027-02"}],"kill_metrics":[{"metric":"季毛利率","bear_threshold":"連兩季低於 20%（Q2 2026 為 24.8%）","window":"至 2027 年底","source":"公司季報與法說","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連三個月低於 10%（2026 年 9 月為 +64.7%）","window":"逐月，至 2027 年底","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"產地標示案進展","bear_threshold":"起訴公司或董事長以上，或美國海關扣貨、主要客戶公開轉單","window":"至 2027 年 6 月","source":"公開資訊觀測站重大訊息、地檢署公告","last_status":"warning"},{"metric":"ABF 載板報價","bear_threshold":"公司或同業首次宣布季減","window":"至 2027 年底","source":"法說會與產業報導","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2028 年共識 EPS 69.69 元（利潤率高於 2022 年高點）當常態獲利，給 FY2027 共識 23.5 倍；但欣興、景碩、南電、Ibiden 的新產能正好在 2027 下半年到 2029 年開出，上一輪高點後兩年營益率由 27% 跌到 4%"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=12.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"3%","requires_critic":["QC-50"],"rearm_trigger":"股價≤765元（約FY2027共識EPS 18倍）且最近一季毛利率≥24%，且產地標示案未起訴公司本身","exec_line":"未觸發前不建倉、不追價；觸發後先重跑判斷，通過才分批建立，首筆 1.5%、總上限 3%；持有中依停損指標減碼或清倉"},"reasoning":{"industry":"營收分部（Q2 2026 法說）：ABF 載板 52%（年增 51%）、HDI 22%（年增 29%）、BT 載板 9%、PCB 9%；載板與 PCB 的 AI 相關營收上半年都超過六成，下半年目標分別 70% 與 65～70%。Q2 營收 428.9 億元、毛利率 24.8%、營益率 15.5%，淨利 131.1 億元含約 89 億元業外，本業品質低於帳面。7～9 月營收合計約 526.5 億元（前九月 1,329.86 億元減上半年 803.36 億元），季增約 23%，高於券商估的 497.8 億元；但 10-27 已公布的 Q3 財報不在事實表內，Q3 毛利率是本次最大資料缺口。產業時鐘在擴張期：需求大於供給、報價逐季調漲，同業新產能要到 2027 下半年以後才開出。供需持久性判為週期性將反轉，依據見供需判讀欄。產業態勢三軸是雙向拉鋸：競爭端惡化（景碩 2027 年 ABF 產能增 25%、南電 468 億元新廠、Ibiden 擴產），結構端轉好（客戶簽 3～7 年長約並預付款），其他端變動中（產地標示刑案、美國 232 關稅是否涵蓋載板未確認）。單點依賴：單一客戶占比事實表未涵蓋；美系 ASIC 載板份額約七成既是護城河證據，也是客戶集中風險。","moat":"機制：AI 高層數、大尺寸 ABF 的製程良率與客戶認證，加上 3～7 年長約與預付款。方向證據：對獲利標竿 Ibiden 差距為負——TTM 營益率 10.24% 對 16.13%、毛利率 19.85% 對 32.01%、FCF 利潤率 −0.4% 對 21.01%；對景碩營益率持平（10.12%），對南電落後（12.27%）。份額端：美系 ASIC 載板約七成、Blackwell 三成以上（2025 年底法人看法），但治理疑慮讓客戶有理由分散。執行力 7 分（擴產與 AI 份額到位，扣分在 HDI 良率、工安、合規），定價權 5 分（短缺期漲價 10～15%，但上一輪毛利率由 35.9% 跌到 13.94%，定價權隨循環來去），綜合 C。同業投入資本不在事實表，ROIC 差距以利潤率代替。","growth":"成長來源：價（ABF 2026 年多次漲價，法人估漲幅 10～15%）＋量（光復一廠三期 Q3 量產、光復二廠 2027 年擴 30% 以上 ABF 產能、楊梅二廠約 2028 年量產）＋利潤率回升；無併購、無回購。共識 EPS：FY2025A 4.34 元→FY2028E 69.69 元，三年年複合約 152%，分母是谷底，沒有參考意義；FY2026E→FY2028E 年複合約 69%。共識營收 FY2026 1,923 億元（11 位分析師）、FY2027 2,794 億元（20 位），FY2028 營收共識事實表未涵蓋。缺口歸因：幾乎全來自利潤率回升（毛利率由 13.94% 回到 24.8% 並預期續升），屬循環，不是再投資複利。Runway：缺口預估到 2028 年，高確信約 2～3 年；第二條曲線 EPS 只有 EMIB-T 2027 年量產，屬世代轉換而非新市場，判中等。衰退訊號亮兩項，價值陷阱風險與長期成長性都判中等。","governance":"現金轉換：2024、2025 年自由現金流 −164 億、−111 億元，對淨利 50.8 億、66.7 億元皆為負；Q2 2026 營業現金流 74.9 億元減資本支出 63.3 億元，自由現金流 11.6 億元，只有淨利的 9%。SBC 只占營業利益 0.5%，不是稀釋來源。現金去向：資本支出為主（2026 年預算 537 億元，八成以上投 ABF）；股息殖利率 0.2%；事實表未涵蓋回購；處分深圳聯能（人民幣 8.8 億元）與日本子公司（意向書階段）屬組合瘦身；無收購。資產負債：總債務約 489 億元、現金約 1,599 億元，淨現金約 1,110 億元，足以支應一年資本支出。股數：以淨利÷EPS 推得的加權股數 2022 年約 15.47 億、2025 年約 15.38 億、Q2 2026 約 15.52 億股，但市值口徑的流通股數 16.43 億股，差距約 6% 原因事實表未涵蓋，終端 EPS 以約 16 億股估算。","valuation":"股價隱含的預期：989 元＝FY2027 共識 23.5 倍、FY2028 共識 14.2 倍。若 2028 年是循環高點，市場屆時通常只給低倍數；要讓現價合理，需要 2029 年後獲利不回落。FY2027 共識隱含淨利率約 23%（42.01 元×約 15.52 億股÷營收 2,794 億元），已高於 2022 年高點約 21%。共識仍在上修：FY1 三個月上修 21.78%，最近一次 FY2 上修 0.77%、FY3 上修 2.88%。法說後賣方目標價 1,010～1,500 元，全距約 1.5 倍，年初大摩 550 元已過時；現價低於所有法說後目標價，賣方共識反對本次偏貴判斷，分歧在框架：賣方用 2027～2028 年獲利給成長倍數，我用循環高點利潤率打折。週線均線仍是多頭排列，RSI 38 屬回檔，不過熱。循環股優先看股價淨值比，但事實表未涵蓋淨值；同業本益比也未涵蓋，終端倍數只能以自身 FY2027 共識倍數作參照。","premortem":"壓力測試五項過兩項：毛利率回到 2025 年 13.94% 仍有獲利（2025 年淨利 66.7 億元）、淨現金約 1,110 億元足以支應一年 537 億元資本支出；未過：自由現金流為負、Bear 下檔約三分之二、產地標示案未決。回撤區間與推導寫在情境假設，反證三視角寫在反證紀錄，這裡不重寫。衰退訊號亮兩項（EPS 成長遠高於營收、自由現金流連兩年為負），價值陷阱判中等。"},"plain":{"six":{"how_it_makes_money":"賺 AI 晶片商（GPU、ASIC）的載板錢：ABF 載板占 Q2 營收 52%，錢卡在高階 ABF 產能與 T-glass 等關鍵材料這一節點；2026 年是缺貨漲價年，毛利率由 2025 年 13.94% 回到 Q2 24.8%","moat":"護城河持平：靠 AI 高階 ABF 的良率、客戶認證與長約撐住份額，但獲利率落後 Ibiden，短缺期的定價權來自循環而非結構，等級 C","growth":"五年後成長空間中等：2028 年前靠漲價加擴產，AI 占比已超過六成，之後要看新世代封裝基板能否接棒，而且成長幾乎全靠利潤率回升","capital":"資本配置偏弱：賺的錢全投回擴產、自由現金流轉負，靠約 1,110 億元淨現金與客戶預付款撐住，股東回饋極低","valuation":"現價 989 元要求 2028 年共識 EPS 69.69 元兌現，而且被當成常態獲利；那是高於 2022 年循環高點的利潤率，我不信能延續，估值偏貴","how_wrong":"最可能看錯在循環長度：若 AI 需求讓短缺延續到 2029 年後、長約讓谷底變淺，偏貴的判斷就錯；往下則是 2027 下半年就見頂，再疊上合規事件"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2028 年共識 EPS 69.69 元（利潤率高於 2022 年高點）當常態獲利，給 FY2027 共識 23.5 倍；但欣興、景碩、南電、Ibiden 的新產能正好在 2027 下半年到 2029 年開出，上一輪高點後兩年營益率由 27% 跌到 4%","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"追蹤","wait_for_price":true,"wait_for_price_condition":"股價≤765 元（約 FY2027 共識 18 倍）且最近一季毛利率≥24%，且產地標示案未起訴公司本身","trap":"🟡","val":"🟠","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":989.0,"week26_return_pct":12.23,"consensus_rev_3m_pct":21.78,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026 共識 EPS 24.43 元含 Q2 約 89 億元業外收益（其中有深圳聯能處分利益），FY2028 共識 69.69 元是循環高點獲利；用哪一年當分母決定便宜或貴，以本益比論便宜不成立"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"10 月營收公布，並補讀 10-27 已公布的 Q3 財報","impact":"中","watch":"月營收年增率是否維持 50% 以上；Q3 毛利率是否≥24%"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年資本支出","impact":"高","watch":"毛利率是否≥26%、資本支出是否再上修"},{"date":"2027-04","date_precision":"quarter","type":"capacity","event":"光復二廠新產能量產","impact":"中","watch":"折舊上升速度與良率"},{"date":null,"type":"regulatory","event":"產地標示案起訴與否","impact":"高","watch":"起訴範圍是個人還是公司，有無美國海關動作"},{"date":"2027-01","date_precision":"quarter","type":"other","event":"日本子公司出售給 Meiko 的正式合約","impact":"低","watch":"處分價格與損益"}],"_projected_from":"v19"}
```
