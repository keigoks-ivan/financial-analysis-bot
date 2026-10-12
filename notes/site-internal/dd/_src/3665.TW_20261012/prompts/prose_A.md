你是 stock-analyst v20 的**散文層（prose）agent**，標的 3665.TW（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3665.TW_20261012/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：3665.TW　日期：2026-10-12　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1393B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（457B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1005B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1225B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1389B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（648B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（933B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1994B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3376B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2401B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1393           3925-5607      5 條（2–6 內）  
s3                  8000         457           5280-7543      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3619          7967-11381      5 條（2–6 內）  
s6                 11000         648          7246-10352      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         933           1797-2567      5 條（2–6 內）  
s10                 5000        1994           2104-3006      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2401           2000-2599      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4985B；至少需散文≈40.02KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−60
−57%
−43%
−40%
−40
0
0.14
0.5
0.54
0.64
0.65
0.655%
0.655
0.75
0.78
1
1.5%
1.82
2
02
3
03
3.92
4
5%
5
05
5.38%
5.4%
5.6
06
6%
6
6.77
6.77%
6.8%
7
07
7%
8
08
8%
8.5
09
9
10%
10
10.46%
10.6%
11
11.4
12%
12
13%
14
15%
15.28
16
17%
17.2%
17.22%
17.3%
17.4%
17.44%
17.52%
18
18%
18.4
20%
20.49%
20.5%
21
22
24
24.4%
25%
25
25.65%
26
26.77%
26.8%
28
28%
28.5%
28.77%
30%
30
30.73%
31%
31.7%
31.73%
31.912
32
34
34.01
34.08
35
35%
37%
37.6%
38
39.2%
39.9%
40%
40
42
43.3
45
46.33
47%
49
52.6%
53%
54.5
60%
69.25
70
70%
72
75%
78
80
85%
88
90
91%
95
96%
96
100
100%
105
115
125
127.97
128
148
150%
160
163
164.67
176
192
220
224
232.81
245
301
448
800
2020
2024
2025
2026
2027
2028
2355.0
3023
3665
20261012
1,010
2,000
2,355
2,450
3,203
3,360
3,870
5,000
5,184
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
{"meta":{"ticker":"3665.TW","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"貿聯-KY（BizLink）"},"oneliner":"AI 資料中心銅纜、電源與光纖互連的製造商，前 9 月營收年增四成、Q2 獲利創單季新高；共識 2027 年 EPS 年增 85% 偏樂觀，銅被光替代、客戶二供與增資稀釋是三大折價，基準情境五年年化約一成。","thesis":{"H":[{"id":"H1","text":"AI 機櫃互連與電源需求讓營收維持三成以上成長，2027 年併入 Interplex 後更高","2y":"2027 全年營收年增 ≥30%（含 Interplex）","5y":null,"10y":null,"threshold":"月營收累計年增率 ≥25%；2027 全年 ≥30%","source":"公司每月營收公告、季報","drift_rule":"2 年期：TTM 營收成長偏離門檻連 2 季 ≥5% 為削弱、連 3 季 ≥10% 為反轉"},{"id":"H2","text":"毛利率與營益率在世代轉換與併購整合期間守住 Q2 2026 水準，規模放大讓每股獲利跟上營收","2y":"2027 年季毛利率維持 ≥28.5%、季營益率 ≥15%","5y":null,"10y":null,"threshold":"季毛利率 ≥28.5% 且季營益率 ≥15%","source":"季報、法說會","drift_rule":"2 年期：連 2 季偏離 ≥5% 為削弱、連 3 季 ≥10% 為反轉"},{"id":"H3","text":"銅、電源、光學三條線並行，讓公司在銅被光替代的轉換中保住每櫃內容價值","2y":null,"5y":"HPC 營收占比 2027 年 ≥60%，2028 年起光學與電源成長抵銷銅纜放緩","10y":null,"threshold":"HPC 營收占比 2027 年 ≥60%；光學（XFS）營收有季度揭露且年增為正","source":"法說會、外資報告、年報產品別營收","drift_rule":"5 年期：連 4 季偏離 ≥5% 為削弱、連 6 季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"Credo 的 AEC 二供分走份額","h_ref":"H1","clock":"⚡","threshold":"公司或 Credo 確認二供出貨，且月營收年增連 2 月 <15%","evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"id":"R2","text":"NVIDIA 平台設計減少線纜內容（運算托盤無線纜化、背板份額重分）","h_ref":"H3","clock":"🔥","threshold":"下一代平台每櫃銅纜條數較 GB300 世代減少 ≥30%（供應鏈 BOM）","evidence_refs":["customer_second_source#2"]},{"id":"R3","text":"光學／CPO 在 scale-up 取代銅，公司光學份額接不住","h_ref":"H3","clock":"🐢","threshold":"CPO 在 scale-up 量產部署，且公司 HPC 營收年增連 4 季 <10%","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"id":"R4","text":"增資稀釋與 Interplex 整合拉低每股獲利","h_ref":"H2","clock":"🔥","threshold":"併入後兩季合併營益率 <15%，或季 EPS 年增落後營收年增 >10pp","evidence_refs":["major_events#2"]},{"id":"R5","text":"AI 資本支出進入消化期，客戶部署時點延後（管理層 2026-08-21 自述會發生）","h_ref":"H1","clock":"⚡","threshold":"單月營收年增連 3 個月 <10%","evidence_refs":[]}],"single_thing":{"description":"NVIDIA 正式宣布下一代機櫃（Rubin Ultra／Kyber）的 scale-up 背板改用光學（CPO／NPO），不再用被動銅纜","why_fatal":"銅背板與 AEC 是 HPC 營收中份額最穩、毛利最好的一塊，外資估 HPC 占比 2027 年達 75%；背板一改光，公司從主要供應商變成光學後進者，FY2028 起 EPS 路徑整段下移，終端倍數同步壓縮，是情境樹裡敏感度最大的單一變數","if_happens":"減碼至半倉並重跑研究；只有在 XFS 拿到同代光學背板訂單證據時才回補","how_monitor":"NVIDIA GTC（每年 3 月）與 Computex（6 月）發表、供應鏈 BOM 報告、公司法說對銅背板世代的說法","probability":"約 20%（12～24 個月）：Rubin 背板仍用約 5,184 條銅纜、NVIDIA 稱 2026～2028 雲端仍以可插拔光模組為主；但 Gartner 預期 CPO 約三年內成主流，Kyber 若延後反而延長銅的壽命"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.4,"peg_fy2":0.64,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":46.33,"FY2026E":69.25,"FY2027E":127.97,"FY2028E":164.67},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS；共識為 Koyfin 美元快照依 2026-10-09 匯率 31.912 換算新台幣"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3665.TW_20261012/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"AI 平台世代驅動的互連製造，三年毛利率上升，成長部分靠併購與外部股本"},"industry":{"clock_phase":"II","sd_verdict_source":"需求結構持久（AI 部署由算力延伸到電力、網路、散熱與機構），但產品層週期性將反轉：管理層自述會有加速與消化期，銅纜段本十年末後面臨光學替代（CRU）","bargaining":{"up":"銅與 PVC 原料漲價，公司只能選擇性轉嫁（2026-05-12 財務長）","down":"NVIDIA 定平台規格、Credo 定 AEC 方案、超大規模雲端付款，議價權在客戶端；Credo 兩度傳出引進二供","geo":"擴產地點分散於巴淡、台南、檳城、柔佛、越南；美國 301 關稅屬總體背景、未點名公司"},"profit_pool_dir":"AI 機櫃互連與電源利潤池擴大，但向光學與 800V HVDC 遷移；銅雙絞線段本十年末後放緩","tam_table":{"expanded":false,"reason":"事實表未收高速銅纜、AEC、HVDC 母排與光纖組件的 TAM、滲透率與段別成長資料，只有 CRU 的定性判斷，無法建表；以 HPC 營收占比與替代技術時點代替"}},"moat":{"mechanism":"多世代平台認證累積的高速銅、電源與系統整合工程能力，加上早期參與客戶下一代平台開發；轉換成本來自重新認證週期","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大（毛利率三年由 25.65% 升到 31.73%、營益率 10.46% 升到 17.52%，Q2 2026 回到 30.73%／17.22%）；定價面持平（營益率仍低於 APH、TEL，FCF 率差距約 12pp，Credo 二供傳聞兩度出現、原料成本只能選擇性轉嫁），合起來判持平","peer_na_reason":"事實表未收同業 ROIC 與投入資本，只能用毛利率、營益率、FCF 率代替 spread","threats":[{"level":"🟡","text":"Credo 兩度傳出引進第二家 AEC 供應商，未見正式確認與出貨規模；屬點對點份額威脅","p":35,"evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"level":"🔴","text":"NVIDIA 平台設計改變線纜內容：CES 2026 稱 Rubin 伺服器採無線纜設計，背板份額每代重分","p":25,"evidence_refs":["customer_second_source#2"]},{"level":"🔴","text":"光學／CPO 在 scale-up 取代銅：CRU 預期 2020 年代後期放緩、Gartner 預期約三年內成主流；公司有 XFS 光學可部分接住，所以列生態攻擊而非全面架構替代","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"大廠跨入資料、電源、光學的完整產品線，董事長 2026-08-21 承認競爭者正在擴大組合","p":40,"evidence_refs":[]}],"roic_durability":{"quadrant":"未定：事實表未收投入資本；營益率 17.4% 屬中高，FCF 率 5.4% 顯示營運資金與資本支出占用偏重","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（AI 機櫃）、決策者（NVIDIA 定規格、Credo 定 AEC 方案）、付款者（超大規模雲端）三環都成立；9 月營收年增 39.2%。風險在部署時點而非需求本身，管理層 2026-08-21 自己說會有消化期"},{"item":"決策層級","level":"🟡","text":"替代性的最小單位是每一代平台的重新認證；董事長稱多代認證讓既有供應商帶著資歷進下一代，但 Credo 兩度傳出引進二供，每代認證都是重新競爭的窗口"},{"item":"價值鏈分配","level":"🟡","text":"規格與晶片價值在 NVIDIA 與 Credo，貿聯拿製造與工程段；營益率低於 APH、TEL，銅與 PVC 漲價只能選擇性轉嫁（2026-05-12 財務長），價值鏈位置偏中段"},{"item":"社會容忍度","level":"🟢","text":"產品非民生必需品、無監管授權依賴；美國 301 關稅與產能過剩關稅屬總體背景、未點名公司，產能已分散到東南亞與台灣"}],"roiic":"事實表未涵蓋（缺投入資本與併購前後資產負債表）","reinvest_rate":"事實表未涵蓋（缺折舊攤銷與營運資金變動；收購 Interplex 企業價值 8.5 億美元，XFS 金額未列）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩項輸入皆缺，不推估上界數字。判定共識超出內生能力的依據不是算式，而是資金來源檢驗：共識三年 EPS 年化約 52.6%，同期內部現金只有 TTM FCF 率 5.4%（FCF／淨利 FY2025 約 0.54），擴張資金實際來自 GDR／ECB 增資（估每股盈餘稀釋 6%～7%）與 8.5 億美元現金收購 Interplex；若內部現金足以支撐，就不需要外部股本。可能看錯之處：外部募資也可能是趁高估值籌碼，而非內部資金不足。此判定屬定性、信心中，待投入資本揭露後改以算式重驗。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","3665.TW":31.08,"APH":37.63,"TEL":36.12,"3023.TW":24.36,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","3665.TW":17.44,"APH":26.77,"TEL":20.49,"3023.TW":10.63,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","3665.TW":5.38,"APH":17.34,"TEL":17.16,"3023.TW":4.1,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","3665.TW":2.46,"APH":null,"TEL":4.76,"3023.TW":4.37,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"APH","gm":37.63,"om":26.77,"fcf_margin":17.34,"rd_intensity":null,"strategy_note":"毛利率 37.6%、營益率 26.8%、FCF 率 17.3% 全面高於貿聯，是高速銅與電源互連最強對手，規模與現金流能在價格與產能上施壓","period":"TTM ending 2026-06-30（4季加總）"},{"name":"TEL","gm":36.12,"om":20.49,"fcf_margin":17.16,"rd_intensity":4.76,"strategy_note":"營益率 20.5%、FCF 率 17.2%；供應鏈報告稱其 GB300 銅背板份額低於預期的 30%，大廠在這個細分並未壓倒性勝出","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3023.TW","gm":24.36,"om":10.63,"fcf_margin":4.1,"rd_intensity":4.37,"strategy_note":"毛利率 24.4%、營益率 10.6%，台系線束同業的獲利結構明顯較低，貿聯的溢價來自 HPC 與高速產品組合","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（AI 機櫃互連、半導體設備子系統）為主，併購（XFS、Interplex）次之，產品組合帶動毛利；股本增加抵銷部分每股成長","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本與再投資率事實表未涵蓋，無法算內生上界；成長資金來自 GDR／ECB 增資與 8.5 億美元現金收購，而非內部現金（TTM FCF 率 5.4%），判定共識三年 EPS 年化約 53% 超出內生能力","segments":[{"item":"HPC 相關營收占比 2024","value":"約 18%（分析估計）"},{"item":"HPC 相關營收占比 2025","value":"約 35%（分析估計）"},{"item":"HPC 營收占比 2026E／2027E","value":"53%／75%（外資估，含 Interplex）"},{"item":"HPC 相關營收年增 2026E／2027E","value":"91%／40%（永豐投顧估）"},{"item":"半導體設備","value":"訂單能見度到 2027 下半年，客戶討論延伸到 2028（2026-08-21 財務長）"},{"item":"工業與車用","value":"逐步回升、各市場速度不一（管理層定性）"}],"decay_signals":["亮：EPS 成長遠高於營收成長，2025 年 EPS 年增約 96%、營收年增 31.7%，共識三年 EPS 年化約 53% 也高於營收成長","亮：替代技術壓縮銅纜 TAM，CRU 與 Gartner 都預期光學在 2020 年代後期擴大替代","半亮：FCF／淨利 FY2024 約 0.78、FY2025 約 0.54，TTM FCF 率 5.4%，尚未連 2 年低於 0.75","未亮：毛利率 Q2 回升到 30.73%，連 2 季年減無資料可證","未亮：核心份額縮減無確認數據，二供僅傳聞"]},"quality":{},"governance":{"capital_returns":[{"item":"股息","value":"trailing 12 個月殖利率 0.655%"},{"item":"回購","value":"事實表未涵蓋，無可引紀錄"},{"item":"增資","value":"GDR＋ECB，估每股盈餘稀釋 6%～7%（2026-07）"},{"item":"併購","value":"Interplex Datacom 企業價值 8.5 億美元現金（2026-09 交割，日期待核）；XFS 2026 年 1 月併入"},{"item":"自由現金流／淨利","value":"FY2024 約 0.78、FY2025 約 0.54"}],"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表未涵蓋：XFS 與 Interplex 併入後的獲利與投入資本未揭露，Interplex 2026-09 才交割","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"無回購可評，近期反向以 GDR 與 ECB 增資","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"GDR＋ECB 估每股盈餘稀釋 6%～7%（2026-07 歐系外資），遠高於每年 1.5% 上限","grade":"不過"}]},"valuation":{"basis":"Fwd 本益比（FY2026 共識與本報告 FY2027 基準）為主，PEG 僅供對照","tier":"台系 AI 互連組件製造","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，未收同業倍數，無法建立同級倍數錨；終端倍數改以自身現值 34 倍與成長降速推導"},"fwd_pe":34.08,"peg":0.65,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價 2,355 元；Fwd 34 倍、以基準 FY2027 EPS 105 元計約 22 倍；PEG 0.65 建立在有爭議的共識分母上不採用；trailing 本益比在近四個年度端點最高（樣本不足五年，不填五年分位）；基準五年終端約 3,870 元、年化約一成→估值中性","upside_short_pct":11,"upside_mid_pct":38},"trap_analysis":{"verdict":"🟡","label":"成長真實，現金轉換與每股經濟待驗"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Credo 兩度傳出引進 AEC 二供；Rubin 伺服器採無線纜設計；CRU、Gartner 預期光學在 2020 年代後期取代銅；管理層兩場法說都提醒會有消化期","assumption":"AI 互連需求與貿聯份額在 2027～2028 年同時延續","consequence":"消化期遇上二供分量與局部改光，EPS 回落到 70 多元、本益比降到 14 倍，股價約 −43%～−57%","ruling":"採納，作為 Bear 情境 30% 機率；與唯一致命點部分重疊（架構改光），本條另補客戶二供與消化期兩個獨立來源","watch":"月營收年增率、Credo 對供應商的說法、NVIDIA 下一代平台 BOM","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_second_source#2","substitute_technology#0","substitute_technology#2"],"fact_refs":["f_kpi0_ifrs"]},{"view":"論點成功但股東經濟變差","evidence":"GDR＋ECB 估每股盈餘稀釋 6%～7%；以現金 8.5 億美元收購 Interplex；FCF／淨利 FY2025 約 0.54，TTM FCF 率 5.4%，APH、TEL 約 17%","assumption":"營收成長能完整轉成每股盈餘與自由現金流","consequence":"營收照預期成長，但股本擴大、併購報酬不明、現金被營運資金吃掉，每股價值成長落後營收","ruling":"採納，基準 FY2027 EPS 取 105 元而非共識 127.97 元，資本配置不給好評","watch":"Interplex 併入後營益率、季 EPS 年增與營收年增差、年度 FCF 率","evidence_refs":["major_events#2"],"fact_refs":["f_peer_3665_tw_fcf_margin_pct","f_peer_aph_fcf_margin_pct","f_peer_tel_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"trailing 本益比 43.3 倍、P/S 5.6 倍都在近四個年度端點最高；14 位分析師全數買進","assumption":"市場已把共識 FY2027 的爆發式成長全部計價","consequence":"若共識下修，倍數與 EPS 同時下修","ruling":"部分反駁：現價低於全部分析師最低目標價 2,450 元，26 週只漲 6.77%，以基準 105 元計約 22 倍，市場已對共識打折；但不足以稱便宜，估值判中性","watch":"共識 FY2027 EPS 修正方向、Q3 與 Q4 季 EPS","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_pe_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy2"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 2355.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=2355.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率復原（管理層承諾對照）","cause":null,"prior_field":null,"side_a":"2026-05-12 法說，財務長 Charles Tsai 把 Q1 毛利率 28.77% 歸因於世代轉換、舊品價格正常化與新案爬坡，稱非長期軌跡改變","side_b":"Q2 毛利率回升到 30.73%、營益率 17.22%；但 2026-08-21 財務長要大家不要把毛利當成每季直線向上建模","ruling":"可調和：承諾已兌現一季，管理層同時降低續升預期；基準不假設毛利率超過 FY2025 的 31.73%","evidence_level":"實現數字＋管理層原話","settle_metric":"Q3 與 Q4 2026 季毛利率","if_then":["若 Q3、Q4 毛利率皆 ≥31%→基準 FY2027 EPS 上修至 115 元並可加碼","若任一季毛利率 <28.5%→停止加碼，連 2 季則減碼"],"evidence_refs":[]},{"axis":"Credo AEC 份額","cause":null,"prior_field":null,"side_a":"2025-02 與 2025-12 兩度傳出 Credo 引進第二家 AEC 供應商，股價一度跌停；公司與 Credo 皆未正式確認，也無出貨規模","side_b":"2026 年中歐系外資稱貿聯仍是 Credo AEC 與 ALC 主要供應商；9 月營收年增 39.2%、前 9 月年增 39.9%","ruling":"不可調和（份額方向相反），裁定採 B 側：營收加速是較硬的數據，傳聞無出貨規模；但二供傳聞本身代表議價權非獨家，定價面不給加分","evidence_level":"實現營收＋外資轉述 vs 媒體傳聞","settle_metric":"月營收年增率與 Credo 季報對供應商的說法","if_then":["若公司或 Credo 確認二供出貨且月營收年增連 2 月 <15%→減碼至半倉","若到 2027 年 6 月仍無二供出貨證據且月營收年增 ≥25%→維持點狀威脅判斷，可加碼至原定上限"],"evidence_refs":["customer_second_source#0","customer_second_source#1","customer_second_source#3"]},{"axis":"銅與光的替代時點","cause":null,"prior_field":null,"side_a":"CRU 預期銅雙絞線成長延續到本十年末後隨光學替代放緩；Gartner（2026-02）預期 CPO 約三年內成主流，銅在 224Gbps 遇到極限","side_b":"大摩分析 Rubin NVLink 背板仍用約 5,184 條被動銅纜；NVIDIA 稱 CPO 交換器 2026 下半年才小量部署、雲端 2026～2028 仍以可插拔為主；公司已有 448Gbps 銅纜與 XFS 光學","ruling":"不可調和在時點：2028 年前採 B 側（直接平台證據較多），2028 年後採 A 側風險，放入長期風險與 Bear 30%；公司光學能否接住尚無營收數字（CEO 2026-05-12 稱需再看數季）","evidence_level":"產業研究機構 vs 平台 BOM 分析與公司產品","settle_metric":"NVIDIA 下一代機櫃 scale-up 互連架構發表","if_then":["若 NVIDIA 正式宣布下一代 scale-up 背板改光學→減碼至半倉並重跑研究","若 Kyber 確認延至 2028 下半年且沿用銅背板→上修基準 FY2029～FY2030 EPS，維持持有"],"evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","supply_demand_durability#3","supply_demand_durability#4","competitive_share_entrants#2"]},{"axis":"共識 FY2027 EPS 可達性","cause":null,"prior_field":null,"side_a":"賣方共識 FY2027 EPS 127.97 元，較 FY2026 的 69.25 元年增 85%；14 位分析師全數買進，平均目標價約 3,203 元","side_b":"營收成長約四成＋Interplex 約一成三，且 GDR／ECB 稀釋每股盈餘 6%～7%；要 EPS 年增 85% 需淨利率大幅跳升，法說無此指引","ruling":"不可調和，採 B 側：基準 FY2027 EPS 105 元，便宜論證不採用；現價已低於最低目標價，市場本身也在打折","evidence_level":"共識快照 vs 實現營收與稀釋估計","settle_metric":"Q4 2026 季 EPS（2027 年 3 月公布）","if_then":["若 Q4 2026 季 EPS ≥22 元且毛利率 ≥31%→基準上修至共識並加碼","若 Q3 2026 季 EPS <16 元→基準下修至 95 元並停止加碼"],"evidence_refs":["major_events#2","capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"資本紀律說法對照實際資金來源","cause":null,"prior_field":null,"side_a":"管理層兩場法說都強調不為高需求預期擴產、資本支出看能見度、資金變多不降低報酬門檻","side_b":"2026 年以 GDR＋ECB 募資並以現金 8.5 億美元收購 Interplex；TTM FCF 率 5.4% 遠低於 APH、TEL","ruling":"可調和（程度差異）：有機擴產確實節制，但成長資金已轉向外部股本；Interplex 報酬要等併入後四季才能驗證，在那之前資本配置不給好評","evidence_level":"管理層原話 vs 已公告交易與現金流","settle_metric":"Interplex 併入後四季合併營益率與 FCF 率","if_then":["若併入後四季營益率 ≥17% 且 FCF 率回到 ≥7%→資本配置上調一級","若併入後兩季合併營益率 <15%→減碼至七成"],"evidence_refs":["major_events#0","major_events#1","ma_merger#0","ma_merger#1","major_events#2"]},{"axis":"現在就買與現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：營收前 9 月年增四成、Q2 獲利創新高、半導體設備能見度到 2027 下半年；股價半年只漲 6.8%、低於全部分析師最低目標價，FY2027 只做到基準 105 元也只有 22 倍","side_b":"現在就賣：共識把 2027 年 EPS 估到年增 85% 本身就是下修風險，trailing 本益比在近四年端點最高，管理層連兩季提醒消化期，二供與銅被光替代都落在 2027～2028 年","ruling":"兩邊都成立：基準五年年化約一成，不追高也不放空，依觸發器分批","evidence_level":"實現數字＋共識＋管理層原話","settle_metric":"Q4 2026 季 EPS 與月營收年增率","if_then":["若股價回到 2,000 元以下且月營收年增仍 ≥25%→分批反買","若股價高於 3,360 元而基準 EPS 未上修→減碼三分之一"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭軸惡化中：大廠擴展 AI 互連、電源與光學產品線，Credo 傳二供","side_b":"結構軸轉好中：AI 部署延伸到電力與互連，800V HVDC 與半導體設備子系統擴大；替代技術軸在 2028 年後成形；關稅屬背景未點名公司","ruling":"雙向拉鋸：2028 年前結構轉好的力量大於競爭惡化，2028 年後替代技術主導","evidence_level":"管理層原話＋外資估計＋產業研究","settle_metric":"HPC 營收占比與月營收年增率","if_then":["若 2027 年 HPC 占比 <60%→下修跑道判斷並停止加碼","若 HPC 占比 ≥70% 且營益率 ≥17%→維持持有並可加碼"],"evidence_refs":["end_markets#1","end_markets#2","reg_tariff_export#0","reg_tariff_export#1"]}],"triggers":[{"n":1,"text":"月營收累計年增率跌破 25%，連 2 個月","type":"假設驗證","maps_to":"H1","metric":"月營收累計年增率","threshold":"<25% 連 2 個月","action":"停止加碼","source_freq":"公司月營收公告，每月","date":null,"evidence_refs":[]},{"n":2,"text":"季毛利率 <28.5% 或季營益率 <15%，連 2 季","type":"假設驗證","maps_to":"H2","metric":"季毛利率／季營益率","threshold":"毛利率 <28.5% 或營益率 <15% 連 2 季","action":"減碼","source_freq":"季報，每季","date":null,"evidence_refs":[]},{"n":3,"text":"公司或 Credo 確認二供出貨，且月營收年增連 2 月 <15%","type":"風險","maps_to":"R1","metric":"二供確認＋月營收年增率","threshold":"確認二供且月營收年增 <15% 連 2 月","action":"減碼至半倉","source_freq":"重大訊息、Credo 季報、月營收","date":null,"evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"n":4,"text":"NVIDIA 正式宣布下一代機櫃 scale-up 背板改光學","type":"Single Thing","maps_to":"Single Thing","metric":"NVIDIA 平台架構發表","threshold":"官方宣布背板改 CPO／NPO","action":"減碼至半倉並重跑研究","source_freq":"GTC（每年 3 月）、Computex（6 月）、供應鏈 BOM 報告","date":"2027-03","evidence_refs":["substitute_technology#2","customer_second_source#2"]},{"n":5,"text":"Interplex 併入後兩季合併營益率 <15%，或季 EPS 年增落後營收年增超過 10pp","type":"風險","maps_to":"R4","metric":"合併營益率／EPS 與營收年增差","threshold":"營益率 <15% 或落差 >10pp，連 2 季","action":"減碼","source_freq":"季報，每季","date":"2027-05","evidence_refs":["major_events#2"]},{"n":6,"text":"月營收年增連 3 個月 <10%，消化期確認","type":"風險","maps_to":"R5","metric":"單月營收年增率","threshold":"<10% 連 3 個月","action":"減碼","source_freq":"公司月營收公告，每月","date":null,"evidence_refs":[]},{"n":7,"text":"股價回到 2,000 元以下且月營收累計年增仍 ≥25%","type":"估值rearm","maps_to":"估值","metric":"股價＋月營收累計年增率","threshold":"≤2,000 元且年增 ≥25%","action":"分批反買","source_freq":"每日股價、每月營收","date":null,"evidence_refs":[]},{"n":8,"text":"股價高於 3,360 元（基準 FY2027 EPS 的 32 倍）而基準 EPS 未上修","type":"減碼","maps_to":"估值","metric":"股價對基準 FY2027 EPS 倍數","threshold":">32 倍","action":"減碼三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":9,"text":"Q4 2026 財報與首個完整 Interplex 併表季後複審","type":"複審日期","maps_to":"H1/H2/R4","metric":"季 EPS、毛利率","threshold":"Q4 季 EPS ≥22 元上修基準；<16 元下修","action":"重跑研究","source_freq":"季報","date":"2027-03","evidence_refs":[]}],"kill_metrics":[{"metric":"月營收累計年增率","bear_threshold":"連 3 個月 <10%","window":"2026-11 至 2027-12","source":"公司月營收公告（公開資訊觀測站）","last_status":"ok"},{"metric":"季營益率","bear_threshold":"<13% 連 2 季","window":"2026Q4 至 2027Q4","source":"公司季報","last_status":"ok"},{"metric":"年度自由現金流／淨利","bear_threshold":"FY2027 <0.5","window":"FY2027 年報","source":"年報現金流量表","last_status":"warning"},{"metric":"NVIDIA 下一代機櫃 scale-up 互連材質","bear_threshold":"官方宣布背板改光學","window":"2027-03 至 2028-06","source":"NVIDIA GTC／Computex 發表、供應鏈 BOM 報告","last_status":"ok"}],"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=6.77, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"verdict":"觀望","rearm_trigger":"股價 ≤2,000 元且月營收累計年增 ≥25%，或 Q4 2026 季 EPS ≥22 元證實共識","exec_line":"不追高；現價可依基準年化約一成持有，股價回到 2,000 元以下且成長未破才分批加碼；二供確認或背板改光學即減碼至半倉；路徑回撤可能達 −60%，論點完整時不因波動砍倉，需有深回撤心理準備"},"reasoning":{"industry":"Q2 2026 營收 232.81 億元（年增 37%、季增 12%），毛利率 30.73%、營益率 17.22%、EPS 15.28 元創單季新高，Q1 毛利率 28.77% 的轉換期壓力已回穩；管理層不給數字指引。營收結構：HPC 相關占比由 2024 年約 18% 升到 2025 年約 35%，外資估 Interplex 併入後 2026、2027 年達 53%、75%（分析估計，口徑不一）；半導體設備端財務長稱訂單能見度到 2027 下半年；工業與車用逐步回升。單點依賴：Credo 的 AEC 據報由貿聯獨家或主要供應，2025 年兩度傳出二供，屬集中度風險，不當護城河證據；前大客戶營收占比事實表未涵蓋。供需持久性：AI 部署需求屬結構性，但管理層兩場法說都說投資週期會有消化期，產品層屬週期性將反轉的類型。產業態勢：競爭惡化中（大廠擴展 AI 互連與電源、客戶二供）與結構轉好中（電力與互連需求、半導體設備子系統）同時存在，屬雙向拉鋸。四項外部依賴逐項檢查：（一）客戶集中度與信用：付款端是少數超大規模雲端，規格由 NVIDIA 決定、AEC 方案由 Credo 決定，HPC 占比外資估 2026 年 53%、2027 年 75%，集中度高且還在上升；前大客戶營收占比、應收帳款天數與客戶信用條件事實表皆未涵蓋，所以只能定性判為高、不給量化分數，以 Credo 二供消息與月營收年增率作監測點。（二）監管與反壟斷：產品不是受監管品項，沒有授權依賴；美國 301 關稅屬總體背景、未點名公司；直接涉及公司的反壟斷或出口管制事件事實表未見，判低。（三）地緣與供應鏈：擴產分散在巴淡、台南、檳城、柔佛、越南，降低單一國家關稅風險；原料端銅與 PVC 漲價只能選擇性轉嫁（2026-05-12 財務長），屬毛利風險而非斷料風險；關鍵零組件是否單一來源事實表未涵蓋。（四）通路與商業模式轉移：由線纜組件往電源母排、光學（XFS）與機構件（Interplex）子系統延伸，是每櫃內容價值擴大，不是通路改變；真正的風險在 NVIDIA 平台設計改動（CES 2026 稱 Rubin 伺服器採無線纜設計）把內容價值移出公司產品範圍，已列入風險項追蹤。","moat":"機制：高速銅與電源產品歷經多代開發與認證，董事長稱既有供應商帶著認證紀錄、客戶關係與量產經驗進入下一代，後進者要追趕；財務長稱部分工程已延伸到 N+2 平台。執行面擴大：毛利率由 FY2022 25.65% 升到 FY2025 31.73%，營益率 10.46% 升到 17.52%（年度財報）。定價面持平：TTM 營益率 17.44% 仍低於 APH 26.77%、TEL 20.49%，FCF 率 5.38% 對兩者約 17%，差距大；原料漲價只能選擇性轉嫁；Credo 二供傳聞代表最大 AEC 客戶並非鎖死。同業 ROIC spread 事實表未涵蓋，以利潤率代替。評分：執行 8、定價 6。","growth":"成長組成：量為主（AI 機櫃出貨、半導體設備子系統）＋併購（XFS 2026 年 1 月、Interplex 2026 年 9 月）＋產品組合帶動毛利；無回購，反向有增資稀釋。共識三年 EPS：FY2025A 46.33 元→FY2028E 164.67 元，年化約 52.6%，前段集中在 FY2027（69.25→127.97，年增 85%）。缺口歸因：內生上界因投入資本缺資料無法計算；可歸因部分＝營益率擴張（FY2025 17.52%，Q2 2026 17.22%）與 Interplex 併入（過去 12 個月營收約 3.92 億美元，依 2026-10-09 匯率 31.912 約 125 億元，約占 2026 年營收一成三）；其餘無法歸因，信心上限中。跑道：滲透率事實表未涵蓋；永豐估 CPO 與 800V HVDC 在 2027～2028 年全面放量，為有來源的下一段，但 CEO 稱 XFS 需再看數季才下結論，所以跑道給中等而非寬。","governance":"FCF／淨利：FY2022 約 0.14、FY2023 約 1.82、FY2024 約 0.78、FY2025 約 0.54（年度財報推算），TTM FCF 率 5.38%，遠低於 APH、TEL 約 17%。股東回報：trailing 殖利率 0.655%，回購紀錄事實表未涵蓋。2026 年以 GDR＋ECB 募資，歐系外資估每股盈餘稀釋約 6%～7%；以現金收購 Interplex（企業價值 8.5 億美元＋最高 5,000 萬美元或有價金），XFS 2026 年 1 月併入。管理層強調不為高需求預期擴產、報酬門檻不降，有機資本支出確實節制，但資金來源已轉向外部股本。營運槓桿：Q2 2026 營收年增 37%、淨利年增 47%，未見壓縮。SBC 數字事實表未涵蓋。","valuation":"現價 2,355 元，Fwd 本益比 34 倍（FY2026 共識 69.25 元），FY2027 共識 127.97 元下約 18.4 倍；共識三年 EPS 年化約 52.6%，PEG 約 0.65。但便宜論證建立在 FY2027 共識上：營收年增約四成＋Interplex 約一成三，扣掉 6%～7% 稀釋，要 EPS 年增 85% 需淨利率大幅跳升，法說沒有這樣的指引，所以本報告基準 FY2027 EPS 取 105 元，對應約 22 倍。trailing 本益比 43.3 倍、P/S 5.6 倍都在近四個年度端點的最高（只有四點，不是五年分位）。賣方 14 位全數買進、平均目標價約 3,203 元，現價低於最低目標價 2,450 元，市場本身已在打折。同業倍數事實表未涵蓋，終端倍數以自身現值與成長降速推，不跨同業錨定。","premortem":"依據見反證紀錄。衰退信號兩個亮、一個半亮：EPS 成長遠高於營收成長、替代技術壓縮銅纜市場、FCF／淨利 FY2025 約 0.54。股價 26 週只漲 6.77%、RSI 54.5，沒有動能過熱；歷史最大回撤事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺 AI 資料中心（銅纜、AEC、電源母排、光纖組件）與半導體設備、工業客戶的互連與子系統製造錢；錢卡在 NVIDIA 平台規格與 Credo AEC 方案這一節點，貿聯是被指定、每一代都要重新認證的工程製造方。","moat":"護城河方向持平：多世代認證累積的工程與量產能力在擴大，但客戶二供與銅被光替代讓定價力沒有變強。","growth":"五年後跑道中等：AI 互連與半導體設備仍在擴張，HVDC 電源與光學是有來源的下一段，但銅纜段本十年末放緩、光學份額尚未證實。","capital":"資本配置偏弱：成長靠增資與現金收購撐，FCF 轉換率低，併購報酬尚無數字可驗證。","valuation":"現價要求 2026～2027 年 EPS 照共識跳升、且銅背板在 2028 年前不被光學取代才算便宜；我信營收成長，不信共識 FY2027 EPS 年增 85%，以自己的基準估算只算合理。","how_wrong":"價值陷阱風險中等：成長是真的，但每股經濟與現金轉換待驗，替代技術在後段等著。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"右側可追蹤","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 2,000 元以下，且月營收累計年增率仍 ≥25%（與加碼觸發器第 7 條相同）","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":2355.0,"week26_return_pct":6.77,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"便宜論證（PEG 0.65、FY2027 本益比約 18 倍）依賴 FY2027 共識 EPS 年增 85%；營收成長、Interplex 規模與 6%～7% 稀釋推不出這個數字，共識另為美元快照換算，可能含口徑問題。本報告改用基準 105 元，短期以 FY2027 基準×25 倍、三年以 FY2029 基準 148 元×22 倍估算"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026 財報與法說，首次反映 GDR 稀釋與 Interplex 一週併表","impact":"高","watch":"毛利率是否 ≥30%、季 EPS 是否 ≥16 元"},{"date":"2026-11","date_precision":"month","type":"other","event":"10 月營收，首個完整併入 Interplex 的月份","impact":"中","watch":"月營收年增率與 Interplex 貢獻規模"},{"date":"2027-03","date_precision":"month","type":"product","event":"NVIDIA GTC 2027，下一代機櫃 scale-up 互連架構","impact":"高","watch":"背板是否仍用銅纜、CPO 部署時程"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"Q4 2026 財報，檢驗共識 FY2027 EPS 可達性","impact":"高","watch":"季 EPS 是否 ≥22 元、FCF 率"}],"_projected_from":"v19"}
```
