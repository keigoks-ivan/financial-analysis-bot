你是 stock-analyst v20 的**散文層（prose）agent**，標的 LYV（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：LYV　日期：2026-11-08　archetype：None　前份裁決：2026-05-18　觀望 — thesis 完整（Concerts +11%、Sponsorship +21%）但估值🔴過熱（PEG 2.6 + 5Y 80% 分位）+ Subramanian remedy 二元未明。等 5 或裁決明朗化｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1766B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（442B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（815B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1309B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（923B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（541B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（817B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2447B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1256B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2040B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1766           3664-5234      5 條（2–6 內）  
s3                  8000         442           5291-7558      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3047          8367-11953      5 條（2–6 內）  
s6                 11000         541          7321-10459      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         817           1878-2683      5 條（2–6 內）  
s10                 5000        2447           1787-2553      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2040           2000-2960      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4291B；至少需散文≈40.71KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−41%
−35
−35%
−1.68%
−0.46
−0.44
−0.24
0
0.1
0.44
0.46
0.46%
0.47%
0.61
0.75
0.8
0.95
1
1.1%
1.17
1.21%
1.3
1.5
1.5%
1.58
1.6%
1.71
1.75
1.8
1.9
1.93
2
02
2.19
2.35
2.5%
2.6
2.9
3
3%
3.05
3.157
3.4%
3.502
3.505
3.8%
04
4
4%
4.55%
4.89%
4.9
4.96
5%
05
5
5.057
5.1
5.23%
6
6%
6.3%
07
7
7.1%
7.58
7.8%
8%
8
08
8.2
8.3%
8.5
8.6%
8.8
8.8%
8.92
9%
9
9.7%
10%
10
10.9%
11
11.7%
11.79
12
12%
12.3
13
13.2%
14%
14
15%
15
16.11%
17
17.31%
20%
20
21.71%
22
24
25
25%
25.78%
27%
28.8%
29%
30
30%
32%
33
33.6%
35%
36
36%
37
38.18
40
48
49
50%
52.6%
56%
60%
60.4
64
65%
65
70
80%
82.57
87
90
90%
92
92.2
101.05
103
103.27
104
114
116.07
145
150
152.64
168.87
175.25
190
191
202
215
222
238
242
245
248
250
252.01
285.35
309
309.77
364.96
416
449.5
2026
2027
2028
2500
4000
6500
28534.92
29800
30400
30900
31200
31800
32400
33400
33800
35600
36100
38900
39700
41600
43800
47800
20261108
2,000
4,730
6,000
7,270
7,500
8,910
9,000
9,830
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
{"meta":{"ticker":"LYV","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Live Nation Entertainment"},"oneliner":"全年粉絲近 1.8 億、票務財測上修，需求論點成立；但州方反壟斷救濟未定，現價的基準五年年化報酬只有約 6%，等價格與救濟結果再談。","thesis":{"H":[{"id":"H1","text":"反壟斷以行為救濟收場，Ticketmaster 留在集團。","2y":"2028 年底前最終救濟不含剝離；票務 AOI 利潤率不低於 32%（Q3 2026 約 36%，由反推營收算出）。","5y":"上訴結束後票務仍在集團，FY2031 票務 AOI 五年年複合不低於 5%。","10y":null,"threshold":"不含剝離；票務 AOI 利潤率不低於 32%；集團 AOI 年增不低於 8%。","source":"法院文件、10-Q 法律附註、季度分部資料。","drift_rule":"票務 AOI 利潤率 TTM 低於門檻 5% 連 2 季為削弱，低於 10% 連 3 季為反轉；裁定含剝離直接反轉。"},{"id":"H2","text":"粉絲與場館管線延續，自營場館提高每位粉絲的利潤，並轉成現金。","2y":"FY2028 粉絲不低於 2 億、自營場館粉絲不低於 9,000 萬（2026 約 7,500 萬）；FCF 利潤率不低於 4%。","5y":"FY2031 粉絲不低於 2.35 億，營收不低於 416 億美元。","10y":null,"threshold":"FY2028 粉絲 2 億、自營 9,000 萬、FCF 利潤率 4%。","source":"季報、新聞稿、投資人日簡報。","drift_rule":"粉絲或 FCF 利潤率 TTM 低於路徑 5% 連 2 季為削弱，低於 10% 連 3 季為反轉。"},{"id":"H3","text":"贊助與票務兩個高利潤段持續成長。","2y":"FY2028 贊助 AOI 兩年年複合不低於 10%，票務 AOI 兩年年複合不低於 5%（已吸收費用上限）。","5y":"FY2031 贊助 AOI 五年年複合不低於 10%。","10y":null,"threshold":"贊助 AOI 年複合 10%；票務 AOI 年複合 5%。","source":"季度分部資料。","drift_rule":"TTM 成長低於門檻 5% 連 2 季為削弱，低於 10% 連 3 季為反轉。"}],"R":[{"id":"R1","text":"法院命令剝離 Ticketmaster，票務與演唱會的交叉導流斷開。","h_ref":"H1","clock":"🔥","threshold":"裁定含剝離即清倉。屬民事案件，受影響的票務 Q3 營收約 8.8 億美元；裁定日期未知。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#0","lawsuit_class_action#0","competitive_share_entrants#2","end_markets#3"]},{"id":"R2","text":"行為救濟逐年侵蝕：獨家年限縮短、系統開放、費用上限，加上自助售票與新對手。","h_ref":"H1","clock":"🐢","threshold":"票務 AOI 利潤率連 2 季低於 32%，或新增淨客戶票量轉負。","evidence_refs":["channel_business_model_shift#0","channel_business_model_shift#1","competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0"]},{"id":"R3","text":"Q4 演唱會 AOI 未兌現全年雙位數成長，2026 檔期紅利在 2027 回落。","h_ref":"H2","clock":"⚡","threshold":"FY2026 演唱會 AOI 年增低於 10%；FY2027 粉絲年增低於 5%。"},{"id":"R4","text":"場館資本支出報酬不達標；CFO 2026-07-30 說效益要到 2028 年，夥伴出資與投資報酬尚未揭露。","h_ref":"H2","clock":"🔥","threshold":"場館投資報酬低於 12%，或 FY2027 FCF 利潤率低於 3%。"},{"id":"R5","text":"FTC 與七州消費者保護訴訟、證券集體訴訟與州方賠償持續消耗現金。","h_ref":"H1","clock":"🔥","threshold":"累計現金賠償超過 10 億美元。","evidence_refs":["major_events#1","lawsuit_class_action#1","lawsuit_class_action#2"]},{"id":"R6","text":"倍數回落：EV/S 位於四個年度端點最高，每股盈餘基期被壓低。","h_ref":"H3","clock":"🔥","threshold":"前瞻 EV/S 高於 1.9 倍且無新證據時減碼；低於 1.3 倍且基本面無損時重跑研究。"}],"single_thing":{"description":"法院最終救濟命令 Live Nation 剝離 Ticketmaster。","why_fatal":"Q3 票務 AOI 占合併 27%，票務也是飛輪的連接點；基準與 Bull 都以票務留在集團為前提，終端 EV/S 每 0.1 倍約 17 美元，是情境中最大的敏感項。","if_happens":"清倉，現有三情境作廢，分拆後兩家公司重跑研究。","how_monitor":"法院救濟程序、JMOL 與上訴、Tunney Act 核准、10-Q 法律附註。","probability":"12 至 24 個月內約 15% 至 20%；事實表法律進度只到約 2026-05，這個機率信心低。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":92.2,"peg_fy2":1.75,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":-0.24,"FY2026E":-0.46,"FY2027E":1.9,"FY2028E":2.9},"fy_end_month":12,"eps_basis":"FY2025A 為年度財報稀釋每股盈餘；FY2026E 至 FY2028E 為 Koyfin 2026-11-07 共識，事實表未標明 GAAP 或調整後，數值方向與 GAAP 接近。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"場館與票務平台靠規模擴張，短期每股盈餘被訴訟費用壓低，救濟結果未定"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久。依據是 2026-07-30 CEO 稱取消率 1.1%、低於歷史均值 1.6%，2026-11-05 CFO 稱售完率高於去年，Goldman Sachs 2026 音樂報告看法相同。","bargaining":{"up":"頭部藝人議價力最強，演唱會利潤薄反映這點。","down":"對場館靠票務長約，對粉絲靠票源獨家，兩者正是訴訟焦點。","geo":"Q3 國際粉絲 +29%，拉美、歐洲、亞洲都至少 +15%；CEO 說拉美仍在早期，日本份額很小。"},"profit_pool_dir":"往自營場館、贊助與國際移動。","tam_table":{"expanded":false,"reason":"事實表沒有 TAM 與滲透率資料，全年近 1.8 億人次只能描述規模，無法算份額；成長論點靠場館產能與國際擴張，等投資人日資料再展開。"}},"moat":{"mechanism":"演唱會帶票務、場館長約綁票務、粉絲規模帶贊助的三段飛輪。定價分只反映票務與場館端，演唱會端藝人拿走大部分；法律衝擊只記在威脅扣分，不重複計入定價分。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行面擴大：今年新增淨客戶票量逾 2,000 萬張，Q3 收費票數 +10%。定價與合約面縮減：陪審團判決與和解條款限制獨家年限。兩者相抵判為穩定；若法院命令剝離或把獨家限制擴大，改判縮減。","peer_na_reason":"事實表只有同業利潤率，沒有投入資本與 ROIC，且同業業態不同，無法計算報酬差距。","threats":[{"level":"🔴","text":"反壟斷救濟：州方求分拆 Ticketmaster 與最高約 7 億美元；DOJ 和解條款含四年獨家上限、開放第三方使用系統、剝離至多 13 座圓形劇場。","p":"30%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#0","lawsuit_class_action#0","competitive_share_entrants#2","end_markets#3","channel_business_model_shift#0","channel_business_model_shift#1"]},{"level":"🟡","text":"自助售票、場館自售、SeatGeek、Fever 與 Eventim 美國擴張，10-K 也點名大型科技與電商可能進入；目前淨客戶票量仍增加。","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉（周轉率事實表未涵蓋，由預收票款模式推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"粉絲是使用者也是付款者，全年近 1.8 億人次；取消率 1.1% 低於歷史均值 1.6%。演出可以延後，但目前沒有延後跡象。"},{"item":"決策層級","level":"🟡","text":"票務決策單位是場館，長約原本 5 至 7 年，和解報導把獨家上限訂為四年，決策頻率會提高；今年新增淨客戶票量逾 2,000 萬張，目前仍在贏。"},{"item":"價值鏈分配","level":"🟡","text":"近 12 個月毛利率 25.78%，藝人拿走演唱會大部分價值；紐約州律師稱 Ticketmaster 每張票平均留 7.58 美元。自營場館讓公司多拿現場消費與贊助，但要投入資本。"},{"item":"社會容忍度","level":"🔴","text":"陪審團認定違法，33 州與華府起訴，FTC 另告消費者保護，費用上限 15% 已進和解條款。實際定價上限現在由政治與法律決定。"}],"roiic":"事實表未涵蓋投入資本，無法計算增量報酬。","reinvest_rate":"事實表未涵蓋折舊、營運資金與收購淨額，無法按公式計算；粗看 2026 資本支出指引 11 至 12 億美元，約等於 FY2025 營業利益 12.3 億的九成以上。","endo_ceiling":null,"formula_note":"FY2025 營業利益由 4.89%×252.01 億美元算出，只作規模參照，不是再投資率。CFO 2026-07-30 說效益要到 2028 年才明顯。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","LYV":25.78,"MSGE":45.82,"SPHR":55.77,"TKO":60.32,"WMG":45.77,"unit":"%"},{"metric":"營業利益率","LYV":2.94,"MSGE":17.31,"SPHR":-1.68,"TKO":21.71,"WMG":16.11,"unit":"%"},{"metric":"FCF 利潤率","LYV":5.23,"MSGE":24.21,"SPHR":22.68,"TKO":31.1,"WMG":3.94,"unit":"%"}],"competitors":[{"name":"MSGE","gm":45.82,"om":17.31,"fcf_margin":24.21,"strategy_note":"自有場館、單一市場，營業利益率 17.31% 反映資產稀缺，不是票務平台的直接對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"SPHR","gm":55.77,"om":-1.68,"fcf_margin":22.68,"strategy_note":"重資產場館，營業利益率 −1.68%，可作新場館投入期成本的反面參照。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"TKO","gm":60.32,"om":21.71,"fcf_margin":31.1,"strategy_note":"賺轉播權利金，營業利益率 21.71%，與演唱會分潤模式不同。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"WMG","gm":45.77,"om":16.11,"fcf_margin":3.94,"strategy_note":"在藝人上游，營業利益率 16.11%，拿的是版權端的分配。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（人次與收費票數），人均消費與價其次，併購補場館，淨回購為零。","runway_years":"事實表未涵蓋滲透率，無法計算","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋投入資本、折舊、營運資金與收購淨額，增量報酬與再投資率都算不出來，內生上界留空；無法驗證時保守視同共識成長超出上界。","segments":[{"item":"票務（Q3 2026）","value":"營收約 8.8 億美元（由年增 7,270 萬、+9% 反推），AOI 3.157 億、年增 10%，收費票數 9,830 萬張對 8,910 萬。"},{"item":"贊助與廣告（Q3 2026）","value":"營收 5.057 億美元、+14%，AOI 3.502 億、+12%，國際占成長 65%。"},{"item":"演唱會含公司費用（Q3 2026，由合併數倒減）","value":"營收約 87 億美元，AOI 約 5.1 億；粉絲逾 6,000 萬、近 +20%。"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":false,"note":"事實表只有 TTM 與年度，單季資料缺口。"},{"name":"核心市占近 12 個月縮減","lit":false,"note":"今年新增淨客戶票量逾 2,000 萬張。"},{"name":"提價後銷量下滑","lit":false,"note":"售完率高於去年。"},{"name":"每股盈餘成長高於營收成長逾 5 個百分點","lit":true,"note":"FY2027E 到 FY2028E 每股盈餘 +52.6%，主因基期被壓低。"},{"name":"FCF／淨利低於 0.75 連 2 年","lit":false,"note":"FY2025 0.61 倍、FY2024 1.17 倍，只有一年。"},{"name":"SBC／營收高於 5% 且上升","lit":false,"note":"Q3 為 0.47%。"},{"name":"TAM 萎縮或被替代","lit":false,"note":"未見證據。"},{"name":"產業倍數近 3 年系統性下移","lit":false,"note":"同業倍數資料缺口。"},{"name":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"2026 指引扣掉 8 至 8.5 億擴建後約 3 億上下，精確值事實表未涵蓋。"},{"name":"停止投資且收入下滑","lit":false,"note":"場館管線擴張中。"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"2026 年收購金額未揭露，事實表也沒有現金去向四分，無法算併購報酬；場館投資報酬與夥伴出資比例要等投資人日。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2026 年多筆場館收購金額未揭露，投入資本事實表未涵蓋，無法驗證。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"事實表沒有回購資料；管理層指引 2026 年股數大致不變。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 4,730 萬美元，年化約 1.9 億，約占市值 0.46%，低於每年 1.5% 上限；可轉債與選擇權的完整稀釋未計。","grade":"過"}]},"valuation":{"basis":"前瞻 EV/S，因 FY2026E 共識每股盈餘為負。","peers":{"expanded":false,"reason":"事實表的同業欄只有利潤率，沒有倍數；MSGE、SPHR、TKO、WMG 的業態也與票務加演唱會不同，終端倍數只能用自身現值錨定，缺同業對照。"},"fwd_pe":92.2,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"基準五年年化約 6%，低於 8%；EV/S 為四個年度端點最高；FY2027E 本益比 92 倍但基期被壓低，沒有極端高估的證據，定為偏貴。三年 PEG 因基期為負無法計算，五年分位資料缺口。","upside_short_pct":8.2,"upside_mid_pct":36.0},"trap_analysis":{"verdict":"🟡","label":"訴訟未定，商業面未見衰退"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"陪審團 2026-04-15 認定違法，33 州與華府求分拆 Ticketmaster 與最高約 7 億美元；DOJ 和解條款若落地，長約鎖定效果會縮短。","assumption":"基準假設救濟止於行為面，Ticketmaster 留在集團，票務 AOI 利潤率維持 32% 以上。","consequence":"若法院命令剝離或擴大獨家限制，票務與演唱會的交叉導流斷開，Bear 情境每股約 103 美元、較現價 −41%；跌 50% 需要再加上消費下行。","ruling":"部分採納。這條與唯一致命點部分重疊，剝離只是其中一條路徑。救濟結果在裁定公布前不可裁決，只能用機率處理；社會容忍度已是紅色，不把現有量價數字當成風險已解。","watch":"法院救濟裁定、Tunney Act 核准、票務 AOI 利潤率、客戶續約年限。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#0","lawsuit_class_action#0"]},{"view":"論點失敗","evidence":"事實表的法律資料只到約 2026-05，救濟程序、JMOL、Tunney Act 的最新狀態都未確認，Q3 逐字稿也沒有相關問答。","assumption":"這六個月沒有發生足以改變機率的裁定。","consequence":"若已有裁定，本次 Bear 機率與 Single Thing 機率都可能過時。","ruling":"採納為資料缺口。下一輪研究必須先補法院文件與 Q3 10-Q 法律附註，再更新機率。","watch":"Q3 10-Q 法律附註全文、法院案件紀錄。","evidence_refs":["regulatory_antitrust#1","end_markets#3"]},{"view":"論點成功但股東經濟變差","evidence":"FY2025 FCF 利潤率 1.21%，淨利 4.96 億美元卻每股 −0.24 美元；CFO 2026-11-05 說體育場利潤率較低、開幕前費用未來幾年上升；2026 資本支出指引 11 至 12 億美元，效益要到 2028 年。","assumption":"粉絲成長能轉成每股現金。","consequence":"粉絲與 AOI 都達標，但資本支出、夥伴分成與非控制權益分走利潤，每股價值增幅低於營收，基準的 245 百萬股與 40 億淨負債會偏樂觀。","ruling":"採納為主要保留。H2 門檻加上 FCF 利潤率，投資人日揭露夥伴出資比例與投資報酬之前，資本報酬檢查維持未知。","watch":"投資人日場館投資報酬與夥伴出資比例、FY2027 FCF 利潤率、開幕前費用。","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_peer_lyv_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"EV/S 1.58 倍為四個年度端點最高，FY2027E 本益比 92.2 倍，賣方均值目標只比現價高 9% 至 15%。","assumption":"現價已把行為救濟當基準，也計入 2026 的檔期高點。","consequence":"基準五年年化約 6%，機率加權約 5%，好消息的上檔有限。","ruling":"採納，這是本次不進場的主因。即使裁定只有行為救濟，上修 Bull 機率後仍需要價格配合。","watch":"EV/S、股價相對 150 美元、賣方目標。","fact_refs":["f_ev_s_fwd","f_ev_s_percentile","f_consensus_eps_fy2"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 168.87 → 本次 175.25（+3.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=168.87","side_b":"本次 price_at_dd=175.25","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 168.87 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 168.87 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 168.87 美元：Bull 價 364.96、Bear 價 103.27，五年期望值 +33.6%，基準年化 7.1%，不對稱比 2.19","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.19。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 168.87 美元：五年期望值 +33.6%，基準年化 7.1%，不對稱比 2.19","side_b":"本次情境、股價 175.25 美元：五年期望值 +28.8%，基準年化 6.3%，不對稱比 1.93","ruling":"再換股價、情境不動：起點價上漲 3.8%，五年期望值少 4.9 個百分點，基準年化少 0.8 個百分點，不對稱比由 2.19 降到 1.93。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"反壟斷救濟力道","cause":null,"prior_field":null,"side_a":"陪審團認定違法，州方求分拆 Ticketmaster，等於否定垂直整合的合法性。","side_b":"DOJ 和解不要求剝離，公司將提 JMOL 並上訴；2026 年票務與粉絲數據沒有受損。","ruling":"方向相反，屬不可調和。基準選和解路徑，依據是 DOJ 和解已明定不要求剝離，事實表也未見法院朝分拆方向裁定。決勝資料是救濟裁定，現在不存在，裁定公布前不可裁決。","evidence_level":"中：判決與和解多為二手報導，進度只到約 2026-05。","settle_metric":"法院救濟裁定文本","if_then":["若法院命令剝離 Ticketmaster，清倉並重跑研究。","若裁定只有行為救濟且獨家上限不短於四年，Bull 機率上調到 30%，股價到 150 美元以下才分批反買。","反向條件：若上訴推翻陪審團認定，Bear 機率下修到 20% 並重跑研究。"],"evidence_refs":["regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]},{"axis":"Q3 強勁的持續性","cause":null,"prior_field":null,"side_a":"2026-07-30 CFO 給票務 AOI 中個位數成長，2026-11-05 上修到高個位數；全年粉絲上修到近 1.8 億，2027 預付廣告雙位數成長。","side_b":"Evercore 分析師 2026-11-05 指出前 9 月演唱會 AOI 只 +4%；Q3 北美增幅部分來自體育場檔期後移，事件遞延收入年增由 Q2 的 25% 降到 Q3 的 8%。","ruling":"可調和，屬程度差異。管理層上修屬實，2026-07-30 說的美國粉絲成長集中下半年也兌現，但 Q3 不能外推；CFO 未拆解 Q4 隱含的演唱會 AOI 改善。基準 FY2027 營收成長 8.3%，略低於共識 8.6%。","evidence_level":"高：新聞稿與逐字稿。","settle_metric":"FY2026 演唱會 AOI 年增","if_then":["若 FY2026 演唱會 AOI 年增低於 10%，Bear 機率上調到 35%，不追。","反向條件：若 FY2027 開年事件遞延收入年增回到 15% 以上，Bull 機率上調 3 個百分點。"]},{"axis":"共識每股盈餘方向","cause":null,"prior_field":null,"side_a":"近 3 個月 FY1 修正顯示 +4.55%，字面像上修。","side_b":"實際是虧損由 0.44 美元擴大到 0.46 美元；Q1 財報後一個月共識曾下修 36%。","ruling":"讀為小幅下修。+4.55% 的正負號被負分母反轉，不作動能證據。36% 下修建立在接近零的基期且來自轉載站，只保留方向。","evidence_level":"低：快照可能尚未反映 Q3 財報。","settle_metric":"Q3 財報後首份完整共識快照","if_then":["若下一份快照 FY2027E 每股盈餘下修超過 10%，視為訴訟成本尚未計入，不追。"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"訴訟費用是否一次性","cause":null,"prior_field":null,"side_a":"Q3 AOI 11.79 億美元，管理層以 AOI 呈現本業。","side_b":"前 9 月營業利益減少 3.505 億美元，主因政府調查與訴訟；FY2026E 每股盈餘為負。","ruling":"未證、監測。不採信也不否定一次性歸因，州方賠償與 FTC 訴訟都還沒落地。","evidence_level":"高：10-Q。","settle_metric":"FY2027 政府調查與訴訟費用","if_then":["若 FY2027 這項費用仍超過 1 億美元，一次性歸因不成立，情境改用含訴訟成本的利潤率，不追。"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"全年粉絲近 1.8 億，2027 預付廣告雙位數成長，Harry Styles、Bruno Mars、Oasis、Metallica 已開賣，票務財測上修；賣方 20 買 3 持有 2 賣，均值目標 202 美元，投資人日就在下週。","side_b":"基準五年年化約 6%，救濟未定，Bear 情境 −41%。","ruling":"不買。最強論證成立在需求，不成立在價格。","evidence_level":"中","settle_metric":"股價相對 150 美元、救濟裁定","if_then":["若股價先漲到 215 美元以上而證據未到，不追。","若股價跌到 150 美元以下且未見剝離命令，重跑研究，通過後分批反買。"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭軸：10-K 稱自助售票競爭增加，Eventim 擴張美國；今年新增淨客戶票量逾 2,000 萬張，暫未見惡化。結構軸：live 需求持久，場館管線 25 座以上。","side_b":"其他軸：反壟斷改變票務合約規則，獨家年限、系統開放與費用都在變動。","ruling":"裁決為其他結構變動中，指反壟斷這一軸。","evidence_level":"中","settle_metric":"救濟裁定與票務續約年限","if_then":["若票務 AOI 利潤率連 2 季低於 32%，改判競爭惡化中，減碼。"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]},{"axis":"前份空白欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位都是空值。","side_b":"本次依新格式補上：護城河方向穩定、跑道中等、以品質複利成長為主、情境機率 22／48／30、最大回撤 −35% 至 −55%。","ruling":"前份沒有對照值，不算立場變動。","evidence_level":"高"},{"axis":"估值結論","cause":"方法變動","prior_field":["val"],"side_a":"前份以 PEG 2.6 加五年 80% 分位判為最貴一級。","side_b":"FY2026E 共識每股盈餘為負，PEG 無法算，五年分位也缺資料，改用 EV/S 與情境報酬，判為偏貴。","ruling":"股價只比前份高 3.8%，沒有變便宜，結論變動來自尺度更換。","evidence_level":"中"},{"axis":"評級與價值陷阱判斷","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評級 B，價值陷阱中度。","side_b":"本次評級與價值陷阱判斷都不變。","ruling":"新證據往兩邊走：Q3 票務與粉絲上修支持論點，救濟仍未定，兩者相抵。","evidence_level":"中"},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件，裁決句只寫等 5 或裁決明朗化，數字在前份已缺損。","side_b":"股價≤150 美元，且法院未命令剝離 Ticketmaster；兩者同時成立才重跑研究。","ruling":"本次改成具體價格加事件；法院命令剝離則清倉，不適用重啟。","evidence_level":"中"},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點為空。","side_b":"法院最終救濟命令 Live Nation 剝離 Ticketmaster。","ruling":"Single Thing 由前份第一項風險的分拆部分收斂而來，發生即清倉。","evidence_level":"中"},{"axis":"第一項風險門檻（減碼改清倉）","cause":"新證據","prior_field":["R1"],"side_a":"若 remedy 包含「強制業務分拆」或「強制資產出售」中任一 → R1 觸發 → 立即減倉 2/3","side_b":"法院命令剝離 Ticketmaster 即清倉；DOJ 和解的至多 13 座圓形劇場剝離不觸發減碼，改看票務 AOI 利潤率連 2 季低於 32%。","ruling":"舊文字會被和解的圓形劇場剝離碰到，但該條款是協議、仍待 Tunney Act 核准且規模有限，所以把資產出售拆開，分拆門檻提高到清倉。","evidence_level":"中","evidence_refs":["regulatory_antitrust#1"]},{"axis":"估值回歸門檻（減碼）","cause":"方法變動","prior_field":["R3"],"side_a":"5Y NTM PE 分位 > 90% 持續 4 週 或 同業 PE 收斂 +20% → R3 已實現","side_b":"前瞻 EV/S 高於 1.9 倍（股價約 215 美元）且救濟與場館報酬都沒有新證據，持有者減碼，未持有者不追。","ruling":"每股盈餘為負，NTM 本益比分位失去意義，舊門檻退休，改用 EV/S。","evidence_level":"中"}],"triggers":[{"n":1,"text":"股價回到 150 美元以下，且法院沒有命令剝離 Ticketmaster，重跑研究。","type":"估值rearm","maps_to":"H1","metric":"股價與救濟裁定","threshold":"≤150 美元且無剝離命令","action":"重跑研究，通過後分批反買","source_freq":"每日股價；法院文件不定期","date":null},{"n":2,"text":"法院最終救濟命令剝離 Ticketmaster。","type":"Single Thing","maps_to":"R1","metric":"救濟裁定","threshold":"裁定含剝離","action":"清倉，重跑研究","source_freq":"法院文件、10-Q 法律附註","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#0"]},{"n":3,"text":"投資人日揭露場館投資報酬與夥伴出資比例。","type":"假設驗證","maps_to":"H2","metric":"場館投資報酬、2027 資本支出","threshold":"投資報酬低於 12%，或 2027 資本支出超過 14 億美元","action":"不追；Bear 機率上調到 35% 並更新情境","source_freq":"投資人日簡報","date":"2026-11"},{"n":4,"text":"FY2026 演唱會 AOI 未達雙位數成長。","type":"風險","maps_to":"R3","metric":"FY2026 演唱會 AOI 年增","threshold":"低於 10%","action":"不追","source_freq":"Q4 財報","date":"2027-02"},{"n":5,"text":"票務 AOI 利潤率連 2 季低於 32%。","type":"減碼","maps_to":"R2","metric":"票務 AOI 利潤率","threshold":"連 2 季低於 32%","action":"減碼，未持有者不追","source_freq":"每季分部資料","date":null,"evidence_refs":["channel_business_model_shift#0","channel_business_model_shift#1"]},{"n":6,"text":"前瞻 EV/S 高於 1.9 倍，而救濟與場館報酬都沒有新證據。","type":"減碼","maps_to":"R6","metric":"前瞻 EV/S","threshold":"高於 1.9 倍（股價約 215 美元）","action":"減碼，未持有者不追","source_freq":"每日","date":null},{"n":7,"text":"FTC 訴訟、州方賠償與和解累計現金超過 Bear 假設。","type":"風險","maps_to":"R5","metric":"累計現金賠償","threshold":"超過 10 億美元","action":"停止加碼","source_freq":"10-Q 法律附註","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#1","lawsuit_class_action#2"]},{"n":8,"text":"Q4 財報後複審。","type":"複審日期","maps_to":"H2","metric":"全年粉絲、演唱會 AOI、事件遞延收入","threshold":"定期複審","action":"更新情境與機率","source_freq":"Q4 財報","date":"2027-02"}],"kill_metrics":[{"metric":"法院是否命令剝離 Ticketmaster","bear_threshold":"裁定含剝離","window":"2028 年底前","source":"法院文件、10-Q 法律附註","last_status":"unknown"},{"metric":"票務 AOI 利潤率","bear_threshold":"連 2 季低於 32%","window":"每季","source":"季報分部資料","last_status":"ok"},{"metric":"演唱會 AOI 利潤率","bear_threshold":"連 2 季低於 2.5%","window":"每季","source":"季報分部資料；事實表未涵蓋，資料缺口","last_status":"unknown"},{"metric":"集團 AOI 年增","bear_threshold":"全年低於 8%","window":"FY2027","source":"年度財報；事實表只有 Q3 單季 AOI，資料缺口","last_status":"unknown"},{"metric":"全年粉絲年增","bear_threshold":"低於 5%","window":"FY2027","source":"季報與新聞稿","last_status":"ok"},{"metric":"事件遞延收入年增","bear_threshold":"連 2 季年減","window":"每季","source":"新聞稿","last_status":"ok"},{"metric":"FCF 利潤率","bear_threshold":"全年低於 3%","window":"FY2027","source":"年度財報","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"股價≤150 美元，且法院未命令剝離 Ticketmaster；兩者同時成立才重跑研究。","exec_line":"現在不建倉。股價先漲而證據未到就不追；跌到 150 美元以下且基本面無損，重跑研究，通過後分批買進；法院命令剝離則清倉。"},"reasoning":{"industry":"Q3 營收 101.05 億美元，AOI 11.79 億，GAAP 營業利益 8.92 億，營業利益率 8.8%，AOI 利潤率 11.7%。票務營收約 8.8 億（由年增 7,270 萬、+9% 反推）、AOI 3.157 億；贊助營收 5.057 億、AOI 3.502 億。兩者合計占營收約 14%，占合併 AOI 約 56%，這是演唱會旺季的單季比重，全年結構事實表未涵蓋。其餘約 87 億營收來自演唱會，扣公司費用後 AOI 約 5.1 億。近 12 個月毛利率 25.78%，單季毛利率事實表未涵蓋。產業時鐘在擴張期：2026 全年粉絲近 1.8 億，Q3 單季逾 6,000 萬、近 +20%，CFO 說售完率高於去年、取消率更低。供需判斷為結構性持久，但 2026 有檔期推升，Q3 北美增幅有一部分是世界盃造成的體育場檔期後移。單點依賴不在客戶，10-K 揭露無單一客戶占營收超過 10%；集中度在頭部藝人的巡演檔期，事實表未量化。事實表財務歷史欄顯示 FY2025 淨利 4.96 億美元卻對應稀釋每股盈餘 −0.24 美元，差距成因事實表未涵蓋，所以每股盈餘不能直接拿來判斷本業。","moat":"機制是三段飛輪：演唱會帶票務、場館合約綁票務、粉絲規模帶贊助。Q3 票務 AOI 年增 10%，收費票數 9,830 萬張對 8,910 萬，今年至今新增淨客戶票量逾 2,000 萬張，CFO 也說預期中的二級市場逆風沒有出現，目前沒有失血跡象。縮減端是法律：陪審團 2026-04-15 認定主要票務市場違法，DOJ 和解報導含四年獨家上限、開放第三方使用票務系統、剝離至多 13 座圓形劇場與 15% 費用上限。事實表的法律進度只到約 2026-05，此後狀態未確認，方向判斷的信心偏低。可能看錯的地方：合約年限縮短要到續約才反映在數字，現在的量價數據無法排除這個遞延效應。同業 ROIC 差距事實表未涵蓋，這裡改看票量軸；列表同業利潤率較高，但業態不同，不構成比較。","growth":"成長以量為主，2026 粉絲增量約 2,000 萬人次，人均消費與價其次，併購補場館，淨回購為零。三年共識每股盈餘年複合無法計算，因為 FY2025 基期 −0.24 美元與 FY2026E −0.46 美元都是負值；FY2027E 1.9 到 FY2028E 2.9 美元增 52.6%，是從被壓低的基期反彈，不是成長率。共識營收 FY2026E 285.35 億、FY2027E 309.77 億，年增 13.2% 與 8.6%。內生上界因投入資本缺資料而留空，缺口歸因為無法歸因，依賴re-rate 的疑慮保留，長期信心上限為中。CFO 2026-07-30 說資本支出效益要到 2028 年才明顯，FY2027 成長多半仍靠既有場館與檔期；當時問到 2027 是否再有雙位數粉絲成長，CFO 說還太早，Q3 也沒有給。","governance":"事實表財務歷史欄的 FCF 除以淨利：FY2024 1.17 倍、FY2025 0.61 倍；FY2025 FCF 僅 3.05 億美元、利潤率 1.21%，近 12 個月回到 5.23%。Q3 SBC 4,730 萬美元，占營收 0.47%。2026 資本支出指引 11 至 12 億美元，其中 8 至 8.5 億用於場館擴建。現金去向四分、債務到期與加權利率事實表未涵蓋。CFO 2026-07-30 說會持續拒絕報酬不達標的專案，但夥伴出資比例與投資報酬在 Q3 法說被推到投資人日。2026 年收購金額未揭露，併購報酬無法驗證。","valuation":"EV 449.5 億美元除以 FY2026E 共識營收 285.35 億得 1.58 倍，在四個年度端點中最高；這不是五年分位，五年分位事實表未涵蓋。本益比只能看遠期：FY2027E 92.2 倍、FY2028E 60.4 倍，都建立在被壓低的基期。基準情境終端每股約 238 美元，五年 +36%。短期以 FY2027E 基準營收 309 億、維持 1.58 倍、淨負債約 37 億、股數 238 百萬股估約 190 美元，+8%。敏感度：終端 EV/S 每 0.1 倍約 17 美元，終端營收每 5% 約 13 美元，終端淨負債每 10 億美元約 4 美元。賣方均值目標 191 至 202 美元，比現價高 9% 至 15%，最低 145、最高 222，全距不大；我比賣方保守的地方在救濟風險，賣方目標沒有揭露這部分機率，我也沒有主張市場看錯。共識修正要小心讀：事實表的近 3 月 FY1 修正寫 +4.55%，實際是 −0.44 美元變 −0.46 美元、虧損擴大，正負號被負分母反轉；11-07 的快照也可能尚未反映 Q3 財報。","premortem":"法律進度資料停在約 2026-05，Q3 法說也沒有人問到救濟進度。歷史最大回撤與空方最強數字事實表未涵蓋。法說迴避紀錄有兩組：2026-11-05 CFO 沒有拆解 Q4 演唱會 AOI 的隱含改善，場館併購進度與夥伴資本支出延到投資人日；2026-07-30 對 2027 雙位數粉絲成長、2027 巡演管線對比與 2027 資本支出都沒有給數字。三個反方視角的裁定見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺粉絲與品牌的錢，利潤卡在票務與贊助兩個節點，演唱會負責導流。","moat":"護城河方向為穩定：執行面擴大，定價與合約面被法律縮減，兩者相抵；救濟若擴大就轉為縮減。","growth":"五年後的跑道為中等：場館與國際還有空間，但事實表沒有滲透率，無法給到寬。","capital":"資本配置暫時看不清：稀釋低、沒有回購，錢主要投場館，報酬要等投資人日。","valuation":"現價要求五年營收年複合約 8% 且倍數只小降，才有約 6% 年化；成長我相信，但這個回報付不起救濟風險。","how_wrong":"最可能看錯在救濟力道與時點，不在需求。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價≤150 美元，且法院未命令剝離 Ticketmaster。150 美元對應基準五年年化約 9.7%，也接近 104 週均線 152.64 美元。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":175.25,"week26_return_pct":7.33,"consensus_rev_3m_pct":4.55,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"每股盈餘被訴訟費用壓低，FY2026E 為負，不能當分母；EV 的現金 82.57 億內有事件遞延收入 38.18 億，屬未履約的預收票款，扣除後 EV/S 由 1.58 倍升到 1.71 倍。本次情境沿用 1.58 倍口徑，不把低倍數當便宜的論據。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"投資人日，管理層承諾說明場館時程、資本支出與夥伴出資、AI 影響","impact":"高","watch":"場館投資報酬、2027 資本支出、開幕前費用"},{"date":null,"date_precision":null,"type":"regulatory","event":"法院對州方案的救濟裁定與 JMOL 結果","impact":"高","watch":"是否含剝離 Ticketmaster、獨家年限、賠償金額"},{"date":null,"date_precision":null,"type":"regulatory","event":"DOJ 和解的 Tunney Act 核准","impact":"中","watch":"圓形劇場剝離座數、費用上限範圍"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 Q4 財報","impact":"中","watch":"演唱會 AOI 是否雙位數成長、事件遞延收入"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,583B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期</h2>
<p class="lead">飛輪仍在轉，但法律正在縮減定價與合約面。</p>
<ul class="pts">
<li>機制是三段飛輪：演唱會帶票務、場館長約綁票務、粉絲規模帶贊助。評分上執行面 8、定價面 8，等級 B，方向判為穩定。定價分只反映票務與場館端，演唱會端藝人拿走大部分，法律衝擊只記在威脅扣分，不重複計入定價分。</li>
<li>執行面擴大的證據很具體。今年至今新增淨客戶票量逾 2,000 萬張，Q3 收費票數 +10%，CFO 也說預期中的二級市場逆風沒有出現。目前沒有失血跡象，這是判為穩定而非縮減的主要依據。</li>
<li>縮減端是法律。陪審團 2026-04-15 認定主要票務市場違法，DOJ 和解報導含四年獨家上限、開放第三方使用票務系統、剝離至多 13 座圓形劇場與 15% 費用上限。州方另求分拆 Ticketmaster 與最高約 7 億美元。這條威脅標為紅燈，機率 30%。</li>
<li>競爭威脅標為黃燈，機率 30%。自助售票、場館自售、SeatGeek、Fever 與 Eventim 美國擴張，10-K 也點名大型科技與電商可能進入。但淨客戶票量仍增加，威脅尚未反映在數字上。</li>
<li>可能看錯的地方在遞延效應。合約年限縮短要到續約才進入財報，現在的量價數據排除不了這一點。事實表的法律進度只到約 2026-05，此後的裁定、JMOL 與 Tunney Act 狀態都未確認，方向判斷的信心偏低。</li>
<li>同業 ROIC 差距事實表未涵蓋，所以改看票量軸。列表同業的利潤率較高，但 MSGE 自有單一市場場館，TKO 賺轉播權利金，WMG 在藝人上游，業態不同，不構成直接比較。</li>
</ul>
<h3>二維評分與護城河對數字</h3>
<!-- E5 -->
<h3>§5.F 對手財務深度對照</h3>
<!-- E6 -->
<ul class="pts">
<li>LYV 近 12 個月營業利益率 2.94%，低於 MSGE 的 17.31%、TKO 的 21.71% 與 WMG 的 16.11%，只高於 SPHR 的 −1.68%。SPHR 是重資產場館，可當新場館投入期成本的反面參照。LYV 的 FCF 利潤率 5.23% 也低於 MSGE 的 24.21%。</li>
</ul>
<h3>§5.R 報酬持續期檢核</h3>
<!-- E7 -->
<ul class="pts">
<li>報酬持續期落在低利潤率、高周轉的象限，周轉率事實表未涵蓋，由預收票款模式推定。增量報酬與再投資率都算不出來。粗看 2026 資本支出指引 11 至 12 億美元，約等於 FY2025 營業利益 12.3 億的九成以上，CFO 說效益要到 2028 年才明顯。</li>
</ul>
</section>

```