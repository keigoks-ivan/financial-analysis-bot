你是 stock-analyst v20 的**散文層（prose）agent**，標的 BSX（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BSX_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：BSX　日期：2026-11-03　archetype：None　前份裁決：2026-07-10　迴避｜不持有　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1769B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（805B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（990B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1554B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（957B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（1098B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1430B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2125B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1498B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3229B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1769           3662-5231      5 條（2–6 內）  
s3                  8000         805           5036-7195      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3501          8049-11499      5 條（2–6 內）  
s6                 11000        1098           6931-9902      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1430           1449-2070      3 條（2–6 內）  
s10                 5000        2125           2012-2875      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3229           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5665B；至少需散文≈39.34KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−40%
−40
−30%
−27%
−25%
−25
−8%
−7%
−6%
−5%
−3%
−2%
−1.9%
−1%
0%
0
0.04
0.05
0.06
0.07
0.08
0.4
0.73
0.75
0.77
0.79
0.80
0.8
0.82
1%
1
01
1.17
1.28
1.5%
1.8
1.9%
1.9
02
2
2%
2.5
2.6
2.73
2.9
2.92
2.95
2.98
3.0
3
3%
03
3.00
3.05
3.06
3.08
3.1
3.15
3.16
3.18
3.19
3.2
3.28
3.32
3.41
3.5
3.6
3.62
3.7%
3.75%
3.8
3.91
4%
4
4.1%
4.1
4.2%
4.2
4.5
4.5%
4.6
5
5%
5.1
6%
06
6
6.5%
7
7%
07
7.6%
8
8%
8.28
8.4%
8.67
8.8%
9
9%
09
9.3
10%
10
10.5
11
11%
11.9
12
12%
12.2
13
13%
13.64
13.8
13.84
13.86
13.88
13.9
14
14.5
14.52
14.8
14.9
15
15.1%
15.9%
16
16.1%
16.3%
18.54
18.6
19.0%
19%
20
20%
20.3
21.1%
21.7%
21.8%
22.5%
23.65
24
25%
26
26%
26.5%
27
28
28%
28.1%
28.98
29
29%
29.0%
30
30%
31
32.8%
32.8
33.07
34.04
35
35%
36
36%
38
38%
38.3%
39
39.7
40%
40.9%
43
44.15
44.99
45%
45
46.1
48%
49
50%
50
51.38
52
56.6%
57
58%
58.7
60
60%
63
65.0%
67%
68.0%
69.9%
70%
70
72
77
77.8%
80%
90
91%
100
102
104
120.85
145
200
209.7
210.3
232
250
300
360
374
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
20261103
7,500
8,000
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
{"meta":{"ticker":"BSX","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Boston Scientific Corporation"},"oneliner":"電生理與 Watchman 兩大成長引擎轉入下行，管理層一年內三度下修並稱 2027 年是谷底；約 14 倍本益比看似便宜，但分母仍在往下修，電生理份額止跌前不碰。","thesis":{"H":[{"id":"H1","text":"其餘約四分之三業務（介入心臟、周邊血管、內視鏡、神經調節、泌尿等）維持約 5%–6% 有機成長，讓公司 2027 年營收不衰退","2y":"2027 年電生理與 Watchman 以外的業務有機成長 ≥5%，公司整體 2027 年有機成長 ≥0%","5y":null,"10y":null,"threshold":"非電生理與 Watchman 業務有機成長 ≥5%；公司 2027 年有機成長 ≥0%","source":"公司季報新聞稿與法說事業別揭露（2026-10-28 法說稱該群組約 6%，2027 年中國價格約扣 1 個百分點）","drift_rule":"TTM 有機成長相對門檻偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"電生理與 Watchman 在 2027 年見底，2028 年回到成長","2y":"2027 下半年美國電生理季營收年減收斂到 5% 以內、2028 年轉正；美國 Watchman 單獨手術年減收斂到個位數","5y":null,"10y":null,"threshold":"美國電生理季營收 2028 年年增 ≥0%；Watchman 全球營收 2028 年年增 ≥0%","source":"公司季報事業別揭露、獨立醫師份額調查","drift_rule":"TTM 相對門檻偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H3","text":"重組節省加上 Penumbra 與新品，讓調整後 EPS 在 2028–2031 年回到高個位數年增","2y":null,"5y":"2028–2031 年調整後 EPS 年複合 ≥7%，Penumbra 在 2028 年後不再稀釋","10y":null,"threshold":"2027 年底實現重組年化節省超過 2.5 億美元；2028 年調整後 EPS 年增 ≥7%","source":"2026-07-27 重組 8-K、公司季報與法說","drift_rule":"TTM 相對門檻偏離連 4 季 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"PFA 份額在 2027 年流失得比管理層「與 2026 下半年相近」的假設更快","h_ref":"H2","clock":"⚡","threshold":"美國電生理季營收連 2 季年減超過 10%","evidence_refs":["competitive_share_entrants#2","end_markets#2","substitute_technology#1","substitute_technology#2"]},{"id":"R2","text":"LAAC 市場因臨床證據續縮，2027 年新對手再分食 Watchman","h_ref":"H2","clock":"🔥","threshold":"美國 Watchman 營收連 4 季年減超過 5%，或 2028 年底前一線標示仍未核准","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","end_markets#3","competitive_share_entrants#3"]},{"id":"R3","text":"中國集採、低價廠商與美國關稅一起壓毛利，抵銷重組節省","h_ref":"H1","clock":"🔥","threshold":"調整後毛利率任一季低於 67%，或全年調整後營業利益率年減超過 100 個基點","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"Penumbra 交割受阻或稀釋擴大、槓桿上升，加上證券集體訴訟與政府調查","h_ref":"H3","clock":"🐢","threshold":"FTC 要求剝離重疊業務或起訴阻擋；交割後毛負債槓桿連 4 季高於 3.5 倍；集體訴訟取得集體認證","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#1","lawsuit_class_action#0"]},{"id":"R5","text":"執行與預測失準延續：新品再延、召回、營運中斷，管理層第四次下修","h_ref":"H3","clock":"⚡","threshold":"2027 年全年指引在年內任一季下修，或主要平台上市時點再延一季以上","evidence_refs":["major_events#3","major_events#4","product_recall_warning#0","capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2","end_markets#0","end_markets#1"]}],"single_thing":{"description":"FARAWAVE Ultra 未能在 2028 年上半年前取得 FDA 核准並上市（公司目前說 2028 年初）","why_fatal":"電生理是兩個拖累中較大的一個，管理層明說 Ultra 上市前份額會持續流失；基準情境 2028 年 EPS 回升約 8%，其中電生理止跌是最大的單一變數，影響比 Penumbra 或 Watchman 標示更直接。","if_happens":"2028 年回升延後一年，基準情境滑向悲觀情境，樂觀情境機率降到 10%；維持迴避，核准公告前不重跑研究；已持有者減碼。","how_monitor":"每季法說對 Ultra 設計驗證進度的說法、FDA PMA 補件核准公告；2027 年第四季法說是第一個檢查點。","probability":"約 35%（12–24 個月內）：此平台已延後一季，同期 FARAFLEX、THRIVE、VITALYST 也延後或轉向，大型平台平均延後約半年。"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.84,"peg_fy2":3.8,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":3.06,"FY2026E":3.18,"FY2027E":3.19,"FY2028E":3.41},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS；FY2025A 由公司「2026 年 3.16–3.18 美元較 2025 年成長 3%–4%」反推約 3.06 美元，不是直接取得；EPS 共識家數事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BSX_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"高毛利多元醫材，成長靠新品循環與併購；目前處於兩大引擎下行、新品延後的空窗"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：房顫與中風預防需求隨老化持久，但 BSX 在 PFA 的超額份額來自先發，三家對手已上市，供給可逆性高；LAAC 需求受近一年臨床證據壓抑，美國市場年減約 7%–8%（2026-10-28 法說）。","bargaining":{"up":"部分材料單一來源，FDA 要求換料前重新驗證，換供應商耗時；PFAS 主要供應商已宣布停供。","down":"買方為醫院、GPO、經銷商，無單一客戶超過 10%；中國集採由政府定價，2027 年擴及更多事業。","geo":"單一產品的製造集中在一到少數廠區（美國、波多黎各、愛爾蘭、哥斯大黎加、馬來西亞、中國，聚合站彙整、待對年報核實）；美國進口關稅與醫材 232 調查結果未定。"},"profit_pool_dir":"電生理利潤池仍在擴大，但向 Medtronic、J&J 流出；LAAC 利潤池在縮；介入心臟與周邊血管利潤池擴大，BSX 份額上升。","tam_table":[{"item":"LAAC 市場規模","value":"約 20 億美元，美國市場年減約 7%–8%（2026-10-28 法說）；BSX 份額約 91%（2026-07-29 法說）"},{"item":"PFA 滲透率","value":"美國房顫消融約 80% 已用 PFA（2026-07-29 法說），滲透接近飽和"},{"item":"PFA 份額","value":"BSX 2025 年約 58%，醫師調查預期 2026 年約 48%；J&J 由 11% 升到 20%（BTIG 調查，2025-01）"},{"item":"加權市場成長率","value":"目前約 7%，未來三年 7%–8%（管理層，2026-10-28）"},{"item":"新市場","value":"2030 年前進入合計約 250 億美元的新市場（管理層說法，未附明細）"},{"item":"利潤池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"臨床證據、醫師使用習慣，加上導管室整套產品（標測系統、穿隔針、PFA 導管、Watchman）綁在一起形成的轉換成本","execution":5,"pricing":7,"grade":"C","trend":"↓","trend_evidence":"PFA 份額一年約掉 10 個百分點，管理層預期續失到 2028 年初；Watchman 美國單獨手術年減高十位數，2027 年再加新對手；中國集採擴及內視鏡與泌尿。","peer_na_reason":"事實表同業對照只有利潤率與研發密度，沒有 ROIC 與投入資本，無法算對最強同業的 ROIC 差距；改用 PFA 份額調查與毛利率對照判方向。","threats":[{"level":"🔴","text":"PFA 對手（Medtronic、J&J、Abbott）以新導管搭配自家標測系統搶份額，BSX 份額一年約掉 10 個百分點，管理層預期 2028 年初 Ultra 上市前續失","p":70,"evidence_refs":["competitive_share_entrants#2","end_markets#2","substitute_technology#1","substitute_technology#2"]},{"level":"🔴","text":"LAAC 需求因臨床證據改變轉診而萎縮，2027 年再加 Abbott 新一代封堵器；Watchman 約 91% 的份額讓 BSX 直接承受市場萎縮","p":50,"evidence_refs":["competitive_share_entrants#3","supply_demand_durability#1","end_markets#3"]},{"level":"🟡","text":"中國集採、本土廠商與低成本製造商帶來價格壓力，2027 年擴及內視鏡與泌尿","p":60,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉：調整後營益率約 26%–28%，周轉率因歷年多筆收購（Axonics、Silk Road、Nalu 等）偏低；投入資本事實表未涵蓋，象限為定性判斷","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"房顫消融需求健康（管理層稱電生理市場仍強）。LAAC 這一側，使用者是病人、決策者是轉診醫師、付款者是保險，轉診端因近一年臨床證據轉向觀望，美國單獨手術年減高十位數。問題（不想終身吃抗凝血藥）還在，解法的接受度在降；CHAMPION-AF 出血率 15.1% 對 21.8% 是反方證據。"},{"item":"決策層級","level":"🔴","text":"決策單位是每一台手術的醫師選品。PFA 份額一年移動約 10 個百分點，代表這個層級的換用成本比原先以為的低；標測系統與導管綁定能部分拉高黏著，但 J&J 與 Medtronic 也有自己的系統。"},{"item":"價值鏈分配","level":"🟡","text":"BSX 毛利率約 70%，高於多數同業，仍拿到價值鏈的大塊；但買方經 GPO 集中議價，中國由集採定價，部分材料單一來源也讓上游有議價空間。"},{"item":"社會容忍度","level":"🟡","text":"醫材價格由政府與保險定價：中國集採已擴及多個事業，美國醫材關稅與 232 調查未定。這類價格上限由政策決定，不由需求決定。"}],"roiic":"事實表未涵蓋（缺投入資本與收購金額序列）","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，兩項輸入都缺，不估。可得的代理：2022→2025 年 GAAP 營業利益由約 20.3 億增到約 39.7 億美元（營收×營益率自算），但同期多筆收購，增量資本無法拆分。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","BSX":69.92,"MDT":65.01,"SYK":64.98,"ABT":56.63,"EW":77.84,"unit":"%"},{"metric":"營業利益率","BSX":21.08,"MDT":19.04,"SYK":21.73,"ABT":15.9,"EW":28.09,"unit":"%"},{"metric":"FCF 利潤率","BSX":4.14,"MDT":16.33,"SYK":18.2,"ABT":15.66,"EW":22.01,"unit":"%"},{"metric":"研發密度","BSX":10.29,"MDT":7.77,"SYK":6.42,"ABT":6.64,"EW":16.75,"unit":"%"}],"competitors":[{"name":"MDT","gm":65.01,"om":19.04,"fcf_margin":16.33,"rd_intensity":7.77,"strategy_note":"PFA 的主要追兵：Sphere-9 在美國搶份額、Sphere-360 已在歐洲上市，醫師調查份額約 28%–29%；營益率 19.0% 略低於 BSX，TTM 自由現金流利潤率 16.3% 則明顯較高。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"SYK","gm":64.98,"om":21.73,"fcf_margin":18.2,"rd_intensity":6.42,"strategy_note":"與 BSX 業務重疊有限，作利潤率參照：營益率 21.7%、毛利率 65.0%，與 BSX 相近。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ABT","gm":56.63,"om":15.9,"fcf_margin":15.66,"rd_intensity":6.64,"strategy_note":"Amulet 360 已取得 CE，預期在美國成為 Watchman 的新對手；PFA 份額約 3% 仍小；營益率 15.9%，利潤結構低於 BSX。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"EW","gm":77.84,"om":28.09,"fcf_margin":22.01,"rd_intensity":16.75,"strategy_note":"結構性心臟的利潤率標竿（毛利率 77.8%、營益率 28.1%）；與 Watchman 同屬結構性心臟，但產品不直接競爭。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"2026–2027 年：量的成長被電生理與 Watchman 份額流失抵銷，中國價格為負；2028 年起：新品帶動的量與 Penumbra 併購；回購為次要。","runway_years":"事實表未涵蓋滲透率序列，不估","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 與再投資率事實表未涵蓋，內生天花板無法計算；以管理層所稱加權市場成長率約 7% 作為有機成長上界的代理。","segments":[{"item":"電生理","value":"第三季年減 5%（美國 −8%、國際 +2%）；2027 年預期續失份額，2028 年 Ultra 上市後改善"},{"item":"Watchman","value":"第三季年減 6%（美國 −7%、國際 +4%）；美國併行手術 +35%、單獨手術年減高十位數"},{"item":"介入心臟","value":"第三季 +19%，影像與藥物塗層產品帶動"},{"item":"神經調節","value":"第三季 +13%"},{"item":"介入腫瘤與栓塞","value":"第三季 +5%，部分供應受限到 2027 年初"},{"item":"周邊血管","value":"第三季 +1%，TCAR 供應受限"},{"item":"內視鏡","value":"第三季 −1%（含中國集採與網攻），2027 年第四季前受集採壓抑"},{"item":"泌尿","value":"第三季 −3%，管理層承認先前對成長的判斷錯誤"},{"item":"心律管理","value":"第三季 −2%，2028 年 Denali 上市後預期回升"},{"item":"各分部營收占比","value":"事實表未涵蓋；管理層稱電生理加 Watchman 約占 25%"}],"decay_signals":[{"signal":"毛利率連2季YoY下滑","lit":true,"evidence":"第三季調整後毛利率 68.0%，年減 300 個基點；全年預期低於 2025 年，2027 年管理層預告顯著壓力（前瞻確認）"},{"signal":"核心市占近12個月縮減","lit":true,"evidence":"PFA 份額由約 58% 往 48%–50% 移動"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"PFA 單價仍穩，份額流失不是提價造成"},{"signal":"EPS CAGR顯著高於Rev CAGR","lit":false,"evidence":"共識 EPS 與營收成長都在低個位數"},{"signal":"FCF/NI<0.75連2年","lit":false,"evidence":"2024、2025 年自由現金流對淨利約 1.28、1.17 倍；同業表 TTM 數字與公司公布數不符，不採"},{"signal":"SBC/Rev>5%且逐年上升","lit":null,"evidence":"事實表未涵蓋"},{"signal":"TAM萎縮或被替代技術壓縮","lit":true,"evidence":"美國 LAAC 市場年減約 7%–8%，單獨手術轉診受臨床證據影響"},{"signal":"產業估值倍數近3年系統性下移","lit":null,"evidence":"同業倍數序列事實表未涵蓋"},{"signal":"maintenance capex占FCF>60%","lit":false,"evidence":"第三季資本支出 1.8 億美元，對自由現金流 8.67 億美元，總資本支出也遠低於 60%"},{"signal":"停止投資新產能且收入3年內下滑","lit":false,"evidence":"持續投資新品與供應鏈"}],"trap_rating":"價值陷阱風險🔴（三項亮燈）；長期成長性🔴"},"quality":{},"governance":{"capital_returns":[{"item":"Penumbra 收購","value":"EV 約 145 億美元、每股約 374 美元；FTC 二次審查中，預計 2027 年第一季初交割；首年稀釋 0.06–0.08 美元，因利率上升擴大"},{"item":"MiRus 投資","value":"15 億美元，含收購其 TAVR 事業的獨家選擇權（2026-07-29 法說）"},{"item":"加速回購","value":"20 億美元，已完成（2026-07-29 法說）"},{"item":"VITALYST 共同出資","value":"Blackstone 出資沖減研發費用，2030 年起依里程碑領回本金報酬加銷售權利金"},{"item":"重組計畫","value":"稅前費用 7–8 億美元，其中 6–7 億為現金；年化節省約 5 億美元，2027 年底前實現過半"},{"item":"股息","value":"資本配置優先順序只列併購與回購，未提股息"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"收購投入資本與增量營業利益事實表未涵蓋；Axonics 整合不順、Silk Road 與 Nalu 順利（2026-10-28 法說）；Penumbra 稀釋擴大","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"20 億美元加速回購已完成（2026-07-29 法說），買入均價與當時 10 年期殖利率事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"2023–2025 年稀釋股數約 14.8–14.9 億（淨利÷稀釋 EPS 自算），2026 年第三季 14.52 億，年均淨稀釋低於 1.5%","grade":"過"}]},"valuation":{"basis":"Forward P/E（主錨 FY2027E 共識，FY2026E 已近年底）加 PEG；EV／營收作輔助","tier":"大型多元醫材（與 Medtronic、Abbott、Stryker 同層）","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業 Forward P/E；唯一可得的同業倍數是前份判斷記載的 Medtronic 約 12.2 倍（2026-07），已過期，只作終端倍數的參照，不作主錨。"},"fwd_pe":13.86,"peg":3.8,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價對今年共識 EPS 約 13.9 倍、對明年約 13.8 倍；trailing 本益比、市售率、EV／營收都位於近四個年度端點的最低，但這只是四個點，五年連續分位事實表未涵蓋，所以不填五年分位。三年 EPS 年複合僅約 3.7%，成長調整後約 3.8 倍；明年分母高於管理層「難以成長」的說法，也未計入 Penumbra 稀釋，仍在下修。絕對倍數低與成長調整後偏貴互相抵銷，結論為合理。","upside_short_pct":4.5,"upside_mid_pct":32.8},"trap_analysis":{"verdict":"🔴","label":"低倍數伴隨共識連續下修，三項衰退信號亮燈"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"PFA 份額一年由約 58% 掉到 50% 上下，管理層預期 2028 年初前續失；Medtronic 已在歐洲推出 Sphere-360，分析師提問點出 2028 年還有新波形對手；Watchman 美國單獨手術年減高十位數，2027 年新對手進場。","assumption":"多頭假設電生理與 Watchman 2027 年見底、2028 年隨新品回升。","consequence":"若 Ultra 延後、份額跌破 35%、LAAC 續縮，2031 年 EPS 停在約 3.1 美元、倍數壓到 10 倍，股價約 31 美元，較現價 −30%；再加上 Penumbra 交割後的槓桿與訴訟，五年虧 40%–50% 有路徑。","ruling":"採納：這是悲觀情境的主體，機率給 35%；與唯一致命點（Ultra 延後）部分重疊，已併入同一條監測。","watch":"美國電生理季營收年增率、Ultra 核准進度","evidence_refs":["competitive_share_entrants#2","substitute_technology#2","end_markets#2","supply_demand_durability#0","competitive_share_entrants#3"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Penumbra 約 145 億美元，首年稀釋 0.06–0.08 美元且因利率上升擴大；MiRus 投資 15 億美元；VITALYST 改由 Blackstone 出資，2030 年起要付報酬與權利金；第三季約 8,000 萬、第二季約 7,500 萬美元產品責任費用；AXIOS 召回涉及 3 起死亡。","assumption":"營收回升就等於股東報酬回升。","consequence":"2028 年後營收回到 7%–8% 成長，但成長靠高價收購與分潤換來，增量報酬低於過去，每股盈餘年增只有 5%–6%，倍數也回不到過去水準。","ruling":"部分採納：基準情境 EPS 年增只給 7%–9%、終端 16 倍，不假設回到過去的高倍數；增量報酬缺資料，列為資料缺口。","watch":"Penumbra 交割後的稀釋幅度、毛負債槓桿、產品責任費用","evidence_refs":["regulatory_antitrust#0","product_recall_warning#0","major_events#4","lawsuit_class_action#0"],"fact_refs":["f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY2027 共識 3.19 美元仍高於管理層的第四季年化基準 3.08–3.16 美元，且未必含 Penumbra 稀釋；賣方目標均價 63–72 美元、評等多為買進。","assumption":"現價約 13.9 倍已反映最壞情況。","consequence":"若 2027 年 EPS 落在 3.00–3.05 美元、倍數維持 13–14 倍，股價約 39–43 美元，仍有 3%–12% 下行；現價反映的是共識，不是管理層自己的說法。","ruling":"採納：現價還沒完全反映管理層的 2027 年框架，不把低倍數當安全邊際。","watch":"1 月的 2027 年指引與共識的差距","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","end_markets#1"],"fact_refs":["f_consensus_eps_fy2","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-40,"hi":-25,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 44.99 → 本次 44.15（-1.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=44.99","side_b":"本次 price_at_dd=44.15","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 44.99 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 44.99 美元：五年期望值 +29.0%，基準年化 7.6%，前份未列不對稱比","side_b":"本次情境、股價仍用 44.99 美元：Bull 價 102、Bear 價 33.07，五年期望值 +38.3%，基準年化 8.4%，不對稱比 2.73","ruling":"先換情境、股價不動：五年期望值多 9.3 個百分點，基準年化多 0.8 個百分點。前份未列不對稱比，本次為 2.73。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 44.99 美元：五年期望值 +38.3%，基準年化 8.4%，不對稱比 2.73","side_b":"本次情境、股價 44.15 美元：五年期望值 +40.9%，基準年化 8.8%，不對稱比 2.98","ruling":"再換股價、情境不動：起點價下跌 1.9%，五年期望值多 2.6 個百分點，基準年化多 0.4 個百分點，不對稱比由 2.73 升到 2.98。合計五年期望值比前份多 11.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2027 年谷底、2028 年回升，對上新品延後與份額流失","cause":null,"prior_field":null,"side_a":"管理層（2026-10-28 法說，CEO Mahoney、CFO Monson）：2027 年是這個循環的谷底，2028 年營收與 EPS 明顯改善，2029 年再加速；依據是 ICE、Ultra、Denali、Penumbra 與 5 億美元節省。","side_b":"同一場法說承認大型平台平均延後約半年，Ultra 延到 2028 年初、FARAFLEX 延到 2029 年；分析師點出 2028 年有新波形 PFA 對手；PFA 份額一年掉約 10 個百分點，說明醫師換用成本低。","ruling":"方向相反、不可調和。採 B 側作基準：電生理出現止跌季報之前，不採信 2028 年回升時點。依據是今年三次下修與三個主要平台延後的實際紀錄。","evidence_level":"管理層前瞻說法，對上已發生的延後紀錄與獨立份額調查","settle_metric":"美國電生理季營收年增率（2027 下半年）、Ultra 核准日","if_then":["若 2027 下半年美國電生理連 2 季年減收斂到 5% 以內，且 2027 年共識 EPS 連 2 個月不再下修 → 重跑研究，通過後首倉 2%","若股價先漲回 52 週均線（約 63 美元）但電生理仍年減超過 5% → 不追","若股價跌破 38 美元且電生理年減已收斂到 5% 以內 → 分批反買，首筆 1%","反向條件：若電生理連 2 季年減超過 10% 或 Ultra 再延 → 維持迴避，樂觀情境機率降到 10%"],"evidence_refs":["end_markets#2","substitute_technology#1","competitive_share_entrants#1","substitute_technology#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"約 13.9 倍本益比是近年最低；其餘四分之三業務仍約 6% 成長，介入心臟 +19%；重組 5 億美元節省過半在 2027 年底兌現；Penumbra 補上高成長血管業務；CHAMPION-AF 達到全部主要終點，一線標示若在 2028 年前核准，Watchman 有上檔；賣方目標均價 63–72 美元。","side_b":"倍數低是因為分母在掉：FY2027 共識三個月內續降，管理層自己說 2027 年難成長；大型平台延後約半年的情況已發生多次；PFA 份額一年轉移約 10 個百分點。","ruling":"採 B 側：分母穩定前，低倍數不算便宜。A 側的每一項都要到 2027–2028 年才能驗證，現在進場等於提前一年替管理層的時程背書。","evidence_level":"事實層：雙方數字都有來源，分歧在時點","settle_metric":"2027 年 1 月指引與共識的差距","if_then":["若 2027 年指引 EPS ≥3.15 美元且已含 Penumbra → 提前檢查重跑研究的三項條件","若指引低於 3.00 美元 → 維持迴避，悲觀情境機率上調到 40%"],"evidence_refs":["capital_markets_pricing#3","substitute_technology#3"]},{"axis":"管理層 7 月說法與 10 月結果","cause":null,"prior_field":null,"side_a":"2026-07-29 法說（CEO Mahoney、CFO Monson）：第三季有機成長 3%–5%、全年調整後 EPS 3.28–3.32 美元；Penumbra 下半年交割；Ultra 與 ICE 2027 下半年、FARAFLEX 2028 年；2027 年目標優於 2026 下半年指引。","side_b":"2026-10-28 法說：第三季 1.5%（網攻約 300 個基點）、全年 EPS 下修到 3.16–3.18 美元；Penumbra 延到 2027 年初；Ultra 延到 2028 年初、FARAFLEX 延到 2029 年；2027 年改口為營收與 EPS 都難成長。CFO 自承「需要重建對預測的信心」。","ruling":"管理層時程的可信度低。本判斷 2027 年基準採管理層新說法再扣 Penumbra 稀釋，不採賣方共識。","evidence_level":"公司自己的兩次法說","settle_metric":"2027 年指引達成率","if_then":["若 2027 年前兩季實績都落在指引區間內 → 恢復採信管理層時程，樂觀情境機率可回到 25%","若任一季再低於指引下緣 → 2028 年回升時點順延一年計算"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2","end_markets#1"]},{"axis":"網攻是否只是一次性","cause":null,"prior_field":null,"side_a":"管理層：網攻使第三季營收少約 300 個基點、EPS 少 0.07 美元；第四季因客戶消化補庫存再拖 200–300 個基點、EPS 0.04–0.05 美元，屬一次性。","side_b":"同一場法說也說網攻加速了電生理份額轉移，回不來的份額不是一次性；全年下修還包括中國價格與電生理競爭。","ruling":"未證、監測。預先設定判準：若 2027 年第一季（不再有網攻影響）有機成長仍低於 0%，則「網攻是主因」的說法視為證偽，2027 年 EPS 基準再下調。","evidence_level":"管理層歸因，未有第三方佐證","settle_metric":"2027 年第一季有機成長率","if_then":["若 2027 年第一季有機成長 ≥2% → 採信一次性歸因，基準情境不動","若低於 0% → 基準 2027 年 EPS 由 3.08 美元下調到 3.00 美元"],"evidence_refs":["major_events#3","end_markets#0"]},{"axis":"估值結論由偏便宜改為合理","cause":"新證據","prior_field":["val"],"side_a":"前份（2026-07-10，股價 44.99 美元）：12 倍遠期本益比視為估值底，估值結論偏便宜。","side_b":"本次（44.15 美元）：股價幾乎沒變，但 FY1 共識三個月下修 4.2%，FY2027 與 FY2028 共識財報後再降；管理層說 2027 年難成長。分母本身成為爭點，便宜的說法不成立，改為合理。","ruling":"歸因新證據（分母下修），不是價格變動。","evidence_level":"共識快照與公司指引","settle_metric":"2027 年共識 EPS","if_then":[],"evidence_refs":["capital_markets_pricing#2","end_markets#1"]},{"axis":"基本面判斷維持同向","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：迴避、不持有；陷阱風險高；護城河向下；五年後跑道中等；歸類品質複利成長；不適用循環位置。","side_b":"本次輸入方向相同：第三季第三次下修、Ultra 與 FARAFLEX 延後、PFA 份額續失、Watchman 單獨手術年減高十位數，都在強化原判斷；歸類加註轉機特徵，主類不變。","ruling":"維持。變動來源是新證據強化，不是方法或價格；最終結論與角色另由規則計算。","evidence_level":"公司季報與法說","settle_metric":null,"if_then":[],"evidence_refs":["capital_markets_pricing#1","substitute_technology#2"]},{"axis":"最大回撤與三情境機率的表達方式","cause":"方法變動","prior_field":["max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份最大回撤記為單點 −40%，三情境機率未記錄。","side_b":"本次最大回撤改為 −25%～−40% 的範圍；三情境機率樂觀 20%、基準 45%、悲觀 35%。","ruling":"屬方法變動：回撤改寫範圍、機率明列。悲觀機率 35% 高於一般的 25%–30%，理由是護城河向下且共識仍在下修。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份假設門檻已被擊穿，本次改為止跌與回升型門檻","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份 H1：PFA 份額 ≥40%、美國電生理有機成長 ≥+8%；H2：公司整體有機成長守 6.5%–8%；H3：遠期本益比 ≥12 倍且共識不再下修；R1 警戒：連 2 季有機 <+5% 或份額 <38%。","side_b":"第三季美國電生理年減 8%，全年有機成長約 3.75%，FY1 共識三個月下修 4.2%；H1、H2 已反轉，H3 倍數仍在 12 倍以上但共識續降。本次假設改為「其餘業務撐住、兩引擎見底、EPS 回升」，風險改用年減幅度門檻。","ruling":"屬新證據：前份門檻建立在成長延續的前提上，前提已破，沿用只會一直亮燈、沒有判讀力。新門檻針對 2027–2028 年的見底與回升；已持有者觸及任一條即減碼。","evidence_level":"公司季報實績","settle_metric":"美國電生理季營收年增率","if_then":[],"evidence_refs":["capital_markets_pricing#1","end_markets#0"]},{"axis":"重新研究條件改寫（重跑研究後才考慮進場首倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"3-of-3 AND 全數成立方重跑 DD：① US EP 有機成長連 2 季止穩且份額止跌；② Penumbra 整合無減損、槓桿回落；③ 證券集體訴訟/聯邦調查落地無重大裁罰或給付風險。任一未過即維持迴避。","side_b":"三項同時成立才重跑研究：①美國電生理連2季年減收斂到5%以內②2027年共識EPS連2個月不再下修③1月給的2027年指引在第一季財報未下修","ruling":"舊條件②③改列風險觸發：Penumbra 交割延到 2027 年初，訴訟沒有可預期的結案日，兩者一年內都不可能落地，綁在重跑條件會讓條件永遠不成立。新增共識與指引兩項，因為本次的約束是分母仍在下修。進場動作：三項同時成立才重跑研究，通過後首倉 2%。","evidence_level":"公司法說與共識快照","settle_metric":"美國電生理季營收、2027 年共識 EPS","if_then":[],"evidence_refs":["regulatory_antitrust#0","lawsuit_class_action#0"]},{"axis":"Single Thing 由未設改為 FARAWAVE Ultra 上市時點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）。","side_b":"FARAWAVE Ultra 未能在 2028 年上半年前取得 FDA 核准並上市（目前公司說 2028 年初）。","ruling":"第三季法說宣布 Ultra 由 2027 下半年延到 2028 年初，管理層並說 Ultra 上市前電生理份額會持續流失；電生理止跌是基準情境 2028 年回升中最大的單一變數，所以設為唯一致命點。若發生，已持有者減碼，未持有者維持迴避。","evidence_level":"公司兩次法說的時程對照","settle_metric":"Ultra FDA 核准日","if_then":[],"evidence_refs":["substitute_technology#1","end_markets#2"]},{"axis":"減碼指標由未設改為五項","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設。","side_b":"美國電生理連 2 季年減 >10%；2027 年共識 EPS <3.00 美元；調整後毛利率任一季 <67%；美國 Watchman 連 2 季年減 >10%；Penumbra 交割後毛負債槓桿連 4 季 >3.5 倍。","ruling":"前份只有假設與風險表，沒有可執行的減碼指標，本次補上。觸及任一項時，已持有者減碼，未持有者維持迴避。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"美國電生理止跌，是重跑研究的第一個條件","type":"假設驗證","maps_to":"H2","metric":"美國電生理季營收年增率","threshold":"2027 下半年連 2 季年減收斂到 5% 以內","action":"列入重跑研究三項條件之一","source_freq":"季報，每季","date":"2027-10","evidence_refs":["end_markets#2"]},{"n":2,"text":"PFA 份額流失加速","type":"風險","maps_to":"R1","metric":"美國電生理季營收年增率","threshold":"連 2 季年減超過 10%","action":"維持迴避，悲觀情境機率上調到 40%","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#2","substitute_technology#1","substitute_technology#2"]},{"n":3,"text":"FARAWAVE Ultra 再延後","type":"Single Thing","maps_to":"single_thing","metric":"Ultra FDA 核准與上市","threshold":"2028-06-30 前未上市","action":"維持迴避，樂觀情境機率降到 10%；已持有者減碼","source_freq":"法說與 FDA 公告","date":"2028-06","evidence_refs":["substitute_technology#1"]},{"n":4,"text":"Watchman 市場續縮並被新對手分食","type":"風險","maps_to":"R2","metric":"美國 Watchman 營收年增率","threshold":"2027 年連 2 季年減超過 10%","action":"維持迴避，2028 年回升假設下修","source_freq":"季報，每季","date":null,"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","end_markets#3","competitive_share_entrants#3"]},{"n":5,"text":"集採與低價競爭壓毛利","type":"風險","maps_to":"R3","metric":"調整後毛利率","threshold":"2027 年任一季低於 67%","action":"維持迴避，基準 EPS 路徑下修","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"n":6,"text":"關稅吸收失敗","type":"風險","maps_to":"R3","metric":"全年調整後營業利益率","threshold":"較前一年下滑超過 100 個基點，且公司歸因關稅","action":"視為關稅吸收失敗，維持迴避","source_freq":"季報與年報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1"]},{"n":7,"text":"Penumbra 監管結果","type":"風險","maps_to":"R4","metric":"FTC 審查結果","threshold":"FTC 起訴阻擋，或要求剝離栓塞重疊業務","action":"重算情境：阻擋則 EPS 不再稀釋、成長下修；剝離則重估稀釋","source_freq":"公司公告","date":"2027-03","evidence_refs":["regulatory_antitrust#0"]},{"n":8,"text":"證券集體訴訟與政府調查","type":"風險","maps_to":"R4","metric":"訴訟程序進度","threshold":"法院准許集體認證，或出現刑事程序","action":"已持有者：集體認證加上不利和解減碼一半，刑事介入清倉；目前不持有則維持迴避","source_freq":"季報法律事項揭露","date":null,"evidence_refs":["lawsuit_class_action#0","major_events#1","regulatory_antitrust#1"]},{"n":9,"text":"召回與營運中斷再發生","type":"風險","maps_to":"R5","metric":"Class I 召回與停工天數","threshold":"新增 Class I 召回涉及前五大產品線，或停工超過 5 個營業日","action":"維持迴避，執行面評分再扣","source_freq":"FDA 公告與 8-K","date":null,"evidence_refs":["product_recall_warning#0","major_events#4","major_events#3"]},{"n":10,"text":"管理層第四次下修","type":"風險","maps_to":"R5","metric":"2027 年全年 EPS 指引","threshold":"1 月給出的指引在年內任一季再下修","action":"維持迴避，重跑研究條件重新計時","source_freq":"季報，每季","date":null,"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2","end_markets#0","end_markets#1"]},{"n":11,"text":"重跑研究的三項條件","type":"估值rearm","maps_to":null,"metric":"美國電生理季營收、2027 年共識 EPS、2027 年指引","threshold":"三項同時成立：電生理連 2 季年減收斂到 5% 以內、共識連 2 個月不再下修、第一季財報未下修指引","action":"重跑研究，通過後首倉 2%","source_freq":"季報與共識快照","date":null,"evidence_refs":[]},{"n":12,"text":"2027 年指引公布","type":"複審日期","maps_to":null,"metric":"2027 年 EPS 指引","threshold":"管理層 1 月給出指引時","action":"比對指引與本判斷 2027 年基準 3.08 美元，差距超過 5% 即重算情境","source_freq":"公司公告","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"美國電生理季營收年增率","bear_threshold":"連 2 季年減超過 10%","window":"2027 全年","source":"公司季報新聞稿與法說","last_status":"warning"},{"metric":"2027 年度共識 EPS","bear_threshold":"低於 3.00 美元","window":"2027-01 至 2027-06","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"調整後毛利率","bear_threshold":"任一季低於 67%","window":"2027 各季","source":"公司季報","last_status":"warning"},{"metric":"美國 Watchman 營收年增率","bear_threshold":"連 2 季年減超過 10%","window":"2027 全年","source":"公司季報事業別揭露","last_status":"warning"},{"metric":"毛負債槓桿","bear_threshold":"Penumbra 交割後連 4 季高於 3.5 倍","window":"2027-03 至 2028-06","source":"公司季報與法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"目前不持有；重新進場後，Ultra 核准前上限 4%","requires_critic":[],"rearm_trigger":"三項同時成立才重跑研究：①美國電生理連2季年減收斂到5%以內②2027年共識EPS連2個月不再下修③1月給的2027年指引在第一季財報未下修","exec_line":"重跑研究通過後首倉 2%；第二個電生理止跌季報後加到 4%；Ultra 核准前不超過 4%"},"reasoning":{"industry":"第三季營收 51.38 億美元，年增 1.5%（公司估網攻拖累約 300 個基點）。GAAP 營業利益 8.28 億美元、利益率 16.1%（含約 8,000 萬美元產品責任費用）；調整後營業利益 13.64 億美元、利益率 26.5%；調整後毛利率 68.0%，年減 300 個基點。調整後 EPS 0.73 美元，低於 7 月指引 0.80–0.82 美元。第四季指引營收年減 1%–3%、EPS 0.77–0.79 美元，全年 EPS 3.16–3.18 美元。分部營收占比事實表未涵蓋，法說可得的是：電生理（第三季 −5%，美國 −8%）與 Watchman（−6%，美國 −7%）合計約占四分之一；介入心臟 +19%、神經調節 +13%、介入腫瘤與栓塞 +5% 撐住；泌尿 −3%、內視鏡 −1%、心律管理 −2% 偏弱。2025 年國際營收占 36%，無單一客戶超過 10%，GPO 與醫院網絡是主要買方。單點依賴：客戶端沒有；產品端是電生理與 Watchman 兩條線，過去三年多數成長來自這裡；供應端有部分材料單一來源。產業時鐘在第三階段：美國房顫消融約八成已改用 PFA（2026-07-29 法說），成長由滲透轉為四家搶份額。產業態勢三軸：競爭面惡化中（PFA 四家同場，LAAC 2027 年有新對手）；結構面需求隨人口老化持久，但中國集採是結構性降價；其他變數是 FTC 對 Penumbra 的二次審查與美國醫材關稅。裁決：競爭惡化中。","moat":"機制：導管室與內視鏡室的整套產品加上臨床數據，讓醫師用慣了就不想換；Watchman 在 LAAC 份額約 91%（2026-07-29 法說）。同業 ROIC 事實表未涵蓋，改看份額與利潤率判方向。份額：醫師調查預期 PFA 份額由 2025 年約 58% 降到 2026 年約 48%，J&J 由 11% 升到 20%；2026 年 9 月法人會議摘要稱已在 50% 上下，且流失快於預期；管理層在 10 月法說承認，2028 年初 FARAWAVE Ultra 上市前會持續流失。利潤率：TTM 毛利率 69.9%，高於 Medtronic 65.0%、Stryker 65.0%、Abbott 56.6%，低於 Edwards 77.8%；營業利益率 21.1%，與 Stryker 21.7% 相當、高於 Medtronic 19.0%。定價權評 7 分：PFA 單價目前仍穩，毛利率仍高於多數同業；但中國集採擴大、低價廠商進場、LAAC 2027 年有新對手，方向是縮減。執行評 5 分：一年三度下修指引、大型平台平均延後約半年、Axonics 整合不順、網攻停工約兩週、AXIOS 與脊髓刺激導線召回，方向也是縮減。可能看錯的地方：介入心臟 +19%、神經調節 +13%，代表多數事業的醫師黏著仍強；若 2028 年新品準時，執行分會回升，趨勢可轉為穩定。","growth":"成長組成：2026–2027 年是量的成長被份額流失抵銷，中國價格為負；2028 年起靠新品（2D ICE、FARAWAVE Ultra、FARAFLEX、SEISMIQ、Denali）與 Penumbra 併購，回購排在併購之後。三年共識：FY2026E 3.18、FY2027E 3.19、FY2028E 3.41 美元。以公司「3.16–3.18 美元較 2025 年成長 3%–4%」反推 FY2025 調整後 EPS 約 3.06 美元，三年年複合約 3.7%。營收共識 FY2026 約 209.7 億、FY2027 約 210.3 億美元（28–29 家），兩年幾乎不動。內生天花板：增量 ROIC 與再投資率事實表未涵蓋，無法計算；以管理層所稱加權市場成長率約 7% 作上界代理，共識 3.7% 遠低於此，缺口為負，不需要靠倍數重估解釋。風險在相反方向：共識仍高於管理層「2027 年營收與 EPS 都難成長」的說法，FY2027 與 FY2028 共識在財報後又各降 1.5% 與 3.7%。跑道：PFA 在美國房顫消融的滲透約八成，原本的 S 曲線已走完大半；LAAC 在縮；下一條曲線（IVL、腎神經阻斷、Penumbra、2030 年前 250 億美元新市場）只有管理層說法，且多數已延後，所以評中等。衰退信號亮三項（毛利率、核心份額、LAAC 市場萎縮），價值陷阱風險高，長期成長性評級偏弱。","governance":"自由現金流對淨利：2024 年 23.65／18.54 億美元約 1.28 倍，2025 年 34.04／28.98 億美元約 1.17 倍，轉換品質好；2026 年第三季自由現金流 8.67 億美元，全年指引約 36 億美元。同業表的 TTM 自由現金流利潤率 4.1% 與上述公司數字對不上，可能是資料源把投資或一次性款項計入，不作承重數字。淨負債約 120.85 億美元，毛負債槓桿 1.9 倍（9 月底）。股數：以年報淨利÷稀釋 EPS 推得 2023–2025 年約 14.8–14.9 億股，第三季稀釋加權股數 14.52 億股，加速回購後淨減約 3%，淨稀釋這一項過關。SBC 金額與現金去向四分事實表未涵蓋。併購已實現報酬：Axonics 整合不順（管理層自承），Silk Road、Nalu 順利；Penumbra 首年稀釋原估 0.06–0.08 美元，利率上升後擴大。回購買入均價與當時 10 年期殖利率事實表未涵蓋，無法判定買入收益率。","valuation":"44.15 美元對 FY2026E 共識 3.18 美元約 13.9 倍、對 FY2027E 3.19 美元約 13.8 倍；trailing 本益比 18.6 倍、市售率 3.0 倍、EV／營收 3.6 倍，都在近四個年度端點中最低（只有四個點，不是五年連續序列）。看起來便宜，但分母還在掉：FY1 共識三個月下修 4.2%，財報後 FY2、FY3 又各降 1.5%、3.7%。管理層說第四季指引（EPS 0.77–0.79 美元，年化約 3.08–3.16）是 2027 年的合理基準，EPS 大致跟營收同步，且未計入 Penumbra 稀釋；若 2027 年落在 3.05 美元，現價約 14.5 倍。三年 EPS 年複合約 3.7%，成長調整後本益比約 3.8 倍，以成長看偏貴。賣方目標均價 63–72 美元、評等多為買進，但目標價在指引下修後大幅調降（例如 Needham 由 77 降到 57），只能當作市場仍偏樂觀的證據。短期：2027 年底以 FY2028E 3.32 美元×13.9 倍，約 46.1 美元（+4.5%）。中期：2029 年底以 FY2030E 3.91 美元×15 倍，約 58.7 美元（+32.8%）。同業 Forward P/E 事實表未涵蓋，前份判斷記載 Medtronic 約 12.2 倍（2026-07，已過期），僅作參考。","premortem":"往上看錯的路徑：其餘四分之三業務仍約 6% 成長，重組 5 億美元節省過半在 2027 年底兌現，Penumbra 補上高成長血管業務，CHAMPION-AF 若帶來一線標示，Watchman 有上檔；這些都要到 2027–2028 年才看得到。往下看錯的路徑：股價 26 週跌 22.5%，在 52、104、250 週均線之下，250 週均線斜率約持平，市場沒有止跌訊號，共識還在往下修。最大回撤推估 −25%～−40%：2027 年 EPS 下修到 2.95 美元、倍數壓到 10.5～11 倍，約 −27%～−30%；再疊加 Penumbra 交割後槓桿上升、集體訴訟或新召回的壓力情境，到 −40%。陷阱判定的依據見反證紀錄：低倍數伴隨共識連續下修，三項衰退信號亮燈。"},"plain":{"six":{"how_it_makes_money":"賺醫院與醫師的錢：靠臨床證據和醫師使用習慣，賣高毛利的一次性器材與植入物。過去三年的超額成長卡在電生理脈衝消融與 Watchman 兩條線，這兩條線 2026 年轉為拖累；其餘約四分之三業務仍穩定成長。","moat":"護城河向下：醫師習慣與臨床證據仍在，但最賺錢的兩條線正被對手和臨床證據侵蝕，執行與定價兩面都在縮。","growth":"成長跑道中等：PFA 滲透已近飽和、LAAC 在縮；下一段成長靠介入心臟、周邊血管、Penumbra 與 2028 年後的新品，全部尚未兌現。","capital":"資本配置轉為押注併購：借款做完 20 億美元加速回購後，接著是約 145 億美元的 Penumbra 與 15 億美元的 MiRus；併購報酬事實表未涵蓋，Penumbra 的稀釋已在擴大。","valuation":"現價要成立，需要 2028 年起 EPS 回到高個位數成長、倍數回到 16 倍上下；這要靠已經延後過的新品準時上市，我只部分相信。估值結論為合理，不是便宜。","how_wrong":"最可能看錯的是低估 2028 年新品與 Penumbra 的回升力道；但在證據出現前，三度下修與份額流失讓低倍數更像陷阱。"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"qc48_result":null,"qc48_note":null,"trap":"🔴","val":"🟡","moat":"C","moat_trend":"↓","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":44.15,"week26_return_pct":-22.45,"consensus_rev_3m_pct":-4.22,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"2027 年共識 3.19 美元高於管理層「第四季指引是 2027 年合理基準、EPS 大致跟營收同步」的說法（第四季 0.77–0.79 美元，年化約 3.08–3.16），也未必計入 Penumbra 交割後的稀釋（原估 0.06–0.08 美元，利率上升後擴大）。分母仍在往下修，便宜的說法暫不成立。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"2027 年全年指引（管理層稱 1 月給出）","impact":"高","watch":"2027 年 EPS 指引相對本判斷基準 3.08 美元與共識 3.19 美元"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"Penumbra 交割（待剩餘監管許可，公司稱 2027 年第一季初）","impact":"高","watch":"FTC 是否要求剝離、交割後稀釋與槓桿"},{"date":"2027","date_precision":null,"type":"other","event":"LAAC 新對手在美國上市（公司稱 2027 年；Abbott Amulet 360 已取得 CE）","impact":"中","watch":"Watchman 美國份額由約 91% 下滑的幅度"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"電生理 2D ICE 上市（公司稱 2027 下半年）","impact":"中","watch":"標測系統與 PFA 導管的搭配使用率"},{"date":"2028-03","date_precision":"quarter","type":"product","event":"FARAWAVE Ultra 上市（公司稱 2028 年初）","impact":"高","watch":"是否再延後；上市後份額是否止跌"},{"date":"2028-03","date_precision":"quarter","type":"regulatory","event":"Watchman 依 CHAMPION-AF 擴大為一線標示（公司目標 2028 年前）","impact":"高","watch":"FDA 標示核准與保險給付範圍"}],"_projected_from":"v19"}
```
