你是 stock-analyst v20 的**散文層（prose）agent**，標的 MS（2026-10-18）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MS_20261018/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

每章 3–6 條，每條 100–200 字；s10（估值與三種未來）與 s12（最可能怎麼賠）至少 1,500 bytes，把情境輸入、終端倍數、反證三視角的裁定鋪開。

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

標的：MS　日期：2026-10-18　archetype：None　前份裁決：2026-07-16　觀望｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1563B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（413B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（492B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1382B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（827B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（570B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（729B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1950B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3663B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2141B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1563           3806-5437      5 條（2–6 內）  
s3                  8000         413           5311-7587      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2701          8609-12299      5 條（2–6 內）  
s6                 11000         570          7301-10430      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         729           1940-2771      5 條（2–6 內）  
s10                 5000        1950           2135-3050      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2141           2000-2859      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3945B；至少需散文≈41.05KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−45
−45%
−42%
−30
−30%
−21%
−21.0%
−18%
−7%
−3.33
0
0.15
0.25
0.33
0.35
0.70%
0.7%
0.75
0.8%
0.93
1
01
1.06
1.1
1.12
1.15
1.48
1.5
1.5%
1.7
2
2%
2.05
2.2%
2.3%
2.3
2.6
03
3
3.155
3.3
3.39
3.4
3.5
04
4
4.3%
4.6%
4.60
4.7
4.8%
4.8
4.9
5
5%
5.1
5.5%
5.6%
5.8%
6
06
6%
6.6
6.7%
6.9%
07
7
7%
7.5%
7.5
08
8%
8
8.9
9
9.5%
10
10%
10.21
10.5
11
11.3
11.4
11.8%
12
12%
12.3%
12.4
12.6%
12.75
13.0%
13
13%
13.3
13.31
13.5
13.5%
13.57
14%
14
14.16
14.2
14.32
14.4
14.56
14.59
14.9%
14.9
15
15%
15.4
15.71
15.9
16
16%
16.9
17
17.2
18%
18
18.4%
18.6
20%
20
20.2
21%
21.0%
22
22.6%
23%
24
24.9%
25%
25
26
26.8
27.6%
28%
28
30
30%
30.4%
31
31%
31.9%
33%
34
35%
36%
39%
41%
42
43%
45
45%
49%
49
50
52%
55
58
60
61.6
62
64.78
65%
66%
67%
70
79.97
80
90
90%
90.65
94
99%
100
100%
100.29
101
105
120
142
145
146.3
150%
158
166
180
$180
180.57
184
190.02
200
203.38
220
222
228.55
262
300
320
389
805
814
2022
2024
2025
2026
2027
2028
2031
20261018
2,000
2,100
2,324
3,000
8,400
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
{"meta":{"ticker":"MS","date":"2026-10-18","schema":"v15.2","contract":"v19","company_name":"Morgan Stanley"},"oneliner":"財富管理的資產累積撐住報酬，但 2026 年盈餘含股票交易與 AI 融資的週期高點；股價跌到前瞻 14.2 倍只算合理，先不建倉，等 166 美元或第四季確認信用與淨新增資產再分批","thesis":{"H":[{"id":"H1","text":"財富管理是結構性複利：漏斗（E*TRADE、職場股票計畫、顧問）持續把新資產轉進收費帳戶，稅前利益率隨規模擴張","2y":null,"5y":"FY2031 前財富管理淨營收年化成長 ≥7%，稅前利益率 ≥30%","10y":null,"threshold":"淨新增資產年化 ≥3,000 億美元（對應三年一兆）；財富管理稅前利益率 ≥28%","source":"季報新聞稿財富管理分部、季度法說","drift_rule":"TTM 淨新增資產低於 3,000 億：連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"},{"id":"H2","text":"全公司報酬穿越循環仍高於資本成本：機構證券回落時，財富管理撐住 ROTCE 不跌破 15%","2y":null,"5y":"2027–2031 每年 ROTCE ≥15%，跨循環平均 ≥18%","10y":null,"threshold":"季度 ROTCE ≥15%；機構證券季營收 ≥80 億美元","source":"季報新聞稿 ROTCE 與分部營收","drift_rule":"TTM ROTCE 低於 18%：連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"},{"id":"H3","text":"超額資本轉成股東回報：資本規則定案後，超額 CET1 支撐每年至少 60 億回購與股息成長","2y":"2027–2028 回購合計 ≥120 億美元，CET1 維持 ≥13.5%","5y":null,"10y":null,"threshold":"CET1 ≥13.5%；年回購 ≥60 億美元","source":"季報新聞稿資本段、Fed 年度壓力測試結果","drift_rule":"TTM 回購低於 60 億：連 2 季偏離 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"資本市場量能回落：9 月起各資產類別量能轉弱；關稅或地緣事件會讓客戶延後併購，2025-04 關稅宣布當日股價跌 9.5%","h_ref":"H2","clock":"⚡","threshold":"機構證券季營收連 2 季年減","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R2","text":"信用循環轉差：第三季撥備 1.48 億（去年同期為零），沖銷集中在企業與商用不動產放款；私募信貸違約率創紀錄","h_ref":"H2","clock":"🔥","threshold":"全公司撥備單季 ≥3 億美元且連 2 季，或淨沖銷單季 ≥2 億","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#3"]},{"id":"R3","text":"資本規則翻轉：放寬提案尚未定案，參議院民主黨議員要求撤回並重提更嚴版本","h_ref":"H3","clock":"🐢","threshold":"最終規則使標準法 CET1 要求較 11.8% 上升 ≥50bp","evidence_refs":["financial_regulatory_capital_rules#2"]},{"id":"R4","text":"訴訟與監管：掃款集體訴訟、VRDO 與利率交換反壟斷訴訟仍在進行；前份列的 AML 程序在本包沒有新進展","h_ref":"H1","clock":"🔥","threshold":"進入集體認證，或任一案和解、罰金超過 5 億美元，或出現 AML 同意令（本包無新進展，資料缺口）","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0"]}],"single_thing":{"description":"AI 資本支出循環在 2027 年底前實質降速（大型雲端業者資本支出年增轉負），同時帶走股票交易、IPO 承銷與 IPO 相關的淨新增資產","why_fatal":"本季股票交易年增 41%，淨新增資產過半與 IPO 相關，管理層自稱對 AI「雙倍加碼」。三條收入線共用同一個驅動因子，是 Bear 情境 EPS 由 12.75 跌到 10.5 的最大單一來源，無法靠業務分散","if_happens":"減碼一半，暫停加碼，直到剔除 IPO 後的淨新增資產連 2 季守住年化 3,000 億","how_monitor":"每季看三個數字：大型雲端業者資本支出指引、MS 股票交易營收年增率、IPO 相關占淨新增資產比重。執行長本季估 AI 年資本支出約 1 兆美元，並說未必再加速","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.31,"peg_fy2":1.06,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":10.21,"FY2026E":12.75,"FY2027E":13.57,"FY2028E":14.56},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識取 Koyfin 2026-10-08 快照，基期為 FY2025 年報稀釋 EPS"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MS_20261018/scenario.json","archetype":{"primary":"金融","secondary":"品質複利成長","confidence":"高","fingerprint":"券商加財富管理平台，旗下有銀行子公司；報酬看 ROTCE 與 CET1，不看 FCF"},"industry":{"clock_phase":"II","sd_verdict_source":"混合：機構證券屬週期性、將隨市場量能反轉（9 月已轉弱）；財富管理資產累積屬結構性持久（六年兩兆淨新增資產，本季法說）","bargaining":{"up":"人才環節議價強，薪酬福利約占淨營收 39%","down":"客戶分散，年報未揭露單一客戶營收占比；議價集中在費率與掃款利率","geo":"全球布局，亞洲與日本（與 MUFG 合作）是管理層點名的優勢區"},"profit_pool_dir":"投行利潤池往大型整合行集中：前十大投行份額合計年增 3.4pp，MS 排第三，落後摩根大通與高盛","tam_table":{"expanded":false,"reason":"金融業跑道看客戶資產、放款與存款成長，不看 TAM 滲透率；美國財富管理總資產池事實表未涵蓋，滲透率無法計算"}},"moat":{"mechanism":"財富管理三層漏斗（自主交易、職場股票計畫、顧問）把新財富導入收費帳戶，加上機構股票業務的全球規模；資產規模帶來另類產品通路與資料優勢","execution":8,"pricing":7,"combined":7.5,"score":7.5,"grade":"B","trend":"→","trend_evidence":"執行面擴大：六年累計逾 2 兆淨新增資產、顧問留任率 99% 以上。定價面持穩：掃款利差受訴訟挑戰，投行份額動能落後高盛。最近兩季淨新增資產皆過半與 IPO 相關，同業報酬差距事實表未涵蓋，向上方向證不出來","peer_na_reason":"同業對照只有 FCF 利潤率，銀行的 FCF 由交易資產與放款變動主導，不具可比性；同業 ROTCE 與 P/TBV 事實表未涵蓋","threats":[{"level":"🟡","text":"高盛投行動能領先：上半年投行費用年增 52%，MS 第三季投行僅 +2% 且低於預期。屬點對點份額競爭，不扣分，但壓住投行定價力","p":0.35,"evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"掃款利差受法律壓力：紐約南區合併集體訴訟以契約與受託義務為由，主張掃款利率過低；若敗訴或和解，財富管理利差下修","p":0.25,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"level":"🟡","text":"AI 代理式理財與代幣化股票可能壓低顧問費率。管理層本季主張規模、獨家產品與資料會讓科技站在 MS 這邊；費率趨勢事實表未涵蓋","p":0.15,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是家戶（決策時有顧問參與），三者一致；財富傳承、退休與稅務規劃屬於需要，不是想要。代理讀數：客戶關係近 2,100 萬，六年累計淨新增資產逾 2 兆美元（本季法說）"},{"item":"決策層級","level":"🟡","text":"替代性要在家戶與單一顧問之間衡量。顧問留任率 99% 以上（執行長本季說法），但 IPO 相關資產解禁後可被賣出或移走；管理層只說保留率穩定，未給數字。漲價後的流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"MS 是資產管理業最大的經銷商，另類產品有獨家條件，在經銷環節有議價力；但人才環節拿走很大一份，本季薪酬福利約占淨營收 39%，顧問與交易員是最難取代的一環"},{"item":"社會容忍度","level":"🟡","text":"掃款利率已引發集體訴訟，客戶現金的利差有法律與社會上限。資本規則屬監管授權：2026-03 提案放寬，但參議院民主黨議員 2026-06 要求撤回，政策可以翻轉"}],"roiic":"事實表未涵蓋有形普通股權益序列，無法算增量報酬；以當期 ROTCE 22.6% 代理，結果偏樂觀","reinvest_rate":0.33,"endo_ceiling":7.5,"formula_note":"內生成長＝ROTCE 22.6%×保留率約 33%。保留率＝1−股息發放率約 36%（4.60÷12.75）−回購占淨利約 31%（年化回購 61.6 億÷FY2026 共識淨利約 200 億）；季股息 1.15 美元見 2026-07-15 前一季法說"},"spread_table":[{"metric":"FCF 利潤率","MS":-25.44,"JPM":-83.39,"GS":-62.71,"BAC":73.37,"WFC":22.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"JPM","fcf_margin":-83.39,"strategy_note":"投行費用榜首（101 億美元），有綜合銀行的資產負債表與低成本存款，是投行與企業放款最強的對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"GS","fcf_margin":-62.71,"strategy_note":"2026 上半年投行費用年增 52%、股票承銷 +90%，MS 第三季投行僅 +2%；投行份額動能目前領先 MS","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BAC","fcf_margin":73.37,"strategy_note":"旗下 Merrill 是財富管理的正面對手，存款基礎厚；其淨新增資產事實表未涵蓋，份額無法比較","period":"TTM ending 2026-06-30（4季加總）"},{"name":"WFC","fcf_margin":22.09,"strategy_note":"財富管理有規模，但投行與交易業務小；FCF 利潤率對銀行不具可比性","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（客戶資產、存款與放款成長）為主，價（資產費隨市值）其次，再加回購減股每年約 2%；無併購","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段內生成長 7.5%（ROTCE 22.6%×保留率 33%），不另算","segments":[{"item":"財富管理","value":"第三季淨營收 90.65 億美元，稅前利益率 30.4%，淨新增資產 2,324 億（過半與 IPO 相關），收費型流入 805 億"},{"item":"機構證券","value":"第三季淨營收 100.29 億，年增 18%；股票 58 億（+41%）、投行 22 億（+2%）、固定收益約 20 億（−7%）"},{"item":"投資管理","value":"第三季淨營收 14.59 億，低於去年的 17 億，主因私募基金附帶權益回沖；長期淨流入 158 億"}],"decay_signals":[{"signal":"EPS CAGR 顯著高於營收 CAGR","lit":true,"note":"FY2022→FY2025 稀釋 EPS 年化 18.4%、營收 9.5%，差 8.9pp，部分來自回購與週期利潤率"},{"signal":"FCF／淨利 < 0.75 連 2 年","lit":false,"note":"金融業不適用：FCF 由交易資產與放款變動主導"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"投行份額動能落後高盛，但 MS 同期份額數字事實表未涵蓋，未亮燈"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"trailing 本益比落在 4 個年度端點的 34 分位，未見系統性下移"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；股東回報以回購與股息為主，金額已在說明中列出"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近六年無重大併購；管理層 2026-07-15 表示偏向有機成長，E*TRADE 的增量報酬事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購買入收益率約 6.7%（FY2026 共識 EPS 12.75÷快照價 190.02）；10 年期公債殖利率事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"股權激勵淨稀釋率事實表未涵蓋","grade":"不過"}]},"valuation":{"basis":"前瞻本益比搭配合理 P/TBV 對 ROTCE（金融業主錨）","tier":"大型整合券商與投行","peers":{"expanded":false,"reason":"事實表同業對照只有 FCF 利潤率，沒有同業本益比、P/TBV 或 ROTCE，不能當估值錨"},"fwd_pe":14.16,"peg":1.12,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 14.2 倍。合理 P/TBV 在跨循環 ROTCE 18% 時約 2.6 倍、在 22.6% 時約 3.5 倍，現價約 3.3 倍（前份換算，本包無每股有形淨值），落在中間偏高；年度端點分位 34 只有 4 個點，不是五年分位，所以五年分位留空。結論：合理不便宜","upside_short_pct":4.7,"upside_mid_pct":31.0},"trap_analysis":{"verdict":"🟡","label":"週期高點盈餘被當成常態"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"本季股票交易年增 41%，分析師稱股票營收接近 2024 年兩倍；淨新增資產過半與 IPO 相關；第三季撥備 1.48 億，高於預期約 8,400 萬；私募信貸違約率創 6% 紀錄；2025-04 關稅宣布當日股價跌 9.5%；高盛投行動能領先","assumption":"財富管理的盈餘地板能抵銷機構證券的回落","consequence":"AI 融資與資本市場同步退潮時，EPS 回到 10 到 11 美元，倍數壓到 10 倍，五年後股價約在 105 到 145 美元，加股息仍虧損","ruling":"部分採納：Bear 機率給 30%，不一次買足。反駁的部分：財富管理稅前利益已占全公司約 43%，2022 年那種營收持平的年份 EPS 仍有 5 美元以上，盈餘不會歸零","watch":"機構證券季營收年增率、全公司撥備、IPO 相關占淨新增資產比重","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#3","reg_tariff_export#1","competitive_share_entrants#2"],"fact_refs":["f_kpi9","f_kpi8"]},{"view":"論點成功但股東經濟變差","evidence":"本季存款季增近 300 億，主要是較高成本的種類，淨利息收入 22 億不升反降（前一季財務長原指引小幅季增）；掃款集體訴訟主張利率過低；參議院民主黨議員要求撤回放寬資本的提案","assumption":"資產增加會等比例轉成利差與費收，超額資本可自由回饋股東","consequence":"資產照樣成長，但每塊錢的利差被壓縮，超額資本被更嚴的規則鎖住，回購放慢，每股 EPS 成長低於資產成長","ruling":"採納為監測項，不改基準。財務長稱融資效益明年才顯現，第四季淨利息收入指引小幅回升；先標未證，若 2027 上半年仍季減，就視為歸因證偽","watch":"財富管理淨利息收入季增率、掃款訴訟程序、資本規則定案內容","evidence_refs":["major_events#0","lawsuit_class_action#0","financial_regulatory_capital_rules#2"],"fact_refs":["f_kpi11_cet1"]},{"view":"價格已反映太多","evidence":"現價約 3.3 倍有形淨值（前份換算）；ROTCE 22.6% 下的合理值約 3.5 倍，跨循環 18% 下約 2.6 倍；賣方均價目標 222 美元","assumption":"市場會繼續按高點報酬定價","consequence":"若 ROTCE 回到 18%，合理倍數下修約兩成，即使盈餘持平，股價也沒有空間","ruling":"採納部分：估值結論只給合理、不給便宜，加碼價設在前瞻 13 倍（約 166 美元）","watch":"季度 ROTCE 是否在機構證券回落時仍守 18%","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_kpi5_rotce"]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 228.55 → 本次 180.57（-21.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=228.55","side_b":"本次 price_at_dd=180.57","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 228.55 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 228.55 美元：Bull 價 389、Bear 價 142，五年期望值 +21.0%，基準年化 5.5%，不對稱比 1.5","side_b":"本次情境、股價仍用 228.55 美元：Bull 價 320、Bear 價 146.3，五年期望值 +0.8%，基準年化 0.7%，不對稱比 0.93","ruling":"先換情境、股價不動：五年期望值少 20.2 個百分點，基準年化少 4.8 個百分點。不對稱比由 1.5 變為 0.93。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 228.55 美元：五年期望值 +0.8%，基準年化 0.7%，不對稱比 0.93","side_b":"本次情境、股價 180.57 美元：五年期望值 +27.6%，基準年化 5.6%，不對稱比 3.39","ruling":"再換股價、情境不動：起點價下跌 21.0%，五年期望值多 26.8 個百分點，基準年化多 4.9 個百分點，不對稱比由 0.93 升到 3.39。合計五年期望值比前份多 6.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：資本與獲利品質","cause":null,"prior_field":null,"side_a":"ROTCE 22.6%，連 5 季高於 20%；CET1 14.9%，高於要求約 300bp","side_b":"管理層與前份都認為資本緩衝充足、財富管理稅前利益率守在 30%","ruling":"兩邊一致：資本與獲利品質不是本份的爭點","evidence_level":"一手財報","settle_metric":"季度 ROTCE 與 CET1","if_then":[],"evidence_refs":[]},{"axis":"管理層指引與兌現","cause":null,"prior_field":null,"side_a":"2026-07-15 前一季法說：財務長 Sharon Yeshaya 指引第三季財富管理淨利息收入小幅季增；執行長 Ted Pick 說投行展望正面；上半年效率比 65%","side_b":"2026-10-14 本季法說：財務長說淨利息收入 22 億小幅下降，原因是存款增加且結構轉向較高成本；投行只年增 2%，低於預期約 1.1 億；年初至今效率比升到 66%","ruling":"可調和，屬程度差異。淨利息收入落差來自主動吸收存款，第四季指引小幅回升，先標未證、監測。投行落差屬時點問題，管線說法沒變","evidence_level":"一手逐字稿","settle_metric":"2026 第四季與 2027 第一季財富管理淨利息收入季增率","if_then":["若 2027 第一季淨利息收入仍季減，則把存款策略視為壓利差，停止加碼","反向：若連 2 季季增且存款續增，則確認銀行融資效益，按原計畫加碼第二批"],"evidence_refs":[]},{"axis":"淨新增資產的結構性","cause":null,"prior_field":null,"side_a":"執行長：收購 E*TRADE 後三年一兆、再三年一兆，漏斗會自我強化；財務長：IPO 資產保留率穩定","side_b":"2026-07-15 前一季：IPO 相關約占淨新增資產略過半；2026-10-14 本季：再度略過半，收費型流入 805 億裡近半來自單一企業退休金委託","ruling":"可調和：六年兩兆是多年實績，結構性成立；但最近兩季的紀錄有過半屬事件性來源，2,324 億不能當新的季度常態。H1 門檻用年化 3,000 億（對應三年一兆），不用單季紀錄","evidence_level":"一手逐字稿","settle_metric":"剔除 IPO 相關後的淨新增資產（看公司是否揭露）","if_then":["若剔除 IPO 後連 2 季年化低於 2,000 億，則減碼一半","反向：若 IPO 冷卻季的淨新增資產仍有年化 3,000 億，則加碼第二批"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：資本規則提案估計最大型銀行 CET1 要求降約 4.8%，前十大投行份額合計年增 3.4pp","side_b":"競爭惡化：高盛上半年投行費用 +52%，MS 第三季 +2%；其他結構變數（法規軸）：參議院民主黨議員要求撤回放寬提案、反壟斷與掃款訴訟仍在進行","ruling":"雙向拉鋸：結構面轉好，競爭面在投行一塊轉差，法規軸可能翻轉。淨效果不足以改變基準情境","evidence_level":"一手文件加二手彙整","settle_metric":"資本規則最終版本、MS 投行份額排名","if_then":["若最終規則使 CET1 要求上升至少 50bp，則下修回購假設並減碼","反向：若 2026 年內按提案定案，則上調回購假設"],"evidence_refs":["competitive_share_entrants#2","financial_regulatory_capital_rules#2","regulatory_antitrust#0"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣方：股票營收接近 2024 年兩倍，IPO 撐起淨新增資產，撥備高於預期，私募信貸違約創紀錄；9 月量能已轉弱，執行長自己說第四季到 2027 上半年是關鍵十字路口，現在的 EPS 就是高點","side_b":"買方：財富管理稅前利益已占約 43%，股價三個月跌 21% 到前瞻 14.2 倍，RSI 25 屬超賣，超額資本 300bp 可在回檔時回購","ruling":"部分採納賣方：現價先不建倉，等 166 美元或第四季確認後才建首批，不一次買足；Bear 機率給 30%","evidence_level":"一手財報加產業數據","settle_metric":"機構證券營收年增率與全公司撥備","if_then":["若機構證券營收連 2 季年減，且撥備單季至少 3 億，則減碼一半","反向：若股價續跌但 ROTCE 守在 18% 以上、CET1 至少 14%，則分批反買到目標倉位"],"evidence_refs":["financial_capital_credit_cycle#1","financial_capital_credit_cycle#3"]},{"axis":"前份漂移：估值與裁決","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-07-16：股價 228.55，估值結論 🔴，訊號 B，觀望；Bull 25%、Bear 30%","side_b":"本份：股價 180.57（−21%），前瞻 14.2 倍，估值結論改 🟡；訊號維持 B；機率維持 Bull 25%、Bear 30%、Base 45%；裁決與倉位角色由程式依新價格重算","ruling":"估值改善全部來自價格下跌，基本面沒有同幅改善：FY2026 共識三個月上修 4.6%，但最近一週下修 1.5%。機率不動，因為下行來源（資本市場循環與信用）沒有消失","evidence_level":"事實表價格與共識","settle_metric":"前瞻本益比與共識修正方向","if_then":["若共識連 2 個月下修，則 Bear 機率上調至 35%"],"evidence_refs":[]},{"axis":"前份漂移：護城河與跑道","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河趨勢 ↑，陷阱風險 🟡，五年後跑道 🟡","side_b":"本份：護城河趨勢改為 →；陷阱 🟡、跑道 🟡 不變","ruling":"改 → 的新證據：兩季紀錄級淨新增資產都有過半屬 IPO 事件性來源，有機加速沒有證實；高盛投行動能領先；同業報酬差距事實表未涵蓋，向上方向證不出來。陷阱維持 🟡，衰退訊號亮一項","evidence_level":"一手逐字稿加同業二手數據","settle_metric":"剔除 IPO 後的淨新增資產、投行份額排名","if_then":["若剔除 IPO 後年化淨新增資產連 2 季超過 3,000 億，則護城河趨勢回到 ↑"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"前份漂移：回撤與循環判讀","cause":"方法變動","prior_field":["max_dd_pct","cycle_position","archetype"],"side_a":"前份最大回撤為點值 −55%，循環位置未填，業務類型為金融","side_b":"本份最大回撤改為範圍 −30% 至 −45%，循環位置填中循環，業務類型仍為金融","ruling":"最大回撤改用範圍，並由 Bear 情境 EPS 乘倍數推導，前份點值沒有推導過程。新增循環判讀的依據：sponsor 退場尚未完成（執行長本季說法），股票交易在高檔，屬中循環","evidence_level":"方法調整","settle_metric":"無","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：加碼重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"P/TBV 回落至 ≤3.3x（≈$180，等 warranted 錨）或 through-cycle ROTCE 連 3 季 >20%（弱市確認結構性步階）或 SEC/FinCEN/OCC AML 程序結案","side_b":"股價 ≤166 美元（前瞻 13 倍）加碼；或 2026 第四季與 2027 第一季剔除 IPO 後淨新增資產年化 ≥3,000 億，且撥備每季 <2 億","ruling":"前份的價格錨（約 180 美元）本週已觸及，這就是本份重跑的原因；前份判斷日距今 94 天，超過 90 天的沿用期限。新條件把價格錨下移到前瞻 13 倍，並把跨循環 ROTCE 改成每季可驗證的淨新增資產與撥備條件。AML 結案條件移出重啟條件，因為本包沒有 AML 程序的新證據（資料缺口）；門檻改放在訴訟監管風險，罰金 >5 億照舊保留。觸及新條件就加碼第二批","evidence_level":"價格事實加方法調整","settle_metric":"股價、季度淨新增資產與撥備","if_then":["若股價 ≤166 美元且 ROTCE 仍 ≥18%，則加碼第二批","反向：若股價回到 220 美元以上而基本面沒有新證據，則不追"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定 Single Thing（null）","side_b":"AI 資本支出循環在 2027 年底前實質降速，同時帶走股票交易、IPO 承銷與 IPO 相關淨新增資產","ruling":"前份沒有設唯一致命點。本份按敏感度挑選：這件事同時打到三條收入線，是 Bear 情境 EPS 最大的單一來源；一旦發生就減碼一半","evidence_level":"一手逐字稿","settle_metric":"大型雲端業者資本支出指引、MS 股票交易年增率","if_then":["若大型雲端業者資本支出年增轉負，且 MS 股票交易年減，則減碼一半"],"evidence_refs":[]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定（null）","side_b":"ROTCE 連 2 季 <15%；CET1 <13%；剔除 IPO 後淨新增資產連 2 季年化 <2,000 億；撥備單季 ≥3 億且連 2 季","ruling":"前份只有假設與風險表，沒有可執行的停損門檻，本份補上四條。命中任兩條就減碼一半；CET1 跌破 12.3% 或 ROTCE 連 4 季低於 10% 就清倉","evidence_level":"方法調整","settle_metric":"季度財報","if_then":["命中任兩條，則減碼一半","CET1 <12.3% 或 ROTCE 連 4 季 <10%，則清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"財富管理淨新增資產的結構性","type":"假設驗證","maps_to":"H1","metric":"剔除 IPO 相關後的淨新增資產（年化）","threshold":"連 2 季年化低於 3,000 億美元","action":"停止加碼","source_freq":"季報與法說，每季","date":"2027-01","evidence_refs":[]},{"n":2,"text":"資本市場量能回落","type":"風險","maps_to":"R1","metric":"機構證券季營收年增率","threshold":"連 2 季年減","action":"減碼","source_freq":"季報新聞稿，每季","date":"2027-01","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":3,"text":"信用撥備升高","type":"風險","maps_to":"R2","metric":"全公司信用損失撥備","threshold":"單季至少 3 億美元且連 2 季","action":"減碼","source_freq":"季度財務補充資料，每季","date":"2027-01","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#3"]},{"n":4,"text":"資本規則翻轉","type":"風險","maps_to":"R3","metric":"最終規則下的標準法 CET1 要求","threshold":"較現行 11.8% 上升至少 50bp","action":"停止加碼","source_freq":"Fed／OCC／FDIC 公告，事件","date":null,"evidence_refs":["financial_regulatory_capital_rules#2"]},{"n":5,"text":"訴訟與監管升級","type":"風險","maps_to":"R4","metric":"掃款與反壟斷訴訟程序、AML 程序","threshold":"進入集體認證，或和解、罰金超過 5 億美元，或出現 AML 同意令","action":"減碼","source_freq":"10-Q／8-K，每季","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0"]},{"n":6,"text":"AI 資本支出降速同時打擊三條收入線","type":"Single Thing","maps_to":null,"metric":"大型雲端業者資本支出年增率與 MS 股票交易年增率","threshold":"兩者同時轉負","action":"減碼","source_freq":"雲端業者財報與 MS 季報，每季","date":null,"evidence_refs":[]},{"n":7,"text":"價格回到加碼區","type":"估值rearm","maps_to":null,"metric":"股價（前瞻本益比）","threshold":"≤166 美元（FY2026 共識 EPS 12.75 乘 13 倍），且 ROTCE ≥18%","action":"加碼","source_freq":"日線收盤","date":null,"evidence_refs":[]},{"n":8,"text":"報酬跌破中段","type":"減碼","maps_to":"H2","metric":"全公司季度 ROTCE","threshold":"連 2 季低於 15%","action":"減碼","source_freq":"季報新聞稿，每季","date":null,"evidence_refs":[]},{"n":9,"text":"資本或報酬失守","type":"清倉","maps_to":"H3","metric":"標準法 CET1／ROTCE","threshold":"CET1 <12.3%，或 ROTCE 連 4 季 <10%","action":"清倉","source_freq":"季報新聞稿，每季","date":null,"evidence_refs":[]},{"n":10,"text":"第四季財報複審","type":"複審日期","maps_to":null,"metric":"淨利息收入、撥備、IPO 相關淨新增資產占比","threshold":"無","action":"重跑判斷","source_freq":"季報","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"全公司季度 ROTCE","bear_threshold":"連 2 季 <15%","window":"2026Q4–2027Q4","source":"MS 季報新聞稿","last_status":"ok"},{"metric":"標準法 CET1 比率","bear_threshold":"<13.0%（要求 11.8%）","window":"每季","source":"MS 季報新聞稿與 10-Q","last_status":"ok"},{"metric":"剔除 IPO 相關後的財富管理淨新增資產","bear_threshold":"連 2 季年化 <2,000 億美元","window":"2026Q4–2027Q4","source":"MS 季度法說","last_status":"unknown"},{"metric":"全公司信用損失撥備","bear_threshold":"單季 ≥3 億美元且連 2 季","window":"2026Q4–2027Q4","source":"MS 季度財務補充資料","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 MS 當成純資本市場週期股，在 9 月量能轉弱、利率走高時三個月殺了 21%。但第三季財富管理稅前利益 28 億美元，已占全公司稅前 64.78 億的約 43%，六年兩兆淨新增資產也是多年實績；週期回落時，盈餘地板有財富管理撐住"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-3.33, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價 ≤166 美元（前瞻 13 倍）加碼；或 2026Q4 與 2027Q1 剔除 IPO 後淨新增資產年化 ≥3,000 億且撥備每季 <2 億","exec_line":"現價先不建倉。股價 ≤166 美元，或 2026Q4 與 2027Q1 確認淨新增資產與撥備（條件同加碼條件）時建首批（目標倉位三分之一）；ROTCE ≥18% 時加碼第二批。kill 指標命中任兩條就減碼一半；CET1 <12.3% 或 ROTCE 連 4 季 <10% 就清倉"},"reasoning":{"industry":"分部：第三季淨營收 203.38 億美元，財富管理 90.65 億、機構證券 100.29 億、投資管理 14.59 億（三者相加略高於總數，差額為分部間沖銷）。最新一季獲利：稅前利益 64.78 億，稅前利益率 31.9%，效率比 67%，ROTCE 22.6%，連 5 季高於 20%。財富管理稅前利益 28 億，約占全公司稅前的 43%，稅前利益率 30.4%（本季法說財務長）。收入品質分兩層。財富管理的資產管理收入 55 億（年增 16%），是收費型資產 3.155 兆乘費率的年金收入；機構證券裡，股票交易 58 億（年增 41%）、投行 22 億（+2%）、固定收益約 20 億（−7%），隨市場量能起落。產業時鐘判為擴張期，依據是第三季全公司營收年增約 12%、投行管線被管理層形容為高檔，但 9 月起量能轉弱，晚期訊號已出現。供需持久性屬混合型：機構證券是週期性，會隨市場量能反轉；財富管理的資產累積屬結構性持久，執行長本季說收購 E*TRADE 後三年累積一兆美元淨新增資產，之後三年又一兆。議價權：上游是人才，本季薪酬福利 79.97 億，占淨營收約 39%，顧問與交易員拿走價值鏈的一大塊；下游客戶分散。單點依賴：FY2025 年報把集中風險定義為單一發行人、國家或產業的部位集中，沒有單一客戶營收占比揭露。最大的依賴是資本市場活動量，以及管理層自稱「雙倍加碼」的 AI 相關融資與 IPO 流量。","moat":"機制是規模漏斗：E*TRADE 自主交易、職場股票計畫、顧問三層通路，把新財富從上游一路導進收費帳戶。機構端有股票業務 9 宮格（現貨、衍生品、主經紀乘三大地區）的規模效應。執行力給 8 分，理由是股票交易接近 2024 年的兩倍（分析師於本季法說提問所述，執行長未反駁），衍生品業務補齊，顧問留任率 99% 以上。定價力給 7 分，理由有三：另類產品有獨家條件，但掃款利差正被訴訟挑戰，投行份額動能又落後高盛。綜合 7.5 分，屬 B 級。方向從前份的 ↑ 改為 →。執行面在擴大，定價面持穩；但兩季紀錄級淨新增資產都有過半與 IPO 相關，有機加速還沒證實。高盛 2026 上半年投行費用年增 52%，MS 第三季投行只 +2% 且低於預期。同業 ROTCE 事實表未涵蓋，報酬差距的方向無法驗證。當期報酬：ROTCE 22.6%。稅前利益率 31.9% 乘資產周轉約 4.8%（年化營收約 814 億，除以總資產 1.7 兆），屬高利益率乘低周轉的象限，靠資本槓桿放大，所以要盯資本要求。再投資空間：內生成長約 7.5%，等於 ROTCE 22.6% 乘保留率約 33%。保留率的算法：股息 4.60 美元除以 FY2026 共識 EPS 12.75，股息發放率約 36%；年化回購約 62 億，除以 FY2026 共識淨利約 200 億（12.75 美元乘 15.71 億股），回購約占 31%；扣掉兩者剩約 33%。增量 ROTCE 需要有形普通股權益序列，事實表未涵蓋，以當期值代理，結果偏樂觀。同業對照表只有 FCF 利潤率，銀行的 FCF 由交易資產與放款變動主導，不能用來比較。","growth":"成長來源以量為主：客戶資產 10.5 兆、存款季增近 300 億、銀行放款季增 50 億。其次是價格，資產管理費隨市值上升。再加上回購減股。沒有併購，管理層 2026-07-15 表示偏向有機成長。共識三年 EPS：FY2025A 10.21 到 FY2028E 14.56，年化 12.6%（Koyfin 快照，分析師家數事實表未涵蓋）。內生天花板 7.5%，見護城河段。缺口約 5.1pp，歸因於兩項：FY2026 單年 EPS 年增 24.9% 的週期性利潤率擴張（股票交易 +41%、營業槓桿），以及淨回購。若只看 FY2026 到 FY2028，共識斜率 6.9%，落在天花板內。跑道：若剔除 IPO 後仍維持三年一兆的節奏，財富管理可再走十年以上；但美國財富管理總資產池事實表未涵蓋，滲透率無法計算，也沒有已證實的第二條曲線，所以給中等。衰退訊號亮一項：FY2022 到 FY2025 稀釋 EPS 年化 18.4%，營收年化 9.5%，差距 8.9pp。","governance":"FCF 換算率對銀行不適用：FY2022 到 FY2025 年度 FCF 都是負值，由交易資產與放款變動主導，不代表現金流失。改看資本：標準法 CET1 14.9%，要求 11.8%（2026-03-31 口徑），超額約 300bp，執行長本季確認。第三季回購 15.4 億美元，年化約 62 億，約占市值 2.2%。季股息在 2026-07-15 宣布調升 15% 至 1.15 美元，過去 12 個月股息殖利率 2.3%。股息加回購約占 FY2026 共識淨利的 67%，保留約 33%。現金去向四分：營運再投資、併購、回購、股息；後兩項約三分之二，併購近六年沒有（E*TRADE 為六年前收購，增量報酬事實表未涵蓋）。回購買入收益率約 6.7%（共識 EPS 除以快照價），但 10 年期公債殖利率事實表未涵蓋，無法判斷是否過關。股權激勵稀釋事實表未涵蓋。","valuation":"現價 180.57 美元，對 FY2026 共識 EPS 12.75 是 14.2 倍，對 FY2027 共識 13.57 是 13.3 倍；10-08 快照價 190.02 時是 14.9 倍。trailing 本益比 14.32，落在 4 個年度端點的 34 分位（不是五年分位）。金融業主錨用合理 P/TBV＝(ROTCE−g)÷(COE−g)，取成長率 5%、資本成本 10%：ROTCE 22.6% 時約 3.5 倍，跨循環 18% 時約 2.6 倍。每股有形淨值事實表未涵蓋，前份以 180 美元對應約 3.3 倍。現價落在兩者之間，靠近高點報酬下的合理值。PEG 1.12，用 FY2025A 到 FY2028E 的共識年化 12.6% 計；若只看 FY2026 到 FY2028 的 6.9%，PEG 約 2.05。金融業不以 PEG 為主錨。賣方均價目標 222 美元（26 位，區間 184–262），高於本份基準。短期上檔用 FY2027 基準 EPS 13.5 乘 14 倍；中期用 FY2031 基準 EPS 16.9 乘 14 倍。","premortem":"三個視角的反證都寫在反證紀錄，這裡只交結論。論點失敗的故事是：AI 資本支出降速，加上信用撥備升高（第三季撥備 1.48 億，去年同期為零，高於預期），把 EPS 拉回 10 到 11 美元，倍數壓到 10 倍。論點成功但股東經濟變差的故事是：存款靠較高成本的種類成長，淨利息收入不升反降，掃款訴訟壓利差。價格已反映太多的故事是：合理 P/TBV 在跨循環報酬下只有約 2.6 倍。陷阱風險維持 🟡：衰退訊號亮一項，業務品質與資本緩衝沒有實質惡化。"},"plain":{"six":{"how_it_makes_money":"MS 賺兩種錢。一是財富管理按資產收費的年金型收入（第三季淨營收 90.65 億美元，約占 45%），二是機構證券靠市場活動量的交易與投行收入（100.29 億，約占 49%）。錢卡在兩個節點：客戶資產規模與市場交易量","moat":"護城河 B 級，方向持平（→）。財富管理的規模漏斗是真的，但最近兩季的向上動能主要來自 IPO 事件，同業報酬差距也證不出正在擴大","growth":"五年後跑道中等（🟡）。資產累積可以延續，但滲透率算不出來；共識三年 EPS 年化 12.6%，高於內生天花板 7.5%，差額來自 2026 年的週期性利潤率擴張","capital":"資本配置穩健，但三項計分能驗證的有限。超額 CET1 約 300bp，本季回購 15.4 億，股東回報約占淨利三分之二；公債殖利率與股權稀釋的資料事實表未涵蓋","valuation":"現價要求 ROTCE 長期守在 20% 上下才划算，我只部分相信。前瞻 14.2 倍屬合理但不便宜，因為分母可能是週期高點的 2026 年盈餘","how_wrong":"最可能看錯的地方，是把週期高點當成常態。股票交易近 2024 年兩倍、IPO 帶動淨新增資產，一旦 AI 融資與資本市場同步退潮，EPS 與倍數會一起下修"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 MS 當成純資本市場週期股，在 9 月量能轉弱、利率走高時三個月殺了 21%。但第三季財富管理稅前利益 28 億美元，已占全公司稅前 64.78 億的約 43%，六年兩兆淨新增資產也是多年實績；週期回落時，盈餘地板有財富管理撐住","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤166 美元（前瞻 13 倍），或 2026Q4 與 2027Q1 剔除 IPO 後淨新增資產年化 ≥3,000 億且撥備每季 <2 億","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"金融","price_at_dd":180.57,"week26_return_pct":-3.33,"consensus_rev_3m_pct":4.59,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026 EPS 含股票交易接近 2024 年兩倍的週期高檔，以及過半與 IPO 相關的財富管理流量；若機構證券回到常態，正常化 EPS 會更低，實際倍數高於 14.2 倍"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"2026 第四季財報與法說：淨利息收入是否回升、信用撥備與 IPO 相關淨新增資產占比","impact":"高","watch":"財富管理淨利息收入季增、撥備 <2 億、剔除 IPO 後淨新增資產"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"美國資本規則三項提案是否定案（MS 促請 2026 年內定案，2028-01-01 生效）","impact":"高","watch":"最終 CET1 要求的變動幅度"},{"date":"2027-06","date_precision":"month","type":"regulatory","event":"Fed 2027 年度壓力測試結果，決定 2027-10-01 起的壓力資本緩衝","impact":"中","watch":"壓力資本緩衝是否低於現行 4.3%"}],"_projected_from":"v19"}
```
