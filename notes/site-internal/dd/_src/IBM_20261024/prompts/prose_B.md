你是 stock-analyst v20 的**散文層（prose）agent**，標的 IBM（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：IBM　日期：2026-10-24　archetype：None　前份裁決：2026-07-23　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1840B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（431B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（994B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1495B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1240B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（681B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（955B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1991B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4208B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2092B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1840           3612-5160      5 條（2–6 內）  
s3                  8000         431           5298-7569      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3729          7890-11271      5 條（2–6 內）  
s6                 11000         681          7223-10319      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         955           1782-2545      5 條（2–6 內）  
s10                 5000        1991           2106-3009      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2092           2000-2908      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5102B；至少需散文≈39.90KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−42%
−41%
−40
−40%
−35%
−31%
−25%
−25
−20%
−19%
−9%
−5%
−3.8%
−3.8
−2%
0%
0
0.7%
0.73%
1
01
1%
1.2
2
2%
02
2.02
2.3
2.4
$2.5
2.56
2.6
2.66
2.66%
2.7%
3.0
3
3%
3.1%
4%
4
$4
04
4.5
4.6%
5
5%
$5.35
6%
6
6.5%
6.7%
07
7
7%
7.14
7.84%
8%
8.0%
8
$8
9%
9
9.0%
10
$10
10%
10.3
10.9%
10.9
11%
11
$11.17
11.17
11.4
12
$12
12.1
12.3
12.4
12.42
$12.42
12.6
12.8
13
13%
13.24
$13.24
13.4
13.5%
13.5
$13.8
14
14.48
$14.48
14.9
15%
15.17%
15.5
15.7%
15.75%
16.2%
16.4
16.55
16.9
17
17.6
$17.60
18
18%
18.39%
18.5%
19%
19.02%
19.15
19.7
20
20%
20.2%
20.4
20.42
21
22
23%
23
23.2%
24
$24
24.9%
24.9
$24.97
25%
25
26
27.9
30
30%
$30.27
30.5%
$31
32%
32.01%
$32.95
34.23%
35%
36.73%
$37
40%
42
42%
45%
45
46.78%
$48
48.1%
49
50
$53
54.0%
$55
58.1%
58.19%
63.96%
67.94%
70
71
71.22
75%
$78
80%
$80
85%
90
$94
$100
100%
100
$105.93
$106
$110
$111
120
$125
$127
$149
150%
161
$165
$171.03
$174
175
$175
179.2
$205.77
205.77
210
$215
$244
$249
253.56
$253.56
$265
$270
$280
300
$316.8
370
433.4
$468
$538
$618.6
$638
$675.36
$675.4
2023
2025
2026
2027
2028
20261024
$1,710
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
{"meta":{"ticker":"IBM","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"International Business Machines"},"oneliner":"第三季軟體回到 9%、交易處理反彈 10%，延遲大單是遞延不是流失；但股價三個月漲兩成三、FY1 本益比 20 倍已反映復原，基本情境年化約 7%，等回檔或 2027 財測再動手","thesis":{"H":[{"id":"H1","text":"軟體段（Red Hat、Confluent、HashiCorp、交易處理）維持高個位數到雙位數成長，第二季交易型軟體失速屬遞延而非需求流失","2y":"FY2027 軟體固定匯率成長 ≥7%；高價值 ARR 於 FY2027 年底 ≥ $270 億","5y":"FY2030 軟體占公司營收過半，經常性占軟體比重 ≥85%","10y":null,"threshold":"高價值 ARR 年增 ≥7%（Q3 FY2026 為 $249 億、年增 8%）；軟體全年固定匯率成長 ≥7%","source":"IBM 季報新聞稿與法說（Q3 FY2026 軟體固定匯率 +9%、ARR $249 億 +8%）","drift_rule":"ARR 年增連 2 季低於 6.5% 為削弱、連 3 季低於 6% 為反轉"},{"id":"H2","text":"顧問段不因 AI 結構性萎縮，AI 轉型專案抵銷傳統專案通縮","2y":"FY2027 顧問固定匯率成長 ≥1%、簽約年增 ≥0","5y":null,"10y":null,"threshold":"顧問季度固定匯率成長 ≥0%；AI 占顧問營收 ≥30%、占在手訂單 ≥35%（Q3 FY2026 值）","source":"Q3 FY2026 法說：顧問 +2%、AI 約占顧問營收 30%、在手訂單 35%；Q2 FY2026 簽約 +6%","drift_rule":"連 2 季固定匯率成長 <0% 為削弱、連 3 季 <−2% 為反轉"},{"id":"H3","text":"生產力計畫每年推升營業稅前利潤率約 100bp，讓 EPS 在營收 4–5% 下仍有約 8% 成長、自由現金流每年增逾 $10 億","2y":null,"5y":"FY2030 營業利益率較 FY2025（18.5%）高 ≥300bp；FCF 每年正成長","10y":null,"threshold":"全年營業稅前利潤率擴張 ≥70bp；FY2026 FCF 年增逾 $10 億","source":"Q3 FY2026 法說（全年擴張 100bp 指引、FCF 上調）；年度營業利益率 FY2022 13.5% → FY2025 18.5%","drift_rule":"連 4 季利潤率年擴張 <50bp 為削弱、連 6 季 ≤0 為反轉"}],"R":[{"id":"R1","text":"AI 編碼工具（如 Claude Code）降低 COBOL 現代化成本，讓主機客戶移出核心系統，侵蝕交易處理與相關顧問","h_ref":"H1","clock":"🔥","threshold":"維持或增加容量客戶占比由約 85% 降至 80% 以下，或前 50 大銀行出現公開遷移案例","evidence_refs":["substitute_technology#2","substitute_technology#0"]},{"id":"R2","text":"交易型軟體與主機硬體的季度波動：z17 週期進入尾段（Q3 FY2026 Z 仍 −20%），第二季式的大單延遲重演","h_ref":"H1","clock":"⚡","threshold":"交易處理連 2 季年減 ≥5%，或軟體季度固定匯率成長 <6%","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#0","end_markets#1","capital_markets_pricing#2"]},{"id":"R3","text":"成長愈來愈靠併購與舉債：Confluent 全現金收購後淨負債由 $468 億升至 $538 億，軟體有機成長只有約 4 點","h_ref":"H3","clock":"🐢","threshold":"剔除併購的有機軟體成長連 4 季 ≤3%，或信用評等降至 BBB+ 以下","evidence_refs":["customer_concentration_credit#2","capital_markets_pricing#3"]},{"id":"R4","text":"估值已回到溢價：FY1 本益比 20.42 倍、RSI 71，七月賣方平均目標價約 $244 低於現價","h_ref":"H3","clock":"⚡","threshold":"FY1 本益比超過 22 倍而共識 EPS 未同步上修","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"single_thing":{"description":"前 50 大銀行中有一家公開宣布以 AI 工具完成核心交易系統移出 IBM 大型主機","why_fatal":"主機是 IBM 利潤與倍數的核心：每 1 美元主機帶 3–5 美元軟體，交易處理多以企業授權綁定；公開先例會讓市場把交易處理、Z 與相關顧問從永續收入重估為遞減資產，EPS 與倍數同時下修","if_happens":"清倉；終端倍數改用 14 倍以下重估","how_monitor":"每季法說的維持或增加容量客戶占比（Q3 FY2026 約 85%）、大型銀行與監管單位的核心系統遷移公告","probability":"約 10%（12–24 個月）：管理層稱沒有客戶離開主機的證據、裝機 MIPS 五年翻倍；但 2026-02 AI 工具發布當天股價重挫約 13%，市場認真看待此風險"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":19.15,"peg_fy2":2.4,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":11.17,"FY2026E":12.42,"FY2027E":13.24,"FY2028E":14.48},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識 non-GAAP 營業 EPS；FY2025A 用 GAAP 稀釋 EPS $11.17（事實表未涵蓋 FY2025 營業 EPS），基期口徑不同會高估三年年增率，FY2026→FY2028 同口徑年增約 8.0%"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/IBM_20261024/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"成熟現金流公司，營收 4–5% 成長，靠生產力擴利潤率與併購推軟體成長，股東回饋以股息為主"},"industry":{"clock_phase":"II","sd_verdict_source":"軟體經常性需求結構性持久；主機與交易處理屬週期性將反轉（z17 週期尾段），依據為 Q2 FY2026 Z 營收年減 42%、Q3 仍 −20%，以及管理層自述 z16 週期上市年持平、之後兩年才加速","bargaining":{"up":"對上游：記憶體、伺服器與儲存元件漲價時，客戶預算被硬體吸走（Q2 FY2026 實例），IBM 七月選擇不漲價","down":"對客戶：多年期企業授權綁定、轉換成本高、無單一客戶占營收 10% 以上；定價權存在但保守使用","geo":"業務遍及 175 國以上、約六成營收來自美國以外，貿易關係惡化列為風險因素但無量化揭露"},"profit_pool_dir":"管理層稱價值往 AI 編排與資料層移動；短期內硬體與記憶體端分走企業預算","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池占比；IBM 的成長來自既有客戶內擴容與併購，不是滲透率故事，改以分部成長與裝機容量判斷"}},"moat":{"mechanism":"主機核心交易系統的轉換成本＋多年期企業授權綁定交易處理與資料軟體；Red Hat 混合雲中立標準","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Q3 FY2026 軟體分部利潤率 +210bp、85% 裝機容量客戶維持或成長、z17 週期比前代多逾 $10 億；定價面縮減：七月未漲價、AI 編碼工具降低移轉成本、Z 營收 Q3 仍 −20%；兩者相抵為穩定","peer_na_reason":"事實表只有同業利潤率、無投入資本與 ROIC，改以毛利率與營業利益率對照","threats":[{"level":"🔴","text":"AI 編碼工具（如 Claude Code）降低 COBOL 現代化成本，讓主機客戶有能力把核心系統移出，侵蝕交易處理與相關顧問","p":30,"evidence_refs":["substitute_technology#2","substitute_technology#0"]},{"level":"🔴","text":"記憶體、伺服器漲價把企業預算從軟體挪到硬體，交易型軟體大單延遲（Q2 FY2026 實例）","p":25,"evidence_refs":["supply_demand_durability#0","end_markets#1"]},{"level":"🟡","text":"超大型雲端與服務商（MSFT、ACN 等）在 AI 平台與 AI 轉型顧問點對點競爭","p":20,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉（定性判斷：併購商譽與融資業務資產厚；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"主機承載核心交易，使用者（營運）、決策者（CIO）、付款者（銀行與零售）三角色都成立，屬需要而非想要；Q3 FY2026 約 85% 裝機容量客戶維持或增加容量，五年裝機 MIPS 翻倍"},{"item":"決策層級","level":"🟡","text":"替代決策發生在單一核心應用的遷移專案，代價是重寫、重新驗證與停機風險，多年期企業授權拉長決策週期；但 AI 編碼工具正壓低重寫成本，2026-02 相關發布當天股價重挫約 13%，替代門檻在下降"},{"item":"價值鏈分配","level":"🟡","text":"Q2 FY2026 客戶把預算轉去搶購漲價約 30% 的伺服器、儲存與記憶體，硬體供應端在當下分走較多價值；IBM 以每 1 美元主機帶 3–5 美元軟體維持自己的份額，但互補品漲價時沒有轉嫁"},{"item":"社會容忍度","level":"🟢","text":"未見針對 IBM 的新反壟斷案或拆分調查，管理層稱監管對併購更友善；唯一監管事件為 2026-04 以 $1,710 萬和解的反歧視證明案，已結案；依賴的不是監管授權"}],"roiic":"事實表未涵蓋投入資本與歷次收購金額，無法算增量報酬；可追溯的部分：營業利益由 FY2023 約 $94 億（$618.6 億 × 15.17%）增至 FY2025 約 $125 億（$675.4 億 × 18.5%），兩年增約 $31 億，對應的新增投入未揭露","reinvest_rate":"2026 年 Confluent 約 $110 億全現金收購，接近一整年稅後營業利益（約 $106 億＝$125 億 × (1 − 約 15% 稅率)），屬一次性高峰；常態再投資率事實表未涵蓋","endo_ceiling":5.0,"formula_note":"無法以增量 ROIC × 再投資率正式推導；以管理層長期營收成長目標逾 5%（2025 投資人日）與 Q3 軟體有機成長約 4 點作為內生上界代理，利潤率擴張與併購另列為缺口來源"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","IBM":58.1,"ACN":32.01,"ORCL":63.96,"MSFT":67.94,"HPE":36.73,"unit":"%"},{"metric":"營業利益率","IBM":18.39,"ACN":15.75,"ORCL":34.23,"MSFT":46.78,"HPE":7.84,"unit":"%"},{"metric":"FCF 利潤率","IBM":19.02,"ACN":17.21,"ORCL":-40.01,"MSFT":20.19,"HPE":9.93,"unit":"%"},{"metric":"研發密度","IBM":12.67,"ACN":null,"ORCL":14.19,"MSFT":10.72,"HPE":8.85,"unit":"%"}],"competitors":[{"name":"ACN","gm":32.01,"om":15.75,"fcf_margin":17.21,"rd_intensity":null,"strategy_note":"純服務商、毛利結構遠低於 IBM，是顧問段 AI 部署的正面對手；IBM 顧問 Q3 僅 +2%，未拉開差距","period":"TTM ending 2026-05-31（4季加總）"},{"name":"ORCL","gm":63.96,"om":34.23,"fcf_margin":-40.01,"rd_intensity":14.19,"strategy_note":"資料庫加雲端重資本擴張，近一年自由現金流轉負，路線與 IBM 輕資本混合雲相反，競爭點在大型企業資料庫與核心系統","period":"TTM ending 2026-08-31（4季加總）"},{"name":"MSFT","gm":67.94,"om":46.78,"fcf_margin":20.19,"rd_intensity":10.72,"strategy_note":"利潤率遠高於 IBM，是 AI 平台與雲的主要對手；IBM 以混合雲中立、本地部署與主權 AI 區隔","period":"TTM ending 2026-06-30（4季加總）"},{"name":"HPE","gm":36.73,"om":7.84,"fcf_margin":9.93,"rd_intensity":8.85,"strategy_note":"混合基礎設施對手、利潤率明顯較低；IBM 稱儲存與 Power 本季取得份額，但事實表未涵蓋份額數字","period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"量（裝機容量、OpenShift 採用）為主、價格（容量變現）次之、併購約占軟體成長一半、無回購；EPS 另加利潤率擴張約 3pp","runway_years":"5~9","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 5%：以管理層長期營收成長目標逾 5% 與軟體有機約 4 點代理；共識 EPS 年增約 8% 超出約 3pp，歸因利潤率擴張（每年營業稅前利潤率約 +100bp）","segments":[{"item":"軟體（Q3 FY2026）","value":"$78 億，固定匯率 +9%；Red Hat +11%、資料 +20%、交易處理 +10%，全年指引約 7%–8%"},{"item":"顧問（Q3 FY2026）","value":"$53 億，固定匯率 +2%；AI 占顧問營收約 30%、在手訂單 35%，全年指引低至中個位數"},{"item":"基礎設施（Q3 FY2026）","value":"$37 億，固定匯率 +5%；分散式基礎設施 +32%、IBM Z −20%，全年指引低個位數"},{"item":"利潤結構","value":"軟體分部利潤率 +210bp、基礎設施 +120bp、顧問小幅下滑（把生產力收益再投資於數位資產）"}],"decay_signals":["替代技術壓縮可用市場：亮（AI 編碼工具降低主機移轉成本，2026-02 單日重挫約 13%）","毛利率連 2 季年減：未亮（毛利率 FY2022 54.0% 起逐年升至 FY2025 58.19%，TTM 58.1%）","EPS 成長高於營收成長逾 5pp：未亮（約 8% 對 4–5%，差 3–4pp）","SBC 占營收逾 5% 且上升：未亮（Q3 SBC $5.35 億 ÷ 營收 $171.03 億約 3.1%）","核心市占縮減：資料不足（事實表未涵蓋份額）","產業估值倍數近 3 年下移：資料不足（事實表未涵蓋同業倍數歷史）"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"股息","value":"前九月 $48 億；TTM 殖利率約 2.66%"},{"item":"併購","value":"Confluent 約 $110 億全現金（2026 年完成）；HRL Laboratories 條件未揭露"},{"item":"回購","value":"法說未提，事實表未涵蓋"},{"item":"負債","value":"Q3 末債務 $638 億（含融資業務 $127 億）、現金 $111 億；6 月底淨負債 $538 億（2025 年底 $468 億）"}],"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"HashiCorp、Confluent 等收購的已實現增量報酬事實表未涵蓋；Confluent 2026 年才併入，資料段 +20% 有貢獻但無利潤數字","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"前九月股東回饋 $48 億全為股息，法說未提回購","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營業稅前利益 16.2%（Q3 FY2026）；股數變動事實表未涵蓋，淨稀釋率無法計算","grade":"不過"}]},"valuation":{"basis":"FY1 non-GAAP 營業 EPS 本益比＋PEG","tier":"成熟軟體與 IT 服務混合","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業本益比，無法做同層級倍數對照"},"fwd_pe":20.42,"peg":2.56,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 本益比 20.42 倍、PEG 約 2.6（20.42 ÷ 共識 EPS 兩年年增 8.0%）；基本情境五年年化約 7% 低於 8%；三個月股價 +23% 對共識 EPS +0.7%，重估已發生；五年百分位事實表未涵蓋 → 偏貴","upside_short_pct":-3.8,"upside_mid_pct":24.9},"trap_analysis":{"verdict":"🟡","label":"成熟現金流公司復原中，主機替代風險未解、估值已回到溢價"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2026-02 AI 編碼工具宣布可做 COBOL 現代化當天股價重挫約 13%；10-K 風險因素自列顛覆性技術；Q3 FY2026 Z 營收仍 −20%","assumption":"主機客戶的移轉成本長期高到不值得搬","consequence":"若前幾大銀行陸續搬離，交易處理、Z 與主機現代化顧問這組高毛利來源轉為遞減，EPS 停在 $12–13、倍數降到 14 倍以下，五年虧三到四成","ruling":"部分採納，已放入 30% 的 Bear 機率；目前反證較強：裝機 MIPS 五年翻倍、約 85% 裝機容量客戶維持或增加、z17 比前代多逾 $10 億，IBM 也把 AI 工具用在主機上的現代化","watch":"每季法說的「維持或增加容量客戶占比」、大型銀行核心系統遷移公告","evidence_refs":["substitute_technology#2","substitute_technology#0"],"fact_refs":[]},{"view":"論點失敗","evidence":"CEO 四月稱伊朗戰爭與地緣不確定性開始經由客戶影響展望；第二季客戶把預算轉去搶購漲價中的伺服器、儲存與記憶體，數十件大單延遲","assumption":"客戶 IT 預算分給 IBM 軟體的比例穩定","consequence":"交易型軟體（約占軟體 20%）再度延後，全年指引第二次下修，市場把第三季反彈視為一次性","ruling":"部分採納：第三季已收回約三分之二延遲單，但硬體漲價擠預算的機制沒有消失","watch":"記憶體與伺服器價格、管理層對預算挪移的說明、交易型軟體季增","evidence_refs":["geo_supply_chain#0","end_markets#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Confluent 約 $110 億全現金收購後淨負債由 $468 億升至 $538 億；賣方因併購稀釋與顧問轉弱下修 2026 EPS；SBC 占營業稅前利益 16.2%；前九月回饋全為股息、未見回購","assumption":"軟體成長能靠有機與既有併購延續，不需要再付高價收購","consequence":"營收與 EPS 達標，但每股價值被高價併購、利息與 SBC 吃掉，股息之外沒有回購撐每股","ruling":"採納為中度風險：管理層稱 2027 為併購綜效年，CFO 同時提到有機與無機並行；若再有逾 $100 億併購，資本配置風險升級","watch":"下一筆收購金額、淨負債與信用評等","evidence_refs":["customer_concentration_credit#2","capital_markets_pricing#3"],"fact_refs":["f_kpi5_sbc_operating"]},{"view":"價格已反映太多","evidence":"FY1 本益比 20.42 倍（三個月前約 16.9 倍）、RSI 71.22、26 週 +10.9%；七月賣方平均目標價約 $244、HSBC $175，均低於現價（皆為 Q3 前資料）","assumption":"市場會持續給復原中的 IBM 20 倍以上","consequence":"即使 EPS 照共識走，倍數回到 17–18 倍就吃掉兩年的 EPS 成長","ruling":"採納：這是本次不追價的主要原因","watch":"FY1 本益比與共識 EPS 上修幅度之間的差距","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_rsi14","f_week26_return_pct","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-40,"hi":-25,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 205.77 → 本次 253.56（+23.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=205.77","side_b":"本次 price_at_dd=253.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 205.77 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 205.77 美元：Bull 價 370、Bear 價 161，五年期望值 +30.5%，基準年化 6.7%，不對稱比 3.0","side_b":"本次情境、股價仍用 205.77 美元：Bull 價 433.4、Bear 價 179.2，五年期望值 +48.1%，基準年化 9.0%，不對稱比 7.14","ruling":"先換情境、股價不動：五年期望值多 17.6 個百分點，基準年化多 2.3 個百分點。不對稱比由 3.0 變為 7.14。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 205.77 美元：五年期望值 +48.1%，基準年化 9.0%，不對稱比 7.14","side_b":"本次情境、股價 253.56 美元：五年期望值 +20.2%，基準年化 4.6%，不對稱比 2.02","ruling":"再換股價、情境不動：起點價上漲 23.2%，五年期望值少 27.9 個百分點，基準年化少 4.5 個百分點，不對稱比由 7.14 降到 2.02。合計五年期望值比前份少 10.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"第二季主機與交易處理失速是遞延還是流失","cause":"新證據","prior_field":null,"side_a":"第二季：交易處理 −9%、Z −42%，全年營收指引由逾 5% 下修至 4–5%，CFO 預期下半年交易處理下降低至中個位數","side_b":"第三季：交易處理 +10%、軟體 +9%，約三分之二延遲大單成交，z17 週期比前代多逾 $10 億，約 85% 裝機容量客戶維持或成長","ruling":"可調和：採第三季證據，遞延說法成立；但第三季同時吃到遞延單與正常購買週期，CEO 自承交易處理雙位數不會延續、全年交易處理指引為持平，因此只確認沒有流失，不確認加速","evidence_level":"公司財報與法說（一手）","settle_metric":"FY2027 交易處理全年成長率（管理層自述 z16 週期：上市年持平、次年中個位數、第三年高個位數）","if_then":["若 FY2027 前兩季交易處理年增 ≥3%，則確認 z16 式週期，Base 機率維持 45%","若 FY2027 任兩季交易處理年減 ≥5%，則 Bear 機率升至 40%、放棄建倉"],"evidence_refs":["end_markets#1","supply_demand_durability#0","capital_markets_pricing#2","competitive_share_entrants#1"]},{"axis":"管理層前後說法對帳","cause":"新證據","prior_field":null,"side_a":"2026-07-22 CEO（Krishna）：三週內約三分之一延遲交易成交，「尚非完整證據」；CFO（Kavanaugh）說約 40%，並把交易處理改列為 2027 年成長動能","side_b":"2026-10-21 CFO（Kavanaugh）：約 $4 億延遲軟體單收回三分之二、約 $2.5 億，占軟體加速的四分之一，其餘四分之三為新業務；全年軟體基本情境上調至約 7%","ruling":"可調和：數字前後一致且有進展，第二季給的保守基準被第三季超越，管理層可信度回升；但剩餘三分之一未收回，第二季被問到另外 15% 主機容量去向時沒有回答，仍是未解問題","evidence_level":"法說逐字稿（一手）","settle_metric":"Q4 FY2026 資料與自動化段是否收回剩餘延遲單；下一次法說是否揭露其餘 15% 容量客戶的狀態","if_then":["若 Q4 FY2026 軟體達全年 7% 以上，則管理層指引視為可信，不再對指引打折","若 Q4 FY2026 軟體全年低於 7%，則把 2027 財測打九折估算"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買：遞延已證、出貨 MIPS 增逾 100% 為 2027 交易處理變現鋪路、Red Hat 訂單回到高十幾、前九月 FCF 利潤率創新高、FCF 指引上調","side_b":"不追：FY1 本益比 20.42 倍已較三個月前約 16.9 倍重估，PEG 約 2.6，基本情境年化約 7% 低於 8%，RSI 71.22 過熱","ruling":"方向相反的估值分歧，不是論點矛盾：選不追。依據：Base EPS 年增約 7% 加股息約 2.7% 已等於基本情境全部報酬，股價再漲只能靠倍數再擴張；硬數據為 FY1 本益比 20.42 倍","evidence_level":"事實表價格與共識（一手）","settle_metric":"FY1 本益比；FY2027 共識 EPS","if_then":["若股價回到約 $215（FY1 本益比約 17 倍）且軟體成長未低於 7%，則分批建首倉至 2%","反向：若 2027 財測軟體 ≥8% 且 FY2027 共識上修至 ≥$13.8，而股價未超過 $265，則直接建首倉 2%"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"前份估值與機率欄位漂移","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-07-23，股價 $205.77）：估值中性、FY1 本益比約 16.9 倍、Bull／Bear 機率 25%／30%、最大回撤 −35%","side_b":"本次（股價 $253.56）：估值偏貴、FY1 本益比 20.42 倍；機率維持 25／45／30，最大回撤改為範圍 −25% 至 −40%","ruling":"估值結論由中性降為偏貴，完全來自股價上漲約 23%，而共識 FY1 EPS 三個月只上修 0.73%；機率不動，因 Q3 的好消息已反映在 Base 終端 EPS，且共識成長超出內生上界，Bear 仍需至少 30%；最大回撤改成範圍、中點與前份相近","evidence_level":"事實表價格與共識","settle_metric":"FY1 本益比","if_then":["若 FY1 本益比回到 17 倍以下，估值結論回到中性"],"evidence_refs":[]},{"axis":"前份基本面欄位對帳","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質中上、價值陷阱風險中等、護城河持平、五年後成長跑道中等、品質複利成長型、非循環股、結論觀望","side_b":"本次：各欄不變。Q3 證據（軟體 +9%、交易處理 +10%、利潤率擴張、FCF 上調）強化軟體論點，但 Z 營收 −20% 與 AI 編碼工具威脅未解，相抵後各欄不動；軟體 ARR 兩年門檻由 $280 億改為 $270 億，因 ARR 年增穩在 8%、未見回到 10%","ruling":"維持：新證據讓延遲屬遞延得到確認，但沒有改變護城河方向或成長跑道；結論維持觀望的原因從「基本面未確認」換成「價格已反映」","evidence_level":"公司財報與法說（一手）","settle_metric":"2027 財測軟體成長","if_then":["若 2027 財測軟體 ≥8% 且交易處理轉正，則重評護城河方向是否轉為擴大"],"evidence_refs":[]},{"axis":"重啟條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Q3 2026（~10 月）軟體回升至 ≥ 高個位數 cc + 滑單 ≥ 75% 收回 + 無第三次砍 guide；或 Fwd PE ≤ 13.5x（~$165）之同業折價","side_b":"FY1 本益比回到 17 倍以下（約 $215）且軟體固定匯率成長未低於 7%；或 2027 財測軟體 ≥8% 且股價未超過 $265","ruling":"前份三項條件兌現兩項（軟體固定匯率 +9%、未再砍指引並上調 FCF），延遲單收回約三分之二、未達 75%；同時股價已大漲，約束從基本面轉為價格，重啟條件改為價格錨，觸發後分批建倉、不追","evidence_level":"公司財報與法說（一手）","settle_metric":"FY1 本益比","if_then":["觸發價格條件後分三批建倉，每批間隔一季財報"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標（空值）","side_b":"軟體固定匯率成長連兩季 <5%；交易處理連兩季 ≤−5%；顧問連兩季 <0%；FY2027 FCF 年增 <0","ruling":"新增：任一觸發即減碼，兩項同時觸發即清倉；門檻取自前份 R1、R2 的監測方向並改為可直接讀季報的數字","evidence_level":"方法調整","settle_metric":"各季報","if_then":["任一指標觸發則減碼一半","兩項同時觸發則清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（空值）","side_b":"前 50 大銀行中有一家公開宣布以 AI 工具完成核心交易系統移出 IBM 大型主機","ruling":"新設：主機加交易處理是利潤與倍數的最大單一敏感項，公開先例會同時壓 EPS 與倍數；觸發即清倉","evidence_level":"方法調整","settle_metric":"公開遷移公告；維持或增加容量客戶占比","if_then":["若出現一例公開遷移，則清倉","若占比由約 85% 降至 80% 以下，則減碼一半"],"evidence_refs":["substitute_technology#2"]}],"triggers":[{"n":1,"text":"Q4 FY2026 軟體全年成長確認","type":"假設驗證","maps_to":"H1","metric":"軟體全年固定匯率成長","threshold":"≥7%","action":"未達則 Base 機率降至 40%、Bear 升至 35%，不建倉","source_freq":"季報（每季）","date":"2027-01"},{"n":2,"text":"交易處理再度失速","type":"風險","maps_to":"R2","metric":"交易處理軟體季度年增率","threshold":"連 2 季 ≤−5%","action":"減碼至零、放棄建倉","source_freq":"季報（每季）","date":null,"evidence_refs":["end_markets#1","supply_demand_durability#0","competitive_share_entrants#1"]},{"n":3,"text":"前 50 大銀行公開移出大型主機","type":"Single Thing","maps_to":"R1","metric":"公開遷移公告；維持或增加容量客戶占比","threshold":"出現一例，或占比低於 80%","action":"清倉","source_freq":"新聞與每季法說","date":null,"evidence_refs":["substitute_technology#2","substitute_technology#0"]},{"n":4,"text":"價格回到合理區","type":"估值rearm","maps_to":"H3","metric":"FY1 本益比","threshold":"≤17 倍（約 $215）且軟體成長 ≥7% 未破","action":"分批建首倉至 2%","source_freq":"每日","date":null,"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"n":5,"text":"大單延遲揭露的證券集體訴訟正式提起並獲集體認證","type":"風險","maps_to":"R2","metric":"集體訴訟程序進度","threshold":"正式起訴且獲集體認證","action":"持倉減半、凍結加碼","source_freq":"SEC 申報與法院公告","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":6,"text":"顧問段轉負","type":"風險","maps_to":"H2","metric":"顧問固定匯率營收年增","threshold":"連 2 季 <0%","action":"Bear 機率升至 35%、停止加碼","source_freq":"季報（每季）","date":null,"evidence_refs":["substitute_technology#0"]},{"n":7,"text":"FY2026 自由現金流兌現","type":"假設驗證","maps_to":"H3","metric":"FY2026 FCF 年增額","threshold":"逾 $10 億","action":"未達則 H3 削弱、Base 終端倍數降至 17 倍","source_freq":"年報","date":"2027-01"},{"n":8,"text":"客戶預算再被硬體漲價或地緣衝突擠壓","type":"風險","maps_to":"R2","metric":"全年營收指引","threshold":"再次下修","action":"Bear 機率升至 40%、放棄建倉","source_freq":"季報（每季）","date":null,"evidence_refs":["geo_supply_chain#0","customer_concentration_credit#2","capital_markets_pricing#2"]},{"n":9,"text":"2027 財測與軟體長期目標量化","type":"複審日期","maps_to":null,"metric":"2027 軟體成長指引","threshold":"≥8% 視為加速、<6% 視為減速","action":"重跑完整判斷","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"軟體段固定匯率年增率","bear_threshold":"連兩季 <5%","window":"2027 年各季","source":"IBM 季報新聞稿（8-K Ex.99.1）","last_status":"ok"},{"metric":"交易處理軟體年增率","bear_threshold":"連兩季 ≤−5%","window":"2027 年各季","source":"IBM 季報法說","last_status":"ok"},{"metric":"顧問段固定匯率營收年增率","bear_threshold":"連兩季 <0%","window":"2027 年各季","source":"IBM 季報新聞稿（8-K Ex.99.1）","last_status":"ok"},{"metric":"全年自由現金流年增額","bear_threshold":"FY2027 年增 <0","window":"FY2027 全年","source":"IBM 10-K","last_status":"ok"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#0","reason":"事件已於 2026-04-10 以 $1,710 萬和解結案，指控屬反歧視證明不實而非反壟斷，證據本身沒有後續程序、也沒有對應的營收或業務限制可延伸到未來現金流"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=10.9, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"FY1 本益比回到 17 倍以下（約 $215）且軟體固定匯率成長未低於 7%；或 2027 財測軟體 ≥8% 且股價未超過 $265","exec_line":"不追高；觸及重啟條件後分三批建首倉至 2%，每批間隔一季財報；2027 財測軟體 <6% 則取消"},"reasoning":{"industry":"最新一季（Q3 FY2026）營收 $171.03 億，年增 5%（固定匯率 6%）；分部：軟體 $78 億（固定匯率 +9%，其中 Red Hat 與混合雲 +11%、資料 +19%、交易處理 +9%～10%）、顧問 $53 億（固定匯率 +2%）、基礎設施 $37 億（固定匯率 +5%，其中 IBM Z −20%、分散式基礎設施 +32%）。三段皆超過營收 10%。營業（non-GAAP）稅前利益 $32.95 億、GAAP 稅前利益 $24.97 億；TTM 毛利率 58.1%、營業利益率 18.39%。軟體約 80% 為經常性收入（高價值 ARR $249 億、年增 8%），其餘 20% 為交易型、與主機企業授權綁定，第二季失速、第三季反彈的波動就出在這 20%。客戶不集中：2023–2025 年無客戶占營收 10% 以上，約六成營收來自美國以外。全年指引：固定匯率營收成長 4%–5% 維持、FCF 年增上調至逾 $10 億。產業態勢屬雙向拉鋸：競爭面，AI 編碼工具壓低主機程式移轉成本（惡化）；結構面，主權 AI 與本地部署需求、記憶體與伺服器漲價讓主機總持有成本優勢擴大（轉好）。產業時鐘在擴張期：企業 AI 支出擴大，第三季三個分部同時加速。供需持久性：軟體經常性需求屬結構性持久；主機硬體與交易處理屬週期性，z17 週期已過高峰，2027 年將回到正常化。單點依賴：主機是利潤核心，這是護城河證據也是集中風險。","moat":"機制：主機承載多數大型金融與零售核心交易，客戶以多年期企業授權把交易處理、資料與自動化軟體綁在主機上，搬家要重寫核心系統與重新驗證，轉換成本高；Red Hat OpenShift 以混合雲中立標準延伸到主機以外。方向證據：執行面，Q3 FY2026 軟體分部利潤率 +210bp、基礎設施 +120bp，約 85% 裝機容量的客戶維持或增加容量，z17 週期至今比前代多逾 $10 億營收（擴大）；定價面，七月未漲價、AI 編碼工具讓 COBOL 現代化變便宜、Q3 Z 營收仍 −20%（縮減）。同業對照（事實表只有利潤率、無 ROIC）：IBM TTM 毛利率 58.1%、營業利益率 18.39%，高於 ACN（32.01%／15.75%）與 HPE（36.73%／7.84%），低於 MSFT（67.94%／46.78%）與 ORCL（63.96%／34.23%）；位置在服務商與純軟體之間，與其混合結構一致。執行力 7、定價權 7，合併 7 分。","growth":"成長來源：量為主（裝機 MIPS 擴大、OpenShift ARR $24 億年增逾 30%），價格次之（容量擴大後的交易處理變現），併購約占軟體成長一半（Q3 軟體 9% 中有機逾 4 點，其餘多為 Confluent）；前九月回饋全為股息，沒有回購助攻。三年共識 EPS：FY2026 $12.42 → FY2027 $13.24 → FY2028 $14.48，FY2026 起兩年年增約 8.0%；若以 FY2025 GAAP 稀釋 EPS $11.17 為基期約 9.0%，但口徑不同會高估。內生上界約 5%（代理值，見護城河段），缺口約 3pp 歸因於利潤率擴張：全年營業稅前利潤率指引 +100bp、累計生產力逾 $55 億，Q3 營業稅前利潤率 +70bp；此缺口可歸因，不屬於依賴重估。成長是否持久看三件事：交易處理能否複製 z16 週期（上市年持平、次年中個位數、第三年高個位數）、Red Hat 訂單高十幾能否轉成營收、顧問能否從低個位數加速。衰退訊號：亮 1 個（替代技術壓縮可用市場）。Runway 5–9 年：成熟市場不以滲透率衡量；量子（Quantum Day 2026-12-10）仍屬早期，不算已證實的下一條曲線。","governance":"現金產出：Q3 FCF $30.27 億，前九月約 $80 億、年增約 8%，FCF 利潤率為歷史最高；全年 FCF 年增指引上調至逾 $10 億。TTM FCF 利潤率 19.02%，對照 FY2025 淨利率約 15.7%（$105.93 億 ÷ $675.36 億），FCF 對淨利轉換約 1.2 倍。SBC 占營業稅前利益 16.2%（約占營收 3.1%）。現金去向：股息前九月 $48 億；併購 Confluent 約 $110 億全現金；回購法說未提、事實表未涵蓋；資本支出上升（CFO 說法，金額未揭露）。負債：Q3 末債務 $638 億（含融資業務 $127 億）、現金 $111 億；6 月底淨負債 $538 億，較 2025 年底 $468 億增加，主因 Confluent；評等 S&P A-、Moody's A3、Fitch A- 維持。三項評分：併購增量報酬無法驗證、回購不適用、SBC 淨稀釋率因股數變動未涵蓋而無法計算。","valuation":"現價 $253.56，FY1（FY2026E）共識 EPS $12.42，本益比 20.42 倍；FY2 $13.24 對應 19.15 倍。PEG＝20.42 ÷ 8.0%（FY2026→FY2028 共識年增）約 2.6，高於 2。共識近三個月只上修 0.73%，但股價自前份判斷（$205.77）上漲約 23%，等於倍數由約 16.9 倍重估到 20.4 倍，漲幅幾乎全來自倍數。股息殖利率約 2.66%。基本情境：FY2031 EPS $17.60 × 18 倍＝$316.8，較現價 +24.9%，加股息年化約 7%，落在弱區。短期參考：七月（Q3 財報前）賣方平均目標價約 $244，較現價約 −3.8%，但該數字未反映 Q3，參考性有限。五年本益比百分位：事實表未涵蓋估值歷史高低點，無法計算。同業倍數：事實表未涵蓋。分母採 non-GAAP 營業 EPS，與 GAAP 稅前差約每季 $8 億（$32.95 億對 $24.97 億，多為併購攤銷），屬一貫口徑，不視為爭點。","premortem":"三個方向的反證見反證紀錄：論點失敗（AI 工具降低移轉成本、客戶預算被硬體擠壓）、股東經濟變差（高價併購與負債上升、無回購）、價格已反映太多（20.4 倍、RSI 71.22、26 週 +10.9%）。衰退訊號亮 1 個，週線均線排列過但長均線走平。"},"plain":{"six":{"how_it_makes_money":"IBM 賺的是大企業關鍵系統的錢：大型主機與其上的交易處理軟體（多年期企業授權綁定）、Red Hat 混合雲訂閱、加上顧問；錢卡在大型主機裝機容量這一節點，每 1 美元主機硬體帶動 3–5 美元軟體","moat":"護城河持平：主機加企業授權的轉換成本仍在、軟體利潤率在擴張，但 AI 編碼工具壓低移轉成本、主機硬體仍在下滑，兩邊相抵","growth":"五年後跑道中等：既有主機與軟體客戶內持續擴容，但五年後沒有已證實的第二條成長曲線","capital":"資本配置中段：現金流穩、股息可靠，但沒有回購、成長靠併購加債，增量報酬無法驗證","valuation":"現價要求 IBM 在 20 倍以上的本益比下維持約 8% 的 EPS 成長五年；我信成長，不信倍數能守住，估值偏貴","how_wrong":"價值陷阱風險中等：最可能看錯的是 AI 編碼工具讓主機客戶真的搬走，其次是倍數回落吃掉 EPS 成長"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 FY1 本益比回到 17 倍以下（約 $215），或 2027 年 1 月財測確認軟體 ≥8% 且股價未超過 $265","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":253.56,"week26_return_pct":10.9,"consensus_rev_3m_pct":0.73,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"non-GAAP 與 GAAP 稅前差約每季 $8 億，主要為併購攤銷等，口徑一貫，不構成爭點"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Confluent Streamhouse 發布","impact":"低","watch":"資料段交叉銷售是否讓 Q4 資料段維持 15% 以上"},{"date":"2026-12-10","date_precision":null,"type":"product","event":"IBM Quantum Day（量子路線圖與商業化進度）","impact":"低","watch":"有沒有量子營收或簽約金額的具體數字"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 2027 全年財測、軟體長期目標量化","impact":"高","watch":"2027 軟體成長指引是否 ≥8%、交易處理是否轉為成長、FCF 年增是否兌現逾 $10 億"}],"_projected_from":"v19"}
```
