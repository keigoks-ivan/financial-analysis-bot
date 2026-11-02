你是 stock-analyst v20 的**散文層（prose）agent**，標的 LIN（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：LIN　日期：2026-11-02　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1934B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（431B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（856B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（761B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（967B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（865B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1015B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2227B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4045B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2129B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1934           3546-5066      5 條（2–6 內）  
s3                  8000         431           5298-7569      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2584          8691-12416      5 條（2–6 內）  
s6                 11000         865          7094-10135      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1015           1740-2485      5 條（2–6 內）  
s10                 5000        2227           1941-2773      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2129           2000-2871      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4141B；至少需散文≈40.86KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−2027
−40%
−35%
−35
−34%
−30%
−30
−23%
−22%
−20%
−20
−17%
−13%
−3%
−2.5%
−2.39%
−2%
0
0.6%
0.738
0.74
0.75
0.750
0.8%
0.89
1
1%
1.08
1.085
1.2
1.3
1.5
1.5%
1.6%
1.6
1.7%
1.9
02
2
2%
2.1%
2.2
2.9%
3
3%
3.5%
3.7
3.8
3.9
4%
4
04
4.25
4.45
4.55
4.59
4.72
5
5%
5.04
6%
06
6
6.51
07
7
7%
7.14
7.6%
8%
8
8.23
9
9%
09
9.6%
10%
10
11
11%
11.4
12%
12
12.7
12.7%
14.0%
14
14.61
15%
15.8
16%
16.47
17
17.1%
17.2
17.5
17.77
17.8
17.82
17.87
17.89
17.90
17.92
18
18.05
18.1
18.20
18.2
18.6
19.0
19
19.3
19.4%
19.5
20%
20
20.6
21%
21.4
21.5
22
22%
22.3
22.9%
23
23.5
24
24.1
24.85%
25%
25
25.8
26
27.08%
27.2%
27.5
27.63
28
28.3
28.7
28.74
29
29.4%
29.5%
30%
30
31
31.6
34
34.15
35%
40%
42
47.86%
49
50%
50
55
60
60%
64%
67.5
69.4
70
80
90
94.04
100
100%
104
110
150%
227.6
228
333.6
339.9
460
461.9
483
514.24
522.5
548
560
562
579.8
600
800
2022
2023
2024
2025
2026
2027
2028
2029
2030
20261102
2,588
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
{"meta":{"ticker":"LIN","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Linde plc"},"oneliner":"Linde 靠現場供氣長約、管線密度與隨通膨調價穩定複利，2026 年調整後 EPS 約年增 8%–9%；但現價約 28.7 倍當年 EPS，一年基本情境上檔不到 2%，2027 年 2 月指引能否回到 8% 以上是關鍵，現價不追。","thesis":{"H":[{"id":"H1","text":"價格引擎：全公司價格貢獻維持每季約 +3%、跨各區分布，足以蓋過能源與配送成本通膨","2y":"每季價格貢獻 ≥ +2%，排除成本轉嫁的營業利益率不低於去年同期","5y":null,"10y":null,"threshold":"單季價格貢獻 ≥ +2%（Q3 2026 為 +3%）；排除成本轉嫁營益率年變化 ≥ 0bp（Q3 2026 持平）","source":"每季財報新聞稿價量拆解表與電話會議","drift_rule":"兩年期論點：近四季數值連兩季偏離門檻 ≥5% 視為削弱，連三季偏離 ≥10% 視為反轉"},{"id":"H2","text":"非氣體部門修復：Lincare 重組與裁員（Q3 2026 認列 4.25 億美元，回收期約 1.5–2 年，2027 年下半年全額生效）讓 2027 年調整後 EPS 回到年增 8% 以上","2y":"2027 年調整後 EPS ≥ 19.3 美元（2026 年指引中點 17.87 × 1.08）","5y":null,"10y":null,"threshold":"2027 年指引中點年增 ≥ 8%（排除匯率），全年實際 EPS ≥ 19.3 美元","source":"2027 年 2 月全年指引、每季調整後 EPS 與 Lincare 拖累說明","drift_rule":"兩年期論點：近四季數值連兩季偏離門檻 ≥5% 視為削弱，連三季偏離 ≥10% 視為反轉"},{"id":"H3","text":"專案積壓轉成量：sale of gas 積壓約 80 億美元（Woodside 2027 年下半年起量、2028 年滿載；電子專案約 20 億美元分 2–3 年投產），每年貢獻約 1% 的量成長，電子維持兩位數成長","2y":null,"5y":"電子年增 ≥10% 延續到 2029 年、Woodside 2028 年滿載、sale of gas 積壓維持 ≥ 70 億美元","10y":null,"threshold":"電子終端市場年增 ≥10%；sale of gas 積壓年底 ≥ 70 億美元","source":"季度電話會議積壓數字與終端市場拆解","drift_rule":"五年期論點：連四季偏離門檻 ≥5% 視為削弱，連六季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"歐洲去工業化：CEO 稱歐洲零催化劑，Q3 歐洲量 +1% 主要靠設備銷售、扣除後持平，化工停產持續","h_ref":"H3","clock":"🐢","threshold":"EMEA 排除設備銷售的基礎量連兩季年減 ≥ 2%","evidence_refs":["end_markets#2"]},{"id":"R2","text":"俄羅斯法律風險：Amur GPP 案 2026 年 1 月一審判賠 800 億盧布（子公司上訴中），RCA 案 HKIAC 仲裁進行中且聖彼得堡禁令未解除，二手來源估或有負債約 18 億美元（約每股 3.9 美元）；另慕尼黑擠出補償訴訟原告上訴中，未見美國證券集體訴訟","h_ref":null,"clock":"🔥","threshold":"任一案判決確定、資產遭扣押或認列損失合計 ≥ 10 億美元","evidence_refs":["geo_supply_chain#0","geo_supply_chain#4","major_events#1","lawsuit_class_action#0"]},{"id":"R3","text":"成本回收落差與氦氣反轉：merchant 與瓶裝氣成本回收落後 3–6 個月，Q3 美洲價格 +6% 中約 2pp 屬回收、管理層預期 Q4 回落；氦氣漲價被成本吃掉，荷莫茲海峽恢復後氦氣轉為過剩","h_ref":"H1","clock":"⚡","threshold":"排除成本轉嫁的營業利益率連兩季年減","evidence_refs":["geo_supply_chain#1"]},{"id":"R4","text":"Lincare 修復失敗：居家醫療勞動成本通膨與給付環境不利，今年已拖累 EPS 成長約 1.5%–2%；策略選項無法保證成交，出售可能認列損失；醫療器材合規方面，第三方紀錄顯示 2025 年 7 月曾收到 FDA 483 觀察（非警告信、原文未核）","h_ref":"H2","clock":"🔥","threshold":"2027 年 Lincare 拖累 EPS 成長仍 ≥ 1%，或出現 FDA 警告信","evidence_refs":["product_recall_warning#0"]}],"single_thing":{"description":"2027 年 2 月公布的 2027 年調整後 EPS 指引中點（排除匯率）年增低於 8%","why_fatal":"現價約 28.7 倍當年 EPS，倍數要靠 8%–12% 複利延續撐住；中點低於 8% 代表重組節省、Lincare 修復與 Woodside 投產都補不回量能疲弱，2027 年 EPS 落到 18.6 美元以下、倍數往 23–24 倍靠，股價約 −13%～−17%，是所有變數裡對五年報酬敏感度最大的一項","if_happens":"停止加碼，持股減至半倉；基本情境 2027 年 EPS 下修到 18.6 美元以下並重跑情境","how_monitor":"Q4 2026 財報電話會議（預計 2027 年 2 月）的全年指引；先行指標為 Q4 實際 EPS 是否 ≥ 4.45 美元（指引中點）","probability":"約 35%：Q4 指引只年增 5%–7%、公司不假設總經改善；但重組節省與 Lincare 拖累消失是 2027 年順風"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":28.3,"peg_fy2":3.7,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":16.47,"FY2026E":17.89,"FY2027E":18.2,"FY2028E":null},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（non-GAAP）。FY2025A 16.47 為推導值：公司 2026 年指引 17.82–17.92 美元對應年增 8%–9%（二手摘要），17.87 ÷ 1.085 ≈ 16.47，原始數字事實表未涵蓋；GAAP 稀釋 EPS 2025 年為 14.61。FY2026E、FY2027E 為 yfinance 共識；FY2028E 共識事實表未涵蓋（只有兩個年度）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LIN_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"全球寡占、長約加管線、價格隨通膨、調整後 EPS 約 8%–10% 複利、資本密集"},"industry":{"clock_phase":"I","sd_verdict_source":"結構性持久：10-K 對現場供氣、管線網絡與 merchant 三至七年合約的描述；量的週期性由 2026-10-29 電話會議終端市場拆解佐證","bargaining":{"up":"電力與天然氣供應商：現場供氣當月轉嫁，merchant 與瓶裝落後 3–6 個月回收；氦氣貨源集中卡達，議價在供應端","down":"客戶分散、無單一依賴；換供應商要重蓋現場工廠，客戶議價力弱","geo":"約 64% 營收在美國以外；歐洲能源成本結構性偏高、中國內需弱"},"profit_pool_dir":"利潤池集中在少數全球業者；增量在美國灣區化工、電子與太空，歐洲在流失；利潤池占比數字事實表未涵蓋","tam_table":{"expanded":false,"reason":"成熟寡占，不是低滲透、份額擴張或新品類故事，成長來自工業產出、通膨調價與專案積壓；事實表也沒有 TAM 與利潤池占比數字"}},"moat":{"mechanism":"本地供應密度：現場供氣蓋在客戶廠旁並簽長約、管線網絡連接多家大客戶、merchant 三至七年需求合約，換供應商要重蓋工廠","execution":8,"pricing":9,"grade":"B","trend":"→","trend_evidence":"價格 +3% 跨各區且量 +2%（Q3 2026）；營業利益率 2022→2025 由 19.4% 升到 27.2%，2026 年 Q2、Q3 調整後營益率年減 60bp、30bp，排除成本轉嫁為 −30bp、持平：擴張暫停而非逆轉，定價力未見縮減","peer_na_reason":"Air Liquide 只有 1 季、大陽日酸只有 2 季且缺營收，無法算利潤率；Messer 事實表無數字，只能與 Air Products 比","threats":[{"level":"🟡","text":"氦氣：卡達 Ras Laffan 約占全球三到四成，荷莫茲海峽受阻使約三分之一供應中斷；Linde 靠全球貨源調度並漲價，但成本同步上升、利潤率未明顯受惠；海峽恢復後氦氣轉為過剩、價格回落","p":"約 40%（12–24 個月內恢復並回落）","evidence_refs":["geo_supply_chain#1"]},{"level":"🟡","text":"關稅與進出口管制：10-K 風險因子列出可能壓低需求或售價；工業氣體多為當地生產當地賣，直接關稅曝險小，風險在客戶端製造業需求","p":"約 20%","evidence_refs":["reg_tariff_export#0"]},{"level":"🟡","text":"商業太空客戶想自建大氣氣體工廠（2026-07-31 CFO），只限大氣氣體、氫氣端未見；Linde 以賣廠加賣氣混合因應","p":"約 30%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"工業氣體是客戶製程的必需投入（煉油脫硫用氫、晶圓廠大氣氣體、醫療氧），使用者、決策者、付款者多為同一家工廠，屬需要而非想要；10-K 稱不依賴單一或少數客戶，終端市場分散。急迫性高但量隨工業產出循環，代理讀數＝Q3 2026 量 +2%，歐洲持平、中國內需弱"},{"item":"決策層級","level":"🟢","text":"替代性要在單一工廠層看：現場供氣是在客戶廠旁蓋廠的長約，換供應商等於重蓋一座廠；10-K 明列管線網絡所在地為競爭優勢，merchant 合約三至七年。代理讀數＝價格 +3% 下量仍 +2%，未見因漲價流失"},{"item":"價值鏈分配","level":"🟡","text":"最大投入是電力與天然氣：現場供氣當月轉嫁，merchant 與瓶裝落後 3–6 個月才回收，2026 年北美電力與配送成本上升時利潤率受壓；上游氦氣貨源集中卡達，議價在供應端；下游歐洲化工停產、Lincare 受醫療給付方壓價。Linde 掌握本地供應密度，但能源成本那一段要靠合約條款搶回"},{"item":"社會容忍度","level":"🟡","text":"醫療用氧與居家照護屬高必要、高敏感，給付價格受政府與保險壓制，Lincare 正是拖累來源；氦氣短缺時管理層表示刻意不過度漲價、只回收調度成本，屬保留社會容忍度的保費。10-K 揭露例行反壟斷索賠，未見針對性大案"}],"roiic":"事實表未涵蓋（缺投入資本與折舊攤銷）；管理層新專案門檻為稅後兩位數無槓桿 IRR（2026-07-31 CEO），未經驗證","reinvest_rate":"事實表未涵蓋精確值；代理：2026 年前三季部署逾 90 億美元，約一半投入事業（2026-10-29 CFO），全年資本支出約 55–60 億美元","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，再投資率＝（資本支出－折舊攤銷＋營運資金變動＋收購淨額）÷ NOPAT；缺折舊攤銷與投入資本，本輪不出數字"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","LIN":47.86,"APD":32.06,"AI.PA":null,"4091.T":null,"unit":"%"},{"metric":"營業利益率","LIN":27.08,"APD":24.85,"AI.PA":null,"4091.T":null,"unit":"%"},{"metric":"FCF 利潤率","LIN":14.02,"APD":-2.39,"AI.PA":null,"4091.T":null,"unit":"%"},{"metric":"研發密度","LIN":0.41,"APD":0.72,"AI.PA":null,"4091.T":null,"unit":"%"}],"competitors":[{"name":"APD","gm":32.06,"om":24.85,"fcf_margin":-2.39,"rd_intensity":0.72,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"AI.PA","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"period":"TTM ending 2025-09-30（1季加總）"},{"name":"4091.T","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"period":"TTM ending 2026-06-30（2季加總）"}]},"growth":{"driver_mix":"價格 3%–4%＋量 1%–2%＋淨減股約 2%，利潤率大致持平","runway_years":"不適用：成熟寡占，非滲透率故事","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板＝增量 ROIC × 再投資率；事實表沒有投入資本與折舊攤銷，算不出數字。可用代理：新專案門檻為稅後兩位數無槓桿 IRR（2026-07-31 CEO，未驗證），前三季部署資本約一半投入事業，Q3 量 +2% 中約一半來自專案積壓。基本情境 EPS 年複合拆為價 3%–4%、量 1%–2%、淨減股約 1.5%–2%，不靠利潤率擴張","segments":[{"item":"化工與能源（約占 22%）","value":"Q3 2026 年增 12%：美國灣區與中國量增，加上美洲回收先前成本通膨"},{"item":"製造（約占 21%）","value":"年增 7%：廣泛漲價，美、中、印量增，航太延續"},{"item":"醫療（約占 15%）","value":"年增 2%；排除 Lincare 為中個位數"},{"item":"金屬與礦業（約占 12%）","value":"年增 3%：美洲走強，歐洲與亞太小幅收縮"},{"item":"電子（約占 10%）","value":"年增 15%：亞太與美國有機成長，另有約 20 億美元專案建造中"},{"item":"食品飲料（約占 9%）","value":"年增 3%"},{"item":"占比來源","value":"占比引自投資人簡報的搜尋摘要、未讀原頁；成長率與 2026-10-29 電話會議一致"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差逾 5pp）","lit":true,"evidence":"GAAP 稀釋 EPS 2022→2025 由 8.23 升到 14.61 美元（年複合約 21%），營收由 333.6 億到 339.9 億美元（約 0.6%）；2022 基期偏低，但成長主要來自利潤率與減股而非量"},{"signal":"FCF／淨利低於 0.75 連兩年","lit":false,"evidence":"2024 年 0.750 剛好在線上、2025 年 0.738，再一年就亮"},{"signal":"毛利率連兩季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；調整後營業利益率 Q2、Q3 年減 60bp、30bp，排除成本轉嫁為 −30bp、持平"},{"signal":"核心市占縮減","lit":null,"evidence":"事實表未涵蓋市占"},{"signal":"提價後銷量下滑","lit":false,"evidence":"Q3 2026 價 +3% 量 +2%"},{"signal":"SBC／營收逾 5% 且上升","lit":null,"evidence":"事實表未涵蓋；稀釋股數年減約 2%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"10-K 未提替代技術；歐洲區域萎縮另列風險"},{"signal":"產業估值倍數近三年系統性下移","lit":null,"evidence":"事實表未涵蓋同業倍數"},{"signal":"維修資本支出占 FCF 逾 60%","lit":null,"evidence":"事實表未涵蓋拆分"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"專案積壓約 110 億美元，2026 年共識營收年增約 7%"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：併購只貢獻約 1% 營收成長，現金去向以專案資本支出、股息與回購為主"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月無重大併購完成申報，併購只貢獻約 1% 營收成長（2026-10-29 CFO）；已實現併購 ROIIC 事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"以前瞻本益比約 28.7 倍推算回購收益率約 3.5%（trailing 34.15 倍則約 2.9%）；要過關需 10 年期殖利率不高於 1.5%，10 年期殖利率事實表未涵蓋，CFO 於 2026-10-29 稱處於利率上升環境，判不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 金額事實表未涵蓋；以淨利 ÷ 稀釋 EPS 回推稀釋股數 2022 年約 5.04 億股、2025 年約 4.72 億股，年減約 2.1%，淨稀釋為負","grade":"過"}]},"valuation":{"basis":"前瞻本益比：FY2026 共識調整後 EPS 17.89 美元，現價 514.24 美元，約 28.7 倍","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有 Air Liquide、Air Products、大陽日酸的本益比，無法做倍數對照"},"fwd_pe":28.7,"peg":3.8,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"P/S 6.51 倍、EV/S 7.14 倍都在近 4 個年度端點最高（分位 100），trailing 本益比 34.15 倍在 67.5 分位；這些不是五年分位，真正五年分位事實表未涵蓋。加上 PEG 約 3.8、一年上檔不到 2%，但品質與現金流穩定、賣方目標仍高於現價，判偏貴、不到極貴","upside_short_pct":1.6,"upside_mid_pct":12.7},"trap_analysis":{"verdict":"🟡","label":"價格與減股撐起的複利，量能偏弱"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"歐洲：CEO 稱零催化劑、扣除設備銷售後量持平；中國：鋼鐵產量 −2.5%、化工持平、國內電動車購買年減約 11%–12%；美國灣區化工的原料優勢來自中東衝突，衝突結束後可能消退","assumption":"基本情境假設 2028 年起回到約 8% EPS 成長，量每年 +1%–2%","consequence":"若三地同時走弱而價格只跟上通膨，EPS 五年持平、倍數由 28.7 倍落到 18–20 倍，股價約 −30%～−40%","ruling":"部分採納：給 25% 熊市機率；但現場長約與當月成本轉嫁讓 EPS 下行有底，五年虧 50% 需要倍數腰斬，判低機率。與唯一致命點部分重疊：2027 年指引低於 8% 是這個故事的第一個訊號，已用同一觸發器監控","watch":"EMEA 排除設備的基礎量、全公司量能、2027 年 2 月指引","evidence_refs":["end_markets#2"],"fact_refs":["f_kpi7_2026_adjusted_diluted_ep"]},{"view":"論點成功但股東經濟變差","evidence":"FCF／淨利由 2023 年 0.89 降到 2024 年 0.75、2025 年 0.74，FCF 利潤率由 2022 年 17.1% 降到 TTM 14.0%；成長靠每年 55–60 億美元資本支出與約 80 億美元專案積壓，回購在 28–34 倍本益比買進；俄羅斯 Amur GPP 一審判賠 800 億盧布、RCA 仲裁與聖彼得堡禁令未解，二手來源估或有負債約 18 億美元；慕尼黑擠出補償訴訟原告上訴中；Lincare 出售可能認列損失","assumption":"EPS 複利能等比例轉成每股自由現金流","consequence":"EPS 照 8% 成長但每股 FCF 只成長 4%–5%，回購收益率約 3.5% 低於資金成本，股東實得報酬落到中低個位數","ruling":"採納為主要風險之一：基本情境終端倍數給 25 倍不給 28 倍；FCF／淨利連兩年低於 0.75 時再下修倍數；俄羅斯案件約每股 3.9 美元，單獨不致命","watch":"年度 FCF／淨利、資本支出占營收、俄羅斯案件判決與扣押進度","evidence_refs":["geo_supply_chain#0","geo_supply_chain#4","major_events#1","lawsuit_class_action#0"],"fact_refs":["f_peer_lin_fcf_margin_pct","f_kpi5_fcf","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"前瞻本益比約 28.7 倍、trailing 34.15 倍；P/S 6.51 倍、EV/S 7.14 倍都是近 4 個年度端點最高；賣方 7–8 月目標均價 548–562 美元只比現價高 7%–9%；FY2027 共識 18.20 美元只比今年高 1.7%","assumption":"市場願意持續給 28 倍以上","consequence":"就算 EPS 照基本情境走，倍數回到 25 倍會吃掉大半 EPS 成長，五年年化報酬只剩中低個位數","ruling":"採納：現價不追，等 460 美元附近或更強的 2027 年指引","watch":"股價對 2027 年 EPS 的倍數、2027 年 2 月指引","evidence_refs":[],"fact_refs":["f_pe_current","f_ps_percentile","f_ev_s_percentile","f_price_at_dd","f_consensus_eps_fy2"]}],"max_dd":{"lo":-35,"hi":-20,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 514.24","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=514.24","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"共識與公司指引","cause":null,"prior_field":null,"side_a":"2026-10-17 第三方網站：29 位分析師 FY2026 EPS 共識 18.05 美元，高於當時指引上限 17.90 美元（口徑待核）","side_b":"2026-10-29 財報後：FY2026 共識 17.89 美元，落在新指引 17.82–17.92 美元內；但 FY2027 共識 18.20 美元只年增 1.7%，遠低於 2026-07-31 CEO 所說的 8%–12%","ruling":"可調和：2026 年的落差在財報後已收斂，屬口徑與時點差異；真正未解的是 2027 年共識與管理層演算法的方向落差，本輪基本情境 2027 年取 19.0 美元（年增約 6%），高於共識、低於演算法下緣，待 2 月指引裁決","evidence_level":"二手共識網站＋一手電話會議","settle_metric":"2027 年 2 月公布的 2027 年調整後 EPS 指引中點","if_then":["若指引中點年增 ≥ 8% → 維持基本情境，股價 ≤ 460 美元時分批建立首倉","若指引中點年增 < 8% → 基本情境 2027 年 EPS 下修到 18.6 美元以下，持股減至半倉","若指引中點年增 < 3% → 清倉檢討"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"管理層利潤率承諾與兌現","cause":null,"prior_field":null,"side_a":"2026-07-31 CEO：預期第三季利益率環比改善；CFO：本季將採取成本行動","side_b":"2026-10-29：Q3 調整後營業利益率 29.4%，低於 Q2 的 29.5%，年減 30bp（排除成本轉嫁持平）；成本行動已兌現為 4.25 億美元重組費用","ruling":"可調和：利潤率承諾小幅落空，但成本行動照預告執行、Q3 EPS 4.59 美元高於 7 月指引 4.45–4.55；判執行力扣分而非論點破裂，執行力給 8 不給 9","evidence_level":"一手（兩場電話會議逐字稿）","settle_metric":"Q4 2026 調整後營業利益率與排除成本轉嫁的年變化","if_then":["若 Q4 營益率再低於 29.4% 且排除成本轉嫁年減 → 執行力降為 7，停止加碼","若 2027 年起排除成本轉嫁營益率年增 ≥ 30bp → 執行力回到 9"],"evidence_refs":["end_markets#3"]},{"axis":"基礎成長數字","cause":null,"prior_field":null,"side_a":"8-K 附件摘要：基礎成長 +9%＝價 6%＋量 3%","side_b":"10-Q 與 2026-10-29 CFO：銷售 +9% 扣掉匯率、成本轉嫁、併購、工程各約 1% 後基礎 +5%（價 3%、量 2%）；6% 是美洲區價格","ruling":"可調和：+9% 是總銷售成長，6% 價格是美洲區數字被誤當全公司；採 +5%","evidence_level":"一手（10-Q＋電話會議逐字稿）","settle_metric":"Q4 2026 財報價量拆解表","if_then":["若 Q4 全公司價格貢獻 < +2% → 停止加碼並重檢定價力分數"],"evidence_refs":["end_markets#0"]},{"axis":"歐洲量能","cause":null,"prior_field":null,"side_a":"Q3 2026 歐洲量 +1%，比 12–18 個月前的 −2%～−3% 改善，比較基期變容易","side_b":"CEO：扣掉設備銷售後持平、零催化劑，看不到歐盟採取讓工業回升的決策，中期不抱期望","ruling":"可調和：程度差異；採 CEO 說法，歐洲不進基本情境的量成長，只當作已觸底的穩定","evidence_level":"一手（電話會議逐字稿）","settle_metric":"EMEA 排除設備銷售的基礎量年增","if_then":["若 EMEA 基礎量連兩季 ≤ −2% → 熊市機率由 25% 升到 30%，停止加碼"],"evidence_refs":["end_markets#2"]},{"axis":"現在買或等回檔","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：Q3 營收、營業利益、EPS 都創季度紀錄且優於 7 月指引；2027 年有重組節省、Lincare 拖累（今年約 1.5%–2% EPS 成長）消失、Woodside 下半年起量、電子約 20 億美元專案四項順風，管理層說 8%–12% 不需總經幫忙；A 級信用、淨負債約 228 億美元相對約 2,588 億美元 EV 很輕；品質複利股很少便宜，等回檔可能等不到","side_b":"等的理由：前瞻約 28.7 倍、P/S 與 EV/S 在近 4 個年度端點最高，一年基本情境上檔約 1.6%；Q4 指引只年增 5%–7%，FY2027 共識僅 18.20 美元；RSI 69.4 接近過熱","ruling":"⚖ 選等：依據是估值不是基本面；硬數據點＝28.7 倍對三年 7.6% 的基本 EPS 複利，PEG 約 3.8。約束只有價格，解除條件＝股價 ≤ 460 美元（約 2027 年基本 EPS 的 24 倍、貼近 104 週均線）；2027 年指引中點不低於 8% 是同時要成立的安全條件","evidence_level":"事實表估值數字＋一手電話會議","settle_metric":"股價對 2027 年基本情境 EPS 19.0 美元的倍數，與 2027 年 2 月指引中點","if_then":["若股價續漲到 560 美元以上而 2027 年指引尚未公布 → 不追","若股價跌到 460 美元以下且 Q4 價格貢獻仍 ≥ +2% → 分批反買，首倉 2%","反向條件：若 2027 年指引中點 < 8% → 即使股價到 460 美元也不買，改等 2027 年 EPS 的 22 倍以下"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"價格引擎是否續航","type":"假設驗證","maps_to":"H1","metric":"全公司價格貢獻與排除成本轉嫁的營業利益率年變化","threshold":"價格 < +2% 或排除成本轉嫁營益率年減","action":"停止加碼","source_freq":"每季財報","date":"2027-02","evidence_refs":[]},{"n":2,"text":"2027 年全年 EPS 指引","type":"Single Thing","maps_to":"H2","metric":"2027 年調整後 EPS 指引中點年增（排除匯率）","threshold":"< 8%","action":"減碼至半倉","source_freq":"一次性（Q4 2026 財報電話會議）","date":"2027-02","evidence_refs":[]},{"n":3,"text":"專案積壓轉成量","type":"假設驗證","maps_to":"H3","metric":"sale of gas 專案積壓與電子終端市場年增","threshold":"積壓 < 70 億美元或電子年增 < 10%","action":"停止加碼","source_freq":"每季電話會議","date":"2027-04","evidence_refs":[]},{"n":4,"text":"俄羅斯法律案件","type":"風險","maps_to":"R2","metric":"俄羅斯案件判決確定、資產扣押與損失認列合計","threshold":"≥ 10 億美元","action":"減碼","source_freq":"10-Q／10-K 或有事項附註，每季","date":"2027-02","evidence_refs":["geo_supply_chain#0","geo_supply_chain#4","major_events#1","lawsuit_class_action#0"]},{"n":5,"text":"歐洲去工業化","type":"風險","maps_to":"R1","metric":"EMEA 排除設備銷售的基礎量年增","threshold":"連兩季 ≤ −2%","action":"停止加碼","source_freq":"每季電話會議","date":"2027-04","evidence_refs":["end_markets#2"]},{"n":6,"text":"成本回收落差與氦氣反轉","type":"風險","maps_to":"R3","metric":"排除成本轉嫁的調整後營業利益率年變化","threshold":"連兩季年減","action":"減碼","source_freq":"每季財報","date":"2027-04","evidence_refs":["geo_supply_chain#1"]},{"n":7,"text":"進場價位","type":"估值rearm","maps_to":null,"metric":"股價與 2027 年指引","threshold":"股價 ≤ 460 美元且 2027 年指引中點年增 ≥ 8%","action":"分批建立首倉","source_freq":"每日股價＋2027 年 2 月指引","date":null,"evidence_refs":[]},{"n":8,"text":"過高價位","type":"減碼","maps_to":null,"metric":"股價","threshold":"≥ 600 美元（約 2027 年基本 EPS 的 31.6 倍）且 2027 年指引未上修","action":"減碼三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":9,"text":"核心引擎失效","type":"清倉","maps_to":"H1","metric":"排除成本轉嫁營業利益率與 2027 年實際調整後 EPS","threshold":"連四季年減且 2027 年 EPS 年增 < 3%","action":"清倉","source_freq":"每季財報","date":"2028-02","evidence_refs":[]},{"n":10,"text":"全面複審","type":"複審日期","maps_to":null,"metric":"Q4 2026 財報與 2027 年指引","threshold":"公布日","action":"重跑完整研究","source_freq":"一次性","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"排除成本轉嫁的調整後營業利益率年變化","bear_threshold":"連兩季年減","window":"2026 Q4–2027 Q2","source":"Linde 季度財報新聞稿與電話會議","last_status":"warning"},{"metric":"2027 年調整後 EPS 指引中點年增（排除匯率）","bear_threshold":"< 8% 減碼；< 3% 清倉檢討","window":"2027 年 2 月","source":"Q4 2026 財報電話會議","last_status":"unknown"},{"metric":"全公司價格貢獻","bear_threshold":"單季 < +2%","window":"每季","source":"季度財報價量拆解","last_status":"ok"},{"metric":"sale of gas 專案積壓","bear_threshold":"< 70 億美元","window":"2026 年底–2027 年中","source":"季度電話會議","last_status":"ok"},{"metric":"俄羅斯案件損失認列或資產扣押","bear_threshold":"≥ 10 億美元","window":"至 2027 年底","source":"10-Q／10-K 或有事項附註","last_status":"warning"},{"metric":"年度 FCF／淨利","bear_threshold":"連兩年 < 0.75","window":"FY2026–FY2027","source":"年度財報現金流量表","last_status":"warning"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#1","reason":"來源是 GCR 的組織索引頁，沒有摘錄、交易金額或審查時程；內容是一樁地區性小型收購的第二階段併購審查，不是違規或濫用調查，證據本身連不到任何營收或利潤數字，無法設門檻或定價"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=1.9, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='早循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價 ≤ 460 美元（約 2027 年基本情境 EPS 的 24 倍）且 2027 年 2 月指引中點年增 ≥ 8%","exec_line":"現價不追；已持有者續抱不加碼；股價 ≤ 460 美元且指引達標時分批建立首倉；2027 年指引中點 < 8% 則減至半倉"},"reasoning":{"industry":"Q3 2026 營收 94.04 億美元（年增 9%，扣掉匯率、成本轉嫁、併購、工程各約 1% 後基礎 +5%＝價 +3%、量 +2%），調整後營業利益 27.63 億美元、利益率 29.4%（年減 30bp，排除成本轉嫁持平）；GAAP 營業利益 21.5 億美元、22.9%，差額主要是 4.25 億美元重組費用。TTM 毛利率 47.86%。三種配送：現場供氣（能源成本當月轉嫁）、merchant 液態（三至七年需求合約）、瓶裝；另有工程（賣廠）與 Lincare 居家照護（年化營收約 23 億美元，本季移到其他部門並評估策略選項）。Q3 終端市場：化工能源（約 22%）+12%、製造（約 21%）+7%、醫療（約 15%）+2%、金屬礦業（約 12%）+3%、電子（約 10%）+15%、食品飲料（約 9%）+3%。單點依賴：10-K 稱不依賴單一或少數客戶，2025 年約 64% 營收在美國以外；唯一明顯集中點在供給端，氦氣貨源集中卡達。產業時鐘判 I：歐洲量由 12–18 個月前的 −2%～−3% 回到持平、美國化工與金屬走強，但公司指引不假設總經改善。供需持久性：結構性持久，現場長約與管線讓供給難被新進者複製，量則隨工業產出循環。","moat":"機制：工業氣體運輸成本高，供應半徑以工廠與管線為中心，現場供氣蓋在客戶廠旁、簽長約並當月轉嫁能源成本，merchant 簽三至七年需求合約；10-K 明列管線網絡所在地是競爭優勢。可證方向：對 Air Products 的 TTM 營業利益率高約 2.2pp、毛利率高約 15.8pp、FCF 利潤率一正一負（期間不一致，LIN 至 2026-09、APD 至 2026-06）；ROIC 差距與趨勢事實表未涵蓋，所以給 B 不給 A，升 A 需要對最強同業 ROIC 差距為正且擴大的證據。定價力 9：Q3 價格 +3% 跨各區，量仍 +2%，美洲排除一次性回收後跑速約 4%；氦氣漲價只回收調度成本、刻意不過度漲價。執行力 8：營業利益率 2022→2025 由 19.4% 升到 27.2%，但 2026 年 Q2、Q3 調整後營益率年減 60bp、30bp，CEO 自承 Q2 未達股東期待，Q2 承諾的第三季環比改善也小幅落空（29.5%→29.4%），拖累來自 Lincare 與工程。趨勢判穩定：利潤率擴張暫停但定價力未退。當期 ROIC 因缺投入資本無法計算，以 TTM 營業利益率 27.08% 與資本支出約占營收 15%–16% 看屬高利益率、低周轉，關鍵在再投資報酬。產業態勢：雙向拉鋸——競爭軸靜態（10-K 未點名新進入者，對手仍是 Air Liquide、Air Products、Messer、大陽日酸），結構軸美國灣區化工與電子轉好、歐洲去工業化變差，其他結構變數是俄羅斯訴訟與關稅風險。","growth":"成長拆解：Q3 2026 基礎銷售 +5%＝價 +3%＋量 +2%，量的一半來自專案積壓，有機量多是亞太與歐洲的設備銷售。共識 EPS：2026 年 17.89 美元、2027 年 18.20 美元（只年增 1.7%，與 2026-07-31 CEO 所說不靠總經的 8%–12% 演算法落差大）；2028 年共識事實表未涵蓋，三年年複合算不出來。內生天花板因缺投入資本與折舊算不出數字；共識成長低於基礎銷售成長，不存在需要歸因的正缺口。基本情境三年 EPS 年複合 7.6% 可拆成價、量與減股，不依賴利潤率擴張或估值重評。跑道：工業氣體不是滲透率故事，電子（占 10%、Q3 +15%，約 20 億美元專案分 2–3 年投產）與太空（2030 年目標 10 億美元）占比小，歐洲（CEO 稱零催化劑）與中國內需拖累；五年後仍是約工業產出加通膨的成長，判中等。衰退信號亮一個：EPS 成長長期高於營收成長；FCF／淨利 2025 年 0.74，再一年就亮第二個。","governance":"現金：Q3 2026 FCF 17.77 億美元；年度 FCF／淨利 2023 年 0.89、2024 年 0.75、2025 年 0.74，FCF 利潤率由 2022 年 17.1% 降到 TTM 14.0%，主因專案資本支出增加（全年約 55–60 億美元）。去向：前三季部署逾 90 億美元，約一半投入事業、一半以股息與回購回饋股東，精確四分事實表未涵蓋。SBC／營收事實表未涵蓋，但稀釋股數年減約 2%。營運槓桿：Q3 營收 +9%、調整後營業利益 +8%，差 1pp，未到壓縮。資產負債：淨負債約 227.6 億美元，第三方筆記列 S&P 歐元債評等 A。俄羅斯案件二手來源估或有負債約 18 億美元，約每股 3.9 美元。","valuation":"前瞻本益比 28.7 倍＝514.24 ÷ 17.89（FY2026 共識，已有三季實績且落在公司指引 17.82–17.92 內）；FY2027 本益比 28.3 倍。三年基本情境 EPS 年複合 7.6%，PEG 約 3.8；以 FY2027 本益比計約 3.7。一年基本情境：2027 年 EPS 19.0 美元 × 27.5 倍＝522.5 美元，上檔約 1.6%；三年：2029 年 22.3 美元 × 26 倍＝579.8 美元，上檔約 12.7%。賣方 2026 年 7–8 月目標均價 548–562 美元（高 600、低 460），比現價高 7%–9%，全距 1.3 倍，支持偏貴但非泡沫。同業本益比事實表未涵蓋，終端倍數無法做同業現值對照，這是本輪估值最大的資料缺口。","premortem":"壓力測試四項過三項：工業衰退量 −3%——長約與當月轉嫁讓 EPS 大致持平，過；氦氣供應恢復、價格回落——管理層說氦氣漲價被成本吃掉、利潤率未受惠，回落時衝擊有限，過；俄羅斯約 18 億美元或有負債全數認列——約每股 3.9 美元、股價的 0.8%，一次性，過；EPS 兩年持平且倍數回到 22 倍——股價約 −23%，不過。最大回撤以倍數壓縮推估 −20%～−35%，歷史回撤事實表未涵蓋。價值陷阱判中度：亮一個衰退信號（EPS 成長長期高於營收成長），FCF／淨利接近第二個。法說未正面回答的有：Lincare 是否獲利與出售時程、2027 年氦氣是否順風、荷莫茲海峽解決後的影響（皆 2026-07-31 場次）；Q3 只補充 Lincare FCF 為正。"},"plain":{"six":{"how_it_makes_money":"賺製造、化工能源、電子與醫療客戶的工業氣體錢：在客戶廠旁或管線網絡上供氣，用長約鎖量、合約條款轉嫁能源成本、隨通膨調價；錢卡在本地供應密度加合約轉嫁條款這一節點。","moat":"護城河穩定：現場長約與管線網絡讓 Linde 每季漲價約 3% 仍不掉量，但 2026 年利潤率擴張暫停，Lincare 與工程拖累執行面。","growth":"成長跑道中等：成熟寡占，EPS 複利靠價格 3%–4%、量 1%–2%（一半來自專案積壓）與每年約 2% 的減股；電子與太空是增量但規模小。","capital":"資本配置紀律好但回購買在高倍數：前三季部署逾 90 億美元，約一半投資、一半回饋股東，稀釋股數年減約 2%。","valuation":"偏貴：現價要求 2027 年起回到約 8% 的 EPS 複利，且市場持續給 25 倍以上；EPS 複利我信，倍數守在 28 倍以上我不信。","how_wrong":"最可能看錯的地方：把價格與減股撐出的 EPS 複利，當成能長期撐住 28 倍的成長；實際量能只有約 2%，一半來自專案。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 460 美元以下（約 2027 年基本情境 EPS 的 24 倍、貼近 104 週均線 461.9 美元），且 2027 年 2 月指引中點年增不低於 8%","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":514.24,"week26_return_pct":1.9,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母用 FY2026 共識 17.89 美元，三季已實現、爭議小；FY2027 共識 18.20 美元只年增 1.7%，與管理層 8%–12% 演算法差距大，原因事實表未涵蓋，估值不以它為錨，待 2027 年 2 月指引確認"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年全年 EPS 指引","impact":"高","watch":"指引中點年增是否 ≥ 8%（排除匯率）、Lincare 重組與策略選項進度"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"Woodside 氨廠兩組 ATR 氫氣設備分批啟動，下半年開始貢獻、2028 年滿載","impact":"中","watch":"啟動時程是否延後、客戶策略檢討結果"},{"date":null,"date_precision":null,"type":"other","event":"Lincare 策略選項評估結果（管理層未給時程）","impact":"中","watch":"出售價格與是否認列損失"},{"date":null,"date_precision":null,"type":"macro","event":"荷莫茲海峽與卡達氦氣出口恢復","impact":"中","watch":"氦氣價格回落速度與 Linde 長約客戶留存"}],"_projected_from":"v19"}
```
