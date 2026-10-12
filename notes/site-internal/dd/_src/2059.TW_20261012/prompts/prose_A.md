你是 stock-analyst v20 的**散文層（prose）agent**，標的 2059.TW（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2059.TW_20261012/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：2059.TW　日期：2026-10-12　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1035B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（387B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1014B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1141B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（841B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（367B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（539B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1843B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3582B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1901B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1035           4176-5965      5 條（2–6 內）  
s3                  8000         387           5329-7613      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2996          8403-12004      5 條（2–6 內）  
s6                 11000         367          7443-10633      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         539           2073-2961      5 條（2–6 內）  
s10                 5000        1843           2210-3157      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1901           2000-3099      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4011B；至少需散文≈40.99KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65
−65%
−60%
−45
−45%
−0.2
0%
0
0.33
0.48%
0.48
0.5
0.75
0.77
0.78
0.8
1%
1
1.06
1.07
1.09
1.36
2%
2
3
3%
03
3.26
3.3
4
5%
5
5.9
6
7
8
09
9
10%
10
11
11.4
12
13%
14
15%
15
17
18.5
20
20%
21
21.36
21.4
22
23%
23.7
24%
24
25
26
26%
27.0
28
28%
30
30%
30.25
30.35
35.8
40%
42
45
48.2%
49%
49
57%
57.3%
59.85
60%
64
65%
70
70%
70.9
73.5%
74%
74.7%
75%
76.1%
78.5%
80%
82%
82.1%
85%
87%
87.4%
90
98.7%
100%
100
100.7
107%
108
108.3
122%
150%
156%
218%
218.36
279
280
300
333
349.76
380
430
480
495
495.27
545
560
572.82
573
575
600
680
790
880
960
2022
2023
2024
2025
2026
2027
2028
2059
2383
3017
3533
10580.0
20261012
10,560
11,200
11,460
12,000
14,897
17,500
3,808
4,200
6,876
7,022
8,500
8,595
9,500
9,530
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
{"meta":{"ticker":"2059.TW","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"川湖科技（King Slide Works）"},"oneliner":"AI伺服器滑軌龍頭，Q2毛利率87.4%、份額約七到八成；現價已計入共識兩年EPS高成長，但大和預告輝達份額降至約75%。現價不追，等回檔或毛利率守住的證據再進。","thesis":{"H":[{"id":"H1","text":"高毛利延續：AI機櫃滑軌單季毛利率維持80%以上","2y":"單季毛利率≥80%","5y":null,"10y":null,"threshold":"單季毛利率≥80%（Q2為87.4%）","source":"公司季報與法說","drift_rule":"低於門檻5個百分點以上連2季＝削弱；低於10個百分點以上連3季＝反轉"},{"id":"H2","text":"獲利跟上基準路徑：FY2027 EPS達480元以上","2y":"FY2027 EPS≥480元","5y":null,"10y":null,"threshold":"近四季EPS對基準路徑偏離不超過5%","source":"公司季報、月營收","drift_rule":"近四季EPS低於基準路徑5%以上連2季＝削弱；10%以上連3季＝反轉"},{"id":"H3","text":"份額守住：輝達與雲端業者的AI機櫃滑軌份額維持七成以上","2y":null,"5y":"份額≥70%","10y":null,"threshold":"份額≥70%","source":"法人供應鏈調查、法說、南俊營收對照","drift_rule":"份額估計低於70%連4季＝削弱；低於60%連6季＝反轉"}],"R":[{"id":"R1","text":"輝達擴大供應商，份額降到約75%甚至更低，新供應商被拿來壓價","h_ref":"H3","clock":"⚡","threshold":"份額<70%","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"]},{"id":"R2","text":"南俊等對手產能放量，壓低價格，毛利率回落","h_ref":"H1","clock":"🔥","threshold":"單季毛利率<75%","evidence_refs":["competitive_share_entrants#3"]},{"id":"R3","text":"AI資本支出進入消化期，營收重演2023年的下滑","h_ref":"H2","clock":"🔥","threshold":"月營收年增率連3個月<0%","evidence_refs":[]},{"id":"R4","text":"生產集中台灣，美國關稅或地緣事件侵蝕毛利率","h_ref":"H1","clock":"🐢","threshold":"關稅生效後單季毛利率<75%","evidence_refs":["geo_supply_chain#1"]}],"single_thing":{"description":"輝達新一代機櫃平台滑軌認證中，川湖分配到的份額跌破60%","why_fatal":"87%毛利與30倍本益比都建立在近乎獨家供應上。份額跌破六成，代表買方已有可信替代來源，價格壓力會擴散到所有客戶，毛利率可能回到六成多，EPS下修四成以上","if_happens":"清倉；未持有則不建倉","how_monitor":"法人供應鏈調查、公司法說、南俊伺服器滑軌營收增速","probability":"約20%（大和預估已降到75%，再降15個百分點需要新平台大幅分配給第二供應商）"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.36,"peg_fy2":1.36,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":100.7,"FY2026E":349.76,"FY2027E":495.27,"FY2028E":572.82},"fy_end_month":12,"eps_basis":"新台幣；FY2025A為yfinance稀釋EPS，共識來自Koyfin快照（美元依2026-10-09匯率換算）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2059.TW_20261012/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"毛利率87%、營益率82%、淨現金約279億元、26週漲218%、份額七到八成、2023年營收曾年減26%"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉風險偏高：需求規格因機櫃重量結構性提高（Taipei Times／Counterpoint），但量隨雲端資本支出波動（2023年營收年減26%，yfinance年度財報），且對手與新供應商同步擴產","bargaining":{"up":"上游為鋼材等通用原料，供應商議價力低；採購集中度事實表未涵蓋","down":"客戶為輝達與大型雲端業者，買方高度集中；但滑軌占機櫃成本不到1%，價格敏感度低","geo":"產能集中台灣，休士頓廠2026年9月量產開始分散地緣與關稅風險"},"profit_pool_dir":"利潤池目前流向川湖（毛利率57%→87%）；輝達擴大供應商後，部分利潤將外溢給第二供應商與買方","tam_table":{"expanded":false,"reason":"事實表沒有滑軌市場規模與滲透率數據，只有份額估計；份額變化已放在護城河威脅與反證處理"}},"moat":{"mechanism":"重載滑軌設計專利（3,808件）＋機櫃共同設計與重新認證成本；滑軌占機櫃成本不到1%，客戶重品質輕價格","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價力擴大：年度毛利率2022年57.3%→2025年76.1%→Q2 87.4%，營益率TTM 74.7%對同業23%～28%。份額轉弱：大和預估輝達份額明年降至約75%（預估，尚未實現）。兩者相抵判持平","peer_na_reason":"同業表三家是AI伺服器零組件鄰業，非滑軌直接競品；直接競品南俊國際不在表內，且投入資本口徑缺，無法算報酬率差","threats":[{"level":"🔴","text":"輝達擴大滑軌供應商基礎，大和預估川湖明年份額降至約75%；新供應商認證後，客戶可用來壓價","p":"60%","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"]},{"level":"🟡","text":"南俊伺服器滑軌營收快速放量（占營收74%、Q1年增73.5%），屬點對點競爭","p":"40%","evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"同業抄襲專利並拿川湖研發成果宣傳，公司已表態走法律途徑","p":"30%","evidence_refs":["competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋；營益率TTM 74.7%）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心營運商，決策者是輝達與代工廠的機櫃設計，付款者是雲端業者。AI伺服器超過70公斤，重載滑軌是必需品；但出貨量跟雲端資本支出走，2023年營收年減26%，急迫性不等於持久性"},{"item":"決策層級","level":"🟡","text":"替代性在機櫃設計認證這一層決定，換供應商要重新認證，形成轉換成本；但最大買方輝達正主動擴大供應商基礎，降低對單一來源的依賴"},{"item":"價值鏈分配","level":"🟡","text":"滑軌占機櫃成本不到1%，客戶重品質輕價格，川湖拿到87%毛利；但買方高度集中，新供應商認證後可被拿來壓價，價值有回流買方的壓力"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的零組件，沒有民生或政治敏感性；產地集中台灣屬關稅與地緣議題，休士頓廠2026年9月量產已在分散"}],"roiic":"事實表未涵蓋（缺投入資本、折舊與營運資金）","reinvest_rate":"事實表未涵蓋；已知擴產為川益三、五期約100億元（2026年底動工）＋休士頓廠，約為FY2026E淨利（約333億元）的三成，分數年投入","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率；兩項輸入皆缺，不推估數字"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","2059.TW":81.5,"3533.TW":49.37,"3017.TW":28.87,"2383.TW":31.06,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","2059.TW":74.68,"3533.TW":27.64,"3017.TW":23.56,"2383.TW":23.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","2059.TW":41.74,"3533.TW":4.43,"3017.TW":24.1,"2383.TW":-2.9,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","2059.TW":2.25,"3533.TW":10.93,"3017.TW":3.36,"2383.TW":2.15,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3533.TW","gm":49.37,"om":27.64,"fcf_margin":4.43,"rd_intensity":10.93,"strategy_note":"連接器廠，毛利率49%、營益率28%；屬AI伺服器零組件鄰業，只作利潤率對照，沒有份額競爭","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3017.TW","gm":28.87,"om":23.56,"fcf_margin":24.1,"rd_intensity":3.36,"strategy_note":"散熱模組廠，營益率24%、自由現金流利潤率24%；同吃AI機櫃順風，與滑軌無重疊","period":"TTM ending 2026-06-30（4季加總）"},{"name":"2383.TW","gm":31.06,"om":23.05,"fcf_margin":-2.9,"rd_intensity":2.15,"strategy_note":"基板材料廠，營益率23%、自由現金流為負，擴產吃現金；對照出川湖輕資本的現金轉換","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（AI機櫃出貨）為主、價（VR滑軌單價）為輔，毛利率擴張貢獻大；無併購、無回購","runway_years":"事實表未涵蓋（無滑軌市場滲透率）","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬與再投資率皆缺，天花板不給數字；已知資本支出強度低，共識三年EPS年化78.5%明顯超出再投資能支撐的範圍，缺口歸因於毛利率擴張與產能利用率","segments":{"expanded":false,"reason":"事實表沒有分部與客戶營收占比；主力營收已確定是AI伺服器滑軌，家具與一般伺服器滑軌比重未知"},"decay_signals":[{"signal":"EPS成長顯著高於營收成長","status":"亮","note":"共識FY2025→FY2027 EPS年化約122%，營收約107%，差約15個百分點，靠毛利率擴張"},{"signal":"核心市占近12個月縮減","status":"預警","note":"大和預估輝達份額降至約75%，屬預估，尚未實現"},{"signal":"自由現金流÷淨利連2年低於0.75","status":"預警","note":"2025年為1.06，未亮；Q2單季0.33"},{"signal":"毛利率連2季年減","status":"未亮","note":"Q2毛利率87.4%，創新高"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長未依賴併購；現金去向四分事實表未涵蓋"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表未見併購紀錄","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未見回購資料","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"股權酬勞與稀釋率事實表未涵蓋；目前股數9,530萬股","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY1共識EPS 349.76元）","tier":"AI伺服器零組件高毛利龍頭","peers":{"expanded":false,"reason":"事實表的同業表只有利潤率，沒有同業倍數；直接競品南俊也不在表內，終端倍數改以自身FY3隱含18.5倍與成長熄火測試錨定"},"fwd_pe":30.35,"peg":1.09,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"前瞻30.35倍÷FY1→FY3共識EPS兩年年化約28%＝約1.09；以FY2025實際為基期的三年年化78.5%受基期低點扭曲，不採用。分位100是四個年度端點內的位置，不是連續五年分位。分母建立在87%高峰毛利率與七到八成份額上，大和已預告份額下滑，便宜論證不成立；成長熄火三情境只有一個不虧→偏貴","upside_short_pct":-0.2,"upside_mid_pct":5.9},"trap_analysis":{"verdict":"🟡","label":"高峰利潤率外推風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2023年營收年減26%；大和預告輝達份額明年降至約75%，新供應商認證後客戶可壓價","assumption":"AI機櫃需求與高峰毛利率至少延續到2028年","consequence":"2028年若進入雲端資本支出消化期，且份額落到六成，EPS回到300元上下、本益比壓到14倍，股價約4,200元（−60%）","ruling":"採納。Bear機率給30%；這條與唯一致命點（份額跌破六成）部分重疊，已補進觸發器","watch":"月營收年增率、法人份額調查","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"],"fact_refs":["f_kpi1"]},{"view":"論點成功但股東經濟變差","evidence":"南俊伺服器滑軌占營收74%、Q1年增73.5%；Q2自由現金流23.7億元，只有淨利70.9億元的三成三；擴產約100億元","assumption":"出貨量成長就等於股東報酬成長","consequence":"出貨量照樣成長，但價格被對手與第二供應商壓低，營運資金與擴產吃掉現金，每股自由現金流成長遠低於EPS","ruling":"部分採納。Base路徑較共識低3%～5%，終端倍數壓到20倍","watch":"單季毛利率、自由現金流÷淨利","evidence_refs":["competitive_share_entrants#3"],"fact_refs":["f_kpi5_ocf_capex","f_kpi4_eps"]},{"view":"價格已反映太多","evidence":"26週漲218%；落後本益比59.85倍，位於四個年度端點最高；前瞻30.35倍","assumption":"市場會繼續用30倍給高峰EPS定價","consequence":"即使EPS照共識兌現，本益比回到20倍左右，五年年化報酬只剩約3%","ruling":"採納。現價不追，設價格與毛利率雙條件才進場","watch":"股價對FY2共識倍數","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_pe_current","f_fwd_pe_latest"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 10580.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=10580.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"輝達平台份額","cause":null,"prior_field":null,"side_a":"媒體與本土券商：新世代平台份額七到八成以上，客製機櫃更高","side_b":"大和：輝達擴大供應商，明年份額降至約75%","ruling":"可調和，屬程度差異。兩邊都同意川湖目前領先，差在下滑幅度。Base採75%；份額跌破六成另列為唯一致命點","evidence_level":"二手轉述，大和原文未見","settle_metric":"2027年上半年法人供應鏈調查、南俊與川湖營收增速對照","if_then":["若南俊伺服器滑軌營收連2季增速高於川湖→減碼","若2027年上半年份額仍確認≥75%且毛利率≥80%→維持Base，不下調"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#0","competitive_share_entrants#1"]},{"axis":"估值與賣方目標價","cause":null,"prior_field":null,"side_a":"賣方目標價12,000～17,500元（Investing.com均值約14,897元），隱含較現價上漲約13%～65%","side_b":"本判斷Base：五年後約12,000元，年化報酬約3%","ruling":"⚖選本判斷這一側。依據：賣方目標是FY2027–28共識EPS乘20～30倍，等於延續高峰毛利率與份額；硬數據點是大和的75%份額預估，以及Q2自由現金流只有淨利三成三。現在就買的最強論證：對FY2共識只有21倍，淨現金約279億元，RSI已回到35.8。執行：不追，等價格或證據","evidence_level":"賣方報告二手轉述","settle_metric":"Q3、Q4單季毛利率與法人份額調查","if_then":["若股價≤8,500元且最近一季毛利率≥80%→分批反買首倉","反向：若Q3與Q4毛利率都≥85%且法人確認份額≥80%→上修Base，等價線上移至9,500元"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"獲利品質","cause":null,"prior_field":null,"side_a":"Q2淨利70.9億元","side_b":"Q2自由現金流23.7億元（營業現金流27.0億元、資本支出3.3億元）","ruling":"可調和。營收季增98.7%時，應收與存貨先墊款，2025全年自由現金流為淨利的1.06倍；但若Q3仍低於0.5，代表收款條件或庫存出問題","evidence_level":"財報數字，營運資金明細事實表未涵蓋","settle_metric":"Q3、Q4自由現金流÷淨利","if_then":["若Q3、Q4自由現金流÷淨利都低於0.5→停止加碼並下調品質分","若Q3回到0.8以上→移除此疑慮"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q3財報單季毛利率是否守住80%以上","type":"假設驗證","maps_to":"H1","metric":"單季毛利率","threshold":"≥80%","action":"守住則維持觀望、等價格；低於75%則停止加碼","source_freq":"公司季報，每季","date":"2026-11"},{"n":2,"text":"輝達新平台滑軌份額跌破六成","type":"Single Thing","maps_to":"Single Thing","metric":"輝達平台滑軌供應份額（法人調查或公司揭露）","threshold":"<60%","action":"清倉；未持有則不建倉","source_freq":"法人報告與法說，每季","date":"2027-12","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"]},{"n":3,"text":"股價回到FY2共識EPS約17倍以下，且毛利率守住","type":"估值rearm","maps_to":"H1","metric":"股價與最近一季毛利率","threshold":"股價≤8,500元且毛利率≥80%","action":"重跑研究後分批反買首倉","source_freq":"每日股價、每季財報","date":null},{"n":4,"text":"南俊伺服器滑軌營收成長連2季快於川湖","type":"風險","maps_to":"R2","metric":"南俊與川湖季營收年增率差","threshold":"南俊高於川湖連2季","action":"減碼","source_freq":"月營收公告，每月","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":5,"text":"月營收年增率轉負","type":"風險","maps_to":"R3","metric":"月合併營收年增率","threshold":"連3個月<0%","action":"減碼","source_freq":"公開資訊觀測站，每月10日前","date":null},{"n":6,"text":"自由現金流跟不上淨利","type":"風險","maps_to":"H2","metric":"單季自由現金流÷淨利","threshold":"<0.5連2季（Q2為0.33）","action":"停止加碼","source_freq":"公司季報，每季","date":"2026-11"},{"n":7,"text":"美國對台灣製伺服器零組件加徵關稅，毛利率未能吸收","type":"風險","maps_to":"R4","metric":"單季毛利率","threshold":"關稅生效後毛利率<75%","action":"減碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":8,"text":"FY2026年報與2027年展望","type":"複審日期","maps_to":null,"metric":"全年EPS對共識349.76元","threshold":"偏離≥10%","action":"重跑研究","source_freq":"年報","date":"2027-03"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"<75%連2季","window":"2026Q3至2027Q4","source":"公司季報與法說","last_status":"ok"},{"metric":"輝達平台滑軌份額","bear_threshold":"<60%","window":"12～24個月","source":"法人供應鏈調查、法說","last_status":"warning"},{"metric":"月合併營收年增率","bear_threshold":"連3個月<0%","window":"2026-10至2027-12","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"單季自由現金流÷淨利","bear_threshold":"<0.5連2季","window":"2026Q3至2027Q2","source":"公司季報現金流量表","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方用FY2027–28共識EPS給12,000～17,500元目標價，等於假設87%毛利率與八成份額延續；大和已預告輝達份額降至約75%，新供應商認證後客戶可壓價，共識尚未反映"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=218.36, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價≤8,500元（約FY2共識EPS 17倍）且最近一季毛利率≥80%，重跑研究後才建首倉","exec_line":"現價不追。跌到8,500元以下且Q3或Q4毛利率≥80%，分兩筆分批反買；份額跌破60%，或毛利率連2季低於75%，則不建倉"},"reasoning":{"industry":"Q2營收108.3億元，年增156%；毛利率87.4%，營益率82.1%，稅後淨利70.9億元。年度毛利率從2022年57.3%一路升到2025年76.1%，今年再上一層。管理層指引下半年營收較上半年成長，全年毛利率80%以上。產能利用率七到八成，逼近九成。休士頓廠2026年9月量產，川益三、五期約100億元預計年底動工。分部與客戶占比事實表未涵蓋，只能從媒體得知主要客戶為輝達與大型雲端業者，單點依賴集中在輝達機櫃平台。產業時鐘判在過熱段，依據是供給端而非股價：營收年增三位數、毛利率創歷史新高，對手（南俊伺服器滑軌占營收74%、Q1年增73.5%）與新供應商同步擴產。供需持久性：AI伺服器超過70公斤，重載規格門檻是結構性提高；但出貨量跟著雲端資本支出走，2023年營收曾年減26%，週期反轉風險偏高。產業態勢屬雙向拉鋸：需求結構轉好（重載與單價提升），競爭面惡化中（輝達擴大供應商基礎）。","moat":"機制：3,808件專利加上機櫃共同設計與認證，客戶換供應商要重新認證；滑軌成本占比低，客戶不值得為省錢冒品質風險。執行力給8分：產能快速擴充、休士頓廠如期量產；扣分在Q2自由現金流只有淨利的三成三，產地仍集中台灣。定價力給8分：營益率TTM 74.7%，同業表三家只有23%～28%；扣分在大和指出新供應商通過認證後，客戶可拿來壓價。同業表三家都是AI伺服器零組件鄰業，不是滑軌直接競品，只能用利潤率代替報酬率差；投入資本口徑事實表未涵蓋，無法算報酬率差。份額下滑目前是券商預估、尚未實現，所以趨勢判持平而非向下；若法人調查確認份額跌破七成，趨勢改判向下。","growth":"成長以量為主（AI機櫃出貨），單價為輔（法人預估VR機櫃滑軌單價再升一成），毛利率擴張貢獻很大；沒有併購，也沒有回購。共識EPS由FY2025實際100.7元到FY2028E 572.82元，三年年化約78.5%；FY1到FY3兩年年化約28%（Koyfin快照，美元換算）。內生天花板無法計算，因為投入資本與折舊事實表未涵蓋。但資本支出強度低（Q2資本支出3.26億元，對營收108億元），即使增量報酬極高，靠再投資撐得住的成長也遠低於78.5%。缺口來自毛利率擴張（57%→87%）與產能利用率拉升的營運槓桿，屬週期性來源，不能外推，所以情境樹的Bear機率提高到30%。衰退信號亮一個：共識EPS成長明顯高於營收成長（FY2025→FY2027 EPS年化約122%，營收年化約107%）。另有預警：Q2自由現金流只有淨利的三成三。","governance":"自由現金流÷淨利：2022年0.77、2023年1.07、2024年0.78、2025年1.06，長期現金轉換良好。Q2單季只有0.33（營業現金流27.0億元、資本支出3.3億元，對淨利70.9億元），推測是營收季增98.7%時應收與存貨先墊款，但營運資金明細事實表未涵蓋。現金去向四分事實表未涵蓋，已知用途是川益三、五期約100億元與休士頓廠。營運槓桿為正：營益率由2022年48.2%升到TTM 74.7%，沒有利益率壓縮。","valuation":"前瞻本益比30.35倍。對FY2共識EPS約21.4倍，對FY3約18.5倍。落後本益比59.85倍，位於四個年度端點最高。賣方目標價12,000～17,500元（Investing.com均值約14,897元），另一聚合站7,022元，日期不明、應已過時，不採用。賣方目標建立在高峰毛利率延續上。成長熄火壓力測試以FY2028共識573元為基：三年後成長降到15%、給20倍，約11,460元；降到10%、給15倍，約8,595元；降到5%、給12倍，約6,876元。三情境只有一個不虧，Bear本益比錨定在14倍。現在就買的最強論證：對FY2共識只有21倍，淨現金約279億元，RSI已回到35.8，7月單月營收64億元若延續，FY2027可能超越共識。我判斷這些都依賴分母不被份額與價格侵蝕，因此不追。","premortem":"往下看錯：雲端資本支出進入消化期，加上輝達第二供應商放量，EPS可能回到300元上下，本益比壓到14倍。往上看錯：VR機櫃單價提升、休士頓廠擴產順利，份額維持八成，FY2027 EPS超越共識。兩邊的決勝數據都是未來兩季的毛利率與法人份額調查。"},"plain":{"six":{"how_it_makes_money":"川湖賺的是AI機櫃組裝方（輝達平台與大型雲端業者）的重載滑軌錢。錢卡在機櫃設計認證這一節點，滑軌又只占機櫃成本不到1%，所以收得到87%毛利。","moat":"護城河持平。設計專利與機櫃認證帶來的定價力仍在擴大，毛利率由57%升到87%；但最大客戶正在引入第二供應商，兩股力量相抵。","growth":"五年後跑道中等。份額已七到八成，再成長只能靠AI機櫃市場本身擴大，未見有來源的第二條成長曲線。","capital":"資本配置以保留現金為主。淨現金約279億元，沒有併購也沒有回購，股息殖利率0.48%；三項計分中兩項不適用，股權稀釋事實表未涵蓋。","valuation":"現價要求FY2027、FY2028共識EPS（495元、573元）兌現，之後還要有雙位數成長，等於假設87%毛利率與八成份額都能維持。份額這一段我不信，基準情境的五年年化報酬只有低個位數。","how_wrong":"最可能看錯的方向是把高峰毛利率當常態；反過來，若AI機櫃需求與份額同時延續，本判斷會錯過上漲。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方用FY2027–28共識EPS給12,000～17,500元目標價，等於假設87%毛利率與八成份額延續；大和已預告輝達份額降至約75%，新供應商認證後客戶可壓價，共識尚未反映","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤8,500元（約FY2共識EPS 17倍），且Q3財報毛利率≥80%","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":10580.0,"week26_return_pct":218.36,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY1到FY3共識EPS建立在87%毛利率與約八成份額上；大和預估輝達份額降至約75%，新供應商可壓價，分母本身就是爭點。短期上檔＝Base FY2027 EPS 480元×22倍≈10,560元；中期上檔＝Base FY2029 EPS 560元×20倍≈11,200元"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3財報與法說，驗證毛利率與下半年營收","impact":"高","watch":"單季毛利率是否≥80%、自由現金流÷淨利"},{"date":"2026-Q4","date_precision":"quarter","type":"capacity","event":"休士頓廠量產爬坡，川益三、五期動工","impact":"中","watch":"美國廠出貨占比、產能利用率"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026年報與2027年展望","impact":"高","watch":"全年EPS對共識349.76元"}],"_projected_from":"v19"}
```
