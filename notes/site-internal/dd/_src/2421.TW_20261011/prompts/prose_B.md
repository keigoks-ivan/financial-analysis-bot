你是 stock-analyst v20 的**散文層（prose）agent**，標的 2421.TW（2026-10-11）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：2421.TW　日期：2026-10-11　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1324B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（751B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1146B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1517B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1467B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（468B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（789B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2299B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4384B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2753B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1324           3973-5676      5 條（2–6 內）  
s3                  8000         751           5074-7249      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        4130          7609-10870      5 條（2–6 內）  
s6                 11000         468          7372-10532      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         789           1898-2711      5 條（2–6 內）  
s10                 5000        2299           1891-2701      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2753           2000-2247      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5610B；至少需散文≈39.39KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−58
−58%
−54%
−38%
−38
−35%
−13.66%
−3
−1
−0.88%
0
0%
0.46
0.54
0.57
0.74
0.75
0.77
01
1
1.07
1.19
1.39
1.61
2
2%
2.082
2.09
2.37
2.53
2.75
2.8%
3
3%
03
3.1%
3.119%
3.119
3.6%
04
4
4%
4.037
5%
5
5.65%
5.65
6
6.05%
6.118
07
7
7.7
7.89
7.96%
8%
8
08
8.17%
8.5
9
09
9.5
9.9%
10%
10
10.7
10.7%
10.85
10.9
11
11.4
11.49
11.85%
12%
12
12.2
12.2%
12.4%
12.4
12.54
12.9
13%
13
13.4
14
14%
15.0
15%
15
15.3%
15.44%
15.48
15.5
15.85%
16%
16.28
16.5
16.6
17
17.5
18
18.5
19.5
20%
20
21.08%
21.5
21.7
22%
22.3%
22.55%
23.5
23.56%
24
24.1%
25
25%
26
26.1%
27
27.24%
27.24
27.3%
27.6%
27.72%
27.85%
28.87%
29%
30%
30
31
31.06%
31.25%
31.65%
31.89%
31.912
33.06%
35%
35.4
40%
42
42.63%
45%
48%
49
49.9
50
52.9
53%
54.19
55%
60%
67.5%
70
76
77
82.2
90
95
100%
100
135
150%
160
165
168
168.0
174
175
180
194
214
240
319
2022
2023
2024
2025
2026
2027
2028
2421
3017
3324
3653
6230
20261011
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
{"meta":{"ticker":"2421.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"建準電機"},"oneliner":"建準：AI 伺服器風扇主要供應商，營收連創新高、本益比 15.5 倍不貴，但利潤率處在四年高點、液冷第二曲線尚無營收證據；現價不追，等液冷營收占比揭露再進場。","thesis":{"H":[{"id":"H1","text":"AI 伺服器散熱需求延續到 2027 年，營收維持雙位數成長","2y":"2027 全年營收年增 ≥15%","5y":null,"10y":null,"threshold":"2027 年月營收累計年增率 ≥15%","source":"公開資訊觀測站月營收公告（每月）","drift_rule":"TTM 營收低於年增 15% 路徑 5% 以上連 2 季＝削弱；低於 10% 以上連 3 季＝反轉"},{"id":"H2","text":"伺服器產品組合撐住利潤率，擴產與折舊上升期間不跌回 2023–2024 年水準","2y":"TTM 毛利率 ≥29%、營益率 ≥14%","5y":null,"10y":null,"threshold":"TTM 毛利率 ≥29% 且 TTM 營益率 ≥14%","source":"季報損益表（每季）","drift_rule":"TTM 毛利率低於門檻 5%（約 27.6%）連 2 季＝削弱；低於門檻 10%（約 26.1%）連 3 季＝反轉"},{"id":"H3","text":"液冷產品（水冷板、CDU、Sidecar、水泵）成為第二支柱，補上氣冷被壓縮的用量","2y":null,"5y":"FY2030 液冷營收占比 ≥15%","10y":null,"threshold":"FY2028 液冷營收占比 ≥10%、FY2030 ≥15%","source":"法說會產品別營收說明與年報（每季／每年）","drift_rule":"揭露占比低於路徑 5% 以上連 4 季＝削弱；低於 10% 以上連 6 季或持續不揭露＝反轉"}],"R":[{"id":"R1","text":"AI 伺服器專案受記憶體、PCB、晶片供應延後，月營收短期失速","h_ref":"H1","clock":"⚡","threshold":"月營收年增率連 2 個月 <10%","evidence_refs":["end_markets#2"]},{"id":"R2","text":"液冷壓縮每台機櫃的風扇用量，氣冷營收被部分取代，利潤率先受壓","h_ref":"H2","clock":"🔥","threshold":"TTM 毛利率 <29% 連 4 季，且伺服器營收占比較前一年下降","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"id":"R3","text":"2028 年後 AI 資本支出進入消化期，營益率回到上一輪 11–12%","h_ref":"H2","clock":"🐢","threshold":"TTM 營益率 <12%","evidence_refs":["supply_demand_durability#0"]},{"id":"R4","text":"菲律賓擴產與液冷投資吃掉自由現金流，新投入資本報酬偏低","h_ref":"H3","clock":"🔥","threshold":"年度 FCF／淨利 <0.75 連 2 年（FY2026–FY2027）","evidence_refs":["capital_markets_pricing#2"]}],"single_thing":{"description":"Vera Rubin 世代主力機櫃的伺服器風扇（含風扇牆）未取得主要 ODM 或 GPU 大廠參考設計的供應資格","why_fatal":"伺服器網通與 AI 約占營收 48%，是 FY2027–2028 共識 EPS 13.4、16.28 元的主要來源；失去一個平台世代等於 18–24 個月的營收缺口，而液冷尚無法補位","if_happens":"EPS 路徑改走 Bear（FY2028 約 9 元），終端倍數 10 倍、價值約 95 元；清倉，不等財報確認","how_monitor":"每月營收年增率與法說會平台出貨說明；伺服器營收占比跌破 40% 視同發生","probability":"約 15%（12–24 個月）：公司稱為 GB200／GB300 推薦供應商（公司說法），風扇份額約 30% 未見流失證據，但每次平台換代都重新認證"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.54,"peg_fy2":0.46,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":7.89,"FY2026E":10.85,"FY2027E":13.4,"FY2028E":16.28},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識為 Koyfin 快照美元值依 2026-10-09 匯率（×31.912）換算新台幣"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"營收隨 AI 伺服器資本支出擺動（2023 年年減 8.17%、2025 年年增 27.72%），獲利成長主要來自產品組合推升的利潤率，而非自有定價權"},"industry":{"clock_phase":"II","sd_verdict_source":"TrendForce 2026-08（液冷滲透率、GPU 機櫃出貨）；摩根士丹利 2026-04（液冷需求延續至 2027 年）","bargaining":{"up":"上游原物料與零件供應商集中度事實表未涵蓋","down":"下游為伺服器 ODM 與品牌客戶，規格由 GPU 大廠參考設計主導，買方議價力強；前 1–2 大客戶占比事實表未涵蓋","geo":"2026 年資本支出上調至 15 億元以上，主要投入菲律賓新廠"},"profit_pool_dir":"散熱利潤池往液冷與高階散熱件移動；建準強項在氣冷，液冷進度落後奇鋐、雙鴻","tam_table":[{"item":"AI 晶片液冷滲透率","value":"2026 年 53%、2027 年接近 60%（TrendForce，2026-08）"},{"item":"GPU 機櫃出貨","value":"預期年增逾 30%，Kyber NVL144 的 2027 年時程可能延後（同上）"},{"item":"建準 AI 伺服器風扇份額","value":"約 30%（報導未標年份）；另一份 2025-03 分析稱其為全球第二大散熱風扇供應商"},{"item":"液冷營收占比","value":"公司未揭露；水冷板首批已出貨，液冷產品 2027 年放量（法說摘要，未逐字取得）"},{"item":"散熱營業利益池占比 5 年前→現","value":"事實表未涵蓋，無法檢查利潤池是否淨流出 5pp 以上"}]},"moat":{"mechanism":"風扇與風扇牆設計量產規模＋每個 GPU 平台世代的供應名單認證；轉換成本只鎖一個平台世代","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面穩定（份額無消長證據、營收創高，但液冷落後）、定價面穩定（毛利率 TTM 31.89% 對 2025 年 31.06% 微升，最新一季 31.25% 略低於 TTM）；兩者都不是擴大也不是縮減","threats":[{"level":"🔴","text":"液冷架構部分取代氣冷：晶片端改用水冷板，風扇只留在機櫃其他部位；建準自身液冷進度落後奇鋐、雙鴻。因混合散熱仍為主流、公司也在布局液冷，定為生態攻擊級而非全面架構替代","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#2","end_markets#2"]},{"level":"🟡","text":"風扇本業點對點競爭：奇鋐、台達、日本電產都供應伺服器風扇，每次平台換代重新比價；目前未見具名丟單或新進入者搶單","p":25,"evidence_refs":["competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"營益率中高（TTM 15.85%）×投入資本周轉率事實表未涵蓋，象限無法定案；2022–2025 年淨利倍增而累計淨再投資接近零，當期報酬偏向低資本需求型態，但 2026 年擴產後周轉率可能下降","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端業者的 AI 機櫃、決策者是 GPU 大廠參考設計與 ODM 散熱團隊、付款者是 ODM，三角色都成立，散熱是需要不是想要。但客戶要解決的是晶片發熱，風扇只是解法之一：GB200 晶片端已改水冷板、其餘部位仍用風扇，需求在、解法在移轉（代理讀數：液冷滲透率 2026 年 53%→2027 年近 60%）"},{"item":"決策層級","level":"🟡","text":"替代性在每個平台世代的供應名單這一層決定，不在風扇品項；GB200→GB300→Vera Rubin 每次換代都重新認證，轉換成本只鎖 1–2 年。公司稱為 GB200／GB300 推薦供應商（公司說法），AI 伺服器風扇份額約 30%（報導未標年份），未見具名丟單證據"},{"item":"價值鏈分配","level":"🟡","text":"散熱在 AI 機櫃中金額占比小、買方集中，價值大多被晶片端拿走；散熱環節內利潤往液冷與高階散熱件集中——健策營益率 33.06%、奇鋐 23.56%、建準 15.85%，超眾 −0.88% 說明沒卡到好位置就賺不到錢"},{"item":"社會容忍度","level":"🟢","text":"B2B 工業零組件，無監管授權、無民生必需品的社會漲價壓力；定價上限由客戶議價決定，不受社會容忍度約束"}],"roiic":"投入資本未入事實表，無法直接計算。代理讀數：2023–2025 年累計淨利 49.9 億、自由現金流 52.9 億，淨再投資約 −3 億，同期淨利由 2022 年 10.9 億增至 2025 年 21.7 億，過去的增量報酬來自產品組合與產能利用率，不是新投入資本；2026 年起的新投入（菲律賓廠、液冷）報酬未知，取 20% 作判斷假設","reinvest_rate":"約 0.54（TTM）：以 FY2025 淨利÷營業利益≈0.77 把 TTM 營益率 15.85% 折成稅後約 12.2%，扣掉 FCF 利潤率 5.65% 的差額視為淨再投資，（12.2−5.65）÷12.2≈0.54","endo_ceiling":10.7,"formula_note":"內生成長上限＝增量報酬 20%（判斷假設）×再投資率 0.54≈10.7%；20% 低於歷史隱含值，理由是液冷同業雙鴻 TTM FCF 利潤率 −13.66%，顯示新業務資本密集"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","2421.TW":31.89,"3017.TW":28.87,"3324.TWO":27.85,"3653.TW":42.63,"6230.TW":15.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","2421.TW":15.85,"3017.TW":23.56,"3324.TWO":15.3,"3653.TW":33.06,"6230.TW":-0.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","2421.TW":5.65,"3017.TW":24.1,"3324.TWO":-13.66,"3653.TW":15.18,"6230.TW":-4.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","2421.TW":6.05,"3017.TW":3.36,"3324.TWO":5.57,"3653.TW":3.61,"6230.TW":7.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3017.TW","gm":28.87,"om":23.56,"fcf_margin":24.1,"rd_intensity":3.36,"strategy_note":"奇鋐是液冷與整合散熱的領先者，營益率 23.56%、FCF 利潤率 24.1% 都遠高於建準，是液冷份額的主要對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3324.TWO","gm":27.85,"om":15.3,"fcf_margin":-13.66,"rd_intensity":5.57,"strategy_note":"雙鴻液冷先行投入，營益率 15.3% 與建準相當，但 FCF 利潤率 −13.66%，顯示液冷擴產非常吃資本","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3653.TW","gm":42.63,"om":33.06,"fcf_margin":15.18,"rd_intensity":3.61,"strategy_note":"健策做均熱片與封裝散熱件，毛利率 42.63%、營益率 33.06%，產品不直接與風扇競爭，只作散熱環節利潤率上限參照","period":"TTM ending 2026-06-30（4季加總）"},{"name":"6230.TW","gm":15.39,"om":-0.88,"fcf_margin":-4.08,"rd_intensity":7.5,"strategy_note":"超眾以熱管為主，營益率 −0.88%，說明散熱產業不是人人受惠，沒有 AI 伺服器份額就沒有利潤","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主：AI 伺服器出貨帶動（2026 年前 8 月營收年增 21.08%）；組合次之：伺服器占比上升把毛利率由 2022 年 22.55% 拉到 2025 年 31.06%；無併購、無回購","runway_years":"不適用滲透率口徑：風扇本業不是低滲透市場；AI 伺服器需求可見度約到 2027 年，液冷第二曲線尚無營收占比，有效成長期暫估 2–3 年","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段報酬持續期推導：增量報酬假設 20%×再投資率約 0.54≈10.7%；共識三年 EPS 年複合 27.3% 超出約 16.6pp，缺口歸因於利潤率擴張與營運槓桿","segments":[{"item":"伺服器網通與 AI 應用","value":"48%（2026 年 3 月報告，出處未確認）；分部利潤率事實表未涵蓋，公司毛利率由 2022 年 22.55% 升到 2025 年 31.06%，與伺服器占比上升同期"},{"item":"IT（NB／PC）","value":"22%"},{"item":"車用電子","value":"12%"},{"item":"工業與醫療","value":"10%"},{"item":"其他","value":"8%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":null,"evidence":"單季年比資料事實表未涵蓋；最新一季 31.25% 略低於 TTM 31.89%"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"未見份額消長的直接證據"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"無提價後量縮證據"},{"signal":"EPS 成長顯著高於營收成長（差距逾 5pp）","lit":true,"evidence":"2022–2025 年 EPS 年複合 22.3%、營收 9.9%，差 12.4pp"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 0.74、2025 年 1.07，未連續；2026 年擴產後有再度跌破風險"},{"signal":"SBC／營收逾 5% 且逐年上升","lit":null,"evidence":"事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"evidence":"晶片端改用水冷板，氣冷單機用量被部分取代；風扇專屬需求的量化資料查無"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"P/S、EV/S 位於四個年度端點最高位置，倍數上移"},{"signal":"維護性資本支出占 FCF 逾 60%","lit":null,"evidence":"折舊與維護性資本支出事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"2026 年資本支出上調至 15 億元以上"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長未靠併購支撐；現金回饋以股息為主（殖利率 3.119%），回購紀錄與現金去向四分事實表未涵蓋"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事件掃描未見併購，無已實現併購報酬可評","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未見回購；股東回饋以現金股息為主（殖利率 3.119%）","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"推算股數 2022 年約 2.53 億→2025 年約 2.75 億（年均約 2.8%，2024→2025 不變）；增加來源事實表未涵蓋，無法認定為股權酬勞稀釋","grade":"不過"}]},"valuation":{"basis":"Forward P/E（FY2026E 共識 EPS 10.85 元）＋PEG；循環屬性下輔以 P/S、EV/S 在四個年度端點的位置","peers":{"expanded":false,"reason":"同業 Forward P/E 事實表未涵蓋（同業對照只有利潤率），無法做倍數對照；改以本身 Fwd P/E 15.48 倍、2026-08 高點 16.5–17 倍與賣方目標 180–214 元為尺"},"fwd_pe":15.48,"peg":0.57,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Fwd P/E 15.48 倍、FY2027E 12.54 倍、PEG 0.57（FY2025A 7.89→FY2028E 16.28 元，年複合 27.3%）表面便宜；但 P/S 2.37 倍與 EV/S 2.09 倍都在四個年度端點最高位置、營益率在四年高點，便宜建立在週期高檔利潤率上。兩者相抵，判為合理","upside_short_pct":15.5,"upside_mid_pct":35.4},"trap_analysis":{"verdict":"🟡","label":"週期高點利潤率被當成新常態"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"TTM 營益率 15.85% 高於 2023–2024 年 11.49–11.85%；2022–2025 年 EPS 年複合 22.3% 而營收只有 9.9%，獲利成長主要來自利潤率；GB200 晶片端已改水冷板，風扇只留在其餘部位","assumption":"市場假設 AI 伺服器需求與產品組合紅利延續到 2028 年之後","consequence":"若 2028 年進入資本支出消化期，營收下滑、營益率回到 11–12%，EPS 回到 8.5–9.5 元，倍數同步壓到 9–10 倍，股價落在 76–95 元，五年虧損約 45%","ruling":"採納為 Bear 情境主軸，機率 30%；與唯一致命點部分重疊（失去下一世代平台資格是這條路徑的加速版），已回補至觸發器","watch":"TTM 營益率是否跌破 12%；月營收年增是否連 3 個月轉負","evidence_refs":["substitute_technology#0"],"fact_refs":["f_peer_2421_tw_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"最新一季營業現金流 6.118 億、資本支出 4.037 億，自由現金流只剩 2.082 億；TTM FCF 利潤率 5.65%，低於 2025 年 12.4%；2026 年資本支出上調至 15 億元以上；液冷先行者雙鴻 TTM FCF 利潤率 −13.66%","assumption":"營收成長會等比例轉成股東可分配的現金","consequence":"營收照共識成長，但液冷與擴產的新投入報酬偏低，FCF／淨利長期低於 0.75，股息成長停滯，終端倍數應下修","ruling":"部分採納：內生成長上限已用 20% 增量報酬保守估計，Base 終端倍數 13 倍低於現值；若 FCF／淨利連 2 年低於 0.75，終端倍數再下修 1 倍","watch":"FY2026、FY2027 年度 FCF／淨利","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_kpi4","f_peer_2421_tw_fcf_margin_pct","f_peer_3324_two_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"26 週漲 27.24%；P/S 2.37 倍、EV/S 2.09 倍都在四個年度端點最高位置；摩根士丹利 2026-04 目標價 165 元、評中性","assumption":"現價已計入 2026 年營收創高與 2027 年延續","consequence":"若 2027 年成長只達共識，股價缺乏上修空間","ruling":"反駁：以本益比看，Fwd 15.48 倍低於 2026-08 漲停時的 16.5–17 倍，FY2027E 只有 12.54 倍，股價也低於 4 位賣方最低目標 180 元；價格沒有過度反映，問題在利潤率持續性而不在倍數","watch":"股價若在共識未上修下漲過 194 元（賣方平均目標）則不追","evidence_refs":["supply_demand_durability#0","capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_ps_percentile","f_ev_s_percentile","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"事件掃描在七個面向都查無資料：客戶二供、客戶集中度與信用、反壟斷與監理、關稅與出口管制、地緣與供應鏈、通路與商業模式轉變、重大事件。事實表也未涵蓋前幾大客戶占比、應收帳款集中度、生產基地分布與對美出貨比重。這一塊唯一已知的事實是：2026 年資本支出上調至 15 億元以上，主要投入菲律賓新廠","assumption":"假設前 1–2 大客戶占比未超過 40%，下一世代平台沒有導入第二供應商分食份額，關稅、出口管制與地緣事件也不改變平台認證結構","consequence":"客戶集中與二供：若單一 ODM 或 GPU 大廠占比過高，或下一世代改採雙供應商，失去一個平台世代的衝擊會大於 Bear 情境。客戶信用：買方集中時，單一客戶延遲付款會放大擴產期已偏低的自由現金流壓力。關稅與出口管制、地緣與供應鏈：若生產基地集中在單一受管制地區，加徵關稅會壓縮毛利，或迫使客戶轉單。菲律賓新廠可以部分分散這個風險，但投產時點事實表未載。通路與商業模式：若散熱採購由逐項採購零組件轉向機櫃級整合方案，決策權會移往整合能力強的同業，建準以單一零組件身分議價會更弱。反壟斷與監理：B2B 工業零組件，有台達、日本電產、奇鋐等多家供應商，沒有監理授權門檻，屬低相關。重大事件：火災停工、訴訟、經營層異動皆查無","ruling":"列為資料缺口，不採信也不否定，逐項處置如下。反壟斷與監理判為低相關，不調整。通路與商業模式轉變的風險方向和液冷替代威脅、唯一致命點相同，已由兩者涵蓋，不另調機率。重大事件查無，不調整。客戶集中與二供、客戶信用、關稅與出口管制、地緣與供應鏈四項在揭露前不計入 Bear 機率；只要出現以下任一情況，Bear 機率上調至 35% 並重跑情境樹：年報揭露單一客戶占比超過 40%、確認下一世代導入第二供應商、確認主要產能落在被加徵關稅或出口管制的地區","watch":"年報前十大客戶與應收帳款集中度揭露；法說會生產基地分布與菲律賓廠投產時點；美國對伺服器零組件的關稅與出口管制公告；下一世代平台供應名單是否出現第二家風扇供應商","evidence_refs":[],"fact_refs":[]}],"max_dd":{"lo":-58,"hi":-38,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 168.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=168.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：2027 年前的需求","cause":null,"prior_field":null,"side_a":"月營收前 8 月年增 21.08%、7 月 31.65%；TrendForce 預估 GPU 機櫃出貨年增逾 30%、液冷滲透率 2027 年近 60%；摩根士丹利認為液冷需求延續到 2027 年","side_b":"無反向證據","ruling":"一致：2027 年前的需求不是爭點，爭點在 2028 年之後的循環與液冷份額","evidence_level":"公告月營收＋第三方產業預估","settle_metric":"2027 年月營收累計年增率","if_then":["若 2027 年上半年累計年增仍 ≥15% → 維持 Base 情境不動","若累計年增跌破 5% → Base 的 FY2027 EPS 下修至 12 元並重跑情境樹"],"evidence_refs":["end_markets#0","end_markets#3","supply_demand_durability#1","supply_demand_durability#0"]},{"axis":"營收創高 vs 液冷落後","cause":null,"prior_field":null,"side_a":"營收連創新高、4 位賣方全數買進、平均目標 194 元；公司稱為 GB200／GB300 推薦供應商，水冷板首批已出貨","side_b":"液冷進度落後奇鋐、雙鴻，液冷產品 2026 年第三季才小量送驗、2027 年放量；摩根士丹利因液冷貢獻待放大把目標價由 175 元降到 165 元","ruling":"可調和（程度差異）：近兩年營收靠風扇本業，液冷落後影響的是 2028 年之後的份額與利潤池；以液冷營收揭露為裁決點，在此之前論點只支撐觀望，不支撐溢價","evidence_level":"A 側為公告數據與賣方評等；B 側為法說摘要與賣方報告（未取得逐字原文）","settle_metric":"法說會揭露的液冷產品營收占比","if_then":["若 2027 年上半年液冷營收占比 ≥5% 且月營收年增 ≥15% → 首倉 2%，之後逐季加碼至 4%","若 2027 年底液冷仍停在送樣、沒有營收占比 → 不進場，Bull 機率由 20% 降到 10% 重跑情境樹"],"evidence_refs":["end_markets#2","supply_demand_durability#0","capital_markets_pricing#0","competitive_share_entrants#1","substitute_technology#1"]},{"axis":"表面便宜 vs 週期高檔利潤率","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：Fwd P/E 15.48 倍、FY2027E 12.54 倍，三年共識 EPS 年複合 27.3%、PEG 0.57，股價低於賣方最低目標 180 元，殖利率 3.1% 墊底","side_b":"便宜建立在四年高點的利潤率上：營益率由 2022 年 7.96% 升到 TTM 15.85%，P/S 與 EV/S 在四個年度端點最高位置；循環型公司在利潤率高點的低本益比不構成安全邊際","ruling":"不可調和（方向相反），選 B 側。依據：2022–2025 年 EPS 年複合比營收高約 12pp，成長來自利潤率擴張而非營收，且液冷會壓縮氣冷單機用量；因此 Base 終端倍數取 13 倍、Bear 取 10 倍，不用現值倍數外推","evidence_level":"公司年度財報＋現值倍數","settle_metric":"TTM 營益率與 2027 年營收年增","if_then":["若 TTM 營益率連 2 季低於 14% 而股價仍在 160 元以上 → 不進場，持有者減碼一半","反向：若 2027 年營益率守住 16% 以上且營收年增 ≥15%，證明利潤率結構性抬升 → Base 終端倍數上調至 15 倍重跑，並以首倉 2% 進場"],"evidence_refs":["substitute_technology#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：液冷滲透率 2026 年 53%、2027 年近 60%，GPU 機櫃出貨年增逾 30%，散熱總預算擴大","side_b":"替代技術：晶片端改水冷板，風扇只留在其餘部位；競爭面未見新進入者搶單或份額流失證據；風扇專屬需求量化資料查無","ruling":"雙向拉鋸：散熱總預算擴大與氣冷單機用量被壓縮同時發生，對建準的淨效果取決於液冷份額","evidence_level":"第三方產業預估＋研究報告引述","settle_metric":"伺服器網通與 AI 營收占比","if_then":["若伺服器營收占比由 48% 升到 55% 以上 → 判定結構轉好占上風，Bull 機率上調至 25%","若占比跌破 40% → 視同唯一致命點發生，清倉"],"evidence_refs":["supply_demand_durability#1","substitute_technology#0","competitive_share_entrants#2","supply_demand_durability#2"]}],"triggers":[{"n":1,"text":"2027 年月營收累計年增維持 15% 以上，驗證 AI 散熱需求延續","type":"假設驗證","maps_to":"H1","metric":"月營收累計年增率","threshold":"≥15%","action":"維持觀察，不因單月波動調整","source_freq":"公開資訊觀測站月營收／每月","date":"2027-01 起每月"},{"n":2,"text":"TTM 毛利率與營益率守住擴產期水準","type":"假設驗證","maps_to":"H2","metric":"TTM 毛利率／TTM 營益率","threshold":"≥29%／≥14%","action":"跌破任一項則停止加碼","source_freq":"季報／每季","date":"2026-11 起每季"},{"n":3,"text":"液冷產品營收占比首次揭露達 5% 以上，且利潤率與營收成長同時守住","type":"估值rearm","maps_to":"H3","metric":"液冷產品營收占比＋TTM 營益率＋月營收年增率","threshold":"≥5%／≥15%／≥15%","action":"重跑研究後首倉 2%","source_freq":"法說會／每季","date":"2027-03 前後"},{"n":4,"text":"月營收年增率連 2 個月低於 10%，供應鏈延後或需求放緩","type":"風險","maps_to":"R1","metric":"月營收年增率","threshold":"連 2 個月 <10%","action":"停止加碼","source_freq":"公開資訊觀測站月營收／每月","date":"2026-11 起每月","evidence_refs":["end_markets#2"]},{"n":5,"text":"毛利率連 4 季低於 29% 且伺服器占比下降，顯示液冷壓縮氣冷用量","type":"減碼","maps_to":"R2","metric":"TTM 毛利率／伺服器網通與 AI 營收占比","threshold":"<29% 連 4 季，且占比較前一年下降","action":"減碼一半","source_freq":"季報與法說會／每季","date":"2026-11 起每季","evidence_refs":["substitute_technology#0"]},{"n":6,"text":"TTM 營益率跌破 12%，利潤率回到上一輪循環水準","type":"減碼","maps_to":"R3","metric":"TTM 營業利益率","threshold":"<12%","action":"減碼一半；連 2 季未回升則清倉","source_freq":"季報／每季","date":"2027-01 起每季"},{"n":7,"text":"Vera Rubin 世代主力機櫃的風扇供應資格旁落","type":"Single Thing","maps_to":"Single Thing","metric":"法說會平台出貨說明／伺服器網通與 AI 營收占比","threshold":"公司確認未取得資格，或伺服器營收占比 <40%","action":"清倉","source_freq":"法說會與月營收／每季","date":"2027 年上半年起"},{"n":8,"text":"股價先跌、基本面未損時分批反買","type":"加碼","maps_to":"H1","metric":"股價／月營收年增率","threshold":"≤135 元／≥15%","action":"分批反買，首倉 2%","source_freq":"日線收盤＋月營收／每日","date":"即日起"},{"n":9,"text":"年度 FCF／淨利連 2 年低於 0.75，擴產吃掉現金","type":"風險","maps_to":"R4","metric":"年度 FCF／淨利","threshold":"<0.75 連 2 年（FY2026–FY2027）","action":"停止加碼並將終端倍數下修 1 倍重跑","source_freq":"年報現金流量表／每年","date":"2028-03","evidence_refs":["capital_markets_pricing#2"]},{"n":10,"text":"FY2026 年報與法說會後複審","type":"複審日期","maps_to":null,"metric":"FY2026 EPS 對共識 10.85 元","threshold":"偏離 ±5%","action":"重跑情境樹","source_freq":"年報／每年","date":"2027-03-31"}],"kill_metrics":[{"metric":"月營收年增率","bear_threshold":"連 3 個月 <0%","window":"2027-01～2028-12","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"TTM 營業利益率","bear_threshold":"<12%（回到 2023–2024 年水準）","window":"2026 年第三季～2028 年第四季","source":"季報損益表","last_status":"ok"},{"metric":"伺服器網通與 AI 營收占比","bear_threshold":"<40%","window":"每次法說會至 2028 年","source":"法說會簡報","last_status":"unknown"},{"metric":"年度 FCF／淨利","bear_threshold":"<0.75 連 2 年","window":"FY2026～FY2027","source":"年報現金流量表","last_status":"warning"},{"metric":"液冷產品營收占比","bear_threshold":"2027 年底仍未揭露或 <5%","window":"至 2027-12","source":"法說會產品別營收說明","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=27.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等法說會揭露液冷產品營收占比 ≥5% 且 TTM 營益率 ≥15% 再進場；現價不追'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"verdict":"觀望","rearm_trigger":"法說會揭露液冷產品營收占比 ≥5%，且 TTM 營益率 ≥15%、月營收年增 ≥15%","exec_line":"現價 168 元不追。液冷占比證實後首倉 2%；若股價先跌到 135 元以下而月營收年增仍 ≥15%，分批反買首倉 2%；伺服器營收占比跌破 40% 或確認失去下一世代資格則清倉"},"reasoning":{"industry":"營收結構（2026 年 3 月報告，原始出處未確認、可能非最新）：伺服器網通與 AI 48%、NB／PC 22%、車用電子 12%、工業與醫療 10%、其他 8%；超過一成的分部是伺服器、NB／PC、車用三塊，各分部成長率事實表未涵蓋。最新一季（2026 年第二季）營收 54.19 億元、毛利率 31.25%、營益率 15.44%。收錢方式是按件出貨的 B2B 零組件，進入 GPU 平台參考設計與 ODM 供應名單後拿下整個平台世代的量，所以錢卡在平台認證這一節點。產業時鐘判為擴張期：TrendForce 預估 GPU 機櫃出貨年增逾 30%、液冷滲透率由 2026 年 53% 升到 2027 年近 60%，需求可見度到 2027 年。供需持久性屬週期性：2027 年之後隨 AI 資本支出消化有反轉風險，散熱供給端有奇鋐、雙鴻、台達、日本電產等多家，供給可逆性高。產業態勢屬雙向拉鋸：散熱總預算擴大，但晶片端液冷壓縮氣冷用量。單點依賴：AI 伺服器平台認證（推薦供應商身分為公司說法）；前幾大客戶與供應商集中度事實表未涵蓋，列資料缺口。本輪未附逐字稿，管理層過去的財測與承諾無法對照。","moat":"機制：風扇與風扇牆的設計量產能力，加上平台世代認證（公司稱為 GB200／GB300 推薦供應商，屬公司說法）。可證方向：同業投入資本未入事實表，ROIC 差距無法計算，改用利潤率可比軸——毛利率 31.89% 高於奇鋐 28.87%，但營益率 15.85% 比奇鋐低 7.7pp、FCF 利潤率 5.65% 比奇鋐低 18.5pp。執行面 7 分：營收連創新高、份額約 30% 未見流失，但液冷進度落後；定價面 5 分：買方集中、風扇有台達與日本電產等多家可替，毛利率上升主要來自產品組合。AI 曝險屬淨增量：伺服器需求直接長在建準的風扇產品上，但晶片端液冷繞過風扇，分界年約在 2027 年（液冷滲透率近 60%）。威脅：液冷部分取代屬生態攻擊級（扣 1 分，機率 30%），風扇點對點競爭不扣分。","growth":"成長是量為主、組合次之，無併購與回購。共識 EPS：FY2026E 10.85、FY2027E 13.4、FY2028E 16.28 元（Koyfin 快照美元值依 2026-10-09 匯率換算新台幣，家數事實表未涵蓋），對 FY2025A 7.89 元的三年年複合＝（16.28÷7.89）^(1/3)−1≈27.3%。內生上限 10.7%（見護城河段），缺口約 16.6pp 歸因於利潤率擴張與營運槓桿：2022–2025 年 EPS 年複合 22.3%、營收只有 9.9%，淨再投資接近零，利潤增加來自組合與產能利用率；這類缺口能維持多久取決於 AI 週期，不是可複利的再投資。跑道判讀：本業已過低滲透期，第二曲線（水冷板、CDU、Sidecar、水泵）還在送樣到小量出貨，沒有可驗證的營收占比，因此給中等跑道。衰退信號亮兩盞（EPS 成長遠高於營收成長、替代技術壓縮氣冷用量），長期成長性與價值陷阱風險皆為中等。","governance":"FCF／淨利：2022 年 1.61、2023 年 1.39、2024 年 0.74、2025 年 1.07（年度財報）。最新一季營業現金流 6.118 億、資本支出 4.037 億，FCF 2.082 億，TTM FCF 利潤率降到 5.65%，主因 2026 年資本支出上調至 15 億元以上（菲律賓新廠）。股東回饋以現金股息為主，殖利率 3.119%；事實表未見回購、未見併購。以淨利÷稀釋 EPS 推算的股數由 2022 年約 2.53 億股增至 2025 年約 2.75 億股（年均約 2.8%，但 2024→2025 不變），增加來源（員工酬勞、可轉債轉換或盈餘轉增資）事實表未涵蓋，無法判定是否屬股權酬勞稀釋。SBC／營收與現金去向四分事實表未涵蓋。營運槓桿：2025 年營收年增 27.72%、營業利益年增約 67.5%，屬擴張而非壓縮。","valuation":"現價 168 元、Fwd P/E 15.48 倍（FY2026E 10.85 元）、FY2027E 12.54 倍；三年共識 EPS 年複合 27.3%，PEG 0.57。賣方：4 位分析師全數買進，平均目標 194 元（高 214、低 180，2026-07-27 快照），現價比平均低約 13%、也低於最低目標，全距倍數 1.19，方向支持不貴；摩根士丹利 2026-04 把目標價由 175 降至 165 元、評中性，與現價接近。反方向：P/S 2.37 倍、EV/S 2.09 倍皆位於四個年度端點的最高位置，本益比在四個年度端點的分位為 82.2（不是五年口徑，五年高低點事實表未涵蓋）。現價隱含什麼：若五年後倍數回到 13 倍，FY2031 EPS 只要約 12.9 元（較 FY2026E 年增約 3.6%）就能保本，所以風險不在成長不夠，而在 2028 年之後的循環回落與營益率回到 11–12%。同業 Forward P/E 事實表未涵蓋，無法做倍數對照。","premortem":"壓力測試以 Base 路徑 FY2028E 15.0 元為起點，之後三年 EPS 年增降到 15%／10%／5% 並分別配 14／12／10 倍，五年後股價約 319／240／174 元，三題都高於現價 168 元；第四題循環下行（FY2031E 9.5 元×10 倍＝95 元）不過，四題過三題。最大回撤推導：歷史最大回撤事實表未涵蓋；下界取 Bear 路徑谷底 FY2029E 8.5 元×9 倍≈77 元（約 −54%），再留 4pp 超跌空間至 −58%；上界取 EPS 停在 FY2026E 10.85 元、本益比由 15.48 倍壓到 10 倍（約 −35%），加 3pp 至 −38%。價值陷阱信號亮兩盞（EPS 成長遠高於營收成長、替代技術壓縮氣冷用量），判為中等。"},"plain":{"six":{"how_it_makes_money":"賺 AI 伺服器平台的散熱預算，錢卡在「風扇與風扇牆進入 GPU 平台參考設計與 ODM 供應名單」這一節點；伺服器網通與 AI 約占營收 48%，最新一季毛利率 31.25%、營益率 15.44%。","moat":"→ 穩定：風扇本業份額未見消長、毛利率守在四年高點，但液冷新賽道落後奇鋐與雙鴻；護城河為 C 級，來自平台認證與量產規模，不來自定價權。","growth":"🟡 中：AI 伺服器散熱需求可見到 2027 年，但風扇本業不是低滲透市場，液冷第二曲線還沒有營收占比證據；共識三年 EPS 年複合 27.3% 遠高於內生上限 10.7%，缺口靠利潤率擴張撐。","capital":"資本配置計分卡三項中兩項不適用（無併購、無回購）；唯一適用的股數稀釋項因股數增加來源不明，無法驗證通過，因此按 C 級計，持有年限上限為中期 2–5 年。這和本判斷的循環屬性不做長抱一致。2026 年現金轉向擴產，最新一季自由現金流只占營業現金流約三分之一。","valuation":"現價 168 元要求 FY2027–2028 達成共識 13.4、16.28 元，且 2028 年後不出現循環回落；前兩年我信，之後的延續不信——這是合理價，不是便宜價。","how_wrong":"🟡：最可能看錯的是把 AI 週期高點的利潤率當成新常態；壓力測試四題過三題，唯一不過的是 2028 年資本支出消化的循環年。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等法說會揭露液冷產品營收占比 ≥5% 且 TTM 營益率 ≥15% 再進場；現價不追","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":168.0,"week26_return_pct":27.24,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026E 分母未見一次性項目；爭點在利潤率是否處於週期高點，已反映在情境樹倍數，不屬分母爭議"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報與法說會（液冷出貨進度、2027 年資本支出）","impact":"高","watch":"毛利率是否守住 29%、液冷營收是否首度量化"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"水冷板放量（法說摘要稱第四季放量）","impact":"中","watch":"10–12 月月營收年增是否維持 20% 以上"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026 年報與股利政策","impact":"中","watch":"FY2026 EPS 對共識 10.85 元、年度 FCF／淨利"},{"date":"2027","date_precision":null,"type":"capacity","event":"液冷產品放量與菲律賓新廠投產（投產確切時點事實表未載）","impact":"高","watch":"液冷營收占比揭露、折舊上升後的營益率"}],"_projected_from":"v19"}
```
