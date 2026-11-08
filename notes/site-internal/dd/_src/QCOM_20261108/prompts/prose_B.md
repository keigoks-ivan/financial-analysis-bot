你是 stock-analyst v20 的**散文層（prose）agent**，標的 QCOM（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：QCOM　日期：2026-11-08　archetype：None　前份裁決：2026-07-30　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1921B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（787B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1003B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1417B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（913B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（695B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（844B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2268B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3595B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3371B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1921           3555-5079      5 條（2–6 內）  
s3                  8000         787           5049-7213      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3333          8167-11667      5 條（2–6 內）  
s6                 11000         695          7213-10305      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         844           1859-2656      5 條（2–6 內）  
s10                 5000        2268           1912-2732      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3371           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5076B；至少需散文≈39.92KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−46%
−45%
−35
−35%
−23.81
−23.8%
0
0.4
0.50
0.5
0.6
0.63
0.75
1
$1.0
1%
1.03
1.1
1.13
1.23
1.6%
1.7
2
02
2.15
2.19
2.25
2.31
2.35
2.4
2.64
3
3%
03
3.5%
3.67
4%
4
04
4.3
4.5
4.9%
5
05
5%
5.93
6
6.0
6%
06
6.5
7
07
08
8
8.5%
8.73
8.8
9
09
9.2
9.5
9.6
9.85
$10
10%
10
10.16
10.4
10.5
10.53
10.73
10.8
10.9%
11
11.26
11.4
11.5%
12%
12
12.70
12.7
12.85
12.87
12.9%
13
13%
13.0
13.1%
13.3%
13.4
13.9%
14
14.4%
15
15%
15.0
15.1%
15.5%
16
16%
16.28
16.3
16.8
17%
17.84
18.0
18
18%
18.2
18.5
18.9
19%
19
19.7
19.9
20
20%
20.1%
21.2
22%
22
23%
23
23.8%
24
24%
26
26%
26.5%
27%
28%
28.6%
29
29.0%
30%
31%
31.5%
32%
32
32.5%
35%
35
36
37
38%
40%
40
42
44.3
45%
45
46%
46
46.3%
48
48%
48.5%
49%
49
50%
50
51.4
53.1%
54
55%
55.4%
57.0%
59
60%
65%
65.2%
68%
70
70%
75.0%
76.7%
80
83.1
86.5
86.6
89%
90
100
100%
104.4
108
110
115
115.5
128.2
135
136.3
140
148.4
150%
150
165
165.41
195
215
217
320
387
400
432
650
2026
2027
2028
2454
20261108
1,783
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
{"meta":{"ticker":"QCOM","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"QUALCOMM Incorporated"},"oneliner":"授權續約解除最大不確定，車用超標，但手機仍在縮、毛利未修復，資料中心 50 億美元集中在兩家客戶；現價 16 倍看的是非 GAAP 盈餘，先等 3 月季資料中心實績再動手。","thesis":{"H":[{"id":"H1","text":"資料中心與車用補上 Apple 退場：FY27 非手機 QCT 營收年增逾 60%，其中資料中心達 50 億美元；FY29 非手機至少 320 億美元（公司目標 400 億打八折）。","2y":"FY27 資料中心 ≥50 億美元、年底跑率約 70 億；FY28 資料中心 ≥80 億美元。","5y":"FY29 資料中心 ≥110 億美元；FY31 資料中心占總營收 ≥20%。","10y":null,"threshold":"FY27 資料中心 ≥50 億美元；FY29 非手機 ≥320 億美元。","source":"公司季報與法說分部揭露，每季。","drift_rule":"TTM 較路徑偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉。"},{"id":"H2","text":"漲價落地後 QCT 基礎毛利率回到 48% 以上，資料中心對毛利率的稀釋不超過 2 個百分點，QCT 營益率仍能走向 30% 的長期目標。","2y":"FY27 下半年扣除資料中心影響的 QCT 毛利率 ≥48%，含資料中心的報表值 ≥46%。","5y":"FY31 QCT EBT 率 ≥28%。","10y":null,"threshold":"扣除資料中心影響 ≥48%；含資料中心 ≥46%。","source":"法說毛利率說明與分部 EBT 率，每季。","drift_rule":"TTM 較路徑偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉。"},{"id":"H3","text":"QTL 年金維持約 54 億美元以上、EBT 率 68% 以上，不被裝置售價上限、監管處置或下一輪續約結構性壓縮。","2y":"年營收 ≥54 億美元、EBT 率 ≥68%。","5y":"FY30 續約週期開始前維持跑率。","10y":"6G 世代費率與 5G 相近，FY33 後年營收 ≥50 億美元。","threshold":"年營收 ≥54 億美元；EBT 率 ≥68%。","source":"QTL 分部營收與 EBT 率，每季；10-K 授權風險揭露，每年。","drift_rule":"跨 2 個年度偏離視為削弱，跨 3 個年度視為反轉。"}],"R":[{"id":"R1","text":"資料中心擴不出兩家客戶：客製矽多源採購，HBC 加速器與 Dragonfly CPU 轉單未經實績驗證，FY29 的 150 億美元斜坡中途停住。","h_ref":"H1","clock":"🔥","threshold":"FY28 資料中心低於 70 億美元，或第三家客戶到 FY28 底仍無實質營收。","evidence_refs":["competitive_share_entrants#2"]},{"id":"R2","text":"QCT 毛利率結構性下移：漲價落地慢於組合稀釋，EBT 率由 Q1 FY26 的 31% 降到 Q4 的 24%，Q1 FY27 指引 20–22%（含資料中心併入影響 3 個百分點）。","h_ref":"H2","clock":"⚡","threshold":"含資料中心的 QCT 毛利率連 2 季低於 46%。","evidence_refs":[]},{"id":"R3","text":"手機市場比公司規畫更弱：記憶體短缺延續到 2027 年以後，FY26 Q4 手機營收已年減 26%，公司的持平到小跌假設落空。","h_ref":"H1","clock":"⚡","threshold":"公司下修 2027 年市場預期至年減 5% 以上，或 QCT 手機營收連 2 季低於指引中點。","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","end_markets#0","end_markets#3"]},{"id":"R4","text":"客戶自研與集中：Apple 已轉自研，下一代 iPhone 份額遠低於先前估計的 20%，Apple 與三星各占 10% 以上營收，三星與小米也在自研。","h_ref":"H1","clock":"🐢","threshold":"三星 Galaxy 份額基準低於 60%，或主要中國 OEM 旗艦改用自研。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1","end_markets#1","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"id":"R5","text":"中國與地緣：依客戶總部計中國占 FY25 營收 46%，出口限制、關稅或台海衝突都可能切斷銷售或供應；華為產品營收已不再預期。","h_ref":"H1","clock":"🔥","threshold":"美國新增對中國客戶銷售限制，或貿易政策使 QCT 毛利率單季下降 2 個百分點以上。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R6","text":"監管與授權做法：10-K 載明調查可能迫使降低權利金率或改變授權做法；裝置售價上限仍在；中國 SAMR 案最新進度事實表未涵蓋，列為資料缺口。","h_ref":"H3","clock":"🐢","threshold":"任一主要司法管轄區命令降低權利金率或強制授權晶片商。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"single_thing":{"description":"兩家超大型雲端客製矽客戶中任一家，在 FY28 前把下一代加速器交給其他供應商或自製，使資料中心營收掉到 FY27 年底 70 億美元跑率以下。","why_fatal":"資料中心是 FY29 盈餘最大的單一變動項：150 億與 70 億美元相差約 80 億營收，以 30% 營益率、13% 稅率假設計約每股 2 美元，再加上終端倍數由 15 倍降到 11 至 12 倍，合計約三成價值（自行估算）。","if_happens":"資料中心 FY29 路徑下修到 70 億美元以下，基本情境改用 Bear 倍數，持股清倉，等新客戶實績再重做判斷。","how_monitor":"每季法說的資料中心營收與 FY28 訂單覆蓋說法；AWS 合作內容變動；第三家客戶是否轉為實質營收。","probability":"12 至 24 個月約 20%，依據是兩案已有採購訂單且為多世代合作，但客製矽向來多源採購。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":12.87,"peg_fy2":0.4,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":12.7,"FY2027E":10.16,"FY2028E":12.85,"FY2029E":17.84},"fy_end_month":9,"eps_basis":"FY2027E 至 FY2029E 為 Koyfin 共識，與法說指引對照屬非 GAAP 口徑；FY2026A 12.70 美元是 GAAP 稀釋 EPS，含非營業或稅務項目，與共識不同口徑，FY26 非 GAAP 全年 EPS 事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"授權年金加晶片平台；FY23 到 FY26 GAAP 營業利益幾乎持平，複利要靠新引擎兌現。"},"industry":{"clock_phase":"IV","sd_verdict_source":"手機處於收縮段，依據是 Counterpoint 預測 2026 年出貨年減 13.9%、IDC 預測年減 12.9%，FY26 10-K 也把手機營收下滑歸因於 OEM 因記憶體受限而調降生產計畫；屬週期性將反轉，但時點不早於 2027 年底。","bargaining":{"up":"記憶體與晶圓代工握有議價權：供應鏈滿載（2026-07-29 CEO），公司以雙位數漲價轉嫁，基礎毛利率到 FY27 下半年才回到 48–50% 區間低端。","down":"下游集中：Apple、三星各占 10% 以上營收；三星、小米自研；AWS 合作附平價認股權，顯示大客戶能分走經濟利益。","geo":"FY2025 依客戶總部計中國占營收 46%，晶圓與封測集中台灣與韓國。"},"profit_pool_dir":"手機鏈利潤向記憶體與自研晶片的品牌商移動；資料中心與車用是高通正在切入的新利潤池，但五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"資料中心","value":"公司稱長期可及市場約 1 兆美元，目標 5 至 7 年份額超過 5%；FY26 營收約 3 億美元，FY27 目標 50 億，FY29 目標 150 億。"},{"item":"車用","value":"FY26 底年化約 80 億美元，FY29 目標 100 億，設計案儲備 650 億美元（2026-06-24）。"},{"item":"IoT 與工業機器人","value":"FY29 目標合計逾 140 億美元，其中工業網通與機器人 80 億。"},{"item":"手機","value":"2026 年出貨預測 10.8 億支、年減 13.9%；公司規畫 2027 年持平到小跌。"},{"item":"未涵蓋項","value":"SAM、滲透率與營業利益池五年變化事實表未涵蓋，無法驗證利潤池流出幅度。"}]},"moat":{"mechanism":"專利跨世代授權年金，加上高階 Android 平台整合與 OEM 驗證週期；車用為多世代平台合約。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"execution 穩定：車用 Q4 年增 89%，三星份額基準升到 70% 以上，Apple 流失另列為威脅。pricing power 穩定：授權費率守住，QCT 雙位數漲價目前只夠修補成本。兩項各 8 分，尚未扣威脅。","peer_na_reason":"同業 ROIC 事實表未涵蓋，改用 TTM 利潤率比較與份額方向。","threats":[{"level":"🔴","text":"客戶垂直整合：Apple 已自研數據機，三星與小米也有自研晶片，10-K 明列為風險。機率指三星或主要中國 OEM 在 24 個月內明顯提高自研比例。","p":"35%","evidence_refs":["competitive_share_entrants#1","customer_second_source#0","customer_second_source#1","customer_concentration_credit#1","substitute_technology#0","substitute_technology#1","substitute_technology#2","end_markets#1"]},{"level":"🟡","text":"手機出貨份額推擠：聯發科與 Apple 在記憶體短缺下的份額變化，可能延伸到高階 Android。","p":"30%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"資料中心客製矽多源競爭：博通、邁威爾與客戶自研都在同一張桌上，影響新事業，不傷既有授權與手機平台。","p":"35%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"Arm：陪審團認定 Arm 違約，補救階段未決。CEO 稱對 CPU 路線圖沒有影響，法院裁定前不算解除；Arm 自製 CPU 也是資料中心對手。","p":"20%","evidence_refs":[]},{"level":"🟡","text":"監管：10-K 載明調查或訴訟可能迫使公司改變授權做法，單一國家處分可能延伸至境外。","p":"15%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"投入資本事實表未涵蓋，無法落象限；授權屬高利益率、輕資產，QCT 為中等利益率。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者要的是手機與裝置體驗，決策者是 OEM，付款者是消費者。高階手機算力是需要，但記憶體漲價讓消費者延後換機，2026 年出貨預測年減 13.9%。車用與推論由車廠與雲端業者付款，較不受消費者延後影響。"},{"item":"決策層級","level":"🟡","text":"替代性要看 OEM 的平台決策：Apple 已換成自研，三星基準卻由 50% 升到 70% 以上，顯示旗艦 Android 仍不易替代。資料中心以雲端業者為決策單位，客製矽可多源，轉換成本尚未證實；車用已由逐案轉向多世代平台（2026-07-29 CEO）。漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"記憶體與晶圓代工正分走更多利潤：QCT EBT 率由 Q1 FY26 的 31% 降到 Q4 的 24%，公司以雙位數漲價轉嫁，基礎毛利率到 FY27 下半年才回到區間低端。AWS 拿到平價認股權，代表大客戶也在分價值。授權費率守住是少數正面證據。"},{"item":"社會容忍度","level":"🟡","text":"授權模式長期受反壟斷檢視，10-K 列明調查可能迫使改變授權做法；2026 年搜尋未見 DOJ、FTC、EU 對高通的新行動，反壟斷焦點轉向 Arm。中國 SAMR 案最新進度事實表未涵蓋，列為資料缺口。"}],"roiic":"近零（FY23 到 FY26 GAAP 營業利益約 86.5 億到 86.6 億美元；投入資本事實表未涵蓋，無法算精確比率）","reinvest_rate":"事實表未涵蓋（資本支出、折舊、營運資金與收購淨額未入表）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩項輸入都缺，不硬算。FY26 同時是手機低點與 Apple 退場年，此窗口偏悲觀。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","QCOM":53.1,"2454.TW":46.28,"AVGO":68.77,"NVDA":74.67,"NXPI":56.43,"unit":"%"},{"metric":"營業利益率","QCOM":20.08,"2454.TW":15.13,"AVGO":48.52,"NVDA":65.21,"NXPI":28.55,"unit":"%"},{"metric":"FCF 利潤率","QCOM":20.06,"2454.TW":13.34,"AVGO":44.22,"NVDA":41.92,"NXPI":24.16,"unit":"%"},{"metric":"研發密度","QCOM":23.67,"2454.TW":25.83,"AVGO":13.28,"NVDA":7.79,"NXPI":17.92,"unit":"%"}],"competitors":[{"name":"2454.TW","gm":46.28,"om":15.13,"fcf_margin":13.34,"rd_intensity":25.83,"strategy_note":"最直接對手，份額同受記憶體短缺拖累；高通 TTM 毛利率與營益率仍高出約 7 與 5 個百分點。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"strategy_note":"客製矽的主要對手，營益率 48.5%，資料中心案子的規模與議價差距最大。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"NVDA","gm":74.67,"om":65.21,"fcf_margin":41.92,"rd_intensity":7.79,"strategy_note":"加速器生態的領先者，營益率 65.2%；高通 CEO 認為推論市場護城河弱於訓練，切入點在推論。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"NXPI","gm":56.43,"om":28.55,"fcf_margin":24.16,"rd_intensity":17.92,"strategy_note":"車用老牌對手，營益率 28.6% 高於高通；高通靠算力平台內容增加搶份額。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（資料中心、車用新平台），價用於修補成本，併購補能力，淨回購貢獻小。","runway_years":"資料中心目前份額低於 1%，以公司 5 至 7 年 5% 目標推算，30% 滲透不構成五年內上限。","runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本、資本支出與折舊，內生上限留空；以 FY23 到 FY26 GAAP 營業利益近零增長作為歷史參考，判定共識成長超過歷史內生能力。","segments":[{"item":"手機","value":"Q4 51.4 億美元，年減 26%；12 月季預期季減中個位數，Android 成長被 Apple 下滑抵銷。"},{"item":"車用","value":"Q4 19.9 億美元，年增 89%；年化約 80 億，FY29 目標 100 億。"},{"item":"IoT","value":"Q4 18.9 億美元，年增 4%，工業網通與機器人年增 20%。"},{"item":"資料中心","value":"12 月季逾 6.5 億美元，FY27 目標 50 億、年底跑率 70 億，FY29 目標 150 億；客製矽稀釋毛利率、對營益率加分。"},{"item":"授權","value":"Q4 13.0 億美元，EBT 率 70%；續約完成，跑率不變。"}],"decay_signals":[{"item":"毛利率連 2 季 YoY 下滑","lit":true,"text":"FY26 毛利率 53.1%，FY25 為 55.4%；QCT 短期低於歷史區間（2026-07-29 CEO）。單季 YoY 序列事實表未涵蓋。"},{"item":"核心市占近 12 個月縮減","lit":true,"text":"Counterpoint 2026Q1 份額 23%，前年同期 27%。"},{"item":"主力產品提價後銷量下滑","lit":false,"text":"漲價 FY27 第二季才開始反映，尚無資料。"},{"item":"EPS CAGR 高於營收 CAGR 逾 5 個百分點","lit":true,"text":"FY27 到 FY28 共識 EPS 增 26.5%，營收增 15.5%，差 11 個百分點。"},{"item":"FCF／淨利連 2 年低於 0.75","lit":false,"text":"FY26 為 0.63、FY25 為 2.31，僅一年，且 FY26 淨利含非營業或稅務項目。"},{"item":"SBC／營收大於 5% 且逐年上升","lit":null,"text":"Q4 為 8.5%；逐年序列事實表未涵蓋。"},{"item":"TAM 萎縮或被替代技術壓縮","lit":"partial","text":"手機市場縮量、Apple 自研移除一塊可服務市場；車用與資料中心 TAM 擴大。"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"text":"事實表未涵蓋。"},{"item":"維護性資本支出占 FCF 大於 60%","lit":null,"text":"事實表未涵蓋。"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"text":"公司仍大幅投資資料中心，FY23 到 FY26 營收成長。"}],"trap_rating":"🔴"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要不靠併購撐，且事實表只有最近兩季的回購與股利，無法編三年現金去向。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Alphawave、Modular 剛併入，尚無已實現回報；五年 35 筆併購後，FY23 到 FY26 GAAP 營業利益持平，投入資本事實表未涵蓋，暫判未過。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購均價與 10 年期殖利率事實表未涵蓋，無法判定。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY23 到 FY26 稀釋股數年減約 1.6%，扣除 SBC 後仍淨縮股；Modular 的 1,783 萬股與 AWS 認股權需在 FY27 重看。","grade":"過"}]},"valuation":{"basis":"FY27 共識非 GAAP EPS 的 Forward P/E，並以 GAAP 指引年化與自由現金流對照。","peers":{"expanded":false,"reason":"同業 Forward P/E 事實表未涵蓋，同業表只有利潤率，無法做倍數對照；終端倍數改以公司自身現值與成長熄火情境定錨。"},"fwd_pe":16.28,"peg":0.5,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"非 GAAP 16.3 倍、PEG 0.50 看似便宜，但成長多為低基期反彈且共識貼著公司目標；GAAP 年化約 37 倍、FCF 殖利率 4.9%、EV/S 4.3 倍居四個年度端點的 59 百分位，兩面相抵落在合理區。PEG 以 FY27 到 FY29 兩年 CAGR 32.5% 計算。事實表只有四個年度端點，不構成五年分位，故留空。","upside_short_pct":8.8,"upside_mid_pct":36.0},"trap_analysis":{"verdict":"🔴","label":"非 GAAP 便宜、GAAP 偏貴，毛利與份額仍在下滑"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"FY27 資料中心 50 億美元大部分來自兩家客戶；客製矽向來多源採購，伺服器級 Oryon 要到 2028 年中才推出。","assumption":"兩家客戶的下一代案子會續留高通。","consequence":"資料中心停在 70 億美元以下，FY31 EPS 約 10.5 美元、倍數 11 倍，五年價格約 115 美元，中途可能見 90 美元。","ruling":"採納，與唯一致命事件相同，Bear 機率維持 32%。","watch":"FY28 訂單覆蓋說法、第三家客戶是否轉為實質營收。","evidence_refs":["competitive_share_entrants#2"]},{"view":"論點成功但股東經濟變差","evidence":"客製矽毛利率低於公司平均（2026-06-24 CFO），FY26 自由現金流由 128.2 億降到 86.5 億美元，Q1 FY27 GAAP EPS 指引只有非 GAAP 的一半；AWS 合作發平價認股權，Modular 以 1,783 萬股作價。","assumption":"資料中心營收達標就等於股東賺到錢。","consequence":"EPS 達標但每股自由現金流成長落後，倍數回不到 18 倍以上。","ruling":"採納。Base 終端倍數壓到 15 倍，低於現值 16.3 倍。","watch":"FY27 FCF 利潤率是否回到 24% 以上；GAAP 與非 GAAP EPS 差距是否縮小；CFO 稱 AWS 認股權是例外，若第二家也要求股權就算證偽。","evidence_refs":[]},{"view":"價格已反映太多","evidence":"FY29 共識 17.84 美元幾乎等於公司目標 18 美元以上；Q1 指引中點 2.25 美元，其餘三季要平均 2.64 美元才到 FY1 共識；財報後盤後跌約 6%（單一二手來源，未證實）。股價較前份 148.4 美元高 11.5%。","assumption":"共識路徑可以全額兌現。","consequence":"共識下修會同時壓低 EPS 與倍數，現價的 16.3 倍會變成更高的實際倍數。","ruling":"部分採納：非 GAAP 倍數不算貴，但共識路徑太滿，Base FY29 EPS 15.0 美元，較共識低 16%。","watch":"下一份月度共識快照是否反映 11-04 指引。","evidence_refs":["capital_markets_pricing#1"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 148.4 → 本次 165.41（+11.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=148.4","side_b":"本次 price_at_dd=165.41","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡、陷阱燈 🟡→🔴。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡、陷阱燈 🟡→🔴。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 148.4 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 148.4 美元：Bull 價 387、Bear 價 100，五年期望值 +76.7%，基準年化 14.4%，不對稱比 6.0","side_b":"本次情境、股價仍用 148.4 美元：Bull 價 432、Bear 價 115.5，五年期望值 +75.0%，基準年化 13.3%，不對稱比 5.93","ruling":"先換情境、股價不動：五年期望值少 1.7 個百分點，基準年化少 1.1 個百分點。不對稱比由 6.0 變為 5.93。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 148.4 美元：五年期望值 +75.0%，基準年化 13.3%，不對稱比 5.93","side_b":"本次情境、股價 165.41 美元：五年期望值 +57.0%，基準年化 10.9%，不對稱比 3.67","ruling":"再換股價、情境不動：起點價上漲 11.5%，五年期望值少 18.0 個百分點，基準年化少 2.4 個百分點，不對稱比由 5.93 降到 3.67。合計五年期望值比前份少 19.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"手機市場 2027 預期","cause":"新證據","prior_field":null,"side_a":"公司：2027 年手機市場持平到小跌，通路庫存已薄，6 月季是中國 Android 低點（2026-11-04 CFO）。","side_b":"Counterpoint 預測 2026 年年減 13.9%、復甦要等 2027 年底；三星稱 2027 年供需缺口可能更大；Bernstein 分析師指年底出貨跑率可能年減逾兩成。","ruling":"屬程度差異。採第三方方向，基本情境假設 2027 年手機市場年減約 5%，低於公司規畫。","evidence_level":"中","settle_metric":"3 月季 QCT 手機營收，以及公司 2027 年市場預期是否下修。","if_then":["若公司把 2027 年市場預期下修到年減 5% 以上，則停止加碼，並下修 FY28 基本 EPS。","反向：若 3 月季中國 Android 續季增且未見提前拉貨，則基本情境回到持平假設。"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","end_markets#0","end_markets#3"]},{"axis":"資料中心營收集中度","cause":"新證據","prior_field":null,"side_a":"2026-06-24 CFO：資料中心營收來源並不集中。","side_b":"2026-11-04 CFO：FY27 的 50 億美元由兩家客戶以大規模貢獻，第三家不在主要斜坡內。","ruling":"採後者。FY27 斜坡按兩家客戶集中看待，這也是致命事件設在客戶續單的原因。","evidence_level":"高","settle_metric":"FY28 營收中第三家客戶的占比。","if_then":["若第三家客戶到 FY28 底仍無實質營收，則停止加碼。","反向：若第三家客戶 FY28 營收達 10 億美元以上，則下調 Bear 機率至 28%。"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"管理層對 3 月季的說法","cause":"新證據","prior_field":null,"side_a":"2026-07-29 CFO：預期 12 月季到 3 月季營收成長。","side_b":"2026-11-04 CFO：不給 3 月季指引，只說市場的看法合理。","ruling":"屬迴避，尚不構成改口實證。季節性判斷不列入基本情境，FY27 基本 EPS 9.85 美元略低於共識 10.16 美元。","evidence_level":"中","settle_metric":"2027-02 法說的 3 月季營收指引。","if_then":["若 3 月季指引中點低於 12 月季指引中點 108 億美元，則停止加碼，FY27 基本 EPS 下修到 9.5 美元以下。","反向：若指引中點高於 115 億美元，則維持基本路徑。"],"evidence_refs":[]},{"axis":"盈餘分母","cause":"新證據","prior_field":null,"side_a":"FY27 非 GAAP 共識對應 16.3 倍，PEG 約 0.5，看起來便宜。","side_b":"Q1 FY27 GAAP 指引年化約 4.5 美元，對應約 37 倍；SBC 單季 8.73 億美元，占非 GAAP 營業利益 31.5%。","ruling":"屬程度差異，但便宜論證不成立。估值以非 GAAP 為主尺，終端倍數下壓到 15 倍反映品質折價。","evidence_level":"高","settle_metric":"FY27 自由現金流利潤率與 GAAP EPS。","if_then":["若 FY27 FCF 利潤率低於 18%，則停止加碼，基本終端倍數下修到 13 倍。","反向：若回到 24% 以上，則基本終端倍數可回到 16 倍。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":"新證據","prior_field":null,"side_a":"授權已續到 FY30 週期、車用 Q4 年增 89%、資料中心 12 月季開始出貨，股價 26 週跌 23.8%，現價隱含 FY31 EPS 約 16 美元，賣方財報前目標價多在 215 美元上下。","side_b":"毛利與份額仍在下滑，共識可能尚未反映 11-04 指引，賣方目標價都早於財報，第一個硬數據只要再等幾個月。","ruling":"不追。等待的代價是可能少賺一段，但 3 月季資料中心實績能分辨斜坡真假，資訊價值高於現在的價格優勢。","evidence_level":"中","settle_metric":"3 月季資料中心單季營收。","if_then":["若股價在實績前漲到 195 美元以上，則不追。","若股價跌破 135 美元而資料中心與毛利框架未破，則分批反買首倉。","反向：若 3 月季資料中心低於 8 億美元，則減碼已持有部位一半並重做判斷。"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2","capital_markets_pricing#3"]},{"axis":"共識是否已含最新指引","cause":"新證據","prior_field":null,"side_a":"FY1 共識最近兩份快照都是 10.16 美元，顯示 11-04 指引可能尚未進模型。","side_b":"FY1 近 3 個月已由 10.53 美元下修到 10.16 美元，部分反映記憶體壓力。","ruling":"不可裁決至下一份月度快照。在此之前凍結加碼，倉位不超過首倉。","evidence_level":"低","settle_metric":"2026-12 共識快照的 FY1 與 FY2 EPS。","if_then":["若 FY1 再下修 5% 以上，則停止加碼，Bear 路徑下移。","反向：若 FY1 持平且 FY2 上修，則維持基本路徑。"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭與客戶結構惡化：手機份額由 27% 降到 23%，Apple 自研，三星與小米自研，中國營收集中。","side_b":"結構轉好：授權續約到 FY30 週期，車用 Q4 年增 89%，資料中心開始出貨，SpaceX 地面 5G 網路 FY28 起貢獻。","ruling":"雙向拉鋸。手機端競爭與客戶結構惡化，非手機端結構轉好；其他結構變數以客戶結構為主，出口管制與關稅維持觀察。","evidence_level":"中","settle_metric":"FY27 非手機占 QCT 比重是否逾一半。","if_then":["若 FY27 非手機占 QCT 低於 45%，則停止加碼。","反向：若逾 55% 且含資料中心的 QCT 毛利率不低於 46%，則加碼至上限 3%。"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#1","regulatory_antitrust#2"]},{"axis":"價值陷阱評級上調","cause":"新證據","prior_field":["trap"],"side_a":"前份為中度風險。","side_b":"本次毛利率下滑、核心份額縮減、EPS 成長遠高於營收三項確定亮燈，手機 TAM 半亮。","ruling":"上調到最高風險級。亮燈中有兩項來自 Apple 與記憶體的已知衝擊，但依亮燈數不能降級；Trailing 倍數的便宜也來自一次性分母。","evidence_level":"中","settle_metric":"FY27 下半年 QCT 毛利率與 FY1 共識方向。","if_then":["若含資料中心的 QCT 毛利率連 2 季低於 46%，則減碼一半。","反向：若扣除資料中心影響的毛利率回到 48% 以上且共識止跌，則風險級下調一檔。"],"evidence_refs":["competitive_share_entrants#0","end_markets#3"]},{"axis":"護城河、跑道、類型與循環位置維持","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河持平、五年後跑道寬、品質複利成長、早循環。","side_b":"本次四欄不變。授權續約與三星份額支持持平，車用實績支持跑道，公司自述 6 月季為中國 Android 低點。","ruling":"維持，但 FY23 到 FY26 GAAP 營業利益持平，使類型信心降為中；手機市場仍在收縮，早循環只適用於公司自身營收。","evidence_level":"中","settle_metric":"三星份額基準、車用年化營收、中國 Android 季增。","if_then":["若三星份額基準低於 60%，則停止加碼，護城河方向改列下滑重評。","反向：若同業 ROIC 資料補齊且差距擴大，則重評等級。"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"訊號與估值維持","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份股價 148.4 美元，訊號與估值均為中性。","side_b":"本次股價 165.41 美元，上漲 11.5%，基本面多空互抵，兩欄維持不變。","ruling":"維持。股價上漲吃掉部分空間，授權續約與車用超標抵銷了部分估值壓力。","evidence_level":"中","settle_metric":"FY27 共識 EPS 與股價的相對變化。","if_then":["若股價漲到 195 美元以上而實績未到，則不追。","反向：若股價跌破 135 美元而基本面未破，則分批反買。"],"evidence_refs":[]},{"axis":"機率與最大回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 22%、Bear 32%、最大回撤單點 −45%。","side_b":"本次機率維持 22%、46%、32%，最大回撤改為 −35% 至 −50% 的範圍。","ruling":"授權續約降低下行，手機展望轉弱增加下行，兩者互抵，機率不動；回撤改用範圍表達不確定性。","evidence_level":"中","settle_metric":"3 月季資料中心實績與手機市場預期。","if_then":["若 3 月季資料中心達 10 億美元以上，則重跑判斷並檢討 Bear 機率。","反向：若低於 8 億美元，則 Bear 機率上調到 40%。"],"evidence_refs":[]},{"axis":"裁決與角色","cause":"新證據","prior_field":[],"side_a":"前份進場、衛星。","side_b":"本次結論是不追，等 3 月季資料中心實績。","ruling":"價值陷阱風險上調、分母爭議成立、最新指引可能尚未進共識，三者都由同一個事件驗證，故等事件而非等價格。","evidence_level":"中","settle_metric":"3 月季資料中心單季營收。","if_then":["若達 10 億美元以上，則重跑判斷，過關開首倉三分之一。","反向：若低於 8 億美元，則減碼已持有部位一半。"],"evidence_refs":[]},{"axis":"加碼與進場條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3·帽 3%·加碼＝QCT 毛利率回 48%＋（Q1 FY27 法說）或資料中心單季營收 ≥ $1.0B","side_b":"3 月季資料中心單季營收 ≥ $10 億（約 2027-04 底法說）→重跑判斷，過關才開首倉 1/3、總倉上限 3%","ruling":"QCT 自 FY27 起納入資料中心，CFO 說基礎毛利率回到區間低端後還會被資料中心拉低，報表值 48% 的門檻即使計畫順利也碰不到，故首要條件改為資料中心實績；毛利加碼條件改用扣除資料中心影響的 48%。","evidence_level":"高","settle_metric":"3 月季資料中心營收與 FY27 下半年毛利率。","if_then":["若資料中心達標，則重跑判斷。","反向：若 FY27 下半年扣除資料中心影響的毛利率仍低於 48%，則不加碼。"],"evidence_refs":[]},{"axis":"Single Thing 補列","cause":"方法變動","prior_field":null,"side_a":"前份摘要未載明 Single Thing（欄位為空）。","side_b":"兩家超大型雲端客製矽客戶中任一家，在 FY28 前把下一代加速器交給其他供應商或自製，使資料中心營收掉到 FY27 年底 70 億美元跑率以下。","ruling":"Single Thing 由本輪補上，依盈餘敏感度選定：資料中心差距每股約 2 美元，大於 Android 營收少一成的約 0.6 美元與毛利率少 2 個百分點的約 0.75 美元（自行估算）。","evidence_level":"中","settle_metric":"FY28 資料中心營收與客戶續單。","if_then":["若事件發生，則清倉。","反向：若兩家都簽下一代合約，則 Bear 機率下調到 28%。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻補列","cause":"方法變動","prior_field":null,"side_a":"前份摘要未載明量化門檻（欄位為空）。","side_b":"資料中心 FY27 低於 40 億美元清倉；含資料中心的 QCT 毛利率連 2 季低於 46% 減碼；QTL 年營收低於 54 億美元或 EBT 率低於 65%、三星份額低於 60%、FCF 利潤率低於 18% 停止加碼。","ruling":"前份門檻散在假設與風險文字中，本輪集中列出，便於逐季對帳。","evidence_level":"中","settle_metric":"各門檻對應的季報數字。","if_then":["若任一清倉門檻觸發，則清倉。","反向：若門檻全部未觸發且資料中心達標，則維持條件。"],"evidence_refs":[]},{"axis":"授權風險降位","cause":"新證據","prior_field":null,"side_a":"前份：裝置售價上限、華為未續約、中國 SAMR 裁決三重壓縮。","side_b":"Apple、華為、傳音已續約，CFO 稱費率守住，下一輪續約落在 FY2030 至 FY2033。","ruling":"華為未續約風險退休；售價上限仍在；SAMR 案本輪事實表未涵蓋，保留為資料缺口。QTL 年營收 54 億美元與 EBT 率 68% 的門檻保留。","evidence_level":"高","settle_metric":"QTL 分部營收與 EBT 率；SAMR 案進度。","if_then":["若 QTL 單季 EBT 率低於 65%，則停止加碼。","反向：若 SAMR 案確認無救濟，則移除該項資料缺口。"],"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"triggers":[{"n":1,"text":"12 月季資料中心營收達 6.5 億美元以上，並在 2 月法說確認 FY27 目標 50 億美元。","type":"假設驗證","maps_to":"H1","metric":"資料中心單季營收","threshold":"≥6.5 億美元且目標不下修","action":"未達則停止加碼並重做判斷","source_freq":"季報與法說，每季","date":"2027-02"},{"n":2,"text":"3 月季資料中心單季營收達 10 億美元以上，重跑判斷後開首倉三分之一，總倉上限 3%。","type":"估值rearm","maps_to":"H1","metric":"資料中心單季營收","threshold":"≥10 億美元","action":"重跑判斷，過關開首倉三分之一","source_freq":"季報與法說，每季","date":"2027-04"},{"n":3,"text":"FY27 下半年扣除資料中心影響的 QCT 毛利率回到 48% 以上，且 FY27 資料中心目標未下修。","type":"加碼","maps_to":"H2","metric":"扣除資料中心影響的 QCT 毛利率","threshold":"≥48%","action":"加碼至上限 3%","source_freq":"法說毛利率說明，每季","date":"2027-08"},{"n":4,"text":"3 月季資料中心低於 8 億美元，FY27 目標 50 億美元在算術上已難達成。","type":"減碼","maps_to":"R1","metric":"資料中心單季營收","threshold":"<8 億美元","action":"減碼一半並重做判斷","source_freq":"季報與法說，每季","date":"2027-04"},{"n":5,"text":"含資料中心的 QCT 毛利率在 FY27 下半年連 2 季低於 46%。","type":"減碼","maps_to":"R2","metric":"含資料中心的 QCT 毛利率","threshold":"連 2 季 <46%","action":"減碼一半","source_freq":"法說毛利率說明，每季","date":"2027-11"},{"n":6,"text":"公司下修 2027 年手機市場預期至年減 5% 以上，或 QCT 手機營收連 2 季低於指引中點。","type":"風險","maps_to":"R3","metric":"手機市場預期與 QCT 手機營收","threshold":"年減 ≥5% 或連 2 季低於中點","action":"停止加碼","source_freq":"法說，每季","date":"2027-05","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2"]},{"n":7,"text":"三星 Galaxy 份額基準跌破 60%，或主要中國 OEM 旗艦改採自研晶片。","type":"風險","maps_to":"R4","metric":"三星份額基準與中國 OEM 旗艦採用","threshold":"<60% 或出現自研旗艦","action":"停止加碼，護城河方向重評","source_freq":"法說與第三方拆機，每半年","date":"2027-03","evidence_refs":["customer_second_source#1","substitute_technology#0"]},{"n":8,"text":"美國新增對中國客戶銷售限制，或貿易政策使 QCT 毛利率單季下降 2 個百分點以上。","type":"風險","maps_to":"R5","metric":"QCT 毛利率與中國營收","threshold":"單季毛利率降 ≥2 個百分點","action":"減碼一半","source_freq":"8-K、10-Q，事件與每季","date":"2027-05","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"]},{"n":9,"text":"兩家客製矽客戶中任一家宣布或被揭露下一代不用高通。","type":"Single Thing","maps_to":"Single Thing","metric":"客製矽下一代合約","threshold":"任一家流失","action":"清倉","source_freq":"法說與公司公告，事件","date":"2028-09"},{"n":10,"text":"FY27 資料中心全年營收低於 40 億美元。","type":"清倉","maps_to":"H1","metric":"資料中心年營收","threshold":"<40 億美元","action":"清倉","source_freq":"10-K，每年","date":"2027-11"},{"n":11,"text":"QTL 單季 EBT 率低於 65%，或年營收低於 54 億美元。","type":"假設驗證","maps_to":"H3","metric":"QTL 營收與 EBT 率","threshold":"EBT 率 <65% 或年營收 <54 億美元","action":"停止加碼並重評授權年金","source_freq":"季報分部資料，每季","date":"2027-05","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]},{"n":12,"text":"3 月季法說後複審全部假設與門檻。","type":"複審日期","maps_to":"H1","metric":"全部假設","threshold":"到期複審","action":"重跑判斷","source_freq":"一次性","date":"2027-05"}],"kill_metrics":[{"metric":"資料中心年營收","bear_threshold":"FY27 低於 40 億美元","window":"FY27 全年","source":"公司季報與法說","last_status":"unknown"},{"metric":"含資料中心的 QCT 毛利率","bear_threshold":"FY27 下半年連 2 季低於 46%","window":"2027-04 至 2027-11","source":"公司法說毛利率說明","last_status":"unknown"},{"metric":"QTL 年營收與 EBT 率","bear_threshold":"年營收低於 54 億美元或單季 EBT 率低於 65%","window":"每季滾動","source":"公司季報分部資料","last_status":"ok"},{"metric":"三星 Galaxy 高通份額基準","bear_threshold":"低於 60%","window":"下一代 Galaxy 旗艦","source":"公司法說與第三方拆機","last_status":"ok"},{"metric":"自由現金流利潤率","bear_threshold":"FY27 低於 18%","window":"FY27 全年","source":"公司 10-K 現金流量表","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場對 FY29 目標打折合理，但把合約鎖到 FY30 週期的授權年金與已實現的車用成長一起打折：現價以 15 倍終端、年報酬 10% 反推，只要求 FY31 EPS 約 16 美元，低於公司 FY29 目標。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-23.81, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='早循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"3 月季資料中心單季營收 ≥ $10 億（約 2027-04 底法說）→重跑判斷，過關才開首倉 1/3、總倉上限 3%","exec_line":"未持有：等上述事件，不預先建倉。已持有首倉：續抱不加碼，FY27 下半年毛利達標才加碼到 3%。股價先漲到 195 美元以上而實績未到則不追；跌破 135 美元而資料中心與毛利框架未破則分批反買。"},"reasoning":{"industry":"Q4 FY26 非 GAAP 營收 104.4 億美元：手機 51.4 億（49%）、車用 19.9 億（19%）、IoT 18.9 億（18%）、授權 13.0 億（12%），比例為自行計算。非 GAAP 營益率 26.5%，GAAP 只有 13.1%，TTM 毛利率 53.1%。FY27 公司預期非手機 QCT 營收年增逾 60%、占 QCT 逾一半。單點依賴有兩個：Apple 與三星各占合併營收 10% 以上，其中 Apple 晶片正在退場；資料中心 FY27 的 50 億美元大部分來自兩家超大型雲端客戶。供需判斷：手機縮量屬週期性，但反轉時點晚於公司規畫，Counterpoint 預測 2026 年出貨年減 13.9%，復甦要等 2027 年底新記憶體產能，公司則規畫 2027 年持平到小跌。可能看錯之處：若通路庫存確實已薄，公司的持平假設會比第三方準確。","moat":"機制是專利組合跨世代授權，加上高階 Android 平台的整合能力與 OEM 驗證週期。三個可證方向：一、授權：Apple、華為、傳音完成續約，CFO 稱費率與權利金守住，營收跑率不變。二、最大客戶份額：Apple 已轉向自研；三星 Galaxy 基準由 50% 升到 70% 以上（2026-11-04 CEO）。三、出貨份額：Counterpoint 顯示 2026Q1 由 27% 降到 23%，但最直接的對手聯發科由 38% 降到 32%，份額流向 Apple 的 15% 到 19%，比較像記憶體短缺更傷 Android，而非對手搶單。與聯發科比，TTM 毛利率 53.1% 對 46.3%、營益率 20.1% 對 15.1%；與 NXP 比，營益率 20.1% 低於 28.6%。可能看錯之處：份額資料只到 2026Q1，若中國 OEM 自研比例在 FY27 持續上升，持平就會變成下滑。同業 ROIC 事實表未涵蓋，以利潤率與份額方向代替。","growth":"成長主要靠量與新品類：資料中心由 FY26 約 3 億美元到 FY27 目標 50 億；車用年化約 80 億美元，比 7 月預期高 10 億。價只用來修補毛利，併購補能力（Alphawave、Modular），淨回購貢獻小。共識 EPS FY27 10.16、FY28 12.85、FY29 17.84 美元，兩年 CAGR 32.5%；FY26 非 GAAP 全年 EPS 事實表未涵蓋，三年 CAGR 無法同口徑計算。FY29 共識已貼近公司目標 18 美元以上，賣方幾乎沒打折。內生上限因投入資本與再投資率缺資料無法量化，FY23 到 FY26 的 GAAP 營業利益近零增長；缺口歸因於營業費用率由 23% 往 19–20% 下降、漲價修補毛利與資料中心新增量。可能看錯之處：FY26 是低基期，若資料中心如期放量，歷史增量報酬的參考性很低。","governance":"FY26 自由現金流 86.5 億美元、利潤率 20.1%，FY25 為 128.2 億、29.0%；Q4 單季 18.2 億。FCF／淨利 FY26 為 0.63，但淨利 136.3 億高於營業利益約 86.6 億，含非營業或稅務項目，比率失真，該項目內容事實表未涵蓋。Q4 回饋股東 20 億美元（回購與股利各 10 億），Q3 為 23 億。SBC 單季 8.73 億美元，占非 GAAP 營業利益 31.5%、GAAP 營收 8.5%。以淨利除以 EPS 推算稀釋股數，FY23 約 11.26 億股、FY26 約 10.73 億股，年減約 1.6%。Modular 以 1,783 萬股作價，AWS 合作發平價認股權。淨負債 83.1 億美元。近三年現金去向四分與回購均價事實表未涵蓋。可能看錯之處：Alphawave 與 Modular 剛併入，現在判未過可能太早。","valuation":"FY27 共識 EPS 10.16 美元對應 16.3 倍。Trailing 13.0 倍不能用：FY26 GAAP EPS 12.70 美元含非營業或稅務項目，淨利高於營業利益。另一端，Q1 FY27 GAAP EPS 指引中點 1.13 美元，年化約 4.5 美元，對應約 37 倍，兩個口徑相差一倍以上。Q1 非 GAAP 指引中點 2.25 美元，其餘三季要平均 2.64 美元才到 FY1 共識，比 Q1 高 17%。FCF 殖利率 4.9%，EV/S 4.3 倍。FY1 共識近 3 個月下修 3.5%，最近兩份快照沒有變動，11-04 指引可能尚未反映。同業 Forward P/E 事實表未涵蓋。可能看錯之處：若資料中心如期放量，GAAP 與非 GAAP 差距會因營收攤薄而收斂，現在的 37 倍會高估貴的程度。","premortem":"股價 26 週跌 23.8%，RSI 44.3，沒有過熱，但跌幅本身不是安全邊際。共識 FY1 近 3 個月下修 3.5%，下修中的共識會把 Bear 地板往下推，上下行比值不能當進場依據。管理層未正面回答的項目：3 月季營收方向（CFO 由 7 月說會成長改為不給指引）、Apple FY27 確切金額、漲價分市場幅度、毛利率回升的確切時點。FY27 訂單覆蓋已由 6 月的迴避改為 11 月的「healthy order coverage」，仍未給數字。反方向的錯誤：若 3 月季資料中心超過 10 億美元，等待的代價是少賺一段。"},"plain":{"six":{"how_it_makes_money":"賺兩種錢：賣晶片給手機、車廠與裝置廠，以及向手機廠收專利授權金。最厚的利潤卡在授權這一節（單季營收約 13 億美元、EBT 率 70%），但未來三年的盈餘要靠資料中心與車用補上 Apple 晶片退場的缺口。","moat":"護城河方向持平：授權續約守住費率、三星份額基準由五成升到七成以上，但 Apple 晶片退場與客戶自研是已經發生的生態攻擊，目前反映在等級折價，尚未構成整體下滑。","growth":"五年後仍有跑道：車用已是實績曲線（Q4 年增 89%），資料中心 12 月季開始出貨，但資料中心的第二段成長還沒有實績。","capital":"資本配置中等：現金大部分還給股東、股本持續縮，但近一輪成長靠併購與股權換取，資本回報還沒有實績。","valuation":"現價 165.41 美元要求 FY31 EPS 約 16 美元（以 15 倍終端倍數、年報酬 10% 反推），低於公司自己訂的 FY29 目標 18 美元以上。這個要求可信，基本情境 FY31 約 18.5 美元，但便宜的說法不成立，因為分母是非 GAAP。","how_wrong":"最可能看錯的地方有三個：資料中心只靠兩家客戶撐起斜坡、手機市場比公司規畫更弱、非 GAAP 盈餘高估了股東實際拿到的錢。衰退信號已亮三盞以上，便宜表象不能當安全邊際。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場對 FY29 目標打折合理，但把合約鎖到 FY30 週期的授權年金與已實現的車用成長一起打折：現價以 15 倍終端、年報酬 10% 反推，只要求 FY31 EPS 約 16 美元，低於公司 FY29 目標。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 3 月季資料中心單季營收 ≥ 10 億美元的實績（約 2027-04 底法說），達標後重跑判斷。","trap":"🔴","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":165.41,"week26_return_pct":-23.81,"consensus_rev_3m_pct":-3.51,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"Trailing EPS 含一次性項目，不採用；FY27 非 GAAP EPS 10.16 美元未計單季 8.73 億美元的 SBC 與收購相關費用，Q1 GAAP 指引只有非 GAAP 的一半。分母本身就是爭點，便宜論證不成立。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第一季財報與 3 月季指引","impact":"高","watch":"資料中心是否達 6.5 億美元、3 月季營收指引方向"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"FY27 第二季財報","impact":"高","watch":"資料中心是否達 10 億美元、漲價是否開始反映在毛利率"},{"date":"2027-06","date_precision":"month","type":"product","event":"首款 HBC 產品 AI250 推出","impact":"中","watch":"商品矽客戶是否轉為訂單"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"SpaceX 地面 5G 網路開始貢獻營收","impact":"中","watch":"FY27 年底起的營收規模"},{"date":null,"type":"other","event":"Arm 案補救階段裁定","impact":"中","watch":"是否影響 Oryon CPU 出貨或授權成本"}],"_projected_from":"v19"}
```
