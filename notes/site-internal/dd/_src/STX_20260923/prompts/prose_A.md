你是 stock-analyst v20 的**散文層（prose）agent**，標的 STX（2026-09-23）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20260923/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：STX　日期：2026-09-23　archetype：None　前份裁決：2026-07-29　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1700B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（640B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（996B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1323B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1131B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（398B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（944B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2146B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3642B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2317B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1700           3710-5300      5 條（2–6 內）  
s3                  8000         640           5152-7360      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3450          8085-11550      5 條（2–6 內）  
s6                 11000         398          7421-10602      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         944           1789-2556      5 條（2–6 內）  
s10                 5000        2146           1998-2854      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2317           2000-2683      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4749B；至少需散文≈40.25KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−75
−75%
−74%
−71%
−50
−50%
−37%
−21.8
−18
−6.3%
−3.5%
0
0%
0.2
0.3
0.36
0.4
0.5%
0.75
1%
1
1.1
1.5%
1.7
1.71
1.75
1.9
2
2.31
2.83
3%
03
3
3.3%
4
04
4.7%
5
5%
5.20
5.29
5.6%
5.69
5.71
6%
06
6
6.5%
6.97
07
7
7.30
8
08
09
9
10%
10
11
11%
11.18
11.4
11.7
12
13
14
14%
14.89
14.9%
15%
15
15.58
16
16.5
16.52
17%
17
17.07
17.25
18
18%
19
19%
20%
20
21.1%
22%
22
22.4%
23%
23
24
25%
25
25.57
25.6
26
26%
26.58
27
28
29
29%
30
30%
31%
31.05
34
$34
34%
34.6%
34.65%
35%
35.5
35.78
36
36.29
37%
38
40
40%
42%
42
43%
44.6%
45%
45.6%
46
47%
48.5%
49
49.5%
50%
50
52%
52.25%
52.7%
55%
55
55.37
56
57
57%
57.5%
58
60%
62
70%
70
71%
72.6%
73.84
76%
76.3%
78.29
81%
85
86
88%
90
98
100%
100
108
116.61
121.5%
121.52
140%
140.3%
$144
150%
150
195
218
$240
265
285
$300
300
$400
400
500
504.3
$505
$572
630
$644
644
000660
$715
747.3
$747.3
$760
914.72
$914.72
$940
2011
2023
2025
2026
2027
2028
2029
005930
20260923
$1,125
$1,200
$1,620
1,660
5,400
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
{"meta":{"ticker":"STX","date":"2026-09-23","schema":"v15.2","contract":"v19","company_name":"Seagate Technology Holdings plc"},"oneliner":"硬碟缺貨讓毛利率連 13 季擴張、Q1 財測再拉高，但現價已付清共識到 FY2029 的單價漲勢，循環走到後段；等股價回到 $572–644，或 CY2028 長約確認單價續漲，再重跑研究","thesis":{"H":[{"id":"H1","text":"資料中心 EB 需求維持結構性成長，長約配置持續往後滾到 CY2029","2y":null,"5y":"FY2031 前資料中心 EB 年增不低於 20%","10y":null,"threshold":"資料中心 EB 出貨年增 ≥20%，且管理層每季仍說 nearline 大部分已配置到 18 個月以後","source":"每季法說 CFO 準備稿的資料中心 EB 與年增；10-Q","drift_rule":"資料中心 EB 年增連 4 季低於 19%（偏離 5%）削弱；連 6 季低於 18%（偏離 10%）反轉"},{"id":"H2","text":"CY2027 已入約的價格加上供需缺口，讓毛利率在 FY2027 逐季上升、FY2028 守住 55% 以上","2y":"FY2028 全年 non-GAAP 毛利率不低於 55%","5y":null,"10y":null,"threshold":"FY2027 各季 non-GAAP 毛利率逐季上升（管理層承諾）；FY2028 不低於 55%；每 EB 單價年增大於 0","source":"每季財報新聞稿的 non-GAAP 毛利率；法說 Q&A 的每 EB 單價年增（分析師轉述、CFO 確認）","drift_rule":"FY2027 任一季毛利率季減即削弱；FY2028 連 2 季低於 52.25% 削弱、連 3 季低於 49.5% 反轉"},{"id":"H3","text":"HAMR 領先換成每 TB 成本優勢，而且領先期撐到 WD HAMR 放量之後","2y":null,"5y":"Mozaic 5、6 持續領先 WD 同代產品至少一年","10y":null,"threshold":"2027 年 6 月底 nearline EB 七成在 HAMR；Mozaic 5 在 2027 年底前送客戶認證","source":"每季法說的 HAMR 占比與里程碑；WD 新聞稿與法說的 HAMR 認證進度","drift_rule":"里程碑延後 1 季削弱；延後 2 季以上，或 WD HAMR 在 Mozaic 5 送認證前已在兩家大型雲端量產，反轉"}],"R":[{"id":"R1","text":"供給追上、單價見頂：WD 40TB ePMR 2026 下半年上市、HAMR 2027 量產；STX 擴磁頭廠、TDK 加磁頭產能，12–18 個月後陸續到位。CY2028 長約定價時缺口可能收斂，重演上一個高峰後的下行","h_ref":"H2","clock":"🔥","threshold":"每 EB 單價年增連 2 季 ≤0，或毛利率連 2 季季減","evidence_refs":["supply_demand_durability#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","substitute_technology#4","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1"]},{"id":"R2","text":"QLC 替代加上漲價的反作用：STX 越漲價，硬碟對 QLC 的每 TB 價差越窄；等 NAND 價格回落，兩邊一起收窄，溫資料層加速轉向快閃","h_ref":"H1","clock":"🐢","threshold":"資料中心 EB 年增連 2 季低於 15%，且管理層或客戶提到溫資料層改用快閃","evidence_refs":["substitute_technology#0","substitute_technology#3"]},{"id":"R3","text":"供應鏈與出口管制：主軸馬達約八成出自 Nidec，稀土精煉約九成在中國，組裝集中泰國，控制晶片靠台積電；10-K 列出關稅、出口管制可能造成重大不利影響。2023 年因對華為出貨被 BIS 罰 3 億美元，仍在分季付款，附五年暫緩拒絕出口令；另有 1.75 億美元證券集體訴訟和解待最終核准","h_ref":"H1","clock":"⚡","threshold":"單季營收低於財測下緣，且公司把原因歸給零件、稀土、出口管制或關稅","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#5","geo_supply_chain#6","geo_supply_chain#7","geo_supply_chain#8","reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#5","regulatory_antitrust#1","regulatory_antitrust#2","major_events#1"]},{"id":"R4","text":"雲端暫停採購：FY2023 雲端消化庫存時 nearline 採購大減；最大客戶約占營收 14%，一家放慢就看得見。CFO 說電力、建照延誤會讓需求往後推","h_ref":"H1","clock":"🔥","threshold":"資料中心營收季減，或 CFO 提到訂單遞延","evidence_refs":["cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5","customer_concentration_credit#0"]}],"single_thing":{"description":"CY2028 年度 build-to-order 合約（預計 2027 年第二到第三季談定）的新約每 EB 單價年增率轉負","why_fatal":"共識 FY2026A→FY2029E EPS 年複合約 71%，量的內生上界約 25%，約六成五的成長靠單價。單價轉負，毛利率從高峰回落，EPS 改走 Bear 路徑，倍數也從前瞻約 25 倍掉到循環常態","if_happens":"未持有者移出觀察名單、不等回檔買；已持有者清倉。Bear 機率由 30% 升到 45%","how_monitor":"2027 年 4 月與 7 月法說對新長約定價的說法；每季每 EB 單價年增（分析師 Q&A 轉述、CFO 確認）；WD 同期的定價說法","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.52,"peg_fy2":0.3,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":15.58,"FY2027E":35.78,"FY2028E":55.37,"FY2029E":78.29},"fy_end_month":6,"eps_basis":"non-GAAP 稀釋 EPS；財年止於最接近 6 月 30 日的週五（FY2026 止於 2026-07-03）；共識取 Koyfin 2026-09-19 快照，家數事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20260923/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"近七年有 GAAP 虧損年（FY2023），毛利率谷峰差超過 30 個百分點（FY2023 最差一季 17%，本季 52.7%），營收由每 EB 單價驅動；長約與顆數紀律讓波動變小，但沒有消失"},"industry":{"clock_phase":"III","sd_verdict_source":"量是結構性、價是週期性：資料留存與 AI 推論讓 EB 需求長期成長，長約把量鎖到 CY2028；但單價漲勢來自供需缺口，供給可逆性中等——WD HAMR 2027 量產，STX 與 TDK 的磁頭擴產 12–18 個月後到位","bargaining":{"up":"上游關鍵零件集中：主軸馬達約八成出自 Nidec，稀土精煉約九成在中國，控制晶片由台積電代工；磁頭與碟片自製，北愛爾蘭晶圓廠約供應全球三分之一磁頭（第三方估計）","down":"買方集中但目前弱勢：最大客戶約占營收 14%，資料中心占 81%；STX 產品只占客戶資本支出低到中個位數，缺貨時客戶願意付得比合約價還高","geo":"組裝與測試集中在泰國、馬來西亞、中國；2011 年泰國水災曾在幾週內讓全球硬碟產能少掉近半"},"profit_pool_dir":"利潤池正往硬碟廠移：CFO 說三年內毛利率幾乎變成三倍；但記憶體同業 TTM 毛利率 57–76%，仍高於 STX 的 45.6%","tam_table":[{"item":"2026 年全產業 HDD 營收","value":"上半年逾 150 億美元，全年可能超過 300 億（Coughlin，2026-08-09）"},{"item":"2026 年 Q2 全產業出貨","value":"504.3 EB，季增 5.6%；營收約 85 億美元，季增 14.9%"},{"item":"EB 份額（2025 全年）","value":"WDC 約 47%、STX 約 42%、Toshiba 約 11%（Coughlin 估計）"},{"item":"nearline 供給缺口（Morgan Stanley，經社群轉載）","value":"2026 年約 300 EB（10–15%），2027–28 年擴大到約 400 EB；供給年增 30–35%、需求年增 40–50%"}]},"moat":{"mechanism":"三家寡占＋顆數持平的供給紀律＋HAMR 單碟容量領先（40% nearline EB 已在 HAMR）＋磁頭、碟片、雷射自製；長約 2–3 年、少彈性","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"份額：2025 年 EB 份額 STX 約 42%、WD 約 47%，本季 STX 出貨對全產業 Q2 出貨約 43%，持平。定價能力擴大（每 EB 單價年增 10% 加速到約 20% 以上），但來自缺貨，不算護城河變寬。執行力穩定（HAMR 里程碑如期）。WD 40TB ePMR 與 2027 年 HAMR 會縮小容量差距","peer_na_reason":"同業表只有記憶體廠利潤率，沒有 WDC 與 Toshiba，無法計算對最強同業的 ROIC 差距","threats":[{"level":"🟡","text":"WD：40TB ePMR 2026 下半年上市、已在兩家大型雲端認證中；HAMR 2027 年認證並量產，2029 年 100TB。STX 的 HAMR 領先期大約只剩一到兩年，屬點對點競爭，但剛好落在 CY2028 定價的時間點","p":"60%","evidence_refs":["substitute_technology#4","channel_business_model_shift#5"]},{"level":"🟡","text":"QLC 大容量 SSD：TrendForce 說硬碟缺貨把部分需求推向 QLC，QLC 功耗約低 30%；另有分析師擔心能源效率需求限縮 Mozaic 4+ 的上檔。目前 NAND 價格偏高，CFO 說資料中心沒有替代品，先判點對點（溫資料層）。升級條件：NAND 價格回落、STX 同時繼續漲價，兩邊每 TB 價差一起收窄","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#3"]},{"level":"🟡","text":"Toshiba 與 TDK：Toshiba 推 34TB SMR，TDK 2026 年 4 月加磁頭產能，給第三家更多量","p":"30%","evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1"]}],"roic_durability":{"quadrant":"高利益率×周轉率未證：TTM 營業利益率 34.65%、Q4 44.6%，資本支出只占營收 4.7%，推定周轉不低；投入資本事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（雲端應用、AI 推論、影片）、決策者（雲端儲存架構）、付款者（雲端業者）三者一致，需求是真的。但延後購買的代價低：FY2023 雲端消化庫存時 nearline 採購大減、營收少 37%；CFO 2026-09-10 也承認電力、建照延誤會讓需求往後推"},{"item":"決策層級","level":"🟡","text":"客戶按儲存層級決定。冷資料層是在硬碟廠之間選：第二代 HAMR 認證已變快（30TB 約一年認證前 8–10 大客戶），WD 40TB 也在兩家大型雲端認證，換供應商的門檻在降。溫資料層是在硬碟與 QLC 之間選。短期黏著來自 2–3 年、少彈性的長約"},{"item":"價值鏈分配","level":"🟢","text":"STX 產品只占客戶資本支出低到中個位數，存資料比重算便宜得多（CFO 2026-09-10），客戶對漲價不敏感；供給端三家、顆數持平，磁頭碟片自製。風險在上游：主軸馬達約八成出自 Nidec，稀土精煉集中中國，可能分走漲價的好處"},{"item":"社會容忍度","level":"🟢","text":"B2B 賣給雲端大廠，沒有消費者或政治上的漲價天花板。政策風險在出口管制與關稅（2023 年被 BIS 罰 3 億美元並附五年暫緩拒絕出口令），不在價格容忍度"}],"roiic":"事實表未涵蓋（缺投入資本、折舊與營運資金變動）","reinvest_rate":"低：FY2026 資本支出 5.69 億美元、占營收 4.7%，同年自由現金流 31.05 億美元；扣除折舊後的淨再投資率事實表未涵蓋","endo_ceiling":25,"formula_note":"標準公式是增量 ROIC×再投資率，兩個輸入都缺。改用管理層在資本支出 4–6% 營收之內可達成的 EB 年增 mid-20%，當作量的內生上界（25%）。這家公司的成長大多來自單價與費用化的研發，不是資本再投資，所以超出上界的部分全數歸給單價"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","STX":45.58,"MU":72.57,"000660.KS":76.27,"005930.KS":57.48,"285A.T":null,"unit":"%"},{"metric":"營業利益率","STX":34.65,"MU":65.67,"000660.KS":68.04,"005930.KS":36.88,"285A.T":null,"unit":"%"},{"metric":"FCF 利潤率","STX":25.46,"MU":28.99,"000660.KS":47.8,"005930.KS":28.95,"285A.T":null,"unit":"%"},{"metric":"研發密度","STX":6.19,"MU":5.3,"000660.KS":4.93,"005930.KS":9.7,"285A.T":null,"unit":"%"}],"competitors":[{"name":"MU","gm":72.57,"om":65.67,"fcf_margin":28.99,"rd_intensity":5.3,"strategy_note":"記憶體同業，TTM 毛利率 72.6%，高 STX 約 27 個百分點；NAND 價格高是 STX 低容量段能漲價的原因，也是 QLC 替代的煞車","period":"TTM ending 2026-05-31（4季加總）"},{"name":"000660.KS","gm":76.27,"om":68.04,"fcf_margin":47.8,"rd_intensity":4.93,"strategy_note":"TTM 毛利率 76.3%；與 STX 合寫 KV cache 分層儲存白皮書，屬互補，不是直接競爭","period":"TTM ending 2026-06-30（4季加總）"},{"name":"005930.KS","gm":57.48,"om":36.88,"fcf_margin":28.95,"rd_intensity":9.7,"strategy_note":"TTM 毛利率 57.5%；NAND 端價格走向決定 QLC 對硬碟的替代速度","period":"TTM ending 2026-06-30（4季加總）"},{"name":"285A.T","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表缺營收，無法比較","period":"TTM ending 2025-12-31（3季加總）"}]},"growth":{"driver_mix":"量（EB 年增約 25%，靠單碟容量）＋價（每 EB 單價年增 10% 到 20% 以上）＋回購（CY2027 起加大）；無併購","runway_years":"不適用滲透率算法（成熟產品）；以合約可見度計約 2–3 年（到 CY2028）","runway_post_y5":"🟡","endo_ceiling_basis":"量的內生上界約 25%（管理層 EB 年增 mid-20% 目標，在資本支出 4–6% 營收內完成）；共識 FY2026A→FY2029E EPS 年複合約 71%，缺口約 46 個百分點歸因於單價帶動的毛利率擴張、利息下降與回購，依賴單價不回頭","segments":[{"item":"資料中心","value":"Q4 FY2026 營收 29 億美元，年增 57%，占 81%；出貨 195 EB，年增 43%；雲端大廠為主，企業 OEM 連 5 季成長"},{"item":"Edge IoT","value":"6.97 億美元，年增 20%，占 19%；非 nearline 出貨 23 EB，年減 10%，營收成長來自缺貨漲價與 NAND 偏貴"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"連 13 季擴張"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"EB 份額約 42–43%，持平"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"漲價同時總出貨 EB 年增 34%"},{"signal":"EPS 年複合比營收年複合高 5 個百分點以上","lit":true,"note":"共識 FY2026A→FY2029E EPS 年複合約 71%，遠高於營收成長；差距靠單價與毛利率"},{"signal":"自由現金流÷淨利連 2 年低於 0.75","lit":false,"note":"全年淨利事實表未涵蓋；Q4 自由現金流利潤率約 31%，未見轉換問題"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"1.5%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"QLC 在溫資料層有壓力，未見 TAM 萎縮，列威脅觀察"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"相反，年度端點分位全在頂部"},{"signal":"維持性資本支出占自由現金流超過 60%","lit":false,"note":"全年資本支出 5.69 億對自由現金流 31.05 億"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"仍在投資 HAMR 製程設備"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；現金先還債，CY2027 起轉回購與加股息，沒有需要拆解的併購報酬"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年唯一收購是 2025 年的 Intevac（全現金每股 4 美元），金額事實表未涵蓋，遠小於市值 5%，不適用","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q4 股息加回購約 2.83 億美元，年化約 11 億；以判斷日股價乘約 2.31 億稀釋股數估市值，回饋殖利率不到 1%，不論 10 年期殖利率多少都過不了（10 年期殖利率事實表未涵蓋）","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 單季 5,400 萬美元，占營收 1.5%、占 non-GAAP 營業利益 3.3%；相對市值的年化稀釋遠低於 1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2027E、FY2028E 共識）對照循環位置；商品循環型本該用股價淨值比，但事實表未涵蓋","peers":{"expanded":false,"reason":"事實表同業只有利潤率、沒有倍數，也沒有 WDC；估值錨改用自身前瞻倍數與循環位置"},"fwd_pe":25.6,"peg":0.36,"percentile_5y":100,"val_light":"🔴","val_light_derivation":"Base 五年價約 $715（FY2031E 55×13 倍），低於現價約 22%；機率加權的五年價也低於現價；本益比、股價營收比、EV/營收在年度端點裡都是最高（只有 3–4 個點，不是連續五年分位）；循環位置在晚段，所以判過貴","upside_short_pct":-18.0,"upside_mid_pct":-21.8},"trap_analysis":{"verdict":"🟡","label":"高峰獲利陷阱（中等）"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY2023 營收由 116.61 億美元掉到 73.84 億（−37%），non-GAAP 毛利率 21.1%、最差一季 17%，全年 GAAP 虧損 5.29 億，閒置產能費用 1.71 億；起因是雲端消化庫存、nearline 採購大減，產業 EB 出貨全年少約 29%。Coughlin 認為這波漲價可能是暫時的","assumption":"長約與顆數紀律讓這次不一樣","consequence":"2028 年單價回頭加上雲端暫停採購，EPS 在 FY2030 探底約 22，倍數壓到 11–12 倍，股價約 $240–300，較現價少約七成","ruling":"部分採納。長約少彈性、有取消費，下行會比 2023 淺，所以 Bear 定在 FY2030 EPS 約 22，不是虧損；但長約只鎖量，CY2028 以後不鎖價，機率給 30%。這條和唯一致命點是同一條因果鏈，CY2028 定價是它第一個看得到的事件","watch":"資料中心營收季增率、CFO 對訂單遞延的說法、每 EB 單價年增","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5","supply_demand_durability#3"],"fact_refs":["f_kpi13_price_per_exabyte_yoy","f_kpi15_nearline_exabyte_lta_bac"]},{"view":"論點成功但股東經濟變差","evidence":"需求照講的成長，但 WD 2027 年 HAMR 量產；STX 自己擴磁頭廠（報導稱近 3 倍，但面積數字是 1.1 萬到 1.9 萬平方呎，約 1.7 倍）；TDK 加磁頭產能。STX 漲價讓硬碟對 QLC 的每 TB 價差收窄，TrendForce 已看到缺貨把需求推向 QLC。上游主軸馬達約八成出自 Nidec，稀土精煉集中中國，漲價的好處可能被上游分走","assumption":"量成長時，單價與毛利率也守得住","consequence":"EB 照樣年增 20% 以上，但每 EB 單價轉跌、毛利率回到五成出頭，EPS 在 FY2029 見高約 58 後走平，低於共識 78.29","ruling":"採納，這就是 Base 情境：量說對了，價說錯了","watch":"CY2028 長約單價、WD HAMR 認證家數、管理層對外購零件成本的說法","evidence_refs":["substitute_technology#0","substitute_technology#3","substitute_technology#4","geo_supply_chain#5","geo_supply_chain#6","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1"],"fact_refs":["f_consensus_eps_fy3"]},{"view":"價格已反映太多","evidence":"現價 $914.72 是 FY2027E 共識的 25.6 倍、FY2029E 的 11.7 倍；股價營收比 17.07 倍，本益比、股價營收比、EV/營收在年度端點裡都是最高；26 週漲 121.5%；賣方 25 家、88% 偏多","assumption":"共識 EPS 一路兌現到 FY2029，而且市場之後還願意給高於循環常態的倍數","consequence":"就算共識全中、FY2029 給 12 倍，股價也只到約 $940，三年幾乎沒有報酬；要賺錢得 EPS 再超共識","ruling":"採納：價格已付清到 FY2029 的共識。反駁面是 Q4 營收與 EPS 都超過自己的財測上緣（EPS 5.71 對上緣 5.20），再超共識不是沒可能，這部分放在 Bull 三成","watch":"股價對 FY2027E、FY2028E 的前瞻倍數；共識修正方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_ps_current","f_ps_percentile","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy3","f_kpi4_non_gaap_diluted_eps"]}],"max_dd":{"lo":-75,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 747.3 → 本次 914.72（+22.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=747.3","side_b":"本次 price_at_dd=914.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"需求是結構性還是週期性","cause":null,"prior_field":null,"side_a":"結構性，也是現在就買的最強論證：nearline 大部分已配置到 CY2028，客戶要把規劃延到 2029 以後（CEO 2026-07-28）；CFO 2026-09-09 說供需缺口沒縮反而略擴，每次重談長約客戶都要更多量；Morgan Stanley 估缺口 2027–28 年擴大到約 400 EB；顆數持平的紀律讓這次不像以前","side_b":"週期性：Coughlin 認為這波漲價可能是暫時的；FY2023 營收一年少 37%、毛利率跌到 17–19%、全年虧損，就發生在上一個高峰之後；CFO 2026-09-09 自己承認這已不是循環起點，走了三年以上","ruling":"方向相反，不可調和，裁決拆開量與價。量的部分採結構性：合約、客戶規劃期延長、資料留存需求都有來源。價的部分採週期性：CY2028 以後的價格沒有入約，WD HAMR 與新磁頭產能剛好在那時到位。所以 FY2027 可信，FY2029 共識不可信；量的結構性給 Bull 三成機率","evidence_level":"管理層說法＋第三方轉述（Morgan Stanley 經社群轉載、Coughlin 僅標題）＋公司歷史財報","settle_metric":"CY2028 長約的每 EB 單價年增率（2027 年 4 月與 7 月法說）","if_then":["若 2027 年中 CY2028 長約確認每 EB 單價續漲，且資料中心 EB 年增 ≥20%：Bull 機率升到 40%，股價 ≤$760 時建首倉 1.5%","若每 EB 單價年增連 2 季 ≤0：維持不持有；已持有者清倉","反向（價格先走、證據未到）：股價續漲而 CY2028 價格未公布，不追；股價跌到 $644 以下而毛利率仍季增，分批反買首倉 1.5%"],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#3","end_markets#3","end_markets#5","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#4"]},{"axis":"HAMR 進度說法前後","cause":null,"prior_field":null,"side_a":"2026-04-28 CFO：FY2027 年底 nearline EB 七成在 HAMR（講到一半把 calendar '27 改成 fiscal '27）；2026-09-10 CFO：12 月前會到位，兩年後資料中心八到九成走 HAMR","side_b":"2026-07-28 CEO 被問七成目標時說 PMR 推得比原先想的多一點，並刻意放慢 Mozaic 4；CFO 2026-09-09 承認換代時 EB 季度波動會變大","ruling":"可調和，是程度差異：40% 里程碑如期達成，多推 PMR 是為了在 HAMR 製程週期較長時維持顆數。但七成目標的緩衝變小，列為第三個假設的第一個驗證點","evidence_level":"法說與會議逐字稿","settle_metric":"2027 年 7 月法說的 HAMR 占 nearline EB 比例","if_then":["若 2027 年 7 月 HAMR 占比低於 60%：Bull 機率降到 20%","若 ≥70% 且 Mozaic 5 如期送認證：假設成立，但估值仍是約束，不建倉"],"evidence_refs":["substitute_technology#5","end_markets#3"]},{"axis":"管理層定價口徑對照實際","cause":null,"prior_field":null,"side_a":"2026-04-28 CFO：資料中心每 TB 營收年增中個位數，預期延續；不對 FY2027 底的價格給指引","side_b":"6 月季每 EB 單價年增 10%，9 月季財測隱含約 20% 以上（Morgan Stanley 分析師推算，CFO 認同缺口擴大）；2026-09-10 CFO 說增量毛利率七成以上","ruling":"可調和：管理層口徑一向保守，實際跑贏。但四場會議被問到價格幅度與持續期時全部迴避、不給數字，市場無法驗證 CY2028 價格，這正是本次把唯一致命點放在 CY2028 定價的原因","evidence_level":"法說逐字稿","settle_metric":"每季每 EB 單價年增","if_then":["若 Q1 FY2027 每 EB 單價年增低於 15%：財測隱含的加速沒發生，Bull 機率降到 20%"],"evidence_refs":["end_markets#2","capital_markets_pricing#4"]},{"axis":"共識上修幅度的口徑","cause":null,"prior_field":null,"side_a":"事實表的 FY1 共識三個月上修 140.3%（14.89 到 35.78）","side_b":"24/7 Wall St. 同期 FY2027 共識由 26.58 上修到 35.78，約 +34.6%","ruling":"採 B 側：14.89 是財年換季前的 FY2026 估計（FY2026 實際 15.58），140% 是換年造成的，不是上修。同年度真實上修約 35%，仍然很強，但不要拿 140% 當動能證據","evidence_level":"兩個資料源對照","settle_metric":"下一次 Koyfin 快照同財年比較","if_then":["若下一次快照顯示 FY2027E 同財年再上修 10% 以上：Base 的 FY2027 上調到共識"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"結構轉好：三家供給、顆數持平、合約化（長約 2–3 年、少彈性、特定情況有取消費）","side_b":"競爭惡化在路上：WD 40TB ePMR 2026 下半年、HAMR 2027 量產，STX 與 TDK 擴磁頭產能；其他結構變數是 QLC 替代與出口管制、關稅","ruling":"雙向拉鋸：結構轉好目前佔上風（毛利率連 13 季擴張），競爭惡化要到 2027–2028 才到，替代技術與出口管制是尾端風險","evidence_level":"公司 10-K、同業新聞稿、第三方報導","settle_metric":"CY2028 長約單價與 WD HAMR 認證家數","if_then":["若 WD HAMR 在 2027 年底前於 2 家以上大型雲端量產：裁決改為競爭惡化中，已持有者減碼一半"],"evidence_refs":["channel_business_model_shift#1","channel_business_model_shift#3","substitute_technology#4","cyclical_supply_discipline_capacity#0","substitute_technology#0","reg_tariff_export#2"]},{"axis":"前份漂移：未變欄位","cause":"價格變動","prior_field":["dca_verdict","dca_role","signal","trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份（2026-07-29，股價 $747.3）：觀望、訊號 B、陷阱風險中等、護城河持平、五年後跑道中等、循環商品型","side_b":"本次（股價 $914.72）：以上判斷不變","ruling":"股價漲約 22%，FY2027 EPS 基數只從指引隱含約 34 升到共識 35.78（約 +5%）。Q4 超標與 Q1 財測是真的好消息，但已被價格吃掉，所以裁決輸入與商業判斷都不變","evidence_level":"事實表價格與共識","settle_metric":null,"if_then":[],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"前份漂移：情境價格與報酬","cause":"新證據","prior_field":["bull_5y_price","bear_5y_price","asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份：Bull 五年價 $1,200、Bear $144、報酬不對稱 1.1、五年期望報酬 −6.3%、Base 年化 −3.5%","side_b":"本次：Bull 約 $1,620（FY2031E 108×15 倍）、Base 約 $715（55×13 倍）、Bear 約 $300（25×12 倍）；不對稱、期望報酬與年化由程式重算","ruling":"Q4 EPS 5.71 超過財測上緣 5.20，Q1 FY2027 財測 7.30，加上 CY2027 規格與價格已入約，三條路徑整體上移。Bear 底部抬高，是因為 FY2027 幾乎沒有下行空間（CFO 說手上有 4–5 季訂單）","evidence_level":"公司財報與財測","settle_metric":null,"if_then":[],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#4","end_markets#0"]},{"axis":"前份漂移：機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 30%、Bear 25%；最大回撤單點 −75%","side_b":"本次：Bull 30%、Base 40%、Bear 30%；最大回撤改為 −50% 到 −75% 的區間","ruling":"共識 EPS 三年年複合約 71%，遠超量的內生上界約 25%，Bear 機率不低於 30%；回撤改用區間，把 Base 下市場提前殺倍數的情況也算進來","evidence_level":"情境樹規則","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份估值結論：偏貴","side_b":"本次估值結論：過貴","ruling":"前瞻本益比由約 22 倍（$747.3÷約 34）升到約 25.6 倍；Base 五年價約 $715 低於現價，機率加權也低於現價","evidence_level":"事實表價格與共識","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"前份：中循環","side_b":"本次：晚循環","ruling":"三件事改變：毛利率從 47% 升到 52.7%，9 月季財測隱含再升；每 EB 單價年增由 10% 加速到約 20% 以上；新產能開始宣布（STX 擴磁頭廠、TDK 加產能，12–18 個月後到位）。CFO 2026-09-09 也承認已不是循環起點。商品循環六訊號中毛利率與量價關係偏賣，供給紀律與庫存中性，情緒未到狂熱（賣方均價仍高於現價），股價淨值比事實表未涵蓋；多數決落在晚段","evidence_level":"財報＋法說＋第三方產能報導","settle_metric":null,"if_then":[],"evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","end_markets#2","capital_markets_pricing#0"]},{"axis":"前份漂移：重新評估價位","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"$505-630（16-18x FY2027 指引隱含 EPS ~$34，即前份 $400-500 門檻按 EPS 基數 +26% 平移）；或循環位置由中轉早","side_b":"股價回到 $572–644（FY2027E 共識 35.78 的 16–18 倍）即重跑研究；此價位之前不建倉","ruling":"倍數法不變（FY2027E 的 16–18 倍），EPS 基數由指引隱含約 34 換成共識 35.78，區間上移到 $572–644。拿掉「循環位置由中轉早」，因為現在已是晚循環；改成單一價格約束，觸發後先重跑研究，不直接建倉","evidence_level":"事實表共識","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"CY2028 年度 build-to-order 合約的新約每 EB 單價年增率轉負（預計 2027 年第二到第三季談定）","ruling":"前份把風險拆成三條並列，沒有指出哪一條數學上最敏感。共識 FY2026A→FY2029E EPS 年複合 71% 裡，約六成五靠單價，所以 Single Thing 定在 CY2028 定價；發生即清倉","evidence_level":"情境樹敏感度","settle_metric":"CY2028 新約每 EB 單價年增率","if_then":[],"evidence_refs":[]},{"axis":"清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標（空白）","side_b":"每 EB 單價年增連 2 季 ≤0（清倉）；non-GAAP 毛利率連 2 季季減且低於 52%（減碼一半）；資料中心 EB 年增連 2 季低於 15%（減碼一半）；WD HAMR 在 2027 年底前於 2 家以上大型雲端量產（減碼一半）","ruling":"前份只有進場價，沒有持有後的退出線；本次補上四條，各自對應情境樹的 Bear 路徑","evidence_level":"情境樹規則","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q1 FY2027 財報：毛利率是否照承諾逐季上升","type":"假設驗證","maps_to":"H2","metric":"non-GAAP 毛利率（季）","threshold":"低於 Q4 的 52.7%（季減）","action":"第二個假設削弱，Bull 機率降到 20%；未持有者不動作","source_freq":"每季財報新聞稿","date":"2026-10"},{"n":2,"text":"股價回到 FY2027E 共識的 16–18 倍","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤$644（35.78×18）","action":"重跑完整研究；通過後建首倉 1.5%","source_freq":"每日收盤","date":null},{"n":3,"text":"CY2028 長約定價","type":"Single Thing","maps_to":"H2","metric":"新長約每 EB 單價年增率","threshold":"≤0%","action":"移出觀察名單；已持有者清倉","source_freq":"2027 年 4 月與 7 月法說","date":"2027-07"},{"n":4,"text":"HAMR 七成目標","type":"假設驗證","maps_to":"H3","metric":"HAMR 占 nearline EB 比例","threshold":"2027 年 6 月底 ≥70%；低於 60% 即削弱","action":"低於 60%：Bull 機率降到 20%","source_freq":"每季法說","date":"2027-07"},{"n":5,"text":"WD HAMR 在大型雲端量產","type":"風險","maps_to":"R1","metric":"WD HAMR 完成認證並量產的大型雲端家數","threshold":"≥2 家，且早於 Mozaic 5 送認證","action":"已持有者減碼一半；未持有者 Bear 機率升到 40%","source_freq":"WD 季度法說與新聞稿","date":"2027-06","evidence_refs":["substitute_technology#4"]},{"n":6,"text":"供應鏈或出口管制卡住出貨","type":"風險","maps_to":"R3","metric":"單季營收對財測下緣","threshold":"低於下緣，且公司把原因歸給零件、稀土、出口管制或關稅","action":"已持有者減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#5","geo_supply_chain#6","geo_supply_chain#8","reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","major_events#1"]},{"n":7,"text":"雲端消化庫存","type":"風險","maps_to":"R4","metric":"資料中心營收季增率；CFO 對訂單的說法","threshold":"季減，或提到訂單遞延","action":"已持有者清倉；未持有者等循環位置轉回早段","source_freq":"每季財報與法說","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5"]},{"n":8,"text":"證券集體訴訟和解最終聽證","type":"風險","maps_to":"R3","metric":"法院是否最終核准 1.75 億美元和解","threshold":"未核准","action":"核准則結案、不動作；未核准則把超出 1.75 億美元的求償列進 Bear 情境","source_freq":"和解網站、8-K","date":"2026-11-17","evidence_refs":["lawsuit_class_action#0","major_events#0"]},{"n":9,"text":"下次複審","type":"複審日期","maps_to":null,"metric":"Q1 FY2027 財報與 Q2 財測","threshold":"財報公布後一週內","action":"更新情境路徑與機率","source_freq":"每季","date":"2026-10"}],"kill_metrics":[{"metric":"新長約每 EB 單價年增率","bear_threshold":"連 2 季 ≤0%（清倉）","window":"2026Q4–2028Q2","source":"每季法說 Q&A（分析師轉述、CFO 確認）","last_status":"ok"},{"metric":"non-GAAP 毛利率","bear_threshold":"連 2 季季減且低於 52%（減碼一半）","window":"FY2027–FY2028","source":"公司財報新聞稿","last_status":"ok"},{"metric":"資料中心 EB 出貨年增率","bear_threshold":"連 2 季低於 15%（減碼一半）","window":"FY2027–FY2028","source":"CFO 法說準備稿","last_status":"ok"},{"metric":"WD HAMR 量產的大型雲端家數","bear_threshold":"2027 年底前 ≥2 家（減碼一半）","window":"2027","source":"WD 新聞稿與法說","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方均價 $1,125 等於 FY2028E 約 20 倍、FY2029E 約 14 倍，隱含每 EB 單價到 CY2029 仍在漲；但 CY2028 價格尚未入約，WD HAMR 2027 量產、磁頭擴產 12–18 個月後到位，單價漲勢在 FY2029 前收斂的機率被低估"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🔴', moat_trend='→', week26=121.52, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"目前 0%；日後進場上限 3%","requires_critic":[],"rearm_trigger":"股價回到 $572–644（FY2027E 共識 35.78 的 16–18 倍）即重跑研究；此價位之前不建倉","exec_line":"不建倉、不追價。約束只有一個：價格已付清共識到 FY2029 的單價漲勢。股價回到 $572–644 重跑研究；若 2027 年中 CY2028 長約確認單價續漲，股價 ≤$760 也重跑。"},"reasoning":{"industry":"Q4 FY2026 營收 36.29 億美元，年增 48.5%。資料中心 29 億美元，占 81%；Edge IoT 6.97 億美元，占 19%。出貨 218 EB，其中資料中心 195 EB。non-GAAP 毛利率 52.7%、營業利益率 44.6%，兩者都是紀錄。每 EB 營收約 1,660 萬美元，季增 6.5%；每 EB 單價年增 10%，9 月季財測隱含約 20% 以上。公司策略是顆數持平、靠 HAMR 提高單碟容量，所以量的成長上限約每年 25%，超出的部分全看單價。產業時鐘在過熱段：大部分 nearline 產能已配置到 CY2028，毛利率連 13 季擴張，而新產能（STX 與 TDK 擴磁頭、WD HAMR）要到 2027–2028 才到。單點依賴有兩處：最大客戶約占營收 14%，資料中心以雲端大廠為主；上游主軸馬達約八成出自 Nidec，磁鐵用稀土的精煉約九成在中國。","moat":"機制是三家寡占，加上 HAMR 技術與自製磁頭、碟片、雷射的垂直整合。執行力給 8 分：40% HAMR 里程碑如期達成，Mozaic 3 在所有主要雲端認證，Mozaic 4 在最大兩家放量。定價能力給 7 分：三年內從價格接受者變成能定價，但這是缺貨撐起來的，CY2028 以後的價格沒有入約。合計落 B。方向判持平：份額沒動——2025 年 EB 份額 STX 約 42%、WD 約 47%，本季 STX 出貨 218 EB 對全產業 Q2 的 504.3 EB 約 43%；定價能力在擴大，但屬週期；執行力穩定。同業表沒有 WD，無法算 ROIC 差距；記憶體同業毛利率 57–76%，STX TTM 45.6%，說明它還不是最能定價的那一種。","growth":"成長來源是量（EB 年增目標 mid-20%，靠單碟容量，不加顆數）加上價（每 EB 單價年增 10% 到 20% 以上），再加 CY2027 起加大的回購；沒有併購。共識 EPS 由 FY2026A 的 15.58 到 FY2029E 的 78.29，年複合約 71%。量的內生上界約 25%，缺口約 46 個百分點，歸因於單價帶動的毛利率擴張、還債後利息下降與回購，其中單價占大頭。實體 AI、KV cache 被管理層提為下一波需求，但 CEO 自己說還很早期、沒有量化，不算第二條曲線。衰退訊號十項亮一項（EPS 成長遠高於營收成長）。","governance":"Q4 自由現金流 11.18 億美元，利潤率約 31%；FY2026 全年 31.05 億美元。資本支出占營收 4.7%，維持 4–6% 區間。債務由年初約 50 億降到 36 億，9 月季末再降到約 24 億，淨槓桿 0.4 倍，剩一筆高利率票據。Q4 以股息加回購回饋約 2.83 億美元，相對市值不到 1%。SBC 占營收 1.5%，稀釋很低。主要風險是 CY2027 起加大的回購，會在倍數最高、循環最熱的時候買進。","valuation":"現價 $914.72 是 FY2027E 共識 35.78 的 25.6 倍、FY2028E 55.37 的 16.5 倍、FY2029E 78.29 的 11.7 倍。對循環股來說，11.7 倍已接近高峰獲利常見的倍數，等於市場把共識算到 FY2029，還給了高峰倍數。要划算，得是 FY2029 之後單價還守得住，或 EPS 再超共識。賣方均價 $1,125 高於現價約 23%，但同期 FY2027 共識三個月內上修約 35%，目標價是跟著 EPS 走，不是獨立證據。PEG 約 0.36 看似便宜，但分母是高峰單價，不採用。股價營收比 17.07 倍、EV/營收 17.25 倍，年度端點分位都在最高。","premortem":"三個反證視角寫在反證紀錄。陷阱風險中等：衰退訊號只亮一項，公司本身沒有問題，問題在估值用的分母。上一個高峰之後的 FY2023，營收一年少 37%、毛利率掉到 17–19%、全年虧損。這次有長約和顆數紀律，下行會比較淺，但不會沒有。股價 26 週已漲 121.5%。"},"plain":{"six":{"how_it_makes_money":"賺雲端大客戶買大容量硬碟的錢，錢卡在每 EB 單價：出貨顆數不增，營收靠單碟容量和漲價","moat":"護城河方向持平：HAMR 領先是真的，但還沒變成份額，2027 年 WD 會追上來","growth":"跑道中等：資料量長期成長有依據，但五年後沒有已證實的第二條曲線，EPS 成長主要靠單價","capital":"資本配置合理但回饋偏小：先還債到投資等級，CY2027 起才大量回購，而回購會落在循環高檔","valuation":"現價要求共識一路兌現到 FY2029，也就是每 EB 單價再漲三年；我只給三成機率，所以過貴","how_wrong":"最可能看錯的是把高峰單價當成新常態：遠期本益比看起來便宜，是因為分母假設單價再漲三年"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方均價 $1,125 等於 FY2028E 約 20 倍、FY2029E 約 14 倍，隱含每 EB 單價到 CY2029 仍在漲；但 CY2028 價格尚未入約，WD HAMR 2027 量產、磁頭擴產 12–18 個月後到位，單價漲勢在 FY2029 前收斂的機率被低估","momentum_overheated":false,"cycle_gates_pass":false,"trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":914.72,"week26_return_pct":121.52,"consensus_rev_3m_pct":140.3,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2028E–FY2029E 共識 EPS 建立在每 EB 單價再漲兩到三年；用遠期本益比說便宜的論證不成立，估值改看 FY2027E（價格已入約）與情境機率"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報與 Q2 財測","impact":"高","watch":"毛利率是否季增、每 EB 單價年增是否約 20% 以上"},{"date":"2026-11-17","date_precision":null,"type":"other","event":"證券集體訴訟 1.75 億美元和解最終聽證","impact":"低","watch":"法院是否核准"},{"date":"2026-11","date_precision":"month","type":"other","event":"年度股息檢討（CFO 說強勁時期通常會加）","impact":"低","watch":"加幅與回購節奏"},{"date":"2026-12","date_precision":"month","type":"product","event":"Mozaic 4 占 HAMR EB 過半的里程碑","impact":"中","watch":"2027 年 1 月法說是否確認達成"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"WD HAMR 客戶認證與量產","impact":"高","watch":"大型雲端認證家數"},{"date":"2027-07","date_precision":"quarter","type":"guidance","event":"CY2028 長約定價談定","impact":"高","watch":"新約每 EB 單價年增是否轉負"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"Mozaic 5（50TB）送客戶認證","impact":"中","watch":"是否如期"}],"_projected_from":"v19"}
```
