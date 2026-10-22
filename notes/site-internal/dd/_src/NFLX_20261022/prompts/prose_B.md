你是 stock-analyst v20 的**散文層（prose）agent**，標的 NFLX（2026-10-22）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：NFLX　日期：2026-10-22　archetype：None　前份裁決：2026-07-17　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1752B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（739B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1134B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1351B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（988B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（417B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（859B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1974B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3905B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1942B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1752           3674-5248      5 條（2–6 內）  
s3                  8000         739           5083-7261      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3473          8069-11527      5 條（2–6 內）  
s6                 11000         417          7408-10583      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         859           1849-2641      5 條（2–6 內）  
s10                 5000        1974           2118-3026      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1942           2000-3058      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4890B；至少需散文≈40.11KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−50
−48%
−35
−35%
−30.24
−30.2%
−25%
−20%
−4.3%
−4%
−1
0
0.2%
0.5%
0.6%
0.67
0.75
0.79
0.8
0.83
0.86
0.9
01
1%
1.0
1
1.3%
1.4
1.9
2%
2
02
2.3
2.5%
2.5
2.53
3%
3.0%
03
3
3.23
3.4
3.45
3.5
3.59
3.6%
3.62
3.7%
3.75
3.8%
3.80
3.8
3.95
4
4%
4.2%
4.25
4.3%
4.56
4.85
5
5%
5.15
5.2
5.3%
5.43
5.45
5.75
5.8%
5.85
6
6%
6.3%
6.5
6.6
6.75
7
7%
07
7.1
7.8
7.9%
8
8%
8.1
8.3%
9
9%
09
10
10%
10.2%
10.4
10.8%
11
11%
11.2%
11.4
12%
12
12.5%
12.6%
12.8%
13
13%
13.5%
13.8%
14%
14
15
15.2
16
16.0
16.03
17
17.1
17.12
17.4%
17.5%
17.5
17.6%
17.8%
17.9
18.1
18.12
18.8
19%
19.2
20
20%
21
21.7%
22%
22
22.4
22.7
23
24%
25
25%
26%
26
27
28%
28
28.8
29.5%
29.7%
30%
30
30.2%
31
31.5%
32%
32.5%
32.6
32.7%
33%
33.1%
33.6
34%
34.6%
35
36%
37%
38%
38.1%
39.4%
40%
40
41.07
41.1
42
43.4
45
45.1
47
48
48.5%
48.75
49
49.1%
50
52.8
52.9
53%
55
56.28
56.3
57.6%
60%
64.7%
65.04
67.97
69.1
69.2
70
72.8%
77.5
80%
80
87.1
93.66
94.6
95%
99.5
100
100%
103
109.8
120
127%
128.7
134
134.4
134.42
150%
151
179.4
180
180.4
200
232
451.8
511
827
2022
2024
2025
2026
2027
2028
20261022
1,700
1,760
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
{"meta":{"ticker":"NFLX","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"Netflix, Inc."},"oneliner":"美國片單與廣告進度落後，注意力份額小幅流失；但流失率改善、調價順利、營益率續升。FY2 本益比約 17 倍沒有計入太多成長，續抱試單，等 2027 年 1 月全年指引再決定是否加碼。","thesis":{"H":[{"id":"H1","text":"會員、單價、廣告三個槓桿在觀看時數只有低個位數成長時，仍撐住雙位數營收成長","2y":"FY27 營收年增 ≥10%（共識約 +10.8%）","5y":"FY26–FY31 營收年複合 ≥9%","10y":null,"threshold":"Q4'26 營收 ≥134 億美元（指引 134.42 億美元，+12%）；UCAN 季營收年增 ≥+10%（Q3'26 為 11%）","source":"Netflix 季度股東信區域營收；2027 年 1 月全年指引","drift_rule":"匯率中性營收年增連 2 季低於 +10% 為削弱；連 3 季低於 +9% 為反轉"},{"id":"H2","text":"營益率每年擴張，FY28 達 34% 以上，體育版權與重組成本不打斷這條路","2y":"FY27 營益率指引 ≥33%（FY26 指引 31.5%）","5y":"FY31 營益率 ≥36%","10y":null,"threshold":"FY27 營益率指引 ≥33%；內容費用成長率低於營收成長率（2026 年內容費用約 +10%，營收 +13%）","source":"Netflix 股東信與年度指引；Ted 2026-07-16 內容費用預估","drift_rule":"FY27 指引低於 32.5% 為削弱；FY27 實際營益率低於 FY26 為反轉"},{"id":"H3","text":"廣告成為第二個成長引擎，廣告方案與標準方案的每會員營收差距持續縮小","2y":"2027 年廣告營收成長 ≥40%，15 國新廣告方案如期上線","5y":"FY31 廣告占營收 ≥12%","10y":null,"threshold":"管理層每季確認每會員營收差距在縮小；2027 年廣告成長率 ≥40%（2026 年逾 80%）","source":"Netflix 法說會與股東信；Greg 2026-10-20 說明","drift_rule":"連 2 季不再提差距縮小，或廣告成長低於 40%，為削弱；新國家上線延後超過 2 季為反轉"}],"R":[{"id":"R1","text":"注意力份額流向 YouTube 與短影音：Nielsen 美國電視觀看份額 8.3%→7.9%，YouTube 12.8%→13.5%","h_ref":"H1","clock":"🔥","threshold":"Nielsen 月份額連 6 個月低於 8% 且 UCAN 營收年增低於 +9%：護城河趨勢改判下降，減碼至 0.5%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#0"]},{"id":"R2","text":"成本通膨與美國片單執行：FY26 營益率指引 31.5% 低於共識 32.7%；內容長更換，Q4 含約 120 個基點重組成本","h_ref":"H2","clock":"🔥","threshold":"內容費用成長率連 2 年高於營收成長率，或單一體育合約超過 15 億美元／屆，重算情境；FY27 營益率指引低於 32.5% 則減碼","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#4"]},{"id":"R3","text":"政策風險：電影進口 100% 關稅（Citi 估最壞 EPS −20%）、DOJ 調查 Netflix 對創作者的議價力、反壟斷倡議","h_ref":"H2","clock":"🐢","threshold":"關稅正式生效且適用串流原創，以 EPS −20% 重算；DOJ 或 FTC 對 Netflix 本身立案，減碼至 0.5%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","regulatory_antitrust#1","regulatory_antitrust#2"]},{"id":"R4","text":"短期財測落差：Q3 指引曾低於市場，廣告進度落後年初目標，全年指引落在區間下緣","h_ref":"H3","clock":"⚡","threshold":"Q4'26 營收低於指引 134.42 億美元，或 FY27 營收指引低於 +10%，減碼","evidence_refs":["capital_markets_pricing#0"]}],"single_thing":{"description":"2027 年 1 月 Q4 財報給出的 FY27 營收成長指引低於 10%","why_fatal":"雙位數成長是市場用 17 倍（成熟複利）還是 13 倍（成熟媒體）定價的分界；跌破後基本情境終值少約 24%，三槓桿論點也同時失效","if_happens":"減碼至 0.5%；營益率指引同時低於 32.5% 則清倉","how_monitor":"2027-01 股東信全年指引；在那之前看 Q4 營收是否達 134.42 億美元","probability":"約 25%（12 個月內）。共識 FY27 營收 +10.8%，只比門檻高 0.8pp；CFO 2026-10-20 重申以維持雙位數成長為目標"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":17.12,"peg_fy2":0.79,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":2.53,"FY2026E":3.59,"FY2027E":3.8,"FY2028E":4.56},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（拆股後口徑），共識取自 Koyfin 2026-10-21 快照，分析師家數事實表未涵蓋；FY2026E 可能含 WBD 終止費一次性收益（推論未證）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"營收雙位數成長、營益率逐年擴張、FCF 利潤率約兩成的輕資本訂閱模式"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：Omdia 2025 年全球線上影音營收 +13.5% 至 1,760 億美元，付費電視 −4% 至 1,700 億美元，收視遷移單向進行；但 2026 年訂閱數成長預期降到個位數，擴張進入後段","bargaining":{"up":"內容供應商同時是競爭者，但 Disney、Globo 等新授權案顯示 Netflix 是首選買方，且不依賴單一供應商；體育版權是議價最弱的環節","down":"消費者分散、無集中度；2026 年各市場調價反應與過往一致","geo":"美國電影進口關稅、EU 網路使用費是政策變數，法源與時點皆未定"},"profit_pool_dir":"由線性電視往串流遷移，Netflix 是淨流入方","tam_table":[{"item":"全球線上影音營收 2025","value":"1,760 億美元，年增 13.5%（Omdia）"},{"item":"全球付費電視營收 2025","value":"1,700 億美元，年減 4%（不含廣告）"},{"item":"Netflix 2025 營收對線上影音營收","value":"約 26%（451.8÷1,760，口徑不同，只看量級）"},{"item":"全球線上影音訂閱數 2025 年底","value":"22.4 億，年增 17.6%，預期 2026 年降到個位數"},{"item":"可觸及家戶","value":"約 8 億戶（CFO 2026-07-16）；Netflix 會員數與滲透率事實表未涵蓋"},{"item":"營業利益池 5 年前→現","value":"事實表未涵蓋；方向為串流淨流入"}]},"moat":{"mechanism":"規模分攤：全球最大付費家戶基數攤提原創與在地內容成本，加上推薦系統，使每小時觀看單價最低、調價空間最大","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價面穩定：2026-03 美國全方案調價後，Q3 全球與美國流失率年改善且優於預測（Greg 2026-10-20）。執行面也判穩定但偏弱：財務面營益率續升，內容面則是美國片單不夠好、更換內容長、廣告落後。Nielsen 份額 8.3%→7.9% 是最接近轉向下降的證據，門槓見風險一。","peer_na_reason":"同業表為廣告與注意力平台，不是串流同業，且沒有 ROIC 數字，報酬價差無法計算","threats":[{"level":"🔴","text":"YouTube 與短影音搶走電視大螢幕的觀看時間，攻擊者內容成本接近零、背後資本量級遠大於 Netflix","p":35,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#0"]},{"level":"🟡","text":"生成式 AI 降低內容製作門檻，新進者與使用者生成內容平台增加供給；Netflix 自身也在用 AI 降低成本","p":20,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"反壟斷與政策：DOJ 曾調查 Netflix 對獨立製片的議價力，倡議團體發起反壟斷運動，美國電影關稅未定案","p":15,"evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","reg_tariff_export#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率待補（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多在同一家戶，三個環節都成立。Q3'26 全球與美國流失率年改善且優於預測，2026 年各市場調價的會員反應與過往一致（Greg 2026-10-20）。娛樂屬於想要而非需要，但每小時單價是美國 SVOD 最低，取消的動機低"},{"item":"決策層級","level":"🟡","text":"替代性要在家戶『今晚看什麼』這一層衡量：月訂閱隨時可取消、轉換成本低，對手是所有螢幕時間而不只串流。兩個代理變數方向相反：調價後流失率在改善，Nielsen 觀看份額由 8.3% 降到 7.9%"},{"item":"價值鏈分配","level":"🟢","text":"毛利率 2022→2025 年由 39.4% 升到 48.5%，價值往 Netflix 移動。Disney、Globo 授權案顯示 Netflix 是首選買方，且不依賴單一供應商（Ted 2026-10-20）。最弱環節是體育版權，直播約占 2026 年內容預算 5%（Greg 2026-07-16）"},{"item":"社會容忍度","level":"🟡","text":"反壟斷關注在升溫：DOJ 審 WBD 案時調查 Netflix 對獨立製片的議價力，倡議團體 2026-07 發起『Netflix is a Monopoly』運動；EU 網路使用費與美國電影關稅屬政策風險。目前價格仍低於經濟上限，還沒碰到社會容忍的天花板"}],"roiic":"約 127%（代理值）","reinvest_rate":"約 13.8%（代理值）","endo_ceiling":17.5,"formula_note":"代理計算：以淨利代 NOPAT、以淨利減 FCF 代再投資。2024 年再投資 87.1−69.2＝17.9 億美元；2025 年淨利增量 109.8−87.1＝22.7 億美元，增量報酬約 127%。2025 年再投資率（109.8−94.6）÷109.8＝13.8%，內生成長上界約 17.5%。限制：內容支出以攤銷計入損益，FCF 口徑會低估真實再投資；增量報酬多來自對既有用戶調價，應視為上限而非常態"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","NFLX":49.12,"META":81.75,"GOOGL":60.9,"PINS":79.47,"ROKU":45.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","NFLX":29.68,"META":38.08,"GOOGL":33.11,"PINS":6.27,"ROKU":5.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","NFLX":23.06,"META":17.95,"GOOGL":11.95,"PINS":28.11,"ROKU":13.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","NFLX":7.67,"META":31.38,"GOOGL":15.47,"PINS":34.42,"ROKU":14.13,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"META","gm":81.75,"om":38.08,"fcf_margin":17.95,"rd_intensity":31.38,"strategy_note":"爭的是手機零碎時間與廣告預算，不是電視大螢幕；利潤率較高但模式不同，不宜當估值錨","period":"TTM ending 2026-06-30（4季加總）"},{"name":"GOOGL","gm":60.9,"om":33.11,"fcf_margin":11.95,"rd_intensity":15.47,"strategy_note":"YouTube 是最直接的攻擊者：美國電視觀看份額 13.5% 且仍在升，內容成本由創作者承擔","period":"TTM ending 2026-06-30（4季加總）"},{"name":"PINS","gm":79.47,"om":6.27,"fcf_margin":28.11,"rd_intensity":34.42,"strategy_note":"只在廣告預算上邊際競爭，營益率約 6%，威脅低","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ROKU","gm":45.5,"om":5.25,"fcf_margin":13.63,"rd_intensity":14.13,"strategy_note":"通路與廣告夥伴兼對手；Roku Channel 份額 2.5%→3.0%，營益率約 5%","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"價（成熟市場調價）＋量（新興市場會員）＋廣告；無併購；淨回購約每年 1.3%","runway_years":"事實表未涵蓋（缺會員數與滲透率）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：增量報酬約 127%×再投資率 13.8%≈17.5%，代理值且偏上限","segments":[{"item":"UCAN","value":"Q3'26 營收 56.28 億美元，年增 11%（Q2'26 為 10%）"},{"item":"EMEA","value":"41.07 億美元，年增 11%，匯率中性 9%"},{"item":"LATAM","value":"16.03 億美元，成長率未取得"},{"item":"APAC","value":"事實表未涵蓋；印度 Q3 營收年增近 20%（Greg 2026-10-20）"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"TTM 毛利率 49.1% 高於 2025 年 48.5%"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"Nielsen 美國電視觀看份額 8.3%→7.9%"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"2026-03 調價後流失率年改善"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"共識 EPS 三年年複合 21.7%，營收約 12%，差距來自營益率擴張與回購"},{"signal":"FCF÷淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 0.79、2025 年 0.86"},{"signal":"SBC 占營收逾 5% 且上升","lit":false,"evidence":"SBC 約營收 1%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"線上影音營收 2025 年 +13.5%"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"自身本益比在 4 個年度端點中最低，但產業倍數事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"evidence":"內容維持性支出拆分事實表未涵蓋"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"2026 年內容支出約 200 億美元，較 2025 年 180 億增加"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：WBD 案已於 2026-02-27 終止；現金去向四分與回購均價事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年沒有完成的重大併購；WBD 案終止並收 28 億美元終止費，沒有已實現的增量報酬可算","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購期間股價與 10 年期殖利率事實表未涵蓋；以現價 FY2 本益比 17.1 倍換算盈餘收益率約 5.8%，10 年期殖利率要 ≤3.8% 才過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占 Q3'26 營業利益 3%；2022→2025 年稀釋股數約 45.1 億→43.4 億，每年淨縮減約 1.3%","grade":"過"}]},"valuation":{"basis":"FY2 本益比（FY2027E EPS 3.80）為主尺；FY1 分母可能含一次性終止費，只作對照","tier":"大型成熟複利","peers":{"expanded":false,"reason":"事實表同業表只有利潤率，沒有同業本益比；終端倍數的同業對照是資料缺口，改用 Netflix 自身 4 個年度端點與 13–23 倍的框架區間定錨"},"fwd_pe":18.12,"peg":0.83,"percentile_5y":0.0,"val_light":"🟢","val_light_derivation":"FY2 本益比 17.1 倍（65.04÷3.80）。共識 FY25A→FY28E EPS 年複合 21.7%，PEG 約 0.8；trailing 本益比 18.8 倍是 4 個年度端點最低（以年度端點代替五年分位），P/S 分位 17.4%。改用基本情境 EPS 年複合 12.6%，PEG 約 1.4，仍在合理區。結論：便宜偏合理","upside_short_pct":19.2,"upside_mid_pct":52.9},"trap_analysis":{"verdict":"🟡","label":"注意力份額下滑與利潤擴張並存，要看 2027 年全年指引"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"YouTube 美國電視觀看份額 12.8%→13.5%，Netflix 8.3%→7.9%；生成式 AI 降低內容製作門檻，新進者增加","assumption":"觀看份額流失最後會傳導到定價力與流失率","consequence":"營收成長 2028 年後降到 5–7%，本益比降到 13 倍，五年後股價約 45–50 美元","ruling":"部分採納：空頭機率給 30%。這條故事與 Single Thing 部分重疊，FY27 指引跌破 10% 是它最早出現的形式，Single Thing 保留不動","watch":"Nielsen 月份額、UCAN 營收年增率","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"],"fact_refs":["f_week26_return_pct"]},{"view":"論點成功但股東經濟變差","evidence":"2025-12 管理層簽下企業價值 827 億美元的 WBD 案並開 50 億美元信貸，與 Ted 2026-07-16『主要是建造者不是買家』的說法有落差。年初 EPS 預估因內容與廣告成本下修 3.7%；FY26 營益率指引 31.5% 低於共識 32.7%","assumption":"營收繼續成長，但被體育版權、內容成本或大型併購吃掉","consequence":"EPS 年增落到 8% 以下，增量報酬下降","ruling":"採納為監測項：WBD 案證明管理層願意做超大併購；再出現超過市值 10% 的併購就重跑判斷","watch":"併購公告、FY27 營益率指引","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#4"],"fact_refs":["f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY1 本益比 18.1 倍看似便宜，但 FY26 EPS 可能含 28 億美元終止費，剔除後約 21–22 倍；Citi 估電影關稅最壞情境 EPS −20%","assumption":"市場用了被一次性收益墊高的分母，真實估值不便宜","consequence":"若以乾淨 FY26 EPS 定價，下行空間比表面大","ruling":"反駁：以不含一次性收益的 FY2 計是 17.1 倍，仍在 4 個年度端點最低。電影關稅法源不明、白宮未定案，列監測，不放入基本情境","watch":"2027-01 股東信是否揭露終止費入帳科目；關稅正式公告","evidence_refs":["reg_tariff_export#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 67.97 → 本次 65.04（-4.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=67.97","side_b":"本次 price_at_dd=65.04","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 67.97 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 67.97 美元：Bull 價 180.4、Bear 價 52.8，五年期望值 +72.8%，基準年化 12.5%，不對稱比 6.6","side_b":"本次情境、股價仍用 67.97 美元：Bull 價 179.4、Bear 價 48.75，五年期望值 +57.6%，基準年化 10.2%，不對稱比 4.25","ruling":"先換情境、股價不動：五年期望值少 15.2 個百分點，基準年化少 2.3 個百分點。不對稱比由 6.6 變為 4.25。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 67.97 美元：五年期望值 +57.6%，基準年化 10.2%，不對稱比 4.25","side_b":"本次情境、股價 65.04 美元：五年期望值 +64.7%，基準年化 11.2%，不對稱比 5.15","ruling":"再換股價、情境不動：起點價下跌 4.3%，五年期望值多 7.1 個百分點，基準年化多 1.0 個百分點，不對稱比由 4.25 升到 5.15。合計五年期望值比前份少 8.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"注意力份額對定價力","cause":null,"prior_field":null,"side_a":"觀看份額在下滑：Nielsen 8.3%→7.9%，YouTube、Prime Video 都在升；管理層自承美國片單不夠好","side_b":"定價力完好：Q3 全球與美國流失率年改善且優於預測，2026 年調價反應與過往一致，UCAN 營收年增 11%","ruling":"不可調和，方向相反。選 B 側。依據是流失率與營收是付費行為的直接證據，份額是落後於定價力的領先指標，目前還沒傳導到付費","evidence_level":"中","settle_metric":"Nielsen 月份額與 UCAN 營收年增率","if_then":["若 Nielsen 份額連 6 個月低於 8% 且 UCAN 營收年增低於 +9%，則護城河趨勢改判下降並減碼至 0.5%","若 2027-01 指引營收 ≥+10% 且營益率 ≥33%，則加碼至 3%","反向：若份額回升到 8.3% 以上，撤銷份額警示"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"美國片單弱、內容長更換、裁員、廣告落後、全年指引落到區間下緣；FY26 EPS 可能含終止費，乾淨本益比約 21–22 倍","side_b":"FY2 本益比 17.1 倍，共識 EPS 三個月未下修，流失率改善，跌幅全來自倍數","ruling":"不賣，維持試單，2027-01 指引前不加碼。賣出論證全部是執行與情緒面的證據，沒有一條出現在盈餘預估或流失率上","evidence_level":"中","settle_metric":"FY27 營收與營益率指引","if_then":["若 FY27 營收指引低於 +10%，減碼至 0.5%；營益率指引同時低於 32.5%，清倉","若股價跌至 55 美元以下且 FY27 共識 EPS 未下修，分批加至 2%"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"管理層財測對照","cause":"新證據","prior_field":null,"side_a":"2026-07-16 CFO Spencer Neumann：全年營收成長 13% 至 14%；Greg 當時稱廣告為積極目標","side_b":"2026-10-20 股東信：全年營收點估 511 億美元，+13%，比前次區間中點低 0.2%；Greg 承認廣告落後年初目標，但今年仍成長逾 80%","ruling":"落在區間下緣但沒有失守，視為三槓桿論點輕度削弱，不改論點","evidence_level":"高","settle_metric":"Q4'26 營收對指引 134.42 億美元","if_then":["若 Q4'26 營收低於指引，H1 記一次削弱"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭惡化：YouTube、Prime Video、Peacock 的份額都在升，Netflix 在降","side_b":"結構轉好：線上影音營收 +13.5%、付費電視 −4%，工作室整併後供應方更需要 Netflix 的通路；其他結構變數包括反壟斷倡議與電影關稅","ruling":"雙向拉鋸：注意力競爭惡化，但收視遷移與內容授權結構轉好，兩股力量目前相抵","evidence_level":"中","settle_metric":"Nielsen 份額對比 Netflix 營收成長率","if_then":["若份額下滑同時營收成長跌破 10%，改判競爭惡化中"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"axis":"前份基本面結論漂移","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合評等 B、估值綠、陷阱黃、護城河趨勢持平、五年後跑道黃、品質複利成長、非循環股、裁決進場、角色衛星","side_b":"本次：基本面判斷全部維持；裁決與角色由程式依本次輸入重算","ruling":"Q3 新證據正負相抵。正面：UCAN 年增 11%、流失率改善、共識 EPS 未下修。負面：廣告落後、全年指引落在區間下緣、美國片單弱與內容長更換。股價較前份 −4.3%，估值更便宜，但不改結論","evidence_level":"中","settle_metric":"2027-01 全年指引","if_then":["若 FY27 營收指引低於 +10%，護城河趨勢與跑道各降一檔重評"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"情境機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭機率 25%、空頭機率 28%、最大回撤 −48%","side_b":"本次：多頭機率 22%、空頭機率 30%、最大回撤區間 −35% 至 −50%","ruling":"共識三年 EPS 年複合 21.7% 超過內生上界 17.5%，依規則空頭機率至少 30%；最大回撤改填區間，極端端點與前份相近","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1%·帽 3%·加碼凍結至 Q3'26 財報（2026-10）；解凍條件＝UCAN YoY ≥+11%","side_b":"2027-01 指引 FY27 營收 ≥+10% 且營益率 ≥33% 才加碼至 3%；未達則維持 1% 試單、不追","ruling":"前份的加碼解凍條件已在 Q3'26 達成（UCAN 年增 11%），這條觸發器已發火。但同一季出現廣告落後與指引落區間下緣，所以不照舊條件加碼，改綁 2027-01 的全年指引","evidence_level":"高","settle_metric":"FY27 營收與營益率指引","if_then":["若指引達標則加碼至 3%","若指引未達則維持 1% 試單"],"evidence_refs":[]},{"axis":"Single Thing 變更","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設 Single Thing","side_b":"2027 年 1 月 Q4 財報給出的 FY27 營收成長指引低於 10%","ruling":"Q3 證據顯示雙位數成長是 17 倍與 13 倍兩種定價框架的分界，數學上是終值最大的單一敏感項，所以設為 Single Thing；發生即減碼，營益率指引同時跌破則清倉","evidence_level":"中","settle_metric":"FY27 營收成長指引","if_then":["若指引低於 10%，減碼至 0.5%；營益率指引同時低於 32.5%，清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設 kill 指標。前份風險門檻：Nielsen 份額連 6 個月低於 8% 則減至試單；FY26 廣告低於 26 億美元或 CPM 低於 25 美元；單一體育合約超過 15 億美元／屆；內容攤銷成長率減營收成長率連 2 年大於 0","side_b":"本次：Nielsen 門檻保留，並加上 UCAN 年增低於 +9% 才減碼；新增營收年增連 2 季低於 +10%、FY27 營益率指引低於 32.5% 兩條減碼與清倉門檻；廣告與 CPM 門檻保留，但本包沒有數據，標資料缺口","ruling":"單看份額容易誤判，因為流失率在改善，所以份額門檻要與營收同時成立才減碼；新增的兩條對應 Q3 暴露的指引下緣與重組成本","evidence_level":"中","settle_metric":"Nielsen 份額、季度營收年增率、FY27 營益率指引","if_then":["任一減碼門檻觸發，減碼至 0.5%；營收與營益率門檻同時觸發，清倉"],"evidence_refs":["competitive_share_entrants#1"]}],"triggers":[{"n":1,"text":"Q4'26 營收是否達到公司指引","type":"假設驗證","maps_to":"H1","metric":"Q4'26 營收","threshold":"低於 134.42 億美元","action":"記 H1 一次削弱，搭配 FY27 指引判斷","source_freq":"季度股東信","date":"2027-01"},{"n":2,"text":"FY27 營收成長指引跌破雙位數","type":"Single Thing","maps_to":"Single Thing","metric":"FY27 營收成長指引","threshold":"低於 10%","action":"減碼至 0.5%；營益率指引同時低於 32.5% 則清倉","source_freq":"年度指引","date":"2027-01"},{"n":3,"text":"注意力份額持續流失並傳導到營收","type":"風險","maps_to":"R1","metric":"Nielsen 美國電視觀看份額與 UCAN 營收年增率","threshold":"份額連 6 個月低於 8% 且 UCAN 年增低於 +9%","action":"減碼至 0.5%，重跑判斷","source_freq":"Nielsen 月報＋季度股東信","date":null},{"n":4,"text":"營益率擴張路徑被成本打斷","type":"風險","maps_to":"R2","metric":"FY27 營益率指引","threshold":"低於 32.5%","action":"減碼至 0.5%","source_freq":"年度指引","date":"2027-01"},{"n":5,"text":"電影進口關稅正式落地","type":"風險","maps_to":"R3","metric":"關稅適用範圍","threshold":"正式生效且適用串流原創","action":"停止加碼，以 EPS −20% 重算情境","source_freq":"白宮與商務部公告","date":null},{"n":6,"text":"全年指引確認雙引擎續航","type":"加碼","maps_to":"H1","metric":"FY27 營收與營益率指引","threshold":"營收 ≥+10% 且營益率 ≥33%","action":"加碼至 3%","source_freq":"年度指引","date":"2027-01"},{"n":7,"text":"價格先走、基本面未變時分批買回","type":"估值rearm","maps_to":"H1","metric":"股價與 FY27 共識 EPS","threshold":"股價 ≤55 美元且 FY27 共識 EPS 未下修","action":"分批加至 2%","source_freq":"每日股價＋共識快照","date":null},{"n":8,"text":"Q4 財報後全面複審","type":"複審日期","maps_to":null,"metric":"全年指引與 Nielsen 份額","threshold":"財報後一週內","action":"重跑判斷","source_freq":"一次性","date":"2027-01"}],"kill_metrics":[{"metric":"匯率中性營收年增率（季）","bear_threshold":"連 2 季低於 +10%","window":"2026Q4 至 2027Q2","source":"Netflix 季度股東信","last_status":"ok"},{"metric":"Nielsen Netflix 美國電視觀看份額","bear_threshold":"連 6 個月低於 8% 且 UCAN 年增低於 +9%","window":"滾動 6 個月","source":"Nielsen The Gauge 月報","last_status":"warning"},{"metric":"FY27 營業利益率指引","bear_threshold":"低於 32.5%","window":"2027-01 財報","source":"Netflix Q4'26 股東信","last_status":"unknown"},{"metric":"FY27 營收成長指引","bear_threshold":"低於 10%","window":"2027-01 財報","source":"Netflix Q4'26 股東信","last_status":"unknown"},{"metric":"FY26 廣告營收","bear_threshold":"低於 26 億美元（資料缺口，公司若揭露才可判）","window":"FY2026","source":"Netflix 股東信；本包未涵蓋","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把美國觀看疲軟與廣告落後外推成成熟媒體股，但共識 EPS 三個月未下修、流失率年改善、調價順利，跌幅全來自倍數壓縮；FY2 本益比 17.1 倍已接近成熟媒體框架的上緣"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=-30.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"pacing":[],"holding_cap":"3%","requires_critic":[],"rearm_trigger":"2027-01 指引 FY27 營收 ≥+10% 且營益率 ≥33% 才加碼至 3%；未達則維持 1% 試單、不追","exec_line":"維持 1% 試單；Q4 財報（2027-01）前不加碼；跌到 55 美元以下且 FY27 共識 EPS 未下修，可分批加至 2%"},"reasoning":{"industry":"Q3'26 營收 128.7 億美元，GAAP 營益率 34.6%；公司說優於預測主要是費用認列時點，不是結構改善。TTM 毛利率 49.1%，從 2022 年 39.4% 逐年升到 2025 年 48.5%。全年營收點估 511 億美元（+13%），Q4 指引 134.4 億美元（+12%）。CFO 2026-10-20 說收入有三個槓桿：會員數、單價、廣告。Ted 2026-10-20 說約 95% 的內容支出和幾乎全部營收都在核心串流。區域營收：UCAN 56.3 億美元，年增 11%；EMEA 41.1 億美元，年增 11%（匯率中性 9%）；LATAM 16.0 億美元；APAC 事實表未涵蓋。單點依賴方面，客戶是分散的消費者，沒有集中度問題；公司稱不依賴任何單一內容供應商，但這些供應商同時也是競爭者。產業時鐘在擴張期：全球線上影音營收 2025 年 +13.5%，付費電視 −4%；不過訂閱數成長預期 2026 年降到個位數，擴張已進入後段。供需持久性屬結構性持久：收視從線性電視往串流遷移仍在進行，工作室端持續整併，不是會反轉的週期。","moat":"護城河機制是規模。全球最大的付費家戶基數分攤原創內容成本，讓美國每小時觀看單價在 SVOD 中最低（Greg 2026-10-20 稱對手每小時價格有時超過兩倍），因此有反覆調價的空間。支持方向的證據：毛利率 2022→2025 年由 39.4% 升到 48.5%，營益率由 17.8% 升到 29.5%；2026-03 美國全方案調價後，Q3 全球與美國流失率都年改善且優於預測。反向證據：Nielsen 美國電視觀看份額 8.3%→7.9%，同期 YouTube 12.8%→13.5%、Prime Video 3.6%→4.2%；管理層自承美國片單成長『沒有我們想要的快』，更換內容長、裁員，廣告進度也落後年初的積極目標。同業表是廣告與注意力平台：Netflix 營益率 29.7%，低於 META 38.1% 與 GOOGL 33.1%，高於 PINS 6.3% 與 ROKU 5.3%。同業 ROIC 事實表未涵蓋，無法驗證報酬價差方向。評分：執行 8、定價 8，YouTube 的生態攻擊扣 1 分，合計 7，等級 B。","growth":"成長來源是量（新興市場會員）、價（成熟市場調價）、廣告（今年成長逾 80%，2027 年新增 15 國廣告方案）三者；沒有併購（WBD 案已終止），淨回購每年約 1.3%。共識 EPS：FY2025A 2.53、FY2026E 3.59、FY2027E 3.80、FY2028E 4.56，三年年複合約 21.7%，算法是（4.56÷2.53）^(1/3)−1。EPS 分析師家數事實表未涵蓋（營收共識 FY1 40 家、FY2 45 家）。FY2027E 只比 FY2026E 高 6%，營收共識卻高 10.8%；推論 FY2026E 含 2026-02 收到的 28 億美元 WBD 終止費（稅前約每股 0.67 美元），這是未證推論。內生上界約 17.5%（見護城河段），缺口約 4pp，可歸因於營益率擴張（2025 年 29.5%，FY26 指引 31.5%）與淨回購，不靠重新評價。跑道：管理層稱全球可觸及家戶約 8 億戶（2026-07-16），但 Netflix 會員數與滲透率事實表未涵蓋，跑道年數無法計算；美英澳已深度滲透，成長偏向單價與廣告（Greg 2026-10-20）。","governance":"FCF÷淨利 2024 年 0.79、2025 年 0.86，轉換率健康；Q3'26 FCF 28.8 億美元。SBC 占 Q3 營業利益 3%，約營收 1%。以淨利÷稀釋 EPS 推算，稀釋股數 2022→2025 年由約 45.1 億降至 43.4 億，每年淨縮減約 1.3%。Q2'26 回購 47 億美元，是單季歷史最大（CFO 2026-07-16）。淨負債 69.1 億美元（含租賃），另收到 WBD 終止費 28 億美元。現金去向四分、債務到期結構、回購均價事實表未涵蓋。爭議點：2025-12 公司簽下企業價值 827 億美元的 WBD 案，並開 50 億美元循環信貸，與 Ted 2026-07-16『主要是建造者不是買家』的說法不一致。此案雖已終止且淨賺終止費，仍顯示大型併購是管理層的選項。","valuation":"股價 65.04 美元。FY1 本益比 18.1 倍，FY2 本益比 17.1 倍；trailing 本益比 18.8 倍，是 4 個年度端點中最低；P/S 5.45 倍（分位 17.4%），前瞻 EV/S 5.43 倍。FY1 分母可能含一次性終止費，主尺改用 FY2。PEG：FY2 本益比÷共識三年 EPS 年複合 21.7%≈0.8；改用基本情境年複合 12.6% 約 1.4，仍在合理區。賣方目標價：2026-09 平均約 93.66 美元，另一來源共識 103 美元，區間 80–151 美元（高低比 1.9 倍，低於 2.5 倍），現價比均值低約 30–37%，方向支持本次不賣的結論，但賣方目標價在下修中。基本情境：一年後以 17 倍乘 FY2028E 4.56 美元得 77.5 美元（+19%）；三年後 17 倍乘 5.85 美元得 99.5 美元（+53%）。共識 FY1 EPS 近三個月 +0.6%，FY2、FY3 未動，跌幅來自倍數不是盈餘。","premortem":"26 週股價 −30.2%，RSI 32.6，市場已把觀看疲軟計入股價。共識 FY1 EPS 近三個月 +0.6%，FY2、FY3 未動，跌幅來自倍數不是盈餘。衰退信號亮 2 個（核心市占縮減、EPS 成長遠高於營收成長），屬中度陷阱風險。三個視角的反證寫在反證紀錄。歷史最大回撤、訴訟金額事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺全球付費家戶的月費，加上快速成長的廣告預算；錢卡在『同一筆內容攤銷能讓多少家戶、以多高單價分攤』這一節點。","moat":"護城河方向持平：定價力穩定，但注意力份額小幅流失，美國片單與廣告兩處的執行落後。","growth":"五年後的成長跑道中等：成熟市場靠單價與廣告，新興市場靠會員，還沒有看到串流本業以外的第二條需求曲線。","capital":"資本配置中等偏好：股權稀釋低、回購持續；但回購價格是否夠便宜無法驗證，且曾嘗試企業價值 827 億美元的大型併購。","valuation":"現價只要求 FY27 起 EPS 年增約一成、本益比維持在 17 倍上下，就有雙位數報酬。我相信成長，但不確定市場會不會改用成熟媒體股的 13 倍框架。","how_wrong":"最可能看錯在：美國注意力流失比流失率更早反映問題。份額下滑先傷內容效率，兩三年後才傷到定價。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把美國觀看疲軟與廣告落後外推成成熟媒體股，但共識 EPS 三個月未下修、流失率年改善、調價順利，跌幅全來自倍數壓縮；FY2 本益比 17.1 倍已接近成熟媒體框架的上緣","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟢","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":65.04,"week26_return_pct":-30.24,"consensus_rev_3m_pct":0.56,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY26 EPS 可能含 WBD 終止費一次性收益（推論未證），所以主尺改用 FY2；以 FY2 計本益比 17.1 倍，結論不變"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4'26 財報與 FY27 全年營收、營益率指引","impact":"高","watch":"營收成長是否 ≥10%、營益率是否 ≥33%"},{"date":"2026-11","date_precision":"month","type":"product","event":"感恩節前夕首場 NFL 直播；12 月聖誕節 NFL 賽事","impact":"中","watch":"直播帶來的新增會員與廣告收入"},{"date":"2027","date_precision":null,"type":"product","event":"15 個新國家上線廣告方案","impact":"中","watch":"上線時程是否延後、廣告成長率"},{"date":"2027","date_precision":null,"type":"product","event":"Narnia 等大型片 45 天戲院窗口上映","impact":"低","watch":"票房與上架後觀看時數"},{"date":null,"date_precision":null,"type":"regulatory","event":"美國電影進口關稅是否經 Section 232 正式落地","impact":"中","watch":"是否適用串流原創、公司損益影響"}],"_projected_from":"v19"}
```
