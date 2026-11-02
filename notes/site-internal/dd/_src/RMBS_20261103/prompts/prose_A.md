你是 stock-analyst v20 的**散文層（prose）agent**，標的 RMBS（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：RMBS　日期：2026-11-03　archetype：None　前份裁決：2026-06-20　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1988B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（661B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1004B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（980B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1167B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（543B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1016B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2193B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4065B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2315B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1988           3508-5012      5 條（2–6 內）  
s3                  8000         661           5137-7339      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3151          8294-11849      5 條（2–6 內）  
s6                 11000         543          7320-10457      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1016           1739-2484      5 條（2–6 內）  
s10                 5000        2193           1965-2807      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2315           2000-2685      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4616B；至少需散文≈40.38KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−39.3%
−35%
−35
−23.13
−1.9%
0
0.08
0.2
0.270
0.4
0.5%
0.651
0.68
0.7%
0.7
0.74
0.75
0.76
0.770
0.8
0.83
0.84
0.89
0.91
0.913
1
1.022
1.025
1.03
1.09
1.092
1.1
1.11
1.13
1.143
1.20
1.24
1.27
1.3
1.33
1.35
1.45
1.5%
1.6%
1.79
1.9
2%
02
2
2.10
2.11
2.16
2.183
2.27
2.30
2.33
2.51
2.60
2.6%
03
3.00
3
3.03
3.1
3.11
3.33
3.34
3.4
3.43
3.6%
3.7
3.70
3.80
3.8
3.88
3.89
4%
4
04
4.05
4.5
4.50
4.61
4.89
5%
5
5.05
5.1
5.10
5.2
5.7
06
6
6.05
6.3
7
07
7.05
7.57
7.77
7.8%
08
8%
8
8.1
09
9
10
10%
10.1
10.5
10.6
11.0%
11
11.1%
11.4
11.5
12
12%
13%
13
13.2
13.42%
14
15%
15
16
16%
16.8%
17
17%
17.3%
18
18%
19.8%
20%
20
20.5%
21%
22
22%
22.09
22.1
23
23%
23.1%
24
24%
24.9%
24.9
25
25%
26
26%
27
27.56
27.6
28
30%
30
30.9%
31
31.5%
33.3%
34%
35%
35
35.4
36.7%
36.9
37%
38.3%
39%
39.3%
39.7
40%
40
41
41.8%
42
42.3%
43
43.7%
45
46.6
46.8%
49
50%
52%
52
55
55.5
60
60%
60.4%
61.7%
62%
62.4
63%
63.5
65%
66%
70%
70
72.4%
73
79%
79.1%
79.6%
82%
84.1
85.71
85.8
90
95%
95
97
97.5%
100
100%
104
105.4
117
137
141.17
145
150%
172
226.8
250
606
2024
2025
2026
2027
2028
2031
9600
688008
20261103
1,000
1,120
1,200
1,600
1,710
6,800
7,000
7,600
9,000
9,130
9,170
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
{"meta":{"ticker":"RMBS","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Rambus Inc."},"oneliner":"Rambus 靠伺服器 DDR5 介面晶片與記憶體專利收錢，Q3 再超指引、Q4 產品營收指引年增 34%；股價半年跌兩成多後 FY2027 本益比約 22 倍，估值轉合理，但份額方向、DOJ 刑事調查與 2028 年記憶體循環三件事未解，分批建倉不一次買滿","thesis":{"H":[{"id":"H1","text":"RMBS 守住 DDR5 RCD 共同領先地位，第六代 9600 世代轉換與周邊晶片帶動產品營收 2027 年續增兩成以上","2y":"2027 年產品營收年增≥20%、份額≥40%、產品毛利≥60%","5y":null,"10y":null,"threshold":"2027 全年產品營收年增≥20%；管理層揭露 DDR5 RCD 份額≥40%；非 GAAP 產品毛利率≥60%","source":"公司季度 8-K 產品營收；每年 2 月 Q4 法說份額自述","drift_rule":"TTM 產品營收較 20% 成長路徑落後 5% 以上連 2 季為削弱；落後 10% 以上連 3 季為反轉"},{"id":"H2","text":"伺服器記憶體子系統每台晶片含量提高（通道數 8 增至 12–16、MRDIMM、LPDDR／SOCAMM2 電源管理），新產品成為產品線第二成長引擎","2y":null,"5y":"2031 年前新產品占產品營收≥30%，產品營收 2026–2031 年化≥15%","10y":null,"threshold":"新產品（周邊晶片、MRDIMM、SOCAMM）占產品營收 2028 年≥25%、2031 年≥30%；產品營收五年年化≥15%","source":"公司法說新產品占比自述（2026-07-27 CEO：年底達中雙位數）；8-K 產品營收","drift_rule":"TTM 產品營收較 15% 年化路徑落後 5% 以上連 4 季為削弱；落後 10% 以上連 6 季為反轉；公司停止揭露新產品占比即列資料缺口，下次複審降為削弱"},{"id":"H3","text":"權利金與矽智財提供穩定高毛利現金流，支撐 FCF 利潤率與股東回饋","2y":null,"5y":"FCF 利潤率維持≥35%，矽智財年增≥10%，每年回饋 FCF 的 40–50%","10y":null,"threshold":"TTM FCF 利潤率≥35%；矽智財業務年增≥10%；權利金年營收不低於 2025 年水準","source":"8-K 現金流量表與營收分項；CFO 矽智財規模自述（約 1.3 億、年增 10–15%）","drift_rule":"TTM FCF 利潤率低於 35% 門檻達 5% 以上（約 33.3% 以下）連 4 季為削弱；低於 31.5% 連 6 季為反轉"}],"R":[{"id":"R1","text":"Montage、Renesas 在第六代 RCD 與 MRDIMM 搶下份額","h_ref":"H1","clock":"🔥","threshold":"管理層揭露 RCD 份額低於 40%，或產品營收年增連 2 季低於伺服器出貨成長","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#0"]},{"id":"R2","text":"記憶體循環轉向：提早下單變成拉貨，2027 下半年起供給追上需求，客戶降規格壓低模組容量","h_ref":"H1","clock":"⚡","threshold":"產品營收連 2 季年減，或季度指引中點年增轉負","evidence_refs":["supply_demand_durability#1","end_markets#5","substitute_technology#2"]},{"id":"R3","text":"上游投入成本上升而標準品不能漲價，產品毛利率跌破 60%","h_ref":"H1","clock":"🔥","threshold":"非 GAAP 產品毛利率連 2 季低於 60%","evidence_refs":["geo_supply_chain#1","reg_tariff_export#1"]},{"id":"R4","text":"DOJ 反壟斷刑事調查以起訴或營運限制收場，並引發民事求償與證券訴訟","h_ref":"H3","clock":"⚡","threshold":"公司或高管遭起訴、簽認罪協議，或揭露罰款超過淨現金一成（約 7,600 萬美元）","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","major_events#0","lawsuit_class_action#0"]},{"id":"R5","text":"客戶集中：前五大占營收約三分之二、最大客戶 23%，任一 DRAM 廠轉單、自製或改採不需授權的技術","h_ref":"H1","clock":"🔥","threshold":"年度揭露前五大占比超過 70% 且營收年減，或最大客戶占比單年下降 5 個百分點以上","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","competitive_share_entrants#1"]},{"id":"R6","text":"替代技術或架構（板載 LPDDR、免權利金方案）壓縮獨立介面晶片與權利金價值，專利執行需訴訟","h_ref":"H2","clock":"🐢","threshold":"主要 CPU 平台或 DRAM 廠推出不需 RCD 的主流伺服器記憶體方案，或權利金年營收連 2 年下滑；機率達 50% 以上才砍倉","evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"id":"R7","text":"地緣與出口管制：唯一來源代工在台海風險區，82% 營收來自美國以外總部客戶","h_ref":"H1","clock":"🐢","threshold":"出口管制擴及記憶體介面晶片，或產品營收單季季減超過 20% 且公司歸因供應或管制","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#1"]}],"single_thing":{"description":"下一代伺服器平台（DDR5 第六代 9600 RCD 與第二代 MRDIMM）認證中，Rambus 在三大 DRAM 廠之一失去主供應地位，RCD 份額跌破 40%","why_fatal":"產品營收占五成且是唯一高成長線；以 Q4 指引產品營收年化約 5.2 億、RCD 占大宗（假設約八成）粗估，份額每掉 10 個百分點約少 9,000 萬美元營收、約 0.4 美元 EPS（產品毛利 60%、稅率 16%、1.09 億股）；世代認證失守要等下一代約兩年才有機會翻盤","if_happens":"清倉；情境改用 Bear 路徑（終端 EPS 3.70、15 倍）重估","how_monitor":"每年 2 月 Q4 法說的份額自述、產品營收年增率對照伺服器出貨、第六代 RCD 與 MRDIMM 設計案公告、第三方份額報導","probability":"12～24 個月約 20%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.09,"peg_fy2":0.89,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.51,"FY2026E":3.11,"FY2027E":3.88,"FY2028E":4.89},"fy_end_month":12,"eps_basis":"非 GAAP 稀釋 EPS（Koyfin 共識 2026-10-31）；FY2025A 非 GAAP 實際值事實表未直接涵蓋，以 CFO 稱 2026 年非 GAAP EPS 約年增 24%（2026-10-26）與 FY2026E 共識 3.11 回推約 2.51，只作基期；FY2025 GAAP 稀釋 EPS 為 2.11"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RMBS_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利、淨現金、FCF 轉換率高於淨利，但產品線隨伺服器與記憶體循環起伏"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：缺貨延續到 2027（Gartner 2026-08、JPMorgan／BofA 2026-09），NAND 供給在 2027 下半年追上需求（TrendForce 2026-07），客戶提早下單屬拉貨訊號（2026-10-26 CEO）","bargaining":{"up":"代工、基板、封測交期拉長、投入成本上升，非 GAAP 產品毛利率壓到 60.4%（區間下緣）；部分供應商為唯一來源","down":"前五大客戶占 FY2025 營收約 66%，Q3 累計最大客戶 23%、次大 18%，以三大 DRAM 廠為主；標準品沒有漲價空間（2026-07-27 CEO）","geo":"2025 年總部在美國以外的客戶占營收 82%；出口管制若擴及主力產品會受衝擊；唯一來源代工位在台海風險區"},"profit_pool_dir":"記憶體價值鏈這一輪利潤集中在缺貨漲價的 DRAM 廠，介面晶片環節分到量、分不到價","tam_table":[{"item":"DDR5 RCD 份額","value":"2025 年底約 mid-40%，高於 2024 年 early 40s（管理層自述，無第三方數據）"},{"item":"MRDIMM 總市場","value":"約 6 億美元，放量比 RCD 世代平緩（2026-10-26 CEO）"},{"item":"新產品占產品營收","value":"年初低雙位數百分比，目標 Q4 底達中雙位數（2026-07-27 CEO）"},{"item":"矽智財業務規模","value":"約 1.3 億美元，年增 10–15% 偏高端（2026-10-26 CFO）"},{"item":"RCD 市場總額、段 CAGR、營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"JEDEC 標準介面晶片的世代認證轉換成本，加上所有 DRAM 廠都要授權的記憶體介面專利組合；矽智財在 HBM、PCIe、硬體安全提早進入客戶架構規劃","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定（Q3 營收 2.183 億超指引上緣、第六代 9600 RCD 廣泛送樣）；定價面縮減（產品毛利 60.4% 在區間下緣、標準品不能漲價）；份額面管理層自述上升與第三方 Q1 搶份額報導方向相反，綜合判持平","peer_na_reason":"同業 ROIC 事實表未涵蓋，以營業利益率與 FCF 利潤率替代比較","threats":[{"level":"🟡","text":"Montage、Renesas 在第六代 RCD 與 MRDIMM 正面搶份額；Montage 營業利益率高於 RMBS，屬點對點競爭","p":"35%","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#0","customer_second_source#0"]},{"level":"🟡","text":"客戶自行開發主張不需授權的技術，或 DRAM 廠自製介面晶片","p":"15%","evidence_refs":["competitive_share_entrants#1","customer_second_source#1"]},{"level":"🟡","text":"記憶體架構替代：LPDDR／SOCAMM 板載方案與客戶降低單模組容量，壓低每模組價值；管理層稱互補不取代，目前屬增量","p":"20%","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"DOJ 反壟斷刑事調查若帶來營運做法限制，可能削弱授權與銷售條件；調查範圍未揭露","p":"20%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"高利益率×周轉待查：稅後營業利益率約 30.9%（TTM 營業利益率 36.7%×(1−16%)）；投入資本事實表未涵蓋，輕資產推測周轉偏高","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是雲端與 OEM 伺服器，決策者是 CPU 平台與 DRAM 廠的認證流程，付款者是模組廠；每支 DDR5 伺服器模組都要 RCD，屬需要不是想要；通道數由 8 增至 12–16 讓模組數增加，客戶降規格只降單模組容量不降模組數（2026-10-26 CEO）"},{"item":"決策層級","level":"🟡","text":"替代性要在每一代平台認證時衡量：同世代內換供應商要重新認證、轉換成本高，但每次世代轉換都重開競局；第一代 MRDIMM 已由對手先拿設計案，代理變數是各世代設計案歸屬與份額"},{"item":"價值鏈分配","level":"🟡","text":"買方集中（前五大約 66%）、標準品不能漲價，上游代工與封測交期拉長把產品毛利壓到 60.4%；這一輪缺貨利潤留在 DRAM 廠。所有 DRAM 廠都付權利金，撐住整體 79% 毛利"},{"item":"社會容忍度","level":"🟡","text":"專利授權依賴法律執行，10-K 自承執行可能需要訴訟；DOJ 反壟斷刑事調查進行中、範圍未揭露，若涉及授權或定價做法就成為政策上限；目前未見起訴，暫列中性偏負並寫入反證紀錄"}],"roiic":95,"reinvest_rate":18,"endo_ceiling":17,"formula_note":"單位為 %。NOPAT 約 3.43 億＝Q3 非 GAAP 營業利益 1.022 億×(1−16%)×4；再投資＝資本支出年化約 0.4 億（D&A 事實表未涵蓋，淨資本支出取 0～0.4 億）＋存貨每年增加約 0.4 億（Q2 1,600 萬、Q3 1,200 萬、Q4 計畫相近），再投資率 12%～23%，取 18%；增量 ROIC：GAAP 營業利益 FY2024 1.79 億→FY2025 2.60 億，稅後增量約 0.68 億，對照每年再投資約 0.7 億，約 95%；內生上界約 95%×18%≈17%。研發全數費用化，公式低估無形再投資，只當上界參考"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","RMBS":79.14,"688008.SS":65.82,"MRVL":52.21,"ARM":97.54,"SNPS":72.38,"unit":"%"},{"metric":"營業利益率","RMBS":36.73,"688008.SS":43.73,"MRVL":16.81,"ARM":17.3,"SNPS":11.03,"unit":"%"},{"metric":"FCF 利潤率","RMBS":39.31,"688008.SS":42.26,"MRVL":18.23,"ARM":28.55,"SNPS":29.18,"unit":"%"},{"metric":"研發密度","RMBS":25.11,"688008.SS":14.99,"MRVL":25.84,"ARM":57.49,"SNPS":30.6,"unit":"%"}],"competitors":[{"name":"688008.SS","gm":65.82,"om":43.73,"fcf_margin":42.26,"rd_intensity":14.99,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"MRVL","gm":52.21,"om":16.81,"fcf_margin":18.23,"rd_intensity":25.84,"period":"TTM ending 2026-07-31（4季加總）"},{"name":"ARM","gm":97.54,"om":17.3,"fcf_margin":28.55,"rd_intensity":57.49,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"SNPS","gm":72.38,"om":11.03,"fcf_margin":29.18,"rd_intensity":30.6,"period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"量為主（伺服器模組數、通道數、周邊晶片含量），價格零貢獻，併購零，淨回購約每年 1 個百分點","runway_years":"RCD 已全面滲透；MRDIMM、SOCAMM 新品類滲透率事實表未涵蓋，以管理層市場規模與放量節奏推估第二曲線約 3～5 年","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段再投資推導：增量 ROIC 約 95%×再投資率約 18%＝約 17%；研發費用化使公式偏低","segments":[{"item":"產品（RCD、周邊晶片、MRDIMM）","value":"Q3 1.143 億，年增 22%、季增 15%；Q4 指引 1.27–1.33 億，中點年增 34%；2026 全年約年增 24%"},{"item":"權利金","value":"Q3 0.770 億（去年同期 0.651 億）；Q4 指引 0.68–0.74 億；近乎全毛利"},{"item":"合約及其他（矽智財為主）","value":"Q3 0.270 億，年增 35%；矽智財總規模約 1.3 億、年增 10–15% 偏高端，部分認列在權利金"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"產品毛利 60.4% 在區間下緣，年比資料事實表未涵蓋；TTM 混合毛利 79.1% 對 FY2025 79.6% 小降"},{"item":"核心市占近 12 個月縮減","lit":true,"note":"第三方稱 Q1 被 Montage、Renesas 搶份額，管理層自述相反，爭議未決先計亮"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"標準品未提價"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"2026 年非 GAAP EPS 約年增 24%、營收約 18%，差 6 個百分點，來自營業槓桿"},{"item":"FCF／淨利 < 0.75 連 2 年","lit":false,"note":"FY2025 為 1.45 倍、FY2024 為 1.11 倍"},{"item":"SBC／營收 > 5% 且逐年上升","lit":false,"note":"Q3 為 7.8%，超過 5%，但逐年趨勢事實表未涵蓋，暫不計亮"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"客戶降低單模組容量但模組數增加"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"item":"維護性資本支出占 FCF > 60%","lit":false,"note":"Q3 資本支出 1,120 萬對 FCF 9,130 萬"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"營收連三年成長"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；回饋以回購為主，Q3 回購 1.35 億（含 1 億 ASR），公司目標回饋 FCF 的 40–50%，期末淨現金約 7.57 億、總債務約 0.2 億"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近一年 8-K 無併購；ChipAgents 為小額策略投資；歷史併購 ROIIC 事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價事實表未涵蓋；以判斷日遠期本益比 27.6 倍換算盈餘殖利率約 3.6%，Q3 回購時價位更高、殖利率更低；門檻要 10 年期殖利率低於約 1.6% 才過（10 年期殖利率事實表未涵蓋），判不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 年化約 6,800 萬（單季 1,710 萬×4），約市值 0.7%；稀釋股數 Q3 約 1.092 億、Q4 指引 1.09 億，淨稀釋接近零","grade":"過"}]},"valuation":{"basis":"遠期本益比（FY2026E 非 GAAP 共識 EPS）搭配 PEG，FY2027E 本益比作對照","peers":{"expanded":false,"reason":"事實表同業表只有利潤率，沒有同業倍數，無法做同級距倍數錨，改用自身歷史年度端點與遠期本益比"},"fwd_pe":27.56,"peg":1.11,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2026E 本益比 27.6 倍、FY2027E 22.1 倍，PEG 約 1.1（合理帶 1～2）；年度端點分位 P/E 55、P/S 41、EV/S 30，偏中低；淨現金約占市值 8%。合理偏便宜，但 EPS 處於循環高段，不給便宜結論","upside_short_pct":13.2,"upside_mid_pct":36.9},"trap_analysis":{"verdict":"🟡","label":"營業槓桿讓 EPS 跑贏營收，份額方向有爭議，循環高段盈餘需打折"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"客戶比過去提早下單、下游庫存看不清（2026-10-26 CEO：很難判斷）；TrendForce 預期 NAND 在 2027 下半年供給成長超過需求；日本分析認為記憶體成長多來自漲價、2027 年可能停滯；Montage 已拿第一代 MRDIMM；最大客戶占營收 23%","assumption":"本論點假設 2027 年訂單是真實需求，且新一代平台份額守得住","consequence":"2028 年產品營收年減兩成以上、毛利跌破 60%，EPS 退回約 3 美元，市場給 15 倍，股價約 45 美元，五年後較現價虧近半","ruling":"部分採納：Bear 機率給 30%，Base 的 2028 年 EPS 低於共識約 8%；與唯一致命點部分重疊（份額失守是這個故事的放大器），唯一致命點保留份額事件，循環轉向另列減碼條件","watch":"產品營收年增率（季）、Q1 指引是否守住正常季節性、RCD 份額年度揭露","evidence_refs":["supply_demand_durability#1","end_markets#5","competitive_share_entrants#3","customer_concentration_credit#3","customer_concentration_credit#0"],"fact_refs":["f_kpi1_product_revenue","f_kpi7_guidance_q4_2026_revenue"]},{"view":"論點成功但股東經濟變差","evidence":"產品線毛利約 60%，遠低於權利金的近乎全毛利，產品占比往上走會稀釋混合毛利；上游投入成本上升而標準品不能漲價；SBC 占營收 7.8%；回購買在高本益比；DOJ 調查若以罰款加民事求償收場會吃掉現金；Pomerantz 律所已在調查證券詐欺","assumption":"營收成長能等比例轉成每股 FCF","consequence":"營收年增兩成，但每股 FCF 只增個位數，FCF 利潤率由 39% 掉到 30% 出頭","ruling":"部分採納：混合毛利下滑是產品成長的代價，營業費用持平帶來的營業槓桿可以抵銷大半；FCF 利潤率 35% 設為第三個假設的門檻，罰款風險用清倉條件處理","watch":"TTM FCF 利潤率、非 GAAP 產品毛利率、稀釋股數、DOJ 法律程序揭露","evidence_refs":["regulatory_antitrust#0","lawsuit_class_action#0","major_events#0"],"fact_refs":["f_kpi6_non_gaap_product_gross_m","f_kpi5_sbc_gaap","f_peer_rmbs_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"FY2027、FY2028 共識 EPS 年增約 25%、26%，已把循環高段的成長寫進去；2026 年 EPS 成長（約 24%）快於營收（約 18%），倍數套在高峰盈餘上並不便宜；Q1 2026 指引不如預期就讓股價重設，對指引高度敏感","assumption":"FY2027E 22 倍本益比是便宜","consequence":"若 2028 年 EPS 持平，現價等於 22 倍持平盈餘，倍數壓到 18 倍就再跌約兩成","ruling":"反駁為主：自 6 月判斷日已跌約 39%，同期 FY1 共識近三個月上修 2.6%；淨現金約占市值 8%；Base 情境倍數由 27.6 倍降到 23 倍仍有約一成年化報酬，報酬不靠倍數擴張。但不給便宜結論","watch":"以未來一年共識 EPS 計算的本益比、共識月度修正方向","evidence_refs":["capital_markets_pricing#3","end_markets#5"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_net_debt_m"]},{"view":"論點失敗","evidence":"10-K 載明部分代工與材料為唯一來源，位在台海緊張與出口管制影響區；美國對中國半導體出口管制若擴及主力產品會受衝擊；各國關稅可能壓低客戶需求；2025 年美國以外總部客戶占營收 82%","assumption":"供應鏈與出口環境維持現狀","consequence":"單一夥伴中斷可讓產品出貨斷一到兩季；管制擴及記憶體介面晶片則失去部分客戶","ruling":"不進 Base，併入 Bear 機率；屬無法預測的政策事件，不寫預測，只設損益層吸收失敗條件：產品營收單季季減超過 20% 且公司歸因供應或管制","watch":"10-K／10-Q 風險因素變動、產品營收季減幅度、非 GAAP 產品毛利率","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":["f_kpi1_product_revenue"]},{"view":"論點失敗","evidence":"10-K 載明部分潛在客戶在評估或開發主張不需向 Rambus 授權的技術；替代技術若以相近成本提供相當效能，客戶可能改採；專利執行可能需要訴訟、結果不確定","assumption":"權利金段每季約 0.7～0.8 億美元可長期維持","consequence":"權利金近乎全毛利，每少 1,000 萬美元季營收約少 0.08 美元季 EPS","ruling":"反駁為主：2026-07-27 CEO 稱記憶體廠都要簽授權，Q3 權利金 0.770 億高於去年同期 0.651 億；屬十年尺度風險，以權利金年營收連 2 年下滑為警戒","watch":"權利金季營收、授權合約到期與續約揭露、專利訴訟","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1"],"fact_refs":["f_kpi0_revenue_gaap"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 141.17 → 本次 85.71（-39.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=141.17","side_b":"本次 price_at_dd=85.71","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 141.17 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 141.17 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 141.17 美元：Bull 價 226.8、Bear 價 55.5，五年期望值 −1.9%，基準年化 0.5%，不對稱比 0.83","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.83。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 141.17 美元：五年期望值 −1.9%，基準年化 0.5%，不對稱比 0.83","side_b":"本次情境、股價 85.71 美元：五年期望值 +61.7%，基準年化 11.1%，不對稱比 3.89","ruling":"再換股價、情境不動：起點價下跌 39.3%，五年期望值多 63.5 個百分點，基準年化多 10.5 個百分點，不對稱比由 0.83 升到 3.89。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"RCD 份額方向","cause":null,"prior_field":null,"side_a":"管理層：2025 年底 DDR5 RCD 份額約 mid-40%，高於前一年 early 40s，預期續升；Q4 產品營收指引中點年增 34%","side_b":"第三方：Q1 2026 產品營收年增約 15% 低於市場，Montage、Renesas 搶份額；第一代 MRDIMM 由對手先拿設計案（2026-10-26 法說問答）","ruling":"可調和，屬程度差異：Q1 有一次性製造問題（2026-07-27 CEO），Q3、Q4 加速；但 MRDIMM 第一代落後是事實。護城河方向只給持平，不給擴大","evidence_level":"管理層自述對單一第三方報導，雙方都缺獨立份額數據","settle_metric":"2027-02 Q4 法說的 RCD 份額揭露；2027 全年產品營收年增是否≥20%","if_then":["若 Q4 法說重申份額不低於 mid-40% 且 Q4 產品營收≥1.27 億 → 加第二批到目標倉位三分之二","若份額揭露低於 40% 或揭露失去任一 DRAM 廠第六代主供應 → 清倉","反向：若管理層不再給份額數字且產品年增跌破 15% → 減碼一半"],"evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#2","end_markets#2"]},{"axis":"2027～2028 年需求：延續還是拉貨","cause":null,"prior_field":null,"side_a":"管理層稱 2027 需求轉強、訂單能見度變好；Gartner 預期缺貨延續到 2027；JPMorgan 稱 2028 年初前無顯著新產能，BofA 預期 2028 仍偏緊","side_b":"TrendForce 預期 NAND 在 2027 下半年供給成長超過需求；日本分析認為記憶體成長多來自漲價；客戶降低單模組容量；客戶提早下單而下游庫存看不清（2026-10-26 CEO）","ruling":"2027 年可調和、2028 年方向相反屬不可調和：2027 年採信 A（有訂單能見度支撐，Base 只比共識低 2%）；2028 年採信 B，依據是 NAND 供給轉折預測與提早下單訊號，反映在 Bear 機率 30% 與 Base 2028 年 EPS 低於共識約 8%","evidence_level":"產業預測對產業預測，加上公司訂單訊號","settle_metric":"2027 年各季產品營收年增率與 Q1、Q2 指引；DRAM 廠資本支出與庫存","if_then":["若 2027 上半年產品營收年增仍≥20% 且管理層維持全年轉強說法 → 維持倉位，2028 年假設上修至共識","若產品營收連 2 季年減 → 減碼一半","反向：若價格先跌而產品營收與份額都未惡化 → 分批反買"],"evidence_refs":["supply_demand_durability#1","end_markets#5","substitute_technology#2","supply_demand_durability#0","supply_demand_durability#2"]},{"axis":"DOJ 反壟斷刑事調查","cause":null,"prior_field":null,"side_a":"公司自 2026 Q1 回應聯邦大陪審團傳票，可能結果含罰款、改變營運做法或禁制令；媒體報導公司為調查對象；Pomerantz 律所以 2026-02-03 單日跌 13.42% 為由調查證券詐欺","side_b":"迄今未見起訴、和解或時程，也未見 FTC、歐盟行動；集體訴訟尚未提起；淨現金約 7.57 億可吸收一般罰款","ruling":"不可裁決至調查出現程序性進展：調查範圍與受影響營收公司未揭露，決勝數據今天不存在，不得稱風險已解；先用分批與清倉條件處理，不計入 Base","evidence_level":"公司 10-Q 一手揭露，影響金額缺口","settle_metric":"10-Q／8-K 法律程序段落：起訴、認罪協議、和解金額或結案","if_then":["若公司或高管遭刑事起訴或簽認罪協議 → 清倉","若以罰款結案、無營運限制且金額低於淨現金一成 → 移除風險折價，允許補滿倉位","反向：若揭露調查涉及權利金或產品定價做法 → 停止加碼並重估權利金段"],"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","major_events#0","lawsuit_class_action#0","regulatory_antitrust#2"]},{"axis":"產品毛利率守不守得住","cause":null,"prior_field":null,"side_a":"CFO：近期毛利 60–63%、長期 60–65%，Q4 可能小升，2026 全年落在區間中段（2026-10-26）","side_b":"Q3 為 60.4% 落在下緣，上游投入成本上升、標準品不能漲價（2026-07-27 CEO）；2026-07-27 法說被問到拉份額是否壓毛利時未正面回答；10-K 提示關稅與唯一來源供應風險","ruling":"可調和，屬程度差異：管理層用內部降本抵銷成本上升，但上游缺貨延續到 2027 時下緣能否守住未證；設連 2 季低於 60% 為減碼條件","evidence_level":"管理層指引對最新一季實績","settle_metric":"Q4 2026 與 2027 各季非 GAAP 產品毛利率","if_then":["若連 2 季低於 60% → 停止加碼並減碼三分之一","反向：若回到 62% 以上且份額不降 → 解除毛利疑慮"],"evidence_refs":["geo_supply_chain#1","reg_tariff_export#1"]},{"axis":"揭露透明度與財務長更替","cause":null,"prior_field":null,"side_a":"新任財務長 2026-07-27 首次主持法說，同場宣布只以 ASC 606 營收口徑給指引、不再揭露授權帳單","side_b":"此後兩季營收都超過指引上緣，逐季指引與回饋 FCF 四到五成的政策延續","ruling":"可調和：未見財務品質問題，但權利金段少了一個領先指標；改用權利金季營收與合約續約揭露監測","evidence_level":"法說逐字稿","settle_metric":"權利金季營收與 10-Q 合約到期揭露","if_then":["若權利金季營收連 2 季低於公司指引下緣 → 停止加碼","反向：若權利金維持指引內 → 不調整"],"evidence_refs":[]},{"axis":"現在進場與否的最強論證對打","cause":null,"prior_field":null,"side_a":"現在就買：FY2027 共識本益比約 22 倍、三年 EPS 年化約 25%、淨現金約占市值 8%、Q2 與 Q3 連續超指引；自 6 月判斷日以來股價跌 39%，同期 FY1 共識上修 2.6%","side_b":"現在就賣：EPS 成長靠營業槓桿與循環高峰，提早下單可能是拉貨，Montage 已在 MRDIMM 先發，DOJ 刑事調查以公司為對象；週線跌破 52 週與 104 週均線，趨勢未修復","ruling":"以 A 為主但分批：基本面與估值站在買方，份額與 DOJ 兩個二元事件未解；首批只建目標倉位三分之一，第二批綁 Q4 財報驗證，DOJ 結案前不補滿","evidence_level":"財報實績與共識對照，兩個二元事件缺決勝數據","settle_metric":"2027-02 Q4 財報與份額揭露；DOJ 程序進展","if_then":["若 Q4 財報驗證通過 → 加到三分之二","若任一清倉條件觸發 → 清倉","反向：若價格再跌 15% 而所有減碼條件都沒觸發 → 分批反買一批"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"估值結論漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份估值結論 🟠（判斷日股價 141.17）","side_b":"本次 🟡（股價 85.71，FY2026E 本益比 27.6 倍、FY2027E 約 22.1 倍）","ruling":"估值改善主因是股價下跌約 39%；以 2026-07-30 快照 FY1 共識 3.03 粗算，前份價位約 46.6 倍，現為 27.6 倍，同期 FY1 共識上修 2.6%，屬價格驅動","evidence_level":"事實表股價與共識快照","settle_metric":"以未來一年共識 EPS 計算的本益比","if_then":[],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"陷阱判斷漂移","cause":"新證據","prior_field":["trap"],"side_a":"前份陷阱判斷 🟢","side_b":"本次 🟡：EPS 成長快於營收逾 5 個百分點（2026 年 EPS 約 +24%、營收約 +18%）；份額方向有第三方反證；MRDIMM 放量比預期平緩、客戶降低單模組容量（2026-10-26 法說）；產品毛利落在區間下緣","ruling":"新證據多數出現在前份之後的兩次法說，降一級合理","evidence_level":"法說逐字稿與第三方報導","settle_metric":"衰退信號亮燈數","if_then":[],"evidence_refs":["substitute_technology#2","competitive_share_entrants#3"]},{"axis":"總評維持","cause":"新證據","prior_field":["signal"],"side_a":"前份總評 B","side_b":"本次維持 B：估值由偏貴轉合理、Q3 與 Q4 營運加速，被份額爭議、產品毛利下緣與 DOJ 刑事調查抵銷","ruling":"正負新證據相抵，總評不變","evidence_level":"財報與法說","settle_metric":"Q4 財報、份額揭露、DOJ 進展","if_then":[],"evidence_refs":["regulatory_antitrust#0"]},{"axis":"新增欄位首次填寫","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未填（舊格式沒有這些欄位）","side_b":"本次：護城河方向 →、五年後成長空間 🟡、公司類型品質複利成長（次類循環/商品）、循環位置晚循環、情境機率 25／45／30、最大回撤 −35%～−50%；裁決與角色由程式依矩陣產生","ruling":"格式改版後首次填寫，沒有可比的前值","evidence_level":"方法變動","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重啟條件首次設定","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重啟條件未填","side_b":"本次：Q4 2026 財報（2027-02）產品營收≥1.27 億美元且管理層重申 DDR5 RCD 份額不低於 mid-40%","ruling":"約束改為事件錨：未解的是份額方向，不是價格；舊份沒有可比門檻","evidence_level":"方法變動","settle_metric":"2027-02 Q4 財報","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點變動","cause":"方法變動","prior_field":null,"side_a":"前份無唯一致命點（Single Thing 未填）","side_b":"本次 Single Thing：下一代平台（第六代 9600 RCD、第二代 MRDIMM）認證中失去任一 DRAM 廠主供應地位、RCD 份額跌破 40%，觸發即清倉","ruling":"產品營收占五成且是唯一高成長線，份額是數學上最大的單一敏感度項，因此設為唯一致命點","evidence_level":"方法變動，依據份額爭議新證據","settle_metric":"每年 2 月法說份額揭露","if_then":[],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"清倉與減碼指標首次設定","cause":"方法變動","prior_field":null,"side_a":"前份無清倉、減碼指標（未填）","side_b":"本次：RCD 份額低於 40% → 清倉；DOJ 起訴公司或高管 → 清倉；產品營收連 2 季年減 → 減碼一半；非 GAAP 產品毛利率連 2 季低於 60% → 減碼三分之一","ruling":"舊份只有論點層門檻，本次補上動作層門檻","evidence_level":"方法變動","settle_metric":null,"if_then":[],"evidence_refs":["regulatory_antitrust#0","supply_demand_durability#1"]},{"axis":"假設與風險門檻改寫","cause":"方法變動","prior_field":["H","R"],"side_a":"前份：H1 產品年成長≥15%、份額≥40%；H2 介面晶片市場由 8 億擴至 20 億美元以上；H3 遠期本益比維持 25 倍以上，跌破 22 倍且共識下修即反轉；R2 產品連 2 季季減","side_b":"本次：H1 2027 年產品年增≥20%、份額≥40%；H2 新產品占產品營收 2028 年≥25%、產品五年年化≥15%；H3 改為 FCF 利潤率≥35%、矽智財年增≥10%；R2 改為產品營收連 2 季年減","ruling":"H1 門檻上調，因 2026 年產品年增已約 24%（2026-10-26 CFO）；H2 改用公司實際揭露的指標（MRDIMM 市場約 6 億、新產品占比）；H3 的估值溢價假設移進情境樹，不再當論點，前份反轉線未觸發（FY1 遠期本益比 27.6 倍、共識上修）；R2 改年減，因上下半年季節性（2026-10-26 CEO）會讓 Q1 季減成為假訊號；前份 R3 架構替代保留為 R6","evidence_level":"方法變動加法說新數據","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q4 2026 產品營收落在指引內並重申份額","type":"假設驗證","maps_to":"H1","metric":"Q4 2026 產品營收；DDR5 RCD 份額自述","threshold":"產品營收≥1.27 億美元且份額不低於 mid-40%","action":"通過則加第二批到目標倉位三分之二","source_freq":"季報 8-K 與法說","date":"2027-02","evidence_refs":["competitive_share_entrants#3"]},{"n":2,"text":"下一代平台認證失守","type":"Single Thing","maps_to":"Single Thing","metric":"DDR5 RCD 份額；三大 DRAM 廠第六代 RCD 主供應地位","threshold":"份額低於 40%，或揭露失去任一 DRAM 廠第六代主供應","action":"清倉","source_freq":"年度（Q4 法說）與設計案公告","date":"2027-02","evidence_refs":["competitive_share_entrants#3","customer_concentration_credit#3"]},{"n":3,"text":"記憶體循環轉向","type":"減碼","maps_to":"R2","metric":"產品營收年增率（季）","threshold":"連 2 季年減","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#1","end_markets#5"]},{"n":4,"text":"DOJ 刑事起訴","type":"清倉","maps_to":"R4","metric":"DOJ 反壟斷調查程序","threshold":"公司或高管遭起訴或簽認罪協議","action":"清倉","source_freq":"10-Q／8-K 法律程序揭露","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2"]},{"n":5,"text":"產品毛利率跌破區間下緣","type":"減碼","maps_to":"R3","metric":"非 GAAP 產品毛利率","threshold":"連 2 季低於 60%","action":"停止加碼並減碼三分之一","source_freq":"季報與法說","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":6,"text":"價格先跌、基本面無損","type":"加碼","maps_to":"H1","metric":"股價對照所有減碼與清倉條件","threshold":"股價約 73 美元以下（較判斷日再跌 15%）且減碼、清倉條件都未觸發","action":"分批反買一批","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":7,"text":"估值過高不追","type":"估值rearm","maps_to":"H2","metric":"以未來一年共識 EPS 計算的本益比","threshold":"≥35 倍停止加碼；≥40 倍減碼三分之一","action":"不追，停止加碼","source_freq":"月度共識快照","date":null,"evidence_refs":[]},{"n":8,"text":"份額訊號轉弱","type":"風險","maps_to":"R1","metric":"產品營收年增率與管理層份額說法","threshold":"管理層停止給份額數字且產品年增低於 15%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":9,"text":"現金流與矽智財驗證","type":"假設驗證","maps_to":"H3","metric":"TTM FCF 利潤率；矽智財年增率","threshold":"FCF 利潤率≥35%；矽智財年增≥10%","action":"未達則停止加碼","source_freq":"季報","date":null,"evidence_refs":[]},{"n":10,"text":"Q4 財報後全份複審","type":"複審日期","maps_to":null,"metric":"全份重跑","threshold":"2027-02 財報公告後一週內","action":"重跑判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"DDR5 RCD 份額（管理層年度揭露）","bear_threshold":"低於 40%，或失去任一 DRAM 廠第六代主供應","window":"2027-02 起每年 Q4 法說","source":"公司法說逐字稿、設計案公告","last_status":"warning"},{"metric":"產品營收年增率（季）","bear_threshold":"連 2 季年減","window":"2027-Q1 至 2028-Q4","source":"公司 8-K 新聞稿","last_status":"ok"},{"metric":"非 GAAP 產品毛利率","bear_threshold":"連 2 季低於 60%","window":"逐季","source":"公司法說與 8-K","last_status":"warning"},{"metric":"DOJ 反壟斷刑事調查","bear_threshold":"公司或高管遭起訴或簽認罪協議","window":"至結案","source":"10-Q／8-K 法律程序揭露","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 RMBS 當記憶體價格循環股折價，但產品營收看伺服器模組顆數與每模組晶片數，不看 DRAM 價格；客戶降規格降的是單模組容量不是模組數，Q4 產品指引年增 34%，FY1 共識近三個月上修"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-23.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"Q4 2026 財報（2027-02）產品營收≥1.27 億美元且管理層重申 DDR5 RCD 份額不低於 mid-40%","exec_line":"首批建倉為目標倉位三分之一；Q4 財報驗證通過加到三分之二；DOJ 以無營運限制結案後才補滿；任何清倉條件觸發即出場"},"reasoning":{"industry":"Q3 營收 2.183 億美元、年增 22%，高於公司指引 2.10–2.16 億：產品 1.143 億（52%）、權利金 0.770 億（35%）、合約及其他 0.270 億（12%）。最新一季 GAAP 營業利益率 38.3%、非 GAAP 46.8%，非 GAAP 產品毛利率 60.4%，TTM 混合毛利率 79.1%。產業時鐘判 III：上游交期拉長、客戶比過去提早下單、記憶體經濟性迫使客戶降低單模組容量（2026-10-26 法說），依據是供需訊號而非股價。供需持久性：週期性將反轉。AI 推動的記憶體缺貨預期延續到 2027（Gartner；JPMorgan 稱 2028 年初前無顯著新產能），但 TrendForce 預期 NAND 在 2027 下半年供給成長將超過需求，反轉時點落在 2027 下半年到 2028。單點依賴：前五大客戶占 FY2025 營收約 66%、Q3 累計最大客戶 23%、次大 18%，屬集中度風險，不是護城河證據；10-K 也載明部分代工為唯一來源且位在台海風險區。產業態勢三軸：競爭面惡化（Montage 先拿第一代 MRDIMM 設計案）、需求結構轉好（CPU 對 GPU 比例上升、伺服器通道數由 8 增至 12–16）、其他結構變數為 DOJ 反壟斷刑事調查與出口管制，裁決為雙向拉鋸。","moat":"機制：DDR5 RCD 是 JEDEC 標準件，每一代平台都要經 CPU 廠與三大 DRAM 廠認證，同世代內換供應商成本高；三十年記憶體介面專利讓所有 DRAM 廠都要付權利金（2026-07-27 CEO：記憶體廠都要簽授權）。方向證據：管理層稱 2025 年底份額約 mid-40%、高於前一年；Q3 產品營收年增 22%、Q4 指引中點年增 34%，快於伺服器出貨的雙位數成長（2026-07-27 CEO）。反向證據：第三方稱 Q1 產品年增約 15% 低於市場、Montage 與 Renesas 搶份額；第一代 MRDIMM 由對手先拿設計案（2026-10-26 法說問答）；標準品不能漲價、產品毛利 60.4% 落在區間下緣。同業比較：同業 ROIC 事實表未涵蓋，改看利潤率；Montage 營業利益率 43.7%、FCF 利潤率 42.3%，都高於 RMBS 的 36.7%、39.3%，RMBS 混合毛利 79.1% 是權利金撐出來的。執行力 8 分（連兩季超指引上緣、第六代 9600 RCD 已廣泛送樣），定價力 6 分（標準品無漲價權、上游擠壓）；等級 B，方向持平：執行穩定、定價小幅縮減，份額爭議在 2027-02 法說揭露前不給擴大。","growth":"成長來源：量為主（伺服器出貨轉雙位數成長、通道數增加、周邊晶片放量），價格不貢獻（標準品不漲價），沒有併購，淨回購每年約 1 個百分點。三年共識非 GAAP EPS：FY2026E 3.11、FY2027E 3.88、FY2028E 4.89（Koyfin，家數事實表未涵蓋；營收共識 7–8 位分析師），以 FY2025A 回推約 2.51 計，年化約 24.9%；內生上界約 17%（見護城河段推導），缺口約 8 個百分點，歸因營業槓桿約 7 個百分點（營業費用季約 7,000 萬持平而產品營收放大，Q4 非 GAAP 總成本指引 1.20–1.24 億對營收 2.27–2.33 億）與淨回購約 1 個百分點，不依賴重新評價。成長空間：RCD 已是每支 DDR5 伺服器模組的標配，滲透率天花板已到；第二條曲線有來源但都比 RCD 平緩，MRDIMM 市場約 6 億美元但放量較淺（2026-10-26 CEO），SOCAMM2 約 2028 年上市且屬利基，矽智財約 1.3 億、年增 10–15% 偏高端。衰退信號亮兩個（EPS 成長快於營收逾 5 個百分點、核心份額方向有第三方反證），長期成長性中等。","governance":"FCF 轉換：FY2025 FCF 3.33 億對淨利 2.30 億（1.45 倍），FY2024 為 1.11 倍；FY2023 淨利 3.34 億遠高於營業利益約 0.91 億（營收 4.61 億×19.8%），屬非營業或稅務項目，該年轉換率不具代表性（事實表 financial_history，yfinance 年度財報）。Q3 FCF 0.913 億、占營收 41.8%。SBC 單季 1,710 萬、占營收 7.8%、占 GAAP 營業利益 20.5%。現金去向：Q3 營業現金流 1.025 億，回購 1.35 億（含 1 億 ASR），存貨增加 1,200 萬，期末現金及有價證券 7.77 億、淨現金約 7.57 億；公司目標把 FCF 的 40–50% 回饋股東；近一年 8-K 無併購。計分：併購項目不適用；回購買在遠期本益比約三十倍上下，盈餘殖利率約 3～4%，達不到公債殖利率加 2 個百分點；SBC 淨稀釋方面，Q3 稀釋股數約 1.092 億（非 GAAP 淨利 9,170 萬÷EPS 0.84），Q4 指引 1.09 億，回購大致抵銷稀釋，通過。","valuation":"現價 85.71 對 FY2026E 共識 EPS 3.11 為 27.6 倍、對 FY2027E 3.88 為 22.1 倍；三年非 GAAP EPS 年化約 24.9%，PEG 約 1.11（27.56÷24.9），落在合理帶。Trailing P/E 35.4 倍、P/S 11.5 倍、EV/S 10.6 倍，在少數年度端點中的分位分別 55、41、30，這不是五年分位，五年高低點事實表未涵蓋，五年分位留空。淨現金 7.57 億約占市值 8%，EV 對 FY2026E 營收 10.1 倍。短期上檔：FY2027E 3.88×25 倍＝97 美元，約 +13%；中期上檔：Base 第三年 EPS 5.10×23 倍＝117 美元，約 +37%。賣方平均目標價約 137～145 美元（2026-04 至 07 快照，Q3 前；區間 90～172，最高最低比 1.9 倍），明顯高於本次判斷；本次比共識保守，理由是共識 2028 年 EPS 年增約 26% 沒有反映記憶體循環轉向。分母為非 GAAP，排除 SBC 與攤銷，Q4 GAAP EPS 指引 0.68–0.76 約比非 GAAP 低 18%，不改變結論方向。","premortem":"三種看錯方式的證據與裁定寫在反證紀錄。陷阱判斷中等：衰退信號亮兩個（EPS 成長快於營收逾 5 個百分點、核心份額方向有第三方反證），FCF 轉換與資本支出負擔都健康；SBC 占營收 7.8% 超過 5%，但逐年趨勢事實表未涵蓋。動能：26 週跌 23.1%，RSI 39.7 未到超賣；週線收盤 84.1 低於 52 週均線 105.4、略低於 104 週均線 85.8，仍高於 250 週均線 62.4 且其 13 週斜率 +1.5%，中期趨勢未修復、長期多頭結構未破。歷史最大回撤與空方最強數字事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺三筆錢：DRAM 廠與模組廠買的伺服器記憶體介面晶片（約五成營收）、所有 DRAM 廠付的專利權利金（約三成五）、晶片設計商付的矽智財授權（約一成二）；錢卡在 JEDEC 標準介面晶片的平台認證節點","moat":"護城河方向持平：RCD 共同領先者靠 JEDEC 平台認證與專利組合守住地位，但標準品沒有定價權、毛利被上游擠壓，Montage 先拿第一代 MRDIMM，份額方向有爭議","growth":"五年後成長空間中等：RCD 滲透已到頂，成長靠份額與每模組含量，MRDIMM、SOCAMM2、矽智財等第二曲線有來源但都比 RCD 世代平緩","capital":"資本配置中等：現金轉換強、淨現金充裕、回購大致抵銷稀釋，但回購買在偏高的價位；近一年沒有併購","valuation":"現價要求 2027–2028 年 EPS 每年增約兩成、倍數不再大幅下修；我大致相信 2027 年，對 2028 年存疑，估值合理但不給便宜結論","how_wrong":"最可能看錯在三處：把 2027 年提早下單當成真需求而忽略 2028 年記憶體循環轉向、Montage 在新一代平台拿走份額、DOJ 刑事反壟斷調查以起訴收場"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 RMBS 當記憶體價格循環股折價，但產品營收看伺服器模組顆數與每模組晶片數，不看 DRAM 價格；客戶降規格降的是單模組容量不是模組數，Q4 產品指引年增 34%，FY1 共識近三個月上修","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":85.71,"week26_return_pct":-23.13,"consensus_rev_3m_pct":2.64,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母為非 GAAP EPS，排除 SBC 與攤銷；GAAP EPS 約低 18%，屬既有口徑差異，不是本次爭點"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報、2027 Q1 指引與 DDR5 RCD 份額揭露","impact":"高","watch":"產品營收是否≥1.27 億美元、份額是否重申 mid-40%"},{"date":null,"date_precision":null,"type":"regulatory","event":"DOJ 反壟斷刑事調查進展（起訴、認罪協議、和解或結案）","impact":"高","watch":"10-Q／8-K 法律程序段落"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"新伺服器平台放量、MRDIMM 隨第二家 CPU 平台放量、第六代 RCD 量產","impact":"中","watch":"新產品占產品營收比重、MRDIMM 設計案歸屬"},{"date":"2027-09","date_precision":"quarter","type":"macro","event":"記憶體供需轉折觀察期（NAND 供給成長預期超過需求）","impact":"中","watch":"客戶下單節奏、DRAM 廠資本支出與庫存"}],"_projected_from":"v19"}
```
