你是 stock-analyst v20 的**散文層（prose）agent**，標的 NUE（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NUE_20261103/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：NUE　日期：2026-11-03　archetype：None　前份裁決：2026-05-25　B 觀望偏進場；等回測 $180-200 (W52 + BB 中軌) 或 WV mill 2027 commissioning + Section 232 維持 50% 確認後分批｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1753B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（429B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（808B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1548B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1318B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（481B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（999B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2375B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3341B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3168B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1753           3673-5247      5 條（2–6 內）  
s3                  8000         429           5300-7571      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3674          7928-11326      5 條（2–6 內）  
s6                 11000         481          7363-10519      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         999           1751-2501      5 條（2–6 內）  
s10                 5000        2375           1837-2625      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3168           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4845B；至少需散文≈40.16KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−50%
−48%
−45%
−40%
−35%
−35
−26%
−9.8%
−5.2%
−5.2
−5%
−4.1%
−4.1
−2.42%
−1.88
−1.41%
−1.1%
−0.11
0
0%
0.25
0.38
0.40
0.5%
0.56
0.75
0.79
0.8%
0.8
1%
01
1
1.05
1.2
1.26
1.4
1.46
1.66
1.75
2%
2
2.27
2.32
2.54%
2.64
2.8%
3
03
3%
3.1%
3.19
3.53
3.81%
4
4%
4.05
4.1
4.65
5%
05
5
5.1%
5.80
6%
6
6.45%
6.5
6.9%
07
7
7%
7.52
7.93
8
8.46
8.5
8.76%
9
9.26%
10%
10
10.5
10.66%
10.8%
11%
11
11.89%
11.93%
12
12.5
13
13%
13.3
14
14%
14.49
15%
15
15.6
15.94%
16
16.5
16.7%
17%
17.3
17.5
17.9
18.0
18%
18
18.13
18.65%
18.74
18.9%
19
19.1
19.5
19.65
19.8%
19.95
20%
20
020
20.5
21
21.0
21.41
22%
22.7%
22.79
23
23%
23.5
24
24.5
25
25%
26
26.5
26.6
26.69
26.7%
27%
27
28
28.1%
28.79
30%
30
30.12%
31
32
32%
33
34.53
35
35%
38.4%
40%
41%
42
42%
43.6
45%
45
49
50
50%
52
52%
57%
58
60%
61
69%
70
74%
76.1
80
80%
83
85%
89%
90
91
95%
100%
100
104
112.49
140
147
150%
150
155.30
170
170.38
180
190
200
232.0
232
250
254
270
273
283
284.71
297
330
340
420
500
700
720
745
867
923
2014
2015
2016
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
20261103
1,000
1,200
1,255
1,350
1,493
7,533
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
{"meta":{"ticker":"NUE","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Nucor Corporation"},"oneliner":"Nucor第三季交出三年來最佳單季，但熱軋價一年漲五成、2028年共識EPS已轉跌，股價284.71美元高於賣方平均目標；判斷處於晚循環，等股價回到200美元以下且進口管制未鬆再重新評估。","thesis":{"H":[{"id":"H1","text":"進口管制維持有效，美國成品鋼進口市占守在18%以下，讓鋼價維持在上一輪谷底之上","2y":"2027–2028：232維持50%，進口市占季度≤18%，熱軋卷價格多數月份≥1,000美元/短噸","5y":null,"10y":null,"threshold":"進口市占季度≤18%（2026Q3約17%）；232稅率50%","source":"Nucor季度投資人簡報進口市占頁、白宮與商務部公告、Fastmarkets熱軋卷價格","drift_rule":"進口市占連2季高於門檻5%以上（>18.9%）→削弱；連3季高於門檻10%以上（>19.8%）→反轉"},{"id":"H2","text":"新產能爬坡把出貨與每股盈餘墊高：西維吉尼亞薄板廠、Berkeley汽車級鍍鋅線、塔架事業如期達標","2y":"2027年底西維吉尼亞稼動率約50%，Berkeley鍍鋅線2027年底滿產（年50萬噸）","5y":"2029–2031：西維吉尼亞年產約100萬噸汽車鋼（其中約10萬噸外板），塔架長期EBITDA約2億美元","10y":null,"threshold":"2027Q4西維吉尼亞稼動率≥50%；2028年起汽車認證；塔架EBITDA達約2億美元","source":"Nucor季度法說與年報","drift_rule":"稼動率進度連4季落後計畫5%以上→削弱；連6季落後10%以上→反轉"},{"id":"H3","text":"週期谷底上移：下一輪下行的谷底年度EPS不低於8美元，年度FCF維持正值","2y":null,"5y":"2028–2031的最低年度EPS≥8美元（2024年8.46、2025年7.52），最低年度FCF≥0（2025年−1.88億美元）","10y":null,"threshold":"谷底年度EPS≥8美元；年度FCF≥0","source":"Nucor年報","drift_rule":"TTM EPS連4季低於門檻路徑5%以上→削弱；連6季低於10%以上→反轉"}],"R":[{"id":"R1","text":"232放寬或進口繞道回流，壓低美國鋼價","h_ref":"H1","clock":"🔥","threshold":"進口市占連2季>18%，或232稅率調降、主要來源國豁免公告","evidence_refs":["reg_tariff_export#1","competitive_share_entrants#3","competitive_share_entrants#1"]},{"id":"R2","text":"北美新電爐產能與全球過剩產能同時壓縮價差","h_ref":"H3","clock":"🔥","threshold":"Nucor鋼廠稼動率連2季<80%（2026Q3為89%），或鋼廠外部均價連2季季減合計≥10%","evidence_refs":["supply_demand_durability#0","supply_demand_durability#4","supply_demand_durability#5","cyclical_supply_discipline_capacity#2","competitive_share_entrants#4"]},{"id":"R3","text":"景氣反轉幅度重演前幾輪：價格先跌、盈餘腰斬","h_ref":"H3","clock":"⚡","threshold":"Nucor CSP 6週內累計下調≥15%，或季度EPS指引季減≥20%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5"]},{"id":"R4","text":"西維吉尼亞啟動成本高於預期、爬坡延後","h_ref":"H2","clock":"🔥","threshold":"2027年開辦與啟動成本高於2026年，且2027Q4稼動率<40%","evidence_refs":[]},{"id":"R5","text":"原料成本與地緣供應：仍外購大部分廢鋼替代品與球團，鐵礦與DRI成本擠壓價差","h_ref":"H3","clock":"🐢","threshold":"原料段連2季虧損，或管理層連2季把轉換成本上升列為盈餘下修主因","evidence_refs":["geo_supply_chain#3"]},{"id":"R6","text":"資料中心與電力投資放緩，需求延伸落空","h_ref":"H3","clock":"🔥","threshold":"四大雲端業者連2季下修資本支出指引>15%","evidence_refs":[]}],"single_thing":{"description":"232鋼鐵關稅由50%調降至25%或以下，或對加拿大、墨西哥、南韓等主要來源國給予配額或豁免","why_fatal":"盈餘對鋼價的敏感度最大，而鋼價的地板來自進口管制：232全面恢復後進口占比由逾22%降到約15%，鋼廠段Q3稅前17.9億美元（去年同期7.93億）。前幾輪價格回落時，鋼廠均價年減27%（2016Q1）、季度EPS年減逾60%（2024Q2）。","if_happens":"悲觀情境成為主路徑：2029–2030年EPS約8美元、股價約140–150美元；不建倉，持有者清倉。","how_monitor":"白宮與商務部公告、USMCA檢討進度、Nucor每季簡報的進口市占（現約17%）","probability":"15%（12–24個月）：現任政府支持232並推動USMCA北美熔煉澆鑄條款，但南韓進口前三季+57%，顯示豁免與繞道壓力已經存在"}},"appendix_a":{"growth_durability":5,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.3,"peg_fy2":17.5,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":7.52,"FY2026E":19.65,"FY2027E":21.41,"FY2028E":19.95},"fy_end_month":12,"eps_basis":"GAAP稀釋EPS；Q3 2026無調整項，Non-GAAP等於GAAP；FY2025A取年報稀釋EPS，FY2026E–FY2028E為Koyfin 2026-10-31共識（家數事實表未涵蓋）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NUE_20261103/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"鋼鐵業；營收由售價驅動（2022→2024營收−26%）；毛利率峰谷擺動約18pp（30.12%→11.93%）；2015年EPS僅0.25"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉、供給可逆性高：OECD估2028年全球過剩產能745百萬噸；北美Calvert電爐2026下半年滿產、Big River二期2027、現代製鐵與POSCO路易斯安那電爐2029；進口市占已由約14%回升至約17%。","bargaining":{"up":"自有DJJ廢鋼與兩座DRI廠（2025年約330萬公噸）降低依賴，但仍外購大部分原料，生鐵與球團受地緣供應影響。","down":"客戶分散，最大單一客戶約占銷售5%；年報自承以價格與服務競爭，買方議價不集中，但價格跟著市場走。","geo":"232關稅與USMCA檢討決定進口量；南韓進口前三季+57%，管理層稱在232之下仍大量湧入。"},"profit_pool_dir":"關稅下利潤池由進口流回美國本土業者；本土內部由高爐流向電爐（汽車外板是最後一塊）。五年淨流向數字事實表未涵蓋。","tam_table":{"expanded":false,"reason":"成熟商品市場，不屬低滲透、新品類或份額擴張主導；美國鋼需年增約2%（管理層與worldsteel），利潤池占比數字事實表未涵蓋。"}},"moat":{"mechanism":"成本位置加產品廣度：電爐以廢鋼與自有DRI煉鋼、上游有DJJ廢鋼，下游延伸到鋼構件、管材、塔架與建築系統，可供應資料中心約95%的鋼材；廠址靠近廢鋼來源與客戶。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Q3出貨連3季創紀錄，Brandenburg約占板材群出貨三分之一，汽車平板出貨年增4%（同期北美汽車產量持平），取得GM汽車外板平台；定價面縮減：進口市占由約14%回升至約17%，南韓前三季+57%，北美近五年資本支出近500億美元、現代製鐵與POSCO電爐2029投產。兩者相抵判持平。","peer_na_reason":"同業ROIC事實表未涵蓋，改以營業利益率與FCF利潤率作可比軸。","threats":[{"level":"🟡","text":"進口回流：進口市占由2025Q4約14%升至2026Q3約17%，南韓前三季+57%；屬全產業價格壓力，不改變Nucor相對成本位置。","p":"40%","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#1"]},{"level":"🟡","text":"新進電爐產能：現代製鐵與POSCO路易斯安那58億美元電爐（2029，主攻車用）、Calvert電爐、Big River二期，北美近五年資本支出近500億美元；直接衝擊薄板與汽車板份額。","p":"35%","evidence_refs":["competitive_share_entrants#4","supply_demand_durability#4","cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"232放寬：年報稱關稅可能被修改或終止；打擊的是全體美國業者的利潤池，而非Nucor相對同業的優勢，故列點對點，另列為唯一致命點。","p":"15%（12–24個月）","evidence_refs":["reg_tariff_export#1"]},{"level":"🟡","text":"替代材料：混凝土、鋁、塑膠、複合材料與木材在部分用途競爭；未見加速證據。","p":"10%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"全球過剩產能：OECD估2028年達745百萬噸、稼動率降至74%以下，規避貿易措施增加，靠關稅擋住的進口有被繞道的風險。","p":"30%","evidence_refs":["supply_demand_durability#0","supply_demand_durability#5"]}],"roic_durability":{"quadrant":"低利益率×低周轉（推定）：TTM營業利益率11.89%、Q3單季16.7%，資本密集；投入資本與杜邦拆解事實表未涵蓋，改查成本曲線位置，電爐加廢鋼與DRI整合位於美國成本曲線低端。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者與付款者多為同一家營建商、電力公司或車廠，鋼材是需要而非想要；急迫性不等於持久性，資料中心約占全公司積壓訂單15%、型鋼30–35%，基建未撥款逾1,350億美元、電力業五年約1.4兆美元，可撐到2028，之後回到美國鋼需年增約2%的基礎值。"},{"item":"決策層級","level":"🟡","text":"替代性在決策最小單位衡量：鋼筋、熱軋等大宗等級客戶按價格與服務比價，換供應商幾乎無成本；汽車外板與特殊板材需PPAP與數年認證，轉換成本高，但Nucor汽車占比約10%，高替代性等級仍是主體。"},{"item":"價值鏈分配","level":"🟡","text":"上游自有DJJ廢鋼與兩座DRI廠，下游延伸到鋼構件、管材、塔架與建築，能多拿幾段利潤，買方分散（最大客戶約5%）；但仍外購大部分原料，原料段Q3稅前1.05億美元低於Q2的1.46億，整條價值鏈的利潤總量由鋼價決定，Nucor拿得多不代表總量穩。"},{"item":"社會容忍度","level":"🟡","text":"當前利潤靠232這項政策授權撐住：年報明說關稅可能被修改或終止，USMCA檢討已在進行，熱軋價一年漲52%，下游製造業對高鋼價的容忍度是看不見的價格天花板；現任政府支持，2028大選是下一次檢驗。"}],"roiic":"事實表未涵蓋：Q3法說稱6.5年部署約190億美元（半數有機、半數併購），但2026E EPS 19.65仍低於2022年28.79，增量報酬須待西維吉尼亞2027–2028爬坡後才可驗證。","reinvest_rate":"約20%（推估）：2026資本支出約25億美元（Q3法說）減年化折舊約16億美元（Q3 EBITDA 22.79億減營業利益18.74億＝4.05億，乘4），約9億美元，除以2026E淨利約45億美元（FY1 EPS 19.65乘約2.27億股）；營運資金與收購未計。","endo_ceiling":null,"formula_note":"內生成長率＝增量ROIC×再投資率；增量ROIC缺值，不給數字上界。即使以15%增量報酬計，上界約3%，遠低於共識三年EPS年化38.4%。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","NUE":15.94,"STLD":14.33,"CMC":18.65,"CLF":1.54,"RS":28.1,"unit":"%"},{"metric":"營業利益率","NUE":11.89,"STLD":10.66,"CMC":9.26,"CLF":-1.41,"RS":8.76,"unit":"%"},{"metric":"FCF 利潤率","NUE":3.81,"STLD":2.54,"CMC":5.1,"CLF":-2.42,"RS":2.83,"unit":"%"}],"competitors":[{"name":"STLD","gm":14.33,"om":10.66,"fcf_margin":2.54,"strategy_note":"同為電爐薄板龍頭，營業利益率10.66%略低於NUE，在薄板與汽車板是最直接的對手，NUE西維吉尼亞投產後份額競爭加劇。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CMC","gm":18.65,"om":9.26,"fcf_margin":5.1,"strategy_note":"長材與鋼筋為主，毛利率18.65%高於NUE但營業利益率9.26%較低；NUE法說承認鋼筋與型鋼有新競爭者進入。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"CLF","gm":1.54,"om":-1.41,"fcf_margin":-2.42,"strategy_note":"高爐整合廠、汽車板主力，營業利益率−1.41%、FCF利潤率−2.42%，9月宣布裁員最多500人；是NUE汽車外板搶份額的對象。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"RS","gm":28.1,"om":8.76,"fcf_margin":2.83,"strategy_note":"下游金屬服務中心，屬客戶端而非同類生產者，毛利率28.1%反映加工通路角色，營業利益率8.76%；作為價值鏈下游參照。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"價格為主、量為輔：Q3營收年增約32%，鋼廠出貨年增約11%、外部均價走高；近年每年淨減股約2–4%加成每股盈餘；併購不是近期成長來源。","runway_years":"不適用：成熟商品市場，滲透率框架無效；Nucor份額擴張空間事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"增量ROIC事實表未涵蓋，內生上界不定值；以再投資率約20%乘假設增量ROIC 10–15%框出約2–3%。共識FY2025A 7.52→FY2028E 19.95年化38.4%，缺口約35pp歸因利潤率擴張（鋼價回升與關稅），屬週期回升，不是內生成長；淨回購另貢獻每年約2%。","segments":[{"item":"鋼廠","value":"Q3稅前17.9億美元（Q2約15.6億、去年同期7.93億），出貨逾720萬短噸連3季創紀錄，稼動率89%"},{"item":"鋼製品","value":"Q3稅前4.65億美元（Q2 3.53億、去年同期3.19億），EBITDA利潤率季增約200基點，積壓訂單約+25%"},{"item":"原料","value":"Q3稅前1.05億美元（Q2 1.46億），DRI實現價走低，Q4預期再小降"}],"decay_signals":[{"signal":"毛利率連2季年減","lit":false,"evidence":"TTM毛利率15.94%高於FY2025的11.93%"},{"signal":"核心市占近12個月縮減","lit":false,"evidence":"Q3出貨連3季創紀錄、年增約11%；Nucor自身市占數字事實表未涵蓋"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"Q3量價齊升；Q4量減為季節性與停機"},{"signal":"EPS成長顯著高於營收成長（差>5pp）","lit":true,"evidence":"FY2025A→FY2027E EPS年化約69%、營收年化約15%；屬谷底反彈"},{"signal":"FCF/淨利<0.75連2年","lit":true,"evidence":"2024年約0.40、2025年約−0.11；2026前三季回升至約0.8"},{"signal":"SBC/營收>5%且上升","lit":false,"evidence":"SBC僅占稅前盈餘2.8%"},{"signal":"TAM萎縮或被替代技術壓縮","lit":false,"evidence":"美國鋼需2026年約+2%；替代材料為長期風險，未見加速"},{"signal":"產業估值倍數近3年系統性下移","lit":null,"evidence":"事實表未涵蓋"},{"signal":"維護性資本支出占FCF>60%","lit":null,"evidence":"事實表未涵蓋"},{"signal":"停止投資新產能且收入3年內下滑","lit":false,"evidence":"2026資本支出約25億美元，約60%用於成長專案"}],"trap_rating":"價值陷阱風險🟡（亮2項）；長期成長性🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：2026前三季回饋股東近14億美元、占淨利42%，承諾每年至少返還淨利40%；併購明細與報酬事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"6.5年部署約190億美元、約半數用於併購（Q3法說），併購後已實現增量報酬未揭露，事實表未涵蓋；管理層自承塔架併購曾數度失手，改走自建。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購均價與10年期公債殖利率事實表未涵蓋；以現價計FY1盈餘殖利率約6.9%（19.65÷284.71）。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC占稅前盈餘2.8%（前三季）；股數由2022年約2.64億股降至2025年約2.32億股（淨利除以稀釋EPS推算），目前約2.27億股，淨稀釋為負。","grade":"過"}]},"valuation":{"basis":"Forward P/E（FY1與FY2共識）對照五年平均EPS；商品循環的主尺應是P/B，但股東權益事實表未涵蓋","peers":{"expanded":false,"reason":"同業倍數事實表未涵蓋，只有毛利率、營業利益率與FCF利潤率；終端倍數以自身現值FY1 14.49倍與trailing 18.13倍作錨"},"peg":19.1,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"五年分位事實表未涵蓋，只有4個年度端點（本益比76.1分位、P/S與EV/S 100分位）。現價284.71美元：FY1 14.49倍、FY2 13.3倍，乘在景氣高點附近的盈餘；以2022–2026E平均EPS約16.5美元計約17.3倍；股價高於7–8月賣方平均目標。12個月：中性情境FY2027E 21.0美元乘13倍＝273美元（−4.1%）；5年：中性情境2031年18.0美元乘15倍＝270美元（−5.2%）。上下檔都不足，判偏貴。","upside_short_pct":-4.1,"upside_mid_pct":-5.2},"trap_analysis":{"verdict":"🟡","label":"中等：亮2項，皆屬谷底基期效應；若2026全年FCF/淨利≥0.75則降為1項"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2024年EBITDA 43.6億美元較2023年降41%；2015年EPS 0.25、ROE 1%；2014–2015鋼價跌勢延續約83週；北美2026–2029新電爐產能陸續投產（Calvert、Big River二期、西維吉尼亞、現代製鐵與POSCO路易斯安那）。","assumption":"本輪需求延伸與關稅足以吸收新產能。","consequence":"232放寬或產能洪水任一成立，2029–2030年EPS回到約8美元，股價回到140–150美元（約−50%），即悲觀情境。","ruling":"採納：悲觀機率給35%，高於一般的25–30%，理由是內生成長遠低於共識且新產能時點落在五年窗內。與唯一致命點部分重疊（232是觸發之一），產能洪水是獨立路徑，另以稼動率監測。","watch":"進口市占、Nucor鋼廠稼動率、CSP與熱軋卷價格","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#3","cyclical_prior_downcycle_behavior#4","supply_demand_durability#4","competitive_share_entrants#4","cyclical_supply_discipline_capacity#2"],"fact_refs":["f_kpi8","f_price_at_dd"]},{"view":"論點失敗","evidence":"年報：無法保證232或其他進口關稅何時會被修改或終止；熱軋價一年漲52%至約1,255美元/短噸；USMCA檢討已啟動。","assumption":"下游製造業與政治端能長期容忍高鋼價。","consequence":"價格上限由政治決定，低於經濟上限；政策一鬆，價格地板消失。","ruling":"採納為唯一致命點，12–24個月機率15%；五年內機率較高，已計入悲觀情境。","watch":"白宮與商務部公告、USMCA檢討進度","evidence_refs":["reg_tariff_export#1"],"fact_refs":["f_kpi9_asp"]},{"view":"論點成功但股東經濟變差","evidence":"Q3法說：6.5年部署約190億美元（半數併購），未來現金主要投入Expand Beyond，並承認塔架併購曾數度失手；2026E EPS 19.65仍低於2022年28.79；Nucor自己的西維吉尼亞產能也是新增供給的一部分。","assumption":"高點現金流會以高於資金成本的報酬再投資，或返還股東。","consequence":"需求與關稅都撐住，但現金流進入報酬未經驗證的下游併購，或自家新產能壓低價差，每股價值增長低於盈餘增長。","ruling":"部分採納：每年至少返還淨利40%與A-評等限制了傷害；單筆併購若超過市值5%即重評。","watch":"單筆併購金額>約32億美元（市值5%）、併購後揭露的報酬","fact_refs":["f_kpi5_fcf","f_ev_m"]},{"view":"價格已反映太多","evidence":"股價284.71美元高於7–8月賣方平均目標（約254–283美元，最高297、最低190）；P/S與EV/S在4個年度端點最高；FY3共識19.95低於FY2的21.41，市場已預期2027見頂；26週漲26.7%。","assumption":"2028年後盈餘不會像前幾輪那樣回落。","consequence":"中性情境5年報酬約−5%（含息約0%），上檔有限。","ruling":"採納：觀望，約束條件是估值相對週期位置過高。","watch":"FY2028E共識修正方向、股價與200美元重啟條件的距離","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_price_at_dd","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy2","f_consensus_eps_fy3","f_week26_return_pct"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 232.0 → 本次 284.71（+22.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=232.0","side_b":"本次 price_at_dd=284.71","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 232 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 232 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 232 美元：Bull 價 420、Bear 價 147，五年期望值 +10.8%，基準年化 3.1%，不對稱比 1.26","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.26。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 232 美元：五年期望值 +10.8%，基準年化 3.1%，不對稱比 1.26","side_b":"本次情境、股價 284.71 美元：五年期望值 −9.8%，基準年化 −1.1%，不對稱比 0.56","ruling":"再換股價、情境不動：起點價上漲 22.7%，五年期望值少 20.5 個百分點，基準年化少 4.1 個百分點，不對稱比由 1.26 降到 0.56。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：2027仍是盈餘上行年","cause":null,"prior_field":null,"side_a":"管理層（2026-10-27，Jack Sullivan與Leon Topalian）：2026可望是公司史上第三好的年度，2027更強；Q4盈餘與Q3持平到小幅高於。","side_b":"共識FY2027E 21.41高於FY2026E 19.65，FY1近3個月上修6.45%；股價26週漲26.7%。","ruling":"三方一致，分歧不在2027而在2028之後：共識FY2028E 19.95已低於2027。","evidence_level":"高：公司指引與共識快照","settle_metric":"FY2028E共識修正方向","if_then":["若FY2028E共識連2季上修且高於FY2027E，則週期見頂時點後延，重跑研究"],"evidence_refs":["capital_markets_pricing#3","end_markets#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：進口市占由約14%回升至約17%、南韓前三季+57%；北美近五年資本支出近500億美元，現代製鐵與POSCO路易斯安那58億美元電爐2029投產。","side_b":"結構轉好：232全面恢復後進口占比由逾22%降至約15%；基建未撥款逾1,350億美元、電力業五年約1.4兆美元投資；電爐取得汽車外板平台。其他結構變數：USMCA檢討要求北美熔煉澆鑄。","ruling":"雙向拉鋸：結構順風仍在，但競爭面的惡化已開始（進口回升），2027–2029新產能上線決定勝負。","evidence_level":"中：公司簡報、年報與產業媒體","settle_metric":"進口市占與Nucor鋼廠稼動率","if_then":["若進口市占連2季>18%且稼動率<85%，則改判競爭惡化中，悲觀機率上調至40%"],"evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#4","cyclical_supply_discipline_capacity#2","competitive_share_entrants#2","reg_tariff_export#0"]},{"axis":"管理層說法對照：進口","cause":null,"prior_field":null,"side_a":"2026-07-28 法說（Leon Topalian）：成品鋼進口年減25%；型鋼進口上升，但「不是價差驅動」。","side_b":"2026-10-27 法說（Leon Topalian）：近月進口回升，南韓在232之下仍大量湧入，「必須保持警覺」；投資人簡報進口市占由約14%升至約17%，年減幅縮到13%。","ruling":"可調和（程度差異）：進口仍比去年少，但邊際已轉向；採納為進口風險的早期訊號。","evidence_level":"高：同一講者兩季說法與公司簡報","settle_metric":"進口市占季度值","if_then":["若2026Q4進口市占>18%，則進口論點列削弱並停止任何加碼","若回落至≤15%，則進口風險降為觀察"],"evidence_refs":["competitive_share_entrants#3","reg_tariff_export#2"]},{"axis":"結構性改善或週期高點","cause":null,"prior_field":null,"side_a":"結構派：電爐份額擴大、232保護、基建、能源與資料中心需求延伸至2028，塔架積壓訂單到2028初，2027合約條件更好（折扣少、附加價高）；管理層稱2027更強。","side_b":"週期派：FY3共識19.95低於FY2的21.41；熱軋價一年漲52%至2022年5月以來高點；前幾輪下行2024年EBITDA年減41%、2015年EPS 0.25；新產能2026–2029上線。","ruling":"可調和（程度差異）：兩邊各對一部分。本次採週期派定價（中性情境2029–2031年EPS 16–18美元），結構派只上修谷底、不消除谷底。依據：2022→2025年EPS由28.79降到7.52的擺幅，以及新產能時點。","evidence_level":"高：年報與共識數字","settle_metric":"下一個谷底年度EPS、進口市占","if_then":["若股價跌至≤200美元而進口市占≤18%、稼動率≥85%，則重跑研究後分批反買，首倉≤3%","若FY2028E共識連2季上修至≥23美元且熱軋卷價格維持≥1,200美元，則結構派勝出，重跑研究並上調中性情境終端EPS","反向：若進口市占連2季>20%或232放寬，則不建倉，持有者清倉"],"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#3","supply_demand_durability#4","end_markets#2"]},{"axis":"管理層說法對照：西維吉尼亞2027年貢獻","cause":null,"prior_field":null,"side_a":"2026-07-28 法說（Leon Topalian）：2027是爬坡年，不確定能否貢獻獲利。","side_b":"2026-10-27 法說：Jack Sullivan稱對2027盈餘前景振奮；同場Stephen Laxton稱2027啟動成本與2026相近或更高。","ruling":"可調和：2027年的盈餘增量要靠既有產線的價格與出貨，西維吉尼亞在2027是成本項；2027 EPS高於2026的前提是鋼價維持，不是新廠。","evidence_level":"高：逐字稿","settle_metric":"2027年開辦與啟動成本、西維吉尼亞2027Q4稼動率","if_then":["若2027上半年啟動成本季增且稼動率低於計畫，則西維吉尼亞風險項啟動，中性情境2028年EPS下修"]},{"axis":"現在就買的最強論證（觀望方的自我攻擊）","cause":null,"prior_field":null,"side_a":"①資本支出由2024–2025高峰下降，前三季FCF約26.6億美元，2027再降，管理層稱FCF將大幅躍升並返還；②FY2027E本益比約13.3倍，2027合約折扣減少、附加價提高、合約比重高於往年的80–85%；③基建未撥款逾1,350億美元、電力業五年約1.4兆美元、資料中心占型鋼積壓訂單30–35%，需求延伸至2028。","side_b":"13.3倍乘在景氣高點附近的盈餘；FY2028E共識已低於2027；股價高於賣方平均目標；新產能與進口回升都落在2027–2029。","ruling":"反駁成立，維持觀望。約束條件只有一個：估值相對週期位置過高；重啟條件是它的否定，股價≤200美元且232與進口市占未破門檻。若FY2028E共識轉為高於FY2027E，代表週期判斷錯，另行重跑研究。","evidence_level":"中","settle_metric":"股價、FY2028E共識","if_then":["若股價≤200美元且政策與進口未破門檻，則重跑研究後首倉≤3%","若股價續漲而FY2028E共識未上修，則不追"],"evidence_refs":["end_markets#2","capital_markets_pricing#2"]},{"axis":"前份漂移：估值與訊號","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-25，股價232美元）：觀望偏進場，估值結論中性，等回測180–200美元分批。","side_b":"本次股價284.71美元（+22.7%）：FY1本益比14.49倍、EV/S與P/S位於4個年度端點最高，估值結論轉偏貴，訊號由B降為C，裁決改為觀望不追。","ruling":"主因是股價由232美元漲到284.71美元；同期盈餘共識上修只部分抵銷（FY1近3個月+6.45%）。前份等的回檔沒有出現，漲幅未達30%不需翻面理由，但前份的進場區間已被價格甩開。","evidence_level":"高","settle_metric":"股價與FY2028E共識","if_then":["若股價回到≤200美元且政策與進口未破門檻，則重跑研究"]},{"axis":"前份漂移：前份未產出的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄為空：未分類型、未給循環位置、未建情境機率與最大回撤。","side_b":"本次：護城河趨勢持平、五年後跑道中等、類型為循環/商品、循環位置為晚循環、情境機率樂觀20%／中性45%／悲觀35%、最大回撤−35%～−55%。","ruling":"屬方法補齊而非看法翻轉；前份以政策與資料中心敘事為主，本次改用商品循環鏡頭框定位置與回撤。","evidence_level":"中","settle_metric":"不適用"},{"axis":"前份漂移：價值陷阱判斷","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱風險中等。","side_b":"本次維持中等：亮2項（EPS成長遠高於營收、FCF/淨利2024–2025連2年低於0.75），但2026前三季FCF約26.6億美元，FCF/淨利回升至約0.8。","ruling":"結論不變；新證據是FCF轉正改善，若2026全年FCF/淨利≥0.75，下次降為1項。","evidence_level":"高：公司披露","settle_metric":"2026全年FCF/淨利"},{"axis":"行動門檻變動：重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重啟欄為空；裁決文字：等回測180–200美元（52週均線加布林中軌），或西維吉尼亞2027投產加232維持50%確認後分批。","side_b":"股價≤200美元，且232稅率維持50%、進口市占季度≤18%；達到後重跑研究、首倉≤3%。","ruling":"舊→新：價格錨由180–200美元區間改為≤200美元單一上緣，加上政策與進口兩項未破門檻；依據是中性情境5年值約270美元，自200美元起算年化約6%加股息約1%。前份的事件錨（西維吉尼亞投產）改列假設驗證，不再與價格錨並列，避免兩個理由混用。","evidence_level":"中","settle_metric":"股價、進口市占、232稅率"},{"axis":"行動門檻變動：清倉與減碼指標","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份：HRC連6週低於700美元/短噸或出貨年減5%連3月，連2季觸發即減倉1/3；新政府100天內降至25%砍倉30%、半年內廢除砍50%；4大雲端業者連2季下修資本支出指引>15%則大砍。","side_b":"本次清倉：232降至25%或以下或主要來源國豁免、進口市占連2季>20%；減碼三分之一：鋼廠稼動率連2季<80%、DRI和解>3億美元或停產、股價≥340美元且FY2028E共識未上修；雲端資本支出門檻保留，動作改為停止加碼。","ruling":"舊→新理由：①熱軋價已漲至約1,255美元，700美元門檻離現價逾四成，失去預警力，改用稼動率與CSP跌幅；②進口市占由約14%回升至約17%是新證據，升為清倉主指標；③2028大選的政策風險併入Single Thing，並提前到USMCA檢討；④雲端資本支出門檻原樣保留，但資料中心只占全公司積壓訂單約15%，動作由大砍降為停止加碼。","evidence_level":"中","settle_metric":"進口市占、稼動率、232稅率","evidence_refs":["competitive_share_entrants#3"]},{"axis":"行動門檻變動：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）。","side_b":"本次Single Thing：232鋼鐵關稅由50%調降至25%或以下，或對加拿大、墨西哥、南韓等主要來源國給予配額或豁免。","ruling":"前份把政策變動放在2028大選後的長期風險；本次改為唯一致命點，理由是它是盈餘對鋼價敏感度最大的單一離散事件，且USMCA檢討已在進行，觸發時點可能早於大選。發生即清倉。","evidence_level":"中","settle_metric":"白宮與商務部公告","evidence_refs":["reg_tariff_export#1"]}],"triggers":[{"n":1,"text":"進口市占守在18%以下","type":"假設驗證","maps_to":"H1","metric":"美國成品鋼進口市占","threshold":"季度≤18%；連2季>18%即削弱","action":"不追；連2季>18%則停止任何加碼","source_freq":"Nucor季度投資人簡報（每季）","date":"2027-01","evidence_refs":["competitive_share_entrants#3"]},{"n":2,"text":"西維吉尼亞爬坡進度","type":"假設驗證","maps_to":"H2","metric":"西維吉尼亞薄板廠稼動率","threshold":"2027Q4≥50%","action":"低於40%時H2列削弱，下修中性情境2028年後EPS","source_freq":"季度法說（每季）","date":"2028-01"},{"n":3,"text":"週期谷底上移","type":"假設驗證","maps_to":"H3","metric":"年度EPS與年度FCF","threshold":"下一谷底年度EPS≥8美元、FCF≥0","action":"若谷底EPS<8美元，週期中值下修，終端倍數降至14倍","source_freq":"年報（每年）","date":null},{"n":4,"text":"232稅率調降或主要來源國豁免","type":"Single Thing","maps_to":"Single Thing","metric":"232鋼鐵關稅稅率與豁免名單","threshold":"降至25%或以下，或加拿大、墨西哥、南韓等取得配額或豁免","action":"不建倉；持有者清倉","source_freq":"白宮與商務部公告（事件）","date":null,"evidence_refs":["reg_tariff_export#1"]},{"n":5,"text":"稼動率跌破80%","type":"減碼","maps_to":"R2","metric":"Nucor鋼廠產能利用率","threshold":"連2季<80%（2026Q3為89%）","action":"持有者減碼三分之一；未持有者把重啟價格下修至170美元","source_freq":"季度新聞稿（每季）","date":null,"evidence_refs":["supply_demand_durability#4","cyclical_supply_discipline_capacity#2"]},{"n":6,"text":"價格快速下調","type":"風險","maps_to":"R3","metric":"Nucor CSP與美國熱軋卷價格","threshold":"CSP 6週內累計下調≥15%，或熱軋卷價格自約1,255美元/短噸下跌≥15%","action":"停止加碼；股價若同步跌至重啟價格，仍需先確認進口市占≤18%","source_freq":"每週CSP公告、Fastmarkets","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"n":7,"text":"進口市占失守","type":"清倉","maps_to":"R1","metric":"美國成品鋼進口市占","threshold":"連2季>20%","action":"持有者清倉；未持有者不建倉","source_freq":"Nucor季度投資人簡報（每季）","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":8,"text":"資料中心需求放緩","type":"風險","maps_to":"R6","metric":"四大雲端業者資本支出指引","threshold":"連2季下修>15%","action":"停止加碼並下修樂觀情境機率","source_freq":"雲端業者季報（每季）","date":null},{"n":9,"text":"路易斯安那DRI廠清潔空氣法和解","type":"風險","maps_to":"R5","metric":"和解金額或改善要求","threshold":"金額>3億美元（約市值0.5%）或要求DRI停產改造","action":"重估原料成本與DRI自給率；持有者減碼三分之一","source_freq":"10-Q與10-K法律程序（每季）","date":null,"evidence_refs":["major_events#1"]},{"n":10,"text":"估值重啟","type":"估值rearm","maps_to":null,"metric":"股價","threshold":"≤200美元，且232稅率維持50%、進口市占季度≤18%","action":"重跑完整研究後首倉≤3%，分兩批","source_freq":"每日收盤","date":null},{"n":11,"text":"高位減碼","type":"減碼","maps_to":null,"metric":"股價與FY2028E共識","threshold":"股價≥340美元（約FY2027E共識16倍）且FY2028E共識未上修","action":"持有者減碼三分之一","source_freq":"每日收盤、共識快照（每月）","date":null},{"n":12,"text":"複審：Q4財報與2027計畫","type":"複審日期","maps_to":null,"metric":"2027資本支出、合約季結果、進口市占","threshold":"不適用（定期複審）","action":"重跑研究","source_freq":"一次性","date":"2027-01"}],"kill_metrics":[{"metric":"美國成品鋼進口市占","bear_threshold":"連2季>20%","window":"2026Q4–2028Q4（每季）","source":"Nucor季度投資人簡報、AISI","last_status":"ok"},{"metric":"232鋼鐵關稅稅率與豁免","bear_threshold":"降至25%或以下，或主要來源國取得配額或豁免","window":"2026-11至2029-01","source":"白宮與商務部公告","last_status":"ok"},{"metric":"Nucor鋼廠產能利用率","bear_threshold":"連2季<80%（2026Q3為89%）","window":"2027–2028（每季）","source":"Nucor季度新聞稿","last_status":"ok"},{"metric":"美國熱軋卷價格","bear_threshold":"自約1,255美元/短噸下跌≥20%（約<1,000美元）","window":"滾動6個月","source":"Fastmarkets、GMK Center、Nucor CSP週公告","last_status":"ok"},{"metric":"西維吉尼亞薄板廠稼動率","bear_threshold":"2027Q4<40%（目標50%）","window":"2027Q4","source":"Nucor季度法說","last_status":"unknown"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"證據出自2023年2月申報的FY2022年報，描述2022年停購俄國生鐵的一次性事件，已過時；現行原料外購風險由FY2025年報的原料條目涵蓋，並已列入原料成本風險，不重複計。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=26.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"≤3%（循環股、晚循環位置）","requires_critic":[],"rearm_trigger":"股價≤200美元，且232稅率維持50%、進口市占季度≤18%","exec_line":"觀望不追；達重啟條件先重跑研究，首倉≤3%分兩批；任一清倉條件發火則不建倉"},"reasoning":{"industry":"分部（Q3稅前）：鋼廠17.9億美元、鋼製品4.65億美元、原料1.05億美元，鋼廠段占八成以上，獲利由鋼價減廢鋼與原料成本的價差決定。Q3營收112.49億美元、推算營業利益率16.7%、EBITDA 22.79億美元，出貨7,533千短噸、外部均價1,493美元/短噸、稼動率89%；TTM毛利率15.94%、營業利益率11.89%，低於單季水準，代表盈餘仍在往上走。Q4指引與Q3持平到小幅高於。產業時鐘判III：熱軋價一年漲52%至2022年5月以來高點、鋼廠出貨連3季創紀錄，但進口市占已由約14%回升至約17%，北美新電爐產能2026–2029陸續投產，FY3共識EPS 19.95低於FY2的21.41，市場已預期2027年見頂。供需耐久性：週期性將反轉，供給可逆性高。議價權：客戶分散（最大客戶約5%），錢卡的節點是鋼價本身。單點依賴不在客戶而在政策，也就是232關稅。產業態勢裁決為雙向拉鋸，依據見反證紀錄。","moat":"機制是成本位置加產品廣度。可證方向：同業ROIC事實表未涵蓋，改用營業利益率對照，NUE 11.89%，高於STLD 10.66%（+1.2pp）、CMC 9.26%、CLF −1.41%；FCF利潤率3.81%高於STLD 2.54%、低於CMC 5.1%。領先幅度小，證明成本位置在前段，不足以證明定價力。執行力8分：出貨連3季創紀錄、西維吉尼亞與Berkeley專案準時且在預算內、取得GM整個汽車外板平台、塔架已通過逾30家電力公司認證；扣分在西維吉尼亞啟動成本2027仍偏高、2025年FCF為負。定價力6分：Nucor以CSP帶動國內薄板定價，2027合約折扣減少、附加價提高；但年報自承主要以價格與服務競爭，2016年Q1鋼廠均價曾年減27%，下行時是價格接受者。趨勢持平：執行面擴大、定價面縮減，五項威脅皆列點對點。報酬持續期四項檢查點都在中等，最弱一環是依賴232這項政策授權。","growth":"成長拆解：價為主、量為輔、回購加成，併購不是主力。共識三年EPS：FY2025A 7.52→FY2028E 19.95，年化38.4%（Koyfin，家數事實表未涵蓋）；但以FY1為錨，FY2026E 19.65→FY2028E 19.95年化僅0.8%，市場已預期2027見頂。內生上界約2–3%（再投資率約20%乘假設增量ROIC 10–15%），缺口約35pp歸因利潤率擴張（鋼價回升與關稅），屬週期而非複利，不外推。跑道：美國鋼需年增約2%，五年後的增量來自電爐從高爐廠搶汽車份額（目前汽車約10%，西維吉尼亞爬坡後年產約100萬噸汽車鋼）與下游擴張（塔架長期EBITDA約2億美元），沒有新的S曲線，判中等。衰退訊號亮2項，都與谷底基期有關。","governance":"現金轉換正在回升：FY2024 FCF/淨利約0.40、FY2025約−0.11（資本支出高峰），2026前三季FCF約26.6億美元；以前三季回饋約14億美元＝淨利42%回推前三季淨利約33億美元，FCF/淨利約0.8。資本支出2026年約25億美元、2027年再降。現金去向（前三季）：資本支出約19億美元、股利加回購約14億美元；淨負債34.53億美元、負債占資本23%、評等A-。SBC占稅前盈餘2.8%，股數由2022年約2.64億股降至2025年約2.32億股（淨利除以稀釋EPS推算），目前約2.27億股。弱點：6.5年部署約190億美元、約半數用於併購，併購增量報酬未揭露；管理層稱下一步現金主攻Expand Beyond，門檻是報酬接近資金成本兩倍，否則返還股東。","valuation":"FY1本益比14.49倍、FY2約13.3倍，乘在景氣高點附近的盈餘上；以2022–2026E五年平均EPS約16.5美元計，現價約17.3倍；trailing本益比18.13倍在4個年度端點中位於76.1分位，P/S 1.66倍與EV/S 1.75倍都在端點最高。賣方目標（7–8月）平均約254–283美元、最高297、最低190，現價已在平均之上，且這批目標早於Q3財報。FY1共識近3個月上修6.45%，但FY3仍低於FY2。循環位置判晚循環：商品循環訊號中供給紀律（新產能）與情緒（股價高於目標）偏賣，量價齊升與毛利率居中，P/B事實表未涵蓋；倍數在樣本高點，新建倉條件不成立。我不信現價隱含的盈餘持續性，判偏貴。","premortem":"依據集中在反證紀錄三視角，不重寫。衰退訊號亮2項（EPS成長遠高於營收、FCF/淨利連2年低於0.75），都和2024–2025谷底基期有關，2026前三季FCF/淨利已回升至約0.8。最大回撤推估−35%～−55%：現價對104週均線170.38美元為−40%、對250週均線155.30美元為−45%；前幾輪2024年EBITDA年減41%、2024Q2 EPS預告年減逾60%、2015年EPS僅0.25。"},"plain":{"six":{"how_it_makes_money":"賺美國營建、能源、資料中心與汽車用鋼的錢；錢卡在鋼價減廢鋼成本的價差，價差由進口管制與景氣決定，不由Nucor決定。","moat":"護城河方向持平：電爐成本位置與產品廣度的領先在擴大，定價力被進口回流與新產能壓住，兩者相抵；等級B。","growth":"五年後跑道中等：美國鋼需年增約2%，成長靠電爐從高爐廠搶汽車份額與下游擴張，沒有新的S曲線；共識三年高成長是谷底基期造成的。","capital":"資本配置穩健偏正面：資本支出高峰已過、FCF回升、股東回饋守住淨利40%下限；扣分在併購報酬未經驗證。","valuation":"現價要求2027年之後盈餘不像前幾輪那樣回落；我不信，2028年共識已先往下，估值偏貴。","how_wrong":"最可能看錯在把景氣高點盈餘當常態；價值陷阱風險中等。"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤200美元，且232稅率維持50%、進口市占季度≤18%","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":284.71,"week26_return_pct":26.69,"consensus_rev_3m_pct":6.45,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母是爭點：以FY2025A谷底EPS 7.52為基期，三年共識年化38.4%，PEG約0.38看似便宜；改以FY1 19.65為錨，到FY3 19.95年化僅0.8%，PEG約19。循環股高點盈餘不能當成長分母，便宜論證無效。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q4 2026 EPS指引（通常於季末前約兩週發布）","impact":"中","watch":"是否守住與Q3持平至小幅高於5.80美元"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4財報、2027資本配置計畫與合約季結果","impact":"高","watch":"2027資本支出降幅、合約量與價格條件、進口市占"},{"date":"2027-Q3","date_precision":"quarter","type":"regulatory","event":"USMCA年度檢討後續（2026年7月啟動）","impact":"高","watch":"是否要求北美熔煉澆鑄、加拿大與墨西哥是否取得232豁免"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"西維吉尼亞薄板廠稼動率目標50%","impact":"中","watch":"啟動成本與稼動率進度"},{"date":"2028-11","date_precision":"month","type":"macro","event":"美國總統大選","impact":"高","watch":"候選人對232的立場"}],"_projected_from":"v19"}
```
