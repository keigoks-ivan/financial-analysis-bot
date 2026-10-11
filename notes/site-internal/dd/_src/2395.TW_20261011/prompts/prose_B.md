你是 stock-analyst v20 的**散文層（prose）agent**，標的 2395.TW（2026-10-11）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2395.TW_20261011/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：2395.TW　日期：2026-10-11　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1434B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（791B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1140B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1554B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1369B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（670B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（672B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2061B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4364B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2298B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1434           3896-5566      5 條（2–6 內）  
s3                  8000         791           5046-7209      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4063          7656-10937      5 條（2–6 內）  
s6                 11000         670          7231-10330      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         672           1980-2828      5 條（2–6 內）  
s10                 5000        2061           2057-2939      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2298           2000-2702      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5785B；至少需散文≈39.22KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−99%
−60%
−60
−56%
−53%
−40%
−40
−35%
−34%
−20%
−18%
−17%
−15%
−10%
−1.44%
−0.3
−0.3%
0
0.07
0.2%
0.557
0.65
0.75
0.77
0.99
1
1.0
1.1%
1.1
1.2
1.21
1.21%
1.25
1.44
1.5%
1.535
1.535%
1.64
1.92
2%
2
2.2
2.31
3
03
3.3%
3.5
3.51
4
4%
4.29%
5%
5
5.20
5.78%
6
06
6.08%
6.5
6.51
6.66%
7
7%
7.20
7.41%
7.48
7.69
8%
8
08
8.33
8.6%
9%
9
9.05
9.78%
10%
10
10.38
11
11.2
11.4
11.46%
11.7%
12
12.14
12.46
14%
14
14.6%
14.7
14.84%
15%
15
15.5
15.53
15.71
16%
16
16.5
16.6%
17%
17.97%
18
18%
18.5
18.6%
19%
19.5
19.6%
20%
20
20.33%
21.3
21.3%
22
22.5%
23
23%
24
25
25%
25.57%
25.9%
26
26.5
27%
27
28%
28
28.5%
29
30%
30
31
31%
31.5
33%
33.62%
34%
34.2%
35%
35
35.49%
36%
36
36.1%
37%
37.7%
38%
38
39.0%
39.78%
40%
40.77%
41
42
43%
45
45%
45.18
46
46%
46.28
49
50%
51%
52%
60%
64%
70
86%
88%
90
92%
93%
100%
100
113%
113.4
113.4%
116
127%
130
150%
209.08
232
250%
261.26
300
400
453
502
628
700
725
727
727.0
750
800
882
2022
2023
2024
2025
2026
2027
2028
2029
2030
2031
2395
2397
3088
6166
6414
20261011
1,068
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
{"meta":{"ticker":"2395.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"研華"},"oneliner":"全球工業電腦份額第一，邊緣 AI 帶動訂單與獲利創高；但現價已是樣本最高倍數，部分訂單是零組件短缺下的提前下單，等價格回落或接單消化的證據再談","thesis":{"H":[{"id":"H1","text":"邊緣 AI 成為主要成長引擎：營收占比 FY2026 年底達 30%，2027 年不回落","2y":"FY2026 年底占比 ≥30%，FY2027 全年維持 ≥30%","5y":null,"10y":null,"threshold":"年底占比 ≥30%；低於 27% 視為未達","source":"研華每季法說會與公司新聞稿","drift_rule":"占比連兩季低於目標 5% 以上（<28.5%）為削弱，連三季低於目標 10% 以上（<27%）為反轉"},{"id":"H2","text":"上游成本可以轉嫁，毛利率回到公司財測區間","2y":"2027 年單季毛利率回到 38%–40%","5y":null,"10y":null,"threshold":"單季毛利率 ≥38%","source":"研華每季公司新聞稿與財報","drift_rule":"連兩季低於 38% 達 5% 以上（<36.1%）為削弱，連三季低於 10% 以上（<34.2%）為反轉；第二季 37.7% 低於財測，但還沒到削弱線"},{"id":"H3","text":"下一次消化期的盈餘底部明顯高於上一輪谷底，證明邊緣 AI 抬高了週期中樞","2y":null,"5y":"2027–2031 年任一年度 EPS 不低於 16 元（FY2024 谷底為 10.38 元），FY2031E 接近 Base 路徑的 31.5 元","10y":null,"threshold":"2027 年起最近四季 EPS ≥16 元","source":"研華季報與年報（GAAP 稀釋 EPS）","drift_rule":"最近四季 EPS 連四季低於 Base 路徑 5% 以上為削弱，連六季低於 10% 以上為反轉"}],"R":[{"id":"R1","text":"提前下單反轉，2027–2028 年進入庫存消化期","h_ref":"H3","clock":"⚡","threshold":"任一季整體接單出貨比 <1.0，或庫存天數 >130 天","evidence_refs":["supply_demand_durability#4"]},{"id":"R2","text":"上游記憶體、CPU、PCB 成本持續侵蝕毛利，轉嫁跟不上","h_ref":"H2","clock":"🔥","threshold":"單季毛利率連兩季 <37%","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#3"]},{"id":"R3","text":"美國關稅成本吸收失敗：北美約占三成營收，60% 北美訂單的關稅先由研華吸收","h_ref":"H2","clock":"🔥","threshold":"單季營益率連兩季 <16%，或主力產品列入 Section 232 衍生品課稅","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]},{"id":"R4","text":"中國本土低價 ARM 工業電腦與軟 PLC 侵蝕研華的中國份額","h_ref":"H3","clock":"🐢","threshold":"中國區營收連兩季年減，而整體營收仍在年增","evidence_refs":["substitute_technology#2"]},{"id":"R5","text":"庫存與擴產長期吸走現金，配息靠資產負債表支應","h_ref":"H3","clock":"🔥","threshold":"FY2026 全年自由現金流／淨利 <30%，且 2027 上半年 <50%","evidence_refs":[]}],"single_thing":{"description":"未來 12–24 個月內，任一季整體接單出貨比跌破 1.0，代表提前下單開始消化","why_fatal":"現價是最近四季 EPS 的 46 倍，隱含多年高成長。接單一轉弱，EPS 路徑與倍數會同時下修：終端 EPS 從 Base 的 31.5 元掉到 Bear 的 19.5 元，倍數從 28 倍掉到 20 倍，這是情境樹裡最大的單一敏感項","if_happens":"不建倉；已持有者減碼至半倉、不攤平。等接單出貨比連兩季回到 1.0 以上、庫存天數降到 100 天以下，再重跑研究","how_monitor":"每季法說公布的整體與分區接單出貨比、月營收年增率、庫存天數","probability":"約 35%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":12.14,"FY2026E":null,"FY2027E":null,"FY2028E":null},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（TWD）；三年共識 EPS 與分析師家數事實表未涵蓋，FY2026E–FY2028E 留空，不另補"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2395.TW_20261011/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"高毛利、長尾客戶的工業電腦品牌。盈餘跟著工業資本支出與零組件庫存週期起伏：FY2023–FY2024 營收連兩年下滑，FY2022–FY2025 EPS 原地踏步。邊緣 AI 是結構性的第二曲線"},"industry":{"clock_phase":"II","sd_verdict_source":"供需分兩層。邊緣 AI 部署屬結構性持久：43% 的邊緣 AI 訂單交期超過六個月，客戶在規劃兩到三年的部署（媒體轉述）。記憶體短缺引發的提前下單屬週期性，將會反轉，2027–2028 年有消化期風險","bargaining":{"up":"上游記憶體、CPU、PCB 供應吃緊，議價權在上游；記憶體的成本壓力可能擴大到 CPU 與 PCB","down":"下游是分散的工業客戶。研華計畫轉嫁大部分關稅與新增成本，研究機構也認為需求強勁、轉嫁可行，但轉嫁有時間差","geo":"製造約台灣 45%、中國 45%，輸美出貨 93% 來自台灣；南加州第二個美國組裝據點預計 2026 年啟用；Section 232 是否涵蓋研華產品尚未確認"},"profit_pool_dir":"利潤池往軟硬整合的邊緣 AI 方案移動，研華邊緣 AI 營收占比從 2023 年 4% 升到上半年 22.5%；整體工業電腦利潤池的五年變化事實表未涵蓋","tam_table":[{"item":"全球工業電腦份額（2025）","value":"研華逾 8.6% 居首，前五大合計 25.9%"},{"item":"中國工業電腦份額","value":"研華逾 36%（無年度消長資料）"},{"item":"邊緣 AI 嵌入式 PC 年複合成長（2024–2030，第三方）","value":"14.6%，第三方口徑差異大"},{"item":"研華邊緣 AI 營收占比","value":"2023 年 4% → 2026 上半年 22.5%，目標年底 30%"},{"item":"AI 邊緣架構滲透","value":"視覺檢測已量產，軟體定義控制在早期量產，閉環製程控制仍在試點；第三方估約 2029 年成為新廠預設規格"},{"item":"TAM 金額、SAM 與營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"長尾工業客戶的設計導入與長生命週期出貨，加上最廣產品線與全球通路帶來的規模，換得約同業兩倍的營益率","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：接單出貨比第二季 1.44、7 月 1.64，邊緣 AI 營收占比從 2023 年 4% 升到上半年 22.5%。定價面縮減：第二季毛利率 37.7%，低於財測 38%–40%，年減 2.31 個百分點。兩者相抵判穩定；份額只有靜態值，沒有來源化的上升證據","peer_na_reason":null,"threats":[{"level":"🟡","text":"中國廠商推出低價 ARM 架構工業電腦，以及可跑軟 PLC 的邊緣控制器。這是點對點的價格攻擊，主要威脅中國市場與低階產品線","p":"25%","evidence_refs":["substitute_technology#2"]},{"level":"🟡","text":"上游記憶體短缺與成本上升侵蝕毛利：2025 年第三季毛利率約少 1 個百分點，2026 年第二季又低於財測，壓力可能擴大到 CPU 與 PCB","p":"40%","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#3"]},{"level":"🟡","text":"美國關稅：北美約占營收三成，60% 北美訂單的關稅先由研華吸收再向客戶請款；若 Section 232 衍生品範圍涵蓋主力產品，轉嫁能力會受考驗","p":"20%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]}],"roic_durability":{"quadrant":"高利益率；周轉率事實表未涵蓋（缺投入資本），庫存約 116 天，顯示營運資金負擔偏重","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"客戶要解決的問題是工廠、醫療、半導體設備的邊緣運算，屬於需要而非想要，延後購買會拖慢產線升級。但目前訂單水位含有記憶體短缺下的提前下單，急迫性不等於持久性；2022 年短缺之後，FY2023–FY2024 營收連兩年下滑就是前例"},{"item":"決策層級","level":"🟡","text":"替代發生在設備商選定平台的那一刻，換供應商要重新設計與驗證。但漲價後流失率、重新認證週期、合約年限等代理變數事實表未涵蓋，只能用份額第一與約同業兩倍的營益率間接佐證"},{"item":"價值鏈分配","level":"🟡","text":"上游記憶體與 CPU 供應集中，短缺時先拿走價值：2025 年第三季 DDR4 讓毛利率少了約 1 個百分點，2026 年第二季毛利率 37.7% 低於財測。研華能轉嫁大部分成本，但有時間差；價值鏈中最難取代的環節不是研華"},{"item":"社會容忍度","level":"🟢","text":"研華賣的是 B2B 工業硬體，不依賴監管授權，也沒有民生必需品式的漲價天花板；關稅屬政策成本，已列入風險，不是社會容忍度的問題"}],"roiic":"事實表未涵蓋（缺投入資本，無法計算增量報酬率）","reinvest_rate":"近四季約 93%（自由現金流只剩淨利約 7%）；FY2022–FY2025 約 2%–35%","endo_ceiling":null,"formula_note":"再投資率以 1−自由現金流÷淨利代理（淨利含業外，不是稅後營業利益）：FY2022 23%、FY2023 23%、FY2024 2%、FY2025 35%，近四季約 93%。近四季的淨利率約 16.6%，由 P/S 7.69÷P/E 46.28 推得；自由現金流利潤率 1.21%。近四季的高再投資有一部分靠資產負債表撐：每股配息約 11.2 元（殖利率 1.535%×727 元），約為 FY2025 EPS 12.14 元的 92%，也約為近四季每股自由現金流 1.1 元的十倍。可持續的保留率約 8%，即使增量報酬率達 50%，內生成長上限也只有約 4%/年。當期 ROIC 與增量報酬率都需要投入資本，事實表未涵蓋。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","2395.TW":39.0,"6414.TW":20.33,"6166.TW":35.49,"3088.TWO":33.62,"2397.TW":25.57,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","2395.TW":17.97,"6414.TW":5.78,"6166.TW":9.78,"3088.TWO":11.46,"2397.TW":6.38,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","2395.TW":1.21,"6414.TW":4.29,"6166.TW":6.66,"3088.TWO":3.3,"2397.TW":-1.44,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","2395.TW":7.43,"6414.TW":6.38,"6166.TW":11.7,"3088.TWO":8.79,"2397.TW":5.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"6414.TW","gm":20.33,"om":5.78,"fcf_margin":4.29,"rd_intensity":6.38,"strategy_note":"毛利率 20.33%、營益率 5.78%，約為研華的一半與三分之一，屬走量的成本結構，對研華的定價不構成直接壓力","period":"TTM ending 2026-06-30（4季加總）"},{"name":"6166.TW","gm":35.49,"om":9.78,"fcf_margin":6.66,"rd_intensity":11.7,"strategy_note":"毛利率 35.49%，最接近研華；但營益率 9.78% 只有研華一半多，研發密度 11.7% 為同業最高。產品面最接近的對手，規模不足以把毛利轉成營益","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3088.TWO","gm":33.62,"om":11.46,"fcf_margin":3.3,"rd_intensity":8.79,"strategy_note":"營益率 11.46% 為同業次高，毛利率 33.62%，自由現金流利潤率 3.3%，屬利基型對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"2397.TW","gm":25.57,"om":6.38,"fcf_margin":-1.44,"rd_intensity":5.26,"strategy_note":"毛利率 25.57%、自由現金流利潤率 −1.44%，價格導向；它同樣被營運資金吃掉現金，顯示備料壓力是全產業現象","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（接單出貨比 1.44、各事業群年增 19%–34%），組合為輔（邊緣 AI 專案毛利約 40%），另有部分成本轉嫁的價格成分；無併購與回購貢獻","runway_years":"≥10（全球份額 8.6%、前五大合計 25.9% 的分散市場）","runway_post_y5":"🟢","endo_ceiling_basis":"引報酬持續期的推導：保留率約 8%，即使增量報酬率達 50%，內生上限也只有約 4%/年。Base 路徑約 14%–15%/年，明顯超出上限，差額來自產能利用率、邊緣 AI 組合與週期","segments":[{"item":"iSystems","value":"上半年年增 34%（半導體設備、雲端網通設備）；營收占比事實表未涵蓋"},{"item":"Embedded","value":"上半年年增 28%（智慧醫療、自動化設備、機器人專案）"},{"item":"iAutomation","value":"上半年年增 19%（自動化設備、交通專案）"},{"item":"iService","value":"上半年僅個位數成長"},{"item":"邊緣 AI（跨事業群）","value":"營收占比 2023 年 4% → 上半年 22.5%，目標年底 30%，專案毛利約 40%"},{"item":"機器人","value":"上半年成長 250%，占比低"}],"decay_signals":[{"signal":"毛利率連兩季年減","status":"部分成立","evidence":"第二季年減 2.31 個百分點已確認，第一季事實表未涵蓋；FY2025 毛利率 39.78% 已低於 FY2024 的 40.77%"},{"signal":"核心市占近 12 個月縮減","status":"資料缺口","evidence":"只有靜態份額（全球逾 8.6%、中國逾 36%），沒有消長資料"},{"signal":"主力產品提價後銷量下滑","status":"不成立","evidence":"轉嫁成本的同時，接單出貨比仍有 1.44"},{"signal":"EPS 成長顯著高於營收成長","status":"不成立","evidence":"FY2022–FY2025 EPS 與營收都接近原地；近一年的差距來自營運槓桿與去年同季業外的低基期，不是多年趨勢"},{"signal":"自由現金流／淨利連兩年低於 0.75","status":"成立","evidence":"FY2025 為 0.65，近四季約 0.07；FY2026 全年待確認"},{"signal":"SBC 占營收逾 5% 且上升","status":"不成立","evidence":"第二季約 0.2%"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"不成立","evidence":"AI 推動買家由 PLC 轉向配備加速器的工業電腦，屬順風"},{"signal":"產業估值倍數近三年系統性下移","status":"不成立","evidence":"自身倍數位在年度端點最高；同業倍數事實表未涵蓋"},{"signal":"維護性資本支出占自由現金流逾 60%","status":"資料缺口","evidence":"第二季資本支出 7.20 億元、自由現金流 8.33 億元，維護與擴產的拆分事實表未涵蓋"},{"signal":"停止投資新產能且營收三年內下滑","status":"不成立","evidence":"美、日、台持續擴產"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，股東回饋以現金股利為主；回購與併購金額事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"併購金額與已實現報酬事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購金額與均價事實表未涵蓋；股東回饋以現金股利為主","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"第二季 SBC 0.557 億元，年化約 2.2 億元，相對市值的稀釋遠低於每年 1.5%","grade":"過"}]},"valuation":{"basis":"Trailing P/E（GAAP 稀釋 EPS），以情境樹終端倍數檢核","peers":{"expanded":false,"reason":"同業倍數事實表未涵蓋，事實表只收同業利潤率；終端倍數以自身現值與年度端點為錨"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"Trailing P/E 46.28 倍、P/S 7.69 倍、EV/S 7.48 倍都在四個年度端點中最高；連續五年分位事實表未涵蓋，所以五年分位欄留空。現價 727 元貼近法說後外資目標 700–750 元的中點。Base 情境五年終值約 882 元，年化價格報酬約 4%，加上股息仍低於 8% 的持有門檻，結論為偏貴。短期上檔以外資目標中點 725 元計約 −0.3%，中期上檔以 Base 五年終值計約 +21.3%","upside_short_pct":-0.3,"upside_mid_pct":21.3},"trap_analysis":{"verdict":"🟡","label":"週期高點的提前下單與現金轉換惡化"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"管理層 2026 年 3 月自承，當季營收被客戶因記憶體短缺而提前下單推升；2022 年短缺期之後，FY2023、FY2024 營收分別年減 6.08%、7.41%，FY2024 EPS 由 12.46 元降到 10.38 元；第三方指出 2024 年工業電腦市場明顯衰退；5 月報導也提到零組件吃緊與材料成本可能限制近期成長","assumption":"目前接單出貨比 1.44、7 月 1.64 的訂單中，有相當比重是為了鎖料，而不是實際部署","consequence":"2027 下半年起進入消化期，FY2028 EPS 回落到 15 元附近，倍數回到 20 倍，股價約 300–400 元，比現價低四成五到六成","ruling":"採納為 Bear 主路徑，機率 30%。不升為 Base，因為 43% 的邊緣 AI 訂單交期超過六個月，客戶也在規劃兩到三年的部署，不全是囤貨。這條與唯一致命數字（接單出貨比跌破 1.0）是同一件事，兩處結論一致","watch":"每季接單出貨比（含北美）、庫存天數、月營收年增率","evidence_refs":["supply_demand_durability#0","supply_demand_durability#4","supply_demand_durability#6"],"fact_refs":["f_kpi8_book_to_bill","f_kpi9"]},{"view":"論點成功但股東經濟變差","evidence":"近四季自由現金流利潤率 1.21%，FY2024 還有 14.84%；第二季毛利率 37.7%，低於財測；記憶體的成本壓力可能擴大到 CPU 與 PCB；2025 年第三季 DDR4 已讓毛利率少約 1 個百分點；北美 60% 訂單的關稅先由研華吸收","assumption":"營收照邊緣 AI 劇本成長，但上游與關稅分走毛利，成長所需的庫存與擴產長期吸走現金","consequence":"EPS 成長，但自由現金流／淨利長期低於 0.75，現行約九成的配息率撐不住，股息成長停滯，每股價值的成長慢於 EPS","ruling":"部分採納。庫存建置有訂單支撐，屬策略備料，暫不視為盈餘品質問題；但設下期限：FY2026 全年自由現金流／淨利低於 30%，且 2027 上半年沒有回到 50% 以上，就認定這條成立，Bear 機率上調至 40%","watch":"自由現金流／淨利、庫存天數、單季毛利率、配息率","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#3","reg_tariff_export#0"],"fact_refs":["f_peer_2395_tw_fcf_margin_pct","f_kpi3","f_kpi5"]},{"view":"價格已反映太多","evidence":"26 週股價上漲 113.4%；Trailing P/E 46.28 倍、P/S 7.69 倍都是四個年度端點中最高；現價 727 元貼近法說後外資目標 700–750 元的中點","assumption":"市場已把邊緣 AI 第二曲線與 2027 年續成長算進價格","consequence":"即使 Base 兌現，五年終值約 882 元，年化價格報酬約 4%，加上股息仍低於 8%；只要任何一季接單轉弱，EPS 與倍數會同時受打擊","ruling":"採納，這是本次不追價的主因。卡住結論的是價格，不是生意","watch":"股價相對最近四季 EPS 的倍數是否回到 30 倍以下","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_pe_current","f_pe_percentile","f_price_at_dd"]},{"view":"論點失敗","evidence":"中國廠商發布 2026 年新一代低價 ARM 架構工業電腦，以及可跑軟 PLC 的邊緣控制器；研華約 45% 的製造在中國，中國營收上半年年增 51%，是本輪主要成長引擎之一","assumption":"中國市場出現本土低價替代，研華逾 36% 的中國份額開始流失","consequence":"中國區成長由正轉負，整體毛利率再受壓","ruling":"反駁它作為主要失敗路徑：目前只有產品發布，沒有份額或價格數據，而且上半年中國區年增 51%，方向相反；列為長期觀察","watch":"中國區營收年增率與整體年增率的落差","evidence_refs":["substitute_technology#2"],"fact_refs":[]}],"max_dd":{"lo":-60,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 727.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=727.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訂單強度：結構性需求還是提前下單","cause":null,"prior_field":null,"side_a":"43% 的邊緣 AI 訂單交期超過六個月，客戶在規劃兩到三年的部署；第二季接單出貨比 1.44、7 月 1.64；法人預期 2027 年續成長，美日台擴產牽動 2027–2028 年營收","side_b":"管理層自承第一季營收被提前下單推升，客戶去年就因擔憂零組件緊俏而下單；5 月報導指出零組件吃緊可能限制近期成長；2022 年短缺之後，FY2023–FY2024 營收連兩年下滑","ruling":"可調和，屬程度差異，兩者並存。Base 保留 FY2028 小幅放緩（EPS 年增約 4%），Bear 承接完整的消化期；2027 上半年之前分不出兩者的比重","evidence_level":"中：證據是公司說法與媒體轉述，訂單分項事實表未涵蓋","settle_metric":"2027 上半年接單出貨比與庫存天數","if_then":["若 2027 上半年接單出貨比維持 1.1 以上，且庫存天數降到 100 天以下，則上修 Base 的 FY2028 EPS，Bear 機率降至 25%","若任一季接單出貨比低於 1.0 且庫存天數高於 130 天，則不建倉；已持有者減碼至半倉"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#3","supply_demand_durability#4","supply_demand_durability#5"]},{"axis":"盈餘品質：EPS 創高，現金轉換卻崩落","cause":null,"prior_field":null,"side_a":"第二季 EPS 5.20 元，營業利益年增 64%，營運槓桿為正","side_b":"第二季自由現金流 8.33 億元，只有淨利的 18%；近四季自由現金流利潤率 1.21%，低於多數同業；庫存約 116 天；近四季每股配息約為每股自由現金流的十倍","ruling":"可調和，屬時間差。採信庫存是有訂單支撐的備料，但這是尚未證實的管理層歸因，所以設下期限，見反證紀錄的股東經濟視角","evidence_level":"中：庫存分項與管理層說法事實表未涵蓋","settle_metric":"FY2026 全年與 2027 上半年的自由現金流／淨利","if_then":["若 2027 上半年自由現金流／淨利回到 50% 以上，則維持原判","若 FY2026 全年低於 30%，且 2027 上半年沒有改善，則 Bear 機率上調至 40%，並停止任何加碼"],"evidence_refs":[]},{"axis":"現在就買的最強論證，對上等待價格","cause":null,"prior_field":null,"side_a":"現在就買的理由：全球份額第一，營益率約為同業兩倍，邊緣 AI 第二曲線有來源，7 月接單創高、交期拉長，美日台擴產支撐 2027–2028 年；若 Bull 的 FY2027 EPS 26.5 元兌現，現價只約是前瞻 EPS 的 27 倍，對龍頭而言合理","side_b":"等待的理由：現價是樣本最高倍數，26 週已漲 113%；Base 五年價格報酬約兩成、年化約 4%，Bear 下跌約 46%；部分訂單是短缺下的提前下單，自由現金流幾乎歸零","ruling":"不可調和，兩邊方向相反，選擇等待。依據：機率加權後，上檔集中在 Bull 一個情境，Base 報酬低於 8% 的持有門檻；硬數據點是 Trailing P/E 46.28 倍與自由現金流利潤率 1.21%。卡住結論的是價格","evidence_level":"高：價格與倍數都是已實現數據","settle_metric":"股價相對最近四季 EPS 的倍數；季度接單出貨比","if_then":["若股價回到最近四季 EPS 的 30 倍以下，且最近一季接單出貨比仍在 1.0 以上，則重跑研究，通過後建立 2% 首倉","若股價續漲，但第三季毛利率仍低於 38%，則不追","反向條件：若股價下跌，但接單出貨比維持 1.2 以上、毛利率回到 38%，則提前重跑研究，通過後分批建立首倉，不等更低的價格"],"evidence_refs":["capital_markets_pricing#1","end_markets#1"]}],"triggers":[{"n":1,"text":"季度整體接單出貨比跌破 1.0，代表提前下單開始消化","type":"Single Thing","maps_to":"R1","metric":"季度整體接單出貨比","threshold":"任一季 <1.0","action":"不建倉；已持有者減碼至半倉，不攤平","source_freq":"每季法說","date":null,"evidence_refs":["supply_demand_durability#4"]},{"n":2,"text":"股價回到最近四季 EPS 的 30 倍以下，且接單沒有轉弱","type":"估值rearm","maps_to":null,"metric":"股價÷最近四季 EPS；最近一季接單出貨比","threshold":"≤30 倍，且接單出貨比 ≥1.0","action":"重跑研究，通過後建立 2% 首倉","source_freq":"每日股價＋每季法說","date":null},{"n":3,"text":"邊緣 AI 營收占比年底達 30%","type":"假設驗證","maps_to":"H1","metric":"邊緣 AI 營收占比","threshold":"FY2026 年底 ≥30%；低於 27% 視為未達","action":"未達則 Bull 機率降至 15%","source_freq":"每季法說","date":"2027-03"},{"n":4,"text":"毛利率回到財測區間","type":"假設驗證","maps_to":"H2","metric":"單季毛利率","threshold":"≥38%","action":"連兩季達標，就解除成本轉嫁的疑慮；連兩季低於 37%，改走減碼條件","source_freq":"每季財報","date":"2026-11"},{"n":5,"text":"上游零組件成本吸收失敗","type":"風險","maps_to":"R2","metric":"單季毛利率","threshold":"連兩季 <37%","action":"不建倉；已持有者減碼至半倉","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#1","capital_markets_pricing#3"]},{"n":6,"text":"關稅成本吸收失敗","type":"風險","maps_to":"R3","metric":"單季營業利益率；Section 232 衍生品清單","threshold":"營益率連兩季 <16%，或主力產品列入衍生品課稅","action":"停止加碼並重跑研究","source_freq":"每季財報＋美國商務部公告","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]},{"n":7,"text":"現金轉換沒有回復","type":"風險","maps_to":"R5","metric":"自由現金流／淨利","threshold":"FY2026 全年 <30%，且 2027 上半年 <50%","action":"Bear 機率上調至 40%，停止任何加碼","source_freq":"半年報、年報","date":"2027-08"},{"n":8,"text":"消化期的盈餘底部跌破論點前提","type":"清倉","maps_to":"H3","metric":"2027 年起的最近四季 GAAP EPS","threshold":"<16 元","action":"已持有者清倉，等下一輪谷底再重跑研究","source_freq":"每季財報","date":null},{"n":9,"text":"第三季財報複審","type":"複審日期","maps_to":null,"metric":"毛利率、接單出貨比、庫存天數、自由現金流","threshold":"見各條門檻","action":"逐條對帳後更新情境機率","source_freq":"每季","date":"2026-11"}],"kill_metrics":[{"metric":"季度整體接單出貨比","bear_threshold":"任一季 <1.0","window":"每季","source":"研華法說會／公司新聞稿","last_status":"ok"},{"metric":"單季毛利率","bear_threshold":"連兩季 <37%","window":"每季","source":"研華公司新聞稿","last_status":"warning"},{"metric":"自由現金流／淨利","bear_threshold":"FY2026 全年 <30%，且 2027 上半年 <50%","window":"至 2027-08","source":"研華合併財報","last_status":"warning"},{"metric":"庫存天數（庫存÷單季營業成本×90）","bear_threshold":">130 天","window":"每季","source":"研華合併財報","last_status":"ok"},{"metric":"邊緣 AI 營收占比","bear_threshold":"FY2026 年底 <27%","window":"2027-03","source":"研華法說會","last_status":"unknown"},{"metric":"2027 年起的最近四季 GAAP EPS","bear_threshold":"<16 元","window":"2027–2029","source":"研華合併財報","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='→', week26=113.4, valuation_dependent=False","input_gap":["week26_return_pct 落 100-150% 邊界帶，QC-42 反動能閘裁量範圍，本腳本無法自動判定，預設不放行"]},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🔴'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"首倉 2%，上限 4%；要有深回撤的心理準備（情境推估回撤 40%–60%）","requires_critic":[],"rearm_trigger":"股價回到最近四季 EPS 的 30 倍以下，且最近一季接單出貨比仍 ≥1.0；觸發後先重跑研究，不直接建倉","exec_line":"觀望，卡住結論的是價格。不追價；等倍數靠回檔或 EPS 成長消化到 30 倍以下、接單也沒有轉弱時，才重新評估 2% 首倉"},"reasoning":{"industry":"最新一季營收 261.26 億元，年增 46%、季增 28%。毛利率 37.7%，低於公司財測 38%–40%，年減 2.31 個百分點，管理層歸因於原物料波動。營益率 19.6%，營業利益年增 64%。上半年美元營收 14.7 億美元、年增 33%。分事業群：iSystems 年增 34%（半導體設備、雲端網通設備），Embedded 28%（智慧醫療、自動化設備、機器人專案），iAutomation 19%，iService 只有個位數。分地區：中國年增 51%、北美 30%，北美約占 2024 年營收 31%。各事業群營收占比事實表未涵蓋，所以占比超過一成的分部無法逐一列出。邊緣 AI 營收占比由 2023 年 4% 升到上半年 22.5%，公司目標年底 30%，專案毛利約 40%。單點依賴：客戶集中度查無資料；上游記憶體與 CPU 是實質單點，證據是 2025 年第三季 DDR4 吃緊讓毛利率少了約 1 個百分點，本季毛利率又低於財測。產業態勢分三面看。競爭面靜態：全球份額 8.6% 居首，但沒有消長資料；中國低價 ARM 工業電腦與軟 PLC 屬點狀攻擊。結構面轉好：AI 推動買家由 PLC 轉向配備加速器的工業電腦。其他結構變數是關稅，Section 232 衍生品範圍尚未確認。裁決為結構性轉好中，關稅與零組件成本兩面拉鋸。產業時鐘判擴張期：2024 年工業電腦市場明顯衰退，2025 年營收年增 18.6%，本季接單出貨比 1.44、7 月 1.64；不過提前下單、零組件短缺、交期拉長已經是過熱徵兆。","moat":"機制：長尾工業客戶的設計導入，加上最廣的產品線與全球通路，讓研華以份額第一（全球逾 8.6%、中國逾 36%）換到約同業兩倍的營益率。可證方向：投入資本事實表未涵蓋，算不出對同業的 ROIC 差距，改用利潤率差距代理。近四季營益率 17.97%，比次佳同業 3088.TWO 的 11.46% 高約 6.5 個百分點；毛利率 39.0%，比 6166.TW 的 35.49% 高約 3.5 個百分點。這只是單期截面，差距在擴大還是收窄，事實表未涵蓋。份額也只有靜態值：凌華 1 月營收年增 43%、2 月 16%，研華第二季年增 46%，看不出消長。執行面判擴大，因為接單出貨比與邊緣 AI 占比雙雙走高；定價面判縮減，因為第二季毛利率年減 2.31 個百分點、低於財測。兩者合判穩定；沒有來源化的份額上升證據，所以不給上升。執行力 8 分、定價力 7 分。報酬持續期方面，當期 ROIC 無法計算；四檢查點裡需求基礎值、決策層級、價值鏈分配都只到中等，持續期的關鍵在於上游零組件的議價權會不會鬆動。","growth":"成長以量為主：各事業群上半年年增 19%–34%，接單出貨比 1.44。產品組合改善為輔：邊緣 AI 專案毛利約 40%，占比 22.5%。另有成本轉嫁帶來的價格成分；併購與回購沒有貢獻。三年共識 EPS 與分析師家數事實表未涵蓋，算不出共識年複合成長；法說後只有「全年營收首度破千億、EPS 大幅上修」的定性描述。高配息讓內生成長上限只有約 4%/年，推導見報酬持續期。Base 路徑由最近四季 15.71 元到 FY2031E 31.5 元，約 14%–15%/年；超出上限的部分，歸因於利潤率擴張（產能利用率與邊緣 AI 組合）和週期上行，其餘無法歸因，所以加註依賴 re-rate 與週期配合，長期信心上限為中。跑道：全球前五大合計只有 25.9%，研華 8.6%。第三方估邊緣 AI 嵌入式 PC 2024–2030 年複合成長 14.6%；軟體定義的 AI 邊緣架構約 2029 年成為新廠預設規格，閉環 AI 製程控制仍在試點，所以第二曲線有來源。衰退信號成立一個半：自由現金流／淨利 FY2025 為 0.65、近四季約 0.07；毛利率第二季年減 2.31 個百分點（第一季事實表未涵蓋）。","governance":"現金轉換：自由現金流／淨利 FY2022 為 0.77、FY2023 0.77、FY2024 0.99、FY2025 0.65，近四季只剩約 0.07。近四季自由現金流利潤率 1.21%，也低於同業 6166.TW 的 6.66%、6414.TW 的 4.29%、3088.TWO 的 3.3%。第二季營業現金流 15.53 億元、資本支出 7.20 億元，自由現金流 8.33 億元，只有淨利 45.18 億元的 18%。庫存 209.08 億元、約 116 天，是現金轉換崩落的主因；管理層的說法是為訂單備料，庫存分項事實表未涵蓋。SBC 第二季 0.557 億元，約占營收 0.2%、營業利益 1.1%，稀釋可以忽略。現金去向：配息是最大宗，約為 FY2025 EPS 的 92%，也約為近四季每股自由現金流的十倍（推導見報酬持續期）；資本支出用於美、日、台擴產；營運資金主要是庫存；併購與回購事實表未涵蓋。差額由帳上現金或借款支應，現金與負債結構事實表未涵蓋。營運槓桿為正：營收年增 46%、營業利益年增 64%，利潤率沒有被壓縮。","valuation":"反推：以年化約 8% 價格報酬加約 1.5% 股息為門檻，五年後股價需要約 1,068 元。終端 28 倍時，FY2031E EPS 需約 38 元；30 倍時需約 36 元。對照最近四季 EPS 15.71 元，等於每年成長約 17%–18%，比 Base 路徑高出一截。倍數：Trailing P/E 46.28 倍、P/S 7.69 倍、EV/S 7.48 倍，三者都在四個年度端點中最高；這是年度端點的比較，不是連續五年分位。賣方：5 月時 15 位分析師平均目標約 502 元（高 628、低 400），早於第二季財報，不拿來當錨。法說後外資目標 700–750 元、本土最高 800 元，現價 727 元貼近外資區間中點，短線上檔約為零，與觀望的結論一致。同業倍數事實表未涵蓋，終端倍數只能以自身現值與歷史端點為錨：Bull 35 倍、Base 28 倍、Bear 20 倍，Bear 取成長熄火到約 10% 時的倍數。分母檢查：近四季 EPS 沒有明顯一次性項目，第二季淨利年增 127% 是去年同季業外偏低的基期效應。分母正處於週期上行段，這個問題交給情境樹處理。","premortem":"依據見反證紀錄。衰退信號成立一個半，價值陷阱屬中度風險：生意本身不會因此變壞，但眼前的盈餘與訂單水位可能被短缺放大了。歷史最大回撤、空方最強數字、訴訟與監管金額事實表未涵蓋；重大事件、訴訟、監管各軸都查無結果。"},"plain":{"six":{"how_it_makes_money":"研華賺的是工業設備商與系統整合商的邊緣運算硬體錢。錢落在設計導入後長期出貨的板卡與系統，毛利則被上游記憶體與 CPU 卡住","moat":"護城河方向穩定：執行面在擴大，定價面被上游成本侵蝕，兩者相抵","growth":"跑道寬：全球份額只有 8.6% 的分散市場，加上邊緣 AI 第二曲線。但近期的高成長主要來自產能利用率、產品組合與週期，不是來自再投資","capital":"資本配置以高配息為主。近四季營運資金與擴產吃掉了幾乎全部自由現金流，配息靠資產負債表支應","valuation":"要讓現價划算，未來約五年 EPS 每年得成長約 17%–18%，終端還要維持 28–30 倍。週期股要同時做到這兩件事，我不信","how_wrong":"最可能看錯的地方，是把零組件短缺下的提前下單當成結構性需求"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到最近四季 EPS 的 30 倍以下，且最近一季接單出貨比仍在 1.0 以上","trap":"🟡","val":"🔴","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":727.0,"week26_return_pct":113.4,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"近四季 EPS 15.71 元沒有明顯一次性項目。第二季淨利年增 127%，高於營業利益的 64%，原因是去年同季淨利只有營業利益的約 64%，基期偏低；本季約 88%，與 FY2022–FY2025 的 86%–99% 一致。分母處於週期上行段的問題交給情境樹，不視為分母爭議"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報與法說：毛利率能否回到 38%，接單出貨比能否維持 1.2 以上","impact":"高","watch":"單季毛利率、接單出貨比、庫存天數"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"南加州第二個美國組裝據點預計 2026 年啟用","impact":"中","watch":"北美毛利率與關稅吸收比例"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026 年報與法說：邊緣 AI 營收占比是否達 30%，以及全年自由現金流","impact":"高","watch":"邊緣 AI 占比、自由現金流／淨利、配息率"}],"_projected_from":"v19"}
```
