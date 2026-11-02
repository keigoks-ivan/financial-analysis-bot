你是 stock-analyst v20 的**散文層（prose）agent**，標的 JCI（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：JCI　日期：2026-11-02　archetype：None　前份裁決：2026-05-18　A 觀望偏進場·thesis 完整但短 R:R 0.5x 偏緊，建議分批 / 等 BB 中軌 $132 或 Fwd PE 24x ~$135 回測｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1692B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（538B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1018B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1415B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1325B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（964B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1025B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2093B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4383B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2641B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1692           3716-5308      5 條（2–6 內）  
s3                  8000         538           5223-7462      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3758          7869-11242      5 條（2–6 內）  
s6                 11000         964          7025-10036      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1025           1732-2475      5 條（2–6 內）  
s10                 5000        2093           2035-2907      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2641           2000-2359      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5521B；至少需散文≈39.48KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45%
−45
−34%
−30%
−30
−20%
−10%
−2%
0%
0.13%
0.15
0.29
0.33
0.4%
0.75
0.8
0.85
0.9
0.94
0.98
1
01
1.11
1.15
1.20
1.2
1.3
1.5
1.5%
1.55
1.66
1.8
2%
2
02
2.39
2.6
2.7%
2.82
3%
03
3
3.3
3.5
3.52
3.85
4
4%
4.09%
4.2%
4.7%
4.8
4.97
05
5%
5
5.05
5.14
5.16
5.4
5.85
5.9
6.00
6%
6
06
6.05
6.2
6.225
6.25
6.30
6.32
6.45
6.6
6.6%
6.64%
7%
07
7
7.2
7.20
7.40
7.4
7.4%
7.75
08
8%
8
8.10
8.1
8.3%
8.49
8.5%
8.71
8.95
9%
9
9.1
9.65
9.75%
9.75
10%
10
10.4
10.78
11
11.4
11.45
11.7
12%
12
12.99
13%
13.12
13.5%
14
14%
14.45%
15
15%
15.34%
16%
16
16.4%
16.43%
17%
17
17.92%
18%
18
19%
20%
20
20.1
20.14
21%
21
21.4
21.5
22%
22
23
23.58
23.6
24
25%
25
26
26%
27%
27
28
29
30
30%
30.8%
31
31%
31.6
32
36.3%
36.41%
36.65%
37%
38%
42
43%
44%
45
49
49.30
52
54%
58%
58
60%
69%
70
71.13
77%
78%
80%
80
83
85%
90
95%
99
100
100%
103
103%
110
119
$132
135
$135
135.46
143.08
144.9
145
149.03
150%
155
160
162
162.1
165
177
178
188
205
210
220
230
283.3
292.5
300
306.8
500
2015
2018
2023
2026
2027
2900
20261102
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
{"meta":{"ticker":"JCI","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Johnson Controls International plc"},"oneliner":"資料中心冷卻訂單年增44%、積壓230億美元，FY2027指引EPS再成長約兩成；生意在變好，但前瞻本益比約23.6倍已反映大半，資料中心占比升高也讓獲利更像景氣循環，不追，等135美元附近且積壓仍年增再分批。","thesis":{"H":[{"id":"H1","text":"資料中心與關鍵任務設施的熱管理需求，加上每百萬瓦含量擴大（CDU、冷板、模組化），撐住兩年雙位數有機成長。","2y":"FY2028 有機營收年增 ≥10%；積壓訂單每季 ≥230 億美元","5y":null,"10y":null,"threshold":"FY2027 有機營收 ≥10%（指引 11–12%）；積壓訂單不轉年減","source":"公司季報新聞稿、法說會積壓與訂單揭露","drift_rule":"有機營收成長連兩季低於門檻 5% 以上＝削弱；連三季低於 10% 以上＝反轉"},{"id":"H2","text":"營運系統（80/20、精實）與兩輪重組把利潤率推近同業頂部。","2y":null,"5y":"FY2031 GAAP 營業利益率 ≥18%（近四季 14.45%），與 TT 差距 ≤2pp","10y":null,"threshold":"FY2027 調整後 EBIT 利益率擴張 ≥100bp；第二輪重組 FY2029 年化節省約 6 億美元兌現","source":"季報、10-K、法說會重組進度","drift_rule":"GAAP 營業利益率連四季低於路徑 5% 以上＝削弱；連六季低於 10% 以上＝反轉"},{"id":"H3","text":"成長轉成股東拿得到的現金：GAAP 自由現金流率回到兩位數，回饋接近 100% FCF。","2y":null,"5y":"FY2028 起 GAAP FCF÷營收 ≥10%，調整後轉換 ≥95%","10y":"服務附加率提高，FCF 利潤率接近 TT 目前的約 16%","threshold":"FY2027 GAAP FCF 利潤率 ≥8%、回饋 ≥85% 調整後 FCF","source":"10-K 現金流量表、法說會資本回饋","drift_rule":"五年期：連四季偏離 5% 以上削弱、連六季 10% 以上反轉；十年期：跨兩個年度未改善削弱、跨三個年度反轉"}],"R":[{"id":"R1","text":"資料中心建置進入消化期，訂單與積壓轉負。","h_ref":"H1","clock":"🔥","threshold":"有機訂單連兩季年減逾 10%，或積壓訂單年減","evidence_refs":["end_markets#2"]},{"id":"R2","text":"液冷與次世代晶片降低冷卻機需求，或公司跟不上 AI 與冷卻技術變化。","h_ref":"H1","clock":"🐢","threshold":"管理層揭露資料中心冷卻機訂單年減，或資料中心營收占比連兩年停在 20% 以下","evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"id":"R3","text":"關稅加碼與單一來源零件（半導體、稀土）推高成本，價格轉嫁不足。","h_ref":"H2","clock":"⚡","threshold":"調整後 Segment EBITA 利益率連兩季年減 ≥100bp","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]},{"id":"R4","text":"AFFF 消防泡沫 PFAS 集體訴訟和解或判決吃掉多年自由現金流。","h_ref":"H3","clock":"🐢","threshold":"單筆或累計和解／判決 >10 億美元","evidence_refs":["major_events#1","lawsuit_class_action#1"]},{"id":"R5","text":"FY2027 約 9 億美元擴產在需求轉弱時變成過剩產能。","h_ref":"H3","clock":"🔥","threshold":"FY2028 資本支出 ≥9 億美元而有機營收成長 <5%","evidence_refs":[]}],"single_thing":{"description":"積壓訂單轉為年減（資料中心訂單進入消化期的第一個硬訊號）。","why_fatal":"Base 的 FY2028–29 EPS 7.20–8.10 美元有一半以上靠積壓轉營收與營運槓桿；積壓年減代表 FY2028 有機成長掉到個位數、營運槓桿反轉，EPS 與本益比同時下修（23.6 倍→15–18 倍），股價落在 90–110 美元，是情境樹中敏感度最大的單一變數。","if_happens":"減碼一半、停止加碼；若隔季有機訂單仍年減逾 10% 且全年指引下修則清倉。","how_monitor":"每季財報新聞稿的積壓訂單金額與有機年增率；法說會資料中心訂單與客戶電力限制的說法。","probability":"12–24 個月約 20%：FY2026 Q4 訂單年增 44%，FY2027 下半年起比較基期墊高，但管理層稱需求延伸到 FY2027 以後。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.14,"peg_fy2":1.11,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":5.16,"FY2027E":6.32,"FY2028E":7.4,"FY2029E":8.49},"fy_end_month":9,"eps_basis":"調整後 EPS（Non-GAAP）；財年 10 月至隔年 9 月，FY1＝FY2027；FY2026A 5.16 取自單一二手來源，與法說指引中值成長 21% 反推約 5.14 相符"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"訂單與積壓領先營收、營運槓桿逾 30% 驅動 EPS、資料中心資本支出占比升高"},"industry":{"clock_phase":"II","sd_verdict_source":"供需 durability：兩年內結構性持久（積壓 230 億美元、管理層稱需求延伸到 FY2027 以後、客戶提前一年下單），五年以上屬週期性、可能反轉；供給可逆性中（JCI 與同業同步擴產）。來源：Q4 FY2026 新聞稿與法說。","bargaining":{"up":"上游鋼、銅、鋁與半導體、稀土零件；冷卻機五大子系統自製、控制銷貨成本，但半導體與稀土零件有單一或少數供應商（FY2025 10-K），議價力中等偏強。","down":"超大型雲端與託管業者議價力強、很少只選一家（Q3 法說），但無單一客戶占比超過 10%；交貨時程受客戶電力與電氣基礎設施限制主導。","geo":"區域內生產供應區域；美洲占 Q4 營收 69%、占積壓約 77%；已實施關稅大致抵銷（2026-03 季報），中東 2026 年受擾。"},"profit_pool_dir":"利潤池往資料中心熱管理移動：冷卻機之外延伸到 CDU、冷板、控制與模組化；消防保全利潤池停滯，住宅類已出售。","tam_table":{"expanded":false,"reason":"TAM、滲透率與利潤池占比事實表未涵蓋；管理層只給資料中心占營收比重（FY2025 約 12%、FY2026 高十幾%、三到五年三分之一）與 CDU 商機約 10 億美元，不足以展開五年利潤池表，這個缺口限制了跑道判斷的信心。"}},"moat":{"mechanism":"冷卻機五大子系統自製的垂直整合＋約 5 萬人現場銷售與技師網＋大型裝機基礎帶來的服務續約；資料中心服務附加率高於平均。","execution":8,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行力擴大：Q4 三區利潤率全面擴張（美洲 22%、EMEA 16.4%、APAC 19%），調整後 EBIT 利益率 +300bp，前一季財測全數兌現；定價力穩定：價格/成本為正但稀釋毛利率，保全業務出現競爭性量壓；相對最強同業 TT 的 GAAP 營業利益率與 FCF 利潤率差距仍為負，同業歷史值事實表未涵蓋，無法證明差距收斂，故方向判穩定。","threats":[{"level":"🔴","text":"散熱架構改變：液冷與次世代晶片可能降低冷卻機需求（NVIDIA 執行長 2026-01 說法、GTC Berlin 影片），JCI 10-K 自承若跟不上液冷變化會受不利影響；公司以 CDU、冷板、模組化擴大含量對沖。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"技術步調：10-K 風險因子稱若跟不上 AI 技術快速演進，競爭地位與經營結果可能受損。","p":"20%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"資料中心冷卻新進者與客戶多供應商策略；資料中心以外需求分化（Q3 法說報導）。","p":"30%","evidence_refs":["end_markets#2"]},{"level":"🟡","text":"保全業務差異化低、出現競爭性量壓，服務積壓下滑（Q3 法說財務長）。","p":"25%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉（判斷）：調整後 EBIT 利益率約 18%、GAAP 近四季 14.45%；Tyco 合併留下大量商譽壓低周轉。投入資本與當期 ROIC 事實表未涵蓋，象限為推斷。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（資料中心營運者）、決策者（設計與工程團隊）、付款者（業主）三角色都成立，散熱是需要不是想要，延後就無法上線算力；Q4 訂單 +44%、積壓 230 億美元。但急迫性不等於持久性：要解決的問題（散熱）會長期存在，公司目前的方案（冷卻機）可能被液冷改變組合，故給黃。"},{"item":"決策層級","level":"🟡","text":"替代性在單一資料中心設計案層級衡量：大型客戶很少只選一家（Q3 法說），NVIDIA 認證是入場券不是鎖定；轉換成本來自設計規格、交期與裝機後服務合約，但新案每次重新比價，漲價後流失率與續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"晶片與電力是價值鏈最稀缺環節，散熱參考設計由晶片端主導，互補品往單一供應商收斂會壓縮散熱商定價空間；JCI 靠子系統自製控制成本，價格/成本為正但通膨回收稀釋毛利率（Q4 法說），分到的份額沒有變多。"},{"item":"社會容忍度","level":"🟡","text":"商用設備不受漲價的社會天花板限制，耗水爭議管理層稱閉迴路設計已解決；但消防泡沫 PFAS 集體訴訟（美國 49 件、加拿大 7 件，FY2025 10-K）顯示舊產品的社會與法律容忍度風險仍在。"}],"roiic":"事實表未涵蓋（缺投入資本、折舊攤銷、Alloy 收購金額）；判斷區間 30%–100%：低端＝一般新建產能，高端＝精實改造的軟性產能（管理層稱一座工廠產能四倍、不增資本）。","reinvest_rate":"約 10%：FY2027 指引調整後 FCF 轉換約 95%，隱含資本支出與營運資金淨再投資約占調整後淨利 5%，加補強型併購約 5%；管理層承諾 100% FCF 回饋，再投資空間受限。","endo_ceiling":6.0,"formula_note":"內生成長率＝增量報酬×再投資率＝30%–100%×約 10%＝約 3%–10%，取中段約 6%（單位：%/年）；以調整後淨利近似 NOPAT。不論取區間哪一端，共識三年 EPS 年複合約 18% 都超過天花板。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","JCI":36.65,"TT":34.99,"CARR":24.64,"LII":33.1,"HON":38.04,"unit":"%"},{"metric":"營業利益率","JCI":14.45,"TT":17.92,"CARR":8.05,"LII":19.94,"HON":16.2,"unit":"%"},{"metric":"FCF 利潤率","JCI":6.64,"TT":16.43,"CARR":10.43,"LII":15.34,"HON":4.95,"unit":"%"},{"metric":"研發密度","JCI":null,"TT":null,"CARR":2.65,"LII":null,"HON":5.37,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"TT","gm":34.99,"om":17.92,"fcf_margin":16.43,"rd_intensity":null,"strategy_note":"商用 HVAC 最強對手，GAAP 營業利益率高約 3.5pp、FCF 利潤率高約 10pp，是 JCI 利潤率收斂的標竿。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CARR","gm":24.64,"om":8.05,"fcf_margin":10.43,"rd_intensity":2.65,"strategy_note":"營業利益率約 8%、毛利率約 25%，同業最低；資料中心冷卻是直接競爭點，但獲利體質弱於 JCI。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"LII","gm":33.1,"om":19.94,"fcf_margin":15.34,"rd_intensity":null,"strategy_note":"以北美住宅與輕商用為主，營業利益率約 20% 最高，但 JCI 已出售住宅業務，重疊有限。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"HON","gm":38.04,"om":16.2,"fcf_margin":4.95,"rd_intensity":5.37,"strategy_note":"在建築自動化與控制層競爭，FCF 利潤率約 5% 低於 JCI；冷卻機不重疊。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量（資料中心冷卻與液冷含量）為主；利潤率擴張（營運槓桿逾 30%、兩輪重組）次之；淨回購約 2%/年；價格略正但稀釋毛利率；併購僅補強型。","runway_years":"事實表未涵蓋 TAM 與滲透率；以資料中心占比三到五年到三分之一推，雙位數成長跑道約 3–5 年。","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板約 6%/年（區間 3–10%）＝增量報酬 30–100%×再投資率約 10%；共識三年 EPS 年複合約 18%（FY2026 調整後約 5.16 → FY2029 共識 8.49），缺口約 12pp：利潤率擴張約 8pp、淨回購約 2pp，約 2pp 屬資料中心週期帶來的產能利用率，無法歸因於再投資。","segments":[{"item":"美洲（Q4 FY2026）","value":"營收 49.30 億美元，有機 +14%；Segment EBITA 利益率 22%（+210bp）；訂單 +58%；積壓約 178 億美元（約占全公司 77%）。"},{"item":"EMEA","value":"營收 13.12 億美元，報表 −2%、有機 +3%；利益率 16.4%（+80bp）；消防保全比重高，中東 2026 年受擾，資料中心與半導體起步較晚。"},{"item":"APAC","value":"營收 8.71 億美元，+12%；利益率 19%（+110bp）；近兩季資料中心與半導體驅動力轉強。"},{"item":"系統對服務","value":"系統有機 +13%（資料中心冷卻機為主）；服務 +8%，保全服務仍在調整，管理層稱還需 1–2 季。"},{"item":"資料中心占比","value":"FY2025 約 12% → FY2026 高十幾% → 管理層目標三到五年三分之一；CDU 商機 10 億美元以上，只有一小部分轉成訂單。"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"近四季毛利率 36.65% 高於 FY2025 的 36.41%；最新一季毛利率事實表未涵蓋。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"未見來源證實的份額下滑；保全業務有競爭量壓但非核心。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"冷卻機訂單仍強，Q4 有機訂單 +44%。"},{"signal":"EPS 成長顯著高於營收","lit":true,"note":"共識 FY2028 EPS +17%（6.32→7.40）對營收 +8.3%（283.3→306.8 億美元），差約 9pp；FY2027 指引 EPS +21% 對有機營收 +11–12%。"},{"signal":"FCF/淨利 <0.75 連兩年","lit":false,"note":"FY2025 GAAP 0.29 受出售住宅業務利益墊高淨利；FY2022–24 為 0.94–0.98；FY2026 調整後轉換 103%。需盯 FY2027 GAAP 數字。"},{"signal":"SBC/營收 >5% 且上升","lit":false,"note":"Q4 SBC 2900 萬美元，約營收 0.4%。"},{"signal":"TAM 被替代技術壓縮","lit":false,"note":"液冷與次世代晶片降低冷卻機需求的說法尚未反映在訂單，列為觀察。"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"JCI 本益比與 EV/S 在近四個年度端點最高。"},{"signal":"維護性資本支出占 FCF >60%","lit":false,"note":"維護與成長資本支出拆分事實表未涵蓋，屬資料缺口。"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"FY2027 資本支出升到約 9 億美元。"}],"trap_rating":"價值陷阱風險 🟡、長期成長性 🟡（亮 1 個）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長以有機為主（FY2027 指引有機 11–12%），近一年唯一收購 Alloy 金額未揭露且屬補強型，成長不靠併購撐；FY2026 回購加股息 25 億美元已寫入理由，逐年回購均價與現金去向四分事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Alloy Enterprises 收購（2026-05 完成）金額未揭露，已實現報酬無法計算；事實表未涵蓋。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"以 52 週均線 135.46 美元代理回購均價，FY2027 共識 EPS 6.32 計盈餘殖利率約 4.7%；十年期公債殖利率事實表未涵蓋，須低於約 2.7% 才過門檻，判未過。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q4 SBC 2900 萬美元，年化約 1.2 億美元，約市值 0.13%，遠低於 1.5%，且有淨回購。","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2027 共識調整後 EPS）＋PEG","peers":{"expanded":false,"reason":"同業前瞻本益比事實表未涵蓋（同業表只有毛利率、營業利益率、FCF 利潤率），不以跨口徑數字當估值錨。"},"fwd_pe":23.58,"peg":1.3,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 23.6 倍、PEG 約 1.3 屬合理帶；但倍數在自身近四年最高、賣方均值目標與現價相近、機率加權年化約 8% → 合理偏滿。短期上檔＝FY2028 Base EPS 7.20×21.5 倍≈155 美元（+4%）；中期（三年）＝FY2030 Base EPS 8.95×21 倍≈188 美元（+26%）。五年分位事實表未涵蓋。","upside_short_pct":4,"upside_mid_pct":26},"trap_analysis":{"verdict":"🟡","label":"EPS 跑贏營收＋資料中心集中度上升"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"資料中心以外需求分化、市場擔心資料中心冷卻熱潮能否持續與新競爭者（Q3 法說報導）；管理層自己說客戶受電力與電氣基礎設施限制、交貨時程由客戶決定；積壓 230 億美元、訂單年增 44% 已是極高基期。","assumption":"資料中心建置在 FY2028 前不會進入消化期。","consequence":"FY2028–29 訂單轉負、積壓年減，營運槓桿反轉，EPS 停在 6 美元附近、本益比壓到 15 倍，五年後約 99 美元（−34%）；與唯一致命點同源，已併入。","ruling":"部分採納：給 Bear 30% 機率；但 FY2027 有積壓 70–80% 轉換的能見度，12 個月內發生機率低。","watch":"每季積壓訂單金額與有機年增率、有機訂單年增率。","evidence_refs":["end_markets#2","supply_demand_durability#2"],"fact_refs":["f_kpi7_organic_orders_yoy","f_kpi8_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"資料中心占比由 FY2025 約 12% 往三分之一走；FY2027 資本支出升到約 9 億美元、重組費用約 4 億美元；近四季 GAAP FCF 利潤率 6.64% 對 TT 16.43%；價格/成本為正但稀釋毛利率；10-K 稱關稅若加碼會壓營收成長與利潤率；關鍵半導體與稀土零件依賴單一或少數供應商。","assumption":"營收與 EPS 成長會等比例變成股東拿得到的現金，倍數不因組合變化而下修。","consequence":"論點兌現、資料中心變成三分之一，但獲利跟著超大型客戶資本支出起伏，市場改給循環股倍數（16–18 倍）；新增產能在下行期變固定成本，GAAP 現金流持續落後，回購能力打折。","ruling":"採納：這是 Base 終端倍數從 23.6 倍降到 21 倍的理由；不加 Bear 機率，改反映在倍數。","watch":"GAAP 營業現金流減資本支出÷營收（目標 ≥10%）；資料中心占營收比重；調整後 Segment EBITA 利益率年變動。","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"],"fact_refs":["f_peer_jci_fcf_margin_pct","f_peer_tt_fcf_margin_pct","f_kpi4_fcf"]},{"view":"論點成功但股東經濟變差","evidence":"Chemguard 與 Tyco Fire Products 在美國 49 件聯邦集體訴訟、加拿大 7 件 AFFF 消防泡沫 PFAS 訴訟中為被告（FY2025 10-K 附註 20）；求償與準備金額事實表未涵蓋。","assumption":"PFAS 責任可控，不會吃掉多年自由現金流。","consequence":"和解若達數十億美元，等於一到兩年的回購額度，調整後 EPS 不受影響，但每股價值與回饋縮水。","ruling":"採納為監測項，不入機率：金額與時程無資料，不可裁決至公司揭露和解或判決金額為止。","watch":"10-K／10-Q 法律附註的和解金額與準備金；任何單筆或累計超過 10 億美元的和解或判決。","evidence_refs":["major_events#1","lawsuit_class_action#1"],"fact_refs":[]},{"view":"價格已反映太多","evidence":"前瞻本益比 23.6 倍、trailing 31.6 倍，本益比與 EV/S 在近四個年度端點最高；FY2027 共識 6.32 已略高於指引上緣 6.30；賣方平均目標價約 145–162 美元，與現價差不多。","assumption":"FY2027 之後仍能維持中雙位數 EPS 成長，倍數不下修。","consequence":"只要 FY2029 之後成長回到 10% 左右、倍數回到 18 倍，股價約 160 美元，三年報酬只剩個位數。","ruling":"採納：不追價，等 135 美元附近（FY2027 約 21.4 倍）且積壓仍年增再分批。","watch":"股價對 FY2027 共識的前瞻本益比；季報後 FY2028 共識是否上修。","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_eps_fy1"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 143.08 → 本次 149.03（+4.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=143.08","side_b":"本次 price_at_dd=149.03","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 143.08 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 143.08 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 143.08 美元：Bull 價 292.5、Bear 價 99，五年期望值 +36.3%，基準年化 7.4%，不對稱比 2.82","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.82。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 143.08 美元：五年期望值 +36.3%，基準年化 7.4%，不對稱比 2.82","side_b":"本次情境、股價 149.03 美元：五年期望值 +30.8%，基準年化 6.6%，不對稱比 2.39","ruling":"再換股價、情境不動：起點價上漲 4.2%，五年期望值少 5.4 個百分點，基準年化少 0.9 個百分點，不對稱比由 2.82 降到 2.39。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：前一季承諾的兌現","cause":null,"prior_field":null,"side_a":"Q3 法說（2026-07-29，財務長）：Q4 有機成長 9–10%、FY2026 調整後 EPS 約 5.05、未來 12–18 個月營運槓桿高於 30%、服務回到中高個位數。","side_b":"Q4 實績（2026-10-27）：Q4 有機 +12%、Q4 EPS 1.66 高於指引約 1.55、FY2027 指引營運槓桿逾 30%、服務 +8%。","ruling":"一致：管理層連續上修並交付，FY2027 指引視為偏保守的下限。","evidence_level":"公司一手（法說逐字稿、新聞稿）","settle_metric":"Q1 FY2027 有機營收是否落在 12–14%","if_then":["若 Q1 FY2027 有機營收低於 12% 且全年指引未上調，則把指引可信度降一級、停止加碼"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"資本回饋與資本支出承諾 vs 實際","cause":null,"prior_field":null,"side_a":"投資人日（2026-06-01，財務長）：承諾 100% 自由現金流還給股東；稱已讓資本支出與營收成長脫鉤。","side_b":"FY2026 回饋 25 億美元，約調整後 FCF 32 億美元的 78%，淨負債比降到 1.8 倍；FY2027 資本支出升到約 9 億美元，FCF 轉換降到約 95%。","ruling":"可調和（程度差異）：承諾在財年後段才提出，差額用於降槓桿與 Alloy 收購；但脫鉤說法已被 FY2027 實體產能投資部分推翻，財務長 6 月也承認終究需要實體產能。","evidence_level":"公司一手","settle_metric":"FY2027 回購加股息÷調整後自由現金流","if_then":["若 FY2027 回饋低於調整後 FCF 的 85% 且淨負債比仍低於目標區間，則資本配置評語降一級","若 FY2027 回饋達 95% 以上，則恢復對承諾的信任"],"evidence_refs":[]},{"axis":"冷卻機長期需求：管理層 vs 晶片端說法","cause":null,"prior_field":null,"side_a":"NVIDIA 執行長 2026-01 稱次世代晶片可能大幅降低資料中心冷卻需求；GTC Berlin 影片再度呈現無冷卻機設計（Q4 法說分析師轉述）；JCI 10-K 自承若跟不上液冷與 AI 技術變化會受不利影響。","side_b":"JCI 執行長（Q4 法說）：客戶以冗餘與尖峰條件設計，實務上沒有少用冷卻機，邊際上也許少 1–2 台；Q3 法說稱影響非常小；Q4 訂單年增 44%、風冷/水冷組合未變。","ruling":"⚖ 不可調和（方向相反），選管理層這邊、期限兩年：依據是硬數據——Q4 有機訂單年增 44%、冷卻機仍是最大產品線，且 JCI 已把產品延伸到 CDU、冷板（Alloy）與模組化，降低單押冷卻機的風險；晶片端說法目前只有新聞轉述，沒有訂單數據支撐。五年以上不排除晶片端說法成立，已放進 Bear 機率與護城河扣分。","evidence_level":"一手訂單數據＋管理層說法 vs 二手新聞轉述","settle_metric":"資料中心冷卻機訂單方向（法說定性揭露）；CDU／冷板訂單占資料中心訂單成長比重","if_then":["若管理層揭露資料中心冷卻機訂單年減，或主要超大型客戶公開量產無冷卻機設計，則減碼至半倉並重跑研究","反向：若 10 億美元以上的 CDU 商機有一半轉成訂單、資料中心營收占比續升，則恢復加碼權限"],"evidence_refs":["substitute_technology#1","substitute_technology#0","competitive_share_entrants#1"]},{"axis":"現金流品質：調整後 vs GAAP","cause":null,"prior_field":null,"side_a":"調整後自由現金流 FY2026 32 億美元、轉換 103%（Q4 法說）。","side_b":"近四季（至 2026-06）GAAP FCF 利潤率 6.64%，低於 TT 16.43%、LII 15.34%；FY2025 GAAP FCF 9.65 億美元、利潤率 4.09%。","ruling":"可調和（口徑差異）：GAAP 口徑可能含出售住宅業務的稅款與重組現金等一次性項目，但拆解事實表未涵蓋，視為未證，以 FY2027 GAAP 數字驗證。","evidence_level":"公司調整後口徑 vs 資料商 GAAP 口徑","settle_metric":"FY2027 GAAP 營業現金流減資本支出÷營收","if_then":["若 FY2027 GAAP FCF 利潤率低於 8%，則不再採信調整後轉換率、品質評語降一級"],"evidence_refs":[]},{"axis":"共識上修幅度是否真實","cause":null,"prior_field":null,"side_a":"近三個月 FY1 共識 EPS 由 4.97 升到 6.32（+27%）；德國財經網站標題稱 FY2027 EPS 指引顯著高於共識。","side_b":"4.97 接近 90 天前的 FY2026 指引（約 5.05），6.32 是 FY2027；財報後兩次快照 FY1–FY3 都沒變，且 6.32 已略高於指引上緣 6.30。","ruling":"可調和：+27% 主要是財年滾動造成，不是真實上修；高於共識是對財報前的舊共識而言。共識動能視為中性，不作加分。","evidence_level":"資料商快照（口徑問題）","settle_metric":"下一次快照 FY2027 與 FY2028 共識的變動","if_then":["若 Q1 FY2027 財報後 FY2028 共識上修 ≥5%，才視為真實上修"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"積壓訂單數字口徑","cause":null,"prior_field":null,"side_a":"公司 Q4 KPI：積壓訂單 230 億美元、有機年增 43%。","side_b":"同一份新聞稿另一段：訂單年增 58%、積壓 178 億美元年增 54%。","ruling":"可調和：178 億美元搭配訂單 +58%，與美洲訂單 +58% 吻合，判讀為美洲分部數字；全公司以 230 億美元為準。美洲約占積壓 77%，高於其營收占比 69%，集中度在升高。","evidence_level":"公司一手（同一份新聞稿不同段落）","settle_metric":"下一季新聞稿分部積壓揭露","if_then":["若確認 178 億美元為全公司口徑，則重算積壓年增與轉換假設"],"evidence_refs":["supply_demand_durability#1","end_markets#0"]},{"axis":"現在就買的最強論證 vs 等回踩","cause":null,"prior_field":null,"side_a":"現在就買：指引連續上修且每季超標；積壓 230 億美元，若客戶電力限制鬆動，FY2027 營收有上修空間（財務長 Q4 法說）；第二輪重組再省 6 億美元；FY2028 共識 7.40 對應只有約 20 倍。","side_b":"等：倍數在自身近四年最高、賣方均值目標接近現價、機率加權年化約 8%；資料中心占比升高讓獲利更景氣化。","ruling":"選等：基本面好，差的是價格不是證據。","evidence_level":"公司一手＋資料商估值","settle_metric":"股價對 FY2027 共識的前瞻本益比；Q1 FY2027 有機營收與全年指引","if_then":["若股價先漲到 165 美元以上而 Q1 FY2027 尚未上調指引，則不追","若股價回到 135 美元以下且積壓仍年增，則分批反買第一批","若 Q1 FY2027 有機營收 ≥12% 且全年 EPS 指引上調到 6.30 以上，即使價格未回落也買第一批"],"evidence_refs":[]},{"axis":"估值結論沿革","cause":"價格變動","prior_field":["val"],"side_a":"前份：合理（股價 143.08，前瞻基期為 FY2026）。","side_b":"本次：合理偏滿（股價 149.03，前瞻基期滾到 FY2027 共識 6.32，前瞻本益比約 23.6 倍）。","ruling":"估值結論不變：股價上漲約 4%，但 EPS 基期上移約兩成，兩者大致抵銷；前份等的 135 美元在 FY2027 基期下約 21.4 倍。","evidence_level":"事實表價格與共識","settle_metric":"前瞻本益比","if_then":["若前瞻本益比升到 28 倍以上而共識未同步上修，則減碼三分之一"],"evidence_refs":[]},{"axis":"價值陷阱風險上調","cause":"新證據","prior_field":["trap"],"side_a":"前份：價值陷阱風險低。","side_b":"本次：中——共識 FY2028 EPS +17% 對營收 +8.3%，差逾 5pp；FY2027 指引 EPS +21% 對有機營收 +11–12%；資料中心占比升高。","ruling":"採新證據：EPS 成長大幅跑贏營收、靠利潤率與景氣，亮一個衰退訊號，調為中等。","evidence_level":"公司指引＋資料商共識","settle_metric":"FY2028 營收與 EPS 成長差距","if_then":["若 FY2028 EPS 成長回到與營收差距 5pp 以內，則調回低風險"],"evidence_refs":[]},{"axis":"品質評級降一級","cause":"方法變動","prior_field":["signal"],"side_a":"前份：品質評級 A，護城河未計分。","side_b":"本次：B——護城河改用執行力／定價力計分並扣生態層威脅，對最強同業利潤率差距為負，得 C 級，連帶品質評級降一級；基本面本身轉強，不是變差。","ruling":"方法變動導致，不是生意變差：Q4 與 FY2027 指引都優於前份預期。","evidence_level":"同業利潤率對照＋法說","settle_metric":"與 TT 的 GAAP 營業利益率差距","if_then":["若兩年內差距縮到 2pp 以內且 CDU 商機轉成訂單，則品質評級回到 A"],"evidence_refs":[]},{"axis":"護城河方向維持","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：方向穩定。","side_b":"本次：方向穩定——執行力證據轉強（三區利潤率擴張、訂單 +44%），但替代技術與多供應商的反證同時增加，相對最強同業的差距未證明收斂。","ruling":"正反新證據互相抵銷，方向不變。","evidence_level":"公司一手＋二手新聞","settle_metric":"與 TT 的 GAAP 營業利益率差距；資料中心冷卻機訂單方向","if_then":["若差距收斂到 2pp 以內則調為擴大；若冷卻機訂單轉年減則調為縮減"],"evidence_refs":["substitute_technology#1","end_markets#2"]},{"axis":"新格式補齊欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未填：五年後跑道、公司類型、景氣位置、情境機率、最大回撤範圍、裁決與角色欄皆空白。","side_b":"本次依新格式補齊：五年後跑道中等、類型為品質複利成長（次類循環）、景氣位置中段、情境機率 25／45／30、最大回撤 −30%～−45%；裁決與角色由程式從本次輸入算出。","ruling":"純格式補齊，非判斷翻轉。","evidence_level":"方法","settle_metric":"無","if_then":["若資料中心占比超過 30% 且訂單波動加大，則類型改為循環主類並改用循環紀律"],"evidence_refs":[]},{"axis":"重新進場條件由空白改設","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場欄；裁決文字寫等 BB 中軌 $132 或 Fwd PE 24x ~$135 回測。","side_b":"股價 ≤135 美元（約 FY2027 共識 21.4 倍）且最近一季積壓訂單仍年增，啟動第一批。","ruling":"價位相近，但改成價格與積壓訂單雙條件：前份 24 倍是舊基期，同一價位在 FY2027 基期只剩 21.4 倍，價格錨不必放寬；加上基本面條件，避免在景氣反轉時接刀。","evidence_level":"方法","settle_metric":"股價；積壓訂單年增率","if_then":["若股價到 135 美元但積壓已轉年減，則不進場、改重跑研究"],"evidence_refs":[]},{"axis":"Single Thing 由空白改設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"Single Thing：積壓訂單轉為年減（資料中心訂單進入消化期的第一個硬訊號）。","ruling":"積壓訂單是情境樹中敏感度最大的單一變數：Base 的 FY2028–29 EPS 有一半以上靠積壓轉營收與營運槓桿。","evidence_level":"方法＋公司一手","settle_metric":"每季積壓訂單有機年增率","if_then":["若積壓轉年減，則減碼一半；若隔季有機訂單仍年減逾 10% 且全年指引下修，則清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻由空白改設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標。","side_b":"積壓轉年減→減碼一半；有機訂單連兩季年減逾 10% 且全年指引下修→清倉；利益率連兩季年減 ≥100bp→停止加碼；FY2027 GAAP FCF 利潤率 <8%→品質評語降一級。","ruling":"新增可量化的減碼與清倉門檻，取代前份的文字描述。","evidence_level":"方法","settle_metric":"見各指標","if_then":["若任一清倉條件觸發，則清倉並重跑研究"],"evidence_refs":[]},{"axis":"論點門檻改寫（H1–H3、R1–R3）","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：H1 FY27 積壓 >220 億美元且 Applied HVAC 有機 ≥15%；H2 FY27 營業利益率 >13.5%、ROIC ≥8.5%；H3 前瞻本益比不破 23 倍；R3 前瞻本益比跌破 22 倍且賣方降評 ≥3 家。","side_b":"本次：H1 FY2028 有機營收 ≥10%、積壓 ≥230 億美元；H2 FY2027 調整後 EBIT 利益率擴張 ≥100bp、FY2031 GAAP 營業利益率 ≥18%；H3 改為 GAAP FCF 利潤率 ≥10%；估值門檻移到行動條件；新增 PFAS 與擴產過度兩條風險。","ruling":"前份 H1 的 220 億美元已在 FY2026 Q4 達到（230 億），門檻上移；Applied HVAC 分部數字與 ROIC 投入資本本包未涵蓋，改用可驗證的公司層數字；估值不是生意假設，移出論點，改由重新進場與減碼條件處理。","evidence_level":"公司一手","settle_metric":"各假設門檻","if_then":["若 FY2027 有機營收低於 10%，則 H1 判削弱、停止加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"積壓與有機成長驗證兩年需求","type":"假設驗證","maps_to":"H1","metric":"積壓訂單金額；有機營收年增率","threshold":"積壓 ≥230 億美元且 FY2027 有機營收 ≥10%","action":"未達則停止加碼","source_freq":"每季財報新聞稿","date":"2027-02"},{"n":2,"text":"積壓訂單轉為年減","type":"Single Thing","maps_to":"H1","metric":"積壓訂單有機年增率","threshold":"<0%","action":"減碼一半、停止加碼","source_freq":"每季財報新聞稿","date":null},{"n":3,"text":"資料中心訂單消化","type":"風險","maps_to":"R1","metric":"有機訂單年增率","threshold":"連兩季 <−10%","action":"減碼至半倉","source_freq":"每季","date":null,"evidence_refs":["end_markets#2"]},{"n":4,"text":"冷卻機被散熱架構改變取代","type":"風險","maps_to":"R2","metric":"資料中心冷卻機訂單方向；主要客戶設計規格","threshold":"管理層揭露資料中心冷卻機訂單年減，或主要客戶量產無冷卻機設計","action":"減碼至半倉、重跑研究","source_freq":"每季法說；晶片商產品發表","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"n":5,"text":"關稅與零件成本吸收失敗","type":"風險","maps_to":"R3","metric":"調整後 Segment EBITA 利益率年變動","threshold":"連兩季年減 ≥100bp","action":"停止加碼","source_freq":"每季","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]},{"n":6,"text":"PFAS 訴訟金額落地","type":"風險","maps_to":"R4","metric":"AFFF 和解或判決金額","threshold":"單筆或累計 >10 億美元","action":"減碼三分之一","source_freq":"10-K／10-Q 法律附註","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#1"]},{"n":7,"text":"價格回到合理區","type":"估值rearm","maps_to":"H1","metric":"股價；積壓訂單年增率","threshold":"股價 ≤135 美元（FY2027 共識約 21.4 倍）且積壓仍年增","action":"分批第一批","source_freq":"每日股價＋每季","date":null},{"n":8,"text":"基本面證實更強","type":"加碼","maps_to":"H2","metric":"Q1 FY2027 有機營收；全年 EPS 指引","threshold":"有機 ≥12% 且全年指引上調到 6.30 美元以上","action":"加碼一批","source_freq":"季報","date":"2027-02"},{"n":9,"text":"倍數過熱","type":"減碼","maps_to":null,"metric":"前瞻本益比（股價÷FY1 共識）","threshold":"≥28 倍（以 FY2027 6.32 約 177 美元）且共識未同步上修","action":"減碼三分之一","source_freq":"每日","date":null},{"n":10,"text":"景氣反轉確認","type":"清倉","maps_to":"H1","metric":"有機訂單年增率；全年 EPS 指引","threshold":"積壓年減後，下一季有機訂單仍 <−10% 且全年指引下修","action":"清倉","source_freq":"每季","date":null},{"n":11,"text":"擴產過度","type":"風險","maps_to":"R5","metric":"資本支出；有機營收成長","threshold":"FY2028 資本支出 ≥9 億美元而有機營收 <5%","action":"停止加碼","source_freq":"年度","date":null},{"n":12,"text":"Q1 FY2027 財報複審","type":"複審日期","maps_to":null,"metric":"全面複審","threshold":"財報公布後一週內","action":"重跑研究","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"積壓訂單有機年增率","bear_threshold":"<0%（轉為年減）","window":"任一季，FY2027–FY2028","source":"公司季報新聞稿","last_status":"ok"},{"metric":"有機訂單年增率","bear_threshold":"連兩季 <−10%","window":"連續兩季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"FY2027 調整後 EPS 指引中值","bear_threshold":"下修至 <6.00 美元","window":"FY2027 各季法說","source":"法說會","last_status":"ok"},{"metric":"調整後 Segment EBITA 利益率年變動","bear_threshold":"連兩季年減 ≥100bp","window":"連續兩季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"GAAP 自由現金流÷營收","bear_threshold":"FY2027 全年 <8%","window":"FY2027 全年","source":"10-K 現金流量表","last_status":"warning"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#2","reason":"證據為 2023-05 的香港報紙報導，指控行為期間 2015-12 至 2018-06，報導未載明罰款、判決結果或對公司的財務影響；HK$30 億是涉案工程總額，不是求償或罰款金額；FY2025 10-K 法律程序未列此案，無法量化也沒有後續進度。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=3.3, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 135 美元以下（FY2027 共識約 21.4 倍、貼近 52 週均線 135.46）且最近一季積壓訂單仍年增'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價 ≤135 美元（約 FY2027 共識 21.4 倍）且最近一季積壓訂單仍年增，啟動第一批","exec_line":"現價不追；135 美元以下且積壓仍年增→第一批；Q1 FY2027 有機 ≥12% 且指引上調→第二批；積壓年減→減碼一半；隔季有機訂單 <−10% 且指引下修→清倉"},"reasoning":{"industry":"分部（Q4 FY2026，公司新聞稿 2026-10-27）：美洲營收 49.30 億美元、有機 +14%、Segment EBITA 利益率 22%；EMEA 13.12 億美元、有機 +3%、16.4%；APAC 8.71 億美元、+12%、19%；合計 71.13 億美元。調整後 EBIT 12.99 億美元、利益率約 18%（+300bp），GAAP EBIT 11.45 億美元；最新一季毛利率事實表未涵蓋，近四季毛利率 36.65%（財務長稱正常約 37%）。資料中心占營收：FY2025 約 12%（2026-06-01 投資人日財務長）、FY2026 高十幾%（2026-07-29 法說），目標三到五年三分之一。單點依賴：無單一客戶超過 10%（FY2025 10-K），但終端需求越來越集中在資料中心資本支出，且半導體與稀土零件有單一或少數供應商。景氣時鐘 II（擴張）：Q4 有機訂單 +44%、三區利潤率同步擴張、JCI 與同業開始擴產（FY2027 資本支出約 9 億美元），尚未看到產能過剩或價格戰。產業態勢三軸：A 競爭——資料中心新進者與客戶多供應商策略，未見份額流失；B 結構——資料中心、半導體、生技等關鍵任務需求轉好；C 其他——液冷等替代技術與關稅。裁決：雙向拉鋸（B 軸轉好對 C 軸替代技術），依據為 Q4 訂單數據與 FY2025 10-K 風險因子。","moat":"機制：冷卻機五大子系統自製（Q4 法說），供應吃緊時交期與品質是優勢；約 5 萬人現場銷售與技師，管理層稱是多數對手兩倍（2026-06-01 投資人日）；資料中心服務附加率高於平均。可證方向：對最強同業 TT，近四季 GAAP 營業利益率 14.45% 對 17.92%，FCF 利潤率 6.64% 對 16.43%；JCI 自己的營業利益率由 FY2022 9.75% 升到近四季 14.45%，但同業歷史值與投入資本事實表未涵蓋，無法證明差距收斂。執行力 8：Q4 三區利潤率全面擴張、有機成長加速到 12%、前一季財測全數兌現，但執行長自承過去幾年沒有快速釋放潛力；定價力 6：價格/成本為正但稀釋毛利率，保全業務差異化低、出現競爭性量壓（Q3 法說），資料中心大客戶很少只選一家。兩項平均 7，晶片端改變散熱架構屬生態層威脅扣 1 分，得 6，對應 C 級。升級路徑：與 TT 的 GAAP 營業利益率差距兩年內縮到 2pp 以內，且 CDU 與冷板商機轉成實際訂單。","growth":"成長來源：量為主（資料中心冷卻機、CDU、模組化；Q4 有機訂單 +44%、積壓 230 億美元），組合與成本次之（FY2027 指引營運槓桿逾 30%、第一輪重組年化節省比 5 億美元目標多 1–1.5 億美元、第二輪 FY2029 年化約 6 億美元），價格只略正，淨回購約每年 2%。共識：FY2027 6.32、FY2028 7.40、FY2029 8.49（Koyfin 2026-10-31，EPS 家數事實表未涵蓋），自 FY2026 調整後約 5.16 起算三年年複合約 18%；前瞻 GAAP EPS 事實表未涵蓋。營收共識 FY2027 283.3 億、FY2028 306.8 億美元（18／17 位分析師），FY2028 營收 +8.3% 對 EPS +17%。內生天花板約 6%（見護城河段推導），缺口約 12pp：利潤率擴張約 8pp、淨回購約 2pp，其餘約 2pp 是既有產能吃滿資料中心訂單的週期貢獻，無法歸因於再投資，部分依賴 re-rate 不下修。跑道：雙位數成長約 3–5 年（管理層稱 FY2027–28 擴產目標是維持雙位數，但不代表永遠雙位數），TAM 與滲透率事實表未涵蓋。衰退訊號亮 1 個（EPS 成長高於營收逾 5pp），價值陷阱風險與長期成長性皆為中等。","governance":"FCF/淨利轉換：FY2026 調整後自由現金流 32 億美元、轉換 103%（Q4 法說）；GAAP 口徑 FY2022–24 為 0.94–0.98，FY2025 為 0.29（淨利含出售住宅業務利益）；近四季 GAAP FCF 利潤率 6.64%，TT 16.43%、LII 15.34%，調整後與 GAAP 落差大，拆解事實表未涵蓋。Q4 FCF 10.78 億美元。SBC：Q4 2900 萬美元，約營收 0.4%，年化約 1.2 億美元、約市值 0.13%。現金去向：FY2026 回購加股息 25 億美元，約調整後 FCF 的 78%，其餘用於降槓桿（淨負債比 1.8 倍，低於長期目標區間）與 Alloy 收購；投資人日（2026-06-01）財務長承諾 100% 自由現金流還給股東，FY2026 未達。FY2027 資本支出約 9 億美元、重組費用 FY2027–28 約 4 億美元、FCF 轉換降到約 95%。現金去向四分與債務到期結構事實表未涵蓋。計分卡三項：併購已實現報酬——Alloy 金額未揭露，無法計算；回購收益率——未過；SBC 淨稀釋——過。","valuation":"前瞻本益比 23.58 倍＝149.03 ÷ FY2027 共識 6.32；FY2028 共識 7.40 對應約 20.1 倍。PEG＝23.58 ÷ 三年 EPS 年複合約 18%≈1.3，落在合理帶。歷史位置：trailing 本益比 31.6 倍、P/S 3.52 倍、EV/S 3.85 倍都在近四個年度端點的最高點（只有四點，不是五年分位，五年分位事實表未涵蓋）。同業前瞻倍數事實表未涵蓋，不做跨口徑對照。賣方目標價（2026-08 前後，各站日期不一）平均 144.9–162.1 美元，現價落在區間內，尚未反映 Q4 財報。共識修正：近三個月 FY1 由 4.97 升到 6.32（+27%）主要是財年滾動（FY1 由 FY2026 換成 FY2027），不是真實上修；財報後兩次快照 FY1–FY3 都沒變。情境：Base 終端 21 倍×FY2031 EPS 9.75≈205 美元；機率加權五年價格約 +31%，加股息與回購年化約 8%，屬中段。分母：調整後 EPS 排除兩輪重組，新一輪 FY2027–28 約 4 億美元，稅前每年每股約 0.33 美元，約 FY2027 EPS 的 5%，不構成分母爭議。","premortem":"反證三視角（見反證紀錄）：論點失敗——資料中心訂單消化、積壓轉年減，EPS 停在 6 美元附近、倍數壓到 15 倍；論點成功但股東經濟變差——資料中心占比升高讓獲利更景氣化，GAAP 現金流落後同業，PFAS 訴訟尾巴未量化；價格已反映太多——前瞻 23.6 倍在自身最高、賣方均值目標接近現價。衰退訊號亮 1 個（EPS 成長高於營收逾 5pp）。成長熄火測試：Base FY2029 EPS 8.10 之後成長降到 15%／10%／5%，給 22／18／14 倍 → 約 205／160／119 美元，對現價 +38%／+7%／−20%，三個裡兩個過。歷史最大回撤、PFAS 求償金額事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺商用建築與資料中心業主的錢：先賣冷卻機、控制與消防保全系統（Q4 有機 +13%），再靠裝機基礎收服務費（+8%）；錢卡在資料中心熱管理這一節點，冷卻機五大子系統自製，是 FY2026 利潤率擴張的主力。","moat":"護城河 C 級、方向穩定：冷卻機子系統自製加上大規模現場服務網，執行力在變強，但近四季 GAAP 營業利益率仍比 TT 低約 3.5pp、FCF 利潤率低約 10pp，定價力只是穩定，晶片端改變散熱架構則是生態層威脅。","growth":"五年後跑道中等：資料中心占比三到五年走到三分之一，CDU、冷板、模組化與歐洲是第二段，但都綁同一個資料中心資本支出，不是獨立曲線；共識三年 EPS 年複合約 18% 遠高於內生天花板約 6%，缺口主要靠利潤率擴張與回購。","capital":"資本配置中等：SBC 幾乎不稀釋、回購照做但買在約 21–24 倍前瞻本益比不便宜；FY2026 回饋 25 億美元只占調整後 FCF 約 78%，低於投資人日 100% 的承諾；FY2027 資本支出升到約 9 億美元，GAAP FCF 利潤率仍遠落後同業。","valuation":"現價要求 FY2027 照指引成長約兩成、FY2028–29 維持中雙位數，且本益比守在 21 倍以上；前半段我信，後半段只信一半——資料中心占比升高會讓獲利更像景氣循環，倍數該往下修不是往上。合理偏滿，不追，等 135 美元附近。","how_wrong":"最可能看錯的地方：把資料中心兩三年的建置潮當成長期結構，同時付了接近自身歷史高點的倍數；生意沒有變壞，但 EPS 跑贏營收靠的是利潤率與景氣，價值陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 135 美元以下（FY2027 共識約 21.4 倍、貼近 52 週均線 135.46）且最近一季積壓訂單仍年增","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":149.03,"week26_return_pct":3.3,"consensus_rev_3m_pct":27.16,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"調整後 EPS 排除重組與併購攤銷；新一輪重組 FY2027–28 約 4 億美元（稅前每股約 0.33 美元/年），約 FY2027 EPS 的 5%；連續兩輪重組代表這是半經常性成本，但幅度不足以推翻估值結論。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報：指引有機營收 +12～14%、調整後 EPS 1.15～1.20 美元，看積壓訂單與全年指引是否上調","impact":"高","watch":"積壓是否 ≥230 億美元、全年 EPS 指引是否高於 6.30"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"Global Intrusion 出售預計 FY2027 第二季末完成（年營收約 5 億美元，年化稀釋約 0.15 美元/股）","impact":"低","watch":"完成時點與出售款用途（回購或併購）"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"約 9 億美元資本支出的新產能與三區 CDU 擴產陸續到位；與 Armada 合作的 500MW 模組化資料中心在 2027 年出貨","impact":"中","watch":"交期縮短、營運槓桿是否守住 30% 以上"}],"_projected_from":"v19"}
```
