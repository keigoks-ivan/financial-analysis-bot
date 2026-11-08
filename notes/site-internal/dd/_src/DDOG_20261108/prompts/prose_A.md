你是 stock-analyst v20 的**散文層（prose）agent**，標的 DDOG（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：DDOG　日期：2026-11-08　archetype：None　前份裁決：2026-09-24　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1628B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（820B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（996B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1467B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1140B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（776B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（695B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2534B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3380B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2091B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1628           3760-5372      5 條（2–6 內）  
s3                  8000         820           5026-7180      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3603          7978-11397      5 條（2–6 內）  
s6                 11000         776          7157-10224      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         695           1963-2805      5 條（2–6 內）  
s10                 5000        2534           1726-2466      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2091           2000-2909      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5460B；至少需散文≈39.54KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70%
−65
−65%
−46%
−45%
−45
−28.8%
−24%
−10.55
−5%
−0.8%
−0.44
−0.33
0
0.31
0.4%
0.91
1
1.0
1%
1.08
1.1
1.4%
1.5%
2%
2
02
2.20
2.22
2.3%
2.5%
2.5
2.55
2.60
2.6
2.7
2.73
2.74
2.75%
2.75
2.81
2.82
2.95
2.98
3.00
3%
3
3.28
3.3
3.30
3.40
3.4
3.7
3.76
3.8
4%
04
4
4.11
4.3%
4.5%
4.83
4.87
4.9
5
5%
5.1
5.7
06
6
6.17
6.42
6.58
6.6
7
7%
07
7.1
7.5%
7.6
8%
08
8
8.5
9
9.09
9.15
10%
10
11%
11
11.9
11.97
12.0
12
12.6
13
13%
13.4
13.9
14
14%
15%
16
16%
17.1%
18.6%
19%
19.5%
19.6%
20%
20
21%
21.4%
23%
23.8%
24%
24
25%
25
26%
26
27%
28
28%
28.8%
29%
29.5%
30
30%
31%
33.5
34%
35%
35.0
35
36
36%
38%
39
39.3%
40%
40
40.1
41%
42.6%
43%
44%
44.5
44.7
45
45.15
45.2
45.25
48
49
50%
50
52%
52
54%
55%
55.3
56
60
60.08
61%
62
65
65.3
65.34
70
70.2
70.21
75
76
78%
81.2%
82.6
83
85.7%
90%
91%
94.4
98.6
99
100
100%
107.5
115%
120%
133
140
142
150%
166
175
179
179.04
185
215
248.7
251
251.49
257
270
271.57
300
341
436.32
450
2024
2025
2026
2027
2028
2029
2036
20261108
1,000
33,400
33,500
4,860
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
{"meta":{"ticker":"DDOG","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Datadog, Inc."},"oneliner":"Datadog 非 AI 客戶連五季加速，最大客戶已按合約下限估入指引；但 179 美元買進的 Base 年化只有約 7.5%，股權激勵又占營收近兩成，等 175 美元以下再談分批。","thesis":{"H":[{"id":"H1","text":"非 AI 客戶維持高成長，證明加速不是雲端優化結束後的短暫回補，而是 AI 帶動軟體量與平台擴張。","2y":"FY2027 各季非 AI 客戶營收年增維持 25% 以上。","5y":null,"10y":null,"threshold":"非 AI 客戶營收年增 ≥25%（現況 high 20s）","source":"每季法說會 CFO 準備稿，公司只給區間","drift_rule":"公司只給區間，依用語判斷：連兩季降到 mid-20s 以下為削弱，連三季降到 low-20s 以下為反轉。"},{"id":"H2","text":"規模與研發效率讓 non-GAAP 利益率上升，同時股權激勵占營收下降，股東實得利潤跟著增加。","2y":null,"5y":"FY2031 non-GAAP 營業利益率約 29.5%，股權激勵占營收 13% 以下。","10y":null,"threshold":"FY2029 前 non-GAAP 營業利益率 ≥28%，且 TTM 股權激勵占營收 ≤15%（2026 Q2 單季 19.6%）","source":"每季 8-K 與 10-Q","drift_rule":"TTM 數字連四季偏離 Base 路徑 5% 以上為削弱，連六季偏離 10% 以上為反轉。"},{"id":"H3","text":"平台滲透與份額繼續上升，資安與 AI 監控在核心監控放緩時接上第二條成長曲線。","2y":null,"5y":null,"10y":"2036 年前公司自述全球觀測份額達 25–30%，資安成為占比兩位數的產品線。","threshold":"使用六項以上產品的客戶比率 2029 年 ≥55%（現況 41%），毛留存維持 90% 中後段","source":"每季法說會 CEO 準備稿、投資人日","drift_rule":"跨兩個年度未達路徑為削弱，跨三個年度未達為反轉。"}],"R":[{"id":"R1","text":"最大客戶降用量或到期不續約，頂端 AI 原生客戶跟進。公司兩季都不說合約期限與降量原因；外界指為 OpenAI，屬媒體推測。SaaStr 把該客群 Q1 的貢獻寫成客群成長，與 10-Q 轉述的貢獻點數口徑不同，以後者為準。","h_ref":"H1","clock":"🔥","threshold":"下次續約承諾金額低於本次或不續約","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_second_source#4","customer_concentration_credit#0","customer_concentration_credit#5","end_markets#2"]},{"id":"R2","text":"提前續約的價格折讓從個案變成常態，大客戶用更高承諾換更低單價，營收增速追不上用量增速。","h_ref":"H2","clock":"🔥","threshold":"cRPO 年增連兩季低於 25%，或 non-GAAP 毛利率連兩季低於 78%","evidence_refs":["end_markets#3"]},{"id":"R3","text":"平台綑綁與低價替代同時壓縮預算：資安與資料平台收購監控廠商，超過 40 家廠商競爭，總持有成本成為標準問題，Grafana ARR 已過 4 億美元。","h_ref":"H3","clock":"🐢","threshold":"Ramp 採用率由 34% 跌破 30%，或毛留存跌出 90% 中後段","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#1","supply_demand_durability#7","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"股權激勵不降，帳面成長轉不成每股價值。","h_ref":"H2","clock":"🐢","threshold":"FY2027 全年股權激勵占營收仍高於 19%，或淨稀釋高於 3%"},{"id":"R5","text":"AI 自動化與貼近推論成本的定價壓縮單位收入，產品採用率上升卻換不到淨留存。","h_ref":"H3","clock":"🐢","threshold":"AI 產品客戶比率持續上升，但淨留存跌破 115%"}],"single_thing":{"description":"FY2027 任一季，非 AI 客戶營收年增掉回 20% 以下。","why_fatal":"非 AI 客戶是營收主體（AI 原生客群 2025 年底約占 11%，最新占比事實表未涵蓋）。這個群組少 10 個百分點成長，一年衝擊接近最大客戶完全歸零，兩年就超過，而且逐年累積，Base 的 EPS 複利約 18.6% 也站不住。","if_happens":"Base 改用 Bear 路徑，終端倍數降到 28 倍，五年目標約 83 美元；持股清倉。","how_monitor":"每季法說會 CFO 準備稿的非 AI 客戶年增區間，下一次在 2027 年 2 月。","probability":"20%（12–24 個月）。一年前仍約 20%，已連五季加速，掉回去等於吐回這段加速。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":60.08,"peg_fy2":2.81,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":2.55,"FY2027E":2.98,"FY2028E":3.76},"fy_end_month":12,"eps_basis":"non-GAAP 稀釋 EPS，Koyfin 2026-11-07 快照。FY2025A 的 non-GAAP EPS 事實表未涵蓋，留空；財報表的 GAAP 0.31 口徑不同，不拿來當基期。FY2026E 2.55 低於 2026-11-04 全年指引 2.73–2.75，FY2027E、FY2028E 可能同樣未更新。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"營收年增 30% 上下、non-GAAP 利益率改善、FCF 利潤率 26%，但 GAAP 營業利益率只有 2.3%，複利品質要扣掉股權激勵才算數。"},"industry":{"clock_phase":"II","sd_verdict_source":"供需持久性判斷為結構性持久。雲端遷移與 AI 上線同時增加監控資料量，非 AI 客戶連五季加速（2026-11-04 CEO）；可逆的部分集中在少數 AI 原生大客戶，他們會用折扣和自建壓低用量，這部分反映在 Bear 機率。景氣位置的依據是客戶用量與新簽金額，不是股價。","bargaining":{"up":"上游雲端與模型供應商的成本與條款事實表未涵蓋。Bits AI 定價貼近推論成本（2026-11-04 CEO），AI 層的價值多半留給模型供應商或回饋客戶。","down":"一般企業客戶分散，議價力弱；頂端 AI 原生客戶議價力強，提前續約換更好單價，最大客戶可把用量降到合約下限。","geo":"10-K 未見半導體或中國供應鏈依賴（程式抽取結果，非逐頁確認）；約 44% 全職員工在美國以外，其中 34% 在法國。"},"profit_pool_dir":"利潤池方向事實表未涵蓋。定性看，AI 層的增量利潤偏向模型與算力供應商，觀測層靠用量以及資安、軟體交付的擴張來補。","tam_table":[{"item":"公司口徑觀測市場","value":"300 億美元以上（2026-02-12 投資人日 CFO）"},{"item":"公司口徑含資安、軟體交付後 TAM","value":"超過 1,000 億美元（同上）"},{"item":"第三方 2026 年估計","value":"33.5 億至 341 億美元，相差十倍，CAGR 11%–16%；最低值比 Datadog 自身營收還小，只能是窄口徑"},{"item":"Gartner 2028 年觀測平台市場","value":"142 億美元（2025-08 報導）"},{"item":"公司自述份額","value":"十幾個百分點（2026-11-04 CEO 引產業分析師）"},{"item":"客戶家數滲透率","value":"約 7%，目標客戶約 50 萬家（2026-02-12 CFO）"},{"item":"利潤池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"同一份生產環境資料支撐多項產品，工具整併後拆分成本高，資料與工作流程構成轉換成本。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Gartner 連六年列領導者、非 AI 客戶連五季加速、多產品滲透上升。定價面由穩定轉向略縮：2026-11-04 法說會證實多家大客戶提前續約換更好單價，Flex Logs 與 Infinite Cardinality Metrics 也在降低客戶單位成本。兩者抵銷，判持平。","peer_na_reason":"同業 ROIC 與份額事實表未涵蓋，只能比利潤率與研發密度。","threats":[{"level":"🔴","text":"資料、資安與監控合併成單一平台：Palo Alto 收購 Chronosphere、Snowflake 收購 Observe、Cisco 整合 Splunk。受損方向在傳統企業與資安綑綁預算；來源是第三方評論，尚無份額流失數據，攻擊者投入金額事實表未涵蓋。","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"頂端 AI 原生客戶自建或部分遷移：2024 年已有一家縮減並部分改用內部工具，最大客戶 2026 年再降用量。受損範圍集中在少數超大客戶，一般企業沒有自建的工程量。","p":"35%","evidence_refs":["customer_second_source#4"]},{"level":"🟡","text":"架構與計價替代：eBPF、資料留在客戶 VPC、按基礎設施計價，加上超過 40 家廠商競爭下總持有成本成為標準問題，Grafana ARR 已超過 4 億美元。架構替代的說法出自競品行銷文，Datadog 也已推 BYOC，CEO 稱資料收集從來不是護城河；本次視為點對點壓價，不是架構取代。","p":"25%","evidence_refs":["substitute_technology#0","supply_demand_durability#1","supply_demand_durability#7"]},{"level":"🟡","text":"開發工具與通用 coding agent 往下吃監控功能。第三方預測只取得論點，缺內文與廠商名單；CEO 於 2026-02-12 承認事後排查用通用工具也有不錯結果，但主動偵測需要生產資料流，通用工具碰不到。","p":"30%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（未經投入資本驗算，只以資本支出占營收 3–4% 推定周轉高；扣股權激勵後利益率僅個位數）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是工程團隊，決策者是平台與技術主管，付款者是財務長；三者都需要知道正式環境出了什麼事。毛留存 90% 中後段是代理讀數。Q2 法說會分析師提到財務長抱怨帳單，表示問題在花多少，不在要不要用。"},{"item":"決策層級","level":"🟡","text":"客戶的替代決策落在每種資料的保留層級，不是整個平台。Q3 CEO 承認大客戶續約時會調整資料層級；最大客戶可把用量降到下限。反方向證據是客戶持續整併三到五套工具進 Datadog。"},{"item":"價值鏈分配","level":"🟡","text":"頂端買方集中且議價力強，提前續約換更低單價；AI 層定價貼近推論成本，價值流向模型供應商或客戶。自研 Scout 模型降低推論成本，是公司保留價值的做法，貢獻尚未量化。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的工具軟體，沒有民生價格上限問題；監管面只見 10-K 列出的歐盟 AI Act 與隱私法規一般風險，未見反壟斷事項。"}],"roiic":"無法計算：事實表未涵蓋投入資本、折舊與營運資金變動。GAAP 代理：FY2023 到 FY2025 營收增加約 13 億美元，GAAP 營業利益由約 −0.33 億美元變為約 −0.44 億美元，扣股權激勵後的增量利潤接近零。","reinvest_rate":"無法按公式計算。可得代理：FY2026 資本支出加資本化軟體占營收 3–4%；真正的再投資走損益表，TTM GAAP 研發密度 42.6%。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，所需的折舊、營運資金與收購淨額都不在證據包內，不以推估代入。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","DDOG":79.58,"SNOW":67.03,"DT":81.05,"ESTC":75.5,"NOW":73.08,"unit":"%"},{"metric":"營業利益率","DDOG":2.3,"SNOW":-22.76,"DT":13.55,"ESTC":-1.54,"NOW":9.68,"unit":"%"},{"metric":"FCF 利潤率","DDOG":25.93,"SNOW":21.96,"DT":26.53,"ESTC":19.37,"NOW":30.78,"unit":"%"},{"metric":"研發密度","DDOG":42.61,"SNOW":38.78,"DT":23.81,"ESTC":25.26,"NOW":22.47,"unit":"%"}],"competitors":[{"name":"SNOW","gm":67.03,"om":-22.76,"fcf_margin":21.96,"rd_intensity":38.78,"strategy_note":"毛利率低約 12.6 個百分點，靠收購 Observe 從資料平台切入監控，威脅在資料層綑綁，尚無份額數據。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"DT","gm":81.05,"om":13.55,"fcf_margin":26.53,"rd_intensity":23.81,"strategy_note":"企業市場主要對手，GAAP 獲利較好、研發密度低很多；Datadog 的差異在平台廣度與新品速度。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ESTC","gm":75.5,"om":-1.54,"fcf_margin":19.37,"rd_intensity":25.26,"strategy_note":"日誌與搜尋起家，FCF 利潤率低約 6.6 個百分點，Flex Logs 搶的正是這類日誌預算。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"NOW","gm":73.08,"om":9.68,"fcf_margin":30.78,"rd_intensity":22.47,"strategy_note":"工作流程平台，不是直接監控對手；在 IT 維運入口與 AI agent 層有重疊，FCF 利潤率高約 4.9 個百分點。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主，產品滲透次之，價格為負向；併購與回購貢獻可忽略。","runway_years":6,"runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本與再投資明細，內生上界無法計算，不以推估代入。","segments":[{"item":"基礎設施監控","value":"ARR 超過 20 億美元，年增 30% 中段（2026-11-04）"},{"item":"日誌管理","value":"ARR 超過 10 億美元，年增 30% 中段（2025 年底）"},{"item":"APM","value":"ARR 超過 10 億美元，年增 30% 中段（2025 年底）"},{"item":"RUM","value":"ARR 超過 2 億美元，年增逾 50%（2026-08-06）"},{"item":"資安產品","value":"ARR 超過 1 億美元（2026-02-12）；百萬美元客戶的資安支出只占其 Datadog 支出 2%"},{"item":"Flex Logs","value":"ARR 接近 1 億美元（2026-02-12）"},{"item":"GPU 監控","value":"裝置數今年增 8 倍，CEO 稱尚未廣泛收費，不在目前成長內"}],"decay_signals":["股權激勵占營收 19.6%（2026 Q2），高於 5%；逐年序列事實表未涵蓋，保守計為亮起。其餘九項未亮或無資料。"]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購或回購撐，且證據包沒有現金去向明細，展開也沒有數字可填。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Adaptive ML 收購價未揭露，歷次併購的已實現報酬事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"證據包內沒有回購紀錄。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"CFO 淨稀釋目標每年 2.5–3%（2026-02-12 投資人日），高於 1.5%；實際逐年序列事實表未涵蓋。","grade":"不過"}]},"valuation":{"basis":"non-GAAP 前瞻本益比搭配 PEG，以前瞻 EV/S 與扣股權激勵的現金流殖利率交叉檢查。","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率與研發密度，沒有同業前瞻本益比或 EV/S，無法做同級倍數對照。"},"peg":3.28,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 65–70 倍，PEG 3.28（70.21 倍除以共識年複合 21.4%），以指引基期計約 3.8，都高於 2 的昂貴線；Base 年化約 7.5%，略低於 8%。比前份便宜一級，因為股價跌約 29%，但還沒到合理。五年分位無資料：事實表只有 3–4 個年度端點，不能當五年分位。短期上檔以 FY2027 EPS 3.40 美元乘 60 倍估一年，中期以 FY2029 EPS 4.87 美元乘 50 倍估三年。","upside_short_pct":13.9,"upside_mid_pct":36.0},"trap_analysis":{"verdict":"🟡","label":"一項衰退訊號亮起（股權激勵），領先指標放緩待驗"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"帳單年增 30%、RPO 年增 38%，都比上季放緩；Q4 指引季增持平；非 AI 客戶一年前年增只有約 20%。","assumption":"非 AI 客戶連五季加速是結構性的，AI 寫程式帶來更多軟體和監控量。","consequence":"若只是雲端優化結束後的回補，加上 AI 預算排擠，非 AI 年增掉回 20% 以下，FY2031 EPS 約 2.95 美元，乘 28 倍約 83 美元，五年虧 54%。","ruling":"採納為 Bear 主路徑，機率 30%，與唯一致命點同一件事。目前毛留存穩定、產品滲透上升，尚無惡化跡象。","watch":"每季非 AI 客戶年增區間、cRPO 年增。","evidence_refs":["end_markets#3"],"fact_refs":["f_kpi13_rpo_current_rpo","f_kpi14_billings","f_kpi15_ai_yoy"]},{"view":"論點失敗","evidence":"CEO 於 2026-02-12 承認事後排查用通用工具也有不錯結果；CTO 同日承認小模型沒有明確資金門檻，自家時序模型訓練只花約 75 萬美元。","assumption":"生產資料是 AI 時代的護城河。","consequence":"若通用 agent 能直接讀取客戶自有遙測，Datadog 會從工作入口退回資料管線，產品溢價下降。","ruling":"部分採納，列為長期風險。Bits AI 是公司史上採用最快的產品，Scout 降低推論成本，短期是加分；但 AI 產品 ARR 未揭露，淨增量未證。","watch":"AI 產品客戶比率上升時，淨留存是否跌破 115%。","fact_refs":["f_kpi12_net_revenue_retention_tr"]},{"view":"論點成功但股東經濟變差","evidence":"股權激勵 2026 Q2 占營收 19.6%、占 non-GAAP 營業利益 85.7%；TTM GAAP 營業利益率 2.3%；CFO 目標淨稀釋每年 2.5–3%；Bits AI 定價貼近推論成本。","assumption":"non-GAAP 利益率提升會轉成每股價值。","consequence":"營收達到 Base，股數卻每年增約 2.75%，利潤大部分歸員工；AI 層價值交給模型供應商，單位收入下降。","ruling":"採納。終端倍數定 40 倍，Base EPS 已用稀釋後股數，並把 FY2027 股權激勵占營收列入監測。","watch":"TTM 股權激勵占營收、稀釋股數年增。","fact_refs":["f_kpi4_stock_based_compensation","f_peer_ddog_operating_margin_pct"]},{"view":"價格已反映太多","evidence":"FY2026 指引中位 65.3 倍，PEG 3.3 以上，前瞻 EV/S 13.4 倍。","assumption":"跌 29% 後定價已合理。","consequence":"要賺 8% 年化需 EPS 五年複利約 19%，Base 18.6%，沒有留失誤空間；倍數往 40 倍靠攏，盈餘成長大部分會被吃掉。","ruling":"採納，這就是不追的約束條件，股價到 175 美元以下才解除。","watch":"收盤價對 175 美元；FY2027 指引後的 Base EPS。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_ev_s_fwd"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 251.49 → 本次 179.04（-28.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=251.49","side_b":"本次 price_at_dd=179.04","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 251.49 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 251.49 美元：Bull 價 450、Bear 價 94.4，五年期望值 +4.3%，基準年化 1.4%，不對稱比 1.1","side_b":"本次情境、股價仍用 251.49 美元：Bull 價 436.32、Bear 價 82.6，五年期望值 −0.8%，基準年化 0.4%，不對稱比 0.91","ruling":"先換情境、股價不動：五年期望值少 5.1 個百分點，基準年化少 1.0 個百分點。不對稱比由 1.1 變為 0.91。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 251.49 美元：五年期望值 −0.8%，基準年化 0.4%，不對稱比 0.91","side_b":"本次情境、股價 179.04 美元：五年期望值 +39.3%，基準年化 7.5%，不對稱比 2.22","ruling":"再換股價、情境不動：起點價下跌 28.8%，五年期望值多 40.1 個百分點，基準年化多 7.1 個百分點，不對稱比由 0.91 升到 2.22。合計五年期望值比前份多 35.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"Q4 指引季增持平對排除最大客戶仍加速","cause":"新證據","prior_field":null,"side_a":"Q4 營收指引 11.9–12.0 億美元，對 Q3 的 11.97 億美元幾乎零季增，年增降到 25–26%；上一季的 Q3 指引也曾顯示年增由 36% 降到 28–29%。","side_b":"CFO 稱排除最大客戶，Q4 隱含年增在 30% 低到中段，並把季增放緩歸因於最大客戶只算合約下限、提前續約折扣、12 月季節性三件事。","ruling":"可調和的程度差異，採 B 側但打折。上一季同樣保守的 Q3 指引實際超出上緣 4.5%，保守是真的。管理層稱全是好消息，本次不全採信：提前續約的單價折讓是實際收入損失，標為未證、監測；若 2027 年上半年連兩季季增低於 4%，這項一次性歸因視為不成立。","evidence_level":"公司法說會（2026-11-04 CFO、CEO）；三項因素的金額拆分公司未提供","settle_metric":"2027 年 Q1、Q2 營收季增率與排除最大客戶年增","if_then":["若 2027 年 Q1 季增 ≥5% 且排除最大客戶年增 ≥30%，上調 Base 路徑，價格在新門檻內就分批反買首批","若連兩季季增 <4%，停止加碼並下修 Base 路徑 5%","若股價先漲過 215 美元而上述數字未到，不追"],"evidence_refs":["end_markets#3"]},{"axis":"帳單、RPO 放緩對營收維持 35%","cause":"新證據","prior_field":null,"side_a":"帳單年增由 Q2 的 38% 降到 30%，RPO 由 43% 降到 38%，cRPO 由約 40% 降到 30% 中段；Q3 淨增客戶只有約 100 家（33,400 到 33,500）。","side_b":"CFO 連兩季強調營收比帳單與 RPO 更能反映趨勢；RPO 年限略拉長，年付 10 萬美元以上客戶增加約 140 家。","ruling":"可調和，但偏向 A 側警示。降幅和最大客戶降量、折扣續約的說法相符，不是新的惡化來源；不過 cRPO 增速已貼近營收，下一季要看是否止穩。","evidence_level":"公司法說會（2026-08-06、2026-11-04 CFO）","settle_metric":"cRPO 年增","if_then":["若 cRPO 年增連兩季低於 25%，減碼一半並停止加碼","若 cRPO 年增回到 35% 以上且價格在門檻內，分批反買首批"]},{"axis":"管理層前後說法：財測去風險與最大客戶揭露","cause":"新證據","prior_field":null,"side_a":"2026-08-06 CEO 稱今年剩餘財測已完全去風險，2026-11-04 CEO 又說提前續約是與上季唯一不同的新逆風；最大客戶的合約期限、折扣與降量原因兩次法說都沒有回答。","side_b":"同期實績超指引：全年營收指引由 44.5–44.7 億美元升到 45.15–45.25 億美元，全年 non-GAAP 營業利益率由 23% 升到 24%。","ruling":"結果站 B 側，揭露站 A 側。指引品質可信，客戶集中度的能見度不足，所以 Bear 機率維持 30%，不因 Q3 超預期下調。","evidence_level":"公司法說會逐字稿；最大客戶占比為資料缺口","settle_metric":"下次續約承諾金額與期限（公司未揭露）","if_then":["若 10-K 揭露單一客戶占營收 ≥10% 且降幅大於指引隱含值，減碼一半","若 FY2027 指引列明最大客戶按下限估算，且非 AI 年增仍為 high 20s，分批反買首批"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#5"]},{"axis":"FY2026 EPS 分母：舊共識對新指引","cause":"方法變動","prior_field":null,"side_a":"事實表共識 2.55（2026-11-07 Koyfin 快照），前瞻本益比 70.2 倍。","side_b":"2026-11-04 全年指引 2.73–2.75；營收共識 45.2 億美元已跟上新指引。","ruling":"採 B 側。快照值低於指引下緣，應是未隨財報更新，FY2027、FY2028 也可能偏低。情境起點改用指引中位 2.74，共識欄位照錄但不承重。","evidence_level":"公司指引優先於未更新的聚合快照","settle_metric":"下一期共識快照的 FY2026 是否 ≥2.73","if_then":["若新快照 FY2027 共識 ≥3.30，維持 Base 第一年 3.40 美元，門檻 175 美元不動","若 FY2026 已更新而 FY2027 共識仍 <3.00，下修 Base 路徑 5%，門檻同比下調到約 166 美元"]},{"axis":"現在就買的最強論證（本次不追）","cause":"價格變動","prior_field":null,"side_a":"非 AI 客戶連五季加速、Q3 超指引 4.5%、non-GAAP 利益率 28%、最大客戶有合約下限兜底；股價六週內由 251 美元跌到 179 美元，RSI 28。前份約定的 185 美元已觸發，當時也說共識上修要上調門檻。","side_b":"已跌多少不是安全邊際。Base 年化約 7.5%，未到 8%；股權激勵占營收近兩成，扣掉後現金流殖利率不到 1%；Q4 才是第一個最大客戶落到下限的季度，FY2027 指引還沒出。","ruling":"站 B 側，但差距只有幾個百分點。這不是看壞，是價格還差一點，股價再跌約 2% 就進入分批範圍。兩側不是不可調和，差別在時點與價格。","evidence_level":"法說會與情境試算","settle_metric":"收盤價對 175 美元","if_then":["若股價收在 175 美元以下，重跑判斷並分批反買首批","若股價未到 175 美元就漲過 215 美元且 FY2027 指引未出，不追"]},{"axis":"前份漂移：價格帶動的欄位","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份 251.49 美元，估值在最高警示級，最大回撤估 −70%，Bull 25%、Bear 30%。","side_b":"本次 179.04 美元，前瞻本益比由約 98.6 倍降到 65 倍，估值降一級為偏貴；最大回撤估 −45% 至 −65%，Bull 25%、Bear 30%。","ruling":"估值改善主要因價格下跌約 29%，FY2026 EPS 上修只占小部分。機率不因價格而動，Bear 主路徑沒有被排除。","evidence_level":"事實表價格與法說會指引","settle_metric":"前瞻本益比","if_then":["若股價收在 175 美元以下，分批反買首批","若股價回到 215 美元以上且基本面未上修，不追"]},{"axis":"前份漂移：基本面欄位","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：時機評級 B、陷阱低風險、護城河持平、五年後跑道寬、品質複利成長、無景氣位置，結論觀望。","side_b":"本次：時機評級 B、陷阱升為中度、護城河持平、跑道寬、品質複利成長、無景氣位置，結論仍是不追。","ruling":"只有陷阱一欄變動：帳單與 RPO 放緩、提前續約折價是 2026-11-04 才確認的新證據，加上股權激勵超標，由低風險升為中度。其餘欄位維持，因 Q3 的加速與折價相互抵銷。","evidence_level":"2026-11-04 法說會","settle_metric":"cRPO 年增與非 AI 客戶年增","if_then":["若 cRPO 連兩季低於 25%，減碼一半","若非 AI 年增掉回 20% 以下，清倉"]},{"axis":"行動門檻變動：分批重啟價位","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","side_b":"股價收盤回落至175美元以下（Base五年年化約8%）才重跑判斷分批；FY2027指引後按Base EPS同比調整","ruling":"舊門檻已觸發（179.04 美元低於 185 美元），本次就是觸發後的重跑。重跑結果 Base 五年目標約 257 美元，低於前份回推的約 270 美元：EPS 上修，但終端倍數下調到 40 倍，反映提前續約折價與股權激勵，8% 年化對應價由 185 美元改為 175 美元。動作仍是分批反買，未觸發前不追，不是減碼。","evidence_level":"情境試算；前份目標價由前份年化報酬回推，前份倍數未留存","settle_metric":"收盤價對 175 美元","if_then":["若收在 175 美元以下，重跑判斷並分批反買首批","若收在 175 美元以上，不追"]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空，原文未留存。","side_b":"FY2027 任一季，非 AI 客戶營收年增掉回 20% 以下。","ruling":"前份未留存，無法比較舊門檻。本次選非 AI 客戶年增，因為這個群組少 10 個百分點成長，兩年的累積衝擊就超過最大客戶完全流失。","evidence_level":"2026-11-04 法說會與投資人日 AI 原生占比","settle_metric":"非 AI 客戶營收年增","if_then":["若掉回 20% 以下，清倉","若維持 high 20s，門檻不動"]},{"axis":"清倉與減碼門檻變動","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空，原文未留存。","side_b":"清倉：非 AI 客戶年增掉回 20% 以下。減碼：排除最大客戶年增連兩季低於 25%、cRPO 年增連兩季低於 25%、毛留存跌出 90% 中後段。","ruling":"前份未留存，本次重建，門檻取自 Bear 路徑與 Q3 現況的距離。","evidence_level":"2026-11-04 法說會","settle_metric":"上述四項指標","if_then":["任一減碼條件成立，減碼一半","清倉條件成立，清倉"]}],"triggers":[{"n":1,"text":"股價收盤跌破 175 美元，重跑判斷後分批反買首批。","type":"估值rearm","maps_to":"H1","metric":"收盤價","threshold":"≤175 美元","action":"重跑判斷，通過後分批反買首批","source_freq":"每日收盤","date":null},{"n":2,"text":"非 AI 客戶營收年增維持 25% 以上。","type":"假設驗證","maps_to":"H1","metric":"非 AI 客戶營收年增","threshold":"連兩季降到 mid-20s 以下","action":"停止加碼","source_freq":"每季法說會","date":"2027-02"},{"n":3,"text":"非 AI 客戶年增掉回 20% 以下，論點失效。","type":"Single Thing","maps_to":"H1","metric":"非 AI 客戶營收年增","threshold":"<20%","action":"清倉","source_freq":"每季法說會","date":null},{"n":4,"text":"最大客戶下次續約承諾低於本次或不續約。","type":"風險","maps_to":"R1","metric":"最大客戶續約承諾","threshold":"低於本次九位數承諾或不續約","action":"減碼一半","source_freq":"法說會與 10-K，到期日公司未揭露","date":null,"evidence_refs":["customer_second_source#0","customer_concentration_credit#0","end_markets#2"]},{"n":5,"text":"提前續約折價擴散，cRPO 或毛利率走弱。","type":"風險","maps_to":"R2","metric":"cRPO 年增、non-GAAP 毛利率","threshold":"cRPO 連兩季 <25%，或毛利率連兩季 <78%","action":"減碼一半並停止加碼","source_freq":"每季法說會","date":null},{"n":6,"text":"排除最大客戶的成長跌破 25%，加速敘事不成立。","type":"減碼","maps_to":"H1","metric":"排除最大客戶營收年增","threshold":"連兩季 <25%","action":"減碼一半","source_freq":"每季法說會","date":null},{"n":7,"text":"持有首批後，FY2027 指引確認基本面才加第二批。","type":"加碼","maps_to":"H1","metric":"FY2027 指引隱含的排除最大客戶年增","threshold":"≥25%，且毛留存維持 90% 中後段","action":"分批反買第二批","source_freq":"2027 年 2 月財報","date":"2027-02"},{"n":8,"text":"第四季財報與 FY2027 指引出爐後全面複審。","type":"複審日期","maps_to":"H1","metric":"Base EPS、門檻價","threshold":"按新指引重算 8% 年化對應價","action":"依重算價更新門檻，股價在門檻內分批反買，門檻外不追","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"非 AI 客戶營收年增","bear_threshold":"掉回 20% 以下，清倉","window":"FY2027 任一季","source":"每季法說會 CFO 準備稿","last_status":"ok"},{"metric":"排除最大客戶營收年增","bear_threshold":"連兩季低於 25%，減碼","window":"2027 年 Q1 至 Q3","source":"每季法說會與指引說明","last_status":"ok"},{"metric":"毛營收留存率","bear_threshold":"跌出 90% 中後段，減碼","window":"連兩季","source":"每季法說會 CFO 準備稿","last_status":"ok"},{"metric":"cRPO 年增","bear_threshold":"連兩季低於 25%，減碼","window":"2027 年各季","source":"每季法說會 CFO 準備稿","last_status":"warning"},{"metric":"TTM 股權激勵占營收","bear_threshold":"FY2027 全年仍高於 19%，不加碼","window":"FY2027","source":"每季 8-K 與 10-Q；Q3 數字事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=-10.55, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 的盈餘路徑以總營收成長率和利益率推算，沒有分部的量價拆解。runway 的滲透率推導依賴公司自己的分母，換成 Gartner 口徑就站不住。兩點都有缺口，但沒有查到足以否定的反證，整體屬於證據不完整，不是被推翻。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價收盤在 175 美元以下，Base 五年年化才到約 8%；2027 年 2 月 FY2027 指引若改變 Base EPS，門檻同比例調整。'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價收盤回落至175美元以下（Base五年年化約8%）才重跑判斷分批；FY2027指引後按Base EPS同比調整","exec_line":"觸發後重跑判斷再分兩批：首批在 175 美元以下，第二批等 FY2027 指引確認排除最大客戶年增仍在 25% 以上。未觸發前不追。"},"reasoning":{"industry":"收費方式是年度承諾加實際用量，客戶用得越多、產品越多，付得越多。2026 年 Q3（2026-11-04 法說會 CFO 準備稿）營收 11.97 億美元，年增 35%；non-GAAP 毛利率 81.2%、營業利益率 28%。公司不揭露營收分部，只給 ARR：基礎設施監控超過 20 億美元、年增 30% 中段，日誌與 APM 在 2025 年底各超過 10 億美元。單點依賴是最大客戶：公司未點名，外界指為 OpenAI，屬媒體推測。它已簽九位數續約但降低用量，Q4 指引只按合約下限估入。AI 原生客群在 2025 年底約占營收 11%（2026-02-12 投資人日 CFO），最新占比與最大客戶單獨占比事實表未涵蓋。事實表的季度 KPI 停在 Q2，Q3 數字皆取自法說會逐字稿。","moat":"機制是把指標、日誌、追蹤、資安和 AI 監控放進同一份生產環境資料，產品越多、工具越難拆。可證方向：使用四項以上產品的客戶由 54% 升到 61%，十項以上由 8% 升到 16%（2026-11-04 CEO），毛留存穩在 90% 中後段。Ramp 採用率 34%、年持平，沒有份額流失，也沒有明顯擴大。不標上升的原因有二：最大客戶用量下降，提前續約的大客戶也拿到更好單價。同業 ROIC 事實表未涵蓋，改以留存與產品滲透當比較軸；利潤率上，FCF 利潤率與 Dynatrace 接近，GAAP 營業利益率低約 11 個百分點，主要差在研發密度 42.6% 對 23.8%。AI 曝險：附著點在自家生產資料，屬強化；通用 coding agent 繞過事後排查的部分屬替代（2026-02-12 CEO 承認事後排查用通用工具也有不錯結果），分界年約 2028。公司未揭露 AI 產品 ARR，淨增量無法計算。","growth":"成長主要靠量：既有客戶多用、多買產品，新客戶貢獻約 30% 年增量；價格不是推力，頂端客戶還在拿折扣；併購與回購都不重要。共識 EPS 年複合 21.4%（FY2026 的 2.55 到 FY2028 的 3.76，兩個跨度，Koyfin 快照），但 2.55 低於 11-04 指引下緣，以指引中位 2.74 為基期則是 17.1%。內生上界無法計算，缺口列為無法歸因，長期信心上限為中。定性看，差距靠利益率由 24% 升到 28–30%，沒有靠回購。市場分母要小心：Mordor 的 33.5 億美元比 Datadog 自身營收還小，只能是窄口徑；公司口徑 300 億美元以上和 CEO 說的十幾個百分點份額對得上。若採 Gartner 2028 年 142 億美元，份額會高得多，跑道判斷要下修，這是本結論最可能出錯的地方。以 27% 對市場 14% 的相對增速，份額翻倍到 30% 約需 6 年。","governance":"FY2025 FCF 9.15 億美元對 GAAP 淨利 1.08 億美元，轉換率約 8.5 倍，高得不尋常的原因是股權激勵不花現金：2026 Q2 單季股權激勵 2.20 億美元，占營收 19.6%、占 non-GAAP 營業利益 85.7%。CFO 的淨稀釋目標是每年 2.5–3%（2026-02-12 投資人日）。現金及有價證券 52 億美元，扣債務後淨現金約 39 億美元；FY2026 資本支出加資本化軟體降到營收 3–4%。營運槓桿正向：Q3 營業費用年增 25%，低於營收 35%。現金去向四分、回購紀錄與債務到期結構事實表未涵蓋。","valuation":"現價 179.04 美元對 FY2026 指引中位 2.74 是 65.3 倍，對事實表舊共識 2.55 是 70.2 倍。以終端 40 倍推回，要賺 8% 年化需要 FY2031 EPS 約 6.58 美元，五年複利約 19%；Base 是 18.6%。估值也不便宜：前瞻 EV/S 13.4 倍，扣股權激勵後的現金流殖利率不到 1%（TTM FCF 約 11 億美元減約 8 億美元股權激勵，後者以 Q2 的 19.6% 外推，屬估計）。賣方平均目標 271.57 美元（8 月 MarketBeat）比現價高 52%，方向上反對不追，但這是財報前數字，全距未知，不調整判斷。我與賣方的差別在終端倍數，不在盈餘：Base 的 FY2027 EPS 3.40 美元高於舊共識 2.98 美元。同業現值倍數事實表未涵蓋。","premortem":"完整反證見反證紀錄。產業態勢為雙向拉鋸：競爭面，資安與資料平台收購監控廠商；結構面，AI 工作負載與工具整併讓領先平台受益，Gartner 連六年列領導者；客戶結構面，AI 原生集中度是新變數。最大客戶的合約期限、折扣與降量原因在 2026-08-06 法說會遭迴避，2026-11-04 仍未說明；投資人日對大客戶單位經濟與 AI 業務風險也未正面回答，這些是資料缺口。歷史最大回撤、空方最強數字事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"向企業收雲端與 AI 系統的監控、資安用量費，錢卡在「生產環境資料集中到同一平台」這一節。","moat":"護城河持平：執行面在擴大，定價面被頂端客戶的折扣抵銷，整體不標上升。","growth":"五年後仍有跑道：以公司口徑份額十幾個百分點計，第五年滲透率仍低於 35%，資安與 AI 監控是第二條曲線。","capital":"資本配置偏弱：沒有回購證據，股權激勵的淨稀釋目標高於 1.5% 的及格線，併購報酬無法驗證。","valuation":"現價要求 EPS 五年複利約 19% 才賺得到 8% 年化；這條路徑我相信走得到，但價格沒有留失誤空間。","how_wrong":"最可能看錯在非 AI 加速只是階段性回補，或股權激勵讓每股價值跟不上報表成長。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"股價收盤在 175 美元以下，Base 五年年化才到約 8%；2027 年 2 月 FY2027 指引若改變 Base EPS，門檻同比例調整。","qc48_result":"pass","qc48_note":"Bull 的盈餘路徑以總營收成長率和利益率推算，沒有分部的量價拆解。runway 的滲透率推導依賴公司自己的分母，換成 Gartner 口徑就站不住。兩點都有缺口，但沒有查到足以否定的反證，整體屬於證據不完整，不是被推翻。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":179.04,"week26_return_pct":-10.55,"consensus_rev_3m_pct":0.79,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"non-GAAP EPS 排除占營收近兩成的股權激勵，GAAP 本益比 248.7 倍，兩個分母差三倍以上。共識 FY2026 的 2.55 又低於新指引下緣。因此不用低本益比或 PEG 主張便宜。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"AWS re:Invent 期間的產品發表","impact":"低","watch":"Bits AI 與 Agent Observability 的收費數字是否揭露"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 FY2027 指引","impact":"高","watch":"最大客戶的估算方式、排除最大客戶年增、非 AI 客戶年增、cRPO"},{"date":"2027-Q3","date_precision":"quarter","type":"other","event":"最大客戶可能的下次續約（公司未揭露到期日，僅依分析師假設的一年期推算）","impact":"高","watch":"承諾金額是否低於本次、是否轉向自建"}],"_projected_from":"v19"}
```
