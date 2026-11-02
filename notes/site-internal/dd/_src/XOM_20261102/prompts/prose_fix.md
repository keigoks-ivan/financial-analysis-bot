你是 stock-analyst v20 的**散文層（prose）agent**，標的 XOM（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：XOM　日期：2026-11-02　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1740B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（462B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1020B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1390B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1185B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（504B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1003B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2275B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3638B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2176B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1740           3682-5260      5 條（2–6 內）  
s3                  8000         462           5277-7538      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3595          7983-11405      5 條（2–6 內）  
s6                 11000         504          7347-10496      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1003           1748-2497      5 條（2–6 內）  
s10                 5000        2275           1907-2725      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2176           2000-2824      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4822B；至少需散文≈40.18KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−49%
−43%
−35
−35%
−33%
−17.5
−16.1%
−8.7
−4.5%
−1
0.3
0.75
0.82
0.91
0.93
01
1
1.05
1.07
1.4%
1.5%
1.6
1.97
2
2%
02
2.02
2.2
2.6
2.6%
3%
3
3.72
4
4.23
5
5%
05
5.2%
6
06
6.4%
6.6
6.70
6.7
7
7.25
7.4
7.81
8%
8
8.5%
9
9%
09
9.5
9.6
10
10%
10.3
10.5
10.7
10.7%
11
11.1
11.4
12
12.01
12.4%
12.4
12.9
13
13.26
13.46
13.6
13.9
13.91
14
14%
14.3
14.4%
14.5
15
15%
15.59
15.6
16
16.3%
17
19
19.3
20%
20
20.6%
21.9%
22.0%
24
24.2%
24.22
25%
25.9%
26
27%
28%
30%
30
34%
35
35%
40
40%
40.79
40.9%
41
42
43
43.05
44
45%
45
49
50
51
52
55
55%
60%
64
70%
70
73
74%
90
91
100%
100
104
107
126
140
145
146
150%
154
155
158
163
169
170
171
175
180
187
187.25
191
200
221
224
229
236
250
256.5
350
360
370
375
400
449.6
500
550
570
800
2014
2015
2016
2019
2020
2025
2026
2027
2028
2030
2050
20261102
1,100
3,239
4,094
4,201
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
{"meta":{"ticker":"XOM","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"ExxonMobil Holdings Corporation"},"oneliner":"XOM 體質比上個循環好（成本節省、Guyana 與 Permian 放量、債少），但 187 美元買到的是荷莫茲中斷期的高峰獲利：FY2026 共識 EPS 13.46 約為去年 6.70 的兩倍，以近三年實際 EPS 平均計約 24 倍；2027 原油過剩在前，不追，等約 145 美元或價差正常化後再評","thesis":{"H":[{"id":"H1","text":"上游量成長兌現：Permian、Guyana、LNG 帶動產量（扣除中東影響）每年增 3% 以上","2y":null,"5y":"2030 年 Guyana 約 170 萬桶/日、Permian 年增 9% 的計畫照進度；扣除中東影響的總產量 2030 年較 2026 年增 15% 以上","10y":null,"threshold":"扣除中東影響的產量年增 ≥3%；Uaru 2026 Q4 投產，Golden Pass 第二列 2026 年 12 月實質完工、第三列 2027 年中機械完工","source":"公司季報產量揭露與法說","drift_rule":"5 年期：TTM 產量成長低於門檻，偏離連 4 季 ≥5% 判削弱，連 6 季 ≥10% 判反轉"},{"id":"H2","text":"常態價差下 EPS 站上 10 美元：結構成本節省 2030 年達 200 億、Energy Products 單位盈餘結構性提升、回購縮股，使中循環 EPS 高於 FY2023 至 FY2025 實際平均 7.81","2y":null,"5y":"FY2030 調整後 EPS 在常態價格下 ≥10.5","10y":null,"threshold":"價差正常化後第一個完整年度（預估 FY2028）EPS ≥9.5；結構成本節省 2027 年底 ≥180 億","source":"公司季報、法說與年度規劃新聞稿","drift_rule":"5 年期：TTM EPS 偏離 Base 路徑連 4 季 ≥5% 判削弱，連 6 季 ≥10% 判反轉"},{"id":"H3","text":"股東回饋穿越週期而不傷資產負債表：2027 年回購 200 億、股利續增，淨負債與信評守住","2y":"2027 至 2028 年淨負債 ≤400 億美元，信評維持 AA- 與 Aa2","5y":null,"10y":null,"threshold":"淨負債 ≤400 億美元且信評不降","source":"季報資產負債表、信評機構公告","drift_rule":"2 年期：淨負債偏離門檻連 2 季 ≥5% 判削弱，連 3 季 ≥10% 判反轉"}],"R":[{"id":"R1","text":"煉油價差正常化快於預期：荷莫茲復航、中東煉廠修復、中國提高成品油出口，Energy Products 盈餘回到 Q2 水準","h_ref":"H2","clock":"⚡","threshold":"Energy Products 單季調整後盈餘低於 50 億美元（Q2 約 41 億、Q3 91 億）","evidence_refs":["end_markets#0"]},{"id":"R2","text":"2027 原油供給過剩：IEA 估約 500 萬桶/日、EIA 約 370 萬桶/日，majors 與 OPEC+ 同時擴產，JPMorgan 估 2027 年 Brent 均價 64 美元；前兩次下行，2015 年獲利腰斬、2020 年虧損","h_ref":"H2","clock":"🔥","threshold":"Upstream 單季調整後盈餘連 2 季低於 55 億美元（Q3 73 億）","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","cyclical_supply_discipline_capacity#1","cyclical_inventory_price_position#1","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"id":"R3","text":"電動車替代壓低需求天花板與終端倍數","h_ref":"H1","clock":"🐢","threshold":"IEA 估電動車替代量在 2028 年前超過 350 萬桶/日，或全球油需連 2 年下滑","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"法律與政治吃掉超額價差：暴利稅、加州塑膠回收訴訟、密西根反壟斷訴訟、德州 CO2 管線反壟斷訴訟","h_ref":"H3","clock":"🔥","threshold":"任一案件不利判決或和解超過 10 億美元，或歐美通過針對煉油的暴利稅","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#1"]},{"id":"R5","text":"地緣資產受損拖慢量的成長：卡達 LNG 兩列要修數年、Stabroek 30% 面積卡在邊界爭議、Q4 中東影響量仍有 35 萬桶/日","h_ref":"H1","clock":"🔥","threshold":"2027 年中中東影響量仍超過 30 萬桶/日，或邊界爭議波及已開發區塊","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]}],"single_thing":{"description":"荷莫茲海峽全面復航，中東煉能與出口恢復（含卡達以外的波斯灣產量回流）","why_fatal":"FY2026 與 FY2027 共識（13.46、12.01）建立在中斷期價差上。管理層估全球成品油短缺約三分之一來自中東出口受阻，IEA 的 2027 年約 500 萬桶/日過剩也以波斯灣產量恢復為前提。復航會同時打掉煉油超額價差、放出原油供給，是 EPS 最大的單一敏感項","if_happens":"Energy Products 單季盈餘回到 Q2 約 41 億附近，Upstream 跟著油價下滑，FY2027 EPS 落到 Base 的 11 以下，甚至 Bear 的 9 至 10；持有者分批了結，未持有者不追，等價格到重評條件","how_monitor":"公司每季揭露的中東影響量（Q4 指引 35 萬桶/日）、海峽航運恢復新聞、EIA 週度成品油庫存、Energy Products 季盈餘","probability":"12 至 24 個月內約 55%：管理層自承無法預測時點（Q2 法說），但 IEA 的 2027 平衡表已假設恢復"}},"appendix_a":{"growth_durability":5,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.59,"peg_fy2":-1,"stress":{"pass":3,"total":5},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-11-02）"},"eps_meta":{"base_eps_path":{"FY2025A":6.7,"FY2026E":13.46,"FY2027E":12.01,"FY2028E":null},"fy_end_month":12,"eps_basis":"FY2025A 為年報 GAAP 稀釋 EPS；FY2026E、FY2027E 為 yfinance 分析師共識平均，口徑可能偏調整後；FY2028E 共識事實表未涵蓋，留空"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"整合型油氣，獲利跟著油價與價差擺動：2020 年度虧損 224 億、2015 年獲利約為 2014 年一半；EPS 由 FY2022 13.26 降到 FY2025 6.70，再被中斷期推回 FY2026 共識 13.46"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉。IEA 2026 年 6 月首份 2027 平衡表估供給增約 800 萬桶/日、過剩約 500 萬桶/日，與波斯灣產量恢復、OPEC+ 提高目標連動；EIA 估 2027 過剩約 370 萬桶/日；成品油緊張取決於荷莫茲復航與俄羅斯煉廠修復","bargaining":{"up":"上游的對手是資源國。Guyana 已回收 550 億美元投資，權益量將調整（Q2 法說），分成往政府端移","down":"賣給批發、零售與工業客戶，產品可完全替代，價差由全球供需決定，沒有議價權","geo":"卡達 LNG 兩列受損、阿聯產量出口受阻（Q3 法說）；Guyana 與委內瑞拉有邊界爭議"},"profit_pool_dir":"中斷期利潤池移向煉油環節（Energy Products 由 Q2 約 41 億升到 Q3 91 億）；常態化後回流上游，長期往資源國與低碳替代移","tam_table":{"expanded":false,"reason":"成熟商品市場，不是低滲透或份額擴張的故事；需求總量改看 IEA、EIA、OPEC 機構預測，已寫進供需判讀；本季利潤池移向煉油屬週期性，不是結構性遷移"}},"moat":{"mechanism":"規模與成本：全球最大非國營煉油網路，加上低成本上游資源（Guyana、Permian），以及集中式專案、技術與營運組織；在整合價值鏈上用交易調度放大資產價值","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面在進步：結構成本節省 Q2 163 億、Q3 169 億，Permian 單季創紀錄逾 180 萬桶油當量/日，Golden Pass 第一列接近銘牌產能。但同業 TTM 營業利益率與 FCF 利潤率 XOM 都是五家最低，同業差距擴大沒有獨立證據，定價權也沒有變化，判穩定","peer_na_reason":"同業 ROIC 與 ROCE 事實表未涵蓋，只能用利潤率對照；利潤率又受煉油營收比重與期間不同扭曲（XOM、CVX、COP 到 2026-06；SHEL、TTE 到 2026-09）","threats":[{"level":"🟡","text":"電動車替代：IEA 估 2025 年已替代約 170 萬桶/日、2030 年約 500 萬桶/日，油價衝擊讓電動車使用成本優勢擴大 20% 至 45%。衝擊的是全產業需求天花板，不改 XOM 對同業的相對位置，屬點對點","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"地緣資產：卡達 LNG 兩列受損，約占全球產量 3%，修復需數年；Stabroek 約 30% 面積因委內瑞拉邊界爭議未探勘；Q4 仍有約 35 萬桶/日的中東影響","p":"40%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"level":"🟡","text":"法律與政策：加州塑膠回收訴訟、密西根指控合謀延緩能源轉型、德州 CO2 管線反壟斷私人訴訟；另有歐洲暴利稅與甲烷法規（後者已延後 3 年）","p":"25%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#1"]},{"level":"🟡","text":"同業共享成長資產：CVX 經 Hess 持有 Stabroek 30%，Guyana 成長不是 XOM 獨享；歐洲大廠 2030 年前成長偏弱，反而是相對優勢","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×低周轉（TTM 營業利益率 10.7%；投入資本周轉率事實表未涵蓋，依資產密集度暫判）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"油氣是需要不是想要，延後購買的代價高。但 IEA 估電動車 2025 年已替代約 170 萬桶/日、2030 年約 500 萬桶/日，油價衝擊又讓電動車省下的使用成本增 20% 至 45%，需求基礎值被侵蝕的速度在加快；公司自家展望稱 2050 年前油需仍高於 1 億桶/日，屬公司來源"},{"item":"決策層級","level":"🔴","text":"在最小決策單位（一桶原油、一加侖柴油）上完全可替代，客戶沒有轉換成本，本季的超額價差不受任何客戶鎖定保護；只有 LNG 長約、CCS 合約（8 家客戶、每年 1,100 萬噸，Q3 法說）與潤滑油品牌有合約年限"},{"item":"價值鏈分配","level":"🟡","text":"本季利潤池移向煉油（Energy Products 由 Q2 約 41 億升到 91 億），XOM 以全球最大非國營煉油商的身分（每日 360 萬桶）吃到。上游端資源國分成在上升：Guyana 已回收 550 億投資，權益量將調整（Q2 法說 Hansen、Woods），價值鏈分配長期往資源國移"},{"item":"社會容忍度","level":"🔴","text":"高必需又高敏感。CEO 自承高油價衝擊民生（Q3 法說）；歐洲上次課暴利稅後，公司取消了歐洲投資，對下一次能否擋住則說不確定（Q2 法說）。加州塑膠回收、密西根反壟斷兩案在進行。中斷期創高的煉油價差，正是政治上限最先壓下來的部分"}],"roiic":"事實表未涵蓋投入資本與折舊，算不出全公司數字。管理層個案：Beaumont 20 億擴建約 3 年回本（Q3 法說 Woods）、Pioneer 綜效由每年 20 億升到 40 億（Q3 法說 Hansen）；這些是自報個案，不能當全公司增量報酬","reinvest_rate":"事實表未涵蓋 NOPAT 與折舊；現金口徑：Q3 資本支出 70 億÷營業現金流 256.5 億，約 27%","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率，兩個輸入都缺，故不給數字。成長題改用產量計畫當代理（2027 年前加 50 萬桶油當量/日，對 449.6 萬的基數約年增 5%），只作合理性對照，不當天花板"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","XOM":20.63,"CVX":32.36,"SHEL":18.69,"TTE":32.33,"COP":27.68,"unit":"%"},{"metric":"營業利益率","XOM":10.72,"CVX":12.37,"SHEL":14.36,"TTE":16.25,"COP":21.92,"unit":"%"},{"metric":"FCF 利潤率","XOM":8.46,"CVX":12.94,"SHEL":11.63,"TTE":10.5,"COP":15.89,"unit":"%"},{"metric":"研發密度","XOM":null,"CVX":null,"SHEL":0.3,"TTE":null,"COP":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"CVX","gm":32.36,"om":12.37,"fcf_margin":12.94,"rd_intensity":null,"strategy_note":"經 Hess 持有 Stabroek 30%，與 XOM 共享 Guyana 成長，是同一資產上最直接的對手；TTM 利潤率高於 XOM","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SHEL","gm":18.69,"om":14.36,"fcf_margin":11.63,"rd_intensity":0.3,"strategy_note":"分析師稱歐洲大廠 2030 年前成長偏弱；利潤率期間到 2026-09，含 Q3 高價差季，不能直接比","period":"TTM ending 2026-09-30（4季加總）"},{"name":"TTE","gm":32.33,"om":16.25,"fcf_margin":10.5,"rd_intensity":null,"strategy_note":"毛利率與營業利益率高於 XOM，期間同樣到 2026-09，含高價差季","period":"TTM ending 2026-09-30（4季加總）"},{"name":"COP","gm":27.68,"om":21.92,"fcf_margin":15.89,"rd_intensity":null,"strategy_note":"純上游，沒有低利潤率的煉油營收；利潤率最高反映業務結構不同，不代表成本優勢","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"內生部分是量（Guyana、Permian、LNG）、結構成本節省與回購；FY2026 至 FY2027 的跳升來自價格與價差","runway_years":"約 4 年（以 2030 產量計畫的可見度計；油氣不適用滲透率口徑）","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC×再投資率的輸入缺（事實表未涵蓋投入資本與折舊），改以產量計畫約年增 5% 加回購約 2.6% 為代理，定價不變下每股約 5% 至 8%/年；兩年共識 EPS 年複合約 34%，遠超此代理，缺口歸因中斷期價差","segments":[{"item":"Upstream（Q3 2026 調整後盈餘）","value":"73 億美元，較 Q2 下滑（原油價格走低）；量靠 Permian、Guyana 成長"},{"item":"Energy Products","value":"91 億美元（Q2 約 41 億），來自中斷期煉油價差"},{"item":"Chemical Products","value":"7.25 億美元（Q2 約 12 億），化工價差下滑"},{"item":"Specialty Products","value":"約 13 億美元，基礎油價差走高"}],"decay_signals":[{"signal":"EPS CAGR 顯著高於營收 CAGR","lit":true,"evidence":"FY2025 到 FY2027 共識 EPS 年複合約 34%，營收約 14%"},{"signal":"TAM 被替代技術壓縮","lit":true,"evidence":"IEA：電動車替代 2025 年約 170 萬桶/日、2030 年約 500 萬桶/日"},{"signal":"FCF/NI<0.75 連 2 年","lit":false,"evidence":"FY2024 約 0.91、FY2025 約 0.82（年報）"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"營收 FY2023 至 FY2025 下滑，但每季仍投資約 70 億擴產"},{"signal":"毛利率連 2 季 YoY 下滑","lit":null,"evidence":"季度毛利率事實表未涵蓋；年度毛利率由 FY2022 25.9% 降到 FY2025 22.0%"},{"signal":"maintenance capex 占 FCF>60%","lit":null,"evidence":"維持性資本支出事實表未涵蓋"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，量來自 Guyana、Permian、LNG 自建專案。回購與股利是承重項，但近三年現金去向與回購均價事實表未涵蓋，只能用 Q3 一季與年報 FCF 推算，已寫在理由"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Pioneer 綜效由每年 20 億升到 40 億（Q3 法說 Hansen）；收購後實際增量報酬與資金成本事實表未涵蓋，無法判斷","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購買入收益率 trailing 約 5.2%、FY2027 共識約 6.4%；10 年期公債殖利率事實表未涵蓋，無法對門檻","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"平均股數由 FY2025 約 43.05 億（年報淨利÷稀釋 EPS）降到目前 40.79 億，淨縮股；SBC 金額事實表未涵蓋，但淨稀釋率為負","grade":"過"}]},"valuation":{"basis":"本益比，以 FY2026 共識、FY2027 共識與 FY2023 至 FY2025 實際 EPS 平均三種分母對照","tier":"整合型油氣大廠","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，未涵蓋同業前瞻本益比或股價淨值比，無法在同層級對錨"},"fwd_pe":13.91,"peg":null,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"商品循環股優先看股價淨值比，但事實表未涵蓋。改用三種分母：FY2026E 13.9 倍、FY2027E 15.6 倍、FY2023 至 FY2025 實際平均 24 倍；trailing 19.3 倍與 P/S、EV/S 都在年度端點最高。五年連續分位事實表未涵蓋；PEG 不適用，因為 FY2026 到 FY2027 共識 EPS 下滑，且沒有 FY2028 共識。分母正是爭點，便宜的論證不成立；Base 一年與三年目標都低於現價，判偏貴（紅）","upside_short_pct":-8.7,"upside_mid_pct":-17.5},"trap_analysis":{"verdict":"🟡","label":"高峰獲利陷阱：前瞻本益比被中斷期價差壓低"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"IEA 估 2027 年供給增約 800 萬桶/日、過剩約 500 萬桶/日，EIA 估約 370 萬桶/日，JPMorgan 估 2027 年 Brent 均價 64 美元；majors 上游持續擴產。前兩次下行：2015 年獲利約為 2014 年一半，2020 年全年虧損 224 億、股價跌 40.9%，Brent 2014 至 2016 年跌約 70%","assumption":"共識假設 FY2027 EPS 只比 FY2026 少一成（13.46 降到 12.01），中斷期價差緩慢退場","consequence":"荷莫茲復航撞上 2027 年過剩，FY2028 EPS 落到 7 附近，倍數壓到 13 倍，股價回到 100 美元左右，五年後虧近半","ruling":"採納：這是 Bear 35% 機率與下檔 −35% 至 −55% 的來源，也是不追的主因。它與 Single Thing 是同一條因果鏈，復航就是觸發點，兩者重疊，不另立","watch":"IEA、EIA 月報的 2027 平衡表、Upstream 季盈餘、公司揭露的中東影響量","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","cyclical_supply_discipline_capacity#1","cyclical_inventory_price_position#1","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"view":"論點成功但股東經濟變差","evidence":"2027 年回購固定 200 億，谷底用資產負債表補（Q3 法說 Woods）；以 trailing 19.3 倍買回，收益率約 5.2%。Guyana 成本回收完成後權益量將調整（Q2 法說）。社會容忍度紅燈：上次歐洲暴利稅後公司取消歐洲投資，CEO 對能否擋下一次說不確定（Q2 法說）；加州、密西根、德州三案進行中","assumption":"產量與成本目標達成，超額價差留在股東手上","consequence":"量的成長與成本下降都兌現，但回購買在高點倍數，資源國分成上升，暴利稅分走價差，每股盈餘成長低於產量成長","ruling":"部分採納：回購穿越週期的紀律本身合理，不改 Base EPS 路徑；但 Base 終端倍數不給高於 15 倍，法律與暴利稅列為風險觸發","watch":"歐美暴利稅立法、三案判決或和解金額、Guyana 權益量調整（2030 計畫更新）、回購執行價對常態化 EPS 的倍數","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#1"]},{"view":"價格已反映太多","evidence":"26 週漲 24.2%，現價較 52 週均線高約 28%；trailing 本益比 19.3 倍、P/S 1.97、EV/S 2.02 都在近四個年度端點最高；賣方聚合目標價均值 158 至 170 美元，都低於現價","assumption":"市場把中斷期獲利當成新常態","consequence":"即使 FY2027 共識 12.01 兌現，15.6 倍也沒有重估空間；價差一回落就直接反映在股價","ruling":"採納：估值結論偏貴，等價格回落或價差正常化後再評","watch":"股價與 52 週均線的距離、FY2027 共識的修正方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 187.25","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=187.25","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"煉油緊張延續多久","cause":null,"prior_field":null,"side_a":"管理層：全球成品油短缺約三分之一來自中東出口受阻，俄羅斯約一半煉能下線，恢復平衡至少要到明年之後，可能更久（Q3 法說 Woods）","side_b":"IEA、EIA 預估 2027 年原油過剩 370 至 500 萬桶/日；JPMorgan 估 2027 年 Brent 均價 64 美元","ruling":"可調和，屬程度差異：兩邊講的是不同市場，原油過剩與成品油緊張可以同時成立，FY2027 上游先走弱、煉油晚一步。Base 照這個順序排，FY2027 EPS 11.4，低於共識 12.01","evidence_level":"管理層前瞻說法對機構預測，兩邊都還沒實現","settle_metric":"Upstream 與 Energy Products 2027 Q1、Q2 調整後盈餘","if_then":["若 2027 上半年 Energy Products 低於 50 億且 Upstream 低於 55 億：Bear 機率上調到 40%，維持不追","反向：若 2027 上半年兩者都不低於 2026 Q3，且 FY2027 共識上修到 13 以上：重跑判斷，評估分批建立首倉 2%"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","end_markets#1"]},{"axis":"結構改善對同業利潤率","cause":null,"prior_field":null,"side_a":"管理層：Energy Products 單位盈餘自 2019 三倍、結構成本節省 169 億、專案成本低 20%、工期快 20%（Q3 法說）","side_b":"事實表 TTM 營業利益率與 FCF 利潤率，XOM 在五家同業中最低","ruling":"可調和：XOM 煉油營收比重高，壓低比率，且期間不同（XOM 到 2026-06，SHEL 與 TTE 到 2026-09）。但這也表示「優於同業」目前只有公司自述，護城河趨勢判穩定，不判擴大","evidence_level":"公司自述對第三方財報數據，口徑不一","settle_metric":"同期間 ROCE 或 ROIC 對照（事實表未涵蓋）","if_then":["若補到同期間資料仍顯示 XOM 營業利益率低於 CVX：執行分維持 8，不上調","反向：若 ROCE 顯示 XOM 領先最強同業 3 個百分點以上且連 2 年擴大：趨勢改判擴大，護城河等級上調一級"],"evidence_refs":[]},{"axis":"固定回購對週期現金流","cause":null,"prior_field":null,"side_a":"管理層：2027 年回購維持 200 億、股利不會砍，谷底用資產負債表補（Q3 法說 Woods、Hansen）","side_b":"FY2025 自由現金流 236 億，低於 2027 年股利約 175 億加回購 200 億；常態價格下每年缺口約 140 億，淨負債 221 億約 1.6 年翻倍","ruling":"可調和：本季已降債逾 90 億，緩衝撐得過兩年常態價格；第三年若仍是低價，回購勢必縮減，列入 H3 與減碼觸發","evidence_level":"年報與季報實績對管理層承諾","settle_metric":"淨負債、信評、回購執行額","if_then":["若淨負債超過 400 億美元或信評遭降：持有者減碼一半","反向：若常態價格下連 2 季自由現金流覆蓋股利加回購：H3 確認，移除壓力測試該項扣分"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：FY2026 13.9 倍、FY2027 15.6 倍不算貴；俄羅斯煉廠要先停火才能修，卡達 LNG 要修 3 至 5 年，緊張可能延續到 2028；Uaru 2026 Q4 投產、Golden Pass 第二列 12 月完工，量在成長；股利 44 年連增、200 億回購與 AA- 信評給下檔支撐","side_b":"賣方：FY2026 EPS 已是 FY2025 的兩倍，任一中斷因素消失就會回落；現價高於多數賣方目標價，trailing 倍數在年度端點最高","ruling":"採賣方側：買方情境我給 20% 機率（Bull 終點約 229 美元），不足以在年度端點最高的倍數追價。分歧核心在中斷期獲利是不是新常態，依據是 IEA、EIA 的 2027 過剩預測，以及管理層自己對正常化時點的描述","evidence_level":"機構預測與公司自述，2027 上半年季報可以裁決","settle_metric":"FY2027 共識 EPS 修正方向與 2027 Q1 分部盈餘","if_then":["若股價續漲而 FY2027 共識沒有上修：不追","若股價回到約 145 美元而 FY2027 共識仍 ≥10：重跑判斷，評估分批建立首倉 2%","反向：若 2027 Q1 分部盈餘證實價差延續，且 FY2027 共識上修到 13 以上：Bull 機率上調到 30%，重跑判斷"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"股價回到常態化估值區：約 145 美元以下，且 FY2027 共識 EPS 仍 ≥10","type":"估值rearm","maps_to":"H2","metric":"週收盤價、FY2027 共識 EPS","threshold":"股價 ≤145 且 FY2027 共識 ≥10","action":"重跑判斷，通過後分批建立首倉 2%","source_freq":"每週收盤、每月共識","date":null},{"n":2,"text":"荷莫茲全面復航、中東出口恢復","type":"Single Thing","maps_to":"R1","metric":"公司揭露的中東影響量、海峽航運狀況","threshold":"中東影響量低於 10 萬桶/日，或海峽正式恢復通行","action":"持有者分批了結一半；未持有者不追，等正常化後第一季數字出來再重跑","source_freq":"季報、每週航運新聞","date":null,"evidence_refs":["geo_supply_chain#1","supply_demand_durability#0"]},{"n":3,"text":"量的里程碑：Uaru 投產、Golden Pass 第二列完工","type":"假設驗證","maps_to":"H1","metric":"專案投產公告","threshold":"Uaru 於 2026 Q4 投產，Golden Pass 第二列 2026 年 12 月實質完工","action":"延遲超過一季：H1 削弱，Base 2028 EPS 下調 0.3 後重算","source_freq":"季報、公司新聞稿","date":"2026-12"},{"n":4,"text":"上游盈餘跌破常態，2027 原油過剩兌現","type":"風險","maps_to":"R2","metric":"Upstream 單季調整後盈餘","threshold":"連 2 季低於 55 億美元","action":"Bear 機率上調到 40%，維持不追；持有者減碼到 1.5% 以下","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","cyclical_inventory_price_position#1"]},{"n":5,"text":"法律判決或暴利稅落地","type":"風險","maps_to":"R4","metric":"判決、和解金額、立法","threshold":"單案超過 10 億美元，或通過針對煉油的暴利稅","action":"Base 終端倍數由 15 倍降到 14 倍重算；持有者停止加碼","source_freq":"法院公告、新聞","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#1"]},{"n":6,"text":"資產負債表被回購撐破","type":"減碼","maps_to":"H3","metric":"淨負債、信評","threshold":"淨負債超過 400 億美元，或信評遭降","action":"持有者減碼一半","source_freq":"季報、信評公告","date":null},{"n":7,"text":"2027 規劃新聞稿與 Q4 財報複審","type":"複審日期","maps_to":"H2","metric":"2027 規劃指標、Q4 調整後 EPS、中東影響量","threshold":"規劃指標與本次 Base 假設（量年增 3%、回購 200 億）對照","action":"重跑判斷","source_freq":"一次性","date":"2027-01"}],"kill_metrics":[{"metric":"Energy Products 單季調整後盈餘","bear_threshold":"低於 50 億美元","window":"2027 Q1 至 Q2","source":"公司季報新聞稿","last_status":"ok"},{"metric":"Upstream 單季調整後盈餘","bear_threshold":"連 2 季低於 55 億美元","window":"2027 全年","source":"公司季報新聞稿","last_status":"ok"},{"metric":"淨負債","bear_threshold":"超過 400 億美元","window":"滾動 4 季","source":"公司季報資產負債表","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"低於 10 美元","window":"2027 Q2 前","source":"yfinance 分析師共識","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把中斷期獲利當常態：FY2027 共識只比 FY2026 少一成（13.46 降到 12.01），但 IEA 與 EIA 預估 2027 年原油過剩 370 至 500 萬桶/日，JPMorgan 預估 2027 年 Brent 均價 64 美元，而管理層自己也說價差正常化要看荷莫茲復航與煉廠修復"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=24.22, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"≤3%（循環股，晚循環期間不新建）","requires_critic":[],"rearm_trigger":"股價≤145 美元（常態化 EPS 約 10×14.5 倍）且 FY2027 共識 EPS 仍 ≥10：重跑判斷，評估分批建立首倉","exec_line":"未持有：不追；價格先漲而證據未到，也不追。觸發重評後首倉 2%，第二批等價差正常化後的第一季數字確認 FY2027 共識沒有跌破 10 再加。已持有者在荷莫茲全面復航時分批了結一半"},"reasoning":{"industry":"分部：事實表未涵蓋分部營收，以 Q3 2026 分部調整後盈餘代替。Upstream 73 億（較 Q2 下滑，原油價格走低）、Energy Products 91 億（Q2 約 41 億）、Chemical Products 7.25 億（Q2 約 12 億）、Specialty Products 約 13 億；全公司調整後 175 億（每股 4.23）、GAAP 154 億（稀釋每股 3.72）。利潤率：最新一季毛利率與營益率事實表未涵蓋，TTM 到 2026-06 毛利率 20.6%、營益率 10.7%。產業時鐘判 III 過熱：荷莫茲受阻、中東煉廠受襲、俄羅斯約一半煉能下線，煉油價差因此創高（Q3 法說 Woods）；原油價格本季已回落，IEA 與 EIA 都預估 2027 年供給過剩。供需持久度：週期性將反轉。成品油短缺取決於停火與修復，管理層估至少延續到明年；原油端 2027 年過剩 370 至 500 萬桶/日。議價：錢卡在煉油與上游資源兩個節點；客戶端沒有集中度（美國品牌站點約 1 萬個），商品化產品沒有定價權。單點依賴：Guyana Stabroek（XOM 45%）是量與現金流轉折的主軸，約 30% 面積因委內瑞拉邊界爭議擱置；本季獲利的另一個依賴是中斷期價差。產業態勢：雙向拉鋸。競爭面在惡化，majors 上游持續擴產（XOM 2027 年前加 50 萬桶油當量/日、CVX 年增逾 3%），加上 2027 年過剩；另一面，Rystad 估非 OPEC 產量 2027 年見頂，天然遞減率約 15%/年（公司展望），支撐中期投資需求","moat":"機制是成本與規模：全球最大非國營煉油商、Permian 自動化鑽機與長水平井、專案執行（管理層稱大型專案數為最近對手兩倍、成本低 20%、工期快 20%，Q3 法說 Hansen），以及整合價值鏈下的交易調度。可證方向：同業 ROIC 事實表未涵蓋，改用利潤率。TTM 營業利益率 XOM 10.7%，低於 CVX 12.4%、SHEL 14.4%、TTE 16.3%、COP 21.9%；FCF 利潤率 8.5% 也是五家最低。這組對照被兩件事扭曲：XOM 營收含大量煉油銷售（每日賣 570 萬桶產品），壓低比率；而且 XOM 期間到 2026-06，SHEL 與 TTE 到 2026-09，含 Q3 高價差季。評分：執行力 8 分，依據是成本節省 169 億、Energy Products 單位盈餘自 2019 三倍、Guyana 11 年產出 10 億桶。定價權 6 分，原油與成品油是價格接受者，只有特用品、潤滑油品牌與 LNG 長約有部分議價。合併 7 分，屬 B 級。執行在擴大、定價持穩，但缺同業報酬差距可證，趨勢只給穩定。報酬持續期：決策層級與社會容忍度兩項紅燈，本季超額報酬撐不久。增量報酬只有管理層個案（Beaumont 擴建約 3 年回本、Pioneer 綜效由每年 20 億升到 40 億）；投入資本與折舊事實表未涵蓋，算不出全公司增量 ROIC","growth":"成長組成：FY2025 實際 EPS 6.70 到 FY2027 共識 12.01，兩年年複合約 34%；同期共識營收由 3,239 億到 4,201 億，年複合約 14%。EPS 比營收快約 20 個百分點，來源是價差擴大，也就是價格，不是量。三年共識：FY2028 共識事實表未涵蓋，只能算兩年。內生上界：增量 ROIC 與再投資率算不出（見護城河題），改用代理，產量計畫約年增 5% 加每年約 2.6% 的回購，定價不變下每股約 5% 至 8%。共識與代理之間的缺口歸因於利潤率擴張（中斷期價差），可以歸因，但不能外推。跑道：Permian 計畫年增 9% 到 2030；Guyana 2030 年 170 萬桶/日（八個開發案）；Golden Pass 第二列 12 月實質完工、第三列 2027 年中機械完工；Rovuma 目標年底做最終投資決策。2030 之後，管理層稱有清楚的專案組合，但要等到有承諾的信心才公開（Q3 法說 Woods），屬未證的第二曲線，所以給黃燈，不給綠燈。衰退訊號亮兩項：EPS 成長遠快於營收（價差驅動），以及替代技術壓縮需求天花板（電動車）","governance":"轉換率：FCF 對淨利 FY2022 1.05、FY2023 0.93、FY2024 0.91、FY2025 0.82（年報）；Q3 2026 自由現金流 191 億，GAAP 淨利 154 億。轉換健康，但連三年下滑。SBC 對營收事實表未涵蓋。Q3 現金去向：營業現金流 256.5 億，分成資本支出 70 億、股利 43 億、回購 51 億，其餘約 90 億降債（CFO 稱淨負債降逾 90 億）。股數：以年報淨利÷稀釋 EPS 推得 FY2025 平均約 43.05 億股，現在 40.79 億股，回購確實在縮股。壓力：2027 年股利（每季 1.07×目前股數）約 175 億，加回購 200 億，合計約 375 億；FY2025 自由現金流只有 236 億。若價格回到 2025 年水準，每年缺口約 140 億，以目前淨負債 221 億計約 1.6 年翻倍。管理層明說谷底會用資產負債表補（Q3 法說 Woods）。併購：Pioneer 綜效倍增到每年 40 億，但收購後實際增量報酬事實表未涵蓋。回購買入收益率：以 trailing 19.3 倍計約 5.2%，以 FY2027 共識 15.6 倍計約 6.4%；10 年期公債殖利率事實表未涵蓋，無法判斷是否過門檻","valuation":"現價 187.25 對 FY2026 共識 13.46 是 13.9 倍，對 FY2027 共識 12.01 是 15.6 倍，看似合理。但 FY2026 EPS 約為 FY2025 實際 6.70 的兩倍，是荷莫茲受阻、卡達 LNG 受損、俄羅斯煉能下線堆出來的價差；以 FY2023 至 FY2025 實際 EPS 平均 7.81 計是 24 倍。trailing 本益比 19.3 倍、P/S 1.97、EV/S 2.02 都在近四個年度端點的最高位（不是五年連續分位）。賣方聚合目標價均值 158 至 170 美元，都低於現價；10 月個別調整中只有 Barclays 的 200 美元高於現價，Wells Fargo 已降評。同業倍數事實表未涵蓋，無法在同層級對錨。Base 情境一年後（FY2027 EPS 11.4×15 倍）為 171 美元，三年後（FY2029 EPS 10.3×15 倍）為 155 美元，都低於現價","premortem":"反方最強的數字：2015 年獲利約為 2014 年一半、2020 年全年虧損 224 億、股價 2020 年跌 40.9%、Brent 2014 至 2016 年由逾 100 美元跌破 30。現價較 52 週均線 146 高約 28%，較 250 週均線 107 高約 74%；回到 104 週均線約 −33%，回到 250 週均線約 −43%。壓力測試五項過三：淨負債低於單季營業現金流（過）；信評 AA- 與 Aa2（過，來源為第三方網站）；FCF 對淨利連兩年 ≥0.75（過）；常態價格下 FCF 覆蓋股利加回購（不過，每年缺口約 140 億）；前兩次下行年度沒有虧損（不過，2020 年虧損）。訴訟：證券集體訴訟 2026-05 由陪審團判公司全勝，約 30 億求償解除；加州塑膠回收、密西根反壟斷、德州 CO2 管線三案的求償金額與時點事實表未涵蓋。法說迴避：Q2 對荷莫茲現況、煉油獲利拆解、歐洲暴利稅可能性、歲修延後規模都沒有正面回答"},"plain":{"six":{"how_it_makes_money":"賺油價與煉油價差的錢：上游賣原油、天然氣與 LNG，下游煉油、化工與特用品；本季錢卡在煉油節點，Energy Products 調整後盈餘 91 億美元，占全公司 175 億的一半以上，屬中斷期的超額價差","moat":"護城河 B 級、趨勢穩定：優勢在規模、上下游整合與低成本資源（Guyana、Permian），定價權有限；同業利潤率對照證明不了差距在擴大","growth":"成長跑道中等（黃燈）：量的成長看得到 2030（Guyana、Permian、LNG），之後的第二曲線管理層還沒公開；FY2026 的 EPS 翻倍來自價格，不是成長","capital":"資本配置紀律穩：本季降債逾 90 億、股利連 44 年增、回購穿越週期不隨油價調整；扣分在固定 200 億回購正好買在高點倍數，常態價格下要靠資產負債表補","valuation":"偏貴：現價要 FY2027 之後 EPS 穩在 12 以上，或市場長期給 17 倍以上才划算；我不信，因為分母是中斷期高峰","how_wrong":"最可能看錯的地方是把中斷期獲利當常態；價值陷阱風險中等（兩項衰退訊號亮燈），下檔可達 −35% 至 −55%"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把中斷期獲利當常態：FY2027 共識只比 FY2026 少一成（13.46 降到 12.01），但 IEA 與 EIA 預估 2027 年原油過剩 370 至 500 萬桶/日，JPMorgan 預估 2027 年 Brent 均價 64 美元，而管理層自己也說價差正常化要看荷莫茲復航與煉廠修復","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到約 145 美元（常態化 EPS 約 10×14.5 倍），或價差正常化後的第一季數字出爐、FY2027 共識仍 ≥10，再重評","trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":187.25,"week26_return_pct":24.22,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026E 共識 13.46 含中斷期超額煉油價差（Energy Products Q3 91 億、Q2 41 億）與高油價，約為 FY2025 實際 6.70 的兩倍；用它當分母算出的 13.9 倍不代表便宜。常態化分母約 10（Base FY2028）時，現價約 19 倍"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"2027 年規劃指標新聞稿，取代 12 月的企業計畫說明會","impact":"高","watch":"產量、資本支出、成本節省目標是否與 Base 假設一致"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"Guyana 第五個開發案 Uaru 投產","impact":"中","watch":"投產時點與爬坡速度"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"Golden Pass 第二列實質完工","impact":"中","watch":"是否如期完工、試車進度"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"Rovuma LNG 最終投資決策","impact":"低","watch":"能否在年底前完成"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與法說","impact":"高","watch":"Energy Products 價差走向、中東影響量、2027 規劃細節"},{"date":null,"date_precision":null,"type":"macro","event":"荷莫茲海峽全面復航","impact":"高","watch":"航運恢復狀況與公司中東影響量"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"Golden Pass 第三列機械完工","impact":"低","watch":"時程是否延誤"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,935B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期</h2>
<p class="lead">B 級護城河、趨勢穩定，優勢在規模與成本，定價權有限。</p>
<ul class="pts">
<li>護城河機制是成本與規模。XOM 是全球最大非國營煉油商，加上 Guyana、Permian 的低成本資源，以及集中式專案與交易調度。管理層稱大型專案數為最近對手的兩倍，成本低 20%，工期快 20%（Q3 法說 Hansen），這是公司自述，尚缺第三方驗證。</li>
<li>評分是執行力 8 分、定價權 6 分，合併 7 分，屬 B 級。執行力的依據是成本節省 169 億美元、Energy Products 單位盈餘自 2019 年起三倍、Guyana 11 年產出 10 億桶。定價權只有 6 分，因為原油與成品油是價格接受者，只有特用品、潤滑油品牌與 LNG 長約有部分議價。</li>
<li>趨勢判穩定，不判擴大。執行面確實在進步，Q2 成本節省 163 億，Q3 169 億，Permian 單季創紀錄逾 180 萬桶油當量/日。但同業利潤率對照中 XOM 最低，沒有獨立證據顯示差距在擴大，所以不上調。</li>
</ul>
<!-- E5 -->
<h3>§5.F 對手財務深度對照</h3>
<ul class="pts">
<li>同業投入資本報酬率（ROIC）與資本報酬率（ROCE）事實表未涵蓋，只能用利潤率。TTM 營業利益率 XOM 為 10.7%，低於 CVX 12.4%、SHEL 14.4%、TTE 16.3%、COP 21.9%。FCF 利潤率 XOM 為 8.5%，同樣是五家最低。毛利率 XOM 20.6%，也低於 CVX 與 TTE 的三成出頭。</li>
<li>這組數字要打折看。XOM 營收含大量煉油銷售，每日賣 570 萬桶產品，天然壓低比率。COP 是純上游，利潤率最高反映業務結構，不代表成本優勢。期間也不同，XOM、CVX、COP 到 2026-06，SHEL 與 TTE 到 2026-09，後兩者含 Q3 高價差季。結論是「優於同業」目前只有公司自述。</li>
</ul>
<!-- E6 -->
<h3>§5.R 報酬持續期檢核</h3>
<ul class="pts">
<li>四個檢查點中兩項亮紅燈。決策層級上，一桶原油、一加侖柴油完全可替代，客戶沒有轉換成本，本季超額價差不受任何鎖定保護。只有 LNG 長約、碳捕捉與封存合約（8 家客戶、每年 1,100 萬噸）與潤滑油品牌有合約年限。</li>
<li>社會容忍度是另一個紅燈。CEO 自承高油價衝擊民生。歐洲上次課暴利稅後，公司取消了歐洲投資，下一次能否擋住則說不確定（Q2 法說）。加州塑膠回收與密西根反壟斷兩案進行中。中斷期創高的煉油價差，正是政治上限最先壓下來的部分。需求基礎與價值鏈分配兩項為黃燈，所以本季超額報酬撐不久。</li>
<li>增量報酬只有管理層個案。Beaumont 20 億美元擴建約 3 年回本，Pioneer 綜效由每年 20 億升到 40 億。投入資本與折舊事實表未涵蓋，算不出全公司增量 ROIC，這些個案不能當全公司數字。</li>
</ul>
<!-- E7 -->
</section>

```