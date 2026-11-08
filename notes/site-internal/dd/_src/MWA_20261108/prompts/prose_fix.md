你是 stock-analyst v20 的**散文層（prose）agent**，標的 MWA（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MWA　日期：2026-11-08　archetype：None　前份裁決：2026-05-24　A｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1611B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（379B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1124B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1467B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（928B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（470B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（903B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2192B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3423B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2910B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1611           3772-5389      5 條（2–6 內）  
s3                  8000         379           5335-7621      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3519          8037-11481      5 條（2–6 內）  
s6                 11000         470          7371-10530      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         903           1818-2597      5 條（2–6 內）  
s10                 5000        2192           1966-2808      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2910           2000-2090      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4629B；至少需散文≈40.37KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−100
−42%
−42
−28
−28%
−8.31
−5.0%
−3
0%
0
0.08
0.09
0.37%
0.75
0.9%
0.90
0.93%
0.967
01
1
1.1
1.1%
1.106
1.12
1.18
1.3%
1.31
1.33
1.37
1.39
1.4%
1.41
1.48
1.5
1.5%
1.53
$1.55
1.57
1.58
1.59
1.64
1.69
1.83
1.87
1.96
02
2
2.0
2.04
2.073
2.08
2.1
2.28
2.3%
2.37
2.42
2.46
2.5%
2.54
2.63
3
3%
3.2%
3.765
3.78
3.83
3.88
3.9
3.9%
4%
4
04
4.4%
4.54
5%
05
5.0%
5
5.5%
5.6%
5.66
5.8
5.9%
6
6%
06
6.575
6.6
6.6%
6.7%
7
7.0%
7%
7.31
7.4%
7.43
8
8%
08
8.175
8.7%
9
9.5
10
10%
10.07%
10.5
11
11.4
11.8
12
13
13.97
14
14.05%
14.3%
14.4
14.55
14.7
14.75
14.95
15.0
15
15.1
15.13
15.5
16
16.06%
16.25
16.9
16.92
17
17.06
17.29
17.6
18.2
18.53
18.76%
19
19.4%
19.73%
19.8%
20
20%
21.54%
21.7
21.9%
22.52%
23%
24%
24.05
24.6%
25
25%
25.2%
25.3%
25.31
25.4%
26
26%
26.0%
26.3%
26.5%
27%
27.5%
28
28%
28.5
30
30%
30.5%
31
31.9%
33.0%
34
34%
36%
36.3
36.5
37.0%
37%
37.4
38.24%
39%
42
42%
45%
49
49%
49.97
50
50%
55%
60
60%
65%
65
70
71
75%
81
84%
90
100
100%
$100
110
120%
150%
232
250
370
383
$390
800
940
2026
2027
2029
20261108
1,150
1,300
1,370
1,455
1,500
2,600
3,100
4,000
5,560
6,000
6,500
7,000
7,400
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
{"meta":{"ticker":"MWA","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Mueller Water Products"},"oneliner":"美國水管閥門與消防栓的置換需求很穩，三年利潤率多了 940 基點，但銷量在降，明年價格成本對利潤率只剩持平；現價約 15 倍 FY27 獲利，算合理，關鍵是第二季那次尚未公告的漲價留不留得住。","thesis":{"H":[{"id":"H1","text":"價格帶動、銷量止跌：排除計量後營收守住指引，之後銷量回到持平以上。","2y":"FY28 排除計量營收 ≥15.0 億美元（FY27 指引中位 14.55 億再加約 3%）","5y":"FY31 營收 ≥16.9 億美元（年複合約 3.9%）","10y":null,"threshold":"FY27 排除計量營收 ≥14.4 億，且排除消防栓基期後銷量不低於持平","source":"公司季度新聞稿與法說","drift_rule":"2 年期：連 2 季偏離門檻 ≥5% 削弱，連 3 季 ≥10% 反轉；5 年期：連 4 季 ≥5% 削弱，連 6 季 ≥10% 反轉"},{"id":"H2","text":"調整後 EBITDA margin 守住 26% 以上，靠製造效率與業務組合清理，不靠關稅退款。","2y":"FY28 ≥26.5%","5y":"FY31 ≥27.5%","10y":null,"threshold":"FY27 ≥26.0%（指引中位 26.3%）","source":"公司季度新聞稿與法說","drift_rule":"2 年期：連 2 季偏離門檻 ≥5% 削弱，連 3 季 ≥10% 反轉；5 年期：連 4 季 ≥5% 削弱，連 6 季 ≥10% 反轉"},{"id":"H3","text":"specialty valves 成為第二條成長線：雙位數成長延續，公司開始揭露規模。","2y":"到 FY28 連續兩年雙位數成長，仍占積壓訂單多數，並揭露營收占比","5y":"FY31 占營收 ≥20%（目前占比事實表未涵蓋）","10y":null,"threshold":"FY27 雙位數成長，且 FY28 前揭露營收占比","source":"法說、投資人日、10-K","drift_rule":"連續兩年未達雙位數即削弱；連續三年未達或未揭露占比即反轉"}],"R":[{"id":"R1","text":"關稅與成本壓過定價：Section 232 鋼鋁關稅 50% 壓在 Krausz 修理產品與 Specialty Valve 線，不再有關稅退款，FY27 價格成本對利潤率只剩持平；以色列與中國廠也是地緣單點。","h_ref":"H2","clock":"⚡","threshold":"連 2 季調整後毛利率年減 ≥100 基點，或 TTM 調整後 EBITDA margin 低於 24%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#5","geo_supply_chain#0","geo_supply_chain#2"]},{"id":"R2","text":"銷量下滑比公司假設的久：2026-08-06 McAndrew 說住宅不會一直低迷，市政與商業策略可抵銷；2026-11-05 的 FY27 指引仍假設住宅再跌低個位數、市政謹慎。","h_ref":"H1","clock":"🔥","threshold":"排除計量與消防栓基期後銷量連 2 季年減，或排除計量後營收連 2 季年減","evidence_refs":["end_markets#0"]},{"id":"R3","text":"通路議價：兩大經銷商占毛銷售 37%，最大一家 20%，非獨家且無長期合約，應收帳款也集中。","h_ref":"H2","clock":"🔥","threshold":"兩大合計 ≥42% 或最大一家 ≥25%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R4","text":"份額被對手或進口吃掉：寡占規格黏性是公司自述，份額資料缺失，運費與關稅變動會改變進口競爭力。","h_ref":"H1","clock":"🐢","threshold":"主要份額指標下滑 3 個百分點，或管理層承認流失份額（份額為資料缺口）","evidence_refs":["competitive_share_entrants#1","substitute_technology#2"]},{"id":"R5","text":"財務長交接與計量退出同時發生：2026-08-06 的財務長 Melissa Rasmussen，到 2026-11-05 已改由 Mike Morgan 發言，離任原因事實表未涵蓋；計量退出約 2,600 萬費用，保固義務留在公司，CEO 未正面回答有無對價。","h_ref":"H2","clock":"🔥","threshold":"計量退出總費用超過 3,100 萬美元、轉移拖到 FY28 下半，或調整項定義變更","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"FY27 第二季那次尚未公告的年度漲價，未能公告或留不住，使全年價格實現低於低個位數。","why_fatal":"價格是營收成長與利潤率擴張最可重複的來源，也是最大的單一敏感度：每 1 個百分點約影響 FY27 EPS 4.4%。FY27 價格成本對利潤率已只剩持平，這次沒守住就代表定價權到頂。","if_happens":"Base 轉向 Bear，margin 往 23% 回吐，EPS 往 1.33 到 1.41，股價約 15 到 17 美元；先減碼一半，下一季仍未回升則清倉。","how_monitor":"看 2027-02 第一季法說是否公告漲價，及 2027-05 第二季財報的全年價格實現、銷量與調整後毛利率；同時看對手是否跟進。","probability":"25%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.13,"peg_fy2":2.04,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.31,"FY2026E":1.57,"FY2027E":1.59,"FY2028E":null},"fy_end_month":9,"eps_basis":"調整後每股盈餘。FY2025A 由 FY26 的 1.57 與年增 19.8% 反推。Koyfin FY1 未滾動，對應剛結束的 FY2026（公司已報實際 1.57，含 0.09 一次性，扣除後 1.48）；FY2 的 1.59 對應 FY2027，與指引隱含約 1.57–1.58 相符。FY2028 無共識，留空。若 FY1 實為 FY2027，則 FY2028 共識為 1.59，結論更保守。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/scenario.json","archetype":{"primary":"受監管公用/穩定內需","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"需求來自市政維修汰換，客戶受預算與水費約束；近四年盈餘成長主要來自利潤率修復，而不是量的成長。"},"industry":{"clock_phase":"IV","sd_verdict_source":"需求屬結構性持久，老舊管網維修汰換占六成以上（2026-06-30 10-Q）；短期量縮屬週期性，FY26 新建住宅雙位數下滑、FY27 再跌低個位數，市政採購轉謹慎（2026-11-05 法說）。產業位置依銷量判為收縮段，不看股價。","bargaining":{"up":"上游是鋼、鋁、銅與進口零組件，Section 232 關稅 50% 主要壓在 Krausz 修理產品與 Specialty Valve 線；供應商集中度事實表未涵蓋。","down":"兩大經銷商占毛銷售 37%，最大一家 20%，非獨家且無長期合約；目前錢仍留在製造端，FY26 調整後 EBITDA margin 25.2%。","geo":"以色列 Ariel 廠與中國荊門廠是關稅與地緣的單點，國內鑄造投資是對策。"},"profit_pool_dir":"事實表未涵蓋","tam_table":{"expanded":false,"reason":"事實表沒有 TAM、滲透率與利潤池資料；核心產品是置換需求，滲透率不是主要成長變數。"}},"moat":{"mechanism":"市政規格與用戶品牌習慣，加上鐵閘閥與消防栓的少數競爭者結構，經由區域與全國水務經銷商觸達。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：調整後 EBITDA margin 三年多 940 基點。定價面穩定：FY26 漲價仍帶動營收，但 2026-11-05 Morgan 說 FY27 價格成本金額為正、利潤率持平，比 2026-08-06 Rasmussen 說的價格成本為正保守。份額資料事實表未涵蓋；銷量下滑可由新建住宅與消防栓基期解釋，目前沒有證據指向份額流失，也沒有證據能排除。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改以營益率與毛利率比較方向。","threats":[{"level":"🟡","text":"進口與北美以外對手：競爭強度隨匯率、運費與貿易救濟波動，目前關稅反而提供保護，關稅退場或運費下降時保護會消失。","p":"20%","evidence_refs":["competitive_share_entrants#1","substitute_technology#2"]},{"level":"🟡","text":"新漲價若未獲兩家主要對手跟進，定價紀律會鬆動；對手定價資料事實表未涵蓋。","p":"25%","evidence_refs":[]},{"level":"🟡","text":"退出計量後公司不再掌握用水數據端，只留漏水偵測；若水務客戶改以計量平台整合採購，硬體綁定會鬆動。事實表沒有這種轉向的證據，只列觀察。","p":"10%","evidence_refs":["major_events#0"]}],"roic_durability":{"quadrant":"高利益率，周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是水務單位與承包商，決策者是市政工程人員，付款者是市政預算與水費。維修汰換是需要不是想要，可以延後但不會消失；六成以上營收屬此類（2026-06-30 10-Q）。"},{"item":"決策層級","level":"🟡","text":"替代性要看市政規格這一層，10-K 稱終端用戶不易換品牌，但這是公司自述。漲價後流失率、規格變更次數事實表未涵蓋，而銷量正在下滑，因此不給綠燈。"},{"item":"價值鏈分配","level":"🟡","text":"下游兩大經銷商占 37% 且無長期合約，上游承受關稅；目前製造端拿到的份額處於高點，FY27 價格成本對利潤率已轉持平，再多拿的空間變小。"},{"item":"社會容忍度","level":"🟡","text":"客戶是受預算與水費約束的市政單位，公司連年靠漲價成長，2026-11-05 法說已提到市政因通膨壓力採購謹慎；公司本身不受費率監管，但實際定價上限受市政預算限制。"}],"roiic":"無法計算：投入資本與營運資金變動事實表未涵蓋。FY23 到 FY26 稅前營業利益增加約 1.53 億，主要來自利潤率修復，不是新投入資本的報酬，不能當增量報酬。","reinvest_rate":"約 6%（不含營運資金與收購）","endo_ceiling":null,"formula_note":"再投資率＝（FY27 資本支出中位 65－折舊攤銷中位 50）÷稅後營業利益（（EBITDA 中位 383－50）×75%≈250）＝15÷250＝6%，單位百萬美元。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","MWA":38.24,"WTS":48.87,"XYL":39.79,"ZWS":50.41,"BMI":41.64,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","MWA":21.54,"WTS":19.73,"XYL":16.06,"ZWS":22.52,"BMI":18.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","MWA":10.07,"WTS":11.55,"XYL":10.17,"ZWS":21.19,"BMI":16.16,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","MWA":null,"WTS":null,"XYL":2.55,"ZWS":null,"BMI":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"WTS","gm":48.87,"om":19.73,"fcf_margin":11.55,"rd_intensity":null,"strategy_note":"毛利率高出約 10 個百分點，產品偏建築與工業，是 specialty valves 轉向工業時可參考的組合。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"XYL","gm":39.79,"om":16.06,"fcf_margin":10.17,"rd_intensity":2.55,"strategy_note":"營益率較低、有研發揭露，走的是技術與數據路線，正是公司退出計量後不再競爭的方向。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ZWS","gm":50.41,"om":22.52,"fcf_margin":21.19,"rd_intensity":null,"strategy_note":"毛利率與 FCF 利潤率都更高，代表水處理產品組合能到的上限，公司靠工廠效率追近營益率但毛利差距仍大。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"BMI","gm":41.64,"om":18.76,"fcf_margin":16.16,"rd_intensity":null,"strategy_note":"計量專業廠，毛利率高於公司，對照公司計量業務銷售萎縮且 EBITDA 為負，說明這塊規模不足。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"FY26 為價格正、量負；FY27 指引價格低至中個位數，量在排除消防栓基期後持平；EPS 成長主要靠利潤率、計量退出與回購。","runway_years":"不適用：置換型需求沒有滲透率概念，滲透率資料事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界無法算出，投入資本事實表未涵蓋。再投資率約 6%，共識由乾淨基期 1.48 到 1.59 的 +7.4% 明顯高於這個再投資率能支撐的水準，按超出處理，缺口歸因利潤率擴張與回購。","segments":[{"item":"Water Flow Solutions","value":"FY26 銷售 8.175 億（年減 0.9%），調整後 EBITDA margin 33.0%；FY27 指引低至中個位數成長，margin 小幅上升（排除關稅退款）。"},{"item":"Water Management Solutions","value":"FY26 銷售 6.575 億（年增 8.7%），margin 24.6%；FY27 指引高個位數下滑（計量退出與消防栓基期），margin 明顯擴張。"}],"decay_signals":["亮：主力產品提價後銷量下滑——FY26 與 Q4 都是價格抵銷銷量，鐵閘閥與 service brass 銷量下滑，部分來自新建住宅。","亮：EPS 成長遠高於營收成長——FY23 到 FY25 稀釋 EPS 年複合約 49%，營收約 5.9%（事實表 financial_history）。","未亮：毛利率連 2 季年減——Q3 排除一次性 +30 基點，Q4 −100 基點，目前只有一季，FY27 第一季決定是否亮起。","未亮：FCF／淨利連 2 年低於 0.75——FY25 約 0.90，FY26 為調整後淨利 84%。","未亮：SBC 占營收超過 5%——FY26 約 0.93%。","未亮：維護性資本支出占 FCF 超過 60%——維護性金額未揭露，總資本支出僅占 FCF 約 27%。","未亮：停止投資新產能——FY27 資本支出升到 6,000–7,000 萬，投入鑄造廠。","資料缺口：核心市占近 12 個月變化，事實表未涵蓋。","資料缺口：TAM 是否萎縮，事實表未涵蓋；目前沒有替代技術證據。","資料缺口：產業倍數近 3 年是否系統性下移，事實表未涵蓋。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐；三年現金去向與回購均價事實表未涵蓋，無法展開成完整表格。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"完整併購帳事實表未涵蓋；可驗證的部分為負：計量銷售近 4–5 年年減約 10%、EBITDA 為負，退出還要付約 2,600 萬，i2O 北美以外業務也已出售。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購均價與十年期公債殖利率事實表未涵蓋，無法判定；以現價計 FY27 盈餘殖利率約 6.6%（1.59÷24.05）。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY26 SBC 1,370 萬÷市值約 37.4 億＝0.37%，低於 1.5%；以金額換算，不是實際股數變動。","grade":"過"}]},"valuation":{"basis":"以 FY27 共識 EPS 1.59 為前瞻分母，現價對應 15.13 倍；起點改用扣除 0.09 一次性後的 FY26 實績 1.48，對應 16.25 倍。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比，無法做倍數對照。"},"peg":2.04,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY27 本益比 15.13 倍，PEG 約 2.0（15.13÷7.43），FY27 EV/EBITDA 約 9.5 倍，FCF 殖利率約 5.5%，基準年化約 8%，屬合理區間。五年分位事實表未涵蓋，只有四個年度端點：本益比分位 0、P/S 分位 81，兩者方向相反，不能只用本益比主張便宜。四週漲幅事實表未涵蓋。","upside_short_pct":5.8,"upside_mid_pct":21.7},"trap_analysis":{"verdict":"🟡","label":"利潤率高點、量縮靠價"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2026-11-05 法說：Q4 排除一次性項目後毛利率年減 100 基點；SG&A 年減 940 萬美元，主因之一是激勵獎金下降，金額大於調整後 EBITDA 約 370 萬的增幅；FY27 價格成本對利潤率持平，指引卻要擴張 110 基點。","assumption":"FY27 的 26.3% 是可維持的新基準。","consequence":"價格留不住時 margin 回到 FY25 的約 23%，Bear EPS 1.33 到 1.41，乘 11 到 12 倍股價約 15 到 17 美元，虧 30–39%。五年虧 50% 的路徑是 margin 20%、EPS 約 1.18、10 倍本益比，股價約 11.8 美元。","ruling":"採納為 Bear，機率 30%。它和唯一致命點同源，五年虧 50% 的故事就是漲價失敗後利潤率回吐，兩者對帳一致。不納入 Base，因為製造改善與計量退出（約 800 萬 EBITDA）不靠價格。","watch":"FY27 Q1 與 Q2 調整後毛利率年變化、價格實現與 SG&A 金額。","evidence_refs":["reg_tariff_export#5","end_markets#0"],"fact_refs":["f_kpi1_adjusted_operating_margi"]},{"view":"論點失敗","evidence":"2026-08-06 法說的財務長是 Melissa Rasmussen，2026-11-05 改由 10-28 到職的 Mike Morgan 發言，約 11-19 接任，離任原因事實表未涵蓋。同一場首度把尚未公告的漲價放進指引，RBC 當場指出與過去做法不同。","assumption":"指引編製紀律與調整項定義不變。","consequence":"新任財務長可能重設調整項或基期，FY27 指引的可信度低於過去三次上調時的水準。","ruling":"部分採納：不改 Base，但把財務長交接列入風險，FY27 Q1 是第一個檢查點。","watch":"FY26 10-K 的調整項定義、FY27 Q1 指引是否維持、中期目標發布時間。","evidence_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"FY26 底現金 5.66 億、流動性 7.31 億，法說提到尋求現有與相鄰市場併購；同一時間公司正在退出 i2O 與計量，計量銷售 4–5 年年減約 10%、EBITDA 為負，退出要付約 2,600 萬，且保留既有硬體合約與保固義務。RBC 問有沒有對價與後續負債，CEO 沒有正面回答。","assumption":"margin 與現金流達標後，現金會用在報酬高於資金成本的地方。","consequence":"一筆 5 億美元、稅後報酬 4% 的併購，相比同額回購（盈餘殖利率約 6.6%）每年少約 1,300 萬獲利，約每股 0.09，是 Base FY31 EPS 的 4%。","ruling":"部分採納：不改 Base，併購列為行動條件；單筆超過 3 億美元且未揭露報酬目標時停止加碼。","watch":"併購金額與揭露的投資報酬，回購實際金額對 3 億授權的比例。","evidence_refs":["major_events#0","ma_merger#0"]},{"view":"價格已反映太多","evidence":"本益比 17.06 是四個年度端點的最低，但 P/S 2.54 在 81 百分位，EV/S 2.46 在 71 百分位。股價已為更高的利潤率付錢，只是獲利長得更快。基準情境年化約 8%。","assumption":"本益比在低檔代表便宜。","consequence":"以銷售倍數衡量，現價已反映大部分利潤率修復，要有超額報酬必須 margin 繼續上升；10% 年化需要 FY31 EPS 約 2.28，對應 margin 近 30%。","ruling":"採納：不主張便宜，估值結論為合理。","watch":"新任財務長預告的中期利潤率目標，及 FY27 全年 margin 是否達 26.3%。","evidence_refs":[],"fact_refs":["f_pe_percentile","f_ps_percentile","f_ev_s_percentile"]}],"max_dd":{"lo":-42,"hi":-28,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 25.31 → 本次 24.05（-5.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=25.31","side_b":"本次 price_at_dd=24.05","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 25.31 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 25.31 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 25.31 美元：Bull 價 49.97、Bear 價 16.92，五年期望值 +25.3%，基準年化 5.6%，不對稱比 1.96","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.96。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 25.31 美元：五年期望值 +25.3%，基準年化 5.6%，不對稱比 1.96","side_b":"本次情境、股價 24.05 美元：五年期望值 +31.9%，基準年化 6.7%，不對稱比 2.42","ruling":"再換股價、情境不動：起點價下跌 5.0%，五年期望值多 6.6 個百分點，基準年化多 1.1 個百分點，不對稱比由 1.96 升到 2.42。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訊號與陷阱判斷下修","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份給偏正面訊號、陷阱風險低，依據包括 FY27 營收 ≥15.5 億、EBITDA ≥3.9 億。","side_b":"FY27 指引營收 14.4–14.7 億（不含約 4,000 萬計量），EBITDA 3.78–3.88 億，兩者都低於前份門檻；銷量下滑，價格成本對利潤率轉持平。","ruling":"採新證據：訊號降一級，陷阱風險由低升到中。方向相反，以公司正式指引為準。","evidence_level":"一手：2026-11-04 新聞稿與 2026-11-05 法說","settle_metric":"FY27 排除計量營收與調整後 EBITDA","if_then":["若 FY27 第二季價格實現達低個位數以上且銷量持平，訊號回升一級","若連 2 季調整後毛利率年減 ≥100 基點，減碼一半"],"evidence_refs":["end_markets#0"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 25.31，結論為合理。","side_b":"現價 24.05，較前份低約 5%，結論仍為合理。","ruling":"價格變動幅度不足以改變結論；FY27 獲利預期也未上升。","evidence_level":"事實表價格與共識","settle_metric":"FY27 本益比","if_then":["若 FY27 第二季驗證達標，且股價仍在 15 倍附近，可建小量首倉","若股價先漲過 28 美元而價格證據未到，不追"]},{"axis":"前份未填欄位補上","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","p_bull_pct","p_bear_pct","max_dd_pct","archetype","cycle_position"],"side_a":"前份這些欄位皆未填。","side_b":"本次補上：護城河持平、成長後勁中等、情境機率 20／50／30、最大回撤 −28% 到 −42%、公司類型為穩定內需；非循環股不填景氣位置，裁決與角色由程式產生。","ruling":"屬格式改版後的新增判斷，不代表基本面變化。","evidence_level":"方法說明"},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":null,"side_a":"前份未設唯一致命點（null）。","side_b":"FY27 第二季那次尚未公告的年度漲價，公告與留存是否達到全年低個位數以上的價格實現。","ruling":"Single Thing 依數學上最大的單一敏感度選定，價格每 1 個百分點約影響 FY27 EPS 4.4%，大於失去單一經銷商的直接可估影響。","evidence_level":"2026-11-05 法說與本次試算","settle_metric":"FY27 全年價格實現"},{"axis":"清倉與減碼門檻、重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份 kill_metrics 與重新進場條件皆未設（null）。","side_b":"減碼：連 2 季調整後毛利率年減 ≥100 基點，或 TTM 調整後 EBITDA margin 低於 24%。清倉：TTM margin 低於 23% 且價格實現低於低個位數。重新進場：第二季確認價格實現達低個位數以上且排除基期後銷量不低於持平。","ruling":"舊版沒有這些欄位，本次新設，門檻綁定價格與利潤率這個最大敏感度。","evidence_level":"方法說明與本次試算","settle_metric":"季度毛利率、EBITDA margin、價格實現"},{"axis":"舊風險門檻調整（減碼條件）","cause":"新證據","prior_field":null,"side_a":"連 2 季 GM < 34% 或 adj EBITDA margin < 23%；reauthorization < 50% 原規模 或 sales 連 2 季 < 0%；主要市佔指標 -3pp 或 management 法說承認 losing market share。","side_b":"連 2 季調整後毛利率年減 ≥100 基點或 TTM margin 低於 24% 時減碼；排除計量後營收連 2 季年減；主要份額指標 −3 個百分點或管理層承認份額流失（份額為資料缺口）。","ruling":"Q4 毛利率 37.0%、margin 25.4%，舊門檻太鬆。聯邦法案結果事實表未涵蓋，2026-08-06 McAndrew 稱聯邦占市政投資不到 5%、未來 1–3 年無重大變化，不再作為減碼條件，仍保留監測。銷售門檻改排除計量口徑，避免機械誤觸。","evidence_level":"一手：法說與新聞稿；聯邦法案為資料缺口","settle_metric":"季度調整後毛利率、排除計量營收","if_then":["若連 2 季調整後毛利率年減 ≥100 基點，減碼一半","若聯邦資金變動使 FY27 指引下修，停止加碼"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"舊論點門檻失效","cause":"新證據","prior_field":null,"side_a":"FY27 sales ≥ $1.55B；FY27 adj EBITDA ≥ $390M；EchoShore subscription 年化 > $100M；FY27 末 trailing PE ≥ 20x。","side_b":"FY27 排除計量營收 ≥14.4 億、EBITDA margin ≥26.0%；specialty valves 持續雙位數成長；倍數不再列為假設。","ruling":"FY27 指引中位加回約 4,000 萬計量後約 14.95 億，仍低於 15.5 億；EBITDA 指引上緣 3.88 億也低於 3.9 億。公司退出計量，智慧水務占比擴大的說法失去依據，門檻全部重設。","evidence_level":"一手：2026-11-04 新聞稿","settle_metric":"FY27 全年營收與 margin"},{"axis":"市政需求說法不一致","cause":null,"side_a":"2026-11-04 新聞稿：Municipal repair and replacement demand remains resilient；2026-08-06 Rasmussen 同樣說具韌性。","side_b":"2026-11-05 McAndrew 在 FY27 展望中提到市政單位 cautious purchasing behavior，且因通膨壓力預算謹慎。","ruling":"可調和，屬程度差異：需求還在，採購時點往後，Base 採排除基期後銷量持平，不採復甦。","evidence_level":"一手：新聞稿與法說","settle_metric":"排除消防栓基期後銷量","if_then":["若連 2 季銷量年減，減碼一半","若連 2 季銷量年增，維持持有並解除停止加碼"]},{"axis":"利潤率結構性或階段性","cause":null,"side_a":"McAndrew：三年 940 基點，FY27 中位達四年 1,150 基點；Morgan：營運系統才剛上軌道，還有空間。","side_b":"Q4 排除一次性毛利率年減 100 基點，SG&A 下降含獎金減少；FY26 含關稅退款；2026-08-06 Rasmussen 說價格成本為正，2026-11-05 Morgan 改口金額為正、利潤率持平。","ruling":"部分結構、部分階段性。Base 取 26–27.5%，不給 30%；管理層把獎金與關稅退款歸入成果的部分未證實，以 FY27 兩季數據檢驗。","evidence_level":"一手法說，獎金金額未揭露","settle_metric":"FY27 Q1、Q2 調整後毛利率與 SG&A 金額","if_then":["若股價先漲過 28 美元（約 17.6 倍 FY27 獲利）而價格證據未到，不追","若股價下跌而第二季價格實現達標，分批反買","若 FY27 全年 margin 達 26.3% 且毛利率年增，Base 上調到 28%"]},{"axis":"第二曲線規模不透明","cause":null,"side_a":"McAndrew：specialty valves 雙位數成長、占積壓訂單多數，資料中心為成長最快之一。","side_b":"2026-08-06 問資料中心規模只答 relatively small，問消防栓更新系統的營收貢獻未答；2026-11-05 問中期利潤率也未答。","ruling":"第二曲線最多支撐後勁中等，不支撐倍數提升；不可裁決至公司揭露占比。","evidence_level":"法說定性描述，無金額","settle_metric":"specialty valves 營收占比","if_then":["若揭露占比且連續兩年雙位數，成長後勁上調一級","若連續四季未揭露占比，維持中等且不給倍數溢價"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"淨現金約 1.12 億、FY27 EV/EBITDA 約 9.5 倍、FCF 殖利率約 5.5%，指引已含量縮，賣方目標價多在 28–31 美元。","side_b":"目標價多為 2026 年中以前；扣除一次性後 FY27 EPS 成長僅 7%，且全靠利潤率；關鍵漲價半年後才揭曉，新財務長尚未給中期框架。","ruling":"等到第二季的代價是可能少賺一段，可以接受，因為基準年化只有約 8%。結論卡在價格實現這個事件，不是股價。","evidence_level":"事實表與法說","settle_metric":"FY27 第二季價格實現","if_then":["若第二季達標，建小量首倉","若第二季未達標，不建倉"]},{"axis":"自由現金流資料不一致","cause":null,"side_a":"事實表同業對照的 TTM FCF 利潤率 10.07%。","side_b":"公司 FY26 FCF 2.073 億÷營收 14.75 億＝14.05%，前九個月 1.106 億加 Q4 0.967 億相符。","ruling":"採公司揭露數字，資料商的 TTM 應有期別或定義問題，同業比較中此欄不採用。","evidence_level":"一手：法說與新聞稿","settle_metric":"FY26 10-K 現金流量表"}],"triggers":[{"n":1,"text":"第二季漲價落地驗證","type":"Single Thing","maps_to":"Single Thing","metric":"FY27 全年價格實現（指引低至中個位數）","threshold":"第二季財報時全年價格實現低於低個位數，或公司撤回新漲價","action":"減碼一半，下一季仍未回升則清倉","source_freq":"季度新聞稿與法說","date":"2027-05"},{"n":2,"text":"毛利率連續下滑","type":"風險","maps_to":"R1","metric":"調整後毛利率年變化","threshold":"連 2 季年減 ≥100 基點，Q4 已出現一季","action":"減碼一半","source_freq":"季度新聞稿與法說","date":"2027-02","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#5","geo_supply_chain#0"]},{"n":3,"text":"銷量是否止跌","type":"假設驗證","maps_to":"H1","metric":"排除計量營收、排除消防栓基期後銷量","threshold":"FY27 排除計量營收 ≥14.4 億且銷量不低於持平","action":"未達標則停止加碼","source_freq":"季度新聞稿與法說","date":"2027-11","evidence_refs":["end_markets#0"]},{"n":4,"text":"全年利潤率達標","type":"假設驗證","maps_to":"H2","metric":"調整後 EBITDA margin","threshold":"FY27 ≥26.0%","action":"未達標則停止加碼","source_freq":"季度新聞稿與法說","date":"2027-11"},{"n":5,"text":"經銷商集中度上升","type":"風險","maps_to":"R3","metric":"兩大經銷商占毛銷售","threshold":"合計 ≥42% 或最大一家 ≥25%","action":"停止加碼","source_freq":"10-K，每年一次","date":"2026-11","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":6,"text":"進場條件成立","type":"估值rearm","maps_to":"H1","metric":"全年價格實現與排除基期後銷量","threshold":"第二季財報確認價格實現達低個位數以上，且銷量不低於持平","action":"建小量首倉，低於目標倉位三分之一","source_freq":"季度新聞稿與法說","date":"2027-05"},{"n":7,"text":"利潤率跌破減碼線","type":"減碼","maps_to":"R1","metric":"TTM 調整後 EBITDA margin","threshold":"低於 24%","action":"減碼一半","source_freq":"季度新聞稿","date":"2027-05"},{"n":8,"text":"利潤率回吐且定價失效","type":"清倉","maps_to":"H2","metric":"TTM 調整後 EBITDA margin 與價格實現","threshold":"TTM margin 低於 23% 且價格實現低於低個位數","action":"清倉","source_freq":"季度新聞稿與法說","date":"2027-11"},{"n":9,"text":"第二曲線與中期目標揭露","type":"加碼","maps_to":"H3","metric":"specialty valves 營收占比與中期 margin 目標","threshold":"揭露占比、中期目標 ≥28%，且 FY27 全年 margin ≥26.3%","action":"加碼至目標倉位","source_freq":"法說或投資人日","date":"2027-11"},{"n":10,"text":"計量退出費用超支","type":"風險","maps_to":"R5","metric":"計量退出總費用與時程","threshold":"總費用超過 3,100 萬美元，或轉移拖到 FY28 下半","action":"停止加碼","source_freq":"季度新聞稿與法說","date":"2027-11","evidence_refs":["major_events#0","ma_merger#0"]},{"n":11,"text":"份額與進口競爭","type":"風險","maps_to":"R4","metric":"主要份額指標與管理層說法","threshold":"份額下滑 3 個百分點或管理層承認流失（份額為資料缺口）","action":"減碼一半","source_freq":"法說、10-K","date":"2027-11","evidence_refs":["competitive_share_entrants#1","substitute_technology#2"]},{"n":12,"text":"全面複審","type":"複審日期","maps_to":"H1","metric":"第二季財報後重跑研究","threshold":"2027-05 財報發布後兩週內","action":"重跑本研究並更新情境","source_freq":"一次","date":"2027-05-15"}],"kill_metrics":[{"metric":"FY27 全年價格實現","bear_threshold":"低於低個位數，或撤回新漲價","window":"FY27 Q2 至 Q4","source":"季度新聞稿與法說","last_status":"unknown"},{"metric":"調整後毛利率年變化","bear_threshold":"連 2 季年減 ≥100 基點","window":"連續 2 季","source":"季度新聞稿與法說","last_status":"warning"},{"metric":"TTM 調整後 EBITDA margin","bear_threshold":"減碼低於 24%；清倉低於 23%","window":"每季","source":"季度新聞稿","last_status":"ok"},{"metric":"排除計量與消防栓基期後銷量","bear_threshold":"連 2 季年減","window":"連續 2 季","source":"季度新聞稿與法說","last_status":"unknown"},{"metric":"兩大經銷商占毛銷售","bear_threshold":"合計 ≥42% 或最大一家 ≥25%","window":"每年","source":"10-K","last_status":"ok"},{"metric":"計量退出總費用","bear_threshold":"超過 3,100 萬美元或拖到 FY28 下半","window":"FY27 全年","source":"季度新聞稿與法說","last_status":"unknown"}],"evidence_dismissed":[{"ref":"substitute_technology#1","reason":"這條是 10-K 通用風險條款，未指名任何對手、產品或金額，證據本身沒有可驗證的事實，也沒有說明 AI 如何影響鑄鐵閥門與消防栓這類產品。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-8.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='受監管公用/穩定內需', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"FY27 第二季財報確認全年價格實現達低個位數以上，且排除消防栓基期後銷量不低於持平","exec_line":"現價不追；已持有者續抱不加碼，等 FY27 第二季財報驗證漲價。股價先漲但證據未到不追；股價下跌而價格實現達標則分批反買。"},"reasoning":{"industry":"FY26 營收約 14.75 億美元，Water Flow Solutions 8.175 億（55%，年減 0.9%），Water Management Solutions 6.575 億（45%，年增 8.7%，含消防栓積壓訂單出清）。2026-11-05 法說明講全年是價格抵銷銷量下滑。Q4 營收 3.765 億年減 1.1%，毛利率 37.0%，調整後營益率 21.9%，GAAP 營益率 19.4%。終端約 60–65% 市政維修汰換、25–30% 新建住宅、約 10% 天然氣公用事業（2026-06-30 10-Q）。單點依賴是通路：兩大經銷商占毛銷售 37%，最大一家 20%，無長期合約（FY2025 10-K）。產業態勢屬雙向拉鋸：關稅與市政預算壓力，對上國內產能需求與 2027-11-01 起過渡的鉛管規則。可能看錯的地方：若銷量下滑其實是份額流失，置換需求穩定就保護不了利潤，份額資料事實表未涵蓋。","moat":"機制是市政工程規格與用戶習慣，加上寡占結構：FY2025 10-K 稱閥門市場成熟、終端用戶不易換品牌，鐵閘閥與消防栓主要對手只有 McWane 和 American Cast Iron Pipe。同業 ROIC 事實表未涵蓋，改看利潤率。TTM 營益率 21.54%，高於 WTS 19.73%、BMI 18.76%、XYL 16.06%，低於 ZWS 22.52%；毛利率 38.24% 卻是五家最低，代表優勢主要在費用率與工廠效率，不是產品溢價。同業產品組合不同，這個比較只能看方向。可能看錯的地方：若 FY27 新漲價未獲對手跟進，定價面要改判縮減，整體方向轉為向下。","growth":"FY26 營收年增 3.2% 全由價格帶動；FY27 指引排除計量後持平到 +2.5%，價格低至中個位數，排除約 2 個百分點的消防栓基期後銷量持平。共識只有兩年：Koyfin FY1 1.57、FY2 1.59，第三年事實表未涵蓋，三年共識複合成長無法算出。FY26 的 1.57 含 0.09 一次性，扣除後 1.48，到 FY27 的 1.59 是 +7.4%，未扣除只有 +1.3%。再投資率約 6%，要單靠再投資達到 7.4% 需要增量報酬超過 120%，不合理，所以缺口歸因利潤率擴張與回購，不是內生成長。Base 五年 EPS 年複合約 7.0%，約一半來自營收（含價格），其餘來自利潤率與股數減少。可能看錯的地方：specialty valves 若占比已高且持續雙位數，後勁會比這裡判的好，占比事實表未涵蓋。","governance":"FY26 自由現金流 2.073 億，為調整後淨利 84%；配發 7,400 萬，約占 36%；SBC 1,370 萬，占營收 0.93%。現金 5.66 億、債務 4.54 億，最近到期 2029 年 6 月，票息 4%。新增回購授權 3 億、季配息調升 14.3% 到 0.08。現金去向：資本支出 5,560 萬，配發 7,400 萬，併購金額事實表未涵蓋，其餘留在帳上。FCF 超預期主因是營運資金有利與資本支出低於 2026-08-06 重申的 6,000–6,500 萬，不能全算經營成果。可能看錯的地方：管理層若把 3 億授權用足，回購會比這裡假設的更有貢獻。","valuation":"要賺 10% 年化，扣掉約 1.3% 股息，股價年增需約 8.7%，FY31 目標約 36.5 美元；以 16 倍計需要 EPS 約 2.28，比 Base 的 2.08 高約 10%，換算 EBITDA margin 近 30%。2026-11-05 Bryan Blair 問中期利潤率是否 3 開頭，McAndrew 沒有回答。賣方目標價多在 28–31 美元、個別 25–34，多為 2026 年中以前，不能當支持。FY27 EV/EBITDA 約 9.5 倍（36.3 億÷3.83 億），FCF 殖利率約 5.5%。可能看錯的地方：淨現金加上 FCF 若全數回購，EPS 可高於 Base，倍數也可能回升。","premortem":"容易看錯的有三處：把高點利潤率當常態、把一次性好處當經營成果、把第二曲線當已證實。衰退信號十項亮兩項，主力產品提價後銷量下滑、EPS 成長遠高於營收成長，另有三項是資料缺口。若 FY27 價格達標且銷量止跌，第一項會熄掉，結論可上調。空方最強數字與歷史最大回撤事實表未涵蓋。訴訟方面，Cobb County 1,500 萬和解預期由第三方補償，資安集體訴訟上限 28.5 萬，都不構成主要風險。"},"plain":{"six":{"how_it_makes_money":"賺市政自來水系統更換老舊閥門與消防栓的錢，貨經由兩大經銷商出去，利潤留在北美寡占的規格與品牌這一節；現階段營收成長全靠漲價，銷量在降。","moat":"護城河持平：定價與規格黏性還在，營運改善擴大了利潤，但這不等於護城河變寬。","growth":"成長後勁中等：核心是成熟的置換市場，第二曲線 specialty valves 在長但規模未揭露，五年成長主要靠價格、利潤率與回購。","capital":"資本配置中等：資產負債表很強、稀釋很低，但現金累積快於配發，併購紀錄是要打折的部分。","valuation":"現價 24.05 約 15.1 倍 FY27 獲利，大致等於基準情境；要賺 10% 年化得把 margin 推到近 30%，目前不信。","how_wrong":"最可能看錯在把歷史最高的利潤率當常態，陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等 FY27 第二季財報（約 2027-05）確認年度漲價已落地，全年價格實現達低個位數以上，且排除消防栓基期後銷量不低於持平；這是事件條件，不設進場價。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"受監管公用/穩定內需","price_at_dd":24.05,"week26_return_pct":-8.31,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY1 共識 1.57 與 FY26 實際相同，且 90 天零修正，快照應未滾動，1.57 實為剛結束的 FY26。它含 0.09 一次性，扣除後 1.48。前瞻分母改用 FY27 的 1.59；但 1.59 建立在歷史最高的利潤率上，便宜的說法不成立。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"FY26 10-K 發布，Mike Morgan 約 11-19 接任財務長","impact":"中","watch":"調整項定義、經銷商占比、財務長交接說明"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第一季財報","impact":"高","watch":"調整後毛利率是否連 2 季年減 ≥100 基點，是否公告新漲價，計量退出費用進度"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 第二季財報","impact":"高","watch":"全年價格實現是否達低個位數以上，排除基期後銷量"},{"date":"2027-11","date_precision":"month","type":"regulatory","event":"鉛管規則改善版自 2027-11-01 起過渡，水務單位更新清冊與更換計畫","impact":"中","watch":"對市政維修汰換預算的實際帶動"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,735B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河持平，優勢在費用率與工廠效率，不在產品溢價。</p>
<ul class="pts">
<li>護城河的機制是市政工程規格與用戶品牌習慣，加上鐵閘閥與消防栓只有少數競爭者。FY2025 10-K 稱閥門市場成熟、終端用戶不易換品牌，主要對手只有 McWane 和 American Cast Iron Pipe。產品經由區域與全國水務經銷商觸達。這些都是公司自述，份額資料事實表未涵蓋，所以評等給 B，趨勢判為持平。</li>
<li>執行面分數 8，定價面分數 7，綜合 7.5。執行面來自三年 940 基點的 margin 擴張，定價面來自 FY26 漲價仍能帶動營收。但 2026-11-05 Morgan 說 FY27 價格成本金額為正、利潤率持平，比 2026-08-06 Rasmussen 說的價格成本為正更保守。定價面因此只能算穩定，不能算變強。</li>
<li>同業對照顯示優勢不在毛利。公司 TTM 營益率 21.54%，高於 WTS 的 19.73%、BMI 的 18.76%、XYL 的 16.06%，只低於 ZWS 的 22.52%。但毛利率 38.24% 是五家最低，ZWS 達 50.41%，WTS 達 48.87%。這代表公司靠的是費用率與工廠效率，不是產品溢價。同業產品組合不同，只能看方向。</li>
<li>自由現金流利潤率有資料不一致。資料商同業表給公司 10.07%，但公司揭露 FY26 FCF 2.073 億美元除以營收 14.75 億，是 14.05%，前九個月 1.106 億加 Q4 0.967 億相符。本報告採公司揭露數字，同業表這一欄不採用。</li>
<li>三個威脅都給黃燈。進口與北美以外對手的競爭強度隨匯率、運費與貿易救濟波動，目前關稅反而提供保護，機率 20%。新漲價若未獲兩家主要對手跟進，定價紀律會鬆動，機率 25%。退出計量後公司不再掌握用水數據端，若客戶改以計量平台整合採購，硬體綁定會鬆動，機率 10%。</li>
<li>報酬持續性方面，公司屬高利益率但周轉率未知的象限，投入資本事實表未涵蓋，增量報酬無法計算。FY23 到 FY26 稅前營業利益增加約 1.53 億美元，主要來自利潤率修復，不是新投入資本的報酬。再投資率約 6%，這是（資本支出中位 65 減折舊攤銷中位 50）除以稅後營業利益約 250，單位為百萬美元。</li>
<li>反方看法也要列出。若 FY27 新漲價未獲對手跟進，定價面要改判縮減，整體方向轉為向下。若銷量下滑其實是份額流失，置換需求穩定就保護不了利潤。目前沒有證據指向份額流失，也沒有證據能排除，所以監測條件設為份額下滑 3 個百分點或管理層承認流失。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```