你是 stock-analyst v20 的**散文層（prose）agent**，標的 APP（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：APP　日期：2026-11-08　archetype：None　前份裁決：2026-07-10　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1865B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（560B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（997B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1469B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1043B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（472B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（893B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2105B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4166B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2667B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1865           3594-5135      5 條（2–6 內）  
s3                  8000         560           5208-7440      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3509          8044-11491      5 條（2–6 內）  
s6                 11000         472          7370-10528      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         893           1825-2607      5 條（2–6 內）  
s10                 5000        2105           2026-2895      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2667           2000-2333      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4802B；至少需散文≈40.20KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65%
−65
−60%
−54%
−48%
−45
−45%
−31.5%
−24.8%
−19%
−17%
−16.5
−16.5%
−9%
−8%
−1.7%
0
0.10
0.1
0.26%
0.66
0.75
0.94
01
1%
1
1.04
1.13
1.18
1.31
$1.45
02
2%
2
2.14
2.3%
3
3%
3.25
3.4
3.5
3.9%
04
4
4.3
4.7%
4.9%
4.94
5.0%
05
5%
5
5.3
6
06
6.2
6.2%
7
7.7%
08
8
8%
8.4%
8.8%
9
9.7%
9.75
10
10%
10.2%
10.5%
11%
11
11.4
12
12%
12.4%
13
13%
14
14%
14.5
15
15%
15.8%
16
16.65
17%
17.08
18%
18
18.1
18.5%
18.5
18.8
19%
19.5
19.55
19.6
19.6%
20
20%
20.01
20.7%
21.0
21
21.7
21.8
21.9
21.93
22
22%
22.3
22.4
22.8
23
23.5
23.95
24
24%
24.27
24.7%
24.8%
25
25%
25.1%
25.5
26
27%
28
28%
28.4%
29
30
30%
30.0
31%
31.7%
32
32.9%
33.3%
34.5
35%
35
35.5%
36
36.5
38.0%
39
40%
42
43%
43.3%
44.0
44%
44.5
45
46%
48.7
49
50%
50.2%
52.5
53.4
55%
55.0%
59.3%
60
60%
64%
64.07%
64.1%
65%
66%
70%
70
75%
75.8%
76.1
76.31
77.3%
77.8%
78%
78.2%
80%
84.2
84.3%
85%
87
87%
87.9%
88.8%
90
94
95
100
100%
104
150%
180
198
200
205.15
243
250
253.5
336
341
391
391.22
410
$430
460
520
520.43
702
714
987
2025
2026
2027
2028
20261108
1,000
1,170
1,207.5
1,299.6
1,709.0
2,184.8
4,262
4,982
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
{"meta":{"ticker":"APP","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"AppLovin Corporation"},"oneliner":"現價 391.22 美元只隱含未來十年自由現金流年增約 11%，新一代模型卻才部分上線；好生意配偏低價格，但財報後短線過熱宜分批。最大風險是模型提升斷檔，使 FY2027 營收年增跌破 20%。","thesis":{"H":[{"id":"H1","text":"新一代模型讓廣告業務維持高成長，併表營收在 2027 年仍年增 25% 以上。","2y":"FY2027 營收不低於 104 億美元，FY2028 年增不低於 20%","5y":"FY2031 營收約 198 億美元","10y":null,"threshold":"FY2027 營收不低於 104 億美元；單季年增連 2 季不低於 25%","source":"公司 8-K 與季報、2026-11-04 法說；共識來自 yfinance","drift_rule":"TTM 偏離連 2 季達 5% 削弱，連 3 季達 10% 反轉；單季年增連 2 季低於 25% 即重評"},{"id":"H2","text":"消費端廣告成為第二條成長線，非遊戲收入成為主力之一。","2y":"消費端年增維持 50% 以上到 2028 年 Q1，年化營收不低於 14.5 億美元","5y":"非遊戲營收成為主力之一，占比待公司揭露","10y":"成為圍牆外電商投放的預設選項之一","threshold":"消費端年增連 2 季不低於 50%；年化營收不低於 14.5 億美元（公司未揭露，資料缺口）；go-live 轉換率不低於 65%（資料缺口）","source":"法說口頭揭露；Needham 估 2026 年電商營收 14.5 億美元（二手摘要）；第三方 Pixel 統計","drift_rule":"連 4 季偏離達 5% 削弱，連 6 季達 10% 反轉；管理層不再揭露方向視同未達"},{"id":"H3","text":"高現金轉換與回購把營收成長轉成每股成長，股東報酬不需要倍數回升。","2y":"EBITDA 利潤率維持 80% 以上，FCF 轉換率 70% 到 75%","5y":"稀釋股數累計減少約 10%","10y":null,"threshold":"調整後 EBITDA 利潤率不低於 80%；稀釋股數年減不低於 1%；淨槓桿不高於 1 倍","source":"公司季報、CFO 於 2026-08-05 與 2026-11-04 法說","drift_rule":"連 2 季偏離達 5% 削弱，連 3 季達 10% 反轉"}],"R":[{"id":"R1","text":"模型提升再次斷檔，營收重演 Q2 的低於預期。","h_ref":"H1","clock":"⚡","threshold":"連 2 季低於指引中點","evidence_refs":["supply_demand_durability#0"]},{"id":"R2","text":"消費端擴張不如預期，受轉換瓶頸、創意門檻與競爭影響。","h_ref":"H2","clock":"🔥","threshold":"消費端年增連 2 季低於 50%；年化 ARR 連 2 季低於 3 億美元或轉換率連 2 季不升破 65%（後兩項資料缺口）","evidence_refs":[]},{"id":"R3","text":"手遊需求轉弱，遊戲廣告成長放慢甚至衰退。","h_ref":"H1","clock":"🐢","threshold":"遊戲廣告年增轉負且非季節性，連 3 季","evidence_refs":["supply_demand_durability#2"]},{"id":"R4","text":"Apple、Google、Meta 等發行平台改變規則，大量營收依賴有限的第三方平台。","h_ref":"H1","clock":"🔥","threshold":"公司揭露重大影響，或單季營收低於指引下緣","evidence_refs":["geo_supply_chain#0","customer_second_source#0"]},{"id":"R5","text":"資料做法的監管與訴訟風險：FTC 調查未見進展，證券集體訴訟仍在進行，SEC 查詢依公司說法已結束。金額與時點事實表未涵蓋。","h_ref":"H1","clock":"🔥","threshold":"集體認證加不利和解減碼至一半；刑事程序介入清倉；SEC 重啟調查減碼至一半","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#0","major_events#1","lawsuit_class_action#0","sec_investigation_restatement#0"]},{"id":"R6","text":"美中緊張與中東衝突影響中國、以色列營運及亞太廣告主；公司自述目前產品不受出口管制限制。","h_ref":"H2","clock":"🐢","threshold":"國際營收連 2 季年減，且管理層歸因於管制或衝突","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]}],"single_thing":{"description":"FY2027 全年營收年增率跌破 20%，也就是低於約 100 億美元，等於新架構沒有帶來下一輪成長。","why_fatal":"營收成長是 Y5 EPS 最大的單一敏感項。五年 CAGR 少 5 個百分點，FY2031E EPS 少約 19%，約 30% 的長期目標也會失效，倍數跟著下修。Q4 指引年化已約 95 億美元，跌破 100 億美元代表 2027 年幾乎沒有季增。","if_happens":"清倉，H1 反轉；股價路徑接近 Bear，約 250 美元。","how_monitor":"每季營收對指引上緣與中點、遊戲與消費端年增描述；2028 年 2 月以全年數字確認，提前的領先條件是連 2 季低於指引中點。","probability":"15%（12 到 24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":19.55,"peg_fy2":0.94,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":9.75,"FY2026E":16.65,"FY2027E":20.01,"FY2028E":24.27},"fy_end_month":12,"eps_basis":"基期為 yfinance 年報稀釋 EPS；FY2026E 至 FY2028E 為 Koyfin 共識快照，事實表未標 GAAP 或調整後口徑"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"TTM 營益率 77.8%、FCF 利潤率 64.1%，成長來自模型提升與新廣告主，主要投入走費用而非資產"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久，但持久的是成效預算需求，不是單一公司的份額。依據：2026-11-04 法說稱 MAX 供給維持強雙位數成長；Oberlo 預估 in-app 廣告 2026 至 2028 年由 4,262 億美元增至 4,982 億美元。","bargaining":{"up":"上游是 MAX 發行商與 Apple、Google、Meta 等發行平台；CEO 承認發行商收益隨拍賣上漲，公司要靠技術進步吸收。","down":"廣告主分散，無單一客戶占營收 10% 以上，以成效計價，沒有合約鎖定。","geo":"在中國與以色列有營運；亞太消費端廣告主增加，法說說明部分網站是專為此通路開設。"},"profit_pool_dir":"利潤往預測最準的圍牆外平台集中，五年占比事實表未涵蓋。","tam_table":[{"item":"全球 in-app 廣告","value":"2026 年 4,262 億美元、2028 年 4,982 億美元（Oberlo，2025-01 圖表，口徑含大型封閉平台）"},{"item":"APP 總投放金額","value":"接近 200 億美元年化（2026-11-04 法說，JPMorgan 分析師轉述）"},{"item":"滲透率","value":"約 4.7%"},{"item":"MAX 手遊中介份額","value":"70% 以上（JPMorgan 估算，賣方資料）"},{"item":"營業利益池五年占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"MAX 拍賣的供給規模加 AXON 預測模型形成資料飛輪：單一拍賣跨遊戲與消費廣告主，預測越準，出價與預算越多。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"上行：Q3 遊戲年增近 50%，新架構部分上線即帶動超預期；消費端增加拍賣密度。下行：Q2 模型斷檔造成未達指引，CEO 承認多家對手同時表現很好，Android 較競爭。份額只有 2026 年 Q1 的賣方查核，沒有最新數字，所以不上調。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用營益率差距。","threats":[{"level":"🔴","text":"生態攻擊：Google 在 Android 上既是平台也是大型對手，Apple、Google、Meta 掌握發行與資料規則；Meta、Amazon、Unity 同時是客戶與對手，可能改用自家方案。APP 研發密度 5.0%，遠低於 META 31.7%、GOOGL 15.8%，模型競賽的資源不對等。","p":"30%","evidence_refs":["competitive_share_entrants#0","geo_supply_chain#0"]},{"level":"🟡","text":"點對點：CloudX 以免 SDK 模式切入，2026-02 推出時 APP 股價下跌約 13%；Wedbush 指出 Google 等過去嘗試類似模式，創辦人也定位為補充。Q3 遊戲年增近 50%，沒有看到受損，本包也沒有 CloudX 的營收或份額數字。","p":"15%","evidence_refs":["competitive_share_entrants#2","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"點對點：10-K 提醒對手可能更快採用新技術。Q3 法說 UBS 提到部分廣告主預期拍賣價格上漲而先把預算移往對手，CEO 認為這類調查樣本有偏誤，但沒有提供份額數字。","p":"25%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（投入資本事實表未涵蓋，依輕資產與自由現金流高於淨利推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是玩家，決策者是投手，付款者是廣告主，三者都成立；廣告主以 ROAS 自付，CEO 稱每年帶來數百億美元營收。風險是消費端仍被部分廣告主視為測試預算（2026-08-05 法說）。"},{"item":"決策層級","level":"🟡","text":"替代性要看單一廣告活動與單一曝光。投手可以當天移走預算，沒有合約；供給端 MAX 份額 70% 以上有黏性，需求端主要靠效果留客，消費端廣告主還要跑增量測試才放量。"},{"item":"價值鏈分配","level":"🟡","text":"抽成推算約 44%，CEO 說領先才能多拿，落後就會被壓縮。Apple、Google、Meta 控制發行，發行商收益隨拍賣上漲。"},{"item":"社會容忍度","level":"🟡","text":"全螢幕廣告佔滿畫面，CEO 稱平均觀看超過 35 秒；資料做法曾受 SEC 與 FTC 關注。CFO 說 SEC 查詢已結束，FTC 未見進展，證券集體訴訟仍在進行。"}],"roiic":"無法計算：投入資本事實表未涵蓋；FY2024 到 FY2025 營業利益增加約 22.4 億美元，新增有形資本很少，比值沒有意義。","reinvest_rate":"接近零或為負：FY2024、FY2025 自由現金流分別為淨利 1.31、1.18 倍；資本支出、折舊與營運資金明細事實表未涵蓋。","endo_ceiling":null,"formula_note":"增量報酬乘再投資率的公式不適用於費用化投入的輕資產模式。公式上界趨近零，共識成長必然超過，因此情境以超過上界處理，Bear 機率取 30%。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","APP":88.78,"META":81.03,"GOOGL":60.86,"TTD":76.87,"U":61.96,"unit":"%"},{"metric":"營業利益率","APP":77.78,"META":32.86,"GOOGL":33.32,"TTD":19.61,"U":-31.46,"unit":"%"},{"metric":"FCF 利潤率","APP":64.07,"META":11.86,"GOOGL":4.19,"TTD":28.38,"U":24.66,"unit":"%"},{"metric":"研發密度","APP":4.97,"META":31.68,"GOOGL":15.81,"TTD":18.12,"U":50.23,"unit":"%"}],"competitors":[{"name":"META","gm":81.03,"om":32.86,"fcf_margin":11.86,"rd_intensity":31.68,"strategy_note":"TTM 營益率 32.9%、研發密度 31.7%，賣方點名的潛在競爭者，資源遠大於 APP；Q3 未見 APP 受損。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"GOOGL","gm":60.86,"om":33.32,"fcf_margin":4.19,"rd_intensity":15.81,"strategy_note":"Android 上的大型對手，CEO 於 2026-08-05 承認 Android 較競爭，同時掌握 Google Play 規則。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"TTD","gm":76.87,"om":19.61,"fcf_margin":28.38,"rd_intensity":18.12,"strategy_note":"同為獨立廣告技術公司，營益率 19.6%、FCF 利潤率 28.4%，資料截至 2026-06；本包沒有份額資料。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"U","gm":61.96,"om":-31.46,"fcf_margin":24.66,"rd_intensity":50.23,"strategy_note":"Unity Vector 被賣方點名為威脅，TTM 營益率 −31.5%、FCF 利潤率 24.7%、研發密度 50.2%，投入重但利潤尚未跟上。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量與模型提升為主，消費端新客為第二動力，併購為零，淨回購約貢獻每年 2% 的每股成長。","runway_years":10,"runway_post_y5":"🟢","endo_ceiling_basis":"再投資率接近零，公式上界趨近零，無法給有意義的數字。成長投入走費用：算力、研發與新客開發；Base 淨利率由 66% 降到 60%，反映這筆投入。","segments":[{"item":"遊戲廣告","value":"Q3 年增近 50%，金額未揭露；CEO 稱遊戲公司幾乎都已在平台上，成長靠模型與供給"},{"item":"消費端廣告","value":"Q3 季增雙位數、年增三位數，金額未揭露；Needham 估 2026 年 14.5 億美元（二手摘要）"},{"item":"聯網電視","value":"試點階段，CEO 表示短期不要計入數字，情境未計入"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"FY2025 87.9%，TTM 88.8%；季度年比事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"賣方查核 2026 年 Q1 上升；Q2 之後沒有份額資料"},{"signal":"提價後銷量下滑","lit":null,"note":"拍賣定價，不適用"},{"signal":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"note":"FY2025 到 FY2027 差 5.3 個百分點"},{"signal":"FCF 除以淨利連 2 年低於 0.75","lit":false,"note":"FY2024 1.31、FY2025 1.18"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"Q3 為 3.9%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"目前未見，CloudX 持續觀察"},{"signal":"產業倍數近 3 年系統性下移","lit":null,"note":"同業倍數事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"輕資產模式，明細未涵蓋"},{"signal":"停止投資且收入下滑","lit":false,"note":"算力投入增加，營收成長"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月沒有重大併購；回購紀錄已在計分項交代，若出現併購案再展開。"},"capalloc_grade":"A","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月沒有重大併購；MoPub 的回本只有管理層說法，沒有已實現報酬數字。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"累計回購均價 90 美元，以 FY2026E EPS 16.65 美元計，買入收益率約 18.5%；Q3 均價約 341 美元時只有約 4.9%。10 年期殖利率事實表未涵蓋，以累計成本判過關。","grade":"過"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數連 8 季下降，年減約 2%；SBC 年化約 3.4 億美元，占市值約 0.26%，淨稀釋為負。","grade":"過"}]},"valuation":{"basis":"FY2026E Forward 本益比，搭配自由現金流反推隱含成長","tier":"大型獨立廣告技術平台","peers":{"expanded":false,"reason":"同業倍數事實表未涵蓋，只有利潤率對照；估值不使用跨類型同業作錨。"},"fwd_pe":23.5,"peg":0.66,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"Forward 本益比 23.5 倍、FY2027E 19.6 倍。PEG 以三年 EPS CAGR 35.5% 算為 0.66，但其中 FY2026 已大致實現；改用 FY2026E 到 FY2028E 的 20.7%，Forward 本益比對應 1.13，FY2027E 本益比對應 0.94，本次採用後者的讀法，落在合理偏便宜。五年分位無法提供：事實表只有 3 到 4 個年度端點，不是五年序列。Base 年化報酬約 12%，高於前份 9.7%。反例：要求報酬提高到 12% 時，現價只算合理；若 78% 營益率是高峰，EPS 分母會被高估。短期空間以 FY2027E 21.0 美元乘 22 倍估 12 個月，中期以 FY2029E 30.0 美元乘 20 倍估 3 年。賣方目標價資料約為 2026-02，平均 714 美元，舊於最新財報，不納入判斷。","upside_short_pct":18.1,"upside_mid_pct":53.4},"trap_analysis":{"verdict":"🟡","label":"低本益比可能建立在高峰利潤率上，衰退信號亮一個"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2026-08-05 CEO 說模型提升沒有保證，Q2 營收略低於指引中點；2026-11-04 再說無法承諾全面上線時間，遊戲公司幾乎都已在平台上。","assumption":"每年都能做出足以支撐 25% 以上成長的模型提升。","consequence":"FY2027 營收年增跌破 20%，EPS 停在 18 到 20 美元，倍數壓到 13 倍，股價約 250 美元，五年虧約 35%，途中可能腰斬。","ruling":"採納，列為 Bear 主路徑，機率 30%，與唯一致命數字是同一件事。","watch":"每季營收對指引上緣與中點、遊戲年增率。","evidence_refs":["supply_demand_durability#0"],"fact_refs":["f_kpi0_revenue_gaap","f_kpi5_guidance_q4_2026_revenue"]},{"view":"論點失敗","evidence":"消費端金額未揭露，CEO 拒絕提供預測性指標；亞太 Pixel 帳戶增加可能是同一客戶開多個網站，小型商家自助要到五年後才成熟。","assumption":"消費端是可持續的第二曲線，而不是少數廣告主的短期測試。","consequence":"約 30% 的長期目標少掉一半支撐，成長回到遊戲單腳。","ruling":"部分採納。Q3 年增三位數是事實，但規模未知，Base 五年營收 CAGR 只給約 19%，低於管理層的 30%。","watch":"管理層是否持續揭露年增方向、賣方消費端估算、第三方 Pixel 統計。","evidence_refs":["end_markets#2","channel_business_model_shift#1"],"fact_refs":["f_rev_consensus_fy2_m"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 說會尋找能買到資料與客戶關係的交易，並以 MoPub 為例；CFO 預期長期淨槓桿約 1 倍；算力持續增加，發行商收益隨拍賣上漲。","assumption":"成長能維持接近 78% 的營益率，現金繼續回饋股東。","consequence":"營收成長但淨利率由 66% 降到 55%，或一筆超過市值 5% 的併購把回購現金轉走，EPS 少 8% 以上。","ruling":"採納。Base 淨利率已降到 60%；併購沒有具體案件，列為觸發條件。","watch":"調整後 EBITDA 利潤率、併購金額占市值比、回購金額。","fact_refs":["f_kpi2_adjusted_ebitda_non_gaap","f_ev_m"]},{"view":"論點成功但股東經濟變差","evidence":"UBS 在 2026-11-04 法說提到部分廣告主預期消費端加入後拍賣價格上漲，先把預算移往對手；CEO 認為 CPM 上升時 ROAS 也會上升。","assumption":"新增需求不會壓縮既有遊戲客戶的報酬。","consequence":"總營收成長，但遊戲預算外流，混合抽成與留存下降。","ruling":"反駁但保留監測。Q3 遊戲年增近 50%，方向相反；不過這只是新架構第一季，投手行為要到 Q4 旺季後才看得清楚。","watch":"Q1 2027 遊戲年增率、MAX 份額的賣方查核。","evidence_refs":["end_markets#3"]},{"view":"價格已反映太多","evidence":"財報後盤後上漲 24% 到 25%，14 日 RSI 76.31；TTM 營益率 77.8% 是資料期內最高，FY2022 僅 −1.7%；淨收入口徑使利潤率比同業好看。","assumption":"現有利潤率可以延續，本益比分母沒有高估。","consequence":"若營益率回到 65%，EPS 約少 17%，Forward 本益比約 28 倍，便宜的說法不成立。","ruling":"反駁估值太貴，採納短線過熱。現在就賣的最強論證是利潤率在高峰且指標不透明，但自由現金流反推只要求十年年增 11% 到 15%。第一筆只建一半。","watch":"RSI、營益率、財報後 FY2027 EPS 共識更新。","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_rsi14","f_peer_app_operating_margin_pct","f_fwd_pe_latest"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 520.43 → 本次 391.22（-24.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=520.43","side_b":"本次 price_at_dd=391.22","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 520.43 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 520.43 美元：Bull 價 1,170、Bear 價 336，五年期望值 +55.0%，基準年化 9.7%，不對稱比 4.3","side_b":"本次情境、股價仍用 520.43 美元：Bull 價 1,207.5、Bear 價 253.5，五年期望值 +33.3%，基準年化 6.2%，不對稱比 2.14","ruling":"先換情境、股價不動：五年期望值少 21.7 個百分點，基準年化少 3.5 個百分點。不對稱比由 4.3 變為 2.14。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 520.43 美元：五年期望值 +33.3%，基準年化 6.2%，不對稱比 2.14","side_b":"本次情境、股價 391.22 美元：五年期望值 +77.3%，基準年化 12.4%，不對稱比 4.94","ruling":"再換股價、情境不動：起點價下跌 24.8%，五年期望值多 44.0 個百分點，基準年化多 6.2 個百分點，不對稱比由 2.14 升到 4.94。合計五年期望值比前份多 22.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與裁決變動","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 520.43 美元，估值中性，裁決為進場。","side_b":"本次股價 391.22 美元，Forward 本益比 23.5 倍，FY2027E 19.6 倍，估值偏便宜。","ruling":"股價下跌 24.8%，大於 FY2027E 共識 EPS 的下修 8.8%（21.93 到 20.01，兩次來源不同，僅看方向），所以估值結論上調。裁決與倉位角色依本次輸入重新計算。","evidence_level":"事實表價格與共識快照","settle_metric":"財報後更新的 FY2027E 共識 EPS 與 Forward 本益比","if_then":["若股價續漲而 Q4 財報尚未公布，不追，第二筆不提前。","若股價下跌但營收仍高於指引上緣，分批反買。"],"evidence_refs":[]},{"axis":"綜合訊號與價值陷阱","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份綜合訊號居中，陷阱風險中性。","side_b":"Q3 重新加速降低陷阱風險，但 Q2 模型斷檔與 EPS 高於營收成長的信號仍在。","ruling":"兩項都維持不變。好消息與壞消息互相抵銷，短線過熱也不支持上調。","evidence_level":"公司財報與法說","settle_metric":"Q4 2026 與 Q1 2027 營收對指引","if_then":["若連 2 季超過指引上緣，加碼至倉位上限。","若再次低於指引中點，減碼至一半。"],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"2026-08-05：Q2 模型提升斷檔，市場擔心競爭，CEO 說無需求或競爭變化。","side_b":"2026-11-04：新架構部分上線，遊戲年增近 50%，營收高於指引上緣約 1 億美元。","ruling":"維持持平。單季反彈不足以上調，新架構尚未全面上線；也沒有證據顯示份額下滑，不下調。","evidence_level":"法說逐字稿，份額僅賣方估算","settle_metric":"未來 2 季營收對指引與遊戲年增率","if_then":["若 Q4 與 Q1 都超過指引上緣且遊戲年增不低於 30%，方向上調，加碼至倉位上限。","若再次低於指引中點，方向下調並減碼至一半。"],"evidence_refs":["competitive_share_entrants#1","end_markets#3"]},{"axis":"第二曲線與跑道","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"Q3 消費端季增雙位數、年增三位數，第二曲線有實際成長。","side_b":"消費端金額未揭露；CEO 說走自助的小型商家要五年後才成熟，成功案例靠人工協助或成熟客戶。","ruling":"維持寬。總投放滲透率約 4.7%，且有已成長的第二曲線；但只給中等確信，Base 不採用管理層的 30%。","evidence_level":"法說與賣方估算","settle_metric":"消費端年增率與管理層揭露程度","if_then":["若連 2 季年增低於 50%，減碼三分之一並下調跑道。"],"evidence_refs":["end_markets#2","supply_demand_durability#1"]},{"axis":"情境機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct","archetype","cycle_position"],"side_a":"前份 Bull 30%、Bear 25%，最大回撤 −60%，類型為品質複利成長，循環位置未填。","side_b":"本次 Bull 25%、Bear 30%，最大回撤 −45% 到 −65%，類型相同，循環位置仍不適用。","ruling":"Bear 上調是因為共識成長超過資本公式上界，並反映 Q2 模型斷檔；最大回撤由單點改為範圍。公司不是循環股，類型不變。","evidence_level":"分析判斷","settle_metric":"FY2027 營收年增率","if_then":[],"evidence_refs":[]},{"axis":"成長門檻","cause":"新證據","prior_field":["H1"],"side_a":"AXON 廣告營收年增不低於 40%；連 2 季低於 25% 觸發重評。","side_b":"FY2027 營收不低於 104 億美元（年增約 25%）；單季年增連 2 季低於 25% 重評並減碼。","ruling":"下限 25% 延續，40% 取消。Q4 指引已是 43% 到 44%，共識 FY2027 為 25%，40% 不再是合理基準；apps 出售後，併表營收可作為廣告營收。","evidence_level":"公司指引與共識","settle_metric":"FY2027 季度營收","if_then":["若單季年增連 2 季低於 25%，減碼至一半。"],"evidence_refs":["end_markets#1"]},{"axis":"SEC 調查","cause":"新證據","prior_field":["R1"],"side_a":"證據索引仍記載 SEC 調查進行中（2026-02 報導），前份以 Wells Notice 為單事件減碼條件。","side_b":"CFO 於 2026-08-05 法說表示 SEC 已結束查詢，沒有建議採取行動。","ruling":"採信後者，因為它是較新的公司一手陳述，索引只是沒有抓到更新。本包沒有 SEC 結案文件或 10-Q 原文可核對，這是缺口。Wells Notice 減碼條件退休，改監測 FTC 與證券集體訴訟。","evidence_level":"管理層法說陳述，未見監管機關文件","settle_metric":"下一份 10-K 法律程序章節","if_then":["若 10-K 或新報導顯示 SEC 重啟調查，減碼至一半。"],"evidence_refs":["regulatory_antitrust#1","major_events#1","sec_investigation_restatement#0"]},{"axis":"重新定價論點","cause":"新證據","prior_field":["H3"],"side_a":"FY2027E EPS 共識不低於 21.9；Forward 分位回到 60% 以上；連 4 季下修 10% 才算偏離。","side_b":"FY2027E 共識 20.01，較前份低 8.8%；本次不再把倍數回升當論點，改為現金轉換與回購。","ruling":"舊論點還沒到正式反轉門檻，但股價由 520 美元跌到 391 美元，倍數回升沒有發生。Base 終端倍數 18 倍低於現值 23.5 倍，報酬不靠重新定價。","evidence_level":"共識快照，前後來源不同","settle_metric":"Base 報酬拆解中的倍數貢獻","if_then":[],"evidence_refs":[]},{"axis":"消費端門檻","cause":"方法變動","prior_field":["R2"],"side_a":"年化 ARR 連 2 季低於 3 億美元，或 go-live 轉換率連 2 季不升破 65%。","side_b":"保留上述門檻並標資料缺口；新增消費端年增連 2 季低於 50%，作為可觀察的減碼條件。","ruling":"公司不揭露 ARR 與轉換率，舊門檻取不到值，所以不刪除，但改用管理層每季會說的年增方向。","evidence_level":"法說口頭揭露","settle_metric":"消費端年增率","if_then":["若管理層不再揭露方向，視同未達，停止加碼。"],"evidence_refs":[]},{"axis":"加碼與重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"SEC 資料實務調查無重大處分結案／和解，或 e-com self-serve 年化 ARR 站上 $1.45B 且 go-live 轉換率升破 70%；回檔 $430-460 分批加碼","side_b":"第二筆加碼條件：Q4 財報（約 2027 年 2 月）營收不低於 23.95 億美元，或 14 日 RSI 回到 60 以下且營收論點未破","ruling":"舊條件的 SEC 一項依公司說法已達成，回檔區間也已跌穿；ARR 與轉換率公司不揭露，無法使用。新條件改看財報與動能，加碼分兩筆，減碼與清倉條件列在觸發清單。","evidence_level":"法說與事實表價格","settle_metric":"Q4 2026 營收","if_then":["若營收低於指引中點，取消第二筆。"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（原文為空）。","side_b":"FY2027 全年營收年增率跌破 20%，也就是低於約 100 億美元，等於新架構沒有帶來下一輪成長。","ruling":"本次補上 Single Thing，選營收成長而不是監管事件，因為 SEC 依公司說法已結束，而營收成長是 Y5 EPS 最大的單一敏感項。若發生則清倉。","evidence_level":"敏感度計算","settle_metric":"FY2027 全年營收","if_then":["若 FY2027 營收低於約 100 億美元，清倉。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設此欄；風險表的減碼條件為 Wells Notice 單事件、年化 ARR 連 2 季低於 3 億美元、遊戲廣告年增轉負連 3 季。","side_b":"本次設五項：FY2027 營收年增低於 20% 清倉；連 2 季低於指引中點減碼；EBITDA 利潤率連 2 季低於 75% 減碼；遊戲廣告年增轉負連 3 季減碼；消費端年增連 2 季低於 50% 減碼。","ruling":"把分散在風險表的條件集中成可檢查的清單，遊戲廣告門檻照舊，SEC 條件退休，ARR 改用可觀察的年增方向。","evidence_level":"分析判斷","settle_metric":"各項季度數字","if_then":[],"evidence_refs":[]},{"axis":"Q2 失誤歸因","cause":null,"prior_field":null,"side_a":"2026-08-05 CEO：Q2 失誤是模型改善步伐低於正常，沒有需求或競爭變化。","side_b":"同場問答未給具體診斷；2026-11-04 CEO 稱是自身失誤，Q3 遊戲年增近 50% 才提供旁證，但也說多家對手同時表現很好。","ruling":"未證、監測。Q3 支持這個說法，但一季反彈無法排除競爭因素。預先登記：連 2 季低於指引中點且管理層仍歸因模型，視為歸因不成立。","evidence_level":"法說逐字稿","settle_metric":"未來 2 季營收對指引中點","if_then":["若連 2 季低於指引中點，減碼至一半。"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-08-05 CFO：全年 FCF 轉換率約 75%。同日 CEO：創意是最大障礙；供給擴張先到非遊戲 App、再到開放網路、最後才是 CTV，目前不具備執行條件。","side_b":"2026-11-04 CFO：70% 到 75%。同日 CEO：創意不算障礙，是機會成本；CTV 列入明年重點，已有試點。","ruling":"轉換率下緣放寬屬小幅改口；創意措辭變軟但沒有數據；CTV 提前，但 CEO 自己說短期不要計入，情境也沒有計入。","evidence_level":"兩場法說逐字稿","settle_metric":"FY2026 全年 FCF 除以調整後 EBITDA","if_then":["若 FY2026 轉換率低於 70%，停止加碼。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：多家對手同時表現好，Android 較競爭，CloudX 等新進入者出現。","side_b":"結構：MAX 供給強雙位數成長，消費端擴大拍賣密度。其他結構變數：發行平台規則與 FTC 調查未決。","ruling":"雙向拉鋸。Q3 年增 55%，大型平台約 10% 到 20% 多，結構順風大於競爭壓力，但競爭壓力確實存在。","evidence_level":"法說與賣方估算","settle_metric":"MAX 份額與遊戲年增率","if_then":[],"evidence_refs":["end_markets#3","competitive_share_entrants#1"]}],"triggers":[{"n":1,"text":"Q4 2026 營收超過指引上緣，驗證新模型動能延續。","type":"假設驗證","maps_to":"H1","metric":"Q4 2026 營收","threshold":"不低於 23.95 億美元","action":"補上第二筆至目標倉位","source_freq":"公司 8-K，每季","date":"2027-02","evidence_refs":["capital_markets_pricing#1"]},{"n":2,"text":"FY2027 全年營收年增跌破 20%。","type":"Single Thing","maps_to":"H1","metric":"FY2027 營收年增率","threshold":"低於 20%（約 100 億美元）","action":"清倉","source_freq":"公司 8-K，每年","date":"2028-02"},{"n":3,"text":"營收連續兩季低於公司指引中點。","type":"減碼","maps_to":"R1","metric":"單季營收與指引中點差距","threshold":"連 2 季為負","action":"減碼至一半","source_freq":"公司 8-K，每季","date":"每季財報"},{"n":4,"text":"連兩季超過指引上緣且遊戲廣告維持高成長。","type":"加碼","maps_to":"H1","metric":"單季營收對指引上緣、遊戲廣告年增率","threshold":"連 2 季高於上緣，且遊戲年增不低於 30%","action":"加碼至倉位上限","source_freq":"8-K 與法說，每季","date":"2027-05"},{"n":5,"text":"消費端成長明顯放慢，或管理層不再揭露方向。","type":"風險","maps_to":"R2","metric":"消費端廣告支出年增率","threshold":"連 2 季低於 50%","action":"減碼三分之一","source_freq":"法說口頭揭露，每季","date":"每季財報"},{"n":6,"text":"發行平台改變規則，影響資料或 SDK。","type":"風險","maps_to":"R4","metric":"8-K、10-Q 揭露及 Apple、Google 政策公告","threshold":"公司揭露重大影響，或單季營收低於指引下緣","action":"減碼至一半","source_freq":"事件","date":"持續","evidence_refs":["geo_supply_chain#0"]},{"n":7,"text":"FTC 調查或證券集體訴訟程序惡化。","type":"風險","maps_to":"R5","metric":"10-K 法律程序章節、法院紀錄","threshold":"集體認證加不利和解；或刑事程序介入","action":"前者減碼至一半，後者清倉","source_freq":"事件","date":"持續","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","lawsuit_class_action#0","major_events#0"]},{"n":8,"text":"調整後 EBITDA 利潤率跌破管理層長期區間太多。","type":"減碼","maps_to":"H3","metric":"調整後 EBITDA 利潤率","threshold":"連 2 季低於 75%","action":"減碼至一半","source_freq":"公司 8-K，每季","date":"每季財報"},{"n":9,"text":"出現超過市值 5% 的資料或客戶併購。","type":"風險","maps_to":"H3","metric":"併購金額占市值","threshold":"超過 5%","action":"停止加碼並重做報告","source_freq":"8-K，事件","date":"持續"},{"n":10,"text":"日線過熱消退，可補第二筆。","type":"估值rearm","maps_to":"H1","metric":"14 日 RSI","threshold":"回到 60 以下且營收論點未破","action":"補上第二筆","source_freq":"每日","date":"持續"},{"n":11,"text":"Q4 財報後複審全部假設。","type":"複審日期","maps_to":null,"metric":"Q4 2026 財報、Q1 2027 指引","threshold":"財報公布","action":"重新檢查情境與門檻","source_freq":"公司 8-K","date":"2027-02"}],"kill_metrics":[{"metric":"FY2027 全年營收年增率","bear_threshold":"低於 20%（約 100 億美元）","window":"FY2027 全年，2028 年 2 月確認","source":"公司 8-K 新聞稿","last_status":"ok"},{"metric":"單季營收與公司指引中點比較","bear_threshold":"連 2 季低於指引中點","window":"每季","source":"公司 8-K 新聞稿","last_status":"ok"},{"metric":"調整後 EBITDA 利潤率","bear_threshold":"連 2 季低於 75%","window":"每季","source":"公司 8-K 新聞稿","last_status":"ok"},{"metric":"遊戲廣告年增率","bear_threshold":"轉負且非季節性，連 3 季","window":"每季","source":"法說口頭揭露","last_status":"ok"},{"metric":"消費端廣告支出年增率","bear_threshold":"連 2 季低於 50%，或管理層不再揭露方向","window":"每季","source":"法說口頭揭露；金額未揭露","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Q2 單季模型斷檔外推成成長熄火：現價只隱含未來十年自由現金流年增 11% 到 15%，但 Q4 指引仍年增 43% 到 44%，共識 FY2027 營收年增 25%，管理層長期目標約 30%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟢', moat_trend='→', week26=-16.5, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"第二筆加碼條件：Q4 財報（約 2027 年 2 月）營收不低於 23.95 億美元，或 14 日 RSI 回到 60 以下且營收論點未破","exec_line":"股價財報後跳升、日線過熱，第一筆只建目標倉位一半，第二筆依加碼條件執行。跌到 250 週均線附近本身不是賣出理由，賣出只看論點門檻。"},"reasoning":{"industry":"收錢方式：廣告主按成效目標投放，AppLovin 在單一拍賣中競價買曝光，以淨收入計算營收。Q3 2026 營收 2,184.8 百萬美元，年增 55%；GAAP 營業利益 1,709.0 百萬美元，營益率 78.2%；調整後 EBITDA 利潤率 84.3%；TTM 毛利率 88.8%。公司已出售 apps，不再分段揭露。遊戲 Q3 年增近 50%，消費端年增三位數，金額都未揭露。景氣位置判在擴張期，依據是 Q3 消費端季增雙位數、MAX 供給維持強雙位數成長（2026-11-04 法說），不是股價。單點依賴有三個：Apple、Google、Meta 等少數發行平台；遊戲廣告仍是主體；成長靠模型團隊持續做出提升，管理層自己說節奏無法預測。客戶端不集中，FY2025 無單一客戶超過營收 10%。總投放約 200 億美元年化是 JPMorgan 分析師在 Q3 法說上的轉述，對照淨收入年化約 87 億美元，推算抽成約 44%；管理層不談抽成。","moat":"機制：MAX 中介在手遊占 70% 以上、AppLovin Ads 占 DSP 40% 以上（JPMorgan 估算），曝光回饋訓練 AXON，模型越準出價越高，再吸引更多預算。方向用利潤率代替 ROIC 差距：APP 營益率 FY2024 59.3%、FY2025 75.8%、TTM 77.8%，高於 META 32.9%、GOOGL 33.3%、TTD 19.6%；同業歷史序列與 ROIC 事實表未涵蓋，且 APP 以淨收入計，比較會偏高。執行面擴大：Q3 超過指引上緣約 1 億美元，管理層自述 16 季有 14 季超過上緣。定價力穩定：CEO 明說領先才能多拿，跟上市場則持平，落後就會被壓縮。兩者合起來判持平。當期 ROIC 無法計算，因投入資本事實表未涵蓋；FY2024、FY2025 自由現金流都高於淨利，再投資率接近零甚至為負，成長主要靠費用化的研發與算力，公式算出的內生成長上界沒有參考價值。","growth":"成長組成：量與模型提升為主，併購為零，回購每年約貢獻 2%。共識 EPS 三年 CAGR 35.5%（FY2025A 9.75 到 FY2028E 24.27，Koyfin 快照，事實表未列家數），其中 FY2026 已大致兌現，FY2026E 到 FY2028E 只有 20.7%。共識營收 FY2027 年增 25.1%，管理層長期目標約 30%。缺口歸因於費用化的研發與算力、利潤率擴張與回購。跑道年數：總投放約 200 億美元，對 in-app 廣告 4,262 億美元約 4.7%；以 30% 成長、市場年增約 8%，約 10 年達 30% 滲透率，但分母包含大型封閉平台，實際可及市場較小，因此只給中等確信。衰退信號亮 1 個：FY2025 到 FY2027 EPS CAGR 43.3% 高於營收 CAGR 38.0%，差 5.3 個百分點，主因是 FY2026 的利潤率與股數；FY2026 之後反轉為 EPS 成長低於營收。","governance":"FY2025 自由現金流為淨利 1.18 倍，FY2024 為 1.31 倍。Q3 SBC 84.2 百萬美元，占營收 3.9%。Q3 回購與扣繳 410 萬股共 14 億美元，約等於當季自由現金流，均價約 341 美元；董事會增加授權 32 億美元，總授權 36 億美元。累計 1.04 億股、94 億美元，均價 90 美元，占期間自由現金流 85%。淨槓桿低於 0.1 倍，公司長期目標約 1 倍。現金去向四分與債務到期結構事實表未涵蓋。主要風險是 CEO 提到可能用併購買資料與客戶關係，目前沒有具體案子。","valuation":"TTM 營收約 76.1 億美元（EV 1,299.6 億美元除以 EV/S 17.08 倍），FCF 利潤率 64.07%，TTM 自由現金流約 48.7 億美元。以折現率 10%、永續成長 3% 反推，現價需要自由現金流十年年增約 11%；折現率 12% 時約 15%。Base 十年平均 EPS 成長約 14%，高於前者、略低於後者。同業倍數事實表未涵蓋，終端倍數無法附同業現值對照，只能用公司現值 23.5 倍與終端成長率推定，這是缺口。短線 14 日 RSI 76.31，26 週報酬 −16.5%，屬於跌深後的跳升。","premortem":"五年敏感度以 Base 的 FY2031E EPS 39 美元、終端價 702 美元為準：營收 CAGR 少 5 個百分點，EPS 約 −19%，年化報酬降到 7.7%；淨利率少 5 個百分點，EPS 約 −8%，報酬 10.5%；不回購，EPS 約 −9%，報酬 10.2%；終端倍數少 3 倍，價格 −17%，報酬 8.4%。營收成長是最大的單一敏感項，四項壓力中有三項年化仍高於 8%。事實表未涵蓋歷史最大回撤，訴訟金額與時點也未揭露。2026-08-05 法說有三次迴避：模型斷檔原因未具體診斷、開放平台後的廣告主數量未提供、Q3 之後的算力金額未給。2026-11-04 法說 CEO 也不談抽成，並表示外界只能自己猜。"},"plain":{"six":{"how_it_makes_money":"賺遊戲與消費品牌廣告主的成效預算，錢卡在 AXON 預測模型加 MAX 拍賣這一節點，Q3 淨收入 21.8 億美元，營益率 78%。","moat":"→ 護城河方向持平：Q3 遊戲重新加速證明模型能力仍在，但新架構只是部分上線，Q2 又剛出現模型斷檔，單季不足以上調。","growth":"🟢 跑道寬：消費端仍在早期且已有實際成長，總投放滲透率僅約 5%；但第二曲線的金額未揭露，確信度只到中等。","capital":"資本配置良好：稀釋股數連 8 季下降，累計回購均價 90 美元遠低於現價，SBC 低。","valuation":"現價要求未來十年自由現金流年增約 11% 到 15%，我相信做得到，估值偏便宜；但財報後短線過熱，不宜一次買滿。","how_wrong":"最可能看錯的是把 Q3 當成新一輪模型週期的開始；Q2 的斷檔若重演，EPS 與倍數會一起下修。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Q2 單季模型斷檔外推成成長熄火：現價只隱含未來十年自由現金流年增 11% 到 15%，但 Q4 指引仍年增 43% 到 44%，共識 FY2027 營收年增 25%，管理層長期目標約 30%。","momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟢","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"A","archetype":"品質複利成長","price_at_dd":391.22,"week26_return_pct":-16.5,"consensus_rev_3m_pct":0.85,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母沒有明顯一次性項目爭議，但 Koyfin EPS 快照在財報前後同為 16.65、20.01、24.27，可能尚未反映 Q3 與 Q4 指引；以 FY2027E 共識營收 104 億美元、淨利率 66%、3.25 億股粗算，EPS 約 21 美元。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 Q1 2027 指引，首次檢驗新模型與電商旺季","impact":"高","watch":"營收是否不低於 23.95 億美元，遊戲與消費端年增描述"},{"date":"2027-02","date_precision":"month","type":"regulatory","event":"FY2026 10-K 更新法律程序與 SEC、FTC 相關揭露","impact":"中","watch":"SEC 結案文字、FTC 進度、集體訴訟階段"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"Q1 2027 財報，消費端季節性回落後的第一個讀數","impact":"高","watch":"季增是否仍為正，新架構部署進度"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s4`：現在 1,437B，下限 1,500B，**目標 ≥ 1,800B**
- `s5`：現在 2,707B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/APP_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s4 -->
<section id="s4"><h2>4　生意品質門檻</h2>
<p class="lead">需求端穩，供給端有黏性，但客戶沒有合約鎖定。</p>
<ul class="pts">
<li>需求基礎值成立。使用者是玩家，決策者是投手，付款者是廣告主，三者都有明確角色。廣告主以 ROAS 自付，CEO 稱每年為廣告主帶來數百億美元營收。風險是消費端仍被部分廣告主當成測試預算。</li>
<li>決策層級偏弱。替代要看單一廣告活動與單一曝光，投手可以當天把預算移走，沒有合約。供給端的 MAX 份額在 70% 以上，黏性較高。需求端主要靠效果留客，消費端廣告主還要跑增量測試才會放量。</li>
<li>價值鏈分配對 APP 不全然有利。Apple、Google、Meta 控制發行與資料規則，發行商收益隨拍賣上漲，CEO 承認公司要靠技術進步吸收。他也直說領先才能多拿，落後就會被壓縮。</li>
<li>社會容忍度有爭議。全螢幕廣告佔滿畫面，CEO 稱平均觀看超過 35 秒。資料做法曾受 SEC 與 FTC 關注。CFO 說 SEC 查詢已結束，FTC 未見進展，證券集體訴訟仍在進行，本包沒有 SEC 結案文件可核對。</li>
<li>客戶端分散。FY2025 沒有單一客戶超過營收 10%，這降低了單一客戶流失的風險。但分散的另一面是沒有合約，廣告主離開的成本很低，APP 必須每天靠成效證明自己。</li>
</ul></section>

```

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">資料飛輪成立，但護城河評為 B，方向持平。</p>
<ul class="pts">
<li>機制是 MAX 拍賣的供給規模加 AXON 預測模型形成資料飛輪。單一拍賣同時服務遊戲與消費廣告主，曝光回饋訓練模型，預測越準，出價與預算越多。這個循環已經運轉多年，Q3 超過指引上緣約 1 億美元，管理層稱 16 季有 14 季超過上緣。</li>
<li>執行面給 9 分，定價力給 7 分，合起來評 B。執行面擴大是因為新架構部分上線就帶動超預期。定價力穩定是因為 CEO 說領先才能多拿，跟上市場則持平，落後就會被壓縮。兩者合起來判持平，不是上調。</li>
<li>利潤率明顯高於同業。APP 營益率 FY2024 為 59.3%，FY2025 為 75.8%，TTM 為 77.8%，META 為 32.9%，GOOGL 為 33.3%，TTD 為 19.6%。必須提醒，APP 以淨收入計，利潤率比同業好看。同業 ROIC 事實表沒有涵蓋，所以用營益率差距代替。</li>
<li>最大的威脅來自生態攻擊，我們估機率 30%。Google 在 Android 上既是平台也是大型對手，Apple、Google、Meta 掌握發行與資料規則，Meta、Amazon、Unity 同時是客戶與對手。APP 研發密度 5.0%，META 為 31.7%，GOOGL 為 15.8%，模型競賽的資源並不對等。</li>
<li>點對點的威脅有兩項。CloudX 以免 SDK 模式切入，2026-02 推出時 APP 股價下跌約 13%，但 Q3 遊戲年增近 50%，沒有看到受損。UBS 在法說上提到部分廣告主預期拍賣價格上漲而先把預算移往對手，CEO 認為樣本有偏誤，但沒有提供份額數字。</li>
<li>報酬持續期要看四個檢查點。需求基礎值為綠，決策層級、價值鏈分配、社會容忍度都是黃。投入資本事實表未涵蓋，ROIIC 無法計算。FY2024 到 FY2025 營業利益增加約 22.4 億美元，新增有形資本很少，比值沒有意義。</li>
<li>再投資率接近零甚至為負，FY2024、FY2025 自由現金流分別是淨利的 1.31 倍與 1.18 倍。成長投入走費用，增量報酬乘再投資率的公式在此不適用，公式上界趨近零。共識成長必然超過上界，所以 Bear 機率取 30%。</li>
<li>護城河方向維持持平。上行證據是 Q3 遊戲年增近 50%，消費端增加拍賣密度。下行證據是 Q2 模型斷檔造成未達指引，CEO 承認多家對手同時表現很好，Android 較競爭。份額只有 2026 年 Q1 的賣方查核，所以不上調。</li>
</ul>
<h3>5｜二維評分與 Moat-to-Numbers</h3>
<!-- E5 -->
<h3>5.F｜對手財務深度對照</h3>
<!-- E6 -->
<h3>5.R｜報酬持續期檢核</h3>
<!-- E7 -->
</section>

```