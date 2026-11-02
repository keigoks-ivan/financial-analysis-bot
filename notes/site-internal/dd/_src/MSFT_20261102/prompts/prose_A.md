你是 stock-analyst v20 的**散文層（prose）agent**，標的 MSFT（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSFT_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：MSFT　日期：2026-11-02　archetype：None　前份裁決：2026-07-30　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1897B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（795B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（998B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1621B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1284B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（915B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1091B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2059B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4483B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2479B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1897           3572-5103      5 條（2–6 內）  
s3                  8000         795           5044-7205      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3903          7768-11097      5 條（2–6 內）  
s6                 11000         915          7060-10085      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1091           1686-2409      3 條（2–6 內）  
s10                 5000        2059           2059-2941      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2479           2000-2521      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5874B；至少需散文≈39.13KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−45%
−45
−33%
−30%
−30
−22%
−10%
−8
−7%
0.1%
0.1
0.2%
0.3%
0.35
0.36%
0.45
0.50
0.5
0.51
0.6
0.697%
0.7
0.70
0.75
0.9
1
01
1.15
1.2
1.3%
1.39
1.5%
1.8%
1.9%
2
02
2%
2.3
2.5
3
3%
3.2%
3.31
3.4%
3.8%
3.88
04
4
4.2%
4.4%
4.5
4.89
05
5%
5
5.8
6
06
6.7
6.8%
6.8
7%
07
7
7.2
8%
8
8.5
9%
9
9.68
9.97
10%
10
11%
11
11.2%
11.4
11.7%
12
12%
13%
13
14
14%
14.6%
15%
15
16
16.1%
17%
17.21
17.3%
17.31%
17.95
18
18%
18.4%
18.8%
19%
19
19.18
19.5%
19.5
20
20%
20.02
20.4
20.5
20.6%
20.8%
21%
21
21.5%
21.6
21.62
22%
22
22.9%
23%
23
23.8
24
24.14
25%
25
26
26.07
26.4%
26.44
27
27%
27.24
27.8
28
28%
29
29%
30
30%
30.09
30.5
31
31.6%
31.8
32
33%
33.3%
33.6%
34.5%
35
35%
35.6
35.7%
35.8
37%
37.6
37.7%
39.5
40%
40.8%
41%
41
41.77%
41.8%
42
45%
46%
46.2
46.5
46.78%
46.8%
47%
47
47.1%
48%
48.4
49
49.7%
49.8%
50%
50
51%
52.9
57.4%
60%
60
61.9%
62%
65%
65
66%
67%
67.7%
68%
69%
70
72
73%
74
74.3
74.51
74.75
75%
84
89%
90
98%
100
100%
102
103%
110.3%
141
150%
155
159
164
186
211.9
241
270
286
288
302
331.8
352
365
$365
390.54
394
408
438
448
452
459
459.2
483
521.91
534
569.45
580
581
639
640
668
694
723.6
767
768
801
807
885
912
922.8
1110
1286
1337.5
1552
1700
1750
2025
2026
2027
2030
3000
3466
6770
6900
20261102
1,255.5
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
{"meta":{"ticker":"MSFT","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Microsoft Corporation"},"oneliner":"雲與 AI 需求仍大於供給，Azure 加速到 48%；但每一元營業利益只換回約四成自由現金流，OpenAI 占營收升到約一成一。股價三個月漲三成三後估值回到合理，續抱不加碼，等現金轉換回升。","thesis":{"H":[{"id":"H1","text":"Azure 與 Microsoft Cloud 的高成長由企業廣度撐住，不靠單一客戶；供給逐步解除後，Azure 固定匯率年增仍守在 30% 以上","2y":"FY28 每季 Azure 固定匯率年增 ≥30%，Microsoft Cloud 年增 ≥22%","5y":null,"10y":null,"threshold":"FY27 每季 Azure 固定匯率年增 ≥40%；FY28 每季 ≥30%","source":"每季財報電話會 CFO 揭露的 Azure 固定匯率成長；新聞稿的 Microsoft Cloud 營收","drift_rule":"兩年期論點：偏離門檻連 2 季 ≥5% 記削弱，連 3 季 ≥10% 記反轉（例：FY28 連 3 季 Azure 年增 <27%）"},{"id":"H2","text":"這輪 AI 資本支出換得回股東現金：折舊高峰過後，自由現金流追上淨利，毛利率止跌","2y":null,"5y":"FY29 起 FCF/淨利 ≥0.7，Microsoft Cloud 毛利率 ≥62%；FY27 全年自由現金流維持為正","10y":null,"threshold":"FY28 全年 FCF/淨利 ≥0.6；Microsoft Cloud 毛利率不低於 62%","source":"10-Q、10-K 現金流量表（營業現金流減不動產廠房設備現金支出）；季報的 Microsoft Cloud 毛利率","drift_rule":"五年期論點：偏離門檻連 4 季 ≥5% 記削弱，連 6 季 ≥10% 記反轉"},{"id":"H3","text":"M365 由按人頭計費擴展為人頭加用量，由 ARPU 接手席位成長，工作流程入口的地位不被前沿模型公司繞過","2y":null,"5y":null,"10y":"到 FY2036，生產力雲營收維持雙位數成長，用量計費占比持續上升","threshold":"M365 商用雲固定匯率年增 ≥15%（席位成長可降到個位數）；Copilot 用量計費客戶數維持季增","source":"財報電話會的 M365 商用雲成長、付費席位與 ARPU 拆解；Copilot 點數消費客戶數","drift_rule":"十年期論點：跨 2 個年度低於門檻記削弱，跨 3 個年度記反轉"}],"R":[{"id":"R1","text":"OpenAI 集中度：本季 OpenAI 約占營收 11%（FY26 全年約 7%），應收帳款由 60 億升到 72 億美元，FY26 Q2 時占商業 RPO 約 45%。OpenAI 自身靠外部融資支付算力，一旦重談或延付，Microsoft 為它建的產能就要折價轉賣","h_ref":"H1","clock":"🔥","threshold":"OpenAI 營收占比 >15%，或應收帳款 >100 億美元，或任一季提列呆帳","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#3","supply_demand_durability#2"]},{"id":"R2","text":"資本支出與元件成本吃掉現金：Q1 資本支出 452 億美元（含融資租賃 74 億），自由現金流 186 億，只有營業利益的四成；CFO 首次表態會在條件合適時動用租賃以外的外部資金。10-K 自述資料中心關鍵零組件供應商有限且短缺，關稅也推高成本","h_ref":"H2","clock":"🔥","threshold":"Microsoft Cloud 毛利率 <62%，或 FY27 全年自由現金流轉負，或發行普通股融資","evidence_refs":["geo_supply_chain#0","reg_tariff_export#0"]},{"id":"R3","text":"前沿模型公司與開源模型繞過 Microsoft：10-K 自承多數業務進入門檻低，AI 對手包括夥伴；Ramp 數據中企業支出 Anthropic 37%、OpenAI 33%（不含 Microsoft）；AI 代理可能壓縮按人頭收費","h_ref":"H3","clock":"🐢","threshold":"M365 商用付費席位年增 <2%，且 M365 商用雲年增 <12% 連兩季","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"id":"R4","text":"反壟斷與出口管制：FTC 就綑綁與雲端授權向對手問訊，英國 CMA 啟動策略市場地位調查，10-K 也列出美、英、歐、中正積極執法；出口管制限制對特定國家提供產品","h_ref":"H3","clock":"🐢","threshold":"FTC 正式起訴，或 CMA 認定策略市場地位並附雲端授權行為要求","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","reg_tariff_export#1"]},{"id":"R5","text":"Copilot 證券集體訴訟：指控 2025-05 至 2026-01 期間誇大 Copilot 能力與採用，2026-01-29 單日跌約 10%；本季法說會未更新 Copilot 付費席位數（7 月時說超過 3000 萬）","h_ref":"H3","clock":"🐢","threshold":"駁回聲請未獲准、進入集體認證，或和解金額 >50 億美元","evidence_refs":["major_events#0","lawsuit_class_action#0"]}],"single_thing":{"description":"OpenAI 公開縮減、延後或重談其對 Azure 的算力承諾，或 Microsoft 對 OpenAI 的應收帳款提列減損","why_fatal":"OpenAI 約占本季營收 11%，FY26 Q2 時占商業 RPO 約 45%；RPO 中 12 個月以後認列的部分年增 98%。這輪資本支出約四分之三是 CPU、GPU 短壽資產，客戶抽單後折舊照提，毛利率與自由現金流會同時受壓。這是對五年 EPS 敏感度最大的單一事件。","if_happens":"FY29 EPS 估計下修 10% 到 15%，倍數向 16 到 18 倍收斂，走 Bear 路徑。部位減半；三季內若 RPO 剔除 OpenAI 後仍年增 ≥20%，才停止減碼。","how_monitor":"每季 10-Q 關係人揭露（OpenAI 營收、應收帳款）、法說會是否說明剔除 OpenAI 後的 RPO、OpenAI 融資消息","probability":"15%（12–24 個月）。依據：應收由 60 億升到 72 億，但增幅低於對應營收；目前未見評等調降或付款延遲。"}},"appendix_a":{"growth_durability":8,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.62,"peg_fy2":1.15,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":17.95,"FY2027E":20.02,"FY2028E":24.14,"FY2029E":30.09},"fy_end_month":6,"eps_basis":"GAAP 稀釋 EPS。FY2026A 取自年報 17.95，含 OpenAI 相關的營業外損益；FY2027E 起為 Koyfin 共識快照（2026-10-31，分析師家數事實表未列）。財年於 6 月底結束。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSFT_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"高營益率、訂閱加用量雙軌收費、資本密集度急升中"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久為主，但供給可逆性高。瓶頸在電力與資料中心殼體，緩解時間約 2026 年底至 2027 年（二手分析，未獨立證實）。緩解後全產業新產能同時上線，供需可能翻轉，這一點計入 Bear 機率。","bargaining":{"up":"上游議價強。10-K 自述 GPU、網通、電力與冷卻等關鍵零組件供應商有限且短缺，競爭者共用同一批供應商；元件漲價直接進資本支出。Microsoft 以自研 Maia、Cobalt 晶片部分對沖。","down":"下游分散，但集中度在上升。FY26 沒有單一客戶超過營收一成，OpenAI 約 7%；FY27 Q1 OpenAI 約占營收 11%，FY26 Q2 時占商業 RPO 約 45%（二手報導，基準與日期不同）。","geo":"美國出口管制限制對特定國家供貨；報導指公司計畫把 Surface 與資料中心元件最多八成移出中國製造（公司未置評）；台灣資料中心將由 2 座增為 4 座。"},"profit_pool_dir":"利潤池往上游算力元件與前沿模型移動。Microsoft Cloud 毛利率年減到 66%，Q2 指引約 65%，管理層歸因於 Azure 組合。Microsoft 在平台層（Foundry 多模型路由、Agent 365 治理）收過路費，以守住自己的分配。","tam_table":[{"item":"全球雲基礎設施支出（2026 年第一季）","value":"約 1286 億美元，年增 35%（Synergy，二手引述）"},{"item":"雲基礎設施份額","value":"AWS 29%→28%、Azure 20%→21%、Google 13%→14%（2025Q3→2026Q1，Synergy 二手；來源間數字不一）"},{"item":"超大規模雲 2026 年資本支出","value":"約 6900 億美元（Introl 二手分析）"},{"item":"企業 AI 支出份額（資料不含 Microsoft）","value":"Anthropic 37%、OpenAI 33%（Ramp）"},{"item":"Microsoft 商業 RPO","value":"6770 億美元，年增 73%；12 個月內認列約 30%，加權平均天期 2.3 年"},{"item":"營業利益池五年占比變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"轉換成本加規模。企業身分（Entra）、M365 資料圖譜（Work IQ）與 Azure 合約綁在同一套授權裡，客戶要換的是整套工作流程，不是單一產品。平台層（Foundry、Fusion）可替換模型，讓模型商在 Microsoft 的平台上互相競價。","execution":9,"pricing":8,"grade":"A","trend":"→","trend_evidence":"執行面擴大：Azure 份額 20%→21%（Synergy 二手），Azure 年增由 7 月指引的約 45% 交出 48%。定價面穩定：M365 漲價後付費席位仍增 5%、token 單價高於預期，但 E3 與單品銷售偏弱。一項擴大、一項穩定，判穩定。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋","threats":[{"level":"🟡","text":"前沿模型公司直接賣給企業，並把新增算力放在其他雲。Microsoft 以多模型平台承接，屬點對點競爭。","p":30,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#1"]},{"level":"🟡","text":"AI 代理壓縮按人頭計費。Microsoft 已主動轉向人頭加用量計費：GitHub 改按用量計費後，代理功能的點數消費翻倍以上。屬點對點。","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"反壟斷調查針對綑綁與雲端授權（FTC 向對手問訊、英國 CMA 啟動策略市場地位調查）。若成案，會直接限制護城河賴以運作的授權折扣機制。","p":35,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2"]}],"roic_durability":{"quadrant":"高利益率、周轉率下滑：Q1 現金資本支出年增 103%，營收只增 19%。應查再投資負擔與資產更新週期（四分之三是短壽資產）。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是員工與開發者。決策者分兩層：訂閱由 IT 出錢，用量由業務單位出錢（Nadella 本季說法），三個角色都成立；Azure 需求大於供給。扣分在增量需求集中：OpenAI 約占本季營收 11%，而 OpenAI 自身靠外部融資支付算力。代理變數：7 月 CFO 稱雲營收近九成來自前沿模型公司以外的客戶。"},{"item":"決策層級","level":"🟢","text":"替代性要在企業工作流程這一層衡量：身分、M365 資料圖譜與資安綁在同一份合約，換掉等於重建整套流程。代理變數：M365 漲價後付費席位仍增 5%；商業 RPO 加權平均天期 2.3 年。模型層可以每個任務換供應商，但換的是 Microsoft 平台上的模型，不是平台本身。"},{"item":"價值鏈分配","level":"🟡","text":"整條 AI 價值鏈裡，GPU、記憶體與電力供應商有限且短缺（10-K），元件漲價先進資本支出；前沿模型公司拿走模型層的價值。Microsoft Cloud 毛利率年減到 66%，Q2 指引約 65%。Microsoft 用自研晶片與多模型路由爭回分配，但目前分配仍往上游移動。"},{"item":"社會容忍度","level":"🟡","text":"美國 FTC、英國 CMA、歐盟同時在審視綑綁與雲端授權折扣，10-K 自述可能遭罰款或被限制產品提供；各國也在推主權雲。監管把實際定價上限壓在經濟上限之下。還不到紅燈，因為仍在調查階段，尚未成案。"}],"roiic":30,"reinvest_rate":65,"endo_ceiling":19.5,"formula_note":"單位為 %。增量 ROIC＝FY23→FY26 稅後營業利益增量÷同期累計再投資。營業利益由 885 億（211.9×41.77%）增到 1552 億（331.8×46.78%），以 CFO 指引的約 20% 稅率換算，稅後增加 534 億。累計再投資以淨利減自由現金流代理：FY24 141 億＋FY25 302 億＋FY26 668 億＝1110 億，得 48%。這個數字未含融資租賃與收購，且最近一年的資本支出尚未產生營收，所以取 30% 為中心值。再投資率：FY26 淨利減 FCF 占淨利 50%；FY27 Q1 加計融資租賃 74 億後約 69%（Q1 淨利以調整後 EPS 4.89 乘約 74.3 億股估算），取 65%。內生上界＝30%×65%≈19.5%。"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","MSFT":67.66,"GOOGL":60.86,"CRM":77.28,"ADBE":89.25,"TEAM":84.83,"unit":"%"},{"metric":"營業利益率","MSFT":47.1,"GOOGL":33.32,"CRM":21.52,"ADBE":35.7,"TEAM":0.16,"unit":"%"},{"metric":"FCF 利潤率","MSFT":17.31,"GOOGL":4.19,"CRM":34.49,"ADBE":40.79,"TEAM":20.07,"unit":"%"},{"metric":"研發密度","MSFT":10.52,"GOOGL":15.81,"CRM":14.49,"ADBE":18.07,"TEAM":49.74,"unit":"%"}],"competitors":[{"name":"GOOGL","gm":60.86,"om":33.32,"fcf_margin":4.19,"rd_intensity":15.81,"strategy_note":"營益率 33.3%，FCF 利潤率只剩 4.2%，資本支出壓力比 Microsoft 更重。雲份額同樣在上升，是 AI 算力與辦公套件的直接對手。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CRM","gm":77.28,"om":21.52,"fcf_margin":34.49,"rd_intensity":14.49,"strategy_note":"FCF 利潤率 34.5% 高於 Microsoft，營益率 21.5%。Dynamics 與 Copilot 代理直接打它的 CRM 地盤，但 7 月 CFO 也說自家 CRM 銷售週期拉長，目前未見份額轉移的證據。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"ADBE","gm":89.25,"om":35.7,"fcf_margin":40.79,"rd_intensity":18.07,"strategy_note":"毛利率 89%、FCF 利潤率 40.8%，是純軟體，不背資本支出。與 Microsoft 的交集在內容生成 AI，不是核心戰場。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"TEAM","gm":84.83,"om":0.16,"fcf_margin":20.07,"rd_intensity":49.74,"strategy_note":"營益率 0.2%，研發密度 49.7%。GitHub 代理（Copilot Fusion，代理開的 PR 已占三分之一）在壓縮它的開發者工具空間。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（Azure 算力、Copilot 與 GitHub 用量），價次之（M365 漲價、token 單價），併購與淨回購近乎零","runway_years":"10+（企業 AI 代理與用量計費仍在早期；滲透率事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"增量 ROIC 約 30% × 再投資率約 65% ≈ 19.5%，推導見護城河題的報酬持續期段；共識年複合 18.8% 落在上界內，營業口徑約 22% 會超出","segments":[{"item":"Agents and Infra（FY27 Q1）","value":"768 億美元，年增 25%；Q2 指引 801–807 億美元（+24–25%）"},{"item":"Devices and Consumer（FY27 Q1）","value":"155 億美元，年減 3%；Q2 指引 159–164 億美元"},{"item":"Microsoft Cloud","value":"639 億美元，年增 30%；毛利率 66%（年減），Q2 指引約 65%"},{"item":"Azure","value":"年增 48%；Q2 指引固定匯率 49–50%"},{"item":"M365 商用雲","value":"年增 17%（調整後 18%）；付費席位增 5%，E3 與單品銷售執行偏弱；Q2 指引約 19%"},{"item":"Windows OEM 與裝置","value":"年減 22%（OEM 年減 27%）；Q2 指引年減 30% 中段"},{"item":"搜尋廣告（扣除 TAC）","value":"年增 12%"},{"item":"Xbox","value":"年減 2%；Q2 內容與服務指引中至高個位數成長"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":true,"evidence":"Q4 FY26 公司毛利率 67%，年減（7 月 CFO）；Q1 FY27 毛利額增 17%，低於營收增 19%，毛利率年減；Q2 指引成本增 26–27%，高於營收增 18–19%"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"Azure 雲基礎設施份額 20%→21%（Synergy 二手）"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"M365 商用 7 月漲價後付費席位仍增 5%；E3 與單品銷售偏弱，列入監測"},{"signal":"EPS 年複合高於營收逾 5 個百分點","lit":true,"evidence":"FY23→FY26 GAAP EPS 年複合 22.9%，營收 16.1%，差 6.8 個百分點；營業利益年複合 20.6%，差距約三分之一來自營業外損益"},{"signal":"FCF/淨利連兩年低於 0.75","lit":true,"evidence":"FY25 0.70、FY26 0.50"},{"signal":"SBC/營收高於 5% 且逐年上升","lit":false,"evidence":"SBC 占營收 3.4%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"Windows OEM 年減 27% 是 Windows 10 換機潮的高基期加上庫存去化（CFO 歸因），不是 TAM 被替代；AI 代理壓縮按人頭計費只有部落格論點"},{"signal":"產業估值倍數近三年系統性下移","lit":null,"evidence":"事實表未涵蓋同業倍數歷史"},{"signal":"維護性資本支出占 FCF 逾 60%","lit":null,"evidence":"事實表未拆分維護性與成長性資本支出"},{"signal":"停止投資新產能且營收三年內下滑","lit":false,"evidence":"資本支出仍在加速，營收增 19%"}],"trap_rating":"🔴"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建資本支出，不靠併購撐；本季股利加回購 102 億美元，完整的現金去向拆分事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年最大收購為 Activision。本季 Devices and Consumer 營益率升到 35%，主因是收購無形資產攤銷減少；Xbox 營收年減 2%。投入資本與增量利潤事實表未涵蓋，算不出已實現的增量報酬","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"現價盈餘殖利率 3.8%（1÷26.07），FCF 殖利率約 1.5%（TTM FCF 利潤率 17.31% × TTM 營收約 3466 億 ÷ 市值 3.88 兆）。10 年期殖利率事實表未涵蓋，但只要高於 1.8% 就不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"稀釋股數由 FY23 約 74.75 億（淨利 723.6 億÷EPS 9.68）降到 FY26 約 74.51 億（1337.5 億÷17.95），三年淨減 0.3%；SBC 占營收 3.4%","grade":"過"}]},"valuation":{"basis":"Fwd P/E（FY1＝FY2027E 共識 EPS）加 PEG","tier":"大型平台軟體與超大規模雲","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率與研發密度，沒有同業 Fwd P/E。終端倍數改以公司三個月前約 20.4 倍、現值 26.07 倍為下上錨，同業倍數列為資料缺口"},"fwd_pe":26.07,"peg":1.39,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Fwd P/E 26.07 倍；三年 EPS 年複合 18.8%，PEG 1.39，落在 1 到 2 的合理帶；trailing P/E 在 4 個年度端點中位於 32 分位（不是五年分位，五年分位事實表未涵蓋）；基本情境五年年化約 12%。判合理，不便宜。","upside_short_pct":14.0,"upside_mid_pct":46.2},"trap_analysis":{"verdict":"🔴","label":"建置期現金轉換型：毛利率連兩季年減、FCF/淨利連兩年低於 0.75、EPS 跑贏營收逾 5 個百分點；不是需求衰退"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"OpenAI 約占本季營收 11%，應收帳款由 60 億升到 72 億美元；FY26 Q2 時 OpenAI 占商業 RPO 約 45%。10-K 自承關鍵零組件與電力短缺，全產業 2026 年資本支出約 6900 億美元（二手）。","assumption":"需求大於供給是結構性的，不是少數 AI 實驗室用外部資金在囤算力。","consequence":"電力瓶頸在 2027–28 年解除後，產能同時上線；OpenAI 縮減承諾，GPU 租價下跌而折舊照提。EPS 五年持平，倍數壓到 16 倍，五年虧 30% 到 50%。","ruling":"部分採納：列為唯一致命點，並把 Bear 機率提到 30%。不全採的理由是，Q1 Azure 加速的主因是 Foundry 與 CPU 閒置產能變現；7 月 CFO 也稱雲營收近九成來自前沿模型公司以外的客戶。","watch":"每季 OpenAI 營收占比與應收、RPO 剔除 OpenAI 後的年增率、12 個月內認列 RPO 的年增率","evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#2","supply_demand_durability#2","supply_demand_durability#4"],"fact_refs":["f_kpi8_commercial_rpo","f_kpi0_revenue_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"Q1 自由現金流 186 億，只有營業利益 459 億的 41%；FY25、FY26 FCF/淨利為 0.70、0.50；Q1 現金資本支出 394 億，年增 103%。CFO 表示會在合適時動用租賃以外的外部資金；Microsoft Cloud 毛利率 66%，Q2 指引約 65%。","assumption":"營收加速終究會讓現金轉換回升。","consequence":"Azure 目標全部達成，但每年約 1700 億美元的資本支出、元件漲價與融資租賃利息，讓 FCF/淨利長期卡在 0.5。股東拿到的現金成長遠低於 EPS 成長，倍數向資本密集型公司靠攏。","ruling":"採納，這是本次不加碼的唯一約束，三盞衰退燈都指向這件事。解除條件是 FY27–FY28 任連續兩季 FCF/淨利 ≥0.6。","watch":"季度 FCF/淨利、Microsoft Cloud 毛利率、是否發債或增資","evidence_refs":["geo_supply_chain#0","reg_tariff_export#0"],"fact_refs":["f_kpi3_free_cash_flow","f_kpi1_gaap_operating_income","f_kpi9_capex_pp_e_cash_addition","f_peer_msft_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"股價由前份的 390.54 漲到 521.91（+33.6%），同期 FY1 共識 EPS 只上修 4.4%（19.18→20.02），Fwd P/E 由約 20.4 倍升到 26.07 倍；26 週報酬 26.4%。","assumption":"市場仍低估 Azure 加速的持續性。","consequence":"一年後若倍數回到 20 倍、FY28 EPS 符合共識 24.14 元，股價約 483（−7%），等於 EPS 達標仍賠錢。","ruling":"部分採納：估值由便宜回到合理區間中段，基本情境年化約 12%。持有合理，追價不划算。","watch":"Fwd P/E 是否在現金轉換未改善時超過 32 倍（約 640 美元）","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_price_at_dd","f_consensus_rev_3m_fy1_pct","f_fwd_pe_latest","f_week26_return_pct"]},{"view":"論點失敗","evidence":"10-K 自承多數業務進入門檻低，AI 對手包括夥伴；Ramp 數據中企業支出 Anthropic 37%、OpenAI 33%（不含 Microsoft）；M365 商用付費席位只增 5%，E3 與單品銷售偏弱；本季未更新 Copilot 付費席位數，同時有集體訴訟指控誇大 Copilot 採用。","assumption":"Copilot 是工作入口，企業不會繞過 M365 直接向模型公司買代理。","consequence":"M365 席位停滯，用量計費的錢被前沿模型公司拿走，生產力雲成長降到個位數，H3 失效。","ruling":"以反駁為主，保留監測。本季 Copilot 日活季增近 50%，用量計費客戶季增逾 75%，5 萬席以上客戶年增逾 8 倍。但席位數不再揭露，證據只剩管理層描述，信心打折。","watch":"M365 商用雲年增率與付費席位、下季是否恢復揭露 Copilot 席位","evidence_refs":["competitive_share_entrants#2","substitute_technology#2","major_events#0"],"fact_refs":[]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 390.54 → 本次 521.91（+33.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=390.54","side_b":"本次 price_at_dd=521.91","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡、陷阱燈 🟡→🔴。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡、陷阱燈 🟡→🔴。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 390.54 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 390.54 美元：Bull 價 912、Bear 價 286，五年期望值 +61.9%，基準年化 11.2%，不對稱比 5.8","side_b":"本次情境、股價仍用 390.54 美元：Bull 價 1,255.5、Bear 價 352，五年期望值 +110.3%，基準年化 18.4%，不對稱比 17.21","ruling":"先換情境、股價不動：五年期望值多 48.4 個百分點，基準年化多 7.2 個百分點。不對稱比由 5.8 變為 17.21。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 390.54 美元：五年期望值 +110.3%，基準年化 18.4%，不對稱比 17.21","side_b":"本次情境、股價 521.91 美元：五年期望值 +57.4%，基準年化 11.7%，不對稱比 3.31","ruling":"再換股價、情境不動：起點價上漲 33.6%，五年期望值少 52.9 個百分點，基準年化少 6.7 個百分點，不對稱比由 17.21 降到 3.31。合計五年期望值比前份少 4.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：股價重估","cause":"價格變動","prior_field":["val","max_dd_pct"],"side_a":"前份（2026-07-30）：股價 390.54，Fwd P/E 約 20.4 倍（390.54÷當時 FY1 共識 19.18），估值合理偏低，結論為建倉；最大回撤估 −50%（單點）。","side_b":"本次：股價 521.91，三個月 +33.6%，同期 FY1 共識只上修 4.4% 到 20.02，Fwd P/E 26.07 倍。估值仍在合理區間，但位置由下緣移到中段；回撤改為 −30% 至 −45% 的區間；新資金不追，既有部位續抱。","ruling":"漲幅約八成五來自倍數擴張（20.4→26.07 倍，+28%），EPS 上修只貢獻約一成五。估值結論的顏色不變，但安全邊際已經用掉，結論由建倉改為續抱不加碼。","evidence_level":"事實表價格與共識快照","settle_metric":"Fwd P/E 與 FY1 共識修正幅度","if_then":["若股價續漲到 Fwd P/E ≥32 倍（約 640 美元），而 FCF/淨利仍 <0.6，則減碼 20%","若股價跌回 W104 均線約 448 以下，而 Azure 固定匯率年增 ≥40%、FCF/淨利不低於 0.45，則分批反買三分之一，不是停損"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"前份漂移：衰退信號增加","cause":"新證據","prior_field":["trap","signal"],"side_a":"前份：價值陷阱風險中等，整體評等 B。","side_b":"本次：Q1 FY27 毛利率再度年減（毛利額增 17%，低於營收增 19%），與 Q4 FY26 連成兩季。再加上 FCF/淨利 FY25 0.70、FY26 0.50，以及 FY23–FY26 GAAP EPS 年複合 22.9% 高於營收的 16.1%，衰退信號亮三盞，價值陷阱風險升為高。整體評等維持 B。","ruling":"三盞燈的共同根因是 AI 建置期資本密集度上升，屬股東現金轉換風險，不是需求衰退，所以評等不降，但也不加碼。當毛利率年減幅收斂到 1 個百分點以內，且 FCF/淨利連兩季 ≥0.6 時，風險降回中等。","evidence_level":"公司財報與法說會（一手）","settle_metric":"季度毛利率年變動、FCF/淨利","if_then":["若 FY27 Q2、Q3 的 FCF/淨利都 ≥0.6，則價值陷阱風險降回中等，並加碼","若 Microsoft Cloud 毛利率跌破 62%，則減碼三分之一"],"evidence_refs":[]},{"axis":"前份漂移：未變動欄位複核","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河趨勢穩定、五年後跑道寬、屬品質複利成長型、非循環股所以不設循環位置。","side_b":"本次維持。Azure 份額 20%→21%，年增由 7 月指引的約 45% 交出 48%，執行面擴大；M365 漲價後席位仍增 5%，定價面持平。Copilot 用量計費客戶季增逾 75%，Foundry 營收年增逾三倍，第二曲線有證據。營收增 19%，不是循環。","ruling":"四欄不變。新證據同向支持，但定價面的 E3 銷售偏弱列入監測。","evidence_level":"公司法說會與二手份額資料","settle_metric":"Azure 份額、M365 商用雲年增率","if_then":["若 M365 商用付費席位年增 <2%，且 M365 商用雲年增 <12% 連兩季，則護城河趨勢改判縮減、停止加碼"],"evidence_refs":["competitive_share_entrants#1","end_markets#2"]},{"axis":"前份漂移：情境機率重配","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份：Bull 25%、Bear 28%。","side_b":"本次：Bull 23%、Base 47%、Bear 30%。終端年改為 FY2032E（判斷日起滿五年時的當期財年，與現價以 FY1 為分母同口徑）；Bear 改為 EPS 五年持平在約 22 元、終端 16 倍。","ruling":"Bear 加 2 個百分點、Bull 減 2 個百分點。依據是 OpenAI 營收占比由 FY26 的約 7% 升到本季約 11%，應收由 60 億升到 72 億美元。需求面的新證據轉強，只支撐 Base 不支撐 Bull，因為 Bull 需要現金轉換同步回升。","evidence_level":"公司揭露與二手報導","settle_metric":"OpenAI 營收占比","if_then":["若 OpenAI 占比回落到 8% 以下，且 RPO 剔除 OpenAI 後年增 ≥25%，則下次把 Bear 機率調回 25%"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"axis":"行動門檻變動：加碼條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"已進場；加碼觸發＝FY27 任兩季 FCF/淨利 ≥0.6，或股價回檔 $365 以下且 Azure cc ≥35%","side_b":"既有部位續抱；重啟加碼＝FY27–FY28 任連續兩季自由現金流÷淨利 ≥0.6（事件錨，不設價位）","ruling":"加碼條件改為只看事件。唯一約束是現金轉換尚未證實，這屬於論點未決，應該用事件錨，不設價位。刪掉 $365 的價格條件，因為現價已高出四成，而且價格到了不代表約束已經解除。「任兩季」改為「任連續兩季」，避免單季租賃交付時點造成誤觸。","evidence_level":"方法調整","settle_metric":"季度 FCF/淨利","if_then":["若 FY27–FY28 任連續兩季 FCF/淨利 ≥0.6，則加碼至前份上限"],"evidence_refs":[]},{"axis":"行動門檻變動：減碼與清倉指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼與清倉指標（kill_metrics 為空）","side_b":"本次新設五項：FCF/淨利連兩季 <0.35，或 FY27 全年 FCF 轉負；OpenAI 營收占比 >15%、應收 >100 億美元或提列呆帳；Azure 固定匯率年增連兩季 <30%；Microsoft Cloud 毛利率 <62%；12 個月內認列 RPO 年增連兩季 <20%。任一項觸發減碼三分之一，兩項同時觸發清倉。","ruling":"前份把風險只寫成敘述，沒有可執行的減碼與清倉門檻。本次補上，門檻取在現值與管理層指引之外、留有安全距離的位置。","evidence_level":"方法調整","settle_metric":"五項指標每季讀數","if_then":["任一項觸發則減碼三分之一","任兩項同時觸發則清倉"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（Single Thing 為空）","side_b":"OpenAI 公開縮減、延後或重談其對 Azure 的算力承諾，或 Microsoft 對 OpenAI 的應收提列減損","ruling":"OpenAI 占營收由約 7% 升到約 11%，FY26 Q2 時占商業 RPO 約 45%，已是對五年 EPS 敏感度最大的單一事件。設為 Single Thing，一旦觸發即減碼一半。","evidence_level":"10-K 關係人揭露與二手報導","settle_metric":"10-Q 關係人揭露","if_then":["若 OpenAI 公開縮減承諾或應收提列減損，則減碼一半"],"evidence_refs":["customer_concentration_credit#3","customer_concentration_credit#1"]},{"axis":"需求強度與訂單背離","cause":null,"prior_field":null,"side_a":"Azure 年增 48%，Q2 指引 49–50%，CFO 稱需求仍大於供給；商業 RPO 6770 億，年增 73%。","side_b":"商業訂單年減 12%；RPO 中 12 個月以後認列的部分年增 98%，遠快於 12 個月內的 29%，新增承諾天期拉長，且集中在大額 Azure 合約。","ruling":"可調和。訂單年減來自去年同期大額 Azure 承諾的高基期（CFO 說明），12 個月內認列的 RPO 增 29%，與營收成長一致。長天期部分的品質取決於 OpenAI 能否履約，交給唯一致命點監測。","evidence_level":"公司揭露（一手）加二手報導","settle_metric":"12 個月內認列 RPO 年增率","if_then":["若 12 個月內認列 RPO 年增連兩季 <20%，則減碼三分之一","反向：若 RPO 剔除 OpenAI 後年增 ≥25%，則需求廣度獲得證實，維持持有"],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#0"]},{"axis":"營業利益成長與股東現金背離","cause":null,"prior_field":null,"side_a":"營業利益增 21%，營益率 49.8%；營業現金流 580 億，年增 29%。","side_b":"現金資本支出 394 億（年增 103%）加融資租賃 74 億，自由現金流 186 億只有營業利益的 41%；FY26 FCF/淨利 0.50；CFO 表示會在合適時動用外部資金。","ruling":"可調和，但尚未證實。差額是建置期的時間差，前提是新產能真如管理層所說「上線即變現」。證據到位之前，現金這一側是續抱不加碼的唯一約束。","evidence_level":"公司財報（一手）","settle_metric":"季度 FCF/淨利","if_then":["若 FY27–FY28 任連續兩季 FCF/淨利 ≥0.6，則加碼至前份上限","若 FY27 全年 FCF 轉負或發行普通股，則減碼三分之一","價格先走、證據未到：若股價續漲而 FCF/淨利仍 <0.6，則不追"],"evidence_refs":["geo_supply_chain#0","supply_demand_durability#1"]},{"axis":"管理層前後說法（2026-07-29 對 2026-10-28）","cause":null,"prior_field":null,"side_a":"7 月 CFO：Q1 Azure 約 45%、Q1 營益率年持平、2026 曆年資本支出約 1750 億、Windows OEM 與裝置 FY27 全年高十位數衰退；CEO：M365 Copilot 付費席位逾 3000 萬。","side_b":"10 月實績：Azure 48%，營益率小升到 50%，兩項超標。資本支出降到約 1700 億，原因是第三方產能延遲，不是紀律。Windows OEM 與裝置 Q1 年減 22%，Q2 指引年減 30% 中段，並說趨勢延續全年，全年恐怕比 7 月說法差。本季未更新 Copilot 席位數。","ruling":"雲端的兌現優於承諾；裝置端的說法實質改口。資本支出下修是延後不是節省，下半財年會補回。在集體訴訟指控誇大 Copilot 採用的背景下，不再揭露 Copilot 席位，視為揭露品質退步，列入監測。","evidence_level":"逐字稿對照（一手）","settle_metric":"FY27 下半年資本支出、Windows OEM 全年衰退幅度、Copilot 席位是否恢復揭露","if_then":["若 FY27 Q2 仍不揭露 Copilot 付費席位，且 M365 商用雲年增 <17%，則 H3 記削弱，停止加碼","反向：若恢復揭露且席位季增 ≥15%，則 R5 降級"],"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"axis":"客戶集中度：年報說法對本季","cause":null,"prior_field":null,"side_a":"FY26 10-K：沒有單一客戶占營收超過一成；OpenAI 商業安排營收 241 億美元，約 7%。","side_b":"FY27 Q1 法說會分析師提問指 OpenAI 占本季營收約 11%（約 100 億美元）；應收帳款 72 億，6 月底為 60 億。","ruling":"集中度在單季已越過一成，方向是上升。採納為唯一致命點與 R1。不因 7 月 CFO「雲營收近九成來自前沿模型公司以外」而降級，因為那是全年口徑，且早於本季。","evidence_level":"10-K 一手加法說會分析師引述","settle_metric":"下一份 10-Q 關係人揭露的 OpenAI 營收與應收","if_then":["若 FY27 Q2 OpenAI 占營收 >15%，則減碼三分之一","反向：若占比回落到 8% 以下，且 RPO 剔除 OpenAI 後年增 ≥25%，則 R1 降為長期風險"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#0","customer_concentration_credit#2"]},{"axis":"反方論證：現在就加碼的最強理由","cause":null,"prior_field":null,"side_a":"Azure Q2 指引 49–50% 高於預期；FY1、FY2、FY3 共識近期分別上修 1.3%、1.9%、3.2%；以 FY2 共識 24.14 元計，本益比只有 21.6 倍，PEG 約 1.15；營業現金流年增 29%。","side_b":"成長已經反映在共識上修與股價的 +33.6% 中；還沒證實的是現金轉換，以及 OpenAI 以外需求的厚度。","ruling":"不採納加碼。約束在現金，不在營收。但如果下一季就出現 FCF/淨利 ≥0.6，接受提前加碼半份。","evidence_level":"事實表共識快照與法說會","settle_metric":"FY27 Q2 FCF/淨利","if_then":["若 FY27 Q2 FCF/淨利 ≥0.6，且 Azure 固定匯率 ≥45%，則先加碼半份，Q3 確認後補足"],"evidence_refs":["capital_markets_pricing#1","supply_demand_durability#3"]}],"triggers":[{"n":1,"text":"Azure 成長驗證","type":"假設驗證","maps_to":"H1","metric":"Azure 固定匯率年增率","threshold":"FY27 各季 ≥40%；FY28 各季 ≥30%","action":"連兩季低於門檻：停止加碼並重寫 H1","source_freq":"每季財報電話會","date":"2027-01","evidence_refs":["supply_demand_durability#3"]},{"n":2,"text":"重啟加碼：現金轉換證實","type":"估值rearm","maps_to":"H2","metric":"自由現金流÷淨利","threshold":"FY27–FY28 任連續兩季 ≥0.6","action":"加碼至前份上限","source_freq":"每季 10-Q 現金流量表","date":"2027-04"},{"n":3,"text":"OpenAI 縮減、延後或重談 Azure 承諾，或應收提列減損","type":"Single Thing","maps_to":"R1","metric":"OpenAI 營收占比、應收帳款、關係人揭露","threshold":"公開縮減承諾、應收 >100 億美元，或提列呆帳","action":"減碼一半","source_freq":"每季 10-Q 關係人附註，加上事件","date":"每季","evidence_refs":["customer_concentration_credit#2","customer_concentration_credit#3"]},{"n":4,"text":"毛利率或現金破底","type":"減碼","maps_to":"R2","metric":"Microsoft Cloud 毛利率；FY27 全年自由現金流","threshold":"毛利率 <62%，或全年 FCF 轉負，或發行普通股","action":"減碼三分之一","source_freq":"每季","date":"2027-07","evidence_refs":["geo_supply_chain#0"]},{"n":5,"text":"股價先走、現金未證：估值過熱","type":"減碼","maps_to":"價格","metric":"Fwd P/E（以 FY1 共識計）","threshold":"≥32 倍（約 640 美元），且 FCF/淨利 <0.6","action":"減碼 20%","source_freq":"每週","date":null},{"n":6,"text":"股價先跌、基本面無損：分批反買","type":"加碼","maps_to":"H1","metric":"週收盤價、Azure 固定匯率年增率、FCF/淨利","threshold":"收盤 ≤448（W104 均線），且 Azure ≥40%、FCF/淨利 ≥0.45","action":"分批反買三分之一，不是停損","source_freq":"每週，加上每季","date":null},{"n":7,"text":"反壟斷正式行動","type":"風險","maps_to":"R4","metric":"FTC 起訴、英國 CMA 認定","threshold":"FTC 正式起訴，或 CMA 認定策略市場地位並附雲端授權行為要求","action":"停止加碼並重跑研究","source_freq":"事件","date":null,"evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2"]},{"n":8,"text":"Copilot 集體訴訟進入集體認證","type":"風險","maps_to":"R5","metric":"訴訟程序","threshold":"駁回聲請未獲准，並進入集體認證","action":"停止加碼","source_freq":"事件","date":null,"evidence_refs":["lawsuit_class_action#0"]},{"n":9,"text":"兩項減碼指標同時觸發","type":"清倉","maps_to":"R1","metric":"減碼指標清單","threshold":"任兩項同時觸發（例：OpenAI 應收提列減損，且 FY27 全年 FCF 轉負）","action":"清倉","source_freq":"每季","date":null},{"n":10,"text":"下次複審","type":"複審日期","maps_to":null,"metric":"FY27 Q2 財報","threshold":"財報發布後一週內","action":"重跑研究","source_freq":"每季","date":"2027-01"}],"kill_metrics":[{"metric":"自由現金流÷淨利（季度）","bear_threshold":"連兩季 <0.35，或 FY27 全年自由現金流轉負","window":"FY27 Q2–FY28 Q4","source":"公司 10-Q、10-K 現金流量表","last_status":"warning"},{"metric":"OpenAI 營收占比與應收帳款（關係人揭露）","bear_threshold":"營收占比 >15%、應收 >100 億美元，或提列呆帳","window":"每季，至 FY28 底","source":"10-Q、10-K 關係人附註，法說會","last_status":"warning"},{"metric":"Azure 固定匯率年增率","bear_threshold":"連兩季 <30%","window":"FY27–FY28","source":"每季財報電話會","last_status":"ok"},{"metric":"Microsoft Cloud 毛利率","bear_threshold":"<62%","window":"FY27–FY28","source":"財報電話會與投影片","last_status":"ok"},{"metric":"12 個月內認列的商業 RPO 年增率","bear_threshold":"連兩季 <20%","window":"FY27–FY28","source":"CFO 每季 RPO 說明","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=26.44, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 FY27–FY28 任連續兩季自由現金流÷淨利 ≥0.6（事件錨，不設價位）；在那之前既有部位續抱、不加碼'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"沿用前份上限，不因本次上調；回撤區間未達深回撤，不另外下修","requires_critic":[],"rearm_trigger":"既有部位續抱；重啟加碼＝FY27–FY28 任連續兩季自由現金流÷淨利 ≥0.6（事件錨，不設價位）","exec_line":"續抱，不追價。現金轉換證實後才加碼到原上限；股價先跌而基本面無損，分批反買三分之一。OpenAI 縮減承諾則減碼一半；任兩項減碼指標同時觸發則清倉。"},"reasoning":{"industry":"收錢方式有兩種：一是 IT 預算支付的訂閱（M365、Windows、資安），二是業務單位按用量支付的算力與 AI（Azure、Foundry、Copilot 點數）。FY27 Q1 營收 922.8 億美元，年增 19%；營業利益 459.2 億，營益率 49.8%。Microsoft Cloud 639 億，約占營收 69%，年增加速到 30%；Azure 年增 48%。錢卡在算力供給：CFO 說客戶需求仍超過可用供給，Q2 Azure 指引 49–50% 靠的是既有機隊的效率提升，因為部分第三方 GPU 交付已延到下半財年。單點依賴：OpenAI 約占本季營收 11%（法說會 Goldman Sachs 分析師提問所述），FY26 全年約 7%（10-K 揭露 241 億美元）。供需持久性：需求面偏結構性，企業代理工作負載正在擴散，商業 RPO 6770 億美元；但供給可逆性高，瓶頸在電力與資料中心殼體（建置 18–24 個月），一旦 2027 年前後緩解，全產業產能會同時上線，供需可能翻轉。產業時鐘判 II（擴張）：需求大於供給、全產業資本支出仍在加速、token 單價與記憶體價格上行。記憶體漲價與第三方產能延遲是過熱前兆，但尚未見需求轉弱。產業態勢判雙向拉鋸：結構在轉好（需求大於供給、Azure 份額 20%→21%），其他結構變數在拉扯（美英反壟斷調查、商模由按人頭轉向按用量）。","moat":"機制是轉換成本加規模。TTM 營業利益率 47.1%，高於 ADBE 35.7%、GOOGL 33.3%、CRM 21.5%、TEAM 0.2%；公司自身 FY23 到 FY26 由 41.8% 升到 46.8%（事實表 financial_history）。毛利率 67.7% 低於純軟體同業，這是雲基礎設施組合的代價。FCF 利潤率 17.3% 落後 CRM 34.5%、ADBE 40.8%，護城河賺到的利潤沒有同比例變成現金。同業 ROIC 事實表未涵蓋，改以營益率差代理：差距為正，Microsoft 這端在擴大，同業的趨勢未知。執行面 9 分：Q1 營收、營業利益、EPS 全面超標；Azure 交出 48%，高於 7 月指引的約 45%；GB300 從到貨到上線的時間季減約 20%。定價面 8 分：M365 在 7 月漲價後，付費席位仍增 5%，token 單價也高於預期；但 E3 與單品銷售執行偏弱。兩項平均 8.5 分，加上營益率領先同業，評 A。趨勢判穩定。三條威脅都屬點對點，不扣分：前沿模型公司直接賣給企業、AI 代理壓縮按人頭計費、反壟斷針對綑綁。報酬持續期方面，投入資本事實表未涵蓋，當期 ROIC 算不出來；象限判高利益率、周轉率下滑。增量 ROIC 約 30%，再投資率約 65%，內生成長上界約 19.5%。","growth":"成長以量為主：Azure 算力與 Copilot、GitHub 的用量。價格次之：M365 7 月漲價，token 單價高於預期。併購與回購的貢獻近乎零，FY23 到 FY26 稀釋股數年減約 0.1%。三年共識 EPS 年複合 18.8%（FY2026A 17.95→FY2029E 30.09，Koyfin 快照，家數事實表未列）。內生上界約 19.5%，共識落在上界內，但只差 0.7 個百分點。FY2026A 的 GAAP EPS 年增 31.6%，營業利益只增 20.8%，基期含營業外收益；改用營業口徑，共識年複合約 22%，超出上界約 2.5 個百分點。超出的部分不來自利潤率（共識淨利率持平在約 37.6–37.7%），也不來自回購，歸為無法歸因，加註依賴 re-rate，長期信心上限為中。跑道：Azure 份額 21%，企業代理才剛開始擴散（Nadella：企業工作負載是十年的事）；Copilot 用量計費客戶季增逾 75%，Foundry 營收年增逾三倍，代理開的 PR 已占 GitHub 三分之一，第二條曲線有證據。衰退燈三盞：毛利率連兩季年減、FCF/淨利連兩年低於 0.75、EPS 年複合高於營收 6.8 個百分點。三盞同源於資本密集度上升，不是需求衰退。","governance":"FCF/淨利：FY25 0.70、FY26 0.50，FY27 Q1 約 0.51。SBC 占營收 3.4%，占營業利益 6.8%。現金去向（FY27 Q1）：營業現金流 580 億，其中現金資本支出 394 億、股利加回購 102 億、其他約 84 億，另有融資租賃 74 億不經現金流量表；四分法的完整拆分事實表未涵蓋。回購：以股利殖利率 0.697% 推算年股利約 270 億，季度股東回報 102 億中回購約 35 億，回購規模約占市值 0.36%，大致只抵掉 SBC。淨負債 694 億（含租賃）。CFO 表示 FY27 自由現金流維持為正，但會在條件合適時動用租賃以外的外部資金，債市尚未動用。","valuation":"Fwd P/E 26.07 倍（521.91÷FY1 共識 20.02），FY2 本益比 21.6 倍（÷24.14）。三年 EPS 年複合（FY2026A 17.95→FY2029E 30.09）18.8%，PEG 1.39；若基期改用營業口徑，年複合約 22%，PEG 約 1.2。trailing P/E 27.24 倍在 4 個年度端點中位於 32 分位；這不是五年分位，五年區間事實表未涵蓋。EV 對前瞻營收 9.97 倍。三個月前同一家公司以約 20.4 倍交易，這段漲幅約八成五來自倍數擴張。基本情境（FY2032E EPS 39.5 元 × 23 倍）五年價格年化約 11.7%，加股息約 12%。一年上檔約 14%（FY28E 23.8 元 × 25 倍），三年約 46%（FY30E 31.8 元 × 24 倍）。成長熄火壓力測試：三年後成長降到 15%、10%、5%，對應倍數 24、19、15 倍，股價約 767、581、438，三種情形中兩種不虧。同業 Fwd P/E 事實表未涵蓋，終端倍數只能拿公司自身前後的倍數對照。賣方平均目標價 569.45（聚合站 8 月快照，各家日期不一）只比現價高 9%，不支撐追價。","premortem":"空方最強的三個數字：FY26 FCF/淨利 0.50；Q1 自由現金流只有營業利益的 41%；OpenAI 約占本季營收 11%。論點失敗的路徑是 OpenAI 縮減承諾，同時 2027–28 年電力瓶頸解除、全產業算力過剩。Bear 情境下 EPS 五年持平、給 16 倍，股價約 352（−33%）。路徑風險：回撤區間 −30% 至 −45%，推法見情境樹的回撤說明。歷史最大回撤事實表未涵蓋，只知道 2026-01-29 單日跌約 10%，2026-07-30 曾到 390.54。訴訟與監管：Copilot 證券集體訴訟（類別期間 2025-05 至 2026-01）、FTC 與英國 CMA 調查，金額與時點事實表未涵蓋。7 月法說問答有三題迴避：資本支出的投資報酬、元件漲價對毛利的影響、開源與自訂模型的營收貢獻，都沒有量化；本季又拒絕更新 Copilot 席位數。"},"plain":{"six":{"how_it_makes_money":"Microsoft 賺的是企業 IT 預算與業務單位 AI 預算的錢。錢卡在 Azure 算力供給。Microsoft Cloud 約占營收七成且在加速，但 OpenAI 單一客戶的占比已升到約一成一。","moat":"護城河穩定：執行面在擴大，定價面持平。機制是轉換成本加規模，營益率領先所有同業 11 個百分點以上。弱點有兩個：AI 層進入門檻低，利潤也沒有同比例變成現金。","growth":"五年後跑道寬：企業 AI 代理與用量計費是第二條曲線。但衰退信號亮三盞，落到股東手上的成長要打折。","capital":"資本配置屬中段：股權稀釋控制得好，但回購收益率低，現金幾乎全部投回資本支出，自由現金流轉換率已降到五成。","valuation":"現價 521.91 要求 FY27 到 FY29 的 EPS 年增約 20%，且倍數守在 24 倍以上。營收成長我大致相信，現金轉換還沒有證據。結論是合理，但不便宜。","how_wrong":"最可能看錯的是現金轉換與 OpenAI 集中度，不是 Azure 需求。價值陷阱風險高，三盞衰退燈都源自資本支出。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 FY27–FY28 任連續兩季自由現金流÷淨利 ≥0.6（事件錨，不設價位）；在那之前既有部位續抱、不加碼","trap":"🔴","val":"🟡","moat":"A","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":521.91,"week26_return_pct":26.44,"consensus_rev_3m_pct":4.38,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026A GAAP EPS 17.95 年增 31.6%，同期營業利益只增 20.8%（事實表 financial_history 換算），差距多半來自 OpenAI 相關的營業外損益。估值錨用 FY1 前瞻共識，不受這個基期影響；EPS 與現金的落差屬資本支出報酬問題，放在 H2 處理，不列為分母爭點。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"FY27 Q2 財報：Azure 是否落在 49–50% 指引、FCF/淨利、OpenAI 營收占比","impact":"高","watch":"FCF/淨利是否 ≥0.6；Azure 固定匯率是否 ≥45%；是否恢復揭露 Copilot 席位"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"延到下半財年的第三方 GPU 產能交付，以及資本支出再加速","impact":"中","watch":"資本支出是否如期加速、Azure 成長是否跟上"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"FTC 綑綁與雲端授權調查、英國 CMA 策略市場地位調查的進展","impact":"中","watch":"是否正式起訴，或附帶行為要求"},{"date":"2026-11","date_precision":"month","type":"product","event":"GTA VI 登上 Xbox、Modern Warfare 4 假期檔期","impact":"低","watch":"Xbox 內容與服務 Q2 是否回到中至高個位數成長"}],"_projected_from":"v19"}
```
