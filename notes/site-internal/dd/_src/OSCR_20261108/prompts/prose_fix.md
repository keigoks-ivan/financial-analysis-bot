你是 stock-analyst v20 的**散文層（prose）agent**，標的 OSCR（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：OSCR　日期：2026-11-08　archetype：None　前份裁決：2026-05-18　觀察池 — C 級護城河 5.5 (execution 7 / pricing power 4) + ACA 補貼到期 binary 風險 + Pure MA 🟠 暫不（盲點 2 救援失效）+ 4 週 +66% 動能透支；等 2025-Q4 PTC 立法 + H2 MLR ≤84% 雙信號明朗化再評估｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1541B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（815B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（902B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1372B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1224B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（349B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（814B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2250B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3366B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2340B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1541           3821-5459      5 條（2–6 內）  
s3                  8000         815           5030-7185      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3498          8051-11502      5 條（2–6 內）  
s6                 11000         349          7456-10651      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         814           1880-2686      5 條（2–6 內）  
s10                 5000        2250           1925-2750      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2340           2000-2660      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4923B；至少需散文≈40.08KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65
−65%
−58%
−56%
−40%
−40
−38%
−1.69
−1.35
−1.1
−0.45
−0.4
0
0.14
0.3
0.35
0.43
0.43%
0.49
0.5
0.55
0.66
0.75
0.9
0.93
1%
1
1.1
1.2
1.25
1.26
1.3
1.36
1.46
1.50
1.5%
1.6
1.60
1.78
1.9
1.94
02
2%
2.0
2
2.22
2.25
2.35
2.45
2.5
2.5%
2.56
2.75
2.77
2.84
2.9
3
3%
3.20
3.2
3.46%
3.55
3.6
4
4.37
4.43
4.5%
4.5
4.6
4.7%
4.81
5
5%
05
5.4
6
06
6.1
6.2
6.3
7%
7
07
7.3
8
08
8%
8.4
8.5
9%
09
9
9.4%
9.5
9.5%
10
10%
11
11.4
12%
12
12.1
12.5
12.8
13
13.36
13.8
14.0%
14
14%
14.7
15
15%
15.1%
15.1
15.5%
15.6%
15.8
16
16%
16.5%
16.78
17
17%
17.5%
17.6
18%
19.03
19.9%
20%
20
21
21%
23
23.32
24
24.20
24.82
25
25%
25.3
25.5
26
27%
28
29%
30
30%
30.65
31%
31.4%
32%
32.9
34.8
35%
37%
37.46
37.6%
38.4
40%
40
42
43%
43.83
43.83%
45
48.9
49
50%
50
51.4
52
55.6%
58%
60
60%
69.8
70%
70
79.2%
80
80%
80.5%
80.5
81.5%
82
83%
84%
84.0%
85
85%
86%
88%
90
96.5%
99.2
100%
100
102
104
104.5%
122
150%
150
167.3
179
190
191.5
193
208
240
250
260
262
269
310.69
329.8
341
367
400
600
713
2021
2022
2023
2025
2026
2027
2028
2029
2030
2031
20261108
1,000
1,600
1,700
2,050
2,200
2,280
2,300
2,430
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
{"meta":{"ticker":"OSCR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Oscar Health, Inc."},"oneliner":"2026 獲利創新高，但全年營業利益近半來自前期項目。現價要靠 2027 利潤率站上 5% 才划算，等 2027 年 2 月財測與開年會員數驗證，不追。","thesis":{"H":[{"id":"H1","text":"2026 的利潤不是一次性：2027 在沒有大額前期利益下，營業利益率仍達 5%。","2y":"2027 全年營業利益率至少 5%，MLR 不高於 81.5%","5y":"三年滾動營業利益率至少 4.5%，期間沒有虧損年度","10y":null,"threshold":"2027 MLR 加 SG&A 率合計不高於 96.5%；風險調整結算不利不超過保費 1 個百分點","source":"公司季報與法說、CMS 風險調整報告、Wakely","drift_rule":"TTM 營業利益率低於門檻 5% 以上連 2 季削弱，低於 10% 以上連 3 季反轉"},{"id":"H2","text":"2027 在費率與對手相近時仍拿到份額，證明份額不是只靠對手撤退。","2y":"2027 第一季會員至少 260 萬，全國份額至少 15%","5y":"2029 全國份額接近 18%，現有區域達 35%","10y":null,"threshold":"2027 第一季會員至少 260 萬","source":"公司季報、CMS 投保資料、KFF","drift_rule":"會員數低於門檻 5% 以上連 2 季削弱，低於 10% 以上連 3 季反轉"},{"id":"H3","text":"固定成本攤提與 AI 讓 SG&A 率繼續下降，且不必靠提高佣金換成長。","2y":"2027 全年 SG&A 率不高於 15.1%","5y":"2029 年 SG&A 率低於 15%","10y":null,"threshold":"2027 全年 SG&A 率不高於 15.1%（2026 指引下緣）","source":"公司季報與法說","drift_rule":"TTM SG&A 率高於門檻 5% 以上連 2 季削弱，高於 10% 以上連 3 季反轉"}],"R":[{"id":"R1","text":"風險調整或罹病率估計反轉，2026 的利多回吐。","h_ref":"H1","clock":"⚡","threshold":"單次估計變動不利至少 2.5 億美元，或全年 MLR 指引高於 83%","evidence_refs":["end_markets#1"]},{"id":"R2","text":"聯邦補貼與資格審查繼續壓縮市場，留下的人風險更高。","h_ref":"H1","clock":"🔥","threshold":"全國有效投保人數低於 1,600 萬，或 Wakely 資料否定 2027 定價的罹病率假設","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","regulatory_antitrust#2","end_markets#1"]},{"id":"R3","text":"對手回補或低價搶市，份額增加無法維持。","h_ref":"H2","clock":"🔥","threshold":"2027 第一季會員低於 240 萬","evidence_refs":["end_markets#1"]},{"id":"R4","text":"藥品關稅與回扣下降推高醫療成本，超出定價假設。","h_ref":"H1","clock":"🔥","threshold":"全年 MLR 超過指引上緣 1 個百分點，且管理層點名藥費或回扣","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R5","text":"DOJ、HHS-OIG 持續審查詐欺與濫用，包括遠距醫療的給付做法。","h_ref":"H1","clock":"🐢","threshold":"收到具名調查或和解金額超過 1 億美元","evidence_refs":["regulatory_antitrust#0"]}],"single_thing":{"description":"CMS 在 2027 年年中公布的 2026 年度風險調整結算，與公司帳上應計相比不利超過保費 2 個百分點（約 4.6 億美元，自算：全年營收中點÷(1−17.5%)×2%）。","why_fatal":"本次法說把風險調整占保費比一次改了 2–3 個百分點，這是損益表最大的估計項。2 個百分點約每股 1.36 美元，超過 2027 共識 2.22 美元的一半；會員少 10% 只影響約 1 億美元營業利益，敏感度差四到五倍。","if_happens":"2027 財測下修，當年營業利益率回到 3% 以下，Bear 路徑成立，五年目標約 12.8 美元。持有者清倉，未持有者移出觀察名單。","how_monitor":"每季風險調整占保費比、Wakely 報告（本次只到 7 月資料）、2027 年第二季財報揭露的結算差額。","probability":"約 20%（12–24 個月）。2026 的結算方向目前有利，但 Wakely 的有利程度已由「相當有利」降到「溫和有利」，且公司 2025 年才虧損 4.43 億美元。"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.8,"peg_fy2":0.66,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-1.69,"FY2026E":1.94,"FY2027E":2.22,"FY2028E":2.84},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；2025 為 yfinance 年報，2026–2028 為 Koyfin 共識（2026-11-07 快照，家數事實表未涵蓋，看來尚未反映 11-05 上修）。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/scenario.json","archetype":{"primary":"金融","secondary":"未獲利高成長","confidence":"中","fingerprint":"ACA 健保承保商，損益由損失率與風險調整決定；2025 年仍虧損，2026 才大幅轉盈。"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高。Cigna、Aetna 與 UnitedHealthcare（喬治亞）退出帶來份額，Centene、AmeriHealth Caritas 同時加縣市（Fierce Healthcare、Healthcare Dive、Becker's，2026-10）。階段判為擴張：承保利潤率由 2025 年虧損回到 2026 指引約 4.7%，2027 費率加 14% 並放入利潤擴張，但人數仍在縮。","bargaining":{"up":"上游議價弱：部分市場醫院與醫師團體接近獨占，藥局理賠委外 CVS/Caremark。","down":"下游議價中等：會員每年比價，經紀人是主要通路，佣金不必最高但要有競爭力。","geo":"只在美國營運，事實表未見地緣暴露。"},"profit_pool_dir":"短期由退出的大型保險商流向留下的 ACA 業者；五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"ACA 全國投保人數","value":"2025 年 2,430 萬 → 2026 開放投保 2,280 萬 → 2026-06 約 2,050 萬（KFF）→ 2026 年底約 1,700 萬（CFO，2027 大致不變）→ 2029 約 2,300 萬（CEO 預估）"},{"item":"Oscar 可服務市場","value":"2027 年 21 州 713 個縣，約 1,000 萬人（CEO，2026-11-05）"},{"item":"Oscar 份額","value":"現有區域由 2025 年 17% 到 2026 年 30%，目標 35%；全國目標 2029 年 18%；以年底 250 萬會員÷1,700 萬計，現約 15%（自算）"},{"item":"第二曲線","value":"CHOICE 2026 約 50 萬人，CEO 預估 2029 年 250 萬；Lucie 未納入財務目標"},{"item":"分段 CAGR 與五年營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"ACA 原生窄網絡、經紀人工具與單一資料平台形成的成本與通路優勢，不是客戶鎖定。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：自報區域份額由 17% 升到 30%，SG&A 率創新低。定價權穩定：2027 調幅與全國平均相當，CFO 說價格必須在最低價的合理範圍內。份額是單一年度、公司自報，又發生在對手退出的年份。2027 開放投保若在費率相近下仍拿到份額，才上調。","peer_na_reason":"事實表沒有投入資本與同業 ROIC，OSCR 的營業利益率在同業表也是空值，ROIC 利差無法計算，改用份額做方向證據。","threats":[{"level":"🟡","text":"對手回補與低價：Centene、AmeriHealth Caritas 2027 加縣市，UBS 分析師在法說指出有對手以最低價進場。","p":"35%","evidence_refs":["end_markets#1","competitive_share_entrants#2"]},{"level":"🟡","text":"上游議價：部分市場的醫院或醫師團體接近獨占，窄網絡的談判力受限。","p":"30%","evidence_refs":["regulatory_antitrust#1"]},{"level":"🟡","text":"技術沒有專利保護，關鍵人員流失會干擾營運，AI 帶來的成本優勢對手可以追上。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"外包依賴：藥局理賠與網絡委外單一 PBM（2021 年 10-K 揭露，近年是否變動事實表未涵蓋），多數通訊與軟硬體由第三方營運。","p":"15%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是會員，決定者多半是經紀人加會員，付款方大半是聯邦補貼。保險需求成立，但付款方一退人數就掉：市場由 2,430 萬縮到 2026 年底約 1,700 萬。"},{"item":"決策層級","level":"🟡","text":"每年重選一次，轉換成本低，經紀人用比價平台。留存較佳的說法沒有數字。2026 費率上調後會員仍年增 27%，顯示相對價格比絕對價格重要，這是競爭力，不是鎖定。"},{"item":"價值鏈分配","level":"🟡","text":"醫院與醫師團體在部分市場接近獨占，藥局理賠委外，經紀人拿佣金。管理層把 MLR 目標放在接近 80%，再扣約 15% 行政費。2029 年 5–7% 利潤率目標已高於其自述的歷史區間 3–5%。"},{"item":"社會容忍度","level":"🔴","text":"定價上限由政治決定：2027 提案保費中位數漲約 15%，Oscar 喬治亞州申請約 29%，補貼仍在國會爭議中，CEO 於 2026-11-05 表示對 2027–28 恢復補貼不抱太大期待，公司也預期持續受 DOJ 與 HHS-OIG 審查。"}],"roiic":25,"reinvest_rate":60,"endo_ceiling":15,"formula_note":"當期 ROIC：2026 指引中點營業利益 9 億美元，稅率按個位數中段，投入資本用保險子公司資本 23 億加母公司現金 3.6 億，約 32%；扣掉前期項目 4.37 億（2025 風險調整結算 1.6 億＋前期準備金有利發展 2.77 億）約 16.5%。保險業沒有常規投入資本口徑，此為近似。增量報酬：2026 淨利約 8.4 億（9 億×九個月淨利對營業利益比 0.93），2029 目標 EPS 4 美元×約 367 百萬股（341 百萬每年增 2.5%）＝14.7 億，增量 6.3 億，除以留存資本 25.5 億（計畫資本 40–45 億中點×60%）≈25%。內生上限 25%×60%＝15%；資本配置若評為最低級，再打八折為 12%。數字由管理層目標推出，是上限，不是實績。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","OSCR":null,"CNC":7.78,"MOH":7.97,"ELV":null,"CLOV":19.53,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","OSCR":null,"CNC":0.75,"MOH":0.6,"ELV":null,"CLOV":0.3,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","OSCR":43.41,"CNC":1.93,"MOH":0.54,"ELV":3.23,"CLOV":3.17,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"CNC","gm":7.78,"om":0.75,"fcf_margin":1.93,"strategy_note":"2027 反向加縣市，是份額爭奪的主要對手；TTM 利潤率偏低，用價格換量的空間要看其他業務能否支撐，事實表未涵蓋分部資料。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"MOH","gm":7.97,"om":0.6,"fcf_margin":0.54,"strategy_note":"同業表只有利潤率，事實表沒有其 ACA 布局，無法判斷對 Oscar 的直接壓力。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ELV","gm":null,"om":null,"fcf_margin":3.23,"strategy_note":"同業表只有 FCF 利潤率，營業利益率空缺，事實表未涵蓋其重疊市場。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CLOV","gm":19.53,"om":0.3,"fcf_margin":3.17,"strategy_note":"事實表未涵蓋其與 Oscar 的業務重疊，不視為直接競爭證據。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"價大於量；併購與回購不是成長來源。","runway_years":"約 6 年（全國份額口徑；現有區域已約 30%）","runway_post_y5":"🟡","endo_ceiling_basis":"見護城河段推導：增量報酬約 25%×留存率 60%≈15%，來自管理層 2029 目標與資本規劃。","segments":{"expanded":false,"reason":"公司只揭露單一保險業務，Lucie 與 CHOICE 沒有營收數字，分部三年成長事實表未涵蓋。"},"decay_signals":["EPS 成長顯著高於營收成長：2026→2028 共識 EPS 年增約 21%，2027 共識營收僅增約 9.5%，差距超過 5 個百分點。","TAM 萎縮：ACA 人數由 2,430 萬降到 2026 年底約 1,700 萬。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，公司沒有配息與回購，近三年現金去向與併購金額事實表未涵蓋。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2025 年收購 Lucie、IHC Specialty Benefits，金額與報酬事實表未涵蓋；近 12 個月無併購 8-K。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未見回購；上繳母公司資金的用途是併購與管理稀釋。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"管理層指引稀釋股數年增 2–3%，高於 1.5%；聚合站顯示 2021–2025 稀釋股數由 179 百萬增到 262 百萬，口徑未核對財報。","grade":"不過"}]},"valuation":{"basis":"Forward P/E（2026 共識 EPS），P/TBV 因事實表沒有帳面淨值而無法使用。","tier":"單一 ACA 業務、獲利波動大的健保承保商","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比，無從比較，列為資料缺口。"},"fwd_pe":15.8,"peg":0.75,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"2026 為 15.8 倍、2027 為 13.8 倍，PEG 0.75（2026→2028 共識 CAGR 21%），表面便宜；但分母有爭議，便宜論證不成立，所以看成中性。五年分位無法計算：本益比只有 1 個年度端點，P/S 在 4 個年度端點中最高，EV/S 位於 69.8 分位。短期空間以 2027 Base EPS 2.35×14 倍＝32.9 美元計；中期以 2029 Base EPS 3.20×12 倍＝38.4 美元計。","upside_short_pct":7.3,"upside_mid_pct":25.3},"trap_analysis":{"verdict":"🟡","label":"獲利品質待驗，市場人數仍在縮"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"前九個月營業利益 13 億美元，其中 4.37 億屬前期項目；第三季另有 2.5 億風險調整更新。Piper 估第三季每人醫療支出年增 19.9%，CFO 說會員月數有扭曲，但沒有給自己的數字。2025 全年虧損 4.43 億美元。","assumption":"2026 的罹病率與風險調整應計都準確，2027 的 14% 調幅足以涵蓋高個位數趨勢與罹病率上升，還留有利潤擴張。","consequence":"2027 MLR 多 2 個百分點，EPS 少約 1.1 美元；Bear 五年後 12.8 美元，較現價跌約 58%。","ruling":"採納。Bear 機率訂 30%，這是不追的主因。","watch":"第四季 MLR、2027 財測、2027 年中風險調整結算。","evidence_refs":["end_markets#1"],"fact_refs":["f_kpi8_fy2026_guidance","f_kpi0_total_revenue_gaap"]},{"view":"論點失敗","evidence":"社會容忍度是最弱一環。聯邦補貼是主要付款方，2022 年約 85% 會員領補貼。增強補貼 2025 年底到期，CMS 資格審查還在繼續，CEO 於 11-05 表示對 2027–28 恢復補貼不抱太大期待。公司也受 DOJ、HHS-OIG 的詐欺與濫用法規審查。","assumption":"2027 市場人數與 2026 年底相當，且調幅已涵蓋資格審查造成的風險池惡化。","consequence":"若市場再縮 15% 且留下者風險更高，營收與 MLR 兩邊同時受壓，2028 接近損益兩平（Bear 路徑 0.35 美元）。","ruling":"採納。但前份最擔心的補貼到期已經發生，公司挺過來了；這條風險由單一事件改為逐年的政策侵蝕。","watch":"CMS 投保人數、2028 年規則、兩黨補貼協商。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","regulatory_antitrust#0","regulatory_antitrust#2"],"fact_refs":["f_kpi7_effectuated_membership"]},{"view":"論點成功但股東經濟變差","evidence":"CFO 於投資人日指引稀釋股數每年增 2–3%，計畫期間資本約 60% 留在保險子公司。聚合站顯示稀釋股數 2021–2025 由 179 百萬增到 262 百萬，2026 第一季 329.8 百萬，口徑未核對。可轉債已在價內。2027 稅率仍是個位數中段，假設回到 20%，EPS 少約 16%。","assumption":"營收與份額目標達成，利潤就會全部歸股東。","consequence":"即使 2029 年 EPS 達 4 美元，新增資本也只有約四成回到母公司，倍數難以上升。","ruling":"採納。Base 終端倍數設 12 倍，低於現值，報酬只來自盈餘成長。","watch":"稀釋股數年增率、母公司現金、有效稅率。","evidence_refs":["unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#1"],"fact_refs":["f_shares_diluted_m","f_kpi6_sbc"]},{"view":"價格已反映太多","evidence":"前份以來股價漲 31%，26 週漲 43.83%，高於 52 週均線 37.6%，P/S 在 4 個年度端點中最高。看似便宜的 EV/S 與 FCF 利潤率都受浮存金影響：第三季付掉 2025 年風險調整應付款後，現金與投資由 102 億降到約 90 億美元。","assumption":"市場用的是約 2.0–2.5 美元的可持續 EPS。","consequence":"若底層 EPS 其實是扣前期項目後的約 1.26 美元，現價約 24 倍。","ruling":"部分採納。2027 的 13.8 倍本身不貴，但分母有爭議，便宜論證不成立，估值只算中性。","watch":"2027 財測的營業利益率與稅率。","fact_refs":["f_week26_return_pct","f_ps_percentile","f_ma_w52","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"管理層有多次沒有正面回答：2026-08-06 沒答 CMS 百萬名單中有多少是 Oscar 會員，也未確認剔除前期項目後的第二季 MLR；2026-09-16 未拆解 MLR 改善 150bp，SG&A 降到 15% 以下只答規模與 AI，未回應 CHOICE 的立法風險，也未給流失者與留存者的 MLR 差異。","assumption":"這些沒講的數字不會改變結論。","consequence":"風險池變化與成本改善的拆解都拿不到，只能靠財報結果反推。","ruling":"採納，列為資料缺口；在 2027 財測前不採信利潤率擴張的拆解。","watch":"2027 年 2 月財報是否揭露費用與 MLR 的拆解。"}],"max_dd":{"lo":-65,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 23.32 → 本次 30.65（+31.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=23.32","side_b":"本次 price_at_dd=30.65","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 23.32 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 23.32 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 23.32 美元：Bull 價 99.2、Bear 價 12.8，五年期望值 +104.5%，基準年化 15.5%，不對稱比 4.81","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 4.81。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 23.32 美元：五年期望值 +104.5%，基準年化 15.5%，不對稱比 4.81","side_b":"本次情境、股價 30.65 美元：五年期望值 +55.6%，基準年化 9.4%，不對稱比 2.56","ruling":"再換股價、情境不動：起點價上漲 31.4%，五年期望值少 48.9 個百分點，基準年化少 6.1 個百分點，不對稱比由 4.81 降到 2.56。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2026 獲利是結構改善，還是估計有利","cause":null,"prior_field":null,"side_a":"CEO 與 CFO（2026-11-05）：改善主要來自定價紀律、費用控管與 AI，風險調整是業務的一部分，不該剔除。","side_b":"全年營業利益中點 9 億美元，其中 4.37 億屬前期項目；第三季另有 2.5 億風險調整更新，全年風險調整占保費比一次改了 2–3 個百分點。","ruling":"兩邊是程度差異，可以調和。定價改善是真的，但不把 2026 當常態，Base 的 2027 營業利益率略低於 5%。管理層的歸因標為未證、持續監測。","evidence_level":"高，公司揭露數字；前期項目合計為自算","settle_metric":"2026 年度風險調整結算差額、2027 全年營業利益率","if_then":["如果結算差額不利不超過保費 1 個百分點，且 2027 營業利益率指引維持 5% 以上，重做完整研究後首筆建倉不超過組合 2%。","如果不利超過保費 2 個百分點，或 2027 指引低於 3%，清倉並移出觀察名單。","反向：如果 2027 連續兩季前期項目歸零、營業利益率仍達 5%，改認定為結構改善，上調 Base。"],"evidence_refs":["end_markets#0","unprofitable_path_to_profitability#0"]},{"axis":"風險調整利多與 MLR 上修對不上","cause":null,"prior_field":null,"side_a":"Wells Fargo 分析師（2026-11-05）：風險調整應付比例下修 2–3 個百分點，全年 MLR 只改善 0.5 個百分點；Piper 分析師估第三季每人醫療支出年增 19.9%。","side_b":"CFO（2026-11-05）：部分風險調整利益被相應的理賠抵銷，Wakely 資料只到 7 月，指引保留了罹病率空間。","ruling":"不採信也不否定。若差額是保守，第四季會超指引；若是真實理賠，底層成本比「溫和有利」的說法差。","evidence_level":"中，分析師估算與管理層口頭說明","settle_metric":"第四季實際 MLR 是否落在九成出頭，2026 全年 MLR 是否不高於 81.5%","if_then":["如果 2026 全年 MLR 高於 81.5%，管理層保守的說法證偽，不追，Bear 機率上調到 35%。","反向：如果全年 MLR 低於 80.5%，保守的說法成立，Bear 機率維持 30% 並等 2027 財測。"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-09-16 投資人日，CEO：開放投保已有 80 萬張保單；CFO：母公司現金 4.6 億美元；同場 NPS 產業平均一說 12，一說 0。","side_b":"2026-11-05 法說，CEO：Lucie 有望在 2027 年賣出約 80 萬張新保單；CFO：母公司現金與投資 3.6 億美元。財測方面，全年營業利益指引由 5–7 億、6–8 億上修到 8.5–9.5 億。","ruling":"「已有」變成「有望」，用語降了一級，Lucie 與 NPS 都不計入 Base。母公司現金少 1 億美元沒有解釋，事實表未涵蓋。財測上修顯示指引偏保守，這點給予肯定。","evidence_level":"中，逐字稿比對","settle_metric":"2027 年 2 月揭露的 Lucie 保單數與母公司現金","if_then":["如果 Lucie 保單數低於 80 萬，Bull 機率由 20% 下修到 15%，差額加到 Base。"]},{"axis":"賣方對 2027 的分歧","cause":null,"prior_field":null,"side_a":"UBS（聚合站轉述）評賣出：2027 營收 122 億美元、EPS 1.25 美元，並稱共識 1.46 美元。","side_b":"Koyfin 共識 2027 EPS 2.22 美元、yfinance 共識營收 208 億美元；管理層說 2027 EPS 超過 2.25 美元。目標價由 11 美元到 Barclays 49 美元，三個聚合站均值 16.78–24.20 美元。","ruling":"UBS 的 122 億營收與全年指引 190 億差距過大，1.46 美元共識也對不上，只取方向，並把 1.25 美元當 Bear 第一年的參考。目標價全距 4.5 倍且日期分散，不用來支持裁決，只下調信心。分歧屬框架層：2026 是常態還是高點。","evidence_level":"低，聚合站轉述，未核原文","settle_metric":"2027 年 2 月公司財測","if_then":["如果 2027 EPS 指引低於 1.50 美元，採信 UBS 的框架，不追並把 Bear 機率上調到 40%。"],"evidence_refs":["end_markets#1","capital_markets_pricing#2"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭面：Cigna、Aetna 退出，UnitedHealthcare 2027 退出喬治亞，約 85 萬人重新進入市場；另一方面 Centene、AmeriHealth Caritas 加縣市。","side_b":"結構面：補貼到期、資格審查延續，市場人數減少，留下者風險較高；ICHRA 經紀人採用度由 15% 升到 37%，但調查由 Oscar 贊助。","ruling":"雙向拉鋸。對留下的業者，競爭在短期轉好；對整個市場，法規與補貼仍在縮小分母。","evidence_level":"中，產業媒體與公司說法","settle_metric":"2027 全國有效投保人數與對手的 2028 縣市布局","if_then":["如果全國有效投保人數低於 1,600 萬，改判為法規結構惡化，不追。"],"evidence_refs":["competitive_share_entrants#2","customer_concentration_credit#1","channel_business_model_shift#1"]},{"axis":"現在就買的最強論證，以及前份觀察以來股價漲 31% 為何仍不追","cause":null,"prior_field":null,"side_a":"現在就買：補貼到期這個最大風險已過，指引連三次上修，2027 倍數 13.8 倍，管理層承諾 2027 EPS 超過 2.25 美元、2029 年至少 4 美元，對手退出放出約 85 萬人，RSI 45 沒有過熱，等到 2 月可能已經漲上去。","side_b":"2027 倍數用的是未經驗證的預期，2026 利潤近半來自前期項目，開放投保在法說時只過了 4–5 天；2 月就有第一份驗證，等待的成本有限。","ruling":"選不追。翻面的部分是評級上調一級，因為前份的補貼風險已經過去；進場沒有翻面，因為 Base 年化報酬約 9%，不足以補償 30% 機率、約 58% 的跌幅。束縛條件只有一個：2027 利潤率能否站住。","evidence_level":"中，情境推算","settle_metric":"2027 年 2 月財測與開年會員","if_then":["如果股價先漲、財測還沒出來，不追。","如果股價下跌但重啟條件成立，分批反買；條件未成立前不動作。","反向：如果 2027 營業利益率指引低於 3%，清倉。"]},{"axis":"評級、估值與價值陷阱的變動","cause":"新證據","prior_field":["signal","val","trap"],"side_a":"前份：評級 C、估值中性、價值陷阱中等，論點卡在補貼立法。","side_b":"本次：評級 B、估值中性、價值陷阱中等。補貼已到期，公司三度上修，2026 指引營業利益 8.5–9.5 億美元。","ruling":"評級上調一級：前份最怕的事發生了，結果是公司賺錢。估值維持中性：股價上漲，盈餘預期也上升，但分母仍有爭議。價值陷阱維持中等：亮燈的是市場萎縮與 EPS 成長高於營收成長。","evidence_level":"高，公司財報","settle_metric":"2027 財測","if_then":["如果 2027 財測達標，維持目前評級並重新研究；如果低於 3%，評級下調並清倉。"]},{"axis":"前份留空的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這幾項都沒有填。","side_b":"本次填入：護城河趨勢穩定、五年後跑道中等、類型為金融、循環位置中循環，最大回撤區間 −65%～−40%，Bull 20%、Bear 30%。","ruling":"前份沒有基準可比，差異來自填寫方式，不是基本面變化。","evidence_level":"不適用","settle_metric":"無","if_then":[]},{"axis":"行動門檻更新：重新研究、減碼、清倉","cause":"新證據","prior_field":["rearm_trigger","kill_metrics"],"side_a":"等 2025-Q4 PTC 立法 + H2 MLR ≤84% 雙信號明朗化再評估；前份 MLR 警戒為任一季 MLR > 86% 削弱，> 88% 反轉；重啟條件與停損指標欄位未設。","side_b":"2027 年 2 月財報同時達到 2027 營業利益率指引至少 5%、開年會員至少 260 萬、2026 全年 MLR 不高於 81.5% 才重新研究；全年 MLR 指引高於 83% 減碼；2027 營業利益率指引低於 3% 清倉。","ruling":"舊門檻失效：補貼立法已有結果。單季 MLR 季節性很強（第二季 79.2%、第三季 84.0%、第四季隱含九成出頭），單季門檻會誤判，改看全年。","evidence_level":"高，公司財報與法說","settle_metric":"2027 年 2 月財報","if_then":["如果三項都達到，重新研究；任一項未達，繼續不追。"]},{"axis":"Single Thing 由補貼立法改為風險調整結算","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（欄位為空），當時最大風險是 2025 Q4 增強補貼立法失敗。","side_b":"CMS 在 2027 年年中公布的 2026 年度風險調整結算，與帳上應計相比不利超過保費 2 個百分點。","ruling":"補貼到期已經發生，不再是未來的二元事件。按敏感度排序，風險調整 2 個百分點約每股 1.36 美元，會員少 10% 只影響約每股 0.3 美元，前者才是最大單項。","evidence_level":"中，敏感度為自算","settle_metric":"2027 年第二季財報揭露的結算差額","if_then":["如果差額不利超過保費 2 個百分點，清倉。"]},{"axis":"前份假設的驗證結果","cause":"新證據","prior_field":["H1","R1"],"side_a":"前份 H1 門檻為 ACA 人數至少 2,200 萬、Oscar 份額 8–12%；R1 為補貼立法失敗即觸發。","side_b":"補貼確實到期，市場預計 2026 年底約 1,700 萬；但 Oscar 會員年增 27%，全年 MLR 指引 80.5–81.5%，SG&A 率 15.1–15.6%，前份 H2、H3 的門檻都已達到。","ruling":"前份把人數當成獲利前提，這點看錯了：人數掉下來時，定對價的業者反而賺得更多。新 H1 改看利潤率。","evidence_level":"高，公司財報與法說","settle_metric":"2027 全年營業利益率","if_then":["如果 2027 利潤率低於 3%，代表 2026 只是一年的定價紅利，回到前份的謹慎立場並清倉。"]}],"triggers":[{"n":1,"text":"2027 年 2 月財報的 2027 財測、開年會員與 2026 全年 MLR 同時達標","type":"估值rearm","maps_to":"H1","metric":"2027 營業利益率指引、開年會員、2026 全年 MLR","threshold":"至少 5%、至少 260 萬、不高於 81.5%，三項都要","action":"三項全過才重做完整研究，通過後首筆不超過組合 2%","source_freq":"季度財報","date":"2027-02"},{"n":2,"text":"CMS 公布 2026 年度風險調整結算，不利超過保費 2 個百分點","type":"Single Thing","maps_to":"Single Thing","metric":"結算差額占保費比","threshold":"不利超過 2 個百分點（約 4.6 億美元，自算）","action":"清倉並移出觀察名單","source_freq":"一年一次，第二季財報揭露","date":"2027-08"},{"n":3,"text":"2027 第一季有效會員驗證份額論點","type":"假設驗證","maps_to":"H2","metric":"季末有效會員","threshold":"至少 260 萬過關，低於 240 萬削弱","action":"低於 240 萬則不進場，已持有者減碼一半","source_freq":"季度新聞稿","date":"2027-05"},{"n":4,"text":"2027 全年 SG&A 率驗證費用論點","type":"假設驗證","maps_to":"H3","metric":"全年 SG&A 率","threshold":"不高於 15.1% 過關，高於 15.6% 削弱","action":"高於 15.6% 則停止加碼","source_freq":"年度財報","date":"2028-02"},{"n":5,"text":"ACA 全國投保人數再度明顯萎縮","type":"風險","maps_to":"R2","metric":"全國有效投保人數","threshold":"低於 1,600 萬","action":"不追，已持有者減碼一半","source_freq":"CMS、KFF 不定期","date":"2027-12","evidence_refs":["customer_concentration_credit#1","regulatory_antitrust#2"]},{"n":6,"text":"關稅或藥品回扣下降未被定價吸收","type":"風險","maps_to":"R4","metric":"全年 MLR 對指引上緣，且管理層點名藥費或回扣","threshold":"超過指引上緣 1 個百分點","action":"減碼一半","source_freq":"季度財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"n":7,"text":"2027 全年 MLR 指引明顯惡化","type":"減碼","maps_to":"R1","metric":"全年 MLR 指引","threshold":"高於 83%","action":"已持有者減碼一半，未持有者不追","source_freq":"季度財報","date":"2027-08"},{"n":8,"text":"2027 營業利益率指引跌破 3%","type":"清倉","maps_to":"H1","metric":"全年營業利益率指引","threshold":"低於 3%","action":"清倉","source_freq":"季度財報","date":"2027-02"},{"n":9,"text":"第四季財報後完整複審","type":"複審日期","maps_to":"H1","metric":"2027 財測與開放投保結果","threshold":"無","action":"財報公布後一週內重做完整研究","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"2027 全年 MLR 指引","bear_threshold":"高於 83%","window":"2027 年 2 月起每季","source":"公司財報與法說","last_status":"unknown"},{"metric":"2027 全年營業利益率指引","bear_threshold":"低於 3%","window":"2027 年 2 月起每季","source":"公司財報與法說","last_status":"unknown"},{"metric":"2026 年度風險調整結算與帳上應計差額","bear_threshold":"不利超過保費 2 個百分點","window":"2027 年第二季財報","source":"CMS 報告、公司 10-Q","last_status":"unknown"},{"metric":"季末有效會員","bear_threshold":"2027 第一季低於 240 萬","window":"2027 年第一季","source":"公司新聞稿","last_status":"unknown"},{"metric":"ACA 全國有效投保人數","bear_threshold":"低於 1,600 萬","window":"2027 全年","source":"CMS、KFF","last_status":"unknown"},{"metric":"2026 全年 MLR","bear_threshold":"高於 81.5%（指引上緣）","window":"2027 年 2 月","source":"公司財報","last_status":"unknown"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=43.83, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"2027 年 2 月財報同時達到：2027 營業利益率指引至少 5%、開年會員至少 260 萬、2026 全年 MLR 不高於 81.5%","exec_line":"未持有：2027 年 2 月財報前不建倉，條件成立後重做完整研究，通過後首筆不超過組合 2%。已持有：不加碼；全年 MLR 指引高於 83% 減碼一半；2027 營業利益率指引低於 3% 清倉。"},"reasoning":{"industry":"Oscar 幾乎只有一條業務線：賣 ACA 個人健康險，收保費，付醫療支出與行政費。2026 第三季營收 51.4 億美元、營業利益 1.78 億（利益率 3.46%）、MLR 84.0%、SG&A 14.0%，季末會員 269 萬，年增 27%。保險業沒有毛利率口徑，這裡用 MLR 代替；分部營收事實表未涵蓋。全年指引營收 190–193 億、MLR 80.5–81.5%、營業利益 8.5–9.5 億。單點依賴有三個：聯邦補貼是主要付款方（最新可查的 2022 年約 85% 會員領補貼，近年比例事實表未涵蓋）；經紀人通路帶來絕大多數會員；CMS 風險調整全年約占保費 17–18%，是損益表最大的估計項。供需持久性判斷為供給可逆性高：對手退出有利，但也有對手同時加縣市，利潤回來後供給可以回來。","moat":"機制是成本與通路，不是客戶鎖定：為 ACA 建的窄網絡、經紀人工具與單一資料平台。同業 ROIC 利差算不出來，方向只能用份額證明。自報區域份額 17%→30%，第三季 SG&A 率 14.0% 創新低，2027 調幅 14% 對競爭者平均 15%，執行力評 7、定價權評 5，保險業以綜合判斷給分。報酬屬低利益率高周轉：2026 ROIC 約 32%，扣掉前期項目約 16.5%，兩者的差距就是爭議所在。TTM FCF 利潤率 43% 是應付風險調整累積的浮存金，不能和同業比。持續期最弱一環是社會容忍度。新增資本報酬約 25%，內生成長上限約 15%，都用管理層目標推算。AI 降費是真的，但對手也做得到，公司也沒有申請專利。","growth":"成長主要靠價，其次靠量：第三季營收年增約 70%，會員年增 27%。2027 費率約加 14%，市場人數預期與 2026 年底相當。共識 EPS 2026–2028 為 1.94、2.22、2.84 美元；基期 2025 虧損，三年 CAGR 無法計算，以 2026→2028 兩年計約 21%。若改用指引推估的 2026 EPS 2.45 美元，只剩約 8%。內生上限約 15%，缺口約 6 個百分點，歸因於利潤率擴張（由約 4.7% 到 2029 年目標 5–7%）。全國份額約 15%，現有區域約 30%，目標 35%，每年擴 400–600 縣，到第五年後現有區域已達成熟水準。CHOICE 與 Lucie 是第二曲線的候選，但 CEO 說 Lucie 未進數字、CHOICE 放進的也有限，因此不計入。","governance":"前九個月 FCF 34.8 億美元，約為淨利 12.1 億的 2.9 倍，但主要是應付風險調整的時間差：第三季付掉 2025 年應付款後，現金與投資由 102 億降到約 90 億。真正可動用的是母公司現金與投資 3.6 億，加子公司超額資本 14 億。第三季 SBC 只占營收 0.43%，但管理層指引稀釋股數每年增 2–3%，超過每年 1.5% 的標準。2030 年到期的 3.55 億美元可轉債轉換價 24.82 美元已在價內，capped call 上限 37.46 美元。投資人日規劃 40–45 億美元資本，約 60% 留在子公司，其餘用於併購與管理稀釋。近三年現金去向四分事實表未涵蓋。","valuation":"現價 30.65 美元，對 2026 共識 15.8 倍，對 2027 共識 13.8 倍；以 12–15 倍計，現價對應約 2.0–2.5 美元的可持續 EPS。分母有兩個相反的問題。第一，1.94 美元看來尚未反映 11-05 上修；用新指引中點推算（營業利益 9 億×0.93÷341 百萬股）約 2.45 美元，倍數約 12.5。第二，全年營業利益中有 4.37 億美元屬前期項目，扣除後 EPS 約 1.26 美元，倍數約 24。EV/S 0.14 倍也不能用：70 億美元淨現金主要對應理賠準備與應付風險調整。改用母公司現金加子公司超額資本 17.6 億計，EV 約 82 億美元，EV/S 約 0.43 倍。股數方面，事實表 310.69 百萬未含完整稀釋，第三季隱含稀釋股約 341 百萬，市值會高約 10%。保險業常用的 P/TBV 因事實表沒有帳面淨值而無法使用。","premortem":"依據見反證紀錄。亮燈兩項：EPS 成長高於營收成長、市場人數萎縮。對 2027 Base EPS 2.35 美元做五項壓力測試：MLR 多 2 個百分點（約 −1.1）、風險調整不利 2 個百分點（約 −1.35）、市場人數少 15%（約 −0.45）、稅率回到 20%（約 −0.4），單獨發生時 EPS 都還是正的；MLR 與風險調整同時發生則轉負，五項過四項。歷史最大回撤、空方數字、訴訟與監管金額事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺的是 ACA 個人保單的承保利差，錢卡在 CMS 風險調整與聯邦補貼兩個節點。","moat":"護城河趨勢穩定，等級 C：執行力在擴大，定價權沒有變，份額增加還沒有證明優勢變寬。","growth":"五年後跑道中等：現有區域份額到時會達到公司自訂的 35% 成熟水準，第二曲線管理層自己也沒有放進數字。","capital":"資本配置偏弱：沒有回購，股數持續增加，新增資本多半要留在保險子公司。","valuation":"現價要求每股盈餘穩在 2.0–2.5 美元、不再回到虧損才划算。方向上相信，幅度上還不能確認，估值看成中性。","how_wrong":"最可能看錯在把 2026 當成常態獲利；價值陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月財報驗證 2027 財測、開年會員與 2026 全年 MLR，不設進場價。","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"金融","price_at_dd":30.65,"week26_return_pct":43.83,"consensus_rev_3m_pct":7.78,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"2026 共識 1.94 美元看來尚未反映上修，按新指引推算約 2.45 美元，扣掉前期項目 4.37 億美元後約 1.26 美元，對應本益比 15.8、12.5、24 倍；未定的是哪一個代表常態。"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"CMS 第二輪資格審查造成第四季會員再減少","impact":"中","watch":"年底會員是否約 250 萬"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 正式財測","impact":"高","watch":"營業利益率指引、開年會員、2026 全年 MLR"},{"date":"2027-05","date_precision":"quarter","type":"guidance","event":"第一季財報","impact":"中","watch":"有效會員是否至少 260 萬、Wakely 資料"},{"date":"2027-08","date_precision":"month","type":"regulatory","event":"第二季財報揭露 2026 年度風險調整結算差額","impact":"高","watch":"不利是否超過保費 2 個百分點"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,499B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/OSCR_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河：成本與通路優勢，等級偏低</h2>
<p class="lead">執行力在擴大，定價權沒有變，護城河維持 C 級，趨勢持平。</p>
<ul class="pts">
<li>機制是成本與通路，不是客戶鎖定。Oscar 為 ACA 建了窄網絡、經紀人工具與單一資料平台，成本因此低於一般綜合型保險商。會員每年重選一次，轉換成本低，經紀人用比價平台。這種優勢靠持續執行維持，一旦鬆懈就會被追上。</li>
<li>執行力評 7，定價權評 5。依據是自報區域份額由 17% 升到 30%，第三季 SG&amp;A 率 14.0% 創新低，2027 調幅 14% 對競爭者平均 15%。2026 費率上調後會員仍年增 27%，顯示相對價格比絕對價格重要，這是競爭力，不是鎖定。</li>
<li>同業 ROIC 利差算不出來。事實表沒有投入資本與同業 ROIC，OSCR 的營業利益率在同業表也是空值。所以本報告改用份額做方向證據，並承認份額增加還沒有證明優勢變寬。2027 開放投保若在費率相近下仍拿到份額，護城河才上調。</li>
<li>報酬屬低利益率高周轉。2026 當期 ROIC 約 32%，扣掉前期項目 4.37 億後約 16.5%，兩者的差距就是爭議所在。新增資本報酬約 25%，留存率 60%，內生成長上限約 15%。這些都由管理層目標推出，是上限，不是實績。</li>
<li>持續期最弱的一環是社會容忍度。定價上限由政治決定，2027 提案保費中位數漲約 15%，Oscar 喬治亞州申請約 29%。CEO 在 11-05 表示對 2027–28 恢復補貼不抱太大期待，公司也預期持續受 DOJ 與 HHS-OIG 審查。</li>
<li>威脅有四項，各約 15% 到 35% 的機率。對手回補與低價最高，Centene 與 AmeriHealth Caritas 2027 加縣市，UBS 分析師在法說指出有對手以最低價進場。其次是上游議價，部分市場醫院或醫師團體接近獨占。第三是技術沒有專利，AI 的成本優勢對手可以追上。最後是外包依賴，藥局理賠委外單一 PBM。</li>
</ul>
<h3>二維評分與護城河對數字</h3>
<!-- E5 -->
<h3>§5.F 對手財務深度對照</h3>
<!-- E6 -->
<p>同業表只有 CNC、MOH、ELV、CLOV 的部分利潤率。Oscar 自身的毛利率與營業利益率為空值，TTM FCF 利潤率 43% 是應付風險調整累積的浮存金，不能與同業比較。CNC 反向加縣市，是份額爭奪的主要對手。</p>
<h3>§5.R 報酬持續期檢核</h3>
<!-- E7 -->
</section>

```