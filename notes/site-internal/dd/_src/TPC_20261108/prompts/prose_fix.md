你是 stock-analyst v20 的**散文層（prose）agent**，標的 TPC（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：TPC　日期：2026-11-08　archetype：None　前份裁決：2026-05-25　B 衛星候選｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1789B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（494B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（915B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1449B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（997B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（547B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（846B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2119B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3423B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2598B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1789           3648-5211      5 條（2–6 內）  
s3                  8000         494           5254-7506      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3361          8147-11639      5 條（2–6 內）  
s6                 11000         547          7317-10453      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         846           1858-2654      5 條（2–6 內）  
s10                 5000        2119           2017-2881      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2598           2000-2402      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4663B；至少需散文≈40.34KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65
−65%
−53%
−40
−40%
−34%
−5.4%
−2.95%
−2.4%
−1.3%
0%
0
0.06
0.09
0.2%
0.3
0.4
0.4%
0.45
0.48
0.63
0.7
0.71
0.75
0.80
0.85
1.0
1
1.1%
1.15
1.2%
1.25
1.30
1.3
1.4%
1.5
1.5%
1.51
1.62
1.7
02
2
2.1
2.13
2.7
2.86
2.9
03
3
3.1
3.5%
3.79
3.8
4
04
4.04
4.2
4.4
4.6
5
05
5%
5.04
5.10
5.38
5.41
5.5
5.64%
5.67
5.90
6
06
6%
6.00
6.0%
6.07
6.10
6.2
6.4%
6.60
6.625%
6.65
6.81%
6.9
7
07
7.07
7.11%
7.3%
7.40
7.4
7.5%
7.5
7.67
7.8
8
8%
08
8.0%
8.2
8.3
8.46%
8.60
8.6
8.69
8.9
8.94
9
9%
10
10%
10.2
10.6%
10.75%
10.8%
11
11%
11.3
11.4
11.5%
11.75%
11.875%
12
12%
12.5
12.8%
13%
13
14
14%
14.3
14.81
14.98
15.0
15
15%
16%
16.08%
16.66%
16.7
16.71
17
17.2
17.6%
18
18.62%
19.46%
21.5
22%
23.5%
24
25%
25
25.5%
26
26%
29%
30%
30
31.14
31.4
33%
33.4%
34.18
35%
35
41
42
45
46
49
50
50%
52%
52
58.97
59%
64.8%
70
72.76
76
77%
78
86%
86.50
89.89
90
100
100%
104
113.25
120
150%
160
190
$200
203.5
204
212.5
220
250
2014
2018
2022
2023
2024
2025
2026
2027
2028
2029
2031
20261108
1,930
2,000
2,100
3,400
5,000
5,100
5,330
5,400
6,500
7,500
8,044
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
{"meta":{"ticker":"TPC","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Tutor Perini"},"oneliner":"大型基建承包商 Tutor Perini 在手訂單 204 億美元，2026 年調整後 EPS 指引上修到 5.90–6.10，獲利能見度到 2028 年；但 Civil 利潤率處於高區，現價約 15 倍指引，基礎情境年化僅約 6%，不追價，等回檔或利潤率再獲驗證。","thesis":{"H":[{"id":"H1","text":"已簽巨型案按標價利潤率交付，Civil 維持 12–15% 區間，Specialty 於 2027 年進入 5–8%。","2y":"FY2027–FY2028 Civil 年度利益率 ≥13%，Specialty 2027 年內 ≥5%","5y":"FY2031 Civil 利益率仍 ≥11%，調整後 EPS 約 8.6 美元","10y":null,"threshold":"季度 Civil ≥12%；Specialty 於 2027 年底前 ≥5%","source":"公司季報與法說會分部數字","drift_rule":"Civil 低於 12% 連兩季為削弱，連三季且低於 10.8% 為反轉；Specialty 到 2027 年底仍低於 5%，舊案拖累的說法視為不成立。"},{"id":"H2","text":"在手訂單補得上，巨型案持續得標且不犧牲標價。","2y":"在手訂單維持 190 億美元以上，滾動四季訂單出貨比 ≥1.0","5y":"FY2030 Q4 在手訂單 ≥220 億美元","10y":"Civil 與 Building 雙引擎持續，不依賴單一專案週期","threshold":"滾動四季訂單出貨比 ≥1.0；每年至少 2 個 10 億美元以上新案","source":"公司季報新聞稿與法說會得標清單","drift_rule":"滾動四季訂單出貨比連兩季低於 1.0 為削弱，連三季為反轉。"},{"id":"H3","text":"現金流以營運為主，不靠爭議和解；可動用現金累積後開始回饋股東。","2y":"2026–2027 年營運現金流高於調整後淨利，可動用現金 ≥5 億美元","5y":"五年累計 FCF 至少三成透過股利與回購回到股東","10y":null,"threshold":"可動用現金 ≥5 億美元；TTM 營運現金流 ≥調整後淨利","source":"公司季報與法說會現金口徑","drift_rule":"TTM 營運現金流連四季低於調整後淨利為削弱，連六季且偏離 ≥10% 為反轉。"}],"R":[{"id":"R1","text":"固定價格巨型案成本超支，或通膨與關稅無法回收。","h_ref":"H1","clock":"🔥","threshold":"單案累計損失 ≥1 億美元，或 TTM 毛利率跌破 10%（最新 11.75%）","evidence_refs":["reg_tariff_export#0"]},{"id":"R2","text":"高利潤吸引對手回流，或漸進式設計建造壓低標價。","h_ref":"H2","clock":"🐢","threshold":"公司下修 Civil 區間，或連續四季未得 10 億美元以上新案","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"前兩大客戶 2025 年合計占營收 25.5%，專案取消或延付會同時影響多個部門。","h_ref":"H2","clock":"🔥","threshold":"單一客戶占比 >25%，或前兩大客戶專案遭取消、延付","evidence_refs":["customer_concentration_credit#0"]},{"id":"R4","text":"舊爭議結算低於帳面，未請款成本餘額 7.67 億美元約為市值 16%。","h_ref":"H3","clock":"🔥","threshold":"單季舊爭議結算損失 ≥5,000 萬美元","evidence_refs":[]},{"id":"R5","text":"創辦人 Ronald Tutor 持股賣壓，沿用前份指標；本包未涵蓋持股現況，屬資料缺口。","h_ref":"H3","clock":"⚡","threshold":"Form 4 單次賣出超過 100 萬股且股價急跌 15%","evidence_refs":[]},{"id":"R6","text":"聯邦預算或環評拖慢印太與基建案。CEO 稱多數資金來自州與地方，2027 年展望未計新聯邦資金。","h_ref":"H2","clock":"🐢","threshold":"Black 待決三案約 10 億美元到 2027 年中仍未決標；前份聯邦支出年增門檻在摘要中不完整，資料缺口","evidence_refs":[]}],"single_thing":{"description":"九大巨型案任一出現重大成本超支，單案累計認列損失達 2 億美元以上。","why_fatal":"Civil 占部門營業利益 77%。2 億美元損失稅後約每股 2.7 美元，約為基礎情境 FY2027 EPS 的四成；市場也可能重新用虧損年代的眼光定價，倍數由 15 倍往 10 倍靠近。Civil 利潤率每掉 100 個基點，年 EPS 約少 0.48 美元，是模型最大的單一敏感度。","if_happens":"清倉，不等下一季解釋，因為超支通常分季認列。","how_monitor":"每季 10-Q 的專案調整揭露、法說會對九大案進度的描述、Civil 利潤率與未請款成本餘額變化。","probability":"12–24 個月約 15%。固定價格案過去確實出過事，案子越到後期越看得出超支；條款改善與材料買斷壓低機率。此機率為判斷，無統計基礎。"}},"appendix_a":{"growth_durability":6,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.81,"peg_fy2":1.15,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.51,"FY2026E":5.38,"FY2027E":6.07,"FY2028E":null},"fy_end_month":12,"eps_basis":"FY2026E、FY2027E 為 Koyfin 調整後 EPS 共識，未反映 2026-11-04 指引上修（5.90–6.10）。FY2028E 共識事實表未涵蓋，留空。FY2025A 1.51 為 GAAP 稀釋 EPS，調整後口徑事實表未涵蓋，與共識口徑不同，不可用來算 CAGR。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"盈餘由巨型案承接週期與固定價格風險決定；2022–2024 連三年虧損後翻正，訂單能見度長但不是複利型生意。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉，時點不在 2028 年前。需求端多為州與地方資金，CEO 稱未受聯邦政策阻礙；供給端的對手減少可逆。來源：10-K FY2025 與 2026-11-04 法說。","bargaining":{"up":"對材料商與分包商較強：得標後買斷鋼材、混凝土並簽固定價分包，把漲價風險往上游轉；電工在部分地區短缺是弱點。","down":"對業主改善中：投標者少，合約條款較平衡；但每案重新競標，沒有轉換成本。","geo":"國際及美屬地營收占 9%，Black Construction 的印太軍事案受環評時程影響。"},"profit_pool_dir":"利潤往願意承擔大型固定價格風險的少數業者集中；五年營業利益池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與份額數據，滲透率框架也不適合逐案競標的工程業；改用管理層揭露的 2,000 億美元管線與 204 億美元訂單判斷，且管線屬管理層口徑，未經第三方驗證。"}},"moat":{"mechanism":"大型固定價格案的保證額度、複雜工程經驗與資產負債表，加上投標對手減少。","execution":6,"pricing":6,"grade":"C","trend":"↑","trend_evidence":"2026-11-04 法說，CEO Gary Smalley 稱新案以更高利潤率投標，Civil 區間短中期有上行壓力，九大案約 9 勝 12。10-K 也寫大型固定價格案競爭減少。此判斷只代表近三年方向，主要來源是公司自述與公司利潤率，反向訊號列在威脅。","peer_na_reason":"同業 ROIC 事實表未涵蓋，只有毛利率、營益率與 FCF 利潤率。","threats":[{"level":"🟡","text":"漸進式設計建造若成為主流，投標門檻下降，部分案件毛利被壓低；10-K 已列為風險，目前沒有實際案例數字。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"高利潤吸引區域業者回流。2026-08-05 法說 Steven Fisher 提問時，CEO Gary Smalley 未正面回答；2026-11-04 法說 CEO 也說不預期再有九大案那樣的得標率。","p":35,"evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×高周轉（方向判斷，周轉率事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是民眾，決策與付款者是公共機關，政府客戶占訂單 86%；基建更新屬必要支出，CEO 稱多數資金來自州與地方。風險是時程延後，例如 Black 最大待決案仍在等環評。"},{"item":"決策層級","level":"🟡","text":"決策單位是單一專案，每案重新競標，開工後才有換手成本。代理變數是得標率：約 9 勝 12，但 CEO 自己說不預期維持。"},{"item":"價值鏈分配","level":"🟡","text":"公司能把材料風險轉給供應商與分包商，但合資夥伴也分走利潤，2026 年非控制權益預估 6,500–7,500 萬美元；單獨投標可收回一部分，代價是自己承擔全部風險。TTM 毛利率 11.75% 為五家最低。"},{"item":"社會容忍度","level":"🟡","text":"客戶用公共資金，14% 的 Civil 利潤率與過去爭議史都容易受檢視；業主轉向漸進式設計建造本身就是分攤風險、壓低承包商議價力的做法。實際定價上限受公共預算與採購制度約束。"}],"roiic":"事實表未涵蓋投入資本，無法計算。","reinvest_rate":"資本支出中值 1.30 億減折舊攤銷 0.45 億為 0.85 億美元，其中 0.75–0.85 億由業主出資；扣除後接近零，營運資金近年是現金流入，再投資率接近零或為負。ΔWC 與 NOPAT 完整數字事實表未涵蓋。","endo_ceiling":null,"formula_note":"公式在本公司失靈：成長主要由客戶進度款支應，再投資率接近零，算出來的內生成長沒有意義。實際天花板是保證額度、工程人力與得標率。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","TPC":11.75,"GVA":16.08,"STRL":23.78,"PWR":15.76,"FIX":25.57,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","TPC":5.64,"GVA":7.11,"STRL":18.62,"PWR":6.81,"FIX":16.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","TPC":10.75,"GVA":8.36,"STRL":10.93,"PWR":8.46,"FIX":19.46,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"GVA","gm":16.08,"om":7.11,"fcf_margin":8.36,"strategy_note":"營益率 7.11%、毛利率 16.08%，都高於 TPC；TPC 的 FCF 利潤率 10.75% 較高，但含訂單早期收款效果，不代表賺錢能力較強。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"STRL","gm":23.78,"om":18.62,"fcf_margin":10.93,"strategy_note":"營益率 18.62%，是 TPC 的三倍多；差距太大，不作同層級估值錨。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PWR","gm":15.76,"om":6.81,"fcf_margin":8.46,"strategy_note":"營益率 6.81% 接近 TPC，FCF 利潤率 8.46%；業務組合事實表未涵蓋，只作利潤率參考。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"FIX","gm":25.57,"om":16.66,"fcf_margin":19.46,"strategy_note":"營益率 16.66%、FCF 利潤率 19.46%，顯示專業工程商的利潤上限遠高於 TPC 的 Specialty 3.5%，但業務差異未經事實表驗證。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主、利潤率次之，無併購，回購金額事實表未涵蓋。","runway_years":"約 5 年：訂單約 3.1 倍年營收，施工峰值約 2028 年下半，之後靠補單。","runway_post_y5":"🟡","endo_ceiling_basis":"公式不適用，改用訂單消化與保證額度判斷；管線逾 2,000 億美元為管理層口徑，保證額度數字事實表未涵蓋。","segments":[{"item":"Civil","value":"Q3 營收 8.94 億美元，年增 16%，利益率 14%，區間 12–15%；占 2026-06-30 訂單約 50%。"},{"item":"Building","value":"Q3 營收 5.41 億美元，年增 29%，利益率 5%，區間 3–6%；占訂單約 35%，另有約 7.5 億美元預建案待轉入訂單。"},{"item":"Specialty Contractors","value":"Q3 營收 2.86 億美元，年增 26%，利益率 3.5%，管理層目標 2027 年內進入 5–8%；占訂單約 15%。"}],"decay_signals":["EPS 成長遠高於營收成長：Q3 調整後 EPS 年增 59%，營收年增 22%，差距來自利潤率回升，已亮燈。","核心市占、產業倍數變化與維護性資本支出占比事實表未涵蓋，未計入。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購或回購，且現金去向四分與回購均價事實表未涵蓋，展開只能列片段數字。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月無併購，管理層把併購列為現金用途最後一項。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購授權餘額 1.7 億美元（2026-08-05 法說），買回金額與均價事實表未涵蓋，無法比較。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY2025 由淨利 8,044 萬美元除以 EPS 1.51 反推約 5,330 萬股，2026 年指引 5,400 萬股，年增約 1.4%，低於 1.5%；股數為反推，誤差約 0.3 個百分點。","grade":"過"}]},"valuation":{"basis":"調整後 EPS 乘本益比，分母用 FY2026 指引中值 6.00，不用已過期的共識 5.38。","tier":"大型基建承包商","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋，只有利潤率，無法做同層級倍數對照；終端倍數改以本公司現值 15.0–16.7 倍為參考。"},"fwd_pe":16.71,"peg":1.3,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"指引中值約 15 倍，前瞻本益比除以 FY1 到 FY2 共識增幅 12.8% 得 PEG 約 1.3，落在合理區；第三年共識缺失，所以只能用單年成長。基礎情境年化約 6.4%，低於 8%。五年分位事實表未涵蓋，只有 1–4 個年度端點。合併判為中性。","upside_short_pct":7.5,"upside_mid_pct":21.5},"trap_analysis":{"verdict":"🟡","label":"峰值利潤待驗證"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2022–2024 年連三年營業虧損；九大案多在早期，Q3 指引上修部分來自先前辨識風險的化解；10-K 也提醒固定價格合約的成本可能無法完全回收。","assumption":"合約條款改善足以防止前份所說的 2018–2023 年問題重演。","consequence":"FY2031 EPS 約 4.2 美元、10 倍，股價約 42 美元，五年約 −53%。","ruling":"採納，與唯一致命事件同一條路徑，空頭機率給 30%。","watch":"單案認列損失、Civil 利潤率、TTM 毛利率。","evidence_refs":["reg_tariff_export#0"],"fact_refs":["f_peer_tpc_gross_margin_pct","f_peer_tpc_operating_margin_pct"]},{"view":"論點失敗","evidence":"2026-08-05 法說，Steven Fisher 問區域業者是否回歸，CEO 只重申競爭有限；Michael Dudas 問營運資金與保證額度，CFO 未給數字。10-K 警告設計建造趨勢可能增加競爭。","assumption":"投標者少的狀態至少延續到 2029 年以後。","consequence":"新案標價下滑時，已簽案仍賺錢，但 2029 年後的 EPS 接不上，基礎情境失效。","ruling":"部分採納，目前沒有對手回流的數據，先列為中度威脅，不降方向。","watch":"法說得標清單、Civil 區間是否上修、公司對競爭家數的描述是否改變。","evidence_refs":["competitive_share_entrants#1"],"fact_refs":["f_kpi6_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"帳上現金約 11 億美元，可用於一般公司用途只有 5.04 億；2026 年非控制權益預估 6,500–7,500 萬美元；FY2025 FCF 約為淨利 7 倍；CEO Gary Smalley 2026-08-05 說保留現金是為取得保證人核准。","assumption":"淨現金 7.07 億美元全屬股東，且未來現金流等於獲利。","consequence":"巨型案到後期進度款回吐，現金流低於獲利；單獨投標需保留更多現金，股東拿到的比損益表少。","ruling":"採納。估值用獲利不用 FCF，企業價值另看可動用現金口徑約 46 億美元，高於表列 41 億。單獨投標減少合資分潤可部分抵銷。","watch":"可動用現金、TTM 營運現金流對調整後淨利、實際回購金額。","fact_refs":["f_net_debt_m","f_ev_m","f_kpi3_free_cash_flow_derived"]},{"view":"價格已反映太多","evidence":"股價是 250 週線 31.14 美元的 2.9 倍；P/S、EV/S 都在 4 個年度端點最高；較前份 72.76 美元上漲 23.5%，大於同期指引中值上修 17.6%。","assumption":"約 15 倍指引已經算便宜。","consequence":"若市場改用常態利潤率看 EPS，不需要壞消息，股價也可能回到 70 多美元。","ruling":"部分採納。倍數由 14.3 倍升到 15.0 倍，並不離譜，但盈餘處於高區，基礎情境年化只有約 6%，所以不追。","watch":"股價對 52 週線乖離、更新後的共識 EPS。","fact_refs":["f_price_at_dd","f_ma_w250","f_ps_percentile","f_ev_s_percentile"]}],"max_dd":{"lo":-65,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 72.76 → 本次 89.89（+23.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=72.76","side_b":"本次 price_at_dd=89.89","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 72.76 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 72.76 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 72.76 美元：Bull 價 212.5、Bear 價 42，五年期望值 +64.8%，基準年化 10.6%，不對稱比 3.79","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.79。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 72.76 美元：五年期望值 +64.8%，基準年化 10.6%，不對稱比 3.79","side_b":"本次情境、股價 89.89 美元：五年期望值 +33.4%，基準年化 6.0%，不對稱比 2.13","ruling":"再換股價、情境不動：起點價上漲 23.5%，五年期望值少 31.4 個百分點，基準年化少 4.6 個百分點，不對稱比由 3.79 降到 2.13。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"Civil 利潤率是結構還是週期","cause":"新證據","prior_field":null,"side_a":"2026-11-04 法說，CEO Gary Smalley：合約條款改善、對手減少，Civil 區間短中期有上行壓力。","side_b":"2022–2024 年營業利益率 −5.4%、−2.95%、−2.4%；10-K 警告設計建造趨勢可能增加競爭、壓低部分案件毛利。","ruling":"可調和，差別在時間。已簽案 160 億美元的利潤率可信到 2028 年；2029 年以後要看尚未簽約的案子，現在沒有數據，所以基礎情境讓 EPS 放緩，不把 14% 當常態。","evidence_level":"中：利潤率是實際數字，原因來自管理層說法。","settle_metric":"Civil 季度利益率；新案標價利潤未揭露，以區間是否上修代替。","if_then":["若 2027 年財報正式上修 Civil 區間且連兩季 ≥14%，上調基礎情境並分批建立首倉。","反向：若 Civil 連兩季低於 12%，減碼一半並停止加碼。"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"帳上淨現金有多少屬於股東","cause":"新證據","prior_field":null,"side_a":"2026-11-04 法說，CFO Ryan Soroka：現金超過總債務 7.07 億美元，財務彈性大。","side_b":"同場揭露可用於一般公司用途的現金 5.04 億美元，扣總債務 4.04 億後僅約 1 億；其餘的限制內容公司未拆解。","ruling":"採可動用口徑。企業價值看約 46 億美元而非 41 億，EV 對 FY1 營收 0.71 倍而非 0.63 倍，不因淨現金給溢價。","evidence_level":"高：兩個數字都是公司揭露。","settle_metric":"可動用現金與總債務。","if_then":["若可動用現金連兩季高於 7 億美元且回購啟動，加回淨現金價值並上調基礎情境目標價。","反向：若可動用現金跌破 3 億美元，停止加碼。"],"evidence_refs":[]},{"axis":"管理層前後說法","cause":"新證據","prior_field":null,"side_a":"2026-08-05 法說：CFO Ryan Soroka 說今年營運現金流不會破紀錄；CEO Gary Smalley 說九大案 9 勝 11、Civil 舊區間 8–12%，預建案第三、四季及 2027 年轉入訂單。","side_b":"2026-11-04 法說：前九月營運現金流 6.65 億美元，Q4 超過約 0.85 億就破去年 7.5 億；CEO 改說約 9 勝 12、舊區間 8–10%，約 7.5 億美元預建案時程講到 12–18 個月。","ruling":"現金流與指引屬保守後超標，可信度加分；得標率與舊區間的出入小，不影響結論，但 CEO 口頭數字不宜當精確引用；預建案時程略為後延，記錄不扣分。","evidence_level":"高：兩場法說原話。","settle_metric":"2026 全年營運現金流；預建案實際轉入訂單時點。","if_then":["若全年營運現金流超過 7.5 億美元，維持管理層指引偏保守的判斷，情境不變。","反向：若 7.5 億美元預建案到 2028 年第一季仍未轉入訂單，停止加碼。"],"evidence_refs":[]},{"axis":"共識修正 0% 與指引上修","cause":"新證據","prior_field":null,"side_a":"Koyfin 11-07 快照：FY2026 EPS 5.38、FY2027 EPS 6.07，近三個月修正 0%。","side_b":"11-04 指引中值 6.00，比 5.38 高 11.5%；管理層另說 2027 年盈餘雙位數成長。","ruling":"0% 應視為資料延遲，不是共識停滯的證據，但延遲本身是推論。FY2027 的 6.07 只比 2026 指引高 1.2%，與管理層說法不符，情境路徑不用它當錨。","evidence_level":"中：數字是原始資料，延遲原因未經查證。","settle_metric":"下一次共識快照。","if_then":["若更新後 FY2027 共識仍低於 6.60 美元，停止加碼。","若更新後 FY2027 共識超過 7.40 美元而股價先漲，仍不追。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":"新證據","prior_field":null,"side_a":"約 13 倍 FY2027 基礎 EPS，連七季亮眼，指引今年上修兩次，共識尚未更新；2027 年營收超過四分之三已在訂單內。","side_b":"EPS 處於高區，施工峰值就在 2028 年下半，五年基礎報酬年化約 6%，下檔約 −53%；等回檔的代價低於追高後遇到超支的代價。","ruling":"不追。唯一約束是價格相對尚未驗證的利潤率持續期，論點本身沒有破。","evidence_level":"中：短期數字扎實，2029 年後沒有數據。","settle_metric":"股價與 Civil 利潤率；2027-02 指引。","if_then":["若 2027-02 財報的 FY2027 EPS 指引下緣 ≥7.40 美元且 Civil 區間上修，取消 78 美元限制，重跑研究後分批建立首倉。","若股價續漲而利潤率未再獲驗證，不追。","若股價下跌但 Civil 仍 ≥12%，分批反買。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭軸：10-K 與 2026-11-04 法說都說大型固定價格案投標者減少；但 10-K 同時警告設計建造趨勢可能增加競爭，區域業者回流的提問也未獲正面回答。","side_b":"結構軸：機會管線逾 2,000 億美元，資金多來自州與地方。其他軸：關稅與通膨靠買斷與分包轉嫁，尚未見吸收失敗。","ruling":"結構性轉好中：需求與投標家數同向，競爭軸有反向提問但沒有數據。ABC 指資料中心榮景掩蓋整體疲弱，TPC 資料中心訂單僅 0.2%，不受益也較少受其回落影響。","evidence_level":"中：多為公司與 10-K 自述。","settle_metric":"得標率、Civil 區間、TTM 毛利率。","if_then":["若公司揭露大型案競爭家數增加且得標率明顯下滑，改判雙向拉鋸並停止加碼。"],"evidence_refs":["competitive_share_entrants#1","reg_tariff_export#0"]},{"axis":"前份空白欄位首次判定","cause":"方法變動","prior_field":["archetype","cycle_position","moat_trend","runway_post_y5","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位未填，沒有可比較的舊值。","side_b":"本次首次判定：循環型、中循環、護城河向上、五年後能見度中等，空頭機率 30%，最大回撤 −40% 到 −65%。","ruling":"這些差異來自框架補欄，不代表基本面轉向。","evidence_level":"高：前份確實為空值。","settle_metric":"下一份研究逐欄比較。","if_then":[],"evidence_refs":[]},{"axis":"估值結論由偏便宜轉中性","cause":"方法變動","prior_field":["val"],"side_a":"前份：72.76 美元，當時指引中值 5.10，約 14.3 倍，結論偏便宜。","side_b":"本次：89.89 美元，指引中值 6.00，約 15.0 倍，結論中性。","ruling":"倍數只升 0.7 倍，主因不是價格。本次把盈餘分母列為爭點，並加入 2029–2031 年放緩路徑，便宜的說法不再成立。","evidence_level":"中：倍數是實算，分母爭議是判斷。","settle_metric":"Civil 利潤率與更新後共識。","if_then":["若股價回到 78 美元以下且 Civil ≥12%，重跑研究後分批建立首倉。"],"evidence_refs":[]},{"axis":"綜合等級與陷阱評估未變，理由更新","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：綜合等級 B，獲利陷阱評為中度，風險集中在舊爭議與持股賣壓。","side_b":"本次：等級與中度評估不變；舊爭議壓力下降（未請款成本餘額 7.67 億美元，為 2014 年底以來最低），風險轉為高區利潤率能否持續。","ruling":"等級不動，但主要風險由過去的爛帳轉為未來的峰值。創辦人持股資料本包未涵蓋，維持資料缺口。","evidence_level":"中：財務數字扎實，持股資料缺失。","settle_metric":"未請款成本餘額、Civil 利潤率。","if_then":["若未請款成本餘額降至 6 億美元以下且無結算損失，陷阱評估可下修。","反向：若單季舊爭議結算損失 ≥5,000 萬美元，減碼一半。"],"evidence_refs":[]},{"axis":"Single Thing 由未設定改為巨型案超支","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點，原文為空。","side_b":"九大巨型案任一出現重大成本超支，單案累計認列損失達 2 億美元以上。","ruling":"採用此事件。Civil 利潤率是模型最大敏感度，每 100 個基點約影響年 EPS 0.48 美元；前份 R2 的同類風險因此升為唯一致命點。","evidence_level":"中：敏感度為推算。","settle_metric":"10-Q 專案調整揭露。","if_then":["若事件發生，清倉。"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設退出指標；最接近的是 R2：任一 cost overrun > $200M 公告 且 Adj EBITDA margin 連 2 季崩 50bp+ → 反轉，重評持倉。","side_b":"單案累計損失 ≥2 億美元清倉；≥1 億美元或 Civil 連兩季低於 12% 減碼一半。","ruling":"2 億美元門檻沿用，但取消兩條件同時成立的要求，因為超支通常分季認列，等兩季會坐滿損失。Adj EBITDA 本包未提供，改用公司每季揭露的 Civil 利潤率。","evidence_level":"中：門檻為判斷。","settle_metric":"單案損失與 Civil 季度利益率。","if_then":["觸發 1 億美元或 Civil 條件時減碼一半；觸發 2 億美元時清倉。"],"evidence_refs":[]},{"axis":"重啟進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設定，原文為空。","side_b":"股價≤78美元（約52週線、13倍FY2026指引中值）且最新一季 Civil 利潤率≥12%，重跑研究後才建首倉。","ruling":"以價格為主要條件，因為目前的約束是價格相對尚未驗證的利潤率持續期；Civil 條件用來確認回檔不是論點破裂。","evidence_level":"中：價位由指引與 52 週線推得。","settle_metric":"股價與最新季 Civil 利潤率。","if_then":["條件成立時重跑研究並分批建立首倉；股價跌破但 Civil 低於 12%，不買。"],"evidence_refs":[]},{"axis":"假設與風險門檻調整","cause":"方法變動","prior_field":null,"side_a":"前份 H1：FY26 全年 Adj EBITDA margin ≥ 8.0%；H3 與 R1：Tutor 18 個月退出，單次 > 1M 股賣出且股價急跌 15%。","side_b":"本次 H1 改看 Civil 與 Specialty 分部利潤率；持股賣壓保留為風險，指標與門檻不變，標資料缺口。","ruling":"Adj EBITDA 本包未提供，公司每季揭露分部利潤率，較可追蹤。持股現況本包完全未涵蓋，不得視為風險解除，保留 Form 4 監測。前份 H2 的 190 億與 220 億美元門檻沿用。","evidence_level":"中：持股部分為資料缺口。","settle_metric":"Form 4 申報；分部利潤率。","if_then":["若單次賣出超過 100 萬股且股價急跌 15%，基本面未破時分批反買。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Civil 利潤率守住已簽案標價水準","type":"假設驗證","maps_to":"H1","metric":"Civil 部門季度營業利益率","threshold":"≥12%（最新季 14%）","action":"達標續抱；未達標轉入減碼條件","source_freq":"公司季報，每季","date":"2027-02 起每季"},{"n":2,"text":"訂單持續補上","type":"假設驗證","maps_to":"H2","metric":"在手訂單與滾動四季訂單出貨比","threshold":"訂單 ≥190 億美元且出貨比 ≥1.0","action":"達標續抱；未達標停止加碼","source_freq":"公司季報，每季","date":"2027-02 起每季"},{"n":3,"text":"現金流以營運為主","type":"假設驗證","maps_to":"H3","metric":"TTM 營運現金流對調整後淨利；可動用現金","threshold":"營運現金流 ≥調整後淨利；可動用現金 ≥5 億美元","action":"未達標停止加碼","source_freq":"公司季報，每季","date":"2027-02 起每季"},{"n":4,"text":"九大巨型案任一重大超支","type":"Single Thing","maps_to":"Single Thing","metric":"單案累計認列損失","threshold":"≥2 億美元","action":"清倉","source_freq":"10-Q 專案調整揭露，每季","date":"每季財報日","evidence_refs":["reg_tariff_export#0"]},{"n":5,"text":"對手回流或設計建造壓低標價","type":"風險","maps_to":"R2","metric":"Civil 區間、得標清單、競爭家數描述","threshold":"公司下修 Civil 區間，或連續四季未得 10 億美元以上新案","action":"停止加碼","source_freq":"法說會，每季","date":"每季財報日","evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"價格回到可承接區","type":"估值rearm","maps_to":"H1","metric":"股價與最新季 Civil 利潤率","threshold":"股價 ≤78 美元且 Civil ≥12%","action":"重跑研究後分批建立首倉","source_freq":"每日股價、每季財報","date":null},{"n":7,"text":"利潤率結構改善獲得驗證","type":"加碼","maps_to":"H1","metric":"Civil 區間與 FY2027 指引","threshold":"Civil 區間上修且 FY2027 EPS 指引下緣 ≥7.40 美元","action":"重跑研究後分批加碼","source_freq":"公司財報","date":"2027-02"},{"n":8,"text":"利潤率或單案損失轉壞","type":"減碼","maps_to":"R1","metric":"Civil 季度利益率；單案累計損失；TTM 毛利率","threshold":"Civil 連兩季 <12%，或單案損失 ≥1 億美元，或 TTM 毛利率 <10%","action":"減碼一半","source_freq":"公司季報，每季","date":"每季財報日","evidence_refs":["reg_tariff_export#0"]},{"n":9,"text":"客戶集中轉為實際損失","type":"風險","maps_to":"R3","metric":"最大客戶營收占比與相關專案取消","threshold":"單一客戶占比 >25%，或前兩大客戶的專案遭取消、延付","action":"減碼一半","source_freq":"10-K，每年；重大事件即時","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":10,"text":"Q4 財報與 2027 指引後複審","type":"複審日期","maps_to":"H1","metric":"2027 指引、Civil 區間、更新後共識","threshold":"財報發布","action":"重跑情境樹並更新等待價位","source_freq":"公司財報","date":"2027-02"}],"kill_metrics":[{"metric":"Civil 部門季度營業利益率","bear_threshold":"連續兩季低於 12%：減碼一半","window":"連續 2 季","source":"公司季報與法說會","last_status":"ok"},{"metric":"九大巨型案單案累計認列損失","bear_threshold":"≥1 億美元減碼一半；≥2 億美元清倉","window":"任一季","source":"10-Q 專案調整揭露","last_status":"ok"},{"metric":"在手訂單與滾動四季訂單出貨比","bear_threshold":"訂單低於 190 億美元且出貨比低於 1.0","window":"滾動 4 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"TTM 營運現金流對調整後淨利","bear_threshold":"連續四季低於 1.0 倍","window":"連續 4 季","source":"公司季報","last_status":"ok"},{"metric":"創辦人 Form 4 賣出量與股價反應","bear_threshold":"單次超過 100 萬股且股價急跌 15%","window":"單一事件","source":"SEC Form 4，本包未涵蓋，資料缺口","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='↑', week26=8.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價≤78美元（約52週線、13倍FY2026指引中值）且最新一季 Civil 利潤率≥12%，重跑研究後才建首倉","exec_line":"現價不追。跌到 78 美元以下且論點未破時分批建首倉；股價續漲但 Civil 區間未上修，繼續不追；股價下跌而 Civil 仍 ≥12%，分批反買，不當停損。"},"reasoning":{"industry":"Q3 營收 17.2 億美元，年增 22%；營業利益 1.25 億美元，利益率 7.3%；TTM 毛利率 11.75%。分部方面，Civil 營收 8.94 億、利益率 14%，Building 5.41 億、利益率 5%，Specialty 2.86 億、利益率 3.5%。三部門營業利益合計約 1.62 億，Civil 占 77%，營收只占 52%。收錢方式是按工程進度認列與請款，九個巨型案合計 160 億美元，多數仍在早期，CEO 說 2027 年營收超過四分之三已在訂單內。產業位置判為擴張期，依據是機會管線逾 2,000 億美元、約為兩年前三倍，大型固定價格案投標者變少，與股價無關。供需持久性：週期性，能見度到 2028 年，供給端可逆，退場的對手可以回來。單點依賴不在客戶（前兩大合計 25.5%，未達警戒），而在專案類型：九大案任一出現超支，影響大於任何一個客戶流失。","moat":"機制是大型固定價格土木案的承接能力，包含保證額度、工程管理經驗與資產負債表，再加上願意投標的對手變少。方向證據是 Civil 利潤率區間上移到 12–15%、九大案得標率大幅改善，以及淨現金讓公司可單獨投標。TPC 的 TTM 營益率 5.64% 是五家最低（GVA 7.11%、PWR 6.81%、FIX 16.66%、STRL 18.62%），優勢目前反映在新案標價，還沒反映在全公司利潤率。同業 ROIC 事實表未涵蓋，改用得標率與利潤率區間當可比軸。執行與定價都給 6 分：連七季亮眼，但前面有連三年虧損。","growth":"成長以量為主、利潤率為輔，沒有併購：Q3 營收年增 22%，調整後 EPS 年增 59%。訂單 203.5 億美元約為 FY1 共識營收的 3.1 倍。三年共識 EPS CAGR 無法計算，第三年共識事實表未涵蓋；FY1 到 FY2 共識增幅 12.8%，但快照未反映 11-04 上修。基礎情境以 FY2026 指引中值 6.00 為起點，FY2031 EPS 8.60，年化 7.5%，主要靠放量與利潤率，不靠倍數擴張。內生天花板因再投資率接近零而無法計算，缺口無法歸因，長期信心上限為中。資料中心僅占訂單 0.2%，CEO 明說不是重點，因此不算第二曲線。","governance":"FY2025 FCF 5.67 億美元、淨利 0.80 億，FCF 為淨利約 7 倍，這不是獲利品質高，而是舊爭議收款與巨型案進度款造成，後期可能回吐。Q3 SBC 占營收 1.1%，2027 年將再下降。7 月以 6.625% 票據取代 11.875% 票據，每年省息 2,100 萬美元。季股利由 0.06 升至 0.09 美元，回購授權餘額 1.7 億美元。2026-08-05 法說 CFO Ryan Soroka 把併購排在現金用途最後，CEO Gary Smalley 說保留現金是為取得保證人核准。近三年現金去向四分、債務到期結構事實表未涵蓋。","valuation":"現價 89.89 美元。前瞻本益比 16.71 倍用的是 5.38 的舊共識，數字仍落在 Q2 指引區間內，未反映 11-04 上修；用新指引中值 6.00 算是 15.0 倍。Trailing 34.18 倍被 Q3 債務清償損失 5,100 萬與退休金結算 3,400 萬拉高，不適合使用。同業前瞻倍數事實表未涵蓋，相對估值無法下結論。基礎情境 FY2031 EPS 8.60 乘 14 倍約 120 美元，年化約 6.4%，拆解為 EPS 複利約 +7.5%、倍數約 −1.3%、股息約 +0.4%，報酬不靠倍數擴張。機率加權五年約 +33%，上下檔比約 2.1 倍。賣方目標價都早於 Q3 財報，8 月共識 86.50 美元，各站 76–113.25 美元，高低比約 1.5 倍；現價高於 8 月共識，支持不追，但資料已舊，只算弱證據。","premortem":"偏多的錯誤路徑是巨型案後期出現超支，重演 2022–2024 年營業利益率 −5.4%、−2.95%、−2.4%。偏空的錯誤路徑是 Civil 區間真的再上移、訂單持續補上，股價不回檔，我們錯過這段。還有兩個未解資訊：2026-08-05 法說對區域業者回歸與保證額度的問題未獲正面回答。歷史最大回撤、未結爭議金額明細事實表未涵蓋；未請款成本餘額 7.67 億美元約為市值 16%，是舊爭議結算的主要曝險。"},"plain":{"six":{"how_it_makes_money":"賺公共工程業主的錢，利潤卡在 Civil 部門的大型固定價格案：Q3 部門營業利益 77% 來自 Civil，能否守住 12–15% 利潤率決定全公司獲利。","moat":"護城河方向向上，但等級只到中下：投標對手變少加上合約條款改善是近三年的順風，尚未經過完整循環考驗。","growth":"五年後能見度中等：現有訂單的施工峰值約在 2028 年下半，2029 年起要靠新單接力，沒有第二條成長曲線。","capital":"資本配置紀錄還太短：再融資明顯省息、淨現金大增，但回購價格與現金去向事實表未涵蓋，現金也未必都能分給股東。","valuation":"現價要求高利潤率延續到 2031 年且 2029 年後訂單補得上；我相信前半段到 2028 年，後半段還沒有數據，價格合理但不便宜。","how_wrong":"最可能看錯兩處：把峰值利潤當常態，或反過來低估合約條款帶來的結構改善。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 78 美元以下（約 52 週線、FY2026 指引中值 13 倍）且 Civil 利潤率仍 ≥12%；若 2027-02 財報上修 Civil 區間，重算等待價位。","trap":"🟡","val":"🟡","moat":"C","moat_trend":"↑","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":89.89,"week26_return_pct":8.69,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母有三項爭議：調整後 EPS 排除股權報酬（Q3 為 1,930 萬美元）；共識 5.38 未反映 11-04 上修；指引 6.00 建立在高區利潤率上，且上修含先前辨識風險的化解。因此不能以低本益比主張便宜。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"大部分負債型股權獎酬年底歸屬，2027 年股權報酬費用將大幅下降","impact":"低","watch":"GAAP 與調整後 EPS 差距是否縮小"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 2027 年指引，可能正式上修 Civil 利潤率區間","impact":"高","watch":"FY2027 調整後 EPS 指引、Civil 區間、全年營運現金流是否破 7.5 億美元"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"Black Construction 印太三案約 10 億美元決標，最大案待環評完成，時點為估計","impact":"中","watch":"決標時點與是否得標"},{"date":null,"date_precision":null,"type":"macro","event":"新聯邦運輸法案進度，管理層 2027 年展望未計入","impact":"中","watch":"法案是否通過與撥款規模，時程事實表未涵蓋"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,758B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與對手比較</h2>
<p class="lead">護城河向上但等級只有 C，優勢尚未反映在全公司利潤率。</p>
<ul class="pts">
<li>護城河的機制是大型固定價格土木案的承接能力，包含保證額度、複雜工程管理經驗與資產負債表，再加上願意投標的對手變少。這不是技術或品牌優勢，而是一種有資格參賽的門票。對手退場期間門票值錢，對手回來後就沒那麼值錢。</li>
<li>方向向上有三項證據。Civil 利潤率區間上移到 12–15%，九大巨型案得標約 9 勝 12，淨現金讓公司可以單獨投標而不必拉夥伴分潤。2026-11-04 法說會 CEO Gary Smalley 說新案以更高利潤率投標。這些主要來自公司自述，反向訊號列在後面。</li>
<li>執行與定價各給 6 分，綜合 6.0，等級 C。理由是連七季表現亮眼，但前面有連三年虧損。TTM 營業利益率 5.64% 是五家比較對象中最低，GVA 為 7.11%，PWR 為 6.81%，FIX 為 16.66%，STRL 為 18.62%。優勢目前反映在新案標價，還沒有反映在全公司利潤率。</li>
<li>對手比較要小心解讀。TTM 毛利率 TPC 為 11.75%，GVA 為 16.08%，PWR 為 15.76%。FCF 利潤率 TPC 為 10.75%，高於 GVA 的 8.36% 與 PWR 的 8.46%，但這含訂單早期收款效果，不代表賺錢能力較強。STRL 的營業利益率是 TPC 的三倍多，FIX 的 FCF 利潤率達 19.46%，兩者業務差異大，不作同層級估值錨。</li>
<li>威脅有兩項，都是中度。第一，漸進式設計建造若成為主流，投標門檻下降，部分案件毛利被壓低，我們給 30% 的發生機率，目前沒有實際案例數字。第二，高利潤會吸引區域業者回流，機率 35%。2026-08-05 法說會分析師 Steven Fisher 問到這點，CEO 沒有正面回答，11-04 又說不預期再有九大案那樣的得標率。</li>
<li>投資報酬持續期的四個檢查點結論不一。需求基礎是綠燈，因為付款者是公共機關，政府客戶占訂單 86%。決策層級、價值鏈分配、社會容忍度三項都是黃燈。每案重新競標，開工後才有換手成本，合資夥伴分走利潤，2026 年非控制權益預估 6,500–7,500 萬美元，14% 的利潤率也容易受公眾檢視。</li>
<li>公式在本公司失靈。成長主要由客戶進度款支應，資本支出中值 1.30 億美元減折舊攤銷 0.45 億美元為 0.85 億美元，其中 0.75–0.85 億由業主出資，扣除後再投資率接近零。算出來的內生成長沒有意義，實際天花板是保證額度、工程人力與得標率。同業投入資本報酬率的資料不足，無法比較。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```