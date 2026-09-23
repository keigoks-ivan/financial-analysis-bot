你是 stock-analyst v20 的**散文層（prose）agent**，標的 AMD（2026-09-23）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20260923/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：AMD　日期：2026-09-23　archetype：None　前份裁決：2026-08-05　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2015B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（1267B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1000B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1636B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1036B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（815B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1077B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2080B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4175B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3041B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2015           3490-4985      5 條（2–6 內）  
s3                  8000        1267           4713-6733      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3672          7930-11328      5 條（2–6 內）  
s6                 11000         815          7130-10185      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1077           1696-2423      3 條（2–6 內）  
s10                 5000        2080           2044-2920      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3041           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=6015B；至少需散文≈38.98KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−73%
−72
−72%
−68%
−62%
−55%
−46%
−45
−45%
−21%
−1.2
0
0.1%
0.75
0.93
1
1.04
1.09
1.15
1.37
1.4
1.5
1.6
1.66
2
02
2%
2.1
2.21
2.5
2.85%
3%
3
03
3.3
04
4
4.36%
4.7
5%
5
05
6
06
7%
07
7
7.58
7.79
8
08
8%
8.8%
09
9
9.77
10
10%
10.6%
11
11%
11.4
12%
12
12.5
13%
13
13.2
13.5%
13.78
14.0
14
15
15.0
15%
15.57
15.58
15.7%
16%
16.6
17
17%
17.5
18%
19
19%
20%
20
20.02
20.3%
21%
21
21.0
22
22%
22.27
22.7%
23%
23
23.8%
24%
24
24.1%
24.4
24.7
25%
25
26
27%
27
28
28%
29
30%
30
30.3%
30.5
31%
31
32
32%
32.5%
33
33%
34
34.1%
34.5
35
35%
36.5
37%
38%
38.3
40
40%
40.1
42
42%
43
45%
46
46%
46.2%
48.6%
49
49%
50
50%
52
52%
53.2%
54%
55
55%
56%
58%
60%
65%
65.2%
67
67%
70%
70
71%
74.7%
80%
82%
82
82.29
84%
85
90
92
100
100%
104
107%
110
111.2
115.36
130
131
150%
156
165.31
170
180
200
203.69
204%
213
216
235.31
250
280
300
323
339.87
350
351
470.79
490
565.13
616.51
623.77
640
760
862.5
2025
2026
2027
2028
2030
3661
20260923
1,200
1,260
1,300
2,200
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
{"meta":{"ticker":"AMD","date":"2026-09-23","schema":"v15.2","contract":"v19","company_name":"Advanced Micro Devices, Inc."},"oneliner":"伺服器 CPU 與 AI 加速器雙線放量是真的，但 623.77 美元已大致定價管理層 2027–28 年計畫；基本情境五年年化約 6–7%，現價不追，回到 490 美元以下或 Helios 放量明顯超標再加。","thesis":{"H":[{"id":"H1","text":"Helios／MI450 讓 GW 級合約在 2027 年變成實際營收，資料中心部門營收翻倍以上","2y":"FY2027 資料中心部門營收 ≥ FY2026 的 2 倍；2026Q4 起每季季增 ≥10%","5y":"AI 加速器營收份額由 5–8% 升到 12% 以上，錨定三家之外至少再有兩家 GW 級客戶","10y":null,"threshold":"2026Q4、2027Q1 資料中心部門季增各 ≥10%；FY2027 資料中心營收 ≥ FY2026 的 2 倍","source":"公司季報；2026-08-04 法說（Lisa Su、Jean Hu）；第三方 AI 加速器份額估計","drift_rule":"資料中心部門營收連 2 季低於指引中值 5% 以上為削弱；連 3 季低 10% 以上為反轉"},{"id":"H2","text":"EPYC 份額續升：Venice 世代把伺服器 CPU 營收份額推過 50%","2y":"2027 年伺服器 CPU 營收年增 ≥70%；營收份額守住 46% 以上","5y":"伺服器 CPU 營收份額超過 50%（2025-11-11 分析師日目標）","10y":null,"threshold":"Mercury Research 伺服器營收份額每季 ≥45%；2026 下半年伺服器營收年增 >80%","source":"Mercury Research 季度份額；公司法說（2026-05-05、2026-08-04）","drift_rule":"份額連 2 季合計下滑 3 個百分點以上為削弱；跌破 42% 為反轉"},{"id":"H3","text":"營業槓桿兌現：營收成長快於費用，毛利率守住 55% 以上，non-GAAP 營業利益率往 35% 走","2y":"FY2027 non-GAAP 營業利益率 ≥32%；每季毛利率 ≥55%","5y":"FY2029 起 non-GAAP 營業利益率 ≥35%（分析師日長期模型），EPS 顯著超過 20 美元","10y":null,"threshold":"起點：2026Q2 non-GAAP 營業利益率 27%、毛利率 56%；營業費用年增持續低於營收年增","source":"公司季報；2025-11-11 分析師日長期模型；2026-08-04 法說（Jean Hu）","drift_rule":"毛利率連 2 季 <55%，或營業費用年增連 2 季高於營收年增，為削弱；連 3 季為反轉"}],"R":[{"id":"R1","text":"Helios 放量初期良率與 HBM 成本壓毛利率：Helios 的 HBM 比對手多約 50%，記憶體短缺延續到 2027 年以後；管理層至今不給 2027 毛利率","h_ref":"H3","clock":"⚡","threshold":"單季 non-GAAP 毛利率 <55%，或 FY2027 首次毛利率指引 <55%，或資料中心占比升 5 個百分點而毛利率降 50 基點以上","evidence_refs":["supply_demand_durability#0"]},{"id":"R2","text":"錨定客戶信用與集中：GW 級合約多年期、按里程碑，大部分營收未簽定出貨；OpenAI 首季虧 213 億美元、兩年融資缺口約 1,300 億美元；S&P 因 OpenAI 曝險把 Oracle 降到 BBB-；Meta 拿到 1.6 億股績效權證","h_ref":"H1","clock":"🔥","threshold":"任一錨定客戶或早期 Helios 客戶公開延後、縮減採購或被降到投機等級；或 AMD 自身股權投資支撐的營收占 2027 資料中心 AI 逾 15%（本包未收錄該投資，資料缺口）","evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#4"]},{"id":"R3","text":"客戶自研晶片吃掉可觸及市場：Meta MTIA、微軟 Maia 200 已部署，Broadcom 替 Google、Meta、微軟、OpenAI、Anthropic 做自研晶片；輝達仍拿 70–80% 加速器營收","h_ref":"H1","clock":"🐢","threshold":"第三方估計 AMD AI 加速器份額到 2027 年底仍低於 10%，或客戶自研晶片合計份額升過 25%","evidence_refs":["competitive_share_entrants#5","customer_second_source#0","customer_second_source#1","customer_second_source#2","substitute_technology#0","end_markets#5"]},{"id":"R4","text":"中國與台灣：中國約占營收兩成，輸中 AI 晶片須付 25% 關稅並受量能上限；先進製程集中在台灣台積電；2025 年曾因禁令認列 8 億美元費用、損失約 15 億美元營收","h_ref":"H1","clock":"🔥","threshold":"再有針對 AMD 產品的出口限制或關稅擴大，導致單季認列存貨相關費用逾 5 億美元或下修財測","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R5","text":"PC 與遊戲轉弱：記憶體與零組件漲價，遊戲 Q2 年減 31%、下半年較上半年再少 20% 以上，管理層預期下半年 PC 市場走軟","h_ref":"H3","clock":"⚡","threshold":"Client 營收由年增轉為年減連 2 季","evidence_refs":["end_markets#11"]},{"id":"R6","text":"產業級 AI 資本支出報酬重定價：Moody's 已把前所未見的 AI 支出列為超大規模業者整體信用風險；AMD 身為第二供應商，對資本支出放緩的彈性大於輝達","h_ref":"H3","clock":"🐢","threshold":"任兩家超大規模業者 2027 資本支出指引年增跌破 20%，或半導體板塊前瞻倍數帶下移一個標準差（兩項本包未涵蓋，資料缺口）","evidence_refs":["customer_concentration_credit#3"]}],"single_thing":{"description":"OpenAI、Meta、Anthropic 三個 GW 級錨定客戶中，任一家公開延後或縮減 MI450／Helios 部署","why_fatal":"2027 年資料中心部門遠超過翻倍主要靠這三家放量；每 GW 營收是雙位數十億美元（Lisa Su 2026-08-04），少一家等於 2027 年少掉以百億美元計的營收，FY2027 EPS 可能少 15–25%；現價倍數建立在這條路徑上，盈餘和倍數會同時往下","if_happens":"減碼一半並停止加碼；兩家以上清倉","how_monitor":"公司法說的部署進度、客戶公告、OpenAI 融資消息、評等機構對 OpenAI 相關業者的動作","probability":"12–24 個月約 20%：OpenAI 融資缺口是主要來源；Meta 信用仍強（Moody's 2026-07-24），Anthropic 與微軟是新增分散，壓低機率"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":40.1,"peg_fy2":0.93,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":7.58,"FY2027E":15.57,"FY2028E":22.27},"fy_end_month":12,"eps_basis":"推定為 non-GAAP 稀釋 EPS 共識（與 Q1 1.37、Q2 1.66 的 non-GAAP 季 EPS 同量級），Koyfin 2026-09-19 快照；FY2025 實際值事實表未涵蓋，基期留空；FY2026E 到 FY2028E 兩年年化約 71%；共識家數事實表未涵蓋（S&P 評等彙整為 55 位）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMD_20260923/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"份額擴張加營業槓桿；需求綁在 AI 資本支出循環上"},"industry":{"clock_phase":"II","sd_verdict_source":"需求端屬結構性（推論與代理式工作負載），但眼前的吃緊有一部分是未預期需求加記憶體短缺；Lisa Su 說 2027 年伺服器供給會比 2026 好，所以交期與定價優勢屬週期性，供給可逆性高。","bargaining":{"up":"上游議價強：台積電掌握約九成先進製程，HBM 短缺預期延續到 2027 年以後；AMD 與客戶分攤成本上漲（Lisa Su 2026-05-05）。","down":"下游集中：三家 GW 級客戶，Meta 另取得 1.6 億股績效權證，議價偏向買方。","geo":"中國約占營收兩成（Lisa Su 2026-05）；輸中 AI 晶片須付 25% 關稅並受量能上限；先進製程集中在台灣。"},"profit_pool_dir":"AI 加速器利潤池仍集中在輝達（營業利益率 65% 對 AMD 16%）；伺服器 CPU 利潤池正從 Intel 流向 AMD。","tam_table":[{"item":"AI 加速器市場（管理層，2030 年）","value":"約 1.4 兆美元，年增 45% 以上（2026-08-04 法說）；2025-11-11 時資料中心整體口徑為 2030 年逾 1 兆美元"},{"item":"伺服器 CPU 市場（管理層，2030 年）","value":"約 2,200 億美元、年增 50% 以上（2026-08-04）；2026-05-05 為逾 1,200 億美元、年增 35% 以上；2025-11-11 為年增約 18%"},{"item":"高效能與 AI 運算整體（管理層）","value":"2030 年接近 2 兆美元，年增約 40%；AMD 目標成長高於市場"},{"item":"第三方 AI 資料中心 GPU 市場","value":"2025 年 111.2 億美元到 2030 年 323 億美元、年增 23.8%（GlobeNewswire 報告）；定義與管理層差距極大，不採用"},{"item":"AMD AI 加速器營收份額","value":"約 5–8%；輝達 70–80%；客戶自研晶片合計 15–20%（Silicon Analysts）"},{"item":"AMD 伺服器 CPU 營收份額","value":"46.2%（2026Q1 紀錄），出貨份額約三分之一"},{"item":"AMD x86 Client 出貨份額","value":"30.3%（2026Q2 首度破 30%，一年前 24.1%）"},{"item":"營業利益池占比五年前到現在","value":"事實表未涵蓋"}]},"moat":{"mechanism":"x86 伺服器 CPU 設計與小晶片成本結構領先，加上年更路線圖的執行紀錄；AI 端以開放軟體與記憶體容量做第二供應商。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"CPU：伺服器營收份額 46.2%（2026Q1 紀錄）高於出貨份額約三分之一，代表單價溢價；EPYC 交期逾 30 週；x86 整體份額 34.1%、年增 4.7 個百分點。AI：份額 5–8% 在升，但最大客戶 Meta 與微軟擴大自研晶片，屬最大客戶份額下滑的跡象，方向不能上調。","threats":[{"level":"🔴","text":"超大規模客戶自研 AI 晶片（Broadcom 代為設計）：Meta 在簽下 AMD 與輝達大單數週後擴大 MTIA 部署，微軟 Maia 200 已上線，OpenAI 與 Anthropic 也在做；這是客戶端的生態攻擊，直接壓縮 AMD 在同一批客戶的 GPU 可觸及市場。","p":40,"evidence_refs":["competitive_share_entrants#5","customer_second_source#0","customer_second_source#1","customer_second_source#2","substitute_technology#0"]},{"level":"🟡","text":"輝達的軟體與整櫃生態：加速器營收份額 70–80%，以絕對金額計差距仍在擴大；AMD 靠開放軟體與記憶體容量追趕。","p":30,"evidence_refs":["end_markets#5"]},{"level":"🟡","text":"ARM 架構伺服器 CPU：Lisa Su 2026-05-05 承認大型客戶會 x86 與 ARM 並用；Venice 宣稱每瓦效能是領先 ARM 方案的 3.3 倍，屬點對點競爭。","p":30,"evidence_refs":[]}],"roic_durability":{"quadrant":"投入資本事實表未涵蓋，象限無法判定；利益率端 GAAP 營業利益率 15.7%（過去四季）、non-GAAP 27%（2026Q2）屬中等。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（模型開發與推論服務）、決策者（雲端業者的基礎設施團隊）、付款者（雲端業者與 AI 實驗室）三環都在，推論算力是需要不是想要；但付款環最弱：OpenAI 首季虧 213 億美元、兩年融資缺口約 1,300 億美元。CPU 端付款者（雲端、企業）穩健，交期逾 30 週。"},{"item":"決策層級","level":"🟡","text":"在單一工作負載層級，客戶多家並用：Meta 同時簽輝達、AMD 又擴大自研；CPU 端 x86 相容，Intel 與 AMD 互換成本低，AMD 靠效能與總持有成本贏，不是靠鎖定。代理讀數：伺服器營收份額高於出貨份額，單價溢價仍在。"},{"item":"價值鏈分配","level":"🔴","text":"上游台積電約九成先進製程、HBM 短缺延續到 2027 年以後，兩者都有定價權；下游 GW 級客戶集中、有自研能力，還拿到 1.6 億股權證；AI 加速器利潤池大半留在輝達。AMD 的增量營收正好落在這段被兩頭擠壓的 AI 業務；CPU 段則相反。"},{"item":"社會容忍度","level":"🟡","text":"AI 晶片受美國出口管制與 25% 關稅，中國約占營收兩成；政策可一夜改變可銷售市場（2025 年曾認列 8 億美元相關費用）。價格上限主要是政治上限，授權依賴商務部逐案審查，屬政策風險。"}],"roiic":"事實表未涵蓋（缺投入資本、資本支出、折舊攤銷與營運資金變動）","reinvest_rate":"事實表未涵蓋；可見的再投資是存貨增到約 85 億美元、研發占營收 22.7%（同業對照表，過去四季）、對客戶與新創的股權安排","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。本包缺兩個輸入，不以估計數硬算；情境樹因此把共識成長視為超過可驗證的內生能力，熊市機率不低於 30%。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","AMD":53.2,"NVDA":74.67,"AVGO":68.77,"MRVL":52.21,"3661.TW":37.2,"unit":"%"},{"metric":"營業利益率","AMD":15.71,"NVDA":65.21,"AVGO":48.52,"MRVL":16.81,"3661.TW":24.0,"unit":"%"},{"metric":"FCF 利潤率","AMD":20.34,"NVDA":41.92,"AVGO":44.22,"MRVL":18.23,"3661.TW":-10.46,"unit":"%"},{"metric":"研發密度","AMD":22.74,"NVDA":7.79,"AVGO":13.28,"MRVL":25.84,"3661.TW":9.17,"unit":"%"}],"competitors":[{"name":"NVDA","gm":74.67,"om":65.21,"fcf_margin":41.92,"rd_intensity":7.79,"strategy_note":"AI 加速器營收份額 70–80%，營業利益率 65%、自由現金流率 42%，靠 CUDA 軟體與整櫃方案定價；AMD 以每美元 token 數切入，不是正面比毛利。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"strategy_note":"不直接賣 GPU，但替 Google、Meta、微軟、OpenAI、Anthropic 設計自研晶片，是 AMD 在 AI 加速器最大的間接對手；營業利益率 49%。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"MRVL","gm":52.21,"om":16.81,"fcf_margin":18.23,"rd_intensity":25.84,"strategy_note":"客製晶片與網通第二陣營，利益率結構（毛利 52%、營益 17%）與 AMD 接近，代表客製晶片端的價格競爭。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"3661.TW","gm":37.2,"om":24.0,"fcf_margin":-10.46,"rd_intensity":9.17,"strategy_note":"世芯，客製晶片設計服務，毛利 37%、自由現金流為負；是超大規模業者自研路線的執行者之一，份額擴張會壓縮通用 GPU 的可觸及市場。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主、價為輔：伺服器 CPU 量與單價同步成長、量較多；AI GPU 靠 GW 級合約放量；小型併購與回購不貢獻。","runway_years":"≥10 年（AI 加速器份額 5–8%，離 30% 很遠；伺服器 CPU 營收份額已 46%，這條跑道較短）","runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本與再投資率，內生天花板無法計算；共識 FY2026 到 FY2028 EPS 年化約 71%，主要來自營收放量加營業槓桿，不是再投資報酬。","segments":[{"item":"資料中心（EPYC 加 Instinct）","value":"2026Q2 營收 67 億美元，年增 107%、季增 16%，占營收 58%；部門營業利益率 31%"},{"item":"Client","value":"31 億美元，年增 23%（行動處理器創新高、Ryzen Pro 年增逾 50%）"},{"item":"遊戲","value":"7.79 億美元，年減 31%（主機週期尾聲、零組件漲價）；Client 加遊戲部門營業利益率 15%（去年 21%）"},{"item":"嵌入式","value":"9.77 億美元，年增 19%，部門營業利益率 40%（去年 33%）；全年新設計案有望逾 180 億美元"},{"item":"2027 管理層方向","value":"伺服器 CPU 年增逾 70%、資料中心部門遠超過翻倍；2026 下半年遊戲較上半年少 20% 以上"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"Q2 可比 EPS 年增約 82%、營收年增 50%；來源是營業槓桿，成長放緩時 EPS 會反向放大"},{"signal":"可觸及市場被替代技術壓縮","lit":true,"evidence":"Meta、微軟自研晶片已部署，Broadcom 替多家 AMD 客戶設計自研晶片"},{"signal":"毛利率連兩季年減","lit":false,"evidence":"Q1 55%（年增 170 基點）、Q2 56%（年增 200 基點）"},{"signal":"核心市占縮減","lit":false,"evidence":"伺服器與 Client 份額都創新高"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"只見於遊戲顯卡（產業零組件漲價），非主力"},{"signal":"自由現金流對淨利低於 0.75","lit":false,"evidence":"過去四季自由現金流率 20.3% 高於營業利益率 15.7%"},{"signal":"SBC 占營收逾 5% 且上升","lit":false,"evidence":"2026Q2 為 4.36%"},{"signal":"產業倍數系統性下移","lit":false,"evidence":"事實表未涵蓋"},{"signal":"維持性資本支出占自由現金流逾 60%","lit":false,"evidence":"事實表未涵蓋；委外製造模式"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"正在擴充晶圓、後段封裝與基板產能"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：近年併購是團隊與軟體型小案，對價事實表未涵蓋；股東回報只有抵銷稀釋的回購，現金去向已在理由段交代"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"ZT Systems（2025-03 完成，製造業務 2025-10 賣給 Sanmina）、MK1、FastFlowLM、Taalas（2026-08）；對價與併購後增量營業利益事實表未涵蓋，無法算已實現報酬","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2026Q1 買回 110 萬股、2.21 億美元（Jean Hu 2026-05-05），年化不到市值 0.1%（市值以判斷日股價乘指引股數 16.6 億估約 1.04 兆美元），遠低於 10 年期殖利率加 2%","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營收 4.36%；稀釋股數指引 Q2、Q3 都是 16.6 億股，股權激勵的稀釋被回購抵銷；Meta 權證不屬股權激勵，另列反證","grade":"過"}]},"valuation":{"basis":"前瞻本益比與 PEG（份額擴張型成長股的優先尺），以 FY2027、FY2028 共識為錨","tier":"大型 AI 算力晶片設計","peers":{"expanded":false,"reason":"事實表只收同業利潤率，未收同業前瞻倍數，屬資料缺口；終端倍數改用自身倍數與成長熄火情境校準"},"fwd_pe":82.29,"peg":1.15,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026 共識 7.58 的 82 倍、FY2027 15.57 的 40 倍、FY2028 22.27 的 28 倍；PEG 約 1.15（前瞻本益比 82.29 除以 FY2026 到 FY2028 兩年 EPS 年化約 71%），落在合理區。但 P/S 24.7 倍、EV/S 24.4 倍都在四個年度端點最高，股價高於賣方平均目標價，基本情境年化只有 6–7%。成長本身不貴，貴在已把管理層計畫當成確定，評偏貴。五年連續分位事實表未涵蓋（只有四個年度端點：本益比分位 43、P/S 與 EV/S 分位 100）。","upside_short_pct":-1.2,"upside_mid_pct":38.3},"trap_analysis":{"verdict":"🟡","label":"成長是真的，陷阱在價格與客戶集中"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"OpenAI 首季虧 213 億美元、兩年融資缺口約 1,300 億美元；S&P 以 OpenAI 曝險為主因把 Oracle 降到 BBB-；GW 級合約多年期、按里程碑，大部分營收尚未簽定出貨；Meta 簽約數週後擴大自研晶片。","assumption":"錨定客戶會照時程把 GW 級合約轉成實際採購。","consequence":"AI 資本支出在 2027–28 年轉入消化期時，AMD 身為第二供應商最先被砍；FY2031 EPS 可能停在 14 美元上下，股價回到約 280 美元（-55%）。這條與唯一致命點部分重疊，唯一致命點取其中最集中的一環（錨定客戶延後）。","ruling":"部分採納：熊市機率給 32%。不全採，因為伺服器 CPU 成長不依賴這幾家 AI 客戶，且 Meta 信用仍強（Moody's 2026-07-24），Anthropic 與微軟是新增分散。","watch":"錨定客戶部署進度、OpenAI 融資消息、評等機構動作","evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#4","customer_second_source#0"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Meta 取得 1.6 億股績效權證，約現有股數一成；Helios 的 HBM 比對手多約 50%，代搭的 HBM 不賺同等毛利（Lisa Su 2025-11-11），記憶體短缺延續到 2027 年以後；資料中心 AI 毛利率低於公司平均；Q2 自由現金流因備貨從 Q1 的 26 億降到 15.58 億美元。","assumption":"營收翻倍會等比例變成每股盈餘。","consequence":"營收照計畫走，但每股盈餘被權證稀釋與毛利組合拉低 10–15%。","ruling":"採納：基本情境 FY2027 EPS 取 15.0，低於共識 15.57，已反映部分稀釋；毛利率 55% 列為停損指標。","watch":"稀釋股數（指引 16.6 億）、non-GAAP 毛利率、存貨","evidence_refs":["customer_concentration_credit#1","supply_demand_durability#0"],"fact_refs":["f_kpi3_fcf","f_kpi4_sbc"]},{"view":"價格已反映太多","evidence":"股價 623.77 高於 S&P 彙整 55 位分析師平均目標 616.51 與 MarketBeat 565.13；前瞻本益比 82 倍（FY2027 約 40 倍）；P/S 24.7 倍在四個年度端點最高；26 週漲 204%，高出 52 週均線約 84%。","assumption":"市場已把管理層 2027–28 年計畫當成確定。","consequence":"基本情境五年總報酬約 38%、年化約 6–7%；Helios 放量只要晚一季，倍數壓縮就會先來。","ruling":"採納：現價不加碼；回到 490 美元以下，或 2026Q4 資料中心季增 ≥20% 且 FY2027 共識升到 17 以上，才重新加。","watch":"股價對 FY2027 共識 EPS 的倍數","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_ps_percentile","f_week26_return_pct","f_ma_w52"]}],"max_dd":{"lo":-72,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 470.79 → 本次 623.77（+32.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=470.79","side_b":"本次 price_at_dd=623.77","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2027 資料中心 AI 規模","cause":null,"prior_field":null,"side_a":"管理層：2027 資料中心部門遠超過翻倍，分析師估的 Instinct 約 300 億美元「大概太低」，Helios 需求量超過原先預測（2026-08-04 法說，Lisa Su）。","side_b":"GW 級合約多年期、按里程碑，大部分營收尚未簽定出貨；最大對手方 OpenAI 首季虧 213 億美元、兩年融資缺口約 1,300 億美元；S&P 以 OpenAI 曝險為主因把 Oracle 降到 BBB-。","ruling":"可調和（程度差異）：Meta 信用仍強，Anthropic 與微軟是新增分散，2027 翻倍的方向可信；金額上限取決於 OpenAI 能否籌到錢。基本情境 FY2027 EPS 取 15.0，略低於共識 15.57。","evidence_level":"管理層指引加第三方媒體與評等機構","settle_metric":"2026Q4、2027Q1 資料中心部門季增率","if_then":["若 2026Q4 資料中心季增 ≥20% 且 Q1 指引續增，則維持基本情境，股價 ≤490 美元時分兩筆加碼","若任一季季增 <10% 或 OpenAI 公開延後部署，則減碼一半"],"evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#3","customer_concentration_credit#4"]},{"axis":"2027 毛利率","cause":null,"prior_field":null,"side_a":"Jean Hu 2025-11-11：2027 資料中心 AI 量若很大，毛利率可能靠近 55% 區間下緣，MI450 是否稀釋「目前還不知道」；2026-05-05：MI450 毛利率低於公司平均。","side_b":"Jean Hu 2026-08-04：伺服器、嵌入式與 Client 可大致抵銷，但第三次仍不給 2027 毛利率數字；Helios 的 HBM 比對手多約 50%，記憶體短缺預期延續到 2027 年以後。","ruling":"可調和但偏空：管理層三次只給方向不給數字，HBM 成本又由 AMD 承擔，2027 毛利率跌破 55% 的機率不低；以 55% 設為停損指標。","evidence_level":"管理層前後說法加產業新聞","settle_metric":"2026Q4 non-GAAP 毛利率；FY2027 首次毛利率指引","if_then":["若 2026Q4 毛利率 ≥56% 且 FY2027 指引 ≥55%，則把毛利率風險降為觀察","若連兩季 <55%，則減碼三分之一"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"伺服器 CPU 市場規模口徑","cause":null,"prior_field":null,"side_a":"2025-11-11 分析師日：伺服器 CPU 市場未來 3–5 年年增約 18%。","side_b":"2026-05-05 改為年增 35% 以上、2030 年逾 1,200 億美元；2026-08-04 再改為年增 50% 以上、2030 年約 2,200 億美元（Lisa Su）。","ruling":"可調和：上修有實績支撐（Q2 雲端與企業伺服器都年增逾 70%、交期逾 30 週），但九個月內三度上修，市場規模數字不作估值依據，只認已實現的伺服器營收。","evidence_level":"管理層前後說法加已實現營收","settle_metric":"2026 下半年伺服器營收年增是否超過 80%","if_then":["若 2026 下半年伺服器年增 >80%，則 H2 維持，並把 2027 年增 70% 視為底線","若低於 60%，則停止加碼並把 H2 降為削弱"],"evidence_refs":["competitive_share_entrants#3","end_markets#1"]},{"axis":"費用紀律","cause":null,"prior_field":null,"side_a":"Jean Hu 2025-11-11 承諾營收成長快於費用；2026-08-04 再說費用增速會低於營收增速。","side_b":"Q2 營業費用 34 億美元，高於 2026-05-05 給的約 33 億美元；Q1 被問費用一再超過指引時未解釋；Q3 指引再升到 36.5 億美元。","ruling":"可調和：Q2 營收也超過指引約 3%，營收年增 50% 仍大於費用年增 40%，營業槓桿成立；但費用指引準確度差，營業槓桿以實際增速差認定，不看指引。","evidence_level":"公司指引與實際值","settle_metric":"營業費用年增率對營收年增率","if_then":["若營業費用年增連兩季高於營收年增，則 H3 降為削弱並停止加碼","若差距維持 10 個百分點以上，則 H3 維持"],"evidence_refs":[]},{"axis":"現在就賣對現在就買","cause":null,"prior_field":null,"side_a":"現在就賣的最強論證：股價已高於賣方平均目標價（616.51、565.13），前瞻本益比 82 倍、P/S 在四年高點、26 週漲 204%；基本情境五年年化只有 6–7%；只要 Helios 晚一季或毛利率跌破 55%，盈餘和倍數會一起修正。","side_b":"現在就買的最強論證：FY2027 共識自 7 月底 13.78 升到 15.57，30 天內 FY2027 上修 33 次對下修 3 次；管理層暗示分析師的 AI 營收估計太低；若 AI 份額到第三方估的 15–20%，FY2028 EPS 可到 27 美元，現價只有 23 倍。","ruling":"不可調和（估值方向相反，論點本身不矛盾）。裁決：持有，不加也不賣。依據：買方論點建立在尚未出貨的 Helios 量能，賣方論點建立在已經發生的價格；第一個完整放量季（2026Q4）出來前，價格這邊的證據較硬。硬數據點：股價是 FY2027 共識的 40 倍，基本情境五年總報酬約 38%。","evidence_level":"事實表加賣方彙整","settle_metric":"2026Q4 資料中心季增與 FY2027 共識 EPS","if_then":["若 2026Q4 資料中心季增 ≥20% 且 FY2027 共識 ≥17，則加碼至原部位 1.5 倍","若股價 ≥760 美元而 FY2027 共識 <17，則減碼三分之一","反向條件：若股價 ≤490 美元且共識不低於 15，則分兩筆加碼"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#4"]},{"axis":"前份漂移：價格","cause":"價格變動","prior_field":["dca_verdict","dca_role","signal","val","asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份 2026-08-05：股價 470.79 美元，判進場，估值合理，上下檔比 2.1，五年期望報酬 48.6%，基本情境年化 10.6%，訊號等級 B。","side_b":"本次：股價 623.77 美元（+32.5%）；FY2027 共識 15.57（前份 13.78，+13%），FY2028 22.27（前份 20.02，+11%）；股價漲幅約為盈餘上修的 2.5 倍，倍數擴張吃掉預期報酬。","ruling":"估值由合理轉偏貴；上下檔比、期望報酬與基本情境報酬由程式依新情境重算，預期明顯下降；訊號等級維持 B，因為生意品質沒變；裁決與角色若改列，原因是價格，不是基本面轉壞。","evidence_level":"事實表加前份摘要","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若倍數回到 31 倍以內（約 490 美元）且共識不降，則恢復分批加碼","若倍數升到 49 倍以上（約 760 美元）而共識未跟上，則減碼三分之一"],"evidence_refs":[]},{"axis":"前份漂移：情境樹","cause":"方法變動","prior_field":["bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：牛市五年價 1,260 美元、熊市 216 美元，機率牛 22%、熊 33%，最大回撤單點 -68%。","side_b":"本次：終端年改為 FY2031E，與起點同用前瞻一年口徑；熊市終端 EPS 14.0 壓在 FY2027 共識以下，倍數用成長降到 10% 的 20 倍；牛市 50 美元乘 30 倍；機率牛 22%、基本 46%、熊 32%；最大回撤改填範圍 -45% 至 -72%。","ruling":"熊市機率 33% 到 32% 屬微調：客戶自研與融資的負面證據增加，但 Anthropic、微軟兩家新客戶分散了單一對手方風險，大致抵銷；共識成長超過可驗證的內生能力，熊市機率不低於 30%。牛熊五年價由程式依新路徑重算。","evidence_level":"方法說明","settle_metric":"錨定客戶部署進度；2026Q4 資料中心季增","if_then":["若錨定客戶任一延後，則熊市機率上調至 40% 並減碼一半","若 2026Q4 資料中心季增 ≥20%，則牛市機率上調至 28%"],"evidence_refs":[]},{"axis":"前份漂移：品質與結構判斷","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：價值陷阱風險中等、護城河方向持平、五年後跑道寬、品質複利成長型、未判循環位置。","side_b":"本次結論相同，新證據兩面：x86 整體份額 34.1%、伺服器營收份額 46.2%、Client 出貨份額首度破 30%；同時 Meta 簽約數週後擴大自研晶片、微軟 Maia 200 已部署、Broadcom 替 OpenAI 與 Anthropic 設計自研晶片。","ruling":"正負證據互抵，五欄維持：CPU 份額上升，但 AI 端最大客戶在做自研，護城河方向不能上調；AI 份額 5–8% 離飽和很遠，跑道仍寬；成長仍以份額擴張加營業槓桿為主，不改判為循環股，所以不填循環位置。","evidence_level":"產業研究機構份額資料加媒體報導","settle_metric":"伺服器營收份額；AI 加速器份額","if_then":["若 Meta 或微軟公開以自研晶片取代 Instinct 部署，則護城河方向改為下降並減碼三分之一","若 AI 份額在 2027 年底前升過 12%，則護城河方向改為上升"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#0","customer_second_source#1","customer_second_source#2","substitute_technology#0"]},{"axis":"前份漂移：假設與風險門檻","cause":"方法變動","prior_field":["H","R"],"side_a":"前份：H1 2027 資料中心 AI 營收 ≥350 億美元；H2 EPYC 營收份額 ≥45%；H3 FY2027 共識 EPS ≥12；R1 資料中心占比升 5 個百分點而毛利率降 50 基點，或 FY2027 指引 <55%；R2 早期 Helios 客戶降到投機等級或延後，或自身投資支撐的營收占 2027 資料中心 AI 逾 15%；R3 任兩家雲端 2027 資本支出年增跌破 20% 或板塊倍數下移一個標準差。","side_b":"本次：H1 改為資料中心部門 2027 營收翻倍、每季季增 ≥10%；H2 改為伺服器營收份額每季 ≥45% 並朝 2030 年過 50%；H3 改為毛利率 ≥55%、non-GAAP 營業利益率 FY2027 ≥32%；前份 R1、R2 門檻保留在 R1、R2；前份 R3 保留為 R6；新增客戶自研晶片（R3）、中國與台灣（R4）、PC 與遊戲（R5）。","ruling":"H1 改門檻，因為公司不單獨揭露資料中心 AI 營收，無法按季驗證；H3 共識已到 15.57，舊門檻 12 失去鑑別力，改看營業槓桿本身。前份 R2 的自身投資比例、R3 的雲端資本支出與板塊倍數，本包事實表未涵蓋，標資料缺口保留，不退休。","evidence_level":"方法說明","settle_metric":"資料中心部門營收；毛利率；營業利益率","if_then":["若 FY2027 資料中心部門營收未達 FY2026 的 2 倍，則 H1 判反轉並減碼一半","若毛利率連兩季 <55%，則減碼三分之一"],"evidence_refs":[]},{"axis":"停損指標（減碼、清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標（null）。","side_b":"本次設五項：資料中心季增 <10%；毛利率連兩季 <55%；錨定客戶延後或縮減；伺服器份額兩季合計掉 3 個百分點以上；FY2027 共識下修逾 15%。任一觸發減碼三分之一（錨定客戶延後為減碼一半），兩項以上清倉。","ruling":"前份格式沒有這一欄，本次補上；門檻取自管理層 2026-08-04 的放量節奏與長期毛利率區間下緣 55%。","evidence_level":"方法說明","settle_metric":"五項停損指標","if_then":["若任一項觸發，則減碼三分之一","若兩項以上同時觸發，則清倉"],"evidence_refs":[]},{"axis":"重新加碼條件（加碼）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設（null）。","side_b":"股價回落到 490 美元以下（約 FY2027 共識 EPS 的 31 倍）且 FY2027 共識不低於 15 美元，才恢復分批加碼。","ruling":"前份在 470.79 美元已判進場，不需要重啟條件；本次現價的限制是價格，重啟條件就是價格回到基本情境年化約 12% 的位置（基本情境終值 862.5 美元折回五年）。","evidence_level":"情境樹推算","settle_metric":"股價與 FY2027 共識 EPS","if_then":["若股價 ≤490 美元且共識 ≥15，則分兩筆加碼","若共識跌破 13.2，則取消加碼條件，改依停損指標處理"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）。","side_b":"OpenAI、Meta、Anthropic 三個 GW 級錨定客戶中，任一家公開延後或縮減 MI450／Helios 部署。","ruling":"前份格式沒有唯一致命點；本次選這一項，因為它是最大的單一敏感度：每 GW 營收是雙位數十億美元（Lisa Su 2026-08-04），少一家等於 2027 年少掉以百億美元計的營收，毛利率每掉 1 個百分點的影響小一個量級。","evidence_level":"管理層每 GW 營收說法加情境推算","settle_metric":"錨定客戶部署公告","if_then":["若任一家延後兩季以上或縮減，則減碼一半並停止加碼","若兩家以上，則清倉"],"evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2"]}],"triggers":[{"n":1,"text":"2026Q3 財報：資料中心部門季增要到雙位數，且第四季指引的季增要高於第三季","type":"假設驗證","maps_to":"H1","metric":"資料中心部門營收季增率","threshold":"Q3 季增 ≥10%，Q4 指引季增高於 Q3","action":"達標續抱；未達停止加碼","source_freq":"每季財報","date":"2026-11（公司未公告確切日）"},{"n":2,"text":"伺服器 CPU 份額：Venice 世代上市後份額要續升","type":"假設驗證","maps_to":"H2","metric":"Mercury Research 伺服器 CPU 營收份額","threshold":"每季 ≥45%，連兩季合計下滑不超過 3 個百分點","action":"跌破門檻停止加碼；跌破 42% 減碼三分之一","source_freq":"每季","date":null},{"n":3,"text":"毛利率守不住 55%：Helios 放量與 HBM 成本壓過組合改善","type":"風險","maps_to":"R1","metric":"non-GAAP 毛利率","threshold":"單季 <55%，或 FY2027 首次毛利率指引 <55%","action":"減碼三分之一","source_freq":"每季財報","date":"2027-02","evidence_refs":["supply_demand_durability#0"]},{"n":4,"text":"錨定客戶融資與信用：OpenAI 融資結果與評等機構對其相關業者的動作","type":"風險","maps_to":"R2","metric":"OpenAI 大型融資結果；以 OpenAI 曝險為由的降評","threshold":"OpenAI 大型融資失敗，或再有一家 AMD 客戶因 OpenAI 曝險被降到投機等級","action":"停止加碼","source_freq":"事件","date":null,"evidence_refs":["customer_concentration_credit#2","customer_concentration_credit#4"]},{"n":5,"text":"客戶自研晶片擠壓 AMD 在同一批客戶的份額","type":"風險","maps_to":"R3","metric":"AMD AI 加速器份額（第三方估計）；Meta、微軟自研晶片部署公告","threshold":"2027 年底份額仍低於 10%，或 Meta、微軟公開以自研晶片取代 Instinct 部署","action":"減碼三分之一","source_freq":"半年","date":"2027-12","evidence_refs":["customer_second_source#0","customer_second_source#2","substitute_technology#0"]},{"n":6,"text":"唯一致命點：OpenAI、Meta、Anthropic 任一家公開延後或縮減 GW 級部署","type":"Single Thing","maps_to":"H1","metric":"錨定客戶部署公告與公司法說進度","threshold":"任一家延後兩季以上或縮減規模","action":"減碼一半並停止加碼；兩家以上清倉","source_freq":"事件","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":7,"text":"股價回到約 FY2027 共識 EPS 的 31 倍以內，且共識不降","type":"估值rearm","maps_to":"H3","metric":"股價對 FY2027 共識 EPS","threshold":"股價 ≤490 美元且 FY2027 共識 EPS ≥15","action":"分兩筆加碼","source_freq":"每日股價加每月共識快照","date":null},{"n":8,"text":"Helios 放量明顯超標，共識追上","type":"加碼","maps_to":"H1","metric":"2026Q4 資料中心季增；FY2027 共識 EPS","threshold":"Q4 資料中心季增 ≥20% 且 FY2027 共識 ≥17","action":"加碼至原部位 1.5 倍","source_freq":"每季加每月","date":"2027-02"},{"n":9,"text":"股價跑在盈餘前面","type":"減碼","maps_to":"H3","metric":"股價與 FY2027 共識 EPS","threshold":"股價 ≥760 美元（約 FY2027 共識 49 倍）且 FY2027 共識 <17","action":"減碼三分之一","source_freq":"每日","date":null},{"n":10,"text":"停損指標任兩項同時觸發","type":"清倉","maps_to":"H1","metric":"五項停損指標","threshold":"任兩項觸發","action":"清倉","source_freq":"每季","date":null},{"n":11,"text":"FY2026 年報與 FY2027 首次全年指引出來後，重做完整研究","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重做完整研究","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"資料中心部門單季營收季增率","bear_threshold":"2026Q4 或 2027Q1 任一季 <10%","window":"2026Q4 至 2027Q2 財報","source":"公司季報新聞稿","last_status":"ok"},{"metric":"non-GAAP 毛利率","bear_threshold":"連續兩季 <55%","window":"2026Q4 至 2027Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"錨定客戶（OpenAI、Meta、Anthropic）部署進度","bear_threshold":"任一家公開延後兩季以上或縮減規模","window":"2026Q4 至 2027Q4","source":"公司法說、客戶公告","last_status":"warning"},{"metric":"伺服器 CPU 營收份額","bear_threshold":"連兩季合計下滑 3 個百分點以上","window":"每季","source":"Mercury Research","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"較 15.57 下修逾 15%（低於 13.2）","window":"每月快照，至 2027-06","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=203.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價回落到 490 美元以下（約 FY2027 共識 EPS 的 31 倍）且 FY2027 共識不低於 15 美元，才恢復分批加碼","exec_line":"現價持有，不追也不賣；≤490 美元分兩筆加碼；Q4 資料中心季增 ≥20% 且 FY2027 共識 ≥17 可加到 1.5 倍；≥760 美元而共識未跟上減碼三分之一；錨定客戶延後減碼一半，兩家以上清倉"},"reasoning":{"industry":"AMD 賣三類晶片。資料中心（EPYC 伺服器 CPU 加 Instinct GPU）2026Q2 營收 67 億美元，年增 107%，占營收 58%，部門營業利益率 31%；Client 31 億美元（年增 23%）；遊戲 7.79 億美元（年減 31%）；嵌入式 9.77 億美元（年增 19%，利益率 40%）。全公司 Q2 營收 115.36 億美元，高於共識；non-GAAP 營業利益率 27%，GAAP 17%。Q3 指引 130 億美元上下 3 億、毛利率約 56%。單點依賴：FY2025 年報沒有單一客戶占營收 10% 以上，但未來營收正往 OpenAI、Meta、Anthropic 三家 GW 級合約集中，這是集中度風險，不是護城河證據。產業時鐘判第二期擴張：需求預測仍在上修、產能仍在加、交期仍長；但客戶舉債擴建、供應商用權證換訂單，已是過熱前的訊號。產業態勢是雙向拉鋸：CPU 端結構性轉好（Intel 各區隔都在失份額），AI 端競爭與客戶自研晶片在加壓。","moat":"機制：x86 伺服器 CPU 的設計與小晶片（chiplet，把大晶片拆成多顆小晶片再封裝，新製程用的晶圓較少）成本結構領先，加上年更路線圖的執行紀錄；AI 端靠開放的 ROCm 軟體與較大的記憶體容量，以第二供應商身分切入。執行力給 9：Venice、MI455X 已量產，Helios 本季出貨，伺服器與 Client 份額都創新高。定價力給 7：CPU 端營收份額高於出貨份額、交期逾 30 週、成本上漲可和客戶分攤；AI 端靠每美元 token 數賣、對 Meta 發權證、資料中心 AI 毛利率低於公司平均，拉低整體。對最強同業輝達的利益率差距為負且大（過去四季毛利率 53.2% 對 74.7%、營業利益率 15.7% 對 65.2%），所以不給 A。當期 ROIC 因事實表缺投入資本無法算；四個持續期檢查點中，價值鏈分配最弱。","growth":"成長以量為主：Q2 伺服器 CPU 量與單價都雙位數成長、量較多（Lisa Su 2026-08-04）；AI GPU 靠 GW 級合約放量；併購與回購不是來源。共識 EPS FY2026 7.58、FY2027 15.57、FY2028 22.27，兩年年化約 71%；FY2025 實際值事實表未涵蓋，無法算三年。近 3 個月 FY2026 共識上修 2.85%。內生天花板因缺投入資本與再投資率無法計算；缺口可部分歸因於營業槓桿（Q2 營收年增 50%、營業費用年增 40%，non-GAAP 營業利益率 27% 往長期模型 35% 以上走），其餘靠錨定客戶放量，所以長期信心上限為中。衰退訊號亮兩個：EPS 成長明顯快於營收、可觸及市場被客戶自研晶片壓縮；價值陷阱風險中等。","governance":"自由現金流 Q2 15.58 億美元（營收的 13.5%），比 Q1 的 26 億美元少，主因存貨增到約 85 億美元備貨；過去四季自由現金流率 20.3%，高於 GAAP 營業利益率 15.7%，現金轉換好。SBC 占營收 4.36%，稀釋股數指引連兩季都是 16.6 億股，回購（Q1 買回 2.21 億美元、剩餘授權 92 億美元）只抵銷股權激勵。現金去向：主要是研發（研發密度 22.7%，Q2 營業費用年增 40%）、供應鏈擴產與備貨，其次是小型併購（ZT Systems、MK1、FastFlowLM、Taalas）；股息事實表未涵蓋，法說只提回購。給 Meta 的 1.6 億股績效權證約為現有股數一成。季末現金與短期投資 131 億美元。","valuation":"市場隱含：以 623.77 美元、要年化 10%，FY2031 EPS 需約 40 美元並給 25 倍前瞻本益比，等於共識 FY2028 22.27 之後還要再年增約 21% 三年。基本情境報酬拆解：EPS 複利年化約 35%，倍數由 82 倍壓到 25 倍年化約 -21%，股息與淨回購約 0，合計年化約 6–7%，重估是拖累不是來源。成長熄火測試：FY2028 之後成長降到 15%、10%、5%，分別給 25、20、15 倍，兩年後股價約 640、490、351 美元，三個情境只有一個守住現價。賣方目標價：S&P 彙整 55 位分析師平均 616.51、MarketBeat 565.13，現價已高於兩者；彙整間差距約 1.09 倍，未到要下修信心的程度。動能：26 週漲 204%，股價高出 52 週均線約 84%，距前份判斷 7 週漲 32.5%，約 9 月 21 日另有單日漲 8.8% 創新高的報導，判為過熱；RSI 資料不可用，未採用。","premortem":"最可能的虧損路徑：錨定客戶延後加上客戶自研擠壓，同時前瞻本益比從 82 倍壓縮；最大回撤範圍 -45% 至 -72%（回到 52 週均線即 -46%）。空方最強數字：股價已高於賣方平均目標價，OpenAI 兩年融資缺口約 1,300 億美元。訴訟與監管：查無 SEC 調查或重大財報重編（FY2025 年報與 2026 各季季報）；監管風險集中在出口管制與關稅。"},"plain":{"six":{"how_it_makes_money":"賺的是雲端業者與 AI 實驗室的算力資本支出：資料中心已占營收 58%；錢卡在兩個節點，上游是台積電先進製程與 HBM 供給，下游是少數 GW 級客戶的付款能力。","moat":"護城河方向持平：CPU 端在擴大，AI 端被客戶自研晶片與輝達生態夾住，兩邊互抵，所以不能上調。","growth":"五年後跑道仍寬：AI 加速器份額只有 5–8%，代理式 CPU 是管理層點名的下一條成長曲線；但共識成長靠營業槓桿與少數大客戶放量，不是可驗證的再投資報酬。","capital":"資本配置中等：錢幾乎全數投回研發、擴產與備貨，回購只夠抵銷股權激勵；對大客戶發權證是新的隱性成本。","valuation":"現價要求 FY2031 EPS 做到約 40 美元並維持 25 倍，才有年化 10%，比管理層「顯著超過 20 美元」的計畫再多一段；方向我相信，但現價已沒有多餘報酬，估值偏貴。","how_wrong":"最可能看錯的地方是錨定客戶的付款能力與自研晶片的速度，不是 AMD 的產品力；看錯時盈餘和倍數會一起往下。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":623.77,"week26_return_pct":203.69,"consensus_rev_3m_pct":2.85,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 是 Helios 放量前一年，前瞻一年倍數 82 倍偏高是時間差，不是一次性費用；判斷改看 FY2027、FY2028 共識，分母本身不是爭點。過去四季盈餘口徑的本益比 156 倍反映放量前的低基期，不採用。短期上檔以 S&P 平均目標價 616.51 計，中期以基本情境五年終值計。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026Q3 財報與 Q4 指引（Helios 首批出貨後第一份數字）","impact":"高","watch":"資料中心季增、毛利率、Q4 指引"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"Helios 第四季放量、Venice 雲端部署開始","impact":"高","watch":"客戶部署公告與出貨節奏"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 年報與 FY2027 首次全年指引（含毛利率）","impact":"高","watch":"毛利率指引是否 ≥55%"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"Anthropic 首個 GW 部署開始（上半年）","impact":"中","watch":"部署進度"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"台積電亞利桑那第二廠 3 奈米目標量產（2027 下半年）","impact":"低","watch":"AMD 是否取得台灣以外的先進製程產能"}],"_projected_from":"v19"}
```
