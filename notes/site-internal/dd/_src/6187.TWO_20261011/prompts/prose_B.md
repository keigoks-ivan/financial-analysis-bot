你是 stock-analyst v20 的**散文層（prose）agent**，標的 6187.TWO（2026-10-11）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6187.TWO_20261011/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：6187.TWO　日期：2026-10-11　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1214B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（751B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1145B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1381B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（888B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（422B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（771B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2249B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4108B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1883B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1214           4050-5786      5 條（2–6 內）  
s3                  8000         751           5074-7249      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3414          8110-11586      5 條（2–6 內）  
s6                 11000         422          7405-10578      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         771           1910-2729      5 條（2–6 內）  
s10                 5000        2249           1926-2751      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1883           2000-3117      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4848B；至少需散文≈40.15KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−79%
−78
−78%
−71%
−70%
−61%
−55%
−55
−46%
−13.4%
−13.4
−12.8
−12.8%
−7.8%
−7.38%
−3%
−1%
−1
0
0.5
0.52
0.53
0.54
0.74
0.75
0.765%
0.77
0.96
1
01
1.1
1.41
1.5
1.5%
1.66
1.87
1.92
2
02
2%
2.6
2.99
3
03
3%
4
04
4%
4.7%
4.7
5%
5
5.82
6
06
6.5
07
7
7.0
08
8
8.5
9
09
10%
10
11
11.4
11.7
12
13.28%
14
14.39%
15%
15
15.38
16%
18
18%
18.14
19
19.11%
19.33%
19.37
19.6
20
20%
21
21.3%
21.9%
22.62
23.34
24
25
25%
26
26.65%
28
28.9%
29%
30
30%
32
33.25%
33.6%
34%
35%
35
35.77%
38
38.3%
39
39.1%
40%
40.99%
41%
42
43
44
45%
45
46%
46.4%
46.8%
47.92%
48
49
50%
50.8
51%
51.81%
52
53.27%
54%
54.29%
54.77%
59.29
60%
61%
66
69%
70
71%
74.31
74.31%
78.73
79
80
82
85.8
90
92
95.2
96.6
99.7
100
100%
102
103%
104
150%
232
250
325.62
359%
448.0
456
587.72
600
771.0
782.8
813.62
826.9
900
1280
1320
1330
1525
1525.0
1550
1650
1800
2022
2023
2024
2025
2026
2027
2028
2029
2030
2456
2467
3131
3583
6187
6640
20261011
1,430.0
1,485.2
2,354.6
3,500
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
{"meta":{"ticker":"6187.TWO","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"萬潤"},"oneliner":"萬潤靠 CoWoS 點膠設備拿到同業最高毛利率，營收正在翻倍；但現價已是 TTM 本益比 79 倍，等於預支 CPO 大成功的情境，加上 2023 年營收腰斬的循環紀錄，不追，等 900 元以下或 CPO 量產兌現再談","thesis":{"H":[{"id":"H1","text":"先進封裝擴產帶動營收翻倍並延續到 2027 年上半年","2y":"2026 年營收約 100 億元、2027 年再成長兩成以上","5y":null,"10y":null,"threshold":"2027 上半年單季營收 ≥ 30 億元，季末合約負債維持 ≥ 2 億元","source":"公開資訊觀測站月營收、季報、法說會","drift_rule":"兩年期：營收較路徑連 2 季偏離 ≥5% 視為削弱、連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"矽光子（CPO）與面板級封裝成為第二條成長曲線","2y":null,"5y":"2028 年 CPO 營收占比 ≥ 30%","10y":null,"threshold":"2027 年 CPO 相關營收 ≥ 15 億元","source":"法說會、外資報告、月營收","drift_rule":"五年期：連 4 季偏離 ≥5% 削弱、連 6 季 ≥10% 反轉"},{"id":"H3","text":"點膠製程綁定帶來的定價力在短缺收斂後仍能維持","2y":null,"5y":"毛利率維持 50% 以上、營業利益率領先同業最高者 5 個百分點以上","10y":null,"threshold":"TTM 毛利率 ≥ 50%","source":"本公司與同業季報","drift_rule":"五年期：連 4 季偏離 ≥5% 削弱、連 6 季 ≥10% 反轉"}],"R":[{"id":"R1","text":"CPO 專案遞延，或設備產出效率提升使機台需求下修","h_ref":"H2","clock":"⚡","threshold":"2027Q1 法說仍未確認 CPO 量產認列","evidence_refs":["end_markets#4","capital_markets_pricing#0"]},{"id":"R2","text":"CoWoS 短缺收斂後客戶擴產消化，2027 下半年起訂單空窗","h_ref":"H1","clock":"🔥","threshold":"合約負債連 2 季下滑且月營收年增轉負","evidence_refs":["supply_demand_durability#3"]},{"id":"R3","text":"兩大客戶約占八成，導入第二供應商或壓價","h_ref":"H3","clock":"🔥","threshold":"TTM 毛利率 < 50%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"id":"R4","text":"股本持續擴張稀釋每股價值","h_ref":"H3","clock":"🐢","threshold":"稀釋股數年增 > 2%","evidence_refs":[]}],"single_thing":{"description":"台積電宣布 2027 年先進封裝擴產放緩或資本支出年減","why_fatal":"封測設備占營收八到九成且客戶集中，現價 79 倍 TTM 本益比假設擴產至少延續到 2028 年；擴產一停，營收可能像 2023 年一樣年減四成以上，倍數同時壓縮","if_happens":"Bear 機率升至 45% 以上；未持有不進場，持有者減碼一半，合約負債同步下滑則清倉","how_monitor":"台積電每季法說資本支出指引、萬潤月營收年增與季末合約負債","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":15.38,"FY2026E":30,"FY2027E":38,"FY2028E":43},"fy_end_month":12,"eps_basis":"稀釋 EPS（GAAP）；事實表未涵蓋賣方共識，三年錨以本判斷 Base 路徑代填，非共識"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6187.TWO_20261011/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收隨客戶擴產劇烈擺盪（2023 年 −46%、2024 年 +359%），但谷底年毛利率仍有 51.81%"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性，2027 下半年後可能反轉：TrendForce 2026-06 缺口收斂預估對照公司 2026-08 法說能見度至 2027Q2","bargaining":{"up":"上游供應商結構事實表未涵蓋","down":"買方高度集中，兩大客戶約八成；短缺期議價力在設備商，缺口收斂後回到客戶端","geo":"台灣生產；美國 232 關稅屬產業背景，未見直接暴露"},"profit_pool_dir":"短缺期利潤池流向先進封裝關鍵站點設備，缺口收斂後預期回流客戶端","tam_table":[{"item":"CoWoS 供需缺口","value":"約 20% → 2026 年底約 10%，2027 年續改善（TrendForce，2026-06）"},{"item":"CoWoS 2027 年月產能","value":"約 18 萬片，片數成長放緩，轉看每片設備用量（鉅亨網，2026-09）"},{"item":"CPO 營收占比預估","value":"高盛：2026／2027／2028 年 3%／29%／69%（2026-09）"},{"item":"CPO 營收預估（另一外資，已下修）","value":"2027 年 21 億元（16%）、2028 年 102 億元（60%）"},{"item":"半導體設備業務成長","value":"美系外資估 2026–2028 年 CAGR 34%"},{"item":"滲透率與營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"CoWoS 點膠製程的認證與製程參數綁定：設備要跟客戶一起調製程才能進線，換供應商等於重跑驗證；點膠、貼合、自動化、光學檢測整合成整線方案，提高單站以外的轉換成本","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"毛利率 2022→2025 年由 47.92% 升至 54.29%、2026Q2 54.77%，執行面在擴張（新製程前導線已交機）；但同業只有 TTM 單點，利差趨勢無從證明，缺口收斂後定價面難再擴大——執行擴大、定價持平，合判持平","threats":[{"level":"🟡","text":"客戶集中：台系晶圓代工與日月光投控約占八成，任一大客戶導入第二供應商即壓縮價格；管理層自己也在投入新製程研發以降低掉單風險","p":"30%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"level":"🟡","text":"CoWoS 短缺收斂：供需缺口由約 20% 收斂至 2026 年底約 10%，2027 年續改善，買方議價力回升、急單溢價消失","p":"40%","evidence_refs":["supply_demand_durability#3"]},{"level":"🟡","text":"CPO 設備產出效率提升，單位產能所需機台減少，新曲線的營收天花板被下修，專案亦有遞延疑慮","p":"35%","evidence_refs":["capital_markets_pricing#0","end_markets#4"]}],"roic_durability":{"quadrant":"高利益率×周轉率待查（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是封裝產線，決策者與付款者是台積電與日月光的資本支出，三角色同在客戶端；AI 封裝產能不足時屬「需要」，但擴產可延後——缺口由約 20% 收斂到 2026 年底約 10% 後急迫性下降，急迫不等於持久"},{"item":"決策層級","level":"🟡","text":"替代性要在單一製程站點衡量：CoWoS 點膠站的設備與製程參數綁定，同代製程內轉換成本高；但每一代新製程（面板級封裝、CPO）都重新比稿，管理層也承認要投入新製程研發以降低掉單風險"},{"item":"價值鏈分配","level":"🟡","text":"價值大多留在晶圓代工端，設備只占擴產支出的一小段；兩大客戶約八成營收，買方集中度高。目前毛利率 54.77% 顯示短缺期設備商分得到利潤，短缺收斂後分配會往客戶端移"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的資本設備，無民生價格敏感或監管授權依賴；美國 232 關稅屬產業背景，未見對本公司的直接暴露"}],"roiic":"事實表未涵蓋投入資本與折舊，無法計算","reinvest_rate":"2026Q2 單季資本支出 771.0 百萬元，接近當季營業利益 782.8 百萬元，擴產期再投資偏重；折舊與營運資金變動事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率；兩項輸入皆缺，天花板不估；本段成長來自外生的客戶擴產需求，情境樹視同超出天花板處理"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","6187.TWO":53.27,"3131.TWO":39.1,"3583.TW":35.77,"6640.TWO":40.99,"2467.TW":46.8,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","6187.TWO":28.9,"3131.TWO":21.9,"3583.TW":14.39,"6640.TWO":19.33,"2467.TW":21.66,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","6187.TWO":11.13,"3131.TWO":8.5,"3583.TW":19.11,"6640.TWO":7.22,"2467.TW":-7.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","6187.TWO":13.28,"3131.TWO":6.03,"3583.TW":4.71,"6640.TWO":7.79,"2467.TW":7.67,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3131.TWO","gm":39.1,"om":21.9,"fcf_margin":8.5,"rd_intensity":6.03,"strategy_note":"毛利率 39.1%、營益率 21.9%，研發密度約本公司一半，同吃先進封裝擴產但定價力明顯較弱","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3583.TW","gm":35.77,"om":14.39,"fcf_margin":19.11,"rd_intensity":4.71,"strategy_note":"毛利率 35.77%、營益率 14.39%，但自由現金流率 19.11% 高於本公司，資本負擔較輕","period":"TTM ending 2026-06-30（4季加總）"},{"name":"6640.TWO","gm":40.99,"om":19.33,"fcf_margin":7.22,"rd_intensity":7.79,"strategy_note":"毛利率 40.99%、營益率 19.33%，與本公司差距約 12 與 10 個百分點","period":"TTM ending 2026-06-30（4季加總）"},{"name":"2467.TW","gm":46.8,"om":21.66,"fcf_margin":-7.38,"rd_intensity":7.67,"strategy_note":"毛利率 46.8% 最接近，但自由現金流率 −7.38%，擴產或營運資金正在吃現金","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（客戶先進封裝擴產）為主，價與組合（CPO、面板級封裝等高單價新機種）為輔，另有營業槓桿；無併購、未見回購，反有股本稀釋","runway_years":"事實表未涵蓋滲透率","runway_post_y5":"🟢","endo_ceiling_basis":"投入資本與折舊事實表未涵蓋，內生天花板無法計算；成長來自客戶擴產的外生需求，視同超出天花板","segments":{"expanded":false,"reason":"半導體封測設備占營收八到九成，其餘業務細項事實表未涵蓋；單一分部即決定利潤結構，成長拆解改在 CPO 與 CoWoS 兩條曲線的營收門檻追蹤"},"decay_signals":["FCF／淨利 < 0.75 連 2 年：2023、2024 年約 0.52、0.53 曾亮，2025 年回到 0.96，2026Q2 單季 0.54 再落下，判半亮","EPS CAGR 高於營收 CAGR 逾 5 個百分點：2022–2025 年 EPS 38.3% 對營收 33.6%，差 4.7 個百分點，未亮但貼線","毛利率連 2 季年減：2026Q2 54.77% 高於 2025 年 54.29%，未見下滑；季度年對年資料事實表未涵蓋","TAM 被替代技術壓縮：面板級封裝定位為加產能而非取代 CoWoS，未亮","其餘六項（市占、提價後銷量、員工股酬、估值倍數系統下移、維持性資本支出、停止投資新產能）事實表未涵蓋或未見"],"trap_rating":"價值陷阱風險🟡（半亮一項）、長期成長性🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠內部擴產而非併購，未見併購與回購紀錄，股東回饋只有現金股利一條，已在理由中交代"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無併購紀錄，重大併購事件搜尋無結果","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未見回購紀錄，股東回饋以現金股利為主","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數由 2022 年約 85.8 百萬股增至 2026Q2 約 99.7 百萬股（淨利÷稀釋 EPS 回推），年化約 4%，高於 1.5% 上限；成因事實表未涵蓋","grade":"不過"}]},"valuation":{"basis":"TTM 本益比為主、自身 Base 路徑前瞻本益比為輔（同業倍數事實表未涵蓋）","peers":{"expanded":false,"reason":"同業本益比事實表未涵蓋，只有利潤率；不拿跨層級同業當倍數錨"},"fwd_pe":50.8,"peg":1.92,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"TTM 本益比 78.73 倍位於四個年度端點 95.2 分位，P/S 23.34 倍與 EV/S 22.62 倍皆為年度端點最高；Base 五年終值約 1320 元低於現價；PEG 1.92 看似合理但分母是擴產高峰成長率——綜合偏貴。五年分位口徑事實表未涵蓋","upside_short_pct":-12.8,"upside_mid_pct":-13.4},"trap_analysis":{"verdict":"🟡","label":"擴產高峰估值陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"CoWoS 供需缺口預期 2026 年底收斂至約 10%、2027 年續改善；CPO 專案遞延疑慮已讓股價自 4 月高點回檔逾 29%；2023 年營收年減 46%、EPS 由 5.82 元跌至 1.66 元","assumption":"2027 下半年客戶擴產消化與 CPO 遞延同時發生","consequence":"2029 年 EPS 跌至 14 元、2030 年回到 19 元，24 倍約 456 元，較現價約 −70%","ruling":"採納：Bear 機率給 35%，高於一般的 25–30%，理由是循環紀錄有實證，且現有訂單能見度只到 2027Q2，蓋不住風險窗；與唯一致命點（台積電擴產放緩）方向一致","watch":"台積電資本支出指引、季末合約負債、月營收年增率","evidence_refs":["supply_demand_durability#3","end_markets#4"],"fact_refs":["f_kpi6_backlog","f_pe_current"]},{"view":"論點成功但股東經濟變差","evidence":"高盛 2026-07 因 CPO 設備產出效率提升下修相關營收、目標價由 1650 降至 1550 元；兩大客戶約占營收八成；稀釋股數年化增約 4%；2026Q2 自由現金流僅為淨利的 0.54 倍","assumption":"CPO 與面板級封裝如期量產，但每單位產能所需機台變少、客戶壓價，擴產又吃掉現金","consequence":"營收成長而每股自由現金流成長落後，EPS 路徑接近 Base 而非 Bull","ruling":"部分採納：Base 已按下修後的外資 CPO 口徑估，淨回購殖利率設為 −1%；若 TTM 毛利率守在 50% 以上，壓價這一半不成立","watch":"TTM 毛利率、稀釋股數、全年 FCF／淨利","evidence_refs":["capital_markets_pricing#0","customer_concentration_credit#0"],"fact_refs":["f_kpi5","f_kpi4_eps"]},{"view":"價格已反映太多","evidence":"TTM 本益比 78.73 倍，P/S 23.34 倍與 EV/S 22.62 倍為年度端點最高；26 週漲 74.31%；現價為 52 週均線 813.62 元的 1.87 倍","assumption":"市場用結構成長的倍數定價擴產高峰的獲利","consequence":"即使 Base 路徑 FY2030 年 EPS 44 元成真，30 倍終值約 1320 元仍低於現價；要年化 10% 需 EPS 約 82 元","ruling":"採納：這是觀望的唯一綁定約束，價格回到 900 元以下才重新評估","watch":"股價對照 FY2027E Base EPS 38 元的倍數","evidence_refs":[],"fact_refs":["f_pe_current","f_ps_current","f_ev_s_current","f_week26_return_pct","f_ma_w52"]}],"max_dd":{"lo":-78,"hi":-55,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1525.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1525.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"CPO 第二曲線的規模與時點","cause":null,"prior_field":null,"side_a":"高盛 2026-09 估 CPO 占營收 2026／2027／2028 年 3%／29%／69%，目標價上調至 1800 元；CPO 耦合設備 2026Q4 交貨、2027Q1 放量","side_b":"高盛 2026-07 曾因 CPO 設備產出效率提升下修營收、目標價由 1650 降至 1550 元；另一外資 CPO 預估已下修，遞延疑慮讓股價自 4 月高點回檔逾 29%","ruling":"不可調和（一方擴大、一方縮小）。選下修側作 Base：設備產出效率提升是每單位產能要更少機台的結構性變化，不是時點問題；高盛口徑只放在 Bull，機率 20%","evidence_level":"賣方預估與媒體轉述，未經公司財測","settle_metric":"2027Q1–Q2 月營收與法說揭露的 CPO 認列","if_then":["若 2027Q2 前法說確認 CPO 量產認列且單季營收 ≥ 35 億元，上調 Base 的 2028 年 EPS 並重跑研究","反向：若 2027Q2 仍未見 CPO 量產出貨，Bull 機率降至 10%，持有者減碼一半"],"evidence_refs":["capital_markets_pricing#0","end_markets#4"]},{"axis":"擴產能見度對照短缺收斂","cause":null,"prior_field":null,"side_a":"公司 2026-08 法說稱能見度至 2027Q2、產能滿載並向外預留 2027–2028 年產能；季末合約負債由 0.74 億元增至 2.99 億元","side_b":"TrendForce 預期 CoWoS 缺口由約 20% 收斂至 2026 年底約 10%，2027 年續改善；2027 年月產能約 18 萬片、片數成長放緩","ruling":"可調和（時間差）：2027Q2 前訂單有底，風險窗在 2027 下半年至 2028 年；現有證據時間窗蓋不住風險窗，不可裁決至 2027Q2 法說","evidence_level":"公司口述加第三方研調","settle_metric":"季末合約負債與月營收年增率","if_then":["若 2027Q1 季末合約負債 ≥ 3 億元且月營收年增仍為正，Bear 機率由 35% 降至 25%","反向：若合約負債連 2 季下滑，持有者減碼至半倉，未持有者不進場"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"營收正在翻倍（8 月年增 103%），營業利益率由 2022 年 21.3% 升至 2026Q2 33.25%；谷底年毛利率 51.81%；高盛最新目標價 1800 元高於現價 18%；CPO 與面板級封裝兩條新曲線都有出處","side_b":"TTM 本益比 78.73 倍、P/S 與 EV/S 為年度端點最高；Base 五年終值約 1320 元低於現價；2023 年 EPS 跌 71% 的循環紀錄","ruling":"不追：即使 Base 路徑 FY2030 年 EPS 44 元成真，30 倍終值仍低於現價；要年化 10% 需 EPS 約 82 元，等於押 Bull","evidence_level":"財報實績加賣方預估","settle_metric":"股價對照 FY2027E Base EPS 38 元的倍數","if_then":["若股價回落至 900 元以下而近 3 個月月營收年增皆為正，重跑研究評估首倉 ≤2%","反向：若股價續漲但 CPO 未見出貨，不追"],"evidence_refs":[]},{"axis":"盈餘品質與現金轉換","cause":null,"prior_field":null,"side_a":"2026Q2 淨利 826.9 百萬元高於營業利益 782.8 百萬元；自由現金流 448.0 百萬元僅為淨利 0.54 倍；資本支出 771.0 百萬元","side_b":"2025 年自由現金流 1,430.0 百萬元、FCF／淨利 0.96，自由現金流率 26.65%","ruling":"可調和：擴產期資本支出與營運資金墊高屬投資期現象；業外成分事實表未涵蓋，FY2026E 以本業獲利估、不外推業外","evidence_level":"財報實績","settle_metric":"2026 全年 FCF／淨利","if_then":["若 2026 全年 FCF／淨利 < 0.5 且 2027 年資本支出未降，Base 終端倍數由 30 倍降至 26 倍"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 900 元以下且月營收年增仍為正，重跑完整研究評估首倉","type":"估值rearm","maps_to":"H1","metric":"股價；月營收年增率","threshold":"股價 ≤ 900 元（約 FY2027E Base EPS 38 元的 24 倍）且近 3 個月月營收年增皆 > 0","action":"重跑研究，通過後首倉 ≤2%","source_freq":"每日股價／每月 10 日月營收","date":null,"evidence_refs":[]},{"n":2,"text":"台積電法說下修或暫緩 2027 年先進封裝擴產","type":"Single Thing","maps_to":"R2","metric":"台積電資本支出指引與 CoWoS 擴產口徑","threshold":"2027 年資本支出指引年減，或明言 CoWoS 擴產放緩","action":"未持有者不進場並把 Bear 機率上調至 45%；持有者減碼一半，當季合約負債同步下滑則清倉","source_freq":"台積電季度法說","date":"2027-01","evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"CPO 設備 2026Q4 交機、2027Q1 放量是否兌現","type":"假設驗證","maps_to":"H2","metric":"法說揭露之 CPO 出貨與月營收","threshold":"2027Q1 平均月營收 ≥ 12 億元且法說確認 CPO 認列","action":"兌現則上調 Base 2027–2028 年 EPS 後重跑研究；未兌現則 Bull 機率降至 10%","source_freq":"每月月營收／每季法說","date":"2027-04","evidence_refs":["end_markets#4","capital_markets_pricing#0"]},{"n":4,"text":"訂單預收連續下滑","type":"風險","maps_to":"R2","metric":"季末合約負債","threshold":"連 2 季下滑且低於 1.5 億元","action":"持有者減碼至半倉；未持有者 Bear 機率上調至 45%","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":5,"text":"定價力鬆動","type":"風險","maps_to":"R3","metric":"TTM 毛利率","threshold":"< 50%","action":"護城河等級重評，持有者減碼一半","source_freq":"季報","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":6,"text":"FY2026 年報與 2027 年第一季月營收出齊後複審","type":"複審日期","maps_to":null,"metric":"FY2026 EPS 對照 Base 30 元","threshold":"偏離 ≥10%","action":"重跑研究","source_freq":"年報","date":"2027-04-15","evidence_refs":[]}],"kill_metrics":[{"metric":"季末合約負債","bear_threshold":"連 2 季下滑且 < 1.5 億元","window":"2026Q4–2027Q2","source":"季報資產負債表","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連 3 個月 < 0","window":"2027 全年","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"TTM 毛利率","bear_threshold":"< 50%","window":"未來 4 季","source":"季報","last_status":"ok"},{"metric":"CPO 設備量產認列","bear_threshold":"2027Q2 前未見量產出貨","window":"2026Q4–2027Q2","source":"法說會","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把客戶擴產高峰的成長當成可延續的結構成長，給 TTM 79 倍；2023 年營收年減 46%、EPS 年減 71% 的紀錄顯示這段成長會隨擴產消化中斷，現價等於押 CPO 大成功"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='→', week26=74.31, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 的每股盈餘路徑只有 CPO 占營收比例的敘事，沒有出貨量乘單價的算式，成長跑道也押在尚未兌現、且已被下修過的 CPO 預估上，所以 Bull 依據不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":["QC-48"],"rearm_trigger":"股價 ≤ 900 元且近 3 個月月營收年增皆為正","exec_line":"現價不追；900 元以下且營收未轉弱才重跑研究評估首倉；持有者以合約負債連 2 季下滑為減碼線、台積電擴產轉向為清倉線"},"reasoning":{"industry":"營收結構：半導體封測設備占營收八到九成，CoWoS 點膠設備地位強；其餘業務細項事實表未涵蓋。客戶以台系晶圓代工與日月光投控為大宗、約占八成（2025-03 報導，非 2026 年精確比重），屬單點依賴，列為集中度風險；近期報導另稱已切入其他 AI 供應鏈客戶。最新一季（2026Q2）營收 2,354.6 百萬元、毛利率 54.77%、營業利益率 33.25%、基本 EPS 8.5 元；淨利 826.9 百萬元高於營業利益 782.8 百萬元，業外成分事實表未涵蓋。錢卡在哪：AI 晶片封裝產能不足時，擴產支出流向點膠、貼合等關鍵站點設備，設備商拿到價格與交期溢價。產業時鐘在擴張期，依據是訂單而非股價：8 月營收年增 103%，季末合約負債由 0.74 億元增至 2.99 億元，產能滿載並向外預留 2027–2028 年產能。供需持久性屬週期性、2027 下半年後可能反轉：CoWoS 供需缺口預期由約 20% 收斂至 2026 年底約 10%，2027 年片數成長放緩，後續要靠每片設備用量與 CPO、面板級封裝撐。產業態勢三軸：競爭面未見新進者或份額流失報導；結構面是設備用量上升與短缺收斂對拉；其他變數中美國 232 關稅屬產業背景、未見直接暴露，面板級封裝定位為加產能而非取代 CoWoS。裁決為雙向拉鋸。","moat":"機制：點膠製程與客戶製程參數綁定，換供應商要重跑驗證；再把點膠、貼合、自動化、光學檢測整合成整線方案，拉高單站以外的轉換成本。可證方向：TTM（至 2026-06）本公司毛利率 53.27%、營業利益率 28.9%，四家同業最高分別為 46.8% 與 21.9%，領先約 6.5 與 7.0 個百分點；研發占營收 13.28%，同業 4.7%–7.8%。自身毛利率由 2022 年 47.92% 升到 2025 年 54.29%，2023 年營收腰斬時仍有 51.81%（年度財報，yfinance）。執行力 8 分：製程延伸到 CPO、面板級封裝與 SoIC，600mm 面板級點膠設備已交付客戶前導線。定價力 7 分：谷底毛利率不破，但兩大客戶約八成、短缺收斂後議價力回升，CPO 設備產出效率提升也在壓縮機台需求。同業 ROIC 與歷年利差事實表未涵蓋，無法證明差距在擴大，故等級停在 B、方向持平。報酬持續期：投入資本事實表未涵蓋，當期 ROIC 無法計算；四檢查點三黃一綠。","growth":"成長來源以量為主：客戶先進封裝擴產帶動出貨（2026 年 1–8 月營收 59.29 億元、年增 51%，8 月年增 103%），加上高單價新機種的組合改善與營業槓桿（營業利益率由 2022 年 21.3% 升至 2026Q2 33.25%）；未見併購與回購，股本反而年化擴張約 4%。賣方三年共識 EPS 事實表未涵蓋；僅有 2026-02 的舊估 2026／2027 年 18.14／19.6 元，TTM EPS 已達 19.37 元，舊估過時不採用。本判斷 Base 路徑 FY2025A 15.38 元到 FY2028E 43 元，三年 CAGR 約 41%。內生天花板因投入資本與折舊缺資料無法計算；缺口歸因於循環量能與利潤率擴張，延續性綁在客戶資本支出，不是內部再投資複利。跑道：滲透率資料缺，改以第二曲線判斷——CPO 耦合設備 2026Q4 交貨、2027Q1 放量，高盛估 2026–2028 年占營收 3%／29%／69%；面板級封裝 2027 年開始拉貨、2028 年才可能放大。衰退信號只有現金轉換半亮，其餘未亮或資料缺。","governance":"現金轉換：FCF／淨利 2025 年 0.96（1,430.0／1,485.2 百萬元）、2024 年 0.53、2026Q2 單季 0.54（448.0／826.9 百萬元）；第二季資本支出 771.0 百萬元幾乎等於當季營業利益，屬海外拓點與擴產。股東回饋：TTM 殖利率 0.765%，以現價回推每股股利約 11.7 元，約 FY2025 稀釋 EPS 15.38 元的七成六。股本：以淨利÷稀釋 EPS 回推，稀釋股數由 2022 年約 85.8 百萬股、2025 年約 96.6 百萬股增至 2026Q2 約 99.7 百萬股，年化約 4%，成因（員工酬勞、可轉債或增資）事實表未涵蓋。現金去向：擴產資本支出與現金股利為主，未見併購與回購；員工股酬占營收、負債到期結構事實表未涵蓋。","valuation":"現價對應 TTM 本益比 78.73 倍（四個年度端點中 95.2 分位），P/S 23.34 倍與 EV/S 22.62 倍皆為年度端點最高；以本判斷 FY2026E Base EPS 30 元計，前瞻本益比約 50.8 倍。現價要求什麼：要五年年化 10%，以 30 倍終端倍數回推 FY2030 年 EPS 需約 82 元（1525×1.1^5≈2456，÷30），接近 Bull 路徑的 92 元，Base 只有 44 元。PEG 以 TTM 本益比 78.73 ÷ Base 三年 EPS CAGR 約 41% ＝1.92，表面在合理區上緣，但分母是擴產高峰的成長率。賣方目標價 1280–1800 元（最高對最低 1.41 倍），現價已在區間上緣，只有高盛 2026-09 的 1800 元高於現價。同業本益比事實表未涵蓋，不拿利潤率對照當倍數錨；五年分位口徑資料缺，只有四個年度端點分位。短期：FY2027E Base EPS 38 元 × 35 倍＝1330 元，−12.8%；中期：FY2030E 44 元 × 30 倍＝1320 元，−13.4%。","premortem":"太保守的路徑：CPO 在 2028 年占營收約七成、面板級封裝 2028 年放大，FY2030 年 EPS 可到 92 元，38 倍下約 3,500 元，五年翻倍以上，機率給 20%。低估循環的路徑：2023 年營收年減 46%、EPS 年減 71%，現價距 104 週均線 587.72 元還有約 61% 的距離。衰退信號只有現金轉換半亮（2023、2024 年 FCF／淨利約 0.52、0.53，2025 年回到 0.96，2026Q2 單季 0.54），價值陷阱風險定黃燈；真正的陷阱不是生意變差，而是把擴產高峰的獲利當成常態給倍數。最強三個反駁點——高盛目標價已上調至 1800 元、營業利益率仍在擴張、谷底年毛利率 51.81% 證明定價力——已併入對質紀錄。"},"plain":{"six":{"how_it_makes_money":"賺的是 AI 晶片先進封裝擴產的設備錢：封測設備占營收八到九成、兩大客戶約占八成，錢卡在 CoWoS 擴產這一節點；產業在擴張期，但 2027 下半年後有週期反轉風險","moat":"護城河方向持平：點膠製程綁定帶來同業最高的毛利率，但只能證明現在領先，證明不了差距在擴大，等級 B","growth":"五年後跑道偏寬：CPO 與面板級封裝是有出處的下一條曲線，但兩者都還在交機與驗證前，寬度要看 2027 年是否兌現","capital":"股東回饋偏弱：現金股利給得大方，但股本四年擴張約一成六，擴產期現金轉換掉到五成左右","valuation":"現價 1525 元要求五年後 EPS 約 82 元並維持 30 倍，等於押 Bull 情境；這條路徑只給兩成機率，不信","how_wrong":"最可能看錯的方向是太保守：若 CPO 依高盛口徑放量、倍數撐在 35 倍以上，五年可翻倍；反方向是低估循環，擴產消化可讓股價回到 104 週均線附近"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把客戶擴產高峰的成長當成可延續的結構成長，給 TTM 79 倍；2023 年營收年減 46%、EPS 年減 71% 的紀錄顯示這段成長會隨擴產消化中斷，現價等於押 CPO 大成功","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 900 元以下（約 FY2027E Base EPS 的 24 倍）且月營收年增未轉負；或 2027Q1 法說確認 CPO 量產認列後重估","qc48_result":"fail","qc48_note":"Bull 的每股盈餘路徑只有 CPO 占營收比例的敘事，沒有出貨量乘單價的算式，成長跑道也押在尚未兌現、且已被下修過的 CPO 預估上，所以 Bull 依據不成立。","trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":1525.0,"week26_return_pct":74.31,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"TTM EPS 19.37 元低估近期獲利（營收正在翻倍，FY2026E 約 30 元），但 FY2026–2027 年 EPS 又是客戶擴產高峰的獲利；2026Q2 淨利 826.9 百萬元高於營業利益 782.8 百萬元，業外成分事實表未涵蓋。分母落在循環哪個位置本身就是爭點，任何「前瞻本益比已不貴」的論證都不成立"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026Q3 財報與 10 月月營收","impact":"中","watch":"毛利率是否守 54%、淨利與營業利益差距（業外成分）"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"CPO 耦合設備首批交機","impact":"高","watch":"法說或月營收是否確認交機"},{"date":"2027-01","date_precision":"month","type":"capacity","event":"台積電 2027 年資本支出與先進封裝擴產指引","impact":"高","watch":"CoWoS 擴產口徑是否放緩"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"CPO 設備放量（2027Q1）","impact":"高","watch":"2027Q1 平均月營收 ≥ 12 億元"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"面板級封裝量產設備拉貨起點","impact":"中","watch":"面板級點膠設備是否由驗證轉量產訂單"}],"_projected_from":"v19"}
```
