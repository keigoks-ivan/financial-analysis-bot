你是 stock-analyst v20 的**散文層（prose）agent**，標的 VICR（2026-10-22）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：VICR　日期：2026-10-22　archetype：None　前份裁決：2026-05-24　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1988B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（502B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1004B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1176B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（965B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（526B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（712B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1910B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3373B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2806B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1988           3508-5012      5 條（2–6 內）  
s3                  8000         502           5249-7498      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3145          8298-11855      5 條（2–6 內）  
s6                 11000         526          7332-10474      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         712           1952-2788      5 條（2–6 內）  
s10                 5000        1910           2163-3090      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2806           2000-2194      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4434B；至少需散文≈40.57KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65
−65%
−61%
−45%
−42%
−35%
−35
−20.4%
−19.46
−7%
0
0.14
0.2%
0.75
0.83
0.85
01
1
1.0
1.1
1.19
1.31
1.33
1.35
1.389
1.43
1.44
1.5
1.7
1.72
1.971
02
2
2.5
2.61
2.7%
2.71
3
3%
3.4
3.5
3.8
4
4.06
4.12
4.3
4.3%
4.4
4.8
4.9
05
5%
5
5.13
5.3
5.5
5.7
6
06
6.12
6.6
7%
7
07
7.8
8%
8
08
8.31
9%
09
9
9.1%
9.2
9.3
9.43
10
10%
10.6
11.4
11.8
11.9%
12
14
14.3
15
16.0%
16
16.5
16.7
16.8%
16.9%
17%
17.6
17.8%
18.4%
18.6%
19
19%
20
20%
20.4%
21
22
24
25
25%
25.5%
25.7
26
28
28.7%
29
29.6%
30%
30
30.1
32
34%
34.9
35
35%
35.7%
36.6%
38%
40%
42
44%
45
47%
47
47.5%
47.9%
49
50%
51.8
52
53%
55%
65%
68.3%
69
70%
70
70.4%
78.5%
79.1%
82.75
90
98.4
100
100%
104
116.6
119%
119.1%
124.38
150%
180
213.42
250
267.99
301
320
337
382
400
528
530
716
737.5
800
2023
2024
2025
2026
2027
2028
2030
2031
2308
20261022
1,080
1,610
1,708
2,100
3,000
3,727
4,300
4,500
4,850
4,860
4,900
5,050
5,360
5,830
6,330
6,660
7,210
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
{"meta":{"ticker":"VICR","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"Vicor Corporation"},"oneliner":"Vicor 第三季營收年增 78.5%、毛利率 68.3%，但約七成營業利益來自權利金；現價約明年共識 EPS 的 35 倍，產品產能在 2027 年中前受限。先等第四季權利金底數兌現，或股價回到 180 美元以下","thesis":{"H":[{"id":"H1","text":"產品營收（扣權利金）隨第一廠去瓶頸，以及第二廠 2027 年第二季起分段上機而持續成長","2y":"2027 全年產品營收至少 7 億美元","5y":"2031 年產品營收至少 15 億美元（第二廠滿載）","10y":null,"threshold":"2026 年第四季產品營收至少 1.43 億美元（季增約 10%）；2027 全年產品營收至少 7 億美元","source":"2026-10-20 第三季電話會議的財務長指引；公司季報新聞稿","drift_rule":"兩年期：產品營收 TTM 對門檻路徑連兩季偏離至少 5% 為削弱，連三季偏離至少 10% 為反轉"},{"id":"H2","text":"權利金已成經常性收入；ITC 調查促使更多 OEM 與超大規模業者以遞增費率取得授權","2y":"2027 全年權利金至少 1.7 億美元，並至少新增一家超大規模業者授權","5y":"2031 年權利金至少 3 億美元","10y":null,"threshold":"每季權利金至少 4,300 萬美元（無新授權時的底數）","source":"2026-10-20 電話會議的財務長與執行長說法；USITC 2026-10-09 立案公告","drift_rule":"兩年期：權利金 TTM 對門檻路徑連兩季偏離至少 5% 為削弱，連三季偏離至少 10% 為反轉"},{"id":"H3","text":"第二代 VPD 在首要客戶以外取得量產訂單，產品毛利率隨規模回升，整體朝 70% 毛利、40% 營益的長期模型靠攏","2y":"2027 年底前，至少一家首要客戶以外的 OEM 或超大規模業者進入第二代 VPD 量產","5y":"合併毛利率維持至少 65%，營益率至少 35%","10y":null,"threshold":"合併毛利率至少 65%、營益率至少 35%；2027 年底前有首要客戶以外的量產訂單","source":"2026-06-19 股東分析師會議；2026-07-21 與 2026-10-20 電話會議","drift_rule":"五年期：TTM 毛利率或營益率連四季偏離至少 5% 為削弱，連六季偏離至少 10% 為反轉"}],"R":[{"id":"R1","text":"首要運算客戶集中：先進產品營收集中在少數客戶，首要客戶延後或減單會立即反映在產品營收","h_ref":"H1","clock":"⚡","threshold":"一年期在手訂單低於 3.5 億美元，或先進產品（扣權利金）單季季減至少 10%；連兩季即減碼","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R2","text":"權利金延續性：兩年期授權到期需續約，ITC 程序可能延後，被訴方也可能以設計迴避，經常性底數因此下滑","h_ref":"H2","clock":"🔥","threshold":"單季權利金低於 3,000 萬美元且當季無新授權；連四季才大動作，ITC 初裁不利例外","evidence_refs":[]},{"id":"R3","text":"競品與架構替代：整合式電壓調節器、IVR、ADI 與 Empower 的垂直供電若在下一代 AI 平台夠用，第二代 VPD 只停在首要客戶","h_ref":"H3","clock":"🐢","threshold":"2027 年底前沒有首要客戶以外的第二代 VPD 量產訂單，且主要 GPU 平台確認採用競品；機率至少 50% 才砍倉","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#3","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"製造與政策：先進產品依賴少數代工與封測，Section 301 關稅加徵，實體清單擴大；第二廠上機延後會讓產能瓶頸拉長","h_ref":"H1","clock":"🔥","threshold":"合併毛利率連兩季低於 55%，或第二廠首批設備延到 2027 年第三季之後","evidence_refs":["geo_supply_chain#0","reg_tariff_export#0","reg_tariff_export#2"]}],"single_thing":{"description":"ITC 第 337 條 VPD 調查的行政法官初裁，認定不侵權或專利無效","why_fatal":"最新一季約七成營業利益來自權利金。遞增費率與進口禁令是逼 OEM 與超大規模業者簽約的主要槓桿；初裁不利會讓新授權停滯，兩年期授權續約降價，Base 情境約四成 EPS 消失","if_happens":"Base 改走 Bear 路徑；持有者清倉，未持有者放棄進場","how_monitor":"USITC 案件程序表、聽證日期與初裁公告；公司每季權利金金額","probability":"約 25%（12 到 24 個月內出現不利初裁；判斷值，事實表無勝訴率資料）"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":34.9,"peg_fy2":0.83,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":2.61,"FY2026E":4.12,"FY2027E":6.12,"FY2028E":8.31},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識取自 Koyfin 快照。FY2025A 含 2025 年 5 月 4,500 萬美元專利和解收入"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VICR_20261022/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"低","fingerprint":"高毛利專利型硬體加授權收入。2024 年 EPS 僅 0.14 美元，獲利曲線剛轉折"},"industry":{"clock_phase":"II","sd_verdict_source":"需求面屬結構性持久：AI 處理器電流需求由數百安培走向數千安培，一年期在手訂單 4.06 億美元，第四季前兩週接單 1 億美元。供給面短期卡在 Vicor 自身產能，對手產能可逆性高。來源為公司季報與 2026-10-20 電話會議","bargaining":{"up":"上游議價力偏弱：先進產品與部分半導體依賴少數代工廠，封裝與測試也只由少數第三方處理","down":"下游客戶集中，每代處理器平台重新議價；但管理層稱多數客戶對 Vicor 為單一來源","geo":"中國含香港約占 2025 年營收 11.9%。產品屬 EAR99，不需出口許可。2025 年 Section 301 關稅約 737.5 萬美元"},"profit_pool_dir":"管理層稱利潤池正往負載點與 IP 授權移動，但 GPU 廠仍拿走價值鏈大部分；第三方量化資料事實表未涵蓋","tam_table":[{"item":"資料中心加速器市場","value":"2025 年 1,708 億美元，2030 年 3,727 億美元，年複合 16.9%（MarketsandMarkets）"},{"item":"800VDC 在新增資料中心容量的採用率","value":"2027 年 16.0%，2030 年 79.1%（Citi）"},{"item":"Vicor 負載點供電滲透率與份額","value":"事實表未涵蓋"},{"item":"營業利益池占比（5 年前與現在）","value":"事實表未涵蓋"}]},"moat":{"mechanism":"分解式供電與 VPD 專利組合，加上自有 ChiP 晶圓級封裝製程；以 ITC 進口禁令為槓桿，收取遞增權利金","execution":6,"pricing":8,"grade":"B","trend":"→","trend_evidence":"擴大的一面：第三季權利金季增 119% 至 6,660 萬美元；首份純 VPD 授權簽給領先 AI OEM；ITC 於 2026-10-09 立案，列 20 家被訴方。縮減的一面：MPS 於 2023 年在 H100 取代 Vicor；二手分析稱部分 Nvidia 平台失守；首要客戶時程比去年說法晚約 9 個月。兩相抵銷，判持平","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能以利潤率比較；Vicor 最新單季營益率已反超，但含一次性權利金","threats":[{"level":"🔴","text":"大型 IDM（MPS、Infineon 等）以整合式電壓調節器加大幅折價搶 AI 處理器插座，已在最大 GPU 客戶平台取代 Vicor","p":"35%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#3"]},{"level":"🔴","text":"架構替代：IVR、6V 中間匯流排，以及 ADI 傳聞收購 Empower 的垂直供電方案。若在下一代平台夠用，會繞過 Vicor","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"客戶自尋第二貨源；管理層已把重心從第二貨源轉向自建第二廠，第二貨源夥伴仍未定案","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率（最新一季營益率 36.6%）乘上周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（AI 處理器）、決策者（GPU 與系統廠）、付款者（OEM 與超大規模業者）三方都需要更高的負載點電流密度。執行長稱每代處理器電流已從數百安培走向數千安培（2026-10-20）。在手訂單 4.06 億美元，第四季前兩週接單 1 億美元"},{"item":"決策層級","level":"🟡","text":"決策單位是單一處理器平台的供電插座，每代重新競標。Vicor 曾在 H100 平台被 MPS 取代；管理層稱多數客戶對其為單一來源，但重新認證週期約為一代平台"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的經濟利益主要由 GPU 廠與雲端業者拿走，供電占系統成本比例小（金額事實表未涵蓋）。Vicor 以權利金從 OEM 端分一杯羹，但買方集中，對手可由多家供應"},{"item":"社會容忍度","level":"🟡","text":"權利金靠 ITC 進口禁令與遞增費率收取，屬依賴監管救濟的優勢。超大規模業者若集體抵制，或 ITC 裁定不利，費率上限會被壓低"}],"roiic":"事實表未涵蓋（缺投入資本與折舊攤提）","reinvest_rate":"無法精算。第三季資本支出 1,610 萬美元約為淨利 6,330 萬的 25%，折舊與營運資金變動未涵蓋，第二廠金額也尚未揭露","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率，周轉率缺資料。內生成長＝增量 ROIC×再投資率，兩項皆缺，故天花板不給數字。近期成長主要來自毛利率擴張，不是再投資"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","VICR":56.63,"MPWR":55.2,"2308.TW":35.69,"VRT":38.04,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","VICR":18.64,"MPWR":28.72,"2308.TW":16.78,"VRT":19.4,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","VICR":10.82,"MPWR":17.8,"2308.TW":11.7,"VRT":25.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","VICR":17.58,"MPWR":12.62,"2308.TW":8.65,"VRT":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"MPWR","gm":55.2,"om":28.72,"fcf_margin":17.8,"rd_intensity":12.62,"strategy_note":"TTM 營益率 28.7%，高於 Vicor 的 18.6%；曾在最大 GPU 客戶平台取代 Vicor，也是 ITC 被訴方之一，屬最直接的插座競爭者","period":"TTM ending 2026-06-30（4季加總）"},{"name":"2308.TW","gm":35.69,"om":16.78,"fcf_margin":11.7,"rd_intensity":8.65,"strategy_note":"毛利 35.7%、營益 16.8%，以系統電源規模與成本競爭；同列 ITC 被訴方，可能成為授權對象","period":"TTM ending 2026-06-30（4季加總）"},{"name":"VRT","gm":38.04,"om":19.4,"fcf_margin":25.47,"rd_intensity":null,"strategy_note":"機房層電力設備，自由現金流率 25.5%；不在負載點環節直接競爭，只作 AI 電力鏈獲利參照","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"以量為主（產品出貨受產能限制），加上價（授權費率隨 ITC 程序遞增）；無併購、無淨回購","runway_years":"事實表未涵蓋份額，無法換算年數；按 5 到 9 年的中等折扣處理","runway_post_y5":"🟢","endo_ceiling_basis":"內生上界無法以增量 ROIC×再投資率計算，因投入資本與折舊未涵蓋。共識三年 EPS 年增約 47%，遠高於近年資本支出規模所能支撐的內生成長。缺口歸因：毛利率擴張（權利金近全額毛利、稼動率提升）與營運槓桿；沒有淨回購，也沒有收購","segments":[{"item":"先進產品（含權利金）","value":"第三季 1.389 億美元，占 70.4%，季增 47.5%；其中權利金 6,660 萬，季增 119.1%"},{"item":"磚型電源","value":"第三季 5,830 萬美元，占 29.6%，季增 18.4%"},{"item":"ATE 測試客戶","value":"年營收逾 1 億美元（管理層口述）"},{"item":"第四季指引","value":"產品營收季增約 10%，權利金至少 4,300 萬美元（假設無新授權）"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差距超過 5 個百分點）","lit":true,"note":"共識 2025 到 2027 年 EPS 年增約 53%，營收年增約 44%"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"2026-07 二手分析稱部分 Nvidia 平台失守，沒有量化份額"},{"signal":"毛利率連兩季年減","lit":false,"note":"第三季毛利率年增 1,080 基點"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"第三季約 2.7%"},{"signal":"FCF 對淨利低於 0.75 連兩年","lit":false,"note":"2024 年約 4.4，2025 年約 1.0"},{"signal":"其餘五類","lit":false,"note":"TAM 仍在擴張；產業倍數、維持性資本支出、停止投資產能三項未見或事實表未涵蓋"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月無併購項目；回購授權剛核准，尚無執行數字"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 無併購類項目","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"2026-08-25 核准 1.5 億美元新授權；實際買回股數與均價事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"第三季股權酬勞約 530 萬美元，年化約 2,100 萬，約為市值 98.4 億的 0.2%；完整稀釋股數變化事實表未涵蓋","grade":"過"}]},"valuation":{"basis":"前瞻本益比與 PEG，以 FY1 共識 EPS 為分母；營收倍數作輔助","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率、沒有同業倍數，無法當估值錨；賣方目標價快照日期不一"},"fwd_pe":51.8,"peg":1.1,"percentile_5y":7.0,"val_light":"🟡","val_light_derivation":"前瞻本益比 51.8 倍，明年共識 EPS 對應約 34.9 倍。三年 EPS 年複合約 47%（2.61 到 8.31，基期含專利和解），PEG 約 1.1，落在合理區。但有兩個反向因素：市銷率 17.6 倍位於近四個年度端點最高；最新一季獲利約七成來自權利金，分母有爭議，不能據以說便宜。綜合判中性。分位值 7 為本益比在四個年度端點內的分位，不是真正的五年分位","upside_short_pct":4,"upside_mid_pct":35},"trap_analysis":{"verdict":"🟡","label":"成長真實，獲利組成待驗"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"10-K 稱先進產品營收大部分來自少數客戶，而且集中度還會升高；首要客戶時程比去年股東會所示晚約 9 個月；管理層不答首要客戶是否達 10% 營收門檻","assumption":"首要客戶 2027 年照計畫量產，ITC 也帶來新的授權","consequence":"若首要客戶減單與 ITC 初裁不利同時發生，EPS 回到 3 美元附近、本益比 22 倍，股價跌幅約六成以上","ruling":"部分採納。Bear 機率定 30%，ITC 初裁前倉位上限 3%","watch":"一年期在手訂單、季度權利金、10-Q 的客戶集中度揭露","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"],"fact_refs":["f_kpi5_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"法律費約為權利金的 20%；第二、三廠資本支出尚未揭露；10-K 稱大型對手以大幅折價守份額；2025 年關稅約 737.5 萬美元且已加徵；先進產品依賴少數代工與封測","assumption":"營收達 25 億美元時，營益率能到公司目標 40%","consequence":"營收成長兌現，但營益率停在 30% 左右、自由現金流被建廠吃掉，EPS 比 Base 低約兩成","ruling":"部分採納。Base 終值營益率假設約 38%，低於公司 40% 的目標","watch":"第二廠資本支出金額（管理層稱下次電話會議揭露）、法律費占權利金比例、扣除權利金後的產品毛利率","evidence_refs":["competitive_share_entrants#1","reg_tariff_export#0","geo_supply_chain#0"],"fact_refs":["f_kpi1_gaap","f_kpi2_gaap"]},{"view":"價格已反映太多","evidence":"市銷率 17.6 倍、企業價值對營收 16.7 倍，都在近四個年度端點的最高位；前瞻本益比 51.8 倍；FY1 共識 EPS 三個月上修 34%","assumption":"共識上修反映的是經常性獲利","consequence":"若市場剔除第三季權利金的一次性部分，實際前瞻倍數會高於帳面","ruling":"採納。估值中性，不追，等價格或權利金底數兌現","watch":"共識 EPS 修正方向、第四季權利金金額","evidence_refs":[],"fact_refs":["f_ps_current","f_ev_s_current","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]},{"view":"論點失敗","evidence":"10-K 稱產業技術變動快、成熟產品價格侵蝕；有傳聞 ADI 以約 15 億美元收購 Empower 布局垂直供電；MPS、Infineon 同樣在推封裝上供電；開放運算大會聚焦 800V 配電與 6V 中間匯流排","assumption":"負載點電流密度的瓶頸只有 Vicor 的分解式供電能解","consequence":"若 IVR 或整合式電壓調節器在下一代平台夠用，Vicor 產品端只剩首要客戶，授權談判籌碼也會減弱","ruling":"部分採納，列為第三項風險，機率約三成。ADI 收購屬未證實傳聞，不加權","watch":"超大規模業者是否導入第二代 VPD；ADI 與 Empower 的交易是否成立","evidence_refs":["substitute_technology#0","substitute_technology#1"],"fact_refs":[]}],"max_dd":{"lo":-65,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 267.99 → 本次 213.42（-20.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=267.99","side_b":"本次 price_at_dd=213.42","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 267.99 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 267.99 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 267.99 美元：Bull 價 528、Bear 價 116.6，五年期望值 +17.8%，基準年化 4.3%，不對稱比 1.43","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.43。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 267.99 美元：五年期望值 +17.8%，基準年化 4.3%，不對稱比 1.43","side_b":"本次情境、股價 213.42 美元：五年期望值 +47.9%，基準年化 9.1%，不對稱比 2.71","ruling":"再換股價、情境不動：起點價下跌 20.4%，五年期望值多 30.1 個百分點，基準年化多 4.9 個百分點，不對稱比由 1.43 升到 2.71。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-05-24，股價 267.99 美元）估值判中性","side_b":"本次股價 213.42 美元，FY1 共識 EPS 三個月上修 34%；前瞻倍數下降，但權利金占獲利比重過高，分母有爭議","ruling":"維持中性，不因股價下跌改判便宜","evidence_level":"事實表價格與共識快照","settle_metric":"第四季權利金是否守住 4,300 萬美元","if_then":["若第四季與 2027 年第一季權利金都至少 4,300 萬美元，分母爭議解除，估值可改判偏便宜","若權利金低於 3,000 萬美元，估值改判偏貴，不建倉"],"evidence_refs":[]},{"axis":"前份漂移：訊號與陷阱","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份訊號 B，陷阱風險中等","side_b":"新證據方向不一：第三季毛利率 68.3%、權利金 6,660 萬、ITC 立案、購入第二與第三廠場址；但首要客戶延後約 9 個月，第四季總營收預期季減","ruling":"兩項都維持不變：品質改善由權利金帶動，產品端的不確定性同步上升，兩者相抵","evidence_level":"8-K 與電話會議","settle_metric":"2027 年上半年產品營收季增率","if_then":["若 2027 年第一、二季產品營收季增都至少 8%，陷阱風險可降一級","若產品營收連兩季季增低於 5%，陷阱風險升一級並停止加碼"],"evidence_refs":[]},{"axis":"前份漂移：前份未填欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份上述欄位為空","side_b":"本次依現行判斷流程補上：護城河方向持平，五年後跑道寬，公司類型為品質複利成長（低信心）。本次判定非循環股，循環位置不適用。情境機率與最大回撤由本次情境樹產生；裁決與角色由程式依本次輸入重算","ruling":"屬方法補欄，不代表基本面改變","evidence_level":"方法","settle_metric":"無","if_then":["若之後判定為循環股，再補循環位置","若護城河方向轉為縮減，重寫情境機率"],"evidence_refs":[]},{"axis":"重新進場條件新設","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件","side_b":"股價不高於 180 美元，或 2026 年第四季權利金至少 4,300 萬美元且產品營收季增約 10% 兌現","ruling":"新設。條件成立前不建倉；ITC 初裁不利時，持有者清倉","evidence_level":"判斷","settle_metric":"股價、第四季權利金與產品營收","if_then":["若條件成立且無新的負面證據，分兩批建倉","若 ITC 初裁不利，持有者清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"ITC 第 337 條 VPD 調查的行政法官初裁，認定不侵權或專利無效","ruling":"Single Thing 改為 ITC 初裁。理由：在情境中它是數學上最大的單一敏感項，權利金淨貢獻約占 2027 年 EPS 四成；發生時清倉","evidence_level":"8-K 與電話會議推算","settle_metric":"USITC 初裁公告","if_then":["若初裁不利，持有者清倉，未持有者不建倉","若初裁有利，ITC 階段的倉位上限解除"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標","side_b":"權利金連兩季低於 3,000 萬美元；一年期在手訂單低於 3.5 億美元；ITC 初裁不利；合併毛利率連兩季低於 55%","ruling":"新設。前兩項與第四項任一觸發即減碼一半；ITC 初裁不利則清倉","evidence_level":"判斷","settle_metric":"每季 8-K","if_then":["若任一指標觸發，減碼一半","若 ITC 初裁不利，清倉"],"evidence_refs":[]},{"axis":"論點門檻改寫","cause":"新證據","prior_field":["H1.threshold","H2.threshold"],"side_a":"前份 H1：2027 全年產品營收至少 12 億美元，2026 年第四季單季至少 3 億；前份 H2：2027 年權利金至少 8,000 萬美元","side_b":"本次 H1：2026 年第四季產品營收至少 1.43 億美元，2027 全年至少 7 億；本次 H2：每季權利金至少 4,300 萬，2027 全年至少 1.7 億","ruling":"前份 H1 門檻已無法達成：財務長指引第四季產品營收約季增 10%，約 1.44 億，離 3 億差一倍；首要客戶時程晚約 9 個月，第二廠 2027 年第二季才分段上機。前份 H2 門檻則偏低：第三季單季權利金 6,660 萬，已達全年門檻的八成以上","evidence_level":"8-K 與 2026-10-20 電話會議","settle_metric":"2026 年第四季產品營收與權利金","if_then":["若第四季產品營收低於 1.35 億美元，H1 削弱並下修 Base","若第四季權利金至少 4,300 萬美元，H2 維持"],"evidence_refs":[]},{"axis":"權利金是否屬經常性","cause":"新證據","prior_field":null,"side_a":"財務長：第三季權利金 6,660 萬美元中有一部分是新授權首付，不會重複；第四季底數 4,300 萬","side_b":"執行長：被稱為「不重複」的收入一再出現，應視為經常性；第四季初同一被授權人又下了大單","ruling":"性質屬程度差異，可調和。取兩者交集：4,300 萬美元是可依賴的底數，超出部分當一次性。因此第三季 EPS 1.33 美元高估了經常性獲利","evidence_level":"公司電話會議口述加 8-K","settle_metric":"2026 年第四季與 2027 年第一季權利金","if_then":["若兩季權利金都至少 4,300 萬美元且有新授權，權利金視為經常性，依重新進場條件分批建倉","若任一季低於 3,000 萬美元且無新授權，Base 路徑下修約兩成、不建倉；持有者減碼一半"],"evidence_refs":[]},{"axis":"產能說法與實際成長","cause":"新證據","prior_field":null,"side_a":"管理層稱第一廠年產出可由約 10 億美元升至至少 15 億（2026-05-01、2026-06-19）","side_b":"2026-10-20 指引第四季產品營收只季增約 10%，年化約 5.7 億，受特定製程步驟限制","ruling":"性質屬程度差異。以實際出貨為準：2027 年上半年產品成長受第一廠瓶頸限制。共識 2027 年營收 9.43 億美元，扣掉權利金底數約 1.72 億後，產品營收需比第四季年化再增三成以上；第二廠 2027 年第二季分段上機是關鍵","evidence_level":"電話會議與事實表共識","settle_metric":"2027 年第一、二季產品營收季增率","if_then":["若 2027 年第一季產品營收季增至少 8%，維持 H1","若產品營收連兩季季增低於 5%，H1 削弱，Base 的 2027 年 EPS 下修至 5.5 美元以下，並停止任何加碼"],"evidence_refs":[]},{"axis":"負載點供電競爭","cause":"新證據","prior_field":null,"side_a":"管理層：競品第一代 VPD 侵權、電流密度不足；第二代 VPD 電流密度約為對手的三倍（2026-10-20）","side_b":"第三方報導 MPS 在 H100 取代 Vicor（2023）；二手分析稱 Vicor 在部分 Nvidia 平台輸給低成本整合方案；10-K 自承大型對手以大幅折價守份額","ruling":"性質屬程度差異，可調和：技術領先目前只在首要客戶與授權收入上兌現，最大 GPU 客戶的產品份額已失守。Base 不假設奪回最大 GPU 客戶插座，護城河以授權變現為主","evidence_level":"10-K、第三方報導、二手分析","settle_metric":"首要客戶以外的第二代 VPD 量產訂單","if_then":["若 2027 年底前出現首要客戶以外的第二代 VPD 量產訂單，產品護城河改判擴大，Bull 機率上調至 30%","若 ITC 初裁不利且沒有新客戶，護城河改判縮減，持有者清倉"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#3"]},{"axis":"觀望的反面：現在就買的最強論證","cause":"價格變動","prior_field":null,"side_a":"現在就買的理由：股價半年跌 19%，FY1 共識 EPS 卻三個月上修 34%；明年本益比約 35 倍，對應三年 EPS 年增約 47%；淨現金約 5 億美元可自籌第二廠；ITC 立案後授權費率每月約遞增 5%，時間站在 Vicor 這邊","side_b":"等待的理由：最新一季獲利約七成來自權利金，經常性底數只有 4,300 萬；第四季總營收預期季減；產品產能 2027 年中前受限；Base 年報酬約 9%，不足以補償深回撤","ruling":"選等待。Base 年報酬約 9% 只在中段，分母爭議也還沒解。這是價格與證據雙重約束；約束解除的條件是股價回到 180 美元以下，或第四季底數兌現","evidence_level":"事實表價格與共識、電話會議","settle_metric":"第四季權利金與產品營收；股價","if_then":["若股價不高於 180 美元且無新的負面證據，分兩批建首倉","若第四季底數兌現但股價高於 250 美元，不追，等 2027 年第一季再檢查"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"第四季產品營收是否照指引季增約 10%","type":"假設驗證","maps_to":"H1","metric":"季度產品營收（扣除權利金）","threshold":"2026 年第四季至少 1.43 億美元","action":"達標則維持觀察並檢查進場價位；低於 1.35 億美元則下修 Base 路徑、不建倉","source_freq":"公司季報（每季）","date":"2027-02"},{"n":2,"text":"權利金經常性底數是否守住","type":"假設驗證","maps_to":"H2","metric":"季度權利金","threshold":"每季至少 4,300 萬美元","action":"連兩季達標則視為經常性；低於 3,000 萬美元則減碼一半","source_freq":"公司季報（每季）","date":"2027-02"},{"n":3,"text":"ITC 的 VPD 調查初裁","type":"Single Thing","maps_to":"Single Thing","metric":"ITC 第 337 條 VPD 調查初裁結果","threshold":"認定不侵權或專利無效","action":"持有者清倉；未持有者不建倉","source_freq":"USITC 公告（事件）","date":"2027-H2"},{"n":4,"text":"首要客戶與在手訂單","type":"風險","maps_to":"R1","metric":"一年期在手訂單與先進產品營收","threshold":"在手訂單低於 3.5 億美元，或先進產品（扣權利金）單季季減至少 10%","action":"減碼一半","source_freq":"公司季報（每季）","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":5,"text":"競品或替代架構拿下下一代平台","type":"風險","maps_to":"R3","metric":"主要 GPU 平台與超大規模業者的供電方案","threshold":"下一代平台確認改用競品垂直供電方案，且沒有第二代 VPD 新客戶","action":"減碼至半倉","source_freq":"產業發表與公司電話會議（每季）","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#3","substitute_technology#0","substitute_technology#1"]},{"n":6,"text":"關稅、出口管制或代工受阻導致毛利率失守","type":"風險","maps_to":"R4","metric":"合併毛利率","threshold":"連兩季低於 55%","action":"停止加碼","source_freq":"公司季報（每季）","date":null,"evidence_refs":["geo_supply_chain#0","reg_tariff_export#0","reg_tariff_export#2"]},{"n":7,"text":"證券集體訴訟重新提起","type":"風險","maps_to":"無對應論點（治理事件）","metric":"放空者證券集體訴訟的進度","threshold":"重新提告並獲集體認證，或和解金額超過現金的 10%","action":"減碼一半","source_freq":"10-K 與 10-Q 附註（每季）","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":8,"text":"重新進場條件","type":"估值rearm","maps_to":"H1,H2","metric":"股價與第四季兌現","threshold":"股價不高於 180 美元，或第四季權利金至少 4,300 萬美元且產品營收季增約 10%","action":"分兩批建首倉","source_freq":"每日股價；公司季報","date":null},{"n":9,"text":"第二代 VPD 擴到首要客戶以外","type":"加碼","maps_to":"H3","metric":"第二代 VPD 新客戶量產訂單","threshold":"首要客戶以外至少一家宣布量產，且權利金連兩季至少 4,300 萬美元","action":"加碼至目標倉位，ITC 初裁前上限 3%","source_freq":"公司電話會議（每季）","date":"2027-Q4"},{"n":10,"text":"第四季財報後複審","type":"複審日期","maps_to":"H1,H2,H3","metric":"全部論點門檻","threshold":"財報公布後","action":"重跑判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"季度權利金收入","bear_threshold":"連兩季低於 3,000 萬美元","window":"2027 年各季","source":"公司季報 8-K 新聞稿","last_status":"ok"},{"metric":"一年期在手訂單","bear_threshold":"低於 3.5 億美元","window":"每季","source":"公司季報電話會議","last_status":"ok"},{"metric":"ITC 第 337 條 VPD 調查初裁","bear_threshold":"認定不侵權或專利無效","window":"2027 下半年至 2028 年","source":"USITC 公告","last_status":"unknown"},{"metric":"合併毛利率","bear_threshold":"連兩季低於 55%","window":"每季","source":"公司季報 8-K 新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"$.counter_evidence.triggers","reason":"供給面的負向情況已有監控，只是沒有放在單獨的觸發條目。第一廠特定製程瓶頸由觸發條件 1 追蹤：第四季產品營收低於 1.35 億美元就下修 Base。第二廠延後寫在 R4 的門檻：首批設備延到 2027 年第三季之後。反證紀錄「產能說法與實際成長」一條也定了連兩季季增低於 5% 的處置。閘自己也說沒看到漏接，只是看不到該軸的負向條目子集；再加一條觸發會和觸發 1、R4 重複"},{"ref":"$.decision_inputs.market_wrong_reason_given","reason":"第五問的「不追」講的是等價格，不是說估值偏貴。估值判中性，加上權利金分母有爭議，正好是觀望、等 180 美元或第四季底數兌現的理由，和 wait_for_price 的條件一致。oneliner 原文寫的是「先等」，沒有寫「不追」。閘也認定這裡不是判斷錯誤，所以不改"}],"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-19.46, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"ITC 初裁前不超過 3%","requires_critic":[],"verdict":"觀望","rearm_trigger":"股價不高於 180 美元，或 2026 年第四季權利金至少 4,300 萬美元且產品營收季增約 10% 兌現","exec_line":"條件成立後分兩批建倉，第一批不超過目標倉位一半；ITC 初裁前總倉位不超過 3%；初裁不利即清倉"},"reasoning":{"industry":"第三季營收 1.971 億美元。先進產品（含權利金）1.389 億，占 70.4%，其中權利金 6,660 萬；磚型電源 5,830 萬，占 29.6%。毛利率 68.3%，營益率約 36.6%。客戶面，10-K 稱先進產品營收大部分來自少數客戶，且集中度會再升高；前一兩大客戶的占比事實表未涵蓋，管理層也拒答首要客戶是否達 10%。ATE 客戶年營收逾 1 億美元（管理層口述）。產業處於擴張期，依據是 AI 處理器電流需求逐代倍增，一年期在手訂單 4.06 億美元。產業態勢屬雙向拉鋸：一方面需求與授權結構在轉好，ITC 已立案、首份 VPD 授權已簽；另一方面競爭在惡化，大型 IDM 以折價守份額，MPS 曾在 H100 取代 Vicor，ADI 傳聞布局垂直供電。單點依賴屬集中度風險，不是護城河證據","moat":"機制是三件事的組合：分解式供電（電流倍增）、VPD 專利組合、自有晶圓級封裝製程。管理層稱第二代 VPD 電流密度約 3 A/mm²，目標 5 到 6。同業 ROIC 事實表未涵蓋，改用利潤率比較：截至 2026-06 的 TTM 營益率 Vicor 18.6%，MPWR 28.7%，落後約 10 個百分點。第三季單季營益率 36.6%，但約七成來自權利金。推算方式：權利金 6,660 萬減法律費 1,610 萬約 5,050 萬，對營業利益 7,210 萬，假設權利金幾乎沒有銷貨成本。評分：執行 6 分，因首要客戶時程晚約 9 個月、產能有瓶頸；定價力 8 分，因授權費率可隨 ITC 程序遞增、毛利率 68.3%。方向：授權在擴大，最大 GPU 客戶的產品份額在縮減，合計持平","growth":"成長來源是量加價：量來自產品出貨，受第一廠特定製程瓶頸限制，第四季指引季增約 10%；價來自授權費率隨 ITC 程序每月約遞增 5%。沒有併購，也沒有淨回購。共識 EPS 路徑：2025 年 2.61（含專利和解），2026E 4.12，2027E 6.12，2028E 8.31，三年年複合約 47%；FY1 共識三個月內上修 34%。內生上界因投入資本與折舊未涵蓋，算不出數字。缺口歸因於毛利率擴張（權利金近全額毛利、稼動率提升）與營運槓桿，不是再投資，所以成長對權利金能否延續高度敏感。跑道方面，資料中心加速器市場至 2030 年年增約 17%，每代處理器電流需求倍增；Vicor 份額事實表未涵蓋，但明顯偏低。授權構成第二條曲線，因此五年後跑道判寬。衰退信號亮兩個，價值陷阱風險中等","governance":"自由現金流對淨利：第三季 5,360 萬÷6,330 萬約 0.85；2025 年 1.19 億÷1.19 億約 1.0，含和解金。股權酬勞第三季約 530 萬美元，占營收 2.7%。現金去向：第三季資本支出 1,610 萬，在建工程尚待支出約 4,860 萬；沒有股息；2026-08-25 核准 1.5 億美元回購，執行金額未涵蓋；沒有併購。資產負債：現金 5.13 億、總債務約 716 萬。管理層稱第二、三廠不需增資，但第二廠資本支出金額尚未揭露，是下一個要看的數字","valuation":"現價 213.42 美元，等於前瞻本益比 51.8 倍、明年共識 EPS 6.12 美元的 34.9 倍、後年 8.31 美元的 25.7 倍。要划算，需要三件事同時成立：權利金每季至少 4,300 萬美元並延續；第二廠 2027 年第二季上機後，產品營收再增三成以上；毛利率守住 65% 以上。我信產品需求，對權利金只信底數，所以 Base 年報酬約 9%，屬中段。歷史分位兩把尺方向相反：本益比在近四個年度端點只在 7% 分位，因為過去 EPS 低、本益比高；市銷率與企業價值對營收都在 100% 分位。以分母較穩的營收倍數看偏貴。賣方目標價均值約 382 美元，但多為 7 月前的快照，Needham 已由 400 降到 320，不採用。PEG 約為 51.8÷47≈1.1","premortem":"第一，權利金：最新一季約七成營業利益來自權利金，延續性取決於 ITC 程序與兩年期授權的續約。第二，客戶集中：首要客戶時程已比去年說法晚約 9 個月，管理層拒答其營收占比。第三，競爭：最大 GPU 客戶的插座已被 MPS 拿走，第二代 VPD 在首要客戶以外的導入，業務主管也承認還在早期。股價距 104 週均線約 −42%、距 250 週均線約 −61%，反映這是一檔回撤很深的股票。三視角的反證與裁定寫在反證紀錄"},"plain":{"six":{"how_it_makes_money":"Vicor 賺兩筆錢：一是 AI 運算、ATE、工業與國防客戶的負載點供電，二是向 OEM 收專利權利金。錢卡在負載點電流密度這一節點，目前約七成營業利益來自權利金","moat":"護城河方向持平。專利授權變現正在擴大，但在最大 GPU 客戶的產品插座已失守，兩者相抵","growth":"五年後跑道判寬。AI 負載點供電滲透率仍低，授權是第二條曲線；但 2027 年中以前，產品成長會被產能卡住","capital":"資本配置中上。約 5 億美元淨現金可自籌第二廠，股權酬勞低；回購授權剛核准，還看不到執行","valuation":"現價要求 2027 到 2028 年 EPS 照共識翻倍，而且權利金被當成經常性收入。我只信一半，估值中性，不追","how_wrong":"最可能看錯在兩處：把權利金當成經常性收入，以及把首要客戶的量產時程當成確定"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 180 美元以下（約明年共識 EPS 的 29 倍），或第四季權利金至少 4,300 萬美元且產品營收季增約 10% 兌現","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":213.42,"week26_return_pct":-19.46,"consensus_rev_3m_pct":34.2,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"第三季 EPS 1.33 美元含新授權首付；管理層給的經常性權利金底數為每季 4,300 萬，比第三季的 6,660 萬少約 35%。2025 年 EPS 含 4,500 萬美元專利和解收入。以 Base 估算，權利金淨貢獻約占 2027 年 EPS 四成，分母延續性本身就是爭點"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報：權利金是否至少 4,300 萬美元、產品營收是否季增約 10%，並可能揭露第二廠資本支出","impact":"高","watch":"權利金、產品營收、第二廠金額"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"第二廠（Merrimack）2027 年第二季首批設備上機","impact":"中","watch":"產品營收季增率是否回升"},{"date":"2027-08","date_precision":"month","type":"regulatory","event":"ITC 的 VPD 調查進入聽證（依執行長所述立案後約 10 個月推估）","impact":"高","watch":"程序是否延後；是否有被訴方和解並取得授權"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"第二代 VPD 在首要客戶量產爬坡，同時看是否出現第二家客戶","impact":"高","watch":"首要客戶以外的量產訂單"}],"_projected_from":"v19"}
```
