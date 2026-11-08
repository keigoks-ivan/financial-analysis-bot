你是 stock-analyst v20 的**散文層（prose）agent**，標的 CELH（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：CELH　日期：2026-11-08　archetype：None　前份裁決：2026-05-18　thesis 仍活 — Q1 26 strong beat(Rev .6M／Adj EPS .41 beat .29 by 41%)、Alani Nu integration ahead of schedule(M synergies)、21% US share(+1000bps YoY)、PepsiCo 11% 戰略持股 + 美加獨家配銷。但 CELSIUS 核心品牌 YoY 僅 +6%(從 +50%+ 大幅減速)、Q1 GM 48.3%(-400bps YoY)、Mgmt FY26 organic Rev guide 僅 +2-4% — 估值🟢(Fwd PE 18.5x／PEG 0.86／分位 <10%) + Pure MA ❌(現價跌穿三條週均)。等 W104 站回或 Q3 26 核心品牌動能回升再建倉 — 訊號 B 觀望，非 C 迴避。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1862B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（534B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（815B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1478B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（618B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（573B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（952B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2240B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4675B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2232B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1862           3597-5138      5 條（2–6 內）  
s3                  8000         534           5226-7466      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2911          8462-12089      5 條（2–6 內）  
s6                 11000         573          7299-10427      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         952           1784-2548      5 條（2–6 內）  
s10                 5000        2240           1932-2760      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2232           2000-2768      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4279B；至少需散文≈40.72KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55
−55%
−47%
−35
−35%
−13.2%
−7.0%
−7%
−6%
−2
−0.4
0
0%
0.03
0.10
0.11
0.25
0.39
0.41
0.43%
0.5
0.7%
0.7
0.86
1
1.0%
1%
01
1.01
1.08
1.25
1.277
1.29
1.3
1.30
1.35
1.4
1.40
1.42
1.50
1.5%
1.53
1.56
1.62
1.63
1.65
1.69
1.7
1.70
1.80
1.8
1.85
1.96
2
2.08
2.1
2.25
2.3
2.50
2.5
2.5056
2.52
2.72
2.73
2.8%
2.9
03
3.0
3
3%
3.01
3.2
3.32%
3.568
3.70
3.7
3.99
4
4%
4.0
4.101
4.4%
4.5
4.502
5
05
5%
5.3%
5.56
5.7%
6%
6
06
6.09%
6.6%
6.747
7%
7
07
7.006
7.6
7.8%
08
8
8%
8.1%
8.3%
8.472
9
9.1%
9.2
9.5%
9.8%
9.8
10
10%
11
11.2%
11.4
11.66
12%
12
12.86%
13
13%
14%
14
14.7%
14.84%
15%
15
15.32%
16
16.8%
16.9
17.5%
18
18.5
18.92
19
19.6
19.7%
20
20%
20.3%
20.7%
20.8
20.9%
21%
22%
22.65
23%
23.4%
24%
24
25
26
28.9
29.16%
29.4
29.4%
30%
30
30.16
31
31.75
31.85
32.11%
32.16
32.4
34
34.5
34.50
35%
35.4%
36
36.47
38.36
40%
40
40.93
41.10
41.6
42
43.2%
44%
45%
46.8%
47%
47.4%
47.95%
48%
48.04%
48.5%
49%
49
50
50%
50.39%
51%
51.3%
51.8
52%
52
55.55%
56%
57.1%
57.9%
58%
58.5%
60.57
61.3%
62.32%
64.6%
68.01
70
75
80
80.58
88.8
90
100
100%
104
150%
250
870
2025
2026
2027
2028
2031
20261108
2,000
2,500
2,592
3,450
4,500
5,000
5,120
8,030
9,100
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
{"meta":{"ticker":"CELH","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Celsius Holdings"},"oneliner":"Alani Nu 撐住組合成長，但 CELSIUS 品牌仍在衰退，毛利率 46.8% 比去年少 4.5 個百分點；現價要靠毛利率回升才划算，先等 2027 年上半年的毛利率數字。","thesis":{"H":[{"id":"H1","text":"毛利率能靠收益管理、北卡第二條產線與直接採購回升，FY2027 回到 49% 以上，FY2028 回到 50% 以上。","2y":"FY2027 毛利率 ≥49%，FY2028 ≥50%","5y":"FY2031 毛利率 50%～52%，接近管理層低 50 目標","10y":null,"threshold":"FY2027 全年毛利率 ≥49%（TTM 為 47.95%）","source":"公司 10-Q、10-K 與法說毛利率說明；鋁價與中西部溢價","drift_rule":"TTM 毛利率低於當期路徑，連 2 季差 1 個百分點以上為削弱，連 3 季差 2 個百分點以上為反轉（1 個百分點約等於 EPS 6%）。"},{"id":"H2","text":"CELSIUS 品牌在 2027 年靠新品與主力 SKU 回到成長，而且不是靠加碼促銷買來的。","2y":"2027 Q3 追蹤通路零售額年增 ≥3%","5y":"CELSIUS 美國追蹤通路份額回到 10% 以上（第三季 9.1%）","10y":null,"threshold":"2027 Q2 零售額年增 ≥0%、Q3 ≥3%，同期品牌交易投資占比不上升","source":"公司法說的掃描數據與品牌別營收","drift_rule":"連 2 季低於門檻 5 個百分點以上為削弱，連 3 季低於門檻 10 個百分點以上為反轉。"},{"id":"H3","text":"Alani Nu 在直送與海外擴張帶動下維持高成長，零售與帳面落差在 2027 年第二季後收斂，海外占比朝 15% 前進。","2y":"FY2027 Alani Nu 淨銷售年增 ≥15%；2027 Q2 起零售與帳面落差縮到 15 個百分點內","5y":"2031 年海外營收占比超過 15%（管理層目標）；組合美國份額 ≥22%","10y":null,"threshold":"FY2027 Alani Nu 淨銷售年增 ≥15%","source":"公司季報品牌別營收、法說橋接表","drift_rule":"連 2 季低於門檻 5 個百分點以上為削弱，連 3 季低於門檻 10 個百分點以上為反轉。"}],"R":[{"id":"R1","text":"毛利率回不來：鋁與柴油居高、公司未避險、轉嫁受競爭限制，直送組合持續拉高交易投資，關稅影響也難估。","h_ref":"H1","clock":"🔥","threshold":"2027 上半年毛利率低於 48%","evidence_refs":["channel_business_model_shift#2","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#1","supply_demand_durability#3"]},{"id":"R2","text":"CELSIUS 份額持續流失：2025 Q3 已年減 0.5 點至 11.2%，2026 Q3 再降至 9.1%，新品若補不上，SKU 精簡的說法就站不住。","h_ref":"H2","clock":"⚡","threshold":"2027 Q2 追蹤通路零售額年增低於 0%","evidence_refs":["competitive_share_entrants#3"]},{"id":"R3","text":"Alani Nu 成長依賴限定款，CFO 已預告第四季有促銷時點、整合與大客戶現金管理雜訊；高基期出現後帳面可能快速降速。","h_ref":"H3","clock":"⚡","threshold":"Alani Nu 淨銷售年增連 2 季低於 10%","evidence_refs":["end_markets#2"]},{"id":"R4","text":"Pepsi 集中度：2025 年占營收 43.2%，2026 前九月 61.3%，第三季 64.6%。Pepsi 調整配銷條款或策略，公司幾乎沒有替代方案。前份的未成年購買立法風險也保留在此。","h_ref":"H1+H3","clock":"🐢","threshold":"Pepsi 公開重新評估配銷條款，或任一州通過 18 歲以上才可購買能量飲的法案（現況事實表未涵蓋）","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R5","text":"品類放緩與 GLP-1：Statista 預估全球成長 2027 年降至約 3.32%，AlixPartners 模型估 GLP-1 使能量飲與咖啡約 4% 年化下滑；研調之間差距大，只列慢變數。","h_ref":"H2+H3","clock":"🐢","threshold":"組合零售額年增連 4 季低於 5%","evidence_refs":["supply_demand_durability#2","substitute_technology#2"]},{"id":"R6","text":"未決訴訟：證券、衍生、channel stuffing 與虛假廣告集體訴訟，以及每箱 10 美分的版稅訴訟，律所也在調查證券詐欺主張；金額與時點事實表未涵蓋，無法估算。","h_ref":"H1","clock":"🐢","threshold":"集體訴訟獲認證且和解或判賠達 5,000 萬美元（約基準 FY2027 淨利 12%）","evidence_refs":["major_events#0","lawsuit_class_action#0","lawsuit_class_action#1","lawsuit_class_action#2"]},{"id":"R7","text":"供應鏈：不完全自有工廠，專用罐供應商少，且供應鏈主管職位目前由代理人選擔任，銜接期出錯會直接反映在毛利率與缺貨。","h_ref":"H1","clock":"🔥","threshold":"任一季因鋁罐短缺或代工中斷使毛利率單季下滑 1 個百分點以上","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"FY2027 全年毛利率低於 48%（2028 年 2～3 月年報揭露），即 TTM 47.95% 沒有改善。","why_fatal":"這是數學上最大的單一敏感度：以 FY2027 共識營收 34.5 億美元算，毛利率每差 1 個百分點，稅前少 3,450 萬美元，約等於 EPS 0.10～0.11 美元（稅率假設 23%，事實表未涵蓋；股數 2.5056 億），約為共識 1.70 的 6%；同樣影響約要 CELSIUS 品牌營收差 7%（貢獻率假設 35%）。","if_happens":"基準路徑失效，情境落到空方，FY2031 EPS 看 1.40 附近；未持有則不建倉，已持有則清倉。","how_monitor":"每季毛利率與交易投資占總銷售比；鋁價、中西部溢價與柴油；2027 年上半年先看是否達 48.5% 以上。","probability":"約 30%（12～24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":18.92,"peg_fy2":1.08,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":0.25,"FY2026E":1.42,"FY2027E":1.7,"FY2028E":1.96},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識（2026-11-07），研判為調整後口徑（第三季調整後 EPS 0.41，與全年 1.42 量級一致），家數事實表未涵蓋。FY2025A 0.25 為 GAAP 稀釋 EPS，FY2025 調整後 EPS 事實表未涵蓋，兩者口徑不同，不得用來算三年 CAGR；本次成長率只用 FY2026E→FY2028E 年複合 17.5%。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/scenario.json","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"併購整合剛完成，原主力品牌衰退待修復，獲利成長取決於毛利率回升"},"industry":{"clock_phase":"II","sd_verdict_source":"需求結構性持久、供給可逆性高：組合零售額第三季年增 14.7%，管理層稱能量飲仍是飲料最強品類；代工外包使新品牌進入成本低，Statista 預估全球成長到 2027 年放慢至約 3.32%。","bargaining":{"up":"鋁罐與柴油成本上升時轉嫁受競爭限制，公司未避險；12 盎司專用罐供應商少。","down":"Pepsi 占第三季營收 64.6%，公司議價位置弱，轉換配銷安排的彈性受限。","geo":"生產以北美代工與自有北卡產線為主，關稅主要經由鋁進入成本。"},"profit_pool_dir":"事實表未涵蓋五年營業利益池；僅知 CELH TTM 營益率 17.5%，低於 MNST 的 29.16%。","tam_table":[{"item":"海外重點市場即飲能量飲","value":"超過 80 億美元，管理層預期明年雙位數成長（2026-11-05 法說）"},{"item":"美國追蹤通路組合份額","value":"約 20.7%（2026 Q3），Q1 為 20.9%"},{"item":"全球能量與運動飲料成長","value":"Statista 預估 2027 年約 3.32%，各研調 CAGR 5.7%～7.8%，差異大"},{"item":"TAM、SAM、滲透率、營業利益池五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"品牌心智加 Pepsi 直送帶來的貨架與冷櫃覆蓋；沒有轉換成本，要靠持續新品與配銷維持。","execution":6,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面穩定：組合份額 Q1 20.9%、Q3 20.7%，Alani Nu 9.8%，CELSIUS 9.1%（2025 Q3 為 11.2%）。定價面縮減：毛利率 46.8% 對 51.3%，定價跟隨品類領導者。合併判→而不是↓，因為份額仍守住、毛利率下滑有一部分是鋁與柴油的週期因素。","peer_na_reason":"同業 ROIC 事實表未涵蓋，以份額與毛利率、營益率差距替代；利潤率只有單一期間，看不出差距擴大或收窄。","threats":[{"level":"🟡","text":"自有品牌與低價新品進場，Costco Kirkland 能量飲 2026 年 3 月底上市；CELSIUS 量販通路第三季已偏弱，點對點壓力最先出現在這裡。","p":"30%","evidence_refs":["substitute_technology#1","competitive_share_entrants#0"]},{"level":"🟡","text":"新進者與激進定價對手增加，CEO 在 2026-08-06 法說提到品類競爭者比以往更多；公司自述這會顯著衝擊份額與獲利。","p":"35%","evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者是同一人，第三季組合零售額年增 14.7%；但能量飲是想要而非需要，Witch's Brew 單一限定款貢獻超過 1.3 億美元零售額，顯示成長有一部分靠新鮮感。"},{"item":"決策層級","level":"🔴","text":"消費者在冷櫃前每次都能換牌，沒有轉換成本；CELSIUS 精簡 SKU 又暫停新品後，份額一年掉 2.1 點，可見少了貨架與新品就流失。回購率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🔴","text":"Pepsi 占第三季營收 64.6%（去年同期 35.4%）；直送比重上升拉高交易投資，Alani Nu 零售額 +58%、淨銷售只有 +24%，價值有一部分留在配銷與促銷環節。"},{"item":"社會容忍度","level":"🟡","text":"目前未見針對未成年購買的已生效限制，但有虛假廣告集體訴訟，前份列出的州級 18 歲購買立法進度事實表未涵蓋，列為資料缺口。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"投入資本、折舊攤銷與收購對價都未涵蓋，當期 ROIC 象限、增量 ROIC、再投資率均不估算，不以記憶補數字。"},"combined":5.5,"score":5.5,"spread_table":[{"metric":"毛利率","CELH":47.95,"KO":62.32,"PEP":54.17,"MNST":55.55,"KDP":48.04,"unit":"%"},{"metric":"營業利益率","CELH":17.5,"KO":32.11,"PEP":15.32,"MNST":29.16,"KDP":14.84,"unit":"%"},{"metric":"FCF 利潤率","CELH":6.09,"KO":27.97,"PEP":10.66,"MNST":22.58,"KDP":9.11,"unit":"%"}],"competitors":[{"name":"KO","gm":62.32,"om":32.11,"fcf_margin":27.97,"strategy_note":"TTM 毛利率 62.32%、營益率 32.11%，利潤率在另一個層級，只當上限參考；能量飲份額事實表未涵蓋。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PEP","gm":54.17,"om":15.32,"fcf_margin":10.66,"strategy_note":"既是最大客戶與配銷商，也是策略股東；TTM 營益率 15.32% 低於 CELH，談判時有壓低配銷條件的動機。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"MNST","gm":55.55,"om":29.16,"fcf_margin":22.58,"strategy_note":"最直接的能量飲對手，TTM 毛利率 55.55%、營益率 29.16%（資料到 2026-06），是 CELH 毛利率回升論點的上限參照。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"KDP","gm":48.04,"om":14.84,"fcf_margin":9.11,"strategy_note":"毛利率 48.04% 與 CELH 接近、營益率 14.84%，可作為毛利率停在 48% 時飲料公司能賺多少的參照。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"2026 年成長主要來自併購併表；FY2027 共識營收 +8.3% 靠量與新品，EPS +19.7% 另靠毛利率回升與回購。","runway_years":"無法計算：組合份額近三季未上升，以現有趨勢到不了 30%；品類滲透率事實表未涵蓋。","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊攤銷與收購對價未涵蓋，內生天花板留空；共識 EPS 年複合 17.5% 高於營收成長 8.3%，缺口 9.2 個百分點歸因於毛利率回升與淨回購。無法證明在天花板內，情境按超出處理，空方機率取 30%。","segments":[{"item":"Alani Nu","value":"第三季淨銷售 4.101 億美元，年增約 24%；追蹤通路零售額 +57.9%，份額 9.8%"},{"item":"CELSIUS","value":"第三季淨銷售 3.568 億美元，年減約 6%；零售額 −7.0%，份額 9.1%"},{"item":"Rockstar","value":"第三季淨銷售 8,030 萬美元；零售額 −13.2%，保留 SKU 較去年少約 1%"},{"item":"海外","value":"第三季年增約 56%，管理層目標五年內占營收 15% 以上；目前金額事實表未涵蓋"}],"decay_signals":[{"signal":"毛利率連續年減","lit":true,"evidence":"Q1 年減 4.0、Q3 年減 4.5 個百分點；Q2 去年同期值未涵蓋，以 TTM 47.95% 低於 FY2025 的 50.39% 佐證。"},{"signal":"主力品牌市占近 12 個月縮減","lit":true,"evidence":"CELSIUS 美元份額由 11.2% 降至 9.1%。"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"共識 EPS 年複合 17.5%，FY2027 營收成長 8.3%，差 9.2 個百分點。"}],"trap_rating":"🔴"},"quality":{},"governance":{"capital_returns":[{"item":"2026 年前三季回購","value":"約 1.69 億美元，第三季約 4,500 萬，授權餘額約 9,100 萬（2026-11-05 CFO）"},{"item":"併購","value":"Alani Nu、Rockstar 整合已完成；對價與已實現報酬事實表未涵蓋"},{"item":"股息","value":"普通股股息事實表未涵蓋，情境以 0 計"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"營業利益由 FY2024 約 1.56 億增至 TTM 約 5.56 億美元，但收購對價與投入資本事實表未涵蓋，算不出已實現增量報酬。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"現價對 FY2026E EPS 殖利率 4.4%、FY2027E 5.3%；回購均價與 10 年期殖利率事實表未涵蓋，無法比較。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"第三季 870 萬美元 × 4 ÷ 市值 80.58 億＝0.43%，低於每年 1.5%；以金額占市值代替淨稀釋率。","grade":"過"}]},"valuation":{"basis":"Fwd P/E，分母為 FY2026E 共識 EPS 1.42，輔以 FY2027E 倍數與 PEG。","tier":"品牌飲料，中型成長","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業 Fwd P/E 或 EV/S；倍數對照承重但無資料，不自行補值。"},"fwd_pe":22.65,"peg":1.29,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 倍數 22.65 ÷ EPS 年複合 17.5%＝PEG 1.29，FY2 倍數 18.92 對應 1.08，落在 1～2 的合理區；EV 對 FY1 營收 2.52 倍。Trailing P/E、P/S、EV/S 雖低於僅有的 3～4 個年度端點，但端點少且含高成長期，不能當便宜證據；五年連續分位與同業倍數事實表未涵蓋。","upside_short_pct":0.7,"upside_mid_pct":29.4},"trap_analysis":{"verdict":"🔴","label":"衰退訊號三項亮燈，要靠毛利率回升才解除"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"CELSIUS 零售額 −7%，管理層把回升時點推到 2027 年；毛利率 46.8%，低 50 目標延後；Alani Nu 第三季靠限定款 Witch's Brew 貢獻超過 1.3 億美元零售額。","assumption":"新品能把 CELSIUS 拉回成長，收益管理能補回直送組合與鋁價的壓力。","consequence":"五年後虧五成最可能的路徑：CELSIUS 持續失血、Alani Nu 限定款效應退潮、毛利率停在 45%～47%，EPS 1.25～1.40、倍數 13 倍左右，股價約 16～18 美元，虧 44%～49%。","ruling":"採納為主要下行路徑，空方機率 30%；與唯一致命點的毛利率部分重疊，CELSIUS 衰退另以觸發器監測。","watch":"每季毛利率、CELSIUS 零售額年增率、Alani Nu 剔除限定款後的零售額年增率。","evidence_refs":["channel_business_model_shift#2","competitive_share_entrants#3"],"fact_refs":["f_kpi6_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"Alani Nu 零售額 +58%，淨銷售只有 +24%；Pepsi 占第三季營收 64.6%，去年同期 35.4%；直送比重上升推高交易投資。","assumption":"組合成長的價值會留在公司，而不是被配銷端與促銷分走。","consequence":"營收與份額都達標，但毛利率停在 48% 左右，EPS 增速追不上共識，倍數無法維持。","ruling":"部分採納。CFO 說 2027 年第二季起落差最乾淨，屆時可驗證；在此之前不把零售額成長當作股東經濟改善的證據。","watch":"2027 Q2 Alani Nu 零售額與淨銷售的落差、交易投資占總銷售比。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"],"fact_refs":["f_kpi0_revenue_gaap"]},{"view":"價格已反映太多","evidence":"FY2026 共識 EPS 由約 1.63 降到 1.42，股價反而由 30.16 漲到 32.16；財報後共識快照修正 0%，第四季放緩可能尚未納入。","assumption":"FY2027 EPS 1.70 站得住，22.65 倍的 FY1 倍數合理。","consequence":"若 FY2027 共識下修 10% 到 1.53，以 FY2 倍數 18.92 倍算約 28.9 美元，較現價低 10%。","ruling":"部分採納。倍數不貴但沒有折扣，下修風險大於上修風險，這也是不追的原因之一。","watch":"2027 年 3 月前 FY2027 共識 EPS。","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 30.16 → 本次 32.16（+6.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=30.16","side_b":"本次 price_at_dd=32.16","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 30.16 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 30.16 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 30.16 美元：Bull 價 88.8、Bear 價 19.6，五年期望值 +57.1%，基準年化 9.5%，不對稱比 3.7","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.7。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 30.16 美元：五年期望值 +57.1%，基準年化 9.5%，不對稱比 3.7","side_b":"本次情境、股價 32.16 美元：五年期望值 +47.4%，基準年化 8.1%，不對稱比 3.01","ruling":"再換股價、情境不動：起點價上漲 6.6%，五年期望值少 9.8 個百分點，基準年化少 1.4 個百分點，不對稱比由 3.7 降到 3.01。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論由偏便宜轉為合理","cause":"新證據","prior_field":["val"],"side_a":"2026-05-18：Fwd P/E 18.5 倍、PEG 0.86，評為便宜。","side_b":"2026-11-08：Fwd P/E 22.65 倍、PEG 1.29，評為合理。","ruling":"採 B 側。股價只漲 6.6%（30.16→32.16），倍數上升大部分來自 FY2026 共識 EPS 下修約 13%（前份 18.5 倍回推約 1.63，現為 1.42）。","evidence_level":"財報與共識快照；前份共識為回推值。","settle_metric":"FY2027 共識 EPS","if_then":["若第四季財報後 FY2027 共識低於 1.50，則不追，且估值結論不因股價下跌而上調。","若 FY2027 共識維持 1.70 以上且毛利率達 49%，則重跑研究。"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"]},{"axis":"結論維持觀望，但陷阱風險升高","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：觀望，陷阱風險中等，前提是 CELSIUS 2027 年恢復 10% 以上成長。","side_b":"本次：仍觀望，衰退訊號亮三項：毛利率連續年減、CELSIUS 份額 11.2%→9.1%、EPS 成長高於營收成長 9.2 個百分點。","ruling":"採 B 側。Alani Nu 與前三季現金流讓論點還活著，所以不改成放棄；但陷阱風險由中等升為高。","evidence_level":"公司財報、10-Q 與法說。","settle_metric":"FY2027 上半年毛利率","if_then":["若 2027 年第一或第二季毛利率達 49% 以上，則重跑研究。","若 FY2027 全年毛利率低於 48%，則清倉，未持有則不建倉。"],"evidence_refs":["channel_business_model_shift#2","competitive_share_entrants#3"]},{"axis":"前份空值欄位首次填寫","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位未填（null）。","side_b":"本次首次填寫：護城河方向→、五年後跑道中等、公司類型為轉機與特殊情境、情境機率 20／50／30、最大回撤 −35%～−55%；週期位置不適用，維持空值。","ruling":"前份沒有可比值，不算結論改變。","evidence_level":"格式差異","settle_metric":null,"if_then":[]},{"axis":"重新建倉條件改為毛利率事件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 W104 站回或 Q3 26 核心品牌動能回升再建倉","side_b":"2027 年第一或第二季毛利率達 49% 以上，且非一次性因素；達成後重跑研究，不直接建倉。","ruling":"舊條件的品牌動能部分已落空（第三季零售額 −7%），均線條件與基本面無關。毛利率是 EPS 敏感度最大的單一項，所以建倉條件改綁毛利率，不設進場價。","evidence_level":"公司財報與法說","settle_metric":"單季毛利率","if_then":["若股價先站上 104 週均線 38.36 而毛利率未回升，則不追。","若股價下跌但毛利率達到 49%，則重跑研究，通過後分批反買。"]},{"axis":"Single Thing 由未設定改為 FY2027 毛利率","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（null）。","side_b":"FY2027 全年毛利率低於 48%（2028 年 2～3 月年報揭露），即 TTM 47.95% 沒有改善。","ruling":"Single Thing 首次設定。選毛利率而不選 Pepsi 終止合約，因為後者雖然最戲劇化，但 12～24 個月機率低；毛利率每 1 個百分點約影響 EPS 6%，是敏感度最大的單一項。","evidence_level":"以 FY2027 共識營收推算，稅率為假設值。","settle_metric":"FY2027 全年毛利率","if_then":["若 FY2027 毛利率低於 48%，則清倉。","若 FY2027 毛利率達 49% 以上，則解除此項風險並重估基準情境。"]},{"axis":"清倉與減碼門檻首次設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（null）。","side_b":"FY2027 毛利率低於 48% 清倉；組合份額連兩季低於 20% 清倉；CELSIUS 零售額 2027 Q2、Q3 皆為負則減碼一半；FY2027 共識 EPS 低於 1.50 減碼一半。","ruling":"前份只有文字警戒，本次改成可量測的門檻。","evidence_level":"格式差異","settle_metric":null,"if_then":[]},{"axis":"前份假設驗證點已失效","cause":"新證據","prior_field":null,"side_a":"前份：Q4 26 CELSIUS 年增重回 10% 以上；2027 年 CELSIUS 年增 ≥10%；Alani Nu 2027 年增 ≥40%；FY26 共識 EPS 上修至約 1.80 以上（前份摘要數字缺首位，依 18.5 倍回推）。","side_b":"第三季 CELSIUS 零售額 −7%，管理層把回升時點推到 2027 年；FY26 共識降到 1.42；Alani Nu 帳面年增約 24%。","ruling":"前份 CELSIUS 與共識上修的門檻已實質失敗，本次重設，不沿用；Alani Nu 零售額達標但帳面未達，改用淨銷售驗證。","evidence_level":"公司財報、法說與共識快照","settle_metric":"CELSIUS 零售額年增率與 Alani Nu 淨銷售年增率","if_then":["若 2027 Q2 CELSIUS 零售額仍為負，則停止加碼。","若 2027 Q3 達 3% 以上，則恢復對該假設的信心並重跑研究。"]},{"axis":"CELSIUS 回到成長的時點","cause":"新證據","prior_field":null,"side_a":"2026-08-06 CEO：第三季與第二季相近，年底前回到成長，第四季是緩慢累積。","side_b":"2026-11-05 CEO：消費轉折要到 2027 年循環過 SKU 精簡後才出現；年底只談週銷維持在 5,000 萬美元區間時部分週次可小幅成長或持平。","ruling":"屬程度差異，可調和。採 B 側時點，驗證點放在 2027 Q2～Q3。管理層把衰退歸因於 SKU 精簡與高基期，列為未證；若 2027 Q2 仍負成長，視為歸因不成立。","evidence_level":"法說原話","settle_metric":"CELSIUS 追蹤通路週銷金額與年增率","if_then":["若 2027 Q2 零售額年增為負，則停止加碼。","若 2027 Q2、Q3 皆為負，則減碼一半。"]},{"axis":"毛利率恢復時程","cause":"新證據","prior_field":null,"side_a":"前份摘要：管理層指引 2026 下半年回到 low 50s。","side_b":"2026-11-05 CFO：全年維持 high 40s，低 50 目標要比一年前預期更久，商品成本沒有改善。","ruling":"採 B 側，管理層已退讓。鋁與柴油、直送組合、整合成本的各自占比拆不開，所以看結果不看歸因。","evidence_level":"法說原話與 10-Q","settle_metric":"單季毛利率、交易投資占總銷售比","if_then":["若 2027 上半年毛利率低於 48%，則不追並下修基準 EPS。","若達 49% 以上，則重跑研究。"],"evidence_refs":["channel_business_model_shift#2"]},{"axis":"Alani Nu 零售成長與帳面落差","cause":"新證據","prior_field":null,"side_a":"第三季零售額 +58%，剔除限定款仍 +50%。","side_b":"淨銷售 +24%，原始落差約 34 個百分點；CFO 說扣除非即飲與合約攤銷後約 24～25 個百分點。","ruling":"可調和，一部分是轉換直送的暫時因素，一部分是交易投資的長期成本；2027 年第二季前無法裁決。","evidence_level":"法說原話","settle_metric":"2027 Q2 零售額與淨銷售年增率落差","if_then":["若 2027 Q2 落差仍大於 15 個百分點，則視為結構性，下修基準毛利率。","若縮到 15 個百分點內，則支持基準情境。"]},{"axis":"回購承諾的步調","cause":"新證據","prior_field":null,"side_a":"2026-08-06 CFO：打算今年用完 3 億美元授權。","side_b":"2026-11-05：第三季只買約 4,500 萬美元（第二季約 1 億），授權餘額約 9,100 萬。","ruling":"尚未違約，但步調放慢，要第四季買滿才算兌現。回購均價未涵蓋，無法評斷買得好不好。","evidence_level":"法說原話","settle_metric":"第四季回購金額","if_then":["若第四季回購低於 9,100 萬美元，則把承諾記為未兌現，基準 EPS 不再上調回購效果。"]},{"axis":"賣方目標價與本次結論","cause":"新證據","prior_field":null,"side_a":"賣方平均目標價 41.10～60.57 美元，各站最高 75、最低 26。","side_b":"本次 12 個月基準約 32.4 美元。","ruling":"本次比賣方悲觀。差異在成長基準：賣方模型仍放 FY2027 EPS 1.70，需要毛利率回升與第四季放緩不影響 2027 年。目標價來源日期不一，全距 75 對 26 為 2.9 倍，超過 2.5 倍，因此不引用為支持，也調低自身機率信心。","evidence_level":"二手聚合站，日期不一致","settle_metric":"第四季財報後目標價與共識修正","if_then":["若財報後共識 FY2027 上修且毛利率達標，則承認判斷過於保守並重跑研究。"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"]},{"axis":"現在就買的最強論證","cause":"新證據","prior_field":null,"side_a":"Alani Nu 零售額剔除限定款仍 +50%，整合已完成，2027 新品與收益管理同時啟動；淨現金、前三季 FCF 3.99 億美元，FY2027 倍數 18.92 倍，第四季雜訊可能是最後低點。","side_b":"毛利率尚未回升，共識未反映第四季放緩，CELSIUS 仍衰退，FCF 可能受終止費補償影響，股價低於三條週均線。","ruling":"不買。買方論點成立的關鍵是毛利率，毛利率數據 2027 年上半年就會出來，等待成本低於先買後看錯的成本。","evidence_level":"公司財報與法說","settle_metric":"2027 上半年毛利率","if_then":["若毛利率達 49% 以上，則重跑研究，通過後分批反買。","若股價先漲而毛利率未回升，則不追。"]}],"triggers":[{"n":1,"text":"FY2027 全年毛利率低於 48%","type":"Single Thing","maps_to":"R1","metric":"FY2027 全年毛利率","threshold":"低於 48%","action":"清倉；未持有則不建倉","source_freq":"10-K，每年一次","date":"2028-03"},{"n":2,"text":"2027 年第一或第二季毛利率達 49% 以上，重跑研究","type":"估值rearm","maps_to":"H1","metric":"單季毛利率","threshold":"≥49%","action":"重跑研究，通過後分批反買，首筆不超過正常倉位三分之一","source_freq":"10-Q，每季","date":"2027-08"},{"n":3,"text":"CELSIUS 追蹤通路零售額 2027 Q2 轉正","type":"假設驗證","maps_to":"H2","metric":"CELSIUS 零售額年增率","threshold":"2027 Q2 ≥0%，Q3 ≥3%","action":"未達則停止加碼；連兩季為負則減碼一半","source_freq":"法說與新聞稿，每季","date":"2027-08"},{"n":4,"text":"Alani Nu 淨銷售年增連兩季低於 10%","type":"風險","maps_to":"R3","metric":"Alani Nu 淨銷售年增率","threshold":"連兩季低於 10%","action":"減碼一半","source_freq":"新聞稿，每季","date":"2027-11","evidence_refs":["end_markets#2"]},{"n":5,"text":"FY2027 共識 EPS 跌破 1.50 美元","type":"減碼","maps_to":"R1","metric":"FY2027 共識 EPS","threshold":"低於 1.50","action":"減碼一半；未持有則不追","source_freq":"共識快照，每月","date":"2027-03","evidence_refs":["capital_markets_pricing#0"]},{"n":6,"text":"Pepsi 配銷合約不利修訂或終止","type":"風險","maps_to":"R4","metric":"Pepsi 合約條款","threshold":"公告不利修約或終止","action":"清倉","source_freq":"8-K，事件發生時","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":7,"text":"集體訴訟獲認證且不利和解","type":"風險","maps_to":"R6","metric":"訴訟進度與金額","threshold":"獲認證且和解或判賠達 5,000 萬美元","action":"減碼一半","source_freq":"10-Q 法律程序章節，每季","date":null,"evidence_refs":["lawsuit_class_action#0"]},{"n":8,"text":"第四季財報全面複審","type":"複審日期","maps_to":"H1","metric":"第四季帳面營收年增、毛利率、2027 年展望","threshold":"全面複審","action":"重看共識修正與情境機率；股價先漲而毛利率未回升則不追","source_freq":"8-K 新聞稿與法說","date":"2027-03","evidence_refs":["end_markets#2"]},{"n":9,"text":"組合美元份額連兩季低於 20%","type":"清倉","maps_to":"H3","metric":"美國追蹤通路組合份額","threshold":"連兩季低於 20%","action":"改判護城河轉弱，清倉","source_freq":"法說與新聞稿，每季","date":"2027-11"}],"kill_metrics":[{"metric":"FY2027 全年毛利率","bear_threshold":"低於 48% 清倉","window":"2028 年 3 月前年報揭露","source":"公司 10-K 與財報新聞稿","last_status":"warning"},{"metric":"CELSIUS 品牌追蹤通路零售額年增率","bear_threshold":"2027 Q2 與 Q3 皆低於 0% 減碼一半","window":"2027 年 8 月至 11 月財報","source":"公司法說引述掃描數據","last_status":"warning"},{"metric":"Alani Nu 淨銷售年增率","bear_threshold":"連兩季低於 10% 減碼一半","window":"2027 年每季","source":"公司新聞稿品牌別營收","last_status":"ok"},{"metric":"美國追蹤通路組合美元份額","bear_threshold":"連兩季低於 20% 清倉","window":"2027 年每季","source":"公司法說與新聞稿引述追蹤通路數據","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"低於 1.50 美元減碼一半","window":"2027 年 3 月前","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"Pepsi 配銷合約","bear_threshold":"公告不利修約或終止則清倉","window":"持續","source":"SEC 8-K Item 1.01","last_status":"ok"}],"evidence_dismissed":[{"ref":"reg_tariff_export#2","reason":"這是 10-K 的通用風險因子，原文沒有任何已發生的出口管制、受影響市場或金額，事實表也沒有海外營收金額可衡量曝險，無法形成可監測的論點。"},{"ref":"regulatory_antitrust#1","reason":"原文是條件句的風險揭露，未載任何 FTC 或州政府已立案的案件；已知的虛假廣告集體訴訟已另列法律風險，不重複計算。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"未達重啟條件前不建倉；達成後上限 3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-0.4, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027 年第一或第二季毛利率達 49% 以上，不設進場價；股價先漲而毛利率未回升則不追。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"2027 年第一或第二季毛利率達 49% 以上且非一次性因素；達成後重跑研究，不直接建倉","exec_line":"目前不建倉。毛利率條件達成後重跑研究，通過才分批買進，首筆不超過正常倉位三分之一；若已持有，第四季財報前不加碼，FY2027 毛利率低於 48% 清倉。"},"reasoning":{"industry":"第三季營收 8.472 億美元，年增 16.8%；Alani Nu 4.101 億（約 +24%）、CELSIUS 3.568 億（約 −6%）、Rockstar 8,030 萬（占 9.5%）。毛利率 46.8%、GAAP 營益率 20.3%、調整後 EBITDA 率 23.4%。單點依賴屬集中度風險，不是護城河證據：Pepsi 占第三季營收 64.6%（去年同期 35.4%）、前九月應收帳款 58.5%，10-K 也寫明 Pepsi 能影響公司的策略決定。產業在擴張期，依據是組合零售額年增 14.7%、份額守在約 21%，管理層稱能量飲仍是飲料裡最強的品類；但全球預測顯示成長逐年放慢。需求結構性持久，供給可逆性高，因為代工外包、新品牌進入成本低。產業態勢判為雙向拉鋸：Alani Nu 帶新客進品類（份額 9.8%，年增近 3 點），同時 CELSIUS 份額由 11.2% 掉到 9.1%，Kirkland 自有品牌也在 2026 年 3 月底進場。第三季帳面含 2,000～2,500 萬美元由第四季提前的出貨，以 46.8% 毛利率換算約貢獻 0.03 美元 EPS（稅率假設 23%，未計額外費用）。","moat":"機制是品牌心智加 Pepsi 直送的貨架與冷櫃覆蓋，沒有轉換成本。同業 ROIC 事實表未涵蓋，改用份額與利潤率比較。份額：組合 2026 Q1 20.9%、Q3 20.7%，Alani Nu 年增近 3 點，CELSIUS 由 11.2% 掉到 9.1%。利潤率：TTM 毛利率 47.95%，比 MNST 低 7.6 個百分點，營益率 17.5% 比 MNST 低 11.66 個百分點（MNST 資料到 2026-06）。執行面給 6 分：整合如期完成、Alani Nu 創紀錄，但 2026 年 SKU 砍過頭是管理層自己承認的失誤（2026-08-06 CEO）。定價面給 5 分：CFO 說定價跟隨品類領導者，毛利率 46.8% 比去年少 4.5 個百分點，交易投資占比第三季仍較第二季上升。方向判→的反例是毛利率下滑若屬結構性，就應判↓；目前拆不開鋁、柴油與直送組合各占多少，所以改判條件寫死：組合份額連兩季低於 20%，或 FY2027 毛利率低於 48%。當期 ROIC、增量 ROIC、再投資率都因投入資本未涵蓋而無法計算；四個持續期檢查點有兩個紅燈，集中在消費者換牌零成本與價值被配銷端分走。","growth":"FY2026E 營收 31.85 億美元、FY2027E 34.50 億（+8.3%）；EPS FY2026E→FY2028E 年複合 17.5%（1.42→1.96）。兩者差 9.2 個百分點，歸因於毛利率回升與淨回購（前三季回購 1.69 億美元，年化約市值 2.8%），不靠收購，也不依賴倍數上升。內生天花板因投入資本未涵蓋而算不出，情境按超出處理。跑道判中等：組合份額 21% 低於 35%，但近三季沒有上升（20.9%→20.7%），以現有趨勢到不了 30%；海外第三季年增約 56%、管理層目標五年內占營收 15% 以上，是有來源的第二曲線，但目前金額未涵蓋，還沒有實績可驗。要升為寬，需要海外占營收達 10% 且組合份額達 22%。","governance":"股權激勵第三季 870 萬美元，占營收 1.0%，年化約市值 0.43%。前三季 FCF 3.99 億美元（營業現金流 4.502 億減資本支出 5,120 萬），第三季 1.277 億。TTM FCF 利潤率只有 6.09%，低於 FY2025 的 12.86%；用 TTM 營收約 31.75 億回推，2025 年第四季 FCF 約為 −2 億美元，很可能與配銷商終止費的收付時點有關，事實表未拆分。FCF 對淨利 FY2024 約 1.65 倍、FY2025 約 3.0 倍，但 FY2025 淨利偏低，這個比率不能當現金品質變好的證據。前三季現金去向：資本支出 5,120 萬、回購約 1.69 億，近 12 個月無併購完成，還債金額未涵蓋。淨現金 2,592 萬美元（含租賃的總債務 6.747 億、現金 7.006 億）。","valuation":"32.16 ÷ FY2026E 1.42＝22.65 倍；÷ FY2027E 1.70＝18.92 倍。共識 EPS 年複合 17.5%，PEG 1.29。要拿到年化 10%，五年後股價要 51.8 美元，以 19 倍算 FY2031 EPS 要 2.73，年複合約 14%；我的基準只有 12%，基準年化約 8%。12 個月：1.62 × 20 倍＝32.4 美元（+0.7%）；36 個月：2.08 × 20 倍＝41.6 美元（+29.4%）。股價低於 52、104、250 週均線（36.47、38.36、40.93），RSI 68.01，四週漲幅事實表未涵蓋。財報後的共識快照 FY1～FY3 修正都是 0%，很可能還沒納入第四季放緩，這是尚未反映的利空，在第一個確認數據出來前不加碼。","premortem":"亮燈三項：毛利率連續年減、CELSIUS 份額近 12 個月由 11.2% 掉到 9.1%、共識 EPS 成長比營收成長高 9.2 個百分點。反例是組合份額仍在 20.7%、前三季 FCF 3.99 億美元、資產負債表為淨現金，這不是典型的現金流衰退型陷阱；但三項都是基本面亮燈，不因此減計。歷史最大回撤與訴訟金額事實表未涵蓋。2026-08-06 法說迴避的第四季回升幅度與費用雜訊何時消退，2026-11-05 只部分補上，CELSIUS 回升仍未給幅度。"},"plain":{"six":{"how_it_makes_money":"賺美國便利商店與量販通路能量飲消費者的錢，錢卡在 Pepsi 這個配銷節點：第三季 64.6% 營收來自 Pepsi，Alani Nu 的零售成長只有一部分變成公司淨營收。","moat":"護城河大致穩定，方向為→：組合份額守在約 21%，但這是 Alani Nu 補上 CELSIUS 的流失，定價能力仍在下滑。","growth":"五年後的成長跑道屬中等：組合份額還有空間，但近三季沒有上升，海外第二曲線目前只有管理層目標與高增速，金額未經驗證。","capital":"資本配置還不能評高分：股權激勵幾乎沒有稀釋，但併購與回購的報酬無法用現有資料驗證。","valuation":"現價 32.16 美元要求 2027～2028 年毛利率回升、EPS 年複合約 17.5%；我只相信一部分，基準 FY2027 EPS 1.62 低於共識 1.70，倍數合理但沒有折扣。","how_wrong":"最可能看錯的是把 Alani Nu 的強勢當成整個組合的體質，以及把毛利率下滑全歸給鋁價；衰退訊號亮三項，陷阱風險高。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年第一或第二季毛利率達 49% 以上，不設進場價；股價先漲而毛利率未回升則不追。","trap":"🔴","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"轉機/特殊情境","price_at_dd":32.16,"week26_return_pct":-0.4,"consensus_rev_3m_pct":-1.39,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY1 分母已有九個月實績，第三季調整後 EPS 0.41 與 GAAP 0.39 差距小，爭點在 FY2、FY3。市值與 EV 未含可轉換工具的完整稀釋，本次不以 EV 倍數作為承重依據。"},"catalysts":[{"date":"2026-11-30","date_precision":"month","type":"product","event":"兩款 CELSIUS 新 SKU 於感恩節前後上架，Alani Nu 冬季限定款 11 月底上市","impact":"中","watch":"限定款零售額與 CELSIUS 週銷是否維持 5,000 萬美元區間"},{"date":"2027-01-31","date_precision":"month","type":"product","event":"2027 年第一波新品上市，含 CELSIUS 新口味與新包裝","impact":"高","watch":"鋪貨點數與週銷速度，是否靠加碼促銷"},{"date":"2027-03-31","date_precision":"quarter","type":"guidance","event":"2026 年第四季財報，帳面成長放緩，並說明 2027 年計畫","impact":"高","watch":"第四季毛利率、交易投資占比、FY2027 共識修正"},{"date":"2027-05-31","date_precision":"month","type":"guidance","event":"2027 年第一季財報，第一個收益管理計畫生效後的毛利率讀數","impact":"高","watch":"毛利率是否達 49%"},{"date":"2027-08-31","date_precision":"month","type":"guidance","event":"2027 年第二季財報，CFO 所稱 Alani Nu 零售與帳面對照最乾淨的一季","impact":"高","watch":"Alani Nu 落差、CELSIUS 零售額年增是否轉正"},{"date":"2027-12-31","date_precision":"quarter","type":"product","event":"Alani Nu 於部分海外市場上市","impact":"中","watch":"海外營收金額與占比是否開始揭露"}],"_projected_from":"v19"}
```
