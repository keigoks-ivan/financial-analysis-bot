你是 stock-analyst v20 的**散文層（prose）agent**，標的 ALV（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ALV　日期：2026-10-24　archetype：None　前份裁決：2026-05-24　B｜衛星候選｜分批進場（建議第一批 50% 現價，第二批待 Pure MA ✅ 或拉回 W52 $115 區間加碼）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1613B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（446B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（983B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1089B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（919B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（419B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（875B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2090B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4364B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2171B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1613           3771-5387      5 條（2–6 內）  
s3                  8000         446           5288-7554      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2991          8406-12009      5 條（2–6 內）  
s6                 11000         419          7407-10581      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         875           1837-2625      5 條（2–6 內）  
s10                 5000        2090           2037-2910      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2171           2000-2829      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4117B；至少需散文≈40.88KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−53%
−50%
−50
−45%
−35%
−35
−27%
−9%
−6.6%
−5%
−4.5%
−1.9%
−1.23
−1.1%
0%
0
0.43%
0.5%
0.63
0.64%
0.74
0.75
0.78
0.84
0.87
0.97
1%
1
01
1.08
1.2
1.24
1.3%
1.3
1.42
1.5
1.55%
1.9
1.9%
2%
2
2.0
2.28
2.3%
2.4%
2.4
2.5
3
3%
3.2%
3.32
3.58%
3.6%
3.67%
3.7
4%
04
4
4.5%
5
5%
5.15
5.48%
5.81%
6
06
6%
6.3%
6.6%
6.8%
6.83%
7%
07
7
7.52%
7.6
7.6%
7.8
8%
8
8.3%
9
9.1%
9.18%
9.4%
9.5%
9.55
9.6
9.7%
9.89
9.9
9.9%
10%
10
10.2%
10.3%
10.32
10.4%
10.5%
10.5
10.8
11%
11
11.1
11.11
11.3
11.4
11.4%
11.5
11.5%
11.59
11.8
12
12%
12.5
13
13%
13.19
13.5
14%
14
14.5
15.2
15.4
16.8
17%
17
18%
18.4%
18.5
18.9
19%
19
19.3%
20
20%
22%
23
24
24%
25
25%
26%
26
26.93
27%
29%
29
30%
30
33%
34%
35%
36.6%
40%
42
44%
45%
46.2%
47%
49
50
51%
52
52%
55%
58%
59
60%
65%
67%
70%
70
72
78%
79
80
80%
90
97.2
100%
100
111
114
114.67
115
120
122.73
125
130
131
135
137
148
150%
150
160
166
170
180
249.75
1997
2009
2020
2021
2022
2023
2024
2025
2026
2027
2028
2030
2031
2033
7282
600699
20261024
1,000
1,869
4,000
9,500
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
{"meta":{"ticker":"ALV","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Autoliv, Inc."},"oneliner":"全球被動安全龍頭（份額約44%），靠回購與利益率撐每股盈餘；12%利益率目標未兌現、2027原物料壓力延續，預估本益比約11倍屬合理，等1月底2027指引再決定","thesis":{"H":[{"id":"H1","text":"靠中國本土車廠與印度單車內容，Autoliv持續跑贏全球輕型車產量並守住約44%份額","2y":"2026、2027年有機成長領先全球產量至少1.5個百分點（2026指引約2個百分點）","5y":null,"10y":"全球被動安全份額維持約44%以上","threshold":"年度領先至少1.5個百分點；本土車廠銷售成長領先中國產量至少10個百分點","source":"季度財報新聞稿、S&P Global Mobility產量、10-K份額揭露","drift_rule":"領先幅度連2季低於門檻削弱，連3季轉為落後反轉"},{"id":"H2","text":"調整後營業利益率由約10.5%走向11%以上，12%為上檔","2y":"FY2027至少11%","5y":"FY2028–FY2031平均至少11.5%","10y":null,"threshold":"FY2026至少10.3%、FY2027至少11%、FY2028至少11.5%","source":"公司指引與季度新聞稿；土耳其關廠自2027起年省約4,000萬美元","drift_rule":"TTM利益率連4季低於路徑值5%以上（約低於10.4%）削弱，連6季低於10%以上（約低於9.9%）反轉"},{"id":"H3","text":"現金轉換率至少80%支撐每年約4～5%股數縮減，槓桿不超過1.5倍","2y":null,"5y":"2031年稀釋股數不超過約59百萬股（現約72百萬股）","10y":null,"threshold":"年度股數減少至少4%、淨負債÷EBITDA不超過1.5倍、現金轉換率至少80%","source":"10-Q股數、季報槓桿比率與現金轉換率","drift_rule":"連4季回購金額低於前4季一半或槓桿超過1.5倍削弱；回購暫停或股利刪減反轉"}],"R":[{"id":"R1","text":"原物料與物流成本回收不足，利益率指引再下修","h_ref":"H2","clock":"⚡","threshold":"2026全年調整後營業利益率低於10.2%，或2026第四季低於12%","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","cyclical_inventory_price_position#0"]},{"id":"R2","text":"中國本土車廠垂直整合、亞洲新競爭者與Joyson擴產侵蝕份額或價格","h_ref":"H1","clock":"🔥","threshold":"中國區有機成長連4季落後中國產量，或本土車廠超越幅度連2季低於5個百分點","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","customer_second_source#1","cyclical_supply_discipline_capacity#4"]},{"id":"R3","text":"法律與稅務負債：ARC氣體產生器集體訴訟、BMW反壟斷求償、德國民事訴訟、墨西哥稅務爭議","h_ref":"H3","clock":"🐢","threshold":"累計提列或和解超過3億美元，或NHTSA對Autoliv產品下強制召回令","evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#0","regulatory_antitrust#2","lawsuit_class_action#1"]},{"id":"R4","text":"汽車產量衰退與車廠臨時停產，EMEA產能過剩","h_ref":"H2","clock":"⚡","threshold":"全球輕型車產量連2季年減超過5%，或EMEA有機成長連2季落後產量超過3個百分點","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_inventory_price_position#1","supply_demand_durability#0","major_events#0","geo_supply_chain#1"]},{"id":"R5","text":"供應鏈與出口管制：半導體、推進劑缺料或關稅無法轉嫁","h_ref":"H2","clock":"🔥","threshold":"關稅回收率連2季低於70%，或財報揭露缺料停產","evidence_refs":["reg_tariff_export#1","geo_supply_chain#0"]}],"single_thing":{"description":"2027-01-29第四季法說公布的2027調整後營業利益率指引中位數低於11%","why_fatal":"利益率是EPS最大的單一敏感項：營收約111億美元下每差1個百分點，稅後約0.78億美元、每股約1.08美元，約占FY1 EPS一成；指引低於11%等於12%路徑延後，EPS成長只剩回購","if_happens":"基準EPS路徑下修約一成，熊市機率升到40%；不建倉，已持有者減碼一半","how_monitor":"2026第四季實際利益率（全年10.5%隱含約14%）、2027指引、原物料補償進度與工程收入","probability":"約35%（管理層已說2027原物料壓力與2026相當）"}},"appendix_a":{"growth_durability":5,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":9.89,"peg_fy2":0.87,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":9.55,"FY2026E":10.32,"FY2027E":11.59,"FY2028E":13.19},"fy_end_month":12,"eps_basis":"FY2025A為GAAP稀釋EPS（年報）；FY2026E–FY2028E為Koyfin共識，多為調整後口徑，基期口徑混用可能略高估三年成長率"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收綁汽車產量、毛利率約19%、2009年營業利益曾年減78%；但全球份額約44%、調整後投入資本報酬約24%"},"industry":{"clock_phase":"IV","sd_verdict_source":"供需持久性：需求是週期性（輕型車產量2026年約−1.9%、2027預估+1.55%）疊加結構性單車內容成長；供給端Autoliv關閉土耳其廠收縮EMEA產能，Joyson在匈牙利擴產，供給可逆性中等；判週期性，下一段反轉向上但幅度小","bargaining":{"up":"不直接買原物料，漲價經供應鏈傳導（2026毛衝擊估約1.2億美元）；半導體與感測器受出口管制影響，上游議價中等","down":"車廠議價強：前五大客戶約44%，關稅回收約八成，物流成本幾乎無法轉嫁，價格調整細到零組件逐項談","geo":"中國本土車廠占Autoliv中國銷售由2022年22%升到本季58%；比亞迪自製被動安全，日韓系車廠多由集團關係企業供貨"},"profit_pool_dir":"利潤池往中國本土車廠與印度移動；Autoliv跟得上量，但本土車廠業務的利潤率管理層不揭露","tam_table":{"expanded":false,"reason":"被動安全已是成熟市場（Autoliv份額約44%、前氣囊數量年增約1.3%），論點不靠滲透率或新品類；成長來源在成長題以量、單車內容、回購拆解"}},"moat":{"mechanism":"規模加安全認證：每個車型平台要通過碰撞驗證並承諾整個車型週期供貨，約44%全球份額帶來成本與工程攤提優勢；換供應商通常只在新車型招標時發生","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大（生產力提升、利益率高於同業），定價力持平（關稅回收約八成、原物料與物流部分吸收）；管理層份額目標為守住，中國區份額33%低於歐美","peer_na_reason":"同業ROIC事實表未涵蓋，以營業利益率與FCF利潤率差距代理；ZF未上市不在表內","threats":[{"level":"🟡","text":"中國本土車廠垂直整合（比亞迪自製）與日韓系車廠由集團關係企業供貨，限制Autoliv在成長最快客群的份額與價格","p":"30%","evidence_refs":["competitive_share_entrants#2","customer_second_source#1"]},{"level":"🟡","text":"中國、韓國、印度預期有更多本土與國際競爭者進入，可能帶來降價與毛利下滑","p":"30%","evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"Joyson在匈牙利擴產而EMEA整體產能過剩（Autoliv自己關閉土耳其廠），歐洲價格壓力上升","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#4","supply_demand_durability#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是乘客、決策者是車廠、付款者是買車的人，三者都成立；安全配備受法規與碰撞評等強制，是需要不是想要，印度單車內容上升也來自安全規範（2026-10-23法說）"},{"item":"決策層級","level":"🟡","text":"替代性要在單一車型平台招標這一層看：一旦定點通常供貨整個車型週期，期間換供應商要重做碰撞驗證；但每次新車型都重新招標，最大單一合約只占約2%，轉換成本只在週期內有效"},{"item":"價值鏈分配","level":"🟡","text":"車廠拿走大部分議價：關稅只回收約八成、物流成本難轉嫁、原物料補償有落後；比亞迪自製證明大型車廠有能力把這一環收回自己做，Autoliv毛利率約19%反映這個分配"},{"item":"社會容忍度","level":"🟡","text":"安全產品社會支持度高，但不容許聯合定價與品質瑕疵：曾因歐盟反壟斷認罪，BMW仍在德國求償約9,500萬歐元，ARC氣體產生器集體訴訟未結；價格上限受這兩條約束"}],"roiic":"約17%（以調整後投入資本報酬24%扣30%稅率代理；增量值事實表未涵蓋）","reinvest_rate":"約14%（FY2023–FY2025（淨利−自由現金流）÷淨利）","endo_ceiling":2.4,"formula_note":"投入資本報酬24%為公司調整後口徑（2026第三季法說CFO），扣約30%稅率得稅後約17%；再投資率以三年（淨利−自由現金流）÷淨利＝（79＋166＋19）÷1,869百萬美元≈14%代理資本支出減折舊加營運資金增加；內生成長≈17%×14%≈2.4%"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","ALV":19.22,"7282.T":null,"600699.SS":18.12,"MGA":14.71,"LEA":6.86,"unit":"%"},{"metric":"營業利益率","ALV":9.18,"7282.T":null,"600699.SS":5.81,"MGA":5.48,"LEA":3.67,"unit":"%"},{"metric":"FCF 利潤率","ALV":6.83,"7282.T":null,"600699.SS":0.64,"MGA":7.52,"LEA":3.58,"unit":"%"},{"metric":"研發密度","ALV":4.09,"7282.T":null,"600699.SS":5.49,"MGA":null,"LEA":null,"unit":"%"}],"competitors":[{"name":"7282.T","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"period":"TTM ending 2026-06-30（2季加總）"},{"name":"600699.SS","gm":18.12,"om":5.81,"fcf_margin":0.64,"rd_intensity":5.49,"period":"TTM ending 2026-03-31（4季加總）"},{"name":"MGA","gm":14.71,"om":5.48,"fcf_margin":7.52,"rd_intensity":null,"strategy_note":"車身與座椅零件為主，非直接被動安全對手，只作利潤率參考","period":"TTM ending 2026-06-30（4季加總）"},{"name":"LEA","gm":6.86,"om":3.67,"fcf_margin":3.58,"rd_intensity":null,"strategy_note":"座椅與電子為主，利潤率最低，只作利潤率參考","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（輕型車產量約0～2%）＋單車內容（約1～2%，印度與前中央氣囊）＋回購（約5%/年）；價格補償不算成長","runway_years":"不適用滲透率換算：份額約44%已成熟，成長來自單車內容與守住份額","runway_post_y5":"🟡","endo_ceiling_basis":"報酬持續期推導：稅後投入資本報酬約17%×再投資率約14%≈2.4%","segments":{"expanded":false,"reason":"公司只有被動安全單一業務，氣囊與安全帶的分產品利潤率未揭露，組合變化不是決定利潤的主因；區域組合影響已在毛利率與議價段處理"},"decay_signals":["毛利率連兩季年減：亮（第二季含土耳其減損與補償回沖約80基點，第三季18.4%對19.3%）","EPS成長高於營收成長逾5個百分點：亮（2022–2025年EPS年化約25%、營收約7%；前瞻約11%對約2.4%）","核心市占近12個月縮減：未亮（全球仍超越產量，但EMEA第三季落後3.7個百分點要追蹤）","FCF／淨利連兩年低於0.75：未亮（2024約0.74、2025約0.97）","提價後銷量下滑：未亮","SBC占營收超過5%：未亮（股數五年減約18%）","TAM萎縮或被替代：未亮（前氣囊數量2026–2033年增約1.3%）","產業倍數三年系統性下移：事實表未涵蓋","維護性資本支出占FCF超過60%：事實表未涵蓋","停止投資新產能且營收下滑：未亮（蕪湖新氣囊廠2027投產）"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近12個月無併購；股東回報以回購和股息為主，已在本題理由與計分項列出"},"capalloc_grade":"A","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近12個月無併購完成（8-K未見併購完成項目），不適用","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"第二、三季回購均價約125美元（2億÷160萬股、1.5億÷120萬股），對FY1共識EPS 10.32的盈餘殖利率約8.3%；10年期公債殖利率事實表未涵蓋，需高於約6.3%才不過，判過但未直接驗證","grade":"過"},{"year":"—","action":"sbc_dilution","rationale":"近五年流通股數約減18%（2026-10-23法說CFO），淨稀釋為負；SBC金額事實表未涵蓋","grade":"過"}]},"valuation":{"basis":"預估本益比（FY1共識）為主，PEG與自身年度端點為輔；同業本益比事實表未涵蓋","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率、沒有同業本益比，不能拿來當估值錨"},"fwd_pe":11.11,"peg":0.97,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"預估本益比11.1倍、年度端點分位約45%（只有4點，非五年分位）、帳面PEG約0.97看似便宜；但三年EPS成長約11%裡有5～6個百分點來自回購，扣掉後實質PEG約1.9；基準情境年化約11%屬中等，故判合理而非便宜","upside_short_pct":13,"upside_mid_pct":25},"trap_analysis":{"verdict":"🟡","label":"兩項衰退信號亮燈：毛利率連兩季年減、每股盈餘成長遠高於營收成長"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2009營業利益年減78%、利益率1.3%；2020第二季銷售年減51%並轉虧、取消股利；2022首季調整後利益率3.2%；2025第四季部分車廠無預警停產調庫存","assumption":"汽車景氣只是溫和下行（2026全球產量約−1.9%）","consequence":"若2027–2028出現實質衰退，EPS掉三成以上、本益比壓到8倍，股價可腰斬","ruling":"採納：放進熊市情境30%機率與最大回撤−35%～−50%；與唯一致命點部分重疊（都經由利益率），衰退是外部觸發，2027利益率指引是能觀察的關口","watch":"S&P Global Mobility季度產量、車廠停產公告","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_inventory_price_position#1"]},{"view":"論點失敗","evidence":"單一小零件缺貨可迫使產品停產且可能持續很久；半導體與感測器受出口管制；固定價合約下關稅可能無法轉嫁","assumption":"供應鏈中斷是一次性","consequence":"類似2021–2022晶片短缺時利益率掉到6.8%","ruling":"部分採納：已含在熊市利益率假設中，不另加機率","watch":"關稅回收率、財報中缺料停產揭露","evidence_refs":["geo_supply_chain#0","reg_tariff_export#1"]},{"view":"論點成功但股東經濟變差","evidence":"中國本土車廠占中國銷售58%且仍升；比亞迪自製、Autoliv只供氣體產生器；管理層不談本土車廠利潤率；BMW求償約9,500萬歐元、ARC集體訴訟未提列","assumption":"跟著本土車廠成長的營收和原有營收一樣賺錢","consequence":"份額守住、營收成長，但利益率卡在10～11%，法律支出吃掉部分回購","ruling":"採納：基準情境利益率用11%，不給12%","watch":"中國區利益率（若揭露）、法律提列","evidence_refs":["competitive_share_entrants#2","customer_second_source#1","regulatory_antitrust#2","major_events#1"]},{"view":"價格已反映太多","evidence":"全年利益率指引收窄到下緣；第三季稀釋EPS年減6.8%；TD Cowen降至持有、目標價148降到137；三年共識EPS成長約11%裡回購占5～6個百分點","assumption":"預估本益比11倍就是便宜","consequence":"若利益率停在10.5%，EPS成長只剩回購，11倍只是合理價","ruling":"採納：估值判合理而非便宜，不追價","watch":"FY2共識EPS修正方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3","capital_markets_pricing#1"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 122.73 → 本次 114.67（-6.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=122.73","side_b":"本次 price_at_dd=114.67","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 122.73 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 122.73 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 122.73 美元：Bull 價 249.75、Bear 價 97.2，五年期望值 +36.6%，基準年化 7.6%，不對稱比 3.32","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.32。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 122.73 美元：五年期望值 +36.6%，基準年化 7.6%，不對稱比 3.32","side_b":"本次情境、股價 114.67 美元：五年期望值 +46.2%，基準年化 9.1%，不對稱比 5.15","ruling":"再換股價、情境不動：起點價下跌 6.6%，五年期望值多 9.6 個百分點，基準年化多 1.5 個百分點，不對稱比由 3.32 升到 5.15。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"利益率能否走向12%","cause":null,"side_a":"管理層：第三季9.7%優於先前預期，第四季隱含約14%，12%中期目標不變，新技術可帶來更大幅生產力提升（2026-10-23法說，CEO）","side_b":"全年指引由10.5～11%收窄到下緣10.5%，年初以來新增成本逆風170～180基點，2027原物料壓力與2026相當，物流成本難轉嫁（同場CEO與CFO）；2026-07-17法說已把獲利節奏改為偏後段","ruling":"不可調和，採B側當基準：情境基準利益率用約11%而非12%；依據是全年兩度靠第四季補償與工程收入撐場","evidence_level":"公司指引與法說原話","settle_metric":"2027-01-29公布的2027利益率指引與2026第四季實際利益率","if_then":["若2027指引≥11%且2026全年實際≥10.3%→首倉2%","若第四季實際<12%或2027指引<10.5%→不建倉，熊市權重升到40%","反向：若指引前股價先漲到130美元以上→不追"],"evidence_refs":["capital_markets_pricing#0","cyclical_inventory_price_position#0"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"股息殖利率約2.3%加回購約6%，總股東回報約8%；預估本益比11.1倍；前份第二批加碼價位（52週均線約115美元）已到","side_b":"第四季全球產量預估年減4.5%，下行期營業利益曾一年跌78%；等三個月看指引的機會成本約2%","ruling":"不採納現在買：等事件的代價小，下行尾巴長","evidence_level":"財報與法說","settle_metric":"2027-01-29指引","if_then":["若指引前股價跌到100美元以下且第四季利益率≥13%→分批反買首倉1%","若指引達標→照首倉2%執行"]},{"axis":"中國超越幅度與份額論點","cause":"新證據","side_a":"前份：中國區超越產量超過30個百分點、警戒線低於10個百分點；2030全球份額≥47%","side_b":"本季中國區整體只超越約1個百分點（本土車廠超越近20個百分點、對全球車廠銷售年減約29%）；2026-10-23法說CEO說全球份額目標是守住","ruling":"前份中國警戒線本季已觸及一次；本土車廠占比升到58%後，整體超越幅度被全球車廠在華衰退拖累，改用中國區相對產量連續落後季數與本土車廠超越幅度判讀；份額擴張到47%的論點撤回，改成守住約44%","evidence_level":"新聞稿與法說","settle_metric":"中國區有機成長減中國產量的連續季數","if_then":["若中國區連4季落後產量→減碼一半","若本土車廠超越幅度回到20個百分點以上且中國區轉正→恢復份額論點"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"利益率門檻","cause":"新證據","side_a":"前份：FY2026≥10.5%、FY2027≥11.5%、FY2028≥12%","side_b":"本次：FY2026≥10.3%、FY2027≥11%、FY2028≥11.5%","ruling":"2026指引收窄到下緣、2027原物料壓力延續，門檻下調約半個百分點；12%目標管理層仍維持，但不當基準","evidence_level":"公司指引"},{"axis":"估值論點","cause":"方法變動","side_a":"前份第三個論點押本益比重評到13～14倍","side_b":"本次不把重評當論點，改成現金轉換支撐的縮股","ruling":"同業本益比事實表未涵蓋，無法佐證13倍合理值；報酬改由EPS複利與股息構成，不依賴估值重評","evidence_level":"方法"},{"axis":"綜合評級","cause":"價格變動","prior_field":["signal"],"side_a":"前份評級B，股價122.73美元","side_b":"本次評級B，股價114.67美元（約−6.6%）","ruling":"股價下跌、FY1共識三個月上修1.9%讓估值變便宜一些，但同期利益率指引收窄到下緣、衰退信號亮兩項，兩邊抵銷，評級維持B","evidence_level":"價格與共識"},{"axis":"估值結論","cause":"新證據","prior_field":["val"],"side_a":"前份判便宜（以13倍為合理本益比）","side_b":"本次判合理","ruling":"扣除回購後EPS成長約6%，實質PEG約1.9；2026利益率指引落在下緣、第三季稀釋EPS年減6.8%、FY2共識小幅下修、TD Cowen降評","evidence_level":"新聞稿與賣方評等","evidence_refs":["capital_markets_pricing#1"]},{"axis":"價值陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份判陷阱風險低","side_b":"本次判中等","ruling":"毛利率第二、三季連續年減，EPS成長遠高於營收成長，兩項衰退信號亮燈","evidence_level":"財報"},{"axis":"首次填入欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位是空值（前份結論文字為分批進場）","side_b":"本次首次填入：護城河方向持平、五年後跑道中等、歸類循環型、位於中循環、最大回撤−35%～−50%、多頭20%／熊市30%","ruling":"這些變動來自新流程首次要求填欄，不代表基本面轉變；結論由分批進場轉為等指引，原因見利益率那條","evidence_level":"方法"},{"axis":"加碼條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件，只寫第二批待週線均線轉強或拉回52週均線115美元區間加碼","side_b":"2027-01-29指引調整後營業利益率≥11%且2026全年實際≥10.3%","ruling":"加碼條件由價格錨改成事件錨：利益率路徑未決時不設進場價；價格已到前份加碼區但證據沒到","evidence_level":"方法"},{"axis":"減碼與清倉門檻","cause":"方法變動","side_a":"前份未設減碼或清倉量化門檻，只有風險表警戒值","side_b":"新設：全年利益率<9.5%、全年有機超越<0、中國區連4季落後、ARC提列或和解>3億美元或強制召回令→清倉、槓桿>2倍","ruling":"把前份風險警戒值改成可執行的減碼與清倉條件","evidence_level":"方法"},{"axis":"Single Thing","cause":"方法變動","side_a":"前份未設唯一致命點（Single Thing為空）","side_b":"2027-01-29公布的2027調整後營業利益率指引中位數低於11%","ruling":"Single Thing改成數學上最大的敏感項：利益率每差1個百分點，EPS約差一成","evidence_level":"方法"},{"axis":"ARC訴訟門檻","cause":"方法變動","side_a":"前份：累積準備金超過5億美元或強制召回超過1,000萬件","side_b":"累計提列或和解超過3億美元，或NHTSA對Autoliv產品下強制召回令→清倉","ruling":"3億美元約等於半年回購、市值約3.6%，足以打斷縮股論點；召回改看有沒有強制令，因件數揭露時點落後","evidence_level":"方法","evidence_refs":["lawsuit_class_action#0"]},{"axis":"產業態勢三軸","cause":null,"side_a":"競爭軸惡化：Joyson在匈牙利擴產、中國垂直整合、亞洲新進者","side_b":"結構軸轉好：EMEA關廠收縮產能、印度與中國單車內容上升、關稅回收約八成；其他軸：反壟斷民事求償、ARC訴訟、出口管制","ruling":"雙向拉鋸：份額守得住，但定價力沒有變強","evidence_level":"10-K、新聞稿、產業報導","evidence_refs":["cyclical_supply_discipline_capacity#4","supply_demand_durability#0"]}],"triggers":[{"n":1,"text":"2027調整後營業利益率指引中位數低於11%","type":"Single Thing","maps_to":"H2","metric":"2027全年調整後營業利益率指引","threshold":"低於11%","action":"不建倉；已持有者減碼一半","source_freq":"年度（第四季法說）","date":"2027-01-29"},{"n":2,"text":"利益率路徑獲確認","type":"估值rearm","maps_to":"H2","metric":"2027利益率指引與2026全年實際","threshold":"指引≥11%且2026實際≥10.3%","action":"首倉2%","source_freq":"年度","date":"2027-01-29"},{"n":3,"text":"全年有機成長領先全球產量幅度不足","type":"假設驗證","maps_to":"H1","metric":"全年有機成長減全球輕型車產量","threshold":"低於1個百分點","action":"停止加碼","source_freq":"年度","date":"2027-01-29"},{"n":4,"text":"中國區連續落後產量","type":"風險","maps_to":"R2","metric":"中國區有機成長減中國輕型車產量","threshold":"連2季低於0","action":"減碼一半","source_freq":"季","date":null,"evidence_refs":["competitive_share_entrants#3","customer_second_source#1"]},{"n":5,"text":"第四季利益率未達隱含水準","type":"減碼","maps_to":"R1","metric":"2026第四季調整後營業利益率","threshold":"低於12%（全年指引隱含約14%）","action":"減碼一半","source_freq":"季","date":"2027-01-29","evidence_refs":["cyclical_inventory_price_position#0"]},{"n":6,"text":"ARC氣體產生器案惡化","type":"清倉","maps_to":"R3","metric":"累計提列或和解金額；NHTSA召回令","threshold":"超過3億美元或強制召回令","action":"清倉","source_freq":"季報或有負債附註","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":7,"text":"首倉後價格回落且利益率改善","type":"加碼","maps_to":"H3","metric":"股價與季度利益率","threshold":"股價≤100美元且季度利益率年增","action":"分批加碼到4%","source_freq":"季","date":null},{"n":8,"text":"估值先走而利益率沒跟上","type":"減碼","maps_to":"H2","metric":"FY2共識預估本益比","threshold":"≥13倍（約150美元）且利益率仍低於11%","action":"減碼到2%","source_freq":"日","date":null},{"n":9,"text":"汽車產量實質衰退","type":"風險","maps_to":"R4","metric":"全球輕型車產量年增率","threshold":"連2季低於−5%","action":"停止加碼","source_freq":"S&P Global Mobility月報","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","geo_supply_chain#1"]},{"n":10,"text":"上海投資人日檢查中國業務與中期目標","type":"複審日期","maps_to":"H1","metric":"本土車廠業務利潤率與中期目標","threshold":"是否更新12%目標與中國份額","action":"重跑研究","source_freq":"一次","date":"2027-04-26"}],"kill_metrics":[{"metric":"全年調整後營業利益率","bear_threshold":"2027全年低於9.5%","window":"FY2027","source":"公司財報新聞稿","last_status":"ok"},{"metric":"全年有機成長減全球輕型車產量","bear_threshold":"低於0個百分點","window":"FY2026–FY2027","source":"財報新聞稿與S&P Global Mobility","last_status":"ok"},{"metric":"中國區有機成長減中國輕型車產量","bear_threshold":"連4季落後","window":"2026Q4–2027Q3","source":"財報新聞稿","last_status":"warning"},{"metric":"ARC氣體產生器案累計提列或和解","bear_threshold":"超過3億美元或NHTSA強制召回令","window":"持續","source":"10-Q與10-K或有負債附註","last_status":"ok"},{"metric":"淨負債÷調整後EBITDA","bear_threshold":"高於2.0倍","window":"任一季","source":"季報槓桿比率","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":"4%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-1.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等2027-01-29法說：2027調整後營業利益率指引≥11%且2026全年實際≥10.3%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"2027-01-29指引調整後營業利益率≥11%，且2026全年實際≥10.3%","exec_line":"條件成立後首倉2%；下一季利益率年增再加到4%；任一清倉條件觸發即出場"},"reasoning":{"industry":"第三季淨銷售26.93億美元（年減0.5%），有機−1.1%，優於全球輕型車產量−1.9%；毛利率18.4%（去年同期19.3%，約一半來自去年一次性供應商補償），調整後營業利益率9.7%、GAAP 9.4%（2026-10-23新聞稿與法說）。營收分部：區域上美洲34%、中國20%、亞洲（不含中國）20%、EMEA 26%（第三季，含暑休）；產品上氣囊與方向盤約67%、安全帶約33%（Moody's 2026-06）。收錢方式是車型平台定點後依實際產量出貨，沒有保底量，原物料與關稅靠事後補償談判回收。單點依賴：無單一客戶超過營收10%，最大單一合約約2%，前五大約44%、前十大約70%，客戶集中度不構成單點風險；真正的單點是汽車產量景氣。產業時鐘判收縮期：全球輕型車產量2026年預估−1.9%、第四季−4.5%、中國第四季−9%，2027預估+1.55%。全年指引：有機約0%、調整後利益率約10.5%、營運現金流約12億美元。","moat":"份額由1997年27%升到2025年約44%，歐洲52%、美洲47%、中國33%（10-K、Moody's）。同業利潤率（TTM）：Autoliv營業利益率9.18%、FCF利潤率6.83%；Joyson 5.81%、0.64%；Magna 5.48%、7.52%；Lear 3.67%、3.58%，差距是規模優勢的可觀察證據，同業ROIC事實表未涵蓋。方向判持平：執行面擴大（直接人工生產力持續改善，第三季在新增成本逆風下利益率優於預期），定價面持平（關稅回收約八成、原物料與物流部分自行吸收）。2026-10-23法說CEO說全球份額目標是守住現有份額，不是擴張；中國本土車廠占比快速上升，Autoliv跟得上，但比亞迪自製、只向Autoliv買氣體產生器。當期報酬屬低利益率×高周轉，四檢查點見下，內生成長上界約2.4%。","growth":"成長拆解：量（全球輕型車產量長期約0～2%）＋單車內容（資本市場日框架1～2%，2026-07-17法說CEO說仍成立，但組合效應讓含量成長沒發揮全部潛力）＋回購（每年縮股約5%）；價格以補償為主，不是成長來源。共識三年EPS：FY2025A 9.55到FY2028E 13.19，年化約11.4%（Koyfin共識，家數事實表未涵蓋；基期是GAAP、共識多為調整後口徑，可能略高估）。內生上界約2.4%，缺口約9個百分點，歸因：淨回購約5～6個百分點、利益率由約10%走向12%約3～4個百分點，大致可完全歸因，不靠估值重評。營收共識FY2026約111億、FY2027約114億美元（年增約2.4%）。衰退信號亮兩項，長期成長性與陷阱風險都判中等。","governance":"FCF／淨利：2023約0.84、2024約0.74、2025約0.97；第三季自由營運現金流1.24億美元、現金轉換率80%（目標至少80%）。現金去向：資本支出約占營收4%（2026指引由低於5%下調，管理層說是時點與優先高回收專案），股息每季約0.63億美元，回購第二季2億、第三季1.5億美元，近12個月回饋股東約7.6億美元、近五年29億美元並縮股約18%；無併購。槓桿1.3倍（上季1.2倍），淨負債約18.9億美元，剩餘回購授權約19億美元。營運槓桿：第三季營收年減0.5%、調整後營業利益年減3%，差2.5個百分點，未到壓縮警戒。SBC金額事實表未涵蓋，但股數淨減少。","valuation":"現價114.67美元，FY1共識EPS 10.32，預估本益比11.1倍；FY2共識11.59對應約9.9倍。歷史本益比只有4個年度端點，現值分位約45%，不是五年分位，五年分位留空。PEG以三年共識EPS年化約11.4%計約0.97，但其中5～6個百分點靠回購，扣掉後成長約6%，實質PEG約1.9。FY1共識近三個月上修1.9%，最新一次FY2下修0.43%。股息殖利率約2.3%。賣方目標價均值約131～135美元（都是第三季財報前資料）。基準情境（利益率約11%、本益比11.5倍）含股息年化約11%，屬中等；多頭要靠利益率到12%加本益比回到13.5倍。","premortem":"空方最強數字：2009年營業利益年減78%、2020年第二季銷售年減51%並轉虧且取消股利、2022首季調整後利益率只剩3.2%。法說迴避紀錄：2026-07-17法說不揭露訂單、不談本土車廠利潤率，準備稿說中國本土車廠占中國銷售55%、問答說成65%，前後不一（以本季新聞稿58%為準）。未決訴訟：ARC氣體產生器集體訴訟未提列且無法估計區間，BMW求償約9,500萬歐元，墨西哥稅務爭議在初期。最大回撤估−35%～−50%，依據見情境假設；各視角反證見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺全球車廠被動安全採購的錢（氣囊與方向盤約三分之二、安全帶約三分之一）；錢卡在車型平台定點與成本補償談判兩個節點，量跟著汽車產量走","moat":"護城河持平：規模與認證讓Autoliv利益率高於同業3～5個百分點，份額長期升到約44%，但管理層目標已改成守住份額，中國垂直整合壓著定價力","growth":"五年後跑道中等：份額已約44%、前氣囊數量年增約1.3%，成長靠單車內容與守份額；電池安全開關等新業務還在起步，不算第二條曲線","capital":"資本配置良好：現金轉換達標、持續縮股、槓桿低，回購價格對應的盈餘殖利率約8%","valuation":"現價要的是利益率守住10.5%、回購每年縮股約5%，換年化約10%的報酬，這個我信；要多賺得靠12%利益率兌現，這部分現價沒有給折扣，判合理不判便宜","how_wrong":"最可能看錯在：汽車景氣下行與利益率目標落空同時發生，回購撐不住每股盈餘"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等2027-01-29法說：2027調整後營業利益率指引≥11%且2026全年實際≥10.3%","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"A","archetype":"循環/商品","price_at_dd":114.67,"week26_return_pct":-1.23,"consensus_rev_3m_pct":1.88,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY1分母含工程收入時點與關稅補償，但沒有單一大額一次性；FY2025基期為GAAP、共識為調整後口徑，差異小，不構成爭點。短期上檔以FY2027基準EPS 11.3×11.5倍計，中期以FY2028基準EPS 12.5×11.5倍計"},"catalysts":[{"date":"2027-01-29","date_precision":null,"type":"guidance","event":"第四季財報與2027全年指引","impact":"高","watch":"2027調整後利益率指引是否至少11%"},{"date":"2027-04-26","date_precision":null,"type":"other","event":"上海投資人日（兩天，含上海車展）","impact":"中","watch":"本土車廠業務利潤率與中期目標是否更新"},{"date":"2028-06","date_precision":"quarter","type":"capacity","event":"土耳其工廠完全關閉，年省約4,000萬美元達滿額","impact":"低","watch":"重組費用是否超出約1.42億美元"}],"_projected_from":"v19"}
```
