你是 stock-analyst v20 的**散文層（prose）agent**，標的 V（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/V_20261103/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：V　日期：2026-11-03　archetype：None　前份裁決：2026-07-29　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2041B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（489B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1080B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1692B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1329B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（440B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1028B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2342B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4570B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3832B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2041           3471-4959      5 條（2–6 內）  
s3                  8000         489           5258-7511      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4101          7629-10899      5 條（2–6 內）  
s6                 11000         440          7392-10560      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1028           1730-2472      5 條（2–6 內）  
s10                 5000        2342           1861-2658      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3832           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5291B；至少需散文≈39.71KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−45
−45%
−43%
−34%
−30
−30%
−20%
−0.05%
0.0%
0.12%
0.5
0.6
0.6%
0.63
0.75
0.95
1
01
1.08
1.5%
1.7%
1.7
1.82
2.0%
2%
2
2.07
2.1
2.34
2.39
2.5
03
3%
3
3.2
3.3%
3.3
3.43
3.48
3.5%
3.5
3.6%
4
4%
04
4.05
4.58
4.6%
5
5%
5.5
5.63
6
06
6%
7.00
7%
7.0%
7
07
7.3%
7.6%
8%
8
08
8.0%
9%
09
9
9.28
9.6%
10
10%
10.2%
10.6%
10.7%
11
11%
11.4
11.6%
11.9%
12
12%
12.3%
12.32
13
13%
13.19
13.27
13.3%
13.5
13.7%
13.8%
13.95%
14%
14
14.2%
14.2
14.6
14.90
14.9
15
15%
15.02
15.03
15.2
15.2%
15.26
15.35
15.7%
15.9
16
16%
16.3%
16.6
16.7
16.71
17%
17
17.13
17.36
17.53
17.75
17.9%
18
18%
18.2
18.37%
18.4%
18.52%
18.65
19%
19.51
19.82%
20%
20
20.45
20.75
20.9
21
21%
21.4
22
22.95
23
23.45
24
24%
24.5
24.5%
24.89
25
25%
25.8
26
26.8
27%
27
27.9
28
28.36
28.4
29
30
30%
30.9
30.95%
30.95
31
31%
31.6%
32
32.1
32.12
33
34.6
35%
40%
40
41
42
42.52%
44.91%
45
45%
45.04%
48%
48
49
49.8%
50%
50
51.7
52
52.0%
53.0%
53.9%
59
59.8%
60
60%
60.07%
60.3%
61.0%
61%
64%
65.57%
66%
66.6%
67%
67.15%
70
77%
79.75%
79.88
80
80%
80.36%
81%
84%
85%
90
100%
100
120
121.39
136
140
150%
150
180
220.57
225
227.7
237.28
243
244
248
250
280
281.1
282.2
298
327
$340
340
342.76
343
350
360
366.59
387
400
405
406
417
426.3
459
470
473
496
543
590
597
610
670
722
784
830.8
928
2018
2022
2023
2026
2027
2028
20261103
2,813
20,058
21,577
22,057
45,900
7,966
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
{"meta":{"ticker":"V","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Visa Inc."},"oneliner":"收全球刷卡與轉帳過路費的雙邊網路，定價與加值服務撐住低雙位數成長；股價三個月漲 16%、前瞻本益比 28 倍，Base 年化約 7%～8%，續抱不追，等 360 美元以下或 Q1 FY27 證明指引保守再加碼。","thesis":{"H":[{"id":"H1","text":"Visa 網路的交易量維持結構性成長：電子支付持續取代現金與支票，並延伸到企業支付與帳戶間轉帳，替代軌道只在邊緣侵蝕。","2y":null,"5y":"FY2031 前固定匯率支付量年增維持 7% 以上、處理筆數 8% 以上","10y":null,"threshold":"支付量（固定匯率）≥+7%、處理筆數 ≥+8%、跨境量（不含歐洲內部）≥+10%；FY2026 分別為 +9%、+9%、+13%","source":"Visa 季報新聞稿與法說（2026-10-27 Q4 FY26：支付量 +9%、跨境 +14%、筆數 +10%）","drift_rule":"支付量成長連 4 季低於 7% → 削弱；連 6 季低於 5% → 反轉"},{"id":"H2","text":"續約高峰年下定價權仍成立：FY2027 有 25% 支付量續約，淨營收仍能低雙位數成長，網路費不被監管直接設限。","2y":"FY2027～FY2028 調整後淨營收年增 ≥10%、非 GAAP 營益率 ≥64%","5y":null,"10y":null,"threshold":"調整後淨營收成長 ≥10%；服務收入成長減前季支付量成長 ≥+3pp；非 GAAP 營益率 ≥64%（Q4 為 66.6%）","source":"FY2027 指引與 Q4 FY26 法說（CFO：定價貢獻與 FY2026 同量級、集中下半年）","drift_rule":"淨營收成長連 2 季低於 9% → 削弱；連 3 季低於 7% 或出現網路費上限立法 → 反轉"},{"id":"H3","text":"加值服務與 CMS 讓成長和消費量脫鉤：兩者占淨營收由 FY2026 逾四成升到一半，Visa 由網路變成按能力收費的服務商。","2y":null,"5y":null,"10y":"FY2036 前加值服務加 CMS 占淨營收過半，加值服務年增長期高於支付量成長 10pp 以上","threshold":"加值服務成長 ≥18%（FY2027 指引 20% 出頭、FY2026 +30%）；CMS 成長 ≥12%（FY2026 +19%）","source":"Q4 FY26 法說（CEO：加值服務 140 億美元、約 2023 年的兩倍；三組合合計 +20% 以上可延續到 FY2027）","drift_rule":"加值服務成長跨 2 個財年低於 15% → 削弱；跨 3 個財年 → 反轉"}],"R":[{"id":"R1","text":"續約高峰年的客戶誘因吃掉定價：FY2027 約 25% 支付量續約、含多家大客戶，Q4 誘因 +21% 已較前季加速 3 點；FY2027 EPS 指引低於指引前共識，若續約靠更高誘因換來，淨營收會落在指引下緣以下。","h_ref":"H2","clock":"🔥","threshold":"客戶誘因成長減淨營收成長 >12pp 連 2 季","evidence_refs":["capital_markets_pricing#0"]},{"id":"R2","text":"DOJ 借記卡壟斷案走向救濟：案件仍在證據開示與審前階段，投資人集體訴訟雖被駁回，政府民事案本身未解；美國借記是規模優勢最集中之處，受影響營收事實表未涵蓋。限制誘因與路由合約會壓低借記定價。","h_ref":"H2","clock":"🐢","threshold":"法院裁定行為或結構性救濟","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#3","major_events#2"]},{"id":"R3","text":"交換費監管外溢到網路層：歐盟將再評估 IFR、可能壓低上限並擴大到其他費用；美國信用卡交換費和解 2026-06 初步核准；訴訟託管 2026-09 再撥 4.05 億。監管對象若由交換費延伸到網路費，定價貢獻會縮。","h_ref":"H2","clock":"🐢","threshold":"任一主要市場對網路費設上限或納入管制","evidence_refs":["regulatory_antitrust#0","end_markets#2","major_events#3"]},{"id":"R4","text":"替代軌道承接主流流量：即時支付在至少 80 國上線、GENIUS 法案給穩定幣制度基礎，10-K 自承穩定幣可能顛覆跨境與企業支付，新進者多半偏離傳統網路模式；帳戶間支付對卡量是雙面刃。","h_ref":"H1","clock":"🐢","threshold":"國際支付量（固定匯率）成長連 2 季 <5%，或 Visa Direct 交易成長 <10%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0","substitute_technology#1","substitute_technology#3","substitute_technology#4"]},{"id":"R5","text":"大型發卡行自建網路：Capital One 借記卡已轉 Discover、信用卡測試中，其他擁有替代網路或聯盟的發卡行可能跟進。","h_ref":"H1","clock":"🔥","threshold":"Capital One 信用卡全面遷移，或另一家美國前十大發卡行轉網路","evidence_refs":["customer_second_source#0"]},{"id":"R6","text":"跨境量受地緣與總經打斷：關稅、貿易報復、制裁（俄羅斯業務 2022 年起停止）與中東衝突直接影響跨境旅遊；超過半數淨營收在美國以外。","h_ref":"H1","clock":"⚡","threshold":"跨境量（不含歐洲內部）成長連 2 季 <8%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]}],"single_thing":{"description":"美國國會通過信用卡路由法案（CCCA），強制大型發卡行在信用卡加開第二個非 Visa／Mastercard 網路，由商戶選擇路由。","why_fatal":"美國信用卡是 Visa 定價最高的流量；路由開放後網路費要和第二網路競價，FY2027 指引中每年約 3～4pp 的定價貢獻會先被削去，定價假設直接反轉。美國信用卡營收占比事實表未涵蓋，衝擊幅度無法精算。","if_happens":"任一院表決通過減碼至半倉；簽署成法減碼至四分之一，重跑完整研究並把 Bear 改為 Base。","how_monitor":"國會委員會與院會議程、是否附掛在必過法案；Visa 法說對路由的說明；美國信用卡支付量成長（Q4 +11%）。","probability":"12～24 個月約 10%：2026-01 屬重新提出、尚未立法；美國信用卡交換費和解 2026-06 初步核准，可能降低立法急迫性。"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"高","fpe_fy2":24.89,"peg_fy2":1.82,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":13.27,"FY2027E":15.03,"FY2028E":17.13,"FY2029E":19.51},"fy_end_month":9,"eps_basis":"非 GAAP 稀釋 EPS（Koyfin 共識；基期 FY2026 實際 13.27 取自 2026-10-27 法說），財年 9 月底結束"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/V_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"輕資本雙邊網路：毛利率約 80%、營益率約 66%、資本支出不到營收 4%，成長來自支付量×定價×加值服務，回購吃掉大半自由現金流。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：FY2026 支付量 +9%、處理筆數 +9%、跨境量 +13%（Q4 新聞稿與法說），十月至 21 日美國支付量 +10%、跨境 +15%；需求來自支付數位化與新流量，可逆部分是跨境旅遊（中東衝突）與匯率波動度。","bargaining":{"up":"上游是資料中心、雲端與軟體供應商，可替換，無單一供應商超過七成的揭露。","down":"下游發卡行握有議價力：最大客戶 FY2022 占淨營收 10%，FY2027 約 25% 支付量續約、客戶誘因 Q4 +21%；Capital One 已把借記卡轉到自家 Discover 網路、信用卡在測試。","geo":"超過半數淨營收來自美國以外；俄羅斯 2022 年起停業；中國人民銀行已核准 Visa 準備境內清算的申請（法說，CEO）。"},"profit_pool_dir":"監管把交換費從發卡行推回商戶（美國信用卡交換費和解平均降 10bp 為期五年、歐盟 20／30bp 上限），網路費尚未被直接觸及；發卡行透過續約誘因向 Visa 要回部分利潤，誘因成長快於營收。","tam_table":{"expanded":false,"reason":"事實表未涵蓋電子支付滲透率、各區 TAM 與利潤池占比的時間序列；Visa 不是低滲透新品類，論點靠支付量、定價與加值服務三個已揭露的實績指標承重，不靠 TAM 擴張數字。"}},"moat":{"mechanism":"雙邊網路效應加信任層：52 億張憑證與逾 2 億受理點互相鎖定，代幣化、詐欺與爭議處理規則讓發卡行、商戶與代理商務都需要 Visa 憑證；新進者要同時攻下兩邊。","execution":9,"pricing":9,"grade":"A","trend":"→","trend_evidence":"執行與定價皆判穩定：定價差額（服務收入減支付量 +4pp、資料處理減筆數 +6pp）延續、加值服務 +30%；但 Capital One 借記卡轉網路是有來源的大客戶份額下滑，客戶誘因 Q4 +21%（前季 +18%），抵銷擴大證據。","peer_na_reason":null,"threats":[{"level":"🟡","text":"政府主導即時支付（FedNow、PIX、UPI）已在至少 80 國上線，跨境即時支付連結將與 Visa 跨境業務競爭，帳戶間支付對卡量是雙面刃。屬逐國點狀侵蝕：巴西受理點 +40%、印度 +15%，國際支付量仍 +9%。升級條件：美國 FedNow 出現實體商戶端規模應用。","p":"40%（五年內在更多新興市場侵蝕境內借記與轉帳）","evidence_refs":["competitive_share_entrants#1","substitute_technology#4"]},{"level":"🟡","text":"GENIUS 法案後穩定幣有了制度基礎，10-K 自承可能顛覆跨境與企業支付，新進者多半偏離傳統網路模式；分析師視為最大長期威脅，但缺消費者保護與詐欺管理層。Visa 以結算（年化逾 250 億美元、年增 10 倍）、逾 225 個穩定幣連結卡計畫與 Open USD 參與，附著在自身網路上。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#3","competitive_share_entrants#0"]},{"level":"🟡","text":"發卡行兼網路的垂直整合：Capital One 借記卡已轉 Discover、信用卡測試中，大客戶有了現成替代網路；目前只有一家發卡行具備這種條件。","p":"35%（24 個月內信用卡部分遷移）","evidence_refs":["customer_second_source#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（持卡人）、決策者（發卡行選網路、商戶選受理）、付款者（商戶付手續費、發卡行付網路費）三角色都成立；支付是需要不是想要，延後成本高。FY2026 處理 2,813 億筆 +9%、支付量 +9%，十月至 21 日仍 +10%。代理變數：處理筆數成長。"},{"item":"決策層級","level":"🟡","text":"替代決策發生在發卡行整個卡組合的多年合約，不在單筆交易，到期時以誘因競價。Capital One 證明擁有替代網路的大型發卡行會換；FY2027 約 25% 支付量續約。代理變數：客戶誘因成長（Q4 +21%）與續約結果。"},{"item":"價值鏈分配","level":"🟡","text":"商戶手續費大部分是交換費歸發卡行，Visa 拿的網路費占比小但最難取代；監管壓交換費後，發卡行透過續約誘因向網路要回利潤，誘因成長快於營收是價值往發卡端移動的讀數。"},{"item":"社會容忍度","level":"🟡","text":"政治上限低於經濟上限：歐盟 IFR 已設 20／30bp 上限且將再評估；美國信用卡交換費和解 2026-06 初步核准、CCCA 2026-01 再提、DOJ 借記卡案進行中。法源是反壟斷與國會立法，第二網路路由的替代方案已在政策討論中；目前打到的是交換費與路由，網路費未被設上限。"}],"roiic":"粗估約 77%（上限估計）：FY2026 淨營收增量約 59 億美元 × TTM 營益率 65.57% × （1 − 長期稅率 19%）≈ 31 億美元增量稅後營業利益，對照資本支出 16.71 億加已宣布的 BioCatch 24 億＝41 億美元；投入資本與折舊攤銷事實表未涵蓋，增量多來自定價與名目消費，並非資本推動。","reinvest_rate":"約 7%～18%：資本支出 16.71 億 ÷ 稅後營業利益約 227.7 億（GAAP 營業利益 281.1 億 × 81%）＝7.3%；加計 BioCatch 24 億一次性併購＝17.9%。","endo_ceiling":12,"formula_note":"單位為 %。內生成長＝增量報酬×再投資率，兩組粗估相乘約 13.8%，等同 FY2026 稅後營業利益增速；FY2026 含 Prisma 併購約 1pp 與 FIFA 一次性營收，扣除後取 12% 作上界。Visa 的成長瓶頸是名目消費與定價容忍度，不是資本；高報酬、低再投資，現金應回到股東。"},"combined":9.0,"score":9.0,"spread_table":[{"metric":"毛利率","V":79.75,"MA":78.42,"AXP":null,"COF":null,"PYPL":45.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","V":65.57,"MA":60.07,"AXP":null,"COF":null,"PYPL":18.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","V":44.91,"MA":42.52,"AXP":19.82,"COF":45.04,"PYPL":18.37,"unit":"%"},{"metric":"研發密度","V":null,"MA":null,"AXP":null,"COF":null,"PYPL":9.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"MA","gm":78.42,"om":60.07,"fcf_margin":42.52,"rd_intensity":null,"strategy_note":"同為四方開放網路，營益率 60.07% 對 Visa 65.57%、自由現金流率 42.52% 對 44.91%，差距是規模差；兩家同受交換費與路由監管，是同向風險，不是份額威脅。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"AXP","gm":null,"om":null,"fcf_margin":19.82,"rd_intensity":null,"strategy_note":"三方封閉網路兼發卡，自由現金流率 19.82%（毛利率與營益率事實表空白），以高端消費卡與商戶費率取勝，與 Visa 爭的是高端信用卡流量。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"COF","gm":null,"om":null,"fcf_margin":45.04,"rd_intensity":null,"strategy_note":"擁有 Discover 網路後借記卡已遷出 Visa、信用卡測試中，是最直接的客戶轉網路案例；自由現金流率 45.04% 屬銀行口徑，不可與網路公司直接比。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PYPL","gm":45.76,"om":18.52,"fcf_margin":18.37,"rd_intensity":9.56,"strategy_note":"錢包與結帳層，營益率 18.52%、自由現金流率 18.37%，多數交易仍跑在卡網路上，屬通路夥伴兼競爭者，近年未見把流量移出卡網路的證據。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量約 9～10pp、價約 3～4pp、併購約 1pp（Q4 淨營收 +13%），匯率波動度拖累；每股盈餘另有淨回購約 1.7pp。","runway_years":"10 年以上（滲透率事實表未涵蓋，以已實現的第二曲線判斷）","runway_post_y5":"🟢","endo_ceiling_basis":"內生上界 12%（推導見護城河段）：增量報酬約 77% × 再投資率約 18% ≈ 13.8%，等同 FY2026 稅後營業利益增速；扣 Prisma 併購約 1pp 與 FIFA 一次性後取 12%。缺口＝共識 13.7% − 12% ≈ 1.7pp，歸因淨回購（約市值 1.7%）。","segments":{"expanded":false,"reason":"事實表與逐字稿只揭露加值服務營收 140 億美元與 CMS 加 VAS 合計逾四成，未揭露分部利潤率，無法判斷組合變化對利潤的影響；利潤率以整體營益率追蹤。"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"季毛利率事實表未涵蓋；TTM 79.75% 對 FY2025 80.36% 小降 0.6pp"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"Capital One 借記卡轉 Discover 屬單一發卡行流失；Visa 單獨份額數字未取得，美國借記支付量 Q4 仍 +9%，列觀察"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"定價帶動服務收入 +14%，同期支付量 +9%～10% 未降"},{"signal":"EPS 年複合高於營收年複合逾 5pp","lit":false,"note":"FY2022～FY2026 營收年複合約 11.9%、GAAP EPS 約 15.2%（7.00 到約 12.32），差 3.3pp；前瞻 EPS 13.7% 對營收 FY1 到 FY2 +10.7%，差約 3pp"},{"signal":"自由現金流÷淨利連 2 年低於 0.75","lit":false,"note":"FY2024 0.95、FY2025 1.08"},{"signal":"SBC÷營收高於 5% 且逐年上升","lit":false,"note":"FY2026 SBC 9.28 億 ÷ 淨營收約 459 億 ≈ 2.0%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"即時支付與穩定幣在邊緣侵蝕，但支付量 +9%、跨境 +13%，未見總量萎縮"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"只有四個年度端點：P/S 17.36 倍在中位（51.7 分位），未見系統性下移；同業倍數未涵蓋"},{"signal":"維持性資本支出占自由現金流逾 60%","lit":false,"note":"資本支出 16.71 億僅占自由現金流 7.6%"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"持續建置新一代雲原生 VisaNet，營收年年成長"}],"trap_rating":"🟢"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：Q4 併購只貢獻淨營收約 1pp，FY2027 指引排除併購影響；現金返還以回購與股利為主，細項已在說明段交代。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Prisma、Newpay、BioCatch（24 億美元）、Featurespace、Pismo 的收購價與增量營業利益事實表未涵蓋；僅知 Prisma 與 Newpay 在 Q4 貢獻淨營收約 1pp、營業費用約 2pp、EPS 約 0.5pp。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購買入收益率＝1 ÷ 前瞻本益比 28.36＝3.5%；門檻為 10 年期公債殖利率加 2%，殖利率事實表未涵蓋，判不過的前提是殖利率高於 1.5%。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY2026 SBC 9.28 億美元，約市值 7,966 億的 0.12%，遠低於 1.5% 門檻；回購使淨股數下降。","grade":"過"}]},"valuation":{"basis":"前瞻本益比為主（FY2027E 共識 15.03）；情境樹用非 GAAP 落後口徑（FY2026 實際 13.27）以對齊五年終點","tier":"大型開放式支付網路（與 Mastercard 同級）","peers":{"expanded":false,"reason":"事實表的同業對照只有毛利率、營益率與自由現金流率，未涵蓋同業前瞻本益比，無法做倍數對照；終端倍數改以 Visa 自身現值（前瞻 28.4 倍、GAAP 落後 34.6 倍）校準。"},"fwd_pe":28.36,"peg":2.07,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"偏貴：前瞻本益比 28.4 倍、PEG 約 2.1（高於 2）、Base 年化約 7%～8%（低於 8%）；P/S 在四個年度端點中位（51.7 分位）。五年分位事實表未涵蓋（只有四個年度端點），留空不外推。短期上檔 8.0%＝FY2027E Base EPS 14.90 × 一年後落後本益比 30.9 倍；中期上檔 24.5%＝FY2029E 18.65 × 三年後 28.4 倍（本益比由 32.1 倍線性降到終端 26 倍）。","upside_short_pct":8.0,"upside_mid_pct":24.5},"trap_analysis":{"verdict":"🟢","label":"價值陷阱風險低：衰退信號零亮，觀察自由現金流率與發卡行轉網路"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Durbin 與 Marshall 2026-01 再提 CCCA；DOJ 借記卡壟斷案仍在證據開示與審前階段；歐盟將再評估 IFR，可能壓低上限並擴大到其他費用；國會引用 Visa 加 Mastercard 約占美國通用信用卡流通張數 84%；10-K 自承面臨多項反壟斷訴訟，可能涉及三倍賠償。","assumption":"監管只打交換費，不打網路費與路由。","consequence":"五年虧 50% 最可能的故事：CCCA 通過讓美國信用卡改為商戶選路由、DOJ 裁定限制借記誘因合約，定價貢獻（每年 3～4pp 營收）消失，再遇一次衰退；EPS 年增掉到 4%～5%、本益比 17 倍，股價約 280 美元（−34%），衰退低點再下探 −45%。","ruling":"部分採納：三條都在程序中但無一定案，Bear 機率由 27% 提到 30%；與唯一致命點（CCCA）重疊的部分由唯一致命點監測承接，DOJ 與歐盟另列觸發器。","watch":"CCCA 委員會或院會表決排程；DOJ 案簡易判決與審判日程；歐盟 IFR 影響評估結論。","evidence_refs":["end_markets#2","regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#3","major_events#2"],"fact_refs":["f_kpi5_guidance_fy2027_q1_fy27"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流率 FY2022 61.0%、FY2023 60.3%、FY2024 52.0%、FY2025 53.9%、FY2026 約 48%（220.57 億÷約 459 億），同期營益率維持 66%～67%；客戶誘因 Q4 +21%（前季 +18%）；訴訟託管 2026-09 再撥 4.05 億；BioCatch 24 億現金併購報酬未知。","assumption":"營收與營業利益成長會等比例變成可分配現金。","consequence":"營收照指引成長、論點全部成立，但每一元營收轉成的自由現金流持續變少，回購與併購又在高價位執行，每股價值增速低於 EPS 增速。","ruling":"採納為監測項，不改 Base：落差原因事實表未涵蓋（可能是誘因預付、訴訟支付與稅），FY2025 自由現金流÷淨利仍 1.08；FY2027 自由現金流率若跌破 40% 改列減碼條件。","watch":"FY2027 年報現金流量表：自由現金流÷淨營收、客戶誘因成長與淨營收成長的差距。","evidence_refs":["major_events#3"],"fact_refs":["f_kpi3_free_cash_flow_fy2026_23","f_peer_v_fcf_margin_pct","f_peer_v_operating_margin_pct"]},{"view":"價格已反映太多","evidence":"三個月漲 16.3%（366.59 到 426.3）、26 週 +30.95%，股價高於 52 週均線 24%；前瞻本益比 28.4 倍、PEG 約 2.1；FY2027 EPS 指引低雙位數到低十位數，共識 15.03（+13.3%）坐在指引上緣；財報前賣方目標價均值 406～417 美元、區間 327～473 美元。","assumption":"公司會像 FY2026 一樣超越指引，本益比不需要下修。","consequence":"成長照 Base 走、本益比回到 26 倍，五年年化只有 7%～8%；若管理層已預告的 Q2 成長低點碰上續約誘因加大，股價可回測 52 週均線 343 美元附近（約 −20%）而基本面無損。","ruling":"採納：不追價、持股不加，等 360 美元以下或 Q1 FY27 證明指引保守。現在就買的最強論證是 Visa 連兩年超越初始節奏、定價集中下半年、十月跨境 +15%，等回檔可能等不到；此論證交給 Q1 FY27 數據驗證，不提前行動。","watch":"FY2027E 共識 EPS 方向、Q1 FY27 淨營收與 EPS 成長、股價對 360 美元。","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"],"fact_refs":["f_price_at_dd","f_week26_return_pct","f_fwd_pe_latest","f_ma_w52","f_consensus_eps_fy1"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 366.59 → 本次 426.3（+16.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=366.59","side_b":"本次 price_at_dd=426.3","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟡→🟠、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟡→🟠、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 366.59 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 366.59 美元：Bull 價 784、Bear 價 248，五年期望值 +49.8%，基準年化 10.7%，不對稱比 3.5","side_b":"本次情境、股價仍用 366.59 美元：Bull 價 830.8、Bear 價 282.2，五年期望值 +53.0%，基準年化 10.2%，不對稱比 4.58","ruling":"先換情境、股價不動：五年期望值多 3.2 個百分點，基準年化少 0.5 個百分點。不對稱比由 3.5 變為 4.58。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 366.59 美元：五年期望值 +53.0%，基準年化 10.2%，不對稱比 4.58","side_b":"本次情境、股價 426.3 美元：五年期望值 +31.6%，基準年化 7.0%，不對稱比 2.34","ruling":"再換股價、情境不動：起點價上漲 16.3%，五年期望值少 21.4 個百分點，基準年化少 3.3 個百分點，不對稱比由 4.58 降到 2.34。合計五年期望值比前份少 18.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：管理層財測信用","cause":null,"prior_field":null,"side_a":"2026-07-28 Q3 法說 CFO：全年 EPS 成長在中十位數低端、Q4 營收與 Q3 調整後相近，FY2027 可見度來自續約、產品管線與定價。","side_b":"2026-10-27 Q4 法說：全年 EPS +16%、Q4 營收 +13%，FY2027 指引低雙位數營收、低雙位數到低十位數 EPS，與 Q3 說法一致。","ruling":"一致：財測達成且略超；Q4 EPS 超出主因稅率 18.4% 低於預期，營運面是符合不是加速。Q3 被問裁員節省是否落到損益時迴避，Q4 給的營業費用只略低於營收，等於節省大致再投資，與迴避的方向一致。另管理層 Q1 後停止揭露月度驅動數據，追蹤頻率由月降為季。Q3 稱六七月跨境電商異常偏高、會回到常態，Q4 仍 +17%、十月 +17%，管理層這一點偏保守。","evidence_level":"一手（法說逐字稿）","settle_metric":"FY2027 實際 EPS 成長對指引區間","if_then":["若 Q1 FY27 EPS 成長低於約 14%（指引中十位數低端） → 停止加碼，直到 Q2 數據出爐"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"估值與裁決（股價先走）","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-07-29，股價 366.59）：估值合理、評 A、進場。","side_b":"本次（股價 426.3，+16.3%）：前瞻本益比 28.4 倍、PEG 約 2.1、Base 年化約 7%～8%，估值改判偏貴、評降一級、不追價。","ruling":"同一家公司、相近的五年終點價值（本次 Base 終點約 597 美元；前份 Base 年化 10.7% 回推約 590～610 美元），報酬率下降幾乎全來自股價上漲；FY2026 實際 EPS 13.27 只比當時共識 13.19 高 0.6%。持股續抱，不在現價加碼。","evidence_level":"一手（價格與共識快照）","settle_metric":"股價對 FY2027E 前瞻本益比","if_then":["若股價回到 360 美元以下（前瞻本益比約 24 倍）且 Q1 FY27 淨營收成長 ≥10% → 分批反買，分三筆加回目標權重","若股價續漲到 470 美元以上而 FY2027E 共識未上修 → 不追，持股不加","反向條件：若 Q1 FY27 淨營收成長 ≥12% 且 EPS 成長 ≥16% → 分批反買，改在前瞻本益比約 27 倍（405 美元）以下承接"],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：擴大（↑）。","side_b":"本次：穩定（→）。","ruling":"Capital One 借記卡已轉自家 Discover 網路、信用卡進入測試，是領先玩家在大客戶份額下滑的有來源證據，前份未處理；Q4 客戶誘因 +21%（前季 +18%）、FY2027 續約 25% 支付量，誘因成長快於營收。定價差額與加值服務仍強，不到縮減，改判穩定。","evidence_level":"二手聚合站（Capital One）加一手法說（誘因）","settle_metric":"客戶誘因成長減淨營收成長；美國前十大發卡行網路選擇","if_then":["若 Capital One 宣布信用卡全面遷移或另一家美國前十大發卡行轉網路 → 減碼三分之一","若 FY2027 續約完成且客戶誘因成長回落到 18% 以下 → 方向回判擴大的條件之一成立，可分批反買"],"evidence_refs":["customer_second_source#0"]},{"axis":"機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 27%、Bear 27%，最大回撤單點 −50%。","side_b":"本次：Bull 25%、Base 45%、Bear 30%，最大回撤 −30%～−45%。","ruling":"Bear 提到 30%：三年共識 EPS 年複合 13.7% 超過內生上界 12%（差額可由淨回購解釋，但超出時 Bear 下限為 30%）；Bull 降到 25%：FY2027 EPS 指引低於指引前共識 +14%。回撤改用一年壓力路徑推導範圍（EPS 九折×倍數 18～22 倍），不再用單點。","evidence_level":"推導","settle_metric":"Q1 FY27 EPS 成長與共識方向","if_then":["若 FY2027E 共識 EPS 兩個季度內下修超過 5% → 不追，Bear 機率上調到 35% 重跑情境"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"加碼條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"已進場；加碼觸發＝回檔至 $340-350（W52 上緣）或 DOJ 事實證據開示結束無結構性不利發展","side_b":"加碼觸發＝股價 ≤360 美元（FY2027E 前瞻本益比約 24 倍，Base 年化回到 10% 以上）且 Q1 FY27 淨營收成長 ≥10%；或 Q1 FY27 淨營收 ≥12%、EPS ≥16% 時於 405 美元以下分批加碼","ruling":"錨點由技術位改為估值位：52 週均線已上移到 342.76，與估值錨 360 相近，但估值錨直接對應報酬率。DOJ 事實證據開示（前份記載預定 2026-10-16 結束）的結果事實表未涵蓋，無法判斷是否成立，改列 DOJ 觸發器單獨追蹤。","evidence_level":"推導","settle_metric":"股價對 360 美元；Q1 FY27 淨營收成長","if_then":["若股價 ≤360 美元且 Q1 FY27 淨營收成長 ≥10% → 分批反買"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（null）","side_b":"Single Thing：美國國會通過信用卡路由法案（CCCA），強制大型發卡行在信用卡加開第二個非 Visa／Mastercard 網路、由商戶選路由；任一院表決通過即減碼至半倉，簽署成法再減碼至四分之一。","ruling":"前份把監管風險分散在風險項而沒指出最大單一敏感度；美國信用卡是定價最高的流量，路由開放直接削去網路費定價空間，敏感度大於 DOJ 借記案（只涉借記）與單一發卡行流失。","evidence_level":"二手（產業與國會報導）","settle_metric":"CCCA 立法進度","if_then":["若 CCCA 任一院表決通過 → 減碼至半倉","若簽署成法 → 減碼至四分之一並重跑完整研究"],"evidence_refs":["end_markets#2"]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼門檻（null）","side_b":"本次減碼門檻：調整後淨營收成長連 2 季 <9%；加值服務成長連 2 季 <15%；服務收入成長減前季支付量成長連 2 季 ≤2pp；自由現金流率連 2 個財年 <40%；DOJ 救濟裁定；CCCA 任一院通過。","ruling":"前份只有漂移規則，沒有可執行的減碼與清倉數字，本次補上；門檻取自 FY2027 指引下緣與前份定價、加值服務兩條假設的削弱線。","evidence_level":"推導","settle_metric":"各季財報與立法、訴訟進度","if_then":["任兩項同時觸發 → 減碼至半倉","四項以上同時觸發 → 清倉"],"evidence_refs":[]},{"axis":"維持未變的判斷","cause":"新證據","prior_field":["trap","runway_post_y5","archetype","cycle_position"],"side_a":"前份：價值陷阱風險低、五年後跑道寬、品質複利成長型、非循環股不判循環位置。","side_b":"本次維持：Q4 加值服務 +31%、FY2027 指引 20% 出頭，衰退信號零亮；營收與 EPS 不隨大宗商品或產能循環。","ruling":"新證據支持原判，四欄不變。","evidence_level":"一手（法說）","settle_metric":"加值服務成長、衰退信號","if_then":["若加值服務成長連 2 季 <15% → 跑道改判中等並停止加碼"],"evidence_refs":[]},{"axis":"前份風險退場：營業費用快於營收","cause":"新證據","prior_field":["thesis.R1"],"side_a":"前份風險一：營業費用 +17% 快於淨營收 +14%，營益率可能是週期性。","side_b":"Q4 營業費用 +12% 低於淨營收 +13%；FY2027 指引營業費用低雙位數、略低於營收；Q4 非 GAAP 營益率 66.6%。","ruling":"Q3 的反向來自匯兌重估與遞延薪酬市價調整（EPS 中性）加上資遣，Q4 已回正，此風險退場；營益率門檻保留並併入定價假設（非 GAAP 營益率 ≥64%）。","evidence_level":"一手（法說）","settle_metric":"非 GAAP 營業費用成長對淨營收成長","if_then":["若 FY2027 任兩季營業費用成長高於淨營收成長 2pp 以上 → 停止加碼"],"evidence_refs":[]},{"axis":"共識修正口徑","cause":null,"prior_field":null,"side_a":"事實表 FY1 共識近三個月 +13.95%（13.19 到 15.03），看似大幅上修。","side_b":"13.19 是 FY2026 的共識（實際 13.27），15.03 是 FY2027；同年度兩份快照之間 FY1 0.0%、FY2 0.0%、FY3 −0.05%，指引前共識 FY2027 約 15.02。","ruling":"採 B 側：+13.95% 是財年換算，不是上修動能，不用它支持加碼。指引發布不到一季，賣方尚未消化（15.02 到 15.03），依此凍結加碼到 Q1 FY27 數據。","evidence_level":"一手快照對照","settle_metric":"FY2027E 共識 EPS 下一次快照","if_then":["若下一次快照 FY2027E 下修 ≥2% 而股價未跌 → 不追，等待價位維持 360 美元","若 FY2027E 上修 ≥3% → 分批反買價位上調到前瞻 25 倍"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭面：政府即時支付已在至少 80 國上線、穩定幣在 GENIUS 法案後取得制度基礎、Capital One 擁有 Discover 網路後遷出借記卡。","side_b":"結構面：FY2026 支付量 +9%、跨境 +13%、加值服務 +30%；Visa 在穩定幣結算（年化逾 250 億美元、年增 10 倍）與代理商務（近 50 家 AI 夥伴上線）都是參與者。","ruling":"雙向拉鋸，主要變動軸在其他結構變數中的監管與反壟斷（美國信用卡交換費和解、CCCA、DOJ 借記卡案、歐盟 IFR 再評估）；競爭面目前是點狀侵蝕，需求結構仍在變好。","evidence_level":"一手 10-K 加法說","settle_metric":"國際支付量成長、美國信用卡路由立法","if_then":["若國際支付量（固定匯率）成長連 2 季 <5% → 減碼三分之一"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#1","customer_second_source#0","supply_demand_durability#0"]},{"axis":"⚖ 現在就買或等價格","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：FY2026 營收 +15%、EPS +16%；FY2027 定價集中下半年、十月跨境 +15%、美國支付量 +10%；若 EPS 再超出到 +15%，前瞻本益比只有約 27.9 倍，等 360 美元可能等不到（前份等 340～350 美元，結果漲了 16%）。","side_b":"等價格：Base 年化 7%～8%，共識 15.03 已在指引上緣，Q2 是全年成長低點且續約誘因加大，賣方目標價均值低於現價；好生意不缺，缺的是價格。","ruling":"選等價格，屬程度差異、可調和：持股不動、新資金不追。綁定約束只有一條，就是價格（Base 年化低於 8%）；解除條件是股價回到 360 美元以下，或 Q1 FY27 證明指引保守。","evidence_level":"一手法說加價格","settle_metric":"Q1 FY27（2027-01 下旬）淨營收與 EPS 成長；股價對 360 美元","if_then":["若 Q1 FY27 淨營收成長 ≥12% 且 EPS ≥16% → 分批反買，在 405 美元以下承接","若股價 ≤360 美元且 Q1 FY27 淨營收成長 ≥10% → 分批反買","反向：若 Q1 FY27 淨營收成長 <10% 且股價仍在 400 美元以上 → 停止加碼，等待價位下修到 340 美元"],"evidence_refs":["capital_markets_pricing#0"]}],"triggers":[{"n":1,"text":"Q1 FY27 調整後淨營收成長達指引（低雙位數）","type":"假設驗證","maps_to":"H2","metric":"調整後固定匯率淨營收成長（季）","threshold":"≥10%","action":"未達：停止加碼；連 2 季 <9%：減碼三分之一","source_freq":"季報新聞稿與法說，每季","date":"2027-01","evidence_refs":["capital_markets_pricing#0"]},{"n":2,"text":"加值服務成長維持 20% 上下","type":"假設驗證","maps_to":"H3","metric":"加值服務營收成長（固定匯率）","threshold":"≥18%；連 2 季 <15% 為削弱","action":"連 2 季 <15%：停止加碼並把跑道改判中等","source_freq":"每季法說","date":"2027-01"},{"n":3,"text":"支付量與處理筆數維持結構性成長","type":"假設驗證","maps_to":"H1","metric":"固定匯率支付量成長、處理筆數成長","threshold":"支付量 ≥7%、筆數 ≥8%","action":"支付量連 4 季 <7%：停止加碼；連 6 季 <5%：減碼三分之一","source_freq":"每季（月度數據 Q1 後停止）","date":"2027-01"},{"n":4,"text":"續約高峰年誘因失控","type":"風險","maps_to":"R1","metric":"客戶誘因成長減淨營收成長","threshold":"差距 >12pp 連 2 季（Q4 為 21% 對 13%，差 8pp）","action":"減碼三分之一","source_freq":"每季","date":"2027-04","evidence_refs":["capital_markets_pricing#0"]},{"n":5,"text":"DOJ 借記卡案出現救濟裁定","type":"風險","maps_to":"R2","metric":"DOJ 借記卡壟斷案程序（簡易判決、審判、救濟）","threshold":"法院裁定限制誘因或路由合約，或結構性救濟","action":"行為救濟：減碼三分之一；結構性救濟：減碼至半倉","source_freq":"法院文件與產業媒體，事件驅動","date":"2027-04","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#3","major_events#2"]},{"n":6,"text":"美國信用卡路由法案（CCCA）進入院會表決","type":"Single Thing","maps_to":"Single Thing","metric":"CCCA 立法進度","threshold":"任一院表決通過","action":"減碼至半倉；簽署成法減碼至四分之一","source_freq":"國會紀錄，事件驅動","date":null,"evidence_refs":["end_markets#2"]},{"n":7,"text":"大型發卡行轉網路擴散","type":"風險","maps_to":"R5","metric":"Capital One 信用卡遷移規模；美國前十大發卡行網路選擇","threshold":"Capital One 宣布信用卡全面遷移，或另一家前十大發卡行宣布轉網路","action":"減碼三分之一","source_freq":"發卡行公告，事件驅動","date":null,"evidence_refs":["customer_second_source#0"]},{"n":8,"text":"交換費監管外溢到網路費","type":"風險","maps_to":"R3","metric":"歐盟 IFR 影響評估結論；美國交換費和解終局核准內容","threshold":"提案降低 20／30bp 上限或把網路費納入管制","action":"停止加碼；網路費被設上限即減碼三分之一","source_freq":"歐盟執委會與法院公告，事件驅動","date":null,"evidence_refs":["regulatory_antitrust#0","end_markets#2","major_events#3"]},{"n":9,"text":"替代軌道侵蝕國際量","type":"風險","maps_to":"R4","metric":"國際支付量成長（固定匯率）","threshold":"連 2 季 <5%（Q4 為 +9%）","action":"減碼三分之一","source_freq":"每季","date":"2027-01","evidence_refs":["competitive_share_entrants#1","substitute_technology#1","substitute_technology#0"]},{"n":10,"text":"跨境旅遊與總經衝擊","type":"風險","maps_to":"R6","metric":"跨境量（不含歐洲內部）成長","threshold":"連 2 季 <8%（Q4 為 +14%）","action":"停止加碼","source_freq":"每季","date":"2027-01","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":11,"text":"價格回到估值錨","type":"估值rearm","maps_to":"H2","metric":"股價與 FY2027E 前瞻本益比","threshold":"≤360 美元（約 24 倍），且 Q1 FY27 淨營收成長 ≥10%","action":"分三筆加碼回目標權重","source_freq":"每日收盤","date":null},{"n":12,"text":"指引被證明保守","type":"加碼","maps_to":"H2","metric":"Q1 FY27 調整後淨營收與 EPS 成長","threshold":"淨營收 ≥12% 且 EPS ≥16%","action":"在 405 美元以下分批加碼","source_freq":"Q1 FY27 法說","date":"2027-01"},{"n":13,"text":"估值超過 Bull 終端倍數","type":"減碼","maps_to":"價格已反映太多","metric":"FY2027E 前瞻本益比","threshold":"≥33 倍（約 496 美元）且共識未上修","action":"減碼五分之一","source_freq":"每日收盤","date":null},{"n":14,"text":"自由現金流轉換持續惡化","type":"減碼","maps_to":"論點成功但股東經濟變差","metric":"自由現金流÷淨營收","threshold":"連 2 個財年 <40%（FY2026 約 48%）","action":"減碼三分之一","source_freq":"年報","date":"2027-11"},{"n":15,"text":"Q1 FY27 財報複審","type":"複審日期","maps_to":"H1/H2/H3","metric":"全套假設與情境","threshold":"—","action":"依上列觸發器執行並更新情境機率","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"調整後固定匯率淨營收成長（季）","bear_threshold":"連 2 季 <9%","window":"FY2027 Q1～Q4","source":"Visa 季報新聞稿與法說","last_status":"ok"},{"metric":"加值服務營收成長（固定匯率）","bear_threshold":"連 2 季 <15%","window":"FY2027～FY2028","source":"Visa 法說","last_status":"ok"},{"metric":"服務收入成長減前季固定匯率支付量成長","bear_threshold":"連 2 季 ≤2pp","window":"FY2027","source":"Visa 法說","last_status":"ok"},{"metric":"自由現金流÷淨營收","bear_threshold":"連 2 個財年 <40%","window":"FY2027～FY2028","source":"Visa 年報現金流量表","last_status":"warning"},{"metric":"DOJ 借記卡案救濟","bear_threshold":"法院裁定行為或結構性救濟","window":"2027～2028","source":"法院文件、產業媒體","last_status":"unknown"},{"metric":"CCCA 信用卡路由法案","bear_threshold":"任一院表決通過","window":"2026-11～2028-12","source":"美國國會紀錄","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#0","reason":"證據是 2018 年單一資料中心交換器故障，早於現行網路架構；逐字稿記載新一代雲原生 VisaNet 已在拉美與中東歐非洲承載即時授權流量，五年投入 150 億美元於網路安全與韌性。此證據的年代與架構都無法代表現行單點失效風險，本包也未收錄 2018 年後同級事件。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=30.95, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 路徑只有「定價與加值服務維持 20% 以上」的敘事，沒有量乘價的算術；五年後的成長跑道又缺滲透率推導，指引的來源也只有未核對的二手整理，所以這條 Bull 依據目前站不住。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價 ≤360 美元（FY2027E 前瞻本益比約 24 倍）且 Q1 FY27 淨營收成長 ≥10%；或 Q1 FY27 淨營收 ≥12%、EPS ≥16% 時於 405 美元以下分批","exec_line":"持股續抱不加碼；新資金等價或等數據，分三筆執行，單筆不超過目標權重三分之一"},"reasoning":{"industry":"FY2026 淨營收約 459 億美元、年增 15%，管理層稱是排除疫後與併購後 15 年來最快；Q4 淨營收 121.39 億美元、年增 13%。收入分四塊：服務收入 +14%（對照前季支付量 +10%，差額歸因定價）、資料處理 +16%（對照處理筆數 +10%）、國際交易 +8%（落後跨境量 +14%，因匯率波動度低於去年）、其他收入 +40%（諮詢與行銷服務）；客戶誘因 +21% 是營收減項。CMS 全年 +19%、加值服務 +30% 至 140 億美元，兩者合計逾淨營收四成（2026-10-27 法說，CEO）。單位經濟：TTM 毛利率 79.75%、營益率 65.57%，資本支出 16.71 億美元約占營收 3.6%，多一筆交易的邊際成本接近零。Q4 GAAP 營益率 59.8%、非 GAAP 66.6%，差額是訴訟準備與資遣等項目。單點依賴：最大客戶 FY2022 占淨營收 10%（之後年度事實表未涵蓋），FY2027 約 25% 支付量到期續約（FY2026 為 20%），議價力集中在大型發卡行。產業在擴張期：支付量 +9%、處理筆數 +9%、跨境 +13%，無產能過剩或價格戰。供需判讀為結構性持久：需求來自現金與支票數位化、企業支付與帳戶間轉帳等新流量；週期性部分集中在跨境旅遊與匯率波動度。","moat":"機制：52 億張憑證（+6%）對上逾 2 億個受理點（加上錢包逾 4 億），全球處理滲透約 80%，新進者得同時說服發卡行與商戶兩邊。方向證據三條：①定價：Q4 服務收入 +14% 對前季支付量 +10%、資料處理 +16% 對處理筆數 +10%，CFO 稱 FY2027 定價貢獻與 FY2026 同量級；②同業差距：營益率 65.57% 對 Mastercard 60.07%（+5.5pp）、自由現金流率 44.91% 對 42.52%，只有 TTM 單一時點，方向無法驗證；③大客戶份額：Capital One 借記卡已轉自家 Discover 網路、信用卡測試中，屬有來源的大客戶份額下滑，方向不得判擴大。執行面 9 分：加值服務 +30%、CMS +19%、逾半數憑證已代幣化、Tap to Pay 占全球面對面交易近 85%。定價面 9 分：監管鎖的是交換費，網路費仍每年調整；續約誘因 +21% 吃掉一部分。三條威脅都屬點狀，Visa 在每一條都同時是參與者（A2A Protect、Visa Direct、穩定幣結算年化逾 250 億美元）。報酬持續期：高利益率×高周轉（投入資本事實表未涵蓋，以資本支出占營收 3.6% 推斷周轉率高），四檢查點一綠三黃。再投資：高報酬、低再投資，內生上界約 12%，多餘現金以回購與股利返還。","growth":"成長組成（Q4 淨營收 +13%）：量約 9～10pp（支付量 +9%、處理筆數 +10%）、價約 3～4pp（服務收入 +14% 對支付量 +10%）、Prisma 併購約 1pp，匯率波動度為拖累；每股盈餘另加淨回購約 1.7pp。三年共識 EPS：FY2026 實際 13.27（法說，CFO）到 FY2029E 19.51，年複合 13.7%（Koyfin 快照 2026-10-31）；FY2027E 15.03 落在公司 EPS 指引低雙位數到低十位數的上緣。缺口＝13.7% − 內生上界 12% ≈ 1.7pp，歸因淨回購：FY2027 可回購約 136 億美元（自由現金流 220.57 億 − 調升後股利約 60 億 − BioCatch 24 億），約市值 7,966 億的 1.7%。跑道：電子支付滲透率事實表未涵蓋，論點不靠滲透率；第二曲線有來源，加值服務約為 2023 年的兩倍，發卡、受理、風險安全三組合 FY2026 合計 +20% 以上且管理層稱 FY2027 可延續；Visa Direct 端點 180 億（前年 120 億）。衰退信號十項零項亮燈，兩項列觀察：核心市占（Capital One 借記卡流失，但無 Visa 單獨份額數字）與自由現金流率（FY2022 61% 到 FY2026 約 48%，不在十項清單內，記入反證）。","governance":"FY2026 營業現金流 237.28 億、資本支出 16.71 億、自由現金流 220.57 億美元。Q3 回購 49 億、Q4 回購 40 億並發股利 13 億，另撥 4.05 億入訴訟託管帳戶（CFO 稱效果等同回購，由 B 類股轉換率下調吸收）；9 月底剩餘回購授權 244 億，季股利調升 16%。現金轉換：FY2025 自由現金流÷淨利＝21,577÷20,058＝1.08；但自由現金流率由 FY2022 61% 降到 FY2026 約 48%（22,057÷約 45,900），同期營益率持平在 66% 上下，落差原因事實表未涵蓋（可能涉及誘因預付、訴訟支付與稅），列為反證觀察。併購：Prisma 與 Newpay（阿根廷）已併入，Q4 貢獻淨營收約 1pp、EPS 約 0.5pp；BioCatch 24 億美元現金待監管核准，預計 FY2027 第二季底前完成。三項計分：併購已實現增量報酬缺收購價與利潤數字，無法判；回購買入收益率＝前瞻本益比 28.36 的倒數 3.5%，公債殖利率事實表未涵蓋，殖利率只要高於 1.5% 即不過；SBC 約市值 0.12%，淨股數因回購下降，通過。近三年現金去向四分、債務到期與利率事實表未涵蓋；淨負債 79.88 億美元，FY2027 營業外費用升至 2.5～3 億美元，因現金餘額下降。","valuation":"倍數：前瞻本益比 28.36 倍（FY2027E 15.03）、非 GAAP 落後本益比 32.1 倍（426.3 ÷ FY2026 實際 13.27）、GAAP 落後 34.6 倍（四個年度端點最高，但分母含資遣等一次性費用）；P/S 17.36 倍、EV/S 17.53 倍在四個年度端點中位附近。PEG＝28.36 ÷ 三年共識年複合 13.7% ≈ 2.1。反推：10% 年報酬需五年後股價約 670 美元，本益比守在 32 倍需 FY2031 EPS 約 20.9（年增 9.6%），回到 26 倍需約 25.8（年增 14.2%）。Base 假設 EPS 年增 11.6%、終端 26 倍，五年後約 597 美元。成長熄火壓力測試（FY2029 前照共識 19.51，之後兩年年增 15%／10%／5%，本益比 28／23／18 倍）：五年後約 722／543／387 美元，三種裡兩種不低於現價。共識：同年度 FY1、FY2 修正 0.0%、FY3 −0.05%；FY1 近三個月 +13.95% 是財年換算（13.19 屬 FY2026、15.03 屬 FY2027），不是上修。指引前共識 FY2027 約 15.02、指引後 15.03，賣方尚未把指引放進模型，共識坐在指引上緣。財報前賣方目標價均值約 406～417 美元，低於現價。價格：三個月 +16.3%（366.59 到 426.3）、26 週 +30.95%，高於 52 週均線 24%；RSI 資料標示不可用，不引用。結論：生意沒變差，倍數已先把好消息算進去。","premortem":"向上看錯：FY2026 淨營收 +15%、EPS +16%；FY2027 定價集中在下半年、十月跨境量 +15%，若 EPS 落在 +15%（約 15.26），現價對應前瞻本益比約 27.9 倍，等不到 360 美元。向下看錯：①CCCA 通過，最賺錢的美國信用卡流量改由商戶選路由，定價貢獻被削去；②DOJ 借記卡案若裁定限制誘因與路由合約，美國借記定價受壓；③續約高峰（25% 支付量）若以更高誘因換來，淨營收低於指引。Q4 EPS 3.48 勝共識 3.43 主要來自較低稅率（18.4%，訴訟和解的稅務利益），營運面只是符合預期，不應解讀為加速。價值陷阱風險低：十項衰退信號零項亮燈；最大回撤推導見情境樹。"},"plain":{"six":{"how_it_makes_money":"賺全球電子支付的網路過路費：發卡行按支付量付服務費、按筆數付處理費，跨境交易另收國際交易費，加值服務已占淨營收約三成；錢卡在授權與清算這一節點，Q4 非 GAAP 營益率 66.6%。","moat":"護城河穩定（→），評 A：雙邊網路與信任層沒有被繞過的證據，定價每年仍貢獻 3～4 個百分點；Capital One 轉網路、續約誘因加速與政府即時支付，讓方向由前份的擴大改為穩定。","growth":"成長跑道寬（🟢）：加值服務（140 億美元、+30%，FY2027 指引 20% 出頭）與 CMS（+19%）是已實現的第二曲線；三年共識 EPS 年複合 13.7%，超出內生上界 12% 的約 1.7pp 由淨回購解釋，不靠倍數擴張。","capital":"資本配置穩健但不出色：FY2026 自由現金流 220.57 億美元大半以回購與股利返還，SBC 只占 GAAP 營業利益 3.3%；扣分在回購買入收益率僅約 3.5%（高價回購）與併購報酬無法驗證，自由現金流率四年由 61% 降到約 48% 需要追。","valuation":"偏貴：現價 426.3 美元要換 10% 年報酬，得靠本益比守住 32 倍（非 GAAP 落後口徑）或 EPS 五年年增約 14%；EPS 年增 11%～12% 我信，倍數不降我不信，Base 年化約 7%～8%。","how_wrong":"最可能看錯的方向是太保守：Visa 連續兩年交出高於初始節奏的成長，若 FY2027 再超出，等價會錯過；向下的錯在監管，美國信用卡路由立法或 DOJ 借記卡案的救濟。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 360 美元以下（FY2027E 前瞻本益比約 24 倍、Base 年化 10% 以上）且 Q1 FY27 淨營收成長 ≥10%；或 Q1 FY27 淨營收 ≥12%、EPS ≥16%，證明指引保守","qc48_result":"fail","qc48_note":"Bull 路徑只有「定價與加值服務維持 20% 以上」的敘事，沒有量乘價的算術；五年後的成長跑道又缺滲透率推導，指引的來源也只有未核對的二手整理，所以這條 Bull 依據目前站不住。","trap":"🟢","val":"🟠","moat":"A","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":426.3,"week26_return_pct":30.95,"consensus_rev_3m_pct":13.95,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"GAAP 落後 EPS（約 12.32＝426.3÷34.6）含資遣 5.63 億等一次性費用，已改用非 GAAP 實際 13.27 與 FY2027E 前瞻 15.03 錨定；這兩個分母沒有爭議。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q1 FY27 財報：檢驗指引是否保守、續約誘因與定價下半年節奏","impact":"高","watch":"淨營收 ≥10% 或 ≥12%、EPS ≥16%、客戶誘因成長"},{"date":"2027-03","date_precision":"month","type":"regulatory","event":"BioCatch 24 億美元收購最遲 FY2027 第二季底完成，屆時公布財務影響","impact":"低","watch":"對 FY2027 EPS 的稀釋幅度"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"DOJ 借記卡案專家證據開示期限（前份記載 2027-04-08）","impact":"中","watch":"審判日程與是否進入和解"},{"date":"2027-04","date_precision":"quarter","type":"other","event":"FY2027 新定價多數在下半年生效","impact":"中","watch":"服務收入成長減支付量成長"}],"_projected_from":"v19"}
```
