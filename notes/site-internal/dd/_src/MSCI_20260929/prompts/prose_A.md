你是 stock-analyst v20 的**散文層（prose）agent**，標的 MSCI（2026-09-29）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20260929/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MSCI　日期：2026-09-29　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1440B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（422B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（896B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1307B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1268B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（959B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1037B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1985B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4031B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3610B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1440           3892-5560      5 條（2–6 內）  
s3                  8000         422           5305-7578      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3471          8070-11529      5 條（2–6 內）  
s6                 11000         959          7029-10041      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1037           1724-2463      5 條（2–6 內）  
s10                 5000        1985           2110-3015      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3610           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5113B；至少需散文≈39.89KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45
−25
0%
0
0.08%
0.1
0.2
0.25%
0.3
0.35
01
1
1.3
1.47
1.5%
1.60
1.70
1.76
1.90
2%
2.0
2
02
2.7%
2.77
2.8%
2.8
2.9%
3
3.26
3.3
3.5%
3.7
4
04
4.4%
4.64
4.9%
5
5%
6%
6
6.11
6.6%
7%
07
7
7.8%
7.8
8%
8
8.1%
8.3%
8.67
9
09
9%
9.48
9.6
10%
10
10.3%
10.8%
11%
11
11.1%
11.4
11.8
11.84
12
12%
13
13.40
13.7
13.70
13.7%
14
14.1
14.85
15
15%
15.35
15.45
15.75
16%
17
17.4%
17.6
17.6%
18
18.7%
18.7
19%
19.4
19.74
20%
20
20.2
20.5
21
21.3
22%
22.3
22.5
23
23%
23.2
24
24.1
24.12
24.8%
25
25%
25.54
26
26.1
26.4
26.6%
27
27.4
27.49
27.5
28.35
29
29.6
29.6%
30%
30
30.8
31.19
34.31
35
39.5
41
41.2
41.6%
42
44.8%
45
45%
46.1%
49
52
55.7%
56.2%
58%
59%
60%
61%
62.1%
70
70.9%
75.0%
80
83.0%
90
93.5%
94.4%
94.5%
95.3%
96%
96.5%
97%
100%
100
104
150%
200
250
400
420
474
517.85
542.72
558
564.28
565.73
570
585
638
639
692
700
722
742
746
760
2024
2025
2026
2027
20260929
1,000
4,500
7,470
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
{"meta":{"ticker":"MSCI","date":"2026-09-29","schema":"v15.2","contract":"v19","company_name":"MSCI Inc."},"oneliner":"全球投資的記分板：MSCI 靠指數標準收使用費，留存 95.3%、ABF run rate 年增 25%；但大型 ETF 客戶壓費率、費用指引連升，FY1 本益比 27.5 倍、PEG 約 2，好生意、價格合理不便宜。","thesis":{"H":[{"id":"H1","text":"指數標準持續擴張：Index 有機訂閱 run rate 年增維持 9% 以上，Index 留存率維持 96% 以上","2y":null,"5y":"FY2031 前 Index 訂閱 run rate 年增平均不低於 9%","10y":null,"threshold":"年增 9% 以上（現 11.1%）；留存 96% 以上（現逾 97%）","source":"每季財報新聞稿 Index 段 run rate 與留存率","drift_rule":"連 4 季低於 9% 削弱；連 6 季低於 8% 反轉"},{"id":"H2","text":"按資產計費的規模成長勝過費率拖累：ABF run rate 年增率不落後期末掛鉤 ETF AUM 年增率超過 10 個百分點","2y":"FY2028 前每季費率拖累不超過 10 個百分點","5y":null,"10y":null,"threshold":"拖累 10 個百分點以內","source":"每季財報的 ABF run rate、期末掛鉤 ETF AUM、平均基點","drift_rule":"連 2 季拖累超過 10 個百分點削弱；連 3 季超過 15 個百分點反轉"},{"id":"H3","text":"新成長曲線接棒：全公司有機訂閱 run rate 年增升到 9% 以上（現 8.1%），留存率守住 94.5%","2y":"FY2028 前全公司有機訂閱 run rate 達 9%","5y":null,"10y":null,"threshold":"低於 8% 連 2 季，或留存低於 94.5%","source":"每季財報新聞稿全公司訂閱 run rate 與留存率；法說的對沖基金、PCS、客製指數成長率","drift_rule":"連 2 季低於 8% 削弱；連 3 季低於 7% 反轉"}],"R":[{"id":"R1","text":"最大客戶 BlackRock 議價：占營收 10.8%、占 Index 段 18.7% 且逐年升，續約可再壓費率下限，或把產品移到自編指數","h_ref":"H2","clock":"🐢","threshold":"BlackRock 占營收超過 12% 且平均基點年降超過 10%","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R2","text":"ABF 對股市位階的曝險：掛鉤 ETF 資產在歷史高點，股市修正或新興市場地緣事件（台灣占 EM 指數 24.8%）會同時壓資產規模與費率組合","h_ref":"H2","clock":"⚡","threshold":"季末掛鉤 ETF AUM 季減超過 15%","evidence_refs":["geo_supply_chain#0"]},{"id":"R3","text":"主動 ETF 分流：主動 ETF 檔數已超過被動、三年資產年化 59%，資金若轉向不掛鉤指數的產品，ABF 流入動能變慢","h_ref":"H2","clock":"🐢","threshold":"掛鉤 ETF 單季現金流入連 2 季低於 200 億美元","evidence_refs":["end_markets#4"]},{"id":"R4","text":"費用跑贏營收：FY2026 營運費用財測已上修到 15.35–15.75 億美元，Q3 另有遣散費，管理層明說 AI 省下的錢要再投資","h_ref":"H1","clock":"🔥","threshold":"調整後 EBITDA 利潤率連 2 季年減超過 1 個百分點（Q2 62.1%）","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"id":"R5","text":"永續段縮水與替代：AI 能低成本複製部分 ESG 評等，歐盟新規自 2026-07-02 起要求取得 ESMA 授權，美洲客戶持續砍預算","h_ref":"H3","clock":"🔥","threshold":"S&C 段淨新增經常性銷售連 3 季為負","evidence_refs":["substitute_technology#0","regulatory_antitrust#1"]}],"single_thing":{"description":"BlackRock 把大型 iShares MSCI 產品改掛其他指數商或自編指數，或下次續約把費率砍到明顯低於現行下限","why_fatal":"BlackRock 占 Index 段營收 18.7%、占全公司 10.8%，幾乎全是按資產計費，營收少掉這塊幾乎全是利潤，EPS 下修可近兩成（推估）。更要命的是它會打破基準一旦用了就不換的前提，其他 ETF 發行商會跟著議價，倍數跟著重估。股市修正對 ABF 的衝擊金額更大，但會回來；客戶換指數不會","if_happens":"清倉並重跑研究；本益比朝 18 倍靠","how_monitor":"iShares 產品標的指數變更公告、每年 10-K 的最大客戶占比、每季平均基點對照掛鉤 ETF 資產","probability":"約 5%（12–24 個月）；2025 年底剛續約並調整過下限，近期再換的誘因低"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟡","long_term_confidence":"高","fpe_fy2":24.12,"peg_fy2":1.76,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":19.74,"FY2027E":22.5,"FY2028E":25.54},"fy_end_month":12,"eps_basis":"Koyfin 共識 EPS（2026-09-26 快照），事實表未標 GAAP 或調整後；FY2025A 實際值事實表未涵蓋，三年年化改以 FY2026E 到 FY2028E 兩年 13.7% 代替"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20260929/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"標準制定者按資產收費加高留存訂閱，輕資產、高利潤率"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：留存率由 94.4% 升到 95.3%（Q2 新聞稿），Q1 掛鉤 ETF 流入逾千億美元、基準資產逾 21 兆美元；ABF 部分屬週期性，隨股市位階波動","bargaining":{"up":"供應端是資料來源與人才，事實表未涵蓋供應商集中度，未見單一供應商依賴","down":"最大客戶 BlackRock 占營收 10.8%、占 Index 段 18.7% 且上升；2025 年底續約時部分產品費率下限調低，財務長稱調整約 0.1 基點（2026-09-14 巴克萊會議）","geo":"台灣占 MSCI 新興市場指數 24.8%（2026-04-30），新興市場產品費率較高，地緣事件會同時打到資產規模與費率組合"},"profit_pool_dir":"利潤池往指數商與超大型 ETF 發行商兩端集中；傳統主動管理人是預算壓力最集中處（2026-09-14 巴克萊會議財務長原話）","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與被動化滲透率；跑道判斷改以管理層揭露的第二曲線成長率為據，未展開屬資料缺口，不是不重要"}},"moat":{"mechanism":"指數基準的網絡效應：資產主選基準，管理人、ETF 與交易生態被迫跟隨，流動性集中讓替換成本逐年升高","execution":9,"pricing":8,"grade":"A","trend":"→","trend_evidence":"執行面擴大：留存率 94.4% 升到 95.3%，Index 訂閱 run rate 加速到 11.1%；定價面縮減：BlackRock 續約調低費率下限，平均基點連兩季下滑；兩者抵銷為持平","peer_na_reason":"同業 ROIC 事實表未涵蓋，以營益率差距與留存率代替；差距只有單期，趨勢無法判","threats":[{"level":"🟡","text":"AI 低成本複製部分 ESG 評等，永續評等的定價溢價被侵蝕；影響限於 S&C 段","p":0.35,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"主動 ETF 檔數已超過被動，資金若改流向不掛鉤指數的產品，ABF 流入動能放慢；公司已推主動型產品授權回應","p":0.3,"evidence_refs":["end_markets#4"]},{"level":"🟡","text":"最大客戶 BlackRock 要求降費或停用 MSCI 指數，公司風險因子已自承","p":0.2,"evidence_refs":["customer_concentration_credit#1"]},{"level":"🟡","text":"自助式指數設計平台（S&P SPICE、Merqube）降低客製指數門檻；公司 2024 年已收購 Foxberry 平台因應","p":0.3,"evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是投資組合經理與交易員，決策者是資產主董事會與投資顧問，付款者是資產管理公司與 ETF 發行商，三個角色都成立；基準寫進投資契約與法遵要求，是需要不是想要。讀數：留存率 95.3%（去年同期 94.4%），基準資產逾 21 兆美元，Q1 掛鉤 ETF 流入逾千億美元"},{"item":"決策層級","level":"🟢","text":"替代要在資產主選基準這一層決定，換基準牽涉投資政策修訂、績效紀錄銜接與指數基金換倉成本，不是採購部門比價。讀數：Index 留存逾 97%，對沖基金客群同樣逾 97%，調價對新增經常性銷售的貢獻穩定（Q2 法說財務長）"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈是終端投資人到 ETF 發行商再到指數商；ETF 費率戰把壓力往上游推，買方高度集中（BlackRock 占 Index 段 18.7% 且上升），2025 年底續約取得部分產品較低費率下限，平均基點連兩季下滑。長期需求還在，但超大型 ETF 的分成在往發行商那邊移，發行商自編指數是潛在替代"},{"item":"社會容忍度","level":"🟡","text":"指數商的影響力受歐美監管與媒體關注（10-K 風險揭露），MSCI Limited 屬英國 FCA 授權基準管理機構；歐盟 ESG 評等規範自 2026-07-02 起要求取得 ESMA 授權。查無反壟斷調查報導。美國政治對 ESG 的反彈與監管對指數集中度的關注，會限制永續產品與大幅漲價的空間"}],"roiic":"事實表未涵蓋（投入資本、商譽與收購金額未入表）","reinvest_rate":"低：資本支出財測 1.60–1.70 億美元，約為自由現金流財測 14.85–15.45 億美元的一成；收購屬小型補強，金額事實表未涵蓋","endo_ceiling":10,"formula_note":"資本公式（增量 ROIC 乘再投資率）算不出來：投入資本、商譽與收購金額事實表未涵蓋。實體再投資率低，成長靠費用化的產品開發與銷售，公式會低估。改用有機代理：訂閱 run rate 約 8%（全公司 8.1%）與 ABF 長期約 9%（股市上漲加資金流、扣費率拖累，屬判斷值）混合，營收約 9%，加少量營業槓桿，EPS 有機上界取 10%，不含淨回購。當期稅後營業利益率約 45%（TTM 營益率 55.7% 扣 Q2 指引稅率 18–20%），周轉率因投入資本缺值無法計算"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","MSCI":82.97,"SPGI":70.9,"MCO":74.98,"FDS":51.38,"unit":"%"},{"metric":"營業利益率","MSCI":55.66,"SPGI":41.56,"MCO":46.1,"FDS":29.55,"unit":"%"},{"metric":"FCF 利潤率","MSCI":44.77,"SPGI":34.57,"MCO":36.36,"FDS":29.05,"unit":"%"},{"metric":"研發密度","MSCI":5.45,"SPGI":null,"MCO":null,"FDS":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"SPGI","gm":70.9,"om":41.56,"fcf_margin":34.57,"rd_intensity":null,"strategy_note":"S&P DJI 是指數業最直接的對手，美國大型股基準強；毛利率 70.9%、營益率 41.6%，低於 MSCI，反映評等與資料業務混合；SPICE 自助平台在客製指數正面競爭","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MCO","gm":74.98,"om":46.1,"fcf_margin":36.36,"rd_intensity":null,"strategy_note":"主業是信評與風險分析，和 MSCI 在氣候、ESG 資料與風險分析有交集，指數業務不重疊；營益率 46.1%，是表中利潤率最接近 MSCI 的同業","period":"TTM ending 2026-06-30（4季加總）"},{"name":"FDS","gm":51.38,"om":29.55,"fcf_margin":29.05,"rd_intensity":null,"strategy_note":"和 MSCI Analytics 在投資組合分析與因子模型搶同一批資產管理客戶；營益率 29.6%，工作站軟體的成本結構明顯較重","period":"TTM ending 2026-05-31（4季加總）"}]},"growth":{"driver_mix":"量為主（ABF 隨掛鉤資產規模、訂閱新客與新模組），價為輔（調價貢獻穩定），小型併購，淨回購每年約 2%","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"有機代理：訂閱 run rate 約 8% 加 ABF 長期約 9% 混合，營收約 9%，利潤率大致持平再加少量營業槓桿，EPS 有機約 10%；資本公式因投入資本與收購金額事實表未涵蓋無法計算","segments":[{"item":"Index","value":"上半年營收年增 17.6%：ABF 年增 26.6%、訂閱年增 10.3%；有機訂閱 run rate 年增 11.1%，ABF run rate 約 9.48 億美元、年增 25%；掛鉤 ETF 資產逾 2.8 兆美元"},{"item":"Analytics","value":"Q1 營收 1.90 億美元、年增 10.3%（含一次性導入收入）；Q2 有機營收年增約 7%，有機訂閱 run rate 年增 6.6%"},{"item":"Sustainability and Climate","value":"氣候 run rate 年增近 12%；永續段美洲取消多，管理層預期未來兩季淨新增約零到小負；First Street 完成後約增 1,000 萬美元訂閱 run rate"},{"item":"All Other–Private Assets","value":"Q2 營收 7,470 萬美元、年增 4.9%（有機 4.4%），有機訂閱 run rate 年增 8.3%；其中 PCS 訂閱 run rate 加速到 16% 以上"},{"item":"分段占比","value":"各段占營收比重事實表未涵蓋"}],"decay_signals":[{"signal":"產業估值倍數近 3 年系統性下移","lit":true,"evidence":"本益比、市銷率、EV/S 都在近四個年度端點最低；同業倍數事實表未涵蓋，以自身代理"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"evidence":"限於永續段：美洲客戶砍預算、AI 可複製部分 ESG 評等；氣候與指數未見"},{"signal":"EPS CAGR 顯著高於 Rev CAGR","lit":false,"evidence":"營收共識事實表未涵蓋，無法判；Q2 調整後 EPS 年增近 19% 對有機營收逾 12%，單季不構成"},{"signal":"SBC/Rev 超過 5% 且逐年上升","lit":false,"evidence":"Q2 推算約 2.9%"},{"signal":"maintenance capex 占 FCF 超過 60%","lit":false,"evidence":"資本支出財測約為 FCF 財測的一成"},{"signal":"毛利率連 2 季 YoY 下滑","lit":false,"evidence":"季度毛利率序列事實表未涵蓋，未能驗證"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"掛鉤 ETF 資金流創新高，財務長稱在新流入資產的市占位置獨特"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自有機訂閱與按資產計費；Vantager、Compass、PM Insights 對 run rate 貢獻有限，First Street 約增 1,000 萬美元訂閱 run rate，不靠併購撐成長"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"收購金額與實現回報事實表未涵蓋；Burgiss 收購後約兩年半才換好團隊，私募資產段 Q2 有機營收只增 4.4%，Fabric 去年沖回或有對價，現有證據偏負，判不過","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購均價約 558 美元對 FY2026E EPS 19.74，買入收益率約 3.5%；要 10 年期殖利率低於 1.5% 才過（10 年期殖利率事實表未涵蓋），判不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 約占營收 2.9%，除以市銷率 11.84 約占市值 0.25%，加上持續回購，淨稀釋遠低於每年 1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比與 PEG（品質複利型優先用這兩把尺）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，未收同業前瞻本益比；終端倍數改以自身年度端點與成長熄火情境錨定，屬資料缺口"},"fwd_pe":27.49,"peg":2.0,"percentile_5y":0,"val_light":"🟡","val_light_derivation":"FY1 本益比 27.5 倍、PEG 約 2.0，位於合理區上緣；倍數在近四個年度端點最低（分位 0，非真五年序列）；成長可信但倍數沒有擴張空間，判黃","upside_short_pct":7.8,"upside_mid_pct":17.6},"trap_analysis":{"verdict":"🟡","label":"估值下移、永續段縮水；核心指數未見衰退"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q1 平均基點因 BlackRock 新約下限下滑，Q2 再因低費率大型 ETF 資產占比上升而下滑；BlackRock 占 Index 段由 17.4% 升到 18.7%；主動 ETF 檔數已超過被動","assumption":"指數基準的黏性足以讓費率只隨組合變動，不隨議價下滑","consequence":"大型 ETF 發行商若每次續約都往下壓，ABF 成長長期落後資產規模 15 個百分點以上，EPS 年增掉到中個位數，本益比落到 18 倍，五年後股價約 400 美元以下","ruling":"部分採納：Q2 下滑主因是資產組合（Q2 法說財務長），BlackRock 新約調整約 0.1 基點（2026-09-14 巴克萊會議），目前是慢性壓力，不是崩壞。和唯一致命點部分重疊：那條是一次性換指數，這條是逐年壓費率的慢性版，已放進 bear 路徑與 30% 機率","watch":"ABF run rate 年增率減期末掛鉤 ETF AUM 年增率","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#2","end_markets#4"],"fact_refs":["f_kpi6_index_analytics_organic_"]},{"view":"論點失敗","evidence":"AI 工具可低成本解析永續揭露、複製部分 ESG 評等；歐盟新規自 2026-07-02 起要求 ESG 評等商取得 ESMA 授權；管理層預期 S&C 段未來兩季淨新增約零到小負，CEO 稱永續需求是拉長的週期性下行","assumption":"永續段只是週期性低迷，不是被替代","consequence":"AI 替代若成真，S&C 段長期負成長，並拖累 Analytics 的定價","ruling":"採納但限縮：衝擊集中在 S&C 段；氣候 run rate 仍年增近 12%，掛永續與氣候指數的指數基金資產約 1.3 兆美元，反而支撐 Index","watch":"S&C 段淨新增經常性銷售、Analytics 有機訂閱 run rate","evidence_refs":["substitute_technology#0","regulatory_antitrust#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"費用指引一路往上：2026-04-21 財務長說落在原區間上半，2026-07-21 上修營運費用區間，2026-09-14 又說落在新區間高端並有遣散費；績效型股酬與獎金跟著資產規模走；回購均價約 558 美元，買入收益率約 3.5%；First Street 與回購動用循環信貸","assumption":"營收加速會帶來營業槓桿","consequence":"營收成長但利潤率不升，EPS 只跟營收同速；加上高價回購與舉債，每股價值成長慢於營收","ruling":"採納：base 路徑 FY2029 起只給 10–11%，不假設利潤率擴張；費用由 R4 監控","watch":"調整後 EBITDA 利潤率、費用年增率對營收年增率","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_kpi1_adjusted_ebitda_margin_n","f_kpi7_fy2026_guidance_q2"]},{"view":"價格已反映太多","evidence":"FY1 本益比 27.5 倍、PEG 約 2.0；ABF 年增 25% 有一段來自股市高位；Q2 後 JPMorgan、Evercore 下修目標價","assumption":"共識兩年 EPS 年化 13.7% 沒有計入股市回檔","consequence":"股市持平一年，ABF 成長回到個位數，FY2027 EPS 低於 22.5，本益比再壓到 23 倍，一年內下跌一成以上","ruling":"部分反駁：倍數已在近四個年度端點最低，26 週只漲 2.8%，市場已先扣掉費用上修；但股市高位帶來的收益沒有被折價，所以不追價，等 474 美元","watch":"FY2027 共識 EPS 修正方向、前瞻本益比","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_week26_return_pct"]}],"max_dd":{"lo":-45,"hi":-25,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 542.72","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=542.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"費率下滑是議價權流失還是組合效應","cause":"新證據","side_a":"議價權流失：BlackRock 續約調低部分產品費率下限，Q1 平均基點下滑；BlackRock 占 Index 段由 17.4% 升到 18.7%；公司風險因子自承客戶可能要求降費或停用","side_b":"組合效應：Q2 下滑主因是資金集中流入美國以外已開發市場與全球型的低費率大型 ETF，新興市場流入變少（Q2 法說財務長）；BlackRock 調整約 0.1 基點（2026-09-14 巴克萊會議）；ABF run rate 仍年增 25%","ruling":"可調和，屬程度差異：短期以組合為主，但大客戶下限調低是結構性的，每次續約只會往下；定價力給 8 分不給 9 分","evidence_level":"公司申報加法說原話","settle_metric":"平均基點對照期末掛鉤 ETF AUM 的新興市場占比","if_then":["若 ABF run rate 年增率落後期末掛鉤 ETF AUM 年增率超過 15 個百分點且連 2 季，則停止加碼，H2 判為反轉","反向：若新興市場流入回升且平均基點持平或回升，則維持費率下滑只是組合效應的判斷"],"evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2"]},{"axis":"費用指引前後說法","cause":"新證據","side_a":"管理層：自稱審慎的財務管理者，費用上修是自願加碼投資，手上有調節槓桿（2026-07-21 Q2 法說，CEO 與財務長）","side_b":"指引一路往上：2026-04-21 財務長說落在原區間上半；2026-07-21 上修營運費用區間 4,500 萬美元；2026-09-14 巴克萊會議又說落在新區間高端，Q3 調整後 EBITDA 費用約 3.3 億美元高段並含遣散費；被追問遣散費分布時財務長不願細說","ruling":"可調和，屬程度差異：上修主因是跟資產規模連動的績效股酬與獎金、First Street 併入，和 ABF 收入同向；但管理層已明說 AI 省下的錢要再投資、不讓利潤率跳升，營業槓桿不能指望","evidence_level":"三場管理層原話前後對照","settle_metric":"FY2026 實際調整後 EBITDA 費用對 13.40–13.70 億美元區間；Q4 調整後 EBITDA 利潤率","if_then":["若 FY2026 調整後 EBITDA 費用超過 13.70 億美元上緣且 Q4 利潤率低於 60%，則減碼三分之一並下修 base 路徑","反向：若 Q3 費用在 3.3 億美元高段以內且利潤率守住 61%，則維持"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"管理層指引與交付（一致項）","cause":"新證據","side_a":"2026-04-21 財務長預告 Q2 Analytics 營收年增約 5%，因一次性導入收入不會重複","side_b":"Q2 Analytics 有機營收年增 7%，好於指引；但 Analytics 訂閱銷售偏弱，CEO 歸因於時點不均","ruling":"一致：本季交付不低於自己的指引。訂閱銷售只是時點問題屬未證歸因，登記期限：Q3、Q4 Analytics 有機訂閱 run rate 仍低於 6.6%，歸因就不成立","evidence_level":"法說原話前後對照","settle_metric":"Analytics 有機訂閱 run rate","if_then":["若 Analytics 有機訂閱 run rate 連 2 季低於 6%，則停止加碼，並把 Analytics 移出成長引擎","反向：若回到 7% 以上，視為時點問題已證實"],"evidence_refs":[]},{"axis":"現在買或現在賣的最強論證","cause":"價格變動","side_a":"現在就買：倍數在近四個年度端點最低，26 週只漲 2.8%，RSI 41；管理層在約 558 美元仍在回購，CEO 說願意站在賣股者的對面；Index 訂閱 run rate 加速、留存上升","side_b":"現在就賣：ABF 年增 25% 有一段來自股市高位，費用指引連兩次往上，JPMorgan、Evercore 下修目標價；股價低於 52 週與 104 週均線，週線偏弱；PEG 約 2","ruling":"不可調和，選等價格：生意面站買方（留存與訂閱加速是硬數據），價格面站賣方（基本情境年化約一成、PEG 2.0）。綁住進場的是價格，不是論點","evidence_level":"價格加季報數據","settle_metric":"股價對 FY1 本益比 24 倍（約 474 美元）","if_then":["若股價跌到 474 美元以下且 Index 訂閱 run rate 仍在 10% 以上，則建首批","若股價先漲破 638 美元而 Q3 費用超標，則不追","反向：若 Q3 Index 訂閱 run rate 跌破 9%，即使到價也不建倉"],"evidence_refs":["capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"Index 有機訂閱 run rate 年增率連四季低於 9%，指數標準擴張的論點削弱","type":"假設驗證","maps_to":"H1","metric":"Index 有機訂閱 run rate 年增率","threshold":"低於 9% 連 4 季（現 11.1%）","action":"停止加碼","source_freq":"季報新聞稿／每季","date":"2026-10"},{"n":2,"text":"ABF 成長落後掛鉤 ETF 資產成長太多，代表費率拖累失控","type":"假設驗證","maps_to":"H2","metric":"ABF run rate 年增率減期末掛鉤 ETF AUM 年增率","threshold":"落後超過 10 個百分點連 2 季","action":"停止加碼","source_freq":"季報新聞稿與財報簡報／每季","date":"2026-10"},{"n":3,"text":"新成長曲線沒有接棒，全公司訂閱成長停在 8% 以下","type":"假設驗證","maps_to":"H3","metric":"全公司有機訂閱 run rate 年增率、留存率","threshold":"低於 8% 連 2 季，或留存低於 94.5%","action":"停止加碼","source_freq":"季報新聞稿／每季","date":"2026-10"},{"n":4,"text":"BlackRock 集中度再升且平均基點明顯下滑，大客戶議價轉成實質降費","type":"風險","maps_to":"R1","metric":"BlackRock 占營收比、平均基點年變動","threshold":"BlackRock 占營收超過 12% 且平均基點年降超過 10%","action":"減碼三分之一","source_freq":"10-K 每年；季報每季","date":"2027-02","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":5,"text":"股市修正或新興市場地緣事件讓掛鉤 ETF 資產大跌；訂閱沒壞就分批反買，不停損","type":"風險","maps_to":"R2","metric":"季末掛鉤 ETF AUM 季變動","threshold":"季減超過 15%，同時全公司有機訂閱 run rate 仍在 8% 以上","action":"分批反買","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["geo_supply_chain#0"]},{"n":6,"text":"掛鉤 ETF 資金流入明顯轉弱，主動 ETF 分流開始反映","type":"風險","maps_to":"R3","metric":"掛鉤 MSCI 指數 ETF 單季現金流入","threshold":"連 2 季低於 200 億美元（Q2 近 400 億）","action":"停止加碼","source_freq":"季報法說／每季","date":null,"evidence_refs":["end_markets#4"]},{"n":7,"text":"費用跑贏營收，利潤率連續下滑","type":"風險","maps_to":"R4","metric":"調整後 EBITDA 利潤率年變動","threshold":"連 2 季年減超過 1 個百分點（Q2 62.1%）","action":"減碼三分之一","source_freq":"季報新聞稿／每季","date":"2026-10","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"n":8,"text":"永續段持續失血，AI 替代或監管成本開始吃掉這一段","type":"風險","maps_to":"R5","metric":"S&C 段淨新增經常性銷售","threshold":"連 3 季為負","action":"停止加碼","source_freq":"季報法說／每季","date":null,"evidence_refs":["substitute_technology#0","regulatory_antitrust#1"]},{"n":9,"text":"BlackRock 宣布大型 iShares MSCI 產品改掛其他指數或自編指數","type":"Single Thing","maps_to":"Single Thing","metric":"iShares 產品標的指數變更公告","threshold":"任一大型 iShares MSCI 產品宣布換指數","action":"清倉","source_freq":"BlackRock 與 MSCI 公告／事件","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":10,"text":"價格回到 FY1 本益比 24 倍且指數訂閱仍健康，建首批","type":"估值rearm","maps_to":"H1","metric":"股價、Index 有機訂閱 run rate","threshold":"股價 474 美元以下，且 Index 訂閱 run rate 年增 10% 以上","action":"建首批","source_freq":"每日股價；每季財報","date":null},{"n":11,"text":"價格跌到 FY2 本益比約 18.7 倍而論點未削弱，加第二批","type":"加碼","maps_to":"H1","metric":"股價、H1 至 H3 狀態","threshold":"股價 420 美元以下，且 H1 至 H3 都沒有削弱","action":"加第二批","source_freq":"每日股價；每季財報","date":null},{"n":12,"text":"價格漲到 FY2028E 本益比約 27.4 倍而共識沒有上修，先收一部分","type":"減碼","maps_to":"R4","metric":"股價、FY2028E 共識 EPS","threshold":"股價 700 美元以上，且 FY2028E 共識未上修","action":"減碼三分之一","source_freq":"每日股價；共識每月","date":null},{"n":13,"text":"FY2026 年報與 FY2027 財測出爐後重跑研究","type":"複審日期","maps_to":"H2","metric":"年報客戶集中度、FY2027 費用財測","threshold":"年報發布","action":"重跑研究","source_freq":"年度","date":"2027-02"}],"kill_metrics":[{"metric":"Index 有機訂閱 run rate 年增率","bear_threshold":"低於 7% 連 2 季（現 11.1%）","window":"每季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"全公司留存率","bear_threshold":"低於 93.5%（現 95.3%）","window":"每季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"調整後 EBITDA 利潤率","bear_threshold":"低於 58% 連 2 季（Q2 62.1%）","window":"每季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"BlackRock 占 Index 段營收比","bear_threshold":"超過 22%，或任一大型 iShares 產品換指數","window":"每年（10-K）","source":"MSCI 10-K 客戶集中度揭露","last_status":"warning"},{"metric":"ABF run rate 年增率減期末掛鉤 ETF AUM 年增率","bear_threshold":"落後超過 15 個百分點連 2 季","window":"每季","source":"MSCI 季報新聞稿與財報簡報","last_status":"unknown"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把平均基點下滑當成議價權流失，但 Q2 下滑主因是資金流向低費率大型 ETF 的組合變化，BlackRock 新約調整約 0.1 基點，ABF run rate 仍年增 25%；倍數已壓到近四個年度端點最低"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=2.77, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價回到 474 美元以下（FY1 本益比 24 倍），且 Index 有機訂閱 run rate 年增仍在 10% 以上","exec_line":"現價基本情境年化約一成，合理不便宜；474 美元以下建首批，420 美元以下加第二批，700 美元以上減碼三分之一，BlackRock 換指數即清倉"},"reasoning":{"industry":"營收分四段：Index（訂閱加按資產計費 ABF）、Analytics（風險與因子模型訂閱）、Sustainability and Climate、Private Assets。Q2 營收 8.67 億美元，GAAP 營益率 56.2%，調整後 EBITDA 利潤率 62.1%，TTM 毛利率 83.0%。成長主力在 Index：上半年 Index 營收年增 17.6%，其中 ABF 年增 26.6%、訂閱年增 10.3%。ABF run rate 約 9.48 億美元，接近全公司營收年化的三成，這塊跟著掛鉤 ETF 的資產規模上下。Analytics 有機訂閱 run rate 年增 6.6%；Private Assets 段 Q2 營收 7,470 萬美元，有機年增 4.4%。各段占營收比重事實表未涵蓋。產業時鐘在擴張期：掛鉤 MSCI 指數的 ETF 資產逾 2.8 兆美元，Q2 流入近 400 億美元，留存率由 94.4% 升到 95.3%；依據是資金流與留存，不是股價。供需持久度：訂閱需求屬結構性持久，基準一旦寫進投資契約很少換；ABF 屬週期性，跟著股市位階走。單點依賴：BlackRock 占 FY2025 營收 10.8%、占 Index 段 18.7%（FY2022 為 17.4%），其中 96.5% 是按資產計費，集中度在升。產業態勢是雙向拉鋸：被動與系統化投資擴大、交易生態對指數資料的需求上升，屬結構轉好；永續需求週期性下行、歐盟 ESG 評等授權新規、主動 ETF 檔數超過被動，屬其他結構變數。","moat":"機制：資產主與顧問把 MSCI 指數寫進投資政策與績效基準，基金經理人、ETF 發行商、做市商與對沖基金就得跟著買授權與資料。用的人越多，流動性越集中在 MSCI 指數上，換掉的成本越高。可證方向：同業只有利潤率可比，ROIC 事實表未涵蓋。MSCI TTM 營益率 55.7%，高出 MCO 9.6 個百分點、SPGI 14.1 個百分點、FDS 26.1 個百分點；毛利率 83.0% 對 SPGI 70.9%、MCO 75.0%。只有單期資料，差距擴大或收窄無法判，改看留存：全公司留存 95.3%（去年同期 94.4%），Index 留存逾 97%，對沖基金客群同樣逾 97%（Q2 法說財務長）。執行力 9 分：兩季推出 80 多項新品，Index 訂閱 run rate 由 8% 中段加速到 11% 以上，PCS 加速到 16% 以上。定價力 8 分：調價對新增銷售的貢獻穩定，但 BlackRock 續約調低部分產品費率下限，低費率大型 ETF 資產占比上升，平均基點連兩季下滑，大客戶手上有議價力。執行面擴大、定價面縮減，合起來持平。威脅都屬點對點：AI 複製 ESG 評等只打永續段；自助式指數平台與主動 ETF 分流屬邊緣競爭，公司已用 Foxberry 平台與主動型產品授權回應。","growth":"成長來源：量為主（ABF 隨資產規模、訂閱新客與新模組），價為輔（調價貢獻穩定），併購小，淨回購每年約 2%。共識 EPS：FY2026E 19.74、FY2027E 22.5、FY2028E 25.54，兩年年化 13.7%；FY2025 實際值與分析師家數事實表未涵蓋，以兩年代替三年。內生上界取 10%（推導見護城河題）。共識高出約 3.7 個百分點，歸因：淨回購約 2 個百分點，2026 年 ABF 在資產新高時墊高的基期延續約 1 個百分點，其餘靠利潤率小幅擴張。缺口可歸因，但其中一塊要股市不回檔才成立。跑道：被動化滲透率事實表未涵蓋，燈號依第二曲線判斷。Index 對沖基金客群訂閱 run rate 年增 19%，客製指數有機訂閱 run rate 23%，PCS 16% 以上，首份 AI 模型訓練授權已簽（Q2 法說）；CEO 自評對沖與交易生態還在九局的第二、三局。衰退信號亮兩個：自身本益比、市銷率、EV/S 都在近四個年度端點最低；永續段需求收縮（美洲取消多，未來兩季淨新增約零到小負）。","governance":"現金流：Q2 自由現金流 3.26 億美元，TTM FCF 利潤率 44.8%，FY2026 財測 14.85–15.45 億美元；資本支出財測 1.60–1.70 億美元，約自由現金流的一成，屬輕資產。現金去向：今年到 7 月 20 日回購約 6.11 億美元（Q1 法說逾 4.64 億、Q2 法說 1.47 億、均價約 558 美元）；併購多筆小型補強（Vantager、Compass、PM Insights、First Street）；First Street 與回購部分用循環信貸支應，利息費用財測因此上修。股息金額與債務到期結構事實表未涵蓋，情境試算股息記 0、淨回購記 2%，合計低估股東回報。淨回購 2% 的算法：年化回購約 11 億美元，對照市值約 400 億美元（市銷率 11.84 除以 FCF 利潤率 44.8% 得 P/FCF 約 26.4 倍，乘 FCF 財測中位數），約 2.7%，扣 SBC 與舉債支應的部分取 2%。計分：回購，558 美元對 FY2026E EPS 19.74 的買入收益率約 3.5%，要 10 年期殖利率低於 1.5% 才過，判不過（10 年期殖利率事實表未涵蓋）；併購，金額與實現回報事實表未涵蓋，Burgiss 收購後約兩年半才換好團隊，私募資產段 Q2 有機營收只增 4.4%，Fabric 去年沖回或有對價，證據偏負，判不過；SBC 約占市值 0.25%，遠低於每年 1.5%，過。","valuation":"FY1 本益比 27.5 倍、FY2 24.1 倍，trailing 29.6 倍；本益比、市銷率 11.8 倍、EV/S 13.7 倍都落在近四個年度端點最低（只有四個年度點，不是五年分位）。PEG：FY1 本益比 27.5 除以兩年 EPS 年化 13.7%，約 2.0，在合理區上緣。共識 EPS 近期幾乎沒動（FY1、FY2 修正 0%，FY3 加 0.08%）。賣方平均目標價約 692 美元、區間 570–760；Q2 後 JPMorgan 由 742 降到 700、Evercore 由 746 降到 722，理由是費用上升。十二個月基本情境：FY2027E 22.5 乘 26 倍約 585 美元，上檔 7.8%；兩到三年：FY2028E 25.54 乘 25 倍約 639 美元，上檔 17.6%。同業前瞻本益比事實表未涵蓋，無法做跨同業倍數對照。結論：價格合理不便宜；倍數已先修正，下檔有一部分已被吃掉。","premortem":"看錯的三條路寫在反證紀錄。技術面：股價 542.72 美元，低於 52 週均線 565.73 與 104 週均線 564.28，高於 250 週均線 517.85；250 週均線 13 週斜率為負 0.08%，長期趨勢走平。RSI 41.2，26 週報酬 2.8%，沒有過熱。歷史最大回撤與空方最強數字事實表未涵蓋。管理層在 2026-09-14 巴克萊會議被問到遣散費落在哪些部門時不願細說，屬資訊保留，併入費用監控。價值陷阱風險判黃：亮兩個衰退信號（自身倍數系統性下移、永續段需求收縮），核心指數與訂閱未見衰退。"},"plain":{"six":{"how_it_makes_money":"賺的是全球資產管理業的標準使用費：錢卡在指數授權這一節點。資產主把 MSCI 指數寫進基準，基金、ETF 與交易商就得付訂閱費和按資產計的費用。","moat":"護城河寬、方向持平：指數基準的網絡效應還在加深（留存上升、交易生態擴張），但大型 ETF 客戶把費率往下壓，兩股力量互相抵銷。","growth":"五年後跑道寬：核心被動授權趨於成熟，但對沖基金交易生態、私募資產財富管理通路、AI 內容授權三條新曲線已經看得到數字，只是規模還小。","capital":"資本配置中等：現金大多回給股東、SBC 稀釋低，但回購買在高本益比，收購回報還沒證實。","valuation":"現價要的是 EPS 每年複合一成出頭、五年後本益比仍有 24 倍；成長我信，倍數回升我不押，價格合理但不便宜。","how_wrong":"最可能看錯的地方：把 2026 年股市新高帶來的 ABF 高成長當成常態，同時低估大型 ETF 客戶壓費率的力道。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把平均基點下滑當成議價權流失，但 Q2 下滑主因是資金流向低費率大型 ETF 的組合變化，BlackRock 新約調整約 0.1 基點，ABF run rate 仍年增 25%；倍數已壓到近四個年度端點最低","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"trap":"🟡","val":"🟡","moat":"A","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":542.72,"week26_return_pct":2.77,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母用 FY2026E 共識 19.74，事實表未標 GAAP 或調整後；trailing 29.6 倍用 GAAP 分母，兩者口徑不同不混用。Q2 單季 EPS 對共識是勝是負，各彙整站說法矛盾，但不影響全年共識分母"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"Q3 FY2026 財報：Q3 調整後 EBITDA 費用（財務長給 3.3 億美元高段）、First Street 併入後的 run rate、S&C 淨新增","impact":"高","watch":"Index 訂閱 run rate 是否守住 11%、平均基點走向"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 FY2027 費用財測","impact":"高","watch":"費用成長率對營收成長率、回購節奏"},{"date":"2026-Q4","date_precision":"quarter","type":"regulatory","event":"歐盟 ESG 評等規範 2026-07-02 生效後的 ESMA 授權進度","impact":"低","watch":"S&C 段是否出現合規成本或產品調整"}],"_projected_from":"v19"}
```
