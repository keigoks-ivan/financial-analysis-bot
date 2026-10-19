你是 stock-analyst v20 的**散文層（prose）agent**，標的 2308.TW（2026-10-19）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261019/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：2308.TW　日期：2026-10-19　archetype：None　前份裁決：2026-05-14　B 觀望偏進場（thesis 完整 + Q1 26 GM 37% 超預期、估值透過 EPS 修正自然壓縮至 FY+2 PE 33.4x，但短中期 R:R 仍雙負，等 BB 中軌 1,500 或 Q2 法說連 2 季驗證）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2069B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（436B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1002B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1318B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1501B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（748B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（784B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2049B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4638B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2467B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2069           3452-4931      5 條（2–6 內）  
s3                  8000         436           5295-7564      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3821          7825-11179      5 條（2–6 內）  
s6                 11000         748          7176-10252      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         784           1901-2716      5 條（2–6 內）  
s10                 5000        2049           2066-2951      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2467           2000-2533      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5266B；至少需散文≈39.73KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60
−60%
−40
−40%
−23.9%
−16.5%
−13.23
−13.2%
−6.2%
0
0.42
0.66
0.7
0.71%
0.74
0.75
0.8
0.85
1%
1
1.07
1.1%
1.10
1.28
1.3
1.33
1.48
1.5%
02
2.0%
2
2%
2.3
3
3%
3.05
04
4
4%
5%
05
5
5.34
5.7
06
6
6.5
07
7%
7
7.5%
7.7%
8
8%
08
9%
9
9.5%
9.68
10
10%
11
11.35%
11.4%
11.4
11.6
12
13%
13
13.2%
14
14.6%
15
15%
15.2%
16%
16
16.5%
16.7%
16.8%
16.9
17%
17
17.59
17.7%
18
18.5%
19
19.4%
20
20%
21
22
22%
22.7%
23
23.08
23.14
23.4%
23.9%
24%
24
25
25%
25.5
25.5%
25.98
26
26.04
28
28.8%
29
30
30%
31%
32
32%
33.4
34%
34
34.3%
35%
35
35.5
35.6%
35.7%
35.9%
36%
36.4%
37
37%
38.0%
38
39%
40%
40.45
40.5
40.54
41%
42
43%
44.3
45%
45
46%
48.7%
49
50
50%
52%
52
52.3
55%
55
59%
60
61%
62
62.5
64
64.33
64.52
65%
66
70
70%
76%
77.3%
78
80%
82%
90%
90
95%
97
97.14
100
100%
108
110
120
140
150%
158
166
200
251
267
269
283
300
337
365
413%
433
443
466
478
601
629.4
650
700
780
800
820
843
879
880
940
990
1640.0
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
2155.0
2301
2308
20261019
1,040
1,119
1,179
1,337
1,350
1,500
1,640
1,794
1,832.6
1,930
1,965
2,155
2,200
2,217
2,369
2,505
4,211
4,424
5,549
7,766
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
{"meta":{"ticker":"2308.TW","date":"2026-10-19","schema":"v15.2","contract":"v19","company_name":"台達電子"},"oneliner":"台達電是 AI 伺服器電源與液冷龍頭，股價較前份跌 24%，2027 年共識本益比降到 25.5 倍；但缺料壓毛利、大客戶多源化與 337 專利調查同時出現，等第三季法說確認毛利率與第四季出貨回補再進場","thesis":{"H":[{"id":"H1","text":"AI 資料中心需求帶動 2027 年營收再成長三成以上，第三季降速是缺料遞延，不是需求轉弱","2y":"2027 年合併營收 ≥1 兆元（共識約 1.10 兆），第四季單季營收季增 ≥10% 驗證遞延回補","5y":null,"10y":null,"threshold":"月營收年增率自 2026 年 11 月起回到 ≥25%；2027 年全年營收年增 ≥30%；輔助門檻：基礎設施部門季營收年增 ≥30%（前份門檻保留，本期數字事實表未涵蓋，標資料缺口）","source":"公司月營收公告、季度法說簡報；2026-10 優分析把第三季降速歸因於電源 IC、PMIC、MOSFET 缺料","drift_rule":"2 年期規則：實績偏離門檻連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"零組件漲價與缺料只是過渡，合併毛利率守住 35% 以上，營業利益率回到 17% 以上","2y":"2027 年四季毛利率皆 ≥35%，全年營業利益率 ≥17%","5y":null,"10y":null,"threshold":"每季合併毛利率 ≥35%；2027 年營業利益率 ≥17%","source":"季度法說簡報；2Q26 毛利率 35.6%、營業利益率 16.7%（共識 36.4%、18.5%）","drift_rule":"連 2 季毛利率 <35% 視為削弱；連 3 季 <34% 視為反轉"},{"id":"H3","text":"台達在 800V 高壓直流電源機櫃世代維持主要供應商地位，客戶多源化之後伺服器電源份額仍在 5 成以上","2y":null,"5y":"2031 年基礎設施部門營收占合併 ≥40%，電源機櫃與高壓直流成為最大單一產品線","10y":null,"threshold":"2027 年起高壓直流與電源機櫃開始大量貢獻（管理層時程）；主要 AI 平台電源供貨比 ≥50%（目前法人估約 7 成）","source":"2025 年第四季、2026 年第一季法說管理層時程；凱基 2026-04 指台達可望為 VR200 首家通過認證的 12kW 電源供應商；經濟日報供貨比報導","drift_rule":"5 年期規則：連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"功率半導體缺料與零組件漲價持續，出貨遞延並壓毛利","h_ref":"H1,H2","clock":"⚡","threshold":"毛利率連 2 季 <35%，或 10–11 月營收年增 <15%","evidence_refs":["supply_demand_durability#4","end_markets#2","capital_markets_pricing#3","capital_markets_pricing#4","capital_markets_pricing#0","capital_markets_pricing#1"]},{"id":"R2","text":"大客戶主動多源化，電源與液冷份額由高點回落並帶動降價","h_ref":"H3","clock":"🔥","threshold":"法人估大型 AI 客戶電源供貨比 <50%，或連 4 季毛利率低於 35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3"]},{"id":"R3","text":"Vicor 專利引發的美國 337 調查，最壞情況是垂直供電相關產品被排除進口美國","h_ref":"H3","clock":"🔥","threshold":"USITC 初步裁定侵權並建議排除令（預計 2027 年第四季前後）","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]},{"id":"R4","text":"關稅與地緣：報導稱美國營收占比逾三成，液冷部分零組件關稅可能自行吸收，產能過去集中中國","h_ref":"H2","clock":"🐢","threshold":"公司歸因關稅的毛利率下滑 >200 個基點，連 4 季","evidence_refs":["reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#1","customer_concentration_credit#2"]},{"id":"R5","text":"AI 資本支出 2028 年進入消化期，同時非 AI 業務（電動車、自動化）仍弱，接不了棒","h_ref":"H1","clock":"🐢","threshold":"2027 年共識 EPS 跌破 55 元，或主要雲端業者 2028 年資本支出指引年減","evidence_refs":["channel_business_model_shift#3"]}],"single_thing":{"description":"輝達 800V 高壓直流世代（2027 年量產）的電源主供落到他家，台達降為第二供應商","why_fatal":"2027 年共識 EPS 年增約 59% 的最大來源是伺服器電源與高壓直流電源機櫃；主供易手後份額可能由約 7 成降到 3–4 成，推估 2027 年 EPS 下修 20–25%，倍數同時從成長股降到電源代工水位","if_happens":"清倉並重跑判斷；Bear 情境機率上調至 50% 以上","how_monitor":"輝達平台電源認證公告、法人供貨比估計、2026 下半年高壓直流小量出貨進度、2027 年月營收","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":25.5,"peg_fy2":0.42,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":23.08,"FY2026E":40.45,"FY2027E":64.33,"FY2028E":97.14},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（台達電無 non-GAAP 口徑）；共識為 Koyfin 美元值依 2026-10-08 匯率換算新台幣"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2308.TW_20261019/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利電源轉換龍頭，獲利被 AI 資本支出週期放大"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性為主：需求來自超大型雲端業者 AI 資本支出（方向結構性），當下瓶頸是電源 IC、PMIC、MOSFET 缺料，供給可逆性高；依據為 2026-07 凱基報告與 2026-10 第三季降速歸因報導","bargaining":{"up":"上游功率半導體部分料號交期逾六個月、零組件漲價壓毛利，上游議價力上升","down":"客戶極度集中且主動找第二、第三供應商，董事長自承份額不會維持這麼高，下游議價力上升","geo":"產能分布中國、台灣、泰國、印度、斯洛伐克，擴產重心轉往泰國；管理層稱超過 95% 業務以 FOB 交貨、關稅多由客戶負擔，但法人估液冷部分零組件關稅需自行吸收"},"profit_pool_dir":"利潤池往系統層移動（電源機櫃、高壓直流、液冷整合），台達往上整合；但到了系統層，對手換成 Vertiv、Eaton 這類國際基礎設施廠","tam_table":{"expanded":false,"reason":"事實表未涵蓋 AI 電源、液冷、高壓直流的市場規模與滲透率數字；高壓直流屬新品類，但證據包只有管理層定性時程，沒有規模可填"}},"moat":{"mechanism":"電源轉換效率＋平台世代認證＋量產規模；產品廣度讓台達能從單顆電源一路整合到整座電源機櫃","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：毛利率 2022 年 28.8% 到 TTM 35.7%，2026 年資本支出約 700 億元擴產；定價面縮減：客戶找第二、第三供應商，董事長表示份額不會維持這麼高，第二季毛利率低於共識 0.8 個百分點。兩向相抵判穩定","threats":[{"level":"🟡","text":"客戶主動多源化：大型 AI 客戶的電源與液冷開始找第二、第三供應商，台達份額由高點回落，液冷最大專案傳出流失小部分份額，另有公司未證實的掉單傳聞","p":"70%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3"]},{"level":"🔴","text":"高壓直流世代由國際基礎設施廠（Vertiv、Eaton 等）以機房到機櫃整套供電方案切入，台達從整合者退為零組件供應商；本輪事實表未涵蓋對手新訂單證據，沿用為結構性威脅","p":"35%","evidence_refs":[]},{"level":"🟡","text":"Vicor 專利引發美國 337 調查，涉及垂直供電系統，最壞情況是相關產品被排除進口美國；審理約 12–18 個月，二手來源指雙方前次爭議在 2025 年 5 月和解","p":"20%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（稅後營業利益率約 13%，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是 AI 伺服器、決策者是輝達平台與雲端業者、付款者多為組裝廠，三角色都成立；電源是必需品不是想要，但出貨量綁 AI 資本支出節奏，急迫性不等於持久性。代理讀數：2026 年 9 月營收年增降到 14.6%，報導歸因缺料遞延而非砍單，尚待第四季驗證"},{"item":"決策層級","level":"🟡","text":"替代性要在每一代平台的電源認證層看：約每年一次重新認證，等於每年給客戶一次換供應商的窗口；執行長證實客戶已在找第二、第三家。轉換成本存在但不長，靠的是每一代都先過認證"},{"item":"價值鏈分配","level":"🟡","text":"整座 AI 機櫃的經濟利益主要被運算晶片端拿走，電源占採購金額小；台達毛利率五年由 28.8% 升到 35.7%，代表多分到一些，但上游功率半導體交期逾六個月、零組件漲價，下游客戶高度集中又主動多源化，兩頭都在擠"},{"item":"社會容忍度","level":"🟢","text":"產品功能是提升能源轉換效率、降低資料中心耗電，社會敏感度低，不靠監管授權；政策風險在關稅與出口管制（報導稱美國營收占比逾三成），屬地緣風險而非定價上限"}],"roiic":"約 65%（2024→2025 實績，含利潤率擴張）；剔除週期成分保守取 40%","reinvest_rate":"約 80%（2026 年推估）","endo_ceiling":32,"formula_note":"增量報酬：營業利益 2024 年約 478 億（4,211 億×11.35%）到 2025 年約 843 億（5,549 億×15.2%），增 365 億，稅率 22.7% 後增約 283 億；增量資本＝2025 年資本支出約 466 億減折舊約 300 億（以 2025 年 EBITDA 1,179 億減稅前利益 879 億推估）＝166 億，加營運資金增量（事實表未涵蓋，假設為新增營收 1,337 億的 20%＝267 億），合計約 433 億，得約 65%，再扣除利潤率擴張的週期成分保守取 40%。再投資率：2026 年資本支出 650–700 億減折舊約 300 億，加營運資金增量（同一假設，新增營收約 2,217 億×20%＝443 億），合計約 820 億，除以稅後營業利益約 990 億（共識營收 7,766 億×16.5%×77.3%），約 80%。內生上界＝40%×80%＝32%。折舊與營運資金皆為推估，只能當量級參考"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","2308.TW":35.69,"VRT":38.04,"ETN":35.9,"2301.TW":23.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","2308.TW":16.78,"VRT":19.4,"ETN":17.71,"2301.TW":11.41,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","2308.TW":11.7,"VRT":25.47,"ETN":13.1,"2301.TW":-6.21,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","2308.TW":8.65,"VRT":null,"ETN":2.81,"2301.TW":5.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"VRT","gm":38.04,"om":19.4,"fcf_margin":25.47,"rd_intensity":null,"strategy_note":"毛利率 38.0%、自由現金流利潤率 25.5% 都高於台達，強項是熱管理加電力系統整合；高壓直流電源機櫃世代是它與台達正面交鋒的戰場","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ETN","gm":35.9,"om":17.71,"fcf_margin":13.1,"rd_intensity":2.81,"strategy_note":"毛利率 35.9%、營業利益率 17.7% 與台達相當，強在電網端與配電，固態變壓器與機房供電整合是潛在交集","period":"TTM ending 2026-06-30（4季加總）"},{"name":"2301.TW","gm":23.4,"om":11.41,"fcf_margin":-6.21,"rd_intensity":5.3,"strategy_note":"光寶毛利率 23.4%、自由現金流利潤率 −6.2%，用價格與擴產搶第二供應商位置，是客戶多源化最直接的受益者，但利潤率差距顯示它在成本與產品組合上仍追不上台達","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（AI 伺服器電源、液冷出貨量），價靠電源機櫃與高壓直流整合提高單機價值；併購與回購貢獻可忽略","runway_years":7,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 32%＝增量報酬保守 40%×2026 年再投資率約 80%，推導見護城河段的報酬持續期說明","segments":[{"item":"電源及零組件","value":"約 50%（2026 年 6 月單月營收比重）；其中伺服器電源占合併營收約 30%（2Q26，凱基），2025 年部門營收年增 25%、利潤年增 37%"},{"item":"基礎設施（資料中心電源系統、液冷）","value":"約 37%（2026 年 6 月）；2Q26 營收 629.4 億元；2025 年營收年增 82%、利潤年增 413%，是利潤成長主引擎"},{"item":"自動化","value":"約 8%；2025 年利潤年減 39%，管理層稱中國市場觸底但未見強勁回升"},{"item":"交通（電動車）","value":"約 5%；2025 年營收年減 16% 且轉虧，公司視需求在 AI 與電動車間調度產能"}],"decay_signals":["核心份額近 12 個月縮減：大客戶多源化、液冷最大專案流失小部分份額","共識 EPS 年化（約 61%）高於營收年化（約 41%）逾 5 個百分點"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能而非併購撐起，現金去向以資本支出與配息為主；四分拆解所需的三年現金流量表細項事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年併購（日本射頻電源公司、晶睿股份轉換）的併購後報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"台達電不做庫藏股回購，股東回饋以現金股利為主","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"流通股約 25.98 億股，與 2025 年淨利÷EPS 推得的約 26.04 億股相當，年稀釋率低於 1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（2027 年共識 EPS 64.33 元）","tier":"AI 資料中心電源與散熱系統供應商","peers":{"expanded":false,"reason":"事實表未涵蓋同業前瞻本益比，同業只有毛利率、營業利益率與自由現金流利潤率可比"},"fwd_pe":40.54,"peg":0.66,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"2027 年本益比 25.5 倍低於一家賣方 9 月採用的 35 倍，但現價已大致反映基準情境（年化約 8%）；Trailing 倍數在近四年最高位置、2028 年共識過度樂觀、337 與份額風險尚未落地，三者抵銷便宜感，結論為合理區","upside_short_pct":9,"upside_mid_pct":34},"trap_analysis":{"verdict":"🟡","label":"成長延續但份額與毛利受壓"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"法人估大客戶電源供貨比已到約 7 成，執行長證實客戶在找第二、第三供應商；9 月營收年增降到 14.6%，市場流傳掉單傳聞","assumption":"第三季降速只是缺料遞延，第四季會回補","consequence":"若其實是份額開始流失，2027 年 EPS 會落在 52–55 元而非 64 元，倍數同時壓到 16–18 倍，五年後虧近五成","ruling":"部分採納：缺料有凱基與優分析兩方佐證，掉單只有傳聞；但份額回落方向已確定，因此 Bear 機率給 30%，基準情境 2027 年 EPS 用 60 元而非共識","watch":"10–11 月營收年增率、第三季毛利率、法人對大客戶供貨比的更新","evidence_refs":["competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3","end_markets#2"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年資本支出由 466 億元拉到約 700 億元；第二季毛利率 35.6% 比共識低 0.8 個百分點，外資指零組件成本持續壓毛利；法人估液冷部分零組件關稅需自行吸收","assumption":"營收成長會轉成同比例的自由現金流","consequence":"營收照成長，但毛利率卡在 34–35%、自由現金流÷淨利跌破 0.75，股東拿到的現金報酬遜於 EPS 成長","ruling":"採納：列為第二條假設的檢驗，毛利率連 2 季低於 35% 就減碼","watch":"每季毛利率、年度自由現金流÷淨利","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4","supply_demand_durability#4","reg_tariff_export#1"],"fact_refs":["f_kpi1","f_kpi5","f_kpi6_2026"]},{"view":"價格已反映太多","evidence":"Trailing 本益比 52.3 倍、P/S 6.5 倍都在近四個年度端點最高位置；2028 年共識 EPS 97 元隱含三年年化約 61%；賣方 7 月與 9 月連續下修目標價","assumption":"2027 年本益比 25.5 倍已經便宜","consequence":"若 2028 年共識下修到我的基準 78 元，現價對應 2028 年本益比 21 倍，並不便宜","ruling":"部分反駁：股價已較前份跌 24%，2027 年倍數從 33.4 倍降到 25.5 倍，再跌的空間主要來自 EPS 下修而非倍數；但現價大致只反映基準情境，不構成安全邊際","watch":"共識 2027、2028 年 EPS 修正方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_pe_current","f_pe_percentile","f_consensus_eps_fy3"]},{"view":"論點失敗","evidence":"美國 ITC 337 調查涉及垂直供電系統，台達與兩家美國子公司列名；另有報導稱美國營收占比逾三成，產能過去約七成在中國；2025 年 2 月美墨關稅曾讓股價盤中跌約 9%","assumption":"337 會像前次一樣和解或改設計，關稅可轉嫁客戶","consequence":"若裁定侵權並發排除令，相關直流轉換產品無法進口美國，伺服器電源份額直接受損","ruling":"暫不採納為主情境：審理約 12–18 個月，二手來源指前次已和解，公司稱產品目前未受影響；列入風險與觸發器追蹤","watch":"USITC 初步裁定、和解公告、公司歸因關稅的毛利率變化","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","lawsuit_class_action#0","reg_tariff_export#2","geo_supply_chain#1","customer_concentration_credit#2"],"fact_refs":[]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 2155.0 → 本次 1640.0（-23.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=2155.0","side_b":"本次 price_at_dd=1640.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 2,155 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 2,155 元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 2,155 元：Bull 價 4,424、Bear 價 880，五年期望值 +13.2%，基準年化 2.0%，不對稱比 1.48","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.48。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 2,155 元：五年期望值 +13.2%，基準年化 2.0%，不對稱比 1.48","side_b":"本次情境、股價 1,640 元：五年期望值 +48.7%，基準年化 7.7%，不對稱比 3.05","ruling":"再換股價、情境不動：起點價下跌 23.9%，五年期望值多 35.5 個百分點，基準年化多 5.7 個百分點，不對稱比由 1.48 升到 3.05。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與情境機率","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-05-14 股價 2,155 元、2027 年本益比 33.4 倍，估值判為中性；情境機率與最大回撤未填","side_b":"本次 1,640 元、2027 年本益比 25.5 倍，估值仍判中性；Bull 25%、Base 45%、Bear 30%，最大回撤 −40% 到 −60%","ruling":"股價跌 24% 讓倍數變便宜，但同期新增 337 調查、份額回落與毛利未達共識，下檔情境加寬，抵銷後估值結論不變","evidence_level":"事實表價格與共識","settle_metric":"2027 年共識 EPS 與本益比","if_then":["若 2027 年共識 EPS 守住 62 元以上且股價跌到 1,350 元以下（約 21 倍），則估值轉入便宜區、分批反買","若 2027 年共識 EPS 跌破 55 元，則即使股價不動，倍數也回到約 30 倍，估值轉貴、不建倉"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"品質評級、陷阱與護城河方向","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份品質評級 B、陷阱風險中度、護城河方向未填","side_b":"本次品質評級 B、陷阱風險中度、護城河方向穩定","ruling":"評級與陷阱結論不變但理由更新：前份靠第一季毛利率 37% 超預期，本次第二季毛利率回到 35.6%，客戶多源化與液冷份額流失有多方報導；執行力擴大與定價力縮減相抵，方向判穩定而非上升","evidence_level":"公司法說＋法人報告＋媒體報導","settle_metric":"每季毛利率、大客戶電源供貨比","if_then":["若連 2 季毛利率 <35% 且法人估大客戶供貨比降到 5 成以下，則護城河方向改判下降、減碼至半倉","若第三、第四季毛利率回到 36% 以上，則維持穩定判斷"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","capital_markets_pricing#3"]},{"axis":"新增判斷欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position"],"side_a":"前份這些欄位為空白","side_b":"本次：成長跑道中等、類型為品質複利成長（次類循環）、循環位置中循環；裁決與角色由決策矩陣推出","ruling":"屬判斷框架新增欄位，不是基本面改變","evidence_level":"方法","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件欄（裁決文字寫等布林通道中軌 1,500 元或第二季法說連 2 季驗證）","side_b":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","ruling":"改用事件錨、不設價格：前份的技術錨 1,500 元未觸及，真正卡住的是毛利與出貨回補兩件事，該等的是證據不是價位","evidence_level":"方法＋公司法說","settle_metric":"第三季毛利率、10 月營收年增率","if_then":["若兩條件同時成立，則重跑判斷並建首倉 2%","若股價先漲但證據未到，則不追"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"輝達 800V 高壓直流世代的電源主供落到他家，台達降為第二供應商","ruling":"前份沒有這一欄；本次依敏感度選定：2027 年共識 EPS 年增約 59% 的最大來源是伺服器電源與高壓直流，主供地位是數學上最大的單一變數，影響範圍比 337 排除令大；發生即清倉","evidence_level":"法人報告＋管理層時程","settle_metric":"輝達平台電源認證與主供公告","if_then":["若確認台達失去主供，則清倉並重跑判斷","若台達取得 VR200 首家 12kW 認證並量產，則此風險降級"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"清倉與減碼門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（空白）","side_b":"毛利率連 2 季 <35% 減碼至半倉、連 2 季 <34% 列失效；月營收年增連 3 個月 <10%；大客戶電源供貨比 <5 成減碼；337 初步裁定侵權減碼一半；2027 年共識 EPS <55 元減碼至 1/3 以下；主供易手清倉","ruling":"新增門檻是回應本輪新證據：第二季毛利率未達共識、9 月營收年增降到 14.6%、337 立案","evidence_level":"公司法說＋月營收＋ITC 立案報導","settle_metric":"同上門檻","if_then":["若任一門檻觸發，則依該門檻的減碼或清倉動作執行並重跑判斷"],"evidence_refs":["end_markets#2","regulatory_antitrust#0"]},{"axis":"假設與風險門檻","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：基礎設施年增 ≥30% 連 6 季、合併毛利率 ≥35%、2027 年本益比 ≤38 倍；Vertiv 取得輝達 Rubin 主供則論點削弱","side_b":"本次：月營收年增自 11 月回到 ≥25%、第四季季增 ≥10%，基礎設施年增 ≥30% 保留為輔助門檻；毛利率 ≥35%、2027 年營業利益率 ≥17%；高壓直流世代主要平台供貨比 ≥5 成；新增 337 與缺料兩條風險","ruling":"毛利率 35% 門檻保留；基礎設施年增門檻保留但本期部門年增數字事實表未涵蓋，標資料缺口，主檢驗改用合併月營收；本益比 38 倍門檻退休，因股價已跌到 25.5 倍、不再是約束；Vertiv 風險移到護城河威脅，本輪無新證據","evidence_level":"公司法說＋月營收＋法人報告","settle_metric":"月營收、每季毛利率","if_then":["若門檻連 2 季未達，則依觸發器減碼"],"evidence_refs":["end_markets#2","supply_demand_durability#4"]},{"axis":"管理層說法與實績","cause":"新證據","prior_field":null,"side_a":"2026 年 7 月法說董事長：產能與物料掌握尚稱穩定，下半年營運優於上半年","side_b":"第三季營收季增 7.5%，但 9 月年增降到 14.6%，降速歸因電源 IC、PMIC、MOSFET 缺料；第二季毛利率與營業利益率低於共識；賣方 7 月與 9 月兩度下修目標價","ruling":"可調和（程度差異）：下半年營收仍高於上半年，管理層說法字面成立，但缺料影響比描述大；採信缺料遞延，但用第四季回補驗證，不靠管理層措辭","evidence_level":"月營收＋法人報告","settle_metric":"第四季營收季增率、10–11 月營收年增率","if_then":["若第四季營收季增 ≥10%，則採信遞延說法","若第四季營收季增 <5%，則判定不只缺料，2027 年 EPS 錨下修至 55 元並減碼"],"evidence_refs":["end_markets#2","supply_demand_durability#4","capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價較前份跌 24%、11 天內跌 16.5%，但 2027 年共識 EPS 幾乎沒動（64.52 到 64.33）；2027 年本益比 25.5 倍低於賣方 35 倍；淨現金約 1,119 億；Vicor 前次爭議已和解","side_b":"第三季法說預計 10 月底（日期事實表未涵蓋，依前兩季 4 月底、7 月底推估），毛利率與第四季展望是當前唯一約束；等這段時間的成本，小於在份額與缺料未明時買進的風險","ruling":"選 B 側：不是不看好，而是決勝數據即將出現；觀望的約束只有一個，就是第三季毛利率與出貨回補","evidence_level":"事實表價格與共識","settle_metric":"第三季毛利率、10 月營收年增率","if_then":["若第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，則重跑判斷後建首倉 2%","若股價先反彈到 1,965 元以上而證據未到，則不追","若跌到 1,350 元以下而基本面門檻未破，則分批反買"],"evidence_refs":["regulatory_antitrust#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：AI 資料中心需求讓產能吃緊，2026 年資本支出由 466 億拉到約 700 億，6 月營收年增 55% 創高","side_b":"競爭惡化：客戶多源化、液冷份額流失；其他結構變數：337 專利調查、關稅與產地分散、電動車業務處於修正期","ruling":"雙向拉鋸：結構順風仍在，但競爭與法規兩軸同時轉負，份額高點已過","evidence_level":"公司法說＋媒體＋ITC 立案報導","settle_metric":"大客戶供貨比、337 初步裁定","if_then":["若供貨比守在 5 成以上且 337 和解，則改判結構性轉好中","若供貨比跌破 5 成，則改判競爭惡化中並減碼"],"evidence_refs":["competitive_share_entrants#2","regulatory_antitrust#0","channel_business_model_shift#3"]}],"triggers":[{"n":1,"text":"第三季法說毛利率確認","type":"假設驗證","maps_to":"H2","metric":"2026 年第三季合併毛利率","threshold":"≥35%","action":"達標且 10 月營收年增 ≥20% 則重跑判斷建首倉；未達則續觀望","source_freq":"季度法說","date":"2026-10","evidence_refs":["capital_markets_pricing#3"]},{"n":2,"text":"第四季遞延訂單回補","type":"假設驗證","maps_to":"H1","metric":"10–12 月合併營收年增率與第四季季增率","threshold":"月營收年增自 11 月起 ≥25%；第四季季增 ≥10%","action":"未達則 2027 年 EPS 錨下修至 55 元重算","source_freq":"每月 10 日前後月營收","date":"2026-11","evidence_refs":["end_markets#2"]},{"n":3,"text":"缺料與零組件成本壓毛利","type":"減碼","maps_to":"R1","metric":"合併毛利率","threshold":"連 2 季 <35%","action":"減碼至半倉並停止加碼","source_freq":"季度法說","date":null,"evidence_refs":["supply_demand_durability#4","capital_markets_pricing#4"]},{"n":4,"text":"客戶多源化侵蝕份額","type":"風險","maps_to":"R2","metric":"法人估大型 AI 客戶電源供貨比","threshold":"<50%","action":"減碼至半倉，護城河方向改判下降並重跑判斷","source_freq":"法人報告與媒體（不定期）","date":null,"evidence_refs":["competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#3"]},{"n":5,"text":"337 專利調查裁定","type":"風險","maps_to":"R3","metric":"USITC 初步裁定","threshold":"裁定侵權並建議排除令","action":"減碼一半；和解或改設計則解除","source_freq":"USITC 案卷（不定期）","date":"2027-10","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]},{"n":6,"text":"輝達高壓直流世代主供易手","type":"Single Thing","maps_to":"Single Thing","metric":"輝達 800V 平台電源主供名單","threshold":"台達不是主供","action":"清倉並重跑判斷","source_freq":"法人報告、平台發表（不定期）","date":"2027","evidence_refs":["competitive_share_entrants#0"]},{"n":7,"text":"證據到位後進場","type":"估值rearm","maps_to":"H1,H2","metric":"第三季毛利率與 10 月營收年增率","threshold":"毛利率 ≥35% 且 10 月營收年增 ≥20%","action":"重跑判斷後建首倉 2%；股價先漲證據未到則不追","source_freq":"季度法說＋月營收","date":"2026-11","evidence_refs":[]},{"n":8,"text":"基本面未破的深跌","type":"加碼","maps_to":"H3","metric":"股價與 2027 年共識 EPS","threshold":"股價 ≤1,350 元且 2027 年共識 EPS ≥62 元","action":"分批反買，每次 1%，上限 4%","source_freq":"每日股價＋每月共識快照","date":null,"evidence_refs":[]},{"n":9,"text":"AI 資本支出降溫與共識下修","type":"減碼","maps_to":"R5","metric":"2027 年共識 EPS","threshold":"<55 元","action":"減碼至 1/3 以下並重跑判斷","source_freq":"每月共識快照","date":null,"evidence_refs":["channel_business_model_shift#3"]},{"n":10,"text":"年度複審","type":"複審日期","maps_to":null,"metric":"2026 年全年財報與 2027 年資本支出指引","threshold":"到期即複審","action":"重跑完整判斷","source_freq":"年度法說","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"合併毛利率（季）","bear_threshold":"連 2 季 <34%","window":"2026Q3–2027Q2","source":"公司季度法說簡報","last_status":"ok"},{"metric":"合併月營收年增率","bear_threshold":"連 3 個月 <10%","window":"2026-10～2027-06","source":"公司月營收公告","last_status":"warning"},{"metric":"大型 AI 客戶電源供貨比（法人估）","bear_threshold":"<50%","window":"2027 年底前","source":"法人報告／經濟日報","last_status":"unknown"},{"metric":"USITC 337 調查初步裁定","bear_threshold":"裁定侵權並建議排除令","window":"2027-10～2028-04","source":"USITC 案卷","last_status":"warning"},{"metric":"2027 年共識 EPS","bear_threshold":"<55 元","window":"2027-06 前","source":"Koyfin 共識快照","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把缺料造成的出貨遞延與 337 立案，當成需求轉弱與出口禁令來定價，11 天跌 16.5%；但 2027 年共識 EPS 幾乎未動，337 也還沒有任何裁定"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-13.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='✅'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等第三季法說毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"首倉 2%，證據確認後上限 4%（最大回撤可能超過五成，需有深回撤心理準備）","requires_critic":[],"rearm_trigger":"第三季毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立後重跑判斷再建首倉","exec_line":"兩條件成立：重跑判斷、首倉 2%；第三季毛利率 <35% 或第四季季增 <5%：2027 年 EPS 錨下修至 55 元重算、不建倉；股價先漲證據未到：不追；跌到 1,350 元以下且 2027 年共識 EPS 守住 62 元：分批反買"},"reasoning":{"industry":"2Q26 營收 1,832.6 億元、毛利率 35.6%、營業利益率 16.7%，但毛利率比共識低 0.8 個百分點、營業利益比共識低 9.5%，稅後 EPS 9.68 元靠業外收益 44.3 億撐住才高於共識。部門結構（2026 年 6 月單月）：電源及零組件約 50%、基礎設施約 37%、自動化約 8%、交通約 5%；伺服器電源占合併營收約 30%（凱基，2Q26），液冷 2025 年約占 9%。超過一成的分部只有電源及零組件與基礎設施兩塊，兩塊都吃 AI 資料中心。客戶集中度公司不揭露，報導點名輝達、Google、Meta 與廣達、鴻海、緯創等組裝廠；單點依賴是輝達平台的電源認證，這既是護城河證據（凱基指台達可望為 VR200 首家通過 12kW 電源認證），也是集中度風險。產業時鐘在擴張期：2026 年資本支出由 466 億元拉到約 700 億元，泰國三座新廠去年底上線後管理層仍說產能吃緊，依據是訂單與擴產，不是股價。供需耐久度判為週期性為主：需求方向是結構性的，但當下限制是功率半導體交期逾六個月，這類供給瓶頸可逆性高，一旦解除，客戶多源化與價格競爭會接手。","moat":"機制是電源轉換效率加上平台認證：每一代輝達平台的電源都要重新認證，台達憑產品廣度（交流電源、直流轉換、液冷、電源機櫃）與量產規模拿到首發。事實表未涵蓋同業投入資本，可證方向改用利潤率對照：TTM 毛利率 35.7%，對直接對手光寶 23.4% 領先 12 個百分點，對 Eaton 35.9% 相當，對 Vertiv 38.0% 落後 2.3 個百分點；營業利益率 16.8%，對 Vertiv 19.4%、Eaton 17.7%、光寶 11.4%。自身毛利率 2022 年 28.8%、2025 年 34.3%、TTM 35.7%，持續擴大。執行面判擴大：2025 年營收年增 32%、2026 年前 8 月年增 41%，資本支出擴約五成。定價面判縮減：法人估大客戶電源供貨比由約 5 成升到約 7 成，但執行長說客戶已感不安、開始找第二第三家，董事長說份額不會維持這麼高；液冷最大專案傳出流失小部分份額；第二季毛利率低於共識。領先者在最大客戶的份額已有下滑證據，不能標上升。執行 8 分、定價力 6 分。","growth":"成長以量為主（伺服器電源 1Q26 年增逾 90%、占營收 31%），價靠系統整合提高單機價值，併購與回購貢獻小。共識 EPS：2025 年實際 23.08 元、2026 年 40.45 元、2027 年 64.33 元、2028 年 97.14 元，三年年化約 61%（Koyfin 快照，家數未揭露；營收共識 21 位分析師）。內生上界約 32%，缺口約 29 個百分點：一部分可歸因營業利益率由 15.2% 往 17% 以上擴張，以及 2025 年第四季資產打銷壓低基期；其餘無法歸因，依賴 AI 需求週期延續與估值不下修，因此長期信心上限為中。2026 年共識營收 7,766 億隱含第四季營收約 2,369 億、季增約 20%，需要第三季遞延訂單在第四季回補才做得到。滲透率事實表未涵蓋，跑道年數以管理層時程推：高壓直流 2027 年主貢獻、固態變壓器最慢 2027 年爆發、燃料電池客戶仍是電力公司，第二曲線有時程但沒有營收證據，判中等。衰退信號亮兩個：核心份額近 12 個月縮減，以及共識 EPS 年化（約 61%）高於營收年化（2025→2027 年約 41%）逾 5 個百分點。","governance":"自由現金流÷淨利：2022 年 0.74、2023 年 1.28、2024 年 1.07、2025 年 0.85（年度財報推算），2Q26 單季自由現金流 269 億對淨利 251 億約 1.07。2025 年每股配息 11.6 元對 EPS 23.14 元，配息率約 50%，TTM 殖利率 0.71%。現金去向：資本支出（2025 年 466 億、2026 年約 700 億）、配息、併購（日本射頻電源公司、晶睿股份轉換每股現金 100 元，金額事實表未涵蓋），沒有回購。流通股約 25.98 億股，2025 年淨利 601 億÷23.08 元約 26.04 億股，未見稀釋；員工股票酬勞事實表未涵蓋。管理層對 2026 年資本支出改口三次：2025-10-30 法說說與 2025 年相近，2026-02-26 法說說略高，7 月再上調到 650–700 億，反映需求超預期，也代表 2026 年自由現金流÷淨利可能跌破 0.75。營運槓桿：2025 年營收年增 32%、營業利益年增 76%，為正向。","valuation":"前瞻本益比：2026 年 40.5 倍、2027 年 25.5 倍、2028 年 16.9 倍；Trailing 52.3 倍、P/S 6.5 倍，都在近四個年度端點的最高位置（這不是五年分位，五年分位事實表未涵蓋）。前瞻 EV/S 5.34 倍。PEG 以共識三年 EPS 年化約 61% 計約 0.66，看似便宜，但 2028 年共識 97 元偏樂觀；改用我的基準（2026→2029 年化約 30%）PEG 約 1.33，屬合理。股價在 10-08 快照時 1,965 元，11 天內跌到 1,640 元（−16.5%），期間有 337 調查立案與第三季營收降速；26 週報酬 −13.2%、RSI 37，不過熱。共識 2026 年 EPS 近三個月下修 1.1%；賣方 7 月底目標價 1,930–2,505 元，9 月一家降到 2,200 元（35 倍 2027 年 EPS 62.5 元），全距約 1.3 倍。12 個月上行以 2028 年基準 EPS 78 元×23 倍＝1,794 元計約 +9%；三年以 2030 年基準 EPS 100 元×22 倍＝2,200 元計約 +34%。","premortem":"價值陷阱風險亮兩個信號（份額縮減、EPS 成長遠超營收成長），判中度。看錯方向一（太保守）：若第四季遞延訂單如期回補、2028 年共識 97 元成真，現價只有約 17 倍 2028 年本益比，偏多情境年化逾 20%。看錯方向二（太樂觀）：2028 年雲端業者資本支出消化，同時客戶把電源份額分給第二供應商，EPS 在 2027 年見頂約 55 元、倍數壓到 16 倍，五年跌約 46%；最大回撤範圍 −40% 到 −60%。法說問答迴避紀錄：2025-10-30 法說被問明年 AI 營收占比、毛利率走向、美國製造成本是否改觀，都沒給數字或直接回答；2026-02-26 法說拒絕拆分 AI 與傳統伺服器電源、GPU 與 ASIC 平台，份額變化只能從法人報告間接追蹤。"},"plain":{"six":{"how_it_makes_money":"賺 AI 資料中心建置的錢：超大型雲端業者經由輝達平台與組裝廠向台達買電源與散熱，錢卡在電源轉換效率與平台認證這一節點，當下瓶頸是上游功率半導體供給","moat":"護城河 B 級、方向穩定：規模與產品廣度的領先還在擴大，但大客戶主動多源化讓定價力縮減，兩向相抵","growth":"成長跑道中等：AI 電源與液冷還在放量，高壓直流電源機櫃 2027 年才進入主要貢獻，固態變壓器與燃料電池只有管理層時程；共識三年 EPS 年化約 61%，遠高於內生上界約 32%","capital":"資本配置穩健、不靠回購：淨現金約 1,119 億元、配息率約五成，但 2026 年資本支出跳增約五成到 650–700 億元，自由現金流轉換會下降","valuation":"現價 1,640 元隱含 2031 年 EPS 約 110 元、終端 22 倍才有年化約 8%，與我的基準情境相當；不算貴也不便宜，便宜論證要靠 2027 年共識 EPS 64 元站得住","how_wrong":"最可能看錯在兩處：把缺料遞延當成需求轉弱而過度保守，或低估客戶多源化與 AI 資本支出降溫同時發生時的毛利與份額下滑"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把缺料造成的出貨遞延與 337 立案，當成需求轉弱與出口禁令來定價，11 天跌 16.5%；但 2027 年共識 EPS 幾乎未動，337 也還沒有任何裁定","momentum_overheated":false,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等第三季法說毛利率 ≥35% 且 10 月營收年增 ≥20%，兩者同時成立","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":1640.0,"week26_return_pct":-13.23,"consensus_rev_3m_pct":-1.12,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母採 2027 年共識 EPS 64.33 元；賣方 9 月已下修到 62.5 元，差距約 3%，不構成分母爭點。第二季業外收益 44.3 億屬單季墊高，不進年度錨"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"2026 年第三季法說：毛利率與第四季展望","impact":"高","watch":"毛利率是否 ≥35%、管理層對缺料回補的說法"},{"date":"2026-11","date_precision":"month","type":"other","event":"10 月合併營收公布","impact":"中","watch":"年增是否回到 ≥20%"},{"date":"2026Q4","date_precision":"quarter","type":"product","event":"800V 高壓直流電源機櫃小量出貨","impact":"中","watch":"是否如期出貨、客戶是誰"},{"date":"2027-02","date_precision":"month","type":"macro","event":"主要雲端業者公布 2027 年資本支出","impact":"高","watch":"年增幅度是否仍為正"},{"date":"2027Q4","date_precision":"quarter","type":"regulatory","event":"USITC 337 調查初步裁定","impact":"高","watch":"侵權認定、排除令或和解"}],"_projected_from":"v19"}
```
