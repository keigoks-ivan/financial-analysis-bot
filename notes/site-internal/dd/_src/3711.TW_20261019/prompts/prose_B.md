你是 stock-analyst v20 的**散文層（prose）agent**，標的 3711.TW（2026-10-19）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261019/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：3711.TW　日期：2026-10-19　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1461B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（397B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1010B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1234B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1403B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（517B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（741B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2019B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3373B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2275B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1461           3877-5539      5 條（2–6 內）  
s3                  8000         397           5322-7603      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3647          7947-11353      5 條（2–6 內）  
s6                 11000         517          7338-10483      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         741           1931-2759      5 條（2–6 內）  
s10                 5000        2019           2087-2981      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2275           2000-2725      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4822B；至少需散文≈40.18KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−328
−236
−60%
−60
−53%
−48%
−45
−45%
−32%
−6.15%
−6%
−6
0
0.28
0.4
0.42
0.75
0.98
1
1%
1.1
1.14
02
2%
2
2.4
2.4%
03
3%
3
3.7%
3.8%
4
4%
04
4.14
4.41
4.61
4.80
5
5%
5.4
6
7
7%
07
7.18
8
8.0%
8.1%
8.6%
8.89
8.9%
9
9.3%
9.89%
9.9%
10%
10
11%
11.1%
11.4
11.5%
12%
12
12.5%
12.9%
13
13%
13.81
14
14.8%
15
15.5%
15.7%
15.8%
17
18
18%
18.83
19
19%
19.5%
20%
20
20.1%
21.0%
21
21%
22
22%
22.9
22.93
23
24
24%
25
25%
25.2%
26%
26
26.6%
26.9%
27%
27.3%
28%
28.5
29
29%
29.22
29.5%
30%
30
30.5
31
31.9
32.5
35%
35
35.58
35.6
37
37.5
40%
40
42
43
44%
45
46
46.5%
46.51
47%
48%
49
51
55
57
60%
61%
65
66%
70
70%
75%
80%
81%
85%
87%
90
91
94%
100%
100
105
150%
211
247
250
285%
300
310
324
400
457
458
470
500
600
627
658
670
670.0
675
685
798
828
835
880
990
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
2449
3711
6239
20261019
1,261
1,901
1,911
1,988
2,360
29,464
3,350
3,962
4,230
6,220
7,117
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
{"meta":{"ticker":"3711.TW","date":"2026-10-19","schema":"v15.2","contract":"v19","company_name":"日月光投控"},"oneliner":"AI 先進封裝供不應求，封測毛利率可望突破 30%，但 670 元已貼近法人目標價下緣，按 2027 年尖峰獲利仍要 23 倍；勝負在 2028 年產能大增後的稼動率，等回到約 500 元或毛利證明是結構性再談。","thesis":{"H":[{"id":"H1","text":"AI 先進封裝帶動封測毛利率突破過去 26%～30% 的結構區間，並在 2027 年守住。","2y":"4Q26 封測毛利率 ≥29.5%，2027 年四季平均 ≥28%","5y":null,"10y":null,"threshold":"2027 年封測毛利率四季平均 ≥28%","source":"公司季度法說簡報封測損益頁","drift_rule":"實際值連兩季低於門檻 5% 以上（約 26.6%）＝削弱；連三季低於 10% 以上（約 25.2%）＝反轉"},{"id":"H2","text":"2027 年 LEAP 營收倍增，新廠與設備如期開出。","2y":"2027 年 LEAP 營收約 70 億美元以上（以 2026 年超過 35 億美元為基）","5y":null,"10y":null,"threshold":"2027 年 LEAP 營收 ≥70 億美元","source":"公司季度法說指引與年度實際","drift_rule":"季度進度連兩季落後倍增路徑 5% 以上＝削弱；連三季落後 10% 以上或指引下修＝反轉"},{"id":"H3","text":"資本支出高峰過後，新產能報酬足以讓自由現金流轉正、投入資本報酬率維持在 10% 以上。","2y":null,"5y":"2028 年全年自由現金流轉正，淨負債÷權益 ≤60%，投入資本報酬率 ≥10%","10y":null,"threshold":"2028 年自由現金流 >0 且淨負債÷權益 ≤60%","source":"年報現金流量表與季報資產負債表","drift_rule":"淨負債÷權益連四季高於路徑 5% 以上＝削弱；連六季高於 10% 以上＝反轉"}],"R":[{"id":"R1","text":"2028 年起 OSAT 端先進封裝產能大增，若碰上 AI 資本支出消化，稼動率與毛利率重演 2023 年下行，且折舊基數更大。","h_ref":"H1","clock":"🔥","threshold":"混合稼動率 <75% 或封測毛利率連兩季 <25%","evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R2","text":"Amkor 取得 NVIDIA 美國多年期合作、Intel EMIB 積壓訂單增加，而公司採台灣優先；客戶在地化與關稅分攤可能分走新增訂單或壓低傳統封測價格。","h_ref":"H2","clock":"🔥","threshold":"前五大客戶占比單季下降 ≥3 個百分點，或 2027 年 LEAP 指引下修","evidence_refs":["competitive_share_entrants#3","geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R3","text":"資本強度失控：資本支出再上修、自由現金流負值延長，淨負債持續累積。","h_ref":"H3","clock":"🐢","threshold":"淨負債÷權益 >80%","evidence_refs":[]},{"id":"R4","text":"關鍵材料由少數供應商主導、替代產能有限，任一斷供即無法出貨。","h_ref":"H2","clock":"⚡","threshold":"單季營收因材料短缺低於指引下緣","evidence_refs":["geo_supply_chain#3"]}],"single_thing":{"description":"主要晶圓代工夥伴或最大 AI 客戶削減委外，公司明確下修 2027 年 LEAP 倍增指引。","why_fatal":"2026 年 105 億美元資本支出中約七成設備投向 LEAP；倍增落空時新增折舊落在空產能上，封測毛利率回到 24%～26%，2027 年 EPS 由共識 29 元降到約 22 元，同時倍數收縮，是 Base 終端 EPS 最大的單一敏感項。","if_happens":"已持有者清倉；未持有者不碰，等稼動率回到 80% 以上再重跑研究。","how_monitor":"每季法說的 LEAP 指引、主要晶圓代工夥伴對委外的說法、月營收年增率。","probability":"約 20%：管理層稱需求不是問題、限制在執行，但 2028 年 OSAT 端產能預估大增，客戶自做與替代技術也在推進。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.93,"peg_fy2":0.42,"stress":{"pass":8,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":8.89,"FY2026E":18.83,"FY2027E":29.22,"FY2028E":null},"fy_end_month":12,"eps_basis":"基期為年報稀釋 EPS；共識為 yfinance 分析師平均，未註明基本或稀釋；FY2028E 事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261019/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"資本支出建設型循環：資本支出約為折舊三倍、稼動率近滿、毛利率位於自身區間上緣；另有 LEAP 先進封測屬長期成長部分"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高：需求到 2027 年能見度高（管理層稱需求不是問題、限制在執行），但公司同時進行約 20 個廠房工程，且法人估 OSAT 端 CoWoS 類產能 2027 年底較 2026 年底大幅增加，2028 年後供給可能追上需求。","bargaining":{"up":"關鍵材料（基板、特殊氣體）由少數供應商主導，部分握有全球八、九成市占，上游議價偏弱。","down":"前五大客戶占 44%、單一客戶逾一成；目前供不應求，管理層稱材料成本可完全轉嫁，下游議價暫時偏強，但屬週期性。","geo":"產能以台灣為主，美國只有研發、測試開發與小型廠；同業 Amkor 已擴大美國產能，客戶在地化要求升高。"},"profit_pool_dir":"利潤池小幅由晶圓代工往封裝端移動（封裝往系統架構上移），但最難取代的前段仍在晶圓代工夥伴手上。","tam_table":{"expanded":false,"reason":"事實表未涵蓋先進封裝 TAM、滲透率與利潤池占比的歷史數字；屬承重項但證據包沒有，標為資料缺口。"}},"moat":{"mechanism":"規模與台灣群聚＋全自動產線＋與主要晶圓代工夥伴的委外分工位置；純封測代工不與生態系任何一方競爭，累積多年認證與客戶信任。","execution":8,"pricing":6,"grade":"B","trend":"↑","trend_evidence":"封測毛利率 2Q25→2Q26 上升 5.4 個百分點、封測占營業利益 87%→94%；TTM 毛利率與營業利益率皆高於 Amkor；但價格面改善部分來自供不應求，尚未經過下行循環檢驗。","threats":[{"level":"🟡","text":"Amkor 2Q26 營收年增 26%，並與 NVIDIA 簽美國多年期 15 億美元封測合作，美國在地產能可能分走最大客戶的新增訂單。","p":30,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"Intel EMIB-T 高階封裝積壓訂單增加，晶圓代工加封裝一條龍可能分流部分 AI 封裝需求；管理層稱也在配合 EMIB，非零和。","p":25,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"客戶在地化：公司採台灣優先，美國只有研發與測試廠；分析師預期傳統封測可能被要求降價分攤客戶關稅成本。","p":25,"evidence_refs":["geo_supply_chain#2","reg_tariff_export#0"]},{"level":"🟡","text":"關鍵材料由少數供應商主導、替代產能有限，任一供應商出問題封裝端可能無法出貨。","p":15,"evidence_refs":["geo_supply_chain#3"]}],"roic_durability":{"quadrant":"低利益率×低周轉（當期投入資本報酬率約 9.3%，貼近資金成本上緣）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是晶片設計公司、付款最終來自雲端業者的 AI 資本支出；客戶目前要的是產能而非價格，需求急迫，但持久性取決於 AI 資本支出週期，管理層自己也把它分成技術十五到二十年、生意約四季的能見度。"},{"item":"決策層級","level":"🟡","text":"替代性要看單一產品的封裝認證：換封測廠要重新認證，先行者有優勢；但客戶已同時下單 Amkor，Intel EMIB 也在爭取，最小決策單位上已有兩到三家可選。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈裡最難取代的是晶圓代工前段，封測拿到的是代工夥伴分出來的部分；管理層稱封裝正往系統架構上移，但結構毛利上限 30% 仍遠低於晶圓代工，分配位置在改善但仍居次。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的中間服務，終端消費者看不到封測價格，沒有社會面的漲價天花板；政策面的壓力來自地緣政治與在地化要求，已列入威脅。"}],"roiic":"前瞻隱含約 19%（2027 共識淨利增量約 457 億元 ÷ 2026 年淨資本支出約 2,360 億元）；已實現值事實表未涵蓋；跨循環取 12%","reinvest_rate":"約 285%（2026 年資本支出 105 億美元×31.9 ≈ 3,350 億元，減年化折舊約 990 億元，除以 2026 共識淨利約 828 億元）；超過 100% 的部分靠借款","endo_ceiling":12,"formula_note":"當期報酬：TTM 營業利益率 9.89%×(1−18% 稅率) ≈ 8.1%；投入資本 ≈ 淨負債 1,988 億元＋權益約 4,230 億元（淨負債÷權益 47% 反推，2Q26 法說資產負債頁）≈ 6,220 億元；TTM 營收 ≈ 市值 29,464 億元 ÷ P/S 4.14 ≈ 7,117 億元，周轉 1.14 倍，報酬率約 9.3%。折舊以 2Q26 EBITDA 458 億元減營業利益 211 億元約 247 億元／季推估。內生成長＝增量報酬 12%×自有資金再投資率上限 100%＝12%；借款支應可暫時拉到約 24%，不屬內生。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","3711.TW":19.49,"AMKR":15.51,"6239.TW":19.12,"2449.TW":38.31,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","3711.TW":9.89,"AMKR":8.64,"6239.TW":12.9,"2449.TW":26.86,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","3711.TW":-6.15,"AMKR":-2.31,"6239.TW":-9.7,"2449.TW":-32.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","3711.TW":5.16,"AMKR":2.15,"6239.TW":3.84,"2449.TW":2.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"AMKR","gm":15.51,"om":8.64,"fcf_margin":-2.31,"rd_intensity":2.15,"strategy_note":"毛利率與營業利益率皆低於日月光，但拿到 NVIDIA 美國多年期 15 億美元合作，是在地化產能這條路上的主要對手。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"6239.TW","gm":19.12,"om":12.9,"fcf_margin":-9.7,"rd_intensity":3.84,"strategy_note":"力成營業利益率 12.9% 高於日月光合併數字，但以記憶體封測為主，與日月光的 AI 邏輯先進封裝重疊有限。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"2449.TW","gm":38.31,"om":26.86,"fcf_margin":-32.27,"rd_intensity":2.7,"strategy_note":"京元電是測試專業廠，營業利益率 26.9% 最高，但 FCF 利潤率 -32% 顯示擴產最激進，AI 測試訂單上是直接對手。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（新產能）＋價（漲價與轉嫁）＋組合（LEAP 占比上升）；無併購、無回購","runway_years":"事實表未涵蓋滲透率序列；先進封裝約占封測營收 48%（2025 年第三季），已過三成","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬跨循環取 12%（前瞻共識隱含約 19% 打折、當期約 9.3%）×自有資金再投資率上限 100%；共識兩年 EPS 年化約 81%，遠超天花板，缺口歸因利潤率擴張。","segments":[{"item":"封測（ATM）","value":"2Q26 營收 1,261 億元（含內部交易）、毛利率 27.3%、營業利益率 15.7%；2026 年美元營收預估年增約 35%"},{"item":"其中 LEAP 先進封測","value":"2026 年高於 35 億美元、2027 年目標倍增；約七成設備資本支出投入此處"},{"item":"EMS 電子代工","value":"2Q26 營收 658 億元、毛利率 8.9%、營業利益率 2.4%；2026 全年成長低於 20%"}],"decay_signals":["亮：EPS 成長遠高於營收成長（2026 共識 EPS 年增約一倍、營收約三成）","亮：自由現金流÷淨利連兩年低於 0.75（2024 年約 0.28、2025 年為負）","未亮：毛利率連兩季年減、核心市占縮減、提價後銷量下滑、替代技術壓縮市場、產業倍數系統性下移、停止投資新產能"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能與購入既有廠房，不是靠併購撐；無回購，股東回報只有約 1% 股息，無須展開。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近期無超過市值 5% 的併購；擴產以自建與購入既有廠房為主，金額事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"未見回購；股息殖利率約 1%","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"事實表未涵蓋員工股票酬勞；2Q26 稀釋 EPS 4.61 元對基本 EPS 4.80 元，差約 4%，來源未拆分","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY1／FY2 共識 EPS）","tier":"台灣大型封測（對照 Amkor、力成、京元電）","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比與目標價，無法做倍數對照。"},"fwd_pe":35.58,"peg":2.4,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻一年 35.6 倍、2027 共識 22.9 倍；trailing 本益比、股價營收比、EV/S 皆為近四個年度端點最高（只有四點，非五年分位，故五年分位留空）；PEG 以 Base 情境 2026→2031 年 EPS 年化約 14.8% 計為 2.4，若用共識兩年 81% 計只有 0.4，但後者來自循環底部基期與利潤率擴張，不採用；Base 五年目標約 675 元，上檔幾乎為零。","upside_short_pct":-6,"upside_mid_pct":1},"trap_analysis":{"verdict":"🟡","label":"獲利率在循環高點、自由現金流為負，倍數按尖峰獲利仍偏高"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2023 年下行時營收年減 13%、毛利率由 20.1% 跌到 15.8%、EPS 腰斬；法人估日月光 CoWoS 類月產能 2027 年底是 2026 年底的數倍，公司另有約 15 個新廠為 2029～2030 年需求準備。","assumption":"AI 先進封裝需求在 2028 年後仍能吸收全部新增產能。","consequence":"若需求消化，稼動率跌破 75%，更大的折舊基數讓毛利率掉得比 2023 年更深，EPS 回到約 18～20 元、倍數 13 倍，股價約 250～300 元。","ruling":"採納：作為 Bear 情境，機率 30%；管理層自己說產能工程足以撐到 2028～2029 年，代表產能是按需求高峰在蓋。","watch":"混合稼動率、封測毛利率、月營收年增率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#1"],"fact_refs":["f_kpi1","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流 2025 年 -236 億元、2Q26 單季 -328 億元，財務長說負現金流會持續一段時間；公司採台灣優先，客戶在地化壓力升高，分析師預期傳統封測可能被要求分攤關稅。","assumption":"LEAP 倍增帶來的利潤足以覆蓋 105 億美元級的年度資本支出，並在 2028 年轉正。","consequence":"營收與 EPS 都達標，但現金被持續擴產與海外高成本產能吃掉，淨負債上升、股東拿到的現金報酬很少，倍數難以維持。","ruling":"部分採納：短期資金無虞（未動用額度 3,962 億元），但把 2028 年自由現金流轉正列為 H3 的驗證點。","watch":"淨負債÷權益、2027 年資本支出指引、美國產能規劃","evidence_refs":["geo_supply_chain#2","reg_tariff_export#0"],"fact_refs":["f_kpi4","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"現價 670 元，前瞻一年 35.6 倍、2027 共識 22.9 倍，trailing 倍數在近四個年度端點最高；法人目標價 685～835 元，26 週已漲 46.5%。","assumption":"市場會持續用成長股倍數看待一個循環高點的封測廠。","consequence":"即使 2027 年達標，只要市場開始按 2028 年正常化獲利定價，股價就沒有上檔。","ruling":"採納：Base 五年上檔約 1%，不追，等價格或毛利證據擇一先到。","watch":"股價對 2027 共識 EPS 的倍數、法人目標價調整方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"],"fact_refs":["f_pe_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy2"]}],"max_dd":{"lo":-60,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 670.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=670.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率是結構性還是週期性","cause":null,"prior_field":null,"side_a":"管理層：第四季封測毛利率很可能突破 30% 結構上限，將檢討上調結構區間，材料成本可完全轉嫁（2026-07-30 財務長董宏思）。","side_b":"2023 年下行時合併毛利率由 20.1% 跌到 15.8%；本輪 OSAT 端先進封裝產能 2027 年底預估大增，新增折舊大量進場，管理層也承認近期成長受限於產能而非需求。","ruling":"不可調和（方向相反）。估值採 B 側：終端倍數用 18 倍，Bear 機率 30%；依據是毛利改善有相當部分來自稼動率與供不應求，這部分在下行時會回吐，管理層的結構區間至今只經過上行期。","evidence_level":"管理層指引＋歷史年報＋法人產能估計","settle_metric":"2027 年四季封測毛利率與混合稼動率","if_then":["若 4Q26 封測毛利率 ≥30%，且 2027 年稼動率回落到 80% 以下時毛利率仍 ≥28%，則 Base 終端倍數上調到 21 倍重算，股價 ≤600 元時建立 2% 首倉","反向：若封測毛利率連兩季 <26%，則維持不碰、Bear 機率升到 40%，已持有者減碼一半"],"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_supply_discipline_capacity#3","end_markets#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"報導稱第三季營收優於指引，2027 年 LEAP 倍增有產能與客戶能見度，毛利率可能再上修；按 2027 共識只要 23 倍，RSI 46 不過熱，法人目標價最高 835 元。","side_b":"670 元已在法人目標價區間下緣附近；前瞻一年 35.6 倍、尖峰獲利 23 倍；自由現金流為負、淨負債上升；26 週已漲 46.5%。","ruling":"可調和（程度差異）：生意變好是真的，但價格已先反映 2027 年；不追，等價格或毛利證據擇一先到。","evidence_level":"二手報導＋法人報告摘要＋事實表估值","settle_metric":"股價對 2027 共識 EPS 倍數、4Q26 封測毛利率","if_then":["若股價續漲而 2027 LEAP 指引與毛利率證據未上修，則不追","若股價跌到 500 元以下而封測毛利率仍 ≥27%、LEAP 指引未下修，則重跑研究後分批反買"],"evidence_refs":["cyclical_inventory_price_position#1","capital_markets_pricing#0","capital_markets_pricing#2"]},{"axis":"管理層前後說法對照","cause":null,"prior_field":null,"side_a":"2026-04-29 財務長：一般業務成長約 13%、暫不調結構毛利區間要等明年；折舊對毛利的稀釋下季可能量化；不排除再上調資本支出。","side_b":"2026-07-30：一般業務上修到約 20%，第四季就要檢討上調結構區間，資本支出再加 20 億美元到 105 億美元；折舊稀釋仍未量化，2027 年資本支出規模拒答。","ruling":"可調和：營運數字兌現且優於前一季說法，可信度加分；但折舊量化承諾未兌現、2027 年資本支出不答，資本強度這一面透明度不足，列入觀察。","evidence_level":"兩場法說逐字稿","settle_metric":"下次法說是否揭露折舊占營收比與 2027 年資本支出範圍","if_then":["若 4Q26 法說仍不給 2027 年資本支出範圍且資本支出再上修，則把 H3 視為削弱，倉位上限維持 3%"],"evidence_refs":[]},{"axis":"合併營收成長品質","cause":null,"prior_field":null,"side_a":"第三季合併營收指引季增 21%～22%。","side_b":"其中 EMS 季增約 40%，財務長說主要是記憶體零件漲價轉嫁，扣除後是正常季節性，EMS 營業利益率約 3.7%～3.8%。","ruling":"可調和：判斷成長改看封測營收（季增 11%～13%）與營業利益，不用合併營收。","evidence_level":"2Q26 法說逐字稿","settle_metric":"封測營收季增率","if_then":["若封測營收季增率連兩季低於 5% 而合併營收仍高成長，則視為成長品質惡化，H2 削弱"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"4Q26 封測毛利率是否突破 30%","type":"假設驗證","maps_to":"H1","metric":"封測（ATM）毛利率","threshold":"4Q26 ≥29.5%","action":"達標則上調 Base 終端倍數重算；未達標維持觀望","source_freq":"公司季度法說／每季","date":"2027-02","evidence_refs":["end_markets#0"]},{"n":2,"text":"2027 年 LEAP 倍增指引是否維持","type":"假設驗證","maps_to":"H2","metric":"LEAP 營收指引與實際","threshold":"2027 年約 70 億美元以上","action":"下修到成長五成以下即走唯一致命點流程","source_freq":"公司季度法說／每季","date":"2027-02","evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"資本支出高峰後自由現金流是否轉正","type":"假設驗證","maps_to":"H3","metric":"全年自由現金流與淨負債÷權益","threshold":"2028 年自由現金流 >0 且淨負債÷權益 ≤60%","action":"未達標則倉位上限維持 3%","source_freq":"年報／每年","date":"2029-03","evidence_refs":[]},{"n":4,"text":"產能大增後稼動率跌破下行門檻","type":"風險","maps_to":"R1","metric":"混合稼動率","threshold":"<75%","action":"已持有者減碼一半","source_freq":"法說管理層口述／每季","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_prior_downcycle_behavior#0"]},{"n":5,"text":"競爭對手與在地化分走主要客戶訂單","type":"風險","maps_to":"R2","metric":"前五大客戶營收占比","threshold":"單季下降 ≥3 個百分點且管理層未說明","action":"減碼一半並重跑研究","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["competitive_share_entrants#3","geo_supply_chain#2","reg_tariff_export#0"]},{"n":6,"text":"公司明確下修 2027 年 LEAP 倍增指引","type":"Single Thing","maps_to":"single_thing","metric":"2027 年 LEAP 營收指引","threshold":"由倍增下修到成長五成以下","action":"已持有者清倉；未持有者不碰","source_freq":"公司季度法說／每季","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":7,"text":"價格回到合理區且毛利未破","type":"估值rearm","maps_to":null,"metric":"股價與封測毛利率","threshold":"股價 ≤500 元且封測毛利率 ≥27%","action":"重跑研究後考慮 2% 首倉","source_freq":"每日股價＋每季法說","date":null,"evidence_refs":[]},{"n":8,"text":"股價跑到 2027 共識 EPS 30 倍以上而獲利未上修","type":"減碼","maps_to":null,"metric":"股價÷2027 共識 EPS","threshold":"≥30 倍（約 880 元）","action":"已持有者減碼一半","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":9,"text":"4Q26 法說後全面複審","type":"複審日期","maps_to":null,"metric":"結構毛利區間、2027 年資本支出、LEAP 指引","threshold":null,"action":"重跑研究","source_freq":"一次","date":"2027-02-15","evidence_refs":[]}],"kill_metrics":[{"metric":"封測（ATM）毛利率","bear_threshold":"連兩季低於 25%","window":"2027～2028 年","source":"公司季度法說簡報","last_status":"ok"},{"metric":"合併月營收年增率","bear_threshold":"連三個月轉負","window":"每月公告","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"混合產能稼動率","bear_threshold":"低於 75%","window":"每季","source":"法說會管理層口述","last_status":"ok"},{"metric":"淨負債÷權益","bear_threshold":"高於 80%","window":"每季","source":"季報資產負債表","last_status":"ok"},{"metric":"2027 年 LEAP 營收指引","bear_threshold":"由倍增下修到成長五成以下","window":"2027 年各季法說","source":"公司季度法說","last_status":"unknown"}],"evidence_dismissed":[{"ref":"substitute_technology#2","reason":"搜尋摘要無法對應到單一來源網址，屬未具名線索，且同一摘要自述英特爾基板良率偏低、短期實質影響有限；英特爾一條龍的威脅已由具名來源的同業條目處理，不重複計入。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=46.51, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價≤500 元（約 2027 共識 EPS 17 倍）且封測毛利率仍≥27%、LEAP 倍增指引未下修","exec_line":"現價不建倉。觸發價格條件後重跑研究，再考慮 2% 首倉；已持有者不加碼，封測毛利率連兩季低於 25% 或稼動率跌破 75% 減碼一半，LEAP 倍增指引明確下修則清倉。"},"reasoning":{"industry":"2Q26 合併營收 1,911 億元、季增 10%、年增 27%，毛利率 21.0%、營業利益率 11.1%，歸屬母公司淨利 211 億元。其中約 57 億元是投資評價與匯率避險利益，公司自己說可能不會重複，約合每股 1.1 元，判讀核心獲利時要扣掉。第三季指引合併營收季增 21%～22%，但 EMS 季增約 40% 主要來自記憶體零件漲價轉嫁，屬於低毛利的過路營收，實質成長要看封測（季增 11%～13%、毛利率 28%～29%）。產業時鐘在擴張期：管理層說限制在裝機與蓋廠速度而不是需求，混合稼動率 80%～85%，打線、測試都接近滿載。供需持久度：需求面到 2027 年能見度高，但供給可逆性高，公司同時進行 13 個新建、8 個改建工程，法人估日月光 CoWoS 類月產能 2027 年底會是 2026 年底的數倍，2028 年後供給可能追上需求。循環位置讀數：資本支出約為折舊三倍、稼動率近滿，偏賣方；訂單能見度領先資本支出、量價齊升，偏買方；客戶集中但信用強、股價貼近法人目標價，屬中性，整體判在中段，持有不加。長期成長部分（LEAP 先進封測）另計，不隨循環賣出。單點依賴：前五大客戶占 44%，另有單一客戶占比超過一成，且未具名；與主要晶圓代工夥伴的委外分工是 LEAP 成長來源，這是集中度風險，也是護城河的一部分。","moat":"機制是規模與台灣群聚、全自動產線，加上與主要晶圓代工夥伴的委外分工位置；純封測代工不與客戶、晶圓廠或基板廠競爭，管理層把多年累積的客戶信任列為先行者優勢。可證方向：TTM 毛利率 19.5% 高於 Amkor 15.5%，營業利益率 9.9% 高於 Amkor 8.6%（合併數字含 EMS 稀釋，封測單看 2Q26 為 15.7%）；封測毛利率一年內上升 5.4 個百分點，封測占營業利益由 87% 升至 94%。投入資本報酬的同業差距事實表未涵蓋，只能用利潤率代替。執行力評 8：LEAP 2026 年高於 35 億美元並有 2027 倍增的產能能見度，Full process 與面板級封裝依進度推進。定價力評 6：漲價與毛利率突破結構上限是真的，但管理層自己把近期成長限制歸因於產能，下行時這部分會回吐；2023 年毛利率曾掉到 15.8%。產業態勢屬雙向拉鋸：結構轉好（AI 先進封裝供不應求，法人稱 2027 年仍滿載）與競爭變動（Amkor 取得 NVIDIA 美國多年期合約、Intel EMIB 積壓訂單增加、客戶在地化）同時發生。","growth":"成長來源是量（新產能開出）、價（漲價與成本轉嫁）與組合（LEAP 占比上升），沒有併購或回購。共識 EPS 由 2025 年 8.89 元到 2026 年 18.83 元、2027 年 29.22 元，兩年年化約 81%；同期營收共識只成長約三成與兩成五，第三年共識事實表未涵蓋。內生天花板 12%（借款支應約 24%），缺口主要歸因於利潤率擴張：營業利益率由 2025 年 8.0% 升到 2Q26 11.1%，第三季指引 11.5%～12.5%，屬營運槓桿與稼動率，循環性成分高。跑道：先進封裝（凸塊、覆晶、晶圓級、系統級）2025 年第三季已占封測營收 48%，落在 35%～70% 區間；CPO 年底初期生產、面板級全自動線 2027 年第一季量產，屬有來源的下一條曲線，但 CPO 管理層說要再兩季才給數字，尚未能算進主要跑道。衰退訊號亮兩項：EPS 成長遠高於營收成長；自由現金流÷淨利連兩年低於 0.75。","governance":"2Q26 營業現金流 470 億元，廠房設備淨支出 798 億元，推算自由現金流 -328 億元；TTM 自由現金流利潤率 -6.15%。年度看，2024 年自由現金流 91 億元對淨利 324 億元（約 0.28），2025 年 -236 億元對淨利 400 億元。2026 年資本支出三度上修到 105 億美元（廠房 40 億、設備 65 億），4 月時財務長說資金缺口主要靠新增借款，7 月說負現金流會持續一段時間。淨負債約 1,901 億元，2Q26 淨負債÷權益 47%，未動用額度 3,962 億元，短期資金無虞。現金去向：擴產遠大於股息，無回購、無大型併購（購入既有廠房屬資本支出）。員工股票酬勞事實表未涵蓋。","valuation":"現價對 2026 共識 EPS 18.83 元是 35.6 倍，對 2027 共識 29.22 元是 22.9 倍；trailing 本益比 51 倍、股價營收比 4.14 倍、EV/S 4.41 倍都在近四個年度端點的最高。法人目標價 685～835 元，現價已在區間下緣附近。我的 Base：2027 年 EPS 28.5 元給 22 倍約 627 元，短期約 -6%；五年後 EPS 37.5 元給 18 倍約 675 元，中期幾乎持平。2027 年 EPS 本身建立在稼動率近滿、毛利率破結構上限的尖峰假設上，2Q26 淨利還含約每股 1.1 元的一次性利益，用它算出來的 23 倍不構成便宜的理由。","premortem":"三個視角都寫在反證紀錄。論點失敗的故事有歷史先例：2022→2023 年營收年減 13%、毛利率 20.1%→15.8%、稀釋 EPS 13.81→7.18 元；本輪資本支出是過去的數倍，自由現金流已為負、淨負債約 1,901 億元。價格已反映太多：26 週已漲 46.5%，trailing 51 倍。兩項衰退訊號亮燈，屬中度陷阱風險；主要擔心的不是生意變差，而是在循環高點付出成長股的倍數。"},"plain":{"six":{"how_it_makes_money":"賺的是 AI 晶片封裝測試的產能稀缺錢：錢卡在「把晶圓變成可出貨晶片」這一節，封測部門以 66% 營收拿走 94% 營業利益。","moat":"↑：先進封裝執行力與定價在擴大，但定價改善有相當部分來自供不應求，未經下行驗證。","growth":"後五年跑道中等：先進封裝已占封測營收近半，CPO 與面板級封裝是下一條曲線，但目前沒有營收數字。","capital":"處於重投資期：營業現金流與新增借款全部投入擴產，自由現金流為負，股息殖利率約 1%，沒有回購。","valuation":"670 元要求 2027 年共識 EPS 29 元兌現，而且 2028 年後產能大增時毛利率不回吐、倍數維持 20 倍以上；前半我大致信，後半不信。","how_wrong":"最可能看錯在把尖峰毛利當常態：2028 年產能大增若碰上 AI 資本支出消化，稼動率與毛利率會像 2023 年那樣回吐，而這次折舊基數更大。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到約 500 元以下（約 2027 共識 EPS 17 倍），且封測毛利率仍 ≥27%、2027 年 LEAP 倍增指引未下修","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":670.0,"week26_return_pct":46.51,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"2Q26 淨利含約 57 億元評價與避險利益（約每股 1.1 元），2027 共識 EPS 又建立在稼動率近滿、毛利率破結構上限的尖峰假設上；分母本身就是爭點，按 2027 年 23 倍算便宜的說法不成立。"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"3Q26 正式法說與第四季指引（報導稱第三季營收已優於指引，待原文確認）","impact":"高","watch":"第四季封測毛利率指引是否接近 30%"},{"date":"2026-12","date_precision":"month","type":"product","event":"CPO 初期小量生產","impact":"中","watch":"頻寬、散熱與良率的初步數據"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"4Q26 法說：結構毛利區間是否上調、2027 年資本支出與 LEAP 指引","impact":"高","watch":"資本支出規模與 LEAP 倍增是否維持"},{"date":"2027-03","date_precision":"quarter","type":"capacity","event":"310×310 面板級封裝全自動線量產","impact":"中","watch":"客戶採用與良率"}],"_projected_from":"v19"}
```
