你是 stock-analyst v20 的**散文層（prose）agent**，標的 3189.TW（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：3189.TW　日期：2026-11-08　archetype：None　前份裁決：2026-10-12　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1480B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（428B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（873B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（793B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（975B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（530B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（777B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2349B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3196B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2578B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1480           3864-5520      5 條（2–6 內）  
s3                  8000         428           5300-7572      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2641          8651-12359      5 條（2–6 內）  
s6                 11000         530          7329-10470      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         777           1906-2723      5 條（2–6 內）  
s10                 5000        2349           1856-2651      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2578           2000-2422      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3860B；至少需散文≈41.14KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−88%
−80
−80%
−74%
−71%
−65
−55
−55%
−53%
−40.2%
−39.7%
−36.8%
−36.7%
−11.4%
−10.8%
−9.2
−5%
−4.8%
−2.2%
−2%
0
0.10
0.11
0.13
0.16%
0.226
0.24
0.27%
0.3
0.31
0.5
0.6
0.7
1
1.0
1.07
1.1
1.2%
1.3
1.5%
1.89%
1.9
2
2.0
2.3
2.8
3%
3
03
3.15
3.2
3.37
3.43%
3.74
3.95%
4%
4
4.55
4.75
5
5%
6
7
7.12
7.22
08
8
8%
8.5
09
9
9.5
10
10%
10.12%
10.72%
11%
11
11.2
12
12.27%
12.7%
12.88
13.30%
13.4%
13.5%
14
14%
14.5
14.57
15%
15.9
16
16%
16.0
16.04%
16.4%
17.1
17.8%
18%
18
18.53%
19.51%
20%
20
20.26
20.3
20.8%
21
21%
21.1
21.13%
21.16%
22
23.2
24%
24
25%
25.6
26
26.09%
26.1%
27%
27
28
28.11
28.17
28.39%
29%
29
30%
30
31
32.6
33
33%
33.12
33.41%
34%
34.9
35
35%
35.4
36.7%
36.8%
37%
37
37.02%
37.7
38
40%
40
42
45
46%
46.76
46.76%
48%
49
50%
51%
51
52%
52
52.1
54%
60
62
64
70
70%
80%
80
84
85%
86%
90%
95%
96
100%
100
103.82
104
124.96
140
150%
162
174.5
176
180
196
198
213%
213
232
235
250
317
448
450
473
480
488
490
526.9
536
600
609
620
640
670
671.0
671
684
695
712
800
837
868
880
892
900
1060.0
2023
2025
2026
2027
2028
2029
2030
2031
3037
3189
4062
8046
20261108
1,060
1,200
1,250
1,536
1,550
1,600
4,000
5,000
7,200
8,000
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
{"meta":{"ticker":"3189.TW","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"景碩科技"},"oneliner":"景碩一個月跌了三成七，FY2027 本益比剩 20 倍，但分母是上一輪高點 2.3 倍的獲利，第三季數字也還沒進證據包。按情境算，現價五年機率加權報酬約 −5%，480 元以下才值得重做研究。","thesis":{"H":[{"id":"H1","text":"2027 年短缺仍在，ABF 與 BT 報價加上稼動率，能把合併毛利率推到上一輪高點的九成。","2y":"FY2027 合併毛利率 ≥33%，歸屬 EPS ≥29 元。","5y":null,"10y":null,"threshold":"FY2027 合併毛利率 ≥33%；FY2027 EPS ≥29 元","source":"MOPS 季報、法說會；以 FY2022 毛利率 37.02% 為對照","drift_rule":"以近四季比對，連兩季偏離 ≥5% 視為削弱，連三季偏離 ≥10% 視為反轉"},{"id":"H2","text":"公司把 CPU 載板的認證優勢擴到 AI GPU 與 ASIC，新增產能在客戶出資與長約下被填滿。","2y":null,"5y":"2029 年底 ABF 月產能至少 7,200 萬顆，稼動率 ≥80%。","10y":null,"threshold":"2027 年 AI 相關營收占比 ≥15%；2029 年底 ABF 月產能 ≥7,200 萬顆且稼動率 ≥80%","source":"法說會、年報、法人份額調查","drift_rule":"連四季落後門檻 ≥5% 視為削弱，連六季落後 ≥10% 視為反轉"},{"id":"H3","text":"下一輪下行時，谷底獲利要明顯高於上一輪，才能證明這不只是一段短缺行情。","2y":null,"5y":"下一個谷底年度營業利益率 ≥8%，全循環自由現金流合計為正。","10y":null,"threshold":"谷底年度營業利益率 ≥8%（FY2023 為 3.95%，FY2024 為 3.43%）","source":"年度財報","drift_rule":"連四季偏離 ≥5% 視為削弱，連六季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"T-glass 由 Nittobo 獨供，擴產要到 2027 年第三季，限料壓住每月 10%～15% 營收。","h_ref":"H1","clock":"⚡","threshold":"單季營收季增率連兩季低於 5%","evidence_refs":["supply_demand_durability#2"]},{"id":"R2","text":"全產業擴產在 2027–29 年開出，新廠折舊落在回落的報價上，重演 2023 年下行。","h_ref":"H1","clock":"🔥","threshold":"ABF 稼動率低於 85% 或季均價季減","evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R3","text":"客戶集中度升高，欣興與 Ibiden 在高階 AI 載板領先，份額目標可能落空。","h_ref":"H2","clock":"🔥","threshold":"最大客戶占比超過 30%，或 2027 年底 AI GPU 份額低於 10%","evidence_refs":["customer_concentration_credit#0","competitive_share_entrants#2"]},{"id":"R4","text":"味之素等上游獨供廠商分走短缺的利潤，景碩漲價留不住。","h_ref":"H1","clock":"🔥","threshold":"ABF 報價上漲期間，合併毛利率連兩季季減","evidence_refs":["geo_supply_chain#1"]},{"id":"R5","text":"玻璃核心基板導入後，核心層價值轉移，景碩沒有可見的對應方案。","h_ref":"H3","clock":"🐢","threshold":"前三大 AI 客戶有一家宣布量產，且公司仍無相應方案","evidence_refs":["substitute_technology#1"]}],"single_thing":{"description":"2028 年底前，ABF 載板平均售價出現第一次季減。","why_fatal":"這是獲利最大的單一敏感度。FY2027 共識營收 837 億元，均價少 10% 相當於稅前少約 84 億元，每股約 15.9 元，占 33.12 元的 48%，而成本不會同步下降。這是以全部合併營收粗算，隱形眼鏡不隨載板報價變動，實際影響略低。","if_happens":"景氣轉折獲得確認，共識 EPS 開始下修，本益比同步壓縮，走向 Bear 路徑，FY2030E EPS 可能回到個位數。","how_monitor":"每季法說的報價說明、法人報價調查、合併毛利率季變化，以及欣興與 Ibiden 對稼動率的說法。","probability":"約 35%（未來 24 個月左右）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":20.26,"peg_fy2":0.13,"stress":{"pass":1,"total":3},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-11-08）"},"eps_meta":{"base_eps_path":{"FY2025A":3.37,"FY2026E":12.88,"FY2027E":33.12,"FY2028E":null},"fy_end_month":12,"eps_basis":"歸屬母公司稀釋 EPS；FY2026E、FY2027E 為 yfinance 共識平均，FY2028E 事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"FY2023 營收跌 36.8%，EPS 由 FY2022 的 14.57 元降到 FY2024 的 0.11 元；FY2022 至 FY2024 自由現金流連三年為負，資本支出呈波段式擴張。"},"industry":{"clock_phase":"III","sd_verdict_source":"供需判斷：短缺至少延續到 2027 年，屬週期性，2028 年後反轉的風險隨擴產升高。2028 年缺口的各家估計從 16% 到 51%，差距太大，不能當結構性持久的證據；這些估計也只到 2028 年，沒有涵蓋 2031 年的情境終點。來源多為媒體與部落格二手轉述。","bargaining":{"up":"上游弱勢：味之素 ABF 膜市占九成以上，T-glass 由 Nittobo 獨供，擴產要到 2027 年第三季。","down":"短缺期暫時占優：客戶出資設備、同意產能相關付款。2025 年前三大客戶合計約 34%，最大客戶占比由 10.72% 升到 19.51%。","geo":"台灣、蘇州、美國設廠。美國 232 條款是否涵蓋載板未確認，事實表未涵蓋公司的關稅影響。"},"profit_pool_dir":"事實表未涵蓋利潤池歷史，無法判斷方向。","tam_table":{"expanded":false,"reason":"事實表只有供需缺口百分比，沒有 ABF 市場規模、滲透率與五年前的利潤池，無法組成對照；份額也多是法人轉述或公司目標。"}},"moat":{"mechanism":"高層數 ABF 的製程良率加上客戶認證；認證通過後份額移動很快，目前的定價能力主要來自全產業短缺。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力改善：第二季毛利率由 21.16% 升到 26.09%，CPU 供貨率據法人升至 50%。定價能力沒有擴大的證據，公司自己把毛利改善歸因於稼動率。前次判斷以來沒有新的份額資料，第三季也未納入，方向維持。","threats":[{"level":"🟡","text":"欣興與 Ibiden 在高階 AI 載板份額領先，景碩要從後段搶份額，屬點對點競爭。","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🔴","text":"玻璃核心基板最快 2027 年底導入，最晚說法 2030 年。Intel 的設計仍保留 ABF 增層，受衝擊的是核心層；事實表沒有景碩的玻璃基板計畫。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"新產能 2027 年起陸續開出，主要廠商資本支出比上一輪高 51%，短缺結束時競爭會轉為價格戰。","p":"35%","evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#2"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟡","text":"AI 加速器與伺服器 CPU 必須用高層數 ABF，延後購買的代價高。但公司口徑 AI 相關營收 2026 年只占約 10%，2027 年 15%～20%，手機、PC 與消費性需求仍弱，其餘八成營收的需求基礎沒有同樣強。"},{"item":"決策層級","level":"🟡","text":"客戶換載板供應商要重新認證。法人稱美系 AI 客戶 CPU 供貨率由 10% 升到 50%，說明認證通過後份額移動很快，份額能移進來也能移出去。認證週期與合約年限事實表未涵蓋。"},{"item":"價值鏈分配","level":"🔴","text":"上游味之素 ABF 膜市占九成以上，Nittobo 獨供 T-glass，下游是少數 AI 大廠並出資鎖設備。景碩夾在中間，公司也把第二季毛利改善歸因於稼動率而非漲價，短缺的好處能留下多少還沒有證據。"},{"item":"社會容忍度","level":"🟢","text":"載板是企業間零組件，沒有消費者漲價壓力或民生監管限制。近 12 個月公平會處分為 0 筆，232 條款是否涵蓋載板則未確認。"}],"roiic":"事實表未涵蓋投入資本，算不出數值。方向上，營業利益由 FY2022 約 96 億元降到 FY2025 約 27 億元，四年自由現金流合計 −65 億元，上一輪投入尚未換回更高獲利。","reinvest_rate":"事實表未涵蓋折舊與營運資金變動，算不出。2026 年資本支出有 80 億元與 140 億元兩種說法，FY2025 歸屬淨利只有 16 億元，再投資需求遠超過現有獲利。","endo_ceiling":null,"formula_note":"當期 ROIC 與內生成長上界都需要投入資本、折舊與營運資金，事實表未涵蓋，不以推估補值。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","3189.TW":23.26,"3037.TW":22.68,"8046.TW":16.04,"4062.T":33.41,"unit":"%"},{"metric":"營業利益率","3189.TW":10.12,"3037.TW":13.3,"8046.TW":12.27,"4062.T":18.53,"unit":"%"},{"metric":"FCF 利潤率","3189.TW":7.37,"3037.TW":1.89,"8046.TW":7.71,"4062.T":34.6,"unit":"%"},{"metric":"研發密度","3189.TW":5.59,"3037.TW":3.85,"8046.TW":null,"4062.T":null,"unit":"%"}],"competitors":[{"name":"3037.TW","gm":22.68,"om":13.3,"fcf_margin":1.89,"rd_intensity":3.85,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"8046.TW","gm":16.04,"om":12.27,"fcf_margin":7.71,"rd_intensity":null,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"4062.T","gm":33.41,"om":18.53,"fcf_margin":34.6,"rd_intensity":null,"period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"FY2027 以價格與稼動率為主。2027 年起 ABF 月產能由約 4,000 萬顆增至 5,000 萬顆，2029 年底目標 8,000 萬顆，是量的來源。併購與回購沒有貢獻。","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"事實表沒有投入資本、折舊與營運資金，內生上界算不出，不填數字。共識 EPS 年化 213% 遠高於營收年化 46%，差距歸因於利潤率擴張，按超出內生上界處理。","segments":[{"item":"手機應用（2025 年第四季）","value":"35%"},{"item":"ABF／HPC（2025 年第四季）","value":"24%"},{"item":"消費性電子與記憶體（2025 年第四季）","value":"18%"},{"item":"隱形眼鏡（2025 年第四季）","value":"18%，2025 年毛利率 52%"},{"item":"基地台（2025 年第四季）","value":"5%"},{"item":"AI 相關營收占比（公司口徑）","value":"2026 年約 10%，2027 年 15%～20%"}],"decay_signals":["亮燈：EPS 增速遠高於營收增速，FY2025A 到 FY2027E 年化 213% 對 46%。","未亮但要看：FY2025 毛利率 21.13%，低於 FY2024 的 28.39%，2026 年第二季已回到 26.1%；去年同季數字事實表未涵蓋，連兩季年減無法確認。","未亮：FY2025 自由現金流為淨利的 1.07 倍；FY2024 為負值，但不是連兩年。","未亮：第二季 SBC 占營收 0.16%。","資料缺口：維護性資本支出比重、產業倍數三年走勢事實表未涵蓋。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月重大訊息沒有併購事項；事實表也沒有近三年股利、回購與現金去向分項。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月重大訊息與搜尋都沒有併購事項，無從計算已實現報酬。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購紀錄與均價。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"上半年 SBC 合計約 4.75 億元，年化約 9.5 億元，占市值約 0.27%，低於 1.5%。股數比 FY2025 多 11% 的原因未說明，不計入這項。","grade":"過"}]},"valuation":{"basis":"本益比，以 FY2027E 共識為主、FY2026E 為輔；循環股本應優先看股價淨值比，但事實表未涵蓋淨值。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或目標價，無法建立倍數對照。"},"fwd_pe":52.1,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價對 FY2026E 是 52.1 倍，對 FY2027E 是 20.3 倍。Base 年化報酬約 −2%，機率加權五年約 −5%，多空報酬比約 1.0，比前次好很多，但仍沒有補償循環風險，所以落在偏貴這一檔，未到最貴。五年分位事實表未涵蓋，只有四個年度端點：本益比第 11.2 百分位因 FY2023、FY2024 EPS 接近零而失真，P/S 與 EV/S 都在最高。三年 PEG 因 FY2028E 共識缺漏算不出；用 FY2025A 低基期算得 0.24，沒有意義；改用 FY2022 高點到 FY2027E 的年化 17.8% 算，約 1.1 倍。","upside_short_pct":-9.2,"upside_mid_pct":1.9},"trap_analysis":{"verdict":"🟡","label":"高點獲利被當成新基期"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY2023 營收跌 36.8%，EPS 由 14.57 元降到 0.10 元，2023 年前三季每股虧 0.7 元。這一輪主要廠商資本支出比上一輪高 51%，景碩新廠折舊從 2027 年起進損益，同業也在擴產。","assumption":"AI 需求在 2028–29 年持續吸收全產業新增產能。","consequence":"FY2030E EPS 跌到個位數，股價落到 104 週均線以下，五年虧損超過 50%。","ruling":"採納，列為 Bear 35%。與 Single Thing 的機制相同；Single Thing 抓報價第一次轉跌的時點，這裡補上折舊與客戶去庫存的放大效果。","watch":"ABF 稼動率、ABF 季均價、2027 年資本支出。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","supply_demand_durability#5"]},{"view":"論點成功但股東經濟變差","evidence":"味之素 ABF 膜市占九成以上，Nittobo 獨供 T-glass，限料每月影響 10%～15% 營收；最大客戶占比由 10.72% 升到 19.51%，客戶出資設備。","assumption":"短缺帶來的漲價大部分留在景碩。","consequence":"營收與產能都達標，但毛利率停在 30% 左右，新產能被客戶鎖定，現金大多再投入，每股盈餘低於 Base。","ruling":"部分採納。公司把第二季毛利改善歸因於稼動率，漲價的留存比例還沒有證據，列為中期風險。","watch":"ABF 報價上漲期間的合併毛利率變化、股本變動。","evidence_refs":["geo_supply_chain#1","supply_demand_durability#2","customer_concentration_credit#0"]},{"view":"價格已反映太多","evidence":"現價為 FY2027E 的 20.3 倍，共識隱含歸屬淨利率 20.8%，高於 FY2022 的 16.4%；EV/S 7.12 倍為四個年度端點最高；欣興在 AI ASIC 份額超過 70%，景碩的份額目標尚未實現。","assumption":"FY2027E 是新的獲利基期。","consequence":"Base 年化約 −2%，多空報酬比約 1.0，上漲空間補償不了循環風險。","ruling":"採納。下跌 36.7% 改善了報酬，但還不足以進場。","watch":"FY2027 共識 EPS、合併毛利率。","evidence_refs":["competitive_share_entrants#2"]},{"view":"論點失敗","evidence":"最近一次財報日是 11 月 3 日，事實表最新一季仍是第二季，也沒有逐字稿；同期股價由 1,060 元跌到 671 元，原因不在證據包內。","assumption":"FY2027 共識 33.12 元已反映第三季與最新展望。","consequence":"若第三季或展望轉弱，三條路徑都要下修；若第三季優於預期，本判斷偏保守。","ruling":"不可裁決至第三季財報與法說內容納入，在那之前不買進、不加碼。","watch":"第三季合併毛利率、營收季增率、法說對 2027 年報價的說法。","fact_refs":["f_earnings_recency","f_price_at_dd"]}],"max_dd":{"lo":-80,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1060.0 → 本次 671.0（-36.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1060.0","side_b":"本次 price_at_dd=671.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,060 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,060 元：Bull 價 1,550、Bear 價 180，五年期望值 −40.2%，基準年化 −11.4%，不對稱比 0.3","side_b":"本次情境、股價仍用 1,060 元：Bull 價 1,536、Bear 價 176，五年期望值 −39.7%，基準年化 −10.8%，不對稱比 0.31","ruling":"先換情境、股價不動：五年期望值多 0.5 個百分點，基準年化多 0.6 個百分點。不對稱比由 0.3 變為 0.31。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,060 元：五年期望值 −39.7%，基準年化 −10.8%，不對稱比 0.31","side_b":"本次情境、股價 671 元：五年期望值 −4.8%，基準年化 −2.2%，不對稱比 1.0","ruling":"再換股價、情境不動：起點價下跌 36.7%，五年期望值多 34.9 個百分點，基準年化多 8.5 個百分點，不對稱比由 0.31 升到 1.0。合計五年期望值比前份多 35.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"共識上修與股價大跌方向相反","cause":null,"prior_field":null,"side_a":"FY2027 共識 EPS 由前次 28.11 元升到 33.12 元，上修 17.8%。","side_b":"股價由 1,060 元跌到 671 元，跌 36.7%，RSI 28.17。","ruling":"證據包沒有第三季數字，也沒有下跌原因，不可裁決至第三季財報納入；在那之前不把跌幅當作便宜的理由。","evidence_level":"低","settle_metric":"2026 年第三季合併毛利率與營收季增率","if_then":["若第三季毛利率 ≥27% 且營收季增 ≥10%：情境不變，股價 ≤480 元才分批反買。","若第三季毛利率 <27% 或 FY2027 共識 EPS 下修超過一成：下修 Base 路徑，不追。"],"evidence_refs":[]},{"axis":"AI 敘事與 AI 營收占比","cause":null,"prior_field":null,"side_a":"賣方把景碩定位為 AI 供應商，FY2027 共識營收 837 億元，年增約 54%。","side_b":"公司口徑 2027 年 AI 相關營收只占 15%～20%，手機、PC 與消費性需求仍弱。","ruling":"兩者要同時成立，非 AI 營收須增加 37%～46%，大部分只能來自漲價，所以 FY2027 的成長屬價格驅動。可能看錯的地方是公司的 AI 定義或許不含伺服器 CPU。","evidence_level":"中","settle_metric":"法說會 AI 營收定義與 2027 年實際占比","if_then":["若 AI 定義已含伺服器 CPU 且 2027 年占比仍低於 20%：維持價格驅動的判斷，不追。","若定義不含 CPU 且含 CPU 後占比超過 40%：上調 Base 的量，重做研究。"],"evidence_refs":[]},{"axis":"多年短缺與擴產潮","cause":null,"prior_field":null,"side_a":"高盛估 ABF 缺口 2026 下半年、2027、2028 年為 14%、34%、51%；真空壓膜機交期排到 2031 年。","side_b":"另一外資估 2026–28 年缺口只有 4%、10%、16%；主要廠商資本支出比上一輪高 51%，景碩、欣興、南電、Ibiden 都在擴產。","ruling":"採信 2027 年仍短缺，不採信可延續到 2031 年。差距屬程度與時點，可以調和：短缺到 2028 年，之後新產能壓低報價。","evidence_level":"中","settle_metric":"ABF 稼動率與 ABF 季均價","if_then":["若 2027 年底稼動率仍 ≥90% 且報價續漲：Bull 機率上調到 30%，重做研究。","若稼動率低於 85% 或報價季減：減碼，已無持股則不進場。"],"evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：同業普遍擴產，未見明確的產能紀律聲明。","side_b":"結構：缺口預估在 2027–28 年擴大，客戶出資鎖產能。其他變數：玻璃核心 2027–2030 年導入，232 條款涵蓋與否未確認。","ruling":"雙向拉鋸。短期結構轉好，2028 年後競爭惡化的機率上升。","evidence_level":"中","settle_metric":"稼動率與 ABF 季均價","if_then":[],"evidence_refs":["cyclical_supply_discipline_capacity#2","substitute_technology#1"]},{"axis":"載板毛利率的資料衝突","cause":null,"prior_field":null,"side_a":"財報第二季合併毛利率 26.1%。","side_b":"Quartr 摘要一處寫合併毛利率 12.7%，另一處寫載板毛利率 14%～15%。","ruling":"合併數字採財報，12.7% 不採用。以合併毛利約 32.6 億元、非載板營收 21.1 億元按 2025 年晶碩毛利率 52% 粗算，載板毛利率約 20.8%，與 14%～15% 對不上，載板毛利率先視為未確認。","evidence_level":"低","settle_metric":"公司法說簡報的分部毛利率","if_then":[],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價一個月跌 36.7%，RSI 28.17，FY2027 本益比 20.3 倍；共識還在上修，設備交期排到 2031 年會拖慢新產能。若短缺延續過 2028 年，Base 的 FY2031E 30 元明顯偏低。","side_b":"跌幅不等於安全邊際。賣方共識的問題在成長基準：FY2027 獲利被當成往後的起點，沒有算進一次下行；12 位分析師全部買進，目標價最高與最低相差 2.8 倍。","ruling":"不採納，但保留反向條件。Base 機率不變時，Bull 機率要由 20% 升到約 35%，五年機率加權報酬才有 25%；目前沒有足以支持這個調整的一手證據。","evidence_level":"中","settle_metric":"FY2027 合併毛利率與 ABF 均價連續性","if_then":["若 ABF 均價連四季上漲且 FY2027 毛利率 ≥33%：Bull 機率上調到 30% 以上，重做研究，不等 480 元。","若股價續漲但第三季數字仍未驗證：不追。"],"evidence_refs":[]},{"axis":"估值結論與路徑風險隨股價調整","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前次股價 1,060 元，對 FY2027 共識 28.11 元是 37.7 倍，估值為最貴一檔，最大回撤估 −88%，多空機率 20％與 35％。","side_b":"現價 671 元，對 FY2027 共識 33.12 元是 20.3 倍，估值降一檔，回撤範圍改為 −55% 到 −80%，多空機率維持 20％與 35％。","ruling":"變化主要來自股價，機率不因股價改變。報酬仍不足，維持不進場的結論。","evidence_level":"高","settle_metric":"股價與 FY2027 共識 EPS","if_then":["若股價 ≤480 元且共識 EPS ≥28 元：重做研究，通過後分批反買。","若股價回到 900 元以上而第三季數字未驗證：不追。"],"evidence_refs":[]},{"axis":"基本面欄位維持不變","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前次：訊號評等 C、價值陷阱中等、護城河方向穩定、五年後跑道中等、循環股、晚循環。","side_b":"本次新增的證據只有 FY2027 共識上修 17.8%，第三季財報未納入，份額與擴產資料都是前次已有。","ruling":"六欄都不動。共識上修不足以改變循環位置，晚循環的依據是稼動率、報價與擴產，都沒有變化。","evidence_level":"中","settle_metric":"第三季財報與下一次法說","if_then":["若第三季顯示稼動率低於 90% 或報價停漲：循環位置改為過熱頂部，不追。","若第三季毛利率超過 29% 且 2027 年長約比重揭露：護城河定價分上調，重做研究。"],"evidence_refs":[]},{"axis":"估值rearm 進場門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價 ≤600 元（約 FY2027 共識 EPS 的 21 倍），且 FY2027 共識 EPS 未較 28.11 元下修逾一成","side_b":"股價 ≤480 元（約 FY2027 共識 EPS 的 14.5 倍），且 FY2027 共識 EPS 不低於 28 元；觸發後先重做研究","ruling":"舊方法是倍數乘共識，照舊用 21 倍乘新共識得 695 元，現價已符合，等於共識上修就自動放行，而分母是否為高點正是爭點。新門檻改用報酬法：600 元時多空報酬比約 1.3，480 元時約 2.0。這是股價接近舊門檻時才改的，有移動門檻的疑慮，下次複審要記錄：若未到 480 元就反轉上漲，這次改動錯過了多少。","evidence_level":"中","settle_metric":"480 元門檻是否觸發及之後的報酬","if_then":["若股價 ≤480 元且共識 EPS ≥28 元：重做研究，通過後分批反買。","若第三季與 2027 年指引上調 Base 路徑：按新路徑重算門檻，不沿用 480 元。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空，沒有舊門檻原文可比。","side_b":"合併季毛利率連兩季季減且低於 24%；FY2027 共識 EPS 低於 23.2 元；ABF 稼動率低於 85%；ABF 季均價出現季減。","ruling":"本次新設減碼與清倉門檻，對應毛利率、共識、稼動率與報價四個指標。","evidence_level":"中","settle_metric":"季報與共識追蹤","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空，沒有原文可比。","side_b":"2028 年底前，ABF 載板平均售價出現第一次季減。","ruling":"選報價，是因為它是獲利最大的單一敏感度，比 T-glass 限料或客戶流失的影響更大。","evidence_level":"中","settle_metric":"法說報價說明與合併毛利率","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"把 11 月 3 日公布的第三季財報納入，重新核對毛利率與營收。","type":"假設驗證","maps_to":"H1","metric":"2026 年第三季合併毛利率與營收季增率","threshold":"毛利率低於 27% 或營收季增低於 10%","action":"不追，並下修基準路徑","source_freq":"MOPS 季報，每季","date":"2026-11-30","evidence_refs":[]},{"n":2,"text":"股價跌到足以補償循環風險的價位，共識也沒有崩。","type":"估值rearm","maps_to":"H1","metric":"股價與 FY2027 共識 EPS","threshold":"股價 ≤480 元且共識 EPS ≥28 元","action":"重做研究，通過後分批反買","source_freq":"每日收盤，每月共識","date":null,"evidence_refs":[]},{"n":3,"text":"T-glass 與材料短缺壓住出貨。","type":"風險","maps_to":"R1","metric":"單季營收季增率","threshold":"連兩季低於 5%","action":"不追","source_freq":"月營收與季報","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"ABF 報價第一次轉跌。","type":"Single Thing","maps_to":"H1","metric":"ABF 載板季均價","threshold":"2028 年底前出現季減","action":"減碼","source_freq":"法說與法人報價調查，每季","date":"2028-12-31","evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0"]},{"n":5,"text":"擴產開出後稼動率回落。","type":"風險","maps_to":"R2","metric":"ABF 稼動率","threshold":"低於 85%","action":"減碼","source_freq":"法說與法人轉述，每季","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"n":6,"text":"客戶集中度進一步升高，或 AI GPU 份額沒有到位。","type":"風險","maps_to":"R3","metric":"最大客戶占比與 AI GPU 載板份額","threshold":"最大客戶超過 30%，或 2027 年底 AI GPU 份額低於 10%","action":"停止加碼","source_freq":"年報與法人調查，每年","date":null,"evidence_refs":["customer_concentration_credit#0","competitive_share_entrants#2"]},{"n":7,"text":"玻璃核心進入主要 AI 客戶量產。","type":"風險","maps_to":"R5","metric":"玻璃核心量產導入與景碩方案","threshold":"前三大 AI 客戶有一家宣布量產，且公司仍無相應方案","action":"停止加碼","source_freq":"產業新聞與法說，每季","date":null,"evidence_refs":["substitute_technology#1"]},{"n":8,"text":"共識大幅下修，毛利率同時走弱。","type":"清倉","maps_to":"H1","metric":"FY2027 共識 EPS 與合併季毛利率","threshold":"共識 EPS 低於 23.2 元，且毛利率連兩季季減","action":"清倉","source_freq":"每月共識與季報","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"n":9,"text":"AI 相關營收與產能進度驗證。","type":"假設驗證","maps_to":"H2","metric":"AI 相關營收占比與 ABF 月產能","threshold":"2027 年 AI 占比低於 15%，或月產能未達 5,000 萬顆","action":"不追","source_freq":"法說與年報，每半年","date":"2027-12-31","evidence_refs":[]},{"n":10,"text":"全年財報與 2027 年資本支出說明出爐，複審情境與 480 元門檻。","type":"複審日期","maps_to":"H1","metric":"FY2026 財報與 2027 年資本支出","threshold":"到期複審","action":"重做研究","source_freq":"年報與法說","date":"2027-03-31","evidence_refs":[]}],"kill_metrics":[{"metric":"合併季毛利率","bear_threshold":"連兩季季減且低於 24%","window":"未來 4 季","source":"MOPS 季報","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"低於 23.2 元（較 33.12 元下修三成）","window":"未來 12 個月","source":"yfinance earnings_estimate","last_status":"ok"},{"metric":"ABF 稼動率","bear_threshold":"低於 85%","window":"未來 8 季","source":"法說會與法人轉述","last_status":"ok"},{"metric":"ABF 載板季均價","bear_threshold":"出現季減","window":"至 2028 年底","source":"法說與法人報價調查","last_status":"unknown"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":"不超過總資金 3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=46.76, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價 ≤480 元（約 FY2027 共識 EPS 的 14.5 倍），且 FY2027 共識 EPS 不低於 28 元；觸發後先重做研究","exec_line":"現價不追。第三季財報納入前不買進。股價 ≤480 元且 FY2027 共識 EPS ≥28 元時先重做研究，通過後分兩批建立，合計不超過總資金 3%。"},"reasoning":{"industry":"2026 年第二季合併營收 124.96 億元，毛利率 26.1%，營業利益率 13.4%，其中載板營收 103.82 億元。2025 年第四季產品組合為手機 35%、ABF／HPC 24%、消費與記憶體 18%、隱形眼鏡 18%、基地台 5%。公司口徑的 AI 相關營收 2026 年約 10%，2027 年 15%～20%，市場的 AI 敘事目前只對應一小部分營收。第三季財報已在 11 月 3 日公布，但事實表最新一季仍是第二季，也沒有逐字稿，本判斷不含第三季數字。產業時鐘放在過熱段，依據是稼動率約 95%、部分現貨漲逾 30%、長約客戶同意支付產能相關款項、2025–28 年資本支出比上一輪高 51%，不是股價。單點依賴有三個：最大客戶占 19.51%，味之素 ABF 膜市占九成以上，Nittobo 獨供 T-glass。","moat":"機制是高層數 ABF 的製程良率與客戶認證。有利的證據是法人稱美系 AI 客戶 CPU 供貨率由 10% 升到 50%、ABF 稼動率由 86% 升到 95%；公司目標 Vera CPU 載板 100%、AI GPU 載板 20%，後兩項尚未實現。不利的證據是欣興在美系 AI ASIC 載板據報超過 70%，Nvidia Blackwell 相關超過 30%。利益率也沒有顯示領先：景碩近四季營業利益率 10.12%，低於欣興 13.30%、南電 12.27%、Ibiden 18.53%，而且景碩的合併數字還含高毛利的隱形眼鏡。欣興與 Ibiden 的資料截至九月，景碩截至六月，可比性有限。同業 ROIC 差距因事實表沒有投入資本而算不出。份額未被一手資料證實前，AI 順風只夠支持繼續追蹤，不支持付溢價。","growth":"成長以價格和稼動率為主，產能為輔。共識 FY2026E 12.88 元、FY2027E 33.12 元，FY2028E 事實表未涵蓋，三年 CAGR 算不出。FY2025A 到 FY2027E 的 EPS 年化 213%，營收年化 46%，兩者的差距是利潤率回升，不是再投資複利，情境樹因此按超出內生上界處理。另一個檢驗：公司口徑 2027 年 AI 占 15%～20%，代入共識營收 837 億元，非 AI 營收約 670～712 億元，比 2026 年約 488 億元增加 37%～46%，而手機與 PC 需求仍弱，這段成長大多要靠漲價。可能看錯的地方是公司的 AI 定義或許不含伺服器 CPU，若是如此，量的貢獻會比這裡高。","governance":"FY2025 自由現金流 17.1 億元，是歸屬淨利 16.0 億元的 1.07 倍，但 FY2022 至 FY2024 連三年為負。第二季自由現金流 3.15 億元。第二季 SBC 占營收 0.16%，占營業利益 1.2%；第一季同欄 4.55 億元疑含員工酬勞，跨季不可比。現金去向四分與債務到期結構事實表未涵蓋。總債務 162 億元、現金 213 億元，相對三年專案偏薄；若計入到 2029 年總規模 600～800 億元（設備由客戶出資），未來幾年要靠獲利兌現或對外籌資。流通股數 526.9 百萬股比 FY2025 由淨利與 EPS 推得的 473 百萬股多 11%，事實表沒有說明是增資、轉換或資料口徑差異。","valuation":"FY2027E 共識隱含歸屬淨利約 174.5 億元（33.12 元乘 526.9 百萬股），占共識營收 20.8%，高於 FY2022 高點的 16.4%。Base 用 FY2031E 30 元乘 20 倍得 600 元，低於現價。短期目標以 FY2027 Base 29 元乘 21 倍得 609 元，中期以 FY2028 Base 38 元乘 18 倍得 684 元。成長熄火測試用 FY2029 Base 40 元：成長降到 15% 給 22 倍得 880 元；降到 10% 給 16 倍得 640 元；降到 5% 給 12 倍得 480 元，三種情況只有第一種高於現價。賣方目標價 FactSet 620 元（6 月）、Investing.com 868～892 元（日期偏舊），最高 1,250 元與最低 450 元相差 2.8 倍，共識不穩，不作為支持依據。同業本益比事實表未涵蓋，終端倍數無法附同業對照，只能對照自身 FY2027E 的 20.3 倍；循環股優先看的股價淨值比也因缺淨值而無法使用。","premortem":"股價由前次 1,060 元跌到 671 元，RSI 28.17，26 週報酬仍有 +46.76%，股價也還在 52 週均線 536 元之上。下跌原因無法判斷，所以跌幅不當作安全邊際。這家公司沒有可守的核心：FY2022 至 FY2024 自由現金流連三年為負，FY2023、FY2024 EPS 接近零，應按循環交易紀律處理，不用長抱的波動容忍。價值陷阱風險中等，亮燈的衰退訊號只有 EPS 增速遠高於營收增速一項，但這項正是爭點。附錄的品質分只反映 AI 不會取代載板製程，不代表獲利品質。"},"plain":{"six":{"how_it_makes_money":"景碩賺的是高階 ABF 與 BT 載板的加工錢，外加晶碩的隱形眼鏡獲利。目前的超額利潤來自短缺，錢卡在上游獨供材料與下游少數大客戶之間。","moat":"護城河方向為穩定（→）。執行力在進步，定價能力仍靠短缺，份額提升還沒有一手資料證明。","growth":"第五年後的跑道為中等（🟡）：ABF 產能可以翻倍到 2029 年，之後沒有已證實的第二條成長曲線。","capital":"資本配置尚未被證明：上一輪四年自由現金流合計 −65 億元，這一輪又要投入 196～235 億元，而淨現金只有 51 億元。","valuation":"671 元要划算，33.12 元的 FY2027 共識就不能是高點，2031 年還要維持 33 元以上的 EPS 與 20 倍本益比。我相信 2027 年大幅成長，不相信這個獲利水準能不經下行就延續。","how_wrong":"最可能看錯的地方有兩個：第三季數字和股價大跌的原因都不在證據包裡；短缺若延續過 2028 年，基準情境就偏低。"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"追蹤","wait_for_price":true,"wait_for_price_condition":"等股價 ≤480 元，且第三季財報納入後 FY2027 共識 EPS 不低於 28 元。","trap":"🟡","val":"🟠","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":671.0,"week26_return_pct":46.76,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"20.3 倍的分母 33.12 元是上一輪高點 14.57 元的 2.3 倍，隱含歸屬淨利率高於 FY2022。分母是否為景氣高點正是爭點，本益比看起來便宜不能當買進理由。另外 P/S 7.22 倍隱含近四季營收約 490 億元，比截至第二季的約 448 億元多，來源未說明；EV 也沒有計入少數股權。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報（11 月 3 日公布）與法說內容納入研究","impact":"高","watch":"合併毛利率是否落在 27%～29%，營收季增是否 ≥10%"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"2026 全年財報與 2027 年資本支出說明","impact":"高","watch":"資本支出 80 億元與 140 億元兩種說法何者成立，新廠折舊時點"},{"date":"2027-09","date_precision":"quarter","type":"capacity","event":"Nittobo T-glass 擴產開始貢獻","impact":"高","watch":"限料緩解後，景碩營收是否加速，報價是否鬆動"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"楊梅與幼獅新廠 ABF 產能陸續開出，月產能往 5,000 萬顆","impact":"高","watch":"新產能稼動率與折舊對毛利率的影響"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"玻璃核心基板供應商目標開始供貨","impact":"中","watch":"主要 AI 客戶是否導入，景碩有沒有對應方案"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,392B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河 C 級，執行力改善但定價力沒有。</p>
<ul class="pts">
<li>機制是高層數 ABF 的製程良率加客戶認證。認證通過後份額移動很快，法人稱美系 AI 客戶 CPU 供貨率由 10% 升到 50%。快的另一面是份額能移進來，也能移出去。目前的定價能力主要來自全產業短缺。</li>
<li>評分上執行力 7、定價力 5，等級 C，方向持平。執行力的證據是第二季毛利率由 21.16% 升到 26.09%，ABF 稼動率據法人由 86% 升到 95%。定價力沒有擴大的證據，公司自己把毛利改善歸因於稼動率。前次判斷以來沒有新的份額資料，第三季也未納入，方向維持。</li>
<li>公司的目標很大。Vera CPU 載板要做到 100%，AI GPU 載板要做到 20%，但這兩項都還沒實現。不利的證據是欣興在美系 AI ASIC 載板據報超過 70%，Nvidia Blackwell 相關也超過 30%。景碩要從後段搶份額，屬點對點競爭，機率約 40%。</li>
<li>利潤率沒有顯示領先。景碩近四季營業利益率 10.12%，低於欣興 13.30%、南電 12.27% 與 Ibiden 18.53%。景碩的合併數字還含高毛利的隱形眼鏡，2025 年隱形眼鏡毛利率 52%，扣掉之後載板本業只會更低。欣興與 Ibiden 的資料截至九月，景碩截至六月，可比性有限。</li>
<li>替代技術是最大的結構風險。玻璃核心基板最快 2027 年底導入，最晚說法 2030 年，機率約 30%。Intel 的設計仍保留 ABF 增層，受衝擊的是核心層。事實表沒有景碩的玻璃基板計畫，所以景碩若被排除在外，沒有可見的對應方案。</li>
<li>價值鏈位置不利。上游味之素與 Nittobo 各自獨供，下游是少數 AI 大廠並出資鎖設備，景碩夾在中間。短缺的好處能留下多少沒有證據。需求基礎也分兩層，公司口徑 AI 相關營收 2026 年只占約 10%，其餘營收的需求仍弱。</li>
<li>同業 ROIC 差距因事實表沒有投入資本而算不出，不以推估補值。份額沒有被一手資料證實前，AI 順風只夠支持繼續追蹤，不支持付溢價。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
<div class="mach">同業期間：欣興與 Ibiden 為近四季到 2026 年 9 月，南電到 2026 年 6 月，景碩到 2026 年 6 月。</div></section>

```