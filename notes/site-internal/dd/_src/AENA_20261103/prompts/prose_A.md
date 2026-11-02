你是 stock-analyst v20 的**散文層（prose）agent**，標的 AENA（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AENA_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：AENA　日期：2026-11-03　archetype：None　前份裁決：2026-07-11　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1969B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（450B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（812B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1681B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1204B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（471B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1108B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2356B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4123B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2740B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1969           3522-5031      5 條（2–6 內）  
s3                  8000         450           5285-7550      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3697          7912-11303      5 條（2–6 內）  
s6                 11000         471          7370-10529      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1108           1674-2392      3 條（2–6 內）  
s10                 5000        2356           1851-2644      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2740           2000-2260      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4879B；至少需散文≈40.12KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−59.5%
−50%
−45
−45%
−44%
−38%
−21
−21%
−10%
−5%
−4.4%
−0.59%
0%
0
0.1
0.33%
0.4
0.5
0.51
0.57%
0.59%
0.601
0.75
0.8%
0.81
0.84
0.9
0.99
1
1%
1.09
1.26
1.3%
1.31
1.32
1.36
1.42
1.46
1.47
1.5
1.5%
1.55
1.6
1.62
1.64
1.66
1.70
1.72
1.74
1.82
1.87
1.88
1.9
1.9%
1.93
1.98
02
2%
2.0%
2
2.03
2.1
2.13
2.22
2.32%
2.35
2.4%
2.5
2.5%
2.51%
2.6
2.7%
3%
3.0%
3
03
3.1%
3.2%
3.22
3.26
3.4%
3.63
3.7%
3.8
3.82%
3.9
3.9%
3.949%
04
4
4%
4.0
4.1%
4.4%
4.5%
4.6%
4.6
4.9
4.9%
05
5
5%
5.5
5.7
5.8%
6%
6
6.08
6.5%
6.7%
6.87
07
7
7.44%
7.5%
7.6
7.8%
7.9%
8
8.0%
8%
8.1%
8.3%
8.32%
9
09
9%
9.015
9.5
9.839
10
10%
10.3
10.7%
11
11%
11.4
12
12.5%
13.73
14
14.44%
15.0
15
15.05
15.16
15.4
15.86
15.9
15.94%
16
16.3
16.5
16.8%
17%
17.28
18
19
19.29
19.6%
19.68
20%
20
20.79
21%
21
21.16
21.367
21.8
22%
22
22.1
23%
23.32%
23.5
24
24.4
25
26
26.3
26.94
27%
27.3
27.46%
27.56
27.6
29
30%
30
30.45
30.779
31
32%
32.3
32.996
33.7
34.9
35
35%
37%
40%
40.81%
41
42
42.3
43.0%
43.29%
47%
47.4%
47.51%
47.7%
48
48%
49
49.8
50%
51%
55
58%
60%
61.06%
65%
65.7%
70
70%
70.36%
74.65%
80%
82%
90
95%
100%
100
120
130
150%
343.5
2015
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
2032
20261103
1,133.5
1,635
1,774.7
2,811.3
3,000
3,077.9
5,283.9
5,845
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
{"meta":{"ticker":"AENA","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Aena S.M.E., S.A."},"oneliner":"DORA III 以年均 +0.33% 費率、准許 WACC 8.32% 落地，監管方向的風險已經解除，剩下的是成本控制與 130 億歐元投資的執行風險。現價約 15.9 倍 FY2026E 本益比，估計 Base 年化報酬約 6%。等年底策略計畫確認 80% 配息，或股價回到 14 倍再談。","thesis":{"H":[{"id":"H1","text":"DORA III 的受管制段按核定兌現：2027 年成本重設後，西班牙網絡營運費用的成長不會明顯快過旅客與核定成本軌跡，策略性投資也按時程執行。","2y":null,"5y":"2031 年受管制成本實際值，超出核定的 20.79 億歐元（2026 固定價）不到 5%","10y":null,"threshold":"2027 年起，西班牙網絡 OpEx 年增減旅客年增 ≤ 4pp；各機場投資執行率 ≥ 80%（法定彈性下限）","source":"Aena 季報西班牙網絡成本表；DORA III 年度執行資料；2026-09-21 投資人說明會","drift_rule":"缺口超過 4pp 連 4 季＝削弱；超過 6pp 連 6 季＝反轉"},{"id":"H2","text":"非受管制段（商業、不動產、國際）帶動集團 EPS 年增 ≥ 3%，抵銷受管制費率年均只有 +0.33% 的逆風。","2y":"新標 MAG（特許店 +82%、餐飲 2027 年 +11%／2028 年 +37%）如期入帳；商業與不動產每旅客營收以 2026 年第一季的 €7.6 為起點，每年 ≥ +3%","5y":null,"10y":null,"threshold":"商業與不動產每旅客營收（排除直線法）年增 ≥ 3%；FY2027 EPS ≥ 共識 1.82 的 95%","source":"Aena 季報商業段揭露；Koyfin 共識快照","drift_rule":"連 2 季低於門檻 5% 以上＝削弱；連 3 季低於門檻 10% 以上＝反轉"},{"id":"H3","text":"130 億歐元的投資週期，不犧牲股東的現金回報：配息率維持 80%，槓桿與評等守得住。","2y":null,"5y":"2027–2031 年配息率維持 80%，淨負債/EBITDA 不超過 2.5x，評等維持 A 級","10y":null,"threshold":"配息率 ≥ 80%；淨負債/EBITDA ≤ 2.5x（Fitch 預估 2026–2030 平均約 1.9x）；Moody's／Fitch 維持 A 級","source":"2026 年底策略計畫；Aena 季報淨負債；Moody's、Fitch 評等公告","drift_rule":"槓桿連 4 季高於 Fitch 路徑 5% 以上＝削弱；配息率下修＝反轉"}],"R":[{"id":"R1","text":"燃油避險到期、載客率轉弱、地緣衝突，讓西班牙交通量轉弱；交通量風險由公司自擔，會同時打到受管制收入與商業收入。","h_ref":"H2","clock":"⚡","threshold":"西班牙網絡月度旅客 YoY 連 3 個月 ≤ −5% 監控；連 3 個月 ≤ −10% 減碼","evidence_refs":["geo_supply_chain#1"]},{"id":"R2","text":"核定成本比公司提案低約一成，CFO 承認部分項目做不到；人事費用連年雙位數成長，會吃掉准許報酬。","h_ref":"H1","clock":"🔥","threshold":"2027 年起，西班牙網絡 OpEx 年增減旅客年增，連 4 季 > 4pp","evidence_refs":["regulated_rate_case_roe#0","regulatory_antitrust#0"]},{"id":"R3","text":"最大客戶 Ryanair（占 19.6%，第一季量年減 3.4%）持續撤出區域機場運力；區域機場的固定成本攤不掉，商業收入也跟著流失。","h_ref":"H1","clock":"🔥","threshold":"Ryanair 占西班牙網絡旅客比重 < 17%，或單季年減 > 10%","evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R4","text":"政治與社會容忍度：CNMC 主張降費、曾有凍結費率的修正案、自治區要求共管，期中修法或 DORA IV 大幅降費，會壓縮受管制報酬。","h_ref":"H3","clock":"🐢","threshold":"費率凍結或共管完成立法；或 CNMC 在 DORA IV 前置報告中主張 WACC 低於 7.5%","evidence_refs":["end_markets#3","regulatory_antitrust#0"]},{"id":"R5","text":"投資執行落後：Tenerife South 流標、已發包比例仍很低、巴塞隆納擴建核准不由 Aena 掌控；策略性項目落後會被罰，擴建容量也會延後。","h_ref":"H1","clock":"🔥","threshold":"任一年度策略性投資遭罰，或延到 DORA IV 的金額 > 10 億歐元","evidence_refs":[]}],"single_thing":{"description":"2027–2031 策略計畫（預計 2026 年底前發布）把配息率由 80% 下修到 70% 以下，或改為以股代息，用來支應約 130 億歐元的投資。","why_fatal":"本檔的總回報約三分之二來自股息（殖利率約 4%，EPS 年化約 3%）。配息率由 80% 降到 65%，等於股息少將近兩成；靠殖利率支撐的本益比會失去錨，終端倍數要改看 12 倍一帶，五年價格報酬由正轉負。","if_happens":"未持有：取消進場條件並重跑 DD。已持有：減碼一半，在新配息政策下的殖利率回到 5% 以上之前不回補。","how_monitor":"看策略計畫的財務目標（配息率、淨負債上限、2031 年淨利目標）。對照基準：2026-07-29 CFO 說新計畫出來前 80% 配息不偏離，以及 Fitch 平均槓桿約 1.9x 的假設。","probability":"12 個月內約 20%。管理層承諾 80% 配息，董事長也預告目標企圖心高；但管理層已承認債務會大幅上升，並拒絕回答可接受的槓桿上限。"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.16,"peg_fy2":3.8,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.42,"FY2026E":1.74,"FY2027E":1.82,"FY2028E":1.88},"fy_end_month":12,"eps_basis":"共識 EPS 為 Koyfin 快照，事實表標美元口徑，與判斷日股價同幣別。FY2025A 的 1.42 是年報歐元稀釋 EPS，幣別不同，不宜直接拿來和共識算成長率；三年共識成長以 FY2026E→FY2028E 的年化約 3.9% 為準。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AENA_20261103/scenario.json","archetype":{"primary":"受監管公用/穩定內需","secondary":null,"confidence":"高","fingerprint":"政府核定的五年費率框架＋單一國家機場網絡獨佔＋80% 配息＋大型受管制投資週期"},"industry":{"clock_phase":"III","sd_verdict_source":"需求屬結構性持久：由入境觀光帶動，2025 年國際線約 +6%、國內線持平。供給擴張受容量上限與監管核准約束，可逆性低。週期風險落在航空公司的運力與燃油成本，不在機場本身。來源：2026-02-25 年報法說、2026-07-29 半年報法說、Aena 上半年新聞稿。","bargaining":{"up":"上游是工程與維護承包商。CapEx 已發包的比例仍很低，Tenerife South 航廈標案無人投標，維護合約續約時範圍擴大、成本上升，議價力偏向承包商。","down":"下游是航空公司。Ryanair 占西班牙網絡旅客 19.6%；費率雖由政府核定，航空公司仍透過撤運力與遊說施壓（ALA 要求每年降價 4.9%）。","geo":"以西班牙單一國家的監管與政治風險為主，巴西（雷亞爾匯率）與英國特許為輔。"},"profit_pool_dir":"利潤池正由受管制航空段，移往商業（MAG 調升、VIP、停車）、不動產與國際段；受管制段的報酬由准許 WACC 封頂。","tam_table":{"expanded":false,"reason":"受監管機場網絡的成長要看受管制資產基礎、費率與交通量，不適用 TAM 滲透率的框架。交通量路徑另以 DORA III 假設的 2031 年 3.63 億旅客追蹤。"}},"moat":{"mechanism":"政府特許的國家級機場網絡獨佔，單一營運商、費率受管制；商業段以 MAG 標案把旅客流量變現。護城河來自法源而非競爭，報酬上限也由監管決定。","execution":7,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價擴大：受管制費率 2027–2031 年均 +0.33%、准許 WACC 8.32%，都優於 CNMC 建議；新標 MAG 特許店 +82%、餐飲 2028 年 +37%，VIP 每旅客 +27%。執行縮減：西班牙網絡 OpEx +7.9%、旅客 +3.2%，人事 +12.5%，核定成本比公司提案低約一成。兩者相抵，判為持平。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用利潤率替代；ADP、Flughafen Zürich 兩家的利潤率也缺值。","threats":[{"level":"🟡","text":"Ryanair 撤出區域機場運力：2026 夏季再砍 120 萬座位，Valladolid 旅客 −59.5%（2025 年報導資料）。網絡整體仍在成長，屬點對點攻擊；真正的風險是區域機場的固定成本攤不掉。","p":35,"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"level":"🟡","text":"監管與政治壓價：CNMC 建議 DORA III 降費，並呼籲政府確保 2031 年前降費。終裁沒有採納，但 DORA IV 與期中修法仍是壓力。","p":20,"evidence_refs":["regulatory_antitrust#0","end_markets#3","regulated_rate_case_roe#0"]},{"level":"🟡","text":"高鐵替代國內線：鐵路可靠時，馬德里–巴塞隆納、馬德里–馬拉加以高鐵為主。2026 上半年因鐵路故障讓旅客回流航空，屬一次性。","p":25,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"第三方系統單點失效：2025 年 9 月報到系統遭攻擊，波及多個歐洲機場；Aena 自身的供應商集中度未揭露。","p":10,"evidence_refs":["geo_supply_chain#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉（營業利益率 47.51%；投入資本周轉率事實表未涵蓋，依機場資產重的性質判斷）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"三個角色分開看：使用者是旅客，決策者是航空公司（決定航線配置），付款者是旅客（機場費含在票價裡）。入境觀光屬需要而非想要；2026 上半年西班牙旅客 +3.7%，管理層估全年約 +3%。弱點是載客率轉弱與燃油避險到期（2026-07-29 法說）。"},{"item":"決策層級","level":"🟡","text":"替代性要從航空公司「這架飛機放在哪個機場」的層級看。主樞紐與島嶼幾乎沒有替代，區域機場的替代性高：Ryanair 撤運力後，Valladolid 旅客 −59.5%。對旅客而言，替代品只有高鐵，而且只限國內線。"},{"item":"價值鏈分配","level":"🟡","text":"管理層引用 IATA 資料：歐洲航空公司每旅客收入增加約 27%，同期西班牙機場費實質下降 37%（2015–2025，2026-04-16 股東會）。受管制段在價值鏈中分到的份額在縮小；商業段則靠 MAG 標案，把零售承租人的利潤拿回來（特許店 MAG +82%）。"},{"item":"社會容忍度","level":"🔴","text":"屬於高必要、高敏感的類型：費率要部長會議核准，CNMC 主張降費，航空公司要求每年降 4.9%，曾有凍結費率的修正案，自治區也要求共管。管理層自己承諾讓西班牙費率維持歐洲最具競爭力。實際的定價上限是政治上限，低於經濟上限。"}],"roiic":"約 8.3%：受管制增量資本以准許 WACC 8.32% 為上限（稅前或稅後口徑事實表未涵蓋）；若成本超出核定，實際報酬會更低","reinvest_rate":"約 37%（淨利口徑）：留存 20%（配息 80%）＋舉債空間約 17%","endo_ceiling":3.0,"formula_note":"內生成長＝增量報酬 × 再投資率 ≈ 8.3% × 37% ≈ 3.1%，保守取 3.0%。舉債空間的算法：淨負債/EBITDA 由 1.47x 升到 Fitch 預估的 2026–2030 平均約 1.9x，約每年 0.1x EBITDA；以前 9 個月 EBITDA 30.779 億年化約 41 億、淨利年化約 23.5 億估算，約占淨利 17%。D&A 與投入資本事實表未涵蓋，以上是量級估計，不是精算。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","AENA":74.65,"ADP.PA":null,"FHZN.SW":null,"ASR":47.63,"PAC":55.6,"unit":"%"},{"metric":"營業利益率","AENA":47.51,"ADP.PA":null,"FHZN.SW":null,"ASR":40.81,"PAC":43.29,"unit":"%"},{"metric":"FCF 利潤率","AENA":15.94,"ADP.PA":null,"FHZN.SW":null,"ASR":23.32,"PAC":14.44,"unit":"%"}],"competitors":[{"name":"ADP.PA","gm":null,"om":null,"fcf_margin":null,"strategy_note":"巴黎機場集團的利潤率事實表無資料。同為受管制歐洲機場，可作監管框架對照：第一季法說中 UBS 提到，法國監管機關表示下期會把燃油衝擊納入交通量與 WACC 假設。數字無法比較。"},{"name":"FHZN.SW","gm":null,"om":null,"fcf_margin":null,"strategy_note":"蘇黎世機場的利潤率事實表無資料。它與 Aena 同場競標 Galeão，是海外特許的直接對手，但 Galeão 最後由 Aena 拿下。"},{"name":"ASR","gm":47.63,"om":40.81,"fcf_margin":23.32,"strategy_note":"營業利益率 40.81%，低於 Aena；FCF 利潤率 23.32%，高於 Aena。Aena 的 FCF 落差主要來自巴西建設期與投資增加，ASR 的投資節奏事實表未涵蓋。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PAC","gm":55.6,"om":43.29,"fcf_margin":14.44,"strategy_note":"營業利益率 43.29%、FCF 利潤率 14.44%，都與 Aena 相近；同樣是受管制費率加商業收入的雙軌結構，但監管國別不同，不宜直接當倍數錨。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量（交通量年增約 2%～3%，受馬德里、巴塞隆納容量管理限制）＋價（受管制費率 +0.33%／年＋通膨 P 因子；商業 MAG 調升）＋併購（Leeds／Newcastle 51%、Galeão 100%）；無回購","runway_years":"受監管業務不適用滲透率。DORA III 到 2031 年，擴建容量在 DORA IV（2032 年起）交付，可見跑道約 10 年，但擴建核准不由 Aena 掌控","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段的再投資空間：增量報酬約 8.3% × 再投資率約 37% ≈ 3.0%","segments":{"expanded":false,"reason":"分部營收事實表只收錄上半年商業營收 9.839 億（約占上半年總營收 32.996 億的 30%）一項，航空、不動產、國際的金額都沒有收錄。利潤組合的爭點在受管制成本，不在分部組合。"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"年度毛利率由 61.06% 升到 70.36%（2022–2025）。季度毛利率事實表未涵蓋；第一季排除 IFRIC 12 的 EBITDA 利潤率 47.4%，對比前一年 47.7%，屬持平"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"國家網絡獨佔，不適用；最大客戶 Ryanair 移出運力另列為威脅"},{"signal":"提價後銷量下滑","lit":true,"note":"2026 年費率調漲約 6.5% 後，Ryanair 砍區域機場座位，Valladolid −59.5%；網絡整體仍 +3.7%，屬局部現象"},{"signal":"EPS 成長顯著高於營收成長","lit":false,"note":"共識 FY2026E→FY2027E：EPS +4.6%、營收 +4.9%"},{"signal":"FCF/NI 連 2 年低於 0.75","lit":true,"note":"2025 年 0.81，TTM FCF 利潤率降到 15.94%。DORA III 投資年均約 26 億歐元，未來數年會結構性低於 0.75，原因是投資週期而非營運惡化"},{"signal":"SBC/營收高於 5% 且上升","lit":false,"note":"2022–2025 年股數持平，約 15 億股"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"高鐵替代只限國內線；eVTOL 仍在可行性研究階段"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"同業倍數事實表未涵蓋"},{"signal":"維護性 capex 占 FCF 高於 60%","lit":null,"note":"維護與擴張的拆分事實表未涵蓋；第一季 capex 約 3 億，多用於安全與設施改善"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"DORA III 投資近 130 億"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"股東回報以 80% 配息為主，沒有回購。併購（Leeds／Newcastle 51%、Galeão 約 4.9 億歐元）合計約占市值 2%，成長主要來自受管制資產基礎與商業標案，不靠併購撐。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Luton、巴西 ANB／BOAB 已併入，國際業務占 2025 年合併 EBITDA 逾一成；ANB 排除 IFRIC 12 後 EBITDA 利潤率 65.7%。但投入資本與收購對價事實表未涵蓋，增量報酬無法與 WACC 比較。Leeds／Newcastle、Galeão 都在 2026 年才交割","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"事實表與逐字稿都沒有回購計畫，股東回報全部走 80% 配息","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"淨利 ÷ 稀釋 EPS：2022 年 9.015 億 ÷ 0.601 ≈ 15.0 億股，2025 年 21.367 億 ÷ 1.42 ≈ 15.05 億股，四年持平；目前股數 15 億，淨稀釋約每年 0%，低於 1.5%","grade":"過"}]},"valuation":{"basis":"股息殖利率＋股息成長為主錨，FY2026E 前瞻本益比為輔；同業倍數事實表未涵蓋","tier":"歐洲受管制機場營運商","peers":{"expanded":false,"reason":"同業本益比與殖利率事實表未涵蓋。同業對照只有利潤率，而且 ADP、Flughafen Zürich 缺值，無法做同層級的倍數錨。"},"fwd_pe":15.86,"peg":4.0,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 15.86x，EPS 兩年年化 3.9%，殖利率約 3.9%。要有 8% 年化，FY2031 EPS 需約 2.13 且倍數不降；Base 為 2.03、終端 15 倍，估計年化約 6%，低於 8%。P/S、EV/S 在 4 個年度端點最高。五年分位事實表未涵蓋。結論偏貴。","upside_short_pct":4.6,"upside_mid_pct":10.3},"trap_analysis":{"verdict":"🟡","label":"受監管成長兌現，但成本與舉債吃掉股東每股經濟的中度風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2026-07-29 法說提到冬季航季沒有能見度、載客率轉弱、燃油避險到期；DORA 期間交通量風險由 Aena 自擔；最大客戶 Ryanair 占 19.6%，且正在撤出區域運力。","assumption":"西班牙旅客年增維持 2%～3%，不出現疫情或燃油危機等級的衝擊。","consequence":"若 2027–2028 年出現燃油或地緣衝擊、旅客年減 5%～10%，而成本已重設在高位，EPS 可能跌到 1.6 附近，本益比壓到 10 倍以下，五年後虧損 40%～50%。","ruling":"部分採納。A1 評等與 1.47x 的淨負債/EBITDA，讓公司撐得過一個衝擊年，−50% 不是五年終點的合理中心，因此放進最大回撤下緣（−45%），不放在 Bear 終點。這個故事與唯一致命點部分重疊：衝擊年最可能逼出配息下修。","watch":"西班牙網絡月度旅客 YoY、載客率、航空燃油價格","evidence_refs":["geo_supply_chain#1","customer_concentration_credit#0"],"fact_refs":["f_kpi5_net_financial_debt_net_d"]},{"view":"論點成功但股東經濟變差","evidence":"核定的受管制成本在 2027–2031 年只增加 7.8%（2026 固定價），CFO 承認部分項目做不到；董事長說債務會大幅上升；第一季債務平均成本升到 2.51%；130 億投資會推高折舊。","assumption":"受管制資產基礎增加逾 55 億歐元、准許 WACC 8.32%，能轉成每股盈餘成長。","consequence":"投資如期完成、交通量也達標，但成本超支，利息與折舊吃掉准許報酬，EPS 年增只剩 1%～2%；FCF 長期付不完配息。股東拿到的是更大的資產，而不是更多的每股現金。","ruling":"採納。Base 已把 2029 年後 EPS 年增壓到約 2.5%，Bear 路徑五年後 EPS 1.64 對應的就是這個故事。","watch":"西班牙網絡 OpEx 年增減旅客年增、淨負債/EBITDA、平均債務成本","evidence_refs":["regulated_rate_case_roe#0","regulatory_antitrust#0"],"fact_refs":["f_kpi5_net_financial_debt_net_d"]},{"view":"價格已反映太多","evidence":"FY2026E 本益比 15.86x，EPS 兩年年化 3.9%，PEG 約 4.0；P/S 6.08x、EV/S 6.87x 都在 4 個年度端點的最高點；26 週漲 21%。Jefferies 引用 2027 年本益比 16.3x，TipRanks 平均目標價 €27.56。","assumption":"市場用低成長公用事業約 16 倍的倍數定價，認為 DORA 落地後成長穩定。","consequence":"Base 年化約 6%，低於 8%。若本益比回到 14 倍、EPS 照共識走，兩年後價格約 26.3，價格報酬約 −5%。","ruling":"採納，不追，進場價設在 14 倍 FY2026E（24.4）。P/S 分位偏高，部分反映利潤率由 32% 升到 47%，所以主看本益比。","watch":"FY2026E／FY2027E 共識本益比","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#0"],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_ev_s_percentile","f_week26_return_pct"]},{"view":"論點失敗","evidence":"CNMC 建議 DORA III 每年降費 0.59%、WACC 7.44%，並呼籲政府確保 2031 年前降費；曾有修正案要凍結 DORA III 期間的機場費；部分自治區要求共管機場，2026-04-16 股東會稱這構成重大風險；Ryanair 公開指責 Aena 壟斷。","assumption":"在政府持股之下，費率仍按法定程序核定，不會被期中修法改寫。","consequence":"若期中凍結費率，或 DORA IV 大幅降費，受管制段報酬會掉到資金成本以下，終端倍數從 15 倍掉到 12 倍以下。","ruling":"短期反駁、長期採納。DORA III 已由部長會議核准，2031 年前的費率路徑已鎖定；CEO 在 2026-02-25 說政治干預不會再發生，這是承諾，不是證據。Base 終端 15 倍略低於現值，Bear 的 12 倍反映這條風險。","watch":"國會的費率相關修正案、自治區共管立法、CNMC 對 DORA IV 的前置報告","evidence_refs":["end_markets#3","regulatory_antitrust#0","regulated_rate_case_roe#0"]}],"max_dd":{"lo":-45,"hi":-21,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 26.94 → 本次 27.6（+2.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=26.94","side_b":"本次 price_at_dd=27.6","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 26.94 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 26.94 美元：Bull 價 49.8、Bear 價 22.1，五年期望值 +43.0%，基準年化 8.0%，不對稱比 5.7","side_b":"本次情境、股價仍用 26.94 美元：Bull 價 42.3、Bear 價 19.68，五年期望值 +10.7%，基準年化 2.5%，不對稱比 1.55","ruling":"先換情境、股價不動：五年期望值少 32.3 個百分點，基準年化少 5.5 個百分點。不對稱比由 5.7 變為 1.55。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 26.94 美元：五年期望值 +10.7%，基準年化 2.5%，不對稱比 1.55","side_b":"本次情境、股價 27.6 美元：五年期望值 +8.1%，基準年化 2.0%，不對稱比 1.36","ruling":"再換股價、情境不動：起點價上漲 2.4%，五年期望值少 2.6 個百分點，基準年化少 0.5 個百分點，不對稱比由 1.55 降到 1.36。合計五年期望值比前份少 34.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"交通量指引：管理層保守，實際與監管假設偏高","cause":null,"prior_field":null,"side_a":"2026-02-25 CEO 說 2026 年西班牙客流 +1.3% 是自然預估；DORA 提案假設 2027–2031 年年增 1.3%。","side_b":"2026-07-29 執行副董事長改口為約 +3%；上半年實際 +3.7%，CAPA 稱 Aena 低估需求；DORA 核定 2031 年 3.63 億旅客，約年增 2%。","ruling":"可調和，屬程度差異。管理層在費率提案期有低報交通量的誘因；實際偏高對 Aena 有利，因為每旅客費率已鎖定、交通風險自擔。但 2027 夏季起馬德里、巴塞隆納按航廈管理容量，上行有天花板，所以 Base 只用約 2%～3%。","evidence_level":"逐字稿＋公司新聞稿＋CAPA 報導","settle_metric":"2027 年西班牙網絡旅客年增率，對比 2%","if_then":["若 2027 年旅客年增 ≥ 3%，且 OpEx 缺口 ≤ 4pp → 上調 Bull 機率並重跑 DD","若 2027 年旅客年增 < 1% → 停止加碼，Bear 機率提到 35%"],"evidence_refs":["supply_demand_durability#2","end_markets#2"]},{"axis":"營運費用：公司提案假設與核定上限的落差","cause":null,"prior_field":null,"side_a":"2026-04-29 CFO 說 DORA III 提案數字仍有效，但承認油價帶動的通膨當時沒有納入；2026-02-25 CFO 說人事費用上升的趨勢不會改變。","side_b":"2026-09-21 核定受管制成本由 2027 年 19.29 億增至 2031 年 20.79 億（2026 固定價）；Bernstein 指出比原始假設低約一成，CFO 承認部分項目有很高的風險做不到，差異數字延到策略計畫才說明。","ruling":"可調和，但幅度大：兩邊都往上，差在速度。2025 年實際受管制成本 16.5 億，重設到 2027 年的 19.29 億，等於已容納約每年 8% 的成長；之後四年核定只增 7.8%（約每年 1.9%），公司人事費用卻仍是雙位數成長。這是第一個假設成不成立的主戰場，Base 已把 2029 年後 EPS 年增壓到 2.5%～2.7%。","evidence_level":"逐字稿（2026-02-25、04-29、09-21）","settle_metric":"2027 年起西班牙網絡 OpEx 年增減旅客年增","if_then":["若 2027 年起連 4 季 > 4pp → 停止加碼，Bear 機率提到 35%","若連 6 季 > 6pp → 減碼一半","反向條件：若策略計畫的 OpEx 目標不高於核定軌跡，且 2027 上半年缺口 ≤ 2pp → 解除這條警示"],"evidence_refs":["regulated_rate_case_roe#0","regulatory_antitrust#0"]},{"axis":"80% 配息承諾與債務大幅上升","cause":null,"prior_field":null,"side_a":"2026-07-29 CFO 說 80% 配息政策不會偏離，新政策要等 DORA 之後的策略計畫；2026-04-16 董事長希望在策略計畫中確認配息率。","side_b":"2026-09-21 董事長說債務會大幅上升；2026-07-29 UBS 問可接受的槓桿上限，管理層不給數字；Fitch 預估 2026–2030 平均淨槓桿約 1.9x（9 月底為 1.47x）。","ruling":"可調和。A1／A+ 評等與 1.9x 的路徑還有空間，維持 80% 的機率較高。但這是唯一致命點，決勝數據在年底的策略計畫，在那之前不可裁決。","evidence_level":"逐字稿＋評等機構","settle_metric":"策略計畫的配息率與淨負債上限","if_then":["若配息率 < 70% 或改以股代息 → 取消進場條件並重跑 DD；已持有則減碼一半","若維持 80% 且淨負債上限 ≤ 2.5x → 解除唯一致命點，進場只剩價格條件"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"投資執行：不超投的承諾與發包進度","cause":null,"prior_field":null,"side_a":"2026-09-21 執行副董事長說不會投超過核定的 100 億；CFO 說工程招標一向要求固定價格。","side_b":"同一場 CFO 說已發包的比例「仍很低」，不給百分比；Tenerife South 航廈流標；策略性投資占 40%～50%，落後會被罰；部分投資可能延到 DORA IV。","ruling":"可調和。投資延後會降低近期的債務與折舊，對短期 EPS 反而有利；但策略性項目落後有罰則，擴建容量延後也會壓抑 DORA IV 的成長。列為中期風險，不改 Base。","evidence_level":"逐字稿 2026-09-21","settle_metric":"年度受管制投資執行率（法定彈性下限 80%）與策略性項目罰款","if_then":["若任一年度策略性投資遭罰，或延到 DORA IV 的金額 > 10 億歐元 → 下修五年後的跑道判斷並停止加碼"],"evidence_refs":[]},{"axis":"共識下修與營運上修方向相反","cause":null,"prior_field":null,"side_a":"FY2026E 共識 EPS 三個月由 1.82 降到 1.74（−4.4%），近兩週再降 0.57%。","side_b":"同期交通量的全年估計由 1.3% 上調到約 3%；前 9 個月淨利 1,774.7 百萬歐元；第二季 EBITDA 只比共識低 0.8%。","ruling":"不可裁決，要等到 2027-02 年報。下修原因事實表未涵蓋，可能包含美元換算或成本預估上調。Bear 第一年 EPS 1.72 已低於現行共識，不再另外下調。","evidence_level":"Koyfin 快照＋公司新聞稿","settle_metric":"FY2026 實際 EPS，對比 1.74","if_then":["若 FY2026 實際 EPS 低於 1.70 → Bear 機率提到 35%，重算終端倍數","若 FY2027E 共識再下修超過 5% → 停止加碼"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"DORA III 終裁每年 +0.33%，優於 CNMC 建議的 −0.59%；WACC 8.32%，高於 CNMC 的 7.44%；Moody's 升 A1、Fitch 升 A+；交通量超出預期；MAG 在 2027–2028 年大幅調升；董事長預告策略計畫的財務目標企圖心高，年底前就是催化劑；殖利率約 4%。","side_b":"現價為 15.9 倍 FY2026E，EPS 兩年年化 3.9%，P/S、EV/S 在 4 個年度端點最高；要有 8% 年化，FY2031 EPS 需約 2.13 且倍數不降，Base 只有 2.03。","ruling":"不追。好消息大多已反映在 7 月之前的漲幅裡（26 週 +21%，7 月以來只 +2.4%），剩下的上行要等策略計畫給出高於共識的 2031 年目標。","evidence_level":"公司新聞稿＋評等機構＋賣方報導","settle_metric":"策略計畫 2031 年淨利目標隱含的 EPS 年化成長","if_then":["若策略計畫的 2031 年淨利目標隱含 EPS 年化 ≥ 5%，且維持 80% 配息 → 重跑 DD，進場價可放寬到 15 倍 FY2027E（約 27.3）","若股價在策略計畫發布前先漲到 30 以上 → 不追"],"evidence_refs":["capital_markets_pricing#0","customer_concentration_credit#3"]},{"axis":"前份觀望的主因（DORA III 終裁）已落地","cause":"新證據","prior_field":["signal","archetype","cycle_position"],"side_a":"前份結論為觀望、追蹤，等待 2026-09-30 前的 DORA III 終裁，要求年化費率 ≥ 持平。","side_b":"2026-09-15 部長會議核准：年均 +0.33%、WACC 8.32%、受管制投資近 100 億。前份第二個假設成立。","ruling":"訊號維持 B，類型維持受監管公用；非循環股，不設景氣位置。監管方向的風險解除，但綁定約束改為估值（Base 年化約 6%）。本輪結論依新輸入重新判定。","evidence_level":"公司新聞稿＋投資人說明","settle_metric":null,"if_then":[],"evidence_refs":["regulated_rate_case_roe#1","regulated_rate_case_roe#2"]},{"axis":"估值結論維持偏貴","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 26.94，估值偏貴。","side_b":"本輪股價 27.6（+2.4%），FY2026E 本益比 15.86x，Base 年化約 6%。","ruling":"估值結論不變。本益比下降來自共識 EPS 上移，不是因為股價變便宜。","evidence_level":"事實表","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"情境機率與回撤區間調整","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 32%、Bear 23%，最大回撤 −38%。","side_b":"本輪 Bull 22%、Base 48%、Bear 30%；最大回撤 −21% 到 −45%。","ruling":"本輪加做內生天花板檢核：Base EPS 年化 3.1%，略高於天花板 3.0%，Bear 機率因此提高到 30%。DORA 終裁費率已知（+0.33%，低於 Aena 申請的 +3.82%），Bull 失去高費率路徑，散布收窄。最大回撤改給區間，下緣對應交通衝擊年 EPS 1.62 乘以 9.5 倍。","evidence_level":"情境推導","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"價值陷阱風險升一級，護城河與跑道不變","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"前份：陷阱 🟢、護城河持平、五年後跑道 🟡。","side_b":"本輪：陷阱 🟡（區域機場量縮、FCF/NI 將跌破 0.75、核定成本偏緊、FY2026E 共識三個月 −4.4%）；護城河持平；跑道 🟡（擴建在 DORA IV 交付，但核准不由公司掌控）。","ruling":"陷阱風險升一級，原因是成本與舉債對每股經濟的壓力已有證據，不是監管方向轉壞。商業定價力擴大，抵銷了執行面的變差，所以護城河仍判持平。","evidence_level":"逐字稿＋報導＋事實表","settle_metric":"西班牙網絡 OpEx 缺口、FCF/NI","if_then":["若 2027 年 FCF/NI 低於 0.5 且 EPS 未達共識 → 陷阱判斷升為 🔴，停止加碼"],"evidence_refs":["competitive_share_entrants#0","regulated_rate_case_roe#0"]},{"axis":"進場條件重設","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"DORA III 政府終裁允許 ≥ 持平關稅路徑（2026-09-30 前）且訴訟風險釐清，或股價回落至 €24 以下（Fwd PE ≤15x）","side_b":"股價 ≤ 24.4（FY2026E 共識本益比 ≤ 14 倍）且年底策略計畫維持 80% 配息率，兩者同時成立才重跑 DD 決定進場首倉","ruling":"前份進場條件的 DORA 那一半已在 2026-09-15 觸發（+0.33% ≥ 持平），訴訟風險事實表未涵蓋；價格那一半沒有觸發（現價 27.6）。監管不確定性解除後，綁定約束改為估值與配息政策，進場首倉改成價格與策略計畫兩個條件同時成立。倍數門檻由 15 倍降到 14 倍，因為 DORA 費率已知偏低、2029 年後成長放慢，要到 14 倍才有約 8%～9% 的年化報酬。","evidence_level":"公司新聞稿＋事實表","settle_metric":"股價與策略計畫配息率","if_then":[],"evidence_refs":["regulated_rate_case_roe#2"]},{"axis":"Single Thing 新設","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"2027–2031 策略計畫（預計 2026 年底前發布）把配息率由 80% 下修到 70% 以下，或改為以股代息，用來支應約 130 億歐元的投資","ruling":"前份最大的二元事件是 DORA III 終裁，已經落地。本輪最大的單一敏感項改為策略計畫的配息率：總回報約三分之二來自股息，配息率由 80% 降到 65%，等於股息少將近兩成，直接打到靠殖利率支撐的本益比。若發生，取消進場條件並重跑 DD；已持有則減碼一半。","evidence_level":"逐字稿 2026-04-16、07-29、09-21","settle_metric":"策略計畫配息率","if_then":["若配息率 < 70% → 減碼一半，未持有則取消進場條件"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（null）","side_b":"本輪設五條：配息率 < 70%；2027 年起 OpEx 缺口連 4 季 > 4pp；月度旅客連 3 個月 ≤ −10%；淨負債/EBITDA > 2.5x；Ryanair 占比 < 17%","ruling":"前份只在風險敘述裡帶門檻，本輪把門檻集中成每季可以核對的指標。任一條觸發，已持有就減碼一半；配息率與月度旅客兩條同時觸發則清倉。","evidence_level":"方法調整","settle_metric":null,"if_then":["任一條觸發 → 減碼一半","配息率與月度旅客兩條同時觸發 → 清倉"],"evidence_refs":[]},{"axis":"風險門檻的退休與替換","cause":"新證據","prior_field":["thesis.R"],"side_a":"前份 R1：連 3 月旅客 YoY −5% 監控、連 3 月 −10% 減碼。R2：DORA III 終裁採 CNMC 降價路徑，年化費率低於持平。R3：EU ETS 航空碳權全額拍賣，IATA 歐洲 10 年交通 CAGR 下修。","side_b":"R1 門檻原樣保留（−5% 監控、−10% 減碼）。R2 退休：終裁為 +0.33%，門檻確定不會成立。R3 改為長期的政治與社會容忍度風險；交通量的長期門檻，改看 DORA 假設的 2031 年 3.63 億旅客。","ruling":"R2 退休，理由是事件已結算，而且方向對 Aena 有利。ETS 本輪沒有新證據，前份門檻原文已截斷、無法核對；既然交通量風險由公司自擔，改用更直接的 DORA 旅客路徑來監測。R1 的減碼門檻不變。","evidence_level":"公司新聞稿＋前份判斷","settle_metric":null,"if_then":[],"evidence_refs":["regulatory_antitrust#0"]}],"triggers":[{"n":1,"text":"年底策略計畫若把配息率降到 70% 以下，或改以股代息，唯一致命點成立","type":"Single Thing","maps_to":"H3","metric":"2027–2031 策略計畫配息率","threshold":"< 70% 或改以股代息","action":"未持有：取消進場條件並重跑 DD；已持有：減碼一半","source_freq":"Aena 策略計畫，一次性（預計 2026 年底前）","date":"2026-12-31","evidence_refs":["customer_concentration_credit#2"]},{"n":2,"text":"股價回到 14 倍 FY2026E，且策略計畫維持 80% 配息，才重跑 DD","type":"估值rearm","maps_to":"H3","metric":"股價 ÷ FY2026E 共識 EPS；策略計畫配息率","threshold":"股價 ≤ 24.4 且配息率 ≥ 80%","action":"重跑 DD，確認後建立首筆小部位","source_freq":"股價每日；策略計畫一次性","date":null,"evidence_refs":[]},{"n":3,"text":"受管制成本重設後，西班牙網絡營運費用的成長若持續明顯快過旅客，准許報酬會被吃掉","type":"假設驗證","maps_to":"H1","metric":"西班牙網絡 OpEx 年增減西班牙旅客年增","threshold":"2027 年起連 4 季 > 4pp；連 6 季 > 6pp","action":"連 4 季：停止加碼；連 6 季：減碼一半","source_freq":"Aena 季報，每季","date":"2027-07-31","evidence_refs":["regulated_rate_case_roe#0"]},{"n":4,"text":"商業與不動產每旅客營收成長若低於 3%，非受管制段撐不起 EPS","type":"假設驗證","maps_to":"H2","metric":"商業與不動產每旅客營收（排除直線法調整）年增","threshold":"連 2 季 < +3%","action":"停止加碼","source_freq":"Aena 季報，每季","date":"2027-04-30","evidence_refs":[]},{"n":5,"text":"西班牙旅客的月度年增轉負，而交通量風險由公司自擔","type":"風險","maps_to":"R1","metric":"西班牙網絡月度旅客 YoY","threshold":"連 3 個月 ≤ −5% 監控；連 3 個月 ≤ −10% 減碼","action":"≤ −10%：減碼一半；未持有則凍結進場條件，直到旅客回正","source_freq":"Aena 月度交通量，每月","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":6,"text":"最大客戶 Ryanair 持續撤出運力","type":"風險","maps_to":"R3","metric":"Ryanair 占西班牙網絡旅客比重與年增","threshold":"占比 < 17% 或單季年減 > 10%","action":"停止加碼，重算區域機場成本攤提對 EPS 的影響","source_freq":"Aena 季報分航空公司交通量，每季","date":null,"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":7,"text":"投資週期把槓桿推過評等容忍區","type":"減碼","maps_to":"H3","metric":"淨負債/EBITDA；Moody's／Fitch 評等","threshold":"> 2.5x，或任一家評等降到 A 級以下","action":"減碼一半","source_freq":"Aena 季報；評等公告","date":null,"evidence_refs":[]},{"n":8,"text":"期中修法凍結費率，或自治區共管機場入法","type":"清倉","maps_to":"R4","metric":"國會費率凍結修正案、機場共管立法","threshold":"任一案完成立法程序","action":"清倉；未持有則移除進場條件","source_freq":"國會議程，事件型","date":null,"evidence_refs":["end_markets#3","regulatory_antitrust#0"]},{"n":9,"text":"FY2026 年報與策略計畫發布後複審","type":"複審日期","maps_to":null,"metric":"FY2026 EPS 對比 1.74；2027 年交通量與 OpEx 指引","threshold":"到期即複審","action":"重跑 DD","source_freq":"一次性","date":"2027-03-15","evidence_refs":[]}],"kill_metrics":[{"metric":"2027–2031 策略計畫配息率","bear_threshold":"< 70% 或改以股代息","window":"2026-12 策略計畫發布","source":"Aena 策略計畫","last_status":"unknown"},{"metric":"西班牙網絡 OpEx 年增減西班牙旅客年增","bear_threshold":"2027 年起連 4 季 > 4pp","window":"2027Q1–2028Q4","source":"Aena 季報","last_status":"warning"},{"metric":"西班牙網絡月度旅客 YoY","bear_threshold":"連 3 個月 ≤ −10%","window":"每月滾動","source":"Aena 月度交通量","last_status":"ok"},{"metric":"淨負債/EBITDA","bear_threshold":"> 2.5x","window":"每季","source":"Aena 季報","last_status":"ok"},{"metric":"Ryanair 占西班牙網絡旅客比重","bear_threshold":"< 17%","window":"每季","source":"Aena 季報分航空公司交通量","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=21.16, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='受監管公用/穩定內需', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價 ≤ 24.4（FY2026E 共識本益比 ≤ 14 倍）且年底策略計畫維持 80% 配息率，兩者同時成立才重跑 DD 決定首倉","exec_line":"觀望，不追。綁定約束是估值：估計 Base 年化約 6%，低於 8%；策略計畫的配息率是唯一致命點。兩者都過關，才重跑 DD 決定首倉。"},"reasoning":{"industry":"收入分四塊。①受管制航空收入：每旅客費率由五年期 DORA 核定，2027–2031 年均 +0.33%，交通量風險由 Aena 自己承擔（2026-04-16 股東會）。②商業收入：零售、餐飲、免稅以最低保證租金（MAG）標案打底，停車與 VIP 自營；上半年 9.839 億歐元，約占上半年總營收 32.996 億的 30%。③不動產（貨運、物流地上權）：第一季 +16.8%。④國際特許：Luton、巴西 ANB／BOAB、2026-05 併入的 Leeds／Newcastle（51%）、2026-10 交割的 Galeão（100%）；國際業務占 2025 年合併 EBITDA 逾一成。航空、不動產、國際三個分部的金額事實表未收錄。最新數字：前 9 個月營收 5,283.9 百萬歐元、EBITDA 3,077.9 百萬（約 58%）、淨利 1,774.7 百萬；TTM 毛利率 74.65%、營業利益率 47.51%。巴西 Congonhas 的 IFRIC 12 建設收入沒有利潤，會灌大營收、壓低利潤率；第一季排除這部分後，集團營收只成長 6%。單點依賴有兩個：一是最大客戶 Ryanair 占西班牙網絡旅客 19.6%（第一季，量年減 3.4%）；二是費率要由部長會議核定的監管依賴。產業態勢分三面看。競爭面：Ryanair 撤出區域機場運力，easyJet 部分填補，屬局部惡化。結構面：DORA III 核准，Moody's 升 A1、Fitch 升 A+，屬轉好。法規面：CNMC 主張降費、自治區要求共管、曾有凍結費率的修正案，風險仍在。整體判為雙向拉鋸。景氣位置判第三階段：交通量成長由 2025 年上半年 +4.5% 降到 2026 年上半年 +3.7%，馬德里、巴塞隆納自 2027 夏季航季起按航廈管理容量，管理層也說載客率轉弱、燃油避險到期。增速在放慢，但需求沒有反轉。","moat":"護城河的機制是政府特許的國家級機場網絡：航線要落地西班牙，就得用 Aena 的機場。這條護城河來自法源，報酬上限也由監管決定。定價面：DORA III 費率年均 +0.33%，介於 Aena 申請的 +3.82% 與 CNMC 建議的 −0.59% 之間；准許 WACC 8.32%，高於 CNMC 主張的 7.44%。WACC 數字取 Quartr 投資人說明摘要；2026-09-21 逐字稿摘錄寫成 2.32%，不在 CNMC 7.44% 與 Aena 9% 之間，判為轉錄誤植。商業面新標 MAG 大幅調升，CFO 在 2026-07-29 也說 VIP 仍有定價力。執行面：第一季西班牙網絡 OpEx +7.9%、人事費用 +12.5%，同期旅客只 +3.2%。核定的受管制成本由 2027 年 19.29 億增至 2031 年 20.79 億（2026 固定價），CFO 承認部分項目有很高的機率做不到。最大客戶 Ryanair 正把運力移出區域機場，最大客戶的份額方向往下，護城河不能判為擴大。同業 ROIC 事實表未涵蓋，改用利潤率比較：Aena 營業利益率 47.51%，高於 PAC 的 43.29% 與 ASR 的 40.81%；FCF 利潤率 15.94%，低於 ASR 的 23.32%，落差主要來自投資週期。評分：執行 7 分、定價 8 分，等級 B。當期 ROIC 屬高利益率、低周轉，但投入資本事實表未涵蓋，無法計算。","growth":"成長來源是量、價加上小型併購，沒有回購。量：交通量約年增 2%～3%。DORA 核定 2031 年西班牙網絡 3.63 億旅客；2025 年約 3.22 億（由 2026 年 1.3% 預測對應 3.26 億推回），換算約年增 2%。馬德里、巴塞隆納自 2027 夏季起管理容量。價：受管制費率年均 +0.33%，再加通膨 P 因子；過渡期的 1% 上限已取消，但 CFO 不保證能完全轉嫁通膨。商業 MAG 的調升排到 2028 年。併購：Leeds／Newcastle 自 2026-05 併入、Galeão 自 2026-10 併入，2027 年會有整年效益。共識 EPS：FY2026E 1.74、FY2027E 1.82、FY2028E 1.88，兩年年化 3.9%（Koyfin 快照，分析師家數未載；營收共識分別為 16 與 19 位分析師）。內生天花板約 3.0%（見護城河段），缺口約 0.9pp。缺口可以歸因：一是收購（2027 年 Leeds／Newcastle、Galeão 整年併入），二是 2027 年受管制成本基期重設帶來的一次性抬升，不依賴重新評價。Base 假設 2029 年後 EPS 年增約 2.5%～2.7%。衰退信號亮兩個：區域機場在費率調漲後量縮；投資週期下 FCF/NI 將跌破 0.75（2025 年 0.81，FCF 利潤率由 FY2025 的 27.46% 降到 TTM 的 15.94%）。","governance":"FCF/NI 轉換率：2022 年 1.26、2023 年 0.51、2024 年 0.99、2025 年 0.81，起伏來自投資節奏。SBC 占營收事實表未涵蓋；但以淨利除以稀釋 EPS 推算，2022 年與 2025 年的股數都約 15.0 億股，四年持平。現金去向（2026 年前 9 個月）：營業現金流 2,811.3 百萬歐元；投資付現 1,133.5 百萬（含 Leeds／Newcastle 股權 343.5 百萬）；配息約 1,635 百萬（每股 1.09 歐元 × 15 億股，4 月發放，與 CFO 所說的約 16 億一致）；剩約 0.4 億。Galeão 約 4.9 億歐元在 10 月交割，不在前 9 個月的數字內。9 月底淨財務負債 5,845 百萬，為 EBITDA 的 1.47x，第一季底是 1.32x。2025 年底的槓桿口徑有出入：2026-02-25 CFO 說 1.46x，2026-04-16 股東會說 1.31x，事實表未說明差異來源。DORA III 投資年均約 26 億歐元，是 2025 年 FCF 17.28 億的 1.5 倍，在 80% 配息下，淨負債會持續上升；Fitch 預估 2026–2030 平均約 1.9x。","valuation":"這是受監管公用事業，主錨用股息殖利率加股息成長，以及前瞻本益比；PEG 只作參考。前瞻本益比 15.86x（判斷日股價 27.6 ÷ FY2026E 共識 1.74），FY2027E 為 15.16x；EPS 兩年年化 3.9%，PEG 約 4.0。股息殖利率約 3.9%（事實表口徑）。回推需求：8% 年化減掉約 3.9% 殖利率，股價需年化約 4.1%，五年後約 33.7；以 15.86 倍回推，FY2031 EPS 需約 2.13。Base 路徑在 2028 年後因費率 +0.33%、利息與折舊上升而放慢，只到 2.03，終端 15 倍對應約 30.45，估計年化約 6%。P/S 6.08x、EV/S 6.87x 都位於 4 個年度端點的最高點，但部分原因是營業利益率由 32% 升到 47%，所以主看本益比。trailing P/E 13.73x 低於 forward，方向與 EPS 成長相反，疑似幣別或分母口徑混用，不當作承重依據。五年分位所需的高低點事實表未涵蓋。","premortem":"最可能看錯的三處，詳見反證紀錄：受管制成本吃掉准許報酬；年底策略計畫下修配息；交通量在容量上限與燃油衝擊下轉弱。衰退信號亮兩個：區域機場漲價後量縮，以及投資週期下 FCF/NI 將跌破 0.75。另有一個訊號方向不明：FY2026E 共識 EPS 三個月下修 4.4%，與營運面上修方向相反，原因事實表未涵蓋。26 週漲 21%；RSI 事實表標示不可用，所以不拿來判斷動能是否過熱。"},"plain":{"six":{"how_it_makes_money":"Aena 收的是航空公司與旅客的過路錢：受管制機場費，加上把人流變現的商業租金。錢卡在西班牙機場使用權這個節點，但費率天花板由政府決定。","moat":"護城河方向持平。法源獨佔沒有鬆動，商業段的定價力在擴大；但受管制段的費率被政治封頂，成本執行也在變差，兩邊相抵。","growth":"五年後的成長跑道屬中等。DORA III 讓受管制資產基礎增加逾 55 億歐元，馬德里、巴塞隆納擴建的容量要到 DORA IV 才完整交付，但擴建核准不由 Aena 掌控，目前看不到可驗證的第二條成長曲線。","capital":"資本配置屬中等。配息率 80%、不做回購、股數持平；併購規模小、時間又新，增量報酬還無法驗證。未來五年投資近 130 億，FCF 付不完配息，差額要靠舉債。","valuation":"要有 8% 年化報酬，現價需要 FY2031 EPS 約 2.13（年化約 4%），而且本益比守在 15.9 倍。我們的 Base 只到 2.03，判為偏貴，不追。","how_wrong":"最可能看錯的地方在成本與配息，而不在監管方向。價值陷阱風險屬中等。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等年底策略計畫確認配息率 ≥ 80%，且股價 ≤ 24.4（FY2026E 共識本益比 ≤ 14 倍）；兩者同時成立才重跑 DD","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"受監管公用/穩定內需","price_at_dd":27.6,"week26_return_pct":21.16,"consensus_rev_3m_pct":-4.4,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母採 FY2026E 共識 EPS 1.74（事實表標美元口徑，與判斷日股價同幣別）。第二季約 3,000 萬歐元的疫情期 MAG 和解收入屬一次性，約占全年淨利 1%，不構成爭點。另外，trailing P/E 13.73x 低於 forward；股息殖利率 3.949% 恰好等於每股 1.09 歐元 ÷ 27.6，兩者疑似混用歐元與美元，所以不承重。短期上行＝FY2027E 1.82 × 現值 15.86 倍；中期上行＝Base 五年後價格 30.45，不含股息。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"2027–2031 策略計畫發布（配息率、淨負債上限、2031 年財務目標）","impact":"高","watch":"配息率是否 ≥ 80%；2031 年淨利目標隱含的 EPS 年化成長"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"公布 2027 年費率的 K 因子與 P 因子","impact":"中","watch":"P 因子能否轉嫁 2026 年約 10% 的西班牙 OpEx 通膨"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 年報與 2027 年交通量指引","impact":"中","watch":"FY2026 EPS 對比 1.74；2027 年交通量與 OpEx 指引"},{"date":"2027-03","date_precision":"month","type":"regulatory","event":"DORA III 第一年費率生效（依往年 3 月 1 日調費的慣例）","impact":"中","watch":"費率調整後航空公司的運力配置，特別是 Ryanair 在區域機場的動向"},{"date":"2027-03","date_precision":"month","type":"capacity","event":"馬德里、巴塞隆納自 2027 夏季航季起按航廈管理容量","impact":"中","watch":"兩大樞紐旅客成長是否被壓到 2% 以下"}],"_projected_from":"v19"}
```
