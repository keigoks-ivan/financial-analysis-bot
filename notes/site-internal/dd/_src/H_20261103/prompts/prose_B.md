你是 stock-analyst v20 的**散文層（prose）agent**，標的 H（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：H　日期：2026-11-03　archetype：None　前份裁決：2026-05-20　B（觀望偏進場；品質 A + asset-light 90% + 66M loyalty +18% + Pipeline 151K 新高，但 Fwd PE 34.8x 已 priced in 完整復甦，5Y PEG 2.05 接近警示；建議等 Fwd PE&lt;28x 或股價回測 W52 $151）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2030B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（667B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（809B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1586B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1402B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（672B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1472B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2179B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3625B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2695B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2030           3479-4970      5 條（2–6 內）  
s3                  8000         667           5133-7333      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3797          7842-11203      5 條（2–6 內）  
s6                 11000         672          7230-10328      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1472           1420-2028      3 條（2–6 內）  
s10                 5000        2179           1975-2821      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2695           2000-2305      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5397B；至少需散文≈39.60KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−60
−49%
−45%
−45
−3%
−2.5%
−2%
−1.2%
−0.55
0
0.3%
0.32%
0.32
0.36
0.5%
0.55
0.58
0.6%
0.63%
0.75
0.82%
1
1%
1.04
1.2%
1.3%
1.35
1.4
1.45
1.47
1.5
1.59
1.6
1.62
1.7
1.8
1.87
1.9
2%
02
2.0%
2
2.1%
2.2%
2.4%
2.74
2.8
2.95
03
3
3%
3.04
3.25
3.27
3.3
3.36
3.4%
3.5
3.75
3.81
3.9%
3.9
4%
04
4
4.05
4.1%
4.25
4.3%
4.4
4.7%
4.75
4.8%
4.8
4.85
4.9%
4.90
4.9
4.95
5
5%
05
5.5%
5.75
5.8
6
06
6%
6.05
6.09
6.3
6.35%
6.65
7
07
7%
7.1%
7.2%
7.21%
7.5%
7.55
7.6
8%
8
8.1%
8.6
8.9
9%
9
9.46
10%
10
10.3
10.4
11
11%
11.6%
11.64%
11.7
11.85
12%
12.0
12
12.4%
12.65
13%
13.2
13.35
14%
14
14.3%
14.49%
14.5%
15
15.2%
15.7%
15.73%
15.8
16%
16
16.1
17%
17
17.43
18
18%
18.28
18.3
19%
19.5%
19.6%
19.7%
20
20%
20.1%
21
23%
23.6
24.0%
24
24.01%
25%
25
25.5%
25.52%
26
26%
26.4%
27%
27
28
28.4%
28.6%
29
30
30%
30.6%
30.9
31
32
33%
35%
36.38%
36.4%
38%
38
38.3
38.35
40%
40
41.5
41.53
45
46.48
48
49
49%
49.3
49.31
50%
50
52
53%
58.9
60%
65%
70%
70
71.0
71.4
77.2
88%
90
90%
95
95%
97.9
98
100%
100
104
150
150%
$151
154.5
155
159
164.4
168.6
175
187.89
188
195
198
217
221
230
232
332.8
400
2006
2019
2022
2023
2024
2025
2026
2027
2028
2030
2031
20261103
2,500
3,000
4,000
4,500
6,000
7,200
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
{"meta":{"ticker":"H","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Hyatt Hotels Corporation"},"oneliner":"Hyatt 的費用引擎與開發 pipeline 都在加速，但股價半年漲 18%，FY2027 共識 38 倍已先反映 25% 以上的盈餘成長。論點完整，價格沒有留安全邊際，等 155 美元以下再談建倉。","thesis":{"H":[{"id":"H1","text":"費用引擎維持雙位數成長：2026 年 gross fees 年增 10%～11% 落地，2027 年再年增至少 9%（投資人日 2025–2028 年複合 9%～13% 的下緣）。","2y":"FY2026 gross fees 達 13.2～13.35 億美元；FY2027 年增 ≥9%","5y":null,"10y":null,"threshold":"FY2027 gross fees 年增 <9%，或單季年增連 2 季 <5%","source":"季報新聞稿的 gross fees；2027-02 第四季法說的 2027 指引；2026-05-28 投資人日 CFO 的三年複合指引","drift_rule":"TTM gross fees 對指引路徑連 2 季偏離 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"},{"id":"H2","text":"開發飛輪延續：2026–2028 年淨增房數年複合 6%～8%，pipeline 持續創新高；中高價位新品牌開進新市場，但不稀釋整體每房費用。","2y":null,"5y":"2028 年底淨增房數三年複合 ≥6%；pipeline ≥17 萬間；管理層仍揭露 pipeline 每房費用高於在營飯店","10y":null,"threshold":"年度淨增房數 <5%，或 pipeline 年增轉負","source":"季報的淨增房數與 pipeline；2026-10-29 第三季法說 CEO 對 2027 Q1 淨增房數 6%～7% 的展望","drift_rule":"TTM 淨增房數對 6% 目標連 4 季偏離 ≥5% 為削弱，連 6 季偏離 ≥10% 為反轉"},{"id":"H3","text":"會員與直銷守住訂房入口：World of Hyatt 會員年增 ≥10%，直銷房晚占比維持約七成；代理式 AI 成為接在 Hyatt 自有預訂上的新入口，而不是抽成的中介。","2y":null,"5y":null,"10y":"2030 年後會員年增仍 ≥10%；直銷房晚占比 ≥65%；AI 平台來源的訂房主要在 Hyatt 自有通路完成","threshold":"會員年增 <10%，或直銷房晚占比 <65%","source":"季報會員數（Q3 2026 約 7,200 萬、年增 19%）；投資人日與 10-K 的直銷占比（2026-05-28 CEO：約 70%）；法說對 AI 訂房占比的揭露","drift_rule":"跨 2 個年度低於門檻為削弱，跨 3 個年度為反轉"}],"R":[{"id":"R1","text":"旅宿景氣反轉：2026 年的世足、猶太節日時點與中東基期等一次性助力退場後，需求成長本來就低於歷史（前 50 大市場 1.3%，2006–2019 年均 2%），RevPAR 轉負。","h_ref":"H1","clock":"🔥","threshold":"系統可比 RevPAR 連 2 季年減，或任一季 ≤−3%","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"全包式與 Distribution 復甦落空：墨西哥坎昆的需求與航班運能、牙買加復開都延後，Distribution 營收與 EBITDA 連年下滑；出售 Playa 時投給買方的 2 億美元優先股，信用風險也連帶升高。","h_ref":"H1","clock":"⚡","threshold":"2027 Q1 net package RevPAR 年增 <0，或 2027 上半年 Distribution 調整後 EBITDA 仍低於 2025 同期","evidence_refs":["end_markets#1","channel_business_model_shift#2"]},{"id":"R3","text":"代理式 AI 與新分銷通路截走訂房入口：由 LLM 決定推薦哪家飯店，第三方 AI 技術的定價又不受 Hyatt 控制；結果是直銷占比下滑、分銷成本上升。","h_ref":"H3","clock":"🐢","threshold":"直銷房晚占比 <65%，或管理層揭露 AI 平台來源訂房 >5% 且需支付佣金","evidence_refs":["competitive_share_entrants#0","substitute_technology#0","substitute_technology#1","channel_business_model_shift#1"]},{"id":"R4","text":"地緣政治與貿易政策：中東衝突、墨西哥治安與關稅急變，壓抑國際旅遊並推高供應商成本。","h_ref":"H1","clock":"🔥","threshold":"中東加墨西哥的年度費用衝擊 >4,000 萬美元（2026 年約 3,000 萬）","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#2"]},{"id":"R5","text":"開幕延遲、轉換案卡關：2026 年過半開幕擠在第四季，2026-07-30 法說已坦承部分開幕會延到 2027，轉換案的 PIP 也比原先模型重。","h_ref":"H2","clock":"⚡","threshold":"FY2026 淨增房數 <5%，或 2027 上半年仍出現跨季延遲","evidence_refs":[]},{"id":"R6","text":"與 MAR、HLT 的規模差距擴大：同業整併、會員規模更大，報表營業利益率只有對方的一半左右（7.2% 對 15.7%、24.0%），在爭取業主與 key money 上處於劣勢。","h_ref":"H2","clock":"🐢","threshold":"調整後 EBITDA 利益率差距 >8pp 連 2 年（事實表只有報表營業利益率，標資料缺口）","evidence_refs":["competitive_share_entrants#1"]}],"single_thing":{"description":"2027～2028 年旅宿景氣轉入衰退，系統可比 RevPAR 出現單季年減 3% 以上","why_fatal":"費用直接按飯店營收與利潤抽成，而 EPS 下方的折舊與利息大致固定；RevPAR 由 +5% 轉為 −3%，會讓共識預期的 2027～2028 年約 25% EPS 成長轉為下滑。現價 49 倍的倍數同時失去成長支撐，盈餘與倍數雙殺，落到衰退情境（五年後約 95 美元）。","if_happens":"單季 ≤−3% 減碼至半倉；連 2 季為負則清倉並重跑研究；未持有者暫停建倉，直到 RevPAR 回正","how_monitor":"每季財報的系統與美國可比 RevPAR；第四季美國全服務飯店的團體 pace（目前中個位數成長）；企業協議價業務成長（Q3 約 +4.8%）","probability":"12～24 個月約 20%"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":38.35,"peg_fy2":1.45,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-0.55,"FY2026E":3.81,"FY2027E":4.9,"FY2028E":6.09},"fy_end_month":12,"eps_basis":"FY2026–2028 為 Koyfin 共識 EPS。TTM GAAP EPS 約 1.9 美元，與共識差距大，推定共識為調整後口徑，但事實表未載明。FY2025A 為 GAAP 稀釋 EPS −0.55 美元，受資產出售與一次性項目影響，口徑與共識不同，不作成長率基期；三年成長率以 FY2026→FY2028 計。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/H_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"輕資產費用模式疊加 RevPAR 週期槓桿"},"industry":{"clock_phase":"II","sd_verdict_source":"供需持久性：供給面屬結構性、偏持久。美國供給成長 2026 年約 1.2%、2027 年約 0.6%～1.3%，在建量為 12 年低點，在建專案年減 4.9%（CoStar、Lodging Econometrics）。需求面屬週期性：前 50 大市場 2026 年需求成長 1.3%，低於 2006–2019 年均 2%（Green Street）。RevPAR 靠房價推動，景氣反轉時會先反映在房價。","bargaining":{"up":"上游是業主與開發商。key money 需求升高，新建案融資仍緊（2026-05-28 CEO：資本形成仍是問題），議價力偏向業主。","down":"下游是住客與企業客戶，沒有單一重要客戶（10-K）。高端客群對房價容忍度高；OTA 與 AI 平台可能分走通路利潤。","geo":"2026 年兩個壓力區：墨西哥坎昆（坎昆需求年減逾 10%）與中東（國際入境年減 40%）。兩地合計使全年費用減約 3,000 萬美元（2026-10-29 CFO）。"},"profit_pool_dir":"高端與休閒市場的利潤池往品牌與會員規模大的業者集中；分銷段的利潤可能流向 AI 平台，方向未定。","tam_table":[{"item":"可拓展房數（管理層辨識）","value":"約 230 萬間（2026-05-28 投資人日 CEO）"},{"item":"開發 pipeline","value":"約 15.8 萬間，年增 12%（Q3 2026）"},{"item":"淨增房數目標","value":"2026–2028 年複合 6%～8%；Q3 2026 為 3.9%（不含 Playa）"},{"item":"美國產業供給成長","value":"2026 年約 1.2%，2027 年約 0.6%～1.3%（CoStar、Lodging Econometrics）"},{"item":"滲透率與利潤池占比","value":"事實表未涵蓋現有系統房數與產業營業利益池，無法計算滲透率，也無法對比五年前"}]},"moat":{"mechanism":"高端、生活風格與全包式品牌組合，加上 World of Hyatt 會員與直銷管道，讓業主拿到較高的 RevPAR 與房價指數；Hyatt 以此換取約 20 年期的管理與加盟合約及費用。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力擴大：年初至今市占 +100bp、房價指數上升（2026-10-29 CEO），坎昆全包式市占 +400bp（CFO），簽約量 +70%、動工 +40%，會員 7,200 萬、年增 19%。定價力穩定：房價貢獻約八成 RevPAR 成長，pipeline 每房費用高於在營飯店，但業主端 key money 競爭激烈。兩者合併為穩定。市占數據為公司自報，第三方報導稱沒有直接的市占與定價數據，故不標擴大。","peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，只能用報表營業利益率與 FCF 利益率比較。MAR 與 CHH 的 TTM 截至 2026-06-30，比 Hyatt 晚一季。","threats":[{"level":"🟡","text":"代理式 AI 與 LLM 平台成為新的分銷入口，可能降低 Hyatt 物業的曝光並抬高通路成本。目前經 LLM 完成的訂房「非常少」（2026-10-29 CEO），先列點對點威脅；直銷占比跌破 65% 時升級為生態攻擊。","p":30,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","channel_business_model_shift#1"]},{"level":"🟡","text":"自家 AI 部分依賴第三方授權技術，可得性與定價不受 Hyatt 控制，談判條件可能不利。","p":20,"evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"同業整併加上部分對手規模與會員數較大（10-K 自承），在爭取業主與 key money 上施壓，也可能使 Hyatt 失去份額。","p":25,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#0"]},{"level":"🟡","text":"Airbnb、Vrbo 等短租替代住宿，以及 Alibaba、Google、信用卡發行商這類新分銷參與者。","p":15,"evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"報表口徑為低利益率（營業利益率 7.2%），周轉率未知。費用收入約占營收 19%，以費用口徑推論屬高利益率×高周轉，但事實表沒有投入資本可以驗證。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"三種角色分開看：住客是使用者，企業差旅與會議主辦是決策者，付費者是住客與企業。Hyatt 的直接客戶是業主，業主要的是更高的 RevPAR 與融資可得性。業主需求強：2026 年初至今簽約 +70%、動工 +40%，pipeline 15.8 萬間創新高（Q3 2026 CEO）。終端住客需求屬可延後的消費，週期風險放在景氣假設處理。"},{"item":"決策層級","level":"🟡","text":"業主端的替換成本高：合約約 20 年，系統轉換「painful and arduous」（Q3 2026 CEO）。但新約與續約靠 key money 激烈競爭。住客端每趟都能換品牌，留存靠會員：會員 7,200 萬，年住 100 晚以上的會員自 2022 年增加近 40%。分析師引述會員滲透率約 49%～50%、同業 65%～70%；管理層質疑計算口徑，但沒有給同口徑數字（2026-05-28 投資人日）。"},{"item":"價值鏈分配","level":"🟡","text":"Hyatt 收費用，業主承擔不動產與營運風險，約七成房晚走 Hyatt 直銷（2026-05-28 CEO）。壓力來自兩端：業主要求更多 key money（每年 1.5～1.7 億美元），通路端的 AI 平台可能成為新的收費關卡（10-K 風險因子）。目前守住分配的證據是：高端組合每房費用較高，pipeline 每房費用高於在營飯店。"},{"item":"社會容忍度","level":"🟢","text":"飯店房價不受價格管制，旅客對高端房價上漲的容忍度高（房價貢獻約八成 RevPAR 成長）。加盟業務受 FTC 與各州加盟法規範，屬既有框架。Hyatt 被控透過 IDeaS 收益管理軟體交換價格資訊的私人反托拉斯集體訴訟，法院已先行駁回；但若演算法定價的監管收緊，收益管理工具會受影響。"}],"roiic":"代理值約 20%～35%（稅後）。2026 調整後 EBITDA 增量約 1.6 億美元（指引 11.7～12.0 億、年增 14%～17%，反推 2025 約 10.3 億），除以每年再投資約 3 億（key money 1.5～1.7 億＋資本支出 1.35～1.4 億），稅前約 53%；以稅率 27%～30% 換算，稅後約 38%。這個增量含 RevPAR 順風與 Playa 管理合約的貢獻，扣除後取 20%～35%。","reinvest_rate":"約 33%：每年再投資約 3 億 ÷（調整後 FCF 指引中值 6.05 億＋3 億）","endo_ceiling":10,"formula_note":"事實表沒有投入資本、折舊與營運資金，無法照（Capex−D&A＋ΔWC＋收購淨額）÷NOPAT 計算。改用 key money 加資本支出作為再投資，以調整後 FCF 加回再投資作為現金 NOPAT 的代理值。上界包含景氣順風，偏高。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","H":20.11,"MAR":19.81,"HLT":30.13,"CHH":50.59,"WH":null,"unit":"%"},{"metric":"營業利益率","H":7.21,"MAR":15.73,"HLT":24.01,"CHH":25.52,"WH":36.38,"unit":"%"},{"metric":"FCF 利潤率","H":6.35,"MAR":11.64,"HLT":14.49,"CHH":7.09,"WH":30.57,"unit":"%"}],"competitors":[{"name":"MAR","gm":19.81,"om":15.73,"fcf_margin":11.64,"strategy_note":"規模最大，營業利益率 15.7%、FCF 利益率 11.6%，都約是 Hyatt 的兩倍。Hyatt 靠高端組合與房價指數取勝，不靠規模。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"HLT","gm":30.13,"om":24.01,"fcf_margin":14.49,"strategy_note":"營業利益率 24.0%、FCF 利益率 14.5%，是輕資產模式的標竿。Hyatt 在 2028 年達成 95% 輕資產目標之前，利益率差距難以收斂。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CHH","gm":50.59,"om":25.52,"fcf_margin":7.09,"strategy_note":"以中低價位加盟為主，營業利益率 25.5%，但 FCF 利益率只有 7.1%。Hyatt 的中高價位 Essentials 品牌進入新市場時，會與它正面競爭。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"WH","gm":null,"om":36.38,"fcf_margin":30.57,"strategy_note":"純加盟、以經濟型為主，營業利益率 36.4%、FCF 利益率 30.6%。Hyatt 不做中低階與經濟型（2026-05-28 CEO），兩者直接重疊有限。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量（淨增房數 2026–2028 年複合 6%～8% 目標）加價（RevPAR，投資人日指引 2025–2028 年複合 2%～4%），帶動費用年增 9%～13%；回購每年約 2%；併購不在展望內（2026-05-28 CEO：展望百分之百是有機成長）。","runway_years":"≥10 年（管理層辨識約 230 萬間可拓展房數、pipeline 15.8 萬間；現有系統房數事實表未涵蓋，滲透率無法計算）","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段的再投資推導：增量報酬約 20%～35% × 再投資率約 33%，約 10%。事實表沒有投入資本，屬代理值。","segments":[{"item":"管理與加盟費用（gross fees）","value":"Q3 2026 為 3.27 億美元、年增 15.2%；FY2026 指引 13.2～13.35 億、年增 10%～11%"},{"item":"Distribution（全包式分銷與旅行社平台）","value":"2025 營收 9.46 億、年減 7.5%；2026 調整後 EBITDA 預期比 2025 少約 3,000 萬（Q3 法說 CFO）"},{"item":"自有與租賃","value":"Q3 調整後 EBITDA 還原資產出售後年減 1%；Grand Central 與數家物業仍在出售中"},{"item":"輕資產盈餘占比","value":"2026 年約 90%，2028 年底目標 95%（2026-05-28 投資人日 CFO）"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"年度毛利率 19.6%→19.5%→19.7%，TTM 20.1%；季度數據事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱年初至今市占 +100bp（公司自報）"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"Q3 房價貢獻約八成 RevPAR 成長，未見入住率下滑的證據"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY2027 共識 EPS +28.6%，共識營收 +8.1%，差 20pp；成因是 EBITDA 下方固定成本攤薄與回購"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2024 年為 0.36，但淨利含出售利得；2025 年淨利為負，比率失真，不構成連 2 年。改用調整後 FCF／EBITDA ≥50% 追蹤"},{"signal":"SBC／營收超過 5% 且逐年上升","lit":false,"note":"Q3 2026 為 0.63%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"尚未見到；代理式 AI 屬通路變動，列入風險監測"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數事實表未涵蓋，屬資料缺口；Hyatt 自身倍數在年度端點最高位"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"資本支出 1.35～1.4 億，對調整後 FCF 5.8～6.3 億，約 23%"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"pipeline 創新高；營收 2022–2025 由 58.9 億增至 71.0 億"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"2022 年以來回饋股東","value":"21 億美元，占現金運用逾九成（2026-05-28 投資人日 CFO）"},{"item":"2026 年初至 Q3 回饋","value":"約 3.36 億美元（回購加股息）；Q3 回購 1.47 億"},{"item":"2026 全年回饋指引","value":"3.75～4.25 億美元（Q2 時為 3.25～3.75 億）"},{"item":"剩餘回購授權","value":"約 14 億美元"},{"item":"淨負債與流動性","value":"淨負債約 41.5 億美元（含租賃口徑）；流動性約 18 億；承諾維持投資等級，2028 年底前可再增加 2～5 億負債"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Playa（2025 年收購，同年 12 月出售不動產、保留管理合約）與 Two Roads 的收購總價、收購後 EBITDA 拆分，事實表未涵蓋，無法驗證已實現報酬","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購均價事實表未涵蓋。以 26 週前約 159 美元到現價 188 美元、FY1 EPS 3.81 計算，買入盈餘殖利率約 2.0%～2.4%，自由現金流殖利率約 3.4%～4.1%。門檻是 10 年期殖利率加 2%；10 年期殖利率事實表未涵蓋，但以盈餘殖利率計，任何正常利率環境都不會通過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營收 0.63%（Q3 2026）。以 FY2026 共識營收 71.4 億計約 4,500 萬美元，約當股本每年稀釋 0.3% 以下，回購抵銷有餘","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY1、FY2 共識 EPS），以 EV/EBITDA 輔助","tier":"輕資產旅宿品牌（高端組合）","peers":{"expanded":false,"reason":"事實表的同業對照只有利益率，沒有收同業的前瞻本益比或 EV/EBITDA，無法做同層級倍數比較；終端倍數改以 Hyatt 自身 FY2028 隱含倍數與 EV/EBITDA 對照"},"fwd_pe":49.31,"peg":1.87,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 49 倍、FY2027 38 倍，自身年度端點分位 100，EV/EBITDA 約 18 倍；PEG 1.87 在合理區間上緣；賣方均價只有約 5% 上行；base 五年價格報酬每年約 4%。結論是偏貴但未到極端，因為 FY2028 的 31 倍對應約 25% 的盈餘成長，判 🟠。五年分位：事實表只有 3～4 個年度端點，不外推。","upside_short_pct":4.8,"upside_mid_pct":23.6},"trap_analysis":{"verdict":"🟡","label":"一項衰退信號亮燈（EPS 成長遠高於營收），成因是固定成本攤薄；陷阱風險低到中"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"前 50 大市場需求成長 1.3%，低於歷史 2%。2026 年 RevPAR 有世足、猶太節日時點與中東基期助力，管理層自己說不會重複。CoStar 預測美國 2027 RevPAR 只有 +2.1%。","assumption":"base 假設 RevPAR 全週期 +2%～4%、淨增房數 6%～7%","consequence":"2028 年衰退使 RevPAR 轉負，EPS 下方的固定成本反向放大，EPS 回到 3.9 美元；倍數由 49 倍收斂到 20 倍，五年後股價約 95 美元，跌約一半。","ruling":"部分採納，給 30% 機率。供給成長 0.6%～1.3%、在建量 12 年低，限制了下行深度，所以不把衰退情境放到 base 之上。這條與唯一致命點同源（RevPAR 轉負），不另立。","watch":"每季系統可比 RevPAR；2027 指引","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_kpi5_comparable_system_wide_r","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"key money 競爭激烈，管理層預估每年 1.5～1.7 億美元（2026-10-29 CEO）。Hall Financial 的 5 億美元融資工具由 Hyatt 提供部分信用支持（2026-07-30 CEO）。出售 Playa 時另投 2 億美元優先股給買方。2025 報表自由現金流 1.59 億（利益率 2.2%），公司調整後口徑約 4.85 億。以 FY1 EPS 計，現價回購的盈餘殖利率約 2%。","assumption":"費用與房數達標，就能轉成每股價值","consequence":"房數與費用都達標，但業主支援（key money、信用支持、優先股）吃掉自由現金流，報表與調整後現金流持續有大落差；回購又在 40～50 倍盈餘下進行，每股價值累積得比費用成長慢。","ruling":"採納為監測項。以管理層自訂的調整後 EBITDA 轉自由現金流 ≥50% 為門檻，並追蹤報表與調整後自由現金流的差距；回購買入收益率偏低這點，已直接計入資本配置評分。","watch":"年度調整後 FCF／EBITDA；報表 FCF；key money 是否超過 1.7 億","evidence_refs":[],"fact_refs":["f_kpi8","f_fwd_pe_latest"]},{"view":"價格已反映太多","evidence":"FY1 前瞻本益比 49 倍、FY2027 38 倍、trailing 98 倍；P/E、P/S、EV/S 都在自身年度端點分位 100。RSI 70，26 週漲 18%。Q2 後多家券商下調目標價，均價約 195～198 美元。","assumption":"市場會持續給輕資產轉型完成的溢價倍數","consequence":"即使 EPS 照 base 走到 8.6 美元，倍數回到 27 倍時，五年價格報酬每年只有約 4%。","ruling":"採納。這是本次不追價的主因，進場改等 155 美元以下。","watch":"股價對 FY2027 共識的倍數；共識修正方向","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_rsi14","f_week26_return_pct","f_consensus_rev_fy2_pct"]},{"view":"論點失敗","evidence":"10-K 承認：AI 工具決定給使用者什麼資訊時，Hyatt 物業可能得到較少關注；新分銷通路（含潛在 AI 平台）可能對業務造成負面影響。管理層也說代理式訂房會成長很快。","assumption":"直銷約七成與會員入口可以延續","consequence":"2028 年後代理式 AI 成為主要預訂入口，Hyatt 只能付佣換曝光，費用率與會員價值下降，倍數向中價位連鎖靠攏。","ruling":"暫不採納為 base。LLM 完成的訂房目前非常少；Hyatt 已在 ChatGPT 等平台建立自有入口，接在自有資產上屬強化。設直銷占比低於 65% 為轉向條件。","watch":"直銷房晚占比；管理層揭露的 AI 來源訂房占比","evidence_refs":["substitute_technology#0","channel_business_model_shift#1","competitive_share_entrants#0"]}],"max_dd":{"lo":-60,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 164.4 → 本次 187.89（+14.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=164.4","side_b":"本次 price_at_dd=187.89","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 164.4 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 164.4 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 164.4 美元：Bull 價 332.8、Bear 價 95，五年期望值 +28.4%，基準年化 7.1%，不對稱比 1.62","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.62。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 164.4 美元：五年期望值 +28.4%，基準年化 7.1%，不對稱比 1.62","side_b":"本次情境、股價 187.89 美元：五年期望值 +12.4%，基準年化 4.3%，不對稱比 1.04","ruling":"再換股價、情境不動：起點價上漲 14.3%，五年期望值少 16.1 個百分點，基準年化少 2.8 個百分點，不對稱比由 1.62 降到 1.04。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"淨增房數：承諾對實績","cause":null,"prior_field":null,"side_a":"管理層：2026 全年淨增房數約 6%，2026–2028 年複合 6%～8%，2027 Q1 可達 6%～7%（2026-10-29 CEO）","side_b":"Q3 2026 淨增房數只有 3.9%（不含 Playa），全年過半開幕擠在 Q4；2026-07-30 CEO 已說部分 Q4 開幕可能延到 2027，轉換案的 PIP 也比原先模型重","ruling":"程度差異，可以調和。採信方向、不採信時點：base 假設 2026 全年約 5%～5.5%，2027 回到 6%～7%。若 2026 全年低於 5%，開發飛輪假設降為削弱。","evidence_level":"公司季報與法說（自報）","settle_metric":"FY2026 全年淨增房數（2027-02 第四季財報）","if_then":["若 FY2026 淨增房數 <5% 且 2027 指引 <6%：開發飛輪假設降為削弱，停止加碼","若 FY2026 ≥6% 且 2027 Q1 單季 ≥6%：維持假設，動作不變"],"evidence_refs":[]},{"axis":"2027 RevPAR：公司口徑對產業預測","cause":null,"prior_field":null,"side_a":"公司兩度上修 2026 全年 RevPAR 指引至 5%～5.5%，稱 2027 的布局很好：企業團體 pace 近 +10%，扣除世足的團體 pace 為中個位數（2026-10-29 CFO、CEO）","side_b":"CoStar 預測美國 2027 RevPAR 只有 +2.1%；同業給 2027 年 3%～4%；管理層自己也說世足與節日時點不會重複；Green Street 估 2026 年前 50 大市場需求成長 1.3%，低於歷史 2%","ruling":"程度差異，可以調和。Hyatt 的高端與休閒組合有贏過產業的紀錄（年初至今市占 +100bp），但 base 只給 2027 系統 RevPAR +2%～3%，不跟管理層的語氣走；衰退情境給 30%。","evidence_level":"第三方產業預測加公司前瞻 pace","settle_metric":"2027 RevPAR 指引（2027-02）與 2027 Q1 實績（2027-05）","if_then":["若 2027 指引 RevPAR ≥4%：上調 base 路徑並重算進場價","若 2027 指引 ≤1% 或 Q1 實績轉負：衰退機率上調至 40%，未持有者不建倉"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"Distribution 與全包式：暫時性歸因","cause":null,"prior_field":null,"side_a":"2026-05-28 投資人日 CFO：2026 年的颶風與墨西哥干擾屬暫時，Distribution EBITDA 年複合成長 2%～4%。Q3 法說稱 2027 Q1 全包式訂房 pace 為高個位數，坎昆航班運能回升，牙買加 2027 Q1 末至 Q2 初復開","side_b":"Distribution 全年 EBITDA 預期年減幅度由 Q2 的 2,500 萬擴大到 3,000 萬，Q3 也低於公司預期；net package RevPAR Q2 −1.2%、Q3 −2.5%；2025 Distribution 營收已年減 7.5%；這塊業務的去留，管理層沒有給答案","ruling":"管理層的一次性歸因，不採信也不否定，標為未證、監測。預先登記：若 2027 上半年 Distribution 調整後 EBITDA 仍低於 2025 同期，或 2027 Q1 net package RevPAR 仍為負，暫時性歸因視為證偽。","evidence_level":"公司季報加法說","settle_metric":"2027 Q1、Q2 的 net package RevPAR 與 Distribution 調整後 EBITDA","if_then":["若證偽：衰退機率上調 5pp，Distribution 改以永久性減損看待","若 2027 Q1 net package RevPAR 轉正且 Distribution EBITDA 年增：維持暫時性歸因"],"evidence_refs":["end_markets#1","channel_business_model_shift#2"]},{"axis":"觀望對現在就買","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：全年指引兩度上修，FY1 共識三個月上修 4.7%，pipeline 與會員都創新高；2027 有牙買加復開與墨西哥回升這兩個已知順風；回購授權還有 14 億美元，可以在回檔時承接","side_b":"股價 26 週漲 18%、RSI 70，但 FY2027 共識只上修 0.82%、FY2028 只上修 0.5%，漲幅主要來自倍數擴張；Q2 後多家券商下調目標價，均價約 195～198 美元，只比現價高約 5%；FY2027 共識 38 倍","ruling":"採觀望，約束條件是估值。漲幅來自倍數而不是遠期盈餘；base 情境五年價格報酬每年約 4%（不含股息與回購），撐不起 30% 機率的衰退情境。","evidence_level":"共識快照加價格資料","settle_metric":"FY2027 共識 EPS 與股價的相對變化","if_then":["若股價續漲而 FY2027 共識未上修 ≥3%：不追","若股價回落至 155 美元以下且共識未下修：重跑估值後分批建倉"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：美國供給成長 2026～2027 年約 0.6%～1.3%，在建量 12 年低，品牌方在高端市場的房價指數上升","side_b":"其他結構變數：10-K 把含 AI 平台的新分銷通路列為負面因素；競爭面則有同業整併與 key money 加碼","ruling":"雙向拉鋸。供給軸轉好，通路軸（代理式 AI）變動中，競爭軸大致靜態；淨效果不足以改變護城河方向。","evidence_level":"第三方產業資料加 10-K","settle_metric":"美國年度供給成長率；直銷房晚占比","if_then":["若美國年度供給成長升破 2%：衰退機率上調","若直銷房晚占比 <65%：護城河方向改判縮減"],"evidence_refs":["channel_business_model_shift#1","competitive_share_entrants#1"]},{"axis":"前份漂移：價格","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-20，股價 164.4）：綜合評級 B，估值偏貴（🟠）","side_b":"本次（股價 187.89，漲 14%）：綜合評級 B，估值偏貴（🟠）；FY1 49 倍、FY2027 38 倍","ruling":"股價上漲，但 FY2027 共識同期只微調，估值更貴；沒有到極端，是因為 FY2028 的 31 倍對應約 25% 的盈餘成長。兩欄的值都沒變，變的是價格。前次觀望以來報酬 +14%，未達需要說明翻面理由的 30%。","evidence_level":"價格與共識快照","settle_metric":"股價對 FY2027 共識的倍數","if_then":["若倍數升破 45 倍：已持有者減碼","若倍數回到 32 倍以下：重跑研究"],"evidence_refs":[]},{"axis":"前份漂移：方法補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這幾欄都是空值，沒有產出護城河方向、五年後成長空間、公司類型、循環位置、情境機率與最大回撤","side_b":"本次：護城河方向穩定（→），五年後成長空間寬（🟢），類型為品質複利成長（次類循環），循環位置中循環，情境機率 20／50／30，最大回撤 −45%～−60%；裁決與角色由矩陣依新欄位產生","ruling":"屬方法補齊，不是基本面變化。","evidence_level":"方法變更","settle_metric":"無","if_then":["若下份研究上述欄位改變：依新證據或價格分別歸因"],"evidence_refs":[]},{"axis":"前份漂移：陷阱判讀","cause":"方法變動","prior_field":["trap"],"side_a":"前份陷阱判讀 🟢","side_b":"本次 🟡：十項衰退信號中，「EPS 成長顯著高於營收成長」亮燈（FY2027 共識 EPS +28.6%，共識營收 +8.1%）","ruling":"本次事實表首度有共識營收可以比對，逐項計數得到 1 項。成因是 EBITDA 下方固定成本攤薄，不是品質惡化，所以只到 🟡。","evidence_level":"共識快照","settle_metric":"FY2027 實際 EPS 與營收成長差","if_then":["若再亮第 2 項以上：陷阱判讀維持 🟡 並重估倉位上限","若 EPS 與營收成長差縮到 5pp 內：回到 🟢"],"evidence_refs":[]},{"axis":"建倉門檻變更","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"建議等 Fwd PE<28x 或股價回測 W52 $151","side_b":"股價回落至 155 美元以下（約 FY2027 共識 EPS 32 倍），且 2027 指引的 RevPAR 與淨增房數未下修","ruling":"前份以單一倍數與 52 週均線作為建倉錨；本次改由情境樹反推。股價 155 美元時，base 五年價格報酬每年約 8%，加股息與回購約 10%。52 週均線已上移到 168.6，不再適合當錨點；新門檻約略等於 104 週均線 154.5。","evidence_level":"情境樹推導","settle_metric":"股價","if_then":["若股價 ≤155 且 2027 指引未下修：重跑研究後分批建倉","若股價 ≤155 但指引下修：不建倉，先重估 base 路徑"],"evidence_refs":[]},{"axis":"唯一致命點變更","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）","side_b":"Single Thing：2027～2028 年旅宿景氣轉入衰退，系統可比 RevPAR 出現單季年減 3% 以上","ruling":"前份沒有指定唯一致命點；本次依敏感度選 RevPAR。每 1 個百分點的 RevPAR 變動同時影響費用、獎勵費與倍數，敏感度大於淨增房數落後。發生時減碼至半倉，連 2 季為負則清倉。","evidence_level":"情境樹敏感度","settle_metric":"每季系統可比 RevPAR","if_then":["若單季 ≤−3%：減碼至半倉","若連 2 季為負：清倉並重跑研究"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"風險門檻與退場指標變更","cause":"新證據","prior_field":["kill_metrics","thesis.R"],"side_a":"前份 R1：連 2 季 RevPAR 年增轉負；R2：調整後 EBITDA 利益率差距由 5pp 擴大到 >8pp 連 2 年；R3：Fwd PE 跌至 25 倍或 EV/EBITDA <18 倍；前份未設退場指標","side_b":"本次：RevPAR 連 2 季年減，或單季 ≤−3% 即減碼、連 2 季清倉；利益率差距 >8pp 門檻保留，標資料缺口；倍數壓縮改列為建倉條件，不再列為風險；新增五項退場指標：gross fees <9%、淨增房數 <5%、FCF 轉換 <50%、Distribution EBITDA 再年減、直銷占比 <65%","ruling":"RevPAR 門檻加上單季 −3%，是因為 Q3 法說顯示 2026 年有一次性助力，而產業預測 2027 年只剩 +2.1%。倍數門檻退休：現價 EV/EBITDA 約 18.3 倍，已貼近前份的 18 倍門檻，但那是估值問題、不是論點風險，改由建倉價處理。利益率差距門檻保留，但事實表只有報表營業利益率（H 7.2%、MAR 15.7%、HLT 24.0%），沒有調整後 EBITDA 利益率，標資料缺口。","evidence_level":"Q3 2026 季報、法說與產業預測","settle_metric":"各退場指標","if_then":["若任一退場指標觸發：依該指標動作減碼或清倉","若利益率差距資料補齊且 >8pp 連 2 年：護城河改判縮減"],"evidence_refs":["supply_demand_durability#3","competitive_share_entrants#1"]},{"axis":"假設門檻變更","cause":"新證據","prior_field":["thesis.H"],"side_a":"前份 H1：RevPAR 年增 +2%～5%（連 2 季 <−2% 為反轉）；H2：會員 FY28 突破 1 億；H3：輕資產 2026 年達 90%（下限 88%）","side_b":"本次 H1：gross fees 年增 ≥9%；H2：淨增房數 ≥5%、三年複合 ≥6%；H3：會員年增 ≥10%、直銷占比 ≥65%；RevPAR 改由唯一致命點與 R1 監測","ruling":"會員 1 億的門檻退休：目前 7,200 萬、年增 19%，到 2028 年底要再年增約 16% 才達標，門檻過度依賴單一增速，而且會員數不等於費用，改用年增率。輕資產 90% 已兌現（2026 年約 90%），退休。RevPAR 從假設移到風險端，是因為 Q3 法說顯示 2026 年有一次性助力。","evidence_level":"Q3 2026 季報與 2026-05-28 投資人日","settle_metric":"gross fees、淨增房數、會員年增率","if_then":["若 H1 至 H3 任兩項削弱：停止加碼並重跑研究","若三項皆維持：動作不變"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 全年 gross fees 指引年增低於 9%，視為費用引擎假設削弱","type":"假設驗證","maps_to":"H1","metric":"FY2027 gross fees 成長指引","threshold":"<9%","action":"停止加碼；未持有者維持觀望","source_freq":"第四季財報（一年一次）","date":"2027-02"},{"n":2,"text":"FY2026 全年淨增房數低於 5%，視為開發飛輪假設削弱","type":"假設驗證","maps_to":"H2","metric":"FY2026 淨增房數","threshold":"<5%","action":"停止加碼，重估 base 的房數路徑","source_freq":"季報","date":"2027-02"},{"n":3,"text":"系統可比 RevPAR 單季年減 3% 以上，唯一致命點成立","type":"Single Thing","maps_to":"Single Thing","metric":"系統可比 RevPAR 年增率（每季）","threshold":"單季 ≤−3%；連 2 季為負","action":"單季 ≤−3% 減碼至半倉；連 2 季為負清倉並重跑研究","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"全包式復甦落空：2027 Q1 net package RevPAR 仍為負","type":"風險","maps_to":"R2","metric":"net package RevPAR 年增率","threshold":"2027 Q1 <0","action":"Distribution 改以永久性減損看待，衰退機率上調 5pp，停止加碼","source_freq":"季報","date":"2027-05","evidence_refs":["end_markets#1","channel_business_model_shift#2"]},{"n":5,"text":"直銷房晚占比跌破 65%，或 AI 平台來源訂房超過 5% 且需付佣","type":"風險","maps_to":"R3","metric":"直銷房晚占比、AI 來源訂房占比","threshold":"<65% 或 >5%","action":"護城河方向改判縮減，減碼三分之一","source_freq":"年度（投資人日、10-K、法說）","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1","channel_business_model_shift#1","competitive_share_entrants#0"]},{"n":6,"text":"中東與墨西哥合計的年度費用衝擊擴大","type":"風險","maps_to":"R4","metric":"區域費用衝擊（管理層揭露）","threshold":">4,000 萬美元／年","action":"衰退機率上調 5pp，停止加碼","source_freq":"季報法說","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#2"]},{"n":7,"text":"股價回落到 155 美元以下，且 2027 指引未下修：重跑研究後分批建倉","type":"估值rearm","maps_to":null,"metric":"股價（約為 FY2027 共識 EPS 的 32 倍）","threshold":"≤155 美元","action":"重跑研究確認論點未破，首批建倉不超過目標倉位的三分之一","source_freq":"每日價格","date":null},{"n":8,"text":"已持有者在 FY2027 共識 45 倍以上分批減碼","type":"減碼","maps_to":null,"metric":"股價","threshold":"≥221 美元（FY2027 共識 4.90 × 45，約等於賣方最高目標價）","action":"減碼三分之一","source_freq":"每日價格","date":null},{"n":9,"text":"第四季財報與 2027 全年指引","type":"複審日期","maps_to":null,"metric":"2027 年 RevPAR、淨增房數、gross fees 與 EBITDA 指引","threshold":null,"action":"重跑情境樹與進場價","source_freq":"一年一次","date":"2027-02"},{"n":10,"text":"World of Hyatt 會員年增連 2 季低於 10%","type":"假設驗證","maps_to":"H3","metric":"會員數年增率","threshold":"<10%，連 2 季","action":"會員入口假設降為削弱，停止加碼","source_freq":"季報","date":null}],"kill_metrics":[{"metric":"系統可比 RevPAR 年增率（每季）","bear_threshold":"單季 ≤−3% 減碼至半倉；連 2 季為負清倉","window":"每季財報","source":"公司季報新聞稿（Q3 2026 為 +7.2%）","last_status":"ok"},{"metric":"年度 gross fees 成長率","bear_threshold":"<9%（投資人日三年複合 9%～13% 的下緣）","window":"年度（2027-02 起）","source":"季報新聞稿與第四季法說指引（2026 指引 +10%～11%）","last_status":"ok"},{"metric":"年度淨增房數","bear_threshold":"<5%","window":"年度","source":"季報新聞稿（Q3 2026 為 3.9%，全年目標約 6%）","last_status":"warning"},{"metric":"調整後 EBITDA 轉調整後自由現金流比率","bear_threshold":"<50%（管理層自訂下限）","window":"年度","source":"季報新聞稿與法說（2026 指引 ≥50%）","last_status":"ok"},{"metric":"Distribution 分部調整後 EBITDA","bear_threshold":"2027 上半年仍低於 2025 同期","window":"2027 上半年","source":"季報分部資料（2026 全年預期年減約 3,000 萬美元）","last_status":"warning"},{"metric":"Hyatt 對 MAR、HLT 的調整後 EBITDA 利益率差距","bear_threshold":">8pp 連 2 年（沿用前份門檻）","window":"年度","source":"資料缺口：事實表只有報表營業利益率（H 7.2%、MAR 15.7%、HLT 24.0%）","last_status":"unknown"},{"metric":"直銷房晚占比","bear_threshold":"<65%","window":"年度","source":"投資人日、10-K 與法說揭露（2026-05-28 約 70%）","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"這是 10-K 對 IT 與雲端供應商依賴的一般性風險揭露，沒有指出任何已發生的事件、受影響營收或金額，無法對應到可監測的門檻；日後若出現具體的系統中斷事件，再列入風險。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=18.28, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Hyatt 的 Bull 情境有量加價的骨架，Essentials 新市場擴張也有公開來源，但從費用收入到 EPS 的槓桿、230 萬間可拓展房數這個數字，以及同業 5 年實際報酬的對照都沒有可驗證的來源，目前只能算部分成立，沒有哪一項被證偽。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回落至 155 美元以下（約 FY2027 共識 EPS 32 倍），且 2027 年指引的 RevPAR 與淨增房數未下修'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價回落至 155 美元以下（約 FY2027 共識 EPS 32 倍），且 2027 指引的 RevPAR 與淨增房數未下修","exec_line":"觀望、不追價。未持有者等股價 ≤155 美元且 2027 指引未下修，重跑研究後分批建倉；已持有者續抱，≥221 美元減碼三分之一；RevPAR 單季 ≤−3% 減碼至半倉，連 2 季為負則清倉。"},"reasoning":{"industry":"營收結構：Q3 2026 報表營收 17.43 億美元，其中 gross fees 3.27 億（年增 15.2%），調整後 EBITDA 2.95 億，GAAP 淨利 0.58 億。全年 gross fees 指引 13.2～13.35 億（2026-10-29 CFO），約占 FY2026 共識營收 71.4 億的 19%，其餘為自有與租賃飯店、Distribution 及其他非費用營收；分部營收事實表未拆。TTM 毛利率 20.1%、營業利益率 7.2%，報表利益率被非費用營收稀釋，看獲利能力要看費用與調整後 EBITDA。成長來源：Q3 系統可比 RevPAR +7.2%，約八成來自房價；pipeline 約 15.8 萬間，年增 12%。單點依賴：10-K 載明沒有單一重要客戶。集中點在兩處，一是通路（直銷約七成，2026-05-28 投資人日 CEO），二是全包式事業的墨西哥 Riviera Maya（約占全包式三分之一強，2026-10-29 CEO）。景氣位置屬擴張期（II）：美國供給成長約 0.6%～1.3%、在建量 12 年低；需求成長 1.3% 低於歷史均值，RevPAR 靠房價推動。供需持久性：供給面屬結構性、偏持久；需求面屬週期性。景氣反轉時，壓力會先出現在房價，而不是供給過剩。","moat":"機制：高端品牌與會員讓業主拿到較高的 RevPAR，Hyatt 以此換取長約與費用。執行力判擴大：年初至今市占 +100bp、房價指數上升（2026-10-29 CEO），坎昆全包式市占 +400bp（CFO），簽約量 +70%、動工 +40%，會員 7,200 萬、年增 19%。定價力判穩定：房價貢獻約八成 RevPAR 成長，管理層稱 pipeline 每房費用高於在營飯店；但業主端 key money 競爭激烈（CEO：key money flying around）。同業只能比利益率：營業利益率 Hyatt 7.21%，MAR 15.73%、HLT 24.01%、CHH 25.52%、WH 36.38%；FCF 利益率 Hyatt 6.35%，MAR 11.64%、HLT 14.49%。差距有一部分來自 Hyatt 仍有自有飯店與 Distribution，一部分是規模。同業投入資本與 ROIC 事實表未涵蓋，無法驗證報酬差距方向，所以合併分不給到 8 分以上：執行力 8、定價力 7，等級 B。市占數據是公司自報，第三方報導也說沒有直接數據，因此不標擴大。AI 曝險：Hyatt 已在 ChatGPT 等平台建自有入口，這是接在自有資產上的強化；若代理式 AI 改經 OTA 或平台自家預訂完成訂房，就是繞過 Hyatt。管理層預期未來兩年代理式訂房成長很快，分界年抓 2028。再投資：增量報酬約 20%～35%，再投資率約 33%，內生成長上界約 10%。","growth":"共識三年 EPS：FY2026 3.81、FY2027 4.90、FY2028 6.09 美元（Koyfin 快照；分析師家數事實表未載，營收共識為 20 位分析師），FY2026→FY2028 兩年年複合 26.4%。FY2025 GAAP 每股 −0.55 美元口徑不同，不作基期。共識營收 FY2026 71.4 億→FY2027 77.2 億，年增 8.1%。內生上界約 10%（增量報酬 20%～35% × 再投資率約 33%，推導見護城河段）。缺口約 16pp，可以歸因：①利益率擴張：EBITDA 下方的折舊與利息等成本相對固定，EBITDA 年增 11%～16%（投資人日 2025–2028 指引）就能撐出 20% 以上的 EPS 成長；這是推論，折舊與利息事實表未涵蓋。②淨回購約 2pp：2026 回饋指引 3.75～4.25 億，扣除股息後約占市值 2%。③2026～2027 的 RevPAR 景氣順風。缺口既然可歸因，就不屬於靠倍數重估撐起的成長。成長空間：管理層辨識約 230 萬間可拓展房數，Essentials 新品牌與國際 pipeline 構成第二條曲線，判 🟢。中高價位的單房費用較低，但管理層稱 pipeline 整體每房費用仍高於在營飯店。十項衰退信號亮 1 項（EPS 成長遠高於營收），長期成長性 🟡。","governance":"現金轉換：年度報表 FCF／淨利，2022 年 1.04、2023 年 2.74、2024 年 0.36（淨利含資產出售利得），2025 年淨利為負、不具意義。2025 報表 FCF 1.59 億（利益率 2.2%）；公司 2026 調整後 FCF 指引 5.8～6.3 億、年增 20%～30%，反推 2025 調整後約 4.85 億。兩種口徑差約 3.3 億，原因事實表未涵蓋。SBC 占營收 0.63%，稀釋可以忽略。現金去向：每年再投資約 3 億（key money 1.5～1.7 億、資本支出 1.35～1.4 億）。2026 股東回饋指引 3.75～4.25 億（Q2 時為 3.25～3.75 億）；2022 年以來回饋 21 億，占現金運用逾九成。收購：2025 年收購 Playa，同年 12 月以約 20 億美元出售不動產，保留管理合約，並投資 2 億美元優先股給買方。Two Roads 收購價只有單一法文來源，由 4.8 億降至 4.05 億，未核原文、不計入。兩案的收購後報酬事實表都無法驗證。負債：總債務 46.48 億、現金 4.95 億，淨負債 41.53 億（含租賃口徑），約為 2026 調整後 EBITDA 指引中值的 3.5 倍；流動性約 18 億，公司承諾維持投資等級。三項評分：收購報酬無法驗證、回購買入收益率不通過、SBC 稀釋通過。","valuation":"現價 187.89 美元。FY2026（FY1）共識 EPS 3.81 對應 49.3 倍，FY2027 的 4.90 對應 38.3 倍，FY2028 的 6.09 對應 30.9 倍；trailing GAAP 97.9 倍受 2025 年一次性損益干擾，不採用。EV 217 億美元除以 2026 調整後 EBITDA 指引中值 11.85 億，約 18.3 倍；前瞻 EV/S 3.04 倍。P/E、P/S、EV/S 都在自身 3～4 個年度端點的最高位（分位 100），但這不是五年分位。PEG＝49.3 ÷ FY2026–2028 EPS 年複合 26.4%＝1.87，落在合理區間上緣。自由現金流殖利率約 3.4%（調整後 FCF 指引中值 6.05 億 ÷ 市值 175 億），股息殖利率 0.32%。賣方目標價均值約 195～198 美元（2026 年 8～9 月，都在 Q3 上修指引之前），最高 221，現價的上行空間約 5%。Base 情境為 2031 年 EPS 8.6 × 27 倍＝232 美元，五年價格報酬只有每年約 4%，加股息與回購約 6%，不足以補償 30% 機率的衰退情境。","premortem":"三個視角與 AI 通路情境已寫在反證紀錄，這裡不重寫。壓力測試 5 項過 3 項。①2026 年墨西哥、中東、牙買加合計 EBITDA 衝擊約 6,000 萬美元，費用仍維持 +10%～11%：通過。②流動性約 18 億、承諾投資等級：通過。③SBC 0.63%：通過。④RevPAR 轉為年減 3%，EPS 成長轉負：不通過。⑤倍數回到 27 倍，base 五年報酬每年低於 8%：不通過。管理層迴避的問題集中在幾處：key money 的新建與轉換拆分、會員滲透率的同口徑數字、系統基金提撥率（2026-05-28 投資人日），以及 2027 淨增房數的具體數字（2026-07-30）。這幾處是資訊最軟的地方。歷史最大回撤事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"Hyatt 賺的是業主付的費用：把高端品牌、會員與訂房系統授權給業主，按飯店營收與利潤抽管理費與加盟費。錢卡在「誰握有訂房入口」這一節點，目前約七成房晚走 Hyatt 直銷；這一節守得住，費用就能維持雙位數成長。","moat":"護城河方向判穩定（→）。高端品牌組合與 World of Hyatt 會員讓 Hyatt 在競爭組中持續拿到市占與房價指數；但報表利益率只有同業一半左右，代理式 AI 分銷入口也還沒定局，所以不標擴大。","growth":"5 年後的成長空間仍寬（🟢）。中高價位 Essentials 品牌進入 Hyatt 原本沒有據點的市場（美國簽約過半在新市場，pipeline 逾 150 家），是第二條成長曲線。但共識 EPS 年增約 26%，大半來自固定成本攤薄與回購，不是內生成長。","capital":"資本配置中等。現金九成以上回饋股東，SBC 很低；但在 40～50 倍盈餘下回購，買入收益率偏低，收購報酬也無法驗證。報表與調整後自由現金流的口徑落差大，是要盯的地方。","valuation":"現價要求 2026–2028 年每股盈餘照共識年增約 26%，而且五年後市場仍給 27 倍以上，才換得每年約 6% 的報酬。成長方向我信，但價格沒有留安全邊際，估值偏貴。","how_wrong":"最可能看錯的是景氣。2026 年的 RevPAR 有一次性助力；若 2027～2028 年轉入衰退，固定成本會把費用下滑放大成 EPS 下滑，49 倍的倍數也會失去支撐。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回落至 155 美元以下（約 FY2027 共識 EPS 32 倍），且 2027 年指引的 RevPAR 與淨增房數未下修","qc48_result":"pass","qc48_note":"Hyatt 的 Bull 情境有量加價的骨架，Essentials 新市場擴張也有公開來源，但從費用收入到 EPS 的槓桿、230 萬間可拓展房數這個數字，以及同業 5 年實際報酬的對照都沒有可驗證的來源，目前只能算部分成立，沒有哪一項被證偽。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":187.89,"week26_return_pct":18.28,"consensus_rev_3m_pct":4.67,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"trailing GAAP 本益比 98 倍的分母受 2025 年 GAAP 每股虧損 0.55 美元與資產出售損益干擾，改用 FY1、FY2 共識；前瞻分母本身不是爭點。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉（管理層稱會壓抑 Q4 美國 RevPAR）","impact":"低","watch":"Q4 美國 RevPAR 是否低於指引隱含值"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年指引（RevPAR、淨增房數、gross fees、EBITDA）","impact":"高","watch":"2027 RevPAR 指引是否 ≥2%，淨增房數是否 ≥6%"},{"date":"2027-02","date_precision":"month","type":"product","event":"Delta 雙向累積合作的細節揭露","impact":"中","watch":"會員交叉使用與聯名卡的經濟效益是否量化"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"轉換案端到端 AI 平台完成","impact":"低","watch":"轉換案開幕週期是否縮短，2027 Q1 淨增房數是否達 6%～7%"},{"date":"2027-04","date_precision":"quarter","type":"capacity","event":"牙買加飯店復開（管理層預估 2027 Q1 末至 Q2 初）","impact":"中","watch":"Distribution 分部 EBITDA 是否轉為年增"}],"_projected_from":"v19"}
```
