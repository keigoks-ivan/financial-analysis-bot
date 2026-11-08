你是 stock-analyst v20 的**散文層（prose）agent**，標的 LEU（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：LEU　日期：2026-11-08　archetype：None　前份裁決：2026-05-25　B 觀望；等估值/MA 修復至 $120-150 + DOE final agreement + Russia 2027 末 waiver 確認後再分批｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1944B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（426B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（902B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1103B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（889B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（463B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（884B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2487B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3375B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3324B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1944           3539-5056      5 條（2–6 內）  
s3                  8000         426           5302-7574      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2894          8474-12106      5 條（2–6 內）  
s6                 11000         463          7376-10537      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         884           1831-2616      5 條（2–6 內）  
s10                 5000        2487           1759-2513      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3324           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4044B；至少需散文≈40.96KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−78%
−78
−73%
−65.02%
−50
−50%
−49.55
−41.7%
−19.1%
−12.4%
−5.7%
−3.5%
−1.5%
−1.26
−1.25%
−0.13
0
0.3
0.40
0.45
0.46
0.75
0.8
0.9
$1
1
01
1.1
1.16
1.2
1.42
1.5%
1.92
1.95
2
2.27
2.4
2.42
2.6
2.7
2.8
03
3
3%
3.1
3.5
3.63
3.7
3.70
3.73
3.9
3.90
4
4.44
$4.50
4.5
4.6
4.76
4.8
5
5%
05
5.03
5.4%
06
6
6.1
7
07
7.5
7.5%
8
08
8.1
8.4
8.5%
8.5
9
09
9.83%
10%
10
10.57
11.0
11
11.4
11.79
12
13%
13
14
14.35%
14.5%
15
15.2%
16
16%
18
18.5
19%
20
20%
21%
22
22.36
23%
23.28%
23.56
24
25
25%
26
26.19%
28
28%
28.27
28.9
29
29%
30%
30
31%
31
33
35%
36
40%
41.7%
42
42%
42.42
43%
45
46%
49
49%
49.55%
50%
50
50.2%
51
54
56
57%
58.23
60%
62.6
63
70
73%
74
75%
77%
80%
90
90%
94%
95%
97.82
99
100
100%
104.6
105%
111
117%
120
$120
124
130
150
150%
157
168.5
179.36
200
200.6
207
210
227
232
250
259
286
325
340
363
365
390
460
699
2016
2023
2025
2026
2027
2028
2029
2030
2031
2032
2035
2036
2040
20261108
1,020
1,060
1,440
1,770
2,000
2,062
2,370
2,970
3,180
3,440
4,640
5,020
5,600
6,700
7,730
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
{"meta":{"ticker":"LEU","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Centrus Energy Corp."},"oneliner":"濃縮訂單與建廠進度都比半年前好，但獲利多半來自營業外項目與加回項，俄羅斯供貨與新廠總成本都未定案；股價腰斬後不算貴，也沒有安全邊際，等 12 月投資人日揭露總建置成本再決定。","thesis":{"H":[{"id":"H1","text":"Piketon 首批新增產能 2029 年底前開始商業交貨，離心機從第一台放大到連續量產。","2y":"2027 年底前 Oak Ridge 連續出貨、Piketon 開始安裝；2028 年底前首批串級完工過半。","5y":"2029 年底前首批商業交貨；FY2031 新產能營收達 5 億美元以上。","10y":"2036 年前產能爬坡完成，新增資本回報高於 10%。","threshold":"2029-12-31 前首批商業交貨，時程延後不超過 6 個月。","source":"10-Q、8-K、投資人日、NRC 與 DOE 公告","drift_rule":"里程碑連 2 季延後 6 個月以上為削弱；延到 2030 年以後為反轉。"},{"id":"H2","text":"54 億美元濃縮或有訂單能按約變現，新增訂單不靠尚無營收的開發商撐場。","2y":"2027 年底總 backlog 不低於 70 億美元，確定協議占濃縮訂單 90% 以上。","5y":"FY2031 總營收達 10 億美元。","10y":"2040 年前訂單交貨完畢，沒有重大取消。","threshold":"濃縮訂單不低於 45 億美元，確定協議占比不低於 80%。","source":"季度 backlog 揭露、10-K 客戶集中度","drift_rule":"backlog 連 2 季下滑 5% 以上為削弱；連 3 季下滑 10% 以上為反轉。"},{"id":"H3","text":"過渡期毛利守得住，自產後單位經濟轉好，每股獲利跨過股本擴張。","2y":"FY2026、FY2027 年度毛利率不低於 20%；FY2027 調整後 EPS 不低於 3.5 美元。","5y":"FY2031 EPS 不低於 7.5 美元，自由現金流轉正。","10y":"FY2036 ROIC 高於資金成本，FCF/淨利不低於 0.75。","threshold":"年度毛利率不低於 20%，FY2031 EPS 不低於 7.5 美元。","source":"10-K、10-Q、季度單位成本揭露","drift_rule":"TTM 毛利率連 2 季偏離門檻 5% 以上為削弱；連 3 季偏離 10% 以上為反轉。"}],"R":[{"id":"R1","text":"俄羅斯 TENEX 供貨在新產能上線前中斷：到 2027 年預計交貨的 LEU 逾半來自 TENEX，未承諾量豁免未定，加拿大運輸許可只到 2027 年 3 月。","h_ref":"H1","clock":"⚡","threshold":"2027-Q3 前未獲新豁免或過渡供貨合約，連 2 季觸發即砍倉。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#2"]},{"id":"R2","text":"總建置成本未揭露，資金缺口可能要低價再增資。權證要股價到 227 美元以上才會行使，Q3 自由現金流 −1.26 億美元，2027 資本投入還會加速。","h_ref":"H1","clock":"🔥","threshold":"2027 上半年實際稀釋超過 25%；或現金低於 10 億美元且 2029 首批尚未上線。","evidence_refs":["major_events#2"]},{"id":"R3","text":"競爭產能與替代技術：Urenco、Orano 擴產，General Matter、BWXT 進場，GLE 雷射濃縮目標 2030 年。","h_ref":"H2","clock":"🐢","threshold":"雷射濃縮規模化或 Urenco USA 取得 HALEU 商業執照的機率跨年度達 50% 以上即砍倉，單一新聞不觸發。","evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#4","substitute_technology#0"]},{"id":"R4","text":"單位毛利擠壓：連兩季 SWU 單位成本漲得比售價快，Q3 負毛利，調整後每股虧損遠差於共識。","h_ref":"H3","clock":"⚡","threshold":"FY2026 毛利率低於 20%，或 Q4 單位成本年增高於單價年增 10 個百分點以上。","evidence_refs":["end_markets#0","end_markets#1","cyclical_inventory_price_position#2","capital_markets_pricing#1"]},{"id":"R5","text":"DOE 不打算行使 HALEU 營運合約後續選擇權，FY2027 預算未列串級資金，示範串級轉商業的長期協議未簽。","h_ref":"H1","clock":"🔥","threshold":"2027 年中前未簽長期協議，且 Technical Solutions 季營收低於 2,000 萬美元（Q3 為 2,370 萬美元）。","evidence_refs":["end_markets#3"]},{"id":"R6","text":"濃縮與鈾週期反轉：上一輪鈾現貨低迷歷時 5–9 年，2016 年 Centrus 毛利率 14.5% 且淨損 6,700 萬美元；WNA 認為全球濃縮供給到 2030 年代初仍過剩。","h_ref":"H3","clock":"🐢","threshold":"公司 SWU 均價連 3 季年減，或鈾長約價自 99 美元回落 20% 以上。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","supply_demand_durability#1"]},{"id":"R7","text":"Westerman 收購 1.16 億美元，占市值 5.4%，管理層稱第一年增厚但利潤率未揭露，且表明可能再做併購。","h_ref":"H3","clock":"🔥","threshold":"投資人日未揭露分部利潤率，或 FY2027 累計併購超過 3 億美元而沒有已實現回報數字。","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"Piketon 首批新增濃縮產能無法在 2029 年底前開始商業交貨，公司正式把時點延到 2030 年以後。","why_fatal":"這是情境樹裡敏感度最大的一項。基本情境 FY2031 EPS 7.5 美元幾乎全靠新產能；延兩年，FY2031 EPS 約回到空頭情境的 2 美元，目標價跌幅約 73%。俄供貨中斷主要傷 FY2028–29，不是終端年。54 億美元濃縮訂單也以產能建成為前提。","if_happens":"若持有則清倉，未持有則不建倉。現金繼續燒、權證價外、訂單交期風險會同時出現。","how_monitor":"每季追 Oak Ridge 離心機產出節奏、Piketon 施工包完成數與資本投入；12 月 7 日投資人日時程表；NRC 與 DOE 公告。","probability":"未來 12–24 個月內公司正式宣布延到 2030 年以後的機率約 20%；到 2029 年底未能準時的累計機率約 35%。此為判斷值，沒有外部統計。"}},"appendix_a":{"growth_durability":6,"quality_score":4,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":23.56,"peg_fy2":58.23,"stress":{"pass":2,"total":5},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-11-07）"},"eps_meta":{"base_eps_path":{"FY2025A":3.9,"FY2026E":3.7,"FY2027E":4.44,"FY2028E":3.73},"fy_end_month":12,"eps_basis":"FY2025A 為 yfinance 稀釋 EPS；FY2026E–FY2028E 為 2026-11-07 Koyfin 共識，是否為調整後口徑事實表未註明，兩者口徑可能不同。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEU_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"長約大宗品，處於國家資助的建廠期，現有業務靠轉售俄羅斯供貨"},"industry":{"clock_phase":"II","sd_verdict_source":"依據：Q3 SWU 單價年增 10%，TradeTech 鈾長約價 99 美元創紀錄，主要新產能多在 2028–2032 才上線。供需持久性：週期性偏結構，2030 年代初起供給可逆性高；管理層說缺口擴大，WNA 說全球供給到 2030 年代初仍過剩，兩者口徑不同。","bargaining":{"up":"TENEX 是單一重大供應來源，Q3 單位成本漲幅高於售價，顯示價差目前偏向上游；Westerman 收購只處理離心機零組件，不解決 SWU 進貨。","down":"客戶以投資級電力公司為主，採購分散給四大供應商，長約至 2040；新增的反應爐開發商有預付款，但信用較弱。","geo":"俄羅斯制裁、DOE 豁免、加拿大運輸許可（至 2027 年 3 月）共同決定現有業務能否續做；美國自有技術與國安需求則是地緣上的加分。"},"profit_pool_dir":"事實表未涵蓋產業營業利益池數字。方向判斷：西方濃縮環節目前分到更多價值，2030 年代新產能疊加後可能反轉。","tam_table":{"expanded":false,"reason":"事實表未涵蓋全球 SWU 市場規模、美國份額與分段成長，只有 Centrus 全球份額不到 5%、前四大合計逾 95%；無法列表，不推估。"}},"moat":{"mechanism":"美國自有、不受外國義務限制的離心濃縮技術（管理層自述為國安用途唯一可量產方案，NNSA 2025-11 發出單一來源意向），加上長約與 DOE 固定價合約。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：第一台離心機提前完成、關鍵供應商 100% 簽約、濃縮訂單增 24 億美元。定價權縮減：Q3 單價增 10%、單位成本增 28%，西方對手與受補助新進者在 2028–2032 同期加產能。","peer_na_reason":"事實表只有同業利潤率，沒有投入資本與 ROIC；Urenco、Orano 非本表標的。","threats":[{"level":"🟡","text":"Urenco USA 現行 70 萬 SWU 擴建已過半，另有 210 萬 SWU 新廠預計 2032 首產；Orano 與 Urenco Almelo 同步增產。同產品點對點競爭，影響已計入定價權評分，不重複扣分。","p":"60%","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#4"]},{"level":"🟡","text":"General Matter 設廠、BWXT 申請執照，UBS 預期競爭壓力在 2030 年代後期累積（搜尋摘要，未核原文）。DOE 三張各 9 億美元任務單代表新進者有政府資金。","p":"40%","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#1"]},{"level":"🟡","text":"GLE 雷射濃縮目標約 2030 年首次商業生產，但此法數十年未達商業規模。目前暫列點對點，若完成商業量產且成本占優，升為架構替代並重寫論點。","p":"30%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是核電機組，決策與付款者是電力公司燃料採購；沒有濃縮鈾就不能發電，屬需要而非想要。WNA 預估 2030 年鈾需求較現在高約 28%。HALEU 需求管理層自己也說要看市場成熟與否，強度低於 LEU。"},{"item":"決策層級","level":"🟡","text":"在單一燃料合約層級，電力公司可向四大供應商分散採購，Centrus 全球份額不到 5%，鎖定靠長約而非技術轉換成本。國安且不受外國義務限制的用途替代性最低，但此塊金額未揭露。"},{"item":"價值鏈分配","level":"🟡","text":"目前 Centrus 多為轉售者，Q3 單位成本漲幅 28% 高於售價 10%，價差偏向上游。自產後分配才可能改善，但長約定價受保密條款未揭露。"},{"item":"社會容忍度","level":"🟡","text":"優勢依賴授權與政策：俄羅斯進口禁令與豁免、DOE 資金、NNSA 採購都是政策產物。FY2027 預算未列 HALEU 串級資金，Portsmouth 污染集體訴訟仍在進行。濃縮占發電成本比例事實表未涵蓋，價格上限無法量化。"}],"roiic":"無法計算：新增資本尚未產生營業利益，總建置成本未揭露。","reinvest_rate":"遠高於 100%：FY2026 資本投入指引 3.5–5 億美元，約為 FY2025 營業利益 5,020 萬美元的 7–10 倍（未扣折舊，折舊事實表未涵蓋）。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率。投入資本與增量 ROIC 都缺資料，TTM 營業利益率 −1.25%，當期 NOPAT 接近零，公式沒有意義，不硬算。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","LEU":23.28,"CCJ":25.49,"UEC":45.36,"BWXT":22.61,"unit":"%"},{"metric":"營業利益率","LEU":-1.25,"CCJ":14.35,"UEC":-357.65,"BWXT":9.83,"unit":"%"},{"metric":"FCF 利潤率","LEU":-65.02,"CCJ":10.31,"UEC":-288.16,"BWXT":10.34,"unit":"%"},{"metric":"研發密度","LEU":null,"CCJ":1.48,"UEC":null,"BWXT":0.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"CCJ","gm":25.49,"om":14.35,"fcf_margin":10.31,"rd_intensity":1.48,"strategy_note":"主業在鈾礦與燃料服務，利潤率遠高於 LEU，受惠同一輪鈾價，但不是 SWU 產能的直接對照。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"UEC","gm":45.36,"om":-357.65,"fcf_margin":-288.16,"rd_intensity":null,"strategy_note":"仍在早期放量，營業利益率極低，比較價值有限。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"BWXT","gm":22.61,"om":9.83,"fcf_margin":10.34,"rd_intensity":0.44,"strategy_note":"既有國防核燃料客戶關係，已揭露將申請新濃縮設施執照，是國安市場最值得盯的潛在對手。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"2029 年前靠價格與合約組合，2029 年後靠新產能的量；併購只有 Westerman，不是主驅動；沒有回購，股本反而擴張。","runway_years":"無法計算：事實表未涵蓋 SWU 市場規模，只知全球份額不到 5%。","runway_post_y5":"🟢","endo_ceiling_basis":"無法計算：當期 NOPAT 接近零，新增資本尚未產生營業利益，總建置成本未揭露。","segments":[{"item":"LEU 部門 Q3 營收","value":"3,180 萬美元，年減 29%，主因鈾銷量減少；SWU 營收增 340 萬美元"},{"item":"Technical Solutions Q3 營收","value":"2,370 萬美元，年減 21%，HALEU 營運合約營收減 1,020 萬美元"},{"item":"總 backlog","value":"70 億美元，至 2040 年；濃縮或有訂單 54 億美元，其中 51 億美元為確定協議"}],"decay_signals":["毛利率下滑：Q3 −19.1% 對去年同期 −5.7%，TTM 低於 FY2025","FCF/淨利連年低於 0.75：FY2024 0.45、FY2025 0.40"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"沒有回購與配息，成長也不靠併購支撐；真正的資本問題是建廠回報，已在再投資與融資風險處理，近三年現金去向事實表未涵蓋。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Westerman 於 2026-10-16 完成，1.16 億美元，占市值 5.4%；CFO 稱第一年增厚，但利潤率未揭露，尚無已實現回報可算。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"未回購，資本全投入建廠，近 365 天也無配息。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"只有兩季資料：Q2 股票補償加回 1,770 萬美元，Q3 為 130 萬美元利益；全年淨稀釋率事實表未涵蓋，不推估。","grade":"不過"}]},"valuation":{"basis":"FY1 前瞻本益比，輔以 EV/S；因分母有爭議，主要看 FY2031 需要多少每股盈餘。","tier":"建廠期核燃料供應商","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，不推估；終端倍數改以自身現值 28.27 倍對照。"},"fwd_pe":28.27,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"基本情境 150 美元，5 年約 7.5% 年化；機率加權約 157 美元，約 8.5% 年化，落在中段偏弱。股價較前份低 42%，但 EPS 分母品質變差，因此判合理而非便宜。五年分位事實表未涵蓋，只有 4 個年度端點，不外推；三年 EPS CAGR 為負，PEG 不適用。","targets":{"short":{"price":111,"basis":"FY2027E 共識 EPS 4.44 美元 × 25 倍，12 個月"},"mid":{"price":124,"basis":"基本情境 FY2031 目標 150 美元以 10% 折現兩年，約 3 年"}},"upside_short_pct":6.1,"upside_mid_pct":18.5},"trap_analysis":{"verdict":"🟡","label":"成長是真的，但亮兩項衰退訊號，獲利品質弱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"到 2027 年逾半 LEU 來自 TENEX，2026–2027 未承諾量豁免未定；新產能 2029 才有，中間沒有替代來源；目前只完成第一台離心機。","assumption":"俄方與美方在 2028 前不切斷供貨，生產線能從第一台放大到商業規模。","consequence":"收入在新廠上線前掉一半，現金同時燒，權證價外，只能在低價增資，五年後虧損超過 50%。","ruling":"採納，這是最大風險，與唯一致命點部分重疊：致命點看終端年的新產能，本條補上過渡期斷供；機率放入 30% 空頭情境。","watch":"DOE 豁免公告、加拿大運輸許可延期、Oak Ridge 出貨節奏。","evidence_refs":["reg_tariff_export#3","geo_supply_chain#1"],"fact_refs":["f_kpi5_free_cash_flow_derived","f_kpi7_cash_and_cash_equivalent"]},{"view":"論點成功但股東經濟變差","evidence":"長約定價受保密條款未揭露；Q3 已宣布的訂單來自 X-energy、Radiant、Antares 等開發商，管理層拒絕拆分；前十大客戶占 77%；對手產能 2028–2032 同期上線；股本 2023–2025 粗算增 29%。","assumption":"長約價格足以回收新廠投資，且客戶有能力履約。","consequence":"工廠如期完工、訂單也交貨，但增量報酬低於資金成本，每股盈餘被股本擴張吃掉。","ruling":"採納，因此基本情境股數用 26M、終端倍數降到 20 倍，並把總建置成本列為重新進場的唯一約束。","watch":"投資人日總建置成本、預付款金額、開發商融資狀況與 backlog 拆分。","evidence_refs":["customer_concentration_credit#0"],"fact_refs":["f_kpi8_total_backlog","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"跌 49.55% 後 Fwd P/E 仍 28.27 倍；FY2028E EPS 3.73 美元低於 FY2025A 3.90 美元；正規化 TTM 約 63 倍。","assumption":"市場願意在獲利下滑期維持 20 倍以上。","consequence":"若以 15 倍看 FY2028E，得 56 美元，再跌 46%。","ruling":"部分採納：本益比角度仍未便宜，但 EV 僅 11 億美元且淨現金占市值 49%，不算過度反映成功。結論是合理、不追。","watch":"FY2026 正規化每股盈餘、共識是否在 Q3 後下修。","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy3","f_ev_m","f_net_debt_m"]}],"max_dd":{"lo":-78,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 179.36 → 本次 104.6（-41.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=179.36","side_b":"本次 price_at_dd=104.6","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 179.36 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 179.36 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 179.36 美元：Bull 價 325、Bear 價 28，五年期望值 −12.4%，基準年化 −3.5%，不對稱比 0.8","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.8。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 179.36 美元：五年期望值 −12.4%，基準年化 −3.5%，不對稱比 0.8","side_b":"本次情境、股價 104.6 美元：五年期望值 +50.2%，基準年化 7.5%，不對稱比 2.4","ruling":"再換股價、情境不動：起點價下跌 41.7%，五年期望值多 62.6 個百分點，基準年化多 11.0 個百分點，不對稱比由 0.8 升到 2.4。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價下跌後的估值結論","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份股價 179.36 美元、Fwd P/E 約 45 倍，估值判偏貴，未給機率與回撤範圍。","side_b":"本次股價 104.6 美元、Fwd P/E 28.27 倍，估值改判合理；機率多 25、基 45、空 30，回撤範圍 −50% 至 −78%。","ruling":"股價跌 42% 讓估值結論放寬，但 EPS 分母品質變差，只放寬到合理，不到便宜。","evidence_level":"高","settle_metric":"FY2026 正規化每股盈餘","if_then":["若 FY2026 正規化每股盈餘低於 2 美元，估值結論回到偏貴，不追。","若總建置成本揭露後基本情境 EPS 上修到 8.4 美元以上，重跑研究並可分批反買。"]},{"axis":"訊號與價值陷阱","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份訊號 B、價值陷阱風險中等，當時訂單 24 億美元且資金未到位。","side_b":"本次兩者維持原判，但組成改變：濃縮訂單 54 億美元、現金 22 億美元變好；Q3 負毛利、FCF 惡化變差。","ruling":"好壞相抵，維持觀望等級；不是沒有新資訊，而是新資訊方向相反。","evidence_level":"中","settle_metric":"FY2026 毛利率與投資人日總建置成本","if_then":["若 FY2026 毛利率低於 20%，價值陷阱升一級，減碼。","若毛利率高於 25% 且總成本可被資金涵蓋，重跑研究。"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份這些欄位為空值。","side_b":"本次依新格式補上：競爭位置穩定、長期空間寬、循環大宗品兼特殊情境、中循環。","ruling":"屬於補填，不代表基本面在這些欄位發生變化。","evidence_level":"高","settle_metric":"無","if_then":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等估值/MA 修復至 $120-150 + DOE final agreement + Russia 2027 末 waiver 確認後再分批","side_b":"投資人日或其後財報揭露總建置成本，且現金加 DOE 里程碑款足以付到 2029 首批上線，不需在 227 美元以下再增資。","ruling":"舊條件已過一項：DOE 於 6 月 30 日簽固定價 9 億美元合約。價格區間失效，股價已低於 120 美元。俄羅斯豁免未定，改列減碼條件。現在真正卡住的是回報算不出來，所以綁單一約束。","evidence_level":"中","settle_metric":"總建置成本與資金涵蓋","if_then":["若條件成立，重跑研究後分批反買，首倉不超過 1.5%。","若揭露後仍需低價再增資，不追；若已持有則減碼。"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（欄位為空）。","side_b":"Piketon 首批新增濃縮產能無法在 2029 年底前開始商業交貨，公司正式把時點延到 2030 年以後。","ruling":"新格式要求列出敏感度最大的一項，新產能時點對終端年 EPS 的影響大於俄供貨中斷。","evidence_level":"中","settle_metric":"公司正式時程與里程碑","if_then":["若正式延到 2030 年以後，若持有則清倉，未持有則不建倉。","若 2028 年底前首批串級已完工過半，降低此項機率並重跑研究。"]},{"axis":"清倉與減碼量化門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設量化出場指標（欄位為空）。","side_b":"本次設六項：新產能延到 2030 後清倉；現金低於 10 億美元且首批未上線清倉；俄供貨未解、毛利率低於 20%、濃縮訂單低於 45 億美元、稀釋超過 25% 均減碼。","ruling":"把前份散在風險表的條件改成可追蹤指標，並補上毛利率與現金兩項新證據對應的門檻。","evidence_level":"中","settle_metric":"各指標季度揭露","if_then":["任一清倉條件觸發即清倉。","減碼條件觸發兩項以上，持股減半。"]},{"axis":"融資風險門檻","cause":"新證據","prior_field":["R2"],"side_a":"2026 末未公告 $1B+ funding plan → 削弱；2027 上半年實際 dilution > 25% → 大砍 thesis","side_b":"第一段已達成並退休，現金 22 億美元；保留 2027 上半年實際稀釋超過 25% 即減碼，新增現金低於 10 億美元且首批未上線即清倉。","ruling":"資金已到位，舊的公告條件失去意義，風險轉為總成本與低價增資。","evidence_level":"高","settle_metric":"現金餘額、總建置成本、股本變動","if_then":["若稀釋超過 25%，減碼。","若現金門檻觸發，清倉。"],"evidence_refs":["major_events#2"]},{"axis":"訂單與本益比舊門檻","cause":"新證據","prior_field":["H2","H3"],"side_a":"2027 末轉換比例 ≥ 30%；2027 末 Fwd PE ≤ 30x，EPS ≥ $4.50","side_b":"確定協議占濃縮訂單已達 94%；Fwd P/E 已 28.27 倍。門檻改為總 backlog 不低於 70 億美元、確定協議占比 90% 以上，以及 FY2027 調整後 EPS 不低於 3.5 美元。","ruling":"舊門檻提前達成或因股價下跌而失去鑑別力，EPS 門檻下調是因為利息收入與建廠費用，共識 FY2027 也只有 4.44 美元。","evidence_level":"高","settle_metric":"季度 backlog 揭露與 FY2027 EPS","if_then":["若 backlog 低於 45 億美元濃縮訂單門檻，減碼。"]},{"axis":"供需缺口方向","cause":null,"prior_field":null,"side_a":"管理層：供需缺口持續擴大，現貨與長約 LEU 價格上升。","side_b":"WNA：全球濃縮供給至少到 2030 年代初仍超過需求。","ruling":"可調和，程度差異。全球數字含俄羅斯與中國產能，西方可用供給較緊。但 WNA 是 2025 年 9 月資料，管理層為自述，所以採中間立場：短缺到新廠大量上線前，之後供給可逆性高。","evidence_level":"中","settle_metric":"公司季度 SWU 均價與 WNA 下一版燃料報告","if_then":["若 SWU 均價連 3 季年減，提高空頭機率到 40% 並減碼。","若 WNA 下一版轉為西方短缺延長到 2035 年以後，重跑研究。"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#3"]},{"axis":"負毛利是時點還是結構","cause":null,"prior_field":null,"side_a":"CFO（2026-11-05）：負毛利主要是進貨與交貨時點錯配，要看 TTM；2026-08-06 CFO 也稱利潤率符合預期。","side_b":"Q2 單價增 3%、單位成本增 13%；Q3 單價增 10%、單位成本增 28%，連兩季成本漲得比價快；Q2 被問成本時未拆解。","ruling":"不採信也不否定，列為未證並監測。Q3 SWU 營收基數小，單季數字可能失真，但方向連兩季相同。不可調和前先不動論點，以 Q4 決勝。","evidence_level":"中","settle_metric":"FY2026 全年毛利率與 Q4 單位成本漲幅","if_then":["若 FY2026 毛利率低於 20%，或 Q4 單位成本年增高於單價年增 10 個百分點以上，時點說法證偽，減碼。","若 FY2026 毛利率高於 25%，時點說法成立，解除此風險。"],"evidence_refs":["end_markets#0","end_markets#1","cyclical_inventory_price_position#2","capital_markets_pricing#1"]},{"axis":"政府支持力度","cause":null,"prior_field":null,"side_a":"CEO（2026-11-05）：兩屆政府支持未減，只會更強。","side_b":"DOE 目前不打算行使 HALEU 營運合約後續選擇權，FY2027 預算未列串級資金；Q3 該合約營收減 1,020 萬美元；2026-08-06 CFO 被問合約資金時未回答。","ruling":"可調和：政策支持轉向新建產能，不再付營運費用。對建廠有利，對 Technical Solutions 不利。示範串級的長期協議仍在談，不能算解決。","evidence_level":"中","settle_metric":"DOE 長期協議與 Technical Solutions 季營收","if_then":["若 2027 年中前未簽長期協議且季營收低於 2,000 萬美元，減碼。","若簽約，移除此風險。"],"evidence_refs":["end_markets#3"]},{"axis":"20 億美元權證資金","cause":null,"prior_field":null,"side_a":"CFO：權證全數行使可帶來約 20 億美元，提供額外財務彈性。","side_b":"699 萬股權證對應平均履約價約 286 美元，逐字稿寫的 2.27 至 3.63 美元應為 227 至 363 美元；現價距最低履約價還要漲 117%。","ruling":"這筆錢只有股價翻倍以上才拿得到，也就是最不缺錢時才有；評估資金時不計入。","evidence_level":"高","settle_metric":"股價相對 227 美元與 10-Q 權證條款","if_then":["若資金缺口要靠這批權證才補得上，不追；若已持有則減碼。"],"evidence_refs":["major_events#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價跌 49.55%，淨現金占市值 49%，EV 11 億美元買到 70 億美元 backlog、美國自有濃縮技術與 DOE 9 億美元合約，里程碑連續提前。","side_b":"現金會花在總成本未揭露的工廠上，FY2028 共識 EPS 低於 FY2025，俄供貨未定，Q3 利空可能未進模型；投資人日只剩一個月，等待成本低。","ruling":"等。基本情境年化約 7.5%，不足以補償二元風險；一個月內會有關鍵資料。","evidence_level":"中","settle_metric":"投資人日總建置成本","if_then":["若股價在條件成立前續漲，不追。","若股價續跌但基本面無損，且條件成立，分批反買，首倉不超過 1.5%，合計不超過 3%。","若機械上偏空的訊號證實為對：FY2026 毛利率低於 20%，到 2027 年 3 月底前仍不進場。"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：Q3 SWU 均價增 10%，WNA 2030 需求高約 28%，國安需求受 GAO 報告支持，濃縮訂單增至 54 億美元。","side_b":"競爭惡化：Urenco、Orano 擴產，General Matter、BWXT 進場，DOE 補助多家。其他結構變數：俄羅斯禁令與豁免、Section 232 關稅、FY2027 預算。","ruling":"雙向拉鋸。2029 年前結構轉好占優，2030 年代初競爭惡化占優。","evidence_level":"中","settle_metric":"西方新增產能時程與長約 SWU 價","if_then":["若 Urenco 或 Orano 擴產提前一年以上，空頭機率加 5 個百分點並停止加碼。"],"evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1"]}],"triggers":[{"n":1,"text":"投資人日後重跑研究。","type":"複審日期","maps_to":"H1","metric":"總建置成本、2027 資本投入、Westerman 利潤率","threshold":"三項是否揭露","action":"不追","source_freq":"公司活動，一次","date":"2026-12-07"},{"n":2,"text":"總建置成本可被現金與 DOE 款涵蓋時，才重新考慮進場。","type":"估值rearm","maps_to":"R2","metric":"現金加 DOE 里程碑款相對總建置成本","threshold":"足以付到 2029 首批上線且不需在 227 美元以下增資","action":"分批反買","source_freq":"投資人日與季報","date":null},{"n":3,"text":"新產能正式延期超過目標年份。","type":"Single Thing","maps_to":"H1","metric":"Piketon 首批商業交貨時點","threshold":"延到 2030 年以後","action":"清倉","source_freq":"季報與 8-K","date":"2029-12-31"},{"n":4,"text":"俄羅斯供貨在過渡期沒有保障。","type":"風險","maps_to":"R1","metric":"2026–2027 未承諾量豁免或過渡供貨合約","threshold":"2027-Q3 前未取得，連 2 季","action":"減碼","source_freq":"DOE 公告與 10-Q","date":"2027-09-30","evidence_refs":["reg_tariff_export#0","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1"]},{"n":5,"text":"Piketon 租約到期前未確定續約。","type":"風險","maps_to":"H1","metric":"Piketon 租約狀態","threshold":"2027-10-01 前未續約","action":"停止加碼","source_freq":"10-Q","date":"2027-10-01","evidence_refs":["regulatory_antitrust#0"]},{"n":6,"text":"負毛利的時點說法被證偽。","type":"風險","maps_to":"R4","metric":"FY2026 毛利率與 Q4 單位成本漲幅","threshold":"毛利率低於 20%，或單位成本年增高於單價年增 10 個百分點以上","action":"減碼","source_freq":"年報","date":"2027-Q1","evidence_refs":["end_markets#0","end_markets#1","cyclical_inventory_price_position#2"]},{"n":7,"text":"現金消耗快於建廠進度。","type":"清倉","maps_to":"R2","metric":"無限制現金","threshold":"低於 10 億美元且 2029 首批尚未上線","action":"清倉","source_freq":"季報","date":"2029-12-31"},{"n":8,"text":"濃縮訂單是否維持。","type":"假設驗證","maps_to":"H2","metric":"濃縮或有訂單金額與確定協議占比","threshold":"低於 45 億美元或占比低於 80%","action":"減碼","source_freq":"季報","date":"2027-12-31"},{"n":9,"text":"替代技術或對手 HALEU 執照成真。","type":"風險","maps_to":"R3","metric":"雷射濃縮商業化與 Urenco USA HALEU 商業執照進度","threshold":"跨年度判斷機率達 50% 以上，單一新聞不觸發","action":"清倉","source_freq":"NRC 公告，半年檢視","date":null,"evidence_refs":["substitute_technology#0","competitive_share_entrants#2"]},{"n":10,"text":"鈾部門關稅若落地，用公司損益判斷能否吸收。","type":"風險","maps_to":"R4","metric":"關稅公告後下一季 SWU 單位成本漲幅","threshold":"單位成本年增高於單價年增 10 個百分點以上","action":"減碼","source_freq":"聯邦公告與季報","date":null,"evidence_refs":["reg_tariff_export#2"]},{"n":11,"text":"McGlone 污染集體訴訟，民事案件；受影響金額與結案日事實表未涵蓋。","type":"風險","maps_to":"R2","metric":"集體認證與和解金額","threshold":"集體認證通過且不利和解超過 1 億美元；刑事介入則清倉","action":"減碼","source_freq":"10-K 與 10-Q 法律附註","date":null,"evidence_refs":["major_events#3","lawsuit_class_action#0"]},{"n":12,"text":"進場條件成立後，股價下跌但基本面無損。","type":"加碼","maps_to":"H3","metric":"股價相對 250 週均線與 Q4 毛利率","threshold":"低於 97.82 美元且 Q4 毛利率為正","action":"分批反買","source_freq":"週線與季報","date":null},{"n":13,"text":"證據未到但股價先走。","type":"估值rearm","maps_to":"R2","metric":"股價與總建置成本揭露","threshold":"條件未達而股價漲到 150 美元以上","action":"不追","source_freq":"週線","date":null},{"n":14,"text":"現有賣方模型尚未消化 Q3，首個確認點前不加碼。","type":"減碼","maps_to":"H3","metric":"FY2026 共識 EPS 是否下修","threshold":"FY2026 財報公布前仍未更新","action":"停止加碼","source_freq":"共識快照，月","date":"2027-Q1","evidence_refs":["capital_markets_pricing#1"]}],"kill_metrics":[{"metric":"Piketon 首批新增產能商業交貨時點","bear_threshold":"公司正式延後到 2030 年以後即清倉","window":"至 2029-12-31","source":"10-Q、8-K、投資人日","last_status":"ok"},{"metric":"俄羅斯 TENEX 2026–2027 未承諾量豁免或過渡供貨","bear_threshold":"2027-Q3 前未取得，連 2 季即減碼","window":"至 2027-09-30","source":"DOE 公告、10-Q","last_status":"warning"},{"metric":"年度毛利率","bear_threshold":"FY2026 或 FY2027 低於 20% 即減碼","window":"FY2026–FY2027","source":"10-K","last_status":"warning"},{"metric":"濃縮或有訂單金額與確定協議占比","bear_threshold":"金額低於 45 億美元，或確定協議占比低於 80%，即減碼","window":"至 2027-12-31","source":"季度財報與法說","last_status":"ok"},{"metric":"無限制現金","bear_threshold":"低於 10 億美元且 2029 首批尚未上線即清倉","window":"至 2029-12-31","source":"10-Q","last_status":"ok"},{"metric":"實際股本稀釋","bear_threshold":"2027 上半年累計超過 25% 即減碼","window":"2027-01-01 至 2027-06-30","source":"10-Q、SEC 增資文件","last_status":"ok"}],"evidence_dismissed":[{"ref":"major_events#4","reason":"證據只有 8-K 申報清單的項目標題，沒有通知內容、原因或後續處理，無法判斷涉及財務還是治理；8-K 件數本身也不是負面資訊，近期多為融資、合約與併購公告。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-49.55, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"投資人日或其後財報揭露總建置成本，且現金加 DOE 里程碑款足以付到 2029 首批上線，不需在 227 美元以下再增資。","exec_line":"條件成立後重跑研究，不直接建倉；首倉不超過 1.5%，第二筆要等 FY2026 毛利率驗證，因為有具名的俄羅斯豁免與建廠成本事件未解。投資人日前不追，Q3 利空進入共識前不加碼。"},"reasoning":{"industry":"營收分兩塊：Q3 LEU 部門 3,180 萬美元（占 57%，年減 29%），Technical Solutions 2,370 萬美元（占 43%，年減 21%）。LEU 部門下滑主要來自鈾銷量減少，SWU 營收其實增加 340 萬美元。Q3 毛損 1,060 萬美元（毛利率 −19.1%），GAAP 營業損失 2,970 萬美元；TTM 毛利率 23.28%、營業利益率 −1.25%。單季波動極大，全年指引 4.5–5 億美元隱含 Q4 要做 1.42–1.92 億美元。單點依賴：到 2027 年預計交貨的 LEU 逾半來自俄羅斯 TENEX，這是集中度風險，不是護城河。前十大客戶占 77%、前兩大 31%、最大 16%，未到必須逐家拆解的程度。Q3 新增訂單的客戶組合管理層拒絕拆分。可能看錯之處：若 Q4 如指引放量，Q3 的負毛利只是時點問題，本段對當期獲利的疑慮會減輕。","moat":"機制是美國自有、不受外國義務限制的濃縮技術，加上至 2040 年的長約與 DOE 9 億美元固定價合約。執行力證據：2026-08-06 CEO 承諾的年底前第一台離心機在 10 月完成，關鍵供應商合約由約 75% 做到 100%，濃縮訂單由 30 億美元增至 54 億美元。定價權證據相反：連兩季單位成本漲得比售價快；Urenco、Orano 擴產，DOE 也把另外兩張 9 億美元任務單給了其他公司，Centrus 沒拿到 LEU 任務單。同業 ROIC 事實表未涵蓋，以營業利益率代替：LEU −1.25%，CCJ 14.35%，BWXT 9.83%，但 LEU 處於建廠期，差距不能全歸於競爭力。全球份額不到 5%，目前是有條件的優勢，評 C。可能看錯之處：若 NNSA 單一來源合約落地且金額大，國安市場的定價權會明顯高於這裡的評分。","growth":"共識 EPS 由 FY2025A 3.90 美元到 FY2028E 3.73 美元，三年 CAGR −1.5%；營收共識 FY2026 4.76 億美元、FY2027 5.03 億美元（18 位分析師），EPS 家數事實表未涵蓋。2029 年前成長主要靠價格與合約組合，2029 年後靠新產能的量。基本情境 FY2026–FY2031 EPS CAGR 15.2%，幾乎全在 FY2030 之後。內生上限算不出來，缺口無法歸因，因此長期信心壓低。衰退訊號亮兩項：毛利率下滑（Q3 −19.1% 對去年同期 −5.7%，TTM 23.28% 低於 FY2025 26.19%；Q2 毛利率事實表未涵蓋），FCF/淨利連年低於 0.75（FY2024 0.45、FY2025 0.40）。滲透率以公司份額衡量很低，但這是空間判斷，不代表產能能如期建成。可能看錯之處：2030 年代初多家新產能疊加，空間可能被對手分走。","governance":"現金 22.36 億美元、總債務 11.79 億美元、淨現金 10.57 億美元，季後再付 Westerman 現金 9,500 萬美元。Q3 自由現金流 −1.26 億美元，TTM FCF 利潤率 −65.02%。9 月募資約 5 億美元，發行 50 萬股加預融資權證最多 200.6 萬股，等於約 200 美元一股，現價僅其一半。逐字稿寫權證履約價 2.27 至 3.63 美元，與 699 萬股權證對應 20 億美元（平均約 286 美元）的數量級不符，應為 227 至 363 美元，現價距最低履約價還要漲 117%，這筆資金目前拿不到。由淨利除以稀釋 EPS 粗算，股本 2023 至 2025 約增 29%。預融資權證與 Westerman 股票可能尚未計入 2,062 萬股。現金去向四分、債務到期結構事實表未涵蓋。壓力測試：若 2027–2029 年均資本投入 8 億美元，扣 Westerman 後現金約撐 2.7 年，未計 DOE 里程碑款。可能看錯之處：DOE 款與客戶預付款若比預期多，再增資需求會大幅下降。","valuation":"推導：104.6 × 1.1^5 ＝ 168.5 美元，除以終端 20 倍得 8.4 美元。Fwd P/E 28.27 倍看似不高，但共識三年 EPS CAGR 為負，PEG 沒有意義。TTM 本益比的分母有爭議，調整後與正規化相差一倍以上。EV/S 2.42 倍在 4 個年度端點中分位 8.1，P/S 分位 28.9，本益比分位 36，都不是五年分位，且 EV 被增資現金壓低。賣方目標價 207–259 美元多為 8 月或未標日期，最高 390 美元是 1 月的舊數字，都早於股價下跌，不支持現在買進。Q3 調整後每股虧損 0.46 美元遠差於約 −0.13 美元的共識（二手摘要），但最新兩份快照 FY1 EPS 仍是 3.70 美元，利空可能尚未進模型。我沒有市場看錯的具體證據，已跌 49.55% 不是安全邊際。可能看錯之處：淨現金占市值 49%，若建廠成本低於預期，現價其實偏低。同業倍數事實表未涵蓋。","premortem":"五年後虧 50% 最可能的故事：俄供貨 2028 前後中斷，新廠延期或超支，現金燒完時股價遠低於權證履約價，只能低價增資。壓力測試五項過兩項：首批延一年現金仍夠、融資窗口關閉時現金可撐約 2.7 年，算通過；SWU 跌 20%、俄供貨 2027 中斷、資本超支 30% 都因單位成本與總建置成本未揭露而無法算過，記未通過。管理層把 Palantir 3 億美元節省的已驗證比例、商用 HALEU 利潤、Westerman 利潤率、2027 資本投入都延到投資人日，2026-08-06 也未拆解成本上升原因。循環位置用建廠循環六訊號：資本投入約為營收的 74–105%（賣）；產能利用率不適用；訂單領先資本投入（買）；交易對手信用混合；情緒偏投降，舊目標價高於現價（買）；量價 Q3 齊升、Q2 量減（中性）。多數落中循環，但訊號互相矛盾，P/B 事實表未涵蓋，反動能檢查不算全過。歷史最大回撤事實表未涵蓋；26 週已跌 49.55%，RSI 42.42，沒有過熱。核心不可守（尚未穿越週期賺錢），適用循環交易紀律。"},"plain":{"six":{"how_it_makes_money":"賺電力公司與美國政府的濃縮錢；今天的利潤卡在 TENEX 進貨成本與交貨時點，五年後的利潤卡在 Piketon 新產能能否如期建成。","moat":"競爭位置穩定：執行力擴大，定價權縮減，兩者相抵。","growth":"長期空間寬：全球份額不到 5%，HALEU 與國安有簽約或政府意向佐證；但 2029 年前不會長在每股盈餘上。","capital":"資金充足，但全押一座廠，回報還算不出來；資本配置尚未通過驗證。","valuation":"現價要 FY2031 EPS 約 8.4 美元才有 10% 年化，高於基本情境 7.5 美元；不貴，但沒有安全邊際，我不信現在的本益比能當便宜的證據。","how_wrong":"最可能看錯在新廠造價與時點，其次是俄羅斯供貨斷在新產能出來之前；成長是真的，但獲利品質弱。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 12 月 7 日投資人日揭露總建置成本，確認現金加 DOE 里程碑款足以付到 2029 首批上線。","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":104.6,"week26_return_pct":-49.55,"consensus_rev_3m_pct":7.56,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"TTM 正規化淨利 3,440 萬美元、調整後 7,730 萬美元，TTM 營業利益率 −1.25%，獲利主要來自營業外與稅務項目及加回的建廠費用（此為推論，利息收入絕對值事實表未涵蓋）。以 2,062 萬股粗算，正規化約 63 倍、調整後約 28 倍；GAAP TTM 又含 4,640 萬美元權證評價利益。GAAP 與 CFO 正規化口徑在營業損失與淨利兩處都差同一筆 460 萬美元，來源未揭露。便宜論證因此無效。"},"catalysts":[{"date":"2026-12-07","date_precision":null,"type":"guidance","event":"Piketon 投資人日：總建置成本、2027 資本投入、Westerman 利潤結構與更新指引","impact":"高","watch":"總成本是否在現金加 DOE 款涵蓋範圍內"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"FY2026 年報與 Q4 結果","impact":"高","watch":"Q4 營收是否達 1.42–1.92 億美元，全年毛利率是否高於 20%"},{"date":"2027-03","date_precision":"month","type":"regulatory","event":"加拿大運輸許可到期，需再延期才能續運 LEU","impact":"中","watch":"是否取得延期"},{"date":"2027-Q3","date_precision":"quarter","type":"regulatory","event":"2026–2027 未承諾交貨的俄羅斯豁免或過渡供貨期限","impact":"高","watch":"DOE 是否核准，或公司是否取得替代供貨"},{"date":"2027-10-01","date_precision":null,"type":"regulatory","event":"Piketon 租約到期","impact":"中","watch":"續約條件"},{"date":"2029-Q4","date_precision":"quarter","type":"capacity","event":"Piketon 首批新產能目標上線","impact":"高","watch":"是否開始商業交貨"}],"_projected_from":"v19"}
```
