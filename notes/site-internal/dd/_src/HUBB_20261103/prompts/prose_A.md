你是 stock-analyst v20 的**散文層（prose）agent**，標的 HUBB（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：HUBB　日期：2026-11-03　archetype：None　前份裁決：2026-05-18　A（核心候選進場，Fwd PE 22x 5Y 分位 0% + post-earnings -13% drop 創 5 年難得 entry，是 PWR 同 thesis 便宜替代品）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1678B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（481B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（991B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1514B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1422B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（1153B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1479B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2285B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4776B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2776B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1678           3725-5322      5 條（2–6 內）  
s3                  8000         481           5263-7519      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3927          7751-11073      5 條（2–6 內）  
s6                 11000        1153           6893-9847      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1479           1415-2021      3 條（2–6 內）  
s10                 5000        2285           1900-2715      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2776           2000-2224      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5822B；至少需散文≈39.18KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−43
−43%
−34%
−30
−30%
−23%
−16.24
−16.2%
−10.5%
−7%
−4%
0
0%
0.18%
0.20
0.3
0.6%
0.75
01
1
1.0
1.32%
1.32
1.5%
1.57
1.7
1.75
1.76
1.85
1.90
2
2.10
2.2
2.4
2.5
2.67
2.8
2.8%
2.9
3
03
3%
3.74
4%
4
04
4.19
4.65%
4.65
4.8%
4.90%
5%
5
05
5.15%
5.6%
5.7%
6
6%
06
7%
7
07
7.1%
7.1
7.5
08
8%
8
8.0%
8.45
8.75
8.9%
09
9
9%
9.43
10%
10
10.28
10.5%
11.0%
11%
11
11.3%
11.4
11.8%
12%
12
12.4
12.5%
13
13%
14%
14
14.3%
14.7%
14.7
15%
15
15.9%
16
16.54
17
17.1%
17.30
17.50
17.6%
17.7%
18
18%
18.22
18.4%
18.6
18.64
18.73
19
19.0
20
20%
20.2%
20.25
20.40
20.5
20.55
20.59
20.6%
20.60
20.7%
20.8%
20.86
20.9
21.8%
21.9%
22%
22
22.2
22.25%
23.0
23
23.0%
23.05
23.1
23.1%
23.2%
23.3%
23.4%
23.8
23.8%
24%
24
24.6%
24.8%
25
25.2
25.3%
25.49
25.5%
26.0%
26
27
27.1
27.1%
27.3
28
29
29%
29.4
30
30%
30.2
31
31.5
33%
33.4
35.3%
35.4%
36.5
36.8
40%
40.0%
40.1%
42
42%
44
45
49
49.5
50%
50
50.6%
51%
52
55%
56%
58.4
60%
65%
69.2
70
73.9
76.8
80%
82
90
90%
99%
100
100%
104
104%
150%
160
240%
247
250
285
299
325
330
368
392
400
401
429.56
443
450
460
479.97
480
500
504
505
546
554
600
645
765
800
876
1500
2000
2022
2024
2025
2026
2027
2028
2029
2030
2031
2033
2036
2500
3000
5000
20261103
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
{"meta":{"ticker":"HUBB","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Hubbell Incorporated"},"oneliner":"Hubbell：被公用事業與資料中心指定規格的電網元件商，EPS 財測再上調、Utility 在手訂單年初至今約增三成，但產能執行與營益率財測小降；前瞻 20.9 倍合理不便宜，等 392 美元（FY2027E 共識 17 倍）再進場。","thesis":{"H":[{"id":"H1","text":"公用事業輸配電投資周期延續，Utility 段 2027–2028 有機成長維持中高個位數，在手訂單轉為營收","2y":"FY2027 Utility 有機成長 ≥6%；Grid Infrastructure 有機 ≥8%","5y":"FY2031 Utility 段營收年複合 ≥6%（含 765kV 約 10 年 15 億美元機會，約貢獻 1 點）","10y":null,"threshold":"Utility TTM 有機成長 ≥5%","source":"季報新聞稿分部表、法說在手訂單與 book-to-bill 評論","drift_rule":"TTM 有機成長 <5% 連 2 季＝削弱；<3% 連 3 季＝反轉"},{"id":"H2","text":"調整後營益率在 FY2026 約 23.1% 基礎上擴張：價格成本生產力中性偏正、Electrical 利益率計畫與 NSI 成本協同 3–5%","2y":"FY2027 調整後營益率 ≥23.3%","5y":"FY2030 調整後營益率 ≥23.8%","10y":null,"threshold":"TTM 調整後營益率 ≥23.1%","source":"季報新聞稿；Q3 法說（2027 價格成本中性至正、增量利潤率 25–30%）","drift_rule":"TTM 較 23.1% 偏離 ≥5%（<21.9%）連 4 季＝削弱；偏離 ≥10%（<20.8%）連 6 季＝反轉"},{"id":"H3","text":"資料中心與擴產帶動 Electrical 份額提升：資料中心銷售 2027 年仍維持 20% 以上成長，占 Electrical 營收比重由約 15% 上升","2y":"FY2027 資料中心銷售年增 ≥20%；Electrical 有機 ≥8%","5y":"FY2030 資料中心占 Electrical 營收 ≥22%","10y":null,"threshold":"資料中心銷售年增 ≥20%","source":"季報法說資料中心揭露","drift_rule":"連 2 季 <15%＝削弱；連 3 季 <10%＝反轉"}],"R":[{"id":"R1","text":"大型公用事業延後輸配電資本支出，或 HUBB 自身產能（控制屋、變電站元件）跟不上，使在手訂單轉營收落後","h_ref":"H1","clock":"⚡","threshold":"Grid Infrastructure 有機成長連 2 季 <5%","evidence_refs":[]},{"id":"R2","text":"成本通膨與關稅快於漲價：價格成本生產力轉負，營益率擴張中斷（2025 年材料與關稅通膨曾吃掉約 3 個百分點毛利率）","h_ref":"H2","clock":"🔥","threshold":"價格成本生產力美元淨額連 2 季為負，且調整後營益率年減 ≥100bps","evidence_refs":["reg_tariff_export#1","competitive_share_entrants#1"]},{"id":"R3","text":"資料中心建置周期見頂、超大規模業者資本支出進入消化","h_ref":"H3","clock":"🔥","threshold":"資料中心銷售年增連 2 季 <15%","evidence_refs":[]},{"id":"R4","text":"重大併購與槓桿：NSI 30 億美元（約市值 13%）以 19 億美元優先債＋9 億美元定期貸款融資，若整合失速或去槓桿延後，利息與攤銷吃掉 EPS 增益","h_ref":"H2","clock":"🔥","threshold":"淨負債／EBITDA 2027 年底 >2.5 倍，或 NSI 營益率低於 Electrical 段平均","evidence_refs":["major_events#1","ma_merger#1"]},{"id":"R5","text":"供應鏈與貿易政策：部分電子元件供應商有限（Q3 電表代工缺料即一例），美中墨關稅與報復關稅推高成本","h_ref":"H2","clock":"⚡","threshold":"單季零件短缺遞延營收 ≥3000 萬美元，或管理層揭露關稅淨成本使營益率年減 ≥50bps","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0"]},{"id":"R6","text":"替代技術與捆綁：固態變壓器整合整流與變流功能、系統商整套出貨，可能繞過單一元件供應商","h_ref":"H1","clock":"🐢","threshold":"管理層揭露大型專案勝率低於過往，或主要公用事業客戶固態變壓器試點轉量產","evidence_refs":["substitute_technology#0"]}],"single_thing":{"description":"公用事業輸配電訂單周期轉向：Utility 段有機成長轉負且半年 book-to-bill 低於 1.0","why_fatal":"Utility 約占銷售 55%、調整後營業利益 56%，是 EPS 最大單一敏感項；轉負代表輸配電假設反轉，EPS 路徑落到 Bear（FY2029E 約 19 美元），倍數同步壓到 13–15 倍，股價約 250–330 美元","if_happens":"已持有即清倉並重跑分析；未持有則取消 392 美元建倉計畫","how_monitor":"每季新聞稿 Utility 有機成長、法說 book-to-bill 與在手訂單；2027-01 全年財測","probability":"12–24 個月約 15%（在手訂單年初至今約 +30%，短期轉負需要訂單快速崩落）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.64,"peg_fy2":1.57,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":18.22,"FY2026E":20.59,"FY2027E":23.05,"FY2028E":25.49},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（排除併購無形資產攤銷等）；FY2025A 18.22 美元由 FY2026 財測 20.40–20.60 對應年增 12–13%（Q3 法說）回推，事實表 GAAP 稀釋 EPS 為 16.54；FY2026–28E 為 Koyfin 2026-10-31 共識，家數未載（營收共識 15 位）；三年年增 11.8%"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"電網元件指定規格＋短週期多 SKU；GAAP 營益率由 2022 年 14.3% 升到 2025 年 20.7%，價格成本與公用事業資本支出周期使獲利有明顯波動"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久（偏）：變壓器與高壓斷路器交期仍至少 2–3 年（Rystad，2026-05，二手摘要）、Utility 在手訂單年初至今約 +30%、GE Vernova 稱需求強勁且持久；供給可逆性中等（Eaton、Hitachi Energy 2027 年擴產投產），資料中心段週期性較高","bargaining":{"up":"鋼、鋁、銅與電子元件；部分電子元件（螺線管、電路板、IC、電源線組）供應商有限，Q3 電表代工缺料即一例；靠每年約 3–4 點漲價轉嫁","down":"公用事業與電氣經銷商，十大客戶約 42%，無單一客戶依賴；指定規格讓轉換成本高，但公用事業支出受費率監管約束","geo":"原料與成品部分來自加拿大、中國、墨西哥與歐洲，關稅推高成本；IEEPA 關稅遭最高法院判違法後，Q3 入帳退款 3000 萬美元，後續退款時點不確定"},"profit_pool_dir":"利潤池往輸配電與資料中心配電移動（兩段 Q3 營益率 24.8%–26.0%），重工業偏軟、非住宅持平","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率；HUBB 主力為成熟電網元件，成長來自公用事業資本支出周期與資料中心配電含量提升，份額變化改以分部有機成長代理（見成長段分部表）"}},"moat":{"mechanism":"指定規格＋安裝基礎＋多 SKU 經銷與直售通路；替換需重新設計測試與上線認證","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力擴大：資料中心有機 +80% 遠超市場、Electrical 營益率年增 400bps、大型專案勝率與過往相近；定價力穩定：價格成本生產力美元中性，FY2026 營益率財測由 23.1–23.4% 小降到 23.0–23.2%；TTM 營業利益率 HUBB 20.2% 領先 ETN 17.7%、ABB 17.6%、NVT 17.1%、AYI 15.9%（同業期間截至 2026-06／08，不完全一致），只有單點無法判斷差距擴大，合併為穩定","peer_na_reason":"事實表同業對照只有毛利率、營業利益率、FCF 利潤率，未涵蓋同業 ROIC 與投入資本；以營業利益率代理，且同業期間（2026-06／08）與 HUBB（2026-09）不一致","threats":[{"level":"🟡","text":"競爭價格壓力與成本通膨：10-K 稱漲價可能無法完全抵銷成本；2025 年材料與關稅通膨約吃掉 3 個百分點毛利率，靠價格與生產力抵銷；10-K 另提 AI 等技術採用可能造成長期劣勢（未具體化）","p":"30%","evidence_refs":["competitive_share_entrants#1","reg_tariff_export#1"]},{"level":"🟡","text":"固態變壓器：NYPA 與 EPRI 2026-08 測試 1MW 機型，主攻資料中心；它吸收整流與變流功能，主要衝擊傳統變壓器，HUBB 的連接器、套管、避雷器多數仍需要，屬點對點替代","p":"10%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"模組化與捆綁趨勢（Q2 法說 CEO）：大型業者整套出貨可能把元件議價權移到系統商；HUBB 以控制屋與跨品牌組合應對","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×周轉率待證：營業利益率 20.2% 為同業最高，但 NSI 收購後商譽墊高投入資本，資產負債表事實表未涵蓋，無法計算當期 ROIC","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（線路工、承包商）、決策者（公用事業工程師）、付款者（公用事業，經費率基礎回收）三方都成立；電網老化、負載成長、資料中心併網屬「需要」而非「想要」，延後的代價是可靠度與併網排隊；Utility 在手訂單年初至今約 +30%、NEMA 六個月展望 73.9 仍遠高於 50；資料中心段需求急迫但持久性較低"},{"item":"決策層級","level":"🟢","text":"替代性要在料號規格層衡量：公用事業指定料號後，換供應商需重新設計測試與上線認證（765kV 新品例）；代理變數為大型專案勝率與過往相近、漲價 3–4 點後量仍成長（Utility 有機 +5%、變電站零組件 >20%）"},{"item":"價值鏈分配","level":"🟡","text":"元件占專案成本低，有利定價；但十大客戶約 42% 以經銷商為主、系統捆綁趨勢可能把議價權移往系統商；價格成本只維持美元中性，顯示 HUBB 目前沒有從價值鏈多拿"},{"item":"社會容忍度","level":"🟡","text":"公用事業的資本支出最終轉成電價，電價上漲受監管機關與民意審視；HUBB 漲價幅度溫和（每年約 3–4 點），未逼近經濟上限；事實表未涵蓋費率案或電價政治化的具體證據"}],"roiic":"事實表未涵蓋投入資本，無法直接計算；代理：有機擴產每季新增約 2500 萬美元營收產能（2026）→約 5000 萬美元（2027），管理層稱是報酬最高的投資；NSI 30 億美元已實現報酬未滿一年；有機增量報酬約 40%、併購約 10% 為判斷假設","reinvest_rate":"有機約 10%（FCF 約為調整後淨利 90%）；含併購 2026 年約 240%（NSI 30 億美元 ÷ 調整後稅後營業利益約 12.4 億美元），2027–28 去槓桿期併購暫停，五年平均取約 50%","endo_ceiling":9.0,"formula_note":"內生成長＝增量報酬×再投資率：有機 40%×10%≈4pp＋併購 10%×50%≈5pp，合計約 9%；調整後稅後營業利益＝FY2026E 共識營收 69.2 億美元×財測營益率中點 23.1%×(1−22.25%)≈12.4 億美元。兩個增量報酬是判斷假設，結論對假設敏感"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","HUBB":35.36,"ETN":35.9,"NVT":36.97,"AYI":50.64,"ABBN.SW":40.12,"unit":"%"},{"metric":"營業利益率","HUBB":20.21,"ETN":17.71,"NVT":17.1,"AYI":15.89,"ABBN.SW":17.6,"unit":"%"},{"metric":"FCF 利潤率","HUBB":14.07,"ETN":13.1,"NVT":11.95,"AYI":16.11,"ABBN.SW":13.29,"unit":"%"},{"metric":"研發密度","HUBB":null,"ETN":2.81,"NVT":1.84,"AYI":null,"ABBN.SW":3.86,"unit":"%"}],"competitors":[{"name":"ETN","gm":35.9,"om":17.71,"fcf_margin":13.1,"rd_intensity":2.81,"strategy_note":"規模更大、從元件做到開關設備與變壓器，南卡變壓器廠 2027 年投產；在資料中心配電是系統級競爭，營業利益率 17.7% 低於 HUBB","period":"TTM ending 2026-06-30（4季加總）"},{"name":"NVT","gm":36.97,"om":17.1,"fcf_margin":11.95,"rd_intensity":1.84,"strategy_note":"資料中心機櫃、散熱與電氣連接件與 HUBB Electrical 正面重疊，營業利益率 17.1%","period":"TTM ending 2026-06-30（4季加總）"},{"name":"AYI","gm":50.64,"om":15.89,"fcf_margin":16.11,"rd_intensity":null,"strategy_note":"照明與建築控制為主，毛利率 50.6% 最高但營業利益率 15.9%，與 HUBB 重疊在非住宅，不是輸配電對手","period":"TTM ending 2026-08-31（4季加總）"},{"name":"ABBN.SW","gm":40.12,"om":17.6,"fcf_margin":13.29,"rd_intensity":3.86,"strategy_note":"全球電網與配電設備龍頭，毛利率 40.1%、營業利益率 17.6%，在變電站與高壓設備與 Utility 段競爭，資源遠大於 HUBB","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（有機）＋併購（2026 年 NSI 約 7.5 點、DMC 約 4 點於 Utility）＋價格約 3–4 點；回購貢獻小","runway_years":"5–9","runway_post_y5":"🟡","endo_ceiling_basis":"沿用護城河段：有機（再投資率約 10%×增量報酬約 40%）約 4pp＋併購（五年平均再投資率約 50%×增量報酬約 10%）約 5pp，合計約 9%；兩個增量報酬皆為判斷假設，投入資本事實表未涵蓋","segments":[{"item":"Utility Solutions（Q3）","value":"銷售 10.28 億美元，年增 9%（有機 5%、DMC 4 點）；調整後營業利益 2.67 億、營益率 26.0%（+30bps）；FY2026 有機財測 6–7%（Q2 時 7–9%）"},{"item":"Grid Infrastructure／Grid Automation（Q3）","value":"Grid Infrastructure 有機 +8%（變電站零組件 >20%、控制屋季持平）；Grid Automation 有機 −4%（電表代工缺料，約 1500 萬美元移到 Q4，管理層預期 Q4 雙位數成長）"},{"item":"Electrical Solutions（Q3）","value":"銷售 8.45 億美元，年增 51%（有機 22%、NSI 29 點）；調整後營業利益 2.10 億、營益率 24.8%（+400bps）；FY2026 有機財測 17–18%（Q2 時 12–14%）"},{"item":"資料中心","value":"Q3 有機 >80%（Q2 約 65%）；2026 年底約占 Electrical 營收 15%；管理層預期 2027 年在更高基期上仍有吸引人的成長"},{"item":"小型終端市場","value":"天然氣、電信、電表與 AMI 約占組合 20%，管理層預期成長較溫和；Aclara 占 Utility 營收 <10%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；TTM 35.4% 與 FY2025 35.3% 持平"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"無來源顯示份額流失；資料中心有機 +80% 屬份額提升"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"漲價 3–4 點後兩段有機量仍成長"},{"signal":"EPS 年增顯著高於營收（差 >5pp）","lit":true,"evidence":"FY2022–25 GAAP EPS 年增 20.6% vs 營收 5.7%；前瞻 FY2025–27 營收年增約 14.7% 已高於 EPS 12.5%"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":false,"evidence":"2024 年 104%、2025 年 99%"},{"signal":"SBC／營收 >5% 且上升","lit":false,"evidence":"前九個月 SBC 3000 萬美元，年化約占營收 0.6%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"固態變壓器仍在 1MW 測試階段"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"同業倍數事實表未涵蓋，無法判斷"},{"signal":"維持性資本支出占 FCF >60%","lit":false,"evidence":"2026 年資本支出 1.75–1.90 億美元，2025 年 FCF 8.75 億美元"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"擴產加速：每季新增產能由約 2500 萬美元營收提高到約 5000 萬美元"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"股利","value":"TTM 殖利率 1.32%；管理層：股利持續成長"},{"item":"併購","value":"NSI 30 億美元現金（2026-06-09 交割，約市值 13%）；DMC Power 金額事實表未涵蓋"},{"item":"融資","value":"19 億美元優先債（4.65% 2031、4.90% 2033、5.15% 2036）＋9 億美元定期貸款；淨負債 49.5 億美元，淨負債／EBITDA 約 2.9 倍"},{"item":"去槓桿","value":"Q2 法說：24–30 個月內償還大部分債務；Q3 法說重申兩年去槓桿，並稱將帶來 2027 年 EPS 增益"},{"item":"資本支出","value":"2026 年 1.75–1.90 億美元，占營收 2.5–3%，擴產每季新增約 2500 萬美元營收產能"},{"item":"回購","value":"去槓桿期只做小額；Q3 稀釋股數因過去回購略降"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"NSI 30 億美元 2026-06 交割，已實現報酬未滿一年；管理層預估 2026 年 EPS 增益約 0.20 美元、整合超前；融資成本 4.65–5.15%；投入資本與 WACC 事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"去槓桿期只做小額回購；以前瞻本益比 20.86 倍計盈餘殖利率約 4.8%，需 10 年期殖利率 <2.8% 才過；10 年期殖利率事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"前九個月 SBC 3000 萬美元，年化約占市值 0.18%；Q3 稀釋股數因過去回購略降","grade":"過"}]},"valuation":{"basis":"Fwd P/E（FY2026E 調整後 EPS 共識）＋PEG；EV/S 與 trailing P/E 年度端點分位輔助","tier":"美國電氣與電網設備品質股","peers":{"expanded":false,"reason":"事實表同業對照只有利益率，未涵蓋同業前瞻本益比或 EV/S，無法建倍數對照；終端倍數以自身前瞻倍數與成長熄火測試錨定"},"fwd_pe":20.86,"peg":1.76,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"PEG 1.76 落 1–2 合理區；前瞻 20.9 倍、FY2027E 18.6 倍；Base 五年年報酬約 9%（中段）；五年連續分位資料不足（只有 4 個年度端點：P/E 44 分位、EV/S 82 分位）→ 合理，不便宜也不貴。短期上行＝FY2027E Base EPS 23.0 美元×20 倍＝460 美元（+7.1%）；中期＝FY2029E 27.3 美元×20 倍＝546 美元（+27.1%）","upside_short_pct":7.1,"upside_mid_pct":27.1},"trap_analysis":{"verdict":"🟡","label":"低度陷阱：歷史 EPS 增速靠利益率回升，前瞻已與營收同步"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Utility 有機財測年內由 7–9% 降到 6–7%，控制屋擴產不順、電表代工缺料；2022 年 GAAP 營益率曾低至 14.3%、EPS 9.43 美元","assumption":"在手訂單（年初至今 +5 億美元）能在 2027–28 轉成營收，公用事業不因電價壓力延後資本支出","consequence":"2028 年起 Utility 有機轉負、EPS 回落到約 19 美元、倍數 15 倍，五年後股價約 285–330 美元（−23%～−34%）","ruling":"部分採納：Q3 下修主因在供給端，訂單仍創高；但周期性真實存在，Bear 機率定 30%，與唯一致命點是同一件事","watch":"Utility 有機成長、book-to-bill、2027-01 財測","evidence_refs":["geo_supply_chain#0","end_markets#1"],"fact_refs":["f_kpi0_net_sales_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"NSI 30 億美元（約市值 13%）以 19 億美元優先債（4.65–5.15%）＋9 億美元定期貸款支付，淨利息費用增加約 1.7 億美元；GAAP 營益率 Q3 年減 20bps；2025 年材料與關稅通膨吃掉約 3 個百分點毛利率；原料與成品來自加中墨歐，有關稅與報復關稅風險","assumption":"NSI 增量報酬高於融資成本，價格可持續轉嫁通膨與關稅","consequence":"營收高成長但利息、攤銷與成本通膨稀釋每股盈餘，FCF 兩年優先還債，股東回報延後","ruling":"部分採納：NSI 整合超前且提升營益率（Q3 法說），但已實現報酬未滿一年；資本配置只評中等，不給溢價倍數，Base 終端 20 倍","watch":"淨負債／EBITDA、NSI 營益率、價格成本生產力","evidence_refs":["major_events#1","ma_merger#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"],"fact_refs":["f_net_debt_m","f_kpi2_gaap_operating_income_ma"]},{"view":"價格已反映太多","evidence":"EV/S 4.19 倍在 4 個年度端點中位於 82 分位；Q3 財測上調僅與共識相當，財報當日跌約 6%","assumption":"市場會繼續給 20 倍左右的前瞻本益比","consequence":"若市場把 HUBB 當周期高點的電氣設備股，倍數回到 15–17 倍，即使 EPS 達共識，三年報酬接近零","ruling":"部分採納：前瞻 20.9 倍、PEG 1.76 只是合理，因此等 17 倍；但 trailing P/E 44 分位不支持嚴重高估，且股價已較 52 週均線低約 10%","watch":"前瞻本益比、共識修正","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_ev_s_percentile","f_pe_percentile","f_fwd_pe_latest","f_ma_w52"]},{"view":"論點失敗","evidence":"固態變壓器 2026-08 已做 1MW 測試、主攻資料中心；10-K 稱 AI 等技術採用可能造成長期競爭劣勢；系統捆綁趨勢","assumption":"HUBB 的元件在新架構中仍被需要","consequence":"若資料中心配電改走固態與直流整合，Pin & Sleeve 與部分配線元件含量下降，資料中心成長熄火","ruling":"暫時反駁：固態變壓器較高電壓應用仍需工程工作，HUBB 已推 800V 直流用 Pin & Sleeve；屬 10 年尺度風險","watch":"資料中心含量、主要客戶固態變壓器試點是否轉量產","evidence_refs":["substitute_technology#0","competitive_share_entrants#1"],"fact_refs":[]}],"max_dd":{"lo":-43,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 479.97 → 本次 429.56（-10.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=479.97","side_b":"本次 price_at_dd=429.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 479.97 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 479.97 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 479.97 美元：Bull 價 876、Bear 價 330，五年期望值 +25.3%，基準年化 5.6%，不對稱比 2.2","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.2。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 479.97 美元：五年期望值 +25.3%，基準年化 5.6%，不對稱比 2.2","side_b":"本次情境、股價 429.56 美元：五年期望值 +40.0%，基準年化 8.0%，不對稱比 3.74","ruling":"再換股價、情境不動：起點價下跌 10.5%，五年期望值多 14.7 個百分點，基準年化多 2.4 個百分點，不對稱比由 2.2 升到 3.74。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"產業態勢三軸（一致判斷）","cause":null,"prior_field":null,"side_a":"A 競爭：大型專案勝率與過往相近（Q2 法說），HUBB 營業利益率為同業最高，未見惡化；C 其他：IEEPA 關稅退款入帳但美中墨關稅仍在、NSI 重大併購、系統捆綁與固態變壓器","side_b":"B 結構與持久度：Utility 在手訂單年初至今約 +30%、變壓器與高壓斷路器交期仍 2–3 年、GE Vernova 稱需求強勁且持久","ruling":"結構性轉好中（B 軸），C 軸關稅與併購屬成本與資本結構的拉鋸，不改方向","evidence_level":"一手法說＋二手產業摘要","settle_metric":"Utility book-to-bill 與在手訂單","if_then":["若 2027 上半年 Utility book-to-bill 仍 >1.0：維持結構性轉好判斷","若 book-to-bill <1.0 連兩季：改判雙向拉鋸並把 Bear 機率調到 40%"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#5","end_markets#2","reg_tariff_export#0"]},{"axis":"Utility 需求與財測下修","cause":null,"prior_field":null,"side_a":"Q3（2026-10-27，CFO Capozzoli）Utility 有機財測降到 6–7%，Q2（2026-07-28，CFO）為 7–9%；Grid Automation −4%、控制屋季持平","side_b":"同場 CEO Bakker：在手訂單年初至今增 5 億美元以上（約 +30%），變電站零組件 >20%，下修主因是電表代工缺料與控制屋擴產爬坡","ruling":"可調和（程度差異）：需求未轉弱，問題在供給與產能執行；管理層「一次性、暫時」的歸因不採信也不否定，標未證並設期限；下修距今不到一季、FY2027 共識 23.05 美元未變，可能尚未完全反映，加碼凍結到 2027-01 財測","evidence_level":"一手逐字稿","settle_metric":"2026 Q4 Grid Automation 成長、2027 上半年 Utility 有機成長","if_then":["若 2026 Q4 Grid Automation 未達管理層所說的雙位數成長：缺料一次性歸因證偽，Bear 機率上調 5 點","若 2027 上半年 Utility 有機連 2 季 <3%：減碼一半","反向：若 2027 上半年 Utility 有機 ≥7%：Base 機率維持、解除加碼凍結"],"evidence_refs":["geo_supply_chain#0","end_markets#1"]},{"axis":"營益率財測與 Q2 承諾","cause":null,"prior_field":null,"side_a":"Q2（2026-07-28，CFO）：全年調整後營益率 23.1–23.4%，下半年 Electrical 利益率回到擴張","side_b":"Q3（2026-10-27，CFO）：全年 23.0–23.2%，Q4 Utility 營益率年減（價格成本中性、成長投資、約 500 萬美元 IEEPA 客戶補償遞延）；Electrical Q3 +400bps 有兌現","ruling":"可調和：EPS 財測仍由 20.25–20.55 上調到 20.40–20.60，營益率小降來自通膨與成長投資；記為營益率假設削弱的早期警示，不改方向","evidence_level":"一手逐字稿","settle_metric":"FY2027 調整後營益率財測（2027-01）","if_then":["若 FY2027 財測營益率 ≥23.3%：營益率假設維持","若 <23.0%：營益率假設削弱，Base EPS 下修 3% 並停止加碼"],"evidence_refs":["reg_tariff_export#1","competitive_share_entrants#1"]},{"axis":"現在就買 vs 等 392 美元（裁決）","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：EPS 財測年內兩度上調，FY2027E 只要 18.6 倍；在手訂單創高、資料中心 +80%、2027 擴產翻倍到每季約 5000 萬美元營收、去槓桿帶來 EPS 增益；賣方目標價均值 504–554 美元；等 17 倍可能等不到","side_b":"等價的理由：Base 五年年報酬約 9% 只在中段；股價在 52 與 104 週均線之下；Utility 執行不順、Q4 營益率年減；距 17 倍只差約 9%，進場價改善可把 Base 年報酬推到約 11%","ruling":"不可調和（方向相反），選等價：依據是 Base 報酬落在中段、Bear 機率 30%，價格改善 9% 對報酬的影響大於錯過的成本","evidence_level":"情境推估＋一手財測","settle_metric":"股價 vs 392 美元；2027-01 財測","if_then":["若股價 ≤392 美元且 Utility 有機未連 2 季 <3%：重跑分析後建首倉（正常部位一半）","若股價續跌但基本面無損（訂單仍增）：分批反買，不停損","反向：若 2027-01 財測 Utility 有機 ≥6%、價格成本為正而股價 ≤450 美元：直接建首倉，不再等 392 美元","若股價先漲到 480 美元以上但財測未出：不追"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"前份進場評級與估值依據","cause":"方法變動","prior_field":["signal"],"side_a":"前份（2026-05-18，股價 479.97 美元）：評級 A，依據為前瞻本益比約 22 倍、五年分位 0%、財報後急跌","side_b":"本次評級 B：事實表只有 4 個年度端點（trailing P/E 44 分位、EV/S 82 分位）與 2026-05 起的前瞻短窗，五年分位 0% 無法驗證；改用五年情境樹後，Base 年報酬約 9%（以前份價位算約 7%），屬中段","ruling":"採本次：股價雖跌 10.5%、三項假設皆未破，但前份的便宜論據缺證據；評級降一級是方法所致，不是基本面轉壞","evidence_level":"事實表估值歷史","settle_metric":"前瞻本益比 vs FY2027E 17 倍","if_then":["若股價 ≤392 美元：評級回到可進場並重跑分析"],"evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份估值結論：合理（🟡），股價 479.97 美元，前份所述前瞻約 22 倍","side_b":"本次：合理（🟡），股價 429.56 美元（−10.5%），前瞻本益比 20.9 倍、PEG 1.76","ruling":"價格下跌改善報酬但未跨出合理區，估值結論不變","evidence_level":"事實表","settle_metric":"前瞻本益比","if_then":["若 FY2027E 本益比 ≤17 倍：估值改判偏便宜"],"evidence_refs":[]},{"axis":"陷阱風險","cause":"方法變動","prior_field":["trap"],"side_a":"前份：陷阱風險低（🟢）","side_b":"本次：低度（🟡），十類衰退信號逐項檢查亮 1 項（FY2022–25 EPS 年增 20.6% vs 營收 5.7%）","ruling":"差異來自逐項檢查而非新利空；該信號源自 2022 年利益率低點回升，前瞻已收斂","evidence_level":"事實表財務歷史","settle_metric":"前瞻兩年營收與 EPS 增速差","if_then":["若 FY2027 EPS 增速再高於營收增速 5pp 以上：維持低度並檢查利益率持續性"],"evidence_refs":[]},{"axis":"前份未記錄欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位皆為空（未記錄）","side_b":"本次：護城河方向持平（→）、五年後成長空間中等（🟡）、類型品質複利成長、中循環、機率 25／45／30、最大回撤 −30%～−43%","ruling":"新增欄位是格式變動，不是判斷翻轉","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"行動門檻：清倉、減碼與重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設（kill_metrics 與 rearm_trigger 皆為空）","side_b":"清倉：Utility 有機成長轉負且半年 book-to-bill <1.0；減碼：Grid Infrastructure 有機連 2 季 <5%，或價格成本連 2 季為負且營益率年減 ≥100bps；重新進場：股價 ≤392 美元（FY2027E 共識 17 倍）","ruling":"前份只有風險描述沒有行動門檻，本次補上；門檻取自本次情境與分部揭露","evidence_level":"方法","settle_metric":null,"if_then":["若任一清倉條件成立：清倉並重跑分析","若任一減碼條件成立：減碼一半"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"公用事業輸配電訂單周期轉向：Utility 段有機成長轉負且半年 book-to-bill 低於 1.0","ruling":"新設；Utility 約占銷售 55%、調整後營業利益 56%，是 EPS 最大單一敏感項，與反證「論點失敗」視角一致","evidence_level":"一手分部揭露","settle_metric":"Utility 有機成長、book-to-bill","if_then":["若發生：清倉並重跑分析"],"evidence_refs":[]},{"axis":"風險減碼門檻調整","cause":"新證據","prior_field":["thesis.R"],"side_a":"前份：R1 Grid Infrastructure 年增連 2 季 <5%；R2 Utility 調整後營益率連 4 季 <20%；R3 資料中心年增連 2 季 <20%（三項至今皆未觸發：Q3 Grid Infrastructure 有機 +8%、Utility 營益率 26.0%、資料中心 +80%）","side_b":"本次：R1 門檻不變但改看有機（剔除 DMC 併購）；R2 改為價格成本連 2 季為負且營益率年減 ≥100bps 即減碼；R3 改為資料中心年增連 2 季 <15% 停止加碼","ruling":"R2：Utility 營益率 26.0% 距 20% 太遠形同不會觸發，Q3 法說顯示通膨與價格成本才是利益率主風險；R3：資料中心 Q3 有機 +80%、基期大增，20% 會因比較基期機械觸發，改用前份資料中心假設自己的削弱線 15%","evidence_level":"一手逐字稿","settle_metric":"季報分部揭露","if_then":["若 R2 新門檻成立：減碼一半","若 R3 新門檻成立：停止加碼"],"evidence_refs":["reg_tariff_export#1"]}],"triggers":[{"n":1,"text":"股價回到 FY2027E 共識 EPS 的 17 倍","type":"估值rearm","maps_to":"H1","metric":"收盤價","threshold":"≤392 美元","action":"重跑分析，通過即建首倉（正常部位一半）","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"2027 年全年財測驗證輸配電周期","type":"假設驗證","maps_to":"H1","metric":"FY2027 Utility 有機成長財測","threshold":"≥6%；<4% 視為警訊","action":"≥6% 且價格成本為正：股價 ≤450 美元可直接建首倉；<4%：停止加碼並上調唯一致命點機率","source_freq":"年度財測","date":"2027-01","evidence_refs":[]},{"n":3,"text":"營益率擴張驗證","type":"假設驗證","maps_to":"H2","metric":"FY2027 調整後營益率財測","threshold":"≥23.3%","action":"<23.0%：營益率假設削弱，Base EPS 下修 3%","source_freq":"年度財測","date":"2027-01","evidence_refs":["reg_tariff_export#1"]},{"n":4,"text":"公用事業資本支出延後或自身產能跟不上","type":"風險","maps_to":"R1","metric":"Grid Infrastructure 有機成長","threshold":"連 2 季 <5%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":[]},{"n":5,"text":"成本通膨快於漲價","type":"風險","maps_to":"R2","metric":"價格成本生產力美元淨額；調整後營益率年變化","threshold":"連 2 季為負且營益率年減 ≥100bps","action":"減碼一半","source_freq":"季報法說","date":null,"evidence_refs":["reg_tariff_export#1","competitive_share_entrants#1"]},{"n":6,"text":"資料中心周期見頂","type":"風險","maps_to":"R3","metric":"資料中心銷售年增","threshold":"連 2 季 <15%","action":"停止加碼；連 3 季 <10% 減碼三分之一","source_freq":"季報法說","date":null,"evidence_refs":[]},{"n":7,"text":"去槓桿延後或 NSI 整合失速","type":"風險","maps_to":"R4","metric":"淨負債／EBITDA；NSI 營益率","threshold":"2027 年底 >2.5 倍，或 NSI 營益率低於 Electrical 段平均","action":"停止加碼；兩者同時成立減碼一半","source_freq":"年報、季報法說","date":"2027-12","evidence_refs":["major_events#1","ma_merger#1"]},{"n":8,"text":"關稅或零件短缺吸收失敗","type":"風險","maps_to":"R5","metric":"零件短缺遞延營收；管理層揭露的關稅淨成本","threshold":"單季遞延 ≥3000 萬美元，或關稅淨成本使營益率年減 ≥50bps","action":"停止加碼；連 2 季成立減碼三分之一","source_freq":"季報法說","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0"]},{"n":9,"text":"公用事業輸配電訂單周期轉向","type":"Single Thing","maps_to":"Single Thing","metric":"Utility 有機成長；半年 book-to-bill","threshold":"有機轉負且 book-to-bill <1.0","action":"清倉並重跑分析","source_freq":"季報法說","date":null,"evidence_refs":[]},{"n":10,"text":"投資人日更新長期目標（Centralia, Missouri）","type":"複審日期","maps_to":"H1","metric":"長期有機成長與營益率目標","threshold":"有機目標維持或上調到中個位數以上","action":"重跑分析","source_freq":"一次性","date":"2027-03-04","evidence_refs":[]},{"n":11,"text":"替代技術或系統捆綁繞過元件","type":"風險","maps_to":"R6","metric":"主要客戶固態變壓器量產採用；大型專案勝率","threshold":"管理層揭露勝率低於過往，或主要客戶試點轉量產","action":"停止加碼並重評護城河","source_freq":"法說","date":null,"evidence_refs":["substitute_technology#0"]}],"kill_metrics":[{"metric":"Utility 段季度有機成長＋半年 book-to-bill","bear_threshold":"有機轉負且 book-to-bill <1.0（清倉）","window":"2027Q1–2028Q4","source":"季報新聞稿分部表、法說","last_status":"ok"},{"metric":"Grid Infrastructure 有機成長","bear_threshold":"連 2 季 <5%（減碼一半）","window":"逐季，至 2028Q4","source":"季報法說","last_status":"ok"},{"metric":"全公司調整後營益率年變化＋價格成本生產力","bear_threshold":"連 2 季年減 ≥100bps 且價格成本為負（減碼一半）","window":"逐季","source":"季報新聞稿、法說","last_status":"warning"},{"metric":"淨負債／EBITDA","bear_threshold":"2027-12 仍 >2.5 倍（停止加碼）","window":"至 2027-12","source":"10-K、法說","last_status":"unknown"},{"metric":"資料中心銷售年增","bear_threshold":"連 2 季 <15%（停止加碼）","window":"2027 全年","source":"季報法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Utility 有機財測下修（7–9%→6–7%）與 Q4 營益率年減讀成需求轉弱；但下修來自電表代工缺料與控制屋產能爬坡，Utility 在手訂單年初至今增 5 億美元以上（約 +30%），變電站零組件成長 >20%"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-16.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='價格錨：收盤 ≤392 美元（FY2027E 共識 EPS 23.05 美元×17 倍，Base 年報酬升到約 11%）才建首倉；例外：2027-01 財測證實 Utility 有機 ≥6% 且價格成本為正時，股價 ≤450 美元也可建首倉；其餘情況不追'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"收盤 ≤392 美元（FY2027E 共識 EPS 23.05×17 倍）且 Utility 有機成長未連 2 季 <3%，重跑分析後建首倉","exec_line":"首倉為正常部位一半，392 美元與 368 美元（16 倍）各一批；跌破但基本面無損就分批反買，不停損；加碼須等 2027-01 財測確認"},"reasoning":{"industry":"收錢方式：連接器、套管、避雷器、開關、配線器材、Pin & Sleeve 等多 SKU 元件，經電氣經銷商或直售公用事業，短週期出貨。Q3 FY2026 銷售 18.73 億美元（年增 24.6%，有機 11.3%、併購約 13 點），調整後營益率 25.5%（年增 160bps），GAAP 營益率 21.8%（年減 20bps，差距主要是併購無形資產攤銷）。分部：Utility 10.28 億美元（有機 +5%，營益率 26.0%）、Electrical 8.45 億美元（有機 +22%，NSI 貢獻 29 點，營益率 24.8%）；資料中心 Q3 有機 >80%，2026 年底約占 Electrical 營收 15%。產業時鐘判 II 擴張：Utility 在手訂單年初至今增 5 億美元以上，管理層稱輸配電在多年投資周期早期，變壓器交期仍 2–3 年；尚未見供給大量釋出或價格回落，但重工業偏軟、Eaton 與 Hitachi Energy 擴產 2027 年投產。供需持久度：輸配電段偏結構性持久（老化電網、負載成長、資料中心併網），資料中心段週期性較高，供給可逆性中等。單點依賴：無單一客戶依賴，十大客戶約占 42%（通路以經銷商為主）；供給端部分電子元件供應商有限，Q3 電表代工廠缺料使約 1500 萬美元營收遞延到 Q4，是集中度風險的實例。Q2 法說兩題未正面回答（扣除關稅退款後 Electrical 利益率、book-to-bill 下半年交貨拆分），記為資料缺口。","moat":"機制：公用事業與承包商在設計圖上指定品牌料號，換供應商要重新做設計測試（765kV 新品需內部與第三方測試，Q3 法說），換掉的成本遠高於元件占專案成本。方向證據：執行力擴大（資料中心有機 +80% 遠超市場，靠含量提升、新品與擴產；Electrical 營益率年增 400bps；大型專案勝率與過去相近，Q2 法說）；定價力穩定（漲價約 3–4 點只抵銷成本通膨，價格成本生產力美元中性，FY2026 營益率財測由 23.1–23.4% 降到 23.0–23.2%；10-K 自承競爭價格壓力可能使漲價無法完全抵銷成本）。同業 TTM 營業利益率：HUBB 20.2%、ETN 17.7%、ABB 17.6%、NVT 17.1%、AYI 15.9%；同業 ROIC 事實表未涵蓋，差距是否擴大無法驗證，因此合併分不給到 8。評分：執行力 8、定價力 7，等級 B。四檢查點：需求基礎值與決策層級正面，價值鏈分配（經銷商集中、系統捆綁趨勢）與社會容忍度（電價政治壓力）中性。增量報酬：投入資本事實表未涵蓋，有機擴產管理層稱報酬最高，NSI 30 億美元已實現報酬未滿一年；內生成長上界估約 9%。","growth":"成長組成：2026 年有機 10–11%（量為主、價格約 3–4 點）、NSI 約 7.5 點、DMC Power 約 4 點（Utility 段）；2027 年管理層稱有機至少中個位數、價格成本中性至正、增量利潤率 25–30%，加上去槓桿利息節省與 NSI 協同（成本 3–5%、銷售 2–3%）。共識三年 EPS 年增 11.8%（FY2025A 調整後約 18.22 美元→FY2028E 25.49 美元；基期由 FY2026 財測年增 12–13% 回推），營收 FY2025 58.4 億→FY2026E 69.2 億（+18.4%）→FY2027E 76.8 億（+11.0%）。內生上界約 9%（見護城河段推導），缺口約 2.8pp，歸因於營益率擴張（Electrical 利益率計畫、增量利潤率高於平均利益率）與去槓桿（淨利息費用增加約 1.7 億美元，兩年內還債），屬可歸因，不依賴倍數重估；Base 情境 EPS 年增 8.9% 落在上界內。成長空間：管理層稱輸配電在多年周期早期，765kV 約 10 年 15 億美元機會（約 1 點成長）、Pin & Sleeve 800V 新品；事實表未涵蓋滲透率，核心元件已是領先供應商，五年後成長回到公用事業資本支出周期，判中等。衰退信號十類亮 1 項：FY2022–25 GAAP EPS 年增 20.6% 遠高於營收 5.7%（差 15pp），來自 2022 年利益率低點回升；前瞻兩年營收增速已高於 EPS，屬歷史性亮燈。","governance":"現金去向：股利（TTM 殖利率 1.32%，持續成長）、併購（NSI 30 億美元，2026-06-09 交割；DMC Power 金額事實表未涵蓋）、資本支出（2026 年 1.75–1.90 億美元，占營收 2.5–3%）、回購（去槓桿期只做小額）。債務：19 億美元優先債（2031 年 4.65%、2033 年 4.90%、2036 年 5.15%）＋9 億美元定期貸款，淨負債 49.5 億美元，收購後淨負債／EBITDA 約 2.9 倍，管理層承諾 24–30 個月內大幅去槓桿。SBC 前九個月 3000 萬美元，年化約占營收 0.6%，稀釋股數因過去回購略降。營運槓桿：Q3 營收年增 24.6%、調整後營業利益年增 33%，未見壓縮；GAAP 營業利益年增約 24%，與營收差約 1pp。計分：併購增量報酬未滿一年無法判定；回購以現價盈餘殖利率約 4.8% 計，需 10 年期殖利率低於 2.8% 才過，判不過（10 年期殖利率事實表未涵蓋）；SBC 稀釋過。","valuation":"前瞻本益比 20.86 倍（FY2026E 20.59 美元）、FY2027E 18.6 倍；PEG 1.76（三年 EPS 年增 11.8%），落在合理區。trailing P/E 25.2 倍在 4 個年度端點中位於 44 分位、EV/S 4.19 倍在 82 分位（NSI 舉債墊高 EV），五年連續分位事實表未涵蓋，前份「五年分位 0%」無法驗證。成長熄火測試（以 FY2028E 25.49 美元為起點，第 4 年成長降到 15%／10%／5%，倍數 22／18／15 倍）→ 645／505／401 美元，相對現價 +50%／+18%／−7%，三項過兩項；Bear 倍數 15 倍取自降到 5% 那一格。賣方目標價：Benzinga 14 位均值 504 美元（325–600）、MarketBeat 554 美元，高於現價 17–29%，與本次「等價」方向相反，但全距 1.85 倍、聚合站數字不一（另一來源約 443 美元），不調高信心。分母：FY2026 調整後 EPS 含 IEEPA 關稅退款淨效益約 2000 萬美元（約每股 0.3 美元、占 1.5%），不構成爭議。","premortem":"反證三視角見反證紀錄（論點失敗：公用事業周期轉向；股東經濟變差：併購舉債與成本通膨稀釋；價格已反映：EV/S 分位偏高）。衰退信號亮 1 項（歷史 EPS 增速遠高於營收，來自利益率回升），判低度陷阱。最大回撤推估 −30%～−43%：上緣＝EPS 停在 FY2027E 約 23 美元、倍數壓到 13 倍（約 299 美元）；下緣＝Bear 路徑 EPS 低點 FY2029E 19.0 美元×13 倍（約 247 美元）；事實表未涵蓋歷史最大回撤，但 2022 年 GAAP 營益率曾低至 14.3%，顯示獲利波動真實存在。動能：26 週 −16.2%、RSI 36.8，股價低於 52 與 104 週均線但高於 250 週均線，非過熱。"},"plain":{"six":{"how_it_makes_money":"賺公用事業輸配電與資料中心／工業配電的錢：Utility 段約占 Q3 銷售 55%、調整後營業利益 56%，錢卡在「被公用事業工程師與電氣承包商指定規格的短週期元件」這一節點。","moat":"護城河方向持平（→）：機制是「指定規格＋安裝基礎＋多 SKU 經銷通路」，執行力在擴大、定價力只是穩定；營業利益率 20.2% 為五家同業最高，但只有單點對照，無法證明差距在擴大。","growth":"五年後成長空間中等（🟡）：輸配電多年周期與 765kV、800V 資料中心新品撐得住中個位數以上有機成長，但核心元件份額已高、第二曲線規模只約 1 點成長，第五年後回到周期驅動。","capital":"資本配置中等：現金轉換率高（2025 年 FCF／淨利 99%，2026 年指引約為調整後淨利 90%），但 2026 年以約 28 億美元新債撐起 30 億美元 NSI 收購，報酬尚待驗證，未來兩年現金優先還債。","valuation":"現價 429.56 美元要求未來五年調整後 EPS 年增約 9%、本益比守在 20 倍左右，才換得約 9% 年報酬（含股息）；EPS 這半我信，但價格只算合理，不夠便宜到值得在 2027 財測前搶進。","how_wrong":"看錯的最可能方式是周期：把多年輸配電與資料中心順風當成永久，2028 年後公用事業資本支出放緩，EPS 回落、倍數同步收縮；陷阱風險低度（🟡）。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Utility 有機財測下修（7–9%→6–7%）與 Q4 營益率年減讀成需求轉弱；但下修來自電表代工缺料與控制屋產能爬坡，Utility 在手訂單年初至今增 5 億美元以上（約 +30%），變電站零組件成長 >20%","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"價格錨：收盤 ≤392 美元（FY2027E 共識 EPS 23.05 美元×17 倍，Base 年報酬升到約 11%）才建首倉；例外：2027-01 財測證實 Utility 有機 ≥6% 且價格成本為正時，股價 ≤450 美元也可建首倉；其餘情況不追","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":429.56,"week26_return_pct":-16.24,"consensus_rev_3m_pct":0.73,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 調整後 EPS 含 IEEPA 關稅退款淨效益約 2000 萬美元（Q2 法說，稅後約每股 0.3 美元、占約 1.5%）；GAAP 與調整後差距（17.30–17.50 vs 20.40–20.60）主要為併購無形資產攤銷，屬常規調整，不是爭點"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 全年財測（含資料中心與 Utility 有機成長）","impact":"高","watch":"Utility 有機 ≥6%、價格成本為正、營益率 ≥23.3%"},{"date":"2027-03-04","date_precision":null,"type":"guidance","event":"投資人日（Centralia, Missouri），更新長期成長與利益率框架","impact":"中","watch":"長期有機目標是否上調"},{"date":"2027-03","date_precision":"quarter","type":"capacity","event":"擴產節奏由每季約 2500 萬美元營收翻倍到約 5000 萬美元","impact":"中","watch":"控制屋與變電站元件出貨季增"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"首個 765kV 專案出貨","impact":"低","watch":"765kV 管線與指定規格進度"}],"_projected_from":"v19"}
```
