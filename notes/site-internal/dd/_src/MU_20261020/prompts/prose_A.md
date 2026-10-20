你是 stock-analyst v20 的**散文層（prose）agent**，標的 MU（2026-10-20）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/MU_20261020/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MU　日期：2026-10-20　archetype：None　前份裁決：2026-07-05　觀望｜條件式衛星持倉　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1577B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（410B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（992B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1085B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1020B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（489B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（749B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2057B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3259B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2156B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1577           3796-5423      5 條（2–6 內）  
s3                  8000         410           5313-7590      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3097          8332-11903      5 條（2–6 內）  
s6                 11000         489          7358-10511      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         749           1926-2751      5 條（2–6 內）  
s10                 5000        2057           2060-2943      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2156           2000-2844      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4257B；至少需散文≈40.74KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70%
−70
−50%
−50
−9.11%
−7.2%
−0.9%
0%
0
0.06
0.062%
0.13
0.13%
0.16
0.20
0.23%
0.28
0.6%
0.75
0.82%
0.9%
1
01
1.02
1.4
1.5%
1.6
2
02
2.34
2.5
2.82
3
03
3%
3.41
3.58
4
4.4
4.43
4.98
5%
5
5.1
5.13
6
06
6.8%
7
7.2%
7.3%
7.4
7.69
8%
8
8.2
8.8%
09
10
10%
10.4%
11
11%
11.3%
11.4
12
12.17
13
13.6
14
15%
15
15.2
17%
18%
18
19.9%
20%
20
22%
22.35%
23
23.8%
24
25
25%
26
27
27.08
30%
30
31
32.3%
32.5%
34.04
35%
35
39.4
39.79%
39.8
39.8%
40%
40
42
45
46.2%
49
49%
50%
50
50.8
51%
55%
56.87
57%
57.6%
58
63%
64%
64.1
65.67%
70
70%
70.84
72.57%
73.37
74.35
74.67%
75%
77.11
77.49
80%
80.4%
81.2%
86%
90
93%
93.18
93.18%
100%
100
118
125
135
140%
140.63%
150%
158
172
176
176.55
183.04
186
200
203.33
204.47
215
225
230
232
240
253.88
382.55
402
414.56
450
470
500
501
700%
904.9
946
$946
975.56
2023
2026
2027
2028
2029
2030
20261020
1,000
1,043
1,308
1,485
1,522
1,700
2,700
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
{"meta":{"ticker":"MU","date":"2026-10-20","schema":"v15.0","contract":"v19","company_name":"Micron Technology, Inc."},"oneliner":"美光 FY2027 共識每股盈餘 176.55 美元，現價約 5 倍，但這個便宜建立在峰值毛利上；長約延後了下一次合約價下行，沒有取消它。循環位置偏晚，等合約價轉跌、止跌兩季後再談進場","thesis":{"H":[{"id":"H1","text":"DRAM 供給緊張延續到 2028 年，FY2027 每季毛利率守在 75% 以上（FQ4'26 財測約 86%）","2y":"FY2027 四季毛利率都 ≥75%；DRAM 合約價季增率不轉負","5y":null,"10y":null,"threshold":"季毛利率 ≥75%；DRAM 一般型合約價季增率 ≥0","source":"美光季報與財測、TrendForce 季度合約價","drift_rule":"季毛利率比 86% 的財測水準連 2 季低 5pp 以上→削弱；連 3 季低 10pp 以上→反轉"},{"id":"H2","text":"長約讓本輪下行比過去淺：下一次景氣下行時，年度毛利率守在 35% 以上（FY2023 為 -9.11%、FY2024 為 22.35%）","2y":null,"5y":"下一個下行年度毛利率 ≥35%，且年度 FCF 為正","10y":null,"threshold":"下行年度毛利率 ≥35%；SCA 覆蓋 DRAM 位元 ≥35%","source":"美光 10-K、法說（2026-09-30 COO：SCA 約四分之三有價格框架）","drift_rule":"TTM 毛利率連 4 季低於門檻 5% 以上→削弱；連 6 季低於門檻 10% 以上→反轉"},{"id":"H3","text":"技術與 HBM 位置守住：HBM 份額約等於整體 DRAM 份額（約二成），1-delta 在 2027 下半年放量，領先中國至少兩個節點","2y":null,"5y":"HBM 份額 ≥18%、DRAM 份額 ≥18%，HBM4E／NVHBM 量產","10y":null,"threshold":"HBM 份額 ≥18%；DRAM 份額 ≥18%（2026Q1 為 19.9%）","source":"Counterpoint 季度份額、美光法說","drift_rule":"份額連 4 季偏離門檻 5% 以上→削弱；連 6 季偏離 10% 以上→反轉"}],"R":[{"id":"R1","text":"記憶體合約價漲幅收斂後轉跌，毛利率自財測約 86% 的峰值回落","h_ref":"H1","clock":"⚡","threshold":"DRAM 一般型合約價季增率 ≤0 連 2 季，或公司財測毛利率季減 ≥5pp","evidence_refs":["end_markets#8","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#2"]},{"id":"R2","text":"中國 CXMT 與 YMTC 擴產，搶走商品 DRAM 與 NAND 的價格和中國客戶","h_ref":"H3","clock":"🔥","threshold":"CXMT DRAM 月產能 ≥ 美光，或美光 DRAM 份額連 2 季 <18%","evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#5","competitive_share_entrants#6"]},{"id":"R3","text":"業界同步擴建無塵室，2028 下半年起新產能開出，下一輪下行跟過去一樣深","h_ref":"H2","clock":"🐢","threshold":"下一個下行年度毛利率 <35%，或年度 FCF 轉負","evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#3"]},{"id":"R4","text":"反托拉斯集體訴訟與 232 條款關稅，壓低價格上限或侵蝕毛利","h_ref":"H2","clock":"🔥","threshold":"DRAM 買方集體訴訟獲集體認證，或 232 條款對記憶體課稅且公司財測毛利率因此下修 ≥3pp","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R5","text":"台灣產能集中與地緣風險：銅鑼廠交割後集中度更高，員工有罷工風險，中國禁令先例還在","h_ref":"H1","clock":"🐢","threshold":"台灣廠區停工 ≥2 週，或中國禁令擴大到一般商用採購","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#4","geo_supply_chain#5"]},{"id":"R6","text":"漲價侵蝕終端需求：手機、PC、車用位元下滑，消費端先鬆動","h_ref":"H1","clock":"⚡","threshold":"手機與用戶端業務單位位元連 3 季季減，且營收轉為季減","evidence_refs":["end_markets#5","end_markets#6"]}],"single_thing":{"description":"DRAM 一般型合約價季增率轉負（以 TrendForce 季度合約價為準）","why_fatal":"營收由合約價驅動，80% 營益率幾乎都是價格。前次下行合約價自高點跌 57%、毛利率轉負，終端盈餘對合約價的敏感度高過份額、HBM 或成本任何一項","if_happens":"已持有者減碼至半倉；連兩季轉負且財測毛利率季減 ≥10pp 就清倉；未持有者不建倉，等止跌兩季","how_monitor":"TrendForce 每季合約價預估與實績；美光每季毛利率財測","probability":"35%（12 到 24 個月內）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":4.43,"peg_fy2":0.28,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2026A":74.35,"FY2027E":176.55,"FY2028E":204.47,"FY2029E":203.33},"fy_end_month":8,"eps_basis":"共識為 Koyfin non-GAAP 稀釋 EPS（FY1＝FY2027，2027 年 8 月止）。FY2026A 由判斷日股價 904.9÷trailing 本益比 12.17 反推約 74.35，屬 GAAP 口徑，與共識口徑不完全一致；事實表沒有直接收錄 FY2026 實際 EPS"},"scenario_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/MU_20261020/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"近五年有虧損年（FY2023 毛利率 -9.11%）；毛利率由負數擺到財測約 86%；營收由合約價主導；屬記憶體產業"},"industry":{"clock_phase":"III","sd_verdict_source":"供需判斷：HBM 排擠與無塵室建置期撐住 2027–2028 的緊張（SK 海力士、TrendForce、美光 COO 三方一致）。但業界建設型資本支出正在加速，2028 下半年起新無塵室陸續投產，供給可逆性高。判為週期性將反轉，只是時點延後","bargaining":{"up":"設備端依賴 EUV，美光已和設備商簽長期供貨協議；供應商集中度事實表未涵蓋","down":"前十大客戶約占營收一半；最大客戶占比由 17% 降到 10%；輝達的 HBM4 同時向三家採購，美光分到的量最少","geo":"台灣產能占比高，力積電銅鑼廠交割後集中度更高；中國營收占比 FY27 預期降到個位數"},"profit_pool_dir":"利潤池目前流向記憶體：美光 TTM 毛利率 72.57%，已逼近輝達的 74.67%。這是稀缺帶來的暫時分配，供給追上後會回流","tam_table":{"expanded":false,"reason":"管理層 2026-09-30 明說不更新 HBM 市場規模，事實表也沒有滲透率序列；本檔的承重點是價格循環，不是滲透率曲線"}},"moat":{"mechanism":"製程節點領先（1-gamma 為主力、1-delta 2027 下半年放量）＋HBM 認證資格＋SCA 多年期長約綁住客戶配置","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：NAND 份額升到 15%，HBM4 量產供貨。定價面縮減：輝達 HBM4 分配美光最少，CXMT 產能逼近美光。兩相抵銷，判持平","peer_na_reason":"事實表同業為 NVDA、TSM、AVGO、AMD，都不是記憶體廠；三星與 SK 海力士的報酬率未收錄，算不出同業報酬差","threats":[{"level":"🟡","text":"CXMT 擴產逼近美光，中國品牌改採國產 DDR5。屬於商品 DRAM 的點對點破壞性競爭","p":"40%","evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#5"]},{"level":"🟡","text":"輝達 HBM4 三家都認證、美光分配最少，HBM 定價受多源採購壓制","p":"50%","evidence_refs":["customer_second_source#1"]},{"level":"🟡","text":"三星與 SK 海力士在探索 HBM 之後的 AI 記憶體架構，目前只有報導，沒有產品時程","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）；依資本密集的產業結構，判為高利益率×低周轉，重點在再投資負擔","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"資料中心的需求是真需要：COO 說客戶在現有記憶體量下盡量多出運算晶片，存在潛在需求。但消費端是可延後的需求，手機與 PC 位元已連兩季下滑，TrendForce 也下修 2026 年手機與筆電出貨"},{"item":"決策層級","level":"🟡","text":"HBM 的重新認證週期與 SCA 的五年期合約提高了轉換成本；但最大的 AI 客戶本來就向三家採購，在產品層的替代性仍高"},{"item":"價值鏈分配","level":"🟡","text":"DRAM 目前是瓶頸，美光毛利率逼近輝達，代表記憶體正在多分利潤。這靠的是稀缺，2028 年後新無塵室開出，分配會回流到運算端"},{"item":"社會容忍度","level":"🔴","text":"DRAM 買方指控四年漲價約 700%，已提起反托拉斯集體訴訟；車用廠商因記憶體短缺出現供應危機；中國 2023 年禁用美光的先例還在。價格上限實際由社會與政治決定，低於經濟上限"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋（資本支出全年數、折舊、營運資金變動都沒收錄；只知 FQ3'26 淨資本支出 70.84 億美元）","endo_ceiling":null,"formula_note":"ROIC＝稅後營益率×投入資本周轉率；TTM 營益率 65.67% 已知，投入資本缺，未計算。管理層的選擇是用 SCA 鎖住配置、建廠支出先行、裝機看需求，以延長稀缺的持續期，代價是建廠支出在出貨前就先燒掉"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","MU":72.57,"NVDA":74.67,"TSM":64.23,"AVGO":68.77,"AMD":53.2,"unit":"%"},{"metric":"營業利益率","MU":65.67,"NVDA":65.21,"TSM":56.1,"AVGO":48.52,"AMD":15.71,"unit":"%"},{"metric":"FCF 利潤率","MU":28.99,"NVDA":41.92,"TSM":25.33,"AVGO":44.22,"AMD":20.34,"unit":"%"},{"metric":"研發密度","MU":5.3,"NVDA":7.79,"TSM":6.07,"AVGO":13.28,"AMD":22.74,"unit":"%"}],"competitors":[{"name":"NVDA","gm":74.67,"om":65.21,"fcf_margin":41.92,"rd_intensity":7.79,"strategy_note":"最大的 AI 客戶，也是價值鏈上分利潤的對手；向三家採購 HBM，壓住單一供應商的議價","period":"TTM ending 2026-07-31（4季加總）"},{"name":"TSM","gm":64.23,"om":56.1,"fcf_margin":25.33,"rd_intensity":6.07,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"period":"TTM ending 2026-07-31（4季加總）"},{"name":"AMD","gm":53.2,"om":15.71,"fcf_margin":20.34,"rd_intensity":22.74,"period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"以價格為主：合約價年增倍數；FQ1'27 位元季增只有個位數，2028 年前量的成長受無塵室限制；不靠併購與回購","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本缺，內生上限算不出；共識三年年化約四成全部來自漲價與毛利率擴張，判定超出任何以再投資支撐的內生上限","segments":[{"item":"雲端記憶體（CMBU）","value":"77.49 億美元（FQ2'26，占 32.5%）"},{"item":"核心資料中心（CDBU）","value":"56.87 億美元（FQ2'26，占 23.8%）"},{"item":"手機與用戶端（MCBU）","value":"77.11 億美元（FQ2'26，占 32.3%）；位元已連兩季下滑"},{"item":"車用與嵌入式（AEBU）","value":"27.08 億美元（FQ2'26，占 11.3%）"}],"decay_signals":["主力產品提價後銷量下滑：手機與 PC 位元連兩季季減（2026-09-30 法說）","盈餘成長顯著高於營收成長：毛利率由 39.79% 擴張到財測約 86%","FCF 對淨利連兩年低於 0.75：FY2024 約 0.16、FY2025 約 0.20"],"trap_rating":"🔴"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；回購與現金去向四分的資料事實表未涵蓋，無法展開"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"唯一一筆收購是力積電銅鑼廠 18 億美元（資產收購），目標 2027 下半年出貨，已實現報酬算不出來","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購金額與均價事實表未涵蓋","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 季 3.41 億美元、占營收 0.82%；年化約占市值 0.13%，遠低於每年 1.5% 的門檻；股數淨變化事實表未涵蓋","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2027E）搭配自身年度端點 P/S；記憶體慣用的 P/B 事實表未涵蓋","tier":"記憶體三強（同業本益比事實表未涵蓋）","peers":{"expanded":false,"reason":"事實表同業為 NVDA、TSM、AVGO、AMD，屬不同層級；沒有三星、SK 海力士的倍數，不能跨層級當錨"},"fwd_pe":4.98,"peg":0.13,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價÷FY2027 共識約 5.1 倍，隱含市場預期 2029 年後盈餘大幅回落。基準情境（FY2030 盈餘較 FY2027 低約三成、終端 11 倍）五年年化約一成，屬合理區。但 P/S 在年度端點最高、分母是峰值盈餘，便宜的論證不成立，所以判黃不判綠。五年分位事實表未涵蓋，只有 3 到 4 個年度端點：本益比在 4.4 分位、P/S 在 100 分位","upside_short_pct":15.2,"upside_mid_pct":64.1},"trap_analysis":{"verdict":"🔴","label":"峰值利潤率陷阱：低本益比建立在漲價撐出的毛利上"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"前次下行合約價自高點跌 57% 與 55%，FY2023 毛利率轉負；TrendForce 預期 NAND 在 2027 下半年轉寬鬆；業界建設型資本支出加速，CXMT 產能逼近美光","assumption":"長約下限加上 HBM 排擠，讓本輪下行比過去淺","consequence":"2029 年合約價腰斬，FY2030 盈餘掉到二十美元以下，五年後股價落在 450 美元附近","ruling":"採納。空頭機率給 35%，情境終點約 -50%；這條與唯一致命點（合約價轉負）是同一件事","watch":"TrendForce 每季合約價、美光每季毛利率財測","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","end_markets#8","competitive_share_entrants#4"],"fact_refs":["f_ps_percentile"]},{"view":"論點成功但股東經濟變差","evidence":"DRAM 買方提起反托拉斯集體訴訟（依 Sherman Act 可求三倍賠償）；台灣 HBM 員工要求分潤、有罷工風險；車用客戶因短缺承壓；FY27 研發年增超過 10 億美元；建廠支出要到 2028 年後才轉成出貨","assumption":"稀缺帶來的利潤會留在股東手上","consequence":"供給緊張雖然延續，但賠償、勞動成本與先行建廠支出吃掉超額利潤，FCF 只有營業利益的五成多","ruling":"部分採納。FCF 轉換率列為持續監測項；賠償金額未知，不放進情境數字","watch":"集體認證裁定、每季 FCF 對營業利益比","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","geo_supply_chain#5","end_markets#6"],"fact_refs":["f_kpi3_adjusted_fcf"]},{"view":"價格已反映太多","evidence":"Goldman 稱美光一家占 S&P 500 盈餘上修的 51%；賣方目標價 1,308 到 1,522；共識 FY2029 盈餘與 FY2028 持平，沒有模擬下行；同一財年快照之間 FY2 共識已下修 0.9%","assumption":"5 倍本益比代表便宜","consequence":"分母是峰值，P/S 7.69 倍位於年度端點最高；共識一旦開始反映下行，倍數不會擴張，盈餘先降","ruling":"採納。便宜論證無效，估值只判合理","watch":"FY2 與 FY3 共識是否連續下修","evidence_refs":["capital_markets_pricing#5","capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_consensus_rev_fy2_pct","f_ps_current","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"台灣產能占比高，銅鑼廠交割後集中度更高；中國 2023 年禁用美光的先例；232 條款半導體調查與關稅","assumption":"地緣風險不會在五年內實現","consequence":"台灣停工或關稅擴及記憶體，會直接打斷出貨或壓縮毛利","ruling":"不放進情境，列為尾端風險。COO 說 FY27 中國營收占比降到個位數（2026-09-30），中國禁令的衝擊已縮小","watch":"台灣廠區運作、232 條款裁定是否涵蓋記憶體","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#4","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":[]}],"max_dd":{"lo":-70,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 975.56 → 本次 904.9（-7.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=975.56","side_b":"本次 price_at_dd=904.9","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式衛星持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、陷阱燈 🟡→🔴。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 975.56 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 975.56 美元：Bull 價 1,700、Bear 價 470，五年期望值 +6.8%，基準年化 0.6%，不對稱比 1.4","side_b":"本次情境、股價仍用 975.56 美元：Bull 價 2,700、Bear 價 450，五年期望值 +46.2%，基準年化 8.8%，不對稱比 2.34","ruling":"先換情境、股價不動：五年期望值多 39.4 個百分點，基準年化多 8.2 個百分點。不對稱比由 1.4 變為 2.34。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 975.56 美元：五年期望值 +46.2%，基準年化 8.8%，不對稱比 2.34","side_b":"本次情境、股價 904.9 美元：五年期望值 +57.6%，基準年化 10.4%，不對稱比 2.82","ruling":"再換股價、情境不動：起點價下跌 7.2%，五年期望值多 11.4 個百分點，基準年化多 1.6 個百分點，不對稱比由 2.34 升到 2.82。合計五年期望值比前份多 50.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值、陷阱、訊號、裁決","cause":"新證據","prior_field":["val","trap","signal"],"side_a":"前份：估值紅、陷阱黃、訊號 B，觀望","side_b":"本次：估值黃（FY2027 共識 176.55、現價約 5 倍）、陷阱紅（衰退訊號亮三項）、訊號 B 不變","ruling":"估值由紅轉黃，主因是盈餘分母換到 FY2027 且大幅高於前份的 FY2026，加上新簽十份 SCA；股價由 975.56 降到 904.9 是次因。陷阱轉紅，是因為手機與 PC 位元連兩季下滑屬新證據，加上 FCF 轉換率連兩年偏低。裁決與角色依新輸入重新路由","evidence_level":"高","settle_metric":"FQ1'27 毛利率與手機用戶端位元","if_then":["若 FQ1'27 毛利率低於 75%→已持有者減碼至半倉","若手機與用戶端位元回到季增且毛利率續升→陷阱降回黃，維持不加碼"],"evidence_refs":["channel_business_model_shift#1","capital_markets_pricing#2","end_markets#5"]},{"axis":"前份漂移：護城河方向、跑道、類型、循環位置","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：持平、跑道中等、循環/商品、晚循環","side_b":"本次：四欄都不變","ruling":"新證據正反都有。NAND 份額升到 15%，但輝達 HBM4 分配美光最少，護城河仍判持平；沒有找到第二條成長曲線，跑道維持中等；合約價季增幅由 58–63% 收斂到 13–18%，循環位置維持晚段","evidence_level":"中","settle_metric":"季度合約價、HBM 份額","if_then":["若合約價季增率轉負→循環位置改為過熱頂部轉下行","若 HBM 份額連兩季升到 22% 以上→護城河方向改為擴大"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#1","cyclical_inventory_price_position#2"]},{"axis":"前份漂移：情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"多頭 30%、空頭 30%、最大回撤單點 -70%","side_b":"多頭 25%、空頭 35%、最大回撤區間 -70% 到 -50%","ruling":"共識成長超出內生上限，空頭機率至少 30%，再加 5 個百分點反映峰值毛利；回撤改用區間取代單點，下緣不變","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"Fwd FY26 P/E ≤13x（≈$946）或合約價 QoQ 轉負後 P/B 回落自身中位（循環重置）；HBM4 份額連 2 季淨增則升級評估","side_b":"DRAM 合約價季減後連 2 季止跌，且公司財測毛利率止跌（循環回到早段），屆時重跑研究，首倉上限 3%；觸發前不追、已持有不加碼","ruling":"舊門檻的價格錨已被股價觸及（904.9 低於 946），但 FY2026 已成實績，分母換成 FY2027 後，5 倍本益比是峰值盈餘下的假便宜，價格錨失效。真正的約束是循環位置，所以改用事件錨；P/B 事實表未涵蓋，拿掉","evidence_level":"中","settle_metric":"TrendForce 合約價、美光財測毛利率","if_then":["若合約價季減後連兩季止跌→重跑研究，確認後首倉 ≤3%","若合約價持續季增而股價續跌→不追，不加碼"],"evidence_refs":["cyclical_inventory_price_position#2"]},{"axis":"停損指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份沒有設停損指標（null）","side_b":"合約價季增 ≤0 連兩季→減碼至半倉；季毛利率低於 70%→減碼；CXMT 產能追平美光→減碼；合約價連兩季轉負且財測毛利率季減 ≥10pp→清倉","ruling":"前份只有警戒閾值，沒有綁定減碼與清倉動作，本次補上，門檻對應三個最大敏感度項","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份 Single Thing 為 null（未設）","side_b":"Single Thing：DRAM 一般型合約價季增率轉負","ruling":"營收由合約價驅動，終端盈餘對合約價的敏感度高於份額、HBM 或成本任何一項，因此設為唯一致命點；發生時減碼至半倉","evidence_level":"高","settle_metric":"TrendForce 季度合約價","if_then":["若轉負→減碼至半倉；連兩季且財測毛利率季減 ≥10pp→清倉"],"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"axis":"供需持續期","cause":null,"prior_field":null,"side_a":"管理層：看不到供需平衡的時點，2028 年比 2027 更緊，FY27 出貨已承諾超過七成五（2026-09-30 COO）","side_b":"TrendForce：NAND 在 2027 下半年轉寬鬆、價格承壓；業界建設型資本支出加速，2028 下半年起新無塵室投產","ruling":"兩邊在時點上方向相反，屬不可調和。選第二邊作為 FY2029 以後的基準：DRAM 緊到 2028 年有多方佐證，但 NAND 先鬆；管理層也承認新增建廠支出主要是 2028 年後才投產","evidence_level":"中","settle_metric":"2027 下半年 NAND 合約價季增率","if_then":["若 TrendForce 公布 DRAM 合約價季增轉負→已持有者減碼至半倉，未持有不建倉","若 2027 下半年 NAND 合約價仍季增、且 2028 年配置談判已完成→維持持有、不加碼，首倉條件不變"],"evidence_refs":["end_markets#8","supply_demand_durability#3","cyclical_supply_discipline_capacity#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2027 約 5 倍本益比、淨現金 382.55 億美元、FY27 七成五出貨已承諾、SCA take-or-pay 到 2030 年、FQ1'27 指引高於共識","side_b":"毛利率財測約 86% 已是峰值，手機位元在下滑；SCA 最低承諾約 1,000 億美元分攤到 2030 年，每年約 200 多億，只占 FY2027 共識營收約 8%","ruling":"不買。真正的約束是循環位置偏晚，長約下限的金額只覆蓋峰值營收的一小塊，托不住價格下行","evidence_level":"中","settle_metric":"合約價季增率","if_then":["若合約價轉跌後連兩季止跌→重跑研究，首倉 ≤3%","若合約價持續季增而股價跌到 FY2028 共識 4 倍以下→仍不追，等合約價訊號"],"evidence_refs":["customer_second_source#0","channel_business_model_shift#1"]},{"axis":"HBM 份額證據","cause":null,"prior_field":null,"side_a":"Counterpoint 與市場彙整：美光 HBM 份額約 20%，輝達 HBM4 分配約兩成","side_b":"供應鏈估計輝達 Vera Rubin 的 HBM4 由 SK 海力士拿六到七成、三星二到三成，美光只拿剩下的；管理層 2026-09-30 也不再確認二成出頭的舊目標","ruling":"不可裁決，要等 2026Q4 的 HBM 份額公布。在那之前不把 HBM 份額當加分項，並列入停損指標","evidence_level":"低","settle_metric":"Counterpoint 2026Q4 HBM 份額","if_then":["若份額連兩季低於 15%→減碼至半倉","若份額 ≥20%→維持護城河判斷，不加碼"],"evidence_refs":["customer_second_source#1","end_markets#3","end_markets#4"]},{"axis":"共識修正口徑","cause":null,"prior_field":null,"side_a":"近 3 個月 FY1 共識上修 140.63%","side_b":"90 天前的 FY1 是 FY2026（73.37），現在的 FY1 是 FY2027（176.55），屬財年換季，不是真上修；同一財年兩次快照之間，FY1 +0.23%、FY2 -0.9%","ruling":"不把 140% 當成盈餘動能證據；近期共識已停止上修，FY2 開始下修","evidence_level":"高","settle_metric":"FY2 共識月度變化","if_then":["若 FY2 共識連兩個月下修合計超過 3%→停止任何加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FQ1'27 財報毛利率對照財測，以及 FY27 毛利續升的說法","type":"假設驗證","maps_to":"H1","metric":"季 GAAP 毛利率","threshold":"≥75%，且 FQ2 財測不低於 FQ1","action":"低於 75% 或財測季減→已持有者減碼至半倉；達標→維持，不加碼","source_freq":"美光季報／每季","date":"2026-12","evidence_refs":["capital_markets_pricing#2"]},{"n":2,"text":"DRAM 一般型合約價季增率轉負","type":"Single Thing","maps_to":"single_thing","metric":"DRAM 一般型合約價季增率","threshold":"≤0%","action":"減碼至半倉；連兩季轉負且財測毛利率季減 ≥10pp→清倉","source_freq":"TrendForce／每季","date":"2027-01","evidence_refs":["end_markets#8","cyclical_prior_downcycle_behavior#0"]},{"n":3,"text":"CXMT 的 DRAM 產能追平美光","type":"風險","maps_to":"R2","metric":"CXMT DRAM 月產能對美光差距","threshold":"差距 ≤0","action":"減碼至半倉","source_freq":"TrendForce／產業報導／每季","date":"2027-03","evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#5","competitive_share_entrants#6"]},{"n":4,"text":"DRAM 買方反托拉斯集體訴訟獲集體認證","type":"風險","maps_to":"R4","metric":"集體認證裁定","threshold":"認證通過","action":"減碼至半倉","source_freq":"美光 10-Q／10-K 訴訟附註／每季","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0"]},{"n":5,"text":"循環回到早段：合約價季減後止跌，財測毛利率止跌","type":"估值rearm","maps_to":"rearm","metric":"DRAM 合約價季增率＋公司財測毛利率","threshold":"合約價季減後連兩季止跌，且財測毛利率止跌","action":"重跑研究，確認循環回到早段後首倉 ≤3%","source_freq":"TrendForce＋美光季報／每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#3"]},{"n":6,"text":"合約價連兩季轉負，且財測毛利率大幅季減","type":"清倉","maps_to":"R1","metric":"合約價季增率與財測毛利率","threshold":"合約價連兩季 ≤0，且財測毛利率季減 ≥10pp","action":"清倉","source_freq":"TrendForce＋美光季報／每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"n":7,"text":"HBM 份額公布，裁定份額證據的衝突","type":"假設驗證","maps_to":"H3","metric":"美光 HBM 份額","threshold":"≥18%","action":"低於 15% 連兩季→減碼至半倉；≥18%→維持","source_freq":"Counterpoint／每季","date":"2027-02","evidence_refs":["customer_second_source#1"]},{"n":8,"text":"FQ1'27 財報後複審","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑研究","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"DRAM 一般型合約價季增率","bear_threshold":"≤0% 連 2 季","window":"2026Q4–2028Q4","source":"TrendForce 季度合約價報告","last_status":"ok"},{"metric":"美光季 GAAP 毛利率","bear_threshold":"低於 70%，或財測季減 ≥10pp","window":"FY2027–FY2028 各季","source":"美光季報與財測","last_status":"ok"},{"metric":"美光 HBM 份額","bear_threshold":"<15% 連 2 季","window":"2026Q4–2028","source":"Counterpoint 季度份額","last_status":"unknown"},{"metric":"CXMT DRAM 月產能對美光差距","bear_threshold":"差距 ≤0（追平）","window":"2026–2027","source":"TrendForce／Tom's Hardware 產能報導","last_status":"warning"},{"metric":"SCA 覆蓋的 DRAM 位元占比","bear_threshold":"<25%","window":"至 2030","source":"美光法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"7a","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":true,"basis":"valuation_dependent=True, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=93.18, valuation_dependent=True"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['7a']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":["QC-50"],"rearm_trigger":"DRAM 合約價季減後連 2 季止跌，且公司財測毛利率止跌（循環回到早段），屆時重跑研究，首倉上限 3%","exec_line":"未持有：不建倉，等循環回到早段。已持有：維持、不加碼；合約價季增轉負即減碼至半倉，連兩季轉負且財測毛利率季減 10pp 以上就清倉"},"reasoning":{"industry":"FQ3'26 營收 414.56 億美元，GAAP 營益率 80.4%，non-GAAP 81.2%；FQ4 財測營收 500 億美元（±10 億）、毛利率約 86%、non-GAAP EPS 31 美元。FQ2'26 四個業務單位都超過營收一成：雲端記憶體 77.49 億、核心資料中心 56.87 億、手機與用戶端 77.11 億、車用與嵌入式 27.08 億美元（2026-03-18 第二季新聞稿）。最大單一客戶占比由 FY26 第一季的 17% 降到前九個月的 10%，前十大客戶約占 FY2025 營收一半，集中度在下降。2026-09-30 法說會上，COO 說 DRAM 已是 AI 資料中心的主要瓶頸，CFO 說 FQ1'27 財測的位元季增只有個位數、單位成本降兩位數，所以營收成長幾乎全是價格。產業態勢屬雙向拉鋸：結構轉好的一邊是多年期長約（SCA）、HBM 排擠一般 DRAM 產能、新無塵室要兩年才投產；另一邊是其他結構變動，包括 DRAM 買方反托拉斯集體訴訟，以及中國 CXMT 的 DRAM 月產能已逼近美光。景氣時鐘判第三期過熱：合約價季增幅由第二季的 58–63% 收斂到第三季的 13–18%，手機與 PC 位元連兩季下滑，毛利率財測卻創新高。","moat":"機制有三：一是製程節點，1-gamma 已占多數位元，CTO 稱領先中國至少兩個節點（2026-09-30）；二是 HBM 認證資格，HBM4 已量產供 Vera Rubin，並與輝達共同設計 HBM4E；三是 SCA 多年期 take-or-pay 長約。執行面在擴大：NAND 份額升到 15%（2026Q2），最大客戶依賴度下降。定價面在縮減：輝達 HBM4 三家都認證，美光分配最少；CXMT 的 DRAM 月產能預計 2026 年底只落後美光約 2.5 萬片；管理層也不再確認 HBM 份額要拿到二成出頭的舊目標。同業表是 AI 價值鏈公司，不是記憶體廠，算不出同業報酬差，只能用份額方向當替代證據。執行力給 8 分、定價力給 6 分。","growth":"共識每股盈餘 FY2027E 176.55、FY2028E 204.47、FY2029E 203.33，第三年持平，賣方沒有模擬下行。以 FY2026 實績約 74.35（股價÷trailing 本益比反推）為基期，三年年化約 39.8%；若從 FY2027 起算只有 7.3%。缺口全部歸因於毛利率擴張（毛利率由 FY2025 的 39.79% 到財測約 86%），不是再投資帶來的內生成長。近 3 個月 FY1 共識上修 140.63%，其實是財年換季（FY2026 換成 FY2027），不是真上修；同一財年兩次快照之間 FY1 只上修 0.23%、FY2 反而下修 0.9%。衰退訊號亮三項：提價後手機與 PC 位元連兩季下滑；盈餘成長遠快於營收（FY2025→FY2027E 營收約 7.4 倍、EPS 約 23 倍）；FCF 對淨利 FY2024 為 0.16、FY2025 為 0.20，連兩年低於 0.75。","governance":"FQ3'26 營業現金流 253.88 億、淨資本支出 70.84 億，調整後 FCF 約為 GAAP 營業利益的 55%。SBC 3.41 億美元、占營收 0.82%，年化約 13.6 億，對約 1.02 兆美元市值約 0.13%，稀釋可忽略。股息殖利率 0.062%；回購金額與均價事實表未涵蓋。CFO 說 FY27 研發年增超過 10 億美元（2026-09-30），建廠支出是先燒錢、後出貨。力積電銅鑼廠 18 億美元屬資產收購，還沒產出，已實現報酬算不出來。","valuation":"現價 904.9 美元，對 FY2027 共識約 5.1 倍、對 FY2028 約 4.4 倍，trailing 12.17 倍；P/S 7.69 倍、EV/S 7.4 倍，都在年度端點的最高分位，前瞻 EV/S 3.58 倍。低本益比是峰值盈餘造成的，分母本身就是爭點。PEG 0.13（4.98÷39.8）因成長全靠漲價而失真，不能當便宜的證據。短期以維持目前前瞻倍數、往後滾一年估算：FY2028E 204.47×5.1≈1,043 美元，約 +15%。中期取基準情境 FY2031 為 135×11≈1,485 美元，約 +64%。賣方均價目標 1,308（Benzinga，26 位）到 1,522（Walnut，42 位）兩個口徑不一致，只當區間參考。","premortem":"衰退訊號亮三項，價值陷阱判紅：提價後位元下滑、盈餘成長遠快於營收、FCF 轉換率連兩年偏低。26 週漲 93.18%，RSI 已回落到 34.04，股價自前份 975.56 美元降到 904.9 美元，市場已開始計價高點。週線均線排列仍完整。前次下行營收年減 49%、毛利率轉負，最大回撤取 -50% 到 -70%。"},"plain":{"six":{"how_it_makes_money":"美光賺的是記憶體位元稀缺的錢，雲端、資料中心、手機與 PC、車用客戶都在付漲價；利潤卡在 DRAM 供給這一節點，本季 80% 營益率主要靠價格撐出來，量的貢獻有限","moat":"護城河方向持平。製程與 HBM 認證守住第三名，執行面在擴大；但定價力來自全產業稀缺，不是美光獨有，HBM 議價又被輝達多源採購壓住，兩邊相抵","growth":"成長跑道屬中等。成長幾乎全來自漲價，量受無塵室限制到 2028 年；HBM 份額成長了但沒有找到第二條曲線，五年後的成長靠下一輪漲價，不靠滲透率","capital":"現金大量流入，但再投資報酬還沒證實。FQ3'26 調整後自由現金流 183.04 億美元，淨現金約 382.55 億；新增資本支出以建廠為主，2028 年後才投產，報酬要到下一輪才看得到","valuation":"現價要成立，前提是 2029 年後的下行比過去淺，FY2031 盈餘還能回到約 135 美元並拿到 11 倍。我半信：長約下限是新東西，但它的金額只覆蓋峰值營收的一小塊。估值判合理，不判便宜","how_wrong":"最可能看錯的地方，是把峰值盈餘當成常態。5 倍本益比看起來便宜，但它是商品循環高點的典型讀數"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":true,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不追價。等 DRAM 合約價季減後連兩季止跌、公司財測毛利率止跌，確認循環回到早段","qc48_result":null,"trap":"🔴","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":904.9,"week26_return_pct":93.18,"consensus_rev_3m_pct":140.63,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母 FY2027 盈餘建立在約 86% 毛利率與合約價年增倍數上，是循環峰值。P/B 事實表未涵蓋，改以 P/S 位於年度端點最高、以及前次下行毛利率轉負作對照"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"FQ1'27 財報與 FQ2 財測（毛利率是否續升）","impact":"高","watch":"毛利率 ≥75%，FQ2 財測不低於 FQ1"},{"date":"2027-01","date_precision":"month","type":"other","event":"TrendForce 公布 CQ1'27 DRAM 與 NAND 合約價","impact":"高","watch":"DRAM 季增率是否轉負"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"力積電銅鑼廠 18 億美元收購交割","impact":"低","watch":"交割進度與 2027 下半年 DRAM 出貨時程"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"Idaho 新廠首批晶圓產出","impact":"中","watch":"首批產出後還要數季才有量；同期業界新無塵室開出的進度"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"HBM4E／NVHBM 量產與 1-delta 放量","impact":"中","watch":"輝達 HBM4E 分配份額"},{"date":null,"date_precision":null,"type":"regulatory","event":"DRAM 買方反托拉斯集體訴訟的集體認證裁定","impact":"中","watch":"認證通過即減碼至半倉"}],"_projected_from":"v19"}
```
