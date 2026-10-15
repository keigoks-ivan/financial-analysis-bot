你是 stock-analyst v20 的**散文層（prose）agent**，標的 3189.TW（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261012/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：3189.TW　日期：2026-10-12　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1232B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（391B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1005B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（780B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1224B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（388B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（689B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1913B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3568B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1936B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1232           4038-5768      5 條（2–6 內）  
s3                  8000         391           5326-7609      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3009          8394-11991      5 條（2–6 內）  
s6                 11000         388          7428-10612      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         689           1968-2811      5 條（2–6 內）  
s10                 5000        1913           2161-3087      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1936           2000-3064      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4049B；至少需散文≈40.95KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−88
−83%
−65%
−55%
−55
−39.6
−39.6%
−17
−17.0%
−0.4%
0
0.10
0.14%
0.143
0.25
0.75
1
1.07
1.2%
2
2%
3
3%
3.37
4
4.1
4.9
5
5%
5.6%
6
6.8%
7
7.4%
7.7%
8%
8
9.33
10%
10
10.1%
10.2%
10.4
11
11.26
12%
12
12.3
12.3%
12.5
12.7%
13.4%
13.5%
14
14%
14.25%
14.5%
14.57
15%
15
15.96
16.0%
16%
18
18.1
19.9%
20
20%
20.2
21
21.2%
22%
23.3%
23.4%
23.9
24
24.7%
25%
25
25.3
26%
26
26.1%
26.5
27
27%
28
28.11
29
29%
29.8%
30
30%
32
34%
35%
35
36.8%
37.7
37.71
40%
40
42%
42
45
46%
48
49
50%
51%
52
58
62
65
66.2
70
78
83%
85%
86%
90%
90
94.1
94.14
95%
100%
100
147
150%
182.8
189%
189.7%
189.72
196
232
235
315
366
473
526.91
560
600
620
640
868
880
892
1060.0
2021
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
3037
3189
4062
8046
20261012
1,060
1,596
1,711
10,382
12,496
2,114
39,351
4,000
5,000
6,977
78,876
8,000
8,457
−1,217
−2,900
−4,105
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
{"meta":{"ticker":"3189.TW","date":"2026-10-12","schema":"v15.0","contract":"v19","company_name":"景碩"},"oneliner":"景碩吃到 ABF 載板缺貨漲價，但 FY2027 共識 EPS 28.11 元已近上輪高峰兩倍，股價仍要 37.7 倍。高峰盈餘配上成長股倍數，2027 年起新產能潮是主要風險，等回檔再談。","thesis":{"H":[{"id":"H1","text":"AI 載板份額實現：AI 相關營收占比由 2026 年約一成升到 2027 年一成五以上","2y":"2027 年全年 AI 相關營收占比 ≥15%","5y":null,"10y":null,"threshold":"2027 年 AI 相關營收占比 ≥15%；低於 12% 視為未實現","source":"公司每季法說與年報","drift_rule":"連兩季法說占比低於 12% 為削弱；連三季低於 10% 為反轉"},{"id":"H2","text":"缺貨帶動的報價撐住毛利率","2y":"2027 年各季合併毛利率 ≥26%","5y":null,"10y":null,"threshold":"季毛利率 ≥26%（Q2 2026 為 26.1%）","source":"MOPS 季報","drift_rule":"連兩季低於 24.7%（偏離 5%）為削弱；連三季低於 23.4%（偏離 10%）為反轉"},{"id":"H3","text":"新增產能在折舊進來後仍賺得到合理報酬","2y":null,"5y":"2027 年起月產能由 4,000 萬顆增到 5,000 萬顆後，2028～2030 年營益率仍 ≥15%、稼動率 ≥85%","10y":null,"threshold":"年度營益率 ≥15%（FY2025 為 6.8%，Q2 2026 為 13.4%）","source":"年報與法說揭露的稼動率","drift_rule":"連四季 TTM 營益率低於 14.25% 為削弱；連六季低於 13.5% 為反轉"}],"R":[{"id":"R1","text":"T-glass 缺料延續，壓住每月 10%～15% 營收；Nittobo 獨供，2027 年第三季才擴產","h_ref":"H2","clock":"⚡","threshold":"擴產延後到 2027 年第三季之後，或受限比率升破 15%","evidence_refs":["supply_demand_durability#2"]},{"id":"R2","text":"全產業擴產潮：資本支出比上一輪高 51%，景碩 196～235 億元、南電逾 100 億元，2027～2029 年新產能陸續開出","h_ref":"H3","clock":"🔥","threshold":"新產能開出後報價季減，或稼動率跌破 85%","evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2"]},{"id":"R3","text":"高階 AI 客戶主供仍是欣興（ASIC 逾七成、Blackwell 逾三成）與 Ibiden，景碩的 GPU 份額目標可能落空","h_ref":"H1","clock":"🔥","threshold":"AI CPU 客戶供貨率由五成回落到三成以下，或 2027 年底 GPU 份額仍低於一成","evidence_refs":["competitive_share_entrants#2"]},{"id":"R4","text":"玻璃核心基板最快 2027 下半年導入，若演進到取代 ABF 增層，會壓縮載板的價值","h_ref":"H1","clock":"🐢","threshold":"主要客戶宣布量產封裝不含 ABF 增層","evidence_refs":["substitute_technology#1"]},{"id":"R5","text":"ABF 膜由味之素近獨供，材料漲價或配額會吃掉載板的漲價空間","h_ref":"H2","clock":"🐢","threshold":"季毛利率因材料成本降 2pp 以上","evidence_refs":["geo_supply_chain#1"]},{"id":"R6","text":"重演上輪下行：2023 年全球載板市場約減三成，景碩前三季虧損","h_ref":"H2","clock":"🔥","threshold":"月營收連三個月年減","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]}],"single_thing":{"description":"ABF 載板報價出現本輪首次季減","why_fatal":"FY2027 共識 EPS 28.11 元建立在報價每季上漲的前提上；稼動率已到 95%，報價是剩下唯一的毛利來源。上輪 2022→2023 年營收減 36.8%，EPS 由 14.57 元掉到 0.10 元。","if_happens":"已持有者清倉、未持有者不建立；改用下行的 Bear 路徑重新估值","how_monitor":"每季法說與法人報價調查、MOPS 月營收、季毛利率","probability":"12～24 個月內約 30%"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":37.71,"peg_fy2":0.25,"stress":{"pass":null,"total":null},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-10-12）"},"eps_meta":{"base_eps_path":{"FY2025A":3.37,"FY2026E":11.26,"FY2027E":28.11,"FY2028E":null},"fy_end_month":12,"eps_basis":"TWD 稀釋 EPS（GAAP）；FY2026E、FY2027E 為 yfinance 分析師平均；FY2028E 共識事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261012/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"FY2022→FY2023 營收減 36.8%，EPS 由 14.57 元掉到 0.10 元，再回升到 FY2025 的 3.37 元。走勢由產能建設週期與報價驅動。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉。缺口估計 2027～2028 年擴大，但全球載板廠 2025～28 年資本支出比上一輪高 51%，綠地產能 2027 年起開出，T-glass 2027 年第三季擴產。各家缺口預估差距大，2028 年從 16% 到 51% 都有。","bargaining":{"up":"上游 T-glass（Nittobo 獨供）與 ABF 膜（味之素市占九成以上）議價力強，景碩是價格接受者。","down":"缺貨期間景碩對客戶的議價轉強，證據有兩項：長約客戶同意額外產能付款，擴產設備由客戶出資。這個判斷只適用於缺貨期。客戶集中度、前幾大客戶的營收占比與信用狀況，以及客戶的第二供應來源與轉單成本，事實表都查無資料，所以這裡不對客戶集中度下結論。單一客戶風險列為資料缺口，待年報主要客戶揭露後補判。間接線索只有一項：美系 AI CPU 客戶對景碩的供貨率由一成升到五成，代表該客戶同時有其他供應商，份額可以在供應商之間移動；但其他供應商是誰、份額多少，事實表未涵蓋。","geo":"生產據點在台灣、中國蘇州與美國；美國 232 半導體關稅是否涵蓋載板未確認。"},"profit_pool_dir":"利潤池目前流向載板環節（報價上漲、部分現貨漲逾三成）。2027 年後上游獨供材料與新一輪擴產會把利潤收回。","tam_table":{"expanded":false,"reason":"事實表未涵蓋載板市場規模與滲透率。AI GPU 份額兩成只是公司目標，沒有第三方份額序列可建表。"}},"moat":{"mechanism":"護城河靠高層數 ABF 的製程良率與客戶認證週期，加上缺貨期的產能可得性。產能這項優勢會隨 2027 年後新產能開出而消退。","execution":6,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：AI CPU 客戶供貨率由 10% 升到 50%。定價力穩定但屬全產業共享；營益率與欣興相當、低於南電，同業利潤率差距沒有擴大。","peer_na_reason":"Ibiden 營收欄缺失且只有兩季資料，無法計算利潤率。","threats":[{"level":"🟡","text":"欣興在美系 AI ASIC 載板份額逾七成、Blackwell 逾三成，景碩在 GPU 端份額目標兩成尚未實現，屬點對點競爭。","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"玻璃核心基板最快 2027 下半年導入（GlaSSEM 目標供貨），但 Intel 的設計保留 ABF 增層，只取代核心層，目前不算整體替代。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"ABF 增層膜由味之素供應九成以上，約占載板原料成本 25%～30%；材料漲價或配額會直接吃掉載板的漲價空間。","p":"30%","evidence_refs":["geo_supply_chain#1"]}],"roic_durability":{"quadrant":"低利益率×低周轉（TTM 營益率 10.1%；周轉率事實表未涵蓋，依載板重資產特性暫判）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"AI 伺服器 CPU／GPU 封裝必須用 ABF，屬於需要而非想要；但手機與 PC 端需求仍弱，非 AI 部分可延後採購，整體需求基礎只有部分是剛性。"},{"item":"決策層級","level":"🟡","text":"客戶在單一封裝料號層級認證，重新認證有成本；但同一客戶同時用欣興、Ibiden、南電多源供應，料號層級可以調整份額，景碩的供貨率由一成升到五成就是例證。"},{"item":"價值鏈分配","level":"🔴","text":"上游 T-glass（Nittobo）與 ABF 膜（味之素）都是獨供或近獨供，下游是強勢晶片商；載板環節只有在缺貨期才多拿到利潤，上輪下行時 FY2023 前三季虧損。"},{"item":"社會容忍度","level":"🟢","text":"B2B 零件，不依賴監管授權，不涉民生定價。美國 232 關稅是否涵蓋載板未確認，屬政策觀察項，不構成價格天花板。"}],"roiic":"事實表未涵蓋（投入資本與折舊未收）","reinvest_rate":"粗估 4.1～4.9 倍，屬總資本支出口徑：三年擴產專案 196～235 億元，年均 65～78 億元，除以 FY2025 淨利 15.96 億元。折舊事實表未涵蓋，淨再投資率無法計算；方向上遠高於 100%。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。再投資率粗估＝（196～235 億元÷3）÷15.96 億元＝4.1～4.9 倍；這是未扣折舊的總資本支出口徑，也無法拆出客戶出資的設備金額，實際淨再投資率會較低。增量 ROIC 缺投入資本，無法計算，所以內生上界不給數字。共識成長主要來自利潤率回升，不是再投資複利。"},"combined":5.5,"score":5.5,"spread_table":[{"metric":"毛利率","3189.TW":23.26,"3037.TW":19.85,"8046.TW":16.04,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","3189.TW":10.12,"3037.TW":10.24,"8046.TW":12.27,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","3189.TW":7.37,"3037.TW":-0.4,"8046.TW":7.71,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","3189.TW":5.59,"3037.TW":3.92,"8046.TW":null,"4062.T":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3037.TW","gm":19.85,"om":10.24,"fcf_margin":-0.4,"rd_intensity":3.92,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"8046.TW","gm":16.04,"om":12.27,"fcf_margin":7.71,"rd_intensity":null,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"4062.T","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"period":"TTM ending 2026-06-30（2季加總）"}]},"growth":{"driver_mix":"量（產能 4,000→5,000 萬顆，2029 年目標 8,000 萬顆）加上價（Q3、Q4 報價各季約 +8%）；沒有併購、沒有回購。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界的輸入事實表未涵蓋。共識 FY2025A→FY2027E EPS 年化約 189%，營收年化約 42%，缺口來自利潤率回升與報價，屬循環修復而非再投資複利，判為超出內生上界。","segments":{"expanded":false,"reason":"ABF 與 BT 的分部營收與毛利事實表未涵蓋。載板營收占 Q2 合併約 83%，其餘約 2,114 百萬元的內容未揭露，無法建表。"},"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"Q1 2026 21.2%→Q2 26.1%，季比上升；季度年比資料事實表未涵蓋"},{"signal":"核心市占縮減","lit":false,"note":"AI CPU 客戶供貨率上升；整體份額序列事實表未涵蓋"},{"signal":"提價後銷量下滑","lit":false,"note":"稼動率由 86% 升到 95%"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY2025A→FY2027E EPS 年化約 189%，營收約 42%"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"note":"FY2024 為負、FY2025 約 1.07，只有一年未達"},{"signal":"SBC／營收逾 5% 且上升","lit":false,"note":"Q2 SBC 僅占營業利益 1.2%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"玻璃核心最快 2027 下半年導入，列入觀察"},{"signal":"產業倍數近三年系統性下移","lit":false,"note":"P/S、EV/S 在自身年度端點最高"},{"signal":"維持性資本支出占 FCF 逾六成","lit":false,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且收入下滑","lit":false,"note":"正在大幅擴產"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；回購與近三年現金去向四分事實表未涵蓋"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年沒有併購事件（事實表併購軸查無資料）","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購；股息殖利率 0.14%","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營業利益 1.2%，但流通股 526.91 百萬股與 FY2025 淨利除以 EPS 推得的約 473 百萬股不一致，淨稀釋率無法確認","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY2027 共識 EPS），輔以 P/S、EV/S 自身區間","tier":"台系 ABF 載板三家（欣興、南電、景碩）同級","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比或 EV/S，無法建倍數對照"},"fwd_pe":94.14,"peg":null,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"94.1 倍 FY1、37.7 倍 FY2 共識本益比，配上 P/S 與 EV/S 都在自身最高點，又是循環高峰盈餘，所以判為昂貴。PEG 不計算：基期 FY2025A 3.37 元是谷底回升，成長率被基期放大；FY2028E 共識也缺。五年分位不給：只有四個年度端點。短期上檔用賣方平均目標價中點 880 元，880÷1,060−1＝−17.0%。中期上檔用基準情境 FY2028E EPS 32 元乘終端 20 倍，得 640 元，640÷1,060−1＝−39.6%。","upside_short_pct":-17.0,"upside_mid_pct":-39.6},"trap_analysis":{"verdict":"🟡","label":"高峰盈餘陷阱：倍數建立在景氣高點盈餘上"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"上輪 FY2022→FY2023 營收減 36.8%，EPS 由 14.57 元掉到 0.10 元，2023 年前三季虧損；2023 年全球 IC 載板市場預估下滑約 30%。本輪全產業資本支出比上一輪高 51%，景碩自己就有 196～235 億元擴產。","assumption":"這輪 AI 需求能吸收 2027～2029 年的新產能，不重演 2023 年","consequence":"若報價在 2027 下半年轉跌，EPS 可能回到個位數；股價以循環股倍數計，有八成以上的下行空間","ruling":"採納。Bear 機率設 35%，高於一般水準，依據是本輪擴產規模比上一輪更大。","watch":"ABF 報價季變動、月營收年增率、季毛利率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","supply_demand_durability#5","cyclical_supply_discipline_capacity#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"三年擴產 196～235 億元，2027 年起折舊進來；ABF 膜由味之素近獨供，約占載板原料成本 25%～30%；流通股數 526.91 百萬股，高於 FY2025 淨利除以 EPS 推得的約 473 百萬股。","assumption":"AI 需求成立時，營收成長能轉成每股盈餘成長","consequence":"即使營收翻倍，折舊、材料漲價與可能的股本稀釋會讓 ROIC 低於帳面成長的暗示，每股價值成長慢於營收","ruling":"部分採納。設備由客戶出資，降低了資本風險；但股數疑點未解，列為資料缺口，下季財報核對。","watch":"季營益率、季報股本變動、材料成本占比","evidence_refs":["supply_demand_durability#5","geo_supply_chain#1"],"fact_refs":["f_shares_diluted_m","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"現價 1,060 元是 FY2026 共識的 94.1 倍、FY2027 共識的 37.7 倍；P/S、EV/S 在自身最高點；現價高於賣方平均目標價約 868～892 元；26 週漲 189.7%。","assumption":"市場給循環高峰盈餘成長股的倍數","consequence":"即使 FY2027 共識兌現，倍數收斂到 20 倍也只值約 560 元","ruling":"採納。現在就買的最強論證是：高盛估 2028 年缺口 51%，若 FY2028 EPS 達 40 元，現價只有 26.5 倍。但這個 EPS 沒有共識數字支持（FY2028E 共識缺），屬於未證實的推論。","watch":"FY2027 共識 EPS 修正方向、FY2028 共識是否出現且高於 FY2027","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_price_at_dd","f_consensus_eps_fy2","f_ps_percentile","f_week26_return_pct"]}],"max_dd":{"lo":-88,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1060.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1060.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率口徑","cause":null,"prior_field":null,"side_a":"MOPS 來源的季報：Q2 2026 合併毛利率 26.1%，營益率 13.4%，上半年數字與公告核對相符","side_b":"Quartr 簡報摘要：Q2 合併毛利率 12.7%，載板毛利率約 14%～15%","ruling":"採用 26.1%。若載板毛利率只有 14.5%，非載板部分要約 83% 的毛利率才能湊出 26.1%，不合理；Quartr 的數字較可能是營益率或其他口徑標錯。","evidence_level":"一手季報對二手摘要","settle_metric":"Q3 2026 季報的分部毛利揭露","if_then":["若 Q3 季報顯示載板毛利率低於 15%，H2 改用載板口徑重設門檻，基準 EPS 路徑下修兩成","若 Q3 合併毛利率落在 27%～29%，維持 26.1% 口徑"],"evidence_refs":["competitive_share_entrants#4","reg_tariff_export#1"]},{"axis":"缺貨持續期對新產能潮","cause":null,"prior_field":null,"side_a":"缺口延續擴大：高盛估 2026 下半年、2027、2028 年分別為 14%、34%、51%；凱基估 2027～28 年 22%、29%；壓膜機交期排到 2031 年","side_b":"供給追上：全球資本支出比上一輪高 51%，綠地產能 2027 年起開出，南電資本支出逾 100 億元，景碩自己擴產兩成五，另一家外資估 2028 年缺口只有 16%","ruling":"兩邊可以調和，關鍵在時間先後。2027 年缺貨的證據較強，採 A 側；2028 年後各家預估差三倍，不採信高峰延續，基準情境讓盈餘在 2028 年見頂。依據：上輪也是在擴產高峰後一年內反轉。","evidence_level":"多家券商估計，二手轉述為主","settle_metric":"ABF 報價季變動、景碩稼動率","if_then":["若 2027 年第三季 T-glass 擴產後報價仍季增且稼動率 ≥90%，Bull 機率由 20% 升到 30%，股價在 600 元以下開始分批反買","若 2027 年任一季報價季減，視為 Single Thing 發生，已持有者清倉"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","end_markets#5"]},{"axis":"毛利改善來源","cause":null,"prior_field":null,"side_a":"公司說法：毛利改善主要來自稼動率提升，而非漲價","side_b":"法人估計：ABF 與 BT 報價 Q2 再漲約 5%，Q3、Q4 各季約 8%，部分現貨漲逾三成","ruling":"程度差異，可以調和。稼動率已到 95%，接下來的毛利只剩報價這條路，所以報價是未來的關鍵變數。","evidence_level":"公司口徑對法人估計","settle_metric":"Q3 毛利率是否落在 27%～29%","if_then":["若 Q3 毛利率低於 26%，報價論點證偽，停止加碼且不建立"],"evidence_refs":["end_markets#4","cyclical_inventory_price_position#0"]}],"triggers":[{"n":1,"text":"股價回到約 600 元以下，且 FY2027 共識 EPS 未下修逾一成：重跑判斷，首筆不超過 2%","type":"估值rearm","maps_to":"action_conditions.rearm_trigger","metric":"股價與 FY2027 共識 EPS","threshold":"股價 ≤600 元且共識 ≥25.3 元","action":"分批反買","source_freq":"每日股價；共識每月","date":null},{"n":2,"text":"2027 年 AI 相關營收占比達 15% 以上，份額論點成立","type":"假設驗證","maps_to":"H1","metric":"AI 相關營收占比","threshold":"≥15%（低於 12% 視為未實現）","action":"不追","source_freq":"每季法說","date":"2027-Q4"},{"n":3,"text":"T-glass 擴產延後到 2027 年第三季之後，或營收受限比率升破 15%","type":"風險","maps_to":"R1","metric":"Nittobo 擴產時程、公司揭露的營收受限比率","threshold":"延後或受限比率 >15%","action":"停止加碼","source_freq":"每季法說與供應鏈報導","date":"2027-Q3","evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"ABF 載板報價出現本輪首次季減","type":"Single Thing","maps_to":"thesis.single_thing","metric":"ABF 報價季變動","threshold":"任一季季減","action":"清倉","source_freq":"每季法說與法人報價調查","date":null},{"n":5,"text":"新產能開出後稼動率跌破 85%，或季毛利率連兩季低於 24.7%","type":"減碼","maps_to":"R2","metric":"稼動率、季毛利率","threshold":"稼動率 <85% 或毛利率連兩季 <24.7%","action":"減碼","source_freq":"每季","date":null,"evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2"]},{"n":6,"text":"主要 GPU 或 CPU 客戶宣布量產封裝改用不含 ABF 增層的玻璃核心設計","type":"風險","maps_to":"R4","metric":"客戶封裝設計公告","threshold":"任一主要客戶宣布量產","action":"減碼","source_freq":"產業新聞與客戶發表會","date":"2027-Q3","evidence_refs":["substitute_technology#1"]},{"n":7,"text":"Q3 2026 財報：核對毛利率口徑、股本變動與 Q3 毛利率是否在 27%～29%","type":"複審日期","maps_to":"H2","metric":"Q3 合併毛利率、季報股本","threshold":"毛利率 ≥26%","action":"不追","source_freq":"季報","date":"2026-11"}],"kill_metrics":[{"metric":"合併季毛利率","bear_threshold":"連兩季低於 22%","window":"2026Q3～2027Q4","source":"MOPS 季報","last_status":"ok"},{"metric":"ABF 載板報價季變動","bear_threshold":"本輪首次季減","window":"2026Q4～2027Q4","source":"公司法說與法人報價調查","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"由 28.11 元下修逾 15%（低於 23.9 元）","window":"未來 12 個月","source":"yfinance 分析師共識","last_status":"unknown"},{"metric":"月營收年增率","bear_threshold":"連三個月低於 10%","window":"未來 12 個月","source":"MOPS 月營收","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把缺貨期的報價漲幅當成 AI 結構性成長來定價。但 AI 相關營收 2026 年只占約一成、2027 年預期一成五到兩成，其餘八成以上仍隨載板週期漲跌；而 2025～28 年全產業資本支出比上一輪高 51%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=189.72, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"verdict":"觀望","rearm_trigger":"股價 ≤600 元（約 FY2027 共識 EPS 的 21 倍），且 FY2027 共識 EPS 未較 28.11 元下修逾一成","exec_line":"不追。觸發重啟條件後重跑判斷，首筆不超過 2%；加碼要等 Q3 2026 毛利率 ≥27% 確認。"},"reasoning":{"industry":"Q2 2026 合併營收 12,496 百萬元，毛利率 26.1%，營益率 13.4%。載板營收 10,382 百萬元，約占合併 83%；其餘約 2,114 百萬元的內容事實表未涵蓋。上半年營收年增 29.8%，Q2 創新高。成長來自三個來源：一是 AI 高層數 ABF，法人稱美系 AI 客戶 CPU 供貨率由 10% 升到 50%，ABF 稼動率由 86% 升到 95%；二是全產業缺貨帶動報價，法人估 Q3、Q4 均價各季增約 8%；三是稼動率回升。手機與 PC 需求仍弱。AI 相關營收 2026 年約一成，2027 年預期一成五到兩成，所以八成以上營收仍跟著載板週期走。錢卡在上游：T-glass 由 Nittobo 獨供，2027 年第三季才擴產，每月壓住 10%～15% 營收；ABF 膜由味之素供應九成以上。供需持久性判為週期性將反轉：缺口預估 2027～2028 年擴大，但全球載板廠 2025～28 年資本支出比上一輪高 51%，綠地產能 2027 年起開出。產業時鐘判在過熱段，依據是稼動率接近滿載、部分現貨價漲逾三成、各家同步擴產、壓膜機交期排到 2031 年。客戶與分部占比事實表未涵蓋，單一客戶依賴程度無法量化。","moat":"同業 TTM 比較：景碩毛利率 23.3%，高於欣興 19.9% 與南電 16.0%；營益率 10.1%，與欣興 10.2% 相當、低於南電 12.3%；FCF 利潤率 7.4%，欣興 −0.4%、南電 7.7%。毛利率領先但營益率沒有領先，多出來的毛利被研發（占營收 5.6%）與費用吃掉，看不出結構性成本優勢。與同業的 ROIC 差距無法計算，因為投入資本事實表未涵蓋。執行面往上：AI CPU 客戶供貨率由一成升到五成；公司目標拿下 Vera CPU 載板全部份額、AI GPU 份額升到兩成，但都尚未實現。定價面穩定：漲價來自全產業 T-glass 缺料，欣興與南電同樣受惠。欣興在美系 AI ASIC 載板份額逾七成、Blackwell 相關逾三成，高階 AI 客戶的主供仍是欣興與 Ibiden。產業態勢是雙向拉鋸：競爭面各家同步擴產，南電 2026 年資本支出逾 100 億元；結構面缺貨延續到 2027 年；替代技術面，玻璃核心基板最快 2027 下半年導入，但目前的設計仍保留 ABF 增層。","growth":"成長由量與價共同推動，沒有併購或回購。量：ABF 月產能 4,000 萬顆，2027 年增到 5,000 萬顆，2029 年底目標 8,000 萬顆，擴產設備由客戶出資。價：法人估 Q3、Q4 報價各季約增 8%。共識 EPS 從 FY2025A 3.37 元到 FY2027E 28.11 元，兩年年化約 189%；同期營收由 39,351 百萬元到 78,876 百萬元，年化約 42%。EPS 成長比營收快約 147pp，差距幾乎全部來自利潤率由谷底回升，屬循環修復，無法歸因到再投資報酬，所以這段成長依賴估值重估。FY2028E 共識事實表未涵蓋，三年 CAGR 無法計算。滲透率事實表未涵蓋，跑道年數不給。衰退訊號亮一個：EPS 成長大幅高於營收成長。","governance":"FCF 轉換率：FY2022 −1,217 百萬元對淨利 6,977 百萬元；FY2023 −4,105 對 48；FY2024 −2,900 對 49；FY2025 才轉正，1,711 對 1,596，約 1.07 倍。TTM FCF 利潤率 7.4%，Q2 FCF 315 百萬元。SBC 很低：Q2 為 20.2 百萬元，占營業利益 1.2%（Q1 同欄口徑不同，跨季不可比）。現金去向以擴產為主：三年專案 196～235 億元，對照目前淨現金 8,457 百萬元，需要靠營運現金或舉債支應；股息殖利率 0.14%，回購事實表未涵蓋。股數存在疑點：目前流通股數 526.91 百萬股，但 FY2025 淨利除以 EPS 約 473 百萬股，可能有增資稀釋，也可能只是口徑差異，事實表未涵蓋原因。","valuation":"現價 1,060 元，對 FY2026 共識 EPS 11.26 元是 94.1 倍，對 FY2027 共識 28.11 元是 37.7 倍，trailing 182.8 倍。P/S 12.5 倍、EV/S 12.3 倍，都在四個年度端點的最高點；前瞻 EV/S 10.4 倍。賣方平均目標價約 868～892 元（7 月資料、偏舊），FactSet 6 月是 620 元，現價高於兩者。共識 EPS 從 6 月的 9.33 元上修到 11.26 元，所以目標價落後並不等於賣方看空，但現價已走在賣方前面。trailing 本益比分位 18.1 看似便宜，是因為 2023～2024 年 EPS 只有約 0.10 元，把歷史本益比撐得極高，不能拿來說便宜。","premortem":"高盛估 2028 年缺口 51%，大摩估 46%；擴產設備由客戶出資，代表客戶願意承擔產能風險；公司目標拿下 Vera CPU 載板全部份額、GPU 份額兩成。若這三件都成立，盈餘高峰會延到 2029 年後，我的基準情境就太悲觀。反方向的證據：另一家外資估 2028 年缺口只有 16%，全產業資本支出比上一輪高 51%，上輪 EPS 從 14.57 元掉到 0.10 元。股價 26 週已漲 189.7%，RSI 66.2，還沒到過熱線，但價格已經走在證據前面。陷阱評為中度：主要不是價值陷阱，而是高峰盈餘陷阱，倍數建立在景氣高點的盈餘上。"},"plain":{"six":{"how_it_makes_money":"賺的是 AI 伺服器 CPU／GPU 與一般運算晶片的載板錢。錢卡在上游兩個獨供節點：T-glass 玻纖布與 ABF 增層膜。產業正處在缺貨漲價的過熱段。","moat":"護城河方向持平（→）。執行面在 AI CPU 客戶拿到份額，但定價力來自全產業缺貨，不是景碩獨有。","growth":"成長跑道評為中等（🟡）。AI 載板是第二曲線的雛形，但占營收只有一到兩成，份額目標也還沒有外部證據證實。","capital":"資本幾乎全部投入擴產，現金回饋股東極低。擴產設備由客戶出資，降低了自有資本的風險，但廠房與折舊仍由景碩承擔。","valuation":"現價要求 FY2027 共識 EPS 28.11 元（上輪 2022 年高峰 14.57 元的近兩倍）兌現，還要在 2028 年後的新產能潮中守住。前半段我信一半，後半段不信。","how_wrong":"我最可能看錯的地方：AI 封裝需求讓這輪缺貨比 2021～2022 年那輪長得多，2028 年缺口真的擴大到三到五成，FY2028 EPS 衝過 40 元，37.7 倍就變成約 26 倍。"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把缺貨期的報價漲幅當成 AI 結構性成長來定價。但 AI 相關營收 2026 年只占約一成、2027 年預期一成五到兩成，其餘八成以上仍隨載板週期漲跌；而 2025～28 年全產業資本支出比上一輪高 51%。","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到約 600 元以下（FY2027 共識 EPS 的 21 倍）且共識未下修逾一成；或 FY2028 共識出現且不低於 FY2027。","trap":"🟡","val":"🔴","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":1060.0,"week26_return_pct":189.72,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"估值分母 FY2027 共識 EPS 28.11 元是缺貨高峰的盈餘，是否能持續正是核心爭點；任何以 37.7 倍說便宜的論證都不成立。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026 財報與法說","impact":"高","watch":"合併毛利率是否落在 27%～29%、分部毛利口徑、股本變動"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"Nittobo T-glass 擴產出貨","impact":"高","watch":"缺料解除後報價是否仍季增"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"景碩與欣興新產能陸續開出（景碩月產能增到 5,000 萬顆）","impact":"高","watch":"稼動率是否守住 85%"},{"date":"2027-Q3","date_precision":"quarter","type":"product","event":"GlaSSEM 玻璃核心基板目標供貨","impact":"中","watch":"主要客戶量產設計是否仍保留 ABF 增層"}],"_projected_from":"v19"}
```
