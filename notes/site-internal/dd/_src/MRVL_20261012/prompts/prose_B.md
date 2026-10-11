你是 stock-analyst v20 的**散文層（prose）agent**，標的 MRVL（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRVL_20261012/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：MRVL　日期：2026-10-12　archetype：None　前份裁決：2026-08-31　觀望｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1932B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（1126B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1000B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1151B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1161B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（1266B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1261B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2510B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4199B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2944B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1932           3548-5068      5 條（2–6 內）  
s3                  8000        1126           4812-6874      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3312          8182-11688      5 條（2–6 內）  
s6                 11000        1266           6814-9734      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1261           1567-2239      3 條（2–6 內）  
s10                 5000        2510           1743-2490      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2944           2000-2056      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5965B；至少需散文≈39.03KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−640
−65
−65%
−58%
−50%
−50
−48%
−10.5%
−7.93%
−6.35%
0
0.087
0.27
0.52
0.53
0.54
0.75
0.93
1
1.10
1.27
1.4
1.5%
1.6
02
2
2%
2.8
03
3
3.07
3.2
3.26
3.8
4%
4
4.22
4.3
4.79
5
5%
5.6
5.68
5.9
06
6
6.06
6.07%
6.4
6.5
6.8
7%
7
7.0
07
7.25
7.4
7.6
7.9
08
8
8%
09
9
9.21
10
10%
10.2
10.9%
11%
11.4
11.9%
12
12%
12.18
13%
13
13.5
13.9
13.92
14
15%
15
15.7%
16.33%
16.8%
16.81%
17%
17
18
18%
18.2%
18.23%
19
20%
20
21
21.72
22
22.6
24
25%
25
26%
26
26.18
26.32
26.70
27%
27.1%
27.39
28
29.9
30%
30
31
31.5
32
33.1
34
35
35%
36%
36.6%
37%
37.2%
37.97
38
38.0
38%
40%
41%
42
44.2%
44.22%
45
46%
48.5%
48.52%
49
49.6
50
52.2%
53
53%
53.1%
53.2%
55
56%
56
57.0%
57.5%
57.5
58%
58.5%
58.9%
59%
60%
60
64.6%
65
65%
65.23
67%
68.8%
70
70%
71%
72%
75%
79%
80
80%
82%
85%
90
90.55
95
100
100%
105
110
114%
114.34
114.34%
115
116
120
126
134.1
138
150%
150
165
180
200
216.62
225
232
245
261
275.28
300
311
375
400
420
570.3
605
700
800
816
900
2024
2025
2026
2027
2028
2030
3661
20261012
1,000
1,150
1,200
2,350
4,000
7,000
7,850
−1,440
−1,860
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
{"meta":{"ticker":"MRVL","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Marvell Technology, Inc."},"oneliner":"互連與客製晶片雙引擎，投資人日把 FY28 營收拉到約 200 億美元；但股價六週漲 27%、基準五年年化約 11%，唯一致命點是雲端客戶資本支出轉為年減。不追，等股價回到 FY28 共識 EPS 32 倍以下","thesis":{"H":[{"id":"H1","text":"客製業務（XPU＋XPU attach）靠四大雲端分散與 Google TPU 生態系長約放量，FY28 年增逾一倍、FY29 達 FY28 三倍以上，抵銷 AWS 世代交接風險","2y":"FY29 客製營收 ≥100 億美元（管理層目標逾 120 億美元）","5y":null,"10y":null,"threshold":"FY28 客製年增 ≥100%；FY29 客製 ≥100 億美元","source":"公司季報、法說會與投資人日的客製營收口頭揭露；10-Q 客戶集中度","drift_rule":"資料中心營收連 2 季低於當季指引中點 5% 以上＝削弱；連 3 季低於 10% 以上或下修 FY29 客製目標＝反轉"},{"id":"H2","text":"互連（光 DSP、TIA／驅動、DCI）與交換器成長持續快於客戶資本支出，scale-up 光學與交換器成為第二曲線","2y":null,"5y":"FY31 互連營收達管理層中點 375 億美元的六成以上（≥225 億美元）","10y":null,"threshold":"互連 FY27 年增 ≥70%；FY28 互連年增率高於四大雲端資本支出增速 10pp 以上；交換器 FY28 年化 ≥10 億美元","source":"法說會分項口頭數字、投資人日、Cignal AI 與 Dell'Oro 份額報告","drift_rule":"互連成長率連 4 季低於門檻 5pp 以上＝削弱；連 6 季低於 10pp 以上＝反轉"},{"id":"H3","text":"毛利率在客製占比上升下守住 57.5%，營業費用增速約為營收一半，非 GAAP 營益率 FY28 內觸及 40%，EPS 成長快於營收；客戶資本支出 2027 年後放緩但不轉負","2y":"FY28 非 GAAP EPS ≥7.0 美元（共識 7.25）","5y":null,"10y":null,"threshold":"非 GAAP 毛利率 ≥57.5%；Q4 FY27 營益率 ≥38%、FY28 觸及 40%","source":"季報新聞稿非 GAAP 損益；四大雲端季報資本支出指引","drift_rule":"毛利率或營益率連 2 季低於門檻 5% 以上（相對值）＝削弱；連 3 季低於 10% 以上＝反轉"}],"R":[{"id":"R1","text":"最大客戶 AWS 次世代 Trainium 設計外流（傳 Trainium 3／4 轉 Alchip）或 Microsoft 改用 Broadcom，Google 與新一線客戶放量來不及補位","h_ref":"H1","clock":"🔥","threshold":"公司或客戶確認任一旗艦世代改由他家設計，或 FY28 客製營收未達倍增","evidence_refs":["customer_second_source#0","customer_second_source#2","customer_second_source#3","customer_concentration_credit#0","customer_concentration_credit#1","competitive_share_entrants#1"]},{"id":"R2","text":"毛利率由組合下滑轉為價格戰：800G 光 DSP 對手報價約低四成、相干 800G 競爭加劇、客製占比升高，Q3 指引已較 Q2 走低","h_ref":"H3","clock":"⚡","threshold":"非 GAAP 毛利率連 2 季 <57.0%","evidence_refs":["competitive_share_entrants#5","competitive_share_entrants#6","capital_markets_pricing#3"]},{"id":"R3","text":"客戶資本支出 2027 年見頂後轉向消化，雲端業者自由現金流轉負、舉債比重升高，訂單遞延","h_ref":"H3","clock":"🔥","threshold":"四大雲端合計年度資本支出指引年減，或 Marvell 下季營收指引季減","evidence_refs":["supply_demand_durability#4","customer_concentration_credit#3"]},{"id":"R4","text":"台灣晶圓與泛太平洋封測集中（歷年 10-K 皆揭露替代晶圓廠有限）、Section 232 半導體關稅第二階段、對中國出口許可延遲或拒發","h_ref":"H3","clock":"🐢","threshold":"關稅或出口管制使公司毛利率指引下修 ≥100bp，或台海供應中斷","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","regulatory_antitrust#1","regulatory_antitrust#2","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R5","text":"光互連架構替代：LPO 去掉模組 DSP、Broadcom 3 奈米 400G／lane Taurus DSP 競爭 1.6T／3.2T，scale-up 走 CPO 時 Marvell 光 DSP 經濟性被侵蝕","h_ref":"H2","clock":"🐢","threshold":"Cignal AI 或 Dell'Oro 的可插拔光 DSP 份額連 2 年下滑，或互連年增率低於四大雲端資本支出增速","evidence_refs":["substitute_technology#3","substitute_technology#4","competitive_share_entrants#6"]}],"single_thing":{"description":"四大美國雲端業者合計年度資本支出指引首次轉為年減","why_fatal":"資料中心占營收 79%、前十大客戶占 82%，FY31 模型假設資本支出增速只放緩到約 20%；一旦轉負，客製、互連、交換器三條線同時遞延，65 倍前瞻本益比向 17 倍收斂，EPS 與倍數雙殺，對五年價值的衝擊大於任何單一客戶事件","if_happens":"持有部位減碼至半倉；未持有則撤回進場條件，待下一季營收指引確認後重跑判斷","how_monitor":"四大雲端每季財報的年度資本支出指引（每年 1–2 月給次年度、每季更新），搭配 Marvell 下季營收指引是否季減","probability":"約 15%（12–24 個月）：BofA 估自由現金流轉負、共識預期 2027 年見頂持平，但 Moody's 估 2027 年仍逼近 1 兆美元、RPO 約 7,000 億美元撐住近兩年"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":37.97,"peg_fy2":0.54,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2026A":3.07,"FY2027E":4.22,"FY2028E":7.25,"FY2029E":12.18},"fy_end_month":1,"eps_basis":"基期 FY2026A 為 GAAP 稀釋 EPS 3.07 美元（含出售車用乙太網路事業一次性利益，事實表未提供非 GAAP 基期）；FY2027E–FY2029E 為 Koyfin 共識（2026-10-08 快照，口徑判斷為非 GAAP），兩者口徑不同，三年年複合僅作參考；財年止於 1 月"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRVL_20261012/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"fabless 設計案黏著（單一來源、跨代沿用）疊加 AI 資本支出循環；FY24–FY25 營收低谷期 GAAP 營業虧損、毛利率約 41%"},"industry":{"clock_phase":"III","sd_verdict_source":"BofA 雲端業者自由現金流預估與 2027 年見頂共識（TFTC 2026-09）、Moody's 資本支出預估（DatacenterDynamics 2026-09）、FactSet 發債統計（2026-07）","bargaining":{"up":"台積電先進製程、CoWoS 與 HBM 為瓶頸，Marvell 以五年預測與約 10 億美元預付鎖產能，上游強勢","down":"前十大客戶占 82%，四大雲端占成長絕大部分，Google 長約附認股權屬讓利，下游強勢","geo":"多數晶圓在台灣同一區域代工，封測分布於中國、馬來西亞、新加坡、台灣、加拿大"},"profit_pool_dir":"AI 資料中心利潤池往加速器與 HBM 集中；連接與客製設計的池子在擴大，但 Marvell 分到的毛利率低於 Broadcom 與 Nvidia","tam_table":[{"item":"2030 曆年可定址市場（公司估）","value":"約 4,000 億美元，較前次放大約 4 倍；前提為 2030 年資料中心資本支出約 3 兆美元（投資人日 2026-10-06）"},{"item":"客製市場與目標份額（公司估）","value":"客製 TAM 約 2,350 億美元，FY31 客製中點約 300 億美元、約 13% 份額；2024 年公司估 XPU 客製 TAM 為 400 億美元"},{"item":"互連（公司估）","value":"FY31 中點約 375 億美元、中點年複合約 65%；FY27 年增逾 70%"},{"item":"交換器與儲存（公司估）","value":"FY31 中點約 100 億美元；Teralynx 明年逾 10 億美元"},{"item":"XPU attach（公司估）","value":"一年前估約 150 億美元，現稱已放大數倍；每顆 XPU 一到兩個 socket、單價約 1,000 美元"},{"item":"第三方份額對照","value":"JPMorgan 估 Broadcom 占高階 ASIC 80–85%、Marvell 10–12%；Counterpoint 估 Marvell 2027 年約 8%"},{"item":"營業利益池占比 5 年前→現在","value":"事實表未涵蓋"}]},"moat":{"mechanism":"設計案轉換成本＋高速 SerDes／光電 IP 廣度：客製晶片流片後為單一來源、attach socket 跨代沿用；互連端靠 1.6T DSP 首發與 TIA／驅動份額","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"對最強同業 Broadcom：TTM GAAP 營益率 16.81% 對 48.52%、FCF 利潤率 18.23% 對 44.22%，投入資本事實表未涵蓋、以利潤率差代替 ROIC spread，差距約 32pp 且無收窄證據（同業僅 TTM 單點）；客戶側 AWS 為差距顯著的最大客戶，次世代 Trainium 傳轉 Alchip（未證實），JPMorgan 則稱現世代與次世代無份額流失","threats":[{"level":"🔴","text":"Broadcom 生態型攻擊：客製加速器份額估 55–85%、路線圖能見度較高（HSBC），同時以 Tomahawk 交換器與 3 奈米 Taurus 光 DSP 正面競爭，Microsoft 傳評估改用其設計","p":"40%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#3","substitute_technology#0","customer_second_source#3"]},{"level":"🟡","text":"台系設計服務與聯發科以低毛利搶 XPU 專案：Alchip、GUC 造成毛利壓力，聯發科瞄準 2027 年 20% 可服務市場，Trainium 3／4 傳轉 Alchip（未證實）；屬破壞性價格競爭","p":"35%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#4","substitute_technology#1","supply_demand_durability#1","customer_second_source#2"]},{"level":"🟡","text":"雲端客戶自研晶片：10-Q 警告大客戶可能自行開發並製造半導體方案，導致業務流失","p":"25%","evidence_refs":["customer_second_source#1"]},{"level":"🟡","text":"光互連路線與價格競爭：LPO 去模組 DSP、800G 可插拔與相干 DSP 份額之爭轉激烈、Broadcom 與 MaxLinear 以約低四成報價送樣；Marvell 自身也賣 LPO／NPO／CPO 元件，屬點對點而非架構全面替代","p":"30%","evidence_refs":["competitive_share_entrants#5","competitive_share_entrants#6","substitute_technology#3","substitute_technology#4"]}],"roic_durability":{"quadrant":"高利益率×低周轉（非 GAAP 營益率 36.6% 屬高利益率；投入資本含約 110 億美元併購商譽、周轉率低；精確投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（模型開發與推論服務）、決策者（雲端架構團隊）、付款者（雲端資本支出）三角都成立，光互連被點名為新瓶頸、屬需要而非想要；但付款端自由現金流轉負、靠舉債支撐，急迫性高不等於持久性高"},{"item":"決策層級","level":"🟡","text":"替代性要在單一晶片世代的設計案層級看：流片後為單一來源、開發週期約兩年（Q1 FY27 法說），世代內幾乎不可替換；但每次換代重新競標，AWS 次世代傳聞正落在這個節點"},{"item":"價值鏈分配","level":"🟡","text":"稀缺環節在台積電先進製程、CoWoS（2026 年 Nvidia 約占六成）與 HBM，Marvell 需預付約 10 億美元鎖產能；下游四大客戶議價力強，Google 長約附認股權即是讓利；Marvell TTM 毛利率 52.2% 遠低於 Broadcom 68.8%，夾在兩端"},{"item":"社會容忍度","level":"🟡","text":"非民生必需品，沒有漲價的政治天花板；但資料中心用電的社會反彈（CEO 於 Citi 會議提及）、Section 232 半導體關稅與對中國出口許可屬政策風險，從客戶需求與成本兩端間接設限"}],"roiic":"事實表未涵蓋（投入資本與折舊攤銷序列缺）。方向判讀：fabless 有機成長所需實體資本低（Q2 資本支出 1.27 億美元對營業現金流 6.06 億美元），但近五年約 110 億美元併購與 FY27 約 10 億美元產能預付拉高增量投入，GAAP 口徑的增量報酬尚未證明高於資金成本","reinvest_rate":"事實表未涵蓋（折舊攤銷、營運資金變動、併購淨額未收錄）","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率；本輪兩項輸入皆缺，天花板不給數字，共識缺口歸因寫在成長段"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","MRVL":52.21,"NVDA":74.67,"AVGO":68.77,"AMD":53.2,"3661.TW":37.2,"unit":"%"},{"metric":"營業利益率","MRVL":16.81,"NVDA":65.21,"AVGO":48.52,"AMD":15.71,"3661.TW":24.0,"unit":"%"},{"metric":"FCF 利潤率","MRVL":18.23,"NVDA":41.92,"AVGO":44.22,"AMD":20.34,"3661.TW":-10.46,"unit":"%"},{"metric":"研發密度","MRVL":25.84,"NVDA":7.79,"AVGO":13.28,"AMD":22.74,"3661.TW":9.17,"unit":"%"}],"competitors":[{"name":"NVDA","gm":74.67,"om":65.21,"fcf_margin":41.92,"rd_intensity":7.79,"period":"TTM ending 2026-07-31（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"period":"TTM ending 2026-07-31（4季加總）"},{"name":"AMD","gm":53.2,"om":15.71,"fcf_margin":20.34,"rd_intensity":22.74,"strategy_note":"利潤率結構與 Marvell 相近（毛利率 53.2%、營益率 15.7%），屬 GPU 供應方而非客製設計對手，影響在雲端客戶 GPU 與自研晶片的預算分配","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3661.TW","gm":37.2,"om":24.0,"fcf_margin":-10.46,"rd_intensity":9.17,"period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（AI 資料中心出貨量與每顆 XPU 連接、attach 內容增加），價為次（1.6T 對 800G 升級，客製毛利較低）；併購貢獻小；回購只抵銷稀釋","runway_years":"6–8（公司 FY31 營收中點約占其估 2030 年可服務市場 20%，若市場不再擴大約 FY33 觸及 30%；市場規模與份額皆為公司估計）","runway_post_y5":"🟢","endo_ceiling_basis":"內生天花板無法以事實表算出（投入資本、折舊攤銷缺）；共識 FY27→FY29 EPS 兩年年複合約 70%，遠超 fabless 增量報酬×再投資率可支撐的區間，保守視為超出；缺口主要來自客戶資本支出驅動的量增與營業槓桿，依賴產業順風","segments":[{"item":"資料中心（Q2 FY27）","value":"21.72 億美元、占 79%、年增 46%、季增 18%；Q3 指引季增逾 20%、年增約 75%（法說會）"},{"item":"通訊及其他（Q2 FY27）","value":"5.68 億美元、年增 10%；Q3 預期季減與年減十幾個百分點，Q4 回升（法說會）"},{"item":"客製（XPU＋attach）","value":"FY27 下半年顯著放量、FY28 年增逾一倍、FY29 為 FY28 三倍以上逾 120 億美元、FY31 中點約 300 億美元（投資人日）"},{"item":"互連（光 DSP、TIA／驅動、DCI、AEC）","value":"FY27 年增逾 70%、FY31 中點約 375 億美元；TIA／驅動與 DCI 各朝年化 10 億美元（法說會、投資人日）"},{"item":"交換器與儲存","value":"scale-out 交換器 FY27 逾 6 億美元、Teralynx FY28 逾 10 億美元、FY31 中點約 100 億美元（Q1 法說、投資人日）"},{"item":"scale-up 光學（NPO／CPO）","value":"目前幾乎無營收，FY28 數億美元起步（上季口徑約 3 億美元，本季稱大幅高於此）"},{"item":"組合對毛利率","value":"客製占比上升使毛利率逐步下降，FY31 目標 56–59%；連接超預期則趨向高端"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"非 GAAP 毛利率 Q1、Q2 FY27 皆 58.9%，Q3 指引 57.5–58.5% 季減；去年同期值事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"Counterpoint 估客製 AI ASIC 份額 2027 年降至約 8%、JPMorgan 估 10–12%（屬預估非實現）"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"無證據"},{"signal":"EPS 年複合高於營收年複合逾 5pp","lit":false,"note":"FY28 共識 EPS 年增約 72%、管理層營收約年增 67%，差約 5pp 邊緣，屬營業槓桿擴張且口徑混用，不計入"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"FY26 為 0.52 但淨利含出售車用乙太網路事業利益；FY24、FY25 淨利為負不適用"},{"signal":"SBC／營收逾 5% 且逐年上升","lit":true,"note":"Q2 FY27 為 11.9%、約占 GAAP 營業利益 71%；逐年走勢事實表未涵蓋，以水準過高計入"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"LPO／CPO 對模組 DSP 有替代壓力，但未見市場萎縮證據"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"倍數在可得區間頂部"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"Q2 總資本支出 1.27 億美元對 FCF 4.79 億美元約 26%"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"相反，正預付產能"}],"trap_rating":"價值陷阱風險🟡（亮 2 項）／長期成長性🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自有機的互連與客製放量，近期併購（Celestial AI、XConn、Polariton）只貢獻 scale-up 光學起步而非成長主力；回購僅抵銷稀釋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"FY21–FY26 併購約 110 億美元（投資人日 CFO）；同期 GAAP 營益率 FY23 6.07%、FY24 −7.93%、FY25 −6.35%、FY26 16.33%，到 FY26 才轉為營業獲利，併購資產的已實現增量報酬未證明高於資金成本","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"Q2 回購 2 億美元；回購均價事實表未涵蓋，以判斷日前瞻本益比 65.23 倍換算盈餘殖利率約 1.5%，低於 10 年期公債殖利率加 2%（公債殖利率事實表未涵蓋，但任何正值加 2% 皆高於 1.5%）","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 指引稀釋加權股數約 9.21 億、與 Q2 大致持平（CFO），每季 3.26 億美元 SBC 由約 2 億美元回購抵銷；Google 認股權與 NVIDIA 入股為另一稀釋來源，規模本包未揭露，年度淨稀釋率事實表未涵蓋","grade":"過"}]},"valuation":{"basis":"前瞻本益比（非 GAAP 共識 EPS），以市場現給 FY29 共識的 22.6 倍作終端倍數的內部對照","tier":"AI 半導體高成長","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋（同業對照只有利潤率），無法建同層級倍數對照"},"fwd_pe":65.23,"peg":0.93,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"前瞻本益比 65.23 倍、P/S 26.18 倍位於可得 4 個年度端點最高（分位 100，非五年連續序列）；基準五年年化約 11%（中）、上下檔比約 2.8；股價高於投資人日前賣方平均目標價；FY28 共識倍數由前份約 32 倍升至 38 倍，結論由合理偏貴轉為偏貴","upside_short_pct":13,"upside_mid_pct":53},"trap_analysis":{"verdict":"🟡","label":"高估值成長股、非價值陷阱；亮燈在第三方份額下滑估計與 SBC 占營收 11.9%"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"BofA 估雲端業者合計自由現金流 2027 年 −1,440 億、2028 年 −1,860 億美元，市場共識傾向 2027 年資本支出見頂後持平；Q1 美國超大型業者直接發債 1,150 億美元，已超過 2025 全年 700 億","assumption":"管理層 FY31 模型假設客戶資本支出增速尾端仍約 20%、不轉負","consequence":"FY29 之後客製放量遞延、互連訂單消化，EPS 由約 7.6 美元回落到 5.6 美元谷底，倍數由 65 倍壓到 17 倍，五年後股價約 116 美元（−58%）","ruling":"部分採納：放進空頭情境、機率 30%，與唯一致命點是同一件事，兩處一致；不再往上加，因 Moody's 估新增約 7,000 億美元 RPO 撐住多年需求、公司稱 FY28 所需供給已到位","watch":"四大雲端每季資本支出指引；Marvell 下季營收指引是否季減","evidence_refs":["supply_demand_durability#4","customer_concentration_credit#3"],"fact_refs":["f_consensus_eps_fy3","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"前十大客戶占 FY26 營收 82%，一家經銷商約 37%（第三方彙整），10-Q 稱 AWS 是差距顯著的最大客戶；Benchmark 稱 Trainium 3／4 設計輸給 Alchip，Microsoft 評估 Broadcom；10-Q 亦警告大客戶可能自製晶片","assumption":"四大客戶各自多世代留在 Marvell","consequence":"單一客戶換代即可吃掉客製成長的一大段","ruling":"採納為中期風險，但不升為唯一致命點：管理層稱 FY31 目標不需新勝案、產品面分散，單一客戶流失的衝擊小於資本支出整體反轉","watch":"10-Q 客戶集中度揭露、AWS 次世代 Trainium 設計夥伴","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0","customer_second_source#1","customer_second_source#2","customer_second_source#3"],"fact_refs":["f_kpi1"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 占營收 11.9%、約為 GAAP 營業利益 71%；Q3 指引 GAAP EPS 0.53 美元對非 GAAP 1.10 美元；Google 長約附認股權、NVIDIA 20 億美元入股，客戶以股權分享成長；FY27 約 10 億美元產能預付；TTM 自由現金流利潤率 18.2%，遠低於管理層長期逾 36% 目標","assumption":"非 GAAP EPS 代表股東實得盈餘、回購足以抵銷稀釋","consequence":"營收照目標成長，但每股可得現金被 SBC、客戶認股權與預付款分走一截，以非 GAAP 本益比估值會高估股東報酬","ruling":"採納：情境樹淨回購殖利率設 0、不給回購加分；SBC 淨稀釋目前被回購抵銷，但認股權規模本包未揭露，列監測","watch":"稀釋股數逐季、SBC 占營收、Google 認股權行使條件與股數","evidence_refs":[],"fact_refs":["f_kpi5_sbc_gaap","f_kpi4_605_5m_capex_126_7m","f_peer_mrvl_fcf_margin_pct","f_kpi3_gaap","f_kpi2_non_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"客製占比提高拉低毛利率（Q3 指引 57.5–58.5% 低於 Q2 58.9%）；世芯以 37.2% 毛利率、−10.5% FCF 利潤率搶專案；先進封裝產能 2026 年由 Nvidia 約占六成，自研晶片與其他客戶搶同一批台積電產能","assumption":"營收成長能同比例轉成利潤","consequence":"價值鏈兩端（晶圓與封裝產能、雲端客戶）多拿，Marvell 營收倍增但毛利率往 56% 下緣走","ruling":"部分採納：基準 EPS 已低於管理層 FY31 目標，吸收部分壓力；毛利率連 2 季跌破 57.0% 時改判為價格戰","watch":"非 GAAP 毛利率逐季","evidence_refs":["geo_supply_chain#3","competitive_share_entrants#1"],"fact_refs":["f_kpi6_gaap_non_gaap","f_kpi7_q3_fy2027_2026_10_31","f_peer_3661_tw_gross_margin_pct","f_peer_3661_tw_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"26 週漲 114.34%；前瞻本益比 65.23 倍、P/S 26.18 倍在可得年度端點最高；股價高於 7–8 月賣方平均目標價 245–261 美元（投資人日前資料）；前份判斷以來六週漲 27%","assumption":"市場給 FY29 共識 22.6 倍代表已充分折現長期目標","consequence":"基準情境年化約 11%，多數上檔已在價格內；若 Q3 只是符合指引，倍數可回到 FY28 共識 32 倍（約 232 美元）","ruling":"採納：不追，進場條件綁 FY28 共識 32 倍","watch":"股價對 FY28 共識 EPS 倍數","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_ps_percentile","f_price_at_dd"]}],"max_dd":{"lo":-65,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 216.62 → 本次 275.28（+27.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=216.62","side_b":"本次 price_at_dd=275.28","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟡→🟠、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"AWS 次世代 Trainium 設計歸屬","cause":null,"prior_field":null,"side_a":"Benchmark 降評稱 Trainium 3／4 設計輸給 Alchip，Dolphin Research 亦有轉向傳聞；10-Q 自承 AWS 是差距顯著的最大客戶，轉換設計夥伴會重大影響營收","side_b":"管理層 2026 年 3 月稱 FY26 看不到 Amazon 營收中斷、否認失去 Amazon 或 Microsoft；投資人日稱客製專案皆為單一來源、目標不需新勝案；Q2 FY27 資料中心季增 18%、Q3 指引季增逾 20%","ruling":"不可調和（一邊是失去下一代、一邊是沒有中斷），但兩邊的時間窗不同：管理層證據蓋到 FY27，傳聞指向的 Trainium 3／4 放量落在 FY28–FY29。現有證據不蓋風險窗，裁定不可裁決至 2027 年中；在此之前不稱風險已解，基準情境不扣 AWS，空頭情境吃進此風險","evidence_level":"二手報導（未經公司證實）對公司口頭說法","settle_metric":"FY28 上半年客製營收年增率是否 ≥100%；10-Q 最大客戶占比與客戶揭露","if_then":["若 10-Q 或法說會確認 AWS 次世代主力 XPU 改由他家設計，且 FY28 客製倍增目標下修→持有部位減碼一半，未持有則撤回進場價位並重跑判斷","反向：若 FY28 上半年客製營收年增 ≥100% 且 AWS 仍列最大客戶→移除此風險，進場價位上調至 FY28 共識 EPS 的 35 倍"],"evidence_refs":["customer_second_source#0","customer_second_source#2","competitive_share_entrants#1","customer_concentration_credit#1"]},{"axis":"管理層長期模型對客戶資本支出路徑","cause":null,"prior_field":null,"side_a":"管理層 FY31 模型：資料中心營收中點年複合約 65%、營收 700–900 億美元、EPS 逾 30 美元，假設資本支出增速尾端約 20%；CEO 自稱這是三年押注而非五年","side_b":"市場共識傾向 2027 年資本支出見頂後持平，BofA 估雲端業者合計自由現金流 2026–2028 年由 −640 億擴大到 −1,860 億美元，Goldman 估 2027 年 AI 資本支出約三分之一靠舉債","ruling":"不可調和，選資本支出共識側作基準：Marvell 年增 65% 而客戶支出年增 20%，代表份額或單位內容每年要擴大約 1.4 倍、連續五年，超過現有證據；管理層目標只放進多頭情境（25%），基準取其六到七成","evidence_level":"公司長期模型對第三方資本支出與現金流預估","settle_metric":"四大雲端 2027–2028 年資本支出指引年增率；Marvell FY29 客製營收是否 ≥120 億美元","if_then":["若 FY29 客製營收 ≥120 億美元且四大雲端 2028 年資本支出指引仍年增 ≥15%→基準 EPS 上調到管理層目標八成並重跑，首倉後可加碼至 4%","反向：若任一年度四大雲端合計資本支出指引年減→改用空頭路徑，持有部位減碼至半倉"],"evidence_refs":["supply_demand_durability#4","customer_concentration_credit#3","supply_demand_durability#3"]},{"axis":"毛利率走向","cause":null,"prior_field":null,"side_a":"CFO：FY28 毛利率與 FY27 下半年同區間（57.5–58.5%），FY31 目標 56–59%；客製有客戶出資 NRE 沖減研發，營益率仍可擴張","side_b":"客製占比上升時毛利率逐步下降（CFO 於 Citi 會議），Q3 指引較 Q2 的 58.9% 下滑；800G 光 DSP 有 Broadcom、MaxLinear 以約 50–60 美元對 Marvell 90–100 美元送樣認證；財報後盤後下跌約 2% 即反映毛利率走低","ruling":"可調和（程度差異）：毛利率走低是組合使然、公司已提前揭露，營益率由營業費用增速約為營收一半撐住；真正的分界是跌破指引下緣，那代表價格戰而非組合","evidence_level":"公司指引對第三方報價資料（2025 年 5 月）","settle_metric":"Q3–Q4 FY27 非 GAAP 毛利率實際值","if_then":["若非 GAAP 毛利率連 2 季低於 57.0%→持有部位減碼至半倉","反向：若 Q4 FY27 毛利率 ≥58% 且營益率 ≥38%→組合衝擊已吸收，可依進場條件建倉"],"evidence_refs":["competitive_share_entrants#5","capital_markets_pricing#3"]},{"axis":"客製加速器份額","cause":null,"prior_field":null,"side_a":"Counterpoint 估 Marvell 客製 AI ASIC 份額 2027 年降至約 8%，JPMorgan 估 Broadcom 占高階 ASIC 80–85%、Marvell 10–12%；聯發科瞄準 2027 年 20% 可服務市場","side_b":"管理層稱客製出貨四大美國雲端、20 件以上設計案，FY31 客製 300 億美元約占其估 2,350 億美元客製市場 13%；JPMorgan 另稱 Microsoft、AWS 現世代與次世代無份額流失","ruling":"可調和：第三方多以加速器出貨顆數算份額，管理層算的是含 XPU attach 的營收，而 Marvell 的成長愈來愈靠 attach 與連接；份額下滑估計計為一個衰退訊號，但不改護城河方向","evidence_level":"第三方預估對公司營收口徑","settle_metric":"FY28 客製營收（含 attach）與第三方下一版份額估計","if_then":["若 FY28 客製營收未達倍增且第三方份額估計續降→護城河方向改為縮減並重跑判斷","反向：若 FY28 客製倍增達成→維持方向持平"],"evidence_refs":["end_markets#3","competitive_share_entrants#0","competitive_share_entrants#4","supply_demand_durability#1","substitute_technology#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"五個月內 FY28 營收展望三度上調（165→180→200 億美元），FY29 共識 EPS 一季上修 17%；以 FY29 共識計本益比只有 22.6 倍、兩年 EPS 年複合約 70%，若 FY31 達 30 美元則現價約 9 倍","side_b":"上修集中在客戶資本支出最熱的一年，FY31 目標連管理層都稱超出三年能見度；26 週已漲 114%、P/S 在可得區間頂部，基準五年年化約 11% 只算中等；空頭 30% 機率下跌約 58%","ruling":"不追：買進論證成立的前提是 FY29 之後的成長，那段沒有可驗證證據；等價格給出更好的上下檔比","evidence_level":"公司指引與共識對情境推算","settle_metric":"股價對 FY28 共識 EPS 倍數","if_then":["若股價回落至 FY28 共識 EPS 32 倍以下（約 232 美元）且毛利率守 57.5%→重跑判斷後以 2% 首倉進場","反向：若股價續漲而 Q3 財報前證據未更新→不追"],"evidence_refs":[]},{"axis":"估值與上下檔比（股價 216.62→275.28 美元，+27%）","cause":"價格變動","prior_field":["signal","val","asym_ratio","ev5y_pct","irr_base_pct","max_dd_pct"],"side_a":"前份：估值合理偏貴、綜合評級 A、上下檔比 4.3、基準年化 10.9%、五年期望 +64.6%、最大回撤 −48%、裁決觀望","side_b":"本次：股價六週漲 27%，FY28 共識 EPS 只上修約 7%，FY28 倍數由約 32 倍升至 38 倍，估值轉偏貴、綜合評級降為 B；基準年化約 11%（遠年 EPS 上修抵銷）、上下檔比約 2.8、最大回撤範圍 −50%～−65%；裁決與倉位角色隨新輸入重算","ruling":"估值結論與綜合評級下調的主因是價格先走、近年 EPS 跟得慢；基準報酬沒降是遠年上修抵銷，屬不同年期互抵，不視為變便宜；上下檔比下降另含多頭機率由 30% 降至 25%","evidence_level":"事實表股價與共識快照","settle_metric":"股價對 FY28 共識 EPS 倍數","if_then":["若股價回落至 FY28 共識 EPS 32 倍以下→估值結論回到合理偏貴並重跑進場","反向：若 FY28 共識再上修 10% 以上而股價不動→同樣達到價位條件"],"evidence_refs":[]},{"axis":"投資人日與 Google 長約後的長期假設","cause":"新證據","prior_field":["bull_5y_price","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：多頭五年價 570.3 美元、護城河持平、Y5 後跑道寬、品質複利成長型、未給循環位置","side_b":"本次：投資人日把 FY28 營收上調至約 200 億美元、FY31 給 700–900 億美元與 EPS 逾 30 美元，揭露 Google 6.5 年 1,200 億美元客製機會；多頭五年價升至約 816 美元；護城河方向、跑道、類型與循環位置不變","ruling":"新證據抬高多頭天花板，不改方向判斷：執行面擴大被定價面縮減抵銷，Trainium 傳聞未解，仍標持平；跑道寬由管理層點名的第二曲線支撐，但市場規模屬公司估計；類型維持品質複利成長，循環屬性以次要類型與空頭情境處理，不另給循環位置","evidence_level":"公司投資人日與 8-K","settle_metric":"FY28 客製營收、Q4 FY27 營益率","if_then":["若 FY28 客製倍增且 Q4 FY27 營益率 ≥38%→重審護城河執行面是否轉為擴大","反向：若 AWS 次世代確認外流→護城河改縮減並重跑判斷"],"evidence_refs":["end_markets#1","customer_second_source#2"]},{"axis":"情境定義與陷阱計數","cause":"方法變動","prior_field":["trap","bear_5y_price","p_bull_pct","p_bear_pct"],"side_a":"前份：陷阱風險低、空頭五年價 134.1 美元、多頭與空頭機率各 30%","side_b":"本次：陷阱風險中（亮 2 項：第三方份額下滑估計、SBC 占營收 11.9%）、空頭五年價約 116 美元（終端 17 倍、EPS 不高於 FY28 共識）、多頭機率 25%、空頭 30% 不變","ruling":"兩項亮燈證據前份已存在，變的是計數口徑：本次把 SBC 水準與第三方份額預估計入；多頭改定義為管理層 FY31 目標約九成兌現，門檻比前份高，機率相應下調；空頭終端倍數改用成長熄火至約 10% 的 17 倍","evidence_level":"口徑調整","settle_metric":"SBC 占營收逐季走勢、第三方份額估計","if_then":["若 SBC 占營收降至 8% 以下且份額估計止跌→陷阱風險回到低","反向：若 SBC 占營收逐季上升→陷阱風險升為高並減碼至半倉"],"evidence_refs":["end_markets#3"]},{"axis":"首倉進場條件（估值重啟）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"三旗艦socket任一正面確認＋GM守57.5-58.5%","side_b":"股價回落至FY2028E共識EPS的32倍以下（以7.25美元計約232美元）且最近一季非GAAP毛利率≥57.5%","ruling":"前份條件未發火：投資人日只說客製出貨四大雲端，沒有客戶端對特定旗艦世代的確認，Q3 毛利率實際值未出。股價六週漲 27% 後，卡住首倉進場的是倍數而非證據，故首倉進場與後續加碼條件改綁 FY28 共識本益比；毛利率守 57.5% 保留為論點完好的前提","evidence_level":"價格與共識快照","settle_metric":"股價÷FY28 共識 EPS；最近一季非 GAAP 毛利率","if_then":["若條件達成→重跑判斷後首倉進場 2%","反向：若 Q3 毛利率跌破 57.5%→進場條件作廢，改看減碼條件"],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"四大美國雲端業者合計年度資本支出指引首次轉為年減","ruling":"前份把客戶資本支出放在風險清單而未指定唯一致命點；本次以數學敏感度選定：資本支出年減同時打到客製、互連、交換器三條線並觸發倍數壓縮，對 Y5 EPS 的衝擊大於任一單一客戶事件；發生即減碼至半倉","evidence_level":"第三方資本支出與現金流預估","settle_metric":"四大雲端年度資本支出指引年增率","if_then":["若合計指引首次年減→持有部位減碼至半倉，未持有則撤回進場條件","反向：若 2027 年指引年增 ≥15%→維持基準"],"evidence_refs":["supply_demand_durability#4"]},{"axis":"出場門檻（減碼與清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）","side_b":"毛利率連 2 季低於 57.0%→減碼至半倉；FY28 營收展望低於 180 億美元且 FY29 客製目標下修→清倉；AWS 次世代外流確認→減碼一半；四大雲端資本支出年減→減碼至半倉","ruling":"前份只有進場條件、沒有減碼與清倉門檻，本次補齊；之後降位也保留指標、門檻與資料來源","evidence_level":"口徑補齊","settle_metric":"各門檻對應的季報與指引","if_then":["若任一減碼門檻觸發→依門檻動作並重跑判斷","反向：若四項皆維持正常至 FY28 年報→門檻依新共識上調"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回落至 FY28 共識 EPS 32 倍以下且毛利率守 57.5%：重跑判斷後首倉 2%","type":"估值rearm","maps_to":"H3","metric":"股價÷FY2028E 共識 EPS","threshold":"≤32 倍（以 7.25 美元計約 232 美元）且最近一季非 GAAP 毛利率 ≥57.5%","action":"重跑判斷後首倉 2%","source_freq":"每日股價／每月共識快照","date":null,"evidence_refs":[]},{"n":2,"text":"Q3 FY27 財報驗證資料中心加速與毛利率指引","type":"假設驗證","maps_to":"H1","metric":"資料中心季增率、總營收、非 GAAP 毛利率","threshold":"資料中心季增 ≥20%、營收在 29.9–33.1 億美元、毛利率 57.5–58.5%、Q4 指引續季增","action":"達標：依新共識重算進場價；未達：凍結進場至 Q4 財報","source_freq":"每季財報","date":"2026-12","evidence_refs":[]},{"n":3,"text":"Q4 FY27 營益率進入長期目標區間且 FY28 約 200 億美元重申：已持有首倉則加碼","type":"加碼","maps_to":"H3","metric":"非 GAAP 營益率；FY28 營收展望","threshold":"Q4 FY27 營益率 ≥38% 且 FY28 展望 ≥200 億美元","action":"加碼至 4%","source_freq":"每季財報","date":"2027-03","evidence_refs":[]},{"n":4,"text":"四大美國雲端業者合計年度資本支出指引首次轉為年減","type":"Single Thing","maps_to":"R3","metric":"四大雲端合計年度資本支出指引年增率","threshold":"首次轉為年減","action":"持有部位減碼至半倉；未持有則撤回進場條件、重跑判斷","source_freq":"每季（各公司季報）","date":"2027-02","evidence_refs":["supply_demand_durability#4","customer_concentration_credit#3"]},{"n":5,"text":"AWS 次世代 Trainium 確認改由他家主導設計","type":"風險","maps_to":"R1","metric":"AWS 次世代 Trainium 設計夥伴","threshold":"公司或 AWS 確認改由他家主導","action":"減碼一半並重跑判斷","source_freq":"每季 10-Q／法說會","date":null,"evidence_refs":["customer_second_source#0","customer_second_source#2"]},{"n":6,"text":"非 GAAP 毛利率連 2 季跌破 57.0%，判為價格戰","type":"減碼","maps_to":"R2","metric":"非 GAAP 毛利率","threshold":"連 2 季 <57.0%","action":"減碼至半倉","source_freq":"每季財報","date":null,"evidence_refs":["competitive_share_entrants#5"]},{"n":7,"text":"FY28 營收展望與 FY29 客製目標同時下修","type":"清倉","maps_to":"H1","metric":"FY28 營收展望；FY29 客製營收目標","threshold":"FY28 展望低於 180 億美元且 FY29 客製目標下修至 FY28 兩倍以下","action":"清倉","source_freq":"每季法說會／投資人日","date":null,"evidence_refs":[]},{"n":8,"text":"股價先於 EPS 衝高：持有部位分批獲利了結","type":"減碼","maps_to":"H3","metric":"股價÷FY2028E 共識 EPS","threshold":"≥55 倍（以 7.25 美元計約 400 美元）且 FY29 共識未同步上修","action":"持有部位減碼三分之一","source_freq":"每日股價／每月共識快照","date":null,"evidence_refs":[]},{"n":9,"text":"Section 232 半導體關稅第二階段涵蓋 Marvell 主要產品並傷及毛利率","type":"風險","maps_to":"R4","metric":"Section 232 涵蓋範圍與公司毛利率指引","threshold":"涵蓋主要產品且毛利率指引因此下修 ≥100bp","action":"減碼至半倉","source_freq":"政策公告／每季財報","date":null,"evidence_refs":["reg_tariff_export#1","regulatory_antitrust#2"]},{"n":10,"text":"Q3 FY27 財報後複審","type":"複審日期","maps_to":"H1","metric":"全部論點與門檻","threshold":"財報公布","action":"重跑判斷","source_freq":"每季","date":"2026-12","evidence_refs":[]}],"kill_metrics":[{"metric":"非 GAAP 毛利率（季）","bear_threshold":"連 2 季 <57.0%（低於指引下緣 57.5%）","window":"Q3–Q4 FY27 財報（2026-12、2027-03）","source":"公司季報新聞稿","last_status":"ok"},{"metric":"資料中心營收對當季指引","bear_threshold":"單季實際低於指引區間下緣，或下季指引季減","window":"每季財報","source":"公司季報新聞稿與法說會","last_status":"ok"},{"metric":"FY2028 營收展望（管理層）","bear_threshold":"由約 200 億美元下修至 180 億美元以下","window":"至 2027-03 年度財報","source":"法說會／投資人日","last_status":"ok"},{"metric":"四大美國雲端業者合計年度資本支出指引","bear_threshold":"任一年度指引合計年減","window":"12–24 個月，每季更新","source":"各公司季報","last_status":"ok"},{"metric":"AWS 次世代 Trainium 設計夥伴","bear_threshold":"公司或 AWS 確認改由他家主導設計","window":"12–24 個月","source":"10-Q 客戶揭露、法說會","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=114.34, valuation_dependent=False","input_gap":["week26_return_pct 落 100-150% 邊界帶，QC-42 反動能閘裁量範圍，本腳本無法自動判定，預設不放行"]},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價回落至FY2028E共識EPS的32倍以下（以7.25美元計約232美元）且最近一季非GAAP毛利率≥57.5%","exec_line":"條件達成先重跑判斷，再以 2% 首倉進場；Q4 FY27 營益率 ≥38% 且 FY28 約 200 億美元重申後加碼至 4%；路徑風險高但論點完整，持有後不因 −50% 以內波動砍倉，只依減碼與清倉條件動作"},"reasoning":{"industry":"Q2 FY27 營收 27.39 億美元，資料中心 21.72 億美元（占 79%、年增 46%），通訊及其他 5.68 億美元（年增 10%，法說會）。非 GAAP 毛利率 58.9%、營益率 36.6%；GAAP 為 53.1%、16.8%，差距主要是 SBC 與併購攤銷。Q3 指引營收 31.5 億美元±5%、非 GAAP 毛利率 57.5–58.5%，下滑來自客製放量的組合效應。錢卡在兩個節點：互連（光 DSP、TIA／驅動、DCI，800G 換 1.6T）與客製加速器及 attach 晶片（設計案綁定、單一來源）。議價權：上游台積電先進製程、CoWoS 與 HBM 稀缺，Marvell 以五年預測加約 10 億美元預付鎖產能；下游前十大客戶占 FY26 營收 82%、一家經銷商約 37%（第三方彙整），AWS 為差距顯著的最大客戶，這是集中度風險而非護城河證據。產業時鐘判為過熱期：客戶資本支出 2026 年約 7,850 億美元、2027 年逼近 1 兆美元，但雲端業者自由現金流轉負、Q1 直接發債 1,150 億美元已超過 2025 全年，屬擴張後段靠舉債延續的特徵；供給仍吃緊，尚未進入收縮。供需持久性：需求屬結構性，但增速預計 2027 年見頂後持平，判為週期性將反轉（反轉的是增速而非總量），這是空頭機率 30% 的來源。產業態勢裁決為雙向拉鋸：競爭面惡化（Broadcom 份額估 55–85%、聯發科瞄準 20% 可服務市場、台系設計服務壓價、800G 光 DSP 對手低價送樣），結構面轉好（光互連被點名為新瓶頸，Moody's 估新增約 7,000 億美元 RPO 支撐多年軌跡）。","moat":"機制是設計案轉換成本加上高速 SerDes 與光電 IP 的廣度：客製專案流片後為單一來源，attach socket 可跨多代 XPU，互連端靠 1.6T DSP 首發（公司稱領先約兩年）與 TIA／驅動份額。執行力評 8：五個月內三度上調展望、客製出貨四大美國雲端、Google 6.5 年 1,200 億美元機會與 NVIDIA 20 億美元入股，Teralynx 交換器已證明能量產大晶片。定價權評 6：Q3 毛利率指引因客製組合較 Q2 下滑，800G 光 DSP 對手以約低四成報價送樣，世芯以 37.2% 毛利率搶單；對最強同業 Broadcom 的利潤率差距大（TTM GAAP 營益率 16.8% 對 48.5%、FCF 利潤率 18.2% 對 44.2%），投入資本事實表未涵蓋、無法算 ROIC spread，以利潤率差替代，未見收窄證據。方向判持平。威脅中 Broadcom 屬生態型攻擊，其餘為點對點。報酬持續期：以非 GAAP 營益率看屬高利益率，投入資本含約 110 億美元併購商譽、周轉率低；四檢查點皆黃，持續期取決於客戶資本支出能否延續、以及每次換代能否守住設計案；增量報酬與再投資率因投入資本、折舊攤銷序列缺而不給數字。","growth":"成長以量為主：資料中心 FY27 預期年增約 60%、投資人日把 FY28 上調為約 80%，來自出貨量與每顆 XPU 的連接、attach 內容增加；1.6T 換代帶來單價升級，但客製產品毛利較低；併購（Celestial AI、XConn、Polariton）只貢獻 scale-up 光學起步；回購只抵銷稀釋。共識 EPS FY27 4.22、FY28 7.25、FY29 12.18 美元，兩年年複合約 70%；FY26 非 GAAP 基期事實表未涵蓋，以 GAAP 3.07 美元算三年年複合約 58%，但 GAAP 基期含出售利益、口徑不一。FY29 共識一季上修 17%，家數事實表未涵蓋。內生天花板無數字，缺口歸因：營益率由 36.6% 擴到 40% 只解釋一小段，其餘是客戶資本支出驅動的量增，無法歸因於公司自身再投資報酬，屬依賴產業順風而非估值重評；長期信心上限中。跑道：以公司估 2030 年 4,000 億美元市場計，FY31 中點 800 億美元約占兩成，若市場不再擴大約 FY33 觸及三成，約 6–8 年、給中等折扣。衰退訊號亮 2 項（第三方份額下滑估計、SBC 占營收過高），價值陷阱風險與長期成長性皆為中。","governance":"現金轉換：Q2 營業現金流 6.06 億美元、資本支出 1.27 億美元，自由現金流 4.79 億美元；營業現金流季減主因產能預付，FY27 預付約 10 億美元。FY26 自由現金流 13.92 億美元對淨利 26.70 億美元約 0.52，但淨利含出售車用乙太網路事業利益；FY24、FY25 淨利為負而自由現金流 10.2、13.9 億美元，轉換率靠 SBC 加回撐起。SBC 3.26 億美元占營收 11.9%、約為 GAAP 營業利益 71%。Q2 現金去向：回購 2 億美元、股利 0.54 億美元、資本支出 1.27 億美元、產能預付；近三年四分結構事實表未涵蓋。三項計分：併購已實現增量報酬未證明高於資金成本，不過；回購盈餘殖利率約 1.5%，不過；稀釋股數與上季持平，過，但 Google 認股權與 NVIDIA 入股屬另一條稀釋來源、規模本包未揭露。負債 49.6 億美元、淨負債／EBITDA 0.27 倍，資產負債表安全。CFO 於 6 月更替（Willem Meintjes 離任、前董事 Dan Durn 接任），屬重大事件，但交接有序、指引口徑未變，不涉核心假設。","valuation":"判斷日股價 275.28 美元：對 FY27 共識 EPS 4.22 為 65.23 倍、FY28 7.25 為 38.0 倍、FY29 12.18 為 22.6 倍；trailing 本益比 90.55 倍（GAAP、含出售利益），P/S 26.18 倍、EV/S 26.32 倍皆在可得 4 個年度端點的最高。PEG 以 FY27→FY29 兩年 EPS 年複合約 70% 計為 0.93，但成長集中在資本支出最熱的兩年，PEG 偏低不代表便宜。反推：以 22 倍終端倍數換約 11% 年化，FY32 EPS 需約 21 美元。短期上檔：一年後以 FY28 基準 EPS 7.4 美元×42 倍約 311 美元（+13%）；中期：三年後以 FY30 基準 15 美元×28 倍約 420 美元（+53%）。賣方 7–8 月平均目標價 245–261 美元低於現價，但屬投資人日前資料；目標價全距 105–400 美元約 3.8 倍，賣方分歧大，對自身上下檔比的信心相應下調。","premortem":"最可能看錯的三處：一是客戶資本支出時點，BofA 估雲端業者自由現金流 2027 年 −1,440 億美元、共識預期 2027 年見頂後持平，與管理層 FY31 模型假設的約 20% 增速衝突；二是 AWS 次世代設計歸屬，傳聞指向的放量窗在 FY28–FY29，現有證據蓋不到；三是管理層問答迴避處：超額下單風險未正面回答、Google 認股權在 FY31 只計入部分價值卻不給比例、互連 TAM 拒絕拆數字。路徑風險：空頭終點約 −58%，FY30 谷底若倍數同步壓縮可到約 −65%，屬深回撤；論點本身完整（護城河持平、跑道寬、非估值依賴），持有後不因波動砍倉，進場前先做好深回撤心理準備。壓力檢核四項過二：淨負債／EBITDA 0.27 倍、FY24–FY25 營收低谷期自由現金流仍為正；同期毛利率跌到約 41%、GAAP 營業虧損，兩項不過。陷阱判為中：高估值成長股而非價值陷阱。"},"plain":{"six":{"how_it_makes_money":"賺四大美國雲端業者 AI 建置的錢：資料中心占營收 79%，獲利卡在互連（光 DSP 與 TIA／驅動）與客製加速器及 attach 晶片兩個節點，上游產能與下游大客戶兩端的議價力都比 Marvell 強","moat":"護城河方向持平：執行面擴大（全連接堆疊、客製出貨四大美國雲端、Google 長約），定價面縮減（客製組合拉低毛利率、800G 光 DSP 對手約低四成報價），兩者相抵；最大客戶次世代有流失報導未證實，證實前不給上升","growth":"Y5 後跑道寬：管理層點名的 scale-up 光學、scale-up 交換器、跨資料中心 DCI、XPU attach 都還在起步，以公司估的市場規模計 FY31 中點只占約兩成；但成長是量驅動、押在四大雲端資本支出，FY29 之後落在管理層自稱的三年能見度之外","capital":"資本配置屬中段：回購只抵銷稀釋且買在 65 倍前瞻本益比，過去約 110 億美元併購到 FY26 才轉為 GAAP 營業獲利，SBC 占營收 11.9%；正面是淨負債／EBITDA 僅 0.27 倍，投資人日承諾長期返還逾五成自由現金流","valuation":"現價要求 FY32 非 GAAP EPS 約 21 美元（FY27 共識的五倍）並維持 22 倍，才換得約 11% 年化，等於管理層 FY31 目標兌現約六到七成；我信基準可達，但價格已把它算進去，不追","how_wrong":"最可能看錯在客戶資本支出 2027 年見頂後轉向消化：客製放量遞延、光 DSP 價格戰與 65 倍本益比同步收縮，股價可回到 115 美元上下"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"衛星","wait_for_price":true,"wait_for_price_condition":"等股價回落至 FY2028E 共識 EPS 的 32 倍以下（以 7.25 美元計約 232 美元）且非 GAAP 毛利率守 57.5%；或 Q3 FY27 財報確認資料中心季增 ≥20%、毛利率在指引內後，依新共識重算價位","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":275.28,"week26_return_pct":114.34,"consensus_rev_3m_pct":4.2,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"trailing GAAP 分母含出售車用乙太網路事業一次性利益與併購攤銷，改用前瞻非 GAAP 共識；SBC 占營收 11.9% 未從非 GAAP EPS 扣除，已以淨回購 0 與空頭倍數處理，分母本身不是本檔爭點"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q3 FY27 財報與 Q4 指引","impact":"高","watch":"資料中心季增是否 ≥20%、非 GAAP 毛利率是否落在 57.5–58.5%"},{"date":"2027-02","date_precision":"month","type":"macro","event":"四大雲端 2027 年度資本支出指引（各家第四季財報）","impact":"高","watch":"合計年增率是否仍為正、是否 ≥15%"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"Q4 FY27 財報與 FY28 全年展望","impact":"高","watch":"非 GAAP 營益率是否進入 38–40%、FY28 約 200 億美元是否重申"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"Photonic Fabric 記憶體模組送樣、UALink U115 交換器推出（管理層稱明年）","impact":"中","watch":"scale-up 光學與交換器是否如期貢獻數億美元營收"},{"date":null,"date_precision":null,"type":"regulatory","event":"Section 232 半導體關稅第二階段範圍","impact":"中","watch":"是否涵蓋 Marvell 主要產品、毛利率指引是否因此下修"}],"_projected_from":"v19"}
```
