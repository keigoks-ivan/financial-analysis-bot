你是 stock-analyst v20 的**散文層（prose）agent**，標的 MTSI（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：MTSI　日期：2026-11-08　archetype：None　前份裁決：2026-05-24　B（衛星觀望·thesis 完整｜Q2 FY26 Adj EPS $1.09 beat + DC +48% FY25 至 $293M + 800G/1.6T 200G/lane photodetector 全 module maker design wins + Adj GM 58.5% 目標 60%；但 Fwd PE FY26 76x / FY27 56x 已 stretched + BB 107.9% 上突破 + 52w +127%，等回測 $290-330 或 BB 中軌 $257 區再評估）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1965B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（689B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（997B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1404B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1258B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（517B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（966B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2061B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3639B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2486B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1965           3524-5035      5 條（2–6 內）  
s3                  8000         689           5118-7311      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3659          7939-11341      5 條（2–6 內）  
s6                 11000         517          7338-10483      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         966           1774-2534      5 條（2–6 內）  
s10                 5000        2061           2057-2939      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2486           2000-2514      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5126B；至少需散文≈39.87KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−60
−45.3%
−41.37
−40%
−40
−23.3%
−14.4%
−2.4%
0
0.57
0.6%
0.75
0.81
0.85
1.0
1%
01
1
1.1
1.18
1.2
1.38
1.4
1.5
1.6
1.633
1.646
1.79
1.881
1.97
2
02
2%
2.03
2.09
2.16
2.2%
2.21
2.29
2.46
2.93
3
3%
3.17
3.407
3.57
3.855
4%
4
4.15
4.248
4.25
4.5
4.517
4.6
5
05
5%
5.0
5.1
5.6%
5.6
5.60
6
06
6%
6.8
6.9
7
07
7%
7.5
7.6
7.924
8
08
8.11
8.5
8.54
8.6
09
9.0
9
9.4
9.44%
9.5
10%
10
10.1%
10.11
10.2
11
11.0
11%
11.4
11.85
12
12.14
12.48
12.5
13%
13.3
14.0
14%
14
15%
15
15.5
16%
16.5
17%
18
19
19.4
19.5
20%
20
20.87
20.9%
22%
22
22.5
23
23.2%
24
24.5
24.7
25
25%
26
27
27.8%
28.4%
30
30%
30.6%
31.6%
32%
32.3%
35%
35.7%
36
37%
38%
38
38.2%
39%
40%
40.8%
41%
42
42%
44%
45%
45.3%
46%
46
47%
48%
48.2%
48.95
49
50%
50
52
54.0%
55%
56
56.5%
56.7%
57%
57.1%
59.5%
60%
60
60.2%
61%
61.3%
62%
62
62.5%
63%
65.8%
70
71.0
74%
76
79%
80%
85
90
100
100%
104
125
127
127.5
150%
150
152
161
170
195
200
210.98
227
230
250
253
257
262.51
280
290
308
330
331
377.56
385.98
448
607.5
660
920
2024
2025
2026
2027
2028
2029
2030
2031
20261108
1,000
2,390
6,000
6,100
6,440
7,150
7,210
7,637
7,900
9,560
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
{"meta":{"ticker":"MTSI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"MACOM Technology Solutions Holdings, Inc."},"oneliner":"MACOM 基本面加速，股價半年卻跌 41%：FY27 資料中心 base case 年增 80%，營益率站上 40%，前瞻本益比 24.7 倍但分母偏舊；爭點是 2028 訂單會不會回吐，Base 年化約 10%，宜分批小量進場，不重押。","thesis":{"H":[{"id":"H1","text":"資料中心完成 FY27 base case，FY28 不衰退","2y":"FY27 資料中心營收 ≥9 億美元，FY28 年增為正","5y":"FY31 資料中心營收 ≥18 億美元，約占公司一半","10y":null,"threshold":"FY27 第一季季增 ≥10%；FY27 資料中心營收 ≥9 億美元；公司訂單出貨比 ≥1.0","source":"MACOM 季度法說與 8-K","drift_rule":"TTM 偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"利潤率提升有一部分是結構性，短缺結束後仍能守住","2y":"FY27 調整後毛利率 ≥62.5%、營益率 ≥40%","5y":"FY31 調整後毛利率 ≥62%、營益率 ≥38%","10y":null,"threshold":"FY27 第一季調整後毛利率 62–63%、營益率約 40%；之後每季毛利率增加 25–50 基點","source":"MACOM 季度 8-K 與法說","drift_rule":"TTM 偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H3","text":"NPO 與 CW 雷射在 2028 成為第二條曲線，接住資料中心放緩","2y":"CW 雷射完成認證，Lowell 第二階段於 2027 年中啟動","5y":"FY31 NPO 與 CW 雷射合計營收 ≥5 億美元","10y":null,"threshold":"FY28 結束前至少一項有量產營收；第二階段擴產不晚於 2027 年底啟動","source":"MACOM 法說；2026-08-06 法說執行長稱 NPO 有 10–20 個開發案，部分不會量產","drift_rule":"TTM 偏離連 4 季 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉；第二階段延到 2028 視為削弱"},{"id":"H4","text":"工業國防提供資料中心以外的地板","2y":"FY27 工業國防年增 ≥30%，營收約 6.9 億美元","5y":"FY31 工業國防營收 ≥12 億美元","10y":null,"threshold":"FY27 年增 ≥30%；RTP 廠產能擴充按計畫進行","source":"MACOM 季度法說","drift_rule":"TTM 偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"雲端資本支出消化與重複下單：訂單無最低採購量，交期拉長時客戶傾向多下單，供給一鬆就回吐","h_ref":"H1","clock":"🔥","threshold":"訂單出貨比連 2 季低於 1.0；或資料中心季增轉負；五大雲端資本支出年增連 2 季低於 15%（目前讀值事實表未涵蓋）","evidence_refs":["supply_demand_durability#1","customer_concentration_credit#2","customer_second_source#0"]},{"id":"R2","text":"架構替代：全整合 CMOS 在 NPO 或 CPO 勝出，分離式 TIA、驅動器與光偵測器的市場縮小","h_ref":"H3","clock":"🐢","threshold":"主要超大規模業者量產採全整合方案，且公司 FY28 NPO 無營收","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"]},{"id":"R3","text":"中國與出口管制：FY25 中國占營收 28.4%，管理層預期客戶組合移轉的說法未經驗證","h_ref":"H1","clock":"⚡","threshold":"中國模組廠禁令實施，且下季指引低於前季營收 5% 以上","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R4","text":"代工與關鍵材料：SiGe 委外、特定製程單一來源，資料中心成長 80% 依賴代工配合；簽下確定承諾後，下行時彈性變小","h_ref":"H1","clock":"🔥","threshold":"營收低於指引下緣且歸因供應；或揭露的代工承諾超過年營收 20%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R5","text":"競爭與客戶集中度：新進者搶 TIA 與驅動器份額，10-K 前十大客戶占比由 48% 升到 57%","h_ref":"H2","clock":"🔥","threshold":"調整後毛利率連 2 季環比下滑 1 個百分點以上，且競爭者宣布 200G／lane 光偵測器量產；或前十大客戶占比超過 60%","evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#1"]},{"id":"R6","text":"併購失誤：2030 年 50 億美元目標需要新技術與新市場，現金累積後大型併購的機率上升","h_ref":"H2","clock":"🐢","threshold":"單筆併購超過市值 10%；或 GAAP 淨利連 3 年低於調整後淨利 60%","evidence_refs":[]}],"single_thing":{"description":"FY28 結束前，資料中心營收出現連續兩季季減。","why_fatal":"資料中心 FY27 約占營收 47%，也是增量獲利的主要來源；Base 與 Bear 的 FY29 EPS 相差 46%，本益比再從 22 倍壓到 15 倍，是情境樹中最大的單一敏感項。","if_happens":"清倉，等訂單出貨比連續兩季回到 1.0 以上再重做研究。","how_monitor":"每季法說的資料中心營收與季增率、訂單出貨比，輔以雲端資本支出指引。","probability":"30%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.87,"peg_fy2":1.0,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":5.6,"FY2027E":8.54,"FY2028E":10.11,"FY2029E":12.48},"fy_end_month":9,"eps_basis":"調整後（Non-GAAP）稀釋 EPS；FY26A 5.60 美元來自 2026-11-05 法說，FY27E–FY29E 為 2026-11-07 Koyfin 共識，財報後尚未完整更新"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MTSI_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"三大終端市場的類比與化合物半導體公司，擁有自有晶圓廠；FY23 營收僅年減 4% 仍維持 59.5% 毛利率，但資料中心占比快速上升，週期性正在抬高。"},"industry":{"clock_phase":"II","sd_verdict_source":"擴張期依據：FY26 訂單出貨比 1.5、第四季 1.4，交期拉長，SiGe 代工開始要求確定承諾。供需判斷為週期性將反轉，時間點在 2027 之後：Lumentum 稱磷化銦雷射緊到 2027，但 LightCounting 指光模組需求與雲端資本支出週期高度相關，2027–2031 成長趨緩。","bargaining":{"up":"SiGe 代工（Tower、ST、GlobalFoundries）開始要求確定承諾，議價權往代工廠移動；特定製程通常單一代工來源。","down":"管理層預期超大規模業者會把份額分給多家供應商；FY25 前十大直接與經銷客戶占 56.7%，終端前十大低於 40%（2026-08-06 法說，執行長）。","geo":"中國占 FY25 營收 28.4%，多數產品受出口管制；美國自有晶圓廠在國防與本土 5G 構成優勢。"},"profit_pool_dir":"利潤池往光互連遷移，公司搭上順風；若全整合 CMOS 在 NPO 勝出，利潤會流向大型整合廠。各環節營業利益占比事實表未涵蓋。","tam_table":[{"item":"2027 SAM 合計","value":"約 150 億美元（管理層估計，2026-11-05 法說）"},{"item":"SAM 結構","value":"工業國防 60 億、資料中心 60 億、電信 30 億美元（2026-08-06 法說，執行長）"},{"item":"SAM 年增","value":"2026 到 2027 約 20–30%；管理層承認對市場數字做過重設"},{"item":"隱含滲透率","value":"FY27 共識營收 19.4 億 ÷ 150 億，約 13%"},{"item":"資料中心成長","value":"2024 年 +35%、2025 年 +48%、FY26 +74%、FY27 base case +80%"},{"item":"營業利益池占比 5 年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"化合物半導體製程廣度（GaN、InP、GaAs）與 SiGe 高速類比設計，加上設計導入後的重新認證成本；美國自有晶圓廠在國防與本土供應具稀缺性。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：FY26 調整後營益率升 660 基點至 32%，第四季各項指引達標或超過。定價面穩定：第一季毛利率指引 62–63% 與管理層稱成本大致可轉嫁，但 TTM GAAP 毛利率 57.1% 仍低於 FY22 的 60.2%，且發生在短缺期。分析師在 2026-11-05 法說點名 Astera Labs 跨入 TIA 與驅動器，管理層也承認全整合 CMOS 不是公司的領域。","peer_na_reason":"事實表同業資料只有毛利率、營益率、FCF 利潤率與研發密度，沒有 ROIC，故改用利潤率比較。","threats":[{"level":"🔴","text":"矽整合、CPO 與 NPO：若全整合 CMOS 勝出，分離式 TIA、驅動器與光偵測器的市場會縮小；目前沒有出貨量受損的硬數據，大量部署預估 2027–2028。","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"]},{"level":"🟡","text":"既有對手與新進者搶 TIA 與驅動器份額，10-K 另提中國公司競爭加劇。","p":"40%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"客戶內製或轉單；採購單制下沒有違約成本，目前查無具體案例。","p":"25%","evidence_refs":["customer_second_source#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（暫判，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是光模組廠，決策者是超大規模業者的架構與採購團隊，付款來源是雲端資本支出。需求急迫，持久性未證：FY26 訂單出貨比 1.5，但 LightCounting 指需求與資本支出週期高度相關。國防端有美歐預算支撐，較持久。"},{"item":"決策層級","level":"🟡","text":"單一插槽一旦導入，重新認證成本高；但管理層預期超大規模業者會分給多家，跨世代的黏著度較弱。國防平台認證週期長，美國僅公司生產這類線性化器，黏著度明顯較高。"},{"item":"價值鏈分配","level":"🟡","text":"短缺期超額利潤主要落在雷射環節，Lumentum 稱出貨比需求低約 30%；SiGe 代工要求確定承諾，顯示上游議價權上升。各環節採購金額占比事實表未涵蓋。"},{"item":"社會容忍度","level":"🟢","text":"終端是資料中心、國防與衛星，不是民生必需品，沒有社會對漲價的上限；CHIPS 補助與出口管制屬政策依賴，已另列風險。"}],"roiic":"資料缺口：事實表無投入資本與全年營運資金變動。可見的是 FY26 調整後營業利益增加約 1.79 億美元（FY25 約 2.46 億，FY26 約 4.25 億，由 32% 營益率與年增 660 基點推得），同期資本支出 6,440 萬美元、IQE 投資 6,100 萬美元。增量報酬看起來很高，但主要來自稼動率與短缺期，不宜外推。","reinvest_rate":"資料缺口：FY26 資本支出 6,440 萬美元、第四季折舊 920 萬美元，FY27 資本支出升到 1.0–1.1 億美元；全年營運資金與收購淨額事實表未涵蓋，無法依公式計算。真正的再投資是研發，FY27 約 3 億美元。","endo_ceiling":null,"formula_note":"當期 ROIC 與內生成長上界都因投入資本缺資料而未計算；情境樹一律當作超出上界處理。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","MTSI":57.13,"SWKS":40.75,"QRVO":48.22,"ADI":65.8,"COHR":38.16,"unit":"%"},{"metric":"營業利益率","MTSI":18.97,"SWKS":8.12,"QRVO":15.38,"ADI":35.72,"COHR":14.11,"unit":"%"},{"metric":"FCF 利潤率","MTSI":9.44,"SWKS":9.28,"QRVO":17.82,"ADI":35.57,"COHR":-23.28,"unit":"%"},{"metric":"研發密度","MTSI":23.23,"SWKS":21.4,"QRVO":19.74,"ADI":14.24,"COHR":10.18,"unit":"%"}],"competitors":[{"name":"SWKS","gm":40.75,"om":8.12,"fcf_margin":9.28,"rd_intensity":21.4,"strategy_note":"手機射頻為主，毛利率 40.8%，與公司高階非手機定位重疊有限。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"QRVO","gm":48.22,"om":15.38,"fcf_margin":17.82,"rd_intensity":19.74,"strategy_note":"毛利率 48.2%，國防與基礎建設射頻直接競爭，獲利能力低於公司最新一季水準。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ADI","gm":65.8,"om":35.72,"fcf_margin":35.57,"rd_intensity":14.24,"strategy_note":"毛利率 65.8%、營益率 35.7%，規模與產品廣度最強，是公司中段 60% 毛利率目標的標竿。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"COHR","gm":38.16,"om":14.11,"fcf_margin":-23.28,"rd_intensity":10.18,"strategy_note":"毛利率 38.2%，光模組垂直整合廠，既是客戶也可能是競爭者；FCF 利潤率 −23.3% 反映重資本投入。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（1.6T、200G／lane、磷化銦產能），新品組合與稼動率推升毛利；近 12 個月無併購重大項目，也沒有回購。","runway_years":5,"runway_post_y5":"🟢","endo_ceiling_basis":"事實表無投入資本序列，無法以增量報酬乘再投資率算出上界，因此保守視為超出，Bear 機率取 30%。缺口歸因為營業利益率擴張，不靠併購或回購。","segments":[{"item":"資料中心","value":"FY26 約 5.0–5.1 億美元、年增 74%，占 38%；第四季 1.881 億美元；FY27 base case +80%，第一季指引季增約 15%"},{"item":"工業國防","value":"FY26 年增 27.8%，占 40%；第四季 1.646 億美元；FY27 目標 30% 以上"},{"item":"電信","value":"FY26 年增約 11%，占約 20%；第四季 7,210 萬美元；FY27 目標超過 3 億美元，上半年受 PON 與寬頻拖累"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY26 調整後 EPS +61% 對營收 +37%，差 24 個百分點，主要是營業槓桿。"},{"signal":"替代技術壓縮市場","lit":false,"note":"尚無出貨受損的硬數據，列為觀察。"},{"signal":"毛利率連兩季年減","lit":false,"note":"毛利率仍在上升。"},{"signal":"FCF 對淨利低於 0.75 連兩年","lit":false,"note":"FY25 GAAP 淨利為負，無法連續比較；第四季 FCF 對調整後淨利 0.85 倍。"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"第四季 5.6%，高於 5%，但逐年趨勢事實表未涵蓋。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"目前成長靠內部研發與產能，近 12 個月 8-K 沒有併購重大項目，也沒有回購與股息，無資本回報可展開。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"併購已實現報酬事實表未涵蓋；可見證據只有 FY24 GAAP 毛利率從 59.5% 降到 54.0%，以及管理層對 Linearizer 案的定性說法。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"沒有回購，2026-11-05 法說執行長稱目前沒有回購或股息計畫。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"第四季 SBC 2,390 萬美元年化約 9,560 萬，占市值 161 億美元約 0.6%。限制：由淨利與 EPS 反推股數，FY23 約 7,150 萬到現在 7,637 萬，年增約 2.2%，其中含可轉債交換，無法單獨拆出 SBC。","grade":"過"}]},"valuation":{"basis":"前瞻本益比與 PEG，以 FY1 為口徑，輔以 EV/S 對照","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻倍數，無法做倍數對照。"},"fwd_pe":24.7,"peg":0.81,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 24.7 倍，修正 EPS 後約 22 倍，PEG 0.81–1.18，遠低於前份的 56 倍；但分母是否為週期高點正是爭點，因此結論是合理，不到便宜。反例：若 FY28 共識 EPS 跌破 9 美元，現價等於 23 倍以上而成長消失，應改判偏貴。","upside_short_pct":20,"upside_mid_pct":46},"trap_analysis":{"verdict":"🟡","label":"盈餘高點風險，非傳統價值陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"訂單是採購單、無最低採購量；FY26 訂單出貨比 1.5，第四季當季接單當季出貨僅 7%，交期拉長；LightCounting 指 2027–2031 成長趨緩且與雲端資本支出高度相關。","assumption":"FY28 資料中心營收不衰退。","consequence":"若重複下單回吐，FY29 EPS 谷底約 6.8 美元，五年終值約 127 美元，較現價跌約 40%。","ruling":"採納，作為 Bear 主軸，機率 30%，與唯一致命點是同一件事。2026-11-05 法說對 2028 的回覆只有長期觀點，沒有數字，證據時間窗蓋不到風險窗。","watch":"訂單出貨比、資料中心季增率、雲端資本支出指引。","evidence_refs":["supply_demand_durability#1","customer_concentration_credit#2","customer_second_source#0"]},{"view":"論點失敗","evidence":"10-K 自述未來會有採低成本矽製程與高整合度的競爭；管理層在 2026-11-05 法說承認全整合 CMOS 不是公司的領域；評論文章指 CPO 內製可能縮小分離式元件市場。","assumption":"NPO 世代仍需要多功能或單功能的高效能 SiGe 元件。","consequence":"資料中心第二條曲線落空，FY31 EPS 落在 Base 以下，終端倍數同步下修。","ruling":"部分採納。目前沒有出貨受損的硬數據，且 448G 驅動器已針對矽光子與 NPO 設計，但 NPO 贏單未揭露，機率取 35%。","watch":"NPO 首筆量產營收時點、超大規模業者的 NPO 方案選擇。","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"]},{"view":"論點失敗","evidence":"FY25 中國占營收 28.4%，多數產品受出口管制，10-K 稱已造成部分出貨困難；2026-08-06 法說回應中國模組廠禁令傳聞時，執行長預期客戶組合移轉而非流失。","assumption":"中國模組廠的份額可由其他地區補回。","consequence":"若禁令實施且補位落後，FY27–FY28 資料中心至少延遲數季。","ruling":"部分採納。管理層的移轉說法未經驗證，列為短期風險，以下季指引作為吸收失敗的判準。","watch":"出口管制公告、次季營收指引、10-K 中國營收占比。","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1"]},{"view":"論點成功但股東經濟變差","evidence":"執行長在 2026-11-05 法說稱 2030 年想成為 50 億美元公司，需要更多技術、人員與新市場，暫無回購與股息；FY27 資本支出升到 1.0–1.1 億美元；SiGe 代工要求確定承諾，公司表示願意簽。","assumption":"營收成長能以現有紀律換成每股價值。","consequence":"若靠大型併購達標，或簽下確定承諾後遇到需求下滑，營收達標但 FCF 轉換率與資本報酬下降。","ruling":"部分採納。目前併購仍是小型補強，但 FY24 GAAP 毛利率曾從 59.5% 降到 54.0%，大型案的風險要預先設門檻。","watch":"單筆併購占市值比重、代工承諾金額、GAAP 與調整後淨利差距。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"view":"價格已反映太多","evidence":"TTM 本益比 48.95 倍，P/S 12.14 倍與 EV/S 11.85 倍都是三個年度端點內最高；FY1 倍數建立在可能是週期高點的盈餘上。","assumption":"FY27 不是盈餘高點。","consequence":"若 FY27–FY28 就是高點，現在的 22–25 倍其實偏貴，本益比最低的時候往往不是買點。","ruling":"反駁一半。Base 情境本益比由 24.7 倍降到 22 倍，年化約 10% 全靠盈餘，不依賴倍數擴張；但股價已跌 45% 本身不是安全邊際。","watch":"FY28 共識 EPS 是否跌破 9 美元。","evidence_refs":[]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 385.98 → 本次 210.98（-45.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=385.98","side_b":"本次 price_at_dd=210.98","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 385.98 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 385.98 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 385.98 美元：Bull 價 607.5、Bear 價 127.5，五年期望值 −14.4%，基準年化 −2.4%，不對稱比 0.57","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.57。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 385.98 美元：五年期望值 −14.4%，基準年化 −2.4%，不對稱比 0.57","side_b":"本次情境、股價 210.98 美元：五年期望值 +56.5%，基準年化 10.1%，不對稱比 3.17","ruling":"再換股價、情境不動：起點價下跌 45.3%，五年期望值多 71.0 個百分點，基準年化多 12.5 個百分點，不對稱比由 0.57 升到 3.17。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 385.98 美元，FY26／FY27 前瞻本益比 76／56 倍，結論偏貴。","side_b":"本次股價 210.98 美元，FY1 前瞻本益比 24.7 倍，結論合理。","ruling":"可調和。股價跌 45% 是主因，FY27 盈餘上修是次因；分母是否為週期高點仍有爭議，所以只升到合理。","evidence_level":"高","settle_metric":"財報後第一份完整共識的 FY27 與 FY28 EPS","if_then":["若 FY28 共識 EPS 跌破 9 美元，停止加碼","若股價漲回 280 美元以上而訂單證據未到，不追"],"evidence_refs":[]},{"axis":"整體評等與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評等 B，陷阱風險低。","side_b":"本次評等 B，陷阱風險中等。","ruling":"FY26 EPS 成長 61% 遠高於營收 37%，衰退信號亮一顆，陷阱風險由低升到中等。股價大跌沒有換來更高評等，因為 FY28 能見度仍低，Base 年化約 10% 只算中等。","evidence_level":"中","settle_metric":"FY27 第三季財報的訂單出貨比","if_then":["若連續兩季訂單出貨比不低於 1.2，加碼至 6%","若連續兩季低於 1.0，減碼一半"],"evidence_refs":[]},{"axis":"前份空白欄位首次填入","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位為空白。","side_b":"本次護城河方向為 →，成長跑道寬，屬品質複利成長、中循環，機率 20／50／30，回撤範圍 −40% 到 −60%。","ruling":"沒有舊值可比，屬首次填入，不代表判斷改變。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"清倉與減碼門檻首次設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（欄位空白）。","side_b":"清倉：資料中心營收連續兩季季減。減碼：訂單出貨比連續兩季低於 1.0，或調整後毛利率低於 60%。","ruling":"新設門檻，因為前份的風險條件只寫到削弱與反轉，沒有對應動作。","evidence_level":"中","settle_metric":"每季資料中心營收與訂單出貨比","if_then":["資料中心營收連續兩季季減，清倉","訂單出貨比連續兩季低於 1.0，減碼一半"],"evidence_refs":[]},{"axis":"重新進場門檻首次設定","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設門檻欄，只在結論寫等回測 290–330 美元或布林中軌 257 美元。","side_b":"現價 230 美元以下建第一筆；FY27 第一季資料中心季增 ≥10% 且訂單出貨比 ≥1.0 才加碼","ruling":"舊等待價位已被穿越，不再適用。新條件把價格與訂單證據分開：價格只決定第一筆，加碼要看訂單。","evidence_level":"中","settle_metric":"FY27 第一季財報","if_then":["達標則加碼至 4%","股價跌到 170–195 美元而基本面未破，分批反買"],"evidence_refs":[]},{"axis":"Single Thing 首次設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未列唯一致命點（欄位空白）。","side_b":"FY28 結束前，資料中心營收出現連續兩季季減。","ruling":"新設。這是情境樹中最大的單一敏感項：Base 與 Bear 的 FY29 EPS 相差 46%，本益比再從 22 倍壓到 15 倍。","evidence_level":"中","settle_metric":"每季資料中心營收","if_then":["事件發生，清倉"],"evidence_refs":[]},{"axis":"共識上修幅度","cause":"方法變動","prior_field":null,"side_a":"事實表顯示 FY1 共識三個月上修 55%。","side_b":"舊快照 FY2 8.54、FY3 10.11 美元，與新快照 FY1、FY2 完全相同，這是財年滾動；FY27 共識在兩份快照之間沒有變動。","ruling":"採後者。55% 不是真實上修，不作為動能證據。8.54 美元也低於第一季指引年化 9.0 美元，說明快照尚未反映最新財報。","evidence_level":"高","settle_metric":"財報後第一份完整共識的 FY27 EPS，接近 9.5 美元才算真上修","if_then":["若完整共識 FY27 EPS 仍低於 9 美元，重新檢視營益率假設，停止加碼"],"evidence_refs":[]},{"axis":"FCF 利潤率口徑","cause":"方法變動","prior_field":null,"side_a":"同業表 TTM FCF 利潤率 9.44%。","side_b":"法說 FY26 營運現金流 3.57 億美元、資本支出 6,440 萬美元，FCF 約 2.93 億美元，利潤率約 22%。","ruling":"採法說口徑。同業表差異原因無法在本包查證，所以同業 FCF 比較不作為論據。","evidence_level":"中","settle_metric":"FY26 10-K 現金流量表","if_then":[],"evidence_refs":[]},{"axis":"短缺持續時間與 2028 能見度","cause":"新證據","prior_field":null,"side_a":"LightCounting（2026 年 4 月）：短缺預計 2026 年底消退，2027–2031 成長趨緩。","side_b":"Lumentum（2026 年 8 月）稱 EML 產能訂到 2027；公司 2026-11-05 法說稱積壓訂單創新高、交期拉長。","ruling":"短缺時間點採後者，資料較新。2028 需求不可裁決，要到 FY27 第三季財報（約 2027-08）才有第一批訂單證據；在此之前不得稱風險已解除，所以倉位上限先壓在 4%。","evidence_level":"中","settle_metric":"FY27 第三季訂單出貨比與 FY28 排程訂單","if_then":["訂單出貨比連續兩季不低於 1.2，加碼至 6%","訂單出貨比連續兩季低於 1.0，減碼一半"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"管理層口徑對帳","cause":"新證據","prior_field":null,"side_a":"2026-08-06 法說：執行長稱 FY27 資本支出約 6,000 萬美元、資料中心 base case +50%，CW 雷射最早 2027 年底量產，同場問答又說 2028。","side_b":"2026-11-05 法說：財務長稱 FY27 資本支出 1.0–1.1 億美元；執行長稱資料中心 base case +80%，CW 雷射目標 2028，尚未宣告成功。","ruling":"資本支出上修與訂單同向，可以解釋，但三個月內上修七成，顯示能見度不如口徑穩定。CW 雷射時程偏向 2028，FY28 前不計入 Base 的放量。","evidence_level":"高","settle_metric":"Phase 2 擴產是否於 2027 年中啟動","if_then":["Phase 2 延到 2028，H3 視為削弱，停止加碼"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":"新證據","prior_field":null,"side_a":"賣方論證：股價低於 52 週均線 262.51 美元，26 週跌 41%，市場在定價 2028 消化；FY27 可能就是週期高點，高點時本益比最低，低本益比不是買點。","side_b":"不賣論證：第一季指引營益率 40%，FY26 工業國防占 40%，FY27 目標年增 30% 以上；淨現金 4.5 億美元。","ruling":"不賣，但只分批小量建立。Base 年化約 10%、Bear 機率 30%，賠率不足以重押。","evidence_level":"中","settle_metric":"FY27 第三季訂單出貨比","if_then":["若資料中心連續兩季季減，清倉","若股價先跌而基本面無損，分批反買"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭：10-K 列 11 家競爭者並提到中國公司競爭加劇，分析師點名 Astera Labs 跨入 TIA 與驅動器。其他結構：CPO 與 NPO 架構變動，出口管制持續。","side_b":"結構轉好：NXP 退出 5G 射頻功率 GaN，部分雷射廠退出 25G DFB，公司是唯一美國本土 5G 功率放大器供應商。","ruling":"雙向拉鋸。射頻與國防的供給面在改善，資料中心的競爭與架構風險在升高。","evidence_level":"中","settle_metric":"調整後毛利率與 NPO 量產案","if_then":["毛利率低於 60%，減碼至 1%"],"evidence_refs":["competitive_share_entrants#0","geo_supply_chain#2"]},{"axis":"客戶集中度口徑","cause":"新證據","prior_field":null,"side_a":"10-K：前十大客戶占比由 FY23 的 48% 升到 FY25 的 57%。","side_b":"2026-08-06 法說，執行長：前十大終端客戶低於 40%，年收入超過 1,000 萬美元的客戶由約 8 家增到逾 20 家。","ruling":"可調和。10-K 計入經銷商，經銷占比升到 32.3%；終端口徑只有管理層口述，無法驗證，風險仍保留。","evidence_level":"中","settle_metric":"FY26 10-K 客戶集中度揭露","if_then":["前十大客戶占比超過 60%，停止加碼"],"evidence_refs":["customer_concentration_credit#1"]}],"triggers":[{"n":1,"text":"FY27 第一季資料中心季增未達 10%","type":"假設驗證","maps_to":"H1","metric":"資料中心營收季增率","threshold":"低於 10%（指引約 15%）","action":"停止加碼","source_freq":"季度法說","date":"2027-02"},{"n":2,"text":"訂單出貨比連續兩季低於 1.0","type":"減碼","maps_to":"R1","metric":"公司整體訂單出貨比","threshold":"連續 2 季低於 1.0","action":"減碼一半","source_freq":"季度法說","date":"2027-05","evidence_refs":["supply_demand_durability#1","customer_concentration_credit#2","customer_second_source#0"]},{"n":3,"text":"資料中心營收連續兩季季減","type":"Single Thing","maps_to":"Single Thing","metric":"資料中心營收季增率","threshold":"連續 2 季為負","action":"清倉","source_freq":"季度法說","date":null},{"n":4,"text":"現價 230 美元以下建第一筆","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"230 美元以下，約 Base FY27 EPS 的 24.5 倍","action":"建第一筆 2%","source_freq":"每日收盤","date":null},{"n":5,"text":"第一季達標，或股價跌到 104 週均線附近而基本面未破","type":"加碼","maps_to":"H1","metric":"資料中心季增率、訂單出貨比、股價","threshold":"季增 ≥10% 且訂單出貨比 ≥1.0；或股價 170–195 美元且 H1 未破","action":"加碼至 4%","source_freq":"季度法說與每日收盤","date":"2027-02"},{"n":6,"text":"毛利率回落且競爭者量產","type":"減碼","maps_to":"H2","metric":"調整後毛利率","threshold":"低於 60%，或連續 2 季環比下滑 1 個百分點以上","action":"減碼至 1%","source_freq":"季度 8-K","date":null,"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#1"]},{"n":7,"text":"中國出口限制升級","type":"風險","maps_to":"R3","metric":"中國模組廠禁令與下季營收指引","threshold":"禁令實施，且下季指引低於前季營收 5% 以上","action":"減碼一半","source_freq":"事件與季度法說","date":null,"evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1"]},{"n":8,"text":"代工或關鍵材料造成出貨受限","type":"風險","maps_to":"R4","metric":"營收對指引下緣、揭露的代工承諾金額","threshold":"營收低於指引下緣且歸因供應；或代工承諾超過年營收 20%","action":"停止加碼","source_freq":"季度法說與 10-Q","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"n":9,"text":"NPO 或 CPO 改採全整合 CMOS 方案","type":"風險","maps_to":"R2","metric":"超大規模業者方案選擇、公司 NPO 營收","threshold":"主要業者量產採全整合方案，且公司 FY28 NPO 無營收","action":"減碼至 1%","source_freq":"產業新聞與季度法說","date":"2028-09","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1"]},{"n":10,"text":"FY27 第三季財報提供第一批 FY28 訂單證據，到期複審","type":"複審日期","maps_to":"H1","metric":"訂單出貨比與 FY28 排程訂單","threshold":"到期即複審","action":"訂單出貨比 ≥1.2 加碼至 6%；低於 1.0 減碼一半","source_freq":"季度法說","date":"2027-08"}],"kill_metrics":[{"metric":"資料中心營收季增率","bear_threshold":"連續兩季季減（清倉）","window":"FY27–FY28 每季","source":"MACOM 季度法說與 8-K","last_status":"ok"},{"metric":"公司整體訂單出貨比","bear_threshold":"連續兩季低於 1.0（減碼一半）","window":"FY27–FY28 每季","source":"MACOM 季度法說","last_status":"ok"},{"metric":"調整後毛利率","bear_threshold":"低於 60%，或連續兩季環比下滑 1 個百分點以上（減碼）","window":"FY27–FY28 每季","source":"MACOM 季度 8-K","last_status":"ok"},{"metric":"FY28 共識 EPS","bear_threshold":"低於 9 美元（停止加碼）","window":"至 FY28 財報","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"NPO 與 CW 雷射量產營收","bear_threshold":"FY28 結束前兩者皆無量產營收（減碼）","window":"至 2028-09","source":"MACOM 季度法說","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把全公司當成 AI 資本支出的單一賭注，26 週跌 41%；但 FY26 工業國防占 40%、FY27 目標年增 30% 以上，且 FY27 共識 EPS 8.54 美元低於第一季指引年化 9.0 美元。市場對 2028 的疑慮有道理，錯在把折扣也套到與 AI 較無關的業務。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-41.37, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"現價 230 美元以下建第一筆；FY27 第一季資料中心季增 ≥10% 且訂單出貨比 ≥1.0 才加碼","exec_line":"分三筆：230 美元以下先建 2%；FY27 第一季財報達標加到 4%；FY27 第三季財報確認 FY28 訂單延伸後才到 6%。股價先漲到 280 美元以上而證據未到，不追；股價下跌而基本面無損，分批反買。"},"reasoning":{"industry":"FY26 營收 13.3 億美元、年增 37%，調整後 EPS 5.60 美元、年增 61%。第四季營收 4.248 億美元，調整後毛利率 61.3%、營益率 38.2%，GAAP 營益率 31.6%。FY27 第一季指引營收 4.5–4.6 億美元、調整後毛利率 62–63%、EPS 2.21–2.29 美元。收錢方式是賣標準與客製晶片、模組，外加晶圓代工服務，法國廠約一半是代工。訂單以採購單為主、沒有最低採購量，靠設計導入與長交期維持能見度，第四季當季接單當季出貨僅占營收 7%。經銷商占 FY25 營收 32.3%。單點依賴有兩處：特定製程晶圓通常只有一家代工來源，資料中心的 SiGe 大多委外；需求面則繫於超大規模業者的資本支出。反例：管理層稱三個市場彼此不相關，但 FY26 三個市場同步成長，還沒有下行期可以驗證這個說法。","moat":"機制是化合物半導體製程廣度加上設計導入後的重新認證成本。TTM GAAP 毛利率 57.1%，高於 SWKS 40.8%、QRVO 48.2%、COHR 38.2%，低於 ADI 65.8%；研發密度 23.2% 為同業最高，代表優勢要靠持續投入維持。第四季財報對 2026-08-06 指引全數達標或超過：營收 4.248 億美元落在 4.15–4.25 億上緣，EPS 2.09 美元高於 1.97–2.03，毛利率 61.3% 高於 60–61%。定價力打 7 分的原因是 GAAP 毛利率仍低於 FY22 的 60.2%，尚未證明結構性突破，且現在是短缺期，轉嫁成本比平時容易。對最強同業的 ROIC 差距事實表未涵蓋，改用毛利率比較。反例：若 FY27 毛利率真的走到中段 60% 並維持到短缺結束，應上修為擴大。","growth":"成長主要來自量，併購與回購貢獻趨近零。管理層 FY27 base case 為資料中心 +80%、工業國防 30% 以上、電信低雙位數，加總約 19 億美元，與共識 19.4 億一致。第一季資料中心指引約 2.16 億美元，之後每季只要季增約 4% 就能達到 +80%，FY27 風險不大。三年共識 EPS CAGR 30.6%（FY26A 5.60 到 FY29E 12.48），高於營收成長的部分來自營業槓桿，稅率由 3% 升到 6% 會抵銷一部分。若 SAM 年增 10–20%、公司維持 37% 年增，約 4–6 年滲透率到 30%。反例：SAM 是管理層定義，且已上修過；若整合方案勝出，可服務市場反而縮小。","governance":"FY26 營運現金流 3.57 億美元、資本支出 6,440 萬美元，FCF 約 2.93 億美元，利潤率約 22%。第四季 FCF 1.38 億美元，對調整後淨利 1.633 億美元為 0.85 倍。同業表的 TTM FCF 利潤率 9.44% 與法說數字對不上，這裡採法說。第四季 SBC 2,390 萬美元，占營收 5.6%，年化約占市值 0.6%。淨現金 4.517 億美元（現金及短投 7.924 億扣可轉債帳面 3.407 億，2029-12 到期），含租賃口徑為 3.855 億。管理層明言目前沒有回購或股息計畫，現金留給併購與景氣下行。現金去向四分的全年數字事實表未涵蓋。","valuation":"現價 210.98 美元。FY1 前瞻本益比 24.7 倍，但 EPS 8.54 美元偏舊：共識營收 19.4 億美元配上第一季指引的 40% 營益率、6% 稅率與 7,900 萬股，約 9.5 美元，換算約 22 倍。TTM GAAP 本益比 48.95 倍，FY1 EV/S 8.11 倍。PEG 依 FY26A 到 FY29E 的 30.6% CAGR 約 0.81；扣掉 FY27 的跳升，用 FY27 到 FY29 的 20.9% 則約 1.18，後者較能代表現價買到的成長。上檔試算：12 個月以 FY28 Base EPS 11.0 美元乘 23 倍約 253 美元（+20%）；3 年以 FY30 Base EPS 14.0 美元乘 22 倍約 308 美元（+46%）。成長熄火測試：第四年起 EPS 年增降到 15%、10%、5%，分別乘 20、15、11 倍，FY31 價格約 331、227、152 美元，前兩者高於現價。賣方平均目標 377.56 美元（2026-08-01）高於現價 79%，但屬舊倍數環境，不單獨採用。五年分位在事實表只有 2–3 個年度端點，不具分位意義，留空；同業前瞻倍數事實表未涵蓋。","premortem":"第一，股價 26 週跌 41%、RSI 38，市場已在定價 2028 消化，而我的 FY27 判斷可能正確卻無關緊要。第二，共識 FY1 三個月上修 55% 是財年滾動造成的假象，舊快照的 FY2、FY3 與新快照的 FY1、FY2 完全相同，不能當作上修動能。第三，NPO 贏單時程在 2026-11-05 法說拒答，光偵測器營收與分部毛利也不拆，第二條曲線的證據主要來自管理層口述。第四，2026-08-06 法說稱 NPO 部分專案不會量產，CW 雷射至今未宣告成功。法律面 10-K 無重大未決訴訟，近 12 個月 8-K 沒有重大事項。歷史最大回撤與空方最強數字事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺雲端光互連、國防射頻與衛星通訊客戶的錢，錢卡在高速類比與化合物半導體這一節；第四季資料中心占營收 44%、工業國防 39%、電信 17%。","moat":"護城河方向 →：執行力在擴大，定價力只算穩定，矽整合與新進者的威脅抵銷了製程廣度的優勢，等級 B。","growth":"成長跑道寬：FY27 營收約 19.4 億美元只占管理層估的 150 億 SAM 約 13%，NPO 與 CW 雷射是下一條曲線，但都要到 2028 才有營收。","capital":"現金累積快、紀律尚可，沒有回購與股息；下一步的考驗是 50 億美元目標要靠多少併購。","valuation":"現價要賺 10% 年化，需要 FY31 EPS 約 15.5 美元且本益比維持 22 倍；我相信 FY27，FY28 之後保留。","how_wrong":"最可能看錯在 FY28：訂單沒有約束力，供給一鬆就可能出現重複下單回吐，這不是傳統價值陷阱，而是盈餘高點風險。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把全公司當成 AI 資本支出的單一賭注，26 週跌 41%；但 FY26 工業國防占 40%、FY27 目標年增 30% 以上，且 FY27 共識 EPS 8.54 美元低於第一季指引年化 9.0 美元。市場對 2028 的疑慮有道理，錯在把折扣也套到與 AI 較無關的業務。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":210.98,"week26_return_pct":-41.37,"consensus_rev_3m_pct":54.99,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY1 共識 8.54 美元偏舊，低於第一季指引年化的 9.0 美元；更關鍵的是 FY27–FY28 EPS 是否為週期高點，正是市場爭點，所以 24.7 倍不能當作便宜的證據。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第一季財報","impact":"高","watch":"資料中心季增約 15%、毛利率 62–63%、訂單出貨比"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"CHIPS 最終協議可能簽署","impact":"中","watch":"2026-08-06 法說提到有無法接受的條款，留意最終條件與補助金額"},{"date":"2027-06","date_precision":"month","type":"capacity","event":"Lowell 第二階段擴產預計啟動，視 CW 雷射表現而定","impact":"中","watch":"是否如期啟動，以及 CW 雷射可靠度結果"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27 第三季財報，FY28 訂單能見度的第一批證據","impact":"高","watch":"訂單出貨比、FY28 排程訂單、管理層對 2028 的量化說法"},{"date":"2028-Q1","date_precision":"quarter","type":"product","event":"NPO 與 CW 雷射預期開始貢獻營收","impact":"高","watch":"首筆量產營收與客戶數"}],"_projected_from":"v19"}
```
