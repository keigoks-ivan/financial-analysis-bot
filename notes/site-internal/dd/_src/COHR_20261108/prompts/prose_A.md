你是 stock-analyst v20 的**散文層（prose）agent**，標的 COHR（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：COHR　日期：2026-11-08　archetype：None　前份裁決：2026-09-01　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1787B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（700B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1003B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1078B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1068B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（560B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（798B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2064B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4129B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2579B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1787           3649-5213      5 條（2–6 內）  
s3                  8000         700           5110-7300      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3149          8296-11851      5 條（2–6 內）  
s6                 11000         560          7308-10440      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         798           1891-2702      5 條（2–6 內）  
s10                 5000        2064           2055-2936      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2579           2000-2421      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4670B；至少需散文≈40.33KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−92.7
−60%
−60
−45%
−45
−42.49
−42%
−30.6%
−23.28%
−10.3
−8.68
−0.42%
0
0.32
0.48
0.7
0.75
0.77%
0.8
0.84
01
1
1.1
1.24
1.4%
1.5%
1.6
1.8
2
02
2.05
2.09
2.28
2.38
2.4
2.48
2.5
2.7
3
3%
3.1%
3.7
3.9
4%
04
4
4.12
4.47
5
05
5%
5.1
5.13
5.7
5.81
5.9
06
6
6.2
6.6%
7
7.3
8%
08
8
8.05
8.1
8.2
8.5%
8.5
9%
9
09
9.2
9.21%
9.4
9.42
9.52%
10%
10
10.0
10.6
11
11.4
11.5
12
12%
12.67%
13.4
13.8
13.80
13.97
14
14.0
14.11%
14.7%
14.8%
15
15%
15.8
15.9%
16%
16
16.5
16.9%
17
17%
17.5
18
18%
19%
19.13
20
20%
20.47
20.7
21%
21
22%
22
22.5
23.2%
23.35%
23.4
23.5
23.7
24
25%
25
25.5
25.9
26
27%
27
27.5
28.5%
28.92%
30
30%
30.6%
30.7%
30.7
31
32%
32.7%
34%
35%
36
36%
37
38.16%
38.9%
39%
39.92
40%
40
40.6%
40.7
40.7%
41%
41.2
41.5%
42%
42
42.1%
42.49%
42.5%
43%
44.1
45%
45
45.91%
46.8
48.3%
49
50%
52
54.3%
54.3
56%
57.13%
60
60%
62.6
70%
70
73.2
78
79%
80%
82%
84
84%
85%
88.9%
100%
100
104.7%
105.98
111.6
112
150%
155
155.0
168
181
184
192.81
197
200
201
210
212
220
232
241%
250
252
260
270
271
277.83
293
297
297.5
300
$300
320
367
400
731
756
775.5
800
843
900
2026
2027
2028
2030
20261108
1,031
1,761
37,976
5,810
7,118
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
{"meta":{"ticker":"COHR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Coherent Corp."},"oneliner":"AI 光通訊缺貨與多年長約讓 CY27 訂單近滿，毛利率目標上調到 45% 以上；但最新一季自由現金流 −8.68 億美元。股價 26 週跌 42% 後，FY29 共識兌現就有報酬，爭點在 CY28 以後的供需。","thesis":{"H":[{"id":"H1","text":"AI 光互連需求到 FY28 有訂單與長約支撐，資料中心與通訊段維持高成長。","2y":"FY27 Q4 單季營收超過 30 億美元，FY28 內出現單季 40 億美元。","5y":"PhotonLink 成為數十億美元產品線，接替可插拔模組放緩的部分。","10y":null,"threshold":"FY27 Q4 營收 ≥30 億美元；資料中心與通訊段年增 ≥30%","source":"公司季報與法說，每季","drift_rule":"段營收年增相對 30% 門檻連 2 季偏離 5% 以上（低於 28.5%）為削弱；連 3 季偏離 10% 以上（低於 27%）為反轉。"},{"id":"H2","text":"毛利率擴張由定價轉向成本：內部 6 吋磷化銦比例上升，單季非 GAAP 毛利率超過 45%。","2y":"2027-06 季毛利率 ≥42%，內部雷射比例開始上升。","5y":"CY28 底前單季超過 45%，新產品占比提高後仍能維持。","10y":null,"threshold":"非 GAAP 毛利率不低於 40%；CY28 底前單季 >45%","source":"公司季報與法說，每季","drift_rule":"TTM 毛利率連 4 季低於規劃路徑 5% 以上為削弱，連 6 季低於路徑 10% 以上為反轉。"},{"id":"H3","text":"這輪資本支出能轉成現金回報，不需要大幅稀釋股東。","2y":"FY27 全年營業現金流高於 FY26 的 0.8 億美元，FY28 全年自由現金流轉正。","5y":"自由現金流利潤率高於 FY23～FY25 的 3～4%。","10y":null,"threshold":"FY27 全年營業現金流 >0.8 億美元；FY28 自由現金流 >0；槓桿 ≤2 倍","source":"10-Q、10-K 現金流量表","drift_rule":"FY27 全年營業現金流未轉正為反轉；FY28 自由現金流為負且資本支出占營收超過 20% 為削弱。"}],"R":[{"id":"R1","text":"客戶集中與向後整合：前兩大客戶占 32%，大客戶可能自製雷射或扶植第二來源。","h_ref":"H1","clock":"🔥","threshold":"最大客戶占比由 20% 降到 10% 以下，或有可靠來源確認自製雷射導致轉單","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0","competitive_share_entrants#0"]},{"id":"R2","text":"AI 資本支出消化與 CY28 磷化銦過剩，同時打擊營收、定價與產能利用率。","h_ref":"H1／H3","clock":"🔥","threshold":"非 GAAP 毛利率連 2 季年減，或 EML 報價連 2 季下跌，或雲端資本支出指引連 2 季下修超過 20%","evidence_refs":["supply_demand_durability#2"]},{"id":"R3","text":"現金流與融資：資本支出持續上升，現金只夠支應約 2.7 季目前的流出速度。","h_ref":"H3","clock":"⚡","threshold":"Q2 FY27 營業現金流仍為負且資本支出再增，或股權增資超過 5%，或槓桿超過 2 倍","evidence_refs":["supply_demand_durability#2"]},{"id":"R4","text":"CPO 替代可插拔模組，以及中國廠在下一代模組份額擴大。","h_ref":"H1／H2","clock":"🐢","threshold":"CPO 滲透率超過 30% 且 PhotonLink 未達每季 2.5 億美元，或可靠來源顯示公司在主要客戶份額下滑","evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#4"]},{"id":"R5","text":"出口管制、關稅與磷化銦基板供應。","h_ref":"H2","clock":"🔥","threshold":"非 GAAP 毛利率單季下降 ≥100 個基點且公司歸因於關稅或管制，或基板出口許可收緊","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]}],"single_thing":{"description":"前兩大客戶之一在 CY28 前下修或延後長約承諾量（含改用自製雷射或轉單）。","why_fatal":"FY26 最大客戶占營收 20%。以 FY28 共識營收 155 億美元估約 31 億美元，毛利率 45% 時少 14 億美元毛利，稅後約 11 億美元，每股約 5.7 美元，占 FY28 共識 EPS 13.97 美元約 41%。同期高資本支出與負自由現金流不會同步下降。","if_happens":"確認後一週內減碼一半；若毛利率同時連 2 季年減，清倉。","how_monitor":"10-K、10-Q 的主要客戶占比、剩餘履約義務與合約負債，法說對長約的描述，以及供應鏈報導。","probability":"15%～20%（12～24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.8,"peg_fy2":0.32,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2026A":4.12,"FY2027E":9.42,"FY2028E":13.97,"FY2029E":19.13},"fy_end_month":6,"eps_basis":"FY27～FY29 為 Koyfin 共識，研判屬非 GAAP，EPS 家數事實表未涵蓋。基期 FY26 只有 GAAP 稀釋 EPS 4.12 美元，含處分利得；FY26 非 GAAP 全年數事實表未涵蓋，因此基期不能與共識直接算複合成長。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COHR_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"低","fingerprint":"需求有長約、毛利率上行，但 FY23、FY24 仍虧損，FY26 自由現金流為負，品質還沒有被現金證明，盈餘也仍受 AI 資本支出週期主導。"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高。幾乎所有資料中心產品線仍受磷化銦限制（2026-08-12 CEO），FQ2 資料中心訂單出貨比超過 4 倍；但公司 CY27 底前內部產能再翻倍以上，且已規劃 2027 年後續擴，法說上已有分析師問 CY28 過剩。判斷擴張期的依據是訂單與產能，不是股價。4 倍訂單出貨比可能含重複下單，事實表未涵蓋拆分。","bargaining":{"up":"基板供應商超過 5 家，多家已簽長約，CEO 稱足以支應 CY27 擴產；公司自身的中國來源比例事實表未涵蓋。","down":"前兩大客戶占 32%，買方議價力上升；缺貨讓公司目前仍能調價，長約價格多已約定。","geo":"實體清單與 232 關稅調查不利；FCC 若禁中國光模組對公司有利，但僅單一來源，公司 2026-08-12 也稱該報導屬臆測。"},"profit_pool_dir":"往上游雷射與整合光學移動；雷射產能鬆動後，利潤可能回流模組廠與客戶。五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"2026 年 AI 光收發模組市場","value":"約 260 億美元（TrendForce，次級來源）"},{"item":"2030 年資料中心與通訊可及市場","value":"約 900 億美元（管理層 11-04 估計，未獨立驗證）"},{"item":"其中 CPO、NPO、晶片間光互連","value":"約 300 億美元（2030 年，管理層估計）"},{"item":"OCS 可及市場","value":"至少 40 億美元（2030 年，管理層估計）"},{"item":"公司滲透率","value":"23.7 億美元×82%×4≈78 億美元年化，對 900 億美元約 9%"},{"item":"五年營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"自家 6 吋磷化銦雷射產能、完整光鏈產品組合與多年長約。CFO 2026-08-12 稱 6 吋產出為 3 吋 4 倍、成本約一半；CEO 11-04 稱德州與瑞典 6 吋良率高於 3 吋。客戶願意預付並簽到本十年底，轉換成本落在重新認證與設計卡位。","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：內部磷化銦產能提前一季翻倍。定價面擴大：Q1 毛利率年增 184 個基點，定價優化是主要來源之一，目標由 42% 以上上調到 CY28 底前 45% 以上。反例：內部雷射比例一年未變，成本優勢尚未進損益；Lumentum 利潤率仍明顯較高。若 2027 年中前內部比例仍未上升，或出現主要客戶份額下滑的可靠來源，方向改為持平。","peer_na_reason":"同業 ROIC 序列事實表未涵蓋，改用毛利率、營業利益率與自由現金流利潤率比較。","threats":[{"level":"🔴","text":"大客戶向後整合或自製 CPO 光源雷射。10-K 自承可能誤判客戶向後整合的能力；CY2028 以後自製的說法來自非獨立研究頁，未核實。","p":"20%","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"]},{"level":"🔴","text":"CPO 與 NPO 替代可插拔收發模組。公司有 PhotonLink 對沖，但內容價值與份額可能和模組時代不同。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"中國模組廠在下一代產品份額擴大，2.4T 單一來源估計公司僅 20～30 萬件。","p":"30%","evidence_refs":["competitive_share_entrants#4"]},{"level":"🔴","text":"Lumentum 擬併 Marvell，對手可能同時掌握雷射與晶片；CEO 主張客戶更需要獨立供應商，尚無訂單數據驗證。","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×低周轉（暫定，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"用光取代銅線是頻寬與距離的實際需要，但採購量取決於 AI 資本支出；法說已有分析師提出資料中心融資與建置許可疑慮。代理讀數：CY27 訂單近滿。"},{"item":"決策層級","level":"🟢","text":"替代要看單一插槽與客戶認證。長約多到本十年底並含預付，200 億美元長約為期五年。反例：2026-08-12 被問 CY28 承諾量時沒有給數字。"},{"item":"價值鏈分配","level":"🟡","text":"缺貨期利潤往雷射端移，但前兩大客戶占 32%，且有能力與動機自製或扶植第二來源，產能鬆動後分配可能反轉。"},{"item":"社會容忍度","level":"🟢","text":"產品是企業基礎建設零組件，消費者不直接付費，價格上限主要來自客戶議價；出口管制與關稅另列風險。"}],"roiic":"16.9%","reinvest_rate":"241%","endo_ceiling":40.7,"formula_note":"代理估算，D&A 與營運資金明細事實表未涵蓋。FY26 營業利益增量＝7,118×12.67%−5,810×9.21%≈367 百萬美元；稅率取財測中位 19%，稅後增量≈297；NOPAT≈731；淨再投資以 NOPAT−FCF≈731+1,031＝1,761 代理；增量 ROIC≈16.9%，再投資率≈241%，內生上界≈40.7%。再投資率超過 100% 靠舉債、處分資產與客戶預付，只用自有現金時上界約 17%。資本支出領先營收 1～2 年，這個增量報酬可能低估；CFO 稱 18 個月回收，目前無法驗證。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","COHR":38.16,"LITE":45.91,"CIEN":44.07,"AAOI":28.92,"MTSI":57.13,"unit":"%"},{"metric":"營業利益率","COHR":14.11,"LITE":23.35,"CIEN":14.12,"AAOI":-10.58,"MTSI":18.97,"unit":"%"},{"metric":"FCF 利潤率","COHR":-23.28,"LITE":9.52,"CIEN":13.53,"AAOI":-100.9,"MTSI":9.44,"unit":"%"},{"metric":"研發密度","COHR":10.18,"LITE":12.47,"CIEN":15.36,"AAOI":18.06,"MTSI":23.23,"unit":"%"}],"competitors":[{"name":"LITE","gm":45.91,"om":23.35,"fcf_margin":9.52,"rd_intensity":12.47,"period":"TTM ending 2026-09-30（4季加總）"},{"name":"CIEN","gm":44.07,"om":14.12,"fcf_margin":13.53,"rd_intensity":15.36,"period":"TTM ending 2026-07-31（4季加總）"},{"name":"AAOI","gm":28.92,"om":-10.58,"fcf_margin":-100.9,"rd_intensity":18.06,"strategy_note":"毛利率 28.92%、營業利益率為負，現金流大幅流出，目前還不構成成本威脅。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MTSI","gm":57.13,"om":18.97,"fcf_margin":9.44,"rd_intensity":23.23,"period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（1.6T、800G、scale-across、PhotonLink、OCS），價與產品組合為輔；沒有併購或回購貢獻。","runway_years":4,"runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段內生上界 40.7%（增量 ROIC 約 16.9%×再投資率約 241%）；共識 FY27→FY29 EPS 年化約 42.5%，超出約 1.8 個百分點，歸因於毛利率與營業費用槓桿。","segments":[{"item":"資料中心與通訊段","value":"Q1 占營收 82%，季增 21%、年增 79%"},{"item":"資料中心","value":"Q1 季增 17%、年增 85%"},{"item":"通訊","value":"Q1 季增 34%、年增 84%；scale-across 超過 2 億美元"},{"item":"工業段","value":"Q1 pro forma 季比與年比持平，訂單強，管理層預期本季恢復成長"},{"item":"PhotonLink","value":"管理層目標：3 月季超過 1 億美元，CY27 底前每季超過 2.5 億美元"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":false,"evidence":"Q1 年增 184 個基點"},{"name":"核心市占近 12 個月縮減","lit":false,"evidence":"沒有可靠份額序列，2.4T 僅單一來源，列為資料缺口"},{"name":"主力產品提價後銷量下滑","lit":false,"evidence":"定價優化期間量仍成長"},{"name":"EPS 成長顯著高於營收成長","lit":true,"evidence":"FY27→FY28 共識 EPS 年增 48.3%、營收 38.9%，差 9.4 個百分點；Q1 年增 80% 對 50%"},{"name":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"FY26 為負、FY25 約 3.9 倍，尚未連 2 年；FY27 續負就亮燈"},{"name":"SBC／營收超過 5% 且逐年上升","lit":false,"evidence":"Q1 為 3.1%"},{"name":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"CPO 有替代風險，但公司已取得 PhotonLink 長約"},{"name":"產業估值倍數 3 年系統性下移","lit":false,"evidence":"事實表未涵蓋"},{"name":"維持性資本支出占 FCF 超過 60%","lit":false,"evidence":"FCF 為負，無法計算"},{"name":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"資本支出仍在增加"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠內部擴產與長約，不靠併購；股利與回購沒有紀錄，沒有可展開項目。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表未涵蓋過去併購投入與報酬；近 12 個月沒有併購完成項目，只有處分航太國防與慕尼黑業務。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"法說與事實表都沒有回購紀錄，現金優先用於擴產與還債。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q1 SBC 73.2 百萬美元×4≈293，除以市值 37,976≈0.77%／年，低於 1.5%；實際股數變化序列事實表未涵蓋。","grade":"過"}]},"valuation":{"basis":"FY1 共識 EPS 的前瞻本益比，搭配隱含預期反推；trailing 本益比含處分利得且分位只有一個年度端點，不採用。","tier":"光通訊零組件與雷射","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比；系統商與類比晶片也不宜跨層當錨。"},"fwd_pe":20.47,"peg":0.48,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"FY1 本益比 20.47 倍（192.81÷9.42）；FY1→FY3 EPS 年化約 42.5%，PEG 約 0.48，只作參考。主要依據是隱含預期：10% 報酬率與 15 倍終端本益比下，FY31 EPS 約 20.7 美元即可。基本情境五年年化約 14.7%，全部來自盈餘成長，倍數由 20.47 倍降到 17 倍。反例：自由現金流為負，非 GAAP 口徑排除 SBC 與攤提；若營業利益率回到 18%，現價接近合理價，沒有明顯便宜。五年分位事實表未涵蓋，只有年度端點分位（P/S 44.1、EV/S 41.2），因此留空。","upside_short_pct":30.7,"upside_mid_pct":54.3},"trap_analysis":{"verdict":"🟡","label":"現金轉換未驗證"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"前兩大客戶 FY26 占 32%，FQ2 資料中心訂單出貨比超過 4 倍，法說上有分析師直接問 CY28 磷化銦過剩與資料中心融資。","assumption":"長約與預付在需求放緩時仍會被客戶照約履行。","consequence":"最大客戶量減半時 FY28 EPS 約少 20%，產能與債務不會同步下降，股價可能回到 250 週線 105.98 美元附近，虧損接近 50%。","ruling":"採納為下行情境，機率 30%。CEO 說看不到過剩的期限只到 CY28，且是賣方單方說法，不足以排除風險。","watch":"剩餘履約義務、合約負債、主要客戶占比與內部磷化銦稼動率。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0"],"fact_refs":["f_ma_w250"]},{"view":"論點成功但股東經濟變差","evidence":"Q1 營收年增 50%，但營業現金流 −92.7 百萬美元、資本支出 775.5 百萬美元；槓桿由 0.7 倍升到 1.1 倍，本季資本支出還要增加。","assumption":"資料中心投資約 18 個月回收（CFO 2026-08-12）。","consequence":"需求成立但現金被擴產吃掉，公司必須舉債或增資，每股價值被稀釋。","ruling":"採納。基本情境股數由 197 百萬股升到約 212 百萬股，並另設增資與槓桿的減碼門檻。","watch":"營業現金流、資本支出、長期負債與增資公告。","evidence_refs":["supply_demand_durability#2"],"fact_refs":["f_kpi3_free_cash_flow_capex"]},{"view":"價格已反映太多","evidence":"跌 42% 後仍是 FY1 20.47 倍、trailing 39.92 倍，而自由現金流為負。","assumption":"FY29 共識 19.13 美元大致可達成。","consequence":"若 FY29 EPS 只有共識七成（13.4 美元），15 倍約 201 美元，五年幾乎沒有報酬。","ruling":"反駁已過度定價：現價只要求 FY29 水準能維持。但採納另一點：已跌 42% 本身不是安全邊際。","watch":"FY2、FY3 共識修正方向與非 GAAP 毛利率。","evidence_refs":[],"fact_refs":["f_pe_current","f_fwd_pe_latest","f_week26_return_pct"]},{"view":"論點失敗","evidence":"產業層面磷化銦基板供應集中，中國出口管制帶來不確定；對美鎵鍺銻出口禁令的暫停期到 2026-11-27；10-K 提到 232 調查與實體清單風險。","assumption":"超過 5 家基板供應商足以分散風險。","consequence":"6 吋擴產若延遲，毛利率路徑與 2027 年放量都會受影響；若管制在擴產承諾後加嚴，可能認列庫存與採購義務費用。","ruling":"部分採納。CEO 稱 CY27 擴產基板已確保，但沒有揭露中國來源比例，因此保留損益層監測，不預測政策結果。","watch":"暫停期是否延長，單季毛利率下降是否達 100 個基點且公司歸因於管制或關稅。","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":[]}],"max_dd":{"lo":-60,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 277.83 → 本次 192.81（-30.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=277.83","side_b":"本次 price_at_dd=192.81","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 277.83 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 277.83 美元：Bull 價 843、Bear 價 168，五年期望值 +88.9%，基準年化 14.8%，不對稱比 5.1","side_b":"本次情境、股價仍用 277.83 美元：Bull 價 756、Bear 價 112，五年期望值 +42.1%，基準年化 6.6%，不對稱比 2.4","ruling":"先換情境、股價不動：五年期望值少 46.8 個百分點，基準年化少 8.2 個百分點。不對稱比由 5.1 變為 2.4。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 277.83 美元：五年期望值 +42.1%，基準年化 6.6%，不對稱比 2.4","side_b":"本次情境、股價 192.81 美元：五年期望值 +104.7%，基準年化 14.7%，不對稱比 5.81","ruling":"再換股價、情境不動：起點價下跌 30.6%，五年期望值多 62.6 個百分點，基準年化多 8.1 個百分點，不對稱比由 2.4 升到 5.81。合計五年期望值比前份多 15.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與進場結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 277.83 美元，估值偏便宜，結論進場。","side_b":"本次股價 192.81 美元，FY1 本益比 20.47 倍，估值仍偏便宜。","ruling":"估值結論維持，差別主要來自股價下跌 30.6%；FY1 共識三個月只變動 −0.42%。進場結論與倉位角色由本次均線狀態與情境結果決定。","evidence_level":"高","settle_metric":"FY1、FY2 共識 EPS 修正與股價相對 52 週線位置","if_then":["若股價續漲但毛利率與現金流未改善，則不追","若股價下跌但訂單與毛利率無損，則分批反買"],"evidence_refs":[]},{"axis":"價值陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份為綠色，認定資本支出暴增是超前建置。","side_b":"本次為黃色：Q1 自由現金流 −8.68 億美元，FY27→FY28 共識 EPS 成長高於營收成長 9.4 個百分點。","ruling":"下調一級。現金轉換尚未驗證，FY27 全年若續為負，第二個衰退訊號會亮燈。","evidence_level":"高","settle_metric":"FY27 全年營業現金流","if_then":["若 FY27 全年營業現金流高於 0.8 億美元，則回到綠色","若 FY27 全年營業現金流為負，則減碼至一半"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"評級、護城河方向、跑道與公司類型","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","archetype"],"side_a":"前份綜合評級 B、護城河向上、五年後跑道寬、屬品質複利成長。","side_b":"本次四項不變：磷化銦產能提前、毛利率目標上調、200 億美元長約支持方向；公司類型的信心給低。","ruling":"維持。新證據支持方向，但自由現金流與同業利潤率差距讓等級停在 B。","evidence_level":"中","settle_metric":"內部磷化銦比例、毛利率與主要客戶份額","if_then":["若 2027 年中前內部比例仍未上升，則護城河方向改為持平"],"evidence_refs":[]},{"axis":"機率、回撤與循環位置","cause":"方法變動","prior_field":["max_dd_pct","p_bull_pct","p_bear_pct","cycle_position"],"side_a":"前份 Bull 30%、Bear 30%，最大回撤 −60%，循環位置留空。","side_b":"本次 Bull 25%、Base 45%、Bear 30%，回撤區間 −60%～−45%，循環位置仍留空。","ruling":"Bull 下調 5 點，因 FY29 以後依賴 CY28 後的持續性，共識也超過內生上界。回撤改用區間表達。本次仍不按循環股處理，但把 CY28 過剩放進下行情境。","evidence_level":"中","settle_metric":"CY27 底毛利率與雷射報價","if_then":[],"evidence_refs":[]},{"axis":"加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"已達進場門檻，本欄示意持有期加碼觸發：GM連2季>41.5%或CPO/OCS單季合計營收破$300M","side_b":"Q2 FY27 毛利率 ≥41.5% 且營業現金流轉正才加碼第二批；或跌破 181 美元且訂單與毛利率無損時分批反買。","ruling":"加入現金流條件，因 Q1 自由現金流明顯惡化；OCS 未單獨揭露，舊條件的合計金額無法驗證，改看 PhotonLink 3 月季是否超過 1 億美元。","evidence_level":"高","settle_metric":"Q2 FY27 毛利率與營業現金流","if_then":["若兩項同時達成，則加碼第二批"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics","triggers"],"side_a":"前份未設清倉與減碼的量化門檻；毛利率下限為 Non-GAAP GM ≥ 39%。","side_b":"減碼：資料中心與通訊段年增連 2 季低於 30%、毛利率連 2 季低於 40%、FY27 全年營業現金流為負，或增資超過 5%。清倉：唯一致命事件發生且毛利率連 2 季年減。","ruling":"補上數字門檻。毛利率下限由 39% 提高到 40%，因 Q2 財測下緣為 40%，再低就代表擴張論點失效。","evidence_level":"高","settle_metric":"每季財報","if_then":["若任一減碼條件成立，則減碼至一半","若清倉條件成立，則清倉"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點欄位為空（null）。","side_b":"前兩大客戶之一在 CY28 前下修或延後長約承諾量（含改用自製雷射或轉單）。","ruling":"本輪補上。依敏感度排序，最大客戶全部流失的影響約占 FY28 共識 EPS 的 41%，是單一項目中最大。","evidence_level":"中","settle_metric":"主要客戶占比、剩餘履約義務與合約負債","if_then":["若確認下修或延後，則一週內減碼一半"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"長約的約束力","cause":"新證據","prior_field":null,"side_a":"CEO 2026-08-12：長約含 take-or-pay，價格幾乎都已約定。","side_b":"CEO 2026-11-04：強調高品質長期預測與預付，200 億美元只說總值；2026-08-12 被問 CY28 承諾量也沒有給數字。","ruling":"屬程度差異，採保守解讀，視為部分約束，基本情境未把 200 億美元全額算入。","evidence_level":"中","settle_metric":"10-Q 剩餘履約義務與合約負債","if_then":["若兩項連 2 季增加，則 Bear 機率下調到 25%","若客戶延後且公司修改長約條款，則減碼至一半"],"evidence_refs":[]},{"axis":"CY28 磷化銦供需","cause":"新證據","prior_field":null,"side_a":"CEO 2026-11-04：看不到 CY28 過剩，公司內部雷射全部自用，外部過剩不影響。","side_b":"分析師提到 CY28 EML 過剩的討論；公司 CY27 底前內部產能再翻倍以上，且規劃 2027 年後續擴。","ruling":"方向相反，今天沒有決勝數據，不可裁決至 2027 年底。全部自用的說法不足以免疫：外部雷射降價會縮小內部成本優勢，客戶也會壓低模組價格。因此保留 30% 下行情境，不當作風險已解除。","evidence_level":"中","settle_metric":"非 GAAP 毛利率、EML 報價與內部雷射比例","if_then":["若 2027-12 季毛利率 ≥43% 且內部比例上升，則加碼至倉位上限","若 EML 報價連 2 季下跌且毛利率連 2 季年減，則減碼一半","若股價續漲但證據未到，則不追"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#4"]},{"axis":"毛利率擴張的來源","cause":"新證據","prior_field":null,"side_a":"CFO 2026-11-04：毛利率擴張具結構性，也受益於 6 吋轉換。","side_b":"CEO 同場：內外部雷射比例一年沒變，6 吋最大的好處還在後面；本季主因是定價、投入成本與良率。","ruling":"屬程度差異。目前提升以定價為主，尚未證明是結構性；45% 目標依賴未來比例轉換與新產品。依管理層歸因歸類，分項金額未揭露。","evidence_level":"中","settle_metric":"內部雷射比例與非 GAAP 毛利率","if_then":["若 2027-06 季毛利率低於 42%，則停止加碼"],"evidence_refs":[]},{"axis":"scale-up 收入時程","cause":"新證據","prior_field":null,"side_a":"CEO 2026-08-12：CPO scale-up 收入 CY27 下半年開始，時程一貫。","side_b":"CEO 2026-11-04 問答：接近 CY27 底開始，NPO 可能到 2028 年初。","ruling":"小幅後移，不影響 FY27，但會影響 PhotonLink 放量節奏，先記錄，不調整情境。","evidence_level":"中","settle_metric":"PhotonLink 單季營收","if_then":["若 CY27 底前每季未達 2.5 億美元，則停止加碼"],"evidence_refs":[]},{"axis":"共識與實績節奏","cause":"新證據","prior_field":null,"side_a":"FY1 共識 9.42 美元，近三個月 −0.42%，最新快照無變動。","side_b":"Q1 實績加 Q2 財測中位已達 4.47 美元，下半年每季只需 2.48 美元，而管理層目標 FY27 底單季 30 億美元以上。","ruling":"共識可能偏舊，或口徑不一，基本情境 FY27 取 10.0 美元。這只影響近一年，對五年報酬的影響小於 FY29 持續性。","evidence_level":"中","settle_metric":"下一次共識快照","if_then":[],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭惡化：單一來源稱中國廠拿 2.4T 世代 60～70%，Lumentum 擬併 Marvell。","side_b":"結構轉好：CY27 訂單近滿、長約到本十年底；其他結構變數包括 232 關稅與出口管制。","ruling":"雙向拉鋸。需求與合約面轉好有公司揭露支持，競爭惡化目前多為單一來源或尚未落地的交易。","evidence_level":"中","settle_metric":"主要客戶份額與毛利率","if_then":[],"evidence_refs":["competitive_share_entrants#4"]},{"axis":"現在就賣的最強論證","cause":"新證據","prior_field":null,"side_a":"賣方論點：每季自由現金流流出近 9 億美元，資本支出還在升，缺貨與預付常見於週期後段；股價跌破 52 週線，趨勢已轉弱。","side_b":"持有論點：CY27 訂單近滿，毛利率目標上調，現價只要求 FY29 共識維持。","ruling":"不賣，但不一次買足。分批以現金流與毛利率的下一個數據點為條件，下行 30% 機率已反映在情境。","evidence_level":"中","settle_metric":"Q2 FY27 營業現金流","if_then":["若 Q2、Q3 營業現金流皆為負且資本支出續增，則減碼至一半"],"evidence_refs":["supply_demand_durability#2"]}],"triggers":[{"n":1,"text":"第二批進場：Q2 FY27 財報確認毛利率與現金流。","type":"估值rearm","maps_to":"H2／H3","metric":"非 GAAP 毛利率、營業現金流","threshold":"毛利率 ≥41.5% 且營業現金流 >0","action":"加碼第二批至目標倉位 2/3","source_freq":"公司季報，每季","date":"2027-02"},{"n":2,"text":"第三批進場：PhotonLink 開始放量。","type":"加碼","maps_to":"H1／H2","metric":"PhotonLink 單季營收與非 GAAP 毛利率","threshold":"3 月季營收 >1 億美元且毛利率 ≥42%","action":"加碼至倉位上限","source_freq":"公司季報，每季","date":"2027-05"},{"n":3,"text":"驗證 FY27 底單季營收目標。","type":"假設驗證","maps_to":"H1","metric":"FY27 Q4 營收","threshold":"≥30 億美元","action":"未達則停止加碼","source_freq":"公司季報，每季","date":"2027-08"},{"n":4,"text":"驗證資本支出是否開始回收。","type":"假設驗證","maps_to":"H3","metric":"FY27 全年營業現金流","threshold":">0.8 億美元","action":"未達則減碼至一半","source_freq":"10-K，每年","date":"2027-08","evidence_refs":["supply_demand_durability#2"]},{"n":5,"text":"中國對美鎵鍺銻出口禁令暫停期到期。","type":"風險","maps_to":"R5","metric":"暫停期是否延長、下一季毛利率","threshold":"到期未延長，且下一季毛利率季減 ≥100 個基點","action":"減碼三分之一","source_freq":"官方公告與公司季報","date":"2026-11-27","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2"]},{"n":6,"text":"關稅與出口管制是否吸收失敗。","type":"風險","maps_to":"R5","metric":"非 GAAP 毛利率","threshold":"單季下降 ≥100 個基點且公司歸因於關稅或出口管制","action":"停止加碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":7,"text":"前兩大客戶之一下修或延後長約承諾量。","type":"Single Thing","maps_to":"R1","metric":"主要客戶占比、剩餘履約義務與合約負債","threshold":"確認下修或延後，或最大客戶占比由 20% 降到 10% 以下","action":"一週內減碼一半","source_freq":"10-K、10-Q 與法說","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":8,"text":"融資壓力超過可接受範圍。","type":"減碼","maps_to":"R3","metric":"增資比例與槓桿倍數","threshold":"股權增資超過 5%，或槓桿超過 2 倍","action":"減碼至一半","source_freq":"8-K 與公司季報","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":9,"text":"客戶承諾與毛利率同時失守。","type":"清倉","maps_to":"H1／H2","metric":"長約變動與非 GAAP 毛利率","threshold":"唯一致命事件已發生，且毛利率連 2 季年減","action":"清倉","source_freq":"公司季報與法說","date":null},{"n":10,"text":"下一次財報後重跑完整研究。","type":"複審日期","maps_to":"H1／H2／H3","metric":"Q2 FY27 財報","threshold":"財報公布","action":"更新情境與倉位條件","source_freq":"每季","date":"2027-02"}],"kill_metrics":[{"metric":"資料中心與通訊段營收年增率","bear_threshold":"連 2 季低於 30%","window":"每季","source":"公司財報與法說","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"連 2 季低於 40%","window":"每季","source":"公司財報","last_status":"ok"},{"metric":"FY27 全年營業現金流","bear_threshold":"全年為負","window":"至 2027-08 年報","source":"10-Q、10-K 現金流量表","last_status":"warning"},{"metric":"最大客戶占營收比與長約承諾","bear_threshold":"承諾下修或延後，或占比由 20% 降到 10% 以下","window":"每季至 CY28","source":"10-K、10-Q、法說","last_status":"unknown"},{"metric":"股權增資與槓桿倍數","bear_threshold":"增資超過 5%，或槓桿超過 2 倍","window":"每季","source":"8-K 與公司財報","last_status":"ok"}],"evidence_dismissed":[{"ref":"end_markets#1","reason":"這筆 10% 下滑來自航太國防與慕尼黑業務處分，屬合併範圍改變；Q1 FY27 pro forma 季比與年比持平，不代表同口徑需求下滑。"},{"ref":"major_events#2","reason":"這是原告律所徵求當事人的公告，查無案號、求償金額或法院程序，無法作為可量化的風險證據。"},{"ref":"lawsuit_class_action#0","reason":"來源為律所調查公告，搜尋未找到已提起的集體訴訟案號，也沒有受影響金額。"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":"總資產 5% 以內；槓桿超過 2 倍或毛利率低於 40% 時降到 3% 以內。","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 26 週 −42% 定價 CY28 過剩與融資風險，但 CY27 訂單近滿、長約多含預付，現價只要求 FY29 共識大致兌現且之後不再快速成長。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟢', moat_trend='↑', week26=-42.49, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"requires_critic":[],"rearm_trigger":"Q2 FY27 毛利率 ≥41.5% 且營業現金流轉正才加碼第二批；或跌破 181 美元且訂單與毛利率無損時分批反買。","exec_line":"首批三分之一可在 192.81 美元附近建立；第二批等 2027-02 財報確認毛利率與現金流；第三批等 PhotonLink 3 月季超過 1 億美元。證據未到前，站回 271 美元也不追價。"},"reasoning":{"industry":"Q1 FY27 營收 23.7 億美元，季增 16%、年增 50%（扣除已處分業務為年增 56%）。資料中心與通訊段占 82%，年增 79%，其中資料中心年增 85%、通訊年增 84%；工業段持平。非 GAAP 毛利率 40.6%、營業利益率 23.2%，GAAP 營業利益率 15.9%，兩者差 7.3 個百分點。Q2 財測營收 25.5～27.5 億美元、EPS 2.28～2.48 美元。對照 2026-08-12 CFO 財測，Q1 營收落在 22～24 億美元區間上半，EPS 2.09 美元高於 2.05 美元上緣。單點依賴在客戶：FY26 最大客戶占 20%（前兩年各 10%），第二大占 12%。另有非獨立研究頁稱某客戶占該段 25～35%，未核實。分部毛利率事實表未涵蓋。","moat":"優勢在雷射端：內部磷化銦產能較原計畫提前一季翻倍，CY27 底前再翻倍以上；400 毫瓦 CW 雷射 CEO 稱只看到一家競爭者；新簽 200 億美元、五年的 PhotonLink 長約。弱點在利潤率：TTM 毛利率 38.16%，低於 Lumentum 的 45.91%；營業利益率 14.11% 對 23.35%；自由現金流利潤率 −23.28% 對 9.52%。同業 ROIC 序列事實表未涵蓋，無法證明對最強同業的差距在收斂，所以綜合評分不到 8。向上判斷的反例有三：內部雷射比例一年未變、毛利率提升相當部分來自缺貨期定價、2.4T 世代有單一來源稱中國廠拿 60～70%。當期 ROIC 因投入資本未涵蓋無法計算，增量報酬用 FY26 損益與自由現金流代理，推導見公式欄。","growth":"成長以量為主，價與產品組合為輔，沒有併購或回購。共識 EPS FY27 9.42 美元、FY29 19.13 美元，兩年年化約 42.5%；共識營收 FY27 111.6 億美元、FY28 155.0 億美元，年增 38.9%。內生上界 40.7%，缺口約 1.8 個百分點，可歸因於毛利率與營業費用槓桿。基本情境 EPS 年化約 19%（9.42→22.5 美元），在上界之內，但高於只用自有現金時的約 17%，代表仍需外部資金或客戶預付。CY27 前的跑道有訂單支撐，五年後的判斷依賴管理層的市場規模估計。滲透率推算：78 億美元以年增約 40% 成長，到 270 億美元約需 3.7 年。","governance":"FY26 自由現金流 −10.3 億美元、淨利 8.05 億美元，轉換率為負。Q1 FY27 營業現金流 −92.7 百萬美元，資本支出 775.5 百萬美元，占營收 32.7%，CFO 說本季還會再增加。現金由 25.9 億美元降到 23.4 億美元，只少 2.5 億美元，差額約 6.2 億美元的來源事實表未涵蓋；槓桿由 0.7 倍升到 1.1 倍。FY26 償債 5.13 億美元，股利與回購沒有紀錄。CFO 稱資料中心投資約 18 個月回收，尚無現金流驗證。事實表現金 17.5 億美元與法說 23.4 億美元不同，淨負債可能高估約 5.9 億美元，約占 EV 1.4%，不改變結論。","valuation":"現價 192.81 美元，FY1 本益比 20.47 倍，FY2 13.80 倍。以 10% 要求報酬、15 倍終端本益比反推，FY31 EPS 要約 20.7 美元，只比 FY29 共識 19.13 美元高 8%。若營收停在 FY28 共識 155 億美元、營業利益率回到 18%，未計利息的 EPS 約 11.5 美元，16 倍約 184 美元，接近現價，代表價格已計入部分高峰疑慮。基本情境 FY29 EPS 17.5 美元，低於共識 8.5%。12 個月以 FY28 EPS 14.0 美元×18 倍得 252 美元，上行 30.7%；24 個月以 FY29 EPS 17.5 美元×17 倍得 297.5 美元，上行 54.3%。FY1 共識 9.42 美元可能偏舊：Q1 實績 2.09 美元加 Q2 財測中位 2.38 美元已達 4.47 美元，下半年每季只需 2.48 美元，約等於 Q2 財測上緣，而管理層指向 FY27 底單季 30 億美元以上。FY28 共識以 19% 稅率與 197 百萬股反推，稅前利益率約 22%，低於 Q1 非 GAAP 營業利益率 23.2%，可能還沒計入毛利率擴張，也可能混用口徑。賣方目標價僅見德銀 400 美元（2026-09-01），均值與全距事實表未涵蓋，不作依據。","premortem":"最強的空方數字是 Q1 自由現金流 −8.68 億美元與前兩大客戶占 32%。壓力測試 5 項過 3 項：最大客戶量減半仍獲利、毛利率退回 36% 仍獲利、出口管制加嚴但未斷料仍可經營，這三項通過；AI 資本支出下滑 30% 時 FY28 EPS 約少六成，不通過；現金 23.4 億美元只夠支應約 2.7 季目前的流出速度，循環額度事實表未涵蓋，不通過。FY31 基本情境敏感度：營業利益率每差 1 個百分點，EPS 約差 0.84 美元，目標價約差 14 美元；股數多 5%，目標價約少 18 美元；終端本益比每差 2 倍，目標價約差 45 美元。歷史最大回撤與訴訟金額事實表未涵蓋。2026-08-12 法說管理層沒有正面回答增量毛利率、毛利率改善拆分、30 億美元季度的營收組成、CY28 承諾量，毛利率目標時間表則到 11-04 才補上。"},"plain":{"six":{"how_it_makes_money":"賺雲端與 AI 客戶擴建光互連的錢，利潤卡在磷化銦雷射這一節：有自家雷射產能的廠商才拿得到單、守得住毛利。","moat":"護城河仍在擴大，來源是磷化銦垂直整合與多年長約；但擴大幅度有多少來自缺貨還分不開，等級只給 B。","growth":"五年後仍有跑道：公司年化營收約占管理層 2030 年市場估計的 9%，整合光學已有長約；但以目前速度約四年就到 30% 滲透率，倍數不宜給高。","capital":"資本幾乎全押擴產，最新一季自由現金流 −8.68 億美元；稀釋可控，併購與回購沒有可評紀錄，配置能力要等現金回收才算數。","valuation":"現價只要求 FY29 共識大致兌現、之後不再快速成長。我相信到 FY28 的數字，FY29 以後打折看待。","how_wrong":"最可能看錯 CY28 以後的定價與客戶承諾：缺貨期的條件不會自動延續。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 26 週 −42% 定價 CY28 過剩與融資風險，但 CY27 訂單近滿、長約多含預付，現價只要求 FY29 共識大致兌現且之後不再快速成長。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"進場","prior_role":"衛星","wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟢","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":192.81,"week26_return_pct":-42.49,"consensus_rev_3m_pct":-0.42,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY1 與 FY2 有訂單與長約支撐，當期分母不是爭點；爭點在 FY29 以後能否持續，已放進下行情境。trailing 分母含處分利得（FY26 慕尼黑處分利得 1.24 億美元），因此改用前瞻錨定。"},"catalysts":[{"date":"2026-11-27","date_precision":null,"type":"regulatory","event":"中國對美鎵鍺銻出口禁令暫停期到期","impact":"中","watch":"是否延長，以及下一季毛利率"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q2 FY27 財報","impact":"高","watch":"毛利率、營業現金流與資本支出"},{"date":"2027-05","date_precision":"month","type":"product","event":"Q3 FY27 財報確認 PhotonLink 3 月季營收","impact":"高","watch":"是否超過 1 億美元"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"蘇黎世 6 吋磷化銦產線開始生產","impact":"中","watch":"是否在 CY27 上半年如期投產"},{"date":"2027-08","date_precision":"month","type":"guidance","event":"FY27 Q4 財報與全年現金流","impact":"高","watch":"單季營收是否達 30 億美元，全年營業現金流是否轉正"},{"date":"2027-12","date_precision":"month","type":"capacity","event":"內部磷化銦產能再翻倍以上的目標期限","impact":"高","watch":"內部雷射比例與毛利率"}],"_projected_from":"v19"}
```
