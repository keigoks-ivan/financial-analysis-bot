你是 stock-analyst v20 的**散文層（prose）agent**，標的 DXCM（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：DXCM　日期：2026-11-02　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1574B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（1071B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（993B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1522B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1604B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（590B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1131B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2651B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4570B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3059B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1574           3798-5426      5 條（2–6 內）  
s3                  8000        1071           4850-6929      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4119          7617-10881      5 條（2–6 內）  
s6                 11000         590          7287-10410      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1131           1658-2369      3 條（2–6 內）  
s10                 5000        2651           1644-2349      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3059           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=6041B；至少需散文≈38.96KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−50
−42%
−35
−35%
−29%
−11%
−4.4%
−0.75%
0
0.3
0.5
0.5%
0.75
0.9
1%
1
01
1.29
1.4%
1.47
1.5%
1.6
1.7
1.85
02
2%
2.0
2
2.06
2.09
2.142
2.5
2.5%
2.7%
2.71
2.75
2.8
2.9
03
3.00
3%
3
3.10
3.1
3.13
3.25
3.272
3.3%
3.395
3.5%
3.55
3.67
3.75
3.85
4%
4
4.05
4.25
4.55
5%
05
5
5.05
5.18
5.20
5.25
5.35
5.98
6%
6
06
6.2
7
7%
07
7.5%
8%
8
8.36
8.7%
9
9%
9.062
9.12
9.5%
9.70
10
10%
10.1%
10.10%
10.77
11
11%
11.02
11.204
11.4
12
12%
13
13%
13.445
14
14%
15%
15
15.7%
15.9%
16
16.3%
16.4%
17
19.0%
19.6%
20
20%
20.6%
22
22.4
23.5
24
24.0%
24%
24.3%
24.5
25%
25
25.3%
26%
26
26.3
27
27%
28%
28
29
30
30%
30.37
30.4
31
33.89%
33.9%
34%
34.1%
34.13
35
35%
40
40%
42
44.7%
45
46%
48
48.5%
49
50%
52.0
52.5
52.8%
52.83%
53
55%
57.5
60%
60
61.3%
62%
63.4%
64%
65
65%
65.1%
66%
70
71
71.1%
72%
75
75%
80%
82.29
84%
86.16
87
90
92.85
94
100%
100
111
112
150
150%
250
306.9
380
900
2022
2025
2026
2027
2028
2030
2031
20261102
1,230
2,300
2,500
3,680
5,200
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
{"meta":{"ticker":"DXCM","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"DexCom, Inc."},"oneliner":"CGM兩大廠之一，毛利率回到65%、美國連季拿份額，下一段成長在第二型非胰島素族群；約30倍今年EPS屬合理不便宜，CMS涵蓋決定年底前揭曉，等結果再動","thesis":{"H":[{"id":"H1","text":"涵蓋擴張（第二型非胰島素、國際新給付、直營化）讓營收維持每年10%以上","2y":"FY2027營收年增≥10%（約57.5億美元以上），CMS涵蓋於2027年中生效","5y":null,"10y":null,"threshold":"FY2027全年營收年增≥10%；美國營收季度年增≥10%","source":"公司季報新聞稿與2027年2月全年財測","drift_rule":"TTM營收年增率連2季低於9.5%＝削弱；連3季低於9%＝反轉"},{"id":"H2","text":"15日感測器普及、Ireland投產成本攤平與G8製造成本較G7低至少10%，推動營業利益率擴張","2y":null,"5y":"FY2030非GAAP營業利益率≥27%（公司目標29–30%）、毛利率回到65%以上","10y":null,"threshold":"FY2027非GAAP營業利益率≥25%、FY2028≥26%；2027年下半年非GAAP毛利率≥64%","source":"公司季報新聞稿；投資人日（2026-05-14，CFO Jereme Sylvain）利益率目標","drift_rule":"TTM非GAAP營業利益率連4季低於當年門檻5%以上＝削弱；連6季低於10%以上＝反轉"},{"id":"H3","text":"CGM成為各型糖尿病標準照護，DXCM維持兩大廠地位","2y":null,"5y":null,"10y":"全球CGM營收份額≥30%（2025年33.89%），G8與多分析物平台如期接棒","threshold":"第三方年度CGM營收份額≥30%；美國營收年增不落後Abbott糖尿病照護同期成長","source":"Mordor與GlobalData年度份額估計；DXCM與Abbott季報","drift_rule":"份額跨2個年度低於30%＝削弱；跨3個年度＝反轉"}],"R":[{"id":"R1","text":"CMS第二型非胰島素涵蓋否決、延後或附A1c門檻，投資人日逐年10%以上營收計畫失去最大增量","h_ref":"H1","clock":"⚡","threshold":"2027-03-31前未公布決定，或決定附A1c門檻等限制","evidence_refs":["end_markets#3","supply_demand_durability#1"]},{"id":"R2","text":"價格壓縮：2028年Medicare競標、PBM排他處方集、OTC與對手在自費市場降價，加上藥局通路轉換壓低每用戶營收","h_ref":"H2","clock":"🔥","threshold":"非GAAP毛利率2027年Q3未回到64%或之後連2季低於62%；競標得標價降幅超過15%","evidence_refs":["competitive_share_entrants#2","end_markets#2","channel_business_model_shift#1"]},{"id":"R3","text":"品質與法律：2025-03 FDA警告信、六件G6/G7使用者集體訴訟、證券集體訴訟與衍生訴訟，品質問題復發會同時傷毛利率與份額","h_ref":"H2","clock":"🔥","threshold":"新警告信或一級召回；使用者訴訟取得集體認證；訴訟金額與受影響營收事實表未涵蓋","evidence_refs":["regulatory_antitrust#2","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","lawsuit_class_action#2"]},{"id":"R4","text":"供應鏈：ASIC與聚合物單一來源、製造集中Mesa與馬來西亞（二手摘要），替代產能難快速建立；Ireland投產與晶片第二來源申請為緩解","h_ref":"H1","clock":"⚡","threshold":"任何出貨中斷或延遲公告","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","customer_second_source#0"]},{"id":"R5","text":"經銷商集中：前三大經銷商未扣回饋前營收占比55%／35%／46%且三年逐年上升，議價力往下游移","h_ref":"H2","clock":"🐢","threshold":"最大經銷商營收占比>60%或應收占比>30%（FY2025為55%與24%）","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"id":"R6","text":"競爭：Abbott規模與雙分析物先行、中國新興廠與醫材以外業者進場、對手用AI加速創新","h_ref":"H3","clock":"🔥","threshold":"美國營收年增連2季落後Abbott糖尿病照護同期，或第三方美國份額跌破40%（2025年44.7%）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","end_markets#1","substitute_technology#0","substitute_technology#3"]}],"single_thing":{"description":"CMS對第二型非胰島素患者的CGM涵蓋決定（公司預期2026年底前公布、2027年中生效），結果為否決、延後或附A1c門檻等限制","why_fatal":"第二型非胰島素是唯一的大型增量族群（美國約2,500萬人、商保涵蓋僅約25%），投資人日逐年10%以上的營收計畫把涵蓋時點放在2027年中；否決會讓成長退回現有涵蓋下的低雙位數並逐年下滑，正是Base與Bear的分水嶺","if_happens":"不建倉；若已持有減碼一半，等2027年財測確認營收年增是否仍≥10%；成長跌破10%且毛利率下滑則清倉","how_monitor":"CMS與Medicare承包商醫療主任公告、公司8-K與法說；ADA照護標準更新是否納入CONNECT","probability":"12–24個月內不利結果約20–25%（CONNECT登上NEJM屬A級證據、CEO稱時程未變並否認A1c門檻傳聞；但決定權在CMS，公司說法屬一方之詞）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":26.3,"peg_fy2":1.6,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":2.09,"FY2026E":2.71,"FY2027E":3.13,"FY2028E":3.67},"fy_end_month":12,"eps_basis":"FY2025A取年度財報GAAP攤薄EPS 2.09（事實表無調整後EPS；Q3 2026 GAAP與調整後營業利益僅差約1,230萬美元，口徑近似）；FY2026E–FY2028E為Koyfin共識（調整後口徑），財年12月底"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"耗材型經常性營收、毛利率六成以上、營業利益率擴張中、FCF高於淨利；2025年FDA警告信與品質問題後的修復期，股價仍在五年均價之下"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：美國第一型滲透約60–65%已成熟，第二型非胰島素約2,500萬人、商保涵蓋僅約25%、Medicare待決，需求由臨床證據與涵蓋擴張驅動，非景氣循環；壓力在單價不在需求（Baird與MarketBeat彙整、CEO投資人日2026-05-14）","bargaining":{"up":"ASIC與生物介面膜聚合物單一來源（10-K），晶片已向FDA申請Silicon Labs第二來源；供應端議價風險中等","down":"前三大經銷商營收占比55%／35%／46%且逐年上升、應收占比24%／20%／24%；PBM可改排他處方集（CVS案），Medicare 2028年起競標；下游議價力強","geo":"製造在美國Mesa與馬來西亞，Ireland廠2026年Q4起商業生產，三地分散；CFO稱多數產品美國製造、關稅直接衝擊小（2025年Q1法說）"},"profit_pool_dir":"利潤池隨涵蓋擴張變大，但單位價格往下：量往第二型與國際走，OTC與競標壓價；DXCM目前靠成本下降守住毛利率","tam_table":[{"item":"美國第一型CGM滲透率","value":"約60–65%，已成熟（Baird與MarketBeat彙整，2025–2026）"},{"item":"美國第二型非胰島素患者","value":"約2,500萬人，商保涵蓋約25%（CEO，投資人日2026-05-14）；四大商業PBM已涵蓋，Medicare待決"},{"item":"全球涵蓋人數","value":"約2,300萬人→2030年底約5,200萬人（CFO，投資人日）"},{"item":"第二型滲透率假設","value":"2030年10–15%，CMS涵蓋後以basal一半速度滲透（CFO，投資人日）"},{"item":"美國有涵蓋但未用CGM","value":"約900萬人（CEO，Q2法說2026-07-30）"},{"item":"第二型basal市場規模","value":"2030年約40億美元（William Blair 2025-10，採用曲線75%情境）"},{"item":"CGM營收份額2025","value":"全球Abbott 52.83%、DXCM 33.89%、Medtronic 10.10%（Mordor）；美國Abbott 48.5%、DXCM 44.7%（GlobalData）"},{"item":"營業利益池占比5年前→現在","value":"事實表未涵蓋"}]},"moat":{"mechanism":"感測器準確度＋幫浦相容生態（AID整合、Share/Follow）造成第一型與胰島素使用者轉換成本，加上隨機試驗證據推動給付擴張與醫師處方偏好","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：毛利率年增約380bp至65.1%、美國多季拿份額（CEO Q3法說）、Q1營收年增15%對Abbott CGM 7.5%；定價面縮減：CVS排他合約流失（占美國營收不到4%）、對手提到自費市場定價逆風、研究機構預測OTC感測器兩年內跌破60美元。全球營收份額仍落後Abbott（2025年33.9%對52.8%），但未見DXCM份額下滑的第三方時間序列，故判持平而非上升","peer_na_reason":"同業ROIC與投入資本事實表未涵蓋；Abbott與Medtronic的利潤率為集團整體、非CGM單一業務，PODD與TNDM是胰島素幫浦廠，只能當利潤結構參考","threats":[{"level":"🟡","text":"Abbott份額與規模領先（2025年全球營收份額52.8%對33.9%），雙分析物（葡萄糖＋酮體）Libre Duo先上市；DXCM酮體要等G8之後的多分析物版本，CEO不給時程","p":"40%","evidence_refs":["substitute_technology#3","competitive_share_entrants#0","end_markets#1"]},{"level":"🟡","text":"中國新興廠與醫材以外的大型企業切入一般健康市場，FDA 2026-01-06一般健康器材指引可能降低門檻，加上OTC感測器價格預測兩年內跌破60美元，壓低自費與第二型族群單價；若大型科技業以穿戴生態系切入則升級為生態攻擊","p":"30%","evidence_refs":["competitive_share_entrants#1","end_markets#2","substitute_technology#0"]},{"level":"🟡","text":"PBM處方集改為單一品牌優先（CVS合約流失，CFO於Q3法說2026-10-29稱占美國營收不到4%），若擴散到其他PBM將迫使降價換取共同優先地位；CEO稱2027年處方集已鎖定。來源只有公司法說，屬一方口徑，外部負向資料沒有收錄此事，尚無第三方佐證","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率（營業利益率24.0%、FCF利潤率33.9%、毛利率63.4%）×周轉率未知（投入資本事實表未涵蓋），先查持續期","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者與決策者兩環已成立：CONNECT隨機試驗6個月A1c較對照組多降0.9個百分點、登上NEJM，真實世界非胰島素第二型配戴率逾80%（CEO Q2法說）。付款者是缺口：非胰島素第二型僅約25%有涵蓋、Medicare決定待定，付款環節不成立前需求轉不成收入"},{"item":"決策層級","level":"🟡","text":"在最小決策單位看替代性分兩群：第一型與幫浦使用者綁自動給藥系統相容與Share/Follow，轉換成本高；第二型非胰島素與OTC族群產品較可比，PBM處方集一紙決定即可換品牌（CVS案）。漲價後流失率與分客群續約率事實表未涵蓋，CFO稱留存與使用率在擴大族群時保持穩定"},{"item":"價值鏈分配","level":"🟡","text":"付款方（Medicare、PBM）與經銷商議價力強：前三大經銷商營收占比55%／35%／46%且逐年上升，Q2經銷通路營收約11.02億美元對直銷約2.06億美元；CMS 2028年起以第75百分位得標價付款。DXCM毛利率仍守在65.1%，代表感測器目前仍是最難取代的環節，但分配正往付款方移動"},{"item":"社會容忍度","level":"🟡","text":"CGM屬必要醫療耗材、價格彈性低，但政策已顯示價格天花板：CMS把CGM納入競標並預期降低Medicare給付，公司長期計畫只假設名目價格影響。Medicare占營收比重事實表未涵蓋，無法量化；此項已列入反證紀錄"}],"roiic":"事實表未涵蓋投入資本與增量資本，無法計算；FY2023→FY2025 GAAP營業利益由約5.98億增至約9.12億美元，增量資本未知","reinvest_rate":"約−29%（FY2025代理算法：再投資率≈（淨利−FCF）÷淨利＝（8.36−10.77）÷8.36；事實表沒有稅後營業利益，以淨利代替）。FCF含SBC加回，若以2026年Q3年化約1.47億美元把SBC當現金成本扣回，約−11%，符號不變。可能看錯的地方：只有一個年度，單年營運資金回收會讓數字偏負。前三季資本支出2.142億美元約占FCF的24%，Ireland擴產已完成","endo_ceiling":null,"formula_note":"內生成長率＝增量ROIC×再投資率。增量ROIC缺投入資本算不出，天花板不給精確數字；但再投資率為負（約−29%，扣回SBC後約−11%），只要增量ROIC為正，天花板就在零以下，不需要增量ROIC的數字也能判定共識EPS成長超出天花板。超出部分來自既有產能與剛投產的Ireland承接涵蓋擴張的量、利益率擴張與回購，不靠新增投入資本"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","DXCM":63.42,"ABT":56.63,"PODD":71.08,"MDT":65.01,"TNDM":56.01,"unit":"%"},{"metric":"營業利益率","DXCM":23.98,"ABT":15.9,"PODD":16.9,"MDT":19.04,"TNDM":-4.4,"unit":"%"},{"metric":"FCF 利潤率","DXCM":33.93,"ABT":15.66,"PODD":8.7,"MDT":16.33,"TNDM":-5.93,"unit":"%"},{"metric":"研發密度","DXCM":11.91,"ABT":6.64,"PODD":11.33,"MDT":7.77,"TNDM":18.03,"unit":"%"}],"competitors":[{"name":"ABT","gm":56.63,"om":15.9,"fcf_margin":15.66,"rd_intensity":6.64,"strategy_note":"CGM份額第一（2025年全球營收份額52.8%），以規模與低價搶自費及新市場，雙分析物Libre Duo先上市；集團營業利益率15.9%不代表其CGM單一業務","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PODD","gm":71.08,"om":16.9,"fcf_margin":8.7,"rd_intensity":11.33,"strategy_note":"貼片式胰島素幫浦廠，非CGM直接對手；毛利率71.1%但FCF利潤率8.7%，其CGM相容選擇影響DXCM在幫浦用戶的黏著度","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MDT","gm":65.01,"om":19.04,"fcf_margin":16.33,"rd_intensity":7.77,"strategy_note":"MiniMed以自家幫浦綁Simplera與Guardian Connect，份額約10.1%，屬生態內封閉競爭，威脅限於自家幫浦用戶","period":"TTM ending 2026-07-31（4季加總）"},{"name":"TNDM","gm":56.01,"om":-4.4,"fcf_margin":-5.93,"rd_intensity":18.03,"strategy_note":"胰島素幫浦廠，營業利益率−4.4%仍虧損，議價力弱，屬相容夥伴而非競爭者","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主：活躍用戶年增十幾%上段、新病患創紀錄（CEO Q3法說）；價為負貢獻：營收年增11%低於用戶增速，每用戶營收下滑；併購僅小型（Nutrisense、歐洲經銷商直營化）；回購補EPS：2026年已買回10億美元，2027年承諾至少50% FCF回購","runway_years":"約8–10年（推估）","runway_post_y5":"🟢","endo_ceiling_basis":"天花板算不出精確數字（增量ROIC缺投入資本），但符號可定：FY2025淨利8.36億美元、FCF 10.77億美元，再投資率約−29%，扣回SBC後約−11%，只要增量ROIC為正，天花板在零以下。交叉核對：共識EPS三年年增約20.6%（FY2025A GAAP 2.09→FY2028E 3.67，Q3 GAAP與調整後營業利益只差約1,230萬美元，口徑近似）、FY2026E→FY2028E約16.4%，全數超出天花板；拆成營收約11%（既有產能與剛投產的Ireland承接涵蓋擴張的量）、利益率擴張（投資人日每年約+150bp，以24%為基期約每年貢獻6%，2030年目標29–30%）與淨回購年約2–3%，三項相乘約每年20%上下，共識16–20%沒有超過，可歸因","segments":[{"item":"美國","value":"Q3 2026營收9.70億美元，年增14%，約占72%；連續多季拿份額，最大增量來自第二型（含非胰島素）"},{"item":"國際","value":"Q3 2026營收3.75億美元，年增5%，約占28%；去年下半年多項給付利多造成高基期，管理層預期2027年初回到較高有機成長；歐洲最大剩餘經銷市場收購直營待2027年完成"},{"item":"通路","value":"Q2 2026經銷通路營收約11.02億美元、直銷約2.06億美元，經銷約占84%"}],"decay_signals":["毛利率連2季年減：未亮（Q3年增約380bp）","核心市占近12個月縮減：未亮（美國連季拿份額，管理層口徑；第三方時間序列未涵蓋）","提價後銷量下滑：未亮","EPS成長顯著高於營收成長：亮（共識FY2026E→FY2028E EPS年增約16.4%對營收約11%）","FCF對淨利低於0.75連2年：未亮（FY2025為1.29倍）","SBC占營收逾5%且上升：未亮（2.7%）","TAM萎縮或被替代：未亮（非侵入式替代技術查無報導）","估值倍數近3年系統性下移：亮（以公司自身為代理，本益比、P/S、EV/S都在近4個年度端點最低處；同業倍數未涵蓋）","維持性資本支出占FCF逾60%：未亮（前三季總資本支出約占FCF 24%）","停止投資新產能且營收下滑：未亮（Ireland剛投產）"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：近年只有小型收購（Nutrisense營收極小、歐洲經銷商直營化未完成），資本回饋以回購為主，現金去向已在理由交代；近三年現金去向四分與回購均價事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無重大併購：Nutrisense價格未揭露、非CGM營收年僅數百萬美元以下，歐洲經銷商收購簽約未完成（2027年完成），無已實現報酬可評","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價事實表未涵蓋；以現價換算前瞻盈餘殖利率約3.3%（30.4倍）、FY2025 FCF殖利率約3.5%（10.77億÷市值306.9億美元）；10年期公債殖利率事實表未涵蓋，但須低於約1.5%才過，判定不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC年化約1.47億美元（Q3 3,680萬×4），約占市值0.5%，且回購使股數淨減，淨稀釋率遠低於1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2026E共識EPS 2.71美元）為主，PEG輔助","tier":"大型醫療器材成長股","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率與研發密度，無同業前瞻本益比，無法做同級倍數錨定；改用自身倍數與FY2028E共識倍數交叉檢查"},"fwd_pe":30.37,"peg":1.47,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比30.4倍、FY2027E 26.3倍、FY2028E 22.4倍；PEG約1.47（三年EPS年增約20.6%，FY2025基期偏低；只看FY2026E→FY2028E的16.4%則約1.85），落在1–2合理區；五年分位事實表未涵蓋，只有近4個年度端點分位：本益比0.5、P/S 2.0、EV/S 0.3，皆在區間最低處；賣方均價86.16美元僅高於現價約5%；Base五年終端約111美元，含回購年報酬約9%，屬中等，合理不便宜","upside_short_pct":6,"upside_mid_pct":35},"trap_analysis":{"verdict":"🟡","label":"中度：EPS成長快於營收、靠利益率與回購撐，自身倍數已系統性下移"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"CMS將CGM納入DMEPOS競標，2028-01-01起以第75百分位得標價付款、預期約10份合約並降低Medicare給付；研究機構預測OTC感測器兩年內跌破60美元；對手在其法說提到自費市場定價逆風（Q3法說分析師轉述）；中國新興廠與醫材以外的大型企業進場；美國份額Abbott 48.5%仍高於DXCM 44.7%","assumption":"公司長期計畫只假設名目價格影響、營業利益率每年約擴張150bp","consequence":"每用戶營收年降中個位數且DXCM被迫跟價，營業利益率退回約19.6%（2025年水準），EPS五年停在約3美元、倍數壓到16倍，股價約48美元，較現價約−42%","ruling":"部分採納：定為Bear情境、機率30%；不採為Base，因為Q3毛利率65.1%是2022年Q4以來最高、CFO稱全球未見定價惡化，2027年處方集已鎖定。與唯一致命點部分重疊（CMS否決會加速這條路），已回補進Bear機率","watch":"非GAAP毛利率（排除Ireland投產）是否連2季低於62%；2027年競標得標價與合約數","evidence_refs":["competitive_share_entrants#2","end_markets#2","competitive_share_entrants#0","competitive_share_entrants#1","end_markets#1","substitute_technology#3"]},{"view":"論點失敗","evidence":"2025-03 FDA警告信（聖地牙哥與Mesa廠製造與品質系統不符、G6/G7感測器未經核准變更）；六件G6/G7使用者集體訴訟、證券集體訴訟（2026-02-06提第二次修正訴狀）與衍生訴訟；ASIC與生物介面膜聚合物單一來源；製造集中Mesa與馬來西亞（二手摘要）","assumption":"品質問題已解決（投資人日CEO承認黏著問題尚未完全解決，Q3稱新黏膠使15日存活率提高4–5個百分點）","consequence":"品質問題復發或訴訟取得集體認證並不利和解，毛利率與份額同時受傷，警告信未結案時新品審查也可能受拖累","ruling":"反駁為主論點：Q3毛利率改善部分來自報廢與品質管理，存貨水準已穩定；Ireland投產讓製造擴到美、歐、亞三地，晶片已向FDA申請第二來源。但訴訟金額、受影響營收與警告信是否結案事實表未涵蓋，標為資料缺口","watch":"FDA警告信結案公告；使用者訴訟集體認證裁定；任何召回或出貨中斷","evidence_refs":["regulatory_antitrust#2","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","lawsuit_class_action#2","geo_supply_chain#0","geo_supply_chain#1","customer_second_source#0"]},{"view":"論點成功但股東經濟變差","evidence":"CEO稱活躍用戶年增十幾%上段，但Q3營收只年增11%，每用戶營收在降（15日款一年用量較少、國際分級定價、藥局通路轉換曾使Q1營收季減6–7%）；前三大經銷商營收占比55%／35%／46%逐年升；Dexcom Direct與歐洲經銷商直營化都要花錢","assumption":"CMS涵蓋帶來的量讓營收維持10%以上，並帶出營業利益率擴張","consequence":"量起來但落在給付較低的政府與自費通路，營收成長追不上用戶成長，利益率卡在24–25%，EPS只跟營收同速，Base的13%EPS年增變成10%左右","ruling":"部分採納：Base已把營業利益率路徑壓到2031年約26%，低於公司29–30%目標；若FY2027非GAAP營業利益率財測低於25%，再下修Base","watch":"FY2027營業利益率財測（2027年2月）；營收年增與活躍用戶年增的差距","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","channel_business_model_shift#1"]},{"view":"價格已反映太多","evidence":"26週上漲34.1%；前瞻本益比30.4倍；分析師提到2027年共識營收約年增11%已接近公司10%以上的下限；Q4財測隱含年增約10%；Q3前賣方均價86.16美元、區間65–112美元，Barclays目標71美元","assumption":"市場已把CMS通過與利益率擴張大致計入","consequence":"CMS通過只換來小幅上修，股價在26倍FY2027E附近原地踏步；Base五年含回購年報酬約9%，只是中等","ruling":"部分採納：不視為高估（自身倍數在近4個年度端點最低處、Base終端22倍已假設再壓縮），但也不構成便宜，故等事件結果、不追價","watch":"前瞻本益比若升到35倍以上而共識EPS未上修，轉為減碼或不追","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_pe_percentile","f_ps_percentile"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 82.29","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=82.29","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層承諾對帳（一致判斷）","cause":null,"prior_field":null,"side_a":"Q2法說（2026-07-30，CFO Jereme Sylvain）：全年營收5.18–5.25B、非GAAP營業利益率23.5–24%、毛利率Q3見高後因Ireland回落；投資人日（2026-05-14）：2026年回購10億美元、年底接近半數美國用戶轉15日款、加拿大下半年上市","side_b":"Q3法說（2026-10-29）：營收財測升至5.20–5.25B、營業利益率升至約24%、Q3毛利率65.1%並預告Q4回落；10億美元回購已完成並再授權10億美元；15日款轉換進度「接近50%」照舊；加拿大11月上市","ruling":"一致：近兩季承諾全部兌現或超前，管理層財測可信度加分；國際年增僅5%在Q2已預告高基期，不算改口","evidence_level":"公司法說逐字稿與8-K","settle_metric":"2027年2月財測營收年增是否≥10%","if_then":["若2027年財測營收年增低於10%，視為投資人日逐年10%以上承諾首度失守，下修Base並暫停任何加碼"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","major_events#2"]},{"axis":"定價：管理層稱穩定對外部壓價訊號","cause":null,"prior_field":null,"side_a":"CFO（Q3法說）：全球未見定價惡化，國際按給付分級配產品、價格穩定；Q3非GAAP毛利率65.1%為2022年Q4以來最高","side_b":"對手提到自費市場定價逆風；研究機構預測OTC感測器兩年內跌破60美元；CMS 2028年起競標並預期降低Medicare給付；CVS排他合約流失","ruling":"可調和（時間與市場不同）：現況數據站在管理層這邊，壓價主要落在自費與新進國際市場以及2028年後的Medicare；採管理層現況，把未來壓價放進Bear 30%","evidence_level":"公司財報為硬數據，壓價方為預測與對手口徑","settle_metric":"非GAAP毛利率（排除Ireland）與2027年競標得標價","if_then":["若2027年下半年非GAAP毛利率回不到64%以上且管理層改口承認價格壓力，Bear機率上調到40%並停止加碼","反向：若2027年毛利率站上66%且競標價格降幅低於10%，維持Base並解除價格疑慮"],"evidence_refs":["competitive_share_entrants#2","end_markets#2"]},{"axis":"份額方向","cause":null,"prior_field":null,"side_a":"DXCM在拿份額：Q1營收年增15%對Abbott CGM 7.5%；Q3美國年增14%、連續多季拿份額（CEO）；CFO稱兩大廠合計美國低雙位數成長，DXCM占其中一大塊","side_b":"Abbott份額水準較高（2025年全球52.8%、美國48.5%），分析師認為雙分析物策略可能讓Abbott領先；Barclays以Libre份額壓力給減碼評等、目標71美元","ruling":"可調和（水準對方向）：Abbott份額水準較高、看空方是預測，看多方是已實現成長率；採已實現數據，競爭趨勢判持平而非上升","evidence_level":"已實現季報對第三方預測","settle_metric":"每季DXCM美國營收年增對Abbott糖尿病照護營收年增","if_then":["若DXCM美國營收年增連2季低於Abbott同期，競爭趨勢改判下降，以目前B級護城河即轉為迴避：未建倉不建、已持有清倉","反向：若連4季領先3個百分點以上，可上調執行面評分"],"evidence_refs":["competitive_share_entrants#0","end_markets#1","substitute_technology#3","competitive_share_entrants#3"]},{"axis":"營收成長對用戶成長","cause":null,"prior_field":null,"side_a":"管理層：定價穩定、活躍用戶年增十幾%上段、新病患創紀錄","side_b":"營收只年增11%、Q4財測隱含約10%，每用戶營收下滑","ruling":"可調和：不是單價下跌而是組合轉向（15日款年用量少、第二型非胰島素與國際分級產品單價低、藥局通路）；但這正是利益率擴張被稀釋的路徑，已列入論點成功但股東經濟變差的反證","evidence_level":"管理層口徑與財報推算","settle_metric":"營收年增減活躍用戶年增的差距（公司不定期揭露）","if_then":["若2027年營收年增低於10%而管理層仍稱用戶年增十幾%，視為每用戶營收下滑加速，Base營業利益率路徑再下修1個百分點"],"evidence_refs":["channel_business_model_shift#1","customer_concentration_credit#2"]},{"axis":"PBM合約流失的財務影響","cause":null,"prior_field":null,"side_a":"CFO（Q3法說）：該PBM占美國營收不到4%，轉非優先後病患自付大幅提高、對2027年財務影響不大；CEO稱2027年處方集已鎖定，Dexcom Direct 2027年初上線協助轉醫療給付","side_b":"流失發生在不到一季前，影響尚未進財報；若其他PBM跟進排他模式，價格與量同時受壓","ruling":"管理層歸因不採信也不否定，標為未證、監測；預登記：2027年Q1與Q2美國營收年增若連2季低於10%且公司歸因PBM，視為影響不大的說法證偽","evidence_level":"管理層一方說法","settle_metric":"2027年上半年美國營收年增","if_then":["證偽則減碼一半，或延後建倉到2028年處方集公布"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"A軸競爭惡化：中國新興廠與醫材以外業者進場、FDA一般健康器材指引降低門檻、Abbott雙分析物先行、對手用AI加速創新、OTC價格下探","side_b":"B軸結構轉好：CONNECT登上NEJM屬A級證據、四大商業PBM涵蓋所有糖尿病患、CMS決定預期年底前、全球涵蓋人數2030年預期到約5,200萬；C軸其他：CMS競標2028年起、PBM排他、通路轉向藥局、經銷商集中","ruling":"雙向拉鋸：2027年前B軸（涵蓋擴張）占上風，2028年起A軸與C軸的競標壓價轉強；依據為CMS決定預期2026年底、競標付款2028-01-01起變更","evidence_level":"10-K、公司法說與第三方研究","settle_metric":"CMS涵蓋決定與2027年競標得標價","if_then":["若CMS涵蓋通過但競標得標價降幅超過15%，判定C軸壓過B軸，Base營收成長下修到8%"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","end_markets#3","supply_demand_durability#1"]},{"axis":"等CMS決定對現在就買","cause":null,"prior_field":null,"side_a":"本判斷：等CMS決定公布再動，因為否決是最大單一敏感度、Base含回購年報酬僅約9%、股價仍在250週均線下方","side_b":"現在就買的最強論證：CONNECT登上NEJM且屬A級證據，CMS通過機率約75–80%；自身倍數在近4年最低處；公司每年至少50% FCF回購；通過消息一出可能跳空，等待成本是錯過重估","ruling":"選等待：通過的上行已部分反映在26週上漲34%與30倍前瞻本益比，否決的下行（Bear約−42%）大於通過的跳空；事件只剩約兩個月，等待成本有限","evidence_level":"情境樹機率與事件時點","settle_metric":"CMS決定內容","if_then":["CMS通過且未設門檻→重跑判斷，首倉以小部位起步","CMS否決或設限→不建倉，等2027年2月財測確認營收年增≥10%再評","價格先走證據未到：決定公布前股價續漲→不追；跌到約70美元但決定未出→仍等決定，不搶跑"],"evidence_refs":["end_markets#3"]}],"triggers":[{"n":1,"text":"CMS第二型非胰島素CGM涵蓋決定（唯一致命點）","type":"Single Thing","maps_to":"single_thing","metric":"CMS決定內容與公布時點","threshold":"否決、附A1c門檻等限制，或2027-03-31前仍未決定","action":"不建倉；已持有則減碼一半，若2027年財測營收年增也低於10%則清倉","source_freq":"CMS公告與公司8-K，事件型","date":"2026-12-31","evidence_refs":["end_markets#3","supply_demand_durability#1"]},{"n":2,"text":"涵蓋通過後重新評估進場","type":"估值rearm","maps_to":"R1","metric":"CMS決定內容","threshold":"通過且未設A1c門檻","action":"重跑判斷，首倉以小部位起步，跳空超過FY2027E 30倍（約94美元）不追","source_freq":"事件型","date":"2026-12-31"},{"n":3,"text":"2027年全年營收財測","type":"假設驗證","maps_to":"H1","metric":"FY2027營收財測年增率","threshold":"≥10%","action":"低於10%：停止加碼、Base營收路徑下修","source_freq":"年度財測","date":"2027-02"},{"n":4,"text":"2027年營業利益率財測","type":"假設驗證","maps_to":"H2","metric":"FY2027非GAAP營業利益率財測","threshold":"≥25%","action":"低於25%：Base利益率路徑下修、Bear機率升到35%","source_freq":"年度財測","date":"2027-02"},{"n":5,"text":"毛利率守不住（含Ireland投產歸因期限）","type":"風險","maps_to":"R2","metric":"非GAAP毛利率","threshold":"2027年Q3仍未回到64%以上（Ireland歸因證偽），或之後連2季低於62%","action":"減碼一半","source_freq":"季報","date":"2027-10","evidence_refs":["competitive_share_entrants#2","end_markets#2","channel_business_model_shift#1"]},{"n":6,"text":"品質、FDA與訴訟里程碑","type":"風險","maps_to":"R3","metric":"FDA警告信結案、召回、使用者訴訟集體認證、證券訴訟和解","threshold":"新警告信或一級召回；使用者訴訟取得集體認證","action":"集體認證加不利和解→減碼一半；刑事或SEC調查介入→清倉","source_freq":"8-K與10-Q，事件型","date":null,"evidence_refs":["regulatory_antitrust#2","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","lawsuit_class_action#2"]},{"n":7,"text":"關稅與匯率吸收失敗","type":"風險","maps_to":"R2","metric":"公司歸因關稅或匯率的毛利率與營收影響","threshold":"單季歸因關稅使毛利率年減超過100bp，或匯率使全年營收財測下修超過1%","action":"減碼","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#0"]},{"n":8,"text":"供貨中斷","type":"風險","maps_to":"R4","metric":"出貨中斷或延遲公告、存貨水準","threshold":"任何因單一來源零件或廠區問題造成的出貨中斷","action":"減碼一半，待恢復出貨且毛利率確認","source_freq":"8-K與季報，事件型","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","customer_second_source#0"]},{"n":9,"text":"經銷商集中度","type":"風險","maps_to":"R5","metric":"最大經銷商營收占比（未扣回饋前）與應收占比","threshold":"營收占比>60%或應收占比>30%","action":"倉位上限下修一級並檢視合約條款","source_freq":"10-K年度","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":10,"text":"份額轉向流失","type":"清倉","maps_to":"R6","metric":"DXCM美國營收年增對Abbott糖尿病照護營收年增","threshold":"連2季落後","action":"競爭趨勢改判下降，清倉或不建倉","source_freq":"季報","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","end_markets#1","substitute_technology#0","substitute_technology#3"]},{"n":11,"text":"估值過熱","type":"減碼","maps_to":"H1","metric":"前瞻本益比","threshold":"≥35倍且FY2027E共識未上修","action":"減碼或不追","source_freq":"每日價格與每月共識","date":null},{"n":12,"text":"Q4 2026財報與2027年財測後重跑判斷","type":"複審日期","maps_to":"H1","metric":"全年財測與CMS進度","threshold":"財報公布","action":"重跑判斷","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"CMS第二型非胰島素CGM涵蓋決定","bear_threshold":"否決、附A1c門檻，或2027-03-31前未決定","window":"2026-12～2027-03","source":"CMS公告、公司8-K","last_status":"unknown"},{"metric":"非GAAP毛利率（Ireland投產後）","bear_threshold":"2027年Q3未回到64%，或之後連2季低於62%","window":"2027年Q3起逐季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"全年營收年增率","bear_threshold":"FY2027財測或實績低於10%","window":"2027年2月財測與各季","source":"公司財測與季報","last_status":"warning"},{"metric":"美國營收年增率","bear_threshold":"連2季低於8%或連2季落後Abbott糖尿病照護","window":"逐季","source":"DXCM與Abbott季報","last_status":"ok"},{"metric":"最大經銷商營收占比（未扣回饋前）","bear_threshold":">60%","window":"年度","source":"10-K集中度附註","last_status":"warning"}],"evidence_dismissed":[{"ref":"$.decision_inputs.market_wrong_reason_given","reason":"判斷沒有主張市場看錯，填否是照實：估值結論是合理不便宜，反證紀錄「價格已反映太多」一條部分採納，承認市場已大致計入CMS通過與利益率擴張。報酬來源是EPS年增約13%，終端倍數還從30.4倍壓到22倍，論點不靠倍數往上修，而「市場錯在哪」的具體理由只在論點靠倍數往上修時才需要。觀望是等CMS決定這個事件，不是等市場改正看法，等待條件已寫明通過與否決各自的做法；閘自己也判定輸入互相一致、應降為輕微"},{"ref":"$.answers.q1_business.verdict_values.industry.sd_verdict_source","reason":"這段結論沒有引用閘點名的那條供需資料，依據已逐一寫在欄內：Baird與MarketBeat彙整的第一型滲透率約60–65%、CEO投資人日的第二型非胰島素約2,500萬人與商保涵蓋約25%。該條只在CMS決定時點的三處（產業態勢三軸、唯一致命點觸發、R1）與另一條終端市場資料並列引用，拿掉不影響供需判斷；閘的疑點是附件沒附原文，不是判斷漏接，閘也寫明找不到漏接"}],"decision_out":{"role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=34.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等CMS第二型非胰島素CGM涵蓋決定（公司預期2026年底前）：通過且未附A1c門檻才重跑判斷建首倉；否決或設限則等2027年2月財測'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[],"verdict":"觀望","rearm_trigger":"CMS公布第二型非胰島素CGM涵蓋且未附A1c門檻等限制（預期2026年底前），之後重跑判斷再建首倉","exec_line":"決定公布前不建倉、不搶跑；通過且非GAAP毛利率維持62%以上→重跑判斷，首倉小部位，跳空超過FY2027E 30倍（約94美元）不追；否決或設限→不建倉，等2027年2月財測確認營收年增≥10%再評"},"reasoning":{"industry":"收錢方式：感測器每10或15天更換一次，屬經常性耗材收入。Q3 2026營收13.445億美元、年增11%，美國9.70億美元（年增14%、約占72%）、國際3.75億美元（年增5%、約占28%）；非GAAP毛利率65.1%、營業利益3.395億美元（25.3%），GAAP營業利益3.272億美元（24.3%），兩者只差約1,230萬美元。全年財測營收52.0–52.5億美元（年增12–13%）、非GAAP營業利益率約24%（上調）。錢卡在哪：Q2經銷通路約占營收84%，前三大經銷商未扣回饋前營收占比55%／35%／46%且三年逐年上升，是本檔最明顯的單點依賴；付款端由PBM處方集與Medicare決定，CVS排他合約流失（CFO Q3法說：占美國營收不到4%）即是例證。產業處於擴張期：CFO稱兩大廠合計美國營收低雙位數成長，全球涵蓋人數預期由約2,300萬升到2030年底約5,200萬。供需屬結構性持久，風險在單價而非需求","moat":"機制：感測器準確度、與多款胰島素幫浦相容的自動給藥系統與Share/Follow家屬分享，讓第一型與胰島素使用者轉換成本高（CEO Q3法說：多款幫浦與對手不相容），再加上一連串隨機試驗堆出的給付證據（CONNECT登上NEJM）。方向：執行面擴大，Q3非GAAP毛利率65.1%、年增約380bp，營業利益率25.3%，美國連續多季拿份額，Q1營收年增15%對Abbott CGM 7.5%，15日款新黏膠讓存活率提高4–5個百分點；定價面小幅縮減，PBM排他合約流失、對手在自費市場降價、OTC價格下探、2028年競標在即。兩者相抵判持平。同業ROIC事實表未涵蓋，改看利潤率：DXCM營業利益率24.0%、FCF利潤率33.9%，高於Abbott 15.9%／15.7%與Medtronic 19.0%／16.3%，但後兩者是多角化集團，只能當方向參考。評分執行8、定價6，B級。報酬持續期四檢查點都落在中間（🟡），主因付款方與政策掌握分配權","growth":"共識EPS：FY2025A 2.09（GAAP攤薄）→FY2026E 2.71→FY2027E 3.13→FY2028E 3.67（Koyfin快照，EPS家數事實表未涵蓋；營收共識27位分析師），三年年增約20.6%，排除FY2026利益率修復後FY2026E→FY2028E約16.4%，同期營收約年增11%。內生成長天花板算不出精確數字（投入資本未涵蓋），但FY2025淨利8.36億美元、FCF 10.77億美元，再投資率約−29%（扣回SBC後約−11%），只要增量ROIC為正，天花板就在零以下，共識EPS成長全數超出天花板；超出部分可歸因於營收約11%（既有產能承接涵蓋擴張的量）、利益率擴張（投資人日：營業利益率每年約+150bp）與淨回購（年約2–3%），三項相乘約每年20%上下，共識沒有超過，不屬依賴重估。跑道：美國第一型滲透率已約60–65%，第二型2030年滲透率假設10–15%、非胰島素商保涵蓋25%，以現行速度到30%滲透約需8–10年（推估），加上國際直營化、Stelo自費與前期糖尿病篩檢（CEO Q3法說）等第二曲線，五年後跑道判寬。衰退信號亮2項（EPS成長高於營收逾5個百分點、自身倍數系統性下移），價值陷阱風險中等","governance":"FCF：2026年前三季9.062億美元（營業現金流11.204億減資本支出2.142億），FY2025 FCF 10.77億美元對淨利8.36億美元，轉換率1.29倍；SBC占營收2.7%（Q3 3,680萬美元）；淨現金4.25億美元。現金去向：2026年回購10億美元已完成，董事會2026-10-29再授權10億美元至2027年底，承諾2027年至少50% FCF回購；小型收購Nutrisense（價格未揭露）與歐洲經銷商（簽約未完成）。治理：投資人日宣布與Elliott合作新增2名董事、董事會原無獨立醫材背景董事；CFO於Q3兼任營運長。回購均價、近三年現金去向四分、債務到期結構事實表未涵蓋","valuation":"現價82.29美元＝FY2026E共識EPS的30.4倍、FY2027E 26.3倍、FY2028E 22.4倍。要拿到約9%年報酬，需要五年EPS年增約13%（Base 5.05美元）且終端倍數不低於22倍（約等於現價對FY2028E的倍數）。EPS成長我信大半（財測連升、利益率路徑清楚），倍數再壓縮的風險還在（競標、價格戰）。一年目標：FY2028E Base EPS 3.55美元×24.5倍≈87美元，約+6%；五年：5.05×22≈111美元，約+35%，另加回購。賣方均價86.16美元（Q3前，25位），區間65–112美元、最高最低比1.7倍，方向支持合理不便宜的判斷。同業倍數事實表未涵蓋","premortem":"最可能看錯的三條路：一是價格壓縮比預期快（2028年競標、OTC價格下探、PBM排他）；二是CMS涵蓋否決或附門檻；三是品質與訴訟復發。歷史最大回撤、空方最強數字與訴訟金額事實表未涵蓋；股價82.29美元仍低於250週均線92.85美元、該均線13週斜率−0.75%，說明過去五年曾在更高價位後長期下跌，26週已反彈34.1%。完整反證見反證紀錄"},"plain":{"six":{"how_it_makes_money":"賣CGM感測器耗材，量來自第一型與第二型糖尿病患，錢卡在付款方（PBM處方集、Medicare）與三大經銷商手上；第二型非胰島素涵蓋是下一段成長的關鍵","moat":"護城河持平（→），B級：執行面擴大，定價面小幅縮減","growth":"成長跑道寬：第二型非胰島素滲透率低且有A級臨床證據撐涵蓋，但成長以量為主、每用戶營收在降，EPS超額成長靠利益率與回購","capital":"現金轉換強、SBC稀釋低，回購積極但以現價換算的報酬偏低","valuation":"現價要求五年EPS年增約13%且終端倍數不低於22倍，才有約9%年報酬；EPS成長我信大半，倍數再壓縮的風險還在，合理不便宜","how_wrong":"最可能看錯在價格：競標、OTC與PBM排他讓每用戶營收降得比利益率擴張快"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等CMS第二型非胰島素CGM涵蓋決定（公司預期2026年底前）：通過且未附A1c門檻才重跑判斷建首倉；否決或設限則等2027年2月財測","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":82.29,"week26_return_pct":34.13,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母為FY2026E共識EPS，已含Ireland投產費用、無一次性扭曲；GAAP與調整後營業利益差距小（Q3約1,230萬美元），分母不是爭點"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"CMS第二型非胰島素CGM涵蓋決定（公司預期年底前）","impact":"高","watch":"是否附A1c門檻；生效時點是否仍為2027年中"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"ADA照護標準更新，是否納入CONNECT","impact":"中","watch":"是否把CGM列為第二型非胰島素的強建議"},{"date":"2026-11","date_precision":"month","type":"product","event":"G7 15 Day加拿大上市","impact":"低","watch":"國際15日款推進節奏"},{"date":"2026-Q4","date_precision":"quarter","type":"capacity","event":"Ireland廠投產，毛利率季減","impact":"中","watch":"Q4毛利率回落幅度與2027年回升速度"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026財報與2027年全年財測","impact":"高","watch":"營收年增是否≥10%、營業利益率是否≥25%"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"Dexcom Direct上線、日本G7 15 Day上市","impact":"中","watch":"PBM流失病患的留存"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"CMS涵蓋預定生效","impact":"高","watch":"第二型非胰島素新病患占比"},{"date":"2027","date_precision":null,"type":"regulatory","event":"CMS DMEPOS競標簽約（2028-01-01起付款變更）","impact":"高","watch":"CGM得標價與合約數"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"G8上市（2027年底或2028年初，視審查）","impact":"高","watch":"送件與核准時點、轉換策略"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,698B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河：B 級，趨勢持平</h2>
<p class="lead">執行面擴大、定價面縮減，兩者相抵判持平。</p>
<ul class="pts">
<li>護城河來自三件事：感測器準確度、與多款胰島素幫浦相容的自動給藥系統，以及 Share 與 Follow 家屬分享功能。第一型與幫浦使用者一旦綁定，轉換成本高，CEO 在 Q3 法說提到多款幫浦與對手不相容。再加上一連串隨機試驗堆出的給付證據，CONNECT 登上 NEJM，推動醫師處方偏好與給付擴張。</li>
<li>執行面評 8 分。Q3 非 GAAP 毛利率 65.1%，年增約 380bp，營業利益率 25.3%。美國連續多季拿份額，Q1 營收年增 15%，對 Abbott CGM 的 7.5%。15 日款新黏膠讓存活率提高 4 到 5 個百分點，但 CEO 在投資人日承認黏著問題尚未完全解決。</li>
<li>定價面評 6 分，比執行面弱。CVS 排他合約流失，CFO 稱占美國營收不到 4%，但來源只有公司法說，屬一方口徑。對手提到自費市場定價逆風，研究機構預測 OTC 感測器兩年內跌破 60 美元。CMS 的 2028 年競標又在前面等著。兩者相抵，趨勢判持平。</li>
<li>同業 ROIC 事實表未涵蓋，只能看利潤率。DexCom 營業利益率 24.0%、FCF 利潤率 33.9%，Abbott 是 15.9% 與 15.7%，Medtronic 是 19.0% 與 16.3%。後兩者是多角化集團，不代表 CGM 單一業務。Tandem 營業利益率 −4.4%，議價力弱，屬相容夥伴。Insulet 毛利率 71.1% 但 FCF 利潤率只有 8.7%。</li>
<li>報酬持續期四個檢查點全落在中間。需求基礎方面，CONNECT 把 6 個月 A1c 多降 0.9 個百分點，真實世界非胰島素第二型配戴率逾 80%，但付款者環節未成立。決策層級方面，第一型黏、第二型與 OTC 可比。價值鏈分配方面，前三大經銷商占比 55%、35%、46% 且逐年上升。社會容忍度方面，CMS 競標已顯示價格天花板。</li>
<li>三條威脅各有機率。Abbott 份額與規模領先、雙分析物 Libre Duo 先上市，機率 40%。中國新興廠與醫材以外的大型企業切入一般健康市場，加上 FDA 2026 年 1 月的一般健康器材指引，機率 30%。PBM 處方集改為單一品牌優先若擴散，機率 20%，CEO 稱 2027 年處方集已鎖定。</li>
<li>內生成長算不出精確天花板，因為投入資本事實表未涵蓋。但 FY2025 再投資率約 −29%，扣回股票薪酬後約 −11%，符號不變。只要增量 ROIC 為正，天花板就在零以下，共識 EPS 成長必須靠既有產能、利益率擴張與回購承接，不靠新增投入資本。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```