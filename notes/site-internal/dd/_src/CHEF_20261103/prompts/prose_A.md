你是 stock-analyst v20 的**散文層（prose）agent**，標的 CHEF（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CHEF_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：CHEF　日期：2026-11-03　archetype：None　前份裁決：2026-05-18　衛星候選 — Specialty B2B 食材分銷利基龍頭，Q1 FY26 organic +10.4% 連續第 4 季雙位數，但 Fwd PE 30.74x 溢價同業 128% 已透支；建議等回測 W52 $64 或 Sysco-Restaurant Depot 整合落地 (FY27Q1-Q2) 後再評估進場｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2039B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（613B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（708B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1236B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1332B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（411B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（941B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2063B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4296B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2084B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（284B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2039           3473-4961      5 條（2–6 內）  
s3                  8000         613           5171-7387      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3276          8207-11724      5 條（2–6 內）  
s6                 11000         411          7412-10589      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         941           1791-2559      5 條（2–6 內）  
s10                 5000        2063           2056-2937      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2084           2000-2916      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         284            851-1216      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4561B；至少需散文≈40.44KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−60
−58%
−52%
−40
−40%
−9%
−5.5
0
0.06
0.39%
0.4%
0.5
0.64
0.64%
0.65%
0.66
0.75
0.9
1%
1
01
1.02
1.085
1.09
1.10
1.157
1.16
1.17
1.19
1.21
1.31%
1.39
1.4
1.5
1.50%
1.5%
1.531
1.68
1.7
1.79
1.87
1.98%
2%
2.00%
2.0
02
2
2.14
2.2
2.29%
2.36%
2.4%
2.5
2.52
2.57
2.6%
2.6
2.60
2.61
2.7
2.75
2.85
2.87
03
3.00
3%
3
3.01
3.02
3.07
3.2
3.23%
3.28%
3.3%
3.55
3.65
3.66%
3.85
4
4%
4.03%
4.05
4.1%
4.3%
4.32%
4.4%
4.485
4.5%
4.5
4.55
4.95
05
5%
5
5.2
5.3
5.5
5.7%
5.8
6
6%
06
6.05
6.1%
6.2
6.3%
6.5%
6.6%
6.65%
6.75
7
7.0%
7%
07
7.2%
7.3%
7.5%
7.5
7.81
8%
8
09
9
9.0%
10%
10
10.3%
10.4%
11%
11
11.2%
11.35
11.4
11.9
11.93%
12
12%
12.1%
13
14%
14
15%
15
15.36
17
17%
17.4
17.55%
17.8%
18%
18
18.1%
18.1
18.5%
18.50%
19.2%
20%
22%
23.67%
24
24.5%
24.66%
24.7%
25%
25
25.0%
26
27
27%
28
28.9
29
29.5%
30
30%
30.74
31%
31
31.2%
32%
33%
34
34.3
34.34
34.4
35%
35.16
38%
40%
40
41
41.02
42
43
43.5
43.65
44
44.5
44.8%
45
45.24
45.6
45.8
46.1
49
50%
51
52
58
60
60%
63
$64
64
65
70
75
80.34
82
83.15
84
90%
90
92
94%
100%
100
104.71
105.41
107.43
116.56
122
124
125
137
141
150%
155
181.5
270
500
930
2025
2026
2027
2028
2029
2030
2031
2033
20261103
2,408
2,540
4,581
5,000
5,150
6,740
8,570
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
{"meta":{"ticker":"CHEF","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"The Chefs' Warehouse, Inc."},"oneliner":"高端餐廳食材配送利基商，有機成長連續雙位數、EBITDA 率提早兩年到 7%，生意比半年前更好；但股價約 41 倍今年獲利，基本情境五年年化僅約 3%，不追，等股價回到明年獲利約 27 倍再動作。","thesis":{"H":[{"id":"H1","text":"CHEF 靠擴編業務員、新增品項與新市場持續搶份額，有機營收成長守在公司 2030 目標區間 7–10% 以上。","2y":"FY2027 有機成長 ≥8%，不重複客戶（排除中東）年增 ≥3%","5y":"FY2030 營收達 60–65 億美元","10y":null,"threshold":"TTM 有機營收成長 ≥7%；不重複客戶（排除中東）年增 ≥3%","source":"每季 8-K 新聞稿與法說：有機成長、specialty 箱數、不重複客戶、品項配置","drift_rule":"兩年期：TTM 有機成長連 2 季低於 6.65%（偏離門檻 5%）為削弱，連 3 季低於 6.3%（偏離 10%）為反轉"},{"id":"H2","text":"產品組合、採購規模與數位定價讓毛利率續升，調整後 EBITDA 率由 FY2026 約 7.0% 走到 FY2030 的 7.5–8%。","2y":"FY2027 調整後 EBITDA 率 ≥7.0%，毛利率年增不為負","5y":"FY2030 調整後 EBITDA 率 ≥7.5%","10y":null,"threshold":"TTM 調整後 EBITDA 率 ≥7.0%；TTM 毛利率 ≥24.5%","source":"每季 8-K 新聞稿（毛利率、調整後 EBITDA）與年度財測","drift_rule":"五年期：TTM 調整後 EBITDA 率連 4 季低於 6.65%（偏離 5%）為削弱，連 6 季低於 6.3%（偏離 10%）為反轉"},{"id":"H3","text":"資本配置照公司計畫：淨槓桿維持 1.5–2.5 倍、自由現金流達調整後 EBITDA 的 40–60%、全稀釋股數逐年下降，不做稀釋性的大型併購。","2y":"FY2027 稀釋股數 ≤43m，年底淨負債÷調整後 EBITDA ≤2.0 倍","5y":"FY2030 前股數不增、淨槓桿 ≤2.5 倍","10y":null,"threshold":"淨負債÷調整後 EBITDA ≤2.5 倍；年度 FCF ÷ 調整後 EBITDA ≥40%；FY2027 稀釋股數 ≤43m","source":"季報資產負債表、法說淨負債與股數指引、年報現金流量表","drift_rule":"兩年期：淨槓桿連 2 季超過 2.5 倍，或年度 FCF 轉換低於 38%（偏離 5%）為削弱；淨槓桿連 3 季超過 2.75 倍為反轉"}],"R":[{"id":"R1","text":"競爭與科技拉平：換配送商成本低，US Foods、新創 Pepper 用 AI 下單降低主廚對業務員的依賴，大型綜合配送商擴張自取倉，CHEF 新客戶成長放慢、毛利率溢價縮小。","h_ref":"H1","clock":"🔥","threshold":"不重複客戶（排除中東）年增連 4 季 <2%，或毛利率連 2 季年減","evidence_refs":["competitive_share_entrants#1","substitute_technology#1"]},{"id":"R2","text":"高端外食景氣下行：業務集中在特定城市的高端餐飲市場，Q3 已見部分會議參加人數少 10–12%、俱樂部單點餐偏軟（CEO 2026-10-28）；若擴散，箱數成長會先掉。","h_ref":"H1","clock":"⚡","threshold":"有機營收成長連 2 季 <5%，或 specialty 箱數年增轉負","evidence_refs":["geo_supply_chain#1"]},{"id":"R3","text":"成本吸收失敗：供應商多無長期合約、公司不避險食品價格，燃料自 3 月大漲只轉嫁大部分；供應商食安違規也可能中斷供貨，利潤率擴張停下。","h_ref":"H2","clock":"🔥","threshold":"毛利率年減且調整後費用率高於 18%（Q3 17.8%）連 2 季","evidence_refs":["reg_tariff_export#0","geo_supply_chain#3"]},{"id":"R4","text":"中東業務：衝突讓 5–6 月營收一度只有去年同期約 94%，Q3 回到約 100%；12 月是當地旅遊旺季，管理層已在財測裡放保守假設。","h_ref":"H1","clock":"⚡","threshold":"中東營收回落到去年同期 90% 以下，或 Q4 實際營收使全年低於財測下緣 45.6 億","evidence_refs":[]},{"id":"R5","text":"高端外食結構性萎縮（前份提出減重藥物與餐飲業成熟化），市場長期成長由約 4% 再往下，搶份額也撐不住 7%。","h_ref":"H1","clock":"🐢","threshold":"跨 2 個年度 specialty 箱數年增 <3%","evidence_refs":[]}],"single_thing":{"description":"有機營收成長首次跌破 7%（公司 2030 目標下緣）的那一季財報；同義事件是 FY2027 全年財測營收中位數隱含的有機成長低於 7%。","why_fatal":"現價約 41 倍今年 EPS、34 倍明年共識，等於假設兩位數有機成長再走幾年；成長跌破 7% 代表搶份額的引擎降速，倍數往 25 倍以下收斂。以 FY2027E 共識 EPS 3.07 計，本益比每少 5 倍約少 15 美元（約 15%），倍數壓縮的影響大於任何單一年度的 EPS 落差。","if_happens":"不攤平；若同季毛利率也年減，持有者減碼一半，連 2 季清倉；若毛利率仍升、只是通膨回落拉低價格成長，改看箱數成長是否 ≥4%，是則維持觀望不動作。","how_monitor":"每季 8-K 的有機營收成長、specialty 箱數、不重複客戶；2027 年 2 月 Q4 財報與 FY2027 財測。","probability":"約 30%（12–24 個月）：Q3 有機 10.3% 中約 4pp 來自通膨，管理層預期通膨回到 1–4% 常態區間；若通膨降到 2%、量成長由約 6% 放慢到 5%，有機成長就落在 7% 左右。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":34.34,"peg_fy2":1.79,"stress":{"pass":8,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":1.68,"FY2026E":2.57,"FY2027E":3.07,"FY2028E":3.65},"fy_end_month":12,"eps_basis":"共識為 Koyfin 2026-10-31 快照（家數未載，推定調整後口徑）；FY2025A 1.68 是 GAAP 稀釋 EPS（年度財報，yfinance），事實表沒有調整後基期，以此算三年 CAGR 29.5% 會高估，FY2026E→FY2028E 年化 19.2% 較乾淨；FY2026 GAAP 淨利指引 1.085–1.10 億與 2.57 同量級。財年結束於 12 月下旬（FY2025 為 2025-12-26）。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CHEF_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"低毛利、高周轉的利基配送商：毛利率約 25%、營業利益率約 4–5%，成長靠擴編業務員、新增品項與新配送中心搶份額，需求跟著高端外食景氣走。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久為主、帶景氣循環：Q3 specialty 箱數 +6.1%、不重複客戶 +4.4%（8-K 2026-10-28）；10-K（2026-02-24）承認進入門檻與轉換成本低，供給可逆性高。","bargaining":{"up":"上游是 40 多國的小型產地與工匠，分散；但多無長期供貨合約、公司不避險食品價格，成本急漲時只能轉嫁大部分。","down":"下游前十大客戶約占 FY2025 營收 6%，單一客戶無議價力；但換配送商成本極低，客戶用腳投票的成本也低。","geo":"配送中心在美國、加拿大與中東，自 40 多國進口；中東 Q3 營收約為去年同期 100%，12 月旅遊旺季仍有不確定。"},"profit_pool_dir":"利潤往有採購規模、數位定價與 AI 下單能力的配送商集中（CHEF 與 US Foods 都在投入），沒有規模的地方小配送商被擠壓；但新創 Pepper 正替獨立配送商補科技（2026-02），集中速度未定。","tam_table":[{"item":"美國 food logistics 市場（代理，非 foodservice 專屬）","value":"2026 年約 2,408 億美元，年增約 4.3% 至 2031（Mordor）"},{"item":"specialty foodservice 配送 TAM／SAM","value":"事實表未涵蓋"},{"item":"CHEF FY2026 營收（公司財測）","value":"45.6–46.1 億美元"},{"item":"CHEF 市占／滲透率","value":"事實表未涵蓋；前份摘要寫 specialty 利基市占 8–12%，未經本期核對"},{"item":"營業利益池占比 5 年前→現","value":"事實表未涵蓋"}]},"moat":{"mechanism":"採購廣度（約 9 萬品項、40 多國）＋主廚顧問型業務員＋高端城市市場的路線密度；客戶買的是找得到、送得準、有人懂，而不是最低價。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：毛利率 FY2022 23.67% → TTM 24.66%，Q3 再 +84bp；品項配置 +7.2% 快於客戶 +4.4%，代表既有客戶買得更多。定價面穩定：燃料只轉嫁大部分（CFO 2026-10-28），specialty 通膨僅 2.6%，Q3 毛利率提升有一部分是燃料轉嫁墊高。同業利益率歷史事實表未涵蓋，無法證明利差擴大；市占提升只有公司自述，沒有第三方數據。兩者合併判穩定。","peer_na_reason":null,"threats":[{"level":"🟡","text":"換配送商成本極低、進入門檻低、沒有獨家合約（10-K 2026-02-24），競爭者可用降價搶客；屬長期存在的結構弱點，不是新出現的攻擊。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"綜合配送商（US Foods MOXē）與新創（Pepper）用 AI 下單降低主廚對業務員建議的依賴，點對點攻擊 CHEF 的差異化。","p":"25%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"大型綜合配送商擴張自取倉（前份提出 Sysco 與 Restaurant Depot 整合，本期事實表未收錄進度），爭奪小型獨立餐廳；Q3 有機 10.3% 尚未看到影響。","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是主廚、決策者是主廚或老闆、付款者是餐廳，三角色一致；但最終需求是高所得消費者的外食，屬想要而非需要，可延後。讀數：Q3 specialty 箱數 +6.1%、不重複客戶 +4.4%，同時 CEO 提到部分會議參加人數少 10–12%。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一品項層看：主廚可以把某一類食材改向地方小配送商買，10-K 承認換配送商成本極低；CHEF 的抵抗力是品項廣度（約 9 萬品項）讓主廚一張單買齊，Q3 品項配置 +7.2% 快於客戶成長。漲價後流失率事實表未涵蓋（Q2 CFO 稱流失率與過去相比無重大變化）。"},{"item":"價值鏈分配","level":"🟢","text":"上游是 40 多國的小型產地，下游是前十大僅約 6% 的分散餐廳，兩端都分散，CHEF 站在整合者位置拿到較多利潤：毛利率 24.66% 對綜合配送同業 11.9–18.5%。弱點是無長期供貨合約、不避險，成本急漲時只能轉嫁大部分。"},{"item":"社會容忍度","level":"🟢","text":"高端食材不是民生必需品，社會對其價格的敏感度低，也不依賴監管授權；相關法規只有一般食安規範，近 12 個月 8-K 沒有訴訟、重編或調查項目。"}],"roiic":"事實表未涵蓋投入資本，無法算增量 ROIC；代理：FY2022→FY2025 營業利益由約 8,570 萬增至 1.531 億美元（營收×營業利益率），增量營業利益約 6,740 萬對增量營收 15.36 億，增量營益率 4.4%，高於 FY2022 的 3.28%，方向為正。","reinvest_rate":"帳上再投資率低：FY2024、FY2025 自由現金流÷淨利分別 1.87、1.21 倍，資本支出約營收 1%（CFO 2026-07-29）；成長的主要投入是費用化的業務員與科技支出，以及以負債支應的收購（金額事實表未涵蓋），所以「增量 ROIC×再投資率」在這家公司會失真。","endo_ceiling":10,"formula_note":"代理值，非增量 ROIC×再投資率直接計算：不加槓桿下能自籌的有機營收成長約 10%（前三季有機約 11%、Q3 10.3%，同期自由現金流為正、淨槓桿 1.4 倍），利潤率不變時營業利益內生成長上界約 10%。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","CHEF":24.66,"SYY":18.5,"USFD":17.55,"PFGC":11.93,"unit":"%"},{"metric":"營業利益率","CHEF":4.32,"SYY":3.66,"USFD":3.23,"PFGC":1.31,"unit":"%"},{"metric":"FCF 利潤率","CHEF":4.03,"SYY":2.29,"USFD":2.36,"PFGC":1.5,"unit":"%"}],"competitors":[{"name":"SYY","gm":18.5,"om":3.66,"fcf_margin":2.29,"strategy_note":"規模最大的綜合配送商，毛利率與營業利益率都低於 CHEF；前份提到其併購 Restaurant Depot 擴張自取倉，本期事實表未收錄進度，攻擊面在小型獨立餐廳的常規品項。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"USFD","gm":17.55,"om":3.23,"fcf_margin":2.36,"strategy_note":"2026 年擴大 MOXē AI 下單並改業務員薪酬，用數位化爭份額，直接挑戰 CHEF 自認的業務員與科技優勢。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"PFGC","gm":11.93,"om":1.31,"fcf_margin":1.5,"strategy_note":"四家中毛利率與營業利益率最低，定位離高端 specialty 最遠，對 CHEF 的直接威脅最小。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量約六成（specialty 箱數 +6.1%、肉品磅數 +6.6%）、價約四成（淨通膨 4.1%）、收購 0.9pp；EPS 再加利潤率擴張與股數下降。","runway_years":"事實表未涵蓋 CHEF 市占與滲透率，無法計算到 30% 滲透率的年數","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段報酬持續期的內生成長代理值約 10%（有機營收自籌成長上界，利潤率不變），不另算。","segments":{"expanded":false,"reason":"資料缺口：specialty 與 center-of-the-plate 只有成長率與毛利率變動，營收金額與利潤占比事實表未涵蓋；組合效應已在毛利率段落處理。"},"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 +49bp、Q3 +84bp"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"公司稱持續提升，無第三方份額數據"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"淨通膨 4.1% 下箱數仍 +6.1%"},{"item":"EPS 成長顯著高於營收成長（差 >5pp）","lit":true,"note":"FY2026E→FY2028E 共識 EPS 年化 19.2% 對 FY2027 共識營收 +9.0%"},{"item":"FCF÷淨利 <0.75 連 2 年","lit":false,"note":"FY2024 1.87、FY2025 1.21"},{"item":"SBC÷營收 >5% 且上升","lit":false,"note":"FY2026 SBC 指引 29–30m，約營收 0.64%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"food logistics 代理年增約 4.3%；未見直接替代技術"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"item":"維修性資本支出占 FCF >60%","lit":false,"note":"前九個月資本支出 2,540 萬對 FCF 1.157 億，全數視為維修也只約 22%"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"德州、新英格蘭、拉斯維加斯擴建中"}],"trap_rating":"價值陷阱風險 🟡（亮 1 項）；長期成長性 🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長以有機為主（Q3 收購只貢獻 0.9pp），不是靠併購撐；逐年現金去向事實表未涵蓋。"},"sbc":{"fy2026_guide":"29–30m","pct_of_revenue":0.64,"q3_pct_of_gaap_oi":18.1},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"收購金額與收購後利潤事實表未涵蓋；近 12 個月無新併購，Italco 簽於 2025-10-01，Q3 收購貢獻營收 0.9pp。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"Q3 未揭露買回金額與均價；以現價 105.41、FY2026E EPS 2.57 計，買回盈餘殖利率約 2.4%，10 年期殖利率事實表未載，但只要高於約 0.4% 就低於門檻。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY2026 SBC 指引 29–30m ÷ 市值 4,581m ≈ 0.64%／年，低於 1.5%；FY2027 稀釋股數指引 42–43m 低於 Q4 2026 的 43–43.5m。","grade":"過"}]},"valuation":{"basis":"Fwd P/E（分母 FY2026E 共識 EPS 2.57）配 PEG；P/S、EV/S 作對照","tier":"高成長利基配送，與綜合配送同業不同層，同業倍數只作終端下緣參考","peers":{"expanded":false,"reason":"同業前瞻本益比事實表未涵蓋（只有同業利潤率）；前份摘要寫同業 14–18 倍，未經本期核對，只用作 Bear 終端倍數參考。"},"fwd_pe":41.02,"peg":2.14,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"Fwd PE 41.02 倍；PEG＝41.02 ÷ FY2026E→FY2028E 共識 EPS 年化 19.2%＝2.14（>2 為貴；若用 GAAP FY2025A 基期三年 29.5% 得 1.39，但基期口徑不同、高估成長）；P/S、EV/S 在近 4 個年度端點最高；基本情境五年年化約 3%，低於 8%。四項都指向偏貴，結論為紅。","upside_short_pct":-5.5,"upside_mid_pct":17.4},"trap_analysis":{"verdict":"🟡","label":"生意無陷阱跡象，風險在價格"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"10-K（2026-02-24）承認換配送商成本極低、進入門檻低、沒有獨家合約；業務集中在特定城市的高端餐飲市場；高端外食可延後，CEO 已提到部分會議參加人數少 10–12%、俱樂部單點餐偏軟（2026-10-28）。","assumption":"業務員擴編與新品項能持續換來新客戶，且高端外食不出現明顯下行。","consequence":"五年後虧 50% 最可能的故事：高端外食下行兩年，有機成長掉到 3–5%，燃料與運費轉嫁不全，EBITDA 率退回約 6%，市場把倍數從 41 倍降到 17 倍左右（即 Bear 情境，約 −52%）。","ruling":"採納為 Bear 主線，機率 30%（Base 成長超出內生上界，空方機率不低於 30%）；目前沒有實證（Q3 有機 10.3%、10 月仍雙位數、不重複客戶排除中東 +5.7%），所以不據此清倉，只用來決定不在 41 倍追價。與唯一致命點同一變數（有機成長），屬部分重疊，門檻已統一在 7%。","watch":"季度有機成長、specialty 箱數、不重複客戶（排除中東）","not_applicable_reason":null,"evidence_refs":["competitive_share_entrants#1","geo_supply_chain#1"],"fact_refs":["f_kpi8_specialty_case_count_yoy","f_kpi9_yoy"]},{"view":"論點失敗","evidence":"US Foods 在 MOXē 平台加入 AI 下單並改業務員薪酬（2026-02）；新創 Pepper 募 5,000 萬美元替 500 多家獨立配送商導入 AI（2026-02）。","assumption":"CHEF 的科技與業務員建議能力持續領先地方小配送商。","consequence":"若下單轉向 AI 介面，主廚對業務員建議的依賴下降，CHEF 最主要的差異化被拉平，毛利率溢價縮小。","ruling":"部分採納：列為護城河威脅（點對點、機率約 25%）；目前毛利率仍在擴張（Q3 +84bp），尚無份額流失證據，CHEF 自己也在投 AI（CEO 2026-10-28）。","watch":"毛利率年增、品項配置成長是否仍快於客戶成長","not_applicable_reason":null,"evidence_refs":["substitute_technology#1"],"fact_refs":["f_kpi4","f_kpi10_unique_item_placements_y"]},{"view":"論點成功但股東經濟變差","evidence":"Q2 法說（2026-07-29）CFO 說要增加買回；Q3 卻把現金用在可轉債溢價，年底淨負債由 4.485 億升到 5.5–6 億美元，另發行約 270 萬股給債權人；燃料只轉嫁大部分；供應商多無長期合約、公司不避險食品價格，供應商食安違規也可能中斷供貨（10-K）。","assumption":"營收與 EBITDA 成長會等比例轉成每股盈餘與股東現金。","consequence":"營收達到 2030 目標，但成本吸收不全，加上在高本益比買回，每股價值成長落後 EBITDA 成長。","ruling":"部分採納：再融資後全稀釋股數指引下降（FY2027 42–43m 對 Q4 2026 43–43.5m），新貸款 SOFR+2.00%、2033 到期，資本結構其實變乾淨；但在 41 倍本益比買回的盈餘殖利率只有約 2.4%，買越多越傷股東，所以情境樹不計入買回。","watch":"FY2027 稀釋股數、淨負債÷調整後 EBITDA、毛利率與調整後費用率的差距","not_applicable_reason":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#3"],"fact_refs":["f_kpi7_fy2026","f_fwd_pe_latest"]},{"view":"價格已反映太多","evidence":"Fwd PE 41.02 倍（FY2026E 2.57）、34 倍 FY2027E；P/S 1.02 倍與 EV/S 1.19 倍都在近 4 個年度端點的最高位；26 週漲 35%；賣方平均目標價 104.71–107.43（MarketBeat）與現價相當；Q3 後 FY1／FY2 共識 EPS 小幅下修 0.39%／0.65%。","assumption":"市場會在 2031 年仍給 30 倍左右的本益比。","consequence":"基本情境（EPS 年增約 14%、倍數收斂到 25 倍）五年報酬約 17%，年化約 3%；要有 8% 年化，需要 2031 年 EPS 6.2 美元配 25 倍，或 5.2 美元配 30 倍，接近 Bull 情境。","ruling":"採納，是這次不追價的唯一約束；賣方目標區間 58–125 美元、高低比約 2.2 倍，分歧不算極端，不另外下調信心。","watch":"股價對 FY2027E 共識 EPS 的倍數、共識 EPS 修正方向","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_ev_s_percentile","f_week26_return_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 80.34 → 本次 105.41（+31.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=80.34","side_b":"本次 price_at_dd=105.41","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 80.34 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 80.34 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 80.34 美元：Bull 價 181.5、Bear 價 51，五年期望值 +44.8%，基準年化 9.0%，不對稱比 2.87","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.87。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 80.34 美元：五年期望值 +44.8%，基準年化 9.0%，不對稱比 2.87","side_b":"本次情境、股價 105.41 美元：五年期望值 +10.4%，基準年化 3.3%，不對稱比 1.17","ruling":"再換股價、情境不動：起點價上漲 31.2%，五年期望值少 34.4 個百分點，基準年化少 5.8 個百分點，不對稱比由 2.87 降到 1.17。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"生意變好 vs 價格已滿","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：有機成長 2026 年前三季約 11%、10 月仍雙位數，全年財測年內多次上修（年初 43.5–44.5 億 → 45.6–46.1 億），EBITDA 率提早兩年到 7%；管理層財測一向保守，AI 帶來的 1–2pp 利潤率上檔沒放進目標；RSI 43.65 不過熱。","side_b":"現價 41 倍今年 EPS、34 倍明年共識；生意照公司 2030 目標下緣走，2031 年給 25 倍，五年年化只約 3%；要 8% 年化得接近 Bull 路徑。","ruling":"可調和（程度差異）：生意好與價格貴同時成立。綁住行動的唯一約束是價格，不是論點；裁決不追、等價格，等的條件就是該約束的否定。","evidence_level":"公司申報＋法說＋共識快照","settle_metric":"股價對 FY2027E 共識 EPS 倍數降到約 27 倍（≤82 美元），同時季度有機成長 ≥7%","if_then":["若股價 ≤82 美元且最近一季有機成長 ≥7%：建目標倉位三分之一的首倉並重跑研究","若股價續漲但共識 EPS 沒有跟著上修（價格先走、證據未到）：不追","若股價下跌但有機成長仍 ≥7%、毛利率仍升（基本面無損）：到 82 美元分批反買，不視為停損訊號","反向條件：若有機成長 <7% 且毛利率年減，進場條件作廢，跌價也不買"],"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"]},{"axis":"利潤率節奏：Q2 迴避 vs Q3 揭露","cause":null,"prior_field":null,"side_a":"Q2 法說（2026-07-29）CFO 對 EBITDA 率逐年進度不給答案，只說「you never know what the cadence is going to be exactly」，CEO 改談不設上限。","side_b":"Q3 法說（2026-10-28）CFO：全年財測隱含 EBITDA 率到 7%，即原本的 2028 目標，Q4 約在 7% 以上。","ruling":"可調和：提早兩年達標是好消息，但 2030 目標 7.5–8% 只比今年高 0.5–1pp，等於管理層自己預告利潤率擴張放慢；Base 情境 EPS 年增由約 17% 逐年降到 10%，依據在此。","evidence_level":"法說逐字稿","settle_metric":"FY2027 財測隱含的 EBITDA 率是否 ≥7.3%","if_then":["若 FY2027 財測 EBITDA 率 ≥7.5%：上調 Base 路徑並重算進場價位","若 FY2027 財測 EBITDA 率 <7.0%：H2 削弱，停止加碼"],"evidence_refs":[]},{"axis":"管理層承諾：增加買回 vs 再融資優先","cause":null,"prior_field":null,"side_a":"Q2 法說（2026-07-29）CFO：維持強健資產負債表並增加買回；槓桿在 1.5–2.5 倍內會配置更多金額到買回。","side_b":"Q3 法說（2026-10-28）CFO 沒提買回金額；現金用於可轉債溢價，年底淨負債由 4.485 億升到 5.5–6 億，另發行約 270 萬股給債權人。","ruling":"可調和：再融資先處理 2028 可轉債到期與連動到期，FY2027 稀釋股數指引 42–43m 顯示全稀釋股數仍會下降；但「增加買回」尚未兌現，且在 41 倍本益比買回不划算，情境樹不計入買回。","evidence_level":"法說逐字稿","settle_metric":"FY2026 年報現金流量表買回金額；FY2027 稀釋股數 ≤43m","if_then":["若 FY2027 稀釋股數 >43.5m：H3 削弱，資本配置評價下調","若 2027 年在股價高於 100 美元時大量買回：記為資本配置扣分，不改變進場條件"],"evidence_refs":[]},{"axis":"前份估值與訊號","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份（2026-05-18，股價 80.34）：估值 🟠、訊號 B，Fwd PE 30.74 倍；建議等回測 52 週均線 64 美元再評估。","side_b":"本次（股價 105.41）：估值 🔴、訊號 B，Fwd PE 41.02 倍。","ruling":"前份要等，之後股價漲約 31%（超過 30%，須說明為何不翻面）：同期 Fwd PE 由 30.74 升到 41.02 倍（約 +33%），漲幅幾乎全來自倍數，近 3 個月 FY1 共識 EPS 只上修 1.98%；營運確實轉好（財測上修、EBITDA 率提早達標），但已被價格吃掉，故估值轉紅、訊號維持 B、不翻面。前份倍數分母口徑可能不同（80.34 ÷ 30.74 ≈ 2.61，高於 2026-07-30 快照 2.52），跨期倍數只作方向參考。","evidence_level":"價格與共識快照","settle_metric":"Fwd PE 回到 30 倍以下","if_then":["若股價 ≤82 美元且有機成長 ≥7%：依進場條件建首倉"],"evidence_refs":[]},{"axis":"價值陷阱判斷","cause":"新證據","prior_field":["trap"],"side_a":"前份：價值陷阱中等（🟡）。","side_b":"本次：仍為中等（🟡），十項衰退信號只亮「EPS 成長遠快於營收成長」一項。","ruling":"維持不變：Q2、Q3 毛利率續升（+49bp、+84bp），FCF 為正且高於淨利，SBC 低；新證據沒有新增衰退信號，也不足以降為低風險，因為未來 EPS 成長比營收更依賴利潤率。","evidence_level":"8-K、年度財報","settle_metric":"毛利率是否連 2 季年減","if_then":["若毛利率連 2 季年減且調整後費用率 >18%：陷阱風險升為高，持有者減碼一半"],"evidence_refs":[]},{"axis":"假設與風險門檻改寫","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份 H1：FY26–28 有機成長 ≥8%；H2：FY28 調整後 EBITDA 率 ≥6.5%；R1：Sysco 併購 Restaurant Depot 後高端小餐廳轉自取，有機成長失速；R2：Hardies／Greenleaf／Cambridge 整合綜效不及預期；R3：減重藥物與餐飲成熟化。","side_b":"本次 H1：TTM 有機成長 ≥7%；H2：TTM 調整後 EBITDA 率 ≥7.0%、FY2030 ≥7.5%；R1 改為低轉換成本＋同業 AI 下單；R2 改為高端外食景氣下行；R3 改為成本吸收；舊 R3 移到長期風險 R5。","ruling":"2026-07-29 公司公布 2030 目標（營收年增 7–10%、EBITDA 率 7.5–8%），FY2026 財測已達 7%，舊 H2 門檻已被跨過，改用新目標；有機門檻由 8% 降到 7% 是對齊公司目標下緣，並與唯一致命點同線。舊 R1 的整合進度本期事實表未收錄，Q3 有機 10.3% 尚無失速證據，併入新 R1；舊 R2 收購整合：Q2、Q3 毛利率年增 49bp、84bp，本期不再單列。","evidence_level":"法說逐字稿、8-K","settle_metric":"季度有機成長、TTM 調整後 EBITDA 率","if_then":["若有機成長跌破 7%：依唯一致命點處理"],"evidence_refs":[]},{"axis":"前份未填欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位為空（null）。","side_b":"本次：護城河方向穩定（→）、五年後成長空間中等（🟡）、類型為品質複利成長（次類循環/商品）、循環位置中循環、情境機率多 25／基本 45／空 30、最大回撤 −40%～−60%；裁決與角色由程式依新輸入重算。","ruling":"前份格式沒有要求這些欄位，屬方法變動，不是判斷翻面；新填值的依據分別寫在護城河、成長、情境段。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場條件（首倉）改寫","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設進場門檻欄（null）；裁決文字為「建議等回測 W52 $64 或 Sysco-Restaurant Depot 整合落地 (FY27Q1-Q2) 後再評估進場」。","side_b":"股價 ≤82 美元（約 FY2027E 共識 EPS 3.07 的 27 倍）且最近一季有機營收成長 ≥7%，觸發後建首倉。","ruling":"52 週均線已由前份的 64 美元升到 83.15，舊價位失去意義；改用價格錨加基本面確認，兩條件同時成立才建首倉；整合事件條件因事實表未收錄進度而移除，改由有機成長門檻代理。","evidence_level":"價格與均線","settle_metric":"股價、季度有機成長","if_then":["兩條件同時成立：建首倉","只成立價格條件、有機成長 <7%：不買"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點設立","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）。","side_b":"有機營收成長首次跌破 7%（公司 2030 目標下緣）的那一季財報；同義事件是 FY2027 全年財測隱含有機成長低於 7%。","ruling":"本次挑數學上最大的單一敏感度：倍數對成長預期的反應大於任何單一年度 EPS 落差，所以把致命點放在有機成長門檻上；發生時不攤平，同季毛利率也年減則減碼一半，連 2 季清倉。","evidence_level":"方法","settle_metric":"季度有機營收成長","if_then":["有機成長 <7%：不攤平","有機成長 <7% 且毛利率年減：減碼一半；連 2 季：清倉"],"evidence_refs":[]},{"axis":"清倉與減碼門檻設立","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉／減碼門檻（null）。","side_b":"清倉：有機成長連 2 季 <5% 或 specialty 箱數年增轉負；減碼：毛利率連 2 季年減且調整後費用率 >18%、淨槓桿 >2.5 倍、不重複客戶（排除中東）年增連 4 季 <2%。","ruling":"前份只有假設與風險描述，沒有可執行的門檻；本次把每條風險配上 8-K 可直接讀到的數字與動作，門檻取自公司 2030 目標下緣與 Q3 實際值（有機 10.3%、費用率 17.8%、淨槓桿 1.4 倍）並留出緩衝。","evidence_level":"8-K、法說","settle_metric":"每季 8-K","if_then":["任一清倉條件成立：清倉","任一減碼條件成立：減碼一半並停止加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"有機營收成長首次跌破 7%","type":"Single Thing","maps_to":"H1","metric":"季度有機營收成長（年增）","threshold":"<7%","action":"不攤平；同季毛利率也年減則持有者減碼一半，連 2 季清倉","source_freq":"每季 8-K","date":"2027-02","evidence_refs":[]},{"n":2,"text":"價格回到可接受區間且成長未破","type":"估值rearm","maps_to":null,"metric":"股價對 FY2027E 共識 EPS 倍數＋季度有機成長","threshold":"股價 ≤82 美元且最近一季有機成長 ≥7%","action":"建目標倉位三分之一的首倉，並重跑完整研究","source_freq":"每日股價／每季財報","date":null,"evidence_refs":[]},{"n":3,"text":"首倉後成長延續","type":"加碼","maps_to":"H1","metric":"季度有機營收成長","threshold":"首倉後下一季 ≥7% 且股價 ≤90 美元","action":"加到目標倉位一半","source_freq":"每季 8-K","date":null,"evidence_refs":[]},{"n":4,"text":"利潤率擴張停下","type":"假設驗證","maps_to":"H2","metric":"TTM 調整後 EBITDA 率","threshold":"連 4 季 <6.65%","action":"H2 削弱，停止加碼","source_freq":"每季 8-K","date":null,"evidence_refs":[]},{"n":5,"text":"競爭與科技拉平","type":"風險","maps_to":"R1","metric":"不重複客戶年增（排除中東）／毛利率年增","threshold":"客戶年增連 4 季 <2%，或毛利率連 2 季年減","action":"持有者減碼一半；未持有者撤回進場條件","source_freq":"每季法說","date":null,"evidence_refs":["competitive_share_entrants#1","substitute_technology#1"]},{"n":6,"text":"成本吸收失敗","type":"風險","maps_to":"R3","metric":"毛利率年增＋調整後費用率","threshold":"毛利率年減且調整後費用率 >18% 連 2 季","action":"減碼一半","source_freq":"每季 8-K","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#3"]},{"n":7,"text":"高端外食下行確認","type":"清倉","maps_to":"R2","metric":"季度有機營收成長／specialty 箱數","threshold":"有機成長連 2 季 <5%，或箱數年增轉負","action":"清倉","source_freq":"每季 8-K","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":8,"text":"槓桿超標","type":"減碼","maps_to":"H3","metric":"淨負債÷調整後 EBITDA","threshold":">2.5 倍","action":"減碼一半，停止加碼","source_freq":"每季法說","date":null,"evidence_refs":[]},{"n":9,"text":"Q4 財報與 FY2027 財測複審","type":"複審日期","maps_to":null,"metric":"FY2027 財測隱含有機成長與 EBITDA 率","threshold":"有機 ≥7%、EBITDA 率 ≥7.0%","action":"重跑估值與情境樹","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"季度有機營收成長（年增）","bear_threshold":"連 2 季 <5%","window":"2 季","source":"公司 8-K 新聞稿","last_status":"ok"},{"metric":"毛利率年增與調整後費用率","bear_threshold":"毛利率連 2 季年減，且調整後費用率 >18%","window":"2 季","source":"公司 8-K 新聞稿與法說","last_status":"ok"},{"metric":"淨負債÷調整後 EBITDA","bear_threshold":">2.5 倍","window":"任一季","source":"法說與 10-Q","last_status":"ok"},{"metric":"不重複客戶年增（排除中東）","bear_threshold":"連 4 季 <2%","window":"4 季","source":"公司法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 41 倍本益比把公司 2030 目標上緣和長期 30 倍以上倍數一起定價；但公司自己的 2030 EBITDA 率目標只比今年高 0.5–1pp，利潤率擴張會放慢，EPS 成長終將向營收成長 7–10% 靠攏，倍數難撐。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🔴', moat_trend='→', week26=35.16, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🔴'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價 ≤82 美元（約 FY2027E 共識 EPS 3.07 的 27 倍）且最近一季有機營收成長 ≥7%","exec_line":"現在不追；觸發後先建目標倉位三分之一的首倉並重跑完整研究，下一季有機成長仍 ≥7% 再加到一半；觸發清倉條件則全數出場。"},"reasoning":{"industry":"營收：Q3 FY2026 淨銷售 11.35 億美元、年增 11.2%，其中有機 10.3%、收購 0.9pp；有機部分約 6pp 來自量（specialty 箱數 +6.1%、center-of-the-plate 磅數 +6.6%），約 4pp 來自價（淨通膨 4.1%，specialty 2.6%、肉品 6.6%）。毛利年增 15% 快於營收，營業利益 5,150 萬美元年增約 32%，經營槓桿主要來自毛利率（CFO 說燃料把費用率壓住，毛利率被燃料轉嫁墊高一點）。分部營收金額事實表未涵蓋，只有成長率與毛利率變動（specialty +63bp、肉品 +137bp）。產業時鐘判在擴張期：2026 年前三季有機成長約 11%（CFO），全年財測年內多次上修（年初 43.5–44.5 億 → 45.6–46.1 億），10 月仍雙位數；降溫跡象只有零星幾處（部分產業會議參加人數少 10–12%、俱樂部單點餐偏軟，CEO 2026-10-28）。供需持久度：需求面結構性持久但帶景氣循環，客群是高所得外食，可延後；供給面門檻低、可逆性高。議價權：上游分散（40 多國小型產地）但無長期合約、不避險；下游極分散（前十大客戶約占 FY2025 營收 6%），單一客戶沒有議價力，但換配送商成本低。單點依賴：沒有單一客戶或供應商依賴，最大的集中在需求端，即高端外食景氣與特定城市市場（10-K 區域集中風險），以及中東業務（5–6 月曾掉到去年同期約 94%，Q3 回到約 100%）。","moat":"機制：主廚一張單買齊特殊食材＋業務員懂料理＋高端城市路線密度。對比同業（TTM，CHEF 截至 2026-09、同業截至 2026-06，期間差一季）：毛利率 24.66% 對 SYY 18.50%、USFD 17.55%、PFGC 11.93%；營業利益率 4.32% 對 3.66%、3.23%、1.31%；FCF 率 4.03% 對 2.29%、2.36%、1.50%，三項都是四家最高。同業 ROIC 與歷史利益率事實表未涵蓋，只能證明利差為正，不能證明擴大。評分：執行 8（有機成長連續雙位數、財測多次上修、EBITDA 率提早兩年達標），定價 6（燃料只轉嫁大部分、10-K 承認轉換成本低、無合約），合計落 B 級。三條威脅都屬點對點，不扣分。產業態勢：雙向拉鋸。競爭面，US Foods 擴大 AI 下單、Pepper 替獨立配送商補科技，門檻本來就低；結構面，CHEF 客戶與品項滲透續增、毛利率續升；其他結構變數（關稅、反壟斷、訴訟）近 12 個月沒有新事件，管理層稱 40 多國採購與自有品牌可因應關稅（2026-03 UBS 會議，二手摘要）。報酬持續期：屬低利益率、高周轉的生意，當期 ROIC 所需投入資本事實表未涵蓋；四檢查點兩綠兩黃，弱點在需求可延後，以及單一品項層級的低轉換成本。","growth":"成長組成：Q3 量約 6pp、價約 4pp、收購 0.9pp；EPS 另外靠利潤率擴張與股數下降。共識三年 EPS：FY2026E 2.57、FY2027E 3.07、FY2028E 3.65（Koyfin 2026-10-31 快照，EPS 家數未載；營收共識 7 位分析師）；以 GAAP FY2025A 1.68 為基期的三年 CAGR 為 29.5%，但基期口徑與共識不同、會高估，FY2026E→FY2028E 兩年年化 19.2% 較乾淨。內生上界引護城河段代理值約 10%。缺口約 9pp（19.2% 對 10%）可歸因：一是利潤率擴張，調整後 EBITDA 率由 FY2026 約 7.0% 往 2030 目標 7.5–8%；二是股數下降，可轉債結算後 FY2027 稀釋股數指引 42–43m；三是利息占營收比下降。缺口可歸因，不依賴倍數重估；但公司自己的 2030 EBITDA 率目標只比今年高 0.5–1pp，利潤率能貢獻的成長會逐年變小，這是 Base 情境 EPS 年增由約 17% 降到 10% 的依據。管理層 2030 目標：營收 60–65 億（年增 7–10%）、調整後 EBITDA 4.5–5.2 億（2026-07-29）。產能：德州、新英格蘭、拉斯維加斯、中西部配送中心未來 2–3 年陸續上線，紐約第二據點仍在找（2026-10-28）。十項衰退信號：亮 1 項（EPS 成長遠快於營收成長：FY2022→FY2025 GAAP EPS 年化約 32% 對營收約 17%；FY2026E→FY2028E 共識 EPS 年化 19.2% 對 FY2027 共識營收 +9.0%），資料缺 1 項（產業估值倍數趨勢），其餘 8 項未亮。","governance":"現金品質：FCF÷淨利 FY2024 1.87 倍、FY2025 1.21 倍，FY2026 前九個月 FCF 1.157 億已高於全年淨利指引 1.085–1.10 億。SBC：FY2026 指引 29–30m，約營收 0.64%，以現價市值 45.8 億換算毛稀釋約 0.64%／年；但 Q3 SBC 930 萬相當於 GAAP 營業利益的 18.1%，對利潤不算小。債務：2026-10-15 新 6.75 億 7 年期定期貸款（SOFR+2.00%、2033 到期）用來提前償還 2029 到期貸款，並結算 2028 可轉債本金與部分溢價，其餘溢價發行約 270 萬股；Q3 末淨負債約 4.485 億（1.4 倍），年底預期 5.5–6 億（1.7–2.0 倍），在目標 1.5–2.5 倍內；事實表另有含租賃負債口徑的淨負債 7.81 億。股數：Q4 2026 全稀釋 43–43.5m，FY2027 42–43m。現金去向四分（再投資／併購／買回／還債）逐年金額事實表未涵蓋。計分三項：併購報酬無資料，近 12 個月無新併購，CFO 稱標的偏貴、偏好投資人才；買回以現價計盈餘殖利率約 2.4%，只要 10 年期公債殖利率高於約 0.4% 即不過；SBC 淨稀釋 ≤1.5% 通過。營運槓桿：Q3 營收 +11.2%、營業利益 +32%，沒有壓縮。","valuation":"現價 105.41：Fwd PE 41.02 倍（FY2026E 2.57）、34.3 倍 FY2027E（3.07）、28.9 倍 FY2028E（3.65）；trailing PE 45.24 倍。P/S 1.02 倍、EV/S 1.19 倍（前瞻 1.16 倍）都在近 4 個年度端點的最高位，trailing PE 在 4 點中約 75 分位；五年連續區間事實表未涵蓋，不換算五年分位。反推：要五年年化 8%，2031 年股價需約 155 美元，即 FY2031E EPS 5.2 美元配 30 倍，或 6.2 美元配 25 倍，接近 Bull 路徑。基本情境（FY2031E 4.95 × 25 倍，約 124 美元）五年約 +17%，年化約 3%；拆解：EPS 年增約 14%，倍數由 41 倍降到 25 倍每年約 −9%，不依賴倍數擴張。賣方：MarketBeat 平均目標 104.71／107.43、Investing.com 116.56／122、Benzinga 約 92（區間 58–125），現價落在平均附近，賣方也不給明顯空間；高低比約 2.2 倍，分歧不極端。共識動向：Q3 後最新快照 FY1／FY2 EPS 小幅下修 0.39%／0.65%，近 3 個月 FY1 上修 1.98%，上修動能變弱。同業前瞻倍數事實表未涵蓋（前份寫 14–18 倍，未核對），Bear 終端 17 倍參考該區間，Base 25 倍保留利基溢價。","premortem":"四條反證紀錄：一是高端外食下行加低轉換成本，對應 Bear（30%）；二是 AI 下單拉平差異化，列為護城河威脅；三是股東經濟，買回時機與成本吸收；四是價格已反映太多，為本次唯一行動約束。價值陷阱判斷：十項衰退信號只亮「EPS 成長遠快於營收」一項，屬利潤率擴張期的正常現象，但也代表未來 EPS 成長比營收更依賴利潤率，故評中等。歷史最大回撤、空方報告事實表未涵蓋；最大回撤依 Bear 路徑推估 −40%～−60%。管理層言行：Q2 預告 Q3 開季雙位數（兌現 11.2%）、財測上修（兌現）、中東由 94% 回到約 100%（兌現）；「增加買回」尚未看到。"},"plain":{"six":{"how_it_makes_money":"賺高端餐廳、飯店與俱樂部主廚的錢：替他們從 40 多國、約 9 萬個品項裡找貨並準時送到，錢卡在「採購廣度＋懂料理的業務員」這一節點；Q3 毛利率 25.0%、GAAP 營業利益率約 4.5%，毛利率比三家綜合配送同業高 6–13 個百分點。","moat":"護城河 B 級、方向穩定：靠採購廣度與懂料理的業務員綁住高端主廚，毛利率 24.7% 比綜合配送同業高 6–13pp，營業利益率與自由現金流率都是四家最高；但轉換成本低是公司自己在 10-K 承認的結構弱點，近年利潤率改善主要來自執行，而不是變得更難被換掉。","growth":"五年後成長空間中等：市場本身年增約 4%（food logistics 代理），CHEF 靠搶份額做到 7–10%；市占與滲透率事實表未涵蓋，也找不到有來源的第二條成長曲線，五年後成長多半回到高個位數。","capital":"資本配置中等：自由現金流穩定高於淨利、SBC 稀釋很低；這季把現金用在處理 2028 可轉債，資本結構變乾淨，但在 40 倍本益比下「增加買回」不划算，併購報酬事實表未涵蓋。","valuation":"現價要求 CHEF 做到 2030 目標上緣、而且 2031 年仍維持約 30 倍本益比，才有 8% 年化；我信生意能接近目標，不信倍數撐得住，估值偏貴。","how_wrong":"最可能看錯的是倍數而不是生意：生意照目標走，股價也只賺約 3% 年化；若高端外食轉弱，41 倍的倍數會和獲利一起掉。反方向的錯是太保守：公司財測一向偏保守，AI 若多帶 1–2pp 利潤率（CEO 自稱的上檔），Bull 情境就會成立。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 41 倍本益比把公司 2030 目標上緣和長期 30 倍以上倍數一起定價；但公司自己的 2030 EBITDA 率目標只比今年高 0.5–1pp，利潤率擴張會放慢，EPS 成長終將向營收成長 7–10% 靠攏，倍數難撐。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤82 美元（約 FY2027E 共識 EPS 27 倍）且最近一季有機營收成長 ≥7%","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":105.41,"week26_return_pct":35.16,"consensus_rev_3m_pct":1.98,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母 FY2026E 共識 2.57 與公司淨利指引 1.085–1.10 億同量級，不含明顯一次性項目；Q4 約 270 萬美元一次性再融資利息，稅前約 0.06 美元／股，不改變結論。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 FY2027 全年財測","impact":"高","watch":"FY2027 財測營收中位數隱含的有機成長是否 ≥7%、EBITDA 率是否 ≥7%"},{"date":"2026-12","date_precision":"month","type":"macro","event":"中東 12 月旅遊旺季","impact":"中","watch":"中東營收是否維持去年同期約 100%"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"德州、新英格蘭、拉斯維加斯、中西部配送中心陸續上線（未來 2–3 年）","impact":"中","watch":"新設施上線後毛利率與每條路線毛利是否續升"}],"_projected_from":"v19"}
```
