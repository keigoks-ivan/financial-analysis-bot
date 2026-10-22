你是 stock-analyst v20 的**散文層（prose）agent**，標的 ISRG（2026-10-22）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：ISRG　日期：2026-10-22　archetype：None　前份裁決：2026-07-17　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1489B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（377B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（864B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1146B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（808B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（448B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（815B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2101B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4049B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2106B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1489           3858-5511      5 條（2–6 內）  
s3                  8000         377           5336-7623      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2818          8527-12182      5 條（2–6 內）  
s6                 11000         448          7386-10552      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         815           1879-2685      5 條（2–6 內）  
s10                 5000        2101           2029-2899      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2106           2000-2894      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3904B；至少需散文≈41.10KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−48
−48%
−47%
−45%
−38%
−30
−30%
−5%
−4.7%
−4.7
−3
−2.94
0
0.35%
0.42
0.56
0.6%
0.87
0.9
0.9%
1%
1
01
1.13
1.5%
1.5
1.85
2.0
02
2
2%
2.13
2.8
2.83
2.9%
3
3.17
3.2
3.5
3.65%
3.79
3.8
4%
4
04
4.5
4.82
5
5%
5.28
6
6.1%
7%
07
7.0%
7
7.69
7.87
8%
8
08
8.6
8.6%
8.65
8.7
9
09
9.6
9.9%
10%
10
10.75
$10.75
10.80
10.8
10.8%
11%
11
11.4%
11.4
11.7
11.9
12%
12.0
12
12.12
12.5%
12.6
13%
13
13.4
13.5
13.67
14%
14
14.6
$14.7
14.7
14.9
15%
15.5%
16
16.4
16.9
17.4%
18%
18
18.2%
19%
19.0%
19.3%
19.4%
19.4
20
20%
21.0%
21%
21.7%
22
22%
22.6
23
24
24.1
24.9
25%
25
25.3%
26
27
27%
28
28%
28.6
28.7
29
29.2%
30
30%
30.49
31%
31.3%
32
33%
34
35
35%
35.3
35.32
36
38%
38
39.6
39.64
40
40%
41
41%
41.6%
42%
42
45
47.9%
49
49.4%
51.8
54%
55%
59%
60
60%
68
68%
68.7
69%
69.3%
69.9%
70
70%
80%
84%
85%
90
100
100%
104
150%
160
228
264
280
301
315
340
$348
$350
350
358.97
377
408
428
428.12
430
439
477
480
488
510
520
539
546
620
770
792
2020
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
20261022
1,152
1,512
1,780
1,800
1,860
12,094
18,000
2,000
48,000
6,370
7,240
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
{"meta":{"ticker":"ISRG","date":"2026-10-22","schema":"v15.0","contract":"v19","company_name":"Intuitive Surgical"},"oneliner":"達文西裝機帶動耗材與服務年金，第三季營收增 22%、手術量增 14%；但公司已宣布 2027 年器械降價 3–5%，美國手術量增速降到 10%，競品陸續拿到美國許可。前瞻本益比近 40 倍只對應年增約 12% 的盈餘，等股價回到 350 美元附近再談。","thesis":{"H":[{"id":"H1","text":"裝機基數與 84% 經常性收入守住，器械配件每台手術收入在延長使用計畫與中國降價全面實施後，加上組合抵銷，年降幅不超過 4%","2y":"2027 年底每台手術器械收入 ≥1,780 美元","5y":"經常性收入占比維持 ≥80%","10y":null,"threshold":"每台手術器械收入 ≥1,780 美元；經常性收入占比 ≥80%","source":"每季法說 CFO 揭露的每台手術器械收入、財報新聞稿經常性收入占比","drift_rule":"5 年期：連 4 季偏離門檻 ≥5% 削弱、連 6 季 ≥10% 反轉"},{"id":"H2","text":"海外良性手術、SP、Ion、心臟與 ASC 接棒，全球達文西手術量維持年增 11% 以上到 2028 年","2y":"2027 年全球 ≥12%、美國 ≥8%","5y":"2028–2030 年全球 ≥10%","10y":null,"threshold":"全球達文西手術量年增 ≥11%、美國 ≥8%","source":"每季財報新聞稿與法說手術量數據","drift_rule":"5 年期：連 4 季偏離門檻 ≥5% 削弱、連 6 季 ≥10% 反轉"},{"id":"H3","text":"在降價與關稅下，非 GAAP 營業利益率仍守在管理層 35–40% 區間上緣","2y":"2027 年非 GAAP 營業利益率 ≥38%","5y":null,"10y":null,"threshold":"非 GAAP 營業利益率 ≥38%","source":"8-K 財報新聞稿、每年 1 月全年指引","drift_rule":"2 年期：連 2 季偏離門檻 ≥5% 削弱、連 3 季 ≥10% 反轉"}],"R":[{"id":"R1","text":"器械單價侵蝕：延長使用計畫（2027 上半年起逐國上路）、中國 11 月起政策降價、XiR 與 X 低價機組合，加上 GLP-1 壓抑減重手術，同向拉低每台手術收入；管理層說的 SP、達文西 5 代與力回饋抵銷尚未量化（力回饋只用在 8% 的 5 代手術）","h_ref":"H1","clock":"🔥","threshold":"每台手術器械收入年減逾 4% 連兩季","evidence_refs":["competitive_share_entrants#1"]},{"id":"R2","text":"美國手術量降檔加競品入場：美國增速由第二季 12% 降到 10%；Hugo、Ottava 已可在美國銷售，Stryker 有模組化系統的消息；ACA 補貼、Medicaid 資格與 340B 變動是付款端壓力","h_ref":"H2","clock":"🔥","threshold":"美國達文西手術量年增 <8% 連兩季","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","substitute_technology#3"]},{"id":"R3","text":"器械售後市場被法院打開：SIS 案發回重審並聲請全院重審，醫院集體訴訟 4.5 億美元和解待核准，第三方再製器械持續挑戰","h_ref":"H1","clock":"🐢","threshold":"發回重審判決不利，或和解條款開放第三方再製器械","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","regulatory_antitrust#3","major_events#1","lawsuit_class_action#0","substitute_technology#4"]},{"id":"R4","text":"關稅與稀土：器械在墨西哥生產靠 USMCA 免稅，內視鏡在德國生產受關稅；2026 前九個月關稅成本 7,240 萬美元，另認列 IEEPA 退款 6,370 萬美元且後續不確定；Section 301 對 60 國加徵 10–12.5%；中國稀土出口管制可能斷料，部分零件單一來源","h_ref":"H3","clock":"⚡","threshold":"非 GAAP 毛利率扣退款 <68% 連兩季","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#4","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R5","text":"產品安全：2026 年兩起 Class II 召回，公民請願要求達文西 5 代 Class I 召回","h_ref":"H2","clock":"🐢","threshold":"FDA Class I 召回或警告信","evidence_refs":["major_events#3","major_events#4","product_recall_warning#0","product_recall_warning#1"]}],"single_thing":{"description":"SIS 反壟斷案全院重審被駁回，發回重審後認定公司在器械售後市場具獨占力，法院要求開放第三方再製與維修","why_fatal":"器械配件約占營收 59%、是利潤主來源；封閉售後市場一打開，每台手術器械收入可能被第三方以低價分走，影響遠大於公司自己宣布的 3–5% 降價","if_happens":"Base 機率移入 Bear，持有者清倉；未持有則撤銷進場條件、重跑判斷","how_monitor":"第九巡迴全院重審聲請結果（2026-09-28 提出）、客戶集體訴訟和解的法院核准條款（管理層稱 2027 年裁定）","probability":"約 10%（12–24 個月內出現不利判決；重審聲請未決、發回後仍需重新審理，客戶集體訴訟已和解）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":35.32,"peg_fy2":2.83,"stress":{"pass":3,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":10.8,"FY2027E":12.12,"FY2028E":13.67},"fy_end_month":12,"eps_basis":"非 GAAP 稀釋 EPS（Koyfin 共識）；FY2025 非 GAAP 實際值事實表未涵蓋（GAAP 7.87 美元口徑不同不得混用），三年 CAGR 以 FY2026→FY2028 兩年年化 12.5% 代理"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ISRG_20261022/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"裝機帶耗材年金、毛利率約 69%、零負債、經常性收入 84%"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：手術量由微創滲透與新適應症驅動（海外良性手術年增 41%、SP 年增 55%），不是庫存或資本支出週期；美國增速放緩至 10% 是降溫訊號","bargaining":{"up":"上游議價弱但金額小：部分零件單一來源、以採購單購料，稀土依賴中國","down":"下游醫院裝機後耗材鎖定，議價權在公司；例外是中國集中招標與成本敏感的 ASC 客群","geo":"美國占營收 68%；中國政策壓價；器械在墨西哥生產依賴 USMCA 免稅"},"profit_pool_dir":"利潤池仍集中在公司的器械配件環節，公司主動讓出 3–5% 單價換滲透，中國由政策強制讓利","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率；管理層稱 2027 年 1 月更新軟組織長期機會估計，屆時再展開"}},"moat":{"mechanism":"裝機基數＋醫師訓練與臨床證據＋器械配件只能用在自家系統的封閉耗材，醫院換平台要重訓團隊、重建流程","execution":9,"pricing":8,"grade":"A","trend":"→","trend_evidence":"執行力擴大：第三季裝機年增 28%、扣退款毛利率年增 0.9 個百分點、達文西 5 代逾 2,000 台；定價權縮減：2027 年器械降價 3–5%、中國 11 月政策降價。兩向相抵為持平","peer_na_reason":"同業 ROIC 與 Fwd P/E 事實表未涵蓋，只用利潤率對照","threats":[{"level":"🔴","text":"中國：本土機器人競爭、集中招標、政策降價，2025 年裝機少於預期、2026 年第二季只裝 2 台，11 月起器械價格大幅下調","p":"60%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#2"]},{"level":"🟡","text":"美國：Medtronic Hugo（2025-12 泌尿許可、2026-02 美國首例、一般外科與婦科已送件）與 J&J Ottava（據報 2026 年中十項一般外科許可）切入良性手術與 ASC；目前仍屬點對點，尚無份額數據","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#3"]},{"level":"🔴","text":"售後市場：第三方再製器械與維修，SIS 案發回重審、醫院集體訴訟以 4.5 億美元和解待核准；若被迫開放，器械配件封閉性受損","p":"20%","evidence_refs":["substitute_technology#4","regulatory_antitrust#0","regulatory_antitrust#2","regulatory_antitrust#3","major_events#1","lawsuit_class_action#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（外科醫師，逾 18,000 人用過達文西 5 代）、決策者（醫院與 IDN，已開始用即時儀表板比較機器人與腹腔鏡的成本與結果）、付款者（保險與政府）三環都成立；良性手術大型統合分析顯示轉開腹機率較腹腔鏡低 54%。付款端有 ACA 補貼到期、Medicaid 資格變動的短期壓力"},{"item":"決策層級","level":"🟡","text":"替代要在醫院手術室層級衡量：已建立機器人計畫的醫院換平台要重訓團隊、重建流程，轉換成本高；但美國約 70% 新系統採租賃、約半數裝機是換機，降低了換平台的資本門檻，ASC 客群更看單台成本"},{"item":"價值鏈分配","level":"🟡","text":"公司拿走手術機器人價值鏈大部分利潤（營業利益率比同業高約 10 個百分點），付款端與中國政府已在要回：中國政策降價、公司主動對高量良性手術降價 3–5%"},{"item":"社會容忍度","level":"🟡","text":"社會天花板已在作用：醫院買方反壟斷集體訴訟以 4.5 億美元和解、SIS 案發回重審、中國以政策壓價；公司選擇不把價格推到經濟上限，用延長器械壽命讓利，屬保費性質"}],"roiic":"事實表未涵蓋（投入資本、折舊攤銷、營運資金變動皆缺）","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；本包缺投入資本，改以代理：2022→2025 營收年化 17.4%，期間唯一收購為 2026 年南歐經銷權約 5.28 億美元，成長幾乎全屬內生"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","ISRG":66.68,"MDT":65.01,"SYK":64.98,"BSX":69.92,"unit":"%"},{"metric":"營業利益率","ISRG":31.28,"MDT":19.04,"SYK":21.73,"BSX":21.0,"unit":"%"},{"metric":"FCF 利潤率","ISRG":29.21,"MDT":16.33,"SYK":18.2,"BSX":8.6,"unit":"%"},{"metric":"研發密度","ISRG":12.82,"MDT":7.77,"SYK":6.42,"BSX":10.25,"unit":"%"}],"competitors":[{"name":"MDT","gm":65.01,"om":19.04,"fcf_margin":16.33,"rd_intensity":7.77,"strategy_note":"Hugo 以泌尿適應症切入美國，一般外科與婦科已送件；營業利益率 19.0%，規模大但機器人業務仍早期","period":"TTM ending 2026-07-31（4季加總）"},{"name":"SYK","gm":64.98,"om":21.73,"fcf_margin":18.2,"rd_intensity":6.42,"strategy_note":"法說問答提及 Stryker 與 CMR 的消息，可能帶模組化系統進 ASC；營業利益率 21.7%","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BSX","gm":69.92,"om":21.0,"fcf_margin":8.6,"rd_intensity":10.25,"strategy_note":"非軟組織手術機器人直接對手，毛利率 69.9% 與 ISRG 相近但 FCF 利潤率只有 8.6%，作利潤率對照","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（手術量 14–15%、裝機 28%），價轉負（2027 年組合不變下 −3～−5%），回購為輔（淨回購約 1%）","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本事實表未涵蓋；代理為 2022–2025 營收年化 17.4% 且無大型收購，共識 EPS 兩年年化 12.5% 在代理之內","segments":[{"item":"器械配件","value":"第三季 18 億美元，年增 18%，約占營收 59%；每台手術約 1,860 美元"},{"item":"系統","value":"第三季 7.69 億美元，年增 30%；購買 ASP 約 160 萬美元持平"},{"item":"服務","value":"第三季 4.82 億美元，年增 22%"},{"item":"Ion","value":"裝機 1,152 台年增 21%，手術量年增 31%"}],"decay_signals":["核心市占近 12 個月縮減：中國 2025 年裝機少於預期、2026 年第二季只裝 2 台，本土機器人競爭與招標政策","SBC 占營收逾 5%：第三季 7.0%，全年估 8.6–8.7 億美元；是否逐年上升事實表未涵蓋","未亮：毛利率（扣退款年增 0.9 個百分點）、EPS 與營收成長差距（25% 對 22%）、FCF 對淨利（2025 年 0.87）"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，唯一收購為南歐經銷權約 5.28 億美元，現金主要用於回購"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"唯一收購為南歐經銷權約 5.28 億美元，約市值 0.35%，已實現報酬事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"第三季均價 377 美元，對 FY2026 共識 EPS 10.80 美元的收益率約 2.9%；十年公債殖利率事實表未涵蓋，但需低於 0.9% 才會通過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"全年 SBC 約 8.65 億美元除以市值約 1,512 億美元約 0.6%，且回購金額遠大於 SBC","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2026 非 GAAP 共識）＋PEG","tier":"高成長醫材","peers":{"expanded":false,"reason":"事實表只有同業利潤率，無同業前瞻本益比；前份以高成長醫材約 28 倍作錨，本次無法重驗"},"fwd_pe":39.64,"peg":3.17,"percentile_5y":0.0,"val_light":"🟠","val_light_derivation":"PEG 3.2（FY2026 口徑，CAGR 用 FY2026→FY2028 兩年年化 12.5%）大於 2 屬貴；但本益比在自身四個年度端點的分位為 0（非連續五年序列），不到最貴一檔，判 🟠。短期以 FY2027 Base 12.0 美元乘 34 倍得 408 美元，−4.7%；中期（三年）以 FY2029 Base 14.9 美元乘 32 倍得 477 美元，+11.4%","upside_short_pct":-4.7,"upside_mid_pct":11.4},"trap_analysis":{"verdict":"🟡","label":"兩項衰退訊號：中國市占流失、SBC 占營收逾 5%"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Ottava 2026 年中獲 FDA 十項一般外科許可、Hugo 2025-12 獲泌尿許可並於 2026-02 完成美國首例；中國本土競爭使裝機少於預期；美國達文西增速 10%，為疫情後最低","assumption":"美國醫院在成本敏感的良性手術與 ASC 會選低價第二平台","consequence":"美國手術量增速降到 5–7%，降價又沒換到量，盈餘五年只增約 2%，倍數壓到 22 倍，股價約 264 美元、五年虧近四成；再疊加售後市場開放（獨立於此故事的唯一致命點）才會到虧五成","ruling":"部分採納：競品拿到許可是事實，但第三季美國系統裝機年增 27%、美國淨新增裝機年增 41%，醫院仍在擴產能；Bear 機率取 30% 而非更高","watch":"美國達文西手術量年增率，連兩季低於 8% 即成立","evidence_refs":["substitute_technology#1","substitute_technology#0","competitive_share_entrants#0"],"fact_refs":["f_kpi7_da_vinci_installed_base_"]},{"view":"論點成功但股東經濟變差","evidence":"CFO：營業利益率合理區間 35–40%，現在 41–42%，有投資的空間；2027 年器械降價 3–5%；全年 SBC 8.6–8.7 億美元","assumption":"手術量照計畫成長，但公司把超額利潤再投入研發、海外擴張與降價","consequence":"營收年增十幾 %、營益率回落到 38%，每股盈餘成長落後營收，股東拿到較低的利潤率","ruling":"採納：Base 路徑已把 2027–2028 年盈餘放在共識略下（12.0／13.4 美元對 12.12／13.67 美元）","watch":"2027 年 1 月指引的非 GAAP 營業費用成長是否高於營收成長","evidence_refs":[],"fact_refs":["f_kpi1_non_gaap_operating_incom","f_kpi5_sbc_gaap","f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"價格已反映太多","evidence":"前瞻本益比 39.6 倍、PEG 3.2；賣方平均目標價由上半年約 620 美元降到 477–539 美元，Evercore 降到 430 美元、BofA 降到 520 美元","assumption":"市場仍以高成長醫材上緣定價","consequence":"即使盈餘照共識，倍數回到 32 倍，五年 Base 年化只有約 7%","ruling":"採納：這是現在不進場的主因，進場條件綁價格","watch":"股價對 FY2027 共識的倍數是否降到 29 倍以下","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"2026 年兩起 Class II 召回（機械臂螺絲、病人側推車煞車銷）；2 月有團體請願要求對達文西 5 代 Class I 召回並發警告信","assumption":"安全事件升級成全系統召回或警告信","consequence":"新機裝機暫停、醫院延後採購，達文西 5 代換機週期中斷","ruling":"反駁：兩起皆為 Class II，未見 FDA 警告信，請願只是請求、FDA 未回應；第三季達文西 5 代裝機 315 台未見影響","watch":"FDA Class I 召回或警告信","evidence_refs":["major_events#3","major_events#4","product_recall_warning#0","product_recall_warning#1"],"fact_refs":[]}],"max_dd":{"lo":-48,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 358.97 → 本次 428.12（+19.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=358.97","side_b":"本次 price_at_dd=428.12","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 358.97 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 358.97 美元：Bull 價 770、Bear 價 280，五年期望值 +47.9%，基準年化 10.8%，不對稱比 3.5","side_b":"本次情境、股價仍用 358.97 美元：Bull 價 792、Bear 價 264，五年期望值 +49.4%，基準年化 9.9%，不對稱比 3.8","ruling":"先換情境、股價不動：五年期望值多 1.5 個百分點，基準年化少 0.9 個百分點。不對稱比由 3.5 變為 3.8。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 358.97 美元：五年期望值 +49.4%，基準年化 9.9%，不對稱比 3.8","side_b":"本次情境、股價 428.12 美元：五年期望值 +25.3%，基準年化 6.1%，不對稱比 1.85","ruling":"再換股價、情境不動：起點價上漲 19.3%，五年期望值少 24.1 個百分點，基準年化少 3.8 個百分點，不對稱比由 3.8 降到 1.85。合計五年期望值比前份少 22.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與裁決（價格變動）","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 358.97 美元，估值判貴（🟠），裁決觀望","side_b":"本次：股價 428.12 美元，漲約 19%，FY2026 共識只上修 3.65%，前瞻本益比升到 39.6 倍；估值結論仍判貴，未到最貴一檔","ruling":"估值結論維持；價格漲幅大於盈餘上修，離進場價更遠，裁決與角色預期不變，由程式依矩陣確認","evidence_level":"事實表","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若股價跌到 350 美元以下則重跑判斷、首倉 ≤2%","若股價續漲到 480 美元以上而盈餘未上修則不追"],"evidence_refs":[]},{"axis":"價值陷阱評級","cause":"新證據","prior_field":["trap"],"side_a":"前份：🟢，無衰退訊號","side_b":"本次：🟡，亮兩項——中國市占流失（2025 年裝機少於預期、第二季只裝 2 台、11 月政策降價）、SBC 占營收 7.0%","ruling":"採 🟡：中國流失有 10-K 與法說原話支持；SBC 比率逐年趨勢事實表未涵蓋，保守計入","evidence_level":"10-K／法說","settle_metric":"中國手術量與裝機","if_then":["若中國手術量轉負則停止加碼","若中國綠色通道核准達文西 5 代且裝機回升則撤回該訊號"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"axis":"情境機率","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份：Bull 22%、Bear 33%","side_b":"本次：Bull 25%、Bear 30%","ruling":"第三季營收增 22%、全年手術量指引收窄到 14–15%、毛利率指引上調，且延長使用計畫量化為 3–5%，低於市場擔心的 5–7%；但美國增速降到 10%、Ottava 已獲准，Bear 只降 3 個百分點、仍守 30%","evidence_level":"8-K／法說","settle_metric":"2027 年手術量指引","if_then":["若 2027 年手術量指引中點低於 12% 則 Bear 調回 35% 以上","若美國手術量連兩季回到 12% 以上則上調 Bull"],"evidence_refs":["substitute_technology#1"]},{"axis":"護城河方向、跑道、總評","cause":"新證據","prior_field":["moat_trend","runway_post_y5","signal"],"side_a":"前份：護城河持平、五年後跑道中等、總評 B","side_b":"本次：三項不變","ruling":"新證據雙向：裝機年增 28%、達文西 5 代逾 2,000 台支持執行力；降價、中國、競品許可壓定價權，相抵後方向不變；滲透率仍無數據，跑道維持中等","evidence_level":"8-K／法說","settle_metric":"同業營益率差距與美國手術量","if_then":["若同業營益率差距連兩期收窄則護城河方向改為縮減並重跑","若海外良性手術維持 35% 以上成長且 1 月更新的長期機會上調則跑道改寬"],"evidence_refs":[]},{"axis":"最大回撤、類型、循環位置","cause":"方法變動","prior_field":["max_dd_pct","archetype","cycle_position"],"side_a":"前份：最大回撤單點 −45%；品質複利成長；不適用循環位置","side_b":"本次：回撤改給範圍 −30%～−48%；類型與循環位置不變","ruling":"規格改為範圍、寬度至少 10 個百分點；下緣取 Bear 路徑中途倍數壓到 20 倍（FY2027 Bear 11.4 美元乘 20 倍為 228 美元）","evidence_level":"推算","settle_metric":"無","if_then":["若售後市場判決不利則以下緣 −48% 作倉位上限依據"],"evidence_refs":[]},{"axis":"進場條件（首倉）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"PEG（FY26 基準）≤ 2.0。今日解＝股價 ≤ $348；或 FY26 共識 EPS 上修至 ≥ $10.75 而價不變。無附加條件。","side_b":"股價 ≤ $350（約 FY2027 共識 EPS 12.12 的 29 倍）；或 FY2027 共識升至 ≥ $14.7 而股價不變","ruling":"首倉進場條件改錨 FY2027：FY2026 只剩一季，已不是前瞻分母；舊條件的 FY2026 EPS 10.75 美元已達成，但股價同時漲到 428 美元，PEG 仍 3.2，未觸發。新門檻 350 美元對應 Base 五年年化約 11%","evidence_level":"事實表","settle_metric":"股價／FY2027 共識","if_then":["若股價跌到 350 美元以下則重跑判斷、首倉 ≤2%","若 FY2027 共識下修 5% 以上則門檻價同比例下移"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）","side_b":"美國手術量連兩季低於 8% 減碼；器械每台手術收入低於 1,780 美元減碼；非 GAAP 營益率低於 35% 減碼；SIS 發回重審認定售後市場獨占則清倉","ruling":"本次新增：延長使用計畫已量化，能把前份風險文字轉成可監測門檻","evidence_level":"法說","settle_metric":"各季財報","if_then":["任一減碼門檻觸發則減碼一半","SIS 不利判決則清倉"],"evidence_refs":["regulatory_antitrust#2"]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"SIS 反壟斷案全院重審被駁回、發回重審認定售後市場獨占並要求開放第三方再製與維修","ruling":"新證據：第九巡迴 2026-08 撤銷原判並發回，公司 2026-09-28 聲請全院重審；器械配件約占營收 59%，是數學上最大的單一敏感項。發生則清倉","evidence_level":"法院判決報導","settle_metric":"全院重審裁定","if_then":["若全院重審准許並恢復原判則風險降級","若發回重審判決不利則清倉"],"evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3"]},{"axis":"假設與風險改寫","cause":"新證據","prior_field":["H","R"],"side_a":"前份 H3 是倍數維持 28–34 倍；R1 延長使用計畫量級管理層兩次拒答","side_b":"本次 H3 改為營益率 ≥38%；R1 改用已量化的 3–5%；新增關稅供應鏈與產品安全兩條風險","ruling":"倍數不是公司能交付的假設，改放進場條件；延長使用計畫第三季已量化，風險改寫成可監測門檻","evidence_level":"法說","settle_metric":"無","if_then":["若 2027 年 1 月指引營益率低於 38% 則 H3 判削弱"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：Ottava、Hugo 在美國可銷售，中國本土競爭與招標政策壓價","side_b":"結構轉好：海外良性手術年增 41%、美國淨新增裝機年增 41%、ASC 兩季裝機超過過去近三年；其他結構變數：售後市場反壟斷、關稅","ruling":"雙向拉鋸：競爭在中國已見份額影響，在美國只有許可、尚無份額數據；需求面擴張仍有手術量支持","evidence_level":"10-K／法說／新聞","settle_metric":"美國手術量與中國裝機","if_then":["若美國手術量連兩季低於 8% 則改判競爭惡化中"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#1"]},{"axis":"降價換滲透（可調和）","cause":null,"prior_field":null,"side_a":"管理層：降價集中在高量良性手術，2020 年第一次延長使用計畫的資料證明有彈性，量會回來","side_b":"2026-07-16 CFO 兩次拒答量級（not ready to quantify it yet）；美國增速 10% 為疫情後最低，降價時機與放緩重疊","ruling":"可調和、程度差異：本次已給 3–5%，小於 2020 年的 7%，管理層並承諾用成本下降抵銷毛利率影響；採信方向，但量的回應要到 2027 下半年才看得到，Base 盈餘放在共識略下","evidence_level":"法說","settle_metric":"2027 年美國良性一般外科手術量增速","if_then":["若 2027 下半年美國手術量回到 12% 以上則上調 Bull","若降價上路後兩季美國手術量仍低於 10% 則減碼一半"],"evidence_refs":[]},{"axis":"管理層承諾兌現（一致）","cause":null,"prior_field":null,"side_a":"2026-07-16 IR：全年手術量 13.5–15.5%、靠近中點；毛利率 68–69%；延長使用計畫下次量化","side_b":"2026-10-20：收窄到 14–15%、靠近中點；毛利率上調到 68.7–69.3%；延長使用計畫已量化 3–5%","ruling":"一致：三項承諾都兌現，管理層信用不扣分","evidence_level":"法說","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"反壟斷：和解與發回重審","cause":null,"prior_field":null,"side_a":"管理層：與美國客戶集體訴訟無過失和解，提供確定性","side_b":"SIS 競爭者案 2026-08 被第九巡迴發回，公司 2026-09-28 聲請全院重審；和解只涵蓋客戶集體訴訟，和解所稱第三方再製與維修的合作框架條款未公開","ruling":"不可調和於確定性這一點，選 B 側：客戶求償金額已封頂在 4.5 億美元，但售後市場能否被開放仍未決，風險保留於唯一致命點","evidence_level":"法說／法院判決報導","settle_metric":"法院核准的和解條款、全院重審裁定","if_then":["若和解條款允許第三方再製器械普遍使用則減碼一半","若全院重審推翻合議庭判決則售後市場風險降級並重跑"],"evidence_refs":["regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"第三季營收增 22%、非 GAAP EPS 增 25%，營益率 41.6%，零負債，第三季以均價 377 美元回購 29 億美元；本益比是自身近四個年度端點最低；賣方 27 人中 23 人給買進","side_b":"同樣的盈餘只值 32 倍時，Base 五年年化約 7%；價格要到 350 美元附近才有 11% 以上","ruling":"不採：好生意，但現價的五年報酬不夠；不追、等價格","evidence_level":"事實表／賣方彙整","settle_metric":"股價","if_then":["若股價跌到 350 美元以下則重跑判斷、首倉 ≤2%","若股價續漲而 FY2027 共識未上修則不追"],"evidence_refs":["capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"美國達文西手術量年增率連兩季跌破 8%","type":"假設驗證","maps_to":"H2","metric":"美國 da Vinci 手術量 YoY","threshold":"<8% 連兩季","action":"撤銷進場條件；持有者減碼一半","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":2,"text":"延長使用計畫上路後器械每台手術收入守不住","type":"假設驗證","maps_to":"H1","metric":"da Vinci 器械配件每台手術收入","threshold":"<1,780 美元（2027 下半年任一季）","action":"減碼","source_freq":"法說／每季","date":"2027-07","evidence_refs":[]},{"n":3,"text":"營業利益率跌出管理層區間","type":"假設驗證","maps_to":"H3","metric":"非 GAAP 營業利益率","threshold":"2027 全年 <38%；單季 <35%","action":"低於 38% 停止加碼；低於 35% 減碼","source_freq":"8-K 財報新聞稿／每季","date":"2027-01","evidence_refs":[]},{"n":4,"text":"SIS 案全院重審裁定與發回重審結果","type":"Single Thing","maps_to":"Single Thing","metric":"第九巡迴全院重審裁定","threshold":"駁回重審並進入發回重審；發回後判決不利","action":"駁回時不追；發回後判決不利則清倉","source_freq":"法院公告／事件","date":"2027-01","evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3"]},{"n":5,"text":"關稅與稀土供應吸收失敗","type":"風險","maps_to":"R4","metric":"非 GAAP 毛利率（扣關稅退款）","threshold":"<68% 連兩季，或公告稀土出口許可造成出貨延遲","action":"停止加碼","source_freq":"季報／每季","date":"2027-04","evidence_refs":["reg_tariff_export#1","geo_supply_chain#2"]},{"n":6,"text":"股價回到進場區","type":"估值rearm","maps_to":"進場條件","metric":"股價／FY2027 共識 EPS","threshold":"股價 ≤350 美元（約 29 倍）","action":"重跑判斷後首倉 ≤2%","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":7,"text":"第四季財報、2027 年指引與軟組織長期機會更新","type":"複審日期","maps_to":"H1/H2/H3","metric":"2027 年手術量與營業費用指引","threshold":"手術量指引中點 <12%","action":"重跑判斷","source_freq":"法說／一次","date":"2027-01","evidence_refs":[]},{"n":8,"text":"中國器械降價 11 月生效後的實際影響","type":"風險","maps_to":"R1","metric":"中國手術量與器械收入","threshold":"中國手術量轉負","action":"停止加碼","source_freq":"法說／每季","date":"2027-01","evidence_refs":["competitive_share_entrants#1"]}],"kill_metrics":[{"metric":"美國 da Vinci 手術量年增率","bear_threshold":"<8% 連兩季","window":"2026Q4–2027Q4","source":"公司季報新聞稿","last_status":"warning"},{"metric":"da Vinci 器械配件每台手術收入","bear_threshold":"<1,780 美元","window":"2027 全年","source":"每季法說 CFO 發言","last_status":"ok"},{"metric":"非 GAAP 營業利益率","bear_threshold":"<35%（管理層區間下緣）","window":"任一連續四季","source":"8-K 財報新聞稿","last_status":"ok"},{"metric":"SIS 反壟斷案","bear_threshold":"發回重審認定器械售後市場獨占","window":"2027–2028","source":"第九巡迴與地方法院公告","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=-2.94, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"4%","requires_critic":[],"rearm_trigger":"股價 ≤ $350（約 FY2027 共識 EPS 12.12 的 29 倍）；或 FY2027 共識升至 ≥ $14.7 而股價不變","exec_line":"觸發後先重跑判斷；首倉 ≤2%，2027 年 1 月指引確認營益率 ≥38% 且美國手術量 ≥8% 後加到 4%；不追高"},"reasoning":{"industry":"錢從醫院來：先賣或租出系統，之後每台手術買器械與配件、每年付服務費。第三季營收 30.49 億美元、年增 22%，其中 84% 是經常性收入；器械配件 18 億美元（年增 18%，約占 59%）、系統 7.69 億美元（年增 30%）、服務 4.82 億美元（年增 22%），分部數字取自 2026-10-20 法說 CFO 發言。非 GAAP 營業利益率 41.6%，GAAP 只有 19.4%，差額主要是 4.5 億美元反托拉斯集體訴訟和解費（待法院核准）。錢卡在每台手術的器械單價：達文西器械配件每台手術約 1,860 美元（去年 1,800 美元），公司已宣布延長使用計畫加中國政策降價，組合不變下每台手術收入降 3–5%，2027 年逐季累積。單點依賴：沒有單一大客戶，美國占營收 68%（FY2025 10-K）；真正的單點是器械售後市場的封閉性，也正是反壟斷訴訟攻擊的位置。產業處於擴張期：第三季全球裝機 546 台年增 28%、裝機基數 12,094 台年增 12%。供需耐久性：結構性持久，手術量由微創滲透驅動（海外良性手術年增 41%），不是庫存週期；但美國增速已由第二季 12% 降至 10%。","moat":"機制：裝機基數加醫師訓練（達文西 5 代已有逾 18,000 位醫師使用）加 48,000 篇同儕審查文獻，加上器械只能用在自家系統，醫院換平台要重訓整個團隊。可證方向用同業利潤率差代替 ROIC 差（事實表無投入資本）：近四季營業利益率 31.3%，對 SYK 21.7%、BSX 21.0%、MDT 19.0%，領先最強同業約 9.6 個百分點；FCF 利潤率 29.2% 對 8.6–18.2%。只有一期數據，差距是否擴大事實表未涵蓋。執行力在擴大：第三季裝機年增 28%，美國第一季達文西 5 代占系統裝機 85%，非 GAAP 毛利率扣除關稅退款仍年增 0.9 個百分點。定價權在縮：公司主動對高量良性手術降價、中國 11 月起政策降價，管理層稱是用單價換滲透。兩向相抵判持平。執行 9 分、定價權 8 分；若同業營益率差距下兩期連續收窄就要下調。","growth":"成長以量為主：2026 年手術量指引 14–15%，系統裝機年增 28%；價格轉為負貢獻（2027 年器械降價 3–5%，管理層稱 SP、達文西 5 代與力回饋器械會抵銷，但未量化）；回購是第三項，第三季買回 29 億美元。共識每股盈餘 FY2026 10.80、FY2027 12.12、FY2028 13.67 美元，兩年年化 12.5%；FY2025 非 GAAP 實際值事實表未涵蓋，三年 CAGR 無法依規格計算，改用兩年代理。內生上界：投入資本與再投資率事實表未涵蓋，無法算增量報酬；代理是 2022–2025 營收年化 17.4%，期間唯一收購是南歐經銷權約 5.28 億美元，成長幾乎全屬內生。共識 12.5% 低於此代理，缺口可由量增減降價、營益率持平、約 1% 淨回購解釋，不依賴重新評價。跑道：滲透率事實表未涵蓋；管理層稱 ASC 滲透在第一個四分位、心臟手術可見機會每年 30–40 萬例、海外良性手術占國際量四分之一且缺口最大，Ion 手術量年增 31%，但這些第二曲線相對總量仍小，美國增速由 12% 降到 10%，判中等。","governance":"現金轉換：2025 年自由現金流 24.9 億美元、淨利 28.6 億美元，轉換率 0.87；2023–2024 年只有 0.42–0.56，因建廠資本支出；2026 前九個月自由現金流 28.7 億美元。SBC 第三季 2.13 億美元、占營收 7.0%，全年估 8.6–8.7 億美元，約市值 0.6%，被回購完全抵銷。現金去向：第三季回購 29 億美元、均價 377 美元，第二季 3.79 億美元、均價 439 美元；南歐經銷權收購約 5.28 億美元；第三季資本支出 1.13 億美元；季底現金 68 億美元、零負債。以 377 美元計算的盈餘收益率約 2.9%（FY2026 共識 10.80 美元除以 377 美元），十年公債殖利率事實表未涵蓋，但要低於 0.9% 才會通過，此項判不過；收購金額小且已實現報酬事實表未涵蓋，不適用；SBC 淨稀釋低於 1.5%，通過。","valuation":"現價 428.12 美元，是 FY2026 共識 10.80 美元的 39.6 倍、FY2027 共識 12.12 美元的 35.3 倍。要划算，市場得相信五年每股盈餘年增約 11–12%，而且 2031 年仍給 32 倍以上。前半我信：共識兩年年化 12.5%，近三個月 FY2026 共識上修 3.65%，第三季優於預期。後半不信：公司自己把每台手術器械單價降 3–5%，美國增速 10%，J&J 與 Medtronic 已在美國拿到許可，倍數要維持 35 倍以上需要成長回到 15% 左右。PEG 以兩年 CAGR 12.5% 計為 3.2（FY2027 口徑 2.8），屬貴。歷史對照：近四個年度端點的本益比、P/S、EV/S 分位都是 0，現價是自己歷史的低點，但只有四個點、不是五年連續序列。追蹤本益比 51.8 倍被 4.5 億美元和解費壓低分母，不採用，改看前瞻口徑。賣方平均目標價 477–539 美元，上半年曾在 620 美元左右，持續下修。同業前瞻本益比事實表未涵蓋，前份以高成長醫材約 28 倍作錨，本次無法重驗。","premortem":"三處：一是降價換滲透沒換到量，2020 年第一次延長使用計畫時管理層稱有彈性，但這次美國增速已降到 10%，若 2027 年美國良性一般外科不加速，單價與量會同時往下；二是競品用低價切入 ASC 與良性手術，Ottava、Hugo 都已可在美國銷售，Stryker 也有模組化系統的消息；三是售後市場被法院打開，SIS 案發回重審，若最終認定售後市場獨占並開放第三方再製，器械配件的封閉性就破了。三個反證視角都已寫進反證紀錄；衰退訊號亮兩項（中國市占、SBC 占營收），判 🟡。股價 26 週跌 2.9%、仍低於 104 週均線，市場已部分反映競爭擔憂。"},"plain":{"six":{"how_it_makes_money":"賣系統、收耗材年金：84% 經常性收入，錢卡在每台手術的器械單價","moat":"→ 持平：執行力擴大，定價權主動讓出一部分","growth":"🟡 五年後跑道中等：量還在長，但第二曲線相對總量仍小、價格轉為負貢獻","capital":"B：回購買得不夠便宜，SBC 稀釋輕","valuation":"現價要市場相信五年每股盈餘年增約 11–12% 且 2031 年仍給 32 倍以上；前半我信，後半不信","how_wrong":"🟡 最可能看錯在：降價沒換到量、競品在美國良性手術切入、售後市場被法院打開"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤350 美元（約 FY2027 共識 29 倍），或 FY2027 共識升至 ≥14.7 美元而股價不變","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟠","moat":"A","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":428.12,"week26_return_pct":-2.94,"consensus_rev_3m_pct":3.65,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"追蹤 GAAP 盈餘含 4.5 億美元一次性和解費，分母偏低；改用 FY2026／FY2027 非 GAAP 共識，分母不構成爭點"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"中國器械收費代碼政策降價生效","impact":"中","watch":"第四季中國手術量與器械收入"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"SP 血管閉合器美國送件","impact":"低","watch":"SP 手術量成長"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報、2027 年指引與軟組織長期機會更新","impact":"高","watch":"手術量指引中點、營業費用成長"},{"date":"2027-Q1","date_precision":"quarter","type":"regulatory","event":"美國延長使用器械 510(k) 許可與上路","impact":"高","watch":"每台手術器械收入"},{"date":"2027-Q2","date_precision":"quarter","type":"regulatory","event":"客戶集體訴訟和解法院核准與 SIS 案全院重審裁定（管理層稱 2027 年裁定，季度未定）","impact":"高","watch":"和解條款是否開放第三方再製器械"}],"_projected_from":"v19"}
```
