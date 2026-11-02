你是 stock-analyst v20 的**散文層（prose）agent**，標的 EBAY（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EBAY_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：EBAY　日期：2026-11-03　archetype：None　前份裁決：2026-05-16　觀望（B，thesis 完整但估值偏貴+MA stretched，QC-22 漂移 +13.3% 追高警示）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2190B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（641B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（867B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1322B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1220B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（1129B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1391B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2162B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3413B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2301B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2190           3367-4810      3 條（2–6 內）  
s3                  8000         641           5151-7359      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3409          8114-11591      5 條（2–6 內）  
s6                 11000        1129           6910-9871      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1391           1476-2109      3 條（2–6 內）  
s10                 5000        2162           1987-2838      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2301           2000-2699      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5440B；至少需散文≈39.56KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−48%
−45%
−45
−40%
−39%
−33%
−28
−28%
0
0%
0.31
0.71
0.75
0.8
0.9
0.99
1
1%
01
1.0%
1.3%
1.3
1.38
1.5
1.5%
1.65
1.69
1.73
02
2%
2
2.04
2.1%
2.4
2.4%
2.7%
3
3%
03
3.1
3.3
3.7
4
04
4%
4.3
4.34
4.4%
4.5%
4.72
5%
5
05
5.3%
5.4
5.4%
5.75
5.9%
6%
6
6.07
6.2
6.25
6.4
6.6
6.8
6.80
6.88
6.9
7%
7
07
7.2%
7.45
7.49
7.5
7.5%
7.81
7.95
8
8%
08
8.10
8.1
8.3
8.3%
8.5%
8.75
8.95
9
9%
9.4
9.40
10%
10
11%
11
11.1
11.4
11.74
11.8%
12
12%
12.4%
12.69
12.9%
13
13%
13.8%
13.84%
14%
14
14.03%
14.5
15%
15
16
16%
16.9%
17.6
18
18.7%
19%
19
19.2%
19.4
19.42
19.5%
19.7%
20
20%
20.2%
21%
22%
23
23.9
24%
24
24.1%
25
25%
25.7
26
26%
26.2%
26.3%
26.5
27
27.67
28%
28
30
30%
31
32.06
33
35%
35.3%
40%
42
42.7%
47%
48%
49
50%
50
52%
52
60
60%
62.8
67
70
72%
72.6%
73.1%
74
74.1%
75
80
80%
81.6
82
85%
87.3
90
100%
100
100.6
104
105
106
110
113
116.13
121
121.4
122
125
126.5
130
135.5
150%
150
162
222
231.66
250
400
410
439
444
533
800
2022
2023
2024
2025
2026
2027
2028
20261103
1,600
2,000
3,700
5,900
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
{"meta":{"ticker":"EBAY","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"eBay Inc."},"oneliner":"eBay 靠收藏品、C2C 與 eBay Live 把有機 GMV 拉到雙位數，Q3 全面超過財測；但抽成率下滑、2027 年交易卡面臨高基期，前瞻本益比 19.4 倍已反映成長延續，基準情境五年年化不到 8%，等 100 美元以下再進場。","thesis":{"H":[{"id":"H1","text":"交易卡退燒後，有機 GMV 仍能維持中個位數以上的成長：聚焦品類、C2C、eBay Live 的結構性成長足以抵銷收藏品高基期。","2y":"FY2027 有機 FX 中性 GMV（不含 Depop）年增 ≥5%；聚焦品類加 C2C 加二手占 GMV 維持 ≥72%","5y":null,"10y":null,"threshold":"FY2027 有機 FX 中性 GMV 年增 ≥5%（Q3 2026 為 13%，Q4 指引 8–10%）","source":"季報新聞稿與法說會（有機 FX 中性 GMV、策略重點占比）","drift_rule":"以單季有機 GMV 年增對照 5% 門檻：連 2 季低於 5% 為削弱；連 3 季低於 3% 為反轉，並啟動唯一致命點檢查"},{"id":"H2","text":"AI 代理與搜尋入口的變化，對 eBay 是增量而不是繞過：非新品長尾庫存、信任機制與自然流量讓 eBay 保住買家入口。","2y":"自然流量占比維持 ≥80%（目前 85%）；AI 轉介新買家中，之後直接回 eBay 購買的比例（目前約一半）不下降","5y":"FY2031 前 GMV 五年年複合 ≥4%，且未出現主要 AI 代理繞過 eBay 直接成交的情況","10y":null,"threshold":"自然流量占比 ≥80%；五年 GMV 年複合 ≥4%","source":"法說會管理層揭露（自然流量占比、AI 轉介買家回訪）；10-K 風險因子更新","drift_rule":"自然流量占比跨 2 個年度下降為削弱；跌破 80%，或主要 AI 代理與 Amazon／Walmart 簽交易介面而 eBay 缺席，為反轉"},{"id":"H3","text":"股東經濟守得住：抽成率下滑由廣告與費用紀律補回，非 GAAP 營益率維持 25% 以上，加上每年約 2.4% 淨回購，每股盈餘年增 8–9%。","2y":"FY2027 非 GAAP 營益率 ≥25%（Q3 2026 為 26.3%，Q4 指引 25.7–26.2%）","5y":"FY2030 流通股數 ≤400 百萬股（目前 439 百萬）；非 GAAP 營益率五年平均 ≥25%","10y":null,"threshold":"非 GAAP 營益率 ≥25%；流通股數每年淨減 ≥2%","source":"季報新聞稿、10-Q／10-K 股數","drift_rule":"營益率連 4 季低於 25% 為削弱，連 6 季低於 24% 為反轉；股數年減連 2 年低於 1.5% 為削弱"}],"R":[{"id":"R1","text":"收藏品（交易卡）高基期反轉：2026 年交易卡與金銀條異常強，2027 年對比基期時有機 GMV 掉速過快。","h_ref":"H1","clock":"⚡","threshold":"單季有機 FX 中性 GMV 年增 <3%，且管理層把主因歸給收藏品","evidence_refs":["supply_demand_durability#0"]},{"id":"R2","text":"抽成率與費用雙重壓力：eBay Live、C2C、Depop、車輛這些低抽成業務長得越來越快，Depop 的行銷與運費補貼又在加碼，9% 裁員顯示成本得重新騰挪；GMV 成長轉不成營業利益。","h_ref":"H3","clock":"🔥","threshold":"抽成率連 4 季年減 ≥30 個基點，且非 GAAP 營益率低於 25%","evidence_refs":["channel_business_model_shift#2","end_markets#3"]},{"id":"R3","text":"AI 代理與搜尋入口分流：Google 演算法調整、LLM 購物代理成為買家入口，eBay 淪為後端庫存供應方，議價權轉到導流方手上。","h_ref":"H2","clock":"🐢","threshold":"主觀機率 ≥50% 才砍倉；硬條件是自然流量占比跌破 80%，或主要 AI 代理與 Amazon／Walmart 簽交易介面而 eBay 缺席","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#2","competitive_share_entrants#0"]},{"id":"R4","text":"跨境貿易與關稅：美國 2025 年取消 800 美元免稅額；歐盟 2026 年 7 月取消 150 歐元免稅額並每件收 3 歐元，英國預期跟進。跨境是重要利潤來源，大中華區賣家幾乎只做跨境；制裁與出口管制的合規責任也在升高。","h_ref":"H1","clock":"🔥","threshold":"國際有機 FX 中性 GMV 連 2 季年減（Q3 2026 為 +4%）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#4","geo_supply_chain#0"]},{"id":"R5","text":"Depop 整合與監管：英國 CMA 調查 Depop 收購；服飾 C2C 對手 Vinted 在英國占 50–60%，並在美國擴張。Depop 若成長放緩，2028 年轉為增益的承諾會落空。","h_ref":"H3","clock":"🔥","threshold":"CMA 要求出售或附重大條件；或 Depop 美國 GMV 年增連 2 季低於 30%","evidence_refs":["regulatory_antitrust#1","competitive_share_entrants#2"]},{"id":"R6","text":"法律與平台責任：違規刊登責任（2024 年 DOJ 和解付 5,900 萬美元並強化監控）、常態性的集體訴訟與政府調查，以及排定 2027-01-04 開庭的 Steiner 跟蹤騷擾民事案。","h_ref":"H3","clock":"🐢","threshold":"單一案件和解或判決金額超過一季 FCF 的一半（約 3.7 億美元），或出現刑事追訴","evidence_refs":["regulatory_antitrust#0","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1"]}],"single_thing":{"description":"2027 年任一季，有機 FX 中性 GMV（不含 Depop）年增跌破 3%，且管理層把主因歸給收藏品（交易卡）轉弱。","why_fatal":"有機 GMV 增速是本次 EPS 路徑最大的單一敏感項，收藏品又是最大的成長來源。基準情境需要 2027 年有機 GMV 5–7%；若跌到 3% 以下，扣掉抽成率下滑後營收幾乎不長，EPS 只剩回購撐起的低個位數成長。市場會回到營收只成長 2–3% 那幾年的倍數，熊市情境的 12 倍落地，股價約 75–80 美元。","if_happens":"未持有：取消 100 美元的進場價條件，重跑研究。已持有：清倉，不等下一季。","how_monitor":"每季財報新聞稿的有機 FX 中性 GMV，以及法說會對收藏品與交易卡的敘述；下一個檢查點是 2027 年 2 月的 Q4 財報與 2027 年財測。交易卡二級市場價格事實表未涵蓋。","probability":"約 25%（12–24 個月）。2026 年交易卡基期異常高，管理層也已預告放緩；但聚焦品類、C2C、eBay Live 都在兩位數以上成長，可以墊住大部分缺口。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":17.6,"peg_fy2":1.5,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":6.25,"FY2027E":6.88,"FY2028E":7.81},"fy_end_month":12,"eps_basis":"共識為 Koyfin 快照的非 GAAP 稀釋 EPS（2026-10-31），財年止於 12 月。FY2025 非 GAAP 實際 EPS 事實表未涵蓋（只有 GAAP 4.34 美元，含投資損益，口徑不同），基期留空；三年年複合改以 FY2026→FY2028 兩年 11.8% 代替。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EBAY_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"毛利率七成以上、營益率約二成、FCF 九成以上配回股東；營收 2023–24 年只成長 2–3%，2025 年 8%，2026 年轉為雙位數；2026-05 另收到 GameStop 不具約束力的收購提案"},"industry":{"clock_phase":"II","sd_verdict_source":"一半結構、一半週期：二手與 C2C 滲透上升屬結構性（聚焦品類加 C2C 加二手占 GMV 72%、年增約 20%）；交易卡與金銀條熱潮屬週期性，管理層 2026-05 稱金銀條是暫時助力，2026-10-28 稱 2027 年交易卡增速會自然放緩。","bargaining":{"up":"供給方是數百萬中小賣家，個別議價力弱，但多平台刊登很普遍；真正的上游是導流（Google 搜尋與 AI 代理）。10-K 自述 Google 演算法調整曾減少導流，eBay 在這一環議價力弱。","down":"買家高度分散，2023–25 年無單一客戶超過營收 10%；熱衷型買家黏著度高（平均每天造訪一次以上），一般買家的比價成本則很低。","geo":"FY2025 美國 52%、國際 48%。跨境（含大中華賣家）是重要利潤來源；美國 2025 年取消 800 美元免稅額，歐盟 2026 年 7 月取消 150 歐元免稅額，跨境成本上升。"},"profit_pool_dir":"二手、收藏品與高價品的利潤池往有鑑定與買家保障的平台集中（公司稱在美國與英國二手精品領先，TCGplayer 年 GMV 破 10 億美元）；平價服飾 C2C 則流向免賣家費模式（英國 CMA 估計 Vinted 占 50–60%）。","tam_table":{"expanded":false,"reason":"事實表沒有二手轉售、收藏品或 C2C 的可比 TAM，也沒有 eBay 份額的時序。現有的只有全球電商總量（二手網站轉述 eMarketer）和管理層口述（家戶閒置物品不到兩成上線），拼成一張表會混用不同口徑。本次論點的承重在有機 GMV 增速與抽成率，改在成長題用分部增速處理，不靠 TAM 外推。"}},"moat":{"mechanism":"二手與收藏品長尾庫存的深度（近 27 億件刊登），加上信任基礎設施（真品保證、PSA／PCGS 鑑定、買家與車輛保障），形成雙邊網路效應；熱衷型買家每天造訪一次以上，貢獻七成 GMV。","execution":8,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行力擴大：聚焦品類 GMV +24%、美國熱衷買家 +9%、eBay Live 年化 GMV 達數十億美元且三位數成長。定價力略縮：抽成率年減約 20 個基點，法國、義大利改為免費賣。英國服飾 C2C 份額流向 Vinted（CMA 估計）。一升一降，方向判穩定。","peer_na_reason":"事實表的同業資料只有毛利率、營益率、FCF 利潤率與研發密度的單期 TTM，沒有同業 ROIC 與歷年差距，改用營益率差代替；直接對手 Vinted 不在同業財務表內。","threats":[{"level":"🔴","text":"AI 代理與搜尋入口控制前端導流。10-K 自述依賴 Google 搜尋、演算法調整曾減少導流，AI 轉介不足可能讓買賣家轉向；分析師認為 LLM 代理可能讓市集淪為後端履約。目前 AI 轉介流量「非常小」、85% 為自然流量，屬尚未發生的生態攻擊。","p":"30%（五年內）","evidence_refs":["competitive_share_entrants#1","substitute_technology#2","substitute_technology#0"]},{"level":"🟡","text":"服飾 C2C 的免賣家費對手。英國 CMA 估計 Vinted 占英國 C2C 服飾 GMV 50–60%，eBay 與 Depop 都在流失份額；Vinted 正在美國擴張。eBay 以 Depop 加免費賣回應，屬點對點競爭；英國 CMA 同時在調查 Depop 收購。","p":"英國已發生；美國擴大的機率約 40%","evidence_refs":["competitive_share_entrants#2","regulatory_antitrust#1"]},{"level":"🟡","text":"進入門檻低，專業平台搶聚焦品類。10-K 自述對手用現成軟體就能低成本開站，專業型對手在直播、收藏卡這類品類可能比 eBay 更快滿足社群需求。","p":"25%","evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉率為推定，事實表未涵蓋投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"買家、決策者、付款者是同一人，三個角色都成立。但收藏品與精品屬於可延後的「想要」，2026 年交易卡與金銀條熱潮有週期成分。賣家端「把閒置變現」是持續需求：公司調查稱約 85% 賣家的二手貨來自自己的物品（自家調查，打折採用）。"},{"item":"決策層級","level":"🟡","text":"替代性要在單筆交易層衡量。一般二手品的買家比價切換成本低，賣家多平台刊登普遍；高價收藏品與精品則因真品保證、PSA／PCGS 鑑定與保管、TCGplayer 與 Goldin 的成交價資料而難以替代。可觀察的代理變數：熱衷型買家每天造訪一次以上、貢獻七成 GMV；漲價後的流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"一筆交易的價值分給賣家、平台（抽成約 13.8%，加廣告約 2.7%）、物流承運商與導流入口。eBay 最難被取代的是信任與撮合，最容易被分走的是前端導流：若 AI 代理成為買家入口，導流方會向平台要分潤。目前 85% 自然流量讓 eBay 保有分配權。"},{"item":"社會容忍度","level":"🟢","text":"優勢不依賴監管授權。主要政策風險是違規刊登責任（2024 年與 DOJ 和解，付 5,900 萬美元並強化監控）與跨境免稅額取消。抽成水準本身未見社會或監管壓力，eBay 在 C2C 反而主動降費。"}],"roiic":"事實表未涵蓋（缺投入資本與增量營業利益的對應數字）","reinvest_rate":"常態年約一成以內（管理層框架是正常年度把 90–100% 正常化 FCF 配回股東）；2026 年因 14 億美元現金收購 Depop 而明顯偏高","endo_ceiling":7.5,"formula_note":"內生成長＝增量 ROIC × 再投資率。增量 ROIC 取不到，以輕資產平台的高檔 50% 推估；再投資率取一成，資本化再投資帶來的內生營業利益成長上界約 5%。eBay 的成長投資多數走費用（行銷，以及記為營收減項的運費補貼），不進投入資本，這條公式會低估真實上界。再加每年約 2.4% 的淨回購，每股盈餘內生上界取 7.5%。這是推定值，不是事實表數字。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","EBAY":72.81,"ETSY":72.62,"AMZN":50.01,"MELI":42.68,"unit":"%"},{"metric":"營業利益率","EBAY":20.2,"ETSY":16.91,"AMZN":12.36,"MELI":8.26,"unit":"%"},{"metric":"FCF 利潤率","EBAY":19.46,"ETSY":19.65,"AMZN":-0.82,"MELI":35.27,"unit":"%"},{"metric":"研發密度","EBAY":15.23,"ETSY":14.8,"AMZN":null,"MELI":7.33,"unit":"%"}],"competitors":[{"name":"ETSY","gm":72.62,"om":16.91,"fcf_margin":19.65,"rd_intensity":14.8,"strategy_note":"利潤結構與 eBay 幾乎相同（毛利率 72.6%、營益率 16.9%），已把 Depop 賣給 eBay、收縮回手作與獨特品，在二手時尚與 eBay 的正面競爭變少。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"AMZN","gm":50.01,"om":12.36,"fcf_margin":-0.82,"rd_intensity":null,"strategy_note":"新品與自建物流巨頭，營益率 12.4%、FCF 利潤率為負，正在大舉投資；對 eBay 的威脅集中在翻新電子與汽車零件，非新品收藏品不是它的主戰場。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"MELI","gm":42.68,"om":8.26,"fcf_margin":35.27,"rd_intensity":7.33,"strategy_note":"拉美電商加金融生態系，與 eBay 的地理市場幾乎不重疊，只拿來對照結構：毛利率 42.7%、營益率 8.3%，但 FCF 利潤率 35.3%。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（件數與 ASP 組合，管理層稱平衡但未量化）；價為負（抽成率年減約 20 個基點）；併購加分（Depop 約貢獻 GMV 3 個百分點、營收 2 個百分點）；每股另有每年約 2.4% 的淨回購。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河題的報酬持續期推導：增量 ROIC 取不到，以 50% 推定，再投資率一成，內生營業利益成長約 5%；加淨回購約 2.4% 後，每股上界 7.5%。費用化的成長投資使這個公式偏低。","segments":[{"item":"聚焦品類（收藏品、汽車零件與車輛、時尚、翻新品）","value":"Q3 GMV +24%，比其他品類快 19 個百分點；收藏品是最大成長來源，美國收藏品因高基期溫和放緩"},{"item":"C2C","value":"全球 GMV 年增逾 20%；法國、義大利 9 月起免費賣"},{"item":"eBay Live","value":"年化 GMV 數十億美元、年增三位數；公司稱直播賣家在核心市集的 GMV 約為直播 GMV 的兩倍；抽成率低於核心市集"},{"item":"車輛","value":"Q3 年增三位數；高單價、低抽成"},{"item":"Depop","value":"7 月 30 日以 14 億美元現金完成收購；Q3 美國 GMV、月活、成交件數年增逾一倍；Q4 指引對 GMV 成長貢獻 4 個百分點、營收 2 個百分點；管理層稱 2028 年對合併非 GAAP 營業利益轉為增益"},{"item":"廣告","value":"Q3 6.07 億美元、年增 16%；第一方廣告 5.75 億美元；約占 GMV 2.7%"},{"item":"地理","value":"美國有機 GMV +22%；國際有機 +4%，德國消費環境疲弱"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q3 非 GAAP 毛利率 73.1%、年增 60 個基點；但比 Q2 的 74.1% 季減 1 點，需留意"},{"item":"核心市占近 12 個月縮減","lit":true,"note":"英國服飾 C2C 份額流向 Vinted（CMA 估計）；屬單一品類，不是整體市集"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"沒有提價；C2C 反而降費"},{"item":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":false,"note":"共識 FY2027 EPS +10%、營收 +7.2%，差約 3 個百分點"},{"item":"FCF／淨利 <0.75 連 2 年","lit":false,"note":"FY2025 約 0.71、FY2024 約 0.99，不連續；GAAP 淨利受投資損益扭曲"},{"item":"SBC／營收 >5% 且逐年上升","lit":null,"note":"Q3 SBC 1.73 億美元，占營收 5.4%，已超過 5%；歷年趨勢事實表未涵蓋，無法確認是否上升"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"AI 代理是潛在替代，但尚未看到 GMV 受損"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"eBay 自身倍數在近四年高點"},{"item":"維護性資本支出占 FCF >60%","lit":null,"note":"事實表未涵蓋資本支出拆分"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"營收連續成長"}]},"quality":{},"governance":{"capital_returns":[{"item":"回購","value":"2026 年目標約 20 億美元；Q2 3.1 億美元、Q3 約 6.9 億美元（均價約 106 美元）"},{"item":"股利","value":"每季每股 0.31 美元，Q3 支出 1.38 億美元；TTM 殖利率約 1.0%"},{"item":"併購","value":"Depop 14 億美元現金（2026-07-30 完成），另有 Tise；英國 CMA 已對 Depop 收購展開調查"},{"item":"配回框架","value":"正常年度把 90–100% 正常化 FCF 以回購加股利配回，有內生或併購用途時除外（2026-10-28 法說會，CFO）"},{"item":"資產負債","value":"現金與固定收益投資 33 億美元、總債務 67 億美元、股權投資 8 億美元；淨負債約 52 億美元（含租賃）"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Depop 14 億美元（2026-07-30 完成）；Q2 法說會預告拖累 Q3 營業利益成長 3–4 個百分點，管理層稱 2028 年才轉為增益，目前已實現報酬低於資金成本","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"Q3 回購均價約 106 美元，對 FY2026 共識 EPS 6.25 美元的盈餘殖利率約 5.9%；十年期公債殖利率事實表未涵蓋，無法對照門檻","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 1.73 億美元，年化約 6.9 億美元，約為市值 533 億美元的 1.3%，低於 1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2026 共識非 GAAP EPS 6.25 美元）為主尺，FY2027 的 17.6 倍作對照；trailing GAAP 倍數只看歷史位置","tier":"成熟市集平台","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有 ETSY、AMZN、MELI 的前瞻本益比，無法做倍數對照；終端倍數改用公司自身的成長熄火情境定錨。"},"fwd_pe":19.42,"peg":1.65,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"前瞻本益比 19.4 倍、PEG 1.65 都屬合理區，但 trailing 本益比、P/S、EV/S 全在近四個年度端點的最高位；基準情境五年年化報酬約 5–6%（含股息），低於 8% 的及格線；Q3 前的賣方平均目標價約 110–113 美元，低於現價。合理但不便宜，偏貴一檔。","upside_short_pct":0.8,"upside_mid_pct":23.9},"trap_analysis":{"verdict":"🟡","label":"成長延續但價格偏滿"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q1 2026 管理層稱金銀條是暫時助力；Q4 指引有機 GMV 8–10%，已內含對 2025 年 Q4 交易卡與金銀條強勢的高基期；2027 年規劃假設交易卡增速自然放緩；扣除 Depop 與 Tise，活躍買家只 +1%。","assumption":"收藏品熱度是結構性的，2027 年核心有機 GMV 仍有 5% 以上。","consequence":"有機 GMV 回到 0–2%，EPS 五年年複合不到 2%，倍數回到 12 倍，五年後股價約 82 美元，較現價 −33%；若同時出現 AI 入口分流，跌幅擴大到 −40% 以上。","ruling":"部分採納。交易卡高基期是真的，但聚焦品類的其他項目（汽車、時尚、翻新品）、C2C、eBay Live 都在兩位數以上成長，單靠交易卡退燒不足以把有機 GMV 壓到 3% 以下。熊市給 30% 機率，與唯一致命點是同一個故事。","watch":"每季有機 FX 中性 GMV 與收藏品敘述；扣除併購後的活躍買家成長率。","evidence_refs":["supply_demand_durability#0","competitive_share_entrants#1","substitute_technology#2"],"fact_refs":["f_kpi7_gmv","f_kpi8_active_buyers","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 抽成率 13.84%（去年同期 14.03%），原因是 eBay Live、C2C 與品類組合；Q4 指引 GMV 合併 FX 中性 +12–14%，營收只有 +7–9%，非 GAAP 營業利益 +6–10%；10 月宣布裁員約 9%、重組費用 1.3–1.5 億美元；跨境免稅額取消，跨境運費與合規成本上升。","assumption":"GMV 成長會等比例轉成營收與每股盈餘。","consequence":"GMV 年增 8% 但營收只長 5%，營益率又被 Depop 行銷與運費補貼吃掉，EPS 年增落到 5–6%。就算 GMV 論點成立，五年報酬也只剩股息加回購。","ruling":"採納為主要的中期風險。管理層明說挑業務看營業利益金額、不看抽成率，代表抽成率會繼續降；守門指標設在非 GAAP 營益率，連 2 季低於 24% 就減碼。","watch":"抽成率年變動、非 GAAP 營益率、Depop 對營業利益的拖累幅度。","evidence_refs":["end_markets#3","channel_business_model_shift#2","reg_tariff_export#0","reg_tariff_export#2"],"fact_refs":["f_kpi1_non_gaap_operating_incom","f_kpi0_revenue_gaap","f_kpi7_gmv"]},{"view":"價格已反映太多","evidence":"trailing 本益比 26.5 倍、P/S 4.3 倍、EV/S 4.72 倍，都在可得年度端點的最高位；前瞻本益比 19.4 倍；Q3 財報前的賣方平均目標價約 110–113 美元，低於現價。GameStop 2026-05 提出不具約束力的收購提案（每股約 125 美元出自搜尋摘要，待核），股價可能含收購題材。","assumption":"市場會繼續給接近 19 倍的前瞻本益比。","consequence":"EPS 照基準情境走、倍數回到 16 倍，五年價格報酬約 +24%，年化約 4.4%，加股息不到 6%；收購題材若消失，短期還會再少一截。","ruling":"採納。生意好，價格偏滿，不追價；等 100 美元以下（約 FY2027 共識 EPS 14.5 倍），基準情境年化才接近一成。","watch":"股價對 FY2027 共識 EPS 的倍數；GameStop 提案的後續（最新進度事實表未涵蓋）。","evidence_refs":["capital_markets_pricing#1","major_events#0"],"fact_refs":["f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_fwd_pe_latest","f_price_at_dd"]},{"view":"論點失敗","evidence":"英國 CMA 調查 Depop 收購；2024 年 DOJ 和解付 5,900 萬美元並強化違規刊登監控；10-K 稱公司常態面臨集體訴訟與政府調查；Steiner 民事案和解破裂，排定 2027-01-04 開庭；客戶規避制裁與出口管制的風險，平台要承擔部分合規責任。","assumption":"法律與監管成本維持在可吸收的範圍。","consequence":"CMA 若要求出售 Depop，第二條曲線少一條；若單一案件金額吃掉一季 FCF 的一半，資本回報要縮。","ruling":"反駁其為致命風險。已知金額（5,900 萬美元）相對一季 FCF 7.49 億美元很小；Steiner 案是個案民事訴訟，刑事部分已在 2024 年以延後起訴協議處理；CMA 結果列為觸發器。","watch":"CMA 調查結論；Steiner 案判決或和解金額。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1","reg_tariff_export#3"],"fact_refs":["f_kpi3_free_cash_flow_continuin"]}],"max_dd":{"lo":-45,"hi":-28,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 116.13 → 本次 121.4（+4.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=116.13","side_b":"本次 price_at_dd=121.4","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 116.13 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 116.13 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 116.13 美元：Bull 價 222、Bear 價 81.6，五年期望值 +24.1%，基準年化 5.3%，不對稱比 2.04","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.04。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 116.13 美元：五年期望值 +24.1%，基準年化 5.3%，不對稱比 2.04","side_b":"本次情境、股價 121.4 美元：五年期望值 +18.7%，基準年化 4.4%，不對稱比 1.69","ruling":"再換股價、情境不動：起點價上漲 4.5%，五年期望值少 5.4 個百分點，基準年化少 0.9 個百分點，不對稱比由 2.04 降到 1.69。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"AI 代理是增量還是繞過","cause":null,"prior_field":null,"side_a":"管理層（2026-10-28 法說會，CEO）：AI 轉介流量目前非常小，但帶進新買家與回流買家的比例高於其他管道，約一半新買家之後直接回 eBay 購買；85% 流量是自然流量；非新品長尾庫存讓 eBay 成為 AI 的最大受益者之一。","side_b":"10-K 自述依賴 Google 搜尋導流、演算法調整曾減少導流，AI 轉介不足會讓買賣家轉向；分析師（Retail Dive，2026-02）認為 LLM 代理可能讓市集淪為後端履約；eBay 2026 年 1 月更新條款、禁止未授權的代購代理，顯示公司自己也把它當威脅。","ruling":"不可調和（方向相反）。裁定兩年內採管理層這一邊，依據是 85% 自然流量與每天造訪一次以上的熱衷型買家，這些都不經過代理；五年以上不下結論，列為長期風險、給 30% 機率。","evidence_level":"管理層數字可驗證（自然流量占比）；分析師一方是推論，沒有 GMV 受損的數據。","settle_metric":"自然流量占比；AI 轉介新買家的回訪率；主要 AI 代理與市集簽交易介面的名單","if_then":["若 eBay 揭露自然流量占比跌破 80%，或主要 AI 代理與 Amazon／Walmart 簽交易介面而 eBay 缺席：已持有者減碼一半，熊市機率上調到 40%","反向：若 eBay 與主要 AI 代理簽交易介面，且 AI 轉介新買家占比上升：熊市機率下調 5 個百分點，進場價上調到 105 美元"],"evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#2"]},{"axis":"收藏品熱度：結構還是週期","cause":null,"prior_field":null,"side_a":"管理層（2026-10-28，CEO）：二手轉售是長期轉變，受訪者每月買二手的比例由 35% 升到 47%；收藏品是最大成長來源，交易卡對高基期仍強。","side_b":"同一批管理層也說：金銀條是暫時助力（2026-05）；2027 年交易卡增速會自然放緩（2026-10-28，CFO）；Q4 指引有機 GMV 8–10%，比 Q3 的 13% 明顯降速。","ruling":"可調和（程度差異）。二手滲透是結構，交易卡熱度是週期，兩者同時成立。基準情境把 2027 年有機 GMV 放在 5–7%，熊市才用 0–2%。","evidence_level":"二手報告是公司自家調查，打折採用；降速指引是管理層財測，可驗證。","settle_metric":"2027 年各季有機 FX 中性 GMV","if_then":["若 2027 年 Q1 有機 GMV ≥6%：基準情境不變，股價到 100 美元以下就分批買進","若 2027 年 Q1 有機 GMV <3%：按唯一致命點處理，已持有者清倉"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"現在就買的最強論證 vs 等價格","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：Q3 營收、營業利益、EPS 都超過財測上緣，全年財測連續上修；FY2026 共識 EPS 近三個月上修 2.1%；FY2027 本益比 17.6 倍，對應每股盈餘年增約一成，另有約 1% 股息與 2–3% 淨回購；Depop 首季美國 GMV 翻倍，第二條曲線比預期快。","side_b":"基準情境五年價格報酬約 +24%，含股息年化不到 6%；倍數在近四年高點；賣方平均目標價低於現價；2026 年 EPS 分母含週期性熱潮。","ruling":"等價格。在 121 美元買進，賺到的只有 EPS 成長，還要吐回一部分倍數；要等到基準情境年化接近一成的價位。","evidence_level":"雙方都用事實表與法說會數字，分歧在倍數假設，不在事實。","settle_metric":"股價對 FY2027 共識 EPS 的倍數；2027 年財測","if_then":["若股價跌到 100 美元以下，且最新一季有機 GMV ≥5%：分兩批建首倉，第一批在 100 美元，第二批在 Q1 2027 財報確認後","若股價續漲但 2027 年財測尚未發布（價格先走、證據未到）：不追","反向：若 2027 年 2 月財測給出有機 GMV ≥8% 且非 GAAP 營益率 ≥26%：重算基準情境，進場價可上調到 110 美元"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：每月買二手的比例 35%→47%（公司調查）、聚焦品類 GMV +24%、全球電商仍以約 7% 成長（eMarketer 系列，經二手網站轉述）。","side_b":"競爭惡化：英國服飾 C2C 份額流向 Vinted（CMA 估計 50–60%），10-K 自述進入門檻低。其他結構變數：美國與歐盟取消小額免稅，跨境是大中華賣家的主要業務；AI 代理改變導流。","ruling":"雙向拉鋸：結構順風與競爭、關稅逆風並存，淨方向不明，所以護城河判穩定、跑道判中。","evidence_level":"CMA 估計與 10-K 為一手來源；成長數字為公司揭露。","settle_metric":"國際有機 GMV、英國服飾 C2C 份額更新、核心活躍買家","if_then":["若國際有機 GMV 連 2 季年減：熊市機率上調 5 個百分點，停止加碼","反向：若核心活躍買家（扣除併購）年增回到 3% 以上：跑道改判寬"],"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#0","reg_tariff_export#1","geo_supply_chain#0"]},{"axis":"基本面結論與前份比較","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份（2026-05-16）：thesis 完整但估值偏貴，陷阱風險中，護城河方向穩定。","side_b":"本次：Q2、Q3 連續超預期並上修財測，Depop 首季優於預期；同時出現新的負面證據，包括英國服飾 C2C 份額流失（CMA，2026-08）、抽成率年減約 20 個基點、裁員 9%。正負抵銷，三個結論都不變。","ruling":"維持：陷阱風險中、護城河方向穩定，整體評等與前份同一級。","evidence_level":"一手來源（10-Q、CMA）","settle_metric":"有機 GMV、抽成率","if_then":["若 2027 年有機 GMV 連 2 季低於 5%：陷阱風險改判高"],"evidence_refs":["competitive_share_entrants#2","end_markets#3"]},{"axis":"估值結論與前份比較","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 116.13 美元，估值偏貴一檔。","side_b":"本次：股價 121.4 美元（+4.5%），FY2026 共識 EPS 近三個月上修 2.1%，前瞻本益比 19.4 倍，與前份相近；在歷史年度端點中仍是最高位。","ruling":"維持偏貴一檔：價格漲幅與共識上修大致相抵。","evidence_level":"事實表","settle_metric":"前瞻本益比","if_then":["若股價跌到 100 美元以下而共識不變：估值改判合理"],"evidence_refs":[]},{"axis":"前份未落值欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位空白（舊格式未落值）。","side_b":"本次補上：跑道判中；公司類型判品質複利成長，次類為轉機；情境機率牛 20、基準 50、熊 30；最大回撤範圍 −28% 到 −45%。循環位置仍不適用（非循環股），維持空白。裁決與角色由程式依本次輸入算出。","ruling":"屬格式補值，不是判斷改變，不需要翻面理由。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場重新評估條件（首倉、加碼）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份為空（未設定重新評估條件）。","side_b":"股價 ≤100 美元（約 FY2027 共識 EPS 14.5 倍），且最新一季有機 GMV ≥5%；觸發後分批建首倉，不加碼追價。","ruling":"新設。本次觀望的約束是價格，條件就是價格約束的否定，另加一條基本面未壞的確認。","evidence_level":"方法","settle_metric":"股價、季度有機 GMV","if_then":["若觸發：重跑研究後分批建首倉"],"evidence_refs":[]},{"axis":"減碼與清倉指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份為空（未設清倉或減碼指標）。","side_b":"有機 GMV 連 2 季 <3%：清倉；非 GAAP 營益率連 2 季 <24%：減碼一半；核心活躍買家連 2 季負成長：減碼；抽成率連 4 季年減 ≥30 個基點：減碼。","ruling":"新設：把前份 R1–R3 的監測項目落成可執行的門檻。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份為空（未設定 Single Thing）。","side_b":"2027 年任一季，有機 FX 中性 GMV（不含 Depop）年增跌破 3%，且管理層把主因歸給收藏品（交易卡）轉弱。","ruling":"新設：選數學上最大的敏感項（有機 GMV 增速），不選最戲劇性的 AI 或收購事件；發生即清倉。","evidence_level":"方法","settle_metric":"季度有機 GMV","if_then":["若發生：已持有者清倉，未持有者取消進場價條件"],"evidence_refs":[]},{"axis":"前份假設與風險門檻更新","cause":"新證據","prior_field":["thesis.H1","thesis.H2","thesis.R1"],"side_a":"前份 H1 門檻：FY26–27 有機 GMV ≥6%。H2：FCF ≥15 億美元、股數 444→410 百萬。R1：Q2／Q3 GMV 不及預期則論點反轉。","side_b":"本次 H1 門檻改為 FY2027 單年有機 GMV ≥5%；股東經濟改列 H3，門檻為非 GAAP 營益率 ≥25%、FY2030 股數 ≤400 百萬；前份 R1 退休。","ruling":"R1 退休的理由是風險沒有發生：Q2、Q3 GMV 都超過財測（Q3 FX 中性 +16%、有機 +13%）。H1 由 6% 改 5% 是放寬：2026 年已遠超門檻，本次只看 2027 單年，而管理層已預告交易卡放緩，5% 是基準情境每股盈餘年增 8–9% 所需的最低有機增速。H2 改看營益率：FCF 絕對值受 Depop 投資與收購時點干擾，營益率更能直接反映抽成率下滑的風險。","evidence_level":"一手來源（季報、法說會）","settle_metric":"FY2027 有機 GMV、非 GAAP 營益率","if_then":["若 FY2027 有機 GMV <5%：H1 削弱，基準 EPS 下修"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年 2 月 Q4 財報與 2027 年財測：看有機 GMV 財測是否 ≥5%","type":"假設驗證","maps_to":"H1","metric":"2027 年有機 FX 中性 GMV 財測；Q4 有機 GMV","threshold":"≥5%","action":"低於 5%：基準 EPS 下修，進場價下調到 90 美元；高於 8% 且營益率 ≥26%：重算情境","source_freq":"季報新聞稿，每季","date":"2027-02","evidence_refs":[]},{"n":2,"text":"唯一致命點：有機 GMV 跌破 3%，且主因是收藏品","type":"Single Thing","maps_to":"Single Thing","metric":"單季有機 FX 中性 GMV 年增（不含 Depop）","threshold":"<3%，且管理層歸因於收藏品","action":"已持有者清倉；未持有者取消進場價條件並重跑研究","source_freq":"季報與法說會，每季","date":null,"evidence_refs":["supply_demand_durability#0"]},{"n":3,"text":"價格回到合理區：分批建首倉","type":"估值rearm","maps_to":"H1","metric":"股價；最新一季有機 GMV","threshold":"股價 ≤100 美元，且有機 GMV ≥5%","action":"重跑研究後分兩批建首倉","source_freq":"每日股價、每季財報","date":null,"evidence_refs":[]},{"n":4,"text":"AI 入口分流成形","type":"風險","maps_to":"R3","metric":"自然流量占比；主要 AI 代理的交易介面名單","threshold":"自然流量 <80%，或主要 AI 代理與 Amazon／Walmart 簽約而 eBay 缺席","action":"已持有者減碼一半；未持有者進場價下調到 90 美元","source_freq":"法說會與新聞，每季","date":null,"evidence_refs":["competitive_share_entrants#1","substitute_technology#2","substitute_technology#0"]},{"n":5,"text":"股東經濟轉差：營益率跌破守門線","type":"減碼","maps_to":"R2","metric":"非 GAAP 營業利益率","threshold":"連 2 季 <24%","action":"已持有者減碼一半","source_freq":"季報，每季","date":null,"evidence_refs":["channel_business_model_shift#2","end_markets#3"]},{"n":6,"text":"跨境逆風擴大","type":"風險","maps_to":"R4","metric":"國際有機 FX 中性 GMV 年增","threshold":"連 2 季 <0%","action":"熊市機率上調 5 個百分點，停止加碼","source_freq":"季報，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#4","geo_supply_chain#0"]},{"n":7,"text":"英國 CMA 對 Depop 收購的調查結論","type":"風險","maps_to":"R5","metric":"CMA 決定","threshold":"要求出售 Depop，或附重大行為條件","action":"牛市機率下調到 15% 並重算情境；現有清倉條件不變","source_freq":"CMA 公告，事件型","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":8,"text":"Steiner 民事案開庭","type":"複審日期","maps_to":"R6","metric":"判決或和解金額","threshold":"超過約 3.7 億美元（一季 FCF 的一半）","action":"超過門檻：資本回報假設下修，重算情境","source_freq":"法院排程","date":"2027-01-04","evidence_refs":["major_events#2","lawsuit_class_action#1"]}],"kill_metrics":[{"metric":"有機 FX 中性 GMV 年增（不含 Depop）","bear_threshold":"連 2 季 <3%（清倉）","window":"2027 年各季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"非 GAAP 營業利益率","bear_threshold":"連 2 季 <24%（減碼一半）","window":"滾動 2 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"核心活躍買家年增（扣除 Depop、Tise，TTM）","bear_threshold":"連 2 季 <0%（減碼）","window":"滾動 2 季","source":"法說會揭露","last_status":"warning"},{"metric":"抽成率年變動","bear_threshold":"連 4 季年減 ≥30 個基點（減碼）","window":"滾動 4 季","source":"10-Q","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=11.74, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價 ≤100 美元（約 FY2027 共識 EPS 14.5 倍）且最新一季有機 GMV ≥5% 時，重跑研究後分批建首倉","exec_line":"現在不建倉；觸發進場條件後分兩批建首倉。已持有者不加碼；營益率連 2 季 <24% 減碼一半；唯一致命點發生即清倉。"},"reasoning":{"industry":"收入結構：10-K 把營收分成市集抽成與廣告兩類。Q3 營收 32.06 億美元、GMV 231.66 億美元，廣告 6.07 億美元（年增 16%，不含 Depop 約占 GMV 2.7%），其餘主要是抽成，加上運送與金融服務。最新一季非 GAAP 營益率 26.3%、GAAP 19.2%，非 GAAP 毛利率 73.1%（2026-10-28 法說會，CFO）。地理分布：FY2025 美國 52%、國際 48%（10-K），2023–25 年沒有單一客戶超過營收 10%。成長來源：聚焦品類、C2C、二手轉售合計 GMV 年增約 20%，占 GMV 72%（不含 Depop）；美國有機 GMV +22%，國際只有 +4%。產業時鐘判 II（擴張），依據有兩點：全球電商仍以約 7% 成長（eMarketer 系列預測，經二手網站轉述）；美國受訪者每月買二手的比例由 35% 升到 47%（公司 2026 年二手報告，屬自家調查，打折採用）。供需持久性一半結構、一半週期：二手與 C2C 滲透上升屬結構性；交易卡與金銀條熱潮屬週期性，而且會反轉，管理層 2026-05 自己說金銀條是暫時助力，2026-10 又說 2027 年交易卡增速會自然放緩。單點依賴：買家端很分散，真正的單點在導流。10-K 自述依賴 Google 搜尋、演算法調整曾減少導流，AI 轉介不足可能讓買賣家轉向別處；目前 85% 流量是自然流量（法說會，CEO），這是主要緩衝。","moat":"機制：二手與收藏品是長尾、非標準化的庫存，買家要的是「找得到」加「買得安心」。eBay 的優勢是兩件事疊加：一是近 27 億件刊登的深度；二是信任基礎設施，包括真品保證（累計檢驗逾 2,000 萬件）、PSA 與 PCGS 鑑定合作、車輛 50 萬美元購買保障。可證方向有三條。①對最強同業的利潤率差：eBay TTM 營益率 20.2%、ETSY 16.9%，差 3.3 個百分點；FCF 利潤率 19.5% 對 19.7%，幾乎相同。同業 ROIC 與利潤率差的歷年走勢事實表未涵蓋，無法判斷差距在擴大還是收窄。②份額：英國服飾 C2C 有來源佐證的份額流失（CMA 估計 Vinted 占 50–60%，eBay 與 Depop 流失份額），因此方向不能標升。③留存與單價：熱衷型買家 TTM 花費約 3,700 美元、逐季上升，美國熱衷買家 +9%；但全球核心活躍買家只 +1%。定價力：抽成率 13.84%，去年同期 14.03%；eBay 自己在法國、義大利推出免費賣，Q2 法說會又稱美國沒有調費計畫。在 C2C，定價力是讓出去換量，不是往上拉。唯一往上的定價槓桿是廣告：6.07 億美元、年增 16%、約占 GMV 2.7%，管理層稱 3% 是中期目標不是上限。評分：執行 8 分（Q3 營收、利潤都超過財測上緣，Depop 首季美國 GMV 翻倍，eBay Live 三位數成長）；定價 6 分；AI 代理控制前端導流屬生態攻擊，扣 1 分，合計 6 分。","growth":"成長拆解是量為主、價為負、併購加分。Q3 GMV FX 中性 +16%，其中有機 +13%、Depop 約 3 個百分點；營收 FX 中性 +13%，其中有機 +11%、Depop 約 2 個百分點；價格面的抽成率年減約 20 個基點。管理層稱 ASP 與件數「平衡」，但沒有給量化拆解，Q2 法說會分析師追問也沒有正面回答。共識：FY2026–28 EPS 6.25→6.88→7.81 美元，兩年年複合約 11.8%；營收共識 FY2027 年增約 7.2%（126.5 億→135.5 億美元）。EPS 增速比營收快約 3 個百分點，來自回購與利潤率，差距不到 5 個百分點，不算衰退信號。三年口徑需要 FY2025 非 GAAP EPS，事實表只有 GAAP 4.34 美元，口徑不同不能混算，這裡以兩年年複合代替。缺口歸因：共識 11.8% 減內生上界 7.5%，約 4.3 個百分點。約 2 個百分點來自利潤率擴張（裁員 9%、管理層稱 Depop 2028 年對營業利益轉為增益）；約 1.5 個百分點來自 Depop 的併購成長（2027 年上半年仍沒有可比基期）；其餘約 1 個百分點是費用化成長投資帶出的有機成長，公式抓不到，屬推定。跑道：滲透率事實表未涵蓋（CEO 說「家戶閒置物品不到兩成上線」是說法，不是統計），無法換算成年數。判中而非寬，是因為核心買家基數幾乎不長，第二曲線的經濟性也還沒被證明。","governance":"2026 年現金去向：回購目標約 20 億美元（Q2 3.1 億、Q3 約 6.9 億，Q3 均價約 106 美元）；股利每季約 1.38 億美元；Depop 14 億美元現金收購。期末現金與固定收益投資 33 億美元、總債務 67 億美元（2026-10-28 法說會，CFO），淨負債約 52 億美元（含租賃）。管理層預告 2027 年利息收入會因現金變少而下降。FCF 品質：GAAP 淨利受股權投資評價損益扭曲（事實表 financial_history，yfinance 年度財報：2022 年淨損 12.69 億美元、2023 年淨利 27.67 億美元），FCF／淨利比失真，改看 FCF 利潤率：2022–24 年 18–19%，2025 年掉到 12.9%（原因事實表未涵蓋），TTM 回到 19.5%。SBC：Q3 1.73 億美元、占營收 5.4%，年化約 6.9 億美元，約為市值的 1.3%。三項計分：①併購已實現報酬：Q2 法說會預告 Depop 拖累 Q3 營業利益成長 3–4 個百分點，管理層自己說 2028 年才轉為增益，不過。②回購買入收益率：均價 106 美元對 FY2026 共識 EPS 6.25 美元，盈餘殖利率約 5.9%；門檻是十年期公債殖利率加 2%，但十年期殖利率事實表未涵蓋，無法判定。③SBC 淨稀釋：年化 SBC 約市值 1.3%，低於 1.5%，過。營運槓桿：Q4 指引營收有機 +5–7%、非 GAAP 營業利益 +6–10%，未見壓縮。","valuation":"主尺用前瞻本益比：121.4 美元對 FY2026 共識 EPS 6.25 美元為 19.4 倍，對 FY2027 共識 6.88 美元為 17.6 倍。PEG：事實表沒有 FY2025 非 GAAP EPS，算不出三年口徑，改用 FY2026→FY2028 兩年共識年複合 11.8%，PEG 約 1.65，在合理區 1–2 中段偏上。歷史位置：trailing 本益比 26.5 倍、P/S 4.3 倍、EV/S 4.72 倍，都在可得的 3–4 個年度端點中最高（分位 100）。這不是連續五年分位，樣本點少，只能說「比過去幾年任何一個年底都貴」。共識方向：FY2026 共識 EPS 近三個月上修 2.1%；股價自前份的 116.13 美元漲約 4.5%，倍數與前份相近。賣方平均目標價約 110–113 美元（Q3 財報前，多家來源），低於現價。同業前瞻倍數事實表未涵蓋，無法做同業倍數對照，終端倍數改用自身成長熄火情境定錨。短期上檔：12 個月以 FY2027 基準 EPS 6.80 美元乘 18 倍，得 122 美元，約 +1%。中期上檔：五年基準情境 FY2031 EPS 9.40 美元乘 16 倍，得 150 美元，約 +24%（不含股息）。分母爭議：2026 年 EPS 含金銀條與交易卡異常高的貢獻，管理層自承前者是暫時的、後者 2027 年會放緩，常態獲利可能被高估，所以這裡不做便宜論證。","premortem":"衰退信號十項中確定亮 1 項（英國服飾 C2C 份額流失），另 1 項已超標但趨勢不明（SBC 占營收 5.4%），陷阱風險與長期成長性都落在中間。最大回撤範圍 −28% 到 −45%：上緣是回到 104 週均線 87.3 美元（−28%）；中心是熊市情境 2027 年 EPS 6.2 美元乘 12 倍，約 74 美元（−39%）；250 週均線 62.8 美元（−48%）是極端值。股價目前比 52 週均線 100.6 美元高約 21%。成長熄火壓力測試，以基準情境 FY2029 EPS 8.10 美元為底：之後增速降到 15% 給 20 倍，得 162 美元；降到 10% 給 16 倍，得 130 美元；降到 5% 給 13 倍，得 105 美元。三種裡兩種高於現價。法說會迴避紀錄：Q2 分析師追問核心（不含 Depop）的 Q4 成長、量價拆解、長期成長框架、可轉配的行銷費用，管理層都沒給數字。核心市集的真實增速是本次最大的資訊缺口。反證細節與裁定寫在反證紀錄。"},"plain":{"six":{"how_it_makes_money":"eBay 賺的是買賣雙方成交額的抽成（Q3 抽成率 13.84%），加上賣家買曝光的廣告費。錢卡在「信任與撮合」這一節：真品保證、買家保障與近 27 億件非新品刊登讓買家留下；它控制不了的環節是上游導流（Google 搜尋、AI 代理）。","moat":"護城河方向判穩定（→）。執行力在擴大、定價力略縮，英國服飾 C2C 份額已流失，抵銷後不升不降。等級 C：執行 8 分、定價 6 分，AI 代理對導流層的生態攻擊扣 1 分。","growth":"跑道判中（🟡）。核心市集已成熟，扣除併購的活躍買家只 +1%；第二條曲線 eBay Live 與 Depop 有來源佐證，但抽成率低，Depop 要到 2028 年才對營業利益轉正。共識 FY2026–28 EPS 兩年年複合約 11.8%，高於推定內生上界 7.5%，缺口靠利潤率擴張與 Depop 的併購成長補。","capital":"資本配置穩定但不出色。回購加股利照框架執行（Q3 配回約 8.3 億美元，高於當季 FCF 7.49 億美元），SBC 稀釋可控；但 Depop 收購的報酬尚未實現，回購也買在不便宜的價位，三項計分只過一項。","valuation":"現價要求三件事：2027 年起有機 GMV 維持中高個位數成長；非 GAAP 營益率守住 25% 以上，每股盈餘年增約一成、持續五年；市場繼續給接近 19 倍的前瞻本益比。前兩件我大致相信，第三件不信：交易卡高基期與抽成率下滑會讓倍數向 16 倍靠攏，基準情境五年年化報酬不到 8%。估值偏貴一檔。","how_wrong":"最可能看錯的地方，是把 2026 年的交易卡熱潮當成新常態。若 2027 年有機 GMV 跌到 3% 以下，倍數會回到 12 倍附近，股價約 75–80 美元。陷阱風險判中（🟡）。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 100 美元以下（約 FY2027 共識 EPS 14.5 倍，基準情境五年年化接近一成），且最新一季有機 GMV 仍 ≥5%","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟠","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":121.4,"week26_return_pct":11.74,"consensus_rev_3m_pct":2.12,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"2026 年 EPS 含金銀條（管理層稱暫時）與交易卡異常高（管理層稱 2027 年放緩）的貢獻，作為分母可能高估常態獲利；因此只用前瞻倍數判斷貴不貴，不用來論證便宜。"},"catalysts":[{"date":"2027-01-04","type":"other","event":"Steiner 跟蹤騷擾民事案開庭","impact":"低","watch":"判決或和解金額是否超過約 3.7 億美元"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年財測","impact":"高","watch":"2027 年有機 GMV 財測是否 ≥5%，非 GAAP 營益率是否 ≥25%"},{"date":"2027-03","date_precision":"month","type":"other","event":"重組計畫大致完成（裁員約 9%，費用 1.3–1.5 億美元，多數在 Q4 2026 認列）","impact":"中","watch":"省下的費用是轉成利潤率，還是再投資到 Depop"},{"date":"2027-Q2","date_precision":"quarter","type":"guidance","event":"Q1 2027 財報：第一個完整對比交易卡高基期的季度","impact":"高","watch":"有機 GMV 是否守住 5%，以及收藏品的敘述"},{"date":null,"type":"regulatory","event":"英國 CMA 對 Depop 收購的調查結論（時點事實表未涵蓋）","impact":"中","watch":"是否要求出售或附加條件"}],"_projected_from":"v19"}
```
