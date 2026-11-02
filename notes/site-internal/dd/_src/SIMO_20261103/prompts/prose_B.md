你是 stock-analyst v20 的**散文層（prose）agent**，標的 SIMO（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：SIMO　日期：2026-11-03　archetype：None　前份裁決：2026-07-10　觀望｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2065B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（678B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（874B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（803B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1438B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（736B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（921B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2455B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1324B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2838B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2065           3454-4935      5 條（2–6 內）  
s3                  8000         678           5125-7322      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3115          8320-11885      5 條（2–6 內）  
s6                 11000         736          7185-10264      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         921           1805-2579      5 條（2–6 內）  
s10                 5000        2455           1782-2545      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2838           2000-2162      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4790B；至少需散文≈40.21KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70%
−69%
−65
−65%
−50%
−40%
−40
−39.4%
−39%
−32%
−24.9%
−19.7%
−16.8%
−13%
−10
−4.9%
−4.07
−3.9%
−2.79
−2.56
−0.5
0
0%
0.05
0.30
0.34
0.37
0.47
0.49
0.6
0.7%
0.745
0.75
0.8
1%
01
1
1.0
1.17%
1.17
1.226
1.4
1.5%
1.58
1.6
1.87
2%
$2.00
02
2
2.04
2.05
$2.30
2.5
2.78
2.81
2.9
3
3%
03
3.1%
3.64
04
4%
4
4.07
4.1
4.25
4.35
4.7
5
5%
5.17
5.41
5.602
5.88
6
06
6.16
6.2%
6.4%
6.4
6.5
6.85
6.9%
07
7%
7
7.4
08
8
8.6
8.856
9%
9
09
9.5
9.536
$10
10%
10
10.1
10.5%
10.51%
11
11.27
11.5
12
13
13.6
14
14.45
15
15%
15.5
16
16%
16.3
17
18
19.0
19
19.61
20%
20
20.7
21.3%
21.5
22
22.73
23
24%
24
25
25%
26
28
29
29.0%
29.3%
30%
30
30.9%
31
32.1%
32.5%
35.4%
35.4
36
36.8
37%
38
39%
39.4%
40%
45%
47.5%
48
48.3%
49
49.3
50
50%
50.2%
50.5%
52%
52
52.2
53.7%
54
55%
56%
56.9%
58%
60%
66%
69.43
70
$70
75%
82%
84%
90
100%
100
104.5
$115
120
121%
131%
$145
$180
189.82
192.76
$196.49
196.49
$209
$230
246%
$251
$266
302
324.26
$324.26
$370
$380.50
$450
480
630
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
8299
20261103
1,730
3,369
3,391
9,500
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
{"meta":{"ticker":"SIMO","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Silicon Motion Technology Corporation"},"oneliner":"營收一年翻倍、Q3 毛利率 53.7%，但現價只給 FY2027 共識約 10 倍，市場把它當 NAND 週期高點定價；Q3 營業現金流 −2.56 億美元，盈餘還沒變成現金，現在不追，等現金流連兩季轉正或股價 ≤$145。","thesis":{"H":[{"id":"H1","text":"企業開機碟、Ferri 車用與 MonTitan 讓 2027 年營收再成長至少 40%，毛利率守在 50% 以上；消費性出貨衰退不改變成長方向","2y":"FY2027 營收 ≥ FY2026 的 1.4 倍，各季毛利率 ≥50%","5y":null,"10y":null,"threshold":"FY2027 營收年增 ≥40%（管理層 Q3 2026 法說）；季 Non-GAAP 毛利率 ≥50%（Q3 為 53.7%，Q4 指引 54–55%）","source":"公司季報新聞稿（6-K）、2027 年 1 月法說的全年指引","drift_rule":"季毛利率連 2 季比 50% 低 5% 以上（約 <47.5%）削弱；連 3 季低 10% 以上（約 <45%）反轉；1 月法說全年營收指引低於 +40% 即削弱"},{"id":"H2","text":"解決方案的高毛利來自 6 個月議價與車用多年合約，不是 NAND 漲價帶來的存貨利得；存貨約兩季周轉回現金，營業現金流在 2027 上半年轉正","2y":"2027Q1–Q2 營業現金流轉正，存貨停止季增","5y":null,"10y":null,"threshold":"營業現金流 >0 連 2 季（Q3 2026 為 −2.56 億美元）；NAND 合約價走平後的那一季，季毛利率仍 ≥50%","source":"季報現金流量表與資產負債表；TrendForce 合約價報告","drift_rule":"2027Q2 營業現金流仍為負且存貨續增，削弱；NAND 合約價走平或季減後，毛利率連 3 季 <45%，反轉"},{"id":"H3","text":"MonTitan 企業級控制器與近 CPU 開機碟成為第二條成長曲線，讓控制器業務在 2028–2030 年 NAND 週期下行時仍能成長","2y":null,"5y":"2028 年即使 NAND 合約價下跌，控制器營收仍年增；PCIe 6 MonTitan 2027Q1 送樣、2028 年量產","10y":null,"threshold":"PCIe 6 MonTitan 2027Q1 開始送樣；近 CPU 開機碟 2H27 開始出貨；2028 年控制器業務年增 ≥10%","source":"法說的產品進度與管理層口頭揭露的控制器／解決方案比重","drift_rule":"送樣或量產時程延後連 4 季削弱；延後連 6 季，或 2028 年控制器營收年減 ≥10%，反轉"}],"R":[{"id":"R1","text":"NAND 週期反轉：2H27 起供需平衡、合約價轉跌，解決方案營收與毛利一起下滑並出現存貨跌價，盈餘下修幅度接近 2023 年","h_ref":"H2","clock":"🔥","threshold":"NAND 合約價首度季減，且 SIMO 季毛利率 <50%","evidence_refs":["supply_demand_durability#4"]},{"id":"R2","text":"消費端量縮：PC 與手機因記憶體漲價而降規，零售 SSD 通路上半年近乎消失；eMMC／UFS 持平，SSD 控制器 Q4 指引持平到小降","h_ref":"H1","clock":"⚡","threshold":"控制器業務連 2 季季減（依管理層口頭揭露）","evidence_refs":["channel_business_model_shift#1"]},{"id":"R3","text":"客戶集中：前五大客戶約占 2025 年營收 66%，四家 >10% 客戶合計 58%；其中 Kioxia、Micron 同時是 NAND 供應商與潛在自製者，任一家轉自製或換供應商，就是一成以上的營收缺口","h_ref":"H1","clock":"🔥","threshold":"任一 >10% 客戶在年報名單中消失，或單季營收季減 ≥15% 且管理層歸因於客戶","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_second_source#0"]},{"id":"R4","text":"供應鏈與地緣：總部與研發在台灣；晶圓主要靠台積電、次要中芯，且沒有長期合約；基板吃緊；關稅與實體清單風險同時存在","h_ref":"H1","clock":"🐢","threshold":"單季毛利率因關稅或基板成本下滑 ≥2pp 且管理層明確歸因；或任一代工來源受出口管制限制","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R5","text":"營運資金吃掉盈餘：Q3 營業現金流 −2.56 億美元、存貨約 8 億美元，靠 11.5 億美元零息可轉債支撐。存貨兩季周轉不成就要再融資；股價若高於轉換價 $380.50，另有約 9% 稀釋","h_ref":"H2","clock":"⚡","threshold":"2027Q2 營業現金流仍為負，或公司宣布新一輪股權或可轉債融資","evidence_refs":[]}],"single_thing":{"description":"NAND 合約價在 2027–2028 年首度轉為季減（TrendForce 合約價報告）","why_fatal":"解決方案已占營收四成以上，存貨約 8 億美元是在高價期買進的。NAND 價格轉跌時，含 NAND 轉嫁的營收與毛利會同步下滑，再加上存貨跌價，2023 年營收 −32%、EPS −69% 的情況可能重演。這是 EPS 最大的單一敏感項","if_happens":"空頭機率由 30% 上調到 40%；若持有，減碼至半倉；觀望期間不進場","how_monitor":"TrendForce 每月與每季的 NAND 合約價；SIMO 季報的毛利率、存貨與營業現金流；法說對 6 個月議價合約的說法","probability":"12–24 個月內約 40%：TrendForce 看 2H27 平衡，管理層、美光、Kuo 看緊到 2028，兩邊抵銷後略偏向會發生"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":10.0,"peg_fy2":0.34,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":3.64,"FY2026E":13.6,"FY2027E":19.61,"FY2028E":22.73},"fy_end_month":12,"eps_basis":"每 ADS 盈餘。FY2026E–FY2028E 為 Koyfin 共識（2026-10-31），事實表未標 GAAP 或 Non-GAAP；量級與 Q3 法說 Non-GAAP 每 ADS 4.35 美元一致，推定為 Non-GAAP。FY2025A 3.64 取年度財報 GAAP 稀釋 EPS（Non-GAAP 基期事實表未涵蓋），基期口徑不同，用它算的三年 CAGR 偏高"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"盈餘隨 NAND 週期大幅擺動：2023 年營收 −32%、EPS −69%；本輪營業利益率由 2025 年 10.5% 升到 Q3 GAAP 29.0%，現價對 FY2027 共識只有約 10 倍"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉。TrendForce（2026-07、2026-09）預期 2027 年供給成長超過需求、2H27 趨於平衡；SIMO 管理層、美光 CEO 與分析師 Kuo 則看緊到 2028。2028 年新廠投產是供給可逆的依據","bargaining":{"up":"晶圓主要靠台積電、次要中芯，都沒有長期合約；NAND 向多家原廠採購，缺貨期供應商議價力強；基板吃緊","down":"前五大客戶約 66%、前十大 82%；四家 >10% 客戶合計 58%；解決方案每 6 個月議價一次","geo":"總部與研發在台灣；中國有 YMTC 與受政策扶持的在地控制器廠，公司在中國擴研發以服務當地客戶"},"profit_pool_dir":"流向 NAND 原廠：同業對照中，原廠的營業利益率約為 SIMO 的三倍；SIMO 靠解決方案進入原廠讓出的小容量市場","tam_table":[{"item":"企業開機碟市場","value":"2026 年約 30 億美元，2030 年逾 50 億（管理層估計，Q3 2026 法說）"},{"item":"近 CPU 含 DRAM 開機碟","value":"2030 年至少 100 億美元（管理層估計）；SIMO 預計 2H27 量產，模組廠夥伴可能 2027Q2 先出貨"},{"item":"PC 端 PCIe 5 滲透率","value":"目前約 10%，2027 年底 20–25%（管理層估計）"},{"item":"PCIe 6 MonTitan 可觸及份額","value":"初始設定至少 15–20%（Q2 2026 法說，CEO）"},{"item":"利潤池占比五年變化與第三方份額","value":"事實表未涵蓋"}]},"moat":{"mechanism":"韌體加上跨多家 NAND 原廠的相容經驗，形成設計導入黏性（車用認證、平台型開機碟、企業級控制器）","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Q3 營收、毛利率、營益率全部高於指引上緣，企業與車用設計導入增加。定價權持平：營業利益率仍低於群聯（兩者期間差一季）；毛利率上升與 NAND 漲價同步，無法證明是議價力提升。兩者合併為持平","peer_na_reason":"事實表沒有同業 ROIC，以營業利益率差代替；同業資料期間不一致（群聯截至 2026-06、Marvell 截至 2026-07）","threats":[{"level":"🟡","text":"NAND 原廠自製控制器：所有主要原廠都有自製能力，過去原廠收回自製曾傷害營運。目前方向相反，原廠正轉向外部控制器，並把小容量市場讓出","p":"20%","evidence_refs":["customer_second_source#0","competitive_share_entrants#1"]},{"level":"🟡","text":"中國在地化控制器廠受政策扶持，加上群聯、Microchip 的點對點競爭。管理層稱中國廠難取得先進製程，企業級暫無威脅","p":"30%","evidence_refs":["competitive_share_entrants#0","substitute_technology#1"]},{"level":"🟡","text":"替代架構：固態儲存若改用 NAND 以外的非揮發記憶體，或新規格把控制功能整合進其他晶粒，控制器可及市場會縮小；目前沒有量產時程","p":"10%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（存貨墊高投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"控制器是每顆 SSD、eMMC／UFS 的必要元件。NAND 缺貨時，SSD 廠寧可降容量也要維持出貨量，控制器需求不減反增（2026-06 公司說法）。使用者（伺服器、車廠）、決策者（模組廠、原廠）、付款者（模組廠）三個角色都成立。消費端屬於延後購買，企業與車用則是真正的需要"},{"item":"決策層級","level":"🟡","text":"車用是 3–5 年的認證專案，價格與供貨在專案開始時談定，替換成本高；企業開機碟靠平台設計導入。消費性控制器則每一代產品重新選，模組廠可以在 SIMO、群聯與中國廠之間切換，單一型號層級的替代性就很高"},{"item":"價值鏈分配","level":"🔴","text":"這一輪週期的利潤主要留在 NAND 原廠，同業對照中原廠的營業利益率約為 SIMO 的三倍。原廠同時是 SIMO 的供應商、>10% 客戶（Kioxia、Micron）與潛在自製者。解決方案的成長來自原廠讓出小容量市場，這是原廠自己的分配選擇，週期反轉後可能收回"},{"item":"社會容忍度","level":"🟢","text":"儲存控制器不是受監管或政治敏感的民生必需品，沒有社會面的價格上限；關稅與出口管制屬貿易政策風險，另列在風險項"}],"roiic":"約 30%（增量稅後營業利益約 2.04 億 ÷ 估計增量投入資本約 6.85 億；週期高點數字）","reinvest_rate":"約 246%（估計再投資額約 6.85 億 ÷ TTM 稅後營業利益約 2.78 億；超過 100% 的部分由可轉債支應）","endo_ceiling":30,"formula_note":"TTM 營收約 16.3 億美元（EV 69.43 億 ÷ trailing EV/S 4.25）。TTM 稅後營業利益 ≈ 16.3 億 × 營業利益率 21.3% × (1−20%) ≈ 2.78 億；FY2025 為 8.856 億 × 10.51% × 0.8 ≈ 0.745 億，增量約 2.04 億。再投資額以稅後營業利益減自由現金流估算：TTM 自由現金流 ≈ 16.3 億 × −24.9% ≈ −4.07 億，所以再投資額 ≈ 2.78 + 4.07 ≈ 6.85 億，再投資率約 246%。ROIIC ≈ 2.04 ÷ 6.85 ≈ 30%。內生成長上界把再投資率上限設為 100%，等於 30%。這是週期高點利益率下的數字，正規化後會明顯較低。稅率 20% 取 Q4 指引的有效稅率；投入資本存量事實表未涵蓋，當期 ROIC 無法直接算"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","SIMO":50.54,"8299.TWO":56.85,"MRVL":52.21,"SNDK":76.84,"unit":"%"},{"metric":"營業利益率","SIMO":21.3,"8299.TWO":30.89,"MRVL":16.81,"SNDK":68.43,"unit":"%"},{"metric":"FCF 利潤率","SIMO":-24.9,"8299.TWO":-8.12,"MRVL":18.23,"SNDK":61.63,"unit":"%"},{"metric":"研發密度","SIMO":23.7,"8299.TWO":21.85,"MRVL":25.84,"SNDK":5.64,"unit":"%"}],"competitors":[{"name":"8299.TWO","gm":56.85,"om":30.89,"fcf_margin":-8.12,"rd_intensity":21.85,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"MRVL","gm":52.21,"om":16.81,"fcf_margin":18.23,"rd_intensity":25.84,"period":"TTM ending 2026-07-31（4季加總）"},{"name":"SNDK","gm":76.84,"om":68.43,"fcf_margin":61.63,"rd_intensity":5.64,"period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量＋價＋組合：解決方案含 NAND 轉嫁（價格成分），控制器靠份額與規格升級；無併購，股數微增","runway_years":"5–9（企業級與車用滲透率低；消費性控制器已是業界標準）","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 約 30% × 再投資率上限 100%（實際約 246%，超過的部分靠可轉債），推導見護城河題；這是週期高點的數字，正規化後應更低","segments":[{"item":"控制器（eMMC／UFS、SSD 含 MonTitan）","value":"Q3 約占營收 60%（CEO 口頭揭露）。SSD 控制器季增、年增都強，Q4 指引持平到小降；eMMC／UFS Q3 小幅季減，短期持平"},{"item":"解決方案（Ferri 車用、企業開機碟）","value":"Q3 逾 40%，季增逾 75%；Q2 約 30%，一年前同期約 4%。2027 年可能到 50%，營收含 NAND"},{"item":"MonTitan 企業級","value":"Q2 法說稱 2026 年底占營收 5–10%，Q3 未更新占比；PCIe 6 已流片，2027Q1 送樣"},{"item":"分部毛利率","value":"事實表未涵蓋；管理層稱車用毛利率優於預期，MonTitan 拉高毛利"}],"decay_signals":[{"item":"EPS 成長顯著高於營收成長（差 >5pp）","lit":true,"note":"FY2025A 到 FY2026E 營收約 +121%，EPS 由 3.64 到 13.6（基期為 GAAP，數字偏高）；成長主要來自利益率擴張"},{"item":"FCF／淨利 <0.75 連 2 年","lit":true,"note":"2024 年 0.37、2025 年 0.05；2026Q3 自由現金流 −2.79 億美元"},{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 50.2%、Q3 53.7%，高於 2025 全年 48.3%"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"沒有第三方份額數據；管理層稱持續取得份額"},{"item":"SBC／營收 >5% 且逐年上升","lit":false,"note":"Q3 約 3.1%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"替代記憶體與新架構都還沒有量產時程"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋產業倍數；SIMO 自身 FY+2 本益比近四個月由 25 倍以上降到約 10 倍，期間太短，不計入"},{"item":"其餘三項（提價後銷量下滑、維持性資本支出占 FCF、停止投資新產能）","lit":false,"note":"不適用或事實表未涵蓋；FCF 為負，維持性資本支出占比無法計算"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產品與新市場，不靠併購；資本回報以股利為主（年股利由每 ADS $2.00 調升到 $2.30），近期未見回購，現金主要投入 NAND 存貨"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年沒有併購；MaxLinear 案中 SIMO 是被併方，且該案已終止","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"法說把回購列為伺機而為，Q2、Q3 現金去向未見回購；回購均價事實表未涵蓋","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數由 2025 年約 3,369 萬（淨利 1.226 億 ÷ EPS 3.64）到目前 3,391 萬，約 +0.7%，低於每年 1.5%；可轉債轉換價 $380.50 之上另有約 302 萬股潛在稀釋，尚未發生","grade":"過"}]},"valuation":{"basis":"Forward 本益比（FY2026E、FY2027E 共識）為主，對照正規化盈餘","tier":"循環型儲存半導體","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比；終端倍數改以公司自身歷史區間（前份記載 7–22 倍）與現值 14.45 倍對照"},"fwd_pe":14.45,"peg":0.49,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Forward 本益比 14.45 倍（FY2026E），對 FY2027E 約 10 倍、FY2028E 約 8.6 倍。FY2026E 到 FY2028E 共識年化 29.3%，PEG 0.49，表面上便宜。但分母落在 NAND 週期高點、有爭議，便宜的論證不成立。改看現價要求什麼：$196.49 ＝ 正規化 EPS 14 美元 × 14 倍，大約落在我基本情境 2029 年谷底到 2031 年之間，所以判合理。五年連續分位事實表未涵蓋；四個年度端點內，trailing 本益比分位 36.8，P/S 與 EV/S 分位 100。後兩者因營收含 NAND 轉嫁，跨年不可比","upside_short_pct":6.4,"upside_mid_pct":35.4},"trap_analysis":{"verdict":"🟡","label":"週期高點的低本益比"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2023 年營收 −32%、營業利益率 6.4%、EPS 1.58（年度財報）。TrendForce 預期 2027 年供給成長超過需求、2H27 緩解。有分析師指出控制器廠不像原廠直接受惠 NAND 漲價，營收可能隨週期反轉快速下滑。分析師在 Q3 法說指出存貨已到約 8 億美元，CFO 沒有否認","assumption":"解決方案的高毛利來自合約與認證，不是 NAND 價差","consequence":"NAND 合約價在 2H27–2028 轉跌，解決方案營收縮水並提列存貨跌價，2028–2029 年 EPS 落到 6.5–9.5 美元。市場給 10–12 倍，股價約 $70–$115，相對現價約 −40%～−65%。五年虧 50% 最可能就是這條路","ruling":"採納，作為空頭情境（30%）的主軸。這條與唯一致命點是同一件事，兩者對得上，不另改","watch":"TrendForce 合約價；SIMO 季毛利率、存貨與營業現金流","evidence_refs":["supply_demand_durability#4"],"fact_refs":["f_kpi5_non_gaap","f_kpi6","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營業現金流 −2.56 億美元，自由現金流 −2.79 億；公司以 0% 利率發行 11.5 億美元可轉債，轉換價 $380.50；2025 年 FCF 只有 630 萬美元，FCF／淨利 0.05","assumption":"營收成長會轉成股東的現金","consequence":"即使 2027 年營收 +40%，存貨也會跟著營收放大，現金流可能繼續為負。股價若漲過 $380.50，可轉債轉換稀釋約 9%，多頭情境的每股盈餘被攤薄。利潤也可能在議價中被 NAND 原廠拿回","ruling":"部分採納：多頭情境的 EPS 已扣約 9% 稀釋，並把現金流轉正列為重啟進場條件","watch":"營業現金流、存貨、股數","evidence_refs":[],"fact_refs":["f_kpi6","f_kpi7_ocf_capex_23_0","f_shares_diluted_m","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"P/S 與 EV/S 在四個年度端點中都是最高（分位 100）；FY2028E 共識 EPS 成長降到 +16%；上一輪 2022 年高點 EPS 只有 5.17","assumption":"現價 10 倍 FY2027 已經夠便宜","consequence":"如果正規化 EPS 只有 12–14 美元，現價等於正規化盈餘的 14–16 倍，並不便宜","ruling":"部分採納：估值結論定為合理而非便宜。但 P/S 偏高有一部分是營收含 NAND 轉嫁造成的，跨年不可比，這條不是全部的故事","watch":"1 月指引後 FY2027 共識是否下修","evidence_refs":[],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy3","f_pe_current"]},{"view":"論點失敗","evidence":"前五大客戶約 66%，>10% 客戶合計 58%；所有主要原廠都有自製控制器能力；中國競爭者受在地化政策扶持","assumption":"原廠會持續外包、客戶結構穩定","consequence":"任一家大客戶轉自製或換供應商，就是一成以上的營收缺口，而且多半發生在週期反轉、原廠產能鬆動的時候","ruling":"反駁它是主要致命路徑：原廠目前反向外包（Q1 2026 法說），中國廠難取得先進製程。保留為長期風險","watch":"年報 >10% 客戶名單、單季營收季減幅度","evidence_refs":["customer_concentration_credit#0","competitive_share_entrants#0","customer_second_source#1"],"fact_refs":["f_kpi0_gaap"]}],"max_dd":{"lo":-65,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 324.26 → 本次 196.49（-39.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=324.26","side_b":"本次 price_at_dd=196.49","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 觀望 → 本次 迴避","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=觀望","side_b":"本次 dca_verdict=迴避","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 不持有","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=不持有","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 324.26 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 324.26 美元：Bull 價 480、Bear 價 120，五年期望值 −16.8%，基準年化 −4.9%，不對稱比 0.6","side_b":"本次情境、股價仍用 324.26 美元：Bull 價 480、Bear 價 104.5，五年期望值 −19.7%，基準年化 −3.9%，不對稱比 0.47","ruling":"先換情境、股價不動：五年期望值少 2.9 個百分點，基準年化多 1.0 個百分點。不對稱比由 0.6 變為 0.47。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 324.26 美元：五年期望值 −19.7%，基準年化 −3.9%，不對稱比 0.47","side_b":"本次情境、股價 196.49 美元：五年期望值 +32.5%，基準年化 6.2%，不對稱比 2.05","ruling":"再換股價、情境不動：起點價下跌 39.4%，五年期望值多 52.2 個百分點，基準年化多 10.1 個百分點，不對稱比由 0.47 升到 2.05。合計五年期望值比前份多 49.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"盈餘是結構性還是週期高點","cause":null,"prior_field":null,"side_a":"管理層、美光與 Kuo：NAND 供給吃緊到 2028。公司 6 個月議價、車用 3–5 年合約，毛利率可守在 50% 中段，2027 年營收至少 +40%","side_b":"TrendForce 與市場：2027 年供給成長超過需求、2H27 緩解；控制器廠不直接受惠 NAND 漲價，營收會隨週期反轉；現價只給 FY2027 共識約 10 倍","ruling":"不可調和，兩邊方向相反。採 B 側作為基本情境的方向：2028 年盈餘持平，2029 年回落約兩成。依據有三：Q3 營業現金流 −2.56 億美元，高毛利還沒變成現金；2023 年營收 −32%、EPS −69%，是這家公司上一輪的實際紀錄；獨立來源（TrendForce）看到的平衡時點比管理層早約一年。A 側的證據要等 2027 上半年的現金流才看得到","evidence_level":"中：雙方都有獨立來源，決勝數據 2027Q2 才會出現","settle_metric":"2027Q1–Q2 營業現金流與存貨；NAND 合約價首度季減那一季的毛利率","if_then":["若 2027 上半年營業現金流連兩季轉正、存貨下降且季毛利率 ≥52%，改採 A 側，重跑研究後以 2% 首倉分兩批建立","若 NAND 合約價首度季減且當季毛利率 <50%，維持不碰，空頭機率上調至 40%","若股價先漲但現金流證據未到，不追","若股價跌破 $145，而毛利率與現金流沒有惡化，分批反買，首批 1%"],"evidence_refs":["supply_demand_durability#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"Q4 指引營業利益率 36–37%，推算單季年化 EPS 約 20.7 美元，已超過 FY2027 共識 19.61。FY1 共識三個月上修 56%，股價卻比前份低 39%。賣方目標價均值 $370（2026-09）與 $251（2026-08）都在現價之上","side_b":"這正是週期股在盈餘高點的典型樣子：本益比最低的時候，往往最該小心。營業現金流為負，賣方目標價 $230–$450，分布很散","ruling":"反駁，但保留一條路：現金流證據若提前出現，A 側成立，現價就是便宜。我比賣方共識悲觀，是因為共識 FY2028 仍有 +16%，等於假設 NAND 平衡後解決方案毛利不降，這與 TrendForce 的時點衝突。股價已比前份低 39%，不等於有安全邊際。目標價全距比值約 2 倍，未超過 2.5 倍，不因此下調信心；但兩份資料都在 Q3 財報前，沒有反映最新上修","evidence_level":"中","settle_metric":"季營業現金流與存貨","if_then":["若 Q4 2026 營業現金流已轉正，提前重跑研究，不必等兩季"],"evidence_refs":[]},{"axis":"產業態勢：競爭、結構、其他","cause":null,"prior_field":null,"side_a":"競爭：20-F 點名群聯、Microchip、原廠自製與受政策扶持的中國廠，預期競爭加劇。其他：關稅、實體清單、零售 SSD 通路消失、替代記憶體","side_b":"結構：原廠把小容量與開機碟市場讓出、轉向外部控制器；車用與企業級的認證週期長","ruling":"雙向拉鋸。結構面短期轉好（Q2、Q3 法說：原廠退出小容量市場），競爭面在中國持續惡化（20-F）。淨效果在 NAND 吃緊期偏正，週期反轉後原廠可能回頭，方向不穩","evidence_level":"中","settle_metric":"原廠是否重回開機碟與小容量市場","if_then":["若原廠在 NAND 鬆動後重新推出開機碟產品，結構面改判轉弱，空頭機率上調至 40%"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","reg_tariff_export#0","channel_business_model_shift#1"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"2026-07-30 Q2 法說，CFO Jason Tsai：長期毛利率仍是 48–50%；解決方案 2027 年占營收至少三分之一「有可能」","side_b":"2026-10-29 Q3 法說，CFO Jason Tsai：2027 年毛利率 low-to-mid 50%。CEO Wallace Kou：解決方案 2027 年可能到 50%","ruling":"可調和，屬程度差異。財測一路超標，Q3 營收、毛利率、營益率都高於指引上緣，可信度加分。但毛利率框架是在 NAND 價格最高的一季上調的，而解決方案占比加速上升代表 NAND 價格曝險變大；兩件事同時發生，所以不把新框架當成正規化水準","evidence_level":"高","settle_metric":"NAND 走平後的季毛利率","if_then":["若 NAND 走平兩季後毛利率仍 ≥52%，接受新框架，基本情境 2028 年 EPS 上調到共識附近"],"evidence_refs":[]},{"axis":"估值結論","cause":"新證據","prior_field":["val"],"side_a":"前份：估值偏貴。現價 $324.26，依前份重啟條件「18 倍約 $180」反推 FY2027 共識約 10 美元，等於 30 倍以上","side_b":"本次：合理。現價 $196.49，FY2027 共識上修到 19.61，約 10 倍；但分母在週期高點，有爭議","ruling":"改判的主因是新證據：Q3 大幅超標，加上 2027 年至少 +40% 的指引，讓 FY2027 共識約翻倍。股價同期下跌 39% 是次因。因為分母有爭議，只升到合理，不判便宜","evidence_level":"高：共識數字與股價都是事實表數據","settle_metric":"1 月法說後 FY2027 共識是否守在 19 美元以上","if_then":["若 1 月指引後 FY2027 共識下修超過 15%，估值結論退回偏貴"],"evidence_refs":[]},{"axis":"公司類型","cause":"新證據","prior_field":["archetype"],"side_a":"前份：品質複利成長","side_b":"本次：循環/商品為主，品質複利成長為輔","ruling":"新證據是營收結構改變。解決方案（含 NAND）由去年同期約 4% 升到 Q3 逾 40%，2027 年可能到 50%；Q3 營業現金流 −2.56 億美元，存貨約 8 億美元，NAND 價格曝險已經進入損益表與資產負債表，Q3 法說分析師 Naji 的提問問的就是這點。控制器本業仍有複利性質，所以列為次要","evidence_level":"高","settle_metric":"NAND 合約價走平後的毛利率與現金流","if_then":["若 NAND 合約價走平兩季後毛利率仍 ≥52% 且營業現金流轉正，類型改回以品質複利成長為主"],"evidence_refs":[]},{"axis":"維持不變的判斷","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","cycle_position"],"side_a":"前份：綜合訊號 B、陷阱風險中、護城河持平、五年後成長跑道中等、晚循環","side_b":"本次：與前份相同","ruling":"新證據逐項檢查後維持。綜合訊號：估值改善，被週線轉弱與盈餘品質疑慮抵銷。陷阱風險：衰退信號亮兩項（EPS 成長遠高於營收、FCF／淨利連兩年 <0.75），仍屬中。護城河：執行面擴大、定價權未證，合併為持平。成長跑道：企業級第二曲線有設計導入，但份額與 TAM 仍是管理層估計。景氣位置：合約價 Q3 到 Q4 走平、消費端需求破壞、新廠 2028 年規劃，仍是晚循環","evidence_level":"中","settle_metric":"各項對應的觸發條件","if_then":["若 NAND 合約價首度季減，景氣位置改判進入下行，陷阱風險升為高"],"evidence_refs":[]},{"axis":"最大回撤範圍","cause":"價格變動","prior_field":["max_dd_pct"],"side_a":"前份：−70%（自 $324.26 起算）","side_b":"本次：−40%～−65%（自 $196.49 起算）","ruling":"股價已跌 39%，部分下行已經發生。以空頭盈餘 7–9.5 美元 × 10–12 倍回推，地板約 $70–$115，換算的回撤比前份淺，但仍可能超過 −50%","evidence_level":"中","settle_metric":"NAND 合約價與季毛利率","if_then":["若 NAND 合約價首度季減，以下緣 −65% 做準備，持股上限不超過 3%"],"evidence_refs":[]},{"axis":"情境機率","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份：多頭 25%、空頭 30%","side_b":"本次：多頭 20%、基本 50%、空頭 30%","ruling":"情境樹改以 FY2031 為終端。空頭路徑明確以 NAND 合約價轉跌加存貨跌價建模，多頭路徑扣入可轉債轉換約 9% 的稀釋。多頭需要 NAND 吃緊延續到 2028，與 TrendForce 的時點衝突，所以降到 20%。空頭維持 30%，因為共識成長超過內生上界，下限就是 30%","evidence_level":"中","settle_metric":"2H27 合約價","if_then":["若 TrendForce 改口 2028 年仍短缺，多頭機率回到 25%"],"evidence_refs":[]},{"axis":"重啟進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE FY27 回落至 ≤18x（約 $180）；或 MonTitan 退出 2026 占營收 ≥7% 且 FY27 共識續上修確認第二曲線；或 through-cycle EPS 站穩 $10+","side_b":"2027 上半年營業現金流連兩季轉正且存貨下降；或股價 ≤$145 而季毛利率仍 ≥50%","ruling":"前份第一條已經成立：FY2027 本益比約 10 倍，低於 18 倍，但成立的方式是共識 EPS 翻倍，而不是股價跌到 $180，本次就是依此重跑研究。第二條：本季法說沒給 MonTitan 占比，無法驗證。第三條：週期平均 EPS 是否站穩 10 美元，要經過一次下行才看得到。本輪的約束是盈餘還沒變成現金、分母落在週期高點，所以重啟進場改綁現金流證據，或綁一個足以吸收空頭情境的價格","evidence_level":"高","settle_metric":"季營業現金流、存貨；股價","if_then":["若任一新條件成立，重跑研究後首倉 1–2%","若股價先漲而現金流未轉正，不追"],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）","cause":"新證據","prior_field":null,"side_a":"前份為空（null），未設唯一致命點","side_b":"NAND 合約價在 2027–2028 年首度轉為季減","ruling":"新增 Single Thing：解決方案已占營收四成以上，並持有約 8 億美元存貨，NAND 價格方向成為 EPS 最大的單一敏感項。若發生，空頭機率上調至 40%，持有者減碼至半倉","evidence_level":"中","settle_metric":"TrendForce 合約價季變動","if_then":["若合約價首度季減，減碼至半倉；未持有則不進場"],"evidence_refs":["supply_demand_durability#4"]},{"axis":"減碼與清倉指標","cause":"新證據","prior_field":null,"side_a":"前份為空（null），未設減碼或清倉指標","side_b":"季毛利率連 2 季 <50% 減碼、連 3 季 <45% 清倉；2027Q2 營業現金流仍為負且存貨續增；NAND 合約價首度季減；任一 >10% 客戶退出名單","ruling":"新增。本輪公司類型改為以循環為主，需要可量測的減碼與清倉指標；門檻取自 H1、H2 與唯一致命點","evidence_level":"中","settle_metric":"季報與 TrendForce","if_then":["若毛利率連 3 季 <45%，清倉"],"evidence_refs":[]},{"axis":"裁決與角色","cause":"新證據","prior_field":[],"side_a":"前份：觀望","side_b":"本次輸入：估值改為合理、公司類型改為以循環為主、景氣位置晚循環、要等價格或現金流證據","ruling":"最終裁決與角色由下游依本次輸入計算。輸入面的變動全部來自 Q3 財報與法說的新證據，方向仍是不追、等條件","evidence_level":"中","settle_metric":"重啟進場條件","if_then":["若重啟進場條件成立，重跑研究"],"evidence_refs":[]},{"axis":"前份假設：市場維持成長股倍數","cause":"新證據","prior_field":null,"side_a":"前份 H3：FPE FY+2 ≥ 20x，連 2 個月 <18x 即削弱","side_b":"本次：FY2027 本益比約 10 倍，遠低於 18 倍","ruling":"前份 H3 已反轉，市場改用週期股倍數定價。前份 R1 的兩半：倍數壓縮已經發生；NAND 現貨鬆動還沒發生，CEO 說 Q3、Q4 合約價持平。本次不再把倍數維持當成假設，改把盈餘能否變成現金當成主假設","evidence_level":"高","settle_metric":"NAND 合約價","if_then":["若 NAND 價格也開始鬆動，前份 R1 完整成立，依唯一致命點處理"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年 1 月 Q4 法說給出 2027 全年指引：營收年增是否 ≥40%、毛利率是否在 50% 中段","type":"假設驗證","maps_to":"H1","metric":"FY2027 營收指引年增率；Q1 2027 毛利率指引","threshold":"營收 ≥+40% 且毛利率指引 ≥52%","action":"符合即列為重啟條件之一，但仍需現金流確認；低於 +40% 則 H1 削弱，維持不碰","source_freq":"季報法說（每季）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"NAND 合約價首度轉為季減","type":"Single Thing","maps_to":"R1","metric":"NAND 合約價季變動（TrendForce）","threshold":"首度季減","action":"空頭機率上調至 40%；觀望期間不進場；若已持有，減碼至半倉","source_freq":"TrendForce 月報與季報","date":null,"evidence_refs":["supply_demand_durability#4"]},{"n":3,"text":"營業現金流與存貨：存貨能否約兩季周轉回現金","type":"假設驗證","maps_to":"H2","metric":"季營業現金流、存貨","threshold":"2027Q1–Q2 營業現金流連兩季 >0 且存貨季減","action":"達標即重跑研究，首倉 2%；2027Q2 仍為負且存貨續增，則 H2 削弱，維持不碰","source_freq":"季報（每季）","date":"2027-07","evidence_refs":[]},{"n":4,"text":"價格跌到足以吸收空頭情境","type":"估值rearm","maps_to":null,"metric":"股價與季毛利率","threshold":"≤$145（約 FY2027 共識 7.4 倍）且季毛利率 ≥50%","action":"重跑研究後分批反買，首批 1%，第二批等下一季現金流","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":5,"text":"大客戶流失或轉自製","type":"風險","maps_to":"R3","metric":">10% 客戶名單（20-F）；單季營收季減","threshold":"任一 >10% 客戶退出名單，或單季營收季減 ≥15% 且歸因於客戶","action":"若持有，減碼至半倉；未持有，重啟條件延後一季","source_freq":"年報（每年 4 月）加季報","date":"2027-04","evidence_refs":["customer_second_source#1","customer_concentration_credit#0"]},{"n":6,"text":"關稅、基板或代工成本吸收失敗","type":"風險","maps_to":"R4","metric":"季毛利率變動與管理層歸因","threshold":"單季毛利率下滑 ≥2pp，且明確歸因於關稅、基板或代工","action":"若持有，減碼一半；未持有，不進場","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1","geo_supply_chain#0"]},{"n":7,"text":"Water Island 證券集體訴訟（S.D. Cal.）進展，SIMO 與兩位高管為被告；受影響金額與審結日期事實表未涵蓋","type":"風險","maps_to":null,"metric":"集體認證裁定、和解金額","threshold":"集體認證通過，且出現金額 ≥ 期末現金 10%（約 9,500 萬美元）的不利和解","action":"若持有，減至半倉；若檢方或 SEC 介入，清倉","source_freq":"年報法律程序章節、法院公告","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":8,"text":"Q4 2026 財報後複審","type":"複審日期","maps_to":null,"metric":"全份研究重跑","threshold":"日期到","action":"重跑研究","source_freq":"一次","date":"2027-02-15","evidence_refs":[]},{"n":9,"text":"再融資或稀釋","type":"風險","maps_to":"R5","metric":"新增股權或可轉債融資公告","threshold":"2027 年內再發行股權類融資","action":"重啟條件作廢並重寫；若持有，減碼","source_freq":"6-K 公告","date":null,"evidence_refs":[]}],"kill_metrics":[{"metric":"季 Non-GAAP 毛利率","bear_threshold":"連 2 季 <50%（NAND 合約價走平或季減時）減碼；連 3 季 <45% 清倉","window":"2027Q1–2028Q4","source":"公司季報新聞稿（6-K）","last_status":"ok"},{"metric":"季營業現金流","bear_threshold":"2027Q2 仍為負且存貨續增","window":"2026Q4–2027Q2","source":"季報現金流量表","last_status":"warning"},{"metric":"NAND 合約價季變動","bear_threshold":"首度季減","window":"2027–2028","source":"TrendForce 合約價報告","last_status":"ok"},{"metric":">10% 客戶名單","bear_threshold":"任一家退出名單","window":"每年 20-F（4 月）","source":"SEC 20-F 客戶集中揭露","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":"≤3%（循環股，深回撤可能超過 −50%）","requires_critic":[],"rearm_trigger":"2027 上半年營業現金流連兩季轉正且存貨下降；或股價 ≤$145 而季毛利率仍 ≥50%","exec_line":"任一條件成立先重跑研究；首倉 1–2%，分兩批，第二批等下一季現金流確認；續漲但證據未到不追"},"reasoning":{"industry":"營收結構：Q3 2026 營收 5.602 億美元，季增 24%、年增 131%，高於 Q2 法說給的指引上緣 5.41 億。CEO 口頭揭露控制器約占 60%，解決方案（Ferri 車用＋企業開機碟）約占 40%，後者季增逾 75%。CEO 說 2027 年兩者可能各半；Q2 法說時 CFO 還只說解決方案占「至少三分之一」有可能。獲利：Non-GAAP 毛利率 53.7%、營業利益率 32.1%，GAAP 營業利益率 29.0%。Q4 指引營收 5.88–6.16 億、毛利率 54–55%、營業利益率 36–37%，全年營收年增逾 100%。產業時鐘判第三期（過熱），依據有四點：NAND 價格一年大漲；消費端已出現需求破壞，包括手機出貨預期 −10～15%、PC 降規、零售 SSD 通路上半年近乎消失；CEO 說 Q3、Q4 合約價差不多，明年季漲幅降到個位數；原廠 2028 年新廠已規劃。供需持久性判週期性將反轉：TrendForce 看 2027 年供給成長超過需求、2H27 緩解，管理層與美光看緊到 2028，兩邊時點差約一年。議價權：上游晶圓主要靠台積電，NAND 向原廠採購，兩者都沒有長期合約；下游前五大客戶約占 66%，四家 >10% 客戶合計 58%（PHISEMI、Kioxia、AFASTOR、Micron）。單點依賴在 NAND 取得能力。CEO 在 Q2 法說說，開機碟成長的前提是能確保 NAND 供應。這項能力一面是護城河（跟多家原廠都有關係），一面是集中度風險，因為原廠同時是供應商、客戶與潛在自製者。","moat":"機制：二十年的韌體與控制器設計經驗，加上相容多家 NAND 原廠顆粒的能力，轉成設計導入的黏性。具體例子有三：車用 3–5 年的認證專案、NVIDIA BlueField 開機碟的主要供應地位、MonTitan 七家已公布客戶 2026 年開始商業量產。方向證據：事實表沒有同業 ROIC，改比營業利益率。SIMO TTM 21.3%，低於群聯 30.9%（群聯資料期間到 2026-06）；毛利率 50.5% 也低於群聯 56.9%，所以沒有利潤率領先。份額只有管理層說法（持續取得份額、原廠轉向外部控制器），沒有第三方數字。評分：執行 8，理由是 Q3 營收、毛利率、營益率全部高於 Q2 法說指引上緣，PCIe 6 也已流片。定價權 6，理由是毛利率上升與 NAND 漲價同步；Q2 法說 CFO 還說長期毛利率 48–50%，一季後改口為 2027 年 low-to-mid 50%，新框架是在價格最高的一季上調的，不能當成議價力的證據。三項威脅都屬點對點或低機率，未扣分。增量報酬：ROIIC 約 30%，但再投資率約 246%，超過盈餘的部分靠可轉債支應，而且這組數字落在週期高點。持續期四項中，價值鏈分配判紅。","growth":"成長來源是量、價與組合：解決方案把 NAND 包進營收（價格成分），控制器靠份額與 PCIe 5、UFS 4.1 升級拉高 ASP；沒有併購，也沒有淨回購。三年共識 EPS：FY2026E 13.6、FY2027E 19.61、FY2028E 22.73（Koyfin），FY2026E 到 FY2028E 年化 29.3%。若以 FY2025A GAAP 3.64 為基期，年化 84%，但基期口徑不同，數字偏高。營收共識有 11–12 位分析師（yfinance），EPS 家數事實表未涵蓋。內生上界約 30%，推導見護城河題的增量報酬：共識兩年 CAGR 落在上界附近，三年口徑則超出。缺口可以歸因於利益率擴張，營業利益率由 2025 年 10.5% 升到 Q3 GAAP 29.0%，不屬於依賴重新評價。我的基本情境 FY2026E 到 FY2031E 年化約 6.9%，在上界內。成長跑道：企業級（MonTitan、開機碟）份額低、正在導入，但時程與 TAM 多是管理層估計；PCIe 6 要到 2027Q1 才送樣，近 CPU 開機碟 2H27 才量產。","governance":"FCF／淨利：2022 年 0.30、2023 年 1.87、2024 年 0.37、2025 年 0.05（年度財報）；2026Q3 營業現金流 −2.56 億美元，自由現金流 −2.79 億。SBC／營收：Q3 為 1,730 萬 ÷ 5.602 億，約 3.1%。Q3 現金去向：可轉債淨入 11.27 億美元，流出到營運資金（存貨）、股利與償還短期銀行借款，期末現金含受限為 9.536 億；未見回購，也沒有併購。股利由每 ADS 每年 $2.00 調到 $2.30。可轉債利率 0%、轉換價 $380.50，股價高於轉換價時約有 302 萬股潛在稀釋（約 9%）。目前淨負債 2.81 億（含租賃），等於用借來的錢養存貨。CFO 的目標是約兩季把 NAND 存貨轉成現金，並說這次募資足夠支應未來幾年的營運資金。三項計分：併購不適用；回購不適用；SBC 淨稀釋約 0.7%，通過。營運槓桿為正，營業利益成長快於營收，沒有壓縮。","valuation":"現價 $196.49。對 FY2026E 13.6 是 14.45 倍，對 FY2027E 19.61 約 10 倍，對 FY2028E 22.73 約 8.6 倍。FY1 共識三個月上修 56%，股價同期卻比前份判斷日低 39%，26 週報酬 −13%，表示盈餘上修全被倍數壓縮吃掉，市場在用週期股的方式定價。這個價格要求的是：2027–2028 年盈餘在 NAND 轉平後回到 13–15 美元，而不是延續成長。盈餘若守在 19 美元以上，現價便宜；若重演 2023 年的下修，現價仍然貴。我的基本情境是 2028 年持平、2029 年回落約兩成、2031 年回到 19 美元，終端 14 倍約 $266。上行空間的口徑：短期指 12 個月，以 FY2027E 基本情境 19.0 × 11 倍 ≈ $209，約 +6.4%；中期指五年基本情境終點，約 +35.4%。年化約 6–7%，偏弱。週線價格 189.82 低於 52 週均線 192.76，RSI 38，動能不熱也不弱。","premortem":"衰退信號十項亮兩項：EPS 成長遠高於營收成長（由利益率擴張帶動），以及 FCF／淨利連兩年低於 0.75（2024 年 0.37、2025 年 0.05）。陷阱風險與長期成長性都判中。壓力測試五項：NAND 合約價轉跌、最大客戶流失、存貨不轉現金而需再融資、消費性出貨再降 15%、台海或關稅造成供應中斷。只吸收得了兩項：單一客戶流失（每家 >10% 客戶約占一到兩成營收，期末現金 9.5 億撐得住），以及消費性再降（控制器占比正降到五成）。NAND 轉跌與再融資兩項正中弱點。最大回撤範圍 −40%～−65%，依據見情境樹。管理層迴避紀錄：Q2 法說不拆 Ferri 與開機碟、把 MonTitan 目標由 10% 改述為 5–10%、不評論季節性；Q3 法說仍不給分部細節，季節性與 2027 年營業費用延到 1 月再談，仲裁也沒有更新。這些迴避集中在最能檢驗盈餘品質的分部數字上。"},"plain":{"six":{"how_it_makes_money":"賺的是 NAND 原廠、模組廠、車廠與伺服器廠的控制器與小容量儲存方案錢。錢卡在 NAND 供給這一節：控制器靠設計導入收費，解決方案把 NAND 包進去賣，毛利與存貨都跟著 NAND 價格走。","moat":"護城河方向持平。執行面因企業與車用新產品而擴大；定價權仍跟著 NAND 週期走，對最接近的同業也沒有利潤率優勢。兩者相抵。","growth":"成長跑道中等。消費性控制器已是業界標準，滲透率高；企業級與車用是第二曲線，但還在早期，量化證據多半是管理層估計。","capital":"資本配置中等。股利持續調升、稀釋低，但成長完全靠舉債養存貨，現金轉換是本輪最弱的一環。","valuation":"合理、不便宜。現價等於假設盈餘高點過後回到每股約 14 美元、給 14 倍；我認為這個假設大致公允，安全邊際不足。","how_wrong":"最可能看錯的是把 NAND 高點的盈餘當成新常態；反方向的錯則是低估車用與企業級合約的黏性。陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤$145（約 FY2027 共識 7.4 倍）且季毛利率仍 ≥50%；或 2027 上半年營業現金流連兩季轉正且存貨下降","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":196.49,"week26_return_pct":-13.15,"consensus_rev_3m_pct":56.14,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2027E 19.61、FY2028E 22.73 建立在 NAND 吃緊延續與解決方案維持高毛利兩個前提上；Q3 營業現金流 −2.56 億美元，盈餘還沒被現金驗證。週期反轉時這組分母會大幅下修，2023 年 EPS 曾 −69%"},"catalysts":[{"date":"2027-01-31","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 全年指引（管理層說 1 月會給更完整的 2027 財測）","impact":"高","watch":"2027 年營收年增是否 ≥40%、毛利率與營業費用指引、Q1 季節性"},{"date":"2027-03-31","date_precision":"quarter","type":"product","event":"PCIe 6 MonTitan（4nm）開始送樣","impact":"中","watch":"送樣客戶數、是否如期"},{"date":"2027-06-30","date_precision":"quarter","type":"macro","event":"NAND 合約價走勢：TrendForce 預期 2H27 供需平衡","impact":"高","watch":"合約價是否首度季減"},{"date":"2027-09-30","date_precision":"quarter","type":"product","event":"近 CPU 含 DRAM 開機碟開始量產出貨（模組廠夥伴可能 Q2 先出貨）","impact":"中","watch":"首批客戶與營收貢獻"},{"date":"2027-04-30","date_precision":"month","type":"other","event":"FY2026 20-F 揭露客戶集中度與競爭者","impact":"中","watch":">10% 客戶名單與前五大占比"},{"date":null,"date_precision":null,"type":"other","event":"MaxLinear 仲裁終局裁決（求償 1.6 億美元終止費及損害賠償），聽證已於 2026-03 結束","impact":"中","watch":"裁決金額與收款時程；1.6 億美元約等於每 ADS 4.7 美元"}],"_projected_from":"v19"}
```
