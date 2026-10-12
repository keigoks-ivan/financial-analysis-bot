你是 stock-analyst v20 的**散文層（prose）agent**，標的 LEVI（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEVI_20261012/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：LEVI　日期：2026-10-12　archetype：None　前份裁決：2026-05-22　B（衛星候選，分批 + 等回測 Bollinger 中軌 $20.88 或 Fwd PE 13x ~$19.50）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1627B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（897B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（812B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1496B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（973B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（843B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（925B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2064B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4064B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2103B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1627           3761-5373      5 條（2–6 內）  
s3                  8000         897           4972-7103      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3281          8203-11719      5 條（2–6 內）  
s6                 11000         843          7110-10157      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         925           1802-2575      5 條（2–6 內）  
s10                 5000        2064           2055-2936      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2103           2000-2897      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5282B；至少需散文≈39.72KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−45%
−45
−40%
−25
−25%
−16.76
−14.0%
−0.07
0.04
0.11
0.16
0.4%
0.48
0.49
0.5
0.5%
0.53
0.62
0.75
1
1%
01
1.07
1.11
1.2%
1.41
1.45
1.5
1.50
1.5%
1.52
1.54
1.55
1.58
1.62
1.68
1.71
1.76
1.88
1.98
02
2
2%
2.05
2.11
2.22
2.32
2.38
2.4
2.5
2.58
2.85
3%
3
3.1
3.1%
3.12
3.19
3.3
4
04
4%
4.27
05
5
5%
5.48%
5.78
6%
6
6.7
6.77
7
07
7%
7.3%
08
8
8%
8.2%
8.5%
9%
9
9.5
9.6
10%
10
10.4
10.6%
10.9%
10.94
11.0%
11%
11
11.1%
11.4
11.4%
11.6%
12%
12
12.0%
12.1%
12.1
12.14
12.2%
12.3
12.5
12.5%
13
13%
13.2
13.3%
13.4%
13.6%
14.0%
14
14%
14.2%
14.5%
15%
15
15.39
15.5%
16%
16
16.1
16.50
16.7%
16.8%
17
18.7
18.70
18.8
19%
19
19.50
20
20%
20.88
21.75
22
22.2
22.5
22.8%
24%
24
25%
25
26
27%
28
29.9%
30%
30
30.7
30.9
32
34
35%
37.7%
40
42
43.3%
45
45%
45.6
48.2%
49
50%
50
51%
55
57.5%
58.8%
60
60%
60.1%
61.7%
62.5%
62.8
65%
65
66.2%
67
70
70.3%
80
90
100
100%
150
150%
180
200
220
240
301
450
500
640
867
914
2024
2026
2027
2030
20261012
1,031.6
1,217.6
4,430
5,880
6,200
7,800
7,860
−3,940
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
{"meta":{"ticker":"LEVI","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Levi Strauss & Co."},"oneliner":"預估本益比 12 倍、殖利率 3.1% 買到丹寧龍頭的利益率擴張；Q3 美歐直營失速與配送中心延宕是真瑕疵，勝負在 2027 年 1 月財測能否守住 12.1% 利益率新基期。","thesis":{"H":[{"id":"H1","text":"美國以外（亞洲、拉美）與批發撐住中個位數有機成長，抵銷美國直營波動。","2y":"FY2027 有機營收年增至少 4%，亞洲營收年增至少 8%","5y":null,"10y":null,"threshold":"FY2026 有機約 6%（財測）→ FY2027 至少 4% → FY2028 至少 4%","source":"季報新聞稿分區與通路數字；2026-10-07 法說會","drift_rule":"TTM 有機成長低於門檻 5% 以上連 2 季為削弱，低於 10% 以上連 3 季為反轉"},{"id":"H2","text":"利益率從 12.1% 新基期逐年擴張，配送中心轉換效益 2027 年起兌現，走向 15% 營業利益率。","2y":null,"5y":"FY2028 調整後 EBIT 利益率至少 13%，FY2030 至少 14.5%","10y":null,"threshold":"FY2026 約 12.1%（含 30bp 淨關稅退款）→ FY2027 至少 12.5% → FY2028 至少 13%","source":"公司財測與法說（2026-10-07 CFO 稱 12.1% 為新基期；2026-07-08 重申 15% 目標）","drift_rule":"TTM 調整後 EBIT 利益率低於門檻路徑 5% 以上連 4 季為削弱，10% 以上連 6 季為反轉"},{"id":"H3","text":"品牌定價權：不靠降價維持並緩升毛利率，高端 Blue Tab 與上身品類拉高均價。","2y":null,"5y":null,"10y":"每個會計年度毛利率（剔除一次性關稅退款）至少 61.7%；Blue Tab 年營收達 1–2 億美元（2026-07-08 CEO 說法）","threshold":"年度毛利率至少 61.7%（FY2025 水準）","source":"年度財報毛利率；季報均價說明","drift_rule":"跨 2 個會計年度低於 61.7% 為削弱，跨 3 個年度為反轉"}],"R":[{"id":"R1","text":"美歐直營流量疲弱不是天氣與單一檔期問題，而是版型週期轉換下品牌熱度降溫。","h_ref":"H1","clock":"⚡","threshold":"Q4 FY2026 與 Q1 FY2027 全球直營有機年增皆低於 3%","evidence_refs":["channel_business_model_shift#0"]},{"id":"R2","text":"Section 301 新關稅（主要產地孟加拉、柬埔寨、巴基斯坦、越南約 10–12.5%，有效稅率各來源不一）吸收失敗，毛利率回吐。","h_ref":"H3","clock":"🔥","threshold":"剔除關稅退款的毛利率連 2 季年減超過 100bp 且公司歸因關稅","evidence_refs":["reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#2"]},{"id":"R3","text":"競爭加劇使行銷與促銷費用常態化，12.1% 新基期守不住。","h_ref":"H2","clock":"🔥","threshold":"FY2027 調整後 EBIT 利益率低於 12.1%，或廣告費率連 2 年高於 FY2026 而利益率未擴張","evidence_refs":[]},{"id":"R4","text":"批發客戶無長期合約、逐單採購，主要客戶財務惡化，或代工整併後供應端議價轉強。","h_ref":"H1","clock":"🐢","threshold":"任一主要批發客戶破產，或前十大批發客戶占比回升至 27% 以上","evidence_refs":["customer_concentration_credit#1","customer_second_source#1"]}],"single_thing":{"description":"2027 年 1 月公布的 FY2027 財測，調整後 EBIT 利益率低於 2026-10-07 CFO 宣稱的 12.1% 新基期。","why_fatal":"基準情境 EPS 年增約 9% 中近一半來自利益率擴張；新基期守不住代表今年為救流量加的行銷、促銷與物流費用不是一次性，EPS 只能跟營收中個位數走，倍數也失去上修理由。這是情境樹中對終端 EPS 敏感度最大的單一變數。","if_happens":"減碼一半；若同時全球直營連 2 季年增低於 3%，清倉。","how_monitor":"Q4 FY2026 實際 EBIT 利益率對比 11.4–11.6% 指引；2027-01 財測的利益率與廣告費率說明；新任 CFO 首份財測口徑。","probability":"約 30%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":10.94,"peg_fy2":1.0,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":1.45,"FY2026E":1.54,"FY2027E":1.71,"FY2028E":1.98},"fy_end_month":11,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識調整後稀釋 EPS；FY2025A 1.45 為年報 GAAP 稀釋 EPS，事實表未提供 FY2025 調整後值，兩者口徑不完全同源"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LEVI_20261012/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"成熟品牌、毛利率六成、營收中個位數成長、EPS 成長倚賴利益率修復與回購"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性慢成長、份額週期可逆：丹寧品類管理層稱至 2030 年每年中個位數成長，第三方估值分歧但多為低至中個位數；印度丹寧布產能過剩約 20–25%（來源未標日期）壓低布料成本；版型潮流造成的流量轉移屬短週期，可逆性高。","bargaining":{"up":"對上游強：約 32 國獨立代工、單一國家不超過 30%；但公司正整併代工家數，上游議價力可能小幅回升。","down":"對下游中強：前十大批發客戶占比由 FY2023 27% 降至 FY2025 24%，無單一客戶達 10%；但與批發客戶無長期合約、逐單採購。","geo":"主要產地為孟加拉、柬埔寨、巴基斯坦、越南，受 2026-07-24 起 Section 301 新關稅約束；中國占產量約 1%。"},"profit_pool_dir":"品牌端利潤池擴大：毛利率 FY2022 57.5% 升至 FY2025 61.7%，直營擴張把原屬零售商的價差收回；關稅是政府從利潤池抽成的新變數，IEEPA 被推翻後改為 Section 301。","tam_table":[{"item":"全球丹寧市場（第三方一）","value":"2024 年底約 867 億美元，預估 2030 年 1,217.6 億美元（市調報告，非共識）"},{"item":"全球丹寧市場（第三方二）","value":"2026 年約 914 億美元、年複合 5.48%；另一來源 1,031.6 億美元，口徑分歧"},{"item":"品類成長（管理層）","value":"2026-07-08 CEO：丹寧品類至 2030 年每年中個位數成長"},{"item":"可觸及市場擴大","value":"2026-07-08 CEO：轉向全身丹寧生活風格使可觸及市場擴大 15 倍（管理層說法，未經第三方驗證）"},{"item":"高端丹寧滲透","value":"超高端丹寧市占不到 1%（2026-10-07 CEO；Q2 法說稱 0.4%），Blue Tab 價位 200–500 美元"},{"item":"利潤池占比 5 年前→現","value":"事實表未涵蓋"}]},"moat":{"mechanism":"品牌與版型話語權：丹寧品類第一的心智占有讓公司不必降價，並把品牌延伸到上身、高端 Blue Tab 與亞洲市場。","execution":6,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價面穩定：毛利率 FY2022 57.5% 到 FY2025 61.7% 連升，Q3 剔除退款仍 +80bp、未降價；執行面縮減：直營 Q1 +16%、Q2 +11%、Q3 +2% 連續減速，物流效益延後。兩向抵銷，判持平。","peer_na_reason":"同業 ROIC 與研發占比事實表未涵蓋，只能用毛利率、營業利益率、FCF 利益率三軸對照。","threats":[{"level":"🟡","text":"丹寧競爭加劇與新進者（2026-10-07 CEO 自述），低腰版型潮流中公司一度失準，迫使行銷與促銷費用上升；點對點競爭，不扣分。","p":"35%","evidence_refs":[]},{"level":"🟡","text":"代工廠整併：供應端集中度上升，大型代工的議價力可能提高，壓縮產品成本下降空間。","p":"20%","evidence_refs":["customer_second_source#1"]},{"level":"🟡","text":"關稅改制：主要產地孟加拉、柬埔寨、巴基斯坦、越南受 Section 301 新關稅約束，退款屬一次性，後續稅率由政策決定。","p":"50%","evidence_refs":["reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#2"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟢","text":"丹寧是耐久品類，管理層與第三方都估至 2030 年低至中個位數成長；使用者、決策者、付款者多為同一消費者，轉換鏈短。版型潮流（寬鬆轉低腰）改變的是品類內份額而非品類需求，Q3 美國批發仍正成長即為證據。"},{"item":"決策層級","level":"🟡","text":"替代性在單一版型與檔期層級就會發生：Q3 返校檔主打寬鬆版型失準，流量在兩個月內轉弱；但全價銷售比例提高、均價上升且未跟隨降價，顯示品牌層級的忠誠度仍在。轉換成本低，靠持續的版型創新與行銷維持。"},{"item":"價值鏈分配","level":"🟢","text":"品牌環節拿走最大一塊：毛利率六成以上，代工分散於約 32 國、單一國家不超過 30%，前十大批發客戶占比逐年下降至 24%；直營占比四成五到五成，把零售價差收回。風險是代工整併與關稅抽成。"},{"item":"社會容忍度","level":"🟢","text":"服飾非必需品，不存在政治性的價格天花板，也不依賴監管授權；政策風險集中在關稅，已列為風險而非社會容忍度問題。"}],"roiic":"事實表未涵蓋（缺投入資本口徑，無法計算增量報酬）","reinvest_rate":"事實表未涵蓋；2026-07-08 CFO 稱自由現金流至少 55–65% 回饋股東，可推知留在公司的自由現金流不超過約四成五（與定義的再投資率口徑不同）","endo_ceiling":null,"formula_note":"當期 ROIC 需稅後營業利益率×投入資本周轉率，事實表只有利益率、缺投入資本，象限無法判定；只能確認高毛利、營業利益率約 11–12%。成長主要靠利益率擴張與回購，而非新增資本，屬高報酬低再投資型。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","LEVI":61.72,"KTB":48.24,"PVH":58.78,"GAP":43.26,"RL":70.27,"unit":"%"},{"metric":"營業利益率","LEVI":11.06,"KTB":12.03,"PVH":8.05,"GAP":10.99,"RL":16.42,"unit":"%"},{"metric":"FCF 利潤率","LEVI":8.46,"KTB":13.6,"PVH":8.01,"GAP":6.24,"RL":11.99,"unit":"%"}],"competitors":[{"name":"KTB","gm":48.24,"om":12.03,"fcf_margin":13.6,"strategy_note":"Wrangler 與 Lee 母公司，毛利率低十多個百分點但營益率與自由現金流率較高，走批發為主的輕資產路線，是丹寧的直接對手。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"PVH","gm":58.78,"om":8.05,"fcf_margin":8.01,"strategy_note":"Calvin Klein 與 Tommy Hilfiger，毛利率接近但營益率低約 3 個百分點，顯示同樣的品牌溢價沒能留到營業利益。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"GAP","gm":43.26,"om":10.99,"fcf_margin":6.24,"strategy_note":"大眾價位自有通路，毛利率低近兩成，營益率與 LEVI 相當，代表通路效率可以彌補品牌溢價差距。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"RL","gm":70.27,"om":16.42,"fcf_margin":11.99,"strategy_note":"高端生活風格品牌，毛利率與營益率皆最高，是 LEVI 用 Blue Tab 往高端延伸要追的標竿。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量與價約各半（2026-07-08 CFO：全年單位數與均價貢獻約 50／50），疊加利益率擴張與小幅淨回購；無併購，Dockers 為出售。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板無法以事實表算出（缺投入資本與增量報酬）。結構推論：營收中個位數成長所需再投資不高，自由現金流過半配回股東；共識 FY2026→FY2028 EPS 年增約 13% 高出營收成長的部分來自利益率擴張與回購，而非再投資驅動，故視為超出內生成長。","segments":[{"item":"美洲（Q3）","value":"營收 +2%，拉美 +10%；營業利益率 29.9%（含退款淨效益，+640bp）"},{"item":"歐洲（Q3）","value":"營收 +5%，批發雙位數；營業利益率 22.8%（+150bp）；2027 春夏批發預訂高個位數成長"},{"item":"亞洲（Q3）","value":"營收 +10%，連三季雙位數；營業利益率 14.2%（+220bp），年初至今 16.7%"},{"item":"品牌","value":"Levi's 品牌 +4%、Signature +13%、Beyond Yoga +9%；Blue Tab 雙位數成長但規模小"},{"item":"通路","value":"批發 +6%、直營 +2%（占 45%）、電商雙位數；管理層預期 Q4 直營中個位數"},{"item":"品類","value":"丹寧下身以外品類貢獻 Q3 約一半成長，上身 +7%、女裝上身 +10%"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 +10bp、Q3 +450bp（剔除退款 +80bp）"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱美國男女裝份額擴大，未經第三方驗證"},{"item":"提價後銷量下滑","lit":false,"note":"Q2 批發量增、全年量價約各半"},{"item":"EPS 成長顯著高於營收成長（差距>5pp）","lit":true,"note":"共識 EPS 年增約 11–13% 對營收中個位數"},{"item":"FCF／淨利<0.75 連 2 年","lit":false,"note":"FY2024 3.19 打斷；FY2025 0.53 單年偏低，監測"},{"item":"SBC／營收>5% 且上升","lit":false,"note":"前九月 SBC 5,880 萬美元，約營收 1% 出頭"},{"item":"TAM 萎縮或被替代","lit":false,"note":"第三方與管理層皆估品類成長"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數事實表未涵蓋，無法判定"},{"item":"維持性資本支出占 FCF>60%","lit":false,"note":"事實表未涵蓋"},{"item":"停止投資新產能且收入下滑","lit":false,"note":"全年淨新增 50–60 家門市，營收成長"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自有機營收與利益率，不靠併購；回饋政策與本季股利、回購數字已寫在判斷理由"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表內近年資本動作是出售 Dockers（賣方），無新收購可評增量報酬","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"加速回購約在 18.7 美元執行，對應 FY2026E 盈餘殖利率約 8.2%（1.54÷18.7）；10 年期公債殖利率事實表未涵蓋，無法判定是否高出 2 個百分點","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 年化約 7,800 萬美元；市值以 P/S 1.07 倍×FY2025 營收 62.8 億美元粗估約 67 億美元，毛稀釋約 1.2%／年，扣除回購後淨稀釋更低，低於 1.5%","grade":"過"}]},"valuation":{"basis":"預估本益比（FY2026E 共識調整後 EPS 1.54 美元）搭配 PEG 與殖利率","tier":"成熟服飾品牌","peers":{"expanded":false,"reason":"事實表同業對照只有毛利率、營業利益率、FCF 利益率，沒有倍數；同業本益比事實表未涵蓋"},"fwd_pe":12.14,"peg":1.11,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"預估本益比 12.1 倍、trailing 12.3 倍在近四個年度端點 6.7 百分位，P/S 18.8、EV/S 9.6 百分位；PEG 1.11 合理偏便宜；殖利率 3.1%。事實表只有年度端點分位、沒有五年連續序列，故五年分位留空不外推。","upside_short_pct":19,"upside_mid_pct":65},"trap_analysis":{"verdict":"🟡","label":"一項衰退信號亮燈：EPS 成長明顯快於營收，倚賴利益率擴張"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 直營只成長 2%（Q1 +16%、Q2 +11%），CEO 承認丹寧競爭加劇、有新進者，美國返校檔需靠重拍廣告與促銷救流量；FY2022 到 FY2023 GAAP EPS 曾由 1.41 降到 0.62。","assumption":"直營失速是歐洲天氣與美國單一檔期行銷失誤，九月已回正。","consequence":"若是品牌熱度轉弱，利益率卡在 11–12%、倍數壓到 9 倍，五年報酬可能接近 −40%。","ruling":"部分採納：一次性歸因未證，熊市機率設 30%。與唯一致命點（FY2027 利益率指引）部分重疊——直營失速是利益率失守最可能的成因，已合併進清倉條件監測。","watch":"Q4 FY2026 全球與美國直營年增；2027-01 財測","not_applicable_reason":null,"evidence_refs":["channel_business_model_shift#0"],"fact_refs":["f_kpi0_net_revenues_gaap","f_kpi4_adjusted_diluted_eps"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 表明行銷費率已在 7% 以上、未來還要加碼；配送中心雙軌成本與火災使效益延至 2027；公司同時整併代工家數，供應端集中度上升。","assumption":"營收與毛利率達標，但為維持品牌熱度須長期提高行銷與促銷，物流效益遲遲不到。","consequence":"營收成長達標而 EPS 只跟營收走，倍數無法上修，股東只拿到股息與小幅回購。","ruling":"採納為主要中期風險：基準路徑利益率只設到 FY2028 約 13%，低於共識隱含水準。","watch":"廣告占營收比例、調整後 SG&A 率（FY2026 指引約 51%）、Groveport 配送中心效率","not_applicable_reason":null,"evidence_refs":["customer_second_source#1"],"fact_refs":["f_kpi1_adjusted_ebit","f_kpi2_gaap_operating_income"]},{"view":"價格已反映太多","evidence":"共識 FY2028 EPS 1.98 美元（兩年年增約 13%）可能偏樂觀，12 倍的便宜可能建立在高估的分母上。","assumption":"現價已反映利益率走到 15%。","consequence":"若共識高估，便宜只是估值錯覺，下檔大於上檔。","ruling":"反駁：以我們低於共識的基準 FY2028 1.88 美元計，現價仍不到 10 倍；trailing 本益比在近四個年度端點 6.7 百分位、殖利率 3.1%，現價反映的是利益率停滯而非擴張。比較可能的錯誤方向是太悲觀。","watch":"預估本益比若回到 15 倍以上而 EPS 未上修，重評","not_applicable_reason":null,"evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_dividend_yield_ttm","f_consensus_eps_fy3"]}],"max_dd":{"lo":-45,"hi":-25,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 21.75 → 本次 18.7（-14.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=21.75","side_b":"本次 price_at_dd=18.7","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 21.75 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 21.75 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 21.75 美元：Bull 價 45.6、Bear 價 15.39，五年期望值 +37.7%，基準年化 7.3%，不對稱比 3.12","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.12。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 21.75 美元：五年期望值 +37.7%，基準年化 7.3%，不對稱比 3.12","side_b":"本次情境、股價 18.7 美元：五年期望值 +60.1%，基準年化 10.6%，不對稱比 6.77","ruling":"再換股價、情境不動：起點價下跌 14.0%，五年期望值多 22.5 個百分點，基準年化多 3.3 個百分點，不對稱比由 3.12 升到 6.77。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：訊號與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-22，股價 21.75 美元）：訊號 B、估值便宜；等回測 20.88 美元或預估本益比 13 倍約 19.50 美元分批。","side_b":"本次股價 18.70 美元，已低於前份兩個分批價位；FY2026E 共識 1.54 美元對應 12.1 倍，估值結論仍為便宜，訊號維持 B。","ruling":"維持不升級：價格下跌讓估值更便宜，但同期出現直營失速、配送中心延宕、CFO 交接等新負面證據，兩者抵銷。","evidence_level":"事實表股價與共識","settle_metric":"2027-01 財報的直營年增與 FY2027 利益率指引","if_then":["若股價續跌至 16.50 美元以下而直營未觸發失速門檻，分批反買三分之一","若直營連 2 季年增低於 3%，停止加碼並減碼至半倉"],"evidence_refs":[]},{"axis":"前份漂移：舊格式未輸出的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份為舊格式，這些欄位皆為空值。","side_b":"本次：護城河持平、五年後跑道中等、類型為品質複利成長（次類轉機）、非循環股不判循環位置、最大回撤 −25% 到 −45%、多頭 25／空頭 30 機率；回撤與機率由程式從本次情境算出。","ruling":"屬方法變動，非基本面漂移；本次首度給值，後續以本次為比較基準。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：價值陷阱判讀","cause":"方法變動","prior_field":["trap"],"side_a":"前份價值陷阱 🟢。","side_b":"本次 🟡：十項衰退信號中「EPS 成長明顯快於營收」亮燈（共識 EPS 年增約 11–13% 對營收中個位數）。","ruling":"結構本來就在，本次改用逐項清單才顯現；不代表基本面轉壞，代表 EPS 成長倚賴利益率擴張，已對應到利益率論點與唯一致命點。","evidence_level":"共識 EPS 與財測","settle_metric":"FY2027 利益率指引","if_then":["若 FY2027 指引利益率低於 12.1%，陷阱判讀升為 🔴 並減碼一半"],"evidence_refs":[]},{"axis":"行動門檻新設：重啟條件、清倉與減碼","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件、清倉門檻與減碼門檻（空值）。","side_b":"本次：清倉＝FY2027 EBIT 利益率指引低於 12.1% 且全球直營連 2 季年增低於 3%；減碼＝剔除關稅退款的毛利率連 2 季年減超過 100bp，或直營連 2 季低於 3%；重啟第二批＝2027-01 財報確認直營年增至少 4% 且指引至少 12.1%。","ruling":"新設，不沿用前份；理由是本季管理層首次給出 12.1% 新基期與直營中個位數承諾，可直接轉成可驗證門檻。","evidence_level":"2026-10-07 法說會","settle_metric":"2027-01 財報","if_then":["若兩項清倉條件同時成立，清倉","若僅一項成立，減碼一半"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":null,"side_a":"前份未設唯一致命點。","side_b":"FY2027 財測的調整後 EBIT 利益率低於 2026-10-07 CFO 宣稱的 12.1% 新基期。","ruling":"新證據：CFO 明言 12.1% 為新基期、本年加碼的行銷與物流費用明年不會重複；這是終端 EPS 敏感度最大的單一變數，且在 2027 年 1 月以單一事件揭曉。","evidence_level":"2026-10-07 法說會 CFO 原話","settle_metric":"FY2027 EBIT 利益率指引","if_then":["若低於 12.1%，減碼一半","若至少 12.1% 且直營至少 4%，補第二批"],"evidence_refs":[]},{"axis":"假設與風險門檻改寫","cause":"新證據","prior_field":null,"side_a":"前份 H2＝Beyond Yoga FY2027 年化至少 2.5 億美元；R1＝連 4 季對 Lululemon 成長差超過 15pp；R2＝連 2 季毛利率年減超過 200bp 且歸因關稅。","side_b":"本次假設改為有機營收至少 4%、EBIT 利益率路徑、毛利率至少 61.7%；風險改為直營連 2 季低於 3%、剔除退款毛利率連 2 季年減超過 100bp。","ruling":"IEEPA 關稅已在 2026-02-20 被最高法院推翻並改為 Section 301 新關稅，舊 200bp 門檻對應的稅率情境已不存在；Beyond Yoga 本季 +9%、事實表無年化營收，無法驗證舊門檻，改追蹤整體利益率。","evidence_level":"10-Q 與 2026-10-07 法說","settle_metric":null,"if_then":[],"evidence_refs":["reg_tariff_export#1"]},{"axis":"管理層說法前後落差：Q4 利益率與配送中心","cause":null,"prior_field":null,"side_a":"2026-07-08 CFO：Q4 2024 是 Q4 2026 的良好參照，約 14% EBIT 利益率；Hebron 移交預計 Q4 初完成，延後成本僅數百萬美元。","side_b":"2026-10-07：Q4 EBIT 指引 11.4–11.6%，含 180bp 退款再投入，剔除後約 13.2–13.4%；配送中心效益延至 2027，另有火災干擾。","ruling":"可調和（程度差異）：採信新數字，對 15% 目標的時程打折，基準路徑 FY2028 利益率只設 13%。","evidence_level":"兩場法說會原話","settle_metric":"Q4 FY2026 實際 EBIT 利益率","if_then":["若 Q4 實際低於 11.4%，視為管理層連兩季過度樂觀，停止加碼","若 Q4 達 11.6% 以上且 FY2027 指引至少 12.5%，基準利益率路徑上調"],"evidence_refs":[]},{"axis":"直營失速：一次性還是品牌熱度轉弱","cause":null,"prior_field":null,"side_a":"管理層：歐洲天氣過熱、美國返校檔主打寬鬆版型失準，九月已回正，Q4 直營中個位數、全年高個位數。","side_b":"直營 Q1 +16%、Q2 +11%、Q3 +2% 連續減速；CEO 承認競爭加劇、新進者入場，Q3 動用促銷清庫存。2026-07-08 CFO 曾預期歐洲直營下半年中到高個位數。","ruling":"管理層一次性歸因不採信也不否定，標未證、監測；預登記：Q4 FY2026 與 Q1 FY2027 全球直營年增皆低於 3%，即視為歸因證偽。","evidence_level":"季報與法說","settle_metric":"全球直營有機年增","if_then":["若連 2 季低於 3%，減碼至半倉","若 Q4 至少 4%，維持分批計畫"],"evidence_refs":["channel_business_model_shift#0"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭：2026-10-07 CEO 稱丹寧競爭加劇、有新進者；結構：品牌毛利率 FY2022 57.5% 升至 FY2025 61.7%，批發連兩年成長且獲利。","side_b":"其他結構變數：關稅由 IEEPA 改為 Section 301 新關稅（2026-07-24 起），主要產地皆受約束；直營與批發從直營主導轉回兩條腿並行。","ruling":"雙向拉鋸：競爭惡化與品牌結構轉好同時成立，關稅改制是第三個變數，淨效果短期偏中性。","evidence_level":"法說與 10-Q","settle_metric":"剔除退款毛利率與直營年增","if_then":[],"evidence_refs":["reg_tariff_export#4"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"直營連三季減速、任期 14 年的 CFO 離職、配送中心效益一延再延、7 月說 Q4 約 14% 利益率如今剔除退款只剩約 13.3%；管理層連續兩季對短期執行過度樂觀，12 倍可能是價值陷阱。","side_b":"批發 +6%、亞洲 +10%、剔除退款毛利率仍 +80bp、EPS 財測年內三度上調、存貨年減 3%；失誤集中在美歐直營單一通路與物流時程，並非全面性。","ruling":"不賣、分批買：負面集中在單一通路與執行時程，基本盤與估值支持小部位；但不追價，第二批等 2027-01 財報。","evidence_level":"季報與法說","settle_metric":"2027-01 財報","if_then":["若 Q4 全球直營至少 4% 且 FY2027 EBIT 指引至少 12.1%，加至目標部位三分之二","若 FY2027 指引低於 12.1%，減碼一半，不等下一季"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"有機營收成長守住中個位數","type":"假設驗證","maps_to":"H1","metric":"有機營收年增（季）","threshold":"FY2027 各季至少 4%","action":"連 2 季低於 4% 停止加碼","source_freq":"季報（每季）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"FY2027 財測利益率低於 12.1% 新基期","type":"Single Thing","maps_to":"Single Thing","metric":"FY2027 調整後 EBIT 利益率指引","threshold":"低於 12.1%","action":"減碼一半；若同時直營連 2 季低於 3% 則清倉","source_freq":"年度財測（每年 1 月）","date":"2027-01","evidence_refs":[]},{"n":3,"text":"美歐直營失速延續","type":"風險","maps_to":"R1","metric":"全球直營有機年增","threshold":"Q4 FY2026 與 Q1 FY2027 皆低於 3%","action":"減碼至半倉","source_freq":"季報（每季）","date":"2027-04","evidence_refs":["channel_business_model_shift#0"]},{"n":4,"text":"關稅成本吸收失敗","type":"風險","maps_to":"R2","metric":"剔除關稅退款的毛利率年變化","threshold":"連 2 季年減超過 100bp 且公司歸因關稅","action":"減碼","source_freq":"季報（每季）","date":null,"evidence_refs":["reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#2"]},{"n":5,"text":"股價再下探而基本面未壞","type":"加碼","maps_to":"H2","metric":"股價","threshold":"16.50 美元以下（約 FY2027E 共識 9.6 倍）且直營未觸發失速門檻","action":"分批反買三分之一","source_freq":"每日","date":null,"evidence_refs":[]},{"n":6,"text":"第二批進場的確認條件","type":"估值rearm","maps_to":"H1","metric":"Q4 FY2026 全球直營年增與 FY2027 EBIT 利益率指引","threshold":"直營至少 4% 且指引至少 12.1%","action":"補第二批至目標部位三分之二","source_freq":"季報","date":"2027-01","evidence_refs":[]},{"n":7,"text":"清倉條件","type":"清倉","maps_to":"H2","metric":"FY2027 EBIT 利益率指引＋全球直營年增","threshold":"指引低於 12.1% 且直營連 2 季低於 3%","action":"清倉","source_freq":"季報","date":"2027-04","evidence_refs":[]},{"n":8,"text":"批發客戶信用與供應端集中","type":"風險","maps_to":"R4","metric":"主要批發客戶財務狀況、前十大批發客戶占比","threshold":"任一主要批發客戶破產，或前十大占比回升至 27% 以上","action":"減碼","source_freq":"年報與新聞","date":null,"evidence_refs":["customer_concentration_credit#1","customer_second_source#1"]},{"n":9,"text":"財報後複審","type":"複審日期","maps_to":null,"metric":"Q4 FY2026 財報與 FY2027 財測","threshold":"財報公布後一週內","action":"重跑判斷","source_freq":"一次","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"FY2027 調整後 EBIT 利益率指引","bear_threshold":"低於 12.1%（CFO 宣稱的新基期）","window":"2027-01 財報","source":"公司 Q4 FY2026 財報新聞稿與法說","last_status":"unknown"},{"metric":"全球直營有機營收年增","bear_threshold":"連 2 季低於 3%","window":"Q4 FY2026 至 Q1 FY2027","source":"季報新聞稿通路數字","last_status":"warning"},{"metric":"剔除關稅退款的毛利率年變化","bear_threshold":"連 2 季年減超過 100bp 且歸因關稅","window":"FY2027 各季","source":"季報與法說拆解","last_status":"ok"},{"metric":"有機營收年增（TTM）","bear_threshold":"低於 3%","window":"FY2027","source":"季報新聞稿","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Q3 美歐直營失速與 CFO 交接當成品牌轉弱，但批發 +6%、亞洲 +10%、剔除關稅退款的毛利率仍擴張 80bp；12 倍預估本益比隱含利益率不再擴張，而管理層已給出可在 2027 年 1 月驗證的 12.1% 新基期。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=-16.76, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"2027-01 財報確認全球直營年增至少 4% 且 FY2027 EBIT 利益率指引至少 12.1%，補第二批","exec_line":"現價 18.70 美元先建目標部位三分之一；跌至 16.50 美元以下且直營未觸發失速門檻再加三分之一；2027-01 財報確認新基期後補足；唯一致命點觸發即減半"},"reasoning":{"industry":"分區：Q3 美洲 +2%（拉美 +10%，美國直營拖累）、歐洲 +5%、亞洲 +10%；通路：批發 +6%、直營 +2%（占 45%）、電商雙位數。營收分部占比事實表未涵蓋，只能用成長率判讀。Q3 調整後 EPS 0.48 美元含 0.11 美元關稅退款淨效益，剔除後年增 9%，來自利益率擴張與回購。產業時鐘判在擴張期：丹寧品類管理層與第三方都估年增低至中個位數，公司年內三度上調 EPS 財測，但 CEO 承認競爭轉強、Q3 動用節慶促銷，尚未到過熱。供需持久性：品類需求屬結構性慢成長，版型週期（寬鬆轉低腰）造成的份額移動可逆；上游丹寧布產能過剩對品牌端是成本順風。單點依賴：無單一客戶達營收 10%，前十大批發客戶占比 FY2025 為 24% 且逐年下降；供應端約 32 國、單一國家不超過 30%，集中度風險低，但公司已開始整併代工家數。","moat":"機制是品牌與版型話語權：TTM 毛利率 61.7%，高於 PVH 58.8%、KTB 48.2%、GAP 43.3%，僅次 RL 70.3%；但營業利益率 11.1% 與 KTB 12.0%、GAP 11.0% 相當，FCF 利益率 8.5% 低於 KTB 13.6%，代表品牌溢價被直營門市與物流成本吃掉。定價權評 8：Q3 同業降價時公司沒有降價，只在節慶檔促銷；Q2 法說稱均價上升來自減少促銷與全價銷售。執行評 6：Q3 直營只成長 2%、美國返校檔行銷主打寬鬆版型失準、配送中心轉換延宕又遇火災、任期 14 年的 CFO 交接。方向：執行面縮減、定價面穩定，綜合判持平而非下滑——批發 +6%、亞洲 +10%，管理層稱美國男女裝份額擴大（未經第三方驗證）。同業 ROIC 事實表未涵蓋，無法做報酬差，故不給 8 分以上。","growth":"三年共識 EPS：FY2026E 1.54、FY2027E 1.71、FY2028E 1.98 美元，近三個月零修正。以 FY2025 GAAP 稀釋 EPS 1.45 為基期，三年年增約 10.9%；以 FY2026E 為起點，兩年年增約 13.4%。營收面 FY2026 有機約 6%，管理層長期框架為中個位數。缺口約 5–7 個百分點，歸因利益率擴張（12.1% 走向 15% 目標）與淨回購，屬可歸因；但 7 月法說稱 Q4 約 14% 利益率、10 月指引剔除退款只剩約 13.2–13.4%，路徑已延後。基期口徑注意：FY2025 淨利 5.78 億美元較 FY2024 2.11 億美元跳升，與營業利益率變化不成比例，疑含非營業項目，事實表未拆分，10.9% 可能低估調整後口徑成長。十項衰退信號亮一項（EPS 成長明顯快於營收），長期成長性中等。","governance":"FCF／淨利：FY2022 −0.07、FY2023 0.49、FY2024 3.19、FY2025 0.53（年報 FCF÷淨利），波動大；FY2025 淨利跳升疑含非營業項目，轉換率可能被低估。Q3 調整後自由現金流 4,430 萬美元（去年同期 −3,940 萬），年初至今 4.27 億美元。SBC 前九月 5,880 萬美元，年化約 7,800 萬美元。回饋政策：2026-07-08 CFO 稱至少把自由現金流的 55–65% 回饋股東，Q3 季股利調升至 0.16 美元，Q3 發出股利 6,200 萬美元。現金去向四分（再投資、併購、股利、回購）與債務到期結構事實表未涵蓋。","valuation":"FY2026E 共識 1.54 美元對應 12.1 倍，trailing 12.3 倍落在近四個年度端點 6.7 百分位，P/S 與 EV/S 也在 9.6–18.8 百分位，處近年低檔。PEG 以三年 EPS 年增 10.9% 計約 1.11。短期上檔：FY2027E 1.71 美元×13 倍約 22.2 美元，+19%；中期：基準 FY2031E 2.38 美元×13 倍約 30.9 美元，+65%。賣方目標價平均約 26–28 美元、區間 14–34 美元（高低比約 2.4 倍），7 月底有一家降評至持有、目標 25 美元；我們的 12 個月估值低於賣方均值，支持分批而非追價。分母 FY2026E 含 0.04 美元淨關稅退款，剔除後 1.50–1.52 美元、倍數 12.3–12.5 倍，不改結論。","premortem":"依據見反證紀錄三條：論點失敗（直營連三季減速、競爭加劇）、股東經濟變差（行銷與物流費用常態化）、價格已反映太多（反駁）。26 週股價下跌 16.8%、RSI 30.7，市場已部分反映直營疑慮。十項衰退信號亮一項：EPS 成長明顯快於營收。管理層 7 月對 Q4 利益率與配送中心時程的說法，到 10 月均已下修，對其一次性歸因採未證、監測處理。"},"plain":{"six":{"how_it_makes_money":"賺的是全球消費者為 Levi's 品牌與版型付的溢價，錢卡在品牌與通路兩個節點：直營占營收四成五到五成、其餘走批發。最新一季營收 16.1 億美元、年增 4%（有機 5%），毛利率 66.2%（剔除關稅退款約 62.5%），調整後 EBIT 利益率 15.5%（剔除後約 12.2%）。","moat":"護城河持平，等級 B：美國男女裝與青少年丹寧第一的品牌定價權撐住六成毛利，但直營與物流執行拖累利益率，營業利益率對同業並不領先。","growth":"跑道中等：丹寧主業是年增中個位數的成熟品類，第二曲線（上身品類、Blue Tab、亞洲直營）有成長證據但規模仍小、主要靠管理層說法；共識 EPS 成長高於營收的部分來自利益率擴張與回購，可歸因但時程已見延後。","capital":"資本配置中上：自由現金流過半配回股東，Q3 股利年增 11%，另以 1 億美元加速回購；但近四年自由現金流對淨利的轉換很不穩定。","valuation":"現價只要求利益率守在 12% 上下、EPS 每年中個位數成長就划算：12 倍預估本益比加 3.1% 殖利率，大致已把利益率不再擴張定價進去。我信這個下限，但不信 15% 利益率會準時到，所以只用 13 倍與低於共識的 EPS 估值。","how_wrong":"最可能看錯在把 Q3 直營失速當成天氣與單一檔期的一次性問題，而它其實是版型週期轉換下品牌熱度降溫的開端；其次是利益率新基期守不住。價值陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Q3 美歐直營失速與 CFO 交接當成品牌轉弱，但批發 +6%、亞洲 +10%、剔除關稅退款的毛利率仍擴張 80bp；12 倍預估本益比隱含利益率不再擴張，而管理層已給出可在 2027 年 1 月驗證的 12.1% 新基期。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟢","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":18.7,"week26_return_pct":-16.76,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026E 含 0.04 美元淨關稅退款，剔除後 1.50–1.52 美元，倍數約 12.3–12.5 倍，便宜結論不變。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 FY2027 首份財測（新任 CFO 上任後首份）","impact":"高","watch":"FY2027 EBIT 利益率指引是否至少 12.1%；Q4 全球直營是否達中個位數"},{"date":"2027","date_precision":null,"type":"capacity","event":"Hebron 配送中心關閉後，美國物流成本效益開始兌現","impact":"中","watch":"調整後 SG&A 率中的物流成本是否下降"},{"date":"2027","date_precision":null,"type":"product","event":"levi.com 全面改版與平台遷移全球上線","impact":"中","watch":"電商成長與轉換率"},{"date":null,"date_precision":null,"type":"regulatory","event":"Section 301 新關稅（2026-07-24 起）後續稅率調整","impact":"中","watch":"剔除退款的毛利率年變化與公司關稅說明"}],"_projected_from":"v19"}
```
