你是 stock-analyst v20 的**散文層（prose）agent**，標的 JNJ（2026-10-18）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JNJ_20261018/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：JNJ　日期：2026-10-18　archetype：None　前份裁決：2026-07-16　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2310B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（433B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1129B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1405B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（737B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（461B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（859B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2031B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4029B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2232B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2310           3283-4690      3 條（2–6 內）  
s3                  8000         433           5297-7567      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3271          8210-11729      5 條（2–6 內）  
s6                 11000         461          7377-10539      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         859           1849-2641      5 條（2–6 內）  
s10                 5000        2031           2078-2969      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2232           2000-2768      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4426B；至少需散文≈40.57KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−54%
−50%
−40%
−40
−38%
−31%
−25
−25%
−4.15%
−3.6%
−3.6
−1.5%
−1%
0
0.06
0.1%
0.5
0.51
0.64
0.7
0.72
0.75
0.8
0.9
1
01
1.06
1.28
1.36
1.5
1.77
1.8%
1.89
2
02
2.07
2.08
2.09
2.1
2.1%
2.5%
2.53
2.59
2.9%
3%
3
3.2
3.5%
3.6%
3.8%
3.9
4
4.0
4%
04
4.42
4.5%
4.8%
5
5%
5.4%
6
06
6%
6.2
6.5
7
7%
07
7.7%
7.9%
8
08
8%
9
9.1%
9.4%
10
10%
10.3%
10.3
10.5%
10.7
10.79
10.8
11%
11
11.04
11.08
11.1%
11.10
11.1
11.2
11.3
11.4
11.6
11.60
11.74
11.75
11.8
12
12%
$12.0
12.0
12.18
12.7
12.9
13
14
14.4
14.8
15
15.1
15.9
16.2
16.3%
16.7
17
17.5
18
19
19.2
20
20%
20.3%
20.4
20.5%
21
21.0%
21%
21.8%
21.8
22
22.9%
23.0%
23
23.07
23.1
24.29
24.3
24.30
25
26
26.8%
27
28
30%
30
$30
30.2%
31
33.0%
33.9%
34%
35%
35.4%
37.3%
38.8
40%
42
43.8
44.3%
45
45.8%
48.4%
49
49.7%
50%
50
55
60%
66%
67.9%
68.2%
70
86
90
95%
100
100%
150%
150
151
168
171
177
193
200
210
$210
215
$215
220
230
232
247.02
253.99
254
255.56
271
283
420
422.4
500
550
690
2010
2021
2025
2026
2027
2028
2029
2030
20261018
1,000
9,000
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
{"meta":{"ticker":"JNJ","date":"2026-10-18","schema":"v15.2","contract":"v19","company_name":"Johnson & Johnson"},"oneliner":"新藥接棒 Stelara 懸崖已有實證（Q3 創新藥營運成長 +7.9%），但醫材連續未達標，2027 年收購稀釋每股 1.36 美元可能還沒進共識；前瞻本益比約 23 倍、基準年化報酬約 6%，等價格回落或 12/8 的 2027 指引。","thesis":{"H":[{"id":"H1","text":"創新藥新品淨接棒：Darzalex、Tremfya、Carvykti、Rybrevant、Caplyta，加上新上市的 ICOTYDE 與 INLEXZO，吸收 Stelara、Simponi、Opsumit 的下滑後，創新藥營運成長維持 +6% 以上。","2y":"FY2026–27 創新藥營運成長 ≥+6%（Q3 2026 為 +7.9%，已含 Stelara −54%）","5y":"2030 年腫瘤銷售超過 500 億美元（管理層目標），創新藥 2026–30 年複合成長 ≥6%","10y":null,"threshold":"創新藥季營運成長 ≥+6%；Tremfya 季成長 ≥+30%（Q3 為 +68.2%）","source":"公司季報新聞稿與法說分品牌成長率（2026-10-13 Ryan Koors）","drift_rule":"季營運成長連 2 季 <+6% 削弱；連 3 季 <+5% 反轉"},{"id":"H2","text":"醫材的國際業務與 Abiomed 在 2027 年回升，醫材營運成長回到 +4% 以上；DePuy Synthes 在 2027 年中前完成分拆（目前傾向分拆上市）。","2y":"Q4 2026 外科轉正；FY2027 醫材營運成長 ≥+4%","5y":"OTTAVA 在 2030 年前成為外科成長支柱；分拆後留存醫材的調整後稅前利益率不低於 22.9%","10y":null,"threshold":"醫材季營運成長 ≥+3%（Q3 2026 為 +2.5%，Q2 為 +3.6%）","source":"公司季報新聞稿；2026-10-13 法說 Tim Schmid 與 Joe Wolk","drift_rule":"連 2 季 <+3% 削弱；連 3 季 <+3% 反轉（Q3 已有一季低於門檻）"},{"id":"H3","text":"法律與定價負債有上限：卵巢 talc 以 55 億美元和解生效（參與率 ≥95%）；證券集體訴訟與反壟斷案不吃掉超過一年自由現金流；MFN 協議成本在利益率指引內吸收。","2y":"卵巢和解生效；2026 年自由現金流約 210 億美元達標，2027 年 ≥200 億美元","5y":"55 億美元以外的 talc 累計新增準備金 ≤100 億美元；2029-01-20 後藥品關稅條件延續","10y":null,"threshold":"單季新增法律準備金 ≤30 億美元（已知和解除外）；全年自由現金流 ≥200 億美元","source":"10-Q 法律附註；2026-10-13 法說 Joe Wolk（和解金額、95% 參與條件、全年自由現金流指引）","drift_rule":"單季新增準備金超過 30 億美元且不是已知和解，連 2 季即削弱；和解失效即反轉"}],"R":[{"id":"R1","text":"醫材持續失速：電生理被脈衝電場消融平台搶份額，Abiomed 回不到成長，國際外科受中國量採與中東拖累。","h_ref":"H2","clock":"⚡","threshold":"Q4 2026 醫材營運成長 <+3%（連同 Q3 即連 2 季）","evidence_refs":["competitive_share_entrants#2","end_markets#1","end_markets#5"]},{"id":"R2","text":"2027 年 EPS 重設：1.36 美元交易稀釋、匯率轉為逆風，加上 Simponi 與 Opsumit 學名藥接續 Stelara 的衰退。","h_ref":"H1","clock":"🔥","threshold":"2027 指引中點 <11.2 美元，或創新藥季營運成長 <+6%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1","substitute_technology#2","end_markets#3"]},{"id":"R3","text":"法律負債擴大：卵巢 talc 和解失效、滑石粉證券集體訴訟走向審判或和解、Stelara 反壟斷案經 FTC 表態後可能復活、Biosense Webster 4.42 億美元判決、比利時品類管理罰款。","h_ref":"H3","clock":"🐢","threshold":"和解參與率 <95%，或單季新增準備金 >30 億美元","evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#0","regulatory_antitrust#2","regulatory_antitrust#3"]},{"id":"R4","text":"定價與關稅：MFN 協議擴大讓利；2029-01-20 零稅率到期；醫材的中國關稅；商務部在地製造協議是否已確認，目前證據不一致。","h_ref":"H3","clock":"🐢","threshold":"季毛利率年減 >200bp，且公司歸因於關稅或定價協議","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#1"]}],"single_thing":{"description":"12/8 企業業務回顧給出的 2027 調整後 EPS 指引中點低於 10.8 美元，即剔除 1.36 美元交易稀釋後，基礎 EPS 成長低於 4%。","why_fatal":"這代表管理層說的「EPS 成長快於營收」不成立，營運槓桿消失；2028–31 年基準路徑整條下移，倍數從 23 倍壓向 17–19 倍，基準年化報酬掉到 3% 以下。","if_happens":"基準情境改用偏 Bear 的路徑，進場價下調至 ≤200 美元，不建倉。","how_monitor":"12/8 企業業務回顧，以及 2027 年 1 月 Q4 季報的指引表。","probability":"約 20%：依 CFO 口徑推算，2027 年約 11.1 美元，落在門檻之上；但匯率逆風與 Simponi 學名藥可能把數字壓到門檻附近。"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.0,"peg_fy2":1.89,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":10.79,"FY2026E":11.08,"FY2027E":12.18,"FY2028E":14.8},"fy_end_month":12,"eps_basis":"調整後 EPS（Non-GAAP，含收購研發費用）。FY2025A 由 2026 指引中點 11.10 與成長 2.9% 回推（Q3 法說 CFO），事實表沒有直接值；共識為 Koyfin 2026-10-08 快照；財年止於 12 月。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JNJ_20261018/scenario.json","archetype":{"primary":"品質複利成長","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"大藥廠加醫材，新藥接棒專利懸崖，股東回饋以股息為主"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：IQVIA 預估全球藥品市場至 2030 年年增約 5–8%；但美國淨價成長降到 4–7%，價格端放緩。","bargaining":{"up":"上游原料與合約製造的占比事實表未涵蓋，議價結構無法量化。","down":"三大批發商約占總毛營收 48.4%；美國政府透過 MFN 協議、TrumpRx 與 Medicaid 國際價格設定價格天花板。","geo":"2025 年關稅成本約 2 億美元，集中在醫材，中國關稅為最大部分；藥品 232 關稅零稅率至 2029-01-20。"},"profit_pool_dir":"利潤池往腫瘤與免疫新藥集中；醫材的國際外科、亞太電生理與 Abiomed 在流出。","tam_table":{"expanded":false,"reason":"成長由個別藥品的份額與適應症驅動，不是低滲透品類的擴張；可引的只有 IQVIA 全球藥品市場增速，分產品滲透率事實表未涵蓋。"}},"moat":{"mechanism":"腫瘤與免疫的臨床證據規模與商業化網路（多發性骨髓瘤約八成病患使用 JNJ 療法）；醫材靠醫院關係與耗材綁定。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"創新藥份額擴大（Darzalex 增加 5 點、Tremfya 增加 4 點，Q3 法說），醫材的電生理與國際外科份額縮減，淨方向持平。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用營業利益率與毛利率對照。","threats":[{"level":"🟡","text":"Stelara 生物相似藥：Q3 −54%，拖累創新藥約 690bp；已進入第二年，殘值在遞減。","p":0.9,"evidence_refs":["competitive_share_entrants#1","substitute_technology#1","substitute_technology#2","end_markets#3"]},{"level":"🟡","text":"Simponi（歐洲生物相似藥已進入，美國可能在 2026 年稍後）與 Opsumit 學名藥。","p":0.8,"evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"level":"🟡","text":"電生理脈衝電場消融競爭，亞太壓力加劇；VARIPULSE Pro 在歐洲已回到雙位數成長，美國第四季才上市。","p":0.5,"evidence_refs":["competitive_share_entrants#2","end_markets#5"]},{"level":"🟡","text":"中國量採擴大，壓縮外科國際業務。","p":0.7,"evidence_refs":["end_markets#5"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"病患、醫師、保險三方都成立；腫瘤與免疫屬於需要而非想要。ICOTYDE 上市不到一年已取得全國商業保險覆蓋，約 60% 病患是首次使用全身性治療（Q3 法說）。"},{"item":"決策層級","level":"🟡","text":"替代發生在醫師處方層，新病人份額一季可移動 4–5 點：Tremfya、Darzalex 是正向例子，Stelara 被生物相似藥與新機轉取代是反向例子。電生理導管同樣在醫師端被換平台，轉換成本比一般印象低。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈中最難取代的是專利期內的分子本身，這部分 JNJ 握有。但三大批發商約占總毛營收 48.4%，美國支付端也透過 MFN 與 Medicaid 國際價格分走一部分利潤。"},{"item":"社會容忍度","level":"🟡","text":"價格上限已由政治決定：2026-01 以 MFN 定價換關稅豁免，零稅率至 2029-01-20。利益率指引已含協議成本、全年仍上調，顯示目前可吸收；2029 年到期後的條件未明，已列入反證紀錄。"}],"roiic":"事實表未涵蓋（投入資本與近三年併購對價未收錄）","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，再投資率＝（資本支出−折舊攤銷＋營運資金變動＋收購淨額）÷稅後營業利益；兩項輸入缺失，不推估。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","JNJ":67.91,"MRK":72.97,"LLY":83.4,"ABBV":71.48,"BSX":69.92,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","JNJ":26.81,"MRK":10.49,"LLY":49.72,"ABBV":33.94,"BSX":21.0,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","JNJ":22.7,"MRK":24.13,"LLY":17.02,"ABBV":28.28,"BSX":8.6,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","JNJ":15.42,"MRK":45.75,"LLY":18.32,"ABBV":15.09,"BSX":10.25,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"MRK","gm":72.97,"om":10.49,"fcf_margin":24.13,"rd_intensity":45.75,"strategy_note":"營業利益率 10.5%、研發密度 45.8%，顯示近期重押研發或收購費用，不是可比的利潤標竿。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"LLY","gm":83.4,"om":49.72,"fcf_margin":17.02,"rd_intensity":18.32,"strategy_note":"營業利益率 49.7%，靠單一大類高價新藥；JNJ 組合較分散，但定價力不在頂層。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ABBV","gm":71.48,"om":33.94,"fcf_margin":28.28,"rd_intensity":15.09,"strategy_note":"營業利益率 33.9%，同樣走過生物相似藥懸崖，可對照 JNJ 接棒 Stelara 的速度。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BSX","gm":69.92,"om":21.0,"fcf_margin":8.6,"rd_intensity":10.25,"strategy_note":"電生理脈衝電場消融的直接對手。營業利益率 21.0% 低於 JNJ，但在電生理份額上施壓。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（新藥份額）、併購補位（Firefly、Sail），價格為負向，回購趨近於零。","runway_years":"事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC × 再投資率；投入資本與近三年併購對價事實表未涵蓋，上界無法計算，保守視為共識成長已超出內生上界。","segments":[{"item":"創新藥（Q3 2026）","value":"營收 168 億美元，營運成長 +7.9%（美國 +11.1%），調整後稅前利益率 35.4%（去年 44.3%，含約 10 億美元收購研發費用）"},{"item":"醫材（Q3 2026）","value":"營收 86 億美元，營運成長 +2.5%（美國 +4.8%、美國以外 +0.1%），調整後稅前利益率 22.9%（去年 21.0%，含關稅追回）"}],"decay_signals":["毛利率：Q3 銷貨成本率年增 150bp（產品組合與 Intra-Cellular 無形資產攤銷）；Q2 是否同向事實表未涵蓋，暫記一項","核心市占：電生理受脈衝電場消融競爭，亞太壓力加劇（Q3 法說）"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"管理層明說本十年末雙位數成長不假設併購（Q3 法說 CFO 回答 Goldman 提問），成長主要靠內部新藥；近三年現金去向四分事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Firefly 收購約 10 億美元收購研發費用、Sail 合作；2027 年合計稀釋每股 1.36 美元，已實現增量報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"股東回饋以股息為主（Q2 法說 CFO），近年無實質回購","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"淨利÷稀釋 EPS 推得稀釋股數 FY2024 約 24.29 億、FY2025 約 24.30 億，年淨稀釋趨近於零","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2026 共識調整後 EPS）搭配 PEG","tier":"大型多元藥廠","peers":{"expanded":false,"reason":"同業前瞻本益比事實表未涵蓋，只有利潤率可對照，不跨口徑當錨。"},"fwd_pe":23.1,"peg":2.08,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 23.1 倍（剔除交易 21.8 倍）、PEG 約 2.1；P/E、P/S、EV/S 皆在近 4 個年度端點的最高位（非五年分位）；基準年化約 6%，低於 8%。判為偏貴。","upside_short_pct":-3.6,"upside_mid_pct":20.4},"trap_analysis":{"verdict":"🟡","label":"兩項衰退信號（毛利率、電生理份額），尚非價值陷阱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Simponi 歐洲生物相似藥已進入，美國可能在 2026 年稍後；Opsumit 學名藥；Stelara 衰退快於公司原預期，且三星 Bioepis 第二個生物相似藥阻擋上訴敗訴；IQVIA 預估美國淨價年增 4–7%，低於過去五年的 9.4%。","assumption":"新品接棒的速度，能持續蓋過每一輪專利到期與淨價放緩。","consequence":"EPS 五年停在 11–12 美元、倍數壓到 15 倍，股價約 177 美元（−31%）；再疊加 talc 失控，才會到 −50%。","ruling":"部分採納。Q3 創新藥在 Stelara −54% 下仍成長 +7.9%，接棒已有實證，所以不升為主情境；Bear 機率維持 30%。","watch":"創新藥季營運成長是否連 2 季低於 +6%。","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1","substitute_technology#2","end_markets#3"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"Q3 醫材營運 +2.5%，低於管理層預期；Abiomed −1.5%，外科 −1%；電生理亞太競爭加劇；中東成為新增逆風。Q2 法說曾說 Abiomed 會在未來數季逐步回到雙位數。","assumption":"醫材疲弱屬於暫時性，2027 年可回到 4% 以上。","consequence":"醫材若停在 2–3%，DePuy Synthes 分拆後的留存組合難以支撐倍數，H2 失效。","ruling":"不採信也不否定：標為未證、監測，以兩季期限檢驗。","watch":"Q4 2026 與 Q1 2027 醫材營運成長是否皆低於 +3%。","evidence_refs":["competitive_share_entrants#2","end_markets#1","end_markets#5"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"成長靠收購補位：Firefly 約 10 億美元收購研發費用，2027 年交易稀釋每股 1.36 美元；卵巢 talc 和解 55 億美元，滑石粉證券集體訴訟已確立集體認證；Biosense Webster 反壟斷判決 4.42 億美元、比利時品類管理罰款；美國價格天花板由 MFN、TrumpRx 與 Medicaid 國際價格決定；三大批發商約占總毛營收 48.4%。","assumption":"營收成長能轉成每股自由現金流成長。","consequence":"營收達到雙位數，但 EPS 被併購稀釋、訴訟支出與定價讓利吃掉，每股價值成長停在中個位數。","ruling":"採納。長期信心上限為中，進場價以 2027 年稀釋後 EPS 計算。","watch":"12/8 的 2027 指引與 2028 年交易稀釋是否收斂；批發商合計占比是否超過 50%；2029-01-20 關稅零稅率到期前的協議延續。","evidence_refs":["customer_concentration_credit#0","major_events#1","lawsuit_class_action#0","regulatory_antitrust#2","regulatory_antitrust#3"],"fact_refs":["f_kpi3_fcf"]},{"view":"價格已反映太多","evidence":"前瞻本益比約 23 倍；P/E、P/S、EV/S 皆在近 4 個年度端點的最高位；二手聚合平均目標價 254–271 美元，與現價 255.56 相當；FY2027 共識 12.18 美元可能未完整反映 1.36 美元稀釋。","assumption":"市場以共識 FY2028 的 14.8 美元定價。","consequence":"共識下修約 8% 時，倍數不變也有約 8% 下行；基準年化報酬約 6%，低於 8%。","ruling":"採納。不追，等價格回落或 2027 指引。","watch":"12/8 之後共識 FY2027 EPS 的修正幅度。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_ps_percentile","f_consensus_eps_fy2"]}],"max_dd":{"lo":-40,"hi":-25,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 247.02 → 本次 255.56（+3.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=247.02","side_b":"本次 price_at_dd=255.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 247.02 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 247.02 美元：Bull 價 420、Bear 價 210，五年期望值 +33.0%，基準年化 7.7%，不對稱比 3.9","side_b":"本次情境、股價仍用 247.02 美元：Bull 價 422.4、Bear 價 177，五年期望值 +20.3%，基準年化 4.5%，不對稱比 2.09","ruling":"先換情境、股價不動：五年期望值少 12.7 個百分點，基準年化少 3.2 個百分點。不對稱比由 3.9 變為 2.09。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 247.02 美元：五年期望值 +20.3%，基準年化 4.5%，不對稱比 2.09","side_b":"本次情境、股價 255.56 美元：五年期望值 +16.3%，基準年化 3.8%，不對稱比 1.77","ruling":"再換股價、情境不動：起點價上漲 3.5%，五年期望值少 4.0 個百分點，基準年化少 0.7 個百分點，不對稱比由 2.09 降到 1.77。合計五年期望值比前份少 16.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2027 EPS：共識與管理層口徑","cause":"新證據","prior_field":null,"side_a":"共識 FY2027 EPS 12.18 美元（Koyfin 10-08 快照，早於 Q3 法說）。","side_b":"Q3 法說 CFO：2027 年 Firefly／Sail 合計稀釋每股 1.36 美元，剔除後 EPS 成長略快於營收（約 5.4%）；以剔除交易的 2026 基礎 11.74 × 約 1.06 − 1.36，推得約 11.1 美元。","ruling":"採管理層口徑，基準路徑 2027 年取 11.2 美元。兩邊方向一致、幅度不同，屬可調和；但共識可能要下修約 8%，是短期價格風險。","evidence_level":"一手法說原話加共識快照","settle_metric":"12/8 企業業務回顧的 2027 調整後 EPS 指引中點","if_then":["若指引中點 ≥12.0 美元，基準路徑上修，進場價上調至約 230 美元並重跑判斷","若指引中點 <10.8 美元，觸發唯一致命點，進場價下調至 ≤200 美元，不建倉"],"evidence_refs":[]},{"axis":"全年 EPS 指引前後數字","cause":"新證據","prior_field":null,"side_a":"二手整理稱 7 月指引為調整後 EPS 11.60–11.75 美元。","side_b":"Q3 新聞稿指引中點 11.10 美元。","ruling":"可調和。Q2 法說 CFO 明說 7/15 指引不含 Firefly 等待完成的交易；扣 0.64 美元稀釋後中點約 11.04，Q3 再上調 0.06 至 11.10，前後一致。FY1 共識近 3 個月 −4.15% 同屬這筆稀釋，不是基本面下修。","evidence_level":"一手法說原話","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"醫材：暫時性歸因與連續未達標","cause":"新證據","prior_field":null,"side_a":"管理層說法：Abiomed 屬短期逆風、非結構性，2026-07-15 Tim Schmid 稱未來數季逐步回到雙位數；外科第四季整體回到成長；手術量環境穩定。","side_b":"Q3 醫材營運 +2.5%，低於管理層自己的預期；Abiomed −1.5%，外科 −1%，電生理亞太競爭加劇；Q2 承諾今年兩項機器人上市，Q3 只見 OTTAVA，泌尿系統未提。","ruling":"不採信也不否定，標為未證、監測。預先登記期限：Q4 2026 與 Q1 2027 醫材營運成長皆低於 +3%，即視為暫時性歸因證偽，H2 反轉。","evidence_level":"一手季報加法說","settle_metric":"醫材季營運成長、Abiomed 季成長","if_then":["若 Q4 2026 外科轉正且醫材 ≥+4%，H2 恢復，進場價不變","若連 2 季低於 +3%，H2 反轉，醫材不再給溢價，Bear 機率上調至 35%"],"evidence_refs":["end_markets#1","competitive_share_entrants#2","end_markets#5"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"Q3 調整後 EPS 2.59 美元優於共識 2.53；全年指引上調；AAA 評等；股息殖利率約 2.1%；新品曲線多條（ICOTYDE、INLEXZO、Rybrevant、OTTAVA）；管理層說 2027 年會更好；動能不過熱。","side_b":"好生意已經反映在價格上：前瞻本益比約 23 倍，基準年化約 6%，2027 年 EPS 還有共識下修風險。","ruling":"不採。等價格回到 215 美元，或等 2027 指引確認共識不需下修。","evidence_level":"一手季報加共識","settle_metric":"股價與 2027 指引","if_then":["若股價 ≤215 美元且醫材未證偽，建首批三分之一","若價格先漲而指引未到，不追"],"evidence_refs":[]},{"axis":"前份漂移：價格與估值相關欄","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct","cycle_position"],"side_a":"前份股價 247.02 美元，估值偏貴，訊號 B，觀望；機率 25／45／30，最大回撤 −38%，非循環股。","side_b":"現價 255.56 美元（+3.5%），前瞻本益比約 23 倍，估值仍偏貴，訊號 B，觀望；機率維持 25／45／30，最大回撤改為 −25% 至 −40% 的範圍，仍非循環股。","ruling":"股價小漲 3.5% 未改變估值結論；回撤由單點改為範圍是表達方式的調整，下緣由 Bear 終點 −31% 推出。","evidence_level":"收盤價","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：護城河、跑道、類型與陷阱","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","trap"],"side_a":"前份：護城河持平、五年後跑道中等、品質複利成長、價值陷阱風險低。","side_b":"本次：護城河持平、跑道中等、類型不變；價值陷阱風險由低升為中，因為出現兩項衰退信號——Q3 銷貨成本率年增 150bp，電生理份額受脈衝電場消融競爭。","ruling":"Q3 新證據兩面都有：創新藥份額擴大、醫材份額流失，方向相抵，所以護城河與跑道不變；陷阱風險依兩項信號上調一級。","evidence_level":"一手季報加法說","settle_metric":"季毛利率年變化、電生理成長率","if_then":["若 Q4 毛利率年減幅收斂至 50bp 內且電生理恢復雙位數，陷阱風險回降"],"evidence_refs":["competitive_share_entrants#2","end_markets#5"]},{"axis":"進場條件改變（加碼與首批建倉門檻）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE 回落 ≤18x（約 $210-220）或 PEG ≤2；或 talc 全球和解定案 ≤$30B；或 Section 232 藥品關稅豁免正式確認","side_b":"股價≤$215（2027基準EPS的19倍）或12/8給出2027調整後EPS指引中點≥$12.0","ruling":"舊條件中的關稅豁免已在 2026-01-08 協議落定（零稅率至 2029-01-20），卵巢 talc 已以 55 億美元和解並計提，兩項事件條件失效。價格門檻改以 2027 稀釋後 EPS 為分母，金額與前份相近；新增指引條件，因為 2027 共識是本次的主要約束。","evidence_level":"一手新聞稿加法說","settle_metric":"股價、2027 指引","if_then":["若股價 ≤215 美元，建首批三分之一，Q4 醫材 ≥+3% 再加碼","若指引中點 ≥12.0 美元，重跑判斷後再決定是否進場"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"新證據","prior_field":null,"side_a":"前份未設定唯一致命點。","side_b":"Single Thing：12/8 給出的 2027 調整後 EPS 指引中點低於 10.8 美元，代表剔除交易後的基礎 EPS 成長低於 4%。","ruling":"本次 EPS 路徑是估值最大的單一敏感項，而 2027 指引是第一個能一次定案的離散事件，因此設為唯一致命點；觸發即不建倉。","evidence_level":"一手法說原話","settle_metric":"2027 調整後 EPS 指引中點","if_then":["若觸發，不建倉，進場價下調至 ≤200 美元"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"新證據","prior_field":null,"side_a":"前份未設指標門檻。","side_b":"本次設四條：醫材季營運成長連 2 季低於 +3%；創新藥季營運成長連 2 季低於 +6%；2027 指引中點低於 10.8 美元；卵巢 talc 和解參與率低於 95% 或單季新增準備金超過 30 億美元。觸發時的動作為減碼或不建倉。","ruling":"前份只有文字警戒閾值，本次改為可逐季核對的數字，便於減碼與清倉判斷。","evidence_level":"一手季報","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份風險門檻的處置","cause":"新證據","prior_field":null,"side_a":"前份 R1：Section 232 豁免未於生效日前定案，即作減碼考量。前份 R3：準備金連 2 季新增超過 30 億美元。","side_b":"本次：232 風險降為 2029-01-20 到期風險，併入新 R4，門檻為毛利率年減超過 200bp 且公司歸因於關稅或定價協議時減碼。R3 改看卵巢和解參與率 ≥95%；Q3 單季計提 55 億美元屬和解定額，只有一季，不構成失控訊號。","ruling":"保留指標、門檻與資料來源，不安靜刪除。仍有一處未釐清：顧問報告稱截至 2026 年 6 月 JNJ 未確認商務部在地製造協議，與 1 月協議的關係不明，列入 R4 監測。","evidence_level":"一手新聞稿加二手顧問報告","settle_metric":"10-Q 法律附註、季毛利率","if_then":["若 2029-01-20 前未取得延續條件，R4 提前為中期風險"],"evidence_refs":["reg_tariff_export#2"]}],"triggers":[{"n":1,"text":"創新藥營運成長是否守住 6%","type":"假設驗證","maps_to":"H1","metric":"創新藥季營運成長","threshold":"連 2 季 <+6%","action":"延後進場；若已持有，減碼三分之一","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":["end_markets#3"]},{"n":2,"text":"醫材是否回升","type":"假設驗證","maps_to":"H2","metric":"醫材季營運成長","threshold":"Q4 2026 與 Q1 2027 皆 <+3%","action":"H2 反轉，Bear 機率上調至 35%，不建倉","source_freq":"季報新聞稿／每季","date":"2027-04","evidence_refs":["end_markets#1","competitive_share_entrants#2"]},{"n":3,"text":"2027 指引是否跌破剔除交易後的成長下限","type":"Single Thing","maps_to":"H1","metric":"2027 調整後 EPS 指引中點","threshold":"<10.8 美元","action":"不建倉，進場價下調至 ≤200 美元","source_freq":"企業業務回顧／一次性","date":"2026-12-08","evidence_refs":[]},{"n":4,"text":"卵巢 talc 和解是否生效、有無新增準備金","type":"風險","maps_to":"R3","metric":"和解參與率；10-Q 新增法律準備金","threshold":"參與率 <95% 致和解失效，或單季新增準備金 >30 億美元（不含已計提的 55 億）","action":"已持有則減碼至半倉；未持有則進場價下調 10%","source_freq":"10-Q／每季","date":"2027-01","evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":5,"text":"反壟斷案是否復活","type":"風險","maps_to":"R3","metric":"第四巡迴法院 CareFirst 上訴裁定；Biosense Webster 4.42 億美元判決後續","threshold":"上訴法院發回重審 Stelara 壟斷案","action":"停止加碼，直到案情金額可量化","source_freq":"法院裁定／不定期","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","regulatory_antitrust#3"]},{"n":6,"text":"定價協議與關稅是否吸收失敗","type":"風險","maps_to":"R4","metric":"季毛利率年變化","threshold":"年減 >200bp，且公司歸因於關稅或定價協議","action":"減碼三分之一","source_freq":"季報／每季","date":null,"evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#1"]},{"n":7,"text":"價格回到合理區","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤215 美元","action":"建首批三分之一","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":8,"text":"通路集中度","type":"風險","maps_to":"R4","metric":"三大批發商占總毛營收","threshold":">50%","action":"定價力子分下調一分","source_freq":"10-K／每年","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":9,"text":"Q4 季報後複審","type":"複審日期","maps_to":"H2","metric":"醫材與創新藥營運成長、2027 指引","threshold":"季報公布","action":"重跑判斷","source_freq":"季報","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"醫材季營運成長","bear_threshold":"連 2 季 <+3%","window":"2026Q4–2027Q1","source":"公司季報新聞稿","last_status":"warning"},{"metric":"創新藥季營運成長（含 Stelara 拖累）","bear_threshold":"連 2 季 <+6%","window":"未來 4 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"2027 調整後 EPS 指引中點","bear_threshold":"<10.8 美元","window":"2026-12-08","source":"企業業務回顧","last_status":"unknown"},{"metric":"卵巢 talc 和解參與率與新增法律準備金","bear_threshold":"參與率 <95%，或單季新增 >30 億美元","window":"未來 6 季","source":"10-Q 法律附註與法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"證據本身標明是 2010 年工廠停工與 2021 年合約廠疫苗報廢兩件舊事件，並自註「非現況集中度證據」；沒有提供現行製造據點或單一廠營收占比，無法形成可監測的門檻。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=10.3, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價≤$215（2027基準EPS的19倍）或12/8給出2027調整後EPS指引中點≥$12.0","exec_line":"現價不建倉。觸及 215 美元先建三分之一；Q4 2026 季報醫材營運成長 ≥+3% 再加碼第二批；唯一致命點觸發則取消。"},"reasoning":{"industry":"Q3 2026 營收 253.99 億美元。創新藥 168 億美元，約占 66%，營運成長 +7.9%；醫材 86 億美元，約占 34%，營運成長 +2.5%（Q3 法說 Ryan Koors）。獲利集中在創新藥：調整後稅前利益率創新藥 35.4%（去年同期 44.3%，差距主因約 10 億美元 Firefly 收購研發費用），醫材 22.9%。全公司調整後稅前利益率 30.2%，自算 GAAP 營業利益率 23.0%；TTM 毛利率 67.9%、營業利益率 26.8%。第一個卡點是美國支付端：2026-01 以 MFN 定價換取藥品關稅豁免，利益率指引已含這份協議的成本。第二個卡點是通路：三大批發商約占總毛營收 48.4%（FY2025 10-K），最大一家由 20.5% 升至 21.8%，三家合計與前一年同為約 48.4%。單點依賴方面，前兩大合計 37.3%，未達 40%，且批發商只是配送方、不是最終需求方，所以列為集中度風險而非護城河證據。供需耐久度判為結構性持久，但價格端在放緩：IQVIA 預估全球藥品市場至 2030 年年增約 5–8%，美國淨價年增 4–7%，低於過去五年的 9.4%。產業態勢是雙向拉鋸：競爭端在惡化（電生理脈衝電場消融、Stelara 與 Simponi 生物相似藥），結構端在轉好（藥品關稅零稅率至 2029-01-20、美國本土 550 億美元投資計畫）。","moat":"機制是腫瘤與免疫的臨床證據加上商業化規模。多發性骨髓瘤約八成病患在療程中用到 JNJ 療法；Darzalex 各線份額增加 5 點，一線增加 10 點；Tremfya 在 UC 與克隆氏症份額各增加 4 點，美國 IL-23 新病人份額居首（Q3 法說）。醫材方向相反：電生理受脈衝電場消融競爭，亞太壓力加劇；Abiomed −1.5%，外科 −1%（中國量採、中東）。同業只有利潤率可比：JNJ TTM 營業利益率 26.8%，低於 ABBV 33.9% 與 LLY 49.7%，高於 BSX 21.0% 與 MRK 10.5%。同業 ROIC 差距事實表未涵蓋，因此綜合分不給到 8 以上。執行力給 8 分：全年指引連續上調，八個品牌雙位數成長。定價力給 7 分：美國以外 Darzalex 有價格逆風，MFN 協議生效，美國淨價成長放緩。報酬持續期方面，投入資本事實表未涵蓋，只能依高營業利益率與大量併購無形資產判為高利益率、低周轉；增量報酬算不出。","growth":"成長以量為主，來自新藥份額與新適應症；併購補位，包括 Firefly 收購與 Sail 合作，2026 年稀釋每股 0.64 美元、2027 年稀釋 1.36 美元；價格為負向（美國以外定價逆風、MFN）；回購幾乎沒有。共識三年 EPS：FY2025A 調整後約 10.79 美元（由 2026 指引中點 11.10 與成長 2.9% 回推），到 FY2028E 14.8 美元，年複合約 11.1%（Koyfin 快照，分析師家數事實表未涵蓋）。內生上界算不出，因為投入資本與併購對價事實表未涵蓋。缺口歸因：約 2 個百分點來自 2026 年一次性交易費用的基期效應，其餘依賴併購資產放量與管理層「本十年末雙位數成長」的承諾，無法用內生數字驗證，長期信心上限為中。第二條曲線有出處：ICOTYDE 上市以來 2 萬名病患、近 9,000 名處方醫師；INLEXZO 年初至今約 2 億美元，平台目標 50 億美元以上；OTTAVA 7 月取得 De Novo 授權。但 Simponi 與 Opsumit 的到期已開始，Stelara 式懸崖會再來，因此跑道判中等。","governance":"自由現金流穩定：FY2022–25 介於 171–193 億美元，FCF 利潤率約 20–21%。淨利因訴訟與一次性項目波動大，FCF 除以淨利 FY2023 為 0.51、FY2024 為 1.28、FY2025 為 0.72，未出現連 2 年低於 0.75。2026 年前三季自由現金流約 151 億美元，全年指引約 210 億美元（Q3 法說 CFO）。淨負債約 283 億美元，S&P 維持 AAA。現金去向：股息為主（Q2 法說 CFO），卵巢 talc 和解 55 億美元，Firefly 收購約 10 億美元；四分比例事實表未涵蓋。計分逐項看：併購回報 Firefly 與 Sail 尚未產生營收，已實現回報算不出；回購不適用；稀釋方面，以年度淨利除以稀釋 EPS 推得 FY2024 與 FY2025 稀釋股數皆約 24.3 億股，近乎零淨稀釋，通過。股權報酬費用占營收比事實表未涵蓋。","valuation":"現價 255.56 美元，以 FY2026 共識 EPS 11.08 計，前瞻本益比約 23.1 倍；剔除 0.64 美元交易稀釋後的 11.74 計，約 21.8 倍。PEG 以共識三年年複合約 11.1% 計約 2.1，偏貴。trailing P/E 38.8 倍、P/S 6.2 倍、EV/S 6.5 倍，皆在近 4 個年度端點的最高位；這不是五年分位，GAAP 本益比也被 talc 計提壓低分母，只作方向參考。FY2027 共識 12.18 美元很可能沒有完整反映 1.36 美元稀釋：依 CFO 說法，剔除交易後 EPS 成長略快於營收（約 5.4%），以 11.74 × 約 1.06 − 1.36 推得約 11.1 美元。FY1 共識近 3 個月 −4.15%，是 7 月納入交易稀釋所致，不是基本面下修。二手聚合平均目標價 254 與 271 美元，與現價相當；全距事實表未涵蓋。短期上檔以 2027 基準 EPS 11.2 × 22 倍計約 −3.6%，中期以五年基準終值計約 +20%。","premortem":"動能不過熱：RSI(14) 43.8，26 週報酬 +10.3%，不構成追價障礙，也不構成撿便宜訊號。看錯的方式有三種。第一，醫材的暫時性歸因如果成立（VARIPULSE Pro 歐洲已回到雙位數，美國第四季上市；Abiomed 美國端季內改善），2027 年醫材回到 4% 以上，H2 恢復。第二，12/8 若給出不含 1.36 美元稀釋疑慮的 2027 指引，共識不下修，基準路徑偏保守。第三，反方向風險：卵巢 talc 和解需 95% 參與率才生效（CFO 稱正趨向達標），證券集體訴訟已確立集體認證；Stelara 反壟斷案若被第四巡迴法院發回，屬於新的負債來源。歷史最大回撤與訴訟總金額事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺醫師處方與醫院採購的錢，獲利集中在腫瘤與免疫新藥。錢卡在兩個節點：美國支付端的定價協議，以及三大批發商通路。","moat":"護城河方向持平：創新藥份額在擴大，醫材份額在流失，兩者相抵。","growth":"五年後的跑道中等。有出處的第二條曲線存在，但放在 1,000 億美元營收的規模上，單一新品都不到一成，專利懸崖會反覆出現。","capital":"資本配置中等。自由現金流足以支付股息、和解與小型併購，但併購回報無法驗證，回購幾乎沒有。","valuation":"現價要求 2027–28 年 EPS 照共識走（年增約 11%），且倍數守在 21 倍以上。這只能信一半：2027 年被交易稀釋壓住，基準情境年化約 6%，不夠。","how_wrong":"最可能看錯在醫材與 2027 指引：Q4 外科與 Abiomed 若真的回升、12/8 給出高於共識的 2027 指引，觀望會錯過；反方向的風險是 talc 和解失效與定價協議到期。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤215 美元（約 2027 基準 EPS 11.2 的 19 倍），或 12/8 給出 2027 調整後 EPS 指引中點 ≥12.0 美元","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":255.56,"week26_return_pct":10.3,"consensus_rev_3m_pct":-4.15,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 EPS 含 Firefly／Sail 一次性稀釋 0.64 美元，剔除後前瞻本益比約 21.8 倍；分母差距不改變偏貴結論。真正的分母爭點在 FY2027 共識是否已扣 1.36 美元，已放進情境路徑。"},"catalysts":[{"date":"2026-12-08","date_precision":null,"type":"guidance","event":"企業業務回顧：2027 展望、DePuy Synthes 分拆的模擬財務、早期管線","impact":"高","watch":"2027 調整後 EPS 指引中點與 1.36 美元稀釋的處理方式"},{"date":"2026-12-31","date_precision":"quarter","type":"regulatory","event":"VARIPULSE Pro 美國核准與上市；RYBREVANT FASPRO 頭頸癌美國核准","impact":"中","watch":"電生理份額能否止跌"},{"date":"2026-12-31","date_precision":"quarter","type":"product","event":"milvexian 次發性中風試驗讀數（事件驅動，可能落在今年）；ICOTYDE 乾癬性關節炎資料與對 Stelara 頭對頭資料","impact":"中","watch":"Factor XI 第二條曲線是否成立"},{"date":"2027-01-31","date_precision":"month","type":"guidance","event":"Q4 2026 季報","impact":"高","watch":"醫材營運成長是否 ≥+3%、外科是否轉正"},{"date":"2027-06-30","date_precision":"quarter","type":"other","event":"DePuy Synthes 分拆完成（目標 2027 年中）","impact":"中","watch":"分拆方式與留存醫材利益率"}],"_projected_from":"v19"}
```
