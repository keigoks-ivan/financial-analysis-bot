你是 stock-analyst v20 的**散文層（prose）agent**，標的 CVS（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVS_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：CVS　日期：2026-11-08　archetype：None　前份裁決：2026-05-18　衛星候選 — turnaround thesis 已 5 季 confirmed (Aetna MBR 84.6% 改善 4.9pp + FY26 guidance raise) + 估值 🟢 便宜 (Fwd PE 11.5x 5Y 25% 分位 + PEG 0.94) + Pure MA ✅ 強勢；但 Oak Street $5.7B 減損結構失敗 + 高槓桿 D/E 1.06 / Net Debt/EBITDA 4.6x + dividend payout 192% 限制長期 compounder 潛力；trap 🟡 觀察期；建議等回測 $88-90 區分批入場｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1671B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（433B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（865B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1406B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（855B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（773B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（944B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2201B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3407B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2721B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1671           3730-5329      5 條（2–6 內）  
s3                  8000         433           5297-7567      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3126          8312-11874      5 條（2–6 內）  
s6                 11000         773          7159-10227      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         944           1789-2556      5 條（2–6 內）  
s10                 5000        2201           1959-2799      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2721           2000-2279      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4593B；至少需散文≈40.41KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−46
−46%
−30%
−30
−12.5%
−6.16
−6.16%
0
0%
0.09%
0.19%
0.20
0.50
0.54
0.75
0.76%
0.88
1%
1
1.07
1.39
1.4
1.49
1.5%
1.65
1.8
2
02
2.0%
2%
2.48%
2.6
2.66
2.7
2.7%
2.74
2.9
3
3%
3.10%
3.17
3.29%
3.58%
3.87%
3.9%
4
4%
04
4.4
5
05
5%
5.32%
5.5%
6
6.1
6.5
6.8%
6.98
7
07
7.30
7.3
7.3%
7.40
7.4
7.46
7.6
7.66
7.8
8
8.00
8%
08
8.04
8.13
8.2
8.20
8.3
8.33
8.54
8.61
8.65
8.8
8.80
9
9.1
9.69
9.7%
9.74
9.78
9.8%
9.82
9.90
9.9
10
10%
10.23
10.3%
10.43
10.6
10.7
10.95
11
11.4
11.5
11.5%
11.9
12
12.0
12.1
12.5%
13%
13
13.2
13.77%
14
14.23%
14.5
15%
15.4%
15.4
16
16.9%
18%
18.1
20
20%
21
23%
23.57
24
25%
26
27.1%
28%
29%
29.9%
29.9
30
30%
30.4%
35
38%
40
40.49
41.94
42
45.2%
45.5
45.7%
49
50
50%
54
57
58
58.4
60
60%
65
70
75
79%
79
83.85
84.6%
86%
87.4%
88
88%
88.5%
89.75%
90
91.3%
95.82
96.8
100%
100
104
105
107
108.9
115
124
129.61
140
150%
150
153.18
155
170.5
188.5
192%
240
340
350
604.10
635
950
2025
2026
2027
2028
20261108
1,083.99
4,020.67
4,200
5,000
9,000
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
{"meta":{"ticker":"CVS","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"CVS Health Corporation"},"oneliner":"CVS 現價約 10 倍獲利，Aetna 修復與藥局成長已兌現，但 Caremark 的 2027 年低點與分拆條件尚未驗證；估值便宜，衰退信號亮三項，等 2027 年 2 月財測與投保結果再決定。","thesis":{"H":[{"id":"H1","text":"Aetna 的 Medicare Advantage 完成重新定價，FY2028 回到 3%～4% 目標利潤率區間。","2y":"FY2028 MA 利潤率至少 3%","5y":"FY2029 至 FY2031 三年滾動 MBR 不高於 88.5%","10y":null,"threshold":"FY2026 全年 MBR ≤89.75%，分部調整後營業利益 ≥54 億美元；FY2027 MBR 再改善","source":"公司季報與法說會","drift_rule":"TTM 分部獲利偏離路徑連 2 季 ≥5% 為削弱，連 3 季 ≥10% 為反轉；同季 MBR 年比轉差連 2 季視同削弱"},{"id":"H2","text":"Caremark 所在的 Health Services 於 FY2027 見底，FY2028 恢復成長。","2y":"FY2027 調整後營業利益至少 70 億美元，FY2028 高於 FY2027","5y":"FY2031 分部獲利高於 FY2027 低點至少 15%","10y":null,"threshold":"FY2027 ≥70 億美元；2028 年銷售季新增高於流失","source":"公司分部資料、第三季法說的銷售季揭露、Drug Channels 年度理賠量","drift_rule":"TTM 分部獲利偏離路徑連 2 季 ≥5% 為削弱，連 3 季 ≥10% 為反轉"},{"id":"H3","text":"現金流足以支撐股息與回購，分拆後兩家公司都維持投資級。","2y":"FY2026 FCF 至少 75 億美元；2028 年上半年完成分拆且兩家都是投資級","5y":"三年累積 FCF 至少 240 億美元，股息未被削減","10y":null,"threshold":"年度 FCF ≥75 億美元；評等不低於 BBB–／Baa3","source":"10-Q、8-K、Form 10 與評等機構公告","drift_rule":"連 4 季 TTM FCF 偏離 ≥5% 為削弱，連 6 季 ≥10% 為反轉；任一家跌破投資級直接反轉"}],"R":[{"id":"R1","text":"醫療成本趨勢持續高於定價假設，MA 修復中斷；Stars 分數下滑也會壓縮後續給付。","h_ref":"H1","clock":"🔥","threshold":"同季 MBR 年比轉差連 2 季則停止加碼；FY2027 全年 MBR 高於 FY2026 則減碼","evidence_refs":["competitive_share_entrants#3"]},{"id":"R2","text":"Caremark 客戶流失延續，2028 年銷售季未回升，FY2027 並非低點。","h_ref":"H2","clock":"🔥","threshold":"FY2027 分部低於 70 億美元，或 2028 年銷售季淨流失","evidence_refs":["end_markets#3","customer_second_source#0","customer_second_source#1","substitute_technology#2"]},{"id":"R3","text":"PBM 監管與反壟斷：FTC、州檢察長與國會針對返利及導流自家藥局施壓。","h_ref":"H2","clock":"🐢","threshold":"正式立法限制返利或強制切割業務則 H2 削弱（保留前份門檻）；來源為 FTC、國會與法院文件","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","regulatory_antitrust#3","major_events#1"]},{"id":"R4","text":"風險調整稽核與 DOJ 調查，影響範圍為約占合併營收 20% 的聯邦政府收入；結案時點未知。","h_ref":"H1","clock":"🐢","threshold":"和解或追繳金額超過約 12 億美元，即 FY2026 FCF 的 10%，或風險調整規則不利變動","evidence_refs":["regulatory_antitrust#0"]},{"id":"R5","text":"證券集體訴訟已部分通過駁回動議，進入證據開示；求償金額事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"集體認證通過且和解不利則持股減半；刑事程序介入則清倉","evidence_refs":["major_events#0","major_events#4","lawsuit_class_action#0"]},{"id":"R6","text":"Oak Street 持續虧損或再度減損；本包沒有損益數字，屬資料缺口。","h_ref":"H1","clock":"🔥","threshold":"FY2027 仍虧損超過 5 億美元視為結構失敗（保留前份門檻）；來源為公司分部揭露","evidence_refs":[]},{"id":"R7","text":"藥局端的關稅、單一來源供應、法規降價與關店壓力侵蝕獲利。","h_ref":"H3","clock":"🐢","threshold":"吸收失敗以 FY2027 分部調整後營業利益低於 65 億美元判斷","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","end_markets#4","channel_business_model_shift#1"]},{"id":"R8","text":"分拆的閒置成本、債務分配與商業協議不如預期。","h_ref":"H3","clock":"🔥","threshold":"任一家預估低於投資級，或年度閒置成本超過調整後營業利益 3%，約 5 億美元","evidence_refs":[]}],"single_thing":{"description":"管理層在 2027 年 2 月至 2028 年 2 月的任一次法說，正式撤回或遞延 FY2028 MA 回到 3%～4% 目標利潤率的時程。","why_fatal":"這是最大的單一敏感度。FY2025 營收 4,020.67 億美元乘 20% 再乘 79%，CMS Medicare 收入約 635 億美元，每 1 個百分點利潤約稅前每股 0.50 美元；修復 3 個百分點約 1.49 美元，是 Health Services 下跌 10% 的 2.7 倍。此收入含非 MA 部分，屬上限估計。","if_happens":"FY2028 EPS 路徑轉向 Bear，獲利與倍數同時下修，五年終點約 58 美元；持股清倉，未持有則取消建倉計畫。","how_monitor":"每季 MBR 同季年比、MA 利潤率的管理層表述、每年 2 月財測、4 月 CMS 費率、10 月 Stars 分數。","probability":"25%（12～24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":9.82,"peg_fy2":1.0,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.39,"FY2026E":8.04,"FY2027E":8.54,"FY2028E":9.69},"fy_end_month":12,"eps_basis":"FY2026E 起為 Koyfin 調整後 EPS 共識（2026-11-07 快照，尚未反映 11-04 財測上修至至少 8.20 美元與 FY2027 至少 8.65 美元）；FY2025A 為 GAAP 稀釋 EPS 1.39 美元，因 FY2025 調整後 EPS 不在本包，兩者口徑不同，不可相除算成長率。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CVS_20261108/scenario.json","archetype":{"primary":"轉機/特殊情境","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"獲利由谷底修復、2028 年上半年分拆、合併營收約兩成來自聯邦政府"},"industry":{"clock_phase":"I","sd_verdict_source":"週期性：MA 利潤率回升來自重新定價與退出虧損市場，屬承保週期修復，到高點後仍可能反轉，因此 Bear 機率取 30%。來源為 2026-08-05 與 2026-11-04 法說及 CMS 2027 年費率報導。","bargaining":{"up":"藥廠限制 340B、部分藥品依賴單一來源，上游議價力強。","down":"CMS 決定費率，雇主與健保客戶持續要求降價，Caremark 利潤受壓。","geo":"藥品與商品多在美國境外製造，關稅影響尚未量化。"},"profit_pool_dir":"五年利潤池序列事實表未涵蓋。定性來看，Joyner 稱三分之二支出來自醫療體系與藥廠，增速為高個位數到低雙位數，利潤主導權在上游。","tam_table":{"expanded":false,"reason":"管理層只給 2 兆美元與 5,000 億美元兩個市場口徑，事實表沒有五年滲透率或利潤池序列；本論點靠利潤率修復，不靠滲透率擴張。"}},"moat":{"mechanism":"三段業務的規模優勢：PBM 採購與給付網路、全國藥局通路、Medicare 承保能力；定價權受政府與大客戶限制。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：同店處方年增 3.9%，MA 於 2026 年回到獲利。定價權縮減：Caremark 理賠量連兩年下滑，2027 年續約留存略低於歷史，客戶持續要求降價。兩者相抵，判定持穩。","peer_na_reason":"同業只有毛利率、營益率與 FCF 利潤率，事實表沒有投入資本與 ROIC，無法計算 ROIC 差距，改用利潤率對照。","threats":[{"level":"🔴","text":"雇主與健保客戶把 PBM 業務拆給多家，改用新創或現金藥局模式，直接挑戰傳統返利架構。實例有 Tyson 改用 Rightway、Blue Shield of California 拆給 Amazon Pharmacy 與 Cost Plus Drugs；目前攻擊者規模仍小，但 Caremark 理賠量已連兩年下滑。","p":35,"evidence_refs":["customer_second_source#0","customer_second_source#1","substitute_technology#2","end_markets#3"]},{"level":"🟡","text":"新創健保、醫療體系自有保險、合資與零售通路持續進入，10-K 預期競爭加劇，但揭露內容未量化。","p":30,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"Aetna 2026 年 Stars 分數下滑，UnitedHealthcare 改善；若差距擴大，會壓縮之後年度的 MA 給付與福利競爭力。","p":30,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"Aetna 退出 ACA 個人交易所，約 100 萬會員需換保，屬客群範圍退縮；公司稱這塊長期沒有改善路徑，短期有利利潤率。","p":"已發生","evidence_refs":["competitive_share_entrants#2","channel_business_model_shift#2"]}],"roic_durability":{"quadrant":"低利益率×高周轉（定性判斷；投入資本事實表未涵蓋，當期 ROIC 無法計算）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是病患，決策者是雇主、健保計畫與 CMS，付款者多為政府與雇主，三角色都成立，用藥難以延後。第三季同店處方年增 3.9%，GLP-1 處方年增 23%。客戶要解決的是可負擔性，PBM 現行做法不一定能延續。"},{"item":"決策層級","level":"🟡","text":"替代發生在合約層：Tyson、Blue Shield of California 換走，CalPERS 換入，顯示大客戶換得動。MA 會員每年可在投保期換計畫。2027 年 Caremark 續約留存率略低於歷史（2026-08-05 法說）。"},{"item":"價值鏈分配","level":"🟡","text":"三分之二支出來自醫療體系與藥廠，增速為高個位數到低雙位數，利潤主導權在上游；340B 受藥廠限制，客戶持續要求降價。正面因素是 CostVantage 讓藥局利潤率結構較一致。"},{"item":"社會容忍度","level":"🔴","text":"PBM 同時面對 FTC、州檢察長與眾議院報告，公司也在挑戰 Arkansas、Tennessee 等州的藥局相關法律；MA 費率與風險調整由 CMS 決定。醫療可負擔性是政治議題，定價上限取決於政治而非經濟。"}],"roiic":"事實表未涵蓋：缺投入資本序列，無法計算增量 ROIC","reinvest_rate":"事實表未涵蓋：只有前九月資本支出 23.57 億美元，缺折舊、營運資金與收購淨額分項","endo_ceiling":null,"formula_note":"內生成長率需要增量 ROIC 與再投資率，兩者輸入都不足，不以推估補值；成長題改用營收成長當代理。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","CVS":14.23,"CI":8.79,"UNH":19.84,"ELV":null,"HUM":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","CVS":3.58,"CI":3.1,"UNH":5.32,"ELV":null,"HUM":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","CVS":3.7,"CI":2.82,"UNH":5.08,"ELV":3.23,"HUM":1.34,"unit":"%"}],"competitors":[{"name":"CI","gm":8.79,"om":3.1,"fcf_margin":2.82,"strategy_note":"Express Scripts 理賠量領先 Caremark，是 PBM 端最直接的份額對手；CVS 目前營益率與 FCF 利潤率略高。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"UNH","gm":19.84,"om":5.32,"fcf_margin":5.08,"strategy_note":"利潤率高於 CVS，2026 年 Stars 分數改善，在 MA 與 PBM 兩端都是最強對手，但 CalPERS 合約由其旗下 Optum Rx 流向 Caremark。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ELV","gm":null,"om":null,"fcf_margin":3.23,"strategy_note":"事實表只有 FCF 利潤率，略低於 CVS，無法比較營益率，判讀有限。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"HUM","gm":null,"om":null,"fcf_margin":1.34,"strategy_note":"以 MA 為主，FCF 利潤率為同業最低，統計期只到 2026 年 6 月，說明 MA 壓力不是 CVS 獨有。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"利潤率修復為主，處方量為輔，回購自 FY2028 起才有實質貢獻，併購不是來源。FY2027 財測下限只假設回購抵銷稀釋。","runway_years":"事實表未涵蓋滲透率，無法計算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊與營運資金分項未進事實表，內生上界無法計算；以 FY1 到 FY2 共識營收成長 2.0% 為量的代理，判定共識 EPS 成長超過可由再投資支撐的部分。","segments":[{"item":"Health Care Benefits","value":"FY2026 調整後營業利益至少 54 億美元；第三季約 9 億美元，年增近 6 億；2027 年預期利潤率再改善，未給金額。"},{"item":"Health Services","value":"第三季調整後營業利益 21 億美元，年增近 3%；FY2027 至少 70 億美元並稱為低點，FY2026 區間本包未揭露。"},{"item":"Pharmacy & Consumer Wellness","value":"FY2026 至少 65 億美元，年增近 8%；FY2027 低個位數成長；第三季同店處方年增 3.9%。"},{"item":"合併","value":"FY2026 調整後營業利益至少 170.5 億美元；FY2027 調整後 EPS 至少 8.65 美元，由約 7.66 美元基期成長約 13%。"}],"decay_signals":[{"signal":"毛利率連兩季年比下滑","lit":false,"evidence":"TTM 毛利率 14.23%，高於 FY2025 的 13.77%；季度序列事實表未涵蓋。"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"Caremark 理賠量 2025 年連續第二年下滑，2027 年會員再減；2026 年份額數字本包沒有。"},{"signal":"主力產品提價後銷量下滑","lit":true,"evidence":"Aetna MA 削減福利並退出部分市場，2026 年會員縮減；2027 年管理層預期小幅成長，尚待投保結果。"},{"signal":"EPS CAGR 顯著高於營收 CAGR","lit":true,"evidence":"共識 EPS 兩年 CAGR 9.8%，FY2 營收成長 2.0%，差 7.8 個百分點。"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"evidence":"FY2024 為 1.4 倍，FY2025 為 4.4 倍。"},{"signal":"SBC／營收超過 5% 且上升","lit":false,"evidence":"年化 SBC 約占 FY2026 營收 0.19%。"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"未見市場萎縮證據，替代模式已列入威脅。"},{"signal":"產業估值倍數近三年系統性下移","lit":null,"evidence":"同業歷史倍數事實表未涵蓋，無法判斷。"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"evidence":"前九月全部資本支出約占 FCF 18%。"},{"signal":"停止投資新產能且收入三年內下滑","lit":false,"evidence":"FY2022 至 FY2025 營收逐年成長，2026 年預期開店多於關店。"}],"trap_rating":"🔴"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"近期成長不靠併購撐，近三年現金去向與回購均價也不在事實表，只能交代 2026 年前九月的現金流向。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"前份記載 Oak Street 減損 57 億美元，2026 年 Oak Street 仍在邁向獲利途中；本包無併購已實現 ROIIC 數字，依減損判為未過。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2026 年前九月只配息，第四季才恢復回購，本包沒有回購均價，無法驗算；10 年期公債殖利率事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"前九月 SBC 6.1 億美元，年化約 8.13 億美元，占市值約 0.76%，低於每年 1.5%；此為金額估算，股數變動事實表未涵蓋。","grade":"過"}]},"valuation":{"basis":"Fwd P/E 與隱含成長；分拆前以合併每股獲利計算","peers":{"expanded":false,"reason":"事實表沒有同業 Fwd P/E，只有利潤率對照，無法建立同級距倍數表，改用自身現值與隱含成長判斷。"},"fwd_pe":10.43,"peg":1.07,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"Fwd P/E 約 10 倍，隱含永續成長約 0%～2.7%，基準情境不靠倍數擴張即可取得雙位數報酬。五年分位與同業倍數事實表未涵蓋，年度端點 0% 分位受 GAAP 低谷扭曲，不作為依據。PEG 1.07 只算合理，便宜的結論主要來自隱含成長。","upside_short_pct":15.4,"upside_mid_pct":29.9},"trap_analysis":{"verdict":"🔴","label":"三項衰退信號亮燈，其中兩項同源於 Aetna 主動重新定價；獲利仍上升，依亮燈數歸為高風險，MA 會員轉為成長可降一級"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"CMS 2027 年費率淨增 2.48%，CEO 也承認低於醫療成本趨勢；第三季 MBR 仍 91.3%，趨勢高於歷史；MA 今年才剛進入獲利區；風險調整有 RADV 稽核與 DOJ 調查。","assumption":"FY2028 前定價足以蓋過成本趨勢，風險調整規則沒有重大不利變動。","consequence":"MA 停在低利潤，Caremark 同步下滑，FY2031 EPS 約 6 美元、倍數 7 倍，股價約 42 美元，五年虧損約 50%。","ruling":"採納為 Bear 的主要路徑，機率 30%。此視角與唯一致命點同源，沿用同一組門檻。","watch":"同季 MBR 年比、CMS 年度費率、Stars 分數、RADV 與 DOJ 進度","evidence_refs":["regulatory_antitrust#0","competitive_share_entrants#3"],"fact_refs":["f_kpi7_medical_benefit_ratio_mb"]},{"view":"論點成功但股東經濟變差","evidence":"Stephen Baxter 追問分拆成本，管理層只說可控，沒有金額；Justin Lake 指出評等機構可能改用負債資本比，管理層未給目標。Moody's 目前只比非投資級高一級。社會容忍度偏低，PBM 面臨 FTC、州檢察長、眾議院報告與多件訴訟。","assumption":"分拆後兩家都維持投資級，商業協議保留現有經濟效益，PBM 轉向淨成本模式不減少利潤。","consequence":"EPS 達標，但獲利被閒置成本、債務重新分配與 PBM 讓利吃掉，可部署資本縮水，倍數停在 10 倍以下。","ruling":"部分採納。分拆方向合理，但成本與資本結構都未量化，基準情境不給分拆溢價，只有 Bull 給。","watch":"Form 10 的債務分配與商業協議、評等機構公告、FTC 和解條款","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","regulatory_antitrust#3","major_events#1"],"fact_refs":["f_net_debt_m"]},{"view":"價格已反映太多","evidence":"WSJ 專欄認為 Medicare 危機已過，容易的獲利改善也已過，現價已反映相當程度的利潤率修復。","assumption":"市場已把 MA 回到目標利潤率算進目前股價。","consequence":"就算修復達成，股價也只賺到獲利成長，不會有倍數擴張。","ruling":"反駁。現價約 10 倍，隱含永續成長約 0%～2.7%，並未反映完整修復；基準情境本來就不靠倍數擴張。賣方目標價高於現價 25%～28%，但資料早於第三季與分拆公告，只作弱證據。","watch":"FY2027 正式財測、第四季法說後的共識修正","evidence_refs":["supply_demand_durability#2"],"fact_refs":["f_fwd_pe_latest","f_consensus_rev_fy1_pct"]}],"max_dd":{"lo":-46,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 95.82 → 本次 83.85（-12.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=95.82","side_b":"本次 price_at_dd=83.85","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 95.82 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 95.82 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 95.82 美元：Bull 價 188.5、Bear 價 58.4，五年期望值 +27.1%，基準年化 6.8%，不對稱比 1.65","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.65。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 95.82 美元：五年期望值 +27.1%，基準年化 6.8%，不對稱比 1.65","side_b":"本次情境、股價 83.85 美元：五年期望值 +45.2%，基準年化 9.7%，不對稱比 2.74","ruling":"再換股價、情境不動：起點價下跌 12.5%，五年期望值多 18.1 個百分點，基準年化多 2.9 個百分點，不對稱比由 1.65 升到 2.74。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","max_dd_pct","p_bull_pct","p_bear_pct","archetype","cycle_position"],"side_a":"前份這九欄都是空值，當時的報告格式沒有要求填寫。","side_b":"本次補齊：護城河趨勢持穩、後段跑道中等、公司類型為轉機或特殊情境、Bear 機率 30%、Bull 機率 20%、回撤範圍 −46%～−30%；循環位置不適用，維持空值；裁決與角色由程式算出。","ruling":"差異來自欄位新增，不代表基本面改變，不能解讀成趨勢變化。","evidence_level":"格式差異，不需外部證據","settle_metric":"下次更新時改與本次填入的值比對","if_then":[],"evidence_refs":[]},{"axis":"陷阱風險與訊號等級","cause":"新證據","prior_field":["trap","signal"],"side_a":"前份：價值陷阱觀察中，訊號等級 B，建議回測 88～90 美元分批進場。","side_b":"本次：衰退信號亮三項，陷阱風險升為高，訊號等級降為 C。","ruling":"採本次。現價 83.85 美元已低於前份進場區，但新增問題在基本面，不在價格，所以不沿用價位條件。三項中兩項來自 Aetna 主動重新定價，在會員與 Caremark 合約數字出來前，不把主動調整當成已證實。","evidence_level":"中：一手法說加第三方年度統計","settle_metric":"2027 年 MA 會員變化、FY2027 Health Services 調整後營業利益、2028 年銷售季淨增減","if_then":["若 2027 年 2 月揭露 MA 會員較 2026 年底成長，衰退信號減為兩項，重跑分析後才建倉，首筆不超過組合 2%","若 FY2027 Health Services 低於 70 億美元，代表信號證實為對，持股減碼一半，未持有則不建倉"],"evidence_refs":["end_markets#3","customer_second_source#0","customer_second_source#1"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份 95.82 美元、Fwd P/E 11.5 倍，評為便宜。","side_b":"本次 83.85 美元、FY1 共識口徑 10.43 倍，仍評為便宜。","ruling":"結論不變。股價下跌 12.5% 是倍數下降的主因；前份分母換算約 8.33 美元，高於目前 FY1 共識 8.04 美元，可能是不同年度口徑，兩次倍數不宜直接比較。","evidence_level":"高：價格與共識快照","settle_metric":"FY2027 正式財測對應的倍數","if_then":["若股價在 2 月前續漲而事件未驗證，不追"],"evidence_refs":[]},{"axis":"H1 的 MBR 門檻","cause":"方法變動","prior_field":["H1.threshold","R1.threshold"],"side_a":"FY2026 全年 MBR ≤86%；連 2 季 >86% 削弱、>88% 反轉。","side_b":"FY2026 全年 MBR ≤89.75%；同季 MBR 年比轉差連 2 季則停止加碼；FY2027 全年 MBR 高於 FY2026 則減碼。","ruling":"舊門檻建立在第一季 84.6% 上，而第一季是全年最低點，2026-08-05 法說指出第一季到第四季 MBR 增幅略高於 950 bps。第二季 87.4%、第三季 91.3% 會誤觸反轉，但第三季實際年比改善約 150 bps，所以改用同季年比與全年區間。","evidence_level":"高：公司財報與法說","settle_metric":"FY2026 全年 MBR 與 FY2027 同季年比","if_then":["若同季 MBR 年比轉差連 2 季，停止加碼","若 FY2027 全年 MBR 高於 FY2026，減碼一半"],"evidence_refs":[]},{"axis":"Oak Street 門檻降位","cause":"方法變動","prior_field":["H2.threshold","R2.threshold"],"side_a":"H2 獨立假設：FY2026 虧損收窄至 5 億美元內；FY2027 仍虧損超過 5 億美元則反轉。","side_b":"降為第六項風險，門檻與資料來源保留：FY2027 仍虧損超過 5 億美元視為結構失敗，減碼三分之一。","ruling":"本包沒有 Oak Street 損益，只有管理層定性說法，標為資料缺口。降位是因為它不再決定獲利路徑的主要方向，不代表問題已解決。","evidence_level":"低：缺分部損益","settle_metric":"FY2027 Oak Street 損益揭露","if_then":["若 FY2027 虧損超過 5 億美元或出現第二次減損，減碼三分之一"],"evidence_refs":[]},{"axis":"Single Thing","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點，欄位為空。","side_b":"管理層在 2027 年 2 月至 2028 年 2 月的任一次法說，正式撤回或遞延 FY2028 MA 回到 3%～4% 目標利潤率的時程。","ruling":"Single Thing 選 MA 目標利潤率時程，因為每股敏感度最大：每 1 個百分點約稅前每股 0.50 美元，修復 3 個百分點約 1.49 美元，是 Health Services 下跌 10% 的 2.7 倍。","evidence_level":"中：CMS 收入含非 MA 部分，屬上限估計","settle_metric":"法說對目標利潤率時程的表述、MA 利潤率揭露","if_then":["若時程被正式撤回或遞延，持股清倉，未持有則取消建倉計畫"],"evidence_refs":[]},{"axis":"重新進場與退出門檻","cause":"方法變動","prior_field":["rearm_trigger","kill_metrics"],"side_a":"前份未設重新進場條件與退出指標，只有回測 88～90 美元分批進場的文字。","side_b":"重新進場改為 2027 年 2 月法說確認 FY2027 EPS 財測不低於 8.65 美元且 MA 會員成長；EPS 財測低於 8.65 美元則減碼，MA 目標時程撤回則清倉。","ruling":"改用事件條件，因為要解決的是基本面不確定，不是價格。","evidence_level":"高：公司已公布的財測下限","settle_metric":"FY2027 正式財測與 2027 年投保結果","if_then":["若 FY2027 財測低於 8.65 美元，減碼一半","若 MA 目標時程撤回，清倉"],"evidence_refs":[]},{"axis":"Caremark 是否在 2027 年見底","cause":null,"prior_field":null,"side_a":"2026-11-04 Newman 與 Prem Shah：2027 年至少 70 億美元是低點，340B 之後不再是需要討論的議題，2028 年銷售季有信心，會員流失反映客戶自身決策。","side_b":"Drug Channels 顯示理賠量連兩年下滑；2026-08-05 Prem Shah 承認留存率略低於歷史，Newman 拒絕量化 340B；第三季仍只說比重更小，沒有金額。","ruling":"不可裁決至 2027 年第三季法說。管理層的歸因不採信也不否定，列為未證；若 FY2027 不到 70 億美元，或 2028 年銷售季淨流失，此歸因視為錯誤。","evidence_level":"中：一手法說與第三方統計，未來數據尚不存在","settle_metric":"FY2027 分部調整後營業利益、2028 年銷售季淨增減","if_then":["若 FY2027 低於 70 億美元，減碼一半","若 FY2027 不低於 70 億美元且 2028 年銷售季淨增，解除此項風險並可加碼至組合 4%"],"evidence_refs":["end_markets#3","customer_second_source#0","customer_second_source#1"]},{"axis":"藥局與 PBM 整合價值","cause":null,"prior_field":null,"side_a":"過去 20 年的策略主軸是藥局與 PBM 垂直整合，Michael Cherny 也指出 Maintenance Choice 等產品來自這層關係。","side_b":"2026-11-04 Joyner：不需要營運上的整合，商業協議就能保留；藥局一直在防火牆後以公平交易方式談判。","ruling":"可調和。藥局獨立運作的說法可信，留下的 Aetna、Caremark 與專科藥局整合才是利潤核心。但協議條款與閒置成本都還沒有數字，基準情境不給分拆溢價。","evidence_level":"中：只有管理層說法","settle_metric":"Form 10 揭露的商業協議年限、定價與閒置成本","if_then":["若閒置成本超過調整後營業利益 3%，減碼三分之一"],"evidence_refs":[]},{"axis":"FY2026 EPS 分母品質","cause":null,"prior_field":null,"side_a":"FY2026 財測至少 8.20 美元，較期初上修逾 1 美元，FY2027 至少 8.65 美元。","side_b":"2026-08-05 Newman 說明 FY2026 基準要排除前期發展與已退出業務，當時 8.00 美元中點對應 7.46 美元；同幅度扣除後，本次基期約 7.66 美元。","ruling":"8.20 到 8.65 表面成長 5.5%，淨化後約 13%。估值用淨化基期 10.95 倍檢查，便宜結論不變，但 8.20 美元不能當作常態獲利。","evidence_level":"高：管理層逐項說明","settle_metric":"2027 年 2 月公布的基期調整項目","if_then":["若淨化基期低於 7.40 美元，停止加碼"],"evidence_refs":[]},{"axis":"FY2026 現金品質","cause":null,"prior_field":null,"side_a":"營運現金流財測由至少 115 億美元上修至至少 155 億美元，一季增加 40 億。","side_b":"同期 EPS 只上修 0.20 美元，約 2.6 億美元；管理層歸因營運資金與付款時點，隱含第四季營運現金流僅約 1.8 億。","ruling":"FY2026 FCF 約 124 億美元不當常態，殖利率以 FY2025 的 7.3% 與 FY2026 的 11.5% 作為上下界。","evidence_level":"高：現金流量表與財測","settle_metric":"FY2027 營運現金流與 FCF","if_then":["若 FY2027 FCF 低於 75 億美元，減碼三分之一"],"evidence_refs":[]},{"axis":"藥局營收與獲利","cause":null,"prior_field":null,"side_a":"第三方摘要稱 Pharmacy & Consumer Wellness 營收下滑，歸因法規降價、學名藥與給付壓力，商業保費下降 16.9%。","side_b":"2026-11-04 法說：該分部調整後營業利益年增逾 10%，同店處方年增 3.9%。","ruling":"可調和，藥價下降會壓低營收，處方量與利潤結構仍可改善。該摘要為轉述，本包沒有分部營收原文，不採用其數字，只保留監測。","evidence_level":"低：二手轉述","settle_metric":"10-Q 分部營收與 FY2027 分部營業利益","if_then":["若 FY2027 分部營業利益低於 65 億美元，減碼三分之一"],"evidence_refs":["end_markets#4"]},{"axis":"Stars 分數","cause":null,"prior_field":null,"side_a":"Fierce 報導 2026 年 MA Stars 中 Aetna 分數下滑，UnitedHealthcare 改善。","side_b":"2026-11-04 Steven Nelson 稱 2027 給付年擁有領先的 Stars 分數。","ruling":"可調和，分數下滑後仍可能排名靠前。本包沒有實際分數與同業排名，列為資料缺口，不把領先的說法當成優勢證據。","evidence_level":"低：缺分數明細","settle_metric":"2027 年 10 月 CMS 公布的 Stars 分數","if_then":["若 Aetna 下一輪 Stars 再降，停止加碼"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：Caremark 理賠量下滑，新進者與替代模式增加。","side_b":"結構轉好：2027 年 MA 費率淨增 2.48%，優於預告的 0.09%，業者維持定價紀律，但持久性未證。其他結構變數：PBM 反壟斷、藥品關稅與 CVS 分拆。","ruling":"雙向拉鋸。MA 承保週期轉好，PBM 的競爭與監管轉差，來源為 CMS 費率報導與 Drug Channels 年度統計。","evidence_level":"中","settle_metric":"CMS 2028 年費率、2028 年銷售季結果","if_then":[],"evidence_refs":["end_markets#3","regulatory_antitrust#3"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"約 10 倍獲利、連續 8 季超出並上修財測；8.65 美元下限已含 340B 與會員流失，且只假設回購抵銷稀釋，回購恢復的增量還沒計入；現價也低於前份進場區。","side_b":"11-04 公布的 Caremark 低點與分拆尚未進賣方模型，兩份共識快照變動為 0；第一個驗證點只差三個月，衰退信號也可能在當時減少。","ruling":"選擇等到 2 月。等待的代價是可能少賺約 15% 的短線重估，換來的是確認投保結果與正式財測。","evidence_level":"中","settle_metric":"2027 年 2 月第四季法說","if_then":["若股價在 2 月前續漲而事件未驗證，不追","若股價下跌而 FY2027 下限與 MBR 趨勢未變，分批反買，單筆不超過組合 1%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2026 全年 MBR 與 Health Care Benefits 獲利達標","type":"假設驗證","maps_to":"H1","metric":"FY2026 全年 MBR、分部調整後營業利益","threshold":"MBR ≤89.75%；營業利益 ≥54 億美元","action":"達標則維持 H1，未達標則停止加碼","source_freq":"季報，每季","date":"2027-02"},{"n":2,"text":"MA 目標利潤率時程被正式撤回或遞延","type":"Single Thing","maps_to":"H1","metric":"法說對 FY2028 目標利潤率的表述","threshold":"撤回或遞延 3%～4% 目標時程","action":"持股清倉，未持有則取消建倉計畫","source_freq":"法說，每季","date":"2027-02 至 2028-02"},{"n":3,"text":"2028 年 PBM 銷售季結果","type":"假設驗證","maps_to":"H2","metric":"銷售季新增與流失合約","threshold":"新增高於流失","action":"成立則可加碼至組合 4%，不成立則減碼一半","source_freq":"法說，每年","date":"2027-11","evidence_refs":["end_markets#3"]},{"n":4,"text":"Health Services 跌破管理層設定的下限","type":"風險","maps_to":"R2","metric":"FY2027 分部調整後營業利益","threshold":"低於 70 億美元","action":"減碼一半","source_freq":"季報，每季","date":"2028-02","evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"n":5,"text":"證券集體訴訟進展","type":"風險","maps_to":"R5","metric":"集體認證與和解金額、程序性質","threshold":"集體認證通過且和解不利；或刑事程序介入","action":"前者持股減半，後者清倉","source_freq":"10-Q 與法院文件，每季","date":null,"evidence_refs":["major_events#4","major_events#0","lawsuit_class_action#0"]},{"n":6,"text":"重新進場條件","type":"估值rearm","maps_to":"R1","metric":"FY2027 正式財測、MA 會員變化","threshold":"EPS 財測不低於 8.65 美元，且 MA 會員較 2026 年底成長","action":"重跑完整分析後才建倉，首筆不超過組合 2%","source_freq":"第四季法說，每年","date":"2027-02"},{"n":7,"text":"Caremark 低點獲得驗證","type":"加碼","maps_to":"H2","metric":"FY2027 分部營業利益、2028 年銷售季","threshold":"分部不低於 70 億美元，且銷售季淨增","action":"加碼至組合 4%","source_freq":"法說，每季","date":"2027-11"},{"n":8,"text":"獲利下限失守","type":"減碼","maps_to":"H1","metric":"FY2027 調整後 EPS 財測、全年 MBR","threshold":"EPS 財測低於 8.65 美元，或全年 MBR 高於 FY2026","action":"減碼一半","source_freq":"季報，每季","date":"2027-02"},{"n":9,"text":"分拆後資本結構失守","type":"清倉","maps_to":"H3","metric":"兩家公司長期評等","threshold":"任一家預估低於 BBB–／Baa3，且股息被削減","action":"清倉","source_freq":"Form 10 與評等公告，事件型","date":"2028-Q2"},{"n":10,"text":"藥局端吸收成本失敗","type":"風險","maps_to":"R7","metric":"FY2027 分部調整後營業利益","threshold":"低於 65 億美元","action":"減碼三分之一","source_freq":"季報，每季","date":"2028-02","evidence_refs":["reg_tariff_export#0","reg_tariff_export#3","geo_supply_chain#1"]},{"n":11,"text":"第四季法說後複審","type":"複審日期","maps_to":"H1","metric":"正式財測、投保結果、分拆進度","threshold":"依第 1、6、8 項判斷","action":"重跑完整分析","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"Health Care Benefits 全年 MBR","bear_threshold":"FY2027 高於 FY2026","window":"FY2027","source":"公司季報與法說","last_status":"ok"},{"metric":"FY2027 調整後 EPS 財測","bear_threshold":"低於 8.65 美元","window":"2027-02 起每季","source":"公司財測","last_status":"ok"},{"metric":"Health Services 調整後營業利益","bear_threshold":"FY2027 低於 70 億美元，或 FY2028 未高於 FY2027","window":"FY2027 至 FY2028","source":"公司分部資料","last_status":"unknown"},{"metric":"Caremark 2028 年銷售季","bear_threshold":"淨流失","window":"2027 年下半年","source":"公司法說","last_status":"unknown"},{"metric":"Oak Street 損益","bear_threshold":"FY2027 虧損超過 5 億美元（目前資料缺口）","window":"FY2027","source":"公司分部揭露","last_status":"unknown"},{"metric":"年度 FCF","bear_threshold":"低於 75 億美元","window":"每年","source":"10-K 現金流量表","last_status":"ok"},{"metric":"分拆後長期評等","bear_threshold":"任一家低於 BBB–／Baa3","window":"至 2028 年上半年","source":"Form 10 與評等機構公告","last_status":"ok"}],"evidence_dismissed":[{"ref":"major_events#3","reason":"內容只描述代工廠 Diamond Wipes 的單一品項包裝不符規定，沒有 CVS 受影響營收、賠償責任或裁罰資料，無法連到公司損益或任何假設。"},{"ref":"product_recall_warning#0","reason":"與痔瘡濕巾召回是同一事件的重複紀錄，同樣沒有 CVS 受影響金額或責任歸屬資料。"},{"ref":"major_events#5","reason":"召回由代工廠 KC Pharmaceuticals 發起，涉及多家通路品牌，報導沒有 CVS 的銷售額或責任資料，無法區分為 CVS 自身問題。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把分拆與 Caremark 的 2027 年低點一起解讀成獲利見頂，用約 10 倍定價；但 8.65 美元下限已含 340B 與會員流失，且只假設回購抵銷稀釋，回購恢復的每股增量未計入。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟢', moat_trend='→', week26=-6.16, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"2027 年 2 月第四季法說確認 FY2027 調整後 EPS 財測不低於 8.65 美元，且 MA 會員較 2026 年底成長","exec_line":"條件成立後重跑完整分析再決定，不直接下單，首筆不超過組合 2%；條件成立前不追，若基本面未變而股價先跌才分批反買，單筆不超過 1%。"},"reasoning":{"industry":"第三季合併營收 1,083.99 億美元，調整後營業利益 41.94 億美元，利益率 3.87%，GAAP 利益率 3.29%。調整後營業利益分部為 Health Care Benefits 約 9 億、Health Services 約 21 億、Pharmacy & Consumer Wellness 逾 16 億美元（2026-11-04 法說）。FY2026 財測為調整後 EPS 至少 8.20 美元、營收至少 4,200 億美元、Health Care Benefits 至少 54 億、Pharmacy & Consumer Wellness 至少 65 億、合併調整後營業利益至少 170.5 億美元。單點依賴：聯邦政府約占合併營收 20%，其中 CMS 的 Medicare 合約占 79%（FY2025 10-K），這是集中度風險，不是護城河證據。產業位於復甦期，依據是 2027 年 MA 費率淨增 2.48%、業者收縮福利與退出虧損市場後利潤率回升，但醫療成本趨勢仍高於歷史水準。分拆後，Aetna、Caremark、專科藥局、Oak Street 與 Signify 留在 CVS Health，零售藥局、郵購、MinuteClinic 與 Health100 成為 CVS Pharmacy，預計 2028 年上半年完成。可能看錯的地方：分部利潤結構會因分拆後的商業協議改變，條款尚未公布。","moat":"機制是規模：Caremark 的採購與給付網路、約 9,000 家門市與逾 29% 零售處方市占、Aetna 的 Medicare 承保能力。執行力給 7 分，依據是連續 8 季超出並上修財測、PCW 連三年成長、MA 於 2026 年回到獲利。定價權給 5 分，依據是 MA 費率由 CMS 決定、Caremark 持續對客戶降價、340B 受藥廠限制。方向證據：Caremark 理賠量連兩年下滑，2027 年會員再減，因此不能標為擴大；零售同店處方年增 3.9%，因此也不標為縮減。TTM 營益率 3.58% 高於 CI 的 3.10%、低於 UNH 的 5.32%，FCF 利潤率排序相同。反例：CalPERS 五年合約由 Optum Rx 轉給 Caremark，2026 年銷售季新增約 60 億美元，代表 PBM 競爭力並未全面流失。若 2028 年銷售季再度淨流失，趨勢應改為縮減。","growth":"FY1 到 FY3 共識 EPS 由 8.04 美元升至 9.69 美元，兩年 CAGR 9.8%；FY2 共識營收只比 FY1 多 2.0%。FY2025 調整後 EPS 不在本包，無法算三年 CAGR，GAAP 基期 1.39 美元被減損壓低，也不能外推。投入資本與折舊不在事實表，內生上界無法計算；以營收成長 2.0% 當代理，缺口約 7.8 個百分點，主要歸因利潤率擴張，其次是 FY2028 起的淨回購，沒有併購因素。人口老化支撐需求，但零售處方市占已逾 29%，Caremark 理賠量下滑；Health100 與價值導向照護尚無營收數字，不算已證實的第二曲線。反例：若分拆後 Health100 或 Oak Street 揭露可驗證的營收與獲利，跑道應上調。","governance":"前九月 FCF 129.61 億美元，由營運現金流 153.18 億減資本支出 23.57 億而來；配息約 26 億，沒有回購，剩餘約 104 億留在資產負債表，還債與現金的拆分事實表未涵蓋。FY2026 營運現金流財測至少 155 億美元，隱含第四季只有約 1.8 億，管理層承認含營運資金與付款時點效果，所以 FY2026 不能當常態。FY2025 FCF／淨利 4.4 倍、FY2024 為 1.4 倍，都受 GAAP 淨利偏低影響。股息 TTM 每股約 2.66 美元，占 FY2026 GAAP 財測 6.98 美元的 38%，前份擔心的 192% 配息率不再成立。淨負債 604.10 億美元，含租賃。評等為 Fitch BBB（負面）、Moody's Baa3（穩定）、S&P BBB（穩定）。可能看錯的地方：分拆後債務如何分配尚未揭露，Moody's 評等只比非投資級高一級。","valuation":"FY1 共識口徑 Fwd P/E 10.43 倍，公司財測下限 8.20 美元口徑 10.23 倍，FY2027 下限 8.65 美元口徑 9.69 倍。以 10% 要求報酬粗算，FY2027 盈餘殖利率 10.3% 隱含永續成長約 0%；改用 FY2025 FCF 殖利率 7.3%，隱含約 2.7%，10% 是假設值。PEG 為 10.43÷9.78＝1.07，屬合理；若用淨化基期約 7.66 美元，兩年 CAGR 12.5%、倍數 10.95 倍，PEG 0.88。短線上檔以 FY2027 基準 EPS 8.80 美元乘 11 倍得 96.8 美元，上漲 15.4%；中期以 FY2028 基準 9.90 美元乘 11 倍得 108.9 美元，上漲 29.9%。賣方目標價均值 105～107 美元，區間 79～140 美元，都早於第三季財報與分拆公告。Trailing P/E 9.74 倍隱含 EPS 8.61 美元，高於 FY2026 財測，口徑不明，不採用。26 週報酬 −6.16%，RSI 40.49，沒有過熱。可能看錯的地方：若 MA 修復中斷，FY2028 EPS 落到 8 美元以下，10 倍就不便宜。","premortem":"衰退信號亮三項：Caremark 理賠量下滑、MA 重新定價後會員縮減、EPS 成長高於營收 7.8 個百分點。三項中後兩項同源於 Aetna 主動調整，獲利仍在上升，尚不是典型的獲利衰退，但依亮燈數歸為高風險。反方向的錯誤是這些信號只是調整的副作用，等待會錯過約 15% 的短線重估。2026-08-05 法說有四個問題未正面回答：340B 規模、340B 抵銷路徑、商業險利潤率與長期目標比較、每張處方毛利，其中 340B 到第三季仍只給方向。未決法律事項金額本包沒有，歷史最大回撤事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"CVS 賺的是美國醫療支出經過三個節點的差價：Aetna 的承保利差、Caremark 與專科藥局的藥品管理費和採購差價、零售藥局的處方毛利。現階段獲利增量卡在 Aetna 的 Medicare 重新定價，下一個卡點是 Caremark 的 2028 年銷售季。","moat":"護城河持穩，評為 C 級。零售藥局與 Aetna 的執行力在改善，Caremark 的議價力在下降，兩邊相抵。","growth":"後段跑道中等。成長主要靠 Aetna 利潤率修復與回購，量的成長只有低個位數，第二條成長曲線尚未證實。","capital":"現金創造強，資本配置紀錄中等。併購報酬未過，回購尚無紀錄，股權稀釋可控；今年前九月的現金主要留在資產負債表改善槓桿，第四季才恢復回購。","valuation":"現價只要求 FY2027 之後每股獲利大致零到低個位數成長，我相信做得到，估值便宜；但便宜的前提是 MA 修復能維持。","how_wrong":"最可能看錯的地方，是把 MA 的週期性修復當成永久，並低估 Caremark 的結構性讓利。"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把分拆與 Caremark 的 2027 年低點一起解讀成獲利見頂，用約 10 倍定價；但 8.65 美元下限已含 340B 與會員流失，且只假設回購抵銷稀釋，回購恢復的每股增量未計入。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月第四季法說：FY2027 調整後 EPS 財測不低於 8.65 美元，且 MA 會員較 2026 年底成長；本次等事件，不等價位。","trap":"🔴","val":"🟢","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"轉機/特殊情境","price_at_dd":83.85,"week26_return_pct":-6.16,"consensus_rev_3m_pct":1.39,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 財測 8.20 美元含約 0.54 美元前期發展與已退出業務項目，淨化後約 7.66 美元，倍數 10.95 倍。改用 FY2027 下限 8.65 美元當前瞻錨，倍數 9.69 倍，便宜結論不受影響，所以不列為爭點。GAAP 財測 6.98 美元對應 12.0 倍。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季法說：FY2027 正式財測、投保結果與回購進度","impact":"高","watch":"EPS 財測是否不低於 8.65 美元，MA 會員是否成長"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"CMS 公布 2028 年 MA 最終費率，時點比照今年 4 月","impact":"高","watch":"淨增幅與醫療成本趨勢的差距"},{"date":"2027-10","date_precision":"month","type":"regulatory","event":"CMS 公布下一輪 MA Stars 分數，時點比照往年 10 月","impact":"中","watch":"Aetna 分數與 UnitedHealthcare 的差距"},{"date":"2027-11","date_precision":"month","type":"other","event":"第三季法說揭露 Caremark 2028 年銷售季結果，時點為預估","impact":"高","watch":"新增與流失的淨額"},{"date":"2028-Q2","date_precision":"quarter","type":"other","event":"分拆預計於 2028 年上半年完成，須先通過 Form 10 與董事會最終核准","impact":"高","watch":"兩家的債務分配、評等、商業協議與閒置成本"}],"_projected_from":"v19"}
```
