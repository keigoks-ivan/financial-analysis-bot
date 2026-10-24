你是 stock-analyst v20 的**散文層（prose）agent**，標的 BX（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BX_20261024/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：BX　日期：2026-10-24　archetype：None　前份裁決：2026-07-24　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1710B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（732B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（913B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1500B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（895B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（738B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（681B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1896B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4078B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2128B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1710           3703-5290      5 條（2–6 內）  
s3                  8000         732           5088-7268      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3308          8184-11692      5 條（2–6 內）  
s6                 11000         738          7183-10262      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         681           1973-2819      5 條（2–6 內）  
s10                 5000        1896           2173-3104      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2128           2000-2872      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5039B；至少需散文≈39.96KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−55
−53%
−49%
−39%
−35
−35%
−5.2%
−5%
−1.13
−1.1%
0
0.14%
0.4%
0.51%
01
1%
1
1.02
1.12
1.2
1.28
1.32
1.348
1.368
1.49%
1.6
1.895
2%
2
2.3
2.5
3
3.2%
3.87
4
4%
04
4.1
4.25
4.4%
4.4
4.43
4.5
4.6
4.992
5%
5
05
5.2%
5.48
5.5
5.7
5.9
5.92
06
6%
6
6.189
6.2
6.5
6.6
6.8
7
07
7.0
7%
7.2
7.38
7.6
7.839
7.9
7.91
8
8%
8.1%
8.2
8.6
8.933
9%
9
9.2%
9.4
9.8
9.9
10%
10
10.2
11
11%
11.1%
11.4
12%
12
12.3
12.5%
12.7%
12.9%
13
13.498
14.0%
14
14%
15%
15.31
15.6%
15.721
16%
16
17%
17.157
18
18%
19
19.9
19.93
20
20%
20.3
22%
22
23
24
25%
25
26
26%
26.4%
27
28.4
29%
30%
30
30.629
31
32.5%
35%
40
40.3%
42
44%
45
47.6%
49
50
50%
52
55
55.6
55.7%
58%
61
63%
63
70
72
72.6
74
75%
76.0%
77
85%
86
90
91
92%
100%
100
104
105
$105
112
117.97
122
124.1
124.5
126
150
150%
156
184
295.2
297
358
401
633
700
907
2025
2026
2027
2030
20261024
1,139
2,700
3,000
3,090
3,091
3,300
4,654
4,800
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
{"meta":{"ticker":"BX","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Blackstone Inc."},"oneliner":"全球最大另類資管，費用相關獲利約占可分配盈餘九成；零售私募信貸贖回與不動產拖累已反映在股價，現價約當年盈餘 20 倍、殖利率 4.4%，等 4Q'26 獲利兌現放量驗證","thesis":{"H":[{"id":"H1","text":"費用相關獲利靠基礎管理費雙位數成長持續複利，不需倚賴獲利兌現","2y":"FY2027 基礎管理費全年年增 ≥10%（管理層指引低雙位數）","5y":"費用相關獲利五年 CAGR ≥10%","10y":null,"threshold":"FY2027 基礎管理費年增 ≥10%；FY2027 費用相關獲利年增 ≥10%","source":"季報新聞稿分部表、CFO 法說指引","drift_rule":"TTM 基礎管理費年增率偏離 10%門檻 ≥5%連 2 季為削弱，≥10%連 3 季為反轉"},{"id":"H2","text":"被壓抑的獲利兌現在 4Q'26 至 2027 年回升，帶動每股可分配盈餘回到共識路徑","2y":"FY2027 每股可分配盈餘 ≥7.0 美元（共識 7.38）","5y":null,"10y":null,"threshold":"4Q'26 淨獲利兌現高於 3Q'26；FY2027 每股可分配盈餘 ≥7.0","source":"季報新聞稿；CFO 3Q'26 法說稱第四季合約中待交割的附帶權益兌現即超過第三季全公司淨兌現","drift_rule":"TTM 每股可分配盈餘偏離共識路徑 ≥5%連 2 季為削弱，≥10%連 3 季為反轉"},{"id":"H3","text":"私人財富與保險兩條永續資本通路維持雙位數擴張，構成五年以上跑道","2y":null,"5y":"私人財富 AUM 與保險 AUM 五年 CAGR 皆 ≥10%","10y":"個人投資人私人資產配置由約 1%明顯上升，401(k) 通路形成第二曲線","threshold":"私人財富 AUM 年增 ≥10%（3Q'26 為 15%）、保險 AUM 年增 ≥10%（3Q'26 為 14%）","source":"季報法說通路 AUM 揭露","drift_rule":"TTM 年增率偏離 10%門檻 ≥5%連 4 季為削弱，≥10%連 6 季為反轉"}],"R":[{"id":"R1","text":"BCRED 等零售私募信貸半流動產品贖回壓力延續或擴散，傷及私人財富品牌與費用","h_ref":"H3","clock":"⚡","threshold":"BCRED 季度贖回申請 ≥10% NAV 且兌付 <50%連 2 季","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","supply_demand_durability#0","supply_demand_durability#1","end_markets#6","substitute_technology#1"]},{"id":"R2","text":"高利率讓不動產估值與費用續降，並拖慢組合公司退出；關稅與美中摩擦加重組合公司壓力","h_ref":"H2","clock":"🔥","threshold":"Real Estate 分部費用相關獲利年減 ≥5%連 4 季，或 BREP 機會型基金季度估值連 2 季下跌","evidence_refs":["end_markets#0","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R3","text":"私募信貸監管收緊與法律案件累積（國會發函、SEC 例行調查、Kentucky 退休基金訴訟和解破局、LivCor 反壟斷和解）","h_ref":"H3","clock":"🐢","threshold":"監管機關正式提案限制零售半流動產品流動性或槓桿；或單一罰款、和解 ≥5 億美元","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#2","lawsuit_class_action#0"]},{"id":"R4","text":"私人財富與保險通路費率競爭，對手降費或加碼分銷費，AI 也可能讓同業取得營運優勢；AUM 成長但費率下滑","h_ref":"H1","clock":"🔥","threshold":"基礎管理費年增落後收費 AUM 年增 ≥5pp 連 4 季","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","channel_business_model_shift#1","substitute_technology#0"]}],"single_thing":{"description":"BCRED 宣布暫停贖回，或兌付比例跌破申請的 25%（事件型）","why_fatal":"BCRED 2025 年貢獻管理與激勵費 12 億美元，約占全年營收一成；更大的傷害在私人財富品牌：3,300 億美元通路建立在半流動結構可兌付的信任上，一次暫停會連帶壓抑 BREIT、BXPE、BXINFRA 的銷售","if_happens":"減碼至追蹤倉，重跑完整研究","how_monitor":"每季法說與 BCRED 公告的贖回申請、兌付比例、淨流量","probability":"12–24 個月約 10%：前兩季兌付約 50%且申請者約 90 天拿回 75%資金，借款人 EBITDA 雙位數成長、償債倍數 2.3 倍，暫停需要信用事件觸發"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":16.0,"peg_fy2":1.02,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":5.92,"FY2027E":7.38,"FY2028E":7.91},"fy_end_month":12,"eps_basis":"每股可分配盈餘（Koyfin 共識口徑，非 GAAP）；FY2025A 同口徑實際值事實表未涵蓋，GAAP 稀釋 EPS 3.87 口徑不同，不代入"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BX_20261024/scenario.json","archetype":{"primary":"品質複利成長","secondary":"金融","confidence":"中","fingerprint":"費用型另類資管：經常性管理費加週期性績效分成，資產輕型、高配息"},"industry":{"clock_phase":"I","sd_verdict_source":"機構與保險需求屬結構性持久；零售信用類半流動產品需求屬週期性、供給可逆（PitchBook 2Q26、Stanger 經 CoStar 引用、3Q'26 法說）","bargaining":{"up":"對資金提供者議價強：四檔機構旗艦基金超額認購達硬頂；但私人財富經銷商握有上架與分銷費議價權","down":"對借款人與被投資公司的議價取決於資本稀缺度，AI 基建與投資級私募信貸的資本缺口有利 BX","geo":"日本、印度為近期主要退出來源；關稅與美中摩擦是組合公司層級風險"},"profit_pool_dir":"利潤池從銀行資產負債表與公開市場流向私人市場；業內往規模化多平台業者集中","tam_table":[{"item":"全球個人投資人私人資產配置比重","value":"約 1%（Gray，3Q'26 法說）"},{"item":"BX 私人財富通路 AUM","value":"3,300 億美元，年增 15%（3Q'26 法說）"},{"item":"BX 保險通路 AUM","value":"逾 3,000 億美元，年增 14%（3Q'26 法說）"},{"item":"私募信貸產業 AUM 2030 預估","value":"4.5 兆美元（Preqin 預估）"},{"item":"產業募資 TTM","value":"私募資本總額 1.348 兆美元年減 12.7%；私募債 3,091 億年增 14.0%；不動產 907 億年減 32.5%（PitchBook 2Q26）"},{"item":"營業利益池占比 5 年前→現","value":"事實表未涵蓋"}]},"moat":{"mechanism":"品牌與長期績效→跨資產類別旗艦基金募資規模→永續資本（私人財富 3,300 億、保險逾 3,000 億美元）與大額出資能力→更好的交易來源與承作條件","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：今年四檔機構旗艦基金達硬頂且皆大於前期，近 12 個月流入逾 2,700 億美元。定價面縮減：10-K 稱私人財富與保險通路對手願收較低費用或付較高分銷費，保險委託費率 40–50 基點。兩相抵銷判為穩定","peer_na_reason":"同業 ROIC 事實表未涵蓋；KKR、APO 合併保險子公司，利潤率口徑不可直接比較","threats":[{"level":"🟡","text":"傳統資管自建私募與私人財富平台，部分對手以較低費用或較高分銷費搶零售與保險資金","p":"35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","channel_business_model_shift#1"]},{"level":"🟡","text":"AI 顛覆組合公司（軟體約占公司曝險 6%），並可能改變資管業營運與投資方式；部分同業在 AI 平台上可能領先","p":"25%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"國會與監管機關關注私募信貸，零售半流動產品可能被加上流動性或槓桿限制","p":"30%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是 LP 與個人投資人，決策者是投資長與財富顧問，付款者是基金。機構需求要解決超額報酬與保險利差（Gray 稱較同評級公開債約多 150 基點），屬需要而非想要；但零售端信用類半流動產品贖回顯示，個人投資人的需求可以延後、也可逆"},{"item":"決策層級","level":"🟢","text":"替代性應在單一委託或單一基金承諾層級衡量：封閉型基金鎖定十年以上，保險委託約從 5 億美元起步再擴大，逾半數保險客戶近 12 個月擴大合作；換管理人要重做盡職調查與內部核准，轉換成本高"},{"item":"價值鏈分配","level":"🟡","text":"BX 握有交易來源與大額承作能力，但財富通路經銷商有分銷費議價權，保險客戶分走多數利差（BX 費率 40–50 基點）；對手加碼分銷費會壓縮 BX 分得的份額"},{"item":"社會容忍度","level":"🟡","text":"國會議員已就私募信貸向 BX 等業者發函，子公司 LivCor 以 700 萬美元和解租金合謀案，資料中心面臨公眾態度壓力；401(k) 開放仍待監管程序。零售化越深，政策與社會容忍度越可能成為定價上限"}],"roiic":"資產輕型、投入資本極小，增量報酬率無法有意義計算（事實表未涵蓋投入資本口徑）","reinvest_rate":"趨近 0：管理層政策為長期將現金盈餘 100%返還股東（2026-07-23 CFO），3Q'26 股息約占每股可分配盈餘 85%","endo_ceiling":11,"formula_note":"增量報酬率×再投資率的公式不適用資產輕型資管；改以總 AUM 年增 10%（3Q'26 CFO）加費用營運槓桿約 1pp 代理，內生成長上界約 11%/年"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","BX":null,"KKR":22.49,"APO":95.45,"ARES":55.81,"BLK":47.15,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","BX":null,"KKR":7.84,"APO":24.85,"ARES":18.08,"BLK":32.99,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","BX":40.3,"KKR":11.11,"APO":26.39,"ARES":13.96,"BLK":12.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"KKR","gm":22.49,"om":7.84,"fcf_margin":11.11,"strategy_note":"走自有保險公司路線並合併保險子公司，利潤率被保險業務稀釋；與 BX 第三方保險管理模式路線不同，保險資金爭奪上是直接對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"APO","gm":95.45,"om":24.85,"fcf_margin":26.39,"strategy_note":"同樣自有保險平台，在投資級私募信貸是 BX 最直接的對手；Gray 2Q'26 稱此領域主要是自家與少數私募同業競爭","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ARES","gm":55.81,"om":18.08,"fcf_margin":13.96,"strategy_note":"以直接放款為核心，零售 BDC 通路與 BCRED 正面競爭，同樣在國會私募信貸發函名單中","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BLK","gm":47.15,"om":32.99,"fcf_margin":12.88,"strategy_note":"屬 10-K 所稱自建私募平台的傳統資管，具低費率與分銷規模，威脅集中在私人財富通路","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（AUM 年增 10%、新基金開始收費）加獲利兌現週期回升；價持平偏降；無併購；淨回購數據事實表未涵蓋","runway_years":"≥10（個人投資人私人資產配置約 1%）","runway_post_y5":"🟢","endo_ceiling_basis":"資產輕型、盈餘近全額配發，公式失效；以總 AUM 年增 10%加費用營運槓桿約 1pp 代理，上界約 11%/年","segments":[{"item":"Private Equity","value":"3Q'26 營收 13.498 億美元年減 6%；費用相關獲利 6.189 億年增 26%；季流入 126 億；AUM 4,654 億年增 18%"},{"item":"Real Estate","value":"3Q'26 營收 8.933 億美元年減 6%；費用相關獲利 4.992 億年減 9%；季流入 63 億；AUM 3,090 億年減 4%"},{"item":"Credit & Insurance","value":"3Q'26 營收 7.839 億美元年增 2%；費用相關獲利年減 1%；季流入 358 億；AUM 4,800 億年增 11%"},{"item":"Multi-Asset Investing","value":"3Q'26 營收 1.895 億美元年增 25%；費用相關獲利年增 26%；季流入 86 億；AUM 1,139 億年增 22%"}],"decay_signals":["產業估值倍數系統性下移：另類資管類股股價受壓（Schwarzman 3Q'26 法說自述），倍數歷史數據事實表未涵蓋，暫列亮燈","TAM 萎縮：產業不動產募資 TTM 年減 32.5%（PitchBook 2Q26），限於不動產分部"]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐；股息約占每股可分配盈餘 85%，回購金額事實表未涵蓋"},"capalloc_grade":null,"scorecard":[{"year":"—","action":"ma_roiic","rationale":"公司層級無重大併購（近 12 個月 8-K 僅債券發行）；基金層級收購不屬股東資本","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購金額與均價；政策為長期現金盈餘 100%返還","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"事實表未涵蓋股權激勵與稀釋股數","grade":"N/A"}]},"valuation":{"basis":"Forward P/E（FY2026 共識每股可分配盈餘）","tier":"大型另類資管","peers":{"expanded":false,"reason":"事實表只有同業利潤率、無同業 Forward P/E；KKR、APO 合併保險子公司，利潤率不能直接比，無法建立倍數錨"},"fwd_pe":19.93,"peg":1.28,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價對 FY2026 共識 19.9 倍、對 FY2027 約 16 倍，殖利率 4.4%，低於 104 週均線約 16%；5 年百分位事實表未涵蓋，無法確認歷史相對位置；FY2027 的 25%跳升依賴兌現回升，因此判為合理偏便宜，不到明確便宜","upside_short_pct":9.9,"upside_mid_pct":55.6},"trap_analysis":{"verdict":"🟡","label":"價值陷阱風險中等：產業估值下移與不動產募資萎縮兩項信號亮起"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2026-04 信用類募資年減 63%，非上市 BDC 贖回首度超過募資；BCRED 兩季只兌付約 50%；國會議員就私募信貸發函；Morningstar 指 AI 顛覆軟體公司與私募信貸疑慮同時壓抑類股","assumption":"私人財富通路的成長，建立在半流動結構可兌付與底層信用品質穩定之上","consequence":"5 年後虧 50%的故事：軟體類借款人在 AI 衝擊下違約上升，BCRED 長期限制贖回，零售信任崩落拖累 BREIT、BXPE 銷售，監管對零售產品設上限；高利率同時讓不動產與退出停滯，每股可分配盈餘回落到 5 美元、倍數壓到 12 倍。與唯一致命點同源","ruling":"部分採納：空頭機率上調至 30%。但 BCRED 借款人 EBITDA 雙位數成長、償債倍數 2.3 倍（Gray 3Q'26），信用事件尚無證據，不列為基本情境","watch":"BCRED 贖回申請與兌付比例、非應計放款比例（事實表未涵蓋）、監管正式提案","evidence_refs":["supply_demand_durability#1","customer_concentration_credit#0","regulatory_antitrust#1","substitute_technology#1"],"fact_refs":["f_kpi4_distributable_earnings_d"]},{"view":"論點成功但股東經濟變差","evidence":"10-K 稱對手願收較低費用或付較高分銷費，傳統資管自建私募平台；保險委託費率 40–50 基點；新成長多來自投資級私募信貸與多資產組合產品，費率較低","assumption":"AUM 成長能等比轉成費用與盈餘","consequence":"AUM 照 10%成長，但加權費率逐年下滑、費用相關獲利率停滯，每股盈餘成長落到 6–7%；股息又幾乎全額配發，股東報酬只剩殖利率加低個位數","ruling":"部分採納：Base 路徑 FY2029 後每股盈餘年增設 9%，不延續 15%；CFO 稱多資產部門費率已企穩，暫不再下修","watch":"基礎管理費年增與收費 AUM 年增的落差、費用相關獲利率","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","channel_business_model_shift#1"],"fact_refs":["f_kpi3_fee_related_earnings_fre"]},{"view":"價格已反映太多","evidence":"FY2027 共識每股 7.38 隱含年增 25%，FY2028 共識近一次下修 1.49%；AI 基建約占 AUM 7%，資料中心是最大成長主題；關稅與美中摩擦壓在實體商品組合公司","assumption":"市場已把 2027 年兌現回升與 AI 基建順風算進股價","consequence":"若 AI 資本支出轉弱或資金成本續升，資料中心估值與兌現同時延後，FY2027 落到 6.5 美元，表面上 16 倍的遠期倍數其實是 18 倍","ruling":"反駁為主：現價對 FY2026 為 19.9 倍、殖利率 4.4%，低於 104 週均線約 16%，股價沒有反映 2027 年跳升。但 FY2027 跳升是承重假設，Base 取 7.2，低於共識","watch":"FY2027／FY2028 共識修正方向、4Q'26 淨兌現、資料中心租賃量","evidence_refs":["substitute_technology#0","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":["f_consensus_eps_fy2","f_consensus_rev_fy3_pct","f_fwd_pe_latest","f_ma_w104"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 124.5 → 本次 117.97（-5.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=124.5","side_b":"本次 price_at_dd=117.97","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 衛星","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。矩陣輸入無可比對的前份值。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 124.5 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 124.5 美元：Bull 價 297、Bear 價 74，五年期望值 +76.0%，基準年化 12.5%，不對稱比 4.1","side_b":"本次情境、股價仍用 124.5 美元：Bull 價 295.2、Bear 價 91，五年期望值 +47.6%，基準年化 8.1%，不對稱比 4.25","ruling":"先換情境、股價不動：五年期望值少 28.4 個百分點，基準年化少 4.4 個百分點。不對稱比由 4.1 變為 4.25。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 124.5 美元：五年期望值 +47.6%，基準年化 8.1%，不對稱比 4.25","side_b":"本次情境、股價 117.97 美元：五年期望值 +55.7%，基準年化 9.2%，不對稱比 5.48","ruling":"再換股價、情境不動：起點價下跌 5.2%，五年期望值多 8.2 個百分點，基準年化多 1.2 個百分點，不對稱比由 4.25 升到 5.48。合計五年期望值比前份少 20.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"BCRED 贖回走勢：管理層說法與實際數字","cause":null,"prior_field":null,"side_a":"2026-07-23 Gray（2Q'26 法說）：第三季初 BCRED 贖回申請顯著下降","side_b":"2026-10-22 Gray（3Q'26 法說）：第三季贖回申請仍達 NAV 10%，高於 5%季度上限，兌付約 50%，淨流出 14 億美元（2Q'26 為 12 億）；歸因於 Q2 結轉","ruling":"不可調和，方向相反。採 B 側實際數字；管理層的結轉歸因不採信也不否定，標為未證、監測，預先登記：4Q'26 剔除結轉後新申請仍 >5% NAV，即視為歸因不成立。前份減碼條件「BCRED 贖回持續超過 5%上限」已技術性觸發，但淨流出僅約占私人財富 AUM 0.4%，本輪動作為停止加碼，不減碼","evidence_level":"管理層自述與公司揭露","settle_metric":"4Q'26 BCRED 新增贖回申請占 NAV（剔除結轉）","if_then":["若 4Q'26 新增申請 ≤5% NAV 且淨流出收斂 → 解除加碼凍結","若 4Q'26 新增申請 >5% NAV 且兌付 <50% → 減碼 1/2","若股價先跌但贖回數據改善 → 分批反買，不停損"],"evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2","supply_demand_durability#0","supply_demand_durability#3","end_markets#6"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"3Q'26 費用相關獲利年增僅 6%，分部可分配盈餘 19 億低於 2Q'26 的 22 億，FY2028 共識下修 1.49%；股價跌破 104 週均線，零售信用、不動產、AI 融資疑慮、監管四項利空並存，FY2027 的 25%跳升全押在兌現回升","side_b":"前九月費用收入與費用相關獲利皆年增 17%，基礎管理費創紀錄，四檔機構旗艦達硬頂；CFO 稱第四季僅合約中的附帶權益兌現就超過第三季全公司淨兌現；淨應計績效收入 72.6 億美元，年增 12%","ruling":"可調和，屬程度差異：賣方論點落在節奏、不在方向。不追高，現價分批；4Q'26 兌現未放量則停止加碼","evidence_level":"公司揭露與管理層指引","settle_metric":"4Q'26 淨獲利兌現、FY2027 基礎管理費年增","if_then":["若 4Q'26 淨兌現未高於 3Q'26 → 停止加碼，Base FY2027 每股下修至 6.8","若 4Q'26 淨兌現放量且 1Q'27 基礎管理費年增 ≥10% → 加碼至目標倉"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"管理層前季財測兌現","cause":null,"prior_field":null,"side_a":"2026-07-23 Chae（2Q'26 法說）：第三季基礎管理費年增與 Q2 相近、淨兌現環比放緩，2027 年回到雙位數；房地產基礎費明年穩定","side_b":"2026-10-22 Chae（3Q'26 法說）：淨兌現環比降 20%，如預告；重申 2027 年基礎管理費雙位數（全年對全年）；房地產基礎費至 2027 年大致穩定","ruling":"一致：財測兌現、未改口，提高 H1 與 H2 的可信度；唯一落差是 BCRED 贖回說法，另列一條","evidence_level":"逐字稿對照","settle_metric":"FY2027 基礎管理費年增","if_then":["若 1H'27 基礎管理費年增 <8% → 視為管理層財測失準，減碼 1/3"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：10-K 稱傳統資管自建私募平台、對手降費或加碼分銷費。其他結構變數：國會就私募信貸發函、AI 顛覆組合公司","side_b":"結構轉好：私募債募資 TTM 年增 14%，Preqin 預估 2030 年私募信貸 AUM 4.5 兆美元，401(k) 通路開啟，保險資金轉向投資級私募信貸","ruling":"雙向拉鋸：私人市場取代銀行與公開市場融資的結構順風，大於零售通路的費率競爭；監管是未定變數","evidence_level":"10-K、產業資料","settle_metric":"私人財富與保險 AUM 年增、基礎管理費年增與收費 AUM 年增的落差","if_then":["若監管正式提案限制零售半流動產品 → 減碼 1/3 並重估空頭機率"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","regulatory_antitrust#1","substitute_technology#0","end_markets#4","end_markets#5"]},{"axis":"情境機率與風險結論漂移","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct","trap","moat_trend"],"side_a":"前份（2026-07-24）：多頭機率 30%、空頭 25%；價值陷阱中等；護城河穩定","side_b":"本次：多頭 25%、空頭 30%；價值陷阱中等、護城河穩定，皆不變","ruling":"新證據：3Q'26 BCRED 贖回仍達 NAV 10%；不動產分部費用相關獲利年減 9%、AUM 年減 4%；第三季調高估值資本化率，BREP 機會型基金跌 3.2%。據此下修多頭、上調空頭。另共識兩年 CAGR 15.6%高於內生上界 11%，空頭不得低於 30%。陷阱與護城河方向在新證據下維持：保險 AUM 年增 14%、私人財富 15%，抵銷費率競爭","evidence_level":"公司揭露","settle_metric":"4Q'26 BCRED 贖回、不動產分部費用相關獲利","if_then":["若 4Q'26 BCRED 新申請 ≤5% NAV 且不動產費用相關獲利止跌 → 空頭機率回調至 25%"],"evidence_refs":["end_markets#0","customer_concentration_credit#1"]},{"axis":"估值與裁決欄位漂移","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份股價 124.5 美元，估值中性偏便宜","side_b":"本次 117.97 美元（−5.2%），Forward P/E 19.9 倍","ruling":"價格跌 5%，但 FY2026 共識僅上修 0.51%、FY2027 下修 0.14%，估值結論仍為中性偏便宜；綜合訊號維持同級；裁決與角色依本次輸入重算","evidence_level":"市場價格與共識快照","settle_metric":"股價對 FY2027 共識倍數","if_then":["若股價 ≤105 美元且 H1、H2 未削弱 → 分批加碼"],"evidence_refs":[]},{"axis":"回撤、類型、循環位置與跑道","cause":"方法變動","prior_field":["max_dd_pct","archetype","cycle_position","runway_post_y5"],"side_a":"前份最大回撤單點 −55%；類型品質複利成長；循環位置空白；五年後跑道寬","side_b":"本次最大回撤改為區間 −55%～−35%；類型、循環位置、跑道寬度不變","ruling":"方法變動：回撤由單點改區間，反映壓力年盈餘與恐慌倍數的不確定；其餘三欄經本次證據檢視不變。非循環股不設循環位置；個人投資人私人資產配置約 1%支撐跑道寬","evidence_level":"推估","settle_metric":"無","if_then":["若私人財富 AUM 年增連 4 季 <10% → 跑道下修一檔"],"evidence_refs":[]},{"axis":"加碼與減碼門檻改寫","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼＝回檔至 $105-112（貼 52 週低區）或 Credit 分部 DE YoY 轉正＋BCRED 贖回續降（確認 Q3 改善）＋Q4 realization 放量；減碼＝BCRED 贖回持續超 5% 上限惡化、或 Credit 分部 DE 連 2 季 YoY 下滑＋mark 減記擴大","side_b":"加碼＝4Q'26 淨兌現高於 3Q'26 且 BCRED 新增贖回 ≤5% NAV，或股價 ≤105；減碼＝BCRED 贖回連 2 季 ≥10% NAV 且兌付 <50%","ruling":"新證據：舊減碼條件「持續超過 5%上限」在 Q2、Q3 都已觸發（皆約 10%），但兩季申請者約 90 天拿回 75%資金（Gray 3Q'26），需區分結轉與新增壓力，故減碼門檻改為連 2 季 ≥10%且兌付 <50%；觸發後的動作是停止加碼，不放寬紀律。加碼價區收斂為 ≤105 美元（約 FY2027 共識 14 倍），並以 4Q'26 兌現放量取代 Credit 分部年增轉正，因 CFO 已給第四季兌現的具體量級","evidence_level":"管理層揭露","settle_metric":"4Q'26 淨兌現、BCRED 新增贖回","if_then":["若 4Q'26 兌現放量且 BCRED 新申請 ≤5% → 加碼","若 BCRED 連 2 季 ≥10%且兌付 <50% → 減碼 1/2"],"evidence_refs":["customer_concentration_credit#1","supply_demand_durability#0"]},{"axis":"減碼量化門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設量化減碼門檻（空白）","side_b":"本次設四條：BCRED 贖回申請連 2 季 ≥10% NAV 且兌付 <50%即減碼；FY2027 基礎管理費年增 <8%；4Q'26 淨兌現未高於 3Q'26；不動產分部費用相關獲利連 4 季年減 ≥5%","ruling":"方法變動：前份缺可量化的減碼門檻，本次補齊，對應 R1、H1、H2、R2","evidence_level":"方法","settle_metric":"各門檻指標","if_then":["任一門檻觸發 → 依觸發器表執行減碼或停止加碼"],"evidence_refs":[]},{"axis":"唯一致命點新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份 Single Thing 未設","side_b":"Single Thing：BCRED 宣布暫停贖回，或兌付比例跌破申請的 25%（事件型）→ 減碼至追蹤倉並重跑完整研究","ruling":"方法變動：前份未指定唯一致命點；本次以私人財富品牌信任為最大單一敏感度。BCRED 2025 年費用 12 億美元約占營收一成，暫停贖回會連帶壓抑 3,300 億美元私人財富通路的銷售","evidence_level":"公司揭露","settle_metric":"BCRED 兌付比例","if_then":["若 BCRED 暫停贖回 → 減碼至追蹤倉"],"evidence_refs":["customer_concentration_credit#0"]}],"triggers":[{"n":1,"text":"第四季獲利兌現放量驗證","type":"假設驗證","maps_to":"H2","metric":"季度淨獲利兌現","threshold":"4Q'26 高於 3Q'26","action":"達標→補足第二批；未達→停止加碼","source_freq":"季報新聞稿／每季","date":"2027-01"},{"n":2,"text":"BCRED 贖回壓力","type":"風險","maps_to":"R1","metric":"BCRED 季度贖回申請占 NAV 與兌付比例","threshold":"連 2 季 ≥10%且兌付 <50%","action":"減碼 1/2","source_freq":"季報法說、BCRED 公告／每季","date":null,"evidence_refs":["customer_concentration_credit#1","supply_demand_durability#0"]},{"n":3,"text":"BCRED 暫停贖回","type":"Single Thing","maps_to":"Single Thing","metric":"BCRED 兌付比例","threshold":"暫停贖回或兌付 <申請的 25%","action":"減碼至追蹤倉並重跑完整研究","source_freq":"BCRED 公告／即時","date":null},{"n":4,"text":"2027 年基礎管理費回到雙位數","type":"假設驗證","maps_to":"H1","metric":"基礎管理費年增率","threshold":"1H'27 年增 ≥10%；<8%為未達","action":"未達→減碼 1/3","source_freq":"季報新聞稿／每季","date":"2027-07"},{"n":5,"text":"估值加碼線","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤105 美元（約 FY2027 共識 14 倍）且 H1、H2 未削弱","action":"分批加碼至目標倉","source_freq":"每日收盤","date":null},{"n":6,"text":"不動產拖累延長","type":"風險","maps_to":"R2","metric":"Real Estate 分部費用相關獲利年增","threshold":"連 4 季 ≤ −5%","action":"停止加碼","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["end_markets#0"]},{"n":7,"text":"私募信貸監管收緊或大額罰款","type":"風險","maps_to":"R3","metric":"監管正式規則提案、單一罰款或和解金額","threshold":"零售半流動產品流動性或槓桿上限提案；或單筆 ≥5 億美元","action":"減碼 1/3 並重估空頭機率","source_freq":"SEC／國會公告、10-Q 訴訟附註／每季","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#2","lawsuit_class_action#0"]},{"n":8,"text":"費率競爭侵蝕","type":"減碼","maps_to":"R4","metric":"基礎管理費年增減收費 AUM 年增","threshold":"落後 ≥5pp 連 4 季","action":"減碼 1/3","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["competitive_share_entrants#1","channel_business_model_shift#1"]},{"n":9,"text":"4Q'26 財報後複審","type":"複審日期","maps_to":null,"metric":"全部假設與風險","threshold":"財報發布","action":"重跑判斷","source_freq":"一次","date":"2027-01-31"}],"kill_metrics":[{"metric":"BCRED 季度贖回申請占 NAV 與兌付比例","bear_threshold":"連 2 季 ≥10%且兌付 <50%","window":"至 2027-06","source":"季報法說、BCRED 公告","last_status":"warning"},{"metric":"基礎管理費年增率","bear_threshold":"FY2027 全年 <8%（指引為低雙位數）","window":"FY2027","source":"季報新聞稿","last_status":"unknown"},{"metric":"季度淨獲利兌現","bear_threshold":"4Q'26 未高於 3Q'26","window":"4Q'26 財報（2027-01）","source":"季報新聞稿","last_status":"unknown"},{"metric":"Real Estate 分部費用相關獲利年增","bear_threshold":"連 4 季 ≤ −5%","window":"至 3Q'27","source":"季報新聞稿","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","pacing":[],"requires_critic":[],"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把零售私募信貸贖回與 AI 融資疑慮套到整家公司；但 3Q'26 費用相關獲利仍年增 6%、約占可分配盈餘九成，近 12 個月流入逾 2,700 億美元為四年高點，四檔機構旗艦達硬頂，盈餘對兌現週期的依賴低於股價所反映"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade=None"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-1.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"holding_cap":null,"rearm_trigger":"加碼＝4Q'26 淨兌現高於 3Q'26 且 BCRED 新增贖回 ≤5% NAV，或股價 ≤105；減碼＝BCRED 贖回連 2 季 ≥10% NAV 且兌付 <50%","exec_line":"現價分批：首批為目標倉 1/2，4Q'26 財報（2027-01）確認兌現放量後補足；BCRED 兌付比例低於 50%期間停止加碼"},"reasoning":{"industry":"3Q'26 GAAP 營收 30.629 億美元、稅前利益 15.31 億，稅前利益率約 50%。費用相關獲利 15.721 億美元，約占可分配盈餘 17.157 億的 92%；以當季費用收入約 27 億美元（CFO 3Q'26 法說）推算，費用相關獲利率約 58%。分部營收：Private Equity 13.498 億（年減 6%）、Real Estate 8.933 億（年減 6%）、Credit & Insurance 7.839 億（年增 2%）、Multi-Asset 1.895 億（年增 25%）。以 GAAP 總營收為分母約 44%／29%／26%／6%，分部口徑與 GAAP 不完全相加。單點依賴：BCRED 2025 年貢獻管理與激勵費 12 億美元，約占全年營收 124.1 億的一成，是最大單一客戶，也是集中度風險。總 AUM 1.368 兆美元，當季流入 633 億。產業時鐘判 I：PitchBook 2Q26 私募資本募資 TTM 年減 12.7%，CFO 稱退出環境不易；但私募債募資年增 14%，BX 近 12 個月流入逾 2,700 億為四年高點，屬收縮後的復甦初段。供需耐久性：機構與保險需求屬結構性持久，今年四檔旗艦基金達硬頂、保險 AUM 年增 14%；零售信用類半流動產品需求屬週期性且可逆，2026-04 信用類募資年減 63%。","moat":"機制是四十年績效紀錄與品牌帶來跨資產類別的募資規模，再轉成永續資本與大額出資能力，換到更好的交易來源。執行面擴大：今年四檔機構旗艦基金達硬頂且都大於前期，保險客戶逾半數近 12 個月擴大合作。定價面縮減：10-K 指出私人財富與保險通路有對手收較低費用或付較高分銷費，保險委託費率僅 40–50 基點。兩者相抵，方向判穩定。當期 ROIC 無法計算，事實表未涵蓋投入資本口徑。FCF 利潤率 40.3% 高於 APO 26.4%、ARES 14.0%、BLK 12.9%、KKR 11.1%，但 KKR 與 APO 合併保險子公司，利潤率口徑不完全可比，不能據此宣稱同業報酬差距在擴大，評級因此停在 B。","growth":"成長以量為主：總 AUM 年增 10%，當季基礎管理費創紀錄。2027 年的驅動是新旗艦基金開始收費、永續策略擴張與信用保險；費率持平偏降；無併購貢獻，淨回購數據事實表未涵蓋。共識每股盈餘 FY2026 5.92、FY2027 7.38、FY2028 7.91，兩年 CAGR 約 15.6%；FY2025 同口徑基期事實表未涵蓋，無法算三年。內生上界約 11%（見護城河題代理推導），缺口約 4.6pp，歸因於績效收入與獲利兌現週期回升，屬獲利組合改善而非內生成長，須 4Q'26 兌現放量驗證。跑道：個人投資人私人資產配置約 1%，距 30%滲透率遠超過十年；401(k) 通路（Empower 合作、2025-10 成立退休方案部門）與投資級私募信貸是第二曲線。衰退信號亮 2 個：產業估值下移、不動產募資萎縮。","governance":"管理層政策是長期將現金盈餘 100%返還股東（2026-07-23 CFO），3Q'26 股息 1.12 美元約占每股可分配盈餘 1.32 的 85%，殖利率 4.4%。FCF 利潤率 40.3%，現金轉換無虞。公司層級無重大併購，近 12 個月 8-K 僅有優先債券發行。回購金額、均價與股權激勵稀釋率事實表未涵蓋，無法判斷回購是否在低價買進。","valuation":"現價 117.97 美元約當 FY2026 共識 19.9 倍、FY2027 約 16 倍，殖利率 4.4%。現價要求 FY2027 每股可分配盈餘回到 7 美元以上，之後約 9%成長，倍數不再下修；Base 情境 5 年價約 184 美元。我信大半：費用相關獲利已撐住九成盈餘，但 FY2027 的 25%跳升需要兌現回升。5 年估值百分位事實表未涵蓋。賣方均價 156 美元（27 位）、最低 122 美元（Wells Fargo 10 月新覆蓋），現價低於最低目標；全距 1.6 倍，未超過 2.5 倍警戒。PEG 約 1.28（19.9 倍÷兩年 CAGR 15.6%）。","premortem":"三視角見反證紀錄。衰退信號亮 2 個，價值陷阱風險中等。FY2028 共識近一次下修 1.49%，26 週報酬 −1.1%，市場仍在觀望兌現回升。"},"plain":{"six":{"how_it_makes_money":"向機構、保險公司與高資產個人收管理費與績效分成；錢卡在「募資通路＋投資績效」這一節點","moat":"護城河穩定：規模與品牌帶來募資優勢，零售通路的費率競爭與之相抵","growth":"成長跑道寬：私人財富與保險通路滲透率低，2027 年基礎管理費可望回到雙位數","capital":"股東回報以高配息為主，紀律清楚，但回購與稀釋數據有缺口","valuation":"現價要求 FY2027 盈餘回到 7 美元以上、倍數不再下修；我大致相信，估值屬中性偏便宜","how_wrong":"最可能看錯在零售私募信貸贖回擴散與不動產拖累延長"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把零售私募信貸贖回與 AI 融資疑慮套到整家公司；但 3Q'26 費用相關獲利仍年增 6%、約占可分配盈餘九成，近 12 個月流入逾 2,700 億美元為四年高點，四檔機構旗艦達硬頂，盈餘對兌現週期的依賴低於股價所反映","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":null,"archetype":"品質複利成長","price_at_dd":117.97,"week26_return_pct":-1.13,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 屬兌現偏低年度（第三季淨兌現環比降 20%），分母偏保守、未灌水；爭點在 FY2027 的跳升，便宜論證不依賴 FY2027"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"4Q'26 財報：獲利兌現放量與 2027 年基礎管理費指引","impact":"高","watch":"淨兌現是否高於 3Q'26、BCRED 第四季贖回申請"},{"date":"2027-01","date_precision":"month","type":"other","event":"多資產與信用類策略年末績效收入結算","impact":"中","watch":"費用相關績效收入年增"},{"date":"2027-05","date_precision":"month","type":"regulatory","event":"TXNM Energy 收購待 NRC 與新墨西哥 PRC 核准，終止日 2027-05-31","impact":"低","watch":"監管核准進度"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,375B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BX_20261024/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭　§5.R　§5.F</h2>
<p class="lead">規模與品牌優勢擴大，定價權縮減，兩者相抵判為穩定，評級 B。</p>
<ul class="pts">
<li>護城河的機制是品牌與長期績效，帶來跨資產類別的旗艦基金募資規模，再轉成永續資本與大額出資能力，最後換到更好的交易來源與承作條件。這個循環的證據是今年四檔機構旗艦基金都達硬頂，且規模皆大於前期，近 12 個月流入逾 2,700 億美元。</li>
<li>執行面給 9 分，定價面給 7 分，綜合 8.0。執行面高是因為募資、交易來源與保險客戶續約都在擴大。定價面較低是因為 10-K 稱私人財富與保險通路有對手願收較低費用，或付較高分銷費，保險委託費率只有 40–50 基點。</li>
<li>趨勢判為持平。執行面擴大與定價面縮減相抵，所以不判上升也不判下降。若基礎管理費年增落後收費 AUM 年增 ≥5pp 連 4 季，才表示定價面的縮減開始壓過執行面，那時要減碼 1/3。</li>
<li>當期 ROIC 無法計算，事實表沒有涵蓋投入資本口徑。FCF 利潤率 40.3% 高於 APO 的 26.4%、ARES 的 14.0%、BLK 的 12.9%、KKR 的 11.1%。但 KKR 與 APO 合併保險子公司，利潤率口徑不可直接比較，不能據此宣稱同業報酬差距在擴大。</li>
<li>KKR 走自有保險公司路線，利潤率被保險業務稀釋，在保險資金爭奪上是直接對手。APO 同樣有自有保險平台，是投資級私募信貸最直接的對手，Gray 稱這個領域主要是自家與少數同業競爭。ARES 以直接放款為核心，零售 BDC 與 BCRED 正面競爭。BLK 是自建私募平台的傳統資管，威脅集中在私人財富通路。</li>
<li>三項威脅各有機率。傳統資管搶零售與保險資金，機率 35%。AI 顛覆組合公司，軟體約占公司曝險 6%，機率 25%。監管對零售半流動產品加限制，機率 30%。三項都是中度，沒有一項單獨足以推翻護城河。</li>
<li>報酬持續期要看四個檢查點。需求基礎值中、決策層級強、價值鏈分配中、社會容忍度中。資產輕型且盈餘近全額配發，再投資率趨近 0，股東報酬主要來自配息與盈餘成長，不是來自再投資的複利。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<!-- E7 -->
</section>

```