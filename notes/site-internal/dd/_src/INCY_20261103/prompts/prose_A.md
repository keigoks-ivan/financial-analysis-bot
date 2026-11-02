你是 stock-analyst v20 的**散文層（prose）agent**，標的 INCY（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：INCY　日期：2026-11-03　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2198B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（430B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（999B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1721B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1366B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（918B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（854B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2305B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1275B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2399B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2198           3361-4802      3 條（2–6 內）  
s3                  8000         430           5299-7570      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4086          7640-10914      5 條（2–6 內）  
s6                 11000         918          7057-10082      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         854           1852-2646      5 條（2–6 內）  
s10                 5000        2305           1886-2695      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2399           2000-2601      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5695B；至少需散文≈39.30KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−708.4
−60%
−60
−51%
−35
−35%
−12.2
−10%
−10
−3%
−1
0%
0
0.15
0.3%
0.33
0.47
0.5
0.55
0.58
0.67
0.75
0.9%
1
1%
1.03
1.12
1.15%
1.5%
1.5
2%
2
02
2.08
2.3
2.35
2.39%
2.4
2.46
2.55
2.62
2.8
3
03
3%
3.4
3.5
3.58
4%
4
4.4
4.4%
4.5%
4.90
05
5%
5
5.4
5.80
5.8
5.9
6.0
6
6.3
6.41
6.6
7%
07
7
7.5
7.6
7.8
7.9
8
8%
8.015
8.2
8.27
8.3
8.70
8.7
8.74
8.9
8.95
9
9.06
9.1
9.2
9.8
9.9
10%
10
10.0
10.5%
11.0
11
11.2
11.3%
11.7%
12
12%
12.2%
12.3
12.5
12.7
12.87
13.1
13.2
13.30
13.4
13.5
13.6
13.61
14%
14
15%
15
15.5%
16%
16.8%
17
17.43%
18%
18
19.6
20%
21%
21
22%
22.5%
23
23%
23.4
24%
24
25%
25
26%
26
26.1%
26.12%
26.9%
29
30
30%
30.6
31
32.2
32.7
33%
33
33.2
33.23
34
35%
35
36
36%
37
38.0%
38
38%
40
40%
40.2%
45%
45
46%
47.7
49
49%
49.4
51.3
52
52.1
52.6
53.0
54%
54
55
55.2
57%
58
60%
60.7
62%
62.8
69.8
70
72%
73%
75
77.06
80%
90%
90
92.7%
96%
100
100%
104
113.6
118.97
121
127.1
128
128.48
140
155
206
232
242.5
250
302
303
708.4
890
989
2009
2010
2011
2024
2025
2026
2027
2028
2029
2030
2031
20261103
1,230
1,557.2
3,245
3,394.6
3,854.6
5,000
5,141.2
5,255
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
{"meta":{"ticker":"INCY","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Incyte Corporation"},"oneliner":"Jakafi 占 2026 年淨銷售指引約六成，美國專利 2028 年底到期。FY2027E 13.6 倍看似便宜，其實套在到期前的高峰盈餘上。Base 情境 FY2031E EPS 5.8 美元×18 倍約 104 美元，低於現價；等 XR 轉換數據出來，或股價跌到 75 美元以下再談。","thesis":{"H":[{"id":"H1","text":"除 Jakafi 外的核心業務（Opzelura、Niktimvo、Zynyz、Monjuvi，加上 2027 年起的 povorcitinib）在 2030 年達到 30 億美元以上，補上 Jakafi 到期後的大半營收缺口。","2y":"FY2027 除 Jakafi 外核心淨銷售 ≥24 億美元（2026 Q3 年化約 19.6 億）","5y":"FY2030 ≥30 億美元（管理層目標 30～40 億的下緣）","10y":null,"threshold":"2027 Q4 單季 ≥6.0 億美元；連 2 季年增不到 15% 視為削弱","source":"公司季度新聞稿（8-K Ex.99.1）的分產品淨銷售","drift_rule":"2Y 口徑：TTM 偏離門檻連 2 季 ≥5% 為削弱、連 3 季 ≥10% 為反轉；5Y 口徑：連 4 季 ≥5% 為削弱、連 6 季 ≥10% 為反轉"},{"id":"H2","text":"Jakafi XR 在學名藥上市前轉過足夠的病患，讓 Jakafi 系列 2030 年保住 2028 年水準的 20% 以上。","2y":"2027 Q4 XR 占 Jakafi 系列 ≥8%（2026 年 9 月約 3%）","5y":"2030 年 Jakafi 系列淨銷售 ≥2028 年的 20%","10y":null,"threshold":"2027 Q4 XR 占比 ≥8%；不到 5% 視為反轉","source":"季報的 XR 淨銷售；法說揭露的 XR 占比與處方集覆蓋","drift_rule":"2Y 口徑：連 2 季低於當季路徑 ≥5% 為削弱、連 3 季 ≥10% 為反轉；5Y 口徑：學名藥上市後連 4 季保留率低於 20% 為削弱、連 6 季低於 10% 為反轉"},{"id":"H3","text":"六個三期資產中，至少兩個在 2029 年底前拿到核准或正面的樞紐讀數，讓公司在 2030 年代重回成長。","2y":"povorcitinib 美國化膿性汗腺炎核准（預期 2027 Q1），且 989 一線數據足以啟動一線樞紐試驗","5y":"989 二線骨髓纖維化（EXCALIBUR-MF2）或 G12D 一線胰臟癌（DAWN-303）至少一個正面","10y":"2030 年代的總營收超過 2028 年 Jakafi 高峰年","threshold":"2029 年底前 ≥2 個核准或正面樞紐讀數","source":"公司新聞稿、FDA 決定、ASH 與 ESMO 等學會發表","drift_rule":"10Y 口徑：跨 2 個年度未達標為削弱、跨 3 個年度為反轉；任一樞紐試驗失敗，立即重算情境機率"}],"R":[{"id":"R1","text":"Jakafi 被學名藥侵蝕得比預期快：多家學名藥廠已遞申請，美國專利約 2028 年 12 月到期，而 XR 占比還只有約 3%。","h_ref":"H2","clock":"🐢","threshold":"2027 Q4 XR 占比不到 5%，或學名藥上市日早於 2028 年 12 月","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#2"]},{"id":"R2","text":"三期管線失利，或被競品壓過：大藥廠資源更多、技術變化快；胰臟癌有 pan-RAS 抑制劑 daraxonrasib，鉑抗卵巢癌已因 ADC 進展停掉 CDK2 三期。","h_ref":"H3","clock":"🐢","threshold":"989 二線骨髓纖維化或 DAWN-303 任一主要終點失敗","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0"]},{"id":"R3","text":"代工與原料藥的單一來源出事：Zynyz 肺癌補件已因 Catalent 充填廠合規問題被 FDA 退件；ruxolitinib 原料藥部分來自中國，關稅、制裁、地緣衝突都可能造成斷料。","h_ref":"H1","clock":"⚡","threshold":"Jakafi 或 Opzelura 因代工合規被退件、收到警告信或斷貨；或公司下修「至少 24 個月」的原料藥庫存政策","evidence_refs":["regulatory_antitrust#2","reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"美國藥價政策壓縮淨價：CMS 新模式、Jakafi 的 Medicaid 國際參考價協議、232 條款專利藥關稅。","h_ref":"H1","clock":"🔥","threshold":"Opzelura 美國 pro forma 淨銷售成長連 4 季落後處方需求成長 10 個百分點以上，或 Jakafi 淨銷售在 2029 年前轉為年減","evidence_refs":["major_events#2","reg_tariff_export#1"]},{"id":"R5","text":"收購花了錢卻沒換到營收：Vega 前期款 12.5 億美元（約市值 5%）全數費用化，2029 年初才有三期數據；若再做同類收購，現金與每股盈餘都會被吃掉。","h_ref":"H3","clock":"🐢","threshold":"再出現單筆前期款超過 10 億美元的臨床階段收購，且 latarcibart 三期失敗","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"Jakafi 學名藥 2029 年上市後，Jakafi 系列（含 XR）的保留率跌破管理層目標的下緣 10%。","why_fatal":"Jakafi 約占 2026 年淨銷售指引 62%，毛利率逾九成。保留率 10% 與 30% 之間差約 7 億美元營收，換算 FY2031E EPS 約 2.3 美元，是情境樹裡最大的單一敏感項，大於任何一個管線資產在 2031 年前的貢獻。","if_happens":"Base FY2031E EPS 由 5.8 美元降到約 3.5 美元，接近 Bear 路徑。已持有就清倉；未持有就放棄事件型進場，只保留 75 美元的價格條件，觸發時重跑 DD。","how_monitor":"每季追蹤 XR 的淨銷售與占比（2026 年 9 月約 3%，全年目標約 5,000 萬美元，年底處方集覆蓋預計 >80%）；2027 Q4 占比不到 5% 是先行警訊。","probability":"12–24 個月內不會定案（學名藥 2029 年才上市）。以目前約 3% 的轉換速度推估，最終跌破 10% 的機率約 35%。"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":13.61,"peg_fy2":1.12,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":6.41,"FY2026E":3.58,"FY2027E":8.74,"FY2028E":9.06},"fy_end_month":12,"eps_basis":"Koyfin 共識快照（2026-10-31），分析師家數事實表未涵蓋；FY2025A 取年報稀釋 EPS；FY2026E 含 Vega 一次性 IPR&D。三年 CAGR 用 FY2025A→FY2028E 計算，約 12.2%。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/scenario.json","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"單一大藥專利到期前、靠第二產品與管線接棒的轉型期"},"industry":{"clock_phase":"II","sd_verdict_source":"需求面結構性持久：付費需求與處方都是雙位數成長（來源：2026 Q3 法說）。供給面可逆性高：Jakafi 美國專利約 2028 年 12 月到期，多家學名藥廠已遞申請（來源：10-K FY2025、Fierce Pharma）。","bargaining":{"up":"弱：原料藥與成品多半只有一家或少數幾家合格代工，ruxolitinib 原料藥有三家合格廠、部分原料在中國；公司以至少 24 個月庫存做緩衝。","down":"中偏弱：前五大客戶約占產品營收 72%，但它們只是通路。真正壓價的是 CMS、Medicaid 與商業保險：CMS 新模式年化約占 Jakafi 毛銷售 1%，Medicaid 改採國際參考價。","geo":"Opzelura 海外約占全年銷售 20%（不含一次性 CMS 影響）；歐洲 2026 年 7 月核准中度異位性皮膚炎，德國等市場 2027 年中起給付。232 條款對專利藥課關稅，與 HHS 簽定價協議者適用 0%，公司是否適用事實表未涵蓋。"},"profit_pool_dir":"往外流：2029 年起，Jakafi 的利潤池流向學名藥與支付方；公司內部的利潤來源由 Jakafi 轉向 Opzelura、血液腫瘤新藥與三期管線。","tam_table":{"expanded":false,"reason":"事實表未涵蓋骨髓增生性腫瘤、皮膚科、腸胃道腫瘤的 TAM 與滲透率；利潤池的遷移改由分部表與情境樹裡的 Jakafi 保留率處理。"}},"moat":{"mechanism":"專利期內的單一分子壟斷（ruxolitinib：口服 Jakafi、外用 Opzelura），加上血液科與皮膚科的處方網（Opzelura 約 2 萬名處方醫師、超過 25 萬名使用者）。Jakafi 這一塊在 2028 年底後只剩 XR 劑型的轉換成本；989 等突變專一新藥是公司重建壟斷的嘗試。","execution":7,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"定價力向下：Jakafi 淨銷售 +4%，付費需求卻是 +12%，差距來自 CMS 新模式與淨價讓步；Apotex、Hikma、Sun、Granules 等已遞學名藥申請通知，美國專利約 2028 年 12 月到期。執行力向上：除 Jakafi 外核心業務 +30%，每個產品都年增。但最大利潤池的保護兩年內歸零，合併判縮減。","peer_na_reason":"事實表的同業對照只有毛利率、營益率、FCF 率與研發密度，沒有 ROIC 與投入資本，所以利差改用營益率代理。","threats":[{"level":"🔴","text":"同分子學名藥：Jakafi 美國專利約 2028 年 12 月到期，Apotex、Hikma、Sun、Granules 等已遞申請通知。到期後，藥局端可直接換成學名藥，XR 劑型是唯一緩衝。","p":"≥90%（2029 年上市的時點已知，不確定的是侵蝕有多深）","evidence_refs":["competitive_share_entrants#0","end_markets#2"]},{"level":"🟡","text":"GSK Ojjaara 等新的 JAK 抑制劑分食骨髓纖維化市場，屬點對點競爭。","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"資源更多的大藥廠可能讓公司產品過時（10-K 風險因子的一般性文字），實際落在管線上：胰臟癌有 pan-RAS 抑制劑 daraxonrasib，鉑抗卵巢癌已因 ADC 進展停掉 CDK2 三期。","p":"30%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"level":"🟡","text":"公司越來越依賴 Opzelura。Opzelura 同樣是 ruxolitinib，處方網是真的護城河，但 2026 年的淨價改善有一部分來自與 CMS 的和解，不是競爭力。","p":"30%","evidence_refs":["competitive_share_entrants#3"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，給不出數字。帳面看屬高利益率×高周轉（毛利率 92.7%、製造外包）；若把研發與收購 IPR&D 視為投入資本，則降為高利益率×低周轉。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（病患）、決策者（血液科、皮膚科醫師）、付款者（Medicare、Medicaid、商業保險）三個角色都成立。骨髓纖維化、真性紅血球增多症、移植物抗宿主病是需要、不是想要，延後治療的代價高。代理讀數：2026 Q3 Jakafi 付費需求 +12%、Opzelura 處方 +24%、新病患 +26%。要分開看的是：需求會留下，但目前的解決方案（品牌 Jakafi）2029 年起可以被同分子替代。"},{"item":"決策層級","level":"🔴","text":"替代性要在最小的決策單位看。學名藥上市後，換藥發生在藥局與藥品福利管理端，醫師不必重新決定，這一層的轉換成本近乎零。XR 劑型是把決策拉回醫師端的唯一工具，但 2026 年 9 月只占 Jakafi 系列約 3%，年底處方集覆蓋預計 >80%。Opzelura 的決策仍在醫師端（約 2 萬名處方醫師、25 萬名使用者），這一塊單看是 🟡。"},{"item":"價值鏈分配","level":"🟡","text":"專利期內，公司拿走價值鏈的大部分（毛利率 92.7%）。但支付方的份額在擴大：CMS 新模式年化約占 Jakafi 毛銷售 1%，Medicaid 改採國際參考價，Opzelura 的 Medicaid 回扣訴訟以和解收場。上游代工只有一家或少數幾家，這是供給風險，不是定價風險。"},{"item":"社會容忍度","level":"🟡","text":"高必要性加上高價格敏感度。Medicaid 國際參考價、232 條款專利藥關稅（簽定價協議者 0%），都顯示政治上限壓在經濟上限之下。公司選擇先簽協議，換取不受未來定價授權影響，並稱不影響 2026 年指引——等於付保費，代價是淨價有了天花板。優勢依賴專利授權，法源明確，到期即失效。"}],"roiic":"事實表未涵蓋投入資本與累計研發，算不出增量 ROIC。代理讀數：FY2022→FY2025 營業利益由約 5.9 億增到約 13.4 億美元（3,394.6×17.43%→5,141.2×26.12%）；但 FY2024 營益率曾掉到 2.39%（原因事實表未涵蓋），2026 年 Vega 的 12.3 億美元費用至今沒有營收，臨床階段收購的增量報酬尚未實現。","reinvest_rate":"接近 100%：TTM 研發密度 57%（含 Vega 一次性費用），現金主要流向研發與臨床階段收購。回購與股利事實表未涵蓋，算不出精確比率。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。兩個輸入都缺，天花板只能給方向：2029–2030 年因 Jakafi 到期為負，2031 年後取決於三期讀數。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","INCY":92.69,"VRTX":86.0,"REGN":84.86,"BMRN":76.12,"EXEL":96.26,"unit":"%"},{"metric":"營業利益率","INCY":11.66,"VRTX":37.95,"REGN":26.87,"BMRN":4.38,"EXEL":40.21,"unit":"%"},{"metric":"FCF 利潤率","INCY":11.31,"VRTX":30.16,"REGN":23.01,"BMRN":21.28,"EXEL":45.84,"unit":"%"},{"metric":"研發密度","INCY":57.16,"VRTX":32.09,"REGN":40.4,"BMRN":28.99,"EXEL":33.43,"unit":"%"}],"competitors":[{"name":"VRTX","gm":86.0,"om":37.95,"fcf_margin":30.16,"rd_intensity":32.09,"strategy_note":"營益率與 FCF 率都約為 INCY 的三倍，研發密度卻較低，是單一治療領域壟斷做到極致的利潤結構；INCY 的研發密度高得多，代表它還在花錢找下一個壟斷。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"REGN","gm":84.86,"om":26.87,"fcf_margin":23.01,"rd_intensity":40.4,"strategy_note":"營益率 26.9%、研發密度 40%，可當多產品自研平台的參照；INCY 要在 2029 年後回到這個營益率，至少需要兩個三期資產成功。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BMRN","gm":76.12,"om":4.38,"fcf_margin":21.28,"rd_intensity":28.99,"strategy_note":"營益率 4.4%、FCF 率卻有 21%，帳面利潤與現金落差大，跟 INCY 的 2024、2026 年一樣，不適合用當期本益比比較。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"EXEL","gm":96.26,"om":40.21,"fcf_margin":45.84,"rd_intensity":33.43,"strategy_note":"毛利率 96%、營益率 40%、FCF 率 46%，是這組同業裡最會把營收變成現金的公司。INCY 研發密度 57%（含 Vega），EXEL 是 33%：INCY 選擇把現金押在管線上，短期利潤率輸，賭的是 2030 年代。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主、價為負、併購補管線；2029 年起 Jakafi 量價同時下滑，成長全看第二產品與三期新藥。","runway_years":"約 2 年（Jakafi 專利 2028 年底到期）；第二條曲線的滲透率事實表未涵蓋，換算不出年限。","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋增量 ROIC 與再投資率。方向判斷：再投資率接近 100%（研發密度 57%，收購全數費用化），但 Vega 等臨床階段收購尚未產生營收；2029–2030 年內生成長為負，2031 年後取決於三期讀數。共識 2025–2028 年 12.2% 的成長不是再投資的成果，而是 Jakafi 到期前的最後高峰加上費用槓桿。","segments":[{"item":"Jakafi 系列（含 XR）","value":"2026 指引 32.2～32.7 億美元，約占淨銷售 62%。Q3 8.27 億（+4%）；XR 0.15 億，9 月占比約 3%。美國專利約 2028 年 12 月到期。"},{"item":"Opzelura","value":"2026 指引 11.0～11.2 億美元（含與 CMS 和解的一次性沖回約 2.46 億）。Q3 2.55 億（+36%，pro forma +21%）：美國 2.08 億、海外 0.47 億。"},{"item":"血液腫瘤（Niktimvo、Zynyz、Monjuvi 等）","value":"2026 指引 8.9～9.1 億美元；Q3 2.35 億（+38%）。"},{"item":"除 Jakafi 外核心業務合計","value":"Q3 4.90 億美元（+30%）；管理層目標 2030 年 30～40 億美元。"},{"item":"權利金與合作收入","value":"Q3 約 2.4 億美元，由總營收 1,557.2 百萬美元減產品淨銷售約 13.2 億推得；明細事實表未涵蓋。"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":null,"note":"事實表只有 TTM 毛利率 92.7%，沒有季度序列。"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"Opzelura 新病患成長約為市場兩倍，品牌外用藥新病患份額 46%。"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"Jakafi 是淨價讓步、需求 +12%，方向相反。"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"共識 FY2025A→FY2027E EPS 年化約 16.8%，營收年化約 10.5%，差 6.3 個百分點。"},{"item":"FCF/NI 低於 0.75 連 2 年","lit":false,"note":"FY2025 約 1.03；FY2024 淨利過小、比值不具意義；FY2023 約 0.75。"},{"item":"SBC/營收高於 5% 且逐年上升","lit":false,"note":"Q3 約 4.5%（69.8÷1,557.2）；趨勢事實表未涵蓋。"},{"item":"TAM 萎縮或被替代技術壓縮","lit":true,"note":"Jakafi 品牌市場 2029 年起被學名藥壓縮；鉑抗卵巢癌因 ADC 進展停掉 CDK2 三期。"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數序列。"},{"item":"維持性資本支出占 FCF 高於 60%","lit":false,"note":"沒有自有大型產能，製造外包。"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"研發與臨床投資仍在擴大。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"事實表未涵蓋近三年的回購、股利與收購金額彙總。唯一可追的大額動作是 2026 年的 Vega 收購，已放進計分與反證處理。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Vega 前期款約 12.5 億美元（現金對價約 12.7 億），2026 Q3 全數列為 IPR&D 費用，沒有營收；三期 2029 年初才讀數，已實現增量報酬為零，低於資金成本。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購金額與均價。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 69.8 百萬美元，年化約 2.8 億÷市值 242.5 億≈每年 1.15%（毛稀釋）。","grade":"過"}]},"valuation":{"basis":"前瞻本益比，分母用 FY2027E；FY2026E 含一次性 IPR&D，不採用","tier":"中型商業化生技（單一大藥到期前）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業前瞻本益比或 EV/S，做不了跨公司的倍數錨；終端倍數改為對照本身 FY2027E 的 13.6 倍。"},"fwd_pe":33.23,"peg":1.12,"percentile_5y":23.4,"val_light":"🟠","val_light_derivation":"表面便宜（FY2027E 13.6 倍，EV/S 年度端點分位 23%），但分母是 Jakafi 到期前的高峰年。換成到期後的谷底盈餘，Base 5 年價約 104 美元，低於現價，機率加權 5 年約 −3%，所以判偏貴。分位只用 4 個年度端點，不是真正的五年分位。","upside_short_pct":1.5,"upside_mid_pct":-12.2},"trap_analysis":{"verdict":"🟡","label":"到期前高峰盈餘撐出的低本益比"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Jakafi 約占 2026 年淨銷售指引 62%；美國專利約 2028 年 12 月到期，Apotex、Hikma、Sun、Granules 等已遞學名藥申請通知；XR 占比在 2026 年 9 月只有約 3%。","assumption":"多頭假設 XR 能保住 Jakafi 的 10～30%，且除 Jakafi 外核心業務在 2030 年達到 30～40 億美元。","consequence":"若保留率不到 10%、核心業務只到 26 億美元，FY2031E EPS 約 3.4 美元，5 年後股價約 58 美元（−51%）。這是 5 年後虧掉一半最可能的劇本。","ruling":"採納，列為 Bear 路徑，機率 30%。這與唯一致命點在保留率上部分重疊；要再加上管線失利，才構成完整的虧一半故事。","watch":"XR 每季占比；除 Jakafi 外核心業務每季的年增率。","not_applicable_reason":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#2"],"fact_refs":["f_kpi6_fy2026_guidance_total_ne"]},{"view":"論點成功但股東經濟變差","evidence":"Vega 前期款 12.5 億美元在 Q3 全數費用化，2029 年初才有三期數據；公司同時跑超過 10 個樞紐試驗，並說要「全額出資」；Jakafi 已與 CMS 簽 Medicaid 國際參考價協議；Opzelura 2027 年後的價格以維持為主。","assumption":"管線成功，每股盈餘就會跟著回升。","consequence":"就算 2030 年核心業務達 35 億美元，只要研發加上市費用維持在 36 億美元以上，營益率也只在 20% 上下，每股盈餘難回到 2027 年的水準。股東拿到的是更大的營收，不是更高的每股盈餘。","ruling":"部分採納。Base 已假設費用只小幅下降；Bull 要成立，營益率必須回到 30% 以上。","watch":"非 GAAP 研發加管銷費用指引占營收的比重；每筆收購的前期金額。","not_applicable_reason":null,"evidence_refs":["major_events#0","major_events#2","ma_merger#0"],"fact_refs":["f_kpi9_fy2026_guidance_non_gaap","f_kpi2_gaap_operating_income"]},{"view":"價格已反映太多","evidence":"26 週漲 22.5%，股價 118.97 美元高於 52、104、250 週均線；Investing.com 23 位分析師平均目標價 128.48 美元，上檔約 8%。FY2026E 共識上修 15.5%，但 FY2027E 只上修 0.3%、FY2028E 不動，代表市場沒有把今年的好表現延伸到到期之後。","assumption":"FY2027E 13.6 倍很便宜。","consequence":"這個便宜是假象：分母是到期前的兩個高峰年。用 FY2031E 谷底後的盈餘 5.8 美元×18 倍，只值約 104 美元。","ruling":"採納。價格偏貴，是現在不進場的主因。","watch":"股價距離 75 美元進場錨還有多遠。","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_week26_return_pct","f_price_at_dd","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"]}],"max_dd":{"lo":-60,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 118.97","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=118.97","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值：低本益比 vs 到期後的谷底盈餘","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：FY2027E 只有 13.6 倍，淨現金約 38 億美元（約市值 16%）；除 Jakafi 外核心業務 +30%，全年指引兩度上調；有六個三期資產，管理層說其中四個成功機率較高。若 989 在 CALR 突變骨髓纖維化取代 Jakafi、G12D 在胰臟癌成功，2031 年盈餘可回到 10 美元附近。","side_b":"這 13.6 倍套在 Jakafi 到期前的最後兩個高峰年。Jakafi 約占淨銷售 62%，XR 才 3%；學名藥 2029 年上市後，盈餘至少掉三成以上。三年共識只到 FY2028，看不到這一段。","ruling":"選 B 側。兩邊對 5 年盈餘的方向相反，屬不可調和。依據是公司揭露的三個數字：Jakafi 占比 62%、專利到期日、XR 占比 3%。Base FY2031E EPS 5.8 美元×18 倍約 104 美元，低於現價。卡住進場的單一條件，是價格高於到期後的 Base 價值。","evidence_level":"高：到期日、營收占比、XR 占比都來自公司揭露","settle_metric":"XR 占 Jakafi 系列的比重（每季）；除 Jakafi 外核心業務的單季淨銷售","if_then":["若 2027 Q4 XR 占比 ≥8%，且除 Jakafi 外核心業務單季 ≥6 億美元 → Base 2031 年盈餘上修到約 7 美元，重跑 DD，通過後首倉 2%","若股價先漲到 140 美元以上，而 XR 占比仍不到 5% → 不追","反向：若股價跌到 75 美元以下，而 XR 與核心業務數據沒有受損 → 重跑 DD 後分批反買，首倉 2%","若已持有，且 2027 Q4 XR 占比不到 5% → 清倉"],"evidence_refs":["end_markets#2","competitive_share_entrants#3","capital_markets_pricing#3","end_markets#0"]},{"axis":"管理層財測：年初低於共識 vs 之後兩度上調","cause":null,"prior_field":null,"side_a":"2026 年 2 月的初始淨銷售指引 47.7～49.4 億美元，低於當時共識（約 55.2 億，各來源口徑不一）；Opzelura 指引 7.5～7.9 億，低於共識的 8.015 億。","side_b":"Q2 上調到 51.3～52.6 億，Q3 再調到 52.1～53.0 億，Opzelura 調到 11.0～11.2 億。但 Q2 那次上調，大半來自與 CMS 和解的一次性沖回約 2.46 億美元。","ruling":"可調和，屬程度差異。年初指引偏保守；扣掉一次性沖回，實質上調幅度不大，Q3 的 Opzelura 與血液腫瘤上調才是真正來自需求。2027 年 2 月的指引即使低於共識，也不宜過度解讀。","evidence_level":"中：初始共識數字各來源不一致","settle_metric":"2027 全年指引與共識營收 62.8 億美元的落差","if_then":["若 2027 指引中點低於共識 5% 以上，且主因是 Jakafi 淨價 → Bear 機率提高到 35%"],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#0","capital_markets_pricing#1","supply_demand_durability#1","major_events#1"]},{"axis":"Jakafi：需求成長 vs 淨銷售成長","cause":null,"prior_field":null,"side_a":"付費需求 +12%，各適應症都在成長，由真性紅血球增多症領頭。","side_b":"淨銷售只 +4%；CFO 說 CMS 新模式年化約占毛銷售 1%；Jakafi 另與 CMS 簽了 Medicaid 國際參考價協議。","ruling":"可調和。需求與價格方向相反，但兩者都成立，約 8 個百分點的差距就是淨價讓步。這支持定價力縮減的判斷，也代表到期前兩年的 Jakafi 營收不會像需求那樣成長。","evidence_level":"高：公司揭露","settle_metric":"Jakafi 淨銷售年增率減付費需求年增率","if_then":["若差距連 2 季擴大到 15 個百分點以上 → Base FY2027–2028 盈餘下修 5%"],"evidence_refs":["supply_demand_durability#0","major_events#2"]},{"axis":"管理層承諾與執行（新舊法說對照）","cause":null,"prior_field":null,"side_a":"2009-05-07 法說，當時的 CEO 說骨髓纖維化新藥將在「2010 年底或 2011 年初送件」，CFO 說可轉債是重大的財務壓力。本包沒有收錄這些承諾的結果。","side_b":"2026-10-29 法說，Pablo Cagnoni 說 axatilimab 併用 ruxolitinib 的一線移植物抗宿主病數據由 2026 Q4 延到 2027 Q1，理由是要在最相關的學會完整發表；CDK2 鉑抗卵巢癌三期停止收案；William Meury 說「還不能宣告勝利」。","ruling":"可調和。2009 年的場次距今 17 年，結果也未收錄，不拿來評現任團隊。現任團隊的延遲屬發表時點與競爭格局的調整，不是療效或安全問題；但同時跑超過 10 個樞紐試驗，執行風險管理層自己也承認。","evidence_level":"低：舊承諾沒有結果可對照","settle_metric":"EXCALIBUR-MF2 是否在 2026 年底前啟動；DAWN-302 是否在 2027 上半年啟動","if_then":["若兩者任一延後超過兩季 → H3 信心下調，Bull 機率降到 20%"],"evidence_refs":["regulatory_antitrust#2"]},{"axis":"Opzelura：處方網護城河 vs 法規帶來的淨價","cause":null,"prior_field":null,"side_a":"William Meury：約 2 萬名處方醫師、超過 25 萬人在用，「這就是護城河」；新病患成長約為市場兩倍，在品牌外用藥的新病患份額 46%。","side_b":"美國 Q3 +45% 裡，有一部分是與 CMS 和解後的淨價改善（pro forma 為 +25%）；Mohamed Issa 說 pro forma 下價格是小幅負貢獻，2027 年後價格以維持為主。","ruling":"可調和。需求面的護城河是真的（處方 +24%、新病患 +26%），但 2026 年的淨價順風是一次性的法規結果，不能外推。Base 只採用需求成長，價格假設持平。","evidence_level":"中","settle_metric":"Opzelura 美國 pro forma 成長率減處方成長率","if_then":["若 pro forma 成長連 2 季低於處方成長 10 個百分點以上 → 定價力再扣 1 分"],"evidence_refs":["end_markets#3","end_markets#0","major_events#1"]}],"triggers":[{"n":1,"text":"除 Jakafi 外核心業務是否走在 2030 年 30 億美元的路徑上","type":"假設驗證","maps_to":"H1","metric":"除 Jakafi 外核心業務的單季淨銷售","threshold":"2027 Q4 ≥6.0 億美元；連 2 季年增不到 15% 視為削弱","action":"達標：Base 的 2030 年核心業務上修到 35 億美元，重跑 DD；削弱：Bear 機率提高到 35%","source_freq":"季報（每季）","date":"2028-02"},{"n":2,"text":"XR 轉換速度","type":"假設驗證","maps_to":"H2","metric":"XR 占 Jakafi 系列淨銷售的比重","threshold":"2027 Q4 ≥8%","action":"達標且股價 ≤100 美元：重跑 DD，評估首倉 2%；不到 5%：不進場","source_freq":"季報與法說（每季）","date":"2028-02"},{"n":3,"text":"學名藥上市後，Jakafi 系列保留率跌破 10%","type":"Single Thing","maps_to":"Single Thing","metric":"學名藥上市後第 4 季的 Jakafi 系列淨銷售÷上市前一季","threshold":"不到 10%","action":"已持有：清倉；未持有：放棄事件型進場，只保留 75 美元的價格條件","source_freq":"季報","date":"2030-02","evidence_refs":["end_markets#2"]},{"n":4,"text":"代工廠合規出問題或原料藥斷料","type":"風險","maps_to":"R3","metric":"FDA 退件或警告信、斷貨、原料藥庫存政策","threshold":"Jakafi 或 Opzelura 任一發生","action":"減碼一半，等第一個解決時點","source_freq":"8-K／10-Q（事件觸發）","date":null,"evidence_refs":["regulatory_antitrust#2","geo_supply_chain#0","reg_tariff_export#2"]},{"n":5,"text":"學名藥提前上市","type":"清倉","maps_to":"R1","metric":"美國 ruxolitinib 學名藥的上市日","threshold":"早於 2028 年 12 月","action":"清倉","source_freq":"10-Q 法律程序揭露（每季）","date":"2028-12","evidence_refs":["competitive_share_entrants#0","end_markets#2"]},{"n":6,"text":"價格跌到到期後價值以下","type":"估值rearm","maps_to":"Base 情境","metric":"收盤價","threshold":"≤75 美元","action":"重跑 DD，通過後首倉 ≤2%","source_freq":"每日","date":null},{"n":7,"text":"989 一線骨髓纖維化數據，以及 FDA 對複合終點的意見","type":"假設驗證","maps_to":"H3","metric":"ASH 數據；一線樞紐試驗設計（2027 年初公布）","threshold":"數據足以啟動含 989 單藥或併用 ruxolitinib 的一線三臂試驗","action":"正面：Bull 機率提高到 30%；負面：Bull 機率降到 20%","source_freq":"學會發表與公司更新","date":"2027-03"},{"n":8,"text":"三期主要終點失敗","type":"清倉","maps_to":"R2","metric":"EXCALIBUR-MF2 或 DAWN-303 的主要終點","threshold":"任一失敗","action":"清倉","source_freq":"公司新聞稿（事件觸發）","date":"2029","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"n":9,"text":"年度複審","type":"複審日期","maps_to":"全份","metric":"2026 Q4 財報與 2027 全年指引","threshold":"財報公布後","action":"重跑 DD","source_freq":"每年","date":"2027-02"}],"kill_metrics":[{"metric":"Jakafi XR 占 Jakafi 系列淨銷售的比重","bear_threshold":"2027 Q4 不到 5%（2026 年 9 月約 3%）","window":"2027 Q4 財報（2028 年 2 月）","source":"Incyte 季度新聞稿與法說","last_status":"ok"},{"metric":"除 Jakafi 外核心業務的單季淨銷售年增率","bear_threshold":"連 2 季不到 15%（2026 Q3 為 +30%）","window":"滾動 2 季","source":"Incyte 季度新聞稿（8-K Ex.99.1）","last_status":"ok"},{"metric":"Opzelura 美國 pro forma 淨銷售成長率減處方需求成長率","bear_threshold":"連 4 季 ≤−10 個百分點（2026 Q3 為 +25% 對 +24%）","window":"滾動 4 季","source":"Incyte 法說","last_status":"ok"},{"metric":"989 二線骨髓纖維化或 G12D 一線胰臟癌的樞紐試驗主要終點","bear_threshold":"任一失敗","window":"2028–2029","source":"公司新聞稿、學會發表","last_status":"unknown"},{"metric":"美國 ruxolitinib 學名藥上市日","bear_threshold":"早於 2028 年 12 月","window":"至 2028 年 12 月","source":"Incyte 10-Q／10-K 法律程序揭露","last_status":"ok"}],"evidence_dismissed":[{"ref":"customer_concentration_credit#0","reason":"這條證據量的是通路集中度，不是需求集中度。同一份 10-K 寫明產品賣給專科與零售藥局、專科經銷商和批發商，前五大客戶都是轉手商，最終處方由醫師與支付方決定。應收帳款占比由 49% 升到 54%，反映的是信用風險而非需求風險，而證據本身沒有任何呆帳或延遲付款紀錄。最大兩家的占比（21%、18%）已寫在「怎麼賺錢」的議價權段。"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":"3%","requires_critic":[],"rearm_trigger":"股價≤75 美元（以 Base 5 年價 104 美元計，年化約 7%），觸發後重跑 DD 再決定首倉","exec_line":"未持有：不追。股價 ≤75 美元，或 2027 Q4 XR 占比 ≥8% 且除 Jakafi 外核心業務單季 ≥6 億美元時，重跑 DD，首倉 ≤2%。已持有：2027 Q4 XR 占比不到 5%，或學名藥提前上市，即清倉。"},"reasoning":{"industry":"最新一季（2026 Q3）總營收 1,557.2 百萬美元，年增 14%，其中產品淨銷售約 13.2 億美元。分產品看：Jakafi 8.27 億（+4%，付費需求 +12%）；Opzelura 2.55 億（+36%，扣掉與 CMS 和解帶來的淨價改善後約 +21%）；血液腫瘤 2.35 億（+38%，其中 Niktimvo 0.67 億、Zynyz 0.58 億、Monjuvi 0.55 億）。總營收減產品淨銷售約 2.4 億美元，是權利金與合作收入。毛利：銷貨成本約占淨銷售 8%，TTM 毛利率 92.7%。營益：GAAP 營業虧損 708.4 百萬美元，主因是 Vega 收購的一次性 IPR&D 12.3 億美元；加回後本季營益率約 33%，算法是（−708.4＋1,230）÷1,557.2；FY2025 全年營益率 26.1%。2026 全年淨銷售指引 52.1～53.0 億美元，其中 Jakafi 指引 32.2～32.7 億，中點占比約 62%（3,245÷5,255）。這是集中度風險，不能當成 2029 年以後的護城河證據。單點依賴：上游 ruxolitinib 原料藥只有三家合格代工廠，部分原料來自中國；下游前五大客戶（批發商與專科藥局）約占產品營收 72%，最大兩家分別占 21% 與 18%，合計未過 40%。產業時鐘判 II（擴張），依據是慢性血液病與皮膚病的處方需求仍有雙位數成長（Jakafi 需求 +12%、Opzelura 處方 +24%）。供需持久性：需求面結構性持久；供給面可逆性高，專利一到期，同分子學名藥會一次進場。","moat":"機制：ruxolitinib 這個單一分子在專利期內的壟斷（口服 Jakafi＋外用 Opzelura），加上血液科與皮膚科的處方網。事實表沒有同業 ROIC，方向證據改用營益率代理：INCY TTM 營益率 11.7%，被 Vega 一次性費用壓低，FY2025 全年為 26.1%；同業 VRTX 38.0%、EXEL 40.2%、REGN 26.9%，對最強同業的差距是負的。執行力給 7 分：本季每個產品都年增，除 Jakafi 外核心業務 +30%，Jakafi XR 已核准上市，多個三期如期開跑；扣分在 Zynyz 肺癌補件因代工廠問題被 FDA 退件、CDK2 三期停止收案。定價力給 5 分：Jakafi 淨銷售 +4%，需求卻是 +12%，CMS 新模式與 Medicaid 國際參考價協議都在壓淨價；Opzelura 方面，管理層說 2027 年後價格以維持為主。趨勢：執行力擴大、定價力縮減，而定價力背後的專利 2028 年底歸零，所以合併判縮減。產業態勢分三條看：一是競爭惡化，Apotex、Hikma、Sun、Granules 已遞學名藥申請，GSK Ojjaara 在骨髓纖維化正面競爭；二是需求面持久，付費需求 +12%；三是法規與定價，包括 CMS 新模式、Medicaid 國際參考價、232 條款專利藥關稅。合起來的裁決是競爭惡化中。","growth":"成長組成：量為主（Jakafi 需求 +12%、Opzelura 處方 +24%）；價為負（Jakafi 淨銷售只 +4%，Opzelura pro forma 成長裡價格小幅負貢獻）；併購補的是管線，不是營收。三年共識 EPS 從 FY2025A 6.41 到 FY2028E 9.06，年化約 12.2%，算法是（9.06÷6.41）^(1/3)−1。FY2026E 3.58 含 Vega 一次性費用，不能拿來算成長。缺口歸因：共識 FY2025A→FY2027E EPS +36%，營收只 +22%，差額來自費用槓桿，加上 Jakafi 到期前最後幾年的營收，所以歸為營益率擴張，不是再投資報酬。而且共識只到 FY2028，沒有涵蓋 2029 年的到期。內生天花板：事實表缺增量 ROIC 與再投資率，給不出數字；方向上，2029–2030 年為負。本次 Base 路徑從 FY2027E 8.70 到 FY2031E 5.80，年化約 −10%。跑道：Jakafi 這條約剩 2 年；第二條曲線（povorcitinib、989、G12D、latarcibart）都還在三期或審查中。管理層自己說 2030 年除 Jakafi 外核心業務目標 30～40 億美元，也說「還不能宣告勝利」，所以 5 年後的跑道給中等，不給寬。衰退信號亮 2 個：到期壓縮 TAM、EPS 成長快於營收；其餘多半事實表未涵蓋。","governance":"FCF/NI：FY2025 約 1.03（13.30÷12.87 億），FY2023 約 0.75，FY2022 約 2.62；FY2024 淨利只有 0.33 億，比值不具比較意義。TTM FCF 利潤率 11.3%，被 Vega 的現金對價壓低。SBC：Q3 69.8 百萬美元，約占總營收 4.5%；年化約 2.8 億，占市值 242.5 億約 1.15%，低於 1.5% 門檻（這是毛稀釋，事實表沒有淨股數變化）。現金去向：期末現金與有價證券 3,854.6 百萬美元、債務約 37 百萬，淨現金約 38 億美元。2026 年最大一筆支出是 Vega 收購：現金對價約 12.7 億，另有最多 7.5 億銷售里程碑，前期款全數費用化。回購與股利事實表未涵蓋。計分三項：收購的已實現報酬不過（Vega 要到 2029 年初才有三期數據，目前報酬為零）；回購沒有資料；股權稀釋過關。","valuation":"先處理分母。FY2026E 共識 3.58 美元含 Vega 一次性 IPR&D 12.3 億美元，trailing 60.7 倍與 forward 33.2 倍都失真，所以改用 FY2027E 8.74 美元：現價 118.97 對應 13.6 倍，FY2028E 9.06 對應 13.1 倍。淨現金約 38 億美元，約占市值 16%。問題是這兩年正是 Jakafi 到期前的最後高峰，便宜的論證不成立。三個情境：Base 路徑 FY2031E EPS 5.8 美元×18 倍約 104 美元，比現價低 12%；Bull 9.8 美元×21 倍約 206 美元（+73%）；Bear 3.4 美元×17 倍約 58 美元（−51%）。機率 25/45/30 加權後，5 年報酬約 −3%。12 個月看，FY2028E Base 8.95 美元×13.5 倍約 121 美元，約 +1.5%。年度端點分位（只有 4 個點，不是真正的五年分位）：EV/S 23.4、P/S 30.6、P/E 10.0，表面偏低，但分母同樣是到期前的高峰營收。PEG 用 FY2027E 13.6 倍÷三年共識 CAGR 12.2%，約 1.12，屬合理；但這個 CAGR 只算到 FY2028，沒有涵蓋到期。賣方查核：Investing.com 23 位分析師平均目標價 128.48 美元（+8%）；MarketBeat 7 月底約 113.6，Barchart 平均 127.1、最高 155。我和賣方的分歧在框架，不在事實：賣方用到期前的盈餘給倍數，我用到期後的谷底盈餘。動能：26 週 +22.5%，RSI 54，股價高於 52、104、250 週均線，均線排列成立，但 250 週斜率只有 +0.9%。事實表未涵蓋同業前瞻本益比，終端倍數只能對照本身 FY2027E 的 13.6 倍。","premortem":"三個視角的反證與裁決都寫在反證紀錄，這裡不重寫。最大回撤範圍 −35%～−60%，依據三點：一，股價回到 250 週均線 77.06 美元約 −35%，這不需要基本面惡化，只要市場提前把 2029 年的谷底定價；二，Bear 情境終點約 −51%；三，XR 轉換失敗與三期失利同時發生時，回撤可到 −60%。事實表未涵蓋歷史最大回撤、空方報告與未決訴訟金額。法說的三條迴避紀錄都來自 2009 年場次，是 17 年前的團隊，不拿來評現任管理層。價值陷阱風險：衰退信號亮 2 個（到期壓縮 TAM、EPS 成長快於營收），判中度。"},"plain":{"six":{"how_it_makes_money":"公司賺的是血液科與皮膚科處方藥的錢。Jakafi 約占 2026 年淨銷售指引六成，利潤靠美國專利與支付方淨價這一關守住；2028 年底專利到期後，這一關就鬆開了。","moat":"護城河在縮減。最大利潤池 Jakafi 的專利保護 2028 年底到期；執行力在升、定價力在降，而新護城河（Opzelura 的處方網、突變專一抗體 989）還不夠大，接不了手。","growth":"成長跑道中等。2028 年前靠 Jakafi 的最後兩年、Opzelura 與血液腫瘤撐住；2029–2030 年 Jakafi 到期，盈餘下探；2031 年以後要看三期管線能不能接棒。","capital":"現金多、稀釋低，但錢押在臨床階段收購上，報酬還沒兌現；資本配置中等。","valuation":"現價要求 2029 年後的谷底盈餘至少約 6.6 美元，而且市場還要給 18 倍。我只信到 5.8 美元，所以價格偏貴，我不信這個定價。","how_wrong":"最可能看錯的有兩處：一是 XR 轉換和 Opzelura 比預期強，Jakafi 保留率到 30%、核心業務 2030 年過 40 億美元；二是 989 的一線數據讓公司在骨髓纖維化重建壟斷。兩者任一成立，2031 年盈餘都會回到 9 美元以上。"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2027E 13.6 倍判斷便宜，但三年共識只到 FY2028，沒有涵蓋 2029–2030 年 Jakafi 被學名藥侵蝕的那段。賣方平均目標價 128 美元，隱含到期後盈餘仍有 6.6 美元以上配 18 倍；我的 Base 只有 5.8 美元。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤75 美元；或 2027 Q4 XR 占 Jakafi 系列 ≥8%，讓 Base 盈餘上修後重算。","trap":"🟡","val":"🟠","moat":"C","moat_trend":"↓","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"轉機/特殊情境","price_at_dd":118.97,"week26_return_pct":22.48,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026E EPS 3.58 美元含 Vega 一次性 IPR&D 約 12.3 億美元（每股約 6 美元），也含 CMS 一次性沖回約 2.46 億美元；trailing 本益比同樣失真。改用 FY2027E 後，FY2027–2028E 又是到期前的高峰年，因此便宜論證無效。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"product","event":"ASH 公布 989 一線骨髓纖維化數據（約 55 名病患，含單藥與併用 ruxolitinib）","impact":"高","watch":"SVR35、TSS50 與貧血改善，能否支持一線三臂樞紐試驗"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"ruxolitinib 乳膏用於輕中度化膿性汗腺炎、povorcitinib 用於結節性癢疹的三期頂線結果","impact":"中","watch":"管理層估計化膿性汗腺炎可為 Opzelura 增加 0.5～1 億美元"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"povorcitinib 歐洲化膿性汗腺炎核准（CHMP 已給正面意見）；EXCALIBUR-MF2 啟動","impact":"中","watch":"二線骨髓纖維化三期能否如期收進第一位病患"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 Q4 財報與 2027 全年指引","impact":"高","watch":"Jakafi 指引與 XR 占比；除 Jakafi 外核心業務的指引是否 ≥24 億美元"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"povorcitinib 美國化膿性汗腺炎、Monjuvi 一線瀰漫性大 B 細胞淋巴瘤預期核准","impact":"高","watch":"povorcitinib 的標籤是否同時涵蓋用過與未用過生物製劑的兩群病患"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"axatilimab 併用 ruxolitinib 的一線慢性移植物抗宿主病二期數據","impact":"低","watch":"反應能維持多久"},{"date":"2028-12","date_precision":"month","type":"other","event":"Jakafi 美國專利約在此時到期，學名藥可上市","impact":"高","watch":"XR 占比與學名藥實際上市日"},{"date":"2029-03","date_precision":"quarter","type":"product","event":"latarcibart（類血友病）三期頂線；NEXERA-303（890 一線 MSS 大腸癌）2029 年頂線","impact":"中","watch":"Vega 收購是否開始有回報"}],"_projected_from":"v19"}
```
