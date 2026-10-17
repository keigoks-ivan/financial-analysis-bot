你是 stock-analyst v20 的**散文層（prose）agent**，標的 ASML（2026-10-17）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ASML_20261017/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ASML　日期：2026-10-17　archetype：None　前份裁決：2026-07-16　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1661B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（495B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1002B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1394B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1173B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（517B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（859B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2242B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3978B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2830B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1661           3737-5339      5 條（2–6 內）  
s3                  8000         495           5254-7505      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3569          8002-11431      5 條（2–6 內）  
s6                 11000         517          7338-10483      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         859           1849-2641      5 條（2–6 內）  
s10                 5000        2242           1931-2758      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2830           2000-2170      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4842B；至少需散文≈40.16KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−50%
−44%
−35%
−35
−30%
−9.6%
0
0.4
0.41
0.5
0.55
0.55%
0.75
0.85
0.9
01
1
1.1
1.14
1.15
1.20
1.27
1.3
1.7%
1.88
2.0
2
2%
2.2
2.4
2.4%
2.55
2.9%
3
3.1
3.29
3.6
3.63
3.7
4
4.1
4.3
4.96
5
5%
6
6%
06
6.1%
6.5
6.7
7
07
7.0%
08
8%
8
8.3%
8.4
9
9%
9.6
9.6%
10%
10
10.8
11.0
11
11.3%
11.3
11.4
11.66
12
12.7
12.8%
12.84
13
13%
13.8%
14
14.1%
14.2
15
15%
15.2
15.8
16
16.5
17
18
19%
20
20%
21.8%
22
24.71
25%
25
26
28%
28
28.2
28.24
28.7%
30%
30
30.7%
31
32
33%
33.4%
33.9%
34.6%
35%
35
35.4%
36%
36
37.0%
37.7
38
38.2
38.23
40%
40
41
42
42.94
44
44.5
45
45%
46%
46
48.0%
49
50
50%
51
51.3%
51.9
52
53%
54
54%
54.2%
55
56%
56.1%
57%
57
57.2
57.5%
58
58.13
60%
60
65%
65
65.2%
66.3%
70
75%
76.46
82
85
86
90%
94
98
100%
100
110
125
143.9
150%
200
229.5
232
260
330
350
394
828
920
1641.52
1815.27
2022
2023
2024
2025
2026
2027
2028
2029
2030
2031
2033
2036
2330
3800
20261017
$1,500
$1,650
1,074
1,100
1,271
1,500
1,641.52
1,650
1,780
1,815.27
1,860
1,970
2,132
2,444
2,623
2,676
3,449
4,000
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
{"meta":{"ticker":"ASML","date":"2026-10-17","schema":"v15.0","contract":"v19","company_name":"ASML Holding N.V."},"oneliner":"EUV獨家供應商，2027–28產能仍供不應求，首次談成關鍵機台漲價；FY2027前瞻本益比約28倍，股價已回到前份設定的加碼價位；最大風險是2028後客戶擴產放緩，讓高點盈利回落。","thesis":{"H":[{"id":"H1","text":"產能吃緊延續至2028：2027營收依共識成長約28%，由產能擴充30%與漲價推動。","2y":"2027營收≥€52bn；2027年低NA EUV出貨較2026年約65台增約30%","5y":null,"10y":null,"threshold":"2027年營收展望中位數≥€52bn（共識€57.2bn的九成）；非流動負債不連2季下降","source":"ASML 2027年1月第四季財報與年度展望；季報資產負債表","drift_rule":"營收或財測較共識路徑連2季偏離≥5%＝削弱，連3季≥10%＝反轉"},{"id":"H2","text":"定價權上移：漲價2027起反映、2028全面，High-NA成為第二曲線（三星2028、台積電2030量產）。","2y":null,"5y":"2028–2030毛利率維持≥57%；High-NA年出貨逐年增加","10y":null,"threshold":"FY2028毛利率≥57%（2026約56%）；三星High-NA量產不晚於2028、台積電不晚於2030","source":"ASML季報、2027-06-10資本市場日、客戶製程藍圖公告","drift_rule":"近四季毛利率連4季低於門檻5%以上（<54.2%）＝削弱，連6季低於10%以上（<51.3%）＝反轉"},{"id":"H3","text":"EUV與High-NA是先進邏輯與DRAM的必要工具，安裝基礎服務隨裝機數累積，墊高營收底部。","2y":null,"5y":null,"10y":"2036年前無量產級替代微影路線；安裝基礎管理營收占比維持≥25%","threshold":"安裝基礎管理占總營收≥25%（2026第三季約28%）；無客戶以非ASML的EUV量產先進節點","source":"ASML年報業務別揭露、客戶量產公告","drift_rule":"跨2個年度低於門檻＝削弱，跨3個年度＝反轉"}],"R":[{"id":"R1","text":"出口管制擴大：MATCH Act擬把禁令擴及DUV與維修，美方調查EUV是否流入中國；中國約占2026營收20%。","h_ref":"H1","clock":"⚡","threshold":"MATCH Act成法且荷蘭執行，或中國全年營收占比<10%","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","substitute_technology#4","regulatory_antitrust#0","reg_tariff_export#0"]},{"id":"R2","text":"需求囤貨或AI資本支出2028見頂，2029–30營收回落；另有2024年期間的美國證券集體訴訟未決。","h_ref":"H1","clock":"🔥","threshold":"非流動負債連2季下降，或2027年1月展望<€52bn","evidence_refs":["customer_concentration_credit#2","major_events#0","lawsuit_class_action#0"]},{"id":"R3","text":"客戶集中與議價反撲：前兩大客戶FY2021合計66.3%，集中度往台積電上升；台積電嫌High-NA貴、延到2030。","h_ref":"H2","clock":"🐢","threshold":"台積電再延後High-NA量產時程，或FY2028毛利率<57%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_second_source#0"]},{"id":"R4","text":"光學唯一供應商Zeiss：若產能跟不上或關係中斷，ASML實質無法出貨。","h_ref":"H1","clock":"🐢","threshold":"管理層承認光學供應限制出貨，或年出貨低於產能計畫一成","evidence_refs":["geo_supply_chain#0"]},{"id":"R5","text":"替代技術與新進者：中國DUV、自由電子雷射光源、Nikon、較不依賴微影的新架構。","h_ref":"H3","clock":"🐢","threshold":"任一對手取得先進節點量產訂單並通過客戶驗證","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","substitute_technology#0"]}],"single_thing":{"description":"2027年1月ASML公布的2027年展望低於€52bn，或宣布縮減2027–2028產能擴充（代表客戶擴產延後）。","why_fatal":"基準路徑FY2027–28每股盈餘58.13→76.46的成長主要靠出貨量（產能年增30%）；量能不到位，漲價與升級業務撐不住，2028年後的盈利高原假設瓦解，盈利與倍數會同時下修。","if_happens":"減碼至三分之一並重跑研究；悲觀機率上調至40%以上。","how_monitor":"2027年1月第四季財報展望；每季非流動負債（預付款）變動；主要客戶資本支出與建廠公告。","probability":"15%：客戶已用預付款下單、管理層稱供不應求至2028，但2026年4月全年指引仍只有€36–40bn，半年內變動逾一成，能見度波動大。"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":28.24,"peg_fy2":0.85,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":24.71,"FY2026E":42.94,"FY2027E":58.13,"FY2028E":76.46},"fy_end_month":12,"eps_basis":"FY2025A為歐元年度稀釋每股盈餘（yfinance年度財報）；FY2026E–FY2028E為美元共識（Koyfin 2026-10-08，ADR一股對一股普通股）。幣別不同，三年年複合會被匯率扭曲，判斷以FY2026E→FY2028E兩年年化33.4%為準。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ASML_20261017/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"獨占設備商，盈利隨晶圓廠資本支出循環，但EUV獨家與服務收入提供底部"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久至2028：第三季新聞稿稱2027與2028規劃供給無法完全滿足客戶需求，客戶以預付款下單、非流動負債季增約€5bn；2029以後僅有客戶意向，尚未接單。","bargaining":{"up":"Zeiss為光學唯一供應商（20-F FY2020版揭露，現況未更新）；管理層稱Zeiss不是2028擴產瓶頸，但擴產需部分補貼供應鏈。","down":"前兩大客戶FY2021合計占66.3%，最大客戶37.0%；台積電公開嫌High-NA太貴並抵制漲價，但關鍵機台漲價已在第三季談成。","geo":"中國約占2026營收20%（2025年33%）；韓國2026第一季占系統銷售45%；出貨受荷蘭與美國出口許可約束。"},"profit_pool_dir":"價值鏈利潤主要在晶片設計（輝達營益率65%）與代工（台積電56%），ASML為35%；本次漲價管理層稱為生態系價值重新分配，利潤池向微影小幅移動。","tam_table":[{"item":"全球WFE 2026（SEMI年中預測）","value":"US$143.9B"},{"item":"WFE 2027成長（SEMI）","value":"+21.8%"},{"item":"WFE 2028（SEMI）","value":"約US$200B，+14.1%"},{"item":"全球設備銷售2028（SEMI）","value":"US$229.5B"},{"item":"ASML光刻市占","value":"約90%，EUV唯一供應商（2026-01投資摘要）"},{"item":"OI池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"EUV唯一供應商＋製程認證轉換成本＋安裝基礎升級與服務隨裝機數累積","execution":9,"pricing":9,"grade":"A","trend":"↑","trend_evidence":"第三季法說：關鍵機台漲價談判完成（史上首次），2027起反映、2028全面；三星2028、台積電2030宣布High-NA量產；英特爾High-NA曝光逾100萬片晶圓；DRAM出現新EUV客戶。反向：台積電抵制High-NA價格。","peer_na_reason":"事實表同業表只有毛利率、營益率、FCF利潤率與研發密度，沒有ROIC；以營益率作利差代理，同業中僅ONTO屬設備業。","threats":[{"level":"🟡","text":"中國DUV新進者：報導稱今年出貨5台DUV、2027暫定20台，機台未經驗證，距EUV多年；即使中國取得20台浸潤式機，估計影響2027營收約2.4%。","p":"10%","evidence_refs":["competitive_share_entrants#1","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"自由電子雷射EUV光源路線（Terafab、xLight）：尚未量產、無設備訂單，ASML與xLight合作技術展示，較像供應鏈元件而非整機替代。","p":"5%","evidence_refs":["competitive_share_entrants#2","customer_second_source#1"]},{"level":"🟡","text":"Nikon與美亞晶片廠洽談採購（未證實），屬DUV層級點對點競爭。","p":"15%","evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"客戶議價反撲：台積電嫌High-NA太貴、延到2030才量產，限制下一代機台的定價空間。","p":"40%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"架構替代：客戶轉向較不依賴微影的新架構或X光微影（Substrate），目前只有宣稱、無量產證據。","p":"5%","evidence_refs":["substitute_technology#0","substitute_technology#3"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推論：客戶預付款讓營運資金為負；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是晶片廠；客戶自身的產品已用長約鎖到至少2028，擴產是需要而非想要，延後買機台等於讓出AI產能。代理讀數：非流動負債（預付款）第三季季增約€5bn。"},{"item":"決策層級","level":"🟢","text":"替代性在製程節點層級衡量：先進邏輯與DRAM的關鍵層只有ASML EUV可用，換供應商要重新認證整條製程；台積電寧可延後High-NA也沒有改用他牌。"},{"item":"價值鏈分配","level":"🟡","text":"營益率35%低於台積電56%與輝達65%；首次漲價成功顯示分配向微影移動，但漲價有一部分要拿去補貼供應鏈擴產，台積電抵制High-NA價格。"},{"item":"社會容忍度","level":"🟡","text":"不依賴監管授權，但出口受荷蘭與美國管制：中國占比由2025年33%降到2026年約20%，MATCH Act擬把禁令擴及DUV與維修；管理層表態不會每年漲價，刻意不把價格推到經濟上限。"}],"roiic":"無法計算：投入資本事實表未涵蓋。2022→2025年營業利益約€6.5bn增至約€11.3bn，同期FCF多數年度高於淨利，增量成長幾乎不耗用股東資本。","reinvest_rate":"近零或為負：2025年FCF €11.0bn高於淨利€9.6bn，2024年FCF/淨利1.20；擴產資金主要來自客戶預付款（第三季FCF €11.4bn）。","endo_ceiling":null,"formula_note":"增量報酬×再投資率在預付款模式下失真：再投資率近零會算出接近零的上限，但實際成長由客戶預付款支應的產能擴充推動（2026年EUV出貨+50%、2027產能+30%）；改以產能年增約30%作為量的上限參考，價與毛利擴張另計。"},"combined":9.0,"score":9.0,"spread_table":[{"metric":"毛利率","ASML":52.73,"2330.TW":64.23,"NVDA":74.67,"AVGO":68.77,"ONTO":50.36,"unit":"%"},{"metric":"營業利益率","ASML":35.42,"2330.TW":56.1,"NVDA":65.21,"AVGO":48.52,"ONTO":13.81,"unit":"%"},{"metric":"FCF 利潤率","ASML":24.27,"2330.TW":25.33,"NVDA":41.92,"AVGO":44.22,"ONTO":22.54,"unit":"%"},{"metric":"研發密度","ASML":13.68,"2330.TW":6.07,"NVDA":7.79,"AVGO":13.28,"ONTO":12.73,"unit":"%"}],"competitors":[{"name":"2330.TW","gm":64.23,"om":56.1,"fcf_margin":25.33,"rd_intensity":6.07,"strategy_note":"最大客戶而非對手；營益率56%高於ASML，High-NA延到2030量產，是ASML漲價最大的議價阻力。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"NVDA","gm":74.67,"om":65.21,"fcf_margin":41.92,"rd_intensity":7.79,"strategy_note":"AI需求源頭，營益率65%顯示利潤池在晶片設計端；ASML漲價等於向這個利潤池分一小塊。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"strategy_note":"客製AI晶片受益者，與ASML不同層級，只作為AI需求強度的側面對照。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"ONTO","gm":50.36,"om":13.81,"fcf_margin":22.54,"rd_intensity":12.73,"strategy_note":"同屬半導體設備，營益率13.8%遠低於ASML的35.4%，反映獨占地位帶來的利差。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（產能+30%）為主、價（2027起漲價，2028全面）次之、升級服務與回購為輔","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"公式（增量報酬×再投資率）在客戶預付款撐資金時失真；以產能年增約30%為量的上限參考，漲價與毛利擴張另計。共識盈餘兩年年化約33%，超出部分可歸因於漲價與毛利擴張。","segments":[{"item":"EUV系統 2026成長","value":">45%"},{"item":"非EUV系統 2026成長","value":"約20%"},{"item":"安裝基礎管理 2026成長","value":"約50%；第三季€3.29bn，第四季指引約€3.7bn"},{"item":"邏輯系統 2026","value":"約+10%（先進邏輯>25%）"},{"item":"記憶體系統 2026","value":"約+75%，主要為DRAM"},{"item":"第三季系統銷售組合","value":"邏輯54%／記憶體46%"}],"decay_signals":[{"signal":"每股盈餘成長顯著高於營收成長（差>5個百分點）","lit":true,"evidence":"FY2026E→FY2027E每股盈餘+35.4%、營收+28.7%，差6.7個百分點；來自漲價與毛利擴張。營收為歐元、盈餘為美元，匯率假設不同時差距會偏移。"},{"signal":"毛利率連2季年減","lit":false,"evidence":"第二季54%、第三季57.5%，皆高於前一年度約51–53%。"},{"signal":"FCF/淨利<0.75連2年","lit":false,"evidence":"2023年0.41、2024年1.20、2025年1.15，未連續。"},{"signal":"核心市占近12個月縮減","lit":false,"evidence":"搜尋未顯示光刻市占變動。"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"漲價2027才反映，尚無量的資料。"},{"signal":"SBC/營收>5%且上升","lit":null,"evidence":"事實表未涵蓋。"},{"signal":"維持性資本支出占FCF>60%","lit":null,"evidence":"事實表未涵蓋。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；配發只有回購（第三季約€4.1bn）與每季股息€1.88兩項，已寫在本題理由，無需展開表格。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無重大併購；Mistral AI為少數股權投資，第三季認列評價增益約€0.5bn，不屬營運併購。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購時點本益比約35–41倍，盈餘殖利率約2.4–2.9%；十年期殖利率事實表未涵蓋，但門檻需高於殖利率加2%，判定未過。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC與歷史股數事實表未涵蓋；反推股數口徑矛盾，無法判定。","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY2027E共識）＋PEG；自身歷史年度端點對照","tier":"獨占半導體設備","peers":{"expanded":false,"reason":"事實表同業表沒有本益比；台積電、輝達、博通是客戶或AI晶片，與微影設備屬不同層級，不能當估值錨；ONTO無倍數資料。"},"peg":1.14,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2027E前瞻本益比28.2倍、當年度38.2倍；PEG約1.14（38.2倍÷兩年盈餘年化33.4%）；本益比年度端點分位51.9，市銷率與EV/S在四點最高（利潤率上升所致）；基準情境五年年化約9%（股價至約2,444美元）。倍數不貴，但分母是週期高點盈利，2029年後沒有證據，因此判中性而非便宜。","upside_short_pct":13,"upside_mid_pct":30},"trap_analysis":{"verdict":"🟡","label":"週期高點盈利與升級業務的可持續性"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"客戶希望提前下2029–30訂單，有分析提醒部分可能是保留產能；Mizuho以客戶集中台積電、三星與英特爾上行有限降評；2026年4月時全年指引還只有€36–40bn，半年內大幅變動，顯示能見度波動大。","assumption":"2027–28需求已由晶圓廠建設計畫與「痛的」預付款驗證，不是重複下單。","consequence":"若AI資本支出在2028見頂，2029–30營收回落，盈利回到悲觀路徑46–55美元，股價跌到約1,100美元以下，五年虧損三成以上。","ruling":"部分採納：悲觀機率給30%。2027–28採信（非流動負債第三季季增約€5bn、管理層尚未接受2029–30訂單以免超賣）；2029–30意向不計入基準。與唯一致命點部分重疊（同為量能落空），本條補上2029年後回落的路徑。","watch":"每季非流動負債（預付款）變動、2027年1月年度展望、主要客戶資本支出公告","evidence_refs":["customer_concentration_credit#2","supply_demand_durability#2"],"fact_refs":["f_consensus_rev_fy1_pct","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"MATCH Act擬把禁令由EUV擴及DUV浸潤式與既有設備維修；美國商務部長據報質疑EUV機台流入中國，ASML否認；中國占比已由2025年33%降至2026年第一季19%。","assumption":"中國占比穩在約20%，管制不再擴大到DUV與服務。","consequence":"若立法且荷蘭執行，分析師估營收影響個位數百分比、每股盈餘最多降10%；若調查成立另有罰款與許可風險。","ruling":"採納為風險但不是主因：衝擊上限約一成盈利，小於需求循環；放進悲觀情境並設減碼觸發。","watch":"MATCH Act院會進度、荷蘭政府執行表態、BIS立案與否、每季中國營收占比","evidence_refs":["geo_supply_chain#2","substitute_technology#4","geo_supply_chain#1","regulatory_antitrust#0","reg_tariff_export#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"CFO稱部分漲價要用來補貼供應鏈擴產；第四季毛利率指引約57%，營收大增仍低於第三季57.5%，原因是擴產成本；升級業務是毛利擺動因素；前兩大客戶集中、台積電抵制漲價；光學只有Zeiss一家。","assumption":"量增帶來固定成本攤提，漲價大部分直接進毛利率。","consequence":"營收照共識成長，但毛利率停在約56%，盈利低於基準路徑，報酬落在基準與悲觀之間。","ruling":"部分採納：以FY2028毛利率≥57%為檢驗門檻；未達則停止加碼。","watch":"每季毛利率、第四季財報對2027毛利率的首次指引","evidence_refs":["geo_supply_chain#0","customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0"],"fact_refs":["f_kpi1_gross_margin","f_kpi4_guidance_q4_2026"]},{"view":"價格已反映太多","evidence":"市銷率16倍、EV/S約15.8倍，都是四個年度端點中最高；本益比約40倍；最新兩份共識快照三個財年皆小幅下修1.3–1.7%。","assumption":"市場用FY2027前瞻倍數約28倍定價，而非用2029谷底盈利。","consequence":"若市場改用谷底盈利定價，倍數壓到20倍，現價下檔約三成。","ruling":"反駁：股價已較前份低約10%，FY2027倍數28倍低於前份認定的30–35倍成熟區；基準情境年化約9%完全來自盈餘成長，不依賴倍數擴張。市銷率高位反映利潤率走高，列入觀察。","watch":"FY2028E前瞻本益比回到35倍以上（約2,676美元）且盈利未上修","evidence_refs":[],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_pe_current","f_consensus_rev_fy2_pct","f_fwd_pe_latest"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1815.27 → 本次 1641.52（-9.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1815.27","side_b":"本次 price_at_dd=1641.52","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,815.27 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,815.27 美元：Bull 價 3,449、Bear 價 1,271，五年期望值 +37.0%，基準年化 7.0%，不對稱比 3.6","side_b":"本次情境、股價仍用 1,815.27 美元：Bull 價 4,000、Bear 價 1,100，五年期望值 +33.9%，基準年化 6.1%，不對稱比 2.55","ruling":"先換情境、股價不動：五年期望值少 3.1 個百分點，基準年化少 0.9 個百分點。不對稱比由 3.6 變為 2.55。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,815.27 美元：五年期望值 +33.9%，基準年化 6.1%，不對稱比 2.55","side_b":"本次情境、股價 1,641.52 美元：五年期望值 +48.0%，基準年化 8.3%，不對稱比 3.63","ruling":"再換股價、情境不動：起點價下跌 9.6%，五年期望值多 14.2 個百分點，基準年化多 2.2 個百分點，不對稱比由 2.55 升到 3.63。合計五年期望值比前份多 11.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"需求真實性：真實擴產還是囤貨","cause":null,"prior_field":null,"side_a":"管理層（2026-10-14 CEO、CFO）：需求以客戶晶圓廠建設計畫驗證，下單附「痛的」預付款且取消代價高；非流動負債季增約€5bn；尚未接受2029–30訂單以免排擠其他客戶。","side_b":"賣方：部分2029–30意向可能是保留產能；Mizuho降評，理由是客戶集中台積電、三星與英特爾2026上行有限。","ruling":"可調和（程度差異）：2027–28以預付款與產能計畫驗證，採信；2029–30只有意向，不計入基準情境。","evidence_level":"中：預付款為財報數字，2029後只有管理層轉述","settle_metric":"每季非流動負債變動；2027年1月年度展望","if_then":["若2027年1月營收展望≥€57bn且非流動負債續增→加碼至目標權重","若非流動負債連2季下降→停止加碼並減碼三分之一"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"管理層前後說法：2027–28產能","cause":null,"prior_field":null,"side_a":"2026-07-15 CFO：2027年約85台是目前供需平衡點，2028年「研究」再增30%；2027低NA訂單接近全滿。","side_b":"2026-10-14 CFO：2027與2028規劃產出都不足以滿足需求，2028研究超過30%；CEO拒絕給2027–28新數字。","ruling":"方向一致、改口是往上修；但不給數字讓檢驗延到2027年1月展望與2027-06-10資本市場日。","evidence_level":"高：兩次法說原話","settle_metric":"2027年1月年度展望；資本市場日長期模型","if_then":["若1月展望與資本市場日確認2028產能增幅≥30%→維持基準並可加碼","若2028產能目標低於30%→停止加碼並重估悲觀機率"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣方論證：市銷率位於年度端點最高；第三季57.5%毛利率靠高毛利升級業務，CFO自稱擺動因素；第四季毛利率指引反而下滑；最新共識快照小幅下修；股價八個交易日跌約8%，市場可能在定價週期頂部。","side_b":"持有論證：FY2027前瞻28倍不貴；漲價2027起才反映；管理層稱仍有大量機台未升級並將推新升級產品；預付款驗證需求至2028。","ruling":"不採納為賣出理由：倍數與盈利證據支持持有；但把毛利率連2季低於53%與預付款連2季下降設為減碼門檻。","evidence_level":"中","settle_metric":"每季毛利率、非流動負債","if_then":["若毛利率連2季低於53%→減碼三分之一","若股價反彈至2,676美元以上且盈利未上修→減碼四分之一"],"evidence_refs":[]},{"axis":"估值與訊號（價格變動）","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份（2026-07-16，股價1,815.27）：估值中性、訊號B；FY27本益比約35倍（以上修後共識約52美元計）。","side_b":"本次（股價1,641.52）：FY2027E共識升至58.13，前瞻本益比約28倍；估值仍判中性（分母在週期高點），訊號升為A（品質A、估值中性、RSI 37.7未過熱）。","ruling":"股價下跌約10%加上共識上修，倍數下降約七個；估值結論不升為便宜，因2029年後盈利沒有證據。","evidence_level":"高：價格與共識皆為事實表數字","settle_metric":"FY2027E前瞻本益比","if_then":["若FY2027E前瞻本益比降到26倍以下且年度展望達標→加碼一批"],"evidence_refs":[]},{"axis":"護城河、跑道、陷阱、類型、週期位置（新證據）","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap","archetype","cycle_position"],"side_a":"前份：護城河趨勢持平、成長跑道寬、陷阱風險中、品質複利成長、週期位置未設。","side_b":"本次：護城河趨勢改為上升（第三季法說確認關鍵機台漲價談判完成，2027起反映、2028全面；三星2028、台積電2030宣布High-NA量產；DRAM新EUV客戶）；跑道寬、陷阱風險中、品質複利成長、週期位置未設，四項重新檢查後維持。","ruling":"定價權由「有彈性但不給時間表」（2026-07-15 CFO）變成「已談成」（2026-10-14 CFO），屬新證據，趨勢上調；其餘四項證據方向未變。","evidence_level":"高：法說原話","settle_metric":"2027毛利率指引；High-NA年度出貨","if_then":["若2027年毛利率未因漲價上升（低於56%）→護城河趨勢降回持平"],"evidence_refs":["customer_second_source#0"]},{"axis":"情境機率、最大回撤、裁決與角色（方法變動）","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：樂觀30%、悲觀25%、最大回撤−55%單點；裁決進場。","side_b":"本次：樂觀25%、基準45%、悲觀30%；內生成長公式在預付款模式失真，保守視為共識超出上限，悲觀機率下限30%；最大回撤改為−55%至−35%範圍，由悲觀路徑谷底盈利×熄火倍數推出；裁決與角色由程式依本次輸入重算。","ruling":"機率調整來自方法（上限檢核與五年窗涵蓋2029–31），不是基本面轉弱。","evidence_level":"中","settle_metric":"2027年1月展望","if_then":["若2027展望與資本市場日把需求能見度延伸到2029→悲觀機率可降回25%"],"evidence_refs":[]},{"axis":"加碼重啟條件（前份觸發已發火）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼觸發：回檔至$1,650（FY27 ≈32x）分批，或 2027 指引/訂單再上修、Intel 14A 外部客戶落地","side_b":"加碼：回檔至$1,500以下（FY2027E共識約26倍）且2027年1月營收展望≥€52bn；或展望≥€57bn時直接加碼","ruling":"前份加碼觸發已於2026-10-16發火（收盤1,641.52低於1,650），另一分支（2027訂單上修）也在第三季成立；共識上修到58.13後，同一價位對應倍數由32倍降到28倍，新門檻改用26倍並綁定年度展望。英特爾14A外部客戶本包未涵蓋，移除。","evidence_level":"高","settle_metric":"股價與2027年1月展望","if_then":["若回檔至1,500美元以下且展望≥€52bn→加碼一批","若展望<€52bn→不加碼，改走減碼條件"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點設定","cause":"方法變動","prior_field":null,"side_a":"前份未設唯一致命點（null）","side_b":"2027年1月ASML公布的2027年展望低於€52bn，或宣布縮減2027–2028產能擴充","ruling":"本次依規則補設；選數學上敏感度最大的一項：基準路徑FY2027–28盈利成長主要靠出貨量，而不是最戲劇性的出口管制（盈利衝擊上限約一成）。","evidence_level":"中","settle_metric":"2027年1月年度展望","if_then":["若發生→減碼至三分之一並重跑研究"],"evidence_refs":[]},{"axis":"清倉／減碼門檻（新增）","cause":"方法變動","prior_field":null,"side_a":"前份無清倉／減碼量化門檻（null）","side_b":"年度展望<€52bn減碼至三分之一；非流動負債連2季下降減碼三分之一；毛利率連2季<53%減碼三分之一；MATCH Act成法且荷蘭執行減碼一半","ruling":"前份只有警戒閾值沒有動作；本次把四個可每季檢驗的指標綁上具體減碼比例。","evidence_level":"中","settle_metric":"季報","if_then":["任兩項同時觸發→清倉"],"evidence_refs":[]},{"axis":"風險門檻調整（減碼條件）","cause":"新證據","prior_field":null,"side_a":"前份風險一：MATCH Act 院會表決 或 BIS 正式立案；China 營收連 2 季 YoY <−30%。前份風險三：hyperscaler 2027 capex guidance 下修 或 WFE 連 2 季負成長","side_b":"風險一：MATCH Act成法且荷蘭執行，或中國全年營收占比<10%；需求風險：非流動負債連2季下降或2027年1月展望<€52bn","ruling":"中國營收在2026第一季已由36%降到19%，年減幅門檻在既有管制下就會誤觸，改用占比水準；院會表決不等於生效，改為成法且荷蘭執行。雲端業者資本支出不在本包，改用ASML自身的預付款與展望作需求代理。","evidence_level":"中","settle_metric":"MATCH Act進度、季報","if_then":["若觸發→依觸發器減碼"],"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2"]}],"triggers":[{"n":1,"text":"2027年展望不及或產能擴充縮減","type":"Single Thing","maps_to":"Single Thing","metric":"2027年1月公布的2027年營收展望；2027–28產能計畫","threshold":"展望中位數<€52bn，或宣布縮減2027–28產能擴充","action":"減碼至三分之一並重跑研究","source_freq":"ASML第四季財報，年度","date":"2027-01","evidence_refs":[]},{"n":2,"text":"客戶預付款轉弱","type":"假設驗證","maps_to":"H1","metric":"非流動負債（主要為客戶預付款）季變動","threshold":"連2季下降","action":"停止加碼並減碼三分之一","source_freq":"季報資產負債表，每季","date":"每季","evidence_refs":["customer_concentration_credit#2"]},{"n":3,"text":"漲價未進毛利率","type":"假設驗證","maps_to":"H2","metric":"年度毛利率","threshold":"FY2027毛利率<56%或FY2028<57%","action":"停止加碼","source_freq":"季報，每季","date":"2028-01","evidence_refs":["customer_second_source#0"]},{"n":4,"text":"MATCH Act把禁令擴及DUV與維修","type":"風險","maps_to":"R1","metric":"MATCH Act立法與荷蘭執行","threshold":"成法且荷蘭宣布執行","action":"減碼一半","source_freq":"新聞與政府公告，事件","date":null,"evidence_refs":["geo_supply_chain#2","substitute_technology#4","geo_supply_chain#1"]},{"n":5,"text":"EUV流入中國調查升級","type":"風險","maps_to":"R1","metric":"美國商務部對ASML的調查狀態","threshold":"BIS正式立案或開罰","action":"減碼三分之一","source_freq":"新聞與BIS公告，事件","date":null,"evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0"]},{"n":6,"text":"美國證券集體訴訟進展","type":"風險","maps_to":"R2","metric":"紐約南區證券集體訴訟（2024年期間）","threshold":"集體認證通過且不利和解金額>€1bn","action":"減碼至半倉","source_freq":"法院紀錄與公司公告，事件","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":7,"text":"光學供應成為瓶頸","type":"風險","maps_to":"R4","metric":"管理層對Zeiss產能的表述、出貨落後","threshold":"管理層承認光學供應限制出貨，或低NA EUV年出貨低於產能計畫一成","action":"停止加碼","source_freq":"法說，每季","date":"每季","evidence_refs":["geo_supply_chain#0"]},{"n":8,"text":"競爭者拿到量產訂單","type":"風險","maps_to":"R5","metric":"Nikon先進浸潤式量產訂單；中國DUV出貨","threshold":"Nikon確認量產訂單，或中國廠2027年出貨≥20台且通過客戶驗證","action":"停止加碼","source_freq":"新聞與產業報告，事件","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","competitive_share_entrants#2"]},{"n":9,"text":"回檔加碼","type":"估值rearm","maps_to":"H1","metric":"股價與FY2027E前瞻本益比","threshold":"股價≤1,500美元（約26倍）且2027展望≥€52bn","action":"分批加碼一批","source_freq":"每日股價；年度展望","date":null,"evidence_refs":[]},{"n":10,"text":"展望強勁加碼","type":"加碼","maps_to":"H1","metric":"2027年營收展望","threshold":"展望中位數≥€57bn且2028產能增幅≥30%獲確認","action":"加碼至目標權重","source_freq":"第四季財報，年度","date":"2027-01","evidence_refs":[]},{"n":11,"text":"估值過熱減碼","type":"減碼","maps_to":"H2","metric":"FY2028E前瞻本益比","threshold":"股價>2,676美元（35倍）且盈利未上修","action":"減碼四分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":12,"text":"年度展望與資本市場日複審","type":"複審日期","maps_to":"H1","metric":"2027展望；長期營收與毛利率模型","threshold":"—","action":"重跑研究","source_freq":"事件","date":"2027-06-10","evidence_refs":[]}],"kill_metrics":[{"metric":"2027年營收展望（2027年1月公布）","bear_threshold":"中位數<€52bn或宣布縮減產能擴充","window":"2027-01財報","source":"ASML第四季財報新聞稿","last_status":"unknown"},{"metric":"非流動負債（客戶預付款）季變動","bear_threshold":"連續2季下降","window":"每季","source":"ASML季報資產負債表","last_status":"ok"},{"metric":"季度毛利率","bear_threshold":"連續2季低於53%","window":"每季","source":"ASML季報","last_status":"ok"},{"metric":"中國營收占比與MATCH Act","bear_threshold":"全年占比<10%或MATCH Act成法並經荷蘭執行","window":"每季／事件","source":"ASML季報地區別、政府公告","last_status":"warning"}],"evidence_dismissed":[{"ref":"reg_tariff_export#1","reason":"證據是2025年7月的關稅不確定性與財測收窄，已被之後2026年三次上調指引取代；同一條也註明搜尋未找到2026年半導體232關稅實施的報導，時效過期且無現行事件可對應。"}],"decision_out":{"verdict":"進場","role":"核心","row_hit":"10","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把FY2027–28盈利當週期高點而給28倍，但漲價2028才全面反映，客戶已用預付款鎖定2028產能並要求2029–30排程，盈利高原可能比市場假設長。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟢', val='🟡', moat_trend='↑', week26=12.84, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":true,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"10-verdict","condition":"命中 row10 → 進場","hit":true,"basis":"row_hit=10"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"加碼：回檔至$1,500以下（FY2027E共識約26倍）且2027年1月營收展望≥€52bn；或展望≥€57bn時直接加碼","exec_line":"前份加碼價位已觸發；現價分兩批：第一批現在，第二批待2027年1月展望確認≥€52bn或回檔至1,500美元以下。"},"reasoning":{"industry":"最新一季（2026第三季）總營收€11.66bn、毛利率57.5%、淨利€4.96bn；系統銷售約€8.4bn（EUV約€4.1bn含1台High-NA，非EUV約€4.3bn），安裝基礎管理€3.29bn，占總營收約28%，比指引高約€0.4bn，是本季毛利率超標的主因。淨利含Mistral AI投資評價增益約€0.5bn，約占當季淨利一成，屬一次性。近四季營益率35.4%。全年2026指引€44–45bn、毛利率約56%，第四季指引€14.2–15.2bn、毛利率約57%。產業時鐘判在擴張期：客戶需求到2028仍超過供給，2027產能增30%、2028研究再增逾30%，SEMI年中預測WFE 2027年+21.8%、2028年+14.1%；過熱的跡象（漲價、客戶要求提前下2029–30訂單）已出現，但管理層表示以晶圓廠建設計畫驗證需求，尚未接受2029–30訂單。供需持久性：結構性持久至2028，證據只蓋到2028，2029以後不足。單點依賴有兩處：上游光學只有Zeiss一家（20-F揭露，管理層稱不是2028擴產瓶頸）；下游前兩大客戶在FY2021合計占66.3%，近期集中度又往台積電上升。產業態勢三軸：競爭面靜態（中國DUV、Nikon、自由電子雷射光源皆未構成量產威脅），結構面轉好（漲價談成、High-NA進量產排程、DRAM新EUV客戶），其他結構變數中出口管制持續收緊（MATCH Act擬把禁令擴及DUV與維修），整體裁為雙向拉鋸，結構性轉好略占上風。","moat":"機制是EUV唯一供應商、整體光刻市占約90%，客戶製程以ASML機台認證，換供應商等於重新認證整條製程。定價權擴大的證據：第三季CFO稱與客戶的漲價談判已完成，2027起反映在營收與毛利率，2028起全面且持續；CEO說這是過去從未做過的討論，客戶接受生態系價值在移動。執行力擴大：2026年低NA EUV出貨約65台，較2025年44台增近50%，2027產能再增30%。同業對照只有利潤率沒有ROIC：ASML營益率35.4%高於設備同業ONTO的13.8%，差距約22個百分點，且ASML年度營益率由2022年30.7%升至2025年34.6%，利差為正且擴大；但低於客戶台積電56.1%與輝達65.2%，說明價值鏈分配仍偏向下游。反向證據：台積電嫌High-NA太貴，量產延至2030；中國DUV新進者與自由電子雷射光源報導曾讓股價兩日跌約10%，但皆未量產。威脅均為點對點，不扣分。","growth":"成長以量為主（產能2027年+30%、2028年研究逾30%），價次之（關鍵機台漲價2027起反映、2028全面），升級服務與回購為輔。共識每股盈餘FY2026E 42.94→FY2027E 58.13→FY2028E 76.46美元，兩年年化約33.4%；三年口徑因基期FY2025實際為歐元（24.71），與美元共識不同幣別，不硬算。共識營收FY2026E €44.5bn→FY2027E €57.2bn，+28.7%。內生上限公式在預付款模式失真，以產能年增約30%作量的上限；共識盈餘年化33%與此相差約3個百分點，由漲價與毛利擴張補上，可以歸因，不屬依賴重估。滲透率：High-NA量產剛起步（三星2028、台積電2030），12吋光罩聯盟目標2031試產、2033量產，客戶規劃更多層，第二曲線有來源；低NA EUV在DRAM仍有新客戶導入。衰退信號亮一盞（盈餘成長高於營收成長逾5個百分點，來自漲價與毛利擴張）。主要不確定在2029以後：證據只蓋到2028。","governance":"FCF/淨利轉換率2022年1.27、2023年0.41、2024年1.20、2025年1.15（事實表年度財務歷史，yfinance），波動來自客戶預付款進出，第三季單季FCF €11.4bn同樣是預付款推高。淨現金約€10.8bn（現金及短投€12.7bn、總債務€2.0bn）。現金去向：第三季依2026–2028計畫回購約€4.1bn（第二季約€1.1bn），每季中期股息€1.88，殖利率約0.55%。無重大併購，Mistral AI為少數股權投資。回購時點的本益比約35–41倍，盈餘殖利率約2.4–2.9%，難以通過十年期殖利率加2%的門檻（十年期殖利率事實表未涵蓋）。SBC與股數歷史事實表未涵蓋；以淨利÷稀釋每股盈餘反推的股數口徑互相矛盾（2022年約350百萬、2024年約394百萬），不採信。","valuation":"現價1,641.52美元，對FY2027E共識58.13為28.2倍，對FY2026E 42.94為38.2倍；前份時FY27本益比約35倍，股價下跌約10%加上共識上修，倍數降約七個。PEG以當年度38.2倍除兩年盈餘年化33.4%約1.14，落在合理區。歷史位置只有四個年度端點：本益比分位51.9，市銷率與EV/S皆為四點中最高，反映利潤率走高而非盈利倍數昂貴。五年分位事實表未涵蓋（只有四個年度端點），不外推。共識FY1近三個月上修11.3%，但最近兩份快照間三年皆小幅下修1.3–1.7%。賣方目標價分散（約1,970至2,623美元），不作承重。基準情境（2031年每股盈餘94美元×26倍）年化約9%，報酬來自盈餘成長，倍數由38倍降到26倍是拖累，不依賴重估。","premortem":"依據見反證紀錄四條：需求囤貨與2029後回落、出口管制擴及DUV、漲價被擴產成本與客戶議價吃掉、市銷率位於年度端點高位。衰退信號只亮一盞（盈餘成長快於營收，來自漲價），陷阱風險判中。動能面不過熱：26週報酬12.8%、RSI 37.7，股價自10月8日快照價約1,780美元回落。"},"plain":{"six":{"how_it_makes_money":"賺晶片廠擴產的錢：機台（EUV／DUV）一次性收款，加上安裝基礎升級與服務的經常性收入；錢卡在先進製程曝光這一節點，EUV只有ASML能供貨。","moat":"護城河趨勢上升：EUV獨家供應下首次談成漲價，High-NA進入客戶量產排程，DRAM端出現新的EUV客戶。","growth":"成長跑道寬：2027–28量價齊揚，High-NA是有客戶量產時程背書的第二條曲線。","capital":"資本配置中等偏弱：現金充裕、配發積極，但回購在高倍數時執行，股權稀釋資料不足。","valuation":"現價要求FY2027–28共識兌現、且2029後盈利不大幅回落；前者有預付款與產能證據，我信；後者沒有證據，所以只給中性。","how_wrong":"最可能看錯在把2027–28週期高點盈利當成高原：若AI資本支出在2028見頂，盈利與倍數會一起下修。"}},"decision_inputs":{"signal":"A","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把FY2027–28盈利當週期高點而給28倍，但漲價2028才全面反映，客戶已用預付款鎖定2028產能並要求2029–30排程，盈利高原可能比市場假設長。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"A","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":1641.52,"week26_return_pct":12.84,"consensus_rev_3m_pct":11.33,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"第三季淨利含Mistral AI評價增益約€0.5bn（約當季淨利一成），屬一次性但不改結論；真正的分歧在2028年後盈利能否維持，不在分母的一次性項目。短期上檔＝FY2027E 58.13×32倍≈1,860美元（+13%）；中期＝三年後FY2029E基準82×26倍≈2,132美元（+30%）。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與2027年展望、2027毛利率首次指引","impact":"高","watch":"營收展望是否≥€52bn；2028產能增幅"},{"date":"2027-01","date_precision":"quarter","type":"product","event":"NXE:3800F小量出貨、浸潤式每小時330片新機導入","impact":"中","watch":"新機售價與毛利貢獻"},{"date":"2027-06","date_precision":"month","type":"guidance","event":"資本市場日（2027-06-10）更新長期展望","impact":"高","watch":"2030年營收與毛利率模型、2029–30接單政策"},{"date":null,"date_precision":null,"type":"regulatory","event":"MATCH Act立法與荷蘭執行","impact":"中","watch":"院會表決、荷蘭政府表態"},{"date":"2028","date_precision":null,"type":"product","event":"三星High-NA進入量產","impact":"中","watch":"High-NA年度出貨與層數"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s4`：現在 1,465B，下限 1,500B，**目標 ≥ 1,800B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ASML_20261017/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s4 -->
<section id="s4"><h2>4　品質門檻與資本配置</h2>
<p class="lead">企業品質過關，資本配置只有中下。</p>
<ul class="pts">
<li>品質評分 9，成長持久度 8。壓力測試五項過了 4 項。AI 取代風險判為低。這幾項合起來，使 ASML 通過「看得懂、有護城河、能長期複利」的基本門檻，這也是裁決能到進場的前提。</li>
<li>現金轉換品質整體良好但波動大。FCF 對淨利的比率 2022 年 1.27，2023 年 0.41，2024 年 1.20，2025 年 1.15。波動來自客戶預付款的進出。第三季單季 FCF €11.4bn，同樣被預付款推高，不能當成常態。</li>
<li>財務體質穩。淨現金約 €10.8bn，現金及短投 €12.7bn，總債務 €2.0bn。第三季淨利含 Mistral AI 投資的評價增益約 €0.5bn，約占當季淨利一成，屬一次性。</li>
<li>資本配置評為 C。成長不靠併購，現金只去兩處：第三季回購約 €4.1bn，加上每季股息 €1.88，殖利率約 0.55%。回購時點本益比約 35 至 41 倍，盈餘殖利率只有 2.4% 至 2.9%，難以通過高於十年期殖利率加 2% 的門檻。</li>
<li>股權稀釋無法判定。SBC 與歷史股數事實表未涵蓋，以淨利除以稀釋每股盈餘反推的股數，2022 年約 350 百萬、2024 年約 394 百萬，口徑互相矛盾，不採信。這項評為 C，使持有年限上限落在中期 2 至 5 年，但不降低裁決。</li>
</ul></section>

```