你是 stock-analyst v20 的**散文層（prose）agent**，標的 MA（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MA　日期：2026-11-02　archetype：None　前份裁決：2026-07-03　進場｜核心持倉　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1816B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（417B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1080B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1568B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1403B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（516B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1089B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2204B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4451B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3148B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1816           3629-5184      5 條（2–6 內）  
s3                  8000         417           5308-7583      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4051          7664-10949      5 條（2–6 內）  
s6                 11000         516          7339-10484      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1089           1688-2411      3 條（2–6 內）  
s10                 5000        2204           1957-2796      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3148           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5245B；至少需散文≈39.76KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−46%
−45%
−45
−30%
−30
−29%
−2%
0
0.1
0.13%
0.16
0.18
0.3
0.55
0.55%
0.75
0.94%
0.97
1
01
1%
1.06
1.10
1.25%
1.5%
1.7%
1.73
1.9%
2.0
2%
2
02
2.02
2.3
2.4
2.5
3%
3
03
3.04
3.1
3.2%
3.4
3.6
3.7
3.7%
04
4
4%
5%
5
5.25
5.3
5.31
5.5
6
06
6%
6.3%
6.48
6.8%
7%
07
7.0
7
7.62
8%
08
8
9
9%
9.5
9.6%
9.9%
10
10%
10.45%
11%
11
11.4
11.41
11.7%
12
12%
12.2%
12.35%
12.5
12.5%
12.9%
13.0%
13%
13
13.2%
13.3%
13.5%
13.8%
14%
14
14.25%
15%
15.3
15.9
15.9%
16%
16.4%
16.52
17%
17
17.4%
17.7%
18%
18
18.3%
18.5%
19%
19.8%
20
20%
20.04
20.3
20.5%
20.9
21%
21.2
21.8
22
22.7
22.8
23
23.13
23.5
23.7
24
25%
25
26
26.2
26.5
26.94
27
27.58
27.6
28
29%
29
29.18
30%
30
31
31.5
31.8
31.84
32
33
33.4
33.6
34
35%
36
36%
36.8
37
37.3
38
40%
40
40.6
41%
41.6
42
42.5%
43.5%
44.9%
45.0%
45%
45
45.8%
47.8%
49
50%
50.4
52
57
57.2%
58%
59.5%
59.8%
60%
60.07%
60.1%
60.5%
65.6%
69.7%
70%
70
75.0%
76.3%
77.9%
78.4%
81%
90
98%
98.07
99.3
100%
100
104
107.18
113.34
134.7
149.7
150%
155
195
250
345
405
441
450
451
456
530
539
539.39
540
580
624
631
638.01
640
660
765
789
1000
1147
2022
2023
2024
2025
2026
2027
2028
2031
5558
20261102
1,302
1,310
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
{"meta":{"ticker":"MA","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Mastercard Incorporated"},"oneliner":"卡網路量價與加值服務雙引擎仍穩（Q3淨營收+14%、調整後EPS+21%），但半年漲29%後本益比約32倍、五年年化只剩約10%；美國強制信用卡路由立法是最大單一風險，不追，等580美元以下","thesis":{"H":[{"id":"H1","text":"雙寡頭卡網路的量價引擎延續：交易量穩定成長，評估費成長持續高於量","2y":"本幣GDV≥+7%、交易筆數≥+9%、國內評估費成長減GDV成長≥3pp","5y":"淨營收（匯率中性）年複合≥11%，淨收費率不下滑","10y":"A2A與穩定幣占MA可及流量低於5%","threshold":"Q3 2026：GDV+7%、交易筆數+9%、國內評估費+13%（差6pp）","source":"季度財報新聞稿與法說簡報（3Q26，2026-10-29）","drift_rule":"5年假設：淨營收TTM成長連4季比11%低5%以上（低於10.45%）削弱，連6季低10%以上（低於9.9%）反轉"},{"id":"H2","text":"加值服務成為第二引擎：安全、數據、代幣化與代理式商務帶動加值服務成長高於整體","2y":"加值服務淨營收（匯率中性）≥+15%","5y":"加值服務占淨營收≥45%（Q3約41%）","10y":null,"threshold":"Q3 2026：加值服務40.6億美元、+19%；前九個月113.34億美元、+20%","source":"3Q26財報新聞稿、10-Q；Q2法說（約60%與網路量連動）","drift_rule":"5年假設：加值服務TTM成長連4季低於14.25%削弱，連6季低於13.5%反轉（沿用前份15%基準）"},{"id":"H3","text":"營運槓桿加回購：調整後營益率守住58%以上，EPS年增≥13%","2y":"2027年調整後EPS≥22.7美元（共識23.13美元的98%）、調整後營益率≥58%","5y":null,"10y":null,"threshold":"Q3 2026：調整後營益率60.5%、調整後EPS 5.31美元（+21%，回購貢獻0.16美元）","source":"季度財報新聞稿、2027年度財測（2027-01法說）","drift_rule":"2年假設：EPS年增連2季比13%低5%以上（低於12.35%）削弱，連3季低10%以上（低於11.7%）反轉"}],"R":[{"id":"R1","text":"跨境放緩：歐洲內部跨境降溫、中東衝突壓抑旅遊、委內瑞拉一次性因素退去，關稅與制裁等貿易政策壓抑消費與企業支出","h_ref":"H1","clock":"⚡","threshold":"跨境量成長（本幣）連2季低於8%→減碼至原倉位三分之二（沿用前份門檻）","evidence_refs":["geo_supply_chain#0","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R2","text":"監管與訴訟：DOJ對美國簽帳卡業務發調查令、信用卡競爭法案2026-01重提、商家和解平均交換費降0.1pp五年且標準信用卡費率上限1.25%八年；英國集體訴訟逾10億英鎊、美國EMV集體訴訟主張逾10億美元，反壟斷敗訴可能三倍賠償","h_ref":"H1","clock":"🔥","threshold":"DOJ轉正式起訴→減碼三分之一；法案通過任一院→減碼至原倉位三分之二；單一訴訟判決或和解超過20億美元→重跑DD","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#1"]},{"id":"R3","text":"繞卡替代：A2A即時支付、金融科技內部轉帳、穩定幣與加密原生業者，以及代理式商務若改走帳戶直付","h_ref":"H1","clock":"🐢","threshold":"A2A與穩定幣占MA可及流量≥5%、Capital One信用卡轉Discover網路超過20%、或國內評估費成長連4季低於GDV成長（沿用前份三門檻，前兩項資料缺口）；機率≥50%才砍倉","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","customer_second_source#1","channel_business_model_shift#1","competitive_share_entrants#0"]},{"id":"R4","text":"發卡行議價與客戶流失：前五大客戶占2025年淨營收21%、多數關係非排他、部分客戶與對手近乎排他；Lloyds約1000萬張卡轉Visa、Capital One簽帳卡移出；回扣與誘因+18%快於淨營收","h_ref":"H3","clock":"🔥","threshold":"回扣與誘因占總評估費比率年增超過2pp連2季，或任一前五大客戶宣布主要卡組合轉網路→停止加碼；連4季→減碼三分之一","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","customer_second_source#0","customer_second_source#2","competitive_share_entrants#1"]}],"single_thing":{"description":"美國立法強制大型發卡行的信用卡支援第二家非關聯網路路由（信用卡競爭法案，2026-01重新提出）","why_fatal":"美國是最大市場，美國信用卡GDV Q3+10%是增量主力；強制路由把選網路的權力交給收單與商店端，直接壓網路評估費，同時坐實社會容忍度上限，本益比會一起下修——EPS與倍數雙殺。失去一家前五大客戶平均約影響4%營收、英國與EMV訴訟是10億級一次性金額，都小於它","if_happens":"通過任一院減碼至原倉位三分之二；簽署成法減碼至半倉、空頭機率上調到40%以上並重跑DD；涵蓋全部發卡行且無過渡期則清倉","how_monitor":"國會表決與行政部門表態（每月）；季報美國信用卡GDV成長與國內評估費減GDV差距","probability":"約15%（12–24個月）：過去多次重提未過，但2026-01再提且參議員公開批評商家和解不足"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"高","fpe_fy2":27.58,"peg_fy2":1.73,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":16.52,"FY2026E":20.04,"FY2027E":23.13,"FY2028E":26.94},"fy_end_month":12,"eps_basis":"FY2025A為GAAP稀釋EPS（年度財報，調整後口徑事實表未涵蓋）；FY2026E至FY2028E為Koyfin共識（快照未標口徑，推定為調整後）；兩者口徑可能不同，三年年複合約17.7%可能偏高，以前瞻兩年共識年增約15.9%為準"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"雙邊網路收費、資產輕、營益率約60%、FCF高於淨利、EPS年增15%以上且持續回購"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：受理點上半年年增20%、店內非接觸占81%、過去12個月淨增逾2.3億張卡（Q2與Q3法說）；週期性部分主要是跨境旅遊","bargaining":{"up":"事實表未涵蓋供應商集中度；前九個月資本支出11.41億美元、只占FCF約11%，上游投入規模小","down":"發卡行議價最強：前五大客戶占2025年淨營收21%、多數關係非排他、回扣與誘因+18%；商店端以訴訟與立法施壓（和解費率上限、信用卡競爭法案）","geo":"印度、巴西的政府主導A2A壓縮國內卡片份額；中國正擴大發卡與受理；中東衝突壓抑跨境旅遊"},"profit_pool_dir":"利潤池往加值服務（安全、代幣化、數據）與跨境移動；國內網路費受監管上限與A2A夾擊","tam_table":{"expanded":false,"reason":"事實表未涵蓋全球消費支出的卡片滲透率與利潤池占比；本案成長承重在已揭露的量價與加值服務成長率，不靠TAM外推"}},"moat":{"mechanism":"雙邊網路效應：38億張卡×逾2億受理點，加上代幣化、詐欺偵測與加值服務綁定發卡行；與Visa雙寡頭共享","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價：Q3國內評估費比GDV多成長6pp、跨境多5pp→擴大；執行：美國簽帳卡因Capital One轉移只+1%、2025年美國購買量MA+6.3%對Visa+6.8%、Lloyds約1000萬張卡轉Visa，對上Pinnacle、HDFC、德國與北歐續約→穩定；監管上限與回扣誘因+18%壓住定價延續性→綜合穩定","peer_na_reason":"同業ROIC事實表未涵蓋，以營益率與FCF利潤率代替；AXP、COF為發卡銀行，利潤率口徑不可直接比","threats":[{"level":"🟡","text":"Visa點對點搶單：Lloyds約1000萬張卡轉Visa、Capital One簽帳卡移出；部分客戶與對手近乎排他、多數關係非排他，續約時可整包換網路","p":"40%","evidence_refs":["customer_second_source#2","competitive_share_entrants#1","customer_second_source#0"]},{"level":"🔴","text":"A2A即時帳戶支付與金融科技內部轉帳的生態攻擊：10-K自述A2A成熟後國內P2M／P2P份額競爭可能增加、互連後也可能擾動跨境；印度UPI已成規模，MA以在地錢包嵌卡與簽帳卡競爭回應","p":"35%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0","customer_second_source#1","channel_business_model_shift#1"]},{"level":"🟡","text":"穩定幣與加密原生業者：10-K稱可能與產品競爭、新技術可能讓現有技術過時；目前MA以BVNK參與、P2M用途未見量，暫列點狀；若穩定幣商戶結算占可及流量達5%升為生態攻擊","p":"30%","evidence_refs":["substitute_technology#1","substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（持卡人）、決策者（發卡行選網路、商店決定受理）、付款者（商店付手續費、發卡行付評估費）三方都成立：38億張卡、逾2億受理點、受理點上半年+20%、店內非接觸占81%；電子支付是需要不是想要，延後的代價是退回現金"},{"item":"決策層級","level":"🟡","text":"替代發生在發卡行的卡組合層級，不在持卡人：Lloyds約1000萬張卡轉Visa、Capital One簽帳卡移出、Pinnacle 2027年整批轉入MA——多年合約到期時整包換網路；前五大客戶占21%營收，代理變數是續約與回扣條件"},{"item":"價值鏈分配","level":"🟡","text":"和解上限針對的是發卡行的交換費，MA收網路評估費與服務費；但回扣與誘因+18%快於淨營收+14%、Q4占總評估費比率再升，代表發卡行在續約時分走更多；淨營收仍+14%，MA這一節點目前仍最難被取代"},{"item":"社會容忍度","level":"🔴","text":"商家和解平均交換費降0.1pp五年、標準消費信用卡費率上限1.25%八年；信用卡競爭法案2026-01重提、DOJ對簽帳卡發調查令、歐盟資訊請求；評估費每季比量多成長5–6pp，政治上限已在視線內，實際定價上限由社會容忍度決定"}],"roiic":"公式值無意義：2022至2025年淨利由99.3億增至149.7億美元（+50.4億），同期FCF/淨利維持0.97–1.10，新增獲利幾乎不需新增投入資本，增量報酬遠高於資金成本；投入資本口徑事實表未涵蓋，無法給精確數字","reinvest_rate":"約10%：前九個月資本支出11.41億美元（D&A事實表未涵蓋，淨額視為接近零）＋BVNK收購14億美元，對照稅後營業利益約155億美元（2025年營業利益約195億×(1−20.5%)）；其餘FCF以回購與股息配回","endo_ceiling":12.5,"formula_note":"增量報酬×再投資率對資產輕的網路不適用（增量報酬趨近無限、再投資率低），改以有機營運上限代替：量8–9%（購買量、交易筆數皆+9%）＋價格組合約4pp，營益率持平→有機淨營收與營業利益約12–13%，取12.5%，不含回購。稅後營業利益率約47.8%（TTM營益率60.07%×(1−20.5%)），投入資本周轉率未涵蓋，當期ROIC無法算出"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","MA":78.42,"V":79.75,"AXP":null,"COF":null,"PYPL":45.76,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","MA":60.07,"V":65.57,"AXP":null,"COF":null,"PYPL":18.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","MA":42.52,"V":44.91,"AXP":19.82,"COF":45.04,"PYPL":18.37,"unit":"%"},{"metric":"研發密度","MA":null,"V":null,"AXP":null,"COF":null,"PYPL":9.56,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"V","gm":79.75,"om":65.57,"fcf_margin":44.91,"rd_intensity":null,"strategy_note":"最強同業：營益率65.6%比MA高約5.5pp、FCF利潤率44.9%；美國購買量份額約70%，2025年成長6.8%略快於MA，並從MA拿走Lloyds","period":"TTM ending 2026-09-30（4季加總）"},{"name":"AXP","gm":null,"om":null,"fcf_margin":19.82,"rd_intensity":null,"strategy_note":"閉環發卡兼網路，FCF利潤率19.8%（截至2026-06）；爭奪高端消費者，與MA富裕客群（支出成長為整體信用卡2倍）正面重疊","period":"TTM ending 2026-06-30（4季加總）"},{"name":"COF","gm":null,"om":null,"fcf_margin":45.04,"rd_intensity":null,"strategy_note":"併入Discover網路後把簽帳卡從MA移走（美國簽帳卡Q3僅+1%），是美國能垂直整合的大型發卡行；FCF利潤率45.0%屬銀行口徑，不可直接比","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PYPL","gm":45.76,"om":18.52,"fcf_margin":18.37,"rd_intensity":9.56,"strategy_note":"錢包業者，營益率18.5%、毛利率45.8%；多數交易仍跑卡網路，MA稱錢包與先買後付業者最後多選擇合作，屬合作兼競爭","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量約8–9%（購買量、交易筆數各+9%）＋價格與組合約4pp＋加值服務組合上移；回購每年約2–3%墊高EPS（Q3回購貢獻0.16美元）；收購影響極小","runway_years":"事實表未涵蓋卡片滲透率，無法換算達30%滲透率的年數","runway_post_y5":"🟢","endo_ceiling_basis":"有機上限約12.5%（量8–9%＋價格組合約4pp、營益率持平、不含回購）；前瞻兩年共識EPS年增約15.9%，缺口約3.4pp歸因淨回購約2–2.5pp與營益率擴張約1pp，可歸因、非依賴重估","segments":[{"item":"支付網路淨營收（Q3 2026）","value":"約57億美元，+11%：量與定價，已扣回扣與誘因"},{"item":"加值服務淨營收（Q3 2026）","value":"40.6億美元，+19%，約占淨營收41%；前九個月113.34億美元、+20%；約60%與網路量連動"},{"item":"跨境（Q3 2026）","value":"跨境量+11%、跨境評估費+16%；非旅遊線上交易由Q2的20%降到15%，歐洲內部跨境由16%降到10%"}],"decay_signals":[{"item":"毛利率連2季年減","lit":false,"note":"季度毛利率事實表未涵蓋；年度由76.3%升到77.9%"},{"item":"核心市占近12個月縮減","lit":true,"note":"美國簽帳卡因Capital One轉移Q3只+1%；2025年美國購買量MA+6.3%略低於Visa+6.8%；Lloyds約1000萬張卡轉Visa"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"評估費比量多成長5–6pp，交易筆數仍+9%"},{"item":"EPS年複合高於營收年複合逾5pp","lit":false,"note":"2022至2025年GAAP EPS年複合約17.4%、營收約13.8%，差3.6pp"},{"item":"FCF/淨利連2年低於0.75","lit":false,"note":"2024年1.06、2025年1.10"},{"item":"SBC/營收逾5%且逐年上升","lit":false,"note":"前九個月SBC占營業利益3.2%，換算約占營收2%"},{"item":"TAM萎縮或被替代技術壓縮","lit":false,"note":"10-K只是潛在風險敘述；印度、巴西的A2A屬既有格局，未見全球卡片可及流量萎縮的量化證據，改列護城河威脅"},{"item":"估值倍數近3年系統性下移","lit":true,"note":"落後本益比33.4倍、市銷率15.3倍皆為4個年度端點中最低"},{"item":"維持性資本支出占FCF逾60%","lit":false,"note":"前九個月資本支出11.41億美元對FCF 107.18億美元，約11%"},{"item":"停止投資新產能且收入3年內下滑","lit":false,"note":"收入2023至2025年各+12.9%、+12.2%、+16.4%"}],"trap_rating":"價值陷阱風險中、長期成長性中（亮2項）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：管理層稱收購對淨營收影響極小、BVNK基期小；現金去向三年四分資料事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"BVNK於2026-08-03以現金14億美元收購（另有最高3億美元或有對價），管理層稱對加值服務成長影響極小、基期小；收購兩個月，已實現增量報酬無法衡量；更早的收購事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"Q2回購49億、Q3回購30億美元；回購均價事實表未涵蓋，以期間股價約540–640美元對2026年共識EPS 20.04推算盈餘殖利率約3.1–3.7%；10年期殖利率事實表未涵蓋，只要高於1.7%即不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"前九個月SBC 5.25億美元（占營業利益3.2%），年化約7億美元，約為市值5558億美元的0.13%，遠低於每年1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（2026年度共識EPS）＋PEG，輔以2027年度倍數","tier":"支付網路雙寡頭","peers":{"expanded":false,"reason":"事實表同業表只有利潤率、沒有同業前瞻本益比；終端倍數改以自身現值（2027年度共識EPS約27.6倍）與前份判斷記載的5年前瞻本益比區間24–40倍對照"},"fwd_pe":31.84,"peg":2.0,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比31.8倍（2026年度）／27.6倍（2027年度）；PEG約2.0；落後本益比在4個年度端點中最低（5年連續分位事實表未涵蓋，不以此代替）；基本情境5年年化約10%落在8–12%中段→合理（🟡），較前份539美元時空間明顯變窄","upside_short_pct":11,"upside_mid_pct":36},"trap_analysis":{"verdict":"🟡","label":"非價值陷阱，但兩項衰退信號亮燈（美國簽帳卡份額、倍數4年下移）"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"信用卡競爭法案2026-01重提、參議員公開批評商家和解不足；DOJ對簽帳卡業務發調查令；10-K自述A2A成熟後國內P2M／P2P份額競爭可能增加","assumption":"評估費每季比量多成長5–6pp的定價能延續五年","consequence":"美國強制信用卡路由＋衰退＋A2A在歐洲擴張：EPS五年停在約23美元、本益比降到約20倍，股價約450美元（約−29%），深度情境−45%","ruling":"部分採納：列為空頭情境（30%）；不採為基本情境，因Q3量價仍強、法案過去多次未過。與唯一致命點部分重疊（法案是觸發點），本條補上衰退與A2A的共振","watch":"法案表決進度、DOJ動向、國內評估費減GDV差距（每季）","evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#1","substitute_technology#0"],"fact_refs":["f_kpi7_purchase_volume_cross_bo","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"10-K稱穩定幣可能隨GENIUS Act普及並與產品競爭、新技術可能讓現有技術過時；代理式商務目前由處理商以一次性虛擬卡墊在中間，MA表態長期不支援","assumption":"代理式商務與穩定幣最後仍跑卡網路代幣","consequence":"若代理平台改走帳戶直付或穩定幣結算，新增線上流量繞過MA，淨營收成長由低雙位數降到個位數","ruling":"暫不採納：MA已併入BVNK、與OpenAI和Shopify簽約使用Agent Pay，管理層稱代理交易量仍小；但這是十年尺度的架構風險，併入繞卡替代監測","watch":"穩定幣商戶結算占可及流量（資料缺口）、Agent Pay採用方數、管理層是否揭露代理交易量","evidence_refs":["substitute_technology#1","substitute_technology#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"回扣與誘因+18%快於淨營收+14%，Q4占總評估費比率預期再升；前五大客戶占21%營收、多數關係非排他；以30倍以上本益比回購的盈餘殖利率約3%；BVNK收入基期小","assumption":"量價成長能轉成每股價值，而不是被發卡行分走或被高價回購稀釋","consequence":"營收年增12%但淨收費率下降、回購報酬低於資金成本，EPS年增掉到10%以下，股價只跟EPS走，五年年化約6–7%","ruling":"採納為監測：目前淨營收仍+14%、調整後營益率60.5%，尚未發生；以回扣與誘因比率和淨收益率當早期指標","watch":"回扣與誘因占總評估費比率年增超過2pp連2季→停止加碼","evidence_refs":["customer_concentration_credit#0","customer_second_source#0","competitive_share_entrants#1"],"fact_refs":["f_kpi1_adjusted_non_gaap_operat","f_fwd_pe_latest"]},{"view":"價格已反映太多","evidence":"26週漲29%、2026年度前瞻本益比31.8倍；Q3淨營收含服務專案與簽約從Q4提前、Q4定價開始滿年；賣方Q3前平均目標價約660美元只高3%，Raymond James曾下調到631美元","assumption":"市場會繼續給約32倍","consequence":"若一年後倍數回到27倍、EPS照2027年共識，股價約624美元，一年報酬約−2%","ruling":"採納：已持有者續抱不加碼，新資金不追，等580美元以下","watch":"股價對2027年共識EPS倍數、Q4淨營收成長（2027-01公布）","evidence_refs":["capital_markets_pricing#5"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_price_at_dd"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 539.39 → 本次 638.01（+18.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=539.39","side_b":"本次 price_at_dd=638.01","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、均線 ✅→🟡、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、均線 ✅→🟡、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 539.39 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 539.39 美元：Bull 價 1,310、Bear 價 405，五年期望值 +75.0%，基準年化 13.0%，不對稱比 7.0","side_b":"本次情境、股價仍用 539.39 美元：Bull 價 1,302、Bear 價 456，五年期望值 +69.7%，基準年化 13.3%，不對稱比 7.62","ruling":"先換情境、股價不動：五年期望值少 5.3 個百分點，基準年化多 0.3 個百分點。不對稱比由 7.0 變為 7.62。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 539.39 美元：五年期望值 +69.7%，基準年化 13.3%，不對稱比 7.62","side_b":"本次情境、股價 638.01 美元：五年期望值 +43.5%，基準年化 9.6%，不對稱比 3.04","ruling":"再換股價、情境不動：起點價上漲 18.3%，五年期望值少 26.2 個百分點，基準年化少 3.7 個百分點，不對稱比由 7.62 降到 3.04。合計五年期望值比前份少 31.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：整體訊號","cause":"新證據","prior_field":["signal"],"side_a":"前份（2026-07-03，股價539.39美元）：整體訊號A；護城河趨勢↑、陷阱風險低（🟢）、估值合理（🟡）","side_b":"本次（股價638.01美元）：整體訊號B；護城河趨勢→、陷阱風險中（🟡）；估值仍判合理（🟡），但空間變窄","ruling":"整體訊號是基本面評級，這次降級來自新證據，不是價格。①護城河趨勢由↑改→：Q3美國簽帳卡因Capital One轉移只+1%，2025年美國購買量MA+6.3%略低於Visa+6.8%，Lloyds約1000萬張卡轉Visa。②陷阱由🟢改🟡：十類衰退信號亮2項，分別是美國份額縮減與倍數4年下移。③前份只把監管列為Visa連帶，本次納入2026年Q1 10-Q揭露的DOJ對MA簽帳卡業務調查令；另外回扣與誘因+18%，快於淨營收+14%。量價引擎沒壞：Q3淨營收+14%、調整後EPS+21%、全年指引維持，所以只降一級到B，不到C。股價上漲18%只影響估值空間：估值判讀前後都是合理（🟡），基本情境5年年化由約13%降到約10%，價格效果已在上方程式拆解的股價變動一條另列。這是新資金等580美元以下的理由，不是訊號降級的理由。裁決與角色變動由程式另列多欄共同歸因，不併入本條","evidence_level":"硬數據＋第三方統計＋公司申報","settle_metric":"美國購買量成長MA對Visa、美國簽帳卡GDV成長、回扣與誘因占總評估費比率、DOJ程序狀態","if_then":["若2027年上半年美國簽帳卡GDV回到+6%以上、美國購買量成長不低於Visa，且回扣與誘因比率未再升→護城河趨勢可回↑，整體訊號可回A","若再有前五大客戶轉出或DOJ正式起訴→護城河趨勢改↓，整體訊號檢討是否降為C並重跑DD"],"evidence_refs":["customer_second_source#2","competitive_share_entrants#2","customer_second_source#0","regulatory_antitrust#1"]},{"axis":"前份漂移：護城河與陷阱","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河趨勢↑、陷阱風險低（🟢）、五年後跑道寬（🟢）","side_b":"本次：護城河趨勢→、陷阱風險中（🟡）、五年後跑道仍寬（🟢）","ruling":"趨勢由↑改→：Q3美國簽帳卡因Capital One轉移只+1%、2025年美國購買量MA+6.3%略低於Visa+6.8%、Lloyds約1000萬張卡轉Visa，大客戶份額有下滑證據就不能標↑；定價面仍強所以不到↓。陷阱改🟡：十類衰退信號亮2項（美國份額、倍數4年下移）。跑道維持：加值服務+19%、占淨營收約41%，是有財報證據的第二曲線","evidence_level":"硬數據＋第三方統計","settle_metric":"美國購買量成長MA對Visa、美國簽帳卡GDV成長（2026年Q4起Capital One轉移滿年）","if_then":["若2027年上半年美國簽帳卡GDV回到+6%以上且美國購買量成長不低於Visa→趨勢可回↑","若再有前五大客戶轉出→趨勢改↓並重跑DD"],"evidence_refs":["customer_second_source#2","competitive_share_entrants#2","customer_second_source#0"]},{"axis":"前份漂移：情境機率與分類","cause":"方法變動","prior_field":["archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：未標公司類型與循環位置；多頭30%、空頭25%；最大回撤−45%單點","side_b":"本次：品質複利成長、非循環股不標位置；多頭25%、基本45%、空頭30%；最大回撤改為−30%至−45%區間","ruling":"空頭機率上調來自本次加做的再投資報酬檢核：前瞻兩年共識EPS年增約15.9%高於有機上限約12.5%（差額為回購與營益率，可歸因），按框架空頭不得低於30%；另有新證據（法案重提、DOJ調查令）支持不下修。回撤改區間是寫法改變，下緣沿用−45%","evidence_level":"推論","settle_metric":"有機淨營收成長對12.5%","if_then":["若2027年財測有機淨營收成長≥13%且法案未過任一院→空頭機率下修到25%","若有機淨營收成長連2季低於10%→空頭機率上調到35%並下修基本情境"],"evidence_refs":[]},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重啟條件：null（前份為進場，未設）","side_b":"股價回到580美元以下（2027年共識EPS約25倍、基本情境5年年化約12%）才恢復加碼","ruling":"本次結論改為不追，唯一約束是價格，重啟條件就是價格約束的否定；不用事件錨，因生意本身沒有待決證據","evidence_level":"推論","settle_metric":"股價","if_then":["若股價≤580美元且Q4淨營收成長≥11%→分三批加碼","若股價≤580美元但跌因是法案或DOJ起訴→不加碼，依唯一致命點處理"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉／減碼門檻（null）","side_b":"減碼：跨境本幣成長連2季低於8%、DOJ對MA正式起訴、股價≥765美元且共識未上修；清倉：國內評估費成長連4季低於GDV成長且淨營收成長低於8%，或美國強制路由立法涵蓋全部發卡行且無過渡期","ruling":"前份只寫假設門檻、沒寫動作；本次補上具體動作，跨境8%沿用前份削弱門檻，未放寬","evidence_level":"推論","settle_metric":"季報評估費與量","if_then":["若觸發任一減碼條件→減碼三分之一並重跑DD","若觸發清倉條件→清倉"],"evidence_refs":[]},{"axis":"Single Thing","cause":"新證據","prior_field":["single_thing"],"side_a":"前份唯一致命點：未設（null）","side_b":"Single Thing：美國立法強制大型發卡行的信用卡支援第二家非關聯網路路由（信用卡競爭法案）","ruling":"法案在2026-01重新提出，參議員公開批評商家和解不足；它同時壓美國網路費與本益比，是情境樹中單一敏感度最大的二元事件（失去一家前五大客戶平均約影響4%營收，英國與EMV訴訟是10億級一次性金額，都小於它）","evidence_level":"立法紀錄與新聞","settle_metric":"法案表決進度","if_then":["若法案通過任一院→減碼至原倉位三分之二","若簽署成法→減碼至半倉並重跑DD；涵蓋全部發卡行且無過渡期→清倉"],"evidence_refs":["regulatory_antitrust#2"]},{"axis":"監管風險門檻","cause":"新證據","prior_field":["thesis.R2"],"side_a":"前份：V遭強制拆分或重大和解→MA連帶下修向18倍；FTC對MA啟動調查→立即重評","side_b":"本次：DOJ對MA美國簽帳卡業務由調查令轉為正式起訴→減碼三分之一並重跑DD；信用卡競爭法案通過任一院→減碼至原倉位三分之二","ruling":"2026年Q1 10-Q揭露DOJ反壟斷司已對MA簽帳卡業務發出調查令，風險從Visa連帶變成MA直接當事人，門檻改盯MA自己的案子；FTC條件沒有新證據，併入此條","evidence_level":"公司申報","settle_metric":"10-Q法律程序揭露","if_then":["若DOJ正式起訴→減碼三分之一","若調查結案未起訴→回到前份監測強度"],"evidence_refs":["regulatory_antitrust#1"]},{"axis":"假設三撤換","cause":"價格變動","prior_field":["thesis.H3"],"side_a":"前份H3：估值從5年低位修復（前瞻本益比23.7倍，2年內回到5年中段40分位以上）","side_b":"本次撤下，改為營益率與EPS成長假設：股價已漲18%、2026年度前瞻本益比31.8倍，重估大致發生，不能再當報酬來源","ruling":"前份的重估論點已兌現；本次報酬只算EPS複利，終端倍數下修到27倍，所以不是估值依賴型","evidence_level":"硬數據","settle_metric":"股價對2027年共識EPS倍數","if_then":["若倍數回到25倍以下而EPS照共識→重估論點重新成立，分批加碼","若倍數升破33倍→減碼四分之一"],"evidence_refs":[]},{"axis":"Q2指引與Q3實績","cause":null,"prior_field":null,"side_a":"2026-07-30 CFO Sachin Mehra：Q3淨營收成長落在低雙位數高端；Q3回扣與誘因比率略高於Q2；全年落在區間較高處","side_b":"2026-10-29 新任CFO Ling Hai：Q3淨營收+14%高於預期，部分是服務專案與簽約時點從Q4挪到Q3，Q4會回吐；回扣與誘因大致持平、Q4比率預期升高；全年維持低雙位數高端","ruling":"兌現且略優，沒有改口；CFO更替是內部輪調（Mehra轉任商務長），口徑一致。但Q3超額有一部分是時點，Q4淨營收成長落在9–11%不算轉弱，低於9%才算","evidence_level":"管理層原話","settle_metric":"Q4淨營收成長（匯率中性、不含收購），2027-01公布","if_then":["若Q4淨營收成長低於9%→停止加碼並下修基本情境2027年EPS","若Q4≥12%且2027年指引不低於低雙位數高端→維持基本情境"],"evidence_refs":[]},{"axis":"跨境放緩的一次性歸因","cause":null,"prior_field":null,"side_a":"管理層（2026-10-29 Ling Hai）：歐洲內部跨境放緩來自歐盟新海關費、大型促銷時點、去年加密貨幣購買高基期，非結構性；高收益的其他跨境穩定","side_b":"數據：跨境非旅遊線上交易成長由Q2的20%降到15%、歐洲內部跨境由去年同期16%降到10%；Q2跨境強勢含委內瑞拉美元一次性；中東衝突仍壓抑旅遊","ruling":"不採信也不否定，標未證、監測。預先登記：加密高基期過後的2027年Q1，若歐洲內部跨境仍≤10%且整體跨境低於10%，視為歸因證偽，跨境成長假設下修1pp","evidence_level":"管理層原話＋季報數據","settle_metric":"跨境量成長（本幣）、跨境評估費成長","if_then":["若2027年Q1整體跨境低於10%→跨境假設下修1pp、停止加碼","若跨境連2季低於8%→減碼至原倉位三分之二"],"evidence_refs":["geo_supply_chain#0","reg_tariff_export#1"]},{"axis":"定價權與社會容忍度","cause":null,"prior_field":null,"side_a":"Q3國內評估費+13%對GDV+7%、跨境評估費+16%對量+11%：定價與組合每季多貢獻5–6pp；管理層稱依價值定價、Q4起部分定價開始滿年","side_b":"商家和解平均交換費降0.1pp五年、標準消費信用卡費率上限1.25%八年；信用卡競爭法案2026-01重提；DOJ對簽帳卡發調查令；英國集體訴訟逾10億英鎊、美國EMV訴訟主張逾10億美元，反壟斷敗訴可能三倍賠償","ruling":"可調和（程度差異）：和解上限落在發卡行的交換費，不直接碰MA網路費；MA的定價多來自國際、代幣與加值服務。但兩邊疊加會壓縮未來提價空間，所以定價只給8分、社會容忍度給紅燈，空頭機率維持30%","evidence_level":"季報數據＋公司申報","settle_metric":"國內評估費成長減GDV成長","if_then":["若差距連2季低於3pp→停止加碼","若信用卡競爭法案通過任一院→減碼至原倉位三分之二"],"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","end_markets#3"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣：26週漲29%、2026年度前瞻本益比31.8倍；Q3有時點提前、Q4定價開始滿年、回扣與誘因比率升高；法案與DOJ在路上；賣方Q3前平均目標價約660美元只高3%，Raymond James曾下調到631美元","side_b":"續抱：Q3淨營收+14%、EPS+21%、全年指引維持；2026年度共識近3個月上修1.9%；落後本益比33.4倍仍是4個年度端點中最低；基本情境5年年化約10%","ruling":"續抱、不加碼、不賣：賣的理由都是價格與時點，不是生意變差；但價格理由足以停止加碼，新資金等580美元以下","evidence_level":"硬數據","settle_metric":"股價對2027年共識EPS倍數、Q4淨營收成長","if_then":["若股價≥765美元且2027年共識EPS未上修→減碼四分之一","若股價≤580美元且Q4淨營收成長≥11%→分三批加碼"],"evidence_refs":["capital_markets_pricing#5","capital_markets_pricing#0"]},{"axis":"回扣與誘因對不為量而量","cause":null,"prior_field":null,"side_a":"2026-07-30 Sachin Mehra：不為量而量，只追能提高淨收益率的量，舉放棄Lloyds信用卡為例","side_b":"Q3回扣與誘因+18%快於淨營收+14%，Q4占總評估費比率預期再升；新任CFO（2026-10-29）不給回扣指引，改稱淨收益率才是最終指標；外部報導Lloyds約1000萬張卡是轉到Visa","ruling":"目前說法與數字一致：淨營收仍+14%、國內評估費仍快於量。但Lloyds案外部報導寫的是Lloyds與Visa擴大合作，不完全是MA主動放棄，續約成本在升高","evidence_level":"管理層原話＋第三方報導","settle_metric":"回扣與誘因占總評估費比率、淨收益率","if_then":["若比率年增超過2pp連2季→停止加碼","若任一前五大客戶轉出→趨勢改↓並重跑DD"],"evidence_refs":["customer_second_source#2","customer_concentration_credit#0"]}],"triggers":[{"n":1,"text":"國內評估費成長減本幣GDV成長連2季低於3個百分點，代表定價權轉弱","type":"假設驗證","maps_to":"H1","metric":"國內評估費成長−本幣GDV成長","threshold":"連2季低於3pp","action":"停止加碼","source_freq":"季報（每季）","date":null,"evidence_refs":[]},{"n":2,"text":"加值服務成長連4季低於15%","type":"假設驗證","maps_to":"H2","metric":"加值服務淨營收成長（匯率中性）","threshold":"連4季低於15%","action":"停止加碼，基本情境EPS下修","source_freq":"季報（每季）","date":null,"evidence_refs":[]},{"n":3,"text":"跨境量本幣成長連2季低於8%","type":"減碼","maps_to":"R1","metric":"跨境量成長（本幣）","threshold":"連2季低於8%","action":"減碼至原倉位三分之二","source_freq":"季報（每季）","date":null,"evidence_refs":["geo_supply_chain#0","reg_tariff_export#0"]},{"n":4,"text":"DOJ對MA美國簽帳卡業務由調查轉為正式起訴","type":"減碼","maps_to":"R2","metric":"DOJ程序狀態","threshold":"提起正式訴訟","action":"減碼三分之一並重跑DD","source_freq":"8-K、10-Q（事件）","date":null,"evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#0"]},{"n":5,"text":"信用卡競爭法案（強制信用卡第二網路路由）簽署成法","type":"Single Thing","maps_to":"R2","metric":"法案立法進度","threshold":"簽署成法","action":"減碼至半倉並重跑DD；涵蓋全部發卡行且無過渡期則清倉","source_freq":"國會紀錄（每月）","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":6,"text":"回扣與誘因占總評估費比率年增超過2個百分點且連2季，或任一前五大客戶宣布主要卡組合轉網路","type":"風險","maps_to":"R4","metric":"回扣與誘因占總評估費比率；前五大客戶轉換公告","threshold":"年增超過2pp連2季；或一家轉出","action":"停止加碼；連4季則減碼三分之一","source_freq":"季報、新聞稿","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","customer_second_source#2"]},{"n":7,"text":"國內評估費成長連4季低於GDV成長，且淨營收成長低於8%：淨收費率結構性下滑","type":"清倉","maps_to":"R3","metric":"國內評估費成長−GDV成長；淨營收成長（匯率中性）","threshold":"連4季低於0且淨營收低於8%","action":"清倉","source_freq":"季報（每季）","date":null,"evidence_refs":["substitute_technology#0","channel_business_model_shift#1"]},{"n":8,"text":"股價回到580美元以下","type":"估值rearm","maps_to":null,"metric":"股價","threshold":"≤580美元（2027年共識EPS約25倍）","action":"分三批加碼","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":9,"text":"股價升破765美元而2027年共識EPS未上修","type":"減碼","maps_to":null,"metric":"股價對2027年共識EPS倍數","threshold":"≥765美元（約33倍）","action":"減碼四分之一","source_freq":"每日收盤＋共識快照","date":null,"evidence_refs":[]},{"n":10,"text":"Q4財報與2027年度財測","type":"複審日期","maps_to":"H3","metric":"2027年淨營收成長指引、Q4淨營收成長","threshold":"指引低於低雙位數或Q4低於9%→基本情境下修","action":"依財測更新情境樹後重跑DD","source_freq":"法說（每季）","date":"2027-01","evidence_refs":[]},{"n":11,"text":"MA核心網路公開揭露的大範圍服務中斷","type":"風險","maps_to":"H1","metric":"網路中斷時數與影響範圍","threshold":"單次≥4小時且影響多家發卡或收單方","action":"停止加碼至原因揭露","source_freq":"公司公告、發卡與收單方狀態頁（事件）","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":12,"text":"加密高基期過後歐洲內部跨境仍≤10%且整體跨境低於10%","type":"假設驗證","maps_to":"R1","metric":"跨境量成長（本幣）","threshold":"2027年Q1整體低於10%","action":"跨境成長假設下修1pp、停止加碼","source_freq":"季報（每季）","date":"2027-04","evidence_refs":["geo_supply_chain#0"]}],"kill_metrics":[{"metric":"淨營收成長（匯率中性、不含收購）","bear_threshold":"連2季低於9%","window":"2季","source":"季度財報新聞稿","last_status":"ok"},{"metric":"國內評估費成長減本幣GDV成長","bear_threshold":"連2季低於3個百分點；連4季低於0且淨營收低於8%即清倉","window":"2至4季","source":"季度財報新聞稿與法說簡報","last_status":"ok"},{"metric":"跨境量成長（本幣）","bear_threshold":"連2季低於8%（沿用前份）","window":"2季","source":"季度財報新聞稿","last_status":"ok"},{"metric":"加值服務淨營收成長（匯率中性）","bear_threshold":"連4季低於15%（沿用前份）","window":"4季","source":"季度財報新聞稿","last_status":"ok"},{"metric":"回扣與誘因占總評估費比率","bear_threshold":"年增超過2個百分點且連2季","window":"2季","source":"10-Q與法說","last_status":"warning"},{"metric":"A2A與穩定幣占MA可及流量","bear_threshold":"≥5%（沿用前份）","window":"年度","source":"資料缺口：事實表未涵蓋","last_status":"unknown"},{"metric":"Capital One信用卡轉至Discover網路比例","bear_threshold":"超過20%（沿用前份）","window":"年度","source":"資料缺口：事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=29.18, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到580美元以下（2027年共識EPS約25倍、基本情境5年年化約12%）'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"單一個股上限6%","requires_critic":[],"verdict":"觀望","rearm_trigger":"股價回到580美元以下（2027年共識EPS約25倍、基本情境5年年化約12%）","exec_line":"已持有者續抱、不加碼；新資金等580美元以下分三批；破765美元且共識未上修減碼四分之一；美國強制路由立法減至半倉"},"reasoning":{"industry":"賺誰的錢：發卡行與商店為每筆交易付網路評估費（國內、跨境、交易處理），MA另向銀行、商店與企業賣加值服務（詐欺與身分、數據分析、行銷、代幣化、資安）。Q3淨營收98.07億美元，其中支付網路約57億美元（+11%）、加值服務40.6億美元（+19%，約60%與網路量連動）（3Q26財報新聞稿，2026-10-29）；GAAP營益率59.8%、調整後60.5%，TTM毛利率78.4%。錢卡在兩個節點：發卡行選哪個網路（前五大客戶占2025年淨營收21%，單一客戶都不到10%——集中度是風險，不是護城河證據），以及商店受理（逾2億個受理點）。量價：購買量+9%、跨境+11%、交易筆數+9%；國內評估費+13%對GDV+7%。產業時鐘II（擴張）：GDV與交易筆數穩定成長，管理層描述勞動市場平衡、家庭資產負債表強、薪資續增。供需持久性：結構性持久，現金數位化與受理擴張仍在延伸，週期性部分主要是跨境旅遊。產業態勢：雙向拉鋸——結構轉好（受理點上半年+20%、加值服務+19%）對上其他結構變動（監管：和解費率上限、信用卡競爭法案重提、DOJ調查令；替代技術：A2A與穩定幣）。","moat":"機制：雙邊網路（38億張卡×逾2億受理點）加上代幣化、詐欺偵測與加值服務把發卡行綁住，與Visa共享雙寡頭結構租金。方向：定價面Q3國內評估費比GDV多6pp、跨境多5pp、交易處理比筆數多5pp，仍在擴大；執行面贏單（Pinnacle 2027年整批轉入、印度HDFC、德國DSGV與DZ Bank續約、北歐Handelsbanken與Swedbank續約、中國銀行簽帳卡）與失單（Lloyds約1000萬張卡轉Visa、Capital One簽帳卡移出使美國簽帳卡只+1%、2025年美國購買量成長6.3%略低於Visa的6.8%）互抵；加上社會容忍度上限壓住定價延續性，綜合判為穩定（→）。同業比較：TTM營益率60.1%比Visa 65.6%低約5.5pp、FCF利潤率42.5%對44.9%，差距反映Visa的規模份額，兩家吃的是同一塊結構租金；對PayPal（營益率18.5%）等其他支付同業大幅領先。與Visa差距的兩年趨勢事實表未涵蓋，但MA自身營益率2022至2025年由57.2%升到59.5%，沒有證據顯示差距在擴大，因此不另扣分。評分：執行8（美國份額小輸、失單）、定價8（提價仍強但碰到監管上限），等級B；A2A列生態攻擊，扣分後仍不低於7分、等級不變。當期報酬：高利益率×高周轉；稅後營業利益率約47.8%，投入資本口徑事實表未涵蓋。","growth":"成長來源：量（購買量、交易筆數各+9%）＋價與組合（評估費比量多成長5–6pp）＋加值服務（+19%），回購墊高EPS（Q3回購貢獻0.16美元，約3%），收購影響極小。共識EPS：2026年20.04、2027年23.13、2028年26.94美元（Koyfin快照，家數未標；營收共識34位），前瞻兩年年增約15.9%；若以2025年GAAP稀釋EPS 16.52美元為基期，三年約17.7%，但基期與共識口徑可能不同，以前者為準。再投資報酬檢核的有機上限約12.5%（不含回購），缺口約3.4pp：淨回購約2–2.5pp、營益率擴張約1pp（Q3營業利益+15%對淨營收+14%），可歸因，不依賴重估。跑道：卡片滲透率事實表未涵蓋，無法換算年數；但第二曲線有財報證據——加值服務占淨營收約41%、前九個月+20%，另有商務虛擬卡、代理式商務與BVNK穩定幣基礎設施，五年後跑道判寬（🟢）。十類衰退信號亮2項（美國簽帳卡份額、倍數4年下移），長期成長性與陷阱風險皆為中。","governance":"現金品質：FCF高於淨利，2024年FCF/淨利1.06、2025年1.10；前九個月FCF 107.18億美元，資本支出11.41億美元只占約11%。SBC占營業利益3.2%（前九個月），年化約7億美元，對市值稀釋約0.13%。股東回饋：Q2回購49億美元、Q3回購30億美元、10月至26日再6.48億美元，股息殖利率0.55%；在30倍以上本益比回購，盈餘殖利率只有約3.1–3.7%，報酬偏低。收購：BVNK 14億美元8月完成，管理層稱收入基期小、影響極小。負債：淨負債134.7億美元，穆迪Aa3／標普A+、展望穩定。計分：SBC稀釋過、回購收益率不過、收購報酬未能衡量，判B。現金去向三年四分、債務到期結構與加權利率事實表未涵蓋。","valuation":"現價638.01美元＝2026年度共識EPS的31.8倍、2027年度27.6倍、2028年度23.7倍。市場要的是：五年EPS年增約13%（2031年約37美元）且本益比只從31.8倍降到27倍，換到約10%年化。EPS路徑我信——Q3淨營收+14%、2026年度共識近3個月上修1.9%；倍數再往上我不信——26週已漲29%，Q3有時點提前、Q4定價開始滿年。落後本益比33.4倍、市銷率15.3倍是4個年度端點中最低，代表相對自身近年不貴，但這不是5年連續分位。PEG約2.0（31.84÷15.9），在合理與偏貴的邊界。同業前瞻本益比事實表未涵蓋，終端倍數只能以自身2027年度27.6倍對照。短期（12個月）約+11%、中期（3年）約+36%：EPS走基本情境、本益比由31.8倍線性降到27倍。結論合理但空間窄，不追；580美元以下（2027年度約25倍）基本情境年化升到約12%才加碼。","premortem":"看錯的三條路見反證紀錄：監管把定價上限壓下來（與唯一致命點重疊）、A2A與穩定幣繞卡、發卡行分走增量。路徑風險中等：歷史最大回撤事實表未涵蓋，以情境推估−30%～−45%——一般衰退或監管驚嚇時EPS照共識、本益比回到約22倍本年EPS（約441美元，接近250週均線451美元）；深度情境EPS谷底約20.3美元×17倍約345美元。成長熄火壓力測試：2028年後成長降到15%／10%／5%、本益比對應28／22／17倍，五年終點約1147／789／530美元，三種中兩種高於現價。週線上股價高於52、104、250週均線，250週均線13週斜率+0.94%，屬中性。陷阱風險中：不是便宜股陷阱，亮的是美國份額與倍數下移兩項。RSI標記不可用，不作動能判斷。"},"plain":{"six":{"how_it_makes_money":"賺全球每筆卡片交易的網路評估費與加值服務費，錢卡在發卡行選網路與商店受理兩個節點；Q3淨營收98.07億美元、調整後營益率60.5%","moat":"護城河穩定（→）、等級B：定價權仍在擴大，但美國份額小輸Visa、發卡行分走更多回扣、監管上限逼近，三者抵銷","growth":"五年後跑道寬（🟢）：量、價、加值服務三條線都有財報證據；共識EPS年增約16%中約3pp靠回購與營益率","capital":"資本配置中等：SBC稀釋極低、FCF高於淨利，但以30倍以上本益比回購的報酬偏低，收購報酬尚未證實","valuation":"現價要求五年EPS年增約13%且本益比只降到27倍，才換到約10%年化；EPS路徑可信，倍數沒有再上行空間——合理但不追","how_wrong":"最可能看錯在監管：美國若立法強制信用卡第二網路路由，定價權與本益比會同時下修；路徑風險中等（−30%～−45%），陷阱風險中"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到580美元以下（2027年共識EPS約25倍、基本情境5年年化約12%）","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":638.01,"week26_return_pct":29.18,"consensus_rev_3m_pct":1.93,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"2026年度分母含Q3服務專案提前認列（管理層稱Q4回吐，全年不變）；GAAP含2.02億美元重組費（每股0.18美元），不在調整後口徑；分母不構成爭點"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026財報與2027年度財測","impact":"高","watch":"淨營收成長指引是否維持低雙位數高端、回扣與誘因比率、Q4時點回吐幅度"},{"date":"2026-12","date_precision":"month","type":"product","event":"年末購物季代理式商務交易（Agent Pay、Shop Pay、OpenAI合作）","impact":"低","watch":"管理層是否揭露代理交易量與採用方數"},{"date":"2027-04","date_precision":"month","type":"other","event":"Q1 2027財報：加密高基期過後的歐洲內部跨境","impact":"中","watch":"整體跨境是否回到10%以上，驗證管理層一次性歸因"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,265B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭地位</h2>
<p class="lead">護城河等級 B，趨勢持平。定價權仍強，但份額小輸、回扣上升、監管逼近。</p>
<ul class="pts">
<li>護城河來自雙邊網路效應。約 38 億張卡與逾 2 億個受理點彼此需要，代幣化、詐欺偵測與加值服務又把發卡行綁得更緊。MA 與 Visa 共享這個雙寡頭結構的租金，新進者很難複製兩邊規模。</li>
<li>定價面仍在擴大。Q3 國內評估費比成交額多成長 6 個百分點，跨境多 5 個百分點，交易處理比筆數多 5 個百分點。交易筆數仍有 +9%，沒有出現提價後銷量下滑。定價給 8 分，扣分原因是監管上限已在視線內。</li>
<li>執行面贏單與失單互抵。贏單包括 Pinnacle 2027 年整批轉入、印度 HDFC、德國 DSGV 與 DZ Bank 續約、北歐 Handelsbanken 與 Swedbank 續約。失單包括 Lloyds 約 1000 萬張卡轉 Visa、Capital One 簽帳卡移出，使美國簽帳卡只 +1%。2025 年美國購買量 MA +6.3%，Visa +6.8%。執行給 8 分。</li>
<li>威脅有三條。Visa 點對點搶單機率 40%，Lloyds 與 Capital One 是實例。A2A 即時帳戶支付與金融科技內部轉帳的生態攻擊機率 35%，印度 UPI 已成規模。穩定幣與加密原生業者機率 30%，目前 MA 以收購 BVNK 參與，商店端用途尚未見量。</li>
<li>與同業相比，MA 營益率 TTM 60.1%，Visa 65.6%，差約 5.5 個百分點。自由現金流利潤率 MA 42.5%，Visa 44.9%。差距反映 Visa 的規模，兩家吃的是同一塊結構租金。MA 自身營益率由 2022 年的 57.2% 升到 2025 年的 59.5%，沒有證據顯示差距在擴大。</li>
<li>社會容忍度是最紅的一格。商家和解讓平均交換費降 0.1 個百分點、為期五年，並將標準消費信用卡費率上限訂在 1.25%、為期八年。信用卡競爭法案 2026-01 重提，DOJ 對簽帳卡業務發出調查令。和解上限落在發卡行的交換費，不直接碰 MA 的網路費，但疊加起來會壓縮未來提價空間。</li>
</ul>
<h3>§5　二維評分與護城河對應數字</h3>
<!-- E5 -->
<h3>§5.F對手財務深度對照</h3>
<!-- E6 -->
<h3>§5.R報酬持續期檢核</h3>
<!-- E7 -->
</section>

```