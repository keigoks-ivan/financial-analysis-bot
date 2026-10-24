你是 stock-analyst v20 的**散文層（prose）agent**，標的 TSLA（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：TSLA　日期：2026-10-24　archetype：None　前份裁決：2026-07-05　迴避｜不持有/迴避　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1697B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（783B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1120B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1419B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1067B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（463B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（623B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2174B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3481B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2340B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1697           3712-5303      5 條（2–6 內）  
s3                  8000         783           5052-7217      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3606          7976-11394      5 條（2–6 內）  
s6                 11000         463          7376-10537      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         623           2014-2877      5 條（2–6 內）  
s10                 5000        2174           1978-2826      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2340           2000-2660      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5113B；至少需散文≈39.89KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−82
−82%
−65%
−60%
−59%
−50%
−50
−18.7
−12.0%
−6.5%
−6.4%
−5.4%
−5.1%
−4.1%
−3.74%
−3%
−2.7%
−1.1%
−1.08
−1.08%
0%
0
0.30
0.56%
0.7
0.98%
1
01
1.08
1.1
1.13
1.16
1.2
1.3
1.37%
1.5
1.6
1.7
1.7%
1.77
1.9
2
2%
2.1
2.16
2.2
2.3
2.4
2.42%
2.6%
2.9
3%
03
3
3.22
3.45
3.6
3.7
04
4%
4
4.15%
4.17
4.31
4.6
4.61%
4.94
5%
5
5.25%
5.3
5.4%
5.5
5.6
5.74%
6
06
6.03
6.2%
6.8
7
07
7.18
8
8.3
8.8
09
9%
9.19%
9.6%
9.6
10%
10
10.7%
10.9
11%
11
11.65
12
12%
12.5
13%
13.5
13.7
14
15%
15
15.3%
15.31
15.9
15.9%
16%
16.2%
16.3%
17%
17.76%
17.9%
18
18%
18.03%
18.1%
18.5%
18.7%
18.85%
19%
20%
20
21
22
22%
24
25%
25
25.6%
26
29
30%
30
33%
33.1%
35%
35
40
40%
42%
42
45
46
46.7
48
49
50%
50
51.5
54%
55%
55
60
70%
70
73%
73.5
74
75%
80
80%
90
91
100
100%
115
134
138
150
150%
160
170
172
172.3
185
192
200
$200
206
210
210.29
216
250
280.5
300
303
372.22
393.45
408
450
600
660
840
1211
2018
2022
2023
2025
2026
2027
2028
2031
20261024
1,000
144,094
262,649
486,532
7,000
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
{"meta":{"ticker":"TSLA","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Tesla, Inc."},"oneliner":"車業利潤薄、估值押在無人車：Fwd P/E 約 210 倍，基本情境五年後約 303 美元仍低於現價，等股價回到 250 美元或無人車營收證據到位再談","thesis":{"H":[{"id":"H1","text":"FSD 訂閱與無人車服務成為經常性利潤來源：付費客戶持續擴大，Robotaxi 2027 年起貢獻可見營收","2y":"2027 年底 FSD 付費客戶≥250 萬、無人監督營運≥10 城","5y":"FSD 與 Robotaxi 占公司毛利三成以上","10y":null,"threshold":"2027 年底 FSD 付費客戶≥250 萬（現約 170 萬）且無人監督營運城市≥10 個","source":"季度更新簡報與法說會（CFO 承諾隨規模揭露 FSD 營收與流失率）","drift_rule":"付費客戶季增連兩季<5% 為削弱、連三季持平或下滑為反轉；2027 年中無人營運仍≤6 城為削弱"},{"id":"H2","text":"汽車本業毛利守住：不含法規積分的汽車毛利率站穩 17% 以上，交付恢復成長","2y":"FY2027 交付≥185 萬輛、汽車毛利率不含積分全年≥17%","5y":null,"10y":null,"threshold":"汽車毛利率（不含法規積分）每季≥17%；FY2027 交付≥185 萬輛（市場共識約 192 萬）","source":"季度交付公告與更新簡報","drift_rule":"連兩季低於門檻≥5%（<16.2%）為削弱，連三季低於≥10%（<15.3%）為反轉"},{"id":"H3","text":"儲能成為第二條利潤線：Megapack 資料中心需求與自產 LFP 電芯撐住部署成長與毛利","2y":"2027 年部署≥60 GWh","5y":"能源毛利占全公司毛利≥25%","10y":null,"threshold":"2027 年部署≥60 GWh，且扣除關稅退款與保固回沖後毛利率≥22%","source":"季度更新簡報與法說會","drift_rule":"部署年增連兩季轉負為削弱；扣除一次性後毛利率連兩季<20% 為反轉"}],"R":[{"id":"R1","text":"本季利潤靠一次性項目撐：能源毛利 33.1% 含關稅退款與供應商保固分攤，汽車毛利改善來自亞太組合；Q4 回落即暴露真實獲利","h_ref":"H3","clock":"⚡","threshold":"Q4 2026 能源毛利率<22% 或汽車毛利率（不含積分）<17%","evidence_refs":["end_markets#1","reg_tariff_export#1"]},{"id":"R2","text":"無人車監管與訴訟：NHTSA 學區超速請願評估、Cybercab 無踏板自我認證查詢、FSD 調查、多起召回、Autopilot／FSD 證券集體訴訟（德州駁回聲請待裁、另有加州案）","h_ref":"H1","clock":"🔥","threshold":"NHTSA 正式立案或要求暫停無人營運；或集體訴訟駁回聲請遭拒","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#2","major_events#3","major_events#5","lawsuit_class_action#0","product_recall_warning#0"]},{"id":"R3","text":"競爭：中國品牌西歐份額創 10.7% 新高、BYD 全球 BEV 份額 12% 逼近；Waymo 無人車規模領先，新進者陸續上路；其他車廠可能借外部方案追上 L2+ 並壓低 FSD 價格","h_ref":"H2","clock":"🔥","threshold":"全球 BEV 份額連兩季<11%，或北美 FSD 交車附加率回落至 55% 以下","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","competitive_share_entrants#5","substitute_technology#0"]},{"id":"R4","text":"資本支出週期與關係人交易：Terafab 至 2028 年初投入數百億美元、長期逾千億，與 SpaceX 分攤未定；合併探索條款未定，可能以換股稀釋股東","h_ref":"H1","clock":"🐢","threshold":"年度自由現金流轉負並動用新信貸額度，或合併換股稀釋逾 10%","evidence_refs":["capital_markets_pricing#0","major_events#0","ma_merger#0"]},{"id":"R5","text":"關稅與供應鏈地緣：關稅推高電芯與零組件成本、對儲能衝擊大於汽車；中國稀土磁鐵出口許可曾延誤 Optimus","h_ref":"H3","clock":"🐢","threshold":"汽車或能源毛利率因關稅單季下滑≥2 個百分點","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#1"]}],"single_thing":{"description":"無人監督 Robotaxi 或 Cybercab 車隊發生致死或重傷事故，監管機關因此暫停或限制無人營運","why_fatal":"現價約 FY2026E 共識 210 倍，倍數幾乎全靠無人車與 FSD 的未來利潤；暫停營運會同時打到 H1 時程、FSD 訂閱需求與 Optimus 的 AI 敘事，Bull 情境幾乎歸零","if_happens":"持有者清倉；重啟條件作廢，待監管恢復且一年內無重大事故再重跑研究","how_monitor":"NHTSA 調查與召回公告、公司無人營運安全報告、營運城市數與營運時段是否收縮","probability":"15%～25%（12～24 個月）：無人里程每週雙位數成長、正擴到 24 小時與高速路段，曝險快速放大；Musk 自承任何傷人事件都會招致監管收緊"}},"appendix_a":{"growth_durability":5,"quality_score":4,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":172.3,"peg_fy2":4.94,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":1.08,"FY2026E":1.77,"FY2027E":2.16,"FY2028E":3.22},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS 1.08 美元（事實表只有此口徑）；FY2026E～FY2028E 為 Koyfin 共識，是否為調整後口徑事實表未涵蓋，兩者可能不同口徑，三年成長率以 FY2026E→FY2028E 兩年年化約 35% 為準"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSLA_20261024/scenario.json","archetype":{"primary":"轉機/特殊情境","secondary":"循環/商品","confidence":"中","fingerprint":"EPS 由 2023 年 4.31 美元降到 2025 年 1.08 美元、營業利益率由 17% 降到最新一季 2.6%，價值押在無人車、Optimus、儲能能否商業化"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉為主：Q3 交付超預期多篇歸因高油價與庫存去化，交付高於產量約 2.2 萬輛；美國稅收抵免結束後 EV 零售占比降 3.6 點至 6.2%；同業營業利益率 GM 0.98%、Ford −3.74%、BYD 5.25%，產業利潤收縮","bargaining":{"up":"上游偏強：管理層稱電池產能是全球量產限制，記憶體在高價下靠 Micron 配額，中國稀土磁鐵需出口許可","down":"直營無經銷商、終端定價自主，但需以融資補貼抵銷利率上升，汽車硬體議價力有限；FSD 訂閱是定價力最強的一段","geo":"中國與德國設廠緩衝汽車關稅；要求供應商把顯示器、ECU、PCB 移出中國與台灣；關稅對儲能電芯成本衝擊大於汽車"},"profit_pool_dir":"汽車利潤池由硬體移向軟體與服務（FSD 訂閱、Robotaxi），硬體端被中國品牌與價格戰擠壓；儲能利潤受關稅與工業儲能均價下滑影響","tam_table":[{"item":"美國 EV 市場 Q3 2026 銷量","value":"262,649 輛，Tesla 約 144,094 輛、份額約 54%（Cox 估計）"},{"item":"全球 BEV 份額 2026Q2","value":"Tesla 13%（Q1 11%），BYD 約 12%（Counterpoint）"},{"item":"西歐 18 國份額 2026Q2","value":"Tesla 2.6%（去年同期 1.7%），中國品牌合計 10.7% 創新高"},{"item":"美國 EV 零售占比","value":"稅收抵免結束後降 3.6 點至 6.2%（J.D. Power 引 Reuters）"},{"item":"儲能部署","value":"2025 年 46.7 GWh；2026 年前三季 8.8＋13.5＋13.7 GWh；管理層稱 2027 年 Megapack 幾乎售罄"},{"item":"Robotaxi 與 Optimus 的市場規模及利潤池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"車隊資料規模加垂直整合：全車隊資料訓練 FSD、自產 LFP 電芯與自研晶片、Cybercab 零件數少 50%、直營與自有超充網","execution":7,"pricing":5,"combined":6,"score":6,"grade":"C","trend":"→","trend_evidence":"執行力擴大（FSD 附加率約 55%→逾 75%、付費客戶近 150 萬→逾 170 萬、Cybercab 量產），定價權縮減（汽車毛利率 2022 年 25.6%→2025 年 18.03%、法規積分萎縮、融資補貼增加），合計持平；營業利益率仍低於 BYD，不足以標擴大","threats":[{"level":"🔴","text":"中國品牌在西歐份額創 10.7% 新高、BYD 全球 BEV 份額 12% 逼近；10-K 自承競爭加劇可能導致降價與份額流失","p":"35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]},{"level":"🔴","text":"Waymo 以光達＋雷達＋相機路線領先無人車部署規模，Zoox、Uber 與 Lucid、Nuro 陸續進入；若多感測器路線先取得監管信任，純視覺路線的成本優勢換不到市場","p":"40%","evidence_refs":["competitive_share_entrants#5","substitute_technology#0"]},{"level":"🟡","text":"其他車廠借 Nvidia 或 Qualcomm 方案推出 L2+ 產品，壓低 FSD 訂閱價格（2026-10-21 法說 RBC 提問）","p":"30%","evidence_refs":[]},{"level":"🟡","text":"中國反壟斷民事訴訟指控限制獨立維修商取得維修軟體，若成立將削弱售後服務的封閉性","p":"15%","evidence_refs":["regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"低利益率×低周轉（周轉率事實表未涵蓋，以重資本擴張判讀）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"個人購車時使用者、決策者、付款者重合，需求成立；但有週期成分：Q3 超預期部分歸因高油價，美國稅收抵免結束後 EV 零售占比降到 6.2%。訂單積壓四年最高、交付高於產量約 2.2 萬輛是正面讀數"},{"item":"決策層級","level":"🟡","text":"FSD 為月訂閱，客戶隨時可退，轉換成本低；流失率管理層承諾日後揭露但目前未給。北美逾 75% 交車簽付費訂閱（每車已含一個月免費仍簽），是黏著度的初步代理"},{"item":"價值鏈分配","level":"🟡","text":"電池電芯與記憶體是瓶頸：管理層稱電池產能限制量產，記憶體在高價下靠 Micron 配額；儲能已開始用自產 LFP 電芯出貨，收回部分價值，但上游議價力仍偏強"},{"item":"社會容忍度","level":"🔴","text":"Robotaxi 能否營運取決於監管授權：NHTSA 正評估學區超速請願並查詢 Cybercab 無踏板的自我認證，Musk 自承任何傷人事件都會招致監管收緊，也說除非被政府擋下才能拿下多數客運里程。授權可被收回，是定價上限的政策風險，已列入反證紀錄"}],"roiic":"負值（推估）：2022→2025 年營收增約 134 億美元，營業利益由約 138 億降到約 48 億美元，減約 90 億；投入資本與 D&A 事實表未涵蓋，無法算精確值","reinvest_rate":"遠高於 100%：2026 年資本支出約 200 億美元（2026-10-21 CFO），對照 TTM 營業利益率 4.61%、Q3 營業利益 7.18 億美元；D&A 與營運資金變動事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率；增量報酬為負時內生上界沒有意義，留空白，共識成長全部要靠新事業的利潤率擴張"},"spread_table":[{"metric":"毛利率","TSLA":18.85,"GM":5.74,"F":2.22,"1211.HK":17.76,"RIVN":7.51,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","TSLA":4.61,"GM":0.98,"F":-3.74,"1211.HK":5.25,"RIVN":-60.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","TSLA":5.55,"GM":0.33,"F":3.87,"1211.HK":-6.5,"RIVN":-59.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","TSLA":7.46,"GM":null,"F":null,"1211.HK":6.75,"RIVN":30.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"GM","gm":5.74,"om":0.98,"fcf_margin":0.33,"rd_intensity":null,"strategy_note":"毛利率 5.74%、營業利益率 0.98%，電動化拖累利潤，成本上不構成威脅，但可外購 L2+ 方案在輔助駕駛上追趕","period":"TTM ending 2026-06-30（4季加總）"},{"name":"F","gm":2.22,"om":-3.74,"fcf_margin":3.87,"rd_intensity":null,"strategy_note":"營業利益率 −3.74%，價格戰承受力最弱，對 Tesla 定價的壓力有限","period":"TTM ending 2026-06-30（4季加總）"},{"name":"1211.HK（BYD）","gm":17.76,"om":5.25,"fcf_margin":-6.5,"rd_intensity":6.75,"strategy_note":"毛利率 17.76% 接近 Tesla、營業利益率 5.25% 反而較高，FCF 利潤率 −6.5% 顯示擴產激進，是份額與成本上最強的對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"RIVN","gm":7.51,"om":-60.05,"fcf_margin":-59.31,"rd_intensity":30.61,"strategy_note":"營業利益率 −60%、FCF 利潤率 −59%，規模未成，短期無威脅","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主：汽車交付年減 2%、儲能部署年增 10%、服務及其他年增 33%；價格面法規積分萎縮、融資補貼增加；無併購、無回購","runway_years":"事實表未涵蓋（全球滲透率資料缺）","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬為負（2022→2025 營收增約 134 億美元、營業利益減約 90 億），內生上界無法支撐共識 FY2026E→FY2028E 年化約 35% 的 EPS 成長；缺口歸因利潤率擴張，無法用既有資本報酬驗證，依賴新事業與重新評價","segments":[{"item":"汽車","value":"Q3 約 206 億美元，年減約 3%；GAAP 毛利率 18.5%，不含積分 18.1%"},{"item":"能源發電與儲能","value":"Q3 約 29 億美元，年減 16%；部署 13.7 GWh 年增 10%；毛利率 33.1%（含關稅退款與保固分攤）"},{"item":"服務及其他（含 Robotaxi）","value":"Q3 約 46 億美元，年增 33%；毛利率 15.9% 創新高"}],"decay_signals":["EPS 成長遠高於營收成長：共識 FY2026E→FY2028E EPS 年化約 35%，營收本季年持平","市場規模壓縮：美國稅收抵免結束後 EV 零售占比降 3.6 點至 6.2%"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"公司未配息、未回購，成長靠自有資本支出而非併購，沒有股東回饋紀錄可展開"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無重大併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"公司不回購、不配息","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 單季 11.65 億美元、占營收約 4.15%；稀釋股數序列事實表未涵蓋，淨稀釋率無法計算","grade":"不過"}]},"valuation":{"basis":"Fwd P/E（FY2026E 共識 EPS）","peers":{"expanded":false,"reason":"事實表未收同業前瞻倍數；GM、Ford、BYD、Rivian 只有利潤率，不能當倍數錨"},"fwd_pe":210.29,"peg":6.03,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"Fwd P/E 210 倍、FY2027E 172 倍，PEG 約 6（共識兩年年化約 35%），遠高於 2 的偏貴線；基本情境五年終點低於現價","upside_short_pct":9.6,"upside_mid_pct":-18.7},"trap_analysis":{"verdict":"🟡","label":"新事業故事撐估值、本業利潤收縮，陷阱風險中"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"無人車被監管或事故卡住：NHTSA 評估學區超速請願（期限約 2027-01-21）並查詢 Cybercab 自我認證、FSD 調查延長、2026 年多起召回；10-K 稱若主管機關日後採取行動，可能面臨責任、罰款與限制性制裁","assumption":"多頭假設監管會跟著安全數據放行，2027 年 Q2 起開放客戶車輛加入車隊","consequence":"無人車營收延後兩年以上，估值回到車廠加儲能，倍數向 35 倍收斂，五年後股價約 70～80 美元","ruling":"採納：這是五年後虧五成最可能的故事，與唯一致命事件部分重疊（致命事件是其中最尖銳的一種），Bear 機率 30% 反映此路徑；社會容忍度判紅記在這裡","watch":"NHTSA 立案與召回公告、無人營運城市數與營運時段是否收縮","evidence_refs":["regulatory_antitrust#0","major_events#3","major_events#5","product_recall_warning#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Cybercab 主要由 Tesla 自有、以運輸服務營運，車隊要用資產負債表買；Terafab 長期逾千億美元、與 SpaceX 的分攤未定；SpaceX 合併只成立委員會；2018 年 CEO 獎勵訴訟判撤銷並付律師費 3.45 億美元，治理爭議未了","assumption":"無人車成功後利潤直接流到股東，不被資本支出與關係人交易吃掉","consequence":"營收與里程成長，但自由現金流長期為負、需借款或換股，每股價值成長遠低於業務成長","ruling":"採納：Bull 情境 EPS 不給到業務成長的幅度，並把合併條款列入複審事件","watch":"年度自由現金流、信貸額度動用、合併換股比例","evidence_refs":["capital_markets_pricing#0","lawsuit_class_action#1","major_events#1","major_events#0"],"fact_refs":["f_kpi4_gaap","f_kpi5_sbc"]},{"view":"價格已反映太多","evidence":"Fwd P/E 210 倍、FY2027E 172 倍；Q3 營收年持平、汽車營收年減約 3%；基本情境五年終點約 303 美元","assumption":"市場把管理層時程當成基本情境","consequence":"即使業務照基本情境走，五年報酬仍為負","ruling":"採納：這是本次不建倉的主因","watch":"股價對 FY2027E 共識的倍數，回到約 115 倍（約 250 美元）重新評估","evidence_refs":["end_markets#0"],"fact_refs":["f_fwd_pe_latest","f_price_at_dd","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"10-K：2025 年關稅調升與報復措施已推高供應鏈成本，汽車銷售成本下降被關稅部分抵銷；中國稀土磁鐵出口許可曾延誤 Optimus 關鍵零件","assumption":"量產擴大時零組件成本可控","consequence":"交付成長但毛利率被成本吃掉，Optimus 量產時程再延","ruling":"部分採納：中國與德國設廠能緩衝汽車關稅，但儲能與 Optimus 的零組件曝險較大；不預測關稅走向，以毛利率單季下滑≥2 個百分點作吸收失敗判定","watch":"汽車與能源毛利率、稀土出口許可消息","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#1"],"fact_refs":[]}],"max_dd":{"lo":-82,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 393.45 → 本次 372.22（-5.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=393.45","side_b":"本次 price_at_dd=372.22","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 迴避 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=迴避","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份裁決：護城河趨勢 ↓→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 不持有/迴避 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=不持有/迴避","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 B→C、護城河趨勢 ↓→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 393.45 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 393.45 美元：Bull 價 660、Bear 價 91，五年期望值 −12.0%，基準年化 −2.7%，不對稱比 0.7","side_b":"本次情境、股價仍用 393.45 美元：Bull 價 840、Bear 價 73.5，五年期望值 −6.4%，基準年化 −5.1%，不對稱比 1.16","ruling":"先換情境、股價不動：五年期望值多 5.6 個百分點，基準年化少 2.4 個百分點。不對稱比由 0.7 變為 1.16。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 393.45 美元：五年期望值 −6.4%，基準年化 −5.1%，不對稱比 1.16","side_b":"本次情境、股價 372.22 美元：五年期望值 −1.1%，基準年化 −4.1%，不對稱比 1.3","ruling":"再換股價、情境不動：起點價下跌 5.4%，五年期望值多 5.3 個百分點，基準年化多 1.1 個百分點，不對稱比由 1.16 升到 1.3。合計五年期望值比前份多 10.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"價格與估值","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份：股價 393.45 美元，估值偏貴，不持有並迴避；Bull 機率 25%、Bear 30%","side_b":"本次：股價 372.22 美元（−5.4%），Fwd P/E 仍約 210 倍，估值結論不變；Bull 25%、Bear 30% 不變","ruling":"跌幅不足以改變估值結論，機率不動；裁決與角色由本次輸入重新路由，價格變動本身不構成改判理由","evidence_level":"事實表股價與共識","settle_metric":"股價對 FY2027E 共識的倍數","if_then":["若股價跌到 250 美元以下而 H1～H3 無損：重跑研究後分批反買小額","反向：若股價續漲而無人車營收仍未揭露：不追"],"evidence_refs":[]},{"axis":"公司類型、綜合評級與回撤區間","cause":"方法變動","prior_field":["archetype","signal","cycle_position","max_dd_pct"],"side_a":"前份歸為品質複利成長，綜合評級 B，最大回撤 −65%（單點），循環位置空白","side_b":"本次改歸轉機／特殊情境（次類循環），綜合評級 C，回撤區間 −50%～−82%，循環位置仍空白","ruling":"EPS 由 2023 年 4.31 美元降到 2025 年 1.08 美元、營業利益率由 17% 降到最新一季 2.6%，增量報酬為負，不符合品質複利的定義；價值押在新事業能否商業化，屬轉機型，品質項連帶降一級。回撤改為區間，下緣加深是因 Bear 終點約 74 美元，區間必須涵蓋該跌幅。循環位置對轉機型不適用，維持空白","evidence_level":"事實表年度財報","settle_metric":"年度營業利益率與 EPS","if_then":["若 2027 年營業利益率回到 9% 以上且 EPS 超過 2023 年水準：改回品質複利評估","反向：若 2027 年營業利益率仍低於 5%：維持轉機型與 C 級"],"evidence_refs":[]},{"axis":"護城河方向、陷阱與跑道","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河方向向下，陷阱風險中，五年後跑道中","side_b":"本次：護城河方向改為持平，陷阱風險與跑道維持中","ruling":"改持平的依據：北美 FSD 交車附加率由約 55% 升到逾 75%、全球付費客戶由近 150 萬升到逾 170 萬、FSD 年化經常性營收約 10 億美元（CFO 確認）、美國 EV 份額約 54%、全球 BEV 份額 13% 高於 BYD；毛利率自 2023 年起穩在 18% 上下，略高於 BYD 的 17.76%。但營業利益率仍低於 BYD（4.61% 對 5.25%），硬體定價權沒有恢復，所以只升到持平、不升到擴大。陷阱與跑道的證據方向未變","evidence_level":"公司法說與第三方份額統計","settle_metric":"北美 FSD 附加率與對 BYD 營業利益率差距","if_then":["若 FSD 附加率回落到 55% 以下或全球 BEV 份額連兩季低於 11%：護城河方向改回向下","反向：若營業利益率連兩季超過 BYD：考慮改為擴大"],"evidence_refs":["channel_business_model_shift#1","end_markets#3","competitive_share_entrants#2","competitive_share_entrants#4"]},{"axis":"重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE 回落至 ~80x（約 $200）＋7/22 Q2 財報 Auto GM ex-credit ≥19% 且非折價驅動＋中國重回前 10 連 2 季；三者齊備才重啟完整 DD","side_b":"股價≤250 美元（約 FY2027E 共識 115 倍）且汽車毛利率不含積分連兩季≥17%；或 Robotaxi 營收單獨揭露且年化≥50 億美元","ruling":"舊條件中「中國重回前 10」在本包沒有可驗證的資料來源，改用真正決定估值的無人車營收取代；毛利門檻由 19% 改 17%，因 Q2 落到 16.3%、Q3 回到 18.1% 靠亞太組合，17% 才是扣除一次性後的中樞；價位改用 FY2027E 共識 2.16 美元的 115 倍約 250 美元。觸發後只重啟完整研究，不直接加碼","evidence_level":"法說會與事實表共識","settle_metric":"股價、汽車毛利率、Robotaxi 營收揭露","if_then":["若任一條件成立：重跑完整研究，首筆僅小額","反向：若條件成立前出現監管暫停無人營運：重啟條件作廢"],"evidence_refs":[]},{"axis":"kill 指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill 指標（空白）","side_b":"汽車毛利率不含積分連兩季<16%；能源毛利率扣除一次性<20%；自由現金流連兩季為負且動用新信貸；2027 年底無人營運<10 城或遭暫停","ruling":"新設：對持有者是減碼與清倉的依據，對本檔（不持有）是重啟評估的否決條件，任一觸發即取消重啟評估","evidence_level":"季度財報口徑","settle_metric":"各 kill 指標季度讀數","if_then":["若兩項以上同時觸發：持有者清倉","若僅一項觸發：持有者減碼一半並凍結加碼"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設定 Single Thing（空白）","side_b":"Single Thing：無人監督 Robotaxi 或 Cybercab 車隊發生致死或重傷事故，監管機關因此暫停或限制無人營運","ruling":"新設 Single Thing：Cybercab 已無人營運並快速擴車，NHTSA 學區超速請願與 Cybercab 認證查詢都是 2026-10 的新證據；這是估值最大的單一敏感項，發生時持有者清倉","evidence_level":"監管公告與法說會","settle_metric":"NHTSA 調查與召回公告","if_then":["若發生：持有者清倉，重啟條件作廢","反向：若 2027 年底前擴到 24 小時與高速路段仍無重大事故：Bear 機率下調 5 個百分點"],"evidence_refs":["major_events#3","product_recall_warning#0"]},{"axis":"論點門檻","cause":"新證據","prior_field":["thesis.H"],"side_a":"前份：H1 2027 底無人監督車隊>1,000 台且營運≥5 城；H2 FY2026 汽車毛利率不含積分全年≥18%；H3 能源部署年化≥40 GWh、營收年增>25%","side_b":"本次：H1 2027 年底 FSD 付費客戶≥250 萬且無人營運≥10 城；H2 汽車毛利率不含積分每季≥17%、FY2027 交付≥185 萬輛；H3 2027 年部署≥60 GWh 且扣除一次性毛利率≥22%","ruling":"H1 改用付費客戶與城市數，因管理層不揭露車隊台數（2026-07-22 被問時迴避），舊門檻無法驗證。按舊門檻 H3 本季已不成立（能源營收年減 16%），H2 前三季約 17.9% 也在邊緣，兩者記為削弱，不因改門檻而抹掉；新門檻改看部署量與扣除一次性的毛利率，是因營收增速被關稅退款扭曲","evidence_level":"季度財報與法說會","settle_metric":"各假設門檻的季度讀數","if_then":["若新門檻連兩季未達：該假設改判反轉，減碼條件成立","反向：若 2027 年三項同時達標：重啟研究"],"evidence_refs":["end_markets#1"]},{"axis":"需求：管理層說法與數字","cause":null,"prior_field":null,"side_a":"管理層：需求快速成長、明顯超過產量，訂單積壓四年最高（Musk、CFO，2026-10-21 法說）","side_b":"數字：Q3 交付 486,532 輛年減 2%、營收年持平、汽車營收約 −3%；交付比產量多約 2.2 萬輛，靠庫存去化；超預期部分歸因高油價；共識交付在 2026 年 3 月曾被下修","ruling":"不可調和（方向相反），採數字側：積壓與交付超產量只說明短期供不應求，年比仍在下滑，且部分需求來自油價這種週期因素；交付恢復年增前不採信需求快速成長","evidence_level":"公司公告交付與第三方報導","settle_metric":"Q4 2026 與 2027 上半年交付年增率","if_then":["若 2027 上半年交付年增≥10% 且汽車毛利率不含積分≥17%：承認需求轉強，進入重啟評估","反向：若 Q4 2026 交付年減且交付低於產量：H2 削弱，維持不建倉"],"evidence_refs":["end_markets#0","capital_markets_pricing#2","supply_demand_durability#0"]},{"axis":"能源毛利率：前後說法","cause":null,"prior_field":null,"side_a":"CFO 2026-07-22：儲能長期毛利率在 20% 出頭到中段；Musk 2026-10-21：毛利率會明顯上升","side_b":"Q3 能源毛利率 33.1%，CFO 自承主要來自關稅退款與供應商保固分攤；能源營收年減 16%，部署 13.7 GWh 低於分析師約 15.9 GWh","ruling":"管理層一次性歸因不採信也不否定，標「未證、監測」：以 CFO 先前給的 20% 出頭為基準，扣除一次性後連兩季≥25% 才承認改口成立","evidence_level":"法說會原話與第三方財報整理","settle_metric":"扣除一次性後的能源毛利率","if_then":["若 Q4 2026 與 Q1 2027 扣除一次性後≥25%：H3 加強","反向：若任一季<20%：H3 削弱並觸發 kill 指標"],"evidence_refs":["end_markets#1","reg_tariff_export#1"]},{"axis":"資本支出與現金流","cause":null,"prior_field":null,"side_a":"2026-04 財報後資本支出指引上調至至少 250 億美元並預期年內其餘時間自由現金流為負；2026-07-22 CFO 稱未來兩三年持續成長","side_b":"2026-10-21 下修本年資本支出至約 200 億美元、Q3 自由現金流逾 15 億美元；同時 Terafab 至 2028 年初投入數百億、長期逾千億美元，並簽 300 億美元信貸額度","ruling":"可調和（程度差異）：今年下修是時點遞延不是規模縮小，2027～2028 年支出仍上升；本季自由現金流扣掉 SBC 後只剩約 3.7 億美元，現金創造不足以自行支應","evidence_level":"法說會與 8-K","settle_metric":"2027 年資本支出指引與季度自由現金流","if_then":["若 2027 年自由現金流連兩季為負並動用新信貸：kill 指標觸發，取消重啟評估","反向：若 2027 年資本支出逾 300 億美元而自由現金流仍為正：上調 Base 情境現金流假設"],"evidence_refs":["capital_markets_pricing#0","major_events#1"]},{"axis":"無人車規模：說法與揭露","cause":null,"prior_field":null,"side_a":"管理層：無人里程每週雙位數成長、未來數月可擴到數百萬輛、2027 年無人車成為營收與獲利的重要部分","side_b":"未揭露車隊車輛數（2026-07-22 被問車隊規模時迴避）；營運市場由 Q2 稱的 7 個變成 Q3 的 6 個城市；每英里成本未達 0.30 美元目標；Musk 自稱本季不影響數字、2027 下半年才明顯","ruling":"不可裁決至 2027 年 Q2 財報：目前沒有車隊數、付費里程或營收，證據時間窗蓋不到估值所需的風險窗，不得把指數成長當成已證實","evidence_level":"法說會原話","settle_metric":"Robotaxi 營收或付費里程揭露","if_then":["若 2027 年 Q2 前揭露 Robotaxi 營收且年化≥50 億美元：重啟研究","反向：若 2027 年 Q2 仍未揭露任何營收或車隊數：H1 削弱，Bull 機率下調"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"多方：FSD 年化經常性營收約 10 億美元且附加率快速攀升、Cybercab 零件少 50%、Megapack 2027 年幾乎售罄、現金與投資逾 450 億美元；若無人車照時程在 2027 年成為主要利潤，現在的 EPS 是谷底","side_b":"本方：即使採基本情境 2031 年 EPS 5.5 美元，55 倍終端倍數只值約 303 美元，低於現價；要回到現價須假設 EPS 約 6.8 美元以上，等於把多頭情境當基本情境","ruling":"可調和（程度差異），採本方：分歧在時程與量級，不在方向。現在不追","evidence_level":"事實表共識與情境推算","settle_metric":"Robotaxi 營收揭露與股價對 FY2027E 倍數","if_then":["若股價≤250 美元而 H1～H3 無損：重跑研究後分批反買小額","反向：若 2027 年 Q2 前 Robotaxi 營收年化≥50 億美元而股價未同步上漲：放棄等價位，直接重啟研究"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FSD 付費客戶與無人營運城市是否達標","type":"假設驗證","maps_to":"H1","metric":"FSD 全球付費客戶數；無人監督營運城市數","threshold":"2027 年底≥250 萬且≥10 城","action":"達標且價位條件成立→重跑完整研究；落後→維持不建倉","source_freq":"季度更新簡報與法說會","date":"2027-12","evidence_refs":["channel_business_model_shift#1"]},{"n":2,"text":"汽車毛利率守住 17%","type":"假設驗證","maps_to":"H2","metric":"汽車毛利率（不含法規積分）","threshold":"每季≥17%；連兩季<16.2% 為削弱","action":"連兩季<16.2%→取消重啟評估","source_freq":"季度更新簡報","date":"2027-01","evidence_refs":["end_markets#0"]},{"n":3,"text":"能源毛利率扣除一次性後的真實水準","type":"假設驗證","maps_to":"H3","metric":"能源毛利率（扣除關稅退款與保固回沖）；年度部署量","threshold":"單季≥22%；2027 年部署≥60 GWh","action":"單季<20%→H3 削弱並列入 kill 指標","source_freq":"季度更新簡報與法說會","date":"2027-01","evidence_refs":["end_markets#1","reg_tariff_export#1"]},{"n":4,"text":"NHTSA 是否就學區超速請願正式立案","type":"風險","maps_to":"R2","metric":"NHTSA 立案決定與範圍","threshold":"正式立案或要求暫停無人營運","action":"立案→凍結重啟評估至調查範圍明朗；持有者減碼一半","source_freq":"NHTSA 公告，事件型","date":"2027-01-21","evidence_refs":["major_events#3","product_recall_warning#0"]},{"n":5,"text":"無人車隊致死或重傷事故導致監管暫停","type":"Single Thing","maps_to":"Single Thing","metric":"監管暫停或限制無人營運","threshold":"任一州或聯邦層級暫停","action":"持有者清倉；重啟條件作廢","source_freq":"監管公告與公司聲明，事件型","date":null,"evidence_refs":["major_events#3"]},{"n":6,"text":"價位或無人車營收到位才重啟研究","type":"估值rearm","maps_to":"rearm","metric":"股價；汽車毛利率；Robotaxi 營收","threshold":"股價≤250 美元且汽車毛利率連兩季≥17%；或 Robotaxi 營收年化≥50 億美元","action":"重跑完整研究，首筆僅小額","source_freq":"每日股價、季度財報","date":null,"evidence_refs":[]},{"n":7,"text":"SpaceX 合併條款公布","type":"風險","maps_to":"R4","metric":"換股比例、稀釋幅度、Terafab 成本分攤","threshold":"條款公布，或換股稀釋逾 10%","action":"公布→重跑估值與稀釋試算；稀釋逾 10% 且無對價說明→持有者減碼","source_freq":"8-K 與公司公告，事件型","date":null,"evidence_refs":["major_events#0","ma_merger#0"]},{"n":8,"text":"Q4 2026 財報後複審","type":"複審日期","maps_to":"全部假設","metric":"交付、汽車與能源毛利率、2027 資本支出指引","threshold":"財報公布","action":"逐項對照 H1～H3 與 kill 指標","source_freq":"季度","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"汽車毛利率（不含法規積分）","bear_threshold":"連兩季<16%","window":"2027 年內","source":"季度更新簡報與法說會","last_status":"ok"},{"metric":"能源毛利率（扣除關稅退款與保固回沖）","bear_threshold":"任一季<20%","window":"2026Q4～2027Q4","source":"季度更新簡報與法說會","last_status":"unknown"},{"metric":"季度自由現金流（公司口徑）","bear_threshold":"連兩季為負且動用新信貸額度","window":"2027～2028","source":"季度更新簡報、8-K","last_status":"ok"},{"metric":"無人監督營運城市數","bear_threshold":"2027 年底<10 城或遭監管暫停","window":"至 2027-12","source":"法說會與公司公告","last_status":"warning"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把管理層的無人車與 Optimus 時程當成基本情境：FY2027E 共識 2.16 美元仍約 172 倍，以 55 倍終端倍數倒推須 2031 年 EPS 約 6.8 美元，而管理層自承無人車營收要到 2027 下半年才明顯、目前未揭露車隊數"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=-1.08, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價≤250 美元（約 FY2027E 共識 115 倍）且汽車毛利率不含積分連兩季≥17%；或 Robotaxi 營收單獨揭露且年化≥50 億美元","exec_line":"現價不建倉；任一重啟條件成立後先重跑完整研究，首筆僅小額試單，不追價"},"reasoning":{"industry":"分部（Electrek 2026-10-21 引 Q3 財報）：汽車約 206 億美元（約 73%，年減約 3%，法規積分由 4.17 億降到 1.13 億美元）、能源約 29 億美元（約 10%，年減 16%）、服務及其他約 46 億美元（約 16%，年增 33%，含超充、保險與 Robotaxi）。汽車 GAAP 毛利率 18.5%，不含積分由上季 16.3% 升到 18.1%，CFO 歸因亞太交車占比提高；能源毛利率 33.1% 含關稅退款與供應商保固分攤。交付 486,532 輛、儲能部署 13.7 GWh，公司不給量化指引。單點依賴：電池電芯產能是整車量產限制，記憶體靠 Micron 配額，稀土磁鐵受中國出口許可影響；客戶端為個人與電網客戶，10-K 集中度附註待核，未見單一客戶達 10% 的揭露。產業時鐘判收縮期：GM、Ford、Rivian 的營業利益率分別為 0.98%、−3.74%、−60%，BYD 5.25%，美國稅收抵免結束後 EV 零售占比降到 6.2%，產業利潤在收縮。供需持久性：週期性將反轉為主，Q3 交付超預期多篇歸因高油價與庫存去化，屬可逆的順風。產業態勢為雙向拉鋸：競爭惡化（中國品牌西歐份額創 10.7% 新高、Waymo 無人車規模領先）對結構轉好（FSD 改為純訂閱、儲能資料中心需求），其他結構變數為關稅與無人車監管。","moat":"機制是車隊資料規模加垂直整合：FSD 以全車隊資料訓練端到端模型，Cybercab 零件比過去任何車款少 50%，直營通路與自有超充網。可證方向：對最強同業 BYD，TTM 毛利率 18.85% 對 17.76% 小幅領先，但營業利益率 4.61% 對 5.25% 落後，報酬差距為負；對 GM、Ford、Rivian 則大幅領先。份額面 Q2 全球 BEV 13% 高於 BYD 12%、美國 EV 約 54%。執行力 7 分：北美 FSD 交車附加率由約 55% 升到逾 75%，全球付費客戶逾 170 萬，Cybercab 已量產。定價權 5 分：汽車毛利率由 2022 年 25.6% 降到 18% 上下後持平，需以融資補貼抵銷利率，法規積分萎縮；FSD 訂閱是唯一在變強的定價點，但其他車廠可能用 Nvidia、Qualcomm 方案追上並壓低價格（2026-10-21 法說 RBC 提問，管理層只說問題很難，未給數字反駁）。綜合 6 分。當期 ROIC 偏低：稅後營業利益率不到 4%，投入資本周轉率事實表未涵蓋。","growth":"成長來源以量為主：交付年減 2%、儲能部署年增 10%、服務及其他年增 33%；價格面法規積分萎縮、融資補貼增加；無併購、無回購。共識 EPS FY2026E 1.77、FY2027E 2.16、FY2028E 3.22 美元（Koyfin 快照，家數事實表未涵蓋），兩年年化約 35%；近 3 個月 FY1 下修 0.56%，本期 FY2、FY3 各下修 1.37%、2.42%。內生上界：增量報酬為負，既有資本報酬撐不起任何成長，缺口全部歸因於利潤率擴張（研發投入回收、無人車與 FSD 高毛利），信心上限中。跑道：Tesla 在美國 EV 份額約 54%，介於 35%～70%；無人車管理層稱 2027 年 Q2 起才明顯、Optimus 對外交貨約 2027 年底、Terafab 量產晶片約 2028 年，都還不是已證實的第二曲線，所以不給寬跑道。衰退信號亮兩個：EPS 成長遠高於營收成長、美國 EV 零售占比下滑。","governance":"現金去向：本年資本支出約 200 億美元（2026-04 曾指引至少 250 億），未來幾年持續擴大到 Robotaxi 車隊、Optimus 產能、太陽能、AI 算力與晶圓廠；Terafab 至 2028 年初投入數百億、長期逾千億美元，與 SpaceX 的分攤未定。期末現金與投資逾 450 億美元，2026-09-29 簽 200 億美元延遲提款定期貸款與合計 100 億美元循環額度，今年不動用。SBC 單季 11.65 億美元，占營收約 4.15%。併購：無重大併購，不適用；回購：公司不回購，不適用；淨稀釋率：股數序列事實表未涵蓋，無法判定。治理：2018 年 CEO 績效獎勵遭判撤銷、原告律師費 3.45 億美元；SpaceX 合併只成立特別委員會，條款未定。FCF 對淨利轉換率的年度序列事實表未涵蓋。","valuation":"Fwd P/E 210 倍（FY2026E 共識 1.77 美元），以 FY2027E 計 172 倍；PEG 約 6（FY2026E→FY2028E 共識年化約 35%）。五年估值分位：事實表只有近期一點，不外推，留空白。分母受研發與折舊壓低，但即使把營業利益率還原到 2023 年的 9.19%，獲利約翻倍，倍數仍逾百倍，分母不是爭點。賣方平均目標價約 408 美元（2026-09 初，非最新），較現價高 9.6%；目標價全距 25～600 美元，最高對最低逾 20 倍，分歧極大，下調對自身情境的信心。基本情境五年終點約 303 美元，較現價低 18.7%。同業前瞻倍數事實表未涵蓋，不跨類比較。","premortem":"反方最強數字：FSD 年化經常性營收約 10 億美元、北美附加率季增約 20%、無人里程每週雙位數成長、Cybercab 產線額定年產逾 12.5 萬輛且可再提高、Megapack 2027 年幾乎售罄。我方會看錯的條件見反證紀錄。動能中性：26 週報酬 −1.08%、RSI 51.5、週線均線排列過但長均線走平；近三個月共識小幅下修。上一季法說有四處未正面回答（車隊規模、儲能資料中心占比、Optimus 4 量產時程、SpaceX 合併），都是估值關鍵資訊。歷史最大回撤事實表未涵蓋；空方最低目標價 25 美元屬賣方個例。"},"plain":{"six":{"how_it_makes_money":"賺的是買車的人和電網、資料中心客戶的錢，錢卡在汽車硬體毛利：Q3 營收 280.5 億美元年持平，GAAP 營業利益率只有 2.6%，研發與折舊把汽車毛利幾乎吃光","moat":"護城河方向持平：汽車硬體定價權仍在流失，但 FSD 訂閱附加率與車隊資料規模擴大，兩者抵銷；綜合等級 C","growth":"五年後跑道中：汽車本業在美國 EV 份額已逾五成，無人車與 Optimus 還沒有營收證據，儲能營收本季年減 16%","capital":"資本配置偏弱：進入大投資期，本季自由現金流 15.31 億美元扣掉 SBC 後只剩約 3.7 億美元，無回購無股息，還有 SpaceX 合併與 Terafab 分攤的關係人問題","valuation":"現價要市場相信無人車與 Optimus 照管理層時程兌現：以 55 倍終端倍數倒推，2031 年 EPS 須達約 6.8 美元，是基本情境的 1.2 倍。我不信這是基本情境","how_wrong":"最可能看錯在無人車速度：若 Robotaxi 在 2027 年真的成為主要利潤，現在的 EPS 是谷底，210 倍會被快速消化"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把管理層的無人車與 Optimus 時程當成基本情境：FY2027E 共識 2.16 美元仍約 172 倍，以 55 倍終端倍數倒推須 2031 年 EPS 約 6.8 美元，而管理層自承無人車營收要到 2027 下半年才明顯、目前未揭露車隊數","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤250 美元且汽車毛利率連兩季≥17%，或 Robotaxi 營收單獨揭露且年化≥50 億美元","trap":"🟡","val":"🔴","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"轉機/特殊情境","price_at_dd":372.22,"week26_return_pct":-1.08,"consensus_rev_3m_pct":-0.56,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母受投資期研發與折舊壓低，但把營業利益率還原到 2023 年 9.19% 後倍數仍逾百倍，結論不因分母改變"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Cybercab 在 Dallas 上線","impact":"中","watch":"上線後車隊規模與營運時段"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年資本支出指引","impact":"高","watch":"能源毛利率扣除一次性後是否≥22%、2027 年資本支出規模"},{"date":"2027-01-21","date_precision":null,"type":"regulatory","event":"NHTSA 決定是否就學區超速請願正式立案","impact":"高","watch":"立案範圍是否涵蓋暫停無人營運"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"FSD 歐盟全境核准（管理層稱不晚於 Q1）","impact":"中","watch":"核准與否及歐洲訂閱附加率"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"客戶車輛加入 Robotaxi 車隊（管理層稱約 Q2）","impact":"高","watch":"是否如期開放及首批城市"}],"_projected_from":"v19"}
```
