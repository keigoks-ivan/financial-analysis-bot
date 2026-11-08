你是 stock-analyst v20 的**散文層（prose）agent**，標的 LITE（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：LITE　日期：2026-11-08　archetype：None　前份裁決：2026-08-12　觀望｜候選/追蹤池　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1824B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（557B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1003B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1483B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（820B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（561B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（916B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2129B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3332B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2995B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1824           3623-5176      5 條（2–6 內）  
s3                  8000         557           5210-7443      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3306          8186-11694      5 條（2–6 內）  
s6                 11000         561          7307-10439      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         916           1809-2584      5 條（2–6 內）  
s10                 5000        2129           2010-2871      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2995           2000-2005      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4685B；至少需散文≈40.31KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−92.96
−60
−60%
−58%
−55%
−48%
−40.41%
−40.41
−40
−40%
−34.4%
−26.59%
−23.9%
−5.49
0
0.35%
0.35
0.45
0.6
0.7%
0.86
01
1%
1
1.009
1.02
1.2%
1.25
1.467
1.5%
1.59
1.6
1.67
2
02
2.3
3.00
3
3.2
3.4%
3.569
3.57
4
4.5
5%
05
5
5.42
5.87
5.90
06
6
6.20
6.49
6.494
6.8
7
7.5%
08
8
8.8
9
09
9.6%
9.96%
10
10%
11
11%
11.4
11.6%
12%
12
12.6
12.63
12.9
12.90
12.9%
13.05
13.81
14
14.11%
15
15.0%
15%
15.4%
15.75
16
16.25
17
18
18.5%
18.73
19.80
20
21
21.69
21.7
22%
22
23%
23.08%
23.35%
23.6
23.9%
24
24.8
24.83
25
25%
26
26.5
26.6%
27
27.4
28.5%
28.92%
29.51
30
30%
31.0
31
32
32.6%
34.4%
35%
35
35.5%
37
38
38.16%
39.0%
39
39.01
40%
40
40.41%
41.6%
42
42.3%
43.8
44
45
45%
45.2%
45.2
45.91%
46
46%
47.5%
48.0%
48%
49
50%
50
50.4%
51.0%
51%
52
54.41
56.5%
57.1%
58%
58.4
64
64.5%
65.9
66.90
68.7
69.35
70%
70.0%
70
72%
77
78
80%
80
83.5%
85
95%
100%
100
103%
104.73
119.7
123%
130%
150%
200
230
232
240
280
360
411.9
488.4
538.59
543
600
608
782
800
820.59
2024
2026
2027
2028
2029
2030
20261108
1,140
1,150
1,420
1,700
1,948.8
4,310
5,000
5,070
5,500
8,940
9,068
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
{"meta":{"ticker":"LITE","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Lumentum Holdings Inc."},"oneliner":"Lumentum 已同意以全股票併入 Marvell。股價 538.59 美元對 FY2027E 為 21.7 倍，獨立看不貴，但股東最後收到的是 Marvell 股票；換股條款與 Marvell 端價值驗證前先等，不因超賣進場。","thesis":{"H":[{"id":"H1","text":"雷射供不應求延續到 2027 年底，定價不回吐，非 GAAP 毛利率站穩 50% 以上。","2y":"FY2027、FY2028 單季毛利率維持 50% 以上","5y":null,"10y":null,"threshold":"非 GAAP 毛利率單季 ≥ 50%（Q4 FY2026 為 50.4%）","source":"公司季度新聞稿與法說對供需缺口的用語","drift_rule":"連 2 季低於 47.5% 為削弱，連 3 季低於 45% 為反轉"},{"id":"H2","text":"FY2028 非 GAAP EPS 達 37 美元以上，管理層 40 美元目標至少兌現九成多。","2y":"FY2028 EPS ≥ 37 美元","5y":null,"10y":null,"threshold":"FY2028 EPS ≥ 37 美元（共識 39.01 美元的 95%）","source":"公司季報與 Koyfin 共識快照","drift_rule":"FY2028 共識連 2 季低於 37 美元為削弱，連 3 季低於 35 美元為反轉"},{"id":"H3","text":"CPO、NPO 與 OCS 成為第二引擎，撐住缺貨紅利消退後的獲利。","2y":null,"5y":"FY2031 前三項合計占營收三成以上","10y":null,"threshold":"2028 年超高功率雷射、ELS 與 OCS 合計營收 ≥ 30 億美元；前哨為 FY2027 Q3 超高功率雷射單季 ≥ 1 億美元","source":"法說、新聞稿與合併後分部揭露","drift_rule":"里程碑連 4 季落後 5% 以上為削弱，連 6 季落後 10% 以上為反轉"},{"id":"H4","text":"合併案在 2028 上半年完成，換到的 Marvell 股票價值不低於 LITE 獨立路徑；換股比例待原文確認。","2y":"交割時換股價值不低於獨立估值","5y":null,"10y":null,"threshold":"換股比例隱含價值 ≥ 608 美元（FY2028E Base 38 美元×16 倍）","source":"8-K、S-4 與 Marvell 股價；Marvell 資料事實表未涵蓋","drift_rule":"隱含價值連 2 季低於門檻 5% 以上為削弱，連 3 季低於門檻 10% 以上為反轉"}],"R":[{"id":"R1","text":"合併案風險：全股票換股，比例與機制待原文確認，交割預期在 2028 上半年，期間股價跟 Marvell 連動；破局或監管要求剝離資產都會改變報酬來源。終止費與核准清單事實表未涵蓋。","h_ref":"H4","clock":"🔥","threshold":"合併終止、換股比例重議，或監管要求剝離磷化銦、OCS 資產","evidence_refs":["ma_merger#0","major_events#0"]},{"id":"R2","text":"客戶集中與第二來源：最大客戶占 FY2026 營收 26.6%（FY2025 15.4%），第二大 15.0%；兩大客戶占應收 30% 與 11%；多數客戶以採購單下單，過去曾因客戶採購變動而減單。未見最大客戶導入第二來源或自製的明確揭露，客戶身分只有二手推測。","h_ref":"H2","clock":"🔥","threshold":"最大客戶占比 ≥ 35%，或最大客戶應收占比 ≥ 40%，或前兩大客戶任一減單","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R3","text":"競爭與定價：10-K 寫明光通訊產品走向商品化，亞洲新進者帶來價格壓力，對手可能以低價搶份額；目前只有管理層說法顯示未受影響。","h_ref":"H1","clock":"🔥","threshold":"雷射合約價首度季減，或 Coherent 200G EML、超高功率雷射通過 NVIDIA 或前三大雲端認證","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"id":"R4","text":"出口管制調查：2024-08 起 BIS 與 DOJ 傳票查華為業務，仍在進行，未見和解或處罰。公司 2024 年初已停止對華為出貨，現行營收不受影響，風險在罰款與出口權限；屬行政傳票與司法部傳票程序，罰款區間與結案時點事實表未涵蓋。","h_ref":"H4","clock":"🐢","threshold":"和解或罰款 ≥ 3 億美元，或刑事起訴、出口權限遭拒","evidence_refs":["regulatory_antitrust#0","major_events#1","sec_investigation_restatement#0","reg_tariff_export#0"]},{"id":"R5","text":"關稅與材料管制：232 條款半導體調查、美國出口管制、中國稀土與基板限制、部分供應商在中國，製造與代工集中亞洲；無法轉嫁就壓縮毛利率。","h_ref":"H1","clock":"🐢","threshold":"單季毛利率下降 ≥ 2 個百分點，且公司歸因關稅或材料管制","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#4","geo_supply_chain#1"]},{"id":"R6","text":"自身供給：磷化銦基板吃緊，AXT 新約後管理層仍說一兩季後可能不夠；雖有多座晶圓廠，缺口仍在擴大，擴產最大變數是客戶認證時間。","h_ref":"H3","clock":"🔥","threshold":"Greensboro 首批營收延到 2028 下半年之後，或基板短缺使單季營收低於指引下緣","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"2028 年底前，雷射由缺貨翻成過剩，出現第一筆合約價季減或前兩大客戶遞延長約。","why_fatal":"這是情境樹最大的單一敏感項：Base 與 Bear 的終端 EPS 差 26 美元，多數來自定價與毛利率。毛利率每掉 1 個百分點，FY2028E EPS 約少 0.86 美元（營收 104.73 億美元×1%×83.5%÷1.02 億股）；上一輪下行的 FY2024 營收年減 23%、毛利率 18.5%。","if_happens":"不等合併結果，減碼至半倉並改用 Bear 路徑重算；下一季續跌且 FY2028 共識跌破 30 美元則清倉。","how_monitor":"每季毛利率、法說對 EML 與高功率雷射缺口的用語（2026-08-11 為 EML 未縮、高功率更落後）、新約價格描述、TrendForce 產能與報價；交割後改看 Marvell 光學相關揭露。","probability":"12–24 個月約 25%：2027 年前缺貨有長約支撐，風險集中在 2028 年 Greensboro、英國廠與對手產能同時開出。"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.81,"peg_fy2":0.35,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":-92.96,"FY2027E":24.83,"FY2028E":39.01,"FY2029E":54.41},"fy_end_month":6,"eps_basis":"FY2027E–FY2029E 為 Koyfin 共識，與公司非 GAAP EPS 同口徑，財年止於六月底；分析師家數事實表未涵蓋，營收共識為 21–22 家。FY2026A 欄只有 GAAP 稀釋 EPS −92.96 美元，含 78 億美元非現金可轉債損失，與共識不同口徑，不能用來算成長率；FY2026 非 GAAP 全年 EPS 事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/scenario.json","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"FY2024 營收年減 23.08%、毛利率 18.5%、營益率 −26.59%，FY2027 起靠缺貨定價把 GAAP 毛利率推到 51%；2026-11-01 簽全股票併購，成為待交割標的。"},"industry":{"clock_phase":"III","sd_verdict_source":"依據為供需與定價，不看股價：漲價、長約、擴產競賽同時出現，訂單仍在上修。2027 年前結構性缺貨（2026-09-09 管理層稱缺口不會緩解），2028 年起反轉風險升高（TrendForce 估 2026 年 EML＋CW-DFB 月產能約倍增至 5,070 萬顆，Greensboro 2028 年開出）。","bargaining":{"up":"基板吃緊，靠日本供應商的領先安排加上 AXT 新約，管理層說需求若續增還要再找貨源。","down":"前兩大客戶占 41.6%。短期缺貨讓公司握有定價權，長期買方有能力扶植第二來源，NVIDIA 已同時資助 LITE 與 Coherent。","geo":"磷化銦廠在日本兩座，美國 Greensboro 2028 年開出；泵浦在 Rose Orchard 擴產並於泰國封測；部分供應商在中國。"},"profit_pool_dir":"利潤向雷射晶片集中：LITE 過去 12 個月毛利率 45.91%，高於 Coherent 38.16% 與 AAOI 28.92%；五年前後的營業利益池占比事實表未涵蓋。","tam_table":[{"item":"OCS 可服務市場（管理層）","value":"先前估 80 億美元，2026-08-27 CEO 稱被低估"},{"item":"scale-up CPO 增量營收（管理層）","value":"2026-05-05 CEO 估逾 50 億美元；2026-11-02 再宣布第二個大型 NPO／CPO 訂單，預期逾 50 億美元"},{"item":"合併後 2030 年 TAM（Marvell 自述）","value":"5,500 億美元，其中增量約 600 億美元"},{"item":"滲透率與營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"磷化銦雷射製程經驗與規格一致性帶來客戶良率優勢，加上約一年的認證週期與長約綁定的產能。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行面擴大：毛利率在季營收 10 億美元就過 50%，原目標是 20 億美元；EPS 連兩季高於指引上緣。定價面穩定：新約價格不低於舊約，但來源是缺貨，1.6T 世代矽光加 CW 分走 EML 占比，由 800G 的 70–80% 降到 40–50%，Coherent 也拿到 NVIDIA 長約。兩者合計判穩定。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，方向改用毛利率與營益率對照。","threats":[{"level":"🔴","text":"客戶扶植第二來源，加上併入 Marvell 後供應中立性受質疑：雷射賣給幾乎所有模組對手（2026-11-02 CEO），NVIDIA 同時資助 Coherent，最大客戶的 OCS 仍保留自製。","p":"35%","evidence_refs":["customer_second_source#0","customer_second_source#1","competitive_share_entrants#1"]},{"level":"🟡","text":"亞洲低價新進者與中國磷化銦新廠，先打可插拔 CW 雷射；管理層稱至今未見影響，但 10-K 已寫出價格壓力。","p":"30%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"矽光加 CW 在 1.6T 分走 EML 占比；LITE 也賣 CW，損失主要落在毛利差與 EML 稀缺性。3.2T 時 EML 能否回來只有管理層說法。","p":"40%","evidence_refs":["substitute_technology#2"]},{"level":"🟡","text":"薄膜鈮酸鋰新進者只搶調變器，不碰磷化銦光源，威脅範圍有限。","p":"15%","evidence_refs":["competitive_share_entrants#4"]}],"roic_durability":{"quadrant":"高利益率、周轉未知：過去 12 個月 GAAP 營益率 23.35%，投入資本事實表未涵蓋，無法落到象限。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是 AI 叢集，決策者是雲端架構團隊與 NVIDIA，付款者是雲端與模組廠，三者都成立。要解決的問題是銅線撐不住的頻寬，會持續；解法會從 EML 換到 CW、NPO、CPO，LITE 這幾種都有產品。代理變數：EML 出貨仍低於需求，高功率雷射缺口擴大（2026-08-11）。"},{"item":"決策層級","level":"🟡","text":"設計導入後換供應商要重新認證，NVIDIA 認證耗時一年，泵浦合約三年且多數照付不議。但缺貨時客戶有貨就用（2026-08-11 Wupen Yuen），多數客戶只下採購單，替代性比供應商家數顯示的高。"},{"item":"價值鏈分配","level":"🟡","text":"目前雷射是最稀缺環節，LITE 毛利率高於模組同業；但買方極度集中，前兩大客戶占 41.6%，NVIDIA 同時資助兩家雷射廠，長期會把超額利潤往回拿。合併後部分利潤改由 Marvell 股東分享。"},{"item":"社會容忍度","level":"🟢","text":"企業間採購，沒有民生漲價爭議，價格上限由買方議價決定。政治風險集中在出口管制與關稅，已列入風險項。"}],"roiic":"事實表未涵蓋投入資本，無法計算","reinvest_rate":"事實表未涵蓋折舊、營運資金與收購淨額，無法計算","endo_ceiling":null,"formula_note":"資本支出只有 Q3、Q4 FY2026 的 1.25 億與 1.67 億美元，沒有折舊、營運資金與投入資本，內生成長率無法推導。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","LITE":45.91,"COHR":38.16,"CIEN":44.07,"AAOI":28.92,"MTSI":57.13,"unit":"%"},{"metric":"營業利益率","LITE":23.35,"COHR":14.11,"CIEN":14.12,"AAOI":-10.58,"MTSI":18.97,"unit":"%"},{"metric":"FCF 利潤率","LITE":9.52,"COHR":-23.28,"CIEN":13.53,"AAOI":-100.9,"MTSI":9.44,"unit":"%"},{"metric":"研發密度","LITE":12.47,"COHR":10.18,"CIEN":15.36,"AAOI":18.06,"MTSI":23.23,"unit":"%"}],"competitors":[{"name":"COHR","gm":38.16,"om":14.11,"fcf_margin":-23.28,"rd_intensity":10.18,"strategy_note":"超高功率雷射目前唯一被管理層點名的對手，NVIDIA 同時與其簽長約，最可能成為第二來源；獲利與現金流都落後 LITE，擴產壓力較大。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CIEN","gm":44.07,"om":14.12,"fcf_margin":13.53,"rd_intensity":15.36,"strategy_note":"網通設備商，不是雷射晶片的直接對手，對照價值在系統層的毛利與現金流。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"AAOI","gm":28.92,"om":-10.58,"fcf_margin":-100.9,"rd_intensity":18.06,"strategy_note":"模組與雷射的擴產者，仍在虧損且現金燒得快，短期構不成定價威脅。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MTSI","gm":57.13,"om":18.97,"fcf_margin":9.44,"rd_intensity":23.23,"strategy_note":"類比與光電元件廠，毛利率高於 LITE，但營益率較低，是規模較小的元件對照，不是直接替代來源。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量與價並進，產品組合往 200G 與高功率雷射移動；併購與回購貢獻為零。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本，內生上限無法計算，情境樹保守視同超出上限。","segments":[{"item":"元件（Q4 FY2026）","value":"6.494 億美元，季增 22%，年增 103%"},{"item":"系統（Q4 FY2026）","value":"3.569 億美元，季增 30%，年增 123%"},{"item":"OCS（管理層）","value":"Q1 FY2027 指引為首個單季破億美元，2026 下半年目標 4 億美元"},{"item":"超高功率雷射（管理層）","value":"2026 年底單季約 5,000 萬美元，FY2027 Q3 破億美元"},{"item":"Q1 FY2027 分部金額","value":"事實表未涵蓋"}],"decay_signals":["核心市占：1.6T 世代 EML 架構占比由 70–80% 降到 40–50%（2026-08-27 CEO），亮，LITE 以 CW 部分補回。","毛利率連兩季年減：未亮，Q4 FY2026 非 GAAP 毛利率年增 12.6 個百分點。","EPS 與營收成長差距：未亮，FY2028E EPS 年增 57.1%、營收年增 56.5%，差 0.6 個百分點。","SBC 占營收：Q1 FY2027 為 11.6%，含一次性；扣除後 3.4%，未亮。","FCF／淨利、維修性資本支出、產業倍數三年走勢：事實表未涵蓋，無法判定。"],"trap_rating":"價值陷阱風險中等，亮 1 項；長期成長性同為中等。"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，證據包未見股利或回購，現金去向四分事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Cloud Light 收購金額與實現報酬事實表未涵蓋；2026-08-27 CEO 承認模組毛利不及頂尖對手且過去有品質問題，方向偏負面。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"證據包未見回購，資金用於擴產與償債。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"以 Q1 FY2027 的 1.467 億美元年化（含一次性，偏高估）為 5.87 億美元，除以市值 488.4 億美元，約 1.2%／年，低於 1.5%；扣一次性約 0.35%。股數實際增加另含可轉債轉股與 NVIDIA 投資，屬融資行為。","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2027E、FY2028E），獨立口徑，未納入 Marvell 換股；P/S 與 EV/S 僅作對照。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比，不能用同業倍數當錨。"},"fwd_pe":21.69,"peg":0.45,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"倍數從前份約 43.8 倍降到 21.69 倍，偏貴的問題已解除；PEG 0.45 因分母有爭議，不計入便宜論證；P/S 年度端點 68.7 分位屬中上。綜合判為合理。","upside_short_pct":12.9,"upside_mid_pct":45.2},"trap_analysis":{"verdict":"🟡","label":"分母爭議未解，衰退信號亮 1 項"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"TrendForce 估 2026 年 EML＋CW-DFB 月產能約倍增；Coherent 有 NVIDIA 長約；中國磷化銦新廠進場；多數客戶只下採購單；FY2024 營收年減 23%、毛利率 18.5%。","assumption":"2027 年前缺貨不會結束，2028 年擴產開出時需求由 NPO、CPO 接手。","consequence":"五年後虧 50% 最可能的故事：2028 年供給開出時 scale-up 延後，長約重議，EPS 回到 20 美元，倍數 12–14 倍。","ruling":"採納為 Bear 路徑核心，與唯一致命點相同，機率 30%。短期不成立，管理層 2026-09-09 仍說新約價格不低於舊約。","watch":"雷射合約價季變動、EML 缺口用語、Coherent 認證進度。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_concentration_credit#1","geo_supply_chain#0"],"fact_refs":["f_kpi5_gaap_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"全股票併入 Marvell，換股比例傳為 4.5 股；10 億美元協同主要在銷貨成本，CFO 不拆細項；ELS 模組毛利低於雷射；Marvell 要投數十億美元鎖產能。","assumption":"雷射需求如期，LITE 獨立 EPS 達到 40 美元。","consequence":"LITE 業務成功，但上行由合併後全體股東分享，LITE 股東拿到的是一定股數的 Marvell；若 Marvell 自身業務拖累，報酬會低於獨立路徑。","ruling":"採納。獨立情境樹的上下行比例不得當進場依據，S-4 公開後改用 Marvell 股票口徑重算。","watch":"S-4 條款，LITE 股價除以 4.5 與 Marvell 股價的價差。","evidence_refs":["ma_merger#0","major_events#0"],"fact_refs":["f_price_at_dd"]},{"view":"價格已反映太多","evidence":"P/S 13.05 倍在四個年度端點的 68.7 分位；FY2028E 共識與管理層目標幾乎重合，賣方未打折；GAAP 毛利率已到 51%。","assumption":"FY2027E 21.69 倍隱含的盈餘可持續。","consequence":"Base 終端 17 倍、EPS 50 美元時年化約一成，只落在中段。","ruling":"部分反駁。股價較前份下跌 34.4%、FY2027 共識上修 32.6%，偏貴的問題已解除；分母是否高點未解，所以只到合理。","watch":"FY2028 共識方向、毛利率是否見頂。","fact_refs":["f_ps_current","f_ps_percentile","f_fwd_pe_latest","f_consensus_eps_fy2"]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 820.59 → 本次 538.59（-34.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=820.59","side_b":"本次 price_at_dd=538.59","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 候選/追蹤池 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=候選/追蹤池","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟢、五年後跑道 🟡→🟢。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 820.59 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 820.59 美元：Bull 價 1,948.8、Bear 價 411.9，五年期望值 +39.0%，基準年化 7.5%，不對稱比 2.3","side_b":"本次情境、股價仍用 820.59 美元：Bull 價 1,700、Bear 價 360，五年期望值 +11.6%，基準年化 0.7%，不對稱比 1.59","ruling":"先換情境、股價不動：五年期望值少 27.4 個百分點，基準年化少 6.8 個百分點。不對稱比由 2.3 變為 1.59。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 820.59 美元：五年期望值 +11.6%，基準年化 0.7%，不對稱比 1.59","side_b":"本次情境、股價 538.59 美元：五年期望值 +70.0%，基準年化 9.6%，不對稱比 5.42","ruling":"再換股價、情境不動：起點價下跌 34.4%，五年期望值多 58.4 個百分點，基準年化多 8.8 個百分點，不對稱比由 1.59 升到 5.42。合計五年期望值比前份多 31.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份估值門檻已達成","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：股價 820.59 美元、FY2027 基礎前瞻本益比約 43.8 倍，估值結論偏貴，Bull 機率 25%、Bear 機率 30%，最大回撤 −58%。","side_b":"本次：股價 538.59 美元、21.69 倍，前份「前瞻本益比回落到 32 倍以下」已達成；Bull、Bear 機率維持 25%、30%，最大回撤區間 −40%～−60%。","ruling":"估值結論由偏貴改為合理。機率未動，新增訂單的利多與合併、供給風險互相抵銷。前份的 COHR 認證前提在事實表沒有新資料，毛利率連四季高於 48% 尚未達成。","evidence_level":"高","settle_metric":"FY2027E 前瞻本益比","if_then":["若股價續漲但 S-4 尚未公開，不追","若股價下跌而毛利率與新約價格未受損，S-4 確認後分批反買"],"evidence_refs":[]},{"axis":"合併案改寫持有標的，等待的理由換了","cause":"新證據","prior_field":["signal"],"side_a":"前份因估值過高而等待，卡住的是價格。","side_b":"本次價格問題解除，卡住的是事件：2026-11-01 簽約併入 Marvell，股東收到 Marvell 股票，換股條款、終止費、監管條件與 Marvell 價值都未驗證。","ruling":"裁決方向維持等待，綜合訊號維持同一級，約束條件由價格改為合併條款。此約束的否定就是重新評估條件，不設進場價。","evidence_level":"中","settle_metric":"S-4 條款與 Marvell 股票口徑的 Base 年化報酬","if_then":["若 S-4 確認條款且 Marvell 口徑 Base 年化達 12%，重跑判斷，首倉以小部位起步","若合併終止，回到獨立路徑重跑，判斷前停止加碼"],"evidence_refs":["ma_merger#0","major_events#0"]},{"axis":"交易金額與市值對不上","side_a":"聚合報導：全股票、4.5 股 Marvell 換 1 股 LITE，交易約 1,150 億美元。","side_b":"事實表 LITE 市值 488.4 億美元；若 1,150 億美元是收購價，每股約 1,140 美元，現價只有一半，不像正常交易價差。","ruling":"不採用 1,150 億美元當收購價，較可能是合併後規模或報導誤差；4.5 股換股比例也列待驗證，本檔未讀 8-K 條款全文。","evidence_level":"低","settle_metric":"合併協議全文與 S-4","if_then":["若換股比例與報導不同，全部 Marvell 口徑數字重算，重算前不追"],"evidence_refs":["major_events#0"]},{"axis":"雷射缺貨能撐多久","cause":"新證據","prior_field":["trap","moat_trend","cycle_position"],"side_a":"管理層：2027 缺口不會緩解，新約價格不低於舊約（2026-09-09）；被問超額供給，執行長認為風險低（2026-05-05）。","side_b":"TrendForce：2026 年 EML＋CW-DFB 月產能約倍增；中國磷化銦新廠陸續出現；英國廠與 Greensboro 在 2027–2028 開出。","ruling":"可調和，屬時間差：2027 年前採信管理層，2028 年起不採信。陷阱風險維持中等、護城河方向維持穩定，循環位置由晚循環到過熱頂部收斂為晚循環。","evidence_level":"中","settle_metric":"雷射合約價季變動與 EML 缺口用語","if_then":["若下季新約價格仍不低於舊約，維持 Base 路徑","若任一類雷射合約價首度季減，減碼至半倉並改用 Bear 路徑"],"evidence_refs":["geo_supply_chain#0"]},{"axis":"五年後跑道上調","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"前份：跑道中等，第二引擎待驗證。","side_b":"本次：第二個大型 NPO／CPO 訂單預期逾 50 億美元（2026-11-02 CEO），NPO 放量由 2028 底提前到 2027 底（2026-08-27 CEO）。","ruling":"上調為寬，只代表需求面的下一條曲線已有訂單。營收要到 2027 下半年才能驗證，驗證前不提高 Bull 機率。","evidence_level":"中","settle_metric":"FY2027 Q3 超高功率雷射單季營收與 2028 年 NPO、CPO 出貨","if_then":["若超高功率雷射 FY2027 Q3 未破 1 億美元，跑道回調為中等並停止加碼"],"evidence_refs":[]},{"axis":"商業類型重新歸類","cause":"方法變動","prior_field":["archetype"],"side_a":"前份歸為品質複利成長。","side_b":"本次歸為循環/商品，次要屬性為特殊情境。","ruling":"近四個財年有兩年自由現金流為負，FY2024 毛利率 18.5%，獲利躍升來自缺貨定價，用複利股的尺度會高估持續性。若缺貨結束後毛利率仍守住 45% 以上，應改回成長型。","evidence_level":"高","settle_metric":"缺貨紓解後的毛利率","if_then":["若供需平衡後毛利率連四季高於 45%，改回成長型重算倍數"],"evidence_refs":[]},{"axis":"管理層說獨立前景極好，卻交出控制權","side_a":"2026-09-09 管理層對 FY28 EPS 40 美元表示有信心，並稱最好的日子還在後面。","side_b":"2026-11-01 同意全股票併入 Marvell；2026-11-02 執行長稱合併第一名勝過買下多家第二到第四名，雙方沒有回答是否有其他出價者，也沒有談買在短缺高峰的價格倍數。","ruling":"可調和。賣出本身不能證明獨立前景變差，但 40 美元目標的可信度要打折，獨立上行也不再全歸 LITE 股東。","evidence_level":"低","settle_metric":"S-4 合併背景章節的出價過程與財務顧問預測","if_then":["若 S-4 顯示財務顧問預測明顯低於 40 美元，Base 的 FY2028E 下修並停止加碼"],"evidence_refs":["ma_merger#0"]},{"axis":"OCS 客戶基礎改口","side_a":"2026-05-05 執行長：OCS 與三家客戶合作，兩家占多數。","side_b":"2026-08-27 執行長：目前主要綁定單一客戶；2026-09-09 管理層：上行來自最大客戶，該客戶還保留內部供應。","ruling":"採信後者，集中度上升，40 美元目標更依賴單一客戶。","evidence_level":"中","settle_metric":"2027 年初是否成為該客戶第一 OCS 供應商、10-K 客戶占比","if_then":["若最大客戶占比升到 35% 以上，減碼"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#1"]},{"axis":"現在就買的最強論證","side_a":"FY2028E 13.81 倍，RSI 29.51，股價低於 52 週線 23.9%，EPS 連兩季高於指引上緣，訂單還在加；若合併破局，獨立路徑 Base 五年仍有約 58% 報酬。","side_b":"股東實收 Marvell 股票，Marvell 股價與盈餘不在事實表；分母爭議未解；交割前約 18 個月股價跟著 Marvell 走。","ruling":"不採納現在買進，等 S-4。代價是股價先反彈時會錯過一段，本檔接受。","evidence_level":"中","settle_metric":"S-4 與 Q2 FY2027 財報","if_then":["若股價續漲但條款未明，不追","若股價再跌且基本面無損，S-4 確認後分批反買"],"evidence_refs":[]},{"axis":"重新評估門檻更換，減碼與清倉條件另列","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE(FY27基礎，隨最新共識滾動重算)回落至≤32x或5Y分位<70%；或GM連續4季維持>48%；生意面前提：COHR 200G/lane EML於任一top hyperscaler/NVIDIA完成客戶認證前，估值觸發不因股價波動單獨視為安全邊際打開","side_b":"S-4 公開並讀過換股條款、終止費與監管條件後，以 Marvell 股票口徑重算，Base 年化達 12% 才重跑進場判斷。","ruling":"舊門檻的估值部分已達成，合併案使獨立估值不再是決定條件，改成事件門檻；減碼與清倉條件列在觸發器。","evidence_level":"中","settle_metric":"S-4","if_then":[],"evidence_refs":["ma_merger#0"]},{"axis":"Single Thing 首次設立","cause":"新證據","prior_field":null,"side_a":"前份未設唯一致命點（摘要此欄為空）","side_b":"2028 年底前，雷射由缺貨翻成過剩，出現第一筆合約價季減或前兩大客戶遞延長約。","ruling":"選敏感度最大的一項，合併案影響報酬形式，對盈餘的敏感度小於雷射定價。","evidence_level":"中","settle_metric":"雷射合約價與長約揭露","if_then":["若發生，減碼至半倉"],"evidence_refs":[]},{"axis":"減碼與清倉指標首次設立","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未列減碼或清倉指標（摘要此欄為空）","side_b":"本次新增五項：毛利率連兩季低於 48%、FY2028 共識跌破 30 美元、雷射合約價首度季減、最大客戶占比達 35%、合併終止或被要求剝離資產。","ruling":"舊檔沒有下行紀律，合併與缺貨高峰下需要明確的減碼與清倉條件。","evidence_level":"中","settle_metric":"各指標來源見清單","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q2 FY2027 財報確認毛利率與指引","type":"假設驗證","maps_to":"H1","metric":"非 GAAP 毛利率、營收、EPS","threshold":"毛利率 ≥ 50%，營收落在 15.75–16.25 億美元，EPS 5.90–6.20 美元","action":"低於任一下緣則停止加碼，並重算 Base 路徑","source_freq":"公司新聞稿，每季","date":"2027-02"},{"n":2,"text":"管理層承諾的 12 月季 EML 出貨年增逾 50%","type":"假設驗證","maps_to":"H1","metric":"EML 單位出貨年增率","threshold":"＞50%","action":"未達則停止加碼","source_freq":"法說，每季","date":"2027-02"},{"n":3,"text":"超高功率雷射與 OCS 里程碑","type":"假設驗證","maps_to":"H3","metric":"FY2027 Q3 超高功率雷射單季營收；2026 下半年 OCS 營收；是否成為最大客戶的第一 OCS 供應商","threshold":"雷射 ≥ 1 億美元；OCS ≥ 4 億美元；2027 年 6 月前完成超車","action":"兩項未達則下修第二引擎假設並停止加碼","source_freq":"法說，每季","date":"2027-05"},{"n":4,"text":"S-4 公開後重跑判斷","type":"估值rearm","maps_to":"H4","metric":"換股比例、終止費、監管條件；Marvell 股票口徑的 Base 年化報酬","threshold":"Base 年化 ≥ 12%","action":"達標才重跑進場判斷，首倉以小部位起步","source_freq":"SEC 申報，單次","date":"2027Q1（本檔估計）","evidence_refs":["ma_merger#0"]},{"n":5,"text":"雷射合約價首度季減或前兩大客戶遞延長約","type":"Single Thing","maps_to":"H1","metric":"EML、CW、泵浦雷射合約價季變動；長約重議揭露","threshold":"任一類首度季減，或前兩大客戶任一遞延","action":"減碼至半倉，改用 Bear 路徑重算","source_freq":"法說與 TrendForce，每季","date":"至 2028-12","evidence_refs":["competitive_share_entrants#0"]},{"n":6,"text":"獲利與毛利率同時破線","type":"清倉","maps_to":"H2","metric":"FY2028 共識 EPS 與非 GAAP 毛利率","threshold":"共識跌破 30 美元，且毛利率連兩季低於 48%","action":"清倉","source_freq":"Koyfin 共識快照與公司新聞稿，每季","date":"至 2027-12"},{"n":7,"text":"合併終止或被要求剝離核心資產","type":"風險","maps_to":"R1","metric":"8-K 與監管公告","threshold":"終止、換股比例重議，或剝離磷化銦、OCS 資產","action":"停止加碼，回到獨立路徑重跑","source_freq":"SEC 申報，事件驅動","date":"至 2028-06","evidence_refs":["ma_merger#0","major_events#0"]},{"n":8,"text":"BIS、DOJ 調查的結案方式","type":"風險","maps_to":"R4","metric":"和解金額與程序性質","threshold":"和解或罰款 ≥ 3 億美元；或刑事起訴、出口權限遭拒","action":"金額達標減碼三分之一；刑事起訴或出口權限遭拒則清倉","source_freq":"10-Q 風險因素，每季","date":"結案時點事實表未涵蓋","evidence_refs":["regulatory_antitrust#0","major_events#1","sec_investigation_restatement#0"]},{"n":9,"text":"最大客戶占比續升","type":"風險","maps_to":"R2","metric":"最大客戶營收占比與應收帳款占比","threshold":"營收占比 ≥ 35%，或應收占比 ≥ 40%","action":"減碼","source_freq":"10-K，每年","date":"2027-08","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":10,"text":"關稅或材料管制吸收失敗","type":"風險","maps_to":"R5","metric":"非 GAAP 毛利率季變動與公司歸因","threshold":"單季下降 ≥ 2 個百分點，且公司歸因關稅或材料","action":"停止加碼","source_freq":"法說，每季","date":null,"evidence_refs":["reg_tariff_export#4","reg_tariff_export#2"]},{"n":11,"text":"下次完整複審","type":"複審日期","maps_to":"H4","metric":"S-4 是否公開、Q2 FY2027 財報是否發布","threshold":"日期到期","action":"重跑判斷","source_freq":"單次","date":"2027-02"}],"kill_metrics":[{"metric":"非 GAAP 毛利率（單季）","bear_threshold":"連兩季低於 48%","window":"2027 全年","source":"公司季度新聞稿","last_status":"ok"},{"metric":"FY2028 共識 EPS","bear_threshold":"跌破 30 美元（目前 39.01 美元）","window":"至 2027-12","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"雷射合約價季變動","bear_threshold":"任一類雷射合約價首度季減","window":"至 2028-12","source":"法說與 TrendForce","last_status":"ok"},{"metric":"最大客戶營收占比","bear_threshold":"≥35%（FY2026 為 26.6%）","window":"FY2027 10-K","source":"SEC 10-K","last_status":"warning"},{"metric":"合併案狀態","bear_threshold":"終止、重議換股比例，或被要求剝離磷化銦資產","window":"至 2028-06","source":"SEC 8-K 與 S-4","last_status":"unknown"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"這是 FY2022 10-K 的搜尋摘要轉述，不是原文，內容是 FY22 Q3 疫情停工，成因已消失；目前工廠分布改用 2026 年法說的日本、泰國與 Rose Orchard 資訊。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"S-4 確認前新增部位為零；確認後首倉從小部位起步，需有承受 −60% 等級回撤的準備。","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-40.41, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"S-4 公開並讀過換股條款、終止費與監管條件後，以 Marvell 股票口徑重算，Base 年化達 12% 才重跑進場判斷。","exec_line":"S-4 公開前不開新倉，不因 RSI 低接；已持有者續抱不加碼，雷射合約價首度季減即減碼至半倉。"},"reasoning":{"industry":"Q1 FY2027 營收 12.63 億美元，GAAP 毛利率 51.0%，GAAP 營益率 28.5%，非 GAAP 營益率 42.3%；Q2 指引營收 15.75–16.25 億美元、非 GAAP 營益率 45–46%。最新可得的分部拆分是 Q4 FY2026：元件 6.49 億美元占 64.5%，系統 3.57 億美元占 35.5%（2026-08-11 CFO）。Q1 FY2027 的完整法說與分部數字不在本包，事實表未涵蓋。成長同時來自量（泵浦雷射出貨年增逾 80%、窄線寬雷射年增逾 130%）、價（新約價格不低於先前已調高的價格，2026-09-09 Wupen Yuen）與產品組合（200G EML 單價約 100G 的兩倍，2026-08-27 CEO）。單點依賴屬集中度風險：前兩大客戶占 FY2026 營收 41.6%，多數客戶用採購單下單，沒有數量承諾。供需判斷：2027 年前屬結構性缺貨，2028 年起供給可逆性升高。產業態勢裁定為雙向拉鋸：光互連滲透銅線使結構轉好，中國磷化銦新廠與 Coherent 第二來源使競爭惡化，其他變數以合併案與出口管制最大。","moat":"機制是磷化銦雷射的製程經驗、規格一致性帶來的客戶良率，加上約一年的認證週期（2026-08-27 CEO，NVIDIA 認證耗時一年）。方向用利潤率對照代替 ROIC：過去 12 個月 LITE 營益率 23.35%，Coherent 14.11%，差距為正；事實表沒有同業 ROIC 與投入資本，無法驗證差距是否擴大。EML 與泵浦各約 70–80% 的份額都是管理層自述，TrendForce 的口徑是前三大合計約 72%。這項判斷會錯的情況：Coherent 遲遲過不了認證，定價面就該上調；反過來，Coherent 通過 NVIDIA 或前三大雲端認證，定價面就該下調。當期報酬、持續期與新增資本報酬分開看：當期利益率高；持續期四項檢查兩綠兩黃；新增資本報酬因缺投入資本無法計算。","growth":"成長同時靠量與價，沒有併購或回購貢獻。共識 EPS 為 FY2027E 24.83、FY2028E 39.01、FY2029E 54.41 美元，兩年年化 48.0%。FY2026 非 GAAP 全年 EPS 事實表未涵蓋，三年年化算不出；GAAP −92.96 美元含 78 億美元非現金損失，不能當基期。內生上限因缺投入資本無法計算，共識成長與上限的缺口無法量化，定性上來自利潤率擴張與缺貨定價，其餘無法歸因，長期信心上限為中。FY2028E 共識與管理層 40 美元目標幾乎重合，賣方沒有打折；營收共識 FY2027E 66.90 億、FY2028E 104.73 億美元。跑道以下一條成長曲線判定：第二個大型 NPO／CPO 訂單預期逾 50 億美元（2026-11-02 CEO），但 2026-08-27 時 CPO／NPO 尚未反映在營收。","governance":"FY2026 自由現金流 3.00 億美元，利潤率 9.96%。FY2026 GAAP 淨損 69.35 億美元含 78 億美元非現金可轉債損失，FCF／淨利轉換率沒有意義，事實表也沒有非 GAAP 全年淨利。Q3、Q4 FY2026 資本支出 1.25 億與 1.67 億美元，泵浦擴產由三年期合約分擔。現金去向四分法與債務到期結構事實表未涵蓋。Q1 FY2027 股票報酬加薪資稅 1.467 億美元占營收 11.6%，其中 8,940 萬美元是高管退休的一次性股權修改，1,420 萬美元是薪資稅，扣除後約 4,310 萬美元，占營收 3.4%。流通股增加主要來自可轉債轉股（Q4 FY2026 減債 11 億美元）與 NVIDIA 直接投資。淨負債為 −5.49 億美元；yfinance 現金 19.80 億美元低於公司 8 月所說現金及短投 27.4 億美元，兩者時點與口徑可能不同，事實表未說明。","valuation":"現價 538.59 美元對 FY2027E 21.69 倍、FY2028E 13.81 倍。較 2026-08-12 的 820.59 美元下跌 34.4%，同期 FY2027 共識由 18.73 上修到 24.83 美元。PEG 以 FY2027E 到 FY2029E 兩年年化 48.0% 計為 0.45，FY2026 非 GAAP 基期缺，不用三年口徑。五年分位事實表未涵蓋，只有四個年度端點：P/S 13.05 倍在 68.7 分位，EV/S 12.90 倍在 65.9 分位。短期上行以 12 個月後 FY2028E Base 38 美元×16 倍＝608 美元，約 +12.9%；中期以 FY2029E Base 46 美元×17 倍＝782 美元，約 +45.2%。這些都是獨立價值。循環股的優先尺是股價淨值比，事實表未涵蓋帳面淨值。現價除以 4.5 隱含 Marvell 約 119.7 美元，未扣價差；Marvell 股價與盈餘事實表未涵蓋，換股比例也來自未讀原文的聚合報導。事實表市值用 9,068 萬股，非 GAAP 稀釋股約 1.009 億股，以稀釋股計市值約 543 億美元，EV 倍數偏低約一成。","premortem":"歷史最大回撤與空方最強數字事實表未涵蓋；股價 26 週已跌 40.41%，RSI 29.51，距 52 週線 −23.9%。衰退信號亮 1 項，分母爭議未解，價值陷阱列中等。法說迴避紀錄值得記下：2026-09-09 不拆 40 美元 EPS 的毛利假設，Coherent 追上高功率雷射的時點答不知道；2026-11-02 不拆 10 億美元協同的成本占比，也不答是否有其他出價者。Q1 FY2027 完整法說不在本包，同季的管理層問答無法核對。"},"plain":{"six":{"how_it_makes_money":"Lumentum 賺的是雲端與 AI 客戶擴建光互連的錢，利潤卡在磷化銦雷射晶片這一節點。","moat":"護城河方向判為穩定：製程與產能領先還在，但定價優勢有一大部分來自缺貨，客戶已在扶植第二來源。","growth":"五年後跑道判為寬：NPO、CPO 與 OCS 已有訂單，但新一代架構目前幾乎沒有營收，要到 2027 下半年才開始驗證。","capital":"現金投向合理，擴產由客戶長約分擔；最大的一筆決定是用全股票把公司賣給 Marvell，這筆交易的價值還驗證不了。","valuation":"現價要求 FY2028 EPS 約 39 美元之後不大幅回吐，獨立看要求不高；但股東最後拿到的是 Marvell 股票，現在還無法判斷這筆換算是否划算。","how_wrong":"最可能看錯在兩處：雷射缺貨比本檔假設更早結束，以及獨立估值掩蓋了 Marvell 換股的真實價值。"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等 S-4 公開換股條款、終止費與監管條件，以 Marvell 股票口徑重算 Base 年化報酬達 12% 再重跑判斷。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":538.59,"week26_return_pct":-40.41,"consensus_rev_3m_pct":14.85,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"分母是缺貨定價下的盈餘：GAAP 毛利率兩年多內由 18.5% 升到 51%，FY2028E 又與管理層目標幾乎重合。分母是否為高點正是爭點，低倍數不能當便宜的證據。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q2 FY2027 財報，時點為本檔估計","impact":"高","watch":"毛利率是否站穩 50%、EML 出貨年增是否逾 50%、新約價格用語"},{"date":"2027Q1","date_precision":"quarter","type":"other","event":"合併案 S-4 公開，時點為本檔估計","impact":"高","watch":"換股比例、終止費、監管核准清單、出價過程與財務顧問預測"},{"date":"2027-05","date_precision":"month","type":"product","event":"FY2027 Q3 財報驗證超高功率雷射單季破億美元，時點為本檔估計","impact":"中","watch":"超高功率雷射營收與 OCS 第一供應商進度"},{"date":"2028Q1","date_precision":"quarter","type":"capacity","event":"Greensboro 磷化銦廠首批營收","impact":"高","watch":"是否延後，以及供給開出時雷射合約價的變化"},{"date":"2028Q2","date_precision":"quarter","type":"other","event":"Marvell 合併案預期於 2028 上半年交割","impact":"高","watch":"監管核准進度與交割前換股價差"}],"_projected_from":"v19"}
```
