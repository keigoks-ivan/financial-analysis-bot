你是 stock-analyst v20 的**散文層（prose）agent**，標的 SPOT（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPOT_20261024/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：SPOT　日期：2026-10-24　archetype：None　前份裁決：2026-07-11　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1541B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（590B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1122B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1362B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1026B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（406B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（784B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1851B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3613B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1541B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1541           3821-5459      5 條（2–6 內）  
s3                  8000         590           5187-7410      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3510          8043-11490      5 條（2–6 內）  
s6                 11000         406          7416-10594      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         784           1901-2716      5 條（2–6 內）  
s10                 5000        1851           2204-3149      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1541           2000-3459      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4767B；至少需散文≈40.23KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60
−60%
−58%
−35
−35%
−12.43%
−7.05%
0
0.5%
0.7
0.7%
0.75
1
1.22
1.3
1.4
1.5%
1.56
1.75%
1.8%
1.8
2
02
2%
2.5
2.7%
3%
3
03
3.06
3.16
3.7
3.94%
04
4%
4
4.4
4.5
4.8
4.95
05
5%
5
5.06
5.3
6
6.72
7
7%
7.05%
7.2%
7.35
7.5%
7.6%
7.8
7.88
8%
8
8.2
8.5%
9%
9.7
10
10%
10.51
11%
11
11.5%
11.99
12
12.43%
12.78
12.78%
12.8%
12.99
13%
13.45
13.5%
14%
14
14.47
14.65%
15
15%
15.8
16.3
16.4
16.8
17
17.2
17.24
17.4%
18%
18
18.04%
20
20%
21.0
21
21.8%
21.98
22%
22.1
23.5
24
24.95%
25
25%
25.5
26
27
27%
27.8%
28
28.5
29
29.68%
29.73%
30%
30
30.7
31.98%
32
32%
32.5
32.8%
33.0%
33
33%
33.3%
33.8%
33.89
33.9
34
35%
37
39.5
40%
41.0%
43
43.4
43.44
45
45%
45.77%
45.8%
48
49
49%
49.12%
49.69
50
50%
52
60%
62.0%
70%
70
70.6
71.7%
90
95%
99
100%
100
130
140
150%
150
180
220
300
340
344
360
$420
425
479.77
480
500
584
584.22
594.92
615
878
2018
2022
2024
2025
2026
2027
2028
2029
2030
2031
20261024
1,224
1,303.5
2,000
2,500
8,700
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
{"meta":{"ticker":"SPOT","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"Spotify Technology S.A."},"oneliner":"逐季兌現、毛利率擴張、帳上近百億歐元現金無負債，生意品質好；但股價 584 美元已貼近分析師均值，FY2027 本益比約 34 倍，FY2026 共識三個月內下修 7%，報酬得靠 2030 年利潤率目標全數達成，等回到約 480 美元再談。","thesis":{"H":[{"id":"H1","text":"訂戶與 ARPU 雙引擎持續：總 Premium 訂戶年增至少 8%，ARPU 固定匯率年增至少 3%","2y":"2028 年 Q4 訂戶約 3.7 億","5y":"2031 年訂戶約 4.5 億，ARPU 每年仍正成長","10y":null,"threshold":"Premium 訂戶年增 ≥ 8%；Premium ARPU（固定匯率）年增 ≥ 3%","source":"公司季報 6-K 與法說","drift_rule":"訂戶年增連 4 季低於 7.6% → 削弱；連 6 季低於 7.2% → 反轉"},{"id":"H2","text":"利潤率朝 2030 年目標擴張：毛利率 35%–40%、營業利益率 20% 以上","2y":"FY2027 毛利率至少 33.8%（FY2026 約 33.3% 加 50bp）","5y":"FY2030 毛利率 ≥ 35%、營業利益率 ≥ 20%","10y":null,"threshold":"全年毛利率年增 ≥ 50bp；季毛利率不低於 32.8%","source":"公司季報 6-K、投資人日 2030 目標","drift_rule":"季毛利率連 4 季年減 → 削弱；續約後連 2 季低於 32.8% → 反轉"},{"id":"H3","text":"投資年過後營業利益增速回到高於營收：Q4 2026 營業利益兌現，2027 年營業費用增速低於營收增速","2y":"Q4 2026 營業利益 ≥ 7.8 億歐元；FY2027 共識 EPS 不低於 16.4","5y":null,"10y":null,"threshold":"Q4 2026 營業利益 ≥ 7.8 億歐元（指引 95%）；FY2027 共識 EPS ≥ 16.4（現值 95%）","source":"公司季報與法說、Koyfin 共識快照","drift_rule":"連 2 季偏離門檻 5% 以上 → 削弱；連 3 季偏離 10% 以上 → 反轉"}],"R":[{"id":"R1","text":"UMG／WMG 2027 年 Q1 續約提高核心串流授權分成，壓住毛利率擴張","h_ref":"H2","clock":"🔥","threshold":"續約後連 2 季毛利率低於 32.8% 或年減","evidence_refs":[]},{"id":"R2","text":"生態系對手（YouTube Music、Apple、Amazon 預載）與 AI 新消費方式搶走增量訂戶，尤其年輕族群","h_ref":"H1","clock":"🔥","threshold":"年度 Premium 淨增低於 2,000 萬（管理層自述 2018 年起每年 ≥ 2,500 萬）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0"]},{"id":"R3","text":"漲價邊際失效：漲價後流失上升，Q1 2026 北美淨增曾偏軟","h_ref":"H1","clock":"⚡","threshold":"任一主要區域漲價後該區訂戶連 2 季季減","evidence_refs":["supply_demand_durability#1"]},{"id":"R4","text":"監管與訴訟成本：土耳其反壟斷調查、USTR 報復威脅、MLC 授權費訴訟","h_ref":"H2","clock":"🐢","threshold":"任一案出現處分或新增費用超過年營業利益 5%","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#3","reg_tariff_export#0","major_events#0"]},{"id":"R5","text":"指引落空與共識下修：Q2 營業利益指引曾低於共識約 8%，Q1 財報後單日跌 12.43% 並引來律所調查","h_ref":"H3","clock":"⚡","threshold":"營業利益連 2 季低於自家指引超過 5%，或 FY+1 共識三個月下修超過 10%","evidence_refs":["capital_markets_pricing#0","major_events#1","lawsuit_class_action#0"]}],"single_thing":{"description":"2027 年 Q1 UMG 與 WMG 兩年期合約續約時，核心串流授權分成條件惡化","why_fatal":"Base 的 EPS 路徑靠毛利率往 35%–40% 擴張；以 TTM 營業利益率 14.65% 計，毛利率每少 1 個百分點，營業費用不變下營業利益少約 7%，五年 EPS 路徑直接下移","if_happens":"Base 毛利率路徑下修、Bear 機率上調到 40%，不進場；若已持有則減碼一半，毛利率再低於 32.8% 兩季則清倉","how_monitor":"續約公告、續約後兩季毛利率、管理層是否改口 2030 年毛利目標","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":33.89,"peg_fy2":1.22,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":10.51,"FY2026E":13.45,"FY2027E":17.24,"FY2028E":21.98},"fy_end_month":12,"eps_basis":"FY2026–FY2028 為 Koyfin 共識（事實表標美元）；FY2025A 取年報稀釋 EPS 10.51，公司以歐元報表，基期與共識可能幣別不同"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SPOT_20261024/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"訂閱收入約九成、資本支出低、營運資本為負，利潤率由虧轉盈後仍在擴張，最大成本是上游授權分成"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：漲價後留存穩定（公司說法、RSM 報導），Q3 各區域訂戶季增，全球付費滲透率不到 4%（Q3 法說）","bargaining":{"up":"弱：三大唱片公司集中，UMG 與 WMG 合約 2027 年 Q1 到兩年期節點；WMG 毛利率 45.8%，高於 Spotify 的 32.8%","down":"強：美國個人方案 2026 年 2 月由 11.99 漲到 12.99 美元，Q3 ARPU 仍年增 7.5%","geo":"成長來自拉美與新興市場；土耳其競爭局調查中，USTR 2025-12 威脅對含 Spotify 在內的歐洲公司報復"},"profit_pool_dir":"往 Spotify 移：毛利率 2022 年 24.95% → 2025 年 31.98% → Q3 2026 33.0%，全年指引擴張約 130bp","tam_table":[{"item":"全球人口付費滲透率","value":"不到 4%（Q3 2026 法說）"},{"item":"瑞典","value":"近 50%"},{"item":"英國、德國","value":"20%–25%"},{"item":"拉丁美洲","value":"約 11%"},{"item":"新興市場","value":"不到 3%"},{"item":"全球音樂串流訂閱（產業）","value":"2027 年底超過 10 億、2029 年約 12 億（Futuresource 預測）；拉美、亞太至 2029 年 CAGR 14%、10%"},{"item":"利潤池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"高頻使用累積的個人化品味資料，加上嵌進車用、音箱、AI 代理等第三方介面的普及度，讓用戶很少主動退訂；漲價後留存穩定是可觀察的證據","execution":8,"pricing":8,"combined":8.0,"score":8.0,"grade":"B","trend":"→","trend_evidence":"擴大面：Q3 毛利率年增約 140bp、廣告成長 3%→9%、美國市占六年 +8–10pp（投資人日）、Midia 稱 2025 年各平台中淨增最多。縮減面：YouTube Music 美國訂戶一年 +45%、大廠裝置預載、UMG／WMG 2027 年 Q1 續約。兩邊抵銷，判持平。","peer_na_reason":null,"threats":[{"level":"🔴","text":"生態系攻擊：Apple、Alphabet、Amazon 在裝置預載或預設自家音訊服務，YouTube Music 美國訂戶一年增 45%，搶的是成熟市場的增量訂戶","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]},{"level":"🟡","text":"AI 帶來新的內容消費方式，年輕族群可能轉向其他產品；公司策略是把自己做成可被其他代理呼叫的服務，目前代理內收聽仍在 Spotify 內發生（Q3 法說）","p":"30%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉（營業利益率中段、投入資本極輕）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"個人方案的使用者就是付款者，家庭方案由一人付款；逾 1 億用戶每月用 28 天，CEO 說問卷裡幾乎沒有人是忘了退訂；聽音樂屬於想要，但日常頻率高，延後購買代價就是每天少了習慣的服務"},{"item":"決策層級","level":"🟡","text":"替代決策發生在個人或家庭層級；漲價後流失極低是最好的代理變數。但大廠把音樂綁進手機與會員組合，換服務的摩擦主要是播放清單與聽歌紀錄，搬遷成本中等"},{"item":"價值鏈分配","level":"🟡","text":"上游三大唱片公司集中，Spotify 毛利率 33% 代表授權分成仍拿走大部分；毛利率 2022–2026 年擴張約 8 個百分點，靠播客、有聲書與行銷平台。2027 年 Q1 兩家續約是檢驗點"},{"item":"社會容忍度","level":"🟡","text":"土耳其競爭局以演算法歧視與掠奪性定價為由調查；USTR 威脅對歐洲數位公司報復；MLC 授權費訴訟未結。目前沒有處分金額，但漲價與分成都受監管與輿論檢視"}],"roiic":"事實表未涵蓋（投入資本口徑缺）","reinvest_rate":"事實表未涵蓋；營運資本為負、資本支出低，帳面再投資率趨近零或為負，再投資主要以研發與行銷費用化","endo_ceiling":14,"formula_note":"增量 ROIC 乘再投資率的公式在這家公司不適用：成長靠費用化的產品與行銷投入，而不是資本支出。改用不靠利潤率擴張的成長上界代理：Q3 2026 固定匯率營收成長 14%，與 2030 年中段兩位數營收 CAGR 目標一致。超出 14% 的 EPS 成長都要靠利潤率擴張。"},"spread_table":[{"metric":"毛利率","SPOT":32.8,"TME":44.32,"NFLX":49.12,"UMG.AS":null,"WMG":45.77,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","SPOT":14.65,"TME":29.73,"NFLX":29.68,"UMG.AS":null,"WMG":16.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","SPOT":18.04,"TME":28.44,"NFLX":23.06,"UMG.AS":null,"WMG":3.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","SPOT":7.36,"TME":null,"NFLX":7.67,"UMG.AS":null,"WMG":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"TME","gm":44.32,"om":29.73,"fcf_margin":28.44,"rd_intensity":null,"strategy_note":"中國市場結構不同，營業利益率 29.73%，不能直接當 Spotify 的利潤率天花板","period":"TTM ending 2026-06-30（4季加總）"},{"name":"NFLX","gm":49.12,"om":29.68,"fcf_margin":23.06,"rd_intensity":7.67,"strategy_note":"自製內容攤提可以靠規模稀釋，毛利率 49.12%；Spotify 音樂成本按營收比例分成，規模槓桿較小","period":"TTM ending 2026-06-30（4季加總）"},{"name":"UMG.AS","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"最大供應商，事實表只有一季且缺營收，無法比較；2027 年 Q1 續約是近期最大變數","period":"TTM ending 2026-03-31（1季加總）"},{"name":"WMG","gm":45.77,"om":16.11,"fcf_margin":3.94,"rd_intensity":null,"strategy_note":"是供應商，毛利率 45.77% 但 FCF 利潤率只有 3.94%；續約時是議價對手","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（訂戶 +9%）加價（ARPU +7.5%）為主；回購只中和稀釋；收購規模小且條件未揭露","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"Q3 2026 固定匯率營收成長 14% 與 2030 年中段兩位數營收 CAGR 目標；共識 EPS 年化 27.8% 超出部分歸因利潤率擴張","segments":{"expanded":false,"reason":"Premium 約九成、廣告約一成；Q3 廣告分部金額與播客、有聲書各自毛利率事實表未取得，無法拆分，利潤率變化只能看合併毛利率"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q3 年增約 140bp，Q4 指引再增約 70bp"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"YouTube Music 美國訂戶 +45%，但沒有 Spotify 市占下降的直接數據；投資人日稱美國市占六年 +8–10pp"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"Q1 2026 美國漲價後北美淨增偏軟，Q2、Q3 恢復，訂戶仍年增"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"共識 EPS 年化約 27.8%，營收約中段兩位數，差額來自利潤率擴張"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"過去 12 個月 FCF 約 32 億歐元，高於 FY2025 淨利 22.1 億歐元"},{"signal":"SBC／營收超過 5% 且上升","lit":false,"note":"Q3 約 1.75%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"產業訂閱預估 2029 年 12 億；AI 替代是風險因素，尚未見量化萎縮"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"資本支出低"},{"signal":"停止投資且收入 3 年內下滑","lit":false,"note":"仍在投資，營收成長"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，回購只中和稀釋並小幅退還現金；現金去向四分事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年收購規模小、條件未揭露（WhoSampled 2025-11），無法計算已實現增量報酬","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"年初至 10-21 回購 220 萬股、11 億美元，均價約 500 美元；以 FY2026 共識 EPS 13.45 計盈餘收益率約 2.7%","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"員工持股年稀釋約 100 萬股（約 0.5%）已被回購抵銷；Q3 SBC 約占營收 1.75%","grade":"過"}]},"valuation":{"basis":"本益比（FY2026 43.4 倍、FY2027 33.9 倍）加 PEG","tier":null,"peers":{"expanded":false,"reason":"事實表同業只有利潤率，沒有同業本益比，無法做倍數對照"},"fwd_pe":43.44,"peg":1.56,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2027 本益比 33.9 倍、PEG 約 1.56，屬合理區間上緣；FY2026 共識三個月下修 7.05% 而股價上漲，倍數擴張；現價與分析師均值目標只差 1.8%；五年分位資料缺口。綜合判偏貴，比前份往貴一級。","upside_short_pct":1.8,"upside_mid_pct":5.3},"trap_analysis":{"verdict":"🟡","label":"生意不是陷阱，風險在上游分成與價格"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"20-F 自述大廠裝置預載使其居重大競爭劣勢；YouTube Music 美國訂戶一年 +45%；AI 帶來新的消費方式可能使年輕用戶轉移；UMG／WMG 2027 年 Q1 續約","assumption":"成熟市場增量訂戶被生態系對手吃掉，同時續約抬高授權分成，毛利率擴張停止","consequence":"Base 的利潤率路徑失效，EPS 停在 15–17 美元，倍數壓到 20 倍，股價約 340 美元","ruling":"部分採納：Bear 機率給 30%。反駁點是公司數據：逾 1 億用戶每月用 28 天、美國市占六年 +8–10pp、2025 年淨增各平台最多，Q3 訂戶還超出指引","watch":"年度訂戶淨增低於 2,000 萬；續約後兩季毛利率","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0"],"fact_refs":["f_kpi7_premium_subscribers","f_kpi3_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"現金 99 億歐元閒置；回購在 FY2026 約 43 倍本益比、均價約 500 美元買入；管理層保留併購彈性；投資人日說 2027 年成為完整納稅人、正常稅率約 22%；Gustav 說 AI 投資會維持在目前水準","assumption":"營運如期擴張，但稅率上升、高價回購與可能的大型收購稀釋每股報酬","consequence":"營業利益達標但每股 EPS 成長比營業利益慢，報酬再少 1–2 個百分點","ruling":"採納：資本配置判 B，回購收益率不過關；稅率正常化影響共識是否已計入事實表未涵蓋","watch":"2027 年有效稅率；單筆收購超過市值 5%；回購均價對應的本益比","evidence_refs":[],"fact_refs":["f_kpi4_free_cash_flow","f_consensus_eps_fy1"]},{"view":"價格已反映太多","evidence":"股價 584 美元與分析師均值 594.92 美元只差 1.8%；FY2026 共識三個月下修 7.05% 而股價 26 週漲 12.78%；RSI 70.6；Q2 營業利益指引曾低於共識約 8%","assumption":"市場已經把 2030 年利潤率目標當成會達成","consequence":"Base 五年年化只有約 9%，兩年上檔約 5%，任何一次指引落空都會讓倍數先壓","ruling":"採納：這是本次觀望的唯一約束","watch":"股價對 FY2027 共識的倍數；共識修正方向","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct","f_rsi14","f_week26_return_pct"]},{"view":"論點成功但股東經濟變差","evidence":"MLC 2024 年 5 月就授權費提告；土耳其競爭局調查演算法歧視與掠奪性定價；USTR 2025-12 威脅報復；Pomerantz 律所 2026 年 5 月宣布調查，起因是 Q1 財報後單日跌 12.43%","assumption":"其中一案演變成費用或處分，直接吃掉利潤率擴張","consequence":"若處分或新增費用超過年營業利益 5%，Base 路徑要下修","ruling":"反駁：目前都沒有金額，律所只是調查通知、未見已提起的集體訴訟，USTR 只是威脅；Drake 灌水案已獲駁回。列監測不進情境","watch":"任一案出現金額或判決；USTR 是否實施","evidence_refs":["major_events#0","major_events#1","lawsuit_class_action#0","regulatory_antitrust#1","regulatory_antitrust#3","reg_tariff_export#0"],"fact_refs":[]}],"max_dd":{"lo":-60,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 479.77 → 本次 584.22（+21.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=479.77","side_b":"本次 price_at_dd=584.22","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 479.77 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 479.77 美元：Bull 價 1,224、Bear 價 360，五年期望值 +62.0%，基準年化 11.5%，不對稱比 4.8","side_b":"本次情境、股價仍用 479.77 美元：Bull 價 1,303.5、Bear 價 344，五年期望值 +71.7%，基準年化 12.8%，不對稱比 5.06","ruling":"先換情境、股價不動：五年期望值多 9.7 個百分點，基準年化多 1.3 個百分點。不對稱比由 4.8 變為 5.06。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 479.77 美元：五年期望值 +71.7%，基準年化 12.8%，不對稱比 5.06","side_b":"本次情境、股價 584.22 美元：五年期望值 +41.0%，基準年化 8.5%，不對稱比 2.5","ruling":"再換股價、情境不動：起點價上漲 21.8%，五年期望值少 30.7 個百分點，基準年化少 4.4 個百分點，不對稱比由 5.06 降到 2.5。合計五年期望值比前份少 21.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價上漲帶動的估值與情境機率變動","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 479.77 美元，估值中性偏貴，Bull 25%／Bear 32%，最大回撤 −58%，裁決觀望","side_b":"股價 584.22 美元（+21.8%），FY2026 共識同期下修，FY2026 本益比 43.4 倍、FY2027 約 33.9 倍，估值改偏貴；Bull 25／Base 45／Bear 30；回撤區間 −35%～−60%","ruling":"估值結論往貴一級。Bear 機率由 32% 降到 30%，因 Q3 營收、訂戶、毛利率全數達標或超標，但價格上漲讓報酬變薄，裁決仍是觀望","evidence_level":"公司財報、共識快照","settle_metric":"股價對 FY2027 共識本益比","if_then":["股價回到 480 美元以下且 FY2027 共識未下修超過 5% → 重跑後分批進場","股價續漲但 Q4 營業利益未達 7.8 億歐元 → 不追"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"跑道判讀","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"前份判中等跑道","side_b":"判寬：Q3 法說首次量化全球付費滲透不到 4%、英德 20%–25%、拉美約 11%、新興市場不到 3%；有聲書年底擴到 180 多個市場","ruling":"改判寬。滲透率遠低於 35%，且有聲書已是有營收的第二條曲線（Audiobooks+ 年化經常性收入逾 1 億美元）","evidence_level":"公司法說","settle_metric":"新興市場訂戶占淨增比重；有聲書擴張後 ARPU","if_then":["新興市場淨增放緩且有聲書擴張後兩季 ARPU 沒有改善 → 改回中等跑道"],"evidence_refs":[]},{"axis":"維持不變的判斷","cause":"新證據","prior_field":["signal","trap","moat_trend","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、價值陷阱中度、護城河持平、品質複利成長型、非循環股","side_b":"本次相同","ruling":"新證據兩邊都有：Q3 毛利率年增約 140bp、廣告回升到 +9% 支持執行面；YouTube Music 美國 +45% 與 2027 年 Q1 續約壓住方向。結論不動","evidence_level":"公司財報、第三方產業資料","settle_metric":"續約後毛利率；年度訂戶淨增","if_then":["續約後兩季毛利率都不低於 32.8% 且年淨增超過 2,500 萬 → 護城河改判擴大"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"進場條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Q2 2026 NA Premium 訂戶回穩（否則連 2 季負＝結構飽和確認）＋7 月 Sony v. Suno 判決明朗；或回檔至 BB 下軌 ~$420","side_b":"股價回落至 480 美元以下（約 FY2027 共識 EPS 28 倍），且 FY2027 共識同期下修不超過 5%","ruling":"北美回穩已由 Q3 各區域訂戶季增兌現，不再是約束；Suno 判決結果證據包未涵蓋，不作條件。現在唯一約束是價格，進場改成價格錨；480 美元由 FY2027 共識 17.24 乘 28 倍得出","evidence_level":"公司法說、共識快照","settle_metric":"股價對 FY2027 共識本益比","if_then":["條件達成 → 重跑後分批進場，首筆小倉位","共識下修超過 5% → 進場價同步下移"],"evidence_refs":[]},{"axis":"賣出門檻新設","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設賣出門檻（null）","side_b":"季毛利率連 2 季低於 32.8%；年度訂戶淨增低於 2,000 萬；FY+1 共識三個月下修超過 10%；營業利益連 2 季低於自家指引超過 5%","ruling":"Q3 法說點名 2027 年 Q1 續約節點，前份的毛利率門檻要落成可執行的賣出條件","evidence_level":"公司法說","settle_metric":"續約後季毛利率","if_then":["持有時毛利率連 2 季低於 32.8% → 減碼一半","毛利率門檻觸發後年淨增也低於 2,000 萬 → 清倉"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"2027 年 Q1 UMG／WMG 兩年期合約續約時，核心串流授權分成條件惡化","ruling":"毛利率是 EPS 路徑數學上最大的單一敏感項：毛利率每少 1 個百分點，營業利益少約 7%。Q3 法說最後一題首次點名續約時點，因此設為唯一致命點","evidence_level":"公司法說","settle_metric":"續約後兩季毛利率與 2030 毛利目標是否改口","if_then":["續約後毛利率指引下修或 2030 目標改口 → Bear 機率上調到 40%，不進場；持有則減碼一半"],"evidence_refs":[]},{"axis":"廣告承諾措辭","cause":"新證據","prior_field":null,"side_a":"投資人日與 Q2 法說：廣告下半年回到兩位數成長","side_b":"Q3 廣告 +9%，CFO 改說 Q4「繼續往兩位數前進」","ruling":"可調和的程度差異：方向兌現（3%→9%），時點往後挪。廣告只占營收約一成，影響有限；但連續措辭軟化要記。Q2 營業利益指引也曾低於共識約 8%","evidence_level":"法說逐字稿","settle_metric":"Q4 2026 廣告成長率","if_then":["Q4 廣告仍低於 10% 且 2027 年 Q1 仍無兩位數 → 管理層承諾可信度下調，進場價再下移 5%"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：Q3 全部達標、Q4 指引營業利益 8.2 億歐元、費用增速 2027 年續降、無負債現金 99 億歐元、過去 12 個月 FCF 32 億歐元、付費滲透不到 4%，好生意少有便宜價","side_b":"觀望：價格已貼近分析師均值，FY2027 本益比約 34 倍，五年 Base 年化約 9%，續約結果未知","ruling":"觀望。生意好不等於現在這個價位有補償；唯一約束是價格","evidence_level":"公司財報、共識快照","settle_metric":"股價對 FY2027 共識本益比","if_then":["股價 480 美元以下且共識未下修 → 分批進場","Q4 達標且 2027 年費用增速低於營收增速、共識上修超過 5% → 進場價上調到 FY2027 共識 30 倍"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q4 2026 營業利益是否達指引","type":"假設驗證","maps_to":"H3","metric":"Q4 2026 營業利益","threshold":"≥ 7.8 億歐元（指引 8.2 億的 95%）","action":"未達 → 不追，Bear 機率上調 5 個百分點","source_freq":"季報（每季）","date":"2027-02","evidence_refs":[]},{"n":2,"text":"UMG／WMG 兩年期續約後的毛利率","type":"Single Thing","maps_to":"R1","metric":"季毛利率","threshold":"續約後連 2 季低於 32.8% 或年減","action":"觸發 → 不進場；持有則減碼一半","source_freq":"季報（每季）","date":"2027-05","evidence_refs":[]},{"n":3,"text":"價格回到有補償的區間","type":"估值rearm","maps_to":null,"metric":"股價與 FY2027 共識 EPS","threshold":"股價 ≤ 480 美元且 FY2027 共識下修不超過 5%","action":"重跑後分批進場，首筆小倉位","source_freq":"每日股價、共識快照","date":null,"evidence_refs":[]},{"n":4,"text":"生態系對手搶走增量訂戶","type":"風險","maps_to":"R2","metric":"年度 Premium 訂戶淨增","threshold":"低於 2,000 萬","action":"護城河改判縮減，不進場","source_freq":"季報（每季）","date":"2027-02","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]},{"n":5,"text":"共識持續下修","type":"風險","maps_to":"R5","metric":"FY+1 共識 EPS 三個月修正","threshold":"下修超過 10%（目前 −7.05%）","action":"進場價同步下移，停止加碼","source_freq":"共識快照（每月）","date":null,"evidence_refs":["capital_markets_pricing#0"]},{"n":6,"text":"Q4 財報與 2027 年展望後複審","type":"複審日期","maps_to":null,"metric":"Q4 結果與 2027 年費用、毛利指引","threshold":null,"action":"重跑判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"季毛利率（IFRS）","bear_threshold":"連 2 季低於 32.8% 或年減","window":"2027 年 Q1 續約後連續 2 季","source":"公司季報 6-K","last_status":"ok"},{"metric":"年度 Premium 訂戶淨增","bear_threshold":"低於 2,000 萬","window":"會計年度","source":"公司季報 6-K","last_status":"ok"},{"metric":"FY+1 共識 EPS 三個月修正","bear_threshold":"下修超過 10%","window":"滾動 90 天","source":"Koyfin 共識快照","last_status":"warning"},{"metric":"營業利益相對公司自家指引","bear_threshold":"連 2 季低於指引超過 5%","window":"滾動 2 季","source":"公司季報與法說","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=12.78, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 路徑是用量加價與利潤率目標撐起來的，但 EPS 沒有被推導到數字，歷史上高倍數成長股的 5 年報酬多半低於本案隱含的 17.4%，runway 的滲透率證據也還沒能回到原文，三項都不到站穩的程度，也沒有哪一項能直接判為不成立。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價回到 480 美元以下（約 FY2027 共識 EPS 28 倍），且 FY2027 共識下修不超過 5%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價回落至 480 美元以下（約 FY2027 共識 EPS 28 倍），且 FY2027 共識同期下修不超過 5%","exec_line":"條件達成後先重跑判斷，再分兩批進場，首筆小倉位；Q4 營業利益未達 7.8 億歐元時不追"},"reasoning":{"industry":"Q3 2026 營收 49.69 億歐元，固定匯率年增 14%；毛利率 33.0%、營業利益 6.72 億歐元、營業利益率 13.5%、單季自由現金流 7.35 億歐元。Premium 營收年增 15%，拆成訂戶 +9% 與 ARPU +7.5%；廣告年增 9%，CFO 說廣告只占營收約 10%。季末 MAU 7.88 億、付費訂戶 3.06 億，比指引多 100 萬。Q4 指引：訂戶 3.16 億、營收 52 億歐元、毛利率 33.8%、營業利益 8.2 億歐元。產業處在擴張期：Q3 各區域訂戶都季增，全球人口付費滲透率不到 4%，Futuresource 預估產業訂閱 2027 年底超過 10 億。供需屬結構性持久：美國 2026 年 2 月漲價，Q1 北美淨增偏軟，但 Q2、Q3 恢復，公司說 150 多個市場漲價後留存穩定。單點依賴在供給端：三大唱片公司集中，UMG 與 WMG 合約在 2027 年 Q1 到兩年期節點。對消費者有定價領導權（2026 年 8 月法說：樂於當品類價格領導者），對供應商沒有。毛利率從 2022 年 24.95% 升到 2025 年 31.98%，表示播客、有聲書與行銷平台正把利潤池往 Spotify 這一節移。分部金額、客戶與供應商占比事實表未涵蓋。","moat":"機制：使用頻率加個人化資料加裝置普及。逾 1 億用戶每月用 28 天（Q3 法說），漲價後流失低到管理層自己都意外（投資人日），美國 Premium 市占六年增加 8–10 個百分點。執行面給 8 分：Q3 毛利率年增約 140bp，廣告由 3% 回升到 9%，人數持平下產品出貨加速。定價權給 8 分：對消費者是價格領導者，但上游授權拿走大部分營收。同業比較是負的：營業利益率 14.65%，TME 29.73%、NFLX 29.68%，差距約 15 個百分點，所以兩項平均不能落到 8 分以上；生態系對手扣 1 分後約 7 分，等級 B。方向持平的理由：執行面在擴大，但 YouTube Music 美國訂戶一年增 45%，Apple、Alphabet、Amazon 在裝置上預載自家服務，2027 年 Q1 又要和兩家唱片公司續約，兩邊抵銷。同業 ROIC 與投入資本口徑事實表未涵蓋，以利潤率代替。","growth":"成長靠量加價：Q3 訂戶 +9%、ARPU +7.5%；回購只中和稀釋，近年收購都小。共識 EPS：FY2026 13.45、FY2027 17.24、FY2028 21.98，FY2026→FY2028 年化約 27.8%（家數事實表未涵蓋）。FY2025 實際稀釋 EPS 10.51 來自年報，公司以歐元報表，共識標美元，三年 CAGR 可能有幣別落差，所以用同源的兩年 27.8% 判斷。不靠利潤率的成長上界約 14%，缺口約 14 個百分點，歸因利潤率擴張：2026 年毛利率擴張約 130bp，2030 年目標毛利率 35%–40%、營業利益率 20% 以上，這部分可歸因，不是倍數擴張。跑道：全球付費滲透不到 4%，英德 20%–25%，瑞典近 50%，就算以每年 9% 訂戶成長，十年內也到不了 30%；有聲書擴到 180 多個市場、加購方案與廣告回升是第二條曲線。衰退信號只亮一個：EPS 成長明顯高於營收成長，原因是利潤率擴張。","governance":"過去 12 個月 FCF 約 32 億歐元（Q3 法說），對 FY2025 淨利 22.1 億歐元，轉換率約 1.4（期間不完全對齊）。Q3 SBC 8,700 萬歐元，約占營收 1.75%。季末現金 99 億歐元，除租賃外無負債。年初至 10 月 21 日回購 220 萬股、11 億美元，均價約 500 美元；2025 年 8 月恢復回購以來約 300 萬股，約占流通股 1.5%。以 FY2026 共識 EPS 13.45 計，買入時的盈餘收益率約 2.7%，低於十年期公債殖利率加 2%（殖利率事實表未涵蓋，但 2.7% 很難過關）。員工持股稀釋約 100 萬股已被抵銷，淨稀釋過關。收購（WhoSampled、Findaway、Sonantic）條件未揭露，無法算已實現報酬。現金去向四分、回購均價明細事實表未涵蓋。","valuation":"以 FY2026 共識 EPS 13.45 計本益比 43.4 倍，以 FY2027 的 17.24 計約 33.9 倍。FY2026→FY2028 共識年化約 27.8%，PEG 約 1.56。FY2026 已只剩一季，等同近乎實現值，所以主要看 FY2027。近三個月 FY2026 共識由 14.47 下修到 13.45（−7.05%），同期股價 26 週漲 12.78%，倍數上升不是盈餘推動。股價與 37 位分析師均值目標 594.92 美元只差 1.8%。兩年看，FY2028 共識 21.98 乘 28 倍約 615 美元，只有約 5%。五年 Base 若 FY2031 EPS 32.5、27 倍，約 878 美元、+50%，年化約 8.5% 加上約 0.7% 淨回購，落在中段偏弱；這段報酬全部來自 EPS，倍數是往下壓的。五年估值分位事實表未涵蓋（估值歷史只有最近一點）。同業倍數事實表未涵蓋。","premortem":"價值陷阱風險只亮一個信號（EPS 成長高於營收成長，原因是利潤率擴張），判中度。致命點是 2027 年 Q1 UMG 與 WMG 續約：以 TTM 營業利益率 14.65% 計，毛利率每少 1 個百分點，營業費用不變下營業利益少約 7%。第二是 YouTube Music 與大廠預載搶增量訂戶。第三個是反方向的錯：Q3 全部兌現、Q4 指引營業利益 8.2 億歐元，若 2027 年費用如承諾放緩，EPS 可能高於共識，等 480 美元可能等不到。監管與訴訟（土耳其調查、USTR 威脅、MLC 訴訟、律所調查）都沒有金額，列監測。"},"plain":{"six":{"how_it_makes_money":"賺的是全球個人與家庭的月訂閱費（約九成），廣告約一成；錢卡在上游唱片公司的授權分成，毛利率 33% 就是 Spotify 從每一歐元裡實際留下的部分。","moat":"→","growth":"🟢","capital":"B：回購已中和稀釋並開始退還多餘現金，但買在高本益比；收購小且無法驗證報酬。","valuation":"現價要求公司在 2030 年前把營業利益率拉到 20% 以上、EPS 維持約兩成年增，而且市場到時仍給 27 倍左右；我信生意，但不信現在這個價格還留有足夠補償。","how_wrong":"最可能看錯在三處：唱片公司續約抽走毛利擴張、生態系對手吃掉成熟市場增量、以及好生意被我低估而股價續漲。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 480 美元以下（約 FY2027 共識 EPS 28 倍），且 FY2027 共識下修不超過 5%","qc48_result":"pass","qc48_note":"Bull 路徑是用量加價與利潤率目標撐起來的，但 EPS 沒有被推導到數字，歷史上高倍數成長股的 5 年報酬多半低於本案隱含的 17.4%，runway 的滲透率證據也還沒能回到原文，三項都不到站穩的程度，也沒有哪一項能直接判為不成立。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":584.22,"week26_return_pct":12.78,"consensus_rev_3m_pct":-7.05,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 EPS 含年內約 2 億歐元一次性費用墊高與隨股價波動的社會費用，已近乎實現值；改以 FY2027 為主要錨，結論不依賴分母爭議"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"product","event":"有聲書擴展到 180 多個市場完成","impact":"中","watch":"Q4 毛利率是否守住 33.8% 指引"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年展望","impact":"高","watch":"營業利益是否達 7.8 億歐元以上、2027 年費用增速"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"UMG／WMG 兩年期合約續約節點","impact":"高","watch":"續約後兩季毛利率與 2030 毛利目標措辭"}],"_projected_from":"v19"}
```
