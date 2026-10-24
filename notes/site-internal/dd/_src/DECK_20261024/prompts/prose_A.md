你是 stock-analyst v20 的**散文層（prose）agent**，標的 DECK（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：DECK　日期：2026-10-24　archetype：None　前份裁決：2026-07-06　進場｜衛星持倉　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1668B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（422B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（818B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1431B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（893B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（570B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（897B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2094B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4855B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2530B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1668           3732-5332      5 條（2–6 內）  
s3                  8000         422           5305-7578      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3142          8301-11858      5 條（2–6 內）  
s6                 11000         570          7301-10430      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         897           1822-2603      5 條（2–6 內）  
s10                 5000        2094           2034-2906      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2530           2000-2470      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4395B；至少需散文≈40.60KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45
−45%
−41%
−40%
−30%
−30
−25.28
−23%
−22.5%
−17%
−8%
0%
0
$0.24
$0.28
$0.5
$0.52
0.75
0.99
01
1
1%
$1
1.0
$1.0
1.05
1.08
1.2
$1.210
1.3%
1.3
1.4%
2
2%
2.57
2.66%
3
3%
03
3.5%
3.5
4
4%
04
$4.4
5%
5
05
5.4%
$5.472
$5.5
5.6
$5.7
$5.700
5.725
$5.86
5.91
6
6.0
06
6.1%
6.3%
6.70
6.7
6.9
7%
07
7
7.02
7.2
$7.36
7.4%
7.4
7.50
7.5
7.53
7.7%
7.73
8%
8
8.05
8.21
8.28%
8.3%
8.47
8.5
8.6
8.85
9%
9
9.34
9.6%
9.65
9.8
9.88
9.9
$10
10.0%
10
10%
10.45
10.49
10.5
11
11%
11.25
11.4
11.6%
12
12.3
12.3%
12.5%
12.5
13
13.6%
13.7
13.79%
13.8%
14
14.7%
15
16
17%
17.5%
18%
18.5%
18.7%
19.1
19.4
20%
20
20.22%
20.7%
20.73%
21%
21.5
21.5%
$22
22
22.5%
22.67%
22.8%
23
23%
23.2%
24%
24
24.9%
24.94%
25%
25
26
26.3%
28%
29.6%
30%
30
32.1%
35%
38.5
40
40%
42
43
43.2%
45
45%
46%
$48
49
$50
50%
50.3%
51.5%
52
53%
54%
55%
56%
$57
57.7%
57.8%
60
60.5%
$62
64.8%
64.82%
$67.5
67.5
$70
70%
70
70.6%
73.4
73.4%
77%
81.09
$81.09
86
90
$92
$93.65
$98.5
$98.68
99%
100
$100
100%
$102.88
$103.79
103.79
$104.69
104.69
$105
$113
$115
$120
120
$125
$138
$140.6
$146
150%
200
218.5
219.2
$234
250
$299.3
$325
$338
$444
$637
$641
$677.2
$786.4
$860.8
$861
2025
2026
2027
20261024
$1,481
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
{"meta":{"ticker":"DECK","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Deckers Outdoor Corporation"},"oneliner":"HOKA 成長從雙位數掉到 7%，全年營收指引再下修；但全價紀律讓剔除退款營業利益率仍有 23%。10.5 倍前瞻本益比加上一年約一成市值的回購，價格已計入停滯，還缺 HOKA 重新加速的證據","thesis":{"H":[{"id":"H1","text":"HOKA 在 2027 年新品週期（Bondi 10、Mach Pro、Fly Pace、Bondi Ultra X）之後回到高個位數成長，並守住 $120 以上價帶的份額","2y":"FY2028 HOKA 年增 ≥8%","5y":"FY2028–FY2032 HOKA 年複合成長 ≥7%","10y":null,"threshold":"HOKA 季度營收年增 ≥8%；Q3 FY27 管理層已預告低至中個位數，該季門檻放寬為 ≥3%","source":"公司季報新聞稿的品牌營收；法說中管理層引用的 Circana 份額說法","drift_rule":"連 2 季 <8% 為削弱；連 3 季 <5% 為反轉"},{"id":"H2","text":"UGG 品牌熱度維持，休閒鞋、木屐、服飾等延伸品類抵銷經典靴的成熟化，營收維持正成長","2y":"FY2028 UGG 年增 ≥0%","5y":"UGG 五年營收不低於 FY2026 水準","10y":null,"threshold":"UGG 季度營收年增 ≥0%；冬季季度（Q3）不年減","source":"公司季報新聞稿","drift_rule":"單季年減為削弱；連 2 季年減 ≥5% 為反轉"},{"id":"H3","text":"全價紀律守住利潤率，自由現金流約八成用於回購；即使營收只成長中個位數，每股盈餘仍能維持高個位數成長","2y":"FY2028 剔除退款營業利益率 ≥21%","5y":"五年流通股淨減 ≥25%，剔除退款營業利益率 ≥20%","10y":null,"threshold":"剔除退款毛利率 ≥56%、營業利益率 ≥21%；年度回購 ≥ 自由現金流 70%","source":"法說中 CFO 的毛利率拆解；新聞稿中的回購金額","drift_rule":"剔除退款毛利率連 2 季 <56% 為削弱；年度營業利益率 <20% 為反轉"}],"R":[{"id":"R1","text":"HOKA 品牌熱度退潮：緩衝技術被複製、On 持續拿份額、Nike 跑鞋回歸，份額流失從 $120 以下延伸到高價段","h_ref":"H1","clock":"🔥","threshold":"HOKA 連 2 季年增 <5%，或管理層不再宣稱 $120 以上份額成長","evidence_refs":["substitute_technology#2","competitive_share_entrants#0","substitute_technology#0"]},{"id":"R2","text":"美國促銷環境拉長，加上成長改靠批發與 $115 的低價款，全價銷售與毛利率被侵蝕","h_ref":"H3","clock":"🔥","threshold":"剔除退款毛利率連 2 季年減","evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#1"]},{"id":"R3","text":"關稅再升級：成品主要在越南、印尼生產，關稅假設已從 10% 升到 12.5%，毛利率下滑主因就是關稅；IEEPA 退款是一次性的，明年同期基期被墊高","h_ref":"H3","clock":"🐢","threshold":"關稅假設 >12.5%，或剔除退款毛利率 <55%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","supply_demand_durability#3","geo_supply_chain#0"]},{"id":"R4","text":"UGG 冬季旺季不如預期：消費者延後到需要時才買，去年天氣帶動的補單今年不會再有","h_ref":"H2","clock":"⚡","threshold":"Q3 FY27 UGG 年減","evidence_refs":[]},{"id":"R5","text":"歐洲第三方物流問題不是一次性：約 $22M 的出貨延遲，部分可能被取消","h_ref":"H1","clock":"⚡","threshold":"下一季再揭露履約延遲","evidence_refs":[]}],"single_thing":{"description":"2027 年 5 月的 FY2028 財測給出 HOKA 全年成長 ≤ 中個位數，也就是 2027 年 1 月 Bondi 10、Fly Pace 上市後，HOKA 仍沒回到高個位數","why_fatal":"HOKA 是唯一的成長引擎，UGG 已經降到低個位數。HOKA 若只剩中個位數，合併營收成長約 3%，EPS 只能靠回購撐，合理倍數從 12–13 倍降到 9–10 倍，情境終點會從 Base 走向 Bear","if_happens":"減碼一半，H1 改判反轉；若 UGG 冬季同時年減，清倉","how_monitor":"Q3 FY27 法說（2027 年 1 月底）的 HOKA 成長與第四財季指引；Bondi 10 上市後的批發補單；2027 年 5 月的 FY2028 財測","probability":"35%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":9.88,"peg_fy2":0.99,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2026A":7.02,"FY2027E":7.73,"FY2028E":8.21,"FY2029E":9.34},"fy_end_month":3,"eps_basis":"GAAP 稀釋 EPS，財年截至 3 月；FY2027E 共識含部分 IEEPA 關稅退款一次性，FY2028E 要對比被退款墊高的基期"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DECK_20261024/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高毛利品牌鞋業，外包製造，自由現金流約八成用於回購，放大每股盈餘"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性壓力、預期反轉：美國運動鞋通路庫存偏高、促銷加劇，消費者集中在促銷檔期購買（2026-10-22 法說 CFO 與 CEO）；國際需求仍強","bargaining":{"up":"代工集中在越南、印尼，代工廠分攤關稅成本（退款按分攤比例扣除後才入帳），品牌對代工有議價權","down":"沒有單一客戶占營收 10% 以上，但單一客戶占應收 18.5% 且無擔保；批發占比上升，零售夥伴的促銷會外溢到品牌自營電商","geo":"成品主要在越南、印尼生產，中國或其他單一國家低於 5%；UGG 羊皮由中國兩家製革廠加工"},"profit_pool_dir":"高價段（$120 以上）利潤池往有創新的品牌集中，HOKA 在這段持續拿份額；$120 以下價帶競爭加劇，HOKA 可能流失（2026-10-22 法說 CEO）","tam_table":{"expanded":false,"reason":"證據包沒有 TAM、滲透率與利潤池占比；HOKA 份額只有管理層引 Circana 的質性說法（$120 以上價帶居首），沒有可展開的數字"}},"moat":{"mechanism":"品牌溢價加全價紀律：控制配銷與上市節奏（如 Bondi 換代前先清乾淨舊款），不參與促銷；外包製造讓資本報酬維持高檔","execution":7,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力縮減：2026 年部分新款反應不佳，HOKA 成長從雙位數降到 7%，Q3 預告只剩低至中個位數。定價力穩定：促銷環境下剔除退款毛利率仍年增 120bp，$120 以上價帶份額持續增加（2026-10-22 法說）。兩者互抵","peer_na_reason":"證據包沒有同業 ROIC 與投入資本，只有利潤率；改以營業利益率差距當可比軸","threats":[{"level":"🟡","text":"HOKA 被複製：緩衝技術已被同業跟進，On 持續拿份額，Nike 跑鞋回歸；資源更大的對手能更快開發產品，也更能運用資料分析與 AI。這是點對點的品牌競爭，不是生態替代","p":"35%","evidence_refs":["substitute_technology#2","competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"促銷壓力：公司在 10-K 自述已經歷、也預期持續面臨定價與促銷壓力；美國運動鞋通路庫存偏高","p":"50%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"UGG 原料集中：羊皮主要來自澳洲，由中國兩家製革廠加工；替代材料不帶相同商標","p":"10%","evidence_refs":["geo_supply_chain#1"]},{"level":"🟡","text":"Quince 提起反壟斷訴訟，挑戰 UGG 的外觀設計權。2026 年 8 月下旬遭法院駁回，但准許修正後再提；若最終勝訴，UGG 經典款防堵仿品的能力會變弱","p":"10%","evidence_refs":["regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是消費者本人，三個角色一致。但這是可以延後的非必需品：2026-10-22 法說指出消費者改成需要時才買，並集中在促銷檔期，購買急迫性下降。跑鞋與冬靴的需求本身是持久的"},{"item":"決策層級","level":"🟡","text":"替代發生在每一雙鞋的購買決策上，轉換成本接近零，品牌偏好是唯一的黏著力。HOKA 在 $120 以上價帶持續拿份額，但 $120 以下可能流失（2026-10-22 法說 CEO）"},{"item":"價值鏈分配","level":"🟢","text":"品牌端拿走大部分價值：TTM 毛利率 57.8%，Nike 是 43.2%；代工廠還分攤了關稅成本。議價缺口有兩個：批發占比上升，以及 UGG 羊皮集中在兩家製革廠"},{"item":"社會容忍度","level":"🟢","text":"屬非必需品，也不依賴監管授權，漲價沒有社會面的上限；政策風險在關稅（越南、印尼生產），不在價格管制"}],"roiic":"無法計算：投入資本與歷年增量投入，證據包都沒有","reinvest_rate":"約 0% 或為負：TTM FCF 利潤率 20.22% 高於稅後營業利益率約 17.5%","endo_ceiling":null,"formula_note":"內生成長＝增量 ROIC × 再投資率。再投資率接近零，公式算出的上限也接近零。品牌鞋業的成長投入（行銷、產品開發、門市）多半費用化，公式會低估實際成長能力；本檔改用實際營收成長加回購來拆解每股成長"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","DECK":57.8,"ONON":64.82,"NKE":43.16,"BIRK":56.86,"CROX":57.47,"unit":"%"},{"metric":"營業利益率","DECK":22.67,"ONON":13.79,"NKE":8.28,"BIRK":24.94,"CROX":20.73,"unit":"%"},{"metric":"FCF 利潤率","DECK":20.22,"ONON":13.32,"NKE":6.25,"BIRK":12.86,"CROX":17.38,"unit":"%"}],"competitors":[{"name":"ONON","gm":64.82,"om":13.79,"fcf_margin":13.32,"strategy_note":"毛利率 64.8% 高於 DECK，但營業利益率只有 13.8%；Bernstein 稱它持續拿份額，是 HOKA 高價跑鞋最直接的對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"NKE","gm":43.16,"om":8.28,"fcf_margin":6.25,"strategy_note":"毛利率 43.2%、營業利益率 8.3%，遠低於 DECK；Bernstein 認為它在跑鞋的回歸是 HOKA 的威脅","period":"TTM ending 2026-08-31（4季加總）"},{"name":"BIRK","gm":56.86,"om":24.94,"fcf_margin":12.86,"strategy_note":"營業利益率 24.9%，略高於 DECK；同樣靠品牌稀缺與全價策略，適合當 UGG 的利潤率對照","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CROX","gm":57.47,"om":20.73,"fcf_margin":17.38,"strategy_note":"營業利益率 20.7%，略低於 DECK；同樣從單一招牌鞋款擴到多品類，可對照 UGG 的延伸路徑","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（HOKA 擴大鋪貨、國際市場）為主，價格（全價銷售、選擇性漲價）為輔；每股層面靠回購；沒有併購","runway_years":"證據包沒有滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"再投資率接近零（TTM FCF 利潤率 20.22% 高於稅後營業利益率約 17.5%），公式上限接近零；共識約 10% 的每股成長主要靠淨回購（年約 8–10% 市值）補足","segments":[{"item":"HOKA Q2 FY27","value":"$677.2M，年增 7%；批發 +9%（$444M），直營 +4%（$234M）；美國直營受促銷拖累"},{"item":"UGG Q2 FY27","value":"$786.4M，年增 4%；批發 +7%（$641M），直營 −8%（$146M）；Q2 以進貨為主，旺季在 Q3"},{"item":"其他品牌","value":"Q2 年減 54%，主因 Koolaburra 收尾的基期效應"},{"item":"FY27 全年指引","value":"HOKA 高個位數、UGG 低個位數；Q3 HOKA 低至中個位數、UGG 低個位數"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q1 年增 60bp；Q2 剔除退款年增 120bp"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"CEO 稱 $120 以下價帶可能流失份額（2026-10-22）"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"2025 年 7 月起選擇性漲價，管理層稱沒看到明顯的銷量下滑"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"FY2023–FY2026 EPS 年複合約 29.6%，營收約 14.7%"},{"signal":"FCF 對淨利低於 0.75","lit":false,"evidence":"約 1.08 倍"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":null,"evidence":"證據包沒有 SBC 資料"},{"signal":"TAM 萎縮或被替代","lit":false,"evidence":"只有 Bernstein 單一賣方稱休閒品類萎縮，沒有量化證據"},{"signal":"產業估值倍數下移","lit":null,"evidence":"證據包沒有同業倍數歷史"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購（近 12 個月沒有併購公告）；資本回饋以回購為主，金額與均價已寫在現金配置的判讀裡"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 唯一的重大項目是信貸協議修訂，沒有併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q1 均價 $103.79、Q2 均價 $93.65，用 FY1 共識 EPS 7.73 換算，買入收益率約 7.4%–8.3%。十年期公債殖利率證據包沒有：只要殖利率低於約 5.4% 就算通過，本判定以此為前提","grade":"過"},{"year":"—","action":"sbc_dilution","rationale":"證據包沒有 SBC 金額。回購讓流通股半年減少約 5%，淨股數在下降，但算不出毛稀釋率","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY1 與 FY2）；PEG 用 FY2026A 到 FY2029E 的三年共識 EPS 年複合成長","tier":"高利潤品牌鞋業","peers":{"expanded":false,"reason":"證據包的同業只有利潤率、沒有本益比，做不了倍數對照；終端倍數改用公司自身 2026 年 7 月約 14 倍當對照，同業倍數的缺口已在情境假設中註明"},"fwd_pe":10.49,"peg":1.05,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"FY1 前瞻本益比 10.5 倍，剔除一次性退款約 11 倍，FY2 口徑 9.9 倍；三年共識 EPS 年複合約 10%，PEG 約 1.0。比 7 月時約 14 倍再壓縮約四分之一，判便宜。五年估值分位證據包沒有，未納入","upside_short_pct":21.5,"upside_mid_pct":73.4},"trap_analysis":{"verdict":"🟡","label":"成長減速型：利潤率與現金流沒壞，衰退訊號亮兩個"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Bernstein 稱 HOKA 緩衝技術已被複製、零售商對這波趨勢疲乏、On 持續拿份額、Nike 跑鞋回歸；2026-10-22 CEO 也承認 Transport、Kawana、Solimar 等新款沒打中","assumption":"HOKA 的高價跑鞋地位是可以持續的品牌優勢，不是一輪潮流","consequence":"五年後 HOKA 停滯、UGG 隨流行退燒，促銷把營業利益率壓到 15–17%；EPS 回到約 $5.5，給 9 倍，股價約 $50（−40%）","ruling":"部分採納：已反映在 Bear 30% 的機率與唯一致命點（兩者部分重疊）。不全採的理由：Bernstein 的觀點早於 FY26 Q3 HOKA +18% 的那一季；管理層引 Circana 稱 $120 以上份額仍在增加；Q2 全價銷售還讓毛利率上升","watch":"HOKA 季度成長、$120 以上份額說法、新品全價售出率","evidence_refs":["competitive_share_entrants#3","substitute_technology#2"],"fact_refs":["f_kpi7"]},{"view":"論點成功但股東經濟變差","evidence":"公司長期目標是提高直營占比，但為了擴大份額持續擴張批發（FY26 批發 +12.3%，快於直營 +6.3%）；HOKA 推出 $115 的入門款並擴大運動用品通路。上半年回購均價 $93.65–103.79，高於現價","assumption":"HOKA 回到成長的同時，不稀釋品牌、不犧牲毛利率","consequence":"營收成長回來，但靠的是批發與低價帶，毛利率回落 100–200bp，每股盈餘成長低於營收成長；高價買進的回購，實際創造的每股價值也低於回購金額","ruling":"列為監測項：Q2 批發成長、毛利率仍上升，暫不扣分；剔除退款毛利率連 2 季年減就觸發","watch":"剔除退款毛利率的年變化、批發占比、Fly Pace 銷售占比","evidence_refs":["channel_business_model_shift#1"],"fact_refs":["f_kpi1_non_gaap_ieepa","f_kpi8"]},{"view":"價格已反映太多","evidence":"7 月財報後賣方下修目標價：Telsey $113→$105、Needham $138→$125、Truist 降到 $105。FY1 共識 7.73 含約 $0.5 的一次性關稅退款；FY2、FY3 共識各下修約 1.4% 和 1.3%","assumption":"現價 10.5 倍是真便宜，而不是盈餘基期被一次性項目墊高造成的假象","consequence":"若 FY2 共識再下修 10% 到約 7.4，本益比約 11 倍，和今年剔除退款後的 EPS 幾乎一樣，等於兩年零成長","ruling":"反駁：剔除退款後仍約 11 倍，FY2 口徑 9.9 倍；即使走 Bear 路徑，EPS 6.9 × 9 倍也只到 $62（−23%）。價格已經反映的是停滯，不是成長","watch":"FY2 共識修正方向、賣方目標價中位數","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_fwd_pe_latest"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 104.69 → 本次 81.09（-22.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=104.69","side_b":"本次 price_at_dd=81.09","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟡→❌。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星持倉 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟡→❌。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 104.69 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 104.69 美元：Bull 價 218.5、Bear 價 86，五年期望值 +51.5%，基準年化 9.6%，不對稱比 6.0","side_b":"本次情境、股價仍用 104.69 美元：Bull 價 219.2、Bear 價 67.5，五年期望值 +32.1%，基準年化 6.1%，不對稱比 2.57","ruling":"先換情境、股價不動：五年期望值少 19.4 個百分點，基準年化少 3.5 個百分點。不對稱比由 6.0 變為 2.57。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 104.69 美元：五年期望值 +32.1%，基準年化 6.1%，不對稱比 2.57","side_b":"本次情境、股價 81.09 美元：五年期望值 +70.6%，基準年化 11.6%，不對稱比 8.47","ruling":"再換股價、情境不動：起點價下跌 22.5%，五年期望值多 38.5 個百分點，基準年化多 5.6 個百分點，不對稱比由 2.57 升到 8.47。合計五年期望值比前份多 19.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"HOKA 成長論點與門檻","cause":"新證據","prior_field":["signal","moat_trend"],"side_a":"前份：HOKA 維持低雙位數成長，Q1 的高個位數只是批發出貨時點造成的一次性；門檻是季度成長 ≥10%","side_b":"本次：Q1 +7.7%、Q2 +7%；全年指引從低雙位數降到高個位數，Q3 預告低至中個位數；CEO 承認 2026 年部分新款反應不佳。門檻下修為 ≥8%","ruling":"採本次證據：前份 H1 已經削弱，出貨時點一次性的說法不成立。門檻從 10% 改為 8%，是依管理層新指引重新定錨，不是放寬標準。定價力沒有受損（剔除退款毛利率年增 120bp），護城河方向維持 →，品質訊號維持 B；進出場結論與倉位角色交給估值與均線重新判定","evidence_level":"公司新聞稿加上法說中管理層口述","settle_metric":"HOKA FY27 第四財季營收年增率（2027 年 5 月公布）","if_then":["若 HOKA 第四財季年增 ≥5%，且 FY2028 指引 ≥ 高個位數 → 維持論點，可分批加碼到 3%","若 HOKA 第四財季 <5%，且 FY2028 指引 ≤ 中個位數 → 減碼一半，H1 改判為反轉"],"evidence_refs":["substitute_technology#2"]},{"axis":"管理層前後說法","cause":"新證據","prior_field":null,"side_a":"2026-07-23 法說：CFO 說 FY27 營收 $5.86–5.91B 維持不變，下半年加速主要來自 HOKA 與國際批發，國際出貨移後不是需求假設改變；CEO 說 UGG 訂單沒有被取消","side_b":"2026-10-22：營收下修到 $5.700–5.725B，HOKA 高個位數、UGG 低個位數；歐洲第三方物流延遲約 $22M，其中部分可能被取消；UGG 不再假設有去年那樣的補單","ruling":"不可調和（方向相反），採 10-22 的新說法。三個月前歸因為物流時點，現在變成全年下修，管理層對短期能見度的判斷要打折。歐洲物流延遲維持為未證實的一次性因素，並先寫下證偽條件","evidence_level":"兩場法說的管理層原話","settle_metric":"下一季是否再揭露履約延遲；HOKA 第四財季是否如指引加速","if_then":["若 Q3 FY27 法說再揭露歐洲或其他物流延遲 → 一次性歸因視為證偽，下修 EMEA 成長假設並停止加碼","若 Q3、Q4 都達到指引且沒有新的延遲 → 恢復對管理層指引的正常信任，不再額外打折"],"evidence_refs":[]},{"axis":"價值陷阱、成長空間與公司類型","cause":"新證據","prior_field":["trap","runway_post_y5","archetype","cycle_position"],"side_a":"前份：價值陷阱 🟡、五年後成長空間 🟡、品質複利成長、非循環股（沒有循環定位）","side_b":"本次維持同樣的判讀。衰退訊號亮兩個：過去三年 EPS 年複合約 29.6%，遠高於營收約 14.7%；$120 以下價帶份額可能流失。HOKA 在批發與國際仍有擴張空間，UGG 在延伸品類；利潤率高、沒有負債，仍屬品質複利型，但信心降為中","ruling":"四欄都不變：成長減速還沒讓衰退訊號累積到三個以上。但若 HOKA 連 3 季低於 5%，陷阱判讀升為 🔴、成長空間降為 🔴","evidence_level":"年度財報與法說","settle_metric":"HOKA 與 UGG 季度營收年增率","if_then":["若 HOKA 連 3 季 <5% 或 UGG 連 2 季年減 → 陷阱改判 🔴、成長空間改判 🔴","若 HOKA FY2028 回到 ≥8% → 維持 🟡"],"evidence_refs":[]},{"axis":"估值結論與回撤範圍","cause":"價格變動","prior_field":["val","max_dd_pct"],"side_a":"前份：股價 $104.69（約 14 倍 FY1）判便宜，最大回撤預估 −40%","side_b":"本次：股價 $81.09，26 週跌 25%，前瞻本益比 10.5 倍（剔除退款約 11 倍），判便宜，而且比前份更便宜；最大回撤改成區間 −30% 至 −45%","ruling":"估值結論不變，股價下跌讓倍數壓縮約四分之一。回撤改用區間表示，下緣用極端 Bear（7.2 倍 × 6.70，約 $48）推出","evidence_level":"收盤價與共識快照","settle_metric":"FY2 共識 EPS 與股價","if_then":["若 FY2 共識下修超過 10% → 重算 Bear 下緣","若股價先漲過 $100 而 HOKA 證據還沒出現 → 不追"],"evidence_refs":[]},{"axis":"情境機率","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份 Bull 25%、Bear 25%","side_b":"本次 Bull 25%、Base 45%、Bear 30%","ruling":"Bear 機率上調 5pp：HOKA 成長門檻已破、管理層改口，而且共識的每股成長要靠回購才補得上，超出資本再投資能支撐的內生成長，所以 Bear 不低於 30%","evidence_level":"法說加財報推算","settle_metric":"FY2028 財測","if_then":["若 FY2028 HOKA 指引 ≥ 高個位數 → Bear 機率降回 25%","若 FY2028 HOKA 指引 ≤ 中個位數 → Bear 機率升到 40% 並減碼一半"],"evidence_refs":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"HOKA cc growth 連 2 季回站 ≥ 低雙位數（證 Q1 高單位是 wholesale timing 一次性）或 回檔至 BB 下軌 $92 附近 thesis 完整","side_b":"HOKA 單季營收年增回到 ≥5%（先看 FY27 第四財季），且週收盤站回 250 週均線 $102.88","ruling":"重新進場的條件改寫。舊條件的價格那一半已被跌破（現價 $81.09），而 HOKA 並沒有回到低雙位數，舊條件失效。新條件依新指引把 HOKA 門檻下修到 ≥5%，並加上 250 週均線確認；兩者同時成立才重跑判斷、首倉進場。另設：跌破 $70 且門檻未破時，可先試單加碼","evidence_level":"法說指引與週線價格","settle_metric":"HOKA 第四財季營收年增率、週收盤價","if_then":["若兩條件同時成立 → 重跑判斷後首倉 2%","若只有價格站回、HOKA 沒達標 → 不追"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份沒有設 Single Thing（null）","side_b":"Single Thing：2027 年 5 月的 FY2028 財測給出 HOKA 全年成長 ≤ 中個位數","ruling":"新設 Single Thing：HOKA 是唯一的成長引擎，它的成長指引是對 EPS 路徑與終端倍數影響最大的單一變數；一旦發生就減碼一半，若 UGG 冬季同時年減則清倉","evidence_level":"法說指引","settle_metric":"FY2028 HOKA 成長指引","if_then":["若發生 → 減碼一半","若同時 UGG 冬季年減 → 清倉"],"evidence_refs":[]},{"axis":"停損指標","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份沒有設停損門檻（null）","side_b":"HOKA 季度年增連 3 季 <5%；剔除退款的年度營業利益率 <20%；UGG 連 2 季年減","ruling":"新設三條：任一條觸發就減碼一半，兩條同時觸發就清倉。門檻來自本次 HOKA 指引下修與全價紀律能不能守住","evidence_level":"季報與法說","settle_metric":"三條指標每季更新","if_then":["任一條觸發 → 減碼一半","兩條同時觸發 → 清倉"],"evidence_refs":[]},{"axis":"現在就買或等待","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：剔除退款仍只有 11 倍本益比，沒有負債，FCF 約為市值 11%；公司一年回購約一成股本，還有 $4.4B 授權。同業在促銷時毛利率反升 120bp，證明定價力沒壞；只要 EPS 不衰退，倍數回到 12–13 倍就有 15–20% 空間","side_b":"現在不買的最強論證：管理層三個月內從只是物流時點，改口成下修全年；HOKA 已連兩季低於 8%，下一季預告更低，第四財季的加速全押在新品。股價在 250 週均線之下，賣方目標價持續下修，價格趨勢和基本面一起轉弱","ruling":"兩邊都成立，結論是等證據：估值給了安全邊際，但成長引擎還在驗證期。不追，等 HOKA 第四財季回到 ≥5% 再進；跌破 $70 且門檻未破，可先試單","evidence_level":"財報、法說與價格","settle_metric":"HOKA 第四財季營收年增率","if_then":["若 2027 年 5 月 HOKA 第四財季 ≥5%，且週收盤站回 $102.88 → 重跑判斷，首倉 2%","若股價先漲過 $100 而 HOKA 證據還沒到 → 不追","若股價跌破 $70 而 HOKA、UGG 門檻都沒破 → 分批試單 1%（不是停損邏輯）"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"HOKA 第四財季（2027 年 1–3 月）營收年增是否回到 ≥5%","type":"假設驗證","maps_to":"H1","metric":"HOKA 季度營收年增率","threshold":"≥5%","action":"達標就維持論點，可分批加碼到 3%；沒達標就停止加碼","source_freq":"季報新聞稿／每季","date":"2027-05","evidence_refs":["substitute_technology#2"]},{"n":2,"text":"UGG 冬季旺季（Q3 FY27）營收能否守住正成長","type":"假設驗證","maps_to":"H2","metric":"UGG 季度營收年增率","threshold":"≥0%","action":"若年減，減碼三分之一","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":[]},{"n":3,"text":"FY2028 財測中 HOKA 全年成長 ≤ 中個位數","type":"Single Thing","maps_to":"single_thing","metric":"HOKA FY2028 成長指引","threshold":"≤ 中個位數（約 ≤5%）","action":"減碼一半；若 UGG 冬季同時年減則清倉","source_freq":"年度財測","date":"2027-05","evidence_refs":[]},{"n":4,"text":"剔除關稅退款的毛利率連 2 季年減（促銷與批發占比擴大侵蝕定價力）","type":"風險","maps_to":"R2","metric":"剔除退款毛利率的年變化","threshold":"連 2 季 <0bp","action":"停止加碼，護城河方向改判 ↓","source_freq":"法說／每季","date":null,"evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#1"]},{"n":5,"text":"公司關稅稅率假設從 12.5% 再上調，或剔除退款毛利率跌破 55%","type":"風險","maps_to":"R3","metric":"關稅稅率假設／剔除退款毛利率","threshold":">12.5%／<55%","action":"減碼三分之一","source_freq":"法說／每季","date":null,"evidence_refs":["reg_tariff_export#0","supply_demand_durability#3"]},{"n":6,"text":"股價跌破 $70（約 FY2 EPS 8.5 倍），且 HOKA、UGG 門檻都沒破","type":"加碼","maps_to":"H3","metric":"股價","threshold":"≤ $70","action":"分批試單 1%","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":7,"text":"股價到 $115（約 FY2 EPS 14 倍），但 HOKA 加速還沒證實","type":"減碼","maps_to":null,"metric":"股價","threshold":"≥ $115","action":"減碼三分之一","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":8,"text":"HOKA 單季營收年增回到 ≥5%，且週收盤站回 250 週均線 $102.88","type":"估值rearm","maps_to":null,"metric":"HOKA 季度營收年增率、週收盤價","threshold":"≥5% 且 ≥ $102.88","action":"重跑判斷後首倉 2%","source_freq":"每季／每週","date":null,"evidence_refs":[]},{"n":9,"text":"歐洲第三方物流再次出現履約問題","type":"風險","maps_to":"R5","metric":"管理層揭露的出貨延遲金額","threshold":"任一季再次出現","action":"一次性歸因視為證偽，下修 EMEA 成長假設並停止加碼","source_freq":"法說／每季","date":"2027-01","evidence_refs":[]},{"n":10,"text":"FY2027 第四季財報與 FY2028 全年財測","type":"複審日期","maps_to":null,"metric":"全面複審","threshold":null,"action":"重跑完整判斷","source_freq":"年度","date":"2027-05","evidence_refs":[]}],"kill_metrics":[{"metric":"HOKA 季度營收年增率","bear_threshold":"連 3 季 <5%","window":"FY27 Q3 至 FY28 Q2","source":"公司季報新聞稿","last_status":"warning"},{"metric":"剔除關稅退款的營業利益率（年度）","bear_threshold":"<20%","window":"FY2028 全年","source":"公司新聞稿與法說","last_status":"ok"},{"metric":"UGG 季度營收年增率","bear_threshold":"連 2 季年減","window":"FY27 Q3 至 FY28 Q1","source":"公司季報新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"capital_markets_pricing#4","reason":"資料日是 2026-03-20，針對的是 FY26 第四季的單季估計，之後又過了兩次財報；本包較新的共識快照顯示 FY1 近三個月上修 2.66%，舊的上下修家數已被較新資料取代"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 HOKA 兩季減速和指引下修直接外推成盈餘停滯，給 10.5 倍；但就算淨利零成長，每年約 8–10% 市值的回購也能撐住高個位數的每股成長。全價紀律在促銷環境下還讓毛利率上升，定價力沒壞"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=-25.28, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='❌'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 HOKA 第四財季（2027 年 1–3 月，5 月公布）營收年增回到 ≥5%，且週收盤站回 $102.88；或股價跌破 $70 且 HOKA、UGG 門檻都沒破時先試單'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"4%","requires_critic":[],"rearm_trigger":"HOKA 單季營收年增回到 ≥5%（先看 FY27 第四財季），且週收盤站回 250 週均線 $102.88","exec_line":"現在不追。兩個條件同時成立才重跑判斷、首倉 2%；跌破 $70 且 HOKA、UGG 門檻都沒破，可先試單 1%"},"reasoning":{"industry":"賺的是消費者為品牌付的溢價：HOKA 賣高價緩衝跑鞋，UGG 從羊皮靴延伸到休閒鞋、木屐和服飾。Q2 FY27 營收 $1,481M，其中 HOKA $677.2M（年增 7%）、UGG $786.4M（年增 4%），兩個品牌合計約占 99%。GAAP 毛利率 60.5%、營業利益率 26.3%；剔除關稅退款後營業利益率 23.2%，去年同期 22.8%。製造外包給越南、印尼的代工廠，品牌端拿走大部分價值，錢卡在全價銷售的定價權這一個節點。本季美國運動鞋促銷加劇，公司選擇不跟價，結果美國電商轉弱，營收靠批發與國際撐住。供需持久性屬週期性壓力，預期會反轉：美國通路庫存與促銷是一輪去化（2026-10-22 法說 CFO），國際需求仍強，APAC 增速最高；目前沒有證據顯示品類在結構性衰退。單點依賴：沒有單一客戶占營收 10% 以上，但有一家客戶占應收帳款 18.5%（前一年 13.6%）；UGG 羊皮依賴中國兩家製革廠加工。產業態勢是雙向拉鋸：競爭面在惡化（美國促銷、新進者、資源更大的對手）；結構面在國際市場與 $120 以上高價段轉好；另有關稅這個結構變數，IEEPA 退款屬一次性","moat":"機制是品牌溢價加全價紀律：拉式需求、控制配銷。證據包沒有同業 ROIC，可證方向改用營業利益率差距：DECK TTM 營業利益率 22.67%，高於 On 的 13.79%、Nike 的 8.28%、Crocs 的 20.73%，略低於 Birkenstock 的 24.94%；毛利率 57.8%，僅次於 On 的 64.82%。資料只有一期，無法判斷差距在擴大還是收窄。執行力評 7，方向縮減：HOKA 成長從 FY26 Q3 的 +18% 降到 Q2 FY27 的 +7%；CEO 承認 Transport、Kawana、Solimar 等新款沒打中；歐洲物流也出了問題。定價力評 8，方向穩定：在促銷環境下，剔除退款後毛利率仍年增 120bp；$120 以上價帶份額持續增加；Bondi 9 仍以全價持續售出。一縮一穩，方向判 →，等級 B。報酬持續期：稅後營業利益率約 17.5%（22.67% × 稅後 77%，用 23% 的稅率指引）。投入資本周轉率證據包沒有；以外包製造、存貨 $861M 對年營收約 $5.7B 推斷，屬高利益率×高周轉。再投資率接近零：TTM FCF 利潤率 20.22% 高於稅後營業利益率，表示淨再投資接近零或為負，公式算出的內生成長上限也接近零。實際成長來自費用化的行銷與產品開發，多出來的現金透過回購還給股東","growth":"成長動力以量為主（HOKA 擴大鋪貨、國際市場），價格為輔（全價銷售、選擇性漲價），每股層面靠回購，沒有併購。FY27 全年營收指引 $5.700–5.725B，比 FY26 的 $5.472B 多約 4%；HOKA 高個位數、UGG 低個位數，兩者都比前次下修。Q3 預告 HOKA 只有低至中個位數，全年數字因此隱含 HOKA 在第四財季加速，加速全部押在 Bondi 10、Fly Pace 等新品。三年共識 EPS 從 FY2026A 的 7.02 到 FY2029E 的 9.34，年複合約 10.0%；共識家數證據包沒有。公式算出的內生成長上限接近零，共識與上限之間約 10pp 的缺口可以歸因：回購每年約 8–10% 市值（$1B 對約 $10B 市值），加上小幅營業利益率改善與費用化的品牌投入；不是無法歸因。過去三年每股盈餘年複合約 29.6%，遠高於營收約 14.7%，來自毛利率從 50.3% 升到 57.7% 加上回購，未來難以重演","governance":"FCF 對淨利的轉換約 1.08 倍：TTM FCF 利潤率 20.22%，FY26 淨利率約 18.7%。兩者期間差一季，只看量級。期末現金 $1.210B，沒有借款；存貨 $860.8M，年增 3%，和營收成長 3.5% 相當，沒有堆積。現金去向以回購為主：FY27 上半年回購 $637M，約占流通股 5%；Q1 $338M 均價 $103.79，Q2 $299.3M 均價 $93.65；剩餘授權約 $4.4B，全年假設回購 $1.0B。沒有股息、沒有併購、沒有債要還；資本支出與 SBC 證據包沒有。用上半年 $637M 約占 5% 回推，流通股約 1.2–1.3 億股，現價市值約 $10B，$1B 回購約等於一成市值。營運槓桿：Q2 營收 +3.5%，剔除退款營業利益率升 40bp，沒有壓縮。缺點：回購均價比現價高 15–28%，已經買進的股票目前帳面上是虧的","valuation":"現價 $81.09，對 FY1 共識 EPS 7.73 是 10.5 倍。FY1 含約 $0.52 的一次性關稅退款（Q2 $0.28、Q3 預估約 $0.24）；剔除後用指引中點約 $7.36 算，約 11 倍。用 FY2 共識 8.21 算是 9.9 倍。三年共識 EPS 從 FY2026A 的 7.02 到 FY2029E 的 9.34，年複合約 10.0%，PEG 約 1.05。這個價格只要求 EPS 不衰退：淨利零成長、每年回購約 8% 市值，每股盈餘仍能年增高個位數。回購這一半我信；共識 FY3 的加速我不完全信，FY2、FY3 共識本週各下修 1.4% 和 1.3%。短期上檔：FY2 EPS × 12 倍＝$98.5（+21.5%）。中期上檔取 Base 情境第五年的 $140.6（+73.4%）。五年估值分位與同業本益比證據包沒有；改用自身倍數對照：前份 7 月股價 $104.69，以 7 月底共識 7.53 算約 14 倍，倍數已壓縮約四分之一","premortem":"可能看錯的路徑有三條：①HOKA 新品週期失靈（即唯一致命點）；②UGG 冬季旺季賣不動、補單不如去年；③促銷與批發占比上升，侵蝕全價紀律。股價已在 250 週均線 $102.88 與 52 週均線 $98.68 之下，26 週跌 25%；RSI 43，不過熱。最大回撤區間 −30% 至 −45%，推導見情境假設，路徑風險中等偏高。十類衰退訊號亮兩類：過去三年 EPS 年複合約 29.6%，遠高於營收約 14.7%；$120 以下價帶份額可能流失。毛利率與 FCF 轉換都沒亮。空方最強論證來自 Bernstein（休閒品類萎縮、HOKA 被複製）與 BMO 9 月以 Underperform 開始追蹤，賣方最低目標價 $70"},"plain":{"six":{"how_it_makes_money":"賺的是消費者為 HOKA 與 UGG 兩個品牌付的溢價；錢卡在全價銷售的定價權。產業時鐘在收縮段：美國通路去庫存、促銷加劇，國際需求仍強","moat":"護城河方向 →：定價力穩定，但 HOKA 執行力在縮減，兩者互抵；等級 B","growth":"五年後成長空間中等：HOKA 在運動用品通路鋪貨仍少、國際市場還早，但美國核心跑鞋已不再是雙位數；UGG 已成熟。每股成長主要靠回購","capital":"資本配置紀律佳：無負債，自由現金流高於淨利，大部分現金拿去回購；缺點是回購均價高於現價","valuation":"現價只要求 EPS 不衰退：就算淨利零成長，回購也能讓每股盈餘年增高個位數。回購這一半我信；FY3 共識的加速，我不完全信","how_wrong":"最可能看錯的是 HOKA：新品週期若救不回成長，10 倍本益比就是價值陷阱的起點。目前衰退訊號亮兩個，陷阱風險中等"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 HOKA 兩季減速和指引下修直接外推成盈餘停滯，給 10.5 倍；但就算淨利零成長，每年約 8–10% 市值的回購也能撐住高個位數的每股成長。全價紀律在促銷環境下還讓毛利率上升，定價力沒壞","momentum_overheated":false,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等 HOKA 第四財季（2027 年 1–3 月，5 月公布）營收年增回到 ≥5%，且週收盤站回 $102.88；或股價跌破 $70 且 HOKA、UGG 門檻都沒破時先試單","trap":"🟡","val":"🟢","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":81.09,"week26_return_pct":-25.28,"consensus_rev_3m_pct":2.66,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY1 共識含約 $0.52 的一次性關稅退款，快照也可能早於 10-22 財報；剔除後本益比約 11 倍，前瞻錨改用 FY2 的 8.21（9.9 倍）。分母本身不是爭點，爭點在 FY2 之後 HOKA 能不能加速"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"product","event":"HOKA Bondi 10 與入門款 Fly Pace（$115）上市","impact":"高","watch":"上市後的批發補單與全價售出率；Bondi 9 是否乾淨出清"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q3 FY27 財報（UGG 冬季旺季、HOKA 第四財季指引）","impact":"高","watch":"UGG 是否年增；HOKA 第四財季的加速指引是否維持"},{"date":"2027-04","date_precision":"month","type":"product","event":"HOKA Mach Pro 上市","impact":"中","watch":"管理層稱訂單很強，看上市後的售出率"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 第四季財報與 FY2028 全年財測","impact":"高","watch":"HOKA 全年成長指引是否 ≥ 高個位數；剔除退款後的營業利益率指引"},{"date":"2027-06","date_precision":"month","type":"product","event":"Bondi Ultra X（$325）上市","impact":"低","watch":"高價段份額能否延伸"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"剩餘約一成、尚未收到的 IEEPA 關稅退款","impact":"低","watch":"未納入財測，到帳屬一次性，不改變經常性盈餘"}],"_projected_from":"v19"}
```
