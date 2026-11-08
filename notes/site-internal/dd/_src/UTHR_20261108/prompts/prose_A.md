你是 stock-analyst v20 的**散文層（prose）agent**，標的 UTHR（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：UTHR　日期：2026-11-08　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1802B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（408B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（999B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1577B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（909B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（539B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（849B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2378B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4095B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3467B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1802           3639-5198      5 條（2–6 內）  
s3                  8000         408           5314-7592      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3485          8060-11515      5 條（2–6 內）  
s6                 11000         539          7323-10461      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         849           1856-2651      5 條（2–6 內）  
s10                 5000        2378           1835-2622      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3467           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4693B；至少需散文≈40.31KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−41.66%
−35
−0.52
0%
0
0.6%
0.7%
0.75
0.78
0.90
1
1.1
1.22
1.25%
1.253
1.3
1.33
1.4
1.45
1.5%
1.64
2.0
02
2
2.1%
2.2%
2.3
2.5%
03
3%
3
3.7%
3.785
4
04
4.776
4.9
4.9%
4.99%
5%
5
05
5.038
5.71
5.83
5.85
06
6%
6
6.03%
6.04
6.074
6.3%
6.512
7
07
7.3
7.4%
7.51
08
8
8.1
8.3
8.325
8.4
8.4%
8.5
8.51
8.6%
8.8
9
9%
09
9.2%
10
10%
10.6%
10.9%
11%
11
11.4
11.5
12%
12
13%
13.6%
14
14.139
14.7
14.7%
14.8%
15%
15
15.0%
15.04%
15.35
16
16.58
16.6
17
17.3
17.3%
17.4%
18
18.0%
18.5
18.5%
19.4
20%
20
20.06
20.679
21
21%
21.22
22.06%
22.5
22.9%
23.6%
24
24.04%
25
25%
26
27.21%
27.86
28.02
29.97%
30%
30
30.5
31
31.5
32
33
33.5
33.89
34%
35%
35.146
35.357
35.4
36%
36.5
37.0%
37.39%
39.39%
40
40%
40.5
41%
42%
42
42.41
43%
45
45%
45.65%
46
47
47.67%
49
50%
50
50.33%
51%
52.5
52.6%
53
57
60%
60.5%
66
68
70
74
76%
78%
83
84%
86.34%
87.92%
88%
89.24%
90%
90
91%
92.17%
92.6%
93.3
93.3%
100
100%
104
150%
232
239.4
279
330
372
480
533
562.02
650
664
664.33
2025
2026
2027
2028
2040
20261108
1,000
3,950
4,100
5,230
7,410
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
{"meta":{"ticker":"UTHR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"United Therapeutics"},"oneliner":"基本盤在 Q3 止穩，PH-ILD 和解補回缺口，現價約 FY2027E 的 16.6 倍；股價要走得好，得靠 2027 年 4 月底 IPF 獲准和上市後放量。","thesis":{"H":[{"id":"H1","text":"基本盤止穩：DPI 的增量蓋過霧化劑流失，Tyvaso 在 IPF 上市前維持正成長。","2y":"2026 Q4 到 2027 Q2 的 Tyvaso 單季年增都在 5% 以上，2026 Q4 總營收達 8.4 億美元以上。","5y":null,"10y":null,"threshold":"Tyvaso 單季年增達 5%；2026 Q4 總營收達 8.4 億美元（共識隱含約 8.5 億）。","source":"公司新聞稿 8-K Ex.99.1 與 10-Q 的產品別營收，每季。","drift_rule":"TTM 偏離門檻連 2 季達 5% 算削弱，連 3 季達 10% 算反轉。"},{"id":"H2","text":"霧化 Tyvaso 取得 IPF 適應症並在上市後放量，成為第二條成長曲線。","2y":"2027-04-30 前獲准，2027-06 前上市，FY2028 總營收達 40 億美元。","5y":"FY2031 Tyvaso 總營收達 33 億美元（FY2026E 約 19.4 億，由前九個月加 Q4 估算）。","10y":null,"threshold":"FDA 2027-04-30 前獲准；FY2028 總營收 40 億美元；FY2031 Tyvaso 33 億美元。","source":"FDA 決定、公司 8-K、季報的 Tyvaso 分項營收。","drift_rule":"未獲准直接反轉；獲准後 TTM 低於路徑連 4 季達 5% 算削弱，連 6 季達 10% 算反轉。"},{"id":"H3","text":"ralinepag 與後續產品降低對 treprostinil 的依賴，淨現金與回購讓每股盈餘跑贏淨利。","2y":"ralinepag 於 2027-06-24 獲准，股數年減達 2.5%。","5y":"FY2031 非 treprostinil 產品占營收達 20%（Q3 2026 約 7.4%）。","10y":null,"threshold":"ralinepag 2027-06-24 獲准；非 treprostinil 占比 20%；股數年減 2.5%。","source":"FDA 決定、季報的產品別營收與股數。","drift_rule":"TTM 偏離門檻連 4 季達 5% 算削弱，連 6 季達 10% 算反轉；FDA 拒絕時直接重評。"}],"R":[{"id":"R1","text":"PAH 競爭持續侵蝕 treprostinil，Winrevair、Yutrepia、TPIP 三面夾擊；PH-ILD 還有標示外使用的漏洞。","h_ref":"H1","clock":"🔥","threshold":"Tyvaso 年增連兩季低於 0%，或 Remodulin 年減達 10%。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#1","end_markets#3","substitute_technology#2","supply_demand_durability#1"]},{"id":"R2","text":"IPF 或 ralinepag 的審查結果不如預期，或原料供應商 OAI 拖累 ralinepag 時程。","h_ref":"H2","clock":"⚡","threshold":"IPF 2027-04-30 前未獲准；ralinepag 2027-06-24 未獲准。","evidence_refs":[]},{"id":"R3","text":"學名藥與專利到期：Orenitram 2027 年可上市，霧化 Tyvaso 學名藥是否已進場未證實，管理層的 2040 年代專利說法未經逐項驗證。","h_ref":"H1","clock":"🔥","threshold":"學名藥上市後兩季內 Orenitram 下滑 25%。","evidence_refs":["supply_demand_durability#3"]},{"id":"R4","text":"藥價與給付政策：MFN、專利藥關稅、付款方階梯療法壓縮淨價。","h_ref":"H1","clock":"🐢","threshold":"TTM 毛利率連兩季低於 84%。","evidence_refs":["reg_tariff_export#0","substitute_technology#1"]},{"id":"R5","text":"經銷集中在 Accredo 與 CVS Specialty，應收帳款集中；聚合站的 51% 與 36% 未核一手。","h_ref":"H1","clock":"🐢","threshold":"任一家經銷合約終止或付款條件明顯惡化；實際占比需以 10-K 核對。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R6","text":"法律風險：Sandoz 案已提列 7,410 萬美元，專利和解可能引發反壟斷主張，公司曾遭 DOJ 調查與保險公司 RICO 提告；其餘案件金額與結案時點事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"DOJ 或 FTC 新立案，或單案估損達 2 億美元。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","lawsuit_class_action#0"]},{"id":"R7","text":"裝置與供應鏈：Remodulin 輸注泵浦依賴第三方且型號停產，資料來自 FY2024 10-K；Remodulin 占 Q3 營收 14.7%。","h_ref":"H1","clock":"🐢","threshold":"公司揭露泵浦短缺導致 Remodulin 單季年減達 10%。","evidence_refs":["geo_supply_chain#1"]},{"id":"R8","text":"成本與資本配置：研發、上市費用與製造器官吃掉利潤，TTM 營益率下滑有約 4 個百分點未解釋。","h_ref":"H3","clock":"🔥","threshold":"排除一次性費用後的營益率連兩季低於 45%。","evidence_refs":[]}],"single_thing":{"description":"FDA 在 2027 年 4 月底審查期結束時，未核准霧化 Tyvaso 的 IPF 適應症，或延審超過 6 個月。","why_fatal":"共識 EPS 從 FY2027E 33.89 美元跳到 FY2028E 42.41 美元，主要靠新產品。IPF 落空時，Base 的 FY2028E 40.5 美元會回到 Bear 的約 32 美元，少 21%，本益比再從 16 倍往 11.5 倍走，合計價值少約 43%，是情境裡最大的單一敏感項。","if_happens":"減碼至原倉位一半，Base 機率移 20 個百分點到 Bear 重算；同時 Tyvaso 年增連兩季低於 0% 就清倉。","how_monitor":"盯 2027-04-30 審查期與公司 8-K，獲准後看標籤的適應症範圍與用藥限制。","probability":"12 到 24 個月內約 10% 到 15%。兩個 Phase 3 都達主要終點，FDA 已受理；事實表沒有 TETON-1 效果量，這是判斷值。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.58,"peg_fy2":1.1,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":27.86,"FY2026E":28.02,"FY2027E":33.89,"FY2028E":42.41},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS；FY2026E 到 FY2028E 為 Koyfin 共識，GAAP 或非 GAAP 口徑事實表未標，分析師家數未列。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"單一分子、高毛利、淨現金、大額回購、晚期管線待批"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：PAH 與肺纖維化病人需要長期用藥，治療選項增加，適應症仍在擴大；依據為 2026-09-30 的 10-Q 與 2026-11-04 法說，判斷不看股價。","bargaining":{"up":"商業原料與成品都在美國製造；ralinepag 的原料供應商被 FDA 列為 OAI，是單一供應點風險。","down":"美國只有 Accredo 與 CVS Specialty 兩家非獨家經銷；聚合站稱約占營收 51% 與 36%，未核一手。付款方可要求學名藥替代或階梯療法。","geo":"二三級供應商在中國、印度、台灣，公司對主要供應商的供應鏈能見度有限。"},"profit_pool_dir":"PAH 的利潤池被新機轉與同分子新劑型分走一部分，PH-ILD 因和解回到 UTHR 手上，IPF 是新增的池子，尚未開張。","tam_table":[{"item":"IPF、PPF、PH-COPD 美國病人數","value":"約 100 萬人，管理層 2026-11-04 法說自述，未經第三方核對"},{"item":"PH-ILD 滲透率","value":"管理層稱市場大且滲透不足，具體數字事實表未涵蓋"},{"item":"SAM、分段 CAGR、營業利益池五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"吸入式 treprostinil 的分子加裝置組合，配上長年累積的肺高壓專科醫師關係與用藥支持；PH-ILD 另有和解帶來的標籤保護。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"Q3 Tyvaso 合計年增 5%，DPI 年增 13%，法院判決與和解拿掉 Yutrepia 的 PH-ILD 適應症；反向是 10-Q 寫明競品已傷及三個 treprostinil 產品，霧化劑年減 12%、Remodulin 年減 3%。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用營益率與 FCF 利潤率當可比軸。","threats":[{"level":"🔴","text":"Merck 的 Winrevair 以新機轉切入 PAH，Insmed 的 TPIP 進入後期；若 prostacyclin 類藥物被往後線推，PAH 基本盤會持續流失。","p":"35%","evidence_refs":["competitive_share_entrants#0","substitute_technology#2","end_markets#1"]},{"level":"🟡","text":"Yutrepia 在 PAH 直接競爭；PH-ILD 標籤雖被拿掉，現有病人不必換藥，標示外使用是否下降要靠處方資料驗證。","p":"40%","evidence_refs":["competitive_share_entrants#3","supply_demand_durability#1","end_markets#3"]},{"level":"🟡","text":"Orenitram 學名藥 2027 年 6 月與 12 月可上市，霧化 Tyvaso 學名藥依舊文件最早 2026 年 1 月可進場，實際是否上市未證實；Orenitram 占 Q3 營收 17.4%。","p":"60%","evidence_refs":["supply_demand_durability#3"]},{"level":"🟡","text":"IPF 市場已有 Jascayd，Tyvaso 上市後能排到第幾線用藥，事實表沒有資料。","p":"35%","evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率，周轉率未知（投入資本事實表未涵蓋，當期 ROIC 無法計算）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是重症病人，決策者是肺高壓專科醫師，付款者是保險與 Medicare；延後用藥的代價高，10 月轉介超過 1,000 件是管理層提供的單月新高。"},{"item":"決策層級","level":"🟡","text":"替代發生在每位病人的處方上。Benkowitz 說用 Yutrepia 穩定的病人不會被換回來，這句話反過來也代表新病人的份額要逐一爭取；PAH 競爭中，PH-ILD 有標籤保護。"},{"item":"價值鏈分配","level":"🟡","text":"86.34% 的毛利率說明價值大多留在 UTHR；兩家經銷商集中，付款方可推階梯療法，毛利率五年下滑的原因事實表未拆解。"},{"item":"社會容忍度","level":"🟡","text":"公司調價維持單位數，等於沒有把價格推到經濟上限；MFN 定價威脅與專利藥關稅已入 10-K 風險，尚未點名 UTHR，商業原料與成品都在美國製造可降低關稅曝險。"}],"roiic":93.3,"reinvest_rate":18.5,"endo_ceiling":17.3,"formula_note":"代理算法：財報歷史 FY2022 到 FY2025 淨利增加 6.074 億美元，除以 FY2023 到 FY2025 累計（淨利－FCF）6.512 億，得 93.3%；再投資率＝6.512 億÷三年淨利 35.146 億＝18.5%；兩者相乘 17.3%。研發費用化（TTM 研發密度 22.06%）不在分母，ROIIC 被高估，淨利也含利息收入，17.3% 只能當上限參考。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","UTHR":86.34,"MRK":71.75,"INSM":84.4,"LQDA":92.54,"JAZZ":89.09,"unit":"%"},{"metric":"營業利益率","UTHR":39.39,"MRK":9.2,"INSM":-41.66,"LQDA":37.39,"JAZZ":24.04,"unit":"%"},{"metric":"FCF 利潤率","UTHR":27.21,"MRK":21.89,"INSM":-41.3,"LQDA":32.75,"JAZZ":29.97,"unit":"%"},{"metric":"研發密度","UTHR":22.06,"MRK":45.65,"INSM":62.14,"LQDA":12.43,"JAZZ":17.58,"unit":"%"}],"competitors":[{"name":"MRK","gm":71.75,"om":9.2,"fcf_margin":21.89,"rd_intensity":45.65,"strategy_note":"以新機轉 Winrevair 切入 PAH，資源量級遠大於 UTHR；TTM 營益率 9.2% 與研發密度 45.65% 偏離常態，原因事實表未涵蓋，不拿來比護城河。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"INSM","gm":84.4,"om":-41.66,"fcf_margin":-41.3,"rd_intensity":62.14,"strategy_note":"TPIP 在後期臨床，是 Yutrepia 之後最值得防的同類吸入對手；TTM 營益率 -41.66%，靠外部資金與其他產品撐研發。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"LQDA","gm":92.54,"om":37.39,"fcf_margin":32.75,"rd_intensity":12.43,"strategy_note":"Yutrepia 上市一年多，TTM 營益率已到 37.39%，說明它能自籌彈藥；失去 PH-ILD 標籤後，要看 PAH 能否撐住成長。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"JAZZ","gm":89.09,"om":24.04,"fcf_margin":29.97,"rd_intensity":17.58,"strategy_note":"同規模專科藥對照組，不是直接對手；UTHR 的營益率 39.39% 高於 JAZZ 的 24.04%，FCF 利潤率 27.21% 則略低於 29.97%。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主、單位數調價為輔；FY2028E 的跳升靠 IPF 與 ralinepag，回購放大每股盈餘，併購占比小。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段的內生上界 17.3%，由淨利增量與（淨利－FCF）推得，研發費用化使其偏高；共識三年 EPS 年化 15.0% 未超過，其中含回購貢獻。","segments":[{"item":"Tyvaso DPI","value":"Q3 2026 3.785 億美元，年增 13%，量增加上調價"},{"item":"霧化 Tyvaso","value":"Q3 2026 1.253 億美元，年減 12%，美國量下滑"},{"item":"Orenitram","value":"Q3 2026 1.45 億美元，年增 11%；學名藥 2027 年 6 月與 12 月可上市"},{"item":"Remodulin","value":"Q3 2026 1.22 億美元，年減 3%；前九個月年減 6%"},{"item":"Unituxin","value":"Q3 2026 5,230 萬美元，年增 9%"}],"decay_signals":["毛利率下滑：亮燈。FY2024 89.24%、FY2025 87.92%、TTM 86.34%；逐季年比事實表未涵蓋。","核心市占縮減：亮燈。10-Q 寫競品傷到霧化 Tyvaso、DPI 與 Remodulin，具體份額事實表未涵蓋。","主力產品提價後銷量下滑：未亮。DPI 量價齊升；霧化劑量減是否與提價有關，事實表未涵蓋。","EPS CAGR 高於營收 CAGR 超過 5 個百分點：未亮。FY2022 到 FY2025 為 22.9% 對 18.0%，差 4.9 個百分點，已接近門檻。","FCF 對淨利連兩年低於 0.75：未亮。FY2024 為 0.90，FY2025 為 0.78。","SBC 占營收超過 5% 且逐年上升：未亮。Q3 2026 為 4.9%，歷年趨勢事實表未涵蓋。","TAM 萎縮或被替代：未亮。PAH 有替代壓力，PH-ILD 與 IPF 是擴大方向。","產業倍數三年系統性下移：事實表未涵蓋。","維護性資本支出占 FCF 超過 60%：事實表未涵蓋。","停止投資新產能且收入下滑：未亮。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"2026-03-09","value":"簽 ASR，核准最高 20 億美元庫藏股"},{"item":"2026-09-08","value":"再簽 4.776 億美元 ASR"},{"item":"2026-10-21","value":"董事會核准新的 20 億美元一年期回購，約市值 8.4%"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Thymmune 尚未產生收入，交割現金占市值約 0.6%，已實現報酬無從計算；過往併購收入事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價與 10 年期公債殖利率事實表未涵蓋；以現價估 FY2026E 盈餘殖利率 4.99%，FY2027E 6.03%。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 4,100 萬美元，年化 1.64 億÷市值 239.4 億＝約 0.7%，低於 1.5%；此為近似，未含選擇權完整稀釋。","grade":"過"}]},"valuation":{"basis":"Fwd P/E 與 PEG；盈餘為正、現金流穩定，主看 FY2027E，因 FY2026E 含一次性費用，FY2028E 依賴未獲准產品。","fwd_pe":20.06,"peers":{"expanded":false,"reason":"事實表只有同業利潤率與研發密度，未含 Fwd P/E 或 EV/S，同業倍數對照屬資料缺口。"},"peg":1.33,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2027E 16.58 倍、PEG 1.33、Base 年化約 8.6%，屬合理不便宜；五年分位事實表未涵蓋，4 個年度端點不能替代。","upside_short_pct":7.3,"upside_mid_pct":22.5},"trap_analysis":{"verdict":"🟡","label":"成長換檔期，有兩項衰退訊號，尚非價值陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"10-Q 已寫競爭療法傷到霧化 Tyvaso、DPI 與 Remodulin；IPF 市場已有 Jascayd；Orenitram 學名藥 2027 年可上市；Q3 treprostinil 占營收 92.6%。","assumption":"IPF 獲准後能快速取得處方，PAH 基本盤只是緩慢流失。","consequence":"IPF 獲准但放量慢，PAH 同時被新藥與學名藥吃掉，EPS 卡在約 30 美元，倍數跌到 11 倍，股價約 330 美元，五年虧約 41%；過程中超跌可到 50% 以上。","ruling":"採納為 Bear 路徑，機率 30%。這條與 Single Thing 部分重疊：Single Thing 管能不能拿到核准，這條管拿到之後賣不賣得動。","watch":"IPF 上市後前兩季 Tyvaso 季增金額、DPI 與霧化劑拆分、Orenitram 季營收。","evidence_refs":["substitute_technology#2","end_markets#1","supply_demand_durability#3"],"fact_refs":["f_kpi5_tyvaso","f_kpi6_orenitram_remodulin_unit"]},{"view":"論點失敗","evidence":"管理層稱專利多延伸到 2040 年代，事實表沒有逐項專利到期表，DPI 與 IPF 用途專利的強度無法獨立確認。","assumption":"新適應症與裝置專利足以擋住學名藥。","consequence":"若關鍵專利被挑戰成功，五年後的成長空間要從寬降為中等，終端倍數也要下修。","ruling":"不可裁決至取得專利到期表。先把管理層說法列為未驗證，10 年期延伸只給 Base 每年 6%。","watch":"10-K 專利章節、學名藥申請與 Paragraph IV 訴訟進度。","evidence_refs":["competitive_share_entrants#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"TTM 營益率 39.39%，FY2025 為 47.67%，FY2024 為 50.33%。Thymmune 約占 4 個百分點，其餘約 4 個百分點事實表沒有解釋。公司同時推 14 個管線、擴編業務團隊、做製造器官；MFN 與階梯療法風險寫進 10-K。","assumption":"新適應症的收入會以現有利潤率落到 EPS。","consequence":"IPF 與 ralinepag 都成功，但上市費用、研發與製造器官持續吃掉利潤，ralinepag 也可能分食公司既有 PAH 產品，FY2031E EPS 比 Base 少 10% 到 15%，每股約 5 到 8 美元。","ruling":"部分採納。Base 淨利率只設約 40%，不假設回到 FY2023 的 50% 營益率。","watch":"排除一次性費用後的營益率、研發密度、ralinepag 上市後 Orenitram 的變化。","evidence_refs":["reg_tariff_export#0","substitute_technology#1"],"fact_refs":["f_peer_uthr_operating_margin_pct","f_kpi1_gaap","f_kpi2_gaap"]},{"view":"價格已反映太多","evidence":"Trailing P/E 21.22 倍與 P/S 7.51 倍都是 4 個年度端點的最高；股價高於 104 週均線約 30%；FY2028E EPS 比 FY2027E 多 25%，靠尚未獲准的產品。","assumption":"FY2028E 42.41 美元能達成。","consequence":"IPF 獲准只是兌現預期，若首年銷售低於賣方模型，股價可能在好消息後不漲；Base 年化只有約 8.6%。","ruling":"部分反駁。Trailing 分母被一次性費用壓低，又只有 4 點，不能當五年高位證據；FY2027E 16.58 倍加每股現金約 83 美元，還不到反映太多。但也不便宜，所以不追價。","watch":"Q3 財報後 FY2027E、FY2028E 共識的修正方向；兩次快照都是 0%，要確認是真的沒動還是資料沒更新。","evidence_refs":[],"fact_refs":["f_pe_current","f_pe_percentile","f_ps_percentile","f_ma_w104","f_consensus_eps_fy3","f_kpi7"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 562.02","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=562.02","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷","cause":null,"prior_field":null,"side_a":"10-Q 與法說都顯示 DPI 接手霧化劑，Q3 Tyvaso 合計年增 5%。","side_b":"財報歷史顯示營收成長已由 FY2024 的 23.6% 降到 FY2025 的 10.6%，FY2026E 共識只有 2.1%。","ruling":"兩者一致指向成長換檔，基本盤止穩，下一段成長要靠新適應症。","evidence_level":"一手申報與財報歷史","settle_metric":"Tyvaso 合計年增率","if_then":["若 Tyvaso 年增維持 5% 以上，論點基礎成立。","反向：若連兩季低於 0%，減碼至一半。"],"evidence_refs":[]},{"axis":"競爭傷害與本季創紀錄","cause":null,"prior_field":null,"side_a":"10-Q 寫競爭療法在 Q3 傷到霧化 Tyvaso、DPI 與 Remodulin；前九個月 Tyvaso 合計 14.139 億美元，沒有成長；二手摘要稱上半年霧化劑年減 20%。","side_b":"2026-11-04 法說 Benkowitz 稱 Q3 是史上最佳一季，Tyvaso 5.038 億美元，10 月轉介超過 1,000 件。","ruling":"可調和，屬程度差異。競爭確實造成流失，DPI 的增量在 Q3 開始蓋過。採止穩，不採動能已恢復到雙位數。","evidence_level":"一手對一手；上半年 20% 為二手摘要，方向與 10-Q 一致。","settle_metric":"2026 Q4 與 2027 Q1 的 Tyvaso 合計年增率","if_then":["若兩季都達 5% 以上，維持 Base 路徑，可加碼一檔。","反向：若任一季低於 0%，停止加碼；連兩季低於 0%，減碼至一半。"],"evidence_refs":["end_markets#1","competitive_share_entrants#3"]},{"axis":"Q3 是否受訂單時點影響","cause":null,"prior_field":null,"side_a":"2026-02-25 Benkowitz 說 Q2、Q3 訂單較重，Q1、Q4 較輕，銷售未必反映病患需求。","side_b":"2026-11-04 Benkowitz 回答 Leerink 時說本季沒有庫存或季節因素。","ruling":"未證，先監測。管理層沒給庫存天數，不採信也不否定。共識隱含 Q4 營收約 8.51 億美元，等於要在較輕的季度再季增 2.2%。","evidence_level":"一手法說，但屬管理層說法，沒有庫存數據。","settle_metric":"2026 Q4 總營收與 2027 Q1 季增率","if_then":["若 2026 Q4 總營收低於 8.1 億美元，認定 Q3 含訂單時點，停止加碼。","反向：若達 8.4 億美元以上，接受動能說法，加碼一檔。"],"evidence_refs":[]},{"axis":"40 億美元年化營收的前提","cause":null,"prior_field":null,"side_a":"2026-02-25 Rothblatt 說 2027 年底年化 40 億美元不需要三個新產品，並承諾雙位數營收成長。","side_b":"2026-08-05 Q2 摘要稱這條路徑建立在 IPF 與 ralinepag 獲准之上；2026-11-04 法說沒有再提 40 億，FY2026E 共識營收只年增 2.1%。","ruling":"可調和，採保守側。摘要是二手，還不足以稱改口；但 FY2026 的雙位數已做不到，Base 假設 40 億要靠新產品。從 Q3 的 8.325 億到 2027 Q4 的 10 億，需要連續五季平均季增約 3.7%。","evidence_level":"一手法說對二手摘要","settle_metric":"2027 Q4 單季營收是否達 10 億美元","if_then":["若 2027 Q4 單季營收達 10 億美元，上修 Base 的 FY2028E。","反向：若 2027 Q2 單季營收低於 8.8 億美元，把 2027 年底 40 億從 Base 拿掉並減碼一檔。"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"PH-ILD 還有沒有品牌競爭","cause":null,"prior_field":null,"side_a":"2026-11-04 Benkowitz 說沒有直接的品牌競爭在望，Tyvaso 有長跑道。","side_b":"同季 10-Q 把 Insmed 的 TPIP 列為 PAH、PH-ILD、IPF 或 PPF 的潛在新競品。","ruling":"採 10-Q。和解擋住的是 Yutrepia，不是 TPIP；PH-ILD 的保護期只算到 TPIP 上市前，上市時程事實表未涵蓋。","evidence_level":"一手申報優先於法說口頭說法","settle_metric":"TPIP 的 PH-ILD 試驗結果與申請時點","if_then":["若 TPIP 在 PH-ILD 提出上市申請，Base 從 FY2030E 起 EPS 下修 5%，停止加碼。","反向：若 TPIP 的 PH-ILD 試驗失敗，Bear 機率下調 5 個百分點。"],"evidence_refs":["substitute_technology#2","competitive_share_entrants#0","supply_demand_durability#1"]},{"axis":"新產品時程","cause":null,"prior_field":null,"side_a":"2026-02-25 Rothblatt 說軟霧吸入器今年送件、明年上市。","side_b":"2026-11-04 Poisson 說與 FDA 溝通後要補資料，送件延到 2027；三合一口服錠的生物等效試驗不足，還在找替代路徑；ralinepag 原料供應商被列 OAI。","ruling":"採後者。這些不影響 IPF 主線，但新產品節奏變慢，軟霧吸入器不放進 2028 年前的 Base。","evidence_level":"一手法說前後對照","settle_metric":"2027-06-24 ralinepag 審查結果、軟霧吸入器送件日","if_then":["若 ralinepag 在 2027-06-24 未獲准，下修 FY2028E 起的 EPS 並停止加碼。","反向：若準時獲准且 OAI 解除，維持 Base，不上修。"],"evidence_refs":[]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭惡化：Winrevair、Yutrepia、Jascayd 已上市，TPIP 在後期，10-Q 寫明已傷及銷售。","side_b":"結構轉好：法院維持 UTHR 專利，和解拿掉 Yutrepia 的 PH-ILD 適應症，IPF 若獲准可打開新市場。其他結構變數：MFN 與 232 關稅未點名 UTHR，商業原料與成品都在美國製造。","ruling":"雙向拉鋸。PAH 在惡化，PH-ILD 在轉好，政策面尚未落到公司損益。","evidence_level":"一手申報與法說","settle_metric":"Tyvaso 年增率與 TTM 毛利率","if_then":["若 TTM 毛利率連兩季低於 84%，減碼一檔並下修終端倍數。","反向：若毛利率回升到 88% 以上，Bear 機率下調 5 個百分點。"],"evidence_refs":["end_markets#1","reg_tariff_export#0"]},{"axis":"多空最強論證","cause":null,"prior_field":null,"side_a":"現在就買：FY2027E 16.58 倍，每股現金約 83 美元，2026 年兩度核准各 20 億美元回購，最新一筆約市值 8.4%；IPF 有兩個 Phase 3 達標，ralinepag 已進 FDA 審查，八個月內有兩個 FDA 日期。","side_b":"現在就賣：treprostinil 占 92.6%，10-Q 已寫競品造成傷害，FY2026E 營收只年增 2.1%，FY2028E 的 25% 跳升靠未獲准的適應症，管理層 2026 年的承諾與時程已多次落空。","ruling":"可調和。現價不用等，但不值得在 IPF 結果前重押：先小倉，用財報和 FDA 結果分批加。","evidence_level":"事實表與一手法說","settle_metric":"2026 Q4 營收與 2027-04 底 FDA 決定","if_then":["價格先走證據未到：股價超過 650 美元且 IPF 尚未獲准，不追。","跌但基本面無損：股價跌到 480 美元以下且 Tyvaso 年增仍為正，分批反買。","判斷被證實為錯：Single Thing 發生，減碼至一半；同時 Tyvaso 年增連兩季低於 0%，清倉。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FDA 對霧化 Tyvaso IPF 適應症的決定是最大單一敏感項。","type":"Single Thing","maps_to":"Single Thing","metric":"FDA 對 IPF 補充申請的決定","threshold":"2027-04-30 前未獲准，或延審超過 6 個月","action":"減碼至原倉位一半，Base 機率移 20 個百分點到 Bear 重算","source_freq":"FDA 公告與公司 8-K，單次","date":"2027-04-30","evidence_refs":[]},{"n":2,"text":"2026 Q4 營收驗證 Q3 的動能是否真實。","type":"假設驗證","maps_to":"H1","metric":"2026 Q4 總營收","threshold":"達 8.4 億美元算過，低於 8.1 億美元算不過","action":"過：加碼一檔；不過：停止加碼","source_freq":"公司新聞稿，每季","date":"2027-02（財報日未公告）","evidence_refs":[]},{"n":3,"text":"Tyvaso 轉負代表基本盤沒有止穩。","type":"減碼","maps_to":"R1","metric":"Tyvaso 合計季營收年增率","threshold":"連兩季低於 0%","action":"減碼至原倉位一半","source_freq":"公司新聞稿與 10-Q，每季","date":"每季","evidence_refs":["end_markets#1","competitive_share_entrants#3"]},{"n":4,"text":"和解後 Yutrepia 若仍快速成長，PH-ILD 的保護可能比管理層講的弱。","type":"風險","maps_to":"R1","metric":"Liquidia 公布的 Yutrepia 季營收季增率","threshold":"和解後連兩季季增超過 10%，且 Tyvaso DPI 季增低於 3%","action":"停止加碼","source_freq":"Liquidia 財報，每季","date":"2027-05 起","evidence_refs":["supply_demand_durability#1","end_markets#3"]},{"n":5,"text":"ralinepag 的原料供應商 OAI 狀態可能影響審查日。","type":"風險","maps_to":"R2","metric":"ralinepag FDA 決定","threshold":"2027-06-24 未獲准，或公司宣布延期","action":"停止加碼，下修 FY2028E 起的 EPS","source_freq":"公司 8-K，單次","date":"2027-06-24","evidence_refs":[]},{"n":6,"text":"Orenitram 學名藥上市後的侵蝕速度。","type":"風險","maps_to":"R3","metric":"Orenitram 季營收","threshold":"學名藥上市後兩季內較 1.45 億美元下滑 25% 以上","action":"減碼一檔","source_freq":"公司新聞稿，每季","date":"2027-06 起","evidence_refs":["supply_demand_durability#3"]},{"n":7,"text":"定價與關稅壓力要看能不能被損益吸收。","type":"風險","maps_to":"R4","metric":"TTM 毛利率","threshold":"連兩季低於 84%","action":"減碼一檔並下修終端倍數","source_freq":"季報，每季","date":"每季","evidence_refs":["reg_tariff_export#0","substitute_technology#1"]},{"n":8,"text":"法律與政府調查要按程序性質處理。","type":"風險","maps_to":"R6","metric":"DOJ 或 FTC 新案、民事案估損","threshold":"民事不利判決或估損達 2 億美元；刑事調查介入","action":"民事不利：減碼至一半；刑事介入：清倉","source_freq":"10-Q 訴訟附註與 8-K，每季","date":"每季","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","lawsuit_class_action#0"]},{"n":9,"text":"IPF 獲准且標籤沒有被限縮，是主要加碼點。","type":"加碼","maps_to":"H2","metric":"FDA 核准與標籤範圍","threshold":"2027-04-30 前獲准，適應症涵蓋 IPF 主要族群","action":"加碼一檔，至倉位上限","source_freq":"FDA 標籤與公司 8-K，單次","date":"2027-04-30","evidence_refs":[]},{"n":10,"text":"價格跌到 Base 年化約 12% 的位置，基本面又沒壞，可以反買。","type":"估值rearm","maps_to":"H1","metric":"股價與 Tyvaso 年增率","threshold":"股價 480 美元以下且 Tyvaso 年增為正","action":"分批反買","source_freq":"每日股價與每季財報","date":"持續","evidence_refs":[]},{"n":11,"text":"IPF 落空加上基本盤轉負，論點已不成立。","type":"清倉","maps_to":"H1、H2","metric":"IPF 決定與 Tyvaso 年增率","threshold":"IPF 未獲准，且 Tyvaso 年增連兩季低於 0%","action":"清倉","source_freq":"FDA 公告與每季財報","date":"2027 Q3 前","evidence_refs":["substitute_technology#2"]},{"n":12,"text":"兩個 FDA 日期過後重新評估。","type":"複審日期","maps_to":"H2、H3","metric":"IPF 與 ralinepag 結果","threshold":"兩項結果都出爐","action":"重跑完整研究並更新情境","source_freq":"單次","date":"2027-07-15","evidence_refs":[]}],"kill_metrics":[{"metric":"FDA 對霧化 Tyvaso IPF 適應症的決定","bear_threshold":"2027-04-30 前未獲准，或延審超過 6 個月","window":"2027-04-30 前","source":"FDA 公告與公司 8-K","last_status":"unknown"},{"metric":"Tyvaso 合計季營收年增率","bear_threshold":"連兩季低於 0%","window":"每季；Q3 2026 為 +5%","source":"公司新聞稿 8-K Ex.99.1","last_status":"ok"},{"metric":"2026 Q4 總營收","bear_threshold":"低於 8.1 億美元","window":"2027 年 2 月財報","source":"公司新聞稿","last_status":"unknown"},{"metric":"TTM 毛利率","bear_threshold":"連兩季低於 84%","window":"每季；最新 86.34%","source":"季報與 yfinance 季度損益表","last_status":"warning"},{"metric":"排除一次性費用後的營益率","bear_threshold":"連兩季低於 45%","window":"每季；Q3 2026 還原約 52.6%","source":"公司新聞稿與 10-Q","last_status":"ok"},{"metric":"Orenitram 季營收","bear_threshold":"學名藥上市後兩季內較 1.45 億美元下滑 25% 以上","window":"2027-06 起","source":"公司新聞稿","last_status":"unknown"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用過去幾季沒有成長的印象定價，FY2027E 只給 16.6 倍；PH-ILD 和解到 10 月中才定案，共識兩次快照都沒動。若快照只是尚未更新，這個理由要打折。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-0.52, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"股價 480 美元以下且 Tyvaso 年增為正；或 FDA 於 2027-04 底前核准 IPF，且 2026 Q4 營收達 8.4 億美元以上","exec_line":"現價可先建小倉；2026 Q4 營收達 8.4 億美元以上加一檔，IPF 獲准再加一檔；股價超過 650 美元而 IPF 未獲准時不追。"},"reasoning":{"industry":"Q3 2026 營收 8.325 億美元，Tyvaso 5.038 億（60.5%，其中 DPI 3.785 億、年增 13%，霧化劑 1.253 億、年減 12%），Orenitram 1.45 億（17.4%），Remodulin 1.22 億（14.7%），Unituxin 5,230 萬（6.3%）。三個 treprostinil 產品合計 92.6%，這是最大的單點依賴，也是護城河本身。GAAP 營益率 37.0%，含 Thymmune 約 1.3 億美元一次性研發費，還原後約 52.6%。美國經銷只經 Accredo 與 CVS Specialty 兩家，真正決定收入的是肺高壓專科醫師的處方與付款方的給付條件。供需判斷：需求結構性持久，競品增加改變的是份額分配，不是需求週期。","moat":"執行力判穩定：過去幾季常是兩個好月配一個差月，營收沒有成長；Q3 連續月份轉好，DPI 年增 13%，10 月轉介超過 1,000 件，是單月新高。同一場法說也承認軟霧吸入器送件延到 2027、三合一口服錠的生物等效試驗不足、ralinepag 原料供應商被列 OAI。定價力判穩定：公司調價維持單位數，DPI 成長含調價，美國學名藥對 Remodulin 侵蝕有限。反面是 10-Q 明寫競品傷到霧化 Tyvaso、DPI 與 Remodulin，毛利率也從 FY2022 的 92.17% 降到 TTM 86.34%。對最強同業的 ROIC 差距事實表未涵蓋，改用營益率比：UTHR TTM 39.39%，Liquidia 37.39%（至 2026-06），差距已小；Liquidia 的數字在和解之前，PH-ILD 標籤拿掉後應會變差。可能看錯的地方：和解擋的是行銷和鼓勵標示外使用，不是醫師處方，標示外使用若沒降下來，PH-ILD 的牆就比看起來薄。","growth":"成長來源以量為主、單位數調價為輔，EPS 再由回購放大，併購只占小部分。三年共識 EPS 由 FY2025A 27.86 美元到 FY2028E 42.41 美元，年化 15.0%；內生上界 17.3%，共識沒有超過，缺口為負 2.3 個百分點。這段成長分布不平均：FY2026E 營收年增 2.1%，FY2027E 年增 10.9%，FY2028E EPS 再跳 25%。下一條曲線有來源：TETON-1、TETON-2 都達主要終點，FDA 已受理 IPF 申請，審查期到 2027 年 4 月底；ralinepag 審查日為 2027-06-24。管理層稱 IPF、PPF、PH-COPD 合計約 100 萬美國病人，滲透率事實表未涵蓋，換算不出達 30% 滲透的年數。若 IPF 未獲准，這一項要降為中等。","governance":"FCF 對淨利的轉換率 FY2022 到 FY2025 分別為 91%、76%、90%、78%，來自財報歷史。SBC 占 Q3 營收 4.9%，年化約為市值的 0.7%。回購：2026 年 3 月簽 ASR 並核准最高 20 億美元，9 月再簽 4.776 億美元 ASR，10 月 21 日再核准 20 億美元一年期計畫，相當於市值 8.4%。併購規模小：Thymmune 現金 1.4 億美元，加里程碑最高 3 億，占市值 1.25%。CFO 在 2026-11-04 法說拒絕說明買斷 Arena 的 ralinepag 權利金花了多少，這筆資本的報酬外界算不出來。現金去向四分、回購均價、10 年期公債殖利率，事實表未涵蓋。","valuation":"FY2026E 本益比 20.06 倍，分母含 Thymmune 一次性費用，還原約 31 美元後約 18 倍；FY2027E 16.58 倍；PEG 以三年 EPS 年化 15.04% 計為 1.33，落在合理區。每股現金與投資約 83 美元，占股價 14.8%。事實表的淨負債只算 20.679 億美元現金，公司公布的現金與可交易投資是 35.357 億，EV 用公司數字會低約 14.7 億。Trailing P/E 21.22 倍是 4 個年度端點的最高，但樣本只有 4 點，且 TTM 盈餘含一次性費用，不能當五年高位。TTM 營益率比 FY2025 低 8.3 個百分點，Thymmune 只解釋約 4 個百分點，其餘事實表未說明。Q3 GAAP EPS 5.71 美元，共識有 5.85 與 6.04 兩個來源。賣方目標價聚合站從 533 到 664 美元不一，最高的 664.33 美元是 8 月資料，只能算弱支持，不當錨。共識兩次快照修正都是 0%，可能還沒反映 Q3 財報。","premortem":"十項衰退訊號亮兩項，毛利率下滑與核心市占縮減，歸為中等風險，不是價值陷阱。論點失敗、股東經濟變差、價格反映太多三條路徑見反證紀錄。歷史最大回撤、空方最強數字、訴訟金額全貌，事實表未涵蓋；已知的金額只有 Sandoz 案提列的 7,410 萬美元。"},"plain":{"six":{"how_it_makes_money":"UTHR 賺的是肺動脈高壓與肺間質病變病人的長期用藥錢，九成以上來自 treprostinil 同一分子，錢卡在吸入劑型的處方決定這一節點。","moat":"護城河方向判穩定：PAH 被新機轉與同分子對手削弱，PH-ILD 因 2026 年 10 月和解重新只剩 Tyvaso 有標籤，兩邊大致抵銷。","growth":"五年後的成長空間判寬，前提是 IPF 與 ralinepag 至少拿到一張核准；FY2026E 營收只年增 2.1%，成長要靠尚未獲批的產品接手。","capital":"資金運用偏向股東：帳上無負債，現金與投資 35.4 億美元，2026 年兩度核准各 20 億美元回購；回購價位的報酬目前無法驗證。","valuation":"現價要有 10% 年化報酬，FY2031E EPS 得做到約 57 美元（年化約 15%）並維持 16 倍；這要 IPF 放量、基本盤不掉才到得了，我的 Base 只信到 13.6%。","how_wrong":"最可能看錯的是 IPF 上市後的放量速度，以及 PH-ILD 標示外使用是否真的降下來。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用過去幾季沒有成長的印象定價，FY2027E 只給 16.6 倍；PH-ILD 和解到 10 月中才定案，共識兩次快照都沒動。若快照只是尚未更新，這個理由要打折。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":562.02,"week26_return_pct":-0.52,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026E 含約 1.3 億美元一次性研發費，還原後約 31 美元，一次性項目壓低而不是墊高盈餘，便宜論證不因此失效。短期上檔用 FY2027E 33.5 美元×18 倍，中期用 FY2028E 40.5 美元×17 倍。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 Q4 財報，日期未公告","impact":"高","watch":"總營收是否達 8.4 億美元，Tyvaso 年增率，是否重申 40 億美元目標"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"FDA 對霧化 Tyvaso IPF 補充申請的審查期結束","impact":"高","watch":"是否獲准、適應症範圍、用藥限制"},{"date":"2027-06-24","date_precision":null,"type":"regulatory","event":"ralinepag PAH 新藥審查日","impact":"高","watch":"原料供應商 OAI 是否解除"},{"date":"2027-06","date_precision":"month","type":"product","event":"Orenitram 學名藥最早可上市，12 月第二家","impact":"中","watch":"Orenitram 季營收下滑幅度"},{"date":"2026-12","date_precision":"month","type":"other","event":"Adcirca 授權 2026-12-31 到期不續","impact":"低","watch":"其他收入的減少幅度"}],"_projected_from":"v19"}
```
