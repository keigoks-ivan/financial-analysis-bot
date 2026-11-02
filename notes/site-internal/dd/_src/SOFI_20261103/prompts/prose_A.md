你是 stock-analyst v20 的**散文層（prose）agent**，標的 SOFI（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：SOFI　日期：2026-11-03　archetype：None　前份裁決：2026-07-30　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1936B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（751B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1111B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1565B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1043B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（808B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1102B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2318B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（5182B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3114B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1936           3545-5064      5 條（2–6 內）  
s3                  8000         751           5074-7249      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3719          7897-11281      5 條（2–6 內）  
s6                 11000         808          7134-10192      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1102           1679-2398      3 條（2–6 內）  
s10                 5000        2318           1877-2682      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3114           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5539B；至少需散文≈39.46KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65%
−65
−55%
−54%
−46%
−45
−45%
−39.9
0
0.05
0.09
0.35
0.39
0.5
0.50
0.503
0.55
0.57
0.6
0.60
0.61
0.62
0.65
0.66
0.7
0.75
0.80
0.8
0.89
0.90
0.93
1.0
01
1
1.03
1.12
1.14
1.22
1.3
1.3%
1.36
1.4%
1.43
1.47
1.5
1.53
1.55
1.56
1.6
1.7%
1.75
1.9
1.92
2%
2.0
02
2
2.25
2.26%
2.30
2.3
2.32
2.41
2.43
2.5
2.54
2.6
2.71
2.84
2.9
03
3
3%
3.1%
3.3
3.37%
3.4%
3.5%
3.53
3.6
3.7%
3.8
3.81%
3.85
3.9
4%
4
4.0%
04
4.1
4.2%
4.4
4.4%
4.5%
4.6
4.70
4.8
05
5%
5.0%
5
5.2%
5.25
5.71
5.97
6%
6.0%
06
6
6.1%
6.14%
6.8%
7.0%
7%
7
07
7.16
7.34
7.48
7.6%
8
08
8.07
9
09
9.27
9.7
10%
10
10.3
10.4%
11
11%
11.3%
11.4
12%
12
12.5%
12.8%
12.8
12.97
13%
13.5%
13.71
13.8
13.85
14
14.0%
14%
14.2
14.3%
14.88
15
15%
15.1%
15.2
15.25
15.9
16
16.5
16.5%
16.6
16.9%
17
17%
17.38
17.70
$17.70
18%
18
18.7%
18.81
19
19.5
19.53
20%
20
20.5
20.6
21%
21.4
21.9
22.8%
23
23.5%
24%
24
24.5
25%
25
26
27
27%
27.5
27.50
28%
28.48
28.49
28.5
29
30%
30
31
31%
31.4
33%
34%
35%
36
36.1
37%
38%
38
39%
40%
40
41
41%
42
42%
43%
44
44%
45
46%
46
49
50%
50.4
51%
52%
52
57.0%
58
58.3%
59%
60
60%
62%
63.9
64
65.6
68%
70
74%
78.9%
80
88
90
90%
97.05
100
100%
101%
103.3%
104
108
120
126
140
150%
150
169
180
200
513
560
710
782
942
2019
2023
2025
2026
2027
2028
2030
2031
2035
20261103
1,200
1,630
1,710
2,670
28,900
3,300
4,800
5,000
5,775
57,754,660
7,090
8,740
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
{"meta":{"ticker":"SOFI","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"SoFi Technologies, Inc."},"oneliner":"升息環境下營收仍年增 44%，2027 財測明言不增資。ROTCE 能否由 10% 爬到 15%，決定了估值；現價已先付了這段爬坡的錢。唯一致命數字是個貸全口徑淨壞帳率能否守在 5% 以下。","thesis":{"H":[{"id":"H1","text":"報酬率爬坡：淨利率與營收／權益比同時上升，ROTCE 由 2026Q3 的約 10% 升到 FY2028 的 15% 以上；管理層長期目標是 20–30%。","2y":null,"5y":"FY2028 ROTCE ≥15%，FY2030 ≥18%","10y":null,"threshold":"FY2027 全年 ROTCE ≥12%（財測淨利 12.8 億 ÷ 推算的平均有形權益約 108 億）；FY2028 ≥15%","source":"公司季度新聞稿的 ROTCE；CFO 在法說揭露的營收／權益比（Q3 為 0.57）","drift_rule":"TTM ROTCE 低於路徑 5% 以上（相對值）連續 4 季，論點削弱；低於 10% 以上連續 6 季，論點反轉"},{"id":"H2","text":"2027 成長完全靠內部資本：不增發普通股；總資本比由 17% 往中低十幾%回落，但不破 12.5%；個貸全口徑年化淨壞帳率守在 4.5% 以下。","2y":"2027 年底前零增資、總資本比 ≥12.5%、個貸淨壞帳率 ≤4.5%","5y":null,"10y":null,"threshold":"任何普通股增發即失效；總資本比 <12.5%；個貸淨壞帳率連兩季 >4.5%","source":"8-K 與 10-Q 的監理資本比；季度法說的信用數據","drift_rule":"總資本比單季降幅連 2 季超過 200bp（比 Q3 的 180bp 快 10% 以上），論點削弱；連 3 季、或跌破 12.5%，論點反轉；任何普通股增發直接反轉"},{"id":"H3","text":"交叉購買飛輪：每會員產品數由 1.56 升到 2.0，費收型營收占比由 42% 升到 50% 以上，讓報酬率不再綁在個貸資產負債表上。","2y":null,"5y":null,"10y":"2030 年產品 1 億（現 2,670 萬）、費收占比 ≥50%；2035 年每會員產品數 ≥2.0","threshold":"每會員產品數每年增加 ≥0.05（Q3 年增 0.09）；FY2028 費收占比 ≥46%","source":"季度法說的會員、產品與費收型營收","drift_rule":"連續 2 個年度低於門檻，論點削弱；連續 3 個年度，論點反轉"}],"R":[{"id":"R1","text":"費收引擎卡住：大客戶流失的基期效應在 2027Q1 消失後，平台段仍回不到 2027 財測的 25% 成長；放款段占比繼續上升，費收占比停在 40% 上下。","h_ref":"H3","clock":"🔥","threshold":"平台段 2027Q1 到 Q2 年增 <10%，或放款段占調整後淨營收連兩季 ≥62%（Q3 為 59%）","evidence_refs":["end_markets#2","channel_business_model_shift#2","end_markets#5","substitute_technology#1"]},{"id":"R2","text":"會計與法律風險：放空報告質疑的公允價值計量，在 FY2026 年度查核中落地為重述、重大內控缺失或監理要求下修；或律所調查升級為已立案的證券集體訴訟。","h_ref":"H1","clock":"⚡","threshold":"10-K 出現重述或重大內控缺失，或公允價值查核事項附帶調整；集體訴訟立案","evidence_refs":["major_events#1","major_events#2","lawsuit_class_action#0"]},{"id":"R3","text":"升息下的消費信用轉弱：聯準會由降息轉為升息（今年已一次，年內預期再兩次，2027 再兩次），產業無擔保個貸逾期率走高，而個貸是放款段的主體。","h_ref":"H2","clock":"🔥","threshold":"個貸全口徑年化淨壞帳率連兩季 >4.5%；表內 90 天逾期率 >60bp（Q3 為 42bp）","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","end_markets#5"]},{"id":"R4","text":"資本消耗比管理層說的快：CET1 由 2025 年底 22.8%、2026-06 的 18.7%，降到 2026-09 的 16.9%，總資本比單季降 180bp。若 2027 年中已貼近 13%，不增資的承諾就會被考驗。","h_ref":"H2","clock":"🔥","threshold":"總資本比 <12.5%，或宣布增發普通股","evidence_refs":["financial_regulatory_capital_rules#0"]},{"id":"R5","text":"放款定價被侵蝕：新進者與既有業者壓價搶份額（Upstart 放款年增 50%），個貸票息連幾季下滑，靠手續費補；存款端仍以高利率當獲客工具。","h_ref":"H1","clock":"🐢","threshold":"核心個貸風險調整後利差連兩季 <6.0%（以 Q3 口徑，Q3 約 7.6%）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]}],"single_thing":{"description":"個人貸款全口徑年化淨壞帳率（排除逾期貸款出售）任一季升破 5.0%；2026Q3 為 3.4%，去年同期約 4.2%。","why_fatal":"個貸是放款段的主體，放款段占調整後淨營收 59%。核心個貸風險調整後利差 7.6%＝票息 12.8%＋手續費 1.4%－資金成本 3.1%－損失 3.4%，損失每多 1.6 個百分點，利差就少兩成。更大的衝擊在公允價值：個貸帳面按 103.3% 標記，一旦上調損失假設，整本貸款會一次減值，直接打進當季損益與有形淨值。同時 LPB 資金方會縮手，資本比也會加速下滑。這四條傳導會同時發生，所以它是估值上最大的單一敏感項。","if_happens":"FY2027 EPS 往 0.6 以下修正，走空頭情境路徑，清倉。重新進場的條件改為壞帳連兩季回落到 4.0% 以下，並重跑完整研究。","how_monitor":"每季財報新聞稿與法說：個貸全口徑淨壞帳率、表內 90 天逾期率（Q3 為 42bp）、個貸公允價值標記。季與季之間看 TransUnion 無擔保個貸 60 天以上逾期率。","probability":"未來 12 到 24 個月約 15%。不利的一面：聯準會今年已升息一次、預期再升兩次，產業逾期率年增 44bp。有利的一面：SoFi 客群偏高收入，Q3 壞帳年降 80bp。"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":19.53,"peg_fy2":0.7,"stress":{"pass":4,"total":8}},"eps_meta":{"base_eps_path":{"FY2025A":0.39,"FY2026E":0.61,"FY2027E":0.89,"FY2028E":1.14},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS（年度財報）；FY2026E 起為 Koyfin 共識，與公司調整後 EPS 財測口徑一致（2026 為 0.61，2027 為 0.90），兩者口徑不完全相同"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SOFI_20261103/scenario.json","archetype":{"primary":"金融","secondary":null,"confidence":"高","fingerprint":"全國性特許銀行的控股公司：淨利息收入是最大收入來源，放款段占營收 59%，成長受監理資本比約束。估值主錨用 P/TBV 對照 ROTCE。"},"industry":{"clock_phase":"III","sd_verdict_source":"供需耐久性分兩段看。會員與存款需求屬結構性持久，數位銀行滲透持續，會員年增 35%。個貸需求屬週期性、可能反轉：產業逾期率上升，聯準會轉為升息。週期判在過熱段，因為放款量創高的同時信用指標開始轉弱。來源：SoFi 2026Q3 新聞稿、TransUnion 2026Q2。","bargaining":{"up":"資金端有兩類。存款人議價力強，要給高利率才留得住（App 廣告 4.4% 年利率）。LPB 外部資金方議價力弱，Q2 法說稱其需求大於 SoFi 願意供給的量。","down":"借款人以優質客群為主，定價靠票息加手續費；手續費已覆蓋逾半數新個貸，但票息連幾季下滑。","geo":"營收全在美國本土，無海外集中。"},"profit_pool_dir":"事實表未涵蓋產業利潤池分布。可觀察到的是，個貸利潤正以兩種方式並行分配：留在 SoFi 資產負債表，或經 LPB 轉給外部資金方、SoFi 收手續費。","tam_table":[{"item":"SoFi 個貸市占（Dolphin Research 估計）","value":"2023 年約 6.8%，2025 年底約 12%；Truist 另有 >25% 的估計，口徑不同、日期不明"},{"item":"會員數","value":"1,710 萬，年增 35%；管理層規劃 2030 年約 5,000 萬會員支撐 1 億產品"},{"item":"產品數","value":"2,670 萬；管理層 2030 年目標 1 億（4 倍）"},{"item":"每會員產品數","value":"1.47（2025Q3）→ 1.56（2026Q3），管理層目標至少 2.0"},{"item":"費收型營收占比","value":"39%（2026Q2）→ 42%（2026Q3），目標 50% 以上"},{"item":"產業營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"全產品線集中在單一 App，交叉購買推高每會員終身價值，再以較好的存放款利率讓利獲客；全國性銀行執照提供存款資金。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大、定價面穩定，合判持平。正面證據：每會員產品數 1.47→1.56，交叉購買占新產品 51%，個貸份額估計 6.8%→12%。負面證據：平台段重要客戶轉投對手，營收年減 24%；放款端競爭加劇。有已證實的最大客戶流失，不得判為擴大。","peer_na_reason":"事實表沒有同業 ROIC 或 ROTCE。同業對照只有 FCF 利潤率，而銀行把放款計入營運現金流，FCF 不能拿來比較報酬率；改用份額、每會員產品數與交叉購買率判斷方向。","threats":[{"level":"🟡","text":"放款端點對點競爭：10-K 稱銀行、信用合作社與科技型放款人會壓價搶份額，Upstart 放款年增 50%。SoFi 以手續費替代票息來維持利差，屬點對點攻擊，不扣分。","p":30,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"平台段客戶集中：Galileo 重要客戶轉投對手，平台段營收年減 24%；排除該客戶則年增 18%。平台段占營收約 6%，不動搖主體護城河。","p":"已發生","evidence_refs":["substitute_technology#1","end_markets#2"]},{"level":"🟡","text":"AI 代理比價：代理工具若讓存放款利率與隱藏費用完全透明，單一產品的轉換摩擦會再降，存款可能變成追最高利率的熱錢。執行長認為終身價值最高者每次都贏，但這只是主張，還沒有證據。","p":20,"evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"低周轉、利益率爬升中：淨利率約 18% × 營收／權益約 0.57 ≈ ROTCE 10%，與股權成本相當","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者是同一位會員，三個角色不脫節。存款與支付屬於需要，不是想要；個貸多用來以 12% 利率替換 25% 的卡債，延後的代價是繼續付高息。讀數：會員年增 35% 至 1,710 萬，單季新增 120 萬創高；管理層稱未見借貸、消費、儲蓄、投資放緩。要注意的是，持久的是低成本數位銀行這個需求，不是個貸量，個貸會隨信用週期起伏。"},{"item":"決策層級","level":"🟡","text":"替代發生在單一產品層。存款跟著利率走，公司自承以高利率代替分行獲客；個貸由比價平台逐筆比較，轉換成本低。能拉高轉換成本的是多產品綁定：37% 會員使用兩項以上產品（去年 33%），新產品 51% 來自既有會員，Q2 稱獲客成本持平。AI 代理比價若普及，單一產品的轉換摩擦還會再降。"},{"item":"價值鏈分配","level":"🟡","text":"SoFi 自己掌握獲客、放款、服務與核心系統，信用風險可以留在表內，也可經 LPB 轉給外部資金方賺手續費。Q2 稱 LPB 需求大於願意供給的量，對資金方有議價力。但存款端要付高利率，個貸票息連幾季下滑、改靠手續費補，對借款人的定價空間有限；管理層也說 LPB 變現率只會在區間內波動。"},{"item":"社會容忍度","level":"🟡","text":"定價上限同時受監理與社會約束。全國性銀行執照本身就是監理授權，資本比受監理約束；2019 年 FTC 同意令限制行銷時誤述節省金額。手續費已覆蓋逾半數新個貸，若消費金融監理轉嚴，手續費是最容易被盯上的項目。Basel III 最終版已重新提出較輕的版本，2026-06 意見期截止、尚未定案，方向中性。"}],"roiic":16.5,"reinvest_rate":100,"endo_ceiling":16.5,"formula_note":"單位為 %。增量 ROTCE：Q3 調整後淨利 2.43 億、年增 74%，年增量約 1.03 億，年化約 4.1 億；同期有形權益增加 25 億（其中約 15.9 億來自增發），4.1÷25≈16.5%。再投資率：不配息、不回購，盈餘 100% 留存放款；外部增資不算內生。內生上限＝16.5%×100%＝16.5%。增發的資本還沒用完（總資本比 17%，規劃水位 13.5%），完全投入後增量報酬可能更高，所以這個數字偏保守。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","SOFI":null,"COF":null,"ALLY":null,"LC":null,"HOOD":81.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","SOFI":null,"COF":null,"ALLY":null,"LC":null,"HOOD":45.65,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","SOFI":-222.21,"COF":45.04,"ALLY":14.38,"LC":null,"HOOD":58.44,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","SOFI":null,"COF":null,"ALLY":null,"LC":null,"HOOD":19.34,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"COF","gm":null,"om":null,"fcf_margin":45.04,"rd_intensity":null,"strategy_note":"信用卡與全國性存款的規模龍頭，資金成本與信用卡承保經驗都領先。SoFi 信用卡約 65.6 萬張，仍在虧損換規模，這條戰線 SoFi 是挑戰者。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ALLY","gm":null,"om":null,"fcf_margin":14.38,"rd_intensity":null,"strategy_note":"純數位存款加汽車放款，是存款端的直接競品。SoFi 宣稱靠產品廣度而非利率勝出，需要交叉購買率持續上升來證明。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"LC","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"同樣持有銀行執照的個貸業者，是個貸定價戰的直接對手；事實表沒有其財務數據，無法比較利潤率。"},{"name":"HOOD","gm":81.44,"om":45.65,"fcf_margin":58.44,"rd_intensity":19.34,"strategy_note":"投資與加密業務的主要對手，資本輕、利潤率遠高於 SoFi。管理層自承 SoFi Invest 的資產收入率低於基準，這一塊 SoFi 是追趕者。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"以量為主（會員 +35%、產品 +44%），價為輔（放款段每產品收入 +20%）；無回購，併購小，2026 年有約 15.9 億外部增資","runway_years":"約 7 年：個貸份額 12%，以每年約 2.6 個百分點推進到 30%；金融服務段另有第二曲線","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段的推算：增量 ROTCE 約 16.5% × 盈餘全數留存 100% ＝ 16.5%","segments":[{"item":"放款段","value":"Q3 調整後淨營收約 8.07 億美元，年增 68%，占 59%；2027 財測年增 25%，成長來源改由房貸與學貸再融資帶動，個貸增速放慢"},{"item":"金融服務段","value":"Q3 淨營收 5.25 億，年增 25%（淨利息收入 +38%、非利息收入 +13%）；2027 財測年增 35%"},{"item":"技術平台段","value":"Q3 營收 8,740 萬，年減 24%（排除流失的大客戶則年增 18%）；段貢獻利潤只有 Q2 的 1,200 萬，Q3 段利潤事實表未涵蓋；2027 財測年增 25%"},{"item":"LPB（含在放款段內）","value":"Q3 代外部資金方放款 38 億、收入 1.53 億（Q2 為 31 億、1.43 億）；管理層稱變現率只在區間內波動"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"銀行沒有毛利率；淨利差 6.14%，季增 16bp"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"個貸份額估計上升；平台段客戶流失發生在非核心段"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"手續費覆蓋率上升的同時，個貸放款量創高"},{"signal":"EPS 成長顯著高於營收成長（差距 >5pp）","lit":true,"note":"FY2025→FY2027：EPS 由 0.39 到 0.90，年複合約 52%；營收由 36.1 億到 64 億，年複合約 33%，差 19pp。來源是淨利率擴張，屬一次性"},{"signal":"FCF／淨利 <0.75 連兩年","lit":false,"note":"不適用：銀行放款計入營運現金流，改看有形淨值年增 25%"},{"signal":"SBC 占營收 >5% 且逐年上升","lit":null,"note":"Q3 為 5.2%，已過線；事實表沒有歷年 SBC，無法判斷是否逐年上升，屬資料缺口"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"未見"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋產業倍數"},{"signal":"維持性資本支出占 FCF >60%","lit":false,"note":"不適用"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"未見"}],"trap_rating":"🟡（亮 1 個，另有 2 個資料缺口）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠盈餘留存與放款再投資，不靠併購；2026 年三筆收購條款未揭露、規模小，展開也沒有可算的報酬數字"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"過去收購形成的技術平台段（Galileo、Technisys），Q3 營收年減 24%，Q2 貢獻利潤 1,200 萬美元（年化約 4,800 萬）。收購對價事實表未涵蓋，無法算出已實現 ROIIC；2026 年三筆收購條款也未揭露。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"沒有回購計畫；反而在 2025-12 以 27.50 美元增發 5,775 萬股。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 單季 7,090 萬美元×4≈2.84 億，以現價 17.38 計約 1,630 萬股，占 12.97 億股約 1.3%／年，沒有回購抵銷，勉強達標。但若用財測淨利÷EPS 推算稀釋股數，2026→2027 年增約 3%（含可轉債等），改用這個口徑就不過。","grade":"過"}]},"valuation":{"basis":"主錨用 P/TBV 對照 ROTCE（合理倍數＝(ROTCE−g)÷(股權成本−g)），輔以前瞻本益比","tier":"數位銀行／消費放款（金融類）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業 P/TBV 或前瞻本益比，無法做倍數對照；終端倍數只能用自身現值校準"},"fwd_pe":28.48,"peg":0.66,"percentile_5y":31.4,"val_light":"🟡","val_light_derivation":"兩把尺結論相反。銀行尺偏貴：P/TBV 2.32 倍，以 ROTCE 約 10%、股權成本約 10% 推算，合理倍數只有約 1.0 倍，現價已預付 ROTCE 升到約 15% 的路徑（(15%−6%)÷(10%−6%)＝2.25 倍）。成長尺偏便宜：FY2027 共識 EPS 對應 19.5 倍，PEG 約 0.66。兩尺一貴一便宜，取中間，判為合理。歷史分位用的是 P/S 四個年度端點中的 31%，不是五年連續序列。","upside_short_pct":18,"upside_mid_pct":41},"trap_analysis":{"verdict":"🟡","label":"成長正在兌現，但信用循環與公允價值查核兩關還沒過"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"聯準會今年已升息一次，管理層預期年內再升兩次，2027 財測再假設兩次。TransUnion 2026Q2 無擔保個貸借款人 60 天以上逾期率 3.81%（去年 3.37%）。放款段占營收 59%，以個貸為主；個貸帳面標記 103.3%；總資本比單季降 180bp。","assumption":"SoFi 客群偏高收入，這輪升息不會把個貸全口徑淨壞帳率推過 5%。","consequence":"壞帳升到 6–7%、標記跌破面值，EPS 在 2028 年掉到 0.35 左右；LPB 資金方縮手，資本比逼近下限，被迫以低 P/TBV 增資。五年後股價約 8 美元（−54%）。","ruling":"採納為空頭主線，機率 30%。這條與唯一致命數字同源，門檻沿用個貸淨壞帳率 5.0%。","watch":"每季的個貸全口徑淨壞帳率、表內 90 天逾期率、個貸標記、總資本比","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","end_markets#5","financial_regulatory_capital_rules#0"],"fact_refs":["f_kpi9_tangible_book_value_rotc","f_kpi1_adjusted_net_revenue"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 單季 7,090 萬美元，占調整後淨營收 5.2%。2025-12 以 27.50 美元增發 5,775 萬股。以財測淨利÷EPS 推算，稀釋股數 FY2026 約 13.8 億、FY2027 約 14.2 億，年增約 3%。存款靠高利率獲客（App 廣告 4.4% 年利率）。技術平台段連三季年減兩成以上，費收占比靠它推升的那條路受阻。","assumption":"營收與會員成長會轉成每股盈餘與每股有形淨值的成長。","consequence":"營收五年翻倍，但每年 3% 稀釋加上存款成本降不下來，ROTCE 卡在 12–13%，每股價值的成長只剩營收成長的一半左右。","ruling":"部分採納。每股有形淨值年增 25%（7.48 對 5.97），目前跑贏稀釋，但其中一部分來自 27.50 美元的高價增發，這種效果不會重複。基本情境 EPS 已內含每年約 2–3% 的股數增加；若稀釋超過每年 4%，就下修基本情境。","watch":"每季稀釋股數年增率、SBC 占營收比、費收型營收占比","evidence_refs":["channel_business_model_shift#2"],"fact_refs":["f_kpi4_share_based_expense_sbc","f_kpi9_tangible_book_value_rotc","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"P/TBV 2.32 倍對 ROTCE 約 10%；用合理倍數公式算，10% ROTCE 只值約 1.0 倍，ROTCE 要長期維持約 15% 才撐得起現價。2027 展望與共識幾乎相同：營收 64 億對 63.9 億，EPS 0.90 對 0.89。Q1 後 Morgan Stanley、Truist 把目標價降到 16、17 美元。","assumption":"市場會繼續用成長股倍數，而不是銀行倍數來評價 SoFi。","consequence":"若市場改用銀行尺，而 ROTCE 到 2028 只有 13%，合理 P/TBV 約 1.75 倍；乘上 2028 年底推算的每股有形淨值約 9.7 美元，約 17 美元，等於兩年零報酬。","ruling":"部分採納，估值因此降為合理。但對 2027 EPS 19.5 倍、EPS 年增近五成，不是泡沫價，不構成迴避的理由。","watch":"季度 ROTCE 與 15% 路徑的差距、P/TBV","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_kpi9_tangible_book_value_rotc","f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy2"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 15.25 → 本次 17.38（+14.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=15.25","side_b":"本次 price_at_dd=17.38","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 15.25 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 15.25 美元：Bull 價 36、Bear 價 10.3，五年期望值 +58.3%，基準年化 10.4%，不對稱比 4.4","side_b":"本次情境、股價仍用 15.25 美元：Bull 價 46、Bear 價 8，五年期望值 +78.9%，基準年化 14.3%，不對稱比 3.53","ruling":"先換情境、股價不動：五年期望值多 20.6 個百分點，基準年化多 3.9 個百分點。不對稱比由 4.4 變為 3.53。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 15.25 美元：五年期望值 +78.9%，基準年化 14.3%，不對稱比 3.53","side_b":"本次情境、股價 17.38 美元：五年期望值 +57.0%，基準年化 11.3%，不對稱比 2.54","ruling":"再換股價、情境不動：起點價上漲 14.0%，五年期望值少 21.9 個百分點，基準年化少 2.9 個百分點，不對稱比由 3.53 降到 2.54。合計五年期望值比前份少 1.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值結論與裁決","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-07-30，股價 15.25）：估值偏便宜；裁決觀望","side_b":"本次（股價 17.38，+14%）：估值合理；裁決與角色由本次輸入重新決定","ruling":"FY2026 共識 EPS 只從 0.60 升到 0.61（+1.7%），股價卻漲了 14%，前瞻本益比跟著上升。以每股有形淨值 7.48 計，P/TBV 2.32 倍、ROTCE 約 10%，銀行尺偏貴、成長尺便宜，所以降一級到合理。變動主因是價格，不是基本面轉差。","evidence_level":"事實表價格與共識","settle_metric":"P/TBV 與季度 ROTCE","if_then":["若股價回到 15 美元以下而基本面無損，則估值回到偏便宜，可分批反買"],"evidence_refs":[]},{"axis":"前份漂移：情境機率與回撤區間","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 28%、空頭 27%、最大回撤 −55%","side_b":"本次：多頭 25%、空頭 30%、最大回撤 −45% 到 −65%","ruling":"前份預期聯準會降息，結果是已升息一次、年內預期再升兩次，2027 財測再假設兩次；產業無擔保個貸 60 天以上逾期率年增 44bp。基本情境 EPS 年複合 23.5%，高於內生上限 16.5%，空頭機率至少要 30%。最大回撤改給區間，依據見情境樹。","evidence_level":"公司法說與產業信用數據","settle_metric":"2026Q4 與 2027Q1 個貸全口徑淨壞帳率","if_then":["若連兩季淨壞帳率 ≤3.5% 且已再升息兩次，則空頭機率降回 25%"],"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"axis":"前份漂移：基本面欄位複核後維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：品質訊號 B、陷阱風險中度、護城河持平、五年後跑道寬、金融類、未判循環位置","side_b":"本次：與前份相同，以 Q3 新數據複核後維持","ruling":"支持飛輪的數據：會員年增 35%，每會員產品數 1.47→1.56，交叉購買占新產品 51%。但平台段大客戶流失、放款競爭加劇，護城河不升級。衰退訊號只亮一個（EPS 成長遠高於營收成長，來自利潤率擴張），陷阱風險維持中度。個貸份額約 12%（Dolphin 估計），金融服務段 2027 財測年增 35%，跑道維持寬。循環位置不適用，本檔以金融類評估，不是循環股。","evidence_level":"公司一手揭露","settle_metric":"每會員產品數、費收型營收占比","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"平台段 YoY 轉正或段 margin ≥25%，且營收／有形權益比首度回升至 ≥0.55（現 0.503）；技術路徑另計＝站回 W104 $17.70 滿 4 週","side_b":"週收盤站回104週均線（現18.81美元）滿4週，且最近一季個貸全口徑淨壞帳率≤4.0%、2027年未增發普通股","ruling":"舊條件的後半段已達成：CFO 揭露營收／權益比 Q3 約 0.57（前份記 0.503，CFO 稱 Q2 已 0.55，兩者口徑可能不同）。前半段會在 2027Q1 因大客戶 2025 年遷出的基期效應自動轉正，那是機械觸發，不是證據。因此改綁本次唯一致命數字（個貸壞帳）加技術面確認，滿足後才建首倉。104 週均線已由 17.70 升到 18.81。","evidence_level":"公司法說與週線均線","settle_metric":"週收盤相對 104 週均線、個貸全口徑淨壞帳率","if_then":["若站回 104 週均線但個貸淨壞帳率 >4.0%，則不追"],"evidence_refs":[]},{"axis":"前份漂移：清倉與減碼門檻（新設）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（null）","side_b":"清倉：個貸全口徑淨壞帳率任一季 >5.0%，或年報查核出現重述或重大內控缺失。減碼：總資本比 <12.5% 或增發普通股，減碼一半；2027 年任兩季 ROTCE <11%，減碼三分之一","ruling":"前份只有論點與風險，沒有可執行的清倉線。本次替信用、資本、會計三個最大敏感項各設門檻，數字都取自公司每季揭露。","evidence_level":"公司一手揭露","settle_metric":"各門檻的季度讀數","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：Single Thing（新設）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"個人貸款全口徑年化淨壞帳率（排除逾期貸款出售）任一季升破 5.0%（2026Q3 為 3.4%）","ruling":"前份把信用風險列為多條風險之一。本次判定它是數學上最大的單一敏感項，因為它同時打到淨利息收入、公允價值標記、LPB 需求與資本比，所以升格為 Single Thing。","evidence_level":"公司法說的利差拆解","settle_metric":"個貸全口徑年化淨壞帳率","if_then":[],"evidence_refs":["financial_capital_credit_cycle#0"]},{"axis":"信用：公司壞帳改善，產業逾期上升","cause":null,"prior_field":null,"side_a":"公司：個貸全口徑淨壞帳率由 Q2 3.7% 降到 Q3 3.4%，年降 80bp；表內 90 天逾期 42bp，持平。執行長稱未見會員借貸放緩。","side_b":"產業：TransUnion 2026Q2 無擔保個貸借款人 60 天以上逾期 3.81%（去年 3.37%），消費者 90 天以上逾期升到 2.26%；聯準會轉為升息。","ruling":"可調和，屬程度差異。產業惡化主要來自次級族群，SoFi 客群偏高收入。但公司壞帳改善有一部分是平均貸款餘額成長稀釋了分母，新放款也還沒走完一個升息週期。當下讀數採公司側，空頭機率 30% 反映這點尚未驗證。","evidence_level":"公司一手揭露對照產業數據（搜尋摘要）","settle_metric":"2026Q4、2027Q1 個貸全口徑淨壞帳率與表內 90 天逾期率","if_then":["若 2027Q1 個貸淨壞帳率 >4.5% 且 90 天逾期 >60bp，則減碼一半","反向條件：若連兩季 ≤3.5% 且已再升息兩次以上，則加碼到目標倉位"],"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"axis":"會計：公允價值計量","cause":null,"prior_field":null,"side_a":"放空方（Muddy Waters，2026-03-17）稱 SoFi 的貸款會計與公允價值評價高估；律所 2026-05-04 公告展開證券法調查。","side_b":"公司：Q3 公允價值負向影響逾 8 億美元，約 7.34 億由避險利得抵銷；個貸標記 103.3%，季降 140bp。現金營收 14 億美元（淨利息收入 9.27 億），連四季破 10 億。執行長買進 28,900 股。","ruling":"不可調和，兩邊方向相反；現有證據偏向公司側：本季公允價值是淨拖累而不是墊高盈餘，現金營收也與調整後淨營收（13.71 億）相當。但標記仍高於面值 3.3 個百分點，信用轉弱時會一次回吐。在 FY2026 年報查核意見（約 2027-02）出來之前無法裁決。","evidence_level":"公司一手揭露加放空報告（未見原文）","settle_metric":"FY2026 10-K 查核意見與公允價值相關查核事項；個貸標記","if_then":["若出現重述或重大內控缺失，則清倉","反向條件：若查核意見無保留且個貸標記 ≥101%，則取消為此預留的減碼，維持原倉位"],"evidence_refs":["major_events#1","major_events#2","lawsuit_class_action#0"]},{"axis":"口徑：個貸風險調整後利差前後不一","cause":null,"prior_field":null,"side_a":"2026-07-29 Q2 法說，CFO：核心個貸風險調整後利差約 6.1%。","side_b":"2026-10-27 Q3 法說，CFO：約 7.6%（票息 12.8%＋手續費 1.4%－資金 3.1%－損失 3.4%），並稱票息加手續費收益率季持平、年增逾 100bp。","ruling":"不可調和，屬數字層矛盾。票息加手續費季持平、損失只降 30bp，推不出單季升 150bp；最可能是兩季口徑不同（例如 Q2 未含手續費）。在 10-Q 對帳之前，不把 7.6% 當成定價力提升的證據，護城河的定價分不因此加分。","evidence_level":"管理層口頭數字","settle_metric":"Q3 10-Q 的個貸收益拆解；Q4 法說是否沿用同一口徑","if_then":["若 Q4 以同口徑仍 ≥7.0%，則把定價力由 6 分調到 7 分","反向條件：若口徑回到 6% 區間，則維持原分數，並把手續費依賴列為放款定價風險"],"evidence_refs":[]},{"axis":"市場：券商下修目標價，公司上修財測","cause":null,"prior_field":null,"side_a":"Q1 後券商下修目標價：Morgan Stanley 16（賣出）、Truist 17（持有）、Citi 30、Mizuho 29。共識為持有，平均目標價約 21.4（2026-08）。","side_b":"Q3 公司上修 2026 營收到 50.4 億，首次給出 2027 營收 64 億、EPS 0.90，並明言不需增資。","ruling":"可調和。下修發生在 Q3 上修之前，屬事實層的時間差。但 2027 展望與共識幾乎相同（營收 64 億對 63.9 億，EPS 0.90 對 0.89），上修沒有帶來新的盈餘驚喜。目標價全距 16 到 30，約 1.9 倍，未超過 2.5 倍，不因此下調信心。現價接近看空券商的目標價，代表市場的風險折價還在。","evidence_level":"賣方動態（搜尋摘要）對照公司一手財測","settle_metric":"Q4 財報後 FY2027 共識 EPS 的修正方向","if_then":["若 Q4 財報後 FY2027 共識上修 ≥5%，則可加碼","反向條件：若下修 ≥5%，則停止加碼"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"管理層前後說法：SoFi Plus 目標與盈餘 4 倍","cause":null,"prior_field":null,"side_a":"2026-07-29，執行長 Noto：一年後若沒有 100 萬 SoFi Plus 付費會員會失望。","side_b":"2026-10-27，執行長 Noto：Q3 SoFi Plus 增長低於預期（約 27.5 萬），並說到期沒達到也沒關係，總會到。同場稱產品成長 4 倍可推動盈餘 4 倍，卻又說 2026–2030 加權每產品收入會下降。","ruling":"可調和，但扣管理層信用分。SoFi Plus 年化收入約 3,300 萬美元（27.5 萬×120 美元），不承重。盈餘 4 倍與每產品收入下降要同時成立，淨利率得由 20% 升到 30%。基本情境 2031 年 EPS 1.75，約為 2026 的 2.9 倍，不採用 4 倍。","evidence_level":"兩季法說逐字稿","settle_metric":"SoFi Plus 付費會員數、淨利率","if_then":["若 2027 年底前 SoFi Plus 達 100 萬，則多頭機率可加回 28%"],"evidence_refs":[]},{"axis":"前季迴避的三個問題，本季回答程度","cause":null,"prior_field":null,"side_a":"2026-07-29 Q2 法說沒有正面回答三題：EBITDA 為何不上修、LPB 個貸量是否繼續受限、超額資本消耗的速度。","side_b":"2026-10-27 Q3 法說：EBITDA 由 16 億上修到 16.6 億；LPB 單季 38 億創高，Q4 進度超前；CFO 給出資本容量算式（13.5% 資本比下可支撐 710 億風險資產，現在 560 億，加上盈餘再生約 140 億），但仍未給消耗時程。","ruling":"前兩題已補答。資本消耗速度只給了容量、沒給節奏，列入資本風險追蹤；總資本比單季降 180bp 的速度若持續，2027 年中就會接近規劃水位。","evidence_level":"兩季法說逐字稿","settle_metric":"每季總資本比降幅","if_then":["若連兩季單季降幅 >200bp，則停止加碼"],"evidence_refs":["financial_regulatory_capital_rules#0"]},{"axis":"產業態勢：競爭、結構與其他變數","cause":null,"prior_field":null,"side_a":"競爭惡化：10-K 稱新進者與既有業者會壓價搶份額；Upstart 放款年增 50%；平台段重要客戶轉投對手。","side_b":"結構轉好：SoFi 個貸份額由 2023 年約 6.8% 升到 2025 年底約 12%（Dolphin 估計）；LPB 需求大於供給；會員年增 35%。","ruling":"雙向拉鋸。SoFi 仍在拿份額，但放款定價壓力與平台客戶集中同時存在。其他結構變數中性：Basel III 重新提出較輕的版本，2019 年 FTC 同意令沒有新動作。","evidence_level":"10-K 加第三方估計","settle_metric":"個貸份額、核心個貸風險調整後利差","if_then":["若風險調整後利差（以 Q3 口徑）連兩季 <6.0%，則判為競爭惡化中，停止加碼"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#1"]},{"axis":"反方論證：現在就買的最強理由","cause":null,"prior_field":null,"side_a":"現在就買：股價是 2027 共識 EPS 的 19.5 倍，2027 EPS 年增約 46%；不需增資；升息下營收仍年增 44%；每股有形淨值年增 25%；股價比 2025-12 增發價 27.50 低 37%。","side_b":"再等一下：股價仍在 52 週與 104 週均線之下，信用在升息中還沒被考驗，年報查核意見也還沒出。","ruling":"買進理由在基本面上成立，但時點證據不足。首倉條件設為技術面站回 104 週均線，並搭配壞帳讀數；若價格先漲、證據還沒到，就不追。","evidence_level":"公司一手揭露加週線均線","settle_metric":"週收盤相對 104 週均線、個貸全口徑淨壞帳率","if_then":["若股價站回 104 週均線但個貸淨壞帳率 >4.0%，則不追","反向條件：若股價跌破 15 美元而個貸淨壞帳率 ≤3.5%、總資本比 ≥13.5%，則分批反買，首倉 2%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"個貸全口徑年化淨壞帳率任一季突破 5.0%","type":"Single Thing","maps_to":"R3","metric":"個貸全口徑年化淨壞帳率（排除逾期貸款出售）","threshold":">5.0%（2026Q3 為 3.4%）","action":"清倉","source_freq":"季度財報新聞稿與法說","date":null,"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"n":2,"text":"個貸淨壞帳率連兩季 >4.5%，或表內 90 天逾期率 >60bp","type":"風險","maps_to":"R3","metric":"個貸全口徑淨壞帳率、表內 90 天逾期率","threshold":">4.5% 連兩季；或 >60bp（2026Q3 為 42bp）","action":"減碼一半並停止加碼","source_freq":"季度法說","date":null,"evidence_refs":["financial_capital_credit_cycle#1","end_markets#5"]},{"n":3,"text":"FY2026 年報查核意見對公允價值的結論","type":"風險","maps_to":"R2","metric":"查核意見、公允價值相關查核事項、重述或內控缺失","threshold":"出現重述或重大內控缺失","action":"清倉；只列為查核事項而沒有調整則不動","source_freq":"年度 10-K","date":"2027-02","evidence_refs":["major_events#1","major_events#2","lawsuit_class_action#0"]},{"n":4,"text":"總資本比跌破 12.5%，或宣布增發普通股","type":"減碼","maps_to":"H2","metric":"總資本比、普通股增發","threshold":"<12.5%（2026Q3 為 17%）或任何普通股增發","action":"減碼一半，並以新股數重算情境","source_freq":"季度 8-K 與 10-Q","date":null,"evidence_refs":["financial_regulatory_capital_rules#0"]},{"n":5,"text":"2027 年季度 ROTCE 達到 12%","type":"假設驗證","maps_to":"H1","metric":"季度 ROTCE","threshold":"2027 年任兩季 ≥12%","action":"論點獲得驗證，可由首倉加到目標倉位 4%","source_freq":"季度財報新聞稿","date":"2027-07","evidence_refs":[]},{"n":6,"text":"大客戶基期效應消失後，平台段能否回到財測成長","type":"假設驗證","maps_to":"R1","metric":"技術平台段營收年增率","threshold":"2027Q1 ≥+18%；<10% 視為未通過","action":"未通過則停止加碼","source_freq":"季度財報新聞稿","date":"2027-04","evidence_refs":["end_markets#2","channel_business_model_shift#2","substitute_technology#1"]},{"n":7,"text":"產業無擔保個貸逾期率續升","type":"風險","maps_to":"R3","metric":"TransUnion 無擔保個貸借款人 60 天以上逾期率","threshold":">4.2%（2026Q2 為 3.81%）","action":"停止加碼","source_freq":"TransUnion 季報","date":null,"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1"]},{"n":8,"text":"週收盤站回104週均線（現18.81美元）滿4週，且最近一季個貸全口徑淨壞帳率≤4.0%、2027年未增發普通股","type":"估值rearm","maps_to":"H2","metric":"週收盤相對 104 週均線、個貸淨壞帳率、普通股增發","threshold":"站回滿 4 週，且壞帳 ≤4.0%，且未增資","action":"建首倉 2%","source_freq":"每週價格加季度財報","date":null,"evidence_refs":[]},{"n":9,"text":"股價漲到盈餘撐不住的區間","type":"減碼","maps_to":"H1","metric":"股價、季度 ROTCE","threshold":"股價 >27 美元（約 2027 共識 EPS 30 倍、P/TBV 3.6 倍），而 ROTCE 未達 13%","action":"減碼三分之一","source_freq":"每日價格加季度財報","date":null,"evidence_refs":[]},{"n":10,"text":"放款段占營收持續上升，收入結構更集中","type":"風險","maps_to":"R1","metric":"放款段占調整後淨營收比","threshold":"連兩季 ≥62%（2026Q3 為 59%）","action":"停止加碼","source_freq":"季度財報新聞稿","date":null,"evidence_refs":["end_markets#5"]},{"n":11,"text":"個貸定價被侵蝕","type":"風險","maps_to":"R5","metric":"核心個貸風險調整後利差（以 Q3 口徑）","threshold":"連兩季 <6.0%（2026Q3 約 7.6%）","action":"停止加碼","source_freq":"季度法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":12,"text":"2026Q4 財報與 2027 財測更新後重新研究","type":"複審日期","maps_to":"H1","metric":"2027 EPS 財測、個貸淨壞帳率、總資本比","threshold":"財報公布","action":"重新跑完整研究","source_freq":"季度","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"個貸全口徑年化淨壞帳率（排除逾期貸款出售）","bear_threshold":"任一季 >5.0% 即清倉（2026Q3 為 3.4%）","window":"每季，至 2028Q4","source":"公司季度財報新聞稿與法說","last_status":"ok"},{"metric":"年報查核意見與公允價值相關查核事項","bear_threshold":"出現重述或重大內控缺失即清倉","window":"FY2026 年報（約 2027-02）","source":"SEC 10-K","last_status":"unknown"},{"metric":"總資本比與普通股增發","bear_threshold":"總資本比 <12.5% 或宣布增發普通股，即減碼一半（2026Q3 為 17%）","window":"每季，2027 全年","source":"公司 8-K、10-Q 監理資本揭露","last_status":"ok"},{"metric":"個貸公允價值標記","bear_threshold":"<101% 即停止加碼（2026Q3 為 103.3%，季降 140bp）","window":"每季","source":"季度法說與 10-Q","last_status":"warning"},{"metric":"季度 ROTCE","bear_threshold":"2027 年任兩季 <11%，減碼三分之一","window":"2027Q1 到 Q4","source":"公司季度財報新聞稿","last_status":"unknown"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#0","reason":"這是 2019 年同意令既有義務的揭露，只限制行銷時誤述節省金額；10-K 沒有揭露任何違反、新調查或罰款金額。證據描述的是一個存在七年的行為約束，不是新事件，也沒有可量化的營收暴露。"},{"ref":"reg_tariff_export#0","reason":"10-K 的制式風險條款，原文只說貿易政策過去曾影響金融市場，沒有給出公司損益的傳導路徑或金額。總經對消費信用的實際影響，已改由個貸逾期率與壞帳門檻直接追蹤，不重複計入。"},{"ref":"reg_tariff_export#1","reason":"條款只說全球匯款服務可能受制裁限制，但事實表與 Q3 逐字稿都沒有把匯款列為營收來源或給出占比，證據本身沒有暴露金額。"},{"ref":"reg_tariff_export#2","reason":"這是 2025-04 單一分析師（Morgan Stanley）的方向性意見，沒有量化。之後 18 個月，公司個貸全口徑淨壞帳率反而由 2026Q2 的 3.7% 降到 Q3 的 3.4%，預期的關稅傳導沒有出現在損益上，證據已過時。"},{"ref":"geo_supply_chain#0","reason":"引用的是 FY2024 年報的制式條款，已被 FY2025 年報取代；沒有指名單一供應商，也沒有服務中斷紀錄或金額，無法從這條證據量化營運中斷風險。"},{"ref":"$.scenario_inputs.p","reason":"閘把兩個機率放在同一期間比較。唯一致命數字的 15% 是未來 12 到 24 個月內任一季破 5.0% 的近端機率；空頭情境的 30% 是五年情境權重，除了這段近端機率，還包含兩年後才破線的路徑，以及基本情境 EPS 年複合 23.5% 高於內生上限 16.5% 所加上的權重（見情境機率與回撤區間的漂移裁定）。空頭 EPS 路徑把谷底放在 2028 年只是代表性時點，不代表 30% 全落在兩年內。兩個數字口徑不同、方向一致，機率不改。"}],"decision_out":{"role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場仍把 SoFi 當成要靠增資撐成長、利率一升就失速的消費放款商：2026 年股價跌約四成，Morgan Stanley、Truist 在 Q1 後把目標價降到 16、17 美元，現價就在這一帶。Q3 已經反證這兩個前提：升息中營收仍年增 44%、個貸壞帳年降 80bp，CFO 也給出不需增資的資本算式。不過 2027 展望與共識幾乎一樣，市場錯的是風險折價，不是盈餘預期；要反轉，得靠接下來的信用數據。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=7.16, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='現價不建倉。首倉 2% 要等以下任一條件成立：一、週收盤站回 104 週均線（現 18.81 美元）滿 4 週，且最近一季個貸全口徑淨壞帳率 ≤4.0%、2027 年未增發普通股；二、股價跌破 15 美元，同時個貸全口徑淨壞帳率 ≤3.5%、總資本比 ≥13.5%。價格先到、壞帳證據沒到，就不追。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"4%。路徑風險高但論點完整，不因股價波動砍倉，要有深回撤的心理準備","requires_critic":[],"verdict":"觀望","rearm_trigger":"週收盤站回104週均線（現18.81美元）滿4週，且最近一季個貸全口徑淨壞帳率≤4.0%、2027年未增發普通股","exec_line":"首倉 2%，分兩批：第一批在重啟條件達成時，第二批等 2027Q1 個貸淨壞帳率 ≤4.0%。2027 年兩季 ROTCE ≥12% 後，上限加到 4%。任一清倉條件觸發即全數出清。"},"reasoning":{"industry":"營收結構（2026Q3）：放款段調整後淨營收約 8.07 億美元，年增 68%，由個貸需求與手續費帶動。金融服務段 5.25 億，年增 25%，其中淨利息收入 +38%、非利息收入 +13%。技術平台段 8,740 萬，年減 24%，因大客戶 2025 年遷出；排除該客戶後 +18%。三段相加超過總額的部分是企業層調整。全公司調整後淨營收 13.71 億，GAAP 13.85 億。銀行不揭露毛利率與營業利益率，改看調整後 EBITDA 4.70 億（34%）、GAAP 淨利 2.41 億（17%）、淨利差 6.14%（季增 16bp）。單點依賴：個貸是唯一承重產品，Q3 個貸放款 126 億，占全部放款 169 億的四分之三，這是集中度風險，不是護城河證據。資金端以存款為主（513 億，目標 80–90% 由存款支應）。產業週期判在過熱段：全產業與公司的個貸放款量都在高檔；聯準會今年已由降息轉為升息；產業無擔保個貸逾期率年增 44bp。信用指標開始轉弱，但還沒出現損失潮。財測：2026 營收 50.4 億（+40%），2027 展望 64 億（+27%），淨利率由 17% 升到 20%。","moat":"機制是「產品廣度×每產品單位經濟」推高會員終身價值，再用存款利率與貸款利率讓利獲客，取代分行成本。事實表沒有同業 ROIC 或 ROTCE；FCF 利潤率對銀行不可比（SoFi 為負，因放款計入營運現金流）。所以方向改用份額與留存來判斷：個貸份額估計由 2023 年約 6.8% 升到 2025 年底約 12%；每會員產品數一年由 1.47 升到 1.56；新產品 51% 來自既有會員；使用兩項以上產品的會員占 37%（去年 33%）。執行力給 8 分：營收成長加 EBITDA 利潤率連 20 季超過 40；2026 營收比原始財測多 3.85 億；升息環境下營收仍年增 44%。定價力給 6 分：手續費已覆蓋逾半數新個貸，公司稱個貸風險調整後利差年增逾 100bp，但兩季口徑沒對齊（見矛盾裁定）；個貸票息連幾季下滑；存款仍需高利率；平台段重要客戶轉投對手。當期 ROTCE 約 10%，增量報酬約 16.5%，報酬能維持多久見四檢查點。","growth":"成長以量為主：會員年增 35%，產品年增 44%。價的部分是放款段每產品年化收入由 782 升到 942 美元，金融服務段由 88 升到 90 美元。沒有回購，併購規模小。共識三年 EPS：FY2025 實際 0.39（GAAP）、FY2026E 0.61、FY2027E 0.89、FY2028E 1.14（Koyfin 快照，分析師家數事實表未涵蓋），年複合約 43%。內生上限是 16.5%（增量 ROTCE 約 16.5% × 盈餘全數留存），缺口約 26 個百分點。缺口可以歸因：一是淨利率由 13%（FY2025）升到 20%（FY2027 財測）；二是超額資本投入（CET1 由 22.8% 降到 16.9%），把營收／權益比由 0.50 推到 0.57。兩者都是一次性墊高；等資本比回到中低十幾%、淨利率接近 25–30%，成長會回落到內生上限附近。跑道年數：個貸份額近兩年每年約推進 2.6 個百分點，照這個速度約 7 年到 30%，屬中等。管理層也預告 2026–2030 加權每產品收入會下降，因為產品組合偏向單價低的金融服務；產品成長 4 倍不等於營收成長 4 倍。","governance":"FCF／淨利對銀行不適用：放款計入營運現金流，FY2025 自由現金流 −39.9 億，拿來對淨利 4.8 億沒有意義。改看有形淨值：一年增加 25 億到 97.05 億，每股 7.48（+25%）。其中約 15.9 億來自 2025-12 的增發（57,754,660 股×27.50 美元）；以 2025 年 9 月底每股有形淨值 5.97 計，約 4.6 倍 P/TBV 發股（實際發股時淨值略高，倍數略低），對既有股東是增值。近三年現金去向的四分拆解，事實表未涵蓋。看得到的是：盈餘全數留存放款，Q3 貸款增加 58 億，CET1 由 2025 年底 22.8% 降到 16.9%，管理層計畫降到中低十幾%。SBC 單季 7,090 萬，占調整後淨營收 5.2%、占調整後 EBITDA 15.1%。收購：2026Q2 買下 Peach Finance 與 Composer，另有報導收購 PrimaryBid 資產，條款都未揭露；過去收購形成的技術平台段營收年減 24%，Q2 貢獻利潤只有 1,200 萬。2027 計畫明言不增資：以 13.5% 資本比計，現有資本可支撐 710 億風險資產（現在 560 億），加上盈餘再生約 140 億的容量。","valuation":"銀行尺：P/TBV＝17.38÷7.48＝2.32 倍。合理 P/TBV＝(ROTCE−g)÷(股權成本−g)；以股權成本 10%、長期成長 6% 計，ROTCE 10% 只值 1.0 倍，12%（2027 推算值）值 1.5 倍，15% 值 2.25 倍。現價大致已預付 15% 的 ROTCE。成長尺：前瞻本益比 FY2026 為 28.5 倍，FY2027（共識 0.89）19.5 倍，FY2028 15.2 倍；PEG 約 0.66（28.48 ÷ 三年 EPS 年複合 43%）。歷史位置：P/S 在四個年度端點中位於 31%，EV/S 位於 7%，本益比只有兩個年度端點；三者都不是五年連續分位。短期上檔：2027 共識 EPS 0.89 × 23 倍≈20.5 美元，約 +18%。中期上檔：基本情境 FY2029 EPS 1.36 × 18 倍≈24.5 美元，約 +41%。分母是否有爭議：放空方質疑公允價值計量，但本季公允價值淨效果是拖累（負向逾 8 億、避險利得約 7.34 億抵銷），現金營收也與調整後淨營收相當，EPS 分母沒有被墊高的跡象，不視為爭點。共識近三個月 FY1 上修 1.7%，FY2 持平。","premortem":"三個視角的反證與裁定見反證紀錄。論點失敗路徑（信用循環加上標記回吐）採納為空頭主線，機率 30%。股東經濟變差（每年稀釋約 2–3%、ROTCE 卡在 12–13%）部分採納。價格已反映太多（P/TBV 已預付 15% ROTCE）部分採納，估值因此降為合理。歷史回撤參考：2025-12 增發價 27.50 到 2026-07 低點 14.88，約 −46%。"},"plain":{"six":{"how_it_makes_money":"SoFi 賺的是會員的放款利差與手續費。放款段占調整後淨營收 59%，錢卡在資金成本與信用損失這一節：個貸票息 12.8% 扣掉資金成本 3.1%、損失 3.4% 之後，才是真正留下的。費收型營收占 42%，是降低這個依賴的第二條腿。","moat":"護城河持平，等級 B。多產品交叉購買讓每位會員的終身價值最高，SoFi 因此能把利潤讓回利率與費用去獲客。執行面在擴大；但放款端點對點競爭加劇、平台段又流失客戶，定價面只算穩定。","growth":"五年後跑道仍寬。個貸份額約 12%，會員 1,710 萬，離管理層 2030 年約 5,000 萬的規劃還遠；第二條成長曲線有來源可查：金融服務段 2027 財測 +35%，另有信用卡、SMB 放款與 LPB 新資產類別。但近三年 EPS 高成長有一大段來自一次性的利潤率擴張，不能直接外推。","capital":"資本配置中等。盈餘全數留下來做放款，不配息、不回購。2025-12 以 27.50 美元增發約 15.9 億美元，回頭看是以高 P/TBV 發股，對每股有形淨值有利。SBC 占營收 5.2%，年化稀釋約 1.3%，勉強達標。歷史收購形成的平台段正在萎縮，報酬無法驗證。","valuation":"現價要求 ROTCE 由 10% 升到約 15% 並長期維持，P/TBV 2.32 倍才算合理；換句話說，2027 財測要兌現，2028 還要再往上一段。資本算式與升息下的成長只給了一半證據，信用循環還沒過考驗。估值合理，但不便宜。","how_wrong":"最可能看錯的是升息中的個貸信用。全口徑淨壞帳率一旦突破 5%，淨利息收入、公允價值標記、LPB 需求與資本比會同時受傷。其次是年報查核對公允價值的結論（約 2027-02）。陷阱風險中度。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場仍把 SoFi 當成要靠增資撐成長、利率一升就失速的消費放款商：2026 年股價跌約四成，Morgan Stanley、Truist 在 Q1 後把目標價降到 16、17 美元，現價就在這一帶。Q3 已經反證這兩個前提：升息中營收仍年增 44%、個貸壞帳年降 80bp，CFO 也給出不需增資的資本算式。不過 2027 展望與共識幾乎一樣，市場錯的是風險折價，不是盈餘預期；要反轉，得靠接下來的信用數據。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"現價不建倉。首倉 2% 要等以下任一條件成立：一、週收盤站回 104 週均線（現 18.81 美元）滿 4 週，且最近一季個貸全口徑淨壞帳率 ≤4.0%、2027 年未增發普通股；二、股價跌破 15 美元，同時個貸全口徑淨壞帳率 ≤3.5%、總資本比 ≥13.5%。價格先到、壞帳證據沒到，就不追。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"金融","price_at_dd":17.38,"week26_return_pct":7.16,"consensus_rev_3m_pct":1.67,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"放空方質疑公允價值計量，但 Q3 公允價值淨效果為負（負向逾 8 億、避險利得約 7.34 億抵銷），現金營收約 14 億與調整後淨營收 13.71 億相當，EPS 分母沒有被墊高的跡象；年報查核意見（約 2027-02）出來前保留判斷。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"macro","event":"聯準會年內剩餘會議，管理層假設今年再升息","impact":"中","watch":"升息幅度與 2027 利率路徑；個貸資金成本"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"2026Q4 財報與 2027 財測更新","impact":"高","watch":"個貸全口徑淨壞帳率、總資本比、2027 EPS 0.90 是否維持"},{"date":"2027-02","date_precision":"month","type":"regulatory","event":"FY2026 年報查核意見","impact":"高","watch":"公允價值相關查核事項，以及有無重述或內控缺失"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"2027Q1 財報，平台段大客戶基期效應消失","impact":"中","watch":"平台段年增是否 ≥18%、ROTCE 是否 ≥11%"},{"date":"2027-12","date_precision":"month","type":"product","event":"SoFi Plus 100 萬付費會員目標期限","impact":"低","watch":"Q3 約 27.5 萬，管理層稱 Q4 成長已重新加速"}],"_projected_from":"v19"}
```
