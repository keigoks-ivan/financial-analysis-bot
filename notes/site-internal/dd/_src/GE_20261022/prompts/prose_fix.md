你是 stock-analyst v20 的**散文層（prose）agent**，標的 GE（2026-10-22）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：GE　日期：2026-10-22　archetype：None　前份裁決：2026-07-17　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1804B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（397B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1122B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1501B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（892B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（528B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（845B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1998B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3357B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2002B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1804           3637-5196      5 條（2–6 內）  
s3                  8000         397           5322-7603      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3515          8039-11485      5 條（2–6 內）  
s6                 11000         528          7330-10472      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         845           1858-2655      5 條（2–6 內）  
s10                 5000        1998           2101-3002      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2002           2000-2998      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4701B；至少需散文≈40.30KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70
−60%
−60
−50%
−45%
−44%
−35%
−35
−14.4%
−14%
−7.4%
−1.2%
0
$0.30
0.46
0.56
0.6%
0.6
0.7%
0.75
0.83
0.96
1%
1.0
01
1
1.3
1.5%
1.5
1.63
2
2%
2.1%
2.25
2.28
2.3%
2.6
2.7%
3
3%
3.1
3.2
3.5
4
4%
4.75
4.9%
05
5
5%
5.3%
5.4%
5.6%
6%
6
06
7
7%
07
7.39
7.4%
7.7%
7.96
08
8
8%
8.00
8.10
8.14
8.2
8.5
8.6
$8.80
9
09
9%
9.0
9.11
9.15
9.4
$9.40
9.5%
10%
10
10.3%
10.4
10.41
11
11.2%
11.55
12%
12
12.3%
12.7
13
13.7%
13.85
14
14%
14.1
14.4%
14.5
15%
16
16.4
16.6%
17%
17.7
18%
18
18.7%
18.9%
19.0%
20
20%
21%
21
22
22.5%
23%
23
24
25
25%
26
27.9%
28
28.4
28.5%
28.87
29
29.88
30
30%
31%
31.0%
31.1
31.8
32.48
32.5
34
35%
35
36%
37
37.17
37.2
38%
40
44.6
45
45%
46.5%
47.5
48
49
49%
50
52
55
60%
70
72.64
74.1%
87.04
90
91
94
95%
100
100%
102.85
104
105%
$111
117.5
130
132.85
141.18
150%
162
$162
165.57
190
$191
196.4
220
$230
232
250
$265
270.94
$280
295.88
$295.88
300
$301
$302
$305
318.55
$345.73
345.73
$350
$387.8
$397
540.75
557.6
737
777
1879
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
2035
2040
20261022
1,000
1,300
1,700
2,000
2,400
3,600
80,000
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
{"meta":{"ticker":"GE","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"GE Aerospace"},"oneliner":"航空引擎售後年金寡頭，第三季訂單 +49% 並再度上修全年財測；現價對 FY2027 共識約 32.5 倍、Base 年報酬約 7.7%，等 $265 以下或 2027 財測驗證服務成長再進場","thesis":{"H":[{"id":"H1","text":"2027 年商用服務低雙位數成長由在手訂單與已飛週期兌現，油價只延後不改變大修需求","2y":"2027 商用服務營收年增 ≥10%、備件延交開始下降","5y":null,"10y":null,"threshold":"2027 全年商用服務營收年增 ≥10%；服務訂單年增率不低於服務營收年增率","source":"公司季報新聞稿與法說會（每季）","drift_rule":"商用服務營收年增連 2 季低於 9.5%（偏離 ≥5%）為削弱；連 3 季低於 9%（偏離 ≥10%）為反轉"},{"id":"H2","text":"LEAP 由新機虧損期進入售後收割期：裝機 2025→2030 翻倍、大修年複合約 25%，LEAP 服務利益率 2028 年對齊整體服務，GE9X 虧損 2027 年後回落，CES 利益率 2028 起擴張","2y":null,"5y":"CES 營業利益率 2028 年起逐年擴張","10y":null,"threshold":"CES 營業利益率 2028 全年 ≥28.5%（2026 年第三季 27.9%）；GE9X 2028 年虧損低於 2027","source":"年報、季報分部數字、法說會","drift_rule":"CES 利益率 TTM 連 4 季低於路徑 ≥5% 為削弱；連 6 季 ≥10% 為反轉"},{"id":"H3","text":"機隊供給不足延續到 2030 年代初，加上 737MAX 與 777X 單一引擎地位，裝機年金持續十年以上；外部維修通路擴大是用 GE 零件放大產能，不是分走零件利潤","2y":null,"5y":null,"10y":"2035 年 LEAP 與 GE9X 裝機年金仍是利潤主體","threshold":"裝機基數年增維持低到中個位數；2030 年 LEAP 外部通路占比 ≤30% 且備件營收成長不低於大修量成長","source":"10-K、投資人日、IATA 與 Boeing 年度市場展望","drift_rule":"跨 2 個年度裝機或備件成長低於門檻為削弱；跨 3 個年度為反轉"}],"R":[{"id":"R1","text":"油價（布蘭特約 $111）與航空公司獲利受壓，出勤停滯，航空公司延後大修、拆舊機取零件，CFM56 退役率由 1.5–2% 回升，二手可用料壓低備件","h_ref":"H1","clock":"⚡","threshold":"商用服務訂單連 2 季年減，或 CFM56 年退役率 ≥3%","evidence_refs":["end_markets#4"]},{"id":"R2","text":"CPP 收購（117.5 億美元，約 70 億現金加新債，2027 下半年交割）壓縮回購、增量報酬未證；鑄件仍是全產業瓶頸，交割前產能改善只能靠合約","h_ref":"H2","clock":"🔥","threshold":"交割延至 2028 或被要求剝離；交割後外部客戶營收年減逾 10%","evidence_refs":["geo_supply_chain#0"]},{"id":"R3","text":"適航與合規事件佔用維修產能：GEnx 燃油熱交換器軟管適航指令（2026-08-21 生效）、Ryanair 1879 航班 CFM56 調查（2026-07-16 CEO）、GE9X 中段密封認證延後、ITAR 和解 3,600 萬美元","h_ref":"H2","clock":"🔥","threshold":"出現涉及 LEAP 或 CFM56 全機隊、要求提前拆換的適航指令；或 GE9X 認證晚於 2027-06-30","evidence_refs":["major_events#2","product_recall_warning#0","reg_tariff_export#2"]},{"id":"R4","text":"下一代窄體推進路線改變：RISE 開放式風扇面臨工程挑戰，電動與氫能長期替代；若 2030 年代中新窄體招標失守，裝機年金在 2040 年後斷層","h_ref":"H3","clock":"🐢","threshold":"空巴或波音下一代窄體宣布非 CFM 為唯一或主力引擎","evidence_refs":["substitute_technology#0"]}],"single_thing":{"description":"2027 年 1 月第四季財報給出的 2027 財測把商用服務成長下修到個位數","why_fatal":"商用服務是利潤成長主體：低雙位數成長對應約 35–40 億美元營收增量且利益率持平，是 FY2027 共識 EPS 9.11 的主要來源；降到個位數代表訂單轉換或航空公司需求出問題，EPS 與倍數會同時下修","if_happens":"不追、停止加碼；已持有者減碼一半；Bear 機率由 30% 提到 35% 並重跑","how_monitor":"每季服務訂單年增率、備件延交、CFM56 退役率、航空公司出勤；2027-01 財報","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":32.48,"peg_fy2":2.28,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":7.96,"FY2027E":9.11,"FY2028E":10.41},"fy_end_month":12,"eps_basis":"調整後（non-GAAP）EPS，Koyfin 共識快照 2026-10-21；FY2025 調整後實際值事實表未涵蓋（年度財報只有 GAAP 稀釋 EPS 8.14，含非經常項，口徑不同不填）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"裝機基數年金＋單一引擎認證寡占＋售後零件定價"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：IATA 供應鏈研究稱再平衡不早於 2030 年代初；Boeing 2026-07 展望約 2,000 架供給缺口、單走道缺口到本十年末","bargaining":{"up":"弱：鑄鍛件前置期 6–18 個月以上，優先供應商物料投入連 10 季成長才勉強跟上；CPP 收購為收回瓶頸","down":"對機身廠強（737MAX 只用 LEAP-1B、777X 只用 GE9X）；對航空公司備件強、大修工時中等（外部維修通路占比上升）","geo":"中國 COMAC 出口許可 2025-07 恢復；與歐盟、英國、日本、韓國有航太零關稅協議；Section 232 談判期至 2027-01"},"profit_pool_dir":"向引擎商與售後零件集中：機身廠 BA TTM 營益率 −7.4%，GE 18.7%，售後零件專利件業者 TDG 46.5%","tam_table":{"expanded":false,"reason":"成長來自既有裝機基數的維修年金，不是滲透率或新品類故事；TAM／SAM 與利潤池占比數字事實表未涵蓋"}},"moat":{"mechanism":"裝機基數×數十年強制維修年金；737MAX 與 777X 單一引擎、A320neo 雙源之一；售後零件為適航認證件，替換需重新認證","execution":9,"pricing":9,"grade":"A","trend":"→","trend_evidence":"執行力擴大（AOG 近零、物料投入連 10 季成長、大修週轉縮短）；定價力穩定（95% 以上備件營收在訂單、零件目錄價策略延續）；但備件延交連兩季季增、LEAP 外部通路占比 2030 年升至約 30%，抵銷部分執行力優勢，整體判穩定","threats":[{"level":"🟡","text":"雙源機型與國防新案的點對點競爭：A320neo 上的 GTF；美國空軍 ACP 無人機引擎授予四隊並明言要多供應商，新進入者 Beehive 入列","p":"20%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"外部維修通路占 LEAP 服務比重由十幾 % 升到 2030 年約 30%，大修工時外流；但外部通路仍向 GE 買零件（第三季備件成長部分來自外部通路），屬點對點","p":"30%","evidence_refs":["channel_business_model_shift#0"]},{"level":"🟡","text":"鑄件產能為全產業瓶頸，GE 以 117.5 億美元收購 CPP 並續用 ATI、Howmet；交割前產能改善靠合約","p":"25%","evidence_refs":["geo_supply_chain#0","supply_demand_durability#4"]},{"level":"🟡","text":"電動與氫能推進的長期替代；GE 自身參與（BETA 混合電動高空飛行、RISE 開放式風扇），窄體主力在 2030 年代中之前難以替代","p":"10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是乘客、決策與付款者是航空公司與租賃商；維修是適航法規強制的「需要」，只能延後不能取消。Boeing 估 2026 年初供給缺口約 2,000 架，IATA 稱再平衡不早於 2030 年代初；第三季 CFM56 退役率僅 1.5–2%，停機坪待修引擎年初至今增加 20%"},{"item":"決策層級","level":"🟢","text":"替代性在機型層決定：737MAX 只有 LEAP-1B、777X 只有 GE9X（逾 1,300 具訂單），選定後鎖 25 年以上；換零件來源需重新認證。弱點在下一代窄體招標時會重開"},{"item":"價值鏈分配","level":"🟡","text":"機身廠拿得少（BA 營益率 −7.4%），引擎商拿得多；但鑄鍛件供應商握有產能瓶頸，外部維修通路占比上升分走工時，非原廠零件業者（TDG 營益率 46.5%）在零件端競爭"},{"item":"社會容忍度","level":"🟡","text":"零件提價由航空公司吸收，布蘭特油價約 $111 時航空公司獲利受壓，提價空間受客戶健康度約束；監管面有 FAA 適航指令、ITAR 和解 3,600 萬美元、Section 232 談判期至 2027-01，屬政策風險但未見替代方案"}],"roiic":"事實表未涵蓋投入資本；有機增量投入多走損益表（年研發逾 30 億、GE9X 虧損），資產負債表增量小","reinvest_rate":"有機約 0–10%（2026 年 FCF 轉換率逾 100%）；計入 CPP 117.5 億則 2027 年單年遠超 100%","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率；事實表無投入資本口徑，周轉率、ROIC、增量 ROIC 與內生天花板均無法計算，只給利益率端：TTM 營益率 18.7%、FCF 利潤率 16.6%"},"combined":9.0,"score":9.0,"spread_table":[{"metric":"毛利率","GE":31.04,"BA":2.86,"RTX":20.35,"TDG":59.57,"GD":15.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","GE":18.68,"BA":-7.44,"RTX":11.21,"TDG":46.47,"GD":10.32,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","GE":16.58,"BA":-1.22,"RTX":11.75,"TDG":19.26,"GD":11.75,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","GE":3.48,"BA":3.98,"RTX":3.02,"TDG":null,"GD":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"BA","gm":2.86,"om":-7.44,"fcf_margin":-1.22,"rd_intensity":3.98,"strategy_note":"是客戶不是對手；TTM 營益率 −7.4%、FCF 利潤率 −1.2%，機身廠財務弱是 GE 新機交付與 GE9X 認證時程的外部風險","period":"TTM ending 2026-06-30（4季加總）"},{"name":"RTX","gm":20.35,"om":11.21,"fcf_margin":11.75,"rd_intensity":3.02,"strategy_note":"A320neo 上 GTF 與 LEAP-1A 雙源競爭；TTM 營益率 11.2% 低於 GE，IndiGo 逾 1,000 具 LEAP-1A 訂單顯示 LEAP 在雙源機型仍拿份額","period":"TTM ending 2026-06-30（4季加總）"},{"name":"TDG","gm":59.57,"om":46.47,"fcf_margin":19.26,"rd_intensity":null,"strategy_note":"售後專利零件標竿，營益率 46.5%，顯示航太售後零件定價上限遠高於 GE 目前水準，也是非原廠零件競爭的代表","period":"TTM ending 2026-06-30（4季加總）"},{"name":"GD","gm":15.38,"om":10.32,"fcf_margin":11.75,"rd_intensity":null,"strategy_note":"國防與公務機為主，不直接競爭商用引擎；營益率 10.3% 作為國防側利潤率參照","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（LEAP 裝機翻倍、大修年複合約 25%）＋價（零件目錄價）＋工作範圍擴大；淨回購約 2%／年；併購非主力","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"內生天花板事實表無法計算（無投入資本）；共識 FY2026E→FY2028E EPS 年複合 14.4%，缺口歸因利益率擴張與淨回購","segments":[{"item":"CES 第三季","value":"營收年增 21%、營業利益 28.87 億、利益率 27.9%；服務營收年增 17%、設備營收年增 38%"},{"item":"DPT 第三季","value":"營收年增 7%、營業利益 4.75 億、利益率 13.7%；在手訂單逾 300 億"},{"item":"2027 年管理層框架","value":"商用服務低雙位數成長、服務利益率持平、DPT 高個位數成長、GE9X 再增虧約 3 億、整體利益率與 2026 持平"}],"decay_signals":["毛利率連兩季年減：未亮（第二季年減 130bp、第三季年增 220bp）","核心市占縮減：未亮（無 sourced 證據）","主力產品提價後銷量下滑：未亮","EPS 成長高於營收成長逾 5pp：未亮（共識差約 3pp）","FCF／淨利連兩年 <0.75：未亮（2025 年 0.83、2026 年逾 1.0）","SBC 占營收逾 5% 且上升：事實表未涵蓋","TAM 萎縮或被替代：未亮","產業倍數三年系統性下移：事實表未涵蓋","維持性資本支出占 FCF 逾 60%：未亮","停止投資新產能：未亮（CPP、年資本支出逾 10 億）"],"trap_rating":"🟢"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；CPP 為產能投資，交割（2027 下半年）後再展開報酬檢核"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"CPP 117.5 億美元收購預計 2027 下半年交割，尚無已實現增量報酬；過往併購報酬事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購在 FY1 本益比約 35–37 倍執行，盈餘殖利率約 2.7%；只要 10 年期公債殖利率高於 0.7%，就低於公債加 2% 的門檻","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"股數年減約 2,400 萬股（約 2%，2026-07-16 CFO），第三季 EPS 成長部分來自股數減少；淨稀釋為負","grade":"過"}]},"valuation":{"basis":"Fwd P/E 與 PEG（品質複利成長）","tier":null,"peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比，無法做倍數錨"},"fwd_pe":37.17,"peg":2.6,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 37.2 倍、FY2027 32.5 倍，PEG 約 2.6 大於 2 屬貴；較前份約 44.6 倍已降一級，但 Base 年報酬約 7.7% 仍低於 8%，故判偏貴而非最貴","upside_short_pct":2.0,"upside_mid_pct":31.1},"trap_analysis":{"verdict":"🟢","label":"衰退訊號十類未亮，風險在倍數與航空周期而非生意變差"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"第三季法說分析師指出布蘭特約 $111、Delta 縮減排班；第一季公司已警示燃油成本使飛行量成長放緩；第三季出勤僅年增 1%","assumption":"2027 年服務成長由在手訂單與已飛週期決定，油價只延後不取消大修","consequence":"若航空公司財務惡化延續到 2028，退役率由 1.5–2% 升到 3–4%，二手可用料回流壓低 CFM56 備件，同時倍數由 37 倍壓到 18 倍，五年後股價可能低於現價一半","ruling":"部分採納：2027 年有 95% 備件在訂單、上半年待修引擎已進廠，短期反駁成立；2028 以後無法排除，Bear 機率由 25% 提到 30%。與唯一致命點（2027 財測下修服務成長）部分重疊，監測指標已回補","watch":"CFM56 年退役率、商用服務訂單年增率、航空公司出勤","evidence_refs":["end_markets#4"],"fact_refs":["f_kpi7_orders","f_kpi8_commercial_services_back"]},{"view":"論點成功但股東經濟變差","evidence":"CPP 117.5 億美元收購（約 70 億現金＋新債），CEO 表明不做自用供應商、續供其他引擎商；LEAP 外部維修通路占比 2030 年升到約 30%；GE9X 2027 年再增虧約 3 億","assumption":"營收與 EPS 成長兌現後，每股價值同步成長","consequence":"現金被併購占用使回購縮小，CPP 若以外部客戶為主，增量報酬可能低於 GE 本業；工時外流使 LEAP 大修量成長不等於 GE 毛利成長","ruling":"採納部分：情境淨回購由約 2% 降到 1.5%；CPP 報酬待交割後驗證","watch":"CPP 交割時程與交割後外部客戶營收、LEAP 外部通路占比","evidence_refs":["geo_supply_chain#0","channel_business_model_shift#0"],"fact_refs":["f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY1 本益比 37.2 倍、PEG 約 2.6；第二季上修指引後股價反跌逾 4%，TD Cowen 稱上修幅度可能不夠；Daiwa 目標 $301、中立，警告 2027–2028 共識有風險；賣方平均目標約 $397","assumption":"終端倍數能維持在 30 倍以上","consequence":"即使 EPS 照共識成長，倍數回到 28 倍時 Base 年報酬只有約 7.7%","ruling":"採納：這是觀望的主因，等價格而不是等基本面","watch":"FY2027 共識本益比是否 ≤29 倍（約 $265）","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"max_dd":{"lo":-60,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 345.73 → 本次 295.88（-14.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=345.73","side_b":"本次 price_at_dd=295.88","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 345.73 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 345.73 美元：Bull 價 540.75、Bear 價 196.4，五年期望值 +19.0%，基準年化 5.4%，不對稱比 1.3","side_b":"本次情境、股價仍用 345.73 美元：Bull 價 557.6、Bear 價 162，五年期望值 +4.9%，基準年化 2.3%，不對稱比 0.96","ruling":"先換情境、股價不動：五年期望值少 14.1 個百分點，基準年化少 3.1 個百分點。不對稱比由 1.3 變為 0.96。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 345.73 美元：五年期望值 +4.9%，基準年化 2.3%，不對稱比 0.96","side_b":"本次情境、股價 295.88 美元：五年期望值 +22.5%，基準年化 5.6%，不對稱比 1.63","ruling":"再換股價、情境不動：起點價下跌 14.4%，五年期望值多 17.7 個百分點，基準年化多 3.2 個百分點，不對稱比由 0.96 升到 1.63。合計五年期望值比前份多 3.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：基本面短期全面向上","cause":null,"prior_field":null,"side_a":"第三季訂單 190 億（+49%）、調整後營收 +18%、營益率 22.5%（+220bp）、EPS 2.25（+36%）；全年 EPS 指引上修到 8.00–8.10","side_b":"前一季（2026-07-16 CFO）給的全年上修與 2027 商用服務雙位數成長，本季都兌現並上調為低雙位數；前一季說現金轉換率會正常化，本季仍逾 100%","ruling":"一致，屬好於承諾；不構成看空理由","evidence_level":"公司 8-K 與法說會一手資料","settle_metric":null,"if_then":[],"evidence_refs":["customer_concentration_credit#1","supply_demand_durability#2","capital_markets_pricing#2"]},{"axis":"需求：在手訂單對油價","cause":null,"prior_field":null,"side_a":"服務訂單年增 23%、年初至今 30%，備件訂單更快；上半年待修引擎已進廠、上半年拆換預期年增逾 10%，停機坪待修引擎年初至今 +20%","side_b":"布蘭特約 $111、航空公司縮減排班，第三季出勤僅 +1%；第一季公司警示燃油成本使飛行量成長放緩","ruling":"可調和（時間差）：2027 年由已飛週期與在手訂單決定，選 A 側；2028 以後 B 側的影響尚未進入訂單，Bear 機率 30% 反映此風險","evidence_level":"一手法說與新聞稿；油價為分析師提問引述","settle_metric":"2027-01 財測的商用服務成長率；2027 年第一季服務訂單年增率","if_then":["若 2027-01 財測商用服務成長 <10%：不追、停止加碼，Bear 機率提到 35%，已持有者減碼一半","若 2027 年第一季服務訂單年增仍 ≥15% 且備件延交下降：確認 A 側，股價 ≤$265 時分批反買"],"evidence_refs":["end_markets#4","end_markets#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價較前份 $345.73 跌 14%，同期 EPS 指引兩度上修；FY2027 本益比 32.5 倍、RSI 31.8 超賣；2026 年現金流已超過 2028 年目標、利潤接近 2028 年目標；航改發電的 CFM56 零件需求未計入 2028 指引","side_b":"Base 年報酬約 7.7% 仍不到 8%：2027 年 GE9X 再增虧約 3 億、CES 利益率 2027 持平、CPP 動用約 70 億現金；油價壓力未進訂單","ruling":"不可調和，選 B 側：約束條件只有價格。依據是 Base 終端 13.85×28 倍＝$387.8，現價對應年報酬約 7.7%；要到 10% 需股價約 $265","evidence_level":"情境推導，輸入全來自共識與法說","settle_metric":"股價對 FY2027 共識 9.11 的倍數","if_then":["若股價 ≤$265 且第四季財報無服務成長下修：分批反買，首筆三分之一目標倉","若股價回到 $350 以上而 2027 財測未高於共識：不追"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"備件延交持續上升","cause":null,"prior_field":null,"side_a":"優先供應商物料投入連 10 季成長、第三季雙位數年增，LEAP 引擎造成的停飛降到接近零","side_b":"備件延交第二季季增 20%（2026-07-16 CFO），第三季再度季增（2026-10-20 CFO）","ruling":"可調和：需求成長快於供給，短期是訂單能見度；長期若延交不降，客戶轉向外部通路與非原廠零件。CEO 本季表明 2027 年要降延交","evidence_level":"一手法說","settle_metric":"2027 年各季備件延交是否季減","if_then":["若 2027 年連兩季延交仍季增且外部通路占比加速上升：停止加碼並重估護城河方向","若延交連兩季季減且備件營收成長 ≥20%：維持護城河判斷"],"evidence_refs":["end_markets#3","channel_business_model_shift#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭軸穩定：A320neo 雙源格局未變、ACP 新進入者規模小；結構軸轉好：IATA 與 Boeing 均稱供給不足延續到 2030 年代初","side_b":"其他結構軸變動中：CPP 反壟斷審查（2027 下半年交割）、Section 232 談判期至 2027-01-05 保留課稅選項、外部維修通路占比上升","ruling":"結構性轉好中（供需結構軸），其他結構軸有法規與通路變動，但現行零關稅協議與 IEEPA 退稅使關稅衝擊有限","evidence_level":"IATA、Boeing 展望與 10-Q","settle_metric":"Section 232 報告與 CPP 監管審查結果","if_then":["若 Section 232 對民用引擎零件課稅且公司未能轉嫁：停止加碼","若 CPP 監管要求剝離關鍵廠：不追，重估 2028 產能假設"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#0"]},{"axis":"前份漂移：價格帶動的估值與裁決","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 $345.73、FY1 本益比約 44.6 倍、估值最貴一級、觀望","side_b":"本次：股價 $295.88（−14%）、FY1 37.2 倍、FY2027 32.5 倍，估值降一級；EPS 指引中點再上修 $0.30 也貢獻一部分","ruling":"估值改善主要來自價格；裁決與角色由本輪決策輸入重算，觀望理由由「價格過高」改為「價格接近但 Base 年報酬仍不到 8%」","evidence_level":"事實表價格與共識","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：結構判斷維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質好但價格貴、陷阱低、護城河持平、五年後跑道寬、品質複利成長、中循環","side_b":"本次全部維持：第三季訂單 +49%、服務訂單 +23%、LEAP 大修到 2030 年年複合約 25% 再確認；新出現的油價壓力與 CPP 收購放進風險項，不改結構判斷","ruling":"新證據支持原判，不改","evidence_level":"一手法說與新聞稿","settle_metric":null,"if_then":[],"evidence_refs":["supply_demand_durability#2","end_markets#0"]},{"axis":"前份漂移：情境機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 25%、Bear 25%，最大回撤 −50%（單點），Base 終端 30 倍","side_b":"本次：Bull 25%、Base 45%、Bear 30%，Bear 上調因第三季法說的油價約 $111 與航空公司縮減排班；最大回撤改為 −35% 至 −60% 的範圍，以 250 週均線為錨；Base 終端改 28 倍","ruling":"回撤改用範圍與可驗證的均線錨；終端倍數下修 2 倍是因 2027 年利益率持平、成長在 2028 後降到約 10%","evidence_level":"情境推導","settle_metric":null,"if_then":[],"evidence_refs":["end_markets#4"]},{"axis":"前份漂移：進場重啟門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"次年度共識 Fwd PE ≤ 35x（今日＝$305，為 13 週前價位）；或 FY2028 財測確認 CES margin 擴張＋GE9X 虧損見頂 → 門檻升至 ~$350","side_b":"股價 ≤ $265（FY2027 共識 EPS 9.11 的 29 倍，對應 Base 年報酬約 10%）","ruling":"舊門檻已觸發（現價對 FY2027 共識 32.5 倍 ≤35 倍），依規定是重跑判斷而非直接建倉；重跑發現 2027 年 GE9X 再增虧約 3 億、CES 利益率 2027 持平、CPP 動用約 70 億現金，Base 年報酬僅約 7.7%，分批反買門檻收緊到 29 倍（$265）；FY2028 財測尚未給出，第二條件未觸發","evidence_level":"第三季法說 CFO 2027 框架","settle_metric":"股價對 FY2027 共識倍數","if_then":["若股價 ≤$265：分批反買首筆","若 2027-01 財測 EPS 中點 ≥$9.40：門檻上調到約 $280 並重跑"],"evidence_refs":["regulatory_antitrust#0"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"（前份無唯一致命點）","side_b":"2027 年 1 月第四季財報給出的 2027 財測把商用服務成長下修到個位數","ruling":"新設 Single Thing：商用服務成長是 EPS 最大單一敏感項（低雙位數對應約 35–40 億美元營收增量），選它而非較戲劇化的適航事件；發生時不追、停止加碼，已持有者減碼一半","evidence_level":"第三季法說 CFO","settle_metric":"2027-01 財測","if_then":["若發生：減碼一半、Bear 機率提到 35% 並重跑"],"evidence_refs":[]},{"axis":"kill 指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"（前份無 kill 指標）","side_b":"商用服務營收年增連 2 季 <8%；服務訂單連 2 季年減；CFM56 年退役率 ≥3%；CES 利益率連 4 季年減 ≥50bp；2027 EPS 指引中點 <$8.80","ruling":"新設可量化的減碼與清倉條件：前兩條任一觸發即減碼，三條以上同時觸發即清倉","evidence_level":"公司季報與法說","settle_metric":null,"if_then":["若任一 kill 指標觸發：減碼一半","若三條以上同時觸發：清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 FY2027 共識 29 倍以下才開始分批反買","type":"估值rearm","maps_to":"H1","metric":"股價對 FY2027 共識 EPS 9.11 的倍數","threshold":"股價 ≤ $265","action":"分批反買，首筆三分之一目標倉","source_freq":"每日股價","date":null,"evidence_refs":["capital_markets_pricing#1"]},{"n":2,"text":"2027 財測把商用服務成長下修到個位數","type":"Single Thing","maps_to":"H1","metric":"2027 商用服務營收成長指引","threshold":"<10%","action":"不追、停止加碼；已持有者減碼一半並重跑","source_freq":"年度財測","date":"2027-01","evidence_refs":["end_markets#4"]},{"n":3,"text":"油價壓力進入訂單：服務訂單轉負","type":"風險","maps_to":"R1","metric":"商用服務訂單年增率","threshold":"連 2 季年減","action":"減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["end_markets#4"]},{"n":4,"text":"新適航指令或合規事件佔用維修產能","type":"風險","maps_to":"R3","metric":"FAA 適航指令範圍與 GE9X 認證時程","threshold":"涉及 LEAP 或 CFM56 全機隊且要求提前拆換，或 GE9X 認證晚於 2027-06-30","action":"停止加碼並重跑","source_freq":"FAA／EASA 公告、每季法說","date":null,"evidence_refs":["product_recall_warning#0","major_events#2","reg_tariff_export#2"]},{"n":5,"text":"CPP 收購監管或整合失敗","type":"風險","maps_to":"R2","metric":"CPP 交割時程與交割後外部客戶營收","threshold":"交割延至 2028 或被要求剝離；交割後外部客戶營收年減逾 10%","action":"停止加碼","source_freq":"8-K、10-Q","date":"2027-09","evidence_refs":["geo_supply_chain#0","major_events#0"]},{"n":6,"text":"2028 利益率拐點驗證","type":"假設驗證","maps_to":"H2","metric":"CES 營業利益率","threshold":"2028 全年 ≥28.5%；連 4 季年減 ≥50bp 視為削弱","action":"削弱則停止加碼，反轉則減碼一半","source_freq":"每季分部數字","date":null,"evidence_refs":[]},{"n":7,"text":"下一代窄體推進失守","type":"清倉","maps_to":"R4","metric":"空巴或波音下一代窄體引擎選型","threshold":"宣布非 CFM 為唯一或主力引擎","action":"清倉","source_freq":"機身廠公告","date":null,"evidence_refs":["substitute_technology#0"]},{"n":8,"text":"第四季財報與 2027 財測後重跑","type":"複審日期","maps_to":"H1","metric":"2027 財測","threshold":"財報公布","action":"重跑判斷","source_freq":"年度","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"商用服務營收年增率（季）","bear_threshold":"連 2 季 <8%","window":"2027 年各季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"商用服務訂單年增率（季）","bear_threshold":"連 2 季年減","window":"2027 年各季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"CFM56 年退役率","bear_threshold":"≥3%（2026 年約 1.5–2%）","window":"2027 全年","source":"公司法說會","last_status":"ok"},{"metric":"CES 營業利益率（季）","bear_threshold":"連 4 季年減 ≥50bp","window":"2027–2028","source":"公司季報分部數字","last_status":"ok"},{"metric":"2027 年調整後 EPS 指引中點","bear_threshold":"<$8.80","window":"2027-01 財報","source":"公司財測","last_status":"unknown"}],"evidence_dismissed":[{"ref":"major_events#1","reason":"衍生訴訟是股東代公司向董事與高管求償，勝訴利益歸公司，不是公司對外賠償；10-K 原文說與 2025 年 4 月已和解的 Sjunde AP-Fonden 案事實相同，且未揭露請求金額，構不成對未來現金流的負向證據"},{"ref":"lawsuit_class_action#0","reason":"與同一份 10-K 法律附註的兩件衍生訴訟重複收錄；同一來源另載搜尋未見 2026 年新提起的證券集體訴訟"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=7.39, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='GE 的 Bull 情境有 LEAP 大修與裝機基數的量價骨架，成長跑道也有公司公開來源支持；但 EPS 逐步推導和歷史類比都不完整，Bull 依據大致站得住，只是細節未經驗證。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 $265 以下（FY2027 共識 EPS 9.11 的 29 倍）'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"6%","requires_critic":[],"rearm_trigger":"股價 ≤ $265（FY2027 共識 EPS 9.11 的 29 倍，對應 Base 年報酬約 10%）","exec_line":"股價 ≤$265 先建三分之一目標倉；2027-01 財測商用服務成長 ≥10% 再加三分之一；基本面無損而跌到 $230 以下加最後三分之一；回撤可能達 −35% 至 −60%，基本面完整時不因波動砍倉"},"reasoning":{"industry":"第三季 GAAP 營收 141.18 億美元、調整後營收 132.85 億（年增 18%），調整後營業利益 29.88 億、營益率 22.5%（年增 220bp）；TTM 毛利率 31.0%。分部：CES 營收年增 21%、營業利益 28.87 億、利益率 27.9%（年減 10bp）；DPT 營收年增 7%、營業利益 4.75 億、利益率 13.7%。CES 占兩大分部營業利益約八成六，其中商用服務是主體，2026 年服務營收增量約 55 億（第三季法說 CFO）。商用服務在手訂單逾 1,700 億，進入第四季時 95% 以上備件營收已在訂單裡。產業時鐘判 II 擴張：訂單年增 49%、交付年增逾 20%、供給仍追不上需求，依據是訂單與交機數據，不是股價。供需持久性判結構性持久：IATA 研究稱交機放緩屬結構性限制、再平衡不早於 2030 年代初；Boeing 2026 年 7 月展望稱 2026 年初約 2,000 架供給缺口。單點依賴：客戶端集中在少數機身廠與大型航空公司（10-K 風險段，單一客戶占比事實表未涵蓋）；供給端鑄件是瓶頸，CPP 收購就是在處理這一點。","moat":"機制是裝機基數乘上數十年服務年金：在翼 80,000 具引擎、23 億飛行小時以上資料，零件屬適航認證件，換供應要重新認證。可證方向用營益率差代理（同業 ROIC 事實表未涵蓋）：GE TTM 營益率 18.7%，RTX 11.2%、GD 10.3%、BA −7.4%；GE 自身營益率由 2022 年 12.3% 升到 2025 年 18.9%，差距擴大。執行力評 9：AOG 降到接近零、內部大修週轉比 2025 年底縮短一週以上、LEAP 風扇組件產出翻倍；定價力評 9：零件目錄價策略延續（2026-07-16 CFO），IndiGo 逾 1,000 具 LEAP-1A、土耳其航空逾 300 具 LEAP-1B 加全機隊長約。當期 ROIC 因無投入資本口徑無法算，只能給利益率端；四個持續期檢查點兩綠兩黃。","growth":"成長組成以量與價為主：LEAP 大修到 2030 年年複合約 25%、裝機基數年增低到中個位數、零件目錄價、工作範圍擴大；淨回購約 2%／年；CPP 為產能投資不是成長主力。共識 EPS：FY2026E 7.96、FY2027E 9.11、FY2028E 10.41，兩年年複合 14.4%；共識營收 FY1→FY2 年增 11.2%。內生天花板因無投入資本口徑無法計算；EPS 與營收成長差約 3pp，歸因於 2028 年起利益率擴張（GE9X 虧損回落、LEAP 服務利益率對齊）與淨回購，不歸因於倍數重估。衰退訊號十類未亮燈：毛利率未連兩季年減（第二季年減、第三季回升）、FCF／淨利 2025 年 0.83 且 2026 年逾 1.0、EPS 與營收成長差未超過 5pp。","governance":"FCF／淨利：2025 年 FCF 72.64 億 ÷ 淨利 87.04 億＝0.83；2026 年迄今轉換率 105%，全年指引 FCF 91–94 億且轉換率逾 100%（第三季法說 CFO）；2023、2024 年 0.46、0.56 是因淨利含分拆與出售利得。現金去向：股息殖利率 0.6%、回購（股數年減約 2%）、CPP 約 70 億現金加新債（117.5 億−70 億＝約 47.5 億），目前淨負債 102.85 億。SBC 占營收事實表未涵蓋。前一季 CFO 說轉換率會正常化，本季仍維持逾 100%，屬好於預期。","valuation":"現價 $295.88，FY1 共識 EPS 7.96（低於公司指引下緣 8.00），FY1 本益比 37.2 倍、FY2027 32.5 倍、FY2028 28.4 倍。PEG 以 FY2026E→FY2028E 共識年複合 14.4% 計約 2.6，屬貴；FY2025 調整後實際 EPS 事實表未涵蓋，故不用三年口徑。五年分位事實表未涵蓋，只有 4 個年度端點：本益比分位 2.1%（早年 GAAP 淨利含分拆利得，失真不採用）、P/S 分位 74.1%。短期上檔：12 個月後以 FY2028E 10.41 乘 29 倍約 $302，約 +2%；中期：Base 五年終端 13.85×28 倍＝$387.8，約 +31%。FY1 共識近三個月上修 5.3%，基本面動能正向，但價格已先反映大部分。","premortem":"三視角反證見反證紀錄：論點失敗的路徑是油價與航空公司財務壓力推高退役率、二手可用料回流壓低備件；股東經濟變差的路徑是 CPP 吃掉回購、外部通路分走工時；價格已反映太多的路徑是 PEG 約 2.6 下倍數均值回歸。股價 $295.88 在 52 週均線 318.55 之下、104 週均線 270.94 之上，距 250 週均線 165.57 約 −44%；RSI 31.8、26 週報酬 +7.4%。衰退訊號十類未亮，陷阱風險低。"},"plain":{"six":{"how_it_makes_money":"賺航空公司在 25 年以上機隊壽命內的強制維修錢；錢卡在適航認證零件與大修工時這一節點，新引擎是用虧損換裝機基數","moat":"護城河方向 →：裝機基數與單一引擎地位穩定，執行力改善，但外部維修通路與備件延交讓部分工時外流","growth":"五年後跑道寬 🟢：LEAP 裝機 2025→2030 翻倍、三分之二 CFM56 機隊未做第二次大修，下一條曲線是 LEAP 第二次大修與寬體工作範圍擴大","capital":"資本配置中等：股數持續淨減、現金轉換率高，但回購價位偏貴，CPP 收購要等交割後驗證","valuation":"現價要求 2026–2031 年 EPS 年複合約 12% 且終端仍給 28 倍，才有約 7.7% 年報酬；成長我相信，倍數能否守在 30 倍以上我不信","how_wrong":"最可能看錯在油價引發的航空業下行把 2028 年的服務成長打斷，同時倍數由 37 倍壓到 20 倍以下"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 $265 以下（FY2027 共識 EPS 9.11 的 29 倍）","qc48_result":"pass","qc48_note":"GE 的 Bull 情境有 LEAP 大修與裝機基數的量價骨架，成長跑道也有公司公開來源支持；但 EPS 逐步推導和歷史類比都不完整，Bull 依據大致站得住，只是細節未經驗證。","trap":"🟢","val":"🟠","moat":"A","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":295.88,"week26_return_pct":7.39,"consensus_rev_3m_pct":5.29,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母用調整後 EPS 共識 7.96，與公司指引 8.00–8.10 同口徑，無一次性爭議"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"GE9X 升級版中段密封 FAA 認證（公司目標 2026 年底）","impact":"中","watch":"若延到 2027 下半年，GE9X 虧損與 777X 交付延後"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年財測","impact":"高","watch":"商用服務成長是否 ≥10%、CES 利益率是否持平、GE9X 增虧約 3 億是否維持"},{"date":"2027-01","date_precision":"month","type":"regulatory","event":"Section 232 航太談判期進度報告（2027-01-05 前）","impact":"中","watch":"是否對民用引擎與零件課稅、零關稅協議是否延續"},{"date":"2027-09","date_precision":"quarter","type":"capacity","event":"CPP 收購監管審查與 2027 下半年交割","impact":"中","watch":"是否被要求剝離、交割後外部客戶是否流失"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,559B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GE_20261022/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河</h2>
<p class="lead">護城河評 A、方向持平，執行與定價力都強。</p>
<ul class="pts">
<li>護城河的機制是裝機基數乘上數十年強制維修年金。737MAX 與 777X 是單一引擎，A320neo 是雙源之一。售後零件是適航認證件，換供應來源要重新認證，成本與時間都高，這是航空公司不輕易轉身的原因。</li>
<li>可驗證的證據用營益率差代理，因為同業 ROIC 事實表沒有涵蓋。GE 的 TTM 營益率 18.7%，RTX 是 11.2%，GD 是 10.3%，BA 是 −7.4%。GE 自己的營益率從 2022 年 12.3% 升到 2025 年 18.9%，差距在擴大，不是縮小。</li>
<li>執行力評 9。AOG（因缺零件停飛）降到接近零，內部大修週轉比 2025 年底縮短一週以上，LEAP 風扇組件產出翻倍，優先供應商的物料投入已連續 10 季成長。這些是供應鏈真的在改善的證據，不只是管理層說法。</li>
<li>定價力也評 9。零件目錄價策略延續，95% 以上備件營收已在訂單裡。IndiGo 逾 1,000 具 LEAP-1A 訂單，顯示 LEAP 在雙源機型上仍拿到份額。土耳其航空逾 300 具 LEAP-1B 加全機隊長約，是定價鎖定的另一個例子。</li>
<li>護城河方向判持平，不判向上。加分是執行力擴大，扣分有兩項。備件延交連兩季季增，第二季季增 20%，第三季再度季增。LEAP 外部維修通路占服務比重，預計由十幾 % 升到 2030 年約 30%，部分大修工時會外流。兩邊互相抵銷。</li>
<li>威脅清單有四項，都屬點對點，沒有全面性。雙源機型與國防新案的競爭，包括 A320neo 上的 GTF 與美國空軍無人機引擎計畫（新進入者 Beehive 入列），機率約 20%。外部通路機率約 30%。鑄件瓶頸約 25%。電動與氫能替代約 10%。</li>
<li>持續期四個檢查點兩綠兩黃。需求基礎值與決策層級是綠，因為維修是法規強制，只能延後不能取消，且替代性在機型層就決定了。價值鏈分配與社會容忍度是黃，因為鑄鍛件供應商握有瓶頸，油價約 $111 時航空公司獲利受壓，零件提價空間受客戶健康度約束。</li>
<li>投入資本口徑事實表沒給，所以 ROIC、增量 ROIC 與內生天花板都無法計算，只能給利益率端：TTM 營益率 18.7%、FCF 利潤率 16.6%。有機增量投入多走損益表，年研發逾 30 億與 GE9X 虧損都在其中，資產負債表上的增量很小。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```