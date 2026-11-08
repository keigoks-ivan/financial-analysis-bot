你是 stock-analyst v20 的**散文層（prose）agent**，標的 MSI（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MSI　日期：2026-11-08　archetype：None　前份裁決：2026-05-24　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2034B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（519B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（989B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1439B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1221B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（760B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1351B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2356B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3493B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2892B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2034           3476-4966      5 條（2–6 內）  
s3                  8000         519           5237-7481      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3649          7946-11351      5 條（2–6 內）  
s6                 11000         760          7168-10240      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1351           1504-2149      3 條（2–6 內）  
s10                 5000        2356           1851-2644      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2892           2000-2108      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5189B；至少需散文≈39.81KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−42%
−42
−41.8%
−33.7%
−32.4%
−30
−30%
−15%
−0.6%
0%
0
0.06%
0.11
0.3%
0.4
0.45
0.66
0.74%
0.75
0.941
1%
1
1.03
1.19
1.2%
1.26
1.39
1.5
1.57
1.6
1.67
1.69
1.7
1.85
1.92
2%
2
02
2.1
2.11
2.23
2.3
2.5
2.68
2.7%
2.74
2.85
3
3.06
3.1%
3.4%
3.67
3.9
4
4%
04
4.3%
4.54
05
5%
5
5.3
5.3%
5.8%
6%
6
6.3
6.35
07
7%
7
7.2%
7.5%
7.77
8
8%
08
8.5
8.6%
9
09
9%
9.2%
9.4%
9.5
9.7
10%
10
10.6%
10.69%
10.8
11%
11
11.7%
12%
12
12.6
12.6%
12.75
13
13%
13.3%
14%
14
14.5
15%
15.17
15.3%
16
16.53%
16.93
17
17.1%
17.62
17.73
17.94
17.965
17.99
18%
18.3
18.6
19
19.4
19.43
19.8
20.0%
20
20%
20.11%
20.5
20.7
21.2
21.69
22
22%
22.8
23
23.87%
23.9
24%
24
24.3
25
25%
25.42%
25.55%
26
26.48
26.7
27
27%
27.3%
27.4
28%
28.6
28.64
29
29.02
29.2
30%
30
30.5
31
31%
31.1
31.7%
32
32.5
32.5%
33%
33.76
33.8%
34%
34.74
34.74%
35
36.4%
37%
37.3
40%
40
41.39
45
46.4%
48
49
50%
52.18%
52.2%
59.41%
60%
60.4
62.45
63%
64.97
70
73.6%
78%
78.25%
83.2
90
98.4
98.91
100
100%
130.5
142.5
146
150%
158
166
168
171.9
179
200
250
300
341
347.75
368.6
370
400
404.08
413.53
437
450
455
507
514.51
527
530
600
690
911
2025
2026
2027
2028
2029
2030
20261108
1,000
1,050
1,300
3,000
4,200
4,500
5,000
6,000
7,000
7,300
7,500
8,700
9,400
9,600
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
{"meta":{"ticker":"MSI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Motorola Solutions"},"oneliner":"公安無線電基本盤加上 Silvus 與 D-Fend 兩條新線，訂單與利潤率都在走高，但 Q3 扣除併購只成長約 5%，現價約 29 倍已計入 2027 年的好消息，不追價，等回到 455 美元以下。","thesis":{"H":[{"id":"H1","text":"公安無線電基本盤靠 D-Series 基礎建設與 APX NEXT 換機延長週期，帶動 backlog 持續年增。","2y":"FY2027 第三季 backlog 年增不低於 8%，達 179 億美元以上。","5y":"FY2031 P25 在美國公安仍為主流，MCN 年增維持中單位數。","10y":"FY2036 美國與歐洲公安專網未被公共寬頻全面取代。","threshold":"期末 backlog 年增不低於 8%；FY2026 Q3 為 14%。","source":"每季 8-K 新聞稿與法說 backlog 揭露。","drift_rule":"2 年期假設：連 2 季偏離門檻達 5% 視為削弱，連 3 季偏離達 10% 視為反轉。"},{"id":"H2","text":"Silvus 與 D-Fend 成為有營收的第二曲線，補上 LMR 成熟後的成長缺口。","2y":"FY2027 Silvus 營收不低於 10.8 億美元，D-Fend 不低於 2.5 億美元。","5y":"FY2031 兩者合計營收不低於 25 億美元。","10y":"FY2036 國防與反無人機占營收不低於 15%。","threshold":"FY2027 Silvus 年增不低於 20%，管理層口徑約 30%。","source":"每季法說口述；Silvus 併滿週年後揭露可能變少，若停止揭露改看 MCN 分部成長並標資料缺口。","drift_rule":"2 年期假設：連 2 季偏離門檻達 5% 視為削弱，連 3 季偏離達 10% 視為反轉；5 年期假設：連 4 季偏離達 5% 視為削弱，連 6 季偏離達 10% 視為反轉。"},{"id":"H3","text":"營運槓桿與軟體加值蓋過記憶體與一次性利益消失的逆風，營益率繼續擴張。","2y":"FY2027 Non-GAAP 營益率高於 FY2026 至少 30bp，軟體與服務年增不低於 10%。","5y":"FY2031 自由現金流利潤率不低於 24%。","10y":null,"threshold":"FY2027 Non-GAAP 營益率年變化不低於 +30bp，毛利率不得連 2 季年減。","source":"每季 8-K、法說與 10-Q。","drift_rule":"2 年期假設：連 2 季偏離門檻達 5% 視為削弱，連 3 季偏離達 10% 視為反轉。"}],"R":[{"id":"R1","text":"記憶體成本 2027 年可能再增加約 1.5 億美元，IEEPA 退款約 7,500 萬美元不再有，加上關稅、單一來源料件與代工集中，合計約 158bp 逆風。","h_ref":"H3","clock":"⚡","threshold":"毛利率連 2 季年減，或 FY2027 營益率指引低於 FY2026。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R2","text":"Silvus 是非線性業務，Q4 隱含約 1.6 億美元，低於 Q3 近 3 億；美國國防仍在測試階段，新創與國防承包商競爭加劇。","h_ref":"H2","clock":"🔥","threshold":"FY2027 年增低於 20%，或 MCN 連 2 季年增低於 5%。","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"公共寬頻、衛星或其他新技術被客戶認定足以取代 LMR，新競爭者進入加快。","h_ref":"H1","clock":"🐢","threshold":"美國人口前十大州或歐洲主要國家任一宣布關閉專網轉公共寬頻；事實表範圍內尚無案例。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0"]},{"id":"R4","text":"英國 CMA 對 Airwave 的費率管制成立且上訴失敗，Home Office 將關停目標延至 2029-12-31；若其他政府援引，軟體與服務利潤率受壓。受影響營收事實表未涵蓋。","h_ref":"H3","clock":"🔥","threshold":"軟體與服務營益率連 4 季年減達 100bp，或任一美國州合約續約含年度調降條款。","evidence_refs":["regulatory_antitrust#2"]},{"id":"R5","text":"生物辨識與車牌辨識面臨州法與 FTC 執法，預期州立法增加，影響 Video 與分析產品。受影響營收事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"Video 年增低於 5%，或人口前十大州通過禁用車牌辨識的立法。","evidence_refs":["regulatory_antitrust#1"]}],"single_thing":{"description":"2027 年 2 月法說給出的 FY2027 全年 Non-GAAP 營益率指引低於 FY2026，管理層 11 月承諾的擴張落空。","why_fatal":"現價約 28.6 倍建立在營益率連年擴張上。每 100bp 約等於 0.66 美元 EPS（142.5 億美元 × 1% × 78% ÷ 1.67 億股），更大的傷害來自倍數，擴張中斷後倍數可能退到 23 倍上下。","if_happens":"FY2027 EPS 由 19.8 美元降到約 19 美元，乘 23 倍為 437 美元，較現價約 −15%，Base 路徑要全面下修。","how_monitor":"2027 年 2 月財測，以及每季毛利率與記憶體直接成本揭露。","probability":"約 15%（12 至 24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":26.48,"peg_fy2":2.5,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":12.75,"FY2026E":17.73,"FY2027E":19.43,"FY2028E":21.69},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin Non-GAAP 共識（2026-11-07）；基期 12.75 美元是 GAAP 稀釋 EPS，事實表未涵蓋 FY2025 Non-GAAP EPS，不能拿基期與共識算成長率。FY2026E 共識 17.73 美元低於公司 11 月 4 日上調後財測 17.94 至 17.99 美元，快照尚未反映；分析師家數事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"毛利率由 FY2022 的 46.4% 升到 TTM 52.2%，FY2025 自由現金流為淨利 1.19 倍，無客戶超過 10%。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：公安預算與地方稅、911 費綁定，CEO 於 2026-11-04 稱跨政黨都優先，DHS 資金到 2029 年；Silvus 需求偏週期，單獨打折。","bargaining":{"up":"記憶體漲價由供應商主導，公司付更高價並選擇性轉嫁；單一來源料件議價力弱。","down":"公安客戶更換成本高，但政府採購與英國 CMA 費率管制設了上限。","geo":"墨西哥、馬來西亞代工與稀土限制是地緣曝險。"},"profit_pool_dir":"往軟體、影像與指揮中心移動，五年利潤池數字事實表未涵蓋。","tam_table":[{"item":"可服務市場（管理層口徑）","value":"接近 1,000 億美元（CEO，2026-11-04），無第三方驗證"},{"item":"滲透率","value":"FY2026 財測營收 130.5 億美元，約 13%"},{"item":"美國第一線人員","value":"約 200 萬人；APX NEXT 應用程式用戶 2026 年底約 30 萬，約 15%"},{"item":"分段 CAGR 與營業利益池占比","value":"事實表未涵蓋，無法判斷利潤池是否流出"}]},"moat":{"mechanism":"專網安裝基礎、長約服務與跨產品工作流程綁定，更換需以州級網路為單位決策。","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行面擴大（三度上修、Q3 營益率擴張 200bp），定價面穩定（毛利率上升，但英國費率管制設上限、記憶體只選擇性轉嫁）；合併判穩定。沒有第三方份額或同業 ROIC 差距可證擴大。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以利潤率代替，只能看水準不能看方向。","threats":[{"level":"🟡","text":"公共行動寬頻取代 LMR，目前進展有限；公司以 APX NEXT 接 5G 與 T-Mobile 衛星，把寬頻納入自家裝置。屬架構層風險，若主要國家真的關閉公安專網就重評。","p":"10 年內 30%，5 年內約 15%","evidence_refs":["competitive_share_entrants#2","substitute_technology#0"]},{"level":"🟡","text":"新競爭者進入加快，Silvus 收購後面對新創與國防承包商；低價消耗型無人機市場擴大，公司推功能較少的 LC 機種應對。","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"影像與指揮中心的跨產品競爭。Q2 法說稱 FHP 與 KC 是翻盤案，對手份額事實表未涵蓋。","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率，周轉率待查（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是第一線員警與消防，決策者是州與地方機關，付款來自地方稅與 911 費，三角色都成立；換機時程可拖，但通訊需求不能取消。Q3 訂單年增逾 20%。"},{"item":"決策層級","level":"🟢","text":"替代要在州級網路層級決定；路易斯安那 10 年、1.39 億美元合約把無線電服務、影像與指揮中心綁在一起。流失率與續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"毛利率四年升近 6 個百分點，但記憶體由 2025 年 5,000 萬美元升到 2026 年約 1.5 億，2027 年可能再倍增，單一來源料件與代工廠分走部分議價力。"},{"item":"社會容忍度","level":"🟡","text":"政府付費的必需品，價格上限由政治決定：英國 CMA 已對 Airwave 實施費率管制且上訴失敗，州層級 ALPR 立法預期增加；美國尚未見費率管制。"}],"roiic":"資料缺口：事實表未涵蓋投入資本與 Silvus 收購金額，無法算整體增量報酬。可算的只有 D-Fend：淨付 13 億美元，FY2027 營收約 2.68 億，假設營益率 33%、稅率 22%，首年報酬約 5.3%。","reinvest_rate":"FY2026 僅 D-Fend 一筆約占稅後營業利益 50%（13 億 ÷〔TTM GAAP 營益率 25.42% × 130.5 億 × 78.25%〕）；資本支出減折舊與營運資金事實表未涵蓋。FY2023 至 FY2025 自由現金流累計 64.97 億美元，高於以 22% 稅率估算的稅後營業利益 62.45 億，有機業務幾乎不需再投入。","endo_ceiling":null,"formula_note":"若用下一年獲利增量除以當年再投資，再乘再投資率，得到的就是獲利預測本身，屬循環論證，因此不填數字。"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","MSI":52.18,"AXON":59.41,"ZBRA":48.9,"TDY":43.6,"LHX":25.55,"unit":"%"},{"metric":"營業利益率","MSI":25.42,"AXON":0.74,"ZBRA":16.53,"TDY":20.0,"LHX":10.69,"unit":"%"},{"metric":"FCF 利潤率","MSI":20.11,"AXON":4.14,"ZBRA":16.09,"TDY":17.6,"LHX":15.6,"unit":"%"},{"metric":"研發密度","MSI":8.39,"AXON":23.87,"ZBRA":10.32,"TDY":5.07,"LHX":2.59,"unit":"%"}],"competitors":[{"name":"AXON","gm":59.41,"om":0.74,"fcf_margin":4.14,"rd_intensity":23.87,"strategy_note":"影像與指揮軟體的直接對手，研發密度 23.87% 約為 MSI 的 2.85 倍，TTM 營益率僅 0.74%，以投入換份額；份額數字事實表未涵蓋。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ZBRA","gm":48.9,"om":16.53,"fcf_margin":16.09,"rd_intensity":10.32,"strategy_note":"企業行動裝置與掃描，客群不同，營益率 16.53% 僅作硬體利潤率參照。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"TDY","gm":43.6,"om":20.0,"fcf_margin":17.6,"rd_intensity":5.07,"strategy_note":"感測與無人系統在國防端有重疊，營益率 20.0%，不構成公安專網對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"LHX","gm":25.55,"om":10.69,"fcf_margin":15.6,"rd_intensity":2.59,"strategy_note":"列在 10-K 主要競爭者名單，TTM 毛利率 25.55%、營益率 10.69%，但屬綜合國防，口徑不完全可比。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主、價為輔；FY2026 成長約一半靠併購，FY2027 併購占比降到約五分之一。","runway_years":9.7,"runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本與累計併購金額，無法計算；可得部分見增量報酬欄。","segments":[{"item":"產品與系統整合 Q3","value":"年增 12%，其中併購 1.69 億美元，扣除後約 2.7%"},{"item":"軟體與服務 Q3","value":"年增 13%，其中併購 4,200 萬美元，扣除後約 9.4%"},{"item":"Silvus","value":"FY2026 略高於 9 億美元，FY2027 管理層預期年增約 30%"},{"item":"D-Fend","value":"全年口徑 1.85 億美元，FY2026 併入 4,500 萬，FY2027 預期年增 40% 至 50%"},{"item":"Video","value":"2026 年雙位數成長，Q2 法說指引 11%"},{"item":"Command Center","value":"2026 年約 15%（CEO，2026-11-04）"},{"item":"區域 Q3","value":"北美 23 億美元年增 10%，國際 10 億美元年增 18%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"全年毛利率預期上升"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"無反向證據，但份額數字事實表未涵蓋"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"選擇性漲價後未見銷量下滑"},{"signal":"EPS CAGR 高於營收 CAGR 逾 5 個百分點","lit":true,"note":"FY2022 至 FY2025 GAAP 稀釋 EPS 年化 17.1%，營收 8.6%，差 8.5 個百分點；扣除 2025 年 Hytera 回收 1.57 億美元仍差約 6.3 個百分點"},{"signal":"自由現金流對淨利連 2 年低於 0.75","lit":false,"note":"FY2025 為 1.19"},{"signal":"SBC 占營收逾 5% 且上升","lit":false,"note":"Q3 約 3.1%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"寬頻替代目前進展有限"},{"signal":"產業估值倍數 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"signal":"維護性資本支出占自由現金流逾 60%","lit":false,"note":"Q3 全部資本支出 7,300 萬美元，占自由現金流約 12%"},{"signal":"停止投資新產能且營收下滑","lit":false,"note":"正在擴充 Silvus 產能"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"Q3 現金股利","value":"2 億美元"},{"item":"Q3 回購","value":"9,400 萬美元"},{"item":"Q2 回購均價","value":"413.53 美元"},{"item":"Q3 資本支出","value":"7,300 萬美元"},{"item":"D-Fend","value":"淨付 13 億美元，2026 年下半年完成"},{"item":"新發長債","value":"2026 年 8 月 9.5 億美元，另再融資 Silvus 定期貸款 3 億美元"},{"item":"回購授權","value":"2026-09-09 增加 20 億美元，累計 200 億美元"},{"item":"近三年現金去向四分","value":"事實表未涵蓋"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Silvus 收購金額事實表未涵蓋，FY2026 營收略高於 9 億美元，CEO 稱高於商業計畫，Q3 認列 earn-out 增加 8,700 萬美元；D-Fend 淨付 13 億美元，假設營益率 33%、稅率 22%，FY2027 報酬約 5.3%，尚未到可評斷期。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"Q2 回購均價 413.53 美元，以 FY2026 財測中點 17.965 美元算盈餘殖利率約 4.3%；十年期公債殖利率事實表未涵蓋，無法比對門檻。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數由 FY2022 約 171.9 百萬股（淨利 ÷ 稀釋 EPS）降到 FY2026 指引約 168 百萬股，年均約 −0.6%。","grade":"過"}]},"valuation":{"basis":"Non-GAAP FY2026 前瞻本益比搭配 PEG，以品質複利股的盈餘倍數為主尺。","tier":"品質複利","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業前瞻本益比，無法做倍數對照。"},"fwd_pe":29.02,"peg":2.74,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026 約 28.6 至 29 倍、PEG 2.74、短期上行約 4%、Base 年化約 8%。偏貴但未到最貴一檔：盈餘口徑年度端點分位 60.4，Base 不需要倍數上升也有約 8%。股價再漲約 10% 而 EPS 未上修，就進最貴一檔。","upside_short_pct":3.9,"upside_mid_pct":22.8},"trap_analysis":{"verdict":"🟡","label":"價值陷阱機率低，主要風險是高倍數回落，而非生意變壞；十類衰退信號亮一類。"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 營收增量扣除併購與匯率後約 5%，產品與系統整合扣除併購約 2.7%；Silvus 隱含 Q4 約 1.6 億美元，低於 Q3 近 3 億；10-K 列明寬頻替代與新競爭者。","assumption":"FY2027 有機成長加速到約 7.5%，靠 LMR 在 Q4 的強勁雙位數與 Silvus 再成長 30% 接力。","consequence":"EPS 停在 19 美元且倍數掉到 13 倍才會腰斬；較可能的壞結果是 370 美元上下，跌約 28%。","ruling":"部分採納：backlog 166 億美元與訂單年增逾 20% 反駁近端失敗，但 Q3 有機成長偏低屬實，已納入 Bear 機率與不追價結論。","watch":"FY2026 Q4 LMR 成長與 FY2027 財測的有機成長口徑。","evidence_refs":["competitive_share_entrants#2","substitute_technology#0","competitive_share_entrants#1"],"fact_refs":["f_kpi0_net_sales_gaap","f_kpi6_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"D-Fend 淨付 13 億美元，FY2027 營收約 2.68 億，首年稅後報酬約 5%；8 月新發 9.5 億美元債，Q3 回購僅 9,400 萬美元；Silvus earn-out 增加 8,700 萬美元，Non-GAAP 全部排除。","assumption":"併購標的長大後報酬高於資金成本，且 Non-GAAP 能代表股東實得。","consequence":"營收與 Non-GAAP EPS 都達標，但 GAAP 獲利與每股自由現金流落後；Q3 SBC 年化每股約 1.92 美元，計入後 FY2026 約 32 倍。","ruling":"採納，資本配置只給到資料允許的程度，估值同時看含 SBC 的倍數。","watch":"GAAP 與 Non-GAAP EPS 差距、年底淨負債對 EBITDA 約 2 倍的承諾、Silvus 併滿週年後揭露是否減少。","evidence_refs":[],"fact_refs":["f_kpi4_sbc_gaap","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"記憶體直接成本由 2025 年 5,000 萬美元升到 2026 年約 1.5 億，CEO 稱 2027 年可能倍增；IEEPA 退款約 7,500 萬美元不再有；部分料件單一來源，代工集中在墨西哥與馬來西亞，庫存預期維持高檔。","assumption":"營運槓桿與選擇性漲價蓋過約 158bp 的成本逆風。","consequence":"每 100bp 營益率約 0.66 美元 EPS，占 FY2027 約 3.4%，且會牽動倍數。","ruling":"部分採納：管理層兩度承諾 2027 年營益率擴張，但沒有給數字，因此列為唯一致命點。","watch":"每季毛利率年變化與記憶體成本揭露。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"],"fact_refs":["f_kpi5_guidance_q4_fy2026_fy202"]},{"view":"價格已反映太多","evidence":"FY2026 約 29 倍，PEG 2.74，26 週上漲 34.74%；自前份以來股價上漲 27%、財測 EPS 上升約 6%，約四分之三來自倍數；FY2027 共識營收已等於管理層口頭的 142.5 億美元。","assumption":"29 倍能維持，且 EPS 上修足以吸收。","consequence":"Base 年化約 8%，倍數回到 25 倍以下時全靠 EPS 硬撐。","ruling":"採納，這是不追價的主因。","watch":"股價相對 455 美元，FY2027 共識 EPS 上修幅度。","evidence_refs":[],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_week26_return_pct"]}],"max_dd":{"lo":-42,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 404.08 → 本次 514.51（+27.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=404.08","side_b":"本次 price_at_dd=514.51","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 404.08 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 404.08 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 404.08 美元：Bull 價 1,050、Bear 價 368.6，五年期望值 +73.6%，基準年化 12.6%，不對稱比 15.17","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 15.17。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 404.08 美元：五年期望值 +73.6%，基準年化 12.6%，不對稱比 15.17","side_b":"本次情境、股價 514.51 美元：五年期望值 +36.4%，基準年化 7.2%，不對稱比 3.06","ruling":"再換股價、情境不動：起點價上漲 27.3%，五年期望值少 37.3 個百分點，基準年化少 5.3 個百分點，不對稱比由 15.17 降到 3.06。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"Q3 超預期與全年上修不成比例","cause":"新證據","prior_field":null,"side_a":"管理層：Q4 將是史上最強，指引只是審慎（CEO，2026-11-04）。","side_b":"Q3 營收 33.76 億美元，高於原指引約 32.5 億，多出約 1.26 億；全年指引只升 7,500 萬，其中 D-Fend 貢獻 4,500 萬。扣除後全年只升 3,000 萬，隱含 Q4 下調約 9,600 萬，CEO 未回答是否有提前認列。","ruling":"可調和，偏向部分提前認列加上保守。提前認列或審慎的說法不採信也不否定，標示未證。","evidence_level":"公司指引與法說口述，需 Q4 實績驗證","settle_metric":"2027 年 2 月公布的 Q4 營收年增率，對照 13% 指引","if_then":["若 Q4 營收年增高於 14%，判定審慎屬實，仍不追價，上調 FY2027 EPS 基準後重算買點。","若 Q4 營收年增低於 12%，判定 Q3 提前認列，停止加碼並維持 Bear 機率 30%。"],"evidence_refs":[]},{"axis":"雙位數成長與有機成長","cause":"新證據","prior_field":null,"side_a":"管理層：兩大分部都雙位數成長。","side_b":"Q3 扣除併購與匯率約 5%，產品與系統整合扣除併購約 2.7%，軟體與服務約 9.4%。","ruling":"可調和，標題數字正確但成色不同；FY2027 有機約 7.5% 要靠 Q4 起的 LMR 加速與 Silvus，尚未發生。","evidence_level":"8-K、10-Q 與法說","settle_metric":"FY2027 財測的有機成長率，門檻 7%","if_then":["若 FY2027 有機成長指引不低於 7%，維持 Base。","若低於 5%，把 FY2027 EPS 下修到 19 美元並停止加碼。"],"evidence_refs":[]},{"axis":"Silvus 需求強勁與競爭升溫","cause":"新證據","prior_field":null,"side_a":"CEO：價格維持且上升，未見需求放緩，FY2027 年增約 30%，繼續拿份額。","side_b":"10-K 指新創與國防承包商競爭加劇；隱含 Q4 約 1.6 億美元；美國國防多在測試階段；為低價市場推出功能較少的 LC。","ruling":"可調和：短期有訂單與擴產支持，長期定價未證，以 FY2027 年增 20% 為檢驗線。","evidence_level":"管理層口述為主，缺第三方份額數字","settle_metric":"FY2027 Silvus 年增率","if_then":["若 FY2027 年增不低於 20%，維持第二曲線假設。","若低於 10%，視為失速並減碼。"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"backlog 166 億美元、FY2027 營收能見度高，有機加速、營益率擴張、Silvus 再成長 30%；共識 19.43 美元落後，我估 19.8 美元，好生意不該等便宜。","side_b":"Base 年化約 8%，短期上行約 4%；記憶體 2027 年可能倍增的訊息 11 月才出現，尚未確認進入共識，下一個驗證點在 2 月。","ruling":"選不追價，綁定限制是價格，455 美元以下 Base 年化約 11%。","evidence_level":"情境計算與法說","settle_metric":"股價相對 455 美元，以及 2027 年 2 月 FY2027 EPS 指引","if_then":["價格先走、證據未到：股價漲破 600 美元而 FY2027 EPS 指引未達 20.5 美元，不追。","跌破 455 美元且 backlog 年增仍不低於 8%，分批反買第一批。","股價未跌但 FY2027 EPS 指引不低於 20.5 美元，重算買點，門檻同比例上調。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：10-K 稱競爭者增加、進入速度加快，Silvus 面對新創與國防承包商，但沒有份額流失的數字。","side_b":"結構：D-Series 更新到 2030 年代，無人系統與反無人機帶來新需求，公安預算穩定；其他變數是 CMA 費率管制、記憶體、關稅與 ALPR 立法。","ruling":"結構性轉好中；競爭軸目前只有文字揭露沒有數字，記憶體與監管是要盯的其他變數。","evidence_level":"10-K 與法說","settle_metric":"backlog 年增與毛利率年變化","if_then":["若 backlog 年增連 2 季低於 5%，改判需求見頂或競爭惡化，停止加碼。"],"evidence_refs":["competitive_share_entrants#0","reg_tariff_export#0","regulatory_antitrust#2"]},{"axis":"前份地方預算風險降位","cause":"新證據","prior_field":null,"side_a":"前份門檻：P&SI YoY 連 2 季偏弱，當時增速 +1%。","side_b":"Q3 P&SI 年增 12%，扣除併購約 2.7%；地方預算未見收縮，CEO 稱 DHS 資金到 2029 年。","ruling":"降位保留：指標改為扣除併購後年增，門檻為連 2 季低於 0%，資料來自 10-Q。","evidence_level":"10-Q 與法說","settle_metric":"產品與系統整合扣除併購後年增","if_then":["若連 2 季低於 0%，停止加碼並重看 LMR 更新假設。"],"evidence_refs":[]},{"axis":"前份軟體服務成長假設下修","cause":"新證據","prior_field":null,"side_a":"Software & Services 加速至 +18% 為新常態，FY26/27 年增 ≥ +15%。","side_b":"Q3 軟體與服務年增 13%，扣除併購約 9.4%；本次門檻改為年增不低於 10%。","ruling":"前份門檻未達，下修並併入營益率假設。","evidence_level":"8-K 與法說","settle_metric":"軟體與服務年增率","if_then":["若連 2 季低於 10%，停止加碼。"],"evidence_refs":[]},{"axis":"前份 Silvus 整合風險換軌","cause":"新證據","prior_field":null,"side_a":"前份門檻：2027 earnout 部分達成視為整合失敗。","side_b":"Silvus FY2026 略高於 9 億美元，CEO 稱高於商業計畫，Q3 認列 earn-out 增加 8,700 萬美元；風險由整合失敗轉為週期與競爭。","ruling":"門檻更換：不再看 earn-out，改看 FY2027 年增 20%。","evidence_level":"法說","settle_metric":"FY2027 Silvus 年增率","if_then":["若 FY2027 年增低於 10%，減碼。"],"evidence_refs":[]},{"axis":"估值結論與情境機率","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 404.08 美元，當時財測中點 16.93 美元，約 23.9 倍，結論偏貴。","side_b":"本次股價 514.51 美元，財測中點 17.965 美元，約 28.6 倍；股價上漲 27%，約四分之三來自倍數。","ruling":"仍在偏貴一檔，但已接近最貴一檔；前份未留機率與最大回撤數值，本次新設。","evidence_level":"事實表價格與公司財測","settle_metric":"FY2026 本益比","if_then":["若股價再漲約 10% 而 EPS 未上修，改列最貴一檔，不追。"],"evidence_refs":[]},{"axis":"整體評級","cause":"新證據","prior_field":["signal"],"side_a":"前份評級 B。","side_b":"本次維持 B：基本面較前份強（三度上修、backlog 166 億美元），但改善已被價格吸收。","ruling":"維持，不因基本面改善而升級。","evidence_level":"財報與法說","settle_metric":"Base 年化報酬是否高於 11%","if_then":["若股價回到 455 美元以下，重跑研究再決定是否升級。"],"evidence_refs":[]},{"axis":"價值陷阱結論","cause":"方法變動","prior_field":["trap"],"side_a":"前份為低風險。","side_b":"本次逐項清點十類衰退信號，EPS 與營收成長差距亮燈一類，結論改為黃。","ruling":"生意未變壞，變動來自檢查項目更完整。","evidence_level":"年度財務歷史","settle_metric":"亮燈類別數","if_then":["若亮燈達 3 類，改列紅並停止加碼。"],"evidence_refs":[]},{"axis":"前份空白欄位首次給值","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份這六欄為空。","side_b":"本次首次給出護城河趨勢、五年後跑道、公司類型與循環位置；裁決與角色由程式得出。","ruling":"屬框架補齊，不代表基本面轉向。","evidence_level":"本次研究","settle_metric":"下次研究對帳","if_then":["若下次任一欄轉差，須指名對應證據後才可調整倉位。"],"evidence_refs":[]},{"axis":"行動門檻新設：重新進場、減碼與清倉","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重新進場條件與停損指標皆為空。","side_b":"重新進場：股價 455 美元以下。減碼：毛利率連 2 季年減、或 Silvus FY2027 年增低於 10%。清倉：美國人口前十大州任一宣布關閉 P25 改採公共寬頻。","ruling":"新設門檻，取代前份只有觀察指標沒有動作的寫法。","evidence_level":"本次研究","settle_metric":"各門檻指標","if_then":["觸發減碼或清倉條件時，依條件動作，不再等下一次研究。"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":null,"side_a":"前份未設唯一致命點（欄位為空）。","side_b":"2027 年 2 月法說給出的 FY2027 全年 Non-GAAP 營益率指引低於 FY2026，管理層 11 月承諾的擴張落空。","ruling":"Single Thing 新設，選營益率是因為它同時影響 EPS 與倍數，敏感度最大。","evidence_level":"法說","settle_metric":"FY2027 營益率指引","if_then":["若指引低於 FY2026，取消建倉計畫；已持有則減碼一半。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 455 美元以下，Base 年化約 11%，才開始第一批建倉。","type":"估值rearm","maps_to":"H1、H2、H3","metric":"MSI 收盤價","threshold":"≤ 455 美元","action":"分批反買第一批，建倉前重跑一次研究","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"FY2027 全年 Non-GAAP 營益率指引低於 FY2026。","type":"Single Thing","maps_to":"H3","metric":"FY2027 Non-GAAP 營益率指引相對 FY2026","threshold":"指引低於 FY2026 實績","action":"未持有則取消建倉計畫，已持有減碼一半","source_freq":"2027 年 2 月法說，一次性","date":"2027-02","evidence_refs":[]},{"n":3,"text":"backlog 年增連 2 季低於 5%，換機週期假設削弱。","type":"假設驗證","maps_to":"H1","metric":"期末 backlog 年增率","threshold":"連 2 季 < 5%","action":"停止加碼","source_freq":"每季 8-K","date":null,"evidence_refs":[]},{"n":4,"text":"Silvus FY2027 年增低於 20%，第二曲線假設削弱；若公司停止揭露，改看 MCN 分部並標資料缺口。","type":"假設驗證","maps_to":"H2","metric":"Silvus 年增率","threshold":"FY2027 < 20%","action":"停止加碼","source_freq":"每季法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":5,"text":"毛利率連 2 季年減，代表記憶體與關稅吸收失敗。","type":"風險","maps_to":"R1","metric":"毛利率年變化","threshold":"連 2 季年減","action":"減碼","source_freq":"每季 8-K","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0"]},{"n":6,"text":"軟體與服務營益率持續下滑，或美國州合約出現年度調降條款，代表英國費率管制模式擴散。","type":"風險","maps_to":"R4","metric":"軟體與服務營益率；州合約續約條款","threshold":"連 4 季年減 ≥ 100bp，或任一州合約含年度調降條款","action":"減碼","source_freq":"每季 8-K 與合約新聞","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":7,"text":"產品與系統整合扣除併購後連 2 季負成長，地方預算風險重新啟動。","type":"風險","maps_to":"H1","metric":"產品與系統整合扣除併購後年增","threshold":"連 2 季 < 0%","action":"停止加碼","source_freq":"每季 10-Q","date":null,"evidence_refs":[]},{"n":8,"text":"股價跌到 400 美元以下而 backlog 仍成長，屬價格先走、基本面無損。","type":"加碼","maps_to":"H1","metric":"收盤價與 backlog 年增","threshold":"≤ 400 美元且 backlog 年增 ≥ 8%","action":"分批反買第二批","source_freq":"每日收盤與每季 8-K","date":null,"evidence_refs":[]},{"n":9,"text":"股價達 FY2027 EPS 約 35 倍時，已超過自身合理上緣。","type":"減碼","maps_to":"H3","metric":"收盤價","threshold":"≥ 690 美元","action":"減碼","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":10,"text":"美國主要州宣布關閉 P25 改採公共寬頻，架構替代成真。","type":"清倉","maps_to":"R3","metric":"州級專網政策","threshold":"美國人口前十大州任一宣布","action":"清倉","source_freq":"事件","date":null,"evidence_refs":["substitute_technology#0","competitive_share_entrants#2"]},{"n":11,"text":"FY2026 Q4 財報與 FY2027 財測公布後一週內複審。","type":"複審日期","maps_to":"H1、H2、H3","metric":"FY2027 財測","threshold":"財報公布","action":"重跑研究","source_freq":"一次性","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"期末 backlog 年增率","bear_threshold":"連 2 季低於 5%","window":"2 季","source":"每季 8-K 新聞稿","last_status":"ok"},{"metric":"FY2027 Non-GAAP 營益率相對 FY2026","bear_threshold":"全年指引或實績低於 FY2026","window":"2027-02 至 2028-02","source":"法說與 8-K","last_status":"unknown"},{"metric":"Silvus 年增率","bear_threshold":"FY2027 低於 20%，低於 10% 視為失速","window":"FY2027","source":"每季法說口述","last_status":"ok"},{"metric":"產品與系統整合扣除併購後年增","bear_threshold":"連 2 季低於 0%","window":"2 季","source":"10-Q 分部說明","last_status":"warning"},{"metric":"軟體與服務營益率","bear_threshold":"連 4 季年減 100bp 以上","window":"4 季","source":"每季 8-K 新聞稿","last_status":"ok"},{"metric":"毛利率年變化","bear_threshold":"連 2 季年減","window":"2 季","source":"每季 8-K 新聞稿","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=34.74, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 路徑只有 FY2027 有分部算術，其後年份靠成長率假設，跑道依據是管理層自己的 1,000 億美元市場口徑，沒有第三方佐證；也沒有查到可比案例能證明或否定 +15.3% 年化，所以這個 Bull 依據有一部分站得住，但不能當成已驗證的數倍成長依據。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 455 美元以下'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價回到 455 美元以下（Base 年化約 11%）；門檻隨 FY2031 Base EPS 上修同比例調整","exec_line":"現價不追。到 455 美元以下先建第一批並重跑研究；到 400 美元以下且 backlog 年增仍不低於 8% 再加第二批。記憶體倍增的訊息 11 月才出現，2027 年 2 月財測前不加碼。"},"reasoning":{"industry":"分部以 Q3 分部營益與營益率回推（法說 2026-11-04，CFO）：產品與系統整合約 21.2 億美元，占 63%，營益率 31.7%；軟體與服務約 12.6 億美元，占 37%，營益率 33.8%。全公司 TTM 毛利率 52.18%，Q3 Non-GAAP 營益率 32.5%。客戶面，美國政府只占 2025 年營收約 8%，沒有單一客戶超過 10%；政府業務多數來自州與地方，資金來自地方稅與 911 費，1,300 個 P25 網路是基本盤（COO，2026-11-04）。產業時鐘判 II 擴張：Q3 訂單年增逾 20%，backlog 166 億美元年增 14%，D-Series 是 12 年來首次基礎建設更新（CEO，2026-08-05），COO 稱延續到 2030 年代。供需判斷：公安部分結構性持久，Silvus 部分帶週期性，無人系統與烏克蘭相關需求可能反轉。單點依賴：部分零組件單一來源，多數產品由墨西哥與馬來西亞代工，屬集中度風險。Q3 標題成長要看成色：營收增加 3.67 億美元，併購貢獻 2.11 億、匯率 0.11 億，扣除後約 5%；產品與系統整合扣除併購只有約 2.7%。","moat":"機制是 1,300 個 P25 網路的安裝基礎、十年級服務合約，加上裝置、影像、指揮中心用 Assist 串起來的工作流程。可比軸：TTM 營益率 MSI 25.42%，對 TDY 20.0%、ZBRA 16.53%、LHX 10.69%、AXON 0.74%；毛利率 52.18% 僅低於 AXON 的 59.41%。同業歷史利潤率與 ROIC 事實表未涵蓋，只能看水準，無法判斷差距方向。定價面，Silvus 價格維持且上升、Assist 等級採用率接近 100% 都是管理層口述；英國 CMA 對 Airwave 的費率管制則證明定價有政治上限。執行面今年三度上修，Q3 營益率擴張 200bp，同時吸收記憶體成本。沒有份額或 ROIC 差距的第三方數字，趨勢只能判穩定，不能判擴大。當期 ROIC 無法計算，投入資本事實表未涵蓋；再投資報酬見下方欄位。","growth":"FY2026 財測營收年增 11.7%，估計併購貢獻約 6 個百分點（Q1 Silvus 2.1 億、Q2 2.3 億、Q3 併購增量 2.11 億、D-Fend 約 0.45 億），有機約 5.8%。FY2027 管理層口頭約 142.5 億美元，年增 9.2%，D-Fend 增量約 2.23 億，占 1.7 個百分點，有機約 7.5%，與管理層稱 2027 有機成長強於 2026 一致；其中 Silvus 年增 30% 貢獻 2.1 個百分點，其餘業務約 5.8%。Bell Canada 是否計入未說明。共識 EPS FY2026 至 FY2028 年化約 10.6%（Koyfin，家數事實表未涵蓋），可拆為營收約 9%、營益率年增約 0.4 個百分點貢獻約 1.2%、股數年減約 0.3%，再扣利息增加。內生天花板算不出，缺口無法量化，長期信心上限定為中，情境裡從嚴當作超過。依管理層 1,000 億美元市場口徑，以 9% 年增率達 30% 滲透約需 9.7 年。","governance":"FY2025 自由現金流對淨利 1.19 倍，TTM 自由現金流利潤率 20.11%。SBC 以 Q3 GAAP 營益 7.77 億乘 13.3% 約 1.03 億美元，占營收約 3.1%。Q3 現金去向：股利 2 億美元、回購 9,400 萬、資本支出 7,300 萬；D-Fend 淨付 13 億美元，8 月新發 9.5 億美元長債。近三年四分法去向與債務到期結構事實表未涵蓋。淨負債 98.91 億美元，CFO 預期年底淨負債對 EBITDA 約 2 倍。年初至今營運現金流約 16 億美元，全年財測 30.5 億，代表 Q4 要貢獻約 14.5 億。計分三項只有股本稀釋能確認通過，併購報酬與回購收益率都是資料缺口。","valuation":"現價 514.51 美元，以 FY2026 財測中點 17.965 美元算約 28.6 倍，以共識 17.73 美元算 29.02 倍，以 FY2027 共識 19.43 美元算 26.48 倍。共識快照在法說後幾乎未動（FY1 僅修正 0.06%），三年成長率以 FY2026 至 FY2028 共識算約 10.6%，PEG 2.74，高於 2 倍的貴價線。歷史位置只有 4 個年度端點：trailing P/E 分位 60.4，P/S 83.2，EV/S 98.4，五年分位事實表未涵蓋，故留空。P/E 在中段而銷售倍數在高點，反映利潤率已大幅提升，倍數能否守住取決於利潤率。Base 情境終端 25 倍，年化約 8%，全靠 EPS 複利，倍數貢獻為負。賣方目標價多取自 8 月，均值約 507 美元，區間 450 至 530 美元，FactSet 527 美元，都早於 Q3，參考性低；方向上接近現價，不支持追高，全距比遠低於 2.5 倍。同業前瞻本益比事實表未涵蓋。","premortem":"歷史最大回撤事實表未涵蓋，下行幅度改用均線與倍數推算。Q2 法說有四項未正面回答：產品 backlog 季減、APX NEXT 出貨占比、LMR 中期成長、Q4 加速來源。第一項已由實績回答，Q3 產品 backlog 季增 4.54 億美元；第二項仍無數字；第三項在 Q3 又以 2 月再談帶過（CEO，回答 Zilberman）；第四項在 Q3 又被問（Niknam），CEO 以審慎帶過。訂單增速有三種說法：開場逾 20%、問答稱整體 25%、CFO 稱 25% 是產品訂單，本文只採逾 20%。IEEPA 退款也有三個數字：Q2 法說 6,000 萬、10-Q 約 7,000 萬、Q3 法說約 7,500 萬美元，本文用 7,500 萬。Bell Canada 由 Q4 延到 2027 年 Q1 或 Q2，原因是客戶與監管核准。十類衰退信號亮一類，RSI 標記不可用，未納入動能判斷。"},"plain":{"six":{"how_it_makes_money":"賺美國州與地方政府及各國公安機關的錢，錢卡在專網基礎建設、無線電換機與其後長達十年的服務合約；Q3 兩大分部營益率都超過 31%。","moat":"護城河穩定：專網安裝基礎與生態綁定守住基本盤，新線的優勢還要時間驗證。","growth":"五年後跑道寬：基本盤更新延續到 2030 年代，另有 Silvus 與 D-Fend 兩條已有營收的曲線，但成長品質要扣掉併購來看。","capital":"資本配置方向正確但證據不齊：股本沒有被稀釋，現金轉換佳，兩筆大併購的報酬還看不出來，回購在高價位明顯縮手。","valuation":"現價要求 FY2031 前 EPS 年增約 10% 且倍數只小幅下修；我相信獲利，不認為這個價位還有足夠補償。","how_wrong":"最可能看錯的地方，是把併購與一次性利益算成內生動能，以及把 29 倍當成新常態。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 455 美元以下","qc48_result":"pass","qc48_note":"Bull 路徑只有 FY2027 有分部算術，其後年份靠成長率假設，跑道依據是管理層自己的 1,000 億美元市場口徑，沒有第三方佐證；也沒有查到可比案例能證明或否定 +15.3% 年化，所以這個 Bull 依據有一部分站得住，但不能當成已驗證的數倍成長依據。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":514.51,"week26_return_pct":34.74,"consensus_rev_3m_pct":0.23,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 有三個 Non-GAAP 分母：共識 17.73、財測中點 17.965、扣除 IEEPA 退款後約 17.62，倍數落在 28.6 至 29.2 倍，差距約 2%，不影響結論。計入 SBC（Q3 年化每股約 1.92 美元）約 32 倍；GAAP trailing 41.39 倍含 Silvus earn-out 等費用。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 Q4 財報與 FY2027 正式財測","impact":"高","watch":"營益率指引是否高於 FY2026、有機成長口徑、Silvus 揭露"},{"date":"2027-Q1","date_precision":"quarter","type":"capacity","event":"Salt Lake City 廠上線","impact":"中","watch":"Silvus 交期能否低於 12 至 14 週"},{"date":"2027-Q2","date_precision":"quarter","type":"other","event":"Bell Canada LMR 服務業務交割，預期 Q1 或 Q2","impact":"低","watch":"客戶與監管核准是否再延"},{"date":"2029-12","date_precision":"month","type":"regulatory","event":"英國 Airwave 關停目標 2029-12-31","impact":"中","watch":"Home Office 是否再延，以及費率管制是否被其他政府援引"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,145B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSI_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河評為 B 且持平，沒有數字證明在擴大。</p>
<ul class="pts">
<li>護城河的機制是安裝基礎、長約服務與工作流程綁定。1,300 個 P25 網路是基本盤，更換要以州級網路為單位決策。路易斯安那 10 年、1.39 億美元的合約，把無線電服務、影像與指揮中心綁在一起，替代者很難只拿走其中一塊。</li>
<li>執行面評 9，定價面評 8。執行面看今年三度上修，Q3 營益率擴張 200bp，同時吸收記憶體成本。定價面看毛利率上升，但英國 CMA 對 Airwave 的費率管制已成立且上訴失敗，證明定價有政治上限，記憶體成本也只能選擇性轉嫁。</li>
<li>水準領先同業。TTM 營益率 MSI 為 25.42%，TDY 為 20.0%，ZBRA 為 16.53%，LHX 為 10.69%，AXON 只有 0.74%。毛利率 52.18% 僅低於 AXON 的 59.41%。但同業歷史利潤率與 ROIC 事實表都沒有，只能看水準，無法判斷差距是擴大還是縮小。</li>
<li>公共寬頻取代專網是最大的架構風險。目前進展有限，公司用 APX NEXT 接 5G 與 T-Mobile 衛星，把寬頻納入自家裝置。機率估計 5 年內約 15%，10 年內 30%。美國人口前十大州或歐洲主要國家任一宣布關閉專網，就要重評，目前事實表內尚無案例。</li>
<li>新競爭者進入加快。Silvus 面對新創與國防承包商，低價消耗型無人機市場擴大，公司推功能較少的低價機種應對。影像與指揮中心則與 AXON 正面競爭，AXON 研發密度 23.87%，約為 MSI 的 2.85 倍，以投入換份額，但營益率只有 0.74%。</li>
<li>投入資本與 Silvus 收購金額事實表都沒有，整體增量報酬算不出來。可算的只有 D-Fend：淨付 13 億美元，FY2027 營收約 2.68 億，假設營益率 33%、稅率 22%，首年報酬約 5.3%。FY2026 這一筆約占稅後營業利益 50%。</li>
</ul>
<h3>§5 二維評分與護城河對應數字</h3>
<!-- E5 -->
<h3>§5.F 對手財務深度對照</h3>
<!-- E6 -->
<h3>§5.R 報酬持續期檢核</h3>
<!-- E7 -->
</section>

```