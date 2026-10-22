你是 stock-analyst v20 的**散文層（prose）agent**，標的 COF（2026-10-22）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：COF　日期：2026-10-22　archetype：None　前份裁決：2026-07-22　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1696B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（402B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（901B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1447B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（826B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（565B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1086B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2114B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4135B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2100B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1696           3713-5304      5 條（2–6 內）  
s3                  8000         402           5319-7598      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3174          8278-11826      5 條（2–6 內）  
s6                 11000         565          7304-10435      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1086           1690-2414      3 條（2–6 內）  
s10                 5000        2114           2020-2886      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2100           2000-2900      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4402B；至少需散文≈40.60KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−52%
−35%
−35
−27%
0.0
0%
0.2%
0.3
0.51
0.59
0.7%
01
1
1%
1.08
1.1
1.48%
1.5%
1.548%
1.55
1.55%
1.7
$2.0
2%
2
2.25
2.4%
2.4
2.65
2.68
2.9%
03
3
3.3
3.98%
4
4.03
4.1
4.25
4.31%
4.44%
4.44
4.5%
4.71%
4.9
5
5%
5.0%
5.25%
5.5%
06
6%
6
6.6
07
7
7%
7.5
8
8%
8.41%
8.59
8.6
8.7%
8.8
9
09
10%
10
10.05
10.6
11
11.0%
11%
11.4
12
12%
12.0%
13
13%
13.8%
14
14%
14.2%
14.2
14.4
14.7
15%
15
16.9%
17%
17.5
17.8%
18
18.5
20%
20
20.2
20.56
20.8
21
22
22%
23
23.6
24
24.07
24.6
25
25%
26
26.6
27.5
28.08
28.7
28.7%
28.8
29
30%
30
31
31.3
32.5
35
35%
36
39.3%
39.6%
40
42
48.76%
49
49%
50
50%
51.5
54.0%
54.19%
58.6
60%
65
65.61%
70
75
88%
90
100
100%
105
150%
150
163
180
$180
190
206.22
206.66
230
236
250
259
266
360
432
433
640.6
675.5
2008
2024
2026
2027
2028
20261022
1,060
1,910
4,625
4,807
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
{"meta":{"ticker":"COF","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"Capital One Financial Corporation"},"oneliner":"Discover 綜效進度超前、卡信用處低點；前瞻本益比約 10 倍只要求盈餘持平，主要尾部是聯邦利率上限與信用循環轉向","thesis":{"H":[{"id":"H1","text":"Discover 併購綜效如期兌現：合併綜效年化由 2026 Q3 的 18 億美元升到 2027 年底 25 億美元，扣掉交換費和解損失後，盈餘能力仍符合交易時預期","2y":"2027 年底綜效年化 ≥25 億美元；FY2027 EPS ≥23 美元","5y":null,"10y":null,"threshold":"2027 Q2 財報綜效年化 ≥22 億美元；FY2027 EPS ≥23 美元","source":"季度法說會綜效進度、新聞稿 EPS","drift_rule":"綜效或季度 EPS 低於路徑 5% 以上連 2 季為削弱；低於 10% 以上連 3 季為反轉"},{"id":"H2","text":"國內卡信用維持良性：2027 年季度淨沖銷率不超過 5.0%，逾期率年比不轉升","2y":"2027 年國內卡年度淨沖銷率 ≤5.0%","5y":null,"10y":null,"threshold":"國內卡季度淨沖銷率 ≤5.0%；季末逾期率年比變動 ≤+30bp","source":"公司季度新聞稿與月度信用資料","drift_rule":"季度沖銷率超出門檻 5% 以上（>5.25%）連 2 季為削弱；>5.5% 連 3 季為反轉"},{"id":"H3","text":"自有網路放大規模：信用卡開始轉到 Discover 網路，網路交易量維持兩位數成長，Discover 卡放款 2027 下半年恢復正成長","2y":"Discover 卡放款 2027 Q4 年比轉正","5y":"信用卡轉網後，網路交易量年複合成長 ≥15%","10y":null,"threshold":"網路交易量年增 ≥15%（Q3 為 25%，主因借記卡轉網）；Discover 卡放款年減幅逐季收斂","source":"法說會消費金融網路交易量、Discover 卡放款年比","drift_rule":"連 4 季低於門檻 5% 以上為削弱；連 6 季低於門檻 10% 以上為反轉"}],"R":[{"id":"R1","text":"信用循環轉向：逾期改善已轉為只跟季節性，回收順風預期一年內退坡，車貸次級占比回到疫情前；CECL 下準備金一次補提，EPS 會跌得比 2008 年更陡","h_ref":"H2","clock":"🔥","threshold":"國內卡逾期率年比轉升 ≥30bp 連 2 季，或季度沖銷率 >5.5%","evidence_refs":["financial_capital_credit_cycle#0"]},{"id":"R2","text":"監管尾部：聯邦 10% 利率上限提案、Visa／Mastercard 交換費和解（11 月終審）、商家交換費反壟斷訴訟；監管機關也可能限制併購與擴張","h_ref":"H1","clock":"🐢","threshold":"利率上限法案出委員會；和解生效後交換費損失大於剩餘綜效","evidence_refs":["supply_demand_durability#1","regulatory_antitrust#1","regulatory_antitrust#2"]},{"id":"R3","text":"競爭吃掉綜效：大型同業資金成本更低、高端卡行銷競爭，公司 2027 年要再加碼行銷；新支付業者（穩定幣、代幣化存款）攻網路端","h_ref":"H1","clock":"🔥","threshold":"2027 調整後效率比率高於 2026；行銷年增持續高於營收年增 5pp 以上","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"id":"R4","text":"Discover 放款緊縮拖長：7 月法說說谷底約在今年第四季，10 月改口為未來數季續縮再轉正；Brex 收購另有消費者反壟斷訴訟；Q1 財報曾低於預期","h_ref":"H3","clock":"⚡","threshold":"Discover 卡放款 2027 Q2 年減仍 ≥2%","evidence_refs":["regulatory_antitrust#3","capital_markets_pricing#5"]},{"id":"R5","text":"法律與營運：Discover 卡片誤分類（已提列 12 億美元、SEC 調查中）、回饋取消與錯誤註記集體訴訟、360 儲蓄 4.25 億美元和解；核心系統多在 AWS，雲端中斷風險；關稅衝擊車市","h_ref":"H1","clock":"🐢","threshold":"單案罰款或和解 >10 億美元，或 SEC 調查轉正式執法","evidence_refs":["major_events#0","major_events#2","major_events#3","lawsuit_class_action#0","lawsuit_class_action#1","sec_investigation_restatement#0","geo_supply_chain#0","reg_tariff_export#0"]}],"single_thing":{"description":"聯邦信用卡利率 10% 上限立法通過","why_fatal":"國內卡收入率 17.8%、淨利差 8.41% 主要靠循環利息；10% 上限讓次級與近優級客群無法定價，KPMG 指出會導致核貸緊縮、信用可得性下降，卡業務盈餘大幅下降（幅度事實表未涵蓋）","if_happens":"法案出委員會即減碼一半；任一院通過即清倉","how_monitor":"S.381／H.R.1944 委員會進度、期中選舉後國會組成","probability":"12–24 個月約 5%（法案尚未出委員會）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":8.59,"peg_fy2":0.51,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":4.03,"FY2026E":20.56,"FY2027E":24.07,"FY2028E":28.08},"fy_end_month":12,"eps_basis":"Koyfin 共識（事實表未標明 GAAP 或調整後）；基期 FY2025A 為 GAAP 稀釋 EPS 4.03，含 Discover 併購一次性費用與準備金首提，不宜作成長基期，成長改看 FY2026→FY2028"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/scenario.json","archetype":{"primary":"金融","secondary":null,"confidence":"高","fingerprint":"發卡行＋全國數位零售銀行＋自有支付網路"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：管理層 Q3 法說稱逾期改善已轉為只跟季節性，Q2 法說稱回收庫存一年內退坡","bargaining":{"up":"資金端：零售存款 4,807 億美元大於放款，管理層稱存款保險覆蓋比例高、客戶關係深，對資金供給方議價強","down":"持卡人換卡成本低，靠回饋與高端權益留客；商家透過反壟斷訴訟與和解壓縮交換費","geo":"業務集中美國；英國、加拿大已有交換費上限先例"},"profit_pool_dir":"網路端利潤池（Visa 營業利益率 65.61%）透過轉網部分收回；發卡端交換費池受和解與訴訟壓縮","tam_table":{"expanded":false,"reason":"美國信用卡為成熟市場，成長來自份額、網路量與高端客群而非滲透率；事實表未涵蓋市場規模與份額數據"}},"moat":{"mechanism":"規模化資料核貸與即時風控、自有 Discover 支付網路、無分行的全國數位銀行低成本存款，三者疊加","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力擴大：綜效年化 18 億美元超前、Discover 新發卡 100% 上公司系統、國內卡沖銷率年降 65bp；定價權縮減：交換費和解將下調收入、行銷年增 14% 高於國內卡營收年增 5%、利率上限提案未解；兩者相抵判持平","peer_na_reason":"同業對照只有現金流利潤率，對銀行無意義；同業 ROTCE 與有形淨值報酬事實表未涵蓋","threats":[{"level":"🔴","text":"監管攻擊整個生態：10% 利率上限提案與交換費和解直接壓縮發卡經濟，監管也可能限制併購與擴張","p":"10%","evidence_refs":["supply_demand_durability#1","regulatory_antitrust#2","regulatory_antitrust#1"]},{"level":"🟡","text":"高端卡行銷競爭：規模更大、資金成本更低的同業持續重金投入，公司 2027 年要再加碼行銷","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"新支付業者（穩定幣、代幣化存款、代理商務）攻網路端；BofA 研究認為較屬估值壓力而非基本面","p":"15%","evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（淨利差 8.41%，資產負債表重）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是持卡人；消費支付與短期信用是需要不是想要。Q3 購買量年增 11%，舊 Capital One 卡放款年增約 6%"},{"item":"決策層級","level":"🟡","text":"替代性要在單一消費者的錢包層衡量：換卡成本低，但回饋點數、高端權益與主要存款帳戶綁定提高黏著；借記卡轉網後管理層稱客戶量有保住，但流失率數據事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"交換費池由網路、發卡行、商家三方分；擁有 Discover 網路後可同時拿發卡與網路兩端，但商家反壟斷訴訟與 Visa／Mastercard 和解在壓縮整個池子，且多數交換費以回饋轉給消費者"},{"item":"社會容忍度","level":"🔴","text":"高利率信用卡是政治敏感產品：10% 利率上限法案、遲繳費規則、交換費訴訟同時存在；實際定價上限由政治決定，低於經濟上限"}],"roiic":"約 20%（法說會分析師推估的報酬量級，管理層未確認；股東權益事實表未涵蓋）","reinvest_rate":12,"endo_ceiling":2.4,"formula_note":"內生成長＝增量報酬約 20%×再投資率約 12%＝約 2.4%（總盈餘口徑）；再投資率＝1−（Q3 回購 26 億＋股息約 4.9 億）÷Q3 淨利 35 億；股息以殖利率 1.548%×市值估算"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","COF":null,"AXP":null,"JPM":null,"C":null,"V":80.18,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","COF":null,"AXP":null,"JPM":null,"C":null,"V":65.61,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","COF":47.95,"AXP":19.82,"JPM":-83.39,"C":-26.88,"V":47.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"AXP","gm":null,"om":null,"fcf_margin":19.82,"strategy_note":"高端卡最強對手，閉環網路加高消費客群；公司往上打高端客群必然正面碰撞，行銷成本由此墊高","period":"TTM ending 2026-06-30（4季加總）"},{"name":"JPM","gm":null,"om":null,"fcf_margin":-83.39,"strategy_note":"規模與資金成本優勢最大的發卡行，正是 10-K 點名的大型對手類型；現金流利潤率為負是銀行口徑，不可比","period":"TTM ending 2026-06-30（4季加總）"},{"name":"C","gm":null,"om":null,"fcf_margin":-26.88,"strategy_note":"大型發卡同業，以聯名卡為主；現金流指標同樣不適用於比較","period":"TTM ending 2026-06-30（4季加總）"},{"name":"V","gm":80.18,"om":65.61,"fcf_margin":47.23,"strategy_note":"原本收網路費的一方；公司把借記卡與部分信用卡轉到自有網路，等於從它手上拿回網路端分潤，其營業利益率顯示這塊利潤池之厚","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（卡購買量、車貸、存款、網路交易量）＋併購綜效（成本與網路經濟）＋淨回購；價（收益率）中性偏壓，交換費和解將下調","runway_years":"事實表未涵蓋滲透率與份額，無法估算","runway_post_y5":"🟡","endo_ceiling_basis":"內生成長上界約 2.4%（增量報酬約 20%×再投資率約 12%，總盈餘口徑）；共識 EPS 年增約 17% 的缺口歸因淨回購與利潤率（綜效、信用正常化），不依賴重估","segments":[{"item":"國內卡","value":"Q3 營收年增 5%、購買量年增 11%、期末放款年增約 2%（扣除 Discover 約 6%）、收入率 17.8%"},{"item":"消費金融（車貸、零售存款、網路）","value":"Q3 營收年增約 17%、放款年增約 13%、車貸撥款年增 22%、網路交易量約 1,910 億美元年增 25%"},{"item":"商業銀行","value":"Q3 營收季增 6%、放款季增約 1%、沖銷率 0%"},{"item":"分部營收占比","value":"事實表未涵蓋"}],"decay_signals":["EPS 成長顯著高於營收成長：亮（共識 FY2027 EPS 年增 17%，營收年增 5%）","核心市占近 12 個月縮減：部分亮（Discover 舊卡放款年減 2.9%、購買量持平；舊 Capital One 卡放款年增約 6%）","毛利率連 2 季年減：不適用，銀行看淨利差，Q3 8.41% 季增 40bp","現金轉換與 SBC 類訊號：不適用或事實表未涵蓋","產業估值倍數近 3 年系統性下移：事實表未涵蓋"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"Q3 回購","value":"26 億美元"},{"item":"CET1","value":"13.8%；管理層稱長期需求 11%，不急著壓低"},{"item":"股息殖利率","value":"約 1.55%（過去 12 個月）"},{"item":"Brex 收購","value":"51.5 億美元（27.5 億現金＋約 1,060 萬股），2026-06-30 完成"},{"item":"壓力測試","value":"嚴重不利情境 CET1 最低 11.0%；壓力資本緩衝 4.5% 維持至 2027-09-30"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Discover 綜效年化 18 億美元超前，管理層稱盈餘能力符合交易時預期；但併購投入資本與實現報酬事實表未涵蓋，待 2027 完整年度驗證","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"Q3 回購 26 億美元；買入收益率約 10%（1÷前瞻本益比 10.05）；10 年期殖利率事實表未涵蓋，低於 8% 即過","grade":"過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 事實表未涵蓋；淨股數因回購下降，Brex 發行約 1,060 萬股，無法拆出 SBC 本身稀釋率","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY2026 共識 EPS）為主；有形淨值倍數事實表未涵蓋","tier":"美國大型發卡行","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比或有形淨值倍數；現金流利潤率對銀行無意義，不作估值錨"},"fwd_pe":10.05,"peg":0.59,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比 10.05 倍÷FY2026→FY2028 共識 EPS 年增約 16.9%＝PEG 約 0.59；扣除準備金釋出後約 10.6 倍，仍只隱含盈餘持平；短期上行＝基本情境 FY2027 EPS 23.6×10 倍＝236 美元（+14.2%），中期＝FY2028 EPS 26.6×10 倍＝266 美元（+28.7%）；五年分位事實表只有四個年度端點、基期失真，不採用","upside_short_pct":14.2,"upside_mid_pct":28.7},"trap_analysis":{"verdict":"🟡","label":"中度陷阱風險：盈餘高點含準備金釋出與回收順風，EPS 成長遠高於營收成長"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"逾期改善自 6 月起只跟季節性（Q2、Q3 法說），回收庫存預期一年內退坡，車貸次級占比回到疫情前；Q2 合併淨沖銷率年增 18bp","assumption":"失業率上升使國內卡沖銷率 2028 年升到 7% 以上，CECL 下一次補提準備金","consequence":"FY2028 EPS 跌到約 15 美元、本益比 7 倍，股價約 105 美元，五年虧損近 50%","ruling":"部分採納：已放進熊情境（機率 30%、FY2028 EPS 15）；目前國內卡逾期率仍年減 15bp，沒有轉向證據，不據此迴避","watch":"國內卡逾期率年比轉升連 2 季","evidence_refs":["financial_capital_credit_cycle#0"],"fact_refs":["f_kpi5_provision_for_credit_los"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 行銷年增 14%，CEO 稱 2027 年更用力投行銷、網路與 AI；剩餘綜效與交換費和解損失大致抵銷；10-K 稱大型對手資金成本更低","assumption":"綜效全數到位，但被行銷競爭與交換費下調吃掉，調整後效率比率停在 49% 上下","consequence":"EPS 成長只剩回購貢獻（每年約 6%），本益比不重估，五年報酬約每年 8%","ruling":"採納：基本情境 FY2027 EPS 23.6 低於共識 24.07，終端本益比不給重估","watch":"調整後效率比率；行銷年增對營收年增的差距","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#0","regulatory_antitrust#2"],"fact_refs":["f_kpi4_efficiency_ratio_gaap"]},{"view":"價格已反映太多","evidence":"FY2026 共識含今年準備金釋出；Q3 是季節性強季；FY2028 共識年增 17% 高於營收 5%；Q1 調整後 EPS 曾低於共識（來源品質低，待核）","assumption":"市場已按綜效全到位加信用持續良性定價","consequence":"若盈餘只維持目前水準，股價沒有上行空間","ruling":"反駁：前瞻本益比 10 倍只隱含盈餘持平，扣掉準備金釋出約 10.6 倍。現在就賣的最強論證是信用已在低點、盈餘高點含一次性順風；但股價從 7 月到現在幾乎沒動（206.22→206.66），沒有先反映","watch":"前瞻本益比超過 12 倍而信用指標轉弱","evidence_refs":["capital_markets_pricing#5"],"fact_refs":["f_fwd_pe_latest","f_week26_return_pct"]},{"view":"論點失敗","evidence":"KPMG：10% 利率上限法案未出委員會，若立法將重創發卡經濟、緊縮核貸；10-K：監管可能限制併購與擴張；社會容忍度檢查為紅","assumption":"期中選舉後利率上限或 CCCA 推進","consequence":"卡業務收益率結構性下降，詳見唯一致命點","ruling":"採納為唯一致命點；法案目前未出委員會，機率低但不可忽視","watch":"S.381／H.R.1944 委員會進度","evidence_refs":["supply_demand_durability#1","regulatory_antitrust#1"],"fact_refs":["f_kpi6_net_interest_margin"]},{"view":"論點成功但股東經濟變差","evidence":"Discover 卡片誤分類和解提列 12 億美元且 SEC 調查中；回饋取消與錯誤註記集體訴訟；360 儲蓄 4.25 億美元和解；Brex 收購遭消費者反壟斷訴訟","assumption":"訴訟與罰款逐年吃掉盈餘","consequence":"一次性費用持續拉開 GAAP 與調整後 EPS 的差距（Q3 每股差 1.08 美元）","ruling":"反駁為致命項：已提列與和解金額相對 Q3 單季淨利 35 億美元有限；但 GAAP 與調整後差距要追","watch":"GAAP 與調整後 EPS 差距是否在 2027 年收斂","evidence_refs":["major_events#0","major_events#2","major_events#3","lawsuit_class_action#0","lawsuit_class_action#1","sec_investigation_restatement#0","regulatory_antitrust#3"],"fact_refs":["f_kpi1_gaap_net_income_diluted_","f_kpi2_adjusted_eps_non_gaap"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 206.22 → 本次 206.66（+0.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=206.22","side_b":"本次 price_at_dd=206.66","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 206.22 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 206.22 美元：Bull 價 433、Bear 價 150，五年期望值 +54.0%，基準年化 12.0%，不對稱比 4.1","side_b":"本次情境、股價仍用 206.22 美元：Bull 價 432、Bear 價 150，五年期望值 +39.6%，基準年化 8.7%，不對稱比 2.68","ruling":"先換情境、股價不動：五年期望值少 14.4 個百分點，基準年化少 3.3 個百分點。不對稱比由 4.1 變為 2.68。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 206.22 美元：五年期望值 +39.6%，基準年化 8.7%，不對稱比 2.68","side_b":"本次情境、股價 206.66 美元：五年期望值 +39.3%，基準年化 8.7%，不對稱比 2.65","ruling":"再換股價、情境不動：起點價上漲 0.2%，五年期望值少 0.3 個百分點，基準年化少 0.0 個百分點，不對稱比由 2.68 降到 2.65。合計五年期望值比前份少 14.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"基本面判斷欄重審（結論未變）","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份（2026-07-22）：評等 B、估值偏便宜、陷阱中度、護城河持平、五年後跑道中等、金融類，裁決進場","side_b":"本次以 Q3 新證據重審：綜效年化 18 億美元超前、國內卡沖銷率 3.98% 年降 65bp、前瞻本益比 10 倍、股價幾乎沒動；評等、估值、陷阱、護城河方向、跑道、類別判斷都維持，裁決與部位由程式依同組輸入重算","ruling":"維持：新證據偏正面，但行銷加碼與交換費和解抵銷了一部分，不足以上調任何一欄","evidence_level":"公司新聞稿與 Q3 法說會","settle_metric":"2027 上半年綜效年化與調整後效率比率","if_then":["若 2027 Q2 綜效年化 <20 億美元且調整後效率比率未降，則基本情境 EPS 下修 5% 並停止加碼","反向：若綜效 ≥25 億美元提前達成且 Discover 放款轉正，則護城河方向上調為擴大"],"evidence_refs":[]},{"axis":"情境機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份牛 25、熊 25，最大回撤單點 −52%","side_b":"本次牛 20、基 50、熊 30；最大回撤改為範圍 −35% 至 −55%","ruling":"共識 EPS 年增約 17% 超過內生成長上界約 2.4%（差距靠回購、綜效與信用正常化），依規則熊機率拉到 30%；回撤改寫範圍以反映 CECL 補提路徑","evidence_level":"本次推導","settle_metric":"國內卡逾期率年比","if_then":["若逾期率年比連 2 季轉升，則熊機率再上調到 35% 並減碼一半","反向：若 2027 全年沖銷率 ≤4.5%，則熊機率回到 25%"],"evidence_refs":[]},{"axis":"循環位置","cause":"方法變動","prior_field":["cycle_position"],"side_a":"前份未填循環位置","side_b":"本次判中循環：損失從高點回落、準備金釋出中，但逾期改善已停在季節性","ruling":"補填；依據為 Q2、Q3 法說的逾期與回收描述","evidence_level":"公司法說","settle_metric":"逾期率年比","if_then":["若逾期率年比轉升，則改判晚循環並停止加碼"],"evidence_refs":["financial_capital_credit_cycle#0"]},{"axis":"加碼條件更新","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼：國內卡 NCO 連 2 季 ≤5% 且 Discover 年化 synergy ≥$2.0B（FY26 末）；或回檔 $180-190（P/TBV ~1.7x）分批加","side_b":"加碼：2027 Q2 綜效年化 ≥22 億美元且國內卡逾期率年比未轉升；或回檔至 180 美元以下分批加","ruling":"沖銷率條件已達成（Q2 4.71%、Q3 3.98%），綜效 18 億美元接近舊門檻，改看下一個里程碑；有形淨值事實表未涵蓋，價格門檻改用前瞻本益比約 8.8 倍","evidence_level":"公司新聞稿與法說","settle_metric":"綜效年化金額","if_then":["若 2027 Q2 綜效 ≥22 億美元且逾期未轉升，則加碼至目標部位","反向：若價格先到 180 美元以下但逾期率已轉升，則不加碼"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標（空白）","side_b":"國內卡沖銷率 >5.5% 連 2 季減碼；CET1 <12% 減碼；利率上限法案任一院通過清倉","ruling":"補上可監測的門檻，對應三大風險","evidence_level":"本次推導","settle_metric":"各指標季度讀數","if_then":["若任一減碼門檻觸發，則減碼一半","若利率上限法案任一院通過，則清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點空白（未設）","side_b":"聯邦信用卡利率 10% 上限立法通過","ruling":"前份把利率上限列在監管風險之一；本次判它是數學上最大的單一敏感度項，獨立成唯一致命點","evidence_level":"KPMG 簡報與 10-K","settle_metric":"法案進度","if_then":["若法案出委員會，則減碼一半","若任一院通過，則清倉"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"盈餘能力說法與投資加碼","cause":"新證據","prior_field":null,"side_a":"CEO（2026-10-20）：併購後盈餘能力現在就看得到，與交易時預期一致；剩餘綜效與交換費和解大致抵銷","side_b":"同場 CEO：2027 年更用力投行銷、網路與 AI，不給效率比率指引；7 月法說也迴避 20% 報酬與效率比率的追問","ruling":"可調和、程度差異：盈餘能力指的是扣投資前的底盤，投資加碼會吃掉一部分；採保守側，基本情境 FY2027 EPS 23.6 低於共識","evidence_level":"Q2、Q3 法說原話","settle_metric":"2027 全年調整後效率比率","if_then":["若 2027 調整後效率比率高於 2026，則下修基本情境 EPS 5% 並停止加碼","反向：若效率比率下降且行銷年增低於營收年增，則上調基本情境至共識"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"Discover 放款谷底改口","cause":"新證據","prior_field":null,"side_a":"CEO（2026-07-21）：Discover 放款收縮谷底約在今年第四季","side_b":"CEO（2026-10-20）：預期未來數季繼續收縮，之後才轉正；Q3 Discover 卡放款年減 2.9%（Q2 為 1.5%）","ruling":"時程延後屬實，但新發卡已 100% 上公司系統、新發卡年增為併購後首次，判延後而非失敗","evidence_level":"Q2、Q3 法說原話","settle_metric":"Discover 卡放款年比","if_then":["若 2027 Q2 Discover 放款年減仍 ≥2%，則停止加碼並下修網路假設","反向：若 2027 Q2 年減收斂到 1% 以內，則維持"],"evidence_refs":["regulatory_antitrust#3","capital_markets_pricing#5"]},{"axis":"合併沖銷率上升對卡沖銷率下降","cause":"新證據","prior_field":null,"side_a":"Q2 合併淨沖銷率 1.48%，年增 18bp","side_b":"Q3 國內卡沖銷率 3.98%，年降 65bp；逾期率年減 15bp","ruling":"可調和：合併數字受 Discover 併入組合變動與車貸次級占比回升影響；卡業務改善屬實，但逾期已只跟季節性","evidence_level":"10-Q 搜尋摘要與 Q3 法說","settle_metric":"國內卡逾期率年比","if_then":["若國內卡逾期率年比轉升連 2 季，則減碼一半"],"evidence_refs":["financial_capital_credit_cycle#0"]}],"triggers":[{"n":1,"text":"綜效進度驗證","type":"假設驗證","maps_to":"H1","metric":"合併綜效年化金額","threshold":"2027 Q2 財報 ≥22 億美元","action":"達標續抱；<20 億美元停止加碼並下修基本情境 EPS 5%","source_freq":"季度法說會","date":"2027-07","evidence_refs":[]},{"n":2,"text":"國內卡信用轉向","type":"風險","maps_to":"R1","metric":"國內卡季度淨沖銷率與逾期率年比","threshold":"沖銷率 >5.5% 或逾期率年比 ≥+30bp，連 2 季","action":"減碼一半","source_freq":"季度新聞稿、月度信用資料","date":null,"evidence_refs":["financial_capital_credit_cycle#0"]},{"n":3,"text":"聯邦 10% 信用卡利率上限","type":"Single Thing","maps_to":"R2","metric":"S.381／H.R.1944 立法進度","threshold":"出委員會減碼一半；任一院通過清倉","action":"清倉","source_freq":"國會紀錄（事件）","date":null,"evidence_refs":["supply_demand_durability#1","regulatory_antitrust#1"]},{"n":4,"text":"Visa／Mastercard 交換費和解終審","type":"風險","maps_to":"R2","metric":"終審結果與交換費收入變化","threshold":"11 月聽證核准後，2027 Q1 交換費損失大於剩餘綜效","action":"下修基本情境 EPS 並停止加碼","source_freq":"法院公告、季度財報","date":"2026-11","evidence_refs":["regulatory_antitrust#2"]},{"n":5,"text":"回檔分批加","type":"加碼","maps_to":"H1","metric":"股價與國內卡逾期率年比","threshold":"股價 ≤180 美元（前瞻本益比約 8.8 倍）且逾期率年比未轉升","action":"分批加碼至目標部位","source_freq":"每日價格、月度信用資料","date":null,"evidence_refs":[]},{"n":6,"text":"資本緩衝下降","type":"減碼","maps_to":"R1","metric":"CET1","threshold":"<12.0% 或回購暫停","action":"減碼三分之一","source_freq":"季報","date":null,"evidence_refs":[]},{"n":7,"text":"Discover 放款轉正","type":"假設驗證","maps_to":"H3","metric":"Discover 卡放款年比","threshold":"2027 Q2 年減仍 ≥2%","action":"停止加碼","source_freq":"季度法說會","date":"2027-07","evidence_refs":["regulatory_antitrust#3"]},{"n":8,"text":"訴訟與調查","type":"風險","maps_to":"R5","metric":"單案罰款或和解金額","threshold":">10 億美元，或 SEC 調查轉正式執法","action":"減碼三分之一","source_freq":"8-K、10-Q 附註","date":null,"evidence_refs":["sec_investigation_restatement#0","major_events#0"]},{"n":9,"text":"Q4 財報複審","type":"複審日期","maps_to":null,"metric":"Q4 2026 財報","threshold":null,"action":"重跑判斷","source_freq":"季度","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"國內卡季度淨沖銷率","bear_threshold":">5.5%，連 2 季","window":"2026Q4–2027Q4","source":"公司季度新聞稿","last_status":"ok"},{"metric":"國內卡逾期率年比變動","bear_threshold":"≥+30bp，連 2 季","window":"2026Q4–2027Q4","source":"公司月度信用資料與季報","last_status":"ok"},{"metric":"CET1 比率","bear_threshold":"<12.0%","window":"每季","source":"公司季報","last_status":"ok"},{"metric":"合併綜效年化金額","bear_threshold":"2027 Q2 <20 億美元","window":"至 2027-07","source":"公司法說會","last_status":"ok"},{"metric":"聯邦 10% 信用卡利率上限法案","bear_threshold":"任一院通過","window":"持續","source":"國會紀錄","last_status":"ok"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場仍用併購年的低盈餘與利率上限、交換費和解等監管尾部折價，前瞻本益比約 10 倍只隱含盈餘持平；但前三季已看得到併購後盈餘能力，綜效進度超前、卡信用優於去年同期"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=4.44, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"加碼：2027 Q2 綜效年化 ≥22 億美元且國內卡逾期率年比未轉升；或回檔至 180 美元以下分批加","exec_line":"現價 206.66 美元一帶依裁決建首倉，不追 230 美元以上（前瞻本益比 11 倍以上）；180 美元以下且信用未轉向時分批加"},"reasoning":{"industry":"Q3 總營收 163 億美元，淨利差 8.41%（季增 40bp，來自國內卡收益率、現金下降與多一天），撥備前盈餘 75 億美元；提列 29 億美元，含淨沖銷 31 億、準備金釋出 2.25 億。期末放款 4,625 億美元，存款 4,807 億美元，存款大於放款，資金不靠批發市場。分部：國內卡 Q3 營收年增 5%、收入率 17.8%、沖銷率 3.98%；消費金融營收年增約 17%（Discover 營收綜效與車貸）；商業銀行營收季增 6%。分部營收占比事實表未涵蓋。產業時鐘判在擴張期：信用損失從 2024 年高點回落、準備金釋出中，但逾期改善自 6 月起只跟季節性，擴張後段。供需持久性：週期性將反轉，卡信用損失有循環，不是結構性改善。產業態勢雙向拉鋸：競爭面惡化（大型同業資金成本更低、高端卡行銷加碼，10-K 稱支付業競爭加劇）；結構面轉好（借記卡轉 Discover 網路完成，網路交易量年增 25%）；監管面變動（10% 利率上限提案、Visa／Mastercard 交換費和解 11 月終審）。單點依賴：核心系統大多在 AWS，列入風險。","moat":"機制：規模化資料核貸加上自有網路與全國數位銀行的低成本存款。銀行不看 ROIC，改看報酬與效率：Q3 調整後效率比率 48.76%、GAAP 54.19%，都低於 60%；CET1 13.8%。同業 ROTCE 事實表未涵蓋，無法做報酬差距對照，評分用綜合分加敘述：執行 8、定價 7。當期報酬屬高利益率低周轉；四檢查點中社會容忍度為紅。增量報酬約 20% 是法說會分析師推估的量級，管理層未確認；再投資率約 12%（Q3 回購 26 億美元加股息約 5 億美元，占淨利 35 億美元約 88%），內生成長上界約 2.4%。高報酬、低再投資空間，多餘資本以回購配回，符合紀律。","growth":"共識 EPS：FY2026 20.56、FY2027 24.07、FY2028 28.08 美元，兩年年增約 17%；同期共識營收 FY2026 640.6 億、FY2027 675.5 億美元，只增約 5%。FY2025 GAAP EPS 4.03 含併購一次性費用與準備金首提，不能當成長基期，三年 CAGR 改看 FY2026→FY2028。缺口（約 17% 對內生上界約 2.4%）可以歸因：淨回購每年約 6–8%（Q3 回購 26 億美元，約市值 2% 一季），其餘來自綜效與信用正常化帶動的利潤率，不依賴估值重估。管理層 Q3 說剩餘綜效與交換費和解損失大致抵銷，2027 年行銷再加碼，所以共識 FY2027 之後的斜率偏樂觀。滲透率與份額事實表未涵蓋，跑道年數無法量化；五年後成長沒有明確第二曲線（網路轉信用卡仍在測試），判中等。","governance":"Q3 回購 26 億美元加股息，約占淨利 35 億美元的 88%，CET1 仍維持 13.8%。CFO 在 Q2 法說稱 11% 是長期資本需求而非目標，不急著壓低。Fed 2026 壓力測試嚴重不利情境下 CET1 最低 11.0%，壓力資本緩衝 4.5% 維持到 2027-09-30（此緩衝在併入 Discover 前計算，2027 年可能重算）。回購收益率以前瞻本益比 10.05 倍換算約 10%；10 年期公債殖利率事實表未涵蓋，除非高於 8%，否則回購買入收益率過門檻。Discover 綜效年化 18 億美元、進度超前，但併購投入資本與增量報酬事實表未涵蓋，暫不判過。SBC 事實表未涵蓋；股數在大額回購下下降，另有 Brex 發行約 1,060 萬股。ROTCE 事實表未涵蓋。","valuation":"現價 206.66 美元，FY2026 共識 EPS 20.56 對應 10.05 倍，FY2027 共識 24.07 對應 8.6 倍。今年準備金釋出（Q2 約 6.6 億、Q3 2.25 億美元，以 22% 稅率估稅後約每股 1.1 美元）扣掉後約 10.6 倍，結論不變。FY1 共識近 3 個月上修 4.31%。賣方目標價均值依聚合站不同落在 236–259 美元。銀行的主錨有形淨值倍數與 ROTCE 事實表未涵蓋，這是估值判斷最大的缺口。trailing 本益比只有四個年度端點、且 FY2025 分母被併購一次性費用壓低，不當五年分位使用。","premortem":"三條主要看錯路徑：一是信用轉向，CECL 下準備金一次補提，跌幅比 2008 年陡（CEO 自述當年大量放款在表外、且無 CECL）；二是綜效全到位但被行銷競爭與交換費下調吃掉；三是 10% 利率上限立法。股價 26 週僅漲 4.44%，RSI 58.6，週線均線排列達標但 250 週均線 13 週斜率只有 0.7%，價格沒有先反映好消息。Q3 提列 29 億美元仍含 2.25 億釋出，扣掉後盈餘品質略低於帳面。"},"plain":{"six":{"how_it_makes_money":"賺持卡人的循環利息與交換費：錢卡在核貸定價模型與低成本零售存款；收購 Discover 後，網路端分潤也收回自家","moat":"護城河持平：Discover 網路與資料核貸是真優勢，綜效進度超前；但交換費與利率監管、高端卡行銷競爭把定價權壓住","growth":"跑道中等：美國信用卡已成熟，五年後成長靠網路量、高端客群、全國數位銀行的份額，以及回購","capital":"資本配置良好：在約 10 倍本益比下大額回購，資本比率仍留緩衝；Discover 併購報酬要到 2027 完整年度才驗得到","valuation":"現價只要求盈餘持平：前瞻本益比約 10 倍、FY2027 共識下約 8.6 倍；我相信盈餘至少持平，所以偏便宜","how_wrong":"最可能看錯在信用循環：盈餘高點含準備金釋出與回收順風，而逾期改善已經停在季節性水準"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場仍用併購年的低盈餘與利率上限、交換費和解等監管尾部折價，前瞻本益比約 10 倍只隱含盈餘持平；但前三季已看得到併購後盈餘能力，綜效進度超前、卡信用優於去年同期","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟢","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"金融","price_at_dd":206.66,"week26_return_pct":4.44,"consensus_rev_3m_pct":4.31,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"trailing 分母含 FY2025 併購一次性費用（GAAP EPS 4.03），改用前瞻錨；前瞻分母含今年準備金釋出，已扣除測試，結論不變"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"Visa／Mastercard 修正和解終審聽證","impact":"中","watch":"是否核准、交換費下調幅度"},{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉（利率上限、CCCA 政治動向）","impact":"中","watch":"國會組成與委員會議程"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與綜效進度","impact":"中","watch":"綜效年化、行銷費用、Discover 放款"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"Discover 舊帳戶轉換完成","impact":"中","watch":"客戶流失、Discover 放款轉向"},{"date":"2027-06","date_precision":"month","type":"regulatory","event":"Fed 年度壓力測試結果","impact":"中","watch":"併入 Discover 後壓力資本緩衝是否重算上調"}],"_projected_from":"v19"}
```
