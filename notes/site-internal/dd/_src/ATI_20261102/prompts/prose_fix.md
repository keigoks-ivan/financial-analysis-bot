你是 stock-analyst v20 的**散文層（prose）agent**，標的 ATI（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ATI　日期：2026-11-02　archetype：None　前份裁決：2026-10-13　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1690B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（387B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（986B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1558B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1092B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（370B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（958B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2085B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4061B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3224B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1690           3717-5310      5 條（2–6 內）  
s3                  8000         387           5329-7613      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3636          7955-11364      5 條（2–6 內）  
s6                 11000         370          7441-10630      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         958           1779-2542      5 條（2–6 內）  
s10                 5000        2085           2040-2915      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3224           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4654B；至少需散文≈40.35KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65
−65%
−61%
−55%
−40%
−40
−11.9%
−2.5%
0
0.1%
0.4%
0.4
0.46
0.55
0.6%
0.63%
0.65
0.7
0.75
0.83
0.85
1
01
1.1%
1.2
1.26
1.28
1.358
1.5%
1.58
1.7
02
2
2%
2.2
2.23
2.4
2.6
2.7%
2.8%
2.8
2.85
3.0
3%
3
3.05
3.1%
3.15
3.28
3.3
3.35
3.4
3.45
3.5%
3.5
3.55
3.8
4
4.25
4.3
4.49
4.5
4.7
4.77
05
5%
5
5.20
5.2
5.21
5.5
5.75
5.8
5.875%
6.0
6%
6
06
6.2
6.35
6.37
6.4%
6.43
6.65
6.7%
6.7
6.8
7
7.0
7.02
7.06
7.20
7.2
7.21
7.52
7.85
8
08
8%
8.3
8.4%
8.60
8.6
8.7%
8.8%
9
9.1
10
10%
10.5%
10.7%
10.8
11
11%
11.1
11.4
11.5
11.9%
11.95
12
12.4%
13
13.2
14
14%
14.15
14.2
14.3%
14.3
14.6
14.9
15
15%
16
16%
16.5%
16.8%
17
18%
18.6%
19.8%
20%
20
20.1%
22
22.0%
22%
22.0
23%
23
23.2%
23.4%
24
24%
24.5%
25
25%
25.75
25.8%
25.8
26%
26
28
28.0%
29
30
30%
31
31.78
31.8
32.9%
34%
35%
38.5
39%
40
40%
41.4
42
43
44
45
45%
49%
49
50%
55%
65
70
75
75.2
79.5
81%
90%
92%
93%
98.4
99
100%
100
141
150%
153
154
165.59
165.6
175
187.98
189
200
265
302.4
348
840
850
2020
2021
2025
2026
2027
2028
2029
2030
2031
2033
2036
20261102
1,410
1,500
2,000
2,800
3,000
4,000
5,000
7,000
8,754
9,000
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
{"meta":{"ticker":"ATI","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"ATI Inc."},"oneliner":"Q3 第三次上修、引擎合金定價權擴大，但倍數仍在自身區間頂部，業界新產能2027下半年起投產；不追，等股價≤154美元且2027指引 EBITDA 中點≥13億美元","thesis":{"H":[{"id":"H1","text":"引擎、國防與特殊能源需求加上長約重新定價，使 FY2027 調整後 EPS 達6.0美元以上（共識6.43）","2y":"FY2027 調整後 EPS≥6.0美元、EBITDA≥13億美元","5y":null,"10y":null,"threshold":"2027 年調整後 EBITDA≥13億美元（2026 指引中點11.95億）；噴射引擎營收年增≥15%","source":"季報新聞稿、2026-11-12 投資人日、2027-02 Q4 法說指引","drift_rule":"TTM 調整後 EBITDA 較此路徑連2季偏離≥5%為削弱、連3季≥10%為反轉"},{"id":"H2","text":"AA&S 組合轉向（航太國防占比由2021年18%升至45%）與長約，讓兩分部 EBITDA 利益率在2027下半年至2030業界新產能投產後仍守住20%以上","2y":null,"5y":"2031 年合併調整後 EBITDA 利益率≥20%","10y":null,"threshold":"AA&S 與 HPMC 分部利益率皆≥20%；合併調整後 EBITDA 利益率≥20%","source":"每季分部資料、續約揭露、交期口述","drift_rule":"利益率較門檻低5%（約1個百分點）連4季為削弱、低10%（約2個百分點）連6季為反轉"},{"id":"H3","text":"新世代引擎單機含量為舊引擎兩倍以上，熱段合金多為獨家或雙源，新機與維修各半，使引擎業務成長延續到2030年代","2y":null,"5y":null,"10y":"2036 年引擎營收占全公司仍≥40%，熱段合金無客戶雙源化","threshold":"無主要引擎客戶導入第二供應商；噴射引擎營收占全公司≥40%","source":"10-K 客戶與競爭揭露、法說會終端市場拆分","drift_rule":"引擎營收占比跨2個年度下降為削弱、跨3個年度為反轉"}],"R":[{"id":"R1","text":"飛機 OEM 減產或去庫存（Boeing 重設、Airbus 爬坡放慢）傳導到 ATI 訂單，HPMC 高度集中航太國防放大衝擊","h_ref":"H1","clock":"⚡","threshold":"機身營收轉為年減，或在手訂單低於40億美元","evidence_refs":["supply_demand_durability#6","customer_concentration_credit#0","cyclical_inventory_price_position#3"]},{"id":"R2","text":"Carpenter、Doncasters、SMP 與 ATI 自身新產能2027下半年至2030投產，交期縮短後續約價格回吐","h_ref":"H2","clock":"🔥","threshold":"優質鈦交期低於12個月，或 AA&S 利益率連兩季低於20%","evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"id":"R3","text":"擴產期存貨與應收墊高，獲利轉現金落後，全年 FCF 指引落空","h_ref":"H1","clock":"⚡","threshold":"FY2026 調整後 FCF 低於5.5億美元"},{"id":"R4","text":"鎳、海綿鈦、鈷等原料多來自地緣不穩國家，中國出口管制與中國合資持股帶來供應與政策風險","h_ref":"H3","clock":"🐢","threshold":"公司揭露原料中斷致單季出貨遞延≥3,000萬美元，或分部利益率受損≥100基點","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","reg_tariff_export#2"]},{"id":"R5","text":"積層製造與複合材料長期替代部分鈦與合金鍛件","h_ref":"H3","clock":"🐢","threshold":"任一引擎 OEM 公開以積層製造取代旋轉件鍛件並進入量產","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"single_thing":{"description":"任一主要引擎 OEM（GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran）在2027–2028長約續約時，把熱段鎳基超合金或等溫鍛件改為雙源，或議定降價","why_fatal":"管理層稱本季增幅約三分之二來自價格與組合，引擎約占全公司營收四成、增量利潤率約50%；價格回吐對 EPS 的衝擊是營收的兩倍以上，共識 FY2027–2028 每年17–23%的 EPS 成長主要靠利益率擴張","if_happens":"基本情境改走空方路徑（FY2028 EPS 由7.2降至5以下），終端倍數下修至16倍；持有則清倉，未持有則撤銷估值重啟條件","how_monitor":"每季法說的續約揭露（Q3 法說稱數份合約即將續約）、優質鈦與等溫鍛件交期、HPMC 利益率、10-K 客戶與競爭揭露","probability":"12–24個月約15%：五種合金獨家供應、認證週期長，但 Carpenter 等新產能2027下半年起投產，提高客戶雙源選項"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":25.75,"peg_fy2":1.28,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":2.85,"FY2026E":5.21,"FY2027E":6.43,"FY2028E":7.52},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 調整後 EPS 共識（2026-10-31 快照，家數事實表未涵蓋）；FY2025A 2.85 為年度 GAAP 稀釋 EPS，調整後口徑事實表未涵蓋，基期與共識口徑不同"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"航太材料認證門檻加交期驅動的定價循環：2020 年 HPMC 航太國防銷售年減55%，2026 年價格與組合貢獻約三分之二增幅"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性偏結構：需求端有新世代引擎含量翻倍、維修與新機各半、Airbus 2025 年底積壓8,754架支撐；供給緊俏屬週期，ATI、Carpenter、Doncasters、SMP 新產能2027下半年至2030投產，可逆性中高","bargaining":{"up":"上游鎳、海綿鈦、鈷、鉻鐵多家供應，但來源含哈薩克、中國、沙烏地等地，中國出口管制可能延誤取得；ATI 已能回收一項難以取得的關鍵原料、支應多數需求","down":"下游為 GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran 與 Boeing、Airbus 等少數大客戶，無單一客戶逾10%；交期20–24個月讓客戶以較高價格與出資擴產換取產能","geo":"生產基地以美國為主，部分原料須進口；2025 年關稅年化曝險約5,000萬美元，經轉嫁與退稅影響極小（2026 年數字事實表未涵蓋）"},"profit_pool_dir":"短期往材料端移動（交期拉長、客戶出資擴產、鉿鋯漲價）；2027末至2030新產能爬坡後可能回流 OEM 與零件端","tam_table":{"expanded":false,"reason":"事實表未收 TAM、滲透率與利潤池歷史；成長以 OEM 產量、單機含量與交期判斷，不靠滲透率承重"}},"moat":{"mechanism":"認證門檻加稀缺產能：熱段六種非自製先進鎳基超合金全部能產、五種獨家，優質鈦與等溫鍛件交期逾20個月，客戶要排隊或出資才拿得到產能","execution":7,"pricing":8,"grade":"B","trend":"↑","trend_evidence":"定價力擴大：管理層稱本季增幅約三分之二來自價格與組合，優質鈦交期20個月、等溫鍛件逾24個月，客戶出資擴產，海軍核能合約以較佳價格續約至2030；執行力持平：新合金9個月完成認證並擴大市占，但墨西哥廠與 Richland 爐認證延宕、新合金爬坡拖累 HPMC 約200基點。對 Carpenter 營益率低6.8個百分點，差距近年是否收窄事實表未涵蓋；定價力有一部分屬供給緊俏的週期成分","threats":[{"level":"🟡","text":"Carpenter 2026 資本支出2.2–2.4億美元投向引擎合金，Athens 擴建約9,000噸與新 VIM 爐 FY2028 前完工，直接增加鎳基合金供給","p":"35%","evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1"]},{"level":"🟡","text":"業界新產能（ATI Monroe 第五座 VIM 爐約9,000噸/年、Doncasters 5,000萬美元超合金廠、SMP 增爐）2027末至2030爬坡，交期縮短將削弱議價","p":"40%","evidence_refs":["cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"積層製造（GKN 與美國空軍 TITAN-AM 專案，840萬美元）與替代材料，目前針對大型鈦機身結構而非熱段旋轉件","p":"10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"peer_na_reason":"同業報酬率比較無法計算：事實表只有利益率，未收投入資本；以營益率差代替","roic_durability":{"quadrant":"中利益率×低周轉（TTM 營益率16.5%；管理營運資金占營收32.9%，重資產熔煉鍛造）；投入資本事實表未涵蓋，ROIC 無法精算","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（航空公司）、決策者（引擎與機身 OEM）、付款者三者皆成立；材料是飛安關鍵件，新機與維修各半，新世代引擎含量為舊引擎兩倍。2020 年航太國防銷售曾年減55%，顯示需求可延後但不會消失"},{"item":"決策層級","level":"🟢","text":"替代要在單一合金、單一零件的認證層級衡量：熱段六種非自製先進合金 ATI 全部能產、其中五種獨家，新合金認證快也要9個月，引擎服役數十年；Boeing 鈦協議非排他是例外"},{"item":"價值鏈分配","level":"🟡","text":"目前交期拉長讓材料端分到較多利潤，客戶甚至出資擴產；但下游 HWM 營益率28.0% 高於 ATI 16.5%，且2027下半年至2030業界新產能投產後，議價可能回到 OEM 端"},{"item":"社會容忍度","level":"🟢","text":"民航與國防材料不受價格管制，漲價由 OEM 與航空公司吸收，政治敏感度低；海軍核能長約屬政府採購，有成本稽核但已以較佳價格續約至2030"}],"roiic":"事實表未涵蓋（投入資本與折舊攤銷未收）；管理層稱新增產能須達內部30%報酬門檻（2026-08-06 法說 CEO），未經驗證","reinvest_rate":"事實表未涵蓋：2026 總資本支出2.8–3.0億美元、客戶出資0.55–0.65億美元，折舊未收，無法求淨再投資","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率，兩項輸入皆缺；以共識 FY2027 EPS +23.4% 遠高於共識營收 +8.8% 判定共識已超出量能驅動的內生上界，差額靠利益率擴張與回購"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","ATI":24.46,"HWM":36.63,"CRS":31.21,"CSTM":16.06,"MTRN":16.01,"unit":"%"},{"metric":"營業利益率","ATI":16.52,"HWM":28.01,"CRS":23.36,"CSTM":8.66,"MTRN":6.35,"unit":"%"},{"metric":"FCF 利潤率","ATI":8.4,"HWM":19.83,"CRS":10.69,"CSTM":3.17,"MTRN":1.55,"unit":"%"},{"metric":"研發密度","ATI":null,"HWM":0.39,"CRS":null,"CSTM":0.53,"MTRN":1.23,"unit":"%"}],"competitors":[{"name":"HWM","gm":36.63,"om":28.01,"fcf_margin":19.83,"rd_intensity":0.39,"strategy_note":"下游鍛鑄件龍頭，TTM 營益率28.0%、FCF 利潤率19.8%，比 ATI 高約11.5個百分點，顯示價值鏈下游零件端拿走較多利潤；同時是鈦合金的直接對手","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CRS","gm":31.21,"om":23.36,"fcf_margin":10.69,"rd_intensity":null,"strategy_note":"鎳基與特殊鋼最直接的對手，TTM 營益率23.4%、高 ATI 6.8個百分點；2026 資本支出2.2–2.4億美元投向引擎合金，Athens 擴建 FY2028 前完工，是2028年後價格壓力的主要來源","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CSTM","gm":16.06,"om":8.66,"fcf_margin":3.17,"rd_intensity":0.53,"strategy_note":"鋁材加工，營益率8.7%，屬不同材料層級，不構成熱段合金替代，只作利益率下緣參照","period":"TTM ending 2026-09-30（4季加總）"},{"name":"MTRN","gm":16.01,"om":6.35,"fcf_margin":1.55,"rd_intensity":1.23,"strategy_note":"特用合金與先進材料，營益率6.4%，與 ATI 核心引擎合金重疊有限","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"價格與組合約三分之二、量約三分之一（Q3 管理層拆解）；噴射引擎年增39%、特殊能源49%、機身11%、國防6%；回購年初至今7,000萬美元，貢獻小；無併購","runway_years":"5–9年（新世代引擎維修週期長達數十年，但滲透率事實表未涵蓋）","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本與折舊事實表未涵蓋，無法算增量報酬×再投資率；共識 FY2026E→FY2028E EPS 年複合約20.1%，同期營收共識 FY1→FY2 僅 +8.8%，差額歸因利益率擴張與小幅回購，可歸因但依賴定價延續","segments":[{"item":"HPMC","value":"Q3 營收7.21億美元，年增20%，利益率23.2%（新合金爬坡拖累約200基點，管理層稱 Q4 回到20%中段）"},{"item":"AA&S","value":"Q3 營收7.02億美元，年增34%，利益率25.8%（年增850基點），航太國防占比45%（2021 年18%）"}],"decay_signals":["EPS 成長高於營收成長逾5個百分點：共識 FY2027 EPS +23.4%、營收 +8.8%，差14.6個百分點（亮）","FCF 對淨利：FY2024 0.46、FY2025 0.83，未連2年低於0.75（未亮）","SBC 約占營收0.6%（未亮）","毛利率 FY2022–2025 由18.6%升至22.0%、TTM 24.5%（未亮）"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產能與定價，非併購；資本回報僅回購（年初至今7,000萬美元）、無股息，規模不承重"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近12個月8-K 未見併購完成，只有小型閒置廠房處分；無可評估的併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"年初至 Q3 回購7,000萬美元，剩餘授權4.25億；回購均價事實表未涵蓋，以現價前瞻盈餘殖利率約3.1%（1÷31.78倍）衡量，門檻為十年期殖利率加2%，只有十年期低於1.1%才過，判為未過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"上半年 SBC 1,410萬美元，約占營收0.6%；年化約2,800萬、占市值約0.1%，同期回購金額大於 SBC，淨稀釋率遠低於1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比：FY2026E 調整後 EPS 共識5.21對現價165.59","peers":{"expanded":false,"reason":"事實表只收同業利益率，未收同業前瞻本益比或 EV 倍數；終端倍數改以 ATI 自身倍數區間與 FY2027E 25.8倍為錨，屬資料缺口"},"fwd_pe":31.78,"peg":1.58,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比31.8倍、FY2027E 25.8倍；追蹤本益比、P/S、EV/S 位於自身四個年度端點98.4–100分位（連續五年序列事實表未涵蓋）；PEG 1.58 屬合理；12個月：FY2028E 基本情境 EPS 7.20×23倍約165.6美元，與現價持平；五年：基本情境8.60×22倍約189美元，+14.3%、年化約3%，低於8%。偏貴但未到極端","upside_short_pct":0.0,"upside_mid_pct":14.3},"trap_analysis":{"verdict":"🟡","label":"週期高點定價風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2020 年 HPMC 航太國防銷售年減55%、Q3 2020 調整後 EBITDA 利益率僅2.8%；Q3 2026 法說分析師點出 Boeing 重設與 Airbus 爬坡放慢；Argus 稱引擎瓶頸正在緩解；HPMC 約92%營收集中航太國防；2025 年機身端去庫存曾拖累鈦銷售","assumption":"飛機產量一路爬升到2028年，長約保護量與價","consequence":"OEM 去庫存疊加2027下半年起新產能，FY2029 EPS 回落到4.3–4.5美元、倍數降至15–16倍，股價約65–75美元，五年虧損逾五成","ruling":"部分採納：長約、國防與核能第二腿、維修過半使2020式崩跌機率低，但週期形狀保留在空方情境30%機率；與唯一致命點部分重疊（需求轉弱會削弱續約議價），已回補到續約監測","watch":"機身營收年增率、在手訂單是否跌破40億美元、HPMC 航太國防銷售年增率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","customer_concentration_credit#0","supply_demand_durability#6","cyclical_inventory_price_position#3"],"fact_refs":["f_kpi5_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年初至 Q3 調整後 FCF 僅2.23億美元，全年指引要 Q4 補3.3–3.8億；管理營運資金占營收32.9%、存貨因新產能暫時偏高；TTM FCF 利潤率8.4%，低於 Carpenter 10.7%、HWM 19.8%；回購在前瞻31.8倍執行，盈餘殖利率約3.1%","assumption":"獲利成長能以90%以上轉為自由現金流（2026-08-06 法說 CFO 承諾）","consequence":"EPS 照共識成長，但擴產資本支出與營運資金吃掉現金，回購買在高價，每股自由現金流成長落後 EPS 數年","ruling":"採納為監測項：Q4 FCF 是第一個裁決點；若未達5.5億，基本情境回購假設歸零","watch":"FY2026 調整後 FCF（2027-02 Q4 財報）、管理營運資金占營收比","fact_refs":["f_kpi3_adjusted_free_cash_flow","f_peer_ati_fcf_margin_pct","f_peer_crs_fcf_margin_pct","f_peer_hwm_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"前瞻本益比31.8倍，追蹤本益比、P/S、EV/S 皆在自身四個年度端點頂部（98.4–100分位）；FY1 共識三個月上修16.8%；賣方幾乎全數買進","assumption":"市場把交期驅動的定價延伸到2028年後，並願意長期給25倍以上","consequence":"即使 FY2027 EPS 6.43 如期達成，倍數回到22倍只值約141美元，較現價低約15%","ruling":"採納，為觀望的主要約束；股價跌到154以下且2027指引確認時重跑","watch":"股價對154美元、FY2027 共識變動、投資人日中期目標","fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2"]}],"max_dd":{"lo":-65,"hi":-40,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 187.98 → 本次 165.59（-11.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=187.98","side_b":"本次 price_at_dd=165.59","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 187.98 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 187.98 美元：Bull 價 348、Bear 價 79.5，五年期望值 +12.4%，基準年化 3.5%，不對稱比 1.2","side_b":"本次情境、股價仍用 187.98 美元：Bull 價 302.4、Bear 價 75.2，五年期望值 −2.5%，基準年化 0.1%，不對稱比 0.85","ruling":"先換情境、股價不動：五年期望值少 14.9 個百分點，基準年化少 3.4 個百分點。不對稱比由 1.2 變為 0.85。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 187.98 美元：五年期望值 −2.5%，基準年化 0.1%，不對稱比 0.85","side_b":"本次情境、股價 165.59 美元：五年期望值 +10.7%，基準年化 2.7%，不對稱比 1.26","ruling":"再換股價、情境不動：起點價下跌 11.9%，五年期望值多 13.2 個百分點，基準年化多 2.6 個百分點，不對稱比由 0.85 升到 1.26。合計五年期望值比前份少 1.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"需求訊號：管理層與 OEM 減速訊號","cause":null,"prior_field":null,"side_a":"Q3 法說（2026-10-29）CEO：看不到去庫存，訂單延伸到2027，引擎 OEM 稱產量加倍也全收；機身營收季增14%","side_b":"同場分析師點出 Boeing 重設、Airbus 爬坡放慢；Argus 稱引擎瓶頸緩解；HPMC 3,000–4,000萬美元遞延出貨 Q3 只出約四分之一；在手訂單由44億降至43億","ruling":"可調和，屬程度差異：ATI 材料提前下單、訂單與 OEM 排程對齊，短期營收有在手訂單支撐；但管理層訊號是自述，利空不到一季且未進賣方模型（FY2027 共識10月仍上修0.63%），凍結加碼到 Q4 財報確認","evidence_level":"中（管理層自述加第三方產業報導，無 OEM 一手數據）","settle_metric":"機身營收年增率、在手訂單","if_then":["若 Q4 2026 或 Q1 2027 機身營收轉年減、或在手訂單跌破40億美元 → 不追，基本情境 FY2027 EPS 下修至6.0以下、空方機率提高到35%","反向：若在手訂單回到44億美元以上且2027指引 EBITDA 中點≥13億美元 → 維持基本情境，股價到154以下時分批反買"],"evidence_refs":["supply_demand_durability#6","cyclical_inventory_price_position#3"]},{"axis":"利益率屬結構還是週期","cause":null,"prior_field":null,"side_a":"Q3 法說 CFO：AA&S 已結構轉型，航太國防占比由2021年18%升至45%，利益率可在20%中段維持到可見未來；長約與海軍核能合約（5年約10億美元）提供底","side_b":"增幅約三分之二來自價格與組合，靠的是優質鈦20個月、等溫鍛件逾24個月的交期；Carpenter Athens 約9,000噸與新 VIM 爐 FY2028 前完工，ATI Monroe 約9,000噸/年、Doncasters、SMP 新產能2027下半年至2030投產；Q2 法說同一場內 CFO 說持續高於20%、CEO 說20%中段，口徑不一","ruling":"可調和，結構與週期成分並存：組合轉向與退出商品不鏽鋼屬結構，AA&S 約20–22%為可守底線（依據：Q2 剔除資產出售利得後底層利益率約22%）；超過的部分視為週期性定價，2028年續約前無法裁決。基本情境假設2029年後利益率回落約2個百分點","evidence_level":"中","settle_metric":"AA&S 分部利益率、優質鈦交期、2027–2028 續約價格","if_then":["若 AA&S 利益率連兩季低於20% → 結構論點失敗，若持有則清倉，未持有則撤銷估值重啟條件","反向：若2028年續約後 AA&S 仍≥22%且優質鈦交期≥12個月 → 結構論點成立，終端倍數由22倍上調至24倍重跑情境"],"evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"axis":"前季承諾與本季兌現","cause":null,"prior_field":null,"side_a":"Q2 法說（2026-08-06）CFO：Q3 EBITDA 3.05–3.15億、Q4 約3.35億、自由現金流轉換率≥90%；CEO：3,000–4,000萬美元 HPMC 出貨移到下半年、引擎全年高十位數成長","side_b":"Q3 實績 EBITDA 3.28億（超過上緣）、Q4 指引上調至3.45–3.55億、引擎成長上調至低至中段20%；但年初至今 FCF 2.23億，全年中點5.75億對應調整後淨利約7.06億（EPS 5.20×1.358億股，未計可轉債稀釋），轉換率約81%；遞延出貨 Q3 只出約四分之一，Richland 高階引擎合金認證延到2027年中","ruling":"可調和，屬時點差異：獲利承諾兌現且超標，現金轉換與產能爬坡落後；以 Q4 FCF 裁決","evidence_level":"高（兩場法說原話與實績）","settle_metric":"FY2026 調整後 FCF","if_then":["若 FY2026 調整後 FCF 低於5.5億美元 → 停止加碼，現金轉換風險視為成立","反向：若≥5.75億美元 → 保留基本情境的回購假設"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"第三次上修、FY2026 EBITDA 年增39%，Q4 EPS 指引年化約6.2美元；股價自前份187.98跌至165.59（−11.9%）而基本面無損，RSI 38.5；FY2027 只要25.8倍；熱段合金五種獨家，引擎 OEM 稱產量加倍也全收","side_b":"跌後倍數仍在自身區間頂部；反推年化8%需要五年 EPS 年複合約16%，等同多方情境；業界新產能2027下半年起投產，循環位置屬中段，持有不加","ruling":"不追。約束是估值：基本情境五年年化約3%，低於8%門檻；跌但基本面無損屬分批反買情境，但價位未到。股價≤154且2027指引 EBITDA 中點≥13億美元時重跑研究","evidence_level":"中","settle_metric":"股價、2027 指引","if_then":["若股價續漲但2027指引尚未公布 → 不追","若股價跌破154而在手訂單與分部利益率無損 → 重跑研究後分批反買，首倉小倉位"]},{"axis":"價格變動後的估值、品質與機率","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-10-13，股價187.98美元）：觀望、追蹤、估值偏貴、品質 B、多方25%、空方30%、最大回撤−65%","side_b":"本次（股價165.59美元，−11.9%）：前瞻本益比31.8倍仍在自身區間頂部，估值偏貴、品質 B 維持；多方25%、空方30%不變；最大回撤區間−40%至−65%","ruling":"跌幅來自價格而非基本面，倍數仍高，估值與品質結論不變；Q3 上修已由基本情境 FY2027 EPS 6.35承接，機率不動","evidence_level":"高（價格與共識皆為事實表數據）","settle_metric":"股價對154美元、FY2027 共識","if_then":["若股價跌至154美元以下且2027指引 EBITDA 中點≥13億美元 → 重跑研究後分批反買","若股價回升至187.98以上而指引未出 → 不追"]},{"axis":"新證據檢視：陷阱、護城河方向、跑道、類型、循環位置","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：陷阱中等、護城河向上、跑道中等、循環/商品、中循環","side_b":"Q3 新證據：定價力續強（三分之二增幅來自價格與組合、新合金市占擴大）、AA&S 創紀錄25.8%；同時 OEM 減速訊號浮現、業界新產能時程確認；各欄結論維持","ruling":"新證據同時強化定價力與確認2027–2030供給回補，兩者相抵，各欄不變；循環位置仍判中段，未到晚期，因 OEM 產量仍低於目標、交期仍在拉長","evidence_level":"中","settle_metric":"交期、分部利益率、在手訂單","if_then":["若優質鈦交期縮短到12個月以下且分部利益率回落 → 循環位置改判晚期，不追","若2027指引確認 EBITDA 成長且交期維持 → 維持中段判斷"]},{"axis":"估值重啟門檻變動（進場首倉條件）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤ 153 美元（FY2027 共識 6.37 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","side_b":"股價 ≤ 154 美元（FY2027 共識 6.43 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","ruling":"方法不變（FY2027 共識24倍），共識由6.37上修至6.43使價位由153調至154；EBITDA 條件不變","evidence_level":"高","settle_metric":"股價、2027 指引","if_then":["兩條件同時成立 → 重跑研究，通過後分批反買"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點欄為空（摘要未保存）","side_b":"任一主要引擎 OEM（GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran）在2027–2028長約續約時，把熱段鎳基超合金或等溫鍛件改為雙源，或議定降價","ruling":"前份未存唯一致命點，本次依數學敏感度最大項新設：價格與組合貢獻約三分之二增幅，續約降價或雙源是單一最大衝擊，發生即清倉","evidence_level":"中","settle_metric":"續約揭露、交期","if_then":["若任一主要引擎客戶公開雙源化或續約降價 → 清倉（若持有），未持有則撤銷估值重啟條件"]},{"axis":"清倉與減碼門檻新設","cause":"方法變動","prior_field":["kill_metrics","triggers"],"side_a":"前份清倉與減碼門檻、觸發器皆為空（摘要未保存）","side_b":"AA&S 利益率連兩季<20%；在手訂單<40億美元；FY2026 調整後 FCF<5.5億美元；HPMC 利益率 Q4 2026 與 Q1 2027 皆<24%；優質鈦交期<12個月","ruling":"前份摘要未保存門檻，本次依論點與風險逐條新設，各自對應減碼或清倉動作","evidence_level":"中","settle_metric":"每季分部資料與法說","if_then":["AA&S 利益率連兩季<20% → 清倉（若持有）","在手訂單<40億美元或優質鈦交期<12個月 → 減碼（若持有）"]}],"triggers":[{"n":1,"text":"估值重啟：股價回到 FY2027 共識24倍以下，且2027指引確認 EBITDA 成長","type":"估值rearm","maps_to":"H1","metric":"股價；2027 年指引調整後 EBITDA 中點","threshold":"股價≤154美元且 EBITDA 中點≥13億美元同時成立","action":"重跑研究，通過後分批反買、首倉小倉位","source_freq":"每日股價；2027-02 Q4 財報","date":"2027-02-01"},{"n":2,"text":"投資人日公布3–5年展望，驗證引擎成長與利益率目標","type":"假設驗證","maps_to":"H1","metric":"引擎營收成長目標、合併 EBITDA 利益率目標","threshold":"引擎營收年成長目標≥15%且利益率目標≥20%中段","action":"未達則基本情境 FY2028 EPS 下修至7.0以下並不追","source_freq":"一次性","date":"2026-11-12"},{"n":3,"text":"OEM 減產或去庫存傳導到訂單","type":"風險","maps_to":"R1","metric":"機身營收年增率、在手訂單","threshold":"機身營收轉年減，或在手訂單<40億美元","action":"不追；若持有則減碼","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#6","customer_concentration_credit#0","cyclical_inventory_price_position#3"]},{"n":4,"text":"業界新產能投產後定價回吐","type":"風險","maps_to":"R2","metric":"優質鈦交期、AA&S 分部利益率","threshold":"優質鈦交期<12個月，或 AA&S 利益率連兩季<20%","action":"若持有則減碼，利益率條件成立則清倉","source_freq":"每季法說與財報","date":null,"evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"n":5,"text":"擴產期獲利轉現金落後","type":"風險","maps_to":"R3","metric":"FY2026 調整後 FCF","threshold":"<5.5億美元","action":"停止加碼","source_freq":"Q4 2026 財報","date":"2027-02-01"},{"n":6,"text":"新合金爬坡成本是否如管理層所說為一次性（未證、監測）","type":"假設驗證","maps_to":"H2","metric":"HPMC 分部利益率","threshold":"Q4 2026 與 Q1 2027 皆<24%，則一次性歸因不成立","action":"不追，基本情境利益率下修","source_freq":"每季財報","date":"2027-05-01"},{"n":7,"text":"原料地緣供應中斷或中國出口管制吃掉利潤","type":"風險","maps_to":"R4","metric":"出貨遞延金額、分部利益率","threshold":"單季出貨遞延≥3,000萬美元，或分部利益率受損≥100基點","action":"若持有則減碼","source_freq":"每季法說、10-K 風險因子","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","reg_tariff_export#2"]},{"n":8,"text":"積層製造進入引擎旋轉件量產","type":"風險","maps_to":"R5","metric":"OEM 量產公告","threshold":"任一引擎 OEM 公開以積層製造取代旋轉件鍛件並量產","action":"若持有則減碼","source_freq":"產業新聞、OEM 公告","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":9,"text":"退休金年金集體訴訟：民事集體案，公司無法估計損失；magistrate 法官已建議以無訴訟資格駁回，待主審法官裁定","type":"風險","maps_to":null,"metric":"主審法官裁定、集體認證","threshold":"駁回建議遭推翻且集體認證成立","action":"停止加碼；不利和解金額超過年度 FCF 一成則減碼","source_freq":"10-Q 與10-K 法律程序","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":10,"text":"Single Thing：主要引擎 OEM 續約改雙源或議定降價","type":"Single Thing","maps_to":"Single Thing","metric":"續約揭露、熱段合金供應地位","threshold":"任一主要引擎客戶公開雙源化或續約降價","action":"清倉（若持有），未持有則撤銷估值重啟條件","source_freq":"每季法說、10-K","date":null},{"n":11,"text":"Q4 2026 財報複審","type":"複審日期","maps_to":null,"metric":"2027 指引、FY2026 FCF、在手訂單","threshold":"依前列各門檻","action":"重跑情境","source_freq":"一次性","date":"2027-02-01"}],"kill_metrics":[{"metric":"AA&S 分部 EBITDA 利益率","bear_threshold":"連兩季<20%","window":"2027–2028 每季","source":"公司季報新聞稿分部資料","last_status":"ok"},{"metric":"在手訂單","bear_threshold":"<40億美元或轉為年減","window":"每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"FY2026 調整後自由現金流","bear_threshold":"<5.5億美元","window":"2027-02 Q4 財報","source":"Q4 2026 新聞稿","last_status":"unknown"},{"metric":"HPMC 分部利益率","bear_threshold":"Q4 2026 與 Q1 2027 皆<24%","window":"2027-02 至 2027-05","source":"公司季報分部資料","last_status":"warning"},{"metric":"優質鈦交期","bear_threshold":"<12個月","window":"每季法說","source":"法說會管理層口述","last_status":"ok"}],"evidence_dismissed":[{"ref":"substitute_technology#2","reason":"來源是投資人社群自撰敘事，非公司揭露也非分析師研究，未附替代比例、平台或時程等可驗證數據；替代風險改由10-K 風險因子與 GKN TITAN-AM 專案兩條一手證據承接"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=6.65, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"≤3%（最大回撤可能逾五成的循環股）","requires_critic":[],"rearm_trigger":"股價 ≤ 154 美元（FY2027 共識 6.43 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","exec_line":"不追；兩條件同時成立才重跑研究，通過後首倉小倉位、分兩批；續漲而2027指引未出則不追"},"reasoning":{"industry":"賺誰的錢：引擎與機身 OEM、國防與核能客戶。Q3（10-Q 與2026-10-29 法說）營收14.2億美元、年增26%，航太國防近七成；噴射引擎年增39%、約占全公司四成，新機與維修各半，且同件同價同利。分部：HPMC 7.21億美元（年增20%，利益率23.2%），AA&S 7.02億美元（年增34%，利益率25.8%）。TTM 毛利率24.5%、營益率16.5%；Q2 單季 GAAP 營業利益2.2億美元。錢卡在經過認證的熔煉與鍛造產能：優質鈦交期20個月、等溫鍛件逾24個月，管理層稱本季增幅約三分之二來自價格與組合。產業時鐘判擴張期：OEM 產量仍低於目標（A320 月產75架延至2027年）、交期拉長、新產能2027下半年才投產，尚未見供給過剩。供需持久性：需求端偏結構（新世代引擎含量為舊引擎兩倍以上），供給緊俏屬週期性、可逆性中高。單點依賴：HPMC 約92%營收來自航太國防，客戶為少數引擎與機身 OEM，但無單一客戶超過10%。產業態勢雙向拉鋸：競爭面 Carpenter、Doncasters、SMP 與 ATI 自身新產能陸續投產，結構面有長約、客戶出資擴產與 AA&S 組合轉向，其他變數為中國出口管制推升鉿鋯價格。","moat":"機制是認證門檻加稀缺產能：熱段六種非自製先進鎳基超合金 ATI 全部能產，其中五種獨家供應，今年新合金9個月完成認證並成為全球兩家之一（Q3 法說）；鉿鋯為西方三家合格廠之一（Q2 法說）。同業報酬率差無法取得，改用定價軸：交期拉長、長約重新定價、客戶出資擴產，定價力擴大；執行力持平，墨西哥廠與 Richland 爐認證延宕、新合金爬坡拖累 HPMC 約200基點。TTM 營益率 ATI 16.5%，低於 Carpenter 23.4%、HWM 28.0%，利益率差為負，評分封頂在 B。威脅都屬點對點：Carpenter 擴產、業界2027–2030新產能、積層製造。持續期四檢查點三綠一黃，弱點在價值鏈分配；增量報酬無法計算，管理層宣稱的30%報酬門檻未經驗證。","growth":"成長是價格加量，無併購、回購貢獻小。共識 FY2026E 5.21、FY2027E 6.43、FY2028E 7.52，兩年年複合約20.1%，FY1 共識近三個月上修16.8%；同期營收共識 FY1→FY2 僅成長8.8%，EPS 與營收差14.6個百分點，缺口歸因利益率擴張（全年增量利潤率約50%）與小幅回購，可歸因但依賴定價延續。內生上界因投入資本與折舊未收無法計算，判定共識已超出量能驅動的上界。跑道：新世代引擎維修週期長達數十年、鎳擴產2028年中約3.5億美元增量營收、飛彈與核能為第二腿，但滲透率事實表未涵蓋；業界新產能2027下半年至2030投產後成長將轉向以量為主，五年後判中等。衰退信號亮一項。","governance":"自由現金流轉換在改善但仍落後：FY2023 FCF 為負、FY2024 FCF 對淨利0.46、FY2025 0.83；2026 年初至 Q3 調整後 FCF 2.23億美元，全年指引5.5–6.0億要靠 Q4 約3.3–3.8億。TTM FCF 利潤率8.4%，低於 Carpenter 10.7%、HWM 19.8%。現金去向：資本支出全年2.8–3.0億（客戶出資0.55–0.65億）、回購年初至今0.7億（剩餘授權4.25億）、無股息、無併購；2026-06 發行4.5億美元5.875%、2033年到期無擔保債。淨負債14.15億美元，約為2026年 EBITDA 指引中點的1.2倍。SBC 約占營收0.6%。債務到期結構與加權利率事實表未涵蓋。","valuation":"現價165.59美元對 FY2026E 前瞻本益比31.8倍、FY2027E 25.8倍、FY2028E 22.0倍；追蹤本益比41.4倍、P/S 4.49倍、EV/S 4.77倍，分別位於自身四個年度端點的98.4、100、100分位（非五年分位）。反推：要拿到年化8%，2031年需 EPS 約11.1美元配22倍，五年年複合約16%，等同多方情境。PEG 以兩年共識年複合20.1%計約1.58，屬合理。賣方目標價多在175–265美元（Investing.com 9位全數買進，均值約200），Benzinga 來源全距逾3倍但含過時目標；本次結論比賣方保守，分歧在框架：賣方把交期驅動的定價延伸到2028年後並沿用目前倍數。動能：26週報酬6.7%、RSI 38.5，未過熱；週線均線多頭排列。","premortem":"最可能看錯的三條路寫在反證紀錄：OEM 去庫存疊加新產能讓定價回吐（論點失敗）、獲利成長但現金轉換與回購價位拖累股東報酬、倍數已反映長期定價。衰退信號亮一項，價值陷阱風險中等；最大回撤區間−40%至−65%，論點未見破損，不因波動砍倉，但要有深回撤心理準備。"},"plain":{"six":{"how_it_makes_money":"賺航太引擎與機身 OEM、國防與核能客戶的錢；錢卡在經過認證的熔煉與鍛造產能，ATI 靠熱段合金獨家或雙源供應拿到定價權，產業處擴張期","moat":"護城河向上、等級 B：認證門檻與稀缺產能讓定價權擴大，但利益率仍低於 Carpenter 與 HWM，部分定價屬週期性緊俏","growth":"跑道中等：兩年內靠新世代引擎含量翻倍與長約重新定價，五年後取決於2027–2030業界新產能投產後價格能否守住","capital":"資本配置中等：獲利轉現金仍在追趕、回購規模小且買在高倍數，SBC 稀釋輕微、無併購","valuation":"偏貴：現價要五年 EPS 年複合約16%並守住22倍才有8%年報酬，等同多方情境；我們信未來兩年獲利，不信2028年後定價與倍數同時守住","how_wrong":"陷阱風險中等：最怕的不是需求消失，而是新產能投產後定價回吐，讓高倍數失去支撐"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"追蹤","wait_for_price":true,"wait_for_price_condition":"股價≤154美元（FY2027 共識6.43的24倍）且2027年指引調整後 EBITDA 中點≥13億美元，兩者同時成立後重跑研究","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":165.59,"week26_return_pct":6.65,"consensus_rev_3m_pct":16.82,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母為調整後 EPS，Q3 含新合金爬坡成本（約1,500–2,000萬美元 EBITDA）屬暫時性壓低；週期高點疑慮由空方情境30%承接，不判分母爭議"},"catalysts":[{"date":"2026-11-12","type":"guidance","event":"投資人日：公布3–5年展望（引擎成長、資本支出與利益率目標）","impact":"高","watch":"引擎營收成長目標是否≥15%、利益率目標是否在20%中段以上"},{"date":"2027-02-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與2027年指引","impact":"高","watch":"2027 調整後 EBITDA 中點是否≥13億美元；FY2026 FCF 是否≥5.5億美元"},{"date":"2027-06-30","date_precision":"quarter","type":"capacity","event":"Richland EB2 爐高階引擎鈦合金完成認證","impact":"中","watch":"認證是否如期於2027年中完成"},{"date":"2027-12-31","date_precision":"quarter","type":"capacity","event":"Monroe 新 VIM 爐上線（2028年中約3.5億美元鎳增量營收）；同期 Carpenter Athens 擴建完工","impact":"中","watch":"交期與續約價格是否鬆動"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s4`：現在 1,430B，下限 1,500B，**目標 ≥ 1,800B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s4 -->
<section id="s4"><h2>4　品質門檻</h2>
<p class="lead">品質評為 B：護城河向上，但現金轉換與資本配置仍在追趕。</p>
<ul class="pts">
<li>護城河等級 B，趨勢向上，綜合分數 7.5。執行力 7、定價力 8。定價力是強項，執行力因墨西哥廠與 Richland 爐的認證延宕而持平。新合金爬坡拖累 HPMC 利益率約 200 基點。</li>
<li>現金轉換是主要弱點。FCF 對淨利比 FY2023 為負，FY2024 為 0.46，FY2025 為 0.83，方向改善但仍落後。2026 年初至 Q3 調整後 FCF 只有 2.23 億美元，全年指引 5.5 至 6.0 億，要靠 Q4 補 3.3 至 3.8 億美元。</li>
<li>資本配置評 B。公司成長來自自有產能與定價，沒有併購可評。回購年初至今 7,000 萬美元，剩餘授權 4.25 億。以前瞻盈餘殖利率約 3.1% 衡量，回購沒有通過門檻。股票酬勞約占營收 0.6%，稀釋輕微，這項通過。</li>
<li>資產負債表可接受。淨負債 14.15 億美元，約為 2026 年 EBITDA 指引中點的 1.2 倍。2026 年 6 月發行 4.5 億美元 5.875% 的 2033 年到期無擔保債。債務到期結構與加權利率事實表未涵蓋。</li>
<li>跑道與陷阱各評中等。成長跑道 5 至 9 年，五年後因新產能而判黃燈。陷阱判為週期高點定價風險。衰退信號四項只亮一項：共識 EPS 成長高於營收成長逾 5 個百分點。</li>
</ul></section>

```