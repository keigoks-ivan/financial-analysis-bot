你是 stock-analyst v20 的**散文層（prose）agent**，標的 NVT（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：NVT　日期：2026-11-03　archetype：None　前份裁決：2026-05-24　B 衛星候選：thesis 完整（A 級執行 9/10、AI 數據中心液冷超級週期、Trachte/EPG systems integrator 轉型）但估值 🟡 + MA stretched + 短期 R:R 負值 + 4 週 +25.5% 漂移 = 時機不到。等回測 BB 中軌 $127 區 或 Fwd PE 28x $140 區 + Q2/Q3 26 backlog 維持 +100%+ YoY 後分批進場 3-5% 衛星倉。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2040B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（737B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1017B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1598B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1268B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（689B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1571B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2283B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4333B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2559B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2040           3472-4960      5 條（2–6 內）  
s3                  8000         737           5084-7263      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3883          7782-11117      5 條（2–6 內）  
s6                 11000         689          7218-10311      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1571           1350-1929      3 條（2–6 內）  
s10                 5000        2283           1902-2717      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2559           2000-2441      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5570B；至少需散文≈39.43KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−36%
−35%
−35
−25%
−24.0%
−24%
−22.82
−3.25
0%
0.2%
0.2
0.3
0.35
0.4
0.52
0.67
0.7%
0.7
0.72
0.74
0.75
01
1
1.0
1.02
1.05
1.1
1.2
1.30
1.33
1.4
1.5
1.5%
1.52
1.6
1.72
1.8
1.84
2.0
2
02
2.02
2.1%
2.5
2.68
3.0
03
3
3.36
3.69
3.72
04
4.0
4
4%
4.1%
4.17
4.31
4.5%
4.95
5.0
5
05
5%
5.11
5.17
5.36
5.375
5.39
5.5
5.55
5.61
5.9
6
06
6.150%
6.2
6.25
6.75
6.78
7%
7
7.1
7.85
8%
8
08
8.05
8.7
8.70
9
09
9.5
9.6%
10%
10
10.2
10.25
10.4%
10.98
11
11%
11.4
11.6
12
12.0%
12%
12.24
12.5
12.9
13%
13.2
13.2%
14
14%
14.1%
14.4%
14.4
15%
15
15.15
16%
16
17
17.1
17.1%
17.5
17.7%
18
18%
18.46
18.5
18.6%
19
20
20%
20.2%
20.35
20.4%
21
21%
21.9%
22
22%
22.1%
23%
23.0%
23.3
23.7%
24%
24
24.0%
24.2
24.21
25%
25
26
27
27%
27.3%
28
28%
28.2%
29%
29.5
29.7
30
30%
30.9
31%
33
34%
34.6
35%
35
35.9%
37.0%
37%
37.7%
38%
38.1%
38.4
38.93
39
39%
39.0%
40%
40.3%
42%
42
44%
45%
45
48
49
49%
50%
50
52
53%
53
54%
54
55%
57.6
58.0
60%
60.4%
62
63
65%
70%
70
72.5
73
75
80%
80
90
90%
93
95
95%
100%
100
104
105.3
108
113
125
125.19
$127
128
136
136.4
$140
140
141.75
145
150%
150
164.66
174
177
180
188
188.22
190
200
204
204.07
232
240
250
260
322.5
415
800
2023
2024
2025
2026
2027
2028
2029
2031
20261103
1,500
2,000
3,090
6,000
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
{"meta":{"ticker":"NVT","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"nVent Electric plc"},"oneliner":"資料中心液冷與電力配送帶動營收年增四成、財測三度上修，但有機訂單只年增低雙位數，又在高點舉債併購 Maverick；股價半年跌 24%，FY2027 本益比 18.5 倍，生意好、價格合理，風險集中在 2027 年資料中心訂單會不會轉負。","thesis":{"H":[{"id":"H1","text":"資料中心（液冷、電力配送、機櫃與線槽）需求延續到 2028 年，nVent 有機成長維持兩位數","2y":"2027 有機營收成長 ≥10%（不含併購），年底在手訂單 ≥26 億美元","5y":"2031 年營收 ≥95 億美元，基礎設施占比 ≥55%","10y":null,"threshold":"2027 有機營收成長 ≥10%；2027 年底在手訂單 ≥26 億美元","source":"公司季報新聞稿與法說會（有機成長、有機訂單、在手訂單）","drift_rule":"TTM 營收比基準路徑（2027 年約 73 億美元）低 5% 以上連兩季→削弱；低 10% 以上連三季→反轉"},{"id":"H2","text":"價格與生產力持續抵銷通膨與關稅，量能放大轉成利潤率擴張","2y":"2027 調整後 ROS（含 Maverick）≥21%，Electrical Connections ROS ≥28%","5y":"2028 年不含併購的調整後 ROS ≥22%（投資人日目標），Maverick ROS 升到 ≥20%","10y":null,"threshold":"2027 調整後 ROS ≥21%；Electrical Connections ROS ≥28%","source":"公司季報新聞稿分部表與法說會（價格、生產力、通膨金額）","drift_rule":"TTM 調整後 ROS 比門檻低 5% 以上（約 1 個百分點）連兩季→削弱；低 10% 以上連三季→反轉"},{"id":"H3","text":"Maverick 與後續併購能在三年內賺回資本成本，公司 ROIC 由 2025 年約 13% 升到 2028 年 15% 以上","2y":"Maverick 2027 營收成長 ≥15%、ROS 升到 ≥18%；2027 年底淨槓桿 ≤2.0 倍","5y":"2028 年 ROIC ≥15%，併購商譽沒有減損","10y":null,"threshold":"Maverick 2027 營收成長 ≥15%、ROS ≥18%；2027 年底淨槓桿 ≤2.0 倍；2028 年 ROIC ≥15%","source":"法說會與年報（分部、Maverick 揭露、槓桿、ROIC）；ROIC 目標來自 2026-03-18 投資人日 CFO","drift_rule":"Maverick 季度營收成長或 ROS 比門檻低 5% 以上連兩季→削弱；低 10% 以上連三季，或出現商譽減損→反轉"}],"R":[{"id":"R1","text":"AI 資料中心建置在 2027–28 年進入消化期，訂單從放緩變成衰退","h_ref":"H1","clock":"🔥","threshold":"任一季有機訂單年減，或季末在手訂單連兩季下降且低於 24 億美元；前份的兩家超大規模客戶下修資本支出保留為輔助監測（事實表未涵蓋，資料缺口）","evidence_refs":["supply_demand_durability#3","end_markets#3"]},{"id":"R2","text":"液冷與資料中心電力競爭加劇：Vertiv 等全套供應商打包銷售，亞洲低價廠與新進者壓價","h_ref":"H1","clock":"🐢","threshold":"Systems Protection 調整後 ROS 連兩季年減 ≥100bp；前份的 2028 年液冷份額 <8% 保留為監測（事實表無份額數據，資料缺口）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"id":"R3","text":"鋼鋁銅關稅，加上依賴墨西哥與中國生產，造成的成本通膨超過定價能力；兩用產品出口管制也限制部分市場","h_ref":"H2","clock":"⚡","threshold":"單季價格加生產力未抵銷通膨（含關稅），或全年關稅衝擊超過 1.5 億美元（2026 年約 1.05 億）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"Maverick 整合不如預期：在週期高點以現金 17.5 億美元加最多 5.5 億績效對價收購，利潤率停在中十位數、槓桿居高不下","h_ref":"H3","clock":"🔥","threshold":"Maverick 2027 營收成長低於 10%，或 2027 年底淨槓桿高於 2.5 倍","evidence_refs":["major_events#0","ma_merger#0","major_events#1"]},{"id":"R5","text":"Electrical Connections 這個傳統高利潤率段的定價力鬆動","h_ref":"H2","clock":"🔥","threshold":"Electrical Connections 調整後 ROS 連兩季低於 27%（第二季 27.3%、第三季 28.2%，皆年減）","evidence_refs":[]}],"single_thing":{"description":"2027 年任一季公司揭露有機訂單年減（資料中心建置暫停或延後）","why_fatal":"資料中心是營收占比最高的終端，基礎設施已近六成；在手訂單只有約 5 個月營收，訂單轉負兩到三季內就會傳到營收。遞減利潤率約 35%，EPS 與倍數同時下修，股價對應熊市情境的 −25%～−50%。這是 EPS 路徑上敏感度最大的單一變數，大於關稅（約 1 億美元）或 Maverick 利潤率。","if_happens":"減碼至半倉並停止加碼；下一季仍年減就清倉，等訂單連兩季回正再重跑完整研究","how_monitor":"每季財報新聞稿與法說：有機訂單年增率、季末在手訂單、管理層對下一季訂單的口頭描述（例如 2026-10-30 稱十月訂單非常強）","probability":"約 25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.46,"peg_fy2":0.74,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":3.36,"FY2026E":5.17,"FY2027E":6.78,"FY2028E":8.05},"fy_end_month":12,"eps_basis":"調整後（non-GAAP）稀釋 EPS。FY2025A 的 3.36 由 2026-10-30 法說 CFO 稱財測中點年增 60% 回推（5.375÷1.6），事實表未直接收錄；GAAP 稀釋 EPS 4.31 含已停業部門的處分利益，不可比。共識為 Koyfin 快照，分析師家數未揭露。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"分拆後靠併購轉型、由 AI 資料中心量能推動的電氣設備商：利潤率與現金轉換好，但成長高度集中在資料中心資本支出週期"},"industry":{"clock_phase":"II","sd_verdict_source":"判結構性持久、帶週期。支持面：Rystad（2026-05）稱歐美變壓器與高壓斷路器交期至少 2–3 年，Wood Mackenzie 調查電力變壓器平均交期 128 週，Goldman 與 Citi（二手轉述）估 2026–28 年供給低於需求。反向證據：Wood Mackenzie（2025-09）稱交期已見改善、低壓變壓器可能轉為過剩。公司端在手訂單由 25 億升到 26 億美元、有機訂單年增低雙位數，供給可逆性中等，熊市機率因此取 30%。","bargaining":{"up":"上游議價力偏強：鋼鋁銅受 232 關稅影響，2026 年關稅衝擊約 1.05 億美元；管理層稱供應商也在擴產、要一起放量，第四季財測因供應鏈刻意保守。","down":"下游分兩群。經銷通路分散、規格寫入，議價力弱；超大規模雲端與託管業者直接採購、單案大，會尋求更多供應商，議價力強。最大客戶約占營收 11%。","geo":"依賴墨西哥與中國生產的零組件與成品，有貿易與關稅風險；部分產品屬兩用產品，受出口管制。歐洲、亞洲資料中心正在擴張，公司在當地加碼商務與製造。"},"profit_pool_dir":"利潤池往資料中心電力與散熱移動，nVent 的基礎設施占比由分拆時 12% 升到近 60%。份額數據事實表未涵蓋，只能用成長率間接推斷公司有分到池子。","tam_table":[{"item":"公司稱總可及市場","value":"逾 1,500 億美元（2026-10-30 法說 CEO）"},{"item":"液冷占資料中心冷卻滲透率","value":"目前 10–15%，管理層預估 2028 年逾 30%（2026-03-18 投資人日）"},{"item":"液冷市場成長率","value":"管理層引用逾 35%（2026-03-18 投資人日）"},{"item":"每百萬瓦內容量","value":"約 100 萬美元（投資人日）→併入 Maverick 後約 200 萬美元（2026-10-30 法說）"},{"item":"基礎設施占營收","value":"分拆時 12%→2025 年 45%→2026 年迄今近 60%"},{"item":"營業利益池占比 5 年前→現在","value":"事實表未涵蓋"}]},"moat":{"mechanism":"規格寫入＋電氣經銷通路＋資料中心液冷與電力的系統工程與快速擴產","execution":9,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面在擴大：2026 年三度上修財測、Blaine 1 約 100 個工作天投產、新品約貢獻 30 個百分點成長、Systems Protection ROS 年增 260bp。定價面在縮小：毛利率 2023 年 40.3%→2025 年 37.7%→TTM 37.0%，Electrical Connections ROS 第二季年減 140bp、第三季年減 180bp，營益率落後 VRT 與 HUBB 約 3 個百分點。兩者相抵，判持平。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用 TTM 營益率與 FCF 率代理；SU.PA 無財務資料。","threats":[{"level":"🔴","text":"生態型攻擊：Vertiv、Schneider、Eaton 能同時賣設施端散熱與電力全套，Vertiv 2026-04 收購 Strategic Thermal Labs 補強液冷工程。若超大規模客戶改採整套採購，nVent 的白空間液冷單品會被打包壓價。","p":0.35,"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#0"]},{"level":"🟡","text":"點對點低價競爭：10-K 點名區域廠、低成本製造商與新進者。投資人日被問到 Envicool 與 Google 洽談時，CEO 沒有正面回答威脅程度，只說客戶在找更多供應商。","p":0.3,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"架構轉換：資料中心配電由 415V AC 轉向 800V DC，可能改寫機櫃電力內容。nVent 連接件已達 800V DC 額定，Maverick 也有 800V DC 機架，目前看機會大於威脅，但還沒有訂單證據。","p":0.2,"evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（機房營運）、決策者（設計與採購工程）、付款者（雲端與託管業者）三者一致。高密度 AI 機櫃的散熱與電力保護是物理上的需要，不是想要；CEO 2026-10-30 稱更多電力就有更多熱、就要更多冷卻。電氣機殼與接地連接多為法規與規格要求。急迫性高不等於持久，時點上的週期風險另列在風險一。"},{"item":"決策層級","level":"🟡","text":"決策的最小單位是超大規模客戶的單一建置案與晶片世代。每一代架構都要重新認證，客戶也在找更多供應商（2026-03-18 投資人日 CEO 回應 Envicool 提問）。最大客戶 2025 年約占營收 11%，2024 年沒有客戶超過 10%，集中度上升。經銷通路的機殼與連接件因規格寫入、單價占專案比重低，轉換誘因小。漲價後流失率、續約率等代理變數事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"AI 機房價值鏈的利潤主要落在晶片端。nVent 每百萬瓦內容量約 100 萬美元，併入 Maverick 後約 200 萬美元。毛利率 37% 與同業 35–38% 相近，營益率落後最強同業約 3 個百分點；關稅靠漲價轉嫁後利潤率仍擴大。這代表這個環節賺得到錢，但不是最難取代的一環。開放規格（800V DC 有 80 多家廠商支持）讓互補品標準化，壓縮差異化空間。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的工業品，沒有消費者價格敏感或政治定價上限，也不依賴監管授權。政策面風險在關稅與兩用產品出口管制，屬成本與市場進入問題，已列在風險三，不構成價格天花板。"}],"roiic":16,"reinvest_rate":90,"endo_ceiling":14.4,"formula_note":"單位為百分比。當期 ROIC 約 13%（2025 年，投資人日 CFO），目標是 2028 年超過 15%。增量 ROIC 粗估 12–20%，取中值 16%：若投入資本三年內因 Maverick（17.5 億美元＋最多 5.5 億）與擴產增加約 40%，ROIC 又由 13% 升到 15%，推得增量報酬約 20%；Maverick 首年利潤率只有中十位數、扣利息後只貢獻幾美分，把下緣壓到 12%。再投資率約 90%＝（資本支出－折舊＋營運資金增加＋併購淨額）÷稅後營業利益，參考 2023–2025 年部署 53 億美元、其中部分資金來自業務出售所得，單年波動極大（2026 年光 Maverick 就超過全年稅後營業利益）。內生上界＝16%×90%≈14.4%。投入資本、折舊與營運資金事實表未涵蓋，以上皆為粗估。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","NVT":36.97,"HUBB":35.36,"ETN":35.9,"VRT":38.12,"SU.PA":null,"unit":"%"},{"metric":"營業利益率","NVT":17.1,"HUBB":20.21,"ETN":17.71,"VRT":20.35,"SU.PA":null,"unit":"%"},{"metric":"FCF 利潤率","NVT":11.95,"HUBB":14.07,"ETN":13.1,"VRT":23.74,"SU.PA":null,"unit":"%"},{"metric":"研發密度","NVT":1.84,"HUBB":null,"ETN":2.81,"VRT":null,"SU.PA":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"HUBB","gm":35.36,"om":20.21,"fcf_margin":14.07,"rd_intensity":null,"strategy_note":"營益率 20.2%、FCF 率 14.1% 都高於 nVent，業務偏電網與公用事業，是 Electrical Connections 的直接標竿；nVent 這一段利潤率在年減，差距沒有縮小。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ETN","gm":35.9,"om":17.71,"fcf_margin":13.1,"rd_intensity":2.81,"strategy_note":"毛利率 35.9%、營益率 17.7% 與 nVent 相近，資料中心電力配送規模大，和新併入的 Maverick 開關設備正面重疊，也是 800V DC 開放規格的支持者之一。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"VRT","gm":38.12,"om":20.35,"fcf_margin":23.74,"rd_intensity":null,"strategy_note":"毛利率 38.1%、營益率 20.4%、FCF 率 23.7% 全面領先，2026-04 收購 Strategic Thermal Labs 補強液冷工程，是液冷段最強的對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"SU.PA","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表無財務資料；它是設施端電力與散熱的全套供應商，也是 800V DC 開放規格的支持者之一。"}]},"growth":{"driver_mix":"量為主（資料中心液冷、機櫃、電力產品出貨）＋併購（2026 年約 10 個百分點，2027 年 Maverick 全年併入）＋價格抵銷通膨；回購貢獻可忽略","runway_years":"約 2 年（液冷占資料中心冷卻由 10–15% 升到 30%，管理層預估 2028 年）","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河題的再投資推導：增量 ROIC 約 16%×再投資率約 90%≈14.4%，不另算","segments":[{"item":"Systems Protection 第三季","value":"營收 10.98 億美元，年增 53%（有機 54%），調整後 ROS 23.0%（年增 260bp），其中基礎設施年增約 90%"},{"item":"Electrical Connections 第三季","value":"營收 4.17 億美元，年增 23%，調整後 ROS 28.2%（年減 180bp），管理層歸因於組合與成長投資"},{"item":"基礎設施占營收","value":"分拆時 12%→2025 年 45%→2026 年迄今近 60%"},{"item":"Maverick","value":"2026-10-01 併入 Systems Protection，第四季約貢獻 19 個百分點營收成長（約 2 億美元），利潤率中十位數"}],"decay_signals":[{"signal":"毛利率連2季年減","lit":true,"evidence":"年度毛利率 2023 年 40.3%→2025 年 37.7%→TTM 37.0%；季度毛利率事實表未涵蓋，由 TTM 低於年度推斷仍在年減"},{"signal":"核心市占近12個月縮減","lit":false,"evidence":"無份額數據，成長率快於自身歷史"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"價格抵銷通膨的同時營收年增 44%"},{"signal":"EPS成長顯著高於營收成長","lit":false,"evidence":"2025→2027 共識 EPS 年複合約 42%、營收約 39%，差距約 3 個百分點"},{"signal":"FCF/淨利低於0.75連2年","lit":false,"evidence":"2025 年報表口徑 0.52 受處分利益扭曲，2024 年 1.72；2026 財測轉換率 90–95%"},{"signal":"SBC/營收大於5%且逐年上升","lit":false,"evidence":"約 0.7%"},{"signal":"TAM萎縮或被替代技術壓縮","lit":false,"evidence":"公司稱可及市場逾 1,500 億美元；800V DC 目前屬機會"},{"signal":"產業估值倍數近3年系統性下移","lit":null,"evidence":"事實表未涵蓋"},{"signal":"維持性資本支出占FCF大於60%","lit":false,"evidence":"2026 資本支出約 1.4 億美元，多為新產能"},{"signal":"停止投資新產能且收入3年內下滑","lit":false,"evidence":"Blaine 2 與亞利桑那廠擴產中"}],"trap_rating":"價值陷阱風險🟡、長期成長性🟡（亮 1 盞，另 1 項資料缺口）"},"quality":{},"governance":{"capital_returns":[{"item":"2026 年迄今回饋股東","value":"2.02 億美元（回購 1 億、股利約 1.02 億），季股利年增 5%"},{"item":"2026 年資本支出","value":"約 1.4 億美元，年增 50%（含 Maverick），前三季已支出 9,500 萬"},{"item":"併購","value":"Maverick 現金約 17.5 億美元＋2027–28 年最多 5.5 億績效對價；管理層預期每年都有交易"},{"item":"融資","value":"2026-09 發行 8 億美元 10 年期 6.150% 優先債；年底槓桿預期 2–2.5 倍"},{"item":"2023–2025 年資本部署","value":"53 億美元（投資人日 CFO）"}],"sbc":{"sbc_9m_musd":30.9,"note":"以第三季營收年化粗估約占營收 0.7%，回購足以抵銷"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"管理層稱近期併購皆達三年內報酬超過資本成本的要求（2026-03-18 投資人日 CFO），但個案報酬未揭露，部分標的進場時利潤率也低於預期。Maverick（17.5 億美元＋最多 5.5 億績效對價）首季利潤率中十位數，報酬要到 2027–28 年才驗得到。事實表未涵蓋，不判過關。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2026 年迄今回購 1 億美元。回購均價事實表未涵蓋，以現價前瞻本益比 24.2 倍換算盈餘殖利率約 4.1%；只要 10 年期公債殖利率高於 2.1% 就低於門檻（10 年期殖利率事實表未涵蓋）。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"前九個月 SBC 3,090 萬美元，以第三季營收年化約占營收 0.7%、約占市值 0.2%；管理層稱以回購抵銷稀釋，淨稀釋遠低於 1.5%。","grade":"過"}]},"valuation":{"basis":"前瞻本益比（2026 年共識調整後 EPS 5.17，財報前快照；公司財測中點 5.375）","tier":"電氣設備與資料中心基礎設施（同業 HUBB、ETN、VRT、Schneider）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比或 EV/S；本題以公司自身年度端點分位與共識 EPS 路徑當尺，同業倍數缺口已在理由中點名"},"fwd_pe":24.21,"peg":0.72,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 24.2 倍、2027 年 18.5 倍；PEG 約 0.7（兩年口徑約 1.0）；歷史本益比位於四個年度端點的 75 分位。PEG 看起來便宜，但分子是週期高點附近的資料中心盈餘，訂單成長也已降到低雙位數，所以判合理而非便宜。股價跌到 108 美元以下（2027 年 16 倍）才算便宜。","targets":{"sell_side_avg_low":188.22,"sell_side_avg_high":204.07,"range_low":136,"range_high":240,"as_of":"2026-08","note":"各聚合站數字不一，早於本季財報；全距高低比約 1.8 倍"},"upside_short_pct":13.2,"upside_mid_pct":39.0},"trap_analysis":{"verdict":"🟡","label":"週期高點盈餘加上毛利率下滑，非典型價值陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"第三季有機訂單只年增低雙位數（去年同季 +65%），營收卻年增 44%，連兩季營收成長遠高於訂單；在手訂單 26 億美元約當 5 個月營收；第四季有機成長財測降到 26–29%。Wood Mackenzie 稱電力設備交期已見改善、低壓變壓器可能過剩；同業與 nVent 的新產能集中在 2027–28 年投產。","assumption":"超大規模客戶的資料中心建置延續到 2028 年以後。","consequence":"2027 下半年起資料中心進入消化期，2028 年營收年減約一成、EPS 回落到 5 美元，倍數壓到 12–16 倍；五年後股價仍低於現價，持有期間最深可到 −50%。","ruling":"部分採納。訂單落後營收是真的領先訊號，但有兩個抵銷證據：去年同季訂單基期是 +65%，以及 Q2 法說稱公司刻意消化在手訂單、縮短交期。十月訂單管理層稱非常強，在手訂單也仍在季增。處理方式是熊市機率取 30%、訂單轉負就減碼，現在不砍論點。這個視角與唯一致命點（訂單轉負）是同一件事。","watch":"每季有機訂單年增率與季末在手訂單；2027-02 首次揭露的 Maverick 在手訂單。","evidence_refs":["supply_demand_durability#3","end_markets#3","supply_demand_durability#1"]},{"view":"論點成功但股東經濟變差","evidence":"在週期高點以現金 17.5 億美元＋最多 5.5 億績效對價收購 Maverick，首季利潤率只有中十位數、扣利息後只貢獻幾美分；毛利率三年降約 3 個百分點；Electrical Connections ROS 連兩季年減；2026 年關稅衝擊約 1.05 億美元，10-K 也預期 2026 年通膨持續；營益率落後最強同業約 3 個百分點。","assumption":"營收成長能等比例轉成每股經濟價值。","consequence":"營收照財測成長，但 ROIC 停在 13% 附近、達不到 2028 年 15% 的目標，槓桿升到 2.5 倍以上；EPS 成長慢於營收，倍數往一般工業股靠攏。","ruling":"部分採納。Systems Protection ROS 年增 260bp、整體調整後 ROS 年增 190bp，證明量能有轉成利潤，目前沒有股東經濟變差的證據。但併購報酬要三年才驗得到，所以把 ROIC 15% 與 Maverick 利潤率寫進第三個假設的門檻，2027 年底槓桿高於 2.5 倍就減碼。","watch":"Maverick ROS、淨槓桿、Electrical Connections ROS、全年關稅衝擊。","evidence_refs":["competitive_share_entrants#0","reg_tariff_export#1","geo_supply_chain#1","major_events#0"]},{"view":"價格已反映太多","evidence":"前瞻本益比 24.2 倍，歷史本益比位於四個年度端點的 75 分位；共識 2028 年 EPS 8.05 隱含 2025→2028 年複合約 34%，遠高於投資人日三年目標 17–20%，也高於內生成長上界約 14%。","assumption":"市場用週期高點的成長率外推。","consequence":"即使 EPS 達到共識，倍數只要回到 18 倍，到 2028 年底的報酬只剩約 16%，年化約 7%。","ruling":"部分反駁。股價已從 2026-05 的 164.66 美元跌 24%，2027 年本益比 18.5 倍已計入一部分減速；基準情境本身就假設倍數從 24 倍降到 20 倍，報酬來自盈餘成長而不是重新評價。但共識三年成長確實超過內生上界，所以熊市機率不低於 30%。","watch":"2027 年本益比、共識修正方向（本季財報後應會上修）。","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#0"],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_consensus_eps_fy3"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 164.66 → 本次 125.19（-24.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=164.66","side_b":"本次 price_at_dd=125.19","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 164.66 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 164.66 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 164.66 美元：Bull 價 322.5、Bear 價 93，五年期望值 +21.9%，基準年化 4.5%，不對稱比 1.84","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.84。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 164.66 美元：五年期望值 +21.9%，基準年化 4.5%，不對稱比 1.84","side_b":"本次情境、股價 125.19 美元：五年期望值 +60.4%，基準年化 10.4%，不對稱比 5.11","ruling":"再換股價、情境不動：起點價下跌 24.0%，五年期望值多 38.4 個百分點，基準年化多 5.9 個百分點，不對稱比由 1.84 升到 5.11。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：營收規模","cause":null,"prior_field":null,"side_a":"前份兩年驗證點：2026 年營收不低於當時財測 49–50 億美元","side_b":"2026-10-30 財測報告營收成長 48–49%，以 2025 年 38.93 億美元計約 57.6–58.0 億美元，已提前超過","ruling":"前份第一個假設的兩年門檻已經達成，不構成矛盾；本次把門檻往後移到 2027 年有機成長。","evidence_level":"公司財測","settle_metric":null,"if_then":[],"evidence_refs":["end_markets#1","capital_markets_pricing#0"]},{"axis":"訂單成長與營收成長的落差","cause":null,"prior_field":null,"side_a":"營收年增 44%、全年財測三度上修、十月訂單管理層稱非常強、在手訂單季增到 26 億美元（2026-10-30 法說）","side_b":"有機訂單只年增低雙位數，連兩季營收成長遠高於訂單（UBS 提問）；Q2 法說被問到年底在手訂單方向時，CEO 答難說、大約在合適水位；第四季有機成長財測降到 26–29%","ruling":"可調和，屬程度差異。去年同季訂單 +65% 的高基期，加上刻意縮短交期，解釋得了一部分落差。若 2027 上半年訂單仍落後、在手訂單轉降，就變成方向問題，改判減速確立。","evidence_level":"公司揭露＋分析師提問","settle_metric":"第四季有機訂單年增率與年底在手訂單","if_then":["若第四季有機訂單年增 ≥10% 且在手訂單 ≥26 億美元，則加第二筆至目標倉位三分之二","若任一季有機訂單年減，則減碼至半倉並停止加碼；連兩季則清倉","反向條件：若股價先漲回 150 美元以上而訂單數據還沒出來，不追"],"evidence_refs":["end_markets#3","supply_demand_durability#2","supply_demand_durability#3"]},{"axis":"自由現金流口徑","cause":null,"prior_field":null,"side_a":"事實表年度財報口徑：2025 年 FCF 3.72 億美元、FCF 率 9.6%；TTM FCF 率 12.0% 為四家同業最低","side_b":"投資人日 CFO：2025 年 FCF 5.61 億美元、年增 31%；Q2 法說維持 2026 年轉換率 90–95%；第三季 FCF 2.68 億美元","ruling":"兩個口徑不混用，看趨勢時採公司持續營業口徑。差異可能來自已出售業務的現金流與相關稅負被計入年度報表，但事實表沒有拆分，這只是推測。在驗證前，同業 FCF 率比較暫不當作護城河扣分證據，以 2026 全年轉換率來驗。","evidence_level":"兩個來源口徑衝突、未拆分","settle_metric":"2026 全年 FCF÷調整後淨利","if_then":["若 2026 全年轉換率低於 80%，則把盈餘品質降一級並停止加碼"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣方：訂單落後營收、第四季成長降速、在週期高點舉債併購、毛利率下滑、同業 2027–28 年集中投產；AI 資本支出一旦消化，盈餘與倍數雙殺，現在賣比等數據確認早一步","side_b":"買方：股價已跌 24%、2027 年本益比 18.5 倍、財測三度上修、十月訂單非常強，工業與商辦住宅也加速到高個位數成長","ruling":"賣方論證指向的是 2027 下半年的風險，目前還沒有數據證實。做法是現價只建首倉、保留兩筆，並把訂單轉負設為減碼與清倉條件，用事先定好的條件處理這個風險，而不是靠預測。","evidence_level":"推論＋公司揭露","settle_metric":"2027 年各季有機訂單年增率","if_then":["若 2027 上半年任一季有機訂單年減，則減碼至半倉","若訂單持平以上而股價跌破 108 美元，則分批反買"],"evidence_refs":["supply_demand_durability#3","competitive_share_entrants#2"]},{"axis":"評級與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-24，股價 164.66 美元，前瞻本益比約 33–35 倍）：B、估值合理偏貴、時機未到","side_b":"本次股價 125.19 美元（−24%），前瞻 24.2 倍、2027 年 18.5 倍；估值結論仍是合理，但已落到區間下緣；評級維持 B","ruling":"價格下跌改善了估值位置，基本面也續強；但同期訂單增速放緩，公司又在週期高點舉債併購，兩者相抵，評級不升。裁決與倉位角色由程式依新輸入重算。","evidence_level":"價格與共識數據","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"價值陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份 🟢","side_b":"本次 🟡","ruling":"新證據包括：毛利率由 2023 年 40.3% 降到 TTM 37.0%、Electrical Connections ROS 第二季與第三季分別年減 140bp 與 180bp、有機訂單成長落後營收。衰退訊號亮 1 盞，因此升一級。","evidence_level":"公司揭露與事實表年度財報","settle_metric":"Electrical Connections ROS；年度毛利率","if_then":["若 Electrical Connections ROS 連兩季低於 27%，則停止加碼"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"前份未產出欄位的補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位皆為空（未以本格式產出）","side_b":"本次：護城河方向持平、五年後跑道中等、公司類型為品質複利成長（次類循環）、週期位置中循環、牛／基／熊機率 25／45／30、最大回撤 −35%～−50%","ruling":"這是方法補齊，不是看法改變；前份執行力 9/10 的看法，本次獨立重估後結論相同。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場與加碼條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"等回測 BB 中軌 $127 區 或 Fwd PE 28x $140 區 + Q2/Q3 26 backlog 維持 +100%+ YoY 後分批進場 3-5% 衛星倉","side_b":"2027-02 第四季法說：2027 有機成長財測 ≥10% 且季有機訂單年增 ≥10% 才加碼第二筆；股價 ≤108 美元且訂單未轉負，再分批加碼","ruling":"價格條件已達（125.19 美元、前瞻 24.2 倍），在手訂單年增 100% 的條件沒達到，而且這個門檻本身設計有誤：2025 年底在手訂單已是前一年的 3 倍，公司又刻意消化在手訂單、縮短交期，不可能再倍增。改用有機訂單年增率與在手訂單不下降作確認。價格先到、證據只到一部分，所以只建首倉。","evidence_level":"方法＋公司揭露","settle_metric":"季有機訂單年增率","if_then":["若 2027-02 兩項條件皆達，則加碼至目標倉位三分之二","若條件未達，則維持首倉不加碼"],"evidence_refs":["end_markets#3"]},{"axis":"停損、減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設（原文為空）","side_b":"任一季有機訂單年減→減碼至半倉，連兩季→清倉；在手訂單連兩季下降且低於 24 億美元；2027 全年調整後 ROS 低於 20%；Electrical Connections ROS 連兩季低於 27%；2027 年底淨槓桿高於 2.5 倍→減碼三分之一，高於 3.0 倍→清倉","ruling":"新證據促成新門檻：有機訂單成長已落後營收、Maverick 併購推高槓桿，需要可量測的減碼與清倉條件。","evidence_level":"公司揭露","settle_metric":"季有機訂單年增率；淨槓桿","if_then":[],"evidence_refs":["supply_demand_durability#3","major_events#1"]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（原文為空）","side_b":"2027 年任一季公司揭露有機訂單年減（資料中心建置暫停或延後）","ruling":"Single Thing 選訂單轉負，而不是關稅或 Maverick，因為資料中心是 EPS 路徑上敏感度最大的單一變數；促成這個選擇的新證據是訂單成長已降到低雙位數。","evidence_level":"公司揭露","settle_metric":"季有機訂單年增率","if_then":["若發生，則減碼至半倉並停止加碼；下一季仍年減則清倉"],"evidence_refs":["end_markets#3"]},{"axis":"前份假設與風險門檻的退休與改寫","cause":"方法變動","prior_field":["thesis.H","thesis.R"],"side_a":"前份風險一：連 2 季 backlog YoY < +50% + 2 家 hyperscaler 下修 capex → R1 觸發；風險二：FY27 OPM 仍卡在 17-18% 未進到 19-20% → H2 削弱；風險三：2028 全球液冷 NVT share < 8%；假設三：Fwd PE 33-35x 維持在 28-30x 區間","side_b":"風險一改為季有機訂單年減，或在手訂單連兩季下降且低於 24 億美元；風險二併入第二個假設，改用 2027 年調整後 ROS ≥21%；液冷份額 <8% 保留為競爭風險的監測項（事實表無份額數據，資料缺口）；估值不再當生意假設，第三個假設改為併購報酬（2028 年 ROIC ≥15%）","ruling":"前份風險一的在手訂單條件很可能已成立（基期是前一年的 3 倍），但兩家超大規模客戶下修資本支出的條件事實表未涵蓋，不能判定觸發；而且在手訂單年增率受基期與交期縮短扭曲，所以改用訂單年增率。前份風險二的營益率門檻以調整後口徑已經達成（第三季 22.1%），改設更高的門檻。前份假設三的倍數區間已被股價下跌打破（現為 24 倍），倍數判斷移到估值題。","evidence_level":"方法＋公司揭露","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027-02 第四季法說的 2027 全年財測：有機營收成長 ≥10%，且第四季有機訂單年增 ≥10%","type":"假設驗證","maps_to":"H1","metric":"2027 有機成長財測；季有機訂單年增率","threshold":"≥10%；≥10%","action":"兩者皆達→加第二筆至目標倉位三分之二；任一未達→維持首倉不加碼","source_freq":"每季法說","date":"2027-02"},{"n":2,"text":"任一季公司揭露有機訂單年減","type":"Single Thing","maps_to":"Single Thing","metric":"季有機訂單年增率","threshold":"<0%","action":"減碼至半倉並停止加碼；連兩季則清倉","source_freq":"每季","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"單季價格加生產力未能抵銷通膨（含關稅），或全年關稅衝擊超過 1.5 億美元","type":"風險","maps_to":"R3","metric":"管理層揭露的價格、生產力與通膨金額；全年關稅衝擊","threshold":"未抵銷；>1.5 億美元（2026 年約 1.05 億）","action":"停止加碼；下一季仍未抵銷則減碼三分之一","source_freq":"每季法說","date":null,"evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]},{"n":4,"text":"Electrical Connections 調整後 ROS 連兩季低於 27%","type":"風險","maps_to":"R5","metric":"Electrical Connections 調整後 ROS","threshold":"連兩季 <27%","action":"停止加碼","source_freq":"每季新聞稿分部表","date":null},{"n":5,"text":"Maverick 2027 營收成長低於 10%，或 2027 年底淨槓桿高於 2.5 倍","type":"風險","maps_to":"R4","metric":"Maverick 營收成長；淨槓桿","threshold":"<10%；>2.5 倍","action":"減碼三分之一","source_freq":"每季法說","date":"2027-12"},{"n":6,"text":"股價跌到 108 美元以下（約 2027 年共識 6.78 的 16 倍），且有機訂單沒有轉負","type":"估值rearm","maps_to":"估值","metric":"股價；季有機訂單年增率","threshold":"≤108 美元且訂單年增 ≥0%","action":"分批反買，加一筆（目標倉位三分之一）","source_freq":"每日股價＋每季訂單","date":null},{"n":7,"text":"股價升到 200 美元以上（約 2027 年共識 6.78 的 29.5 倍），而訂單沒有再加速","type":"減碼","maps_to":"估值","metric":"股價；季有機訂單年增率","threshold":"≥200 美元且訂單年增 <15%","action":"減碼三分之一","source_freq":"每日股價＋每季訂單","date":null},{"n":8,"text":"Maverick 相關商譽減損，或 2027 年底淨槓桿高於 3.0 倍","type":"清倉","maps_to":"H3","metric":"商譽減損；淨槓桿","threshold":"出現減損；>3.0 倍","action":"清倉","source_freq":"每季財報","date":null,"evidence_refs":["major_events#0"]},{"n":9,"text":"第四季財報複審：首次揭露的 Maverick 在手訂單、2027 財測、淨槓桿","type":"複審日期","maps_to":null,"metric":"Maverick 在手訂單；2027 財測；淨槓桿","threshold":null,"action":"依觸發一、二、五重新檢視倉位","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"單季有機訂單年增率（公司法說揭露）","bear_threshold":"轉負（<0%）","window":"任一季，2026Q4–2027Q4","source":"公司季報新聞稿與法說會","last_status":"ok"},{"metric":"季末在手訂單","bear_threshold":"連兩季下降且低於 24 億美元","window":"連續兩季","source":"公司法說會","last_status":"ok"},{"metric":"全年調整後營業利益率（含 Maverick）","bear_threshold":"低於 20%","window":"2027 全年","source":"公司新聞稿","last_status":"ok"},{"metric":"Electrical Connections 調整後 ROS","bear_threshold":"連兩季低於 27%","window":"連續兩季","source":"公司新聞稿分部表","last_status":"warning"},{"metric":"淨槓桿（淨負債÷EBITDA）","bear_threshold":"2027 年底高於 2.5 倍","window":"2027 年底","source":"公司法說會","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把訂單成長落後營收讀成 AI 資本支出見頂，但落差有一部分來自去年同季訂單 +65% 的高基期，以及公司刻意縮短交期；十月訂單管理層稱非常強，工業與商辦住宅也同步加速到高個位數。2027 年本益比 18.5 倍只反映有限的成長。這個理由要在 2027-02 法說用訂單數據證實，沒有證實就撤回。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-22.82, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":"單檔上限 4%","requires_critic":[],"rearm_trigger":"2027-02 法說：2027 有機成長財測 ≥10% 且第四季有機訂單年增 ≥10%，兩者皆達才加第二筆","exec_line":"現價約 125 美元先建目標倉位三分之一；2027-02 兩項條件達標再加三分之一；股價跌破 108 美元且訂單未轉負，再加最後三分之一；任一季訂單年減就停手，並減碼至半倉"},"reasoning":{"industry":"第三季營收 15.15 億美元，報告與有機皆年增 44%；調整後營業利益率 22.1%（年增 190bp），GAAP 營業利益率 18.6%，自由現金流 2.68 億美元。分部方面，Systems Protection 10.98 億美元（年增 53%，ROS 23.0%），Electrical Connections 4.17 億美元（年增 23%，ROS 28.2%）。全年財測為報告營收成長 48–49%、調整後 EPS 5.36–5.39，第四季 1.30–1.33。單點依賴：最大客戶（屬 Systems Protection）約占 2025 年營收 11%、年底應收 11%，2024 年沒有客戶超過 10%，集中度在上升；目前未見該客戶導入第二供應商的具體證據。產業時鐘判擴張期，依據是變壓器與高壓設備交期仍 2–3 年、同業新產能多在 2027–28 年才投產，nVent 自身也還在擴產（Blaine 2 與亞利桑那廠都在 2027 年中投產）。不過有機訂單只年增低雙位數，遠低於營收成長，第四季有機成長財測也降到 26–29%，屬擴張後段的訊號。供需持久性判結構性為主、帶週期，供給可逆性中等。","moat":"護城河機制是規格寫入加經銷通路，再加上資料中心液冷的工程能力與擴產速度。10-K 自承不依賴單一專利、客戶或品牌，也點名新進者與低價廠。執行力給 9 分：2026 年三度上修財測、Blaine 1 約 100 個工作天投產、新品活力 30%、Systems Protection ROS 年增 260bp。定價力給 6 分：第三季價格幾乎獨力抵銷約 6,000 萬美元通膨（含約 2,000 萬關稅），但毛利率由 2023 年 40.3% 降到 TTM 37.0%，Electrical Connections ROS 連兩季年減，管理層歸因於產品組合與成長投資。營益率 17.1% 落後 VRT 的 20.4% 與 HUBB 的 20.2%；FCF 率 12.0% 是同業最低，但有口徑爭議，見矛盾段。同業 ROIC 事實表未涵蓋，改以營益率代理，對最強同業落後約 3 個百分點。當期 ROIC 約 13%（2025 年，投資人日 CFO），利潤率高，但併購商譽讓資本周轉偏低。產業態勢判雙向拉鋸。競爭面：Vertiv 2026-04 收購 Strategic Thermal Labs 強化液冷工程，客戶也在找更多供應商。結構面：電力設備交期 2–3 年，新產能 2027–28 年才集中投產。其他結構變數：鋼鋁銅關稅，以及 800V DC 架構轉換（80 多家廠商支持開放規格；nVent 連接件已達 800V DC 額定，Maverick 有 800V DC 機架）。","growth":"成長以量為主，來自資料中心液冷、機櫃與電力產品出貨；再加上併購（2026 年約貢獻 10 個百分點營收成長，2027 年 Maverick 全年併入，年化營收約 8 億美元），以及用價格抵銷通膨。回購貢獻可忽略。共識 EPS：2025 年調整後約 3.36 美元（由 CFO 稱 2026 財測中點年增 60% 回推）→2026 年 5.17→2027 年 6.78→2028 年 8.05（Koyfin 快照，家數未揭露；營收共識 2026 年 8 家、2027 年 10 家），三年年複合約 34%，只看 2026→2028 兩年約 25%。內生上界約 14%（見護城河題），缺口約 19 個百分點。其中一部分可以由併購（2026–27 年合計約 20 個百分點營收）與利潤率擴張（第三季調整後 ROS 由 20.2% 升到 22.1%）解釋；剩下是資料中心量能的週期性放大，無法用再投資歸因，標『依賴re-rate』：若市場照共識外推，價格就要靠倍數撐住。基準情境因此不採用共識的 2028 年 8.05，改用 7.85。跑道方面，液冷目前占資料中心冷卻 10–15%，管理層預估 2028 年超過 30%，照此約 2 年就到 30%；之後滲透率還能往上，但五年後會落在 35–70% 區間。第二條曲線（800V DC 電力機架、服務、電網工程建築）目前還沒有營收證據，所以判中等。衰退訊號十項亮 1 盞（毛利率下滑），產業倍數一項為資料缺口。","governance":"2026 年現金去向：併購是大宗，10-01 以現金約 17.5 億美元完成 Maverick，2027–28 年另有最多 5.5 億美元績效對價；資本支出約 1.4 億美元（年增 50%，多為資料中心、電網與供應鏈韌性的新產能）；前三季回饋股東 2.02 億美元（回購 1 億、股利約 1.02 億，季股利年增 5%）。融資：2026-09 發行 8 億美元 10 年期、票息 6.150% 的優先債。季末現金逾 11 億、總債務約 22 億美元、循環額度 6 億可用，管理層預期年底槓桿落在 2–2.5 倍目標內（2025 年底 1.6 倍、2026 年中 1.2 倍）。現金轉換：第三季 FCF 2.68 億美元，對調整後 EPS 1.52 換算的淨利約 1.1 倍；Q2 法說維持全年轉換率 90–95%。2025 年報表口徑的 FCF÷淨利只有 0.52，但淨利含處分利益，FCF 口徑也與公司自報的 5.61 億不同，見矛盾段。SBC 約占營收 0.7%。三項檢核：股權稀釋過關；回購在 24 倍本益比下盈餘殖利率約 4.1%，不過關；併購報酬管理層自述達標但個案未揭露，Maverick 待驗證，不判過關。","valuation":"現價 125.19 美元，等於 2026 年共識 EPS 5.17 的 24.2 倍（以上修後財測中點 5.375 計約 23.3 倍），也等於 2027 年共識 6.78 的 18.5 倍。基準情境假設 2031 年 EPS 10.25、終端 20 倍，等於倍數從 24 倍降到 20 倍，報酬全部來自盈餘成長。三年共識 EPS 年複合約 34%，PEG 約 0.7；改用 2026→2028 兩年約 25% 計算，PEG 約 1.0。歷史倍數只有四個年度端點（本益比 75 分位、股價營收比 62、EV/S 54），不是五年分位，所以五年分位留空。短期上檔 13.2%＝2027 年基準 EPS 6.75×21 倍＝141.75 美元；中期上檔 39.0%＝2029 年基準 EPS 8.70×20 倍＝174 美元。賣方目標價均值 188–204 美元、全距 136–240 美元，但資料是 2026-08 的，早於本季財報與這波下跌，也還沒看到 11 月更新。現價低於最低目標價，方向上支持價格已消化部分減速，但資料陳舊，不當作依據。同業倍數事實表未涵蓋，終端倍數只能用自身前瞻倍數校準，這是本題的資料缺口。","premortem":"壓力測試三組，以共識 2028 年 EPS 8.05 為第三年基礎：成長降到 15% 給 22 倍＝177 美元；降到 10% 給 18 倍＝145 美元；降到 5% 給 14 倍＝113 美元。三組過兩組，只有 5% 那組低於現價 125.19。熊市情境用 15 倍，介於 10% 與 5% 兩組之間，因為熊市路徑的 EPS 年複合只有約 4%。最大回撤推導：熊市情境 2028 年 EPS 約 5.0，乘 16 倍約 80 美元（−36%），乘 12.5 倍約 63 美元（−50%），後者也約等於跌破 250 週均線 72.5 美元後再跌 13%。股價目前低於 52 週均線 136.4、高於 104 週均線 105.3，RSI 34.6，沒有過熱。反證細節見三個視角的反證紀錄，這裡不重寫。"},"plain":{"six":{"how_it_makes_money":"賣電氣保護與連接產品（機殼、接地與連接件、液冷分配單元、模組化機房，併入 Maverick 後再加開關設備）給資料中心、電網、工業與商辦住宅。錢卡在『規格寫進設計＋經銷通路＋快速擴產交付』這個節點。2026 年基礎設施占營收近六成，資料中心同時是成長與風險的單一來源。","moat":"護城河方向持平，等級 B：執行力在擴大，定價力在縮小，兩者相抵。","growth":"五年後跑道中等：液冷滲透率預計 2028 年就超過 30%，第二條曲線（800V DC 電力、服務）還沒有證實。","capital":"資本配置以併購為主軸：2026 年以現金 17.5 億美元（另有最多 5.5 億績效對價）買下 Maverick，資本支出約 1.4 億、回購 1 億、股利約 1 億。SBC 約占營收 0.7%，現金轉換率財測 90–95%。三項檢核中只有股權稀釋確定過關，併購報酬待證，回購在 24 倍本益比下不划算。","valuation":"現價要求 2027–28 年 EPS 照共識走到 8 美元左右、倍數守在 18–20 倍；這個前提我信，只要資料中心訂單不轉負。估值合理，不便宜。","how_wrong":"最可能看錯在資料中心建置的時點：若 2027 年訂單轉負，盈餘與倍數會一起下修。陷阱風險中等，最大回撤要準備 −35%～−50%。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把訂單成長落後營收讀成 AI 資本支出見頂，但落差有一部分來自去年同季訂單 +65% 的高基期，以及公司刻意縮短交期；十月訂單管理層稱非常強，工業與商辦住宅也同步加速到高個位數。2027 年本益比 18.5 倍只反映有限的成長。這個理由要在 2027-02 法說用訂單數據證實，沒有證實就撤回。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":125.19,"week26_return_pct":-22.82,"consensus_rev_3m_pct":12.15,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"兩處分母要校正。一、2026 年共識 EPS 5.17 是財報前快照，低於上修後財測 5.36–5.39，以財測計前瞻本益比約 23.3 倍。二、EV 用的淨負債 12.24 億美元是 9 月底數字，還沒扣掉 10-01 支付的 Maverick 現金約 17.5 億美元；交割後淨負債約 29.7 億、EV 約 232 億美元，前瞻 EV/S 約 4.0 倍而非 3.69 倍，績效對價最多再加 5.5 億。兩者都不是爭點，校正後估值結論不變。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Supercomputing 展示 Maverick 800V DC 電力機架與新模組化液冷平台","impact":"中","watch":"客戶採用情況與訂單描述"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年財測，首次揭露 Maverick 在手訂單","impact":"高","watch":"2027 有機成長財測是否 ≥10%、第四季有機訂單年增率、淨槓桿"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"Blaine 2 液冷廠與亞利桑那工程建築廠投產","impact":"中","watch":"產能爬坡進度與 2027 下半年營收成長"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,408B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVT_20261103/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河</h2>
<p class="lead">護城河等級 B，執行力在擴大，定價力在縮小，方向持平。</p>
<ul class="pts">
<li>護城河機制是規格寫入加電氣經銷通路，再加上資料中心液冷與電力的系統工程能力與擴產速度。10-K 自承不依賴單一專利、客戶或品牌，也點名區域廠、低成本製造商與新進者。這不是靠專利築起來的牆，是靠交付速度與通路維持的位置。</li>
<li>執行力給 9 分。2026 年三度上修財測，Blaine 1 約 100 個工作天就投產，新品約貢獻 30 個百分點成長，Systems Protection ROS 年增 260bp。這些都是可以在財報上直接驗證的事實，而且從前份報告以來持續強化。</li>
<li>定價力給 6 分。第三季價格幾乎獨力抵銷約 6,000 萬美元通膨，其中約 2,000 萬是關稅。但毛利率從 2023 年 40.3% 降到 2025 年 37.7%，TTM 為 37.0%。Electrical Connections ROS 第二季年減 140bp，第三季年減 180bp，管理層歸因於組合與成長投資。</li>
<li>與同業比，營業利益率 17.1% 落後 Vertiv 的 20.4% 與 Hubbell 的 20.2%，差距約 3 個百分點。自由現金流率 12.0% 是四家同業最低，但這個數字有口徑爭議，公司自報口徑不同，兩者不混用，同業 FCF 率差距暫不當作扣分證據。同業 ROIC 事實表沒有涵蓋，所以改用營益率代理。</li>
<li>最強的威脅是生態型攻擊，機率估 35%。Vertiv、Schneider、Eaton 能同時賣設施端散熱與電力全套，Vertiv 在 2026-04 收購 Strategic Thermal Labs 補強液冷工程。若超大規模客戶改採整套採購，nVent 的白空間液冷單品會被打包壓價。</li>
<li>其次是點對點低價競爭，機率 30%，與架構轉換（資料中心配電由 415V AC 轉向 800V DC），機率 20%。後者目前看機會大於威脅，連接件已達 800V DC 額定，Maverick 也有 800V DC 機架，但還沒有訂單證據。</li>
<li>報酬持續期看四個檢核點，象限落在高利益率但低周轉。增量 ROIC 粗估取 16%，再投資率約 90%，內生成長上界約 14.4%。這個上界遠低於共識的三年盈餘成長，詳見§6 與§7。</li>
</ul>
<h3>5　二維評分與護城河對應數字</h3>
<!-- E5 -->
<h3>5.F　對手財務深度對照</h3>
<!-- E6 -->
<h3>5.R　報酬持續期檢核</h3>
<!-- E7 -->
</section>

```