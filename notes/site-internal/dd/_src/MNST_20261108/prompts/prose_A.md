你是 stock-analyst v20 的**散文層（prose）agent**，標的 MNST（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MNST　日期：2026-11-08　archetype：None　前份裁決：2026-05-18　Q1 26 數字爆表(Rev +27%／EPS +29%／國際 +45%／China/India +95%)；新 .5B 回購；但估值已追平 5Y median；PEG 2.44 仍在 🟠 區；現價 .09 貼 BB 上軌(.70)+ 接近 52W 高 .77。Thesis 完整(品質 A／長期信心高／護城河 9/10)但時機不到 → B 觀望。等 PEG <2.0 或 MA 短回測 W52(./股) 再加碼。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1850B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（602B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（815B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1472B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1262B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（595B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（859B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2172B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4029B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2551B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1850           3605-5150      5 條（2–6 內）  
s3                  8000         602           5179-7398      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3549          8016-11451      5 條（2–6 內）  
s6                 11000         595          7283-10405      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         859           1849-2641      5 條（2–6 內）  
s10                 5000        2172           1980-2828      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2551           2000-2449      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5007B；至少需散文≈39.99KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−47.5%
−37.4%
−35%
−35
−8.2%
0%
0
0.13
0.14%
0.14
0.3
0.33
0.62%
0.91
0.97
1
01
1%
1.02
1.07
1.09
1.15
1.19
1.2%
1.2
1.21
1.22
1.24
1.27
1.3
1.30
1.31
1.34
1.35
1.42
1.48
1.5%
1.56
1.57
1.66
1.72
1.79
1.89
2.0
2
02
2.04
2.24
2.31
2.4%
2.44
2.62%
2.63
2.9
3
3.0
3%
03
3.2%
3.6
4%
4
04
4.4%
4.5
5%
5
05
5.97
6%
06
6
6.3
6.4%
6.9
07
7%
7
7.1%
7.2%
7.6%
08
8%
8
9
9%
9.4%
9.5%
9.6
9.9
10%
10
10.3
10.5%
11%
11
11.3%
11.4
11.6%
12
12.3%
12.4%
12.6
13%
13.3%
13.5%
13.6%
13.9%
14%
14
14.3%
14.7%
14.84%
15%
15.1%
15.32%
16
16.2%
16.7%
17%
17.1%
17.50%
18%
19%
19.2%
19.8%
20
20%
20.2%
20.7%
21
22.9
23.7
24
24%
24.9%
25
25%
25.63
25.7%
26%
26
27%
27
27.1%
27.5%
28%
28.0%
28
28.1%
28.3%
28.5%
28.6%
28.9%
29%
29.16%
29.2%
29.5
29.80
29.8
30%
30
30.5%
31.8%
32
32.11%
34
34.6%
34.9
35%
35.5%
36%
36
37%
37
37.2%
38
38.5
39.76
40
42
42.1%
42.24
43
43.55
43.87
44
44.5%
45%
45.29
45.7
45.72
46.0%
46.9
47%
47.5%
47.7%
48%
48.8%
48.83
49
49%
50%
50
50.2
50.5
51.5
52
52.5%
53%
54%
54.7%
55%
56%
56.6
58%
58.8
60.4%
67.9%
70
77
78.54
82.94
86.5%
87.09
90
90.58
92%
95
100
100%
103
107.64
126
150
150%
159
185
190
250
269
810
894.97
2022
2023
2025
2026
2027
2028
2030
20261108
1,470
1,990
2,850
3,040
5,000
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
{"meta":{"ticker":"MNST","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Monster Beverage Corporation"},"oneliner":"全球能量飲料的品牌與通路贏家，第三季營收年增 16.7%，但增量營益率只剩約 14%。現價約 40 倍 FY2026E，基礎情境五年年化約 4%～5%，等股價回到 38 美元以下再談進場。","thesis":{"H":[{"id":"H1","text":"美國以外仍是第一成長引擎，增速從第三季 28.1% 回落，但 FY2027 仍守得住 18% 以上。","2y":"FY2027 美國以外淨銷售年增 ≥18%，占總營收 ≥49%","5y":"FY2031 美國以外占總營收 ≥56%，EMEA、亞太、拉美沒有一區連兩年衰退","10y":null,"threshold":"FY2027 年增 ≥18%，占比 ≥49%（第三季為 28.1%、47%）","source":"每季財報新聞稿與 10-Q 的地區淨銷售，法說的區域數字","drift_rule":"TTM 年增連 2 季低於 17.1% 算削弱，連 3 季低於 16.2% 算反轉"},{"id":"H2","text":"美加基本盤守住高個位數成長，份額不被對手體系明顯侵蝕。","2y":"FY2027 美加淨銷售年增 ≥8%","5y":"FY2031 美加淨銷售年增 ≥6%","10y":null,"threshold":"美加淨銷售年增 ≥8%（第三季 9.5%），美國價值份額年減不超過 50 個基點","source":"10-Q 地區營收；8-K 附件的 Nielsen 份額表（本次資料未收錄，下次須補）","drift_rule":"TTM 年增連 2 季低於 7.6% 算削弱，連 3 季低於 7.2% 算反轉"},{"id":"H3","text":"百分比會被地區組合拖累，但營業利益金額要跟得上營收，FY2027 調整後營益率守住 28.5%。","2y":"FY2027 調整後營益率 ≥28.5%，營收與調整後營業利益增速差 ≤3 個百分點","5y":"FY2031 營益率 ≥28.5%，毛利率 ≥52.5%","10y":null,"threshold":"調整後營益率 ≥28.5%（第三季 29.2%）；增速差 ≤3 個百分點（第三季 9.6、第二季 6.9）","source":"每季財報新聞稿的調整後損益調節表","drift_rule":"TTM 調整後營益率連 2 季低於 27.1% 算削弱，連 3 季低於 25.7% 算反轉；增速差已連 2 季超過 5 個百分點，先記削弱觀察"}],"R":[{"id":"R1","text":"美國對手體系成形：Celsius 加 Alani Nu 金額份額約 20.7%，KDP 整合 C4、Bloom、GHOST，Red Bull 新口味也分走份額；美洲主管 Rob Gehring 又轉任可口可樂，接班安排法說未交代。","h_ref":"H2","clock":"🔥","threshold":"美加淨銷售年增連 2 季低於 8%（沿用前份數字，改用公司有揭露的美加總額），或連 2 季落後 Nielsen 美國品類 3 個百分點以上（第三季 2.9）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","supply_demand_durability#1","end_markets#3"]},{"id":"R2","text":"毛利率與營益率往下：地區組合是結構性拖累，鋁價與 Midwest Premium、運費、代工費是成本面壓力，避險也不完整。","h_ref":"H3","clock":"⚡","threshold":"GAAP 毛利率連 2 季低於 54%（沿用前份，不因毛利走低而放寬；第三季 54.7%）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","capital_markets_pricing#3"]},{"id":"R3","text":"監管從標示走向年齡限制：英國 16 歲以下禁售預計 2027 年 4 月生效，待國會批准；印度 FSSAI 禁用能量飲料字樣，德里高等法院 10 月只給暫時救濟，案件未結。兩國營收金額事實表未涵蓋。","h_ref":"H1","clock":"🐢","threshold":"第三個主要市場立法限制年齡或咖啡因上限，且評估擴散機率達 50% 以上才砍倉；印度終局敗訴且當季印度營收年減則減碼","evidence_refs":["regulatory_antitrust#2"]},{"id":"R4","text":"客戶集中升高：Coca-Cola Europacific Partners 占淨銷售從 2023 年 13% 升到 2026 年第三季 17%，Coca-Cola Consolidated 約 9%，後者 2025 年 11 月遭 S&P 展望調負。","h_ref":"H1","clock":"🐢","threshold":"單一裝瓶商占淨銷售 >20%，或前兩大裝瓶商任一信評低於 BBB-","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]}],"single_thing":{"description":"FY2027 全年調整後營業利益率跌破 27.5%（第三季 29.2%）。","why_fatal":"這是最大的單一敏感度：營益率每差 1 個百分點，FY2027 EPS 差約 3.2%，國際增速少 5 個百分點只差約 2.4%。共識 1.31 美元隱含營益率約 30%，跌破 27.5% 代表 EPS 約低 6%～9%，利潤追上營收的說法失效，倍數往 28～30 倍靠，股價約 34～37 美元，跌 19%～26%。","if_happens":"未持有就不建倉，持有就減碼一半，基礎情境的營益率中樞改為 27%。","how_monitor":"每季新聞稿的調整後營業利益除以淨銷售；2027 年 8 月公布上半年後先看半年值，2028 年 2 月定案。","probability":"約 25%（未來 12～24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":34.9,"peg_fy2":2.31,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":0.97,"FY2026E":1.15,"FY2027E":1.31,"FY2028E":1.48},"fy_end_month":12,"eps_basis":"FY2025A 為拆股調整後 GAAP 稀釋 EPS（yfinance 年報）；FY2026E～FY2028E 為 Koyfin 11 月 7 日共識快照，GAAP 或調整後口徑事實表未標明。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"輕資產品牌商、淨現金、借可口可樂體系出貨，成長靠國際鋪貨而非併購"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久，依據 2026-11-05 法說引用的 GlobalData 到 2030 年高個位數成長與 Nielsen 第三季各區雙位數品類成長；NACS 報導美國 2027 年降溫到約 7%。","bargaining":{"up":"鋁罐與代工廠議價偏弱：FY2025 10-K 稱通常不避險，部分代工合約可轉嫁成本，Midwest Premium 又受關稅推高。","down":"前兩大裝瓶商合計約 26%，可口可樂體系同時是通路夥伴；零售端靠冷櫃與貨架爭奪，品牌強勢時議價偏向公司。","geo":"美國以外占第三季 47%，關稅影響集中在鋁；英國年齡限制與印度標示令是地區監管風險。"},"profit_pool_dir":"利潤池往美國以外移，金額增加但百分比較低；五年份額變化事實表未涵蓋。","tam_table":[{"item":"美國能量飲料零售額 2025 年","value":"269 億美元，五年高個位數成長（Monster 主管所述）"},{"item":"第三季品類成長","value":"美國 12.4%、EMEA 14.7%、亞太 11.3%、拉美 28.3%（2026-11-05 法說引用 Nielsen 等）"},{"item":"第三方預測","value":"GlobalData 到 2030 年全球高個位數成長（2026-11-05 法說引用，非公司數字）"},{"item":"全球 TAM、滲透率、營業利益池占比","value":"事實表未涵蓋，12 月 1 日投資人日待補"}]},"moat":{"mechanism":"品牌心智加上可口可樂全球裝瓶體系的鋪貨、冷櫃與新品上架能力","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力擴大（EMEA 份額增加 190 個基點），定價權穩定（第三季定價大致抵銷鋁與投入成本），美國份額缺數字，合併看穩定。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用份額方向與單期營益率。","threats":[{"level":"🔴","text":"美國出現對手體系：Celsius 有 PepsiCo 長約配銷並收購 Alani Nu，金額份額約 20.7%；KDP 配銷 C4、Bloom 並收購 GHOST。攻擊點是無糖與女性客群，第三季美加淨銷售增速低於品類。","p":"35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","supply_demand_durability#1"]},{"level":"🟡","text":"Red Bull 新口味搶份額，Jefferies 認為主要取自 Celsius，其次才是 Monster。","p":"30%","evidence_refs":["end_markets#3"]},{"level":"🟡","text":"BODYARMOR、Prime、Starbucks 等加入機能成分搶能量場景，公司認為成分含量較低、定位不同，目前是點對點分流。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多半是同一人。第三季品類美國年增 12.4%、EMEA 14.7%，歐洲每年約 30% 新客，公司稱 Gen Z 家戶觸及 58%。屬於想要而非必需，但價位低、習慣已形成。"},{"item":"決策層級","level":"🟡","text":"替代要看單次購買：消費者在冷櫃前換牌幾乎沒有成本，黏著靠品牌與鋪貨。最好的代理變數是漲價後銷量，美國 11 月 1 日漲價的第一個完整季要到 2027 年 5 月才看得到。"},{"item":"價值鏈分配","level":"🟡","text":"品牌商拿走大部分利潤，TTM 營益率 29.16%。但最大客戶占比升到 17%，海外區域毛利率 37%～48%，代表海外的利潤分配對公司較不利；裝瓶商利潤率事實表未涵蓋。"},{"item":"社會容忍度","level":"🟡","text":"英國 16 歲以下禁售預計 2027 年 4 月生效，待國會批准；印度 FSSAI 要求停用能量飲料字樣，德里高等法院 10 月只給暫時救濟。目前壓力在年齡與標示，還沒有壓到價格。"}],"roiic":"事實表未涵蓋投入資本，無法直接算。代理：FY2022～FY2025 稅後營業利益約增 6.3 億美元（稅率假設 24%），FY2023～FY2025 累計淨利與自由現金流各約 50.5 億美元（財務歷史表，yfinance 年報），帳面淨再投資接近 0，比率沒有意義。","reinvest_rate":"約 0%（代理：FY2023～FY2025 累計淨利減自由現金流，FY2023 含營運資金回收）","endo_ceiling":null,"formula_note":"內生成長等於增量報酬乘再投資率，此處再投資率近零，算式給不出上界。資金不是成長的限制，真正上限是品類成長加份額與價格。行銷費用走損益，帳面看起來像零再投資；2026-08-06 法說 Schlosberg 預告冷櫃將有重大投資，再投資率之後可能上升。周轉率事實表未涵蓋，象限依生產外包與現金轉換推定。"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","MNST":55.55,"KO":62.32,"PEP":54.17,"CELH":47.95,"KDP":48.04,"unit":"%"},{"metric":"營業利益率","MNST":29.16,"KO":32.11,"PEP":15.32,"CELH":17.5,"KDP":14.84,"unit":"%"},{"metric":"FCF 利潤率","MNST":22.58,"KO":27.97,"PEP":10.66,"CELH":6.09,"KDP":9.11,"unit":"%"}],"competitors":[{"name":"KO","gm":62.32,"om":32.11,"fcf_margin":27.97,"strategy_note":"既是配銷夥伴也是利潤率標竿，TTM 營益率 32.11% 高於 MNST 29.16%；Rob Gehring 轉任可口可樂後雙方合作可能更深，利益分界也要多看一眼。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PEP","gm":54.17,"om":15.32,"fcf_margin":10.66,"strategy_note":"靠 2022 年起與 Celsius 的長約配銷切入能量飲料，TTM 營益率 15.32%。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CELH","gm":47.95,"om":17.5,"fcf_margin":6.09,"strategy_note":"最直接的對手，併 Alani Nu 後美國金額份額約 20.7%，貢獻無糖成長約 28%，但 TTM 營益率只有 17.50%，遠低於 MNST。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"KDP","gm":48.04,"om":14.84,"fcf_margin":9.11,"strategy_note":"走配銷整合路線，帶 C4、Bloom 並收購 GHOST，TTM 營益率 14.84%，整合效果還要時間證明。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主、價為輔；無併購，回購貢獻很小。","runway_years":"事實表未涵蓋全球滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本事實表未涵蓋，增量報酬乘再投資率算不出上界；實際上限看品類高個位數成長加份額與價格，基礎情境 EPS 年化 10.5% 不依賴外部資金。","segments":[{"item":"Monster Energy 飲料分部","value":"第三季 23.7 億美元，年增 17.1%"},{"item":"策略品牌分部","value":"第三季 1.56 億美元，年增 19.8%"},{"item":"酒類分部","value":"第三季 2,850 萬美元，年減 13.6%"},{"item":"美加","value":"第三季年增 9.5%"},{"item":"EMEA","value":"第三季年增 24.9%，毛利率 37.2%"},{"item":"亞太","value":"第三季年增 12.3%，毛利率 42.1%"},{"item":"拉美","value":"第三季年增 48.8%，毛利率 47.7%"}],"decay_signals":["核心市占：美加第三季淨銷售年增 9.5%，低於 Nielsen 美國品類 12.4%，第三季法說也沒有再報美國份額；口徑不完全相同，算半亮，計一個。"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自身品牌與品類，近 12 個月無併購，資本報酬表不影響本輪結論。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 無併購；過往併購的投入金額事實表未涵蓋，無法計算已實現報酬。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"FY2026E EPS 1.15 美元除以第三季回購均價 43.87 美元，約 2.62%。10 年期殖利率事實表未涵蓋，但要過門檻，10 年期須低於 0.62%，判未過。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"第三季 SBC 3,040 萬美元年化約 1.22 億美元，除以市值 894.97 億美元，約 0.14%／年，低於 1.5%。","grade":"過"}]},"valuation":{"basis":"FY2026E 共識 EPS 的本益比，搭配 PEG；公司已獲利，不用營收倍數當主尺。","tier":"飲料品牌高成長","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，屬資料缺口，無法做跨公司倍數比較。"},"fwd_pe":39.76,"peg":2.63,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026E 39.76 倍、PEG 2.63，高於 2 算貴；基礎情境五年年化約 4%～5%，低於 8%。本益比在 4 個年度端點的 67.9% 分位，還沒到頂，RSI 48.83，動能不熱，所以判偏貴，還不到最貴一檔。短期空間：FY2027 基礎 EPS 1.27 美元乘 36 倍約 45.7 美元；中期空間：FY2029 基礎 EPS 1.57 美元乘 32 倍約 50.2 美元。","upside_short_pct":0.0,"upside_mid_pct":9.9},"trap_analysis":{"verdict":"🟡","label":"不是低價陷阱，風險是用高倍數買到利潤率下滑"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"第三季美加淨銷售年增 9.5%，低於 Nielsen 美國品類 12.4%；Celsius 組合份額約 20.7%；增量營益率約 14%。","assumption":"美國份額流失與成本壓力同時發生，公司用更多行銷與促銷防守。","consequence":"五年後虧 50% 的路徑：美加成長掉到中個位數，營益率落到 24%，FY2031 EPS 1.30 美元，20 倍，股價 26 美元，途中再多跌一段。","ruling":"部分採納，機率 25%。反駁面是 EMEA 份額與歐洲零糖 46.0% 都還在擴大。此路徑與唯一致命點部分重疊，營益率是共同變數，這裡多了美國份額一項。","watch":"美加淨銷售增速、美國份額表、調整後營益率","evidence_refs":["supply_demand_durability#1","competitive_share_entrants#1"]},{"view":"論點成功但股東經濟變差","evidence":"美國以外占第三季 47% 且仍快於美國，區域毛利率 37.2%～47.7%；2026-11-05 法說 Schlosberg 說「we bank dollars, we don't bank percentages」；2026-08-06 法說 Schlosberg 預告冷櫃重大投資。","assumption":"國際成長達成，但新增營收的利益率長期低於舊生意，還要多投冷櫃與平價品牌。","consequence":"營收超預期、EPS 不超預期，倍數照樣下來。推算每多 1 個百分點國際占比，毛利率少約 0.13～0.33 個百分點，占比到 56% 約再少 1.2～3.0 個百分點。","ruling":"採納，這是本輪最重要的修正，第三個假設從毛利率反彈改成營業利益金額跟上營收。","watch":"增量營益率、區域毛利率、資本支出","evidence_refs":["capital_markets_pricing#3"]},{"view":"價格已反映太多","evidence":"FY2026E 39.76 倍、PEG 2.63，股價營收比在 4 個年度端點的最高點；賣方平均目標價拆股調整後約 45.29 美元，幾乎等於現價。","assumption":"五年後倍數仍高，但會隨成長降溫往 30 倍走。","consequence":"基礎情境成真，五年年化也只有 4%～5%，要靠牛市情境才到約 11%。","ruling":"採納。卡住進場的只有價格，生意本身沒有壞。","watch":"股價相對 38 美元；FY2027 共識 EPS 是否下修"}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 87.09 → 本次 45.72（-47.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=87.09","side_b":"本次 price_at_dd=45.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 87.09 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 87.09 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 87.09 美元：Bull 價 78.54、Bear 價 26，五年期望值 −37.4%，基準年化 −8.2%，不對稱比 0.14","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.14。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 87.09 美元：五年期望值 −37.4%，基準年化 −8.2%，不對稱比 0.14","side_b":"本次情境、股價 45.72 美元：五年期望值 +19.2%，基準年化 4.4%，不對稱比 1.66","ruling":"再換股價、情境不動：起點價下跌 47.5%，五年期望值多 56.6 個百分點，基準年化多 12.6 個百分點，不對稱比由 0.14 升到 1.66。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份空欄補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位都是空值，當時的格式沒有產出。","side_b":"本輪護城河方向穩定，五年後跑道中等，類型為品質複利成長，最大回撤 −35%～−50%，牛熊機率各 25%，不屬循環股，週期位置留空。","ruling":"這是格式補齊，不是看法改變，無法和前份比方向。","evidence_level":"格式差異","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"結論與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評級 B、陷阱風險中等，理由是時機不到，等回檔加碼。","side_b":"本輪評級 B、陷阱風險中等，但理由換了：第三季毛利率 54.7% 跌破前份 55% 的反彈假設，增量營益率約 14%，美加增速低於品類。","ruling":"等級不變，內容變差。前份看的是價格時機，本輪多了利潤率這個基本面問題，長期信心由高降到中。","evidence_level":"實績","settle_metric":"FY2026 第四季毛利率與增速差","if_then":["若第四季毛利率低於 54%，下一季再低於 54% 就減碼三分之一","若連 2 季增速差縮到 3 個百分點內，陷阱風險降一級"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份估值偏貴，PEG 2.44，拆股前 87.09 美元，換算 43.55 美元。","side_b":"本輪仍偏貴，PEG 2.63，45.72 美元，較前份拆股調整價約高 5%。","ruling":"結論不變。股價小漲而共識沒有上修，PEG 略升。前份的 87.09 美元不可和現價直接比，否則會誤讀成腰斬。","evidence_level":"實績","settle_metric":"FY2027 共識 EPS 與股價","if_then":[],"evidence_refs":[]},{"axis":"建倉與加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 PEG <2.0 或 MA 短回測 W52 再加碼","side_b":"股價回到 38 美元以下，基礎情境五年年化回到 8% 以上；觸發後重跑研究再建首倉","ruling":"舊條件作廢。52 週線現在 42.24 美元，回測到那裡基礎情境年化只有約 6.4%，不夠補償利潤率風險；PEG 用的三年共識成長正是本輪不採信的部分，改用報酬率直接定價。任何加碼前先重跑研究。","evidence_level":"本研究推算","settle_metric":"股價與基礎情境報酬","if_then":["若股價跌到 38 美元以下且毛利率未連 2 季低於 54%，分批反買","若股價先漲、利潤數字未改善，不追"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份沒有獨立的清倉或減碼指標，只有警戒：美加 Monster Energy 連 2 季 <8%；GM 連 2 季 <54%。","side_b":"保留 8% 與 54% 兩個數字，美加改用公司有揭露的總額；新增 FY2027 調整後營益率 <27.5% 與增速差連 3 季 >7 個百分點，觸發時減碼；營益率破線且美加連 4 季 <5% 才清倉。","ruling":"舊數字不放寬。新增利潤率門檻，是因為地區組合會讓毛利率單獨看失真。","evidence_level":"格式與新增指標","settle_metric":"每季財報","if_then":[],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（欄位為空）","side_b":"FY2027 全年調整後營業利益率跌破 27.5%","ruling":"本輪新設 Single Thing。選營益率是因為敏感度最大：1 個百分點約等於 FY2027 EPS 的 3.2%，高於國際增速少 5 個百分點的約 2.4%。","evidence_level":"本研究推算","settle_metric":"FY2027 年報","if_then":["若 FY2027 全年調整後營益率低於 27.5%，減碼一半，未持有則不建倉"],"evidence_refs":[]},{"axis":"假設門檻重訂","cause":"新證據","prior_field":["thesis.H"],"side_a":"2027 國際合計 ≥30% YoY；2027 美加 Monster Energy 品牌 ≥10%；FY27 全年 GM ≥56%","side_b":"FY2027 美國以外年增 ≥18%；美加淨銷售年增 ≥8%；FY2027 調整後營益率 ≥28.5%","ruling":"國際增速第一季約 45%、第二季 34.6%、第三季 28.1%，基期變大，30% 已不適合當兩年門檻。毛利率反彈假設被否定：第三季 54.7%，2026-11-05 法說 Schlosberg 明說國際成長會持續拖累，FY27 56% 的門檻正式退休，改看利潤金額。門檻下調同時，基礎 EPS 也調到低於共識，沒有放寬結論。","evidence_level":"實績＋管理層說法","settle_metric":"FY2027 年報","if_then":[],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"FY2027 利潤率方向","cause":null,"prior_field":null,"side_a":"共識：FY2027 營收年增 9.4%、EPS 年增 13.9%，推算營益率從約 29% 升到約 30%；11 月 7 日快照三年 EPS 全部沒動。","side_b":"第三季營收年增 16.7%、調整後營業利益只增 7.1%，第二季是 20.2% 對 13.3%；2026-11-05 法說 Schlosberg 說國際成長對毛利率的拖累是大家都得接受的事，鋁成本上升延到至少 2027 年第一季。","ruling":"方向相反，必須選邊。採第三季實績這一側：基礎情境 FY2027 EPS 1.27 美元，低於共識約 3%。依據是增量營益率約 14%，而美國漲價 11 月 1 日才生效，效果還沒有數字。市場若錯，錯在成長基準，把漲價當成已經抵銷成本與組合拖累。快照在財報後兩天，賣方可能還沒改模型，在第一個驗證數字出來前凍結加碼。","evidence_level":"實績與管理層說法為高，隱含營益率為本研究推算","settle_metric":"FY2026 第四季與 FY2027 第一季的營收年增減調整後營業利益年增","if_then":["若連 2 季增速差 ≤3 個百分點，基礎 EPS 上修到共識，可建倉價調到 40 美元","若連 3 季增速差 >7 個百分點，取消建倉計畫，已持有則減碼三分之一","若股價先漲、利潤數字未改善，不追","若股價跌到 38 美元以下而利潤率未破門檻，分批反買"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"美國份額","cause":null,"prior_field":null,"side_a":"2026-08-06 法說 Schlosberg：美加價值份額第二季增加 70 個基點；同場 Gehring：家戶調查拉新客速度約品類兩倍。","side_b":"2026-11-05 法說沒有再給美國份額數字，只報 EMEA 與 Oceania；美加淨銷售年增 9.5%，Nielsen 美國品類 12.4%。Jefferies 認為 Red Bull 新口味也取走部分份額。","ruling":"目前不可裁決。淨銷售與掃描數據口徑不同，裝瓶商庫存也會造成差異，不能直接算成掉份額；但管理層少報了上一季報過的數字，本身是警訊，先記半個衰退訊號。決勝數據在 8-K 的區域掃描附件，本次資料未收錄，2027 年 2 月財報前要補。","evidence_level":"公開實績，但口徑不完全可比","settle_metric":"8-K 附件 Nielsen 美國份額年變化","if_then":["若美國份額連 2 季年減超過 50 個基點，第二個假設改判削弱並停止加碼","若美國份額回到年增，這個衰退訊號熄燈"],"evidence_refs":["supply_demand_durability#1","end_markets#3"]},{"axis":"管理層利潤說法","cause":null,"prior_field":null,"side_a":"2026-08-06 法說（摘錄標為 Rob Gehring，該段講者與原話有錯位）：營收快於銷量、利潤快於營收。","side_b":"第二季調整後營業利益年增 13.3%、營收 20.2%；第三季 7.1%、16.7%，連兩季做不到。2026-11-05 法說 Schlosberg 改強調「we bank dollars」，不回答第四季與明年節奏。","ruling":"採實績。這句話出自訂價討論，未必是全公司承諾，但連兩季反向就不能當利潤率會回升的證據。","evidence_level":"實績＋法說摘錄","settle_metric":"FY2026 第四季增速差","if_then":["若第四季調整後營業利益增速仍低於營收 5 個百分點以上，基礎情境維持低於共識，停止加碼"],"evidence_refs":[]},{"axis":"鋁成本時程與避險","cause":null,"prior_field":null,"side_a":"2026-08-06 法說 Schlosberg：鋁成本至少到 2026 年底持續溫和上升，摘錄也記錄管理層承認 Midwest Premium 避險可能不足。FY2025 10-K：公司通常不避險。","side_b":"2026-11-05 法說 Schlosberg：延到至少 2027 年第一季，原鋁一年漲 36%，仍稱影響溫和，並說有在做避險。","ruling":"不採信也不否定「溫和」。第三季定價確實大致抵銷成本，毛利率下滑主要來自地區組合；但時程已往後延一季，這項歸因列為未證、監測。","evidence_level":"管理層說法","settle_metric":"GAAP 毛利率","if_then":["若到 2027 年第二季報告時毛利率連 2 季低於 54%，「溫和」的說法算證偽，減碼三分之一"],"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"調整項是否一次性","cause":null,"prior_field":null,"side_a":"公司把第三季設備減損 1,990 萬美元、數位轉型 1,470 萬美元列為 G&A 內的特殊項目。","side_b":"SAP S/4HANA 要到 2028 年 1 月 1 日上線，數位轉型費用至少還有 5 季。","ruling":"減損先當一次性，數位轉型不算一次性，所以本輪同時看 GAAP 營益率 28.0%。未證、監測：減損類項目若連 3 季出現，就不再視為一次性。","evidence_level":"實績","settle_metric":"GAAP 與調整後營業利益差額","if_then":[],"evidence_refs":[]},{"axis":"賣方目標價口徑","cause":null,"prior_field":null,"side_a":"Tickergate 彙整 44 位分析師 12 個月平均目標價 90.58 美元，區間 77～103 美元；Morgan Stanley 103 美元、Bernstein 95 美元。","side_b":"這些都在 8 月拆股前。除以 2 後平均 45.29 美元，區間 38.5～51.5 美元，比現價低約 1%。","ruling":"不能用 90.58 美元算出接近翻倍的空間。現價已貼著拆股調整後平均目標價，支持觀望。最高與最低目標價相差 1.34 倍，分歧不大。目標價都在第三季財報前，下次要重查。","evidence_level":"二手彙整，日期未標明","settle_metric":"投資人日與第四季財報後的目標價","if_then":[],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"營收年增 16.7%，國際 28.1%，歐洲零糖份額 46.0%，淨現金約 36 億美元；美國 11 月 1 日漲價加上 2027 年費用基期墊高，利潤率可能反彈；FY2027 營收共識只有年增 9.4%，明顯偏低，10 月銷售還有 11.6%。","side_b":"就算營收比共識高 3%，營益率不回升，EPS 也只到共識附近；40 倍已經把反彈算進去。","ruling":"不買。多頭說的營收上修我同意，基礎情境營收高於共識；差異在利潤率與倍數。卡住進場的只有價格。","evidence_level":"本研究推算","settle_metric":"FY2027 第一季調整後營益率","if_then":["若 FY2027 第一季調整後營益率 ≥30% 且股價 ≤43 美元，可建倉價調到 43 美元並重跑研究","若 FY2027 第一季調整後營益率低於 28% 而股價高於 38 美元，不追"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：Celsius 併 Alani Nu、KDP 併 GHOST，新進者持續增加。","side_b":"結構：美國零售額 2025 年 269 億美元，第三季各區品類雙位數成長，GlobalData 看到 2030 年高個位數。其他變數：英國年齡限制與印度標示令。","ruling":"雙向拉鋸。品類需求結構性轉好，美國競爭同時惡化，監管是第三個慢變數。","evidence_level":"公司申報＋第三方資料","settle_metric":"美國份額與品類增速","if_then":[],"evidence_refs":["competitive_share_entrants#1"]}],"triggers":[{"n":1,"text":"股價回到 38 美元以下，重跑研究後建首倉","type":"估值rearm","maps_to":"H3","metric":"MNST 收盤價","threshold":"≤38 美元","action":"分批反買","source_freq":"每日收盤","date":null},{"n":2,"text":"FY2027 全年調整後營益率跌破 27.5%","type":"Single Thing","maps_to":"H3","metric":"調整後營業利益除以淨銷售","threshold":"<27.5%","action":"減碼一半，未持有則不建倉","source_freq":"每季新聞稿，年度定案","date":"2028-02"},{"n":3,"text":"GAAP 毛利率連 2 季低於 54%","type":"風險","maps_to":"R2","metric":"GAAP 毛利率","threshold":"連 2 季 <54%","action":"減碼三分之一","source_freq":"每季新聞稿","date":"2027-05","evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","capital_markets_pricing#3"]},{"n":4,"text":"營收與調整後營業利益增速差回到 3 個百分點內","type":"假設驗證","maps_to":"H3","metric":"營收年增減調整後營業利益年增","threshold":"連 2 季 ≤3 個百分點","action":"基礎 EPS 上修到共識，可建倉價調到 40 美元","source_freq":"每季新聞稿","date":"2027-05"},{"n":5,"text":"美加淨銷售年增連 2 季低於 8%","type":"風險","maps_to":"R1","metric":"美加淨銷售年增","threshold":"連 2 季 <8%","action":"減碼三分之一","source_freq":"每季 10-Q","date":"2027-05","evidence_refs":["supply_demand_durability#1","end_markets#3"]},{"n":6,"text":"營益率破線且美加成長同時失守","type":"清倉","maps_to":"H2、H3","metric":"FY2027 調整後營益率與美加淨銷售年增","threshold":"營益率 <27.5% 且美加連 4 季 <5%","action":"清倉","source_freq":"每季財報","date":"2028-02"},{"n":7,"text":"年齡與標示限制擴散：英國 2027 年 4 月生效，印度案件未結","type":"風險","maps_to":"R3","metric":"新增立法市場數、印度當季營收","threshold":"第三個主要市場立法且擴散機率 ≥50%，或印度終局敗訴且當季營收年減","action":"減碼三分之一","source_freq":"法規公告與法院公告","date":"2027-04","evidence_refs":["regulatory_antitrust#2"]},{"n":8,"text":"投資人日複審：看全球滲透率、長期利潤率框架與冷櫃投資","type":"複審日期","maps_to":"H1、H3","metric":"管理層揭露內容","threshold":"提供滲透率或利潤率框架","action":"更新五年後跑道與基礎情境","source_freq":"一次性","date":"2026-12-01"},{"n":9,"text":"股價先漲、利潤數字沒有改善","type":"估值rearm","maps_to":"H3","metric":"收盤價與增速差","threshold":"股價高於 45.72 美元且增速差仍 >5 個百分點","action":"不追","source_freq":"每季財報與每日收盤","date":null},{"n":10,"text":"裝瓶商集中或信用惡化","type":"風險","maps_to":"R4","metric":"單一裝瓶商占淨銷售、前兩大信評","threshold":"單一裝瓶商 >20% 或信評低於 BBB-","action":"停止加碼","source_freq":"每季 10-Q 與評等公告","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]}],"kill_metrics":[{"metric":"FY2027 全年調整後營業利益率","bear_threshold":"<27.5%","window":"FY2027 全年","source":"財報新聞稿調整後損益調節表","last_status":"ok"},{"metric":"GAAP 毛利率","bear_threshold":"連 2 季 <54%","window":"連續 2 季","source":"財報新聞稿","last_status":"warning"},{"metric":"美加淨銷售年增","bear_threshold":"連 2 季 <8%","window":"連續 2 季","source":"10-Q 地區營收","last_status":"ok"},{"metric":"營收年增減調整後營業利益年增","bear_threshold":"連 3 季 >7 個百分點","window":"連續 3 季","source":"財報新聞稿","last_status":"warning"},{"metric":"美國以外淨銷售 TTM 年增","bear_threshold":"連 3 季 <16.2%","window":"連續 3 季","source":"10-Q 地區營收","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=5.97, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價回到 38 美元以下，基礎情境五年年化回到 8% 以上；觸發後重跑研究再建首倉","exec_line":"現在不追。38 美元以下分批建首倉，第一筆前先重跑研究；12 月 1 日投資人日與 2027 年 2 月財報前不加碼。"},"reasoning":{"industry":"第三季淨銷售 25.63 億美元，Monster Energy 飲料分部 23.7 億美元占約 92%，策略品牌 1.56 億美元占約 6%，酒類 2,850 萬美元且年減 13.6%。GAAP 毛利率 54.7%，GAAP 營益率 28.0%，調整後營益率 29.2%。生產與配銷交給代工廠和可口可樂體系裝瓶商，資本用得少，代價是 EMEA、亞太、拉美毛利率只有 37%～48%。單點依賴：Coca-Cola Europacific Partners 占第三季淨銷售約 17%，Coca-Cola Consolidated 約 9%，兩家同屬一個體系，這既是通路護城河，也是集中風險。產業時鐘在擴張期，依據是 2026-11-05 法說引用的第三季品類成長：美國 12.4%、EMEA 14.7%、亞太 11.3%、拉美 28.3%。供需持久性判為結構性持久，但增速會降溫：GlobalData 預期到 2030 年全球高個位數成長，美國零售商預期 2027 年降到約 7%。","moat":"機制是品牌加上可口可樂體系的鋪貨與冷櫃。同業 ROIC 事實表未涵蓋，可證方向改用份額：EMEA 第三季價值份額增加 190 個基點，歐洲零糖區隔 46.0%（第二季 44.5%），Oceania 增加 150 個基點，英國、埃及、塞爾維亞拿到價值第一；2026-08-06 法說報美加份額增加 70 個基點。TTM 營益率 29.16%，高於 CELH 17.50%、PEP 15.32%、KDP 14.84%，低於 KO 32.11%，只有單期，看不出利差方向。本輪從前份 9 分下調：定價權給 8 分，因為第三季定價只是大致抵銷鋁與投入成本，美國 11 月 1 日漲價的銷量反應還沒有數字；Celsius 加 Alani Nu 與 KDP 整合形成的對手體系再扣一分，合併落在 B。","growth":"成長以量為主、價為輔，沒有併購，回購貢獻很小。三年共識 EPS 從 FY2025A 0.97 美元到 FY2028E 1.48 美元，年化 15.1%（Koyfin 11-07 快照）；營收 FY2025 82.94 億美元到 FY2027E 107.64 億美元，年化 13.9%。內生上界算不出來，資金也不是限制，缺口改用共識自身拆：FY2027 EPS 年增 13.9%、營收 9.4%，多出的 4.5 個百分點全靠利潤率擴張，這正是本輪不採信的部分，長期信心上限為中。全球滲透率事實表未涵蓋，無法算到 30% 的年數。下一條成長曲線有證據但不夠厚：第三季印度當地貨幣年增 86.5%、巴西 60.4%、中國 35.5%，餐飲通路與蛋白飲料還沒有數字。第三季營收與 GAAP 營業利益增速差 10.3 個百分點，遠超 3 個百分點的警戒。若 12 月 1 日投資人日給出全球滲透率且低於 35%，跑道可上調一級。","governance":"自由現金流對淨利 FY2023 0.91 倍、FY2024 1.07 倍、FY2025 1.02 倍（財務歷史表，yfinance 年報）。SBC 第三季 3,040 萬美元，占淨銷售約 1.2%，年化稀釋約 0.14%。現金去向四分事實表未涵蓋，只知道第三季回購 1 億美元、均價 43.87 美元，第二季沒有回購，無股息，截至 11 月 4 日授權餘額約 8 億美元，近 12 個月無併購。","valuation":"現價 45.72 美元約當 FY2026E 39.76 倍、FY2027E 34.9 倍。PEG 以 FY2025A 到 FY2028E 年化 15.1% 算為 2.63，高於前份 2.44。分位數只有 4 個年度端點：本益比 67.9%，股價營收比與企業價值營收比都在最高點，不能當五年區間用，五年高低點事實表未涵蓋。前份價格 87.09 美元是拆股前，換算 43.55 美元，本次實際上漲約 5%。同業倍數事實表未涵蓋，只能和自身比。","premortem":"成長熄火壓力：以 FY2028 基礎 EPS 1.42 美元為起點，FY2029 成長 15%、10%、5% 配 36、30、20 倍，股價約 58.8、46.9、29.8 美元，對現價約＋29%、＋3%、−35%，三項過兩項。十類衰退訊號只有美國份額半亮，毛利率第三季年減一次，第二季還是上升，再差一季就亮第二個。管理層連兩季不回答利潤率節奏：2026-08-06 對 Herzog 的費用 run rate、對 Carey 的毛利率信心，2026-11-05 對 Galbo 的組合影響、對 Herzog 的第四季與明年節奏，都沒有正面答案。歷史最大回撤事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺的是全球便利通路每一罐能量飲料的品牌溢價，錢卡在品牌與可口可樂體系的貨架位置，不在產能。","moat":"護城河穩定：國際份額還在擴大，定價能抵成本但抵不過地區組合，美國是唯一要盯的缺口。","growth":"五年後還有跑道但要打折：美國以外還在快速鋪貨，全球滲透率查不到，新增長也比舊生意薄。","capital":"資本紀律沒有大錯，但閒錢太多：帳上淨現金約 36 億美元，回購在 40 倍附近買得很貴。","valuation":"現價要 FY2031 EPS 做到約 2.24 美元、年化 14.3%，再守住 30 倍，才有 8% 年化；我只信 1.89 美元、年化 10.5%。","how_wrong":"最可能看錯在利潤率：漲價與費用槓桿若提早見效，38 美元可能等不到；美國份額若也掉，跌幅不只兩成。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 38 美元以下，基礎情境五年年化回到 8% 以上","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":45.72,"week26_return_pct":5.97,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026E 已接近完成，未見一次性項目墊高；爭點在 FY2027 利潤率，放在情境路徑處理。"},"catalysts":[{"date":"2026-12-01","date_precision":null,"type":"guidance","event":"紐約投資人日","impact":"高","watch":"長期利潤率框架、全球滲透率、冷櫃投資"},{"date":"2027-02","date_precision":"month","type":"other","event":"FY2026 第四季財報","impact":"高","watch":"毛利率是否低於 54%、增速差、美國份額"},{"date":"2027-03","date_precision":"month","type":"product","event":"Monster Protein 上市","impact":"低","watch":"鋪貨進度與對基本款的稀釋"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"英國 16 歲以下禁售預計生效，待國會批准","impact":"中","watch":"英國銷量與其他市場是否跟進"},{"date":"2027-05","date_precision":"month","type":"other","event":"FY2027 第一季財報，美國 11 月 1 日漲價的第一個完整季","impact":"高","watch":"銷量反應、調整後營益率"},{"date":"2028-01-01","date_precision":null,"type":"other","event":"SAP S/4HANA 上線","impact":"中","watch":"轉換期的出貨中斷與費用"}],"_projected_from":"v19"}
```
