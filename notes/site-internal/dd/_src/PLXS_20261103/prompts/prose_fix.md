你是 stock-analyst v20 的**散文層（prose）agent**，標的 PLXS（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：PLXS　日期：2026-11-03　archetype：None　前份裁決：2026-05-24　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1781B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（425B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（978B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1511B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1122B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（594B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1047B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2452B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4038B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2463B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1781           3653-5219      5 條（2–6 內）  
s3                  8000         425           5302-7575      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3611          7972-11389      5 條（2–6 內）  
s6                 11000         594          7284-10406      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1047           1717-2453      5 條（2–6 內）  
s10                 5000        2452           1784-2548      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2463           2000-2537      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4891B；至少需散文≈40.11KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−55%
−50%
−37%
−37
−19.3%
−18.4%
−18.37
−1.0%
−0.3%
0
0%
0.15
0.20
0.3
0.35
0.5
0.6%
0.67%
0.75
0.89
0.97
1%
1
1.0
01
1.15
1.2
1.29
1.3
1.33
1.5
1.5%
1.59
1.6
1.75%
1.96
2
02
2%
2.1%
2.2
2.46
2.5
2.61
2.62
2.84
3%
03
3
3.1
3.3%
3.32%
3.4%
3.4
3.8
3.82%
04
4%
4
4.25%
4.3%
4.4
4.5
4.5%
4.66%
4.7%
4.8%
4.9
5
5.0%
05
5%
5.02%
5.1%
5.11%
5.44%
5.49%
5.5%
5.8%
6%
6.0
6
6.0%
06
6.2%
6.3%
6.4%
6.5%
6.5
6.7%
6.8
07
7%
7
7.5
8%
8
8.23
8.47
8.7
8.87
8.9%
9.0%
9.0
9
9%
9.1%
9.10
9.1
9.4
9.5%
9.8
10
10%
10.08%
10.1%
10.1
10.12
10.2%
10.3%
10.33
10.38%
10.4%
11
11.2
11.3%
11.36
11.4
11.40
11.79
12%
12
12.5%
13%
13
13.2%
13.2
13.3
13.8
13.8%
14%
14
14.1
14.27
14.6
15%
15
15.2
15.8%
16
16.8
17
17%
18
18%
18.18
18.2
18.6
18.7%
19%
19
19.2%
19.3%
19.33
20%
20
20.75
21.85
22
23%
23.6%
23.9
24
25%
25
25.5%
26
27%
27.7%
27.7
28
28.92
29
29.8%
30
30%
31
33%
34.8%
35%
37
39%
39.5%
40%
42
44%
45
45%
47.8%
49
49%
49.1%
49.65
50%
52%
52
54%
54
56%
57
60%
60
62
64
65
65%
66
66.8
68
69
70
75
90
98
100
100%
104
108
110
117
119
131.3
133
135
150
150%
160
175
177
181
190
200
214.32
223
224
247
250
265.72
274
300
308
330
409.2
483
640
960
2025
2026
2027
2029
2030
2031
20261103
1,081
2,100
2,280
2,920
3,500
4,200
5,000
7,000
−2,890
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
{"meta":{"ticker":"PLXS","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Plexus Corp."},"oneliner":"EMS 裡執行力上乘的一家：FY26 營收 +23%、ROIC 15.8% 近十年新高，FY27 指引再成長中高十位數；但成長有一大塊來自半導體設備順週期，現金轉換在同業墊底，FY27E 20.75 倍已反映前兩年，等 175 美元附近再談。","thesis":{"H":[{"id":"H1","text":"FY27 營收照新指引成長中高十位數，由航太國防與工業各 >20% 帶動，不是只靠半導體設備。","2y":"FY27 營收 ≥57 億美元（FY26 49.65 億 × 1.15）","5y":"FY31 營收 ≥75 億美元（FY28 共識 64 億後每年約 6% 以上）","10y":null,"threshold":"FY27 營收 ≥57 億美元，且航太國防與工業至少一個年增 >20%","source":"公司季報新聞稿分部營收表、法說會指引","drift_rule":"以 TTM 營收對照年度路徑：連 2 季落後 ≥5% 判削弱，連 3 季落後 ≥10% 判反轉"},{"id":"H2","text":"營收槓桿與自動化效率讓非GAAP營益率走向公司新目標 6.5–7%，ROIC 守在 15% 以上。","2y":"FY27 非GAAP營益率 ≥6.3%、ROIC ≥15%","5y":"FY29–FY31 非GAAP營益率平均落在 6.5–7%","10y":null,"threshold":"FY27 非GAAP營益率 ≥6.3%；任一季 <5.8% 為警訊","source":"公司季報非GAAP營益率與 ROIC 揭露","drift_rule":"5 年論點：營益率較路徑連 4 季偏離 ≥5%（約 0.3 個百分點）判削弱，連 6 季偏離 ≥10% 判反轉"},{"id":"H3","text":"成長期也能把利潤轉成現金：營運資金效率維持，FY27 自由現金流超過 1 億美元。","2y":"FY27 FCF >1 億美元、年底現金循環 60–65 天","5y":"FY28–FY31 FCF 對淨利轉換 ≥0.75","10y":null,"threshold":"FY27 FCF ≥1 億美元；現金循環 ≤68 天（Q1 季節性 66–70 天除外）","source":"公司季報現金流量表與現金循環天數","drift_rule":"2 年論點：累計 FCF 對年度路徑連 2 季落後 ≥5% 判削弱、連 3 季 ≥10% 判反轉；Q1 管理層已預告用現金，不計入"}],"R":[{"id":"R1","text":"半導體設備週期反轉，工業部門由高成長轉為衰退，營業槓桿反向。","h_ref":"H1","clock":"🔥","threshold":"工業部門營收連 2 季年減，或 FY27 營收指引下修到 13% 以下","evidence_refs":["end_markets#3","supply_demand_durability#0"]},{"id":"R2","text":"客戶集中度持續上升，任一大客戶轉單、自製或砍單的衝擊被放大。","h_ref":"H1","clock":"🔥","threshold":"前十大客戶單季占比 ≥60%，或年報出現單一客戶 ≥10%","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#2","customer_concentration_credit#3"]},{"id":"R3","text":"關稅、出口管制或墨西哥 IMMEX 規則改變，成本無法轉嫁，吃掉營益率擴張空間。","h_ref":"H2","clock":"🐢","threshold":"單季毛利率 <9.5% 且管理層歸因關稅或貿易措施","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"擴產與營運資金投入跑在獲利前面：檳城新廠稼動不足、FY27 FCF 不到 1 億美元，ROIC 跌回 15% 以下。","h_ref":"H3","clock":"⚡","threshold":"Q2 FY27 累計 FCF 仍為負且現金循環 >70 天，或單季 ROIC <14%","evidence_refs":["ems_utilization_capex_cycle#2"]}],"single_thing":{"description":"FY27 內半導體設備需求反轉，公司把全年營收成長指引由中高十位數下修到 13% 以下。","why_fatal":"工業部門占營收 44%，FY26 半導體設備 +50% 是成長與營業槓桿的最大來源；營益率目標靠營收槓桿（增量營益率 8–12%）達成，營收一轉弱，槓桿反向，FY28 EPS 由共識 11.79 掉到空頭路徑約 9，倍數同時壓到 13–15 倍，是情境樹裡對股價影響最大的單一項。","if_happens":"改走空頭路徑，價位約 117–135 美元；持有則清倉，未持有則至少等下修後兩季、確認工業部門止跌再重跑研究。","how_monitor":"每季工業部門營收與管理層對半導體設備的曆年展望；北美 EMS 月度 book-to-bill（跌破 1 為預警）；FY27 營收成長指引。","probability":"約 20%（12–24 個月）：管理層對 FY27 有約一年能見度、產業預測仍在上修，但半導體設備屬週期且已連續高成長。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.18,"peg_fy2":1.29,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":9.1,"FY2027E":10.33,"FY2028E":11.79,"FY2029E":null},"fy_end_month":9,"eps_basis":"非GAAP 稀釋 EPS；財年在 9 月底至 10 月初結束（FY26 季末 2026-10-03）。FY2026A 9.10 為推算：Chartmill 2026-10-18 的 FY26 共識 8.87 內含 Q4 預估 2.61，換成實際 Q4 非GAAP EPS 2.84（2026-10-29 法說），不是公司公布的全年數。FY2029E 共識事實表未涵蓋（只有兩個年度）。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/scenario.json","archetype":{"primary":"EMS/ODM","secondary":null,"confidence":"高","fingerprint":"毛利率約 10%、營益率 5–7%、資本支出占營收 2–3%、未揭露研發、前十大客戶過半、按專案量產爬坡認列"},"industry":{"clock_phase":"II","sd_verdict_source":"北美 EMS 2026 年 6 月 book-to-bill 1.33、出貨 +6.7%，產業協會稱限制在產能與交期；歐洲 EMS 以國防為最強結構性需求（Evertiq，2026-03）；半導體設備管理層只看得到 FY27、自承有週期（2026-10-29 法說）。合判：國防結構性持久，半導體設備週期性將反轉。","bargaining":{"up":"上游零組件吃緊（COO 10-29 稱材料環境受限），漲價在調價空檔由公司吸收，對上游議價力弱。","down":"下游是大型 OEM，前十大占 54–56%；客戶可自製或換廠，價格與組合對營益率的貢獻管理層自稱有限，議價力在客戶手上。","geo":"美國以外營運占營收與營業利益多數，集中在馬來西亞；墨西哥廠依 IMMEX 保稅計畫運作；另有中國廈門廠。"},"profit_pool_dir":"事實表未涵蓋 EMS 利潤池五年分布；同業營益率集中在 4.3%–5.5%，看不出利潤往 EMS 環節移動。","tam_table":{"expanded":false,"reason":"事實表沒有 EMS 外包滲透率與 TAM 資料；公司成長來自份額與新專案爬坡，不是低滲透或新品類故事，TAM 不是估值的承重假設"}},"moat":{"mechanism":"受監管、高組合低量產品（醫療 Class III、航太國防、太空）的製造執行與再認證轉換成本，加上營運資金周轉效率；不是專利或定價權。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：上行期仍拿到份額（IR 副總稱上行期拿份額少見）、ROIC 由 Q1 13.2% 升到 Q4 15.8%、現金循環 69→64→62 天。定價面穩定：毛利率 10.08% 與同業 9.0%–10.4% 同一區間，CFO 稱價格與組合影響相當有限。兩面合計，執行改善有一部分來自半導體設備順週期與年底固定成本槓桿，故方向判穩定而非擴大。","peer_na_reason":"事實表同業對照只有利潤率，沒有 ROIC 與投入資本；同業 ROIC 只能引第三方彙整站口徑，與公司自報口徑不同，僅作方向參考。","threats":[{"level":"🟡","text":"製程無專利保護，資源更大的同業或客戶自製可能帶來降價與丟單（10-K 風險因素）；管理層 10-29 稱競爭環境目前沒有變化。","p":"20%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0"]},{"level":"🟡","text":"零組件漲價在合約調價空檔由公司吸收，回收調價又稀釋營益率；COO 稱目前材料環境吃緊。","p":"30%","evidence_refs":["reg_tariff_export#2"]},{"level":"🟡","text":"醫療品質事件：第三方彙整站記錄 2025-01 一份 FDA 483 檢查缺失（心臟監測器材），不是警告信，之後未見召回紀錄；品質是公司主打賣點，若升級為警告信或召回，會直接傷到占營收 39% 的醫療部門贏單。","p":"10%","evidence_refs":["clinical_fda#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是病患、國防單位與晶圓廠，決策與付款者是 OEM；外包製造是『需要』而非『想要』，延後的代價是 OEM 自建產能。國防與太空需求結構性成長，但工業部門（44%）的主力半導體設備屬週期性，管理層只看得到 FY27，故給黃燈。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一專案層級看：醫療 Class III 心臟除顫器、飛行加油系統、太空電子換廠需重新認證，轉換成本高；但每個新專案都重新比稿，10-K 承認製程無專屬保護、客戶可自製。漲價後流失率與續約率事實表未涵蓋，只看得到贏單多來自既有客戶擴大份額。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈的利潤主要留在 OEM 品牌與晶片零組件端，EMS 只拿約 10% 毛利；前十大客戶占比升到 54–56%、上游材料吃緊，兩頭議價都不在公司手上。但毛利率由 FY22 9.1% 緩升到 FY26 10.1%，分配比例沒有惡化。"},{"item":"社會容忍度","level":"🟢","text":"製造服務費占終端產品成本小，沒有社會對漲價敏感的問題，也不靠監管授權取得優勢；政策面風險是關稅與出口管制，屬成本與營運風險，不是定價上限，已列入長期風險。"}],"roiic":"約 12%–20%（推算）","reinvest_rate":"FY26 逾 100%；FY27 約 65%（推算）","endo_ceiling":10,"formula_note":"內生上限＝增量 ROIC 約 15%（區間中值）× FY27 再投資率約 65% ≈ 每年 10%。增量 ROIC：FY25→FY26 營業利益增量 GAAP 約 4,200 萬、非GAAP 約 7,000 萬美元（營益率×營收推算），扣 17% 稅後，除以新增營運資金約 2.5 億（CFO 2026-10-29）加資本支出淨額（折舊事實表未涵蓋，以 FY26 資本支出指引 1.0–1.2 億近似上限）。再投資率：FY27 非GAAP稅後營業利益約 3 億（營收成長中高十位數、增量營益率 8%、稅率 16–18% 推算）減 FCF 目標 1 億。均為推算，非公司公布。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","PLXS":10.08,"SANM":9.01,"BHE":10.38,"FLEX":9.5,"JBL":9.23,"unit":"%"},{"metric":"營業利益率","PLXS":5.02,"SANM":5.49,"BHE":4.25,"FLEX":5.44,"JBL":5.11,"unit":"%"},{"metric":"FCF 利潤率","PLXS":-1.0,"SANM":4.66,"BHE":4.61,"FLEX":3.32,"JBL":3.82,"unit":"%"},{"metric":"研發密度","PLXS":null,"SANM":0.26,"BHE":null,"FLEX":null,"JBL":0.08,"unit":"%"}],"competitors":[{"name":"SANM","gm":9.01,"om":5.49,"fcf_margin":4.66,"rd_intensity":0.26,"strategy_note":"營益率 5.49%、FCF 率 4.66% 都高於 PLXS，同樣做高組合工業與國防，是現金轉換最直接的對照；第三方 ROIC 11.3% 則低於 PLXS。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BHE","gm":10.38,"om":4.25,"fcf_margin":4.61,"rd_intensity":null,"strategy_note":"毛利率 10.38% 略高於 PLXS，但營益率只有 4.25%，是同一高組合低量定位裡費用效率較差的對手，PLXS 在此對照中領先。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"FLEX","gm":9.5,"om":5.44,"fcf_margin":3.32,"rd_intensity":null,"strategy_note":"營益率 5.44%、FCF 率 3.32%；第三方 ROIC 19.2% 略高於 PLXS，同樣押資料中心與電力。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"JBL","gm":9.23,"om":5.11,"fcf_margin":3.82,"rd_intensity":0.08,"strategy_note":"營益率 5.11% 與 PLXS 相近，FCF 率 3.82%；第三方 ROIC 29.8% 遠高於 PLXS，差距主要在資產周轉（1.6 倍對 1.3 倍）。","period":"TTM ending 2026-08-31（4季加總）"}]},"growth":{"driver_mix":"量為主：新專案爬坡、既有客戶份額提升與終端需求；價格與組合貢獻 CFO 稱相當有限；無併購；回購約每年 1 億美元。","runway_years":"事實表未涵蓋外包滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段報酬持續期：增量 ROIC 約 15% × FY27 再投資率約 65% ≈ 每年 10%，共識兩年 EPS 年化 13.8% 超出約 3.8 個百分點，缺口由營益率擴張與淨回購解釋。","segments":[{"item":"工業（FY26 21.85 億美元，44%）","value":"FY26 +27%（半導體設備 +50%）；Q4 年增約 50%；FY27 指引 >20%；Q1 FY27 預估季減低個位數"},{"item":"醫療與生命科學（19.33 億，39%）","value":"FY26 +19%；FY27 高個位數（7 月時說短期放緩，10 月上調）；Q1 季增低個位數"},{"item":"航太國防（8.47 億，17%）","value":"FY26 +23%；FY27 >20%；FY26 贏單 4.9 億美元，超過 FY23–FY25 合計；Q4 季減 4%，管理層歸因材料時點"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"FY26 TTM 10.08% 與 FY25 相同，Q4 10.2%"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱上行期仍拿份額；第三方份額數據事實表未涵蓋"},{"item":"提價後銷量下滑","lit":false,"note":"不適用，EMS 價格隨零組件調整"},{"item":"EPS 成長顯著快於營收（差 >5 個百分點）","lit":true,"note":"FY23→FY25 營收年減約 2%、GAAP EPS 年增約 12.5%"},{"item":"FCF 對淨利 <0.75 連 2 年","lit":false,"note":"FY25 約 0.89；FY26 為負；FY27 指引隱含約 0.35，若兌現即亮燈"},{"item":"SBC 占營收 >5% 且上升","lit":false,"note":"0.67%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"10-K 未點名替代技術"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"item":"維持性資本支出占 FCF >60%","lit":null,"note":"FCF 接近零，維持性資本支出事實表未涵蓋，無法判定"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"檳城第六廠擴產中"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，資本回饋只有回購（FY26 計畫已執行完畢，FY27 新授權 1 億美元已開始）；近三年現金四分去向、回購均價與債務利率事實表未涵蓋，無法展開。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 無併購項目，成長不靠併購，不適用。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價事實表未涵蓋；以現價計 FY27E 盈餘殖利率約 4.8%（10.33 ÷ 214.32），10 年期公債殖利率事實表未涵蓋，但即使只有 3%，門檻也要 5%，判不過；FY26 回購期間 FCF 為負。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q4 SBC 960 萬美元（含 110 萬高階主管退休加速認列），占營收 0.67%；年化約 3,500 萬，約市值 0.6%，每年 1 億美元回購抵銷有餘，淨稀釋為負。","grade":"過"}]},"valuation":{"basis":"Forward P/E（FY27E 非GAAP 共識）為主，EV/S 0.97 倍與 P/S 作交叉檢查","tier":"中型 EMS（高組合低量）","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比或 EV/S，倍數無法做同業對照；這是資料缺口，不是不承重"},"fwd_pe":20.75,"peg":1.5,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY27E 本益比 20.75 倍、PEG 約 1.5（20.75 ÷ FY26 推算基期到 FY28E 兩年 EPS 年化 13.8%），在合理區上緣；P/S 1.15、EV/S 1.15 是近三個年度端點最高；基本情境五年年化約 6%（含約 1% 淨回購），低於 8%。一年目標以 FY28E 11.79 × 19 倍（現行與終端倍數之間）約 224 美元，上檔約 4.5%；五年基本情境 15.2 × 18 倍約 274 美元，約 +27.7%。判偏滿：不到紅燈，因股價已較前份跌約 19% 且 FY27 共識財報後再上修。","upside_short_pct":4.5,"upside_mid_pct":27.7},"trap_analysis":{"verdict":"🟡","label":"週期高峰 EPS 加上現金轉換偏弱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"工業部門占 FY26 營收 44%，半導體設備子段 FY26 +50%；CEO 10-29 只願對 FY27 表態，IR 副總自承半導體設備有週期；Q1 FY27 工業部門預估季減低個位數。","assumption":"基本情境假設半導體設備溫和正常化，FY29 起公司成長仍有 8–10%。","consequence":"若 FY28 半導體設備進入下行，工業部門由 +27% 轉負，營業槓桿反向，營益率回到 5% 附近，EPS 回到約 7.5 美元、倍數 13 倍，股價約 98 美元，較現價約 −55%。","ruling":"採納為空頭路徑與回撤下緣（空頭 30% 內約三分之一是這個尾端），但不當基本情境：上行期仍拿份額、國防贏單 4.9 億美元超過前三年合計，可緩衝；此視角與唯一致命點重疊，維持不動。","watch":"工業部門季營收年增率、北美 EMS book-to-bill、FY27 營收指引","evidence_refs":["end_markets#3","supply_demand_durability#0","competitive_share_entrants#1"],"fact_refs":["f_kpi5_guidance_q1_fy2027_2027_","f_ma_w250"]},{"view":"論點成功但股東經濟變差","evidence":"FY26 營收 +23%，但全年 FCF −2,890 萬美元、TTM FCF 率 −1.0%，同業 3.3%–4.7%；CFO 說每 1 美元增量營收要 0.15–0.20 美元營運資金；檳城第六廠新增逾 5 億美元營收產能，Q2 FY26 仍略低於損益兩平；10-K 承認零組件漲價在調價空檔由公司吸收。","assumption":"成長放緩前，營運資金效率與新廠稼動能讓 FCF 轉正並守住 ROIC 15%。","consequence":"若成長再超預期，營運資金吃掉更多現金，FY27 FCF 達不到 1 億美元；新產能閒置則 ROIC 回落到 13% 以下，EPS 成長但股東拿不到現金，回購只能靠借款。","ruling":"部分採納：低 FCF 主要是成長期營運資金投入，現金循環 62 天創紀錄、客戶分攤部分存貨，屬時點問題；但把 FY27 FCF ≥1 億美元設為驗證門檻，未達即品質分降一級。","watch":"季度 FCF、現金循環天數、ROIC、檳城新廠損益","evidence_refs":["ems_utilization_capex_cycle#2","reg_tariff_export#2","ems_roic_asset_turnover_benchmark#2"],"fact_refs":["f_kpi3_free_cash_flow","f_peer_plxs_fcf_margin_pct","f_kpi6_inventory_days"]},{"view":"價格已反映太多","evidence":"FY27E 本益比 20.75 倍、FY28E 約 18.2 倍；P/S 1.15、EV/S 1.15 在近三個年度端點最高；FY1 共識『近三個月 +25.5%』可能混入財年換檔，財報後真實上修只有 +2.1%（FY1）與 +3.4%（FY2）。","assumption":"市場給的倍數反映的是可持續的成長，而不是半導體設備高峰。","consequence":"若市場把 FY27 EPS 視為週期高點，倍數回到 15–17 倍，即使 EPS 兌現，一年後股價也只有約 177–200 美元。","ruling":"採納：判估值偏滿，現價不追，等 175 美元附近；但股價已較前份跌約 19%，不是泡沫，不給紅燈。","watch":"財報後共識修正方向、FY27E 本益比","evidence_refs":["capital_markets_pricing#4","capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct"]},{"view":"論點失敗","evidence":"10-K FY2025：美國以外營運占營收與營業利益多數、集中在馬來西亞；墨西哥廠依 IMMEX 保稅計畫降關稅；出口管制可能限制對中國出貨、在中國生產與採購先進半導體零組件；另有中國廈門廠。","assumption":"關稅與貿易措施的成本能透過合約調價轉嫁。","consequence":"若無法轉嫁，毛利率掉 0.5–1 個百分點就吃掉營益率由 6.2% 走向 6.5–7% 的全部空間。","ruling":"列為長期風險，不放進基本情境；不預測政策，只以單季毛利率 <9.5% 且管理層歸因關稅作為吸收失敗的判定。","watch":"單季毛利率、法說中關稅損益歸因、IMMEX 規則","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"],"fact_refs":["f_peer_plxs_gross_margin_pct"]}],"max_dd":{"lo":-55,"hi":-37,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 265.72 → 本次 214.32（-19.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=265.72","side_b":"本次 price_at_dd=214.32","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 265.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 265.72 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 265.72 美元：Bull 價 409.2、Bear 價 131.3，五年期望值 −0.3%，基準年化 0.6%，不對稱比 0.89","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.89。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 265.72 美元：五年期望值 −0.3%，基準年化 0.6%，不對稱比 0.89","side_b":"本次情境、股價 214.32 美元：五年期望值 +23.6%，基準年化 5.0%，不對稱比 1.96","ruling":"再換股價、情境不動：起點價下跌 19.3%，五年期望值多 23.9 個百分點，基準年化多 4.4 個百分點，不對稱比由 0.89 升到 1.96。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"客戶集中度","cause":null,"prior_field":null,"side_a":"CEO Todd Kelsey（2026-10-29）：56% 是長期常見水準，49% 偏低，公司沒有變得結構性集中。","side_b":"10-K 與財報：前十大占比 FY24 47.8%、FY25 49.1%、FY26 54%、Q4 56%，Q4 年增 7 個百分點；FY23 GE Healthcare 單一客戶 10.3%。","ruling":"可調和（程度差異）：事實表沒有 FY23 以前的前十大占比，無法驗證『歷史常態』，但 FY23 有單一客戶超過 10%，顯示過去集中度也不低；趨勢向上且與大型專案爬坡同步，列為中期風險，不當作論點失效。","evidence_level":"一手（10-K、8-K）對照管理層口述","settle_metric":"前十大客戶季占比、年報單一客戶是否 ≥10%","if_then":["若 FY27 任一季前十大 ≥60% 或年報揭露單一客戶 ≥10%，倉位上限降一級，該風險時鐘改為一到兩季","若前十大回落到 52% 以下且營收成長未放緩，降為觀察項"],"evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#3"]},{"axis":"成長與現金","cause":null,"prior_field":null,"side_a":"FY26 營收 +23%、ROIC 15.8% 近十年最高、現金循環 62 天創紀錄。","side_b":"同一年 FCF −2,890 萬美元、TTM FCF 率 −1.0% 為同業最差；FY27 FCF 目標 1 億美元只約稅後利潤三分之一。","ruling":"可調和：兩者同時成立，因為高成長要先墊營運資金與產能；關鍵是 FY27 成長放緩到中高十位數時 FCF 能否回到 1 億美元以上。","evidence_level":"一手（財報新聞稿、法說）","settle_metric":"FY27 全年 FCF、現金循環天數","if_then":["若 Q2 FY27（約 2027-04）累計 FCF 仍為負且現金循環 >70 天，品質分降一級，重啟價位由 175 下調到 160 美元","若 FY27 FCF ≥1 億美元且現金循環 60–65 天，本矛盾撤銷"],"evidence_refs":["ems_utilization_capex_cycle#2","ems_roic_asset_turnover_benchmark#2"]},{"axis":"半導體設備能見度","cause":null,"prior_field":null,"side_a":"COO Oliver Mihm（2026-10-29）：半導體設備曆年成長會比 FY26 的 50% 更強；分析師引述同業已看到 2029–2030 年的預測。","side_b":"CEO Todd Kelsey 同場：只對 FY27 有把握，不願往後看；IR 副總 Shawn Harrison：半導體設備有週期，採保守假設。","ruling":"可調和：近一年強、更遠不可見，兩者並存。基本情境 FY29 起成長降到 8–10%，空頭機率 30% 承擔週期反轉，不採信長天期預測。","evidence_level":"管理層口述（同場）","settle_metric":"工業部門季營收年增率、北美 EMS book-to-bill","if_then":["若工業部門連 2 季年減，持有部位減碼一半並把空頭機率提到 40%","若 FY27 下半年工業部門仍年增 >20% 且 FY28 指引延續成長，多頭機率由 25% 提到 30%"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#2","supply_demand_durability#4"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-07-30 法說：CEO 給 Q4 營收 13.3–13.8 億、FY26 成長逾 20%；CFO 說 Q4 FCF 約損益兩平或小幅用現金；IR 副總說 A&D Q4 約與 Q3 相當、醫療 FY27 短期放緩，且不肯給 A&D FY27 成長率。","side_b":"2026-10-29 法說：Q4 營收 14.27 億超過上緣、FY26 成長 23%、Q4 FCF +640 萬；醫療 FY27 上調為高個位數、A&D 給出 >20%；但 A&D Q4 季減 4%，COO 歸因材料時點並稱 Q1 會補回。","ruling":"大致兌現或超標，管理層可信度加分。A&D 的材料時點歸因不採信也不否定，列為未證：若 Q1 FY27 A&D 未見高個位數季增，此歸因判為不成立，國防這條成長腿降級。","evidence_level":"一手（兩場法說逐字稿）","settle_metric":"Q1 FY27 航太國防季增率","if_then":["若 Q1 FY27 航太國防季增 <5%，H1 的國防腿降級，多頭機率降到 20%","若 Q1 FY27 航太國防季增 ≥8%，歸因成立，不調整"],"evidence_refs":["end_markets#1","capital_markets_pricing#0","end_markets#3"]},{"axis":"共識修正口徑","cause":null,"prior_field":null,"side_a":"FY1 共識 EPS 近三個月由 8.23 升到 10.33（+25.5%）。","side_b":"財報前後兩份快照只從 10.12 升到 10.33（+2.1%），FY2 由 11.40 升到 11.79（+3.4%）；7 月時的 FY1 很可能仍是 FY26（Chartmill 10-18 的 FY26 共識 8.87 與 8.23 同一量級），10 月底已換成 FY27。","ruling":"採後者：近三個月 +25.5% 大部分是財年換檔，不是分析師大幅上修；真實上修幅度以財報後 +2.1%／+3.4% 為準，動能判讀不應引用 +25.5%。","evidence_level":"推論（兩份快照未標財年）","settle_metric":"下一份快照的 FY27 共識三個月變化","if_then":["若 2027-01 快照 FY27 共識較 10-31 再上修 ≥5%，多頭機率由 25% 提到 30%","若 FY27 共識下修 ≥5%，空頭機率提到 35% 並暫停重啟評估"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"循環位置","cause":null,"prior_field":null,"side_a":"偏買：股價 26 週 −18.4%、RSI 37，賣方目標價高於現價；北美 EMS book-to-bill 1.33，限制在產能而非需求；公司機會漏斗年增 33%。","side_b":"偏賣：P/S、EV/S 在近三個年度端點最高；半導體設備 FY26 +50% 且管理層只看得到 FY27；存貨天數 119 天；Q1 FY27 營收只季增約 1%、工業部門季減。","ruling":"五個需求量訊號多數決判中循環：需求仍向上但動能放緩、倍數貼近自身近年高點，客戶庫存狀況事實表未涵蓋。中循環對應持有不加；倍數貼高點，新建立部位的條件不成立，交易面等回踩。","evidence_level":"產業協會＋公司數字","settle_metric":"北美 EMS book-to-bill、工業部門季營收","if_then":["若北美 EMS book-to-bill 跌破 1 且工業部門連 2 季季減，改判晚循環，不建立任何部位","若股價回到 104 週均線 181 美元以下而工業部門仍年增 >15%，改判中循環偏早，進入首倉評估"],"evidence_refs":["supply_demand_durability#2","capital_markets_pricing#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：Q4 非GAAP EPS 2.84 年化 11.36，已高於 FY27 共識 10.33；股價較前份跌約 19%、26 週 −18.4%、RSI 37，賣方 8 月目標價 247–308 美元都在現價之上；財報後 FY27、FY28 共識仍上修，ROIC 近十年最高、機會漏斗 49 億美元創新高。若 FY27 EPS 落在 11 以上，現價只有約 19 倍。","side_b":"觀望：Q4 有年底固定成本槓桿與材料拉貨，管理層自己把 Q1 營益率指引壓到 6.0–6.4%、EPS 2.46–2.62，年化 Q4 會高估；基本情境五年年化約 6%，低於 8%；成長有一大塊來自週期性的半導體設備。","ruling":"採觀望：綁定約束是估值，不是論點；論點完整，等價格。","evidence_level":"一手數字＋推算","settle_metric":"Q1 FY27 非GAAP EPS 與全年指引","if_then":["若 Q1 FY27 非GAAP EPS ≥2.62 且全年營收指引上調，基本情境 FY27 EPS 上修到 11，重啟價位由 175 上調到 190 美元","若股價先漲回 250 美元以上而 Q1 數據未到，不追"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"估值結論漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份估值紅燈（股價 265.72 美元）。","side_b":"本次偏滿（股價 214.32 美元，FY27E 20.75 倍、FY28E 18.2 倍）。","ruling":"股價下跌約 19% 為主因，同期 FY27 共識財報後再上修 2.1%；只降一級到偏滿，因為 P/S 仍在三個年度端點最高、基本情境五年年化約 6%。","evidence_level":"事實表數字","settle_metric":"FY27E 本益比","if_then":["若股價 ≤175 美元而 FY27 共識不變，估值結論改為合理"],"evidence_refs":[]},{"axis":"品質與競爭方向結論","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份：訊號等級 B、陷阱風險黃燈、護城河方向穩定。","side_b":"本次：三者結論不變。","ruling":"新證據兩面互抵：ROIC 15.8% 近十年新高、上行期仍拿份額、管理層財測大致兌現（正）；前十大客戶 49%→54%、FY26 FCF 為負、毛利率未見溢價（負）。結論維持，理由更新。","evidence_level":"一手（財報、法說、10-K）","settle_metric":"FY27 FCF、前十大客戶占比、ROIC","if_then":["若 FY27 FCF ≥1 億美元且 ROIC ≥15%，陷阱風險改為綠燈","若前十大 ≥60% 或 FCF 未達，護城河方向改判縮減並重評等級"],"evidence_refs":["ems_roic_asset_turnover_benchmark#2","customer_concentration_credit#3","competitive_share_entrants#0"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份未填情境機率、最大回撤、五年後成長空間、公司類型、循環位置，也沒有定期定額結論。","side_b":"本次：情境機率多頭 25／基本 45／空頭 30；最大回撤 −37%～−55%；五年後成長空間黃燈；類型 EMS/ODM；循環位置中循環；定期定額結論由程式依本次輸入另算。","ruling":"方法變動，不是基本面改變；前份這些欄為空，沒有可比較的漂移。","evidence_level":"方法","settle_metric":null,"if_then":["若下一份判斷的循環位置改為晚循環，不建立任何部位"],"evidence_refs":[]},{"axis":"唯一致命點 Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"FY27 內半導體設備需求反轉，公司把全年營收成長指引由中高十位數下修到 13% 以下。","ruling":"方法變動：Single Thing 取情境樹裡對 EPS 與倍數同時影響最大的單一事件；工業部門占營收 44%、半導體設備是成長與營業槓桿的最大來源，發生即清倉。","evidence_level":"一手（分部營收、法說）","settle_metric":"FY27 營收成長指引","if_then":["若指引下修到 13% 以下，清倉並改走空頭路徑","若 FY27 全年指引維持或上調，維持基本情境"],"evidence_refs":["end_markets#3"]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼指標。","side_b":"工業部門營收連 2 季年減；FY27 營收指引下修到 13% 以下；非GAAP營益率連 2 季 <5.8%；FY27 FCF <1 億美元；前十大客戶 ≥60% 或單一客戶 ≥10%。","ruling":"方法變動：本版每條風險配可量測門檻。指引下修到 13% 以下單項即清倉；工業部門連 2 季年減或營益率連 2 季 <5.8% 單項減碼一半；後兩項觸發則停止加碼並降品質分。","evidence_level":"方法","settle_metric":"上列五項","if_then":["任一清倉條件觸發即清倉，不等下一份判斷","減碼條件觸發後兩季內未恢復，再減碼剩餘的一半"],"evidence_refs":[]},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件。","side_b":"股價 ≤175 美元（基本情境五年年化約 10%）且 FY27 營收成長指引未下修到 13% 以下。","ruling":"方法變動：本次觀望的綁定約束是估值（現價基本情境五年年化約 6%），重啟條件就是這個約束的否定；到價後重跑研究、分批建立首倉，之後才談加碼。","evidence_level":"推算","settle_metric":"股價、FY27 指引","if_then":["若股價 ≤175 美元且指引未下修，重跑研究後分三批建立首倉","若 Q1 FY27 優於指引上緣且全年上調，重啟價位上調到 190 美元"],"evidence_refs":[]},{"axis":"假設與風險門檻改寫","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：H1 FCF 率由 FY26 1.5% 升到 FY28 4% 以上（FY26 下半年 FCF 5,000 萬美元以上）；H2 非GAAP營益率 6% 以上向 7%；H3 醫療年增 12% 以上；風險為 FCF 率無法改善、醫療回落中個位數、EMS 估值均值回歸。","side_b":"本次：H1 FY27 營收 ≥57 億美元；H2 FY27 非GAAP營益率 ≥6.3% 且 ROIC ≥15%；H3 FY27 FCF ≥1 億美元；風險改為半導體設備反轉、客戶集中、關稅地緣、擴產吃現金。","ruling":"新證據：FY26 全年 FCF −2,890 萬、Q4 只有 640 萬（Q3 數字事實表未涵蓋），前份 FCF 方向未兌現，改用公司自己承諾的 1 億美元當門檻；前份營益率驗證點 FY26 6.0–6.5% 已達成（6.2%），門檻上移；醫療 FY26 +19% 已過前份門檻，但 FY27 只看高個位數，主引擎換成工業與國防；股價較前份已跌約 19%，前份估值均值回歸風險部分兌現，改由估值結論處理。","evidence_level":"一手（財報、法說）","settle_metric":"FY27 營收、營益率、FCF","if_then":["若 FY27 三項門檻有兩項未達，假設整組重寫並改判陷阱風險紅燈","若三項全達，維持論點並把重啟價位上調 10%"],"evidence_refs":["end_markets#0","ems_roic_asset_turnover_benchmark#2"]}],"triggers":[{"n":1,"text":"Q1 FY27 營收低於指引下緣","type":"假設驗證","maps_to":"H1","metric":"季營收","threshold":"<14.1 億美元","action":"H1 判削弱，重啟價位下移到 150 美元，等 Q2 再看","source_freq":"季報（每季）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"工業部門營收連 2 季年減","type":"風險","maps_to":"R1","metric":"工業部門營收年增率","threshold":"連 2 季 <0%","action":"若持有減碼一半；未持有停止首倉評估","source_freq":"季報（每季）","date":null,"evidence_refs":["end_markets#3"]},{"n":3,"text":"FY27 全年營收成長指引下修到 13% 以下（半導體設備需求反轉）","type":"Single Thing","maps_to":"Single Thing","metric":"FY27 營收成長指引","threshold":"<13%","action":"清倉；未持有則至少等下修後兩季再重跑研究","source_freq":"季報與法說","date":null,"evidence_refs":["supply_demand_durability#0"]},{"n":4,"text":"股價回到 175 美元以下，且 FY27 營收指引未下修","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤175 美元","action":"重跑研究後分三批建立首倉","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":5,"text":"客戶集中度越線","type":"風險","maps_to":"R2","metric":"前十大客戶營收占比","threshold":"單季 ≥60% 或年報單一客戶 ≥10%","action":"倉位上限降一級，停止加碼","source_freq":"季報、10-K","date":null,"evidence_refs":["customer_second_source#1","customer_concentration_credit#3"]},{"n":6,"text":"關稅或貿易措施吸收失敗","type":"風險","maps_to":"R3","metric":"單季毛利率","threshold":"<9.5% 且管理層歸因關稅或貿易措施","action":"減碼三分之一，H2 判削弱","source_freq":"季報（每季）","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"n":7,"text":"成長吃掉現金","type":"風險","maps_to":"R4","metric":"上半年累計 FCF 與現金循環天數","threshold":"Q2 FY27 累計 FCF <0 且現金循環 >70 天","action":"停止加碼；FY27 全年 FCF <1 億美元確認後減碼三分之一","source_freq":"季報（每季）","date":"2027-04","evidence_refs":["ems_utilization_capex_cycle#2"]},{"n":8,"text":"跌深而基本面無損","type":"加碼","maps_to":"H1","metric":"股價","threshold":"≤150 美元（約 FY28E 13 倍）且 H1–H3 無一失效","action":"分批反買，不停損","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":9,"text":"股價先跑在 EPS 前面","type":"減碼","maps_to":"H2","metric":"FY28E 本益比","threshold":"股價 ≥300 美元而 FY28 共識未上修 10% 以上","action":"減碼三分之一","source_freq":"每日收盤、月度共識","date":null,"evidence_refs":[]},{"n":10,"text":"Q1 FY27 財報後複審","type":"複審日期","maps_to":null,"metric":"Q1 FY27 營收、營益率、航太國防季增、全年指引","threshold":null,"action":"重跑判斷","source_freq":"一次性","date":"2027-02-05","evidence_refs":[]}],"kill_metrics":[{"metric":"工業部門營收年增率（季）","bear_threshold":"連 2 季 <0%","window":"FY27–FY28","source":"公司季報分部營收表","last_status":"ok"},{"metric":"FY27 全年營收成長指引","bear_threshold":"下修到 13% 以下","window":"FY27 每季財報","source":"公司財報新聞稿與法說","last_status":"ok"},{"metric":"非GAAP營益率（季）","bear_threshold":"連 2 季 <5.8%","window":"FY27–FY28","source":"公司季報","last_status":"ok"},{"metric":"FY27 全年自由現金流","bear_threshold":"<1 億美元","window":"FY27 年底（2027-10）","source":"公司季報現金流量表","last_status":"warning"},{"metric":"前十大客戶營收占比","bear_threshold":"單季 ≥60% 或單一客戶 ≥10%","window":"FY27","source":"公司季報、10-K","last_status":"warning"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=-18.37, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價 ≤175 美元（基本情境五年年化約 10%）且 FY27 營收成長指引未下修到 13% 以下","exec_line":"現價觀望不追，綁定約束是估值；股價 ≤175 美元且 FY27 營收指引未下修時重跑研究，首倉分三批；跌破 150 美元而 H1–H3 無失效則分批反買，不設停損；唯一致命點發生則清倉。"},"reasoning":{"industry":"FY26 營收 49.65 億美元，年增 23%；分部為工業 21.85 億（44%）、醫療與生命科學 19.33 億（39%）、航太國防 8.47 億（17%）（Q4 FY26 財報新聞稿分部表，2026-10-28）。最新一季營收 14.27 億美元，年增 34.8%；毛利率 10.2%（CFO，2026-10-29 法說），非GAAP營益率 6.7%、GAAP 6.0%。Q1 FY27 指引營收 14.1–14.6 億、非GAAP營益率 6.0–6.4%。單點依賴：FY25 無單一客戶達 10%，但前十大客戶由 FY25 49% 升到 FY26 54%、Q4 56%；工業部門的成長主要來自半導體設備（FY26 該子段 +50%）。產業時鐘判擴張期：北美 EMS 2026 年 6 月 book-to-bill 1.33，限制在產能與交期而非需求；公司機會漏斗 49 億美元、年增 33%；尚未見產能過剩或降價。供需持久度：國防與太空屬結構性持久，半導體設備屬週期性、終將反轉，醫療在 FY26 消化後回到高個位數。產業態勢三軸：競爭面靜態（管理層 10-29 稱競爭環境沒有變化，10-K 承認製程無專屬保護）；需求結構轉好（歐洲國防是 EMS 最強的結構性需求、北美訂單出貨比大於 1）；其他結構變數在關稅與出口管制（馬來西亞集中、墨西哥 IMMEX）。裁決：雙向拉鋸，需求結構轉好與貿易政策風險並存。","moat":"機制：醫療 Class III 器材、飛行加油系統、太空電子這類受監管、高組合低量產品，換廠要重新認證，形成專案層級的轉換成本；再加上現金循環 62 天的營運資金效率，把約 5% 的營益率放大成 15.8% 的 ROIC。評分：執行 7（上行期仍拿份額、ROIC 由 Q1 13.2% 升到 Q4 15.8%、FY26 贏單 12 億美元年化），定價 5（毛利率 10.08% 與 SANM、FLEX、JBL、BHE 的 9.0%–10.4% 同區間，營益率 5.02% 居中，FCF 率 −1.0% 同業最差）。對最強同業：第三方彙整站 ROIC 顯示 CLS 39.5%、JBL 29.8%、FLEX 19.2% 都高於 PLXS 的 18.7%（2026 Q1 口徑），只贏 SANM 11.3%；對自身 WACC 9% 的利差 6.8 個百分點且在擴大。報酬持續期：當期屬低利益率、高周轉，15.8% 約等於稅後營益率 5.1%（非GAAP 6.2% 扣 17% 稅）乘投入資本周轉約 3.1 倍（推算）；四檢查點三黃一綠；增量 ROIC 約 12%–20%，FY27 再投資率約 65%，內生成長上限約每年 10%。","growth":"成長來源以量為主：新專案量產爬坡、既有客戶份額提升與終端需求，價格與組合貢獻 CFO 稱相當有限；無併購；回購每年約 1 億美元（約市值 1.75%）。共識：FY27E 10.33、FY28E 11.79，以 FY26 推算基期 9.10 計兩年 EPS 年化約 13.8%（只有兩年，第三年共識事實表未涵蓋）。內生上限約 10%（增量 ROIC 約 15% × 再投資率約 65%），缺口約 3.8 個百分點，可歸因於營益率由 6.2% 走向 6.5–7% 目標（每年約 2–3 個百分點）與淨回購（約 1 個百分點），不依賴倍數上調。五年後：事實表沒有外包滲透率，無法換算達 30% 滲透的年數；第二條曲線有雛形（國防與太空、資料中心電力機會漏斗約 5 億美元，CEO 2026-07-30），但尚未成為可量化營收，故判黃燈。衰退訊號亮 1 個、接近 1 個：EPS 成長長期快於營收（FY23→FY25 營收年減約 2%、GAAP EPS 年增約 12.5%）；FCF 對淨利轉換偏低（FY26 為負，FY27 指引 1 億美元只約稅後利潤三分之一），FY27 若照指引即連 2 年亮燈。","governance":"FCF 對淨利轉換偏弱：FY26 全年 FCF −2,890 萬美元，Q4 為營業現金流 2,920 萬減資本支出 2,280 萬＝640 萬；TTM FCF 率 −1.0%，同業 3.3%–4.7%。原因是營收年增 23% 需要約 2.5 億美元營運資金（CFO 2026-10-29：每 1 美元增量營收約需 0.15–0.20 美元）。SBC 占營收 0.67%，稀釋輕。現金去向：FY26 回購計畫執行完畢（Q4 約 2,100 萬美元），FY27 新授權 1 億美元已開始；無併購；事實表未見股息。資產負債：事實表淨負債 1,081 萬美元（含租賃負債），公司口徑為淨現金；循環額度動用 1.59 億、可再借逾 3.4 億，2026-06 新信用協議到期 2031 年。近三年現金四分去向與債務利率事實表未涵蓋。","valuation":"現價 214.32 美元＝FY27E 20.75 倍、FY28E 18.2 倍、EV 對 FY27E 營收 0.97 倍。Trailing P/E 28.92 倍在近三個年度端點的 66.8 分位，P/S 1.15、EV/S 1.15 在三點中最高；五年分位事實表只有三個年度端點，無法計算。PEG 約 1.5。現價隱含：FY27–FY28 共識兌現、之後每年仍有約 10% 成長、終端倍數守在 18 倍左右，基本情境五年年化約 6%（含約 1% 淨回購）。我信前兩年（指引、漏斗、贏單都支持），不信半導體設備高峰 EPS 配現行倍數。需求量循環五訊號判中循環。賣方目標價 8 月前後 247–308 美元（多來源，均非 11 月最新）全在現價之上，最高與最低（150–330）相差 2.2 倍，未到需下修信心的 2.5 倍。","premortem":"三個視角的反證已寫在反證段，這裡只交結論：衰退訊號亮 1 個（EPS 長期快於營收），另 1 個接近（FCF 對淨利轉換，FY27 若照指引將連 2 年偏低），陷阱風險黃燈。價格面已先反映一部分：股價較前份 265.72 美元跌約 19%、26 週 −18.4%、RSI 37，週線位於 52 週均線 223 美元之下、104 週均線 181 美元之上；250 週均線 133 美元在空頭情境價位附近。歷史最大回撤、空方最強數字事實表未涵蓋。上一季法說的迴避（A&D FY27 成長率）本季已補上 >20%，這個缺口已關閉。"},"plain":{"six":{"how_it_makes_money":"賺的是工業、半導體設備、醫療與國防 OEM 的高組合低量外包製造費：錢卡在客戶議價與零組件成本轉嫁之間，公司只拿約 10% 毛利、6% 營益率，超額報酬來自營運資金周轉，不是定價權。","moat":"護城河方向穩定：機制是受監管、高組合低量產品的製造執行與再認證轉換成本，不是定價權；ROIC 15.8% 對 WACC 9% 有 6.8 個百分點利差、創近十年新高，但毛利率與營益率只在同業中段、自由現金流率同業最差，改善有相當部分來自半導體設備順週期的稼動率。","growth":"五年後成長空間黃燈：未來兩年有中高十位數的指引、創新高的 49 億美元機會漏斗與 12 億美元年化贏單支撐；但 Y5 之後沒有可量化的滲透率或已成形的第二條曲線，半導體設備有週期，長期回到公司 9–12% 的長期營收目標附近較合理。","capital":"資本配置中等：回購有紀律、SBC 稀釋輕，但 FY26 自由現金流為負，回購靠的是資產負債表而不是當年現金。","valuation":"現價要求 FY27–FY28 共識（10.33／11.79 美元）兌現、之後每年仍有約 10% 成長、倍數守在 18 倍左右，五年年化才約 6%；前兩年我信，半導體設備高峰 EPS 配現行倍數我不信，估值偏滿。","how_wrong":"最可能看錯的地方是把半導體設備高峰的成長與營益率當常態；其次是成長吃掉現金，EPS 好看但股東拿不到現金。陷阱風險黃燈。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 175 美元以下（基本情境五年年化約 10%），且 FY27 營收成長指引未下修到 13% 以下","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟠","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"EMS/ODM","price_at_dd":214.32,"week26_return_pct":-18.37,"consensus_rev_3m_pct":25.52,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母採 FY27E 非GAAP 共識（排除 SBC 等），GAAP 與非GAAP 每季約差 0.3 美元；FY1 共識『近三個月 +25.5%』可能混入財年換檔，真實上修以財報後 +2.1% 為準。分母本身不是爭點。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"FY2026 10-K 申報","impact":"中","watch":"前十大客戶占比、是否出現單一客戶 ≥10%、馬來西亞集中與 IMMEX 風險描述是否改寫"},{"date":"2026-11","date_precision":"month","type":"other","event":"Baird 工業論壇（11-11）","impact":"低","watch":"管理層對半導體設備能見度與 FY27 指引的說法是否改變"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報（季末 2027-01-02）","impact":"高","watch":"營收是否落在 14.1–14.6 億美元、非GAAP營益率 6.0–6.4%、航太國防季增是否 ≥8%、FY27 全年指引"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"Q2 FY2027 財報","impact":"中","watch":"營益率是否如 CFO 所說季節性不降、上半年累計 FCF、現金循環天數"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,476B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期</h2>
<p class="lead">護城河等級 C，靠執行與再認證，不靠定價權，方向判穩定。</p>
<ul class="pts">
<li>機制是受監管、高組合低量產品的製造執行與再認證轉換成本。醫療 Class III 器材、飛行加油系統、太空電子換廠要重新認證，形成專案層級的轉換成本。再加上現金循環 62 天的營運資金效率，把約 5% 的營益率放大成 15.8% 的 ROIC。這不是專利，也不是定價權。</li>
<li>評分是執行 7、定價 5。執行面的證據有三項：上行期仍拿到份額，IR 副總稱這種情況少見。ROIC 由 Q1 的 13.2% 升到 Q4 的 15.8%。現金循環從 69 天降到 64 天再到 62 天。FY26 贏單年化約 12 億美元，航太國防單年贏單 4.9 億美元，超過 FY23 到 FY25 合計。</li>
<li>定價面只能給中性。公司毛利率 10.08% 與 SANM 9.0%、FLEX 9.5%、BHE 10.38% 落在同一區間，營益率 5.02% 居中。CFO 自己說價格與組合的貢獻相當有限。FCF 率 −1.0% 則是同業最差，對手在 3.32% 到 4.66% 之間。</li>
<li>對最強同業要誠實比。第三方彙整站的 ROIC 顯示 CLS 39.5%、JBL 29.8%、FLEX 19.2% 都高於 PLXS 的 18.7%（2026 Q1 口徑），只贏 SANM 的 11.3%。口徑與公司自報不同，只能當方向參考。JBL 的差距主要在資產周轉，1.6 倍對 1.3 倍。對自身 WACC 9% 的利差是 6.8 個百分點，且在擴大。</li>
<li>護城河方向判穩定，不判擴大。執行改善有一部分來自半導體設備順週期與年底固定成本槓桿。毛利率與同業同區間，沒有溢價。這兩面合起來，方向是持平。要改判擴大，需要看到 FY27 FCF 達標且前十大客戶占比回落。</li>
<li>威脅有三項，都是黃燈。製程無專利保護，資源更大的同業或客戶自製可能帶來降價與丟單，機率約 20%。零組件漲價在調價空檔由公司吸收，機率約 30%。醫療品質事件方面，2025-01 有一份 FDA 483 檢查缺失，不是警告信，之後未見召回。若升級，會直接傷到占營收 39% 的醫療部門贏單，機率約 10%。</li>
<li>報酬持續期屬低利益率、高周轉。四個檢查點三黃一綠，見§4。增量 ROIC 約 12%–20%，FY26 的再投資率逾 100%，FY27 約 65%。這個組合能守住 15% 的 ROIC，但不容易再大幅上移。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```