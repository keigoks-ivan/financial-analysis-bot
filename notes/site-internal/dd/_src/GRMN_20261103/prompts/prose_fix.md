你是 stock-analyst v20 的**散文層（prose）agent**，標的 GRMN（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRMN_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：GRMN　日期：2026-11-03　archetype：None　前份裁決：2026-07-30　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1815B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（441B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（870B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1279B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1278B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（738B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（966B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2291B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3517B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2939B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1815           3629-5185      5 條（2–6 內）  
s3                  8000         441           5291-7559      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3427          8101-11573      5 條（2–6 內）  
s6                 11000         738          7183-10262      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         966           1774-2534      5 條（2–6 內）  
s10                 5000        2291           1896-2709      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2939           2000-2061      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4867B；至少需散文≈40.13KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−55%
−53%
−40%
−35
−35%
−20%
−6.1%
−5%
−3.6%
−2%
−0.6
−0.6%
0%
0.1
0.12
0.2
0.4
0.5
0.53
0.6
0.66
0.75
0.82
0.88
0.92
0.94
1
1%
1.08
1.13
1.21
1.3
1.32
1.36
1.4
1.4%
1.41
1.5%
1.54
1.7
1.74
1.8%
1.88
02
2%
2
2.02
2.1
2.2
2.3%
2.31
2.33
2.53
2.6
3
3%
03
3.10
3.3%
3.5%
3.55%
3.8%
4
4%
4.07
4.20
4.7%
5
05
5%
5.1
5.2
5.6%
5.8
5.97
6%
6
06
6.1%
6.12
6.49
6.76
6.9
6.94
7%
7
07
7.2
7.3%
8
8%
8.1
8.5%
8.57
8.59
9%
9
9.2%
9.70
9.7
10.0
10%
10
10.1
10.13
10.2
10.2%
10.49
10.6
10.8%
10.80
11
11%
$11.05
11.1
11.3
11.30
11.35
11.4
11.8
12.0
12
12%
12.5
12.50
12.5%
12.74
12.9%
13%
13.4
13.5
13.6
14
14%
14.0%
14.2%
14.70
14.7
15
15%
15.3%
15.4
15.8
16%
16.0
16.5%
16.6
16.7
16.9%
16.9
16.95
17
17%
17.2
17.3%
17.7%
17.9%
18
18.0%
18.5
18.9
19.4%
19.86
20
20%
20.3
20.8
21
21%
21.1
21.2%
22%
22
22.5
22.9
24%
24
24.2
24.38
24.4
25
25%
25.9%
26%
26
26.38
26.4
26.6
27%
28
28.8%
29%
29
29.1
29.3
29.3%
30
30%
30.8%
31
32%
33%
33.2%
35%
35.0
37%
39%
40%
41
42
45%
45
45.5%
46%
47%
48%
48.7%
49
50%
57.5%
58.5%
58.7%
59.0%
59.7%
60%
61%
61.1%
63%
63.3%
64%
65%
68%
69.8%
70
76%
78%
81.5
90
91.4
100
100%
119%
120
131
135
150
150%
160
166.5
174
180
192.7
192.82
200
210
213
230
275
$276
276.75
284
294.83
300
310
320
323
360
370
416
420
455
481
2022
2023
2024
2025
2026
2027
2028
20261103
1,000
1,200
2,100
2,500
3,300
4,100
4,470
5,400
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
{"meta":{"ticker":"GRMN","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Garmin Ltd."},"oneliner":"Garmin 在下滑的穿戴市場持續拿份額、利潤率創高，但 2026 年 61% 毛利率含關稅退款與低價記憶體庫存，管理層已預告 2027 回到歷史區間；現價約 24 倍 FY2027 共識，要 EPS 年增約 12.5% 或倍數不降才有 10% 年報酬，等 230 美元以下或 2027-02 指引再看","thesis":{"H":[{"id":"H1","text":"高階穿戴（Fitness＋Outdoor）在整體穿戴出貨下滑的市場裡繼續拿份額，成長以新用戶與新品類（CIRQA）為主、不靠併購","2y":"FY2026–FY2027 Fitness＋Outdoor 合計營收每年年增 ≥10%，Omdia 份額 ≥13%","5y":null,"10y":null,"threshold":"Fitness＋Outdoor 合計營收年增 ≥10%；Omdia 智慧手錶份額 ≥13%（2Q26 為 15%）","source":"Garmin 季度 8-K 分部營收；Omdia 季度出貨新聞稿","drift_rule":"兩年期：TTM 合計營收低於 10% 年增路徑 5% 以上連 2 季＝削弱；低 10% 以上連 3 季＝反轉"},{"id":"H2","text":"毛利率回到歷史區間時，靠費用槓桿、規模與垂直整合把營業利益率守在 26% 以上，FY2027 EPS 不倒退","2y":"FY2027 營業利益率 ≥26%、pro forma EPS ≥10.80 美元","5y":null,"10y":null,"threshold":"FY2027 營業利益率 ≥26%（FY2025 為 25.9%，FY2026 指引 29%）","source":"2027-02 全年指引；季度 8-K 損益","drift_rule":"兩年期：TTM 營業利益率低於 26% 達 1.3pp（偏離 5%）以上連 2 季＝削弱；低 2.6pp（偏離 10%）以上連 3 季＝反轉"},{"id":"H3","text":"成長的資本需求可控：泰國廠與記憶體存貨是一次性墊高，FY2027 起 FCF÷淨利回到 0.75 以上，FY2026–FY2031 營收年複合 ≥8% 且以有機為主","2y":null,"5y":"FY2031 營收約 120 億美元以上（FY2026 指引 81.5 億×1.08⁵），FCF÷淨利 ≥0.75","10y":null,"threshold":"FCF÷淨利 ≥0.75（2025 年 0.82、2026E 約 0.53）；營收五年年複合 ≥8%","source":"10-K 現金流量表與損益表；季度 10-Q 存貨","drift_rule":"五年期：TTM 偏離門檻 5% 以上連 4 季＝削弱；10% 以上連 6 季＝反轉"}],"R":[{"id":"R1","text":"記憶體與其他零組件漲價（AI 需求排擠）在 2026Q4–2027 吃進毛利率，部分供應商是單一來源，安全庫存用完後全面反映市價","h_ref":"H2","clock":"⚡","threshold":"季度毛利率年減 >300bp（扣除關稅退款）連 2 季，或 FY2027 毛利率指引 <57.5%","evidence_refs":["supply_demand_durability#2","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R2","text":"Apple／Samsung／Huawei 用手機生態補齊運動健康功能，Whoop／Oura 等專業品牌複製功能，加上 OEM 客戶自製，侵蝕高階穿戴份額與單價","h_ref":"H1","clock":"🔥","threshold":"Fitness 營收年增連 4 季 <5% 且 Omdia 份額 <12%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0","customer_second_source#0"]},{"id":"R3","text":"消費產品主要在台灣製造，暴露於關稅與兩岸風險；泰國廠 2027Q1 才投產，2026Q1 Marine 毛利率就曾因關稅年減 200bp","h_ref":"H3","clock":"🐢","threshold":"任一分部毛利率因關稅年減 ≥200bp 連 2 季，或泰國廠投產延後到 2027Q2 以後","evidence_refs":["geo_supply_chain#0","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R4","text":"大型零售客戶要求促銷壓毛利，加上主動墊高存貨（Q3 22.5 億美元），若需求轉弱會變成去化折價","h_ref":"H3","clock":"🔥","threshold":"存貨÷當季營收 >1.3 連 2 季（Q3 2026 為 1.13），或 Fitness／Outdoor 毛利率年減 ≥200bp","evidence_refs":["customer_concentration_credit#1"]},{"id":"R5","text":"監管與技術依賴類尾端風險：波蘭競爭機關 2024 年對 Garmin Polska 與經銷商價格協議的調查未見結果；GNSS 干擾與欺騙可能損害定位功能","h_ref":"H1","clock":"🐢","threshold":"UOKiK 公告裁罰（受影響營收事實表未涵蓋），或 GNSS 干擾導致產品功能停用／召回","evidence_refs":["regulatory_antitrust#2","substitute_technology#1"]}],"single_thing":{"description":"FY2027 實際 pro forma EPS 低於 FY2026 的約 10.80 美元（EPS 年減）；2027-02 公布的全年指引是第一個讀數","why_fatal":"營業利益率每 100bp 約等於 EPS 0.4 美元（約 4%），是五年路徑裡最大的單一敏感項；EPS 年減代表記憶體成本與 Mercedes 低毛利組合吃掉整年營收成長，基本情境 FY2027 的 11.30 不成立，倍數也會往 20 倍以下靠","if_happens":"Bear 機率由 30% 升到 40%，230 美元的價格門檻失效，改等 2027Q1 實際毛利率；若已持有則減碼一半","how_monitor":"2027-02 Q4 法說的 FY2027 指引；在那之前看 Q4 2026 實際毛利率與營業利益率","probability":"約 25%（12–24 個月）：以 FY2026 指引的稅率與非營業收入不變推算，營收照共識成長 12% 時，營業利益率要低於約 25.9% 才會年減；FY2025 在毛利率 58.7% 時營業利益率已有 25.9%，要毛利率跌破歷史區間或營收明顯放慢才會發生"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":24.38,"peg_fy2":1.74,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":8.59,"FY2026E":10.49,"FY2027E":11.35,"FY2028E":12.74},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識（2026-10-31 快照，EPS 家數事實表未涵蓋）；FY2025A 用年報稀釋 EPS 8.59（GAAP）。公司 pro forma 口徑 FY2026 指引 10.80、較上年 +26%，回推上年約 8.57，與 GAAP 差異很小"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRMN_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"淨現金、營業利益率 29%、營收四年年複合約 14%，但毛利受記憶體等零組件成本循環影響"},"industry":{"clock_phase":"II","sd_verdict_source":"需求面結構性持久（健康與運動穿戴、新用戶占比高、Connect+ 續訂強）；成本面週期性將反轉（記憶體短缺預期延續到 2027，供給可逆性高）。來源：Q3 2026 法說（2026-10-28）與 the5krunner（2026-10-28）","bargaining":{"up":"對上游轉弱：記憶體、半導體、LCD 部分單一來源，AI 需求讓記憶體廠議價力上升，公司以安全庫存與預付款換供給","down":"對下游穩定：前十大客戶占 20%–25%、無單一客戶超過 10%，直營超過 10%；大型零售可要求加碼促銷壓毛利","geo":"消費產品主要在台灣自有工廠製造，泰國廠 2027Q1 投產後分散；APAC 成長 4%，中國市場疲弱"},"profit_pool_dir":"利潤池短期往上游記憶體廠移動（管理層預告 2027 毛利率回到歷史區間）；下游通路分配穩定","tam_table":{"expanded":false,"reason":"事實表未涵蓋穿戴 TAM、滲透率與利潤池占比；只有份額（Omdia 15%、Counterpoint 5.6%，口徑不同），份額已寫進護城河段，滲透率列資料缺口"}},"moat":{"mechanism":"垂直整合（自有台灣工廠）＋運動戶外專業功能與 Connect 資料累積的轉換成本＋航空認證與改裝存量＋船用經銷商口碑","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：Omdia 2Q26 份額 11%→15%（Apple 48%→46%），Counterpoint 出貨 +11%，Q3 主要分部毛利率扣除關稅退款仍擴張；定價權持平：管理層把漲價列為工具之一但不承諾。反例：fēnix 9 屬產品週期，首波需求以舊用戶換機為主，2027 下半年換機潮退去後要再驗","peer_na_reason":"事實表無同業 ROIC 與歷史利潤率，以 TTM 營業利益率代理","threats":[{"level":"🟡","text":"Apple／Samsung／Huawei 以手機生態補齊運動健康功能，Coros、Whoop、Oura 等專業品牌複製部分功能；目前份額數據顯示未造成損害","p":"30%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"OEM 客戶自製目前向 Garmin 採購的設備與零組件（車用 domain controller、航空 OEM）；10-K 未點名客戶、無已發生事件","p":"20%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"大型零售客戶要求更多促銷壓低毛利率，失去任一大客戶會有重大影響；前十大占 20%–25%","p":"25%","evidence_refs":["customer_concentration_credit#1"]}],"roic_durability":{"quadrant":"高利益率（稅後營業利益率約 24%）×周轉率待補（事實表未涵蓋投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是消費者本人，三角色一致；但運動錶屬想要而非需要，可延後購買（Marine 終端偏軟、油價高讓買家觀望）。代理讀數：Q3 註冊量高於進貨、零售商 Q4 拉貨強，健康需求有世代與政策順風，判中性偏正"},{"item":"決策層級","level":"🟢","text":"替代性在個人裝置與機身層級衡量：fēnix 首波買家多為跨一代以上的舊用戶換機，Connect+ 免費期後續訂強；航空端改裝要重新認證（G1000 King Air 改裝破 1,000 套），換供應商成本高。漲價後流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"自有工廠吃下製造環節利潤，但 AI 需求讓記憶體廠議價力上升，2027 毛利率回到歷史區間就是價值往上游移；下游前十大客戶占 20%–25%、無單一客戶超過 10%，大型零售可要求促銷，判中性"},{"item":"社會容忍度","level":"🟢","text":"非必需品、無價格管制與監管授權依賴，漲價不構成社會或政治議題；相關的只有 FCC 與歐盟產品認證，屬一般性要求"}],"roiic":"代理約 119%（2022→2025 淨利增加 6.9 億美元 ÷ 2023–2025 累計〔淨利−FCF〕5.8 億）；前瞻假設約 50%","reinvest_rate":"代理 2023–2025 約 13%；2026E 約 47%（淨利約 20.8 億−FCF 約 11 億）；前瞻假設約 25%","endo_ceiling":12.0,"formula_note":"內生成長率＝增量報酬×再投資率；再投資率原式＝（資本支出−折舊攤銷＋營運資金變動＋收購淨額）÷稅後營業利益，事實表無折舊攤銷、營運資金變動與投入資本，改用（淨利−FCF）代理淨再投資、淨利代理稅後營業利益，SBC 被加回使再投資低估。歷史代理 119%×13%≈16%，泰國廠與存貨策略墊高再投資、增量報酬應下降，前瞻取 50%×25%≈12%（兩個比率是假設，非事實表數字）"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","GRMN":61.12,"AAPL":48.65,"LOGI":45.48,"TRMB":69.8,"unit":"%"},{"metric":"營業利益率","GRMN":28.82,"AAPL":33.17,"LOGI":17.87,"TRMB":17.68,"unit":"%"},{"metric":"FCF 利潤率","GRMN":18.61,"AAPL":29.28,"LOGI":19.25,"TRMB":20.44,"unit":"%"},{"metric":"研發密度","GRMN":15.31,"AAPL":9.19,"LOGI":6.72,"TRMB":17.33,"unit":"%"}],"competitors":[{"name":"AAPL","gm":48.65,"om":33.17,"fcf_margin":29.28,"rd_intensity":9.19,"strategy_note":"營業利益率 33.2%、FCF 利潤率 29.3% 都高於 GRMN，靠 iPhone 綁定與規模；手錶是 iPhone 配件，Omdia 份額 48%→46% 顯示它沒有在運動戶外高階段擠掉 Garmin","period":"TTM ending 2026-06-30（4季加總）"},{"name":"LOGI","gm":45.48,"om":17.87,"fcf_margin":19.25,"rd_intensity":6.72,"strategy_note":"毛利率 45.5%、營業利益率 17.9%，代表一般消費周邊的利潤水準；GRMN 高出約 11pp，說明它不是被當成普通消費硬體在賣","period":"TTM ending 2026-09-30（4季加總）"},{"name":"TRMB","gm":69.8,"om":17.68,"fcf_margin":20.44,"rd_intensity":17.33,"strategy_note":"毛利率 69.8% 高於 GRMN，但研發密度 17.3%、營業利益率只有 17.7%；同是定位技術，GRMN 靠消費規模攤薄費用","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（穿戴出貨與份額提升）＋高階組合；併購（TrainingPeaks／TrainHeroic）不重大；回購可忽略","runway_years":"事實表未涵蓋滲透率，無法推算；以份額代理：Omdia 智慧手錶 15%、Counterpoint 5.6%","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段再投資空間：前瞻增量報酬約 50%×再投資率約 25%≈12%；歷史代理值 119%×13%≈16%，因泰國廠與存貨策略墊高再投資、增量報酬應下降，取 12%","segments":[{"item":"Fitness","value":"Q3 6.94 億美元，+16%，毛利率 63%、營業利益率 33%，營業利益 2.31 億"},{"item":"Outdoor","value":"Q3 5.97 億美元，+20%，68%／39%，營業利益 2.33 億"},{"item":"Marine","value":"Q3 3.10 億美元，+16%，64%／30%，營業利益 0.94 億（含關稅退款）"},{"item":"Aviation","value":"Q3 2.53 億美元，+5%，78%／26%，營業利益 0.66 億"},{"item":"Auto OEM","value":"Q3 1.32 億美元，−20%，毛利率 16%，營業虧損 0.12 億；Q4 降幅相近，2027 靠 Mercedes 回到成長"},{"item":"來源","value":"Q3 2026 法說逐字稿（2026-10-28 CEO）與 8-K 新聞稿"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"evidence":"Q2 +360bp、Q3 +420bp（含關稅退款）；Q4 起記憶體成本是下一個檢查點"},{"item":"核心市占近 12 個月縮減","lit":false,"evidence":"Omdia 2Q26 份額 11%→15%；Counterpoint 出貨 +11%"},{"item":"主力產品提價後銷量下滑","lit":false,"evidence":"事實表無提價與銷量對照；2025 穿戴成長主要來自量"},{"item":"EPS 年複合比營收高 5pp 以上","lit":true,"evidence":"2022→2025 EPS 19.4% 對營收 14.2%，差 5.2pp；前瞻 FY2025→FY2027 差約 2.6pp"},{"item":"FCF÷淨利連 2 年低於 0.75","lit":false,"evidence":"2025 年 0.82；2026E 約 0.53，FY2027 若仍低於 0.75 即亮"},{"item":"SBC÷營收高於 5% 且逐年上升","lit":false,"evidence":"Q3 約 2.3%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"Omdia 新聞稿標題稱整體穿戴出貨 −2%，但轉向無螢幕手環與進階運動錶，兩者都是 Garmin 有產品的品類"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"evidence":"事實表未涵蓋同業倍數歷史"},{"item":"維護性資本支出占 FCF 超過 60%","lit":false,"evidence":"2026 資本支出約 5 億美元，含泰國新廠擴產，總額只占 FCF 約 45%；維護性占比事實表未涵蓋"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"泰國廠 2027Q1 投產，營收仍雙位數成長"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長以有機為主、併購不重大；現金去向集中在股利（每季約 2.02 億美元）、資本支出（全年約 5 億）與存貨預付，回購規模小"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"TrainingPeaks／TrainHeroic 2026-07-20 完成，條件未揭露、對合併財報影響不重大，沒有可算的已實現報酬","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q3 回購 4,100 萬美元，以 Fwd P/E 約 26.4 倍買入，買入收益率約 3.8%；10 年期殖利率事實表未涵蓋，要過門檻需 10 年期低於約 1.8%，判不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"流通股 2026-05-22 為 192.82 百萬股、判斷日 192.7 百萬股，淨稀釋約 0%；Q3 SBC 4,470 萬美元，占營業利益 7.3%","grade":"過"}]},"valuation":{"basis":"Fwd P/E（主錨 FY2027 共識 11.35 美元；FY2026 共識含關稅退款與低價記憶體庫存）","tier":"介於高毛利品牌消費硬體與高 ROIC 利基複利之間（前份同業分類）","peers":[{"item":"Logitech（高毛利品牌消費硬體）","value":"16.6 倍（前份 2026-07-30 記載，非本次事實表）"},{"item":"Amer Sports","value":"22.9 倍（同上）"},{"item":"YETI","value":"15.4 倍（同上）"},{"item":"Apple（高 ROIC 利基複利）","value":"35.0 倍（同上）"},{"item":"TransDigm","value":"29.3 倍（同上）"},{"item":"Honeywell","value":"24.2 倍（同上）"},{"item":"GRMN","value":"26.4 倍 FY2026 共識／24.4 倍 FY2027 共識（本次事實表）"}],"fwd_pe":26.38,"peg":1.88,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"Fwd P/E 26.4 倍（FY2026 共識）、24.4 倍（FY2027 共識）；trailing P/E 26.6 倍在 4 個年度端點第 90 分位，P/S、EV/S 在第 100 分位；三年共識 EPS 年複合 14.0%（FY2025A 8.59→FY2028E 12.74），PEG 1.88 屬合理偏貴，若改看 FY2026→FY2028 的 10.2%，PEG 約 2.6。五年分位事實表未涵蓋（只有 4 個年度端點），留空。基本情境五年年報酬約 6%，要 10% 需倍數不降或 EPS 年增約 12.5%，判偏貴、未到極貴。短期以 12 個月後 FY2028E 基本情境 EPS 12.50×22 倍≈275 美元（−0.6%）、中期以 3 年後 FY2030E 14.70×22 倍≈323 美元（+16.9%）計","upside_short_pct":-0.6,"upside_mid_pct":16.9},"trap_analysis":{"verdict":"🟡","label":"利潤率高峰風險（EPS 成長快於營收），不是生意衰退型陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"管理層 2026-10-28 預告 2027 毛利率回到歷史區間，記憶體新貨按市價採購；產業 DRAM 緊缺預期延續到 2027；Q4 2025 法說就為記憶體刻意建庫存","assumption":"費用槓桿與垂直整合能抵銷毛利率下滑，營業利益率守在 26% 以上","consequence":"若營業利益率回到 2022–2023 年的約 21%，EPS 停在 9–10 美元，倍數回到 15 倍，股價約 135–150 美元，五年後虧近 50%","ruling":"部分採納：放進 Bear 30% 與唯一致命點；反駁點是 2025 年毛利率 58.7% 時營業利益率已有 25.9%，要回到 21% 得營收停滯、費用率回升","watch":"季度毛利率與營業利益率；2027-02 FY2027 指引","evidence_refs":["supply_demand_durability#2","geo_supply_chain#2"],"fact_refs":["f_kpi5_fy2026","f_kpi2_gaap"]},{"view":"論點失敗","evidence":"10-K 承認對手已能複製部分功能、部分 OEM 客戶可能自製；Garmin 當年的車用導航就是被手機取代","assumption":"運動戶外專業功能（續航、GNSS、耐用）與 Connect 資料累積是手機生態補不齊的","consequence":"高階穿戴被 Apple／Samsung／Huawei 吃下，Fitness＋Outdoor（Q3 占營收 65%）成長歸零，倍數往消費硬體同業靠","ruling":"反駁：Omdia 2Q26 Garmin 份額 11%→15%、Apple 48%→46%，註冊量高於進貨，非 fēnix 產品的新用戶比重高；保留 R2 門檻監測","watch":"Omdia／Counterpoint 季度份額；Fitness 年增率","evidence_refs":["substitute_technology#2","competitive_share_entrants#0","substitute_technology#0","customer_second_source#0"],"fact_refs":["f_kpi0_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"2026 全年 FCF 指引由約 14 億下修到約 11 億美元（存貨與預付款），資本支出約 5 億，Q3 存貨 22.5 億；Mercedes domain controller 放量但車用 OEM 毛利率只有 16%","assumption":"存貨與預付是記憶體短缺期的一次性墊款，2027 後回收","consequence":"營收與 EPS 照基本情境成長，但 FCF÷淨利停在 0.5–0.6，股利成長放緩、每股自由現金流落後 EPS；成長組合偏向低毛利車用，拖累整體報酬率","ruling":"部分採納：把 FY2027 FCF÷淨利 <0.75 設為出場指標；反駁點是 2023–2025 年轉換率 0.82–0.92","watch":"FY2027 現金流量表；季度存貨÷營收","evidence_refs":["geo_supply_chain#2","customer_concentration_credit#1"],"fact_refs":["f_kpi3_fcf","f_kpi6"]},{"view":"價格已反映太多","evidence":"P/S 6.76 倍、EV/S 6.49 倍都在 4 個年度端點最高位，trailing P/E 26.6 倍在第 90 分位，26 週漲 17%；前份記載高毛利消費硬體同業中位 16.6 倍、利基複利 29.3 倍，倍數取決於市場把 Garmin 歸哪一類","assumption":"市場持續給 26 倍並接受 2026 的高峰利潤率","consequence":"即使基本情境（EPS 年增 8.5%）兌現，倍數回到 22 倍的五年報酬只有約 6%／年","ruling":"採納：這是本次唯一卡住的條件","watch":"股價相對 230 美元；FY2027 共識 EPS","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_pe_percentile","f_fwd_pe_latest","f_week26_return_pct"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 294.83 → 本次 276.75（-6.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=294.83","side_b":"本次 price_at_dd=276.75","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 294.83 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 294.83 美元：Bull 價 455、Bear 價 160，五年期望值 +12.9%，基準年化 3.5%，不對稱比 1.4","side_b":"本次情境、股價仍用 294.83 美元：Bull 價 481、Bear 價 166.5，五年期望值 +10.8%，基準年化 3.3%，不對稱比 1.21","ruling":"先換情境、股價不動：五年期望值少 2.1 個百分點，基準年化少 0.2 個百分點。不對稱比由 1.4 變為 1.21。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 294.83 美元：五年期望值 +10.8%，基準年化 3.3%，不對稱比 1.21","side_b":"本次情境、股價 276.75 美元：五年期望值 +18.0%，基準年化 4.7%，不對稱比 1.54","ruling":"再換股價、情境不動：起點價下跌 6.1%，五年期望值多 7.2 個百分點，基準年化多 1.3 個百分點，不對稱比由 1.21 升到 1.54。合計五年期望值比前份多 5.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：管理層前一季承諾的兌現度","cause":null,"prior_field":null,"side_a":"2026-07-29 CEO：Outdoor 下半年轉強、全年成長優於 2025；Auto OEM 下半年營收下滑並回到營業虧損；Fitness 是全年最大成長來源","side_b":"2026-10-28：Outdoor +20%（fēnix 9）、Auto OEM −20% 且虧損 1,200 萬美元、Fitness +16% 並重申全年最大貢獻，三項都照說的發生","ruling":"一致：管理層前一季的分部說法全數兌現，指引可信度加分，也代表 2027 毛利率回到歷史區間這句話要當真","evidence_level":"兩場法說逐字稿","settle_metric":"Q4 2026 分部營收","if_then":["若 Q4 2026 Outdoor 年增跌到個位數，表示 fēnix 9 換機潮比預期短，提前檢查 H1 門檻"],"evidence_refs":["end_markets#0"]},{"axis":"2027 毛利率：管理層預告回落 vs 2026 年每季都超出自己的指引","cause":null,"prior_field":null,"side_a":"2026-10-28 CEO／CFO：記憶體新貨按市價採購、Mercedes 放量帶來不利組合，2027 合併毛利率回到歷史區間（2022–2025 年 57.5%–58.7%）","side_b":"2026 年初（2026-02-18）毛利率指引 58.5%，2026-07-29 上修到 59.7%，2026-10-28 再上修到 61%；CEO 在 2026-07-29 說會用處理關稅的同一套做法應對記憶體，利潤率策略「不倒退」","ruling":"可調和、屬程度差異：毛利率會回落，不倒退指的是營業利益率；基本情境取 FY2027 毛利率約 58.5%、營業利益率約 27%，介於兩側之間","evidence_level":"管理層指引與歷史兌現紀錄","settle_metric":"2027-02 的 FY2027 毛利率與營業利益率指引","if_then":["若 FY2027 營業利益率指引 ≥27% 且 EPS 指引 ≥12.0 美元，基本情境改用 Bull 前兩年路徑重算，不必等到 230 美元","若 FY2027 EPS 指引 <10.80 美元，Bear 機率升到 40%，股價到 230 美元也不建首倉，等 2027Q1 實際毛利率"],"evidence_refs":["supply_demand_durability#2","geo_supply_chain#2"]},{"axis":"自由現金流指引下修","cause":null,"prior_field":null,"side_a":"2026-07-29 CFO：全年 FCF 約 14 億美元","side_b":"2026-10-28 CFO：全年 FCF 下修到約 11 億美元，因為現有存貨增加與記憶體預付款；資本支出約 5 億、Q3 存貨 22.5 億","ruling":"可調和：屬記憶體短缺期的保供給墊款，CFO 說預付款是逐家個案談；管理層沒給回收時點，標「未證、監測」，FY2027 FCF÷淨利仍 <0.75 就視為結構性","evidence_level":"兩場法說 CFO 發言","settle_metric":"FY2027 FCF÷淨利","if_then":["若 FY2027 FCF÷淨利 <0.75，H3 判削弱、Bear 機率升到 35%"],"evidence_refs":["geo_supply_chain#2"]},{"axis":"現在就買 vs 等價格（唯一卡住的條件是價格）","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：①2026 年指引連續上修，年初毛利率指引 58.5% 最後做到約 61%，「回到歷史區間」可能又是保守說法；②在下滑的穿戴市場拿份額，泰國廠 2027Q1 解除產能上限；③淨現金約 21 億美元、殖利率 1.4%，股價較前份回落 6%，FY2027 共識只要 24.4 倍","side_b":"等待的理由：基本情境（EPS 年增約 8.5%、終端 22 倍）五年年報酬約 6%，要 10% 需倍數維持 26 倍或 EPS 年增約 12.5%；FY2027 的分母正是爭點，2027-02 指引前沒有可裁決的數據","ruling":"維持等待；卡住的是價格相對正常化後的獲利，不是生意本身。自我攻擊三點（保守指引、份額擴大、淨現金下檔保護）都不改變基本情境報酬低於 8% 的事實","evidence_level":"事實表估值與共識、兩場法說","settle_metric":"股價相對 230 美元；FY2027 EPS 指引","if_then":["若股價跌到 230 美元以下而 FY2027 指引未讓 EPS 年減，屬跌但基本面無損，重跑完整 DD 後首倉 2%，不當停損訊號","若股價先漲到 320 美元以上而 FY2027 指引尚未公布，不追","反向條件：若 FY2027 營業利益率指引 ≥27% 且 EPS 指引 ≥12.0 美元，以新分母重算後首倉 2%"],"evidence_refs":[]},{"axis":"估值與機率（股價 294.83→276.75）","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-07-30：股價 294.83，FY2026 共識 EPS 10.13，Fwd P/E 約 29.1 倍，估值判極貴；Bull 25%／Bear 30%；裁決觀望","side_b":"本次：股價 276.75（−6.1%），FY2026 共識上修到 10.49（三個月 +3.55%），Fwd P/E 26.4 倍、FY2027 共識 24.4 倍，估值降一級為偏貴；機率維持 25／45／30；裁決與角色依本次均線與估值輸入重算","ruling":"估值改善約三分之二來自股價回落、三分之一來自 EPS 上修；機率不動，因為 2027 毛利率正常化的新證據抵銷了份額上升的好消息","evidence_level":"事實表價格與共識快照","settle_metric":"Fwd P/E（FY2027 共識）","if_then":["若股價回到 300 美元以上而 FY2027 共識未上修，估值回到極貴一級，不追"],"evidence_refs":[]},{"axis":"護城河方向（穩定→擴大）","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份判穩定：擔心 Apple／Samsung 用軟體更新把健康功能推給存量機、Whoop／Oura 占住恢復力品類、高階穿戴單價下滑","side_b":"本次判擴大：Omdia 2Q26 Garmin 份額 11%→15%、Apple 48%→46%；Counterpoint 出貨 +11%；Q3 Fitness +16%、Outdoor +20%，主要分部毛利率扣除關稅退款仍擴張","ruling":"改判擴大，只限執行面，定價權仍判持平。反例保留：fēnix 9 換機潮屬產品週期，若 2027 下半年 Fitness＋Outdoor 年增連 2 季跌破 5%，改回穩定","evidence_level":"兩家第三方出貨統計＋公司分部數據","settle_metric":"Omdia 季度份額；Fitness＋Outdoor 年增率","if_then":["若 Omdia 份額跌破 12%，護城河方向改回穩定，R2 時鐘改為 ⚡"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#0","competitive_share_entrants#0"]},{"axis":"價值陷阱風險（低→中）","cause":"新證據","prior_field":["trap"],"side_a":"前份判低：衰退信號未亮","side_b":"本次判中：2022→2025 EPS 年複合 19.4% 高於營收 14.2% 達 5.2pp（利潤率帶動），管理層 2026-10-28 預告 2027 毛利率回到歷史區間；2026E FCF÷淨利約 0.53","ruling":"升到中：不是生意在衰退，而是近年 EPS 成長有一塊來自不會重複的利潤率擴張與關稅退款","evidence_level":"事實表年度財報＋法說","settle_metric":"FY2027 營業利益率；FY2027 FCF÷淨利","if_then":["若 FY2027 FCF÷淨利仍 <0.75，衰退信號亮第二項，維持中並把 Bear 機率升到 35%"],"evidence_refs":["geo_supply_chain#2"]},{"axis":"重新評估條件改寫（重跑完整 DD／首倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"價格回落至 fwd PE ≤25x（FY27 自建 EPS $11.05 → 約 $276）且 2027-02 給出的 FY27 毛利率指引 ≥59.0%；兩條同時成立才重跑完整 DD","side_b":"股價≤230美元（約FY2027共識EPS 20.3倍）即重跑完整DD；或2027-02 FY2027 pro forma EPS指引≥12.0美元時以新分母重算","ruling":"價格腿已到（276.75 約 FY2027 共識 24.4 倍），但毛利率 ≥59.0% 在管理層預告 2027 回到歷史區間（57.5%–58.7%）後幾乎注定不成立，且決定 EPS 的是營業利益率不是毛利率；改成單一價格條件（對應基本情境 10% 年報酬），另開 EPS 指引的替代路徑，重跑通過後首倉 2%","evidence_level":"法說指引＋情境樹","settle_metric":"股價；FY2027 EPS 指引","if_then":["若兩條都未觸發，2027-02 指引公布後仍重跑一次完整 DD"],"evidence_refs":["geo_supply_chain#2"]},{"axis":"Single Thing 新設","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"FY2027 實際 pro forma EPS 低於 FY2026 的約 10.80 美元（EPS 年減）；2027-02 指引若已低於此數先行預警","ruling":"設立理由：2026-10-28 管理層首次明說 2027 毛利率回到歷史區間，FY2027 利潤率成為五年路徑裡最大的單一敏感項（營業利益率每 100bp 約 0.4 美元 EPS）","evidence_level":"法說指引","settle_metric":"FY2027 pro forma EPS","if_then":["若發生，Bear 機率升到 40%、暫停進場；若已持有則減碼一半"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"減碼／清倉指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（null）","side_b":"FY2027 營業利益率 <26%；Fitness＋Outdoor 合計年增連 2 季 <5%；Omdia 份額 <12%；FY2027 FCF÷淨利 <0.75","ruling":"前份只有進場條件、沒有持有後的出場指標，本次補上；若已持有，第一條觸發減碼一半，第一條加第二條同時觸發清倉","evidence_level":"方法補齊","settle_metric":"四項指標各自的資料來源","if_then":["若任兩項同時觸發，清倉並重跑完整 DD"],"evidence_refs":[]},{"axis":"記憶體風險門檻由毛利率年比轉負改為年減超過 300bp","cause":"新證據","prior_field":null,"side_a":"前份 R1：記憶體成本全年攤入＋無關稅退款→毛利率年比轉負","side_b":"本次 R1：季度毛利率年減 >300bp（扣除關稅退款）連 2 季，或 FY2027 毛利率指引 <57.5%","ruling":"管理層已預告 2027 毛利率回到歷史區間，年比轉負已是基本情境的一部分，不再是風險訊號；門檻移到基本情境之外（58.5% 再低 1pp）。觸發時 Bear 機率升到 35%、價格門檻下修到 210 美元；若已持有則減碼三分之一","evidence_level":"法說指引","settle_metric":"季度毛利率；FY2027 毛利率指引","if_then":["若 FY2027 毛利率指引 <57.5%，價格門檻改為 210 美元"],"evidence_refs":["supply_demand_durability#2","geo_supply_chain#1"]},{"axis":"最大回撤由單點改範圍","cause":"方法變動","prior_field":["max_dd_pct"],"side_a":"前份最大回撤 −55%（單點）","side_b":"本次 −55%～−35%：下緣用 Bear 第二年 EPS 9.70×13.5 倍≈131 美元，上緣用 EPS 不跌但倍數回到約 17 倍≈180 美元","ruling":"下緣不變，改成範圍並寫明推導；事實表未涵蓋歷史最大回撤","evidence_level":"情境樹推估","settle_metric":"實際回撤","if_then":["若股價跌破 180 美元而基本面指標都未觸發，屬深回撤心理準備範圍，重跑 DD 評估分批買進"],"evidence_refs":[]},{"axis":"其餘基本面結論複核後維持","cause":"新證據","prior_field":["signal","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、成長跑道中等、品質複利成長、不判循環位置","side_b":"本次維持：品質（淨現金、營業利益率 29%）與動能（RSI 45、未過熱）未改變綜合訊號；份額上升但滲透率仍無資料，跑道維持中等；營收四年年複合約 14% 且淨現金，仍屬品質複利成長；記憶體成本循環影響毛利但不改變公司類型","ruling":"維持；若 FY2027 EPS 年減，要重新檢查是否該按循環股處理","evidence_level":"事實表＋法說","settle_metric":"FY2027 EPS 與營收成長","if_then":["若 FY2027 EPS 年減且營收成長低於 5%，公司類型改按循環股重審"],"evidence_refs":[]},{"axis":"前份 Outdoor 結構性衰退風險退休","cause":"新證據","prior_field":null,"side_a":"前份：Outdoor（最高毛利段）結構性衰退擴散，2026Q1 −5%、Q2 −2%，近四季三負，下半年改善承諾與上半年算術難相容","side_b":"2026-10-28：Outdoor +20% 至 5.97 億美元，fēnix 9 帶動，毛利率 68%、營業利益率 39%；2026-07-29 承諾的下半年轉強已兌現","ruling":"退休：前份把產品週期低谷看成結構衰退。換機潮退去的風險保留：fēnix 首波需求以舊用戶跨代換機為主，改由 Fitness＋Outdoor 合計成長門檻（H1）追蹤","evidence_level":"公司分部數據","settle_metric":"Fitness＋Outdoor 合計營收年增率","if_then":["若 2027 下半年 Outdoor 年增連 2 季為負，重新開立 Outdoor 結構性風險"],"evidence_refs":["end_markets#0"]}],"triggers":[{"n":1,"text":"股價跌到 230 美元以下（約 FY2027 共識 EPS 20.3 倍），對應基本情境約 10% 年報酬","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"≤230 美元","action":"重跑完整 DD，通過後首倉 2%","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"FY2027 實際 pro forma EPS 低於 FY2026（約 10.80 美元）；2027-02 指引若已低於此數先行預警","type":"Single Thing","maps_to":"H2","metric":"FY2027 pro forma EPS（指引與實際）","threshold":"<10.80 美元","action":"Bear 機率升到 40%，暫停進場；已持有則減碼一半","source_freq":"2 月年度指引、季度財報","date":"2027-02","evidence_refs":["supply_demand_durability#2"]},{"n":3,"text":"高階穿戴份額與成長的假設檢驗","type":"假設驗證","maps_to":"H1","metric":"Fitness＋Outdoor 合計 TTM 營收相對 10% 年增路徑的偏離","threshold":"低於路徑 5% 以上連 2 季＝削弱；10% 以上連 3 季＝反轉","action":"削弱：護城河方向改回穩定；反轉：Bear 機率升到 40%","source_freq":"季度 8-K","date":null,"evidence_refs":[]},{"n":4,"text":"記憶體與零組件成本吃進毛利率","type":"風險","maps_to":"R1","metric":"季度合併毛利率年變化（扣除關稅退款）","threshold":"年減 >300bp 連 2 季，或 FY2027 毛利率指引 <57.5%","action":"Bear 機率升到 35%，價格門檻下修到 210 美元","source_freq":"季度 8-K","date":null,"evidence_refs":["supply_demand_durability#2","geo_supply_chain#1","geo_supply_chain#2"]},{"n":5,"text":"穿戴份額回落","type":"風險","maps_to":"R2","metric":"Omdia 智慧手錶出貨份額","threshold":"<12%（2Q26 為 15%）","action":"護城河方向改回穩定，Bear 機率升到 35%","source_freq":"Omdia 季度新聞稿","date":null,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","customer_second_source#0"]},{"n":6,"text":"成長的資本需求未回落","type":"假設驗證","maps_to":"H3","metric":"FCF÷淨利","threshold":"FY2027 <0.75","action":"衰退信號亮第二項，維持價值陷阱風險中並把 Bear 機率升到 35%","source_freq":"年報","date":"2028-02","evidence_refs":[]},{"n":7,"text":"關稅或台灣集中造成的毛利侵蝕（吸收失敗的判準）","type":"風險","maps_to":"R3","metric":"任一分部毛利率中歸因於關稅的年減幅；泰國廠投產時點","threshold":"≥200bp 連 2 季；或投產延後到 2027Q2 以後","action":"Bear 機率升到 35%","source_freq":"季度 10-Q／法說","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":8,"text":"波蘭競爭機關對 Garmin Polska 與經銷商價格協議的調查結果","type":"風險","maps_to":"R5","metric":"UOKiK 裁罰或命令","threshold":"公告裁罰（受影響營收事實表未涵蓋）","action":"金額低於全年營業利益 1% 只記錄；若擴及其他歐盟國家的經銷協議，重跑完整 DD","source_freq":"UOKiK 公告；10-K 法律程序","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":9,"text":"存貨與通路促銷壓力","type":"風險","maps_to":"R4","metric":"存貨÷當季營收","threshold":">1.3 連 2 季（Q3 2026 為 1.13）","action":"Bear 機率升到 35%","source_freq":"季度 10-Q","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":10,"text":"Q4 2026 財報與 FY2027 全年指引","type":"複審日期","maps_to":"H2","metric":"FY2027 營收、毛利率、營業利益率、EPS 指引","threshold":"營業利益率 ≥27% 且 EPS ≥12.0 美元＝替代進場路徑；EPS <10.80 美元＝唯一致命點預警","action":"重跑完整 DD","source_freq":"年度","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"FY2027 營業利益率（2027-02 指引與全年實際）","bear_threshold":"<26%（FY2025 為 25.9%）","window":"2027-02 指引；FY2027 全年","source":"Garmin 8-K 新聞稿與法說","last_status":"unknown"},{"metric":"Fitness＋Outdoor 合計營收年增率","bear_threshold":"連 2 季 <5%","window":"季度，2027Q1 起","source":"Garmin 8-K 分部營收","last_status":"ok"},{"metric":"Omdia 智慧手錶出貨份額","bear_threshold":"<12%（2Q26 為 15%）","window":"季度","source":"Omdia 季度新聞稿","last_status":"ok"},{"metric":"FCF÷淨利","bear_threshold":"FY2027 <0.75（連第二年）","window":"FY2027 年報","source":"Garmin 10-K 現金流量表","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=現價隱含 2026 的高峰利潤率延續且倍數不降；管理層已預告 2027 毛利率回到歷史區間，正常化後 EPS 年增約 8.5%，配 22 倍終端倍數只有約 6% 年報酬"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=16.95, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價≤230美元（約FY2027共識EPS 20.3倍）即重跑完整DD；或2027-02 FY2027 pro forma EPS指引≥12.0美元時以新分母重算","exec_line":"現價不追。股價≤230 美元且 FY2027 指引未讓 EPS 年減 → 重跑完整 DD，通過後首倉 2%，2027Q1 實際營業利益率 ≥26% 再補到 4%；FY2027 EPS 指引 <10.80 美元則暫停所有進場"},"reasoning":{"industry":"Q3 2026 營收 19.86 億美元（+12%），GAAP 營業利益 6.12 億、營業利益率 30.8%，毛利率 63.3%（含 3,300 萬美元關稅退款）。分部：Fitness 6.94 億（+16%，毛利率 63%／營業利益率 33%）、Outdoor 5.97 億（+20%，68%／39%）、Marine 3.10 億（+16%，64%／30%）、Aviation 2.53 億（+5%，78%／26%）、Auto OEM 1.32 億（−20%，毛利率 16%、營業虧損 1,200 萬）。Fitness＋Outdoor 占營收 65%、營業利益約 76%。全年指引：營收約 81.5 億、毛利率 61%、營業利益率 29%、pro forma EPS 約 10.80 美元。客戶不集中：前十大占 20%–25%，無單一客戶超過 10%；直營超過 10%，訂閱與服務仍低於 10%。單點依賴在供給端：消費產品主要在台灣自有工廠製造，記憶體等部分零組件為單一來源，管理層稱產能已到上限，泰國廠 2027Q1 才投產。產業時鐘判 II 擴張：註冊量高於進貨、零售商 Q4 拉貨強，Fitness、Outdoor、Marine 雙位數成長，但 Marine 終端市場偏軟（油價高、買家觀望）。供需持久性：健康與運動穿戴需求屬結構性持久，記憶體成本屬週期性、預期延續到 2027 後可反轉。產業態勢判雙向拉鋸：Garmin 份額上升（Omdia 11%→15%），但對手在補功能、部分 OEM 客戶可能自製，另有關稅與台灣集中兩個結構變數。","moat":"機制：垂直整合（自有台灣工廠，記憶體短缺期靠安全庫存與預付款保供給，靠全公司規模取得航空用的 PCB 與線材）＋運動戶外專業功能與 Connect 資料累積讓用戶換機留在 Garmin（fēnix 首波需求以跨代換機的舊用戶為主）＋航空認證與改裝存量（G1000 King Air 改裝破 1,000 套、Autoland 2,500 架）＋船用經銷商口碑（NMEA 連 12 年年度製造商）。方向：執行面擴大——Omdia 2Q26 Garmin 份額 11%→15%、Apple 48%→46%，Counterpoint 出貨 +11%；Q3 法說中分析師與管理層都指出 Aviation、Marine（扣除退款）、Outdoor、Fitness 毛利率年增。定價權持平——CEO 把漲價列為抵銷記憶體成本的工具之一但不承諾，毛利擴張主要來自組合、規模與台幣走弱。同業（TTM）：營業利益率 28.8%，高於 LOGI 17.9%、TRMB 17.7%，低於 AAPL 33.2%；毛利率 61.1% 高於 AAPL 48.7%，研發密度 15.3% 也較高。事實表無同業 ROIC，以營業利益率代理；GRMN 自身營業利益率由 2022 年 21.2% 升到 TTM 28.8%，同業歷史值事實表未涵蓋，差距方向無法驗證。當期稅後營業利益率約 24%（28.8%×（1−16.5%）），投入資本周轉率事實表未涵蓋。反例：fēnix 9 屬產品週期，份額上升可能隨換機潮退去；兩家機構口徑差很大（15% 對 5.6%）。","growth":"成長以量為主：2025 年穿戴成長主要來自量而非價，2026Q1 CEO 稱出貨量帶動份額提升；再加上高階組合。併購（TrainingPeaks／TrainHeroic）不重大，回購可忽略。共識 EPS：FY2025A 8.59→FY2026E 10.49→FY2027E 11.35→FY2028E 12.74，三年年複合 14.0%（Koyfin 快照，EPS 家數事實表未涵蓋）；營收共識 FY2026 81.5 億、FY2027 91.4 億美元（6／8 位分析師）。內生上界約 12%，缺口約 2pp 歸因於利潤率擴張：FY2026 營業利益率由 25.9% 升到指引 29%，已在 FY2026 兌現；FY2026→FY2028 共識年複合 10.2%，落在上界內，不依賴倍數重估。跑道：以份額代理，Omdia 15%、Counterpoint 5.6%；新曲線有 CIRQA（無螢幕手環，擴大可及市場、需求超出預期）、Connect+（成長快於所在分部、免費期後續訂強）、Mercedes domain controller（2027 量產），但規模都還小，判中等。AI 取代風險低：產品長在自有感測器與硬體上，AI 用在 Connect+ 洞察屬強化；AI 資料中心需求推高記憶體價格是成本面的間接衝擊。衰退信號十項亮一項（2022→2025 EPS 年複合高於營收 5.2pp），FCF÷淨利 2026E 約 0.53 列警示。","governance":"FCF÷淨利：2023 年 0.92、2024 年 0.88、2025 年 0.82；2026 全年 FCF 指引由約 14 億（2026-07-29 CFO）下修到約 11 億美元（2026-10-28 CFO），以 pro forma EPS 10.80×192.7 百萬股≈淨利 20.8 億估算，轉換率約 0.53，原因是存貨（Q3 22.5 億）與記憶體預付款，加上資本支出約 5 億（含泰國廠）。SBC：Q3 4,470 萬美元，占營業利益 7.3%、約占營收 2.3%。現金去向：股利每季約 2.02 億（年 4.20 美元／股，殖利率 1.4%）；Q3 回購 4,100 萬，授權剩 4.07 億到 2028 年 12 月；流通股由 2026-05-22 的 192.82 百萬股到判斷日 192.7 百萬股，持平。淨現金約 21.1 億美元（不含長期有價證券；法說稱現金與有價證券約 41 億）。回購以約 26 倍 Fwd P/E 進行，買入收益率約 3.8%。","valuation":"現價要求什麼：股價 276.75，Fwd P/E 26.4 倍（FY2026 共識 10.49）、24.4 倍（FY2027 共識 11.35）。扣掉約 1.5% 的股息與淨回購，10% 年報酬要五年後股價約 416 美元：倍數 22 倍需 FY2031 EPS 約 18.9（年增約 12.5%），倍數 26 倍需約 16.0（年增約 9%）。基本情境 EPS 年增約 8.5%、終端 22 倍，五年年報酬約 6%（EPS 複利 8.5%、倍數 −3.6%／年、股息與回購 1.5%），我不信現價隱含的組合。分母爭點：FY2026 EPS 含約 5,400 萬美元關稅退款（Q2 2,100 萬＋Q3 3,300 萬）、低價記憶體庫存與台幣走弱的好處，改以 FY2027 共識為主錨。歷史位置：trailing P/E 26.6 倍落在 4 個年度端點第 90 分位，P/S 6.76 倍、EV/S 6.49 倍都在第 100 分位。賣方目標價平均約 284–310 美元（多數早於 Q3 財報、口徑不一），現價低約 3%–11%，最高 370、最低平均 213（4 家、疑為舊資料），全距約 1.7 倍，對等待沒有構成反證。動能：RSI 45、26 週 +17%，未過熱。","premortem":"可能看錯的兩個方向。太悲觀：2026 年指引連續上修（EPS 由 10.0 到 10.80，毛利率由年初 58.5% 到 61%），2027 的「回到歷史區間」可能又是保守說法；份額上升代表執行面在擴大。太樂觀：記憶體短缺若延續到 2028，加上 Mercedes 低毛利放量，營業利益率可能跌破 26%。最大回撤 −55%～−35%：事實表未涵蓋歷史最大回撤，下緣用 Bear 第二年 EPS 9.70×13.5 倍≈131 美元（−53%），上緣用 EPS 10.49 不跌但倍數回到約 17.2 倍≈180 美元（−35%）。壓力測試五項過三項：①淨現金約 21 億、總債務 2.2 億，營收急跌也無再融資壓力——過；②年股利約 8.1 億對 2026E FCF 約 11 億，覆蓋 1.36 倍——過；③毛利率回到 2023 年 57.5%、費用率維持 32%，以 FY2027 共識營收 91.4 億、稅率 16.5% 推得 EPS 約 10.1（不計利息收入），仍高於 2025 年 8.59——過；④倍數回到前份記載消費硬體同業 16.6 倍，10.49×16.6≈174 美元，跌 37% 超過 30%——不過；⑤主要製造集中台灣，泰國廠 2027Q1 才投產——不過。價值陷阱判中，依據見反證紀錄中論點失敗與股東經濟變差的條目。"},"plain":{"six":{"how_it_makes_money":"賺的是運動、戶外、航空、船用玩家願意為專業功能多付的錢；利潤卡在自有工廠的垂直整合與高階產品組合，Fitness＋Outdoor 貢獻約四分之三營業利益，車用 OEM 是唯一虧損段","moat":"護城河方向判擴大（執行面）：兩家機構的出貨統計都顯示 Garmin 在下滑的穿戴市場拿份額，主要分部毛利率扣除關稅退款仍擴張；定價權判持平。評分執行 9、定價 7","growth":"成長跑道判中等：份額還在擴大，CIRQA 與 Connect+ 開出新客群，但滲透率事實表未涵蓋，第二條曲線規模仍小（訂閱與服務低於營收 10%）","capital":"資本配置穩健但不積極：現金主要用在股利與為記憶體短缺墊高存貨，回購規模小且價位偏貴，股數持平；2026 年 FCF 轉換率跌到約 0.53 是要盯的點","valuation":"現價約 26 倍 FY2026、24 倍 FY2027 共識，要倍數維持 26 倍、EPS 年增約 9%，或倍數回到 22 倍、EPS 年增約 12.5%，才有 10% 年報酬；我的基本情境是 EPS 年增約 8.5%、終端 22 倍，年報酬約 6%，判偏貴","how_wrong":"最可能看錯的是 FY2027 利潤率：管理層若又一次保守，基本情境偏悲觀；若記憶體短缺拖到 2028，Bear 30% 還不夠"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"現價隱含 2026 的高峰利潤率延續且倍數不降；管理層已預告 2027 毛利率回到歷史區間，正常化後 EPS 年增約 8.5%，配 22 倍終端倍數只有約 6% 年報酬","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤230 美元，或 2027-02 FY2027 pro forma EPS 指引 ≥12.0 美元","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":276.75,"week26_return_pct":16.95,"consensus_rev_3m_pct":3.55,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026 EPS 含約 5,400 萬美元關稅退款（Q2 2,100 萬＋Q3 3,300 萬）、低價記憶體安全庫存與台幣走弱的好處，管理層已說 2027 毛利率回到歷史區間；便宜與否改看 FY2027 共識 11.35 美元（24.4 倍）"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 全年指引","impact":"高","watch":"營業利益率指引是否 ≥27%、pro forma EPS 指引是否 ≥10.80 美元"},{"date":"2027-03","date_precision":"quarter","type":"capacity","event":"泰國新廠開始量產（管理層稱 2027Q1）","impact":"中","watch":"是否如期投產、投產初期對毛利率的拖累"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"Mercedes-Benz 新一代 domain controller 量產（管理層稱 2027 年偏上半年）","impact":"中","watch":"車用 OEM 營收回到成長，以及低毛利組合對合併毛利率的稀釋"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"Omdia／Counterpoint 3Q26 智慧手錶出貨統計","impact":"低","watch":"Garmin 份額是否守住 2Q26 的 15%（Omdia）"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,447B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRMN_20261103/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河執行面擴大，定價權持平，綜合評為 B 級向上。</p>
<!-- E5 -->
<h3>§5.F 對手財務深度對照</h3>
<!-- E6 -->
<h3>§5.R 報酬持續期檢核</h3>
<!-- E7 -->
<ul class="pts">
<li>護城河來自四件事。第一是自有台灣工廠的垂直整合，記憶體短缺期靠安全庫存與預付款保供給。第二是運動戶外專業功能與 Connect 資料累積，讓用戶換機時留在 Garmin。第三是航空認證與改裝存量，G1000 King Air 改裝破 1,000 套，Autoland 裝機 2,500 架。第四是船用經銷商口碑，NMEA 連 12 年選為年度製造商。</li>
<li>方向判擴大，只限執行面。Omdia 2Q26 Garmin 份額從 11% 升到 15%，Apple 從 48% 降到 46%，Counterpoint 出貨年增 11%。Q3 法說中分析師與管理層都指出 Aviation、Marine 扣除退款、Outdoor、Fitness 毛利率年增。執行評 9 分，定價評 7 分，綜合 8.0。</li>
<li>定價權持平。CEO 把漲價列為抵銷記憶體成本的工具之一，但不承諾。毛利擴張主要來自組合、規模與台幣走弱，不是單純提價。漲價後的流失率事實表沒有涵蓋，所以定價分數不往上給。</li>
<li>跟同業比，GRMN 毛利率 61.1%，高於 AAPL 的 48.7% 與 LOGI 的 45.5%，低於 TRMB 的 69.8%。營業利益率 28.8%，高於 LOGI 的 17.9% 與 TRMB 的 17.7%，低於 AAPL 的 33.2%。研發密度 15.3%，高於 AAPL 與 LOGI。比一般消費周邊高出約 11 個百分點，說明它不是被當成普通硬體在賣。</li>
<li>同業 ROIC 與歷史利潤率事實表沒有，所以用營業利益率代理。GRMN 營業利益率從 2022 年的 21.2% 升到近四季 28.8%，但同業歷史值缺少，差距擴大或縮小無法驗證。當期稅後營業利益率約 24%，投入資本周轉率列為缺口。</li>
<li>威脅有三項，機率都不高。Apple、Samsung、Huawei 補齊運動健康功能，機率 30%。OEM 客戶自製向 Garmin 採購的零組件，機率 20%。大型零售客戶要求促銷壓毛利，機率 25%。目前份額數據顯示都還沒有造成損害。</li>
<li>反例要保留。fēnix 9 屬產品週期，首波買家多為跨代換機的舊用戶，份額上升可能隨換機潮退去。若 2027 年下半年 Fitness 加 Outdoor 年增連 2 季跌破 5%，或 Omdia 份額跌破 12%，護城河方向改回穩定。</li>
</ul></section>

```