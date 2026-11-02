你是 stock-analyst v20 的**散文層（prose）agent**，標的 BWA（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：BWA　日期：2026-11-03　archetype：None　前份裁決：2026-05-24　B｜衛星候選｜等 W52 拉回 $46-50 後分批進場；近 4 月 +60% 短期 stretched，估值燈 🟡 不急建倉｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2405B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（524B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（706B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1195B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1118B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（1065B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（867B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2219B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4447B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2755B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2405           3216-4595      3 條（2–6 內）  
s3                  8000         524           5233-7476      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3019          8387-11981      5 條（2–6 內）  
s6                 11000        1065           6954-9935      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         867           1843-2633      5 條（2–6 內）  
s10                 5000        2219           1947-2781      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2755           2000-2245      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4869B；至少需散文≈40.13KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−67%
−55%
−55
−48%
−37%
−35%
−35
−24%
−21%
−20.7%
−20%
−18
−14%
−10%
−8%
−7%
−6.77%
−6.77
−6
−5%
−4.5%
−4%
−3.5%
−2.5%
−2%
−1.5%
−1
0%
0
0.1%
$0.17
0.24
0.74
0.75
$0.81
0.84
0.85
$0.9
0.94
0.96
01
1
$1.0
$1
1%
1.07
1.1
$1.21
$1.24
1.28
1.3%
1.3
$1.39
1.5
1.54%
1.6%
$1.6
1.7
1.7%
1.95
02
2
2.0
2%
2.08
2.2
$2.8
2.9%
03
3%
3
3.1%
$3.43
3.58%
3.65%
3.67%
3.8%
3.9
$3.9
4%
4
4.1%
4.1
4.3
$4.3
4.4
4.5%
$4.65
4.7
4.75
4.8
4.84
4.93
5
5%
$5
05
$5.05
5.18
$5.20
$5.2
5.2
$5.26
5.26
5.27
5.275
5.30
5.33
5.35
5.48%
$5.5
$5.75
5.75
5.90
5.9
6
$6
06
6%
6.05
6.3
6.5%
6.66
6.75
6.86%
6.95
7
$7.0
7%
7.15
7.5
7.52%
7.6
7.9
08
8%
8.0%
8
8.57%
8.7%
8.8
8.85
9%
09
9
9.16%
9.24%
9.5%
9.6%
9.75%
9.9
9.92
10
10%
10.1%
10.2%
10.2
$10.48
10.5%
10.7%
10.7
10.9%
11
11.4
12%
12
12.7
13
13%
14%
$14.0
14
$14.2
14.2
$14.3
14.7%
15%
15.2%
18%
18
18.09%
18.68%
18.8%
19.63%
19.8%
20%
20
20.7%
21%
22.1
24
25%
26
$27
27.1
27.7
28%
$28
29
30%
30
30.9%
31
32.25
33
33%
35%
$35
37.0%
37
39%
39.6%
40%
$40
42
$45
$45.78
$46
48
49
50
$51.94
52
52.2
$52.2
$54
$55
$57.39
$57.5
60%
65.82
$65.82
70
71%
71
$71.5
75%
$78.57
$78.6
80%
$80
84%
$85
90
$100
100
100%
104
$108
$112
114.4
150%
170
172
$175
200.8
$240
$249
$270
$277
$300
$338
$520
$630
$700
$708
$725
$729
$810
$855
2008
2009
2020
2022
2024
2025
2026
2027
2028
2029
2030
2034
20261103
$1,208
$1,372
$1,437
$1,616
$1,681
$1,968
$12,635
$14,086
$14,198
$14,316
$14,675
$3,487
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
{"meta":{"ticker":"BWA","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"BorgWarner Inc."},"oneliner":"BWA 前瞻本益比 9.9 倍、自由現金流殖利率約 9.5%，但利潤率在近年高點、2027 年車市有逆風；等 2027 年 2 月指引證明有機營收不落後市場、調整後 EPS 中點 ≥$5.75 再分批，渦輪發電機當期權看，不算進基礎","thesis":{"H":[{"id":"H1","text":"車用本業在產量下滑中守住調整後營業利益率，2027 年起有機營收不落後加權市場","2y":"FY2026 調整後營業利益率落在指引 10.7–10.9%；FY2027 ≥10.5%，且有機營收成長 ≥ 加權輕型車市場","5y":null,"10y":null,"threshold":"FY2026 調整後營業利益率 ≥10.7%；FY2027 ≥10.5%；有機營收成長減加權市場 ≥0pp","source":"季度新聞稿與法說（公司以地理曝險加權的輕型車產量作為市場口徑）","drift_rule":"TTM 調整後營業利益率連 2 季低於 10.2%（偏離 5%）＝削弱；連 3 季低於 9.6%（偏離 10%）＝反轉"},{"id":"H2","text":"渦輪發電機 2027 年營收約 $300M，首年增量利潤率中十幾 %","2y":"2026 年底完成試產；2027 上半年揭露客戶與出貨曲線；2027 年營收 ≥$300M","5y":null,"10y":null,"threshold":"2027 年營收 ≥$300M（管理層 2026-08-05 與 2026-10-29 兩次重申）；增量轉換 ≥13%","source":"2026-10-29 法說，CEO Joseph Fadool、CFO Craig Aaron；公司承諾 2027 年初揭露的成長曲線","drift_rule":"2027 年指引把 $300M 下修 5% 以上、連 2 季＝削弱；全年低於 $270M（偏離 10%）＝反轉"},{"id":"H3","text":"自由現金流每年 ≥$0.9B，約七成回饋股東，流通股每年減約 3–5%，支撐每股盈餘年增 ≥7%","2y":null,"5y":"FY2026–FY2030 平均自由現金流 ≥$0.9B；流通股數 FY2030 ≤172M 股（由約 200.8M 股每年減 3%）；調整後 EPS FY2030 ≥$7.0","10y":null,"threshold":"年度自由現金流 ≥$0.9B；年度股數減幅 ≥3%","source":"10-K／10-Q 現金流量表與稀釋股數","drift_rule":"TTM 自由現金流連 4 季低於 $855M（偏離 5%）＝削弱；連 6 季低於 $810M（偏離 10%）＝反轉"},{"id":"H4","text":"電動化產品轉為穩定獲利，避免燃油零件萎縮時整體利潤率被稀釋","2y":null,"5y":"PowerDrive 分部 2027 年調整後營業利益轉正，2030 年利潤率 ≥8%；eProduct 占營收由 2026 年 Q3 的 20% 升到 2030 年 ≥30%","10y":null,"threshold":"PowerDrive 分部 2027 全年調整後營業利益 ≥0；eProduct 占比每年增加 ≥2pp","source":"10-Q 分部揭露、季度法說","drift_rule":"PowerDrive 分部 TTM 利潤率連 4 季低於 0%，且 eProduct 營收年增 <15%＝削弱；連 6 季＝反轉"}],"R":[{"id":"R1","text":"2027–2028 年車市衰退式下滑：量一掉，遞減率會讓高檔利潤率快速回落。2009 年 Q2 營業利益率只剩 0.1%，2020 年 Q2 調整後 EBIT 只剩去年同期的約一成","h_ref":"H1","clock":"⚡","threshold":"有機營收連 2 季年減逾 5%，且調整後營業利益率 <10%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"id":"R2","text":"客戶集中與客戶信用：VW 13%、Ford 12%、前十大 71%，VW 評等降到 Baa1 且展望負面；失去主要平台或客戶逼價，衝擊會不成比例","h_ref":"H1","clock":"🔥","threshold":"VW 或 Ford 任一占營收 <8%，或 VW 長期評等再降一級以上","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R3","text":"關稅與貿易協定：2025 年關稅成本約 $108M，客戶回收約 $80M；USMCA 2026 年待續約；IEEPA 退款已收約 $35M，但金額與時點不確定，尚未認列","h_ref":"H1","clock":"🔥","threshold":"關稅淨成本年化 >$100M，或 USMCA 未續約","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"id":"R4","text":"燃油零件結構萎縮加上 OEM 自製：渦輪與熱管理分部營收與利潤率同步下滑，中國本土 OEM 把零件收回自製，eProduct 轉盈跟不上","h_ref":"H4","clock":"🐢","threshold":"渦輪與熱管理分部有機營收連 4 季年減逾 5%，或分部利潤率 <13%","evidence_refs":["end_markets#0","substitute_technology#1","competitive_share_entrants#1","customer_second_source#0","supply_demand_durability#1"]},{"id":"R5","text":"渦輪發電機時程或客戶落空：設備安裝 8 月說第三季開始，10 月改為 12 月；CEO 承認政治環境可能拖慢合約定案；交期、EBIT 與合約規模都未揭露","h_ref":"H2","clock":"🔥","threshold":"2027 年 Q1 前沒有揭露首批終端客戶，或下修 2027 年 $300M 目標","evidence_refs":[]}],"single_thing":{"description":"2027-02 公布的 2027 年調整後 EPS 指引中點，低於 2026 年水準（約 $5.26）","why_fatal":"公司每年靠回購減股約 4–5%，指引若仍是零成長，代表營業利益至少衰退約 5%，也就是車市衰退或高檔利潤率開始回落。這會同時打掉利潤率防守（H1）與回購複利（H3），倍數也會從約 10 倍往 7.5 倍走，股價對應約 $40 以下","if_happens":"不建倉；已持有者減碼一半，Bear 機率上調到 40%，重跑情境樹","how_monitor":"Q4 2026 財報（2027-02）。在那之前，看 2026 年 Q4 實際營收是否接近 CFO 給的約 $3.43B，以及法說會對 2027 年市場的說法","probability":"20%（12–24 個月）：CFO 已點名利率與購車負擔，但同時預期 2027 年有新案、渦輪發電機約 $300M，以及小幅超越市場"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":8.85,"peg_fy2":0.84,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":4.93,"FY2026E":5.26,"FY2027E":5.9,"FY2028E":6.66},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（非 GAAP）。FY2025A 4.93 由 2026-10-29 法說 CFO「2026 年指引中點約較 2025 年調整後 EPS 增 7%」回推（5.275 ÷ 1.07），事實表未直接收錄；FY2026E–FY2028E 為 Koyfin 2026-10-31 共識；2025 年 GAAP 稀釋 EPS 為 1.28"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"車用 Tier 1 動力系統零件，營收隨全球輕型車產量走：2009 年 Q2 營收年減 39.6%，2020 年上半年年減 28%。不屬商品子型（近年無虧損年、毛利率擺動小、不是報價型產品），屬需求量循環。"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉（量）：2026 年加權終端市場 −1~−2%（2026-10-29 法說），BCG 2026 年 3 月估至 2027 年供應商年成長約 2–3%。燃油零件組合另屬結構性萎縮：渦輪與熱管理分部 Q3 營收年減約 4.5%。","bargaining":{"up":"電子料成本上升，CFO 2026-10-29 說今年吸收得了、明年再看；碳化矽沿用車用供應商","down":"前十大客戶 71%，合約多為依排產的需求合約；2025 年關稅成本約 $108M，只向客戶回收約 $80M","geo":"中國約 20%（CEO 2026-08-05），其中約 75% 為中國本土 OEM（高盛轉述，二手）；美國以外約 84%（二手）；USMCA 2026 年待續約"},"profit_pool_dir":"利潤池由燃油動力系統往混動、純電的電機與電力電子移動，中國本土 OEM 同時把部分零件收回自製；車用以外，資料中心電力是新池，尚未有公司營收。","tam_table":{"expanded":false,"reason":"利潤池遷移（燃油→電動化、車用→資料中心電力）確實存在，但事實表沒有 TAM、滲透率或利潤池占比數字。Base 情境不靠新品類 TAM，只用公司給的 2027 年渦輪發電機約 $300M 目標，並在情境裡打折。"}},"moat":{"mechanism":"車款平台設計導入綁住整個車型生命週期（例如新 ECU 合約延到 2034 年），加上燃油、混動、純電三種架構都有產品與成本規模。換供應商的時點在新平台招標，轉換成本只在平台期間有效。","execution":8,"pricing":4,"grade":"C","trend":"→","trend_evidence":"執行力擴大：產量下滑中，調整後營業利益率由 2025 年 10.7% 擴到指引 10.7–10.9%；Q3 剔除匯率營收少 $112M，營業利益只少 $6M。定價力縮減：2025 年關稅成本約 $108M，只回收約 $80M；電子料通膨。份額穩定：前三季輕型車營收與加權市場同步，沒有縮減也沒有超越。兩個方向互相抵銷，判穩定。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用利潤率差代理，且只有單一期間","threats":[{"level":"🔴","text":"OEM 垂直整合：10-K 稱多家主要 OEM 表明要自製部分零件，中國本土 OEM 擴大市占，並把原由 Tier 1 供應的零件收回自製。這是生態層級的攻擊。","p":"35%","evidence_refs":["customer_second_source#0","competitive_share_entrants#1","substitute_technology#1"]},{"level":"🟡","text":"燃油車結構萎縮壓縮渦輪與熱管理分部：Q3 分部營收 $1,372M（去年 $1,437M），利潤率 14.7%（去年 15.2%）。公司 eProduct 同期成長 33%，屬產品層級替代、可部分對沖，所以不列為架構替代；代價是組合轉換期間利潤率被稀釋。","p":"40%","evidence_refs":["end_markets#0","substitute_technology#1"]},{"level":"🟡","text":"供應商利潤率結構重置與中國供應商低價（Ken Research 二手意見）。BWA 2026 年利潤率仍在擴張，尚未反映在財報上，但屬破壞性競爭，機率取下限 30%。","p":"30%","evidence_refs":["supply_demand_durability#1"]}],"roic_durability":{"quadrant":"無法定象限：事實表未涵蓋投入資本與周轉率。營業利益率在同業屬高檔，但絕對值約 10%，暫視為中等利益率，周轉率待補","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是駕駛，決策者是 OEM 工程與採購，付款者是 OEM，三個角色都成立；不論燃油、混動、純電，每台車都要動力系統零件，需求是必要而非想要。但量隨車市：2026 年加權市場 −1~−2%、中國 −6~−8%，CFO 預告 2027 年有利率與購車負擔逆風。延後買車的代價低，急迫性不等於持久性。"},{"item":"決策層級","level":"🟡","text":"替代性要看平台招標這一層。設計導入後，供貨綁住整個車型生命週期，平台期間轉換成本高；但每個新平台都重新報價。BWA 自己在中國以 VCT 取代既有供應商、拿下渦輪 conquest 案，可見招標點換供應商是常態；10-K 也稱多家 OEM 表明要自製部分零件。"},{"item":"價值鏈分配","level":"🔴","text":"議價權在 OEM：前十大客戶占 71%，合約多為依排產的需求合約；2025 年關稅成本 $108M，只回收 $80M；Ken Research 稱供應商利潤率是結構性重置（二手）。BWA 營益率高於同業，靠的是成本執行，不是分到更大的利潤池。"},{"item":"社會容忍度","level":"🟢","text":"單一零件占整車成本低，沒有價格管制，也沒有社會對漲價的反彈問題。政策風險在別處：2025 年關稅、USMCA 2026 年待續約、電池事業因北美缺乏補貼而衰退。美國限制外國電網設備的行政命令若落實，反而有利於美國製造的微電網逆變器（CEO 2026-10-29）。"}],"roiic":"事實表未涵蓋（缺投入資本）","reinvest_rate":"事實表未涵蓋（缺資本支出、折舊、營運資金變動）","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率 × 投入資本周轉率；內生成長率＝增量 ROIC × 再投資率。事實表只有 TTM 營業利益率 10.2%，沒有投入資本、資本支出、折舊、營運資金，三項都無法計算，列為資料缺口。代理讀數：2022→2025 年營收增 $1,681M，GAAP 營業利益增約 $240M（增量利潤率約 14%），但缺投入資本，無法換算成報酬率"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","BWA":19.8,"APTV":19.63,"LEA":6.86,"MGA":14.71,"unit":"%"},{"metric":"營業利益率","BWA":10.2,"APTV":9.75,"LEA":3.67,"MGA":5.48,"unit":"%"},{"metric":"FCF 利潤率","BWA":9.16,"APTV":3.65,"LEA":3.58,"MGA":7.52,"unit":"%"}],"competitors":[{"name":"APTV","gm":19.63,"om":9.75,"fcf_margin":3.65,"strategy_note":"毛利率 19.63% 與 BWA 相當，營益率 9.75% 略低，但 FCF 利潤率只有 3.65%，BWA 現金轉換明顯較好；同業期間截至 2026-06-30，差一季","period":"TTM ending 2026-06-30（4季加總）"},{"name":"LEA","gm":6.86,"om":3.67,"fcf_margin":3.58,"strategy_note":"毛利率 6.86%、營益率 3.67%、FCF 利潤率 3.58%，三項都遠低於 BWA，顯示 Tier 1 之間利潤池位置差距大","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MGA","gm":14.71,"om":5.48,"fcf_margin":7.52,"strategy_note":"Magna Powertrain 是 10-K 點名的非 OEM 主要對手；Magna 營益率 5.48%、FCF 利潤率 7.52%，BWA 營益率高約 4.7pp","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量：輕型車與市場同步（2026 年加權 −1~−2%），2027 年起有新案與渦輪發電機約 $300M；價：議價與關稅轉嫁不足，為負；併購：零；回購：過去四季約市值 6%，2026 年約七成自由現金流回饋股東；利潤率：成本控制與稅率","runway_years":"核心車用是成熟市場，滲透率年數不適用；eProduct 占營收 Q3 為 20%，事實表沒有歷年占比序列，無法推算到 30% 需要幾年","runway_post_y5":"🟡","endo_ceiling_basis":"無法計算：事實表沒有投入資本、資本支出、折舊與營運資金，增量 ROIC 與再投資率都是缺口。以營收年增約 4%（共識 FY2027）當內生量能代理，共識 EPS 三年年複合約 10.5%，超出代理值約 6pp；缺口可歸因於淨回購約 4–5pp 與利潤率擴張","segments":[{"item":"渦輪與熱管理（Q3 2026）","value":"營收 $1,372M（去年同期 $1,437M），分部調整後營業利益率 14.7%（去年 15.2%）；來源 10-Q 2026-09-30"},{"item":"PowerDrive（Q3 2026）","value":"季營收約 $700M 以上，EBIT 虧損約 $5M，季增約 20%；CFO 預期 2026 全年成長約 20%，目標增量轉換中十幾 %"},{"item":"eProduct 合計","value":"Q3 約 $708M，占營收 20%；前九月約 $1,968M，占 18%；Q3 輕型車 eProduct $630M，年增 33%，主要來自歐洲"},{"item":"電池儲能系統事業","value":"Q3 營收年減 $54M，全年拖累營收成長約 170bp；分部營收與利潤事實表未涵蓋"},{"item":"其餘分部","value":"事實表未涵蓋"},{"item":"資料中心與工業（2027 年起）","value":"渦輪發電機 2027 年營收目標約 $300M，首年增量轉換中十幾 %；電池儲能 2027 年量產就緒；微電網逆變器樣品已送 7 家客戶，UL 認證預計 2027 年初完成"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"季度毛利率事實表未涵蓋；年度依序 18.09%、18.8%、18.68%，TTM 19.8%"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"前三季輕型車營收大致與加權市場同步，未見縮減，也未見超越"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"事實表未涵蓋"},{"signal":"EPS 成長顯著高於營收成長（差逾 5pp）","lit":true,"note":"共識 EPS 三年年複合約 10.5%，共識營收 FY2027 只增 4.1%"},{"signal":"自由現金流／淨利連 2 年低於 0.75","lit":false,"note":"2024 年約 2.2 倍、2025 年約 4.4 倍"},{"signal":"SBC／營收逾 5% 且上升","lit":false,"note":"事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"note":"渦輪與熱管理分部 Q3 營收年減約 4.5%；電池事業因補貼缺口衰退"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數事實表未涵蓋"},{"signal":"維護性資本支出占自由現金流逾 60%","lit":false,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"營收四年持平，但仍在投資渦輪發電機廠與 2GW 產能"}],"trap_rating":"🟡（衰退信號亮 2 項）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購：近 12 個月沒有併購類 8-K，EPS 成長來源是回購與利潤率；回購與股息已寫在回購項，不另展開"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 無併購類重大項目；歷史併購的已實現報酬事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"現價回購的盈餘收益率約 10.1%（5.26 ÷ 52.2），以 $65.82 高位計約 8.0%；過去四季回購約 $725M、約市值 6%。10 年期殖利率事實表未涵蓋，低於約 6% 即過","grade":"過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 事實表未涵蓋；回購使淨股數下降，但毛稀釋率無法驗證","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（調整後 EPS）","tier":"車用 Tier 1 動力系統零件","peers":{"expanded":false,"reason":"事實表同業對照只有毛利率、營益率與 FCF 利潤率，沒有同業前瞻本益比或 EV 倍數，無法做倍數對照；終端倍數以自身現值與 4 個年度端點為錨"},"fwd_pe":9.92,"peg":0.94,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 9.9 倍、PEG 0.94 指向便宜，但有三點抵銷。第一，股價營收比 0.74 倍在近 4 個年度端點的最高點，EV/S 在 71 分位，營收端並不便宜。第二，調整後營業利益率在近年高點，循環股的低本益比可能落在高峰盈餘上。第三，以 Base 路徑與 10 倍終端倍數，五年年化約 7–9%（含股息），落在弱與中的交界。綜合判合理，不到便宜。五年分位：事實表只有 4 個年度端點，依規不外推，留空。","upside_short_pct":10.2,"upside_mid_pct":37.0},"trap_analysis":{"verdict":"🟡","label":"利潤率高檔的循環股：低本益比可能是對高峰盈餘的折價"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2008-05 到 2009-01 股價約 −67%；2009 年 Q2 營收年減 39.6%、調整後營業利益率 0.1%；2020 年上半年營收年減 28%、Q2 調整後 EBIT $28M；2008–09 年產業零件出貨連兩年 −14%、−24%","assumption":"2027–2028 年加權車市不出現年減 8% 以上的衰退，Q4 指引的中十幾 % 遞減率在更大跌幅下仍然成立","consequence":"EPS 落到約 $3.9–4.4、倍數壓到 7–7.5 倍，股價約 $27–33（−37%～−48%），這是五年後虧損接近五成最可能的故事","ruling":"採納：Bear 機率給 30%，最大回撤給 −35%～−55%。不照搬 2009 年 −67%，因為目前淨槓桿約 1.5 倍、2025 年自由現金流 $1.21B，但這只能降低幅度。這條與唯一致命點部分重疊：致命點是這個故事最早可觀察到的結果（2027 年 EPS 指引），已補進觸發器","watch":"季度有機營收年增率對公司口徑的加權輕型車市場；連 2 季年減逾 5% 即減碼","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"],"fact_refs":["f_net_debt_m","f_kpi3_free_cash_flow"]},{"view":"論點失敗","evidence":"渦輪與熱管理分部 Q3 營收 $1,372M（去年 $1,437M），利潤率 14.7%（去年 15.2%）；10-K 稱多家主要 OEM 表明要自製部分零件，中國本土 OEM 擴大自製；Ken Research 稱供應商利潤率結構重置；Pitchgrade 指渦輪的替代風險最高（二手）","assumption":"燃油零件萎縮的速度，慢於 eProduct 轉盈的速度，組合轉換期間整體利潤率不被稀釋","consequence":"高利潤的燃油零件每年縮 5% 以上，低利潤的 PowerDrive 補不上，調整後營業利益率回到 9% 附近，EPS 年增歸零","ruling":"部分採納：列為長期風險並設分部門檻。不據此把護城河方向標為往下，因為公司整體有機營收仍與市場同步；本季也在中國拿到鋁線電機首案與三件電機案，在歐洲與南美拿到渦輪 conquest 案","watch":"渦輪與熱管理分部的有機營收年增率與利潤率；PowerDrive 分部損益","evidence_refs":["end_markets#0","competitive_share_entrants#1","customer_second_source#0","substitute_technology#1","supply_demand_durability#1"],"fact_refs":["f_kpi1_adjusted_operating_incom"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 2026-10-29 稱併購『已打開視野』，車用內外都在看；渦輪發電機產能是否擴充尚未決定；逆變器的產能投資規模，8 月法說不願回答。VW 評等降到 Baa1、S&P 展望負面；VW 占營收 13%、Ford 12%，前十大 71%","assumption":"資料中心業務成功後，公司仍把約七成自由現金流回饋股東，不用高價併購或大額資本支出換成長；主要客戶的財務壓力不會轉成更狠的降價","consequence":"成長兌現，但每股價值被稀釋：回購降速、資本支出拉高、併購溢價吃掉報酬；或 VW 等客戶逼價，讓車用利潤率掉 50–100bp","ruling":"採納為監測項。管理層的三條併購準則（核心能力、近期增厚、不多付）是目前唯一的約束；任何超過市值 5%（約 $520M）的交易，都要重跑分析","watch":"每季回購金額（Q4 預計 $175M）、資本支出指引、併購公告、VW 長期評等","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"],"fact_refs":["f_ev_m","f_kpi3_free_cash_flow"]},{"view":"價格已反映太多","evidence":"股價營收比 0.74 倍，在近 4 個年度端點的最高點，EV/S 0.85 倍在 71 分位；共識 FY2027–FY2028 EPS 年增約 12–13%，但共識營收 FY2027 只增 4.1%；2025 年關稅成本 $108M，只回收 $80M","assumption":"共識已把渦輪發電機 $300M、利潤率續升與回購全部算進去，營收端倍數並不便宜","consequence":"若 2027 年只有回購帶來的成長，EPS 約 $5.5，10 倍只值 $55，上行僅約一成","ruling":"部分採納：這是估值只給合理、不給便宜的原因。但前瞻本益比 9.9 倍本身不要求倍數擴張，所以不構成迴避理由","watch":"2027 年指引的 EPS 中點與共識 5.90 的差距","evidence_refs":["reg_tariff_export#0"],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy2","f_rev_consensus_fy2_m"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 65.82 → 本次 52.2（-20.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=65.82","side_b":"本次 price_at_dd=52.2","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 65.82 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 65.82 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 65.82 美元：Bull 價 114.4、Bear 價 32.25，五年期望值 +3.8%，基準年化 1.7%，不對稱比 0.96","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.96。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 65.82 美元：五年期望值 +3.8%，基準年化 1.7%，不對稱比 0.96","side_b":"本次情境、股價 52.2 美元：五年期望值 +30.9%，基準年化 6.5%，不對稱比 2.08","ruling":"再換股價、情境不動：起點價下跌 20.7%，五年期望值多 27.1 個百分點，基準年化多 4.8 個百分點，不對稱比由 0.96 升到 2.08。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷","cause":null,"side_a":"公司、賣方與事實表三方一致：自由現金流強（2025 年 $1.21B、2026 年指引 $0.9–1.1B），回購持續，2026 年在產量下滑中利潤率仍擴張","side_b":null,"ruling":"一致，不需要裁決；這是 H3 的證據基礎","evidence_level":"高","settle_metric":"年度自由現金流","if_then":[],"evidence_refs":[]},{"axis":"賣方目標價與股價方向相反","cause":null,"side_a":"賣方平均目標價 $78.57（MarketBeat 2026-10-10，共識偏買進）；Q2 後 JPMorgan 上調到 $85、Barclays 上調到 $85；FY1 共識 EPS 近 3 個月上修 1.54%","side_b":"股價由前份的 $65.82 跌到 $52.2（−21%），26 週報酬 −6.77%，RSI 27.7。盈餘上修而股價下跌，等於倍數由約 12.7 倍壓到 9.9 倍","ruling":"性質：不可調和（方向相反）。裁決站市場一側的一半。賣方目標價隱含約 13 倍 FY2027 EPS，需要倍數重新評價；而 Q3 的 EPS 上修來自回購與稅率，營收區間上緣反而下修，有機營收指引由 −3.5%～−1.5% 降到 −4%～−2.5%。市場為 2027 年車市逆風打折（CFO 點名利率與購車負擔）有根據。決勝的硬數據是 2027 年 2 月的指引。現在就買的最強論證：自由現金流殖利率約 9.5%，股息 1.3% 加回購約 5%；即使 EPS 零成長、倍數不變，也有中個位數報酬。而且 RSI 已超賣，股價離 104 週均線 $45.78 只剩約 12%","evidence_level":"高（公司指引與共識快照）","settle_metric":"2027 年調整後 EPS 指引中點與有機營收指引","if_then":["若 2027 年指引的有機營收不落後市場，且調整後 EPS 中點 ≥$5.75，則重跑分析後以 2% 首倉分批建立","若股價先跌到 $45 以下，但最近一季有機營收年減未逾 5%，則分批反買，倉位上限 3%","反向：若指引的 EPS 中點 <$5.26，或有機營收年減逾 5%，則不建倉，已持有者減碼一半"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"EPS 上修與營收下修","cause":null,"side_a":"Q3 調整後 EPS $1.39，高於共識約 $1.24（二手來源）；全年調整後 EPS 指引由 $5.05–5.30 上調到 $5.20–5.35","side_b":"Q3 營收年減約 2.9%；全年營收區間上緣由 $14.3B 降到 $14.2B；有機營收指引由 −3.5%～−1.5%（2026-08-05 CFO Craig Aaron）降到 −4%～−2.5%（2026-10-29）。EPS 上調的原因是回購與稅率","ruling":"性質：可調和（程度差異）。盈餘品質靠成本控制與回購，不是靠量；這支撐 H3，不支撐 H1，所以 2027 年有機營收是決勝數據","evidence_level":"高（公司前後兩次指引）","settle_metric":"2027 年有機營收指引減加權市場","if_then":["若 2027 年有機營收指引不落後市場，則 H1 成立，依首倉條件分批建立","若有機營收落後市場逾 2pp，而 EPS 仍靠回購上修，則不追，維持觀望"],"evidence_refs":[]},{"axis":"管理層 8 月承諾與 10 月實績","cause":null,"side_a":"2026-08-05 CEO Joseph Fadool：渦輪發電機組裝廠設備預計第三季開始安裝；今年會有部分電池儲能訂單；對目前超越市場的幅度不滿意，新案會改善","side_b":"2026-10-29 CEO：廠房完工，產線與設備安裝預計 12 月，年底開始試產；電池儲能只說專注拿下第一張訂單，2027 年再多說；Q3 輕型車營收仍只與市場同步。已兌現的部分：UL 子系統認證大致完成，微電網逆變器樣品由 4 家客戶增到 7 家","ruling":"性質：可調和（時程延後約一季，未改 2027 年 $300M 目標）。但三項承諾裡有兩項落後，Base 只給渦輪發電機 2027 年營收約六成把握，其餘放在 Bull","evidence_level":"中（管理層口頭陳述，沒有合約揭露）","settle_metric":"2026 年底試產是否完成；2027 年初揭露的出貨曲線與首批客戶","if_then":["若 2027 年 Q1 法說確認試產完成，並揭露首批終端客戶，則 Base 維持 $300M","若 2027 年 Q1 仍無客戶合約，或目標下修，則把渦輪發電機貢獻移出 Base，Bear 機率上調到 35%"],"evidence_refs":[]},{"axis":"客戶多元的說法與集中度數據","cause":null,"side_a":"2026-10-29 CEO：公司大概是動力系統領域客戶組合最多元的一家，一家客戶輸、另一家客戶就贏","side_b":"10-K：VW 13%（2024 年 10%）、Ford 12%，前十大 71%；VW 2025-03 遭 Moody's 降到 Baa1，展望負面","ruling":"性質：可調和（相對同業多元，絕對值仍集中）。列為中期風險，不當護城河證據","evidence_level":"高（10-K）","settle_metric":"年度前兩大客戶占比與 VW 評等","if_then":["若 VW 或 Ford 任一失去主要平台、占比跌到 8% 以下，則減碼一半","若 VW 長期評等再降到投資級最低一級以下，則停止加碼"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"axis":"估值與評等（股價下跌）","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份 2026-05-24：股價 $65.82，評等 B，估值合理，裁決為等 W52 拉回 $46–50 後分批進場","side_b":"本次 2026-11-03：股價 $52.2（−21%）；FY1 共識 EPS 三個月由 5.18 升到 5.26；前瞻本益比由約 12.7 倍（以 5.18 粗算）降到 9.92 倍。估值仍判合理，但由偏上移到偏下；評等維持 B；裁決與角色依本次輸入重算","ruling":"估值改善全部來自股價，基本面只小幅上修。維持合理而非便宜，理由見估值題：利潤率在高點，營收端倍數在 4 年端點的高位","evidence_level":"高","settle_metric":"前瞻本益比與 2027 年指引","if_then":["若股價跌到 $45 以下，而有機營收年減未逾 5%，則分批反買"],"evidence_refs":[]},{"axis":"價值陷阱判讀","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱風險為 🟡","side_b":"本次仍為 🟡：衰退信號亮兩項（EPS 成長高於營收成長逾 5pp；燃油零件被替代技術壓縮）。新證據是 Q3 渦輪與熱管理分部的營收與利潤率同步下滑，以及 10-K 的 OEM 自製風險","ruling":"結論不變，依據換成本季的分部數據","evidence_level":"中","settle_metric":"渦輪與熱管理分部有機營收","if_then":["若亮燈增加到 3 項，則改判高風險並停止加碼"],"evidence_refs":["end_markets#0"]},{"axis":"前份未記錄的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這七欄皆為空（舊格式未產出）","side_b":"本次：護城河方向 →；五年後跑道 🟡；主型為循環/商品；循環位置為中循環；情境機率 20／50／30；最大回撤 −35%～−55%","ruling":"這不是判斷翻轉，是格式補欄；之後以本次為比較基準","evidence_level":"—","settle_metric":"下一份判斷的同欄比較","if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場欄；裁決文字為「等 W52 拉回 $46-50 後分批進場」","side_b":"本次：2027-02 公布的 2027 年指引，有機營收成長不低於加權市場，且調整後 EPS 中點 ≥$5.75，則重跑分析後以首倉 2% 分批建立；若價格先到 $45 以下，且有機營收年減未逾 5%，則可提前分批反買、加碼","ruling":"由價格錨改為事件錨。股價已跌到 $52.2、接近前份區間，但 Q3 有機營收指引下修，CFO 又點名 2027 年逆風，決勝點從價格變成 2027 年車市。價格條件下移到 $45（約 FY2027 共識 7.6 倍），只留作反買用","evidence_level":"中","settle_metric":"2027 年指引","if_then":["若 2027 年指引符合條件，則首倉 2% 分批建立","若指引的 EPS 中點 <$5.26，則不建倉"],"evidence_refs":[]},{"axis":"出場門檻（減碼與清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（空）；前份的風險門檻為：連 4 季集團營業利益率 <9.5%，連 4 季 Air Management 有機營收 <−7%","side_b":"本次：TTM 調整後營業利益率連 3 季 <9.6% 則清倉；有機營收連 2 季落後市場逾 2pp 則減碼；2027 年 EPS 指引中點 <$5.26 則減碼一半；渦輪與熱管理分部有機營收連 4 季 <−5% 則停止加碼；年度自由現金流 <$0.81B 則減碼","ruling":"門檻改用與 H1、H3 漂移規則同一套數字（偏離 5%／10%）。燃油分部門檻由 −7% 收緊到 −5%，因為 Q3 已出現約 −4.5% 的營收跌幅，等到 −7% 會太晚","evidence_level":"中","settle_metric":"季報","if_then":[],"evidence_refs":["end_markets#0"]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（空）","side_b":"本次 Single Thing：2027-02 公布的 2027 年調整後 EPS 指引中點，低於 2026 年水準（約 $5.26）","ruling":"選這一項，是因為車市量能是數學上最大的單一敏感度：量每少 10%，EPS 約少 18–20%；而年度指引是最早、最明確的二元觀察點。渦輪發電機延遲對 EPS 的影響約 $0.17，較小","evidence_level":"中","settle_metric":"2027 年指引","if_then":["若發生，則不建倉，已持有者減碼一半"],"evidence_refs":[]},{"axis":"假設與風險改寫","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份 H1：eProducts 2027 年營收 ≥$4.3B（占 25%）且利潤率 ≥8%；R1：連 4 季集團營業利益率 <9.5%；R2：合併案與中國電動車價格戰；R3：連 4 季 Air Management 有機營收 <−7%","side_b":"本次 eProduct 前九月約 $1,968M（18%）、Q3 約 $708M（20%），年化約 $2.8B，2027 年 $4.3B 已不可能達成。H1 改為車用本業利潤率防守與不落後市場；eProduct 改為 2030 年占比 ≥30% 的五年假設（H4）；燃油分部風險改用渦輪與熱管理分部口徑；前份 R2 的價格戰併入護城河威脅中的供應商利潤率重置項","ruling":"前份 H1 依新證據判為失敗並退休，理由是 eProduct 的實際規模只有目標的約三分之二。前份 R1 的 9.5% 門檻保留在 H1 反轉線附近（9.6%），沒有刪除","evidence_level":"高（10-Q）","settle_metric":"eProduct 占營收比","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年 2 月財報給出 2027 年指引：有機營收成長不低於加權市場，且調整後 EPS 中點 ≥$5.75","type":"估值rearm","maps_to":"H1","metric":"2027 年有機營收指引減加權市場；調整後 EPS 指引中點","threshold":"≥0pp 且 ≥$5.75","action":"觸發後重跑分析，確認後以首倉 2% 分三批建立，上限 3%","source_freq":"年度指引（Q4 財報）","date":"2027-02"},{"n":2,"text":"股價先跌到 $45 以下，但最近一季有機營收年減未逾 5%","type":"加碼","maps_to":"H3","metric":"股價；季度有機營收年增率","threshold":"≤$45 且 ≥−5%","action":"分批反買 1%，總倉位上限 3%","source_freq":"每日股價／季報","date":null},{"n":3,"text":"Single Thing：2027 年調整後 EPS 指引中點低於 2026 年水準","type":"Single Thing","maps_to":"Single Thing","metric":"2027 年調整後 EPS 指引中點","threshold":"<$5.26","action":"不建倉；已持有者減碼一半，Bear 機率上調到 40%","source_freq":"年度指引","date":"2027-02"},{"n":4,"text":"車市衰退：有機營收連 2 季年減逾 5%，且調整後營業利益率跌破 10%","type":"減碼","maps_to":"R1","metric":"季度有機營收年增率；調整後營業利益率","threshold":"連 2 季 <−5% 且 <10%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"n":5,"text":"H1 反轉：TTM 調整後營業利益率連 3 季低於 9.6%","type":"清倉","maps_to":"H1","metric":"TTM 調整後營業利益率","threshold":"連 3 季 <9.6%","action":"清倉","source_freq":"季報","date":null},{"n":6,"text":"燃油零件萎縮加速：渦輪與熱管理分部有機營收連 4 季年減逾 5%，或分部利潤率跌破 13%","type":"風險","maps_to":"R4","metric":"渦輪與熱管理分部有機營收年增率；分部調整後營業利益率","threshold":"連 4 季 <−5% 或 <13%","action":"停止加碼，Bear 機率上調到 35%","source_freq":"10-Q 分部揭露（每季）","date":null,"evidence_refs":["end_markets#0","substitute_technology#1"]},{"n":7,"text":"渦輪發電機兌現：年底完成試產，2027 年 Q1 揭露首批終端客戶與出貨曲線","type":"假設驗證","maps_to":"H2","metric":"首批終端客戶合約；2027 年營收目標","threshold":"2027 年 Q1 前揭露，且目標維持 ≥$300M","action":"未兌現就把渦輪發電機移出 Base","source_freq":"季度法說","date":"2027-05"},{"n":8,"text":"關稅吸收失敗：關稅淨成本（費用減客戶回收）年化逾 $100M，或 USMCA 未續約","type":"風險","maps_to":"R3","metric":"關稅費用減回收；USMCA 續約結果","threshold":"逾 $100M／年，或未續約","action":"停止加碼","source_freq":"10-K／10-Q MD&A","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":9,"text":"主要客戶流失：VW 或 Ford 任一占營收跌到 8% 以下","type":"減碼","maps_to":"R2","metric":"前兩大客戶營收占比","threshold":"<8%","action":"減碼一半","source_freq":"10-K（每年）","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":10,"text":"Q4 2026 財報與 2027 年指引公布後重跑分析","type":"複審日期","maps_to":null,"metric":"—","threshold":"—","action":"重跑分析","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"TTM 調整後營業利益率","bear_threshold":"連 3 季 <9.6% → 清倉","window":"2027–2028 年","source":"季度新聞稿","last_status":"ok"},{"metric":"季度有機營收年增率減加權輕型車市場","bear_threshold":"連 2 季落後逾 2pp → 減碼","window":"2027 年","source":"季度法說（公司的市場口徑）","last_status":"ok"},{"metric":"2027 年調整後 EPS 指引中點","bear_threshold":"<$5.26 → 減碼一半","window":"2027-02","source":"Q4 2026 新聞稿","last_status":"unknown"},{"metric":"渦輪與熱管理分部有機營收年增率","bear_threshold":"連 4 季 <−5% → 停止加碼","window":"2027–2028 年","source":"10-Q 分部揭露","last_status":"warning"},{"metric":"年度自由現金流","bear_threshold":"<$0.81B → 減碼","window":"FY2026–FY2028","source":"10-K 現金流量表","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-6.77, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027-02 公布的 2027 年指引：有機營收不落後加權市場，且調整後 EPS 中點 ≥$5.75；或股價先跌到 $45 以下，且有機營收年減未逾 5%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"3%","requires_critic":[],"rearm_trigger":"2027-02 公布的 2027 年指引：有機營收成長不低於加權市場，且調整後 EPS 中點 ≥$5.75","exec_line":"觸發後重跑分析，確認後以 2% 首倉分三批建立，上限 3%；若股價先跌到 $45 以下、但有機營收年減未逾 5%，可分批反買；Single Thing 發生則不建倉"},"reasoning":{"industry":"最新一季（Q3 2026）營收 $3,487M，年減約 2.9%，有機年減 3.1%。剔除電池事業後有機年減 1.6%，大致等於輕型車產量跌幅。調整後營業利益率 10.9%（去年同期 10.7%），GAAP 營業利益率 8.7%；TTM 毛利率 19.8%。調整後 EPS $1.39，年增 12%，增幅來自稅率與過去四季約 $725M 回購（約市值 6%），不是營運量能。分部：渦輪與熱管理 $1,372M（約 39%，利潤率 14.7%）；PowerDrive 季營收約 $700M 以上，季虧約 $5M；eProduct 合計約 $708M（20%）；其餘分部事實表未涵蓋。輕型車占營收 80% 以上。收錢方式依 10-K：年度合約或長期供貨協議，按 OEM 排產出貨，量隨車市走。單點依賴：Volkswagen 13%、Ford 12%，前十大客戶 71%，這是集中度風險，不是護城河證據；中國約占 20%（CEO 2026-08-05）。產業時鐘在收縮段：2026 年加權終端市場 −1~−2%、中國 −6~−8%，CFO 點名 2027 年有利率與購車負擔逆風。供需上，量是週期性、會反轉，燃油零件組合則是結構性萎縮。產業態勢判為雙向拉鋸：競爭端，中國 OEM 自製與供應商利潤率重置在惡化；結構端，電動化（Q3 輕型車 eProduct 年增 33%）與資料中心電力在打開新利潤池；其他結構變數（關稅、USMCA 續約）偏負。循環位置判中段：需求量未見向上拐點；倍數在自身 4 個年度端點的中位到偏高；情緒超賣（RSI 27.7），賣方目標價高於股價約五成。訊號互相矛盾，不給循環進場姿態。","moat":"事實表沒有同業 ROIC，可證方向改用同業利潤率差代理。BWA TTM 營業利益率 10.2%，高於 APTV 9.75%、MGA 5.48%、LEA 3.67%；FCF 利潤率 9.16%，對三家的 3.65%、7.52%、3.58% 優勢更大。同業資料截至 2026-06-30，BWA 截至 2026-09-30，期間差一季；而且只有單一期間，價差是擴大還是收窄無法判斷。自身 GAAP 營業利益率 2022–2025 由 8.57% 升到 9.24%，TTM 10.2%，方向往上。執行力 8 分：2026 年產量下滑，仍把調整後營業利益率守在 10.7–10.9%；新案不斷，包括中國 VCT 取代既有供應商（CEO 2026-08-05）、全球動力系統大廠的三件渦輪 conquest 案、中國鋁線電機首案（2026-10-29）。定價力 4 分：2025 年關稅只轉嫁約七成；CFO 說電子料通膨今年吸收、明年再看；前十大客戶占 71%。份額方面，2026 前三季輕型車營收大致與加權市場同步；CEO 2026-08-05 說對目前超越市場的幅度不滿意，Q3 仍未見超越，所以不標往上。最大威脅是 OEM 自製（10-K 風險因素），屬生態層級。燃油車萎縮方面，公司自己也賣替代產品，算產品層級替代，不算整體架構出局。","growth":"營收 2022–2025 年依序為 $12,635M、$14,198M、$14,086M、$14,316M，2026 年指引 $14.0–14.2B，四年幾乎沒長；共識營收 FY2027 為 $14,675M（+4.1%）。共識調整後 EPS 路徑：FY2025A 約 4.93（由 2026-10-29 CFO「指引中點約較 2025 年增 7%」回推）→ FY2026E 5.26 → FY2027E 5.90 → FY2028E 6.66，三年年複合約 10.5%，比營收成長高 6pp 以上。成長拆解：量約 0～+4%；價為負（議價與關稅轉嫁不足）；併購為零；回購每年約減股 4–5%（過去四季約市值 6%）。內生上界無法計算（缺投入資本、資本支出、折舊），改用營收年增約 4% 當量能代理，缺口約 6pp。缺口歸因：淨回購約 4–5pp；利潤率擴張約 1–2pp，包括成本控制、稅率，以及渦輪發電機 2027 年約 $300M、以中十幾 % 增量轉換，約貢獻每股 $0.17（以 25% 稅率、約 1.95 億股粗估）。缺口可歸因，不靠倍數重新評價。跑道：核心車用是成熟市場，滲透率概念不適用；eProduct 占營收由前九月 18% 升到 Q3 20%，PowerDrive 2026 年預期成長約 20%。第二條曲線（渦輪發電機、電池儲能、微電網逆變器）有廠房完工、UL 認證、7 家客戶取得樣品等具體進度，但沒有已揭露的終端客戶合約，算不上已證實的下一條曲線，所以給中而不給寬。衰退信號亮兩項：EPS 成長高於營收成長逾 5pp，以及燃油零件被替代技術壓縮。","governance":"現金轉換：2025 年自由現金流 $1,208M，對 GAAP 淨利 $277M 約 4.4 倍；2024 年 $729M 對 $338M 約 2.2 倍。GAAP 淨利被非現金項目壓低，現金面比帳面好。2026 年指引自由現金流 $0.9–1.1B、營運現金流 $1.6–1.7B。現金去向：股東回饋 2026 年預計逾 $700M（Q3 回購 $175M、股息 $35M，Q4 回購同規模），約占自由現金流七成。Q3 另做了債務收購（CFO 稱可增厚 EPS），淨槓桿 1.5 倍，目標 2.0 倍。資本支出投向北卡羅來納的渦輪發電機組裝廠與 2GW 產能，產能是否擴充尚未決定。近 12 個月沒有併購類 8-K；CEO 稱併購範圍已擴大到車用以外，但維持三條準則。回購報酬：以判斷日股價 $52.2 與 FY2026 共識 EPS 5.26 計，盈餘收益率約 10.1%；以前份判斷日 $65.82 的高位計也約 8.0%。自由現金流指引中點 $1.0B 對市值約 $10.48B，約 9.5%。10 年期公債殖利率事實表未涵蓋，只要低於約 6%，回購就過關。目前淨負債 $1,616M。SBC 占營收比、歷史併購的已實現報酬，事實表都未涵蓋。","valuation":"前瞻本益比 9.92 倍（FY2026 共識 5.26），以 FY2027 計 8.85 倍。Trailing GAAP 本益比 22.1 倍被減損等項目扭曲，不採用。PEG 0.94（9.92 ÷ 三年 EPS 年複合 10.5%）。歷史位置只有 4 個年度端點可用：本益比在 48 分位；股價營收比 0.74 倍在最高點；EV/S 0.85 倍在 71 分位。營收端並不便宜，而且這不能當五年分位用。分母檢查：調整後 EPS 2026 年指引 $5.20–5.35，GAAP $4.65–4.84，差約一成；以 GAAP 中點計前瞻本益比約 11 倍，結論不變。自由現金流佐證調整後盈餘有現金支撐，分母不構成爭點。賣方平均目標價約 $78.6（MarketBeat 2026-10-10），隱含約 13 倍 FY2027 EPS，需要倍數重新評價，本次 Base 不採用。上行空間：一年以 Base FY2027 EPS 5.75 × 10 倍＝$57.5（+10.2%）；五年以 Base FY2030 EPS 7.15 × 10 倍＝$71.5（+37.0%）。同業前瞻倍數事實表未涵蓋，終端倍數只能對照自身現值 9.9 倍。","premortem":"最強的三個反駁如下。一是循環：2008-05 到 2009-01 股價約 −67%，2009 年 Q2 調整後營業利益率只剩 0.1%；2020 年 Q2 調整後 EBIT $28M，去年同期 $249M。現在調整後營業利益率在近年高點，低本益比可能正是對高峰盈餘的折價。二是結構：燃油零件萎縮與 OEM 自製同時發生，渦輪與熱管理分部 Q3 營收年減約 4.5%、利潤率降 50bp，PowerDrive 仍小虧，組合轉換期間整體利潤率會被稀釋。三是揭露落差：渦輪發電機的設備安裝，2026-08-05 說第三季開始，2026-10-29 改為 12 月安裝、年底試產；交期、EBIT、合約規模在 8 月法說都沒有回答。壓力測試 5 項過 3 項。過關的三項：關稅（2025 年淨成本約 $28M，利潤率仍擴張）；中國產量 −6~−8%（2026 年利潤率仍擴張）；VW 降評（BWA 對其營收占比反而由 10% 升到 13%）。不過的兩項：車市衰退（量 −10%、遞減率約 18%，EPS 約 −18~−20%）；燃油零件萎縮只能算部分通過，計為不過。動能：股價 $51.94，低於 52 週均線 $57.39、高於 104 週均線 $45.78，RSI 27.7 超賣，26 週報酬 −6.77%，不是追高情境。"},"plain":{"six":{"how_it_makes_money":"賺 OEM 車款平台合約的錢：把渦輪、可變正時（VCT）、分動箱、電機、逆變器、引擎控制模組等動力系統零件，按車型生命週期直接賣給 OEM。錢卡在 OEM 排產量與年度議價兩個節點；近兩年獲利成長靠成本控制與回購，不靠量。","moat":"→：執行力擴大、定價力縮減，份額大致跟著市場走。機制是車款平台設計導入，加上跨燃油、混動、純電的成本規模，不是定價權，評 C。","growth":"🟡：核心車市飽和，營收四年持平；五年後的跑道靠 eProduct 占比提升，以及尚未驗證的資料中心電力。共識 EPS 年增約 10.5%，一半以上靠回購。","capital":"資本配置以回購為主，紀律尚可：2026 年約七成自由現金流回饋股東，買回價位約 10 倍本益比。併購報酬與 SBC 事實表未涵蓋。","valuation":"現價只要求 EPS 維持在 2026 年的水準：以 10 倍終端倍數回推，$52.2 對應長期 EPS 約 $5.2，等於零成長。回購帶來的每年約 4–5% 成長我信；2027 年車市與高檔利潤率一定撐得住，我不信。結論是合理價，不是便宜價。","how_wrong":"🟡：最可能看錯的地方，是把循環高點的利潤率當成常態。2009 年與 2020 年都證明，量一掉，利潤會很快蒸發。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027-02 公布的 2027 年指引：有機營收不落後加權市場，且調整後 EPS 中點 ≥$5.75；或股價先跌到 $45 以下，且有機營收年減未逾 5%","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":52.2,"week26_return_pct":-6.77,"consensus_rev_3m_pct":1.54,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"調整後 EPS 2026 年指引 $5.20–5.35，GAAP $4.65–4.84，差約一成；以 GAAP 中點 4.75 計前瞻本益比約 11 倍，結論不變。2025 年 GAAP EPS 1.28 被非現金項目壓低，但同年自由現金流 $1.21B，調整後盈餘有現金支撐"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"capacity","event":"渦輪發電機北卡羅來納組裝廠安裝產線與設備，年底前開始試產","impact":"中","watch":"Q4 法說是否確認試產完成"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年全年指引","impact":"高","watch":"有機營收是否不落後加權市場、調整後 EPS 中點是否 ≥$5.75"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"管理層承諾在 2027 年初揭露渦輪發電機出貨曲線與客戶","impact":"高","watch":"是否有終端客戶合約、$300M 目標是否維持"},{"date":"2026","date_precision":null,"type":"regulatory","event":"USMCA 2026 年續約","impact":"中","watch":"是否續約、新條款是否不利於車用零件"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"微電網逆變器 UL 認證預計 2027 年初完成","impact":"低","watch":"認證是否完成、首張訂單是否落地"}],"_projected_from":"v19"}
```
