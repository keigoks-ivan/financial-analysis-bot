你是 stock-analyst v20 的**散文層（prose）agent**，標的 NVTS（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVTS_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：NVTS　日期：2026-11-08　archetype：None　前份裁決：2026-05-24　X 迴避：估值 🔴 P/S 163x（同業 8x 的 20 倍）+ MA 動能末段（4 週 +144% 漂移）+ 體質 veto 4 項不過 + 共識目標 .88 隱含 −56% 下行。NVIDIA 800V HVDC thesis 真實但已透支；等回測 Bollinger 中軌  區或 2027H1 Rubin Ultra Kyber 量產驗證後再重評。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2052B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（448B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1004B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1467B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（927B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（541B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（764B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2381B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1283B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2435B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2052           3464-4948      5 條（2–6 內）  
s3                  8000         448           5286-7552      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3398          8121-11602      5 條（2–6 內）  
s6                 11000         541          7321-10459      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         764           1915-2736      5 條（2–6 內）  
s10                 5000        2381           1833-2619      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2435           2000-2565      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4648B；至少需散文≈40.35KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−350
−272.56%
−245.7%
−189.08%
−151
−150
−129%
−85
−85%
−78.1%
−74.77%
−70.6%
−60
−58.5%
−55%
−55
−34.9%
−28
−26
−18.1%
−2.05
−0.57
−0.18
−0.15
−0.12
−0.1
−0.10
0%
0
0.09
0.18
0.24
0.6%
1
1.12
1.25
1.26
1.4
1.5%
1.5
1.6
1.63
1.7
1.98
02
2
2.04
2.33
2.5
2.6
2.83
2.88
2.9
2.95
03
3%
3
3.2
3.25
3.5
3.73
3.9
4%
4
4.05
4.2
4.6%
5%
05
5
5.315
5.574
5.67
5.8
06
6
6.23
6.37
6.6
07
7
7%
7.5%
7.67%
8
08
8.61
09
9
10
10%
11
12%
12
13
14%
14
14.71
14.74
15%
15
15.17
16.65
17
17%
17.17%
17.96
18
19.12%
19.2
20
20%
21
21.89
22.7
22.9
24
24.5
25%
26
27
28
29%
29.25
29.5%
30%
30
31.5%
33%
33.49
35
35%
36.89
38%
38.61%
38.68%
39%
39.5%
39.7%
40%
40
40.0%
40.9%
42%
43%
44.08
44.43
45
46%
48.67
49
50%
52%
52.69%
53.32%
54%
55.26%
57
57.42
60
61%
64.3%
65%
68
70
70.6%
75%
80
81%
82
88
90
99.4
100
112
125%
130
136.57%
140
150
163
169.2
170
200
225
300
315
320
325
350
380
386
400
420
600
640
700
800
850
2024
2025
2026
2027
2028
2029
2030
20261108
1,000
1,350
1,400
1,550
1,600
1,650
1,750
1,850
2,500
3,000
3,200
3,400
3,700
4,000
4,200
4,867
6,000
6,400
6,800
7,000
7,200
7,400
7,838
8,000
8,200
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
{"meta":{"ticker":"NVTS","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Navitas Semiconductor Corporation"},"oneliner":"題材是真的，Q3 營收季增 33%、訂單出貨比約 2 倍，但 EV 仍是 FY2027 共識營收的 22.9 倍，損益兩平要季營收 6,000 萬美元以上，目前不值得買。","thesis":{"H":[{"id":"H1","text":"AI 基礎設施放量：2027 年 AI 基礎設施營收達 2026 年三倍，其餘高功率業務持平，帶動全年營收成長。","2y":"FY2027 營收 ≥8,000 萬美元，全年每季季增 ≥10%。","5y":null,"10y":null,"threshold":"FY2027 營收 ≥8,000 萬美元；上半年累計 ≥3,700 萬美元。","source":"公司季度新聞稿與法說；賣方共識 7,838 萬美元（7 位分析師）。","drift_rule":"TTM 營收連 2 季落後路徑 ≥5% 算削弱，連 3 季落後 ≥10% 算反轉。"},{"id":"H2","text":"800V 原生架構與 IVR 接力：第三拐點 2028 年形成實質營收，Claros 錨定客戶 2028 年底到 2029 年放量，FY2031 營收達 4 億美元以上。","2y":null,"5y":"FY2030 營收 ≥3.2 億美元，約占公司口徑 2030 年 SAM 的 4%；FY2031 ≥4.2 億美元。","10y":"十年後仍是 GaN、SiC 高功率前三大供應商，屆時需第三方份額資料。","threshold":"FY2030 營收 ≥3.2 億美元；Claros 至少兩家客戶進入量產。","source":"公司新聞稿與法說；Yole 等第三方市場資料。","drift_rule":"TTM 營收連 4 季落後路徑 ≥5% 算削弱，連 6 季落後 ≥10% 算反轉；十年論點跨 2 個年度落後算削弱，跨 3 個年度算反轉。"},{"id":"H3","text":"獲利路徑成立：毛利率靠 IVR 升到 50% 以上，費用增速低於營收，季營收 6,000 萬美元出頭時損益兩平。","2y":"FY2028 非 GAAP 毛利率 ≥43%，費用占營收比逐季下降。","5y":"2029 年底前季營收 ≥6,000 萬美元，非 GAAP 營業利益轉正。","10y":null,"threshold":"2029 年底前季營收 ≥6,000 萬美元、毛利率 ≥50%、非 GAAP 營業利益為正。","source":"公司新聞稿；CEO 2026-11-03 的損益兩平模型。","drift_rule":"兩年指標連 2 季偏離 ≥5% 算削弱，連 3 季偏離 ≥10% 算反轉；五年指標連 4 季偏離 ≥5% 算削弱，連 6 季偏離 ≥10% 算反轉。"}],"R":[{"id":"R1","text":"高功率放量不如預期：客戶延後導入或經銷商庫存堆積，轉型缺口露出。","h_ref":"H1","clock":"⚡","threshold":"單季營收低於指引中點 10% 以上，或連 2 季季增低於 5%。前份的高功率占比條件保留，但 Q4 起占比接近全部，已失去鑑別力。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","channel_business_model_shift#1","end_markets#1"]},{"id":"R2","text":"大廠搶份額：Infineon、onsemi、ST、POWI 等在 800V 方案拿走更多份額。","h_ref":"H2","clock":"🔥","threshold":"沿用前份：2027 上半年確認公司份額低於 15%，或 POWI 公告 NVIDIA AI 營收每年超過 2 億美元；份額目前是資料缺口。新增：毛利率連 2 季季減。","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","customer_second_source#0"]},{"id":"R3","text":"架構分流或技術替代：±400V 與 800V 並存，或新技術讓現有方案過時。CEO 2026-11-03 已把 ±400V 放進第二拐點，公司兩邊都賣，風險低於前份。","h_ref":"H2","clock":"🐢","threshold":"沿用前份：2028 年前 OCP 接受多架構並存且超過一家雲端廠公開選 ±400V 進入觀察；機率超過 50% 才大動作。","evidence_refs":["substitute_technology#0"]},{"id":"R4","text":"代工換廠：TSMC 2027 年 7 月停止 GaN 生產，GlobalFoundries 與力積電的驗證或量產延遲，製造又多在美國境外且有單一來源。","h_ref":"H1","clock":"🔥","threshold":"2027 年 6 月底前 GlobalFoundries 未取得合格產品，或緩衝存貨用完前出現缺貨。","evidence_refs":["substitute_technology#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R5","text":"損益兩平變遠與持續稀釋：Claros 拉高費用，ATM、SBC 與 earnout 持續增加股數。","h_ref":"H3","clock":"🔥","threshold":"股數年增超過 10% 且營收落後路徑，或 2028 年底季營收仍低於 4,000 萬美元。","evidence_refs":["unprofitable_path_to_profitability#1","unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#1","unprofitable_dilution_trajectory#2","unprofitable_dilution_trajectory#4"]},{"id":"R6","text":"專利訴訟：Wolfspeed 在德拉瓦提告，Renesas 也提告，屬民事個案；受影響營收與結案日事實表未涵蓋。","h_ref":"H1","clock":"🔥","threshold":"法院發出初步禁制令，或和解金超過現金 10%。","evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"id":"R7","text":"出口管制與關稅：GaN、SiC 被列為國安關鍵技術，可能限制對中國終端客戶出貨，或壓縮 SiC 價格競爭力。","h_ref":"H1","clock":"🐢","threshold":"毛利率因關稅單季下滑 ≥200 個基點，或公司揭露受限營收超過總營收 10%；中國營收占比事實表未涵蓋。","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3"]}],"single_thing":{"description":"FY2027 全年營收低於 7,000 萬美元，即管理層說的季增雙位數沒有發生。","why_fatal":"情境樹裡最敏感的是終端營收：Base 與 Bear 的 FY2031 營收差 2.5 倍，每股價值差 6.6 倍；FY2027 是第一個能檢驗的年度。現價是 FY2027 共識營收 22.9 倍，放量落空時營收與倍數會一起掉。","if_happens":"改用空方情境，FY2031 每股約 1.6 美元；若持有則清倉，不因股價已跌而攤平。","how_monitor":"每季新聞稿的營收與季增率；FY2027 上半年累計低於 3,400 萬美元就提前示警。","probability":"25%（未來 12 到 24 個月）；上半年有訂單支撐，風險集中在下半年。"}},"appendix_a":{"growth_durability":6,"quality_score":3,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":1,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-0.57,"FY2026E":-0.15,"FY2027E":-0.12,"FY2028E":-0.1},"fy_end_month":12,"eps_basis":"FY2025A 為 yfinance GAAP 稀釋 EPS，含 earnout 公允價值變動；FY2026E 到 FY2028E 為 Koyfin 共識，來源未標明是否 Non-GAAP，判斷接近 Non-GAAP，兩者不可直接算成長率。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVTS_20261108/scenario.json","archetype":{"primary":"未獲利高成長","secondary":"轉機/特殊情境","confidence":"高","fingerprint":"TTM 營業利益率 −272.56%，營收連續季增雙位數，無負債，靠增資支應虧損與併購。"},"industry":{"clock_phase":"I","sd_verdict_source":"產業位置為復甦：公司 Q3 是 2024 年以來首次營收年增，AI 用 GaN 首批 800V 商用約在 2027 年（Yole，經 Meticulous 摘要）。供需判斷為結構性持久但供給可逆性高：功率需求來自機櫃功率上升，onsemi、ST 已推出 AI 用 GaN。先進製程與記憶體吃緊的資料不適用功率半導體。","bargaining":{"up":"弱。GaN 與 SiC 各有單一來源依賴，無代工長期供貨合約，TSMC 將退出 GaN；公司用緩衝存貨與共同投資補位。","down":"弱。架構由處理器廠與雲端廠決定，FY2025 最大經銷商占營收 46%；每個電源方案通常 2 到 3 家供應商。","geo":"絕大多數製造在美國境外，GaN 正移往美國 GlobalFoundries 與台灣力積電；出口管制可能影響中國終端客戶。"},"profit_pool_dir":"利潤池往 AI 資料中心電源移動，目前高利潤在 MPWR 這類已站穩的電源晶片廠（TTM 營益率 29.5%）；GaN、SiC 專業廠的五年利潤池占比事實表未涵蓋。","tam_table":[{"item":"公司口徑 2030 年 SAM（含 Claros）","value":"超過 80 億美元，管理層數字，未經第三方驗證"},{"item":"GaN 功率元件 2026 年市場","value":"約 8 億到 13 億美元，各家口徑差異大"},{"item":"公司 FY2026 共識營收占 2030 年 SAM","value":"約 0.6%"},{"item":"五年利潤池變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"自有 GaN、SiC 元件 IP 加系統級設計導入，靠搶先進入一代電源方案取得插槽；轉換成本只保護一代產品，沒有規模或成本優勢。","execution":7,"pricing":4,"grade":"C","trend":"→","trend_evidence":"執行面擴大：Q3 營收達指引高端，AI 基礎設施年底占比從三分之一以上提高到 40% 以上，並拿到 100 萬顆 GaN 的 800V 訂單。定價力穩定：毛利率年增 130 個基點，主要來自組合，仍比 POWI 低 14.71 個百分點。","peer_na_reason":"同業 ROIC 與份額事實表未涵蓋，改用毛利率差。","threats":[{"level":"🔴","text":"Infineon、TI、Renesas 與 onsemi、ST 都在 GaN 或 SiC 對手名單內，財力與客戶關係強過公司，可用完整產品組合爭取插槽。","p":"50%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","customer_second_source#0"]},{"level":"🟡","text":"客戶自研，或因出口限制轉向不受限的對手；垂直整合的處理器與雲端廠掌握電源架構。","p":"30%","evidence_refs":["customer_second_source#1","reg_tariff_export#2","substitute_technology#1"]},{"level":"🟡","text":"IVR 賽道有 Ferric、Empower 等對手，業界也在併購 IVR 公司，Claros 的模組化優勢目前只有管理層與客戶回饋的口徑。","p":"40%"}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是電源設計團隊，決策者是雲端與處理器廠，付款者多為電源廠與經銷商。省電等於增加算力，需求成立；第一拐點與 800V 無關，已進營收。第三、第四拐點 2028 年才有實質營收，金額只有管理層口徑。"},{"item":"決策層級","level":"🟡","text":"決策單位是單一電源方案的插槽，通常 2 到 3 家供應商，公司有時是第一供應商，有時是第二。10-K 說設計採用後客戶多半到下一代才換，轉換成本只保護一代產品。"},{"item":"價值鏈分配","level":"🔴","text":"架構由處理器與雲端廠決定，買方集中，代工端又有單一來源依賴。公司毛利率比 POWI 與 MPWR 低 15 到 17 個百分點，CEO 2026-07-27 說漲價不是重點，目前看不到公司能多分到利潤。"},{"item":"社會容忍度","level":"🟢","text":"電源元件是企業對企業採購，沒有消費者或監管對漲價的壓力。政策風險來自出口管制，已列入風險項，不影響定價上限。"}],"roiic":"不適用：營業利潤為負。Q3 非 GAAP 增量營益率約 15%（營收年增約 386 萬美元，營業虧損改善 60 萬美元），只是早期訊號，Q4 費用上升後會轉負。","reinvest_rate":"不適用：營業利潤為負，再投資率公式沒有意義。實際資金來自 2026 Q2 增資約 3.73 億美元。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率，兩項目前都沒有意義，上界留空；情境樹視同超過內生上界，空方機率不低於 30%。"},"combined":5.5,"score":5.5,"spread_table":[{"metric":"毛利率","NVTS":38.61,"POWI":53.32,"MPWR":55.26,"ON":38.68,"WOLF":-34.9,"unit":"%"},{"metric":"營業利益率","NVTS":-272.56,"POWI":7.67,"MPWR":29.5,"ON":19.12,"WOLF":-74.77,"unit":"%"},{"metric":"FCF 利潤率","NVTS":-189.08,"POWI":16.61,"MPWR":16.29,"ON":25.38,"WOLF":-46.38,"unit":"%"},{"metric":"研發密度","NVTS":136.57,"POWI":23.53,"MPWR":12.18,"ON":8.85,"WOLF":16.79,"unit":"%"}],"competitors":[{"name":"POWI","gm":53.32,"om":7.67,"fcf_margin":16.61,"rd_intensity":23.53,"strategy_note":"10-K 列為 GaN 對手，毛利率 53.32%、營益率 7.67%，有獲利支撐研發，是毛利率的直接比較基準。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"MPWR","gm":55.26,"om":29.5,"fcf_margin":16.29,"rd_intensity":12.18,"strategy_note":"毛利率 55.26%、營益率 29.5%，證明電源晶片可以賺高利潤；其 GaN、SiC 或 IVR 布局事實表未涵蓋。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ON","gm":38.68,"om":19.12,"fcf_margin":25.38,"rd_intensity":8.85,"strategy_note":"2026-06 推出 AI 資料中心用 GaN 產品組合，毛利率 38.68% 與公司相當，營益率 19.12%，差距來自規模。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"WOLF","gm":-34.9,"om":-74.77,"fcf_margin":-46.38,"rd_intensity":16.79,"strategy_note":"TTM 毛利率 −34.9%、營益率 −74.77%，SiC 同業仍在虧損；也是 2026-07 專利侵權訴訟的原告。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量與產品組合為主，價格沒有證據，併購在 2028 年底前沒有貢獻，沒有回購。","runway_years":9,"runway_post_y5":"🟢","endo_ceiling_basis":"營業利潤為負，內生成長率公式不適用；現階段成長由增資與併購支應。","segments":[{"item":"AI 基礎設施（資料中心加電網）","value":"Q4 指引占營收超過 40%，約 640 萬美元以上；管理層預期 2027 年約三倍，全年基期未揭露"},{"item":"其他高功率","value":"管理層 2027 年模型假設大致持平"},{"item":"行動與低階消費","value":"2025 年占多數營收，2026 年底降到低個位數"},{"item":"IVR（Claros）","value":"目前無營收，錨定客戶 2028 年底到 2029 年放量"}],"decay_signals":["亮燈：SBC 占營收 64.3%，高於 FY2025 的約 31.5%","未亮：毛利率 Q2、Q3 都年增","未亮：TAM 未見萎縮，行動業務是主動退出","無法判斷：市占變化沒有第三方資料","無法判斷：產業估值倍數三年走勢事實表未涵蓋","不適用：EPS 與 FCF 為負，EPS 對營收成長差與 FCF 轉換率沒有意義"]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"公司沒有配息與回購，現金用途是虧損、存貨與併購，已在本題判讀寫明。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Claros 約 2.33 億美元（搜尋摘要，現金部分約 1.26 億美元），2026-10-05 完成，錨定客戶 2028 年底到 2029 年才放量，已實現報酬為零。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"公司沒有回購。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 占營收 64.3%；流通股約一年增 17.17%（StockAnalysis，未標日期），遠高於每年 1.5%。","grade":"不過"}]},"valuation":{"basis":"EV/S 為主，EV／毛利為輔；公司虧損，本益比與 PEG 不適用。","tier":"小型未獲利功率半導體","peers":[{"item":"公司 EV÷FY2026 共識營收","value":"36.89 倍"},{"item":"公司 EV÷FY2027 共識營收","value":"22.9 倍"},{"item":"同業 P/S","value":"約 8 倍，來自前份判斷（2026-05）；現值事實表未涵蓋"}],"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"EV 是 FY2027 共識營收 22.9 倍，遠高於前份記載的同業約 8 倍；Rule-of-40 約 −151；12% 年化報酬所需營收比 Base 高約 42%，判為最貴一檔。五年分位資料不足，未納入。","upside_short_pct":-28,"upside_mid_pct":-26},"trap_analysis":{"verdict":"🟡","label":"題材真實，但股東報酬要等稀釋後的規模兌現"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2027 年第二、第三拐點放量時，Infineon、onsemi、ST 等大廠同時供貨，公司只拿到第二供應商份額；GaN 又要在 TSMC 停產前換廠。","assumption":"電源方案維持 2 到 3 家供應商，公司長期拿 30% 到 40%。","consequence":"FY2031 營收停在約 1.7 億美元，EV/S 3 倍，每股約 1.63 美元，較現價跌約 81%。","ruling":"採納為空方情境，機率 35%，因為份額只有管理層口徑，再投資報酬又為負。與唯一致命事件部分重疊：FY2027 營收低於 7,000 萬美元是這條故事最早的訊號。","watch":"每季毛利率、第二拐點轉營收進度、GlobalFoundries 合格時點。","evidence_refs":["competitive_share_entrants#3","customer_second_source#0","substitute_technology#2"]},{"view":"論點成功但股東經濟變差","evidence":"損益兩平門檻從季營收 3,000 多萬美元後段升到 6,000 萬美元出頭；Q4 費用指引 2,500 萬美元，較 Q3 增 52%；Q3 SBC 占營收 64.3%。","assumption":"毛利率 50% 需要 IVR，而 IVR 的錨定客戶 2028 年底到 2029 年才放量。","consequence":"營收達到 Base 路徑，股數仍增至 3.25 億股，每股成果被攤薄約 17%。沒有 IVR 時，毛利率約 43%、季費用 3,200 萬美元，損益兩平約 7,400 萬美元。","ruling":"採納。營收成長不等於股東報酬，Base 五年終值只比現價高約 25%。","watch":"費用占營收比、股數年增率、ATM 使用。","evidence_refs":["unprofitable_path_to_profitability#1","unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#1","unprofitable_dilution_trajectory#2","unprofitable_dilution_trajectory#4"]},{"view":"價格已反映太多","evidence":"EV 是 FY2027 共識營收 22.9 倍，扣掉 Claros 現金後約 24.5 倍，EV／毛利約 57 倍。","assumption":"12% 年化報酬需要 FY2031 營收約 6 億美元，再給 8 倍 EV/S，超過公司口徑 2030 年 SAM 的 7%。","consequence":"Base 路徑成立時年化報酬只有約 4.6%；短中期倍數壓縮時股價可能先跌到 6 美元多。","ruling":"採納。現在就買的最強論證是股價跌過半而基本面加速，且現金約占市值 17%；但倍數還在同業數倍以上，這個論證不足以支持建倉。","watch":"EV÷FY2027 營收是否降到 15 倍，以及共識營收是否上修。"}],"max_dd":{"lo":-85,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 29.25 → 本次 8.61（-70.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=29.25","side_b":"本次 price_at_dd=8.61","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 29.25 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 29.25 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 29.25 美元：Bull 價 33.49、Bear 價 1.63，五年期望值 −58.5%，基準年化 −18.1%，不對稱比 0.09","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.09。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 29.25 美元：五年期望值 −58.5%，基準年化 −18.1%，不對稱比 0.09","side_b":"本次情境、股價 8.61 美元：五年期望值 +40.9%，基準年化 4.6%，不對稱比 2.04","ruling":"再換股價、情境不動：起點價下跌 70.6%，五年期望值多 99.4 個百分點，基準年化多 22.7 個百分點，不對稱比由 0.09 升到 2.04。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：onsemi 2026-06 推 AI 用 GaN，ST 2026-05 推 700V GaN；Infineon、TI、Renesas 也在對手名單。","side_b":"結構轉好：CEO 2026-11-03 稱 800V 轉換已確定，Yole 預期 800V GaN 首批商用約 2027 年。其他結構變數：TSMC 退出 GaN、專利訴訟、出口管制。","ruling":"雙向拉鋸。需求轉好的證據比份額轉好的證據強，份額未證實前，題材只支持觀察，不支持溢價。","evidence_level":"大廠產品為二手報導，800V 時程為管理層與 Yole 摘要","settle_metric":"2027 年上半年季增率與毛利率","if_then":["若 2027 年連兩季季增 ≥12% 且毛利率上升，判結構性轉好，重跑研究","若毛利率連兩季季減，判競爭惡化，不追"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"現在就買的最強論證與估值","cause":null,"prior_field":null,"side_a":"現在就買：股價 26 週跌 52.69%，同期營收加速，Q4 指引高於共識，Q3 訂單出貨比 2 倍，現金 4.05 億美元約占市值 17%。","side_b":"不買：EV 仍是 FY2027 共識營收 22.9 倍，12% 年化報酬要 FY2031 營收約 6 億美元，Rule-of-40 約 −151。","ruling":"選不買。股價下跌是倍數從 P/S 163 倍回到 57 倍，還不夠便宜。兩邊是程度差異，可由更低價格或更快成長調和。","evidence_level":"價格與共識為事實表；訂單為管理層口徑","settle_metric":"EV÷FY2027 營收、2027 年上半年累計營收","if_then":["若股價上漲但季增率未達 12%，不追","若股價跌到約 5.8 美元且季增率與毛利率達標，重跑研究後分批反買","若 FY2027 上半年累計營收超過 4,200 萬美元，代表我看錯，取消估值條件並用 Bull 路徑重跑研究"],"evidence_refs":["unprofitable_path_to_profitability#1"]},{"axis":"損益兩平門檻上移","cause":null,"prior_field":null,"side_a":"2026-05 公司說法：季營收 3,000 多萬美元後段可損益兩平。","side_b":"CEO 2026-11-03：毛利率 50%、費用 3,000 萬美元出頭時，損益兩平約 6,000 萬美元出頭。","ruling":"採用新門檻，並加上條件：50% 毛利率要靠 IVR。沒有 IVR 時損益兩平約 7,400 萬美元。","evidence_level":"管理層口徑，IVR 毛利率尚無實績","settle_metric":"IVR 量產後的合併毛利率","if_then":["若 2029 年底前季營收未達 6,000 萬美元，持有者減碼，未持有者不追","若 2028 年毛利率已達 46% 以上且費用占比下降，把獲利時點提前一年重跑研究"],"evidence_refs":["unprofitable_path_to_profitability#1"]},{"axis":"費用紀律承諾與指引","cause":null,"prior_field":null,"side_a":"CFO 2026-07-27：Q3 起季度費用約增 100 萬到 150 萬美元，增幅低於營收成長。","side_b":"Q4 指引費用 2,500 萬美元，季增 52%，營收季增 14%。","ruling":"Claros 帶來一次性跳升，管理層的歸因目前未證實，先監測。預先定下檢驗：2027 年連兩季費用增速高於營收增速，就視為費用紀律承諾失敗。","evidence_level":"公司指引","settle_metric":"2027 年季度費用與營收增速差","if_then":["若 2027 年連兩季費用增速高於營收增速，持有者減碼，未持有者不追","若 2027 年連四季費用增速低於營收增速，獲利假設不扣分"]},{"axis":"賣方 EPS 是否反映 Claros 費用","cause":null,"prior_field":null,"side_a":"FY2027 共識 EPS −0.12 美元，近 3 個月修正 0%。","side_b":"用 FY2027 共識營收、42% 毛利率、每季費用 2,500 萬美元估算，每股虧損約 0.18 到 0.24 美元；利息收入事實表未涵蓋，以每年 0 到 1,600 萬美元估。","ruling":"判定這項利空還沒進賣方模型，在 2027-02 指引前不把共識 EPS 當依據，也不考慮進場。","evidence_level":"事實表共識加本次估算","settle_metric":"2027-02 財報後的 FY2027 EPS 共識","if_then":["若共識下修到 −0.18 美元以下而股價未跌，不追","若共識維持且公司費用低於指引，重算虧損路徑後才考慮分批反買"],"evidence_refs":["unprofitable_path_to_profitability#1"]},{"axis":"管理層承諾與實績","cause":null,"prior_field":null,"side_a":"2026-07-27 的財測：Q3 營收 1,350 萬美元、毛利率 39.7%、費用 1,550 萬到 1,750 萬美元；全年中個位數成長；AI 基礎設施年底占比超過三分之一；CEO 表示不給 2027 年財測。","side_b":"2026-11-03 實績：營收 1,400 萬美元、毛利率 40.0%、費用 1,650 萬美元；全年約增 7%；AI 占比提高到 40% 以上；CEO 改口給出 2027 年季增雙位數與 AI 三倍。","ruling":"短期承諾都做到，這是執行分給 7 的依據。2027 年的口徑變積極，但仍不拆已承諾訂單比例，只能算方向性說法。","evidence_level":"法說與新聞稿","settle_metric":"FY2027 季度營收","if_then":["若 2027 年第一季未達季增 10%，不追","若連兩季季增 ≥12%，納入重新研究條件"]},{"axis":"估值結論與前份比較","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-05-24）股價 29.25 美元，P/S 163 倍，結論很貴。","side_b":"本次股價 8.61 美元，P/S 57.42 倍，FY2027 EV/S 22.9 倍，結論仍偏貴。","ruling":"結論不變，差距縮小。變化主要來自股價下跌 70.6%，FY2027 共識營收只從 7,200 萬美元升到 7,838 萬美元。","evidence_level":"事實表價格與倍數","settle_metric":"EV÷FY2027 營收","if_then":["若倍數降到 15 倍且營運條件成立，才打開重新研究","若倍數回到 30 倍以上而營收未跟上，不追"]},{"axis":"迴避結論的理由更換","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份迴避，理由是估值、動能末段、體質四項不過；價值陷阱風險中等。","side_b":"本次仍迴避，動能不再過熱（RSI 44.08），但 Rule-of-40 約 −151、股數年增超過 10%；價值陷阱風險維持中等，只有 SBC 一項亮燈。","ruling":"結論維持，動能理由消失，新增損益兩平上移與 Claros 費用。前份迴避後股價跌 70.6%，判斷方向對，但不能據此推論現在還會跌。","evidence_level":"事實表與公司財報","settle_metric":"Rule-of-40、股數年增率","if_then":["若 Rule-of-40 轉到 20 以上且股數年增低於 10%，解除體質上的迴避理由","若跑道降到 12 個月以下且沒有轉正路徑，持有者清倉"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位為空。","side_b":"本次定為未獲利高成長，護城河方向穩定，成長跑道寬，情境機率 20／45／35，最大回撤 −55% 到 −85%；循環位置不適用。","ruling":"屬於口徑補齊，不代表基本面轉向。情境樹改用營收乘 EV/S，因為公司仍虧損。","evidence_level":"方法說明","settle_metric":"無","if_then":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份欄位為空；裁決文字寫等回測布林中軌區（原文價位缺漏）或 2027H1 Rubin Ultra Kyber 量產驗證後再重評。","side_b":"三項同時成立才重跑研究：EV÷FY2027 營收 ≤15 倍（約 5.8 美元）、連兩季季增 ≥12%、非 GAAP 毛利率 ≥42%。","ruling":"舊的技術位置已跌破，失去意義。新條件同時看價格與營運，滿足前不追，滿足後重跑研究再決定進場，不直接建倉。","evidence_level":"本次情境計算","settle_metric":"EV÷FY2027 營收、季增率、毛利率","if_then":["三項同時成立，重跑研究","任一項未成立，不追"]},{"axis":"Single Thing 改設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設（null）","side_b":"FY2027 全年營收低於 7,000 萬美元，即管理層說的季增雙位數沒有發生。","ruling":"前份沒有這一欄，本次選終端營收敏感度最大、又最早能驗證的事件；發生時若持有則清倉。","evidence_level":"情境敏感度計算","settle_metric":"FY2027 全年營收","if_then":["若 FY2027 營收低於 7,000 萬美元，持有者清倉，未持有者不追"]},{"axis":"停損指標改設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）","side_b":"FY2027 營收低於 7,000 萬美元清倉；季增連兩季低於 5%、毛利率連兩季低於 39%，或股數年增超過 10% 且營收落後路徑則減碼。","ruling":"前份沒有這一欄，本次補上可量測門檻，對應清倉與減碼動作。","evidence_level":"公司財報可驗證","settle_metric":"季度營收、毛利率、股數","if_then":["觸發清倉門檻就清倉","觸發減碼門檻就減碼一半"]},{"axis":"前份 NVIDIA 份額假設退休","cause":"新證據","prior_field":["thesis.H2"],"side_a":"每顆 GPU 的 GaN 加 SiC 含量 ≥300 美元，公司份額 ≥25%。","side_b":"CEO 2026-11-03 說每個電源方案 2 到 3 家供應商，長期 30% 到 40%；公司不拆 NVIDIA 營收。","ruling":"舊門檻取不到值，列為資料缺口，不再當主要假設；份額低於 15% 的警戒保留在大廠搶份額風險。","evidence_level":"管理層口徑，無第三方份額","settle_metric":"第三方拆解或公司揭露的份額","if_then":["若第三方確認份額低於 15%，持有者減碼，未持有者不追"]}],"triggers":[{"n":1,"text":"Q4 財報驗證指引","type":"假設驗證","maps_to":"H1","metric":"Q4 2026 營收與非 GAAP 毛利率","threshold":"營收 ≥1,550 萬美元且毛利率 ≥39.5%","action":"未達就不追，FY2027 路徑改用空方情境","source_freq":"公司新聞稿，每季","date":"2027-02"},{"n":2,"text":"FY2027 放量檢驗","type":"Single Thing","maps_to":"Single Thing","metric":"FY2027 全年營收","threshold":"低於 7,000 萬美元；上半年累計低於 3,400 萬美元提前示警","action":"持有者清倉，未持有者不追","source_freq":"公司新聞稿，每季","date":"2028-02"},{"n":3,"text":"重新研究條件","type":"估值rearm","maps_to":"H1","metric":"EV÷FY2027 營收、季增率、非 GAAP 毛利率","threshold":"≤15 倍、連兩季 ≥12%、≥42%，三項同時成立","action":"重跑完整研究，不直接建倉","source_freq":"每日收盤與每季財報","date":null},{"n":4,"text":"800V 原生量產時點","type":"假設驗證","maps_to":"H2","metric":"800V 原生方案量產與營收貢獻","threshold":"2027 年底前未量產，或 2028 年仍無實質營收","action":"不追，Base 路徑下修","source_freq":"法說，每季","date":"2028-02"},{"n":5,"text":"GaN 換廠","type":"風險","maps_to":"R4","metric":"GlobalFoundries GaN 合格與量產時點","threshold":"2027 年 6 月底前未取得合格產品","action":"持有者減碼一半，未持有者不追","source_freq":"法說與新聞稿，每季","date":"2027-07","evidence_refs":["substitute_technology#2"]},{"n":6,"text":"現金消耗與增資","type":"風險","maps_to":"R5","metric":"季度現金減少額、股數年增率","threshold":"連兩季現金季減超過 4,000 萬美元，或股數年增超過 10% 且營收落後路徑","action":"持有者減碼，未持有者不追","source_freq":"10-Q，每季","date":null,"evidence_refs":["unprofitable_dilution_trajectory#2"]},{"n":7,"text":"專利訴訟里程碑","type":"風險","maps_to":"R6","metric":"Wolfspeed 與 Renesas 訴訟裁定","threshold":"法院發出初步禁制令，或和解金超過現金 10%","action":"初步禁制令就清倉，和解金超限則減碼","source_freq":"法院公告與 8-K，不定期；受影響營收與結案日未知","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":8,"text":"大廠搶份額","type":"風險","maps_to":"R2","metric":"非 GAAP 毛利率、第三方份額","threshold":"毛利率連兩季季減，或 2027 上半年確認份額低於 15%","action":"持有者減碼，未持有者不追","source_freq":"每季財報；第三方拆解不定期","date":"2027-08","evidence_refs":["competitive_share_entrants#3"]},{"n":9,"text":"下次複審","type":"複審日期","maps_to":"H1","metric":"FY2026 全年財報與 2027 年首季指引","threshold":"財報公布後一週內","action":"更新情境路徑與各項門檻","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"FY2027 全年營收","bear_threshold":"低於 7,000 萬美元","window":"FY2027，2028-02 公布","source":"公司新聞稿","last_status":"unknown"},{"metric":"季營收季增率","bear_threshold":"連兩季低於 5%","window":"2027 年各季","source":"公司新聞稿","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"連兩季低於 39%","window":"2027 年各季","source":"公司新聞稿","last_status":"ok"},{"metric":"扣除 Claros 後現金（目前約 4.05 億美元）","bear_threshold":"低於 2.5 億美元且季營收低於 3,000 萬美元","window":"2028 年底前","source":"10-Q","last_status":"ok"},{"metric":"股數年增率","bear_threshold":"超過 10% 且營收落後路徑","window":"每年檢查","source":"10-Q","last_status":"triggered"},{"metric":"GlobalFoundries GaN 合格時點","bear_threshold":"2027 年 6 月底前未取得合格產品","window":"2027 上半年","source":"法說與新聞稿","last_status":"unknown"}],"evidence_dismissed":[{"ref":"unprofitable_nrr_rule40_band#0","reason":"資料日 2025-10-26，摘要寫 −129%，摘錄寫 75%，來源自相矛盾，且該站註明只適用 SaaS；本次改用 Q3 年增率加 TTM FCF 利潤率計算，約 −151。"},{"ref":"unprofitable_nrr_rule40_band#1","reason":"資料截至 2025-11-11，早於轉型完成，同業組含 QCOM、FSLR 這類非功率半導體公司；本次改用 TTM 營業利益率與功率半導體同業對照。"},{"ref":"unprofitable_dilution_trajectory#3","reason":"三個聚合站的 SBC 數字互相矛盾，來源本身註明須以 10-Q 為準；本次改用公司 Q3 新聞稿的 SBC 占營收 64.3%。"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"1","pacing":[],"holding_cap":"不建倉","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":true,"basis":"signal='X'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"三項同時成立才重跑研究：EV÷FY2027 營收 ≤15 倍（約 5.8 美元）、連兩季季增 ≥12%、非 GAAP 毛利率 ≥42%","exec_line":"目前不建倉。三項條件同時成立才重跑研究，研究通過後首筆只試單；FY2027 上半年累計營收超過 4,200 萬美元則取消估值條件。"},"reasoning":{"industry":"Q3 營收 1,400 萬美元，季增 33%、年增 38%；非 GAAP 毛利率 40.0%，非 GAAP 營業利益率 −78.1%，GAAP 營業利益率 −245.7%。Q4 指引 1,600 萬美元，AI 基礎設施占比超過 40%，行動業務降到低個位數。公司只給占比，不給分部金額，2026 年 AI 基礎設施全年基期也沒有數字，所以「2027 年成長三倍」還無法換算成美元。客戶集中：FY2025 最大經銷商占營收 46%，背後終端客戶未揭露。事實表有一條寫 Q3 經銷商占營收 29%，但對應金額 169.2 萬美元只等於 Q3 營收 12%，應是應收帳款占比，Q3 營收集中度事實表未涵蓋。單點依賴在代工：TSMC 預定 2027 年 7 月停止 GaN 生產，公司轉往 GlobalFoundries 與力積電，第一批美國製晶圓 2026 年 9 月才出貨。","moat":"機制是自有 GaN 製程 IP、GeneSiC 的 SiC 技術與系統級參考設計，先進入一代電源方案後，客戶通常到下一代才換（10-K）。對同業 ROIC 差距與第三方份額都取不到，改看兩個替代軸。毛利率方面，TTM 38.61% 低於 POWI 與 MPWR，Q3 較一年前升 130 個基點，來源是產品組合。份額方面，CEO 2026-11-03 說每個方案 2 到 3 家供應商，長期可拿 30% 到 40%，這是管理層估計；高功率營收成長 125% 快於市場的說法也沒有附市場數字。CEO 2026-07-27 說漲價目前不是重點。執行面擴大，定價力穩定，合併為穩定。不標上升，因為份額未經驗證；不標下降，因為大廠進場尚未反映在可量測的份額或毛利率。當期 ROIC 為負，投入資本事實表未涵蓋。另外，Q3 逐字稿寫授權給 Microchip，Q2 法說與 2026-09 的 8-K 對象是 Magnachip，我判斷是轉錄錯誤，無法對原始音檔查證。","growth":"成長靠量與產品組合，高功率產品取代行動產品；Claros 在 2028 年底前沒有實質營收。2026 年營收指引增 7%，CEO 口徑高功率成長 125%。共識營收 FY2026 4,867 萬美元、FY2027 7,838 萬美元，增 61%，約等於 2027 年每季季增 10%。三年共識 EPS 為 −0.15、−0.12、−0.10 美元，都是虧損，CAGR 沒有意義。內生上界無法計算，成長資金來自增資與併購，所以缺口歸因於外部融資與收購。跑道估算：以 Base 年化 54% 成長，營收到 SAM 的 30% 約需 9 年，屬中等長度。第二曲線是 IVR，錨定客戶是垂直整合的處理器與系統廠，2028 年底到 2029 年放量。GaN 功率元件 2026 年市場約 8 億到 13 億美元，與 80 億美元 SAM 口徑不同，不宜直接比較。","governance":"FCF 連四年為負，FY2022 到 FY2025 合計 −2.05 億美元；淨利為負，FCF 對淨利的轉換率沒有意義。Q3 SBC 占營收 64.3%。Q3 末現金 5.315 億美元，扣掉 10 月付給 Claros 約 1.26 億美元後約 4.05 億美元，公司無負債，Q3 未動用 ATM。Q4 非 GAAP 營業虧損約 1,850 萬美元，加上存貨與產能預付，每季約燒 3,000 萬到 4,000 萬美元，跑道約 10 到 13 季，超過 12 個月。稀釋壓力仍在：SPAC 原股東還可再領最多 1,000 萬股，ATM 額度在不同來源有 1.25 億與 5 億美元兩種說法，待核對 SEC 文件。近三年完整現金去向與 SBC 年度序列事實表未涵蓋。Q2 法說 CEO 口述現金 5.67 億美元，與 CFO 及 Q3 對照值 5.574 億美元不同，以後者為準。","valuation":"目前 EV 17.96 億美元，等於 FY2026 共識營收 36.89 倍、FY2027 共識營收 22.9 倍。事實表的 EV 用 9 月底現金，扣掉 Claros 付款後約 19.2 億美元，FY2027 倍數約 24.5 倍。以 40% 毛利率換算，EV／毛利約 57 倍。終端倍數 8 倍的對照只有前份記載的同業 P/S 約 8 倍（2026-05），同業現值事實表未涵蓋。12% 報酬的算法：8.61×1.12^5≈15.17 美元，乘 3.25 億股，減淨現金 1.5 億美元，再除以 8 倍，得營收約 6 億美元，比 Base 高約 42%。賣方平均目標 14.74 美元（2026-07）、最高 21、最低 6，高低差 3.5 倍，且都在 Q3 財報前，不能當支持依據，也降低我對情境報酬的信心。短期估計：2027 年底用 18 倍 FY2027 營收 8,200 萬美元，加淨現金 2.88 億美元，除以 2.83 億股，得約 6.23 美元。中期估計：2028 年底用 12 倍 1.4 億美元，加淨現金 1.98 億美元，除以 2.95 億股，得約 6.37 美元。歷史分位只有 4 個年度端點，不是五年分位，不使用。","premortem":"看多的最強版本是 Q3 訂單出貨比 2 倍、訂單看到 2027 年中，AI 基礎設施年底占比指引從三分之一以上提高到 40% 以上。看空的最強數字有三個：Rule-of-40 約 −151（Q3 年增 38% 加 TTM FCF 利潤率 −189.08%）；股數一年增 17%；損益兩平門檻升到季營收 6,000 萬美元出頭。未獲利高成長的五項體質標準只過現金跑道一項。股價 2026-05-24 起已跌 70.6%，跌幅本身不是安全邊際。管理層迴避的問題要當缺口看待：2026-07-27 與 2026-11-03 都不拆 2027 年已承諾訂單比例；2026-07-27 不拆資料中心營收、不答訴訟勝算與 Magnachip 收費結構；2026-11-03 再次不談訴訟。專利訴訟是民事個案，受影響營收與結案日事實表未涵蓋，不能裁定風險已解。"},"plain":{"six":{"how_it_makes_money":"賣 GaN、SiC 功率元件給 AI 資料中心與電網的電源廠，多經經銷商出貨；錢卡在能否拿到電源插槽的第一供應商位置，目前每季營收只有 1,400 萬美元，還賺不到錢。","moat":"護城河方向穩定（→），評為 C：技術與設計導入有進展，但份額沒有第三方證據，定價力也弱於獲利同業。","growth":"成長跑道寬（🟢）：公司營收只占自估 2030 年 SAM 的 0.6%，IVR 是有來源的第二曲線；但 SAM 是管理層數字，IVR 最快 2028 年底才放量。","capital":"資本配置目前偏弱：沒有回購，股數增長遠超每年 1.5%，Claros 尚無報酬；明顯加分只有在每股 21.89 美元募到約 3.73 億美元。","valuation":"現價要有 12% 年化報酬，FY2031 營收要到約 6 億美元，五年複合約 65%，再維持 8 倍 EV/S；我不相信這是基本情境，估值偏貴。","how_wrong":"最可能看錯在太保守：若 2027 年每季季增 20%，FY2027 營收破億美元，現在的倍數就不算離譜；但 Rule-of-40 約 −151、股數一年增 17%，目前仍列迴避。"}},"decision_inputs":{"signal":"X","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方平均目標 14.74 美元多在 Q3 前設定，隱含 FY2027 EV/S 約 45 倍；錯在倍數基準沿用題材高點，且共識 EPS 尚未計入 Claros 費用。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🔴","moat":"C","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"未獲利高成長","price_at_dd":8.61,"week26_return_pct":-52.69,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母不是爭點：用 TTM（44.43 倍）、FY2026（36.89 倍）或 Q4 指引年化 6,400 萬美元（約 28 倍），結論都是昂貴。分子要注意 Claros 付款後 EV 約多 1.26 億美元。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年首季指引","impact":"高","watch":"營收是否 ≥1,550 萬美元，Q1 指引是否季增 ≥10%"},{"date":"2027-03","date_precision":"quarter","type":"capacity","event":"GlobalFoundries GaN 首批合格產品","impact":"高","watch":"是否在 2027 年初取得合格"},{"date":"2027-07","date_precision":"month","type":"capacity","event":"TSMC 停止 GaN 生產","impact":"高","watch":"緩衝存貨與換廠銜接"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"800V 原生方案進入量產","impact":"高","watch":"2028 年是否形成實質營收"},{"date":"2028-12","date_precision":"quarter","type":"product","event":"Claros 錨定客戶開始放量","impact":"中","watch":"IVR 營收與合併毛利率"}],"_projected_from":"v19"}
```
