你是 stock-analyst v20 的**散文層（prose）agent**，標的 UNH（2026-10-17）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UNH_20261017/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：UNH　日期：2026-10-17　archetype：None　前份裁決：2026-05-25　B 衛星候選 / 觀望偏進場｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1770B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（461B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1123B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1336B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1249B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（942B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（888B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1865B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4570B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3110B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1770           3661-5230      5 條（2–6 內）  
s3                  8000         461           5277-7539      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3708          7904-11292      5 條（2–6 內）  
s6                 11000         942          7041-10058      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         888           1828-2612      5 條（2–6 內）  
s10                 5000        1865           2194-3135      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3110           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5372B；至少需散文≈39.63KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−130
−52%
−52
−45%
−36
−36%
−34%
−1.7%
−1%
0
0.09%
0.25
0.25%
0.41
0.5
0.7
01
1
1.13
1.2
1.3
1.3%
1.33
1.36
1.44
1.61
1.85
2%
2
02
2.2%
2.26%
2.26
2.3%
2.48%
2.6%
3
3%
3.3%
3.4%
3.5
3.6%
3.93
4%
04
4
4.2
4.24%
4.69
4.82%
5
5%
5.1%
5.6%
5.8%
6
06
6%
7
07
7%
7.2%
7.35
7.5%
7.9%
08
8%
8
8.77%
9
10
10%
10.4
10.4%
11
11%
11.4
12%
12
13%
13
13.23
14
14.8%
14.8
15
15%
16%
16
17%
17
17.3
17.6
17.75
17.8
18
18.45
19
19.50
19.51%
19.58
19.6
19.8
19.87
20.00
20%
20
20.2
20.50
20.5
21
21.5
22
22.61
23
23.17
23.6
24
25%
25.13
25.6
26
26%
26.18
27.0%
27
27.2
28.2
29%
30%
30
30.8
31
31.2%
33
33.4
34.8
35
38%
38.6
39
40%
41.7%
42
43.13%
44
44%
44.1
49
49.72%
50%
50
55
60
62
65.63
70%
70
75%
80
88.1%
88.4%
88.8%
88.9%
89.8%
89.9%
90%
90
95%
100%
100
121
130
150
150%
221
229
258
264
360
388.47
397
399
400
401
401.43
443
460
461
733.4
843
860
863
2024
2025
2026
2027
2028
2029
2030
20261017
1,126.9
1,132
12,056
14,405
16,075
2,000
2,421
20,705
22,666
25,087
352,229
4,000
4,830
45,782
5,010
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
{"meta":{"ticker":"UNH","date":"2026-10-17","schema":"v15.0","contract":"v19","company_name":"UnitedHealth Group Incorporated"},"oneliner":"醫療成本率從 89.9% 降到 88.4%、全年指引兩度上調，利潤率修復第一段已兌現；現價約今年指引 19.6 倍，剩下的勝負在 2027 年定價壓不壓得住成本，以及監管調查會不會走到刑事或分拆。","thesis":{"H":[{"id":"H1","text":"醫療成本率修復可延續：2027 年定價追上成本趨勢，合併醫療成本率不回升，2027 EPS 至少成長 13%","2y":"FY2027 全年合併醫療成本率 ≤88.9%；2027 調整後 EPS 指引 ≥23.17 美元","5y":null,"10y":null,"threshold":"FY2027 醫療成本率 ≤88.9%（2026 指引 88.1%±0.25pp 上緣加 0.5pp）；2027 指引 ≥23.17 美元","source":"季報 8-K、2026 年底投資人說明會、2026-07-16 與 2026-10-13 法說","drift_rule":"TTM 調整後 EPS 連 2 季低於路徑 5% 以上→削弱；連 3 季低於 10% 以上→反轉"},{"id":"H2","text":"Optum Health 價值型照護重整成功，2028 年營業利益率回到管理層 6–8% 目標區","2y":null,"5y":"FY2027 Optum Health 營業利益率 ≥4%、FY2028 ≥6%","10y":null,"threshold":"FY2027 ≥4%；FY2028 ≥6%","source":"季報分部資料；2026-10-13 法說 Krista Nelson 的 2028 目標","drift_rule":"TTM 分部營業利益率偏離路徑 5% 以上連 4 季→削弱；偏離 10% 以上連 6 季→反轉"},{"id":"H3","text":"UNH 與 Optum 的垂直整合在監管下存續：各項 DOJ 調查不以刑事起訴公司或強制分拆收場，MA 仍是多數老人的選擇","2y":null,"5y":null,"10y":"十年內無公司層級刑事起訴、無強制分拆 Optum；MA 滲透率維持逾五成","threshold":"無刑事起訴、無強制分拆、單筆和解 ≤50 億美元；MA 滲透率 >50%","source":"10-Q／10-K 法律程序揭露、DOJ 公告、CMS 年度給付公告","drift_rule":"跨 2 個年度出現不利監管里程碑（起訴書、分拆條件）→削弱；跨 3 個年度→反轉；單筆和解逾 50 億美元或刑事起訴→直接反轉"}],"R":[{"id":"R1","text":"2027 年成本趨勢超出定價：MA 給付缺口比前一年更寬、CMS 2027 預告一度僅 +0.09%、風險池最快 2028 穩定、藥品關稅推高成本","h_ref":"H1","clock":"⚡","threshold":"單季醫療成本率連 2 季年增 >1pp 或單季 >89.8%；2027 指引撤回或下修 ≥10%","evidence_refs":["supply_demand_durability#1","supply_demand_durability#2","supply_demand_durability#3","supply_demand_durability#5","reg_tariff_export#1"]},{"id":"R2","text":"監管與法律升級：MA 業務刑事與民事調查、2024 年起的反壟斷調查、證券集體訴訟，任一走到起訴、分拆或巨額和解","h_ref":"H3","clock":"🔥","threshold":"公司層級刑事起訴、強制分拆 Optum、單筆和解 >50 億美元、集體訴訟認證通過","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#1","sec_investigation_restatement#0","major_events#2","lawsuit_class_action#0"]},{"id":"R3","text":"Optum Health 縮編變成結構性萎縮：價值型照護病人持續減少（第二季少約 70 萬人），雇主直接簽約與垂直整合提供者繞過付款方","h_ref":"H2","clock":"🐢","threshold":"FY2027 Optum Health 營業利益率 <4%，或服務病人數連 4 季年減","evidence_refs":["end_markets#2","channel_business_model_shift#0","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"MA 份額流失超出主動退出範圍：2026 約 60 萬、2027 約 39 萬人方案退出之後，若仍續失份額就是競爭力問題","h_ref":"H1","clock":"🔥","threshold":"2027 MA 會員淨流失 >150 萬，或 2028 年仍淨流失","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","channel_business_model_shift#2"]},{"id":"R5","text":"社會容忍度收緊：PBM 胰島素訴訟、AI 與事前授權拒賠遭國會追查，定價與利潤留存空間被立法壓縮","h_ref":"H3","clock":"🐢","threshold":"Optum Rx 被要求改變收費結構，或立法限制 AI 承保決定","evidence_refs":["regulatory_antitrust#3","substitute_technology#3"]}],"single_thing":{"description":"2027 年財測被撤回，或較年底發布值下修 10% 以上（醫療成本超出定價再次發生）","why_fatal":"醫療成本率是最大單一敏感項：FY2025 保費 352,229 百萬美元，每 1pp 約等於稅前 35 億美元、每股約 3 美元（稅率約兩成三為假設），相當今年指引 15%；財測撤回同時打掉盈餘路徑與管理層信用，EPS 與倍數一起下修","if_happens":"清倉；等新指引站穩兩季、醫療成本率回到年減後才重新研究","how_monitor":"每季醫療成本率年增幅、法說對成本趨勢的措辭、年底 2027 指引、2027 年 4 月第一季財報","probability":"約 20%（12–24 個月）；依據：Humana 稱 2027 投標給付與成本缺口比前一年更寬、BofA 稱風險池最快 2028 穩定，對照公司已按 MA 近 10%、商業險逾 11% 的趨勢定價"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":17.75,"peg_fy2":1.2,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":13.23,"FY2026E":19.87,"FY2027E":22.61,"FY2028E":26.18},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS（yfinance 年度財報）；FY2026E–FY2028E 為 Koyfin 2026-10-08 調整後 EPS 共識，早於第三季財報（管理層已把 2026 指引上調至至少 20.50 美元）；FY2025 調整後 EPS 事實表未涵蓋，基期與共識口徑不同，不可直接以基期算成長率"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UNH_20261017/scenario.json","archetype":{"primary":"轉機/特殊情境","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"利潤率谷底後的重整：前執行長回任、2026 年指引兩度上調、主動以會員數換利潤率"},"industry":{"clock_phase":"I","sd_verdict_source":"S&P Global 2026-08-17（Evercore 稱使用率 2026 年維持高檔、2027 年起改善）對照 BofA 2026-01-27（風險池穩定最可能在 2028、Medicaid 恢復可能延至 2029–2030）與 Humana 2026-08（2027 投標給付與成本缺口比前一年更寬）","bargaining":{"up":"醫療提供者與藥廠占上風：仲裁給付可達 Medicare 的 10–11 倍、部分地區仲裁金額近醫療支出 6%；專科藥成本持續上升","down":"給付方強勢：MA 費率由 CMS 公告（2027 定案 +2.48%，預告僅 +0.09%）、Medicaid 費率由各州調整且時點不一；雇主端國家帳戶續約率強","geo":"幾乎全在美國，藥品關稅經由保費間接傳導（部分州費率申報加計 2.2%–3.6%）"},"profit_pool_dir":"利潤池往醫療提供者與藥廠移動，UNH 以 Optum 垂直整合（照護、藥局、軟體）留住價值鏈中段，但這條路正受反壟斷審視","tam_table":{"expanded":false,"reason":"MA 滲透率已逾五成、會員數在縮，未來五年獲利來自利潤率修復而非份額或品類擴張，市場規模不是承重變數；分段 TAM 與利潤池占比數字事實表未涵蓋"}},"moat":{"mechanism":"承保規模＋Optum 垂直整合（照護、藥局、理賠與資料軟體），在醫療成本管理上多一層控制","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大：第三季醫療成本率 88.4%（去年 89.9%）、全年指引由 19.50–20.00 上調到至少 20.50 美元、Optum Health 營業利益 7.35 億美元（去年 0.41 億）；定價權縮減到持平：MA 份額 29%→26%（主動退出為主）、MA 2027 費率 +2.48% 仍低於成本趨勢、商業險長期利潤率目標時程被拉長。兩軸合判持平。","peer_na_reason":"事實表同業清單為製藥與 CDMO，管理式醫療同業（Humana、Elevance、CVS/Aetna、Cigna、Centene）的 ROIC 與利潤率事實表未涵蓋，無法計算同業報酬差距","threats":[{"level":"🔴","text":"監管結構性拆解：DOJ 自 2024 年起調查 UnitedHealthcare 與 Optum 醫師集團的關係，至今未見結案；若走到強制分拆，垂直整合的成本控制優勢直接消失","p":"15%","evidence_refs":["regulatory_antitrust#0"]},{"level":"🔴","text":"PBM 監管：FTC 胰島素訴訟對象含 Optum Rx，PBM 改制已讓公司放棄 spread pricing 與回扣留存，若立法再收緊會壓縮 Optum Rx 利潤","p":"25%","evidence_refs":["regulatory_antitrust#3"]},{"level":"🟡","text":"付款方邊界被抹除：雇主繞過保險公司直接與醫療提供者簽約、垂直整合的醫療系統與大型 AI 業者可能讓部分保險功能商品化（BCG 2026-06 屬策略觀點）","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"MA 份額流向 Humana 等同業：UNH 份額 29%→26%，若 2027 年後主動退出結束仍續失份額，就不再是定價紀律而是競爭力問題","p":"25%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"資安單點失效：2024-02-21 Change Healthcare 勒索軟體事件顯示整合後服務集中，一次攻擊可癱瘓大量醫療系統（二手彙整來源）","p":"10%","evidence_refs":["geo_supply_chain#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"醫療保障屬需要而非想要；MA 是逾半數合格老人的選擇，公司稱 MA 老人每年平均省逾 4,000 美元。使用者（病人）、決策者（老人或雇主）、付款者（CMS、各州、雇主）三角色分開，最弱一環是付款方的給付是否足夠，這個風險另記在社會容忍度與價值鏈。"},{"item":"決策層級","level":"🟡","text":"個人 MA 會員每年開放期可換方案，轉換成本低，UNH 退出方案的會員多數流向同業；雇主國家帳戶續約率強、Optum Rx 留存率在 90% 高段，企業客戶端黏著度較高。兩種決策單位黏性差距大，合判中等。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈總量被上游拿走更多：仲裁給付達 Medicare 10–11 倍、專科藥漲價，TTM 營業利益率 4.82% 對照 FY2022 8.77%；Optum 垂直整合在照護與藥局端留住一部分，第三季 Optum Health 利益回升，但這正是反壟斷審視的對象。"},{"item":"社會容忍度","level":"🔴","text":"高必要×高政治敏感：事前授權與 AI 拒賠遭參議員追查、DOJ 調查 MA 業務、FTC 告 PBM 胰島素回扣。公司已主動把價格放在經濟上限之下（減少 30% 事前授權、回扣全數轉嫁、交易所利潤返還、基金會 10 億美元），定價上限由政治決定；授權法源（MA 給付、PBM 規則）都在修法討論中。"}],"roiic":"事實表未涵蓋（投入資本與歷年增量資本未收錄）","reinvest_rate":"低：2026 前九個月資本支出 2,421 百萬美元約為營運現金流 25,087 百萬美元的一成，股息加回購超過 FY2025 淨利；折舊、營運資金與收購淨額事實表未涵蓋，無法依公式算出","endo_ceiling":null,"formula_note":"當期 ROIC 無法以稅後營業利益率×投入資本周轉率計算（投入資本未收錄）。內生成長＝增量 ROIC×再投資率也無法算出，所以內生上界沒有數值。情境輸入裡「共識成長超出內生上界」的標記是定性判斷，不是數值比較：再投資率低（股東回報超過淨利、資本支出約營運現金流一成），內生成長貢獻偏小，共識 EPS 年增約 14.8% 主要來自利潤率修復與淨回購，不是再投資驅動。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","UNH":19.51,"LLY":83.4,"NVO":80.65,"STVN":29.17,"1A8.DE":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","UNH":4.82,"LLY":49.72,"NVO":43.13,"STVN":17.37,"1A8.DE":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","UNH":5.25,"LLY":17.02,"NVO":14.51,"STVN":-2.51,"1A8.DE":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","UNH":null,"LLY":18.32,"NVO":17.64,"STVN":2.08,"1A8.DE":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"LLY","gm":83.4,"om":49.72,"fcf_margin":17.02,"rd_intensity":18.32,"strategy_note":"製藥業者，營業利益率 49.72%，是 UNH 的成本來源（GLP-1 等高價藥）而非同業，不能拿來比利潤率差距。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"NVO","gm":80.65,"om":43.13,"fcf_margin":14.51,"rd_intensity":17.64,"strategy_note":"製藥業者，營業利益率 43.13%，同樣站在價值鏈上游向保險方收錢，不是可比同業。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"STVN","gm":29.17,"om":17.37,"fcf_margin":-2.51,"rd_intensity":2.08,"strategy_note":"藥品委託開發製造業者，FCF 為負，業務與管理式醫療無關，不作對照。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"1A8.DE","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表無財務資料，無法判讀。"}]},"growth":{"driver_mix":"價（重新定價、利潤率修復）＋回購為主，量為負，併購小","runway_years":"已逾 30% 滲透門檻（MA 滲透率逾五成），不適用滲透年數","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界無法以增量資本報酬計算（投入資本事實表未涵蓋）；股東回報（股息逾 80 億＋回購 50 億美元）超過 FY2025 淨利 121 億美元，保留盈餘再投資率低，共識 EPS 年增約 14.8% 主要來自利潤率修復與淨回購","segments":[{"item":"UnitedHealthcare","value":"第三季營收 863 億美元微降；服務人數 4,830 萬（去年 5,010 萬）；Medicare 利潤率 2026 接近 2–4% 區間上緣，Medicaid 2026 為谷底（略優於 −1%），商業險利潤率回到 7% 以上的時程被拉長"},{"item":"Optum Rx","value":"第三季營收 399 億美元（去年 397 億）；處方量 3.93 億張；外部客戶首度過半；總處方量季減約 5%、專科藥量 +2.6%"},{"item":"Optum Health","value":"第三季營收 229 億美元年減 10%（價值型照護病人減少），營業利益 7.35 億美元（去年 0.41 億）；目標 2028 年營業利益率 6–8%，管理層暗示第四季因風險季節性與投資轉負"},{"item":"Optum Insight","value":"第三季營收 55 億美元年增 3%；2026 為投資年，管理層稱 2028 年起加速成長，屬自述"}],"decay_signals":["核心市占近 12 個月縮減：MA 份額約 29%→26%（多為主動退出無利方案）","EPS 成長顯著高於營收成長：共識 FY2026→FY2028 EPS 年增約 14.8%，FY1→FY2 共識營收僅 +3.4%，差距超過 5pp","產業估值倍數近 3 年是否系統性下移：同業倍數事實表未涵蓋，未計入"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：收購金額相對 4,000 億美元市值與企業價值小，獲利修復來自定價與成本管理；分年回購均價事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Amedisys 33 億美元、Alegeus 已完成，收購後增量報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"以 2026 指引計盈餘殖利率約 5.1%（20.50÷401.43）；10 年期公債殖利率事實表未涵蓋，無法對照","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"前九個月股權激勵 843 百萬美元，同期回購 50 億美元，回購遠大於股權激勵，淨稀釋率推定為負；股數年變化事實表未涵蓋","grade":"過"}]},"valuation":{"basis":"前瞻本益比（今年調整後 EPS 指引與共識）＋PEG，輔以年度端點本益比與營收倍數分位","peers":{"expanded":false,"reason":"事實表同業為製藥與 CDMO，不是管理式醫療，拿來當倍數錨會跨族群；管理式醫療同業倍數事實表未涵蓋"},"fwd_pe":20.2,"peg":1.36,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"PEG 約 1.36（FY1 共識前瞻本益比 20.2 倍÷共識兩年 EPS 年增 14.8%）落在 1–2 合理區；以指引計 19.6 倍、FY2 共識 17.8 倍；年度端點本益比分位 44；Base 情境年化約 9–10% 屬中等→合理偏便宜，未到便宜。五年分位：事實表只有 4 個年度端點，無五年序列，留空。","upside_short_pct":10.4,"upside_mid_pct":14.8},"trap_analysis":{"verdict":"🟡","label":"利潤率修復期的定價與監管尾部風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"BofA 稱風險池穩定最快 2028、CMS 編碼變更若定案會把目標利潤率延到 2028 以後、Medicaid 恢復可能延至 2029–2030；DOJ 對 MA 業務的刑事與民事調查仍在，UNH 已在 SEC 文件中揭露。","assumption":"2027–2028 年利潤率持續回升，調查以金錢和解收場","consequence":"給付缺口結構化加上監管強制調整 Optum 與保險的關係，EPS 停在 20–22 美元、倍數 12 倍，五年股價約 264 美元（−34%），中途回撤可到五成","ruling":"部分採納：列入 Bear 機率 30%；與唯一致命點部分重疊（成本超出定價部分），監管部分另設清倉條件","watch":"每季醫療成本率年增、10-Q 法律程序段落、CMS 2028 年 MA 給付預告（2027 年初）","evidence_refs":["supply_demand_durability#5","regulatory_antitrust#2","sec_investigation_restatement#0"],"fact_refs":["f_kpi7_mcr"]},{"view":"論點成功但股東經濟變差","evidence":"管理層承諾 2026 年底逾 95% PBM 客戶採回扣全數轉嫁、取消 spread pricing、事前授權減少 30%、交易所利潤返還、基金會 10 億美元，CFO 說這類投資不是一次性；參議員追查以 AI 與事前授權拒絕老人術後照護；2025 年三大評等機構展望轉負、AM Best 下調母公司評級；證券集體訴訟在案。","assumption":"利潤率回到歷史水準後，盈餘能經回購與股息回到股東","consequence":"社會容忍度把定價上限壓在經濟上限之下，營業利益率可能停在 6% 上下而非 FY2022 的 8.77%；訴訟和解與評等壓力吃掉回購預算，每股盈餘成長落到 8–10%","ruling":"採納：社會容忍度判紅燈；Base 終端倍數由現值 19.6 倍降到 17 倍、回購殖利率只抓 1.3% 反映","watch":"S&P／Moody's 評等行動、年度回購金額、集體訴訟認證與和解金額","evidence_refs":["customer_concentration_credit#2","substitute_technology#3","lawsuit_class_action#0"],"fact_refs":["f_peer_unh_operating_margin_pct","f_kpi5_sbc"]},{"view":"價格已反映太多","evidence":"26 週上漲 25%；股價 401 美元已是第三季前賣方目標均值 443 美元的九成；FY2 共識 22.61 美元低於管理層暗示的 23.17 美元，市場可能已用管理層數字定價。","assumption":"市場仍在折價監管尾部與 2027 不確定性","consequence":"若 2027 指引只落在 13% 下緣，三年上檔約 +15%，回報主要剩股息與 EPS 複利","ruling":"反駁一半：以 FY2 共識計約 17.8 倍、年度端點本益比分位 44、P/S 分位 19.8，倍數沒有擴張，漲幅來自 EPS 上修（FY1 共識三個月上修 7.5%）；但不追高，進場分批","watch":"年底 2027 指引、第三季後賣方目標價更新","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_pe_percentile","f_ps_percentile","f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2"]}],"max_dd":{"lo":-52,"hi":-36,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 388.47 → 本次 401.43（+3.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=388.47","side_b":"本次 price_at_dd=401.43","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 388.47 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 388.47 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 388.47 美元：Bull 價 733.4、Bear 價 264，五年期望值 +31.2%，基準年化 7.9%，不對稱比 1.85","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.85。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 388.47 美元：五年期望值 +31.2%，基準年化 7.9%，不對稱比 1.85","side_b":"本次情境、股價 401.43 美元：五年期望值 +27.0%，基準年化 7.2%，不對稱比 1.61","ruling":"再換股價、情境不動：起點價上漲 3.3%，五年期望值少 4.2 個百分點，基準年化少 0.7 個百分點，不對稱比由 1.85 降到 1.61。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2027 成長起點","cause":null,"prior_field":null,"side_a":"管理層（2026-10-13 CFO Wayne DeVeydt）：2026 調整後 EPS 至少 20.50 美元是成長基準，2027 至少從長期 13–16% 的下緣起算，共識低估。","side_b":"BofA（2026-01）：風險池穩定最可能在 2028、編碼變更延後目標利潤率；Humana（2026-08）：2027 投標給付與成本缺口比前一年更寬；同場 Tim Noel 承認商業險長期利潤率目標時程被拉長。","ruling":"可調和（程度差異）：2027 成長可由 Optum Health 修復、MA 利潤率站上 2–4% 上緣與回購撐起，不必等商業險回到 7% 以上；但成長來源變窄。採管理層方向，Base 以 12% 起算後逐年降速。","evidence_level":"管理層指引對賣方研究與同業說法","settle_metric":"2026 年底投資人說明會的 2027 調整後 EPS 指引；2027 年第一季合併醫療成本率","if_then":["若 2027 指引 ≥23.17 美元且第一季醫療成本率不高於去年同季→加碼至目標倉位","若 2027 指引低於 21.5 美元（成長不到 5%）→減碼一半","反向：若指引未出但股價先漲過 460 美元（FY2028 共識約 17.6 倍）→不追"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#3","supply_demand_durability#5"]},{"axis":"成本趨勢是否在加速","cause":null,"prior_field":null,"side_a":"BofA Kevin Fischbeck（2026-10-13 法說提問）：追蹤資料顯示趨勢年初低、年中後加速，質疑 2027 是否按年底實際水準定價。","side_b":"Tim Noel（同場）：未見加速，政府業務趨緩、商業險在 11% 以上持平，已用更即時資料定價。","ruling":"不可裁決至 2027 年 4 月第一季財報：決勝數據今天不存在，第四季又是風險季節性高峰；暫採公司說法，但不據此加碼。","evidence_level":"雙方皆為說法，無第三方數據","settle_metric":"2027 年第一季合併醫療成本率年增幅","if_then":["若第一季醫療成本率年增超過 1pp→減碼一半並停止加碼","若年增不超過 0→解除加碼限制"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"管理層承諾兌現（2026-07-16 對 2026-10-13）","cause":null,"prior_field":null,"side_a":"第二季法說 CFO Wayne DeVeydt：全年 19.50–20.00 美元、第三季略多於第四季；Michael Cotton：Medicaid 全年 −1% 至 −1.7%；Timothy Noel：Medicare 趨勢偏低不代表轉折點。","side_b":"第三季實際：調整後 EPS 4.69 美元、全年上調到至少 20.50；Medicaid 改為略優於 −1%；Bobby Hunter：Medicare 利潤率接近 2–4% 上緣；Optum Rx 留存仍在 90% 高段。","ruling":"一致：兩季財測都達成並上調，未見改口；仍迴避的是 2027 MA 投標假設與核心使用率點估計，第二季未答、第三季只說年底再給。","evidence_level":"公司財報與法說原話","settle_metric":"年底 2027 指引是否含 MA 會員與分部利潤率","if_then":["若年底仍不給 2027 MA 會員與利潤率指引→停止加碼直到 2027 年 1 月財報"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：UNH MA 份額 29%→26%、Humana 17%→20%；雇主直接簽約、垂直整合提供者與 AI 業者模糊付款方邊界。","side_b":"結構：CMS 2027 費率定案 +2.48%（高於預告 0.09%），同業多家稱 2027 起使用率與 Medicaid 改善；其他結構變數：DOJ 反壟斷與 MA 調查、FTC 胰島素訴訟、PBM 改透明收費、藥品關稅推升保費。","ruling":"雙向拉鋸：份額流失主要是 UNH 自己退出 PPO 等無利方案（2026 約 60 萬、2027 約 39 萬人），屬定價紀律；監管軸是持續的其他結構變動，方向偏負。","evidence_level":"產業報導與公司揭露","settle_metric":"2027 開放期後 MA 會員淨變化對公司預期約 −130 萬","if_then":["若 MA 會員淨流失超過 150 萬→停止加碼並重審護城河方向"],"evidence_refs":["competitive_share_entrants#0","regulatory_antitrust#3","substitute_technology#1"]},{"axis":"多空最強論證","cause":null,"prior_field":null,"side_a":"現在就買：盈餘從谷底修復且連兩季上調、FY2 本益比約 17.8 倍、股息 2.3% 加回購，利潤率只要回到歷史水準一半就有兩位數 EPS 成長。","side_b":"現在就賣：26 週已漲 25%，修復第一段已反映；2027 由 MA 給付缺口、商業險延後、監管調查三股力量決定，任一失手都是財測撤回級事件，而 2027 指引年底才給。","ruling":"偏多但不追：Base 年化約 9–10% 屬中等，主要來自 EPS 複利而非倍數；首倉分批，加碼綁 2027 指引。","evidence_level":"情境推演","settle_metric":"2027 調整後 EPS 指引","if_then":["若指引 ≥23.17 美元→加碼","若股價續漲但指引未出→不追","若股價下跌而指引與醫療成本率無損→分批反買"],"evidence_refs":[]},{"axis":"前份未輸出欄位（格式改版）","cause":"方法變動","prior_field":["archetype","cycle_position","moat_trend","runway_post_y5","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份為空值：舊版判斷未產出這些欄位","side_b":"本次：轉機/特殊情境、早循環、護城河方向持平、五年後跑道中等、機率 20／50／30、最大回撤 −36% 至 −52%；定期定額欄位本次不產出","ruling":"格式改版補欄，不是基本面變化","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"綜合評等與價值陷阱評級","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：綜合評等 B、價值陷阱中等","side_b":"本次：綜合評等 B、價值陷阱中等（皆維持）","ruling":"新證據雙向：第二、三季指引上調與醫療成本率改善支持維持；MA 份額流失與 BofA 認為 2028 才穩定的看法讓陷阱評級不下修","evidence_level":"公司財報＋賣方研究","settle_metric":"2027 指引與第一季醫療成本率","if_then":[],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"估值結論","cause":"方法變動","prior_field":["val"],"side_a":"前份：便宜（股價 388.47 美元）","side_b":"本次：合理偏便宜（股價 401.43 美元）","ruling":"股價只漲 3.3%，EPS 基準反而上修，變化不是來自價格；本次改用前瞻本益比對共識兩年成長（PEG 約 1.36，落在 1–2 合理區）定估值，前份推導未留存，以本次方法為準","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":null,"side_a":"前份未設唯一致命點（空值）","side_b":"2027 年財測被撤回，或較年底發布值下修 10% 以上（醫療成本超出定價再次發生）；發生即清倉","ruling":"新設：醫療成本率是數學上最大單一敏感項（每 1pp 約每股 3 美元），財測撤回是它的離散事件形式","evidence_level":"方法","settle_metric":"2027 年各季財報與指引","if_then":["若發生→清倉，新指引站穩兩季後重新研究"],"evidence_refs":[]},{"axis":"清倉、減碼門檻與重啟條件","cause":"方法變動","prior_field":null,"side_a":"前份清倉／減碼門檻（致命指標）與重啟條件皆為空值；前份風險表另有：刑事起訴、Optum 強制分拆訊號或單筆和解逾 50 億美元即重評，連 2 季醫療成本率高於 89.8% 削弱","side_b":"清倉＝公司層級刑事起訴、強制分拆 Optum 或單筆和解逾 50 億美元；減碼一半＝醫療成本率連兩季年增逾 1pp 或單季高於 89.8%；重啟＝2027 指引 ≥23.17 美元或股價 ≤360 美元","ruling":"前份風險表門檻全數保留（50 億美元、89.8%）並升格為明確動作，另加年增 1pp 的相對門檻，因單季醫療成本率有季節性","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"假設與風險門檻更新","cause":"新證據","prior_field":["H","R"],"side_a":"前份：H1 FY26 醫療成本率 ≤88.8%；H2 Optum Health FY28 利益率 3.5–4%；R3 連 4 季 Optum Health 利益率低於 2% 即反轉","side_b":"本次：H1 改看 FY2027 醫療成本率 ≤88.9% 與 2027 指引 ≥23.17 美元；H2 改為 FY2028 Optum Health 利益率 ≥6%、FY2027 ≥4%；R3 改為 FY2027 Optum Health 利益率低於 4% 減碼","ruling":"FY26 已接近完成（第二季指引 88.1%±0.25pp），驗證期往後移一年；Optum Health 門檻上移是因 2026-10-13 法說 Krista Nelson 明確給出 2028 年 6–8% 目標，且第三季利益已大幅回升","evidence_level":"公司指引","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"年底公布的 2027 調整後 EPS 指引是否達到管理層暗示的 13% 成長下緣","type":"假設驗證","maps_to":"H1","metric":"2027 調整後 EPS 指引","threshold":"≥23.17 美元（20.50×1.13）；低於 21.5 美元為失敗","action":"達標→加碼三分之一；低於 21.5 美元→減碼一半","source_freq":"年底投資人說明會／2027 年 1 月財報","date":"2026-12","evidence_refs":[]},{"n":2,"text":"醫療成本率失控：連兩季年增逾 1pp 或單季高於 89.8%","type":"風險","maps_to":"R1","metric":"單季合併醫療成本率","threshold":"連 2 季年增 >1pp，或單季 >89.8%","action":"減碼一半並停止加碼","source_freq":"每季 8-K","date":null,"evidence_refs":["supply_demand_durability#1","supply_demand_durability#2","supply_demand_durability#3","supply_demand_durability#5"]},{"n":3,"text":"2027 年財測被撤回或較年底發布值下修 10% 以上","type":"Single Thing","maps_to":"H1","metric":"2027 調整後 EPS 指引","threshold":"撤回，或下修 ≥10%","action":"清倉","source_freq":"每季財報與臨時公告","date":null,"evidence_refs":[]},{"n":4,"text":"監管調查走到公司層級刑事起訴、強制分拆 Optum，或單筆和解逾 50 億美元","type":"清倉","maps_to":"R2","metric":"DOJ 起訴、法院或和解條件","threshold":"任一發生","action":"清倉","source_freq":"10-Q 法律程序、DOJ 公告","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#1","sec_investigation_restatement#0"]},{"n":5,"text":"股價回落到 FY2 共識約 16 倍且基本面無損","type":"估值rearm","maps_to":null,"metric":"股價","threshold":"≤360 美元，且醫療成本率與指引未觸發減碼","action":"分批反買三分之一","source_freq":"每日","date":null,"evidence_refs":[]},{"n":6,"text":"2027 年第一季醫療成本率不高於 2026 年同季，且全年指引維持","type":"加碼","maps_to":"H1","metric":"2027 年第一季合併醫療成本率年增","threshold":"≤0pp 且指引不下修","action":"加碼至目標倉位","source_freq":"2027 年 4 月財報","date":"2027-04","evidence_refs":[]},{"n":7,"text":"2027 開放期後 MA 會員淨流失超出公司預期","type":"風險","maps_to":"R4","metric":"MA 會員年變化","threshold":"淨流失 >150 萬（公司預期約 130 萬）","action":"停止加碼並重審護城河方向","source_freq":"2027 年 1 月與 4 月財報","date":"2027-04","evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#2"]},{"n":8,"text":"Optum Health 重整未達進度","type":"風險","maps_to":"R3","metric":"Optum Health 全年營業利益率","threshold":"FY2027 <4%","action":"減碼三分之一","source_freq":"每季分部資料","date":"2028-01","evidence_refs":["end_markets#2","channel_business_model_shift#0"]},{"n":9,"text":"評等下調壓縮回購預算","type":"風險","maps_to":"R5","metric":"S&P／Moody's 長期評級","threshold":"S&P 低於 A，或 Moody's 實際下調","action":"停止加碼","source_freq":"評等機構公告","date":null,"evidence_refs":["customer_concentration_credit#2"]},{"n":10,"text":"證券集體訴訟取得集體認證或出現不利和解","type":"減碼","maps_to":"R2","metric":"明尼蘇達案與 SDNY Faller 案程序進度","threshold":"集體認證通過且和解金額不利","action":"減碼一半","source_freq":"法院文件、10-Q","date":null,"evidence_refs":["lawsuit_class_action#0","major_events#2"]},{"n":11,"text":"PBM 與事前授權監管升級","type":"風險","maps_to":"R5","metric":"FTC 胰島素案結果、事前授權或 AI 拒賠相關立法","threshold":"Optum Rx 被要求改變收費結構，或立法限制 AI 承保決定","action":"停止加碼並重估 Optum Rx 利潤","source_freq":"FTC／國會公告","date":null,"evidence_refs":["regulatory_antitrust#3","substitute_technology#3"]},{"n":12,"text":"第四季財報與 2027 完整指引後複審","type":"複審日期","maps_to":null,"metric":"全份判斷複審","threshold":"日期到期","action":"重跑研究","source_freq":"一次","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"單季合併醫療成本率","bear_threshold":"連 2 季年增 >1pp，或單季 >89.8%","window":"2026Q4–2027Q4 每季","source":"UNH 季報 8-K","last_status":"ok"},{"metric":"2027 調整後 EPS 指引","bear_threshold":"撤回或 <21.5 美元","window":"2026-12 至 2027-12","source":"年底投資人說明會、季報","last_status":"unknown"},{"metric":"DOJ 調查結果","bear_threshold":"公司層級刑事起訴、強制分拆 Optum 或單筆和解 >50 億美元","window":"未來 24 個月","source":"10-Q 法律程序、DOJ 公告","last_status":"ok"},{"metric":"Optum Health 全年營業利益率","bear_threshold":"FY2027 <4%","window":"FY2027","source":"UNH 季報分部資料","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"role":"衛星","row_hit":"9（MA❌例外）","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 FY2 共識 22.61 美元定價，低於管理層暗示的 23.17 美元，且仍把監管尾部折進倍數；若 2027 指引達標、醫療成本率守住，EPS 修復會先於倍數被確認"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=25.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position='早循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"MA=❌ 但 signal≥B 且 val≤🟡 且無 Veto：依「baseline rows 9/9b/10 的 MA 條件字面不含 ❌ 時，該組合不落空、不降觀望——按對應 val 燈 baseline row 裁決，MA❌ 僅作 row4 節奏調節」推論，verdict=進場（row4 pacing 已疊加，見上）"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[],"verdict":"進場","rearm_trigger":"2027 調整後 EPS 指引 ≥23.17 美元，或股價回落至 360 美元以下且醫療成本率未觸發減碼","exec_line":"首倉以目標倉位三分之一建立；2027 指引 ≥23.17 美元再加三分之一；2027 年第一季醫療成本率不高於去年同季再補足；觸發清倉條件即全數出場"},"reasoning":{"industry":"第三季合併營收 1,126.9 億美元（去年同期約 1,132 億）。分部：UnitedHealthcare 863 億美元微降，服務人數 4,830 萬（去年 5,010 萬），主因 Medicare 業務收縮；Optum Rx 399 億美元近乎持平，調整後處方量 3.93 億張；Optum Health 229 億美元年減 10%，營業利益 7.35 億美元（去年 0.41 億）；Optum Insight 55 億美元年增 3%。GAAP 營業利益 65.63 億美元、利益率 5.8%，調整後 5.6%；TTM 毛利率 19.51%、營業利益率 4.82%，對照年度財報 FY2022 營業利益率 8.77%、FY2025 4.24%。產業時鐘在復甦期：2024–2025 年醫療成本衝擊把利潤率壓到谷底，2026 年靠重新定價與退出無利方案回升，第三季醫療成本率 88.4% 低於去年 89.9%，調整後 EPS 4.69 美元。供需持久性：週期性將反轉——使用率仍高，但定價已追上（MA 假設趨勢近 10%、商業險逾 11%），同業稱 2027 年起改善；政府給付缺口則偏結構性（BofA 認為風險池最快 2028 年才穩定），這部分餵進 Bear 機率。議價權：上游醫療提供者靠 No Surprises Act 仲裁拿到 Medicare 的 10–11 倍給付、藥廠專科藥漲價；下游 MA 費率由 CMS 定、Medicaid 由各州定，UNH 對給付方幾乎沒有議價權，只能調整福利與退出市場。單點依賴：第三方估 CMS 約占營收 44%（未經 10-K 原文核實），Medicare & Retirement 2025 年占合併營收約 38%，這是集中度風險，不是護城河證據。","moat":"機制是規模加垂直整合：保險端 4,830 萬人的承保規模，配上 Optum Health 2,000 萬病人（約 400 萬為全責照護）、Optum Rx（外部客戶首度過半、留存率 90% 高段）與 Optum Insight 的理賠與 AI 工具，讓 UNH 在成本管理上比單純保險公司多一層控制。方向證據：MA 份額約 29%→26%、Humana 17%→20%，但這一年 UNH 自己退出約 60 萬人（2026）與約 39 萬人（2027）的方案，屬定價紀律；同期醫療成本率由 89.9% 降到 88.4%、Stars 預期 2027–2028 年近 75% 會員在 4 星以上（產業約 70%）、國家帳戶續約率強。依規則份額下滑不得判擴大，執行力在改善、定價權持平偏弱，合判持平。大客戶有沒有第二來源：UNH 最大的付款方是 CMS、各州與雇主，本次兩條查詢查到的是 Optum 自營化與 PBM 客戶流失，沒有直接回答這三方會不會改找別家，所以這一軸以已知結構判斷。結構上替代來源一直存在：MA 會員每年開放期自選方案，UNH 退出的會員多數流向同業，Humana 份額由 17% 升到 20% 就是付款方改用第二來源的實例；雇主可換承保公司，國家帳戶續約率強說明目前沒有大量轉走；各州 Medicaid 合約的轉換紀錄事實表未涵蓋。結論是 UNH 的護城河不靠綁住客戶，而靠成本管理效率，這也是定價權只給到持平偏弱的原因。同業利潤率差距無法算：事實表同業為製藥與 CDMO，不是管理式醫療。當期 ROIC 無法依公式計算（投入資本未收錄），以利益率判斷屬低利益率靠高周轉的保險結構。四檢查點中社會容忍度判紅燈：事前授權、AI 拒賠、PBM 回扣、MA 編碼都在政治追查中，公司已主動把價格放在經濟上限之下（取消 spread pricing、回扣全數轉嫁、減少 30% 事前授權）。","growth":"成長來源：量為負（UnitedHealthcare 服務人數 4,830 萬，去年 5,010 萬；2027 年 MA 預期再減約 130 萬）、價為正（重新定價、福利縮減）、併購小（Amedisys、Alegeus）、回購約每年 1.3%。三年共識 EPS（Koyfin 2026-10-08 快照，早於第三季財報，家數未載）：FY2026 19.87、FY2027 22.61、FY2028 26.18 美元，FY2026→FY2028 年增約 14.8%；管理層指引今年至少 20.50 美元、2027 至少從 13% 起算（約 23.17 美元）。共識營收 FY1→FY2 僅 +3.4%（yfinance 20／21 位分析師）。缺口：共識 EPS 年增約 14.8% 減內生上界（無法計算、定性偏低）→ 歸因利潤率擴張（營業利益率 4.82% 對 FY2022 8.77%）＋淨回購，可歸因，不依賴倍數重估。跑道：MA 滲透率已逾 30% 門檻多年（逾五成），Optum Health 400 萬全責病人對 2,000 萬服務病人仍有加深空間，Optum Insight 新 AI 產品客戶由 2 家增到 15 家（另 24 家導入中），屬管理層自述、規模尚小，不算已證實的第二曲線。衰退信號亮兩個：核心市占近 12 個月縮減、EPS 成長顯著高於營收成長。","governance":"自由現金流對淨利：年度財報 FY2025 16,075／12,056 百萬美元＝1.33 倍、FY2024 20,705／14,405＝1.44 倍；2026 前九個月自由現金流 22,666 百萬美元，第三季營運現金流為淨利 1.2 倍。股權激勵前九個月 843 百萬美元，年化約占 FY1 共識營收 0.25%。現金去向四分：股息前九個月 62 億美元、全年預期逾 80 億；回購前九個月 50 億美元；資本支出前九個月 24 億美元；降負債（負債資本比 41.7%，年底目標約 40%，淨負債 45,782 百萬美元）；併購以 Amedisys（33 億美元，DOJ 和解後完成）與 Alegeus 為主。回購買入收益率：以今年指引 20.50 美元計盈餘殖利率約 5.1%，10 年期公債殖利率事實表未涵蓋，無法判過不過；併購已實現增量報酬事實表未涵蓋；股權激勵遠小於回購金額，淨稀釋為負。評等壓力（三大評等展望轉負）是回購預算的約束。","valuation":"現價 401.43 美元，以今年指引 20.50 美元計約 19.6 倍、以 FY1 共識 19.87 計 20.2 倍、以 FY2 共識 22.61 計 17.8 倍；共識 FY2026→FY2028 EPS 年增約 14.8%，PEG 約 1.36。年度端點（僅 4 點，非五年序列）本益比分位 44.1、P/S 19.8、EV/S 17.3，營收倍數低是因為利潤率仍在谷底後段。股息殖利率 2.26%。賣方目標均值 443 美元（Benzinga 2026-08-31，第三季前），距現價 +10.4%；第三季後目標價分布未查到。我信 EPS 修復（兩季兌現並上調、FY1 共識三個月上修 7.5%），不信倍數回升：監管尾部與給付缺口仍在，Base 終端倍數用 17 倍而非現值。同業倍數錨：事實表同業為製藥與 CDMO，不可用；管理式醫療同業倍數事實表未涵蓋。","premortem":"管理層迴避紀錄：2026-07-16 法說對 2027 MA 投標假設（Bobby Hunter）、核心使用率 7.5% 假設的追蹤值、Stars 結果都不給數字；2026-10-13 法說 Stephen Hemsley 明說 2027 只能講到這裡，完整指引年底才給。同場 BofA 提問稱追蹤資料顯示年中後趨勢加速，管理層否認，雙方都沒有第三方數據。監管面：DOJ 對 MA 業務的刑事與民事調查、2024 年起的反壟斷調查、證券集體訴訟都無 2026 年進展紀錄，時點不可預測。這兩項是反證紀錄的主軸，價值陷阱評級維持中等。"},"plain":{"six":{"how_it_makes_money":"賺的是保費與醫療支出的差價（第三季醫療成本率 88.4%），加上 Optum 的照護、藥局與軟體服務費；錢卡在政府給付方（CMS、各州）與醫療提供者、藥廠之間的夾層。","moat":"護城河方向持平：規模與 Optum 垂直整合仍在，MA 份額下滑主要是主動退出無利方案；定價權被政府給付與監管容忍度壓住，擴大不了。","growth":"五年後跑道中等：MA 滲透率已逾五成、會員數在縮，未來五年每股盈餘成長靠利潤率修復與回購；Optum Insight 的 AI 產品是可能的第二條曲線，但尚未證實。","capital":"資本配置穩健偏保守：現金轉換率高、股權激勵稀釋低，股息加回購超過淨利；併購報酬與回購門檻因缺資料無法驗證。","valuation":"現價要求 2026 調整後 EPS 20.50 美元站穩、之後五年每年約 10% 成長且倍數守住 17 倍以上；EPS 修復我信，倍數回升我不信，估值合理偏便宜。","how_wrong":"最可能看錯在 2027 年定價：成本趨勢若在第四季與明年初再加速，今年的修復會被一次財測撤回抹掉；其次是監管調查走到刑事或分拆。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":"早循環","cycle_verdict":"右側可追蹤","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2 共識 22.61 美元定價，低於管理層暗示的 23.17 美元，且仍把監管尾部折進倍數；若 2027 指引達標、醫療成本率守住，EPS 修復會先於倍數被確認","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"轉機/特殊情境","price_at_dd":401.43,"week26_return_pct":25.13,"consensus_rev_3m_pct":7.52,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母含第二季 860 百萬美元有利前期準備金調整，CFO 稱不必扣除；若扣除約影響每股 0.7 美元（稅率約兩成三為假設），不改變估值結論，不列爭點。短期上檔＝賣方目標均值 443 美元；中期上檔＝Base FY2028 EPS 25.6 美元×18 倍＝461 美元。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"年底投資人說明會公布 2027 完整指引","impact":"高","watch":"調整後 EPS 是否 ≥23.17 美元、MA 會員與分部利潤率是否給數字"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年開放期 MA 會員結果","impact":"高","watch":"MA 會員淨流失是否超過 150 萬、第四季 Optum Health 虧損幅度"},{"date":"2027-01","date_precision":"month","type":"regulatory","event":"CMS 2028 年 MA 給付預告","impact":"高","watch":"預告費率與編碼變更內容"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"CMS 2028 年 MA 費率定案","impact":"中","watch":"定案費率相對預告的調整幅度"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"2027 年第一季財報","impact":"高","watch":"合併醫療成本率是否不高於 2026 年同季"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s4`：現在 1,467B，下限 1,500B，**目標 ≥ 1,800B**
- `s5`：現在 2,481B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UNH_20261017/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s4 -->
<section id="s4"><h2>4　生意品質與管理層</h2>
<p class="lead">現金轉換率高，管理層兩季兌現財測，但仍迴避 2027 細節。</p>
<ul class="pts">
<li>獲利品質有現金支持。FY2025 自由現金流 16,075 百萬美元，對淨利 12,056 百萬美元約 1.33 倍，FY2024 是 20,705 百萬對 14,405 百萬，約 1.44 倍。2026 前九個月自由現金流已有 22,666 百萬美元。盈餘不是會計堆出來的。</li>
<li>股權激勵稀釋低。前九個月股權激勵 843 百萬美元，年化約占 FY1 共識營收 0.25%，同期回購 50 億美元，淨股數是在減少。這對每股盈餘複利有利。</li>
<li>管理層承諾有兌現。第二季法說給的全年範圍是 19.50–20.00 美元，第三季上調到至少 20.50 美元。Medicaid 利潤率由 −1% 至 −1.7% 改為略優於 −1%，Medicare 利潤率接近 2–4% 區間上緣，兩季都沒有改口。</li>
<li>管理層仍然迴避兩件事。2027 年老人醫療保險的投標假設，以及核心使用率的點估計，第二季法說沒有回答，第三季也只說年底再給。這些正好是 2027 年盈餘最敏感的輸入。</li>
<li>賣方研究與管理層對成本趨勢看法分歧。BofA 在法說上追問，追蹤資料顯示趨勢年中後加速，管理層回答未見加速。雙方都沒有第三方數據，要等 2027 年第一季財報才能分出對錯，暫採公司說法，但不據此加碼。</li>
</ul></section>

```

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期（§5.R／§5.F）</h2>
<p class="lead">護城河方向持平，執行力在改善，定價權被政治壓住。</p>
<ul class="pts">
<li>護城河的機制是規模加垂直整合。保險端 4,830 萬人的承保規模，配上 Optum Health 2,000 萬服務病人（約 400 萬為全責照護）、Optum Rx 與 Optum Insight 的理賠和資料軟體，讓 UNH 在醫療成本管理上比單純的保險公司多一層控制。整體評為 B 級，趨勢持平。</li>
<li>方向證據兩邊拉鋸。老人醫療保險份額由 29% 降到 26%，Humana 由 17% 升到 20%，依規則不得判護城河擴大。但這一年 UNH 自己退出約 60 萬人（2026）與約 39 萬人（2027）的無利方案，屬定價紀律。同期醫療成本率由 89.9% 降到 88.4%，執行力是實際改善。</li>
<li>大客戶沒有綁住。個人會員每年開放期可換方案，UNH 退出方案的會員多數流向同業，Humana 份額上升就是付款方改用第二來源的實例。雇主國家帳戶續約率強，Optum Rx 留存率在 90% 高段，企業端黏著度較高。結論是護城河靠成本管理效率，不靠綁住客戶，這也是定價權只給到持平偏弱的原因。</li>
<li>四個報酬持續期檢查點中，需求基礎值判綠燈，決策層級與價值鏈分配判黃燈，社會容忍度判紅燈。事前授權與 AI 拒賠遭參議員追查，司法部調查老人醫療保險業務，聯邦貿易委員會告藥品福利管理業者胰島素回扣。公司已主動把價格放在經濟上限之下，包括減少 30% 事前授權與回扣全數轉嫁。</li>
<li>威脅清單裡最重的有兩項。第一是司法部自 2024 年起調查 UnitedHealthcare 與 Optum 醫師集團的關係，若走到強制分拆，垂直整合的成本優勢直接消失，機率抓 15%。第二是藥品福利管理業者監管，Optum Rx 已放棄價差定價與回扣留存，立法再收緊會壓縮利潤，機率抓 25%。</li>
<li>同業對照無法做。事實表同業是製藥與委託開發製造業者，例如 Eli Lilly 營業利益率 49.72%、Novo Nordisk 43.13%，它們是 UNH 的成本來源而不是同業。管理式醫療同業的報酬資料事實表未涵蓋，所以不能算報酬差距，也不能用來證明 UNH 優於同業。當期投入資本報酬同樣無法計算，只能以低利益率高周轉的結構判斷。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```