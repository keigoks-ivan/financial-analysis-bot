你是 stock-analyst v20 的**散文層（prose）agent**，標的 SNPS（2026-10-19）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNPS_20261019/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：SNPS　日期：2026-10-19　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1497B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（814B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（996B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1509B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1201B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（593B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1425B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1987B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3995B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2226B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1497           3852-5503      5 條（2–6 內）  
s3                  8000         814           5030-7186      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3706          7906-11294      5 條（2–6 內）  
s6                 11000         593          7285-10407      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1425           1452-2075      3 條（2–6 內）  
s10                 5000        1987           2109-3013      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2226           2000-2774      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5374B；至少需散文≈39.63KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−35%
−35
0
0.2
0.5
0.56
0.75
0.9%
1
1%
1.0
1.01
1.05
1.1%
1.12
1.3%
2
2%
02
2.25
2.316
2.5
3
3.3%
3.5%
3.84
4
04
4.08
4.74
4.8
5
5%
05
6
07
7%
7
7.11
8%
8
8.04
8.5%
09
9%
9
9.25
9.3
9.35%
9.6
10%
10
10.0
11%
11.0%
11
11.4
12
12.4%
13%
13.3
13.5
13.7%
14
14.4%
15
15%
15.04
15.10
15.14
16
16%
16.6
17
17%
17.4
17.6
18
18%
18.5
18.6
18.67
18.70
19
19%
19.08
19.1
20%
20
21
21.9
22
23%
23.3%
23.6
24
24.35
24.4
24.77
25%
25
25.6
26%
26
26.5%
27
28
28.6%
29.2%
29.2
29.7
29.8
30.0
30
30%
30.03
30.6%
30.8%
31%
31
34.2
35.8%
36%
36
41%
41
41.5%
41.6%
42%
42
43.5
44%
45%
45.2%
49
50%
50
53.0
54%
60%
70
72.3
72.4%
77.0%
79.7%
80
80.6%
81%
85%
85.9%
90
90%
95%
96.9
97.2
97.4
100
100%
109
109.3
110.5
111.5
150%
350
400
454.63
504
564
571
640
871
2025
2026
2027
2030
4000
688521
20261019
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
{"meta":{"ticker":"SNPS","date":"2026-10-19","schema":"v15.0","contract":"v19","company_name":"Synopsys, Inc."},"oneliner":"AI 讓晶片設計更複雜，工具用量隨之增加。Synopsys 連兩季超預期並上調財測，FY27 共識前瞻約 24 倍、PEG 約 1，價格合理；關鍵在核心 EDA 年增能否從 8.5% 拉到 13% 以上，並守住 FY27 財測。","thesis":{"H":[{"id":"H1","text":"FY27 財測兌現：營收年增約 15%，non-GAAP 營業利益率擴張到約 44%，EDA 有機年增回到 13% 以上。","2y":"FY27 營收 ≥109 億美元、non-GAAP EPS ≥18.5","5y":null,"10y":null,"threshold":"FY27 營收 ≥109 億美元，non-GAAP EPS ≥18.5，EDA 有機年增連兩季 ≥13%","source":"Synopsys 季報新聞稿、法說與財測","drift_rule":"營收或 EPS 連兩季落後財測路徑 ≥5% 視為削弱，連三季 ≥10% 視為反轉"},{"id":"H2","text":"IP 從 FY26 低迷回到高十幾 % 成長，客製化 IP 由授權轉成授權加版稅，2030 年達 10 億美元。","2y":null,"5y":"Design IP 年增 ≥15%（FY27–FY28），FY28 起出現版稅營收","10y":null,"threshold":"Design IP 年增 ≥15%，FY28 年報揭露版稅營收","source":"季報分部揭露、投資人日更新","drift_rule":"連四季年增低於 10% 視為削弱，連六季低於 5% 視為反轉"},{"id":"H3","text":"AI agent 讓每個設計案呼叫更多工具，是增量而不是替代；Synopsys 透過訂閱加用量或成果分成拿到這部分價值。","2y":null,"5y":null,"10y":"EDA 長期年增 ≥13%，AI 相關營收從 FY27 開始揭露且逐年成長","threshold":"EDA 年增維持 ≥13%，積壓訂單不出現年減","source":"季報、年度財報、投資人日","drift_rule":"跨兩個年度 EDA 年增 <10% 視為削弱，跨三個年度視為反轉"}],"R":[{"id":"R1","text":"中國出口管制反覆，中國客戶無法啟動新設計案；中國約占營收 10%。","h_ref":"H1","clock":"⚡","threshold":"再度出現出口授權要求，或財測因中國下修 ≥2%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#1"]},{"id":"R2","text":"大型晶圓代工客戶（媒體推測為 Intel）需求轉弱或 IP 執行失準，重演 2025 年 9 月單日跌 36%；相關證券集體訴訟仍未裁決。","h_ref":"H2","clock":"🔥","threshold":"Design IP 連兩季年增 <5%","evidence_refs":["customer_concentration_credit#2","capital_markets_pricing#6","major_events#0","lawsuit_class_action#0"]},{"id":"R3","text":"AI 原生設計、hyperscaler 自建與每案工程師減少，侵蝕授權池。","h_ref":"H3","clock":"🐢","threshold":"積壓訂單年減且 EDA 年增 <10% 同季出現","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","substitute_technology#0","substitute_technology#2","geo_supply_chain#2"]},{"id":"R4","text":"Cadence 在數位實作搶占份額。","h_ref":"H1","clock":"🐢","threshold":"出現具名大客戶整套流程轉向 Cadence，或 EDA 成長連四季低於 Cadence","evidence_refs":["competitive_share_entrants#5"]}],"single_thing":{"description":"FY27 財測（營收約 111.5 億、non-GAAP EPS 約 19.08）在 FY27 任一季財報被下修，營收中點低於 109.3 億或 EPS 中點低於 18.70。","why_fatal":"現價 24 倍是建立在新長期框架第一年就兌現的前提上；管理層一年前已失準一次，再失準會讓市場改用個位數成長的倍數評價，這是 EPS 與倍數同時下修的最大單一敏感項。","if_happens":"清倉，等新財測至少穩定兩季後再重跑判斷。","how_monitor":"每季財報的 FY27 指引中點、EDA 有機成長、IP 季增與積壓訂單。","probability":"約 25%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":24.35,"peg_fy2":1.05,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":15.14,"FY2027E":18.67,"FY2028E":null},"fy_end_month":10,"eps_basis":"non-GAAP 稀釋 EPS（yfinance 共識）。FY2025 non-GAAP 實際值事實表未涵蓋（只有 GAAP 8.04）；FY2028E 共識事實表未涵蓋（只有兩個年度）。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNPS_20261019/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高毛利設計軟體寡占，正從大型併購後修復利潤率"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：AI 設計啟動加速、非 AI 兩季止穩（Q3 FY26 法說 CEO）；EDA 年複合 13% 高於半導體研發 7%（SemiAnalysis primer）。","bargaining":{"up":"上游以人才與運算資源為主，與 NVIDIA 是 GPU 加速合作關係，沒有供應商卡脖子。","down":"FY2023 單一客戶占 12.4%；hyperscaler 自研晶片客戶議價力上升，續約時不願承諾三年固定容量（投資人日 CEO）。","geo":"中國約占季營收 10%（2025-04 季，第三方估計），受出口管制影響；韓國今年營收占比接近 20%（Q3 FY26 法說分析師提問）。"},"profit_pool_dir":"利潤池往設計前段集中：多物理模擬與 IP 客製化讓 EDA 廠在晶片研發預算的占比上升；但 OpenAI 合作採營收分成，部分價值要讓給模型商。","tam_table":[{"item":"CY2025 EDA 營收規模","value":"Synopsys 約 80 億美元（含 Ansys）、Cadence 53.0 億、Siemens EDA 約 22–25 億（SemiAnalysis，2026）"},{"item":"三大廠合計市占","value":"逾 85%；Synopsys 與 Cadence 各約 30%（Barchart 引述分析師）"},{"item":"產業成長","value":"EDA 年複合 13%，半導體研發支出 7%"},{"item":"新品類：IP 客製化加版稅","value":"管理層目標 2030 年營收 10 億美元，FY27 沒有版稅，FY28 起才開始（投資人日）"},{"item":"新品類：AI agent 用量計費","value":"50 個以上客戶合作進行中；計價方式仍在早期探索，客戶目前偏好訂閱"},{"item":"OI 池五年遷移","value":"事實表未涵蓋"}]},"moat":{"mechanism":"簽核精度與晶圓代工製程認證造成的轉換成本，加上 silicon-proven 介面 IP 的規模優勢；三家寡占合計逾 85%。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"市占兩家各約 30%，三家寡占逾 85%，沒有具名客戶轉移；IP 關鍵標準勝率逾 90–95%。GAAP 營業利益率 11.0% 對 Cadence 30.8% 主要是併購攤提，不是份額流失。Cadence 數位實作推進屬意見文章，不足以判為下降；AI 帶來的用量增加尚未轉成可驗證的定價提升，也不足以判為上升。","peer_na_reason":null,"threats":[{"level":"🟡","text":"Cadence 在數位實作逐步推進，屬點對點競爭；目前只有意見文章，沒有份額數據。","p":"30%","evidence_refs":["competitive_share_entrants#5"]},{"level":"🔴","text":"Hyperscaler 自建設計能力與 AI 原生流程，可能侵蝕最高價值客戶；10-K 也承認受管制影響的客戶可能自行開發或改用替代方案。屬生態攻擊，目前定性為長期情境。","p":"30%","evidence_refs":["competitive_share_entrants#3","geo_supply_chain#2","competitive_share_entrants#1"]},{"level":"🔴","text":"AI 讓每個設計案需要的工程師變少，授權總數可能隨之縮小；管理層的反論是 agent 呼叫工具的頻率更高。若改用用量計費卻談不攏，就會變成減量。","p":"30%","evidence_refs":["substitute_technology#2","substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（推論：Ansys 約 350 億美元收購讓投入資本大增；投入資本實際數字事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是設計工程師，決策者是研發主管，付款者是晶片公司，三個角色都成立。客戶要解決的是「投片一次成功」，延後購買的代價是投片失敗與上市延誤；AI 與先進封裝讓設計啟動加速，非 AI 兩季止穩（Q3 FY26 法說）。"},{"item":"決策層級","level":"🟢","text":"替代要在整套流程與製程認證的層級發生，不是單一工具；管理層稱所有自研晶片客戶都用到其 EDA、硬體驗證、IP 與模擬（Q2 FY26 法說）。反例：Cadence 數位實作推進，代表單點工具層級仍可被替換；客戶也不願承諾三年固定容量。"},{"item":"價值鏈分配","level":"🟡","text":"EDA 占半導體研發支出的比重上升（13% 對 7%），但 hyperscaler 客戶議價力增強，OpenAI 合作採營收分成，GPU 加速的部分價值歸 NVIDIA；客戶自建 agent 的能力正在形成。"},{"item":"社會容忍度","level":"🟡","text":"屬政策風險而非價格天花板：2025-05 美國商務部曾對中國 EDA 出口加授權要求，同年 7 月解除；FTC、歐盟與英國對 Ansys 併購都要求剝離資產，三家寡占持續受反壟斷關注。"}],"roiic":"事實表未涵蓋投入資本與 Ansys 分部營業利益，無法計算。僅能指出：Ansys 約 350 億美元收購，FY26 貢獻營收約 29.8 億，營收對收購價約 8.5%。","reinvest_rate":"有機再投資率低：FY26 資本支出指引約 2.25 億美元，對比 FCF 約 26 億（約 9%）。研發費用化占營收約 30.6%，這才是實質再投資；D&A 與營運資金變動事實表未涵蓋。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。有機實體再投資很少，研發又全數費用化，公式算出的天花板會偏低；共識 EPS 成長主要靠利潤率擴張與併購綜效，不是靠新增投入資本。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","SNPS":72.38,"CDNS":85.87,"ARM":97.54,"QCOM":54.23,"688521.SH":null,"unit":"%"},{"metric":"營業利益率","SNPS":11.03,"CDNS":30.82,"ARM":17.3,"QCOM":23.28,"688521.SH":null,"unit":"%"},{"metric":"FCF 利潤率","SNPS":29.18,"CDNS":28.64,"ARM":28.55,"QCOM":23.64,"688521.SH":null,"unit":"%"},{"metric":"研發密度","SNPS":30.6,"CDNS":33.02,"ARM":57.49,"QCOM":22.45,"688521.SH":null,"unit":"%"}],"competitors":[{"name":"CDNS","gm":85.87,"om":30.82,"fcf_margin":28.64,"rd_intensity":33.02,"strategy_note":"最直接對手，市占約 30%，GAAP 營業利益率與毛利率都高於 Synopsys；有文章稱其數位實作工具推進，但沒有份額數據。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ARM","gm":97.54,"om":17.3,"fcf_margin":28.55,"rd_intensity":57.49,"strategy_note":"處理器 IP 授權加版稅模式；Synopsys 已出售處理器 IP，雙方直接重疊縮小，ARM 主要作為版稅模式的參照。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"QCOM","gm":54.23,"om":23.28,"fcf_margin":23.64,"rd_intensity":22.45,"strategy_note":"既是客戶也是授權模式的可比公司，毛利率 54% 含硬體，只當作授權變現的參照，不當護城河對照。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"688521.SH","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"中國本土 IP 與設計服務廠，事實表無財務資料；可作為出口管制下中國客戶尋找替代的觀察點。"}]},"growth":{"driver_mix":"量（設計啟動數與每案工具用量）為主，併購（Ansys）與利潤率擴張次之，淨回購很小。","runway_years":"事實表未涵蓋滲透率數據；EDA 三家寡占逾 85%，核心市場滲透已高，延伸空間在多物理模擬與 IP 版稅。","runway_post_y5":"🟡","endo_ceiling_basis":"有機實體再投資率約 9%（資本支出對 FCF），投入資本與 ROIIC 事實表未涵蓋，無法給數值天花板。共識 EPS 23% 年增明顯高於有機再投資能支撐的幅度，差額由利潤率擴張與綜效解釋，因此視為超出天花板。","segments":[{"item":"Design Automation（含 Ansys 約 7.11 億）","value":"Q3 FY26 約 20 億美元，調整後營業利益率 45.2%；其中 EDA 年增 8.5%（去年同期基期 16%），Q4 與全年預期雙位數"},{"item":"Design IP","value":"Q3 FY26 4.74 億美元，年增約 11%，調整後營業利益率 26.5%；長期下限 17%（投資人日）"},{"item":"Ansys（模擬與分析）","value":"FY26 貢獻約 29.8 億美元，長期下限 10%；FY27 起半導體業務約占 Ansys 營收 10%，將改列入 EDA"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":true,"note":"年度毛利率 80.6%→79.7%→77.0%，TTM 72.4%，主因 Ansys 組合與攤提"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"只有意見文章，沒有份額數據"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"事實表未涵蓋"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY27 共識 EPS +23.3% 對營收 +13.7%"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"note":"FY24 0.56、FY25 1.01，未連續"},{"signal":"SBC／營收逾 5% 且逐年上升","lit":false,"note":"Q3 為 9.35%，逾 5%；是否逐年上升事實表未涵蓋，管理層目標 2030 年降至 8%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"AI 替代屬推論，尚無數據"},{"signal":"產業估值倍數近三年系統性下移","lit":false,"note":"事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"資本支出約 2.25 億對 FCF 約 26 億"},{"signal":"停止投資新產能且營收三年內下滑","lit":false,"note":"不適用"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":[{"item":"Ansys 收購","value":"約 350 億美元，現金加股票，約 100 億債務融資，2025-07-17 完成；光學事業群依監管要求剝離給 Keysight"},{"item":"償債","value":"定期貸款提前還清；Q3 FY26 總債務約 100 億，淨負債 72.3 億（含租賃）"},{"item":"回購","value":"Q2 FY26 2.5 億 ASR 加 0.5 億公開市場；投資人日宣布未來數月回購 10 億"},{"item":"回報框架","value":"最多 FCF 的 50% 還給股東，並維持投資等級評等"},{"item":"處分","value":"處理器 IP 業務於 Q3 FY26 出售，FY26 營收約減 4000 萬"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"Ansys FY26 營收約 29.8 億÷收購價約 350 億＝約 8.5%；即使套用公司整體 non-GAAP 營業利益率 41.5%，稅前報酬也只有約 3.5%，低於合理資金成本。Ansys 分部營業利益事實表未涵蓋。","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"以 454.63 美元回購，FY26E non-GAAP 盈餘收益率 15.14÷454.63＝3.3%，GAAP 約 0.9%；10 年期公債殖利率事實表未涵蓋，但只要高於 1.3%，3.3% 就達不到殖利率加 2 個百分點。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 2.316 億×4≈9.3 億÷市值 871 億≈1.1%／年毛稀釋，扣除回購後更低；股數歷史事實表未涵蓋，淨額無法精算。","grade":"過"}]},"valuation":{"basis":"前瞻 non-GAAP P/E 與 PEG；P/S、EV/S 作為輔助","tier":"高毛利設計軟體","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業倍數，無法當作估值錨；Cadence 前瞻倍數事實表未涵蓋。"},"fwd_pe":24.35,"peg":1.05,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY27 前瞻 24.4 倍÷FY27 共識 EPS 年增 23.3%＝PEG 約 1.05，屬合理區間。P/S 在四個年度端點的低端（分位 0.2），EV/S 分位 16.6，偏便宜；但 non-GAAP 排除稅前每股約 4.8 美元的 SBC，GAAP P/E 80 倍，又抵銷一部分。五年分位事實表未涵蓋（只有四個年度端點），結論是合理，不是便宜。","upside_short_pct":11,"upside_mid_pct":41},"trap_analysis":{"verdict":"🟡","label":"兩個衰退信號亮起，皆屬併購與利潤率結構造成，需求面尚未見衰退"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"AI 讓每個設計案需要的工程師變少，授權總數可能縮小；AI 原生新創與 Kimi K3 展示不用商用 EDA 的設計實驗；hyperscaler 可能自建能力。","assumption":"AI agent 會大量呼叫既有工具，用量增加抵銷人數減少，而且 Synopsys 能把增量變現。","consequence":"若授權按人頭縮減，用量計費又談不攏，EDA 成長掉到個位數，EPS 停滯，倍數壓到 16 倍，五年虧損逾三成。","ruling":"部分採納：目前替代證據多為廠商自述或推論，Kimi K3 文章本身也說取代還很遙遠；Q3 硬體驗證創紀錄、EDA 財測上調，與替代說法方向相反。但計價模式未定是實質風險，列入熊市機率 30%。","watch":"FY27 各季 EDA 有機年增是否維持 13% 以上；管理層是否揭露 agent 或用量計費營收。","evidence_refs":["substitute_technology#2","substitute_technology#0","competitive_share_entrants#1","competitive_share_entrants#2"],"fact_refs":["f_rev_consensus_fy2_m"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 占營收 9.35%；Ansys 收購報酬遠低於資金成本；GAAP 營業利益率 11%，Cadence 為 31%；OpenAI 合作採營收分成。","assumption":"營收成長會轉成每股經濟價值，而不是被 SBC、利息與分成吃掉。","consequence":"營收如期成長，但 GAAP 盈餘與每股自由現金流成長落後 non-GAAP EPS，股東實得報酬比帳面成長低。","ruling":"採納一半：FCF 指引由 20 億上調到 26 億，FY27 約 31 億，現金面確實改善；但 SBC 與併購報酬是真實成本，因此資本配置只給中等，估值不判便宜。","watch":"SBC 占營收是否朝 8% 下降；FY27 FCF 是否達約 31 億美元。","evidence_refs":[],"fact_refs":["f_kpi4_sbc","f_peer_snps_operating_margin_pct","f_peer_cdns_operating_margin_pct","f_kpi3_free_cash_flow_ytd_9"]},{"view":"價格已反映太多","evidence":"管理層剛把長期目標從雙位數上調到 mid-teens，現價已隱含 FY27 營收年增 15%、EPS 19 美元；Q2 FY26 財測低於預期後股價跌 9%，2025 年大型晶圓代工客戶問題導致單季失準。","assumption":"一年前才失準的管理層，這次的長期框架可信。","consequence":"FY27 只要一季未達，估值就會從 24 倍往 18–20 倍修正。","ruling":"反駁大半：24 倍對應 23% EPS 成長，PEG 約 1，P/S 在四年低端，價格並未反映版稅與 agent 放量；但財測可信度是唯一致命點，所以設下財測下修即清倉的條件。","watch":"2026 年 12 月 Q4 FY26 財報是否維持 FY27 財測；IP 是否連續季增。","evidence_refs":["capital_markets_pricing#6","customer_concentration_credit#2"],"fact_refs":["f_pe_current","f_ps_percentile","f_consensus_eps_fy2"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 454.63","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=454.63","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"核心 EDA 能否由 8.5% 加速到 13% 以上","cause":null,"prior_field":null,"side_a":"管理層（Q3 FY26 法說、2026-09-30 投資人日 CFO）：Q4 與全年 EDA 雙位數，長期 mid-teens、下限 13%。","side_b":"Q2、Q3 FY26 EDA 年增都在 8–8.5%；投資人日分析師指出核心 EDA 近年低至中個位數，CEO 沒有回答單獨的成長數字。","ruling":"程度差異，可以調和：Q3 的 8.5% 是對上去年 16% 的高基期，硬體驗證創紀錄、Q4 財測隱含加速。但 13% 下限尚無一季實績，判斷暫採管理層方向，信心中等。","evidence_level":"管理層指引對比已實現季度數字","settle_metric":"FY27 前兩季 EDA 有機年增","if_then":["若 FY27 前兩季 EDA 有機年增都 ≥13% 且財測未下修，加碼到上限","若 FY27 任一季 EDA 有機年增 <10% 且全年財測未上修，減碼一半","若股價先漲到 FY27 EPS 30 倍以上但 EDA 數字還沒出來，不追"],"evidence_refs":[]},{"axis":"AI 對 EDA 是增量還是替代","cause":null,"prior_field":null,"side_a":"管理層：agent 讓 VCS／Verdi 授權用量增加 5–10 倍，50 個以上客戶合作進行中，OpenAI 出資後訓練 GPT-Synopsys。","side_b":"研究筆記與評論：每案工程師減少會縮小授權池；Kimi K3 不用商用工具完成設計實驗；客戶目前偏好訂閱，不想用量計費。","ruling":"方向尚未定論，目前偏向增量：已實現數字（硬體驗證紀錄、EDA 財測上調）支持增量，替代面只有實驗與推論。但結論在 FY27 揭露 AI 營收以前不可裁決，列為長期風險。","evidence_level":"已實現財報數字對比實驗與推論","settle_metric":"FY27 管理層揭露的 AI 相關營收，以及續約時用量條款的採用情況","if_then":["若 FY27 揭露 AI 營收並維持 EDA 13% 以上，視為增量論點成立，可加碼","若 FY27 積壓訂單年減且 EDA 年增 <10%，視為替代開始，減碼一半"],"evidence_refs":["substitute_technology#0","substitute_technology#2","competitive_share_entrants#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"前瞻 24 倍、PEG 約 1、P/S 在四年低端；連兩季超預期並上調財測，FCF 指引上調 6 億；FY27 EPS 指引 19.08 高於共識 18.67；10 億回購。","side_b":"核心 EDA 加速尚未實現，FY27 是新長期框架的第一年，一年前曾單日跌 36%。","ruling":"可調和：估值不構成阻礙，限制條件是財測可信度。所以以小倉起步，用 FY27 前兩季的 EDA 數字決定加碼或撤出，不等更低價格。","evidence_level":"估值數字對比執行紀錄","settle_metric":"2026 年 12 月 Q4 FY26 財報是否維持 FY27 財測","if_then":["若 Q4 FY26 財報維持或上調 FY27 財測，維持首倉","若 FY27 財測下修，清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY27 各季 EDA 有機年增檢驗長期 13% 下限","type":"假設驗證","maps_to":"H1","metric":"EDA 有機營收年增率（季）","threshold":"連兩季 ≥13% 為通過；任一季 <10% 為警示","action":"通過則加碼到上限；警示則停止加碼","source_freq":"季報新聞稿與法說，每季","date":"2027-02","evidence_refs":[]},{"n":2,"text":"美國對中國 EDA 或 IP 出口再度要求授權，或公司停接中國新單","type":"風險","maps_to":"R1","metric":"官方出口管制公告／公司對中國營收說明","threshold":"再次發出出口授權要求函，或財測因中國下修 ≥2%","action":"減碼一半","source_freq":"事件驅動，公告即查","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#1"]},{"n":3,"text":"Single Thing：FY27 財測被下修","type":"Single Thing","maps_to":"Single Thing","metric":"FY27 營收與 non-GAAP EPS 指引中點","threshold":"營收中點 <109.3 億美元（較 111.5 億低逾 2%），或 EPS 中點 <18.70","action":"清倉","source_freq":"季報，每季","date":"2026-12","evidence_refs":[]},{"n":4,"text":"大型晶圓代工客戶或 IP 再度低於預期","type":"風險","maps_to":"R2","metric":"Design IP 營收年增率（季）","threshold":"連兩季 <5%","action":"減碼一半","source_freq":"季報分部揭露，每季","date":null,"evidence_refs":["customer_concentration_credit#2","capital_markets_pricing#6"]},{"n":5,"text":"AI 替代開始反映在訂單：積壓訂單下滑加上 EDA 放緩","type":"風險","maps_to":"R3","metric":"積壓訂單年增率與 EDA 有機年增率","threshold":"積壓訂單年減，且 EDA 年增 <10%，同一季出現","action":"減碼一半","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","geo_supply_chain#2","substitute_technology#2"]},{"n":6,"text":"證券集體訴訟進展（2025 年 IP 揭露爭議）","type":"風險","maps_to":"R2","metric":"集體認證裁定與和解金額","threshold":"集體認證通過且和解金額逾 5 億美元；若有刑事或 SEC 調查介入","action":"前者減碼一半；後者清倉","source_freq":"法院文件與公司 10-Q，每季","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":7,"text":"股價回落但論點未破時加倉","type":"估值rearm","maps_to":"H1","metric":"股價對 FY27 共識 EPS 倍數","threshold":"股價 ≤400 美元（約 21 倍）且 FY27 財測未下修","action":"分批反買到上限","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":8,"text":"Q4 FY26 財報與 FY27 財測確認後重新檢查","type":"複審日期","maps_to":null,"metric":"FY27 財測、積壓訂單、IP 季增","threshold":"財報公布","action":"重跑判斷","source_freq":"一次性","date":"2026-12","evidence_refs":[]}],"kill_metrics":[{"metric":"EDA 有機營收年增率","bear_threshold":"FY27 起連兩季 <10%","window":"FY27 各季","source":"Synopsys 季報新聞稿與法說","last_status":"warning"},{"metric":"FY27 營收指引中點","bear_threshold":"<109.3 億美元","window":"FY27 各季財報","source":"Synopsys 季報新聞稿","last_status":"ok"},{"metric":"Design IP 營收年增率","bear_threshold":"連兩季 <5%","window":"未來四季","source":"Synopsys 季報分部揭露","last_status":"ok"},{"metric":"non-GAAP 營業利益率（年度）","bear_threshold":"FY27 <42%（指引 44%）","window":"FY27 全年","source":"Synopsys 年度財報與指引","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把「AI 會繞過 EDA」當成現況折價，P/S 落在四年低端；但 Q3 硬體驗證創紀錄、EDA 財測上調、Amazon 與 OpenAI 合作，都顯示 AI 目前在增加工具用量。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=1.12, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"FY27 前兩季 EDA 有機年增 ≥13% 且財測未下修；或股價 ≤400 美元且財測未下修","exec_line":"現價可小倉起步，不追高；FY27 前兩季 EDA 數字兌現再加碼，財測下修即清倉。"},"reasoning":{"industry":"營收分部（Q3 FY26 法說）：Design Automation 約 20 億美元，約占 81%，內含 Ansys 約 7.11 億，調整後營業利益率 45.2%；Design IP 4.74 億美元，約占 19%，年增約 11%，調整後營業利益率 26.5%。最新一季營收 24.77 億美元，non-GAAP 營業利益率 41.6%，GAAP 只有 14.4%，差距主要來自 Ansys 無形資產攤提、SBC 與重組費用。FY26 全年財測營收 96.9–97.4 億美元、non-GAAP EPS 15.04–15.10；積壓訂單 109 億美元，約一年營收，收入能見度高。產業位置屬擴張期：管理層說 AI 設計啟動持續加速，非 AI 設計啟動近兩季止穩，Q3 硬體驗證營收創紀錄。供需屬結構性持久：多晶粒與先進封裝讓每個案子的工具用量上升，EDA 產業年複合成長 13%，高於半導體研發支出的 7%。單點依賴：FY2023 10-K 揭露單一客戶占營收 12.4%，FY2018 前點名為 Intel；併入 Ansys 後客戶數擴大 10 倍，集中度應已稀釋，但最新年度數字事實表未涵蓋。議價權：上游供應商議價弱，主要成本是人才；下游 hyperscaler 自研晶片客戶的議價力上升，續約時不願承諾三年固定容量。","moat":"機制：先進製程投片動輒數億美元，客戶要求工具結果準確、可重現，加上與晶圓代工共同認證的製程設計套件，形成轉換成本（投資人日 CEO：「In AI, we believe, but in physics, we trust.」）。IP 端 PCIe 7 勝率逾 95%、車用設計勝率連三季逾 90%、die-to-die 累計逾 100 個設計勝利，顯示介面 IP 地位未動搖。方向證據：Synopsys 與 Cadence 各約 30% 市占，搜尋未找到 2026 年客戶從對手轉向 Synopsys 的具名案例，也未見反向流失；Cadence 在數位實作推進只出自意見文章。同業比較：TTM GAAP 營業利益率 Synopsys 11.0%、Cadence 30.8%，毛利率 72.4% 對 85.9%，差距主因是 Ansys 攤提與產品組合。差距為負，合併分不能給到 8 以上，因此落在 B。FCF 利潤率 29.2% 對 28.6%，現金面兩家相當。執行力 8：連兩季超預期並上調財測，成本綜效提前一年；但 2025 年 9 月 IP 低於預期曾讓股價單日跌 35.8%。定價力 7：AI 讓工具用量增加，但客戶續約不願承諾三年固定容量、偏好訂閱而非用量計費，中國 IP 需求也放緩。產業態勢屬雙向拉鋸：A 競爭面 AI 原生新創與 Cadence 推進都屬自述或意見，尚未證實；B 結構面 EDA 成長快於研發支出，屬結構性轉好；C 出口管制與商業模式轉向用量計費仍是變數。","growth":"成長來源：量（設計啟動數、每案工具用量）為主，加上併購（Ansys 併入使 Q3 營收年增約 42%）與利潤率擴張；回購貢獻小。共識 EPS 只有兩年：FY26E 15.14、FY27E 18.67，年增 23.3%；同期共識營收 97.2 億到 110.5 億，年增 13.7%，EPS 比營收快約 9.6 個百分點，差距來自利潤率擴張（管理層 FY26 41.5%→FY27 44%→2030 約 50%）與 4 億美元成本綜效。第三年共識事實表未涵蓋；管理層長期框架是 EPS 年增 mid-20s 到 2030。缺口歸因：利潤率擴張，加上研發費用化使公式天花板失真，不屬無法歸因。為什麼不是 🟢：第二條曲線有 Amazon 逾 10 億美元授權與 OpenAI 合作佐證，但版稅要到 FY28，客戶目前偏好訂閱；分析師在投資人日問到核心 EDA 近年只有低至中個位數成長，管理層沒有回答單獨的成長數字。","governance":"現金去向（近兩年）：一是 Ansys 約 350 億美元收購，現金加股票，其中約 100 億用債務融資；二是提前還清定期貸款，Q3 末總債務約 100 億、現金及短投 36 億；三是回購，Q2 啟動 2.5 億 ASR 與 0.5 億公開市場回購，投資人日再宣布數月內回購 10 億；四是股息，事實表未列，本包只提回購。股東回報框架為最多 FCF 的 50%。FCF 轉換：FY25 FCF 13.5 億對淨利 13.3 億，約 1.0 倍；FY26 指引 FCF 約 26 億，遠高於 GAAP 淨利，差額主要是攤提與 SBC。SBC 占營收 9.35%，換算每年約 9.3 億美元，管理層目標 2030 年降至 8%。","valuation":"FY27 共識 EPS 18.67 對應前瞻 24.4 倍，FY26E 為 30.0 倍；FY26→FY27 共識 EPS 年增 23.3%，PEG 約 1.05。P/S 9.25 倍，落在四個年度端點的最低端；EV/S 10.0 倍，分位 16.6。GAAP trailing P/E 80 倍，因為攤提與 SBC 被計入。non-GAAP 排除的 SBC 稅前約每股 4.8 美元，把它當成真實成本，倍數就更滿，所以不判便宜。賣方平均目標價約 564–571 美元（2026 年 7–9 月三份彙整），比現價高約 24–26%，方向支持合理偏低的判斷。短期上檔：FY27 EPS 18.67×27 倍≈504 美元，約 +11%。中期上檔：本案基本情境 FY29 EPS 25.6×25 倍≈640 美元，約 +41%。","premortem":"衰退信號亮兩個：毛利率下滑、EPS 成長遠快於營收成長，兩者都可由併購攤提與利潤率擴張解釋，不是需求衰退，屬中度風險。三個視角的反證與裁定見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"Synopsys 賺的是全球晶片設計研發預算：EDA 軟體訂閱（多年期授權）、硬體驗證設備、介面 IP 授權（正轉向授權加版稅），再加上 Ansys 的模擬軟體。錢卡在簽核精度與晶圓代工製程認證這一節點，客戶要投片就繞不過去。","moat":"護城河穩定（→），等級 B。機制是簽核精度加上晶圓代工製程認證造成的轉換成本，三家寡占合計逾 85%；但對最強同業的報酬差距目前為負，定價能否延伸到 agent 用量仍未證明。","growth":"Runway 中等（🟡）：EDA 本身已高度寡占、滲透率高，第二條曲線（IP 客製化加版稅、AI agent 用量、多物理整合）都有具名合約與時程，但 FY27 沒有版稅，agent 計價也尚未定案，營收還沒看到。","capital":"資本配置中等：Ansys 收購的報酬尚未證明高於資金成本，回購的盈餘收益率也偏低；SBC 毛稀釋約每年 1%，可以接受。","valuation":"現價要求 FY27 財測兌現（營收年增 15%、EPS 19 美元上下），之後 EPS 每年維持高十幾 % 成長。在不計 AI 版稅大爆發的前提下，我大致相信，因此估值合理，但談不上便宜。","how_wrong":"最可能看錯的地方：把管理層剛上調的長期框架當成既定事實。核心 EDA 近兩季只有約 8%，FY27 卻要做到 13% 以上；一年前 IP 低於預期曾讓股價單日跌 36%。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把「AI 會繞過 EDA」當成現況折價，P/S 落在四年低端；但 Q3 硬體驗證創紀錄、EDA 財測上調、Amazon 與 OpenAI 合作，都顯示 AI 目前在增加工具用量。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":454.63,"week26_return_pct":1.12,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"GAAP 與 non-GAAP 差距大（FY26 GAAP EPS 3.84–4.08 對 non-GAAP 15.04–15.10），主要是 Ansys 攤提（非現金）、SBC 與重組費用。本案用前瞻 non-GAAP，但把 SBC 視為真實成本，所以不據此主張便宜。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q4 FY26 財報，確認 FY27 財測","impact":"高","watch":"FY27 營收與 EPS 指引中點是否維持；IP 是否續季增"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q1 FY27 財報，首次檢驗 EDA 13% 下限","impact":"高","watch":"EDA 有機年增、AI 相關營收揭露"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"下一代 ZeBu 硬體驗證系統 Artemis 上市","impact":"中","watch":"硬體驗證營收是否延續紀錄"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"Multiphysics Fusion 由評估轉量產，開始貢獻營收綜效","impact":"中","watch":"營收綜效年化是否朝 FY27 末逾 1 億美元前進"}],"_projected_from":"v19"}
```
