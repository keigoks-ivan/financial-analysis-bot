你是 stock-analyst v20 的**散文層（prose）agent**，標的 RCL（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：RCL　日期：2026-11-03　archetype：None　前份裁決：2026-07-29　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2990B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（452B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（715B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1288B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1126B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（430B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（933B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2070B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3547B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2580B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2990           2807-4010      3 條（2–6 內）  
s3                  8000         452           5284-7548      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3129          8310-11871      5 條（2–6 內）  
s6                 11000         430          7399-10570      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         933           1797-2567      5 條（2–6 內）  
s10                 5000        2070           2051-2930      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2580           2000-2420      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4272B；至少需散文≈40.73KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60
−60%
−48%
−40%
−40
−6.4%
−5%
−0.8%
−0.1%
0.0
0%
0
0.1%
0.1
0.15%
0.2
0.26
0.29
0.34
0.4%
0.4
0.45
0.5
0.6
0.6%
0.69
0.75
1%
1
1.0%
01
1.1
1.12
1.25
1.5%
1.5
1.7%
1.7
1.71
1.8
1.84
2%
2
02
2.1%
2.2
2.8
3
3%
03
3.0
3.5%
3.5
4%
04
4
4.04
4.3
4.5%
4.5
4.51
4.6
4.6%
5
5%
05
5.55%
5.6%
5.67
5.9
6%
6
6.57
6.6%
6.8
07
7%
7
7.2%
7.3%
7.9%
08
8%
8.0
8
8.05
8.5
8.8%
8.8
09
9%
9
9.4%
9.6
10
10%
10.5
10.9%
11
11%
11.4%
11.4
11.5%
11.6
12
12.5
13
13.5
13.8
13.94
14%
14
14.1%
14.4%
14.5
15
15.0
15%
15.5
15.61
15.7
15.78
15.8
16
16%
16.0%
16.1
16.5
16.6%
16.7
16.8
17
17.30
17.73
17.85
17.87
17.9
17.90
17.95
18.0
18
18.01
18.4
18.5
19
19.0
19.2
20%
20
20.0
20.01
20.4
20.43
20.5
20.7%
21.0
21
22.95
23%
23.0
23
23.3%
23.38
24
24.4
24.8%
24.9%
24.92%
25%
25
25.39
25.5
25.65
25.7%
26
26%
26.2%
27
27.38%
27.4%
27.6%
28
28.8%
28.9%
29%
29
30
30%
30.3
30.5
30.6%
31
31.8
33.5%
35%
35.6
38.13
38.80
40%
45%
45
48
49
49.06%
49.1%
49.35%
49.9%
50%
51.8
52.74
55%
55.9
56%
57
57%
58%
60
60%
67%
70
72.7
74
80
88.42
90
93
95%
100%
100
112%
133%
150%
164.85
165
167.87
170
179.34
190
194
194.25
200
223
250
274
290
$290
296
317
322.3
322.5
325
337
342
345
349
351
605.2
646
2024
2025
2026
2027
2028
2029
2031
2034
2036
20261103
3,830
4,030
9,400
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
{"meta":{"ticker":"RCL","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Royal Caribbean Cruises Ltd."},"oneliner":"郵輪業利潤率最高的一家，2027 年 20 美元 EPS 大概率達標；但現價已用 15.8 倍 FY2027 盈餘在利潤率高點定價，自由現金流又只有淨利三成上下，等回到約 296 美元再談","thesis":{"H":[{"id":"H1","text":"Perfecta 收尾兌現：FY2027 調整後 EPS 達 20 美元以上，靠運力 +4.5%、淨收益率溫和成長與成本紀律，不靠 Sandals 與回購","2y":"FY2027 調整後 EPS ≥ 20 美元、淨收益率（固定匯率）≥ +2%","5y":null,"10y":null,"threshold":"FY2026 調整後 EPS ≥ 17.85 美元（新指引下緣）；FY2027 ≥ 20.0 美元；FY2027 淨收益率（固定匯率）≥ +2%","source":"公司 Q3 2026 財報新聞稿與 2026-10-27 法說（CEO 稱依目前燃油遠期曲線 2027 年可達 20 美元以上，且不含 Sandals、回購、再融資）；FY2027 共識 20.43（Koyfin 快照 2026-10-31）","drift_rule":"FY2027 共識或公司指引連 2 季比 20.43 低 5% 以上→削弱；連 3 季低 10% 以上（約 18.4）→反轉"},{"id":"H2","text":"利潤率領先能守住：全球船廠產能受限壓住新增供給，加上硬體與私人目的地差異化，RCL 營業利益率維持同業最高","2y":null,"5y":"2031 年前 TTM 營業利益率不低於 24.8%，且對 CCL 差距 ≥ 8 個百分點","10y":null,"threshold":"TTM 營業利益率 ≥ 26.2%（現值 27.6% 的 95%）為健康，< 24.8% 為反轉線；對 CCL 營益率差距 ≥ 8 個百分點（現 11.6）；全業界年交付 ≤ 16 艘","source":"事實表同業對照（yfinance TTM）；CLIA 稱大型船訂單排到 2036；Cruise Industry News 2026 年訂單簿更新","drift_rule":"TTM 營益率連 4 季低於 26.2%（偏離現值 5%）→削弱；連 6 季低於 24.8%（偏離 10%）→反轉"},{"id":"H3","text":"資本週期轉正：新船交付放緩後，自由現金流追上淨利，股東回饋不再靠舉債","2y":null,"5y":"FY2028 自由現金流÷淨利 ≥ 0.6，Sandals 交割後淨負債÷調整後 EBITDA ≤ 3 倍","10y":null,"threshold":"FY2027 自由現金流÷淨利 ≥ 0.5、FY2028 ≥ 0.6（FY2025 為 0.29）；淨負債÷調整後 EBITDA ≤ 3.0 倍","source":"年度財報（事實表 financial_history，yfinance FY2023–FY2025）；FY2026 前 9 個月現金流量（Q3 財報）；2026-10-27 法說 CFO 稱槓桿低於 3 倍、2027 運力 +4.5%","drift_rule":"TTM 自由現金流÷淨利連 4 季低於 0.45→削弱；連 6 季低於 0.4→反轉"},{"id":"H4","text":"度假錢包份額擴大：跨品牌會員、河輪與 Sandals 把客戶留在體系內，郵輪之外長出第二條曲線","2y":null,"5y":null,"10y":"會員占旅客比例由 40% 升到 50% 以上；Sandals 權益法收益與管理層所稱數億美元綜效逐年兌現","threshold":"會員占比 ≥ 40% 且逐年上升；Sandals 交割後兩年內權益法收益進入指引且未認列減損","source":"2026-10-27 法說（CEO：40% 旅客為會員、約一半為回頭客、目前只拿到客人年度度假支出 20～25%，加入全包式度假村後可觸及約 50%）","drift_rule":"會員占比連 2 個年度未上升→削弱；連 3 個年度下降或 Sandals 認列減損→反轉"}],"R":[{"id":"R1","text":"加勒比運力集中投放引發降價：NCLH 2026 加勒比運力 +55%、MSC +23%，業界新船訂單約 93 艘、22.95 萬床位，RCL 運力 57% 在加勒比","h_ref":"H2","clock":"🔥","threshold":"FY2027 淨收益率（固定匯率）指引 < +1%，或公司稱加勒比收益率轉負","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#2"]},{"id":"R2","text":"地緣事件與燃油：中東衝突壓抑歐洲航程，2026-07 營收成長指引由 10% 降到約 9%；2026-04 曾因燃油把全年 EPS 指引中點由 17.90 下修到 17.30；歐洲占 2027 運力 16%","h_ref":"H1","clock":"⚡","threshold":"單季因地緣或燃油下修全年 EPS 指引 ≥ 3%，連 2 季發生","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","end_markets#2"]},{"id":"R3","text":"資本負擔吃掉股東經濟：在建新船約 165 億美元、約 49.9% 成本為歐元，可建船廠只有少數幾家，關稅與貿易制裁可能干擾供應鏈；再加上 Sandals 約 30 億美元舉債收購","h_ref":"H3","clock":"🔥","threshold":"淨負債÷調整後 EBITDA > 3.5 倍，或 FY2027 自由現金流÷淨利 < 0.4","evidence_refs":["geo_supply_chain#1","substitute_technology#1","reg_tariff_export#0"]},{"id":"R4","text":"目的地與法律風險：Mahahual 開發時程受影響且管理層兩季不評論；Havana Docks 案（原判約 1.12 億美元已被上訴法院推翻）最高法院 2025-10 受理，結果事實表未涵蓋","h_ref":"H2","clock":"🐢","threshold":"Mahahual 正式停建，或最高法院恢復原判且衍生其他古巴航線索賠","evidence_refs":["regulatory_antitrust#0","major_events#1","lawsuit_class_action#0"]}],"single_thing":{"description":"2027 年 1 月底 Q4 財報給出的 FY2027 首次調整後 EPS 指引中值低於 20 美元","why_fatal":"20 美元是市場把 RCL 從週期股改看成複利股的錨；共識 20.43 已在其上，跌破代表 FY2027 下修 5% 以上、FY2028 共識 23.38 跟著下修，同時退場倍數往週期股區間回落，兩者疊加估值約下修 25～30%（推估：盈餘 −5%、倍數 18 倍→14 倍）","if_happens":"撤出進場名單，重啟價位改為新指引中值的 12 倍；Perfecta 假設判反轉，利潤率領先假設重估","how_monitor":"Q4 2026 財報（預計 2027-01 底至 02 初）的 FY2027 指引；期間看每月共識快照、燃油遠期曲線與避險比例（Q4 2026 避險 58%）","probability":"約 15%（12–24 個月）：2026 與 2027 訂位進度領先往年且費率創紀錄，CEO 稱依目前燃油遠期曲線可達 20 美元以上；主要變數是燃油與匯率"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.78,"peg_fy2":1.1,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":15.61,"FY2026E":17.9,"FY2027E":20.43,"FY2028E":23.38},"fy_end_month":12,"eps_basis":"共識為調整後 EPS（Koyfin 快照 2026-10-31；共識營收為 yfinance 25 位分析師）；FY2025A 用 GAAP 稀釋 EPS 15.61（年度財報），公司稱 FY2026 指引年增 14%，隱含調整後基期約 15.7，差距約 0.6%"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"重資產、預收現金、運力受船廠排程限制；三年共識 EPS 年複合約 14%，但自由現金流只有淨利三成上下，景氣下行時盈餘彈性大"},"industry":{"clock_phase":"III","sd_verdict_source":"供給結構性受限、需求週期性：CLIA 稱大型船訂單排到 2036、2027 年約 15 艘約 2.8 萬床位交付；需求面 CLIA 預測 2026–2029 全球乘客個位數成長，NCLH 預期 2027 上半年需求仍弱","bargaining":{"up":"船廠議價權強：可建大型船的船廠少，RCL 在建船約 165 億美元、約 49.9% 成本以歐元計（2026-09-30 10-Q）","down":"客戶為分散個人消費者，無單一大客戶；旅行顧問仍是重要通路，佣金需維持競爭力","geo":"客源以美國為主（FY2020 10-K 美國占船票營收 67%，資料偏舊）；運力過半在加勒比"},"profit_pool_dir":"利潤池向頭部集中：TTM 營益率 RCL 27.6%、VIK 23.3%、CCL 16.0%、NCLH 10.9%","tam_table":{"expanded":false,"reason":"核心郵輪屬成熟市場，事實表未涵蓋郵輪滲透率與利潤池分段歷史；Sandals 全包式度假村是新品類，但公司稱 2027 年貢獻不重大，不承重本次估值"}},"moat":{"mechanism":"規模＋硬體差異化（Icon 級新船載客率 133%、NPS 80 以上）＋自有私人目的地＋跨品牌會員（約一半回頭客、40% 為會員），轉成定價溢價與單位成本優勢","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"營益率 FY2023 20.7%→FY2024 24.9%→FY2025 27.4%→TTM 27.6%，每年擴張幅度由 2～4 個百分點降到 0.2；FY2026 淨收益率約 +2.1%（固定匯率），低於年初指引區間 1.5–3.5% 的中點；2026 加勒比運力 RCL +9%，NCLH +55%、MSC +23%","peer_na_reason":"事實表同業對照只有利潤率、沒有投入資本，無法算同業 ROIC 差距；改用營益率差距，且只有單一 TTM 時點","threats":[{"level":"🟡","text":"加勒比對手運力集中投放（NCLH +55%、MSC +23%）與業界新船訂單約 93 艘，區域價格競爭；目前 RCL 加勒比收益率仍為正","p":"35%","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#2"]},{"level":"🟡","text":"陸上全包式度假村與主題樂園爭奪同一筆度假預算；管理層自承郵輪價格漲幅落後陸上，並以 Sandals 50% 股權因應","p":"25%","evidence_refs":["substitute_technology#3","substitute_technology#2"]},{"level":"🟡","text":"旅行顧問通路：佣金若不具競爭力，顧問會轉賣對手產品；公司同步投資自有網站與 App","p":"15%","evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#0"]},{"level":"🟡","text":"技術落後或 AI 應用失誤的通用風險，10-K 未點名具體取代技術；郵輪是實體體驗，AI 較可能是工具而非替代","p":"10%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多為同一家庭，三角色一致；但度假屬可延後的「想要」。Q2 法說（2026-07-28）CEO 稱消費者花錢更審慎、偏好近程，Q3 法說改稱訂位加速、2027 費率創紀錄：目前需求強，本質仍是景氣轉差時最先延後的支出"},{"item":"決策層級","level":"🟡","text":"客戶在「這次去哪度假」的層級選擇，CEO 稱客戶不是拿 RCL 換別家郵輪，而是換陸上度假；代理變數：回頭客約一半、會員占 40%、跨品牌旅客單日消費較高。但沒有合約或轉換成本，留存靠產品力而非鎖定"},{"item":"價值鏈分配","level":"🟡","text":"上游船廠集中（兩家承建、約 49.9% 成本為歐元）分走部分價值；旅行顧問收佣；目的地港口與政府收稅費。RCL 以自有私人目的地（2028 年前由 3 個增至 8 個）把岸上消費留在體系內，是少數能從其他環節搶回價值的做法"},{"item":"社會容忍度","level":"🟡","text":"目的地社區與政府的容忍度是上限：Mahahual 開發時程已受影響，兩季法說都不評論進度；環保法規與目的地稅費會抬高成本。航運所得稅務地位與碳排成本數字事實表未涵蓋，列資料缺口"}],"roiic":20,"reinvest_rate":57,"endo_ceiling":11.4,"formula_note":"當期 ROIC：事實表未涵蓋投入資本，管理層稱已達 Perfecta ROIC 目標，數字未核實。再投資率＝FY2023–FY2025 累計（淨利−自由現金流）÷累計淨利＝（88.42−38.13）÷88.42 億美元≈57%（以淨利代稅後營業利益、以自由現金流缺口代淨再投資，含預收款變動，屬粗估）。增量報酬＝FY2024→FY2025 營業利益增加約 8.0 億美元（164.85 億×24.92%→179.34 億×27.38%）÷FY2025 淨再投資約 30.3 億美元≈26%；疫後收益率回升殘差會高估、新船當年未滿載會低估，取 20% 為中值（區間 15–26%）。內生成長上界＝20%×57%≈11.4%"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","RCL":49.06,"VIK":43.21,"NCLH":40.57,"CCL":39.47,"unit":"%"},{"metric":"營業利益率","RCL":27.56,"VIK":23.27,"NCLH":10.85,"CCL":15.99,"unit":"%"},{"metric":"FCF 利潤率","RCL":7.89,"VIK":16.56,"NCLH":-6.36,"CCL":11.51,"unit":"%"}],"competitors":[{"name":"VIK","gm":43.21,"om":23.27,"fcf_margin":16.56,"strategy_note":"河輪與小型遠洋、高價位熟齡客群，TTM 營益率 23.3%、自由現金流利潤率 16.6% 高於 RCL，資本負擔較輕；RCL 2027 年進入河輪後正面相遇","period":"TTM ending 2026-06-30（4季加總）"},{"name":"NCLH","gm":40.57,"om":10.85,"fcf_margin":-6.36,"strategy_note":"2026 年加勒比運力 +55% 最激進，TTM 營益率 10.9%、自由現金流利潤率 −6.4%，並預期 2027 上半年需求仍弱，最可能在加勒比以價格搶客","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CCL","gm":39.47,"om":15.99,"fcf_margin":11.51,"strategy_note":"最大運力、偏大眾價位，TTM 營益率 16.0%，比 RCL 低約 11.6 個百分點；稱 2027 約半數已訂、價格創紀錄，需求面與 RCL 同向","period":"TTM ending 2026-08-31（4季加總）"}]},"growth":{"driver_mix":"量＋價為主：運力每年 +4.5～7%、淨收益率約 +2%，加上成本約持平的營業槓桿與淨回購；Sandals 2027 年貢獻公司稱不重大","runway_years":"≥10（推估；郵輪滲透率事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"內生成長上界約 11.4%（增量報酬約 20%×再投資率約 57%）；三年共識 EPS 年複合約 14.4%，缺口約 3 個百分點歸因利潤率擴張與淨回購，可歸因","segments":{"expanded":false,"reason":"公司只報單一郵輪分部，品牌別營收事實表未涵蓋；部署區域占比已寫進怎麼賺錢一題，利潤 mix 的承重點在加勒比收益率，已設為風險與觸發條件"},"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；TTM 49.06% 對 FY2025 49.35% 小幅回落，列觀察"},{"item":"核心市占近 12 個月縮減","lit":false,"evidence":"加勒比運力份額被稀釋（RCL +9% 低於 NCLH +55%、MSC +23%），但 RCL 加勒比收益率仍為正，營收份額未見縮減，列觀察"},{"item":"主力產品提價後銷量下滑","lit":false,"evidence":"Q3 載客率 112%，2027 訂位量年增高十幾%且費率創紀錄"},{"item":"EPS 成長顯著高於營收成長","lit":true,"evidence":"FY2027 共識 EPS +14.1% 對共識營收 +7.3%，差 6.8 個百分點"},{"item":"自由現金流÷淨利連 2 年 < 0.75","lit":true,"evidence":"FY2024 0.69、FY2025 0.29，主因新船資本支出"},{"item":"SBC 占營收 > 5% 且逐年上升","lit":false,"evidence":"前 9 個月 SBC 9,400 萬美元，不到營收 1%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"CLIA 預測乘客 2026 年 3,830 萬→2027 年 4,030 萬"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"P/S、EV/S 都在近 4 個年度端點最高位"},{"item":"維持性資本支出占自由現金流 > 60%","lit":false,"evidence":"維持性資本支出事實表未涵蓋，無法判斷"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"2027 仍有 Hero of the Seas 與河輪加入，營收持續成長"}],"trap_rating":"🟡（亮 2 項）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠新船運力與收益率，不靠併購；Sandals 交割後才有併購報酬可驗，股利與回購數字已寫在判讀句"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"尚無已實現併購：Sandals 50% 股權約 30 億美元（10 倍前瞻 EBITDA）預計 2027 年初交割，報酬待驗","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"以約 18 倍本益比回購，盈餘殖利率約 5.6%，僅與 2026-08 新發 2034 年票據利率 5.55% 相當；10 年期公債殖利率與回購均價事實表未涵蓋，無法判過或不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"前 9 個月 SBC 9,400 萬美元，年化約 1.25 億，約為市值 0.15%，遠低於 1.5%；股數變化事實表未涵蓋","grade":"過"}]},"valuation":{"basis":"Fwd P/E：FY2026E 共識調整後 EPS 17.90，現值 18.0 倍；FY2027E 20.43 對應 15.8 倍","tier":"大型上市郵輪（與 CCL、NCLH、VIK 同層）","peers":{"expanded":false,"reason":"事實表同業對照只含毛利率、營益率、自由現金流利潤率，未含同業倍數，無法建立倍數對照"},"fwd_pe":18.01,"peg":1.25,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"PEG 約 1.25（Fwd P/E 18.0÷三年共識 EPS 年複合約 14.4%）落在合理區；但分母是利潤率歷史高點的盈餘（TTM 營益率 27.6%，FY2023 為 20.7%），P/S 4.51 倍、EV/S 5.67 倍都在近 4 個年度端點最高位；5 年本益比分位事實表未涵蓋（只有 3 個年度端點，51.8 分位不能當 5 年分位）。週期性重資產公司在利潤率高點給 18 倍當年本益比，定為偏貴","upside_short_pct":4.6,"upside_mid_pct":8.8},"trap_analysis":{"verdict":"🟡","label":"亮 2 項：EPS 成長快於營收、自由現金流轉換率偏低"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"業界新船訂單約 93 艘、對手加勒比運力大增；NCLH 預期 2027 上半年需求仍弱；有分析師質疑船上消費能否轉成 2027 票價；Q2 法說 CEO 稱消費者花錢更審慎","assumption":"2027 訂位年增高十幾%與創紀錄費率能延續到 2028","consequence":"2028 消費衰退疊加加勒比降價，淨收益率轉負、EPS 回到 15～16 美元，市場改用週期股 10～11 倍定價，五年後股價約 190 美元（−40%）","ruling":"部分採納：列為 Bear 30% 機率；不再往上調，因為 2026、2027 訂位都領先往年、費率創紀錄，12 個月內需求斷崖的證據不足。與唯一致命點部分重疊：FY2027 指引跌破 20 美元是這個故事最早能看到的訊號","watch":"FY2027 首次指引、Q1 2027 淨收益率、加勒比收益率是否轉負","not_applicable_reason":null,"evidence_refs":["supply_demand_durability#2","end_markets#2","supply_demand_durability#4"]},{"view":"論點成功但股東經濟變差","evidence":"FY2025 自由現金流只有淨利 29%，股利已約等於自由現金流；在建新船約 165 億美元、近半以歐元計價，可建船廠少、議價權在船廠，關稅與貿易制裁可能干擾供應鏈；Sandals 30 億美元舉債收購","assumption":"2027 年後運力成長放緩、資本支出下降，自由現金流自然追上淨利","consequence":"EPS 照樣達標，但新船成本因歐元與關稅上升、Sandals 綜效延後，自由現金流長期停在淨利三到五成，回購靠舉債，股東實拿報酬低於 EPS 成長","ruling":"採納：列入資本週期假設與資本負擔風險監測；這是本次最被市場忽略的一點，也是不給更高 Base 倍數的原因之一","watch":"TTM 自由現金流÷淨利、淨負債÷調整後 EBITDA、新船訂單金額與歐元匯率","not_applicable_reason":null,"evidence_refs":["geo_supply_chain#1","reg_tariff_export#0","substitute_technology#1"]},{"view":"價格已反映太多","evidence":"現價為 FY2026E 18.0 倍、FY2027E 15.8 倍；P/S 與 EV/S 都在近 4 個年度端點最高位；26 週漲 25.7%、RSI 72.7；Freedom Capital 2026-07 降評至持有，Q3 後 Barclays、BofA 下修目標價","assumption":"市場會繼續以複利股而非週期股替 RCL 定價","consequence":"即使盈餘照共識走，倍數由 18 倍回到 15 倍就吃掉約一年半的盈餘成長，五年 Base 年化報酬只剩約 9%","ruling":"採納：這是觀望的主因，價格回到 FY2027 共識 14.5 倍（約 296 美元）以下才重啟","watch":"股價÷FY2027 共識 EPS、賣方目標價變化","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#4","capital_markets_pricing#3"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 322.5 → 本次 322.3（-0.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=322.5","side_b":"本次 price_at_dd=322.3","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 322.5 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 322.5 美元：Bull 價 646、Bear 價 170，五年期望值 +30.6%，基準年化 9.4%，不對稱比 1.8","side_b":"本次情境、股價仍用 322.5 美元：Bull 價 605.2、Bear 價 194.25，五年期望值 +28.8%，基準年化 7.2%，不對稱比 1.84","ruling":"先換情境、股價不動：五年期望值少 1.8 個百分點，基準年化少 2.2 個百分點。不對稱比由 1.8 變為 1.84。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 322.5 美元：五年期望值 +28.8%，基準年化 7.2%，不對稱比 1.84","side_b":"本次情境、股價 322.3 美元：五年期望值 +28.9%，基準年化 7.3%，不對稱比 1.84","ruling":"再換股價、情境不動：起點價下跌 0.1%，五年期望值多 0.1 個百分點，基準年化多 0.0 個百分點，不對稱比由 1.84 升到 1.84。合計五年期望值比前份少 1.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"現在就買 vs 等價格","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：Perfecta 三年 EPS 年複合約 20% 已近兌現，FY2027 本益比 15.8 倍換約 14% 的三年 EPS 成長（PEG 約 1.1），2026、2027 訂位都領先往年且費率創紀錄，利潤率同業最高、仍在擴張","side_b":"等價格的理由：現價用利潤率歷史高點的盈餘給 18 倍當年本益比，Base 五年年化約 9%、上下檔比約 1.8 屬平庸；自由現金流只有淨利約三成；RSI 72.7 偏熱；加勒比對手運力大增、收益率成長已放緩到約 2%","ruling":"不可調和（買或等，方向相反），選等價格。依據：上檔不足以補償 30% 機率的 Bear（五年 −40%）；硬數據點是 FY2027 本益比 15.8 倍對比重啟門檻 14.5 倍。執行上用價格解：價格到位就買，證據先轉壞就延後","evidence_level":"事實表數字＋公司財報指引（一手）","settle_metric":"股價÷FY2027 共識 EPS；2027-01 底 FY2027 首次指引","if_then":["若股價跌到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）且基本面無損，則重跑判斷、分批反買，首筆不超過目標倉位三分之一","若股價續漲但 FY2027 指引尚未公布，則不追","若 FY2027 首次指引中值低於 20 美元，則不追，重啟價位改為新指引中值的 12 倍","反向條件（等待證實為錯）：若 2027-04 Q1 財報淨收益率（固定匯率）扣除約 200 個基點逆風後仍 ≥ +2%，且全年指引中值 ≥ 20.5 美元，則把重啟倍數上調到 15.5 倍（約 317 美元）重跑判斷"],"evidence_refs":["capital_markets_pricing#3","end_markets#0"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"2026-07-28 Q2 法說：CEO 稱 2027 訂位與往年相當、價格創紀錄，消費者花錢更審慎、偏好近程；CFO 預告 Q3 淨收益率約持平、全年 EPS 17.73～17.87","side_b":"2026-10-27 Q3 法說：Q3 淨收益率 +0.6%，高於指引約 60 個基點，EPS 6.57 高於指引中點 0.26；CEO 改稱 2027 訂位領先往年、2027 航次訂位年增高十幾%；但分析師追問「高十幾%」是年增還是季增時，CEO 未正面回答","ruling":"可調和：財測兌現紀錄良好（全年 EPS 指引上調到 17.85～17.95，回到年初中點 17.90），採信方向；但「高十幾%」口徑不明，標為未證、以 Q1 2027 淨收益率驗證","evidence_level":"公司法說逐字稿（一手）","settle_metric":"Q1 2027 淨收益率（固定匯率）扣除約 200 個基點結構性逆風後是否為正","if_then":["若 Q1 2027 淨收益率（固定匯率）< 0%，則視 2027 訂位說法落空，Bear 機率上調到 35%"],"evidence_refs":["end_markets#1","supply_demand_durability#0"]},{"axis":"訂位量與收益率","cause":null,"prior_field":null,"side_a":"訂位：自上次法說以來訂位量年增中段十幾%、2027 航次訂位年增高十幾%，費率創紀錄","side_b":"收益率：Q3 淨收益率僅 +0.6%（固定匯率），報表口徑毛利收益率 −0.8%；全年約 +2.1%，低於年初區間 1.5–3.5% 的中點；NCLH 預期 2027 上半年需求仍弱","ruling":"可調和（程度差異）：量的成長大部分來自運力與短航程產品，單價成長溫和；Base 只給 2027 收益率 +2～3%","evidence_level":"公司財報＋同業說法","settle_metric":"FY2027 淨收益率指引","if_then":["若 FY2027 淨收益率指引 < +1%，則重啟價位下修到 FY2027 EPS 13 倍"],"evidence_refs":["supply_demand_durability#0","end_markets#4","supply_demand_durability#4","end_markets#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：NCLH 2026 加勒比運力 +55%、MSC +23%，業界訂單約 93 艘、22.95 萬床位，區域競爭惡化中","side_b":"結構：大型船廠排到 2036、2027 年約 15 艘交付，全球供給受限；其他結構變數：Sandals 擴到全包式度假村、私人目的地 2028 年前增至 8 個，通路仍倚重旅行顧問，未見反壟斷行動","ruling":"雙向拉鋸：加勒比區域競爭惡化與全球供給受限同時成立，前者壓 2026–2027 收益率，後者撐長期定價地板","evidence_level":"產業媒體＋CLIA＋公司 10-K","settle_metric":"加勒比收益率方向、年度新船交付艘數","if_then":["若全業界年交付超過 16 艘，則供給受限論點削弱、Base 退場倍數降到 13.5 倍"],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#3","competitive_share_entrants#2","channel_business_model_shift#1"]},{"axis":"估值、評級與機率（股價幾乎未動）","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-07-29，股價 322.5）：估值偏貴、整體評級 B、Bull／Bear 機率 25%／30%、最大回撤 −60%、觀望","side_b":"本次（股價 322.3）：估值偏貴、整體評級 B、機率 25%／45%／30%、最大回撤範圍 −40%～−60%","ruling":"股價幾乎不變；FY2027 共識上修約 2% 讓 FY2027 本益比由 16.1 倍降到 15.8 倍，幅度不足以改變估值結論。機率維持，因 Q3 的利多（指引上調、訂位領先）與利空（收益率放緩、對手運力大增）互相抵銷。裁決與角色由程式依本輪輸入重算","evidence_level":"事實表價格與共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：護城河方向擴大（↑）","side_b":"本次：穩定（→）","ruling":"新證據：營益率擴張幅度由每年 2～4 個百分點降到 0.2（FY2025 27.4%→TTM 27.6%）；FY2026 淨收益率約 +2.1%，低於年初區間中點，Q3 報表口徑毛利收益率 −0.8%；2026 加勒比對手運力 NCLH +55%、MSC +23%。執行面仍擴大，定價面轉穩定，合判穩定","evidence_level":"公司財報＋產業媒體","settle_metric":"TTM 營業利益率、FY2027 淨收益率","if_then":["若 FY2027 淨收益率 ≥ +3% 且營益率再擴張 1 個百分點以上，則方向回調為擴大"],"evidence_refs":["supply_demand_durability#2","competitive_share_entrants#2","end_markets#4"]},{"axis":"價值陷阱風險","cause":"方法變動","prior_field":["trap"],"side_a":"前份：價值陷阱風險低（🟢）","side_b":"本次：中等（🟡），十項衰退信號逐條檢查亮 2 項","ruling":"前份未逐條套用衰退信號清單；本次逐條檢查：EPS 成長快於營收（FY2027 共識 EPS +14.1% 對營收 +7.3%，差 6.8 個百分點）與自由現金流÷淨利連 2 年低於 0.75（FY2024 0.69、FY2025 0.29）兩項亮燈。後者主因新船資本支出、屬成長投資，但仍真實壓低股東可拿的現金，故由低調到中等","evidence_level":"年度財報＋共識快照","settle_metric":"FY2027 自由現金流÷淨利","if_then":["若 FY2027 自由現金流÷淨利 ≥ 0.6，則該項熄燈、陷阱風險回到低"],"evidence_refs":[]},{"axis":"跑道、類型與循環位置","cause":"新證據","prior_field":["runway_post_y5","archetype","cycle_position"],"side_a":"前份：中長期跑道寬（🟢）、品質複利成長型、晚循環","side_b":"本次：三項判斷維持，次要類型另標循環型","ruling":"Q3 新證據支持維持：Sandals 全包式度假村（CEO 稱可觸及度假支出由 20～25% 擴到約 50%）、河輪 2027 開航、私人目的地 2028 年前增至 8 個，是有來源的第二條曲線；利潤率在高點、收益率成長放緩，仍屬晚循環。次要類型標循環型，反映自由現金流與景氣敏感度","evidence_level":"公司法說（一手）","settle_metric":"Sandals 交割後權益法收益、會員占比","if_then":["若 Sandals 交割延後超過 2027 年底或認列減損，則跑道下修一檔"],"evidence_refs":["substitute_technology#2","channel_business_model_shift#1"]},{"axis":"重啟進場門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd P/E(FY2027E) ≤ 14.5x（約 $290）；或 FY27 共識上修使該倍數自然回落至 14.5x 以下","side_b":"股價回到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）才重啟進場；倍數沿用前份，價位隨共識上修由 290 上移","ruling":"倍數門檻 14.5 倍不變；FY2027 共識由前份的 20.01 上修到 20.43，對應重啟進場價位由約 290 美元上移到約 296 美元","evidence_level":"共識快照","settle_metric":"股價÷FY2027 共識 EPS","if_then":[],"evidence_refs":[]},{"axis":"假設門檻","cause":"新證據","prior_field":null,"side_a":"前份：FY2026 調整後 EPS ≥ 17.73 美元（當時指引下緣）；FY2027 ≥ 20.0","side_b":"本次：FY2026 ≥ 17.85 美元（2026-10-27 上調後指引下緣）；FY2027 ≥ 20.0 不變","ruling":"公司兩度上調指引，門檻隨新指引下緣上移","evidence_level":"公司財報新聞稿","settle_metric":"FY2026 實績","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 補設","cause":"方法變動","prior_field":null,"side_a":"前份未設定唯一致命點（null）","side_b":"2027 年 1 月底 Q4 財報給出的 FY2027 首次調整後 EPS 指引中值低於 20 美元","ruling":"本次補設：FY2027 指引跌破 20 美元會同時打到盈餘與退場倍數，是數學上最大的單一敏感項","evidence_level":"公司法說（一手）","settle_metric":"FY2027 首次指引中值","if_then":["若指引中值 < 20 美元，則撤出進場名單、重啟價位改為新指引中值的 12 倍"],"evidence_refs":[]},{"axis":"清倉／減碼門檻（kill 指標）","cause":"方法變動","prior_field":null,"side_a":"前份未設 kill 指標（null）；前份 H2 反轉條件為 FY2027 共識跌破 18.5 美元","side_b":"本次四條：FY2027 首次指引中值 < 19 美元；FY2027 淨收益率 < +1%；FY2027 共識跌破 18.5 美元；Sandals 交割後淨負債÷調整後 EBITDA > 3.5 倍。持有中觸發任一即減碼一半、兩條以上清倉；未持有則撤出進場名單","ruling":"補上可監測的出場門檻；18.5 美元共識底線沿用前份，其餘三條為本次新增","evidence_level":"公司財報＋共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2027 本益比回到 14.5 倍以下才重啟進場","type":"估值rearm","maps_to":"H1","metric":"股價÷FY2027 共識調整後 EPS","threshold":"≤ 14.5 倍（現約 296 美元）","action":"重跑判斷；通過後分批反買，首筆不超過目標倉位三分之一","source_freq":"每日股價、每月共識快照","date":null,"evidence_refs":["capital_markets_pricing#4"]},{"n":2,"text":"FY2027 首次指引中值跌破 20 美元","type":"Single Thing","maps_to":"H1","metric":"公司 FY2027 調整後 EPS 指引中值","threshold":"< 20.0 美元","action":"撤出進場名單；重啟價位改為新指引中值的 12 倍；H1 判反轉","source_freq":"Q4 2026 財報一次","date":"2027-01"},{"n":3,"text":"營業利益率領先失守","type":"假設驗證","maps_to":"H2","metric":"TTM 營業利益率","threshold":"連 4 季 < 26.2% 削弱；連 6 季 < 24.8% 反轉","action":"削弱時 Base 退場倍數由 15 倍降到 13.5 倍重算；反轉時改以週期股框架重做判斷","source_freq":"每季財報","date":null},{"n":4,"text":"自由現金流追不上淨利","type":"假設驗證","maps_to":"H3","metric":"自由現金流÷淨利","threshold":"FY2027 < 0.5","action":"Bear 機率上調到 35%，重啟價位改為 FY2027 EPS 13.5 倍","source_freq":"年度財報、每季現金流量","date":"2028-02"},{"n":5,"text":"加勒比降價擴散到全年收益率","type":"風險","maps_to":"R1","metric":"全年淨收益率（固定匯率）","threshold":"FY2027 指引 < +1%，或公司稱加勒比收益率轉負","action":"Bear 機率上調到 35%；重啟價位下修到 FY2027 EPS 13 倍","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":6,"text":"地緣或燃油再度迫使下修指引","type":"風險","maps_to":"R2","metric":"全年 EPS 指引因地緣或燃油下修幅度","threshold":"單季下修 ≥ 3%，連 2 季","action":"不追；若已持有則減碼三分之一","source_freq":"每季財報、燃油遠期曲線","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","end_markets#2"]},{"n":7,"text":"資本負擔超出投資級框架","type":"風險","maps_to":"R3","metric":"淨負債÷調整後 EBITDA","threshold":"Sandals 交割後 > 3.5 倍","action":"Bear 機率上調到 35%；若已持有則減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["geo_supply_chain#1","substitute_technology#1","reg_tariff_export#0"]},{"n":8,"text":"目的地或訴訟出現不利定案","type":"風險","maps_to":"R4","metric":"Mahahual 開發狀態；Havana Docks 案最高法院判決","threshold":"Mahahual 正式停建，或最高法院恢復原判且衍生其他古巴航線索賠","action":"重估西加勒比部署與法律負債；涉及集體索賠時暫停進場計畫","source_freq":"法說、8-K、法院判決","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#1","lawsuit_class_action#0"]},{"n":9,"text":"Q4 財報後複審","type":"複審日期","maps_to":null,"metric":"FY2027 首次指引與 2027 訂位進度","threshold":"財報公布後一週內","action":"重跑完整判斷","source_freq":"一次","date":"2027-02-05"}],"kill_metrics":[{"metric":"公司 FY2027 調整後 EPS 首次指引中值","bear_threshold":"< 19.0 美元（比共識 20.43 低約 7%）","window":"2027-01 底 Q4 2026 財報","source":"公司財報新聞稿（8-K）","last_status":"unknown"},{"metric":"全年淨收益率成長（固定匯率）","bear_threshold":"FY2027 指引或實績 < +1.0%","window":"2027 全年，按季追蹤","source":"公司季報與法說","last_status":"ok"},{"metric":"FY2027 共識調整後 EPS","bear_threshold":"跌破 18.5 美元","window":"滾動 2 季","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"淨負債÷調整後 EBITDA","bear_threshold":"> 3.5 倍","window":"Sandals 交割後每季","source":"公司季報","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=25.65, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='RCL 的爆發情境缺少「運力 × 收益率 → 營收 → EPS」的逐步算術，第二條成長曲線（Sandals）真實存在，但還沒有可驗證的營收或盈餘數字。這些依據大多只能算作未證實，本次沒有發現足以否定的反證。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價回到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）才重啟進場；倍數沿用前份，價位隨共識上修由 290 上移","exec_line":"未持有，不追；到價先重跑判斷，再分批進場，首筆不超過目標倉位三分之一；FY2027 首次指引跌破 20 美元則撤出進場名單"},"reasoning":{"industry":"收錢方式：先收訂金後出航，營收＝船票＋船上消費；Q3 營收年增 9%＝運力 +8%＋淨收益率 +0.6%（固定匯率）。部署：2026 年加勒比占運力 57%、歐洲 15%、阿拉斯加 5%；2027 年加勒比 56%、歐洲 16%、亞太 11%（2026-10-27 法說 CFO）。船票與船上消費的拆分、品牌別營收事實表未涵蓋。單點依賴：加勒比占運力過半；新船集中在 Meyer Turku 與 Chantiers de l'Atlantique 兩家船廠，屬供應商集中風險；客戶為分散個人，無大客戶。供需持久性：供給端結構性受限（大型船廠訂單排到 2036、2027 年全業界約 15 艘交付），需求端屬可延後的週期性消費；加勒比區域運力 2026 年 NCLH +55%、MSC +23%，區域供給可逆性高。產業時鐘判 III：利潤率在歷史高點（營益率 FY2023 20.7%→FY2025 27.4%→TTM 27.6%），淨收益率成長已放緩到全年約 2.1%，對手運力集中投放加勒比，屬擴張後段。","moat":"機制：規模＋硬體差異化＋自有私人目的地＋跨品牌會員，轉成定價溢價與單位成本優勢。證據：TTM 毛利率 49.1%、營益率 27.6%，分別高於 CCL 9.6 與 11.6 個百分點、高於 NCLH 8.5 與 16.7 個百分點、高於 VIK 5.9 與 4.3 個百分點；Icon 級新船載客率 133%、NPS 80 以上（2026-10-27 法說，品牌總裁 Bayley）；約一半旅客為回頭客、40% 為會員。同業 ROIC 差距無法計算（事實表無投入資本），改用營益率差距，且只有一個 TTM 時點，差距方向無法驗證。方向：執行面仍擴大（營益率續升、不含燃油單位成本約持平），定價面由擴大轉穩定（淨收益率放緩到全年約 2.1%，Q3 報表口徑毛利收益率 −0.8%），合判穩定。反例：VIK 自由現金流利潤率 16.6% 遠高於 RCL 7.9%，代表 RCL 的利潤率優勢有一部分是靠更重的資本投入換來。評分：執行 8、定價 7。","growth":"成長拆解：量（運力 2026 +6.6%、2027 +4.5%，Q1 2026 財報稿稱 2028 +6%、2029 +7%）＋價（淨收益率 2026 約 +2.1%，2027 公司未給，且 Q1 有約 200 個基點結構性逆風）＋成本（不含燃油單位成本約持平帶來營業槓桿）＋淨回購。三年共識 EPS 年複合約 14.4%（FY2025A 15.61→FY2028E 23.38），但 FY2027 共識營收只成長 7.3%，差額靠利潤率與每股化。再投資報酬推導的內生成長上界約 11.4%，缺口約 3 個百分點主要歸因利潤率擴張（營業槓桿），其次淨回購；財務費用變化方向事實表未涵蓋。跑道：10-K 稱公司在逾兆美元度假市場占比小，CEO 稱目前只拿到客人年度度假支出的 20～25%，加入全包式度假村後可觸及約 50%；限制主要在船廠交付而非需求。反例：CLIA 預測 2028–2029 全球乘客只成長約 2%，若第二曲線遲遲不貢獻，跑道會比判斷窄。","governance":"自由現金流轉換率偏低：FY2023／2024／2025 自由現金流÷淨利＝0.34／0.69／0.29（年度財報，事實表 financial_history，yfinance）；FY2026 前 9 個月自由現金流 13.94 億美元（營運現金流 52.74 億−資本支出 38.80 億），TTM 自由現金流利潤率 7.9%，低於 CCL 11.5%、VIK 16.6%。主因新船資本支出；2027 運力成長降到 4.5%，資本支出有機會放緩，但金額事實表未涵蓋。現金去向：資本支出為大宗；Q2 回饋股東逾 6 億美元（股利 4.04 億美元＋回購），剩餘回購額度 8.05 億美元（2026-07-28 法說 CFO）；股利殖利率 1.7%，年化股利約 14～15 億美元，與自由現金流相當，回購與 Sandals 實質靠舉債與再融資（2026-08 發行 12.5 億美元 5.55% 2034 年票據償還浮動利率貸款；Sandals 由 Morgan Stanley 承諾融資）。三年現金去向四分事實表未涵蓋。資產負債表：淨負債 223 億美元、流動性 74 億美元、槓桿低於 3 倍、S&P 2026-02 升到 BBB。","valuation":"現價＝FY2026E 共識 17.90 的 18.0 倍、FY2027E 20.43 的 15.8 倍、FY2028E 23.38 的 13.8 倍；三年共識 EPS 年複合約 14.4%，PEG 約 1.25（FY2027 口徑約 1.1）。現價要求三件事：2027 年 20 美元以上兌現、之後每年約 10% 成長、退場倍數不跌回週期股區間。第一項有訂位與指引支撐，第三項依賴市場繼續把 RCL 當複利股。短期上檔：FY2027E 20.43×16.5 倍≈337 美元（+4.6%）；約兩年：FY2028E 23.38×15 倍≈351 美元（+8.8%）。賣方目標價平均約 345～349 美元，Q3 後 Barclays、BofA 下修目標價到 342、325。動能：26 週漲 25.7%、RSI 72.7 偏熱，同期盈餘預估上修遠小於股價漲幅（FY1 近 3 個月僅 +1.0%），漲幅主要來自倍數回升。同業倍數事實表未涵蓋。","premortem":"三視角反證寫在反證紀錄。最大回撤推估 −40%～−60%：250 週均線 167.87 美元距現價約 −48%；Bear 五年終點約 194 美元（−40%）；淨負債約為市值 26%，衰退時槓桿放大跌幅。路徑風險偏高，但論點未破，屬深回撤心理準備，不是砍倉理由。衰退信號亮 2 項（FY2027 共識 EPS +14.1% 對營收 +7.3%；自由現金流÷淨利連 2 年低於 0.75），陷阱風險中等。反例：若 2027 年運力成長降到 4.5% 後資本支出明顯下降，自由現金流這一項會自然熄燈。"},"plain":{"six":{"how_it_makes_money":"賺北美為主度假客的船票與船上消費，錢卡在「自有新船＋私人目的地」這一節：Q3 營收 55.9 億美元、營業利益率 33.5%，TTM 營益率 27.6% 為上市同業最高","moat":"護城河 B 級、方向穩定（→）：利潤率仍是同業最高，但收益率成長放緩、加勒比對手運力大增，前幾年的擴大趨勢暫停","growth":"中長期跑道寬：郵輪在兆美元度假市場占比小，Sandals、河輪與私人目的地是有來源的第二條曲線；但未來三年約 14% 的 EPS 成長有約 3 個百分點不是內生","capital":"資本配置中等：SBC 稀釋輕、資產負債表升到投資級，但自由現金流只有淨利三成上下，股利已吃掉大半，回購與 Sandals 靠舉債支應，回購報酬是否跑贏資金成本無法驗證","valuation":"現價 322.3 美元要求 FY2027 調整後 EPS 達 20 美元以上、之後每年再成長約 10%，且退場時市場仍給 15 倍左右；前者我信，後者只信一半，估值偏貴","how_wrong":"最可能看錯兩處：一是 2027–2028 年收益率被加勒比運力與消費降溫壓到 1% 以下；二是 EPS 達標但自由現金流長期只剩淨利三成、靠舉債回饋股東"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 FY2027 共識 EPS 的 14.5 倍以下（現約 296 美元）","qc48_result":"pass","qc48_note":"RCL 的爆發情境缺少「運力 × 收益率 → 營收 → EPS」的逐步算術，第二條成長曲線（Sandals）真實存在，但還沒有可驗證的營收或盈餘數字。這些依據大多只能算作未證實，本次沒有發現足以否定的反證。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":322.3,"week26_return_pct":25.65,"consensus_rev_3m_pct":1.02,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"調整後與 GAAP 口徑差距小（FY2025 GAAP 稀釋 EPS 15.61，公司稱 FY2026 指引年增 14%，隱含調整後基期約 15.7）；分母的真正爭點是利潤率是否在週期高點，已反映在偏貴結論與 Bear 情境，不另標爭議"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 首次指引","impact":"高","watch":"調整後 EPS 指引中值是否 ≥ 20 美元、淨收益率指引是否 ≥ +2%"},{"date":"2027-Q1","date_precision":"quarter","type":"other","event":"Sandals 與 Beaches 50% 股權交割（約 30 億美元、舉債支應）","impact":"中","watch":"交割後淨負債÷調整後 EBITDA、權益法收益何時納入指引"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"Q1 2027 財報（公司預告 Q1 約 200 個基點結構性逆風）","impact":"中","watch":"Q1 淨收益率扣除逆風後是否仍為正"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節（篇幅不足，或含判斷／事實表裡沒有的數字）被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：含 1 個未覆蓋數字（見下方清單）；現在 2,851B，下限 3,000B（改完仍須達標）

### 未覆蓋數字（不在判斷物／事實表裡，驗證器逐個擋）

`s5`：
- `5.1` ｜ …程已受影響，兩季法說管理層都不評論。 5.1 二維評分與數字對照 5.F 對手財務…

處理方式：那幾個數字**要嘛刪掉**（連同只靠它撐起來的半句），**要嘛改用判斷物／事實表（白名單與判斷投影視圖）裡已有的數字**，逐字照抄；**不得自行推算新數字**（差值、比率、加總、幾個百分點都算新數字）。改寫時保留該章的論點與結論，其餘沒被點名的數字不要動。

格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RCL_20261103/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河：利潤率領先能守多久（§5.R、§5.F）</h2>
<p class="lead">護城河 B 級、方向穩定，領先是真的，但擴大的趨勢暫停。</p>
<ul class="pts">
<li>護城河來源有四層。規模、硬體差異化、自有私人目的地、跨品牌會員，共同轉成定價溢價與單位成本優勢。Icon 級新船載客率 133%，NPS 80 以上，約一半旅客為回頭客，40% 為會員。執行面給 8 分，定價面給 7 分，合計 7.5 分。</li>
<li>數字上的領先很清楚。TTM 毛利率 49.1%，營業利益率 27.6%。營業利益率分別高於 CCL 11.6 個百分點、NCLH 16.7 個百分點、VIK 4.3 個百分點。毛利率則高於 CCL 9.6、NCLH 8.5、VIK 5.9 個百分點。同業 ROIC 事實表無投入資本，無法比較，所以只能用單一 TTM 時點的營益率差距，差距是否擴大無法驗證。</li>
<li>方向由擴大改判穩定。營業利益率由 FY2023 的 20.7% 升到 FY2024 的 24.9%、FY2025 的 27.4%，再到 TTM 的 27.6%，每年擴張幅度由 2 至 4 個百分點降到 0.2。FY2026 淨收益率約 +2.1%，低於年初區間 1.5% 至 3.5% 的中點，Q3 報表口徑毛利收益率 −0.8%。執行面仍在擴大，定價面轉為穩定。</li>
<li>最大的威脅是加勒比運力集中投放。NCLH 2026 年加勒比運力 +55%，MSC +23%，業界新船訂單約 93 艘、22.95 萬床位，RCL 運力有 57% 在加勒比。我們給這項威脅 35% 機率，燈號中等。目前 RCL 加勒比收益率仍為正，RCL 自己加勒比運力為 +9%，所以還沒有看到實質降價。</li>
<li>次要威脅有三項。陸上全包式度假村與主題樂園爭奪同一筆度假預算，管理層自承郵輪價格漲幅落後陸上，機率 25%。旅行顧問若覺得佣金沒有競爭力會轉賣對手，機率 15%。技術落後的通用風險機率 10%。四項合計都沒有走到會讓護城河降級的程度。</li>
<li>反方證據要放在前面。VIK 的自由現金流利潤率 16.6%，遠高於 RCL 的 7.9%，NCLH 為 −6.4%，CCL 為 11.5%。這代表 RCL 的利潤率優勢有一部分是用更重的資本投入換來的。報酬持續期的四項檢查，需求基礎、決策層級、價值鏈分配、社會容忍度，全都只拿到中等。</li>
<li>報酬率的持續性只能粗估。再投資率取 FY2023 至 FY2025 累計（淨利減自由現金流）除以累計淨利，約 57%。增量報酬取中值 20%，區間 15% 至 26%，疫後收益率回升的殘差會高估，新船當年未滿載又會低估。目的地社區容忍度是上限，Mahahual 開發時程已受影響，兩季法說管理層都不評論。</li>
</ul>
<h3>5.1　二維評分與數字對照</h3>
<!-- E5 -->
<h3>5.F　對手財務深度對照</h3>
<!-- E6 -->
<h3>5.R　報酬持續期檢核</h3>
<!-- E7 -->
</section>

```