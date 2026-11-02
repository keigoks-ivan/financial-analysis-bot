你是 stock-analyst v20 的**散文層（prose）agent**，標的 FLEX（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：FLEX　日期：2026-11-03　archetype：None　前份裁決：2026-05-18　B（觀望·thesis 完整 — Q4 FY26 beat + SpinCo 公告 + FY27 guide raise + AI infra 訂單 verified；但估值 🟡 救援後 PEG 0.87 / Fwd PE 31x（5Y 分位 92%）+ Pure MA ✅ 極端拉伸 4.5x W250、12 週 +119% 動能末段，等回測 W52 $63 / BB 中軌 $76 分批進場）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1868B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（752B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（983B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1604B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1446B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（1002B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（983B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2209B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4396B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2348B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1868           3592-5132      5 條（2–6 內）  
s3                  8000         752           5074-7248      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4033          7677-10967      5 條（2–6 內）  
s6                 11000        1002           6999-9998      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         983           1762-2517      5 條（2–6 內）  
s10                 5000        2209           1954-2791      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2348           2000-2652      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=6048B；至少需散文≈38.95KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−55%
−48%
−38%
−36.9%
−35%
−35
−20.3
−10%
−5.24
−5.2%
−0.46%
−0.2%
0
0.24
0.36
0.37
0.40
0.41
0.5%
0.51%
0.6%
0.61
0.70
0.75
0.79
0.99
1%
1
01
1.04
1.1
1.13
1.18
1.20
1.27
1.28
1.4%
1.4
1.5%
1.52
1.6
1.7
1.9
2%
02
2
2.61
2.87%
2.99%
03
3%
3
3.02
3.29
3.32%
3.51%
3.69
3.75
3.82%
4%
4
4.3%
4.4%
4.42
4.44
4.5
4.62
4.66%
4.7%
4.74
4.84
4.9
4.9%
5
5.00
05
5%
5.07
5.11%
5.16
5.2
5.3
5.44%
5.49%
5.5
5.5%
5.8%
5.9
6
06
6%
6.1%
6.12%
6.3%
6.3
6.4%
6.4
6.7
6.8%
7
7%
07
7.0
7.1%
7.1
7.10
7.2%
7.6
7.6%
7.7%
7.8%
7.83
08
8
8.29%
8.5
8.9
9
09
9%
9.01%
9.23%
9.30
9.3
9.4%
9.5%
9.5
9.6
9.7
9.7%
9.9%
9.9
10
10%
10.2
10.22
10.4
10.5
10.7%
11%
11
11.1
11.3%
11.4
11.46%
11.5%
11.5
11.7%
12
12%
12.2
13
13%
13.6
13.9%
14%
14
14.9
15%
15
15.5
16%
16
17
17.16
17.2
18
18.5
19%
19.2%
19.2
20%
20
21%
21.5
22%
24
25
25%
26
27
27%
28
29%
29
29.8%
30
30%
31
31.3
32
33
35%
36%
36.9%
37%
39%
39
39.5%
39.5
39.9
40%
42
44
45
45%
45.9%
46%
48%
49
50
50%
52%
52
53
54
54%
55
60
60%
61.2
$63
63
65
65.9%
70
70%
70.07
72%
73
74
75%
75
$76
77
80%
84.9
85%
86.25
87
87.03
90
94
95
95.07
99
100%
100
104
105
115%
119
121
137.86
150
150%
160
160.5
170
170.7
171
200
203
210
240
250
268.2
277%
279
337
349
352
354
359
364
395
463.7
464
550
800
2026
2027
2028
2317
20261103
4,300
6,800
6,850
6,900
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
{"meta":{"ticker":"FLEX","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Flex Ltd."},"oneliner":"AI 資料中心電源帶動 FY27 調整後 EPS 指引年增約五成，股價卻自 5 月的 137.86 美元回落到 87 美元、前瞻本益比 17 倍；FY28 以後的成長取決於少數雲端大廠的資本支出，加上 2027 年初分拆在即，先等 11-10 投資人日的 FY28 指引再動。","thesis":{"H":[{"id":"H1","text":"CPI（2027 年初分拆為 Axiom）FY27 指引兌現，FY28 營收再成長五成以上、營益率 12% 以上","2y":"FY27 CPI 營收年增 ≥75%、營益率 ≥11.5%；FY28 CPI 營收年增 ≥50%、營益率 ≥12%","5y":null,"10y":null,"threshold":"FY28 CPI 營收年增低於 50% 或營益率低於 11.5% 即不成立","source":"季報部門數據；2026-11-10 投資人日與 Q4 FY27 法說（預計 2027-05）的 FY28 指引；分拆後改看 Axiom 季報","drift_rule":"兩年期：CPI 季營收成長連 2 季落後指引路徑 5% 以上為削弱，連 3 季落後 10% 以上為反轉"},{"id":"H2","text":"分拆後的 Flex（RMS＋ITS）維持中個位數以上成長、營益率約 6%，資本支出回到營收 2% 以下，成為現金穩定的工業製造平台","2y":null,"5y":"FY29–FY31 RMS＋ITS 合計營收年增 ≥5%、調整後營益率 ≥5.8%、資本支出占營收 ≤2%","10y":null,"threshold":"合計營益率跌破 5.5%，或營收連兩個年度衰退即不成立","source":"分拆後 Flex 季報；CCO 10-28 稱資本支出回到營收 2% 或以下","drift_rule":"五年期：連 4 季偏離 5% 以上為削弱，連 6 季偏離 10% 以上為反轉"},{"id":"H3","text":"FY27 的超額投資（資本支出 15–16 億美元、EPC 收購約 44 億美元）在 FY29 前轉成現金：自由現金流轉換率回到 70% 以上，合併淨負債回落","2y":null,"5y":"FY29 自由現金流轉換率 ≥70%，FY29 年底合併淨負債低於 FY27 年底","10y":null,"threshold":"FY28、FY29 連兩年自由現金流轉換率低於 50% 即不成立","source":"年報現金流量表；公司自由現金流轉換率指引（FY27 約 40%）","drift_rule":"五年期：連 4 季偏離 5% 以上為削弱，連 6 季偏離 10% 以上為反轉"}],"R":[{"id":"R1","text":"雲端大客戶集中與內製：Axiom 前兩大客戶可能占六到七成營收，任一家內製、雙供應或轉單，CPI 營收與議價同時受損；CPI 單一客戶已占應收帳款 16%","h_ref":"H1","clock":"🔥","threshold":"CPI（Axiom）季營收季減超過 15%，或公司揭露任一大客戶程式轉出","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1","competitive_share_entrants#0"]},{"id":"R2","text":"AI 資本支出進入消化期：CPI 成長急速減速，FY27 堆高的存貨與為 FY28 預建的產能轉成跌價與閒置；新架構（800V、固態變壓器）也可能讓既有產品與存貨過時","h_ref":"H1","clock":"🔥","threshold":"CPI 營收年增連 2 季低於 30%，或存貨扣客戶預付款後天數連 2 季超過 65 天（Q2 FY27 為 60 天）","evidence_refs":["ems_utilization_capex_cycle#1","substitute_technology#0"]},{"id":"R3","text":"分拆與融資執行：分拆延後，或 Axiom 20 億美元可轉換特別股未完成，EPC 債務與 33 億美元 364 天定期貸款額度變成長期負擔","h_ref":"H3","clock":"⚡","threshold":"2027-06-30 前未完成分拆，或特別股交易終止","evidence_refs":["major_events#2"]},{"id":"R4","text":"貿易與地緣：墨西哥占營收約 25%、淨固定資產 36%，USMCA 2026 年檢討可能修改或暫停協定；中國營運受法規與地緣影響；關稅成本回收有時間差；紅海與荷莫茲海峽航運受擾推高運費","h_ref":"H2","clock":"🔥","threshold":"USMCA 被修改或暫停，或單季調整後營益率年減 ≥50bp 且公司歸因關稅或運費","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#4","geo_supply_chain#3"]},{"id":"R5","text":"零組件缺料與客戶指定單一來源：CEO 稱缺料會延續幾年，Flex 換來源與轉嫁成本的能力有限，營收可能遞延","h_ref":"H1","clock":"⚡","threshold":"單季營收低於指引下緣，且公司歸因缺料","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2"]}],"single_thing":{"description":"Axiom（現 CPI）前兩大雲端客戶中任一家把主要電源或機櫃程式改為自製，或轉給其他供應商","why_fatal":"10-28 法說分析師以兩家客戶占 Axiom 六到七成提問，CEO 未否認；以 FY26 資料中心營收約 65 億美元、FY27 與 FY28 各成長約八成推算，FY28 CPI 約 210 億美元，失去一家約少 63–74 億美元營收，以 12% 營益率計少 7.6–8.9 億美元營業利益、每股約 1.6–1.9 美元，約占 FY28 共識兩成，議價權也連帶受損，是單一項目中對 EPS 敏感度最大者","if_happens":"已建倉則清倉，未建倉則放棄進場並重跑研究；不在消息當週攤平","how_monitor":"Axiom 分拆後 10-K、10-Q 的客戶集中度；每季 CPI 營收季變化；雲端大廠自研電源與機櫃的公開計畫","probability":"12–24 個月約 10–15%"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":11.1,"peg_fy2":0.24,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":3.29,"FY2027E":5.07,"FY2028E":7.83,"FY2029E":10.22},"fy_end_month":3,"eps_basis":"調整後（non-GAAP）EPS，合併口徑：公司指引與 Koyfin 共識皆未反映 2027 年初 CPI 分拆，代表現有一股 FLEX 在分拆後持有的 Flex＋Axiom 合計；FY2026A 3.29 美元由 10-28 法說 CFO「FY27 調整後 EPS 4.84–5.16 美元、中點年增 52%」反推（5.00÷1.52）；共識取 2026-10-31 Koyfin 快照；財年於 3 月結束"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FLEX_20261103/scenario.json","archetype":{"primary":"EMS/ODM","secondary":"轉機/特殊情境","confidence":"高","fingerprint":"低毛利（約 9.5%）、營益率 5–7%、成長由雲端大廠資本支出帶動；2027 年初分拆屬特殊情境"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性：需求來自少數雲端大廠的 AI 資本支出建置循環，零組件缺料為選擇性缺料（記憶體可能延續到 2027 年後），EMS 產能可轉用、供給可逆性高；目前未見反轉","bargaining":{"up":"部分零組件只有少數或單一供應商，且客戶可指定供應商，Flex 換來源與轉嫁成本能力有限（10-K）","down":"前十大客戶 45%、CPI 對少數雲端大廠高度集中，客戶可雙供應或內製（10-K），議價偏買方","geo":"墨西哥占營收約 25%、淨固定資產 36%，中國 16%；USMCA 2026 年檢討與中國法規屬地緣變數"},"profit_pool_dir":"資料中心利潤池往電源、散熱與整機整合移動，Flex 以自有電源產品與 EPC 往高利潤環節靠；標準整機組裝的利潤被大型組裝廠壓低，Flex 自述不做標準配置","tam_table":[{"item":"全球 EMS 市場規模（2026）","value":"約 6,800–6,900 億美元，多家機構估 CAGR 6.1%–6.8%（定義不同，區間 4.3%–7.6%）"},{"item":"Flex 占全球 EMS","value":"FY27 營收指引中點約 354 億美元，約占 5%（以市場規模中值推算）"},{"item":"資料中心營收（FY26）","value":"約 65 億美元、年增至少 35%、約占總營收 25%（公司 2026-02 說法）"},{"item":"AI 基礎建設投資規模","value":"CEO 稱約 1 兆美元擴建、多數出自少數雲端大廠（口徑未揭露）"},{"item":"CPI 所在市場的 SAM、滲透率、營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"自有電源產品（嵌入式、關鍵電源、EPC 數位整流）加上垂直整合的大規模製造；醫療與車用的法規認證帶來高轉換成本。EMS 主體仍是以規模與執行力取勝的代工，定價權有限","execution":8,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行面擴大：Q2 三部門營益率全數年增，CPI 10.7%（年增 240bp）、電源約 16%（年增約 550bp）；定價面穩定：雲端大客戶集中、可內製或雙供應（10-K）；份額面：聚合站估計 2026 Q1 在同業中份額下滑，ROIC 19.2% 低於 Celestica 39.5%、Jabil 29.8%，不能標擴大","peer_na_reason":null,"threats":[{"level":"🔴","text":"雲端大客戶內製或雙供應：10-K 稱部分超大規模客戶已發展或可能發展內部設計、工程與製造能力，CPI 集中度尤高；過去也有客戶把製造移回自有產能","p":"20%","evidence_refs":["customer_second_source#1","competitive_share_entrants#0"]},{"level":"🟡","text":"同業在 AI 資料中心代工搶份額：聚合站估計 Flex 2026 Q1 在同業集合中份額下滑（營收仍成長），Celestica 營益率與 ROIC 都較高","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"800V 與固態變壓器等技術換代，可能使既有電源、散熱產品與存貨過時（10-K）；Flex 已用 EPC 收購卡位新架構，屬點對點而非架構替代","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉：稅後營益率約 4–6%，ROIC 約 19% 代表投入資本一年周轉三到四倍；現金轉換週期約 31 天（2026-03 季，來源間差異大）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是雲端大廠，三角色一致；AI 機櫃的電源與散熱是「需要」，延後就無法上線算力。但急迫性來自一波資本支出，急迫不等於持久，FY29 以後的需求基礎事實表未涵蓋"},{"item":"決策層級","level":"🟡","text":"替代性要在單一程式層級看：客戶可雙供應、區域化、內製，並可指定供應商（10-K）；醫療、車用有 FDA 與車規認證，重新認證週期長（CCO 法說）。CPI 程式的轉單成本與合約年限事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"AI 資料中心的利潤集中在晶片與雲端大廠，Flex 在中段，毛利率 9.5%；電源段營益率約 16% 顯示在電源環節拿得到較多，但買方高度集中（Axiom 前兩大或占六到七成）、客戶可指定零組件，議價偏買方"},{"item":"社會容忍度","level":"🟡","text":"不涉民生必需品定價，社會對價格的容忍不是限制；但優勢部分建在墨西哥產能（營收約 25%）上，USMCA 2026 年檢討可能修改或暫停協定，屬政策風險"}],"roiic":"未能直接算：投入資本與折舊事實表未涵蓋。粗估：FY27 營收中點 354 億×7.7%－FY26 營收 279 億×6.3%＝調整後營業利益增量約 9.7 億美元，稅後約 7.6 億；同期新增資本支出約 15.5 億加 EPC 約 44 億，全計增量報酬約 13%，但 EPC 只貢獻約半年、三分之二資本支出是為 FY28 預建，時點錯配，實際落點待 FY28 驗證","reinvest_rate":"有機約 72%（資本支出中點 15.5 億÷FY27 稅後營業利益約 21.5 億，未扣折舊、未計營運資金，折舊事實表未涵蓋）；計入 EPC 約 44 億則單年約 277%","endo_ceiling":14,"formula_note":"內生成長上界＝當期 ROIC 19.2%（聚合站，未對 10-K 核實，作為增量報酬的代理值）×有機再投資率約 72%≈14%；稅後營業利益＝營收中點 354 億×調整後營益率中點 7.7%×（1－21%）≈21.5 億"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","FLEX":9.5,"CLS":11.46,"JBL":9.23,"SANM":9.01,"2317.TW":6.12,"unit":"%"},{"metric":"營業利益率","FLEX":5.44,"CLS":8.29,"JBL":5.11,"SANM":5.49,"2317.TW":3.51,"unit":"%"},{"metric":"FCF 利潤率","FLEX":3.32,"CLS":2.99,"JBL":3.82,"SANM":4.66,"2317.TW":-0.46,"unit":"%"},{"metric":"研發密度","FLEX":null,"CLS":0.93,"JBL":0.08,"SANM":0.26,"2317.TW":1.31,"unit":"%"}],"competitors":[{"name":"CLS","gm":11.46,"om":8.29,"fcf_margin":2.99,"rd_intensity":0.93,"strategy_note":"AI 伺服器與網通最純的同業，TTM 營益率 8.29%、聚合站 ROIC 39.5% 皆高於 Flex，是雲端代工最強的對照；Flex 的差別在自有電源與散熱產品","period":"TTM ending 2026-09-30（4季加總）"},{"name":"JBL","gm":9.23,"om":5.11,"fcf_margin":3.82,"rd_intensity":0.08,"strategy_note":"營益率 5.11%、FCF 利潤率 3.82% 與 Flex 相近，ROIC 29.8% 較高，同樣押資料中心，是分拆後 Flex 最直接的對照","period":"TTM ending 2026-08-31（4季加總）"},{"name":"SANM","gm":9.01,"om":5.49,"fcf_margin":4.66,"rd_intensity":0.26,"strategy_note":"營益率 5.49%、FCF 利潤率 4.66% 為五家最高，ROIC 11.3% 最低，偏傳統 EMS，可當分拆後 Flex 的下緣對照","period":"TTM ending 2026-06-30（4季加總）"},{"name":"2317.TW","gm":6.12,"om":3.51,"fcf_margin":-0.46,"rd_intensity":1.31,"strategy_note":"毛利率 6.12%、營益率 3.51%、FCF 利潤率 −0.46%，以規模承接 AI 整機組裝，壓低標準組裝的利潤；Flex 自述不做標準配置、只做客製，等於避開這塊價格戰","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（CPI 新程式放量），加組合（電源產品）與併購（EPC、EP² 約占 CPI 成長 10 個百分點）","runway_years":"不適用：CPI 所在市場規模事實表未涵蓋；以全球 EMS 約 6,850 億美元計，Flex 約占 5%，滲透率不是限制","runway_post_y5":"🟡","endo_ceiling_basis":"當期 ROIC 19.2%（聚合站，未對 10-K 核實）×有機再投資率約 72%（資本支出 15.5 億÷稅後營業利益約 21.5 億）≈14%","segments":[{"item":"CPI（雲端與電源基礎建設，2027 年初分拆為 Axiom）","value":"Q2 FY27 營收 25 億美元、年增 54%、調整後營益率 10.7%（電源約 16%）；FY27 指引年增 75–85%、營益率 11.5–11.7%；Q3 指引年增 105–115%；管理層先前提過 FY28 年增約 80%，投資人日更新"},{"item":"RMS（工業、醫療、車用）","value":"Q2 營收 27 億美元、年增 9%、營益率 6.4%；FY27 指引年增中至高個位數；Q3 指引低至中個位數"},{"item":"ITS（通訊、企業、消費）","value":"Q2 營收 33 億美元、年增 22%、營益率 5.5%；通訊強、消費相關疲弱；FY27 指引年增低雙位數到十幾%，Q3 指引中至高個位數"},{"item":"RMS＋ITS 合計（分拆後的 Flex）","value":"Q2 合計年增 16%、連續 4 季年增；FY27 指引年增 8–11%、營益率 5.9–6.1%；分拆後資本支出回到營收 2% 以下（CCO）"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":false,"note":"Q2 調整後毛利率 9.9%，年增 60bp"},{"name":"核心市占近 12 個月縮減","lit":true,"note":"聚合站估計 2026 Q1 在同業集合中份額下滑，來源無原文摘錄，可信度低"},{"name":"主力產品提價後銷量下滑","lit":false,"note":"價格資料事實表未涵蓋，未見此現象"},{"name":"EPS 成長顯著高於營收成長（差距超過 5 個百分點）","lit":true,"note":"FY27 指引 EPS 年增 52%、營收 27%；三年共識 EPS CAGR 約 46% 對營收約 29%"},{"name":"FCF／淨利低於 0.75 連 2 年","lit":false,"note":"FY25 1.27、FY26 1.20；FY27 指引轉換率約 40%，若 FY28 仍低則亮燈"},{"name":"SBC／營收超過 5% 且上升","lit":false,"note":"SBC 約占營收 0.51%"},{"name":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"800V 與固態變壓器屬換代，Flex 以 EPC 卡位"},{"name":"產業估值倍數近 3 年系統性下移","lit":false,"note":"Flex 自身倍數在四個年度端點高位"},{"name":"維持性資本支出占 FCF 超過 60%","lit":null,"note":"維持性資本支出事實表未涵蓋"},{"name":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"FY27 資本支出 15–16 億美元擴產"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"FY27 成長以內生為主（併購約占 CPI 成長 10 個百分點、全年營收指引上調的約一半），股東回饋金額事實表未涵蓋；本年度現金幾乎全數用於資本支出與 EPC，回饋不承重"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"EPC 2026-10-14 完成，約 44 億美元買約 8 億美元營收，管理層稱 FY27 增益；已實現 ROIIC 與 WACC 事實表未涵蓋，暫無法判定","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購金額與均價事實表未涵蓋；FY27 現金主要投向資本支出與 EPC，回購空間有限","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 每季約 4,300 萬美元、年化約 1.7 億，以現價 87 美元約 200 萬股，約占流通股 3.69 億股的 0.5%/年，低於 1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY27 共識調整後 EPS 5.07 美元，合併口徑）為主，PEG 與自身年度端點倍數為輔","tier":"EMS 同業（Celestica、Jabil、Sanmina、鴻海）","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或 EV/S 現值，無法建立倍數對照；終端倍數的同業對照列為資料缺口"},"fwd_pe":17.16,"peg":0.37,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 17.2 倍、PEG 0.37（三年共識 EPS CAGR 45.9%）屬便宜；但 trailing 本益比 31.3 倍、P/S 1.04、EV/S 1.13 全在過去四個年度端點最高（連續五年序列事實表未涵蓋，五年分位留空）；EPC 債務尚未計入淨負債，EV 倍數低估約一成。便宜只在 FY28–FY29 共識成立時成立，而那正是資本支出循環最難驗的兩年，兩相抵判中性。","targets":{"sell_side_avg_usd":170.7,"sell_side_median_usd":170,"range_usd":"150–203","as_of":"2026-07","note":"另一來源共識約 160.5 美元（2026-08）；皆早於股價下跌"},"upside_short_pct":14,"upside_mid_pct":39},"trap_analysis":{"verdict":"🟡","label":"循環高峰獲利被當成常態的風險中等"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"CPI Q3 指引年增 105–115%、存貨年增 39%、FY27 資本支出 15–16 億美元中三分之二為 FY28 預建產能；AI 擴建資金集中在少數雲端大廠","assumption":"雲端大廠在 2028 年（FY29）進入資本支出消化期","consequence":"CPI 營收自高峰回落三到四成，預建產能閒置、存貨跌價；合併 EPS 回到 4.5–5.5 美元、倍數壓到 10 倍，股價 45–55 美元，五年虧損約四成到五成","ruling":"採納為空頭情境主線，機率 30%；不採更高，因為 CFO 7-29 稱 CPI 未來三季九成以上已預訂、FY28 產能已在建，崩落最早落在 FY29。與 Single Thing（大客戶轉出）部分重疊：同樣打在 CPI，但消化期是全產業、客戶轉出是 Flex 專屬，兩者分開監測","watch":"CPI 季營收年增率、存貨扣客戶預付款後天數、FY28 指引；外部參考：主要雲端大廠資本支出年增率","not_applicable_reason":null,"evidence_refs":["ems_utilization_capex_cycle#1","substitute_technology#0"],"fact_refs":["f_kpi6_q3_fy2027_guidance","f_consensus_eps_fy3"]},{"view":"論點成功但股東經濟變差","evidence":"Axiom 將發行 20 億美元可轉換特別股，用來償還 EPC 收購約 44 億美元債務中的約 20 億；另簽 33 億美元 364 天定期貸款額度；FY27 自由現金流轉換率指引約 40%（Q1 0.41 億、Q2 2.61 億美元）；Q2 調整後 EPS 1.18 美元對 GAAP 0.70 美元","assumption":"CPI 照指引成長，但成長要用特別股、債務與資本支出換","consequence":"普通股東對 Axiom 的權益被特別股稀釋，每股自由現金流落後 EPS；合併 EPS 達標，但股東實拿約少一成","ruling":"採納：基準情境 FY28 EPS 取 7.10 美元，比共識 7.83 美元低約 9%，差額反映特別股、利息與分拆後獨立營運成本；特別股條件事實表未涵蓋，取得後重估","watch":"Axiom 特別股股利率與轉換價、FY28 自由現金流轉換率","not_applicable_reason":null,"evidence_refs":["major_events#2","ems_utilization_capex_cycle#1"],"fact_refs":["f_kpi4_free_cash_flow","f_kpi3_non_gaap_eps_adjusted","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"ITS 消費相關需求疲弱；下半年 RMS＋ITS 面對較高比較基期，Q3 指引 RMS 年增低至中個位數、ITS 中至高個位數，上半年兩者合計年增約 16%","assumption":"分拆後 Flex 只剩傳統 EMS，市場給 EMS 倍數","consequence":"分拆後 Flex 成長降到個位數，若市場只給 10–12 倍，合併部位的價值主要靠 Axiom 撐，Axiom 的集中風險被放大","ruling":"部分採納：H2 門檻設在營收年增 ≥5%、營益率 ≥5.8%；FY27 指引（年增 8–11%、營益率 5.9–6.1%）仍在門檻上方","watch":"RMS＋ITS 合計營收年增與營益率","not_applicable_reason":null,"evidence_refs":["supply_demand_durability#1"],"fact_refs":["f_kpi6_q3_fy2027_guidance","f_kpi7_fy2027_guidance"]},{"view":"價格已反映太多","evidence":"現價 87.03 美元、FY28 共識 11.1 倍、FY29 8.5 倍；前份 2026-05-18 股價 137.86 美元，至今回落約 37%，期間 FY1 共識上修 9.7%；但 trailing 本益比 31.3 倍為過去四個年度端點最高","assumption":"市場已經把 FY28–FY29 當成循環高峰在定價","consequence":"若高峰判斷對，現價並不便宜；若 FY28–FY29 只是循環中段，現價低估","ruling":"反駁「已反映太多」：基準情境 FY30 EPS 9.3 美元×13 倍＝121 美元，現價隱含的期望低於我的基準；但下跌原因事實表未涵蓋，不把跌幅當安全邊際","watch":"股價對 52 週均線（約 95 美元）、共識修正方向","not_applicable_reason":null,"evidence_refs":[],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 137.86 → 本次 87.03（-36.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=137.86","side_b":"本次 price_at_dd=87.03","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 137.86 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 137.86 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 137.86 美元：Bull 價 268.2、Bear 價 53，五年期望值 +4.7%，基準年化 −0.2%，不對稱比 1.28","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.28。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 137.86 美元：五年期望值 +4.7%，基準年化 −0.2%，不對稱比 1.28","side_b":"本次情境、股價 87.03 美元：五年期望值 +65.9%，基準年化 9.4%，不對稱比 4.44","ruling":"再換股價、情境不動：起點價下跌 36.9%，五年期望值多 61.2 個百分點，基準年化多 9.6 個百分點，不對稱比由 1.28 升到 4.44。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值：前瞻便宜對自身歷史偏貴","cause":null,"prior_field":null,"side_a":"前瞻便宜：FY27 共識 17.2 倍、FY28 11.1 倍、FY29 8.5 倍，PEG 0.37，FY1 共識近三個月上修 9.7%","side_b":"自身歷史偏貴：trailing 本益比 31.3 倍、P/S 1.04、EV/S 1.13 皆高於過去四個年度端點；EMS 在資本支出高峰的低本益比常是高峰獲利","ruling":"不可調和（方向相反），現階段選自身歷史這一側，依據是前瞻這一側的分母尚未被訂單覆蓋：CFO 7-29 稱 CPI 未來三季九成以上已預訂，只蓋到 FY28 第一季，FY28 全年與 FY29 沒有揭露。決勝數據是 FY28 CPI 營收成長指引，最早 2026-11-10 出現。","evidence_level":"公司指引與共識快照，中","settle_metric":"FY28 CPI 營收成長指引","if_then":["若 FY28 CPI 指引 ≥50% 且股價 ≤100 美元，則重跑研究、首倉 ≤2%，分拆後按兩檔估值再分配","若指引 <50% 或不給，則不追，空頭機率上調至 35%","若股價在指引前先漲回 52 週均線（約 95 美元）以上而證據未到，則不追","反向：若指引達標但股價跌破 104 週均線（約 70 美元）且基本面無損，則分批反買，首倉 ≤2%"],"evidence_refs":[]},{"axis":"客戶集中：管理層說法對 10-K 風險揭露","cause":null,"prior_field":null,"side_a":"CEO（2026-10-28）：雲端大廠是 AI 擴建的主要出資者，不集中就會丟份額，集中是好事；會在每家內部分散產品線","side_b":"10-K：部分超大規模客戶已發展或可能發展內部製造能力，可能內製、雙供應或轉單；CPI 集中度尤高，單一客戶占應收帳款 16%","ruling":"不可調和（方向相反），採 10-K 這一側：CEO 的論證說明了集中為何必要，沒有說明集中為何安全。處置是把大客戶轉出設為唯一致命點，空頭機率定在 30%。","evidence_level":"10-K 風險揭露與法說原話，中","settle_metric":"Axiom 分拆後首份 10-K 的客戶集中度揭露","if_then":["若 Axiom 前兩大客戶占比揭露超過 70%，則首倉上限降為 1%","若任一大客戶程式轉出，則清倉"],"evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1"]},{"axis":"管理層前後說法（7-29 對 10-28）","cause":null,"prior_field":null,"side_a":"7-29：FY27 營收 337–352 億美元、EPS 4.42–4.74 美元、營益率 7.0–7.2%、CPI 營益率至少擴張 100bp、自由現金流轉換率約 40%；散熱自稱早期；CPI 已裝產能認證比例、散熱市場規模、Amazon 協議皆未正面回答","side_b":"10-28：營收 349–359 億美元、EPS 4.84–5.16 美元、營益率 7.6–7.8%、CPI 營益率擴張約 240bp、自由現金流轉換率仍約 40%；散熱仍稱早期、新產品要六個月；7 月未答的三題沒有補","ruling":"一致且超額兌現：損益承諾全數上調，可調和、無矛盾。落差在現金與揭露：現金轉換沒有跟著改善，7 月迴避的三題至今未補，散熱進度停在原地。不改方向，但把散熱排除在基準情境之外。","evidence_level":"兩場法說原話，高","settle_metric":"FY27 實際自由現金流轉換率","if_then":["若 FY27 自由現金流轉換率低於 30%，則停止加碼","若投資人日給出散熱營收規模，則重估樂觀情境"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價自 5 月 137.86 美元跌到 87 美元，同期 FY27 EPS 指引兩次上調、FY1 共識三個月上修 9.7%；FY28 共識只有 11 倍，CPI 未來三季九成已預訂、FY28 產能已在建；等投資人日可能錯過重估","side_b":"投資人日只剩一週，等待的代價小；合併口徑還沒扣 Axiom 特別股與分拆成本，FY28 指引前押注等於替最大的不確定付錢；股價下跌原因不明，跌幅不是安全邊際","ruling":"選等待：一週的等待成本低於提前承擔 FY28 指引風險；指引達標後股價漲到 100 美元以內仍可接受。","evidence_level":"公司指引與價格，中","settle_metric":"FY28 CPI 營收成長指引","if_then":["若指引達標且股價 ≤100 美元，則首倉 ≤2%","若指引達標但股價已超過 100 美元，則不追，等回到 100 美元以下"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：AI 資料中心、關鍵電力支撐高可靠度 EMS 的稼動率與組合（Lincoln 2026 Q2 季報）；Flex 電源段營益率約 16%；EPC 卡位 800V","side_b":"競爭惡化：雲端大廠可能內製、聚合站估計 Flex 份額下滑；其他結構變數：USMCA 2026 年檢討、中國營運、關稅成本回收時點","ruling":"雙向拉鋸：需求面結構轉好有營收與利潤率佐證，競爭與政策面的惡化目前只在風險揭露與聚合站估計，尚未出現在 Flex 的數字；以營收與利潤率為準，結構轉好略占上風，但拉鋸未解。","evidence_level":"10-K、產業季報與聚合站，中低","settle_metric":"CPI 營收成長與營益率；Axiom 客戶集中度","if_then":["若 CPI 營益率連 2 季年減，則改判競爭惡化中並減碼一半"],"evidence_refs":["competitive_share_entrants#2","reg_tariff_export#4"]},{"axis":"前份漂移：價格變動","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-18，股價 137.86 美元）：結論觀望、前瞻本益比約 31 倍、估值中性","side_b":"本次（股價 87.03 美元）：結論仍為觀望、前瞻本益比 17.2 倍、估值仍判中性","ruling":"股價回落約 37% 讓倍數大降，但結論不變：前份中性是因為倍數偏高，本次中性是因為 FY28–FY29 的分母未驗證；觀望理由由價格錨改為事件錨。","evidence_level":"價格與共識快照，高","settle_metric":"FY28 CPI 營收成長指引","if_then":["若指引達標，則估值改判便宜並重跑研究"],"evidence_refs":[]},{"axis":"前份漂移：新證據","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","cycle_position"],"side_a":"前份：陷阱風險低（🟢）；護城河方向、五年後跑道、循環位置未給值","side_b":"本次：陷阱風險中等（🟡）、護城河方向持平（→）、五年後跑道中等（🟡）、循環位置為中循環","ruling":"陷阱風險上調的依據是新資料：FY27 EPS 指引年增 52% 遠高於營收 27%、聚合站估計份額下滑、FY27 自由現金流轉換率只有約 40%、存貨年增 39%。護城河方向與跑道首度給值，依據是 10-28 法說的部門營益率、10-K 的內製風險與同業 ROIC 對照；循環位置依需求量循環五訊號多數決。","evidence_level":"財報、10-K 與聚合站，中","settle_metric":"FY28 自由現金流轉換率與 CPI 營收成長","if_then":["若 FY28 自由現金流轉換率回到 70% 以上，則陷阱風險回調為低"],"evidence_refs":["competitive_share_entrants#2","ems_utilization_capex_cycle#1"]},{"axis":"前份漂移：方法變動","cause":"方法變動","prior_field":["archetype","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：公司類型、裁決角色、情境機率與最大回撤皆未以結構化欄位給值","side_b":"本次：歸為電子代工（EMS/ODM），兼分拆特殊情境；情境機率 25／45／30，最大回撤區間 −35%～−55%；裁決與角色由程式依本次輸入重算","ruling":"屬方法變動而非看法改變：本版要求情境機率與回撤範圍逐項給值，前份無對應數字可比。空頭機率 30% 由內生成長上界（約 14%）低於共識三年成長（約 46%）決定。","evidence_level":"方法說明","settle_metric":"無","if_then":["若下份研究方法再變，則以本次數字作為對照基準"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（空值）","side_b":"Axiom（現 CPI）前兩大雲端客戶中任一家把主要電源或機櫃程式改為自製，或轉給其他供應商","ruling":"新設 Single Thing，依據是 10-28 法說分析師以兩家客戶占 Axiom 六到七成提問、CEO 未否認，加上 10-K 的內製風險揭露；以 FY28 推算，失去一家約少每股 1.6–1.9 美元，是單一項目中敏感度最大者。發生即清倉。","evidence_level":"法說與 10-K，中","settle_metric":"Axiom 客戶集中度揭露、CPI 季營收季變化","if_then":["若發生，則清倉"],"evidence_refs":["customer_second_source#1"]},{"axis":"出場指標變動","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設出場指標（空值）","side_b":"CPI 營收年增連 2 季低於 30% 則減碼一半；存貨淨天數連 2 季超過 65 天則減碼一半；Axiom 大客戶轉出則清倉；RMS＋ITS 營益率低於 5.5% 則停止加碼","ruling":"新設，因為前份的風險門檻掛在雲端大廠資本支出等外部數字上，不在 Flex 財報內；改用公司自己揭露、每季可驗的數字，觸發後動作分為減碼與清倉。","evidence_level":"公司季報","settle_metric":"每季部門數據","if_then":["若任一減碼條件成立，則減碼一半","若 Single Thing 發生，則清倉"],"evidence_refs":[]},{"axis":"重新進場條件變動","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份：等回測 W52 $63／BB 中軌 $76 分批進場（價格錨）","side_b":"投資人日或 Q3 FY27 法說給出 FY28 CPI 營收成長指引 ≥50%，且股價 ≤100 美元","ruling":"由價格錨改為事件錨：股價已跌到 87 美元，價格不再是主要限制，主要限制是 FY28 需求能否確認；達標才首倉，否則不追。","evidence_level":"價格與指引","settle_metric":"FY28 CPI 營收成長指引","if_then":["若條件成立，則首倉 ≤2%","若不成立，則不追"],"evidence_refs":[]},{"axis":"風險門檻變動","cause":"方法變動","prior_field":["thesis.R"],"side_a":"前份：in-sourcing 以「連 4 季 CPI top 3 客戶 share 下滑 ≥10pp，或任一 hyperscaler 公開 in-house 計畫」；分拆以「2027 Q1 未完成」；AI 資本支出以「top 5 hyperscaler 連 2 季 capex YoY −10%，或 NVDA DC revenue YoY 連 2 季低於 20%」","side_b":"本次：大客戶轉出以「CPI 季營收季減超過 15% 或揭露程式轉出」並清倉；分拆以「2027-06-30 前未完成或特別股交易終止」；循環以「CPI 營收年增連 2 季低於 30%」並減碼一半","ruling":"改為 Flex 財報內可驗的數字。CPI 客戶份額 Flex 不按季揭露，舊門檻無法驗證，故退休；雲端大廠資本支出與 NVIDIA 資料中心營收門檻保留為外部參考（來源為各公司季報），現值事實表未涵蓋。分拆容忍期放寬一季，因為 Form 10 已申報、管理層原訂期間為 2027 年第一季。","evidence_level":"方法說明","settle_metric":"每季部門數據","if_then":["若分拆在 2027-06-30 前未完成，則停止加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"投資人日公布 FY28 CPI 營收成長指引","type":"假設驗證","maps_to":"H1","metric":"FY28 CPI 營收成長指引","threshold":"≥50%","action":"達標且股價 ≤100 美元則首倉 ≤2%；未達標則不追、空頭機率上調至 35%","source_freq":"一次性（投資人日）","date":"2026-11-10","evidence_refs":[]},{"n":2,"text":"重新進場：FY28 CPI 成長指引達標，且股價不高於基準 FY28 EPS 的 14 倍","type":"估值rearm","maps_to":"H1","metric":"FY28 CPI 營收成長指引；股價","threshold":"指引 ≥50% 且股價 ≤100 美元","action":"重跑研究後首倉 ≤2%","source_freq":"事件後每日價格","date":null,"evidence_refs":[]},{"n":3,"text":"Single Thing：Axiom 前兩大客戶任一家程式轉出","type":"Single Thing","maps_to":"R1","metric":"CPI（Axiom）季營收季變化；客戶集中度揭露","threshold":"季減超過 15%，或揭露程式轉出","action":"清倉","source_freq":"每季","date":null,"evidence_refs":["customer_second_source#1","customer_concentration_credit#0"]},{"n":4,"text":"資本支出循環轉向：CPI 成長急速減速或存貨堆積","type":"減碼","maps_to":"R2","metric":"CPI 營收年增率；存貨扣客戶預付款後天數","threshold":"CPI 年增連 2 季低於 30%，或存貨淨天數連 2 季超過 65 天","action":"減碼一半","source_freq":"每季","date":null,"evidence_refs":["ems_utilization_capex_cycle#1"]},{"n":5,"text":"分拆或特別股融資延誤","type":"風險","maps_to":"R3","metric":"分拆完成日；Axiom 特別股交易狀態","threshold":"2027-06-30 前未完成分拆，或特別股交易終止","action":"停止加碼，重估債務壓力","source_freq":"8-K 即時","date":"2027-06-30","evidence_refs":["major_events#2"]},{"n":6,"text":"USMCA 檢討結果或關稅成本回收失敗","type":"風險","maps_to":"R4","metric":"USMCA 檢討結果；調整後營益率年變化","threshold":"協定被修改或暫停，或單季調整後營益率年減 ≥50bp 且公司歸因關稅","action":"停止加碼","source_freq":"每季與政策公告","date":null,"evidence_refs":["reg_tariff_export#4","reg_tariff_export#2"]},{"n":7,"text":"FY27 超額投資能否轉成現金","type":"假設驗證","maps_to":"H3","metric":"自由現金流轉換率","threshold":"FY28 低於 50%","action":"減碼一半","source_freq":"每年","date":"2028-05","evidence_refs":[]},{"n":8,"text":"Q3 FY27 法說複審（預計 2027 年 1 月底至 2 月初）","type":"複審日期","maps_to":"H1","metric":"CPI 營收成長、存貨淨天數、分拆進度","threshold":"CPI 是否達 Q3 指引年增 105–115%","action":"重跑研究","source_freq":"每季","date":"2027-02","evidence_refs":[]},{"n":9,"text":"零組件缺料使營收落後指引","type":"風險","maps_to":"R5","metric":"單季營收對指引區間","threshold":"低於指引下緣，且公司歸因缺料","action":"停止加碼","source_freq":"每季","date":null,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2"]}],"kill_metrics":[{"metric":"CPI（分拆後 Axiom）營收年增率","bear_threshold":"連 2 季低於 30%","window":"2027-01 至 2028-03 每季","source":"公司季報部門數據；分拆後 Axiom 季報","last_status":"ok"},{"metric":"存貨扣客戶預付款後天數","bear_threshold":"連 2 季超過 65 天（Q2 FY27 為 60 天）","window":"每季","source":"法說 CFO 揭露","last_status":"warning"},{"metric":"自由現金流轉換率","bear_threshold":"FY28 低於 50%","window":"FY2028（至 2028-03）","source":"年報現金流量表與公司轉換率口徑","last_status":"warning"},{"metric":"Axiom 前兩大客戶營收占比","bear_threshold":"超過 70%，或任一家程式轉出","window":"分拆後首份 10-K 起每年","source":"Axiom Form 10 與 10-K 客戶集中度","last_status":"unknown"},{"metric":"RMS＋ITS 合計調整後營益率","bear_threshold":"低於 5.5%","window":"每季","source":"公司季報部門數據","last_status":"ok"}],"evidence_dismissed":[{"ref":"ems_roic_asset_turnover_benchmark#1","reason":"聚合站資產周轉定義未對齊，同一 Flex 頁面同時出現 1.4 倍與 6.3 倍到 5.5 倍兩組互相矛盾的數字，Sanmina 數字取自另一站，且未對 10-K 核實，無法當作 Flex 周轉率落後的證據；同業比較改用同站同期的 ROIC 並註明未核實"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-5.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2026-11-10 投資人日或 Q3 FY27 法說給出 FY28 CPI 營收成長指引 ≥50%；達標後股價 ≤100 美元才首倉'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"3%","requires_critic":[],"rearm_trigger":"投資人日或 Q3 FY27 法說給出 FY28 CPI 營收成長指引 ≥50%，且股價 ≤100 美元","exec_line":"現在不建倉；條件成立後首倉 ≤2%，分拆生效後依兩檔各自估值再分配；減碼與清倉條件見出場指標與觸發器"},"reasoning":{"industry":"分部（Q2 FY27，季末 2026-09-25）：RMS 營收 27 億美元、年增 9%、調整後營益率 6.4%；ITS 33 億美元、年增 22%、5.5%；CPI 25 億美元、年增 54%、10.7%（年增 240bp），其中電源約 16%（年增約 550bp）。三段都超過營收一成。全公司調整後毛利率 9.9%、營益率 7.1%，GAAP 營益率 4.9%；GAAP 與調整後 EPS 差距大（0.70 對 1.18 美元）。FY27 指引：營收 349–359 億美元、中點年增約 27%；CPI 年增 75–85%、營益率 11.5–11.7%；RMS＋ITS 年增 8–11%、營益率 5.9–6.1%。收錢方式：按客戶程式收製造、整合與物流服務費，物料轉手占營收大宗，所以毛利率不到一成；CPI 多了自有電源產品與 EPC 數位整流器，利潤率才拉高。客戶：FY26 前十大占 45%（FY24 為 37%，三年上升），無單一客戶超過一成；FY26 年底單一客戶占應收帳款 16%，幾乎全在 CPI；10-28 法說分析師以 Axiom 前兩大客戶可能占六到七成提問，CEO 未否認，只說要在每家雲端大廠內分散產品線。單點依賴：CPI 對少數雲端大廠的集中是集中度風險，不是護城河證據。地理：產地以墨西哥最大（營收約 25%、淨固定資產 36%），美國 19%、中國 16%、馬來西亞 11%。產業時鐘在擴張期（II）：AI 資料中心與關鍵電力撐起高可靠度 EMS 的稼動率與組合，零組件缺料屬選擇性而非全面；擴張後段訊號已出現（存貨年增 39%、FY27 資本支出約營收 4%、三分之二為 FY28 預建產能），但 CPI Q3 指引仍是年增 105–115%，需求端還沒減速。供需持久性：週期性，屬雲端大廠資本支出建置循環，目前未見反轉；EMS 產能可轉用、供給可逆性高，需求一旦消化，稼動率與組合會一起回落。CPI 預計 2027 年第一季分拆為 Axiom，現有股東將同時持有兩檔。","moat":"機制：自有電源產品（嵌入式、關鍵電源、EPC 數位整流）加上垂直整合的大規模製造，以及醫療、車用的法規認證；CCO 稱 FDA 認證廠房讓轉換成本高。執行力 8 分：FY27 EPS 指引兩次上調（7-29 為 4.42–4.74 美元，10-28 為 4.84–5.16 美元），CPI 營益率擴張由原先承諾的至少 100bp 上調為約 240bp，Q2 三個部門營益率全數年增。定價權 6 分：CFO 說 CPI 的增量利潤來自組合、價格與量，電源段營益率約 16%；但 EMS 主體是成本加成，客戶可指定零組件、可雙供應或內製（10-K），定價權有限。同業（TTM，營益率、毛利率、FCF 利潤率）：Flex 5.44%、9.5%、3.32%；Celestica 8.29%、11.46%、2.99%；Jabil 5.11%、9.23%、3.82%；Sanmina 5.49%、9.01%、4.66%；鴻海 3.51%、6.12%、−0.46%。Flex 居中，不是最強。ROIC（聚合站 2026 Q1，未對 10-K 核實）：Flex 19.2%（前一年 13.9%）、Jabil 29.8%、Celestica 39.5%、Sanmina 11.3%；對最強同業差約 20 個百分點，Celestica 前期值事實表未涵蓋，差距收窄或擴大無法判定。威脅：雲端大客戶內製屬生態層級攻擊，扣 1 分，等級落在 C。方向：執行面擴大、定價面穩定，加上一筆份額下滑估計，不能標擴大，判持平。報酬持續期：當期 ROIC 屬低利益率、高周轉；四個檢查點全黃，持續期取決於這一波資本支出能撐多久；有機內生成長上界約 14%，推導見報酬持續期欄。","growth":"成長組成：以量為主（CPI 新程式放量，Q3 指引年增 105–115%），加上組合（電源段營益率約 16%）與併購（EP² 與 EPC 約貢獻 CPI 全年成長 10 個百分點，EPC 約占這次全年營收指引上調 9.5 億美元的一半）。三年共識：FY26 實際調整後 EPS 約 3.29 美元（由 FY27 指引中點 5.00 美元、年增 52% 反推）到 FY29 共識 10.22 美元，CAGR 約 45.9%；營收 FY26 279 億美元到 FY28 共識 464 億，兩年 CAGR 約 29%。內生成長上界約 14%（ROIC 19.2%×有機再投資率約 72%）。缺口約 32 個百分點，歸因：營益率擴張（調整後營益率 FY26 約 6.3%、FY27 指引 7.7%，CPI 再擴張約 240bp）、收購（EPC、EP²）、去年投資產能的營運槓桿；缺口可歸因，不靠倍數重估，但營益率擴張是一次性台階，不能外推。營運槓桿：Q2 營收年增 25%、調整後營業利益年增 48%，仍在擴張。跑道：Flex 約占全球 EMS 市場（約 6,850 億美元、年增 6–7%）的 5%，三成滲透率的測試不承重；真正的限制是 CPI 所在市場的規模與週期，其 SAM 事實表未涵蓋。第二條曲線（散熱、固態變壓器、機器人、售後服務）管理層都稱早期或剛起步，沒有營收揭露，不算已證實的下一條 S 曲線，故判中等。衰退訊號亮 2 個，見下列。","governance":"FCF／淨利（事實表年度財務歷史）：FY23 0.40、FY24 0.79、FY25 1.27、FY26 1.20；FY27 指引自由現金流轉換率約 40%（含分拆成本，7 月由不含分拆的約 60% 下修），上半年 FCF 僅 3.02 億美元（Q1 0.41 億、Q2 2.61 億，Q2 含 0.61 億一次性分拆現金成本）；Q2 存貨季增 13%、年增 39%，扣客戶預付款後存貨天數 60 天、年增 5 天。SBC：Q2 約 4,300 萬美元，占營收 0.51%、占調整後營業利益 7.1%；年化約 1.7 億美元，以現價約 200 萬股、占流通股約 0.5%，稀釋低。現金去向（FY27）：一是資本支出 15–16 億美元（約營收 4.4%，三分之二給 CPI、三分之二是為 FY28 預建產能）；二是收購 EPC 約 44 億美元（以新債支應）與 EP²；三、四是回購與股利，金額事實表未涵蓋；Q3 指引加權股數約 3.75 億股。負債：Q2 季末淨負債 29 億美元未含 EPC；若收購全數以新債支應，合併淨負債約 73 億，Axiom 發行 20 億美元可轉換特別股後約 53 億，另有 20 億特別股排在普通股之前；33 億美元 364 天定期貸款額度簽約未動用。分拆後 Flex 資本支出回到營收 2% 以下（CCO），Axiom 需要另一套為快速成長設計的資本配置框架（CEO，7-29）。M&A 報酬：EPC 以約 44 億美元買約 8 億美元營收（約 5.5 倍營收），管理層稱 FY27 即增益，已實現報酬尚無資料。","valuation":"倍數：前瞻本益比 17.2 倍（FY27 共識 5.07 美元），FY28 共識 7.83 美元下 11.1 倍、FY29 共識 10.22 美元下 8.5 倍；前瞻 EV/S 0.99 倍。自身歷史：trailing 本益比 31.3 倍、P/S 1.04、EV/S 1.13 皆高於過去四個年度端點（非連續五年序列）。EV 低估：目前淨負債 29 億美元為 Q2 季末數，未含 10-14 完成的 EPC 收購債務約 44 億美元，納入後 EV 約 395 億、前瞻 EV/S 約 1.1 倍。PEG：以 FY26 實際約 3.29 美元到 FY29 共識 10.22 美元的三年 CAGR 45.9% 計為 0.37，但共識假設 CPI 第三年仍高成長，PEG 低主要反映循環中的高成長，不能當便宜的全部證據。共識：FY1 近三個月上修 9.7%（4.62 到 5.07），最近一次快照 FY1 上修 0.6%、FY2 上修 1.4%、FY3 持平。賣方：平均目標價約 160–171 美元（2026-07 到 08，股價大跌前），全距 150–203 美元；現價低於均值約一半，但日期早於跌勢，不作支持依據。股價自前份 137.86 美元回落約 37%，期間 EPS 指引上調，下跌原因事實表未涵蓋。上行空間：12 個月以基準 FY28 EPS 7.10 美元×14 倍＝99 美元（約 +14%）；三年以基準 FY30 EPS 9.30 美元×13 倍＝121 美元（約 +39%）。循環位置（需求量循環五訊號）：需求量仍在加速（CPI Q3 指引年增 105–115%）偏買；存貨年增 39% 偏賣；自身倍數在四年端點最高偏賣；雲端大廠約 1 兆美元擴建、缺料延續幾年，屬中後段；賣方目標價遠高於現價偏買。多數決為中循環，訊號互相矛盾，姿態為持有不加、不新建；trailing 本益比貼近自身高點，也不符新建條件。","premortem":"反證見反證紀錄。衰退訊號亮 2 個（EPS 成長遠高於營收、份額下滑估計），陷阱風險中等；FY27 自由現金流轉換率約 40% 若延續到 FY28 會亮第 3 個。壓力測試以基準 FY29 EPS 8.5 美元計：三年後成長降到 15%、倍數 14 倍＝119 美元，過；降到 10%、倍數 11 倍＝94 美元，勉強過；降到 5%、倍數 9 倍＝77 美元，不過，3 項過 2 項。最大回撤推導見情境假設。技術面：股價 86.25 美元在 52 週均線 95.07 美元之下、104 週均線 70.07 美元之上，250 週均線 13 週斜率 2.87%，排列過但長期斜率平緩；RSI 39.9，未過熱；26 週報酬 −5.2%。法說迴避：7 月 CPI 已裝產能中已認證比例、散熱市場規模、Amazon 協議分拆後歸屬三題未正面回答，10 月未補，散熱兩季都自稱早期。訴訟與監管：10-K 僅一般性提及，近 12 個月未見新案。"},"plain":{"six":{"how_it_makes_money":"Flex 賺的是電子製造的加工、整合與自有電源產品的錢；EMS 主體營益率只有 5–6%，錢主要卡在少數大客戶手上，真正拉高獲利的是 CPI（電源段營益率約 16%）。最新一季營收 84.9 億美元，調整後營益率 7.1%、GAAP 4.9%。","moat":"護城河方向持平（→），等級 C：執行力在擴大，三個部門營益率同步上升，但定價權沒有跟著擴大；雲端大客戶可內製或雙供應，聚合站估計 Flex 在同業中份額下滑，ROIC 19.2% 明顯低於 Celestica 的 39.5%。","growth":"五年後的成長跑道中等（🟡）：Flex 約占全球 EMS 的 5%，份額不是限制，但 CPI 的成長綁在雲端大廠資本支出上，FY29 以後能否延續沒有證據；散熱、固態變壓器、機器人都還在早期。","capital":"資本配置結論待驗：FY27 幾乎全部現金與新增債務投向 CPI 擴產（資本支出 15–16 億美元）與 EPC 收購（約 44 億美元），報酬尚未證實；SBC 稀釋低，回購與股利金額事實表未涵蓋。","valuation":"現價 87.03 美元若用 13 倍左右的成熟倍數，只要求 FY28 合併 EPS 約 6.7 美元、FY29 不衰退；共識 7.83 美元給了空間，我部分相信：FY28 有預訂與已建產能支撐，FY29 以後沒有證據。","how_wrong":"最可能看錯的地方是把資本支出循環的高峰獲利當常態：雲端大廠若在 2028 年進入消化期，合併 EPS 會回到 5 美元附近、倍數壓到 10 倍，股價約 50 美元；陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2026-11-10 投資人日或 Q3 FY27 法說給出 FY28 CPI 營收成長指引 ≥50%；達標後股價 ≤100 美元才首倉","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"EMS/ODM","price_at_dd":87.03,"week26_return_pct":-5.24,"consensus_rev_3m_pct":9.74,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母採合併口徑：公司指引明言未反映分拆，FY28 共識營收 463.7 億美元也約等於 CPI 再成長八成加 RMS＋ITS 個位數成長，判斷 Koyfin 共識同為合併口徑。分拆後 FLEX 代號的 EPS 會重編，持股人改持 Flex＋Axiom，合併口徑仍是現有股東的經濟分母。未扣項：Axiom 20 億美元可轉換特別股的股利或轉換稀釋、分拆後獨立營運成本（條件事實表未涵蓋）；SBC 年化約 1.7 億美元、稅後每股約 0.36 美元未扣，扣除後前瞻本益比約 18.5 倍。分母不是本案爭點，爭點在 FY28–FY29 能否成立。"},"catalysts":[{"date":"2026-11-10","date_precision":null,"type":"guidance","event":"投資人日：Flex 與 Axiom 管理層公布策略與 FY28 展望","impact":"高","watch":"FY28 CPI 營收成長與營益率、Axiom 客戶集中度、特別股條件"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q3 FY27 財報與法說（預計）","impact":"中","watch":"CPI 是否達年增 105–115%、存貨淨天數、自由現金流"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"CPI 分拆為 Axiom（預計 2027 年第一季）","impact":"高","watch":"完成時點、兩檔初始估值、Axiom 資本結構"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"USMCA 2026 年聯合檢討","impact":"中","watch":"協定是否修改或暫停；確切時點事實表未涵蓋"}],"_projected_from":"v19"}
```
