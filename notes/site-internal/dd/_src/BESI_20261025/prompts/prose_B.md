你是 stock-analyst v20 的**散文層（prose）agent**，標的 BESI（2026-10-25）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BESI_20261025/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：BESI　日期：2026-10-25　archetype：None　前份裁決：2026-07-10　觀望｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1843B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（838B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（996B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1502B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1090B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（390B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（689B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2043B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4721B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2232B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1843           3610-5157      5 條（2–6 內）  
s3                  8000         838           5013-7162      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3588          7988-11412      5 條（2–6 內）  
s6                 11000         390          7427-10610      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         689           1968-2811      5 條（2–6 內）  
s10                 5000        2043           2070-2957      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2232           2000-2768      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5077B；至少需散文≈39.92KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65%
−65
−60%
−45
−45%
−42.3%
−42.1
−42%
−9.7%
−3.2%
0
0.5
0.54
0.55%
0.6
0.75
0.79
0.84
0.9
1
01
1.09
1.1
1.2
1.21
1.5
1.59%
1.6
1.66
1.7
02
2
2.2
2.5
2.7
2.9
3
3.4%
3.6
3.67
4
4.6
4.96
5
5.0%
5%
5.6
06
6
6.5
6.9
7
07
7.27
7.3
7.4
7.8
08
8
8.1%
8.3
8.4%
8.8
9%
9
9.31
10%
10
10.2
10.5
11.3
11.4
11.6
12
$12
13.21%
13.4%
13.4
14
15%
15
15.6
16
16.4%
18
19%
19.9%
19.96
20%
20
20.1
21
22
23
23.08%
24
25
25%
26
27
27%
27.4
28
28%
29
29.25
30%
30.4
31.09%
32
32%
35
35%
36.36%
37%
37.8%
40
40%
42
42%
42.1%
42.3%
42.49%
43
43%
43.0%
44.9%
45
45%
48.18%
49%
49
49.4%
50
52
52.7
55%
55
55.1
55.9%
56.4%
57.35%
58%
60%
60
62%
63
64.25%
64.9%
65%
65.2%
66.1
69%
70
70%
75%
84
90
96%
100%
100
104
107.2
113.6%
125.4
131.6
145
145.1
146
150%
173
174
179%
180
185
210
215
230
246.6
250
251
251.4
254.4
280
283.4
297
300
323.7%
342.6
350
401
432
578
591
718
2019
2023
2025
2026
2027
2028
2029
2030
2031
042700
20261025
1,000
1,150
2,200
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
{"meta":{"ticker":"BESI","date":"2026-10-25","schema":"v15.2","contract":"v19","company_name":"BE Semiconductor Industries N.V."},"oneliner":"混合鍵合龍頭的訂單與獲利仍在加速，股價半年跌四成，反映對手開始出貨、記憶體導入延後與 ASML 疑慮；兩年後本益比約 20 倍已不貴，但第二供應源風險要等 Q4 訂單與一月策略檢討結論才看得清。","thesis":{"H":[{"id":"H1","text":"混合鍵合由邏輯擴散到 CPO 與邊緣 AI，BESI 維持首選供應商地位，客戶數與累計需求持續成長","2y":"2027 年底公司揭露累計需求≥350 台、客戶≥28 家","5y":"累計需求達公司低情境 1,150 台的一半以上","10y":"混合鍵合成為 3D 堆疊標準製程，BESI 仍為最大供應商","threshold":"累計需求每季增量≥20 台；主要客戶未公開向對手下量產訂單","source":"公司季報新聞稿與法說；TrendForce、Bits&Chips 的競爭報導","drift_rule":"5 年論點：連 4 季累計需求增量低於 20 台為削弱，連 6 季為反轉；任一主要客戶公開向對手下量產訂單即削弱"},{"id":"H2","text":"AI 帶動的先進封裝資本支出上行延續到 2027 年，訂單維持高檔、毛利率守住長期區間","2y":"2027 年各季訂單≥€250M、毛利率≥62%","5y":"跨過一次消化期後，2031 年 EPS 高於 2027 年","10y":null,"threshold":"單季訂單≥€250M；毛利率≥62%；FY2 共識 EPS≥6.5","source":"公司季報新聞稿與法說；Koyfin 共識快照","drift_rule":"2 年論點：連 2 季訂單低於門檻 5% 以上為削弱，連 3 季低於 10% 以上為反轉"},{"id":"H3","text":"記憶體廠在 HBM4E 或 HBM5 世代（2027–2029 年）至少一家量產導入混合鍵合，且使用 BESI 機台","2y":"2027 年底前至少一家記憶體廠公布量產導入世代","5y":"三大記憶體廠中至少兩家量產採用","10y":null,"threshold":"2027-12 前有一家量產宣布","source":"記憶體廠法說與技術發表、BESI 法說、TrendForce","drift_rule":"5 年論點：連 4 季無新的記憶體混合鍵合訂單為削弱，連 6 季為反轉"}],"R":[{"id":"R1","text":"循環見頂與訂單消化：擴產集中在少數客戶，單一客戶延後即可讓單季訂單驟降，歷史下行期營收曾年減約 45%","h_ref":"H2","clock":"⚡","threshold":"單季訂單連 2 季低於 €230M，或訂單對營收比連 2 季低於 0.9","evidence_refs":["cyclical_prior_downcycle_behavior#0","customer_concentration_credit#1"]},{"id":"R2","text":"記憶體延後：SK hynix 據報把混合鍵合延到 HBM5，記憶體缺貨讓客戶沿用既有製程，HBM 曲線延後 1–2 年以上","h_ref":"H3","clock":"🔥","threshold":"2027 年底前三大記憶體廠無一公布量產導入世代","evidence_refs":["supply_demand_durability#3"]},{"id":"R3","text":"第二供應源侵蝕：ASMPT、Süss、Shibaura 已出貨，韓廠四家與約二十個平台追趕，台積電可能導入第二家，另有 ASML 進入傳聞","h_ref":"H1","clock":"🐢","threshold":"任一主要邏輯或記憶體客戶公開向對手下混合鍵合量產訂單","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_second_source#1","substitute_technology#0","substitute_technology#2","substitute_technology#3","geo_supply_chain#1","cyclical_supply_discipline_capacity#1","end_markets#2"]},{"id":"R4","text":"地緣與出口規範：Q3 訂單約四成來自中國，出口規則、客戶集中與匯率會影響利潤的可預測性","h_ref":"H2","clock":"🔥","threshold":"荷蘭或美國對鍵合設備新增對中出口限制，或中國訂單占比單季腰斬","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"台積電公開把混合鍵合量產訂單分給第二家供應商","why_fatal":"台積電是最重要客戶，混合鍵合是成長與高毛利的來源；最大客戶一旦雙供應，份額與定價同時被壓，牛市情境失效，基本情境的毛利率假設要下修","if_happens":"持有者減碼至半倉，未持有者不建倉；重跑情境，熊市機率提高到 40% 以上","how_monitor":"季報客戶揭露、對手訂單公告、TrendForce 與 Bits&Chips 產業報導，每季檢查","probability":"約 30%（12–24 個月；目前僅為評論，未見確認報導）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":19.96,"peg_fy2":0.54,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":1.66,"FY2026E":4.96,"FY2027E":7.27,"FY2028E":9.31},"fy_end_month":12,"eps_basis":"共識 EPS 取自 Koyfin 快照（事實表標示美元）；FY2025A 1.66 取自年度財報稀釋 EPS，幣別未標示（推測為歐元），以此為基期的三年成長率會被幣別差異高估，判斷改以 FY1→FY3 年化約 37% 為準"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BESI_20261025/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"後段設備資本支出循環，內含混合鍵合結構成長曲線"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：管理層自述上行週期約 6–8 季後過剩（2026-07-23 法說），本輪訂單倍增已約四季；混合鍵合屬結構需求，但訂單時點受少數客戶擴產左右","bargaining":{"up":"外包供應鏈與營運模式可讓產能年增約 70%，上游成本上升已轉嫁漲價，未見上游議價壓力","down":"客戶集中於台積電與三大記憶體廠，前一兩大客戶占比事實表未涵蓋；單一客戶擴產即可左右單季訂單","geo":"Q3 訂單約四成來自中國；荷蘭國安審查與出口規範是政策變數，管理層正減少機台中的美國零件"},"profit_pool_dir":"利潤池往先進封裝與混合鍵合遷移；BESI 過去四季毛利率 64.25%，高於 KLIC 48.18%、AMAT 49.4%","tam_table":[{"item":"封裝設備市場（TechInsights）","value":"2026 年成長 37%；2028 年達 $12B（Q3 法說轉述）"},{"item":"混合鍵合累計機台需求（公司模型）","value":"低情境 1,150 台、高情境 2,200 台（2026-06-18 投資人日）"},{"item":"已實現累計需求","value":"超過 215 台，客戶 23 家（Q3-26）"},{"item":"滲透率","value":"約 10–19%（215 台對 2,200／1,150 台，分母為公司自估）"},{"item":"主流晶粒貼合可及市場","value":"約 €1.6B，至 2030 年約成長 2 倍（投資人日）"},{"item":"公司長期營收目標","value":"€1.7–2.2B，營業利益率 45–55%（2026-06 上調）"},{"item":"利潤池占比 5 年前→現在","value":"事實表未涵蓋"}]},"moat":{"mechanism":"放置精度路線圖領先＋客戶產線驗證逾三年的轉換成本＋與 Applied Materials 的整合平台","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"客戶 15→23 家、混合鍵合訂單較 2025 全年翻倍、毛利率守在 63–65%；但 ASMPT、Süss、Shibaura 已出貨，約二十個平台開發中，評論指台積電預期導入第二供應商，管理層自承下一輪精度世代競爭者會切入","threats":[{"level":"🔴","text":"韓廠（SEMES 隸屬三星、Hanmi、Hanwha、LG）與 ASMPT、Süss、Shibaura 推出混合鍵合機，約二十個平台開發中；記憶體客戶有自家體系供應商可扶植，下一輪 50nm／25nm 世代是切入點","p":"35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#1","substitute_technology#0","substitute_technology#2","substitute_technology#3","geo_supply_chain#1","cyclical_supply_discipline_capacity#1"]},{"level":"🟡","text":"最大邏輯客戶台積電導入第二家混合鍵合供應商（產業評論，未確認）","p":"30%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"ASML 進入晶片對晶圓混合鍵合（賣方報導，ASML 未公布產品或時程）","p":"15%","evidence_refs":["competitive_share_entrants#2","end_markets#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（營業利益率 36.36%；周轉率事實表未涵蓋，依外包供應鏈、可快速擴產的營運模式推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是代工與記憶體廠的封裝產線，決策者實為終端 GPU 大廠（管理層：最終客戶會指定要混合鍵合），付款者是代工與記憶體廠，三角色都成立。客戶要解決的是頻寬、功耗與散熱，混合鍵合是目前最佳解法之一；但記憶體缺貨時客戶先用既有製程滿足需求，急迫性不等於持久性，時點可延後。"},{"item":"決策層級","level":"🟡","text":"替代性在客戶單一製程站點衡量：台積電驗證逾三年，換供應商要重新驗證，轉換成本高；但領先客戶已有約 60 台裝機，擴產時引進第二家的成本最低，評論指台積電預期導入第二供應商。"},{"item":"價值鏈分配","level":"🟡","text":"BESI 毛利率 64.25% 高於前段設備商 AMAT 49.4%，在鏈上分到的比例高；但買方集中於少數代工與記憶體廠，議價力強，且 Applied Materials 同時是夥伴與持股約 9% 的股東，整合平台若由 AMAT 主導，價值可能往前段移。"},{"item":"社會容忍度","level":"🟡","text":"企業對企業設備，沒有消費端漲價的政治壓力；但 Q3 訂單約四成來自中國，荷蘭與美國出口規範、荷蘭國安審查是政策上限，管理層已在減少機台中的美國零件。"}],"roiic":"事實表未涵蓋（投入資本、資本支出與折舊未列）；營收由 FY2025 €591M 增至 2026 前三季 €718M，營業費用占營收下降，增量報酬方向偏高但無法量化","reinvest_rate":"低：FY2025 淨利 €131.6M，2026 Q2 支付年度股利 €125.4M，另有每年 €100M 回購，盈餘大部分配回股東；確切比率事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長＝增量報酬率×再投資率；兩者都缺數字，只能判斷內生上界明顯低於共識 EPS 成長，差額來自循環營運槓桿"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","BESI":64.25,"KLIC":48.18,"ASMPT":null,"042700.KS":57.35,"AMAT":49.4,"unit":"%"},{"metric":"營業利益率","BESI":36.36,"KLIC":13.21,"ASMPT":null,"042700.KS":42.49,"AMAT":31.09,"unit":"%"},{"metric":"FCF 利潤率","BESI":23.08,"KLIC":4.21,"ASMPT":null,"042700.KS":18.69,"AMAT":18.23,"unit":"%"},{"metric":"研發密度","BESI":11.71,"KLIC":17.0,"ASMPT":null,"042700.KS":3.44,"AMAT":12.88,"unit":"%"}],"competitors":[{"name":"KLIC","gm":48.18,"om":13.21,"fcf_margin":4.21,"rd_intensity":17.0,"strategy_note":"主力在打線與熱壓鍵合，利潤率遠低於 BESI，混合鍵合未見具名量產訂單，目前不構成直接威脅","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ASMPT","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"熱壓鍵合份額約 35–40%，並已出貨混合鍵合設備，是最可能成為第二供應源的成熟對手；財務數字事實表未涵蓋"},{"name":"042700.KS","gm":57.35,"om":42.49,"fcf_margin":18.69,"rd_intensity":3.44,"strategy_note":"Hanmi 在 HBM 熱壓鍵合約占七成，投資約 1,000 億韓元建混合鍵合工廠，目標 2027 年底前推出，對記憶體客群是最近的威脅","period":"TTM ending 2026-06-30（4季加總）"},{"name":"AMAT","gm":49.4,"om":31.09,"fcf_margin":18.23,"rd_intensity":12.88,"strategy_note":"持股約 9%、與 BESI 共推整合平台，現階段是夥伴；若轉為自研或收購對手，關係會反轉","period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"量為主（機台數），價為輔（精度升級、成本轉嫁漲價）；無併購；回購每年約 €100M","runway_years":"5–9","runway_post_y5":"🟢","endo_ceiling_basis":"再投資率低（2026 Q2 股利 €125.4M 對 FY2025 淨利 €131.6M），內生上界無法精算但明顯低於共識 FY1→FY3 年化約 37%；缺口歸因於循環復甦下的利潤率擴張","segments":{"expanded":false,"reason":"分部營收拆分不在事實表；投資人日只給長期目標拆分（主流業務約 €1.1B、次微米 €0.6–1.1B），無當期數字可展開"},"decay_signals":["毛利率連兩季年減：未亮（Q3 65.2%，指引 63–65%；逐季年比數字事實表未涵蓋）","核心市占近 12 個月縮減：未亮（客戶數 15→23，未見對手具名量產訂單；可靠份額數據不存在）","提價後銷量下滑：未亮（轉嫁漲價同時訂單年增 96%）","EPS 成長高於營收成長逾 5 個百分點：亮（前三季淨利年增 179% 對營收 69%，循環營運槓桿）","自由現金流對淨利連兩年低於 0.75：無法判斷（年度自由現金流事實表未涵蓋）","股權酬勞占營收逾 5% 且上升：無法判斷（事實表未涵蓋）","可及市場萎縮或被替代：未亮但需監測（SK hynix HBM4 16 層保留 MR-MUF）","產業倍數三年系統性下移：無法判斷（同業倍數歷史事實表未涵蓋）","維護性資本支出占自由現金流逾六成：未亮（輕資產外包模式）","停止投資新產能且營收三年內下滑：未亮（越南廠擴產中）"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近年無收購；現金去向以股利與回購為主，四分拆解數字事實表未涵蓋"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無收購，管理層表明以夥伴關係為主","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"FY1 盈餘殖利率約 3.4%、FY2 約 5.0%；十年期殖利率不在證據包","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"股權酬勞與年度稀釋率事實表未涵蓋；2026 年可轉債轉股曾稀釋","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY1／FY2 共識 EPS）","tier":"高毛利後段設備","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比，無法做倍數對照"},"fwd_pe":29.25,"peg":0.79,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 29.25 倍、FY2 約 20 倍，成長調整後約 0.79；但獲利處於循環上行段，FY2、FY3 共識開始小幅下修，五年分位缺資料，判合理不判便宜","upside_short_pct":20.1,"upside_mid_pct":27.4},"trap_analysis":{"verdict":"🟡","label":"循環獲利放大＋對手開始出貨"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2019 上半年營收年減 44.9%、2023 全年年減 19.9%；管理層說上行週期約 6–8 季後過剩，本輪訂單倍增已走約四季；2026 Q1 混合鍵合成長主要來自單一客戶擴產","assumption":"AI 資本支出上行延續到 2028 年","consequence":"若 2027 下半年見頂，疊加台積電雙供應與記憶體延後，EPS 在 2029 年谷底回到約 3.6，終端 5.6 配 15 倍，股價較現價再跌約四成","ruling":"採納：熊市機率維持 32%，以單季訂單與訂單對營收比作為最早警訊；與唯一致命點部分重疊（雙供應），故唯一致命點只看台積電事件，本條看循環","watch":"單季訂單、訂單對營收比、管理層對產能過剩的說法","evidence_refs":["cyclical_prior_downcycle_behavior#0","customer_concentration_credit#1","supply_demand_durability#3"]},{"view":"論點成功但股東經濟變差","evidence":"約二十個平台開發中，ASMPT、Süss、Shibaura 已出貨；管理層自承下一輪精度世代競爭者會切入；Q4 營業費用因策略顧問費增加 5–10%","assumption":"混合鍵合成為主流時 BESI 仍能維持 63–65% 毛利率","consequence":"技術普及但價格競爭使毛利率降到 55% 左右、研發支出上升，營收達標而 EPS 不達標","ruling":"部分採納：2019 與 2023 年下行期毛利率仍守在 55.9% 與 64.9%，定價韌性有歷史支持，但當時沒有混合鍵合對手；基本情境假設毛利率守在 60% 以上，低於 60% 即轉向熊市情境","watch":"季度毛利率、對手具名量產訂單","evidence_refs":["substitute_technology#0","substitute_technology#2","geo_supply_chain#1","customer_second_source#1"]},{"view":"價格已反映太多","evidence":"FY1 本益比仍有 29.25 倍；FY2、FY3 共識 EPS 開始下修 0.55% 與 1.59%；Q4 營收指引持平；BofA 降評並砍半目標價","assumption":"FY2 約 20 倍代表便宜","consequence":"若獲利處於循環高段，前瞻本益比低估真實倍數，股價下跌 42% 也不構成安全邊際","ruling":"部分反駁：股價已從約 40 倍修正到 29 倍，ASML 疑慮已反映在價格；但共識開始下修，故不追價，只在事件確認後建倉","watch":"共識 EPS 修正方向、Q4 訂單","evidence_refs":["end_markets#2","competitive_share_entrants#2"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 251.4 → 本次 145.1（-42.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=251.4","side_b":"本次 price_at_dd=145.1","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 ✅→🟠、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 251.4 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 251.4 美元：Bull 價 578、Bear 價 146，五年期望值 +43.0%，基準年化 8.4%，不對稱比 2.7","side_b":"本次情境、股價仍用 251.4 美元：Bull 價 432、Bear 價 84，五年期望值 −9.7%，基準年化 −3.2%，不對稱比 0.84","ruling":"先換情境、股價不動：五年期望值少 52.7 個百分點，基準年化少 11.6 個百分點。不對稱比由 2.7 變為 0.84。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 251.4 美元：五年期望值 −9.7%，基準年化 −3.2%，不對稱比 0.84","side_b":"本次情境、股價 145.1 美元：五年期望值 +56.4%，基準年化 8.1%，不對稱比 3.67","ruling":"再換股價、情境不動：起點價下跌 42.3%，五年期望值多 66.1 個百分點，基準年化多 11.3 個百分點，不對稱比由 0.84 升到 3.67。合計五年期望值比前份多 13.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"ASML 是否進入晶片對晶圓混合鍵合","cause":"新證據","prior_field":null,"side_a":"BofA（2026-10-06）：ASML 進入混合鍵合是股價未反映的威脅，降評至中立並將目標價砍半","side_b":"管理層（2026-10-22 法說）：ASML 不是競爭者，其方向是晶片內 3D 電晶體堆疊，雙方合作研究晶粒應力","ruling":"方向相反，依證據裁決採管理層一側：ASML 未公布產品或時程，BofA 本身也不假設其取得顯著份額；但管理層說法無第三方佐證，保留為風險而非排除","evidence_level":"賣方報導與管理層說法，皆無產品證據","settle_metric":"ASML 是否公布晶片對晶圓鍵合產品或客戶評估","if_then":["若 ASML 在 2027 年內公布晶片對晶圓混合鍵合機台並有客戶評估，停止加碼，已持有者減碼一半","若 ASML 2027 年投資人日仍只談晶圓對晶圓與晶片內堆疊，移除此風險權重，牛市機率回到 28%"],"evidence_refs":["competitive_share_entrants#2","end_markets#2"]},{"axis":"記憶體導入混合鍵合的時點","cause":"新證據","prior_field":null,"side_a":"2026-06-18 投資人日，Peter Wiedner：第一家 HBM 廠將在 2027 年的 HBM4E 導入混合鍵合","side_b":"2026-10-22 法說，Richard Blickman：確切時點我們不知道，採用較優技術「有所延後」；另有報導稱 SK hynix 延到 HBM5","ruling":"程度差異，可調和：方向未變（Q3 有記憶體客戶同時下混合鍵合與 TC Next 訂單），時點延後；前份風險門檻「16 層前明示不導入」已對 SK hynix 一家觸發，牛市機率因此由 28% 降到 25%","evidence_level":"管理層前後說法＋產業報導","settle_metric":"2027 年記憶體廠量產導入公告","if_then":["若 2027 年中前有記憶體廠宣布 HBM4E 量產採混合鍵合，牛市機率回到 30%","若 2027 年底前無一公告，停止加碼並把記憶體曲線移出基本情境"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"訂單強勁與 Q4 營收持平","cause":"新證據","prior_field":null,"side_a":"Q3 訂單 €342.6M、年增 96%，管理層稱動能延續到 Q4","side_b":"Q4 營收指引持平 ±5%，有分析師解讀為客戶延後","ruling":"程度差異，可調和：管理層說明為整線交期安排，部分 Q3 訂單排到 2027 上半年出貨，訂單對營收約 1.21 倍支持此說；以 Q1-27 營收指引驗證","evidence_level":"公司指引與法說問答","settle_metric":"Q1-27 營收指引是否季增","if_then":["若 Q1-27 營收指引季增，交期說法成立","若 Q1-27 再持平或下滑且單季訂單低於 €280M，視為消化開始，檢查減碼條件"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2 本益比約 20 倍、淨現金 €246.6M、訂單年增 96%、客戶 23 家；股價下跌主要來自 ASML 傳聞與收購溢價退去，不是基本面","side_b":"關鍵約束是第二供應源與記憶體時點，兩者在 Q4 財報與一月策略檢討前沒有新證據；共識 FY2、FY3 已開始小幅下修","ruling":"觀望：約束是護城河能否扛住第二供應源，不是價格；事件確認前不追","evidence_level":"財報數字＋產業報導","settle_metric":"Q4-26 單季訂單與對手具名量產訂單","if_then":["若股價續跌而 Q4 訂單≥€280M、毛利率≥62%，分批反買首倉，不停損","若股價先漲回 52 週均線上方而事件未確認，不追"],"evidence_refs":[]},{"axis":"估值、機率、回撤區間與整體結論","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-07-10）：股價 251.4、FY1 本益比約 40 倍、估值偏貴；牛 28%／熊 32%；最大回撤 −60%；前份兩年驗證點「前瞻本益比不跌破 25 倍」","side_b":"本次：股價 145.1、FY1 29.25 倍、FY2 約 20 倍，估值合理；牛 25%／基本 43%／熊 32%；回撤區間 −45%～−65%；FY2 本益比已跌破 25 倍，市場不再為獨佔性付溢價","ruling":"估值由偏貴轉合理全由股價下跌造成，FY1 共識近三個月不變；品質與估值的綜合評級維持不變；牛市機率下調的原因另見記憶體時點一條；回撤改為區間表達，結論與倉位依新估值重算","evidence_level":"價格與共識快照","settle_metric":"股價與共識 EPS","if_then":[],"evidence_refs":[]},{"axis":"護城河方向、陷阱風險與循環位置","cause":"新證據","prior_field":["moat_trend","trap","cycle_position"],"side_a":"前份：護城河方向擴大、陷阱風險低、循環位置早循環","side_b":"本次：護城河方向穩定、陷阱風險中等、循環位置中循環","ruling":"護城河：ASMPT、Süss、Shibaura 已出貨、約二十平台開發、評論指台積電可能導入第二家（2026-06／07 報導），管理層自承下一輪世代競爭會切入，無法再判擴大；陷阱：EPS 成長高於營收成長的衰退訊號亮起，加上對手出貨；循環：訂單倍增已約四季，管理層自述上行週期 6–8 季，TechInsights 預期延續至 2027 年，判中循環，循環視角姿態為持有不加","evidence_level":"產業報導＋公司財報＋管理層說法","settle_metric":"對手具名量產訂單；單季訂單","if_then":["若 2027 上半年單季訂單仍≥€280M 且無對手量產訂單，護城河方向維持穩定","若對手取得具名量產訂單，護城河方向改判縮減並重跑情境"],"evidence_refs":["customer_second_source#0","substitute_technology#0","substitute_technology#2"]},{"axis":"五年後跑道與公司類型","cause":"新證據","prior_field":["runway_post_y5","archetype"],"side_a":"前份：五年後跑道寬，類型為循環／商品","side_b":"本次：維持跑道寬，類型維持循環／商品（次類型品質複利成長）","ruling":"客戶數 15→23、累計需求逾 215 台，對公司自估 1,150–2,200 台仍屬低滲透，CPO 與邊緣 AI 是新增曲線，維持寬；記憶體延後只動時點，不動空間","evidence_level":"公司揭露","settle_metric":"累計需求台數與客戶數","if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"價格回落至 Fwd PE FY2027 ~28-32x（約 €180-210）；且／或 HBM4 混合鍵合 design-win 確認（≥2 家記憶體廠量產）化解 7/7 遞延疑慮","side_b":"Q4-26 單季訂單≥€280M，且主要客戶未公開向對手下混合鍵合量產訂單；兩者成立才重跑判斷建首倉","ruling":"價格條件已失效：FY2 本益比約 20 倍，低於前份 28–32 倍區間，價格不再是約束；關鍵約束改為第二供應源與訂單延續，進場首倉改綁事件、不設進場價；條件反向（訂單連兩季 <€230M）則轉為減碼","evidence_level":"價格與財報","settle_metric":"Q4-26 訂單與對手量產訂單","if_then":["條件成立：重跑判斷，通過則分批建首倉","訂單連兩季 <€230M：減碼一半"],"evidence_refs":[]},{"axis":"清倉／減碼指標與風險門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉／減碼指標；風險門檻用「混合鍵合份額掉出 60%」與「訂單年增率連 2 季 <0」","side_b":"本次設四項：訂單連 2 季 <€230M 減碼一半、毛利率連 2 季 <60% 減碼、主要客戶公開向對手下量產訂單減碼一半、FY2 共識 <6.5 停止加碼；份額門檻改為具名訂單事件","ruling":"份額數據各來源互相矛盾（75%、42%、49% 並存），不能當可觀察門檻，改用具名訂單事件；訂單門檻由年增率改為絕對金額，因基期翻倍後年增率會機械轉負","evidence_level":"方法調整","settle_metric":"季報訂單、毛利率、共識快照","if_then":[],"evidence_refs":["competitive_share_entrants#5"]},{"axis":"唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份唯一致命點未設定（null）","side_b":"Single Thing：台積電公開把混合鍵合量產訂單分給第二家供應商","ruling":"Single Thing 新設：2026 年 6 月評論指台積電預期導入第二家，加上多家對手已出貨，最大客戶雙供應是對份額與毛利影響最大的單一事件","evidence_level":"產業評論，未確認","settle_metric":"主要客戶具名第二供應源訂單","if_then":["發生則減碼至半倉，未持有者不建倉"],"evidence_refs":["customer_second_source#0"]}],"triggers":[{"n":1,"text":"Q4-26 財報檢查訂單是否延續","type":"假設驗證","maps_to":"H2","metric":"單季訂單（€M）","threshold":"≥€280M 為確認；<€230M 為警訊","action":"確認且無對手量產訂單：重跑判斷建首倉；警訊：延長觀望","source_freq":"公司季報，每季","date":"2027-02","evidence_refs":[]},{"n":2,"text":"台積電公開把混合鍵合量產訂單分給第二家","type":"Single Thing","maps_to":"Single Thing","metric":"主要客戶具名第二供應源訂單","threshold":"任一公開確認","action":"減碼至半倉；未持有則不建倉","source_freq":"產業報導與公司揭露，持續","date":null,"evidence_refs":["customer_second_source#0"]},{"n":3,"text":"記憶體廠混合鍵合量產世代公告","type":"風險","maps_to":"R2","metric":"三大記憶體廠量產導入公告","threshold":"2027-12 前無一公告","action":"停止加碼，牛市機率降到 15%","source_freq":"記憶體廠法說，每季","date":"2027-12","evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"循環消化","type":"減碼","maps_to":"R1","metric":"單季訂單與訂單對營收比","threshold":"訂單連 2 季 <€230M 或比值連 2 季 <0.9","action":"減碼一半","source_freq":"公司季報，每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","customer_concentration_credit#1"]},{"n":5,"text":"對手取得具名量產訂單，或 ASML 公布晶片對晶圓鍵合產品","type":"風險","maps_to":"R3","metric":"對手具名混合鍵合量產訂單／ASML 產品公告","threshold":"任一出現","action":"停止加碼並重跑護城河評估","source_freq":"TrendForce、Bits&Chips、ASML 投資人日，持續","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","cyclical_supply_discipline_capacity#1"]},{"n":6,"text":"一月策略檢討結論","type":"複審日期","maps_to":"H1","metric":"管理層公布的混合鍵合、TC Next 與回焊路線及 3–5 年需求","threshold":"長期目標或混合鍵合需求情境下修","action":"下修則維持觀望並重估牛市機率；維持或上修則與 Q4 財報一併複審","source_freq":"公司公告，一次","date":"2027-01","evidence_refs":[]},{"n":7,"text":"出口規範收緊","type":"風險","maps_to":"R4","metric":"對中出口限制、中國訂單占比","threshold":"新增鍵合設備對中限制，或中國訂單占比單季腰斬","action":"減碼三分之一並重跑情境","source_freq":"荷蘭與美國政府公告，持續","date":null,"evidence_refs":["geo_supply_chain#0"]},{"n":8,"text":"重新評估進場","type":"估值rearm","maps_to":"H1","metric":"Q4 訂單與第二供應源事件","threshold":"單季訂單≥€280M 且無對手具名量產訂單","action":"重跑判斷，通過則分批建首倉","source_freq":"每季","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"單季訂單（€M）","bear_threshold":"連 2 季 <€230M（減碼一半）","window":"2027-Q1～2027-Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"季度毛利率","bear_threshold":"連 2 季 <60%（減碼）","window":"2026-Q4～2027-Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"主要邏輯或記憶體客戶向對手下混合鍵合量產訂單","bear_threshold":"任一公開確認（減碼一半）","window":"未來 24 個月","source":"公司揭露、TrendForce、Bits&Chips","last_status":"warning"},{"metric":"FY2 共識 EPS","bear_threshold":"低於 6.5（停止加碼）","window":"未來 6 個月","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 ASML 進入與記憶體延後當成護城河崩解來定價，但 ASML 未公布晶片對晶圓產品、管理層稱雙方合作研究晶粒應力，Q3 訂單年增 96%、客戶增至 23 家；部分跌幅是 3 月收購傳聞溢價退去，不是基本面惡化"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-42.1, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027 年 2 月 Q4-26 財報：單季訂單≥€280M，且主要客戶未公開向對手下混合鍵合量產訂單；2027 年 1 月策略檢討結論同時參考'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"Q4-26 單季訂單≥€280M，且主要客戶未公開向對手下混合鍵合量產訂單；兩者成立才重跑判斷建首倉","exec_line":"條件成立後分兩批：首批在 Q4 財報後，次批待一月策略檢討未下修長期目標；若股價先跌而訂單與毛利率未惡化，分批反買、不停損；股價先漲而事件未到，不追"},"reasoning":{"industry":"Q3-26 營收 €283.4M，年增 113.6%、季增 13.4%；毛利率 65.2%，淨利 €107.2M（淨利率 37.8%），營業費用 €55.1M。訂單 €342.6M，訂單對營收約 1.21 倍（342.6÷283.4），近四季訂單 €1.2B（Q3 法說）。成長來源依法說為混合鍵合、光子與資料中心，另有 AI 伺服器電源管理；車用由過去占營收 15–20% 降到約 10%（Q3 法說）。Q3 訂單約四成來自中國（Q3 法說問答）。分部營收與前幾大客戶占比事實表未涵蓋。單點依賴：台積電被產業評論列為最重要客戶，2026 Q1 混合鍵合成長主要來自單一客戶超預期擴產，客戶集中是風險，不是護城河證據。供需持久度：週期性將反轉——管理層自述過往上行週期約 6–8 季後出現產能過剩（2026-07-23 法說），混合鍵合的結構需求只能拉長循環，不能消除循環。產業時鐘判擴張期：TechInsights 把 2026 年封裝設備成長預估上調到 37%，並預期 2027 年延續（Q3 法說轉述），訂單連續數季倍增，尚未見消化。Q4 指引營收持平 ±5%、毛利率 63–65%，管理層解釋為整線交期安排，不是客戶延後。","moat":"機制：放置精度路線圖領先（已售 215 台皆為 100nm 世代，本季開始出貨 50nm，25nm 開發中，Q3 法說）＋客戶驗證週期長（台積電驗證逾三年，2026-07-23 法說）＋與 Applied Materials 的整合平台。同業報酬率事實表未涵蓋，改用利潤率對照：BESI 過去四季毛利率 64.25%，高於 KLIC 48.18%、Hanmi 57.35%、AMAT 49.4%；營業利益率 36.36% 高於 KLIC 13.21%、AMAT 31.09%，但低於 Hanmi 42.49%（Hanmi 在 HBM 熱壓鍵合約占七成，屬不同機台）。客戶數 15→21→23 家，2026 年混合鍵合訂單已是 2025 全年兩倍以上，2026 年未見對手取得具名量產訂單。反方：ASMPT、Süss、Shibaura 已出貨混合鍵合設備，全球約二十個平台開發中，韓廠四家爭取三星與 SK hynix；管理層在投資人日自承「競爭者會在下一輪切入」「是否擁有最好的鍵合機仍是挑戰」。執行力判擴大（產能可年增約 70%，營業費用占營收由 32% 降到 16.4%），定價力判穩定（毛利率維持 63–65% 指引），合併為穩定。產業態勢：雙向拉鋸——競爭惡化（對手出貨、ASML 傳聞）對上結構轉好（混合鍵合由邏輯擴及 CPO、邊緣 AI 與記憶體），出口規範與荷蘭國安審查是另一項結構變數。投入資本事實表未涵蓋，當期報酬率無法精算。","growth":"成長以量為主（機台數），價為輔（精度升級提高單價、成本轉嫁漲價），無併購，回購規模小。共識 EPS：FY1 4.96、FY2 7.27、FY3 9.31，FY1→FY3 年化約 37%；最近一次快照 FY2、FY3 各下修 0.55%、1.59%，FY1 近三個月不變。內生上界：盈餘多數配回股東，再投資率低，內生成長明顯低於 37%；缺口歸因於利潤率擴張（營業費用占營收由 32% 降到 16.4%，毛利率回到 65%）與循環復甦，可歸因，但會隨循環反轉。跑道：215 台對公司高情境 2,200 台約一成，對低情境 1,150 台約兩成；以 2026 年訂單翻倍的速度推，約 5–9 年到三成滲透。管理層 6 月投資人日說首家 HBM 廠 2027 年在 HBM4E 導入，Q3 法說改口「確切時點我們不知道」並承認採用「有所延後」，SK hynix 據報延到 HBM5，記憶體曲線延後 1–2 年列為基本假設。衰退訊號亮一個：EPS 成長顯著高於營收成長（法說：前三季營收年增 69%、淨利年增 179%），屬循環營運槓桿。","governance":"期末淨現金 €246.6M，較去年同期增加 €254.4M（Q3 法說）；自 2026-10-27 起回購計畫擴大到每年 €100M；2026 Q2 支付年度股利 €125.4M，可轉債已轉股（2026-07-23 法說），股數曾被稀釋。過去四季自由現金流利潤率 23.08%；自由現金流對淨利轉換率、股權酬勞占營收、現金去向四分比例事實表未涵蓋。管理層對併購的說法是「產業併購近乎不存在，以夥伴關係為主」，近年無收購，併購報酬一項不適用。回購買入收益：FY1 本益比 29.25 倍換算盈餘殖利率約 3.4%，FY2 約 5.0%；十年期公債殖利率不在證據包內，無法判斷是否過門檻。營運槓桿：Q3 營收年增 113.6%、淨利年增 323.7%，未見壓縮。","valuation":"FY1 本益比 29.25 倍、FY2 約 20 倍（145.1÷7.27）、FY3 約 15.6 倍（145.1÷9.31）。成長調整後本益比：29.25 除以 FY1→FY3 年化 EPS 成長約 37%，約 0.79，落在便宜區；但分子分母都在循環上行段，景氣反轉時 EPS 會像 FY2022 2.9→FY2025 1.66 那樣回落，所以不以此論便宜。五年估值分位：事實表只有近期前瞻本益比，五年區間未涵蓋，無法計算。前份判斷時股價 251.4、FY1 本益比約 40 倍，現在下跌 42%；股價低於 52 週與 104 週均線、高於 250 週均線，RSI 30.4，屬超賣邊緣而非過熱。短期上行：一年後以基本情境 FY2028 EPS 8.3×21 倍約 174，約 +20%；中期三年以 FY2030 EPS 8.8×21 倍約 185，約 +27%。賣方目標價均值約 €297（2026-08，區間 €173–401）已過時且幣別不同，不採用。","premortem":"管理層多次迴避關鍵數字：不揭露混合鍵合出貨與訂單台數、不給 HBM 各客戶驗證時程、對產能過剩只答「沒人知道」、服務收入不給數字、對領先幅度未舉具體例證（2026-06-18 投資人日與 2026-07-23 法說問答）。這些空白正好落在論點最承重的三處：份額、記憶體時點、循環長度。歷史下行：2019 上半年營收年減 44.9%、2023 全年年減 19.9%，但毛利率兩次都守住（55.9%、64.9%），下行時傷的是量而非價。股價過去 26 週已跌 42.1%，部分反映 2026 年 3 月收購傳聞溢價退去與 10 月 BofA 降評。最強空方數字：FY2、FY3 共識 EPS 開始小幅下修，Q4 營收指引持平。訴訟與監管調查：證據包未見。"},"plain":{"six":{"how_it_makes_money":"賣後段鍵合設備給晶圓代工、記憶體廠與封測廠，錢卡在先進封裝「晶粒精準放置」這一節點；產業處於 AI 帶動的擴張期，但需求屬週期性，終將反轉。","moat":"護城河方向判穩定：混合鍵合領先與毛利率優勢仍在，但對手已開始出貨、最大客戶可能導入第二供應源，不再能判擴大。","growth":"跑道寬：混合鍵合累計需求約 215 台，對公司自估 1,150–2,200 台的累計空間，滲透約一至二成，且有 HBM、CPO、邊緣 AI 後續曲線；但分母是公司自估，記憶體導入時點已延後。","capital":"資本配置大致健康但多項無法驗證：淨現金轉正並擴大回購，盈餘多配回股東；三項計分中兩項缺數據。","valuation":"現價要求 2027 年 EPS 約 7.3 兌現、且循環不在 2028 年前明顯反轉；兩年後本益比約 20 倍，我大致相信獲利，但不相信競爭對毛利毫無影響，估值判合理而非便宜。","how_wrong":"最可能看錯在把循環高段獲利當常態，以及低估第二供應源進入的速度；陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 ASML 進入與記憶體延後當成護城河崩解來定價，但 ASML 未公布晶片對晶圓產品、管理層稱雙方合作研究晶粒應力，Q3 訂單年增 96%、客戶增至 23 家；部分跌幅是 3 月收購傳聞溢價退去，不是基本面惡化","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月 Q4-26 財報：單季訂單≥€280M，且主要客戶未公開向對手下混合鍵合量產訂單；2027 年 1 月策略檢討結論同時參考","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":145.1,"week26_return_pct":-42.1,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母為循環上行期的共識 EPS，不含一次性項目；事實表股價與共識 EPS 標示為美元，FY2025 實際 EPS 1.66 幣別未標（推測為歐元），三年成長率改以 FY1→FY3 計算，避免幣別混用"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"策略檢討結論（16 週客戶路線圖深度訪談，涵蓋混合鍵合、TC Next 與回焊的 3–5 年需求）","impact":"中","watch":"長期目標與混合鍵合需求情境是否變動"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4-26 財報與 Q1-27 指引","impact":"高","watch":"單季訂單是否≥€280M、Q1 營收指引是否季增"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"50nm 第二代混合鍵合機開始出貨","impact":"中","watch":"客戶驗證進度與重複訂單"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"記憶體廠 HBM4E 世代鍵合技術選擇","impact":"高","watch":"是否宣布量產採混合鍵合"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"美國邏輯客戶亞洲擴產與領先代工 AP7 擴產","impact":"中","watch":"新一輪混合鍵合訂單"}],"_projected_from":"v19"}
```
