你是 stock-analyst v20 的**散文層（prose）agent**，標的 2421.TW（2026-10-11）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：2421.TW　日期：2026-10-11　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1502B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（694B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1146B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1515B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1027B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（370B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（779B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2322B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4662B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2598B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1502           3849-5498      5 條（2–6 內）  
s3                  8000         694           5114-7306      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3688          7918-11312      5 條（2–6 內）  
s6                 11000         370          7441-10630      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         779           1905-2721      5 條（2–6 內）  
s10                 5000        2322           1875-2678      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2598           2000-2402      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5013B；至少需散文≈39.99KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−60
−58%
−50%
−35%
−35
−26%
−13.66%
−4.08%
−0.88%
0
0.74
0.75
0.8
1
1.07
1.2
1.39
1.5%
1.61
2
2.09
2.37
2.41
2.5
2.53
2.75
2.8%
2.8
3%
3.0
3
03
3.1
3.1%
3.119%
3.36%
3.9%
4
5
5%
5.24
5.65%
6
6%
06
6.05%
7.0
7
7%
7.1
7.1%
7.6
7.7
7.89
7.96%
8%
8
08
8.17%
8.3
8.6%
9
9.6
10%
10
10.6
10.75
10.9
11
11.1
11.4
12%
12.0
12
12.3
12.4%
12.6%
13.0
13
13%
13.2
13.3%
13.5
14%
14
14.5
15
15%
15.44%
15.6
15.63
15.8
15.85%
16.5
17%
17
17.54
17.8
18%
18
18.1
18.5
19.8
20%
20.5
20.8%
20.8
21%
21.08%
21.5
22%
22.55%
23%
23.2
23.56%
24
24.1%
25
26
27.24
27.72%
27.85%
28.87%
29%
30%
30
31%
31
31.06%
31.25%
31.65%
31.89%
32%
33.06%
34
34%
35%
38%
40%
42
42.63%
45
48%
49
53%
60%
66%
70
82
85
90
100%
100
104
110
123.7
130
145.32
150%
165
168
168.0
175
179.5
180
182
194
203
208.2
214
220
221
403.7
611.8
2025
2026
2027
2028
2029
2030
2421
3017
3324
3653
6230
20261011
5,418.6
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
{"meta":{"ticker":"2421.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"建準電機"},"oneliner":"建準靠伺服器風扇把毛利率推上近 32%，但液冷轉型落後奇鋐、雙鴻；168 元約為法人今年 EPS 的 15.6 倍，Base 五年年化約 7%，液冷營收證據出來前不追。","thesis":{"H":[{"id":"H1","text":"AI 伺服器與氣液混合散熱帶動風扇、風扇牆出貨，2026–2027 年營收維持雙位數成長","2y":"FY2026 營收年增 ≥18%（約 220 億元），FY2027 再增 ≥12%","5y":null,"10y":null,"threshold":"月營收 3 個月移動年增 ≥15%；FY2026 營收 ≥220 億元","source":"公開資訊觀測站月營收（每月 10 日前）與季報","drift_rule":"2 年期：TTM 營收偏離門檻路徑 ≥5% 連 2 季＝削弱，≥10% 連 3 季＝反轉"},{"id":"H2","text":"液冷產品（水冷板、CDU、Sidecar、水泵）在 Vera Rubin 世代量產，成為第二條成長曲線","2y":null,"5y":"液冷營收占比 2028 年 ≥20%、2030 年 ≥30%","10y":null,"threshold":"液冷營收占比 2027 年底 ≥10%、2028 年 ≥20%","source":"法說會產品別營收說明、年報","drift_rule":"5 年期：連 4 季偏離 ≥5%＝削弱，連 6 季偏離 ≥10%＝反轉；占比連 4 季未揭露視同削弱"},{"id":"H3","text":"產品組合升級抵銷液冷初期的低利益率，營業利益率守在歷史高檔附近","2y":null,"5y":"FY2026–FY2030 營業利益率平均 ≥14%、毛利率 ≥29%","10y":null,"threshold":"TTM 營業利益率 ≥14%；單季毛利率 ≥29%","source":"公開資訊觀測站季報","drift_rule":"5 年期：TTM 營業利益率連 4 季低於門檻 5% 以上（<13.3%）＝削弱，連 6 季低於 10% 以上（<12.6%）＝反轉"}],"R":[{"id":"R1","text":"AI 伺服器專案受記憶體、PCB、晶片供應延後，出貨遞延","h_ref":"H1","clock":"⚡","threshold":"月營收 3 個月移動年增 <10% 連 2 個月","evidence_refs":["end_markets#2"]},{"id":"R2","text":"液冷替代壓縮每機櫃風扇含量，而建準液冷份額落後，毛利率下滑","h_ref":"H2","clock":"🔥","threshold":"單季毛利率 <29% 連 2 季，或 2027 年底液冷營收占比仍 <10%","evidence_refs":["substitute_technology#0","end_markets#2","supply_demand_durability#0"]},{"id":"R3","text":"AI 資本支出進入消化期，營收轉負、利益率回到 FY2023–24 的 11–12%","h_ref":"H3","clock":"🐢","threshold":"TTM 營業利益率 <12% 且營收年增轉負","evidence_refs":["supply_demand_durability#2"]},{"id":"R4","text":"菲律賓新廠與液冷擴產吃掉現金，自由現金流長期低於淨利","h_ref":"H3","clock":"🔥","threshold":"年度自由現金流÷淨利 <0.75 連 2 年","evidence_refs":["capital_markets_pricing#2"]}],"single_thing":{"description":"2027 年 6 月底前，建準的水冷板或 CDU 沒有進入 NVIDIA Vera Rubin 世代機櫃的量產出貨","why_fatal":"AI 晶片液冷滲透率 2027 年近 60%，拿不到液冷訂單時建準在 AI 機櫃只剩風扇，且每櫃風扇含量被水冷板壓縮；EPS 路徑由 Base 落到 Bear（FY2031E 14.5→8.3 元），倍數同時由 14 倍降到 10 倍，是本份對終值影響最大的單一變數","if_happens":"持有者清倉；未持有者移出觀察，Bear 機率由 30% 上調至 40% 重跑","how_monitor":"每季法說的液冷營收占比與出貨說明、月營收是否出現液冷貢獻的跳升、菲律賓新廠稼動","probability":"35%（12–24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":7.89,"FY2026E":10.75,"FY2027E":null,"FY2028E":null},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS。FY2025A 取年報 7.89 元；FY2026E 取法人預估 10.6–10.9 元中值（MoneyWeekly，2026-08-31，家數未揭露）；FY2027E、FY2028E 共識事實表未涵蓋，留空不推估"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2421.TW_20261011/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收隨 PC 與 AI 伺服器週期擺動：FY2023 年減 8.17%、FY2025 年增 27.72%；毛利率隨產品組合與稼動率從 22.55% 升到 31.89%，高點落在 AI 週期內"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性：TrendForce（2026-08）預估 2027 年 GPU 機櫃出貨仍年增逾 30%、AI 晶片液冷滲透率近 60%，Kyber NVL144 可能延後；需求綁雲端業者 AI 資本支出，消化期來時會反轉","bargaining":{"up":"上游為馬達、IC、塑料等通用零件，供應商集中度事實表未涵蓋","down":"下游為伺服器 ODM 與雲端業者，買方集中、每代平台重開設計案；前幾大客戶占比事實表未涵蓋","geo":"菲律賓新廠擴產（2026 資本支出上調至 15 億元以上）分散產地；關稅與出口管制查無資料"},"profit_pool_dir":"散熱利潤池往水冷板、CDU 與液冷一條龍廠商移動；建準風扇段利益率創高，液冷段份額未證","tam_table":[{"item":"AI 晶片液冷滲透率 2026E","value":"53%（TrendForce，2026-08）"},{"item":"AI 晶片液冷滲透率 2027E","value":"接近 60%（TrendForce）"},{"item":"GPU 機櫃出貨 2027E 年增","value":"逾 30%（TrendForce；Kyber NVL144 可能延後）"},{"item":"建準 AI 伺服器風扇市占","value":"約 30%（報導未標年份）；2025 年 3 月分析稱全球第二大散熱風扇廠"},{"item":"風扇專屬 TAM／SAM 與段 CAGR","value":"事實表未涵蓋"},{"item":"散熱營業利益池占比 5 年前→現","value":"事實表未涵蓋，利潤池流出幅度無法量化"}]},"moat":{"mechanism":"高轉速伺服器風扇須通過 NVIDIA 參考設計與 ODM 散熱驗證，加上磁浮馬達技術；轉換成本只在單一平台世代內有效，每代重開設計案","execution":6,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行面穩定：風扇段創新高（毛利率 FY2022 22.55%→TTM 31.89%、營益率 7.96%→15.85%），但液冷進度落後雙鴻、奇鋐，一升一落；定價面穩定：毛利率高於直接同業，但查無漲價或份額擴張證據，摩根士丹利 2026 年 4 月因液冷貢獻待放大把目標價由 175 降到 165 元；AI 伺服器風扇市占約 30% 的報導無年份，份額方向無直接證據","threats":[{"level":"🔴","text":"液冷替代：GB200 的 CPU／GPU 已改用水冷板，風扇只負責其餘元件；AI 晶片液冷滲透率 2027 年近 60%，每機櫃風扇含量被壓縮。目前是部分替代（氣液混合），尚未到全面架構替代","p":"35%","evidence_refs":["substitute_technology#0","supply_demand_durability#1","substitute_technology#2"]},{"level":"🟡","text":"奇鋐、雙鴻在液冷段先行，水冷板與 CDU 設計案先被拿走，建準液冷 2026 年第三季小量送驗、2027 年才放量","p":"40%","evidence_refs":["end_markets#2"]},{"level":"🟡","text":"台達、尼得科等大型馬達廠在伺服器風扇點對點競爭；具名設計定案與新進者搶單的證據查無","p":"20%","evidence_refs":["competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知：營益率 15.85% 屬中高，投入資本事實表未涵蓋，周轉率與當期 ROIC 無法計算","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心、決策者是 NVIDIA 參考設計與 ODM 散熱工程、付款者是雲端業者，三環都成立，散熱是不能延後的需求。但客戶要解決的是發熱，風扇只是目前解法之一：GB200 的 CPU／GPU 已改水冷板，液冷滲透率 2027 年近 60%，需求在、解法在換"},{"item":"決策層級","level":"🟡","text":"替代性在每個平台世代的散熱設計案衡量，不在風扇這個品類；公司自述為 GB200／GB300 推薦供應商，但每代平台都重開設計案，轉換成本只在世代內有效。流失率、重新認證週期等代理變數事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"機櫃價值大頭在 GPU，散熱環節內的價值正往水冷板與 CDU 移；建準毛利率 31.89% 高於奇鋐、雙鴻，但營益率 15.85% 低於奇鋐 23.56%，在散熱利潤池分到的比例不是最大；採購收斂到液冷一條龍廠商時，建準議價會轉弱"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的零組件，不是民生必需品，沒有漲價的社會或政治上限，也不依賴監管授權"}],"roiic":"事實表未涵蓋（投入資本、折舊攤銷、營運資金變動皆缺），無法推導","reinvest_rate":"盈餘保留率約 34%：TTM 殖利率 3.119%×168 元＝每股股息約 5.24 元，對 FY2025 EPS 7.89 元配發約 66%；資本支出口徑的再投資率事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；增量 ROIC 缺，天花板留空，情境樹不以內生上界替 Base 成長背書，Base EPS 年化約 6% 只靠產業量能與利益率持平"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","2421.TW":31.89,"3017.TW":28.87,"3324.TWO":27.85,"3653.TW":42.63,"6230.TW":15.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","2421.TW":15.85,"3017.TW":23.56,"3324.TWO":15.3,"3653.TW":33.06,"6230.TW":-0.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","2421.TW":5.65,"3017.TW":24.1,"3324.TWO":-13.66,"3653.TW":15.18,"6230.TW":-4.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","2421.TW":6.05,"3017.TW":3.36,"3324.TWO":5.57,"3653.TW":3.61,"6230.TW":7.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3017.TW 奇鋐","gm":28.87,"om":23.56,"fcf_margin":24.1,"rd_intensity":3.36,"strategy_note":"液冷一條龍領先者，營益率 23.56%、FCF 利潤率 24.1% 都遠高於建準，是建準液冷轉型最直接的對手","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3324.TWO 雙鴻","gm":27.85,"om":15.3,"fcf_margin":-13.66,"rd_intensity":5.57,"strategy_note":"液冷擴產期以現金換份額，FCF 利潤率 −13.66%、毛利率 27.85% 低於建準，但液冷進度領先建準","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3653.TW 健策","gm":42.63,"om":33.06,"fcf_margin":15.18,"rd_intensity":3.61,"strategy_note":"產品線不同，不是風扇直接對手；毛利率 42.63%、營益率 33.06%，只作散熱零組件利益率的上緣參考","period":"TTM ending 2026-06-30（4季加總）"},{"name":"6230.TW 尼得科超眾","gm":15.39,"om":-0.88,"fcf_margin":-4.08,"rd_intensity":7.5,"strategy_note":"營益率 −0.88%、FCF 利潤率 −4.08%，散熱模組的落後者賺不到錢，說明這行份額落後的代價","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（AI 伺服器機櫃出貨）為主，加上組合（高轉速伺服器風扇、風扇牆）與產能（菲律賓新廠）；無併購與回購貢獻","runway_years":"約 5 年（中等折扣）：以液冷第二曲線為前提，建準液冷營收占比未揭露，滲透進度無法量測","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 不可得，內生天花板留空；FY2022–FY2025 自由現金流每年為正（11.1–23.2 億元），成長期間未出現現金缺口，只能作為自籌成長的旁證","segments":[{"item":"伺服器網通與 AI","value":"48%"},{"item":"IT（筆電／PC）","value":"22%"},{"item":"車用電子","value":"12%"},{"item":"工業與醫療","value":"10%"},{"item":"其他","value":"8%（以上為 2026 年 3 月口徑，原始出處未確認，可能非最新）"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q2 2026 毛利率 31.25%，TTM 31.89% 高於 FY2025 31.06%；去年同季值事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"份額消長無直接證據，屬資料缺口而非否證"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"查無提價紀錄"},{"signal":"EPS 成長顯著高於營收成長（差逾 5pp）","lit":true,"note":"FY2022–FY2025 EPS 年化約 22%、營收年化約 10%，差約 12pp，來自利益率擴張"},{"signal":"FCF÷淨利連 2 年低於 0.75","lit":false,"note":"FY2024 0.74、FY2025 1.07，未連兩年；TTM FCF 利潤率 5.65% 偏弱，列觀察"},{"signal":"SBC 占營收逾 5% 且逐年上升","lit":false,"note":"SBC 事實表未涵蓋；稀釋股數三年增 8.6%，來源待查"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"note":"水冷板接手 CPU／GPU 散熱，每機櫃風扇含量下降"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"P/S 與 EV/S 在 4 個年度端點最高，方向相反"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"維持與擴張資本支出拆分事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"菲律賓新廠擴產中，營收連兩年成長"}],"trap_rating":"價值陷阱風險中、長期成長性中（亮兩項）"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長沒有靠併購撐，回饋以現金股利為主；分年股利、回購與增資明細事實表未涵蓋"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"證據包查無併購紀錄（重大併購軸查無）","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表與證據包查無回購紀錄","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"以淨利÷稀釋 EPS 推算稀釋股數 FY2022 約 2.53 億股→FY2025 約 2.75 億股，年化約 2.8%；股權激勵金額與股數增加來源事實表未涵蓋，無法判定是否超過 1.5%／年的稀釋門檻","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（法人 FY2026E 中值 10.75 元）為主，trailing 本益比與 P/S 的年度端點分布為輔","peers":{"expanded":false,"reason":"同業本益比事實表未涵蓋，只有利益率對照；健策產品線不同，不跨產品線當估值錨"},"fwd_pe":15.63,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比約 15.6 倍對年增兩成的營收不算貴，但分子是週期高檔利益率，營收倍數已在 4 年端點頂部；三年共識 EPS 事實表未涵蓋、PEG 不可得，五年分位也不可得（只有 4 個年度端點）。綜合判合理偏滿：不便宜，也沒到過熱","upside_short_pct":7.1,"upside_mid_pct":20.8},"trap_analysis":{"verdict":"🟡","label":"價值陷阱風險中：EPS 成長靠利益率擴張、風扇含量受液冷壓縮兩項亮燈"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"GB200 的 CPU／GPU 已改水冷板，風扇只負責其餘元件；建準液冷進度落後雙鴻、奇鋐，液冷產品 2026 年第三季才小量送驗、2027 年放量；摩根士丹利 4 月因液冷貢獻待放大把目標價由 175 降至 165 元","assumption":"氣液混合仍是未來數年主流，建準能在 Vera Rubin 世代拿下水冷板或 CDU 的量產訂單","consequence":"液冷拿不下時，AI 段只剩風扇且單位含量被壓，EPS 回到 7–8 元、本益比 10 倍，股價約 70–85 元，五年虧損約一半","ruling":"採納為 Bear 主路徑，機率 30%；與唯一致命事件是同一條故事，兩者一致","watch":"法說揭露的液冷營收占比；單季毛利率是否守在 29% 以上","evidence_refs":["substitute_technology#0","end_markets#2","supply_demand_durability#0"],"fact_refs":["f_peer_2421_tw_gross_margin_pct","f_peer_3017_tw_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"TTM 自由現金流利潤率 5.65%，FY2025 為 12.4%；Q2 營業現金流 611.8 百萬元中 403.7 百萬元用於資本支出；2026 資本支出上調至 15 億元以上；稀釋股數 FY2022 約 2.53 億股、FY2025 約 2.75 億股，三年增 8.6%","assumption":"液冷放量後利益率不被拉低，擴產回收期合理，股數不再增加","consequence":"營收成長但每股自由現金流不增：液冷整合方案利益率可能低於高階風扇，擴產占用現金，股數年增約 3%，每股價值成長落後營收","ruling":"部分採納：FCF 轉換率與股數變化是本份最大資料缺口，Base 情境 EPS 年化只給約 6%，不給液冷放量的利益率加分","watch":"年度 FCF÷淨利是否回到 0.8 以上；稀釋股數年增是否壓到 1.5% 以下","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_kpi4","f_peer_2421_tw_fcf_margin_pct","f_kpi3_eps"]},{"view":"價格已反映太多","evidence":"P/S 2.37 倍、EV/S 2.09 倍都是近 4 個年度端點最高，trailing 本益比 17.54 倍在第 82 分位；同期毛利率 31.89%、營益率 15.85% 也在最高，等於用高檔倍數買高檔利益率","assumption":"利益率在 AI 週期後仍能維持 FY2025 的水準","consequence":"利益率回到 FY2023–24 的 11–12% 且倍數回到中段，股價下修 30–40%","ruling":"部分採納：以法人 FY2026E 計 15.6 倍並不極端，但營收倍數在頂端；Base 終端倍數取 14 倍，不給再評價","watch":"P/S 與營益率是否同步回落；法人 FY2026E 是否在第三季財報後下修","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_ps_current","f_ps_percentile","f_pe_current","f_pe_percentile","f_ev_s_current","f_ev_s_percentile"]}],"max_dd":{"lo":-60,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 168.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=168.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"液冷轉型進度","cause":null,"prior_field":null,"side_a":"公司端：氣液混合設計未來數年仍是主流，建準為 GB200／GB300 推薦供應商；水冷板預計第四季放量，2026 資本支出上調至 15 億元以上","side_b":"外部：液冷進度落後雙鴻、奇鋐，另一資料稱液冷 2026 年第三季小量送驗、2027 年放量；摩根士丹利因液冷貢獻待放大降目標價至 165 元；沒有液冷營收占比數字","ruling":"可調和（時程與幅度差異）。採外部側為基準：公司說法沒有附營收數字，推薦供應商身分屬公司自述；液冷營收占比揭露前，Base 不計液冷份額","evidence_level":"雙方都是法說摘要與媒體轉述，非逐字原文；外部側有券商與產業研究兩個獨立來源","settle_metric":"法說揭露的液冷營收占比；Vera Rubin 世代水冷板或 CDU 量產出貨","if_then":["若 2027 年第二季前法說揭露液冷營收占比 ≥10% 且單季毛利率 ≥29%，重跑本份，通過後首倉 3%","反向：若 2027-06-30 前仍無量產出貨證據，持有者清倉，未持有者移出觀察並把 Bear 機率上調至 40% 重跑"],"evidence_refs":["end_markets#2","substitute_technology#2","supply_demand_durability#0","capital_markets_pricing#2"]},{"axis":"法人今年 EPS 與實際跑速","cause":null,"prior_field":null,"side_a":"法人預估 2026 全年 EPS 10.6–10.9 元（8 月底），4 位分析師全數買進、目標價均值 194 元","side_b":"Q2 單季 EPS 2.41 元，年化約 9.6 元；7–8 月營收月均約 20.5 億元，比 Q2 月均約 18.1 億元高約 13%，營收面只補得了一部分，其餘要靠下半年利益率再擴張","ruling":"可調和（程度差異）。本份把 10.75 元當上緣，不在其上再加成長；賣方目標價全距 180–214 元，最高÷最低約 1.2 倍，分歧小、方向比本份樂觀，市場假設是風扇段的高檔利益率可延續","evidence_level":"法人預估為媒體轉述；Q2 EPS 與月營收為已實現數字","settle_metric":"2026 年第三季單季 EPS 與毛利率","if_then":["若第三季單季 EPS ≥2.8 元且毛利率 ≥31%，上調 Base 2027 年 EPS，仍等液冷證據","反向：若第三季單季 EPS <2.5 元，法人全年估值須下修，Bear 機率上調至 35% 重跑"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#0","end_markets#0"]},{"axis":"觀望或現在就買","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：前 8 月營收年增 21%、液冷滲透率 2027 年近 60%、GPU 機櫃出貨仍增逾 30%；以法人 FY2026E 計本益比約 15.6 倍、殖利率 3.1%，毛利率高於奇鋐與雙鴻","side_b":"Base 五年年化報酬約 7%（股價約 3.9%＋股息 3.1%），低於 8% 的及格線；液冷份額沒有營收證據，Bear 情境下跌約一半","ruling":"選觀望。約束只有一條：液冷份額沒有證據。這條被否定（液冷營收占比揭露達一成，或量產出貨確認）就重跑；股價本身不是約束","evidence_level":"Base 報酬為本份情境推導；液冷份額缺口有券商與媒體兩方來源","settle_metric":"液冷營收占比或 Vera Rubin 世代量產出貨確認","if_then":["若液冷營收占比 ≥10% 揭露，重跑本份，Bull 機率可上調至 35%，通過後首倉 3%","價格先走、證據未到：股價先漲過 194 元而液冷證據未到，不追","價格先走、基本面無損：股價跌到 130 元以下而月營收年增仍 ≥15%，Base 年化回到約 13%，重跑本份評估分批反買"],"evidence_refs":["end_markets#0","supply_demand_durability#1","end_markets#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：TrendForce 預估 AI 晶片液冷滲透率 2026 年 53%、2027 年近 60%，GPU 機櫃出貨 2027 年仍年增逾 30%；摩根士丹利認為液冷需求延續到 2027 年","side_b":"其他結構變數（替代技術）：水冷板接手 CPU／GPU 散熱，風扇單位含量下降。競爭面：奇鋐、雙鴻在液冷領先，台達、尼得科的具名搶單證據查無","ruling":"雙向拉鋸：需求面結構轉好，替代技術軸對風扇本業不利，淨效果取決於建準能否把風扇客戶帶進液冷產品","evidence_level":"產業研究與券商報告，皆為轉述","settle_metric":"風扇與液冷的產品別營收","if_then":["若 2027 年液冷滲透率升到 60% 時風扇相關營收仍年增，代表混合架構撐住，替代風險降級","反向：若 2027 年風扇相關營收年減，替代風險升為架構替代，Bear 機率上調至 40% 重跑"],"evidence_refs":["supply_demand_durability#1","substitute_technology#0","competitive_share_entrants#2","supply_demand_durability#0"]}],"triggers":[{"n":1,"text":"月營收年增維持兩位數，驗證 AI 機櫃帶動風扇出貨","type":"假設驗證","maps_to":"H1","metric":"月營收年增率（3 個月移動）","threshold":"≥15%","action":"論點維持；跌破 10% 連 2 個月改走第 6 條","source_freq":"公開資訊觀測站月營收，每月 10 日前","date":"2026-11-10","evidence_refs":["end_markets#0"]},{"n":2,"text":"液冷營收占比揭露並達一成，第二曲線成形","type":"假設驗證","maps_to":"H2","metric":"液冷產品營收占比","threshold":"2027 年底前 ≥10%，2028 年 ≥20%","action":"達標即重跑本份，評估首倉 3%","source_freq":"法說會，每季","date":"2027-12-31","evidence_refs":["end_markets#2"]},{"n":3,"text":"毛利率跌破 29% 連兩季，代表液冷替代與份額落後開始吃到風扇本業","type":"減碼","maps_to":"R2","metric":"單季毛利率（GAAP）","threshold":"<29% 連 2 季","action":"持有者減碼一半；未持有者撤回首倉條件","source_freq":"季報，每季","date":null,"evidence_refs":["substitute_technology#0"]},{"n":4,"text":"Single Thing：Vera Rubin 世代液冷量產出貨期限","type":"Single Thing","maps_to":"Single Thing","metric":"建準水冷板或 CDU 進入 Vera Rubin 世代機櫃量產出貨","threshold":"2027-06-30 前未見量產出貨證據","action":"持有者清倉；未持有者移出觀察，Bear 機率上調至 40% 重跑","source_freq":"法說會與公司公告，每季","date":"2027-06-30","evidence_refs":["end_markets#2","supply_demand_durability#0"]},{"n":5,"text":"重啟條件：液冷份額出現證據","type":"估值rearm","maps_to":"H2","metric":"液冷營收占比或量產出貨確認","threshold":"法說揭露液冷營收占比 ≥10%，或確認 Vera Rubin 世代水冷板或 CDU 已量產出貨","action":"重跑本份；通過後首倉 3%，下一季毛利率 ≥29% 再加到 5%","source_freq":"法說會，每季","date":null},{"n":6,"text":"出貨遞延：AI 專案受記憶體、PCB、晶片供應延後","type":"風險","maps_to":"R1","metric":"月營收年增率（3 個月移動）","threshold":"<10% 連 2 個月","action":"持有者減碼三分之一，凍結加碼到下一份季報","source_freq":"公開資訊觀測站月營收，每月","date":null,"evidence_refs":["end_markets#2"]},{"n":7,"text":"擴產吃現金：自由現金流長期低於淨利","type":"風險","maps_to":"R4","metric":"年度自由現金流÷淨利","threshold":"<0.75 連 2 年","action":"暫停加碼，Base 終端倍數下調 1 倍重跑","source_freq":"年報，每年","date":"2027-03-31","evidence_refs":["capital_markets_pricing#2"]},{"n":8,"text":"第三季財報複審：檢查法人全年 EPS 是否站得住（日期為推估，前一季於 8 月 7 日公告）","type":"複審日期","maps_to":"H3","metric":"2026 年第三季單季 EPS 與毛利率","threshold":"EPS ≥2.8 元且毛利率 ≥31% 為達標；EPS <2.5 元為不達標","action":"不達標時 Bear 機率上調至 35% 重跑；達標維持等液冷證據","source_freq":"季報","date":"2026-11-14"}],"kill_metrics":[{"metric":"單季毛利率（GAAP）","bear_threshold":"連 2 季低於 29%","window":"2026 年第三季至 2027 年第四季","source":"公開資訊觀測站季報","last_status":"ok"},{"metric":"月營收年增率（3 個月移動）","bear_threshold":"連 2 個月低於 10%","window":"2026-10 至 2027-12","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"Vera Rubin 世代水冷板或 CDU 量產出貨","bear_threshold":"2027-06-30 前未見量產出貨證據","window":"至 2027-06-30","source":"法說會、公司公告","last_status":"unknown"},{"metric":"年度自由現金流÷淨利","bear_threshold":"連 2 年低於 0.75","window":"FY2026–FY2027","source":"年報現金流量表","last_status":"warning"},{"metric":"TTM 營業利益率","bear_threshold":"低於 12% 且營收年增轉負","window":"2027–2029","source":"公開資訊觀測站季報","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場（4 位分析師全數買進、目標價均值 194 元）假設風扇段的高檔利益率可延續、液冷會順利接棒；本份認為液冷份額沒有營收證據，P/S 已在 4 年端點最高，市場把週期高點的利益率當成常態"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=27.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='不追 168 元；等法說揭露液冷營收占比達一成，或 Vera Rubin 世代水冷板或 CDU 量產出貨確認後重跑'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"法說揭露液冷產品營收占比達一成以上，或確認 Vera Rubin 世代水冷板或 CDU 已量產出貨","exec_line":"重啟條件成立後先重跑本份；仍成立則首倉 3%，下一季毛利率守 29% 以上再加到 5%；條件未到前股價上漲不追，下跌只在基本面無損時重算"},"reasoning":{"industry":"營收結構（2026 年 3 月口徑，可能非最新）：伺服器網通與 AI 48%、筆電與 PC 22%、車用 12%、工業與醫療 10%、其他 8%。最新一季（2026 年第二季，8 月 7 日公告）營收 5,418.6 百萬元、毛利率 31.25%、營業利益率 15.44%。毛利率高於奇鋐 28.87% 與雙鴻 27.85%，但 TTM 營益率 15.85% 低於奇鋐 23.56%。產業時鐘判擴張期，依據是出貨量而非股價：2026 前 8 月營收 145.32 億元、年增 21.08%，7 月年增 31.65%。供需持久性：週期性將反轉的風險中等，需求綁在雲端業者 AI 資本支出，TrendForce 仍預估 2027 年 GPU 機櫃出貨增逾 30%，但風扇的單位含量正被液冷壓縮。單點依賴：前一至兩大客戶占比與供應商集中度事實表未涵蓋，無法判定是護城河證據還是集中度風險，列資料缺口。最新一季逐字稿缺，管理層說法只能用法說摘要與媒體轉述。","moat":"機制是高轉速伺服器風扇須通過 NVIDIA 參考設計與 ODM 散熱驗證，換供應商要重新驗證，但每個平台世代都重開設計案，轉換成本只在世代內有效。可證方向：對最強同業奇鋐，毛利率高 3.0pp、營益率低 7.7pp、FCF 利潤率低 18.5pp；ROIC 對照所需的投入資本事實表未涵蓋，改用利益率軸。份額：AI 伺服器風扇市占約 30% 的報導無年份，份額消長無直接證據，最大客戶份額方向也查無。執行面 6 分：風扇段創新高，但液冷落後雙鴻、奇鋐，TTM FCF 利潤率只有 5.65%。定價面 6 分：毛利率是直接同業最高，但查無漲價證據，液冷段議價未建立，摩根士丹利因液冷貢獻待放大降目標價。報酬持續期：當期 ROIC 無法計算；四個檢查點三黃一綠，需求還在、解法在換。","growth":"成長以量為主（AI 機櫃出貨），加上高轉速風扇與風扇牆的組合升級、菲律賓新廠產能，沒有併購與回購貢獻。三年共識：只有法人 FY2026E 10.6–10.9 元（較 FY2025 的 7.89 元增約 34–38%），FY2027E、FY2028E 事實表未涵蓋，三年 CAGR 不可得；內生天花板也因增量 ROIC 缺而不可得，缺口無法歸因，長期信心上限為中。FY2022–FY2025 EPS 年化約 22%、營收年化約 10%，差 12pp 來自利益率擴張，不可外推。Runway：AI 晶片液冷滲透率 2026 年已達 53%，產業層的液冷不是早期市場；建準液冷營收占比未揭露，第二曲線存在但份額沒有證據，所以判中不判寬。衰退信號亮兩項：EPS 成長高於營收成長逾 5pp、液冷壓縮風扇單位含量。FCF÷淨利 FY2024 為 0.74、FY2025 回到 1.07，未連兩年，列觀察。","governance":"現金轉換：FCF÷淨利 FY2022 1.61、FY2023 1.39、FY2024 0.74、FY2025 1.07；TTM FCF 利潤率 5.65%，Q2 營業現金流 611.8 百萬元、資本支出 403.7 百萬元、FCF 208.2 百萬元，2026 資本支出上調至 15 億元以上投入菲律賓新廠。股東回饋：TTM 殖利率 3.119%，換算每股股息約 5.24 元，對 FY2025 EPS 7.89 元配發約 66%。併購與回購：證據包查無。股數：以淨利÷稀釋 EPS 推算，FY2022 約 2.53 億股、FY2025 約 2.75 億股，三年增 8.6%、年化約 2.8%，來源（員工酬勞、可轉債或盈餘轉增資）事實表未涵蓋，無法判斷是否屬經濟性稀釋。SBC 占營收、債務到期與利率、現金去向四分事實表未涵蓋。","valuation":"現價 168 元（事實表單位標為 USD，實為新台幣，與 EPS 同幣別，倍數自洽）。trailing 本益比 17.54 倍，在近 4 個年度端點中排第 82 分位；P/S 2.37 倍、EV/S 2.09 倍都是 4 個端點最高。以法人 FY2026E 中值 10.75 元計，前瞻本益比約 15.6 倍，和法人 8 月底在 179.5 元時算的 16.5–17 倍一致。賣方：4 位分析師全數買進，目標價均值 194 元（180–214），摩根士丹利 4 月中性、165 元。短期上檔取 Base FY2027E 12.0 元×15 倍＝180 元（+7.1%），中期取 Base 五年終值 14 倍×14.5 元＝203 元（+20.8%）。同業本益比事實表未涵蓋，不以產品線不同的健策當估值錨。","premortem":"往下的故事見反證紀錄第一條：液冷份額拿不下與 AI 資本支出消化同時發生，EPS 回到 7–8 元。Max DD 範圍 −35% 至 −60% 由情境推導，歷史最大回撤事實表未涵蓋。成長熄火壓力測試：以 Base FY2028E 13.0 元計，成長降到 15%／10%／5% 對應本益比約 17／14／10 倍，股價 221／182／130 元，前兩個不跌破現價，第三個跌約 23%。往上：若建準在 Vera Rubin 世代拿下水冷板與 CDU，Base 年化約 6% 的 EPS 成長明顯太低。訴訟、監管、重大事件各軸查無紀錄。"},"plain":{"six":{"how_it_makes_money":"賺 AI 伺服器、筆電與車用散熱風扇的錢，錢卡在高轉速伺服器風扇的平台設計認證這一節；散熱價值正往水冷板與 CDU 移，建準在新節點還沒站穩。","moat":"→ 穩定：風扇段利益率續創新高，液冷段落後奇鋐與雙鴻，兩股力量相抵","growth":"🟡 中：風扇是成熟產品，液冷這條第二曲線在產業層已經成形，建準的份額還沒有營收證據","capital":"資本主要用在現金股利（配發約六成五）與菲律賓擴產；沒有併購與回購紀錄，股數三年增 8.6% 的來源待查，配置紀律證據不足以給高評價","valuation":"現價 168 元要求今年 EPS 做到法人的 10.6 元以上、明年再成長，且市場繼續給 15 倍以上本益比；風扇段做得到，液冷段沒有證據，只信一半","how_wrong":"最可能看錯在液冷份額：拿不下時利益率回到 FY2023–24 的 11–12%、本益比 10 倍，股價約 70–85 元；拿下時本份 Base 太保守"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場（4 位分析師全數買進、目標價均值 194 元）假設風扇段的高檔利益率可延續、液冷會順利接棒；本份認為液冷份額沒有營收證據，P/S 已在 4 年端點最高，市場把週期高點的利益率當成常態","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不追 168 元；等法說揭露液冷營收占比達一成，或 Vera Rubin 世代水冷板或 CDU 量產出貨確認後重跑","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":168.0,"week26_return_pct":27.24,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母用法人 FY2026E 中值 10.75 元；Q2 單季 2.41 元年化約 9.6 元，差距要靠下半年營收與利益率同時上升，屬程度差異，沒有一次性項目"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026 年第三季財報與法說會（日期為推估，前一季於 8 月 7 日公告）","impact":"高","watch":"單季 EPS 是否 ≥2.8 元、毛利率是否守 31%、液冷營收占比是否揭露"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"水冷板預計第四季放量（法說摘要）","impact":"高","watch":"11 月至隔年 1 月月營收是否出現液冷貢獻的跳升"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"2026 年全年財報與股利政策","impact":"中","watch":"全年 FCF÷淨利、稀釋股數變化、2027 年資本支出"},{"date":"2027-06","date_precision":"month","type":"product","event":"Vera Rubin 世代液冷量產出貨檢查點","impact":"高","watch":"水冷板或 CDU 是否已量產出貨"}],"_projected_from":"v19"}
```
