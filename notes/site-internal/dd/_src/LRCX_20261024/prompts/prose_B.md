你是 stock-analyst v20 的**散文層（prose）agent**，標的 LRCX（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：LRCX　日期：2026-10-24　archetype：None　前份裁決：2026-07-30　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1665B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（673B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（994B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1073B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1099B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（559B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（828B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1965B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4129B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2059B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1665           3734-5335      5 條（2–6 內）  
s3                  8000         673           5129-7327      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3166          8284-11834      5 條（2–6 內）  
s6                 11000         559          7309-10441      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         828           1870-2672      5 條（2–6 內）  
s10                 5000        1965           2124-3035      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2059           2000-2941      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4659B；至少需散文≈40.34KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−62%
−60
−60%
−41%
−40%
−40
−13.92
−9%
−8.8%
−1
0.16%
0.48
0.67
0.75
0.84
0.85
01
1
1.01
1.06
1.15
1.4%
1.5%
1.5
1.9
2%
2.0
2
2.15
2.20
2.27
2.33
2.58
2.72
2.8%
3
3.25
04
4
4.2%
4.6
4.7%
5%
5
5.6%
5.6
5.76
6%
6
06
6.5
07
7%
7
7.4%
7.5
8
8%
8.8%
9
9%
9.5
9.6
9.63
10
10%
10.2
11
11%
11.4
11.5%
11.6
12%
12
12.15
12.6
13
13.1
13.2
13.6
13.9%
14
14%
14.1%
14.44
14.5
14.5%
15%
15
16%
16
16.5%
16.9%
17%
17
18%
18
18.9
19
19.1
19.8%
20%
20
21
21.1%
21.5
21.8%
22%
22
22.5%
23.89
23.9
24
24.6
25
25%
26%
26
26.6
27
28
29
29.4%
29.8
30%
30
30.85
31
31.4%
32.4
32.9%
34%
34.3
35%
35.0
35.3%
35.5%
35.9%
36%
36.5%
37
37%
37.8%
39.5%
40%
40.2%
40.5%
41%
41.5%
42
45%
45
46%
48%
49
49%
50%
51%
52%
52.4%
54%
55%
56
59%
60%
70
70%
72%
75
80%
81
82
82.2
85%
86
100
100%
119
120%
138%
142.5
150%
$150
164.5
$180
200
$200
230.1
243
250
252.35
256
290
342
384
516
553.5
2001
2023
2025
2026
2027
2028
2029
2030
20261024
1,500
1,550
1,800
1,900
2,000
2,100
2,295
2,880
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
{"meta":{"ticker":"LRCX","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Lam Research"},"oneliner":"AI 推動 2027 年晶圓設備支出逾 2,000 億美元，Lam 蝕刻沉積強度與份額同步上升；股價半年跌 14% 而共識上修 17%，但利潤率已在循環高檔，出口管制與 2028 年降溫是兩大風險。","thesis":{"H":[{"id":"H1","text":"AI 帶動的晶圓設備支出上行延續至 CY2027，WFE 逾 2,000 億美元、DRAM 領先，Lam 系統營收成長高於 WFE。","2y":"CY2027 WFE ≥1,900 億美元，且 Lam CY2027 營收成長率高於 WFE 成長率","5y":null,"10y":null,"threshold":"1 月法說 CY2027 WFE ≥1,900 億美元；季營收不低於共識路徑 5%","source":"公司每季法說、SEMI 年中與年底預測","drift_rule":"季營收 TTM 低於共識路徑連 2 季 ≥5% 為削弱、連 3 季 ≥10% 為反轉"},{"id":"H2","text":"蝕刻沉積強度隨 3D 化、背面供電、先進封裝與乾式光阻上升，Lam 的 SAM 占 WFE 比重接近 40%，連續第四、五年跑贏 WFE。","2y":"2027 年連續第四年跑贏 WFE","5y":"2030 年前 SAM 占 WFE 接近 40%，先進封裝與面板級封裝成為第二成長曲線","10y":null,"threshold":"Lam 年度營收成長率高於 WFE 成長率；SAM 占 WFE ≥37%（2027）","source":"公司法說與投資人日 SAM 揭露","drift_rule":"TTM 營收成長率低於 WFE 成長率連 4 季差距 ≥5 個百分點為削弱，連 6 季差距 ≥10 個百分點為反轉"},{"id":"H3","text":"利潤結構上移：毛利率朝中 50% 推進、營業利益率 2027 年守 40%，下一輪下行谷底毛利率不低於 45%（2023 年谷底 41.5%）。","2y":null,"5y":"毛利率中 50%，下一輪谷底毛利率 ≥45%","10y":null,"threshold":"2027 年單季 non-GAAP 毛利率 ≥51%","source":"公司每季新聞稿","drift_rule":"毛利率較 52% 基準偏離連 4 季 ≥5% 為削弱、連 6 季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"循環轉折：2027 年含提前拉貨與擠潔淨室成分，SEMI 估 2028 年 WFE 成長放緩至 14.1%，同業大舉擴產；NAND 2027 下半年隨新產能放鬆。設備業歷史下行：2001 年出貨年減 41%、Lam 出貨峰谷跌 80%，2023 年谷底毛利率 41.5%。","h_ref":"H1","clock":"🔥","threshold":"連續兩季營收指引中點季減，或 NAND 占系統營收降至 15% 以下且記憶體金額季減","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#3","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3"]},{"id":"R2","text":"中國出口管制與在地化：中國占 FY2026 營收約 34%、9 月季 35%，出貨依賴出口許可；前份記載關聯方規則一年暫緩約 2026-10-30 到期，MATCH Act 討論中點名 Lam 的蝕刻沉積設備；客戶與下游同樣受關稅與管制影響；NAURA 升至全球第五，本土廠在成熟節點替代。","h_ref":"H1","clock":"⚡","threshold":"12 月季管制衝擊 ≥1.5 億美元，或新規涵蓋在華跨國廠","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#1","customer_concentration_credit#3","competitive_share_entrants#1","competitive_share_entrants#4"]},{"id":"R3","text":"倍數繼續向循環中段回歸而盈餘未同步成長：前份前瞻約 30.85 倍、本次 23.9 倍；長窗中位數事實表未涵蓋（前份所記 19.1 倍）。若 2027 年 WFE 只持平，倍數與盈餘同時下修。","h_ref":"H1","clock":"🔥","threshold":"CY2027 WFE 展望 <1,800 億美元且前瞻本益比仍 >20 倍","evidence_refs":[]},{"id":"R4","text":"客戶集中：四家客戶占 FY2026 營收約 55%（16%、15%、12%、12%），五家占應收帳款約 72%；大客戶可壓價、限制技術分享，單一記憶體客戶縮手影響不成比例。","h_ref":"H3","clock":"🐢","threshold":"營收成長中毛利率連兩季 <51%（壓價訊號），或單一客戶 >20% 營收","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R5","text":"擴產跟不上：零組件吃緊已壓低 12 月季指引，10-K 列出跟不上 AI 需求可能流失份額；部分元件歷來只能向單一或少數供應商採購。","h_ref":"H2","clock":"⚡","threshold":"3 月季營收低於 12 月季實績","evidence_refs":["competitive_share_entrants#2","geo_supply_chain#0"]}],"single_thing":{"description":"美國出口管制擴大至 Lam 在中國的核心蝕刻沉積品項（MATCH Act 立法，或關聯方規則到期後全面恢復且不給豁免、涵蓋在華跨國廠）。","why_fatal":"中國占 FY2026 營收約 34%、9 月季 35%，是最大的單一敏感度；被拿掉的營收不會回來，還會加速本土設備商在中國的替代。","if_happens":"只涵蓋中國本土客戶：減碼至半倉；涵蓋在華跨國廠：清倉後重跑判斷。","how_monitor":"國會法案進度、商務部聯邦公報、公司 8-K 與 10-Q 地區營收占比、法說對中國的指引。","probability":"25%"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.9,"peg_fy2":0.84,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":5.76,"FY2027E":9.63,"FY2028E":12.15,"FY2029E":14.44},"fy_end_month":6,"eps_basis":"Koyfin 共識 EPS（以 non-GAAP 為主）；基期 FY2026A 取年報稀釋 EPS 5.76（GAAP），公司 GAAP 與 non-GAAP 差距小。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收隨 WFE 擺動（FY2024 年減 14.5%），但近四年無虧損、2023 年谷底毛利率仍有 41.5%，裝機服務收入提供底部。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉，但本輪被潔淨室與零組件供給限制拉長：SEMI 估 WFE 2027 年增 21.8%、2028 年增 14.1%，成長率 2028 年起放緩；設備同業大幅擴產，下一輪供給可逆性高。","bargaining":{"up":"零組件供應商短期議價力上升：12 月季指引因供給吃緊而保守，分析師指出應付帳款增加約 13 億美元。","down":"四家客戶占 FY2026 營收約 55%，10-K 明言大客戶可壓價並限制技術分享。","geo":"中國占營收 34%–35%，出貨須取得美國出口許可，管制擴大會直接縮小可服務市場。"},"profit_pool_dir":"利潤池往蝕刻沉積移動：3D NAND、背面供電、先進封裝與乾式光阻使 Lam 的 SAM 占 WFE 過去幾年擴大約 4 個百分點。","tam_table":[{"item":"CY2026 WFE（公司展望）","value":"約 1,550 億美元（2026-10-21 法說；7 月為 1,500 億出頭）"},{"item":"CY2027 WFE（公司初步）","value":"逾 2,000 億美元，成長以 DRAM 領先，其次先進邏輯與 NAND；為供給受限下的數字"},{"item":"SEMI 2028 設備總銷售","value":"2,295 億美元；WFE 2027 年增 21.8%、2028 年增 14.1%"},{"item":"Lam SAM 占 WFE","value":"2025 年約 35%，2026 年約 36%–36.5%，目標接近 40%"},{"item":"先進封裝","value":"2026 年成長逾 70%；面板級電鍍設備已出貨逾 20 家客戶"}]},"moat":{"mechanism":"製程指定機台綁定：每一代 3D 結構的蝕刻沉積配方在客戶產線驗證後難以替換，加上業界最大的 NAND 裝機量帶來升級與零件服務收入。","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"SAM 占 WFE 擴大約 4 個百分點、2026 年連續第三年跑贏 WFE；背面供電四項產品在一家領先客戶取得指定機台；乾式光阻已在 HBM 量產並上調累計營收預期約 10 億美元（2026-10-21 法說，CEO）。事實表未見最大客戶份額下滑的證據。","peer_na_reason":"事實表只有同業利潤率，沒有投入資本口徑，ROIC 差距無法計算；以營業利益率代替比較。東京威力營收缺漏，無法算利潤率。","threats":[{"level":"🟡","text":"中國本土設備商在在地化政策下擴張，NAURA 升至全球第五；在中國成熟節點逐項產品替代，屬區域點對點競爭，尚未進入先進節點。","p":"35%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#4"]},{"level":"🟡","text":"同業大舉擴產（應材產出倍增、東京威力資本支出上調 48%），景氣下行時設備供給過剩，價格與份額競爭加劇。","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"製程技術快速變遷，若新世代機台不及對手改良版會失去份額；10-K 未點名具體替代技術，目前 3D 化方向反而推升蝕刻沉積強度。","p":"15%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉率事實表未涵蓋，以低資本支出強度與自由現金流利潤率推斷）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是晶圓廠製程工程、決策者是客戶資本支出委員會、付款者同為晶片廠，三角色一致；製程升級是需要而非想要，但時點可延後：FY2024 營收年減 14.5%、2023 年谷底毛利率 41.5%，顯示需求會遞延。公司引述每週 token 用量 18 個月約增 250 倍，支撐需求基礎值。"},{"item":"決策層級","level":"🟢","text":"替代性要在單一製程步驟衡量：新節點的蝕刻沉積步驟選定機台後即寫入量產配方，換供應商要重新認證；本季在一家領先客戶的背面供電四項產品全拿下指定機台，乾式光阻在 HBM 量產被指定。"},{"item":"價值鏈分配","level":"🟡","text":"四家客戶占 FY2026 營收約 55%、五家占應收帳款約 72%，買方集中可壓價；但毛利率升至 52.4% 且有調價，現階段 Lam 分到的比重在增加。上游零組件吃緊，供應商短期議價力上升。"},{"item":"社會容忍度","level":"🟡","text":"價格不是社會議題，政治上限在出口：中國營收約 34% 依賴美國出口許可，法源為出口管制規則與國會法案（MATCH Act 討論中點名 Lam），政策可在短時間改變可服務市場。"}],"roiic":"約 138%（FY2023→FY2026 營業利益增加約 29.8 億美元，以 11%–16.5% 稅率計稅後約 25–27 億；同期累計再投資約 18.9 億美元）","reinvest_rate":"約 11.5%（三年累計再投資 18.9 億÷累計淨利 164.5 億美元）","endo_ceiling":16,"formula_note":"事實表未涵蓋投入資本口徑。再投資以每年淨利減自由現金流近似（含資本支出減折舊與營運資金變動，三年無併購），淨利代替稅後營業利益（淨現金公司差異小）。上行段營運槓桿讓增量報酬偏高，不代表下一輪；內生上界約 16%。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","LRCX":50.47,"ASML":52.73,"AMAT":49.4,"KLAC":61.3,"8035.T":null,"unit":"%"},{"metric":"營業利益率","LRCX":35.29,"ASML":35.42,"AMAT":31.09,"KLAC":41.69,"8035.T":null,"unit":"%"},{"metric":"FCF 利潤率","LRCX":21.05,"ASML":24.27,"AMAT":18.23,"KLAC":27.74,"8035.T":null,"unit":"%"},{"metric":"研發密度","LRCX":10.23,"ASML":13.68,"AMAT":12.88,"KLAC":11.28,"8035.T":null,"unit":"%"}],"competitors":[{"name":"ASML","gm":52.73,"om":35.42,"fcf_margin":24.27,"rd_intensity":13.68,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"AMAT","gm":49.4,"om":31.09,"fcf_margin":18.23,"rd_intensity":12.88,"period":"TTM ending 2026-07-31（4季加總）"},{"name":"KLA","gm":61.3,"om":41.69,"fcf_margin":27.74,"rd_intensity":11.28,"strategy_note":"檢測量測為主，與 Lam 不直接競爭；利潤率為同業最高，作為設備業利潤率上限的參照。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"8035.T","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"period":"TTM ending 2026-06-30（2季加總）"}]},"growth":{"driver_mix":"量（WFE 擴張＋SAM 占比上升）為主、價與組合為輔、淨回購每年約 2%，無併購。","runway_years":"不適用（以 SAM 占 WFE 比重衡量，非滲透率）","runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段：增量報酬約 138%×再投資率約 11.5%≈16%；本輪營運槓桿灌水，下一輪不保證。","segments":[{"item":"記憶體系統營收","value":"9 月季占系統 46%，金額年增 120%；NAND 季增約 40%（轉 256 層以上、初步 384 層），DRAM 創新高"},{"item":"晶圓代工","value":"占系統 46%，創新高；先進節點、先進封裝與中國成熟節點帶動"},{"item":"邏輯及其他","value":"占系統 8%，以先進節點為主"},{"item":"服務事業（CSBG）","value":"單季近 25 億美元、年增 40%；CY2026 成長逾 30%、CY2027 逾 15%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"9 月季 52.4% 創新高"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"SAM 占比與份額上升"},{"signal":"提價後銷量下滑","lit":false,"note":"量價齊升"},{"signal":"EPS 年複合高於營收年複合逾 5 個百分點","lit":true,"note":"共識 FY2026→FY2028 EPS 約 45%、營收約 35.5%"},{"signal":"自由現金流÷淨利 <0.75 連 2 年","lit":false,"note":"FY2026 0.67、FY2025 1.01，僅一年"},{"signal":"SBC÷營收 >5% 且上升","lit":false,"note":"約 1.4%"},{"signal":"TAM 萎縮或被替代","lit":false,"note":"WFE 擴張中"},{"signal":"產業倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"signal":"維持性資本支出占自由現金流 >60%","lit":false,"note":"9 月季資本支出 2.58 億對自由現金流 32.4 億"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"持續擴廠與研發實驗室"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月無併購；股東回饋以回購與股息為主，已在計分卡與理由段交代，現金去向四分（回購、股息、償債、增加現金）見理由段。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 無併購項目，搜尋亦無 2025–2026 併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價與 10 年期殖利率事實表未涵蓋；現價前瞻盈餘殖利率約 4.2%（9.63÷230.1）","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"股權酬勞年化約 4.6 億美元÷市值約 2,880 億≈0.16%/年，且稀釋股數逐年下降","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY1，2027 年 6 月年度）","tier":"大型前段設備龍頭","peers":{"expanded":false,"reason":"事實表只有同業利潤率，無同業本益比或目標價的結構化數字，無法做倍數對照；終端倍數以自身前瞻 23.9 倍為對照。"},"fwd_pe":23.89,"peg":0.67,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 23.9 倍、FY2 約 18.9 倍；利潤率歷史最高、盈餘處循環上段，倍數對近峰盈餘不算便宜，也未過熱。五年分位事實表未涵蓋，僅 4 個年度端點分位 37.8%。基準 5 年約 +26%、一年約 +6%，報酬中等偏弱，結論中性。","upside_short_pct":5.6,"upside_mid_pct":26.0},"trap_analysis":{"verdict":"🟡","label":"循環高點風險：獲利在高檔，非價值陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"SEMI 估 WFE 2028 年成長放緩至 14.1%；應材目標產出倍增、東京威力資本支出上調 48%；2001 年設備出貨年減 41%、Lam 出貨峰谷跌 80%，2023 年谷底毛利率 41.5%。","assumption":"2027 年逾 2,000 億美元的 WFE 中有客戶提前拉貨與擠潔淨室的成分，AI 資本支出一旦放緩，2028–29 年 WFE 下修 20%–30%。","consequence":"EPS 自高點回落 30%–40%、倍數壓到 15 倍，股價較現價跌 50%–60%，五年後仍虧損。","ruling":"採納為空頭情境主軸，空頭機率 30%；與唯一致命點（出口管制）不同源，屬獨立的第二條失敗路徑。","watch":"每季營收指引中點是否季減、SEMI 2028 年預測修正方向、記憶體客戶資本支出指引。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#3","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3"],"fact_refs":["f_kpi5_2026_12"]},{"view":"論點失敗","evidence":"10-K 列出若無法跟上 AI 需求擴產可能流失份額；12 月季指引因零組件吃緊而保守；FY2015 年報揭露部分元件只能向單一或少數供應商採購（舊揭露，本季法說證實零組件仍是瓶頸）。","assumption":"零組件瓶頸持續到 2027 年，客戶轉向有貨的對手。","consequence":"份額論點受損，跑贏 WFE 的紀錄中斷。","ruling":"暫時反駁：CEO 稱與疫情短缺不可比、很快追上，延後出貨移到 3 月季；但列為短期風險，3 月季驗證。","watch":"3 月季營收是否高於 12 月季實績、存貨與應付帳款變化。","evidence_refs":["competitive_share_entrants#2","geo_supply_chain#0"],"fact_refs":["f_kpi5_2026_12"]},{"view":"論點成功但股東經濟變差","evidence":"鋼鋁關稅推高 FY2026 製造成本；稅率由 11% 升至 16.5% 並延續；營業費用增加主因獎酬；FY2026 自由現金流利潤率由 29.4% 降至 21.1%；大客戶可壓價；未來五年逾 30 億美元研發實驗室與 15 億美元奧勒岡擴建。","assumption":"營收照預期成長，但成本、稅率與擴產資本吃掉一部分盈餘與現金。","consequence":"每股盈餘與自由現金流成長低於營收，回饋率低於 85% 目標。","ruling":"部分採納：稅率已進指引，9 月季自由現金流 32.4 億創新高；但 9 月季回饋率只 41%，若 FY2027 全年 <70% 即屬股東經濟變差。","watch":"FY2027 自由現金流÷淨利 ≥0.85、全年回饋率、毛利率是否守 51%。","evidence_refs":["reg_tariff_export#1","customer_second_source#0"],"fact_refs":["f_kpi3","f_kpi4_sbc_gaap"]},{"view":"價格已反映太多","evidence":"前瞻 23.9 倍對應的是歷史最高利潤率；FY1 共識三個月已上修 16.9%；賣方 22 位中 21 位買進，8 月均目標價 342 美元。","assumption":"共識已把 2027 年高點寫進去，再上修空間小，倍數向循環中段回歸。","consequence":"盈餘照預期，股價仍因倍數壓縮而停滯。","ruling":"部分反駁：股價 26 週已跌 13.9%、倍數由前份約 30 倍壓到 23.9 倍，價格先修了一段；但基準報酬約年 7%，不支撐追價加碼。","watch":"前瞻倍數 >28 倍且共識未再上修時視為過熱。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct","f_week26_return_pct"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 252.35 → 本次 230.1（-8.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=252.35","side_b":"本次 price_at_dd=230.1","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 252.35 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 252.35 美元：Bull 價 553.5、Bear 價 119，五年期望值 +32.9%，基準年化 7.4%，不對稱比 2.0","side_b":"本次情境、股價仍用 252.35 美元：Bull 價 516、Bear 價 142.5，五年期望值 +19.8%，基準年化 2.8%，不對稱比 2.0","ruling":"先換情境、股價不動：五年期望值少 13.1 個百分點，基準年化少 4.6 個百分點。不對稱比由 2.0 變為 2.0。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 252.35 美元：五年期望值 +19.8%，基準年化 2.8%，不對稱比 2.0","side_b":"本次情境、股價 230.1 美元：五年期望值 +31.4%，基準年化 4.7%，不對稱比 2.72","ruling":"再換股價、情境不動：起點價下跌 8.8%，五年期望值多 11.6 個百分點，基準年化多 1.9 個百分點，不對稱比由 2.0 升到 2.72。合計五年期望值比前份少 1.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價與基本面背離","cause":null,"side_a":"股價 26 週跌 13.9%、RSI 24.6；法說當日一家記憶體大廠稱優先 3D DRAM 而非 4F²，股價下跌，市場在折現循環高點與 DRAM 路線疑慮。","side_b":"同期 FY1 共識三個月上修 16.9%，CY2027 WFE 由不給數字變成逾 2,000 億美元；CEO 稱跳到 3D DRAM 只會讓蝕刻沉積強度更早上升。","ruling":"可調和（程度差異）：市場提前折現 2028 年降溫，CEO 對 3D DRAM 的說法採信但未證。偏基本面側，持有不追價。","evidence_level":"公司法說＋共識快照","settle_metric":"1 月法說 CY2027 WFE 定案數字與 3 月季營收指引","if_then":["若 1 月法說 CY2027 WFE ≥1,900 億美元且股價 ≤200 美元，分兩批加碼至衛星上限","反向：若 WFE 展望下修至 1,800 億美元以下，停止加碼並把空頭機率上調至 35%"],"evidence_refs":[]},{"axis":"中國營收占比","cause":null,"side_a":"2026-01 公司預期 CY2026 中國占比降至 30% 以下（Zacks 轉述）。","side_b":"9 月季中國占 35%（6 月季 26%），CFO 稱完全如預期；12 月季將明顯下降，主因中國本土客戶。","ruling":"可調和：季度波動，全年仍可能接近 30%。9 月季本土客戶拉貨是否為管制到期前搶出貨屬推論、未證，12 月季的落差就是驗證。","evidence_level":"公司法說＋10-K 地區營收","settle_metric":"12 月季 10-Q 中國營收占比與總營收","if_then":["若 12 月季中國占比降到 20% 以下但總營收仍達指引下緣 82 億美元，視為已吸收，維持持有","反向：若中國下滑拖累總營收低於 82 億美元，停止加碼"],"evidence_refs":["geo_supply_chain#2","customer_concentration_credit#3"]},{"axis":"管理層前後說法對照","cause":null,"side_a":"2026-07-29 CFO 指引 9 月季營收 81 億±4 億、毛利率 52%、營業利益率 39.5%、EPS 2.15 美元；CEO 稱 CY2026 WFE 1,500 億出頭、2027 年不給數字；當時遞延收入增加主因客戶預付款。","side_b":"9 月季實績 82.2 億、52.4%、40.2%、2.20 美元，全數高於中點；WFE 上修為約 1,550 億，2027 年首度給出逾 2,000 億；本季遞延收入增加來自銷量，客戶預付款反而減少。","ruling":"一致：說到做到，未見改口。唯一的退步訊號是客戶預付款減少，可能是急迫性降溫，也可能只是銷量放大，未證。","evidence_level":"兩季法說逐字稿","settle_metric":"下一季遞延收入與預付款變化","if_then":["若 12 月季預付款續降且遞延收入轉為季減，停止加碼並提前檢視減碼門檻","反向：若預付款回升，維持"],"evidence_refs":[]},{"axis":"股東回饋承諾與實際","cause":null,"side_a":"長期承諾回饋自由現金流 85%（7 月法說說至少 85%）。","side_b":"9 月季只回饋 41%、年初至今 59%；現金由 56 億增至 75 億美元，另償還 7.5 億到期債。","ruling":"可調和：加速回購在 12 月季續執行，增加現金是為支應擴產與營運規模；FY2027 全年回饋率 <70% 才算偏離。","evidence_level":"公司法說","settle_metric":"FY2027 全年回饋率","if_then":["若 FY2027 回饋率 <70% 且現金續增，資本配置評估下修一級","反向：若 12 月季回購加速、回饋率回到 85% 以上，維持"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":null,"side_a":"賣方：利潤率歷史最高、同業大舉擴產、共識三個月已上修 17%，2027 年是受限下的高點且含提前拉貨，設備業歷史下行可達 −41%；現在賣在盈餘高點、倍數尚未壓到循環中段。","side_b":"持有方：股價已跌 13.9%、倍數由約 30 倍壓到 23.9 倍；客戶需求能見度到 2028 年，CFO 稱明年 10 座一線新廠上線，不受限需求高於 2,000 億；份額連三年上升。","ruling":"不賣、不追高加碼：2027 年盈餘能見度高，賣點留給營收指引連兩季季減或唯一致命點發生。","evidence_level":"公司法說＋SEMI 預測＋設備業下行史","settle_metric":"每季營收指引中點方向","if_then":["若連續兩季營收指引中點季減，減碼一半","反向：若 1 月法說 WFE ≥1,900 億且價格 ≤200 美元，加碼"],"evidence_refs":[]},{"axis":"前份漂移：價格變動","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-07-30，股價 252.35，前瞻約 30 倍）：綜合評級 B、估值中性 🟡、裁決進場、角色衛星。","side_b":"本次（股價 230.1，前瞻 23.9 倍）：綜合評級 B、估值中性 🟡；裁決與角色由程式依本次輸入重算。","ruling":"股價跌約 9%、前瞻倍數明顯壓縮，但盈餘處循環高檔、利潤率創新高，估值結論與綜合評級不變。","evidence_level":"價格與共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：新證據確認","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap","archetype","cycle_position"],"side_a":"前份：護城河趨勢 ↑、五年後跑道 🟢、陷阱風險 🟡、循環/商品型、中循環。","side_b":"本次全部維持：SAM 占比上升、連三年跑贏 WFE、背面供電與乾式光阻新增指定機台（護城河 ↑）；先進封裝 2026 年成長逾 70%、面板級封裝出貨逾 20 家（跑道 🟢）；衰退訊號亮 1 個（陷阱 🟡）；WFE 2027 年仍增 30%、2028 年放緩，同業擴產（中循環）。","ruling":"新一季證據強化原判斷，五欄皆不變；中循環維持，若 1 月法說後 2028 年展望轉弱則改判晚循環。","evidence_level":"2026-10-21 法說＋SEMI 預測","settle_metric":"1 月法說 2028 年展望","if_then":["若 2028 年 WFE 展望持平或下修，循環位置改判晚循環並停止加碼"],"evidence_refs":[]},{"axis":"前份漂移：機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份機率多頭 26%、空頭 30%，最大回撤單點 −60%。","side_b":"本次多頭 25%、基準 45%、空頭 30%；最大回撤改填範圍 −40%～−60%。","ruling":"回撤改填範圍並依設備業下行史推導；共識成長超過內生上界，空頭機率須守 30%；多頭下調 1 個百分點反映零組件供給限制。","evidence_level":"方法調整","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼待兩約束同時解除：10月法說CY2027 WFE≥$180B且NAND合約價未連2季跌；且關聯方規則到期處置明朗（衝擊<$150M/季）。獨立分支：價格≤$200且R1未觸發","side_b":"加碼待兩條件之一：①關聯方規則到期後12月季中國衝擊<1.5億美元且1月法說CY2027 WFE≥1,900億美元；②價格≤200美元且季營收指引未季減","ruling":"加碼條件改寫：10 月法說已給出逾 2,000 億，原 1,800 億門檻已過，新門檻改看 1 月定案數字 1,900 億；NAND 合約價事實表未涵蓋，改用公司營收指引方向這個可觀察指標；關聯方規則門檻 1.5 億美元保留。","evidence_level":"2026-10-21 法說","settle_metric":"1 月法說 WFE、12 月季中國營收","if_then":["兩條件任一成立即分兩批加碼至衛星上限"],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）。","side_b":"美國出口管制擴大至 Lam 在中國的核心蝕刻沉積品項（MATCH Act 立法或新規涵蓋在華跨國廠），12–24 個月機率約 25%。","ruling":"本輪補上 Single Thing：中國占營收約 34%，是數學上最大的單一敏感度；前份把它放在風險 R2，未獨立成唯一致命點。發生即減碼至半倉。","evidence_level":"10-K 與 10-Q 風險因子","settle_metric":"商務部與國會公告","if_then":["發生且只涵蓋中國本土客戶：減碼至半倉","發生且涵蓋在華跨國廠：清倉"],"evidence_refs":["reg_tariff_export#0","reg_tariff_export#3"]},{"axis":"前份漂移：退出指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設退出指標（空值）。","side_b":"營收指引連兩季季減；毛利率連兩季 <50%；1 月法說 CY2027 WFE <1,800 億美元；出口新規後中國占比 <20% 且總營收季減。","ruling":"本輪補上四條可觀察門檻，分別對應減碼一半、停止加碼與清倉的動作，取代前份只寫在加碼條件裡的隱含門檻。","evidence_level":"方法調整","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"1 月法說 CY2027 WFE 展望定案","type":"假設驗證","maps_to":"H1","metric":"公司 CY2027 WFE 展望","threshold":"≥1,900 億美元維持；<1,800 億美元視為削弱","action":"<1,800 億則停止加碼、空頭機率升至 35%","source_freq":"每季法說","date":"2027-01"},{"n":2,"text":"出口管制關聯方規則暫緩到期處置","type":"風險","maps_to":"R2","metric":"12 月季中國營收中屬管制造成的減少額","threshold":"管制衝擊 ≥1.5 億美元／季，或規則擴大到 Lam 核心蝕刻沉積品項","action":"停止加碼","source_freq":"聯邦公報＋10-Q","date":"2026-10-30","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3"]},{"n":3,"text":"美國出口管制擴大至 Lam 在中國的核心蝕刻沉積品項","type":"Single Thing","maps_to":"single_thing","metric":"出口新規適用範圍","threshold":"MATCH Act 立法或新規涵蓋中國本土以外的在華跨國廠","action":"減碼至半倉；涵蓋跨國廠則清倉","source_freq":"國會與商務部公告（事件）","date":null,"evidence_refs":["reg_tariff_export#3","geo_supply_chain#1"]},{"n":4,"text":"價格回落加碼分支","type":"估值rearm","maps_to":"H1","metric":"股價與季營收指引中點","threshold":"價格 ≤200 美元且最新季營收指引中點未季減","action":"分兩批加碼至衛星上限","source_freq":"每日價格＋每季指引","date":null},{"n":5,"text":"循環轉折：營收指引連續季減","type":"減碼","maps_to":"R1","metric":"下一季營收指引中點相對當季實績","threshold":"連續兩季指引中點季減","action":"減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"]},{"n":6,"text":"份額論點反轉","type":"清倉","maps_to":"H2","metric":"Lam 年度營收成長率減 WFE 成長率","threshold":"連續兩年跑輸 WFE 且毛利率連兩季 <49%","action":"清倉","source_freq":"年度法說","date":null},{"n":7,"text":"零組件供給吃緊是否在 3 月季解除","type":"風險","maps_to":"R5","metric":"3 月季營收相對 12 月季實績","threshold":"3 月季營收低於 12 月季實績","action":"停止加碼","source_freq":"每季財報","date":"2027-04","evidence_refs":["competitive_share_entrants#2"]},{"n":8,"text":"1 月法說後重跑完整判斷","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑完整判斷","source_freq":"一次","date":"2027-01-31"}],"kill_metrics":[{"metric":"下一季營收指引中點相對當季實績","bear_threshold":"連續兩季季減→減碼一半","window":"2027-01 至 2027-07 法說","source":"公司新聞稿與 8-K","last_status":"ok"},{"metric":"單季 non-GAAP 毛利率","bear_threshold":"連兩季 <50%→停止加碼；<49% 且跑輸 WFE→清倉","window":"2026-12 季起四季","source":"公司新聞稿","last_status":"ok"},{"metric":"公司 CY2027 WFE 展望","bear_threshold":"1 月法說 <1,800 億美元→停止加碼","window":"2027-01 法說","source":"法說逐字稿","last_status":"ok"},{"metric":"出口新規後中國營收占比與總營收","bear_threshold":"中國占比 <20% 且總營收季減→減碼至半倉","window":"2026-11 至 2027-06","source":"10-Q 地區營收","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2027 年當循環頂點並對 DRAM 架構路線反應過度；但 2027 年逾 2,000 億美元是供給受限下的數字（CFO 稱不受限需求更高），客戶需求能見度到 2028 年，且跳到 3D DRAM 只會讓蝕刻沉積強度更早上升。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='↑', week26=-13.92, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"加碼待兩條件之一：①關聯方規則到期後12月季中國衝擊<1.5億美元且1月法說CY2027 WFE≥1,900億美元；②價格≤200美元且季營收指引未季減","exec_line":"持有不追高；條件①或②成立分兩批加碼；連兩季營收指引中點季減減碼一半；Single Thing 發生減碼至半倉；管制擴及在華跨國廠或份額轉跌則清倉。"},"reasoning":{"industry":"9 月季營收 82.2 億美元（季增 22%、年增 54%），non-GAAP 毛利率 52.4%、營業利益率 40.2%，均創新高；12 月季指引 86 億±4 億美元、EPS 2.33 美元，CFO 表示零組件吃緊壓低指引，延後的出貨移到 3 月季。系統營收組合：記憶體 46%（NAND 26%、DRAM 20%）、晶圓代工 46%、邏輯及其他 8%；地區：中國 35%、韓國 20%、台灣 18%。服務事業單季近 25 億美元、年增 40%。景氣處擴張期：公司估 CY2026 WFE 約 1,550 億美元、CY2027 逾 2,000 億美元，客戶需求能見度到 2028 年，今年受潔淨室限制、明年再加上零組件。產業態勢為雙向拉鋸：結構面轉好（3D 化、先進封裝、背面供電推高蝕刻沉積強度），對上競爭面（應材目標倍增產出、東京威力擴產、中國本土廠升級）與出口管制。單點依賴：前四大客戶 FY2026 占營收約 55%，中國約 34%，屬集中度風險，不當護城河證據。","moat":"機制是製程指定機台：新節點的蝕刻沉積步驟一旦在客戶產線驗證通過便進入量產配方，換供應商要重新認證；裝機量再帶出升級、零件與服務收入。方向證據：SAM 占 WFE 擴大約 4 個百分點，2026 年為連續第三年跑贏 WFE；本季在一家領先客戶的背面供電四項產品全拿下指定機台，乾式光阻累計營收預期上調約 10 億美元至約 25 億美元（2026-10-21 法說，CEO）。事實表只有同業利潤率，無 ROIC 差距：Lam 營業利益率高於應材、與 ASML 相當、低於 KLA。執行力給 8 分（連五季營收新高、指引全數達成），定價力給 7 分（毛利率新高且有調價，但四家客戶占營收過半、可壓價）。當期報酬：高利益率、低資本支出強度；增量報酬約 138%、再投資率約 11.5%，內生成長上界約 16%。","growth":"成長以量為主（WFE 擴張加 SAM 占比上升），價與組合為輔（毛利率朝中 50% 推進、調價），淨回購每年約 2%（稀釋股數由 FY2023 約 13.6 億降至 FY2026 約 12.6 億，以淨利÷EPS 推得）。共識三年 EPS 年複合：FY2026A 5.76 美元→FY2029E 14.44 美元，(14.44÷5.76)^(1/3)−1≈35.9%。缺口約 20 個百分點：營業利益率由 TTM 35.3% 升到指引 40.5% 與循環量能是主因，淨回購貢獻約 2 個百分點，其餘屬循環性、無法歸給可延續的再投資，長期信心上限為中。衰退訊號亮 1 個：共識 FY2026→FY2028 EPS 年複合約 45% 高於營收年複合約 35.5%，差距約 10 個百分點；FY2026 自由現金流÷淨利 0.67 只一年，未亮。長期成長性 🟡、價值陷阱風險 🟡。","governance":"9 月季自由現金流 32.4 億美元創新高（營業現金流 35.0 億減資本支出 2.58 億），回購約 10 億、股息 3.25 億，另進行中的加速回購延續到 12 月季；年初至今回饋 59%，並償還 7.5 億到期債。股權酬勞單季 1.15 億美元，占營收 1.4%，對 2,880 億美元市值每年稀釋約 0.16%，遠低於 1.5%；稀釋股數 FY2023→FY2026 約減 7%。回購買入收益率無法驗：回購均價與 10 年期殖利率事實表未涵蓋，以現價計前瞻盈餘殖利率約 4.2%。近 12 個月無併購。淨現金約 37 億美元。FY2026 自由現金流÷淨利 0.67（存貨與擴產），9 月季已回升。","valuation":"股價 230.1 美元，前瞻本益比 23.9 倍（FY1 EPS 9.63）、FY2 約 18.9 倍、trailing 34.3 倍；26 週跌 13.9%、RSI 24.6，同期 FY1 共識三個月上修 16.9%，倍數壓縮全數抵銷盈餘上修。trailing 本益比在 4 個年度端點內分位 37.8%，非五年分位，五年分位事實表未涵蓋。PEG 以共識三年 EPS 年複合 35.9% 計約 0.67，但這是循環回升的成長率，不能當便宜依據；改用 FY1→FY3 年複合約 22.5% 則約 1.06。分母處循環高檔、利潤率創新高，前瞻倍數對近峰盈餘不算便宜。基準 5 年終端 20 倍×FY2031E 14.5 美元≈290 美元，較現價約 +26%；一年以 FY2 12.15 美元×20 倍≈243 美元，約 +5.6%。同業本益比事實表未涵蓋，終端倍數只能對照自身現值 23.9 倍。","premortem":"設備業下行史：2001 年全球設備出貨年減 41%，Lam 出貨峰谷跌 80%；2023 年谷底毛利率 41.5%。本輪客戶擠潔淨室、提前專案（CFO 原話），2027 年部分需求是提前拉貨。第二條路是中國：9 月季中國占 35%，12 月季將明顯下降，出口管制擴大會把這塊直接拿掉。第三條是倍數：前瞻 23.9 倍若在 2027 年 WFE 持平時回到循環中段，股價與盈餘同跌。陷阱評估 🟡：不是價值陷阱，而是高點陷阱風險。"},"plain":{"six":{"how_it_makes_money":"賺晶圓廠擴產與製程升級的錢：蝕刻與沉積設備約七成、裝機服務與升級約三成；錢卡在每一代 3D 結構與先進封裝都需要更多蝕刻沉積步驟這一節點。","moat":"護城河擴大（↑）：蝕刻龍頭、NAND 最大裝機量，SAM 占比與份額同步上升，連續第三年跑贏 WFE；等級 B，威脅集中在中國本土替代與同業擴產。","growth":"跑道寬（🟢）：WFE 2027 年逾 2,000 億美元，另有先進封裝、背面供電、面板級封裝、NAND 分層儲存等新曲線；但共識三年 EPS 年複合約 36%，遠高於內生上界約 16%，差距靠循環上行的營運槓桿與利潤率擴張。","capital":"資本配置中上：無併購、股權酬勞稀釋極低、股數逐年下降；但 9 月季只回饋自由現金流 41%，現金累積到 75 億美元。","valuation":"現價要求 FY2028 年 EPS 站上 12 美元且下一輪下行不深於 2023 年；2027 年我們相信，2028 年後的循環深度不確定，估值中性。","how_wrong":"最可能看錯在循環轉折時點：2027 年是供給受限下的高點，2028 年 WFE 成長放緩、同業大舉擴產，一旦記憶體客戶縮手，EPS 與倍數會同時下修。"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2027 年當循環頂點並對 DRAM 架構路線反應過度；但 2027 年逾 2,000 億美元是供給受限下的數字（CFO 稱不受限需求更高），客戶需求能見度到 2028 年，且跳到 3D DRAM 只會讓蝕刻沉積強度更早上升。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"prior_verdict":"進場","prior_role":"衛星","wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":230.1,"week26_return_pct":-13.92,"consensus_rev_3m_pct":16.87,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母無一次性項目：稅率升至 16.5% 已反映在指引，12 月季供給延後屬時點移轉。循環高檔盈餘的風險放在空頭機率與終端倍數處理，不靠分母修正。"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"regulatory","event":"出口管制關聯方規則一年暫緩到期（前份判斷記載約 10-30）","impact":"高","watch":"是否延長暫緩或擴大適用；12 月季中國營收衝擊是否 <1.5 億美元"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"12 月季財報與 CY2027 WFE 定案展望","impact":"高","watch":"WFE ≥1,900 億美元；3 月季營收指引是否補回延後出貨"},{"date":"2027-04","date_precision":"month","type":"capacity","event":"3 月季財報：零組件供給吃緊是否解除","impact":"中","watch":"營收是否高於 12 月季實績、存貨與應付帳款變化"}],"_projected_from":"v19"}
```
