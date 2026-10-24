你是 stock-analyst v20 的**散文層（prose）agent**，標的 HON（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：HON　日期：2026-10-24　archetype：None　前份裁決：2026-07-24　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1958B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（434B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1128B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1469B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1068B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（780B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1112B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1984B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3188B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1501B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1958           3529-5042      5 條（2–6 內）  
s3                  8000         434           5296-7566      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3665          7934-11335      5 條（2–6 內）  
s6                 11000         780          7154-10220      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1112           1672-2388      3 條（2–6 內）  
s10                 5000        1984           2111-3016      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1501           2000-3499      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5140B；至少需散文≈39.86KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−45
−45%
−44%
−42%
−36%
−29%
−28%
−28
−10.2%
−0.24
−0.2%
0.5
0.6%
0.75
1%
1
1.0
1.04
1.2
1.30
1.46
1.5%
1.6
1.8
1.8%
2
2.0%
02
2%
2.01
2.1
2.1%
2.2
2.27
2.33
2.8
3
3%
3.1
3.17
3.3%
3.5
4
4%
4.0
4.2
4.5%
4.7
5
5%
5.6%
6%
06
6
6.48
6.5
6.88
07
7
7%
7.4
7.7%
8
8%
8.0%
08
8.20
8.3%
8.4
8.40
8.425
8.44
8.45
8.9
9
9.1
9.3
9.4
9.5
9.6
9.7
9.84
9.9
10
10%
10.2%
10.78
10.8
11
11%
11.03
11.2
11.4
11.5
11.7%
11.8
12
12%
12.8
12.9
13%
13
13.0%
13.8
14%
14
14.1%
14.2
14.3%
14.7
14.8%
15
15%
15.6
16%
16
16.0
16.6%
16.9%
17
18%
18
18.4%
18.6
19%
19.8%
20
20%
20.2
21
21%
21.3%
21.5%
22
22%
22.2%
22.5
23
23%
24
25%
25
25.9%
26
26.2
26.7
27
27%
28
29.0%
29
29%
30
30%
34%
35%
36.6%
37%
40%
40
42
45%
45
47%
49
49.9
50%
50
54.5%
60
60%
66
70
79%
80%
80
85%
95%
100%
100
104
110
125
130
150
150%
155
155.2
157
185
190
197
200
201.6
205.2
216
$218
218
221
221.15
241
245
246.27
249.64
250
254
350
370
374
405.6
416
701
2025
2026
2027
2028
2029
20261024
7,000
8,000
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
{"meta":{"ticker":"HON","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Honeywell International Inc."},"oneliner":"分拆後的純自動化公司，Q3 有機成長 7%、全年指引三項全上修，但現價 26 倍今年獲利只換到約一成的年化獲利成長；等股價回到 216 美元以下，或 2027 年 2 月指引確認獲利路徑。","thesis":{"H":[{"id":"H1","text":"流程自動化與技術進入多年成長期：能源專案（LNG、非洲與中東煉油、石化）會轉成營收，並帶動之後的催化劑與服務續購。","2y":"2026Q4 至 2027Q2 有機成長維持 5% 以上；2027 年催化劑中個位數成長","5y":"分部有機成長年化達中個位數以上，margin 從 2027 下半年起恢復擴張","10y":null,"threshold":"分部有機成長連兩季 ≥5%；分部 backlog 年增 ≥10%；2027 下半年 margin 年增轉正","source":"公司季報新聞稿與法說（分部有機成長、backlog、margin）","drift_rule":"連 2 季偏離門檻 5% 以上視為削弱，連 3 季偏離 10% 以上視為反轉"},{"id":"H2","text":"樓宇自動化靠新品與資料中心維持高於市場的成長，消防與安防持續拿份額。","2y":"有機成長維持中個位數以上（目前已連 8 季高個位數）","5y":"margin 由 27% 走向 29%（投資人日目標），資料中心占比持續上升","10y":null,"threshold":"有機成長 ≥5%；margin 年增 ≥50bp","source":"季報分部數據；2026-06-11 投資人日 Billal Hammoud 的目標","drift_rule":"5 年期論點：連 4 季偏離 5% 以上視為削弱，連 6 季偏離 10% 以上視為反轉"},{"id":"H3","text":"分拆後成本結構上了一個台階，2029 年調整後 EPS 約 12 美元可以達成。","2y":"2027 年 EPS 指引中點 ≥9.6 美元；公司費用約 4 億美元；margin 每年擴張 60bp 以上","5y":"2029 年 EPS ≥11.5 美元（公司目標 12 美元打折計）","10y":null,"threshold":"2027 指引中點 ≥9.6 美元；全公司 segment margin 年增 ≥60bp","source":"2027-02 的 Q4 2026 財報；Q3 2026 法說 Mike Stepniak；2026-06-11 投資人日","drift_rule":"2 年期論點：連 2 季偏離 5% 以上視為削弱，連 3 季偏離 10% 以上視為反轉"}],"R":[{"id":"R1","text":"流程分部的專案占比與 CT 併購稀釋，拖累 margin 的時間比管理層說的長。","h_ref":"H1","clock":"⚡","threshold":"Q4 分部 margin 低於 21.5%，或 2027 上半年 margin 年減超過 100bp","evidence_refs":[]},{"id":"R2","text":"工業自動化轉機失敗：對手持續增加、產品商品化，份額繼續流失。","h_ref":"H3","clock":"🔥","threshold":"工業自動化有機成長連 4 季低於 2%，或 Q4 margin 未達 22%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"id":"R3","text":"關稅、通膨與中東衝突讓價格成本轉負；國際營運占銷售一半以上，供應商也可能出問題。","h_ref":"H3","clock":"🔥","threshold":"價格成本淨效果連 2 季為負，或全公司 margin 年增轉負","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R4","text":"能源資本支出見頂：高油價帶來的專案潮在 2028 年前退去，訂單轉弱。","h_ref":"H1","clock":"🐢","threshold":"分部訂單（剔除大型 LNG 案）連 4 季年減且 book-to-bill 低於 1.0；機率達 50% 以上才砍倉","evidence_refs":[]}],"single_thing":{"description":"2027 年 2 月公布的 2027 全年調整後 EPS 指引中點低於 9.4 美元（較 2026 指引中點 8.425 美元成長不到 12%）。","why_fatal":"現價是今年 26 倍、明年 22.5 倍獲利，撐住這個價格的是 2027–2029 年每年雙位數的獲利成長、一路走到 12 美元。指引一旦低於 12% 成長，就跌破 CFO 在投資人日自己設的底線，倍數和獲利路徑會同時下修。這是情境樹裡敏感度最大的一項。","if_happens":"持股減碼一半；未持有則取消進場價，等 2027 上半年兩季的分部數據再重做研究。","how_monitor":"看 2027-02 的 Q4 財報與指引。在那之前看兩件事：Q4 訂單剔除大型 LNG 案後是否達高個位數成長，工業自動化 Q4 margin 是否達到 22%。","probability":"約 20%。呆滯成本已提前清完，Q3 上修後的指引低端已高於原本的高端，達標的可能性較高；風險在流程分部上半年的 margin 與通膨。"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.5,"peg_fy2":1.6,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":6.48,"FY2026E":8.44,"FY2027E":9.84,"FY2028E":11.03},"fy_end_month":12,"eps_basis":"公司口徑調整後 EPS，採 2026-06-29 的 1 比 2 反向分割後股數與分拆後基準。FY2025A 是用 Q3 法說「全年獲利成長約 30%」，從 2026 指引中點 8.425 美元回推（8.425÷1.30）；2026–2028 為 Koyfin 共識。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HON_20261024/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"分拆後的純自動化公司，靠裝機基礎帶動售後與軟體收入；流程分部受能源資本支出週期影響"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性偏結構：LNG 設備三年產能已被訂滿（2026-06-11 投資人日，Mike Stepniak），流程分部 backlog 年增超過 10%，但 Q3 法說也提到 Brent 高於 110 美元。消防安防與資料中心需求偏結構性。","bargaining":{"up":"上游是半導體、電子零件、銅與黃銅等通膨項目，公司以 3.5–4.5% 漲價抵銷，價格與成本相抵後淨正約 30bp。","down":"樓宇銷售六成以上經通路夥伴；流程端的大型專案業主（如 Dangote）議價力強，但裝機後的催化劑與服務會持續續購。","geo":"國際營運（含美國出口）占銷售一半以上，關稅和中東衝突是主要的地緣變數。"},"profit_pool_dir":"利潤池往軟體、服務與售後催化劑移動；服務加軟體目標由營收的 40% 提高到 45%。","tam_table":{"expanded":false,"reason":"事實表沒有 TAM 與滲透率的分段資料；成長主軸是既有裝機的漲價、售後與專案轉換，不是新品類滲透，展開也沒有可引用的數字。"}},"moat":{"mechanism":"裝機基礎鎖定：樓宇的消防安防面板與 Niagara 中介軟體、約 2 萬座流程工廠的控制系統與製程授權，帶出催化劑、服務與軟體續購。換系統需要停機、重新驗證並重新訓練人員。","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力在擴大：工業自動化準時交貨率由不到 40% 升到 60%，逾期訂單減少 18%，樓宇連續 8 季高個位數成長。定價力穩定：漲價 3.5–4.5%，價格與成本相抵後淨正約 30bp。不過工業自動化過去四年失去份額、近期才止血，同業 ROIC 差距無資料可比，合判持平。","peer_na_reason":"事實表沒有同業 ROIC，以利潤率代替。HON 近四季數字含分拆前的航太，和分拆後的結構不能直接比。","threats":[{"level":"🟡","text":"對手數量增加，包括新進者與非傳統對手，可能帶來產品商品化、壓低價格與毛利（10-K 自述）","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"樓宇軟體平台層之爭：JCI、西門子、施耐德都押注水平平台加生成式 AI，Honeywell 靠 Niagara 的裝機量防守；10-K 也列出要防範顛覆性技術與產品商品化","p":"30%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"工業自動化對 Emerson、Rockwell 失去份額；2026-06-11 投資人日上 Peter Lau 承認過去四年失份額，轉機才剛開始","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"事實表沒有投入資本數據，推定為高利益率×低周轉（segment margin 21%，歷年併購帶來大量商譽）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"消防與安防有法規強制需求；流程控制是工廠安全運轉必需品，客戶要解決的問題長期存在。backlog 近 190 億美元、年增 7%。"},{"item":"決策層級","level":"🟢","text":"替代決策的最小單位是整座工廠或整棟建築的控制系統，換系統要停機、重新驗證並重新訓練人員。Q3 法說說明，升級與資安強化可以在線上完成，不必停機，裝機客戶受到保護。新建專案則是競標，屬另一回事。"},{"item":"價值鏈分配","level":"🟡","text":"樓宇有六成以上銷售經通路夥伴，通路分走部分價值；上游的半導體與金屬通膨約 350bp，漲價只比成本多出約 30bp，在價值鏈裡能守住分配，但擴張空間有限。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業與工業業主，沒有消費者層面的政治價格上限；主要政策風險是關稅與出口管制，那是成本面的問題，不是定價上限。"}],"roiic":"事實表沒有增量投入資本。唯一能算的是 Johnson Matthey 催化劑技術的收購：買價約 13 倍 EBITDA（2026-07-23 Q2 法說），換算稅前 EBITDA 收益率約 7.7%，扣稅與折舊後報酬偏低，要靠成本綜效才能提高。","reinvest_rate":"事實表未涵蓋。資本支出約占營收 3%（投資人日），收購金額沒有收錄。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，兩個輸入都不在事實表內。成長題改用公司承諾的有機營收 4–6% 當替代上界。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","HON":36.57,"ROK":54.53,"SIE.DE":39.36,"ABBN.SW":40.09,"SU.PA":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","HON":16.58,"ROK":19.75,"SIE.DE":12.98,"ABBN.SW":16.93,"SU.PA":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","HON":11.1,"ROK":16.76,"SIE.DE":14.61,"ABBN.SW":11.7,"SU.PA":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","HON":5.28,"ROK":5.85,"SIE.DE":8.31,"ABBN.SW":3.92,"SU.PA":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"ROK","gm":54.53,"om":19.75,"fcf_margin":16.76,"rd_intensity":5.85,"strategy_note":"毛利率 54.5%，比 HON 高約 18pp，強項在離散自動化；Honeywell 在這一塊目前沒有參與，正面重疊集中在工業自動化。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SIE.DE","gm":39.36,"om":12.98,"fcf_margin":14.61,"rd_intensity":8.31,"strategy_note":"以 Building X 爭奪樓宇平台層，營業利益率 13.0% 低於 HON，但研發密度 8.3% 高出約 3pp，是平台戰的主要對手。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ABBN.SW","gm":40.09,"om":16.93,"fcf_margin":11.7,"rd_intensity":3.92,"strategy_note":"營業利益率 16.9%、FCF 利潤率 11.7%，與 HON 幾乎同一水準，在流程控制系統上正面競爭。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SU.PA","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"以 EcoStruxure 押注同一個水平平台；事實表沒有它的財務數據，無法比較利潤率。"}]},"growth":{"driver_mix":"價格約 4%（2026 年平均）＋銷量約 2–4%＋margin 擴張（呆滯成本清除、每年營運面 60bp）＋利息下降；2029 年 12 美元的目標不含併購。","runway_years":"事實表沒有滲透率資料，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"增量投入資本不在事實表內，內生上界以公司承諾的有機營收 4–6% 替代，約 5%。共識 EPS 年化 14–19% 和這個上界的差額歸因於 margin 擴張與利息下降，可以歸因，不屬於依賴重新評價。","segments":[{"item":"樓宇自動化","value":"Q3 營收 20.2 億美元，有機成長 8%，連續 8 季高個位數；segment margin 27%；高成長產業（資料中心、醫療、旅館）占 20%，其餘本業成長中個位數。"},{"item":"流程自動化與技術","value":"Q3 營收 18.6 億美元，有機成長 8%；專案 +14%，煉油催化劑 +80%；margin 由 22.2% 降到 Q4 預估 21.5%，原因是專案占比提高與 CT 併購稀釋；backlog 年增超過 10%。"},{"item":"工業自動化","value":"Q3 營收約 11.2 億美元（推算），有機成長 4%，帳面年減 23%（出售業務）；margin 18.4%，Q4 目標 22%，其中約 150bp 來自營運改善；核心訂單成長 15%。"}],"decay_signals":[{"signal":"EPS 成長顯著快於營收成長（差距超過 5pp）","lit":true,"evidence":"2027 共識 EPS 年增 16.6%，共識營收只增 1.8%；獲利成長靠成本結構。"},{"signal":"FCF 對淨利低於 0.75 連 2 年","lit":false,"evidence":"2026 FCF 指引 21 億美元，除以調整後淨利約 26.7 億美元（8.425 美元×3.17 億股），約 79%；前一年分拆後口徑不在事實表內。"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"evidence":"Q3 約 2.1%（14.1%×7.4 億÷49.9 億）"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"樓宇連續 8 季拿份額；工業自動化失份額發生在過去四年，近期已止血。"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主體是有機成長（2029 年 12 美元目標不含併購）；近三年現金去向四分與回購均價都不在事實表內。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Johnson Matthey 催化劑技術 2026-07-17 完成收購，買價約 13 倍 EBITDA（Q2 法說），還沒有實現報酬可以驗證；13 倍的倒數約 7.7%，是稅前現金收益率的起點，扣稅後不一定高於資金成本。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2026 年資金優先還債（總債務年底降到 130 億美元以下），今年沒有回購可評；投資人日的目標是每年減少約 1% 股數。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 股票酬勞約占 GAAP 營業利益 7.4 億美元的 14.1%，約 1.04 億美元一季，年化約 4.2 億美元，占市值 701 億美元約 0.6%，低於每年 1.5%。淨稀釋要看股數年變化，事實表未涵蓋。","grade":"過"}]},"valuation":{"basis":"前瞻本益比（2026 共識調整後 EPS）＋ PEG（2026→2028 共識 EPS 年化）","tier":"大型多角化工業自動化","peers":{"expanded":false,"reason":"事實表沒有同業的前瞻本益比，只有利潤率對照，無法做倍數錨定。"},"fwd_pe":26.2,"peg":1.8,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"今年 26.2 倍、明年 22.5 倍；兩年共識 EPS 年化 14.3%，PEG 約 1.8，落在 1–2 的合理區間；分拆後只有一季可比的歷史倍數，五年分位不可用；賣方目標價約 250 美元，較現價高 13%。綜合判為中性。","upside_short_pct":12.9,"upside_mid_pct":14.7},"trap_analysis":{"verdict":"🟡","label":"獲利增速遠超營收增速，靠成本結構撐"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 剔除去年同期大單後，訂單只成長 3%，book-to-bill 1.0；法說提到 Brent 高於 110 美元。10-Q 揭露中東衝突影響能源市場與航運。","assumption":"流程分部的多年成長期是結構性的，不是高油價帶來的一波專案潮。","consequence":"如果 2027–2028 年能源專案退潮，同時工業自動化轉機停住，EPS 會停在 9–10 美元，倍數壓到 16 倍，五年後股價約 155 美元，較現價下跌約 30%。","ruling":"部分採納。管理層提到非洲 Dangote 擴建、永續航空燃料授權專案只建成 20%、LNG 設備三年產能已訂滿，這些支撐需求的力量不只來自油價，所以不採全盤失敗；但熊市機率因此維持 30%。這條與唯一致命點部分重疊：唯一致命點監測的是 2027 指引，這條監測的是訂單。","watch":"流程分部訂單（剔除大型 LNG 案）年增率；book-to-bill 是否連兩季低於 1.0","evidence_refs":["geo_supply_chain#0"],"fact_refs":["f_kpi8_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"GAAP 營業利益率 14.8%，segment margin 21.3%，差 6.5pp；股票酬勞約占營業利益 14%；每年重整費用約 7,000–8,000 萬美元。管理層稱 2027 年起做 20–40 億美元補強併購，CT 以 13 倍 EBITDA 買入。10-K 另稱對俄合約剩餘義務超出已提列準備的可能損失無法估計。","assumption":"調整後獲利能轉成股東拿得到的現金，降槓桿後省下的現金會用在高報酬的地方。","consequence":"營運目標全部達成，但調整項持續存在、併購以高倍數買入，每股自由現金流成長會比調整後 EPS 慢，股東實得報酬低於帳面成長。","ruling":"採納為監測項，不改結論。今年 FCF 轉換約 79%，Q4 管理層預期超過 100%；但 GAAP 與調整後的差距需要逐年縮小。","watch":"GAAP 營業利益率與 segment margin 的差距；新併購的 EBITDA 倍數是否超過 15 倍；全年 FCF 對調整後淨利是否低於 85%","evidence_refs":["reg_tariff_export#3"],"fact_refs":["f_kpi2_gaap","f_kpi3_segment_margin","f_kpi6_sbc","f_kpi5_fcf"]},{"view":"價格已反映太多","evidence":"今年 26.2 倍、明年 22.5 倍獲利；PEG 約 1.8；2027 共識營收只增 1.8%。","assumption":"市場會一直給純自動化公司的高倍數，不會回到多角化集團的折價。","consequence":"基本情境 EPS 到 13.8 美元，但倍數由 26 倍降到 21 倍，股價年化約 5–6%，加上股息約 8%，在中段偏弱。","ruling":"採納。這是等價格而不追價的主要理由；但現價只比進場價高約 2%，這個風險在價格上的差距不大。","watch":"股價對 2027 共識 EPS 的倍數；賣方目標價的方向","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_rev_consensus_fy2_m"]}],"max_dd":{"lo":-45,"hi":-28,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 246.27 → 本次 221.15（-10.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=246.27","side_b":"本次 price_at_dd=221.15","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 246.27 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 246.27 美元：Bull 價 416、Bear 價 185，五年期望值 +29.0%，基準年化 8.0%，不對稱比 2.8","side_b":"本次情境、股價仍用 246.27 美元：Bull 價 405.6、Bear 價 155.2，五年期望值 +13.0%，基準年化 3.3%，不對稱比 1.46","ruling":"先換情境、股價不動：五年期望值少 16.0 個百分點，基準年化少 4.7 個百分點。不對稱比由 2.8 變為 1.46。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 246.27 美元：五年期望值 +13.0%，基準年化 3.3%，不對稱比 1.46","side_b":"本次情境、股價 221.15 美元：五年期望值 +25.9%，基準年化 5.6%，不對稱比 2.33","ruling":"再換股價、情境不動：起點價下跌 10.2%，五年期望值多 12.8 個百分點，基準年化多 2.2 個百分點，不對稱比由 1.46 升到 2.33。合計五年期望值比前份少 3.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訂單動能：backlog 創高，但本季 book-to-bill 只有 1.0","cause":null,"side_a":"Q2 法說訂單有機成長 16%；投資人日稱流程分部 book-to-bill 高於 1.2；本季 backlog 年增 7%，接近 190 億美元。","side_b":"Q3 剔除去年同期一筆 7 億美元大單後，訂單只成長 3%，book-to-bill 1.0。","ruling":"可調和，屬程度差異。去年 Q3、Q4 各有一筆 7 億美元的低碳與 LNG 大單，本季比較基期偏高；流程分部 backlog 仍年增超過 10%。採 A 側，但把 Q4 訂單當作驗證點。","evidence_level":"公司新聞稿與法說（2026-10-22 Q3、2026-07-23 Q2、2026-06-11 投資人日）","settle_metric":"Q4 訂單剔除大型 LNG 案後的年增率","if_then":["若 Q4 剔除大單後的訂單年增達高個位數，維持流程分部的成長論點，進場價不變","若 Q4 剔除大單後的訂單年減，進場價下修到 2027 共識 EPS 的 20 倍（約 197 美元）"],"evidence_refs":[]},{"axis":"管理層承諾與改口：軟體 ARR 與年底 margin","cause":null,"side_a":"2026-07-23 Q2 法說：Vimal Kapur 稱 2026 年 ARR 成長約 15%；Mike Stepniak 稱年底 segment margin 高於 22%。","side_b":"2026-10-22 Q3 法說：Vimal Kapur 改稱今年 ARR 約 12–13%；Mike Stepniak 稱 Q4 margin 約 22%，流程分部降到 21.5%。","ruling":"可調和，屬程度差異的小幅改口。EPS、FCF、有機成長三項都上修，改口集中在軟體成長與流程分部的 margin。記為管理層可信度的扣分項，不改結論。","evidence_level":"兩場法說逐字稿","settle_metric":"2027 年指引中的 ARR 目標與 Q4 實際 margin","if_then":["若 2027 年指引把 ARR 成長目標降到 12% 以下，護城河中軟體這一項降為弱項","若 Q4 margin 達 22% 以上，視為承諾兌現"],"evidence_refs":[]},{"axis":"現在就買的最強論證，對照等價格","cause":null,"side_a":"全年指引三項全部上修，新指引低端已高於原本的高端；股價較上份研究下跌 10%，明年獲利倍數 22.5 倍；上份研究等待的流程分部拐點本季已經出現（有機成長 8%）。","side_b":"26 倍今年獲利只換到約一成的年化獲利成長，基本情境年報酬約 8%；成長多來自 margin 而不是營收（2027 共識營收只增 1.8%）；2 月的指引是二元事件。","ruling":"選擇等價格。基本情境報酬在 8% 上下，現價離進場價只差約 2%，不值得為這 2% 去承擔 2 月指引的二元風險。現在就買的論證有分量，所以進場價設在接近現價的位置。","evidence_level":"事實表估值與共識數字＋Q3 法說","settle_metric":"股價對 2027 共識 EPS 的倍數；2027-02 的指引","if_then":["若股價跌到 216 美元以下，先建 2% 試單","若股價沒有回落，但 2 月指引 EPS 中點達 9.6 美元以上、且 Q4 流程分部有機成長達 5%，以當時價格建 2% 試單","若指引中點低於 9.4 美元，取消進場價，等兩季數據後重做研究"],"evidence_refs":[]},{"axis":"前份漂移：估值、評等、裁決與角色","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份股價 246.27 美元，今年指引中點 8.20 美元，前瞻倍數約 30 倍，估值偏貴，評等 B，裁決為觀望。","side_b":"現價 221.15 美元，今年共識 8.44 美元，前瞻 26.2 倍、明年 22.5 倍，估值轉為中性；品質判斷不變。","ruling":"估值結論由偏貴改為中性，原因是股價下跌 10% 加上獲利上修 3%。綜合評等維持 B；裁決與角色由矩陣決定，預期仍是等價格觀察。","evidence_level":"事實表股價與共識快照","settle_metric":"前瞻本益比","if_then":["若股價回升到 245 美元以上而獲利沒有再上修，估值回到偏貴"],"evidence_refs":[]},{"axis":"前份漂移：陷阱、護城河方向、跑道、公司類型、循環位置","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：陷阱 🟢，護城河方向持平，五年後跑道 🟡，品質複利型，未判循環位置。","side_b":"本次：陷阱轉 🟡，因 2027 共識 EPS 年增 16.6%、營收只增 1.8%，差距超過 5pp；護城河方向維持持平（樓宇連 8 季拿份額，工業自動化過去四年失份額、剛止血）；跑道維持 🟡；類型維持品質複利型；循環位置仍不判。","ruling":"只有陷阱一欄改變，來源是事實表新收錄的分拆後共識營收。其他四欄有新證據，但不足以改判。","evidence_level":"事實表共識營收與 EPS；Q3 法說","settle_metric":"2027 實際營收與 EPS 成長差距","if_then":["若 2027 年有機營收成長達 5% 以上、獲利與營收的成長差距收窄到 10pp 以內，陷阱回到 🟢"],"evidence_refs":[]},{"axis":"前份漂移：情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份牛市、熊市機率各 25%，最大回撤 −42%。","side_b":"本次牛市 25%、基本 45%、熊市 30%；最大回撤範圍 −28% 至 −45%。","ruling":"基本情境的獲利成長超過再投資能支撐的內生上界，差額靠 margin 擴張，因此熊市機率提高到 30%。回撤改用區間，並以熊市倍數壓縮推導。","evidence_level":"本次情境假設","settle_metric":"2027 margin 擴張幅度","if_then":["若 2027 年 margin 擴張達 60bp 以上且有機成長在 4–6%，下份可把熊市機率降回 25%"],"evidence_refs":[]},{"axis":"進場條件更動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"回檔至 Fwd PE ≤22x FY27（約 $218）或 PA&T Q3/Q4 營收確認高個位數拐點兌現（backlog 轉換 + catalyst 出貨回升）","side_b":"股價 ≤216 美元（FY2027 共識 EPS 9.84 的 22 倍），觸及後進場試單 2%，2 月指引確認後再加碼到 4%。","ruling":"上份進場條件的後半「流程分部 Q3 確認高個位數拐點」已經發生（Q3 有機成長 8%、催化劑雙位數成長），約束只剩價格。2027 共識 EPS 由約 9.9 美元變為 9.84 美元，22 倍對應的價格由 218 改為 216 美元。","evidence_level":"Q3 新聞稿與法說；事實表共識","settle_metric":"股價對 2027 共識 EPS 的倍數","if_then":["若股價跌到 216 美元以下，進場試單 2%","若 2 月指引中點達 9.6 美元以上，加碼到 4%"],"evidence_refs":[]},{"axis":"出場指標新設","cause":"方法變動","prior_field":[],"side_a":"前份沒有設定獲利或營運的出場指標（空白）。","side_b":"本次設定四條：2027 指引 EPS 中點低於 9.4 美元，減碼一半；流程分部有機成長連兩季低於 3%；全公司 margin 連兩季年減；工業自動化有機成長連兩季低於 2%，減碼到 2% 以下。","ruling":"前份是觀察、不持有，所以沒有設出場指標。本次股價接近進場價，補上減碼的量化條件；四條都觸發時清倉。","evidence_level":"本次判斷","settle_metric":"各條指標的季報數據","if_then":["若四條中任兩條同季觸發，減碼一半","若四條全部觸發，清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"新證據","prior_field":[],"side_a":"前份沒有設定唯一致命點（空白）。","side_b":"2027 年 2 月公布的 2027 全年調整後 EPS 指引中點低於 9.4 美元（較 2026 指引中點成長不到 12%）。","ruling":"Single Thing 設定為 2027 年指引。分拆完成後的第一份完整年度指引，是獲利路徑上最大的單一敏感項；CFO 在投資人日說過，明年 EPS 成長不到 12% 會非常失望。觸發時減碼一半。","evidence_level":"2026-06-11 投資人日 Mike Stepniak；Q3 法說","settle_metric":"2027-02 指引 EPS 中點","if_then":["若中點低於 9.4 美元，減碼一半，未持有則取消進場價","若中點達 9.6 美元以上，視為通過"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年指引的 EPS 中點低於 9.4 美元","type":"Single Thing","maps_to":"H3","metric":"2027 全年調整後 EPS 指引中點","threshold":"<9.4 美元","action":"減碼一半；未持有則取消進場價","source_freq":"公司財報，每年 2 月","date":"2027-02","evidence_refs":[]},{"n":2,"text":"股價回到 216 美元以下（2027 共識 EPS 的 22 倍）","type":"估值rearm","maps_to":"H3","metric":"股價÷FY2027 共識 EPS","threshold":"≤22 倍（約 216 美元）","action":"先建 2% 試單","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":3,"text":"Q4 流程分部有機成長達 5% 以上，訂單剔除大型 LNG 案後達高個位數成長","type":"假設驗證","maps_to":"H1","metric":"流程分部有機成長；剔除大單後的訂單年增","threshold":"有機成長 ≥5%；訂單 ≥7%","action":"確認後試單可加到 4%","source_freq":"季報","date":"2027-02","evidence_refs":[]},{"n":4,"text":"關稅與通膨讓價格成本淨效果轉負","type":"風險","maps_to":"R3","metric":"法說揭露的價格成本淨效果（bp）","threshold":"連 2 季為負","action":"停止加碼","source_freq":"季報法說","date":null,"evidence_refs":["reg_tariff_export#4","geo_supply_chain#1"]},{"n":5,"text":"工業自動化有機成長連兩季低於 2%","type":"減碼","maps_to":"R2","metric":"工業自動化有機成長","threshold":"連 2 季 <2%","action":"減碼到 2% 以下","source_freq":"季報","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"Q4 財報與 2027 年指引公布後，重做研究","type":"複審日期","maps_to":"H3","metric":"2027 指引全項","threshold":"公布即複審","action":"重跑研究","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"2027 全年調整後 EPS 指引中點","bear_threshold":"<9.4 美元（成長不到 12%）","window":"2027-02 財報","source":"公司 Q4 2026 新聞稿","last_status":"unknown"},{"metric":"流程自動化與技術分部有機成長","bear_threshold":"連兩季 <3%","window":"2026Q4–2027Q2","source":"公司季報新聞稿","last_status":"ok"},{"metric":"全公司 segment margin 年增幅","bear_threshold":"連兩季年減","window":"2027 每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"工業自動化有機成長","bear_threshold":"連兩季 <2%","window":"2027 每季","source":"公司季報新聞稿","last_status":"ok"}],"evidence_dismissed":[{"ref":"competitive_share_entrants#2","reason":"這條講的是航太事業的份額，航太已在 2026-06-29 分拆，不再屬於本公司；而且來源是商業資料庫，分母口徑沒有驗證。"},{"ref":"supply_demand_durability#0","reason":"來源是 Honeywell Aerospace 的 Q2 2026 法說，這家公司分拆後已獨立上市，數據不屬於本公司的營運。"},{"ref":"reg_tariff_export#2","reason":"原文指出單一來源採購「particularly in Aerospace Technologies」，主要範圍是已分拆的事業；剩下三個分部的單一來源比重，原文沒有揭露。"},{"ref":"geo_supply_chain#3","reason":"這是 2025 年 3 月航太事業負責人談機械類供應商的說法，該事業已分拆，證據對象不是本公司。"},{"ref":"capital_markets_pricing#2","reason":"這條拿分拆後的指引去比分拆前的共識（EPS 10.78 美元、營收 241 億美元），基準不同，原文也自己註明共識還沒更新；而且引用的指引之後已上修到 8.40–8.45 美元。"},{"ref":"capital_markets_pricing#3","reason":"來源是轉載站，品質偏弱；降目標價的理由是航太部門表現，而航太已分拆，和現在的公司結構不同。"},{"ref":"product_recall_warning#0","reason":"通報只涵蓋英國兩款照明控制器的特定批次，沒有揭露數量和成本，無法連結到任何分部營收或 margin。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-0.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價 ≤216 美元（FY2027 共識 EPS 9.84 的 22 倍）","exec_line":"觸及後先建 2% 試單；2027 年 2 月指引 EPS 中點 ≥9.6 美元且 Q4 流程分部有機 ≥5% 再加到 4%；指引 <9.4 美元則取消進場價並減碼一半"},"reasoning":{"industry":"Q3 營收 49.9 億美元。三個分部如下：樓宇自動化 20.2 億美元，有機成長 8%；流程自動化與技術 18.6 億美元，有機成長 8%；工業自動化約 11.2 億美元（由總營收減去另兩個分部推算），有機成長 4%，帳面因出售業務年減 23%。GAAP 營業利益率 14.8%，公司口徑 segment margin 21.3%，年增 370bp。調整後 EPS 2.27 美元，年增 34%。backlog 近 190 億美元。單點依賴：10-K 稱銷售不實質依賴單一客戶，風險不在集中度。護城河證據是裝機基礎：Niagara 中介軟體超過百萬套，約 2 萬座流程工廠用 Honeywell 技術。產業時鐘判在擴張期，依據是能源專案在北美、中東、非洲與亞洲同時下單，資料中心訂單倍增，backlog 年增 7%。供需持久性屬週期性偏結構：LNG 與煉油專案跟著能源資本支出週期走；消防安防法規需求和資料中心偏結構性；供給端可逆性中等。","moat":"護城河機制是裝機基礎鎖定：換掉控制系統或消防平台要停機並重新驗證，所以售後、催化劑與軟體會跟著已裝設備續購。執行力在改善：工業自動化準時交貨率由不到 40% 升到 60%，樓宇連續 8 季高個位數有機成長，Q3 法說稱這是在拿份額。定價力穩定：價格成長 3.5–4.5%，抵銷通膨後仍淨正。扣分項有兩個：投資人日上 Peter Lau 承認工業自動化過去四年失去份額；10-K 稱對手數量持續增加、產品有商品化風險。同業 ROIC 不在事實表內，只能用利潤率比較。HON 近四季營業利益率 16.6%，Rockwell 19.8%、ABB 16.9%、西門子 13.0%；Rockwell 毛利率 54.5%，HON 36.6%。另外 HON 這四季數字含分拆前的航太，可比性有限。兩項評分都給 7 分，合併等級 B。產業態勢判為雙向拉鋸：競爭面，對手增加，且四大樓宇業者都在押注水平平台；結構面，能源專案多區域上行、資料中心訂單倍增；其他變數是關稅與中東衝突。","growth":"共識調整後 EPS：2026 年 8.44 美元、2027 年 9.84 美元、2028 年 11.03 美元，兩年年化約 14.3%。從分拆後的 2025 年基期約 6.48 美元起算，三年年化約 19%。基期是用 Q3 法說「全年獲利成長約 30%」，從 2026 指引中點 8.425 美元回推。共識營收 2027 年只比 2026 年多 1.8%（205.2 億對 201.6 億美元），獲利成長遠快於營收。內生上界：增量投入資本沒有資料，以有機營收 4–6% 當替代，約 5%。共識成長高出的部分歸因於 margin 擴張：呆滯成本 2026 年底清完，營運面每年擴張 60bp，公司費用降到約 4 億美元，利息費用也在下降。這不是再投資帶來的成長。第二曲線方面，資料中心訂單成長超過 100%，但只占樓宇分部約 5%；永續航空燃料已授權 100 個專案，只有約 20% 建成。兩者都還沒到能撐規模的程度，事實表也沒有滲透率資料，所以判中等。","governance":"Q3 FCF 6.88 億美元，現金轉換率 95%。全年 FCF 指引 21 億美元，約為調整後淨利的 79%，上半年受中東衝突與分拆影響。淨負債 104 億美元，目標年底總債務降到 130 億美元以下、毛槓桿低於 3 倍。股息殖利率 2.0%，投資人日設定配發率約 35%。股票酬勞約占 GAAP 營業利益的 14.1%，年化約 4.2 億美元，約占市值 0.6%。Johnson Matthey 催化劑技術以約 13 倍 EBITDA 買入，Q3 法說稱成本綜效高於原估，但收購 2026-07-17 才完成，報酬還無法驗證。管理層稱 2027 年起再看 20–40 億美元的補強併購，第一優先是工業自動化的感測與量測。Quantinuum 47% 持股帳面約 70 億美元，管理層說會擇時出售。","valuation":"前瞻本益比是今年 26.2 倍、明年 22.5 倍。兩年共識 EPS 年化 14.3%，PEG 約 1.8，在合理區間的偏上緣。近四季本益比只有 11 倍、EV/S 2.1 倍，看起來便宜，但分母含已經分拆出去的航太和分拆前的營收，不能當便宜的證據。前瞻 EV/S 是 4.0 倍。分拆前的歷史倍數和現在不可比，五年分位也無法使用。賣方平均目標價約 250 美元（2026-07 至 08 月，27 至 28 位分析師），較現價高約 13%。股價自上份研究以來下跌 10%，同期今年 EPS 上修 3%，倍數由約 30 倍降到 26 倍，估值由偏貴轉為中性。26 週股價報酬 −0.2%，RSI 66，動能沒有過熱。","premortem":"價值陷阱的訊號亮了一個：2027 共識 EPS 年增 16.6%，營收只增 1.8%，獲利靠成本結構撐，所以判 🟡。其餘訊號沒有亮：FCF 轉換約 79%，股票酬勞約占營收 2.1%，樓宇仍在拿份額。下行路徑：今年 EPS 約 8.4 美元，倍數如果由 26 倍壓到 14–16 倍，股價約落在 125–157 美元。管理層改口的地方有兩處：軟體 ARR 成長由 15% 降為 12–13%，Q4 margin 由「高於 22%」改為「約 22%」。"},"plain":{"six":{"how_it_makes_money":"Honeywell 賺的是全球建築、能源與工廠業主的錢。利潤主要落在裝機之後的售後環節，包括消防與安防面板、控制系統、催化劑和服務的續購。","moat":"護城河方向持平","growth":"五年後的成長跑道屬中等。成長來自漲價 3–4%、銷量約 2–4% 與 margin 擴張；資料中心與低碳燃料這兩條可能的第二曲線，規模還不足以撐起成長。","capital":"資本配置中等：2026 年先還債，之後以補強型併購為主，回購要等槓桿降下來。","valuation":"以現價 221 美元買進，需要 2026–2028 年 EPS 年化成長約 14%、2029 年接近 12 美元；就算倍數之後由 26 倍降到 21 倍，基本情境年報酬仍有約 8%。前兩年我相信，2029 年的目標我打折看。","how_wrong":"最可能看錯的地方有三個。一是能源專案潮比管理層說的短；二是工業自動化的轉機停在低個位數成長；三是獲利成長主要靠成本、營收增速太慢，一旦 margin 擴張用完，倍數會下修。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"股價 ≤216 美元（2027 共識 EPS 22 倍），或 2027-02 指引 EPS 中點 ≥9.6 美元且 Q4 流程分部有機 ≥5%","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":221.15,"week26_return_pct":-0.24,"consensus_rev_3m_pct":1.81,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"近四季本益比 11 倍與 EV/S 2.1 倍的分母，含已分拆的航太和分拆前營收（2025 年 374 億美元，分拆後今年約 200 億美元），而且 2026-06-29 還做了 1 比 2 反向分割，不能當便宜的證據。本研究一律用前瞻口徑。短期上檔以賣方平均目標 249.64 美元計算；中期上檔以 2028 共識 EPS 11.03 美元 × 23 倍 ≈ 254 美元計算。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 全年指引","impact":"高","watch":"EPS 中點達 9.6 美元以上為通過，低於 9.4 美元為唯一致命點"},{"date":"2027-02","date_precision":"month","type":"other","event":"Q4 訂單：剔除大型 LNG 案後的成長","impact":"中","watch":"管理層預期高個位數成長；book-to-bill 是否回到 1.0 以上"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"新型燃氣表在多家公用事業的測試完成（測試期 6–9 個月）","impact":"低","watch":"2027 年起是否轉成大規模換裝訂單"},{"date":null,"date_precision":null,"type":"other","event":"Quantinuum 47% 持股變現","impact":"中","watch":"帳面約 70 億美元，管理層稱擇時出售；所得用於還債或回購"}],"_projected_from":"v19"}
```
