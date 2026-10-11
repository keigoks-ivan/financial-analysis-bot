你是 stock-analyst v20 的**散文層（prose）agent**，標的 6805.TW（2026-10-11）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6805.TW_20261011/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：6805.TW　日期：2026-10-11　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1561B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（700B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1144B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1434B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（918B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（437B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（748B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2151B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4244B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2058B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1561           3807-5439      5 條（2–6 內）  
s3                  8000         700           5110-7300      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3496          8053-11504      5 條（2–6 內）  
s6                 11000         437          7394-10563      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         748           1926-2752      5 條（2–6 內）  
s10                 5000        2151           1994-2849      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2058           2000-2942      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4894B；至少需散文≈40.11KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−72
−72%
−70%
−65%
−48%
−45%
−45
−26%
−25%
0%
0
0.22
0.35
0.4
0.5%
0.5
0.527%
0.53
0.7
0.70
0.75
0.77
1
1.6%
1.62
1.74
1.8
1.84
2
03
3%
3
3.9
4
4.7
5%
5
5.6%
5.64
6
06
7
07
08
8
8.49
8.57
8.9%
09
9
9.4
9.7
9.7%
9.93
10
10%
10.51
10.61%
11%
11
11.4%
11.4
12
12.27
12.37
12.39
13
13%
14
15%
15
15.62
15.84
16.42
17.89
19.2%
20%
20
20.23%
21.25
22%
22
22.08
24
24.27%
25%
25
25.6%
26
26.34%
27.82%
28
28%
29.71
29.71%
30
30%
30.1
30.38%
30.98
33%
34%
34.05%
34.6
35
35%
35.8
36%
36
37%
37.40
38%
42
44.1
45%
45
46.72
48.72
49
50
50%
50.7
50.7%
50.73
51.62%
52
54.49
55.7%
56
58
60
62.64%
66
66.17
66.52
69
70
70%
71%
73%
77%
79.24
85%
90
100
100%
106
109%
112
114
120
138
150%
158
172
173
250
300
680
730
780
900
2022
2023
2024
2025
2026
2027
2028
2029
2030
2370.0
3017
3324
3653
6805
8996
20261011
1,220
1,308
1,700
1,717
1,750
1,830
2,370
2,391
2,440
2,594
2,600
2,640
3,817
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
{"meta":{"ticker":"6805.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"富世達"},"oneliner":"富世達把鉸鏈工藝移植到 AI 伺服器滑軌與液冷快接頭，上半年伺服器已占營收 55.7%，2027 年產能倍增；但現價為 trailing 本益比 50.73 倍、約 FY2026 共識 EPS 的 36 倍，已貼近賣方平均目標價，Base 五年報酬約一成，等回落再談。","thesis":{"H":[{"id":"H1","text":"AI 伺服器滑軌與液冷快接頭撐起 2026 下半年：營收與毛利率高於上半年，全年 EPS 接近共識。","2y":"2026 下半年營收高於上半年 79.24 億元，全年 EPS≥60 元","5y":null,"10y":null,"threshold":"下半年營收＞79.24 億元；第三、四季毛利率≥33%；FY2026 EPS≥60 元（共識 66.17 元）","source":"公司季報與法說；FactSet 共識","drift_rule":"以 TTM 營收與毛利率對 Base 路徑的偏離計：連 2 季偏離≥5% 視為削弱，連 3 季≥10% 視為反轉。"},{"id":"H2","text":"2027 年產能倍增能轉成營收：AWS 自 2027 第一季增溫，驗證中的 ASIC 客戶至少一家量產。","2y":"2027 年營收年增≥30%，伺服器占比≥70%","5y":null,"10y":null,"threshold":"2027 年營收年增≥30%；伺服器占比≥70%；2027 年底前 AWS 以外至少一家 ASIC 客戶量產","source":"月營收、法說營收結構與客戶驗證進度","drift_rule":"連 2 季營收偏離 Base 路徑≥5% 視為削弱，連 3 季≥10% 視為反轉。"},{"id":"H3","text":"同業擴產後毛利率仍守在 30% 以上，代表賺到的是工藝與認證，不只是供給吃緊。","2y":null,"5y":"2027–2030 年度毛利率≥30%、營業利益率≥22%","10y":null,"threshold":"年度毛利率≥30%（TTM 30.38%）；營業利益率≥22%（TTM 24.27%）","source":"年報與季報","drift_rule":"連 4 季偏離門檻≥5% 視為削弱，連 6 季≥10% 視為反轉。"}],"R":[{"id":"R1","text":"新專案量產遞延：第三季起投產的 NVIDIA／ASIC 滑軌專案延後，下半年轉強落空。","h_ref":"H1","clock":"⚡","threshold":"第三季營收季增＜10% 或毛利率＜33%","evidence_refs":["end_markets#2"]},{"id":"R2","text":"折疊機鉸鏈份額持續流失：華為 Pure S 未承接、蘋果鉸鏈名單未列，加上大和點名的主要客戶市占率與折疊機滲透率不如預期。","h_ref":"H1","clock":"🔥","threshold":"折疊機營收連 2 季年減≥25%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","channel_business_model_shift#2"]},{"id":"R3","text":"2028 年起雲端資本支出消化，滑軌與快接頭同業同步倍增產能，報價與毛利率下行。","h_ref":"H3","clock":"🐢","threshold":"年度毛利率＜28%，或月營收年增轉負連 3 個月","evidence_refs":["supply_demand_durability#3","competitive_share_entrants#3"]},{"id":"R4","text":"集中度只是換了對象：由陸系折疊機品牌（2025 年鉸鏈占營收約 85%）換成 AWS 與 NVIDIA 平台，單一平台換代落選的衝擊放大。","h_ref":"H2","clock":"🔥","threshold":"伺服器占比回落至 50% 以下，或 2027 年底前 AWS 以外 ASIC 客戶仍未量產","evidence_refs":["customer_concentration_credit#0","customer_second_source#0"]}],"single_thing":{"description":"2027 年主力 AI 機櫃平台（NVIDIA 下一代與 AWS ASIC 機櫃）換代時，公司未獲選為滑軌或液冷快接頭主要供應商。","why_fatal":"法人估第三季伺服器已占營收 8 成以上，2027 年產能倍增以新平台放量為前提；落選會讓 FY2027E EPS 由 Base 90 元落到 70 元以下，倍數同時由成長股收縮到零組件循環股，是股價對單一事件最大的敏感項。","if_happens":"清倉；未持有則停止追蹤並取消進場價。","how_monitor":"每季法說的新平台量產時程與客戶驗證進度、月營收年增率、越南廠稼動率、供應鏈報導的平台供應商名單。","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":30.98,"FY2026E":66.17,"FY2027E":null,"FY2028E":null},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（新台幣）；FY2026E 為 FactSet 共識中位數（9 家，2026-07 報導）；FY2027E／FY2028E 共識事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6805.TW_20261011/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"AI 資本支出與折疊機新機兩個產品週期疊加的精密機構件廠，擴產期毛利率與營業槓桿同步放大"},"industry":{"clock_phase":"II","sd_verdict_source":"供需持久性判為週期性：需求是雲端資本支出的衍生需求，供給端公司自身 2027 年產能倍增、滑軌三強同步擴產，供給可逆性高；依據為 2026 年 8 月法說產能規劃與滑軌擴產報導。","bargaining":{"up":"上游原物料與加工環節的議價事實表未涵蓋。","down":"下游是 NVIDIA 主導的 GPU／ASIC 平台與雲端業者，平台定案權在客戶手上，買方集中度高。","geo":"以中國生產為主，越南廠擴產滑軌與快接頭，目的之一是降低單一地區依賴。"},"profit_pool_dir":"利潤池由消費性折疊機轉向 AI 伺服器機構件，伺服器占比一年內由 19.2% 升至 55.7%。","tam_table":[{"item":"折疊機出貨（2025）","value":"約 1,830 萬支，占手機市場 1.6%"},{"item":"折疊機成長（Counterpoint，2026-09）","value":"全球累計出貨 2026 年底破 1 億支，2027 年出貨年增 37%，預期蘋果 2026 年占 25%"},{"item":"蘋果折疊 iPhone","value":"IDC 預估 2027 年逾 1,700 萬支；Mizuho 稱鉸鏈與面板設計未定，上市可能延至 2027；公司未列鉸鏈供應商"},{"item":"AI 伺服器滑軌與液冷快接頭的 TAM、滲透率與利潤池占比","value":"事實表未涵蓋；滑軌台灣三強為川湖、南俊、富世達，無權威市占統計"}]},"moat":{"mechanism":"精密機構件工藝由鉸鏈延伸到伺服器滑軌與液冷快接頭，加上每一代平台的認證資格與越南自動化產能；轉換成本只存在於單一平台生命週期內。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：AWS 第二季起出貨、多項 NVIDIA／ASIC 滑軌專案第三季起投產、伺服器占比一年由 19.2% 升至 55.7%。定價面縮減：折疊機最大客戶的 Pure S 專案未承接、蘋果鉸鏈名單未列、滑軌僅排第三。最大客戶份額下滑，方向不能判擴大，兩邊相抵判 →。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用份額方向與利潤率對照。","threats":[{"level":"🟡","text":"折疊機鉸鏈份額被新日興與 Amphenol 分走：華為 Pure S 未承接、蘋果折疊 iPhone 鉸鏈名單未列，折疊機最大增量不在手上。","p":0.5,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"伺服器滑軌排第三，川湖與南俊同步擴產，2027 年後滑軌報價可能下修。","p":0.35,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"液冷快接頭目前近滿載、毛利靠供給吃緊；公司自身 2027 年產能倍增，若其他液冷零組件廠跟進，單價與毛利率回落（快接頭市占統計事實表未涵蓋）。","p":0.4,"evidence_refs":["supply_demand_durability#0"]}],"roic_durability":{"quadrant":"高營業利益率（TTM 24.27%）×周轉率不明（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心機櫃，決策者是 GPU／ASIC 平台與伺服器設計團隊，付款者是雲端業者與代工廠，三者都成立；液冷機櫃一定要用滑軌與快接頭，屬需要而非想要。但這是雲端資本支出的衍生需求，急迫性高不等於持久，2028 年後的需求事實表未涵蓋。"},{"item":"決策層級","level":"🟡","text":"替代性在平台世代這個最小單位決定：每一代 NVIDIA／ASIC 平台都要重新驗證，AWS 第二季才開始出貨，其他 ASIC 客戶仍在驗證。滑軌有三家台廠可選，客戶多源採購，轉換成本只在單一平台生命週期內有效。"},{"item":"價值鏈分配","level":"🟡","text":"價值大部分落在 GPU 與 ASIC 端，滑軌與快接頭占機櫃成本的比例事實表未涵蓋；買方高度集中，客戶握有定案權。目前 34% 的毛利率靠快接頭近滿載的供給吃緊，產能倍增後分配可能回到買方。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的機構件，沒有消費者或政策對價格的容忍上限，也不依賴監管授權；外部約束主要是地緣，越南擴產用來降低中國單一地區依賴，關稅與出口管制未見相關報導。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋（Q2 資本支出僅 0.22 億元、營業現金流 15.84 億元，淨再投資接近零，公式不適用）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；投入資本、折舊與營運資金變動事實表未涵蓋，無法計算。可觀察的代理：TTM 自由現金流利潤率 25.6% 高於營業利益率 24.27%，成長目前由內部現金支應。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","6805.TW":30.38,"3017.TW":28.87,"3324.TWO":27.85,"3653.TW":42.63,"8996.TW":27.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","6805.TW":24.27,"3017.TW":23.56,"3324.TWO":15.3,"3653.TW":33.06,"8996.TW":16.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","6805.TW":25.6,"3017.TW":24.1,"3324.TWO":-13.66,"3653.TW":15.18,"8996.TW":6.98,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","6805.TW":4.6,"3017.TW":3.36,"3324.TWO":5.57,"3653.TW":3.61,"8996.TW":3.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3017.TW","gm":28.87,"om":23.56,"fcf_margin":24.1,"rd_intensity":3.36,"strategy_note":"毛利率與營業利益率和富世達相近，同屬吃液冷順風的台廠；對照表只能比利潤率，無法比快接頭份額。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3324.TWO","gm":27.85,"om":15.3,"fcf_margin":-13.66,"rd_intensity":5.57,"strategy_note":"毛利率接近但自由現金流為負，擴產吃現金；富世達的現金轉換明顯較好。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3653.TW","gm":42.63,"om":33.06,"fcf_margin":15.18,"rd_intensity":3.61,"strategy_note":"毛利率與營業利益率都高於富世達，是液冷相關零組件裡定價力較強的參照。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"8996.TW","gm":27.03,"om":16.3,"fcf_margin":6.98,"rd_intensity":3.31,"strategy_note":"營業利益率與自由現金流利潤率都低於富世達，規模化的散熱方案未轉成更高獲利。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（伺服器滑軌與快接頭出貨、產能擴張），組合為輔（伺服器占比拉高毛利率）；無併購、無回購。","runway_years":"事實表未涵蓋（液冷與滑軌滲透率無資料，無法換算）","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板無法計算：增量 ROIC 與再投資率所需的投入資本、折舊、營運資金事實表未涵蓋。代理證據顯示成長由內部現金支應（Q2 營業現金流 15.84 億元、資本支出 0.22 億元），Base 路徑 FY2025A→FY2028E EPS 年化約 50.7% 主要來自產能擴張的量與組合；是否超過天花板無法裁定。","segments":[{"item":"伺服器（滑軌＋液冷快接頭）","value":"上半年占 55.7%（去年同期 19.2%），營收約為去年同期的 4.7 倍；法人估第三季占比升至 8 成以上"},{"item":"折疊機鉸鏈","value":"上半年占 38%（去年同期 71%），營收估年減約 13%"},{"item":"筆電","value":"上半年占 5.6%（去年同期 8.9%）"}],"decay_signals":[{"item":"核心市占近 12 個月縮減","lit":true,"note":"折疊機：華為 Pure S 未承接、蘋果鉸鏈名單未列，上半年折疊機營收估年減約 13%"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"2025 年 EPS 年增約 73%（30.98 元對 17.89 元），營收年增 51.62%，差逾 5 個百分點，屬擴產期營業槓桿"},{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 毛利率 34.05%，高於 2025 年全年 26.34%"},{"item":"自由現金流÷淨利＜0.75 連 2 年","lit":false,"note":"2024 年約 0.70、2025 年約 0.77，未連兩年；Q2 2026 約 1.84"},{"item":"SBC 占營收＞5% 且逐年上升","lit":false,"note":"約 0%"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產能擴張而非併購，股東回報可見部分只有股息（殖利率約 0.5%），近三年現金去向事實表未涵蓋。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事件掃描未見併購紀錄，成長來自自有產能擴張","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購紀錄事實表未涵蓋；可見的股東回報只有股息，殖利率 0.527%","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營收約 0%（Q2 2026），Q1 僅約 250 萬元；稀釋 EPS 12.37 元對基本 12.39 元","grade":"過"}]},"valuation":{"basis":"trailing 本益比與 FY2026 共識前瞻本益比為主尺，PEG 輔助；循環屬性以獲利正常化後的終端倍數校驗。","peers":{"expanded":false,"reason":"同業本益比與目標價事實表未涵蓋，同業對照只有利潤率，無法當倍數錨；終端倍數改以成長降至 5～10% 的零組件廠倍數區間定錨，並標資料缺口。"},"fwd_pe":35.8,"peg":1.8,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"三個倍數都在可得 4 個年度端點的最高（非連續五年序列，五年分位事實表未涵蓋）；前瞻本益比約 35.8 倍、PEG 約 1.8；現價距共識目標價約 +9.7%，Base 五年終值約 +11.4%。成長真實但價格已大致反映，判偏貴；未到最貴一級，是因為動能未過熱、且 8 月法說後法人調升獲利預估。","upside_short_pct":9.7,"upside_mid_pct":11.4},"trap_analysis":{"verdict":"🟡","label":"週期高點的獲利放大，非價值陷阱；風險在倍數收縮與折疊機份額流失"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"公司 2027 年滑軌與快接頭產能要比現在倍增，滑軌三強同時擴產（富世達由 7～8 萬套擴至 35 萬套）；需求全部來自雲端資本支出；大和點名主要客戶市占率不如預期是下行風險。","assumption":"雲端資本支出 2028 年仍成長，新增產能被吸收、報價守住。","consequence":"若 2028 年進入消化期，滑軌與快接頭報價下修，EPS 由 2027 年高點回落到 50～60 元、本益比收縮到 14～15 倍，五年後股價約 780～900 元，較現價虧六成以上。","ruling":"採納：Bear 機率給 30%，這是五年虧損過半最可能的路徑。與唯一致命事件部分重疊——致命事件是平台落選（離散），本條是整體報價下行（連續），兩者分開監測。","watch":"月營收年增率、單季毛利率、同業擴產公告","evidence_refs":["supply_demand_durability#3","competitive_share_entrants#3","channel_business_model_shift#2"],"fact_refs":["f_kpi8","f_kpi1"]},{"view":"論點失敗","evidence":"2026 第一季未承接華為 Pure S 鉸鏈；蘋果折疊 iPhone 鉸鏈由新日興主供、Amphenol 競爭；2025 年 4 月時鉸鏈占營收約 85%、高度依賴陸系品牌。","assumption":"華為三摺與左右摺新機能補回 Pure S 的缺口，折疊機維持現金流業務。","consequence":"折疊機營收年減擴大，伺服器以外沒有第二支腳，伺服器一旦換代失利就沒有緩衝。","ruling":"部分採納：上半年折疊機營收估年減約 13%，已計入 Base；蘋果名單未列，折疊機不再算成長來源。","watch":"每季折疊機營收年增率","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_concentration_credit#0"],"fact_refs":["f_kpi9"]},{"view":"論點成功但股東經濟變差","evidence":"2024 年擴產期自由現金流只有淨利的 70%（8.57 億元÷12.27 億元），2025 年 77%；股息殖利率 0.527%，回購紀錄事實表未涵蓋。","assumption":"產能倍增不需要大額資本支出，成長紅利會以現金回到股東手上。","consequence":"若越南廠與 2027 年倍增轉為重資本，或客戶要求降價換量，EPS 成長了，但每股自由現金流與股東回報不成比例。","ruling":"暫不採納：Q2 營業現金流 15.84 億元、資本支出 0.22 億元，TTM 自由現金流利潤率高於營業利益率，目前沒有重資本跡象；保留監測。","watch":"自由現金流÷淨利連兩年低於 0.75；資本支出占營收比","evidence_refs":[],"fact_refs":["f_kpi5","f_peer_6805_tw_fcf_margin_pct","f_dividend_yield_ttm"]},{"view":"價格已反映太多","evidence":"trailing 本益比 50.73 倍、P/S 10.51 倍、EV/S 9.93 倍都在可得 4 個年度端點的最高；現價 2,370 元已落在賣方平均目標價約 2,391～2,594 元附近，FactSet 目標價 2,600 元只剩約 10%；FY2026 EPS 共識中位數由 66.52 元微降至 66.17 元。","assumption":"市場會一直用高成長年度的倍數評價，2027 年後倍數不回落。","consequence":"Base 路徑五年後約 2,640 元，只比現價高約 11%；要拿到一成年化報酬需要 FY2030E EPS 約 173 元，等同 Bull 路徑。","ruling":"採納：這是不追價的主因，也是唯一的約束條件。","watch":"股價相對 52 週均線 1,717 元的距離；FY2027 共識 EPS 上修幅度","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"],"fact_refs":["f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_price_at_dd","f_ma_w52"]}],"max_dd":{"lo":-72,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 2370.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=2370.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"折疊機份額：公司說法對上客戶專案落選","cause":null,"prior_field":null,"side_a":"公司稱在中系與美系客戶皆為折疊機軸承主要供應商，訂單占比超過五成（2026-03）。","side_b":"2026 第一季未承接華為 Pure S 鉸鏈；蘋果折疊 iPhone 鉸鏈由新日興主供、Amphenol 競爭，未列富世達；上半年折疊機營收估年減約 13%（79.24 億元×38% 對上回推去年同期 48.72 億元×71%）。","ruling":"可調和，屬程度差異：既有中系客戶仍是主要供應商，但份額在流失，最大增量不在手上。採 B 側作為定價依據，折疊機視為逐年縮小的現金流業務，不計入成長。","evidence_level":"法說摘要與媒體供應鏈報導，非公司正式揭露","settle_metric":"每季法說營收結構中的折疊機營收年增率","if_then":["若 2026 下半年華為三摺與左右摺新機帶動折疊機營收年增轉正，則把折疊機由衰退改為不變並上調 Base FY2027E","若蘋果折疊機量產後折疊機營收仍連 2 季年減超過 25%，則下修 Base 並停止任何加碼"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2"]},{"axis":"客戶集中度：降低還是換對象","cause":null,"prior_field":null,"side_a":"2025 年 4 月報導鉸鏈占營收約 85%，為陸系品牌高階折疊機的關鍵供應商。","side_b":"2026 上半年伺服器占 55.7%，法人估第三季伺服器占比升至 8 成以上；AWS 第二季起出貨，其他 ASIC 客戶仍在驗證。","ruling":"可調和：舊數字已過時，但集中度沒有下降，只是從陸系手機品牌換到少數 AI 平台；風險性質由消費週期換成雲端資本支出週期與平台換代。","evidence_level":"媒體報導與法人說法","settle_metric":"AWS 以外 ASIC 客戶的量產時點；伺服器營收占比","if_then":["若 2027 年底前至少一家 AWS 以外的 ASIC 客戶量產，則把集中度風險由中期降為長期","若伺服器占比逾 8 成而第二家雲端客戶到 2027 年底仍未量產，則 Bear 機率由 30% 上調至 35%"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#0","end_markets#4"]},{"axis":"賣方全面看多對上本研究不追價","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：8 位分析師全為買進、FactSet 目標價 2,600 元；第三季伺服器占比衝上 8 成以上，第三、四季營收預期季增雙位數；2027 年產能倍增、AWS 自 2027 第一季放量、CPO 產品 2027 年貢獻營收；26 週漲 29.71% 但 RSI 只有 54.49，沒有過熱。","side_b":"現價 2,370 元已在平均目標價約 2,391～2,594 元附近，trailing 本益比 50.73 倍為可得年度端點最高；FY2026 EPS 共識中位數由 66.52 元微降至 66.17 元；Base 路徑五年報酬約 11%。","ruling":"不可調和（行動方向相反），採 B 側。依據：分歧在框架層，賣方以短期目標價對高成長年度獲利給高倍數，本研究以五年終值計入同業同步倍增產能後的倍數回落；現價要 Bull 路徑才換得到一成年化報酬。執行：不追價，等價格回落或等 2027 年共識上修。","evidence_level":"賣方共識快照（日期不明確）與年度端點估值","settle_metric":"股價對 52 週均線的距離；FY2027 共識 EPS","if_then":["若股價回落至 1,700 元附近（約 52 週均線）且最近一季毛利率≥30%，則重跑研究後分批建立首倉","若股價續漲但 2027 年新平台與 AWS 放量的營收證據未到，則不追","反向：若 2027 年共識 EPS 上修使現價前瞻本益比降到 25 倍以下且毛利率≥33%，則不等回落，改以現價分批建立首倉"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"股價回落至 1,700 元附近且最近一季毛利率仍在 30% 以上，重跑研究後分批建立首倉","type":"估值rearm","maps_to":null,"metric":"股價；單季毛利率","threshold":"股價≤1,700 元且毛利率≥30%","action":"重跑研究後分批建立首倉","source_freq":"每日股價／每季財報","date":null},{"n":2,"text":"2026 第三季財報驗證下半年轉強","type":"假設驗證","maps_to":"H1","metric":"第三季營收季增率、毛利率","threshold":"營收季增≥10% 且毛利率≥33%","action":"未達則下修 Base FY2026E 至 60 元並把進場價下移","source_freq":"季報","date":"2026-11"},{"n":3,"text":"2027 上半年產能倍增轉成營收","type":"假設驗證","maps_to":"H2","metric":"2027 上半年營收年增率；伺服器占比","threshold":"營收年增≥30% 且伺服器占比≥70%","action":"達標則上調 Base FY2027E 並重估進場價；未達則維持觀望","source_freq":"月營收／法說","date":"2027-08"},{"n":4,"text":"折疊機份額流失擴大","type":"風險","maps_to":"R2","metric":"折疊機營收年增率","threshold":"連 2 季≤−25%","action":"下修 Base FY2027E 約 5%，停止任何加碼","source_freq":"每季法說營收結構","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","channel_business_model_shift#2"]},{"n":5,"text":"資本支出消化與同業擴產壓縮毛利","type":"風險","maps_to":"R3","metric":"單季毛利率；月營收年增率","threshold":"毛利率連 2 季＜30%，或月營收年增轉負連 3 個月","action":"取消進場價、改以 Bear 路徑重估；若已持有則減碼一半","source_freq":"季報／月營收","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":6,"text":"2027 年主力 AI 機櫃平台換代時未獲選為滑軌或快接頭主要供應商","type":"Single Thing","maps_to":"Single Thing","metric":"新平台量產供應商名單；伺服器營收年增率","threshold":"法說或供應鏈報導確認落選，或伺服器營收年增轉負","action":"清倉；未持有則停止追蹤","source_freq":"法說／供應鏈報導","date":"2027-06"},{"n":7,"text":"2026 年報與 2027 年法說後全面複審","type":"複審日期","maps_to":null,"metric":"FY2026 實際 EPS 對 Base 66 元","threshold":"偏離≥10%","action":"重跑完整研究","source_freq":"年報","date":"2027-03"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"連 2 季＜30%","window":"2026Q3–2027Q4","source":"公司季報","last_status":"ok"},{"metric":"折疊機營收年增率","bear_threshold":"連 2 季≤−25%","window":"2026Q3–2027Q4","source":"每季法說營收結構","last_status":"warning"},{"metric":"月營收年增率","bear_threshold":"轉負連 3 個月","window":"2026-10 至 2027-12","source":"公開資訊觀測站月營收","last_status":"unknown"},{"metric":"伺服器產品營收占比","bear_threshold":"回落至 50% 以下","window":"2027 全年","source":"法說營收結構","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方以短期目標價對高成長年度獲利給高倍數，未計入 2027 年同業同步倍增產能與 2028 年資本支出消化後的倍數回落；現價要 Bull 路徑才換得到一成年化報酬。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=29.71, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價≤1,700 元（約 52 週均線）且最近一季毛利率≥30%；或 2027 共識 EPS 上修使前瞻本益比≤25 倍","exec_line":"不追價；觸發重啟條件後先重跑研究，再分批建立首倉；主力平台落選則停止追蹤。"},"reasoning":{"industry":"營收分部（2026 上半年）：伺服器（滑軌＋液冷快接頭）55.7%、折疊機鉸鏈 38%、筆電 5.6%，去年同期分別為 19.2%、71%、8.9%。以上半年營收 79.24 億元（年增 62.64%）回推去年同期約 48.72 億元，伺服器營收約 44.1 億元、約為去年同期 9.4 億元的 4.7 倍；折疊機約 30.1 億元，對去年同期約 34.6 億元年減約 13%。最新一季（Q2 2026）營收 37.40 億元、季減 10.61%，毛利率 34.05%、營業利益率 27.82%，EPS 12.39 元；營收下滑時毛利率仍季增 1.74 個百分點，說明伺服器組合在拉高毛利。錢卡在兩個節點：一是 NVIDIA 與 ASIC 平台換代時能否入選，二是產能能否到位（滑軌 35 萬組／月、快接頭 300 萬件／月且近滿載）。產業時鐘判 II（擴張）：快接頭近滿載、第三季起多項新專案投產、2027 年產能規劃倍增，依據是供需而非股價。單點依賴：集中度沒有消失，只是由陸系折疊機品牌換到 AWS 與 NVIDIA 主導的平台；法人估第三季伺服器占比升至 8 成以上，單一平台落選的衝擊因此放大。管理層指引只有定性（下半年營收與毛利率優於上半年、費用率下降），沒有數字區間；最新一季逐字稿未收錄，無法對照管理層前後說法。","moat":"機制：把折疊機鉸鏈的精密機構件工藝延伸到伺服器滑軌與液冷快接頭，靠平台認證與越南自動化產能卡位。對同業的 ROIC 利差無法計算（投入資本事實表未涵蓋），改看份額方向與利潤率：TTM 毛利率 30.38%、營業利益率 24.27%，毛利率高於 3017、3324、8996，低於 3653；FCF 利潤率 25.6% 為同業對照中最高。份額方向分兩邊：伺服器線擴大（AWS 第二季起出貨、NVIDIA／ASIC 多項滑軌專案第三季起投產）；折疊機線縮減（華為 Pure S 未承接、蘋果折疊 iPhone 鉸鏈由新日興主供、Amphenol 競爭，上半年折疊機營收估年減約 13%）。領先玩家在最大客戶的份額下滑，方向不能判擴大，兩邊相抵判 →。評分：執行力 7，一年內把伺服器占比由 19.2% 拉到 55.7%、滑軌產能由 7～8 萬套擴到 35 萬套，扣分在折疊機丟掉華為 Pure S；定價力 5，滑軌排第三、折疊機份額流失、快接頭毛利靠近滿載的供給吃緊撐住。合併約 6，等級 C。架構替代：浸沒式液冷建置成本高數倍、機構需重新設計，部分品牌廠偏好水循環，現有證據不支持列為架構替代；折疊機摺痕改善轉向 UTG 與面板堆疊的材料協同設計，不是替換鉸鏈本身。","growth":"成長來源是量與組合：AI 伺服器滑軌與快接頭出貨放量、產能擴張，毛利率隨伺服器占比上升；沒有併購，也沒有回購。三年共識 EPS 成長率無法計算：只有 FY2026 共識中位數 66.17 元（FactSet 9 家，2026-07 報導），FY2027／FY2028 共識事實表未涵蓋。Base 路徑 FY2025A 30.98 元→FY2028E 106 元，年化約 50.7%，主要來自 2026 至 2027 年的放量；FY2026E→FY2029E 年化約 20%。內生天花板缺投入資本資料無法量化，缺口無法計算，但成長可歸因於產能擴張的量與組合，不靠收購或回購；長期信心上限取中。跑道：折疊機滲透率 1.6% 很低，但最大增量（蘋果）不在手上、華為 Pure S 未承接；伺服器線滲透率事實表未涵蓋，管理層稱 2027 年成長最高的是快接頭，其次滑軌與手機；法人提到 CPO 產品 2027 年貢獻營收，未見規模數字，不算已證實的第二條曲線。衰退信號亮 2 個：折疊機核心份額縮減、EPS 成長顯著高於營收成長，長期成長性判黃燈。","governance":"自由現金流÷淨利：2022 年約 3.9（22.08 億元÷5.64 億元）、2023 年約 1.62、2024 年約 0.70（擴產期）、2025 年約 0.77（16.42 億元÷21.25 億元），Q2 2026 約 1.84（15.62 億元÷8.49 億元）。SBC 占營收約 0%，稀釋 EPS 12.37 元對基本 12.39 元，稀釋可忽略。EV/S 9.93 倍低於 P/S 10.51 倍，表示帳上為淨現金。營運槓桿為正：2025 年營業利益年增約 109%，高於營收年增 51.62%。近三年現金去向四分、債務結構與回購均價事實表未涵蓋；事件掃描未見併購。","valuation":"trailing 本益比 50.73 倍、P/S 10.51 倍、EV/S 9.93 倍，都在可得 4 個年度端點的最高位置；前瞻本益比約 35.8 倍（2,370 元÷FY2026 共識 66.17 元）。賣方：8 位分析師全為買進，平均目標價兩份快照約 2,391 元與 2,594 元，FactSet 目標價 2,600 元，現價只差約 9.7%。Base 五年終值約 2,640 元（120 元×22 倍），比現價高約 11.4%，年化不到 3%；反推一成年化報酬需要約 3,817 元，以 22 倍計要 FY2030E EPS 約 173 元。PEG 以 FY2026E→FY2029E 年化約 20% 計約 1.8；若用 FY2025A 低基期算三年成長會壓到約 0.7，那是週期高成長期的假便宜，不採用。26 週漲 29.71%，RSI 54.49 未過熱，股價在 52 週均線 1,717 元之上約 38%。","premortem":"陷阱判斷依據見反證紀錄：衰退信號亮 2 個（折疊機核心份額縮減、EPS 成長顯著高於營收成長），判黃燈，屬週期高點的獲利放大，不是價值陷阱。產業態勢三軸：競爭面惡化（折疊機鉸鏈份額被新日興與 Amphenol 分走，滑軌三強同步擴產）；結構面轉好（液冷滲透推升快接頭近滿載，伺服器占比一年升到近 3 倍）；其他結構變數以客戶結構為主（集中度由陸系品牌換到 AI 平台），裁決為雙向拉鋸。成長熄火壓力測試：Base 到 FY2028E 106 元後，若 FY2029 成長降到 15%／10%／5%，給 20／15／11 倍，價格約 2,440／1,750／1,220 元，對現價 +3%／−26%／−48%，三種只過一種。最大回撤：純倍數收縮回 28 倍即跌約 45%，Bear 路徑谷底可到約 −70%。事件面：併購、訴訟、召回、監管調查均未見。"},"plain":{"six":{"how_it_makes_money":"賺 AI 伺服器機櫃與折疊機品牌的精密機構件錢：滑軌、液冷快接頭與鉸鏈按件出貨，利潤卡在平台換代時能否被選進供應商名單、以及產能能否及時到位；伺服器已占上半年營收 55.7%，成為主引擎。","moat":"護城河方向不變（→）、等級 C：伺服器線的平台導入在擴大，折疊機在最大客戶與蘋果的份額在縮，滑軌只排第三；毛利率走高主要來自產品組合與快接頭供給吃緊，不是定價權。","growth":"五年後的跑道判黃燈（🟡）：折疊機滲透率只有 1.6%，但公司不在蘋果鉸鏈名單；伺服器線靠 2027 年產能倍增撐到 2028 年，之後看雲端資本支出，第二條曲線（CPO 產品）只有法人說法。","capital":"資本配置以自有現金擴產，不靠併購也沒有股權稀釋，現金轉換好；但回購與現金去向事實表未涵蓋，可見的股東回報只有約 0.5% 的股息。","valuation":"現價要求 FY2030E EPS 約 173 元、且屆時仍給 22 倍，才換得到一成年化報酬，等同 Bull 路徑；我信成長、不信倍數撐得住，結論是偏貴、等價格。","how_wrong":"最可能看錯在兩處：一是 2027 年產能倍增撞上同業同步擴產與資本支出消化，毛利率回落、倍數從 50 倍級收縮；二是低估 AI 平台導入的黏著度，伺服器成長一路延續到 2029 年，現價其實不貴。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方以短期目標價對高成長年度獲利給高倍數，未計入 2027 年同業同步倍增產能與 2028 年資本支出消化後的倍數回落；現價要 Bull 路徑才換得到一成年化報酬。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回落至 1,700 元附近（約 52 週均線）且最近一季毛利率維持 30% 以上；或 2027 年共識 EPS 上修，使同價位前瞻本益比降到 25 倍以下。","trap":"🟡","val":"🟠","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":2370.0,"week26_return_pct":29.71,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母為 TTM 與 FY2026 共識 EPS，屬擴產期高成長獲利、非一次性；但以 FY2025A 低基期算成長會讓 PEG 失真，本結論以 FY2026E→FY2029E 成長率為準。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026 第三季財報與法說：驗證伺服器占比升至 8 成以上與毛利率","impact":"高","watch":"營收季增率是否≥10%、毛利率是否≥33%"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"蘋果折疊機上市時點（Counterpoint 預期 2026 年，Mizuho 稱可能延至 2027）","impact":"中","watch":"公司是否打入鉸鏈或周邊機構件供應鏈；折疊機營收年增率"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"AWS 滑軌出貨自 2027 第一季增溫（法人預估）","impact":"高","watch":"月營收年增率；AWS 以外 ASIC 客戶的驗證進度"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"2027 年滑軌與液冷快接頭產能較現在倍增","impact":"中","watch":"稼動率與毛利率是否同步維持"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,974B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6805.TW_20261011/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2><p class="lead">護城河等級 C，伺服器線在擴大，折疊機線在縮小，方向持平。</p><ul class="pts">
<li>護城河的機制是精密機構件工藝，由鉸鏈延伸到滑軌與液冷快接頭，加上每一代平台的認證資格與越南自動化產能。轉換成本只存在於單一平台生命週期內，因為每一代 NVIDIA 與 ASIC 平台都要重新驗證，滑軌有三家台廠可選，客戶多源採購。</li>
<li>評分是執行力 7、定價力 5，合併約 6，等級 C。執行力給 7，因為一年內把伺服器占比由 19.2% 拉到 55.7%，滑軌產能由 7 萬到 8 萬套擴到 35 萬套。扣分在折疊機丟掉華為 Pure S。定價力給 5，因為滑軌排第三，折疊機份額流失，快接頭毛利靠近滿載的供給吃緊撐住。</li>
<li>方向判持平。擴大的證據是 AWS 第二季起出貨，NVIDIA 與 ASIC 多項滑軌專案第三季起投產。縮小的證據是華為 Pure S 未承接，蘋果折疊 iPhone 鉸鏈由新日興主供，Amphenol 也在競爭。領先玩家在最大客戶的份額下滑，所以方向不能判擴大，兩邊相抵判持平。</li>
<li>威脅有三條，都是黃燈。折疊機鉸鏈份額被新日興與 Amphenol 分走，機率 0.5。滑軌排第三，川湖與南俊同步擴產，2027 年後報價可能下修，機率 0.35。液冷快接頭目前近滿載，毛利靠供給吃緊，公司自身 2027 年產能倍增，若其他廠跟進，單價與毛利率回落，機率 0.4。</li>
<li>同業對照只能比利潤率，因為同業 ROIC 與投入資本資料沒有涵蓋。富世達 TTM 毛利率 30.38%，營業利益率 24.27%，FCF 利潤率 25.6%。3017 為 28.87%、23.56%、24.1%，3324 為 27.85%、15.3% 與 −13.66%，3653 為 42.63%、33.06%、15.18%，8996 為 27.03%、16.3%、6.98%。</li>
<li>解讀這張表有兩個重點。第一，富世達現金轉換在同業中最好，3324 擴產吃現金，自由現金流為負。第二，3653 的毛利率與營業利益率都明顯高於富世達，是液冷相關零組件中定價力較強的參照，富世達離那個水準還有距離。</li>
<li>報酬持續期四個檢查點都沒有綠燈，只有社會容忍度亮綠。需求基礎值黃：資料中心機櫃一定要用滑軌與快接頭，屬需要而非想要，但這是雲端資本支出的衍生需求，2028 年後缺資料。決策層級黃：替代性在平台世代決定。價值鏈分配黃：價值大多落在 GPU 與 ASIC 端，客戶握有定案權，34% 的毛利率靠供給吃緊。</li>
<li>內生成長率無法計算，投入資本、折舊與營運資金資料沒有涵蓋。可觀察的代理是 TTM 自由現金流利潤率 25.6% 高於營業利益率 24.27%，成長由內部現金支應。Q2 資本支出只有 0.22 億元，營業現金流 15.84 億元，淨再投資接近零，公式不適用。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```