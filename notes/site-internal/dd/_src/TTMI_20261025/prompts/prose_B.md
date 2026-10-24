你是 stock-analyst v20 的**散文層（prose）agent**，標的 TTMI（2026-10-25）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：TTMI　日期：2026-10-25　archetype：None　前份裁決：2026-05-18　觀望偏進場｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1799B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（749B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1005B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1254B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1402B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（618B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1133B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2118B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3344B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2099B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1799           3641-5201      5 條（2–6 內）  
s3                  8000         749           5076-7251      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3661          7937-11339      5 條（2–6 內）  
s6                 11000         618          7267-10382      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1133           1657-2367      3 條（2–6 內）  
s10                 5000        2118           2017-2882      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2099           2000-2901      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5289B；至少需散文≈39.71KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−58
−58%
−52.1%
−46.24
−38%
−38
−27.5%
−4.4%
−0.6
−0.45%
0
0.24
0.38
0.47
0.6%
0.75
0.9
0.91
1.0
1
1.075
1.081
1.2
1.5%
1.5
1.6
1.68
1.77
02
2.0%
2
2.1
2.13
2.2
2.41
2.5
2.61
03
3
3.2
3.5
4
4.2
4.5
4.6
4.96
4.97
5
5%
05
5.03
5.6
6
06
6.5
6.7
6.75%
7%
7
7.2
7.3
7.68
8
08
8.10
8.3
8.34
8.90
8.9
9
9%
09
9.5
9.6
9.61
9.9%
10%
10
10.06
10.3
10.8%
11%
11
11.4
12
12.04
12.5
13
13.5%
13.6
14
14%
14.2
14.4
14.5
14.9%
15
15%
15.2
16
16.1%
16.15
16.2
17.4%
17.5
17.7%
18
18%
20
20%
20.1%
20.2%
21
21%
22
23%
24%
24
24.8%
25
26%
26
27
30
30%
31%
32%
32.0
33
34%
35
35%
36
40
41%
42
42%
44%
44.7
45
46%
47%
49
49%
50
50%
51.4%
52
52.1%
55%
60%
65
65%
65.9
67
67%
67.5
68%
70
78.9
80.11
90
97%
100
100%
104
111%
115%
116.38
134
150
150%
167.35
175
180
200
217.5
220
330
400
800
2009
2019
2024
2025
2026
2027
2028
2029
2030
2034
2368
3037
20261025
1,210
2,000
2,410
3,390
4,500
7,480
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
{"meta":{"ticker":"TTMI","date":"2026-10-25","schema":"v15.0","contract":"v19","company_name":"TTM Technologies, Inc."},"oneliner":"AI 資料中心 N+M 板與國防訂單把 TTM 推上紀錄獲利，股價卻半年腰斬；2027 年有訂單與指引撐腰，2028 年中國新產能開出與舉債併購是還沒解的兩個問題。","thesis":{"H":[{"id":"H1","text":"N+M 不對稱板放量：資料中心營收中 N+M 占比由約三成升到 2027 年約五成，帶動調整後 EBITDA 利益率在 2027 年再升 200bp 以上","2y":"FY2027 non-GAAP EPS 不低於 8.10（指引下緣），各季調整後 EBITDA 利益率不低於 Q3 2026 的 20.1%","5y":null,"10y":null,"threshold":"2027 年各季調整後 EBITDA 利益率 ≥20.1%，全年 non-GAAP EPS ≥8.10","source":"季度財報新聞稿與法說會（N+M 占資料中心比重由 CEO 口頭揭露）","drift_rule":"兩年期：近四季獲利較指引路徑連兩季偏離 5% 以上視為削弱，連三季偏離 10% 以上視為反轉"},{"id":"H2","text":"國防與航太訂單續強：專案 backlog 不低於 20 億美元、訂單出貨比不低於 1.0；向上整合（Epiq、Ophir）讓高毛利長週期營收占比上升","2y":null,"5y":"FY2030 A&D 營收維持雙位數年增，backlog 持續高於 20 億美元","10y":null,"threshold":"A&D 訂單出貨比四季平均 ≥1.0，且專案 backlog ≥20 億美元","source":"季度法說會","drift_rule":"五年期：連四季偏離 5% 以上視為削弱，連六季偏離 10% 以上視為反轉"},{"id":"H3","text":"大型併購告一段落，2027 年自由現金流轉正並開始還債：Ophir 交割時淨槓桿低於 2 倍，2027 年底降到 1.5 倍以下","2y":"FY2027 自由現金流大於零；2027 年底淨槓桿 ≤1.5 倍；2027 年內沒有新的 3 億美元以上併購","5y":null,"10y":null,"threshold":"FY2027 自由現金流 >0，且 2027 年底淨槓桿 ≤1.5 倍","source":"10-Q、10-K 與法說會","drift_rule":"兩年期：自由現金流或槓桿連兩季偏離目標路徑視為削弱，連三季視為反轉"}],"R":[{"id":"R1","text":"資料中心專案時程與客戶集中：三個 N+M 大專案有一個延後，Q3 資料中心低於前季指引約 10%，Q4 N+M 約為前季說法一半；前十大客戶占 55%","h_ref":"H1","clock":"⚡","threshold":"資料中心營收連兩季低於公司指引 10% 以上","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","supply_demand_durability#5"]},{"id":"R2","text":"中國與台灣同業 2026–2030 年擴產潮，2028 年起高階板價格與稼動率回落，重演 2009、2019 年的毛利下滑但幅度更大","h_ref":"H1","clock":"🔥","threshold":"non-GAAP 毛利率連兩季年減","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#4","substitute_technology#0","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R3","text":"舉債併購：Epiq 11 億、Ophir 6.5 億，靠 6.75% 票據與 11 億定期貸款支應，利息每季多約 2,000 萬美元；併購報酬未證","h_ref":"H3","clock":"🔥","threshold":"Ophir 交割後淨槓桿高於 2 倍，或 2027 年再宣布 3 億美元以上併購","evidence_refs":["major_events#1","ma_merger#1"]},{"id":"R4","text":"地緣與關稅：約一半營收來自美國以外，中國是主要製造據點；美中都把 PCB 列入關稅，部分元件為有限或單一來源","h_ref":"H1","clock":"🐢","threshold":"毛利率單季季減逾 150bp，且管理層歸因關稅或出口限制","evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","geo_supply_chain#1"]}],"single_thing":{"description":"主要 AI 客戶在 2027 年削減或轉單 N+M 專案，使資料中心單季營收季減逾 20%","why_fatal":"資料中心約占 Q4 營收 49%，兩大客戶占 FY25 營收 23%；N+M 毛利遠高於公司平均，2027 年 EPS 由約 5 美元升到 8 美元以上，主要靠它","if_happens":"2027 年 EPS 落到指引下緣以下，市場改用週期谷底倍數定價，股價可能再跌三到五成","how_monitor":"每季資料中心營收對指引、CEO 揭露的 N+M 占資料中心比重、10-K／10-Q 客戶與應收集中度","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":9.61,"peg_fy2":0.47,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.68,"FY2026E":4.96,"FY2027E":8.34,"FY2028E":10.06},"fy_end_month":12,"eps_basis":"基期 FY2025A 為 GAAP 稀釋 EPS（事實表年度財報；non-GAAP 基期未涵蓋）；FY2026E–FY2028E 為 Koyfin non-GAAP 共識，口徑不一致，共識成長率以 FY26→FY28 兩年計"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TTMI_20261025/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"需求量循環：AI 資料中心建置帶動高層數板量價齊升，國防長約與向上整合（射頻、光學次系統）部分抵銷週期"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉。依據：多方產業來源指 AI 用 PCB 與上游玻纖布、覆銅板吃緊延續到 2027–2028 年，中國綠地建廠 13–15 個月，新產能 2027 年底至 2029 年分批開出；中國逾 20 家同業 2026 上半年宣布擴產。","bargaining":{"up":"上游覆銅板與玻纖布吃緊，Kingboard 2026 年已漲價八次，部分元件為有限或單一來源；公司稱交期 12–24 週，目前漲價由客戶吸收。","down":"FY25 前五大 OEM 客戶占 44%、前十大占 55%、兩家合計 23%，一家占應收 14% 且不要求擔保；資料中心客戶每個專案都有多家供應商。","geo":"約一半淨銷售來自美國以外的營運，中國廠是 N+M 主要產能；美中兩國都把 PCB 列入進口關稅；歐洲與以色列、羅馬尼亞透過併購擴點。"},"profit_pool_dir":"利潤池往高層數 AI 板與上游材料端移動（材料商連續漲價）；營業利益池五年變化事實表未涵蓋。","tam_table":[{"item":"資料中心與網通可服務市場","value":"約 100 億美元，TTM 市占約 9%（2026-05-27 投資人日 Soder；CFO 稱此為回頭看的數字）"},{"item":"N+M 長期營收機會","value":"約 45 億美元（投資人日 Soder）；2027 年 N+M 預計占資料中心營收約 50%（Q3 法說 CEO）"},{"item":"超大型雲端業者 PCB 供應份額","value":"2025 年 10–15%，2026 年預期超過 15%（第三方 Substack 估計，非公司揭露）"},{"item":"A&D 合格潛在商機","value":"逾 70 億美元（2026-08-05 Q2 法說 CEO）；專案 backlog 20 億美元"},{"item":"利潤池五年流向","value":"事實表未涵蓋"}]},"moat":{"mechanism":"美國本土高階 PCB 產能，加上國防受限專案資格（認證、安全許可、重新認證週期長）與 N+M 不對稱板的製程良率領先；商用段屬先行者優勢，無專利保護","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：N+M 良率優於預期，Q3 調整後 EBITDA 利益率 20.1% 年增 400bp，A&D 訂單出貨比約 1.6，backlog 20 億美元創新高，受限專案黏著度高。定價面持穩：Kingboard 年內八次漲價由客戶吸收，但第三方指客戶集中使定價權有限；TTM 營業利益率約 9.9%（近四季），遠低於台灣高階同業約 26%。中國同業 2027 年起的新產能可能削弱商用段。","threats":[{"level":"🔴","text":"中國與台灣同業 2026–2030 年大舉擴產：勝宏 2026 Q1 資本支出約 36 億人民幣（去年同期 7.3 億），臻鼎 2026 年資本支出逾新台幣 800 億、13 座新廠興建中。2027–2029 年產能開出後，高階板價格與稼動率可能回落","p":"35%","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#1"]},{"level":"🟡","text":"Sanmina 擴充高階 PCB 產能（AI、航太國防），以三大洲製造足跡挑戰 TTM 歐洲擴張；Amphenol 透過併購強化高速電子","p":"30%","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#4"]},{"level":"🟡","text":"PCB 產業高度分散且變化快，製程技術多無重大專利保護；玻璃基板與共封裝光學可能帶來新進入者，但目前尚無量產時程","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×周轉率未知（近四季營業利益率約 9.9%，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是超大型雲端業者與國防主承包商，三角色都成立。AI 加速器要更高層數與 N+M 板，屬「需要」；但需求屬建置期，CEO 在投資人日自承 AI 浪潮終將下滑、時點不知。急迫性高，持久性未證。國防端有預算順風且 2027 年約 65% 營收已有能見度。"},{"item":"決策層級","level":"🟡","text":"決策單位是單一專案、單一世代。國防受限專案的重新認證週期長、難替換，CEO 稱美國部分國防產品有時是唯一供應商。資料中心客戶每個專案都有多家供應商，Q3 法說 CEO 也說每家都得在同一技術窗口，換代時份額會重新分配。"},{"item":"價值鏈分配","level":"🟡","text":"上游覆銅板與玻纖布吃緊、連續漲價，目前能轉嫁；下游客戶高度集中。台灣高階同業的利益率遠高於 TTM，表示這條價值鏈裡 TTM 不是拿得最多的環節。一旦 2027 年後供給放鬆，價值可能回流給客戶。"},{"item":"社會容忍度","level":"🟢","text":"產品是企業與政府採購的中間財，沒有消費者端的漲價政治壓力。國防部分合約受認證成本與定價規範、多以固定價格投標（投資人日 Gridley、Fortier），這限制的是利潤上限，不構成政策風險。"}],"roiic":"事實表未涵蓋投入資本與增量投入資本，無法計算已實現增量 ROIC。投資人日 CFO 稱 N+M 4.5 億美元資本支出對應約 45 億美元營收機會（約 10 倍），並說明這不是全部資本支出的基準；這是管理層預期，不是已實現數字","reinvest_rate":"高於 100% 的稅後營業利益：近四季自由現金流利潤率約 −0.45%（資本支出大於營業現金流）。2026 年資本支出約 3–3.2 億美元（投資人日），Q2 再上調約 4,500 萬；2025–2029 年承諾逾 13 億，另加 4 億 N+M 擴產；同期以 11 億現金收購 Epiq、6.5 億收購 Ophir（待交割）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。再投資率輸入（資本支出、折舊、營運資金變動、收購淨額）只有部分在逐字稿，增量投入資本不在事實表，因此天花板留空，不以推估補數字"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","TTMI":21.19,"SANM":9.01,"2368.TW":34.69,"3037.TW":19.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","TTMI":9.94,"SANM":5.49,"2368.TW":26.05,"3037.TW":10.24,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","TTMI":-0.45,"SANM":4.66,"2368.TW":0.64,"3037.TW":-0.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","TTMI":0.88,"SANM":0.26,"2368.TW":1.87,"3037.TW":3.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"SANM","gm":9.01,"om":5.49,"fcf_margin":4.66,"rd_intensity":0.26,"strategy_note":"EMS 為主、利潤率比 TTM 低一截，但正在擴充 AI 與國防用高階 PCB 產能，並以北美、歐洲、亞洲製造足跡直接挑戰 TTM 的歐洲擴張","period":"TTM ending 2026-06-30（4季加總）"},{"name":"2368.TW","gm":34.69,"om":26.05,"fcf_margin":0.64,"rd_intensity":1.87,"strategy_note":"台灣高階板同業，毛利率與營業利益率都明顯高於 TTM，是 AI 伺服器板最強的報酬標竿；TTM 對它的報酬差為負","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3037.TW","gm":19.85,"om":10.24,"fcf_margin":-0.4,"rd_intensity":3.92,"strategy_note":"台灣載板與 PCB 大廠，利潤率與 TTM 相近、近四季自由現金流同樣為負，反映整個產業都處在擴產吃現金的階段","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（N+M 與高層數板、A&D 訂單）＋價（N+M 單價約傳統板 4 倍、材料漲價轉嫁）＋併購（2027 年約 5 億美元營收）；無回購","runway_years":"約 3–5 年","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋投入資本與增量投入資本，內生天花板無法計算。共識 FY26→FY28 EPS 年化約 42%，缺口部分歸因於 N+M 組合帶來的利益率擴張與收購，其餘無法歸因、依賴重新評價，長期信心上限為中","segments":[{"item":"資料中心與網通","value":"Q3 占 41%、年增 115%；Q4 預估占約 49%（約 6.7–7 億美元），N+M 約占三成，2027 年升到約五成"},{"item":"航太國防","value":"Q3 占 34%、年增 21%；backlog 20 億美元、訂單出貨比約 1.6；Q4 預估占約 31%"},{"item":"醫療工業儀器","value":"Q3 占 18%、年增 97%（含調價與 AI 車用測試設備需求）；Q4 預估占約 14%"},{"item":"車用","value":"Q3 占 7%、年增 11%；全年由原估中個位數衰退改為中個位數成長"}],"decay_signals":["EPS 成長顯著高於營收成長：共識 FY26→FY27 EPS 約 +68%，營收約 +47%，差距超過 5pp，亮","FCF 對淨利低於 0.75：FY25 自由現金流約為零、淨利 1.77 億；FY24 約 0.91，只有一年未達、未連兩年，暫不亮，列監測","毛利率連兩季年減：未亮（Q3 non-GAAP 毛利率年增 330bp）","核心市占縮減：未亮（第三方估超大型雲端業者份額上升）","SBC 占營收逾 5%：未亮（Q3 約 2.0%）","維護性資本支出占 FCF 逾 60%：事實表未涵蓋"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"股息","value":"事實表未涵蓋；法說會未提股息政策"},{"item":"回購","value":"證據包未見；CFO 說明 2027 年現金優先用於資本支出與還債"},{"item":"併購支出","value":"Epiq 11 億美元現金（2026-09-30 完成）、Ophir 6.5 億美元（預計 2027Q2）、STG 已完成、ILFA 接近完成、英國 Merlin 旗下兩家小廠"},{"item":"資本支出承諾","value":"2025–2029 年逾 13 億美元，另加 4 億 N+M 擴產（2026Q4 至 2028 初）"},{"item":"融資","value":"5 億美元 6.75% 2034 年票據＋3 億 TLA＋8 億 TLB；Q4 利息支出指引約 3,390 萬美元"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Epiq 9/30 才完成、Ophir 待交割，已實現增量報酬無數據；過往併購報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"證據包未見回購；稀釋股數逐年上升","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數 FY26 約 1.075 億、FY27 約 1.081 億，年稀釋約 0.6%，低於 1.5%；Q3 SBC 占營收 2.0%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY26／FY27 共識 non-GAAP EPS）","tier":"美國高階 PCB 與國防電子","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業前瞻本益比，無法做倍數對照；終端倍數改以自身前瞻與 trailing 倍數為錨"},"fwd_pe":16.15,"peg":0.38,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"數字上便宜（FY26 16.2 倍、FY27 約 9.6 倍）；但 trailing P/S 與 EV/S 落在自身年度端點八成以上分位，分母是 AI 建置高峰獲利，淨負債可能低估約 17.5 億美元的新增債務與待付併購款，所以結論給黃，不給綠","upside_short_pct":24,"upside_mid_pct":67},"trap_analysis":{"verdict":"🟡","label":"高峰獲利期的低本益比可能是陷阱；FCF 薄、舉債併購"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"中國逾 20 家 PCB 廠 2026 上半年宣布擴產，勝宏 Q1 資本支出約 36 億人民幣，臻鼎 13 座新廠興建中、產能 2026–2030 年分批開出；第三方整理指資料中心建置若放緩，Penang 與 Syracuse 擴產的稼動率與毛利有風險；過去下行期毛利率 2009 年由 20.2% 降到 17.7%，2019 年由 16.1% 降到 14.9%","assumption":"Base 假設 2029 年 EPS 只小幅回落、毛利結構大致守住","consequence":"若 N+M 在 2028 年被中國產能削價，資料中心利益率退回傳統板水準，EPS 可能回到 4–5 美元，股價約 50 美元，五年虧約四成","ruling":"採納：Bear 機率給 35%，高於一般的 25–30%；同時列入毛利率年減的減碼門檻","watch":"non-GAAP 毛利率年增減、中國同業高階板報價、超大型雲端業者資本支出指引","evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","supply_demand_durability#5"],"fact_refs":["f_kpi1_non_gaap"]},{"view":"論點失敗","evidence":"FY25 前十大客戶占 55%（2024 年 42%），兩家合計 23%，一家占應收 14% 且不要求擔保；Q3 資料中心比前季占比指引低約 10%，Q4 N+M 約為前季說法的一半，管理層歸因一家客戶專案延後","assumption":"三個 N+M 大專案在 2027 年都正常放量","consequence":"一家主要 AI 客戶削減或轉單，2027 年 EPS 成長的最大來源就會斷掉","ruling":"採納：列為唯一致命點，並設資料中心連兩季低於指引的減碼門檻","watch":"季度資料中心營收對指引、N+M 占資料中心比重、應收集中度","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"],"fact_refs":["f_kpi10"]},{"view":"論點成功但股東經濟變差","evidence":"8 月起以 5 億美元 6.75% 票據加 11 億定期貸款完成 Epiq 收購，另以現金加循環信貸付 Ophir 6.5 億；CFO 稱利息每季增加約 2,000 萬美元；資本支出承諾逾 16 億；FY25 自由現金流約為零","assumption":"N+M 與國防都成功，獲利就會留給股東","consequence":"營運成功的果實被高價併購、利息與持續擴產吃掉，每股自由現金流長期偏薄，股東報酬落後獲利成長","ruling":"採納：併購已實現報酬沒有數據，資本配置不給高分，長期信心上限為中","watch":"2027 年自由現金流、Ophir 交割後淨槓桿、是否再宣布大型併購","evidence_refs":["major_events#1","ma_merger#1"],"fact_refs":["f_kpi3_fcf","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"賣方雖然都給買進，Needham 已於 2026-09-21 把目標價由 220 降到 175；trailing P/S 與 EV/S 仍在自身年度端點八成以上分位；FY1 共識三個月上修約 23%，週期股在上修高峰時本益比往往最低","assumption":"16 倍前瞻、9.6 倍 FY27 已經夠便宜","consequence":"若市場改用週期中位獲利來定價，即使 2027 年兌現，股價也可能停在原地","ruling":"部分反駁：前瞻倍數已由前份的 25–30 倍以上降到約 16 倍，價格已經消化很大一塊週期風險；但用銷售倍數看仍在自身區間上緣，不構成安全邊際，所以不追","watch":"FY27 共識是否開始下修、P/S 是否回到自身區間中位","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-58,"hi":-38,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 167.35 → 本次 80.11（-52.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=167.35","side_b":"本次 price_at_dd=80.11","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 167.35 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 167.35 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 167.35 美元：Bull 價 217.5、Bear 價 50，五年期望值 −27.5%，基準年化 −4.4%，不對稱比 0.24","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.24。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 167.35 美元：五年期望值 −27.5%，基準年化 −4.4%，不對稱比 0.24","side_b":"本次情境、股價 80.11 美元：五年期望值 +51.4%，基準年化 10.8%，不對稱比 2.61","ruling":"再換股價、情境不動：起點價下跌 52.1%，五年期望值多 78.9 個百分點，基準年化多 15.2 個百分點，不對稱比由 0.24 升到 2.61。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與機率（前份漂移）","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-05-18：股價 167.35，前瞻本益比約 25–30 倍以上，估值結論黃；前份第三條假設要求前瞻本益比守住 20 倍、股價落在 90–180 美元","side_b":"本次股價 80.11，FY26 前瞻約 16.2 倍、FY27 約 9.6 倍；前份第三條假設已破（倍數與股價雙雙跌破下限）","ruling":"股價腰斬是倍數壓縮，不是獲利下修（FY1 共識三個月上修約 23%）。估值結論維持黃，因為便宜建立在 AI 建置高峰的獲利上，分母本身就是爭點。情境機率與回撤範圍按本次股價重估：Bear 35%，回撤 −38% 到 −58%","evidence_level":"事實表股價、共識與倍數","settle_metric":"2027 年各季 non-GAAP EPS 是否守住指引下緣 8.10 的年化路徑","if_then":["若 Q4 財報資料中心營收達約 6.7 億美元且第三個 N+M 專案量產，重跑研究考慮小倉位試單","若資料中心營收連兩季低於指引 10% 以上，維持不買，已持有者減碼"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"品質與陷阱評等（前份漂移）","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份品質評等 B、價值陷阱風險黃","side_b":"本次品質評等 B、價值陷阱風險黃，但理由換了。品質一側：Q3 紀錄獲利（non-GAAP 營益率 17.4%）與訂單出貨比 2.13。陷阱一側：FY25 自由現金流約為零、EPS 成長遠快於營收、舉債併購讓利息每季多約 2,000 萬美元","ruling":"評等不變，組成換了：營運面變好、資產負債表變差，兩者抵銷","evidence_level":"財報新聞稿、法說會、8-K","settle_metric":"FY2027 自由現金流與淨槓桿","if_then":["若 2027 年自由現金流轉正且淨槓桿降到 1.5 倍以下，陷阱評等降為綠","若 2027 上半年自由現金流仍為負，陷阱評等升為紅"],"evidence_refs":["major_events#1","ma_merger#1"]},{"axis":"新增欄位（前份漂移）","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份為舊格式，護城河趨勢、五年後跑道、公司類型、週期位置與定期定額結論皆未填","side_b":"本次護城河趨勢持穩、五年後跑道黃、類型循環與商品、週期位置中循環；定期定額結論本流程不產出","ruling":"首次填寫，不代表判斷翻轉","evidence_level":"流程改版","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"行動門檻（重啟、減碼、清倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件，也沒有清倉或減碼門檻（兩欄皆空白）","side_b":"本次重啟：Q4 財報資料中心營收約 6.7 億美元、第三個 N+M 專案量產、FY26 自由現金流轉正。減碼：資料中心營收連兩季低於指引 10% 以上，或 non-GAAP 毛利率連兩季年減。清倉：主要 AI 客戶削減 N+M 下單，資料中心單季營收季減逾 20%","ruling":"新增門檻都來自本季新證據：Q3 資料中心比前季指引低約 10%，Q4 N+M 金額約為前季說法的一半，公司又已舉債併購","evidence_level":"法說會逐字稿、8-K","settle_metric":"Q4 2026 資料中心營收與 N+M 占比","if_then":["若 Q4 達成重啟三條件，重跑研究","若 Q4 資料中心營收再低於指引 10% 以上，維持不買"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（Single Thing 空白）","side_b":"主要 AI 客戶在 2027 年削減或轉單 N+M 專案，使資料中心單季營收季減逾 20%","ruling":"新設。資料中心約占 Q4 營收 49%，兩大客戶占 FY25 營收 23%，N+M 毛利遠高於公司平均，是 2027 年 EPS 成長最大的單一敏感項","evidence_level":"10-K 客戶集中度、法說會","settle_metric":"季度資料中心營收","if_then":["若發生，清倉","若 2027 上半年 N+M 占資料中心比重升向 50%，下調此風險機率"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"axis":"風險門檻改寫","cause":"新證據","prior_field":["R1","R2","R3"],"side_a":"前份：FY27 資本支出指引超過 3.5 億美元；A&D backlog 季減；前瞻本益比超過 40 倍，或半年內部人賣股逾 2,000 萬美元","side_b":"本次：資料中心營收連兩季低於指引 10%（減碼）；non-GAAP 毛利率連兩季年減（減碼）；Ophir 交割後淨槓桿高於 2 倍（減碼）；關稅使毛利率單季降逾 150bp","ruling":"舊門檻失效。資本支出已承諾 2025–2029 年逾 13 億再加 4 億，3.5 億門檻沒有鑑別力；前瞻本益比已降到約 16 倍，40 倍門檻沒有意義；A&D backlog 創新高 20 億。風險重心移到資料中心專案時程、中國新產能與舉債","evidence_level":"法說會、8-K","settle_metric":"季度資料中心營收、毛利率、淨槓桿","if_then":["若三條減碼門檻任兩條同時亮起，已持有者減碼一半"],"evidence_refs":["cyclical_supply_discipline_capacity#2","major_events#1"]},{"axis":"N+M 放量規模：管理層前後說法","cause":"新證據","prior_field":null,"side_a":"2026-08-05 Q2 法說 CFO：下半年 N+M 約 6 億美元，三分之一在 Q3、三分之二在 Q4（Q4 約 4 億）；同場 CEO 指引 Q3 資料中心占營收 49%","side_b":"2026-10-22 Q3 法說 CEO：Q3 資料中心占 41%；Q4 N+M 約占資料中心 30–32%，資料中心約 6.7–7 億美元，換算 N+M 約 2.1 億，CEO 卻又說「略低於 4 億」","ruling":"不可調和，兩組數字不能同時成立。採百分比口徑，因為 CEO 兩次回答都給出約三成占比與 6.7–7 億的資料中心金額，換算 Q4 N+M 約為前季說法的一半。公司把落差歸因於一家客戶專案時程延後：未證，列監測；若 Q1 2027 第三個專案仍未全面量產，視為歸因不成立","evidence_level":"兩場法說逐字稿","settle_metric":"Q4 2026 財報揭露的 N+M 營收或占比","if_then":["若 Q4 實際 N+M 接近 4 億美元，撤回本條並上調第一條假設的信心","若 Q1 2027 第三個 N+M 專案仍未全面量產，不買，已持有者減碼至半倉"],"evidence_refs":["customer_concentration_credit#1"]},{"axis":"併購規模：投資人日說法與實際","cause":"新證據","prior_field":null,"side_a":"2026-05-27 投資人日 CFO：地理擴張與小型策略併購機會，擴大的借款額度主要用於併購","side_b":"8 月起宣布或完成 Epiq 11 億美元現金收購、Ophir 6.5 億美元（待 2027Q2）、STG、ILFA 與英國兩家小廠；Q3 法說 CFO 稱大型併購到此告一段落","ruling":"採實際行為這一側：四個月內併購金額約占市值兩成，資金靠 6.75% 票據與 11 億定期貸款。併購已實現報酬沒有數據，資本配置不給高分","evidence_level":"8-K、逐字稿","settle_metric":"2027 年淨槓桿與 Epiq 營收貢獻","if_then":["若 2027 年再宣布 3 億美元以上併購，減碼","若 2027 年底淨槓桿降到 1.5 倍以下且自由現金流轉正，上調資本配置評價"],"evidence_refs":["major_events#1","ma_merger#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：中國逾 20 家 PCB 廠 2026 上半年宣布擴產，勝宏 Q1 資本支出約 36 億人民幣，臻鼎 13 座新廠興建中，產能 2026–2030 年分批開出","side_b":"結構轉好：多方來源指 AI 板與上游材料吃緊延續到 2027–2028 年，玻纖布新產能 2027 年後才到位，客戶要求中國以外的產能。其他結構變數：美中都把 PCB 列入關稅，約一半營收來自美國以外","ruling":"雙向拉鋸：2027 年以前結構性吃緊占上風，2028 年起新產能開出後，競爭惡化可能翻轉優勢","evidence_level":"產業新聞與 10-K","settle_metric":"中國同業高階板報價與稼動率、TTM 毛利率年增減","if_then":["若 2027 下半年 non-GAAP 毛利率轉為年減，判定競爭惡化占上風，不買"],"evidence_refs":["cyclical_supply_discipline_capacity#3","reg_tariff_export#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY27 公司指引 EPS 8.10–8.90，現價約 9.6 倍。訂單出貨比 2.13；90 天 backlog 13 億美元，年增 111%；A&D backlog 20 億，2027 年 A&D 營收約 65% 已有能見度。賣方平均目標價約為現價兩倍，股價仍在 104 週均線之上","side_b":"便宜靠的是高峰獲利；Q4 N+M 規模約只有前季說法一半；舉債併購與 16 億資本支出承諾都在週期中段加碼；近四季自由現金流為負","ruling":"不追。2027 年能見度足以支撐「不賣」，不足以支撐在 N+M 規模與資產負債表釐清之前建倉；等 Q4 財報這個具名事件","evidence_level":"財報、法說會、賣方目標價","settle_metric":"Q4 2026 財報（2027-02）","if_then":["若 Q4 達成重啟條件，重跑研究","若股價先漲但證據未到，不追","若股價下跌但重啟條件成立，分批反買"],"evidence_refs":["capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"Q4 財報確認 N+M 放量與現金轉正，才重啟研究","type":"估值rearm","maps_to":"H1","metric":"Q4 2026 資料中心營收、第三個 N+M 專案量產狀態、FY26 自由現金流","threshold":"資料中心營收約 6.7 億美元以上、第三個 N+M 專案進入量產、FY26 自由現金流大於零","action":"重跑完整研究，成立才以小倉位試單","source_freq":"季報與法說會","date":"2027-02","evidence_refs":[]},{"n":2,"text":"2027 年 N+M 組合推升利益率","type":"假設驗證","maps_to":"H1","metric":"調整後 EBITDA 利益率、non-GAAP EPS","threshold":"2027 年各季調整後 EBITDA 利益率不低於 20.1%，全年 non-GAAP EPS 不低於 8.10","action":"未達則下調 Base 路徑、不加碼","source_freq":"每季","date":null,"evidence_refs":[]},{"n":3,"text":"資料中心營收再度低於公司指引","type":"減碼","maps_to":"R1","metric":"資料中心營收相對公司當季指引口徑","threshold":"連兩季低於指引 10% 以上（Q3 已低約 10%）","action":"不買，已持有者減碼一半","source_freq":"每季","date":"2027-05","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","supply_demand_durability#5"]},{"n":4,"text":"中國新產能開出後毛利率轉弱","type":"風險","maps_to":"R2","metric":"non-GAAP 毛利率年增減","threshold":"連兩季年減（基準 Q3 2026 為 24.8%）","action":"減碼","source_freq":"每季","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3","competitive_share_entrants#1","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"n":5,"text":"主要 AI 客戶削減或轉單 N+M","type":"Single Thing","maps_to":"R1","metric":"資料中心單季營收季增減","threshold":"單季季減逾 20%，且管理層歸因客戶下單減少","action":"清倉","source_freq":"每季","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":6,"text":"舉債併購後槓桿降不下來","type":"風險","maps_to":"R3","metric":"淨負債對近 12 個月調整後 EBITDA","threshold":"Ophir 交割後高於 2 倍，或 2027 年底未降到 1.5 倍以下，或再宣布 3 億美元以上併購","action":"減碼","source_freq":"每季","date":"2027-08","evidence_refs":["major_events#1","ma_merger#1"]},{"n":7,"text":"關稅或出口管制吃掉毛利","type":"風險","maps_to":"R4","metric":"non-GAAP 毛利率季增減與管理層歸因","threshold":"單季季減逾 150bp，且管理層歸因關稅或出口限制","action":"停止加碼","source_freq":"每季","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","geo_supply_chain#1"]},{"n":8,"text":"Q4 財報後複審","type":"複審日期","maps_to":null,"metric":"全部門檻","threshold":"Q4 2026 財報公布","action":"重跑研究","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"資料中心與網通營收相對公司指引","bear_threshold":"連兩季低於公司當季指引口徑 10% 以上","window":"2026Q4–2027Q1","source":"季度財報新聞稿與法說會","last_status":"warning"},{"metric":"non-GAAP 毛利率年增減","bear_threshold":"連兩季年減（基準 Q3 2026 為 24.8%）","window":"2027 全年","source":"季度財報新聞稿","last_status":"ok"},{"metric":"淨負債對近 12 個月調整後 EBITDA","bear_threshold":"Ophir 交割後高於 2 倍，或 2027 年底未降到 1.5 倍以下","window":"2027Q2–2027Q4","source":"10-Q 與法說會","last_status":"unknown"},{"metric":"A&D 訂單出貨比與專案 backlog","bear_threshold":"訂單出貨比連兩季低於 1.0 且 backlog 低於 18 億美元","window":"2027 全年","source":"季度法說會","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-46.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"Q4 財報（2027-02）資料中心營收約 6.7 億美元以上、第三個 N+M 專案量產、FY26 自由現金流轉正，三者同時成立","exec_line":"觀望不追。三項重啟條件同時成立才重跑研究；股價先漲但證據未到不追；股價下跌而重啟條件成立則分批反買；資料中心連兩季低於指引則維持不買。"},"reasoning":{"industry":"Q3 FY2026 營收 12.04 億美元，年增 60%，高於公司指引上緣 11.4 億。GAAP 營益率 13.5%，non-GAAP 17.4%。終端市場結構：資料中心與網通占 41%（年增 115%）、航太國防 34%（年增 21%）、醫療工業儀器 18%（年增 97%）、車用 7%。管理層預估 Q4 資料中心占比升到約 49%。訂單出貨比 2.13，A&D 專案 backlog 20 億美元創新高。Q4 指引營收 14.2–14.4 億美元；2027 年初步指引營收 65–67.5 億美元、non-GAAP EPS 8.10–8.90，其中約 5 億美元營收來自收購。產業時鐘判為擴張期：訂單仍在加速，新增供給多在 2027–2029 年才開出。供需持久性判為週期性將反轉，因為多方來源都指出吃緊只延續到 2027–2028 年，供給可逆性高。單點依賴有兩處：一是客戶集中，FY25 前十大客戶占 55%、兩家合計 23%，一家客戶占應收 14%；二是 N+M 有三個大型專案，其中一個已延後。","moat":"機制：美國本土高階產能、國防受限專案資格與 N+M 製程良率三者疊加。商用段靠的是先行者優勢，不是專利，10-K 自承製程技術通常不受重大專利保護。執行面在擴大：N+M 良率比預期好（Q2 法說），Q3 調整後 EBITDA 利益率 20.1% 創紀錄，國防受限專案難以被替換，第三方分析也稱 TTM 是美國唯一在 ASIC 領域具相當產能的 PCB 廠。定價面持穩：材料漲價能轉嫁，醫療工業儀器段有調價，但客戶集中限制議價。同業對照方面，台灣高階同業的營業利益率遠高於 TTM，TTM 對最強同業的報酬差為負，所以合併分不到 8。兩面相抵，趨勢判為持穩。最大威脅是中國同業 2026–2030 年的擴產潮。投入資本事實表未涵蓋，當期 ROIC 無法計算。","growth":"成長由三部分組成：量（N+M 與高層數板出貨、A&D 訂單）、價（N+M ASP 較高、材料漲價轉嫁）、併購（2027 年約 5 億美元營收來自收購）；沒有回購。共識 EPS FY26 4.96、FY27 8.34、FY28 10.06，兩年年化約 42%。FY25 non-GAAP 基期事實表未涵蓋，GAAP 稀釋 EPS 為 1.68，口徑不同不直接算三年 CAGR。共識營收 FY26 44.7 億、FY27 65.9 億，增約 47%，同期 EPS 增約 68%，差距來自 N+M 組合推高利益率。內生天花板因投入資本未涵蓋而無法計算。缺口歸因：毛利結構改善與收購可以說清楚一部分，剩下的無法歸因，長期信心上限為中。跑道方面，資料中心可服務市場約 100 億、市占約 9%，N+M 長期機會約 45 億；2027 年 N+M 約占資料中心一半，按此推估約 3–5 年會吃到大半機會。國防向上整合（Epiq、Ophir）是靠收購補的第二條腿，不是自己長出的下一條 S 曲線，所以五年後跑道判為中。","governance":"現金轉換弱：FY25 自由現金流約為零（淨利 1.77 億），近四季自由現金流利潤率約 −0.45%；Q3 單季回到 7,480 萬。SBC 2,410 萬，占營收 2.0%。稀釋股數 FY26 約 1.075 億、FY27 約 1.081 億，年稀釋約 0.6%。現金去向：一是資本支出（2025–2029 年承諾逾 13 億，另加 4 億）；二是併購（Epiq 11 億現金於 9/30 完成、Ophir 6.5 億待 2027Q2、STG 已完成、ILFA 將完成、英國兩家小廠）；三是無股息、無回購的證據。資金來源是 5 億美元 6.75% 2034 年到期票據，加 3 億 TLA、8 億 TLB 增貸，Q4 利息支出指引 3,390 萬美元，Q3 為 1,210 萬。淨槓桿由 Q2 的 0.9 倍升到 Ophir 交割時的「低於 2 倍」。事實表的淨負債 7.68 億是最新一季數字，可能未含 9/30 增貸與待交割的 Ophir。併購已實現的增量報酬目前沒有數據；Ophir 約 10 倍 2027 年 EBITDA 的價格，管理層自稱保守。","valuation":"前瞻本益比 16.15 倍（分母 FY1 4.96），trailing 本益比 32.0 倍，落在自身 3 個年度端點的約五成分位。trailing P/S 2.2 倍、EV/S 2.41 倍，在自身 4 個年度端點的八成以上分位。年度端點太少，不是五年分位，五年分位留空。PEG：FY26→FY28 共識 EPS 年化約 42%，16.15÷42≈0.38；但週期股在高峰期 PEG 失真，不作便宜依據。分母本身就是爭點：FY27 8.34 是 AI 建置高峰的獲利，而且淨負債可能未含 9/30 增貸 11 億與待交割 Ophir 6.5 億，EV 偏低。所以便宜論證打折，估值結論給黃。短期上行：2027 年 EPS 8.3×12 倍約 100 美元，約 +24%。中期上行用 Base 五年終點約 134 美元，約 +67%。同業前瞻本益比事實表未涵蓋，無法做倍數對照。","premortem":"股價 26 週跌 46%、RSI 33，可是同期 FY1 共識三個月上修約 23%。市場在折價的是 2028 年以後，不是 2027 年。過去下行期 TTM 毛利率 2009 年降 2.5pp、2019 年降 1.2pp，跌幅不大；但這次資料中心占營收近半、N+M 毛利遠高於平均，營運槓桿大很多。Q4 N+M 規模約只有前季說法的一半，管理層歸因客戶時程延後，未證。三視角的反證與裁定見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"TTM 賺的是 AI 資料中心客戶與美國國防主承包商的高層數印刷電路板與射頻次系統的錢。錢卡在高階產能與 N+M 良率這一節點；上游材料漲價、下游客戶集中，議價空間兩頭受擠。","moat":"→","growth":"🟡","capital":"資本配置偏激進：在獲利高峰期舉債做大型併購，同時承諾 16 億美元以上擴產，自由現金流還很薄。","valuation":"現價 80.11 美元，約為 FY26 共識 16.2 倍、FY27 約 9.6 倍。要划算，只需 2027 年獲利大致兌現，且 2028 年不腰斬。我信前一半：2027 年有訂單與指引撐。後一半要看中國新產能開出後的價格，現在無從驗證。","how_wrong":"最可能看錯的地方，是把高峰獲利當常態：2028 年中國新產能開出、AI 建置放緩時，資料中心板價格與稼動率一起回落，加上舉債併購放大損益波動。"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 Q4 2026 財報（2027-02）：資料中心營收約 6.7 億美元以上、第三個 N+M 專案量產、FY26 自由現金流轉正","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":80.11,"week26_return_pct":-46.24,"consensus_rev_3m_pct":22.77,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"便宜論證靠 FY27 共識 EPS 8.34，這是 AI 建置與材料吃緊高峰的獲利，2028 年中國新產能開出後能否守住正是爭點；另外最新一季淨負債可能未含 9/30 Epiq 交割時的 11 億定期貸款與待交割 Ophir 6.5 億"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年分終端市場指引","impact":"高","watch":"資料中心營收是否達約 6.7 億美元、N+M 占比、FY26 自由現金流"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"第三個 N+M 大專案全面量產（CEO 稱 Q4 下半爬坡、Q1 全面生產）","impact":"高","watch":"Q1 2027 法說是否確認全面量產"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"Ophir Optics 6.5 億美元收購預計交割","impact":"中","watch":"交割後淨槓桿是否低於 2 倍"},{"date":"2028-03","date_precision":"quarter","type":"capacity","event":"新增 4 億美元 N+M 擴產開始貢獻 2028 年營收","impact":"中","watch":"同期中國同業新產能開出與報價"}],"_projected_from":"v19"}
```
