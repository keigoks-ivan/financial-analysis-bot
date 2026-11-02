你是 stock-analyst v20 的**散文層（prose）agent**，標的 CDNS（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：CDNS　日期：2026-11-02　archetype：None　前份裁決：2026-09-24　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2014B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（598B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1004B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1649B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1293B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（518B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1045B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2118B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4745B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3138B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2014           3490-4986      5 條（2–6 內）  
s3                  8000         598           5181-7402      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3946          7738-11054      5 條（2–6 內）  
s6                 11000         518          7337-10482      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1045           1718-2455      5 條（2–6 內）  
s10                 5000        2118           2017-2882      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3138           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5323B；至少需散文≈39.68KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−49%
−41%
−35%
−35
−21.3%
−14%
−3.83
0
0%
0.2
0.30
0.3
0.45
0.6%
0.75
0.8
1
1.05
1.06
1.11
1.17
1.20
1.3
1.32
1.406
1.43
1.47
1.6
1.7
1.87
02
2%
2
2.11
2.2
2.24
2.6%
2.6
2.99
3
3%
3.1
3.3%
3.74
3.8%
4
04
4.06
5
5%
5.82
6
06
6%
6.1%
7%
07
7
7.1
7.6%
7.6
8
8.40
8.42
8.8
9.0%
9
09
9%
9.20
9.3%
9.3
9.4
9.5%
9.55
9.6%
9.7
9.8
9.85
10
10%
10.2
10.3%
11
11.0%
11%
11.4
11.60
11.6
12
12%
12.3
12.7
13
13.1
13.5%
14%
14
14.25%
14.4%
14.52
14.7
14.9
15%
15
16
16.33
16.8
17.0%
17
17%
17.1
17.4%
17.5
17.9
18%
19.5%
20
20%
20.5
21%
22%
22
23
24%
24
25%
25
26
26%
26.2%
26.5
27%
27
27.5
28.5%
28.7%
29%
29.2%
29.6%
30
30%
31
31%
32.6%
33%
33
33.3
33.3%
35%
35
36
36.7%
37%
38.9
38.94
39
40%
40
40.95%
41.8
42
42.75%
43.2%
44%
44
44.1%
44.25%
44.7%
45
45.0%
45%
45.5%
46.7%
48
49
49.5
49.6
50%
50
52.97
53
53.7
53.7%
53.8%
54
54.2%
55%
57.5%
60%
65
65.2
70
72.4%
80%
82
85.7%
86.4%
89
89.6%
97.5%
100
100%
146
150%
206.8
213
213.4
$260
260
266
273.1
274.4
274.7
300
309.09
327.89
353
413
420
450
504
635
691.2
738
2015
2021
2025
2026
2027
2028
2031
2036
688521
20261102
5,300
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
{"meta":{"ticker":"CDNS","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Cadence Design Systems"},"oneliner":"EDA 雙寡頭之一，先進製程簽核與硬體驗證鎖住客戶，agent 帶動底層工具用量，經常性營收年增由 11% 升到 18%；現價約 FY2026 共識 39 倍，基本情境年報酬約 9%，等 11/9 出口規則結果再動，266 美元以下加碼。","thesis":{"H":[{"id":"H1","text":"設計活動加上 agent 帶動底層工具用量，經常性營收維持中高十幾%的有機成長","2y":"FY2027 經常性營收有機年增 ≥15%，在手訂單年增 ≥10%","5y":null,"10y":null,"threshold":"經常性營收有機年增 ≥15%（Q3 報 18%，是否含 Hexagon 待 Q4 揭露）","source":"每季 CFO commentary 與法說；在手訂單見季報新聞稿","drift_rule":"連 2 季低於 14.25% 為削弱；連 3 季低於 13.5% 為反轉"},{"id":"H2","text":"扣除 Hexagon 後增量利潤率 54–55%，加上 Hexagon 整合改善，非 GAAP 營業利益率續升，EPS 成長快於營收","2y":"FY2027 非 GAAP 營業利益率 ≥45.5%（FY2026 財測中點 44.7%）","5y":null,"10y":null,"threshold":"FY2027 非 GAAP 營業利益率財測中點或實績 ≥45.5%","source":"2027 年 2 月全年財測、每季 CFO commentary","drift_rule":"連 2 季低於 43.2% 為削弱；連 3 季低於 40.95% 為反轉"},{"id":"H3","text":"agent 成為可揭露的營收來源並推高核心 EDA 用量，EDA 占客戶研發預算由約 11–12% 上升","2y":null,"5y":"2028 年底前揭露 agent 營收或占比，核心 EDA 年增維持 ≥15%","10y":null,"threshold":"首次揭露 agent 營收，且當期核心 EDA 年增 ≥15%（Q3 為 20%）","source":"法說、投資人會議、10-K","drift_rule":"核心 EDA 年增連 4 季低於 14.25% 為削弱；連 6 季低於 13.5% 為反轉"},{"id":"H4","text":"開源工具加大模型的流程停留在成熟製程，N3 以下的先進製程簽核仍由商用 EDA 把持，Cadence 在數位實作、類比、硬體驗證維持前二","2y":null,"5y":null,"10y":"到 2036 年，7 奈米以下的量產投片仍使用商用簽核流程","threshold":"前十大晶片設計公司無一在 7 奈米以下以非商用工具量產投片","source":"台積電技術論壇、產業新聞、法說","drift_rule":"跨 2 個年度出現繞過案例為削弱；跨 3 個年度為反轉"}],"R":[{"id":"R1","text":"BIS 把出口限制擴及實體清單持股五成以上關係企業的規則，一年暫停期在 2026-11-09 到期；中國營收占比未揭露，10-K 已承認先前限制造成不利影響","h_ref":"H1","clock":"⚡","threshold":"暫停未延長，且公司下修全年財測或揭露影響→停止加碼；全年營收影響超過 2%→減碼三分之一","evidence_refs":["geo_supply_chain#4","geo_supply_chain#2","geo_supply_chain#3","reg_tariff_export#4","reg_tariff_export#2"]},{"id":"R2","text":"2025 年認罪協議、BIS 行政和解與緩刑義務仍在持續；違反可能招致新的刑事、民事程序或拒絕出口特權","h_ref":"H1","clock":"⚡","threshold":"任一新處分或出口特權受限→清倉","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","reg_tariff_export#0","geo_supply_chain#5","major_events#2","lawsuit_class_action#0"]},{"id":"R3","text":"大模型加開源 EDA 的流程由成熟製程往先進製程延伸，繞過商用簽核","h_ref":"H4","clock":"🐢","threshold":"前十大設計公司在 7 奈米以下以非商用流程量產投片 1 例→減碼一半並重跑研究","evidence_refs":["substitute_technology#0"]},{"id":"R4","text":"agent 層三家趨同，對手以 50% 營益率目標與權利金模式搶客；共封裝光學設計工具可能落後","h_ref":"H3","clock":"🔥","threshold":"核心 EDA 連 4 季年增 <14.25%，或 2027 年台積電論壇前仍無 COUPE 支援→停止加碼","evidence_refs":["substitute_technology#3","competitive_share_entrants#0","competitive_share_entrants#1"]},{"id":"R5","text":"硬體依賴單一或少數零組件供應商；Q2 稱受供給限制，Q3 改稱沒有限制，硬體認列按季起伏","h_ref":"H1","clock":"🔥","threshold":"硬體營收連 2 季年減，或公司再提供給受限→停止加碼","evidence_refs":["geo_supply_chain#1"]},{"id":"R6","text":"經常性營收年增由約 20% 降到 18%，沒有說明是否含 Hexagon；有機成長可能已接近 15% 門檻","h_ref":"H1","clock":"⚡","threshold":"Q4 扣除 Hexagon 的經常性營收年增 <15%→停止加碼；連 3 季 <13.5%→減碼三分之一","evidence_refs":[]},{"id":"R7","text":"GAAP 與非 GAAP 營益率差距擴大：Q3 GAAP 營益率低於財測下緣，SBC 占營收 9.3%","h_ref":"H2","clock":"🔥","threshold":"Q4 GAAP 營益率 <29%→停止加碼","evidence_refs":[]}],"single_thing":{"description":"2027 年 2 月 Q4 財報給出的 FY2027 全年非 GAAP EPS 財測中點低於 9.20 美元：比共識 9.85 美元低約 7%，比 FY2026 財測中點 8.40 美元只多約 9.5%。","why_fatal":"現價約是 FY2027 共識的 33 倍，前提是 EPS 年增 15% 以上能延續。財測若只給一成以下的成長，代表 2026 年 21% 的營收成長含有 Hexagon 與硬體的一次性成分，倍數會往 22–25 倍走，五年價值由基本情境約 504 美元掉向空頭的約 213 美元。倍數與 EPS 同時下修，是五年價值裡敏感度最大的單一項。","if_happens":"減碼一半，停止加碼；重跑研究，基本情境改用財測中點，空頭機率提高到 40%。","how_monitor":"看 Q4 財報新聞稿與 CFO commentary 的全年財測。事前追蹤 Q4 經常性營收年增，以及 82 億美元的在手訂單是否續增。","probability":"約 15%（12–24 個月）。全年財測連兩季上調，2026 年是三年續約週期的低點年，2027 年續約量較大，所以機率不高；但 agent 用量型營收不在財測內，Maestro 後訓練成本也可能壓低開局財測。"}},"appendix_a":{"growth_durability":8,"quality_score":8,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":33.3,"peg_fy2":1.87,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":8.42,"FY2027E":9.85,"FY2028E":11.6},"fy_end_month":12,"eps_basis":"非 GAAP 稀釋 EPS（Koyfin 共識，2026-10-31 快照）。FY2025A 非 GAAP 實績事實表未涵蓋：年度表只有 GAAP 稀釋 EPS 4.06 美元，口徑不同不混用，所以共識成長改以 FY2026E 到 FY2028E 兩年計。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"高毛利寡占設計軟體，約八成經常性營收；成長跟著客戶研發預算與設計複雜度走，再投資靠費用化研發而非資本支出"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久。CEO 稱設計活動為歷來最強，並轉述台積電預估五年內晶片尺寸增 48 倍（Q3 法說）。硬體按季起伏，IP 有季度時點性（Q2 法說 CFO 提醒勿年化單季）。","bargaining":{"up":"上游是硬體零組件與代工；部分零組件只有單一或少數供應商（10-K），議價權在供應商，但只影響硬體","down":"沒有單一客戶占營收 10% 以上，系統公司占約 45%；先進製程整套流程轉換成本高，客戶議價力有限","geo":"受中國出口管制與 2025 年認罪協議的緩刑義務約束；中國營收占比未揭露"},"profit_pool_dir":"利潤往 EDA 流：管理層稱 EDA 占客戶研發預算由約 11–12% 往更高走（2026-06 投資人會議，未經獨立驗證）。風險是 agent 層的價值被大模型與算力供應商分走。","tam_table":[{"item":"EDA 占晶片公司研發預算","value":"約 11–12%；管理層稱可往約 33% 走（2026-06 投資人會議，未經獨立驗證）"},{"item":"系統公司占營收","value":"約 45%（Q3 法說 CEO）"},{"item":"設計尺寸","value":"台積電預估五年內晶片尺寸增 48 倍（Q3 法說 CEO 轉述）"},{"item":"agent 客戶接觸","value":"Q3 超過 100 個進行中；Q2 時 ChipStack 逾 20 個、ViraStack 逾 25 個"},{"item":"TAM 金額與滲透率","value":"事實表未涵蓋"}]},"moat":{"mechanism":"轉換成本加晶圓廠製程認證。先進製程的設計實作、簽核結果與 PDK 綁在一起，換供應商要重驗整套流程。agent 疊在自家模擬與最佳化引擎上，agent 呼叫次數越多，底層工具用量越大。","execution":9,"pricing":8,"grade":"A","trend":"↑","trend_evidence":"執行面在擴大：經常性營收年增由去年 11% 升至 Q3 18%；Q3 新增 16 個數位全流程案，類比、PCB 與多體動力學都有競爭替換（Q3 法說 CEO）。定價面持平：agent 採訂閱加用量計價，IR 稱每個 agent 價值數萬美元（2026-06 投資人會議），但營收尚未揭露。","peer_na_reason":"同業 ROIC 與投入資本口徑事實表未涵蓋，改用營益率與 FCF 利潤率代替。營益率差距為正（29.6% 對 11.0%），但 FCF 利潤率持平；缺多年資料，無法判斷差距是否擴大。","threats":[{"level":"🟡","text":"agent 層三家趨同：Synopsys 推出自主驗證 agent，並與 OpenAI 合作專用模型；三家都建在 NVIDIA 架構上，路線圖由 NVIDIA 與 AMD 帶動。屬點對點競爭，差異化取決於 agent 與自家引擎整合的深度。","p":40,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"成熟製程被大模型加開源工具部分繞道：Kimi K3 以開源工具 48 小時完成 45 奈米設計。目前只到成熟製程；若延伸到 7 奈米以下量產，升級為架構替代並重評論點。","p":30,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"共封裝光學（COUPE）需要跨領域模擬，Cadence 尚未揭露支援，這一塊可能讓給 Synopsys。","p":35,"evidence_refs":["substitute_technology#3"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推定）：非 GAAP 營益率 44–45%，有機成長幾乎不需實體資本。但 Hexagon 約 27 億歐元的收購墊高了投入資本，周轉率實數事實表未涵蓋。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是設計工程師，決策者是設計主管與 CAD 團隊，付款來自研發預算，三方利益一致。延後買工具等於延後投片，是需要而不是想要。Q3 MediaTek、Renesas、Samsung Foundry 已把 agent 放進量產流程，需求來自設計複雜度上升（晶片尺寸五年增 48 倍）。"},{"item":"決策層級","level":"🟢","text":"替代性要看整套流程，不是單一工具：實作、簽核與晶圓廠認證綁在一起。Q3 新增 16 個數位全流程案，大客戶整套導入讓轉換成本再升。10-Q 沒有揭露任何具名客戶改用第二供應商或自建。續約率與漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"EDA 只拿走客戶研發預算約 11–12%，相對所創造的價值偏少，有提價空間。但 agent 層新增的價值可能被大模型與算力供應商分走，三家都建在 NVIDIA 架構上。公司的對策是自有 Maestro 模型、模型路由，以及讓客戶自付算力，成效未證。"},{"item":"社會容忍度","level":"🟡","text":"不是民生必需品，沒有消費者端的漲價天花板。限制來自國安：2025 年認罪協議與緩刑義務，加上中國出口規則反覆，銷售權受監管授權左右。中國營收占比未揭露。"}],"roiic":"事實表未涵蓋（缺投入資本與 D&A）。分兩段看：有機段幾乎不需實體資本，增量報酬極高；併購段 Hexagon 2026 年營收約 1.6 億美元，營業利益貢獻接近零（Q3 法說 CFO），首年 ROIIC 接近零。","reinvest_rate":"事實表未涵蓋（缺 D&A 與營運資金變動）。2026 年含 Hexagon 約 27 億歐元（七成現金）收購，當年再投資率偏高；其餘年度現金多用於回購，2026 年逾自由現金流五成。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。本公司成長主要來自費用化研發（研發密度 33.3%），這個公式會低估有機成長能力，所以不填數字。"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","CDNS":85.68,"SNPS":72.38,"ARM":97.54,"QCOM":54.23,"688521.SH":34.18,"unit":"%"},{"metric":"營業利益率","CDNS":29.64,"SNPS":11.03,"ARM":17.3,"QCOM":23.28,"688521.SH":-21.28,"unit":"%"},{"metric":"FCF 利潤率","CDNS":28.65,"SNPS":29.18,"ARM":28.55,"QCOM":23.64,"688521.SH":12.94,"unit":"%"},{"metric":"研發密度","CDNS":33.3,"SNPS":30.6,"ARM":57.49,"QCOM":22.45,"688521.SH":46.23,"unit":"%"}],"competitors":[{"name":"SNPS","gm":72.38,"om":11.03,"fcf_margin":29.18,"rd_intensity":30.6,"strategy_note":"唯一同級對手。TTM 營益率 11.0% 受併購攤銷拖累，但 FCF 利潤率 29.2% 與 Cadence 28.7% 持平，現金獲利力並未落後。已宣示 50% 營益率與權利金模式，又推出與 OpenAI 合作的專用模型，agent 層競爭會更激烈。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"ARM","gm":97.54,"om":17.3,"fcf_margin":28.55,"rd_intensity":57.49,"strategy_note":"IP 授權同業，毛利率 97.5%、研發密度 57.5%。可當 Cadence IP 業務的參照，不是 EDA 直接對手。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"QCOM","gm":54.23,"om":23.28,"fcf_margin":23.64,"rd_intensity":22.45,"strategy_note":"大客戶型參照（晶片設計公司），毛利率 54.2%。用來對照 EDA 供應商在客戶價值鏈裡拿走多少，不是競爭者。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"688521.SH","gm":34.18,"om":-21.28,"fcf_margin":12.94,"rd_intensity":46.23,"strategy_note":"中國設計服務與 IP 業者，營益率 −21.3%。中國本土替代者的財務體質仍弱，短期難以在先進製程構成威脅。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（設計案數、晶片尺寸、系統公司自研），價與 agent 加購次之；2026 年併購約 3 個百分點，淨回購約 0","runway_years":"≥10（以 EDA 占客戶研發預算約 11–12% 估，不是滲透率口徑）","runway_post_y5":"🟢","endo_ceiling_basis":"增量 ROIC 與再投資率事實表未涵蓋，不給數字。有機成長靠費用化研發，公式算出的上界偏低。共識 EPS 成長超出的部分，歸因於營益率擴張（增量利潤率 54–55%）與很少的淨回購。","segments":[{"item":"核心 EDA","value":"Q3 年增 20%、Q2 18%；營收占比事實表未涵蓋"},{"item":"IP","value":"Q3 年增 24%、Q2 逾 40%；季度時點性大，CFO 提醒勿年化單季"},{"item":"系統設計與分析","value":"Q3 年增 30%、Q2 37%；含 Hexagon D&E（2026 年約 1.6 億美元）"},{"item":"硬體（Palladium／Protium）","value":"連續創單季紀錄，預期 2026 年創年度紀錄；季度起伏大"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":null,"evidence":"TTM 85.7%，低於 FY2025 的 86.4% 與 FY2022 的 89.6%；季度年比事實表未涵蓋，主因是硬體、IP 與併購造成的組合變化"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"CEO 稱幾乎各區塊都在拿份額；沒有第三方份額數字"},{"signal":"主力產品提價後銷量下滑","lit":null,"evidence":"事實表未涵蓋"},{"signal":"EPS 成長顯著高於營收成長（差距超過 5 個百分點）","lit":false,"evidence":"FY2026 到 FY2027 共識 EPS 增 17.0%，營收增 14.4%，差 2.6 個百分點"},{"signal":"FCF÷淨利連 2 年低於 0.75","lit":false,"evidence":"FY2022–FY2025 約 1.32、1.20、1.06、1.43"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":null,"evidence":"Q2 為 9.3%，水準已超過 5%；逐年趨勢事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"開源加大模型示範只到 45 奈米，列入追蹤"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"evidence":"事實表未涵蓋；自身 trailing 本益比在四個年度端點的第 49.6 百分位"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"evidence":"Q2 資本支出 5,300 萬美元，FCF 5.82 億美元，約 9%"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"營收連年雙位數成長"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"2026 年約 21% 營收成長中 Hexagon 約占 3 個百分點，以有機成長為主，不是靠併購撐。近三年現金去向四分事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Hexagon D&E 約 27 億歐元；2026 年營收約 1.6 億美元，營業利益貢獻接近零（Q3 法說 CFO），首年已實現 ROIIC 遠低於資金成本。CFO 預期 2027 年改善，未證。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購買入收益率＝FY2026 共識 EPS 8.42÷股價 327.89，約 2.6%。10 年期殖利率事實表未涵蓋，但只要高於 0.6% 就過不了門檻。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營收 9.3%（Q2）。稀釋股數由 FY2022 約 274.7 百萬到 FY2025 約 273.1 百萬，現為 274.4 百萬（含 Hexagon 換股），淨稀釋率約每年 0%。","grade":"過"}]},"valuation":{"basis":"Forward 本益比（FY2026E 非 GAAP 共識）搭配 PEG；終端以 FY2031E EPS×本益比計","peers":{"expanded":false,"reason":"同業本益比與前瞻倍數事實表未涵蓋，只有利潤率對照；終端倍數改以自身 FY2027 的 33 倍為上緣參考"},"fwd_pe":38.94,"peg":2.24,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Forward 本益比 38.9 倍，FY2027 為 33.3 倍。PEG 2.2（以 FY2026E 到 FY2028E 共識年複合 17.4% 計），屬偏貴。但 trailing 本益比、P/S、EV/S 在近四個年度端點只落在第 42–50 百分位，位於自身區間中段；26 週下跌 3.8%，RSI 49.5，沒有過熱。綜合判斷為合理偏貴，不算便宜。五年分位事實表未涵蓋，只有四個年度端點。12 個月看 FY2027E 9.8 美元×36 倍，約 353 美元（+7.6%）；五年基本情境 504 美元（+53.7%，未計回購）。","upside_short_pct":7.6,"upside_mid_pct":53.7},"trap_analysis":{"verdict":"🟢","label":"不是價值陷阱：成長在加速、現金轉換率高；風險在估值與監管事件，不在基本面衰退"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 經常性營收年增 18%，低於 Q2 扣除 Hexagon 後的約 20%，而且沒有說明 18% 是否含 Hexagon；若含約 4 個百分點，有機成長只剩約 14%。2026 年是續約低點年，訂單仍強，可能有提前成交。7 月開源模型在 45 奈米完成整套設計，當日股價跌 9.6%。","assumption":"H1：經常性營收有機年增 15% 以上可延續到 2027 年。","consequence":"有機成長若回到低十幾%，EPS 五年只增約 3%（FY2031E 9.7 美元），本益比壓到 22 倍，五年後約 213 美元，較現價 −35%。","ruling":"部分採納：與唯一致命點部分重疊，已補成減碼門檻，但不當基本情境。理由是 Q2 在手訂單年增 27%，Q3 再創 82 億美元新高；續約低點年的訂單成長來自加購，不是續約時點（Q3 法說 CFO）。","watch":"Q4 法說揭露的扣除 Hexagon 經常性營收年增；FY2027 全年財測。","evidence_refs":["substitute_technology#0","supply_demand_durability#4"],"fact_refs":["f_kpi6_backlog","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"2025 年 7 月認罪協議與 BIS 和解，淨罰款與沒收 1.406 億美元。10-K 寫明，違反認罪協議、行政和解或緩刑條件，可能招致進一步的刑事、民事、行政程序或拒絕出口特權；同時承認先前的中國出口限制已造成不利影響，未來的限制無法預測。","assumption":"合規計畫有效，緩刑期內沒有新違規；出口限制不擴大到 EDA 主力產品。","consequence":"出口特權若遭拒，海外銷售中斷，論點全面失效。中國限制若擴大，營收與利潤率都會下修，但占比未揭露，無法量化。","ruling":"採納為清倉條件，但不放進基本情境。違規期間是 2015–2021 年，和解後已建合規計畫，近 12 個月的 8-K 也沒有新的法律程序；機率低，但後果極端。","watch":"DOJ 與 BIS 公告、8-K 法律程序、11/9 規則到期結果。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","reg_tariff_export#0","geo_supply_chain#5","major_events#2","lawsuit_class_action#0","geo_supply_chain#3","reg_tariff_export#4"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Q2 SBC 1.47 億美元，占營收 9.3%、占 GAAP 營業利益 32.6%。Q3 GAAP 營益率 26.2%、GAAP EPS 1.05 美元，都低於公司自己給的 Q3 財測（27.5–28.5%、1.11–1.17 美元），非 GAAP 卻高於財測。稀釋股數四年大致持平，回購只是抵銷 SBC 與 Hexagon 換股。全年營收財測上調約 1 億美元，營運現金流財測仍維持約 20 億美元。","assumption":"營收成長能按比例轉成每股自由現金流。","consequence":"營收與非 GAAP EPS 達標，但每股 GAAP 盈餘與每股現金流成長落後；股東實際拿到的報酬會低於情境樹，因為情境樹用的是非 GAAP EPS。","ruling":"部分採納：資本配置只有 SBC 淨稀釋一項過關。不改情境機率，但把 GAAP 營益率列入追蹤，長期信心上限設為中。","watch":"Q4 GAAP 營益率是否落在財測 30–31%；FY2027 SBC 占營收是否續升。","evidence_refs":[],"fact_refs":["f_kpi4_sbc_gaap_sbc_146_89m_9_3","f_kpi2_gaap_operating_margin","f_kpi8_guidance_q3_fy2026","f_shares_diluted_m","f_kpi3_free_cash_flow_635m_53m"]},{"view":"價格已反映太多","evidence":"Forward 本益比 38.9 倍、FY2027 為 33.3 倍，PEG 2.2；GAAP trailing 本益比 65 倍。賣方最低目標價 300 美元（Oppenheimer）。","assumption":"市場願意長期為 15% 以上的 EPS 成長付 30 倍以上。","consequence":"即使 EPS 照基本情境走，終端倍數若只有 25 倍，五年後約 420 美元，年報酬約 5%。","ruling":"部分反駁：trailing 本益比與 P/S 在近四個年度端點只在第 42–50 百分位，26 週下跌 3.8%，沒有過熱。但基本情境年報酬約 9%，只屬中等，所以不追價，266 美元以下才加碼。","watch":"股價對 FY2027 共識的本益比；共識修正方向。","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_week26_return_pct","f_consensus_eps_fy2"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 309.09 → 本次 327.89（+6.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=309.09","side_b":"本次 price_at_dd=327.89","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 309.09 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 309.09 美元：Bull 價 691.2、Bear 價 206.8，五年期望值 +46.7%，基準年化 9.5%，不對稱比 3.1","side_b":"本次情境、股價仍用 309.09 美元：Bull 價 738、Bear 價 213.4，五年期望值 +53.8%，基準年化 10.3%，不對稱比 3.74","ruling":"先換情境、股價不動：五年期望值多 7.1 個百分點，基準年化多 0.8 個百分點。不對稱比由 3.1 變為 3.74。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 309.09 美元：五年期望值 +53.8%，基準年化 10.3%，不對稱比 3.74","side_b":"本次情境、股價 327.89 美元：五年期望值 +45.0%，基準年化 9.0%，不對稱比 2.99","ruling":"再換股價、情境不動：起點價上漲 6.1%，五年期望值少 8.8 個百分點，基準年化少 1.3 個百分點，不對稱比由 3.74 降到 2.99。合計五年期望值比前份少 1.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：基本面判斷維持","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：訊號等級 A，估值結論合理偏貴（🟡），陷阱風險低（🟢），護城河方向擴大（↑），五年後跑道寬（🟢），品質複利成長，非循環股。","side_b":"本次全部維持：Q3 營收年增 22%，全年營收財測再上調到年增 21%，EPS 財測上調 0.30 美元到 8.40 美元，在手訂單 82 億美元創新高，經常性營收年增 18%。","ruling":"新證據強化而不是推翻前份判斷，基本面欄位全數不變。估值結論不變，是因為股價上漲 6.1% 與 FY2026 共識 EPS 三個月上修 3.3% 大致抵銷。","evidence_level":"公司揭露（Q3 財報與法說）","settle_metric":"Q4 財報與 FY2027 全年財測","if_then":["若 FY2027 財測與共識相符，且經常性營收有機年增 ≥15%，各欄判斷維持","若經常性營收有機年增 <15%，護城河方向改判持平並停止加碼"],"evidence_refs":["supply_demand_durability#1","end_markets#0"]},{"axis":"前份漂移：情境機率與回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：股價 309.09 美元，多頭 25%、空頭 30%，最大回撤 −50%。","side_b":"本次：股價 327.89 美元（+6.1%），機率維持多頭 25%、基本 45%、空頭 30%，最大回撤區間 −35%～−50%。","ruling":"股價只動 6%，不足以改變情境機率。空頭機率維持 30%，是因為內生成長上界無法驗證，依保守原則不低於 30%。最大回撤下緣仍是 −50%。","evidence_level":"價格資料","settle_metric":"股價對 FY2027 共識本益比","if_then":["若股價跌到 266 美元以下且基本面無損，分批反買，不停損","若股價先漲但 FY2027 財測還沒公布，不追"],"evidence_refs":[]},{"axis":"裁決與角色","cause":"新證據","prior_field":[],"side_a":"前份：進場，角色由矩陣決定。","side_b":"本次加上等待條件：等 2026-11-09 關係企業出口規則暫停期到期的結果，再建倉或加碼。裁決與角色由矩陣依本次輸入重算。","ruling":"如果裁決由進場改為觀望，原因是一週內就有結果的離散監管事件，不是基本面轉弱。結果明朗且財測沒有下修，就恢復進場。","evidence_level":"公司 10-Q 揭露","settle_metric":"BIS 公告與公司全年財測","if_then":["若暫停期延長，或到期後財測沒有下修，恢復建倉","若到期未延長且公司下修財測，維持觀望，空頭機率提高到 35%"],"evidence_refs":["geo_supply_chain#4","reg_tariff_export#2"]},{"axis":"加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"價≤$260（約FY2027本益比27倍）加碼一段；11/9關係企業出口規則到期後EDA未受限且全年財測維持→再加一段","side_b":"11/9 出口規則暫停延長，或到期後未下修全年財測→建倉或加一段；股價≤266 美元（FY2027 共識 27 倍）→再加一段","ruling":"加碼價由 260 美元上移到 266 美元：FY2027 共識 EPS 上修到 9.85 美元，同樣 27 倍對應約 266 美元。出口規則條件由「再加一段」改成建倉的前提，因為規則到期只剩一週，中國營收占比仍未揭露。","evidence_level":"共識與公司揭露","settle_metric":"FY2027 共識 EPS、BIS 公告","if_then":["若 11/9 後財測維持，建倉或加一段","若股價 ≤266 美元且 H1 未削弱，再加碼一段"],"evidence_refs":[]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）。","side_b":"Single Thing：2027 年 2 月公布的 FY2027 全年非 GAAP EPS 財測中點低於 9.20 美元，發生即減碼一半。","ruling":"前份缺唯一致命點，本次補上。選財測而不選出口或司法事件，是因為現價 33 倍 FY2027 本益比對成長能否延續最敏感：財測一轉弱，倍數與 EPS 會同時下修，對五年價值影響最大。出口與緩刑事件機率低，另設清倉條件。","evidence_level":"情境敏感度推導","settle_metric":"FY2027 非 GAAP EPS 財測中點","if_then":["若財測中點 ≥9.20 美元，且經常性營收有機年增 ≥15%，維持","若財測中點 <9.20 美元，減碼一半，空頭機率提高到 40%"],"evidence_refs":[]},{"axis":"停損指標設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標（空值）。","side_b":"經常性營收有機年增連 3 季 <13.5%：減碼三分之一。FY2027 非 GAAP EPS 財測中點 <9.20 美元：減碼一半。非 GAAP 營益率財測中點 <44%：減碼三分之一。核心 EDA 連 6 季 <13.5%：減碼。出現新處分或出口特權受限：清倉。先進製程出現 1 例繞道：減碼一半。","ruling":"前份只有論點漂移條件，沒有對應動作。本次把 H1–H4 的反轉門檻與兩個離散事件，接成減碼與清倉動作；門檻數字沿用各假設的漂移規則。","evidence_level":"方法調整","settle_metric":"各停損指標季度讀數","if_then":["若任一停損指標觸發，依對應動作執行並重跑研究","若四季內都沒有觸發且股價 ≤266 美元，可加碼"],"evidence_refs":[]},{"axis":"H2 營益率門檻","cause":"新證據","prior_field":["H2.threshold"],"side_a":"FY2027 非 GAAP 營業利益率 ≥45%（FY2026 指引中點 44.25%）；連 2 季低於 42.75% 為削弱。","side_b":"FY2027 非 GAAP 營業利益率 ≥45.5%（FY2026 財測中點 44.7%）；連 2 季低於 43.2% 為削弱，減碼三分之一。","ruling":"FY2026 財測中點上移 0.45 個百分點後，舊門檻只要求 0.3 個百分點的擴張，失去鑑別力。CFO 稱扣除 Hexagon 後增量利潤率 54–55%，Hexagon 整合也會在 2027 年改善利潤，所以 45.5% 才算有意義的擴張。","evidence_level":"公司財測","settle_metric":"FY2027 非 GAAP 營業利益率財測中點","if_then":["若財測中點 ≥45.5%，H2 成立","若財測中點 <44%，減碼三分之一"],"evidence_refs":[]},{"axis":"經常性營收成長：Q2 說法與 Q3 數字","cause":"新證據","prior_field":null,"side_a":"Q2 法說（2026-07-27，CFO John Wall）：經常性營收年增約 24%，其中 Hexagon 約 4 個百分點，扣除後為高十幾到 20%。","side_b":"Q3 法說（2026-10-26）：經常性營收年增 18%。CEO 歸因於去年同季中國營收挪動造成的基期效應，沒有說明 18% 是否含 Hexagon；Goldman 分析師點出由 20% 降到 18%。","ruling":"可調和，屬程度差異。基期效應的說法合理但未證，標為未證並監測。若 18% 已含 Hexagon，有機成長約 14%，已低於 H1 門檻 15%。目前無法裁決，要等 2027 年 2 月 Q4 的揭露。","evidence_level":"公司法說口頭說明","settle_metric":"Q4 經常性營收年增與 Hexagon 貢獻拆分","if_then":["若 Q4 扣除 Hexagon 的經常性營收年增 ≥17%，維持 H1 並恢復加碼節奏","若 <15%，停止加碼；連 3 季 <13.5%，減碼三分之一"],"evidence_refs":[]},{"axis":"Q3 GAAP 獲利與管理層說法","cause":"新證據","prior_field":null,"side_a":"Q3 法說 CFO：每項關鍵財務指標都超過財測。","side_b":"Q3 GAAP 營益率 26.2%、GAAP EPS 1.05 美元，低於 Q2 時給的 Q3 財測 27.5–28.5% 與 1.11–1.17 美元；非 GAAP 營益率 44.1%、EPS 2.11 美元則在區間內或之上。CFO 只說 G&A 因年度捐贈提前到 Q3。","ruling":"可調和：管理層所說的關鍵指標是非 GAAP。捐贈時點的說法不採信也不否定，標為未證並監測。GAAP 與非 GAAP 營益率的差距由 Q2 的 17.1 個百分點擴大到 17.9 個百分點。","evidence_level":"公司財報數字對公司財測","settle_metric":"Q4 GAAP 營益率對財測 30–31%","if_then":["若 Q4 GAAP 營益率 ≥30%，視為一次性，結案","若 Q4 GAAP 營益率 <29%，認定差距結構性擴大，品質分下修一級並停止加碼"],"evidence_refs":[]},{"axis":"硬體供給說法前後不一","cause":"新證據","prior_field":null,"side_a":"Q2 法說 CFO：硬體仍受供給限制，而非需求限制。10-K：部分硬體零組件依賴單一或少數供應商。","side_b":"Q3 法說 CFO：沒有產能或供應鏈限制，存貨增加是為了消化在手訂單。","ruling":"可調和：一季之內由受限轉為不受限，可能是備貨到位。但單一供應商的結構沒有變，說法轉變本身也提示上一季的硬體認列有時點因素。仍以 2026 年硬體創年度紀錄為基準，不調整情境。","evidence_level":"公司法說與 10-K","settle_metric":"Q4 硬體營收是否續創紀錄、存貨是否回落","if_then":["若 Q4 硬體創紀錄且存貨回落，結案","若硬體營收連 2 季年減，或公司再提供給受限，停止加碼"],"evidence_refs":["geo_supply_chain#1"]},{"axis":"agent 層競爭：份額說法對對手目標","cause":"新證據","prior_field":null,"side_a":"Q3 法說 CEO：幾乎所有業務區塊都在拿份額，競爭地位前所未有地強；只有 Cadence 同時掌握模型、agent 與引擎三層。","side_b":"BofA 分析師在 Q3 法說轉述對手目標：成長由中十幾%複合到 30%，營益率 50%，權利金模式未來幾年增加約 10 億美元營收；對手也推出與 OpenAI 合作的專用模型。Futurum 認為三家都在 NVIDIA 架構上朝同一方向走。COUPE 共封裝光學方面，Cadence 尚未揭露支援。","ruling":"可調和：市場擴張期兩家可以同時成長。份額說法是公司自述，沒有第三方份額數字；agent 層的差異化未證。護城河方向仍判擴大，此項列為中期風險。","evidence_level":"公司自述對分析師轉述與第三方研究","settle_metric":"核心 EDA 年增；agent 營收揭露","if_then":["若核心 EDA 連 4 季低於 14.25%，護城河方向改判持平","若 2027 年台積電技術論壇前仍沒有 COUPE 支援，停止加碼"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#3"]},{"axis":"大模型繞過商用 EDA","cause":"新證據","prior_field":null,"side_a":"2026-07-17 報導：Kimi K3 用開源 EDA 工具，48 小時自主完成 45 奈米晶片設計，沒有用到 Cadence 或 Synopsys 的授權軟體；CDNS 當日跌 9.6%。","side_b":"同篇報導引述分析師：45 奈米落後 3 奈米、2 奈米好幾代。Cadence 支援台積電 N3、N2、A16、A14。Q2 法說 CEO 稱該示範仍需要 EDA 工具，會被商品化的是大模型選擇，不是 EDA。","ruling":"可調和：示範停在成熟製程，先進製程簽核並未被繞過。以 H4 為裁決依據，出現 7 奈米以下量產繞道才改判。","evidence_level":"媒體報導與公司說法","settle_metric":"前十大晶片設計公司是否在 7 奈米以下以非商用流程量產投片","if_then":["若出現 1 例，減碼一半並重跑研究","若到 2028 年仍沒有先進製程案例，威脅降為觀察"],"evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"axis":"現在就賣與現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就賣：FY2026 本益比 39 倍、PEG 2.2；經常性營收由 20% 降到 18%，口徑不明；Q3 GAAP 低於財測；11/9 出口規則即將到期，中國營收占比未揭露；三家 agent 趨同，對手要做到 50% 營益率；賣方最低目標價 300 美元。","side_b":"現在就買：全年財測連兩季上調到年增 21%、EPS 8.40 美元；在手訂單 82 億美元；續約低點年仍有分析師估約 26% 的訂單成長；agent 用量型營收不在財測內；26 週股價下跌 3.8%，倍數在自身四年區間中段。","ruling":"不賣也不追。基本面支持持有，但基本情境年報酬約 9% 只屬中等，不值得在一週後就有結果的監管事件之前加碼。等 11/9 結果，或股價到 266 美元以下。","evidence_level":"綜合","settle_metric":"11/9 規則結果與 Q4 財測","if_then":["若 11/9 後財測維持，建倉或加一段","若股價跌破 266 美元而基本面無損，分批反買"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"BIS 關係企業出口規則的一年暫停期到期，看是否延長，以及公司是否下修財測","type":"風險","maps_to":"R1","metric":"BIS 公告、公司 8-K 與全年財測","threshold":"暫停未延長，且全年財測下修或公司揭露影響","action":"停止加碼；全年營收影響超過 2% 則減碼三分之一","source_freq":"事件型","date":"2026-11-09","evidence_refs":["geo_supply_chain#4","reg_tariff_export#2","geo_supply_chain#2","geo_supply_chain#3","reg_tariff_export#4","end_markets#7"]},{"n":2,"text":"出口規則結果明朗且財測未下修，建倉或加一段","type":"加碼","maps_to":"R1","metric":"BIS 公告與公司財測","threshold":"暫停期延長，或到期後至 Q4 財報前公司未下修全年財測","action":"建倉或加一段（分批第一段）","source_freq":"事件型","date":"2026-11-09"},{"n":3,"text":"股價回到 FY2027 共識 27 倍","type":"估值rearm","maps_to":"H1","metric":"股價對 FY2027 共識 EPS 9.85 美元","threshold":"股價 ≤266 美元，且 H1 未削弱","action":"加碼一段","source_freq":"每日","date":null},{"n":4,"text":"FY2027 全年非 GAAP EPS 財測中點低於 9.20 美元","type":"Single Thing","maps_to":"H1","metric":"FY2027 非 GAAP EPS 財測中點","threshold":"<9.20 美元","action":"減碼一半，停止加碼並重跑研究","source_freq":"年度（Q4 財報）","date":"2027-02"},{"n":5,"text":"Q4 揭露扣除 Hexagon 的經常性營收年增","type":"假設驗證","maps_to":"H1","metric":"經常性營收有機年增","threshold":"<15% 停止加碼；連 3 季 <13.5% 減碼三分之一","action":"停止加碼","source_freq":"每季","date":"2027-02"},{"n":6,"text":"非 GAAP 營業利益率擴張失速","type":"減碼","maps_to":"H2","metric":"FY2027 非 GAAP 營業利益率財測中點與季度實績","threshold":"財測中點 <44%，或連 2 季 <43.2%","action":"減碼三分之一","source_freq":"每季","date":"2027-02"},{"n":7,"text":"Q4 GAAP 營業利益率能否回到財測區間","type":"假設驗證","maps_to":"R7","metric":"Q4 GAAP 營業利益率","threshold":"<29% 視為 GAAP 差距結構性擴大","action":"停止加碼","source_freq":"每季","date":"2027-02"},{"n":8,"text":"核心 EDA 成長失速","type":"減碼","maps_to":"H3","metric":"核心 EDA 年增","threshold":"連 6 季 <13.5%","action":"減碼三分之一","source_freq":"每季","date":null},{"n":9,"text":"違反認罪協議、行政和解或緩刑義務而遭到新處分","type":"清倉","maps_to":"R2","metric":"DOJ 與 BIS 公告、8-K 法律程序","threshold":"任一新處分或出口特權受限","action":"清倉","source_freq":"事件型","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","reg_tariff_export#0","geo_supply_chain#5","major_events#2","lawsuit_class_action#0"]},{"n":10,"text":"先進製程出現繞過商用簽核的量產投片","type":"風險","maps_to":"R3","metric":"7 奈米以下以非商用流程量產投片的案例","threshold":"前十大設計公司出現 1 例","action":"減碼一半並重跑研究","source_freq":"年度","date":null,"evidence_refs":["substitute_technology#0"]},{"n":11,"text":"硬體供給或需求轉弱","type":"風險","maps_to":"R5","metric":"硬體營收年增、公司供給說法","threshold":"硬體營收連 2 季年減，或公司再提供給受限","action":"停止加碼","source_freq":"每季","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":12,"text":"共封裝光學設計工具落後","type":"風險","maps_to":"R4","metric":"COUPE 支援揭露","threshold":"2027 年台積電技術論壇前仍未宣布支援","action":"停止加碼","source_freq":"年度","date":"2027-04","evidence_refs":["substitute_technology#3"]},{"n":13,"text":"Q4 財報與 FY2027 財測公布後重跑研究","type":"複審日期","maps_to":null,"metric":"全年財測、經常性營收、在手訂單","threshold":"財報公布","action":"重跑研究","source_freq":"年度","date":"2027-02"}],"kill_metrics":[{"metric":"經常性營收有機年增（扣除 Hexagon）","bear_threshold":"連 3 季 <13.5%","window":"每季，2026Q4 起","source":"CFO commentary、季度法說","last_status":"warning"},{"metric":"FY2027 非 GAAP EPS 財測中點","bear_threshold":"<9.20 美元","window":"2027-02 Q4 財報","source":"Q4 新聞稿與 CFO commentary","last_status":"unknown"},{"metric":"非 GAAP 營業利益率","bear_threshold":"FY2027 財測中點 <44%，或連 2 季 <43.2%","window":"每季，2027 年","source":"CFO commentary","last_status":"ok"},{"metric":"核心 EDA 年增","bear_threshold":"連 6 季 <13.5%","window":"每季，2026Q4–2028Q1","source":"季度法說","last_status":"ok"},{"metric":"DOJ 與 BIS 對認罪協議、和解或緩刑義務的新處分","bear_threshold":"任一新處分或出口特權受限","window":"持有期間持續","source":"DOJ 與 BIS 公告、8-K、10-Q 法律程序","last_status":"ok"},{"metric":"7 奈米以下以非商用流程量產投片的案例","bear_threshold":"前十大設計公司出現 1 例","window":"每年檢核，至 2031 年","source":"台積電技術論壇、產業新聞、法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原10)","pacing":[],"holding_cap":null,"requires_critic":[],"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 7 月開源模型在 45 奈米完成整套設計的示範，外推成 EDA 會被大模型取代（當日跌 9.6%，26 週下跌 3.8%）。但先進製程仍綁在商用簽核上，agent 反而增加底層工具呼叫：經常性營收年增由 11% 升到 18%，全年財測連兩季上調。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟢', val='🟡', moat_trend='↑', week26=-3.83, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":true,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row10 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2026-11-09 關係企業出口規則暫停期到期的結果：暫停延長，或到期後公司未下修全年財測，再建倉或加一段；股價若先跌到 266 美元以下，就不必等。'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但判斷者宣告 wait_for_price：不得把觀望承繼回進場（只往保守方向）","hit":false,"basis":"wait_for_price=True, prior_verdict='進場', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"rearm_trigger":"11/9 出口規則暫停延長，或到期後未下修全年財測→建倉或加一段；股價≤266 美元（FY2027 共識 27 倍）→再加一段","exec_line":"現價 327.89 美元不追。11/9 出口規則結果明朗且財測未下修，才建倉或加一段；266 美元以下再加一段。FY2027 非 GAAP EPS 財測中點低於 9.20 美元，減碼一半。緩刑或出口特權遭處分，清倉。"},"reasoning":{"industry":"收錢方式：軟體按三年續約週期授權、按期認列；CFO 在 Q2 法說稱全年約 80% 經常性、20% 前置認列，硬體與部分 IP 一次認列。分部營收占比事實表未涵蓋，只有成長率：Q3 核心 EDA 年增 20%、IP 24%、系統設計與分析 30%（Q2 分別為 18%、逾 40%、37%）。最新一季為 Q3（2026-10-26 法說）：營收 16.33 億美元，年增 22%；非 GAAP 營益率 44.1%，GAAP 26.2%；TTM 毛利率 85.7%。客戶端沒有集中風險：無單一客戶占營收或應收 10% 以上，系統公司約占營收 45%。單點依賴在硬體端：10-K 寫明部分硬體零組件只有單一或少數供應商。供需判斷為結構性持久：CEO 稱設計活動為歷來最強，並轉述台積電預估五年內晶片尺寸增 48 倍，硬體驗證需求隨設計尺寸放大。週期性的部分只在硬體與 IP 的季度起伏。產業態勢是雙向拉鋸。一邊是結構轉好：系統公司自研晶片，AI 推高設計複雜度。另一邊是競爭加劇：三家同時推 agent，對手宣示營益率 50% 與權利金模式。此外還有其他結構變數，包括中國出口管制與開源工具替代。","moat":"機制是轉換成本加上晶圓廠製程認證：先進製程的實作、簽核與 PDK 綁在一起，換供應商等於整套流程重驗。方向證據有四項。第一，經常性營收年增由 2025 年的 11% 升到 Q3 的 18%。第二，Q3 新增 16 個數位全流程案。第三，類比、PCB、多體動力學都有競爭替換案。第四，台積電 N3、N2、A16、A14 四個製程全數支援，是三家中跨度最廣。同業對照只有利潤率：CDNS 營益率 29.6%、SNPS 11.0%，毛利率 85.7% 對 72.4%。但 FCF 利潤率 28.7% 對 29.2%，幾乎持平；SNPS 帳面營益率偏低多半來自併購攤銷，不能當成 ROIC 差距擴大的證據。自身毛利率由 FY2022 的 89.6% 降到 TTM 85.7%，主因是硬體與 IP 占比上升及併購，看不出定價轉弱，但要追蹤。威脅在 agent 層：三家都在 NVIDIA 架構上推 agent，對手與 OpenAI 合作專用模型；開源工具加大模型已能在 45 奈米完成整套設計。執行力 9 分，方向擴大；定價力 8 分，方向穩定。整體趨勢判為擴大。","growth":"成長拆解：以量為主，包括設計案數、晶片尺寸、系統公司自研晶片；agent 加購與用量次之。2026 年 21% 的營收成長中，Hexagon 約占 3 個百分點（約 1.6 億美元÷FY2025 營收 52.97 億美元）。淨回購對股數幾乎沒有貢獻。共識 EPS：FY2026E 8.42 美元、FY2027E 9.85 美元、FY2028E 11.60 美元，兩年複合 17.4%。FY2025 非 GAAP 實績事實表未涵蓋，所以算不出三年。同期共識營收 FY2026 到 FY2027 增 14.4%，EPS 比營收快約 2.6 個百分點，可用 54–55% 的增量利潤率解釋。內生上界以增量 ROIC×再投資率算不出，因為投入資本與 D&A 事實表未涵蓋；而且成長靠費用化研發，公式本身會低估。共識成長超出公式上界的部分，歸因於營益率擴張與費用化研發，不需要倍數上調。跑道：EDA 只占客戶研發預算約 11–12%；系統公司占營收 45% 且仍在增加；agent 用量型營收沒有計入財測。這算是公司已揭露的第二條曲線，但營收尚未揭露，仍屬早期證據。","governance":"自由現金流轉換率高：FCF÷淨利 FY2022–FY2025 分別約 1.32、1.20、1.06、1.43（事實表 financial_history，yfinance 年度財報）；Q2 FCF 5.82 億美元，占營收 36.7%。SBC 占營收 9.3%、占 GAAP 營業利益 32.6%，回購主要用來抵銷稀釋。以淨利÷稀釋 EPS 推算，稀釋股數由 FY2022 約 274.7 百萬降到 FY2025 約 273.1 百萬；目前 274.4 百萬，含 Hexagon 三成的股票對價。現金去向：2026 年回購逾 FCF 五成（Q2 2 億美元、Q3 4 億美元），10/23 董事會再授權 25 億美元；Hexagon 約 27 億歐元，其中七成付現。資產負債表：Q3 現金 14.52 億美元，債務本金 26.5 億美元，淨負債約 12.7 億美元；相對年營運現金流約 20 億美元，負擔輕。計分結果：併購已實現 ROIIC 不過，回購收益率不過，SBC 淨稀釋過。近三年現金去向四分、債務到期與利率、回購均價，事實表皆未涵蓋。","valuation":"現價 327.89 美元，是 FY2026 共識 EPS 8.42 美元的 38.9 倍、FY2027 共識 9.85 美元的 33.3 倍。FY2026 到 FY2028 共識 EPS 年複合 17.4%，PEG 2.2。要讓現價成立，EPS 五年需年增約 15%，終端本益比仍要有 30 倍，才有約 9% 年報酬。我相信 EPS 那一半：全年財測連兩季上調，在手訂單 82 億美元。我不信倍數會停在 39 倍。自身歷史只有四個年度端點可比：trailing 本益比 65.2 倍落在第 49.6 百分位，P/S 14.7 倍在第 41.8 百分位，都在中段。賣方目標價均值約 413 美元，區間 300–450 美元；現價比均值低 21%，支持持有，不支持追價。同業本益比事實表未涵蓋，終端倍數沒有同業錨，只能以自身 FY2027 的 33 倍為上緣參考。","premortem":"最大回撤區間 −35%～−50%。空頭終點是 FY2031E EPS 9.7 美元×22 倍，約 213 美元（−35%）。路徑上若 FY2027 財測轉弱，Forward 本益比由 38.9 倍壓到 22 倍，EPS 再下修一成，跌幅約 −49%。成長熄火壓力測試假設 FY2028 後成長率降到 15%、10%、5%，對應 30、22、16 倍；三種情境只有第一種高於現價，結果分別約 +22%、−14%、−41%。7 月開源模型事件單日跌 9.6%，顯示 AI 替代敘事會造成急跌。陷阱風險低：十類衰退訊號沒有一類確認亮燈，風險在估值與離散監管事件，不在基本面衰退。"},"plain":{"six":{"how_it_makes_money":"Cadence 向晶片公司與系統公司收三筆錢：EDA 軟體授權、IP 授權、模擬驗證硬體。錢卡在先進製程的設計實作、簽核與驗證這一節點。營收約八成是經常性，產業處於擴張期。","moat":"護城河在擴大。先進製程簽核與硬體驗證的轉換成本加深，agent 疊在自家引擎上推高用量。威脅集中在 agent 層：三家趨同，加上開源工具搭配大模型在成熟製程繞道。","growth":"成長跑道寬。agent 帶動底層工具用量，加上系統公司自研晶片，構成第二條曲線；但目前只有公司自述，營收尚未揭露。","capital":"資本配置中等。現金轉換率高、股數四年持平；但回購是在 39 倍本益比買進，收益率低，實質上只是抵銷 SBC。Hexagon 首年獲利貢獻接近零。","valuation":"現價要求 EPS 五年年增約 15%，且終端仍有 30 倍本益比，才換得約 9% 年報酬。我相信獲利成長那一半，不信倍數會停在 39 倍。結論是合理偏貴，不追價。","how_wrong":"最可能看錯在兩處。其一，2026 年 21% 成長裡有 Hexagon 與硬體的一次性成分；有機經常性成長若回到 14% 左右，39 倍本益比撐不住。其二，11/9 出口規則與緩刑義務是兩個離散風險。"}},"decision_inputs":{"signal":"A","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 7 月開源模型在 45 奈米完成整套設計的示範，外推成 EDA 會被大模型取代（當日跌 9.6%，26 週下跌 3.8%）。但先進製程仍綁在商用簽核上，agent 反而增加底層工具呼叫：經常性營收年增由 11% 升到 18%，全年財測連兩季上調。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"進場","prior_role":"衛星","wait_for_price":true,"wait_for_price_condition":"等 2026-11-09 關係企業出口規則暫停期到期的結果：暫停延長，或到期後公司未下修全年財測，再建倉或加一段；股價若先跌到 266 美元以下，就不必等。","trap":"🟢","val":"🟡","moat":"A","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":327.89,"week26_return_pct":-3.83,"consensus_rev_3m_pct":3.31,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母用非 GAAP EPS。GAAP 與非 GAAP 差距大（Q3 GAAP EPS 1.05 美元，非 GAAP 2.11 美元），主因是 SBC 與併購攤銷，屬經常性費用，不是一次性項目。本文以非 GAAP 共識為錨，GAAP 本益比 65 倍另列參考。"},"catalysts":[{"date":"2026-11-09","date_precision":null,"type":"regulatory","event":"BIS 關係企業出口規則一年暫停期到期","impact":"高","watch":"是否延長；公司是否調整全年財測或揭露影響"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 FY2027 全年財測","impact":"高","watch":"非 GAAP EPS 財測中點是否 ≥9.20 美元；扣除 Hexagon 的經常性營收年增"},{"date":"2027-04","date_precision":"month","type":"product","event":"台積電技術論壇","impact":"中","watch":"COUPE 共封裝光學與 A14 的支援進度"}],"_projected_from":"v19"}
```
