你是 stock-analyst v20 的**散文層（prose）agent**，標的 TSM（2026-09-16）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20260916/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：TSM　日期：2026-09-16　archetype：None　前份裁決：2026-08-08　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1893B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（713B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（993B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1444B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（957B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（329B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（659B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1728B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4519B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2769B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1893           3575-5107      5 條（2–6 內）  
s3                  8000         713           5101-7287      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3394          8124-11606      5 條（2–6 內）  
s6                 11000         329          7470-10671      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         659           1989-2841      5 條（2–6 內）  
s10                 5000        1728           2290-3272      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2769           2000-2231      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4697B；至少需散文≈40.30KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−52%
−50%
−50
−45%
−37%
−35%
−35
−29%
−5%
−1.5%
0%
0
0.2
0.62
0.75
0.82
0.9
1
1%
01
1.5%
2
2.91%
2.93%
3
03
3%
3.5
4
4%
5%
5
5.9%
6
06
6.3
07
7
8.0
08
8
8.1
9%
09
9
9.65%
10
10%
11.4
12%
12
12.3
13.0%
13
14
14.4
15
15%
15.7%
16
16%
16.5
17%
17.05
17.6
18
18%
18.3
18.35
18.5
19%
19.5
19.87
19.9%
20
$20
20%
21%
21.0
21
22%
22.5
22.55
24%
24
24.27
24.3
24.5
25%
25.3%
25.4
26
27.9
28%
28
28.65
29.6
29.6%
30%
30
31.0
32
32.4
33%
34%
35%
36.3
38%
38.5
40%
40
$40.2
41.9%
42
44.2%
$44.6
45.5
45.8
47.0
47
49
50%
52
55%
56.1%
60%
$60
60
60.3%
63%
64
64%
$64
65%
65
65.2%
65.7%
66%
67%
67.7%
70
70%
72.3%
72.5%
72.6%
77%
78%
81.4%
90
90%
92%
93%
100%
100
$100
110
$110
120%
150%
156
$198
232
250
$259
$265
287
$288
$294
$346
$360
$361
$413.75
413.75
$420.04
420.04
$433.24
$451
451
496
$554
$573
573
783
$1222
$1300
2025
2026
2027
2028
2029
2030
20260909
20260916
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
{"meta":{"ticker":"TSM","date":"2026-09-16","schema":"v15.2","contract":"v19","company_name":"Taiwan Semiconductor Manufacturing Company"},"oneliner":"AI 先進製程供不應求延續至 2027 之後、代工份額創高 72.5%、2026 營收指引上修至 40% 以上（來源：摘要）；FY2026 共識本益比約 24.3x 對兩年 EPS 複合約 30% 不貴，核心倉進場、分兩批建：首批現在，第二批等 250 週均線斜率回到 +3% 以上或回檔至 $361 以下；唯一致命點是台灣本島產能的地緣事件。","thesis":{"H":[{"id":"H1","text":"AI 先進製程與 CoWoS 需求超過供給延續至 2027 之後，2026 營收成長 40% 以上兌現、毛利率守住 65%","2y":"FY2026 營收成長 ≥40%（美元）且 Q3 毛利率 ≥65%；FY2027 共識 22.55 不被下修超過 5%","5y":null,"10y":null,"threshold":"FY2026 營收成長 ≥40%；季毛利率 ≥65%；FY2027 共識 90 天修正 ≥ −5%","source":"公司季報與指引（2026-07-16）；Koyfin 共識快照（f_consensus_rev_3m_fy1_pct、f_consensus_eps_fy2）；supply_demand_durability#0","drift_rule":"TTM 偏離門檻連 2 季 ≥5% 削弱、連 3 季 ≥10% 反轉"},{"id":"H2","text":"製程與良率領先維持份額與定價：2nm 放量後 A14 於 2028 接棒，代工份額守住 70% 以上","2y":null,"5y":"份額 ≥70%（TrendForce）；A14 2028 量產不延誤超過 2 季；毛利率扣除新節點稀釋後 ≥63%","10y":null,"threshold":"份額 ≥70%；A14 量產延誤 ≤2 季；毛利率 ≥63%","source":"TrendForce 份額（competitive_share_entrants#0）；法說 A14 進度（逐字稿 2026-07-16）；季報毛利率","drift_rule":"連 4 季 ≥5% 削弱、連 6 季 ≥10% 反轉"},{"id":"H3","text":"資本支出換得營收成長且股東回報不被稀釋：海外廠稀釋不超過管理層口徑、股息逐年增、FCF 利潤率三年均值守住 20%","2y":null,"5y":null,"10y":"海外廠毛利率稀釋 ≤4pp；每股股息年年增（2026 TWD 24）；FCF 利潤率三年均值 ≥20%","threshold":"海外稀釋 ≤4pp；股息不減；FCF 利潤率 3 年均 ≥20%","source":"法說管理層口徑（逐字稿 2026-07-16）；季報現金流（f_kpi2_fcf、f_peer_tsm_fcf_margin_pct）","drift_rule":"跨 2 年度偏離削弱、跨 3 年度反轉"}],"R":[{"id":"R1","text":"2nm 爬坡稀釋 3–4pp 疊加消費端與價格敏感市場疲軟，毛利率跌破管理層口徑","h_ref":"H1","clock":"⚡","threshold":"毛利率連兩季低於 64%（排除匯率）即減碼一半","evidence_refs":["end_markets#4"]},{"id":"R2","text":"Apple 與 Intel 18A 初步協議、探索三星第二來源，加上前十大客戶 78%、最大 19% 的集中度，使單一客戶轉單即可傷及份額與定價","h_ref":"H2","clock":"🔥","threshold":"單一旗艦客戶轉單超過 20% 配額，或 Apple 18A 產品量產出貨，連 4 季才大動作","evidence_refs":["competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#0"]},{"id":"R3","text":"地緣與法規：約 92% 先進產能在台灣本島、海外 2028 前不成規模、晶片製造耗電占全台 18%、台灣研議對中出口管制刑事化","h_ref":"H1","clock":"🐢","threshold":"受限中國先進製程營收超過 5%、限電影響交期，或台海事件；事件機率 ≥50% 才砍倉","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#2"]},{"id":"R4","text":"資本支出 $60–64B（來源：摘要）且下三年更高，若 2027–2028 AI 資本支出回落，折舊壓毛利率、稼動率下滑","h_ref":"H1","clock":"🔥","threshold":"FY2027 資本支出再上修但營收成長指引低於 20%","evidence_refs":["capital_markets_pricing#2","competitive_share_entrants#1"]}],"single_thing":{"description":"台海封鎖或軍事衝突導致台灣本島先進製程停產或大規模斷電","why_fatal":"5nm 以下約 92% 產能在台灣、海外先進製程 2028 前不成規模、晶片製造耗電占全台 18%；這不是壓 EPS 兩三成，而是營收歸零期，且無法用分散持股消除","if_happens":"清倉全部部位，不等季報","how_monitor":"公司公告、封鎖或軍事行動新聞、台灣電力供應公告；亞利桑那與日本先進製程量產進度作為緩解指標","probability":"12–24 個月低於 10%（事實表無量化來源，屬判斷）"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.35,"peg_fy2":0.62,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"fy1":17.05,"fy2":22.55,"fy3":28.65,"fy1_label":"FY2026E","fy2_label":"FY2027E","fy3_label":"FY2028E","cagr_fy1_fy3_pct":29.6,"source":"Koyfin 快照 2026-09-09（DD_universe_EPS_estimates_20260909.xlsx），ADR 口徑（普通股 ×5）","analyst_count":"事實表未涵蓋家數"},"fy_end_month":12,"eps_basis":"台灣 IFRS 單一口徑，ADR 每股（普通股 ×5）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20260916/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"高毛利、資本密集、份額 72.5% 的獨占型代工，成長靠先進製程量與 ASP，無併購無回購"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：管理層需求能見度至 2029–2030、新廠 2–3 年無捷徑（逐字稿；supply_demand_durability#0、#1）；先進製程需求為可供產能 110–120%（competitive_share_entrants#1）","bargaining":{"up":"設備端單一來源且通膨推高工具價格（逐字稿：資本支出上修部分原因是通膨），資本強度由台積電吸收","down":"前十大客戶 78%、最大 19%（customer_concentration_credit#0），但需求超過產能，定價主動權在台積電、公司自我設限不推到上限","geo":"5nm 以下約 92% 產能在台灣本島，海外先進製程 2028 前不成規模（geo_supply_chain#0、#1）"},"profit_pool_dir":"AI 半導體利潤池向記憶體（MU 營益率 65.7%）與加速器（NVDA 65.2%）傾斜，代工端 56.1% 居中；先進封裝首度外溢給封測廠但主體仍在台積電","tam_table":[{"item":"全球晶圓代工份額（2026 Q2）","value":"72.5%，季增 0.2pp，創歷史新高；三星 5.9%（competitive_share_entrants#0）"},{"item":"HPC 平台佔營收","value":"66%（Q2 2026），季增 20%；智慧型手機 22%、IoT 5%、車用 4%、DCE 1%（逐字稿）"},{"item":"CoWoS 供需（2026）","value":"需求約 100 萬片對供給 60–70 萬片，缺口延至 2027 底（channel_business_model_shift#1）；年底月產能 13 萬片、已售罄（channel_business_model_shift#2）"},{"item":"利潤池 5 年遷移","value":"事實表未涵蓋 5 年前營業利益池占比，無法計算淨流出 pp"}]},"moat":{"mechanism":"多年設計導入與產能協同的轉換成本＋製程良率領先（N2 放量、A14 2028、A13／A12 2029），使客戶在供不應求下仍無法快速轉單","execution":10,"pricing":8,"combined":9.0,"score":9.0,"grade":"A","trend":"↑","trend_evidence":"代工份額 72.3%→72.5% 創高（TrendForce，2026-09-10）；2nm 帶動出貨量與 ASP 同步上升；毛利率 67.7% 創高；Apple 佔比下滑為 Nvidia 成長稀釋而非份額流失（customer_concentration_credit#1）","peer_na_reason":"事實表同業表為客戶（NVDA、AVGO、AMD）與記憶體（MU），無先進代工同業 ROIC；改以份額軸","threats":[{"level":"🟡","text":"Apple 以 Intel 18A 生產部分 Apple Silicon 的初步協議，可能結束近乎單一代工依賴；短期為備援或低量次要來源","p":"35%","evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"level":"🟡","text":"前十大客戶 78%、最大單一客戶 19%（由 12% 升），集中度為 Nvidia 資本支出週期敞口","p":"n/a（結構性敞口）","evidence_refs":["customer_concentration_credit#0"]},{"level":"🟡","text":"先進封裝首度委外封測廠與 Intel EMIB-T 取得注意，長期可能分走封裝環節價值；公司主動歡迎以紓解瓶頸","p":"20%","evidence_refs":["channel_business_model_shift#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（營益率 TTM 56.1%，資本密集，需查再投資負擔與資產更新週期）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是 AI 模型與雲端服務、決策者是晶片設計商、付款者是雲端服務商，三角色皆成立；管理層核對資料中心進度以確認晶片不進庫存；缺口延至 2027 之後（supply_demand_durability#0）"},{"item":"決策層級","level":"🟢","text":"決策最小單位是單一產品的製程選定，轉換需約 5 年設計導入（逐字稿）；代理讀數為 Apple 探索第二來源仍被視為備援而非主力（customer_second_source#0），漲價後未見流失"},{"item":"價值鏈分配","level":"🟡","text":"整條 AI 鏈中記憶體（MU 營益率 65.7%）與加速器（NVDA 65.2%）分得更多，代工 56.1%；公司刻意不把價格推到上限以維持客戶成功，等於用利潤率換持續期；先進封裝外溢降低自身環節議價"},{"item":"社會容忍度","level":"🟡","text":"美國 232 關稅以在美建廠換豁免（reg_tariff_export#0）、亞利桑那投資累計 $265B 屬政治保費；台灣研議對中出口管制刑事化（reg_tariff_export#2）；執行長明言不會 4–5 倍提價，實際定價上限低於經濟上限"}],"roiic":"事實表未涵蓋（缺投入資本、折舊與增量營業利益口徑）","reinvest_rate":"事實表未涵蓋（Q2 毛資本支出 NT$496B ÷ 營運現金流 NT$783B ≈ 63% 只是資本強度代理，未扣折舊、未用投入資本口徑，不是再投資率）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率；增量 ROIC 無法自事實表推得，天花板留空，情境樹以保守假設（共識超過天花板）處理"},"spread_table":[{"metric":"毛利率","TSM":64.23,"NVDA":74.67,"AVGO":68.77,"AMD":53.2,"MU":72.57,"unit":"%"},{"metric":"營業利益率","TSM":56.1,"NVDA":65.21,"AVGO":48.52,"AMD":15.71,"MU":65.67,"unit":"%"},{"metric":"FCF 利潤率","TSM":25.33,"NVDA":41.92,"AVGO":44.22,"AMD":20.34,"MU":28.99,"unit":"%"},{"metric":"研發密度","TSM":6.07,"NVDA":7.79,"AVGO":13.28,"AMD":22.74,"MU":5.3,"unit":"%"}],"competitors":[{"name":"NVDA","gm":74.67,"om":65.21,"fcf_margin":41.92,"rd_intensity":7.79,"strategy_note":"最大客戶（19%）而非同業，營益率 65.2% 高於台積電 56.1%，顯示設計端分走較大利潤，但鎖定 CoWoS 過半產能","period":"TTM ending 2026-07-31（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"strategy_note":"客戶端，FCF 利潤率 44.2% 對台積電 25.3%，反映輕資產設計商與重資產代工的分工","period":"TTM ending 2026-07-31（4季加總）"},{"name":"AMD","gm":53.2,"om":15.71,"fcf_margin":20.34,"rd_intensity":22.74,"strategy_note":"營益率 15.7%，前三大客戶之一，完全依賴台積電先進製程","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MU","gm":72.57,"om":65.67,"fcf_margin":28.99,"rd_intensity":5.3,"strategy_note":"記憶體同業營益率 65.7%、毛利率 72.6%，執行長明說羨慕；顯示 AI 利潤池此刻偏向記憶體，代工端有未收割的定價空間","period":"TTM ending 2026-05-31（4季加總）"}]},"growth":{"driver_mix":"量為主（先進製程晶圓＋CoWoS 產能，2nm 家族產能 2026–2028 複合成長高於 70%）、價次之（2nm ASP 上升）、無併購、無回購","runway_years":"事實表未涵蓋滲透率；以需求能見度至 2029–2030 與 A14 2028 量產推估 5 年以上","runway_post_y5":"🟢","endo_ceiling_basis":"內生天花板無法自事實表推得（缺增量 ROIC）；再投資率代理約 63%；共識兩年複合 29.6% 視為超過天花板，缺口無法歸因","segments":[{"item":"HPC","value":"66% 營收，季增 20%（Q2 2026）"},{"item":"智慧型手機","value":"22%，季減 4%"},{"item":"IoT","value":"5%，季增 4%"},{"item":"車用","value":"4%，季增 15%"},{"item":"DCE","value":"1%，季增 5%"}],"seven_questions":[],"decay_signals":["FCF 對淨利疑似低於 0.75（TTM FCF 利潤率 25.3% 對營益率 56.1%）——門檻需連兩年、事實表僅一年，且資本支出為擴產性質，列疑似不計入"],"trap_rating":"🟢"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長非靠併購；現金回饋僅股息（2026 每股 TWD 24、年增 33%，逐字稿），無回購"},"scorecard":[{"year":"—","action":"ma_roiic","rationale":"無併購（逐字稿明確不做客戶財務安排）","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"無回購，現金全數投入擴產與股息（2026 每股 TWD 24）","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"員工酬勞為現金紅利，佔營收 2.93%（H1 2026），股權稀釋約 0%","grade":"過"}],"sbc":{"note":"台灣公司法員工現金紅利，非股權稀釋；佔營收 2.93%（H1 2026）"},"capalloc_grade":"B"},"valuation":{"basis":"FY2026 共識 EPS 17.05（Koyfin 2026-09-09，ADR 口徑）對現價 $413.75 ＝ 24.3x；兩年共識 EPS 複合 29.6%","tier":"品質複利成長","peers":{"expanded":false,"reason":"事實表未涵蓋同業前瞻倍數，僅有利潤率對照；終端倍數的同業對照標為資料缺口"},"fwd_pe":24.27,"peg":0.82,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 24.3x 對複合 29.6%、PEG 0.82 偏便宜；trailing 本益比在 4 年度端點分位 100% 與 26 週 +19.9% 偏貴；兩者相抵為合理，且五年分位事實表未涵蓋不能判便宜","targets":{"short_12m":451,"mid_3y":573,"basis":"FY2027 EPS 22.55 × 20x；FY2028 EPS 28.65 × 20x"},"upside_short_pct":9.0,"upside_mid_pct":38.5},"trap_analysis":{"verdict":"🟢","label":"成長型資本密集，非價值陷阱；唯一疑似訊號為擴產期 FCF 轉換率"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"先進製程需求為可供產能 110–120%，三星與 Intel 不需搶客戶即可受惠；Apple 與 Intel 18A 初步協議；前十大客戶 78%、最大 19%。替代技術軸與重大事件軸：本份查詢不切題（替代技術只查到台積電自家 GAA 與背面供電，重大事件查到與半導體無關的 FDA 警告信），這兩軸事實表未涵蓋，不能寫「沒有」，列為採證缺口。前份追蹤的出口管制調查（Sophgo 案、罰款超過 $20 億或新增全面出口限制的門檻）本份採證包沒有後續，同列採證缺口，門檻沿用前份","assumption":"缺口收斂速度慢於新產能開出，客戶不會在 2027–2028 把第二來源量產化","consequence":"5 年後虧 50% 的故事：2027 AI 資本支出回落，Intel 18A 承接 Apple 與溢出訂單，$64B 資本支出變折舊，稼動率跌破 90%，毛利率回到 55%，倍數壓至 12x","ruling":"部分採納：不改方向，但空頭機率上調至 30%、終端空頭倍數 14x；與唯一致命點（地緣事件）獨立，不重疊。兩軸缺口與出口管制調查未查，是採證缺口而非已證無事，本輪無工具不補數字","watch":"最大客戶轉單配額、Apple 18A 量產時點、FY2027 共識 90 天修正方向；下份採證必補三項：非台積電路線的替代技術（Intel 18A、三星 SF2 的密度與良率）、半導體相關重大事件、Sophgo 出口管制調查結果與罰款金額","not_applicable_reason":null,"evidence_refs":["competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#0","competitive_share_entrants#1"],"fact_refs":["f_consensus_rev_fy2_pct"]},{"view":"論點成功但股東經濟變差","evidence":"2026 資本支出 $60–64B、下三年更顯著高於過去三年；海外廠稀釋毛利率 2–4pp；亞利桑那累計 $265B；TTM FCF 利潤率 25.3% 對 NVDA 41.9%、AVGO 44.2%；先進封裝首度外溢","assumption":"資本支出能在 2028 後轉成營收，海外廠稀釋不超過管理層口徑","consequence":"營收與 EPS 兌現但 FCF 轉換率停在五成、股息成長慢於 EPS、倍數因資本強度上升而不擴張","ruling":"採納為情境樹中基本情境倍數由 24.3x 降至 21x 的理由；不採納為迴避理由，因股息仍年增 33%","watch":"FCF 利潤率 3 年均值是否守住 20%；海外廠稀釋是否超過 4pp","not_applicable_reason":null,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","channel_business_model_shift#0"],"fact_refs":["f_peer_tsm_fcf_margin_pct","f_kpi2_fcf"]},{"view":"價格已反映太多","evidence":"trailing 本益比 31.0x 在 4 年度端點分位 100%、P/S 分位 100%、26 週 +19.9%、賣方共識目標價 $554（以判斷日現價 413.75 計 +34%）已計入 40% 成長","assumption":"2027 共識 22.55 是市場基準，不是上限","consequence":"若 2027 成長從 40% 減速至 30%，倍數由 24x 壓至 18x 就抵掉一年 EPS 成長，股價原地或下跌","ruling":"反駁大半：前瞻 FY2027 18.3x、PEG 0.82，共識近三月上修 9.65% 未見頂；保留為分批建倉的理由","watch":"FY2027 共識修正轉負、RSI 高於 70 且 4 週漂移超過 +10%","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_pe_percentile","f_ps_percentile","f_week26_return_pct","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 420.04 → 本次 413.75（-1.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=420.04","side_b":"本次 price_at_dd=413.75","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：裁決方向、角色、估值結論、陷阱、護城河方向、跑道、商業型態與前份相同","cause":"新證據","prior_field":["dca_verdict","signal","val","trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份 2026-08-08：進場、核心、護城河向上、跑道寬、估值合理","side_b":"本份：進場、核心、護城河向上、跑道寬、估值合理；新一季證據為份額 72.5% 創高、2026 指引上修至 40% 以上、CoWoS 售罄至年底、A14 進度超前","ruling":"基本面各項維持不變；新證據全部同向，無一項要求降位。均線由排列完成轉為長期斜率未達 +3%，依規則不改裁決與角色，只反映在分批建倉的第二批條件","evidence_level":"公司季報＋第三方份額","settle_metric":"Q3 2026 營收與毛利率是否落在指引","if_then":["若 Q3 營收低於 $44.6B 且毛利率低於 65%，停止加碼","若 Q3 落在指引內，第二批依估值或均線條件執行"],"evidence_refs":["competitive_share_entrants#0","end_markets#1","channel_business_model_shift#2"]},{"axis":"判斷日現價由 $420.04 降至 $413.75，基本情境內部報酬率隨起始價重算","cause":"價格變動","prior_field":["irr_base_pct"],"side_a":"前份現價 $420.04、基本情境內部報酬率 13.0%","side_b":"本份現價 $413.75，內部報酬率由情境腳本以新起始價重算","ruling":"價格下跌 1.5% 不改基本面結論，只影響起始價與由此重算的內部報酬率。裁決與角色維持進場、核心；均線六態改由程式計算（見本區第一條方法變動條目）只影響第二批建倉的時點，不影響裁決。前份均線判讀的依據本份採證包未保存，不對前份 250 週斜率是否達標下結論。","evidence_level":"程式計算","settle_metric":"—","if_then":["若價格跌破 52 週均線 $360 但基本面無損，分批反買而非停損"],"evidence_refs":[]},{"axis":"方法與情境改寫：內生天花板無法自事實表推得，共識視為超過天花板，空頭機率由 25% 上調至 30%、多頭由 30% 降至 28%；情境 EPS 與終端倍數重寫，多頭五年由 $1300 改為 47.0 × 26x ＝ $1222、空頭五年由 $288 改為 21.0 × 14x ＝ $294；不對稱比 8.0→6.3、五年期望值 93%→81.4%；最大回撤由單點 −45% 改為 −35% 至 −50% 範圍；產業循環位置首次填入","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct","cycle_position","asym_ratio","ev5y_pct","bull_5y_price","bear_5y_price"],"side_a":"前份多頭 30%、空頭 25%、多頭五年 $1300、空頭五年 $288、不對稱 8.0、五年期望值 93%、最大回撤 −45%、循環位置未填","side_b":"本份多頭 28%、空頭 30%、多頭五年 $1222、空頭五年 $294、不對稱 6.3、五年期望值 81.4%、最大回撤 −35% 至 −50%、循環位置中循環","ruling":"五年終點價不隨現價變動，所以不對稱比與期望值下降不是價格原因：用本份價位配前份機率，不對稱仍約 8.1，降到 6.3 幾乎全來自機率改寫與情境 EPS／倍數重寫。空頭機率上調掛兩個理由：一是反證「論點失敗」部分採納（Apple 18A 與溢出承接），二是天花板算不出。天花板一旦算出且共識在內，只解除第二個理由；第一個理由要等 Apple 18A 到 2027 底仍為備援才解除，兩者都解除才回 25%","evidence_level":"方法","settle_metric":"增量 ROIC 與再投資率是否可自財報推得；Apple 18A 量產配額","if_then":["若天花板算出且共識在內、且 Apple 18A 至 2027 底仍為備援，下份空頭機率回 25%","若任一理由仍在，維持 30%"],"evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"axis":"加碼門檻變動：前份加碼窗口以 FY2027 前瞻 16x（約 $346）或毛利率條件表述，本份改為 FY2027 共識 22.55 × 16x ≈ $361 或均線斜率回升條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"回檔至 Fwd PE(FY27) ≤16x（約 $346）或連兩季 GM 低於 65% 之外的加碼窗口","side_b":"FY2027 共識 EPS 22.55 × 16x ≈ $361 以下加碼，或 250 週均線斜率回到 +3% 以上且毛利率連兩季 ≥66% 時加碼","ruling":"FY2027 共識由前份基準上修至 22.55，同一 16x 倍數對應價位由 $346 升至 $361；毛利率條件由「不低於 65%」改為「連兩季 ≥66%」以對齊 Q3 指引中點","evidence_level":"Koyfin 共識快照＋公司指引","settle_metric":"FY2027 共識 EPS 與 250 週均線斜率","if_then":["若價格回到 $361 以下且基本面無損，加碼至倉位上限","若均線斜率回升但價格高於 $451，不追"],"evidence_refs":[]},{"axis":"清倉與減碼門檻新增：前份未列出可執行的致命指標清單，本份新增四條清倉／減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份無","side_b":"毛利率連兩季低於 64% 減碼一半；最大客戶轉單超過 20% 配額減碼；FY2027 共識 90 天下修超過 10% 減碼；台海封鎖或衝突清倉","ruling":"前份門檻散落於假設區，本份集中列出；毛利率門檻統一為 64%，與風險 R1 及觸發器同一數字，對齊 Q3 指引 65–67% 扣除新節點稀釋；客戶門檻對齊 20-F 客戶揭露","evidence_level":"方法","settle_metric":"各條指標按窗口回報","if_then":["任一條觸發即執行對應動作，不再評估"],"evidence_refs":[]},{"axis":"Single Thing 新增：前份未填唯一致命點，本份填為台灣本島先進製程停產事件","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份無","side_b":"台海封鎖或軍事衝突導致台灣本島先進製程停產或斷電（92% 先進產能在台灣、海外 2028 前不成規模）","ruling":"這是數學上最大的單一敏感度項：其他風險壓 EPS 兩到三成，此事件直接讓營收歸零期出現；機率低但不能用分散消除","evidence_level":"第三方彙整","settle_metric":"事件本身","if_then":["若發生，清倉全部部位"],"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"⚖ 不可調和矛盾：份額創高 72.5% 對 Apple 探索 Intel 18A 第二來源，方向相反","cause":"新證據","prior_field":[],"side_a":"份額 72.3%→72.5%、2nm 放量、A14 客戶投片提前，護城河向上","side_b":"Apple 與 Intel 18A 初步協議、探索 Intel 與三星，護城河可能在 2027 後受損","ruling":"選 A 側：協議未量產、分析師判為備援或低量次要來源，且轉單需約 5 年設計導入；硬數據點為 Apple 佔營收 17%，即使 20% 配額轉出也只影響營收約 3%","evidence_level":"報導（WSJ 轉引）對第三方份額統計","settle_metric":"Apple 18A 量產配額與台積電在 Apple 的份額","if_then":["若 Apple 18A 量產配額超過 20%，減碼至一半並重評護城河方向","若 2027 底前 18A 仍為備援且份額維持 70% 以上，維持核心倉並依均線或估值條件補足第二批"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","customer_second_source#0"]},{"axis":"現在就賣的最強論證（進場方 steelman）","cause":null,"prior_field":[],"side_a":"trailing 本益比在 4 年度端點分位 100%、26 週 +19.9%、資本支出下三年更顯著高於過去三年，2027 成長減速時倍數與 FCF 同時承壓","side_b":"前瞻 FY2027 18.3x、PEG 0.82、共識近三月上修 9.65%、需求能見度至 2029–2030","ruling":"賣方論證成立於「2027 減速」而非「2026 見頂」，因此以分批建倉與 90 天共識修正門檻處理，不以賣出處理","evidence_level":"事實表估值欄","settle_metric":"FY2027 共識 90 天修正","if_then":["若 FY2027 共識 90 天下修超過 10%，減碼"],"evidence_refs":["capital_markets_pricing#0"]}],"triggers":[{"n":1,"text":"Q3 2026 營收與毛利率落在指引，驗證需求超過供給假設","type":"假設驗證","maps_to":"H1","metric":"Q3 營收與毛利率","threshold":"營收 ≥ $44.6B 且毛利率 ≥65%","action":"通過則第二批依估值或均線條件執行；未通過停止加碼","source_freq":"季報","date":"2026-10-16","type_display":null,"evidence_refs":["end_markets#1"]},{"n":2,"text":"2nm 稀釋與消費端疲軟壓毛利率超過管理層口徑","type":"風險","maps_to":"R1","metric":"毛利率（排除匯率）","threshold":"連兩季低於 64%","action":"減碼至目標倉位一半","source_freq":"季報","date":"2027-01","type_display":null,"evidence_refs":["end_markets#4"]},{"n":3,"text":"Apple 或最大客戶把 Intel 18A 第二來源量產化","type":"風險","maps_to":"R2","metric":"最大客戶轉單配額","threshold":"單一旗艦客戶轉單超過 20% 配額，或 Apple 18A 量產產品出貨","action":"減碼至一半並重評護城河方向","source_freq":"年報客戶揭露＋產業報導","date":"2027-03","type_display":null,"evidence_refs":["competitive_share_entrants#2","customer_second_source#0","customer_concentration_credit#0"]},{"n":4,"text":"台海封鎖或軍事衝突導致台灣本島先進製程停產","type":"Single Thing","maps_to":"single_thing","metric":"事件","threshold":"封鎖、衝突或本島先進製程廠停產超過 30 天","action":"清倉全部部位","source_freq":"事件","date":null,"type_display":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":5,"text":"台灣對中 AI 晶片出口管制刑事化定案，或本島電力不穩影響交期","type":"風險","maps_to":"R3","metric":"受限中國先進製程營收占比；限電導致交期延誤","threshold":"受限營收超過 5%，或管理層在法說承認限電影響交期","action":"凍結加碼並重跑情境樹；受限營收與交期延誤同時成立則減碼至一半","source_freq":"法規公告＋季報","date":"2026-12","type_display":null,"evidence_refs":["reg_tariff_export#2","geo_supply_chain#2"]},{"n":6,"text":"回檔到 FY2027 共識 16x 加碼第二批","type":"估值rearm","maps_to":"q5_valuation","metric":"FY2027 共識前瞻本益比","threshold":"價格 ≤ $361（22.55 × 16x）且基本面無損","action":"加碼至倉位上限","source_freq":"每週","date":null,"type_display":null,"evidence_refs":[]},{"n":7,"text":"250 週均線斜率回到 +3% 以上且動能未過熱","type":"加碼","maps_to":"decision_inputs","metric":"250 週均線 13 週斜率；RSI 14","threshold":"斜率 ≥ +3% 且 RSI 低於 70 且價格低於 $451","action":"補足第二批至倉位上限","source_freq":"每週","date":null,"type_display":null,"evidence_refs":[]},{"n":8,"text":"FY2027 共識 EPS 90 天內大幅下修","type":"減碼","maps_to":"H1","metric":"FY2027 共識 EPS 90 天修正","threshold":"下修超過 10%","action":"減碼至一半","source_freq":"Koyfin 快照每月","date":null,"type_display":null,"evidence_refs":[]},{"n":9,"text":"資本支出再上修但成長指引減速，折舊拖累風險上升","type":"風險","maps_to":"R4","metric":"FY2027 資本支出指引與營收成長指引","threshold":"資本支出上修且 2027 營收成長指引低於 20%","action":"停止加碼並重跑情境樹","source_freq":"1 月法說","date":"2027-01","type_display":null,"evidence_refs":["capital_markets_pricing#2"]},{"n":10,"text":"Q3 2026 法說後複審","type":"複審日期","maps_to":"全份","metric":"複審","threshold":"2026-10-16 法說後兩週內","action":"重跑判斷","source_freq":"季","date":"2026-10-30","type_display":null,"evidence_refs":[]}],"kill_metrics":[{"metric":"毛利率（排除匯率，含 2nm 稀釋後）","bear_threshold":"連兩季低於 64%","window":"2 季","source":"公司季報","last_status":"ok"},{"metric":"最大客戶轉單至 Intel 18A 或三星的配額","bear_threshold":"單一旗艦客戶轉單超過 20% 配額","window":"4 季","source":"20-F 客戶揭露＋產業報導","last_status":"warning"},{"metric":"FY2027 共識 EPS 90 天修正","bear_threshold":"下修超過 10%","window":"90 天","source":"Koyfin 月度快照","last_status":"ok"},{"metric":"台海封鎖或衝突導致本島先進製程停產","bear_threshold":"停產超過 30 天","window":"事件","source":"公司公告＋新聞","last_status":"ok"}],"evidence_dismissed":[{"ref":"$.answers.q2_moat.verdict_values.moat.roic_durability","reason":"事實表沒有投入資本、折舊與增量營業利益的口徑，增量 ROIC、再投資率與內生天花板無法列出算式；補算式等於編數字，違反不得編造的規則。本份已明標為資料缺口，並以共識超過天花板、空頭機率 30%、長期信心中作保守處理，情境樹三條路徑價差實質、期望值與不對稱可複算，未因缺口退化。"},{"ref":"前份 H3：出口管制調查（Sophgo 案、罰款超過 $20 億或新增全面出口限制）","reason":"本份 12 軸採證包沒有這項調查的後續，事實表也沒有罰款或調查結果的數字；本輪修補無工具，不能補查也不能編結論。改列為盲點區的採證缺口與追蹤項，沿用前份門檻（罰款超過 $20 億或新增全面出口限制），下份採證必查。"}],"decision_out":{"verdict":"進場","role":"核心","row_hit":"10","pacing":[],"holding_cap":"-","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=本份在數字上沒有和市場對賭：基本情境 FY2027 EPS 22.5 與共識相同、FY2028 27.9 略低於共識 28.65，12 個月目標 $451 也低於賣方共識目標 $554。市場錯的地方不在 EPS，而在持續期：市場把 2026 年 40% 以上成長當成週期高點，因此只給 FY2027 18x；本份依需求缺口為可供產能 110–120%、新廠 2–3 年無捷徑、管理層需求能見度至 2029–2030，判為供給受限的多年結構，用 21x 終端倍數與 10% 第二階段成長表達，而不是用更高的 EPS。裁決不依賴估值再評價。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟢', val='🟡', moat_trend='↑', week26=19.87, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='A', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":true,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"10-verdict","condition":"命中 row10 → 進場","hit":true,"basis":"row_hit=10"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"FY2027 共識 EPS 22.55 × 16x ≈ $361 以下，或 250 週均線斜率回到 +3% 以上且毛利率連兩季 ≥66%","exec_line":"現價 $413.75、FY2026 共識 24.3x：核心倉分兩批，首批現在建至核心倉位一半；第二批等 250 週均線斜率回到 +3% 以上且 RSI 低於 70，或回檔至 $361 以下；價格高於 $451 不追"},"reasoning":{"industry":"最新一季營收 $40.2B 落在指引上緣，毛利率 67.7%、營益率 60.3% 創歷史新高（季報）。7nm 以下佔晶圓營收 77%，HPC 平台季增 20% 佔 66%，智慧型手機降至 22%（季報），公司收入結構已由 AI 資料中心主導。供需：管理層直言需求缺口「很大」、AI 晶片短缺可能延續到 2027 之後、需求能見度至 2029–2030（逐字稿與 supply_demand_durability#0），先進製程需求達可供產能的 110–120%（competitive_share_entrants#1），新廠要 2–3 年、供給可逆性低，判為結構性持久。議價權：對客戶端錢卡在台積電，但公司自我設限（執行長明說不會把價格推到 4–5 倍，逐字稿）；對供應商端設備通膨推高資本支出，2026 資本支出上修至 $60–64B（來源：摘要）。單點依賴：前十大客戶佔 FY2025 營收 78%、最大單一客戶 19%，這是集中度風險而非護城河證據，落在風險 R2。產業態勢三軸：A 競爭惡化——Intel 18A 取得 Apple 初步協議並有美國政策支持；B 結構轉好——需求超過產能、缺口延至 2027 之後、2nm 首季貢獻 3% 晶圓營收；C 其他結構變數——美國 232 關稅框架與台灣研議對中出口管制收緊。裁決：雙向拉鋸，以結構性轉好為主軸，依據為 TrendForce 份額 72.5% 創高（competitive_share_entrants#0）與 2026 指引兩度上修至 40% 以上（end_markets#1；來源：摘要）。Q3 指引營收 $44.6–45.8B、毛利率 65–67%（來源：摘要）。","moat":"機制是 5 年設計導入與產能協同形成的轉換成本（執行長：選代工不是到 7-Eleven 買牛奶，需要約 5 年）加上技術與良率領先（2nm 首季 3% 晶圓營收，A14 內部載具 SRAM 良率近 90%、客戶投片提前，2028 量產）。可證方向取份額軸：72.3%→72.5% 創高、與三星差距擴至 12.3 倍（competitive_share_entrants#0）。獲利對照：營益率 TTM 56.1% 對 AMD 15.7%，落後記憶體 MU 65.7% 與 NVDA 65.2%，執行長直言羨慕記憶體毛利率，這證明定價權存在但由公司自我設限，故定價權給 8 不給 10。Apple 佔營收由 22% 降至 17% 是 Nvidia 升至 19% 的稀釋效應，不是台積電在 Apple 的份額下滑，因此仍可標向上；Apple 與 Intel 18A 的初步協議（competitive_share_entrants#2、customer_second_source#0）尚未量產，屬點對點威脅，機率取破壞性競爭下限以上的 35%。先進封裝外溢給封測廠（channel_business_model_shift#0）由公司主動歡迎，前段晶圓與後段封裝是兩件事（逐字稿），不視為護城河損傷。當期 ROIC 落在高利益率×低周轉象限（Q2 資本支出 NT$496B 對營運現金流 NT$783B），四檢查點兩綠兩黃。增量 ROIC 與內生天花板：事實表未涵蓋投入資本與折舊口徑，不能自算，標資料缺口；再投資率以逐字稿毛資本支出除以營運現金流作代理。","growth":"成長靠量（先進製程晶圓與 CoWoS 產能，2nm 家族產能 2026–2028 複合成長高於 70%，逐字稿）為主、價（2nm ASP 上升）次之，無併購無回購。三年共識 EPS：FY1 17.05、FY2 22.55、FY3 28.65（Koyfin 2026-09-09 快照，ADR 口徑），FY1→FY3 兩年複合 29.6%；近 90 天 FY1 共識上修 9.65%，方向與公司指引一致。缺口＝共識複合成長減內生天花板，天花板無法自事實表算出，缺口無法歸因，依規則加註「依賴再評價」並將長期信心上限設為中；情境樹將共識視為超過天花板，空頭機率上調至 30%。Runway：滲透率數字事實表未涵蓋，以管理層需求能見度至 2029–2030 與 A14 2028 量產推估 5 年以上；下一條曲線有來源（逐字稿）。衰退訊號：FCF 對淨利疑似低於 0.75（TTM FCF 利潤率 25.3% 對營益率 56.1%），但門檻需連兩年、事實表僅一年且資本支出為擴產性質，列疑似不計入。","governance":"Q2 營運現金流 NT$783B、資本支出 NT$496B、自由現金流 NT$287B（f_kpi2_fcf），發放 NT$156B 股息，季末現金與有價證券 NT$3.5T（約 $110B）。TTM FCF 利潤率 25.3%，對淨利轉換率約一半，原因是 2026 資本支出上修至 $60–64B（來源：摘要）且下三年「更顯著高於」過去三年（逐字稿），屬擴產性質而非維持性。股息 2025 年每股 TWD 18、2026 年 TWD 24（+33%），2027 承諾續增。員工酬勞現金紅利佔營收 2.93%（H1 2026），為台灣公司法利潤分配，非股權稀釋。計分：併購不適用（無併購）、回購不適用（無回購，現金全數投入擴產與股息）、稀釋通過。營運槓桿為正（營收成長 40% 以上、營益率創高），無成長熄火跡象。","valuation":"現價 $413.75 對 FY2026 共識 EPS 17.05 為 24.3x、對 FY2027 22.55 為 18.3x、對 FY2028 28.65 為 14.4x；FY1→FY3 兩年複合 29.6%，PEG 約 0.82。事實表最近快照前瞻本益比 25.4x（快照價 $433.24）。歷史尺：trailing 本益比 31.0x 在 4 個年度端點中為最高分位 100%，P/S 分位 100%，但這不是五年分位，五年分位事實表未涵蓋，留空；EV/S 為負值屬資料異常不採用。同業倍數事實表未涵蓋，終端倍數的同業對照標為資料缺口。上檔：12 個月以 FY2027 EPS 22.55 × 20x ＝ $451（+9%）；3 年以 FY2028 EPS 28.65 × 20x ＝ $573（+38%）。26 週報酬 +19.9%、RSI 45.5 不過熱；週線均線排列完成但 250 週均線 13 週斜率 2.91% 未達 +3%。分母無爭議：共識由公司指引兩度上修支撐。","premortem":"空方最強數字：先進製程需求為可供產能 110–120%，代表三星與 Intel 只要承接溢出就能成長，供給缺口一旦收斂，台積電失去定價與稼動率雙重支撐；2026 資本支出 $60–64B 加下三年「更顯著高於」過去三年，折舊在 2028 起壓毛利率。反證裁定見反證區三視角，價值陷阱判斷引用該紀錄：衰退訊號 0 個確認、1 個疑似，判綠。管理層在法說未正面回答三年資本支出數字、AI 五年複合成長數字與 $100B 亞利桑那時程，屬未證監測項。歷史最大回撤與訴訟金額事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺的是 AI 加速器與 CPU 設計商（Nvidia、Apple、Broadcom、AMD）為先進製程與先進封裝付的錢，錢卡在 3nm／2nm 晶圓與 CoWoS 兩個供不應求的節點；產業時鐘在擴張期第二階段，供需屬結構性持久而非短週期。","moat":"護城河方向向上：份額創高、2nm 已放量、A14 進度超前；執行力 10 分、定價權 8 分（公司刻意不推到經濟上限），等級 A；最大客戶的第二來源探索是點對點威脅，未量產前不改方向。","growth":"五年後跑道寬：A14 2028、A13／A12 2029 與 Agentic AI CPU 是有來源的下一條曲線，需求能見度至 2029–2030；缺口歸因因內生天花板無法計算而不完整，長期信心上限為中。","capital":"資本配置紀律高：現金流全數投入擴產與穩定增加的股息，無併購無回購，員工酬勞為現金紅利不稀釋股權；代價是 FCF 轉換率在資本支出週期偏低。","valuation":"現價要求 2027 年 EPS 22.55 兌現且 2028 仍有兩成以上成長；我信，因為 2026 指引已上修至 40% 以上且共識近三月只上修不下修；估值判為合理，不是便宜，也不是貴。","how_wrong":"最可能看錯的是把週期高點當成結構：若 2027–2028 AI 資本支出回落，$60–64B 的資本支出變成折舊拖累、稼動率下滑；其次是 Apple 與 Intel 18A 量產化；最致命但最低機率是台灣地緣事件。"}},"decision_inputs":{"signal":"A","ma":"🟡","cycle_position":"中循環","cycle_verdict":"右側可追蹤","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"本份在數字上沒有和市場對賭：基本情境 FY2027 EPS 22.5 與共識相同、FY2028 27.9 略低於共識 28.65，12 個月目標 $451 也低於賣方共識目標 $554。市場錯的地方不在 EPS，而在持續期：市場把 2026 年 40% 以上成長當成週期高點，因此只給 FY2027 18x；本份依需求缺口為可供產能 110–120%、新廠 2–3 年無捷徑、管理層需求能見度至 2029–2030，判為供給受限的多年結構，用 21x 終端倍數與 10% 第二階段成長表達，而不是用更高的 EPS。裁決不依賴估值再評價。","momentum_overheated":false,"cycle_gates_pass":null,"trap":"🟢","val":"🟡","moat":"A","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":413.75,"week26_return_pct":19.87,"consensus_rev_3m_pct":9.65,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"共識 EPS 由公司 2026 指引兩度上修支撐；EV/S 負值為事實表資料異常不採用；五年分位未涵蓋"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"Q3 2026 法說：營收 $44.6–45.8B 與毛利率 65–67% 是否兌現、2027 資本支出方向","impact":"高","watch":"毛利率是否守住 65%；資本支出是否再上修"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"台灣對中 AI 晶片出口管制收緊是否定案","impact":"中","watch":"受限客戶範圍與受影響營收占比"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"Intel 18A-P 量產與 Apple 初步協議是否轉為量產訂單","impact":"中","watch":"Apple 產品配額與台積電在 Apple 的份額"},{"date":"2027-01","date_precision":"month","type":"capacity","event":"2027 資本支出指引與亞利桑那 $100B 追加投資時程","impact":"中","watch":"資本支出對營收成長的比例"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"A14 預生產啟動（2028 量產前一年）","impact":"中","watch":"良率與客戶投片是否維持超前"}],"_projected_from":"v19"}
```
