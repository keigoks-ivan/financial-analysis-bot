你是 stock-analyst v20 的**散文層（prose）agent**，標的 WDC（2026-10-13）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261013/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：WDC　日期：2026-10-13　archetype：None　前份裁決：2026-09-06　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1530B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（472B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1132B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（963B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（2375B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（371B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1156B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2410B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1480B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2424B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1530           3829-5470      5 條（2–6 內）  
s3                  8000         472           5270-7528      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4470          7371-10530      5 條（2–6 內）  
s6                 11000         371          7440-10629      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1156           1641-2344      3 條（2–6 內）  
s10                 5000        2410           1813-2590      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2424           2000-2576      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5574B；至少需散文≈39.43KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−72
−72%
−69%
−65%
−64%
−55
−55%
−17.2%
−17%
−6.4%
−5.37
−4.37%
−2.6%
−2.6
−0.7%
0
0%
0.1%
0.15
0.15%
0.2
0.25%
0.31
0.38
0.5
0.69
0.75
0.82
0.9
0.9%
1
1.08
1.2%
1.23
1.29
1.3
1.4%
1.8
1.87
2
02
2.1
2.25
2.9%
03
3
3.25
3.28
3.5
3.56
3.9%
3.9
4.00
04
4
4.2
4.37%
5%
5
05
5.2
5.3%
5.36%
6%
6
06
7.0%
07
7
7%
7.5
7.52
7.7
8%
08
8
9%
9
09
9.0
9.95
10%
10
10.22
11
11.2
12
12.16
12.2
12.5
12.81
13.0
13
13%
13.89
14
14.4
14.7
15
15%
15.6
16%
16
17%
17.2%
18
18.5
19.2
19.23
19.8
20.0%
20%
20
20.12
20.7
21
21.3
21.5
22%
22
22.6
22.6%
23
24
24.7
25
25%
26.92
27.2%
28
29
29.0
30
30%
31
31.83
32
32%
33
34%
34.5
35%
35.11
35.6%
36%
36
36.4
36.5
37.47
37.5
38%
38
38.5
40%
40
41
41.7%
42
42%
42.87
43%
44%
44
44.2%
46.0
46
48%
48
48.9%
49
49%
50%
51
52%
52
53%
54
54%
54.4%
55%
55
56%
57
57.5%
58
60%
60
61%
65%
67%
70
71.5%
73%
76%
76.3%
80%
84
85%
89%
90
102%
121
126%
129
137.5
138
156
200
230
231
232
250
259
290
292
$320
320
350
$350
360
377
380
386.94
387
467
467.46
475
480
480%
483
500
501
580
600
639
000660
900
928
2025
2026
2027
2028
2030
2031
005930
20261013
1,050
1,310
4,500
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
{"meta":{"ticker":"WDC","date":"2026-10-13","schema":"v15.2","contract":"v19","company_name":"Western Digital Corporation"},"oneliner":"HDD 漲價循環處於高檔：長約鎖住 2027 年，但 Toshiba 擬倍增產能、HAMR 落後 Seagate，2028 年後每 TB 價格方向成爭點；FY2028E 12 倍本益比建立在高峰毛利率上，Base 五年年化約 5%，不追，等 320 美元或長約鎖價證據。","thesis":{"H":[{"id":"H1","text":"AI 推論與代理式工作負載使雲端 EB 需求年增 ≥25%，WDC 出貨 EB 年增維持 ≥20%（供給受限下上限約 25%）","2y":"FY2027 出貨 EB 年增 ≥20%（Q4 FY26 為 22%，FY2026 全年 25%）","5y":null,"10y":null,"threshold":"出貨 EB 年增 <15% 連 2 季即削弱","source":"每季法說 EB 出貨量與年增率","drift_rule":"以年增 25% 為錨：連 2 季偏離 ≥5% 削弱、連 3 季 ≥10% 反轉"},{"id":"H2","text":"價格與成本剪刀差延續：CY2027 長約價格續漲、每 TB 成本年降約 10%，non-GAAP 毛利率站穩 55% 以上","2y":"FY2027 毛利率 ≥55%、每 TB 混合價格年增 >0","5y":null,"10y":null,"threshold":"non-GAAP 毛利率 <53% 或每 TB 價格年增 ≤0","source":"每季新聞稿毛利率；CFO 每 TB 價格與成本說明","drift_rule":"TTM 毛利率相對 55% 錨連 2 季偏離 ≥5% 削弱、連 3 季 ≥10% 反轉"},{"id":"H3","text":"技術路線不失守：40TB ePMR 於 FQ3 FY27 占近線 EB ≥50%，44TB HAMR 於 2027 上半年量產出貨，HDD 份額維持 ≥40%","2y":"ePMR 占近線 EB ≥50%（FQ3 FY27）、HAMR 2027-06-30 前出貨","5y":"HAMR 成為主力平台後份額不低於 40%","10y":null,"threshold":"HAMR 2027-06-30 前未出貨，或份額連 2 季 <40%","source":"法說產品進度；TrendForce／Coughlin 份額資料","drift_rule":"份額連 4 季偏離 ≥5% 削弱、連 6 季 ≥10% 反轉"}],"R":[{"id":"R1","text":"供給回應：Toshiba 擬倍增 HDD 產能、份額目標由約 10% 拉到 30%，可能以低價搶單；Toshiba 未證實，Citi 認為受碟片與磁頭外購限制。","h_ref":"H2","clock":"🔥","threshold":"Toshiba 正式公告擴產時程，且 WDC 每 TB 價格年增連 2 季降到個位數","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"]},{"id":"R2","text":"HAMR 落後與轉換風險：Seagate 已在兩家大型客戶量產，WDC 44TB 要到 2027 上半年；HAMR 有良率、可靠度與合約賠償條款風險，TrendForce 預估 Seagate 2028 年成最大供應商。","h_ref":"H3","clock":"🔥","threshold":"HAMR 2027-06-30 前未出貨，或份額連 2 季 <40%","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"id":"R3","text":"客戶集中：前十大客戶占 73%、三家合計 44%，集中度三年上升 18pp；單一客戶延後提貨或重談價格即影響當季。","h_ref":"H1","clock":"⚡","threshold":"單季營收季減 >10%，或任一大客戶公開延後提貨","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"id":"R4","text":"快閃長期替代：SanDisk、Samsung、Micron、Kioxia 的 QLC 企業級 SSD；目前每 TB 價差 5–10 倍，NAND 供給可能在 2027 下半年轉寬。","h_ref":"H1","clock":"🐢","threshold":"QLC SSD 與近線 HDD 每 TB 價差縮到 3 倍以內","evidence_refs":["competitive_share_entrants#4"]},{"id":"R5","text":"關稅與供應鏈：組裝集中泰國與馬來西亞、Section 232 第二階段可能課顯著關稅、磁頭獨立供應只剩 TDK、中國稀土逐案核准；公司稱已建立替代來源且關稅至今無重大影響。","h_ref":"H2","clock":"🔥","threshold":"non-GAAP 毛利率單季下滑 ≥200bp 且公司歸因關稅或零組件","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R6","text":"Kioxia 合併傳聞：2026-07 報導稱洽談，可能逾 200 億美元、以股票支付；來源日期不一致、未見協議，且 WDC 已把快閃業務分給 SanDisk，交易邏輯存疑。若成真，WDC 重回快閃循環並稀釋股權。反壟斷面：本輪反壟斷相關查詢（美國司法部、聯邦貿易委員會、歐盟）都沒有結果，屬資料缺口。快閃業務已分出，推論與 Kioxia 的直接重疊有限，但跨國交易仍須多地審查，時程與條件事實表未涵蓋。","h_ref":"H2","clock":"🐢","threshold":"簽署最終協議或公司公告","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"任一季法說揭露每 TB 混合價格年增轉負，代表本輪漲價週期結束","why_fatal":"EPS 路徑靠「價格漲＋成本年降約 10%」的剪刀差；價格轉為年降，毛利率停止擴張並回落，FY2029 共識 42.87 的前提失效，Bear 路徑 EPS 約為 Base 的三分之一。每 TB 價格是情境樹中數學上最大的單一敏感度項。","if_happens":"清倉，未持有者不建倉；Bear 機率上調至 ≥50%，重跑判斷","how_monitor":"每季法說 CFO 揭露的每 TB 混合價格年增（Q4 FY26 為高十幾%）；Seagate 同期定價說法；Toshiba 菲律賓產能時程","probability":"12–24 個月內約 20%：FY2027 絕大部分量已在長約下（CFO 2026-09-09），轉負較可能落在 CY2028 下半年以後"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.16,"peg_fy2":0.2,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":10.22,"FY2027E":20.12,"FY2028E":31.83,"FY2029E":42.87},"fy_end_month":6,"eps_basis":"non-GAAP 稀釋 EPS（持續營運）；FY2026A 10.22 取自 Q4 FY26 法說 CFO，GAAP 26.92 含 SanDisk 持股利益不採用；FY2026 季末為 2026-07-03"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/WDC_20261013/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營益率由 FY2023 −6.4%（含快閃業務）升至 FY2026 35.6%，振幅來自每 TB 價格隨供需擺動；第三名廠商以擴產回應；長約降低但未消除循環性。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉（約 CY2028）：TrendForce 稱雙寡頭轉 HAMR 後供需逐步趨近平衡、Toshiba 擬倍增產能；反方為 Morgan Stanley 稱加計 Toshiba 至 2028 仍短缺、CFO 稱營收受供給而非需求限制。產能售罄、價格年增加速、競爭者宣布擴產三者並存，屬過熱初段。","bargaining":{"up":"磁頭獨立供應商僅 TDK 一家（二手轉述），WDC 以自製磁頭與碟片為主，資本支出主要投向磁頭、媒體與自動化；CFO 2026-09-09 稱 DRAM 與 NAND 等投入成本上升。","down":"前十大客戶占 73%，三家各占 16%／15%／13%；但 HDD 只占超大規模業者資本支出 4–5%，客戶主動要求長約鎖量，目前賣方議價力偏強。","geo":"組裝集中泰國與馬來西亞（二手來源，未對照年報），面對關稅與原產地認定風險；中國中重稀土逐案核准，暫停期至 2026-11-10。"},"profit_pool_dir":"儲存與記憶體利潤池整體擴大：WDC 毛利率 48.9%（TTM），快閃與記憶體同業 SanDisk 71.5%、SK hynix 76.3%、Samsung 57.5%；WDC 營益率三年由 −6.4% 升至 35.6%。","tam_table":{"expanded":false,"reason":"HDD 為成熟寡占品類，論點不在滲透率或份額擴張而在每 TB 價格；事實表未涵蓋 TAM／SAM 金額與五年前利潤池占比，需求以 EB 年增衡量（管理層稱五年 >25%）。"}},"moat":{"mechanism":"三家寡占＋面密度技術門檻＋一年以上客戶認證週期＋多年長約鎖量；定價力目前來自供給緊張，非品牌或轉換成本。","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力偏縮：HAMR 量產落後 Seagate 約一年，TrendForce 預估 Seagate 2028 年成最大供應商；定價力擴大：每 TB 價格年增由高個位數升至高十幾%，長約延至 CY2029。份額 42–48% 未見下滑序列，兩軸方向相反，合併判穩定。若 2027 上半年 HAMR 未出貨或份額序列連兩季下滑，改判向下。","peer_na_reason":"事實表同業對照缺 Seagate、Toshiba 兩家直接 HDD 競爭者，表內為快閃與記憶體廠，利潤率差距不可解讀為護城河差距；Pure Storage 無財務資料。","threats":[{"level":"🟡","text":"Toshiba 擬於其 FY2027 前倍增 HDD 產能、容量份額目標由約 10% 拉到 30%，可能以低價搶單；Toshiba 未證實，Citi 認為受碟片與磁頭外購限制。","p":30,"evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"]},{"level":"🟡","text":"Seagate HAMR 已量產、WDC 44TB HAMR 要到 2027 上半年；HAMR 轉換另有良率、可靠度與客戶合約大規模瑕疵條款風險。","p":40,"evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"level":"🟡","text":"快閃長期替代：目前每 TB 價差 5–10 倍，雲端冷資料層未見架構替代；若價差縮到 3 倍內升級為架構替代。","p":15,"evidence_refs":["competitive_share_entrants#4"]},{"level":"🟡","text":"互補零件收斂：磁頭獨立供應只剩 TDK，中國稀土逐案核准；公司稱已建立替代來源。","p":15,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推論，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是超大規模業者，冷資料保存是需要而非想要；HDD 存放超大規模資料約 80%，每 TB 價格比 SSD 低 5–10 倍（公司說法經轉述）。代理讀數：管理層稱 EB 需求五年 >25%，CFO 稱目前看不到消化期。付款時點受資本支出節奏影響，但延後購買的代價是資料無處存放，延後空間有限。"},{"item":"決策層級","level":"🟡","text":"替代決策發生在每家客戶每代平台的認證，不在商品層：認證一年以上、長約多年，但客戶同時認證兩到三家，Seagate HAMR 已先在兩家大型客戶量產，換供應商的成本只是一個認證週期。代理讀數：長約只承諾低於需求的基礎量，上行量另議價。"},{"item":"價值鏈分配","level":"🟡","text":"HDD 只占超大規模業者資本支出 4–5%（CFO 2026-09-09），付款方對價格不敏感，有利 WDC 分得較多；但買方高度集中（前十大 73%），磁頭的獨立供應收斂到 TDK 一家，價值可能向上游與大客戶移轉。快閃與記憶體同業毛利率 57–76%，整條儲存價值鏈的利潤目前在記憶體端較厚。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的資本財，沒有消費者必需品的漲價政治壓力，也不依賴監管授權；政策風險在關稅與原產地認定（Section 232 第二階段未定），屬成本面而非社會容忍度上限。"}],"roiic":"淨值無法實算：投入資本、折舊攤銷與營運資金變動事實表未涵蓋。以下是可複算的界線。FY2025→FY2026 GAAP 營業利益由約 21.3 億增至約 46.0 億美元，增量約 24.7 億。FY2026 營收約 129 億，由營業利益 46.0 億 ÷ 35.6% 與自由現金流 35.11 億 ÷ 27.2% 兩路回推一致。FY2026 全年資本支出事實表未涵蓋，以長期區間 4–6% 代入，約 5.2–7.7 億；即使全數視為新增投入資本，增量報酬仍約 320–480%。營運資金增加未計入，實際值較低。增量主要來自漲價而非新投入資本，不作承重數字。","reinvest_rate":"毛再投資率約 7–17%（可複算，非淨值）。長期口徑：資本支出占營收 4–6%（CFO）÷ FY2026 GAAP 營益率 35.6%，約 11–17%。Q4 FY26 實際：資本支出 1.08 億美元 ÷ GAAP 營業利益約 15.6 億（37.47 億 × 41.7%），約 7%；當季資本支出只占營收約 2.9%，低於長期區間。分母用稅前營業利益，稅率事實表未涵蓋，改用稅後會讓比率上升；分子未扣折舊攤銷與營運資金變動，兩者事實表未涵蓋，所以淨再投資率會低於此值。CFO 稱未來兩年資本支出可能略高於 4–6%。管理層承諾超額自由現金流全數回饋，與再投資需求低一致。","endo_ceiling":25,"formula_note":"增量 ROIC × 再投資率在本例失真。照公式代入，兩者相乘等於營業利益增量 ÷ 本期營業利益（24.7 億 ÷ 46.0 億），約 54%，資本支出假設在乘積中互相抵銷。這只是把 FY2026 漲價帶來的獲利跳升重述一次，不代表可持續的內生成長。因此改用實體上界：EB 供給年增上限約 25%（CFO 2026-09-09：目前供給無法超過 25%）× 長期每 TB 價格持平，得出營收與 EPS 內生上界約 25%。公司選擇不擴單位產能、以面密度換成長，是用短期成長換持續期。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","WDC":48.85,"SNDK":71.47,"000660.KS":76.27,"005930.KS":57.48,"PSTG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","WDC":35.6,"SNDK":61.58,"000660.KS":68.04,"005930.KS":36.88,"PSTG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","WDC":27.18,"SNDK":56.77,"000660.KS":47.8,"005930.KS":28.95,"PSTG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","WDC":8.99,"SNDK":6.56,"000660.KS":4.93,"005930.KS":9.7,"PSTG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"SNDK","gm":71.47,"om":61.58,"fcf_margin":56.77,"rd_intensity":6.56,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"000660.KS","gm":76.27,"om":68.04,"fcf_margin":47.8,"rd_intensity":4.93,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"005930.KS","gm":57.48,"om":36.88,"fcf_margin":28.95,"rd_intensity":9.7,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"PSTG","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null}]},"growth":{"driver_mix":"量（EB 年增約 22–25%）＋價（每 TB 價格年增高十幾%）＋淨回購；無併購","runway_years":"不適用滲透率口徑：需求隨資料量複利（管理層稱五年 EB 年複合 >25%），HDD 已占超大規模資料約 80%，成長年限取決於價格循環而非滲透率","runway_post_y5":"🟡","endo_ceiling_basis":"EB 供給年增上限約 25% × 長期每 TB 價格持平 → 內生上界約 25%；共識三年 EPS 年複合約 61%，缺口約 36pp 歸因毛利率擴張（每 TB 價格漲、成本年降約 8–10%）與淨回購，無併購。","segments":[{"item":"雲端（Cloud）","value":"Q4 FY26 約 33 億美元，占 89%，年增 43%；FY2026 全年年增 38%"},{"item":"Client","value":"Q4 FY26 2.25 億美元，占 6%，年增 61%，主因漲價"},{"item":"Consumer","value":"Q4 FY26 1.87 億美元，占 5%，年增 38%，主因漲價"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q4 毛利率年增 1,310bp"},{"signal":"核心份額近 12 個月縮減","lit":false,"note":"42–48%，無下滑序列；TrendForce 預估 2028 年被 Seagate 超越屬預測"},{"signal":"提價後銷量下滑","lit":false,"note":"漲價同時 EB 年增 22%"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"共識三年 EPS 年複合約 61%，FY2026→FY2028 營收年複合約 43%，差逾 5pp"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":true,"note":"GAAP 口徑 FY2025 0.69、FY2026 0.38，但 GAAP 淨利含 SanDisk 持股利益，non-GAAP 口徑約 0.9，低權重"},{"signal":"SBC／營收 >5% 且上升","lit":false,"note":"1.2%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"快閃替代屬長期，每 TB 價差 5–10 倍"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"},{"signal":"維護性資本支出占 FCF >60%","lit":false,"note":"Q4 資本支出 1.08 億美元對 FCF 12.81 億"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"不擴單位產能但營收年增 36%"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自量價，非併購；資本回饋以回購為主、股利為輔，管理層承諾超額自由現金流全數回饋（Q3 法說、2026-09-09 Citi 會議 CFO），細節見計分卡"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年無收購；Kioxia 合併僅為來源日期不一致的報導，未見協議","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q3 FY26 買回 290 萬股、7.52 億美元（均價約 259 美元）；Q4 公開市場約 230 萬股、均價約 292 美元（10 億美元內含 3.28 億可轉債溢價）。以 FY2026 non-GAAP EPS 回算收益率約 3.5–3.9%，以現行 FY2027 共識回算約 7–8%；10 年期公債殖利率事實表未涵蓋，無法判斷是否過關","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 單季 4,500 萬美元（營收 1.2%、GAAP 營業利益 2.9%），年化約 1.8 億美元、約市值 0.1%；同期回購與 SanDisk 換股回收 480 萬股，流通股淨減少","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2027E／FY2028E 共識 non-GAAP EPS）；循環股優先尺為股價淨值比，但淨值事實表未涵蓋，改以 FY2028E 本益比交叉","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，缺同業前瞻倍數；直接競爭者 Seagate 與 Toshiba 不在表內，無法建立同級倍數錨"},"fwd_pe":19.23,"peg":0.31,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"表面便宜（FY2028E 12.2 倍），但分母在高峰毛利率上；Base 五年年化約 5%、上下行比約 1.3，不便宜也不貴，判黃。股價 ≤320 美元時 Base 年化約 9%、上下行比約 2，可轉綠。五年分位：事實表只有年度端點分位，不外推。","upside_short_pct":-2.6,"upside_mid_pct":22.6},"trap_analysis":{"verdict":"🟡","label":"高峰獲利陷阱：本益比低是因為分母在週期高點"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Toshiba 擬於其 FY2027 前倍增產能、份額目標 30%；TrendForce 稱雙寡頭轉 HAMR 後供需趨近平衡；WDC 營益率 FY2023 曾為 −6.4%。","assumption":"長約只鎖基礎量、上行量另議價，CY2028 後的價格機制仍可重談。","consequence":"五年後虧 50% 最可能的故事：CY2028 起 EB 供給增速超過 25%、超大規模業者進入消化期，每 TB 價格年降幅超過成本降幅，毛利率回到約 40%，EPS 自 30 美元以上落到 11–13 美元，市場給 11 倍，股價約 138 美元（−64%）。與唯一致命點是同一變數（每 TB 價格方向）。","ruling":"部分採納：長約延至 CY2027–29 讓崩價最早落在 CY2028 之後，Bear 機率 32% 而非過半。","watch":"每季每 TB 混合價格年增；Toshiba 擴產公告；Seagate 2027–28 定價說法","evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"],"fact_refs":["f_consensus_rev_fy3_pct"]},{"view":"論點成功但股東經濟變差","evidence":"Seagate HAMR 已在兩家大型超大規模客戶量產，WDC 要到 2027 上半年；HAMR 轉換有瑕疵與合約賠償條款風險；磁頭獨立供應只剩 TDK；CFO 稱未來兩年資本支出可能略高於營收 4–6%，DRAM／NAND 投入成本上升。","assumption":"AI 資料需求年增 25% 以上成立，但 WDC 分到的份額與每 TB 利潤不一定跟著。","consequence":"產業成長、WDC 份額讓給 Seagate、成本降幅停在 5–8%，毛利率停在 50% 出頭；同時回購在循環高檔大量買入，每股價值成長低於產業。","ruling":"採納為中度風險：反映在 Base 毛利率持平 58–60%（低於共識隱含水準）與 H3 份額門檻。","watch":"HAMR 首批出貨時點；份額序列；每 TB 成本年降幅；回購均價對照股價","evidence_refs":["competitive_share_entrants#2","substitute_technology#2","geo_supply_chain#1"],"fact_refs":["f_kpi5_non_gaap"]},{"view":"價格已反映太多","evidence":"Q4 FY26 營收與 EPS 優於預期，財報後股價仍跌 5.36%；共識 FY2029 EPS 42.87 粗估隱含毛利率約 60% 以上；前瞻 EV／營收 7.5 倍，P／S 11.2 倍在 4 個年度端點中位於 67%。","assumption":"市場用高峰獲利給倍數，而循環股的高峰本益比通常被壓低。","consequence":"即使每 TB 價格續漲到 FY2028，若市場提前定價供給回應，倍數由 FY2028E 12 倍壓到 9–10 倍，股價難漲。","ruling":"採納：這是不追的主因，Base 終端 13 倍、五年年化約 5%。","watch":"FY2028／FY2029 共識修正方向；財報後股價反應","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_ev_s_fwd","f_ps_percentile","f_consensus_eps_fy3"]}],"max_dd":{"lo":-72,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 467.46 → 本次 386.94（-17.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=467.46","side_b":"本次 price_at_dd=386.94","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 467.46 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 467.46 美元：Bull 價 928、Bear 價 156，五年期望值 +7.0%，基準年化 0.9%，不對稱比 1.23","side_b":"本次情境、股價仍用 467.46 美元：Bull 價 900、Bear 價 137.5，五年期望值 −0.7%，基準年化 1.4%，不對稱比 0.82","ruling":"先換情境、股價不動：五年期望值少 7.7 個百分點，基準年化多 0.5 個百分點。不對稱比由 1.23 變為 0.82。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 467.46 美元：五年期望值 −0.7%，基準年化 1.4%，不對稱比 0.82","side_b":"本次情境、股價 386.94 美元：五年期望值 +20.0%，基準年化 5.3%，不對稱比 1.29","ruling":"再換股價、情境不動：起點價下跌 17.2%，五年期望值多 20.7 個百分點，基準年化多 3.9 個百分點，不對稱比由 0.82 升到 1.29。合計五年期望值比前份多 13.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2028 年後供需方向（不可調和）","cause":null,"prior_field":null,"side_a":"結構性：CFO 稱營收受供給而非需求限制、EB 需求五年 >25%，客戶要求簽到 2030–31 年長約；Morgan Stanley 認為加計 Toshiba 新產能至 2028 仍供不應求，Citi 認為 Toshiba 受碟片與磁頭外購限制。","side_b":"週期性：Toshiba 擬於其 FY2027 前倍增產能、份額目標 30%；TrendForce 稱雙寡頭轉 HAMR 後供需逐步趨近平衡；Seagate 執行長稱 2027–28 新產能上線後價格「持平至小幅上漲」；FY2029 共識最近一次下修 4.37%。","ruling":"⚖ 選中間偏週期側：CY2027 價格大致鎖定（CFO：FY2027 絕大部分在長約下），CY2028 起每 TB 漲幅收斂至持平，Base EPS 低於 FY2029 共識約 20%。依據：長約只承諾低於需求的基礎量、上行量另議價（Q4 法說執行長），CY2029 後長約的價格機制管理層仍在談；擴產消息後遠年共識已先下修。利空出現不到一季，只部分進入賣方模型，凍結加碼直到第一個確認數據點。","evidence_level":"雙方皆為管理層說法或二手轉述，無 CY2028 實際價格資料；不可裁決至 2027 年中長約價格揭露","settle_metric":"每季法說揭露的每 TB 混合價格年增；CY2029–31 長約價格機制；Toshiba 菲律賓產能量產時程","if_then":["若連兩季每 TB 價格年增 ≥15% 且 CY2029 後長約揭露含漲價機制 → Bear 機率降到 25%，股價 ≤380 美元時首倉 1/3","若每 TB 價格年增降到個位數且 Toshiba 正式公告擴產時程 → 不建倉，Bear 機率上調至 40%","價格先走證據未到：股價續漲但價格年增未加速 → 不追；股價跌破 320 美元而價格年增仍 ≥0 → 分批反買首倉 1/3"],"evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"]},{"axis":"不追的反面：現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價已自前份 467.46 跌 17% 至 386.94，對 FY2028E 共識僅 12.2 倍、FY2029E 9.0 倍；Q1 FY27 指引營收年增 42–49%、毛利率 55–56%，年增量毛利率約 80%；淨現金、自由現金流全數回饋；RSI 36.4 接近超賣；賣方平均目標價 483 美元。","side_b":"低本益比建立在高峰毛利率上；Base 五年年化約 5%、上下行比約 1.3；賣方目標價以 500–1,050 美元計約 2.1 倍，含疑似過時的 250 美元則達 4.2 倍，共識本身不穩；已跌 17% 不是安全邊際。","ruling":"可調和（程度差異）：基本面動能真實，但價格只反映到 Base 與 Bull 之間，選不追。","evidence_level":"指引與法說為一手，賣方目標價為彙整","settle_metric":"Q1 FY27 實際毛利率與每 TB 價格年增","if_then":["若 Q1 FY27 毛利率 ≥56% 且每 TB 價格年增 ≥20% → 重算 Base，股價 ≤360 美元時首倉 1/3","若毛利率低於 55% 指引下緣 → 不建倉"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"兌現項：Q3 法說（2026-04-30，CFO）指引 FQ4 營收 36.5 億±1 億、毛利率 51–52%、EPS 3.25±0.15。實際營收 37.47 億，約在上緣 37.5 億；毛利率 54.4%、EPS 3.56，皆超過上緣。執行長在 Q3 說價格年增朝高個位數，Q4 實際為高十幾%。","side_b":"落差項：高頻寬硬碟目標在 Q4 法說（2026-08-05，執行長）為吞吐量最高 8 倍，Citi 會議（2026-09-09，CFO）改為效能提升 2 倍，口徑可能不同但目標明顯降低；EB 出貨年增由 Q3 的 34% 降到 Q4 的 22%；每 TB 成本年降約 8%，低於長期約 10%，CFO 稱處於產品轉換之間且 DRAM／NAND 投入成本上升；Q3 法說三次迴避（毛利率超標來源未量化、2027 年底 HAMR 占比拒給數字、成本降幅加速未給數字）。","ruling":"短期財測可信，長期第二曲線與成本曲線說法打折：五年後成長空間不升寬，成本年降 10% 在 HAMR 放量前不當作基準。","evidence_level":"一手逐字稿","settle_metric":"FY2027 每 TB 成本年降幅；高頻寬硬碟首張量產訂單","if_then":["若 FY2027 連兩季每 TB 成本年降 <5% → Base 毛利率下修 2pp、不建倉","若高頻寬硬碟 2027 年內取得量產訂單 → Bull 機率上調至 25%"],"evidence_refs":[]},{"axis":"共識修正口徑","cause":null,"prior_field":null,"side_a":"FY1 共識近三月 +102%（9.95→20.12），表面看是大幅上修。","side_b":"7 月快照的 FY1 為尚未公布的 FY2026（實際 non-GAAP 10.22，接近 9.95），10 月已滾動成 FY2027；同口徑真實修正為 FY1 +0.15%、FY2 +0.25%、FY3 −4.37%。","ruling":"採後者：+102% 是財年滾動，不作上修動能證據；遠年共識實為下修。","evidence_level":"快照數值與法說實際值對照，屬推論","settle_metric":"下次快照 FY1／FY2／FY3 同口徑修正","if_then":["若下次快照 FY2／FY3 再下修 ≥5% → Bear 機率上調至 35%、不建倉"],"evidence_refs":[]},{"axis":"前份漂移：裁決、角色、綜合評級、估值","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-09-06，股價 467.46）：觀望、追蹤，綜合評級 B，估值黃（FY2028E 約 14.7 倍）。","side_b":"本次股價 386.94（−17%），FY2028E 降至 12.2 倍；但便宜來自高峰分母，估值結論仍黃、綜合評級維持 B；裁決與角色由程式依本次輸入重算。前份重啟條件（≤350 美元）未觸發。","ruling":"價格下跌未改變判斷。","evidence_level":"事實表價格與共識","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：護城河方向、陷阱、五年後成長空間、循環位置","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5","cycle_position"],"side_a":"前份：護城河方向穩定、陷阱風險黃、五年後成長空間中等、晚循環。","side_b":"本次新增 Toshiba 擬倍增產能報導（2026-10-02）、TrendForce 預估 Seagate 2028 年成最大供應商（2026-10-07）、CFO 把高頻寬硬碟目標由 8 倍改為 2 倍（2026-09-09）；結論不變，但晚循環證據更充分，執行力軸由穩定轉偏弱。","ruling":"四欄維持原值；若 HAMR 2027 上半年未出貨，護城河方向改判向下。","evidence_level":"二手報導＋一手逐字稿","settle_metric":"HAMR 首批出貨時點；份額季度序列","if_then":["若 HAMR 2027-06-30 前未出貨 → 護城河方向改向下，不建倉、已持有者減碼一半"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","supply_demand_durability#4"]},{"axis":"前份漂移：公司類型","cause":"新證據","prior_field":["archetype"],"side_a":"品質複利成長","side_b":"循環/商品（次要：品質複利成長）","ruling":"改判：營益率由 FY2023 −6.4%（含快閃）到 FY2026 35.6%，獲利振幅來自每 TB 價格；本輪新出現第三名廠商擴產回應與研究機構「供需趨近平衡」看法，供給可逆性比前份假設高。長約降低循環但未消除；前份同時標晚循環，改判讓框架一致。","evidence_level":"財報序列＋二手報導","settle_metric":"CY2028 每 TB 價格方向","if_then":["若 CY2029–31 長約揭露鎖價且 CY2028 每 TB 價格年增仍 >0 → 改回品質複利成長、Bull 機率上調至 25%"],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#4"]},{"axis":"前份漂移：情境機率與最大回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 25%、Bear 30%，最大回撤 −65%（單點）。","side_b":"本次 Bull 20%、Base 48%、Bear 32%，最大回撤區間 −55% 至 −72%。","ruling":"改用循環股框架重建情境：共識三年 EPS 年複合約 61% 超出內生上界約 25%，Bear 機率須 ≥30%；Toshiba 擴產使 Bear 由 30% 升至 32%、Bull 由 25% 降至 20%；回撤改為區間，深端依 Bear 路徑低點約 −69%。","evidence_level":"本次情境推導","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：重啟條件（首倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤$350（≤11x FY2028E）且 ASP/TB 年增仍 ≥0 → 衛星首倉 1/3；或 CY2027 定價確認持平＋再有 2 家長約延至 2028 → 重跑 DD 升條件式","side_b":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","ruling":"首倉價位由 350 降到 320 美元：Toshiba 擴產使 Bear 機率上升，320 美元時 Base 年化約 9%、上下行比約 2，跨過中等門檻；長約條件改為 CY2029 以後，因 Q4 法說已揭露一家長約延至 CY2029，原「再有 2 家延至 2028」已不是約束所在。","evidence_level":"二手報導＋一手逐字稿","settle_metric":"股價；每 TB 價格年增；CY2029 後長約揭露","if_then":["股價 ≤320 美元且每 TB 價格年增 ≥0 → 首倉 1/3"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"前份漂移：清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼門檻（摘要為空）","side_b":"新設：每 TB 混合價格年增轉負 → 清倉；non-GAAP 毛利率連兩季 <50% → 減碼一半；份額連兩季 <38% → 減碼一半；HAMR 2027-06-30 前未出貨 → 減碼一半","ruling":"前份無門檻可對照，本次依唯一致命點與 H2、H3 補設。","evidence_level":"本次判斷","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（摘要為空）","side_b":"Single Thing：任一季法說揭露每 TB 混合價格年增轉負（漲價週期結束）","ruling":"每 TB 價格是 EPS 路徑中數學上最大的單一敏感度項，設為唯一致命點。","evidence_level":"本次判斷","settle_metric":"每季法說每 TB 混合價格年增","if_then":["若發生 → 清倉，Bear 機率上調至 ≥50%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q1 FY27 法說：毛利率是否落在 55–56% 指引、每 TB 混合價格年增是否維持高十幾%","type":"假設驗證","maps_to":"H2","metric":"non-GAAP 毛利率；每 TB 混合價格年增","threshold":"毛利率 ≥55% 且價格年增 >0","action":"未達 → H2 削弱、不建倉；達標且價格年增 ≥20% → 重算 Base","source_freq":"每季法說","date":"2026-Q4（Q1 FY27 財報，確切日期事實表未涵蓋）","evidence_refs":[]},{"n":2,"text":"44TB HAMR 是否於 2027 上半年量產出貨，40TB ePMR 於 FQ3 FY27 是否達近線 EB 50%","type":"假設驗證","maps_to":"H3","metric":"HAMR 首批量產出貨；ePMR 占近線 EB 比重","threshold":"2027-06-30 前出貨；ePMR ≥50%","action":"未達 → 護城河方向改向下、不建倉、已持有者減碼一半","source_freq":"每季法說","date":"2027-06-30","evidence_refs":["competitive_share_entrants#2","substitute_technology#2"]},{"n":3,"text":"Toshiba 是否正式公告菲律賓擴產時程，WDC 是否在法說提到價格競爭","type":"風險","maps_to":"R1","metric":"Toshiba 公告；WDC 每 TB 價格年增","threshold":"公告擴產且 WDC 價格年增降到個位數","action":"Bear 機率上調至 40%、不建倉","source_freq":"事件＋每季法說","date":null,"evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2","end_markets#5"]},{"n":4,"text":"任一季法說揭露每 TB 混合價格年增轉負","type":"Single Thing","maps_to":"Single Thing","metric":"每 TB 混合價格年增","threshold":"<0%","action":"清倉；未持有者不建倉","source_freq":"每季法說","date":null,"evidence_refs":[]},{"n":5,"text":"股價跌到 320 美元以下且每 TB 價格年增仍 ≥0","type":"估值rearm","maps_to":"rearm","metric":"股價；每 TB 混合價格年增","threshold":"≤320 美元（約 FY2028E 共識 10 倍）且年增 ≥0","action":"首倉 1/3，其餘待 HAMR 出貨確認","source_freq":"每日股價＋每季法說","date":null,"evidence_refs":[]},{"n":6,"text":"大客戶延後提貨或長約重談降價","type":"風險","maps_to":"R3","metric":"單季營收季變動；前十大客戶占比","threshold":"單季營收季減 >10%，或前十大占比 >80%","action":"減碼一半；未持有者不建倉","source_freq":"每季財報＋年報","date":null,"evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"n":7,"text":"關稅、原產地認定或磁頭與稀土供應壓縮毛利率","type":"風險","maps_to":"R5","metric":"non-GAAP 毛利率季變動","threshold":"單季下滑 ≥200bp 且公司歸因關稅或零組件","action":"減碼一半","source_freq":"每季法說；Section 232 公告","date":"2026-11-10（稀土暫停期屆滿）","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"n":8,"text":"Q2 FY27 財報後依新資料重跑判斷","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑判斷","source_freq":"一次","date":"2027-Q1","evidence_refs":[]}],"kill_metrics":[{"metric":"每 TB 混合價格年增（公司法說揭露）","bear_threshold":"轉為負值（<0%）→ 清倉","window":"任一季","source":"WDC 季度法說 CFO 說明","last_status":"ok"},{"metric":"non-GAAP 毛利率","bear_threshold":"<50%（較 Q1 FY27 指引 55–56% 低 5pp 以上）→ 減碼一半","window":"連續 2 季","source":"WDC 季度新聞稿","last_status":"ok"},{"metric":"HDD 份額（容量或出貨口徑）","bear_threshold":"<38% → 減碼一半","window":"連續 2 季","source":"TrendForce／Coughlin 產業資料","last_status":"ok"},{"metric":"44TB HAMR 量產出貨","bear_threshold":"2027-06-30 前未開始出貨 → 減碼一半","window":"至 2027-06-30","source":"WDC 法說與新聞稿","last_status":"ok"}],"decision_out":{"role":"追蹤","row_hit":"2→QC-49(觀望)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"QC-49 承繼前次裁決（矩陣機械輸出＝迴避／row2，前次裁決＝觀望，90 天內翻面查無已發火觸發器）","hit":true,"basis":"qc49_inherit_prior=True, prior_verdict='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望","rearm_trigger":"股價≤$320（約10倍FY2028E共識）且每TB價格年增仍≥0→首倉1/3；或CY2029後長約揭露鎖價且Toshiba擴產未致降價→重跑判斷","exec_line":"現價不追；跌至 320 美元以下且每 TB 混合價格年增仍 ≥0 時首倉 1/3，HAMR 2027 上半年如期出貨後再加 1/3；每 TB 價格年增轉負則清倉、未持有者不建倉。"},"reasoning":{"industry":"Q4 FY26 營收 37.47 億美元（年增 44%），non-GAAP 毛利率 54.4%、營益率 44.2%，GAAP 營益率 41.7%；Q1 FY27 指引營收 41 億美元±1 億、毛利率 55–56%、EPS 4.00±0.15。分部：雲端約 33 億（89%，年增 43%）、Client 2.25 億（6%，年增 61%）、Consumer 1.87 億（5%，年增 38%），CFO 稱三段毛利率都在 50% 出頭，獲利不靠組合撐。量價：Q4 出貨 231 EB、年增 22%（Q3 為 34%），每 TB 混合價格年增由高個位數升至高十幾%，每 TB 成本年降約 8%。單點依賴：前十大客戶占 FY2026 營收 73%（FY2024 為 55%），三家各占 16%／15%／13%，集中度三年升 18pp，屬集中度風險而非護城河證據。供需持久性：週期性將反轉，時點約 CY2028——需求真實，但供給可逆性中等，Toshiba 擴產與雙寡頭 HAMR 面密度提升會在 2027–28 年加快 EB 供給。產業態勢三軸裁決為雙向拉鋸：競爭面惡化（Toshiba 擬擴產、Seagate HAMR 領先），結構面轉好（2026 產能售罄、長約延至 CY2029、HDD 存放超大規模資料約 80%），其他變數為關稅與原產地認定、客戶集中度上升。","moat":"機制：HDD 只剩三家，面密度技術門檻高，超大規模客戶每代平台需一年以上認證並以多年長約鎖量（CFO：客戶提前 52 週下單，FY2027 絕大部分已在長約下）。可證方向：份額 42–48%（2025 Q1 Coughlin 42%、TrendForce 2026 估 48%，口徑不同），未見下滑序列；定價力實證為每 TB 價格年增由 9% 升至高十幾%。執行力 7：40TB ePMR 如期放量、Q4 營收達指引上緣、毛利率與 EPS 超出上緣，但 HAMR 量產比 Seagate 晚約一年，分析師指出 Seagate 毛利率指引高約 200bp。定價力 7：漲價主要來自供給緊張，非轉換成本或品牌，Toshiba 擴產可直接削弱。同業對照缺 Seagate 與 Toshiba，表內快閃與記憶體廠利潤率較高屬不同循環，不作護城河差距解讀。當期 ROIC：投入資本事實表未涵蓋，依營益率 35.6% 與資本支出低於營收 4–6% 推論屬高利益率×高周轉，非實算。","growth":"成長組成：量（EB 年增 22–25%，供給受限）＋價（每 TB 價格年增高十幾%）＋淨回購，無併購。三年共識 EPS：FY2027E 20.12、FY2028E 31.83、FY2029E 42.87（Koyfin 快照，EPS 家數未揭露；營收共識 FY1 23 位、FY2 22 位分析師），以 non-GAAP FY2026A 10.22 為基期，年複合約 61%；GAAP 基期 26.92 含 SanDisk 持股利益，不可用。內生上界約 25%（見護城河段），缺口約 36pp 可歸因毛利率擴張（每 TB 價格漲、成本降）與淨回購，屬可歸因但高度依賴漲價續航。營運槓桿為正：Q4 營業利益年增 126%、營收年增 44%。FY2029 共識在最近兩份快照之間下修 4.37%，是第一個向下修正。","governance":"FY2026 自由現金流 35.11 億美元（利潤率 27.2%），Q4 單季 12.81 億（營運現金流 13.89 億、資本支出 1.08 億）；FY2026 回饋股東 31 億美元。FCF 對 GAAP 淨利僅 0.38，因 GAAP 淨利含 SanDisk 持股處分與評價利益（Q3 法說賣出 580 萬股抵減債務 31 億美元）；以 non-GAAP EPS 10.22 粗估淨利約 38–40 億，轉換率約 0.9。SBC 單季 4,500 萬美元（營收 1.2%）。Q4 末債務 11 億、現金 16 億，淨現金約 4–5 億；股利每季 0.15 美元；CFO 稱長期資本支出占營收 4–6%，未來兩年可能略高，投向磁頭、媒體與自動化。","valuation":"現價 386.94 美元：FY2027E 19.2 倍、FY2028E 12.2 倍、FY2029E 9.0 倍；前瞻 EV／營收 7.5 倍。trailing 本益比 14.4 倍用 GAAP EPS 26.92，含 SanDisk 持股利益，失真不用；P／S 11.2 倍在 4 個年度端點中位於 67%，非五年分位。PEG 以 non-GAAP 三年年複合約 61% 計約 0.31，但循環股在高峰 PEG 偏低屬常態，不作便宜證據。Base（FY2031E EPS 38.5 × 13 倍＝約 500 美元）五年年化約 5%，低於 8% 門檻。12 個月：FY2028E Base EPS 29.0 × 13 倍＝377 美元（−2.6%）；三年：FY2030E 36.5 × 13 倍＝475 美元（+22.6%）。賣方平均目標價 483 美元（20 位）比本裁決樂觀，差異在賣方把漲價外推到 FY2029（共識粗估隱含毛利率約 60% 以上），本裁決認為供給回應會先到。另：FY1 共識近三月 +102% 是財年滾動造成（7 月快照的 FY1 是 FY2026、10 月是 FY2027），同口徑真實修正為 FY1 +0.15%、FY2 +0.25%、FY3 −4.37%。","premortem":"反證三視角與陷阱判斷依據見反證紀錄。衰退訊號亮 2 項：EPS 成長遠高於營收成長；GAAP 自由現金流對淨利連兩年 <0.75，但受 SanDisk 持股利益扭曲，低權重。成長熄火壓力測試以 Base FY2029E 34.5 為起點，之後年增 15%／10%／5% 配 14／12／10 倍，FY2031E 價位約 639／501／380 美元，三案兩案守住現價。最大回撤依據見情境假設。"},"plain":{"six":{"how_it_makes_money":"賺超大規模雲端業者的容量儲存錢：雲端占營收 89%，多年長約鎖基礎量、基礎量以外另議價；錢卡在「每 TB 價格上漲＋每 TB 成本年降約 10%」的剪刀差，產業處過熱初段。","moat":"護城河 B、方向穩定：三家寡占與長約撐住定價力，但 HAMR 落後 Seagate、Toshiba 擬擴產，執行力軸偏弱，兩軸相抵判穩定。","growth":"五年後成長空間中等：EB 需求隨資料量複利、管理層稱 >25%，但 HDD 已占超大規模資料約 80%，難再搶份額；第二曲線高頻寬硬碟仍在送樣，且目標由「吞吐量最高 8 倍」改為「效能提升 2 倍」。","capital":"資本配置紀律好但時點偏高：淨現金、SBC 低、自由現金流全數回饋；回購集中在股價上漲段，若此刻在循環高檔，買回的價值打折。","valuation":"現價要求 FY2028–29 共識 EPS（31.83／42.87）大致兌現，且市場在高峰毛利率上仍給 12 倍以上；這等於假設每 TB 價格在 Toshiba 擴產與雙寡頭 HAMR 放量下續漲到 2028 年，我只信到 2027 年。","how_wrong":"最可能看錯的地方是 2028 年後每 TB 價格方向：若長約延到 2031 並含漲價，循環論錯、Bull 成立；若 Toshiba 擴產與 HAMR 放量讓供給追上，現價的 12 倍 FY2028E 就是高峰本益比。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"追蹤","wait_for_price":true,"wait_for_price_condition":"股價 ≤320 美元（約 FY2028E 共識 10 倍）且每 TB 混合價格年增仍 ≥0；或 CY2029 後長約揭露鎖價機制且 Toshiba 擴產未引發降價","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":386.94,"week26_return_pct":10.57,"consensus_rev_3m_pct":102.21,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"便宜論證全落在 FY2028–29 EPS，而這兩年的毛利率假設（約 58–60% 以上）正是循環高峰爭點；trailing 分母又含 SanDisk 一次性利益。分母有爭議，低本益比不構成便宜論證。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"guidance","event":"Q1 FY27 財報：檢查營收 41 億±1 億、毛利率 55–56%、每 TB 價格年增","impact":"高","watch":"毛利率是否 ≥55%；每 TB 價格年增是否維持高十幾%；CY2029 後長約進度"},{"date":"2026-11","date_precision":"month","type":"regulatory","event":"中國中重稀土出口逐案核准暫停期 2026-11-10 屆滿","impact":"中","watch":"是否延長；公司是否提到供應或成本影響"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"44TB HAMR 預計 2027 上半年開始量產出貨（CFO：Q1 少量、Q2 較多）","impact":"高","watch":"首批出貨是否如期；認證客戶數（目前 4 家）"},{"date":null,"date_precision":null,"type":"capacity","event":"Toshiba 擬於其 FY2027 前倍增 HDD 產能（確切月份事實表未涵蓋）","impact":"高","watch":"Toshiba 正式公告；菲律賓產線量產時程；每 TB 價格反應"},{"date":null,"date_precision":null,"type":"other","event":"Kioxia 合併傳聞（未證實，來源日期不一致）","impact":"低","watch":"公司公告"}],"_projected_from":"v19"}
```
